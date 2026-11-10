"""eyes.json -> eyes_smooth.json: bridge short dropouts, centred moving average (pos 9 frames, size 31), fade strength in/out at gaps."""
import json, sys
J = json.load(open(sys.argv[1])); E = J['eyes']; n = len(E)
ok = [e is not None and e[6] > 0.3 for e in E]
# reject jumps: eye width outliers vs median
ws = sorted(e[2] + e[5] for e, o in zip(E, ok) if o); med = ws[len(ws) // 2]
ok = [o and 0.6 * med < E[i][2] + E[i][5] < 1.6 * med for i, o in enumerate(ok)]
# fill gaps <= 20 frames by linear interpolation
F = [list(E[i][:6]) if ok[i] else None for i in range(n)]
i = 0
while i < n:
    if F[i] is None:
        j = i
        while j < n and F[j] is None: j += 1
        if 0 < i and j < n and j - i <= 20:
            a, b = F[i - 1], F[j]
            for k in range(i, j): t = (k - i + 1) / (j - i + 1); F[k] = [x + (y - x) * t for x, y in zip(a, b)]
        i = j
    else: i += 1
def smooth(idx, win):
    out = [None] * n
    for i in range(n):
        if F[i] is None: continue
        vs = [F[k][idx] for k in range(max(0, i - win // 2), min(n, i + win // 2 + 1)) if F[k] is not None]
        out[i] = sum(vs) / len(vs)
    return out
S = [smooth(k, 31 if k in (2, 5) else 9) for k in range(6)]
# strength ramps 0->1 over 12 frames at the edges of tracked runs
st = [0.0] * n
for i in range(n):
    if F[i] is None: continue
    d = 0
    while d < 12 and 0 <= i - d - 1 and F[i - d - 1] is not None and i + d + 1 < n and F[i + d + 1] is not None: d += 1
    st[i] = (d + 1) / 13 if d < 12 else 1.0
out = [None if F[i] is None else [S[k][i] for k in range(6)] + [st[i]] for i in range(n)]
J['eyes'] = out; json.dump(J, open(sys.argv[2], 'w'))
print('frames', n, 'tracked', sum(o is not None for o in out), 'raw ok', sum(ok), 'median eye width', round(med / 2))
