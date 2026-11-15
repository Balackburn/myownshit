# shot_strips.py VIDEO STORY_JSON OUTDIR [step=2] [tile_w=144] [shots=S01,S02|all]: one filmstrip per shot (every `step` frames), named strip_<shot>.jpg
import sys, json, cv2, numpy as np, os
v, js, out = sys.argv[1], sys.argv[2], sys.argv[3]; step = int(sys.argv[4]) if len(sys.argv) > 4 else 2; tw = int(sys.argv[5]) if len(sys.argv) > 5 else 144
want = None if len(sys.argv) <= 6 or sys.argv[6] == 'all' else set(sys.argv[6].split(','))
os.makedirs(out, exist_ok=True); d = json.load(open(js)); c = cv2.VideoCapture(v); fps = c.get(cv2.CAP_PROP_FPS) or 30
for s in d['scenes']:
    if want and s['id'] not in want: continue
    f0, f1 = int(round(s['start'] * fps)), int(round((s['start'] + s['duration']) * fps)) - 1; ims = []
    for f in range(f0, f1 + 1, step):
        c.set(cv2.CAP_PROP_POS_FRAMES, f); ok, im = c.read()
        if not ok: break
        h = int(tw * im.shape[0] / im.shape[1]); im = cv2.resize(im, (tw, h)); cv2.putText(im, f'{(f - f0) / fps:.2f}', (3, 13), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1); ims.append(im)
    n = 12
    while len(ims) % n: ims.append(np.zeros_like(ims[0]))
    cv2.imwrite(f'{out}/strip_{s["id"]}.jpg', np.vstack([np.hstack(ims[i:i + n]) for i in range(0, len(ims), n)]), [cv2.IMWRITE_JPEG_QUALITY, 88])
print('strips ->', out)
