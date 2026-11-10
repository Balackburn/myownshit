#!/usr/bin/env python3
"""Face rig for le mec: the painted face split into layers that the engine composes and animates at runtime (engine/facerig.js).

The neutral face is the MEASURED one: its own brows, eye outlines, eye whites, pupils and mouth are cut out of face_neutral.png as
sprites, so the rig at rest gives back the original pixels. Everything else is drawn with the same ink and the same paint pass as
tools/face/gen_expressions.py (imported): bigger eyes that keep the measured silhouette and the measured stroke width, lid lines
(the original draws a half-closed eye as a thick flat line with the lower part of the eye under it: the engine clips the eye and moves
that line, so lids are continuous), special eyes, pupils, every mouth shape, brows, cheeks and extras.
Writes characters/lemec/face/rig/: blank.png, blank_clean.png, sprites.png (atlas) and rig.json (rects, anchors, presets: every
expression of the face set as rig parameters).
Run: python3 tools/face/gen_rig.py [--sheet out.jpg]"""
import json, math, os, sys
import cv2, numpy as np
import scipy.ndimage as ndi
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_expressions as G

OUT = os.path.join(G.D, 'rig'); os.makedirs(OUT, exist_ok=True)
W, H, SS, STROKE, INK, WHITE = G.W, G.H, G.SS, G.STROKE, G.INK, G.WHITE
GREEN = (62, 138, 74)
BIGWHITE = (236, 229, 212)
sprites = {}   # name -> (RGBA image cropped, x, y)

def crop(im, pad=4):
    a = np.asarray(im)[..., 3]; ys, xs = np.nonzero(a > 6)
    if len(xs) == 0: return None
    x0, x1, y0, y1 = max(0, xs.min() - pad), min(W, xs.max() + 1 + pad), max(0, ys.min() - pad), min(H, ys.max() + 1 + pad)
    return im.crop((x0, y0, x1, y1)), int(x0), int(y0)
def put(name, im):
    c = crop(im)
    if c: sprites[name] = c
    return c
def add(name, pen, seed): return put(name, G.paint(pen.im, seed=seed))

# ---- measured features: the neutral face's own ink (flat ink colour, alpha from the grey level: the measured ragged edge is kept)
def ink_sprite(mask, col=INK, grow=2):
    reg = cv2.dilate(mask.astype(np.uint8), np.ones((2 * grow + 1, 2 * grow + 1), np.uint8)) > 0
    a = np.clip((150 - G.gray.astype(np.float32)) / 60, 0, 1) * reg
    im = np.zeros((H, W, 4), np.uint8); im[..., :3] = col; im[..., 3] = (a * 255).astype(np.uint8); return Image.fromarray(im, 'RGBA')
def fill_sprite(mask, col=WHITE):
    im = np.zeros((H, W, 4), np.uint8); im[..., :3] = col; im[..., 3] = (mask * 255).astype(np.uint8); return Image.fromarray(im, 'RGBA')
EYEM = {}
for side in 'LR':
    ring = G.lab == G.C['eye' + side]; filled = ndi.binary_fill_holes(ring); x, y, w, h = G.EYE[side]
    pm = np.zeros((H, W), bool); pc = None
    for i in range(1, G.n):
        if 80 < G.st[i, 4] < 400 and x <= G.cen[i][0] <= x + w and y <= G.cen[i][1] <= y + h: pm |= G.lab == i; pc = G.cen[i]
    EYEM[side] = dict(ring=ring, filled=filled, pupil=pm, pc=pc, cx=x + w / 2, cy=y + h / 2, w=w, h=h, x=x, y=y)

def eye_geom(side):
    e = EYEM[side]; rx, ry = e['w'] / 2 - STROKE / 2, e['h'] / 2 - STROKE / 2
    prx, pry = (6.5, 11.5) if side == 'L' else (5, 7.5)
    return e['cx'], e['cy'], rx, ry, prx, pry

def scaled_eye(side, s, seed):
    """the measured eye silhouette at scale s, with the measured stroke width: white under, ink ring over (same paint seed: aligned)"""
    e = EYEM[side]; cx, cy = e['cx'], e['cy']
    M = np.float32([[SS * s, 0, SS * (cx - s * cx)], [0, SS * s, SS * (cy - s * cy)]])
    big = cv2.warpAffine(e['filled'].astype(np.float32), M, (W * SS, H * SS), flags=cv2.INTER_CUBIC) > 0.5
    r = int((STROKE - 1) * SS); k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    inner = cv2.erode(big.astype(np.uint8), k) > 0; ring = big & ~inner
    def rgba(mask, col):
        im = np.zeros((H * SS, W * SS, 4), np.uint8); im[..., :3] = col; im[..., 3] = mask * 255; return Image.fromarray(im, 'RGBA')
    u = G.paint(rgba(big, WHITE), seed)
    if s >= 1.4: a = np.array(u); a[..., :3] = BIGWHITE; u = Image.fromarray(a, 'RGBA')   # wide-open eyes: a lighter white, so a take reads at phone size
    return u, G.paint(rgba(ring, INK), seed)

SIZES = [1.0, 1.25, 1.5, 1.9]
KINDS = ['closed', 'happy', 'flat', 'squeeze', 'x', 'spiral', 'heart', 'star']   # drawn by gen_expressions.eye
NEWKINDS = ['dot', 'euro']
PSIZES = [0.6, 1.0, 1.4, 1.7]
BROWS = {'arch': dict(bulge=14), 'bold': dict(bulge=0, thick=1.25), 'straight': dict(bulge=0)}   # 'flat' is the measured brow
MOUTHS = {'line_m12': dict(kind='line', curve=-12), 'line_m6': dict(kind='line', curve=-6), 'line_p6': dict(kind='line', curve=6), 'line_p12': dict(kind='line', curve=12), 'line_p20': dict(kind='line', curve=20),
          'smile': dict(kind='smile'), 'smile_05': dict(kind='smile', curve=0.5), 'smile_07': dict(kind='smile', curve=0.7), 'frown': dict(kind='frown'), 'frown_05': dict(kind='frown', curve=0.55),
          'smirk': dict(kind='smirk'), 'wavy': dict(kind='wavy'), 'open': dict(kind='open'), 'laugh': dict(kind='laugh'), 'bigsmile': dict(kind='bigsmile'), 'sob': dict(kind='sob'), 'yawn': dict(kind='yawn'),
          'O': dict(kind='O'), 'o': dict(kind='o'), 'grimace': dict(kind='grimace'), 'clench': dict(kind='clench'), 'evil': dict(kind='evil'), 'tongue': dict(kind='tongue'), 'tongueout': dict(kind='tongueout'),
          'pout': dict(kind='pout'), 'kiss': dict(kind='kiss'), 'whistle': dict(kind='whistle'), 'drool': dict(kind='drool')}
EXTRAS = ['tears', 'tear', 'sweat', 'blush', 'vein', 'shadow']

def new_mouth(pen, kind):
    (x0, y0), (x1, y1) = G.MOUTH; cx, cy, hw = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2
    if kind == 'scream':   # the mouth of a take: tall, teeth on top, uvula, tongue at the bottom
        top, bot = cy - 26, cy + 168
        shape = [(cx - hw * 0.78, top)] + G.bez((cx + hw * 0.78, top), (cx + hw * 0.92, (top + bot) / 2), (cx + hw * 0.5, bot), k=10) + G.bez((cx + hw * 0.5, bot), (cx, bot + 22), (cx - hw * 0.5, bot), k=8) + G.bez((cx - hw * 0.5, bot), (cx - hw * 0.92, (top + bot) / 2), (cx - hw * 0.78, top), k=10)
        pen.poly(shape, G.MOUTH_IN)
        pen.poly([(cx - hw * 0.66, top + 4), (cx + hw * 0.66, top + 4), (cx + hw * 0.6, top + 24), (cx - hw * 0.6, top + 24)], WHITE)
        pen.ellipse(cx, top + 56, 9, 20, fill=(176, 66, 70)); pen.ellipse(cx + 4, bot - 26, hw * 0.4, 30, fill=G.TONGUE)
        pen.line([(cx + 4, bot - 46), (cx + 4, bot - 10)], w=6, col=(170, 60, 70)); pen.line(shape + [shape[0]], w=13)
    elif kind == 'zigzag': pen.line([(cx - hw + i * 2 * hw / 8, cy + (13 if i % 2 else -13)) for i in range(9)], w=12)
    elif kind == 'teeth':   # a wide smile showing two rows of teeth
        shape = [(cx - hw * 1.02, cy - 20)] + G.bez((cx + hw * 1.02, cy - 20), (cx + hw * 0.8, cy + 44), (cx, cy + 50), k=10) + G.bez((cx, cy + 50), (cx - hw * 0.8, cy + 44), (cx - hw * 1.02, cy - 20), k=10)
        pen.poly(shape, WHITE)
        for i in range(1, 7): xx = cx - hw + 2 * hw * i / 7; pen.line([(xx, cy - 18), (xx, cy + 40)], w=5)
        pen.line(G.bez((cx - hw, cy + 6), (cx, cy + 22), (cx + hw, cy + 6)), w=5); pen.line(shape + [shape[0]], w=13)
    elif kind == 'gulp': pen.line(G.bez((cx - hw * 0.5, cy - 4), (cx, cy + 6), (cx + hw * 0.5, cy - 4)), w=13); pen.line(G.bez((cx - hw * 0.28, cy + 20), (cx, cy + 28), (cx + hw * 0.28, cy + 20)), w=8)
NEWMOUTHS = ['scream', 'zigzag', 'teeth', 'gulp']

def new_eye(pen, side, kind):
    cx, cy, rx, ry, prx, pry = eye_geom(side)
    if kind == 'dot': pen.ellipse(cx, cy, 13, 15, fill=INK)
    elif kind == 'euro':
        r = min(rx, ry) * 0.72; pen.line([(cx + r * math.cos(a), cy + r * math.sin(a)) for a in np.linspace(math.radians(52), math.radians(308), 22)], w=9, col=GREEN)
        for dy in (-r * 0.24, r * 0.24): pen.line([(cx - r * 1.25, cy + dy), (cx + r * 0.25, cy + dy)], w=7, col=GREEN)

def build():
    for side in 'LR':
        e = EYEM[side]; cx, cy, rx, ry, prx, pry = eye_geom(side); sd = 211 + ord(side)
        put(f'brow{side}_flat', ink_sprite(G.lab == G.C['brow' + side]))
        for nm, kw in BROWS.items():
            pen = G.Pen(); G.brow(pen, side, **kw); add(f'brow{side}_{nm}', pen, 101 + ord(side))
        # eyes: measured at size 1, the measured silhouette repainted at the other sizes
        put(f'eye{side}_u_100', fill_sprite(cv2.dilate((e['filled'] & ~e['ring']).astype(np.uint8), np.ones((5, 5), np.uint8)) & e['filled']))
        put(f'eye{side}_o_100', ink_sprite(e['ring'], grow=1))
        for s in SIZES[1:]:
            u, o = scaled_eye(side, s, sd); put(f'eye{side}_u_{int(s * 100)}', u); put(f'eye{side}_o_{int(s * 100)}', o)
        # lid lines (upper: flat, a little wider than the eye; lower: a shallow arc): the engine clips the eye at the lid and lays these on the cut
        pen = G.Pen(); pen.line([(e['x'] - 5, cy), (e['x'] + e['w'] + 5, cy)], w=STROKE + 2); add(f'lid{side}', pen, 251 + ord(side))
        pen = G.Pen(); pen.line(G.bez((e['x'] - 2, cy + 5), (cx, cy - 9), (e['x'] + e['w'] + 2, cy + 5)), w=STROKE); add(f'lidlow{side}', pen, 257 + ord(side))
        for kind in KINDS:
            pen = G.Pen(); G.eye(pen, side, kind=kind); add(f'eye{side}_{kind}', pen, 307 + ord(side))
        for kind in NEWKINDS:
            pen = G.Pen(); new_eye(pen, side, kind); add(f'eye{side}_{kind}', pen, 331 + ord(side))
        # pupils: measured at size 1 (re-centred on the eye centre: the engine places it), drawn at the other sizes
        pim = ink_sprite(e['pupil'], grow=1); dx, dy = int(round(cx - e['pc'][0])), int(round(cy - e['pc'][1]))
        put(f'pupil{side}_100', Image.fromarray(np.roll(np.asarray(pim), (dy, dx), (0, 1)), 'RGBA'))
        for ps in PSIZES:
            for shine in ([False, True] if ps >= 1.4 else [False]):
                if ps == 1.0: continue
                pen = G.Pen(); pen.poly(G.jitter_poly(G.superellipse(cx, cy, prx * ps, pry * ps, 2.8, k=24), 6, 0.16, int(cx * 3 + cy)), INK)
                if shine: pen.ellipse(cx - prx * ps * 0.35, cy - pry * ps * 0.4, prx * ps * 0.35, pry * ps * 0.25, fill=(255, 255, 255))
                add(f'pupil{side}_{int(ps * 100)}{"s" if shine else ""}', pen, 401 + ord(side))
        # cheeks: the crease a smile pushes up under the eye, and a puffed cheek beside the mouth
        k = 1 if side == 'L' else -1; yy = e['y'] + e['h'] + 26
        pen = G.Pen(); pen.line(G.bez((cx - 34, yy + 8), (cx, yy - 12), (cx + 34, yy + 8)), w=7); add(f'cheek{side}', pen, 431 + ord(side))
        (x0, y0), (x1, y1) = G.MOUTH; mx = (x0 if side == 'L' else x1); my = (y0 + y1) / 2
        pen = G.Pen(); pen.line(G.bez((mx - k * 22, my - 52), (mx - k * 70, my - 2), (mx - k * 22, my + 48)), w=9); add(f'puff{side}', pen, 441 + ord(side))
    put('mouth_line', ink_sprite(G.lab == G.C['mouth']))
    for nm, kw in MOUTHS.items():
        pen = G.Pen(); G.mouth(pen, **kw); add('mouth_' + nm, pen, 503 + len(nm))
    for nm in NEWMOUTHS:
        pen = G.Pen(); new_mouth(pen, nm); add('mouth_' + nm, pen, 547 + len(nm))
    for ex in EXTRAS:
        pen = G.Pen(); G.extra(pen, ex); add('extra_' + ex, pen, 601 + len(ex))

def pack(maxw=2048):
    names = sorted(sprites, key=lambda n: -sprites[n][0].size[1]); x = y = rowh = 0; rects = {}; places = []
    for n in names:
        im, ox, oy = sprites[n]; w, h = im.size
        if x + w + 2 > maxw: x = 0; y += rowh + 2; rowh = 0
        places.append((n, x, y)); rects[n] = [x, y, w, h, ox, oy]; x += w + 2; rowh = max(rowh, h)
    atlas = Image.new('RGBA', (maxw, y + rowh + 2), (0, 0, 0, 0))
    for n, px, py in places: atlas.paste(sprites[n][0], (px, py))
    return atlas, rects

# measured expressions (paintings in the face set) as rig parameters, and the rig's own extremes (takes, gags)
B = lambda dy=0, rot=0, **k: dict(dy=dy, rot=rot, **k)
both = lambda **k: dict(L=dict(k), R=dict(k))
RIG = {
 'neutral': {}, 'talk': dict(mouth=dict(kind='o', dy=4)), 'talkWide': dict(mouth=dict(kind='open')), 'blink': dict(eyes=both(kind='closed')),
 'skeptical': dict(brows=dict(L=B(-20, 6), R=B(8, 6)), eyes=dict(L=dict(lid=0.3), R=dict(lid=0.45)), mouth=dict(kind='line', tilt=8)),
 'unimpressed': dict(brows=dict(L=B(6), R=B(6)), eyes=both(lid=0.5), mouth=dict(kind='line', curve=-6)),
 'surprised': dict(brows=dict(L=B(-20), R=B(-20)), eyes=dict(L=dict(s=1.2), R=dict(s=1.25)), mouth=dict(kind='o')),
 'shocked': dict(brows=dict(L=B(-26), R=B(-26)), eyes=dict(L=dict(s=1.4, psize=0.6), R=dict(s=1.5, psize=0.6)), mouth=dict(kind='O')),
 'angry': dict(brows=dict(L=B(14, -20), R=B(12, 18)), eyes=both(lid=0.3), mouth=dict(kind='frown', curve=0.55)),
 'sad': dict(brows=dict(L=B(-8, 18), R=B(-8, -18)), eyes=both(pupil=(0, 0.35), lid=0.2), mouth=dict(kind='frown', curve=0.55, w=0.8)),
 'happy': dict(brows=dict(L=B(-10), R=B(-10)), eyes=both(kind='happy'), mouth=dict(kind='smile'), cheeks=1),
 'sleepy': dict(brows=dict(L=B(4), R=B(4)), eyes=both(lid=0.65), mouth=dict(kind='line')),
 'scared': dict(brows=dict(L=B(-18, 14), R=B(-18, -14)), eyes=dict(L=dict(s=1.25, psize=0.6), R=dict(s=1.3, psize=0.6)), mouth=dict(kind='wavy')),
 'grin': dict(brows=dict(L=B(-8), R=B(-8)), eyes=both(low=0.35), mouth=dict(kind='bigsmile'), cheeks=1),
 # rig-only: takes and gag faces
 'take': dict(brows=dict(L=B(-46, 8), R=B(-46, -8)), eyes=dict(L=dict(s=1.9, psize=0.6), R=dict(s=1.9, psize=0.6)), mouth=dict(kind='scream')),
 'takeSmall': dict(brows=dict(L=B(-34), R=B(-34)), eyes=dict(L=dict(s=1.5, psize=0.6), R=dict(s=1.5, psize=0.6)), mouth=dict(kind='O')),
 'deadpan': dict(brows=dict(L=B(4), R=B(4)), eyes=both(lid=0.42), mouth=dict(kind='line', w=0.55)),
 'dotEyes': dict(brows=dict(L=B(-10), R=B(-10)), eyes=both(kind='dot'), mouth=dict(kind='line', w=0.4)),
 'greed': dict(brows=dict(L=B(-18), R=B(-18)), eyes=both(kind='euro'), mouth=dict(kind='teeth'), cheeks=1),
 'zap': dict(brows=dict(L=B(-30, 16), R=B(-30, -16)), eyes=dict(L=dict(s=1.5, psize=0.6), R=dict(s=1.5, psize=0.6)), mouth=dict(kind='zigzag')),
 'gulp': dict(brows=dict(L=B(-16, 16), R=B(-16, -16)), eyes=both(pupil=(0, 0.3), s=1.1), mouth=dict(kind='gulp'), extras=['sweat']),
 'puffed': dict(brows=dict(L=B(8, -8), R=B(8, 8)), eyes=both(s=1.15), mouth=dict(kind='line', w=0.35), puff=1),
 'strain': dict(brows=dict(L=B(12, -20), R=B(12, 20)), eyes=both(kind='squeeze'), mouth=dict(kind='clench'), puff=0.6, extras=['vein']),
 'teeth': dict(brows=dict(L=B(-12), R=B(-12)), eyes=both(low=0.3), mouth=dict(kind='teeth'), cheeks=1),
 'hmm': dict(brows=dict(L=B(-22, 4), R=B(10, 8)), eyes=dict(L=dict(pupil=(0.35, -0.5)), R=dict(pupil=(0.35, -0.5), lid=0.3)), mouth=dict(kind='line', w=0.6, tilt=10, dx=14)),
 'side': dict(brows=dict(L=B(2), R=B(2)), eyes=both(pupil=(0.8, 0.05), lid=0.25), mouth=dict(kind='line', w=0.7)),
 'sideL': dict(brows=dict(L=B(2), R=B(2)), eyes=both(pupil=(-0.8, 0.05), lid=0.25), mouth=dict(kind='line', w=0.7)),
}

if __name__ == '__main__':
    build()
    atlas, rects = pack(); atlas.save(os.path.join(OUT, 'sprites.png'), optimize=True)
    G.BLANK.convert('RGB').save(os.path.join(OUT, 'blank.png'), optimize=True); G.clean(G.BLANK.convert('RGB')).save(os.path.join(OUT, 'blank_clean.png'), optimize=True)
    anchors = {}
    for side in 'LR':
        p0, p1, th = G.BROW[side]; m = (p0 + p1) / 2; cx, cy, rx, ry, prx, pry = eye_geom(side); e = EYEM[side]
        anchors['brow' + side] = [round(float(m[0]), 2), round(float(m[1]), 2)]
        rest = [round(float((e['pc'][0] - cx) / (rx - prx - 4)), 3), round(float((e['pc'][1] - cy) / (ry - pry - 4)), 3)]   # the measured pupil, in the units of a recipe's pupil=(x, y)
        anchors['eye' + side] = {'cx': float(cx), 'cy': float(cy), 'rx': float(rx), 'ry': float(ry), 'prx': prx, 'pry': pry, 'rest': rest, 'x': int(e['x']), 'y': int(e['y']), 'w': int(e['w']), 'h': int(e['h'])}
    (x0, y0), (x1, y1) = G.MOUTH; anchors['mouth'] = {'cx': float((x0 + x1) / 2), 'cy': float((y0 + y1) / 2), 'hw': float((x1 - x0) / 2)}
    tup = lambda o: {k: (list(v) if isinstance(v, tuple) else (tup(v) if isinstance(v, dict) else v)) for k, v in o.items()}
    presets = {k: tup(v) for k, v in {**G.X, **RIG}.items()}
    json.dump({'size': [W, H], 'sprites': rects, 'anchors': anchors, 'sizes': SIZES, 'psizes': PSIZES, 'kinds': KINDS + NEWKINDS, 'mouths': ['line'] + list(MOUTHS) + NEWMOUTHS, 'brows': ['flat'] + list(BROWS), 'extras': EXTRAS, 'presets': presets},
              open(os.path.join(OUT, 'rig.json'), 'w'), indent=0)
    print(len(sprites), 'sprites', atlas.size, len(presets), 'presets')
    if '--sheet' in sys.argv:
        bg = Image.new('RGB', atlas.size, (217, 168, 119)); bg.paste(atlas, (0, 0), atlas); bg.save(sys.argv[sys.argv.index('--sheet') + 1], quality=88)
