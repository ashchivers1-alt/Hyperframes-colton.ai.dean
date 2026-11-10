"""Dialogue stem (new timeline timing) + music beds per section, ducked under the voice where they overlap it.
Pixabay tracks (Pixabay Content License: free commercial use, no attribution)."""
import json, subprocess
P = json.load(open('plan.json')); FPS = P['fps']; M = P['marks']
SR = 48000
def run(a): subprocess.run(['ffmpeg', '-v', 'error', '-y'] + a, check=True)
def sec(fr): return fr / FPS

# ---- dialogue stem ----
total = sec(M['end'])
inputs, fc, labels = [], [], []
for k, s in enumerate([s for s in P['segs'] if s['dlg']]):
    d = s['dlg']; inputs += ['-i', d['file']]
    fc.append(f"[{k}:a]atrim=start={d['start']:.4f}:end={d['end']:.4f},asetpts=PTS-STARTPTS,"
              f"adelay={sec(s['rec']) * 1000:.1f}:all=1[d{k}]")
    labels.append(f'[d{k}]')
fc.append(''.join(labels) + f"amix=inputs={len(labels)}:normalize=0,apad,atrim=end={total:.4f}[out]")
run(inputs + ['-filter_complex', ';'.join(fc), '-map', '[out]', '-ar', str(SR), '-ac', '2', '-c:a', 'pcm_s24le', 'audio/dialogue_stem.wav'])
print('stem', f'{total:.1f}s')

MUS = 'src/music/'
T = dict(lofi=MUS + 'alex-morgan-lofi-hip-hop-jazzy-coffee-shop-560036.mp3',
         desires=MUS + '42698505-desires-rnb-type-beat-277125.mp3',
         smoke=MUS + 'soulprodmusic-smoke-143172.mp3',
         sport=MUS + 'the_mountain-hip-hop-sport-567422.mp3',
         gym=MUS + 'vaitsez-gym-gym-music-574157.mp3',
         power=MUS + 'kulakovka-hip-hop-power-614899.mp3',
         chill=MUS + 'danyvin-chill-rnb-621264.mp3')

def bed(name, tracks, a, b, level, duck=False, fade_in=1.0, fade_out=1.5, offset=0.0):
    """tracks: list of track keys chained with 2 s crossfades; section = record frames [a, b)."""
    L = sec(b - a)
    ins, fc = [], []
    for k, t in enumerate(tracks):
        ins += ['-i', T[t]]
        fc.append(f'[{k}:a]aresample={SR},aformat=channel_layouts=stereo[t{k}]')
    cur = 't0'
    for k in range(1, len(tracks)):
        fc.append(f'[{cur}][t{k}]acrossfade=d=2:c1=tri:c2=tri[x{k}]'); cur = f'x{k}'
    fc.append(f'[{cur}]atrim=start={offset}:end={offset + L:.4f},asetpts=PTS-STARTPTS,'
              f'afade=t=in:d={fade_in},afade=t=out:st={max(0, L - fade_out):.4f}:d={fade_out}[m]')
    out = f'audio/music_{name}.wav'
    tmp = out.replace('.wav', '_raw.wav')
    run(ins + ['-filter_complex', ';'.join(fc), '-map', '[m]', '-c:a', 'pcm_s24le', tmp])
    # set level (fixed gain from measured loudness)
    o = subprocess.run(['ffmpeg', '-nostats', '-i', tmp, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(o[o.rindex('I:'):].split()[1]); g = level - I
    if duck:   # sidechain: dip ~10 dB under the voice, recover in gaps
        run(['-i', tmp, '-ss', f'{sec(a):.4f}', '-t', f'{L:.4f}', '-i', 'audio/dialogue_stem.wav', '-filter_complex',
             f'[0:a]volume={g:.2f}dB[m];[1:a]aresample={SR},highpass=f=150[sc];'
             f'[m][sc]sidechaincompress=threshold=0.015:ratio=10:attack=40:release=700:makeup=1[o]',
             '-map', '[o]', '-c:a', 'pcm_s24le', out])
    else:
        run(['-i', tmp, '-af', f'volume={g:.2f}dB', '-c:a', 'pcm_s24le', out])
    import os; os.remove(tmp)
    print(name, f'{L:.1f}s', f'gain {g:+.1f}dB', 'duck' if duck else '', flush=True)
    return dict(name=name, file=out, rec=a, dur=b - a)

beds = []
beds.append(bed('hyperlapse', ['lofi'], M['i2'], M['i3'], -20, fade_in=0.6, fade_out=1.2, offset=4))
beds.append(bed('checkin_golds', ['desires'], M['i6'], M['i10'], -19, fade_in=0.5, fade_out=1.5))
for k in ('vn_fast1', 'vn_fast3'):
    r, n = M[k]
    beds.append(bed(k, ['lofi'], r, r + n, -21, fade_in=0.25, fade_out=0.4, offset=40 if k == 'vn_fast1' else 70))
beds.append(bed('gym', ['sport', 'gym', 'sport'], M['i13'], M['i26'], -21, duck=True, fade_in=0.8, fade_out=1.0, offset=9))
beds.append(bed('posing', ['power'], M['i26'], M['i30'], -19, duck=True, fade_in=0.4, fade_out=2.0, offset=8))
beds.append(bed('checkin_showday', ['smoke'], M['i33'], M['i35'], -20, fade_in=1.0, fade_out=1.5, offset=17))
json.dump(beds, open('beds.json', 'w'), indent=1)
