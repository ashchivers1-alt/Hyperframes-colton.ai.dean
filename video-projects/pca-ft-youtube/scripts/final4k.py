"""4K master (3840x2160, 23.976) straight from the camera originals -> ~/Documents/Claude Video - Completed/pca-ft-youtube.mp4
Same edit as the approved preview (preview.py + show_preview.py): teaser, posing (Edit 02 V1), gym clip, training (edl.json),
show day (show_edl.json), Team Apexx outro. Graphics = gfx/out4k. Audio = the preview mix, kept as PCM until the final AAC encode.
Sections are cached in renders/4k/ (delete a file to rebuild it).  usage: python3 scripts/final4k.py"""
import json, subprocess, os
FPS = 24000 / 1001; W, H = 3840, 2160; OUT = 'renders/4k/'; os.makedirs(OUT + 'seg', exist_ok=True)
P = json.load(open('src/resolve_probe.json')); EDL = json.load(open('edl.json')); X = json.load(open('show_edl.json'))
G = json.load(open('gfx/made.json')); GS = json.load(open('gfx/made_show.json')); BR = json.load(open('broll.json'))
GYM = json.load(open('gym.json')); TZ = json.load(open('show/teaser/teaser.json'))
PATH = {it['media_pool_item_id']: it['file_path'] for tr in P['tracks']['video']['tracks'] for it in tr['items']}
POSE = [it for it in P['tracks']['video']['tracks'][0]['items'] if it['end'] - 86400 <= GYM['rec']]
DJI = '/Volumes/Untitled/DCIM/DJI_001/'; L3 = DJI + 'DJI_20261101150314_0003_D.MP4'
T0 = EDL[0]['rec'] / FPS; TG = GYM['rec'] / FPS; TEND = (EDL[-1]['rec'] + EDL[-1]['dur']) / FPS
S0 = X['start'] / FPS; SD = (X['end'] - X['start']) / FPS
INT = ['-c:v', 'libx264', '-preset', 'fast', '-crf', '12', '-pix_fmt', 'yuv420p']          # intermediates: near-lossless
FIT = f'scale={W}:{H}:flags=lanczos,setsar=1'
def run(a): subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + a, check=True)
def have(f): return os.path.exists(f) and os.path.getsize(f) > 0
def piece(o, f, a, n, vf='', speed=1.0):
    """n frames of file f from source second a, conformed to 4K 23.976"""
    if have(o): return o
    if speed == 1: v = f'fps=24000/1001,{FIT}'
    else: v = f'tmix=frames={int(speed)},setpts=(PTS-STARTPTS)/{speed},fps=24000/1001,{FIT}'
    run(['-ss', f'{a:.5f}', '-t', f'{n / FPS * speed + 0.5:.5f}', '-i', f, '-vf', v + vf, '-frames:v', str(n), '-an'] + INT + [o])
    return o
def concat(files, o):
    open(o + '.txt', 'w').write('\n'.join(f"file '{os.path.abspath(f)}'" for f in files))
    run(['-f', 'concat', '-safe', '0', '-i', o + '.txt', '-c', 'copy', o])
def vertical(src, o, d, a=0.0):
    """vertical clip over a blurred, darkened copy of itself"""
    if have(o): return
    run(['-ss', f'{a:.4f}', '-t', f'{d + 0.3:.4f}', '-i', src, '-filter_complex',
         f'[0:v]fps=24000/1001,split[a][b];[a]scale={W}:-2,crop={W}:{H},gblur=sigma=80,eq=brightness=-0.12:saturation=0.85[bg];'
         f'[b]scale=-2:{H}:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:0,setsar=1[o]', '-map', '[o]', '-frames:v', str(round(d * FPS)), '-an'] + INT + [o])
def composite(base, lays, gfx, t_off, dur, o):
    """base + full-frame video overlays [(file, src_in, dur, t)] + gfx comps [(name, t)] -> o"""
    if have(o): return
    ins = ['-i', base]; fc = ['[0:v]setsar=1[v0]']; cur = 'v0'; n = 1
    for f, si, d, t in lays:
        ins += ['-ss', f'{si:.4f}', '-t', f'{d:.4f}', '-i', f]
        fc.append(f'[{n}:v]fps=24000/1001,{FIT},setpts=PTS-STARTPTS+{t:.4f}/TB[b{n}]')
        fc.append(f"[{cur}][b{n}]overlay=enable='between(t,{t:.3f},{t + d:.3f})':eof_action=pass[v{n}]"); cur = f'v{n}'; n += 1
    for name, t in gfx:
        f = f'gfx/out4k/{name}.mov'
        if not os.path.exists(f): raise SystemExit('missing 4K graphic ' + f)
        ins += ['-i', f]; fc.append(f'[{n}:v]setpts=PTS-STARTPTS+{t - t_off:.4f}/TB[g{n}]')
        fc.append(f'[{cur}][g{n}]overlay=eof_action=pass[v{n}]'); cur = f'v{n}'; n += 1
    run(ins + ['-filter_complex', ';'.join(fc), '-map', f'[{cur}]', '-t', f'{dur:.4f}'] + INT + [o]); print('composited', o)

# ---------------------------------------------------------------- posing + gym + training
segs = [piece(f'{OUT}seg/p{i:02d}.mp4', it['file_path'], it['source_start_seconds'], it['end'] - it['start']) for i, it in enumerate(POSE)]
vertical(GYM['file'], f'{OUT}seg/gym.mp4', GYM['frames'] / FPS, GYM['src_in']); segs.append(f'{OUT}seg/gym.mp4')
segs += [piece(f'{OUT}seg/t{i:02d}.mp4', PATH[p['mpid']], p['src_start'] / FPS, p['dur']) for i, p in enumerate(EDL)]
if not have(OUT + 'main_base.mp4'): concat(segs, OUT + 'main_base.mp4')
composite(OUT + 'main_base.mp4', [(L3, b['src'] / FPS, b['dur'] / FPS, b['rec_s']) for b in BR],
          [(g['name'], g['rec'] / FPS) for g in G], 0.0, TEND, OUT + 'main.mp4')

# ---------------------------------------------------------------- show day
segs = [piece(f'{OUT}seg/s{i}.mp4', s['file'], s['src_start'], s['frames'], speed=s['speed']) for i, s in enumerate(X['segs'])]
if not have(OUT + 'show_base.mp4'): concat(segs, OUT + 'show_base.mp4')
a, b = X['designed']['x_vertical']; vertical('show/px/8934_vert_src.mp4', OUT + 'seg/x_vertical.mp4', b - a)
lays = [(r['file'], r['src_in'], r['src_out'] - r['src_in'], r['t'] - S0) for r in X['broll']] + [(OUT + 'seg/x_vertical.mp4', 0, b - a, a - S0)]
composite(OUT + 'show_base.mp4', lays, [(g['name'], g['rec'] / FPS) for g in GS if g['rec'] >= X['start']], S0, SD, OUT + 'show.mp4')

# ---------------------------------------------------------------- teaser + outro
if not have('show/teaser/teaser_2160.mp4'): subprocess.run(['python3', 'scripts/teaser.py', '2160'], check=True)
composite('show/teaser/teaser_2160.mp4', [], [('i_teaser', 0.0)], 0.0, TZ['dur'], OUT + 'teaser.mp4')
if not have(OUT + 'outro.mp4'):
    run(['-ss', '1.0', '-t', '7.87', '-i', os.path.expanduser('~/Downloads/APEX.MP4'), '-vf', f'fps=24000/1001,{FIT}', '-an'] + INT + [OUT + 'outro.mp4'])

# ---------------------------------------------------------------- audio: the approved preview mix, PCM
if not have(OUT + 'mix.wav'):
    run(['-i', 'src/aud/intro-cut.wav', '-i', 'src/pp/train-dlg.wav', '-i', 'audio/bed_intro.wav', '-i', 'audio/bed_train.wav', '-filter_complex',
         f"[0:a]aresample=48000,aformat=channel_layouts=stereo,volume=3dB[d1];[1:a]adelay={int(T0 * 1000)}|{int(T0 * 1000)}[d2];"
         f"[3:a]adelay={int(TG * 1000)}|{int(TG * 1000)}[b2];[d1][d2][2:a][b2]amix=inputs=4:normalize=0,atrim=0:{TEND:.4f},apad,atrim=0:{TEND:.4f}[o]",
         '-map', '[o]', '-ar', '48000', '-c:a', 'pcm_s24le', OUT + 'a_main.wav'])
    run(['-i', 'show/pp/dlg.wav', '-i', 'audio/bed_show.wav', '-filter_complex', f'[0:a][1:a]amix=inputs=2:normalize=0,apad,atrim=0:{SD:.4f}[o]',
         '-map', '[o]', '-ar', '48000', '-c:a', 'pcm_s24le', OUT + 'a_show.wav'])
    run(['-i', 'audio/teaser.wav', '-af', f'aformat=sample_rates=48000:channel_layouts=stereo,apad,atrim=0:{TZ["dur"]:.4f}', '-c:a', 'pcm_s24le', OUT + 'a_teaser.wav'])
    run(['-i', '../training-day/v7/outro-sfx.wav', '-af', 'aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:7.87', '-c:a', 'pcm_s24le', OUT + 'a_outro.wav'])
    run(['-i', OUT + 'a_teaser.wav', '-i', OUT + 'a_main.wav', '-i', OUT + 'a_show.wav', '-i', OUT + 'a_outro.wav', '-filter_complex',
         '[0:a][1:a][2:a][3:a]concat=n=4:v=0:a=1[o]', '-map', '[o]', '-c:a', 'pcm_s24le', OUT + 'mix.wav'])

# ---------------------------------------------------------------- master: concat + the training->show wipe on the join
DEST = os.path.expanduser('~/Documents/Claude Video - Completed/'); dst = DEST + 'pca-ft-youtube.mp4'; k = 2
while os.path.exists(dst): dst = DEST + f'pca-ft-youtube-v{k}.mp4'; k += 1
J = next(g for g in GS if g['name'] == 'w1_showday')
concat([OUT + 'teaser.mp4', OUT + 'main.mp4', OUT + 'show.mp4', OUT + 'outro.mp4'], OUT + 'video.mp4')
run(['-i', OUT + 'video.mp4', '-i', f"gfx/out4k/{J['name']}.mov", '-i', OUT + 'mix.wav', '-filter_complex',
     f"[1:v]setpts=PTS-STARTPTS+{TZ['dur'] + J['rec'] / FPS:.4f}/TB[w];[0:v][w]overlay=eof_action=pass,format=yuv420p[v]",
     '-map', '[v]', '-map', '2:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-profile:v', 'high', '-tag:v', 'avc1',
     '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', dst])
print('MASTER', dst)
