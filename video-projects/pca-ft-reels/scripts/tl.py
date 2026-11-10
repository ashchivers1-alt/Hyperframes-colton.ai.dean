"""Ash's Resolve 'PCA FT' Timeline 1 as source ranges -> map timeline seconds to (file, source seconds)."""
FPS = 24000 / 1001
A = {1: 'assets/DJI_20261101143043_0001_D.MP4', 2: 'assets/DJI_20261101145020_0002_D.MP4', 3: 'assets/DJI_20261101150314_0003_D.MP4'}
SEGS = [(1,0,983),(2,0,400),(3,352,698),(3,1196,1421),(3,1692,1921),(3,2110,2301),(3,2703,2937),(3,3022,3279),
        (3,4416,4581),(3,9387,10768),(3,10768,10860),(3,6379,6943),(3,15027,15266),(3,12152,12774),(3,12802,13360)]
TL = []   # (tl_start_frame, tl_end_frame, file, src_start_frame)
_t = 0
for c, a, b in SEGS:
    TL.append((_t, _t + b - a, A[c], a)); _t += b - a

def seg_of(tf):
    for i, (s, e, f, a) in enumerate(TL):
        if s <= tf < e: return i
    raise ValueError(tf)

def split(t0, t1):
    """timeline seconds -> list of (file, src_start_frame, n_frames, tl_start_frame) not crossing Ash's cuts"""
    f0, f1, out = round(t0 * FPS), round(t1 * FPS), []
    while f0 < f1:
        i = seg_of(f0); s, e, f, a = TL[i]; n = min(f1, e) - f0
        out.append((f, a + f0 - s, n, f0)); f0 += n
    return out
