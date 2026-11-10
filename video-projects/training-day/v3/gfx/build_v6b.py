"""v6b overlay — beat-cut stage montage. Flash/punch on every cut, swapping athlete tag, intro title, triptych end card.
Timing comes from ../../v6/shots.json. Reuses HEAD + page() from build_v3."""
import json, shutil

src = open('build_v3.py').read()
exec(src[:src.index('# ---------- LEG DAY opener')])
made.clear()
SH = json.load(open('../../v6/shots.json')); shots, TOT = SH['shots'], SH['total']
INFO = {'R': ('RACHEL', 'FIT MODEL', 'TBJP BRITISH FINALS'),
        'G': ('GABRIELLA', 'BIKINI', 'TBJP BRITISH FINALS'),
        'K': ('KATKA', 'MASTERS BIKINI 45+', 'PCA BRITISH FINALS')}
css = """
#fl { position:absolute; inset:0; background:#fff; opacity:0; }
.bar { position:absolute; left:0; right:0; height:120px; background:#000; display:none; }
#bt { top:0; transform-origin:50% 0; } #bb { bottom:0; transform-origin:50% 100%; }
#op { position:absolute; left:0; right:0; top:350px; text-align:center; }
#op .k { font-weight:800; font-size:24px; letter-spacing:0.5em; color:#ff3b30; }
#op .big { font-family:"Bebas Neue"; font-size:240px; line-height:0.86; letter-spacing:0.04em; text-shadow:0 0 40px rgba(255,255,255,0.25), 0 14px 50px rgba(0,0,0,0.8); }
#op .s { font-weight:700; font-size:26px; letter-spacing:0.3em; margin-top:10px; }
#opd { position:absolute; inset:0; background:radial-gradient(ellipse 60% 55% at 50% 50%, rgba(0,0,0,0.55), rgba(0,0,0,0) 75%); opacity:0; }
.tg { position:absolute; left:52px; bottom:72px; opacity:0; padding:14px 90px 16px 24px; border-left:6px solid #ff3b30;
  background:linear-gradient(90deg, rgba(0,0,0,0.82) 0%, rgba(0,0,0,0.62) 70%, rgba(0,0,0,0) 100%); }
.tg .nm { font-family:"Bebas Neue"; font-size:84px; line-height:0.9; }
.tg .s1 { font-weight:800; font-size:20px; letter-spacing:0.22em; margin-top:4px; white-space:nowrap; }
.tg .s1 b { color:#ff3b30; }
.tg.k .s1 b { color:#6f93ff; } .tg.k { border-left-color:#3f6cf0; }
#bug { position:absolute; right:36px; top:36px; width:140px; opacity:0; filter:drop-shadow(0 4px 12px rgba(0,0,0,0.6)); }
.en { position:absolute; bottom:60px; width:640px; text-align:center; opacity:0; }
.en .nm { font-family:"Bebas Neue"; font-size:96px; line-height:0.9; text-shadow:0 8px 30px rgba(0,0,0,0.9); }
.en .s1 { font-weight:800; font-size:19px; letter-spacing:0.22em; text-shadow:0 2px 10px rgba(0,0,0,0.9); }
.en .s1 b { color:#ff3b30; }
.dv { position:absolute; top:0; bottom:0; width:6px; margin-left:-3px; background:#ff3b30; box-shadow:0 0 18px rgba(255,59,48,0.8); transform-origin:50% 0; opacity:0; }
#endlogo { position:absolute; left:40px; top:36px; width:170px; opacity:0; filter:drop-shadow(0 8px 24px rgba(0,0,0,0.8)); }
"""
body = ('<div id="opd"></div><div id="op"><div class="k">TEAM APEXX · ON STAGE</div><div class="big">STAGE DAY</div>'
        '<div class="s">TBJP BRITISH FINALS · PCA BRITISH FINALS</div></div>')
for a, (nm, s1, s2) in INFO.items():
    body += f'<div class="tg{" k" if a == "K" else ""}" id="t{a}"><div class="nm">{nm}</div><div class="s1"><b>{s1}</b> · {s2}</div></div>'
for j, a in enumerate('RGK'):
    nm, s1, s2 = INFO[a]
    body += f'<div class="en" id="e{a}" style="left:{j * 640}px"><div class="nm">{nm}</div><div class="s1"><b>{s1}</b></div></div>'
body += ('<div class="dv" id="d1" style="left:640px"></div><div class="dv" id="d2" style="left:1280px"></div>'
         '<img id="bug" src="assets/apexx-logo.png"/>'
         '<div class="bar" id="bt"></div><div class="bar" id="bb"></div><img id="endlogo" src="assets/apexx-logo.png"/><div id="fl"></div>')

js = 'gsap.set(["#op","#opd",".tg","#fl","#bug",".en",".dv","#endlogo"], { opacity:0 });\n'
# letterbox in, title
js += ('tl.fromTo([".bar"], { scaleY:0 }, { scaleY:1, duration:f(0.5), ease:"power3.out", immediateRender:false }, 0);\n'
       'tl.to("#opd", { opacity:1, duration:f(0.3) }, 0);\n'
       'tl.fromTo("#op", { opacity:0, scale:1.18, filter:"blur(14px)" }, { opacity:1, scale:1, filter:"blur(0px)", duration:f(0.55), ease:"expo.out", immediateRender:false }, f(0.1));\n'
       'tl.to("#op .big", { scale:1.06, duration:f(2.2), ease:"none" }, f(0.65));\n')
first = shots[1]['start']
js += (f'tl.to(["#op","#opd"], {{ opacity:0, y:-20, filter:"blur(10px)", duration:f(0.3), ease:"power2.in" }}, f({first} - 0.3));\n'
       f'tl.fromTo("#bug", {{ opacity:0 }}, {{ opacity:0.9, duration:f(0.4), immediateRender:false }}, f({first}));\n')
cur = None
for s in shots[1:]:
    t = s['start']; big = s['kind'] in ('end',) or s['i'] in (1, 7, 16, 20)
    t = t + 0.2
    a = s['a']
    if cur and cur != a:
        js += f'tl.to("#t{cur}", {{ opacity:0, duration:f(0.35), ease:"power1.inOut" }}, f({t} - 0.45));\n'
    if a in INFO and a != cur:
        js += (f'tl.fromTo("#t{a}", {{ opacity:0, x:-20 }}, {{ opacity:1, x:0, duration:f(0.5), ease:"power3.out", immediateRender:false }}, f({t}));\n'
               f'tl.fromTo("#t{a} .nm", {{ y:16, opacity:0 }}, {{ y:0, opacity:1, duration:f(0.5), ease:"power3.out", immediateRender:false }}, f({t} + 0.1));\n')
    cur = a
end = shots[-1]['start']
js += (f'tl.to("#bug", {{ opacity:0, duration:f(0.2) }}, f({end}));\n'
       f'tl.fromTo(".dv", {{ opacity:1, scaleY:0 }}, {{ scaleY:1, duration:f(0.45), ease:"power3.out", stagger:0.1, immediateRender:false }}, f({end} + 0.1));\n'
       f'tl.fromTo(".en", {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:f(0.45), ease:"expo.out", stagger:0.15, immediateRender:false }}, f({end} + 0.35));\n'
       f'tl.fromTo("#endlogo", {{ opacity:0, scale:0.6, rotation:-8 }}, {{ opacity:1, scale:1, rotation:0, duration:f(0.5), ease:"back.out(2)", immediateRender:false }}, f({end} + 0.9));\n'
       f'tl.to([".en",".dv","#endlogo"], {{ opacity:0, duration:f(0.5), ease:"power2.in" }}, f({TOT} - 0.6));\n'
       f'tl.to([".bar"], {{ scaleY:0, duration:f(0.5), ease:"power3.in" }}, f({TOT} - 0.55));\n')
page('v6-montage', TOT, body, js, css)
shutil.copy('../../v5/media/apexx-logo.png', 'comps/v6-montage/assets/apexx-logo.png')
print(made, TOT)
