"""HKC Instagram story (9:16, 15 s): darkened reel shots behind an HKC promo card, with an empty slot + arrow
where Ash drops the IG link sticker to the full YouTube race. Reuses the 4K reel shots in pieces-final/.
IG story safe zones: nothing important in the top/bottom 250 px (layout px) — reply bar + profile header.
usage: story.py gfx | video [out.mp4]"""
import os, shutil, subprocess, sys
import gfx as G
R = os.path.dirname(os.path.abspath(__file__)); os.chdir(R)
D = R + '/story-gfx'
DUR, XF = 15.0, 0.35
SHOTS = ['hook', 'p1', 'spin', 'lunge', 'gone', 'fin', 'green']     # cycled under the card, cross-faded

CSS = """
#slot { position:absolute; left:0; right:0; top:1300px; height:220px; background:linear-gradient(180deg, rgba(6,6,8,0) 0%, rgba(6,6,8,0.7) 30%, rgba(6,6,8,0.7) 70%, rgba(6,6,8,0) 100%); }
#dim { position:absolute; inset:0; background:radial-gradient(ellipse 90% 60% at 50% 42%, rgba(30,12,4,0.55) 0%, rgba(6,6,8,0.82) 70%, rgba(6,6,8,0.92) 100%); }
#str { position:absolute; inset:0; background:repeating-linear-gradient(115deg, rgba(255,255,255,0.03) 0 2px, rgba(0,0,0,0) 2px 52px); }
#glow { position:absolute; left:540px; top:560px; width:1000px; height:1000px; margin:-500px 0 0 -500px; border-radius:50%; background:radial-gradient(circle, rgba(255,90,31,0.35) 0%, rgba(255,90,31,0) 62%); }
#col { position:absolute; left:40px; right:40px; top:270px; display:flex; flex-direction:column; align-items:center; gap:20px; text-align:center; }
#k { font-family:"JetBrains Mono"; font-weight:700; font-size:28px; letter-spacing:0.3em; color:#111; background:#ff5a1f; padding:11px 18px 10px 26px; }
#lg { width:340px; height:340px; filter:drop-shadow(0 20px 50px rgba(0,0,0,0.7)) drop-shadow(0 0 30px rgba(255,90,31,0.45)); }
#t1 { font-weight:900; font-style:italic; font-size:100px; line-height:0.95; color:#fff; text-shadow:0 5px 0 rgba(0,0,0,0.5); }
#t1 b { color:#ff5a1f; }
#t2 { font-weight:800; font-size:36px; line-height:1.25; color:#f5c242; letter-spacing:0.02em; }
#lnk { position:absolute; left:0; right:0; top:1215px; text-align:center; }
#lnk .w { font-weight:900; font-style:italic; font-size:52px; color:#fff; text-shadow:0 4px 0 rgba(0,0,0,0.6); }
#lnk .a { display:flex; justify-content:center; gap:18px; margin-top:10px; }
#lnk .a i { width:0; height:0; border-left:22px solid transparent; border-right:22px solid transparent; border-top:28px solid #ff5a1f; filter:drop-shadow(0 0 10px rgba(255,90,31,0.8)); }
#rp { position:absolute; left:40px; right:40px; top:1520px; display:flex; flex-direction:column; align-items:center; gap:14px; text-align:center; }
#rp .q { font-weight:900; font-style:italic; font-size:44px; line-height:1.05; color:#fff; text-shadow:0 4px 0 rgba(0,0,0,0.6); }
#rp .q b { color:#ff5a1f; }
#rp .h { display:flex; align-items:center; gap:16px; font-weight:800; font-size:36px; color:#fff; }
#ic { width:48px; height:48px; border-radius:13px; position:relative; background:radial-gradient(circle at 30% 110%, #fdf497 0%, #fd5949 45%, #d6249f 60%, #285AEB 95%); }
#ic::before { content:""; position:absolute; inset:10px; border:4px solid #fff; border-radius:10px; }
#ic::after { content:""; position:absolute; left:16px; top:16px; width:8px; height:8px; border:4px solid #fff; border-radius:50%; }
"""
BODY = ('<div id="dim"></div><div id="str"></div><div id="glow"></div><div id="vig"></div><div id="slot"></div>'
        '<div id="col"><div id="k">HEAVYWEIGHT KARTING CHAMPIONSHIP</div><img id="lg" src="assets/hkc-logo.png" />'
        '<div id="t1">NEW CHAMPIONSHIP<br><b>INCOMING…</b></div>'
        '<div id="t2">BUILT FOR HEAVYWEIGHT DRIVERS.<br>RACE PEOPLE YOUR SIZE.</div></div>'
        '<div id="lnk"><div class="w">WATCH THE FULL RACE</div><div class="a"><i></i><i></i><i></i></div></div>'
        '<div id="rp"><div class="q">REPLY “<b>HKC</b>” TO REGISTER<br>YOUR INTEREST</div><div class="h"><i id="ic"></i>@heavyweight_karting_48</div></div>')
JS = f"""
tl.from("#dim", {{ opacity:0, duration:0.5, ease:"power1.out" }}, 0);
tl.from("#k", {{ clipPath:"inset(0 100% 0 0)", duration:0.4, ease:"expo.out" }}, 0.25);
tl.from("#lg", {{ scale:0.2, rotation:-220, opacity:0, duration:0.85, ease:"back.out(1.4)" }}, 0.35);
tl.to("#lg", {{ rotation:5, duration:1.6, yoyo:true, repeat:7, ease:"sine.inOut" }}, 1.3);
tl.from("#t1", {{ scale:1.5, opacity:0, duration:0.35, ease:"back.out(1.8)" }}, 0.9);
tl.from("#t2", {{ y:24, opacity:0, duration:0.4, ease:"power3.out" }}, 1.3);
tl.from("#lnk .w", {{ y:20, opacity:0, duration:0.4, ease:"power3.out" }}, 1.7);
tl.from("#lnk .a i", {{ y:-20, opacity:0, duration:0.3, stagger:0.08, ease:"back.out(2)" }}, 1.9);
tl.to("#lnk .a", {{ y:14, duration:0.45, yoyo:true, repeat:27, ease:"sine.inOut" }}, 2.3);
tl.from("#rp .q", {{ scale:1.3, opacity:0, duration:0.35, ease:"back.out(1.8)" }}, 2.2);
tl.from("#rp .h", {{ x:-30, opacity:0, duration:0.4, ease:"expo.out" }}, 2.5);
tl.to("#rp .q", {{ scale:1.05, duration:0.55, yoyo:true, repeat:19, ease:"sine.inOut" }}, 3.0);
tl.to("#glow", {{ scale:1.15, duration:1.5, yoyo:true, repeat:8, ease:"sine.inOut" }}, 0);
tl.fromTo("#str", {{ backgroundPositionX:"0px" }}, {{ backgroundPositionX:"420px", duration:{DUR}, ease:"none" }}, 0);
"""

def write():
    os.makedirs(D + '/assets', exist_ok=True)
    html = G.HEAD.replace('%DUR%', f'{DUR:.3f}').replace('%BODY%', BODY).replace('%JS%', JS)
    html = html.replace('</style>', CSS + '</style>')
    open(D + '/index.html', 'w').write(html)
    shutil.copy(G.GSAP, D + '/assets/'); shutil.copy(G.HFJSON, D); shutil.copy(R + '/gfx/assets/hkc-logo.png', D + '/assets/')
    open(D + '/meta.json', 'w').write('{"id":"story","name":"story","width":2160,"height":3840,"fps":25}')

def video(out):
    each = (DUR + XF * (len(SHOTS) - 1)) / len(SHOTS)
    ins, fc, prev = [], [], '0:v'
    for s in SHOTS: ins += ['-stream_loop', '-1', '-i', f'pieces-final/{s}.mp4']
    for i in range(len(SHOTS)):
        fc.append(f'[{i}:v]trim=0:{each:.3f},setpts=PTS-STARTPTS,gblur=sigma=6,eq=brightness=-0.05:saturation=0.9[s{i}]')
    prev = 's0'
    for i in range(1, len(SHOTS)):
        fc.append(f'[{prev}][s{i}]xfade=transition=fade:duration={XF}:offset={i * (each - XF):.3f}[x{i}]'); prev = f'x{i}'
    n = len(SHOTS)
    fc.append(f'[{n}:v]format=yuva444p10le[o];[{prev}][o]overlay=0:0:format=auto,format=yuv420p[v]')
    ins += ['-i', D + '/out4k.mov', '-i', G.WS + '/assets/music/music-bed-cinematic-tech.mp3']
    fc.append(f'[{n + 1}:a]atrim=0:{DUR},afade=t=in:d=0.5,afade=t=out:st={DUR - 1.2}:d=1.2,volume=-6dB[a]')
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-profile:v', 'high', '-level', '5.2', '-r', '25',
                    '-c:a', 'aac', '-b:a', '256k', '-t', str(DUR), '-movflags', '+faststart', out], check=True)
    print('wrote', out)

if __name__ == '__main__':
    if sys.argv[1] == 'gfx': write()
    else: video(sys.argv[2])
