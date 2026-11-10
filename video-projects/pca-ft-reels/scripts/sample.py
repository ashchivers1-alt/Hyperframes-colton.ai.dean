import os, subprocess, sys; sys.path.insert(0, 'scripts'); from tl import *
for i in (9, 10, 11, 12):
    s, e, f, a = TL[i]; d = f'src/tk/seg{i}'; os.makedirs(d, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a / FPS:.4f}', '-t', f'{(e - s) / FPS:.4f}', '-i', f, '-vf', 'fps=4,scale=960:-2', '-q:v', '3', f'{d}/f%04d.jpg'], check=True)
    subprocess.run(['scripts/track', d, f'src/tk/seg{i}.json'], check=True)
