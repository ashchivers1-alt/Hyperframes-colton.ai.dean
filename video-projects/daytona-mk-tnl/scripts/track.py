"""Centre line of the circuit from the lap-timer overlay's map dot (src/dot.json, one lap at 10 Hz),
rotated so index 0 is the start/finish line, smoothed, resampled to N points by arc length -> src/track.json."""
import json, math
d = [x for x in json.load(open('src/dot.json')) if x[1] is not None]
LAP = 78.4; SF = 237.7
p = [(x, y) for t, x, y in d if t < 200 + LAP]
i0 = min(range(len(p)), key=lambda i: abs(d[i][0] - SF)); p = p[i0:] + p[:i0]
def smooth(p, k):
    n = len(p); return [(sum(p[(i + j) % n][0] for j in range(-k, k + 1)) / (2 * k + 1),
                         sum(p[(i + j) % n][1] for j in range(-k, k + 1)) / (2 * k + 1)) for i in range(n)]
p = smooth(smooth(p, 3), 3)
seg = [math.hypot(p[(i + 1) % len(p)][0] - p[i][0], p[(i + 1) % len(p)][1] - p[i][1]) for i in range(len(p))]
L = sum(seg); N = 600; out = []; acc = 0; j = 0
for k in range(N):
    s = L * k / N
    while acc + seg[j] < s: acc += seg[j]; j += 1
    f = (s - acc) / seg[j] if seg[j] else 0; a, b = p[j], p[(j + 1) % len(p)]
    out.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
xs, ys = [q[0] for q in out], [q[1] for q in out]
cx, cy, sc = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, max(max(xs) - min(xs), max(ys) - min(ys))
norm = [(round((x - cx) / sc, 5), round((y - cy) / sc, 5)) for x, y in out]
json.dump({'pts': norm, 'aspect': (max(ys) - min(ys)) / (max(xs) - min(xs))}, open('src/track.json', 'w'))
print('px length', round(L), 'bbox', round(max(xs) - min(xs)), round(max(ys) - min(ys)))
