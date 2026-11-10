"""Music beds + SFX: audio/bed_intro.wav (posing section) and audio/bed_train.wav (training; starts at the training's first frame)."""
import json, subprocess
FPS = 24000 / 1001; MUS = '../npc-italy/src/music/'; SFX = '../../assets/sfx/'
EDL = json.load(open('edl.json')); G = {m['name']: m for m in json.load(open('gfx/made.json'))}
T0 = json.load(open('gym.json'))['rec'] / FPS; TEND = (EDL[-1]['rec'] + EDL[-1]['dur']) / FPS; D = TEND - T0
LOW, HIGH = -27.0, -13.0           # dB on the -9 LUFS masters: under talk vs music-only reps
# volume envelope (dB) for the training bed
pts = [(0, HIGH)]                 # gym exterior clip: music up
for p in EDL:
    a, b = p['rec'] / FPS - T0, (p['rec'] + p['dur']) / FPS - T0
    lvl = HIGH if p['mode'] == 'mus' else LOW
    pts += [(a + 0.25, lvl), (b - 0.25, lvl)]
pts.append((D, LOW))
def env(pts):
    e = '0'
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        if t1 <= t0: continue
        e = f"if(between(t,{t0:.3f},{t1:.3f}),{v0}+({v1}-({v0}))*(t-{t0:.3f})/{t1 - t0:.3f},{e})"
    return e
SPLIT = [p for p in EDL if p['ex'] == 'press'][0]['rec'] / FPS - T0
open('audio/env.txt', 'w').write(env(pts))
# SFX: whoosh on exercise cards, soft pop on coaching cues / tags (training-relative seconds)
sfx = []
for n, m in G.items():
    t = m['rec'] / FPS - T0
    if n.startswith('t0'): sfx.append(('transitions/whoosh.mp3', t, -14))
    elif n.startswith('t'): sfx.append(('ui/pop.mp3', t + 0.1, -18))
ins = ['-stream_loop', '-1', '-i', MUS + 'vaitsez-gym-gym-music-574157.mp3', '-stream_loop', '-1', '-i', MUS + 'the_mountain-hip-hop-sport-567422.mp3']
fc = [f'[0:a]atrim=0:{SPLIT + 1.5:.3f},afade=t=out:st={SPLIT:.3f}:d=1.5[m1]',
      f'[1:a]atrim=0:{D - SPLIT + 0.1:.3f},afade=t=in:d=1.5,adelay={int(SPLIT * 1000)}|{int(SPLIT * 1000)}[m2]',
      f'[m1][m2]amix=inputs=2:normalize=0,atrim=0:{D:.3f},afade=t=in:d=1.0,afade=t=out:st={D - 3:.3f}:d=3,'
      f"volume='pow(10,({env(pts)})/20)':eval=frame[bed]"]
for i, (f, t, db) in enumerate(sfx):
    ins += ['-i', SFX + f]; fc.append(f'[{i + 2}:a]volume={db}dB,adelay={int(t * 1000)}|{int(t * 1000)}[s{i}]')
fc.append('[bed]' + ''.join(f'[s{i}]' for i in range(len(sfx))) + f'amix=inputs={len(sfx) + 1}:normalize=0,atrim=0:{D:.3f},aformat=sample_rates=48000:channel_layouts=stereo[out]')
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', '[out]', '-c:a', 'pcm_s24le', 'audio/bed_train.wav'], check=True)
# posing section: Kulakovka 'Hip-Hop Power' (Pixabay, not Content ID registered), looped with crossfades, under the talk + pops on graphics
ins = ['-i', MUS + 'kulakovka-hip-hop-power-614899.mp3'] * 3; fc = ['[0:a][1:a]acrossfade=d=3[x1]', '[x1][2:a]acrossfade=d=3[loop]']; k = 2
for n, m in G.items():
    if not n.startswith('p'): continue
    t = m['rec'] / FPS; ins += ['-i', SFX + 'ui/pop.mp3']; k += 1
    fc.append(f'[{k}:a]volume=-19dB,adelay={int(t * 1000)}|{int(t * 1000)}[s{k}]')
fc.insert(2, f'[loop]atrim=0:{T0:.3f},volume=-27dB,afade=t=in:d=1.5,afade=t=out:st={T0 - 2:.3f}:d=2[bed]')
fc.append('[bed]' + ''.join(f'[s{i}]' for i in range(3, k + 1)) + f'amix=inputs={k - 1}:normalize=0,atrim=0:{T0:.3f},aformat=sample_rates=48000:channel_layouts=stereo[out]')
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', '[out]', '-c:a', 'pcm_s24le', 'audio/bed_intro.wav'], check=True)
print('train bed', round(D, 2), 's; intro bed', round(T0, 2), 's; sfx', len(sfx), k)
