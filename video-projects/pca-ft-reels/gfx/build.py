"""PCA FT reels (from the NPC Italy reels kit) — graphics overlay comps (one per reel), 9:16 alpha.
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
R = json.load(open(PROJ + '/reels.json')); FPS = 24000 / 1001
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
/* 3D breakdown insert */
.br { position:absolute; inset:0; opacity:0; }
.brbg { position:absolute; inset:0; background:radial-gradient(ellipse 80% 55% at 50% 52%, #2a0a0b 0%, #0d0d0f 55%, #050506 100%); }
.brgrid { position:absolute; inset:0; opacity:0.5; background-image:linear-gradient(rgba(255,255,255,0.06) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,0.06) 2px, transparent 2px);
  background-size:120px 120px; -webkit-mask-image:radial-gradient(ellipse 70% 60% at 50% 55%, #000 30%, transparent 80%); }
.brttl { position:absolute; left:64px; right:40px; top:200px; }
.brttl .t { font-size:96px; margin-top:12px; }
.brwrap { position:absolute; left:160px; top:470px; width:760px; height:1064px; perspective:1600px; }
.brcard { position:absolute; inset:0; border-radius:26px; overflow:hidden; transform-style:preserve-3d; border:2px solid rgba(255,255,255,0.18);
  box-shadow:0 40px 90px rgba(0,0,0,0.75), 0 0 0 1px rgba(216,6,9,0.35), 0 0 60px rgba(216,6,9,0.25); background:#0b0b0c; opacity:0; }
.brcard img { position:absolute; left:-507px; top:-760px; width:1351px; height:1824px; }
.brcard .still { filter:brightness(0.32) saturate(0.4) blur(2px); }
.brcard .fig { filter:contrast(1.08) saturate(1.05) drop-shadow(0 0 18px rgba(216,6,9,0.45)); }
.glow { position:absolute; width:240px; height:240px; border-radius:50%; opacity:0; mix-blend-mode:screen;
  background:radial-gradient(circle, rgba(255,40,40,0.55) 0%, rgba(216,6,9,0.25) 40%, rgba(216,6,9,0) 70%); }
.brsvg { position:absolute; left:0; top:0; }
.dot { position:absolute; width:26px; height:26px; border-radius:50%; background:#d80609; border:4px solid #fff; transform:scale(0); }
.dot i { position:absolute; inset:-4px; border-radius:50%; border:3px solid #ff3b3b; }
.cl { position:absolute; display:flex; align-items:center; gap:12px; opacity:0; padding:12px 18px 8px; border-radius:10px; background:rgba(10,10,10,0.88);
  border:1px solid rgba(255,255,255,0.2); font-family:"Bebas Neue"; font-size:46px; line-height:1; letter-spacing:0.02em; white-space:nowrap; }
.cl b { font-family:Montserrat; font-weight:900; font-size:24px; color:#fff; background:#d80609; border-radius:50%; width:40px; height:40px;
  display:flex; align-items:center; justify-content:center; padding-top:2px; }
.brsub { position:absolute; left:80px; right:80px; top:1566px; text-align:center; opacity:0; font-weight:800; font-size:32px; letter-spacing:0.04em; color:#fff;
  padding:16px 20px 14px; border-radius:12px; background:#d80609; }
/* live breakdown (marks drawn on the footage) */
.mk { position:absolute; inset:0; opacity:0; }
.mk .fz { position:absolute; left:0; top:0; width:1080px; height:1920px; filter:brightness(0.85) contrast(1.05); }
.mkvig { position:absolute; inset:0; background:radial-gradient(ellipse 75% 50% at 60% 68%, rgba(0,0,0,0) 40%, rgba(0,0,0,0.55) 100%),
  linear-gradient(90deg, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.25) 38%, rgba(0,0,0,0) 55%); }
.mkttl { position:absolute; left:50px; width:440px; top:520px; }
.mkttl .kick { white-space:nowrap; }
.mkttl .t { font-size:88px; margin-top:12px; white-space:normal; }
.rg { position:absolute; left:0; top:0; width:0; height:0; }
.rg .o, .rg .p { position:absolute; left:-46px; top:-46px; width:92px; height:92px; border-radius:50%; }
.rg .o { border:6px solid #d80609; box-shadow:0 0 18px rgba(216,6,9,0.9), inset 0 0 14px rgba(216,6,9,0.6), 0 0 0 2px rgba(255,255,255,0.7); opacity:0; }
.rg .p { border:4px solid #ff3b3b; opacity:0; }
.arw { position:absolute; left:0; top:0; width:0; height:0; }
.arw .sh2 { position:absolute; left:-170px; top:-9px; width:112px; height:18px; opacity:0; filter:drop-shadow(0 0 10px rgba(216,6,9,0.9)) drop-shadow(0 2px 4px rgba(0,0,0,0.8)); }
.arw .sh2 i { position:absolute; left:0; top:4px; width:84px; height:10px; background:#fff; border-radius:5px; }
.arw .sh2 b { position:absolute; left:76px; top:-8px; width:0; height:0; border-top:17px solid transparent; border-bottom:17px solid transparent; border-left:34px solid #fff; }
.mksub { position:absolute; left:60px; right:60px; top:96px; text-align:center; opacity:0; font-weight:800; font-size:32px; letter-spacing:0.04em; color:#fff;
  padding:16px 20px 14px; border-radius:12px; background:#d80609; }
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
            b = min([b] + [h0 for h0, _ in hide if a < h0])     # never run into a breakdown window
            id = f'c{gi}'
            spans = ' '.join(f'<span id="{id}w{k}">{E(w["text"])}</span>' for k, w in enumerate(g))
            self.body.append(f'<div class="cap" id="{id}" style="top:{y}px">{spans}</div>')
            self.js.append(f'tl.set("#{id}", {{ opacity:1 }}, {T(a)}); tl.fromTo("#{id}", {{ scale:0.86, y:14 }}, {{ scale:1, y:0, duration:{T(0.13)}, ease:"power3.out", immediateRender:false }}, {T(a)}); tl.set("#{id}", {{ opacity:0 }}, {T(b)});')
            for k, w in enumerate(g):
                we = g[k + 1]['start'] if k + 1 < len(g) else b
                self.js.append(f'tl.set("#{id}w{k}", {{ color:"{RED}" }}, {T(w["start"])}); tl.fromTo("#{id}w{k}", {{ scale:1.12 }}, {{ scale:1, duration:{T(0.16)}, ease:"power2.out", immediateRender:false }}, {T(w["start"])}); '
                               f'tl.set("#{id}w{k}", {{ color:"#ffffff" }}, {T(max(w["start"] + 0.05, we))});')

    def scope_flashes(self):
        """white flash + whoosh wherever the reel switches between the 16:9 band and the 9:16 crop"""
        t, prev = 0.0, None
        for sg in R['reels'][self.name]['segs']:
            wide = sg[2] == 'wide'
            if prev is not None and wide != prev: self.flash(t)
            prev = wide; t += (round(sg[1] * FPS) - round(sg[0] * FPS)) / FPS

    def stamp(self, card, t, text, dim='.chip'):
        """slam a red stamp onto a card and knock back its chips"""
        self.body[[i for i, b in enumerate(self.body) if f'id="{card}"' in b][0]] = self.body[[i for i, b in enumerate(self.body) if f'id="{card}"' in b][0]][:-6] + f'<div class="stamp">{E(text)}</div></div>'
        self.js.append(f'tl.to("#{card} {dim}", {{ opacity:0.3, duration:{T(0.2)}, ease:"power2.out" }}, {T(t)});')
        self.js.append(f'tl.fromTo("#{card} .stamp", {{ opacity:0, scale:1.8, rotation:-6, yPercent:-50 }}, {{ opacity:1, scale:1, rotation:-6, yPercent:-50, duration:{T(0.22)}, ease:"power4.in", immediateRender:false }}, {T(t + 0.05)});')
        self.sfx.append(('slam', t + 0.18, 0.28))

    def broll(self, id, t0, t1, kicker, title, calls, sub=None):
        """3D breakdown insert: Ash's cut-out freeze on a tilted card, numbered callouts land on the spoken word.
        calls: [(n, label, t, (px, py) point in still px, (lx, ly) label pos, side)]"""
        P = lambda x, y: (160 + (x - 600) * 0.8444, 470 + (y - 900) * 0.8444)
        lines, labs, dots = [], [], []
        for k, (num, text, t, pt, lp, side) in enumerate(calls):
            px, py = P(*pt); lx, ly = lp
            ey = ly + 36; ex = lx + 19 * len(text) + 100 if side == 'L' else lx
            lines.append(f'<line class="ln{k}" x1="{px:.0f}" y1="{py:.0f}" x2="{ex:.0f}" y2="{ey:.0f}" stroke="#fff" stroke-width="4" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>')
            dots.append(f'<div class="dot d{k}" style="left:{px - 13:.0f}px; top:{py - 13:.0f}px"><i></i></div>')
            labs.append(f'<div class="cl c{k} sh" style="left:{lx}px; top:{ly}px; "><b>{num}</b><span>{text}</span></div>')
            self.js.append(f"""tl.to("#{id} .ln{k}", {{ strokeDashoffset:0, duration:{T(0.3)}, ease:"power2.out" }}, {T(t)});
tl.fromTo("#{id} .d{k}", {{ scale:0 }}, {{ scale:1, duration:{T(0.3)}, ease:"back.out(3)", immediateRender:false }}, {T(t)});
tl.fromTo("#{id} .c{k}", {{ opacity:0, x:{30 if side == 'L' else -30} }}, {{ opacity:1, x:0, duration:{T(0.3)}, ease:"expo.out", immediateRender:false }}, {T(t + 0.15)});
tl.to("#{id} .d{k} i", {{ scale:2.4, opacity:0, duration:{T(0.9)}, ease:"power1.out", repeat:{max(0, int((t1 - t) / 0.9) - 1)} }}, {T(t + 0.3)});""")
            self.sfx.append(('click', t, 0.4))
        glows = ''.join(f'<div class="glow g{k}" style="left:{P(*pt)[0] - 280:.0f}px; top:{P(*pt)[1] - 590:.0f}px"></div>' for k, (_, _, _, pt, _, _) in enumerate(calls))
        for k, (_, _, t, _, _, _) in enumerate(calls):
            self.js.append(f'tl.fromTo("#{id} .g{k}", {{ opacity:0, scale:0.5 }}, {{ opacity:1, scale:1, duration:{T(0.4)}, ease:"power2.out", immediateRender:false }}, {T(t)});')
        sb = f'<div class="brsub sh">{sub[0]}</div>' if sub else ''
        self.body.append(f"""<div class="br" id="{id}"><div class="brbg"></div><div class="brgrid"></div>
<div class="brttl sh"><div class="kick"><i></i>{E(kicker)}</div><div class="clip"><div class="bb t">{title}</div></div></div>
<div class="brwrap"><div class="brcard"><img class="still" src="assets/still.jpg"><img class="fig" src="assets/fig.png">{glows}</div></div>
<svg class="brsvg" width="1080" height="1920">{''.join(lines)}</svg>{''.join(dots)}{''.join(labs)}{sb}</div>""")
        self.js.append(f"""tl.set("#{id}", {{ opacity:1 }}, {T(t0)});
tl.fromTo("#{id} .brbg, #{id} .brgrid", {{ opacity:0 }}, {{ opacity:1, duration:{T(0.25)}, ease:"power1.out", immediateRender:false }}, {T(t0)});
tl.fromTo("#{id} .brcard", {{ rotationY:62, rotationX:8, scale:0.72, z:-300, opacity:0 }}, {{ rotationY:-10, rotationX:3, scale:1, z:0, opacity:1, duration:{T(0.6)}, ease:"expo.out", immediateRender:false }}, {T(t0)});
tl.to("#{id} .brcard", {{ rotationY:6, rotationX:-2, duration:{T(max(0.5, t1 - t0 - 0.95))}, ease:"sine.inOut" }}, {T(t0 + 0.6)});
tl.fromTo("#{id} .brttl .t", {{ yPercent:105 }}, {{ yPercent:0, duration:{T(0.5)}, ease:"expo.out", immediateRender:false }}, {T(t0 + 0.15)});
tl.fromTo("#{id} .brttl .kick", {{ opacity:0, x:-20 }}, {{ opacity:1, x:0, duration:{T(0.35)}, ease:"power3.out", immediateRender:false }}, {T(t0 + 0.1)});
tl.fromTo("#{id} .brgrid", {{ backgroundPositionY:"0px" }}, {{ backgroundPositionY:"240px", duration:{T(t1 - t0)}, ease:"none", immediateRender:false }}, {T(t0)});""")
        if sub:
            self.js.append(f'tl.fromTo("#{id} .brsub", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:{T(0.35)}, ease:"back.out(1.8)", immediateRender:false }}, {T(sub[1])});')
            self.sfx.append(('pop', sub[1], 0.25))
        if t1 < self.dur - 0.05:
            self.js.append(f"""tl.to("#{id} .brcard", {{ rotationY:-70, scale:0.8, z:-200, opacity:0, duration:{T(0.32)}, ease:"power3.in" }}, {T(t1 - 0.32)});
tl.to("#{id}", {{ opacity:0, duration:{T(0.18)}, ease:"power1.in" }}, {T(t1 - 0.18)});""")
            self.sfx.append(('whoosh', t1 - 0.3, 0.3))
        self.sfx.append(('whoosh', t0 - 0.1, 0.32))

    def marks(self, id, t0, t1, kicker, title, calls, sub=None, pose=None, freeze=None):
        """live breakdown: red rings + arrows drawn straight onto the footage, following Ash's leg (Vision pose @12 fps).
        calls: [(n, label, t, pointfn(pose)->(x,y), (lx, ly) label pos, arrow angle deg or None)]
        freeze=(img, t): full-bleed freeze of the cut video at reel time t instead of live tracking"""
        rings, labs, lines = [], [], []
        def at(t):                                    # median-smoothed pose sample at reel time t
            i = min(max(int(round(t * 12)), 0), len(pose) - 1)
            win = [pose[j] for j in range(max(0, i - 2), min(len(pose), i + 3))]
            return {k: [sorted(p[k][c] for p in win if k in p)[len([p for p in win if k in p]) // 2] for c in (0, 1)]
                    for k in pose[i] if sum(k in p for p in win) >= 3} or pose[i]
        for k, (num, text, t, fn, lp, ang) in enumerate(calls):
            lx, ly = lp; ex, ey = lx + 21 * len(text) + 96, ly + 36
            arw = (f'<div class="arw" style="transform:rotate({ang}deg)"><div class="sh2"><i></i><b></b></div></div>' if ang is not None else '')
            rings.append(f'<div class="rg m{k}"><div class="o"></div><div class="p"></div>{arw}</div>')
            labs.append(f'<div class="cl c{k} sh" style="left:{lx}px; top:{ly}px; "><b>{num}</b><span>{text}</span></div>')
            lines.append(f'<line class="ln{k}" x1="{ex}" y1="{ey}" x2="{ex}" y2="{ey}" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity="0"/>')
            ts = [t] if freeze else [t + j / 12 for j in range(int((t1 - t) * 12) + 1)]
            for j, tt in enumerate(ts):
                x, y = fn(at(freeze[1] if freeze else tt))
                self.js.append(f'tl.set("#{id} .m{k}", {{ x:{x:.0f}, y:{y:.0f} }}, {T(tt)}); tl.set("#{id} .ln{k}", {{ attr:{{ x2:{x:.0f}, y2:{y:.0f} }} }}, {T(tt)});')
            self.js.append(f"""tl.set("#{id} .ln{k}", {{ attr:{{ opacity:1 }} }}, {T(t)});
tl.fromTo("#{id} .m{k} .o", {{ scale:2.2, opacity:0 }}, {{ scale:1, opacity:1, duration:{T(0.3)}, ease:"back.out(2.2)", immediateRender:false }}, {T(t)});
tl.fromTo("#{id} .m{k} .p", {{ scale:1, opacity:0.9 }}, {{ scale:2.1, opacity:0, duration:{T(0.85)}, ease:"power1.out", repeat:{max(0, int((t1 - t) / 0.85) - 1)}, immediateRender:false }}, {T(t + 0.25)});
tl.fromTo("#{id} .c{k}", {{ opacity:0, x:-30 }}, {{ opacity:1, x:0, duration:{T(0.3)}, ease:"expo.out", immediateRender:false }}, {T(t + 0.1)});""")
            if ang is not None:
                self.js.append(f"""tl.fromTo("#{id} .m{k} .arw .sh2", {{ opacity:0, x:-40 }}, {{ opacity:1, x:0, duration:{T(0.3)}, ease:"power3.out", immediateRender:false }}, {T(t + 0.15)});
tl.to("#{id} .m{k} .arw .sh2", {{ x:16, duration:{T(0.4)}, ease:"sine.inOut", yoyo:true, repeat:{max(1, int((t1 - t - 0.5) / 0.4)) | 1} }}, {T(t + 0.45)});""")
            self.sfx.append(('click', t, 0.4))
        fz = f'<img class="fz" src="assets/{freeze[0]}">' if freeze else ''
        sb = f'<div class="mksub sh">{sub[0]}</div>' if sub else ''
        self.body.append(f"""<div class="mk" id="{id}">{fz}<div class="mkvig"></div>
<div class="mkttl sh"><div class="kick"><i></i>{E(kicker)}</div><div class="clip"><div class="bb t">{title}</div></div></div>
<svg class="brsvg" width="1080" height="1920">{''.join(lines)}</svg>{''.join(rings)}{''.join(labs)}{sb}</div>""")
        self.js.append(f"""tl.set("#{id}", {{ opacity:1 }}, {T(t0)});
tl.fromTo("#{id} .mkvig", {{ opacity:0 }}, {{ opacity:1, duration:{T(0.3)}, ease:"power1.out", immediateRender:false }}, {T(t0)});
tl.fromTo("#{id} .mkttl .t", {{ yPercent:105 }}, {{ yPercent:0, duration:{T(0.5)}, ease:"expo.out", stagger:{T(0.08)}, immediateRender:false }}, {T(t0 + 0.1)});
tl.fromTo("#{id} .mkttl .kick", {{ opacity:0, x:-20 }}, {{ opacity:1, x:0, duration:{T(0.35)}, ease:"power3.out", immediateRender:false }}, {T(t0 + 0.05)});""")
        if freeze:
            self.js.append(f'tl.fromTo("#{id} .fz", {{ scale:1.0 }}, {{ scale:1.05, duration:{T(t1 - t0)}, ease:"none", transformOrigin:"50% 70%", immediateRender:false }}, {T(t0)});')
            self.flash(t0)
        if sub:
            self.js.append(f'tl.fromTo("#{id} .mksub", {{ opacity:0, y:-20 }}, {{ opacity:1, y:0, duration:{T(0.35)}, ease:"back.out(1.8)", immediateRender:false }}, {T(sub[1])});')
            self.sfx.append(('pop', sub[1], 0.25))
        if t1 < self.dur - 0.05:
            self.js.append(f'tl.to("#{id}", {{ opacity:0, duration:{T(0.22)}, ease:"power1.in" }}, {T(t1 - 0.22)});')
        self.sfx.append(('whoosh', t0 - 0.1, 0.3))

    def write(self):
        self.scope_flashes()
        d = f'{ROOT}/comps/{self.name}'; os.makedirs(d + '/assets', exist_ok=True)
        open(f'{d}/index.html', 'w').write(HEAD.replace('%DUR%', f'{self.dur * K:.3f}').replace('%BODY%', '\n'.join(self.body))
                                           .replace('%JS%', '\n'.join(self.js)).replace('%CSS%', '\n'.join(self.css))
                                           .replace('%W%', str(W)).replace('%H%', str(H)).replace('%S%', str(SCALE)))
        shutil.copy(HFJSON, d); shutil.copy(GSAP, d + '/assets/')
        for f, n in getattr(self, 'assets', []): shutil.copy(f, f'{d}/assets/{n}')
        open(f'{d}/meta.json', 'w').write(json.dumps({"id": self.name, "name": self.name, "width": W, "height": H, "fps": 24}))
        json.dump(sorted(self.sfx, key=lambda s: s[1]), open(f'{ROOT}/sfx_{self.name}.json', 'w'))
        print('wrote', self.name, len(self.body), 'elements', len(self.sfx), 'sfx')


# --------------------------------------------------------------------- words
CENSOR = {'fucking': 'f*cking', "cunt's": "c*nt's", 'shit': 'sh*t'}
def load_words(name, fixes=(), drop=(), add=()):
    d = json.load(open(f'{PROJ}/src/rt/{name}.json')); d = d if isinstance(d, list) else d['words']
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
    return R['reels'][name].get('hold', 0) + sum(round(sg[1] * FPS) - round(sg[0] * FPS) for sg in R['reels'][name]['segs']) / FPS



STILL = PROJ + '/gfx/broll/still-172.5.jpg'; FIG = PROJ + '/gfx/broll/ash-legs.png'
KNEE, HAM, TOES, GLUTE = (990, 1528), (1067, 1360), (1190, 1890), (1120, 1173)

# ============================================================ 1. prep isn't always 3,500 calories
n = 'prep-isnt-3500'; r = Reel(n, dur(n))
wd = load_words(n, add=[('Prep', 0.0, 0.0)])
wd = [w for w in wd if w['raw'] != 'Hey,']
wd[0]['start'], wd[0]['end'], wd[1]['start'] = 0.03, 0.24, 0.26     # 'Prep' (missed by whisper), 'for'
for w in wd:
    if w['raw'] == '500-gram': w['text'] = '500G'
    if w['raw'] == 'cheap': w['text'] = 'cheat'
f = lambda t, a=0.0: find(wd, t, a)
r.hook('h1', 0.08, 1.74, 'CONTEST PREP', ['PREP ISN’T ALWAYS', '<span class="r">3,500 CALORIES</span>'])
items = [('3,500 KCAL', f('three'), ''), ('500G CARBS', f('500G'), ''), ('8,000 STEPS', f('8,000'), '')]
r.card('k1', f('blessed') - 0.2, f('mean', 7.0) + 0.2, 'SOME PEOPLE ARE BLESSED', 'PREP ON <span class="r">EASY MODE</span>', inner=r.chips(items), size=84)
r.chip_js('k1', items)
r.stamp('k1', f('ain\'t') - 0.1, 'NOT EVERYONE')
r.card('k2', f('do', 8.5) - 0.15, f('it\'s', 12.0) - 0.1, 'YOUR PREP, YOUR RULES', 'DO WHAT <span class="r">YOU</span> HAVE TO DO', size=80)
CUT = (16.58, 17.26)     # 'f*cking, this c*nt's' cut from the dialogue (reels.json seg 4 split) -> drop + pull later words back
wd = [w for w in wd if not CUT[0] - 0.25 <= w['start'] < CUT[1]]     # whisper puts 'fucking' at 16.39; audio has it at 16.64
for w in wd:
    if w['start'] >= CUT[1]: w['start'] -= CUT[1] - CUT[0]; w['end'] -= CUT[1] - CUT[0]
wd = [w for w in wd if w['start'] < 19.95 - (CUT[1] - CUT[0])]     # reel ends on "...do you know what I mean?" before the stress line
r.card('k3', f('social') - 0.3, r.dur, 'WHAT YOU SEE ON SOCIAL MEDIA', 'CHEAT MEAL <span class="r">EVERY WEEK</span>', size=80)
r.strike('s3', 'k3', f('them') - 0.25, 40, 640, 96, stamp='THAT’S THEM')
r.captions(wd)
r.write()

# ============================================================ 2. side leg pose — the hamstring drop
n = 'side-leg-pose'; r = Reel(n, dur(n)); r.assets = [(PROJ + '/gfx/freeze/recap.jpg', 'recap.jpg')]
POSE = json.load(open(PROJ + '/src/pose-side-leg.json'))       # Vision leg joints of the cut video @12 fps (scripts/pose)
L = lambda p, k: (p[k][0] * 1080, p[k][1] * 1920)
def knees(p): return sorted([L(p, 'lKnee'), L(p, 'rKnee')])                    # [front, back] — Ash faces frame-left
def ankles(p): return sorted([L(p, 'lAnkle'), L(p, 'rAnkle')])
def glute(p): x, y = L(p, 'lHip') if p['lHip'][0] > p.get('rHip', [0])[0] else L(p, 'rHip'); return (x + 60, y + 55)
BACK_KNEE = lambda p: knees(p)[1]
HAM = lambda p: ((knees(p)[1][0] + glute(p)[0]) / 2 + 30, (knees(p)[1][1] + glute(p)[1]) / 2)
TOES = lambda p: (ankles(p)[0][0] - 100, ankles(p)[0][1] + 85)
GLUTE = glute
wd = load_words(n, add=[('imagine', 18.02, 18.25)])
f = lambda t, a=0.0: find(wd, t, a)
END = f('time', 27.0) + 0.45
r.hook('h1', 0.06, 1.42, 'POSING TIP', ['THE SIDE LEG', '<span class="r">HAMSTRING DROP</span>'])
r.card('k1', 1.55, f('so', 4.8) - 0.05, 'THE PROBLEM', 'HARD TO HOLD THE <span class="r">GLUTE</span>', sub='…and hit the pose at the same time', size=78)
items = [('HAMSTRING DROP', f('hamstring'), '=')]
r.card('k2', f('so', 4.8), f('look', 9.5) - 0.15, 'THE FIX', 'SQUEEZE <span class="r">THIS KNEE</span>', inner=r.chips(items), size=92)
r.chip_js('k2', items)
B1 = (f('look', 9.5) - 0.1, f('drop', 13.0) + 0.45)
r.marks('b1', B1[0], B1[1], 'WATCH THE LEG', 'THE <span class="r">HAMSTRING DROP</span>',
        [(1, 'BACK KNEE IN', f('pushed'), BACK_KNEE, (40, 1300), 180), (2, 'HAMSTRING DROP', f('extra'), HAM, (40, 1180), 90)],
        sub=('PUSH THE BACK KNEE INTO THE FRONT LEG', f('pushed') + 0.3), pose=POSE)
r.card('k3', B1[1] + 0.05, f('driving') - 0.25, 'THEN', 'PLANT IT <span class="r">ON THERE</span>', size=92)
B2 = (f('driving') - 0.12, f('toe') + 0.4)
r.marks('b2', B2[0], B2[1], 'THEN', 'DRIVE THE <span class="r">TOES</span>',
        [(3, 'DRIVE THE TOES', f('tiptoes'), TOES, (40, 1560), 90)],
        sub=('LIKE THE START OF A LEG EXTENSION', f('leg', 19.0)), pose=POSE)
items = [('HAMSTRING', f("hamstring's"), '✓'), ('QUADS', f('quads'), '✓'), ('GLUTE', f('glute', 24.0), '✓')]
r.card('k4', B2[1] + 0.05, END - 0.1, 'THEN', 'LOCK IT <span class="r">ALL IN</span>', inner=r.chips(items), size=92)
r.chip_js('k4', items)
r.marks('b3', END, r.dur, 'LITTLE THINGS, BIG DIFFERENCE', 'THE <span class="r">SIDE LEG</span> CUES',
        [(4, 'SQUEEZE THE GLUTE', END + 0.3, GLUTE, (40, 900), None), (2, 'HAMSTRING DROP', END + 0.55, HAM, (40, 1180), 90),
         (1, 'BACK KNEE IN', END + 0.8, BACK_KNEE, (40, 1300), 180), (3, 'DRIVE THE TOES', END + 1.05, TOES, (40, 1560), 90)],
        pose=POSE, freeze=('recap.jpg', 12.5))
r.captions(wd, hide=[B1, B2, (END, r.dur)])
r.write()
