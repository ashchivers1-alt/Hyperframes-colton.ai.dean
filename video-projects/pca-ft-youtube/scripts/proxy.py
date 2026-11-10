"""Low-res review assembly of the training pieces from the LRF proxies -> renders/train-proxy.mp4 + pieces timeline."""
import json, subprocess, os
E = json.load(open('pieces.json'))['ex']; os.makedirs('src/pp', exist_ok=True)
lst, t, rows = [], 0.0, []
for e in E:
    for i, (c, a, b, w, *_) in enumerate(e['pieces']):
        o = f"src/pp/{e['id']}{i}.mp4"; d = b - a
        subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-ss',str(a),'-t',str(d),'-i',f'src/lrf/{c}.mp4',
            '-vf','scale=960:540,fps=24000/1001','-af',f'afade=t=in:d=0.04,afade=t=out:st={d-0.06}:d=0.06',
            '-c:v','libx264','-preset','veryfast','-crf','26','-c:a','aac','-ar','48000','-ac','2',o], check=True)
        lst.append(f"file '{os.path.abspath(o)}'"); rows.append((round(t,2), e['id'], c, a, b, w)); t += d
open('src/pp/list.txt','w').write('\n'.join(lst))
subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-f','concat','-safe','0','-i','src/pp/list.txt','-c','copy','renders/train-proxy.mp4'], check=True)
json.dump(rows, open('src/pp/rows.json','w'))
for r in rows: print(*r)
print('total', round(t,1))
