"""Synthesize the overtake SFX (no downloads): cha-ching (gain a place) and game-show fail buzzer (lose a place)."""
import math, random, struct, wave
SR = 48000
def write(path, s):
    peak = max(abs(x) for x in s) or 1
    with wave.open(path, 'w') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b''.join(struct.pack('<hh', v, v) for v in (int(x / peak * 0.89 * 32767) for x in s)))
random.seed(7)
# cha-ching: "ka" (drawer clunk: noise burst + low knock) then two bright bell strikes
n = int(1.7 * SR); s = [0.0] * n
for i in range(n):
    t = i / SR; v = 0.0
    if t < 0.06: v += (random.random() * 2 - 1) * math.exp(-t * 70) * 0.7 + math.sin(2 * math.pi * 180 * t) * math.exp(-t * 50) * 0.6
    for t0, amp in ((0.09, 1.0), (0.17, 0.75)):
        u = t - t0
        if u >= 0:
            env = math.exp(-u * 3.0) * min(1, u / 0.002)
            v += amp * env * (0.55 * math.sin(2 * math.pi * 2093 * u) + 0.35 * math.sin(2 * math.pi * 3136 * u)
                              + 0.22 * math.sin(2 * math.pi * 4186 * u) + 0.12 * math.sin(2 * math.pi * 5280 * u)) * (1 + 0.2 * math.sin(2 * math.pi * 9 * u))
    s[i] = v
write('assets/sfx-chaching.wav', s)
# buzzer: detuned square waves, classic game-show "wrong answer"
n = int(1.0 * SR); s = [0.0] * n
sq = lambda f, t: 1.0 if math.sin(2 * math.pi * f * t) >= 0 else -1.0
prev = 0.0
for i in range(n):
    t = i / SR
    env = min(1, t / 0.012) * (1 if t < 0.88 else max(0, 1 - (t - 0.88) / 0.1))
    v = (sq(110, t) + 0.9 * sq(116.5, t) + 0.35 * sq(233, t)) * env
    prev += (v - prev) * 0.25          # gentle low-pass to take the fizz off
    s[i] = prev
write('assets/sfx-buzzer.wav', s)
print('ok')
# start-light beeps: three 1 kHz countdown beeps + a higher two-tone "go" beep (matches the reference's start sequence)
def tone(freqs, dur, amp=1.0):
    n = int(dur * SR); out = []
    for i in range(n):
        t = i / SR; env = min(1, t / 0.005) * min(1, (dur - t) / 0.02)
        out.append(amp * env * sum(a * math.sin(2 * math.pi * f * t) for f, a in freqs))
    return out
write('assets/sfx-beep.wav', tone([(1000, 0.8), (2000, 0.12)], 0.16))
write('assets/sfx-go.wav', tone([(1650, 0.7), (1240, 0.45), (3300, 0.08)], 0.5))
print('beeps ok')
# "you've been hit" (shooter-game style, synthesized): body thump + noise crack + hit-marker tick + short ear-ring
random.seed(21)
n = int(1.6 * SR); s = [0.0] * n; lp = 0.0
for i in range(n):
    t = i / SR; v = 0.0
    f = 95 * math.exp(-t * 9) + 45                                        # pitch-dropping thump
    v += math.sin(2 * math.pi * f * t) * math.exp(-t * 11) * 1.0
    nz = random.random() * 2 - 1; lp += (nz - lp) * 0.35
    v += lp * math.exp(-t * 38) * 0.9                                     # crack
    if t < 0.03: v += math.sin(2 * math.pi * 2600 * t) * math.exp(-t * 120) * 0.5   # hit-marker tick
    if t > 0.05: v += math.sin(2 * math.pi * 3150 * t) * math.exp(-(t - 0.05) * 2.6) * min(1, (t - 0.05) / 0.08) * 0.13  # ring
    s[i] = v
write('assets/sfx-hit.wav', s)
# sad trombone "wah wah wah wahhh" (four descending notes, last one wobbling), brassy saw stack
notes = [(0.0, 0.42, 293.7), (0.45, 0.42, 277.2), (0.9, 0.42, 261.6), (1.35, 1.25, 246.9)]
n = int(2.7 * SR); s = [0.0] * n; lp = 0.0
for i in range(n):
    t = i / SR; v = 0.0
    for t0, d, f in notes:
        u = t - t0
        if 0 <= u < d:
            env = min(1, u / 0.05) * min(1, (d - u) / 0.12)
            ff = f * (1 - 0.025 * math.exp(-u * 12)) * (1 + (0.022 * math.sin(2 * math.pi * 6 * u) if d > 1 else 0))
            ph = (ff * u) % 1.0
            v += env * (2 * ph - 1) * (0.6 + 0.4 * min(1, u / 0.15))
    lp += (v - lp) * 0.18
    s[i] = lp
write('assets/sfx-sadtrombone.wav', s)
print('hit + trombone ok')
