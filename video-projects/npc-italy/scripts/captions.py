"""Turn per-clip whisper words into proofread caption phrases (seconds relative to the clip). Writes captions.json."""
import json, re
FIX = {  # phrase (lowercase, no punctuation) -> replacement; '' drops it
    '03': [('the minutes', 'at the minute'), ('first dieting', 'reverse dieting'), ('all my health', 'hormonal health'),
           ('athletes from less', 'athletes with less'), ('at the end of the end but', 'but'), ('turn around maintenance', 'around maintenance'),
           ('the the the best', 'the best'), ('for for months', 'for months'), ('with this with this', 'with this'), ('why why', 'why'), ('as as', 'as')],
    '04': [('love of food', 'lower food'), ('try and touch on that', 'try and detach from that'), ('embrace the show', 'embrace the post-show'),
           ('by growing the offseason', 'i.e. grow in the offseason'), ('your body in put your body', 'put your body')],
    '12': [('in a minute', 'at the minute'), ('with a coach like this but i think thats whats to be fair', 'in a coaching relationship but to be fair'),
           ('growth formula drugs', 'growth hormone and drugs'), ('a baguette session', 'a banging session'), ('you can\'t you can\'t', "you can't"),
           ('i\'m i\'m', "I'm"), ('they they', 'they'), ('it\'s it\'s', "it's"), ('that\'s that\'s', "that's")],
    '20': [('chess', 'chest'), ('jim neko', 'Gym80'), ('since the', ''), ('train for phil', 'train for feel'), ('pegs', 'pecs'),
           ('phenomenal i guess', 'phenomenal'), ("i've just i just", 'I just')],
    '44': [('lmpi', 'Olympia'), ('buildings issue', 'building tissue'), ('in this game for years', 'in this game'),
           ('getting a reverse that this prep', 'getting her reversed out of this prep'), ('get a progressing for our offseason', 'get her progressing through our offseason'),
           ('get a you know climbing', 'get her climbing'), ("that's the topic", "that's the top tip"), ('the judge', 'the judges'),
           ("that's just guys", ''), ('because ain\'t the result', 'because the result'), ("what i've i say", 'what I say')],
}
FILLERS = {'um', 'uh', 'erm', 'ah'}
def norm(t): return re.sub(r"[^a-z0-9' ]", '', t.lower().replace('’', "'"))

def words(key):
    w = [dict(x) for x in json.load(open(f'src/tx/t{key}.json')) if norm(x['text']) not in FILLERS and norm(x['text'])]
    for pat, rep in FIX.get(key, []):
        p = pat.split(); i = 0
        while i <= len(w) - len(p):
            if [norm(x['text']) for x in w[i:i + len(p)]] == [norm(q) for q in p]:
                tail = w[i + len(p) - 1]['text']; punct = tail[-1] if tail[-1] in '.,?!' else ''
                new = dict(text=(rep + punct) if rep else '', start=w[i]['start'], end=w[i + len(p) - 1]['end'])
                w[i:i + len(p)] = [new] if rep else []
            i += 1
    for x in w:   # whisper stretches words across silences: pin long words to their end
        if x['end'] - x['start'] > 0.9: x['start'] = x['end'] - 0.45
    # whisper spread "don't / get / me" over a long pause in clip 20; they're really said together just before "wrong"
    for i in range(len(w) - 3):
        if [norm(x['text']) for x in w[i:i + 4]] == ["don't", 'get', 'me', 'wrong']:
            t = w[i + 3]['start']
            for k, off in enumerate((0.6, 0.4, 0.2)): w[i + k]['start'] = t - off; w[i + k]['end'] = t - off + 0.18
    return [x for x in w if x['text']]

def phrases(w, max_chars=34, max_dur=3.2, gap=0.45):
    out, cur = [], []
    def flush():
        if cur: out.append(dict(text=' '.join(x['text'] for x in cur), start=cur[0]['start'], end=cur[-1]['end']))
        cur.clear()
    for x in w:
        if cur and (x['start'] - cur[-1]['end'] > gap or len(' '.join(c['text'] for c in cur + [x])) > max_chars
                    or x['end'] - cur[0]['start'] > max_dur):
            flush()
        cur.append(x)
        if x['text'][-1] in '.?!': flush()
    flush()
    # merge one/two-word fragments into a neighbour when it still fits
    i = 0
    while i < len(out):
        p = out[i]
        if len(p['text'].split()) <= 2:
            nb = out[i + 1] if i + 1 < len(out) else None
            pv = out[i - 1] if i > 0 else None
            if nb and nb['start'] - p['end'] < 0.8 and len(p['text'] + ' ' + nb['text']) <= max_chars + 8 and p['text'][-1] not in '.?!':
                nb['text'] = p['text'] + ' ' + nb['text']; nb['start'] = p['start']; out.pop(i); continue
            if pv and p['start'] - pv['end'] < 0.8 and len(pv['text'] + ' ' + p['text']) <= max_chars + 8:
                pv['text'] += ' ' + p['text']; pv['end'] = p['end']; out.pop(i); continue
        i += 1
    prev_end = '.'
    for p in out:  # tidy: strip trailing commas, capitalise only sentence starts, fix lone "i"
        t = re.sub(r'\bi\b', 'I', p['text']).rstrip(',')
        if prev_end in '.?!': t = t[0].upper() + t[1:]
        prev_end = t[-1]
        p['text'] = t
    for a, b in zip(out, out[1:]):  # hold each phrase until the next (max +0.6 s)
        a['end'] = min(b['start'] - 0.04, a['end'] + 0.6)
    out[-1]['end'] += 0.6
    for p in out: p['end'] = min(p['end'], p['start'] + 0.42 * len(p['text'].split()) + 1.0)
    return out

caps = {k: phrases(words(k)) for k in FIX}
json.dump(caps, open('captions.json', 'w'), indent=1)
for k, v in caps.items(): print(k, len(v), 'phrases; e.g.', ' | '.join(p['text'] for p in v[:4]))
