// Painted texture atlas for the protagonist (assets/lemec_atlas.webp, 1774×887 px).
// Every box face of the "lemec" rig samples a rectangle of this atlas (per-face UVs).
// The face panel is the NEUTRAL expression as painted; other expressions are produced by
// patching skin over the eyes/brows/mouth and redrawing them in the same ink style.
import * as THREE from 'three';

export const ATLAS_URL = '/assets/lemec_atlas.webp';
export const AW = 1774, AH = 887;

// Atlas regions in pixels [x0, y0, x1, y1] (measured on the atlas with a 50 px grid).
export const R = {
  face:       [64, 8, 350, 759],     // front of the head, cropped (not squashed) to the measured W/H ≈ 0.38; border redrawn
  headSide:   [436, 2, 668, 762],    // left edge = front of the head; hair + drips + painted ear
  headTop:    [452, 24, 676, 270],   // solid black hair
  headBottom: [10, 770, 128, 884],   // skin
  skinCap:    [672, 2, 820, 142],    // clean skin square (neck front / hands)
  neckA:      [140, 770, 290, 884], neckB: [300, 770, 430, 884], neckC: [440, 770, 600, 884],
  jacketFront:[826, 92, 1298, 628],  // lapels, shirt, tie, pocket stroke
  jacketSide: [692, 148, 818, 626],  // navy panels
  jacketBack: [1308, 158, 1436, 698],// plain navy (left of the teal crease)
  navyBlock:  [615, 636, 930, 808],  // sleeve panels
  navyBlock2: [940, 648, 1190, 762],
  legFrontL:  [1310, 158, 1524, 698], legFrontR: [1534, 158, 1770, 698],  // trousers with the teal crease
  legSide:    [1308, 158, 1420, 698],
  cuff:       [636, 818, 756, 884], cuffSide: [1198, 652, 1238, 758], cuffEnd: [1248, 642, 1298, 708],
  collar:     [1004, 12, 1106, 86],
  shoeTop:    [1256, 720, 1496, 790], shoeFront: [1556, 720, 1770, 790], shoeSide: [1256, 800, 1496, 884], shoeSole: [1556, 800, 1770, 884],
};

// Face features (atlas px) — used to erase/redraw for expressions.
const F = {
  eyeL: { x: 150, y: 262, rx: 40, ry: 35 }, browL: { x: 145, y: 188 },
  eyeR: { x: 298, y: 420, rx: 40, ry: 26 }, browR: { x: 292, y: 360 },
  mouth: { x0: 133, x1: 301, y: 624 }, nose: { x: 211, y: 528 },
  cleanSkin: [216, 138, 380, 330],
};

// ---- load once (top-level await: modules importing this wait for the image) ----------
export const atlasImage = await new Promise((res) => {
  const im = new Image(); im.onload = () => res(im); im.onerror = () => { console.warn('atlas missing', ATLAS_URL); res(null); };
  im.src = ATLAS_URL;
});

// Measured face set (tools/face/reconstruct.py): characters/<name>/face/expressions/face_<expr>.png.
// When present it REPLACES the painted-over atlas face: these textures are reconstructed 1:1 from the footage.
// Engine expression names → face-set names (measured or "designed" variants, see face_landmarks.json).
const FACE_SET_DIR = '/characters/lemec/face';
const EXPR_MAP = { neutral: 'neutral', talk: 'talk', blink: 'blink', sleepy: 'sleepy', suspicious: 'skeptical', smug: 'skeptical',
  unimpressed: 'unimpressed', sideLook: 'unimpressed', surprised: 'surprised', shocked: 'shocked', scared: 'scared', angry: 'angry',
  disgusted: 'angry', grimace: 'angry', sad: 'sad', worried: 'sad', happy: 'happy', dead: 'blink', grin: 'grin' };
export const faceSet = await (async () => {
  try {
    const lm = await (await fetch(FACE_SET_DIR + '/face_landmarks.json')).json();
    const names = Object.keys(lm.expressions || {}); const imgs = {};
    await Promise.all(names.map(n => new Promise(res => { const im = new Image(); im.onload = () => { imgs[n] = im; res(); }; im.onerror = res; im.src = `${FACE_SET_DIR}/expressions/face_${n}.png`; })));
    return Object.keys(imgs).length ? { imgs, meta: lm } : null;
  } catch { return null; }
})();
const faceSetCache = {};
function faceSetTexture(expression) {
  const n = EXPR_MAP[expression] || expression; const im = faceSet.imgs[n] || faceSet.imgs.neutral;
  if (!im) return null;
  if (faceSetCache[n]) return faceSetCache[n];
  const c = document.createElement('canvas'); c.width = im.width; c.height = im.height; const g = c.getContext('2d');
  // the face set already has the ORIGINAL colours: pre-invert the global grade (director.js GRADE) so it comes out 1:1
  g.filter = 'brightness(0.935) contrast(1.163) saturate(1.282)'; g.drawImage(im, 0, 0); g.filter = 'none';
  g.strokeStyle = '#151313'; g.lineWidth = Math.round(im.width * 0.03); g.strokeRect(g.lineWidth / 2, g.lineWidth / 2, c.width - g.lineWidth, c.height - g.lineWidth);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  return (faceSetCache[n] = t);
}

let _tex = null, _mat = null;
export function atlasTexture() {
  if (_tex || !atlasImage) return _tex;
  _tex = new THREE.Texture(atlasImage); _tex.colorSpace = THREE.SRGBColorSpace; _tex.anisotropy = 8; _tex.needsUpdate = true;
  return _tex;
}
export function atlasMaterial() {
  if (!_mat) _mat = new THREE.MeshLambertMaterial({ map: atlasTexture(), flatShading: true, color: new THREE.Color(1.18, 1.18, 1.18) }); // painted navy is dark: lift it a bit under Lambert
  return _mat;
}

// Remap the UVs of a BoxGeometry so each face samples an atlas rectangle.
// faces: { px, nx, py, ny, pz, nz } -> [x0,y0,x1,y1]; give x1 < x0 to mirror horizontally.
const ORDER = ['px', 'nx', 'py', 'ny', 'pz', 'nz'];
export function atlasUV(geo, faces) {
  const uv = geo.attributes.uv;
  ORDER.forEach((k, f) => {
    const r = faces[k]; if (!r) return;
    for (let i = f * 4; i < f * 4 + 4; i++) {
      const u = uv.getX(i), v = uv.getY(i);
      uv.setXY(i, (r[0] + u * (r[2] - r[0])) / AW, 1 - (r[1] + (1 - v) * (r[3] - r[1])) / AH);
    }
  });
  uv.needsUpdate = true; return geo;
}

// Box mesh textured from the atlas (same signature spirit as style.box()).
export function atlasBox(w, h, d, faces, opts = {}) {
  const geo = new THREE.BoxGeometry(w, h, d);
  if (opts.taper) { // reuse style.taperGeometry semantics without importing (avoid cycles)
    const p = geo.attributes.position; geo.computeBoundingBox(); const min = geo.boundingBox.min.y, max = geo.boundingBox.max.y;
    const tx = typeof opts.taper === 'number' ? opts.taper : opts.taper.x, tz = typeof opts.taper === 'number' ? opts.taper : opts.taper.z;
    for (let i = 0; i < p.count; i++) { const t = (p.getY(i) - min) / (max - min || 1); p.setX(i, p.getX(i) * (1 + (tx - 1) * t)); p.setZ(i, p.getZ(i) * (1 + (tz - 1) * t)); }
    p.needsUpdate = true;
  }
  if (opts.pivot === 'top') geo.translate(0, -h / 2, 0);
  if (opts.pivot === 'bottom') geo.translate(0, h / 2, 0);
  atlasUV(geo, faces); geo.computeVertexNormals();
  const m = new THREE.Mesh(geo, atlasMaterial()); m.castShadow = m.receiveShadow = true; return m;
}

// Helper: same region on all six faces (optionally a different front).
export const allFaces = (r, extra = {}) => ({ px: r, nx: r, py: r, ny: r, pz: r, nz: r, ...extra });
export const flipX = r => [r[2], r[1], r[0], r[3]];

// ---- face panel with expressions --------------------------------------------------------
const faceCache = new Map();
// Draw `img` into ctx at (x,y,w,h) with edges faded over `f` px, so skin patches have no visible seams.
function feathered(ctx, img, x, y, w, h, f = 18) {
  const t = document.createElement('canvas'); t.width = Math.max(1, Math.round(w)); t.height = Math.max(1, Math.round(h));
  const g = t.getContext('2d'); g.drawImage(img, 0, 0, t.width, t.height);
  g.globalCompositeOperation = 'destination-in';
  const gx = g.createLinearGradient(0, 0, t.width, 0); const fx = Math.min(0.45, f / t.width);
  gx.addColorStop(0, 'rgba(0,0,0,0)'); gx.addColorStop(fx, 'rgba(0,0,0,1)'); gx.addColorStop(1 - fx, 'rgba(0,0,0,1)'); gx.addColorStop(1, 'rgba(0,0,0,0)');
  g.fillStyle = gx; g.fillRect(0, 0, t.width, t.height);
  const gy = g.createLinearGradient(0, 0, 0, t.height); const fy = Math.min(0.45, f / t.height);
  gy.addColorStop(0, 'rgba(0,0,0,0)'); gy.addColorStop(fy, 'rgba(0,0,0,1)'); gy.addColorStop(1 - fy, 'rgba(0,0,0,1)'); gy.addColorStop(1, 'rgba(0,0,0,0)');
  g.fillStyle = gy; g.fillRect(0, 0, t.width, t.height);
  ctx.drawImage(t, x, y);
}

function crop(r) { const c = document.createElement('canvas'); c.width = r[2] - r[0]; c.height = r[3] - r[1]; c.getContext('2d').drawImage(atlasImage, r[0], r[1], c.width, c.height, 0, 0, c.width, c.height); return c; }

export function atlasFaceTexture(expression = 'neutral') {
  if (faceSet) { const t = faceSetTexture(expression); if (t) return t; }
  if (!atlasImage) return null;
  if (faceCache.has(expression)) return faceCache.get(expression);
  const r = R.face, c = crop(r), g = c.getContext('2d');
  const X = x => x - r[0], Y = y => y - r[1];
  const skin = crop(F.cleanSkin);
  const patch = (x0, y0, x1, y1) => { feathered(g, skin, X(x0) - 10, Y(y0) - 10, x1 - x0 + 20, y1 - y0 + 20, 14); };
  const ink = '#151313', white = '#EFEDE5';
  g.lineCap = 'round'; g.lineJoin = 'round';

  const e = expression;
  const touchEyes = e !== 'neutral' && e !== 'talk' && e !== 'grimace';
  const touchMouth = !['neutral', 'blink', 'sleepy', 'suspicious', 'unimpressed', 'sideLook', 'worried'].includes(e) || e === 'talk';
  if (touchEyes) { patch(98, 160, 205, 305); patch(244, 335, 352, 455); }
  if (touchMouth) patch(118, 606, 318, 646);

  const brow = (b, dy = 0, tilt = 0) => { g.strokeStyle = ink; g.lineWidth = 6; g.beginPath(); g.moveTo(X(b.x - 34), Y(b.y + 8 + dy + tilt)); g.quadraticCurveTo(X(b.x), Y(b.y - 10 + dy), X(b.x + 34), Y(b.y + 8 + dy - tilt)); g.stroke(); };
  const eye = (p, { s = 1, lid = 0, pupil = [0, 0], closed = false, happy = false, x = false } = {}) => {
    const rx = p.rx * s, ry = p.ry * s, cx = X(p.x), cy = Y(p.y);
    g.strokeStyle = ink;
    if (x) { g.lineWidth = 7; g.beginPath(); g.moveTo(cx - rx * 0.7, cy - ry * 0.7); g.lineTo(cx + rx * 0.7, cy + ry * 0.7); g.moveTo(cx + rx * 0.7, cy - ry * 0.7); g.lineTo(cx - rx * 0.7, cy + ry * 0.7); g.stroke(); return; }
    if (closed) { g.lineWidth = 7; g.beginPath(); if (happy) g.arc(cx, cy + ry * 0.6, rx * 0.8, Math.PI * 1.15, Math.PI * 1.85); else { g.moveTo(cx - rx, cy); g.quadraticCurveTo(cx, cy + 6, cx + rx, cy); } g.stroke(); return; }
    g.fillStyle = white; g.lineWidth = 7; g.beginPath(); g.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2); g.fill(); g.stroke();
    g.fillStyle = ink; g.beginPath(); g.ellipse(cx + pupil[0] * rx, cy + pupil[1] * ry, 7, 8, 0, 0, Math.PI * 2); g.fill();
    if (lid > 0) {
      const ly = cy - ry + 2 * ry * lid;
      g.save(); g.beginPath(); g.ellipse(cx, cy, rx + 2, ry + 2, 0, 0, Math.PI * 2); g.clip(); g.drawImage(skin, cx - rx - 4, cy - ry - 4, 2 * rx + 8, ly - (cy - ry) + 4); g.restore();
      g.lineWidth = 7; g.beginPath(); const hw = rx * Math.sqrt(Math.max(0, 1 - ((ly - cy) / ry) ** 2)); g.moveTo(cx - hw - 3, ly); g.lineTo(cx + hw + 3, ly); g.stroke();
    }
  };
  const L = F.eyeL, Rr = F.eyeR;
  if (touchEyes) {
    const B = { surprised: [-14, 0], shocked: [-20, 0], scared: [-18, 8], worried: [-12, 10], sad: [-2, 8], angry: [8, -12], suspicious: [-12, 0], smug: [-8, 0], unimpressed: [6, 0], disgusted: [4, -8], sideLook: [-4, 0], happy: [-8, 0] }[e] || [0, 0];
    brow(F.browL, B[0], B[1]); brow(F.browR, e === 'suspicious' ? 8 : B[0], e === 'suspicious' ? 10 : -B[1]);
    switch (e) {
      case 'blink': case 'sleepy': eye(L, { closed: true }); eye(Rr, { closed: true }); break;
      case 'happy': eye(L, { closed: true, happy: true }); eye(Rr, { closed: true, happy: true }); break;
      case 'dead': eye(L, { x: true }); eye(Rr, { x: true }); break;
      case 'surprised': eye(L, { s: 1.12 }); eye(Rr, { s: 1.35 }); break;
      case 'shocked': case 'scared': eye(L, { s: 1.45, pupil: [0, 0.12] }); eye(Rr, { s: 1.75, pupil: [0, 0.12] }); break;   // wide-eyed (reads at phone size)
      case 'unimpressed': eye(L, { lid: 0.5, pupil: [0, 0.3] }); eye(Rr, { lid: 0.45, pupil: [0, 0.2] }); break;
      case 'suspicious': eye(L, { lid: 0.5, pupil: [0.35, 0.2] }); eye(Rr, { pupil: [0.35, 0] }); break;
      case 'smug': eye(L, { lid: 0.45, pupil: [0.25, 0.3] }); eye(Rr, { lid: 0.35, pupil: [0.25, 0.1] }); break;
      case 'angry': eye(L, { lid: 0.38 }); eye(Rr, { lid: 0.3 }); break;
      case 'sad': case 'worried': eye(L, { pupil: [0, 0.35] }); eye(Rr, { pupil: [0, 0.3] }); break;
      case 'disgusted': eye(L, { lid: 0.5 }); eye(Rr, { s: 1.1 }); break;
      case 'sideLook': eye(L, { pupil: [0.55, 0] }); eye(Rr, { pupil: [0.55, 0] }); break;
      default: eye(L); eye(Rr);
    }
  }
  if (touchMouth) {
    const m = F.mouth, mc = X((m.x0 + m.x1) / 2), my = Y(m.y);
    g.strokeStyle = ink; g.fillStyle = '#2A0E0A'; g.lineWidth = 9; g.beginPath();
    switch (e) {
      case 'surprised': g.ellipse(mc, my + 6, 16, 22, 0, 0, Math.PI * 2); g.fill(); break;
      case 'shocked': case 'scared': g.moveTo(mc - 44, my - 18); g.lineTo(mc + 44, my - 18); g.lineTo(mc + 32, my + 46); g.lineTo(mc - 32, my + 46); g.closePath(); g.fill(); g.lineWidth = 7; g.stroke(); g.fillStyle = white; g.fillRect(mc - 34, my - 14, 68, 12); g.fillStyle = '#C46A6A'; g.beginPath(); g.ellipse(mc, my + 38, 20, 8, 0, Math.PI, 0); g.fill(); break;
      case 'grimace': g.fillRect(mc - 52, my - 16, 104, 34); g.lineWidth = 7; g.strokeRect(mc - 52, my - 16, 104, 34); g.fillStyle = white; for (let k = 0; k < 5; k++) { g.fillRect(mc - 46 + k * 19, my - 12, 14, 11); g.fillRect(mc - 46 + k * 19, my + 3, 14, 11); } break;
      case 'talk': g.ellipse(mc, my + 2, 24, 12, 0, 0, Math.PI * 2); g.fill(); break;
      case 'happy': g.arc(mc, my - 36, 50, Math.PI * 0.22, Math.PI * 0.78); g.stroke(); break;
      case 'smug': g.moveTo(X(m.x0) + 8, my); g.quadraticCurveTo(mc + 10, my + 14, X(m.x1), my - 12); g.stroke(); break;
      case 'sad': g.arc(mc, my + 40, 40, Math.PI * 1.22, Math.PI * 1.78); g.stroke(); break;
      case 'angry': case 'disgusted': g.moveTo(X(m.x0), my + 8); g.lineTo(mc - 12, my - 4); g.lineTo(mc + 16, my + 6); g.lineTo(X(m.x1), my - 4); g.stroke(); break;
      case 'dead': g.moveTo(X(m.x0), my); g.lineTo(X(m.x1), my); g.stroke(); g.fillStyle = '#C46'; g.fillRect(mc + 6, my, 18, 24); break;
      default: g.moveTo(X(m.x0), my); g.lineTo(X(m.x1), my); g.stroke();
    }
  }
  g.strokeStyle = ink; g.lineWidth = 12; g.strokeRect(6, 6, c.width - 12, c.height - 12); // ink border (cropped away with the sides)
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  faceCache.set(expression, tex); return tex;
}

// Side of the head: the atlas panel's lower-back corner belongs to the jacket zone (navy),
// so it is patched with skin from the same panel. mirror=true for the character's right side.
const sideCache = {};
function sideCanvas(withEar = true) {
  const c = crop(R.headSide), g = c.getContext('2d'), s = crop(F.cleanSkin);
  g.drawImage(s, 596 - R.headSide[0], 620 - R.headSide[1], 668 - 596, 762 - 620); // navy corner -> skin (hard edge: it meets the panel border)
  feathered(g, s, 570 - R.headSide[0], 596 - R.headSide[1], 110, 60, 20); // soften the top seam of that patch
  if (!withEar) feathered(g, s, 446 - R.headSide[0], 488 - R.headSide[1], 178, 214, 16);  // hide painted ear
  return c;
}
export function atlasSideTexture(mirror = false) {
  const k = mirror ? 'm' : 'n'; if (sideCache[k] || !atlasImage) return sideCache[k];
  const t = new THREE.CanvasTexture(sideCanvas(true)); t.colorSpace = THREE.SRGBColorSpace;
  if (mirror) { t.wrapS = THREE.RepeatWrapping; t.repeat.x = -1; t.offset.x = 1; }
  return (sideCache[k] = t);
}
// Back of the head: hair cap with drips, no ear.
export function atlasBackTexture() {
  if (sideCache.back || !atlasImage) return sideCache.back;
  const t = new THREE.CanvasTexture(sideCanvas(false)); t.colorSpace = THREE.SRGBColorSpace; return (sideCache.back = t);
}
