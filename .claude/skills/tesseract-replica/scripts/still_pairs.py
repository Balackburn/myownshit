"""still_pairs.py TIMES OUT.jpg REF.mp4 STILLS_DIR [WORK_DIR]: side-by-side sheet of reference frames (left) and your stills (right) at
the same times (STILLS_DIR holds s_000.jpg, s_001.jpg ... in the order of TIMES). The fastest loop: render stills, compare, fix, repeat."""
import sys, json, subprocess, os
from PIL import Image, ImageDraw
REF = sys.argv[3]
ST = sys.argv[4]
S = sys.argv[5] if len(sys.argv) > 5 else os.path.dirname(os.path.abspath(sys.argv[2]))
times = [float(t) for t in sys.argv[1].split(',')]
out = sys.argv[2]
w, h = 216, 384
per_row = 4
rows = (len(times) + per_row - 1) // per_row
im = Image.new('RGB', (w * 2 * per_row + 6 * per_row, h * rows), 'black')
for i, t in enumerate(times):
    f = int(round(t * 30))
    rp = os.path.join(S, f'ref_{f}.png')
    if not os.path.exists(rp):
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', REF, '-vf', f'select=eq(n\\,{f})', '-vframes', '1', rp])
    a = Image.open(rp).convert('RGB').resize((w, h))
    b = Image.open(os.path.join(ST, f's_{i:03d}.jpg')).convert('RGB').resize((w, h))
    x = (i % per_row) * (2 * w + 6); y = (i // per_row) * h
    im.paste(a, (x, y)); im.paste(b, (x + w, y))
    d = ImageDraw.Draw(im); d.rectangle((x, y, x + 64, y + 16), fill='black'); d.text((x + 3, y + 3), f'f{f} ref', fill='white')
    d.rectangle((x + w, y, x + w + 40, y + 16), fill='black'); d.text((x + w + 3, y + 3), 'ours', fill='yellow')
im.save(out, quality=88); print(out)
