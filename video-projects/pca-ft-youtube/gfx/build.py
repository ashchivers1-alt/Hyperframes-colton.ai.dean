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

# ------------------------------------------------------------------ Ash's notes 2026-11-09: pulses, alarm, quad freeze + diagram, phones
top_tag('t12_pulses', tr('c05', 99.2), 'FINISHER', 'PULSES TO FINISH', dur=4.6, right=True)

css = """#A { position:absolute; left:0; right:0; top:46px; display:flex; flex-direction:column; align-items:center; gap:8px; }
#A .pill { background:#d80609; font-weight:800; font-size:19px; letter-spacing:0.26em; padding:7px 14px 6px; }
#A .t { font-size:78px; }
#A .row { display:flex; align-items:center; gap:18px; }
#A .st { font-family:"Bebas Neue"; font-size:64px; letter-spacing:0.05em; background:#d80609; padding:4px 20px 0; transform:rotate(-4deg); }
#A .s { font-size:24px; }"""
body = ('<div id="A" class="sh"><div class="pill">ALARM UPDATE</div><div class="clip"><div class="t">MY ALARM IS GOING OFF</div></div>'
        '<div class="row"><div class="st">AGAIN.</div><div class="s">Snooze count: lost track</div></div></div>')
ad = 4.2
js = f"""gsap.set(["#A .pill","#A .t","#A .st","#A .s"], {{ opacity:0 }});
tl.fromTo("#A .pill", {{ opacity:0, y:-16 }}, {{ opacity:1, y:0, duration:0.35*K, ease:"power3.out", immediateRender:false }}, 0.05*K);
tl.fromTo("#A .t", {{ opacity:0, yPercent:100 }}, {{ opacity:1, yPercent:0, duration:0.55*K, ease:"expo.out", immediateRender:false }}, 0.15*K);
tl.fromTo("#A .pill", {{ rotation:-6 }}, {{ rotation:6, duration:0.06*K, ease:"none", yoyo:true, repeat:13, immediateRender:false }}, 0.4*K);
tl.fromTo("#A .st", {{ opacity:0, scale:2.4 }}, {{ opacity:1, scale:1, duration:0.28*K, ease:"power4.in", immediateRender:false }}, 1.05*K);
tl.fromTo("#A .s", {{ opacity:0, x:-14 }}, {{ opacity:1, x:0, duration:0.4*K, ease:"power2.out", immediateRender:false }}, 1.5*K);
tl.to("#A", {{ opacity:0, y:-16, duration:0.4*K, ease:"power2.in" }}, {ad - 0.45:.3f}*K);"""
page('t14b_alarm', tr('c07', 161.5), ad, body, js, css)

# quad bias: freeze on the bottom of the rep, red line down the shin, side-on diagram under the 'BIAS THE QUADS' card
import math
FZ = 45.03                                     # c10 source second of the frozen frame (bottom of the rep)
FZ_HOLD = 5.0
KNEE, ANKLE, TOE = (920, 527), (982, 722), (1088, 598)   # 1920x1080 frame positions
def leg(hip, ankle, l1=105, l2=100):
    """knee from hip + ankle (the solution above the hip-ankle line)"""
    dx, dy = ankle[0] - hip[0], ankle[1] - hip[1]; d = math.hypot(dx, dy)
    a = (l1 * l1 - l2 * l2 + d * d) / (2 * d); h = math.sqrt(max(0, l1 * l1 - a * a))
    mx, my = hip[0] + a * dx / d, hip[1] + a * dy / d
    return min([(mx + h * dy / d, my - h * dx / d), (mx - h * dy / d, my + h * dx / d)], key=lambda p: p[1])
def panel(x0, label, sub, s, hot):
    """side-on 45-degree leg press pictogram; s = foot position along the plate (negative = higher). Dashed line = the toes,
    square to the plate: the low foot's knee ends up past it"""
    r = 0.7071; fp = (x0 + 238, 105); n = (-r, r)                      # plate runs along (r, r); n points from the plate to the lifter
    hip = (fp[0] + 150 * n[0], fp[1] + 150 * n[1])
    ank = (fp[0] + s * r, fp[1] + s * r); toe = (ank[0] - 38 * r, ank[1] - 38 * r); kn = leg(hip, ank)
    col = '#d80609' if hot else '#f2f2f2'
    q = (kn[0] - toe[0]) * n[0] + (kn[1] - toe[1]) * n[1]; ref = (toe[0] + q * n[0], toe[1] + q * n[1])   # knee projected onto the toe line
    g = [f'<line x1="{fp[0] - 130 * r:.0f}" y1="{fp[1] - 130 * r:.0f}" x2="{fp[0] + 60 * r:.0f}" y2="{fp[1] + 60 * r:.0f}" stroke="#8a8a8a" stroke-width="10" stroke-linecap="round"/>',
         f'<line x1="{hip[0] - 14:.0f}" y1="{hip[1] + 12:.0f}" x2="{hip[0] - 104:.0f}" y2="{hip[1] - 44:.0f}" stroke="#4a4a4a" stroke-width="12" stroke-linecap="round"/>',
         f'<line x1="{hip[0]:.0f}" y1="{hip[1]:.0f}" x2="{hip[0] - 86:.0f}" y2="{hip[1] - 52:.0f}" stroke="#bdbdbd" stroke-width="15" stroke-linecap="round"/><circle cx="{hip[0] - 110:.0f}" cy="{hip[1] - 72:.0f}" r="17" fill="#bdbdbd"/>',
         f'<line x1="{toe[0]:.0f}" y1="{toe[1]:.0f}" x2="{toe[0] + 125 * n[0]:.0f}" y2="{toe[1] + 125 * n[1]:.0f}" stroke="#fff" stroke-opacity="0.75" stroke-width="3" stroke-dasharray="7 6"/>',
         f'<polyline points="{hip[0]:.0f},{hip[1]:.0f} {kn[0]:.0f},{kn[1]:.0f} {ank[0]:.0f},{ank[1]:.0f} {toe[0]:.0f},{toe[1]:.0f}" fill="none" stroke="{col}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>',
         f'<circle cx="{hip[0]:.0f}" cy="{hip[1]:.0f}" r="10" fill="#fff"/><circle cx="{kn[0]:.0f}" cy="{kn[1]:.0f}" r="11" fill="#fff"/><circle cx="{ank[0]:.0f}" cy="{ank[1]:.0f}" r="8" fill="#fff"/>']
    if hot:
        g.append(f'<line class="ov" x1="{ref[0]:.0f}" y1="{ref[1]:.0f}" x2="{kn[0] + 12 * r:.0f}" y2="{kn[1] + 12 * r:.0f}" stroke="#ff5254" stroke-width="5" marker-end="url(#ar)"/>'
                 f'<text class="ov" x="{kn[0] - 6:.0f}" y="{kn[1] - 22:.0f}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="15" letter-spacing="2" fill="#ff5254">KNEES PAST TOES</text>')
    g.append(f'<text x="{x0 + 150}" y="262" text-anchor="middle" font-family="Bebas Neue" font-size="40" fill="{col}">{label}</text>'
             f'<text x="{x0 + 150}" y="290" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="19" letter-spacing="3" fill="#cfcfcf">{sub}</text>')
    return f'<g id="pn{int(hot)}" transform="translate(0,46)">' + ''.join(g) + '</g>'
dia = ('<svg width="590" height="350" viewBox="0 0 590 350"><defs><marker id="ar" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4" markerHeight="4" orient="auto">'
       '<path d="M0,0 L10,5 L0,10 z" fill="#ff5254"/></marker></defs>' + panel(0, 'HIGH FOOT', 'GLUTES · HAMS', -85, False) + panel(300, 'LOW FOOT', 'QUADS', 15, True) + '</svg>')
fz_end = piece_end('c10', 43.0) - 0.15
F0 = tr('c10', FZ); fd = fz_end - F0
L = math.hypot(ANKLE[0] - KNEE[0], ANKLE[1] - KNEE[1])
css = f"""#FZ {{ position:absolute; inset:0; }}
#FZ img {{ position:absolute; left:0; top:0; width:1920px; height:1080px; transform-origin:{KNEE[0]}px {KNEE[1]}px; }}
#FZ .dim {{ position:absolute; inset:0; background:rgba(0,0,0,0.22); }}
#FL {{ position:absolute; inset:0; background:#fff; opacity:0; }}
#LB {{ position:absolute; font-family:"Bebas Neue"; font-size:44px; letter-spacing:0.04em; line-height:0.95; }}
#LB small {{ display:block; font-family:Montserrat; font-weight:800; font-size:18px; letter-spacing:0.2em; color:#ff5254; margin-bottom:8px; }}
#D {{ right:72px; top:400px; width:640px; padding:20px 24px 14px; }}
#D .k {{ font-size:19px; color:#ff5254; letter-spacing:0.28em; margin-bottom:6px; }}"""
body = (f'<div id="FZ"><img src="assets/freeze.png"><div class="dim"></div>'
        f'<svg width="1920" height="1080" style="position:absolute; left:0; top:0;">'
        f'<line id="shin" x1="{KNEE[0]}" y1="{KNEE[1]}" x2="{ANKLE[0]}" y2="{ANKLE[1]}" stroke="#d80609" stroke-width="9" stroke-linecap="round" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}" style="filter:drop-shadow(0 0 8px rgba(216,6,9,0.9))"/>'
        f'<line id="foot" x1="{ANKLE[0]}" y1="{ANKLE[1]}" x2="{TOE[0]}" y2="{TOE[1]}" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-dasharray="12 9" opacity="0"/>'
        f'<circle id="kd" cx="{KNEE[0]}" cy="{KNEE[1]}" r="16" fill="none" stroke="#fff" stroke-width="5"/><circle id="ad" cx="{ANKLE[0]}" cy="{ANKLE[1]}" r="13" fill="#d80609" stroke="#fff" stroke-width="4"/></svg>'
        f'<div id="LB" class="sh" style="left:{KNEE[0] - 360}px; top:{KNEE[1] + 70}px;"><small>WATCH THE KNEE</small>KNEE TRAVELS<br>OVER THE ANKLE</div>'
        f'<div id="FL"></div></div>'
        f'<div id="D" class="card sh"><div class="k">WHY IT HITS THE QUADS</div>{dia}</div>')
H = FZ_HOLD
js = f"""gsap.set(["#LB", "#kd", "#ad", "#D"], {{ opacity:0 }});
tl.fromTo("#FL", {{ opacity:0.75 }}, {{ opacity:0, duration:0.3*K, ease:"power2.out", immediateRender:false }}, 0);
tl.fromTo("#FZ img", {{ scale:1 }}, {{ scale:1.05, duration:{H:.2f}*K, ease:"none", immediateRender:false }}, 0);
tl.fromTo("#kd", {{ opacity:0, scale:2.2, transformOrigin:"50% 50%" }}, {{ opacity:1, scale:1, duration:0.35*K, ease:"back.out(2)", immediateRender:false }}, 0.3*K);
tl.to("#shin", {{ strokeDashoffset:0, duration:0.55*K, ease:"power3.inOut" }}, 0.45*K);
tl.fromTo("#ad", {{ opacity:0, scale:0.3, transformOrigin:"50% 50%" }}, {{ opacity:1, scale:1, duration:0.3*K, ease:"back.out(2.4)", immediateRender:false }}, 0.95*K);
tl.to("#foot", {{ opacity:0.85, duration:0.3*K }}, 1.1*K);
tl.fromTo("#LB", {{ opacity:0, x:-20 }}, {{ opacity:1, x:0, duration:0.45*K, ease:"expo.out", immediateRender:false }}, 1.15*K);
tl.fromTo("#D", {{ opacity:0, y:24 }}, {{ opacity:1, y:0, duration:0.5*K, ease:"power3.out", immediateRender:false }}, 1.6*K);
gsap.set(["#pn0", "#pn1"], {{ opacity:0 }});
tl.fromTo("#pn0", {{ opacity:0, x:-16 }}, {{ opacity:1, x:0, duration:0.4*K, ease:"power2.out", immediateRender:false }}, 1.9*K);
tl.fromTo("#pn1", {{ opacity:0, x:16 }}, {{ opacity:1, x:0, duration:0.4*K, ease:"power2.out", immediateRender:false }}, 2.4*K);
tl.fromTo("#pn1 .ov", {{ opacity:0 }}, {{ opacity:1, duration:0.12*K, yoyo:true, repeat:4, immediateRender:false }}, 2.9*K);
tl.to("#FL", {{ opacity:0.6, duration:0.08*K }}, {H - 0.08:.3f}*K);
tl.set(["#FZ img", "#FZ .dim", "#FZ svg", "#LB"], {{ opacity:0 }}, {H:.3f}*K);
tl.to("#FL", {{ opacity:0, duration:0.25*K }}, {H:.3f}*K);
tl.to("#D", {{ opacity:0, x:30, duration:0.35*K, ease:"power2.in" }}, {fd - 0.4:.3f}*K);"""
page('t15b_kneefreeze', F0, fd, body, js, css)
shutil.copy(PRJ + f'/show/px/freeze_{SCALE}.png', ROOT + '/comps/t15b_kneefreeze/assets/freeze.png')

css = """#N { position:absolute; right:64px; top:56px; text-align:right; display:flex; flex-direction:column; align-items:flex-end; gap:8px; }
#N .pill { background:#d80609; font-weight:800; font-size:19px; letter-spacing:0.26em; padding:7px 14px 6px; }
#N .t { font-size:72px; }
#N .row { display:flex; align-items:center; gap:16px; }
#N .s { font-size:24px; }
#N .st { font-family:"Bebas Neue"; font-size:60px; letter-spacing:0.06em; background:#d80609; padding:4px 18px 0; transform:rotate(4deg); }"""
body = ('<div id="N" class="sh"><div class="pill">HOUSE RULES</div><div class="clip"><div class="t">NO PHONES ALLOWED IN TRAINING</div></div>'
        '<div class="row"><div class="s">Caught in 4K</div><div class="st">LOL</div></div></div>')
nd = 5.0
js = f"""gsap.set(["#N .pill","#N .t","#N .s","#N .st"], {{ opacity:0 }});
tl.fromTo("#N .pill", {{ opacity:0, x:24 }}, {{ opacity:1, x:0, duration:0.4*K, ease:"power3.out", immediateRender:false }}, 0.05*K);
tl.fromTo("#N .t", {{ opacity:0, yPercent:100 }}, {{ opacity:1, yPercent:0, duration:0.55*K, ease:"expo.out", immediateRender:false }}, 0.15*K);
tl.fromTo("#N .s", {{ opacity:0, y:10 }}, {{ opacity:1, y:0, duration:0.4*K, ease:"power2.out", immediateRender:false }}, 0.9*K);
tl.fromTo("#N .st", {{ opacity:0, scale:2.4 }}, {{ opacity:1, scale:1, duration:0.28*K, ease:"power4.in", immediateRender:false }}, 1.3*K);
tl.to("#N .st", {{ scale:1.08, duration:0.18*K, ease:"sine.inOut", yoyo:true, repeat:5 }}, 1.8*K);
tl.to("#N", {{ opacity:0, x:24, duration:0.4*K, ease:"power2.in" }}, {nd - 0.45:.3f}*K);"""
page('t22_phones', tr('c12', 132.9), nd, body, js, css)

# the frozen frame sits under the 'BIAS THE QUADS' card (comps are stacked in list order)
fzc = next(m for m in made if m['name'] == 't15b_kneefreeze'); made.remove(fzc)
made.insert(next(i for i, m in enumerate(made) if m['name'] == 't15_quads'), fzc)
json.dump(made, open(ROOT + '/made.json', 'w'), indent=1)
print(len(made), 'comps')
for m in made: print(f"{m['name']:22s} {m['rec'] / FPS:7.2f}s  {m['frames'] / FPS:5.1f}s")
