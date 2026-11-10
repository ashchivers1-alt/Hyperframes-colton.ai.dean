"""Original 'wasted'-style music sting: dark D-minor synth chord with a tape-stop pitch sag. Pure Python, writes 48k stereo."""
import math, struct, wave, sys
SR, DUR = 48000, 2.6
notes = [73.42, 110.0, 146.83, 174.61, 220.0, 293.66]      # D2 A2 D3 F3 A3 D4
amps  = [0.9, 0.55, 0.6, 0.45, 0.4, 0.22]
detune = [0.0, 0.004, -0.003, 0.005, -0.004, 0.003]
out = []
ph = [[0.0]*6 for _ in notes]                               # 6 harmonics per voice
for n in range(int(SR*DUR)):
    t = n / SR
    sag = 1.0 - 0.09 * (1 - math.exp(-t / 0.9))             # pitch sags ~1.5 semitones
    env = min(1.0, t / 0.05) * math.exp(-t / 1.25)
    s = 0.0
    for v, f0 in enumerate(notes):
        f = f0 * sag * (1 + detune[v])
        for h in range(6):
            ph[v][h] += 2 * math.pi * f * (h + 1) / SR
            s += amps[v] * math.sin(ph[v][h]) / (h + 1) ** 1.3
    out.append(s * env)
peak = max(abs(x) for x in out)
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(b''.join(struct.pack('<hh', int(x / peak * 30000), int(x / peak * 30000)) for x in out))
