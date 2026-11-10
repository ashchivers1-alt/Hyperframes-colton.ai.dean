"""Clean dialogue per timeline item: extract the item's exact source range, denoise + EQ + compress + level.
Writes audio/dlg_<idx>.wav (48k stereo, 24-bit). Source files are only read."""
import json, subprocess, sys
TL = json.load(open('/private/tmp/claude-501/-Users-ashleychivers-Documents-Claude-Video-Studio/88a5434b-e5ee-441f-8a31-409b07c3b15a/scratchpad/italy_tl.json'))
items = {i['item_index']: i for i in TL['tracks']['video']['tracks'][0]['items']}

RNN = 'src/rnn/bd.rnnn'
# v2: blend the denoiser with the dry signal (full-strength RNNoise gates between words = choppy),
# softer presence boost, gentle slow compression instead of leaning on the brick-wall limiter
VOICE = ("highpass=f={hp},aresample=48000,arnndn=m=" + RNN + ":mix={mix},equalizer=f=170:t=q:w=1.0:g=1.5,"
         "equalizer=f=420:t=q:w=1.4:g=-2,equalizer=f=3200:t=q:w=1.0:g=2,"
         "acompressor=threshold=-20dB:ratio=2:attack=20:release=300:knee=6:makeup=1")
LEVEL = "highpass=f=40"
VOICE_OUT = VOICE.replace(':mix={mix},', ':mix={mix},afftdn=nr=8:nf=-38,')
TARGET = {'voice': -16.0}
# item -> (mode, params)
PLAN = {}
for i in (0, 1, 5, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 28, 29, 30, 31, 32, 35, 36):
    PLAN[i] = ('voice', dict(hp=80, mix=0.5))
for i in (3, 4):                      # noisy cafe
    PLAN[i] = ('voice', dict(hp=90, mix=0.7))
for i in (44,):                       # outdoors at night
    PLAN[i] = ('voice', dict(hp=90, mix=0.6))
for i in (11, 12):                    # outdoors, steady traffic/wind: add a stationary-noise pass
    PLAN[i] = ('voice_out', dict(hp=100, mix=0.65))
for i in (13, 14, 15, 26, 27):        # gym ambience under music
    PLAN[i] = ('level', dict(I=-28.0))
for i in (10,):
    PLAN[i] = ('level', dict(I=-24.0))
for i in range(37, 44):               # stage audio: announcer + venue music
    PLAN[i] = ('level', dict(I=-18.0))

def run(a): subprocess.run(['ffmpeg', '-v', 'error', '-y'] + a, check=True)
only = set(int(x) for x in sys.argv[1:]) if len(sys.argv) > 1 else None
for idx, (mode, p) in PLAN.items():
    if only and idx not in only: continue
    it = items[idx]; fps = it['source_fps']
    fps = 24000 / 1001 if abs(fps - 23.976) < 0.01 else fps
    ss = it['source_start'] / fps; dur = (it['source_end'] - it['source_start']) / fps
    af = {'voice': VOICE, 'voice_out': VOICE_OUT, 'level': LEVEL}[mode].format(**p)
    tmp = f'audio/_tmp_{idx:02d}.wav'
    run(['-ss', f'{ss:.4f}', '-t', f'{dur:.4f}', '-i', it['file_path'], '-map', '0:a:0', '-af', af + ',aresample=48000',
         '-ac', '2', '-c:a', 'pcm_s24le', tmp])
    # fixed gain to the target loudness (no dynamic levelling, so the noise floor isn't pumped up), then a limiter
    o = subprocess.run(['ffmpeg', '-nostats', '-i', tmp, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(o[o.rindex('I:'):].split()[1])
    tgt = TARGET['voice'] if mode.startswith('voice') else p['I']
    g = max(-30, min(30, tgt - I))
    run(['-i', tmp, '-af', f'volume={g:.2f}dB,alimiter=limit=0.89:attack=4:release=120:level=false,afade=t=in:d=0.02,afade=t=out:st={max(0, dur - 0.03):.3f}:d=0.03',
         '-c:a', 'pcm_s24le', f'audio/v2/dlg_{idx:02d}.wav'])
    import os; os.remove(tmp)
    print(idx, mode, f'{dur:.2f}s', flush=True)
