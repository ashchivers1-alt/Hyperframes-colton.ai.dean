"""Composite the race-broadcast overlays onto the 4K base render of Ash's Resolve edit.
usage: composite.py draft|final [out] [--start S --dur D]
  base  = assets/base-4k.mov  (Resolve 'Timeline 1 - 4K', tl frames 91141-124727, i.e. DJI source 45.64s on)
  times below are DJI source seconds (= timeline seconds); base time = T - BASE0.
draft = 1920x1080 hardware H.264 for review; final = 3840x2160 libx264 CRF 16."""
import json, os, subprocess, sys
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(P)
q = sys.argv[1]
args = sys.argv[2:]
out = args[0] if args and not args[0].startswith('--') else f'renders/daytona-{q}.mp4'
ss = float(args[args.index('--start') + 1]) if '--start' in args else 0.0
dd = float(args[args.index('--dur') + 1]) if '--dur' in args else None
R = json.load(open('src/race.json'))
BASE0 = 91141 / 25 - 3600          # 45.64 s
O = 'gfx/out4k/'
# (file, start T, x, y) in 4K pixels
OV = [('smoke.mov', None, 0, 0), ('heat.mov', 47.5, 0, 0), ('track3d.mov', 57.0, 0, 0), ('grid.mov', 80.0, 0, 0), ('lights.mov', R['lights_in'], 0, 0),
      ('hud.mov', R['hud_in'], (1920 - 93 - 640) * 2, 63 * 2)]

ins = ['-ss', f'{ss:.3f}', '-i', 'assets/base-4k.mov']
fc = ['[0:v]setpts=PTS-STARTPTS,format=yuv420p10le[b0]']
cur = 'b0'
for k, (f, t, x, y) in enumerate(OV, 1):
    if t is None:                                          # looping smoke border: whole video
        ins += ['-stream_loop', '-1', '-i', O + f]
        fc.append(f'[{k}:v]setpts=PTS-STARTPTS,format=yuva444p10le[o{k}]')
        fc.append(f'[{cur}][o{k}]overlay=0:0:shortest=0:eof_action=pass:format=auto[b{k}]')
        cur = f'b{k}'; continue
    off = t - BASE0 - ss                                   # overlay start on the output clock
    ins += ['-i', O + f]
    fc.append(f'[{k}:v]setpts=PTS-STARTPTS+{off:.3f}/TB,format=yuva444p10le[o{k}]')
    fc.append(f'[{cur}][o{k}]overlay={x}:{y}:eof_action=pass:format=auto[b{k}]')
    cur = f'b{k}'
# overtake SFX: cha-ching when Ash gains a place, game-show buzzer when he loses one (synthesized, scripts/sfx_synth.py)
amix = ['[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[a0]']; alab = ['[a0]']
pos = R['positions']; k = len(OV) + 1
for (t0, p0), (t1, p1) in zip(pos, pos[1:]):
    at = t1 - BASE0 - ss
    if at < 0 or (dd and at > dd): continue
    f, gain = ('assets/sfx-chaching.wav', -3.0) if p1 < p0 else ('assets/sfx-buzzer.wav', -10.0)
    ins += ['-i', f]; ms = int(at * 1000)
    amix.append(f'[{k}:a]volume={gain}dB,adelay={ms}|{ms}[s{k}]'); alab.append(f'[s{k}]'); k += 1
# start sequence: three countdown beeps one second apart, then the "go" beep on the green
g = R['green']
for t, f, gain in ((g - 3, 'assets/sfx-beep.wav', -8.0), (g - 2, 'assets/sfx-beep.wav', -8.0), (g - 1, 'assets/sfx-beep.wav', -8.0), (g, 'assets/sfx-go.wav', -6.0)):
    at = t - BASE0 - ss
    if at < 0 or (dd and at > dd): continue
    ins += ['-i', f]; ms = int(at * 1000)
    amix.append(f'[{k}:a]volume={gain}dB,adelay={ms}|{ms}[s{k}]'); alab.append(f'[s{k}]'); k += 1
amix.append(''.join(alab) + f'amix=inputs={len(alab)}:normalize=0:duration=first,alimiter=limit=0.95:level=false[a]')
fc += amix
if q == 'draft':
    fc.append(f'[{cur}]scale=1920:1080:flags=bicubic,format=yuv420p[v]')
    enc = ['-c:v', 'h264_videotoolbox', '-b:v', '16M']
else:
    fc.append(f'[{cur}]format=yuv420p[v]')
    enc = ['-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-profile:v', 'high', '-level', '5.2', '-x264-params', 'keyint=50']
cmd = ['ffmpeg', '-nostdin', '-v', 'error', '-stats', '-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '[a]']
if dd: cmd += ['-t', f'{dd:.3f}']
cmd += enc + ['-r', '25', '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', out]
subprocess.run(cmd, check=True)
print('wrote', out)
