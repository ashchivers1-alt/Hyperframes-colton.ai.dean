"""Generate the training-day overlay compositions (one standalone HTML per overlay).

Every overlay renders as ProRes 4444 MOV with alpha and sits on V2 of
"YouTube – Edit 01" over the matching V1 clip. Timing comes from the source
transcripts (word onsets in the source clip) minus the clip's in-point.
Run: python3 build.py   then render each with
     npx hyperframes render -c <name>.html --format mov -o renders/<name>.mov
"""
import json

HEAD = """<!doctype html>
<html lang="en"><head><meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<script src="assets/gsap.min.js"></script>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:1920px; height:1080px; overflow:hidden; background:transparent; }
#root { position:relative; width:1920px; height:1080px; overflow:hidden; font-family:Montserrat, sans-serif; }
/* Team Apexx keyword card (approved style A) */
.card { position:absolute; display:flex; align-items:stretch; border-radius:14px; overflow:hidden;
  background:rgba(10,10,10,0.78); box-shadow:0 18px 50px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.12);
  border:1px solid rgba(255,255,255,0.10); }
.bar { width:10px; background:#d80609; flex:none; }
.ct { padding:16px 30px 14px 22px; }
.kick { font-weight:700; font-size:20px; letter-spacing:0.32em; color:#a19f9f; }
.big { font-family:"Bebas Neue", sans-serif; font-size:76px; line-height:0.95; color:#f6f6f6; letter-spacing:0.02em; }
.big b { color:#d80609; font-weight:400; }
.small { font-weight:600; font-size:26px; color:#f6f6f6; line-height:1.3; }
.small b { color:#ff4b47; font-weight:800; }
%CSS%
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%DUR%" data-width="1920" data-height="1080">
%BODY%
</div>
<script>
(() => {
  const tl = gsap.timeline({ paused: true });
  const f = (s) => Math.round(s * 30) / 30;
%JS%
  tl.to({}, { duration: %DUR% }, 0);
  window.__timelines = window.__timelines || {};
  window.__timelines["main"] = tl;
})();
</script></body></html>
"""


def page(name, dur, body, js, css=""):
    html = HEAD.replace("%DUR%", str(dur)).replace("%BODY%", body).replace("%JS%", js).replace("%CSS%", css)
    open(f"{name}.html", "w").write(html)
    return name


def card_in(sel, t, dx=-60):
    return (f'  tl.fromTo("{sel}", {{ x:{dx}, opacity:0, filter:"blur(10px)" }}, {{ x:0, opacity:1, filter:"blur(0px)", duration:f(0.4), ease:"expo.out", immediateRender:false }}, f({t}));\n'
            f'  tl.fromTo("{sel} .bar", {{ scaleY:0, transformOrigin:"50% 100%" }}, {{ scaleY:1, duration:f(0.33), ease:"power3.out", immediateRender:false }}, f({t}+0.1));\n')


def card_out(sel, t):
    return f'  tl.to("{sel}", {{ x:-40, opacity:0, filter:"blur(8px)", duration:f(0.3), ease:"power2.in" }}, f({t}));\n'


made = []

# ---------- exercise titles (lower-left, 3.5s) ----------
TITLES = {
    "t-banded":   ("EXERCISE", "BANDED <b>GLUTE</b> KICKBACK"),
    "t-kickback": ("EXERCISE", "GLUTE KICKBACK <b>MACHINE</b>"),
    "t-hipthrust": ("EXERCISE", "HIP <b>THRUST</b> · MACHINE"),
    "t-legpress": ("COACHING", "LEG PRESS · <b>GLUTE</b>-FOCUSED SETUP"),
    "t-slmsquat": ("EXERCISE", "SINGLE-LEG <b>MACHINE</b> SQUAT"),
    "t-beltsquat": ("EXERCISE", "BELT <b>SQUAT</b>"),
    "t-cable":    ("EXERCISE", "CABLE <b>KICKBACK</b>"),
}
for name, (kick, big) in TITLES.items():
    body = f'<div class="card" id="c" style="left:72px; top:820px;"><div class="bar"></div><div class="ct"><div class="kick">{kick}</div><div class="big">{big}</div></div></div>'
    js = '  gsap.set("#c", { opacity:0 });\n' + card_in("#c", 0.2) + card_out("#c", 3.15)
    made.append(page(name, 3.5, body, js))

# ---------- Formula 75 intro (tub render, left of Ash) ----------
body = """
<div id="tubw" style="position:absolute; left:40px; top:120px; width:560px; height:620px;">
  <img src="assets/tub-official.jpg" style="position:absolute; left:-200px; top:-40px; width:960px; -webkit-mask-image:radial-gradient(ellipse 34% 46% at 50% 50%, #000 70%, transparent 100%); mask-image:radial-gradient(ellipse 34% 46% at 50% 50%, #000 70%, transparent 100%);" />
</div>
<div class="card" id="c" style="left:72px; top:770px;"><div class="bar"></div><div class="ct"><div class="kick">FIRST REACTIONS</div><div class="big">tbJP · FORMULA <b>75</b></div></div></div>
"""
js = ('  gsap.set(["#c","#tubw"], { opacity:0 });\n'
      '  tl.fromTo("#tubw", { y:500, opacity:0, filter:"blur(14px)" }, { y:0, opacity:1, filter:"blur(0px)", duration:f(0.8), ease:"power3.out", immediateRender:false }, f(0.3));\n'
      + card_in("#c", 0.7) +
      '  tl.to("#tubw", { y:-10, duration:f(2.4), ease:"sine.inOut", yoyo:true, repeat:1 }, f(1.1));\n'
      '  tl.to("#tubw", { y:500, opacity:0, filter:"blur(12px)", duration:f(0.43), ease:"power2.in" }, f(5.97));\n'
      + card_out("#c", 5.9))
made.append(page("f75-intro", 6.5, body, js))

# ---------- Formula 75 ingredients panel takeover (source 33.0 -> 63.8) ----------
S = 1000 / 1236          # panel scale
PX, PY = 48, 40          # panel position on screen
L = [389, 426, 463, 500, 537, 572, 608, 645, 683, 718, 753, 789, 825, 861, 898, 935, 970, 1006, 1042, 1077, 1113]
R = {"valine": (389, 36), "alphagpc": (608, 36), "cognizin": (645, 36), "huperzine": (683, 36), "caffeine": (753, 36), "teacrine": (1015, 74)}
T0 = 33.0
# (spoken source time, column, row-centre y, band height, exact panel name, exact panel amount)
TICKS = [
    (34.8, "L", L[0], 36, "L-Citrulline", "10,000mg"),
    (38.0, "L", L[3], 36, "PeptiPump®", "500mg"),
    (38.6, "L", L[4], 36, "Beetroot Extract", "2,000mg"),
    (39.9, "L", L[5], 36, "Pine Bark Extract", "300mg"),
    (41.1, "L", L[6], 36, "S7®", "100mg"),
    (41.6, "L", L[7], 36, "HydroPrime Glycerol®", "5,000mg"),
    (42.9, "L", L[8], 36, "Beta Alanine", "4,800mg"),
    (44.1, "L", L[9], 36, "Taurine", "4,000mg"),
    (45.2, "L", L[10], 36, "Betaine Anhydrous", "3,000mg"),
    (46.0, "L", L[11], 36, "Peak ATP®", "400mg"),
    (46.8, "L", L[14], 36, "Creatine Monohydrate", "5,000mg"),
    (57.4, "R", *R["alphagpc"], "Alpha GPC 50%", "1,200mg"),
    (57.9, "R", *R["cognizin"], "Cognizin®", "500mg"),
    (58.8, "R", *R["huperzine"], "Huperzine A", "200mcg"),
    (60.6, "R", *R["caffeine"], "Caffeine", "250mg"),
    (62.7, "R", *R["teacrine"], "Teacrine® 40%", "100mg (yielding 40mg)"),
]
COLX = {"L": (243, 632, 214), "R": (665, 1052, 903)}   # band x0, x1 (source px), tick x (screen px)
bands, ticks = [], []
for i, (t, col, y, h, nm, amt) in enumerate(TICKS):
    x0, x1, tx = COLX[col]
    top = PY + (y - h / 2) * S
    bands.append(f'<div class="band" id="b{i}" style="left:{PX + x0 * S - 4:.0f}px; top:{top:.0f}px; width:{(x1 - x0) * S + 8:.0f}px; height:{h * S:.0f}px;"></div>')
    ticks.append(f'<div class="tick" id="k{i}" style="left:{tx - 13}px; top:{PY + y * S - 13:.0f}px;">✓</div>')
css = """
#dimbg { position:absolute; inset:0; background:radial-gradient(ellipse 80% 90% at 40% 50%, rgba(5,7,10,0.96), rgba(5,7,10,0.9)); }
#panel { position:absolute; left:@PX@px; top:@PY@px; width:@PW@px; height:1000px; border-radius:22px; overflow:hidden; box-shadow:0 30px 80px rgba(0,0,0,0.7), 0 0 0 1px rgba(255,255,255,0.08); }
#panel img { width:100%%; height:100%%; display:block; }
.band { position:absolute; border-radius:6px; background:rgba(111,195,238,0.22); box-shadow:inset 3px 0 0 #6fc3ee, 0 0 18px rgba(111,195,238,0.35); }
.tick { position:absolute; width:26px; height:26px; border-radius:50%%; background:#2fbf71; color:#fff; font:800 17px/26px Montserrat, sans-serif; text-align:center; box-shadow:0 0 12px rgba(47,191,113,0.8); }
#side { position:absolute; left:1150px; top:70px; width:700px; }
#side .kick { font-size:22px; }
#cur { margin-top:30px; height:190px; }
.cn { position:absolute; left:0; width:700px; }
.cn .nm { font-family:"Bebas Neue", sans-serif; font-size:84px; line-height:0.95; color:#f6f6f6; }
.cn .am { font-weight:700; font-size:40px; color:#6fc3ee; margin-top:8px; }
#legend { position:absolute; left:1150px; top:960px; font-weight:600; font-size:22px; color:#a19f9f; }
#legend span { display:inline-block; width:24px; height:24px; border-radius:50%%; background:#2fbf71; color:#fff; text-align:center; font:800 15px/24px Montserrat; margin-right:10px; vertical-align:-4px; }
#tub { position:absolute; left:1290px; top:420px; width:460px; height:520px; -webkit-mask-image:radial-gradient(ellipse 40% 48% at 50% 50%, #000 70%, transparent 100%); mask-image:radial-gradient(ellipse 40% 48% at 50% 50%, #000 70%, transparent 100%); }
#tub img { position:absolute; left:-130px; top:-90px; width:700px; }
""".replace("@PX@", str(PX)).replace("@PY@", str(PY)).replace("@PW@", str(round(1290 * S))).replace("%%", "%")
curs = "".join(f'<div class="cn" id="n{i}"><div class="nm">{nm}</div><div class="am">{amt} · per 75g serving</div></div>' for i, (t, c, y, h, nm, amt) in enumerate(TICKS))
body = (f'<div id="dimbg"></div><div id="panel"><img src="assets/panel-official.jpg" /></div>'
        + "".join(bands) + "".join(ticks)
        + f'<div id="side"><div class="kick">INGREDIENT BREAKDOWN</div><div id="cur">{curs}</div></div>'
        + '<div id="tub"><img src="assets/tub-official.jpg" /></div>'
        + '<div id="legend"><span>✓</span>= mentioned in Ash\'s review (not a verified benefit)</div>')
js = '  gsap.set([".band",".tick",".cn"], { opacity:0 });\n'
js += '  tl.fromTo("#dimbg", { opacity:0 }, { opacity:1, duration:f(0.4), ease:"power2.out", immediateRender:false }, 0);\n'
js += '  tl.fromTo("#panel", { y:60, opacity:0, scale:0.96 }, { y:0, opacity:1, scale:1, duration:f(0.6), ease:"expo.out", immediateRender:false }, f(0.1));\n'
js += '  tl.fromTo(["#side","#legend"], { x:40, opacity:0 }, { x:0, opacity:1, duration:f(0.5), ease:"power3.out", stagger:0.1, immediateRender:false }, f(0.35));\n'
js += '  tl.fromTo("#tub", { y:60, opacity:0 }, { y:0, opacity:1, duration:f(0.7), ease:"power3.out", immediateRender:false }, f(0.5));\n'
for i, (t, *_rest) in enumerate(TICKS):
    lt = round(t - T0 - 0.1, 2)
    nxt = round(TICKS[i + 1][0] - T0 - 0.1, 2) if i + 1 < len(TICKS) else 30.4
    hold = round(min(nxt, lt + 3.0), 2)   # active until the next ingredient (max 3s), then stays dimly ticked
    js += f'  tl.fromTo("#b{i}", {{ opacity:0, scaleX:0.2, transformOrigin:"0% 50%" }}, {{ opacity:1, scaleX:1, duration:f(0.2), ease:"power2.out", immediateRender:false }}, f({lt}));\n'
    js += f'  tl.to("#b{i}", {{ opacity:0.35, duration:f(0.4), ease:"power1.out" }}, f({hold}));\n'
    js += f'  tl.fromTo("#k{i}", {{ opacity:0, scale:2.2 }}, {{ opacity:1, scale:1, duration:f(0.27), ease:"back.out(2.5)", immediateRender:false }}, f({lt + 0.05}));\n'
    js += f'  tl.fromTo("#n{i}", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:f(0.2), ease:"power2.out", immediateRender:false }}, f({lt}));\n'
    js += f'  tl.to("#n{i}", {{ opacity:0, y:-14, duration:f(0.15), ease:"power2.in" }}, f({hold - 0.15}));\n'
js += '  tl.to(["#panel","#side","#legend","#tub",".band",".tick"], { opacity:0, duration:f(0.33), ease:"power2.in" }, f(30.37));\n'
js += '  tl.to("#dimbg", { opacity:0, duration:f(0.4), ease:"power1.inOut" }, f(30.4));\n'
made.append(page("f75-panel", 30.8, body, js, css))

# ---------- Discount code ----------
body = '<div class="card" id="c" style="left:72px; top:800px;"><div class="bar"></div><div class="ct"><div class="kick">tbJP</div><div class="big">DISCOUNT CODE: <b>ASH10</b></div></div></div>'
js = '  gsap.set("#c", { opacity:0 });\n' + card_in("#c", 0.3) + card_out("#c", 10.25)
made.append(page("ash10", 10.7, body, js))

# ---------- Leg press cues A/B (item 21, source 14.5 -> 49.5) ----------
L0 = 14.5
# freeze-frame knee line: ankle (830,420) -> knee (1220,480); heel (690,340) on the platform
css = """
.ff { position:absolute; inset:0; }
.ff img { width:1920px; height:1080px; display:block; }
.frz { position:absolute; left:40px; top:40px; padding:6px 14px; border-radius:6px; background:#d80609; color:#fff; font:800 20px Montserrat; letter-spacing:0.25em; }
svg { position:absolute; inset:0; }
"""
body = f"""
<div class="ff" id="fk"><img src="assets/freeze-knee.jpg" /><div class="frz">FREEZE</div>
  <svg width="1920" height="1080"><line id="kl" x1="830" y1="420" x2="1220" y2="480" stroke="#ff3b30" stroke-width="8" stroke-linecap="round" />
  <circle cx="830" cy="420" r="16" fill="none" stroke="#fff" stroke-width="5"/><circle cx="1220" cy="480" r="16" fill="none" stroke="#fff" stroke-width="5"/></svg></div>
<div class="ff" id="fh"><img src="assets/freeze-heel.jpg" /><div class="frz">FREEZE</div>
  <svg width="1920" height="1080"><defs><marker id="ah" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#ff3b30"/></marker></defs>
  <line id="hl" x1="880" y1="470" x2="712" y2="352" stroke="#ff3b30" stroke-width="9" stroke-linecap="round" marker-end="url(#ah)" />
  <circle cx="690" cy="340" r="22" fill="none" stroke="#fff" stroke-width="5"/></svg></div>
<div class="card" id="cA" style="left:72px; top:780px;"><div class="bar"></div><div class="ct"><div class="kick">CUE 1 · FOOT POSITION</div><div class="small">Foot <b>higher</b> on the platform —<br/>keep a straight line <b>knee → ankle</b></div></div></div>
<div class="card" id="cB" style="left:72px; top:800px;"><div class="bar"></div><div class="ct"><div class="kick">CUE 2</div><div class="small">Press through your <b>heel</b></div></div></div>
<div class="card" id="cC" style="left:72px; top:820px;"><div class="bar"></div><div class="ct"><div class="small">“You could go a little bit <b>higher</b> if you dare”</div></div></div>
"""
js = '  gsap.set(["#fk","#fh","#cA","#cB","#cC"], { opacity:0 });\n'
js += card_in("#cA", 15.0 - L0) + card_out("#cA", 24.9 - L0)
js += f'  tl.fromTo("#fk", {{ opacity:0 }}, {{ opacity:1, duration:f(0.1), immediateRender:false }}, f({16.2 - L0}));\n'
js += f'  tl.fromTo("#kl", {{ strokeDasharray:420, strokeDashoffset:420 }}, {{ strokeDashoffset:0, duration:f(0.5), ease:"power2.out", immediateRender:false }}, f({16.3 - L0}));\n'
js += f'  tl.to("#fk", {{ opacity:0, duration:f(0.2) }}, f({19.0 - L0}));\n'
js += card_in("#cB", 31.0 - L0) + card_out("#cB", 38.6 - L0)
js += f'  tl.fromTo("#fh", {{ opacity:0 }}, {{ opacity:1, duration:f(0.1), immediateRender:false }}, f({32.3 - L0}));\n'
js += f'  tl.fromTo("#hl", {{ strokeDasharray:220, strokeDashoffset:220 }}, {{ strokeDashoffset:0, duration:f(0.4), ease:"power2.out", immediateRender:false }}, f({32.4 - L0}));\n'
js += f'  tl.to("#fh", {{ opacity:0, duration:f(0.2) }}, f({35.0 - L0}));\n'
js += card_in("#cC", 47.0 - L0) + card_out("#cC", 49.0 - L0)
made.append(page("legpress-cues", 35.0, body, js, css))

# ---------- Leg press machine note (item 22, source 62.0 -> 81.0) ----------
body = """<div class="card" id="cD" style="left:72px; top:690px; max-width:820px;"><div class="bar"></div><div class="ct">
<div class="kick">ASH'S MACHINE NOTE</div>
<div class="small">This press moves in an <b>arc</b> — “it's always going to get a bit of <b>quad</b>”.<br/>For this setup, Ash prefers a <b>linear (sliding) leg press</b>.</div></div></div>"""
js = '  gsap.set("#cD", { opacity:0 });\n' + card_in("#cD", 0.3) + card_out("#cD", 18.6)
made.append(page("legpress-note", 19.0, body, js))

# ---------- Water skiddy caption ----------
body = '<div class="card" id="c" style="left:72px; top:830px;"><div class="bar"></div><div class="ct"><div class="kick">ASH DICTIONARY</div><div class="small"><b>Water skiddy</b> (n.) — a sweat patch</div></div></div>'
js = '  gsap.set("#c", { opacity:0 });\n' + card_in("#c", 0.2) + card_out("#c", 5.6)
made.append(page("cap-skiddy", 6.0, body, js))

json.dump(made, open("made.json", "w"))
print("\n".join(made))
