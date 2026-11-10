"""flash_check.py VIDEO STORY.json: per street shot, the luma of a patch of road (found on the shot's median frame as the darkest low-saturation region of the lower half) frame by frame;
prints the frames whose patch luma jumps by more than 35 from the shot's median (two coplanar surfaces fighting for depth show as single pale frames)."""
import sys, json, cv2, numpy as np
V, J = sys.argv[1], sys.argv[2]; shots = json.load(open(J))['scenes']; c = cv2.VideoCapture(V); bad = 0
for s in shots:
    if s['set'] != 'parisStreet': continue
    f0, f1 = round(s['start'] * 30), round((s['start'] + s['duration']) * 30); fr = []
    c.set(cv2.CAP_PROP_POS_FRAMES, f0)
    for f in range(f0, f1):
        ok, im = c.read()
        if not ok: break
        fr.append(cv2.resize(im, (270, 480), interpolation=cv2.INTER_AREA))
    if not fr: continue
    A = np.stack(fr).astype(np.float32); med = np.median(A, axis=0); hsv = cv2.cvtColor(med.astype(np.uint8), cv2.COLOR_BGR2HSV)
    road = (hsv[..., 1] < 40) & (hsv[..., 2] > 70) & (hsv[..., 2] < 135)   # grey asphalt
    if road.sum() < 150: print(s['id'], 'no road in view'); continue
    lum = A.mean(axis=3)[:, road].mean(axis=1); m = np.median(lum); flips = [(i, round(float(v))) for i, v in enumerate(lum) if abs(v - m) > 35]
    bad += len(flips); print(s['id'], f'road px {int(road.sum())}, median luma {m:.0f}, frames off: {len(flips)}', flips[:12])
print('frames with a flash:', bad)
