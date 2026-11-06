#!/usr/bin/env python3
"""Generate extra facial expressions for le mec in the measured face-set style (characters/lemec/face).

The measured face_neutral.png keeps its hair line, nose and stubble; the brows, eyes and mouth are erased with the clean skin plate
and redrawn with the same ink (stroke widths and colours measured on the neutral face), supersampled 4x. Writes
expressions/face_<name>.png and registers each name in face_landmarks.json ("status": "designed"), which the engine loads.
Run: python3 tools/face/gen_expressions.py [--sheet out.jpg]"""
import json, math, os, sys
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(ROOT, 'characters', 'lemec', 'face')
W, H, SS = 400, 1080, 4
INK, WHITE, TONGUE, MOUTH_IN, TEAR, BLUSH, RED = (45, 37, 31), (205, 189, 166), (206, 98, 98), (78, 28, 22), (126, 184, 226), (226, 122, 112), (200, 48, 44)   # ink and eye white sampled on the measured neutral face

neutral = cv2.imread(os.path.join(D, 'expressions', 'face_neutral.png'))
plate = cv2.imread(os.path.join(D, 'skin_plate_neutral.png'))
gray = cv2.cvtColor(neutral, cv2.COLOR_BGR2GRAY)
n, lab, st, cen = cv2.connectedComponentsWithStats((gray < 90).astype(np.uint8), 8)

def comp_near(cx, cy, min_area=800):
    best = None
    for i in range(1, n):
        if st[i, 4] < min_area: continue
        d = math.hypot(cen[i][0] - cx, cen[i][1] - cy)
        if best is None or d < best[0]: best = (d, i)
    return best[1]

C = {k: comp_near(*xy) for k, xy in {'browL': (106, 126), 'browR': (325, 368), 'eyeL': (85, 278), 'eyeR': (299, 488), 'mouth': (213, 836)}.items()}
def bbox(k): x, y, w, h, _ = st[C[k]]; return x, y, w, h
def axis(k):   # brow endpoints along its main axis, and its thickness
    ys, xs = np.nonzero(lab == C[k]); pts = np.stack([xs, ys], 1).astype(float); m = pts.mean(0)
    u, s, vt = np.linalg.svd(pts - m, full_matrices=False); a = vt[0]; proj = (pts - m) @ a
    p0, p1 = m + a * proj.min(), m + a * proj.max()
    if p0[0] > p1[0]: p0, p1 = p1, p0
    return p0, p1, len(pts) / (proj.max() - proj.min())

BROW = {s: axis('brow' + s) for s in 'LR'}
EYE = {s: bbox('eye' + s) for s in 'LR'}
MX0, MY0, MW, MH = bbox('mouth'); MOUTH = ((MX0 + 4, MY0 + MH / 2), (MX0 + MW - 4, MY0 + MH / 2))
STROKE = 10   # eye outlines on the measured face are ~9-10 px

# ---- blank face: brows, eyes and mouth erased (stubble kept around the mouth: only the mouth's own pixels are replaced)
blank = neutral.copy()
def erase_mask(mask, feather=6):
    m = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), feather)[..., None]; m = np.clip(m * 2.2, 0, 1)
    return (blank * (1 - m) + plate * m).astype(np.uint8)
for k in ['browL', 'browR', 'eyeL', 'eyeR']:
    x, y, w, h = bbox(k); mk = np.zeros((H, W), np.uint8); cv2.rectangle(mk, (x - 10, y - 10), (x + w + 10, y + h + 10), 1, -1); blank = erase_mask(mk)
pup = np.zeros((H, W), np.uint8)
for i in range(1, n):   # pupils
    if 80 < st[i, 4] < 400 and any(EYE[s][0] <= cen[i][0] <= EYE[s][0] + EYE[s][2] and EYE[s][1] <= cen[i][1] <= EYE[s][1] + EYE[s][3] for s in 'LR'): pup[lab == i] = 1
blank = erase_mask(cv2.dilate(pup, np.ones((9, 9), np.uint8)), 3)
mm = cv2.dilate((lab == C['mouth']).astype(np.uint8), np.ones((11, 11), np.uint8)); blank = erase_mask(mm, 3)
BLANK = Image.fromarray(cv2.cvtColor(blank, cv2.COLOR_BGR2RGB))

# ---- drawing helpers (in canonical px; scaled by SS)
def P(x, y): return (x * SS, y * SS)
class Pen:
    def __init__(s): s.im = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0)); s.d = ImageDraw.Draw(s.im)
    def line(s, pts, w=STROKE, col=INK):
        pts = [P(*p) for p in pts]; s.d.line(pts, fill=col + (255,), width=int(w * SS), joint='curve')
        r = w * SS / 2
        for (x, y) in (pts[0], pts[-1]): s.d.ellipse([x - r, y - r, x + r, y + r], fill=col + (255,))
    def taper(s, pts, w0, w1, col=INK, belly=0.0):
        pts = [np.array(p, float) for p in pts]; L, R = [], []; n = len(pts)
        for i, p in enumerate(pts):
            d = pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]; d = d / (np.linalg.norm(d) + 1e-9); nrm = np.array([-d[1], d[0]])
            u = i / (n - 1); w = (w0 + (w1 - w0) * u) * (1 + belly * math.sin(math.pi * u)) / 2; L.append(p + nrm * w); R.append(p - nrm * w)
        s.d.polygon([P(*q) for q in L + R[::-1]], fill=col + (255,))
        for (q, w) in ((pts[0], w0), (pts[-1], w1)): r = w * SS / 2; x, y = P(*q); s.d.ellipse([x - r, y - r, x + r, y + r], fill=col + (255,))
    def poly(s, pts, fill, outline=None, w=STROKE):
        s.d.polygon([P(*p) for p in pts], fill=fill + (255,))
        if outline: s.line(list(pts) + [pts[0]], w, outline)
    def ellipse(s, cx, cy, rx, ry, fill=None, outline=None, w=STROKE):
        box = [P(cx - rx, cy - ry), P(cx + rx, cy + ry)]
        if fill: s.d.ellipse(box, fill=fill + (255,))
        if outline: s.d.ellipse(box, outline=outline + (255,), width=int(w * SS))
def arc(cx, cy, rx, ry, a0, a1, k=24): return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / k)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / k))) for i in range(k + 1)]
def bez(p0, p1, p2, k=20): return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / k for i in range(k + 1)]]
def superellipse(cx, cy, rx, ry, e=3.0, k=48):
    pts = []
    for i in range(k):
        a = 2 * math.pi * i / k; c, s_ = math.cos(a), math.sin(a)
        pts.append((cx + rx * math.copysign(abs(c) ** (2 / e), c), cy + ry * math.copysign(abs(s_) ** (2 / e), s_)))
    return pts

# ---- paint: turn the clean supersampled drawing into the measured face's hand-painted pixels
# wobbly contours (smooth displacement), uneven stroke thickness (noisy threshold on a blurred mask), ragged pixel edges at the native
# resolution (fine-noise threshold, 1-px transition band) and the measured palette (one ink, one eye white) with a little per-pixel noise
def paint(im4, seed=7):
    rs = np.random.RandomState(seed); A = np.asarray(im4).astype(np.float32) / 255; H4, W4 = A.shape[:2]
    def field(step, amp):
        n = rs.randn(H4 // step + 3, W4 // step + 3).astype(np.float32); n = cv2.resize(n, (W4, H4), interpolation=cv2.INTER_CUBIC)
        return n / (np.abs(n).max() + 1e-6) * amp
    yy, xx = np.mgrid[0:H4, 0:W4].astype(np.float32)
    A = cv2.remap(A, xx + field(48, 8.0) + field(14, 2.6), yy + field(48, 8.0) + field(14, 2.6), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    a = A[..., 3]; rgb = A[..., :3]; lum = rgb @ np.array([0.299, 0.587, 0.114], np.float32)
    ink4 = a * (lum < 0.33); fill4 = a * (lum >= 0.33)
    inkT = cv2.GaussianBlur(ink4, (0, 0), 3.8) > np.clip(0.5 + field(52, 0.46) + field(18, 0.12), 0.14, 0.86)   # uneven thickness, bites
    fillT = cv2.GaussianBlur(fill4, (0, 0), 1.6) > 0.5
    down = lambda x: cv2.resize(x.astype(np.float32), (W, H), interpolation=cv2.INTER_AREA)
    ci, cf, a1 = down(inkT), down(fillT), down(fill4)
    fcol = down(rgb * fill4[..., None]) / np.maximum(a1[..., None], 1e-4)
    fine = lambda: rs.rand(H, W).astype(np.float32)
    ragged = lambda cov: np.clip((cov - (0.5 + (fine() - 0.5) * 0.42)) / 0.14 + 0.5, 0, 1)   # 1-px transition band, noisy threshold
    ai, af = ragged(ci), ragged(cf)
    fl = fcol @ np.array([0.299, 0.587, 0.114], np.float32); fs = fcol.max(-1) - fcol.min(-1); wh = (fl > 0.6) & (fs < 0.2)
    fcol[wh] = np.array(WHITE, np.float32) / 255   # flat paint, like the measured face
    inkc = np.array(INK, np.float32) / 255
    col = fcol * (1 - ai[..., None]) + inkc * ai[..., None]; alpha = np.maximum(af, ai)
    out = np.dstack([np.clip(col, 0, 1), alpha]); return Image.fromarray((out * 255).astype(np.uint8), 'RGBA')

def jitter_poly(pts, k, amp, seed):   # resample a closed shape to k points and push each in/out: a hand-drawn polygon
    r = np.random.RandomState(seed); n = len(pts); cx = sum(p[0] for p in pts) / n; cy = sum(p[1] for p in pts) / n; out = []
    for i in range(k):
        x, y = pts[int(i * n / k)]; f = 1 + (r.rand() - 0.5) * 2 * amp; out.append((cx + (x - cx) * f, cy + (y - cy) * f))
    return out

# ---- features
def brow(pen, side, dy=0, rot=0, bulge=0, thick=1.0, dx=0):   # rot > 0 lifts the inner end (worried), < 0 lowers it (angry)
    p0, p1, th = BROW[side]; m = (p0 + p1) / 2
    def tr(p):
        q = p - m; a = math.radians(-rot); q = np.array([q[0] * math.cos(a) - q[1] * math.sin(a), q[0] * math.sin(a) + q[1] * math.cos(a)]); return q + m + [dx, dy]
    a, b = tr(p0), tr(p1); mid = (a + b) / 2; nrm = np.array([-(b - a)[1], (b - a)[0]]); nrm = nrm / np.linalg.norm(nrm)
    if nrm[1] > 0: nrm = -nrm   # bulge > 0 arches upward
    inner_first = (side == 'L') == (a[0] > b[0])   # the inner end (toward the nose) is the thick one
    pts = bez(tuple(a), tuple(mid + nrm * (bulge + 4)), tuple(b), k=16)
    w_in, w_out = th * 1.12 * thick, th * 0.62 * thick
    pen.taper(pts, w_in if inner_first else w_out, w_out if inner_first else w_in, belly=0.12)

def eye(pen, side, kind='open', s=1.0, pupil=(0, 0), lid=0.0, low=0.0, psize=1.0, shine=False):
    x, y, w, h = EYE[side]; cx, cy = x + w / 2, y + h / 2; rx, ry = (w / 2 - STROKE / 2) * s, (h / 2 - STROKE / 2) * s
    if kind == 'open':
        shape = jitter_poly(superellipse(cx, cy, rx, ry, 3.4, k=56), 8, 0.07, int(cx * 7 + cy))
        shape = [p for i in range(len(shape)) for p in (shape[i], ((shape[i][0] * 2 + shape[(i + 1) % len(shape)][0]) / 3, (shape[i][1] * 2 + shape[(i + 1) % len(shape)][1]) / 3))]
        pen.poly(shape, WHITE)
        prx, pry = (6.5 if side == 'L' else 5) * psize, (11.5 if side == 'L' else 7.5) * psize
        px, py = cx + pupil[0] * (rx - prx - 4), cy + pupil[1] * (ry - pry - 4)
        pen.poly(jitter_poly(superellipse(px, py, prx, pry, 2.8, k=24), 6, 0.16, int(px * 3 + py)), INK)
        if shine: pen.ellipse(px - prx * 0.35, py - pry * 0.4, prx * 0.35, pry * 0.25, fill=(255, 255, 255))
        if lid > 0:   # upper lid: skin over the top of the eye, ink lid line
            ly = cy - ry + 2 * ry * lid; pen.poly([(cx - rx - 8, cy - ry - 10), (cx + rx + 8, cy - ry - 10), (cx + rx + 8, ly), (cx - rx - 8, ly)], (211, 163, 117))
            pen.line([(cx - rx - 2, ly), (cx + rx + 2, ly)])
        if low > 0:
            ly = cy + ry - 2 * ry * low; pen.poly([(cx - rx - 8, ly), (cx + rx + 8, ly), (cx + rx + 8, cy + ry + 10), (cx - rx - 8, cy + ry + 10)], (211, 163, 117))
            pen.line(bez((cx - rx - 2, ly + 4), (cx, ly - 10), (cx + rx + 2, ly + 4)))
        pen.line(shape + [shape[0]], w=STROKE)
    elif kind == 'closed': pen.line(bez((cx - rx, cy), (cx, cy + ry * 0.55), (cx + rx, cy)))
    elif kind == 'happy': pen.line(bez((cx - rx, cy + ry * 0.35), (cx, cy - ry * 0.95), (cx + rx, cy + ry * 0.35)))
    elif kind == 'flat': pen.line([(cx - rx, cy), (cx + rx, cy)])
    elif kind == 'squeeze':
        d = 1 if side == 'L' else -1
        pen.line([(cx - d * rx, cy - ry * 0.7), (cx + d * rx * 0.6, cy), (cx - d * rx, cy + ry * 0.7)])
    elif kind == 'x':
        pen.line([(cx - rx * 0.7, cy - ry * 0.7), (cx + rx * 0.7, cy + ry * 0.7)]); pen.line([(cx + rx * 0.7, cy - ry * 0.7), (cx - rx * 0.7, cy + ry * 0.7)])
    elif kind == 'spiral':
        pts = [(cx + (2 + 3.2 * t) * math.cos(t) * rx / 22, cy + (2 + 3.2 * t) * math.sin(t) * ry / 22) for t in [i * 0.25 for i in range(int(4.2 * math.pi / 0.25))]]
        pen.line(pts, w=STROKE * 0.75)
    elif kind == 'heart':
        r = min(rx, ry) * 1.05; pts = [(cx + r * 16 * math.sin(t) ** 3 / 16, cy - r * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 16) for t in [i * math.pi / 30 for i in range(60)]]
        pen.poly(pts, RED, outline=INK, w=STROKE * 0.8)
    elif kind == 'star':
        r = min(rx, ry) * 1.15; pts = [(cx + (r if i % 2 == 0 else r * 0.45) * math.sin(i * math.pi / 5), cy - (r if i % 2 == 0 else r * 0.45) * math.cos(i * math.pi / 5)) for i in range(10)]
        pen.poly(pts, (245, 200, 60), outline=INK, w=STROKE * 0.8)

def mouth(pen, kind='line', dx=0, dy=0, w=1.0, curve=0.0, tilt=0.0):
    (x0, y0), (x1, y1) = MOUTH; cx = (x0 + x1) / 2 + dx; cy = (y0 + y1) / 2 + dy; hw = (x1 - x0) / 2 * w
    L, R = (cx - hw, cy + tilt), (cx + hw, cy - tilt)
    if kind == 'line': pen.taper(bez(L, (cx, cy + curve), R, k=16), 13, 12, belly=0.25)
    elif kind == 'smile': pen.line(bez(L, (cx, cy + 46 * (curve or 1)), R), w=16)
    elif kind == 'frown': pen.line(bez((L[0], L[1] + 10), (cx, cy - 40 * (curve or 1)), (R[0], R[1] + 10)), w=16)
    elif kind == 'smirk': pen.line(bez((cx - hw * 0.9, cy + 6), (cx + hw * 0.2, cy + 14), (cx + hw, cy - 26)), w=16)
    elif kind == 'wavy': pen.line([(cx - hw + i * 2 * hw / 24, cy + 9 * math.sin(i * math.pi / 3)) for i in range(25)], w=14)
    elif kind in ('open', 'laugh', 'bigsmile', 'sob', 'yawn', 'O', 'o', 'grimace', 'clench', 'evil', 'tongueout'):
        if kind == 'O': shape = arc(cx, cy + 8, hw * 0.32, 44, 0, 360)
        elif kind == 'o': shape = arc(cx, cy + 4, hw * 0.16, 18, 0, 360)
        elif kind == 'yawn': shape = arc(cx, cy + 18, hw * 0.38, 70, 0, 360)
        elif kind in ('laugh', 'bigsmile', 'tongueout'): top = cy - 6; shape = [(cx - hw, top)] + [(cx - hw + 2 * hw * i / 24, top + (78 if kind == 'laugh' else 58) * math.sin(math.pi * i / 24)) for i in range(25)] + [(cx + hw, top)]
        elif kind == 'sob': shape = [(cx - hw * 0.8, cy + 4), (cx - hw * 0.35, cy - 18), (cx, cy - 8), (cx + hw * 0.35, cy - 18), (cx + hw * 0.8, cy + 4), (cx + hw * 0.55, cy + 62), (cx - hw * 0.55, cy + 62)]
        elif kind in ('grimace', 'clench', 'evil'): hh = 18 if kind != 'evil' else 14; shape = [(cx - hw * (1.1 if kind == 'evil' else 1), cy - hh), (cx + hw * (1.1 if kind == 'evil' else 1), cy - hh - (10 if kind == 'evil' else 0)), (cx + hw * (1.05 if kind == 'evil' else 1), cy + hh), (cx - hw * (1.05 if kind == 'evil' else 1), cy + hh)]
        else: shape = arc(cx, cy + 10, hw * 0.6, 34, 0, 360)
        inside = WHITE if kind in ('grimace', 'clench', 'evil') else MOUTH_IN
        pen.poly(shape, inside)
        if kind in ('laugh', 'bigsmile', 'tongueout'):   # teeth strip and tongue
            pen.poly([(cx - hw * 0.86, cy - 4), (cx + hw * 0.86, cy - 4), (cx + hw * 0.8, cy + 10), (cx - hw * 0.8, cy + 10)], WHITE)
            if kind != 'bigsmile': pen.ellipse(cx + 8, cy + (48 if kind == 'laugh' else 40), hw * 0.42, 18, fill=TONGUE)
        if kind in ('grimace', 'clench'):
            for i in range(1, 6): xx = cx - hw + 2 * hw * i / 6; pen.line([(xx, cy - 18), (xx, cy + 18)], w=6)
            pen.line([(cx - hw, cy), (cx + hw, cy)], w=6)
        if kind == 'yawn': pen.ellipse(cx, cy + 58, hw * 0.24, 16, fill=TONGUE)
        pen.line(shape + [shape[0]], w=13)
        if kind == 'tongueout': pass
    elif kind == 'tongue':
        pen.ellipse(cx + 18, cy + 28, 26, 32, fill=TONGUE, outline=INK, w=10); pen.line(bez(L, (cx, cy + 10), R), w=16); pen.line([(cx + 18, cy + 8), (cx + 18, cy + 38)], w=6, col=(170, 60, 70))
    elif kind == 'pout': pen.line(bez((cx - hw * 0.35, cy + 6), (cx, cy - 18), (cx + hw * 0.35, cy + 6)), w=17); pen.line(bez((cx - hw * 0.3, cy + 12), (cx, cy + 26), (cx + hw * 0.3, cy + 12)), w=12)
    elif kind == 'kiss': pen.line(bez((cx - 16, cy - 22), (cx + 18, cy - 12), (cx - 6, cy)), w=13); pen.line(bez((cx - 6, cy), (cx + 22, cy + 12), (cx - 14, cy + 22)), w=13)
    elif kind == 'whistle': pen.ellipse(cx + 20, cy + 2, 14, 16, fill=MOUTH_IN, outline=INK, w=11)
    elif kind == 'drool': pen.line(bez(L, (cx, cy + 20), R), w=16); pen.line(bez((cx + hw * 0.7, cy + 8), (cx + hw * 0.75, cy + 40), (cx + hw * 0.7, cy + 76)), w=9, col=TEAR); pen.ellipse(cx + hw * 0.7, cy + 80, 8, 9, fill=TEAR)

def extra(pen, kind):
    if kind == 'tears':
        for s in 'LR':
            x, y, w, h = EYE[s]; cx, by = x + w / 2, y + h - 8
            pen.line(bez((cx - 8, by), (cx - 16, by + 90), (cx - 4, by + 170)), w=14, col=TEAR); pen.ellipse(cx - 4, by + 182, 10, 14, fill=TEAR)
    elif kind == 'tear':
        x, y, w, h = EYE['L']; pen.ellipse(x + w / 2 - 10, y + h + 26, 10, 15, fill=TEAR, outline=INK, w=4)
    elif kind == 'sweat':
        cx, cy = 352, 232; pen.poly([(cx, cy - 34)] + arc(cx, cy + 6, 20, 22, -20, 200), TEAR, outline=INK, w=5)
        pen.ellipse(cx - 6, cy + 2, 4, 7, fill=(255, 255, 255))
    elif kind == 'blush':
        for (cx, cy) in [(92, 450), (318, 640)]:
            pen.ellipse(cx, cy, 44, 22, fill=BLUSH)
            for k in range(3): pen.line([(cx - 22 + k * 18, cy + 8), (cx - 12 + k * 18, cy - 8)], w=5, col=(200, 80, 80))
    elif kind == 'vein':
        cx, cy = 300, 205
        for a in (0, 90, 180, 270): pen.line(bez((cx + 30 * math.cos(math.radians(a + 20)), cy + 30 * math.sin(math.radians(a + 20))), (cx, cy), (cx + 30 * math.cos(math.radians(a - 20)), cy + 30 * math.sin(math.radians(a - 20)))), w=8, col=RED)
    elif kind == 'shadow':   # blue gloom over the forehead (horror / dread)
        for k in range(5): pen.line([(30 + k * 70, 70), (60 + k * 70, 230)], w=10, col=(100, 120, 190))

# ---- expressions (name -> recipe)
def E(**kw): return kw
X = {
 'laugh':     E(brows=dict(L=dict(dy=-14), R=dict(dy=-14)), eyes=dict(L=dict(kind='squeeze'), R=dict(kind='squeeze')), mouth=dict(kind='laugh')),
 'cry':       E(brows=dict(L=dict(dy=-4, rot=18), R=dict(dy=-4, rot=-18)), eyes=dict(L=dict(kind='closed'), R=dict(kind='closed')), mouth=dict(kind='sob'), extras=['tears']),
 'sob':       E(brows=dict(L=dict(dy=-10, rot=22), R=dict(dy=-10, rot=-22)), eyes=dict(L=dict(pupil=(0, 0.3), s=1.05), R=dict(pupil=(0, 0.3), s=1.05)), mouth=dict(kind='wavy'), extras=['tears']),
 'wink':      E(brows=dict(L=dict(dy=-12), R=dict(dy=8)), eyes=dict(L=dict(), R=dict(kind='happy')), mouth=dict(kind='smirk')),
 'tongue':    E(brows=dict(L=dict(dy=-8), R=dict(dy=-8)), eyes=dict(L=dict(kind='happy'), R=dict(kind='closed')), mouth=dict(kind='tongue')),
 'rage':      E(brows=dict(L=dict(dy=16, rot=-24, thick=1.25), R=dict(dy=12, rot=22, thick=1.25)), eyes=dict(L=dict(lid=0.42, psize=0.7), R=dict(lid=0.38, psize=0.7)), mouth=dict(kind='clench'), extras=['vein']),
 'love':      E(brows=dict(L=dict(dy=-12), R=dict(dy=-12)), eyes=dict(L=dict(kind='heart'), R=dict(kind='heart')), mouth=dict(kind='smile'), extras=['blush']),
 'dizzy':     E(brows=dict(L=dict(dy=-6, rot=10), R=dict(dy=-6, rot=-10)), eyes=dict(L=dict(kind='spiral'), R=dict(kind='spiral')), mouth=dict(kind='wavy')),
 'nervous':   E(brows=dict(L=dict(dy=-14, rot=14), R=dict(dy=-6, rot=-10)), eyes=dict(L=dict(pupil=(0.5, 0)), R=dict(pupil=(0.5, 0))), mouth=dict(kind='wavy', w=0.8), extras=['sweat']),
 'proud':     E(brows=dict(L=dict(dy=-16), R=dict(dy=-16)), eyes=dict(L=dict(kind='closed'), R=dict(kind='closed')), mouth=dict(kind='smile', curve=0.7)),
 'pout':      E(brows=dict(L=dict(dy=6, rot=-8), R=dict(dy=6, rot=8)), eyes=dict(L=dict(lid=0.25), R=dict(lid=0.25)), mouth=dict(kind='pout')),
 'yawn':      E(brows=dict(L=dict(dy=-8, rot=12), R=dict(dy=-8, rot=-12)), eyes=dict(L=dict(kind='squeeze'), R=dict(kind='squeeze')), mouth=dict(kind='yawn')),
 'kiss':      E(brows=dict(L=dict(dy=-10), R=dict(dy=-10)), eyes=dict(L=dict(kind='closed'), R=dict(kind='closed')), mouth=dict(kind='kiss'), extras=['blush']),
 'blush':     E(brows=dict(L=dict(dy=-6, rot=10), R=dict(dy=-6, rot=-10)), eyes=dict(L=dict(pupil=(0, 0.4)), R=dict(pupil=(0, 0.4))), mouth=dict(kind='line', w=0.6, curve=12), extras=['blush']),
 'sweat':     E(brows=dict(L=dict(dy=-4, rot=8), R=dict(dy=-4, rot=-8)), eyes=dict(L=dict(lid=0.2), R=dict(lid=0.2)), mouth=dict(kind='line', curve=-6), extras=['sweat']),
 'whistle':   E(brows=dict(L=dict(dy=-10), R=dict(dy=-10)), eyes=dict(L=dict(pupil=(0.45, -0.55)), R=dict(pupil=(0.45, -0.55))), mouth=dict(kind='whistle')),
 'lookSide':  E(eyes=dict(L=dict(pupil=(0.75, 0)), R=dict(pupil=(0.75, 0))), mouth=dict(kind='line')),
 'lookLeft':  E(eyes=dict(L=dict(pupil=(-0.75, 0)), R=dict(pupil=(-0.75, 0))), mouth=dict(kind='line')),
 'lookUp':    E(brows=dict(L=dict(dy=-8), R=dict(dy=-8)), eyes=dict(L=dict(pupil=(0.1, -0.75)), R=dict(pupil=(0.1, -0.75))), mouth=dict(kind='line')),
 'lookDown':  E(eyes=dict(L=dict(pupil=(0, 0.75), lid=0.25), R=dict(pupil=(0, 0.75), lid=0.25)), mouth=dict(kind='line')),
 'starEyes':  E(brows=dict(L=dict(dy=-16), R=dict(dy=-16)), eyes=dict(L=dict(kind='star'), R=dict(kind='star')), mouth=dict(kind='bigsmile')),
 'smirk':     E(brows=dict(L=dict(dy=-10), R=dict(dy=6, rot=8)), eyes=dict(L=dict(lid=0.35, pupil=(0.3, 0)), R=dict(lid=0.3, pupil=(0.3, 0))), mouth=dict(kind='smirk')),
 'confused':  E(brows=dict(L=dict(dy=-18, rot=10), R=dict(dy=10, rot=10)), eyes=dict(L=dict(s=1.1), R=dict(s=0.9)), mouth=dict(kind='wavy', w=0.7)),
 'determined':E(brows=dict(L=dict(dy=12, rot=-18, thick=1.2), R=dict(dy=10, rot=16, thick=1.2)), eyes=dict(L=dict(lid=0.3), R=dict(lid=0.3)), mouth=dict(kind='line', w=0.8, curve=-8)),
 'eyeRoll':   E(brows=dict(L=dict(dy=-6), R=dict(dy=4)), eyes=dict(L=dict(pupil=(0.2, -0.85), lid=0.3), R=dict(pupil=(0.2, -0.85), lid=0.3)), mouth=dict(kind='line', tilt=8)),
 'awe':       E(brows=dict(L=dict(dy=-20), R=dict(dy=-20)), eyes=dict(L=dict(s=1.25, psize=1.4, shine=True), R=dict(s=1.4, psize=1.4, shine=True)), mouth=dict(kind='O')),
 'sneaky':    E(brows=dict(L=dict(dy=8, rot=-14), R=dict(dy=6, rot=12)), eyes=dict(L=dict(lid=0.55, pupil=(0.6, 0.3)), R=dict(lid=0.5, pupil=(0.6, 0.3))), mouth=dict(kind='smirk')),
 'pain':      E(brows=dict(L=dict(dy=6, rot=20), R=dict(dy=6, rot=-20)), eyes=dict(L=dict(kind='squeeze'), R=dict(kind='squeeze')), mouth=dict(kind='grimace')),
 'disgust':   E(brows=dict(L=dict(dy=8, rot=-10), R=dict(dy=-6, rot=-6)), eyes=dict(L=dict(lid=0.55), R=dict(s=1.05)), mouth=dict(kind='tongue', dx=-10)),
 'relieved':  E(brows=dict(L=dict(dy=-6, rot=10), R=dict(dy=-6, rot=-10)), eyes=dict(L=dict(kind='closed'), R=dict(kind='closed')), mouth=dict(kind='smile', curve=0.5), extras=['sweat']),
 'drool':     E(brows=dict(L=dict(dy=4), R=dict(dy=4)), eyes=dict(L=dict(kind='closed'), R=dict(kind='closed')), mouth=dict(kind='drool')),
 'squint':    E(brows=dict(L=dict(dy=10, rot=-6), R=dict(dy=8, rot=6)), eyes=dict(L=dict(lid=0.6, low=0.15), R=dict(lid=0.55, low=0.15)), mouth=dict(kind='line', w=0.8, curve=-6)),
 'cold':      E(brows=dict(L=dict(dy=-8, rot=16), R=dict(dy=-8, rot=-16)), eyes=dict(L=dict(lid=0.2, pupil=(0, 0.2)), R=dict(lid=0.2, pupil=(0, 0.2))), mouth=dict(kind='clench', w=0.8)),
 'surprisedHappy': E(brows=dict(L=dict(dy=-20), R=dict(dy=-20)), eyes=dict(L=dict(s=1.2), R=dict(s=1.35)), mouth=dict(kind='bigsmile')),
 'evil':      E(brows=dict(L=dict(dy=12, rot=-22), R=dict(dy=10, rot=20)), eyes=dict(L=dict(lid=0.5, pupil=(0, 0.3)), R=dict(lid=0.45, pupil=(0, 0.3))), mouth=dict(kind='evil')),
 'puppy':     E(brows=dict(L=dict(dy=-16, rot=22), R=dict(dy=-16, rot=-22)), eyes=dict(L=dict(s=1.15, psize=1.7, shine=True), R=dict(s=1.25, psize=1.7, shine=True)), mouth=dict(kind='frown', curve=0.5, w=0.6)),
 'worried':   E(brows=dict(L=dict(dy=-10, rot=18), R=dict(dy=-10, rot=-18)), eyes=dict(L=dict(pupil=(0, 0.3)), R=dict(pupil=(0, 0.3))), mouth=dict(kind='wavy', w=0.75)),
 'disgusted': E(brows=dict(L=dict(dy=10, rot=-12), R=dict(dy=-4)), eyes=dict(L=dict(lid=0.5), R=dict(lid=0.15)), mouth=dict(kind='frown', curve=0.6, tilt=10)),
 'dead':      E(eyes=dict(L=dict(kind='x'), R=dict(kind='x')), mouth=dict(kind='tongue')),
 'smug':      E(brows=dict(L=dict(dy=-12), R=dict(dy=-2)), eyes=dict(L=dict(lid=0.45, pupil=(0.25, 0.2)), R=dict(lid=0.4, pupil=(0.25, 0.1))), mouth=dict(kind='smirk')),
 'bigGrin':   E(brows=dict(L=dict(dy=-14), R=dict(dy=-14)), eyes=dict(L=dict(kind='happy'), R=dict(kind='happy')), mouth=dict(kind='bigsmile')),
 'tongueOut': E(brows=dict(L=dict(dy=-12), R=dict(dy=-12)), eyes=dict(L=dict(kind='squeeze'), R=dict(kind='squeeze')), mouth=dict(kind='tongueout')),
}

def render(rec):
    pen = Pen()
    for s in 'LR': brow(pen, s, **(rec.get('brows', {}).get(s, {})))
    for s in 'LR': eye(pen, s, **(rec.get('eyes', {}).get(s, {})))
    mouth(pen, **rec.get('mouth', {}))
    for e in rec.get('extras', []): extra(pen, e)
    ov = paint(pen.im, seed=sum(map(ord, str(rec))) % 9973)
    out = BLANK.copy().convert('RGBA'); out.alpha_composite(ov); return out.convert('RGB')

# ---- variants: <name>_blink (eyes closed, brows and mouth kept) and <name>_clean (no stubble), for every expression
MEASURED = ['neutral', 'skeptical', 'unimpressed', 'surprised', 'shocked', 'angry', 'sad', 'happy', 'sleepy', 'blink', 'scared', 'talk', 'talkWide', 'grin']
CLOSED = {'happy', 'sleepy', 'blink', 'laugh', 'cry', 'tongue', 'proud', 'yawn', 'kiss', 'relieved', 'drool', 'pain', 'bigGrin', 'tongueOut', 'dead', 'dizzy', 'love', 'starEyes'}
ys, xs = np.mgrid[0:H, 0:W]
def stubble_mask(bgr):   # small dark marks in the lower face that are not part of the mouth (largest marks) or the nose
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY); n2, lab2, st2, cen2 = cv2.connectedComponentsWithStats(((g < 125) & (ys > 690)).astype(np.uint8), 8); m = np.zeros((H, W), np.uint8)
    for i in range(1, n2):
        x, y, w, h, a = st2[i]; cx, cy = cen2[i]
        nose = 180 < cx < 250 and 660 < cy < 712
        mouthlike = a >= 260 and 760 < cy < 930 and 60 < cx < 360
        if not nose and not mouthlike: m[lab2 == i] = 1
    return cv2.dilate(m, np.ones((5, 5), np.uint8))
def clean(rgb_img):
    bgr = cv2.cvtColor(np.array(rgb_img), cv2.COLOR_RGB2BGR); m = cv2.GaussianBlur(stubble_mask(bgr).astype(np.float32), (0, 0), 1.5)[..., None]; m = np.clip(m * 1.6, 0, 1)
    out = (bgr * (1 - m) + plate * m).astype(np.uint8); return Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
def blinked(rgb_img):
    bgr = cv2.cvtColor(np.array(rgb_img), cv2.COLOR_RGB2BGR); mk = np.zeros((H, W), np.uint8)
    for s in 'LR':
        x, y, w, h = EYE[s]; cv2.rectangle(mk, (x - 22, y - 16), (x + w + 22, y + h + 26), 1, -1)
    m = cv2.GaussianBlur(mk.astype(np.float32), (0, 0), 5)[..., None]; m = np.clip(m * 2.0, 0, 1)
    base = Image.fromarray(cv2.cvtColor((bgr * (1 - m) + plate * m).astype(np.uint8), cv2.COLOR_BGR2RGB)).convert('RGBA')
    pen = Pen()
    for s in 'LR': eye(pen, s, kind='closed')
    base.alpha_composite(paint(pen.im, seed=11)); return base.convert('RGB')
def save(img, name): img.quantize(colors=112, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(os.path.join(D, 'expressions', f'face_{name}.png'), optimize=True)

if __name__ == '__main__':
    lm_path = os.path.join(D, 'face_landmarks.json'); lm = json.load(open(lm_path))
    names = list(X)
    for nm in names:
        save(render(X[nm]), nm)
        lm['expressions'][nm] = {'status': 'designed', 'from_source': 'neutral', 'tool': 'tools/face/gen_expressions.py'}
    variants = 0
    for nm in MEASURED + names:
        img = Image.open(os.path.join(D, 'expressions', f'face_{nm}.png')).convert('RGB')
        save(clean(img), nm + '_clean'); lm['expressions'][nm + '_clean'] = {'status': 'designed', 'from_source': nm, 'variant': 'clean'}; variants += 1
        if nm not in CLOSED:
            b = blinked(img); save(b, nm + '_blink'); save(clean(b), nm + '_clean_blink'); variants += 2
            lm['expressions'][nm + '_blink'] = {'status': 'designed', 'from_source': nm, 'variant': 'blink'}; lm['expressions'][nm + '_clean_blink'] = {'status': 'designed', 'from_source': nm, 'variant': 'clean+blink'}
    json.dump(lm, open(lm_path, 'w'), indent=1)
    if '--sheet' in sys.argv:
        out = sys.argv[sys.argv.index('--sheet') + 1]; cols = 9; tw, th = 133, 360
        allnames = sys.argv[sys.argv.index('--sheet') + 2].split(',') if len(sys.argv) > sys.argv.index('--sheet') + 2 else ['neutral'] + names
        sheet = Image.new('RGB', (cols * tw, ((len(allnames) + cols - 1) // cols) * (th + 22)), 'white'); dr = ImageDraw.Draw(sheet)
        for i, nm in enumerate(allnames):
            im = Image.open(os.path.join(D, 'expressions', f'face_{nm}.png')).convert('RGB').resize((tw, th)); x, y = (i % cols) * tw, (i // cols) * (th + 22)
            sheet.paste(im, (x, y)); dr.text((x + 4, y + th + 4), nm, fill=(0, 0, 0))
        sheet.save(out, quality=90)
    print(len(names), 'expressions,', variants, 'variants written')
