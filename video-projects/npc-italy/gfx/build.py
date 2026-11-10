"""NPC Italy vlog graphics (1920x1080 alpha). One Hyperframes comp per graphic + one per caption section.
Team Apexx look: Bebas Neue display, Montserrat text, red #d80609 accent, soft dark backing, calm slide/fade motion.
Comps render at 24 fps with times divided by 1.001, then are conformed to 23.976 so they line up exactly."""
import json, os, shutil, html
ROOT = os.path.dirname(os.path.abspath(__file__))
WS = '/Users/ashleychivers/Documents/Claude Video Studio'
GSAP = WS + '/video-projects/training-day/gfx/assets/gsap.min.js'
HFJSON = WS + '/video-projects/training-day/gfx/hyperframes.json'
P = json.load(open(ROOT + '/../plan.json')); FPS = P['fps']; M = P['marks']
CAPS = json.load(open(ROOT + '/../captions.json'))
K = 1 / 1.001    # comp-time scale (rendered at 24, played at 23.976)
SCALE = 2        # comps are laid out at 1920x1080 and rendered at SCALE x (2 = 3840x2160 UHD)
W, H = 1920 * SCALE, 1080 * SCALE

HEAD = """<!doctype html><html lang="en"><head><meta charset="UTF-8" />
<meta name="viewport" content="width=%W%, height=%H%" /><script src="assets/gsap.min.js"></script>
<style>
@font-face { font-family:'Apple Color Emoji'; src: local('Apple Color Emoji'); }
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:%W%px; height:%H%px; overflow:hidden; background:transparent; }
#stage { position:relative; width:%W%px; height:%H%px; overflow:hidden; }
#stage > #root { transform:scale(%S%); transform-origin:0 0; }
#root { position:relative; width:1920px; height:1080px; overflow:hidden; font-family:Montserrat, sans-serif; color:#f6f6f6; }
.sh { text-shadow:0 3px 18px rgba(0,0,0,0.75), 0 1px 3px rgba(0,0,0,0.7); }
.back { position:absolute; left:-200px; bottom:-220px; width:1500px; height:760px;
  background:radial-gradient(ellipse 55% 50% at 30% 62%, rgba(0,0,0,0.62), rgba(0,0,0,0) 70%); }
.k { font-weight:800; font-size:22px; letter-spacing:0.3em; color:rgba(255,255,255,0.88); display:flex; align-items:center; gap:16px; }
.k i { display:inline-block; width:40px; height:4px; background:#d80609; }
.t { font-family:"Bebas Neue", sans-serif; line-height:0.9; letter-spacing:0.01em; white-space:nowrap; }
.s { font-weight:600; font-size:27px; color:#d6d6d6; letter-spacing:0.02em; }
.clip { overflow:hidden; padding-bottom:6px; }
%CSS%
</style></head><body>
<div id="stage" data-composition-id="main" data-start="0" data-duration="%DUR%" data-width="%W%" data-height="%H%"><div id="root">%BODY%</div></div>
<script>(() => { const tl = gsap.timeline({ paused:true }); const K = %K%;
%JS%
tl.to({}, { duration:%DUR% }, 0); window.__timelines = window.__timelines || {}; window.__timelines["main"] = tl; })();</script>
</body></html>"""

made = []
def page(name, dur, body, js, css='', rec=None, assets=()):
    d = f'{ROOT}/comps/{name}'; os.makedirs(d + '/assets', exist_ok=True)
    open(f'{d}/index.html', 'w').write(HEAD.replace('%DUR%', f'{dur * K:.3f}').replace('%BODY%', body)
                                     .replace('%JS%', js).replace('%CSS%', css).replace('%K%', f'{K:.6f}')
                                     .replace('%W%', str(W)).replace('%H%', str(H)).replace('%S%', str(SCALE)))
    shutil.copy(HFJSON, d); shutil.copy(GSAP, d + '/assets/')
    for a in assets: shutil.copy(a, d + '/assets/')
    open(f'{d}/meta.json', 'w').write(json.dumps({"id": name, "name": name, "width": W, "height": H, "fps": 24}))
    made.append(dict(name=name, rec=rec, frames=round(dur * FPS)))

def at(mark, sec=0.0): return M[mark] + round(sec * FPS)
E = lambda s: html.escape(s)

# entrance/exit shared by lower-third style blocks (times in real seconds, scaled by K in JS)
def lt_js(root, hold):
    return f"""const r="{root}"; gsap.set([r+" .back", r+" .k", r+" .t", r+" .s", r+" .x"], {{ opacity:0 }});
tl.to(r+" .back", {{ opacity:1, duration:0.5*K }}, 0);
tl.fromTo(r+" .k", {{ opacity:0, x:-30 }}, {{ opacity:1, x:0, duration:0.45*K, ease:"power3.out", immediateRender:false }}, 0.1*K);
tl.fromTo(r+" .t", {{ opacity:0, yPercent:105 }}, {{ opacity:1, yPercent:0, duration:0.6*K, ease:"expo.out", immediateRender:false }}, 0.2*K);
tl.fromTo(r+" .s, "+r+" .x", {{ opacity:0, y:14 }}, {{ opacity:1, y:0, duration:0.5*K, ease:"power2.out", stagger:0.08*K, immediateRender:false }}, 0.5*K);
tl.to([r+" .k", r+" .t", r+" .s", r+" .x"], {{ opacity:0, x:-24, duration:0.4*K, ease:"power2.in", stagger:0.04*K }}, {hold - 0.45:.3f}*K);
tl.to(r+" .back", {{ opacity:0, duration:0.5*K }}, {hold - 0.35:.3f}*K);"""

def lower_third(name, rec, kicker, title, sub=None, dur=5.5, size=96, extra_body='', extra_css='', assets=()):
    body = (f'<div class="back"></div><div id="L" class="sh" style="position:absolute; left:80px; bottom:96px;">'
            f'{extra_body}<div class="k"><i></i>{E(kicker)}</div>'
            f'<div class="clip"><div class="t" style="font-size:{size}px; margin-top:10px;">{E(title)}</div></div>'
            + (f'<div class="s" style="margin-top:8px;">{E(sub)}</div>' if sub else '') + '</div>')
    page(name, dur, body, lt_js('#L', dur), extra_css, rec, assets)

def top_tag(name, rec, kicker, title, dur=6.0):
    css = """#T { position:absolute; left:64px; top:56px; }
#T .pill { display:inline-block; background:#d80609; font-weight:800; font-size:19px; letter-spacing:0.26em; padding:7px 14px 6px; }
#T .t { font-size:62px; margin-top:10px; }"""
    body = f'<div id="T" class="sh"><div class="pill k">{E(kicker)}</div><div class="clip"><div class="t">{E(title)}</div></div></div>'
    js = f"""gsap.set(["#T .pill","#T .t"], {{ opacity:0 }});
tl.fromTo("#T .pill", {{ opacity:0, x:-24 }}, {{ opacity:1, x:0, duration:0.4*K, ease:"power3.out", immediateRender:false }}, 0.05*K);
tl.fromTo("#T .t", {{ opacity:0, yPercent:105 }}, {{ opacity:1, yPercent:0, duration:0.55*K, ease:"expo.out", immediateRender:false }}, 0.15*K);
tl.to(["#T .pill","#T .t"], {{ opacity:0, x:-20, duration:0.35*K, ease:"power2.in", stagger:0.05*K }}, {dur - 0.4:.3f}*K);"""
    page(name, dur, body, js, css, rec)

def speed_chip(name, rec, dur, label):
    css = """#C { position:absolute; right:64px; top:56px; display:flex; align-items:center; gap:12px; padding:10px 18px 9px;
  background:rgba(10,10,10,0.55); border:1px solid rgba(255,255,255,0.18); border-radius:6px; font-weight:800; font-size:24px; letter-spacing:0.14em; }
#C b { color:#d80609; font-size:22px; letter-spacing:-0.1em; }"""
    body = f'<div id="C"><b>&#9654;&#9654;</b>{E(label)}</div>'
    js = f"""gsap.set("#C", {{ opacity:0 }});
tl.fromTo("#C", {{ opacity:0, y:-12 }}, {{ opacity:1, y:0, duration:0.3*K, ease:"power2.out", immediateRender:false }}, 0.05*K);
tl.to("#C b", {{ opacity:0.35, duration:0.5*K, yoyo:true, repeat:{max(1, int(dur / 0.5) - 2)}, ease:"sine.inOut" }}, 0.4*K);
tl.to("#C", {{ opacity:0, duration:0.25*K }}, {dur - 0.3:.3f}*K);"""
    page(name, dur, body, js, css, rec)

def exercise(name, rec, n, total, title, sets, reps, note=None, pos='bl', dur=6.0):
    css = f"""#X {{ position:absolute; {'left:80px; bottom:96px;' if pos == 'bl' else 'left:72px; top:64px;'} }}
#X .idx {{ font-family:"Bebas Neue"; font-size:40px; letter-spacing:0.12em; color:#d80609; }}
#X .idx span {{ color:rgba(255,255,255,0.7); }}
#X .rule {{ width:120px; height:3px; background:#d80609; margin:8px 0 12px; transform-origin:0 50%; }}
#X .t {{ font-size:100px; }}
#X .x {{ display:inline-block; margin-top:16px; padding:8px 16px 7px; border:2px solid rgba(255,255,255,0.85); border-radius:4px;
  font-weight:800; font-size:27px; letter-spacing:0.22em; background:rgba(0,0,0,0.35); }}
#X .x b {{ color:#d80609; }}
#X .note {{ margin-top:14px; font-weight:600; font-size:27px; color:#e6e6e6; }}"""
    back = '<div class="back"></div>' if pos == 'bl' else '<div class="back" style="top:-260px; bottom:auto;"></div>'
    body = (back + f'<div id="X" class="sh"><div class="k idx">{n:02d} <span>/ {total:02d}</span></div><div class="rule"></div>'
            f'<div class="clip"><div class="t">{E(title)}</div></div><div class="x">{E(sets)} <b>&middot;</b> {E(reps)}</div>'
            + (f'<div class="note s x" style="border:none; background:none; padding:0; letter-spacing:0.02em; font-size:27px; display:block;">{E(note)}</div>' if note else '')
            + '</div>')
    js = lt_js('#X', dur) + '\ngsap.set("#X .rule", { scaleX:0 }); tl.to("#X .rule", { scaleX:1, duration:0.5*K, ease:"power3.inOut" }, 0.25*K);'
    page(name, dur, body, js, css, rec)

def quote(name, rec, text, dur=6.5):
    css = """#Q { position:absolute; left:80px; top:250px; width:780px; }
#Q .mk { font-family:"Bebas Neue"; font-size:170px; line-height:0.6; color:#d80609; height:70px; }
#Q .q { font-weight:800; font-size:52px; line-height:1.14; letter-spacing:-0.01em; }
#Q .rule { width:90px; height:4px; background:#d80609; margin-top:22px; transform-origin:0 50%; }"""
    body = (f'<div class="back" style="left:-300px; top:60px; bottom:auto; height:700px;"></div>'
            f'<div id="Q" class="sh"><div class="mk">&ldquo;</div><div class="q">{E(text)}</div><div class="rule"></div></div>')
    js = f"""gsap.set(["#Q .mk","#Q .q",".back"], {{ opacity:0 }}); gsap.set("#Q .rule", {{ scaleX:0 }});
tl.to(".back", {{ opacity:1, duration:0.5*K }}, 0);
tl.fromTo("#Q .mk", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.45*K, ease:"power3.out", immediateRender:false }}, 0.05*K);
tl.fromTo("#Q .q", {{ opacity:0, y:24 }}, {{ opacity:1, y:0, duration:0.6*K, ease:"expo.out", immediateRender:false }}, 0.2*K);
tl.to("#Q .rule", {{ scaleX:1, duration:0.5*K, ease:"power3.inOut" }}, 0.55*K);
tl.to(["#Q .mk","#Q .q","#Q .rule",".back"], {{ opacity:0, duration:0.4*K, ease:"power2.in" }}, {dur - 0.45:.3f}*K);"""
    page(name, dur, body, js, css, rec)

def captions(key, rec, dur, offset=0.0):
    css = """.cap { position:absolute; left:160px; right:160px; bottom:74px; text-align:center; opacity:0;
  font-weight:700; font-size:44px; line-height:1.2; letter-spacing:0.005em; color:#fff;
  text-shadow:0 0 2px #000, 0 2px 4px rgba(0,0,0,0.9), 0 4px 18px rgba(0,0,0,0.75); }"""
    body, js = [], []
    for k, p in enumerate(CAPS[key]):
        a, b = p['start'] - offset, p['end'] - offset
        if b <= 0 or a >= dur: continue
        a = max(0.0, a); b = min(dur - 0.05, b)
        body.append(f'<div class="cap" id="c{k}">{E(p["text"])}</div>')
        js.append(f'tl.set("#c{k}", {{ opacity:1 }}, {a * K:.3f}); tl.set("#c{k}", {{ opacity:0 }}, {b * K:.3f});')
    page(f'cap_{key}', dur, ''.join(body), '\n'.join(js), css, rec)

# ----------------------------------------------------------------- the edit's graphics
lower_third('g01_milan', at('i0', 2.0), 'AMATEUR OLYMPIA WEEKEND', 'MILANO, ITALY', dur=5.5)
lower_third('g02_admin', at('i2', 0.6), 'BEHIND THE SCENES', 'CHECK-INS + ADMIN', dur=5.0)
speed_chip('g03_hyper_speed', at('i2', 0.2), (M['i3'] - M['i2']) / FPS - 0.5, '8×')
top_tag('g04_topic_reverse', at('i3', 0.6), 'POST-SHOW', 'REVERSE DIETING', dur=6.0)
logo = WS + '/video-projects/npc-italy/src/dl/golds-gym-logo.png'
lower_third('g05_golds', at('i6', 0.5), 'CLIENT CHECK-IN · GABRIELLA', "GOLD'S GYM MILAN", dur=6.5, size=104,
            extra_body='<img class="x" src="assets/golds-gym-logo.png" style="width:150px; height:150px; display:block; margin-bottom:18px; filter:drop-shadow(0 6px 16px rgba(0,0,0,0.6));">',
            assets=(logo,))
lower_third('g06_nextday', at('i10', 0.2), 'THE NEXT DAY', 'TRAINING AT GOLD’S', dur=4.8, size=84)
lower_third('g07_voicenote', at('i11', 0.4), 'WHATSAPP', 'VOICE NOTE TO A CLIENT', dur=5.0, size=84)
for k in ('vn_fast1', 'vn_fast3'):
    r, n = M[k]; speed_chip(f'g08_{k}', r, n / FPS, '5×')
top_tag('g09_topic_life', at('i12', 0.6), 'COACHING', 'LIFE STILL HAPPENS ON PREP', dur=6.0)
EX = [(17, 'FLAT MACHINE CHEST PRESS', '2 SETS', '8–12 REPS', None, 'bl', 1.0),
      (18, 'TRICEP DIP MACHINE', '3 SETS', '10–15 REPS', None, 'bl', 0.6),
      (19, 'PULL-UPS', '3 SETS', '10–15 REPS', 'Only because it was sunny ☀️ Why not?', 'bl', 0.6),
      (20, 'MACHINE CHEST PRESS', '3 SETS', '8–12 REPS', None, 'tl', 0.6),
      (21, 'MACHINE PULLOVER', '3 SETS', '8–12 REPS', None, 'bl', 0.6),
      (22, 'MACHINE PREACHER CURL', '3 SETS', '10–15 REPS', None, 'bl', 0.6),
      (24, 'MACHINE SIDE LATERAL RAISE', '3 SETS', '10–15 REPS', None, 'bl', 0.3)]
for n, (item, title, s, r, note, pos, off) in enumerate(EX, 1):
    exercise(f'g10_ex{n}', at(f'i{item}', off), n, len(EX), title, s, r, note, pos, dur=6.5 if note else 6.0)
q20 = next(p for p in CAPS['20'] if p['text'].startswith('I literally'))
quote('g11_quote_feel', at('i20', q20['start'] - 0.2), 'I literally just train what feels good.', dur=6.0)
# posing room — "always being held accountable by my team" (left wall space, clear of Ash)
css = """#A { position:absolute; left:84px; top:330px; }
#A .k { font-size:36px; margin-bottom:8px; color:#fff; }
#A .acc { position:relative; font-size:140px; color:#fff; }
#A .acc .w { display:inline-block; overflow:hidden; padding-bottom:4px; vertical-align:bottom; }
#A .acc .w span { display:inline-block; }
#A .acc .gl { position:absolute; left:0; top:0; color:transparent; text-shadow:none; pointer-events:none;
  background:linear-gradient(100deg, rgba(255,255,255,0) 42%, rgba(255,255,255,0.95) 50%, rgba(255,255,255,0) 58%);
  background-size:300% 100%; background-position:100% 0; -webkit-background-clip:text; background-clip:text; }
#A .team { position:relative; display:inline-block; margin-top:14px; padding:10px 22px 4px; }
#A .team .bar { position:absolute; inset:0; background:#d80609; transform-origin:left center; }
#A .team .t { position:relative; font-size:92px; color:#fff; }"""
word = ''.join(f'<span class="w"><span>{c}</span></span>' for c in 'ACCOUNTABLE')
body = ('<div class="back" style="left:-300px; top:120px; bottom:auto; width:1400px; height:800px; background:radial-gradient(ellipse 50% 50% at 40% 50%, rgba(0,0,0,0.7), rgba(0,0,0,0) 72%);"></div>'
        '<div id="A" class="sh"><div class="k"><i></i>ALWAYS BEING HELD</div>'
        f'<div class="acc t">{word}<div class="gl t">ACCOUNTABLE</div></div>'
        '<div><div class="team"><div class="bar"></div><div class="t">BY MY TEAM</div></div></div></div>')
pd = (M['i28'] - M['i26']) / FPS - 0.3
js = f"""gsap.set([".back", "#A .k"], {{ opacity:0 }}); gsap.set("#A .acc .w span", {{ yPercent:110 }});
gsap.set("#A .team .bar", {{ scaleX:0 }}); gsap.set("#A .team .t", {{ opacity:0, x:-20 }});
tl.to(".back", {{ opacity:1, duration:0.6*K }}, 0.3*K);
tl.fromTo("#A .k", {{ opacity:0, x:-30 }}, {{ opacity:1, x:0, duration:0.5*K, ease:"power3.out", immediateRender:false }}, 0.5*K);
tl.to("#A .acc .w span", {{ yPercent:0, duration:0.7*K, ease:"expo.out", stagger:0.045*K }}, 0.8*K);
tl.to("#A .acc .gl", {{ backgroundPosition:"0% 0", duration:1.1*K, ease:"power2.inOut" }}, 1.7*K);
tl.to("#A .team .bar", {{ scaleX:1, duration:0.5*K, ease:"power4.inOut" }}, 2.2*K);
tl.to("#A .team .t", {{ opacity:1, x:0, duration:0.45*K, ease:"back.out(1.6)" }}, 2.5*K);
tl.fromTo("#A .acc .gl", {{ backgroundPosition:"100% 0" }}, {{ backgroundPosition:"0% 0", duration:1.1*K, ease:"power2.inOut", immediateRender:false }}, 7.5*K);
tl.to("#A", {{ opacity:0, x:-40, duration:0.5*K, ease:"power2.in" }}, {pd - 0.6:.3f}*K);
tl.to(".back", {{ opacity:0, duration:0.5*K }}, {pd - 0.5:.3f}*K);"""
page('g12_accountable', pd, body, js, css, at('i26', 0.0))
lower_third('g13_showday', at('i31', 0.6), 'SUNDAY · AMATEUR OLYMPIA ITALY', 'SHOW DAY', 'Crowne Plaza Milan Linate', dur=6.5, size=170)
lower_third('g14_final_checkin', at('i33', 0.4), 'BACKSTAGE', 'FINAL CHECK-IN · GAB', dur=4.5, size=76)
lower_third('g15_stage', at('i37', 0.8), 'AMATEUR OLYMPIA ITALY', 'BIKINI', 'Milan · NPC Worldwide', dur=5.5, size=110)
top_tag('g16_topic_post', at('i44', 0.8), 'POST-SHOW', 'THE REAL RESULT', dur=6.0)
q44 = next(p for p in CAPS['44'] if 'not to judge' in p['text'] or p['text'].startswith('show or your prep'))
quote('g17_quote_result', at('i44', q44['start'] - 0.3), 'Don’t judge your show by the result. Bring your best to stage.', dur=7.0)
# captions per talking section (offset: the clip transcript starts at the item start)
for key, item in (('03', 3), ('04', 4), ('12', 12), ('20', 20), ('44', 44)):
    captions(key, M[f'i{item}'], (M[f'i{item + 1}'] - M[f'i{item}']) / FPS)
json.dump(made, open(ROOT + '/made.json', 'w'), indent=1)
print(len(made), 'comps:', ' '.join(m['name'] for m in made))

# ======================= EDIT 02 additions =======================
def svgpage(name, dur, body, js, css, rec):
    page(name, dur, body, js, css, rec)

# 1) Menstrual-cycle recovery diagram — slides up from behind Ash (composited under his matte later)
css = """#D { position:absolute; left:1340px; top:170px; width:540px; }
#D .card { background:rgba(10,10,10,0.72); border:1px solid rgba(255,255,255,0.16); border-radius:14px; padding:28px 30px 26px; }
#D .k { margin-bottom:16px; }
#D .row { display:flex; align-items:center; gap:16px; margin:14px 0; font-weight:700; font-size:27px; }
#D .row .n { flex:none; font-family:"Bebas Neue"; font-size:44px; line-height:1; color:#d80609; width:40px; text-align:center; }
#D .arr { width:3px; height:26px; background:rgba(255,255,255,0.35); margin-left:19px; }
#D .end { margin-top:18px; padding:12px 16px 10px; border-radius:8px; background:#d80609; font-family:"Bebas Neue"; font-size:40px; letter-spacing:0.03em; text-align:center; }"""
body = ('<div id="D"><div class="card"><div class="k"><i></i>POST-SHOW RECOVERY</div>'
        '<div class="row r1"><span class="n">1</span>Calories up to maintenance</div><div class="arr a1"></div>'
        '<div class="row r2"><span class="n">2</span>Cardio &amp; output down</div><div class="arr a2"></div>'
        '<div class="row r3"><span class="n">3</span>Energy balance restored</div>'
        '<div class="end">MENSTRUAL CYCLE RETURNS</div></div></div>')
dd = 15.0
js = f"""gsap.set("#D", {{ y:520 }}); gsap.set(["#D .row","#D .arr","#D .end"], {{ opacity:0 }});
tl.to("#D", {{ y:0, duration:0.9*K, ease:"power3.out" }}, 0.1*K);
tl.fromTo("#D .r1", {{ opacity:0, x:-16 }}, {{ opacity:1, x:0, duration:0.4*K, ease:"power2.out", immediateRender:false }}, 0.9*K);
tl.to("#D .a1", {{ opacity:1, duration:0.3*K }}, 1.6*K);
tl.fromTo("#D .r2", {{ opacity:0, x:-16 }}, {{ opacity:1, x:0, duration:0.4*K, ease:"power2.out", immediateRender:false }}, 1.8*K);
tl.to("#D .a2", {{ opacity:1, duration:0.3*K }}, 2.6*K);
tl.fromTo("#D .r3", {{ opacity:0, x:-16 }}, {{ opacity:1, x:0, duration:0.4*K, ease:"power2.out", immediateRender:false }}, 2.8*K);
tl.fromTo("#D .end", {{ opacity:0, scale:0.92 }}, {{ opacity:1, scale:1, duration:0.5*K, ease:"back.out(2)", immediateRender:false }}, 4.0*K);
tl.to("#D", {{ y:560, duration:0.8*K, ease:"power3.in" }}, {dd - 0.9:.3f}*K);"""
page('g20_menstrual', dd, body, js, css, at('i3', 166.9))

# shared arrow/line drawing helpers (SVG, stroke-dash draw-on)
ARROW_CSS = """svg { position:absolute; inset:0; overflow:visible; }
.ln { fill:none; stroke:#fff; stroke-width:7; stroke-linecap:round; stroke-linejoin:round; filter:drop-shadow(0 2px 6px rgba(0,0,0,0.8)); }
.ln.red { stroke:#d80609; }
.lbl { position:absolute; font-weight:800; font-size:30px; color:#fff; padding:8px 14px 6px; background:rgba(10,10,10,0.7); border-left:5px solid #d80609; white-space:nowrap; }
"""
def draw_js(sel, at_s, dur=0.6):
    return f"""document.querySelectorAll("{sel}").forEach(p => {{ const L = p.getTotalLength(); gsap.set(p, {{ strokeDasharray:L, strokeDashoffset:L }}); }});
tl.to("{sel}", {{ strokeDashoffset:0, duration:{dur}*K, ease:"power2.inOut", stagger:0.12*K }}, {at_s}*K);"""

# 2) Flat machine chest press setup cues (static camera, item 17)
css = ARROW_CSS + "#l1 { left:60px; top:720px; } #l2 { left:1180px; top:120px; } #l3 { left:1290px; top:640px; }"
body = ('<svg viewBox="0 0 1920 1080">'
        '<path class="ln red p1" d="M 220 790 C 230 850, 240 900, 255 950"/><path class="ln red p1h" d="M 226 922 L 255 950 L 278 916"/>'
        '<path class="ln p2" d="M 1320 190 C 1270 260, 1250 300, 1240 350"/><path class="ln p2h" d="M 1215 318 L 1240 350 L 1262 316"/>'
        '<path class="ln p3" d="M 1280 640 C 1290 560, 1260 470, 1190 420"/><path class="ln p3h" d="M 1200 452 L 1190 420 L 1225 418"/>'
        '</svg>'
        '<div class="lbl" id="l1">FOOT PEDAL: PUSH DOWN</div>'
        '<div class="lbl" id="l2">HANDLES START IN FULL STRETCH</div>'
        '<div class="lbl" id="l3">DRIVE REP 1 WITH THE MOMENTUM</div>')
d17 = 26.0
js = f"""gsap.set(["#l1","#l2","#l3"], {{ opacity:0 }}); gsap.set("svg path", {{ opacity:1 }});
{draw_js('.p2, .p2h', 0.3)}
tl.fromTo("#l2", {{ opacity:0, y:-10 }}, {{ opacity:1, y:0, duration:0.35*K, immediateRender:false }}, 0.5*K);
{draw_js('.p1, .p1h', 6.5)}
tl.fromTo("#l1", {{ opacity:0, x:-12 }}, {{ opacity:1, x:0, duration:0.35*K, immediateRender:false }}, 6.7*K);
tl.to(["#l2",".p2",".p2h"], {{ opacity:0, duration:0.4*K }}, 11.5*K);
{draw_js('.p3, .p3h', 14.5, 0.8)}
tl.fromTo("#l3", {{ opacity:0, x:12 }}, {{ opacity:1, x:0, duration:0.35*K, immediateRender:false }}, 14.8*K);
tl.to(["#l1","#l3","svg path"], {{ opacity:0, duration:0.45*K }}, {d17 - 0.5:.3f}*K);"""
page('g21_bench_cues', d17, body, js, css, at('i17', 22.5))

# 3) Preacher curl: seat low -> full stretch at the bottom (item 22, static camera)
css = ARROW_CSS + "#c1 { left:1180px; top:820px; } #c2 { left:180px; top:420px; }"
body = ('<svg viewBox="0 0 1920 1080">'
        '<path class="ln p4" d="M 1170 840 L 1050 900"/><path class="ln p4h" d="M 1075 862 L 1050 900 L 1094 905"/>'
        '<path class="ln red p5" style="stroke-width:10" d="M 720 520 C 680 590, 640 640, 600 690"/><path class="ln red p5h" style="stroke-width:10" d="M 600 646 L 600 690 L 642 676"/>'
        '</svg>'
        '<div class="lbl" id="c1">SEAT LOW</div>'
        '<div class="lbl" id="c2">ARMS FULLY LENGTHENED = BICEP STRETCH</div>')
d22 = 11.0
js = f"""gsap.set(["#c1","#c2"], {{ opacity:0 }});
{draw_js('.p4, .p4h', 0.2)}
tl.fromTo("#c1", {{ opacity:0, x:12 }}, {{ opacity:1, x:0, duration:0.35*K, immediateRender:false }}, 0.4*K);
{draw_js('.p5, .p5h', 2.4, 0.7)}
tl.fromTo("#c2", {{ opacity:0, y:-10 }}, {{ opacity:1, y:0, duration:0.35*K, immediateRender:false }}, 2.6*K);
tl.to(["#c1","#c2","svg path"], {{ opacity:0, duration:0.45*K }}, {d22 - 0.5:.3f}*K);"""
page('g22_curl_stretch', d22, body, js, css, at('i22', 10.2))
json.dump(made, open(ROOT + '/made.json', 'w'), indent=1)
