"""Voiceover pass on Ash's Resolve timeline ('Timeline 1 - 4K', DAYTONA MK - TNL):
  V1  daytona-mk-tnl.mp4 @0  ·  end card straight after (no gap; Ash's call)  ·  outro (gfx/out4k/outro.mov + Ash's 9:16 subscribe clip screen-blended) @OUTRO
  A4-A6 voiceover clips at the positions Ash placed them (source in = 1.0 s each).
Voice: high-pass, denoise, de-mud/presence EQ, compression, levelled to VO_LUFS.
Race/outro audio ducks DUCK_DB under speech (speech regions from silencedetect, merged, ramped) — except over the HKC ad.
usage: vo_mix.py audio|video|all [out.mp4]"""
import os, re, subprocess, sys
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(P)
H = os.path.expanduser('~')
MAIN = f'{H}/Documents/Claude Video - Completed/daytona-mk-tnl.mp4'
OUTRO_SRC = f'{H}/Downloads/YOUTUBE - INTRO : OUTRO.MOV'
VD = f'{H}/DaVinci Resolve Media/DAYTONA MK - TNL/Audio Files/Voiceover/Timeline 1 - 4K/'
FPS = 25
MAIN_LEN = 34959 / FPS                     # 1398.36
OUTRO, OUTRO_LEN = MAIN_LEN, 395 / FPS     # 9:16 subscribe clip: 15.8 s, starts the frame the race ends
CARD = 17.0                                # end card holds past the clip until the last VO ends (1414.36) + 1 s
TOTAL = OUTRO + CARD                       # 1415.36
# (file, timeline start s, duration s); source in-point 1.0 s on all three
VO = [('Audio 4_003_2ITSFP.wav', 0.0, 1468 / FPS), ('Audio 5_001_2ITSW8.wav', 2512 / FPS, 1580 / FPS),
      ('Audio 6_001_2ITT5K.wav', 32829 / FPS, 2530 / FPS)]
AD = (108.96, 155.08)                      # pause + HKC ad: Ash is happy with the balance there, no ducking
VO_LUFS, DUCK_DB, PRE, POST, MERGE = -16.5, -9.0, 0.35, 0.6, 1.6
CHAIN = ('highpass=f=90,afftdn=nr=18:nf=-46:tn=1,agate=threshold=0.012:ratio=2:range=0.3:attack=8:release=250,equalizer=f=250:t=q:w=1.1:g=-2.5,equalizer=f=3200:t=q:w=1.3:g=3.5,'
         'treble=g=2:f=9000,acompressor=threshold=-26dB:ratio=3.5:attack=6:release=140:makeup=2')
TMP = 'renders/vo'; os.makedirs(TMP, exist_ok=True)

def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)

def clean_vo():
    """per clip: trim, enhance, normalise -> renders/vo/vo{i}.wav (mono 48k) + speech regions on the timeline"""
    regions = []
    for i, (f, at, dur) in enumerate(VO):
        raw = f'{TMP}/vo{i}-pre.wav'
        run(['ffmpeg', '-y', '-ss', '1.0', '-t', f'{dur:.3f}', '-i', VD + f, '-af', CHAIN, '-ar', '48000', '-ac', '1', raw])
        lufs = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', run(['ffmpeg', '-nostats', '-i', raw, '-af', 'ebur128', '-f', 'null', '-']).stderr)[-1])
        out = f'{TMP}/vo{i}.wav'
        run(['ffmpeg', '-y', '-i', raw, '-af', f'volume={VO_LUFS - lufs:.2f}dB,alimiter=limit=0.89:level=false', out])
        sd = run(['ffmpeg', '-nostats', '-i', out, '-af', 'silencedetect=noise=-38dB:d=0.5', '-f', 'null', '-']).stderr
        ss = [float(x) for x in re.findall(r'silence_start: (-?[\d.]+)', sd)]
        se = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', sd)]
        # speech = complement of silence
        edges, t = [], 0.0
        for a, b in zip(ss, se + [dur] * (len(ss) - len(se))):
            if a > t + 0.05: edges.append((t, a))
            t = b
        if t < dur - 0.05: edges.append((t, dur))
        regions += [(at + a, at + b) for a, b in edges]
        print(f'vo{i}: {lufs:.1f} -> {VO_LUFS} LUFS, {len(edges)} speech runs')
    merged = []
    for a, b in sorted(regions):
        if merged and a - merged[-1][1] < MERGE: merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else: merged.append((a, b))
    out = []                                   # cut the HKC ad window out of every run
    for a, b in merged:
        if a < AD[0]: out.append((a, min(b, AD[0])))
        if b > AD[1]: out.append((max(a, AD[1]), b))
    return out

def duck_expr(regions):
    """gain(t): 1 outside speech, DUCK below; PRE s ramp down before a run, POST s ramp up after"""
    g = 10 ** (DUCK_DB / 20)
    terms = [f'clip((t-{a - PRE:.3f})/{PRE},0,1)*clip(({b + POST:.3f}-t)/{POST},0,1)' for a, b in regions]
    m = terms[0]
    for x in terms[1:]: m = f'max({m},{x})'
    return f'1-{1 - g:.4f}*{m}'

def audio():
    regions = clean_vo()
    open(f'{TMP}/regions.txt', 'w').write('\n'.join(f'{a:.2f}\t{b:.2f}' for a, b in regions))
    expr = duck_expr(regions)
    open(f'{TMP}/duck.expr', 'w').write(expr)
    o = int(OUTRO * 1000)
    fc = [f'[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={TOTAL}[m]',
          f'[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{OUTRO_LEN},afade=t=out:st={OUTRO_LEN - 0.8}:d=0.8,adelay={o}|{o}[ot]',
          f'[m][ot]amix=inputs=2:normalize=0:duration=first,volume=\'{expr}\':eval=frame[bed]']
    ins = ['-i', MAIN, '-i', OUTRO_SRC]
    labs = ['[bed]']
    for i, (_, at, _) in enumerate(VO):
        ms = int(round(at * 1000)); ins += ['-i', f'{TMP}/vo{i}.wav']
        fc.append(f'[{i + 2}:a]pan=stereo|c0=c0|c1=c0,adelay={ms}|{ms}[v{i}]'); labs.append(f'[v{i}]')
    fc.append(''.join(labs) + f'amix=inputs={len(labs)}:normalize=0:duration=first,atrim=0:{TOTAL},alimiter=limit=0.95:level=false[a]')
    open(f'{TMP}/fc.txt', 'w').write(';\n'.join(fc))
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-stats', '-y'] + ins + ['-/filter_complex', f'{TMP}/fc.txt', '-map', '[a]',
                    '-c:a', 'pcm_s24le', f'{TMP}/mix.wav'], check=True)
    print('wrote', f'{TMP}/mix.wav')

def video(out):
    fc = (f'[0:v]setpts=PTS-STARTPTS,format=yuv420p[m];'
          f'[1:v]format=gbrp,trim=0:{CARD},setpts=PTS-STARTPTS[oa];'
          f'[2:v]fps=25,trim=0:{OUTRO_LEN},setpts=PTS-STARTPTS,scale=1519:2700:flags=lanczos,crop=1412:2160:90:270,pad=3840:2160:0:0:black,tpad=stop_mode=add:stop_duration={CARD - OUTRO_LEN:.2f}:color=black,format=gbrp[ob];'
          f'[oa][ob]blend=all_mode=screen,format=yuv420p[o];[m][o]concat=n=2:v=1:a=0[v]')
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-stats', '-y', '-i', MAIN, '-i', 'gfx/out4k/outro.mov', '-i', OUTRO_SRC,
                    '-i', f'{TMP}/mix.wav', '-filter_complex', fc, '-map', '[v]', '-map', '3:a',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-profile:v', 'high', '-level', '5.2', '-x264-params', 'keyint=50',
                    '-r', '25', '-c:a', 'aac', '-b:a', '320k', '-t', f'{TOTAL:.3f}', '-movflags', '+faststart', out], check=True)
    print('wrote', out)

if __name__ == '__main__':
    q = sys.argv[1]
    if q in ('audio', 'all'): audio()
    if q in ('video', 'all'): video(sys.argv[2])
