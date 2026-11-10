import sys, os, glob
from PIL import Image, ImageDraw, ImageFont
n, step = sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 3
fs = sorted(glob.glob(f'src/fr/{n}/*.jpg')); C, R = 8, 8
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 20)
for p in range(0, len(fs), C * R):
    page = fs[p:p + C * R]; w, h = Image.open(page[0]).size
    sh = Image.new('RGB', (C * w, R * h))
    for i, f in enumerate(page):
        im = Image.open(f); d = ImageDraw.Draw(im); t = (p + i) * step + step / 2 if step == 3 else (p + i) * step
        t = (p + i) * step
        d.rectangle([0, 0, 70, 24], fill='black'); d.text((3, 1), f'{int(t//60)}:{int(t%60):02d}', fill='yellow', font=font)
        sh.paste(im, ((i % C) * w, (i // C) * h))
    sh.save(f'src/sheets/{n}-{p // (C * R)}.jpg', quality=80)
