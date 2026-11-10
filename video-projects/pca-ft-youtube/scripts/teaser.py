"""Cinematic cold-open teaser (plays before the video) -> show/teaser/teaser_<res>.mp4 + audio/teaser.wav.
Shots come straight from the source files (4K for the final, scaled for the preview), graded with the Apexx cine LUT,
slow push-in on every shot; letterbox / flashes / title are the gfx comp i_teaser (gfx/show.py) laid on top.
usage: python3 scripts/teaser.py [1080|2160]"""
import json, subprocess, os, sys
FPS = 24000 / 1001
RES = int(sys.argv[1]) if len(sys.argv) > 1 else 1080; W, H = RES * 16 // 9, RES
LUT = '../training-day/grade/apexx_cine_punch.cube'
P = json.load(open(sys.argv[2] if len(sys.argv) > 2 else 'src/resolve_probe.json'))
EDL = json.load(open('edl.json')); X = json.load(open('show_edl.json'))
PATH = {it['media_pool_item_id']: it['file_path'] for tr in P['tracks']['video']['tracks'] for it in tr['items']}
POSE = [it for it in P['tracks']['video']['tracks'][0]['items'] if it['start'] - 86400 < X['segs'][0]['rec'] and it['start'] - 86400 < EDL[0]['rec']]

def full(t):
    """whole-video timeline seconds (posing + training) -> (source file, source seconds)"""
    f = t * FPS
    if f < EDL[0]['rec']:
        it = next(i for i in POSE if i['start'] - 86400 <= f < i['end'] - 86400)
        return it['file_path'], it['source_start_seconds'] + (f - (it['start'] - 86400)) / FPS
    p = next(p for p in EDL if p['rec'] <= f < p['rec'] + p['dur'])
    return PATH[p['mpid']], (p['src_start'] + f - p['rec']) / FPS

C15, C16, C17 = (s['file'] for s in X['segs'][:3])
SD = 'show/sdr/'
M = 0.85                                      # montage shot length
# (file, src_in, out_dur, speed, kind)   kind: h = landscape, v = vertical with blurred fill
SHOTS = [(C16, 20.0, 2.0, 3.0, 'h'), (C15, 2.0, 2.4, 1.0, 'h')]
SHOTS += [(*full(t), M, 1.0, 'h') for t in (45, 95, 200)]
SHOTS += [(*full(t), M, 1.0, 'h') for t in (289, 404, 464, 524)]    # (+4 s: gym exterior clip now sits before the training)
SHOTS += [(SD + 'IMG_8934.mov', 80.5, M, 1.0, 'v'), (SD + 'IMG_3767.mov', 24.0, M, 1.0, 'h'), (SD + 'IMG_3784.mov', 28.0, M, 1.0, 'h'),
          (*full(190), M, 1.0, 'h'), (SD + 'IMG_3768.mov', 23.0, M, 1.0, 'h'), (SD + 'IMG_3768.mov', 52.6, 3.8, 0.5, 'h')]
VOICE = [(0.0, 'show/dn/c15_voice.wav', 0.0, 4.4), (None, 'show/dn/c17_voice.wav', 66.2, 3.8)]   # (teaser t | None = with the slow-mo shot, file, src_in, dur)
TITLE = 3.2                                    # black title card after the last shot

def run(a): subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + a, check=True)
os.makedirs('show/teaser', exist_ok=True)
L, t, cuts = [], 0.0, []
for i, (f, a, d, sp, kind) in enumerate(SHOTS):
    o = f'show/teaser/s{i:02d}_{RES}.mp4'; n = round(d * FPS); d = n / FPS
    push = f"scale={W * 1.08:.0f}:{H * 1.08:.0f},crop={W}:{H}:(iw-{W})/2*(1-t/{d:.3f}*0.6):(ih-{H})/2*(1-t/{d:.3f}*0.6)"
    pre = (f'tmix=frames={int(sp)},' if sp > 1 else '') + f'setpts=(PTS-STARTPTS)/{sp},fps=24000/1001'
    if sp < 1: pre = f'setpts=(PTS-STARTPTS)/{sp},minterpolate=fps=24000/1001:mi_mode=blend'
    if kind == 'v':
        vf = (f'{pre},split[a][b];[a]scale={W}:-2,crop={W}:{H},gblur=sigma={RES // 27},eq=brightness=-0.12[bg];'
              f'[b]scale=-2:{H}[fg];[bg][fg]overlay=(W-w)/2:0,lut3d={LUT},{push}')
    else:
        vf = f'{pre},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},lut3d={LUT},{push}'
    run(['-ss', f'{a:.4f}', '-t', f'{d * sp + 0.3:.4f}', '-i', f, '-filter_complex', f'[0:v]{vf},setsar=1[o]', '-map', '[o]', '-frames:v', str(n),
         '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14' if RES > 1080 else '18', '-pix_fmt', 'yuv420p', o])
    L.append(f"file '{os.path.abspath(o)}'"); cuts.append(round(t, 3)); t += d
o = f'show/teaser/title_{RES}.mp4'; run(['-f', 'lavfi', '-i', f'color=c=black:s={W}x{H}:r=24000/1001', '-t', f'{TITLE:.3f}', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', o])
L.append(f"file '{os.path.abspath(o)}'"); title_at = t; t += TITLE
open('show/teaser/list.txt', 'w').write('\n'.join(L))
run(['-f', 'concat', '-safe', '0', '-i', 'show/teaser/list.txt', '-c', 'copy', f'show/teaser/teaser_{RES}.mp4'])
json.dump(dict(dur=t, cuts=cuts, title_at=title_at, slowmo_at=cuts[-1]), open('show/teaser/teaser.json', 'w'), indent=1)

# audio: music (bed 'Hip-Hop Power' from its drop) + the two voice lines, music dipped under the voice; hit on the title
if RES == 1080:
    MUS = '../npc-italy/src/music/kulakovka-hip-hop-power-614899.mp3'; SFX = '../../assets/sfx/'
    v2 = cuts[-1]
    duck = f"volume='if(between(t,0,4.5)+between(t,{v2 - 0.1:.2f},{v2 + 3.9:.2f}),0.32,1)':eval=frame"
    run(['-ss', '8.0', '-i', MUS, '-ss', '0', '-t', '4.4', '-i', 'show/dn/c15_voice.wav', '-ss', '66.2', '-t', '3.8', '-i', 'show/dn/c17_voice.wav',
         '-i', SFX + 'transitions/whoosh.mp3', '-filter_complex',
         f"[0:a]atrim=0:{t:.3f},afade=t=in:d=0.4,afade=t=out:st={t - 1.6:.3f}:d=1.6,volume=-6dB,{duck}[m];"
         f"[1:a]volume=+1dB,afade=t=out:st=4.2:d=0.2[v1];[2:a]aresample=48000,volume=+1dB,afade=t=in:d=0.05,afade=t=out:st=3.6:d=0.2,adelay={int(v2 * 1000)}|{int(v2 * 1000)}[v2];"
         f"[3:a]volume=-6dB,adelay={int(title_at * 1000)}|{int(title_at * 1000)}[w];"
         f"[m][v1][v2][w]amix=inputs=4:normalize=0,atrim=0:{t:.3f},aformat=sample_rates=48000:channel_layouts=stereo[o]",
         '-map', '[o]', '-c:a', 'pcm_s24le', 'audio/teaser.wav'])
print('teaser', round(t, 2), 's; cuts', cuts, 'title at', round(title_at, 2))
