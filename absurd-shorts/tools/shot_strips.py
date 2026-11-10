#!/usr/bin/env python3
"""shot_strips.py VIDEO STORY.json OUTDIR [--range a:b] [--step 2] [--tile 150] [--shots S01,S02]: one filmstrip per shot of a story,
every `step` frames, the time inside the shot on each tile -> OUTDIR/strip_<shot>.jpg. VIDEO is the whole film, or with --range a:b the
part of it rendered with `render3.mjs --range a:b` (see tools/motion_check.sh)."""
import sys, json, os, math
import cv2, numpy as np
a = sys.argv[1:]; opt = lambda k, d: a[a.index('--' + k) + 1] if '--' + k in a else d
video, story, out = a[0], a[1], a[2]; step, tw = int(opt('step', 2)), int(opt('tile', 150)); want = set(opt('shots', '').split(',')) - {''}
t0, t1 = (float(x) for x in opt('range', '0:1e9').split(':')); os.makedirs(out, exist_ok=True)
c = cv2.VideoCapture(video); fps = c.get(cv2.CAP_PROP_FPS) or 30; F0 = round(t0 * fps); n = 12
for s in json.load(open(story))['scenes']:
    if (want and s['id'] not in want) or s['start'] < t0 - 1e-3 or s['start'] >= t1 - 1e-3: continue
    f0, f1 = math.ceil(s['start'] * fps - 1e-6) - F0, math.ceil((s['start'] + s['duration']) * fps - 1e-6) - F0 - 1; ims = []   # frame i shows time i / fps: a shot owns the frames from its start on
    for f in range(f0, f1 + 1, step):
        c.set(cv2.CAP_PROP_POS_FRAMES, f); ok, im = c.read()
        if not ok: break
        im = cv2.resize(im, (tw, round(tw * im.shape[0] / im.shape[1])), interpolation=cv2.INTER_AREA)
        cv2.rectangle(im, (0, 0), (44, 14), (255, 255, 255), -1); cv2.putText(im, f'{(f - f0) / fps:.2f}', (2, 11), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 0, 200), 1); ims.append(im)
    if not ims: continue
    while len(ims) % n: ims.append(np.full_like(ims[0], 235))
    cv2.imwrite(f'{out}/strip_{s["id"]}.jpg', np.vstack([np.hstack(ims[i:i + n]) for i in range(0, len(ims), n)]), [cv2.IMWRITE_JPEG_QUALITY, 88]); print(s['id'], f1 - f0 + 1, 'frames')
