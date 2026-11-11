#!/usr/bin/env python3
"""cut_flash_check.py FILM.mp4 scripts-fr/story_x.json: one odd frame at the start of a shot (a shot graded dark whose first frame is still lit, a prop
that pops in one frame late, a pose that jumps). For every cut it compares the first frame of the shot with the two that follow: a first frame that
differs from the second far more than the second differs from the third is reported. Run it on the draft and on the final film."""
import sys, json, cv2, numpy as np
V, J = sys.argv[1:3]
sc = json.load(open(J))['scenes']; c = cv2.VideoCapture(V); fps = c.get(cv2.CAP_PROP_FPS) or 30; n = int(c.get(cv2.CAP_PROP_FRAME_COUNT))
def fr(i):
    c.set(cv2.CAP_PROP_POS_FRAMES, i); ok, im = c.read(); return cv2.resize(im, (180, 320)).astype(np.float32) if ok else None
bad = 0
for s in sc:
    f0 = round(s['start'] * fps); best = None
    for off in (-1, 0, 1):   # the cut may fall one frame either side of the rounded time
        a, b, e = fr(f0 + off), fr(f0 + off + 1), fr(f0 + off + 2)
        if a is None or b is None or e is None: continue
        d01, d12 = float(np.abs(a - b).mean()), float(np.abs(b - e).mean())
        prev = fr(f0 + off - 1); dp = float(np.abs(prev - a).mean()) if prev is not None else 99
        if d01 > 20 and dp > 0.4 * d01 and d01 > 0.4 * dp and d01 > 6 * max(d12, 0.3) and (best is None or d01 > best[1]): best = (f0 + off, d01, d12, dp)   # it differs as much from the frame before as from the frame after, and the shot is still after it
    if best:
        bad += 1; print(f"{s['id']}: frame {best[0]} ({best[0] / fps:.2f} s) stands alone: differs from the previous frame by {best[3]:.1f}, from the next by {best[1]:.1f}, while the two after it differ by {best[2]:.1f}")
print('no lone frame at a cut' if not bad else f'{bad} lone frame(s) at a cut')
sys.exit(1 if bad else 0)
