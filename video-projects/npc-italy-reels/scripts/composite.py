"""Composite a reel: cut vertical video + conformed graphics overlay + dialogue / music bed (ducked) / SFX.
usage: composite.py <reel> draft|final [out]
draft = 1080x1920 from gfx/out1 (fast review); final = 2160x3840 from gfx/out4k."""
import json, subprocess, sys, os
name, q = sys.argv[1], sys.argv[2]
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(P)
WS = '/Users/ashleychivers/Documents/Claude Video Studio'
MUS = WS + '/video-projects/npc-italy/src/music/'
BEDS = {  # file, integrated LUFS (measured) -> bed sits ~-32 LUFS before ducking
    'post-show-recovery': ('danyvin-chill-rnb-621264.mp3', -7.9),
    'life-balance': ('soulprodmusic-smoke-143172.mp3', -10.1),
    'judge-your-prep': ('the_mountain-hip-hop-sport-567422.mp3', -9.5),
    # bicep-stretch keeps the gym bed already in the edit's audio
}
SFX = {'whoosh': 'transitions/whoosh.mp3', 'pop': 'ui/pop.mp3', 'click': 'ui/click.wav', 'slam': 'impact/slam.mp3'}
FPS = 24000 / 1001
ovl_dir = 'gfx/out1' if q == 'draft' else 'gfx/out4k'
out = sys.argv[3] if len(sys.argv) > 3 else f'renders/{name}-{q}.mp4'

dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'assets/{name}-dlg.wav']))
ins = ['-i', f'assets/{name}-v.mp4', '-i', f'{ovl_dir}/{name}-24.mov', '-i', f'assets/{name}-dlg.wav']
fc = []
size = '1080:1920' if q == 'draft' else '2160:3840'
fc.append(f'[0:v]scale={size}:flags=bicubic,format=yuv420p[bv]')
# overlay rendered at 24 fps with times pre-scaled by 1/1.001 -> conform to 23.976
fc.append(f'[1:v]setpts=N/({FPS})/TB,scale={size}:flags=bicubic,tpad=stop_mode=clone:stop_duration=0.5,format=yuva420p[ov]')
fc.append('[bv][ov]overlay=0:0:eof_action=pass:format=auto,format=yuv420p[v]')
mix = ['[dlg]']
fc.append('[2:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[dlg][key]')
k = 3
if name in BEDS:
    f, lufs = BEDS[name]
    ins += ['-i', MUS + f]
    g = -32 - lufs
    fc.append(f'[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{dur:.3f},volume={g:.1f}dB,'
              f'afade=t=in:d=0.6,afade=t=out:st={dur - 1.8:.3f}:d=1.8[bedraw]')
    fc.append('[bedraw][key]sidechaincompress=threshold=0.03:ratio=3:attack=20:release=350[bed]')
    mix.append('[bed]'); k += 1
else:
    fc.append('[key]anullsink')
for j, (s, t, vol) in enumerate(json.load(open(f'gfx/sfx_{name}.json'))):
    ins += ['-i', f'{WS}/assets/sfx/{SFX[s]}']
    ms = max(0, int(t * 1000))
    fc.append(f'[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={vol * 0.6:.3f},adelay={ms}|{ms}[s{j}]')
    mix.append(f'[s{j}]'); k += 1
fc.append(''.join(mix) + f'amix=inputs={len(mix)}:normalize=0:duration=first,alimiter=limit=0.93:level=false[a]')
enc = (['-c:v', 'libx264', '-preset', 'fast', '-crf', '22'] if q == 'draft'
       else ['-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-profile:v', 'high', '-level', '5.2', '-maxrate', '100M', '-bufsize', '200M'])
cmd = (['ffmpeg', '-nostdin', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '[a]']
       + enc + ['-pix_fmt', 'yuv420p', '-r', '24000/1001', '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', '-t', f'{dur:.3f}', out])
subprocess.run(cmd, check=True)
print('wrote', out)
