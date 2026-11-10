"""Dialogue (talk units only, 48k from source MP4s, levelled) + beat-aligned music bed, ducked."""
import json, subprocess, glob, re

U = json.load(open('units.json')); units, TOTAL = U['units'], U['total']
D = '/Volumes/Untitled/DCIM/DJI_001/'
def src(c): return glob.glob(D + f'DJI_*_{c[1:]}_D.MP4')[0]
def lufs(path):
    o = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', o)[-1])

VOICE_FX = ("afftdn=nr=10:nf=-42,highpass=f=85,equalizer=f=170:t=q:w=1.0:g=3,equalizer=f=420:t=q:w=1.4:g=-2.5,"
            "equalizer=f=3000:t=q:w=1.2:g=4.5,equalizer=f=6500:t=q:w=1.0:g=1.5,"
            "acompressor=threshold=-24dB:ratio=3:attack=8:release=140:makeup=2")

# 1) each talk unit -> its own levelled wav (pieces joined with 15ms fades to avoid clicks)
parts = []
for i, u in enumerate(units):
    if u['kind'] != 'talk': continue
    raw = f'out/a_{i:02d}_raw.wav'; ins, f = [], []
    for j, (a, b) in enumerate(u['pieces']):
        ins += ['-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', src(u['clip'])]
        f.append(f"[{j}:a]aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.015,afade=t=out:st={b - a - 0.015:.3f}:d=0.015[p{j}]")
    n = len(u['pieces'])
    fc = ';'.join(f) + ';' + ''.join(f'[p{j}]' for j in range(n)) + f'concat=n={n}:v=0:a=1[o]'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', fc, '-map', '[o]', raw], check=True)
    if u['tag'] in ('review', 'review2'):
        # voice enhance for the product review (Ash: voice sounds thin/hard to hear): light denoise, body + presence EQ, gentle compression
        enh = raw.replace('_raw', '_enh')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', raw, '-af', VOICE_FX, enh], check=True); raw = enh
    gain = (-16.0 if u['tag'] in ('review', 'review2') else -17.0) - lufs(raw)
    fin = u['xf_in'] if u['xf_in'] > 0.05 else 0.03
    lev = f'out/a_{i:02d}.wav'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', raw, '-af',
                    f"volume={gain:.2f}dB,alimiter=limit=0.89,afade=t=in:d={fin:.3f},afade=t=out:st={u['dur'] - 0.25:.3f}:d=0.25", lev], check=True)
    parts.append((u['start'], lev)); print(u['tag'], 'gain', round(gain, 1))

ins, f = [], []
for k, (st, p) in enumerate(parts):
    ins += ['-i', p]; ms = int(round(st * 1000)); f.append(f"[{k}:a]adelay={ms}|{ms}[d{k}]")
fc = ';'.join(f) + ';' + ''.join(f'[d{k}]' for k in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0,apad,atrim=end={TOTAL}[o]"
open('out/dlg_mix.txt', 'w').write(fc)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-/filter_complex', 'out/dlg_mix.txt', '-map', '[o]', '-c:a', 'pcm_s24le', '-ar', '48000', 'out/dialogue-v3.wav'], check=True)

# 2) music: Gym Phonk (training, beat 0 at output 0) + vlog track (low) under the Formula 75 review
RA = next(u for u in units if u['tag'] == 'review')['start']; RB = next(u for u in units if u['tag'] == 'review2')['end']
import os
P = os.environ.get('TRACK', '../../vlog-music/assets/download/sub_clair-gym-phonk-571899.mp3'); T0 = float(os.environ.get('TSTART', '7.705'))
L = float(os.environ.get('LOOP', 128 * 0.47922)); segs = int(TOTAL // L) + 2
f = [f"[0:a]atrim=start={T0}:end={T0 + L:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,asplit={segs}" + ''.join(f'[p{i}]' for i in range(segs))]
cur = 'p0'
for i in range(1, segs):
    f.append(f"[{cur}][p{i}]acrossfade=d=0.02[q{i}]"); cur = f'q{i}'
f.append(f"[{cur}]atrim=end={TOTAL}[out]")
open('out/phonk.txt', 'w').write(';'.join(f))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', P, '-/filter_complex', 'out/phonk.txt', '-map', '[out]', 'out/phonk-raw.wav'], check=True)
V = '../../vlog-music/assets/download/the_mountain-upbeat-upbeat-music-567445.mp3'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', '0.285', '-i', V, '-af', 'aformat=sample_rates=48000:channel_layouts=stereo', '-t', f'{RB - RA + 3:.3f}', 'out/vlog-raw.wav'], check=True)
pg = -18.0 - lufs('out/phonk-raw.wav'); vg = -30.0 - lufs('out/vlog-raw.wav')
d0 = int((RA - 1.0) * 1000)
# extra -10 dB dip on the phonk under every talk unit (ramped 0.35s) so funny bits/coaching stay clear
talk = [u for u in units if u['kind'] == 'talk' and u['tag'] not in ('review', 'review2')]
env_ = '+'.join(f"min(1,max(0,(t-{u['start']:.3f})/0.35))*min(1,max(0,({u['end']:.3f}-t)/0.35))" for u in talk)
dip = f"volume='1-0.684*min(1,{env_})':eval=frame" 
fc = (f"[0:a]volume={pg:.2f}dB,volume='min(1,max(0,({RA + 0.2:.3f}-t)/1.0))+min(1,max(0,(t-{RB - 0.33:.3f})/0.6))':eval=frame,{dip}[ph];"
      f"[1:a]volume={vg:.2f}dB,afade=t=in:d=1.0,afade=t=out:st={RB - RA + 0.3:.3f}:d=0.6,adelay={d0}|{d0}[vl];"
      f"[ph][vl]amix=inputs=2:normalize=0[m];[2:a]highpass=f=120[sc];"
      f"[m][sc]sidechaincompress=threshold=0.01:ratio=12:attack=40:release=600:makeup=1[d];"
      f"[d]afade=t=in:d=0.4,afade=t=out:st={TOTAL - 3:.3f}:d=3,alimiter=limit=0.7,apad,atrim=end={TOTAL}[o]")
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'out/phonk-raw.wav', '-i', 'out/vlog-raw.wav', '-i', 'out/dialogue-v3.wav', '-filter_complex', fc,
                '-map', '[o]', '-c:a', 'pcm_s24le', '-ar', '48000', 'out/music-v3.wav'], check=True)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'out/dialogue-v3.wav', '-af', 'alimiter=limit=0.79:attack=2:release=50:level=disabled', '-c:a', 'pcm_s24le', 'out/dialogue-v3b.wav'], check=True)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'out/dialogue-v3b.wav', '-i', 'out/music-v3.wav', '-filter_complex',
                '[0:a][1:a]amix=inputs=2:normalize=0[o]', '-map', '[o]', '-c:a', 'pcm_s24le', 'out/mix-preview.wav'], check=True)
print('dialogue', lufs('out/dialogue-v3.wav'), 'music', lufs('out/music-v3.wav'), 'mix', lufs('out/mix-preview.wav'))
