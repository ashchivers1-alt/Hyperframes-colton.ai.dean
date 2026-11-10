"""Master edit plan for the NPC Italy vlog. Writes plan.json: every picture/dialogue segment with its new
record position (timeline frames @ 23.976), plus named markers used by graphics + music."""
import json
TL = json.load(open('/private/tmp/claude-501/-Users-ashleychivers-Documents-Claude-Video-Studio/88a5434b-e5ee-441f-8a31-409b07c3b15a/scratchpad/italy_tl.json'))
V1 = {i['item_index']: i for i in TL['tracks']['video']['tracks'][0]['items']}
V2 = TL['tracks']['video']['tracks'][1]['items'][0]
FPS = 24000 / 1001
S0 = TL['start_frame']
HYPER = 8          # hyperlapse speed
FAST = 5           # voice-note fast-forward speed
# voice note (item 11) sub-segments, seconds relative to the item: (start, end, speed)
VN = [(0.0, 22.95, 1), (22.95, 60.9, FAST), (60.9, 69.65, 1), (69.65, 97.9, FAST), (97.9, None, 1)]
MUTE = {2, 6, 7, 8, 9, 33, 34}      # no dialogue: music instead

def sfps(it): return FPS if abs(it['source_fps'] - 23.976) < 0.01 else it['source_fps']

segs, rec, marks = [], 0, {}
for idx in sorted(V1):
    it = V1[idx]; dur = it['end'] - it['start']
    base = dict(item=idx, name=it['name'], path=it['file_path'], mpid=it['media_pool_item_id'], src_fps=it['source_fps'])
    marks[f'i{idx}'] = rec
    if idx == 2:
        n = -(-(it['source_end'] - it['source_start']) // HYPER)
        segs.append(dict(base, kind='plate', plate='hyper', src_start=it['source_start'], src_end=it['source_end'],
                         speed=HYPER, rec=rec, dur=n, dlg=None))
        rec += n; continue
    if idx == 11:
        tot = dur / FPS
        for k, (a, b, sp) in enumerate(VN):
            b = tot if b is None else b
            fa, fb = round(a * FPS), round(b * FPS)
            ss, se = it['source_start'] + fa, it['source_start'] + fb
            if sp == 1:
                segs.append(dict(base, kind='clip', src_start=ss, src_end=se, rec=rec, dur=fb - fa,
                                 dlg=dict(file='audio/dlg_11.wav', start=a, end=b)))
                rec += fb - fa
            else:
                n = -(-(fb - fa) // sp)
                segs.append(dict(base, kind='plate', plate=f'vn{k}', src_start=ss, src_end=se, speed=sp, rec=rec, dur=n, dlg=None))
                marks[f'vn_fast{k}'] = (rec, n)
                rec += n
        continue
    dlg = None if idx in MUTE or idx == 45 else dict(file=f'audio/dlg_{idx:02d}.wav', start=0.0, end=dur / FPS)
    segs.append(dict(base, kind='clip', src_start=it['source_start'], src_end=it['source_end'], rec=rec, dur=dur, dlg=dlg))
    if idx == 1:   # keep the cutaway the user placed on V2 over the end of item 1
        marks['v2_cutaway'] = dict(rec=rec + (V2['start'] - it['start']), dur=V2['end'] - V2['start'],
                                   src_start=V2['source_start'], src_end=V2['source_end'], mpid=V2['media_pool_item_id'])
    rec += dur
marks['end'] = rec
json.dump(dict(fps=FPS, segs=segs, marks=marks), open('plan.json', 'w'), indent=1)
print('segments', len(segs), 'total frames', rec, f'= {rec / FPS / 60:.2f} min')
for s in segs:
    if s['kind'] == 'plate' or s['item'] in (10, 11, 12): print(s['item'], s['kind'], s.get('plate', ''), s['rec'], s['dur'])
