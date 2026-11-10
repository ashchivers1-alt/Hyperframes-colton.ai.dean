"""Cut each reel from Ash's source clips (via the Resolve timeline map), 2160x3840.
wide = whole 16:9 frame as a band (y 940) over a blurred, darkened 9:16 crop; ash/legs = 9:16 crop following Ash.
usage: cut.py [reel...]"""
import json, math, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__)); from tl import *
R = json.load(open('reels.json'))['reels']; SW, SH = 3840, 2160
BAND_Y = 940
only = sys.argv[1:]

def smooth(xs, sigma):
    n, r = len(xs), int(sigma * 3) + 1
    ker = [math.exp(-(k * k) / (2 * sigma * sigma)) for k in range(-r, r + 1)]
    return [sum(ker[k + r] * xs[min(n - 1, max(0, i + k))] for k in range(-r, r + 1)) / sum(ker) for i in range(n)]

def ash_track(seg, side):
    """per-sample (x, faceY) of Ash in timeline segment `seg`; side = left|right picks him out of the two people"""
    pick = min if side == 'left' else max
    out, last = [], None
    for s in json.load(open(f'src/tk/seg{seg}.json')):
        if s['faces']: f = pick(s['faces'], key=lambda v: v[0]); last = (f[0], f[1])
        elif s['bodies']: b = pick(s['bodies'], key=lambda v: v[0]); last = (b[0], (last or (0, b[1] + 0.06))[1])
        out.append(last)
    first = next(v for v in out if v)
    return [v or first for v in out]

for name, r in R.items():
    if only and name not in only: continue
    parts, auds = [], []
    os.makedirs('src/cut', exist_ok=True)
    pi = 0
    for si, sg in enumerate(r['segs']):
        t0, t1, mode = sg[0], sg[1], sg[2]; z = sg[3] if len(sg) > 3 else 1.0
        for f, a, n, tf in split(t0, t1):
            seg = seg_of(tf); s0 = TL[seg][0]
            tk = ash_track(seg, r['pick'][str(seg)])
            k0 = tf - s0                      # frame offset into the timeline segment
            xs = [tk[min(len(tk) - 1, int((k0 + k) / FPS * 4))][0] for k in range(-24, n + 24)]
            ys = [tk[min(len(tk) - 1, int((k0 + k) / FPS * 4))][1] for k in range(-24, n + 24)]
            xs = smooth(xs, FPS * 0.8)[24:24 + n]; fy = sum(ys) / len(ys)
            cw, ch = round(1215 / z / 2) * 2, round(2160 / z / 2) * 2
            if mode == 'legs': y0 = (2160 - ch) // 2
            else: y0 = int(min(2160 - ch, max(0, fy * 2160 - 0.16 * ch)))
            cmd = []
            for k, cx in enumerate(xs):
                x = min(SW - cw, max(0, round(cx * SW - cw / 2)))
                cmd.append(f'{k / FPS:.5f} crop@track x {x};')
            cf = f'src/cut/{name}_{pi}.cmd'; open(cf, 'w').write('\n'.join(cmd))
            x0 = int(cmd[0].split()[-1].rstrip(';'))
            vf = f"sendcmd=f={cf},crop@track={cw}:{ch}:{x0}:{y0},scale=2160:3840:flags=lanczos,unsharp=5:5:0.3"
            if mode == 'wide':
                vf = (f"movie=src/widebg.png,loop=-1:1,setpts=N/FRAME_RATE/TB[bg];"
                      f"[0:v]scale=2160:1215:flags=lanczos,unsharp=5:5:0.3[band];[bg][band]overlay=0:{BAND_Y}:shortest=1")
            vf += ',eq=contrast=1.05:saturation=1.08'
            v = f'src/cut/{name}_{pi}.mp4'
            subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f'{a / FPS:.6f}', '-i', f, '-frames:v', str(n), '-an',
                            '-filter_complex', vf, '-c:v', 'libx264', '-preset', 'medium', '-crf', '12', '-pix_fmt', 'yuv420p', '-r', '24000/1001', v], check=True)
            wv = f'src/cut/{name}_{pi}.wav'
            subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f'{a / FPS:.6f}', '-i', f, '-t', f'{n / FPS:.6f}', '-vn',
                            '-af', f'afade=t=in:d=0.015,afade=t=out:st={n / FPS - 0.015:.4f}:d=0.015', '-ar', '48000', '-ac', '2', wv], check=True)
            parts.append(v); auds.append(wv); pi += 1
            print(name, si, mode, 'frames', n, 'crop', cw, ch, x0, y0, flush=True)
    lst = f'src/cut/{name}.txt'; open(lst, 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', f'src/{name}-v.mp4'], check=True)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + sum([['-i', a] for a in auds], []) +
                   ['-filter_complex', ''.join(f'[{k}:a]' for k in range(len(auds))) + f'concat=n={len(auds)}:v=0:a=1', f'src/{name}-dlg.wav'], check=True)
    print('done', name, flush=True)
