"""1080p preview of the show-day section -> renders/show-preview.mp4, then renders/preview-full.mp4 (posing + training + show).
Also writes audio/bed_show.wav (music bed + SFX for the show section, starts at the section's first frame)."""
import json, subprocess, os
FPS = 24000 / 1001
X = json.load(open('show_edl.json')); G = json.load(open('gfx/made_show.json'))
S0 = X['start'] / FPS; D = (X['end'] - X['start']) / FPS
DJI = '/Volumes/Untitled/DCIM/DJI_001/'
LRF = {'c15': DJI + 'DJI_20261108093859_0015_D.LRF', 'c16': DJI + 'DJI_20261108094057_0016_D.LRF', 'c17': DJI + 'DJI_20261108162434_0017_D.LRF',
       'c01': 'show/IMG_3801_rt.mov'}
MUS = '../npc-italy/src/music/kulakovka-hip-hop-power-614899.mp3'; SFX = '../../assets/sfx/'
run = lambda a: subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + a, check=True)
os.makedirs('show/pp', exist_ok=True)

# talking / driving base: video + dialogue (drive = road noise, low)
vl, al = [], []
for i, s in enumerate(X['segs']):
    d = s['frames'] / FPS; a = s['src_start']; ov, oa = f'show/pp/v{i}.mp4', f'show/pp/a{i}.wav'
    if s['speed'] == 1:
        vf = 'scale=1920:1080,setsar=1,fps=24000/1001'
        run(['-ss', f'{a:.4f}', '-t', f'{d:.4f}', '-i', LRF[s['clip']], '-vf', vf, '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', ov])
        asrc = f"show/dn/{s['clip']}_voice.wav"   # cleaned + level-matched dialogue (-18 LUFS); c15 also has the road rumble taken out
        run(['-ss', f'{a:.4f}', '-t', f'{d:.4f}', '-i', asrc, '-vn', '-ar', '48000', '-ac', '2', '-af', f'afade=t=in:d=0.03,afade=t=out:st={d - 0.05:.4f}:d=0.05', oa])
    else:   # sped up: blend 3 frames per output frame for motion blur
        sp = s['speed']
        vf = f'tmix=frames={int(sp)},setpts=(PTS-STARTPTS)/{sp},fps=24000/1001,scale=1920:1080,setsar=1'
        run(['-ss', f'{a:.4f}', '-t', f'{d * sp:.4f}', '-i', LRF[s['clip']], '-vf', vf, '-an', '-t', f'{d:.4f}', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', ov])
        run(['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-t', f'{d:.4f}', oa])
    vl.append(f"file '{os.path.abspath(ov)}'"); al.append(f"file '{os.path.abspath(oa)}'")
open('show/pp/vlist.txt', 'w').write('\n'.join(vl)); open('show/pp/alist.txt', 'w').write('\n'.join(al))
run(['-f', 'concat', '-safe', '0', '-i', 'show/pp/vlist.txt', '-c', 'copy', 'show/pp/base.mp4'])
run(['-f', 'concat', '-safe', '0', '-i', 'show/pp/alist.txt', '-c', 'pcm_s16le', 'show/pp/dlg.wav'])

# vertical backstage clip, full screen with a blurred fill (also used as-is in Resolve, 4K version made at final)
a, b = X['designed']['x_vertical']
run(['-i', 'show/px/8934_vert_src.mp4', '-filter_complex',
     '[0:v]split[a][b];[a]scale=1920:-2,crop=1920:1080,gblur=sigma=40,eq=brightness=-0.12:saturation=0.8[bg];[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0,setsar=1[o]',
     '-map', '[o]', '-t', f'{b - a:.4f}', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', 'show/px/x_vertical.mp4'])

# music bed (Kulakovka 'Hip-Hop Power', not Content ID registered): low under talk, up on the motorway, fade at the end
drive = X['segs'][1]; da, db = drive['rec'] / FPS - S0, (drive['rec'] + drive['frames']) / FPS - S0
LOW, HIGH = -27.0, -12.0
pts = [(0, LOW), (da - 0.6, LOW), (da + 0.2, HIGH), (db - 0.3, HIGH), (db + 0.6, LOW), (D, LOW)]
def env(pts):
    e = '0'
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        e = f"if(between(t,{t0:.3f},{t1:.3f}),{v0}+({v1}-({v0}))*(t-{t0:.3f})/{t1 - t0:.3f},{e})"
    return e
sfx = []
for g in G:
    t = max(0.0, g['rec'] / FPS - S0)
    if g['name'].startswith('w'): sfx.append(('transitions/whoosh.mp3', t + 0.05, -10))
    elif g['name'].startswith('x'): sfx.append(('transitions/whoosh.mp3', t, -16))
    elif g['name'] != 's22_outro': sfx.append(('ui/pop.mp3', t + 0.1, -18))
ins = ['-stream_loop', '-1', '-i', MUS]
fc = [f"[0:a]atrim=0:{D:.3f},afade=t=in:d=1.0,afade=t=out:st={D - 4:.3f}:d=4,volume='pow(10,({env(pts)})/20)':eval=frame[bed]"]
for i, (f, t, db_) in enumerate(sfx):
    ins += ['-i', SFX + f]; fc.append(f'[{i + 1}:a]volume={db_}dB,adelay={int(t * 1000)}|{int(t * 1000)}[s{i}]')
fc.append('[bed]' + ''.join(f'[s{i}]' for i in range(len(sfx))) + f'amix=inputs={len(sfx) + 1}:normalize=0,atrim=0:{D:.3f},aformat=sample_rates=48000:channel_layouts=stereo[out]')
run(ins + ['-filter_complex', ';'.join(fc), '-map', '[out]', '-c:a', 'pcm_s24le', 'audio/bed_show.wav'])

# composite: base + full-screen B-roll + vertical + graphics/designed comps; dialogue + bed
ins = ['-i', 'show/pp/base.mp4']; fc = ['[0:v]setsar=1[v0]']; cur = 'v0'; n = 1
lays = [(b['file'], b['src_in'], b['src_out'] - b['src_in'], b['t'] - S0) for b in X['broll']] + [('show/px/x_vertical.mp4', 0, b - a, a - S0)]
for f, si, d, t in lays:
    ins += ['-ss', f'{si:.4f}', '-t', f'{d:.4f}', '-i', f]
    fc.append(f'[{n}:v]fps=24000/1001,scale=1920:1080,setsar=1,setpts=PTS-STARTPTS+{t:.4f}/TB[b{n}]')
    fc.append(f"[{cur}][b{n}]overlay=enable='between(t,{t:.3f},{t + d:.3f})':eof_action=pass[v{n}]"); cur = f'v{n}'; n += 1
for g in G:
    f = f"gfx/out1/{g['name']}.mov"
    if g['rec'] < X['start']: continue            # straddles the training -> show cut: overlaid on the whole-video join below
    if not os.path.exists(f): print('missing', f); continue
    ins += ['-i', f]; fc.append(f"[{n}:v]setpts=PTS-STARTPTS+{g['rec'] / FPS - S0:.4f}/TB[g{n}]")
    fc.append(f"[{cur}][g{n}]overlay=eof_action=pass[v{n}]"); cur = f'v{n}'; n += 1
ins += ['-i', 'show/pp/dlg.wav', '-i', 'audio/bed_show.wav']
fc.append(f'[{n}:a][{n + 1}:a]amix=inputs=2:normalize=0,atrim=0:{D:.3f}[aout]')
run(ins + ['-filter_complex', ';'.join(fc), '-map', f'[{cur}]', '-map', '[aout]', '-t', f'{D:.3f}',
           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', 'renders/show-preview.mp4'])
# whole video: previous preview (posing + training) + show
J = next(g for g in G if g['name'] == 'w1_showday')
# cold-open teaser (shots + letterbox/flash/title comp + its own audio) and the Team Apexx sting as the outro
TZ = json.load(open('show/teaser/teaser.json'))
run(['-i', 'show/teaser/teaser_1080.mp4', '-i', 'gfx/out1/i_teaser.mov', '-i', 'audio/teaser.wav', '-filter_complex', '[0:v][1:v]overlay=eof_action=pass[v]',
     '-map', '[v]', '-map', '2:a', '-t', f"{TZ['dur']:.3f}", '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', 'show/pp/teaser.mov'])
run(['-ss', '1.0', '-t', '7.87', '-i', os.path.expanduser('~/Downloads/APEX.MP4'), '-i', '../training-day/v7/outro-sfx.wav', '-filter_complex',
     '[0:v]fps=24000/1001,scale=1920:1080,setsar=1[v];[1:a]aresample=48000,apad,atrim=0:7.87[a]', '-map', '[v]', '-map', '[a]',
     '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', 'show/pp/outro.mov'])
run(['-i', 'show/pp/teaser.mov', '-i', 'renders/preview.mp4', '-i', 'renders/show-preview.mp4', '-i', 'show/pp/outro.mov', '-i', f"gfx/out1/{J['name']}.mov", '-filter_complex',
     f"[0:v]setsar=1[t];[1:v]setsar=1[p];[2:v]setsar=1[s];[3:v]setsar=1[o];[0:a]aformat=sample_rates=48000:channel_layouts=stereo[ta];[1:a]aformat=sample_rates=48000:channel_layouts=stereo[pa];"
     f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo[sa];[3:a]aformat=sample_rates=48000:channel_layouts=stereo[oa];"
     f"[t][ta][p][pa][s][sa][o][oa]concat=n=4:v=1:a=1[c][a];[4:v]setpts=PTS-STARTPTS+{TZ['dur'] + J['rec'] / FPS:.4f}/TB[w];[c][w]overlay=eof_action=pass[v]",
     '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', 'renders/preview-full.mp4'])
print('show preview', round(D, 2), 's')
