"""NPC Italy reels — graphics overlay comps (one per reel), 9:16 alpha.
Laid out at 1080x1920 and rendered at SCALE x (2 = 2160x3840 UHD vertical).
Team Apexx look (PREFERENCES style A): Bebas Neue display, Montserrat text, red #d80609 accent, dark glass keyword cards
below karaoke captions, everything out of the bottom ~20% Reels UI band except where it has to cover the edit's burned graphics.
Comps render at 24 fps with times divided by 1.001, then are conformed to 23.976 so they line up with the cut video."""
import json, os, shutil, html, re
ROOT = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(ROOT)
WS = '/Users/ashleychivers/Documents/Claude Video Studio'
GSAP = WS + '/video-projects/training-day/gfx/assets/gsap.min.js'
HFJSON = WS + '/video-projects/training-day/gfx/hyperframes.json'
R = json.load(open(PROJ + '/reels.json')); FPS = R['fps']
K = 1 / 1.001
SCALE = int(os.environ.get('SCALE', 2))
W, H = 1080 * SCALE, 1920 * SCALE
RED = '#d80609'

def T(t): return f'{t * K:.3f}'
E = lambda s: html.escape(s)

HEAD = """<!doctype html><html lang="en"><head><meta charset="UTF-8" />
<meta name="viewport" content="width=%W%, height=%H%" /><script src="assets/gsap.min.js"></script>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:%W%px; height:%H%px; overflow:hidden; background:transparent; }
#stage { position:relative; width:%W%px; height:%H%px; overflow:hidden; }
#stage > #root { transform:scale(%S%); transform-origin:0 0; }
#root { position:relative; width:1080px; height:1920px; overflow:hidden; font-family:Montserrat, sans-serif; color:#f6f6f6; }
.sh { text-shadow:0 3px 18px rgba(0,0,0,0.75), 0 1px 3px rgba(0,0,0,0.7); }
.bb { font-family:"Bebas Neue", sans-serif; line-height:0.92; letter-spacing:0.01em; white-space:nowrap; }
.r { color:#d80609; }
.kick { font-weight:800; font-size:22px; letter-spacing:0.28em; color:rgba(255,255,255,0.86); display:flex; align-items:center; gap:14px; }
.kick i { display:inline-block; width:36px; height:4px; background:#d80609; }
.clip { overflow:hidden; padding-bottom:4px; }
/* captions */
.cap { position:absolute; left:40px; right:40px; text-align:center; opacity:0; font-weight:900; font-size:62px; line-height:1.06;
  letter-spacing:-0.005em; text-transform:uppercase; color:#fff;
  text-shadow:-3px -3px 0 #000, 3px -3px 0 #000, -3px 3px 0 #000, 3px 3px 0 #000, 0 4px 0 #000, 0 6px 22px rgba(0,0,0,0.85); }
.cap span { display:inline-block; }
/* hook */
.hook { position:absolute; left:0; right:0; top:0; height:640px; opacity:0;
  background:linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.38) 45%, rgba(0,0,0,0) 100%); }
.hook .in { position:absolute; left:64px; right:64px; top:150px; }
.hook .pill { display:inline-block; background:#d80609; font-weight:800; font-size:22px; letter-spacing:0.24em; padding:8px 16px 7px; }
.hook .bb { font-size:122px; margin-top:16px; }
/* keyword card */
.card { position:absolute; left:54px; right:54px; top:1290px; opacity:0; padding:24px 34px 26px 44px; border-radius:18px;
  background:linear-gradient(135deg, rgba(18,18,18,0.86), rgba(8,8,8,0.78)); border:1px solid rgba(255,255,255,0.14);
  box-shadow:0 18px 50px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.16); overflow:hidden; }
.card::before { content:""; position:absolute; left:0; top:0; bottom:0; width:10px; background:#d80609; }
.card .bb { font-size:92px; margin-top:8px; }
.card .sub { font-weight:700; font-size:28px; color:#cfcfcf; margin-top:8px; letter-spacing:0.02em; }
.strike { position:absolute; height:9px; background:#d80609; transform-origin:0 50%; border-radius:3px; }
.stamp { position:absolute; right:30px; top:50%; font-family:"Bebas Neue"; font-size:64px; color:#fff; background:#d80609;
  padding:6px 18px 2px; opacity:0; letter-spacing:0.03em; }
.chips { display:flex; gap:14px; margin-top:14px; flex-wrap:wrap; }
.chip { display:flex; align-items:center; gap:12px; padding:12px 18px 9px; border-radius:10px; background:rgba(255,255,255,0.08);
  border:1px solid rgba(255,255,255,0.18); font-family:"Bebas Neue"; font-size:50px; line-height:1; letter-spacing:0.02em; opacity:0; }
.chip b { font-family:Montserrat; font-weight:900; font-size:30px; color:#d80609; }
.chip.ok b { color:#2ecc71; }
/* cover label (sits over the edit's burned-in labels) */
.lbl { position:absolute; display:flex; align-items:center; gap:14px; padding:14px 22px 10px; opacity:0;
  background:#0c0c0c; border-left:8px solid #d80609; font-family:"Bebas Neue"; letter-spacing:0.03em; line-height:1; }
.flash { position:absolute; inset:0; background:#fff; opacity:0; }
%CSS%
</style></head><body>
<div id="stage" data-composition-id="main" data-start="0" data-duration="%DUR%" data-width="%W%" data-height="%H%"><div id="root">%BODY%</div></div>
<script>(() => { const tl = gsap.timeline({ paused:true });
%JS%
tl.to({}, { duration:%DUR% }, 0); window.__timelines = window.__timelines || {}; window.__timelines["main"] = tl; })();</script>
</body></html>"""


class Reel:
    def __init__(self, name, dur):
        self.name, self.dur = name, dur
        self.body, self.js, self.css, self.sfx = [], [], [], []

    # --- building blocks -------------------------------------------------
    def hook(self, id, t0, t1, kicker, lines, top=150):
        ls = ''.join(f'<div class="clip"><div class="bb l">{l}</div></div>' for l in lines)
        self.body.append(f'<div class="hook" id="{id}"><div class="in sh" style="top:{top}px"><div class="pill">{E(kicker)}</div>{ls}</div></div>')
        self.js.append(f"""tl.set("#{id}", {{ opacity:1 }}, {T(t0)});
tl.fromTo("#{id} .pill", {{ opacity:0, x:-30 }}, {{ opacity:1, x:0, duration:{T(0.35)}, ease:"power3.out", immediateRender:false }}, {T(t0 + 0.05)});
tl.fromTo("#{id} .l", {{ yPercent:110 }}, {{ yPercent:0, duration:{T(0.55)}, ease:"expo.out", stagger:{T(0.09)}, immediateRender:false }}, {T(t0 + 0.12)});
tl.to("#{id} .l", {{ scale:1.03, duration:{T(max(0.5, t1 - t0 - 1.2))}, ease:"none", transformOrigin:"0% 50%" }}, {T(t0 + 0.7)});
tl.to("#{id}", {{ opacity:0, y:-24, duration:{T(0.3)}, ease:"power2.in" }}, {T(t1 - 0.3)});""")
        self.sfx.append(('whoosh', t0 + 0.05, 0.30))

    def card(self, id, t0, t1, kicker, title, sub=None, inner='', top=1290, size=92):
        assert t1 > t0 + 0.8, (self.name, id, t0, t1)
        s = f'<div class="sub">{sub}</div>' if sub else ''
        self.body.append(f'<div class="card" id="{id}" style="top:{top}px"><div class="kick"><i></i>{E(kicker)}</div>'
                         f'<div class="clip"><div class="bb t" style="font-size:{size}px">{title}</div></div>{s}{inner}</div>')
        self.js.append(f"""tl.fromTo("#{id}", {{ opacity:0, y:40, scale:0.97 }}, {{ opacity:1, y:0, scale:1, duration:{T(0.4)}, ease:"back.out(1.6)", immediateRender:false }}, {T(t0)});
tl.fromTo("#{id} .t", {{ yPercent:105 }}, {{ yPercent:0, duration:{T(0.5)}, ease:"expo.out", immediateRender:false }}, {T(t0 + 0.08)});
tl.fromTo("#{id} .sub", {{ opacity:0, y:10 }}, {{ opacity:1, y:0, duration:{T(0.35)}, ease:"power2.out", immediateRender:false }}, {T(t0 + 0.3)});
tl.to("#{id}", {{ y:-6, duration:{T(max(0.4, t1 - t0 - 0.8))}, ease:"sine.inOut" }}, {T(t0 + 0.45)});""")
        if t1 < self.dur - 0.05:
            self.js.append(f'tl.to("#{id}", {{ opacity:0, y:-30, filter:"blur(6px)", duration:{T(0.28)}, ease:"power2.in" }}, {T(t1 - 0.28)});')
        self.sfx.append(('pop', t0, 0.22))

    def strike(self, id, card, t, left, width, top, stamp=None):
        """red line drawn through a card's title at t (+ optional stamp)"""
        self.js.append(f'tl.fromTo("#{card} .strike", {{ scaleX:0 }}, {{ scaleX:1, duration:{T(0.28)}, ease:"power3.inOut" }}, {T(t)});')
        self.body[-1] = self.body[-1].replace('</div></div>', f'</div></div><div class="strike" style="left:{left}px; width:{width}px; top:{top}px"></div>', 1)
        if stamp:
            self.body[-1] = self.body[-1][:-6] + f'<div class="stamp">{E(stamp)}</div></div>'
            self.js.append(f'tl.fromTo("#{card} .stamp", {{ opacity:0, scale:1.8, rotation:-6, yPercent:-50 }}, {{ opacity:1, scale:1, rotation:-6, yPercent:-50, duration:{T(0.22)}, ease:"power4.in", immediateRender:false }}, {T(t + 0.25)});')
            self.sfx.append(('slam', t + 0.38, 0.28))

    def chips(self, items):
        """items: [(label, t, mark)] -> inner html + timeline (call after card() of the same id via chip_js)"""
        return '<div class="chips">' + ''.join(
            f'<div class="chip{" ok" if m == "✓" else ""}" data-t="{t}"><b>{m}</b>{E(l)}</div>' if m else f'<div class="chip" data-t="{t}">{E(l)}</div>'
            for l, t, m in items) + '</div>'

    def chip_js(self, id, items):
        for k, (l, t, m) in enumerate(items, 1):
            self.js.append(f'tl.fromTo("#{id} .chip:nth-child({k})", {{ opacity:0, y:18, scale:0.9 }}, {{ opacity:1, y:0, scale:1, duration:{T(0.3)}, ease:"back.out(2)", immediateRender:false }}, {T(t)});')
            self.sfx.append(('click', t, 0.35))

    def label(self, id, t0, t1, x, y, w, h, text, size, align='left'):
        just = 'flex-end' if align == 'right' else 'flex-start'
        self.body.append(f'<div class="lbl sh" id="{id}" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px; font-size:{size}px; justify-content:{just}">{text}</div>')
        self.js.append(f"""tl.fromTo("#{id}", {{ opacity:0, x:{-20 if align == 'left' else 20} }}, {{ opacity:1, x:0, duration:{T(0.25)}, ease:"power3.out", immediateRender:false }}, {T(t0)});
tl.to("#{id}", {{ opacity:0, duration:{T(0.3)}, ease:"power2.in" }}, {T(t1 - 0.3)});""")

    def flash(self, t):
        self.body.append(f'<div class="flash" id="fl{len(self.body)}"></div>')
        fid = f'fl{len(self.body) - 1}'
        self.js.append(f'tl.fromTo("#{fid}", {{ opacity:0 }}, {{ opacity:0.85, duration:{T(0.06)}, ease:"none", immediateRender:false }}, {T(t - 0.06)}); '
                       f'tl.to("#{fid}", {{ opacity:0, duration:{T(0.22)}, ease:"power2.out" }}, {T(t)});')
        self.sfx.append(('whoosh', t - 0.18, 0.32))

    def captions(self, words, y=1110, hide=()):
        """karaoke: groups of <=3 words, active word red + pop. hide: [(t0,t1)] windows with no captions"""
        groups, g = [], []
        for k, w in enumerate(words):
            g.append(w)
            txt = ' '.join(x['text'] for x in g)
            nxt = words[k + 1] if k + 1 < len(words) else None
            brk = (len(g) >= 3 or len(txt) > 13 or re.search(r'[.,?!]$', w['raw'])
                   or (nxt and nxt['start'] - w['end'] > 0.45) or (nxt and len(txt) + len(nxt['text']) > 17))
            if brk or not nxt: groups.append(g); g = []
        for gi, g in enumerate(groups):
            a = g[0]['start']; nxt = groups[gi + 1][0]['start'] if gi + 1 < len(groups) else None
            b = nxt if (nxt is not None and nxt - g[-1]['end'] < 0.7) else min(self.dur, g[-1]['end'] + 0.3)
            if any(h0 <= a < h1 for h0, h1 in hide): continue
            id = f'c{gi}'
            spans = ' '.join(f'<span id="{id}w{k}">{E(w["text"])}</span>' for k, w in enumerate(g))
            self.body.append(f'<div class="cap" id="{id}" style="top:{y}px">{spans}</div>')
            self.js.append(f'tl.set("#{id}", {{ opacity:1 }}, {T(a)}); tl.fromTo("#{id}", {{ scale:0.86, y:14 }}, {{ scale:1, y:0, duration:{T(0.13)}, ease:"power3.out", immediateRender:false }}, {T(a)}); tl.set("#{id}", {{ opacity:0 }}, {T(b)});')
            for k, w in enumerate(g):
                we = g[k + 1]['start'] if k + 1 < len(g) else b
                self.js.append(f'tl.set("#{id}w{k}", {{ color:"{RED}" }}, {T(w["start"])}); tl.fromTo("#{id}w{k}", {{ scale:1.12 }}, {{ scale:1, duration:{T(0.16)}, ease:"power2.out", immediateRender:false }}, {T(w["start"])}); '
                               f'tl.set("#{id}w{k}", {{ color:"#ffffff" }}, {T(max(w["start"] + 0.05, we))});')

    def scope_flashes(self):
        for t0, t1 in R['reels'][self.name].get('scopes', []):
            if t0 > 0: self.flash(t0)
            if t1 < self.dur and self.name != 'judge-your-prep': self.flash(t1)

    def write(self):
        self.scope_flashes()
        d = f'{ROOT}/comps/{self.name}'; os.makedirs(d + '/assets', exist_ok=True)
        open(f'{d}/index.html', 'w').write(HEAD.replace('%DUR%', f'{self.dur * K:.3f}').replace('%BODY%', '\n'.join(self.body))
                                           .replace('%JS%', '\n'.join(self.js)).replace('%CSS%', '\n'.join(self.css))
                                           .replace('%W%', str(W)).replace('%H%', str(H)).replace('%S%', str(SCALE)))
        shutil.copy(HFJSON, d); shutil.copy(GSAP, d + '/assets/')
        open(f'{d}/meta.json', 'w').write(json.dumps({"id": self.name, "name": self.name, "width": W, "height": H, "fps": 24}))
        json.dump(sorted(self.sfx, key=lambda s: s[1]), open(f'{ROOT}/sfx_{self.name}.json', 'w'))
        print('wrote', self.name, len(self.body), 'elements', len(self.sfx), 'sfx')


# --------------------------------------------------------------------- words
CENSOR = {'fucking': 'f*cking'}
def load_words(name, model, fixes=(), drop=(), add=()):
    d = json.load(open(f'{PROJ}/src/rt/{name}/{model}.json')); d = d if isinstance(d, list) else d['words']
    out = []
    for w in d:
        raw = w['text'].strip()
        if not raw or raw.startswith('♪'): continue
        out.append({'raw': raw, 'start': w['start'], 'end': w['end']})
    for i, new in fixes:              # (index, replacement raw text) ; replacement '' deletes
        out[i]['raw'] = new
    out = [w for i, w in enumerate(out) if i not in drop and w['raw']]
    out += [{'raw': r, 'start': a, 'end': b} for r, a, b in add]
    out.sort(key=lambda w: w['start'])
    for w in out:
        core = w['raw'].strip('.,?!').lower()
        w['text'] = CENSOR.get(core, w['raw'].strip('.,?!'))
    return out

def find(words, text, after=0.0):
    for w in words:
        if w['start'] >= after and w['text'].lower() == text.lower(): return w['start']
    raise KeyError(text)

def dur(name):
    return sum(round(b * FPS) - round(a * FPS) for a, b in R['reels'][name]['segs']) / FPS


# ============================================================ 1. post-show recovery
n = 'post-show-recovery'; r = Reel(n, dur(n))
wd = load_words(n, 'transcript', add=[('to', 42.86, 42.98), ('you.', 42.98, 43.2)])
wd = [w for w in wd if not (w['raw'] == 'look,' and 4.2 < w['start'] < 4.4) and not (w['raw'] == 'stage' and 3.6 < w['start'] < 3.7)]
f = lambda t, a=0.0: find(wd, t, a)
r.hook('h1', 0.15, 8.3, 'POST-SHOW RECOVERY', ['STAGE LEAN IS', '<span class="r">A ONE-DAY</span> LOOK'])
t = f('forever'); r.card('k1', t - 0.6, f('right', 7.9) + 0.4, 'THE MISTAKE', 'HOLDING STAGE LEAN FOREVER', size=74)
r.strike('s1', 'k1', f('happen') - 0.05, 40, 640, 92, stamp='NOPE')
t = f('one'); r.card('k2', t - 0.1, f('so', 16.0), 'REALITY', '<span class="r">1 DAY</span> LOOK', sub='Your show day — not a year-round look')
t = f('recover'); r.card('k3', f('goal') - 0.1, f('so', 25.5) - 0.1, 'THE GOAL OF A RECOVERY PHASE', 'JUST <span class="r">RECOVER</span>')
items = [('OUTPUT', f('reduction'), '↓'), ('FOOD', f('increase'), '↑'), ('MAINTENANCE', f('maintenance'), '✓')]
r.card('k4', f('reduction') - 0.25, f('try', 34.0) - 0.2, 'WHAT RECOVERY LOOKS LIKE', 'THE RECOVERY PHASE', inner=r.chips(items), size=70)
r.chip_js('k4', items)
r.card('k5', f('detach') - 0.1, f('rely') - 0.15, 'MINDSET', 'DETACH <span class="r">&amp;</span> EMBRACE', sub='Let go of the stage look. Embrace the post-show.')
r.card('k6', f('rely') - 0.05, r.dur, 'YOU’RE NOT ALONE', 'RELY ON YOUR <span class="r">COACH</span>', sub='…and the people close to you')
r.captions(wd)
r.write()

# ============================================================ 2. bicep stretch (static crop, covers the edit's burned labels)
n = 'bicep-stretch'; r = Reel(n, dur(n))
wd = load_words(n, 'med')
for w in wd:
    if w['text'] == 'card': w['text'] = 'curl'
f = lambda t, a=0.0: find(wd, t, a)
# cover for the edit's "MACHINE PREACHER CURL" title (fragment at x0-350, y1465-1610 until ~4.1 s)
r.body.append('<div class="card" id="t0" style="left:0; right:auto; width:700px; top:1412px; min-height:224px; border-radius:0 18px 18px 0; padding:30px 34px 24px 44px; background:#0c0c0c;">'
              '<div class="kick"><i></i>BICEP TIP</div><div class="clip"><div class="bb t" style="font-size:96px">PREACHER <span class="r">CURL</span></div></div></div>')
r.js.append(f"""tl.set("#t0", {{ opacity:1 }}, 0);
tl.fromTo("#t0 .t", {{ yPercent:105 }}, {{ yPercent:0, duration:{T(0.5)}, ease:"expo.out", immediateRender:false }}, {T(0.1)});
tl.fromTo("#t0 .kick", {{ opacity:0, x:-20 }}, {{ opacity:1, x:0, duration:{T(0.35)}, ease:"power3.out", immediateRender:false }}, {T(0.05)});
tl.to("#t0", {{ x:-760, duration:{T(0.4)}, ease:"power3.in" }}, {T(4.35)});""")
r.sfx.append(('whoosh', 0.05, 0.28))
# "SEAT LOW" over the edit's label stub (x1015-1080, y1460-1545, 8.1-18.7 s)
r.label('l1', 7.85, 18.8, 690, 1446, 390, 112, 'SEAT <span class="r">&nbsp;LOW</span>', 72, align='right')
r.sfx.append(('click', 7.85, 0.35))
# "FULL STRETCH" over the edit's "…= BICEP STRETCH" pill (x0-565, y748-835, 10.3-18.7 s)
r.label('l2', 10.15, 18.8, 0, 726, 640, 132, 'FULL STRETCH <span class="r">&nbsp;AT THE BOTTOM</span>', 58)
r.sfx.append(('click', 10.15, 0.35))
r.card('k1', 19.0, r.dur, 'THE TIP', 'SEAT LOW <span class="r">=</span> FULL STRETCH', sub='Lengthened position, biceps stretched at the bottom', top=1300, size=84)
r.captions(wd, y=1215)
r.write()

# ============================================================ 3. life balance (outside Gold's)
n = 'life-balance'; r = Reel(n, dur(n))
wd = load_words(n, 'transcript')
f = lambda t, a=0.0: find(wd, t, a)
r.hook('h1', 0.1, 7.45, 'PREP REALITY', ['LIFE STILL', 'HAPPENS <span class="r">ON PREP</span>'])
r.card('k1', f('life', 7.5) - 0.1, f('hardcore') - 0.45, 'THE TRUTH', 'LIFE STILL NEEDS <span class="r">MANAGING</span>', size=84)
r.card('k2', f('hardcore') - 0.2, f('wise') - 0.2, 'DON’T GET IT TWISTED', 'AS <span class="r">HARDCORE</span> AS THEY COME', size=84)
r.card('k3', f('wise') - 0.1, f('people', 17.0) - 0.2, 'BUT BE WISE ENOUGH', 'LIFE HAPPENS <span class="r">OUTSIDE</span> BODYBUILDING', size=72)
items = [('PERSONAL LIFE', f('personal'), ''), ('WORK', f('work'), ''), ('RELATIONSHIPS', f('relationships'), ''), ('BODYBUILDING', f('bodybuilding', 26.0), '')]
r.card('k3b', f('balance') - 0.35, f('between') - 0.25, 'PEOPLE SAY', 'THERE’S NO BALANCE', size=88)
r.strike('s3b', 'k3b', f('but', 19.0), 40, 560, 98, stamp='WRONG')
r.card('k4', f('between') - 0.15, f('otherwise') - 0.2, 'YOU NEED SOME', '<span class="r">BALANCE</span> BETWEEN', inner=r.chips(items), size=84)
r.chip_js('k4', items)
items = [('LONELY', f('lonely'), '✕'), ('NO JOB', f('job'), '✕'), ('BILLS UNPAID', f('bills'), '✕')]
r.card('k5', f('otherwise') - 0.05, r.dur, 'OTHERWISE YOU END UP…', 'NO BALANCE <span class="r">=</span>', inner=r.chips(items), size=72)
r.chip_js('k5', items)
r.captions(wd)
r.write()

# ============================================================ 4. judge your prep (widescreen hook band 0-7 s)
n = 'judge-your-prep'; r = Reel(n, dur(n))
wd = load_words(n, 'med')
wd = [w for w in wd if not (w['raw'] == 'could' and 6.5 < w['start'] < 7.0)]
for w in wd:
    if w['raw'] == 'cloud': w['text'] = 'clouds'
f = lambda t, a=0.0: find(wd, t, a)
SC = R['reels'][n]['scopes'][0][1]
# hook above the band (band sits at y 575-1098)
r.body.append('<div class="hook" id="h1" style="height:600px; background:none;"><div class="in sh" style="top:205px"><div class="pill">PREP MINDSET</div>'
              '<div class="clip"><div class="bb l" style="font-size:108px">DON’T JUDGE YOUR PREP</div></div>'
              '<div class="clip"><div class="bb l" style="font-size:108px">BY THE <span class="r">RESULT</span></div></div></div></div>')
r.js.append(f"""tl.set("#h1", {{ opacity:1 }}, 0);
tl.fromTo("#h1 .pill", {{ opacity:0, x:-30 }}, {{ opacity:1, x:0, duration:{T(0.35)}, ease:"power3.out", immediateRender:false }}, {T(0.05)});
tl.fromTo("#h1 .l", {{ yPercent:110 }}, {{ yPercent:0, duration:{T(0.55)}, ease:"expo.out", stagger:{T(0.1)}, immediateRender:false }}, {T(0.12)});
tl.to("#h1", {{ opacity:0, duration:{T(0.12)} }}, {T(SC - 0.1)});""")
r.sfx.append(('whoosh', 0.05, 0.3))
r.flash(SC)
vs = ('<div style="display:flex; gap:18px; margin-top:16px;">'
      '<div class="chip" style="flex:1; justify-content:space-between;"><span>70% <span style="opacity:.6">ON STAGE</span></span><b style="color:#f2c94c">1ST</b></div>'
      '<div class="chip" style="flex:1; justify-content:space-between;"><span>100% <span style="opacity:.6">ON STAGE</span></span><b>5TH</b></div></div>')
r.card('k1', f('70%') - 0.3, f('is', 17.9) - 0.15, 'SAME ATHLETE. ONE WEEK APART.', 'WHAT’S THE <span class="r">REAL</span> RESULT?', inner=vs, size=76)
r.js.append(f'tl.fromTo("#k1 .chip:nth-child(1)", {{ opacity:0, x:-30 }}, {{ opacity:1, x:0, duration:{T(0.3)}, ease:"back.out(2)", immediateRender:false }}, {T(f("70%"))});')
r.js.append(f'tl.fromTo("#k1 .chip:nth-child(2)", {{ opacity:0, x:30 }}, {{ opacity:1, x:0, duration:{T(0.3)}, ease:"back.out(2)", immediateRender:false }}, {T(f("100%"))});')
r.sfx += [('click', f('70%'), 0.35), ('click', f('100%'), 0.35)]
r.card('k2', f('cheap') - 0.2, f('focus') - 0.2, 'THE CHEAP TROPHY?', 'OR <span class="r">PERSONAL</span> DEVELOPMENT', size=80)
r.card('k3', f('focus') - 0.05, f('so', 28.0) - 0.1, 'THE ONLY JOB', 'BRING YOUR <span class="r">BEST</span> TO STAGE', size=84)
r.card('k4', f('give') - 0.2, f('you', 36.6) - 0.2, 'WHATEVER THE OUTCOME', 'GIVE IT <span class="r">10/10</span>', sub='So there’s nothing more you could have done', size=110)
items = [('THE JUDGES', f('judges'), '✕'), ('THE LINE-UP', f('lineup'), '✕'), ('YOURSELF', f('yourself'), '✓')]
r.card('k5', f('judges') - 0.35, r.dur, 'WHAT YOU CAN CONTROL', 'CONTROL <span class="r">YOURSELF</span>', inner=r.chips(items), size=80)
r.chip_js('k5', items)
r.captions([w for w in wd if w['start'] >= 0], y=1150)
r.write()
