"""Kart spins reel overlays: CoD-style hitmarker + GTA-style WASTED. 1080x1920 alpha MOVs for Resolve V2/V3."""
import json, os, shutil
SRC = '../../training-day/gfx'
HEAD = """<!doctype html><html lang="en"><head><meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" /><script src="assets/gsap.min.js"></script>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:1080px; height:1920px; overflow:hidden; background:transparent; }
#root { position:relative; width:1080px; height:1920px; overflow:hidden; }
%CSS%
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%DUR%" data-width="1080" data-height="1920">%BODY%</div>
<script>(() => { const tl = gsap.timeline({ paused:true });
%JS%
tl.to({}, { duration:%DUR% }, 0); window.__timelines = window.__timelines || {}; window.__timelines["main"] = tl; })();</script>
</body></html>"""
def page(name, dur, body, js, css):
    d = f'comps/{name}'; os.makedirs(d, exist_ok=True)
    open(f'{d}/index.html', 'w').write(HEAD.replace('%DUR%', str(dur)).replace('%BODY%', body).replace('%JS%', js).replace('%CSS%', css))
    shutil.copy(f'{SRC}/hyperframes.json', d)
    open(f'{d}/meta.json', 'w').write(json.dumps({"id": name, "name": name, "width": 1080, "height": 1920, "fps": 30}))
    os.makedirs(f'{d}/assets', exist_ok=True); shutil.copy(f'{SRC}/assets/gsap.min.js', f'{d}/assets/')

# ---- hitmarker: four short white diagonals pointing at screen centre ----
css = """
#hm { position:absolute; left:540px; top:960px; width:0; height:0; }
.l { position:absolute; left:-5px; top:-74px; width:10px; height:46px; background:#fff; border-radius:2px;
     box-shadow:0 0 0 2px rgba(0,0,0,0.55), 0 0 10px rgba(0,0,0,0.5); transform-origin:5px 74px; }
"""
body = '<div id="hm">' + ''.join(f'<div class="l" style="transform:rotate({a}deg)"></div>' for a in (45, 135, 225, 315)) + '</div>'
js = """gsap.set("#hm", { scale:1.45, opacity:1 });
tl.to("#hm", { scale:1, duration:0.07, ease:"power2.out" }, 0);
tl.to("#hm", { opacity:0, duration:0.14, ease:"power1.in" }, 0.24);"""
page('hitmarker', 0.4, body, js, css)

# ---- WASTED: dark band + big red text, slams in and creeps ----
css = """
#band { position:absolute; left:0; right:0; top:820px; height:280px;
  background:linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.62) 22%, rgba(0,0,0,0.62) 78%, rgba(0,0,0,0) 100%); }
#w { position:absolute; left:0; right:0; top:832px; text-align:center; font-family:"Bebas Neue", sans-serif; font-size:250px; line-height:1;
  letter-spacing:0.06em; color:#c8161d; -webkit-text-stroke:5px #000; paint-order:stroke fill;
  text-shadow:0 6px 0 #000, 0 0 40px rgba(0,0,0,0.6); }
"""
body = '<div id="band"></div><div id="w">WASTED</div>'
js = """gsap.set("#band", { opacity:0 }); gsap.set("#w", { opacity:0, scale:1.6 });
tl.to("#band", { opacity:1, duration:0.15, ease:"power1.out" }, 0);
tl.to("#w", { opacity:1, scale:1, duration:0.16, ease:"power3.in" }, 0.02);
tl.to("#w", { scale:1.05, duration:1.7, ease:"none" }, 0.18);"""
page('wasted', 1.9, body, js, css)
page('wasted_long', 2.5, body, js.replace('duration:1.7','duration:2.3'), css)
print('ok')
