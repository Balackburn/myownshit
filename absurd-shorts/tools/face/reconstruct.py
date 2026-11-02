#!/usr/bin/env python3
"""Steps 2–6 — reconstruct a character's painted FACE PANEL 1:1 from accepted reference frames.

  python3 tools/face/reconstruct.py characters/<name>/character.json

character.json → "sources": accepted candidates (see find_faces.py), e.g.
  {"candidate": 5, "expression": "neutral", "identity": true}           # the clean frame identity layers come from
  {"candidate": 0, "expression": "skeptical", "occlude": [[0.6,0,1,0.2]]} # normalised boxes to ignore (occluders)

Pipeline (every value MEASURED from pixels; nothing invented):
  2. rectify   : homography of the 4 measured panel corners → canonical W×H (aspect measured on frontal frames)
  3. classify  : ink = pixels much darker than the local skin; connected components → border / hair / brow / eye /
                 nose / mouth / stubble by measured position; eye whites = bright low-saturation blobs
  4. clean skin: ink + whites inpainted away → the painted skin plate (keeps its real texture and colour)
  5. vectorise : every ink component → a filled polygon (exact rough outline, 0.6 px tolerance) → SVG layers
  6. render    : skin plate + identity layers (from the identity frame) + expression layers (from the frame that shows
                 that expression). Expressions never seen are built by TRANSFORMING the measured strokes (lid clip,
                 brow raise/tilt, mouth bend) and are labelled "designed" in landmarks.json.
  7. validate  : reference vs reconstruction vs overlay + ink IoU / MAE (a score is not proof: look at the overlay).
"""
import sys, os, json, math
import numpy as np, cv2

INK_DELTA = 55          # ink = darker than local skin luminance by this much (0–255)
SS = 4                  # supersampling when rasterising vector layers

def load_frame(video, n):
    import subprocess
    w, h = map(int, subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', video], capture_output=True, text=True).stdout.strip().split(','))
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', video, '-vf', f'select=eq(n\\,{n})', '-vsync', '0', '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w, 3).copy()

def rectify(frame, quad, W, H, pad=0.0):
    src = np.array(quad, np.float32)
    dst = np.array([[0, 0], [W - 1, 0], [W - 1, H - 1], [0, H - 1]], np.float32)
    M = cv2.getPerspectiveTransform(src, dst)
    return cv2.warpPerspective(frame, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE), M

def caption_mask(frame, zone=(0.5, 0.95)):
    """Burned-in captions: near-pure-white glyphs + their dark outline, in horizontal text bands. → occlusion mask."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    txt = ((hsv[:, :, 2] > 228) & (hsv[:, :, 1] < 35)).astype(np.uint8)
    # salmon highlighted words too
    b, g, r = cv2.split(frame.astype(np.int16)); txt |= ((r > 200) & (g < 160) & (b < 140) & (r - g > 70)).astype(np.uint8)
    # keep only GLYPH-sized blobs (letters), not long streaks/props; then rows holding ≥ 4 glyphs form a text band
    n, lab, st, _ = cv2.connectedComponentsWithStats(txt, 8); Hf = frame.shape[0]
    glyph = np.zeros_like(txt); rows = np.zeros(Hf)
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if 0.008 * Hf <= h <= 0.045 * Hf and w <= 0.09 * frame.shape[1] and a >= 12:
            glyph[lab == i] = 1; rows[y:y + h] += 1
    band = rows >= 4
    band[:int(zone[0] * Hf)] = False; band[int(zone[1] * Hf):] = False   # captions live in a known vertical zone (measured)
    m = np.zeros_like(txt); m[band] = glyph[band]
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 15), np.uint8))
    return cv2.dilate(m, np.ones((19, 19), np.uint8))   # include the dark outline / drop shadow

def register(src_img, src_ink, ref_ink, valid):
    """Affine ECC alignment of a source panel onto the identity panel using identity ink (hair/border/stubble)."""
    a = cv2.GaussianBlur((ref_ink * 255).astype(np.float32), (0, 0), 4)
    b = cv2.GaussianBlur((src_ink * valid * 255).astype(np.float32), (0, 0), 4)
    M = np.eye(2, 3, dtype=np.float32)
    try:
        _, M = cv2.findTransformECC(a, b, M, cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), None, 5)
    except cv2.error as e:
        print('  [register] ECC failed, keeping homography only:', str(e).split('\n')[0]); return src_img, None
    H, W = src_img.shape[:2]
    return cv2.warpAffine(src_img, M, (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE), M

def skin_luma(img, ink_guess):
    L = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)[:, :, 0].astype(np.float32)
    k = max(31, (img.shape[1] // 6) | 1)
    masked = np.where(ink_guess, np.nan, L)
    # local skin level = blurred luminance of non-ink pixels
    filled = np.where(np.isnan(masked), np.nanmedian(masked), masked).astype(np.float32)
    return L, cv2.GaussianBlur(filled, (k, k), 0)

def classify(img, occlude, occ_mask=None):
    H, W = img.shape[:2]
    L0 = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)[:, :, 0].astype(np.float32)
    L, skin = skin_luma(img, L0 < np.median(L0) - INK_DELTA)
    ink = ((skin - L) > INK_DELTA).astype(np.uint8)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # eye whites: clearly BRIGHTER and much LESS saturated than the local skin (works in dark scenes too)
    V = hsv[:, :, 2].astype(np.float32); Sat = hsv[:, :, 1].astype(np.float32)
    # global skin reference (skin dominates the panel; a local median gets swallowed by big eyes)
    skinV = float(np.median(V[ink == 0])); skinS = float(np.median(Sat[ink == 0]))
    white = ((V > 0.55 * skinV) & (Sat < 0.6 * skinS) & (ink == 0)).astype(np.uint8)  # low saturation is the discriminating cue
    white = cv2.morphologyEx(white, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    occ = np.zeros((H, W), np.uint8)
    for (x0, y0, x1, y1) in occlude or []: occ[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)] = 1
    if occ_mask is not None: occ |= (occ_mask > 0).astype(np.uint8)
    ink[occ > 0] = 0; white[occ > 0] = 0
    ring = cv2.dilate(occ, np.ones((7, 7), np.uint8)) - occ   # ink hugging an occluder edge = occluder outline, not paint
    n, lab, stats, cent = cv2.connectedComponentsWithStats(ink, 8)
    # group white pieces split by the pupil: label on a closed mask, keep only the real white pixels
    wclosed = cv2.morphologyEx(white, cv2.MORPH_CLOSE, np.ones((13, 13), np.uint8))
    wn, wlab, wstats, wcent = cv2.connectedComponentsWithStats(wclosed, 8)
    wlab = np.where(white > 0, wlab, 0)
    eyes = []
    for i in range(1, wn):
        x, y, w, h, a = wstats[i]
        if a < 0.0012 * W * H or a > 0.04 * W * H or y < 0.1 * H or y > 0.65 * H: continue
        eyes.append(dict(id=int(i), bbox=[int(x), int(y), int(w), int(h)], c=[float(wcent[i][0]), float(wcent[i][1])], area=int(a)))
    eyes = sorted(sorted(eyes, key=lambda e: -e['area'])[:2], key=lambda e: e['c'][0])
    eye_zone = {e['id']: cv2.dilate((wlab == e['id']).astype(np.uint8), np.ones((15, 15), np.uint8)) > 0 for e in eyes}
    comps = []
    for i in range(1, n):
        x, y, w, h, a = stats[i]; cx, cy = cent[i]
        if a < 6: continue
        if ring[lab == i].mean() > 0.5: continue
        u, v = cx / W, cy / H
        touches = x <= 2 or y <= 2 or x + w >= W - 3 or y + h >= H - 3
        near_eye = next((e for e in eyes if eye_zone[e['id']][lab == i].any()), None)
        above_eye = next((e for e in eyes if abs(cx - e['c'][0]) < e['bbox'][2] * 1.5 and 0 < e['bbox'][1] - cy < max(e['bbox'][3] * 3.5, 0.09 * H)), None)
        if touches and (w > 0.6 * W or h > 0.6 * H): kind = 'border'
        elif above_eye and not touches and w > 1.6 * h and a > 0.0012 * W * H: kind = 'brow'   # brows can sit up near the hairline
        elif v < 0.16 or (touches and v < 0.35): kind = 'hair'
        elif near_eye: kind = 'eye'
        elif above_eye and w > h: kind = 'brow'
        elif 0.66 < v < 0.86 and w > 0.18 * W and w > 2.5 * h: kind = 'mouth'
        elif 0.5 < v < 0.72 and a < 0.004 * W * H and 0.3 < u < 0.7 and not (v > 0.62 and h > 1.8 * w): kind = 'nose'
        elif v > 0.55: kind = 'stubble'
        else: kind = 'mark'
        comps.append(dict(id=int(i), kind=kind, bbox=[int(x), int(y), int(w), int(h)], c=[float(cx), float(cy)], area=int(a)))
    # nose = the single best candidate (closest to centre line), the rest of 'nose' become stubble
    noses = sorted([c for c in comps if c['kind'] == 'nose'], key=lambda c: abs(c['c'][0] / W - 0.5) + abs(c['c'][1] / H - 0.62))
    for c in noses[2:]: c['kind'] = 'stubble'   # the nose is drawn as 1–2 tiny marks
    return dict(ink=ink, lab=lab, white=white, wlab=wlab, eyes=eyes, comps=comps, occ=occ)

def stroke_width(mask):
    if mask.sum() == 0: return None
    d = cv2.distanceTransform(mask.astype(np.uint8), cv2.DIST_L2, 3)
    sk = d[(d > 0) & (d >= cv2.dilate(d, np.ones((3, 3))) - 1e-6)]
    return float(2 * np.median(sk)) if len(sk) else None

def polys(mask, eps=0.6):
    cnts, hier = cv2.findContours(mask.astype(np.uint8), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    out = []
    for i, c in enumerate(cnts):
        if len(c) < 3: continue
        c = cv2.approxPolyDP(c, eps, True).reshape(-1, 2)
        parent = int(hier[0][i][3]) if hier is not None else -1
        out.append(dict(pts=c.tolist(), hole=parent >= 0, grp=parent if parent >= 0 else i))
    return out

def svg_path(pl):
    return ' '.join('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in p['pts']) + ' Z' for p in pl)

def raster(layers, W, H):
    """Rasterise polygon layers (with holes) at SS× and downsample → anti-aliased alpha."""
    big = np.zeros((H * SS, W * SS), np.uint8)
    for li, pl in enumerate(layers):
        groups = {}
        for p in pl: groups.setdefault((li, p.get('grp', id(p))), []).append(p)
        for parts in groups.values():   # each component: its outline minus ITS OWN holes (a pupil inside a ring survives)
            outer = [np.array(p['pts'], np.float64) * SS for p in parts if not p['hole']]
            if not outer: continue
            allp = np.vstack(outer); x0, y0 = np.floor(allp.min(0)).astype(int) - 2; x1, y1 = np.ceil(allp.max(0)).astype(int) + 2
            x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(W * SS, x1), min(H * SS, y1)
            if x1 <= x0 or y1 <= y0: continue
            tmp = np.zeros((y1 - y0, x1 - x0), np.uint8); off = np.array([x0, y0])
            cv2.fillPoly(tmp, [(o - off).astype(np.int32) for o in outer], 255)
            holes = [(np.array(p['pts'], np.float64) * SS - off).astype(np.int32) for p in parts if p['hole']]
            if holes: cv2.fillPoly(tmp, holes, 0)
            np.maximum(big[y0:y1, x0:x1], tmp, out=big[y0:y1, x0:x1])
    return cv2.resize(big, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255

def layer_mask(cls, kinds):
    m = np.zeros(cls['ink'].shape, np.uint8)
    for c in cls['comps']:
        if c['kind'] in kinds: m[cls['lab'] == c['id']] = 1
    return m

def eye_mask(cls):
    m = np.zeros(cls['ink'].shape, np.uint8)
    for e in cls['eyes']: m[cls['wlab'] == e['id']] = 1
    return m

# ---- expression transforms applied to MEASURED strokes ("designed" variants) -------------------
def affine_layer(pl, M):
    return [dict(pts=(np.c_[np.array(p['pts'], float), np.ones(len(p['pts']))] @ M.T).tolist(), hole=p['hole'], grp=p.get('grp')) for p in pl]

def design_expression(name, L, meta, W, H):
    """L = measured vector layers of the neutral frame. Returns modified layers; mark as designed."""
    import copy
    out = copy.deepcopy(L)
    eyes = meta['eyes']; sw = meta['stroke_px'] or 6
    def brow_move(dy=0, tilt=0, side=None):
        res = []
        for p in out['brow']:
            xs = [q[0] for q in p['pts']]; cx = np.mean(xs); left = cx < W / 2
            if side and (side == 'L') != left: res.append(p); continue
            t = (tilt if left else -tilt) * math.pi / 180
            M = cv2.getRotationMatrix2D((float(cx), float(np.mean([q[1] for q in p['pts']]))), math.degrees(t), 1.0); M[1, 2] += dy * H
            res += affine_layer([p], M)
        out['brow'] = res
    def lids(levels):  # cover the top of each eye white with skin, draw a lid stroke (measured stroke width)
        out.setdefault('_lids', [])
        for e, lv in zip(eyes, levels):
            if lv <= 0: continue
            x, y, w, h = e['bbox']; out['_lids'].append(dict(eye=[x, y, w, h], y=y + h * lv, sw=sw))
    def mouth(curve=0.0, open_=0.0):
        res = []
        for p in out['mouth']:
            pts = np.array(p['pts'], float); x0, x1 = pts[:, 0].min(), pts[:, 0].max(); mid = (x0 + x1) / 2; half = max(1, (x1 - x0) / 2)
            pts[:, 1] += curve * H * (1 - ((pts[:, 0] - mid) / half) ** 2)   # bend the real stroke (smile < 0 < frown)
            res.append(dict(pts=pts.tolist(), hole=p['hole'], grp=p.get('grp')))
        out['mouth'] = res
        if open_: out['_mouthOpen'] = open_; out['_sw'] = sw
    if name == 'skeptical': brow_move(-0.025, -6, 'L'); lids([0, 0.45])
    elif name == 'unimpressed': lids([0.5, 0.5]); brow_move(0.008)
    elif name == 'surprised': brow_move(-0.03); mouth(0, 0.03)
    elif name == 'shocked': brow_move(-0.04); mouth(0, 0.06)
    elif name == 'angry': brow_move(0.012, 12); lids([0.3, 0.3]); mouth(0.008)
    elif name == 'sad': brow_move(0.0, -10); mouth(0.012)
    elif name == 'happy': mouth(-0.014); brow_move(-0.01)
    elif name == 'sleepy': lids([0.8, 0.8])
    elif name == 'blink': lids([1.0, 1.0])
    elif name == 'scared': brow_move(-0.035, -10); mouth(0, 0.045)
    return out

def compose(plate, L, W, H, ink_rgb, white_rgb, extra=None):
    img = plate.astype(np.float32).copy(); ink = np.array(ink_rgb, np.float32)
    wa = raster([L['eyewhite']], W, H)[..., None]; img = img * (1 - wa) + np.array(white_rgb, np.float32) * wa
    if extra and extra.get('_mouthOpen') and L.get('mouth'):
        # open mouth: dark cavity hanging under the MEASURED mouth stroke (same length, same tilt), inked outline
        ms = np.array([q for p in L['mouth'] for q in p['pts']], float)
        x0, x1 = ms[:, 0].min(), ms[:, 0].max(); top = ms[:, 1].min(); depth = extra['_mouthOpen'] * H
        xs = np.linspace(x0 + 0.15 * (x1 - x0), x1 - 0.15 * (x1 - x0), 24)
        bot = top + depth * np.sqrt(np.clip(1 - ((xs - (x0 + x1) / 2) / ((x1 - x0) * 0.36)) ** 2, 0, 1))
        poly = np.r_[np.c_[xs, np.full_like(xs, top + 2)], np.c_[xs[::-1], bot[::-1] + 2]].astype(np.int32)
        cv2.fillPoly(img, [poly], (32, 22, 58), cv2.LINE_AA)
        cv2.polylines(img, [poly], True, tuple(float(c) for c in ink), max(2, int(round(extra.get('_sw', 6) * 0.8))), cv2.LINE_AA)
    kinds = ['border', 'hair', 'brow', 'eye', 'nose', 'mouth', 'stubble', 'mark']
    ia = raster([L[k] for k in kinds if L.get(k)], W, H)[..., None]
    img = img * (1 - ia) + ink * ia
    for ld in (extra or {}).get('_lids', []):
        # eyelid: everything of the eye above the lid line goes back to skin (outline included), then the lid stroke
        x, y, w, h = ld['eye']; pad = int(ld['sw'] * 1.4) + 2; closed = ld['y'] >= y + 0.95 * h
        ly = int(round(y + 0.58 * h)) if closed else int(round(ld['y']))
        zone = np.zeros((H, W), np.uint8); cv2.ellipse(zone, (x + w // 2, y + h // 2), (w // 2 + pad, h // 2 + pad), 0, 0, 360, 1, -1)
        if not closed: zone[ly:] = 0
        img[zone > 0] = plate[zone > 0]
        ys, xs = np.where(cv2.ellipse(np.zeros((H, W), np.uint8), (x + w // 2, y + h // 2), (w // 2 + 1, h // 2 + 1), 0, 0, 360, 1, -1)[ly:ly + 1] > 0)
        lx0, lx1 = (xs.min(), xs.max()) if len(xs) and not closed else (x, x + w)
        cv2.line(img, (int(lx0) - pad // 2, ly), (int(lx1) + pad // 2, ly), tuple(float(c) for c in ink), max(2, int(round(ld['sw']))), cv2.LINE_AA)
    return np.clip(img, 0, 255).astype(np.uint8)

def main():
    cfgp = sys.argv[1]; cfg = json.load(open(cfgp)); root = os.path.dirname(os.path.abspath(cfgp)); fdir = os.path.join(root, 'face')
    cands = json.load(open(os.path.join(fdir, 'candidates.json')))
    W, H = cfg['canonical']['width'], cfg['canonical']['height']
    os.makedirs(os.path.join(fdir, 'expressions'), exist_ok=True); os.makedirs(os.path.join(fdir, 'rectified'), exist_ok=True)
    measured, landmarks = {}, dict(character=cfg['name'], canonical=[W, H], units='px in canonical face space (0,0 = top-left of the panel)', sources=[], expressions={})
    identity = None; identity_cls = None
    # identity source first so the others can be registered onto it
    for src in sorted(cfg['sources'], key=lambda s: not s.get('identity')):
        c = cands[src['candidate']]; frame = load_frame(c['video'], c['frame'])
        rect, Mh = rectify(frame, c['quad'], W, H)
        capm = cv2.warpPerspective(caption_mask(frame, tuple(cfg.get('caption_zone', [0.5, 0.95]))), Mh, (W, H), flags=cv2.INTER_NEAREST)   # captions → occlusion
        cls = classify(rect, src.get('occlude'), capm)
        if identity_cls is not None and not src.get('identity'):   # align extra sources onto the identity panel
            idink = layer_mask(identity_cls, ['border', 'hair', 'stubble', 'nose'])
            srcink = layer_mask(cls, ['border', 'hair', 'stubble', 'nose'])
            rect2, Ma = register(rect, srcink, idink, (cls['occ'] == 0).astype(np.uint8))
            if Ma is not None:
                capm = cv2.warpAffine(capm | (cls['occ'] > 0).astype(np.uint8), Ma, (W, H), flags=cv2.INTER_NEAREST | cv2.WARP_INVERSE_MAP)
                rect = rect2; cls = classify(rect, None, capm)
        cv2.imwrite(os.path.join(fdir, 'rectified', f"{src['expression']}.png"), rect)
        ink_ok = cls['ink'].copy()
        # clean skin plate: remove ink + whites + occluders with a generous halo (anti-aliased edges would leave ghosts),
        # then re-add a little of the measured paper grain so inpainted areas don't look smoothed
        kill = cv2.dilate(((ink_ok + eye_mask(cls) + cls['occ']) > 0).astype(np.uint8), np.ones((11, 11), np.uint8))
        plate = cv2.inpaint(rect, kill, 9, cv2.INPAINT_TELEA)
        grain = (rect.astype(np.float32) - cv2.GaussianBlur(rect, (0, 0), 3).astype(np.float32)); grain[kill > 0] = 0
        gstd = float(grain[kill == 0].std()) if (kill == 0).any() else 0
        noise = np.random.default_rng(7).normal(0, gstd, rect.shape[:2])[..., None]
        plate = np.clip(plate.astype(np.float32) + np.where(kill[..., None] > 0, noise, 0), 0, 255).astype(np.uint8)
        L = {k: polys(layer_mask(cls, [k])) for k in ['border', 'hair', 'brow', 'eye', 'nose', 'mouth', 'stubble', 'mark']}
        L['eyewhite'] = polys(eye_mask(cls))
        dbg = rect.copy() // 3
        colors = dict(border=(255, 255, 255), hair=(60, 60, 255), brow=(0, 220, 255), eye=(0, 255, 0), nose=(255, 0, 255), mouth=(255, 128, 0), stubble=(160, 160, 160), mark=(0, 0, 255))
        for cc in cls['comps']: dbg[cls['lab'] == cc['id']] = colors[cc['kind']]
        dbg[eye_mask(cls) > 0] = (255, 255, 160); dbg[cls['occ'] > 0] = dbg[cls['occ'] > 0] // 2 + np.array([0, 0, 90], np.uint8)
        cv2.imwrite(os.path.join(fdir, 'rectified', f"{src['expression']}_classes.png"), dbg)
        inkpx = rect[cls['ink'] > 0]
        if len(inkpx): lum = inkpx.astype(float).sum(1); inkpx = inkpx[lum <= np.median(lum)]
        ink_rgb = inkpx.mean(0).tolist() if len(inkpx) else [20, 20, 20]
        wpx = rect[eye_mask(cls) > 0]; white_rgb = wpx.mean(0).tolist() if len(wpx) else [235, 235, 235]
        sw = stroke_width(layer_mask(cls, ['brow', 'eye', 'mouth']))
        feats = {}
        for k in ['brow', 'eye', 'nose', 'mouth']:
            cs = [x for x in cls['comps'] if x['kind'] == k]
            feats[k] = [dict(bbox=x['bbox'], centroid=[round(x['c'][0], 1), round(x['c'][1], 1)], area=x['area']) for x in cs] or 'unverified'
        feats['eye_white'] = [dict(bbox=e['bbox'], centroid=[round(e['c'][0], 1), round(e['c'][1], 1)], area=e['area']) for e in cls['eyes']] or 'unverified'
        feats['stubble_marks'] = sum(1 for x in cls['comps'] if x['kind'] == 'stubble')
        feats['hair_ink_px'] = int(layer_mask(cls, ['hair']).sum())
        conf = 'high' if (len(cls['eyes']) == 2 and isinstance(feats['mouth'], list) and c['frontality'] > 0.9) else 'medium' if len(cls['eyes']) >= 1 else 'low'
        meta = dict(eyes=cls['eyes'], stroke_px=sw)
        measured[src['expression']] = dict(L=L, plate=plate, rect=rect, cls=cls, ink=ink_rgb, white=white_rgb, meta=meta)
        landmarks['sources'].append(dict(expression=src['expression'], video=os.path.basename(c['video']), frame=c['frame'], quad=c['quad'], frontality=round(c['frontality'], 3), occluded=src.get('occlude', []), confidence=conf, stroke_px=round(sw, 2) if sw else 'unverified', ink_rgb=[round(v) for v in ink_rgb[::-1]], features=feats))
        if src.get('identity'): identity = src['expression']; identity_cls = cls
        landmarks['sources'][-1]['occluded_px_ratio'] = round(float(cls['occ'].mean()), 3)
    identity = identity or cfg['sources'][0]['expression']
    I = measured[identity]
    # colour reference: the identity frame may come from a dark scene; match its skin to a well-lit source (per-channel gain)
    ref = cfg.get('color_reference')
    if ref and ref in measured and ref != identity:
        def skin_med(m):
            ok = (m['cls']['ink'] == 0) & (m['cls']['occ'] == 0) & (eye_mask(m['cls']) == 0)
            return np.median(m['plate'][ok].reshape(-1, 3).astype(np.float32), 0)
        gain = skin_med(measured[ref]) / np.maximum(skin_med(I), 1)
        I['plate'] = np.clip(I['plate'].astype(np.float32) * gain, 0, 255).astype(np.uint8)
        I['white'] = list(np.clip(np.array(I['white']) * gain, 0, 255))
        landmarks['color_gain_bgr'] = [round(float(g), 3) for g in gain]
    # Occluded rows of the identity panel (captions…): stubble there is NOT measurable. Fill it by cloning the measured
    # stubble from the rows just below (or above), and record it as "inferred".
    occ = I['cls']['occ']; rows = np.where(occ.mean(1) > 0.3)[0]; inferred = []
    if len(rows):
        y0, y1 = int(rows.min()), int(rows.max()) + 1; hgt = y1 - y0
        sy = y1 if y1 + hgt <= H else max(0, y0 - hgt)
        clone = [dict(pts=[[x, yy - sy + y0] for x, yy in p['pts']], hole=p['hole'], grp=('clone', p.get('grp'))) for p in I['L']['stubble']
                 if all(sy <= yy < sy + hgt for _, yy in p['pts'])]
        I['L']['stubble'] = I['L']['stubble'] + clone
        I['plate'] = I['plate'].copy(); I['plate'][y0:y1] = I['plate'][sy:sy + hgt]  # skin texture cloned from the same rows
        inferred.append(dict(rows=[y0, y1], what='stubble cloned from rows %d-%d' % (sy, sy + hgt), marks=len(clone)))
    landmarks['inferred'] = inferred or 'none'
    # identity layers (border, hair, nose, stubble) always come from the identity frame; expression layers from each source
    def build(expr_layers, extra=None):
        L = dict(I['L']); L.update({k: expr_layers[k] for k in ['brow', 'eye', 'eyewhite', 'mouth']})
        return compose(I['plate'], L, W, H, I['ink'], I['white'], extra)
    import copy
    allx = cfg.get('expressions', ['neutral', 'skeptical', 'unimpressed', 'surprised', 'shocked', 'angry', 'sad', 'happy', 'sleepy', 'blink', 'scared'])
    for name in allx:
        if name in measured:
            img = build(measured[name]['L']); status = 'measured'; src = name
        else:
            base = measured.get('neutral', I)
            d = design_expression(name, base['L'], base['meta'], W, H); img = build(d, d); status = 'designed (transformed measured strokes, not seen in the footage)'; src = 'neutral' if 'neutral' in measured else identity
        cv2.imwrite(os.path.join(fdir, 'expressions', f'face_{name}.png'), img)
        landmarks['expressions'][name] = dict(status=status, from_source=src)
    # SVG (editable vector layers of the identity frame + each measured expression)
    for name, m in measured.items():
        groups = []
        for k in ['eyewhite', 'border', 'hair', 'brow', 'eye', 'nose', 'mouth', 'stubble', 'mark']:
            fill = '#%02x%02x%02x' % tuple(int(v) for v in (m['white'] if k == 'eyewhite' else m['ink'])[::-1])
            groups.append(f'  <g id="{k}" fill="{fill}" fill-rule="evenodd"><path d="{svg_path(m["L"][k])}"/></g>')
        cv2.imwrite(os.path.join(fdir, f'skin_plate_{name}.png'), m['plate'])
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n  <image href="skin_plate_{name}.png" width="{W}" height="{H}"/>\n' + '\n'.join(groups) + '\n</svg>\n'
        open(os.path.join(fdir, f'face_{name}.svg'), 'w').write(svg)
    json.dump(landmarks, open(os.path.join(fdir, 'face_landmarks.json'), 'w'), indent=1)
    # validation: reference | reconstruction | overlay (red = ink only in reference, cyan = only in reconstruction)
    rows, metrics = [], {}
    for name, m in measured.items():
        rec = cv2.imread(os.path.join(fdir, 'expressions', f'face_{name}.png'))
        ref_ink = m['cls']['ink'] > 0; rec_cls = classify(rec, None); rec_ink = rec_cls['ink'] > 0
        valid = m['cls']['occ'] == 0
        iou = float((ref_ink & rec_ink & valid).sum() / max(1, ((ref_ink | rec_ink) & valid).sum()))
        mae = float(np.abs(rec.astype(float) - m['rect'].astype(float))[valid].mean())
        metrics[name] = dict(ink_iou=round(iou, 3), mae=round(mae, 2))
        ov = np.full_like(rec, 255); ov[ref_ink & ~rec_ink] = (40, 40, 230); ov[rec_ink & ~ref_ink] = (230, 200, 40); ov[ref_ink & rec_ink] = (30, 30, 30)
        rows.append(np.hstack([m['rect'], rec, ov]))
    cv2.imwrite(os.path.join(fdir, 'face_comparison.png'), np.vstack(rows) if len(rows) > 1 else rows[0])
    landmarks['validation'] = metrics; json.dump(landmarks, open(os.path.join(fdir, 'face_landmarks.json'), 'w'), indent=1)
    print('identity frame:', identity); print('validation:', metrics); print('expressions:', {k: v['status'][:8] for k, v in landmarks['expressions'].items()})

if __name__ == '__main__': main()
