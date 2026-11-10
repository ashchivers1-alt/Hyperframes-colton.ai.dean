"""Stage montage: beat-cut alternating Rachel / Gabriella / Katka shots from stage-raw.mp4 (Resolve render of Ash's
trimmed stage clips). Writes montage-video.mp4 + shots.json (cut times / athlete per shot) for the overlay + audio."""
import json, subprocess, os

B = 0.37
SRC = 'stage-raw.mp4'
G = "eq=contrast=1.08:saturation=1.12:gamma=0.97,colorbalance=rs=0.03:bs=-0.03:rh=0.02,unsharp=5:5:0.5,vignette=angle=0.35"
# (athlete, source time, beats, athlete-centre-x, kind)   kind: wide = comparison line-up, solo = individual, pca = portrait
S = [('R', 1.0, 8, 560, 'wide'),
     ('R', 25.6, 8, 760, 'solo'), ('G', 41.5, 8, 980, 'solo'), ('K', 99.0, 8, 0, 'pca'),
     ('R', 29.6, 8, 920, 'solo'), ('G', 47.5, 8, 960, 'solo'), ('K', 112.0, 8, 0, 'pca'),
     ('G', 75.0, 8, 560, 'wide'), ('R', 13.0, 8, 620, 'wide'), ('K', 105.0, 8, 0, 'pca'),
     ('R', 34.6, 8, 920, 'solo'), ('G', 56.5, 8, 1080, 'solo'), ('K', 119.0, 8, 0, 'pca'),
     ('G', 61.9, 8, 540, 'wide')]
XF = 0.4   # dissolve between shots
END_BEATS = 12
os.makedirs('mt', exist_ok=True)

def punch(d):  # 1.10 -> 1.0 over first 0.22s, then slow 4% push
    return f"(1+0.035*t/{d:.3f})"

shots, t = [], 0.0
for i, (a, st, nb, cx, kind) in enumerate(S):
    d = round(nb * B + XF, 3)
    z = punch(d)
    if kind == 'pca':
        vf = (f"[0:v]fps=30,crop=604:1080:658:0,split[a][b];[a]scale=1920:3434,crop=1920:1080,gblur=sigma=40,eq=brightness=-0.12:saturation=1.2[bg];"
              f"[b]scale=w='trunc(724*{z}/2)*2':h=-2:eval=frame,crop=724:1080:(iw-724)/2:(ih-1080)/2,{G}[fg];[bg][fg]overlay=(W-w)/2:0,vignette=angle=0.4,format=yuv420p[o]")
    else:
        zoom = 1.1 if kind == 'wide' else 1.2
        w, h = int(1920 / zoom) // 2 * 2, int(1080 / zoom) // 2 * 2
        x = max(0, min(1920 - w, cx - w // 2)); y = max(0, min(1080 - h, 560 - h // 2))
        vf = (f"[0:v]fps=30,crop={w}:{h}:{x}:{y},scale=1920:1080:flags=lanczos,"
              f"scale=w='trunc(1920*{z}/2)*2':h=-2:eval=frame,crop=1920:1080,{G},format=yuv420p[o]")
    out = f'mt/{i:02d}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{st}', '-t', f'{d}', '-i', SRC, '-filter_complex', vf, '-map', '[o]',
                    '-an', '-frames:v', str(round(d * 30)), '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-r', '30', out], check=True)
    shots.append(dict(i=i, a=a, start=round(t, 3), dur=round(round(d * 30) / 30, 3), kind=kind)); t += round(d * 30) / 30 - XF

# end card: three athletes side by side
d = round((END_BEATS * B + XF) * 30) / 30
panel = lambda idx, st, cx, ystart, src_crop='': (
    f"[{idx}:v]fps=30,{src_crop}crop=474:800:{cx}-237:{ystart},scale=640:1080,{G},"
    f"scale=w='trunc(640*(1+0.05*t/{d:.3f})/2)*2':h=-2:eval=frame,crop=640:1080[p{idx}]")
fc = (panel(0, 0, 760, 140) + ';' + panel(1, 0, 980, 160) + ';' +
      "[2:v]fps=30,crop=604:1080:658:0,crop=330:556:137:300,scale=640:1080," + G +
      f",scale=w='trunc(640*(1+0.05*t/{d:.3f})/2)*2':h=-2:eval=frame,crop=640:1080[p2];[p0][p1][p2]hstack=3,format=yuv420p[o]")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '26.0', '-t', f'{d}', '-i', SRC, '-ss', '42.5', '-t', f'{d}', '-i', SRC,
                '-ss', '99.5', '-t', f'{d}', '-i', SRC, '-filter_complex', fc, '-map', '[o]', '-an', '-frames:v', str(round(d * 30)),
                '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-r', '30', f'mt/{len(S):02d}.mp4'], check=True)
shots.append(dict(i=len(S), a='END', start=round(t, 3), dur=d, kind='end')); t += d

n = len(shots); ins = []; fc = []
for k in range(n): ins += ['-i', f'mt/{k:02d}.mp4']; fc.append(f"[{k}:v]settb=1/30,setpts=PTS-STARTPTS[s{k}]")
last = 's0'
for k in range(1, n):
    fc.append(f"[{last}][s{k}]xfade=transition=fade:duration={XF}:offset={shots[k]['start']:.3f}[x{k}]"); last = f'x{k}'
open('mt/join.txt', 'w').write(';'.join(fc))
subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-/filter_complex', 'mt/join.txt', '-map', f'[{last}]', '-c:v', 'libx264', '-crf', '15',
                '-preset', 'medium', '-r', '30', '-pix_fmt', 'yuv420p', 'montage-video.mp4'], check=True)
t = shots[-1]['start'] + shots[-1]['dur']
json.dump(dict(beat=B, total=round(t, 3), shots=shots), open('shots.json', 'w'), indent=1)
print('total', round(t, 3), 'frames', round(t * 30))
