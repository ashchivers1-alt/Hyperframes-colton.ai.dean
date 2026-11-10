"""Per-incident kart audio: play section (ducked around the hitmarker) + wasted section (slowed/pitched-down, ducked under the sting)."""
import subprocess
SRC = '/Volumes/SD_Card/DCIM/CAM_001/CAM_20261020211207_0003_D.MP4'
INC = [dict(a=236.84, h=238.84, s=240.16), dict(a=380.28, h=382.28, s=383.88), dict(a=497.92, h=499.92, s=501.52)]
BASE = -5.0   # dB: ~-9 LUFS source -> ~-14 LUFS so the full mix lands near -14 LUFS for Reels
def run(a): subprocess.run(['ffmpeg', '-v', 'error', '-y'] + a, check=True)
for i, c in enumerate(INC, 1):
    P = c['s'] - c['a']; d = c['h'] - c['a']
    # dip to ~-7 dB for the hitmarker: 40 ms down, hold, 120 ms back
    duck = f"1-0.55*max(0,min(1,min((t-{d-0.05:.3f})/0.04,({d+0.40:.3f}-t)/0.12)))"
    run(['-ss', f"{c['a']:.2f}", '-t', f"{P:.2f}", '-i', SRC, '-map', '0:a:0',
         '-af', f"volume={BASE}dB,volume='{duck}':eval=frame,afade=t=in:d=0.02,afade=t=out:st={P-0.02:.2f}:d=0.02,alimiter=limit=0.8:level=false", '-ar', '48000', '-c:a', 'pcm_s24le', f'audio/kart_play{i}_v2.wav'])
    W = 2.8 if i == len(INC) else 2.2
    # slowed 0.3x like the picture; sits ~-12 dB under once the sting lands (0.32 s in)
    g = f"1-0.75*min(1,max(0,(t-0.25)/0.1))"
    run(['-ss', f"{c['s']:.2f}", '-t', '1.0', '-i', SRC, '-map', '0:a:0',
         '-af', f"asetrate=48000*0.3,aresample=48000,lowpass=f=4000,volume={BASE+2}dB,volume='{g}':eval=frame,atrim=end={W},afade=t=out:st={W-0.5:.2f}:d=0.5,alimiter=limit=0.8:level=false",
         '-ar', '48000', '-c:a', 'pcm_s24le', f'audio/kart_wasted{i}_v2.wav'])
print('ok')
