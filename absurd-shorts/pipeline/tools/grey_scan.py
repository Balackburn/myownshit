#!/usr/bin/env python3
"""grey_scan.py VIDEO...: flag short dips in colour saturation (a camera behind a wall shows a grey veil for a few frames; a missing material too)."""
import sys, subprocess, numpy as np
for v in sys.argv[1:]:
    w, h = 54, 96
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', v, '-vf', f'scale={w}:{h},format=rgb24', '-f', 'rawvideo', '-'], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3).astype(np.float32)
    mx, mn = fr.max(axis=3), fr.min(axis=3); sat = ((mx - mn) / np.maximum(mx, 1)).mean(axis=(1, 2)) * 255
    bad = []
    for i in range(len(sat)):
        lo, hi = max(0, i - 12), min(len(sat), i + 13); ref = np.median(sat[lo:hi])
        if sat[i] < 0.45 * ref and ref > 25: bad.append((i, round(float(sat[i]), 1), round(float(ref), 1)))
    print(v.split('/')[-1], len(sat), 'frames', 'dips:', bad[:12] if bad else 'none')
