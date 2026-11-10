"""Event graphics for the retimed cut (output-time comps, 16:9 alpha, same canvas + style as build.py).
Each fx comp lasts exactly as long as its slow-mo / freeze segment (scripts/timemap.py) or its own 'dur'."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/scripts')
from build import write
import timemap as TM

CSS = """
.cap { position:absolute; left:0; right:0; bottom:118px; display:flex; flex-direction:column; align-items:center; gap:14px; }
.k { font-family:"JetBrains Mono"; font-weight:700; font-size:26px; letter-spacing:0.3em; color:#fff; background:#d80609; padding:9px 18px 8px 22px; }
.t { font-weight:900; font-style:italic; font-size:84px; line-height:1; letter-spacing:-0.01em; color:#fff; white-space:nowrap;
  text-shadow:0 4px 0 rgba(0,0,0,0.55), 0 0 30px rgba(0,0,0,0.75), 0 0 2px #000; }
.t b { color:#ff2a2d; font-weight:900; }
.s { font-family:"JetBrains Mono"; font-weight:600; font-size:24px; letter-spacing:0.3em; color:rgba(255,255,255,0.85); text-shadow:0 2px 10px #000; }
.vig { position:absolute; inset:0; opacity:0; background:radial-gradient(ellipse 75% 70% at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%); }
.slo { position:absolute; left:50%; top:46px; transform:translateX(-50%); display:flex; align-items:center; gap:12px; opacity:0;
  font-family:"JetBrains Mono"; font-weight:700; font-size:24px; letter-spacing:0.3em; color:#fff; background:rgba(10,10,12,0.7); padding:9px 18px; border-radius:30px; }
.slo i { width:14px; height:14px; border-radius:50%; background:#d80609; box-shadow:0 0 10px #ff2a2d; }
.bf { width:46px; height:32px; position:relative; }
.bf::before { content:""; position:absolute; left:0; top:-4px; width:4px; height:44px; background:#ddd; }
.bf::after { content:""; position:absolute; left:4px; top:0; width:42px; height:28px; background:#1565ff; box-shadow:0 0 12px rgba(40,110,255,0.8); }
"""

def caption(kicker, text, t_k, t_t, dur, sub=None, slow=None):
    body = '<div class="vig" id="vig"></div>' if slow else ''
    if slow:
        body += f'<div class="slo" id="slo"><i></i>SLOW-MO {slow}</div>'
    body += f'<div class="cap"><div class="k" id="k">{kicker}</div><div class="t" id="t">{text}</div>'
    body += (f'<div class="s" id="s">{sub}</div>' if sub else '') + '</div>'
    js = ''
    if slow:
        js += ('tl.to("#vig", { opacity:1, duration:0.4, ease:"power1.out" }, 0.0);'
               'tl.fromTo("#slo", { opacity:0, y:-16 }, { opacity:1, y:0, duration:0.35, ease:"back.out(2)", immediateRender:false }, 0.15);'
               'tl.fromTo("#slo i", { opacity:1 }, { opacity:0.25, duration:0.4, yoyo:true, repeat:%d, ease:"sine.inOut", immediateRender:false }, 0.5);'
               % max(1, int((dur - 1.2) / 0.4) // 2 * 2 - 1))
        js += f'tl.to(["#vig", "#slo"], {{ opacity:0, duration:0.3, ease:"power1.in" }}, {dur - 0.35:.3f});'
    js += f"""
tl.fromTo("#k", {{ opacity:0, clipPath:"inset(0 100% 0 0)" }}, {{ opacity:1, clipPath:"inset(0 0% 0 0)", duration:0.4, ease:"expo.out", immediateRender:true }}, {t_k:.3f});
tl.fromTo("#t", {{ opacity:0, scale:1.35, y:10 }}, {{ opacity:1, scale:1, y:0, duration:0.32, ease:"back.out(1.8)", immediateRender:true }}, {t_t:.3f});
"""
    if sub:
        js += f'tl.fromTo("#s", {{ opacity:0, y:12 }}, {{ opacity:1, y:0, duration:0.4, ease:"power2.out", immediateRender:true }}, {t_t + 0.3:.3f});'
    js += f'tl.to(".cap", {{ opacity:0, y:24, duration:0.35, ease:"power2.in" }}, {dur - 0.4:.3f});'
    return body, js

def segdur(sid):
    p = TM.SEG[sid]; return p['frames'] / TM.FPS

def lead():
    d = segdur('lead')
    b, j = caption('BATTLE FOR THE LEAD', 'SIDE BY SIDE… <b>CONTACT!</b>', 0.3, 0.8, d, slow='0.5×')
    write('fx-lead', d, b, j, CSS)

def signal():
    d = segdur('signal')
    b, j = caption('THE HAND SIGNAL', '“STOP FIGHTING — <b>PUSH ON!</b>”', 0.2, 0.55, d, sub='TO THE DRIVER BEHIND: LET’S PULL AWAY TOGETHER', slow='0.5×')
    write('fx-signal', d, b, j, CSS)

def listen():
    d = segdur('listen')
    b, j = caption('OVERTAKEN · P2', 'YEP… HE <b>DIDN’T LISTEN.</b>', 0.25, 0.6, d, slow='0.6×')
    write('fx-listen', d, b, j, CSS)

def spin():
    d = segdur('spin')
    b, j = caption('LAPPED TRAFFIC', 'BACKMARKER <b>SPINS!</b>', 0.2, 0.9, d, slow='0.4×')
    write('fx-spin', d, b, j, CSS)

def hello():
    d = segdur('hello')
    b, j = caption('SAYING HELLO TO THE LEADER', '“I’M <b>STILL HERE!</b>”', 0.2, 0.6, d, slow='0.5×')
    write('fx-hello', d, b, j, CSS)

def look():
    d = segdur('look'); p = TM.SEG['look']; fz = (p['t1'] - p['t0']) / p['speed']   # freeze starts here
    css = CSS + """
#fl { position:absolute; inset:0; background:#fff; opacity:0; }
#frz { position:absolute; inset:0; border:10px solid rgba(255,255,255,0.9); opacity:0; }
"""
    b, j = caption('THE LEADER LOOKS BEHIND…', '…FOR THE <b>4,000TH TIME</b>', fz + 0.05, fz + 0.3, d, slow='0.5×')
    b = '<div id="frz"></div><div id="fl"></div>' + b
    j += f"""
tl.fromTo("#fl", {{ opacity:0.85 }}, {{ opacity:0, duration:0.35, ease:"power2.out", immediateRender:false }}, {fz:.3f});
tl.fromTo("#frz", {{ opacity:1, scale:1.04 }}, {{ opacity:0.85, scale:1, duration:0.3, ease:"power3.out", immediateRender:false }}, {fz:.3f});
tl.to("#frz", {{ opacity:0, duration:0.2, ease:"power1.in" }}, {d - 0.25:.3f});
"""
    write('fx-look', d, b, j, css)

def pb():
    d = 4.0
    css = """
#band { position:absolute; left:-100px; top:330px; width:2120px; height:210px; transform:skewY(-4deg); transform-origin:50% 50%; overflow:hidden;
  background:linear-gradient(90deg, rgba(90,62,8,0.94), rgba(214,166,40,0.96) 30%, rgba(255,226,120,0.97) 50%, rgba(214,166,40,0.96) 70%, rgba(90,62,8,0.94));
  box-shadow:0 18px 50px rgba(0,0,0,0.55), 0 0 60px rgba(255,200,60,0.35); border-top:4px solid #fff3c4; border-bottom:4px solid #fff3c4; }
#shine { position:absolute; top:-40px; left:-500px; width:300px; height:300px; background:linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.65), rgba(255,255,255,0)); transform:skewX(-20deg); }
#txt { position:absolute; left:0; right:0; top:330px; height:210px; display:flex; flex-direction:column; align-items:center; justify-content:center; transform:skewY(-4deg); }
#kk { font-family:"JetBrains Mono"; font-weight:700; font-size:30px; letter-spacing:0.45em; color:#3a2500; padding-left:14px; }
#tt { font-weight:900; font-style:italic; font-size:112px; line-height:1; color:#1e1300; letter-spacing:-0.01em; margin-top:6px; text-shadow:0 2px 0 rgba(255,240,190,0.6); }
"""
    body = ('<div id="band"><div id="shine"></div></div>'
            '<div id="txt"><div id="kk">◆ CROSSING THE LINE ◆</div><div id="tt">PERSONAL BEST LAP INCOMING</div></div>')
    js = f"""
tl.fromTo("#band", {{ scaleX:0, opacity:1 }}, {{ scaleX:1, duration:0.45, ease:"expo.out", immediateRender:true }}, 0.1);
tl.fromTo("#kk", {{ opacity:0, y:-14 }}, {{ opacity:1, y:0, duration:0.35, ease:"power3.out", immediateRender:true }}, 0.35);
tl.fromTo("#tt", {{ opacity:0, scale:1.3 }}, {{ opacity:1, scale:1, duration:0.32, ease:"back.out(1.8)", immediateRender:true }}, 0.45);
tl.fromTo("#shine", {{ x:0 }}, {{ x:2900, duration:1.1, ease:"power2.inOut", immediateRender:true }}, 0.8);
tl.fromTo("#shine", {{ x:0 }}, {{ x:2900, duration:1.1, ease:"power2.inOut", immediateRender:false }}, 2.2);
tl.to(["#band", "#txt"], {{ opacity:0, y:-30, duration:0.35, ease:"power2.in" }}, {d - 0.45:.3f});
"""
    write('fx-pb', d, body, js, css)

HKC = """
.wp { position:absolute; inset:0; background:linear-gradient(110deg, #ff5a1f 0%, #ff7a2e 60%, #f5c242 100%); }
.wp .lg { position:absolute; left:0; right:0; top:50%; transform:translateY(-50%); text-align:center; font-weight:900; font-style:italic; font-size:220px;
  line-height:1; color:#111; letter-spacing:-0.02em; }
.wp .lg small { display:block; font-family:"JetBrains Mono"; font-style:normal; font-weight:700; font-size:30px; letter-spacing:0.4em; margin-top:16px; color:#1a0b00; }
"""

def pause():
    d = segdur('pause'); p = TM.SEG['pause']; fz = (p['t1'] - p['t0']) / p['speed']
    css = CSS + HKC + """
#frz { position:absolute; inset:0; border:10px solid rgba(255,255,255,0.9); opacity:0; }
#ps { position:absolute; left:50%; top:230px; width:150px; height:170px; margin-left:-75px; display:flex; gap:34px; opacity:0; }
#ps i { flex:1; background:#fff; border-radius:8px; box-shadow:0 0 40px rgba(0,0,0,0.6); }
"""
    b, j = caption('HOLD UP…', 'QUICK ONE <b>BEFORE WE CONTINUE</b>', fz + 0.1, fz + 0.3, d - 0.4)
    b = '<div class="vig" id="vg"></div><div id="frz"></div><div id="ps"><i></i><i></i></div>' + b + '<div class="wp" id="wp"><div class="lg">HKC<small>HEAVYWEIGHT KARTING CHAMPIONSHIP</small></div></div>'
    j += f"""
tl.to("#vg", {{ opacity:1, duration:0.2 }}, {fz:.3f});
tl.fromTo("#frz", {{ opacity:1, scale:1.04 }}, {{ opacity:0.85, scale:1, duration:0.3, ease:"power3.out", immediateRender:false }}, {fz:.3f});
tl.fromTo("#ps", {{ opacity:0, scale:1.6 }}, {{ opacity:0.95, scale:1, duration:0.25, ease:"back.out(2)", immediateRender:false }}, {fz:.3f});
tl.fromTo("#wp", {{ xPercent:-102 }}, {{ xPercent:0, duration:0.4, ease:"power3.in", immediateRender:true }}, {d - 0.4:.3f});
"""
    write('fx-pause', d, b, j, css)

def hkcad():
    d = segdur('ad'); cta = 8.0
    css = CSS + HKC + """
#chip { position:absolute; left:60px; bottom:56px; display:flex; align-items:center; gap:14px; opacity:0;
  font-family:"JetBrains Mono"; font-weight:700; font-size:24px; letter-spacing:0.28em; color:#fff; background:rgba(10,10,12,0.82); padding:12px 22px; border-left:6px solid #ff5a1f; }
#cta { position:absolute; left:0; right:0; bottom:0; height:300px; opacity:0;
  background:linear-gradient(180deg, rgba(10,10,12,0) 0%, rgba(10,10,12,0.92) 30%, rgba(10,10,12,0.97) 100%); }
#ctain { position:absolute; left:0; right:0; bottom:50px; display:flex; flex-direction:column; align-items:center; gap:16px; }
#c1 { font-family:"JetBrains Mono"; font-weight:700; font-size:28px; letter-spacing:0.3em; color:#111; background:#f5c242; padding:10px 22px 9px 28px; }
#c2 { display:flex; align-items:center; gap:24px; font-weight:900; font-style:italic; font-size:76px; line-height:1; color:#fff; }
#ig { width:70px; height:70px; border-radius:20px; position:relative;
  background:radial-gradient(circle at 30% 110%, #fdf497 0%, #fd5949 45%, #d6249f 60%, #285AEB 95%); }
#ig::before { content:""; position:absolute; inset:14px; border:6px solid #fff; border-radius:16px; }
#ig::after { content:""; position:absolute; left:23px; top:23px; width:12px; height:12px; border:6px solid #fff; border-radius:50%; }
#c3 { font-family:"JetBrains Mono"; font-weight:600; font-size:26px; letter-spacing:0.22em; color:rgba(255,255,255,0.85); }
"""
    b = ('<div id="chip">AD BREAK · HKC</div>'
         '<div id="cta"><div id="ctain"><div id="c1">INTERESTED? LET ME KNOW</div>'
         '<div id="c2"><i id="ig"></i>@heavyweight_karting_48</div><div id="c3">COMMENT BELOW OR DM ME ON INSTAGRAM</div></div></div>'
         '<div class="wp" id="w1"><div class="lg">HKC<small>HEAVYWEIGHT KARTING CHAMPIONSHIP</small></div></div>'
         '<div class="wp" id="w2"><div class="lg">HKC<small>BACK TO THE RACE</small></div></div>')
    j = f"""
tl.fromTo("#w1", {{ xPercent:0 }}, {{ xPercent:102, duration:0.5, ease:"power3.out", immediateRender:true }}, 0.35);
tl.fromTo("#chip", {{ opacity:0, x:-30 }}, {{ opacity:1, x:0, duration:0.4, ease:"power3.out", immediateRender:true }}, 0.9);
tl.to("#chip", {{ opacity:0, duration:0.3 }}, {d - cta:.3f});
tl.fromTo("#cta", {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:0.5, ease:"expo.out", immediateRender:true }}, {d - cta:.3f});
tl.fromTo("#c1", {{ opacity:0, clipPath:"inset(0 100% 0 0)" }}, {{ opacity:1, clipPath:"inset(0 0% 0 0)", duration:0.4, ease:"expo.out", immediateRender:true }}, {d - cta + 0.3:.3f});
tl.fromTo("#c2", {{ opacity:0, scale:1.3 }}, {{ opacity:1, scale:1, duration:0.35, ease:"back.out(1.8)", immediateRender:true }}, {d - cta + 0.55:.3f});
tl.fromTo("#c3", {{ opacity:0, y:12 }}, {{ opacity:1, y:0, duration:0.4, ease:"power2.out", immediateRender:true }}, {d - cta + 0.85:.3f});
tl.to("#ig", {{ scale:1.12, duration:0.5, yoyo:true, repeat:5, ease:"sine.inOut" }}, {d - cta + 1.4:.3f});
tl.fromTo("#w2", {{ xPercent:-102 }}, {{ xPercent:0, duration:0.45, ease:"power3.in", immediateRender:true }}, {d - 0.45:.3f});
"""
    write('fx-hkcad', d, b, j, css)

def back():
    d = 1.6
    css = CSS + HKC
    b = '<div class="wp" id="w"><div class="lg">HKC<small>BACK TO THE RACE</small></div></div>'
    j = 'tl.fromTo("#w", { xPercent:0 }, { xPercent:102, duration:0.5, ease:"power3.out", immediateRender:true }, 0.15);'
    j += 'tl.set({}, {}, %.2f);' % d
    write('fx-back', d, b, j, css)

def move():
    d = segdur('move')
    b, j = caption('<span style="display:inline-flex;align-items:center;gap:14px"><span class="bf"></span>LAPPED LIGHTWEIGHT</span>',
                   'MOVE <b>OVER!</b>', 0.15, 0.45, d, sub='HEAVYWEIGHT WIN ON THE LINE')
    write('fx-move', d, b, j, CSS)

def wave():
    d = segdur('wave')
    b, j = caption('THE WAVE', '…AND HE’S <b>LOOKING BACK</b>', 0.2, 1.3, d, slow='0.6×')
    write('fx-wave', d, b, j, CSS)

def lunge():
    d = segdur('lunge')
    b, j = caption('THE LUNGE', 'UP THE INSIDE <b>FOR P2!</b>', 0.3, 3.3, d, slow='0.5×')
    write('fx-lunge', d, b, j, CSS)

def gone():
    d = 2.8
    b, j = caption('BACK TO P3', '…AND IT’S <b>GONE.</b>', 0.1, 0.35, d)
    write('fx-gone', d, b, j, CSS)

def contact():
    d = segdur('contact'); p = TM.SEG['contact']; fz = (p['t1'] - p['t0']) / p['speed']   # freeze starts here
    css = CSS + """
#fl { position:absolute; inset:0; background:#fff; opacity:0; }
#ct { position:absolute; left:0; right:0; top:226px; text-align:center; font-weight:900; font-style:italic; font-size:190px; line-height:1;
  color:#fff; letter-spacing:-0.02em; text-shadow:0 8px 0 #8a0002, 0 0 40px rgba(216,6,9,0.9); opacity:0; }
#ck { position:absolute; left:50%; top:166px; transform:translateX(-50%); opacity:0; }
.ln { position:absolute; top:318px; height:10px; width:420px; background:linear-gradient(90deg, rgba(255,42,45,0), #ff2a2d); opacity:0; }
#l1 { left:60px; } #l2 { right:60px; background:linear-gradient(270deg, rgba(255,42,45,0), #ff2a2d); }
#frz { position:absolute; inset:0; border:10px solid rgba(255,255,255,0.9); opacity:0; }
"""
    body = ('<div class="vig" id="vig"></div><div class="slo" id="slo"><i></i>SLOW-MO 0.5×</div><div id="frz"></div><div id="fl"></div>'
            '<div class="k" id="ck">P1 vs P2</div><div class="ln" id="l1"></div><div class="ln" id="l2"></div><div id="ct">CONTACT!</div>')
    js = f"""
tl.to("#vig", {{ opacity:1, duration:0.3, ease:"power1.out" }}, 0);
tl.fromTo("#slo", {{ opacity:0, y:-16 }}, {{ opacity:1, y:0, duration:0.35, ease:"back.out(2)", immediateRender:false }}, 0.1);
tl.set("#slo", {{ opacity:0 }}, {fz:.3f});
tl.fromTo("#fl", {{ opacity:0.9 }}, {{ opacity:0, duration:0.35, ease:"power2.out", immediateRender:false }}, {fz:.3f});
tl.fromTo("#frz", {{ opacity:1, scale:1.04 }}, {{ opacity:0.85, scale:1, duration:0.3, ease:"power3.out", immediateRender:false }}, {fz:.3f});
tl.fromTo("#ct", {{ opacity:0, scale:2.2 }}, {{ opacity:1, scale:1, duration:0.22, ease:"power4.out", immediateRender:false }}, {fz + 0.05:.3f});
tl.fromTo("#ck", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.3, ease:"back.out(2)", immediateRender:false }}, {fz + 0.25:.3f});
tl.fromTo(["#l1", "#l2"], {{ opacity:0, scaleX:0.2 }}, {{ opacity:1, scaleX:1, duration:0.3, ease:"expo.out", immediateRender:false }}, {fz + 0.1:.3f});
tl.to("#ct", {{ x:6, duration:0.05, yoyo:true, repeat:5, ease:"none" }}, {fz + 0.27:.3f});
tl.to(["#ct", "#ck", "#l1", "#l2", "#frz", "#vig"], {{ opacity:0, duration:0.2, ease:"power1.in" }}, {d - 0.22:.3f});
"""
    write('fx-contact', d, body, js, css)

def backmarkers():
    d = 4.5
    css = CSS + """
#bmw { position:absolute; left:0; right:0; top:240px; display:flex; justify-content:center; }
#bm { display:flex; align-items:center; gap:22px; opacity:0;
  background:linear-gradient(90deg, rgba(12,26,70,0.92), rgba(8,14,40,0.92)); border-left:8px solid #1565ff; padding:16px 30px 16px 24px; border-radius:6px;
  box-shadow:0 10px 30px rgba(0,0,0,0.5), 0 0 30px rgba(21,101,255,0.35); }
#bm .w { display:flex; flex-direction:column; gap:4px; }
#bm .a { font-weight:900; font-style:italic; font-size:52px; line-height:1; color:#fff; }
#bm .b { font-family:"JetBrains Mono"; font-weight:700; font-size:22px; letter-spacing:0.3em; color:#8fb4ff; }
#flag { width:70px; height:60px; position:relative; }
#pole { position:absolute; left:0; top:0; width:5px; height:60px; background:#e8e8e8; border-radius:2px; }
#cloth { position:absolute; left:5px; top:2px; width:62px; height:40px; background:#1565ff; transform-origin:0 50%;
  box-shadow:0 0 16px rgba(40,110,255,0.8); clip-path:polygon(0 0, 100% 8%, 92% 50%, 100% 92%, 0 100%); }
"""
    body = '<div id="bmw"><div id="bm"><div id="flag"><div id="pole"></div><div id="cloth"></div></div><div class="w"><div class="a">BACKMARKERS AHEAD</div><div class="b">LAPPED TRAFFIC · BLUE FLAGS</div></div></div></div>'
    js = f"""
tl.fromTo("#bm", {{ opacity:0, y:-30 }}, {{ opacity:1, y:0, duration:0.45, ease:"back.out(1.8)", immediateRender:true }}, 0.15);
tl.fromTo("#cloth", {{ skewY:-8, scaleX:0.86 }}, {{ skewY:8, scaleX:1, duration:0.3, yoyo:true, repeat:{int((d - 0.8) / 0.3) // 2 * 2 - 1}, ease:"sine.inOut", immediateRender:true }}, 0.2);
tl.to("#bm", {{ opacity:0, y:-20, duration:0.35, ease:"power2.in" }}, {d - 0.45:.3f});
"""
    write('fx-backmarkers', d, body, js, css)

def hit(name, d=1.2):
    """Call-of-Duty style 'you've been hit' flash: blood-red edge vignette + hit-marker ticks."""
    css = """
#rv { position:absolute; inset:0; opacity:0; background:radial-gradient(ellipse 70% 65% at 50% 50%, rgba(160,0,0,0) 45%, rgba(170,0,0,0.55) 75%, rgba(120,0,0,0.92) 100%); }
#wf { position:absolute; inset:0; background:#fff; opacity:0; }
#hm { position:absolute; left:930px; top:510px; width:60px; height:60px; opacity:0; }
#hm i { position:absolute; width:22px; height:5px; background:#fff; box-shadow:0 0 6px rgba(0,0,0,0.8); }
#hm i:nth-child(1) { left:0; top:6px; transform:rotate(45deg); } #hm i:nth-child(2) { right:0; top:6px; transform:rotate(-45deg); }
#hm i:nth-child(3) { left:0; bottom:6px; transform:rotate(-45deg); } #hm i:nth-child(4) { right:0; bottom:6px; transform:rotate(45deg); }
"""
    body = '<div id="rv"></div><div id="wf"></div><div id="hm"><i></i><i></i><i></i><i></i></div>'
    js = f"""
tl.fromTo("#wf", {{ opacity:0.35 }}, {{ opacity:0, duration:0.12, ease:"power2.out", immediateRender:false }}, 0.0);
tl.fromTo("#rv", {{ opacity:1 }}, {{ opacity:0, duration:{d - 0.1:.2f}, ease:"power2.in", immediateRender:false }}, 0.0);
tl.fromTo("#hm", {{ opacity:1, scale:1.5 }}, {{ opacity:0, scale:1, duration:0.35, ease:"power2.out", immediateRender:false }}, 0.0);
"""
    write(name, d, body, js, css)

def towel():
    d = 4.0
    css = CSS + """
#tw { position:absolute; left:1500px; top:-260px; width:300px; height:230px; }
"""
    svg = ('<svg id="tw" viewBox="0 0 300 230"><defs><linearGradient id="tg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/>'
           '<stop offset="1" stop-color="#d9dde2"/></linearGradient></defs>'
           '<path d="M20,30 C80,5 160,40 280,18 C270,80 290,140 272,205 C190,222 110,190 28,214 C40,150 8,95 20,30 Z" fill="url(#tg)" stroke="#b9bec5" stroke-width="3"/>'
           '<path d="M24,58 C90,38 170,70 278,48" stroke="#c7ccd2" stroke-width="7" fill="none"/>'
           '<path d="M30,182 C100,166 180,196 276,178" stroke="#c7ccd2" stroke-width="7" fill="none"/>'
           '<path d="M60,40 C70,100 50,150 62,200 M150,30 C140,90 160,150 146,205 M230,25 C240,90 222,150 236,200" stroke="#e7eaee" stroke-width="5" fill="none"/></svg>')
    body = svg + '<div class="cap"><div class="k" id="k">AT THIS POINT…</div><div class="t" id="t">I THREW IN <b>THE TOWEL</b></div></div>'
    js = f"""
tl.fromTo("#tw", {{ x:0, y:0, rotation:-30 }}, {{ x:-640, y:520, rotation:250, duration:1.1, ease:"power1.in", immediateRender:true }}, 0.1);
tl.to("#tw", {{ y:560, rotation:262, scaleY:0.7, duration:0.18, ease:"power2.out" }}, 1.2);
tl.to("#tw", {{ y:540, scaleY:1, duration:0.25, ease:"power1.inOut" }}, 1.38);
tl.fromTo("#k", {{ opacity:0, clipPath:"inset(0 100% 0 0)" }}, {{ opacity:1, clipPath:"inset(0 0% 0 0)", duration:0.4, ease:"expo.out", immediateRender:true }}, 1.0);
tl.fromTo("#t", {{ opacity:0, scale:1.35 }}, {{ opacity:1, scale:1, duration:0.32, ease:"back.out(1.8)", immediateRender:true }}, 1.25);
tl.to(["#tw", ".cap"], {{ opacity:0, duration:0.35, ease:"power2.in" }}, {d - 0.4:.3f});
"""
    write('fx-towel', d, body, js, css)

def p3():
    d = 6.0
    css = """
#band { position:absolute; left:-100px; top:400px; width:2120px; height:330px; transform:skewY(-6deg); transform-origin:50% 50%;
  background:linear-gradient(90deg, rgba(60,28,6,0.95), rgba(150,80,26,0.95) 45%, rgba(60,28,6,0.95)); box-shadow:0 20px 60px rgba(0,0,0,0.6); }
.chk { position:absolute; left:0; right:0; height:28px; background:conic-gradient(#fff 25%, #111 0 50%, #fff 0 75%, #111 0) 0 0/28px 28px; }
#c1 { top:0; } #c2 { bottom:0; }
#big { position:absolute; left:0; right:0; top:400px; text-align:center; font-weight:900; font-style:italic; font-size:270px; line-height:330px;
  background:linear-gradient(180deg, #ffe2bd 0%, #e0a46a 40%, #9a5520 75%, #ffcf9e 100%); -webkit-background-clip:text; background-clip:text; color:transparent;
  filter:drop-shadow(0 8px 0 rgba(0,0,0,0.5)); transform:skewY(-6deg); }
#nm { position:absolute; left:0; right:0; top:770px; text-align:center; font-weight:900; font-style:italic; font-size:64px; color:#fff;
  text-shadow:0 4px 0 rgba(0,0,0,0.6), 0 0 24px rgba(0,0,0,0.8); }
#sb { position:absolute; left:0; right:0; top:790px; text-align:center; font-family:"JetBrains Mono"; font-weight:700; font-size:28px; letter-spacing:0.35em; color:#ffcf9e;
  text-shadow:0 2px 10px #000; }
"""
    body = ('<div id="band"><div class="chk" id="c1"></div><div class="chk" id="c2"></div></div><div id="big">P3</div>'
            '<div id="sb">TNL SODI HEAVY · DAYTONA MK</div>')
    js = f"""
tl.fromTo("#band", {{ scaleX:0 }}, {{ scaleX:1, duration:0.5, ease:"expo.out", immediateRender:true }}, 0.1);
tl.fromTo(".chk", {{ backgroundPositionX:"0px" }}, {{ backgroundPositionX:"280px", duration:{d:.2f}, ease:"none", immediateRender:true }}, 0);
tl.fromTo("#big", {{ opacity:0, scale:2.4 }}, {{ opacity:1, scale:1, duration:0.35, ease:"power4.out", immediateRender:true }}, 0.45);
tl.to("#big", {{ x:5, duration:0.05, yoyo:true, repeat:5, ease:"none" }}, 0.8);
tl.fromTo("#sb", {{ opacity:0 }}, {{ opacity:1, duration:0.5, ease:"none", immediateRender:true }}, 1.2);
tl.to("#big", {{ scale:1.05, duration:3.5, ease:"sine.inOut" }}, 1.3);
tl.to(["#band", "#big"], {{ x:2200, duration:0.55, ease:"power3.in" }}, {d - 0.75:.3f});
tl.to("#sb", {{ opacity:0, duration:0.35, ease:"power1.in" }}, {d - 0.6:.3f});
"""
    write('fx-p3', d, body, js, css)

if __name__ == '__main__':
    lead(); pause(); hkcad(); back(); signal(); listen(); move(); wave(); lunge(); gone(); contact(); backmarkers(); spin(); hello(); pb(); look(); hit('fx-tap'); towel(); p3()
