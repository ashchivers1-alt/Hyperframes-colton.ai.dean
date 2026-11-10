"""PCA FT YouTube graphics: posing + training sections (kit.py holds the look and building blocks)."""
from kit import *

# ================================================================== POSING SECTION (Ash's edit; m() maps his original seconds past the cuts in intro.json)
CUTS = json.load(open(PRJ + '/intro.json'))['cuts']
def m(t): return t - sum((b - a) / FPS for a, b, _ in CUTS if t * FPS >= b)
lower_third('p01_gym', 4.2, 'IN-PERSON CHECK-IN', 'ALPHA MUSCLE GYM', 'St Neots', dur=5.2, size=100)
lower_third('p02_client', 9.9, 'CLIENT', 'NICK', 'First show · PCA First Timers', dur=6.2, size=120)
top_tag('p03_peak', 16.5, '1 WEEK OUT', 'PEAK WEEK CHECK-IN', dur=4.2)
top_tag('p04_qturn', 61.0, 'POSING', 'QUARTER TURN', dur=3.6, right=True)
cue('p05_breathe', 71.6, 'BREATHE OUT', 'Any pose where you need to contract the waist — blow that air out.', sub_at=1.6, dur=8.4, kicker='POSING CUE')
top_tag('p06_front', 91.3, 'POSING', 'BACK TO THE FRONT', dur=3.4, right=True)
top_tag('p07_sidetri', 107.8, 'POSING', 'SIDE TRICEP', dur=3.6, right=True)
top_tag('p08_sideleg', 127.0, 'POSING', 'INTO THE SIDE LEG', dur=3.6, right=True)
steps('p09_sideleg_cues', 144.6, 'SIDE LEG · 3 CUES', 'GET THE HAMSTRING DROP', [
    ('Push the back knee into the front leg', 0.3, '01', ('= extra hamstring drop', 153.3 - 144.6)),
    ('Drive through the tiptoes', 163.5 - 144.6, '02', ('Like the start of a leg extension', m(170.1) - 144.6)),
    ('Squeeze the glute', m(178.9) - 144.6, '03')], dur=m(184.9) - 144.6, width=560)
s = m(188.5)
chips('p10_prep', s, 'PREP LOOKS DIFFERENT FOR EVERYONE', [('500G CARBS', m(194.7) - s), ('8,000 STEPS', m(196.1) - s)],
      "THAT AIN'T EVERYONE", m(197.4) - s, dur=m(199.35) - s)
s = m(CUTS[1][1] / FPS)   # first frame after the swear cut: "that's them, that's not you"
quote('p11_them', s + 0.05, "THAT'S THEM. THAT'S NOT YOU.", dur=2.8)
s = m(220.6)
steps('p12_checklist', s, 'PEAK WEEK', 'PREPPING FOR THE TAN', [
    ('Exfoliate your skin', m(223.4) - s, '✓'),
    ('Hair removal cream', m(227.6) - s, '✗', ("It's essentially burning your skin", m(232.0) - s)),
    ('Clean razor shave — start of the week', m(242.8) - s, '✓'),
    ('Wet shave', m(250.8) - s, '✓'),
    ('Electric / lady shaver top-ups', m(257.4) - s, '✓')],
    dur=m(270.3) - s, pos='gap', width=500, foot=('FRESH BLADE = NO SKIN IRRITATION', m(266.6) - s))

# ================================================================== TRAINING SECTION
T0 = ex_start('kick')
GYM = json.load(open(PRJ + '/gym.json'))
body = ('<div class="back"></div><div id="L" class="sh" style="position:absolute; left:80px; bottom:90px; display:flex; align-items:flex-end; gap:36px;">'
        '<img class="x" src="assets/muscleworks-logo.png" style="width:210px; filter:drop-shadow(0 6px 18px rgba(0,0,0,0.6));">'
        '<div><div class="k"><i></i>TRAINING SESSION WITH</div><div class="clip"><div class="t" style="font-size:130px; margin-top:10px;">PAULINA + GABI</div></div>'
        '<div class="s" style="margin-top:6px;">Muscle Works · Southwark</div></div></div>')
gd = GYM['frames'] / FPS - 0.3
page('t0g_gym', GYM['rec'] / FPS + 0.25, gd, body, lt_js('#L', gd))
shutil.copy(PRJ + '/show/px/muscleworks-logo.png', ROOT + '/comps/t0g_gym/assets/')
lower_third('t00_session', T0 + 0.3, 'THE SESSION', 'GLUTES & HAMSTRINGS', '6 movements · 3 people · a few rounds each', dur=3.4, size=120)
X = [('kick', 'CABLE GLUTE KICKBACK', 'GLUTE MAX', 3.8), ('abd', 'HIP ABDUCTION', 'GLUTE MED', 0.4), ('thrust', 'BANDED HIP THRUST', 'GLUTES', 0.4),
     ('press', 'LEG PRESS', 'QUADS · GLUTES', 0.4), ('rdl', 'ROMANIAN DEADLIFT', 'HAMSTRINGS · GLUTES', 0.4), ('curl', 'SEATED LEG CURL', 'HAMSTRINGS', 0.4)]
for i, (k, t, tg, off) in enumerate(X):
    exercise(f't{i + 1:02d}_{k}', ex_start(k) + off, i + 1, 6, t, tg, dur=3.9 if k == 'kick' else 5.0)

cue('t10_squeeze', tr('c04', 86.4), 'SQUEEZE THE GLUTES', 'Contract at the top of every rep', dur=4.6)
s = tr('c05', 160.9); cue('t11_fit', s, 'MAKE THE MACHINE FIT YOU', "Too far back and you can't open up enough. Machines don't fit everybody.",
                         sub_at=1.4, dur=piece_end('c05', 160.9) - s - 0.15)
cue('t13_squeeze_top', tr('c07', 41.4), 'SQUEEZE ON TOP', dur=4.6)
s = tr('c07', 146.9); cue('t14_lower', s, 'THE GLUTE IS LOWERING YOU', 'Constant tension — work with the bands', sub_at=155.6 - 146.9, dur=12.0)
s = tr('c10', 43.0); cue('t15_quads', s, 'BIAS THE QUADS', 'Low foot position = knees travel further over the toes', sub_at=1.2,
                         dur=piece_end('c10', 43.0) - s - 0.15, kicker='ASH\'S TIP')
top_tag('t16_3weeks', tr('c09', 56.8), '3 WEEKS OUT', 'THREE WEEKS TO MAKE IT COUNT', dur=5.0, right=True)
s = tr('c11', 55.8); cue('t17_hips', s, 'DRIVE YOUR HIPS BACK', 'Lengthen the glute and the hammy — not more load on your lower back',
                         sub_at=70.6 - 55.8, dur=piece_end('c11', 60) - s - 0.15, pos='left')
s = tr('c11', 209.5); cue('t18_stable', s, 'CREATE A STABLE BACK', 'Slight arch in the lower back — rounding it loads the lower back', sub_at=211.4 - 209.5,
                          dur=piece_end('c11', 220) - s - 0.15, pos='left')
s = tr('c11', 251.2); cue('t19_stretch', s, 'JUST STRETCH THE HAMS & GLUTES', "Straight down — don't chase extra range, that's what pulls your back forward",
                          sub_at=257.8 - 251.2, dur=piece_end('c11', 255) - s - 0.15, pos='left')
# t20_floor dropped: Ash cut the 'not trying to reach the floor' line
s = tr('c14', 32.6)
reps('t21_reps', s, [(7, 0.3), (8, 36.1 - 32.6), (9, 38.3 - 32.6), (10, 42.1 - 32.6), (11, 46.6 - 32.6)],
     dur=piece_end('c14', 40) - s, extra=('TWO MORE', 43.7 - 32.6))

json.dump(made, open(ROOT + '/made.json', 'w'), indent=1)
print(len(made), 'comps')
for m in made: print(f"{m['name']:22s} {m['rec'] / FPS:7.2f}s  {m['frames'] / FPS:5.1f}s")
