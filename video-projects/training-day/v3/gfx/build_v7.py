"""v7 overlays — closing wrap-up (park clip). Weekend results with athlete photos, what's-next show list, subscribe nudge.
Times are local to each overlay; placement offsets from clip start in the session notes. Reuses HEAD + page() from build_v3."""
import shutil

src = open('build_v3.py').read()
exec(src[:src.index('# ---------- LEG DAY opener')])
made.clear()
PH = '../../v7/ph/'
LOGO = '../../v5/media/apexx-logo.png'

CSS = """
#ph { position:absolute; right:90px; top:90px; width:470px; height:627px; padding:12px; background:#f4f4f4; border-radius:6px;
  box-shadow:0 30px 80px rgba(0,0,0,0.55); transform:rotate(2.5deg); }
#ph .im { position:absolute; inset:12px 12px 12px 12px; overflow:hidden; border-radius:3px; background:#111; }
#ph .im img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
#ph .tape { position:absolute; left:50%; top:-16px; width:130px; height:34px; margin-left:-65px; background:rgba(255,59,48,0.85); transform:rotate(-3deg); }
#ph .logo { position:absolute; right:-36px; bottom:-30px; width:150px; filter:drop-shadow(0 6px 14px rgba(0,0,0,0.6)); transform:rotate(-6deg); }
.ex .badge { display:inline-flex; align-items:center; gap:12px; margin-top:14px; padding:8px 18px 7px; border-radius:4px; font-weight:800; font-size:28px;
  letter-spacing:0.18em; background:#ff3b30; }
.ex .badge.gold { background:linear-gradient(135deg, #f7d774, #c99a2e); color:#1b1400; }
.ex .badge .big { font-family:"Bebas Neue"; font-size:46px; letter-spacing:0.04em; line-height:0.9; }
.ex .sub { font-weight:700; font-size:22px; letter-spacing:0.2em; margin-top:12px; color:#e6e6e6; white-space:nowrap; }
"""

def result(name, dur, imgs, idx, nm, cls, badge_big, badge_txt, gold, sub):
    ims = ''.join(f'<img id="i{k}" src="assets/{im}"/>' for k, im in enumerate(imgs))
    body = (f'<div id="ph"><div class="im">{ims}</div><div class="tape"></div><img class="logo" src="assets/apexx-logo.png"/></div>'
            f'<div class="ex shadow"><div class="idx">{idx}</div><div class="rule"></div>'
            f'<div class="nmw"><div class="nm">{nm}</div></div><div class="sub">{cls}</div>'
            f'<div class="badge{" gold" if gold else ""}"><span class="big">{badge_big}</span>{badge_txt}</div>'
            f'<div class="sub" style="font-size:19px;color:#bdbdbd">{sub}</div></div>')
    js = ('gsap.set(["#ph",".ex",".ex .idx",".ex .rule",".ex .sub",".ex .badge"], { opacity:0 });\n'
          'tl.fromTo("#ph", { opacity:0, y:60, rotation:8 }, { opacity:1, y:0, rotation:2.5, duration:f(0.6), ease:"back.out(1.3)", immediateRender:false }, f(0.2));\n'
          'tl.fromTo("#ph .im img", { scale:1.0 }, { scale:1.07, duration:f(%s), ease:"none", immediateRender:false }, 0);\n' % dur +
          'tl.fromTo(".ex", { opacity:0, x:-50 }, { opacity:1, x:0, duration:f(0.45), ease:"expo.out", immediateRender:false }, f(0.5));\n'
          'tl.fromTo(".ex .idx", { opacity:0, x:-20 }, { opacity:1, x:0, duration:f(0.3), ease:"power2.out", immediateRender:false }, f(0.55));\n'
          'tl.fromTo(".ex .rule", { opacity:1, scaleX:0 }, { scaleX:1, duration:f(0.35), ease:"power3.inOut", immediateRender:false }, f(0.6));\n'
          'tl.fromTo(".ex .nm", { opacity:1, yPercent:110 }, { yPercent:0, duration:f(0.5), ease:"expo.out", immediateRender:false }, f(0.7));\n'
          'tl.fromTo(".ex .sub", { opacity:0, y:10 }, { opacity:1, y:0, duration:f(0.35), ease:"power3.out", stagger:0.6, immediateRender:false }, f(1.0));\n'
          'tl.fromTo(".ex .badge", { opacity:0, scale:0.6 }, { opacity:1, scale:1, duration:f(0.45), ease:"back.out(2)", immediateRender:false }, f(1.3));\n')
    if len(imgs) > 1:
        js += f'gsap.set("#i1", {{ opacity:0 }});\ntl.to("#i1", {{ opacity:1, duration:f(0.6) }}, f({dur / 2:.2f}));\n'
    js += (f'tl.to("#ph", {{ opacity:0, y:-40, rotation:-4, duration:f(0.4), ease:"power2.in" }}, f({dur} - 0.5));\n'
           f'tl.to(".ex", {{ opacity:0, x:-30, duration:f(0.35), ease:"power2.in" }}, f({dur} - 0.5));')
    page(name, dur, body, js, CSS)
    for im in imgs: shutil.copy(PH + im, f'comps/{name}/assets/{im}')
    shutil.copy(LOGO, f'comps/{name}/assets/apexx-logo.png')

result('v7-rachel', 17.0, ['r.jpg'], 'WEEKEND RESULTS · 01', 'RACHEL', 'FIT MODEL · 2 BROS PRO QUALIFIER', '5TH', 'PLACE', False, 'BRADFORD · TBJP BRITISH FINALS')
result('v7-gabriella', 18.0, ['g.jpg'], 'WEEKEND RESULTS · 02', 'GABRIELLA', 'BIKINI · 2 BROS PRO QUALIFIER', '🏆', 'WON BOTH CLASSES', True, 'BRADFORD · TBJP BRITISH FINALS')
result('v7-katka', 21.0, ['k.jpg'], 'WEEKEND RESULTS · 03', 'KATKA', 'MASTERS BIKINI 45+ · PCA BRITISH FINALS', '5TH', 'PLACE', False, 'TELFORD · STRONG LINE-UP')
result('v7-daniela', 19.5, ['d1.jpg', 'd2.jpg'], 'WEEKEND RESULTS · 04', 'DANIELA', 'WELLNESS · NPC KENTUCKY · USA', '🏆', 'BOTH CLASSES + OVERALL', True, 'NPC KENTUCKY BOURBON & KENTUCKY STATE')

# ---------- wrap-up title ----------
body = ('<div class="ex shadow"><div class="idx">TEAM APEXX</div><div class="rule"></div>'
        '<div class="nmw"><div class="nm">WEEKEND WRAP-UP</div></div><div class="chip">4 ATHLETES · <b>3 SHOWS</b> · 2 COUNTRIES</div></div>')
js = """gsap.set([".ex",".ex .idx",".ex .rule",".ex .chip"], { opacity:0 });
tl.fromTo(".ex", { opacity:0, x:-50 }, { opacity:1, x:0, duration:f(0.45), ease:"expo.out", immediateRender:false }, f(0.1));
tl.fromTo(".ex .idx", { opacity:0, x:-20 }, { opacity:1, x:0, duration:f(0.3), ease:"power2.out", immediateRender:false }, f(0.15));
tl.fromTo(".ex .rule", { opacity:1, scaleX:0 }, { scaleX:1, duration:f(0.35), ease:"power3.inOut", immediateRender:false }, f(0.2));
tl.fromTo(".ex .nm", { opacity:1, yPercent:110 }, { yPercent:0, duration:f(0.5), ease:"expo.out", immediateRender:false }, f(0.3));
tl.fromTo(".ex .chip", { opacity:0, y:12 }, { opacity:1, y:0, duration:f(0.35), ease:"back.out(1.6)", immediateRender:false }, f(0.7));
tl.to(".ex", { opacity:0, x:-30, duration:f(0.35), ease:"power2.in" }, f(5.6));"""
page('v7-wrap', 6.0, body, js)

# ---------- what's next (upcoming shows) ----------
ND = 32.0
SHOWS = [  # (local time, name, detail)
    (2.2, 'NPC ITALY', 'Amateur Olympia'), (8.3, 'COPENHAGEN', 'Pro Qualifier · TBC'), (11.7, 'ALICANTE', 'Pro Qualifier'),
    (15.7, 'TEXAS', 'Pro Qualifier · Attending'), (24.6, 'PCA FIRST TIMERS', ''), (27.6, 'PCA OPEN', 'Start of November')]
css = """
#nx { position:absolute; left:60px; top:90px; width:600px; padding:28px 34px 30px; border-radius:16px; border-left:6px solid #ff3b30;
  background:linear-gradient(160deg, rgba(14,14,16,0.9) 0%, rgba(8,8,10,0.82) 100%); box-shadow:0 30px 80px rgba(0,0,0,0.55); }
#nx .k { font-weight:800; font-size:18px; letter-spacing:0.4em; color:#ff3b30; }
#nx .h { font-family:"Bebas Neue"; font-size:96px; line-height:0.86; margin-top:6px; }
#nx .rule { width:110px; height:3px; background:#ff3b30; margin:12px 0 12px; transform-origin:0 50%; }
#nx .it { display:flex; align-items:center; gap:18px; padding:11px 0; border-bottom:1px solid rgba(255,255,255,0.12); }
#nx .it .d { width:14px; height:14px; border-radius:50%; background:#ff3b30; flex:none; box-shadow:0 0 12px rgba(255,59,48,0.8); }
#nx .it .n { font-family:"Bebas Neue"; font-size:44px; line-height:1; }
#nx .it .s { font-weight:600; font-size:20px; color:#cfcfcf; margin-left:auto; text-align:right; }
"""
items = ''.join(f'<div class="it" id="s{i}"><div class="d"></div><div class="n">{n}</div><div class="s">{d}</div></div>' for i, (_, n, d) in enumerate(SHOWS))
body = f'<div id="nx" class="shadow"><div class="k">TEAM APEXX · 2026 SEASON</div><div class="h">WHAT\'S NEXT</div><div class="rule"></div>{items}</div>'
js = 'gsap.set(["#nx"' + ''.join(f',"#s{i}"' for i in range(len(SHOWS))) + '], { opacity:0 });\n'
js += ('tl.fromTo("#nx", { opacity:0, x:-60 }, { opacity:1, x:0, duration:f(0.5), ease:"expo.out", immediateRender:false }, f(0.2));\n'
       'tl.fromTo("#nx .rule", { scaleX:0 }, { scaleX:1, duration:f(0.4), ease:"power3.inOut", immediateRender:false }, f(0.45));\n')
for i, (t, _, _) in enumerate(SHOWS):
    js += f'tl.fromTo("#s{i}", {{ opacity:0, x:30 }}, {{ opacity:1, x:0, duration:f(0.4), ease:"power3.out", immediateRender:false }}, f({t}));\n'
js += f'tl.to("#nx", {{ opacity:0, x:-40, duration:f(0.4), ease:"power2.in" }}, f({ND} - 0.5));'
page('v7-next', ND, body, js, css)

# ---------- subscribe nudge ----------
css = """
#sb { position:absolute; left:52px; bottom:72px; display:flex; align-items:center; gap:22px; padding:18px 40px 18px 22px; border-radius:14px;
  background:linear-gradient(90deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.7) 100%); box-shadow:0 0 40px 10px rgba(0,0,0,0.25); }
#sb img { width:150px; }
#sb .t { font-weight:800; font-size:20px; letter-spacing:0.32em; color:#cfcfcf; }
#sb .h { font-family:"Bebas Neue"; font-size:64px; line-height:0.95; margin-top:2px; }
#sb .btn { margin-left:12px; padding:14px 26px 12px; border-radius:8px; background:#ff3b30; font-weight:800; font-size:26px; letter-spacing:0.16em; }
#sb .bell { font-size:40px; margin-left:4px; }
"""
body = ('<div id="sb" class="shadow"><img src="assets/apexx-logo.png"/><div><div class="t">ENJOYING THE CHANNEL?</div>'
        '<div class="h">MORE EDUCATION COMING SOON</div></div><div class="btn">SUBSCRIBE</div><div class="bell">🔔</div></div>')
js = """gsap.set(["#sb","#sb .btn","#sb .bell"], { opacity:0 });
tl.fromTo("#sb", { opacity:0, x:-60 }, { opacity:1, x:0, duration:f(0.5), ease:"expo.out", immediateRender:false }, f(0.1));
tl.fromTo("#sb .btn", { opacity:0, scale:0.6 }, { opacity:1, scale:1, duration:f(0.4), ease:"back.out(2.2)", immediateRender:false }, f(0.7));
tl.fromTo("#sb .bell", { opacity:0, rotation:-30 }, { opacity:1, rotation:0, duration:f(0.4), ease:"back.out(2)", immediateRender:false }, f(1.0));
tl.to("#sb .bell", { keyframes:[{ rotation:-14, duration:0.1 },{ rotation:14, duration:0.1 },{ rotation:-8, duration:0.1 },{ rotation:0, duration:0.1 }] }, f(1.6));
tl.to("#sb .btn", { backgroundColor:"#3a3a3a", duration:f(0.2) }, f(3.2));
tl.set("#sb .btn", { textContent:"SUBSCRIBED ✓" }, f(3.2));
tl.to("#sb", { opacity:0, x:-30, duration:f(0.35), ease:"power2.in" }, f(8.1));"""
page('v7-sub', 8.5, body, js, css)
shutil.copy(LOGO, 'comps/v7-sub/assets/apexx-logo.png')
print(made)
