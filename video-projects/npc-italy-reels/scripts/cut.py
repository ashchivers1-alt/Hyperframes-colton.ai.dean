"""Cut each reel's segments out of the finished 4K edit, crop to 9:16 following Ash's face, scale to 2160x3840.
tight crop = 1045x1858 from the top of frame (stays above the edit's burned-in captions); full = 1215x2160 (no captions there).
Alternate segments get a 1.10x punch-in so the jump cuts read as intentional. Audio is cut at the same frame-snapped times."""
import json, math, subprocess, sys, os
R = json.load(open('reels.json')); FPS = R['fps']; SRC = R['source']
SW, SH = 3840, 2160
only = sys.argv[1:]

def smooth(xs, sigma):
    if sigma <= 0: return xs
    n, r = len(xs), int(sigma * 3) + 1
    ker = [math.exp(-(k * k) / (2 * sigma * sigma)) for k in range(-r, r + 1)]
    return [sum(ker[k + r] * xs[min(n - 1, max(0, i + k))] for k in range(-r, r + 1)) / sum(ker) for i in range(n)]

for name, r in R['reels'].items():
    if only and name not in only: continue
    parts, auds = [], []
    base = 0.0   # reel-local start of this segment
    for i, (a, b) in enumerate(r['segs']):
        fa, fb = round(a * FPS), round(b * FPS); n = fb - fa
        tk = json.load(open(f'src/tk/{name}_{i}.json'))
        xs = [t['x'] if t['ok'] else None for t in tk]
        last = next(x for x in xs if x is not None)
        for k in range(len(xs)):
            if xs[k] is None: xs[k] = last
            last = xs[k]
        # per-frame centre from the 4 fps samples, then smooth (heavier for steady shots)
        per = [xs[min(len(xs) - 1, int(k / FPS * 4))] for k in range(n)]
        spread = max(xs) - min(xs)
        per = smooth(per, FPS * (0.7 if spread > 0.08 else 2.0))
        if r.get('static'): per = [sum(per) / len(per)] * n
        if r['crop'] == 'tight': w, h = 1045, 1858
        else: w, h = 1215, 2160
        z = 1.10 if i % 2 == 1 else 1.0
        cw, ch = round(w / z / 2) * 2, round(h / z / 2) * 2
        y0 = round((h - ch) * 0.3)
        # optional floor on crop x for a window (keeps the edit's burned-in cards out of frame), eased over 0.4 s
        floor = [(0, 0.0)] * n
        for si, t0, t1, mx in r.get('minx', []):
            if si != i: continue
            for k in range(n):
                t = k / FPS; e = min(1, max(0, (t - t0 + 0.4) / 0.4), max(0, (t1 + 0.4 - t) / 0.4))
                floor[k] = (mx, e * e * (3 - 2 * e))
        cmd = []
        for k, cx in enumerate(per):
            x = cx * SW - cw / 2
            mx, e = floor[k]; x = x + (max(x, mx) - x) * e
            x = min(SW - cw, max(0, round(x)))
            cmd.append(f'{k / FPS:.5f} crop@track x {x};')
        os.makedirs('src/cut', exist_ok=True)
        cf = f'src/cut/{name}_{i}.cmd'; open(cf, 'w').write('\n'.join(cmd))
        x0 = int(cmd[0].split()[-1].rstrip(';'))
        vf = f"sendcmd=f={cf},crop@track={cw}:{ch}:{x0}:{y0},scale=2160:3840:flags=lanczos,unsharp=5:5:0.35"
        # widescreen "scope" windows (reel-local seconds): full 16:9 frame as a band over a blurred, darkened vertical crop
        win = [(t0 - base, t1 - base) for t0, t1 in r.get('scopes', []) if t0 < base + n / FPS and t1 > base]
        if win:
            en = '+'.join(f'between(t,{max(0, a0):.4f},{b0:.4f})' for a0, b0 in win)
            vf = (f"split[w][v];[v]{vf},split[vv][bgs];[bgs]boxblur=60:2,eq=brightness=-0.22:saturation=0.8[bg];"
                  f"[w]crop=3840:1858:0:0,scale=2160:1046:flags=lanczos[band];[bg][band]overlay=0:1150[lb];"
                  f"[vv][lb]overlay=0:0:enable='{en}'")
        v = f'src/cut/{name}_{i}.mp4'
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f'{fa / FPS:.6f}', '-i', SRC, '-frames:v', str(n), '-an',
                        '-vf', vf,
                        '-c:v', 'libx264', '-preset', 'medium', '-crf', '12', '-pix_fmt', 'yuv420p', '-r', '24000/1001', v], check=True)
        wv = f'src/cut/{name}_{i}.wav'
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f'{fa / FPS:.6f}', '-i', SRC, '-t', f'{n / FPS:.6f}', '-vn',
                        '-af', f'afade=t=in:d=0.012,afade=t=out:st={n / FPS - 0.012:.4f}:d=0.012', '-ar', '48000', '-ac', '2', wv], check=True)
        parts.append(v); auds.append(wv); base += n / FPS
        print(name, i, 'frames', n, 'crop', cw, ch, 'x', x0, 'spread %.3f' % spread, flush=True)
    lst = f'src/cut/{name}.txt'; open(lst, 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', f'assets/{name}-v.mp4'], check=True)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + sum([['-i', a] for a in auds], []) +
                   ['-filter_complex', ''.join(f'[{k}:a]' for k in range(len(auds))) + f'concat=n={len(auds)}:v=0:a=1', f'assets/{name}-dlg.wav'], check=True)
    print('done', name, flush=True)
