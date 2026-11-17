# critic_final.py STORY FINAL.mp4 OUTDIR "S01+S02,S03,..." "name:time,name:time": evidence from the finished film: overview sheets (60 % and 85 % of each shot),
# motion strips (every second frame, one block per shot), full frames (576 px wide) at the given times
import sys, json, cv2, numpy as np
import os as _os
PIPE = _os.environ.get('PIPE', '/tmp/pipe')
PIPELINE_DIR = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
ROOT = _os.path.dirname(PIPELINE_DIR)
REPO = _os.path.dirname(ROOT)
_os.makedirs(f'{PIPE}/critic/configs', exist_ok=True)
S, V, C, G, F = sys.argv[1:6]
d = json.load(open(f'{ROOT}/scripts-fr/story_{S}.json'))['scenes']; D = {s['id']: s for s in d}; c = cv2.VideoCapture(V); NF = int(c.get(cv2.CAP_PROP_FRAME_COUNT)); FR = round(c.get(cv2.CAP_PROP_FPS) or 30)   # (cycle 34) drafts may be 15 fps
def frame(t):
    c.set(cv2.CAP_PROP_POS_FRAMES, min(NF - 1, round(t * FR))); ok, im = c.read(); return im
for k, tag in ((0.6, '60pct'), (0.85, '85pct')):
    tiles = []
    for s in d:
        x = cv2.resize(frame(s['start'] + s['duration'] * k), (216, 384), interpolation=cv2.INTER_AREA); cv2.rectangle(x, (0, 0), (40, 18), (255, 255, 255), -1); cv2.putText(x, s['id'], (3, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2); tiles.append(x)
    while len(tiles) % 6: tiles.append(np.full_like(tiles[0], 235))
    cv2.imwrite(f'{C}/overview_{tag}.jpg', np.vstack([np.hstack(tiles[i:i + 6]) for i in range(0, len(tiles), 6)]), [cv2.IMWRITE_JPEG_QUALITY, 90])
TW, TH, N = 124, 220, 12
for g in [x.split('+') for x in G.split(',')]:
    rows = []
    for sid in g:
        s = D[sid]; f0, f1 = round(s['start'] * FR), round((s['start'] + s['duration']) * FR) - 1; ims = []
        for f in range(f0, f1 + 1, max(1, FR // 15)):   # every second frame at 30 fps, every frame at 15
            c.set(cv2.CAP_PROP_POS_FRAMES, f); ok, im = c.read()
            if not ok: break
            im = cv2.resize(im, (TW, TH), interpolation=cv2.INTER_AREA); cv2.rectangle(im, (0, 0), (46, 14), (255, 255, 255), -1); cv2.putText(im, f'{(f - f0) / FR:.2f}', (2, 11), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 0, 200), 1); ims.append(im)
        lab = np.full((18, TW * N, 3), 235, np.uint8); cv2.putText(lab, f'{sid}  ({s["start"]:.2f}-{s["start"] + s["duration"]:.2f} s)', (4, 13), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1); rows.append(lab)
        while len(ims) % N: ims.append(np.full_like(ims[0], 235))
        rows += [np.hstack(ims[i:i + N]) for i in range(0, len(ims), N)]
    out = f'{C}/motion_{"_".join([g[0], g[-1]]) if len(g) > 1 else g[0]}.jpg'; img = np.vstack(rows); cv2.imwrite(out, img, [cv2.IMWRITE_JPEG_QUALITY, 90]); print(out, img.shape[1], 'x', img.shape[0])
for x in F.split(','):
    nm, t = x.split(':'); im = cv2.resize(frame(float(t)), (576, 1024), interpolation=cv2.INTER_AREA); cv2.imwrite(f'{C}/frame_{nm}.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 92]); print('frame', nm, t)
