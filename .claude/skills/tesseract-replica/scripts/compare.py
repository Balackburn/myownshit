#!/usr/bin/env python3
"""compare.py — measure how far a replica is from its reference, shot by shot.

usage:
  compare.py --ref ref.mp4 --cand cand.mp4 --shots shots.json --out DIR [--per-shot 3] [--times 1.2,3.4]
  compare.py --ref ref.mp4 --cand-frames DIR_WITH_t_<ms>.png --shots shots.json --out DIR

Candidate frames are scaled to the reference size. For each sample time it computes:
  ssim     structural similarity on luma (1 = identical)
  dE       mean CIE76 colour difference in Lab (lower is better; under 2 is invisible, over 10 is obvious)
  dL,da,db mean Lab offsets (candidate minus reference): which way the grade is off
  hist     Lab histogram distance 0..1 (palette / exposure mismatch independent of layout)
  edge     F1 of edge maps with 3 px tolerance (silhouettes, layout, framing; 1 = same edges)
  sharp    Laplacian-variance ratio candidate/reference (<1 softer, >1 crisper/noisier)
and writes report.json, report.md (worst first, with a diagnosis per sample) and sheet_<shot>.jpg
(reference | candidate | difference heatmap).
"""
import argparse, json, os, subprocess, sys
import numpy as np
from skimage.metrics import structural_similarity
from skimage.color import rgb2lab
import cv2

def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate',
                          '-show_entries', 'format=duration', '-of', 'json', path], capture_output=True, text=True).stdout
    j = json.loads(out); s = j['streams'][0]; n, d = s['r_frame_rate'].split('/')
    return int(s['width']), int(s['height']), float(n) / float(d), float(j['format']['duration'])

def frame_at(path, t, w, h):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.4f}', '-i', path, '-frames:v', '1', '-vf', f'scale={w}:{h}:flags=area',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    if len(raw) < w * h * 3: return None
    return np.frombuffer(raw[:w * h * 3], np.uint8).reshape(h, w, 3)

def load_png(path, w, h):
    im = cv2.imread(path, cv2.IMREAD_COLOR)
    if im is None: return None
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    return cv2.resize(im, (w, h), interpolation=cv2.INTER_AREA)

def edges(rgb):
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY); g = cv2.GaussianBlur(g, (3, 3), 0)
    return cv2.Canny(g, 60, 140) > 0

def edge_f1(a, b, tol=3):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * tol + 1, 2 * tol + 1))
    da = cv2.dilate(a.astype(np.uint8), k) > 0; db = cv2.dilate(b.astype(np.uint8), k) > 0
    p = (b & da).sum() / max(1, b.sum()); r = (a & db).sum() / max(1, a.sum())
    return 0.0 if p + r == 0 else 2 * p * r / (p + r)

def metrics(ref, cand):
    gr = cv2.cvtColor(ref, cv2.COLOR_RGB2GRAY); gc = cv2.cvtColor(cand, cv2.COLOR_RGB2GRAY)
    ssim, smap = structural_similarity(gr, gc, data_range=255, full=True)
    lr = rgb2lab(ref); lc = rgb2lab(cand); dlab = lc - lr
    dE = np.sqrt((dlab ** 2).sum(-1))
    hb = [(0, 100), (-60, 60), (-60, 60)]; hd = 0
    for c in range(3):
        h1, _ = np.histogram(lr[..., c], 32, hb[c]); h2, _ = np.histogram(lc[..., c], 32, hb[c])
        h1 = h1 / max(1, h1.sum()); h2 = h2 / max(1, h2.sum()); hd += 0.5 * np.abs(h1 - h2).sum() / 3
    lv = lambda g: cv2.Laplacian(g, cv2.CV_64F).var()
    return dict(ssim=round(float(ssim), 4), dE=round(float(dE.mean()), 2), dL=round(float(dlab[..., 0].mean()), 2),
                da=round(float(dlab[..., 1].mean()), 2), db=round(float(dlab[..., 2].mean()), 2), hist=round(float(hd), 3),
                edge=round(float(edge_f1(edges(ref), edges(cand))), 3), sharp=round(float(lv(gc) / max(1e-6, lv(gr))), 2)), dE

def diagnose(m):
    out = []
    if m['edge'] < 0.35: out.append('layout/framing: silhouettes do not line up (camera, lens, positions, timing)')
    elif m['edge'] < 0.55: out.append('shapes partly misaligned (pose, model proportions or small camera offset)')
    if abs(m['dL']) > 4: out.append(f"exposure {'too bright' if m['dL'] > 0 else 'too dark'} by {abs(m['dL']):.0f} L*")
    if abs(m['da']) > 3 or abs(m['db']) > 3: out.append(f"colour cast a*{m['da']:+.0f} b*{m['db']:+.0f} (grade, light colour, materials)")
    if m['hist'] > 0.25: out.append('palette differs (materials, sky, lighting)')
    if m['sharp'] < 0.6: out.append('too soft (texture detail, blur, resolution)')
    elif m['sharp'] > 1.7: out.append('too crisp or noisy (missing motion blur or paper softness, aliasing, grain)')
    return out or ['close: refine details']

def heat(dE):
    v = np.clip(dE / 30.0, 0, 1); return cv2.cvtColor(cv2.applyColorMap((v * 255).astype(np.uint8), cv2.COLORMAP_INFERNO), cv2.COLOR_BGR2RGB)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ref', required=True); ap.add_argument('--cand'); ap.add_argument('--cand-frames')
    ap.add_argument('--shots', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--per-shot', type=int, default=3); ap.add_argument('--times'); ap.add_argument('--only', help='comma list of shot ids')
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    W, H, fps, dur = probe(a.ref); spec = json.load(open(a.shots)); shots = spec['shots']
    if a.only: keep = set(a.only.split(',')); shots = [s for s in shots if s['id'] in keep]
    samples = []
    for s in shots:
        f0, f1 = s['frames']
        if a.times: ts = [float(x) for x in a.times.split(',') if s['t0'] <= float(x) < s['t1']]
        else:
            k = a.per_shot; ts = [(f0 + (f1 - f0) * (i + 0.5) / k) / fps for i in range(k)]
        samples += [(s['id'], round(t * fps) / fps) for t in ts]
    rows = []; sheets = {}
    for sid, t in samples:
        ref = frame_at(a.ref, t + 0.5 / fps, W, H)
        if a.cand: cand = frame_at(a.cand, t + 0.5 / fps, W, H)
        else: cand = load_png(os.path.join(a.cand_frames, f't_{int(round(t * 1000))}.png'), W, H)
        if ref is None or cand is None: rows.append(dict(shot=sid, t=t, missing=True)); continue
        m, dE = metrics(ref, cand); m.update(shot=sid, t=round(t, 3), diagnosis=diagnose(m)); rows.append(m)
        tile = np.concatenate([ref, cand, heat(dE)], 1)
        sheets.setdefault(sid, []).append(cv2.resize(tile, (tile.shape[1] // 2, tile.shape[0] // 2), interpolation=cv2.INTER_AREA))
    for sid, tiles in sheets.items():
        cv2.imwrite(os.path.join(a.out, f'sheet_{sid}.jpg'), cv2.cvtColor(np.concatenate(tiles, 0), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 85])
    good = [r for r in rows if not r.get('missing')]
    per = {}
    for r in good: per.setdefault(r['shot'], []).append(r)
    summary = {sid: {k: round(float(np.mean([r[k] for r in rs])), 3) for k in ('ssim', 'dE', 'hist', 'edge', 'sharp', 'dL', 'da', 'db')} for sid, rs in per.items()}
    score = lambda m: (1 - m['ssim']) + m['dE'] / 25 + m['hist'] + (1 - m['edge'])   # 0 = identical
    for sid in summary: summary[sid]['gap'] = round(score(summary[sid]), 3)
    overall = {k: round(float(np.mean([v[k] for v in summary.values()])), 3) for k in ('ssim', 'dE', 'hist', 'edge', 'gap')} if summary else {}
    json.dump(dict(reference=a.ref, candidate=a.cand or a.cand_frames, overall=overall, shots=summary, samples=rows), open(os.path.join(a.out, 'report.json'), 'w'), indent=1)
    L = ['# Replica comparison', '', f"Overall: SSIM {overall.get('ssim')}, ΔE {overall.get('dE')}, histogram {overall.get('hist')}, edges {overall.get('edge')}, gap {overall.get('gap')} (0 = identical)", '',
         '| shot | gap | SSIM | ΔE | dL / da / db | hist | edges | sharp |', '|---|---|---|---|---|---|---|---|']
    for sid, m in sorted(summary.items(), key=lambda kv: -kv[1]['gap']):
        L.append(f"| {sid} | {m['gap']} | {m['ssim']} | {m['dE']} | {m['dL']:+} / {m['da']:+} / {m['db']:+} | {m['hist']} | {m['edge']} | {m['sharp']} |")
    L += ['', '## Diagnosis by sample (worst first)', '']
    for r in sorted(good, key=lambda r: -score(r)):
        L.append(f"- {r['shot']} @ {r['t']:.2f}s: " + '; '.join(r['diagnosis']))
    miss = [r for r in rows if r.get('missing')]
    if miss: L += ['', f"Missing candidate frames: {', '.join(f'{r['shot']}@{r['t']:.2f}' for r in miss)}"]
    open(os.path.join(a.out, 'report.md'), 'w').write('\n'.join(L) + '\n'); print('\n'.join(L[:8 + len(summary)]))

if __name__ == '__main__': main()
