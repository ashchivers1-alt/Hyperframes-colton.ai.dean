"""Encode each unit to a 1080p30 intermediate, then join with dissolves (xfade).
Sources are only read. Output: out/reel-video.mp4 (no audio)."""
import json, subprocess, glob, os, sys

U = json.load(open('units.json'))
units, XF = U['units'], U['xf']
D = '/Volumes/Untitled/DCIM/DJI_001/'
SRC = {'SLOWEXT': '../assets/slowmo-exterior.mp4'}
def src(c):
    return SRC.get(c) or glob.glob(D + f'DJI_*_{c[1:]}_D.MP4')[0]

GRADE = "eq=contrast=1.06:saturation=1.08:gamma=0.98,vignette=angle=0.32"
os.makedirs('out/u', exist_ok=True)

def zoomf(z):
    if z <= 1.0: return ""
    return f",crop=iw/{z}:ih/{z}:(iw-iw/{z})*0.47:(ih-ih/{z})*0.38,scale=1920:1080"

for i, u in enumerate(units):
    out = f'out/u/{i:02d}.mp4'
    if os.path.exists(out) and '--force' not in sys.argv: continue
    parts, filt = [], []
    for j, (a, b) in enumerate(u['pieces']):
        z = u.get('zoom', 1.0)
        if len(u['pieces']) > 1: z = 1.0 if j % 2 == 0 else 1.1      # alternate punch-in hides jump cuts
        parts += ['-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', src(u['clip'])]
        filt.append(f"[{j}:v]scale=1920:1080:flags=lanczos,fps=30{zoomf(z)},{GRADE},setsar=1,format=yuv420p[v{j}]")
    n = len(u['pieces'])
    fc = ';'.join(filt) + ';' + ''.join(f'[v{j}]' for j in range(n)) + f'concat=n={n}:v=1:a=0[o]'
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-hwaccel', 'videotoolbox', *parts, '-filter_complex', fc, '-map', '[o]',
           '-t', f"{u['dur']:.3f}", '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '14', '-r', '30', out]
    subprocess.run(cmd, check=True)
    print(i, u['tag'], 'ok', flush=True)

# --- join with dissolves ---
inputs, fc, last, acc = [], [], '0:v', None
for i, u in enumerate(units):
    inputs += ['-i', f'out/u/{i:02d}.mp4']
for i, u in enumerate(units):
    fc.append(f"[{i}:v]fps=30,settb=1/30,setpts=PTS-STARTPTS[s{i}]")
last = 's0'
for i, u in enumerate(units):
    if i == 0:
        acc = u['dur']; continue
    xf = u['xf_in']
    lab = f'x{i}'
    if xf > 0:
        fc.append(f"[{last}][s{i}]xfade=transition=fade:duration={xf:.3f}:offset={acc - xf:.3f}[{lab}]")
        acc += u['dur'] - xf
    else:
        fc.append(f"[{last}][s{i}]concat=n=2:v=1:a=0,settb=1/30[{lab}]")
        acc += u['dur']
    last = lab
open('out/join.txt', 'w').write(';'.join(fc))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *inputs, '-/filter_complex', 'out/join.txt', '-map', f'[{last}]',
                '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', '-r', '30', '-movflags', '+faststart',
                'out/reel-video-e.mp4'], check=True)
print('joined, expected', round(acc, 3), 'planned', U['total'])
