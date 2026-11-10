"""Daytona MK TNL — 30 s vertical highlight reel (IG Reels / YT Shorts), 2160x3840.
Shots are cut straight from the clean onboard (assets/base-4k.mov, T = DJI seconds, base time = T - BASE0),
9:16-cropped around the action, slowed where it matters, joined with rotating xfades.
Graphics: one 1080x1920 HyperFrames overlay comp (gfx/index.html, rendered at 2x with alpha) built from the same shot table.
usage: reel.py gfx | draft | final [out.mp4]"""
import json, os, shutil, subprocess, sys
R = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(R); os.chdir(R)
WS = os.path.dirname(os.path.dirname(P))
BASE = P + '/assets/base-4k.mov'; BASE0 = 91141 / 25 - 3600
HKC_LOGO = os.path.expanduser('~/Documents/KARTING WEBSITE/hkl/site/public/brand/hkc-logo.png')
FPS, XD = 25, 0.24                       # xfade length

# id, T in, output secs, speed, crop centre x (0-1 of the 16:9 frame), zoom (>=1.12 keeps the burnt-in lap timer out), transition INTO this shot
SHOTS = [
    ('hook',   1154.70, 2.8, 0.5, 0.38, 1.12, None),
    ('green',   117.40, 2.0, 1.0, 0.50, 1.12, 'fadewhite'),
    ('launch',  120.00, 1.5, 1.0, 0.50, 1.12, 'hblur'),
    ('p1',      609.00, 2.4, 1.0, 0.60, 1.12, 'zoomin'),
    ('signal',  733.40, 1.8, 0.6, 0.33, 1.25, 'slideup'),
    ('over',    829.20, 1.7, 0.7, 0.32, 1.25, 'hblur'),
    ('spin',    958.10, 2.4, 0.5, 0.72, 1.12, 'zoomin'),
    ('pb',     1069.40, 2.0, 1.0, 0.50, 1.12, 'fadewhite'),
    ('look',   1198.95, 2.0, 0.5, 0.47, 1.30, 'smoothup'),
    ('lunge',  1237.30, 2.4, 0.75, 0.62, 1.12, 'hblur'),
    ('gone',   1244.40, 1.5, 1.0, 0.65, 1.12, 'zoomin'),
    ('fin',    1385.40, 2.2, 1.0, 0.50, 1.12, 'fadewhite'),
]
OUTRO = 7.5                              # HKC end card (opaque in the overlay; footage under it is the 'fin' shot frozen)

def timeline():
    t, out = 0.0, []
    for i, (sid, T, L, sp, cx, z, tr) in enumerate(SHOTS):
        st = t if i == 0 else t - XD
        out.append(dict(id=sid, T=T, len=L, speed=sp, cx=cx, z=z, tr=tr, start=round(st, 3)))
        t = st + L
    return out, round(t, 3)

SH, END = timeline()
TOTAL = round(END + OUTRO, 3)
S = {s['id']: s['start'] for s in SH}

# ---------------------------------------------------------------- footage
def shot_cmd(s, q, path):
    W, H = (2160, 3840) if q == 'final' else (1080, 1920)
    cw = 2160 * 9 / 16 / s['z']                                  # 1215 / z wide window of the 3840 frame
    ch = 2160 / s['z']
    cw, ch = int(cw) // 2 * 2, int(ch) // 2 * 2
    x = min(max(s['cx'] * 3840 - cw / 2, 0), 3840 - cw); y = 2160 - ch   # bottom-anchored: drops the lap-timer box burnt into the top-left of the base
    src = s['len'] * s['speed'] + 0.2
    vf = f'crop={cw}:{ch}:{x:.0f}:{y:.0f}'
    if s['speed'] < 1:
        vf += f',setpts=PTS/{s["speed"]},minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1'
    vf += f',scale={W}:{H}:flags=lanczos,eq=contrast=1.08:saturation=1.18,trim=0:{s["len"]},setpts=PTS-STARTPTS,format=yuv420p'
    return ['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f'{s["T"] - BASE0:.3f}', '-t', f'{src:.3f}', '-i', BASE, '-an', '-vf', vf,
            '-r', str(FPS), '-c:v', 'libx264', '-crf', '12' if q == 'final' else '16', '-preset', 'fast', path]

def footage(q):
    d = f'pieces-{q}'; os.makedirs(d, exist_ok=True)
    procs = []
    for s in SH:
        p = f'{d}/{s["id"]}.mp4'
        if not os.path.exists(p): procs.append(subprocess.Popen(shot_cmd(s, q, p)))
        if len(procs) >= 4: [x.wait() for x in procs]; procs = []
    [x.wait() for x in procs]
    # hold the last frame under the outro
    last = SH[-1]
    ins, fc, prev = [], [], '0:v'
    for i, s in enumerate(SH): ins += ['-i', f'{d}/{s["id"]}.mp4']
    for i, s in enumerate(SH[1:], 1):
        lab = f'x{i}'
        fc.append(f'[{prev}][{i}:v]xfade=transition={s["tr"]}:duration={XD}:offset={s["start"]:.3f}[{lab}]'); prev = lab
    fc.append(f'[{prev}]tpad=stop_mode=clone:stop_duration={OUTRO}[v]')
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', '[v]',
                    '-c:v', 'libx264', '-crf', '12' if q == 'final' else '16', '-preset', 'fast', '-r', str(FPS), f'{d}/seq.mp4'], check=True)
    return f'{d}/seq.mp4'

# ---------------------------------------------------------------- audio
SFX = WS + '/assets/sfx/'
def audio(q):
    """engine sound per shot (slow-mo shots pitched down with the footage), crossfaded like the picture;
    music bed under everything; whoosh into each cut, slams on the stamps, bass drop into the HKC card"""
    ins, fc, labs = [], [], []
    for i, s in enumerate(SH):
        ins += ['-ss', f'{s["T"] - BASE0:.3f}', '-t', f'{s["len"] * s["speed"] + 0.2:.3f}', '-i', BASE]
        a = f'[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo'
        if s['speed'] < 1: a += f',asetrate={48000 * s["speed"]:.0f},aresample=48000'
        fc.append(a + f',atrim=0:{s["len"]},asetpts=PTS-STARTPTS[e{i}]')
    prev = 'e0'
    for i in range(1, len(SH)):
        fc.append(f'[{prev}][e{i}]acrossfade=d={XD}:c1=tri:c2=tri[c{i}]'); prev = f'c{i}'
    fc.append(f'[{prev}]volume=-9dB,afade=t=out:st={END - 0.6:.3f}:d=0.8,apad=whole_dur={TOTAL}[eng]'); labs.append('[eng]')
    k = len(SH)
    def add(f, at, gain, extra=''):
        nonlocal k
        ins.extend(['-i', SFX + f]); ms = int(at * 1000)
        fc.append(f'[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={gain}dB{extra},adelay={ms}|{ms}[s{k}]'); labs.append(f'[s{k}]'); k += 1
    add('../music/music-bed-cinematic-tech.mp3', 0, -9, f',atrim=0:{TOTAL},afade=t=in:d=0.4,afade=t=out:st={TOTAL - 1.5}:d=1.5')
    add('impact/boom.mp3', 0.0, -8)
    for s in SH[1:]:
        add('transitions/whoosh.mp3', max(s['start'] - 0.12, 0), -12)
    add('impact/slam.mp3', S['p1'] + 1.0, -8)
    add('impact/slam.mp3', S['fin'] + 0.5, -7)
    add('cinematic/riser.mp3', END - 2.6, -14, ',afade=t=out:st=2.4:d=0.3')
    add('impact/bass-drop.mp3', END + 0.05, -5)
    fc.append(''.join(labs) + f'amix=inputs={len(labs)}:normalize=0:duration=longest,atrim=0:{TOTAL},alimiter=limit=0.93:level=false[a]')
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', '[a]',
                    '-c:a', 'pcm_s24le', f'pieces-{q}/mix.wav'], check=True)
    return f'pieces-{q}/mix.wav'

# ---------------------------------------------------------------- assemble
def build(q, out):
    seq = footage(q); mix = audio(q)
    ov = 'gfx/out4k.mov'
    W, H = (2160, 3840) if q == 'final' else (1080, 1920)
    fc = f'[1:v]scale={W}:{H}:flags=bicubic,format=yuva444p10le[o];[0:v][o]overlay=0:0:format=auto,format=yuv420p[v]'
    enc = (['-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-profile:v', 'high', '-level', '5.2'] if q == 'final'
           else ['-c:v', 'h264_videotoolbox', '-b:v', '14M'])
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-stats', '-y', '-i', seq, '-i', ov, '-i', mix, '-filter_complex', fc,
                    '-map', '[v]', '-map', '2:a'] + enc + ['-r', str(FPS), '-c:a', 'aac', '-b:a', '320k', '-t', f'{TOTAL}',
                    '-movflags', '+faststart', out], check=True)
    print('wrote', out, TOTAL, 's')

if __name__ == '__main__':
    q = sys.argv[1]
    if q == 'gfx':
        import gfx; gfx.write(SH, END, TOTAL, HKC_LOGO)
    else:
        build(q, sys.argv[2] if len(sys.argv) > 2 else f'renders/reel-{q}.mp4')
