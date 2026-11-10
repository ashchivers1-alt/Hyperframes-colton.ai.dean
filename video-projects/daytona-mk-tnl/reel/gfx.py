"""Overlay for the 9:16 reel: 1080x1920 layout rendered at 2x (2160x3840) with alpha.
Same type system as the race video (Montserrat 900 italic + JetBrains Mono chips, red #ff2a2d), HKC orange on the end card.
Text stays in the top ~60% (sky); IG/Shorts UI owns the bottom 20% and the right-hand icon column."""
import os, shutil
D = os.path.dirname(os.path.abspath(__file__)) + '/gfx'
WS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(D))))
GSAP = WS + '/video-projects/training-day/gfx/assets/gsap.min.js'
HFJSON = WS + '/video-projects/training-day/gfx/hyperframes.json'

# kicker, big line (<b> = red)
CAP = {
    'green':  ('TNL SODI HEAVY · DAYTONA MK', 'LIGHTS OUT. <b>FROM P3</b>'),
    'launch': ('NIGHT RACE · ONE WINNER', '11 <b>HEAVYWEIGHTS</b>'),
    'p1':     ('MAKING THE MOVE', 'INTO <b>THE LEAD!</b>'),
    'signal': ('TO THE DRIVER BEHIND', '“LET’S <b>PULL AWAY!</b>”'),
    'over':   ('…HE HAD OTHER IDEAS', 'HE <b>DIDN’T LISTEN.</b>'),
    'spin':   ('LAPPED TRAFFIC', 'BACKMARKER <b>SPINS!</b>'),
    'look':   ('THE LEADER LOOKS BACK…', '…<b>AGAIN.</b>'),
    'lunge':  ('LATE IN THE RACE', 'THE LUNGE <b>FOR P2!</b>'),
    'gone':   ('ONE CORNER LATER', '…AND IT’S <b>GONE.</b>'),
}
SLOW = {'hook': '0.5×', 'signal': '0.6×', 'over': '0.7×', 'spin': '0.5×', 'look': '0.5×', 'lunge': '0.75×'}

HEAD = """<!doctype html><html lang="en"><head><meta charset="UTF-8" />
<meta name="viewport" content="width=2160, height=3840" /><script src="assets/gsap.min.js"></script>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:2160px; height:3840px; overflow:hidden; background:transparent; }
#stage { position:relative; width:2160px; height:3840px; overflow:hidden; }
#root { position:relative; width:1080px; height:1920px; overflow:hidden; transform:scale(2); transform-origin:0 0; font-family:Montserrat, sans-serif; color:#f6f6f6; }
.mono { font-family:"JetBrains Mono", monospace; }
#top { position:absolute; left:0; right:0; top:0; height:820px; background:linear-gradient(180deg, rgba(0,0,0,0.62) 0%, rgba(0,0,0,0.3) 55%, rgba(0,0,0,0) 100%); }
#vig { position:absolute; inset:0; background:radial-gradient(ellipse 80% 70% at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%); }
#grain { position:absolute; inset:0; opacity:0.07; background:repeating-linear-gradient(0deg, rgba(255,255,255,0.5) 0 1px, rgba(0,0,0,0) 1px 3px); mix-blend-mode:overlay; }
/* position badge (callback: changes as places change) */
#pos { position:absolute; left:52px; top:200px; display:flex; align-items:stretch; opacity:0; filter:drop-shadow(0 6px 18px rgba(0,0,0,0.6)); }
#pos .l { font-family:"JetBrains Mono"; font-weight:700; font-size:20px; letter-spacing:0.25em; color:#fff; background:#d80609; padding:0 12px; display:flex; align-items:center; writing-mode:vertical-rl; transform:rotate(180deg); }
#pos .v { position:relative; width:150px; height:96px; background:rgba(10,10,12,0.85); overflow:hidden; }
#pos .v i { position:absolute; left:0; right:0; top:0; height:96px; text-align:center; font-style:italic; font-weight:900; font-size:76px; line-height:96px; color:#fff; opacity:0; }
#pos .v i.g { color:#f5c242; }
#slo { position:absolute; right:52px; top:214px; display:flex; align-items:center; gap:10px; opacity:0; font-family:"JetBrains Mono"; font-weight:700; font-size:22px; letter-spacing:0.25em; color:#fff; background:rgba(10,10,12,0.75); padding:9px 16px; border-radius:30px; }
#slo b { width:12px; height:12px; border-radius:50%; background:#d80609; box-shadow:0 0 10px #ff2a2d; }
/* shot captions */
.cap { position:absolute; left:40px; right:40px; top:360px; display:flex; flex-direction:column; align-items:center; gap:16px; opacity:0; text-align:center; }
.cap .k { font-family:"JetBrains Mono"; font-weight:700; font-size:26px; letter-spacing:0.28em; color:#fff; background:#d80609; padding:9px 16px 8px 20px; }
.cap .t { font-weight:900; font-style:italic; font-size:78px; line-height:0.98; letter-spacing:-0.01em; color:#fff;
  text-shadow:0 4px 0 rgba(0,0,0,0.55), 0 0 34px rgba(0,0,0,0.8), 0 0 2px #000; }
.cap .t b { color:#ff2a2d; font-weight:900; }
/* hook */
#hook { position:absolute; left:30px; right:30px; top:330px; text-align:center; font-weight:900; font-style:italic; line-height:0.92; }
#hook div { text-shadow:0 5px 0 rgba(0,0,0,0.55), 0 0 40px rgba(0,0,0,0.85); }
#h1 { font-size:86px; color:#fff; }
#h2 { font-size:108px; letter-spacing:-0.02em; background:linear-gradient(180deg,#ffffff 0%,#ff6a5c 38%,#d80609 62%,#7a0002 100%); -webkit-background-clip:text; background-clip:text; color:transparent; text-shadow:none !important; filter:drop-shadow(0 5px 0 rgba(0,0,0,0.6)) drop-shadow(0 0 28px rgba(255,42,45,0.55)); }
#h3 { font-size:74px; color:#fff; }
/* P1 slam */
#p1 { position:absolute; left:0; right:0; top:620px; text-align:center; font-weight:900; font-style:italic; font-size:380px; line-height:1; opacity:0;
  background:linear-gradient(180deg,#fff7d6 0%,#f5c242 45%,#b07a10 100%); -webkit-background-clip:text; background-clip:text; color:transparent;
  filter:drop-shadow(0 8px 0 rgba(0,0,0,0.6)) drop-shadow(0 0 40px rgba(245,194,66,0.7)); }
#ring { position:absolute; left:540px; top:810px; width:300px; height:300px; margin:-150px 0 0 -150px; border-radius:50%; border:10px solid #f5c242; opacity:0; }
/* PB band */
#pb { position:absolute; left:-40px; right:-40px; top:420px; height:250px; transform:skewY(-5deg); opacity:0; overflow:hidden;
  background:linear-gradient(100deg,#b07a10 0%,#f5c242 35%,#fff1b8 50%,#f5c242 65%,#b07a10 100%); box-shadow:0 0 60px rgba(245,194,66,0.55); }
#pb .sh { position:absolute; top:0; bottom:0; width:200px; left:-260px; background:linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.85), rgba(255,255,255,0)); }
#pbt { position:absolute; left:0; right:0; top:440px; transform:skewY(-5deg); text-align:center; opacity:0; color:#1b1000; }
#pbt .k { font-family:"JetBrains Mono"; font-weight:700; font-size:28px; letter-spacing:0.4em; padding-top:22px; }
#pbt .t { font-weight:900; font-style:italic; font-size:104px; line-height:0.95; margin-top:10px; }
/* P3 finish */
#chq { position:absolute; left:-60px; right:-60px; top:560px; height:440px; transform:skewY(-6deg); opacity:0;
  background:linear-gradient(100deg,#5a2c0c 0%,#cd7f32 35%,#f3c39a 50%,#cd7f32 65%,#5a2c0c 100%); box-shadow:0 0 70px rgba(205,127,50,0.6); }
#chq::before, #chq::after { content:""; position:absolute; left:0; right:0; height:34px;
  background:repeating-conic-gradient(#111 0 25%, #f4f4f4 0 50%) 0 0/34px 34px; }
#chq::before { top:-34px; } #chq::after { bottom:-34px; }
#p3 { position:absolute; left:0; right:0; top:560px; text-align:center; opacity:0; }
#p3 .n { font-weight:900; font-style:italic; font-size:330px; line-height:1;
  background:linear-gradient(180deg,#fff2e4 0%,#e9a467 40%,#8a4a1c 100%); -webkit-background-clip:text; background-clip:text; color:transparent;
  filter:drop-shadow(0 8px 0 rgba(0,0,0,0.55)); }
#p3 .k { display:inline-block; font-family:"JetBrains Mono"; font-weight:700; font-size:32px; letter-spacing:0.4em; color:#fff; background:#111; padding:12px 22px 10px 30px; margin-top:-10px; }
/* HKC end card */
#end { position:absolute; inset:0; opacity:0; background:radial-gradient(ellipse 90% 60% at 50% 38%, #3a1a08 0%, #150906 50%, #060606 100%); }
#end .glow { position:absolute; left:540px; top:640px; width:1100px; height:1100px; margin:-550px 0 0 -550px; border-radius:50%; background:radial-gradient(circle, rgba(255,90,31,0.35) 0%, rgba(255,90,31,0) 62%); }
#end .str { position:absolute; inset:0; background:repeating-linear-gradient(115deg, rgba(255,255,255,0.03) 0 2px, rgba(0,0,0,0) 2px 52px); }
#end .in { position:absolute; left:40px; right:40px; top:470px; display:flex; flex-direction:column; align-items:center; gap:26px; text-align:center; }
#end img { width:400px; height:400px; filter:drop-shadow(0 20px 50px rgba(0,0,0,0.7)) drop-shadow(0 0 30px rgba(255,90,31,0.45)); }
/* hook callback at the top of the end card */
#eh { position:absolute; left:30px; right:30px; top:175px; text-align:center; font-weight:900; font-style:italic; line-height:0.95; }
#eh1 { font-size:62px; color:#fff; text-shadow:0 4px 0 rgba(0,0,0,0.55); }
#eh2 { font-size:92px; letter-spacing:-0.02em; background:linear-gradient(180deg,#ffffff 0%,#ff6a5c 38%,#d80609 62%,#7a0002 100%); -webkit-background-clip:text; background-clip:text; color:transparent; filter:drop-shadow(0 4px 0 rgba(0,0,0,0.6)) drop-shadow(0 0 24px rgba(255,42,45,0.5)); }
#eh3 { font-size:54px; color:#fff; text-shadow:0 4px 0 rgba(0,0,0,0.55); }
#e1 { font-family:"JetBrains Mono"; font-weight:700; font-size:28px; letter-spacing:0.3em; color:#111; background:#ff5a1f; padding:11px 18px 10px 26px; }
#e2 { font-weight:900; font-style:italic; font-size:96px; line-height:0.95; color:#fff; text-shadow:0 5px 0 rgba(0,0,0,0.5); }
#e2 b { color:#ff5a1f; }
#e3 { font-weight:900; font-style:italic; font-size:58px; line-height:1.05; color:#f5c242; }
#e4 { display:flex; align-items:center; gap:18px; font-weight:800; font-size:42px; color:#fff; margin-top:6px; }
#ic { width:54px; height:54px; border-radius:15px; position:relative; background:radial-gradient(circle at 30% 110%, #fdf497 0%, #fd5949 45%, #d6249f 60%, #285AEB 95%); }
#ic::before { content:""; position:absolute; inset:11px; border:5px solid #fff; border-radius:12px; }
#ic::after { content:""; position:absolute; left:17px; top:17px; width:10px; height:10px; border:5px solid #fff; border-radius:50%; }
#wp { position:absolute; inset:0; background:linear-gradient(160deg,#ff5a1f 0%,#ff7a2e 60%,#f5c242 100%); }
</style></head><body><div id="stage" data-composition-id="main" data-start="0" data-duration="%DUR%" data-width="2160" data-height="3840">
<div id="root">%BODY%</div></div>
<script>(() => { const tl = gsap.timeline({ paused:true });
%JS%
tl.to({}, { duration:%DUR% }, 0); window.__timelines = window.__timelines || {}; window.__timelines["main"] = tl; })();</script>
</body></html>"""

def write(SH, END, TOTAL, logo):
    S = {s['id']: s for s in SH}
    st = lambda i: S[i]['start']
    en = lambda i: S[i]['start'] + S[i]['len']
    b = ['<div id="top"></div><div id="vig"></div><div id="grain"></div>']
    j = []
    # hook — three stacked lines slam in
    b.append('<div id="hook"><div id="h1">WHO’S THE BEST</div><div id="h2">HEAVYWEIGHT</div><div id="h3">DRIVER IN THE UK?</div></div>')
    j.append('tl.from("#h1", { scale:2.2, opacity:0, duration:0.3, ease:"expo.out" }, 0.12);')
    j.append('tl.from("#h2", { scale:2.6, opacity:0, filter:"blur(12px)", duration:0.35, ease:"back.out(1.6)" }, 0.42);')
    j.append('tl.from("#h3", { y:40, opacity:0, duration:0.35, ease:"power3.out" }, 0.78);')
    j.append(f'tl.to("#hook", {{ scale:1.06, duration:{st("green") - 1.2:.2f}, ease:"none" }}, 1.1);')
    j.append(f'tl.to("#hook", {{ opacity:0, y:-40, filter:"blur(8px)", duration:0.2, ease:"power2.in" }}, {st("green") - 0.12:.2f});')
    # slow-mo pill
    b.append('<div id="slo"><b></b><span id="slot">SLOW-MO</span></div>')
    for sid, txt in SLOW.items():
        j.append(f'tl.set("#slot", {{ textContent:"SLOW-MO {txt}" }}, {st(sid):.2f});')
        j.append(f'tl.fromTo("#slo", {{ opacity:0, x:20 }}, {{ opacity:1, x:0, duration:0.25, ease:"power3.out", immediateRender:false }}, {st(sid) + 0.15:.2f});')
        j.append(f'tl.to("#slo", {{ opacity:0, duration:0.15 }}, {en(sid) - 0.3:.2f});')
    # captions
    for sid, (k, t) in CAP.items():
        b.append(f'<div class="cap" id="c-{sid}"><div class="k">{k}</div><div class="t">{t}</div></div>')
        a, z = st(sid), en(sid)
        j.append(f'tl.fromTo("#c-{sid}", {{ opacity:0 }}, {{ opacity:1, duration:0.01, immediateRender:false }}, {a + 0.12:.2f});')
        j.append(f'tl.from("#c-{sid} .k", {{ clipPath:"inset(0 100% 0 0)", duration:0.3, ease:"expo.out" }}, {a + 0.12:.2f});')
        j.append(f'tl.from("#c-{sid} .t", {{ scale:1.35, opacity:0, duration:0.3, ease:"back.out(1.8)" }}, {a + 0.28:.2f});')
        j.append(f'tl.to("#c-{sid}", {{ opacity:0, y:-24, duration:0.16, ease:"power2.in" }}, {z - XD_OUT:.2f});')
    # position badge
    b.append('<div id="pos"><div class="l">POS</div><div class="v"><i id="q3">P3</i><i id="q1" class="g">P1</i><i id="q2">P2</i><i id="q3b">P3</i><i id="q2b">P2</i><i id="q3c">P3</i></div></div>')
    j.append(f'tl.fromTo("#pos", {{ opacity:0, x:-40 }}, {{ opacity:1, x:0, duration:0.35, ease:"expo.out", immediateRender:false }}, {st("green") + 0.3:.2f});')
    flips = [('q3', st('green') + 0.3), ('q1', st('p1') + 1.0), ('q2', st('over') + 0.8), ('q3b', st('lunge') + 0.1),
             ('q2b', en('lunge') - 0.35), ('q3c', st('gone') + 0.75)]
    for n, (q, t) in enumerate(flips):
        if n: j.append(f'tl.to("#{flips[n - 1][0]}", {{ yPercent:-100, opacity:0, duration:0.22, ease:"power3.in" }}, {t:.2f});')
        j.append(f'tl.fromTo("#{q}", {{ yPercent:100, opacity:0 }}, {{ yPercent:0, opacity:1, duration:0.28, ease:"back.out(1.6)", immediateRender:false }}, {t + (0.12 if n else 0):.2f});')
        if n: j.append(f'tl.fromTo("#pos .v", {{ backgroundColor:"rgba(216,6,9,0.9)" }}, {{ backgroundColor:"rgba(10,10,12,0.85)", duration:0.6, immediateRender:false }}, {t + 0.1:.2f});')
    j.append(f'tl.to("#pos", {{ opacity:0, x:-40, duration:0.25, ease:"power2.in" }}, {st("fin"):.2f});')
    # P1 slam
    b.append('<div id="ring"></div><div id="p1">P1</div>')
    t = st('p1') + 1.0
    j.append(f'tl.fromTo("#p1", {{ opacity:0, scale:2.8 }}, {{ opacity:1, scale:1, duration:0.28, ease:"expo.in", immediateRender:false }}, {t - 0.28:.2f});')
    j.append(f'tl.fromTo("#ring", {{ opacity:1, scale:0.6 }}, {{ opacity:0, scale:3.2, duration:0.6, ease:"power2.out", immediateRender:false }}, {t:.2f});')
    j.append(f'tl.to("#p1", {{ scale:1.06, duration:{en("p1") - t - 0.3:.2f}, ease:"none" }}, {t:.2f});')
    j.append(f'tl.to("#p1", {{ opacity:0, scale:0.7, duration:0.15, ease:"power2.in" }}, {en("p1") - XD_OUT:.2f});')
    # PB band
    b.append('<div id="pb"><div class="sh"></div></div><div id="pbt"><div class="k">◆ CROSSING THE LINE ◆</div><div class="t">PERSONAL<br>BEST LAP</div></div>')
    a = st('pb') + 0.15
    j.append(f'tl.fromTo("#pb", {{ opacity:1, scaleX:0 }}, {{ opacity:1, scaleX:1, duration:0.32, ease:"expo.out", immediateRender:false }}, {a:.2f});')
    j.append(f'tl.fromTo("#pbt", {{ opacity:0, scale:1.4 }}, {{ opacity:1, scale:1, duration:0.3, ease:"back.out(1.7)", immediateRender:false }}, {a + 0.18:.2f});')
    j.append(f'tl.to("#pb .sh", {{ x:1560, duration:0.8, ease:"power2.inOut" }}, {a + 0.5:.2f});')
    j.append(f'tl.to(["#pb","#pbt"], {{ opacity:0, y:-30, duration:0.16, ease:"power2.in" }}, {en("pb") - XD_OUT:.2f});')
    # P3 finish
    b.append('<div id="chq"></div><div id="p3"><div class="n">P3</div><div class="k">PODIUM FINISH</div></div>')
    a = st('fin') + 0.3
    j.append(f'tl.fromTo("#chq", {{ opacity:1, scaleX:0 }}, {{ opacity:1, scaleX:1, duration:0.35, ease:"expo.out", immediateRender:false }}, {a - 0.1:.2f});')
    j.append(f'tl.fromTo("#p3", {{ opacity:0, scale:2.4 }}, {{ opacity:1, scale:1, duration:0.26, ease:"expo.in", immediateRender:false }}, {a + 0.0:.2f});')
    j.append(f'tl.from("#p3 .k", {{ clipPath:"inset(0 100% 0 0)", duration:0.35, ease:"expo.out" }}, {a + 0.35:.2f});')
    j.append(f'tl.to("#p3", {{ scale:1.05, duration:1.4, ease:"none" }}, {a + 0.3:.2f});')
    # HKC end card: orange wipe up, then card
    b.append('<div id="end"><div class="glow"></div><div class="str"></div>'
             '<div id="eh"><div id="eh1">WHO’S THE BEST</div><div id="eh2">HEAVYWEIGHT</div><div id="eh3">DRIVER IN THE UK?</div></div><div class="in"><img id="lg" src="assets/hkc-logo.png" />'
             '<div id="e1">HEAVYWEIGHT KARTING CHAMPIONSHIP</div>'
             '<div id="e2">NEW CHAMPIONSHIP <b>INCOMING…</b></div>'
             '<div id="e3">COMMENT “HKC” TO REGISTER YOUR INTEREST</div>'
             '<div id="e4"><i id="ic"></i>@heavyweight_karting_48</div></div></div><div id="wp"></div>')
    j.append('tl.set("#wp", { yPercent:102 }, 0);')
    j.append(f'tl.fromTo("#wp", {{ yPercent:102 }}, {{ yPercent:0, duration:0.3, ease:"power3.in", immediateRender:false }}, {END - 0.3:.2f});')
    j.append(f'tl.set("#end", {{ opacity:1 }}, {END:.2f});')
    j.append(f'tl.to("#wp", {{ yPercent:-102, duration:0.4, ease:"power3.out" }}, {END + 0.05:.2f});')
    e = END + 0.2
    j.append(f'tl.from("#eh1", {{ scale:2, opacity:0, duration:0.28, ease:"expo.out" }}, {e:.2f});')
    j.append(f'tl.from("#eh2", {{ scale:2.4, opacity:0, filter:"blur(10px)", duration:0.32, ease:"back.out(1.6)" }}, {e + 0.2:.2f});')
    j.append(f'tl.from("#eh3", {{ y:30, opacity:0, duration:0.3, ease:"power3.out" }}, {e + 0.45:.2f});')
    j.append(f'tl.from("#lg", {{ scale:0.2, rotation:-220, opacity:0, duration:0.8, ease:"back.out(1.4)" }}, {e + 0.5:.2f});')
    j.append(f'tl.to("#lg", {{ rotation:5, duration:1.6, yoyo:true, repeat:3, ease:"sine.inOut" }}, {e + 1.4:.2f});')
    j.append(f'tl.from("#e1", {{ clipPath:"inset(0 100% 0 0)", duration:0.4, ease:"expo.out" }}, {e + 0.85:.2f});')
    j.append(f'tl.from("#e2", {{ scale:1.5, opacity:0, duration:0.35, ease:"back.out(1.8)" }}, {e + 1.1:.2f});')
    j.append(f'tl.from("#e3", {{ y:30, opacity:0, duration:0.4, ease:"power3.out" }}, {e + 1.4:.2f});')
    j.append(f'tl.from("#e4", {{ x:-40, opacity:0, duration:0.4, ease:"expo.out" }}, {e + 1.7:.2f});')
    j.append(f'tl.to("#e3", {{ scale:1.05, duration:0.5, yoyo:true, repeat:7, ease:"sine.inOut" }}, {e + 2.0:.2f});')
    j.append(f'tl.to("#end .glow", {{ scale:1.15, duration:1.4, yoyo:true, repeat:3, ease:"sine.inOut" }}, {e:.2f});')
    j.append(f'tl.to(["#top","#vig"], {{ opacity:0, duration:0.2 }}, {END:.2f});')
    os.makedirs(D + '/assets', exist_ok=True)
    open(D + '/index.html', 'w').write(HEAD.replace('%DUR%', f'{TOTAL:.3f}').replace('%BODY%', ''.join(b)).replace('%JS%', '\n'.join(j)))
    shutil.copy(GSAP, D + '/assets/'); shutil.copy(HFJSON, D); shutil.copy(logo, D + '/assets/hkc-logo.png')
    open(D + '/meta.json', 'w').write('{"id":"reel-gfx","name":"reel-gfx","width":2160,"height":3840,"fps":25}')
    print('wrote', D + '/index.html', TOTAL)

XD_OUT = 0.2
