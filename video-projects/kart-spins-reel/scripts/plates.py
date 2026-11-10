"""Render vertical plates from the 4K onboard: play (lead-up + spin, normal speed) and wasted (slow-mo, desat, push-in)."""
import subprocess, sys
SRC = '/Volumes/SD_Card/DCIM/CAM_001/CAM_20261020211207_0003_D.MP4'
# a = lead-up start, h = loses control, s = spin settles  (absolute source seconds, frame-aligned @25)
INC = [dict(a=236.84, h=238.84, s=240.16), dict(a=380.28, h=382.28, s=383.88), dict(a=497.92, h=499.92, s=501.52)]
VERT = ("split[a][b];[a]scale=-2:1920,crop=1080:1920,gblur=sigma=34,eq=brightness=-0.10:saturation=0.8[bg];"
        "[b]scale=1400:788:flags=lanczos[fg];[bg][fg]overlay=x=-160:y=566")
PR = ['-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le', '-an']
def run(args): subprocess.run(['ffmpeg', '-v', 'error', '-y'] + args, check=True)
which = sys.argv[1] if len(sys.argv) > 1 else 'all'
for i, c in enumerate(INC, 1):
    last = i == len(INC)
    if which in ('all', 'play'):
        n = round((c['s'] - c['a']) * 25)
        run(['-ss', f"{c['a']:.2f}", '-i', SRC, '-frames:v', str(n), '-filter_complex', f"[0:v]scale=1920:1080:flags=lanczos,{VERT}", *PR, f'plates/play{i}.mov'])
    if which in ('all', 'wasted'):
        frames = 70 if last else 55          # last one holds a little longer
        slow = 55                            # frames of slow-mo; remainder freezes
        f = (f"[0:v]scale=1920:1080:flags=lanczos,minterpolate=fps=83.333:mi_mode=mci:mc_mode=aobmc:me_mode=bidir,"
             f"setpts=(PTS-STARTPTS)*3.33333,fps=25,trim=end_frame={slow},tpad=stop_mode=clone:stop={frames-slow},{VERT},"
             f"hue=s='max(0,1-t/0.45)',eq=brightness='-0.07*min(1,t/0.45)':contrast='1+0.12*min(1,t/0.45)':eval=frame,"
             f"zoompan=z='1+0.07*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=25,vignette=PI/4.5")
        run(['-ss', f"{c['s']:.2f}", '-t', '0.8', '-i', SRC, '-filter_complex', f, '-frames:v', str(frames), *PR, f'plates/wasted{i}.mov'])
    print('done', i, flush=True)
