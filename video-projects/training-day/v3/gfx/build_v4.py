"""v4 overlays — show day / meal prep / supplements section (clips 0027-0024 after the drive B-roll).
Reuses HEAD + page() from build_v3 (same editorial style). Times are local to each overlay; placement in place_v4."""
import json, shutil, os

src = open('build_v3.py').read()
exec(src[:src.index('# ---------- LEG DAY opener')])
made.clear()
POST = '../../../shows-clash/assets/'

# ---------- show day roster (clip 0027, starts at clip t=15.0) ----------
SD = 34.0
css = """
#pn { position:absolute; right:40px; top:56px; width:560px; padding:26px 30px 30px 60px; border-radius:14px;
  background:linear-gradient(270deg, rgba(5,8,12,0.86) 0%, rgba(5,8,12,0.74) 78%, rgba(5,8,12,0) 100%); }
#pn .k { font-weight:800; font-size:20px; letter-spacing:0.4em; color:#ff3b30; }
#pn .h { font-family:"Bebas Neue", sans-serif; font-size:78px; line-height:0.9; margin-top:6px; }
#pn .rule { width:120px; height:3px; background:#ff3b30; margin:12px 0 18px; transform-origin:0 50%; }
.row { display:flex; align-items:center; gap:18px; margin-top:14px; }
.row .th { flex:none; width:84px; height:84px; border-radius:8px; overflow:hidden; border:2px solid rgba(255,255,255,0.85); }
.row .th img { width:100%; height:100%; object-fit:cover; object-position:50% 30%; display:block; }
.row .th.txt { display:flex; align-items:center; justify-content:center; text-align:center; font-weight:800; font-size:18px; line-height:1.1;
  letter-spacing:0.08em; background:#e0302a; }
.row .nm { font-family:"Bebas Neue", sans-serif; font-size:54px; line-height:0.92; }
.row .sb { font-weight:700; font-size:19px; letter-spacing:0.12em; margin-top:4px; color:#e9e9e9; }
.row .sb b { color:#ff3b30; } .row.pca .sb b { color:#6f93ff; } .row.pca .th { border-color:#3f6cf0; }
.row.ath { margin-top:10px; padding-left:102px; } .row.ath .nm { font-size:48px; }
.row.ath .sb { display:inline-block; margin:0 0 0 14px; }
"""
body = f"""<div id="pn" class="shadow"><div class="k">SHOW DAY · SAT 17 OCT</div><div class="h">4 ATHLETES · 3 SHOWS</div><div class="rule"></div>
<div class="row" id="r1"><div class="th txt">NPC<br>USA</div><div><div class="nm">DANIELLA</div><div class="sb"><b>NPC</b> · WELLNESS · USA</div></div></div>
<div class="row pca" id="r2"><div class="th"><img src="assets/pca.jpg"/></div><div><div class="nm">KATKA</div><div class="sb"><b>PCA BRITISH FINALS</b></div><div class="sb">MASTERS BIKINI</div></div></div>
<div class="row" id="r3"><div class="th"><img src="assets/tbjp.jpg"/></div><div><div class="nm" style="font-size:44px">TBJP INTERNATIONAL BRITISH FINALS</div><div class="sb"><b>2 BROS PRO QUALIFIER</b></div><div class="sb">LIFE CENTRE · BRADFORD</div></div></div>
<div class="row ath" id="r4"><div class="nm">RACHEL</div><div class="sb">· FIT MODEL</div></div>
<div class="row ath" id="r5"><div class="nm">GABRIELLA</div><div class="sb">· BIKINI</div></div></div>"""
def rin(sel, t, ease="expo.out"):
    return f'tl.fromTo("{sel}", {{ opacity:0, x:40 }}, {{ opacity:1, x:0, duration:f(0.45), ease:"{ease}", immediateRender:false }}, f({t}));\n'
js = ('gsap.set(["#pn","#r1","#r2","#r3","#r4","#r5"], { opacity:0 });\n'
      'tl.fromTo("#pn", { opacity:0, x:60 }, { opacity:1, x:0, duration:f(0.5), ease:"expo.out", immediateRender:false }, f(0.6));\n'
      'tl.fromTo("#pn .rule", { scaleX:0 }, { scaleX:1, duration:f(0.4), ease:"power3.inOut", immediateRender:false }, f(0.9));\n'
      + rin('#r1', 8.1) + rin('#r2', 15.3, 'back.out(1.4)') + rin('#r3', 20.0) + rin('#r4', 26.1, 'power3.out') + rin('#r5', 27.6, 'power3.out') +
      f'tl.to("#pn", {{ opacity:0, x:40, duration:f(0.4), ease:"power2.in" }}, f({SD - 0.5}));')
page('v4-shows', SD, body, js, css)
for p in ('tbjp.jpg', 'pca.jpg'): shutil.copy(POST + p, f'comps/v4-shows/assets/{p}')

# ---------- microwave rice top tip (clip 0030, starts at clip t=1.5) ----------
TD = 22.0
css = """
#tp { position:absolute; left:52px; top:44px; width:680px; padding:24px 110px 28px 32px; border-radius:12px;
  background:linear-gradient(90deg, rgba(0,0,0,0.80) 0%, rgba(0,0,0,0.68) 72%, rgba(0,0,0,0) 100%); }
#tp .lbl { font-weight:800; font-size:20px; letter-spacing:0.4em; color:#ff3b30; }
#tp .h { font-family:"Bebas Neue", sans-serif; font-size:82px; line-height:0.9; margin-top:6px; }
#tp .st { display:flex; gap:16px; align-items:baseline; margin-top:14px; font-weight:700; font-size:30px; line-height:1.2; }
#tp .st .n { font-family:"Bebas Neue"; font-size:48px; color:#ff3b30; flex:none; width:26px; }
#tp .st u { text-decoration:none; background:linear-gradient(transparent 62%, rgba(255,59,48,0.75) 62%); }
"""
body = """<div id="tp" class="shadow"><div class="lbl">TOP TIP</div><div class="h">MICROWAVE RICE</div>
<div class="st" id="s1"><div class="n">1</div><div>Microwave the pouch as normal</div></div>
<div class="st" id="s2"><div class="n">2</div><div>Open it, add a <u>splash of water</u> &amp; stir</div></div>
<div class="st" id="s3"><div class="n">3</div><div>Let it sit <u>~1 minute</u>, far more moist</div></div></div>"""
js = ('gsap.set(["#tp","#s1","#s2","#s3"], { opacity:0 });\n'
      'tl.fromTo("#tp", { opacity:0, x:-50 }, { opacity:1, x:0, duration:f(0.45), ease:"expo.out", immediateRender:false }, f(1.6));\n'
      'tl.fromTo("#s1", { opacity:0, y:14 }, { opacity:1, y:0, duration:f(0.35), ease:"power2.out", immediateRender:false }, f(5.8));\n'
      'tl.fromTo("#s2", { opacity:0, y:14 }, { opacity:1, y:0, duration:f(0.35), ease:"back.out(1.6)", immediateRender:false }, f(8.6));\n'
      'tl.fromTo("#s3", { opacity:0, y:14 }, { opacity:1, y:0, duration:f(0.35), ease:"power3.out", immediateRender:false }, f(15.2));\n'
      f'tl.to("#tp", {{ opacity:0, x:-30, duration:f(0.3), ease:"power2.in" }}, f({TD - 0.4}));')
page('v4-tip', TD, body, js, css)

# ---------- logged-meal food diary (clip 0034, starts at clip t=13.3) ----------
# per-100g / per-egg label values: Tesco British Beef Rump Steak 171kcal P20.3 F10.0 C0; Jason's Great White sourdough
# 237kcal P9.7 F0.7 C46.4; Tesco Very Large free-range egg (69g) 91kcal P8.7 F6.2 C<0.1
F = [('Tesco British Beef Rump Steak', '255 g', 255 * 1.71, 255 * .203, 0.0, 255 * .100),
     ("Jason's Sourdough The Great White", '200 g', 200 * 2.37, 200 * .097, 200 * .464, 200 * .007),
     ('Tesco Free Range Eggs, Very Large', '3 eggs', 3 * 91, 3 * 8.7, 0.3, 3 * 6.2)]
TK = sum(x[2] for x in F); TP = sum(x[3] for x in F); TC = sum(x[4] for x in F); TF = sum(x[5] for x in F)
MD = 29.0
css = """
#ph { position:absolute; right:110px; top:70px; width:500px; border-radius:42px; background:#111; padding:14px; transform:rotate(-2.5deg);
  box-shadow:0 30px 80px rgba(0,0,0,0.6); }
#sc { border-radius:30px; overflow:hidden; background:#f2f3f5; color:#1d2129; font-family:Montserrat, sans-serif; }
#sc .sbar { display:flex; justify-content:space-between; padding:14px 26px 6px; font-weight:700; font-size:17px; }
#sc .top { background:#1b6ef3; color:#fff; padding:16px 22px 18px; }
#sc .top .t { font-weight:800; font-size:26px; } #sc .top .d { font-weight:600; font-size:17px; opacity:0.85; margin-top:2px; }
#sc .rem { display:flex; justify-content:space-between; margin-top:14px; font-weight:700; font-size:15px; text-align:center; }
#sc .rem b { display:block; font-size:24px; font-weight:800; }
#sc .sec { display:flex; justify-content:space-between; padding:16px 22px 10px; font-weight:800; font-size:21px; }
#sc .sec span { color:#1b6ef3; }
#sc .it { background:#fff; margin:0 0 2px; padding:14px 22px; display:flex; justify-content:space-between; align-items:center; }
#sc .it .n { font-weight:700; font-size:18px; line-height:1.2; max-width:330px; } #sc .it .q { font-weight:500; font-size:15px; color:#6b7280; margin-top:3px; }
#sc .it .k { font-weight:800; font-size:20px; }
#sc .add { padding:12px 22px 16px; font-weight:800; font-size:16px; color:#1b6ef3; letter-spacing:0.06em; }
#sc .mac { background:#fff; margin-top:6px; padding:18px 22px 22px; }
#sc .mac .ttl { display:flex; justify-content:space-between; font-weight:800; font-size:19px; }
#sc .mac .ttl b { font-size:30px; }
#sc .bars { display:flex; gap:14px; margin-top:14px; }
#sc .bar { flex:1; } #sc .bar .l { font-weight:700; font-size:14px; color:#6b7280; } #sc .bar .v { font-weight:800; font-size:24px; margin-top:2px; }
#sc .bar .tr { height:8px; border-radius:4px; background:#e5e7eb; margin-top:6px; overflow:hidden; }
#sc .bar .fl { height:100%; border-radius:4px; transform-origin:0 50%; }
"""
pct = lambda g, kc: round(g * kc / (TP * 4 + TC * 4 + TF * 9) * 100)
items = ''.join(f'<div class="it" id="i{j}"><div><div class="n">{n}</div><div class="q">{q}</div></div><div class="k">{round(k)}</div></div>'
                for j, (n, q, k, *_r) in enumerate(F))
body = f"""<div id="ph"><div id="sc"><div class="sbar"><span>08:42</span><span>●●●  ▮</span></div>
<div class="top"><div class="t">Food Diary</div><div class="d">Saturday 17 October · Show day</div></div>
<div class="sec">Breakfast<span id="bk">0</span></div>{items}<div class="add">+ ADD FOOD</div>
<div class="mac" id="mc"><div class="ttl"><span>Meal total</span><b><span id="tk">{round(TK):,}</span> kcal</b></div>
<div class="bars"><div class="bar"><div class="l">PROTEIN</div><div class="v">{round(TP)}g</div><div class="tr"><div class="fl" style="background:#1b6ef3;width:{pct(TP,4)}%"></div></div></div>
<div class="bar"><div class="l">CARBS</div><div class="v">{round(TC)}g</div><div class="tr"><div class="fl" style="background:#10b981;width:{pct(TC,4)}%"></div></div></div>
<div class="bar"><div class="l">FAT</div><div class="v">{round(TF)}g</div><div class="tr"><div class="fl" style="background:#f59e0b;width:{pct(TF,9)}%"></div></div></div></div></div>
</div></div>"""
cum = [round(sum(x[2] for x in F[:j + 1])) for j in range(3)]
js = ('gsap.set(["#ph","#i0","#i1","#i2","#mc"], { opacity:0 });\n'
      'tl.fromTo("#ph", { opacity:0, y:80, rotation:4 }, { opacity:1, y:0, rotation:-2.5, duration:f(0.55), ease:"back.out(1.3)", immediateRender:false }, f(0.2));\n')
for j, t in enumerate((2.6, 6.4, 8.6)):
    js += (f'tl.fromTo("#i{j}", {{ opacity:0, x:40, backgroundColor:"#dbeafe" }}, {{ opacity:1, x:0, duration:f(0.4), ease:"power3.out", immediateRender:false }}, f({t}));\n'
           f'tl.to("#i{j}", {{ backgroundColor:"#ffffff", duration:f(0.8) }}, f({t}+0.5));\n'
           f'tl.set("#bk", {{ textContent:"{cum[j]:,}" }}, f({t}+0.2));\n')
js += ('tl.fromTo("#mc", { opacity:0, y:20 }, { opacity:1, y:0, duration:f(0.45), ease:"expo.out", immediateRender:false }, f(17.1));\n'
       'tl.fromTo("#mc .fl", { scaleX:0 }, { scaleX:1, duration:f(0.7), ease:"power2.out", stagger:0.12, immediateRender:false }, f(17.3));\n'
       f'tl.to("#ph", {{ opacity:0, y:60, duration:f(0.4), ease:"power2.in" }}, f({MD - 0.5}));')
page('v4-macros', MD, body, js, css)

# ---------- tbJP site + code (clip 0024, as the JP range is introduced) ----------
CD = 12.0
css = """
#cd { position:absolute; left:52px; bottom:64px; padding:26px 150px 28px 36px; border-radius:14px; border-left:6px solid #ff3b30;
  background:linear-gradient(90deg, rgba(0,0,0,0.84) 0%, rgba(0,0,0,0.72) 66%, rgba(0,0,0,0) 100%); box-shadow:0 0 40px 10px rgba(0,0,0,0.25); }
#cd .top { display:flex; align-items:center; gap:20px; }
#cd .top img { height:58px; display:block; }
#cd .top .bar { width:2px; height:44px; background:rgba(255,255,255,0.45); }
#cd .lbl { font-weight:800; font-size:21px; letter-spacing:0.38em; color:#ff3b30; }
#cd .code { font-family:"Bebas Neue", sans-serif; font-size:132px; line-height:0.88; margin-top:12px; letter-spacing:0.02em; }
#cd .code span { color:#ff3b30; }
#cd .web { display:flex; align-items:center; gap:14px; margin-top:12px; }
#cd .web small { font-family:Montserrat; font-weight:700; font-size:19px; letter-spacing:0.22em; color:#cfcfcf; }
#cd .web b { font-family:"Bebas Neue", sans-serif; font-weight:400; font-size:56px; line-height:1; letter-spacing:0.05em; padding:4px 14px 0; border:2px solid rgba(255,255,255,0.85); border-radius:6px; }
"""
body = ('<div id="cd" class="shadow"><div class="top"><img src="assets/tbjp-logo.png"/><div class="bar"></div><div class="lbl">DISCOUNT CODE</div></div>'
        '<div class="code">ASH<span>10</span></div><div class="web"><small>SHOP AT</small><b>TB-JP.COM</b></div></div>')
js = f"""gsap.set(["#cd","#cd .top img","#cd .web"], {{ opacity:0 }});
tl.fromTo("#cd", {{ opacity:0, x:-50 }}, {{ opacity:1, x:0, duration:f(0.45), ease:"expo.out", immediateRender:false }}, f(0.15));
tl.fromTo("#cd .top img", {{ opacity:0, scale:0.7, transformOrigin:"0% 50%" }}, {{ opacity:1, scale:1, duration:f(0.4), ease:"back.out(2)", immediateRender:false }}, f(0.3));
tl.fromTo("#cd .code", {{ scale:1.3, transformOrigin:"0% 50%" }}, {{ scale:1, duration:f(0.4), ease:"back.out(2)", immediateRender:false }}, f(0.35));
tl.fromTo("#cd .web", {{ opacity:0, y:14 }}, {{ opacity:1, y:0, duration:f(0.4), ease:"power3.out", immediateRender:false }}, f(0.85));
tl.to("#cd", {{ opacity:0, x:-30, duration:f(0.3), ease:"power2.in" }}, f({CD - 0.4}));"""
page('v4-code', CD, body, js, css)
shutil.copy('../../../vitamin-c-reel/assets/brand/tbjp-logo.png', 'comps/v4-code/assets/tbjp-logo.png')

print(made, 'meal', round(TK), round(TP, 1), round(TC, 1), round(TF, 1), [round(x[2]) for x in F])
