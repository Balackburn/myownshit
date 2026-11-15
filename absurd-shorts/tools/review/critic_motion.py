# critic_motion.py STORY PREVIEW.mp4: evidence for the critics of a cartoon-staged story -> scratchpad/critic/STORY/
#   motion_<shots>.jpg: every second frame of groups of shots (one row block per shot); needs the stills already rendered for the overviews
import sys, json, cv2, numpy as np, os
S, V = sys.argv[1], sys.argv[2]; C = f'/tmp/claude-0/-home-user-myownshit/55de8c21-9e41-5895-8198-7b13ed3b7877/scratchpad/critic/{S}'
GROUPS = [g.split('+') for g in sys.argv[3].split(',')]
d = {s['id']: s for s in json.load(open(f'/home/user/myownshit/absurd-shorts/scripts-fr/story_{S}.json'))['scenes']}; c = cv2.VideoCapture(V); TW, TH, N = 124, 220, 12
for g in GROUPS:
    rows = []
    for sid in g:
        s = d[sid]; f0, f1 = round(s['start'] * 30), round((s['start'] + s['duration']) * 30) - 1; ims = []
        for f in range(f0, f1 + 1, 2):
            c.set(cv2.CAP_PROP_POS_FRAMES, f); ok, im = c.read()
            if not ok: break
            im = cv2.resize(im, (TW, TH), interpolation=cv2.INTER_AREA); cv2.rectangle(im, (0, 0), (46, 14), (255, 255, 255), -1); cv2.putText(im, f'{(f - f0) / 30:.2f}', (2, 11), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 0, 200), 1); ims.append(im)
        lab = np.full((18, TW * N, 3), 235, np.uint8); cv2.putText(lab, f'{sid}  ({s["start"]:.2f}-{s["start"] + s["duration"]:.2f} s)', (4, 13), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1); rows.append(lab)
        while len(ims) % N: ims.append(np.full_like(ims[0], 235))
        rows += [np.hstack(ims[i:i + N]) for i in range(0, len(ims), N)]
    out = f'{C}/motion_{"_".join([g[0], g[-1]]) if len(g) > 1 else g[0]}.jpg'; img = np.vstack(rows); cv2.imwrite(out, img, [cv2.IMWRITE_JPEG_QUALITY, 90]); print(out, img.shape[1], 'x', img.shape[0])
