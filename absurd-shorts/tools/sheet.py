#!/usr/bin/env python3
"""Contact sheet: python3 tools/sheet.py list.json out.jpg [cols]   (list = [{"f": path, "label": text}])"""
import json, sys
from PIL import Image, ImageDraw
items = json.load(open(sys.argv[1])); out = sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 10
tw = 180
ims = []
for it in items:
    im = Image.open(it['f']).convert('RGB'); th = int(im.height * tw / im.width); im = im.resize((tw, th))
    d = ImageDraw.Draw(im); d.rectangle((0, 0, tw, 13), fill=(0, 0, 0)); d.text((2, 1), it['label'][:34], fill=(255, 255, 0)); ims.append(im)
if not ims: sys.exit(0)
th = ims[0].height; rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (tw * min(cols, len(ims)), th * rows), (20, 20, 20))
for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
sheet.save(out, quality=88); print(out, len(ims), 'frames')
