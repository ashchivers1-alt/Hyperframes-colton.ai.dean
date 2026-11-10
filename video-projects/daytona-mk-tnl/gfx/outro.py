"""End card: Ash's 9:16 subscribe outro (screen-blended in on the left by scripts/vo_mix.py) + HKC register-your-interest panel.
Opaque 16:9 background; the left 700px is left plain for the outro video."""
import os, shutil
from build import write, ROOT

DUR = 17.0                 # starts the frame the race ends (1398.36), holds until Ash's VO ends (1414.36) + 1 s
LOGO = os.path.expanduser('~/Documents/KARTING WEBSITE/hkl/site/public/brand/hkc-logo.png')

CSS = """
#bg { position:absolute; inset:0; background:radial-gradient(ellipse 60% 80% at 72% 50%, #2a1206 0%, #120806 45%, #070707 100%); }
#glow { position:absolute; left:1290px; top:300px; width:900px; height:900px; margin:-450px 0 0 -450px; border-radius:50%;
  background:radial-gradient(circle, rgba(255,90,31,0.30) 0%, rgba(255,90,31,0) 65%); }
#stripes { position:absolute; inset:0; background:repeating-linear-gradient(115deg, rgba(255,255,255,0.025) 0 2px, rgba(0,0,0,0) 2px 46px); }
#vig { position:absolute; inset:0; background:radial-gradient(ellipse 75% 75% at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.6) 100%); }
#div { position:absolute; left:706px; top:150px; width:4px; height:780px; background:linear-gradient(180deg, rgba(255,90,31,0), #ff5a1f 30%, #f5c242 70%, rgba(245,194,66,0)); }
#sub { position:absolute; left:0; width:706px; top:880px; text-align:center; font-family:"JetBrains Mono"; font-weight:700; font-size:24px; letter-spacing:0.35em; color:rgba(255,255,255,0.7); }
#panel { position:absolute; left:760px; right:60px; top:70px; bottom:70px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:22px; }
#logo { width:330px; height:330px; filter:drop-shadow(0 18px 40px rgba(0,0,0,0.6)); }
#k { font-family:"JetBrains Mono"; font-weight:700; font-size:26px; letter-spacing:0.38em; color:#111; background:#ff5a1f; padding:10px 20px 9px 30px; margin-top:6px; }
#t1 { font-weight:900; font-style:italic; font-size:112px; line-height:0.95; letter-spacing:-0.01em; color:#fff; white-space:nowrap;
  text-shadow:0 5px 0 rgba(0,0,0,0.5), 0 0 40px rgba(0,0,0,0.6); }
#bar { width:760px; height:8px; background:linear-gradient(90deg, #ff5a1f, #f5c242); transform-origin:0 50%; }
#t2 { font-weight:900; font-style:italic; font-size:64px; line-height:1; color:#f5c242; white-space:nowrap; text-shadow:0 4px 0 rgba(0,0,0,0.5); }
#ig { display:flex; align-items:center; gap:20px; margin-top:18px; font-weight:800; font-size:44px; color:#fff; }
#ic { width:56px; height:56px; border-radius:16px; position:relative; background:radial-gradient(circle at 30% 110%, #fdf497 0%, #fd5949 45%, #d6249f 60%, #285AEB 95%); }
#ic::before { content:""; position:absolute; inset:11px; border:5px solid #fff; border-radius:12px; }
#ic::after { content:""; position:absolute; left:18px; top:18px; width:10px; height:10px; border:5px solid #fff; border-radius:50%; }
#dm { font-family:"JetBrains Mono"; font-weight:600; font-size:22px; letter-spacing:0.25em; color:rgba(255,255,255,0.75); }
#out { position:absolute; inset:0; background:#000; opacity:0; }
"""

BODY = ('<div id="bg"></div><div id="glow"></div><div id="stripes"></div><div id="vig"></div><div id="div"></div>'
        '<div id="sub">SUBSCRIBE FOR MORE RACES</div>'
        '<div id="panel"><img id="logo" src="assets/hkc-logo.png" />'
        '<div id="k">HEAVYWEIGHT KARTING CHAMPIONSHIP</div>'
        '<div id="t1">COMMENT BELOW</div><div id="bar"></div>'
        '<div id="t2">TO REGISTER YOUR INTEREST</div>'
        '<div id="ig"><i id="ic"></i>@heavyweight_karting_48</div><div id="dm">OR DM ME ON INSTAGRAM</div></div>'
        '<div id="out"></div>')

JS = f"""
tl.from("#bg", {{ opacity:0, duration:0.5, ease:"power1.out" }}, 0);
tl.from("#glow", {{ scale:0.6, opacity:0, duration:1.2, ease:"power2.out" }}, 0.2);
tl.to("#glow", {{ scale:1.12, duration:1.6, yoyo:true, repeat:9, ease:"sine.inOut" }}, 1.4);
tl.fromTo("#stripes", {{ backgroundPositionX:"0px" }}, {{ backgroundPositionX:"460px", duration:{DUR}, ease:"none" }}, 0);
tl.from("#div", {{ scaleY:0, duration:0.7, ease:"expo.out" }}, 0.35);
tl.from("#logo", {{ scale:0.2, rotation:-200, opacity:0, duration:0.9, ease:"back.out(1.4)" }}, 0.5);
tl.to("#logo", {{ rotation:6, duration:2.2, yoyo:true, repeat:6, ease:"sine.inOut" }}, 1.6);
tl.from("#k", {{ clipPath:"inset(0 100% 0 0)", duration:0.45, ease:"expo.out" }}, 1.1);
tl.from("#t1", {{ scale:1.5, opacity:0, duration:0.4, ease:"back.out(1.8)" }}, 1.45);
tl.from("#bar", {{ scaleX:0, duration:0.5, ease:"power3.out" }}, 1.75);
tl.from("#t2", {{ y:30, opacity:0, duration:0.45, ease:"power3.out" }}, 1.95);
tl.from("#ig", {{ x:-40, opacity:0, duration:0.45, ease:"expo.out" }}, 2.35);
tl.from("#dm", {{ opacity:0, duration:0.5, ease:"power1.out" }}, 2.6);
tl.to("#t1", {{ scale:1.04, duration:0.6, yoyo:true, repeat:21, ease:"sine.inOut" }}, 3.4);
tl.to("#ic", {{ scale:1.15, duration:0.5, yoyo:true, repeat:25, ease:"sine.inOut" }}, 3.0);
tl.from("#sub", {{ opacity:0, y:14, duration:0.5, ease:"power2.out" }}, 6.0);
tl.to("#out", {{ opacity:1, duration:0.8, ease:"power1.in" }}, {DUR - 0.8:.2f});
"""

if __name__ == '__main__':
    write('outro', DUR, BODY, JS, CSS)
    shutil.copy(LOGO, f'{ROOT}/comps/outro/assets/hkc-logo.png')
