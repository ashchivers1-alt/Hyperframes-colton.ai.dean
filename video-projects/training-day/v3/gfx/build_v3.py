"""v3 overlays — new 'editorial' style (no dark glass cards) so the video stops looking templated.
Each overlay -> comps/<name>/index.html, rendered to ProRes 4444 alpha MOV for Resolve V2."""
import json, os, shutil

T = json.load(open('../gfx_times.json'))

HEAD = """<!doctype html><html lang="en"><head><meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" /><script src="assets/gsap.min.js"></script>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:1920px; height:1080px; overflow:hidden; background:transparent; }
#root { position:relative; width:1920px; height:1080px; overflow:hidden; font-family:Montserrat, sans-serif; color:#f6f6f6; }
.shadow { text-shadow:0 4px 24px rgba(0,0,0,0.75), 0 2px 4px rgba(0,0,0,0.6); }
/* exercise title: index numeral + name + rep chip, no box */
.ex { position:absolute; left:52px; bottom:72px; padding:22px 160px 24px 32px; border-radius:12px; box-shadow:0 0 40px 10px rgba(0,0,0,0.25);
  background:linear-gradient(90deg, rgba(0,0,0,0.78) 0%, rgba(0,0,0,0.66) 65%, rgba(0,0,0,0) 100%); }
.ex .idx { font-family:"Bebas Neue", sans-serif; font-size:40px; letter-spacing:0.12em; color:#ff3b30; }
.ex .idx span { color:rgba(255,255,255,0.7); }
.ex .rule { width:120px; height:3px; background:#ff3b30; margin:8px 0 12px; transform-origin:0 50%; }
.ex .nm { font-family:"Bebas Neue", sans-serif; font-size:104px; line-height:0.88; letter-spacing:0.01em; white-space:nowrap; }
.ex .nmw { overflow:hidden; padding-bottom:6px; }
.ex .chip { display:inline-block; margin-top:16px; padding:8px 16px 7px; border:2px solid rgba(255,255,255,0.85); border-radius:4px;
  font-weight:800; font-size:28px; letter-spacing:0.24em; background:rgba(0,0,0,0.45); }
.ex .chip b { color:#ff3b30; font-weight:800; }
%CSS%
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%DUR%" data-width="1920" data-height="1080">%BODY%</div>
<script>(() => { const tl = gsap.timeline({ paused:true }); const f = (s) => Math.round(s*30)/30;
%JS%
tl.to({}, { duration:%DUR% }, 0); window.__timelines = window.__timelines || {}; window.__timelines["main"] = tl; })();</script>
</body></html>"""

made = []
def page(name, dur, body, js, css=""):
    d = f'comps/{name}'; os.makedirs(d, exist_ok=True)
    open(f'{d}/index.html', 'w').write(HEAD.replace('%DUR%', str(dur)).replace('%BODY%', body).replace('%JS%', js).replace('%CSS%', css))
    shutil.copy('../../gfx/hyperframes.json', d)
    open(f'{d}/meta.json', 'w').write(json.dumps({"id": name, "name": name, "width": 1920, "height": 1080, "fps": 30}))
    if not os.path.exists(f'{d}/assets'): shutil.copytree('../../gfx/assets', f'{d}/assets')
    made.append(name)

# ---------- LEG DAY opener ----------
css = """
#ld { position:absolute; left:0; right:0; top:330px; text-align:center; }
#ld .k { font-weight:700; font-size:26px; letter-spacing:0.6em; color:rgba(255,255,255,0.85); }
#ld .big { font-family:"Bebas Neue", sans-serif; font-size:300px; line-height:0.86; letter-spacing:0.04em; }
#ld .big .ch { display:inline-block; color:#f4f4f4; text-shadow:0 0 30px rgba(255,255,255,0.25), 0 12px 40px rgba(0,0,0,0.75); }
#slash { position:absolute; left:660px; top:620px; width:600px; height:10px; background:#ff3b30; transform:skewX(-20deg); transform-origin:0 50%;
  box-shadow:0 0 30px rgba(255,59,48,0.8); }
#dim { position:absolute; inset:0; background:radial-gradient(ellipse 60% 55% at 50% 50%, rgba(0,0,0,0.5), rgba(0,0,0,0) 75%); }
"""
letters = ''.join(f'<span class="ch">{c}</span>' if c != ' ' else '<span class="ch" style="width:70px"></span>' for c in 'LEG DAY')
body = f'<div id="dim"></div><div id="ld" class="shadow"><div class="k">WELLNESS WEEK · TEAM APEXX</div><div class="big">{letters}</div></div><div id="slash"></div>'
js = """gsap.set(["#dim","#ld .k","#ld .ch","#slash"], { opacity:0 });
tl.to("#dim", { opacity:1, duration:f(0.4) }, 0);
tl.fromTo("#ld .ch", { opacity:0, y:80, scale:1.4, filter:"blur(12px)" }, { opacity:1, y:0, scale:1, filter:"blur(0px)", duration:f(0.5), ease:"expo.out", stagger:0.06, immediateRender:false }, f(0.15));
tl.fromTo("#slash", { opacity:1, scaleX:0 }, { scaleX:1, duration:f(0.4), ease:"power3.inOut", immediateRender:false }, f(0.7));
tl.fromTo("#ld .k", { opacity:0, y:-16 }, { opacity:1, y:0, duration:f(0.6), ease:"power2.out", immediateRender:false }, f(0.9));
tl.to("#ld .big", { scale:1.06, duration:f(4.2), ease:"none" }, f(0.6));
tl.to(["#ld","#slash"], { opacity:0, y:-30, filter:"blur(10px)", duration:f(0.4), ease:"power2.in" }, f(5.2));
tl.to("#dim", { opacity:0, duration:f(0.4) }, f(5.3));"""
page('v3-legday', 5.8, body, js, css)

# ---------- exercise titles ----------
EX = [('t3-act', '01', 'GLUTE ACTIVATION', None),
      ('t3-abd', '02', 'STANDING ABDUCTOR MACHINE', '<b>3</b> SETS · <b>10–15</b> REPS'),
      ('t3-ht', '03', 'HIP THRUST MACHINE', '<b>2</b> SETS · <b>6–10</b> REPS'),
      ('t3-lp', '04', 'GLUTE-FOCUSED SINGLE-LEG PRESS', '<b>2</b> SETS · <b>8–12</b> REPS'),
      ('t3-sq', '05', 'GLUTE-BIAS SINGLE-LEG MACHINE SQUAT', '<b>2</b> SETS · <b>8–12</b> REPS'),
      ('t3-bs', '06', 'SUMO BELT SQUAT', '<b>2</b> SETS · <b>10–15</b> REPS'),
      ('t3-gp', '07', 'GLUTE PRESS', '<b>2</b> SETS · <b>8–12</b> REPS')]
for name, idx, nm, chip in EX:
    size = 104 if len(nm) <= 20 else 78
    body = (f'<div class="ex shadow"><div class="idx">{idx} <span>/ 07</span></div><div class="rule"></div>'
            f'<div class="nmw"><div class="nm" style="font-size:{size}px">{nm}</div></div>'
            + (f'<div class="chip">{chip}</div>' if chip else '') + '</div>')
    js = """gsap.set([".ex .idx",".ex .rule",".ex .nm",".ex .chip"], { opacity:0 });
tl.fromTo(".ex .idx", { opacity:0, x:-20 }, { opacity:1, x:0, duration:f(0.3), ease:"power2.out", immediateRender:false }, f(0.1));
tl.fromTo(".ex .rule", { opacity:1, scaleX:0 }, { scaleX:1, duration:f(0.35), ease:"power3.inOut", immediateRender:false }, f(0.15));
tl.fromTo(".ex .nm", { opacity:1, yPercent:110 }, { yPercent:0, duration:f(0.5), ease:"expo.out", immediateRender:false }, f(0.25));
tl.fromTo(".ex .chip", { opacity:0, y:12 }, { opacity:1, y:0, duration:f(0.35), ease:"back.out(1.6)", immediateRender:false }, f(0.6));
tl.to(".ex .nm", { yPercent:-110, duration:f(0.35), ease:"power2.in" }, f(3.0));
tl.to([".ex .idx",".ex .rule",".ex .chip"], { opacity:0, duration:f(0.3) }, f(3.05));"""
    page(name, 3.5, body, js)

# ---------- Ash Dictionary: dictionary-entry card ----------
css = """
#dict { position:absolute; left:84px; bottom:110px; width:620px; padding:26px 30px 24px; background:#f4efe4; color:#1b1b1b; border-radius:6px;
  box-shadow:0 20px 60px rgba(0,0,0,0.55); transform:rotate(-2deg); font-family:"Playfair Display", Georgia, serif; }
#dict .src { font-family:Montserrat, sans-serif; font-weight:800; font-size:16px; letter-spacing:0.35em; color:#d80609; }
#dict .hw { font-size:58px; font-weight:700; margin-top:6px; }
#dict .ph { font-size:22px; font-style:italic; color:#555; margin-top:2px; }
#dict .df { font-size:28px; margin-top:12px; line-height:1.3; }
#dict .df i { color:#777; }
"""
body = ('<div id="dict"><div class="src">THE ASH DICTIONARY</div><div class="hw">water skiddy</div>'
        '<div class="ph">/ˈwɔː.tə ˈskɪd.i/ · <i>noun</i></div><div class="df">a sweat patch. <i>Not</i> the other kind.</div></div>')
js = """gsap.set("#dict", { opacity:0 });
tl.fromTo("#dict", { opacity:0, y:60, rotation:-8 }, { opacity:1, y:0, rotation:-2, duration:f(0.5), ease:"back.out(1.4)", immediateRender:false }, f(0.1));
tl.to("#dict", { y:-6, duration:f(2.4), ease:"sine.inOut", yoyo:true, repeat:1 }, f(0.6));
tl.to("#dict", { opacity:0, y:40, rotation:4, duration:f(0.35), ease:"power2.in" }, f(5.6));"""
page('v3-skiddy', 6.0, body, js, css)

# ---------- coaching cues (single-leg press) ----------
E = T['edu']; C0 = E['15.0'] - 0.5
rel = lambda k: round(E[k] - C0, 3)
css = """
.ff { position:absolute; inset:0; } .ff img { width:1920px; height:1080px; display:block; }
.frz { position:absolute; right:60px; top:50px; font-family:"Bebas Neue"; font-size:40px; letter-spacing:0.2em; color:#fff;
  padding:4px 16px; border:3px solid #ff3b30; }
svg { position:absolute; inset:0; }
.cue { position:absolute; left:52px; top:44px; width:1100px; padding:24px 120px 26px 32px; border-radius:12px;
  background:linear-gradient(90deg, rgba(0,0,0,0.78) 0%, rgba(0,0,0,0.66) 70%, rgba(0,0,0,0) 100%); }
.cue .no { font-family:"Bebas Neue"; font-size:150px; line-height:0.8; color:transparent; -webkit-text-stroke:3px #ff3b30; float:left; margin-right:24px; }
.cue .lbl { font-weight:800; font-size:20px; letter-spacing:0.4em; color:#ff3b30; }
.cue .tx { font-weight:800; font-size:44px; line-height:1.15; margin-top:6px; }
.cue .tx u { text-decoration:none; background:linear-gradient(transparent 62%, rgba(255,59,48,0.75) 62%); }
.cue .sub { clear:both; margin-top:18px; margin-left:4px; font-weight:600; font-size:28px; line-height:1.35; color:#fff; max-width:900px;
  padding-left:18px; border-left:4px solid #ff3b30; }
"""
body = f"""
<div class="ff" id="fk"><img src="assets/freeze-knee.jpg" /><div class="frz">FREEZE</div>
 <svg width="1920" height="1080"><line id="kl" x1="830" y1="420" x2="1220" y2="480" stroke="#ff3b30" stroke-width="8" stroke-linecap="round"/>
 <circle cx="830" cy="420" r="16" fill="none" stroke="#fff" stroke-width="5"/><circle cx="1220" cy="480" r="16" fill="none" stroke="#fff" stroke-width="5"/>
 <text x="1250" y="470" fill="#fff" font-family="Montserrat" font-weight="800" font-size="26">KNEE</text><text x="700" y="410" fill="#fff" font-family="Montserrat" font-weight="800" font-size="26">ANKLE</text></svg></div>
<div class="ff" id="fh"><img src="assets/freeze-heel.jpg" /><div class="frz">FREEZE</div>
 <svg width="1920" height="1080"><defs><marker id="ah" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#ff3b30"/></marker></defs>
 <line id="hl" x1="880" y1="470" x2="712" y2="352" stroke="#ff3b30" stroke-width="9" stroke-linecap="round" marker-end="url(#ah)"/>
 <circle cx="690" cy="340" r="22" fill="none" stroke="#fff" stroke-width="5"/></svg></div>
<div class="cue shadow" id="cA"><div class="no">1</div><div class="lbl">COACHING CUE</div>
 <div class="tx">Foot <u>high</u> on the platform — keep a straight line with the <u>knee and ankle</u>.</div>
 <div class="sub">Don't let the knee travel in front of the ankle — that adds quad bias.</div></div>
<div class="cue shadow" id="cB"><div class="no">2</div><div class="lbl">COACHING CUE</div><div class="tx">Press through your <u>heel</u>.</div></div>
<div class="cue shadow" id="cC"><div class="lbl">ASH</div><div class="tx" style="font-style:italic">“You could go a little bit <u>higher</u>, to be fair.”</div></div>
"""
def cin(sel, t):
    return (f'tl.fromTo("{sel}", {{ opacity:0, x:-50 }}, {{ opacity:1, x:0, duration:f(0.45), ease:"expo.out", immediateRender:false }}, f({t}));\n'
            f'tl.fromTo("{sel} .no", {{ scale:1.6, opacity:0 }}, {{ scale:1, opacity:1, duration:f(0.4), ease:"back.out(2)", immediateRender:false }}, f({t}+0.05));\n')
def cout(sel, t): return f'tl.to("{sel}", {{ opacity:0, x:-30, duration:f(0.3), ease:"power2.in" }}, f({t}));\n'
js = 'gsap.set(["#fk","#fh","#cA","#cB","#cC","#cA .sub"], { opacity:0 });\n'
js += cin('#cA', rel('15.0')) + f'tl.fromTo("#cA .sub", {{ opacity:0, y:14 }}, {{ opacity:1, y:0, duration:f(0.35), ease:"power2.out", immediateRender:false }}, f({rel("15.0") + 1.4}));\n' + cout('#cA', rel('24.9'))
js += f'tl.fromTo("#fk", {{ opacity:0 }}, {{ opacity:1, duration:f(0.1), immediateRender:false }}, f({rel("16.2")}));\n'
js += f'tl.fromTo("#kl", {{ strokeDasharray:420, strokeDashoffset:420 }}, {{ strokeDashoffset:0, duration:f(0.5), ease:"power2.out", immediateRender:false }}, f({rel("16.2") + 0.1}));\n'
js += f'tl.to("#fk", {{ opacity:0, duration:f(0.2) }}, f({rel("19.0")}));\n'
js += cin('#cB', rel('31.0')) + cout('#cB', rel('38.6'))
js += f'tl.fromTo("#fh", {{ opacity:0 }}, {{ opacity:1, duration:f(0.1), immediateRender:false }}, f({rel("32.3")}));\n'
js += f'tl.fromTo("#hl", {{ strokeDasharray:220, strokeDashoffset:220 }}, {{ strokeDashoffset:0, duration:f(0.4), ease:"power2.out", immediateRender:false }}, f({rel("32.3") + 0.1}));\n'
js += f'tl.to("#fh", {{ opacity:0, duration:f(0.2) }}, f({rel("35.0")}));\n'
js += cin('#cC', rel('47.0')) + cout('#cC', rel('49.0'))
CUE_DUR = round(rel('49.0') + 0.5, 2)
page('v3-cues', CUE_DUR, body, js, css)

# ---------- machine note ----------
ND = round(T['note_end'] - T['note'], 2)
css = """
#nt { position:absolute; left:52px; top:44px; width:1060px; padding:24px 120px 26px 32px; border-radius:12px;
  background:linear-gradient(90deg, rgba(0,0,0,0.78) 0%, rgba(0,0,0,0.66) 70%, rgba(0,0,0,0) 100%); }
#nt .lbl { font-weight:800; font-size:20px; letter-spacing:0.4em; color:#ff3b30; }
#nt .tx { font-weight:800; font-size:40px; line-height:1.2; margin-top:8px; }
#nt .tx u { text-decoration:none; background:linear-gradient(transparent 62%, rgba(255,59,48,0.75) 62%); }
#nt .q { margin-top:14px; font-weight:600; font-style:italic; font-size:28px; padding-left:18px; border-left:4px solid #ff3b30; }
#arc { position:absolute; left:1460px; top:110px; }
"""
body = """<div id="nt" class="shadow"><div class="lbl">ASH'S MACHINE NOTE</div>
<div class="tx">This is a <u>squat press</u> and moves in an <u>arc</u>. For this movement, I typically prefer a more <u>linear press</u>, e.g. a <u>Hammer Strength leg press</u>.</div></div>
<svg id="arc" width="380" height="300"><path id="ap" d="M40,40 Q300,40 330,260" fill="none" stroke="#fff" stroke-width="6" stroke-dasharray="14 10"/>
<line id="lp" x1="40" y1="120" x2="330" y2="120" stroke="#ff3b30" stroke-width="6"/>
<text x="40" y="290" fill="#fff" font-family="Montserrat" font-weight="800" font-size="22">ARC (this machine)</text>
<text x="40" y="105" fill="#ff3b30" font-family="Montserrat" font-weight="800" font-size="22">LINEAR (preferred)</text></svg>"""
js = f"""gsap.set(["#nt","#arc"], {{ opacity:0 }});
tl.fromTo("#nt", {{ opacity:0, x:-50 }}, {{ opacity:1, x:0, duration:f(0.45), ease:"expo.out", immediateRender:false }}, f(0.2));
tl.fromTo("#arc", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:f(0.4), ease:"power2.out", immediateRender:false }}, f(0.8));
tl.fromTo("#ap", {{ strokeDashoffset:600 }}, {{ strokeDashoffset:0, duration:f(1.2), ease:"power1.inOut", immediateRender:false }}, f(0.9));
tl.to(["#nt","#arc"], {{ opacity:0, x:-30, duration:f(0.3), ease:"power2.in" }}, f({ND - 0.4}));"""
page('v3-note', ND, body, js, css)


# ---------- ASH10 discount code (new style, timed to the shortened review end) ----------
AD = 6.5
css = """
#cd { position:absolute; left:52px; bottom:72px; padding:22px 160px 24px 32px; border-radius:12px;
  background:linear-gradient(90deg, rgba(0,0,0,0.78) 0%, rgba(0,0,0,0.66) 65%, rgba(0,0,0,0) 100%); box-shadow:0 0 40px 10px rgba(0,0,0,0.25); }
#cd .lbl { font-weight:800; font-size:22px; letter-spacing:0.38em; color:#ff3b30; }
#cd .code { font-family:"Bebas Neue", sans-serif; font-size:120px; line-height:0.9; margin-top:6px; }
#cd .code span { color:#ff3b30; }
"""
body = '<div id="cd" class="shadow"><div class="lbl">tbJP · DISCOUNT CODE</div><div class="code">ASH<span>10</span></div></div>'
js = f"""gsap.set("#cd", {{ opacity:0 }});
tl.fromTo("#cd", {{ opacity:0, x:-50 }}, {{ opacity:1, x:0, duration:f(0.45), ease:"expo.out", immediateRender:false }}, f(0.15));
tl.fromTo("#cd .code", {{ scale:1.3, transformOrigin:"0% 50%" }}, {{ scale:1, duration:f(0.4), ease:"back.out(2)", immediateRender:false }}, f(0.25));
tl.to("#cd", {{ opacity:0, x:-30, duration:f(0.3), ease:"power2.in" }}, f({AD - 0.4}));"""
page('v3-ash10', AD, body, js, css)

# ---------- JOB DONE end card (music runs over the mirror peace-sign clip) ----------
JD = T['jobdone_dur']
css = """
#jd { position:absolute; left:52px; bottom:72px; padding:22px 160px 24px 32px; border-radius:12px; display:flex; align-items:center; gap:26px;
  background:linear-gradient(90deg, rgba(0,0,0,0.78) 0%, rgba(0,0,0,0.66) 65%, rgba(0,0,0,0) 100%); }
#jd .t { font-family:"Bebas Neue", sans-serif; font-size:150px; line-height:0.86; }
#jd svg { flex:none; }
#jd .peace { font-size:96px; line-height:1; }
"""
body = ('<div id="jd" class="shadow"><div class="t">JOB DONE</div>'
        '<svg width="120" height="120" viewBox="0 0 120 120"><circle cx="60" cy="60" r="54" fill="#ff3b30"/>'
        '<path id="tk" d="M34 62 L53 80 L88 42" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        '<div class="peace">✌️</div></div>')
js = f"""gsap.set(["#jd","#jd svg","#jd .peace"], {{ opacity:0 }});
tl.fromTo("#jd", {{ opacity:0, x:-60 }}, {{ opacity:1, x:0, duration:f(0.45), ease:"expo.out", immediateRender:false }}, f(0.1));
tl.fromTo("#jd svg", {{ opacity:0, scale:0.3 }}, {{ opacity:1, scale:1, duration:f(0.4), ease:"back.out(2.2)", immediateRender:false }}, f(0.5));
tl.fromTo("#tk", {{ strokeDasharray:90, strokeDashoffset:90 }}, {{ strokeDashoffset:0, duration:f(0.35), ease:"power2.out", immediateRender:false }}, f(0.7));
tl.fromTo("#jd .peace", {{ opacity:0, rotation:-30, scale:0.5 }}, {{ opacity:1, rotation:0, scale:1, duration:f(0.45), ease:"back.out(2)", immediateRender:false }}, f(0.95));"""
page('v3-jobdone', JD, body, js, css)

# ---------- squeaky machine caption (Ash's hip thrust, 'you've ruined my set') ----------
css = """
#sq { position:absolute; left:52px; top:44px; padding:22px 150px 24px 32px; border-radius:12px; display:flex; gap:22px; align-items:center;
  background:linear-gradient(90deg, rgba(0,0,0,0.78) 0%, rgba(0,0,0,0.66) 65%, rgba(0,0,0,0) 100%); }
#sq .ic { font-size:84px; line-height:1; }
#sq .l1 { font-weight:800; font-size:22px; letter-spacing:0.36em; color:#ff3b30; }
#sq .l2 { font-family:"Bebas Neue", sans-serif; font-size:76px; line-height:0.92; }
#sq .l3 { font-weight:700; font-size:30px; margin-top:6px; }
#sq .l3 b { color:#ff3b30; }
"""
body = ('<div id="sq" class="shadow"><div class="ic">🔊</div><div><div class="l1">THE CULPRIT</div>'
        '<div class="l2">THAT SQUEAK? IT&#39;S THE MACHINE.</div><div class="l3">Someone get this thing some <b>WD-40</b> 😂</div></div></div>')
js = """gsap.set(["#sq","#sq .ic"], { opacity:0 });
tl.fromTo("#sq", { opacity:0, x:-50 }, { opacity:1, x:0, duration:f(0.45), ease:"expo.out", immediateRender:false }, f(0.1));
tl.fromTo("#sq .ic", { opacity:0, scale:0.4, rotation:-20 }, { opacity:1, scale:1, rotation:0, duration:f(0.4), ease:"back.out(2.4)", immediateRender:false }, f(0.3));
tl.to("#sq .ic", { keyframes:[{ rotation:-12, duration:0.1 },{ rotation:12, duration:0.1 },{ rotation:-8, duration:0.1 },{ rotation:0, duration:0.1 }] }, f(0.9));
tl.to("#sq", { opacity:0, x:-30, duration:f(0.3), ease:"power2.in" }, f(5.6));"""
page('v3-squeak', 6.0, body, js, css)

# ---------- drive B-roll: motorway sign + 'next stop Bradford' ----------
DD = 8.0
css = """
#tlp { position:absolute; left:52px; top:44px; font-weight:800; font-size:22px; letter-spacing:0.4em; color:#fff; padding:8px 16px 7px;
  background:rgba(0,0,0,0.45); border-radius:4px; }
#tlp b { color:#ff3b30; letter-spacing:0; margin-right:12px; }
#sg { position:absolute; right:90px; top:90px; width:640px; padding:26px 30px 28px; background:#1d4f9c; border:6px solid #fff;
  outline:3px solid #1d4f9c; border-radius:18px; color:#fff; font-family:Montserrat, sans-serif; box-shadow:0 24px 70px rgba(0,0,0,0.6); }
#sg .row { display:flex; align-items:center; gap:22px; }
#sg .row + .row { margin-top:22px; padding-top:22px; border-top:4px solid rgba(255,255,255,0.9); }
#sg .rt { font-weight:700; font-size:50px; padding:2px 16px 0; border:4px solid #fff; border-radius:6px; line-height:1.1; }
#sg .pl { font-weight:700; font-size:58px; line-height:1; }
#sg .pl small { font-size:58px; text-transform:none; }
#sg .ar { margin-left:auto; width:58px; height:58px; }
"""
body = ('<div id="sg"><div class="row"><div class="rt">M1</div><div class="pl">The NORTH</div>'
        '<svg class="ar" viewBox="0 0 60 60"><path d="M30 4 L52 30 H38 V56 H22 V30 H8 Z" fill="#fff"/></svg></div>'
        '<div class="row"><div class="pl">Leeds<br>Bradford</div><div class="rt" style="margin-left:auto">M62</div></div></div>'
        '<div class="ex shadow"><div class="idx">EN ROUTE</div><div class="rule"></div>'
        '<div class="nmw"><div class="nm">NEXT STOP: BRADFORD</div></div>'
        '<div class="chip">TWO BROS <b>PRO QUALIFIER</b></div></div>')
js = """gsap.set(["#sg",".ex",".ex .idx",".ex .rule",".ex .nm",".ex .chip"], { opacity:0 });
tl.fromTo(".ex", { opacity:0 }, { opacity:1, duration:f(0.3), ease:"power1.out", immediateRender:false }, f(4.3));
tl.fromTo("#sg", { opacity:0, y:-40, scale:0.9 }, { opacity:1, y:0, scale:1, duration:f(0.55), ease:"back.out(1.5)", immediateRender:false }, f(0.5));
tl.to("#sg", { scale:1.04, duration:f(3.0), ease:"none" }, f(1.05));
tl.to("#sg", { opacity:0, y:-30, duration:f(0.35), ease:"power2.in" }, f(4.1));
tl.fromTo(".ex .idx", { opacity:0, x:-20 }, { opacity:1, x:0, duration:f(0.3), ease:"power2.out", immediateRender:false }, f(4.2));
tl.fromTo(".ex .rule", { opacity:1, scaleX:0 }, { scaleX:1, duration:f(0.35), ease:"power3.inOut", immediateRender:false }, f(4.25));
tl.fromTo(".ex .nm", { opacity:1, yPercent:110 }, { yPercent:0, duration:f(0.5), ease:"expo.out", immediateRender:false }, f(4.3));
tl.fromTo(".ex .chip", { opacity:0, y:12 }, { opacity:1, y:0, duration:f(0.35), ease:"back.out(1.6)", immediateRender:false }, f(4.7));
tl.to(".ex .nm", { yPercent:-110, duration:f(0.35), ease:"power2.in" }, f(7.4));
tl.to(".ex", { opacity:0, duration:f(0.3) }, f(7.5));"""
page('v3-drive', DD, body, js, css)

json.dump(made, open('made.json', 'w')); print(made, 'cues dur', CUE_DUR, 'note dur', ND)
