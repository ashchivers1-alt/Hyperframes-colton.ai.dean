"""v6 overlay — stage reel (Rachel fit model, Gabriella bikini, Katka PCA masters bikini 45+). One full-length alpha comp:
flash cuts at each segment change, athlete plates, round chips, logo bug. Reuses HEAD + page() from build_v3."""
import shutil

src = open('build_v3.py').read()
exec(src[:src.index('# ---------- LEG DAY opener')])
made.clear()

D = 3703 / 30            # matches the stage section on V1
CUTS = [24.6333, 38.5333, 61.9, 91.9667]
css = """
#fl { position:absolute; inset:0; background:#fff; opacity:0; }
#bug { position:absolute; right:36px; bottom:30px; width:150px; opacity:0; filter:drop-shadow(0 4px 12px rgba(0,0,0,0.6)); }
#op { position:absolute; left:0; right:0; top:360px; text-align:center; }
#op .k { font-weight:800; font-size:24px; letter-spacing:0.5em; color:#ff3b30; }
#op .big { font-family:"Bebas Neue"; font-size:230px; line-height:0.86; letter-spacing:0.04em; text-shadow:0 0 40px rgba(255,255,255,0.25), 0 14px 50px rgba(0,0,0,0.8); }
#op .s { font-weight:700; font-size:26px; letter-spacing:0.3em; margin-top:10px; }
#opd { position:absolute; inset:0; background:radial-gradient(ellipse 60% 55% at 50% 50%, rgba(0,0,0,0.55), rgba(0,0,0,0) 75%); opacity:0; }
.pl { position:absolute; left:52px; bottom:72px; padding:20px 150px 22px 30px; border-radius:12px; opacity:0;
  background:linear-gradient(90deg, rgba(0,0,0,0.84) 0%, rgba(0,0,0,0.70) 65%, rgba(0,0,0,0) 100%); box-shadow:0 0 40px 10px rgba(0,0,0,0.2); }
.pl .k { font-weight:800; font-size:18px; letter-spacing:0.4em; color:#ff3b30; }
.pl .nmw { overflow:hidden; padding-bottom:4px; }
.pl .nm { font-family:"Bebas Neue"; font-size:110px; line-height:0.88; margin-top:4px; }
.pl .rule { width:110px; height:3px; background:#ff3b30; margin:8px 0 10px; transform-origin:0 50%; }
.pl .s1 { font-weight:800; font-size:23px; letter-spacing:0.18em; white-space:nowrap; }
.pl .s2 { font-weight:600; font-size:22px; margin-top:6px; color:#dcdcdc; white-space:nowrap; }
.ch { position:absolute; left:52px; top:44px; display:flex; align-items:center; gap:14px; padding:10px 20px 9px 16px; border-radius:6px; opacity:0;
  background:rgba(0,0,0,0.6); border:2px solid rgba(255,255,255,0.85); font-weight:800; font-size:24px; letter-spacing:0.26em; }
.ch i { width:12px; height:12px; border-radius:50%; background:#ff3b30; box-shadow:0 0 12px #ff3b30; }
#pca { position:absolute; left:0; right:0; top:420px; text-align:center; opacity:0; }
#pca .k { font-weight:800; font-size:22px; letter-spacing:0.5em; color:#6f93ff; }
#pca .big { font-family:"Bebas Neue"; font-size:150px; line-height:0.9; text-shadow:0 12px 40px rgba(0,0,0,0.8); }
"""
def plate(i, k, nm, s1, s2=''):
    return (f'<div class="pl shadow" id="p{i}"><div class="k">{k}</div><div class="nmw"><div class="nm">{nm}</div></div><div class="rule"></div>'
            f'<div class="s1">{s1}</div>' + (f'<div class="s2">{s2}</div>' if s2 else '') + '</div>')
chip = lambda i, t: f'<div class="ch shadow" id="c{i}"><i></i>{t}</div>'
body = ('<div id="opd"></div><div id="op"><div class="k">TEAM APEXX · ON STAGE</div><div class="big">STAGE DAY</div>'
        '<div class="s">TBJP INTERNATIONAL BRITISH FINALS</div></div>'
        + plate(0, 'ATHLETE · FIT MODEL', 'RACHEL', 'OPEN PRO QUALIFIER · FIT MODEL', 'Second from left')
        + plate(1, 'ATHLETE · BIKINI', 'GABRIELLA', 'OPEN PRO QUALIFIER · BIKINI')
        + plate(2, 'ATHLETE · PCA BRITISH FINALS', 'KATKA', 'MASTERS BIKINI 45+')
        + chip(0, 'COMPARISONS') + chip(1, 'INDIVIDUAL ROUTINE') + chip(2, 'INDIVIDUAL ROUTINE') + chip(3, 'COMPARISONS') + chip(4, 'I-WALK')
        + '<div id="pca"><div class="k">MEANWHILE IN TELFORD</div><div class="big">PCA BRITISH FINALS</div></div>'
        + '<img id="bug" src="assets/apexx-logo.png"/><div id="fl"></div>')

def pin(i, t, hold):
    return (f'tl.fromTo("#p{i}", {{ opacity:0, x:-50 }}, {{ opacity:1, x:0, duration:f(0.45), ease:"expo.out", immediateRender:false }}, f({t}));\n'
            f'tl.fromTo("#p{i} .nm", {{ yPercent:110 }}, {{ yPercent:0, duration:f(0.5), ease:"expo.out", immediateRender:false }}, f({t}+0.12));\n'
            f'tl.fromTo("#p{i} .rule", {{ scaleX:0 }}, {{ scaleX:1, duration:f(0.35), ease:"power3.inOut", immediateRender:false }}, f({t}+0.3));\n'
            f'tl.to("#p{i}", {{ opacity:0, x:-30, duration:f(0.35), ease:"power2.in" }}, f({t + hold}));\n')
def cin(i, t, hold):
    return (f'tl.fromTo("#c{i}", {{ opacity:0, y:-16 }}, {{ opacity:1, y:0, duration:f(0.35), ease:"back.out(1.6)", immediateRender:false }}, f({t}));\n'
            f'tl.to("#c{i}", {{ opacity:0, y:-10, duration:f(0.3), ease:"power2.in" }}, f({t + hold}));\n')
def flash(t):
    return (f'tl.fromTo("#fl", {{ opacity:0 }}, {{ opacity:0.85, duration:f(0.08), ease:"none", immediateRender:false }}, f({t} - 0.08));\n'
            f'tl.to("#fl", {{ opacity:0, duration:f(0.35), ease:"power2.out" }}, f({t}));\n')

js = 'gsap.set(["#op",".pl",".ch","#pca","#fl","#bug"], { opacity:0 });\n'
# cold open title
js += ('tl.to("#opd", { opacity:1, duration:f(0.3) }, 0);\n'
       'tl.fromTo("#op", { opacity:0, scale:1.15, filter:"blur(14px)" }, { opacity:1, scale:1, filter:"blur(0px)", duration:f(0.6), ease:"expo.out", immediateRender:false }, f(0.15));\n'
       'tl.to("#op .big", { scale:1.05, duration:f(2.6), ease:"none" }, f(0.75));\n'
       'tl.to(["#op","#opd"], { opacity:0, y:-20, filter:"blur(10px)", duration:f(0.4), ease:"power2.in" }, f(3.2));\n')
js += 'tl.fromTo("#bug", { opacity:0 }, { opacity:0.92, duration:f(0.5), immediateRender:false }, f(3.6));\n'
js += pin(0, 3.8, 6.5) + cin(0, 3.8, 6.5)
js += flash(CUTS[0]) + cin(1, CUTS[0] + 0.2, 5.0)
js += flash(CUTS[1]) + pin(1, CUTS[1] + 0.3, 6.5) + cin(2, CUTS[1] + 0.3, 6.5)
js += flash(CUTS[2]) + cin(3, CUTS[2] + 0.2, 5.0)
js += flash(CUTS[3])
js += (f'tl.fromTo("#pca", {{ opacity:0, scale:1.1 }}, {{ opacity:1, scale:1, duration:f(0.5), ease:"expo.out", immediateRender:false }}, f({CUTS[3]} + 0.15));\n'
       f'tl.to("#pca", {{ opacity:0, y:-20, duration:f(0.35), ease:"power2.in" }}, f({CUTS[3]} + 2.6));\n')
js += pin(2, CUTS[3] + 3.0, 7.0) + cin(4, CUTS[3] + 3.0, 7.0)
js += f'tl.to("#bug", {{ opacity:0, duration:f(0.5) }}, f({D} - 0.7));\n'
page('v6-stage', round(D, 3), body, js, css)
shutil.copy('../../v5/media/apexx-logo.png', 'comps/v6-stage/assets/apexx-logo.png')
print(made, D)
