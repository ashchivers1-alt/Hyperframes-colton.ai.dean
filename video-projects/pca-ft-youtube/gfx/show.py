"""Show-day section graphics -> gfx/comps/<name>, gfx/made_show.json. Times from show_edl.json (scripts/show_plan.py).
s* = text graphics (kit blocks), w* = full-frame section wipes, x* = designed B-roll pieces (photos / video in cards)."""
import sys
from kit import *
sys.path.insert(0, PRJ + '/scripts'); os.chdir(PRJ)
from show_plan import T, designed, cuts, END
PX = PRJ + '/show/px/'
made.clear()

def media(name, files):
    os.makedirs(f'{ROOT}/comps/{name}/assets', exist_ok=True)
    for f in files: shutil.copy(PX + f, f'{ROOT}/comps/{name}/assets/{f}')

BG = """<div class="bg"></div>"""
BG_CSS = """.bg { position:absolute; inset:0; background:radial-gradient(ellipse 70% 60% at 50% 45%, #1d1d22 0%, #0b0b0d 75%); }
.bg::after { content:''; position:absolute; inset:0; opacity:0.18;
  background-image:linear-gradient(rgba(255,255,255,0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.07) 1px, transparent 1px);
  background-size:80px 80px; }
.hd { position:absolute; left:0; right:0; top:46px; text-align:center; }
.hd .k { justify-content:center; font-size:20px; color:#ff5254; }
.hd .t { font-size:84px; margin-top:6px; }
.pol { position:absolute; background:#f3f1ec; padding:16px 16px 70px; box-shadow:0 30px 70px rgba(0,0,0,0.6); }
.pol img, .pol video { display:block; width:100%; height:100%; object-fit:cover; }
.pol .cap { position:absolute; left:0; right:0; bottom:12px; text-align:center; color:#141414; }
.pol .cap b { font-family:"Bebas Neue"; font-size:40px; letter-spacing:0.04em; }
.pol .cap span { display:block; font-weight:700; font-size:17px; letter-spacing:0.08em; color:#555; margin-top:-2px; }
.tag { position:absolute; top:-22px; left:22px; background:#d80609; color:#fff; font-family:"Bebas Neue"; font-size:38px; letter-spacing:0.08em;
  padding:4px 18px 0; box-shadow:0 8px 20px rgba(0,0,0,0.4); }
.vcard { position:absolute; background:#0c0c0e; padding:10px; border-top:6px solid #d80609; box-shadow:0 30px 80px rgba(0,0,0,0.6); }
.vcard video { display:block; width:100%; height:100%; object-fit:cover; }
.vcard .lab { position:absolute; left:10px; bottom:-52px; font-weight:800; font-size:21px; letter-spacing:0.24em; color:#fff;
  background:rgba(12,12,14,0.85); padding:10px 16px 9px; }
.vcard .lab b { color:#ff5254; }"""

def vid(i, f, dur, start=0):
    return f'<video id="v{i}" src="assets/{f}" data-start="{start * K:.3f}" data-duration="{dur * K:.3f}" data-track-index="{i}" muted playsinline></video>'

# ---------------------------------------------------------------- full-frame wipe across a cut (opaque from 0.45 s to dur-0.45 s)
def wipe(name, cut, title=None, kicker=None, dur=2.2):
    t0 = cut - dur / 2
    css = """#P { position:absolute; inset:0; background:#0c0c0e; }
#P .edge { position:absolute; right:-36px; top:0; bottom:0; width:36px; background:#d80609; }
#P .bg { opacity:1; }
#M { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; }
#M .k { font-size:22px; color:#ff5254; }
#M .t { font-size:150px; margin-top:6px; }
#M .rule { width:140px; height:5px; background:#d80609; margin-top:16px; transform-origin:50% 50%; }"""
    txt = (f'<div id="M" class="sh">' + (f'<div class="k"><i></i>{E(kicker)}<i></i></div>' if kicker else '')
           + f'<div class="clip"><div class="t">{E(title)}</div></div><div class="rule"></div></div>') if title else ''
    body = f'<div id="P">{BG}<div class="edge"></div>{txt}</div>'
    js = f"""gsap.set("#P", {{ xPercent:-104 }});
tl.to("#P", {{ xPercent:0, duration:0.45*K, ease:"power3.inOut" }}, 0);
tl.to("#P", {{ xPercent:104, duration:0.45*K, ease:"power3.inOut" }}, {dur - 0.45:.3f}*K);"""
    if title:
        js += f"""
gsap.set(["#M .k","#M .t"], {{ opacity:0 }}); gsap.set("#M .rule", {{ scaleX:0 }});
tl.fromTo("#M .t", {{ opacity:0, yPercent:100 }}, {{ opacity:1, yPercent:0, duration:0.5*K, ease:"expo.out", immediateRender:false }}, 0.35*K);
tl.fromTo("#M .k", {{ opacity:0, y:10 }}, {{ opacity:1, y:0, duration:0.35*K, immediateRender:false }}, 0.45*K);
tl.to("#M .rule", {{ scaleX:1, duration:0.5*K, ease:"power3.inOut" }}, 0.5*K);"""
    page(name, t0, dur, body, js, BG_CSS + css)

def big_title(name, t0, kicker, title, dur, fade_black=False):
    css = """#B { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; }
#B .k { font-size:24px; } #B .t { font-size:170px; margin-top:4px; }
#B .rule { width:150px; height:5px; background:#d80609; margin-top:14px; transform-origin:50% 50%; }
#BK { position:absolute; inset:0; background:#000; opacity:0; }
.back2 { position:absolute; inset:0; background:radial-gradient(ellipse 50% 40% at 50% 50%, rgba(0,0,0,0.5), rgba(0,0,0,0) 75%); }"""
    body = (f'<div class="back2"></div><div id="B" class="sh"><div class="k"><i></i>{E(kicker)}<i></i></div>'
            f'<div class="clip"><div class="t">{E(title)}</div></div><div class="rule"></div></div>' + ('<div id="BK"></div>' if fade_black else ''))
    js = f"""gsap.set(["#B .k","#B .t",".back2"], {{ opacity:0 }}); gsap.set("#B .rule", {{ scaleX:0 }});
tl.to(".back2", {{ opacity:1, duration:0.5*K }}, 0);
tl.fromTo("#B .t", {{ opacity:0, yPercent:100 }}, {{ opacity:1, yPercent:0, duration:0.7*K, ease:"expo.out", immediateRender:false }}, 0.1*K);
tl.fromTo("#B .k", {{ opacity:0, letterSpacing:"0.6em" }}, {{ opacity:1, letterSpacing:"0.3em", duration:0.8*K, ease:"power2.out", immediateRender:false }}, 0.3*K);
tl.to("#B .rule", {{ scaleX:1, duration:0.6*K, ease:"power3.inOut" }}, 0.45*K);
tl.fromTo("#B .t", {{ scale:1 }}, {{ scale:1.04, duration:{dur:.2f}*K, ease:"none", immediateRender:false }}, 0);"""
    js += (f'\ntl.to("#BK", {{ opacity:1, duration:1.4*K, ease:"power1.in" }}, {dur - 1.45:.3f}*K);' if fade_black else
           f'\ntl.to(["#B", ".back2"], {{ opacity:0, duration:0.45*K, ease:"power2.in" }}, {dur - 0.5:.3f}*K);')
    page(name, t0, dur, body, js, css)

# ---------------------------------------------------------------- designed B-roll pieces
def x_progress():
    a, b = designed['x_progress']; d = b - a; media('x_progress', ['burger.jpg', '8934_now.mp4'])
    css = BG_CSS + """#L { left:330px; top:240px; width:470px; height:690px; transform:rotate(-4deg); }
#R { right:350px; top:212px; width:420px; height:760px; transform:rotate(3deg); padding-bottom:16px; }
#R .tag, #L .tag { left:auto; right:22px; }
#AR { position:absolute; left:906px; top:520px; font-family:"Bebas Neue"; font-size:120px; color:#d80609; }
#out { position:absolute; inset:0; background:#000; opacity:0; }"""
    body = (BG + '<div class="hd sh"><div class="k"><i></i>FIRST-TIMER · THE PREP<i></i></div><div class="clip"><div class="t">NICK&#39;S PROGRESS</div></div></div>'
            '<div id="L" class="pol"><img src="assets/burger.jpg"><div class="tag">THEN</div><div class="cap"><b>LIFESTYLE CLIENT</b><span>DAY ONE</span></div></div>'
            f'<div id="R" class="pol">{vid(1, "8934_now.mp4", d)}<div class="tag">NOW</div></div>'
            '<div id="AR" class="sh">&#10140;</div><div id="out"></div>')
    js = f"""gsap.set(["#L","#R","#AR",".hd .t",".hd .k"], {{ opacity:0 }});
tl.fromTo(".bg", {{ opacity:0 }}, {{ opacity:1, duration:0.3*K, immediateRender:false }}, 0);
tl.fromTo(".hd .t", {{ opacity:0, yPercent:100 }}, {{ opacity:1, yPercent:0, duration:0.6*K, ease:"expo.out", immediateRender:false }}, 0.15*K);
tl.fromTo(".hd .k", {{ opacity:0 }}, {{ opacity:1, duration:0.4*K, immediateRender:false }}, 0.3*K);
tl.fromTo("#L", {{ opacity:0, x:-260, rotation:-14 }}, {{ opacity:1, x:0, rotation:-4, duration:0.7*K, ease:"back.out(1.4)", immediateRender:false }}, 0.35*K);
tl.fromTo("#AR", {{ opacity:0, x:-40 }}, {{ opacity:1, x:0, duration:0.4*K, ease:"power3.out", immediateRender:false }}, 1.3*K);
tl.fromTo("#R", {{ opacity:0, x:260, rotation:12 }}, {{ opacity:1, x:0, rotation:3, duration:0.7*K, ease:"back.out(1.4)", immediateRender:false }}, 1.5*K);
tl.fromTo(["#L","#R"], {{ scale:1 }}, {{ scale:1.035, duration:{d:.2f}*K, ease:"none", immediateRender:false }}, 0);
tl.to("#out", {{ opacity:1, duration:0.3*K }}, {d - 0.3:.3f}*K);"""
    page('x_progress', a, d, body, js, css)

def x_compare():
    a, b = designed['x_compare']; d = b - a; media('x_compare', ['burger.jpg', 'IMG_3771.jpg'])
    r_at = T('c17', 119.6) - a
    css = BG_CSS + """#L { left:300px; top:230px; width:500px; height:700px; transform:rotate(-4deg); }
#R { right:300px; top:215px; width:525px; height:730px; transform:rotate(3deg); }
#R .tag { background:#f2f2f2; color:#111; }
#VS { position:absolute; left:910px; top:500px; width:100px; height:100px; border-radius:50%; background:#d80609; display:flex; align-items:center;
  justify-content:center; font-family:"Bebas Neue"; font-size:52px; box-shadow:0 10px 30px rgba(0,0,0,0.5); }
#out { position:absolute; inset:0; background:#000; opacity:0; }"""
    body = (BG + '<div class="hd sh"><div class="k"><i></i>FIRST &amp; ONLY COACH<i></i></div><div class="clip"><div class="t">DAY ONE TO SHOW DAY</div></div></div>'
            '<div id="L" class="pol"><img src="assets/burger.jpg"><div class="tag">DAY ONE</div><div class="cap"><b>LIFESTYLE CLIENT</b><span>DIETING FOR A HOLIDAY</span></div></div>'
            '<div id="R" class="pol"><img src="assets/IMG_3771.jpg" style="object-position:50% 30%"><div class="tag">SHOW DAY</div><div class="cap"><b>P4 · FIRST SHOW</b><span>PCA FIRST TIMERS</span></div></div>'
            '<div id="VS">VS</div><div id="out"></div>')
    js = f"""gsap.set(["#L","#R","#VS",".hd .t",".hd .k"], {{ opacity:0 }});
tl.fromTo(".bg", {{ opacity:0 }}, {{ opacity:1, duration:0.3*K, immediateRender:false }}, 0);
tl.fromTo(".hd .t", {{ opacity:0, yPercent:100 }}, {{ opacity:1, yPercent:0, duration:0.6*K, ease:"expo.out", immediateRender:false }}, 0.15*K);
tl.fromTo(".hd .k", {{ opacity:0 }}, {{ opacity:1, duration:0.4*K, immediateRender:false }}, 0.3*K);
tl.fromTo("#L", {{ opacity:0, y:80, rotation:-12 }}, {{ opacity:1, y:0, rotation:-4, duration:0.7*K, ease:"back.out(1.4)", immediateRender:false }}, 0.4*K);
tl.fromTo("#VS", {{ opacity:0, scale:2.4 }}, {{ opacity:1, scale:1, duration:0.35*K, ease:"power4.in", immediateRender:false }}, {r_at - 0.5:.3f}*K);
tl.fromTo("#R", {{ opacity:0, y:80, rotation:12 }}, {{ opacity:1, y:0, rotation:3, duration:0.7*K, ease:"back.out(1.4)", immediateRender:false }}, {r_at:.3f}*K);
tl.fromTo(["#L","#R"], {{ scale:1 }}, {{ scale:1.035, duration:{d:.2f}*K, ease:"none", immediateRender:false }}, 0);
tl.to("#out", {{ opacity:1, duration:0.3*K }}, {d - 0.3:.3f}*K);"""
    page('x_compare', a, d, body, js, css)

def x_card(name, f, label, side='right', w=860, top=None):
    """video in a floating card over the talking shot (alpha)"""
    a, b = designed[name]; d = b - a; media(name, [f]); h = round(w * 9 / 16)
    pos = f'right:80px;' if side == 'right' else f'left:80px;'
    top = (1080 - h) // 2 - 40 if top is None else top
    css = BG_CSS + f"""#V {{ {pos} top:{top}px; width:{w + 20}px; height:{h + 20}px; transform:rotate({-2 if side == 'right' else 2}deg); }}
#SH {{ position:absolute; inset:0; background:radial-gradient(ellipse 45% 55% at {72 if side == 'right' else 28}% 50%, rgba(0,0,0,0.45), rgba(0,0,0,0) 75%); }}"""
    body = f'<div id="SH"></div><div id="V" class="vcard">{vid(1, f, d)}<div class="lab">{label}</div></div>'
    js = f"""gsap.set(["#V .lab"], {{ opacity:0 }});
tl.fromTo("#SH", {{ opacity:0 }}, {{ opacity:1, duration:0.4*K, immediateRender:false }}, 0);
tl.fromTo("#V", {{ opacity:0, scale:0.55, y:80, rotation:{-8 if side == 'right' else 8} }}, {{ opacity:1, scale:1, y:0, rotation:{-2 if side == 'right' else 2}, duration:0.6*K, ease:"back.out(1.5)", immediateRender:false }}, 0.05*K);
tl.fromTo("#V .lab", {{ opacity:0, x:-20 }}, {{ opacity:1, x:0, duration:0.4*K, ease:"power3.out", immediateRender:false }}, 0.5*K);
tl.fromTo("#V", {{ y:0 }}, {{ y:-14, duration:{d - 1:.2f}*K, ease:"sine.inOut", immediateRender:false }}, 0.7*K);
tl.to("#V", {{ opacity:0, scale:0.85, y:30, duration:0.35*K, ease:"power2.in" }}, {d - 0.38:.3f}*K);
tl.to("#SH", {{ opacity:0, duration:0.35*K }}, {d - 0.35:.3f}*K);"""
    page(name, a, d, body, js, css)

def x_lads(name):
    """Nick (left) + Mark (right) polaroids either side of Ash"""
    a, b = designed[name]; d = b - a; media(name, ['IMG_3771.jpg', 'IMG_3796.jpg'])
    css = BG_CSS + """#N { left:96px; top:200px; width:432px; height:642px; transform:rotate(-4deg); }
#M { right:96px; top:250px; width:592px; height:530px; transform:rotate(3deg); }
#N img { object-position:50% 30%; }
#SH { position:absolute; inset:0; background:linear-gradient(90deg, rgba(0,0,0,0.4), rgba(0,0,0,0) 30%, rgba(0,0,0,0) 70%, rgba(0,0,0,0.4)); }"""
    body = ('<div id="SH"></div>'
            '<div id="N" class="pol"><img src="assets/IMG_3771.jpg"><div class="tag">NICK</div><div class="cap"><b>P4</b><span>FIRST-TIMERS BODYBUILDING</span></div></div>'
            '<div id="M" class="pol"><img src="assets/IMG_3796.jpg"><div class="tag">MARK</div><div class="cap"><b>P4</b><span>MASTERS MEN&#39;S PHYSIQUE</span></div></div>')
    js = f"""tl.fromTo("#SH", {{ opacity:0 }}, {{ opacity:1, duration:0.4*K, immediateRender:false }}, 0);
tl.fromTo("#N", {{ opacity:0, scale:1.6, rotation:-16 }}, {{ opacity:1, scale:1, rotation:-4, duration:0.55*K, ease:"power4.out", immediateRender:false }}, 0.05*K);
tl.fromTo("#M", {{ opacity:0, scale:1.6, rotation:15 }}, {{ opacity:1, scale:1, rotation:3, duration:0.55*K, ease:"power4.out", immediateRender:false }}, 0.35*K);
tl.fromTo("#N", {{ y:0 }}, {{ y:-12, duration:{d - 1:.2f}*K, ease:"sine.inOut", immediateRender:false }}, 0.6*K);
tl.fromTo("#M", {{ y:0 }}, {{ y:12, duration:{d - 1:.2f}*K, ease:"sine.inOut", immediateRender:false }}, 0.9*K);
tl.to(["#N", "#M", "#SH"], {{ opacity:0, duration:0.35*K, ease:"power2.in" }}, {d - 0.38:.3f}*K);"""
    page(name, a, d, body, js, css)

def teaser(T):
    """cold open: letterbox, white flash on every cut, chapter words, title card, flash out"""
    d = T['dur']; media('i_teaser', ['team-apexx-logo.png']); ta = T['title_at']; cuts = T['cuts'][1:] + [d - 0.12]
    css = """.bar { position:absolute; left:0; right:0; height:139px; background:#000; } #bt { top:0; } #bb { bottom:0; }
.fl { position:absolute; inset:0; background:#fff; opacity:0; }
.ch { position:absolute; left:96px; bottom:170px; font-family:"Bebas Neue"; font-size:64px; letter-spacing:0.08em; opacity:0; }
.ch i { display:inline-block; width:46px; height:5px; background:#d80609; margin-right:16px; vertical-align:middle; }
#TT { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; opacity:0; }
#TT img { width:250px; margin-bottom:6px; }
#TT .k { font-size:24px; color:#ff5254; } #TT .t { font-size:150px; margin-top:6px; }
#TT .rule { width:150px; height:5px; background:#d80609; margin-top:12px; transform-origin:50% 50%; }"""
    chap = [('PEAK WEEK', T['cuts'][2], T['cuts'][5]), ('THE SESSION', T['cuts'][5], T['cuts'][9]), ('SHOW DAY', T['cuts'][9], T['cuts'][14])]
    body = ('<div class="bar" id="bt"></div><div class="bar" id="bb"></div>'
            + ''.join(f'<div class="ch sh" id="c{i}"><i></i>{E(c)}</div>' for i, (c, _, _) in enumerate(chap))
            + '<div id="TT" class="sh"><img src="assets/team-apexx-logo.png"><div class="k"><i></i>PCA FIRST TIMERS · UK OPEN<i></i></div>'
              '<div class="clip"><div class="t">PEAK WEEK TO SHOW DAY</div></div><div class="rule"></div></div>'
            + ''.join(f'<div class="fl" id="f{i}"></div>' for i in range(len(cuts))))
    js = ['gsap.set("#TT .rule", { scaleX:0 });']
    for i, (c, a0, a1) in enumerate(chap):
        js.append(f'tl.fromTo("#c{i}", {{ opacity:0, x:-30 }}, {{ opacity:1, x:0, duration:0.35*K, ease:"power3.out", immediateRender:false }}, {a0 + 0.08:.3f}*K);')
        js.append(f'tl.to("#c{i}", {{ opacity:0, duration:0.2*K }}, {a1 - 0.22:.3f}*K);')
    for i, c in enumerate(cuts):
        js.append(f'tl.fromTo("#f{i}", {{ opacity:{0.95 if i == len(cuts) - 1 else 0.7} }}, {{ opacity:0, duration:{0.12 if i == len(cuts) - 1 else 0.22}*K, ease:"power2.out", immediateRender:false }}, {c:.3f}*K);')
    js.append(f"""tl.fromTo("#TT", {{ opacity:0 }}, {{ opacity:1, duration:0.2*K, immediateRender:false }}, {ta + 0.15:.3f}*K);
tl.fromTo("#TT img", {{ opacity:0, scale:0.8 }}, {{ opacity:1, scale:1, duration:0.6*K, ease:"back.out(1.6)", immediateRender:false }}, {ta + 0.15:.3f}*K);
tl.fromTo("#TT .t", {{ yPercent:100 }}, {{ yPercent:0, duration:0.7*K, ease:"expo.out", immediateRender:false }}, {ta + 0.35:.3f}*K);
tl.fromTo("#TT .k", {{ opacity:0, letterSpacing:"0.6em" }}, {{ opacity:1, letterSpacing:"0.3em", duration:0.8*K, immediateRender:false }}, {ta + 0.5:.3f}*K);
tl.to("#TT .rule", {{ scaleX:1, duration:0.6*K, ease:"power3.inOut" }}, {ta + 0.6:.3f}*K);
tl.fromTo("#TT", {{ scale:1 }}, {{ scale:1.04, duration:{d - ta:.2f}*K, ease:"none", immediateRender:false }}, {ta:.3f}*K);""")
    page('i_teaser', 0, d, body, '\n'.join(js), css)

# ================================================================== build
c_train, c_15_16, c_16_17, c_17_01 = cuts[0], cuts[1], cuts[2], cuts[3]
wipe('w1_showday', c_train, 'SHOW DAY', 'PCA FIRST TIMERS · UK OPEN', dur=2.6)
wipe('w2_road', c_15_16, dur=1.3)
wipe('w3_later', c_16_17, 'LATER THAT DAY', 'NICK HAS COMPETED', dur=2.4)
wipe('w4_morning', c_17_01, 'THE MORNING AFTER', 'THE DEBRIEF', dur=2.4)

# --- car, morning of the show (c15)
lower_third('s01_lads', T('c15', 5.3), 'SHOW DAY', 'NICK & MARK', 'Two clients on stage this weekend', dur=5.6, size=110)
s = T('c15', 15.2)
chips('s02_mark', s, 'MARK · PURE ELITE WORLDS · PRO', [('TOP 3', 24.7 - 15.2), ('TOP 3', 25.3 - 15.2), ('4TH', 26.7 - 15.2), ('5TH', 27.7 - 15.2)],
      'VERY COMPETITIVE LINE-UPS', 29.9 - 15.2, dur=31.7 - 15.2)
cue('s03_kilos', T('c15', 39.2), '-10 KG IN 5 WEEKS', 'A last-minute decision — and he put in serious work', sub_at=46.0 - 39.2, dur=49.9 - 39.2, kicker="MARK'S PREP")
lower_third('s04_nick', T('c15', 51.1), 'FIRST-TIMER', 'NICK', 'His first ever show', dur=5.1, size=120)
x_progress()
steps('s05_double', T('c15', 72.7), 'DOUBLE HEADER', "TODAY'S SHOWS", [('PCA First Timers', 75.4 - 72.7, '01'), ('PCA UK Open — afternoon', 77.9 - 72.7, '02')], dur=79.85 - 72.7)
top_tag('s06_procards', T('c15', 85.8), 'PCA UK OPEN', 'PRO CARDS ON OFFER', dur=3.7, right=True)
top_tag('s07_caffeine', T('c15', 104.1), 'LONG DAY AHEAD', 'PLENTY OF CAFFEINE', dur=4.6)
# --- motorway (c16, 3x)
big_title('s08_road', cuts[1] + 0.9, 'EN ROUTE', 'ROAD TO THE SHOW', dur=cuts[2] - cuts[1] - 2.2)
# --- car, after Nick (c17)
top_tag('s09_done', T('c17', 2.6), 'NICK', 'DONE & DUSTED', dur=4.2)
cue('s10_result', T('c17', 27.1), 'NICK — 4TH PLACE', 'PCA First Timers · Bodybuilding', sub_at=29.8 - 27.1, dur=37.6 - 27.1, kicker='RESULT', pos='left')
x_card('x_routine', '3768_card.mp4', '<b>NICK</b> &nbsp;POSING ROUTINE', side='left', w=660, top=96)
quote('s12_bench', T('c17', 66.4), 'THIS IS THE BENCHMARK.', dur=5.6)
steps('s13_plan', T('c17', 73.5), 'NEXT FOR NICK', 'THE PLAN', [
    ('Reverse out into an off-season', 77.5 - 73.5, '01'), ('4–6 week push through the reverse', 82.2 - 73.5, '02'),
    ("Bloodwork — make sure it's all good", 89.8 - 73.5, '03'), ('Two years off stage', 93.2 - 73.5, '04', ('Add significant tissue to his frame', 98.9 - 73.5))],
    dur=103.6 - 73.5, width=620)
x_compare()
lower_third('s14_mark', T('c17', 148.1), 'UP NEXT', 'MARK', "PCA UK Open · Masters Men's Physique", dur=5.6, size=120)
# --- morning after (c01)
lower_third('s15_recap', T('c01', 19.8), 'RECAP', 'FIRST TIMERS + UK OPEN', 'Two shows back to back', dur=6.6, size=96)
cue('s16_nick', T('c01', 41.8), 'P4 · FIRST-TIMERS BODYBUILDING', 'Really happy with the look — and the process', sub_at=48.2 - 41.8, dur=9.0, kicker='NICK')
x_card('x_mark_card', '3784_card.mp4', "<b>MARK</b> &nbsp;MASTERS MEN'S PHYSIQUE", w=640, top=96)
s = T('c01', 70.5)
chips('s18_markprep', s, "MARK'S PREP", [('5-WEEK PREP', 70.9 - 70.5), ('-10 KG', 81.6 - 70.5), ('FINAL 3 WEEKS: LOCKED IN', 88.8 - 70.5)], 'P4', 95.2 - 70.5, dur=97.6 - 70.5)
x_lads('x_mark_photo')
steps('s20_ahead', T('c01', 127.0), "WHAT'S NEXT", 'THE ROAD AHEAD', [
    ('NPC Big Man Weekend', 128.4 - 127.0, '01', ('Alicante · Pro Qualifier · end of this month', 130.0 - 127.0)),
    ('NPC Nationals — Dallas, Texas', 139.1 - 127.0, '02', ('December · final show of the season', 142.8 - 127.0))], dur=146.9 - 127.0)
def logo_pop(name, t0, f, w, dur):
    media(name, [f])
    css = f"""#G {{ position:absolute; left:110px; top:120px; width:{w}px; filter:drop-shadow(0 14px 30px rgba(0,0,0,0.65)); }}"""
    js = f"""tl.fromTo("#G", {{ opacity:0, scale:1.5, rotation:-6 }}, {{ opacity:1, scale:1, rotation:0, duration:0.5*K, ease:"power4.out", immediateRender:false }}, 0.05*K);
tl.fromTo("#G", {{ y:0 }}, {{ y:-10, duration:{dur - 1:.2f}*K, ease:"sine.inOut", immediateRender:false }}, 0.55*K);
tl.to("#G", {{ opacity:0, scale:0.9, duration:0.35*K, ease:"power2.in" }}, {dur - 0.38:.3f}*K);"""
    page(name, t0, dur, f'<img id="G" src="assets/{f}">', js, css)
logo_pop('s20b_bigman', T('c01', 128.3), 'bigman-weekend-logo.png', 400, T('c01', 138.9) - T('c01', 128.3))
logo_pop('s20c_nationals', T('c01', 139.1), 'npc-nationals-logo.png', 330, T('c01', 146.8) - T('c01', 139.1))
top_tag('s21_edu', T('c01', 160.8), 'COMING SOON', 'MORE EDUCATIONAL CONTENT', dur=6.0, right=True)
big_title('s22_outro', T('c01', 171.2), 'HAVE A GOOD WEEK', 'SEE YOU NEXT TIME', dur=END / FPS - T('c01', 171.2), fade_black=True)

json.dump(made, open(ROOT + '/made_show.json', 'w'), indent=1)
made.clear(); teaser(json.load(open(PRJ + '/show/teaser/teaser.json'))); json.dump(made, open(ROOT + '/made_teaser.json', 'w'), indent=1)
print(len(made), 'show comps')
for m in made: print(f"{m['name']:16s} {m['rec'] / FPS:8.2f}s  {m['frames'] / FPS:5.1f}s")
