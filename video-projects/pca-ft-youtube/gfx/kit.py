"""Shared graphics kit (Team Apexx look) for the PCA FT YouTube edit. build.py = posing + training graphics, show.py = show-day section.
Team Apexx look (same kit as npc-italy/gfx/build.py): Bebas Neue display, Montserrat text, red #d80609, soft dark backing.
Comps render at 24 fps with times divided by 1.001, then are conformed to 23.976 so they line up with the timeline.
Timeline anchors: posing section = intro seconds (Ash's edit minus the cuts in intro.json); training = edl.json pieces (src seconds -> timeline)."""
import json, os, shutil, html, sys
ROOT = os.path.dirname(os.path.abspath(__file__)); PRJ = ROOT + '/..'
WS = '/Users/ashleychivers/Documents/Claude Video Studio'
GSAP = WS + '/video-projects/training-day/gfx/assets/gsap.min.js'
HFJSON = WS + '/video-projects/training-day/gfx/hyperframes.json'
FPS = 24000 / 1001; K = 1 / 1.001
SCALE = int(os.environ.get('SCALE', '2')); W, H = 1920 * SCALE, 1080 * SCALE
EDL = json.load(open(PRJ + '/edl.json'))
E = lambda s: html.escape(s)

HEAD = """<!doctype html><html lang="en"><head><meta charset="UTF-8" />
<meta name="viewport" content="width=%W%, height=%H%" /><script src="assets/gsap.min.js"></script>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:%W%px; height:%H%px; overflow:hidden; background:transparent; }
#stage { position:relative; width:%W%px; height:%H%px; overflow:hidden; }
#stage > #root { transform:scale(%S%); transform-origin:0 0; }
#root { position:relative; width:1920px; height:1080px; overflow:hidden; font-family:Montserrat, sans-serif; color:#f6f6f6; }
.sh { text-shadow:0 3px 18px rgba(0,0,0,0.75), 0 1px 3px rgba(0,0,0,0.7); }
.back { position:absolute; left:-200px; bottom:-220px; width:1500px; height:760px;
  background:radial-gradient(ellipse 55% 50% at 30% 62%, rgba(0,0,0,0.62), rgba(0,0,0,0) 70%); }
.k { font-weight:800; font-size:22px; letter-spacing:0.3em; color:rgba(255,255,255,0.88); display:flex; align-items:center; gap:16px; }
.k i { display:inline-block; width:40px; height:4px; background:#d80609; }
.t { font-family:"Bebas Neue", sans-serif; line-height:0.9; letter-spacing:0.01em; white-space:nowrap; }
.s { font-weight:600; font-size:27px; color:#d6d6d6; letter-spacing:0.02em; }
.clip { overflow:hidden; padding-bottom:6px; }
.card { position:absolute; background:rgba(12,12,14,0.78); border-left:6px solid #d80609; padding:22px 30px 24px;
  box-shadow:0 18px 50px rgba(0,0,0,0.45); }
%CSS%
</style></head><body>
<div id="stage" data-composition-id="main" data-start="0" data-duration="%DUR%" data-width="%W%" data-height="%H%"><div id="root">%BODY%</div></div>
<script>(() => { const tl = gsap.timeline({ paused:true }); const K = %K%;
%JS%
tl.to({}, { duration:%DUR% }, 0); window.__timelines = window.__timelines || {}; window.__timelines["main"] = tl; })();</script>
</body></html>"""

made = []
def page(name, t0, dur, body, js, css=''):
    """t0 = timeline seconds (from timeline start) where the graphic begins"""
    d = f'{ROOT}/comps/{name}'; os.makedirs(d + '/assets', exist_ok=True)
    open(f'{d}/index.html', 'w').write(HEAD.replace('%DUR%', f'{dur * K:.3f}').replace('%BODY%', body)
                                     .replace('%JS%', js).replace('%CSS%', css).replace('%K%', f'{K:.6f}')
                                     .replace('%W%', str(W)).replace('%H%', str(H)).replace('%S%', str(SCALE)))
    shutil.copy(HFJSON, d); shutil.copy(GSAP, d + '/assets/')
    open(f'{d}/meta.json', 'w').write(json.dumps({"id": name, "name": name, "width": W, "height": H, "fps": 24}))
    made.append(dict(name=name, rec=round(t0 * FPS), frames=round(dur * FPS)))

def tr(clip, src):
    """training: source second in clip -> timeline seconds"""
    for p in EDL:
        if p['clip'] == clip and p['src_start'] <= src * FPS < p['src_end']:
            return (p['rec'] + src * FPS - p['src_start']) / FPS
    raise ValueError((clip, src))
def ex_start(i): return [p for p in EDL if p['ex'] == i][0]['rec'] / FPS
def piece_end(clip, src):
    for p in EDL:
        if p['clip'] == clip and p['src_start'] <= src * FPS < p['src_end']: return (p['rec'] + p['dur']) / FPS

# ------------------------------------------------------------------ building blocks
def lt_js(r, hold):
    return f"""gsap.set(["{r} .back", "{r} .k", "{r} .t", "{r} .s", "{r} .x"], {{ opacity:0 }});
tl.to("{r} .back", {{ opacity:1, duration:0.5*K }}, 0);
tl.fromTo("{r} .k", {{ opacity:0, x:-30 }}, {{ opacity:1, x:0, duration:0.45*K, ease:"power3.out", immediateRender:false }}, 0.1*K);
tl.fromTo("{r} .t", {{ opacity:0, yPercent:105 }}, {{ opacity:1, yPercent:0, duration:0.6*K, ease:"expo.out", immediateRender:false }}, 0.2*K);
tl.fromTo("{r} .s, {r} .x", {{ opacity:0, y:14 }}, {{ opacity:1, y:0, duration:0.5*K, ease:"power2.out", stagger:0.08*K, immediateRender:false }}, 0.5*K);
tl.to(["{r} .k", "{r} .t", "{r} .s", "{r} .x"], {{ opacity:0, x:-24, duration:0.4*K, ease:"power2.in", stagger:0.04*K }}, {hold - 0.45:.3f}*K);
tl.to("{r} .back", {{ opacity:0, duration:0.5*K }}, {hold - 0.35:.3f}*K);"""

def lower_third(name, t0, kicker, title, sub=None, dur=5.5, size=96):
    body = (f'<div class="back"></div><div id="L" class="sh" style="position:absolute; left:80px; bottom:96px;">'
            f'<div class="k"><i></i>{E(kicker)}</div>'
            f'<div class="clip"><div class="t" style="font-size:{size}px; margin-top:10px;">{E(title)}</div></div>'
            + (f'<div class="s" style="margin-top:8px;">{E(sub)}</div>' if sub else '') + '</div>')
    page(name, t0, dur, body, lt_js('#L', dur))

def top_tag(name, t0, kicker, title, dur=4.0, right=False):
    side = 'right:64px; text-align:right;' if right else 'left:64px;'
    css = f"""#T {{ position:absolute; {side} top:56px; }}
#T .pill {{ display:inline-block; background:#d80609; font-weight:800; font-size:19px; letter-spacing:0.26em; padding:7px 14px 6px; }}
#T .t {{ font-size:66px; margin-top:10px; }}"""
    body = f'<div id="T" class="sh"><div class="pill">{E(kicker)}</div><div class="clip"><div class="t">{E(title)}</div></div></div>'
    js = f"""gsap.set(["#T .pill","#T .t"], {{ opacity:0 }});
tl.fromTo("#T .pill", {{ opacity:0, x:{24 if right else -24} }}, {{ opacity:1, x:0, duration:0.4*K, ease:"power3.out", immediateRender:false }}, 0.05*K);
tl.fromTo("#T .t", {{ opacity:0, yPercent:105 }}, {{ opacity:1, yPercent:0, duration:0.55*K, ease:"expo.out", immediateRender:false }}, 0.15*K);
tl.to(["#T .pill","#T .t"], {{ opacity:0, x:{20 if right else -20}, duration:0.35*K, ease:"power2.in", stagger:0.05*K }}, {dur - 0.4:.3f}*K);"""
    page(name, t0, dur, body, js, css)

def exercise(name, t0, n, total, title, target, dur=5.0):
    css = """#X { position:absolute; left:80px; bottom:96px; }
#X .idx { font-family:"Bebas Neue"; font-size:40px; letter-spacing:0.12em; color:#d80609; }
#X .idx span { color:rgba(255,255,255,0.7); }
#X .rule { width:120px; height:3px; background:#d80609; margin:8px 0 12px; transform-origin:0 50%; }
#X .t { font-size:104px; }
#X .x { display:inline-block; margin-top:16px; padding:8px 16px 7px; border:2px solid rgba(255,255,255,0.85); border-radius:4px;
  font-weight:800; font-size:25px; letter-spacing:0.2em; background:rgba(0,0,0,0.35); }
#X .x b { color:#d80609; }"""
    body = (f'<div class="back"></div><div id="X" class="sh"><div class="k idx">{n:02d} <span>/ {total:02d}</span></div><div class="rule"></div>'
            f'<div class="clip"><div class="t">{E(title)}</div></div><div class="x"><b>TARGET</b> &nbsp;{E(target)}</div></div>')
    js = lt_js('#X', dur) + '\ngsap.set("#X .rule", { scaleX:0 }); tl.to("#X .rule", { scaleX:1, duration:0.5*K, ease:"power3.inOut" }, 0.25*K);'
    page(name, t0, dur, body, js, css)

def cue(name, t0, title, sub=None, sub_at=None, dur=5.0, kicker='COACHING CUE', pos='right', width=640):
    """dark glass card with a red bar; sub can land later (sub_at, seconds after t0) on the spoken word"""
    place = {'right': f'right:72px; top:150px; width:{width}px;', 'left': f'left:72px; top:150px; width:{width}px;',
             'center': f'left:{(1920 - width) // 2}px; top:70px; width:{width}px;'}[pos]
    css = f"""#C {{ {place} }}
#C .k {{ font-size:19px; color:#ff5254; letter-spacing:0.28em; }}
#C .t {{ font-size:66px; white-space:normal; margin-top:10px; line-height:0.95; }}
#C .s {{ margin-top:12px; font-size:26px; line-height:1.25; color:#e9e9e9; font-weight:700; }}"""
    body = (f'<div id="C" class="card sh"><div class="k">{E(kicker)}</div><div class="clip"><div class="t">{E(title)}</div></div>'
            + (f'<div class="s">{E(sub)}</div>' if sub else '') + '</div>')
    sa = 0.55 if sub_at is None else sub_at
    js = f"""gsap.set(["#C .k","#C .t","#C .s"], {{ opacity:0 }});
tl.fromTo("#C", {{ opacity:0, x:{40 if pos == 'right' else -40 if pos == 'left' else 0}, y:{-20 if pos == 'center' else 0} }}, {{ opacity:1, x:0, y:0, duration:0.45*K, ease:"power3.out", immediateRender:false }}, 0);
tl.fromTo("#C .k", {{ opacity:0 }}, {{ opacity:1, duration:0.3*K, immediateRender:false }}, 0.15*K);
tl.fromTo("#C .t", {{ opacity:0, yPercent:100 }}, {{ opacity:1, yPercent:0, duration:0.55*K, ease:"expo.out", immediateRender:false }}, 0.2*K);
tl.fromTo("#C .s", {{ opacity:0, y:12 }}, {{ opacity:1, y:0, duration:0.45*K, ease:"power2.out", immediateRender:false }}, {sa:.3f}*K);
tl.to("#C", {{ opacity:0, x:{30 if pos == 'right' else -30 if pos == 'left' else 0}, duration:0.35*K, ease:"power2.in" }}, {dur - 0.4:.3f}*K);"""
    page(name, t0, dur, body, js, css)

def steps(name, t0, kicker, title, items, dur, pos='right', width=600, foot=None):
    """numbered/ticked list; items = [(text, at_seconds_after_t0, mark)] mark in '01','✓','✗'; foot=(text, at)"""
    place = {'right': f'right:64px; top:110px; width:{width}px;', 'gap': f'left:880px; top:90px; width:{width}px;', 'center': f'left:{(1920 - width) // 2}px; top:60px; width:{width}px;'}[pos]
    css = f"""#S {{ {place} }}
#S .k {{ font-size:19px; color:#ff5254; letter-spacing:0.28em; }}
#S .t {{ font-size:58px; margin:8px 0 12px; white-space:normal; }}
#S .row {{ display:flex; align-items:flex-start; gap:16px; padding:11px 0; border-top:1px solid rgba(255,255,255,0.14); }}
#S .m {{ flex:0 0 46px; height:46px; display:flex; align-items:center; justify-content:center; font-family:"Bebas Neue"; font-size:30px;
  background:#d80609; color:#fff; border-radius:4px; }}
#S .m.no {{ background:#2a2a2e; color:#ff5254; border:2px solid #ff5254; }}
#S .m.ok {{ background:#f2f2f2; color:#111; }}
#S .tx {{ font-weight:800; font-size:27px; line-height:1.2; letter-spacing:0.01em; padding-top:6px; }}
#S .tx small {{ display:block; font-weight:600; font-size:21px; color:#bdbdbd; margin-top:3px; letter-spacing:0.02em; }}
#S .ft {{ margin-top:12px; font-weight:800; font-size:23px; letter-spacing:0.14em; color:#ff5254; }}"""
    rows, js = [], [f"""gsap.set(["#S .k","#S .t"], {{ opacity:0 }});
tl.fromTo("#S", {{ opacity:0, x:{40 if pos == 'right' else 0}, y:{0 if pos == 'right' else -20} }}, {{ opacity:1, x:0, y:0, duration:0.45*K, ease:"power3.out", immediateRender:false }}, 0);
tl.fromTo("#S .k", {{ opacity:0 }}, {{ opacity:1, duration:0.3*K, immediateRender:false }}, 0.15*K);
tl.fromTo("#S .t", {{ opacity:0, yPercent:100 }}, {{ opacity:1, yPercent:0, duration:0.55*K, ease:"expo.out", immediateRender:false }}, 0.2*K);"""]
    for i, (text, at, mark, *small) in enumerate(items):
        cls = 'no' if mark == '✗' else 'ok' if mark == '✓' else ''
        sm = f'<small id="sm{i}">{E(small[0][0])}</small>' if small else ''
        rows.append(f'<div class="row" id="r{i}"><div class="m {cls}">{E(mark)}</div><div class="tx">{E(text)}{sm}</div></div>')
        js.append(f"""gsap.set("#r{i}", {{ opacity:0 }});
tl.fromTo("#r{i}", {{ opacity:0, x:24 }}, {{ opacity:1, x:0, duration:0.4*K, ease:"power3.out", immediateRender:false }}, {at:.3f}*K);
tl.fromTo("#r{i} .m", {{ scale:0.4 }}, {{ scale:1, duration:0.45*K, ease:"back.out(2.2)", immediateRender:false }}, {at + 0.08:.3f}*K);""")
        if small:
            js.append(f"""gsap.set("#sm{i}", {{ opacity:0 }}); tl.fromTo("#sm{i}", {{ opacity:0, y:8 }}, {{ opacity:1, y:0, duration:0.35*K, immediateRender:false }}, {small[0][1]:.3f}*K);""")
    ft = ''
    if foot:
        ft = f'<div class="ft" id="ft">{E(foot[0])}</div>'
        js.append(f"""gsap.set("#ft", {{ opacity:0 }}); tl.fromTo("#ft", {{ opacity:0, y:10 }}, {{ opacity:1, y:0, duration:0.4*K, immediateRender:false }}, {foot[1]:.3f}*K);""")
    js.append(f"""tl.to("#S", {{ opacity:0, x:{30 if pos == 'right' else 0}, duration:0.4*K, ease:"power2.in" }}, {dur - 0.45:.3f}*K);""")
    body = f'<div id="S" class="card sh"><div class="k">{E(kicker)}</div><div class="clip"><div class="t">{E(title)}</div></div>{"".join(rows)}{ft}</div>'
    page(name, t0, dur, body, '\n'.join(js), css)

def chips(name, t0, title, chips_at, stamp, stamp_at, dur):
    """top-centre: title, stat chips landing on the words, then a red stamp"""
    css = """#P { position:absolute; left:0; right:0; top:34px; display:flex; flex-direction:column; align-items:center; gap:10px; }
#P .t { font-size:58px; }
#P .row { display:flex; gap:18px; }
#P .c { padding:10px 22px 9px; background:rgba(12,12,14,0.78); border:2px solid rgba(255,255,255,0.8); border-radius:4px;
  font-family:"Bebas Neue"; font-size:40px; letter-spacing:0.04em; }
#P .st { font-family:"Bebas Neue"; font-size:44px; letter-spacing:0.06em; background:#d80609; padding:6px 22px 2px; transform:rotate(-3deg); }"""
    body = (f'<div id="P" class="sh"><div class="clip"><div class="t">{E(title)}</div></div><div class="row">'
            + ''.join(f'<div class="c" id="c{i}">{E(c)}</div>' for i, (c, _) in enumerate(chips_at))
            + f'</div><div class="st">{E(stamp)}</div></div>')
    js = [f"""gsap.set(["#P .t","#P .c","#P .st"], {{ opacity:0 }});
tl.fromTo("#P .t", {{ opacity:0, yPercent:100 }}, {{ opacity:1, yPercent:0, duration:0.55*K, ease:"expo.out", immediateRender:false }}, 0.1*K);"""]
    for i, (_, at) in enumerate(chips_at):
        js.append(f'tl.fromTo("#c{i}", {{ opacity:0, scale:1.4 }}, {{ opacity:1, scale:1, duration:0.35*K, ease:"back.out(2)", immediateRender:false }}, {at:.3f}*K);')
    js.append(f'tl.fromTo("#P .st", {{ opacity:0, scale:2.2 }}, {{ opacity:1, scale:1, duration:0.3*K, ease:"power4.in", immediateRender:false }}, {stamp_at:.3f}*K);')
    js.append(f'tl.to("#P", {{ opacity:0, y:-16, duration:0.4*K, ease:"power2.in" }}, {dur - 0.45:.3f}*K);')
    page(name, t0, dur, body, '\n'.join(js), css)

def quote(name, t0, text, dur=5.0):
    css = """#Q { position:absolute; left:0; right:0; top:80px; text-align:center; }
#Q .mk { font-family:"Bebas Neue"; font-size:150px; line-height:0.55; color:#d80609; height:60px; }
#Q .q { font-family:"Bebas Neue"; font-size:92px; letter-spacing:0.02em; }
#Q .rule { width:110px; height:4px; background:#d80609; margin:14px auto 0; transform-origin:50% 50%; }"""
    body = f'<div id="Q" class="sh"><div class="mk">&ldquo;</div><div class="clip"><div class="q">{E(text)}</div></div><div class="rule"></div></div>'
    js = f"""gsap.set(["#Q .mk","#Q .q"], {{ opacity:0 }}); gsap.set("#Q .rule", {{ scaleX:0 }});
tl.fromTo("#Q .mk", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.4*K, ease:"power3.out", immediateRender:false }}, 0.05*K);
tl.fromTo("#Q .q", {{ opacity:0, yPercent:100 }}, {{ opacity:1, yPercent:0, duration:0.6*K, ease:"expo.out", immediateRender:false }}, 0.15*K);
tl.to("#Q .rule", {{ scaleX:1, duration:0.5*K, ease:"power3.inOut" }}, 0.45*K);
tl.to("#Q", {{ opacity:0, duration:0.4*K, ease:"power2.in" }}, {dur - 0.45:.3f}*K);"""
    page(name, t0, dur, body, js, css)

def reps(name, t0, counts, dur, extra=None):
    """top-right rep counter; counts = [(n, at)]; extra = (text, at) chip under it"""
    css = """#R { position:absolute; right:72px; top:64px; display:flex; flex-direction:column; align-items:flex-end; gap:10px; }
#R .box { display:flex; align-items:baseline; gap:14px; background:rgba(12,12,14,0.78); border-left:6px solid #d80609; padding:8px 22px 4px 18px; }
#R .l { font-weight:800; font-size:22px; letter-spacing:0.28em; color:#ff5254; }
#R .n { position:relative; width:96px; height:110px; overflow:hidden; }
#R .n div { position:absolute; right:0; top:0; font-family:"Bebas Neue"; font-size:120px; line-height:0.92; }
#R .ex { font-family:"Bebas Neue"; font-size:44px; letter-spacing:0.06em; background:#d80609; padding:4px 16px 0; }"""
    nums = ''.join(f'<div id="n{i}">{n}</div>' for i, (n, _) in enumerate(counts))
    body = f'<div id="R" class="sh"><div class="box"><div class="l">REPS</div><div class="n">{nums}</div></div>' + (f'<div class="ex">{E(extra[0])}</div>' if extra else '') + '</div>'
    js = [f'gsap.set("#R .n div", {{ yPercent:110 }}); tl.fromTo("#R .box", {{ opacity:0, x:30 }}, {{ opacity:1, x:0, duration:0.4*K, ease:"power3.out", immediateRender:false }}, 0);']
    for i, (_, at) in enumerate(counts):
        js.append(f'tl.to("#n{i}", {{ yPercent:0, duration:0.25*K, ease:"back.out(1.6)" }}, {at:.3f}*K);')
        if i: js.append(f'tl.to("#n{i - 1}", {{ yPercent:-110, duration:0.25*K, ease:"power2.in" }}, {at:.3f}*K);')
    if extra:
        js.append(f'gsap.set("#R .ex", {{ opacity:0 }}); tl.fromTo("#R .ex", {{ opacity:0, scale:1.5 }}, {{ opacity:1, scale:1, duration:0.3*K, ease:"back.out(2)", immediateRender:false }}, {extra[1]:.3f}*K);')
    js.append(f'tl.to("#R", {{ opacity:0, x:24, duration:0.35*K, ease:"power2.in" }}, {dur - 0.4:.3f}*K);')
    page(name, t0, dur, body, '\n'.join(js), css)
