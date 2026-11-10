"""Show-day section (after the training) -> show_edl.json.
Ash's Resolve layout (Edit 02, 2026-11-09) is the source: car talk (c15), motorway (c16, sped up), Nick-done talk (c17),
morning-after walk (c01 = IMG_3801, eye-bag retouched). B-roll ranges are Ash's; timings land on the transcript words.
All times are timeline seconds from the start of the whole video; 'src' times are seconds into each source file."""
import json
FPS = 24000 / 1001
EDL = json.load(open('edl.json'))
S0 = round((EDL[-1]['rec'] + EDL[-1]['dur']))          # first frame of the show section (timeline frames)
DJI = '/Volumes/Untitled/DCIM/DJI_001/'
SRC = {'c15': DJI + 'DJI_20261108093859_0015_D.MP4', 'c16': DJI + 'DJI_20261108094057_0016_D.MP4',
       'c17': DJI + 'DJI_20261108162434_0017_D.MP4', 'c01': 'show/IMG_3801_rt.mov'}
DRIVE_SPEED = 3.0
SEGS = [('c15', 2.84, 111.86, 1.0), ('c16', 17.73, 45.05, DRIVE_SPEED), ('c17', 1.38, 156.78, 1.0), ('c01', 0.0, 175.31, 1.0)]

segs, rec = [], S0
for c, a, b, sp in SEGS:
    n = round((b - a) / sp * FPS)
    segs.append(dict(clip=c, file=SRC[c], src_start=a, src_end=b, speed=sp, rec=rec, frames=n)); rec += n
END = rec

def T(clip, src):
    """source second in a talk clip -> timeline seconds"""
    s = next(s for s in segs if s['clip'] == clip)
    return s['rec'] / FPS + (src - s['src_start']) / s['speed']

# full-screen B-roll: (file, src_in, src_out, timeline_start). Ash's ranges, butted together unless he left a gap back to camera.
BR = 'show/sdr/'
broll = []
def run(f, ranges, t):
    for a, b in ranges:
        broll.append(dict(file=BR + f, src_in=a, src_out=b, t=t)); t += b - a
    return t
run('IMG_3767.mov', [(3.70, 9.31), (13.80, 17.86), (21.13, 35.66)], T('c17', 25.0))            # Nick's line-up, "footage ... on the screen now"
run('IMG_3768.mov', [(28.82, 33.42), (52.58, 57.48)], T('c17', 63.0))                         # routine, full screen after the card
for a, b, at in [(6.25, 12.48, 68.90), (19.22, 24.49, 77.24), (24.52, 35.05, 82.51), (44.53, 49.35, 96.05), (61.47, 65.40, 102.56), (67.32, 76.22, 109.15)]:
    broll.append(dict(file=BR + 'IMG_3784.mov', src_in=a, src_out=b, t=T('c01', at)))         # Mark's line-up, exactly where Ash put it

# designed pieces (hyperframes comps, gfx/show.py): name -> (start, end) timeline seconds
designed = {
    'x_progress':   (T('c15', 56.4), T('c15', 71.2)),     # THEN (burger) vs NOW (backstage video), full screen
    'x_vertical':   (T('c15', 80.0), T('c15', 89.58)),    # backstage video full screen, blurred fill
    'x_routine':    (T('c17', 49.2), T('c17', 63.0)),     # posing routine in a floating card over Ash
    'x_compare':    (T('c17', 111.5), T('c17', 127.4)),   # day one vs show day photos, full screen
    'x_mark_card':  (T('c01', 62.0), T('c01', 68.9)),     # Mark's line-up in a card, before the full-screen run
    'x_mark_photo': (T('c01', 118.7), T('c01', 124.6)),   # Mark + Ash photo, polaroid
}
cuts = [s['rec'] / FPS for s in segs]                   # wipes sit on these (first = training -> show)
json.dump(dict(fps=FPS, start=S0, end=END, segs=segs, broll=broll, designed=designed, cuts=cuts), open('show_edl.json', 'w'), indent=1)
if __name__ == '__main__':
    for s in segs: print(f"{s['clip']} {s['rec'] / FPS:8.2f}s  {s['frames'] / FPS:7.2f}s  x{s['speed']}")
    print('show', round((END - S0) / FPS, 2), 's; whole video ends', round(END / FPS, 2), 's;', len(broll), 'B-roll pieces')
