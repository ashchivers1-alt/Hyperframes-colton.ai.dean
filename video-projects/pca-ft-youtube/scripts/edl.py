"""pieces.json -> edl.json (training pieces in timeline frames, after the cut posing section)."""
import json
FPS = 24000 / 1001
I = json.load(open('intro.json')); MP = {p['clip']: p['mpid'] for p in json.load(open('edl-v1.json'))}
rec = I['length'] - sum(b - a for a, b, _ in I['cuts']); out = []
# Muscle Works Gym exterior (vertical iPhone clip, blurred fill) between the posing section and the training
GYM = dict(file='/Users/ashleychivers/Downloads/DE8C4FD8-778B-4977-928F-EB30F00AE1F5.MP4', src_in=0.0, rec=rec, frames=round(4.0 * FPS))
json.dump(GYM, open('gym.json', 'w'), indent=1); rec += GYM['frames']
for e in json.load(open('pieces.json'))['ex']:
    for c, a, b, w, m in e['pieces']:
        s, t = round(a * FPS), round(b * FPS)
        out.append(dict(ex=e['id'], clip=c, mpid=MP[c], src_start=s, src_end=t, rec=rec, dur=t - s, mode=m, who=w)); rec += t - s
json.dump(out, open('edl.json', 'w'), indent=1)
print(len(out), 'pieces; training', round((rec - out[0]['rec']) / FPS, 2), 's; total', round(rec / FPS, 2), 's')
