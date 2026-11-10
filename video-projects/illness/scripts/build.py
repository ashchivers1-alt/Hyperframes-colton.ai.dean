"""Build index.html for the Illness reel (@kingketo top-card style).
Captions are generated from assets/transcript.json: 1-3 word ALL-CAPS chunks, yellow active word.
Usage (from the project folder): python3 -I scripts/build.py
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DUR = 52.37
words = json.loads((ROOT / "assets/transcript.json").read_text())

FIX = {"fucker": "F*CKER", "ie": "I.E.", "ash": "ASH"}

def clean(t):
    t = t.strip()
    k = re.sub(r"[^\w']", "", t).lower()
    if k in FIX:
        return FIX[k]
    return re.sub(r"[^\w'*.-]", "", t).upper().rstrip(".")

# ---- caption chunks: break on punctuation, max 2 words (3 if all short) ----
chunks, cur = [], []
for w in words:
    if w["start"] >= DUR - 0.05:
        break
    cur.append(w)
    end_punct = bool(re.search(r"[.,?!]$", w["text"].strip()))
    short = sum(len(clean(x["text"])) for x in cur) <= 9
    if end_punct or len(cur) >= 3 or (len(cur) == 2 and not short):
        chunks.append(cur); cur = []
if cur:
    chunks.append(cur)

cap_html, cap_js = [], []
for i, ch in enumerate(chunks):
    start = ch[0]["start"]
    end = chunks[i + 1][0]["start"] if i + 1 < len(chunks) else DUR
    spans = "".join(f'<span id="c{i}w{j}">{clean(w["text"])}</span> ' for j, w in enumerate(ch))
    cap_html.append(f'<div class="cap" id="c{i}">{spans.strip()}</div>')
    cap_js.append(f'tl.set("#c{i}", {{ opacity: 1 }}, {start:.2f}); tl.fromTo("#c{i}", {{ scale: 0.88 }}, {{ scale: 1, duration: 0.12, ease: "back.out(2.5)", immediateRender: false }}, {start:.2f}); tl.set("#c{i}", {{ opacity: 0 }}, {end:.2f});')
    for j, w in enumerate(ch):
        cap_js.append(f'tl.set("#c{i}w{j}", {{ color: "#FFD400" }}, {w["start"]:.2f});')
        if j + 1 < len(ch):
            cap_js.append(f'tl.set("#c{i}w{j}", {{ color: "#FFFFFF" }}, {ch[j+1]["start"]:.2f});')

html = (ROOT / "scripts/template.html").read_text()
html = html.replace("<!--CAPTIONS-->", "\n".join(cap_html)).replace("//CAPTIONS_JS", "\n        ".join(cap_js)).replace("__DUR__", str(DUR))
(ROOT / "index.html").write_text(html)
print("chunks", len(chunks))
