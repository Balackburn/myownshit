// Face rig (opt-in, comes with the cartoon rig: cast `toon: true`, script `"rig": "toon"`, or `faceRig: true` alone).
// The painted face of le mec as layers (tools/face/gen_rig.py -> characters/lemec/face/rig): a blank face, and one painted sprite per
// feature state. The engine composes them on a canvas for every frame, so brows slide and tilt, lids close continuously, pupils
// travel, eyes grow, the mouth changes shape, cheeks rise, each side on its own. At rest the rig gives back the measured neutral face.
//
// A face state (all numbers blend):
//   brows: { L|R: { dx, dy, rot (deg, >0 lifts the inner end), shape: 'flat' | 'arch' | 'bold' | 'straight' } }
//   eyes:  { L|R: { kind: 'open' | 'closed' | 'happy' | 'flat' | 'squeeze' | 'x' | 'spiral' | 'heart' | 'star' | 'dot' | 'euro',
//                   s (size), lid 0..1 (upper lid), low 0..0.5 (lower lid), px, py (pupil, -1..1), ps (pupil size), shine, open (0..1, y scale of a drawn eye) } }
//   mouth: { spr (sprite name), dx, dy, w, h, tilt, flip }      cheeks 0..1      puff 0..1      extras: { tears|tear|sweat|blush|vein|shadow: 0..1 }
// Expressions are the recipes of the face set (rig.json "presets", same format as tools/face/gen_expressions.py), plus the rig's own
// (take, takeSmall, deadpan, dotEyes, greed, zap, gulp, puffed, strain, teeth, hmm, side, sideL); a script can add its own under "faces".
import * as THREE from 'three';
import { EXPR_MAP, FACE_FILTER, toneFace, variantRigLayers } from './atlas.js';

const DIR = '/characters/lemec/face/rig';
const loadImg = n => new Promise(res => { const im = new Image(); im.onload = () => res(im); im.onerror = () => res(null); im.src = `${DIR}/${n}`; });
export const RIG = await (async () => {
  try {
    const j = await (await fetch(DIR + '/rig.json')).json(); const [blank, clean, img] = await Promise.all(['blank.png', 'blank_clean.png', 'sprites.png'].map(loadImg));
    return blank && img ? { ...j, blank, clean: clean || blank, img } : null;
  } catch { return null; }
})();
export const hasFaceRig = !!RIG;

// ---- recipes -> states
const LINE = [[-12, 'line_m12'], [-6, 'line_m6'], [0, 'line'], [6, 'line_p6'], [12, 'line_p12'], [20, 'line_p20']];
function mouthSprite(m) {
  const k = m.kind || 'line', c = m.curve;
  if (k === 'line') { let best = LINE[2]; for (const e of LINE) if (Math.abs(e[0] - (c || 0)) < Math.abs(best[0] - (c || 0))) best = e; return best[1]; }
  if (k === 'smile') return (c ?? 1) <= 0.6 ? 'smile_05' : (c ?? 1) <= 0.85 ? 'smile_07' : 'smile';
  if (k === 'frown') return (c ?? 1) < 0.8 ? 'frown_05' : 'frown';
  return k;
}
function fromRecipe(rec = {}) {
  const st = { brows: {}, eyes: {}, cheeks: rec.cheeks || 0, puff: rec.puff || 0, extras: {} };
  for (const s of 'LR') {
    const b = rec.brows?.[s] || {}, e = rec.eyes?.[s] || {}, a = RIG.anchors['eye' + s];
    st.brows[s] = { dx: b.dx || 0, dy: b.dy || 0, rot: b.rot || 0, shape: b.shape || ((b.thick || 1) > 1.1 ? 'bold' : (b.bulge || 0) > 7 ? 'arch' : 'flat') };
    st.eyes[s] = { kind: e.kind || 'open', s: e.s ?? 1, lid: e.lid || 0, low: e.low || 0, px: e.pupil ? e.pupil[0] : a.rest[0], py: e.pupil ? e.pupil[1] : a.rest[1], ps: e.psize ?? 1, shine: !!e.shine, open: 1 };
  }
  const m = rec.mouth || {}; st.mouth = { spr: m.spr || mouthSprite(m), dx: m.dx || 0, dy: m.dy || 0, w: m.w ?? 1, h: m.h ?? 1, tilt: m.tilt || 0, flip: !!m.flip };
  for (const x of rec.extras || []) st.extras[x] = 1;
  return st;
}
const stateCache = new Map();
export function faceState(name, custom) {   // an expression name (engine or face-set name, or one of the script's own "faces") -> state
  const own = custom && custom[name], n = own ? name : (EXPR_MAP[name] || name), key = (own ? '@' : '') + n;
  if (!stateCache.has(key)) stateCache.set(key, fromRecipe(own || RIG.presets[n] || RIG.presets.neutral));
  return stateCache.get(key);
}
export const hasFace = (name, custom) => !!(custom && custom[name]) || !!RIG.presets[EXPR_MAP[name] || name];

// ---- blend two states: the brows lead, the eyes follow, the mouth trails (three weights); a change of eye kind passes through a
// closed eye, a change of mouth shape through a flattened mouth
const lerp = (a, b, w) => a + (b - a) * w, c01 = x => x < 0 ? 0 : x > 1 ? 1 : x;
export function blendFace(A, B, wb, we = wb, wm = we) {
  const out = { brows: {}, eyes: {}, extras: {} };
  for (const s of 'LR') {
    const a = A.brows[s], b = B.brows[s]; out.brows[s] = { dx: lerp(a.dx, b.dx, wb), dy: lerp(a.dy, b.dy, wb), rot: lerp(a.rot, b.rot, wb), shape: wb < 0.5 ? a.shape : b.shape };
    const x = A.eyes[s], y = B.eyes[s], cur = we < 0.5 ? x : y;
    const e = { kind: cur.kind, s: lerp(x.s, y.s, we), lid: lerp(x.lid, y.lid, we), low: lerp(x.low, y.low, we), px: lerp(x.px, y.px, we), py: lerp(x.py, y.py, we), ps: lerp(x.ps, y.ps, we), shine: cur.shine, open: 1 };
    if (x.kind !== y.kind) { const c = Math.abs(1 - 2 * c01(we)); if (cur.kind === 'open') e.lid = Math.max(e.lid, 1 - c); else e.open = 0.12 + 0.88 * c; }
    out.eyes[s] = e;
  }
  const m = A.mouth, n = B.mouth, cur = wm < 0.5 ? m : n, sw = m.spr !== n.spr;
  out.mouth = { spr: cur.spr, dx: lerp(m.dx, n.dx, wm), dy: lerp(m.dy, n.dy, wm), w: lerp(m.w, n.w, wm), h: lerp(m.h, n.h, wm) * (sw ? 0.4 + 0.6 * Math.abs(1 - 2 * c01(wm)) : 1), tilt: lerp(m.tilt, n.tilt, wm), flip: cur.flip };
  out.cheeks = lerp(A.cheeks, B.cheeks, we); out.puff = lerp(A.puff, B.puff, wm);
  for (const k of new Set([...Object.keys(A.extras), ...Object.keys(B.extras)])) out.extras[k] = c01(lerp(A.extras[k] || 0, B.extras[k] || 0, we));
  return out;
}
export const cloneFace = st => ({ brows: { L: { ...st.brows.L }, R: { ...st.brows.R } }, eyes: { L: { ...st.eyes.L }, R: { ...st.eyes.R } }, mouth: { ...st.mouth }, cheeks: st.cheeks, puff: st.puff, extras: { ...st.extras } });

// ---- layers: the hero's own, or a variant's (skin tone, hair line, clean-shaven, lipstick, and the painted features over the face)
const layerCache = new Map();
function filtered(im) { const c = document.createElement('canvas'); c.width = im.width; c.height = im.height; const g = c.getContext('2d'); g.filter = FACE_FILTER; g.drawImage(im, 0, 0); g.filter = 'none'; return c; }
function spriteSheet(lipstick) {
  const key = 'spr' + (lipstick ? 1 : 0); if (layerCache.has(key)) return layerCache.get(key);
  const c = filtered(RIG.img);
  if (lipstick) {   // the mouth's ink turns red (open mouths keep their dark inside), as on the variants of the face set
    const g = c.getContext('2d');
    for (const [n, r] of Object.entries(RIG.sprites)) { if (!n.startsWith('mouth_')) continue; const id = g.getImageData(r[0], r[1], r[2], r[3]), d = id.data; for (let i = 0; i < d.length; i += 4) if (d[i + 3] > 0 && d[i] + d[i + 1] + d[i + 2] < 210 && d[i] < 90) { d[i] = 168; d[i + 1] = 38; d[i + 2] = 42; } g.putImageData(id, r[0], r[1]); }
  }
  layerCache.set(key, c); return c;
}
function layersFor(v) {
  if (!v) { if (!layerCache.has('hero')) layerCache.set('hero', { base: filtered(RIG.blank), sprites: spriteSheet(false) }); return layerCache.get('hero'); }
  const clean = !['stubble', 'beard'].includes(v.facial ?? 'stubble'), key = [clean, v.skin, v.hair, v.hairColor, v.facial, v.glasses, v.glassesColor, v.lipstick, v.redNose, v.beardColor, v.seed].join('|');
  if (!layerCache.has(key)) { const base = filtered(clean ? RIG.clean : RIG.blank); toneFace(base.getContext('2d'), { ...v, lipstick: false }); layerCache.set(key, { base, sprites: spriteSheet(!!v.lipstick), ...variantRigLayers(v) }); }
  return layerCache.get(key);
}

// ---- one rig per character: a canvas texture redrawn when the state changes
const nearest = (list, v) => { let b = list[0]; for (const x of list) if (Math.abs(Math.log(v / x)) < Math.abs(Math.log(v / b))) b = x; return b; };
const q = (x, s) => Math.round(x / s) * s;
let scratch = null;
const GLOW_INK = '#F1E9D6', GLOW_OWN = new Set(['heart', 'star', 'euro']);   // in the dark: drawn eyes in the pale of an eye white; these keep their colours
const GLOW_MOUTHS = new Set(['teeth', 'grimace', 'clench', 'bigsmile', 'laugh', 'open', 'scream', 'evil', 'tongueout', 'tongue']);   // mouths with teeth or a tongue: they show in the dark
export function makeFaceRig(v = null) {
  const [W, H] = RIG.size, c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d'), L = layersFor(v), S = RIG.sprites, A = RIG.anchors;
  if (!scratch) { scratch = document.createElement('canvas'); scratch.width = W; scratch.height = H; }
  const sg = scratch.getContext('2d');
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  // a sprite drawn where it was painted, moved by (dx, dy), turned and scaled about (ax, ay)
  // a sprite drawn enlarged is taken from a copy of its own (2 px of clear margin): straight from the sheet, the filter picked up the edge of the
  // sprite next to it: a thin dark line beside a pupil drawn three times its size (dark-room eyes)
  const isoCache = new Map();
  const iso = name => { let c = isoCache.get(name); if (!c) { const r = S[name]; c = document.createElement('canvas'); c.width = r[2] + 4; c.height = r[3] + 4; c.getContext('2d').drawImage(L.sprites, r[0], r[1], r[2], r[3], 2, 2, r[2], r[3]); isoCache.set(name, c); } return c; };
  const spr = (ctx, name, ax, ay, dx = 0, dy = 0, rot = 0, sx = 1, sy = 1, alpha = 1) => {
    const r = S[name]; if (!r) return false;
    ctx.save(); ctx.translate(ax + dx, ay + dy); if (rot) ctx.rotate(rot); if (sx !== 1 || sy !== 1) ctx.scale(sx, sy); if (alpha < 1) ctx.globalAlpha = alpha;
    if (Math.abs(sx) > 1.15 || Math.abs(sy) > 1.15) ctx.drawImage(iso(name), r[4] - ax - 2, r[5] - ay - 2); else ctx.drawImage(L.sprites, r[0], r[1], r[2], r[3], r[4] - ax, r[5] - ay, r[2], r[3]);
    ctx.restore(); return true;
  };
  const centre = name => { const r = S[name]; return r ? [r[4] + r[2] / 2, r[5] + r[3] / 2] : [0, 0]; };
  let tg = g;   // where the eyes are drawn: the face, or the glow layer (the eyes alone, for a shot in the dark)
  function eye(s, e) {
    const a = A['eye' + s], cx = a.cx, cy = a.cy, dark = tg !== g;
    if (e.kind !== 'open') {
      if (dark) { if (e.kind === 'closed') return;   // in the dark a shut eye is gone; a drawn eye (a cross, a spiral, a happy arc) shows in pale ink, a coloured one (heart, star, euro) as it is
        const x0 = Math.floor(cx - a.w * e.s) - 20, y0 = Math.floor(cy - a.h * e.s) - 20, w = Math.ceil(2 * a.w * e.s) + 40, h = Math.ceil(2 * a.h * e.s) + 40;
        const hrx = a.w * 0.56 * e.s, hox = e.kind === 'heart' ? Math.round(Math.max(0, 6 - (cx - hrx)) + Math.min(0, (W - 6) - (cx + hrx))) : 0;   // a heart eye slides inward rather than off the panel (its white was cut flat by the edge of the canvas)
        if (e.kind === 'heart') { tg.fillStyle = GLOW_INK; tg.beginPath(); tg.ellipse(cx + hox, cy, hrx, a.h * 0.56 * e.s * (e.open ?? 1), 0, 0, 2 * Math.PI); tg.fill(); }   // a heart in the dark sits on the white of its eye
        const hk = e.kind === 'heart' ? 0.74 : 1;
        sg.clearRect(x0, y0, w, h); if (!spr(sg, `eye${s}_${e.kind}`, cx, cy, 0, 0, 0, e.s * hk, e.s * hk * (e.open ?? 1))) return;
        if (!GLOW_OWN.has(e.kind)) { sg.globalCompositeOperation = 'source-in'; sg.fillStyle = GLOW_INK; sg.fillRect(x0, y0, w, h); sg.globalCompositeOperation = 'source-over'; }
        tg.drawImage(scratch, x0, y0, w, h, x0 + hox, y0, w, h); return; }
      if (!spr(g, `eye${s}_${e.kind}`, cx, cy, 0, 0, 0, e.s, e.s * (e.open ?? 1))) spr(g, `eye${s}_closed`, cx, cy); return; }
    if (e.lid >= 0.9) { if (!dark) spr(g, `eye${s}_closed`, cx, cy, 0, 0.24 * a.h * e.s, 0, e.s, 1); return; }   // shut: the lid line has reached the lower lid
    const P = nearest(RIG.sizes, e.s), k = e.s / P, hh = a.h / 2 * e.s, hw = a.w / 2 * e.s, tag = Math.round(P * 100);
    const ox = Math.max(0, 14 - (cx - hw)) + Math.min(0, (W - 14) - (cx + hw));   // a big eye slides inward rather than off the panel
    tg.save(); tg.translate(Math.round(ox), 0); eyeOpen(s, e, a, cx, cy, P, k, hh, hw, tag); tg.restore();
  }
  function eyeOpen(s, e, a, cx, cy, P, k, hh, hw, tag) {
    const x0 = Math.floor(cx - hw - 14), y0 = Math.floor(cy - hh - 14), w = Math.ceil(2 * hw + 28), h = Math.ceil(2 * hh + 28);
    sg.clearRect(x0, y0, w, h);
    spr(sg, `eye${s}_u_${tag}`, cx, cy, 0, 0, 0, k, k);
    // the pupil stays inside the white
    const PS = nearest(RIG.psizes, e.ps), kp = e.ps / PS, n = Math.hypot(e.px, e.py), f = n > 1 ? 1 / n : 1;
    const px = e.px * f * Math.max(0, a.rx * e.s - a.prx * e.ps - 4), py = e.py * f * Math.max(0, a.ry * e.s - a.pry * e.ps - 4);
    sg.globalCompositeOperation = 'source-atop'; spr(sg, `pupil${s}_${Math.round(PS * 100)}${e.shine && PS >= 1.4 ? 's' : ''}`, cx, cy, px, py, 0, kp, kp); sg.globalCompositeOperation = 'source-over';
    spr(sg, `eye${s}_o_${tag}`, cx, cy, 0, 0, 0, k, k);
    const top = cy - hh + 2 * hh * e.lid, bot = cy + hh - 2 * hh * e.low, cutT = e.lid > 0.03, cutB = e.low > 0.03;
    tg.save(); tg.beginPath(); tg.rect(x0, cutT ? top : y0, w, Math.max(0, (cutB ? bot : y0 + h) - (cutT ? top : y0))); tg.clip(); tg.drawImage(scratch, x0, y0, w, h, x0, y0, w, h); tg.restore();
    if (tg !== g) return;   // the lid lines are ink: nothing of them in the dark
    if (cutT) spr(g, 'lid' + s, cx, cy, 0, top - cy, 0, e.s, 1);
    if (cutB) spr(g, 'lidlow' + s, cx, cy, 0, bot - cy, 0, e.s, 1);
  }
  // a pale rim round the brows, the eyes and the mouth (variant `rim`: true = from the skin's luminance, or 0..1): on a dark skin the black line work has
  // no contrast and the face reads as a plain box at phone size. Off by default: nothing changes for the stories made before
  const lumOf = hex => { const n = parseInt(String(hex || '#E2B48A').slice(1), 16); return (0.3 * (n >> 16 & 255) + 0.59 * (n >> 8 & 255) + 0.11 * (n & 255)) / 255; };
  const rim = v?.rim ? (v.rim === true ? c01((0.6 - lumOf(v.skin)) / 0.22) * 0.95 : +v.rim) : 0;
  const RIM = [[3, 0], [-3, 0], [0, 3], [0, -3], [2.2, 2.2], [-2.2, 2.2], [2.2, -2.2], [-2.2, -2.2]];   // the features are drawn once per offset with a crisp pale shadow: a light outline round every stroke
  const rimOff = () => { g.shadowColor = 'rgba(0, 0, 0, 0)'; g.shadowBlur = 0; g.shadowOffsetX = 0; g.shadowOffsetY = 0; };
  function draw(st) {
    g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.globalCompositeOperation = 'source-over'; rimOff(); g.drawImage(L.base, 0, 0);
    const X = st.extras || {};
    for (const k of ['shadow', 'blush']) if (X[k] > 0.02) spr(g, 'extra_' + k, 0, 0, 0, 0, 0, 1, 1, c01(X[k]));
    for (const s of 'LR') {
      if (st.cheeks > 0.02) { const [x, y] = centre('cheek' + s); spr(g, 'cheek' + s, x, y, 0, 8 - 14 * st.cheeks, 0, 1, 1, c01(st.cheeks * 1.6)); }
      if (st.puff > 0.02) { const [x, y] = centre('puff' + s); spr(g, 'puff' + s, x + (s === 'L' ? 30 : -30), y, (s === 'L' ? -1 : 1) * 10 * (st.puff - 1), 0, 0, 0.5 + 0.5 * st.puff, 0.7 + 0.3 * st.puff, c01(st.puff * 1.6)); }
    }
    const m = st.mouth, ma = A.mouth, features = () => {
      for (const s of 'LR') { const b = st.brows[s], [ax, ay] = A['brow' + s]; spr(g, `brow${s}_${b.shape}`, ax, ay, b.dx, b.dy, -b.rot * Math.PI / 180); }
      for (const s of 'LR') eye(s, st.eyes[s]);
      spr(g, 'mouth_' + m.spr, ma.cx, ma.cy, m.dx, m.dy, -Math.atan2(m.tilt, ma.hw), m.w * (m.flip ? -1 : 1), m.h); };
    if (rim > 0.02) { g.shadowColor = `rgba(255, 236, 205, ${rim})`; g.shadowBlur = 0; for (const [ox, oy] of RIM) { g.shadowOffsetX = ox; g.shadowOffsetY = oy; features(); } rimOff(); }
    features();
    for (const k of ['tears', 'tear', 'sweat', 'vein']) if (X[k] > 0.02) spr(g, 'extra_' + k, 0, 0, 0, 0, 0, 1, 1, c01(X[k]));
    if (L.lens) g.drawImage(L.lens, 0, 0);
    if (L.ov) g.drawImage(L.ov, 0, 0);
    if (L.lash && st.eyes.L.kind === 'open' && st.eyes.L.lid < 0.6) g.drawImage(L.lash, 0, 0);
    const lw = Math.round(W * 0.03); g.strokeStyle = '#151313'; g.lineWidth = lw; g.strokeRect(lw / 2, lw / 2, W - lw, H - lw);
  }
  const keyOf = st => {
    let k = '';
    for (const s of 'LR') { const b = st.brows[s], e = st.eyes[s]; k += `${b.shape},${q(b.dx, 0.5)},${q(b.dy, 0.5)},${q(b.rot, 0.5)}|${e.kind},${q(e.s, 0.01)},${q(e.lid, 0.02)},${q(e.low, 0.02)},${q(e.px, 0.02)},${q(e.py, 0.02)},${q(e.ps, 0.02)},${e.shine ? 1 : 0},${q(e.open ?? 1, 0.03)}|`; }
    const m = st.mouth; k += `${m.spr},${q(m.dx, 0.5)},${q(m.dy, 0.5)},${q(m.w, 0.01)},${q(m.h, 0.01)},${q(m.tilt, 0.5)},${m.flip ? 1 : 0}|${q(st.cheeks, 0.03)},${q(st.puff, 0.03)}`;
    for (const [n, a] of Object.entries(st.extras || {})) if (a > 0.02) k += `|${n}${q(a, 0.05)}`;
    return k;
  };
  let last = null;
  // the glow layer (a shot in the dark, scene `dark`): the eyes alone, and a mouth that shows teeth, on a clear canvas of the same size. The head carries it
  // on a second skin that stays lit when the picture goes black (engine/human.js setEyeGlow, engine/look.js)
  let gc = null, gg = null, gtex = null, glast = null;
  function glow(st, big = 1.3) {   // big: the eyes grow in the dark (two white ovals must read on a phone), and a heavy lid lifts; a blink still shuts them
    if (!gc) { gc = document.createElement('canvas'); gc.width = W; gc.height = H; gg = gc.getContext('2d'); gtex = new THREE.CanvasTexture(gc); gtex.colorSpace = THREE.SRGBColorSpace; gtex.anisotropy = 8; }
    const k = keyOf(st) + '|' + big; if (k === glast) return gtex; glast = k;
    gg.setTransform(1, 0, 0, 1, 0, 0); gg.globalAlpha = 1; gg.globalCompositeOperation = 'source-over'; gg.clearRect(0, 0, W, H);
    tg = gg; for (const s of 'LR') { const e = st.eyes[s]; eye(s, big === 1 ? e : { ...e, s: Math.min(1.9, e.s * big), ps: big > 1.9 ? Math.max(e.ps, 1) * 3.2 : e.ps, lid: e.lid < 0.6 ? e.lid * 0.3 : 0.18 + 0.82 * (e.lid - 0.6) / 0.4, low: e.low * 0.5 }); } tg = g;   // above 1.9 the skin itself is scaled (engine/human.js): the pupils are drawn three times their size (about a third of the eye) so that a look still reads
    const m = st.mouth, ma = A.mouth; if (GLOW_MOUTHS.has(m.spr)) spr(gg, 'mouth_' + m.spr, ma.cx, ma.cy, m.dx, m.dy, -Math.atan2(m.tilt, ma.hw), m.w * (m.flip ? -1 : 1), m.h);
    gtex.needsUpdate = true; return gtex;
  }
  return { texture: tex, canvas: c, glow, set(st) { const k = keyOf(st); if (k === last) return false; last = k; draw(st); tex.needsUpdate = true; return true; } };
}
