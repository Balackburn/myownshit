# Residual (non-camera) motion per shot: Farneback flow, global camera motion removed with a RANSAC homography,
# then per-cell mean residual magnitude and divergence (growing / shrinking) for the original vs ours.
# usage: motion.py REF.mp4 OURS.mp4 OUTDIR
import cv2, numpy as np, sys, os, json
REF, OURS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(OUT, exist_ok=True)
CUTS = [0, 57, 103, 135, 196, 211, 229, 243, 254, 313, 335, 386, 431, 483, 529, 584, 607, 648, 670, 707, 724, 766, 780, 864]
NAMES = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8a', 'S8b', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S18', 'S19', 'S20', 'S21', 'S22']
W, H = 288, 512; GX, GY = 6, 10
mask = np.ones((H, W), bool); mask[int(780 / 2):int(872 / 2)] = False          # caption band
def read(p):
    c = cv2.VideoCapture(p); out = []
    while True:
        ok, im = c.read()
        if not ok: break
        out.append(cv2.cvtColor(cv2.resize(im, (W, H), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY))
    return out
def analyse(fr):
    ys, xs = np.mgrid[0:H:8, 0:W:8]; pts = np.stack([xs.ravel(), ys.ravel()], 1).astype(np.float32)
    res = []
    for i in range(len(fr) - 1):
        f = cv2.calcOpticalFlowFarneback(fr[i], fr[i + 1], None, 0.5, 3, 15, 3, 5, 1.2, 0)
        d = f[ys, xs].reshape(-1, 2); m = mask[ys, xs].ravel()
        Hm, inl = cv2.findHomography(pts[m], pts[m] + d[m], cv2.RANSAC, 1.0) if m.sum() > 20 else (None, None)
        if Hm is None: Hm = np.eye(3)
        gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
        P = np.stack([gx, gy, np.ones_like(gx)], -1) @ Hm.T; cam = P[..., :2] / P[..., 2:3] - np.stack([gx, gy], -1)
        r = f - cam; r[~mask] = 0
        mag = np.hypot(r[..., 0], r[..., 1]); div = np.gradient(r[..., 0], axis=1) + np.gradient(r[..., 1], axis=0)
        res.append((mag, div, float(np.hypot(*cam.reshape(-1, 2).mean(0)))))
    return res
R, O = read(REF), read(OURS)
n = min(len(R), len(O)); ar, ao = analyse(R[:n]), analyse(O[:n])
report = {}
for s, name in enumerate(NAMES):
    a, b = CUTS[s], min(CUTS[s + 1], n) - 1
    if b - a < 2: continue
    # skip the frame pair that crosses the cut
    mr = np.mean([ar[i][0] for i in range(a, b)], 0); mo = np.mean([ao[i][0] for i in range(a, b)], 0)
    dr = np.mean([ar[i][1] for i in range(a, b)], 0); do = np.mean([ao[i][1] for i in range(a, b)], 0)
    cell = lambda m: m[:H // GY * GY, :W // GX * GX].reshape(GY, H // GY, GX, W // GX).mean((1, 3))
    cr, co = cell(mr), cell(mo)
    miss = [(int(y), int(x), round(float(cr[y, x]), 3), round(float(co[y, x]), 3)) for y in range(GY) for x in range(GX) if cr[y, x] > 0.15 and cr[y, x] > 1.8 * co[y, x] + 0.05]
    tr = [float(ar[i][0][mask].mean()) for i in range(a, b)]; to = [float(ao[i][0][mask].mean()) for i in range(a, b)]
    report[name] = {'ref_resid': round(float(np.mean(tr)), 3), 'ours_resid': round(float(np.mean(to)), 3), 'missing_cells': miss,
                    'ref_div': round(float(cell(dr).std()), 4), 'ours_div': round(float(cell(do).std()), 4)}
    # heatmap image: ref | ours, residual magnitude (log scale) over the shot's middle frame
    mid = (a + b) // 2
    def heat(m, base):
        v = np.clip(np.log1p(m * 4) / np.log1p(8), 0, 1); hm = cv2.applyColorMap((v * 255).astype(np.uint8), cv2.COLORMAP_JET)
        return cv2.addWeighted(cv2.cvtColor(base, cv2.COLOR_GRAY2BGR), 0.45, hm, 0.55, 0)
    img = np.hstack([heat(mr, R[mid]), heat(mo, O[mid])])
    cv2.putText(img, f'{name} ref {report[name]["ref_resid"]} | ours {report[name]["ours_resid"]}', (4, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    cv2.imwrite(f'{OUT}/{name}.jpg', img)
json.dump(report, open(f'{OUT}/motion.json', 'w'), indent=1)
for k, v in report.items(): print(k, 'resid ref', v['ref_resid'], 'ours', v['ours_resid'], ' div-spread ref', v['ref_div'], 'ours', v['ours_div'], ' missing cells', v['missing_cells'][:6])
