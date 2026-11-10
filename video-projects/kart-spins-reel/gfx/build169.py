"""16:9 overlays (1920x1080 alpha MOVs): hitmarker, red death flash, WASTED + skulls."""
import json, os, shutil
SRC = '../../training-day/gfx'
HEAD = """<!doctype html><html lang="en"><head><meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" /><script src="assets/gsap.min.js"></script>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:1920px; height:1080px; overflow:hidden; background:transparent; }
#root { position:relative; width:1920px; height:1080px; overflow:hidden; }
%CSS%
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%DUR%" data-width="1920" data-height="1080">%BODY%</div>
<script>(() => { const tl = gsap.timeline({ paused:true });
%JS%
tl.to({}, { duration:%DUR% }, 0); window.__timelines = window.__timelines || {}; window.__timelines["main"] = tl; })();</script>
</body></html>"""
def page(name, dur, body, js, css):
    d = f'comps169/{name}'; os.makedirs(d, exist_ok=True)
    open(f'{d}/index.html', 'w').write(HEAD.replace('%DUR%', str(dur)).replace('%BODY%', body).replace('%JS%', js).replace('%CSS%', css))
    shutil.copy(f'{SRC}/hyperframes.json', d)
    open(f'{d}/meta.json', 'w').write(json.dumps({"id": name, "name": name, "width": 1920, "height": 1080, "fps": 30}))
    os.makedirs(f'{d}/assets', exist_ok=True); shutil.copy(f'{SRC}/assets/gsap.min.js', f'{d}/assets/')

# hitmarker: four white diagonals around frame centre
css = """
#hm { position:absolute; left:960px; top:540px; width:0; height:0; }
.l { position:absolute; left:-5px; top:-70px; width:10px; height:44px; background:#fff; border-radius:2px;
     box-shadow:0 0 0 2px rgba(0,0,0,0.55), 0 0 10px rgba(0,0,0,0.5); transform-origin:5px 70px; }
"""
body = '<div id="hm">' + ''.join(f'<div class="l" style="transform:rotate({a}deg)"></div>' for a in (45, 135, 225, 315)) + '</div>'
js = """gsap.set("#hm", { scale:1.45, opacity:1 });
tl.to("#hm", { scale:1, duration:0.07, ease:"power2.out" }, 0);
tl.to("#hm", { opacity:0, duration:0.14, ease:"power1.in" }, 0.24);"""
page('hitmarker', 0.4, body, js, css)

# red death flash: soft red wash + heavier red edges, quick in, long fade
css = """
#wash { position:absolute; inset:0; background:rgba(190,0,0,0.22); }
#edge { position:absolute; inset:0; background:radial-gradient(ellipse 75% 70% at 50% 50%, rgba(170,0,0,0) 35%, rgba(170,0,0,0.45) 75%, rgba(120,0,0,0.78) 100%); }
"""
body = '<div id="wash"></div><div id="edge"></div>'
js = """gsap.set(["#wash","#edge"], { opacity:0 });
tl.to(["#wash","#edge"], { opacity:1, duration:0.06, ease:"power2.out" }, 0);
tl.to("#wash", { opacity:0, duration:0.55, ease:"power2.out" }, 0.1);
tl.to("#edge", { opacity:0, duration:0.85, ease:"power1.out" }, 0.15);"""
page('redflash', 1.0, body, js, css)

# WASTED + skull emojis
css = """
#band { position:absolute; left:0; right:0; top:420px; height:240px;
  background:linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.62) 22%, rgba(0,0,0,0.62) 78%, rgba(0,0,0,0) 100%); }
#row { position:absolute; left:0; right:0; top:428px; height:224px; display:flex; align-items:center; justify-content:center; gap:44px; }
#w { font-family:"Bebas Neue", sans-serif; font-size:220px; line-height:1; letter-spacing:0.06em; color:#c8161d;
  -webkit-text-stroke:5px #000; paint-order:stroke fill; text-shadow:0 6px 0 #000, 0 0 40px rgba(0,0,0,0.6); padding-top:14px; }
@font-face { font-family:'Apple Color Emoji'; src: local('Apple Color Emoji'); }
.sk { font-family:"Apple Color Emoji", sans-serif; font-size:130px; line-height:1; filter:drop-shadow(0 6px 10px rgba(0,0,0,0.7)); }
"""
body = '<div id="band"></div><div id="row"><span class="sk" id="s1">☠️</span><div id="w">WASTED</div><span class="sk" id="s2">☠️</span></div>'
def wjs(hold):
    return f"""gsap.set("#band", {{ opacity:0 }}); gsap.set("#w", {{ opacity:0, scale:1.6 }}); gsap.set(".sk", {{ opacity:0, scale:0.2, rotation:-25 }});
tl.to("#band", {{ opacity:1, duration:0.15, ease:"power1.out" }}, 0);
tl.to("#w", {{ opacity:1, scale:1, duration:0.16, ease:"power3.in" }}, 0.02);
tl.to(".sk", {{ opacity:1, scale:1, rotation:0, duration:0.32, ease:"back.out(2.2)", stagger:0.06 }}, 0.2);
tl.to("#row", {{ scale:1.05, duration:{hold}, ease:"none" }}, 0.18);"""
page('wasted', 1.9, body, wjs(1.7), css)
page('wasted_long', 2.5, body, wjs(2.3), css)
print('ok')
