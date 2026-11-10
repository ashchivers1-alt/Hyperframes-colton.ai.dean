"""Map edit-time transcript words into each reel's local time -> src/<reel>_words.json"""
import json
R = json.load(open('reels.json')); FPS = R['fps']; W = json.load(open('src/words.json'))
FIX = {'car': 'curl', 'cloud': 'clouds'}
for name, r in R['reels'].items():
    out, base = [], 0.0
    for a, b in r['segs']:
        fa, fb = round(a * FPS) / FPS, round(b * FPS) / FPS
        for w in W:
            mid = (w['start'] + w['end']) / 2
            if fa <= mid < fb:
                t = w['text'].strip()
                core = t.strip('.,?!').lower()
                if core in FIX: t = t.lower().replace(core, FIX[core])
                out.append({'text': t, 'start': round(max(fa, w['start']) - fa + base, 3), 'end': round(min(fb, w['end']) - fa + base, 3)})
        base += fb - fa
    json.dump(out, open(f'src/{name}_words.json', 'w'), indent=0)
    print(f'\n## {name} {base:.2f}s'); print(' '.join(f"{w['text']}@{w['start']:.1f}" for w in out))
