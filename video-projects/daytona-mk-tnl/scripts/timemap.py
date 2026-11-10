"""Source time (T = DJI/timeline seconds) -> output time, for the trimmed + slow-mo + freeze-frame cut.
Pieces cover [start, end] back to back: normal-speed runs between the effect segments in src/race.json.
Every boundary snaps to the 25 fps frame grid so pieces concatenate with exact frame counts."""
import json, os
FPS = 25
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = json.load(open(P + '/src/race.json'))

def snap(t):
    return round(t * FPS) / FPS

def pieces():
    out, T, o = [], snap(R['start']), 0.0
    for s in sorted(R['segs'], key=lambda s: s['t0']):
        a, b = snap(s['t0']), snap(s['t1'])
        if a > T:
            out.append(dict(id=f'run{len(out)}', t0=T, t1=a, speed=1.0, o0=o, frames=round((a - T) * FPS))); o += (a - T)
        n = round((b - a) / s['speed'] * FPS) + round(s.get('freeze', 0) * FPS) + round(s.get('insert', 0) * FPS)   # insert = outside footage, source clock stops
        out.append(dict(s, t0=a, t1=b, o0=o, frames=n)); o += n / FPS; T = b
    end = snap(R['end'])
    out.append(dict(id=f'run{len(out)}', t0=T, t1=end, speed=1.0, o0=o, frames=round((end - T) * FPS)))
    for p in out:
        p['o1'] = p['o0'] + p['frames'] / FPS
    return out

PIECES = pieces()
SEG = {p['id']: p for p in PIECES}
TOTAL = PIECES[-1]['o1']

def out(T):
    """output seconds for source time T (inside a freeze, the freeze starts at the segment's t1)"""
    for p in PIECES:
        if p['t0'] <= T <= p['t1']:
            return p['o0'] + (T - p['t0']) / p['speed']
    raise ValueError(T)

if __name__ == '__main__':
    for p in PIECES:
        print(f"{p['id']:8} T {p['t0']:8.2f}-{p['t1']:8.2f}  out {p['o0']:8.2f}-{p['o1']:8.2f}  x{p['speed']}  {p['frames']}f")
    print('total', TOTAL)
