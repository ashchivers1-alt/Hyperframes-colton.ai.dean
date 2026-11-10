"""Apply intro.json cuts to the posing-section proxy + audio -> renders/intro-proxy-cut.mp4, src/aud/intro-cut.wav"""
import json, subprocess
FPS = 24000 / 1001; I = json.load(open('intro.json'))
keep, a = [], 0
for s, e, _ in I['cuts']: keep.append((a, s)); a = e
keep.append((a, I['length']))
sel = '+'.join(f'between(n,{s},{e - 1})' for s, e in keep)
asel = '+'.join(f'between(t,{s / FPS:.5f},{(e - 0.5) / FPS:.5f})' for s, e in keep)
subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i','renders/intro-proxy.mp4','-an','-vf',f"fps=24000/1001,select='{sel}',setpts=N/(24000/1001)/TB,tpad=stop_mode=clone:stop=12",'-frames:v',str(I['length'] - sum(e - s for s, e, _ in I['cuts'])),
                '-c:v','libx264','-preset','veryfast','-crf','20','renders/intro-proxy-cut.mp4'], check=True)
# audio: concat kept ranges with 10ms crossfade-free micro fades
parts = []
for i, (s, e) in enumerate(keep):
    o = f'src/aud/intro-k{i}.wav'; d = (e - s) / FPS
    subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-ss',f'{s / FPS:.5f}','-t',f'{d:.5f}','-i','src/aud/intro.wav','-ar','48000','-ac','2',
                    '-af',f'afade=t=in:d=0.012,afade=t=out:st={d - 0.012:.5f}:d=0.012',o], check=True); parts.append(o)
subprocess.run(['ffmpeg','-nostdin','-v','error','-y'] + sum([['-i', p] for p in parts], []) +
               ['-filter_complex', ''.join(f'[{i}:a]' for i in range(len(parts))) + f'concat=n={len(parts)}:v=0:a=1[a]', '-map','[a]','src/aud/intro-cut.wav'], check=True)
print('kept', keep)
