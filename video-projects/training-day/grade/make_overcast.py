"""Overcast variant of the Apexx look: same filmic base, plus strong highlight roll-off to bring detail and tone back
into a white sky, a little density in the mids, and extra saturation for greens/blues (skin protected)."""
import math
exec(open('make_lut.py').read().split("write('apexx_cine.cube'")[0])
def over(r, g, b):
    r, g, b = look(r, g, b, 1.15, 1.0, 0.8)
    l = 0.2126 * r + 0.7152 * g + 0.0722 * b
    # highlight roll-off on luma: compress above 0.55
    if l > 0.55:
        nl = 0.55 + (l - 0.55) * 0.58
        k = nl / l; r, g, b = r * k, g * k, b * k; l = nl
    # density: slight gamma on mids
    r, g, b = (max(v, 0) ** 1.06 for v in (r, g, b)); l = 0.2126 * r + 0.7152 * g + 0.0722 * b
    # selective saturation: greens/blues/cyans up, skin (r>g>b) protected
    skin = r > g > b and (r - b) > 0.04
    s = 1.06 if skin else 1.32
    r, g, b = l + (r - l) * s, l + (g - l) * s, l + (b - l) * s
    # subtle cool tint into the brightest areas so the sky reads grey-blue not white
    hi = max(0.0, (l - 0.5) / 0.5)
    r -= 0.025 * hi; b += 0.03 * hi
    return [min(max(v, 0.0), 1.0) for v in (r, g, b)]
with open('apexx_cine_overcast.cube', 'w') as f:
    f.write(f'TITLE "Apexx Cine Overcast"\nLUT_3D_SIZE {N}\n')
    for bi in range(N):
        for gi in range(N):
            for ri in range(N):
                f.write('%.6f %.6f %.6f\n' % tuple(over(ri / (N - 1), gi / (N - 1), bi / (N - 1))))
print('ok')
