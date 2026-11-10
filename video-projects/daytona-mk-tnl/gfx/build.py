"""Daytona MK TNL — race-broadcast overlays (16:9 alpha), laid out at 1920x1080, rendered at SCALE x (2 = UHD).
Comps (times are timeline seconds = DJI source seconds; lights go green at GREEN):
  heat    — race title card (series / THE RACE / circuit / layout, drawn track outline + stats)
  track3d — camera flies one lap of the Cliff Drop layout in perspective, red trail draws behind, pulls out to overview
  grid    — HEAVYWEIGHT GRID: staggered two-column grid from qualifying (positions, kart numbers, best laps), Ash highlighted
HUD (position / CHIVERS / ASH / time remaining) is rendered separately by scripts/hud.mjs."""
import json, os, shutil, html
ROOT = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(ROOT)
WS = '/Users/ashleychivers/Documents/Claude Video Studio'
GSAP = WS + '/video-projects/training-day/gfx/assets/gsap.min.js'
HFJSON = WS + '/video-projects/training-day/gfx/hyperframes.json'
SCALE = int(os.environ.get('SCALE', 2))
W, H = 1920 * SCALE, 1080 * SCALE
RED = '#d80609'
E = html.escape
TRACK = json.load(open(PROJ + '/src/track.json'))['pts']

# qualifying (Sodi Qualifying screenshot, TNL Sodi Heavy) -> race grid
QUALI = [(1, 4, 'David Rollins', '1:17.651'), (2, 2, 'Micheal Bowles', '1:17.696'), (3, 7, 'Ash Chivers', '1:17.816'),
         (4, 6, 'Shaun Ward', '1:18.603'), (5, 3, 'Liam Jackson', '1:18.851'), (6, 34, 'Chris Lane', '1:18.936'),
         (7, 11, 'Jamie Brown', '1:19.048'), (8, 12, 'Kenny Eaton', '1:19.081'), (9, 13, 'Dan Watkins', '1:20.025'),
         (10, 22, 'Harrison W.', '1:20.629'), (11, 32, 'Mark Smith', '1:26.156')]
ASH = 3

HEAD = """<!doctype html><html lang="en"><head><meta charset="UTF-8" />
<meta name="viewport" content="width=%W%, height=%H%" /><script src="assets/gsap.min.js"></script>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:%W%px; height:%H%px; overflow:hidden; background:transparent; }
#stage { position:relative; width:%W%px; height:%H%px; overflow:hidden; }
#stage > #root { transform:scale(%S%); transform-origin:0 0; }
#root { position:relative; width:1920px; height:1080px; overflow:hidden; font-family:Montserrat, sans-serif; color:#f6f6f6; }
.mono { font-family:"JetBrains Mono", monospace; }
.wash { position:absolute; inset:0; opacity:0; background:radial-gradient(ellipse 80% 75% at 50% 50%, rgba(6,6,8,0.55) 0%, rgba(4,4,6,0.78) 100%); }
%CSS%
</style></head><body><div id="stage" data-composition-id="main" data-start="0" data-duration="%DUR%" data-width="%W%" data-height="%H%">
<div id="root">%BODY%</div></div>
<script>(() => { const tl = gsap.timeline({ paused:true });
%JS%
tl.to({}, { duration:%DUR% }, 0); window.__timelines = window.__timelines || {}; window.__timelines["main"] = tl; })();</script>
</body></html>"""

def write(name, dur, body, js, css):
    d = f'{ROOT}/comps/{name}'; os.makedirs(d + '/assets', exist_ok=True)
    open(f'{d}/index.html', 'w').write(HEAD.replace('%DUR%', f'{dur:.3f}').replace('%BODY%', body).replace('%JS%', js)
                                       .replace('%CSS%', css).replace('%W%', str(W)).replace('%H%', str(H)).replace('%S%', str(SCALE)))
    shutil.copy(HFJSON, d); shutil.copy(GSAP, d + '/assets/')
    open(f'{d}/meta.json', 'w').write(json.dumps({"id": name, "name": name, "width": W, "height": H, "fps": 25}))
    print('wrote', name)

def track_path(size, ox, oy):
    pts = [(ox + x * size, oy + y * size) for x, y in TRACK]
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + ' Z', pts

# ------------------------------------------------------------------ heat card
def heat():
    dur = 8.0
    d, pts = track_path(440, 1480, 300)
    sx, sy = pts[0]; nx, ny = pts[3]
    css = """
#card { position:absolute; left:96px; top:220px; width:1000px; opacity:0; border-radius:14px; overflow:hidden;
  background:linear-gradient(135deg, rgba(16,16,20,0.80), rgba(8,8,10,0.70)); border:1px solid rgba(255,255,255,0.13);
  box-shadow:0 24px 60px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.12); }
#card::before { content:""; position:absolute; left:0; top:0; bottom:0; width:8px; background:#d80609; }
#card .in { position:relative; padding:46px 40px 40px 58px; }
.kick { font-family:"JetBrains Mono"; font-weight:600; font-size:24px; letter-spacing:0.22em; color:rgba(255,255,255,0.72); }
.mask { overflow:hidden; }
.big { font-weight:900; font-size:150px; line-height:0.9; letter-spacing:-0.01em; margin-top:14px; font-style:italic; }
.big b { color:#d80609; }
.loc { font-weight:700; font-size:34px; letter-spacing:0.14em; margin-top:16px; }
.lay { font-family:"JetBrains Mono"; font-weight:600; font-size:26px; letter-spacing:0.18em; color:#d80609; margin-top:8px; }
.stats { display:flex; margin-top:30px; padding-top:22px; border-top:1px solid rgba(255,255,255,0.12); gap:40px; font-family:"JetBrains Mono"; font-size:20px; letter-spacing:0.14em; color:rgba(255,255,255,0.7); }
.stats b { display:block; font-family:Montserrat; font-weight:900; font-size:40px; letter-spacing:0.02em; color:#fff; line-height:1.05; margin-top:4px; }
#map { position:absolute; left:0; top:0; width:1920px; height:1080px; overflow:visible; }
#map .base { fill:none; stroke:rgba(255,255,255,0.22); stroke-width:13; stroke-linejoin:round; }
#map .line { fill:none; stroke:#fff; stroke-width:5; stroke-linejoin:round; stroke-linecap:round; filter:drop-shadow(0 0 6px rgba(255,255,255,0.55)); }
#map .sf { stroke:#ffd21f; stroke-width:5; stroke-linecap:round; }
#maplbl { position:absolute; left:1480px; top:540px; transform:translateX(-50%); font-family:"JetBrains Mono"; font-size:20px; letter-spacing:0.2em; color:rgba(255,255,255,0.75); white-space:nowrap; opacity:0; }
"""
    # start/finish tick perpendicular to direction of travel
    dx, dy = nx - sx, ny - sy; L = (dx * dx + dy * dy) ** 0.5; px, py = -dy / L * 16, dx / L * 16
    body = f"""<div class="wash" id="wash"></div>
<div id="card"><div class="in">
  <div class="kick" id="k">TNL · SODI HEAVY · 20 MIN RACE</div>
  <div class="mask"><div class="big" id="big">THE <b>RACE</b></div></div>
  <div class="loc" id="loc">DAYTONA MILTON KEYNES</div>
  <div class="lay" id="lay">CLIFF DROP LAYOUT</div>
  <div class="stats" id="stats"><div>GRID<b>11 KARTS</b></div><div>POLE<b>1:17.651</b></div><div>DIRECTION<b>ANTI-CLOCKWISE</b></div></div>
</div></div>
<svg id="map" viewBox="0 0 1920 1080"><path class="base" id="mb" d="{d}"/><path class="line" id="ml" d="{d}" pathLength="1000" stroke-dasharray="1000" stroke-dashoffset="1000"/>
<line class="sf" id="sf" x1="{sx - px:.1f}" y1="{sy - py:.1f}" x2="{sx + px:.1f}" y2="{sy + py:.1f}" opacity="0"/></svg>
<div id="maplbl">START / FINISH ▸ ANTI-CLOCKWISE</div>"""
    js = f"""
tl.to("#wash", {{ opacity:0.55, duration:0.5, ease:"power1.out" }}, 0.0);
tl.fromTo("#card", {{ opacity:0, x:-80 }}, {{ opacity:1, x:0, duration:0.55, ease:"expo.out", immediateRender:false }}, 0.15);
tl.from("#k", {{ opacity:0, x:-24, duration:0.4, ease:"power2.out" }}, 0.45);
tl.from("#big", {{ yPercent:105, duration:0.55, ease:"power4.out" }}, 0.5);
tl.from("#loc", {{ opacity:0, y:18, duration:0.45, ease:"back.out(1.6)" }}, 0.8);
tl.from("#lay", {{ opacity:0, x:-18, duration:0.4, ease:"power3.out" }}, 1.0);
tl.from("#stats > div", {{ opacity:0, y:16, duration:0.4, stagger:0.12, ease:"power2.out" }}, 1.2);
tl.from("#mb", {{ opacity:0, duration:0.5, ease:"none" }}, 0.6);
tl.to("#ml", {{ attr:{{ "stroke-dashoffset":0 }}, duration:2.4, ease:"power2.inOut" }}, 0.8);
tl.to("#sf", {{ opacity:1, duration:0.2 }}, 0.8);
tl.to("#maplbl", {{ opacity:1, duration:0.4 }}, 2.6);
tl.to("#map, #maplbl", {{ scale:1.03, duration:4.0, ease:"none", transformOrigin:"1480px 300px" }}, 3.2);
tl.to("#card", {{ opacity:0, x:-60, duration:0.45, ease:"power2.in" }}, {dur - 0.6});
tl.to("#map, #maplbl", {{ opacity:0, duration:0.45, ease:"power1.in" }}, {dur - 0.6});
tl.to("#wash", {{ opacity:0, duration:0.5, ease:"power1.in" }}, {dur - 0.5});
"""
    write('heat', dur, body, js, css)

# ------------------------------------------------------------------ 3D track flythrough
def track3d():
    dur = 16.0
    S = 5200  # world size of the track (px)
    d, pts = track_path(S, S / 2, S / 2)
    css = f"""
#persp {{ position:absolute; inset:0; perspective:1100px; perspective-origin:960px 300px; }}
#world {{ position:absolute; left:0; top:0; width:{S}px; height:{S}px; transform-origin:0 0; opacity:0; }}
#world svg {{ position:absolute; left:0; top:0; width:{S}px; height:{S}px; overflow:visible; }}
.edge {{ fill:none; stroke:rgba(255,255,255,0.88); stroke-width:26; stroke-linejoin:round; }}
.core {{ fill:none; stroke:rgba(10,10,12,0.9); stroke-width:16; stroke-linejoin:round; }}
.trail {{ fill:none; stroke:#ff1d22; stroke-width:18; stroke-linejoin:round; stroke-linecap:round; filter:drop-shadow(0 0 30px rgba(255,20,30,0.95)); }}
.sf {{ stroke:#ffd21f; stroke-width:10; stroke-linecap:round; }}
#dot {{ fill:#fff; filter:drop-shadow(0 0 16px #fff); }}
#lbl {{ position:absolute; left:0; right:0; top:92px; text-align:center; opacity:0; }}
#lbl .k {{ font-family:"JetBrains Mono"; font-weight:600; font-size:24px; letter-spacing:0.3em; color:rgba(255,255,255,0.75); }}
#lbl .t {{ font-weight:900; font-style:italic; font-size:84px; line-height:1; margin-top:10px; }}
#lbl .t b {{ color:#d80609; }}
#lap {{ position:absolute; right:110px; bottom:96px; text-align:right; opacity:0; font-family:"JetBrains Mono"; font-size:22px; letter-spacing:0.22em; color:rgba(255,255,255,0.7); }}
#lap b {{ display:block; font-family:Montserrat; font-weight:900; font-size:64px; letter-spacing:0.02em; color:#fff; line-height:1; margin-top:6px; }}
"""
    sx, sy = pts[0]; nx, ny = pts[3]
    dx, dy = nx - sx, ny - sy; L = (dx * dx + dy * dy) ** 0.5; px, py = -dy / L * 46, dx / L * 46
    body = f"""<div class="wash" id="wash"></div>
<div id="persp"><div id="world"><svg viewBox="0 0 {S} {S}">
<path class="edge" d="{d}"/><path class="core" d="{d}"/>
<path class="trail" id="trail" d="{d}" pathLength="1000" stroke-dasharray="1000 1000" stroke-dashoffset="1000"/>
<line class="sf" x1="{sx - px:.1f}" y1="{sy - py:.1f}" x2="{sx + px:.1f}" y2="{sy + py:.1f}"/>
<circle id="dot" r="38" cx="{sx:.1f}" cy="{sy:.1f}"/></svg></div></div>
<div id="lbl"><div class="k">DAYTONA MILTON KEYNES</div><div class="t">CLIFF DROP <b>LAYOUT</b></div></div>
<div id="lap">POLE LAP<b>1:17.651</b></div>"""
    js = """
const P = %PTS%, S = %S%, N = P.length;
const pt = s => { const f = ((s % 1) + 1) % 1 * N, i = Math.floor(f), a = P[i], b = P[(i + 1) %% N], u = f - i;
  return [(a[0] + (b[0] - a[0]) * u + 0.5) * S, (a[1] + (b[1] - a[1]) * u + 0.5) * S]; };
// smoothed heading: look 1.6%% ahead and behind
const hd = s => { const a = pt(s - 0.008), b = pt(s + 0.016); return Math.atan2(b[1] - a[1], b[0] - a[0]); };
const H0 = hd(0) * 180 / Math.PI + 90;                 // heading at the start line (travel pointing up the screen)
const RF = Math.round(-H0 / 360) * 360;                 // north-up = same orientation as the lap-timer map
// camera: z scale, tilt, f = follow the dot (0 = track centre), rot = world rotation
const cam = { s:0, z:1.25, tilt:64, f:1, rot:-H0 };
function render() {
  const [x, y] = pt(cam.s), C = S / 2, f = cam.f;
  const cx = C + (x - C) * f, cy = C + (y - C) * f;
  const ty = 540 + 330 * f;
  document.getElementById("world").style.transform =
    `translate(960px, ${ty}px) rotateX(${cam.tilt}deg) scale(${cam.z}) rotate(${cam.rot}deg) translate(${-cx}px, ${-cy}px)`;
  const dot = document.getElementById("dot"); dot.setAttribute("cx", x.toFixed(1)); dot.setAttribute("cy", y.toFixed(1));
  document.getElementById("trail").setAttribute("stroke-dashoffset", (1000 - cam.s * 1000).toFixed(2));
}
render();
tl.to("#wash", { opacity:1, duration:0.5, ease:"power1.out" }, 0.0);
tl.to("#world", { opacity:1, duration:0.5, ease:"power1.out" }, 0.1);
// comes in big on the start line, then pulls back and settles centred with the whole track in view
tl.to(cam, { z:0.245, tilt:46, f:0, rot:RF - 42, duration:2.8, ease:"power3.inOut", onUpdate:render }, 0.5);
tl.to(cam, { rot:RF - 12, duration:8.4, ease:"sine.inOut", onUpdate:render }, 3.3);   // slow orbit while the lap runs
tl.to(cam, { s:1, duration:10.0, ease:"sine.inOut", onUpdate:render }, 1.2);
tl.fromTo("#lbl", { opacity:0, y:-20 }, { opacity:1, y:0, duration:0.5, ease:"power3.out", immediateRender:false }, 2.4);
// finish: flatten to the top-down map
tl.to(cam, { tilt:0, z:0.21, rot:RF, duration:1.5, ease:"power3.inOut", onUpdate:render }, 11.7);
tl.fromTo("#lap", { opacity:0, x:30 }, { opacity:1, x:0, duration:0.45, ease:"back.out(1.6)", immediateRender:false }, 13.2);
tl.to("#world, #lbl, #lap", { opacity:0, duration:0.5, ease:"power1.in" }, %END%);
tl.to("#wash", { opacity:0, duration:0.5, ease:"power1.in" }, %END2%);
""".replace('%PTS%', json.dumps(TRACK)).replace('%S%', str(S)).replace('%%', '%').replace('%END%', str(dur - 0.7)).replace('%END2%', str(dur - 0.55))
    write('track3d', dur, body, js, css)

# ------------------------------------------------------------------ grid
def grid():
    dur = 24.0
    ROWH = 190
    css = """
#title { position:absolute; left:0; top:300px; width:1920px; display:flex; flex-direction:column; align-items:center; opacity:0; }
#title .k { font-family:"JetBrains Mono"; font-weight:700; font-size:34px; letter-spacing:0.32em; color:#fff; background:#d80609; padding:10px 22px 9px 30px; }
#title .t { font-weight:900; font-style:italic; font-size:156px; line-height:1; margin-top:22px; letter-spacing:-0.01em; text-shadow:0 8px 40px rgba(0,0,0,0.6); }
#title .t b { color:#d80609; }
#title .bar { width:1280px; height:6px; margin-top:18px; background:linear-gradient(90deg, transparent, #d80609 20%, #d80609 80%, transparent); transform-origin:50% 50%; }
#title .s { font-family:"JetBrains Mono"; font-weight:600; font-size:36px; letter-spacing:0.5em; color:rgba(255,255,255,0.85); margin-top:22px; padding-left:18px; }
#list { position:absolute; left:0; top:0; width:1920px; }
.row { position:absolute; width:850px; height:200px; border-radius:6px; overflow:hidden;
  background:linear-gradient(90deg, rgba(20,20,24,0.86), rgba(12,12,14,0.78)); border:2px solid rgba(255,255,255,0.12); }
.row .ghost { position:absolute; top:-46px; font-weight:900; font-style:italic; font-size:270px; line-height:1; color:rgba(255,255,255,0.06); }
.row .num { position:absolute; top:0; bottom:0; width:160px; display:flex; align-items:center; justify-content:center;
  background:#d9d4c7; color:#141414; font-weight:900; font-size:84px; letter-spacing:-0.02em; }
.row .nm { position:absolute; top:40px; font-weight:800; font-size:62px; line-height:1.1; white-space:nowrap; }
.row .sub { position:absolute; top:118px; font-family:"JetBrains Mono"; font-size:34px; letter-spacing:0.06em; color:rgba(255,255,255,0.55); white-space:nowrap; }
.row .sub i { font-style:normal; color:rgba(255,255,255,0.9); }
.row .sub i.p { color:#d43cf0; }
.L .num { right:0; padding-left:0; clip-path:polygon(0 0, 82% 0, 100% 50%, 82% 100%, 0 100%); justify-content:flex-start; padding-left:26px; }
.L .nm, .L .sub { right:196px; text-align:right; } .L .ghost { left:30px; }
.R .num { left:0; clip-path:polygon(18% 0, 100% 0, 100% 100%, 18% 100%, 0 50%); justify-content:flex-end; padding-right:26px; }
.R .nm, .R .sub { left:196px; } .R .ghost { right:30px; }
.row.me { border:3px solid #d80609; box-shadow:0 0 40px rgba(216,6,9,0.55), inset 0 0 0 1px rgba(216,6,9,0.6); background:linear-gradient(90deg, rgba(40,6,8,0.92), rgba(18,8,9,0.86)); }
.row.me .num { background:#fff; color:#d80609; }
.row.me .ghost { color:rgba(216,6,9,0.2); }
#youtag { position:absolute; font-family:"JetBrains Mono"; font-weight:700; font-size:28px; letter-spacing:0.24em; color:#fff; background:#d80609; padding:7px 14px 6px; opacity:0; }
"""
    rows = []; js_rows = []
    for pos, kart, name, best in QUALI:
        right = pos % 2 == 0                      # pole on the left, staggered like the real grid
        x = 1020 if right else 50
        y = 120 + (pos - 1) * ROWH                # each grid slot a bit further back
        cls = ('R' if right else 'L') + (' me' if pos == ASH else '')
        tcls = ' class="p"' if pos == 1 else ''
        rows.append(f'<div class="row {cls}" id="g{pos}" style="left:{x}px; top:{y}px"><div class="ghost">{pos}</div>'
                    f'<div class="num">{pos}</div><div class="nm">{E(name)}</div><div class="sub">#{kart} · <i{tcls}>{best}</i></div></div>')
    me_right = ASH % 2 == 0
    me_x, me_y = (1020 if me_right else 50), 120 + (ASH - 1) * ROWH
    tag = f'<div id="youtag" style="left:{me_x + (850 - 110 if me_right else 24)}px; top:{me_y - 18}px; z-index:2">ASH</div>'
    body = f"""<div class="wash" id="wash"></div>
<div id="title"><div class="k">SET BY QUALIFYING</div><div class="t">HEAVYWEIGHT <b>GRID</b></div><div class="bar"></div><div class="s">STARTING ORDER</div></div>
<div id="list">{''.join(rows)}{tag}</div>"""
    # camera starts at the back of the grid with P11 at the TOP of the frame, then the list rolls DOWN the screen
    # (each row enters from the top edge) until the front row sits at the top
    y0 = -(ROWH * 10)                             # P11 row at y=120
    y1 = 20                                       # P1 row at y=140
    S0, SD = 3.7, 10.5
    js = f"""
tl.to("#wash", {{ opacity:1, duration:0.6, ease:"power1.out" }}, 0.0);
tl.fromTo("#title", {{ opacity:0, scale:1.08 }}, {{ opacity:1, scale:1, duration:0.6, ease:"expo.out", immediateRender:false }}, 0.3);
tl.from("#title .k", {{ opacity:0, y:-30, duration:0.5, ease:"back.out(2)" }}, 0.35);
tl.fromTo("#title .bar", {{ scaleX:0 }}, {{ scaleX:1, duration:0.7, ease:"power3.inOut" }}, 0.6);
tl.from("#title .s", {{ opacity:0, y:24, duration:0.6, ease:"power3.out" }}, 0.9);
tl.to("#title", {{ opacity:0, y:-120, duration:0.5, ease:"power2.in" }}, 3.3);
tl.set("#list", {{ y:{y0} }}, 0);
tl.to("#list", {{ y:{y1}, duration:{SD}, ease:"sine.inOut" }}, {S0});
"""
    # each row slides in as it comes over the top edge (sine.inOut list motion inverted numerically)
    import math
    def list_y(t):
        u = min(1, max(0, (t - S0) / SD)); e = -(math.cos(math.pi * u) - 1) / 2
        return y0 + (y1 - y0) * e
    for pos, *_ in reversed(QUALI):
        right = pos % 2 == 0
        top = 120 + (pos - 1) * ROWH
        t = 3.6 if top + y0 > -40 else next(k / 100 for k in range(0, 3000) if top + list_y(k / 100) > -60) - 0.25
        js += f'tl.fromTo("#g{pos}", {{ opacity:0, x:{80 if right else -80}, y:-40 }}, {{ opacity:1, x:0, y:0, duration:0.5, ease:"expo.out", immediateRender:true }}, {max(3.6, t):.2f});\n'
    js += f"""
tl.fromTo("#youtag", {{ opacity:0, scale:0.6 }}, {{ opacity:1, scale:1, duration:0.35, ease:"back.out(2.2)", immediateRender:false }}, 13.1);
tl.to("#g{ASH}", {{ scale:1.05, duration:0.35, ease:"power2.out" }}, 14.3);
tl.to("#g{ASH}", {{ scale:1.0, duration:0.6, ease:"power2.inOut" }}, 14.65);
tl.to("#g{ASH}", {{ boxShadow:"0 0 54px rgba(216,6,9,0.85), inset 0 0 0 1px rgba(216,6,9,0.6)", duration:1.2, yoyo:true, repeat:2, ease:"sine.inOut" }}, 15.3);
tl.to("#list", {{ y:40, duration:7.3, ease:"none" }}, 14.2);
tl.to("#list", {{ opacity:0, duration:0.5, ease:"power1.in" }}, {dur - 0.7});
tl.to("#wash", {{ opacity:0, duration:0.55, ease:"power1.in" }}, {dur - 0.6});
"""
    write('grid', dur, body, js, css)

# ------------------------------------------------------------------ HUD (position / name / time remaining)
def hud():
    """Top-right box, aligned with the lap-timer box (top 63px, right margin 93px in 1080 space).
    Rendered as its own small canvas (HW x HH layout px); composited at x=1920-93-HW, y=63."""
    R = json.load(open(PROJ + '/src/race.json'))
    t0 = R['hud_in']; dur = round(R['end'] - t0, 2); g = R['green'] - t0; secs = R['race_secs']
    HW, HH = 640, 200
    fin = R['final_lap'] - t0
    css = """
html, body, #stage { width:%HW%px; height:%HH%px; }
#root { width:640px; height:200px; }
#box { position:absolute; left:0; top:0; width:640px; height:143px; border-radius:6px; overflow:hidden;
  background:linear-gradient(180deg, rgba(22,22,26,0.92), rgba(12,12,14,0.92)); box-shadow:0 10px 30px rgba(0,0,0,0.45); }
#chip { position:absolute; left:0; top:0; width:176px; height:92px; background:#d80609;
  clip-path:polygon(0 0, 100% 0, 100% 100%, 22px 100%, 0 calc(100% - 22px)); }
#chip span { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-weight:900; font-style:italic;
  font-size:70px; letter-spacing:-0.02em; color:#fff; padding-right:6px; }
#nm { position:absolute; right:30px; top:8px; font-weight:900; font-style:italic; font-size:54px; letter-spacing:0.01em; line-height:1.1; }
#sub { position:absolute; right:32px; top:63px; font-family:"JetBrains Mono"; font-weight:600; font-size:20px; letter-spacing:0.32em; color:rgba(255,255,255,0.62); }
#rule { position:absolute; left:20px; right:20px; top:96px; height:1px; background:rgba(255,255,255,0.12); }
#bot { position:absolute; left:0; right:0; top:97px; height:46px; display:flex; align-items:center; justify-content:center; gap:22px; }
#lbl { font-family:"JetBrains Mono"; font-weight:600; font-size:20px; letter-spacing:0.28em; color:rgba(255,255,255,0.62); }
#clk { font-weight:900; font-size:36px; letter-spacing:0.02em; font-variant-numeric:tabular-nums; min-width:112px; }
#fin { position:absolute; left:0; right:0; top:97px; height:46px; display:flex; align-items:center; justify-content:center; gap:16px; opacity:0;
  font-weight:900; font-style:italic; font-size:34px; letter-spacing:0.06em; color:#fff; background:#d80609; }
.chq { width:34px; height:24px; background:conic-gradient(#fff 25%, #111 0 50%, #fff 0 75%, #111 0) 0 0/12px 12px; border:1px solid rgba(255,255,255,0.6); }
#glow { position:absolute; left:0; right:0; top:141px; height:3px; background:#d80609; box-shadow:0 0 14px rgba(216,6,9,0.9); }
#chip.c1 { background:linear-gradient(135deg, #fff1a8 0%, #f2c230 35%, #b8860b 70%, #ffe066 100%); }
#chip.c2 { background:linear-gradient(135deg, #ffffff 0%, #d4d8dd 35%, #8e959c 70%, #e9ecef 100%); }
#chip.c3 { background:linear-gradient(135deg, #ffcf9e 0%, #d08a45 35%, #8a4b17 70%, #e0a46a 100%); }
#chip.c1 span, #chip.c2 span { color:#141414; }
#chip.c3 span { color:#fff; text-shadow:0 2px 6px rgba(0,0,0,0.35); }
#yf { position:absolute; left:0; top:150px; width:640px; height:46px; border-radius:6px; overflow:hidden; opacity:0;
  background:#ffd400; color:#111; display:flex; align-items:center; justify-content:center; gap:16px;
  font-weight:900; font-style:italic; font-size:32px; letter-spacing:0.08em; box-shadow:0 8px 24px rgba(0,0,0,0.4); }
#yf .fl { width:30px; height:22px; background:#111; clip-path:polygon(0 0, 100% 20%, 100% 80%, 0 100%); position:relative; }
#yf .fl::after { content:""; position:absolute; inset:3px 4px 3px 2px; background:#ffd400; clip-path:polygon(0 0, 100% 20%, 100% 80%, 0 100%); }
""".replace('%HW%', str(HW * SCALE)).replace('%HH%', str(HH * SCALE))
    body = """<div id="box"><div id="chip" class="c%P0%"><span id="pos">P%P0%</span></div>
<div id="nm">CHIVERS</div><div id="sub">ASH</div><div id="rule"></div>
<div id="bot"><span id="lbl">TIME REMAINING</span><span id="clk">20:00</span></div>
<div id="fin"><i class="chq"></i>FINAL LAP<i class="chq"></i></div><div id="glow"></div></div>
<div id="yf"><i class="fl"></i>YELLOW FLAG<i class="fl"></i></div>""".replace('%P0%', str(R['positions'][0][1]))
    js = f"""
const clk = {{ r:{secs} }}, el = document.getElementById("clk");
const fmt = r => {{ const c = Math.max(0, Math.ceil(r - 1e-6)); return Math.floor(c / 60) + ":" + String(c % 60).padStart(2, "0"); }};
const draw = () => {{ el.textContent = fmt(clk.r); }}; draw();
tl.fromTo("#box", {{ opacity:0, x:60 }}, {{ opacity:1, x:0, duration:0.5, ease:"expo.out", immediateRender:true }}, 0.2);
tl.from("#chip", {{ xPercent:-100, duration:0.45, ease:"power3.out" }}, 0.45);
tl.from("#nm", {{ opacity:0, x:24, duration:0.4, ease:"power2.out" }}, 0.55);
tl.from("#sub", {{ opacity:0, duration:0.4, ease:"none" }}, 0.7);
tl.from("#bot", {{ opacity:0, y:10, duration:0.4, ease:"back.out(1.6)" }}, 0.8);
tl.from("#glow", {{ scaleX:0, transformOrigin:"0 50%", duration:0.6, ease:"power2.inOut" }}, 0.6);
tl.to(clk, {{ r:0, duration:{secs}, ease:"none", onUpdate:draw }}, {g:.3f});
tl.fromTo("#glow", {{ opacity:0.3 }}, {{ opacity:1, duration:0.25, yoyo:true, repeat:3, ease:"sine.inOut", immediateRender:false }}, {g:.3f});
tl.set("#bot", {{ opacity:0 }}, {fin:.3f});
tl.fromTo("#fin", {{ opacity:0, scaleY:0.2 }}, {{ opacity:1, scaleY:1, duration:0.3, ease:"back.out(2)", immediateRender:false }}, {fin:.3f});
tl.fromTo("#fin", {{ backgroundColor:"#d80609" }}, {{ backgroundColor:"#ff3b3e", duration:0.5, yoyo:true, repeat:5, ease:"sine.inOut", immediateRender:false }}, {fin + 0.3:.3f});
"""
    for t, p in R['positions'][1:]:
        lt = t - t0
        # P1 gold, P2 silver, P3 bronze, anything else brand red; chip flips and flashes white on each change
        js += (f'tl.to("#chip", {{ scaleY:0, duration:0.12, ease:"power2.in", transformOrigin:"50% 50%" }}, {lt:.3f});'
               f'tl.set("#pos", {{ textContent:"P{p}" }}, {lt + 0.12:.3f});'
               f'tl.set("#chip", {{ attr:{{ class:"c{p}" }} }}, {lt + 0.12:.3f});'
               f'tl.to("#chip", {{ scaleY:1, duration:0.22, ease:"back.out(2.4)" }}, {lt + 0.12:.3f});'
               f'tl.fromTo("#chip", {{ filter:"brightness(2.2)" }}, {{ filter:"brightness(1)", duration:0.6, ease:"power2.out", immediateRender:false }}, {lt + 0.12:.3f});\n')
    for a, b in R['yellow']:
        js += (f'tl.fromTo("#yf", {{ opacity:0, y:-14 }}, {{ opacity:1, y:0, duration:0.3, ease:"back.out(2)", immediateRender:false }}, {a - t0:.3f});'
               f'tl.fromTo("#yf", {{ backgroundColor:"#ffd400" }}, {{ backgroundColor:"#ffef7a", duration:0.4, yoyo:true, repeat:{int((b - a) / 0.4) // 2 * 2 - 1}, ease:"sine.inOut", immediateRender:false }}, {a - t0 + 0.3:.3f});'
               f'tl.to("#yf", {{ opacity:0, y:-10, duration:0.3, ease:"power2.in" }}, {b - t0:.3f});\n')
    page = (HEAD.replace('%DUR%', f'{dur:.3f}').replace('%BODY%', body).replace('%JS%', js).replace('%CSS%', css)
            .replace('%W%', str(HW * SCALE)).replace('%H%', str(HH * SCALE)).replace('%S%', str(SCALE)))
    d = f'{ROOT}/comps/hud'; os.makedirs(d + '/assets', exist_ok=True)
    open(f'{d}/index.html', 'w').write(page)
    shutil.copy(HFJSON, d); shutil.copy(GSAP, d + '/assets/')
    open(f'{d}/meta.json', 'w').write(json.dumps({"id": "hud", "name": "hud", "width": HW * SCALE, "height": HH * SCALE, "fps": 25}))
    print('wrote hud', dur, 's')

# ------------------------------------------------------------------ red smoke frame border (seamless loop)
def smoke():
    """Wispy red smoke glow around the frame edge (like the reference's edge glow, in brand red).
    6 s seamless loop (every animated value yoyos back to its start); composite.py loops it for the whole video."""
    dur = 6.0
    css = """
#sm { position:absolute; left:0; top:0; width:1920px; height:1080px; }
"""
    body = """<svg id="sm" viewBox="0 0 1920 1080">
<defs>
  <filter id="f" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">
    <feTurbulence id="tb" type="fractalNoise" baseFrequency="0.0065 0.009" numOctaves="4" seed="11" result="n"/>
    <feDisplacementMap id="dm" in="SourceGraphic" in2="n" scale="150" xChannelSelector="R" yChannelSelector="G" result="d"/>
    <feGaussianBlur in="d" stdDeviation="16" result="b"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 2.6 -0.75" result="wisp"/>
    <feComposite in="b" in2="wisp" operator="in" result="bw"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="bw"/></feMerge>
  </filter>
  <radialGradient id="g" cx="50%" cy="50%" r="72%">
    <stop offset="0.74" stop-color="#ff1a10" stop-opacity="0"/>
    <stop offset="0.9" stop-color="#e00808" stop-opacity="0.5"/>
    <stop offset="1" stop-color="#b80000" stop-opacity="0.85"/>
  </radialGradient>
</defs>
<g filter="url(#f)" id="glow">
  <rect x="-60" y="-60" width="2040" height="1200" fill="url(#g)"/>
  <rect x="-40" y="-40" width="2000" height="1160" fill="none" stroke="#ff2014" stroke-width="54" opacity="0.85"/>
</g></svg>"""
    js = """
tl.fromTo("#dm", { attr:{ scale:95 } }, { attr:{ scale:135 }, duration:3, yoyo:true, repeat:1, ease:"sine.inOut", immediateRender:true }, 0);
tl.fromTo("#tb", { attr:{ baseFrequency:"0.0065 0.009" } }, { attr:{ baseFrequency:"0.0072 0.0098" }, duration:3, yoyo:true, repeat:1, ease:"sine.inOut", immediateRender:true }, 0);
tl.fromTo("#glow", { opacity:0.85 }, { opacity:1, duration:1.5, yoyo:true, repeat:3, ease:"sine.inOut", immediateRender:true }, 0);
"""
    write('smoke', dur, body, js, css)

# ------------------------------------------------------------------ start lights (top centre)
def lights():
    """Three red lights pop on 3.1 s before the green, beeps at -3/-2/-1 s (audio added in composite.py),
    all three switch to green on the start, hold, then fade. Comp starts at LIGHTS_T0 timeline seconds."""
    R = json.load(open(PROJ + '/src/race.json'))
    g = R['green'] - R['lights_in']; dur = g + 1.6
    css = """
#lt { position:absolute; left:839px; top:34px; width:242px; display:flex; gap:16px; padding:12px 18px; border-radius:40px;
  background:rgba(8,8,10,0.55); box-shadow:0 6px 22px rgba(0,0,0,0.45); opacity:0; }
.l { position:relative; width:54px; height:54px; border-radius:50%; border:3px solid #1a0000;
  background:radial-gradient(circle at 38% 32%, #ff8a80 0%, #ff1a10 32%, #c40000 70%, #7a0000 100%);
  box-shadow:0 0 18px rgba(255,20,10,0.85), inset 0 -4px 8px rgba(0,0,0,0.35); }
.l.g { position:absolute; left:0; top:0; border-color:#002a08; opacity:0;
  background:radial-gradient(circle at 38% 32%, #b9ffbf 0%, #2bff4a 32%, #00c22a 70%, #006a14 100%);
  box-shadow:0 0 22px rgba(40,255,80,0.9), inset 0 -4px 8px rgba(0,0,0,0.3); }
.cell { position:relative; width:54px; height:54px; }
"""
    body = '<div id="lt">' + ''.join(f'<div class="cell"><div class="l r" id="r{i}"></div><div class="l g" id="g{i}"></div></div>' for i in range(3)) + '</div>'
    js = f"""
tl.fromTo("#lt", {{ opacity:0, y:-30 }}, {{ opacity:1, y:0, duration:0.3, ease:"back.out(1.8)", immediateRender:true }}, 0.05);
tl.from(".r", {{ scale:0.4, duration:0.25, stagger:0.06, ease:"back.out(2.2)" }}, 0.1);
tl.to(".g", {{ opacity:1, duration:0.06, ease:"none" }}, {g:.3f});
tl.fromTo(".g", {{ scale:1.18 }}, {{ scale:1, duration:0.3, ease:"power2.out", immediateRender:false }}, {g:.3f});
tl.to("#lt", {{ opacity:0, y:-20, duration:0.35, ease:"power2.in" }}, {dur - 0.4:.3f});
"""
    write('lights', dur, body, js, css)

if __name__ == "__main__":
    heat(); track3d(); grid(); hud(); lights()
