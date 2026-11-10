"""Cinematic look LUT for Rec.709 phone/DJI footage: filmic S-curve with soft highlight roll-off and lifted-but-dense
blacks, subtle teal shadows / warm highlights split-tone, gentle saturation with skin-tone protection."""
import math, sys
N = 33
def curve(x, k=1.0):
    # filmic S: toe + shoulder; k scales contrast
    x = min(max(x, 0.0), 1.0)
    s = 1 / (1 + math.exp(-(x - 0.5) * 6.2 * k)); s0 = 1 / (1 + math.exp(3.1 * k)); s1 = 1 / (1 + math.exp(-3.1 * k))
    y = (s - s0) / (s1 - s0)
    y = 0.62 * y + 0.38 * x          # blend back so it's not crushed
    return 0.018 + y * (0.975 - 0.018)  # black lift / highlight roll-off
def look(r, g, b, k, sat, split):
    r, g, b = curve(r, k), curve(g, k), curve(b, k)
    l = 0.2126 * r + 0.7152 * g + 0.0722 * b
    # skin protection: hue near orange keeps saturation boost lower
    mx, mn = max(r, g, b), min(r, g, b)
    skin = 1.0 if (r > g > b and (r - b) > 0.05 and (g - b) / (r - b + 1e-6) > 0.25) else 0.0
    s = sat * (1 - 0.6 * skin) + 1.0 * (0.6 * skin) if skin else sat
    r, g, b = l + (r - l) * s, l + (g - l) * s, l + (b - l) * s
    # split tone: shadows toward teal, highlights toward warm
    sh = max(0.0, 1 - l / 0.45) ** 2; hi = max(0.0, (l - 0.55) / 0.45) ** 1.5
    r += split * (-0.018 * sh + 0.022 * hi); g += split * (0.004 * sh + 0.008 * hi); b += split * (0.020 * sh - 0.026 * hi)
    return [min(max(v, 0.0), 1.0) for v in (r, g, b)]
def write(path, k, sat, split, title):
    with open(path, 'w') as f:
        f.write(f'TITLE "{title}"\nLUT_3D_SIZE {N}\n')
        for bi in range(N):
            for gi in range(N):
                for ri in range(N):
                    r, g, b = look(ri / (N - 1), gi / (N - 1), bi / (N - 1), k, sat, split)
                    f.write(f'{r:.6f} {g:.6f} {b:.6f}\n')
write('apexx_cine.cube', 1.0, 1.10, 1.0, 'Apexx Cine')          # main look
write('apexx_cine_soft.cube', 0.6, 1.04, 0.7, 'Apexx Cine Soft')  # for already-graded renders
write('apexx_cine_punch.cube', 1.25, 1.16, 1.1, 'Apexx Cine Punch')  # flat overcast footage
print('ok')
