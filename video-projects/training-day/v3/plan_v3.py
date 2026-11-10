"""Edit v3 — cinematic training reel with talk inserts.

Units play in order. Each unit: (kind, clip, in, out, opts)
  kind 'reel'  -> muted, graded, beat-snapped length, dissolve in/out
  kind 'talk'  -> audio on (funny / review / coaching), dissolve in/out
Talk units listed with 'gaps' get interior pauses removed (jump cuts, alternating punch-in).
Output: units.json with timeline start/end per unit, plus a source->output time map
for the overlay timing (ingredient ticks, coaching cues).
"""
import json, math, wave, struct

BEAT = 0.47922        # Gym Phonk (Sub_Clair) ~125 BPM, beat 0 aligned to output t=0
XF = 0.333            # dissolve length (10 frames)
FPS = 30

def env(c, hop=0.05, cache={}):
    if c not in cache:
        w = wave.open(f'../audio/{c}.wav'); sr = w.getframerate(); n = w.getnframes()
        d = struct.unpack(f"<{n}h", w.readframes(n)); h = int(sr * hop)
        cache[c] = [20 * math.log10(math.sqrt(sum(x * x for x in d[i:i + h]) / h) / 32768 + 1e-9) for i in range(0, n - h, h)]
    return cache[c]

def gaps(c, a, b, minlen=0.7, keep=0.25):
    e = env(c); s = sorted(e); p20 = s[len(s) // 5]; p60 = s[len(s) * 3 // 5]; thr = p20 + 0.45 * (p60 - p20)
    out = []; run = None
    for i in range(int(a / 0.05), int(b / 0.05)):
        if e[i] < thr:
            run = i if run is None else run
        else:
            if run is not None and (i - run) * 0.05 >= minlen and run * 0.05 > a + 0.3:
                out.append((round(run * 0.05 + keep, 2), round(i * 0.05 - keep, 2)))
            run = None
    return out

R = 'reel'; T = 'talk'
UNITS = [
    # --- open: LEG DAY ---
    (R, 'SLOWEXT', 0.0, 4.4, {'tag': 'exterior', 'nobeat': True}),
    (R, 'c0006', 0.0, 6.6, {'tag': 'walkin', 'title': 'legday'}),
    (T, 'c0012', 12.6, 16.3, {'tag': 'moan'}),
    (R, 'c0002', 4.3, 9.55, {'tag': 'mixing'}),
    (T, 'c0002', 39.9, 41.15, {'tag': 'trysome'}),   # her 'not really, no' cut at Ash's request
    (T, 'c0007', 0.0, 99.7, {'tag': 'review', 'gaps': True}),
    # 99.7-107.95 removed at Ash's request: 'it's got a kick to it ... it's very thick'
    (T, 'c0007', 107.95, 111.1, {'tag': 'review2', 'hardin': True}),
    # --- glute activation ---
    (R, 'c0003', 2.0, 4.7, {'tag': 'act1', 'title': 'activation'}),
    (R, 'c0003', 9.0, 11.7, {'tag': 'act2'}),
    # --- standing abductor ---
    (T, 'c0005', 24.3, 41.55, {'tag': 'moccasins'}),
    (R, 'c0004', 59.0, 62.0, {'tag': 'abd1', 'title': 'abductor'}),
    (R, 'c0005', 50.0, 53.0, {'tag': 'abd2'}),
    (R, 'c0004', 81.0, 84.0, {'tag': 'abd3'}),
    (R, 'c0005', 125.8, 129.0, {'tag': 'abd4'}),
    # --- hip thrust ---
    (R, 'c0009', 41.0, 44.0, {'tag': 'ht1', 'title': 'hipthrust'}),
    (R, 'c0009', 45.0, 48.0, {'tag': 'ht2'}),
    (T, 'c0008', 24.75, 31.3, {'tag': 'warmup', 'zoom': 1.12}),
    (R, 'c0010', 100.0, 103.0, {'tag': 'ht3'}),
    (R, 'c0011', 283.5, 286.5, {'tag': 'ht4'}),
    (T, 'c0009', 88.6, 113.15, {'tag': 'skiddy'}),
    (R, 'c0011', 288.5, 291.5, {'tag': 'ht5'}),
    (T, 'c0011', 299.15, 323.35, {'tag': 'ruined', 'zoom': 1.12}),
    # --- glute-focused single-leg press (coaching) ---
    # c0013 removed: different leg press machine to the one used in the set
    (T, 'c0014', 0.0, 38.9, {'tag': 'edu1', 'gaps': True, 'title': 'legpress'}),
    # 38.9-46.35 removed at Ash's request: 'How does it feel? - feeling it in here' (points to quad)
    (T, 'c0014', 46.35, 59.8, {'tag': 'edu1b', 'gaps': True, 'hardin': True}),
    (T, 'c0014', 61.9, 82.2, {'tag': 'edu2', 'gaps': True, 'hardin': True}),
    # --- glute-bias single-leg machine squat ---
    (R, 'c0017', 33.0, 36.5, {'tag': 'sq1', 'title': 'slmsquat'}),
    (R, 'c0017', 44.0, 47.5, {'tag': 'sq2'}),
    # --- sumo belt squat ---
    (R, 'c0018', 2.5, 6.0, {'tag': 'bs1', 'title': 'beltsquat'}),
    (R, 'c0018', 24.5, 28.0, {'tag': 'bs2'}),
    # --- glute press ---
    (R, 'c0019', 10.0, 13.3, {'tag': 'gp1', 'title': 'glutepress'}),
    (R, 'c0020', 41.0, 44.3, {'tag': 'gp2'}),
    (R, 'c0021', 12.0, 15.3, {'tag': 'gp3'}),
    (R, 'c0019', 40.0, 43.3, {'tag': 'gp4'}),
    # --- outro ---
    (R, 'c0022', 0.0, 4.8, {'tag': 'outro', 'nobeat': True, 'last': True})   # muted: client talking; music + JOB DONE text,
]

units = []; t = 0.0; prev = None
for kind, c, a, b, o in UNITS:
    pieces = [(a, b)]
    if o.get('gaps'):
        pieces = []; cur = a
        for g0, g1 in gaps(c, a, b):
            if g1 - g0 > 0.1: pieces.append((cur, g0)); cur = g1
        pieces.append((cur, b))
    dur = sum(p1 - p0 for p0, p1 in pieces)
    xf_in = 0.0 if prev is None or o.get('hardin') else XF
    if kind == R and not o.get('nobeat'):
        # snap so the dissolve centre into the NEXT unit lands on a beat
        start = t - xf_in
        end_target = start + dur
        k = math.floor((end_target - XF / 2) / BEAT)
        dur = round(k * BEAT + XF / 2 - start, 3)
        dur = min(dur, b - a)
        pieces = [(a, a + dur)]
    start = round(t - xf_in, 3)
    u = dict(kind=kind, clip=c, pieces=pieces, dur=round(dur, 3), start=start, end=round(start + dur, 3), xf_in=xf_in, **o)
    units.append(u); t = start + dur; prev = u

total = round(units[-1]['end'], 3)
json.dump(dict(units=units, total=total, beat=BEAT, xf=XF), open('units.json', 'w'), indent=1)

def src_to_out(tag, src):
    u = next(x for x in units if x['tag'] == tag); acc = u['start']
    for p0, p1 in u['pieces']:
        if src < p0: return round(acc, 3)
        if src <= p1: return round(acc + src - p0, 3)
        acc += p1 - p0
    return round(acc, 3)

if __name__ == '__main__':
    for u in units:
        print(f"{u['start']:7.2f}-{u['end']:7.2f} {u['kind']:4} {u['clip']} {u['tag']:10} pieces={len(u['pieces'])} dur={u['dur']}")
    print('TOTAL', total, 's =', f"{int(total // 60)}:{total % 60:05.2f}")
