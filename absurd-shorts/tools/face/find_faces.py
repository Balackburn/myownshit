#!/usr/bin/env python3
"""Step 1 — find the best close-ups of a character's FACE PANEL in reference videos.

The face is a flat painted panel on a box head: a skin-coloured quadrilateral with a thick dark border.
For every Nth frame: segment skin (HSV range from the character config), take tall quadrilateral contours,
score them (area × rectangularity × sharpness × frontality) and keep the top-K frames with their 4 corners.

  python3 tools/face/find_faces.py characters/lemec/character.json --top 12
Writes characters/<name>/face/candidates.json and candidate crops (for a human to accept/reject).
All values here are MEASURED from pixels; nothing is drawn.
"""
import sys, os, json, argparse, subprocess
import numpy as np, cv2

def frames(video, step):
    w, h = map(int, subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', video], capture_output=True, text=True).stdout.strip().split(','))
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', video, '-vf', f'select=not(mod(n\\,{step}))', '-vsync', '0', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], capture_output=True).stdout
    arr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
    for i, f in enumerate(arr): yield i * step, f

def order_quad(pts):
    pts = pts.reshape(4, 2).astype(np.float32); s = pts.sum(1); d = np.diff(pts, axis=1).ravel()
    return np.array([pts[np.argmin(s)], pts[np.argmin(d)], pts[np.argmax(s)], pts[np.argmax(d)]])  # tl, tr, br, bl

def detect(frame, cfg):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lo, hi = np.array(cfg['skin_hsv_lo']), np.array(cfg['skin_hsv_hi'])
    m = cv2.inRange(hsv, lo, hi)
    # keep the thick ink border as a separator (face panel vs neck / head side): tiny close, then fill interior holes
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    ff = m.copy(); hh, ww = m.shape; fm = np.zeros((hh + 2, ww + 2), np.uint8); cv2.floodFill(ff, fm, (0, 0), 255)
    m = m | cv2.bitwise_not(ff) if m[0, 0] == 0 else m
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    H, W = m.shape; best = None
    for c in cnts:
        a = cv2.contourArea(c)
        if a < 0.02 * H * W: continue
        hull = cv2.convexHull(c); peri = cv2.arcLength(hull, True)
        q = cv2.approxPolyDP(hull, 0.03 * peri, True)
        if len(q) != 4: continue
        q = order_quad(q); (tl, tr, br, bl) = q
        wq = (np.linalg.norm(tr - tl) + np.linalg.norm(br - bl)) / 2; hq = (np.linalg.norm(bl - tl) + np.linalg.norm(br - tr)) / 2
        aspect = wq / max(hq, 1)
        if not (cfg['aspect_min'] <= aspect <= cfg['aspect_max']): continue
        rect = a / max(cv2.contourArea(q.astype(np.int32)), 1)                       # how much of the quad is skin
        para = 1 - abs(np.linalg.norm(tr - tl) - np.linalg.norm(br - bl)) / max(wq, 1)  # frontality: opposite sides equal
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY); x, y, w_, h_ = cv2.boundingRect(q.astype(np.int32))
        sharp = cv2.Laplacian(gray[y:y + h_, x:x + w_], cv2.CV_64F).var()
        # painted-face evidence: some ink (2–30 %) and at least one white eye blob inside the quad
        qm = np.zeros(m.shape, np.uint8); cv2.fillConvexPoly(qm, q.astype(np.int32), 255)
        inside = gray[qm > 0]; ink = float((inside < 60).mean())
        white = cv2.inRange(frame, (200, 200, 200), (255, 255, 255)) & qm
        nwhite = sum(1 for cc in cv2.findContours(white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] if 0.0004 * a < cv2.contourArea(cc) < 0.06 * a)
        edge = (q[:, 0].min() < 3) or (q[:, 1].min() < 3) or (q[:, 0].max() > W - 4) or (q[:, 1].max() > H - 4)
        if not (0.02 <= ink <= 0.30) or nwhite < 1 or edge: continue
        score = (a / (H * W)) * min(rect, 1.0) * max(para, 0) ** 2 * np.log1p(sharp) * min(nwhite, 2)
        if best is None or score > best['score']:
            best = dict(score=float(score), quad=q.round(1).tolist(), area=float(a / (H * W)), aspect=float(aspect), frontality=float(para), sharpness=float(sharp), ink=round(ink, 3), eyes_white_blobs=nwhite)
    return best

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('config'); ap.add_argument('--top', type=int, default=12); ap.add_argument('--step', type=int, default=3)
    a = ap.parse_args(); cfg = json.load(open(a.config)); root = os.path.dirname(os.path.abspath(a.config))
    out = os.path.join(root, 'face'); os.makedirs(out + '/candidates', exist_ok=True)
    found = []
    for v in cfg['videos']:
        for n, f in frames(v, a.step):
            d = detect(f, cfg)
            if d: d.update(video=v, frame=n); found.append((d, f))
    found.sort(key=lambda x: -x[0]['score'])
    picked, seen = [], []
    for d, f in found:   # diversity: skip near-duplicate frames of the same video (< 0.5 s apart)
        if any(s['video'] == d['video'] and abs(s['frame'] - d['frame']) < 15 for s in seen): continue
        seen.append(d); picked.append((d, f))
        if len(picked) >= a.top: break
    for i, (d, f) in enumerate(picked):
        vis = f.copy(); cv2.polylines(vis, [np.array(d['quad'], np.int32)], True, (0, 255, 0), 2)
        name = f'cand_{i:02d}.jpg'; cv2.imwrite(os.path.join(out, 'candidates', name), vis); d['crop'] = 'candidates/' + name
    json.dump([d for d, _ in picked], open(os.path.join(out, 'candidates.json'), 'w'), indent=1)
    print(f'{len(found)} detections, kept {len(picked)} -> {out}/candidates.json')
    for d, _ in picked: print(f"  {os.path.basename(d['video'])[:8]} f{d['frame']:4d} score {d['score']:.3f} area {d['area']:.2f} aspect {d['aspect']:.2f} front {d['frontality']:.2f} sharp {d['sharpness']:.0f}")

if __name__ == '__main__': main()
