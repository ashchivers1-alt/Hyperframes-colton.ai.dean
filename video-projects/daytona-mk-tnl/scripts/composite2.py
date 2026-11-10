"""v2 cut: trimmed start, slow-mo / zoom / freeze segments, rebuilt lap-timer overlay (sync-shifted), event graphics.
usage: composite2.py draft|final [out] [--only id,id] [--skip-pieces]
  camera  = DJI source (Resolve applies no grade or transform to V1, verified frame-for-frame)
  overlay = the lap-timer editor .mov exactly as Ash placed it on V2/V3 (identity transforms; V3 doubles it from 212.28),
            delayed by race.json overlay_delay so the Best/Prev panel lands on the first start/finish crossing
  T-time layers (camera, overlay, HUD, cards) are retimed per piece; fx comps are already in output time.
Pieces render to renders/pieces/<q>/ (ProRes), then concat + mixed audio -> one H.264."""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import timemap as TM
P = TM.P; os.chdir(P); R = TM.R
q = sys.argv[1]; args = sys.argv[2:]
out = args[0] if args and not args[0].startswith('--') else f'renders/daytona-{q}.mp4'
only = args[args.index('--only') + 1].split(',') if '--only' in args else None
FINAL = q == 'final'
RW, RH = (3840, 2160) if FINAL else (1920, 1080)
K = 1.0 if FINAL else 0.5                                   # 4K-pixel coords -> output pixels
SRC = '/Volumes/SD_Card/DCIM/DJI_001/DJI_20261029210231_0003_D.MP4'
OVL = os.path.expanduser('~/Downloads/30_10_26_17_08_All_Laps_Overlay_editor.mov')
O = 'gfx/out4k/'
D = R['overlay_delay']
PD = f'renders/pieces/{q}'; os.makedirs(PD, exist_ok=True)

def dur(f):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]))

# (file, T start, T end, source time at T start, x, y [4K px], scale-to-4K?)
OV_END = 1382.88 + D
TCLIPS = [(OVL, 45.64 + D, 125.8 + D, 0.0, 0, 0, True),
          (OVL, 125.8 + D, OV_END, 0.0, 0, 0, True),
          (OVL, 212.28 + D, OV_END, 86.48, 0, 0, True)]
for name, t in (('heat', R['cards']['heat']), ('track3d', R['cards']['track3d']), ('grid', R['cards']['grid']), ('lights', R['lights_in'])):
    TCLIPS.append((O + name + '.mov', t, t + dur(O + name + '.mov'), 0.0, 0, 0, False))
TCLIPS.append((O + 'hud.mov', R['hud_in'], R['hud_in'] + dur(O + 'hud.mov'), 0.0, (1920 - 93 - 640) * 2, 63 * 2, False))

SEGS = {p['id']: p for p in TM.PIECES}
OCLIPS = []                                                  # (file, output start, output end)
for f in R['fx']:
    fo = SEGS[f['seg']]['o0'] if 'seg' in f else SEGS[f['after']]['o1'] if 'after' in f else TM.out(f['t'])
    fn = O + 'fx-' + f['id'] + '.mov'
    OCLIPS.append((fn, fo, fo + dur(fn)))

def zoom_expr(p):
    """zoompan z/x/y: ease in over 0.6 s, out over the last 0.5 s (held through a freeze, with a punch-in on it)"""
    n = p['frames']; t = 'on/25'
    if p.get('shake'):
        ts = (p['shake'] - p['t0']) / p['speed']
        S = f'exp(-pow(({t}-{ts:.3f})/0.28,2))'
        z = f'1+0.06*{S}'
        x = f'(iw-iw/zoom)/2*(1+0.8*sin(on*2.1))'
        y = f'(ih-ih/zoom)/2*(1+0.8*cos(on*1.7))'
        return z, x, y
    Z, cx, cy = p['z'], p['cx'], p['cy']
    E = f'min(clip({t}/0.6,0,1),clip(({n}-on)/25/0.5,0,1))'
    S = f'({E})*({E})*(3-2*({E}))'
    z = f'1+{Z - 1:.3f}*{S}'
    if p.get('freeze'):
        fz = (p['t1'] - p['t0']) / p['speed']
        z = f'(1+{Z - 1:.3f}*clip({t}/0.6,0,1))*(1+0.14*clip(({t}-{fz:.3f})/0.25,0,1))'
        S = f'clip({t}/0.6,0,1)'
    if 'cx1' in p:                                           # pan the zoom target across the segment
        cx = f"({cx}+{p['cx1'] - cx:.3f}*on/{n})"; cy = f"({cy}+{p['cy1'] - cy:.3f}*on/{n})"
    x = f'clip(iw*(0.5+({cx}-0.5)*{S})-iw/zoom/2,0,iw-iw/zoom)'
    y = f'clip(ih*(0.5+({cy}-0.5)*{S})-ih/zoom/2,0,ih-ih/zoom)'
    return z, x, y

def insert_cmd(p):
    """HKC ad break: Showdown scroll -> slide -> Community scroll (4K site recordings), branding/CTA overlay is an fx comp"""
    A = R['ad']; xf = A['xfade']; n = p['frames']
    sc = '' if FINAL else ',scale=1920:1080:flags=bicubic'
    a_len = dur(A['showdown'])
    fc = [f'[0:v]fps=25{sc},format=yuv420p,setpts=PTS-STARTPTS[a]', f'[1:v]fps=25{sc},format=yuv420p,setpts=PTS-STARTPTS[b]',
          f'[a][b]xfade=transition=slideleft:duration={xf}:offset={a_len - xf:.3f}[c]']; cur = 'c'; k = 2; ins = ['-i', A['showdown'], '-i', A['community']]
    for f, fo, fe in OCLIPS:
        lo, hi = max(p['o0'], fo), min(p['o1'], fe)
        if hi <= lo:
            continue
        ins += ['-ss', f'{lo - fo:.3f}', '-t', f'{hi - lo:.3f}', '-i', f]
        fc.append(f'[{k}:v]setpts=PTS-STARTPTS+{lo - p["o0"]:.3f}/TB' + ('' if FINAL else ',scale=1920:1080') + f',format=yuva444p10le[o{k}]')
        fc.append(f'[{cur}][o{k}]overlay=0:0:eof_action=pass:format=auto[b{k}]'); cur = f'b{k}'; k += 1
    fc.append(f'[{cur}]tpad=stop_mode=clone:stop_duration=1,format=yuv422p10le[v]')
    enc = ['-c:v', 'prores_ks', '-profile:v', '1' if FINAL else '0', '-vendor', 'apl0']
    return ['ffmpeg', '-nostdin', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', '[v]', '-frames:v', str(n), '-r', '25'] + enc + ['-an', f'{PD}/{p["id"]}.mov']

def piece_cmd(p):
    if p.get('insert'):
        return insert_cmd(p)
    a, b, s, n = p['t0'], p['t1'], p['speed'], p['frames']
    fz = p.get('freeze', 0)
    ins = ['-ss', f'{a:.3f}', '-t', f'{b - a + 0.3:.3f}', '-i', SRC]
    cam = '[0:v]setpts=PTS-STARTPTS'
    if not FINAL:
        cam += ',scale=1920:1080:flags=bicubic'
    if s < 1:
        cam += f',setpts=PTS/{s},minterpolate=fps=25:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1'
    else:
        cam += ',fps=25'
    if fz:
        cam += f',trim=end={(b - a) / s:.3f},tpad=stop_mode=clone:stop_duration={fz}'
    if p.get('z', 1) != 1 or p.get('shake'):
        z, x, y = zoom_expr(p)
        cam += f",zoompan=z='{z}':x='{x}':y='{y}':d=1:s={RW}x{RH}:fps=25"
    fc = [cam + ',format=yuv420p[c0]']; cur = 'c0'; k = 1
    for f, ts, te, s0, x, y, full in TCLIPS:
        lo, hi = max(a, ts), min(b, te)
        if hi <= lo:
            continue
        ss = s0 + (lo - ts); off = (lo - a) / s
        ins += ['-ss', f'{ss:.3f}', '-t', f'{hi - lo:.3f}', '-i', f]
        ch = f'[{k}:v]setpts=(PTS-STARTPTS)/{s}+{off:.3f}/TB'
        ch += f',scale={RW}:{RH}' if full and FINAL else (',scale=1920:1080' if full else ('' if FINAL else ',scale=iw/2:ih/2'))
        if fz and te >= b:
            ch += f',fps=25,tpad=stop_mode=clone:stop_duration={fz}'
        fc.append(ch + f',format=yuva444p10le[o{k}]')
        fc.append(f'[{cur}][o{k}]overlay={int(x * K)}:{int(y * K)}:eof_action=pass:format=auto[b{k}]'); cur = f'b{k}'; k += 1
    for f, fo, fe in OCLIPS:
        lo, hi = max(p['o0'], fo), min(p['o1'], fe)
        if hi <= lo:
            continue
        ins += ['-ss', f'{lo - fo:.3f}', '-t', f'{hi - lo:.3f}', '-i', f]
        fc.append(f'[{k}:v]setpts=PTS-STARTPTS+{lo - p["o0"]:.3f}/TB' + ('' if FINAL else ',scale=1920:1080') + f',format=yuva444p10le[o{k}]')
        fc.append(f'[{cur}][o{k}]overlay=0:0:eof_action=pass:format=auto[b{k}]'); cur = f'b{k}'; k += 1
    fc.append(f'[{cur}]format=yuv422p10le[v]')
    enc = ['-c:v', 'prores_ks', '-profile:v', '1' if FINAL else '0', '-vendor', 'apl0']
    return ['ffmpeg', '-nostdin', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', '[v]', '-frames:v', str(n), '-r', '25'] + enc + ['-an', f'{PD}/{p["id"]}.mov']

def run_piece(p):
    subprocess.run(piece_cmd(p), check=True)
    got = int(subprocess.check_output(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', f'{PD}/{p["id"]}.mov']).split(b',')[0])
    print(f'{p["id"]:8} {got}/{p["frames"]} frames', flush=True)
    assert got == p['frames'], p['id']

LEAD_AIR = 0.8                                               # 'contact' headline lands in the lead slow-mo

def audio():
    """base audio retimed per piece (slow-mo pitched down, freeze = silence) + SFX at output times"""
    ins = ['-i', SRC]; fc = []; labs = []
    for i, p in enumerate(TM.PIECES):
        ch = f'[0:a]atrim={p["t0"]:.4f}:{max(p["t1"], p["t0"] + 0.04):.4f},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo'
        if p.get('insert'):
            ch += ',volume=0'
        if p['speed'] < 1:
            ch += f',asetrate={48000 * p["speed"]:.0f},aresample=48000,lowpass=f=6000'
        if p.get('freeze'):
            ch += f',apad=pad_dur={p["freeze"]}'
        ch += f',apad,atrim=end={p["frames"] / 25:.4f}'
        fc.append(ch + f'[p{i}]'); labs.append(f'[p{i}]')
    fc.append(''.join(labs) + f'concat=n={len(labs)}:v=0:a=1[base]')
    sfx = []
    pos = R['positions']
    for (t0, p0), (t1, p1) in zip(pos, pos[1:]):
        if t1 >= R['start']:
            sfx += [(TM.out(t1), 'assets/sfx-chaching.wav', -3) if p1 < p0 else (TM.out(t1), 'assets/sfx-buzzer.wav', -10)]
    g = R['green']
    sfx += [(TM.out(g - 3), 'assets/sfx-beep.wav', -8), (TM.out(g - 2), 'assets/sfx-beep.wav', -8), (TM.out(g - 1), 'assets/sfx-beep.wav', -8), (TM.out(g), 'assets/sfx-go.wav', -6)]
    for p in TM.PIECES:
        if p['speed'] < 1:
            sfx.append((max(0, p['o0'] - 0.12), 'assets/sfx-whoosh.mp3', -5))
        if p.get('freeze'):
            fzo = p['o0'] + (p['t1'] - p['t0']) / p['speed']
            sfx += ([(fzo, 'assets/sfx-hit.wav', -1), (fzo, 'assets/sfx-slam.mp3', -8)] if p['id'] == 'contact' else [(fzo, 'assets/sfx-slam.mp3', -10)])
    sfx.append((TM.out(986.74), 'assets/sfx-hit.wav', -2))
    fx = {f: (fo, fe) for f, fo, fe in OCLIPS}
    sfx.append((fx[O + 'fx-lead.mov'][0] + LEAD_AIR, 'assets/sfx-bassdrop.mp3', -8))
    ad = SEGS['ad']
    sfx += [(ad['o0'] - 0.25, 'assets/sfx-whoosh.mp3', -6), (ad['o1'] - 0.45, 'assets/sfx-whoosh.mp3', -6)]
    sfx.append((fx[O + 'fx-pb.mov'][0] + 0.05, 'assets/sfx-whoosh.mp3', -7))
    sfx.append((fx[O + 'fx-towel.mov'][0] + 1.2, 'assets/sfx-sadtrombone.wav', -7))
    sfx.append((fx[O + 'fx-p3.mov'][0] + 0.45, 'assets/sfx-boom.mp3', -4))
    for k, (t, f, gdb) in enumerate(sfx, 1):
        ins += ['-i', f]; ms = int(t * 1000)
        fc.append(f'[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={gdb}dB,adelay={ms}|{ms}[s{k}]')
    # music bed under the HKC ad break (royalty-free workspace library), placeholder level until Ash's voiceover sits on it
    k = len(sfx) + 1; L = ad['o1'] - ad['o0']; ms = int(ad['o0'] * 1000); ins += ['-i', 'assets/music-bed.mp3']
    fc.append(f'[{k}:a]atrim=0:{L:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.8,afade=t=out:st={L - 1.2:.3f}:d=1.2,volume=-16dB,adelay={ms}|{ms}[s{k}]')
    sfx.append(None)
    fc.append('[base]' + ''.join(f'[s{k}]' for k in range(1, len(sfx) + 1)) + f'amix=inputs={len(sfx) + 1}:normalize=0:duration=first,alimiter=limit=0.95:level=false[a]')
    wav = f'{PD}/audio.wav'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-vn'] + ins + ['-filter_complex', ';'.join(fc), '-map', '[a]', '-c:a', 'pcm_s16le', wav], check=True)
    print('audio', dur(wav), 'expected', TM.TOTAL, flush=True)
    return wav

if __name__ == '__main__':
    todo = [p for p in TM.PIECES if not only or p['id'] in only]
    if '--skip-pieces' not in args:
        with ThreadPoolExecutor(2) as ex:
            list(ex.map(run_piece, sorted(todo, key=lambda p: -p['frames'])))
    if only:
        sys.exit(0)
    wav = audio()
    lst = f'{PD}/list.txt'
    open(lst, 'w').write(''.join(f"file '{os.path.abspath(PD)}/{p['id']}.mov'\n" for p in TM.PIECES))
    enc = (['-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-profile:v', 'high', '-level', '5.2', '-x264-params', 'keyint=50', '-pix_fmt', 'yuv420p']
           if FINAL else ['-c:v', 'h264_videotoolbox', '-b:v', '16M', '-pix_fmt', 'yuv420p'])
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-stats', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-i', wav, '-map', '0:v', '-map', '1:a']
                   + enc + ['-r', '25', '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', out], check=True)
    print('wrote', out, dur(out))
