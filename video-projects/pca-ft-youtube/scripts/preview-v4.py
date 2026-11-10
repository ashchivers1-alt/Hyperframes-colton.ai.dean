"""1080p preview of the whole edit (proxies + B-roll + graphics + audio mix) -> renders/preview.mp4"""
import json, subprocess, os
FPS = 24000 / 1001
EDL = json.load(open('edl.json')); G = json.load(open('gfx/made.json')); BR = json.load(open('broll.json'))
T0 = EDL[0]['rec'] / FPS; TEND = (EDL[-1]['rec'] + EDL[-1]['dur']) / FPS
L3 = '/Volumes/Untitled/DCIM/DJI_001/DJI_20261101150314_0003_D.LRF'
# training dialogue: real audio for 'av' pieces, silence for 'mus'
parts = []
for i, p in enumerate(EDL):
    o = f'src/pp/a{i:02d}.wav'; d = p['dur'] / FPS
    if p['mode'] == 'mus':
        subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-t',f'{d:.5f}',o], check=True)
    else:
        subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-ss',f"{p['src_start'] / FPS:.5f}",'-t',f'{d:.5f}','-i',f"src/lrf/{p['clip']}.mp4",'-vn','-ar','48000','-ac','2',
                        '-af',f'afade=t=in:d=0.03,afade=t=out:st={d - 0.05:.4f}:d=0.05',o], check=True)
    parts.append(f"file '{os.path.abspath(o)}'")
open('src/pp/alist.txt','w').write('\n'.join(parts))
subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-f','concat','-safe','0','-i','src/pp/alist.txt','-c','pcm_s16le','src/pp/train-dlg.wav'], check=True)
# video base: intro proxy + training proxy
subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i','renders/intro-proxy-cut.mp4','-i','renders/train-proxy.mp4','-filter_complex',
                '[0:v]fps=24000/1001,setsar=1[a];[1:v]fps=24000/1001,setsar=1[b];[a][b]concat=n=2:v=1:a=0[v]','-map','[v]','-c:v','libx264','-preset','veryfast','-crf','20','src/pp/base.mp4'], check=True)
ins = ['-i','src/pp/base.mp4']; fc = ['[0:v]scale=1920:1080,setsar=1[v0]']; cur = 'v0'; n = 1
for b in BR:
    ins += ['-ss', f"{b['src'] / FPS:.4f}", '-t', f"{b['dur'] / FPS:.4f}", '-i', L3]
    fc.append(f"[{n}:v]scale=1920:1080,setpts=PTS-STARTPTS+{b['rec_s']:.4f}/TB[b{n}]")
    fc.append(f"[{cur}][b{n}]overlay=enable='between(t,{b['rec_s']:.3f},{b['rec_s'] + b['dur'] / FPS:.3f})':eof_action=pass[v{n}]"); cur = f'v{n}'; n += 1
for g in G:
    f = f"gfx/out1/{g['name']}.mov"
    if not os.path.exists(f): continue
    t = g['rec'] / FPS
    ins += ['-i', f]; fc.append(f"[{n}:v]setpts=PTS-STARTPTS+{t:.4f}/TB[g{n}]")
    fc.append(f"[{cur}][g{n}]overlay=eof_action=pass[v{n}]"); cur = f'v{n}'; n += 1
a = n
ins += ['-i','src/aud/intro-cut.wav','-i','src/pp/train-dlg.wav','-i','audio/bed_intro.wav','-i','audio/bed_train.wav']
fc.append(f"[{a}:a]aresample=48000,aformat=channel_layouts=stereo,volume=3dB[d1];[{a + 1}:a]adelay={int(T0 * 1000)}|{int(T0 * 1000)}[d2];"
          f"[{a + 3}:a]adelay={int(T0 * 1000)}|{int(T0 * 1000)}[b2];[d1][d2][{a + 2}:a][b2]amix=inputs=4:normalize=0,atrim=0:{TEND:.3f}[aout]")
subprocess.run(['ffmpeg','-nostdin','-v','error','-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', f'[{cur}]', '-map', '[aout]',
                '-t', f'{TEND:.3f}', '-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','renders/preview.mp4'], check=True)
print('preview', TEND)
