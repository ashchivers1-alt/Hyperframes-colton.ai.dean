"""v5 overlays — athlete spotlights over the car update (clip 0038). Portrait posing clip in a framed panel on the
left (over the car window, clear of Ash), with an editorial name plate. Reuses HEAD + page() from build_v3."""
import shutil

src = open('build_v3.py').read()
exec(src[:src.index('# ---------- LEG DAY opener')])
made.clear()
MEDIA = '../../v5/media/'

A = [  # comp, media, dur, idx, name, line1 (show), line2 (note)
    ('v5-rachel', 'rachel.mp4', 11.5, '01', 'RACHEL', 'FIT MODEL · TBJP BRITISH FINALS', 'More shape &amp; fullness'),
    ('v5-gabriella', 'gabriella.mp4', 12.5, '02', 'GABRIELLA', 'BIKINI · TBJP BRITISH FINALS', ''),
    ('v5-katka', 'katka.mp4', 10.3, '03', 'KATKA', 'MASTERS BIKINI · PCA BRITISH FINALS', 'Competing in Telford today'),
    ('v5-daniela', 'daniela.mp4', 13.8, '04', 'DANIELA', 'WELLNESS · NPC · USA', ''),
]
css = """
#pw { position:absolute; left:70px; top:60px; width:480px; height:800px; }
#pf { position:absolute; inset:0; border-radius:14px; overflow:hidden; box-shadow:0 30px 80px rgba(0,0,0,0.6); background:#000; }
#pf video { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
#pf .vg { position:absolute; inset:0; background:linear-gradient(180deg, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%); }
#edge { position:absolute; left:-10px; top:24px; bottom:24px; width:6px; background:#ff3b30; border-radius:3px; transform-origin:50% 0;
  box-shadow:0 0 24px rgba(255,59,48,0.8); }
#wp { position:absolute; inset:0; background:#ff3b30; transform-origin:50% 0%; }
#tag { position:absolute; right:12px; top:12px; width:150px; filter:drop-shadow(0 4px 10px rgba(0,0,0,0.6)); }
#np { position:absolute; left:52px; top:740px; padding:20px 120px 22px 30px; border-radius:12px;
  background:linear-gradient(90deg, rgba(0,0,0,0.86) 0%, rgba(0,0,0,0.74) 70%, rgba(0,0,0,0) 100%); }
#np .k { font-weight:800; font-size:18px; letter-spacing:0.4em; color:#ff3b30; }
#np .nmw { overflow:hidden; padding-bottom:4px; }
#np .nm { font-family:"Bebas Neue"; font-size:104px; line-height:0.88; margin-top:4px; }
#np .rule { width:110px; height:3px; background:#ff3b30; margin:8px 0 10px; transform-origin:0 50%; }
#np .s1 { font-weight:800; font-size:22px; letter-spacing:0.18em; white-space:nowrap; }
#np .s2 { font-weight:600; font-size:24px; margin-top:8px; color:#e6e6e6; white-space:nowrap; }
"""
for comp, media, dur, idx, nm, l1, l2 in A:
    body = (f'<div id="pw"><div id="edge"></div><div id="pf">'
            f'<video id="v" src="assets/{media}" muted playsinline data-start="0" data-duration="{dur}" data-track-index="1"></video>'
            f'<div class="vg"></div><div id="wp"></div><img id="tag" src="assets/apexx-logo.png"/></div></div>'
            f'<div id="np" class="shadow"><div class="k">ATHLETE {idx} / 04</div><div class="nmw"><div class="nm">{nm}</div></div>'
            f'<div class="rule"></div><div class="s1">{l1}</div>' + (f'<div class="s2">{l2}</div>' if l2 else '') + '</div>')
    js = f"""gsap.set(["#pw","#np","#np .k","#np .s1","#np .s2","#tag"], {{ opacity:0 }});
tl.fromTo("#pw", {{ opacity:0, y:40, scale:0.96 }}, {{ opacity:1, y:0, scale:1, duration:f(0.45), ease:"expo.out", immediateRender:false }}, f(0.05));
tl.fromTo("#wp", {{ scaleY:1 }}, {{ scaleY:0, duration:f(0.55), ease:"power3.inOut", immediateRender:false }}, f(0.2));
tl.fromTo("#pf video", {{ scale:1.12 }}, {{ scale:1.0, duration:f({dur}), ease:"none", immediateRender:false }}, 0);
tl.fromTo("#edge", {{ scaleY:0 }}, {{ scaleY:1, duration:f(0.5), ease:"power3.out", immediateRender:false }}, f(0.3));
tl.fromTo("#tag", {{ opacity:0, scale:0.6, rotation:-8 }}, {{ opacity:1, scale:1, rotation:0, duration:f(0.4), ease:"back.out(2)", immediateRender:false }}, f(0.7));
tl.fromTo("#np", {{ opacity:0, x:-50 }}, {{ opacity:1, x:0, duration:f(0.45), ease:"expo.out", immediateRender:false }}, f(0.35));
tl.fromTo("#np .k", {{ opacity:0, x:-16 }}, {{ opacity:1, x:0, duration:f(0.3), ease:"power2.out", immediateRender:false }}, f(0.45));
tl.fromTo("#np .nm", {{ yPercent:110 }}, {{ yPercent:0, duration:f(0.5), ease:"expo.out", immediateRender:false }}, f(0.5));
tl.fromTo("#np .rule", {{ scaleX:0 }}, {{ scaleX:1, duration:f(0.35), ease:"power3.inOut", immediateRender:false }}, f(0.65));
tl.fromTo("#np .s1", {{ opacity:0, y:10 }}, {{ opacity:1, y:0, duration:f(0.35), ease:"back.out(1.6)", immediateRender:false }}, f(0.85));
tl.fromTo("#np .s2", {{ opacity:0, y:10 }}, {{ opacity:1, y:0, duration:f(0.35), ease:"power3.out", immediateRender:false }}, f(1.1));
tl.to("#pw", {{ opacity:0, y:-30, duration:f(0.4), ease:"power2.in" }}, f({dur} - 0.5));
tl.to("#np", {{ opacity:0, x:-30, duration:f(0.35), ease:"power2.in" }}, f({dur} - 0.5));"""
    page(comp, dur, body, js, css)
    shutil.copy(MEDIA + media, f'comps/{comp}/assets/{media}')
    shutil.copy(MEDIA + 'apexx-logo.png', f'comps/{comp}/assets/apexx-logo.png')

# ---------- Gabriella rear-shot progression photo ----------
PD = 7.2
css2 = """
#pc { position:absolute; left:70px; top:90px; width:680px; height:680px; border-radius:14px; overflow:hidden; box-shadow:0 30px 80px rgba(0,0,0,0.6); }
#pc img.ph { width:100%; height:100%; display:block; object-fit:cover; }
#pc .half { position:absolute; top:0; bottom:0; width:50%; background:#0b0b0b; }
#pc .hl { left:0; transform-origin:0 50%; } #pc .hr { right:0; transform-origin:100% 50%; }
#pc .div { position:absolute; left:50%; top:0; bottom:0; width:6px; margin-left:-3px; background:#ff3b30; transform-origin:50% 0; box-shadow:0 0 18px rgba(255,59,48,0.8); }
#pc #tag { position:absolute; right:12px; top:12px; width:150px; filter:drop-shadow(0 4px 10px rgba(0,0,0,0.6)); }
#np { position:absolute; left:52px; top:740px; padding:20px 120px 22px 30px; border-radius:12px;
  background:linear-gradient(90deg, rgba(0,0,0,0.86) 0%, rgba(0,0,0,0.74) 70%, rgba(0,0,0,0) 100%); }
#np .k { font-weight:800; font-size:18px; letter-spacing:0.4em; color:#ff3b30; }
#np .nmw { overflow:hidden; padding-bottom:4px; }
#np .nm { font-family:"Bebas Neue"; font-size:96px; line-height:0.88; margin-top:4px; }
"""
body = ('<div id="pc"><img class="ph" src="assets/gab-progress.jpg"/><div class="half hl"></div><div class="half hr"></div><div class="div"></div>'
        '<img id="tag" src="assets/apexx-logo.png"/></div>'
        '<div id="np" class="shadow"><div class="k">GABRIELLA · PROGRESS</div><div class="nmw"><div class="nm">REAR SHOT</div></div></div>')
js = f"""gsap.set(["#pc","#np","#tag"], {{ opacity:0 }});
tl.fromTo("#pc", {{ opacity:0, scale:0.94, y:30 }}, {{ opacity:1, scale:1, y:0, duration:f(0.45), ease:"expo.out", immediateRender:false }}, f(0.05));
tl.fromTo(".div", {{ scaleY:0 }}, {{ scaleY:1, duration:f(0.45), ease:"power3.out", immediateRender:false }}, f(0.2));
tl.fromTo(".hl", {{ scaleX:1 }}, {{ scaleX:0, duration:f(0.55), ease:"power3.inOut", immediateRender:false }}, f(0.45));
tl.fromTo(".hr", {{ scaleX:1 }}, {{ scaleX:0, duration:f(0.55), ease:"power3.inOut", immediateRender:false }}, f(0.85));
tl.fromTo("#pc .ph", {{ scale:1.0 }}, {{ scale:1.05, duration:f({PD}), ease:"none", immediateRender:false }}, 0);
tl.fromTo("#tag", {{ opacity:0, scale:0.6, rotation:-8 }}, {{ opacity:1, scale:1, rotation:0, duration:f(0.4), ease:"back.out(2)", immediateRender:false }}, f(1.1));
tl.fromTo("#np", {{ opacity:0, x:-50 }}, {{ opacity:1, x:0, duration:f(0.45), ease:"expo.out", immediateRender:false }}, f(0.4));
tl.fromTo("#np .nm", {{ yPercent:110 }}, {{ yPercent:0, duration:f(0.5), ease:"expo.out", immediateRender:false }}, f(0.55));
tl.to("#pc", {{ opacity:0, y:-30, duration:f(0.4), ease:"power2.in" }}, f({PD} - 0.5));
tl.to("#np", {{ opacity:0, x:-30, duration:f(0.35), ease:"power2.in" }}, f({PD} - 0.5));"""
page('v5-gabprog', PD, body, js, css2)
shutil.copy(MEDIA + 'gab-progress.jpg', 'comps/v5-gabprog/assets/gab-progress.jpg')
shutil.copy(MEDIA + 'apexx-logo.png', 'comps/v5-gabprog/assets/apexx-logo.png')

# ---------- Daniela meal 1 plan card ----------
MD5 = 8.5
css3 = """
#mc { position:absolute; left:70px; top:110px; width:640px; padding:30px 40px 34px; border-radius:16px; border-left:6px solid #ff3b30;
  background:linear-gradient(160deg, rgba(14,14,16,0.92) 0%, rgba(8,8,10,0.86) 100%); box-shadow:0 30px 80px rgba(0,0,0,0.6); }
#mc .top { display:flex; justify-content:space-between; align-items:center; }
#mc .k { font-weight:800; font-size:18px; letter-spacing:0.4em; color:#ff3b30; }
#mc .top img { width:120px; }
#mc .h { font-family:"Bebas Neue"; font-size:110px; line-height:0.86; margin-top:6px; }
#mc .rule { width:110px; height:3px; background:#ff3b30; margin:12px 0 18px; transform-origin:0 50%; }
#mc .sec { font-weight:800; font-size:16px; letter-spacing:0.32em; color:#9aa3ab; margin:4px 0 8px; }
#mc .it { display:flex; align-items:baseline; gap:18px; padding:9px 0; border-bottom:1px solid rgba(255,255,255,0.12); }
#mc .it .q { font-family:"Bebas Neue"; font-size:42px; color:#ff3b30; width:110px; flex:none; line-height:1; }
#mc .it .n { font-weight:700; font-size:30px; }
#mc .gap { height:20px; }
"""
FOOD = [('1×', 'Bagel'), ('50g', 'Chicken'), ('1×', 'Square bar'), ('20g', 'Peanut butter')]
EXTRA = [('500ml', 'Water'), ('1×', 'Dandelion / Vit C'), ('1×', 'Double espresso if needed'), ('—', 'Salt as usual')]
row = lambda q, n, i: f'<div class="it" id="r{i}"><div class="q">{q}</div><div class="n">{n}</div></div>'
items = ''.join(row(q, n, i) for i, (q, n) in enumerate(FOOD))
extras = ''.join(row(q, n, i + 4) for i, (q, n) in enumerate(EXTRA))
body = (f'<div id="mc" class="shadow"><div class="top"><div class="k">DANIELA · SHOW DAY</div><img src="assets/apexx-logo.png"/></div>'
        f'<div class="h">MEAL 1</div><div class="rule"></div><div class="sec">FOOD</div>{items}<div class="gap"></div>'
        f'<div class="sec">WITH IT</div>{extras}</div>')
js = 'gsap.set(["#mc"' + ''.join(f',"#r{i}"' for i in range(8)) + '], { opacity:0 });\n'
js += 'tl.fromTo("#mc", { opacity:0, x:-60 }, { opacity:1, x:0, duration:f(0.45), ease:"expo.out", immediateRender:false }, f(0.05));\n'
js += 'tl.fromTo("#mc .h", { yPercent:60, opacity:0 }, { yPercent:0, opacity:1, duration:f(0.45), ease:"expo.out", immediateRender:false }, f(0.2));\n'
js += 'tl.fromTo("#mc .rule", { scaleX:0 }, { scaleX:1, duration:f(0.35), ease:"power3.inOut", immediateRender:false }, f(0.35));\n'
for i in range(8):
    js += f'tl.fromTo("#r{i}", {{ opacity:0, x:-24 }}, {{ opacity:1, x:0, duration:f(0.3), ease:"power3.out", immediateRender:false }}, f({0.55 + i * 0.12:.2f}));\n'
js += f'tl.to("#mc", {{ opacity:0, x:-30, duration:f(0.35), ease:"power2.in" }}, f({MD5} - 0.45));'
page('v5-danmeal', MD5, body, js, css3)
shutil.copy(MEDIA + 'apexx-logo.png', 'comps/v5-danmeal/assets/apexx-logo.png')
print(made)
