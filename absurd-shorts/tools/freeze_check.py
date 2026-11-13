#!/usr/bin/env python3
"""freeze_check.py VIDEO STORY.json [--gap 2] [--thr 14] [--min 0.4]: the holds that read as a freeze at phone size.

(cycle 13) The animation review of 49 measured it this way: consecutive strip tiles (every second frame) that differ only by grain, the
99.5th-percentile local difference at 4-7 on 0-255, nothing moving by a pixel of the 576 draft. This repeats that measurement on a draft before
the review, at the size of a strip tile (144 x 256; calibrated on the spans that review named: 7-13 there, a median of 74 elsewhere)
frames `gap` apart, absolute difference on a slightly blurred grey image, 99.5th percentile; a run of `min` seconds or more under
`thr` is printed with its shot. A camera that drifts hides a frozen character (the edges move), as it did for the reviewer: the tool finds
what the reviewer will find, not every stillness."""
import argparse, json
import cv2, numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('video'); ap.add_argument('story')
ap.add_argument('--gap', type=int, default=2); ap.add_argument('--thr', type=float, default=14.0); ap.add_argument('--min', type=float, default=0.4)
A = ap.parse_args()
d = json.load(open(A.story)); shots = [(s['id'], s['start'], s['start'] + s['duration']) for s in d['scenes']]
cap = cv2.VideoCapture(A.video); fps = cap.get(cv2.CAP_PROP_FPS) or 30
prev, i, vals = None, 0, []
while True:
    ok, im = cap.read()
    if not ok: break
    if i % A.gap == 0:
        g = cv2.GaussianBlur(cv2.cvtColor(cv2.resize(im, (144, 256), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY), (3, 3), 0).astype(np.int16)   # the size of a strip tile: the grain averages out
        if prev is not None: vals.append((i / fps, float(np.percentile(np.abs(g - prev), 99.5))))
        prev = g
    i += 1
def shot_of(t):
    for sid, a, b in shots:
        if a <= t < b: return sid, a, b
    return shots[-1]
runs, cur = [], None
for t, v in vals:
    sid, a, b = shot_of(t)
    if v < A.thr and (cur is None or cur[0] == sid):
        cur = cur or [sid, t, t, []]; cur[2] = t; cur[3].append(v)
    else:
        if cur and cur[2] - cur[1] >= A.min - 1e-6: runs.append(cur)
        cur = [sid, t, t, [v]] if v < A.thr else None
if cur and cur[2] - cur[1] >= A.min - 1e-6: runs.append(cur)
for sid, t0, t1, vs in runs:
    print(f'  freeze {sid} {t0:.2f}-{t1 + A.gap / fps:.2f} s ({t1 + A.gap / fps - t0:.2f} s, motion p99.5 {min(vs):.1f}-{max(vs):.1f} < {A.thr}): a blink, a breath, a glance, a drift')
print(f'{len(runs)} frozen spans in {len(vals)} samples')
