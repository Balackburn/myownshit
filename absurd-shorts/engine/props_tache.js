// « La tache » (story 93): this man stained his shirt; the stain refused to leave; the judge signed its eviction; the riot police charged the
// shirt; the stain dug in under the pocket; a tank fired stain remover; it bleached the whole neighbourhood; the houses, the cars, the mayor; the
// stain stayed red; stretched, it had the exact shape of the country; a presidential decree forbids washing it; the shirt replaced the flag; two
// guards salute it day and night; the embassies recognised the stain; the shirt stays his, and so does the upkeep; he irons around the stain.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
// The stain is drawn on the shirt's opaque canvas (never a transparent decal), and is never a round disc: an irregular orange-red splat with a
// strand of pasta and one drip, which the jet stretches into a long splash with drips (the invented country, made-up coastline).
import * as THREE from 'three';
import { box, cyl, sphere, mat } from './style.js';
import { grp, at, canvasPlane, buildProp, rod, glowSprite } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const easeOut = x => { const u = clamp01(x); return 1 - (1 - u) * (1 - u); };
const outBack = x => { const u = clamp01(x), c = 1.70158; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const lerp = (a, b, u) => a + (b - a) * u;
// (round 1) a cool white: the warm grade turned the old warm white peach
const INK = '#1B1B1E', SHIRT = '#E2EBF8', SEAM = '#7E8894', CHROME = '#C9CED4';
const STAIN = '#D8452A', STAIN_D = '#A63221', STAIN_L = '#EE7048', PASTA = '#F1D06E', PASTA_D = '#B98E34';
const BLEACH = new THREE.Color('#F6F8FA'), WHITE = new THREE.Color('#FFFFFF'), COOL = new THREE.Color('#2E4466');

// ---------------------------------------------------------------- the stain: one shape, two states (u 0: the splat, u 1: the country)
// coordinates in fractions of the shirt's width, canvas axes (y down), origin at the stain's centre; both outlines have NS points so they morph
const NS = 40;
const SPLAT = (() => { const p = []; for (let i = 0; i < NS; i++) { const a = i / NS * TAU; let r = 0.072 * (1 + 0.16 * Math.sin(3 * a + 0.7) + 0.1 * Math.sin(5 * a + 2.1) + 0.05 * Math.sin(9 * a + 1.3));
  if (i % 10 === 3) r += 0.05; if (i % 10 === 4) r += 0.016; if (i === 17) r += 0.03; p.push([Math.cos(a) * r, Math.sin(a) * r * 0.92]); } return p; })();
const COUNTRY = (() => { const p = [], A = 0.31, Bb = 0.092; for (let i = 0; i < NS; i++) { const a = i / NS * TAU, c = Math.cos(a), s = Math.sin(a);
  let r = A * Bb / Math.sqrt((Bb * c) ** 2 + (A * s) ** 2); r *= 1 + 0.12 * Math.sin(4 * a + 1.0) + 0.08 * Math.sin(7 * a + 0.3) + 0.05 * Math.sin(11 * a + 2.0);
  let x = c * r, y = s * r; if (x > 0) y *= 1 - 0.55 * x / A; else y *= 1 + 0.25 * (-x / A);
  if (i === 6) { x *= 1.04; y *= 1.5; } if (i === 25) { y *= 1.45; } if (i === 31) { y *= 0.6; } if (i === 13) { y *= 1.3; }
  p.push([x + 0.02, y]); } return p; })();
// drips: [x, length, width]; dots: [x, y, r]; the pasta strand: a polyline
const DRIPS = [[[0.012, 0.07, 0.018], [-0.03, 0.0, 0.012], [0.03, 0.0, 0.012], [-0.05, 0.0, 0.01], [0.05, 0.0, 0.01]],
               [[-0.2, 0.1, 0.019], [-0.09, 0.17, 0.021], [0.02, 0.075, 0.016], [0.12, 0.13, 0.016], [0.22, 0.06, 0.012]]];
const DOTS = [[[-0.13, -0.065, 0.012], [0.145, -0.03, 0.011], [0.11, 0.095, 0.009], [-0.1, 0.1, 0.008], [0.01, -0.13, 0.01], [-0.165, 0.025, 0.007]],
              [[0.37, -0.01, 0.012], [0.42, 0.02, 0.009], [0.46, -0.02, 0.007], [0.34, 0.045, 0.008], [-0.31, -0.06, 0.009], [0.39, -0.05, 0.006]]];
const PASTAL = [[[-0.07, -0.035], [-0.025, -0.002], [0.02, -0.022], [0.064, 0.012]], [[-0.21, -0.03], [-0.06, 0.004], [0.1, -0.022], [0.28, 0.006]]];
function stainShape(u) {
  const m = (A, B) => A.map((a, i) => a.map((v, j) => lerp(v, B[i][j], u)));
  return { poly: m(SPLAT, COUNTRY), drips: m(DRIPS[0], DRIPS[1]), dots: m(DOTS[0], DOTS[1]), pasta: m(PASTAL[0], PASTAL[1]) };
}
// the lowest point of the outline under x (where a drip starts)
function bottomY(poly, x) {
  let best = 0;
  for (let i = 0; i < poly.length; i++) { const [x1, y1] = poly[i], [x2, y2] = poly[(i + 1) % poly.length];
    if ((x1 - x) * (x2 - x) <= 0 && x1 !== x2) { const y = y1 + (y2 - y1) * (x - x1) / (x2 - x1); if (y > best) best = y; } }
  return best;
}
// s: {u, cx, cy (fractions of the canvas), sc (size factor), k (pop 0..1)}; the shape's units are fractions of the width W
function drawStain(c, W, H, s, outlineOnly = false, col = null) {
  const sh = stainShape(s.u), k = s.k ?? 1, f = W * (s.sc ?? 1) * k, X = x => s.cx * W + x * f, Y = y => s.cy * H + y * f;
  const path = () => { c.beginPath(); sh.poly.forEach(([x, y], i) => { const j = (i + 1) % sh.poly.length, [x2, y2] = sh.poly[j], mx = (x + x2) / 2, my = (y + y2) / 2; if (i === 0) c.moveTo(X(mx), Y(my)); else c.quadraticCurveTo(X(x), Y(y), X(mx), Y(my)); });
    const [x0, y0] = sh.poly[0], [x1, y1] = sh.poly[1]; c.quadraticCurveTo(X(x0), Y(y0), X((x0 + x1) / 2), Y((y0 + y1) / 2)); c.closePath(); };
  const drip = ([x, len, w], ext = 0) => { if (len + ext < 0.004) return; const y0 = bottomY(sh.poly, x) - 0.012, y1 = y0 + 0.012 + len + ext;
    c.beginPath(); c.moveTo(X(x - w / 2), Y(y0)); c.lineTo(X(x - w * 0.42), Y(y1)); c.arc(X(x), Y(y1), w * 0.62 * f, PI, 0, true); c.lineTo(X(x + w / 2), Y(y0)); c.closePath(); };
  if (outlineOnly) {
    c.strokeStyle = col || '#1F4E8C'; c.lineWidth = Math.max(2, (s.lw ?? 0.009) * W); c.lineJoin = 'round';
    path(); c.stroke(); sh.drips.forEach(d => { drip(d); c.stroke(); });
    return;
  }
  c.fillStyle = STAIN; c.strokeStyle = STAIN_D; c.lineWidth = Math.max(1.5, 0.006 * W) * k; c.lineJoin = 'round';
  path(); c.fill(); sh.drips.forEach(d => { drip(d, s.ext ?? 0); c.fill(); }); path(); c.stroke(); sh.drips.forEach(d => { drip(d, s.ext ?? 0); c.stroke(); });
  sh.dots.forEach(([x, y, r]) => { c.beginPath(); c.ellipse(X(x), Y(y), r * f * 1.25, r * f * 0.85, 0.4, 0, TAU); c.fill(); });
  // a highlight and a few darker lumps of tomato
  c.fillStyle = STAIN_L; c.beginPath(); c.ellipse(X(-0.025 - 0.08 * s.u), Y(-0.02), 0.03 * f * (1 + 2.2 * s.u), 0.013 * f, -0.3, 0, TAU); c.fill();
  c.fillStyle = STAIN_D; [[0.02, 0.02], [-0.04, 0.015], [0.035, -0.03]].forEach(([x, y], i) => { c.beginPath(); c.ellipse(X(x * (1 + 3 * s.u)), Y(y), 0.008 * f * (1 + s.u), 0.006 * f, i, 0, TAU); c.fill(); });
  // the strand of pasta stuck in it
  c.lineCap = 'round'; c.lineJoin = 'round';
  for (const [lw, cl] of [[0.016, PASTA_D], [0.011, PASTA]]) { c.strokeStyle = cl; c.lineWidth = lw * f; c.beginPath(); sh.pasta.forEach(([x, y], i) => (i ? c.lineTo(X(x), Y(y)) : c.moveTo(X(x), Y(y)))); c.stroke(); }
}

// ---------------------------------------------------------------- the shirt's front: collar, placket, buttons, breast pocket, the stain
// lay: {pocket: [u0, u1, v0, v1] (v in widths from the top), stainAt: [cx, cy] fractions, sc}; st: {u, k, slide (0..1 to the pocket), peek}
function drawShirt(c, W, H, o, st) {
  const V = v => v * W, bg = o.bg || SHIRT, seam = o.seam || SEAM;
  c.fillStyle = bg; c.fillRect(0, 0, W, H);
  c.strokeStyle = 'rgba(120,128,140,0.18)'; c.lineWidth = W * 0.006;
  [[0.18, 0.5, 0.24, 0.95], [0.82, 0.55, 0.76, 0.98], [0.3, 0.7, 0.36, 1.0]].forEach(([a, b, d, e]) => { c.beginPath(); c.moveTo(a * W, b * H); c.lineTo(d * W, e * H); c.stroke(); });
  // placket and buttons
  c.strokeStyle = seam; c.lineWidth = W * 0.007;
  for (const u of [0.468, 0.532]) { c.beginPath(); c.moveTo(u * W, V(0.09)); c.lineTo(u * W, H); c.stroke(); }
  for (let i = 0; i < 7; i++) { const y = V(0.16 + 0.13 * i); if (y > H - 4) break; c.fillStyle = o.button || '#E4E8EC'; c.beginPath(); c.arc(W * 0.5, y, W * 0.016, 0, TAU); c.fill(); c.strokeStyle = '#6E757E'; c.lineWidth = W * 0.005; c.stroke();
    c.fillStyle = '#6E757E'; for (const dx of [-0.005, 0.005]) { c.beginPath(); c.arc(W * (0.5 + dx), y, W * 0.0028, 0, TAU); c.fill(); } }
  // the stain, under the pocket
  if (st && st.k > 0.001) {
    const sl = smooth(st.slide || 0), pk = o.pocket || [0.6, 0.82, 0.2, 0.42];
    const cx = lerp(o.stainAt[0], (pk[0] + pk[1]) / 2, sl), cy = lerp(o.stainAt[1], V((pk[2] + pk[3]) / 2) / H, sl);
    const u = st.u || 0, cx2 = lerp(cx, o.countryAt ? o.countryAt[0] : cx, u), cy2 = lerp(cy, o.countryAt ? o.countryAt[1] : cy, u);
    // (round 1) the stain lives: a crouch and a wriggle before it runs (st.wig, st.crouch), stretched into a smear along its way while it slides
    const dx = ((pk[0] + pk[1]) / 2 - o.stainAt[0]) * W, dy = V((pk[2] + pk[3]) / 2) - o.stainAt[1] * H, ang = Math.atan2(dy, dx);
    const sm = 1 + 2.4 * Math.sin(PI * clamp01(st.slide || 0)) * (st.slide > 0 && st.slide < 1 ? 1 : 0), cr = st.crouch || 0;
    c.save(); c.translate(cx2 * W, cy2 * H); c.rotate(ang); c.scale(sm, 1 / Math.sqrt(sm)); c.rotate(-ang); c.rotate(0.22 * (st.wig || 0)); c.scale(1 + 0.22 * cr, 1 - 0.3 * cr); c.translate(-cx2 * W, -cy2 * H);
    if (sm > 1.05) { c.globalAlpha = 0.35; drawStain(c, W, H, { u, cx: cx2 - 0.05 * Math.cos(ang) * sm, cy: cy2 - 0.05 * Math.sin(ang) * sm * W / H, sc: (o.sc ?? 1) * 0.9, k: st.k }); c.globalAlpha = 1; }
    drawStain(c, W, H, { u, cx: cx2, cy: cy2, sc: (o.sc ?? 1) * lerp(1, o.countrySc ?? 1, u) * (1 - 0.18 * sl), k: st.k, ext: st.ext || 0 });
    c.restore();
  }
  // the breast pocket (on his left, the right of the picture) with its flap, drawn over the stain
  if (o.pocket !== false) {
    const [u0, u1, v0, v1] = o.pocket || [0.6, 0.82, 0.2, 0.42];
    c.fillStyle = bg; c.strokeStyle = seam; c.lineWidth = W * 0.007;
    c.beginPath(); c.moveTo(u0 * W, V(v0)); c.lineTo(u1 * W, V(v0)); c.lineTo(u1 * W, V(v1 - 0.02)); c.lineTo((u0 + u1) / 2 * W, V(v1)); c.lineTo(u0 * W, V(v1 - 0.02)); c.closePath(); c.fill(); c.stroke();
    c.beginPath(); c.moveTo(u0 * W, V(v0 + 0.065)); c.lineTo((u0 + u1) / 2 * W, V(v0 + 0.09)); c.lineTo(u1 * W, V(v0 + 0.065)); c.stroke();
    c.fillStyle = o.button || '#E4E8EC'; c.beginPath(); c.arc((u0 + u1) / 2 * W, V(v0 + 0.07), W * 0.012, 0, TAU); c.fill(); c.strokeStyle = '#6E757E'; c.lineWidth = W * 0.004; c.stroke();
    // a drip peeking out from under the pocket (the stain has dug in)
    // (round 1) bigger, and it peeks out and ducks back in (st.peek keyed by o.peekKeys)
    if (st && st.peek > 0.01) { const x = (u0 + u1) / 2 + 0.02, y = V(v1 - 0.012), L = 0.1 * st.peek * W, w = 0.034 * W;
      c.fillStyle = STAIN; c.strokeStyle = STAIN_D; c.lineWidth = W * 0.006; c.beginPath(); c.moveTo(x * W - w / 2, y); c.lineTo(x * W - w * 0.45, y + L); c.arc(x * W, y + L, w * 0.62, PI, 0, true); c.lineTo(x * W + w / 2, y); c.closePath(); c.fill(); c.stroke(); }
  }
  // the collar: a band and two pointed flaps
  if (o.collar !== false) {
    c.fillStyle = bg; c.strokeStyle = seam; c.lineWidth = W * 0.008; c.lineJoin = 'round';
    for (const sd of [-1, 1]) { c.beginPath(); c.moveTo(W * (0.5 + sd * 0.012), V(0.085)); c.lineTo(W * (0.5 + sd * 0.17), V(0.0)); c.lineTo(W * (0.5 + sd * 0.215), V(0.012)); c.lineTo(W * (0.5 + sd * 0.115), V(0.15)); c.closePath(); c.fill(); c.stroke(); }
    c.strokeStyle = 'rgba(110,117,126,0.5)'; c.lineWidth = W * 0.004; c.beginPath(); c.moveTo(W * 0.33, V(0.004)); c.quadraticCurveTo(W * 0.5, V(0.06), W * 0.67, V(0.004)); c.stroke();
  }
}

// the canvas plane of a shirt front, redrawn only when its state changes (states quantised so a held stain does not re-upload)
function shirtFace(w, h, o, wTop) {
  const res = o.res || 512, cv = document.createElement('canvas'); cv.width = res; cv.height = Math.max(8, Math.round(res * h / w)); const c = cv.getContext('2d');
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  const geo = new THREE.PlaneGeometry(w, h);
  if (wTop) { const p = geo.attributes.position; for (let i = 0; i < p.count; i++) { const v = (p.getY(i) + h / 2) / h; p.setX(i, p.getX(i) * lerp(1, wTop / w, v)); } p.needsUpdate = true; }
  // (round 1) a cool emissive under the cloth: the warm sun and grade turned the white shirt peach
  const m = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ map: tex, side: THREE.FrontSide, emissive: o.bg ? '#000000' : '#33476A', emissiveIntensity: 0.4 }));
  m.receiveShadow = true; let last = '';
  m.userData.draw = st => { const key = JSON.stringify([st.u, st.k, st.slide, st.peek, st.ext, st.wig, st.crouch].map(v => Math.round((v || 0) * 40) / 40)); if (key === last) return; last = key; drawShirt(c, cv.width, cv.height, o, st); tex.needsUpdate = true; };
  return m;
}
// the stain's state at t from the options: o.stain ('splat' | 'country' | 'none'), o.stainAt (pop in), o.stretchAt/stretchDur (splat -> country),
// o.slideAt/slideDur (up and under the pocket), o.peek (a drip left showing under the pocket once slid)
function stainState(o, t) {
  const st = { u: o.stain === 'country' ? 1 : 0, k: o.stain === 'none' ? 0 : 1, slide: o.slid ? 1 : 0, peek: o.slid ? (o.peek ?? 1) : 0, ext: 0 };
  if (o.stainAt != null) { const v = (t - o.stainAt) / 0.12; st.k = v <= 0 ? 0 : Math.min(1.12, outBack(v)); }
  if (o.stretchAt != null) { const v = (t - o.stretchAt) / (o.stretchDur ?? 0.35); st.u = clamp01(easeOut(v)); st.slide = st.slide * (1 - clamp01(v * 3)); st.peek = st.peek * (1 - clamp01(v * 3)); }
  if (o.slideAt != null) { const v = (t - o.slideAt) / (o.slideDur ?? 0.5); st.slide = smooth(v); st.peek = clamp01((v - 0.85) * 4) * (o.peek ?? 1); }
  if (o.dripAt != null) { st.ext = 0.035 * smooth((t - o.dripAt) / 0.6); }
  // (round 1) o.wigAt: a crouch and a wriggle from o.wigAt to the slide; o.peekKeys [[t, v]...]: the drip ducks in and peeks out after it
  if (o.wigAt != null && o.slideAt != null && t > o.wigAt && t < o.slideAt + 0.05) { const v = (t - o.wigAt) / Math.max(0.05, o.slideAt - o.wigAt); st.wig = Math.sin(v * 5 * PI) * (1 - 0.5 * v); st.crouch = smooth(v * 1.4) * (v < 0.95 ? 1 : 0.3); }
  if (o.peekKeys && o.slideAt != null && t > o.slideAt) { const P = o.peekKeys; let v = P[0][1]; for (let i = 0; i < P.length; i++) { if (t >= P[i][0]) v = P[i][1]; if (i + 1 < P.length && t >= P[i][0] && t < P[i + 1][0]) { const a = (t - P[i][0]) / (P[i + 1][0] - P[i][0]); v = lerp(P[i][1], P[i + 1][1], P[i + 1][1] > P[i][1] ? outBack(a) : smooth(a)); } } if (t >= P[0][0]) st.peek = Math.max(0, v); else st.peek = 0; }
  return st;
}

// the invented country's map, drawn over the country-shaped stain (same outline, same place): a pale blue acetate with a grid, the coast in
// dark blue, three towns, a title; transparent (it is a sheet you see through)
function drawMap(c, W, H, o) {
  c.clearRect(0, 0, W, H);
  const cx = o.countryAt[0], cy = o.countryAt[1], sc = (o.sc ?? 1) * (o.countrySc ?? 1);
  const x0 = (cx - 0.42 * sc) * W, x1 = (cx + 0.5 * sc) * W, y0 = cy * H - 0.2 * sc * W, y1 = cy * H + 0.3 * sc * W;
  c.fillStyle = 'rgba(150,196,236,0.34)'; c.fillRect(x0, y0, x1 - x0, y1 - y0);
  c.strokeStyle = 'rgba(40,90,150,0.45)'; c.lineWidth = Math.max(1, W * 0.003);
  for (let i = 1; i < 8; i++) { const x = lerp(x0, x1, i / 8); c.beginPath(); c.moveTo(x, y0); c.lineTo(x, y1); c.stroke(); }
  for (let i = 1; i < 5; i++) { const y = lerp(y0, y1, i / 5); c.beginPath(); c.moveTo(x0, y); c.lineTo(x1, y); c.stroke(); }
  c.strokeStyle = '#1F4E8C'; c.lineWidth = W * 0.008; c.strokeRect(x0, y0, x1 - x0, y1 - y0);
  drawStain(c, W, H, { u: 1, cx, cy, sc }, true, o.coast || '#163E78');
  c.fillStyle = '#163E78'; [[-0.12, 0.0], [0.08, -0.02], [0.2, 0.01]].forEach(([x, y], i) => { const r = W * (i ? 0.007 : 0.011); c.fillRect(cx * W + x * sc * W - r, cy * H + y * sc * W - r, 2 * r, 2 * r); });
  const title = o.mapTitle || 'CARTE OFFICIELLE'; let fs = W * 0.05; c.font = `900 ${fs}px Arial`; const tw = c.measureText(title).width, mw = (x1 - x0) * 0.8; if (tw > mw) { fs *= mw / tw; c.font = `900 ${fs}px Arial`; }
  c.fillStyle = '#163E78'; c.textAlign = 'left'; c.textBaseline = 'top'; c.fillText(title, x0 + W * 0.015, y0 + W * 0.012);
}

// bleaching: clone every material of a built prop once, then lerp its colour to white (canvas pictures go white through the emissive)
let _grain = null;
function bleachPrep(root) {
  if (!_grain) _grain = mat('#FFFFFF').map;
  const L = [];
  root.traverse(m => {
    if (!m.isMesh || m.name === 'outline' || !m.material) return;
    const one = mm => { const c = mm.clone(); L.push({ m: c, c0: c.color ? c.color.clone() : null, e0: c.emissive ? c.emissive.clone() : null, ei: c.emissiveIntensity ?? 1, pic: !!(c.map && c.map !== _grain), map0: c.map, bare: false }); return c; };
    m.material = Array.isArray(m.material) ? m.material.map(one) : one(m.material);
  });
  return L;
}
function bleachSet(L, k) {
  for (const it of L) {
    if (it.c0) it.m.color.copy(it.c0).lerp(it.pic ? WHITE : BLEACH, k);
    if (it.e0 && it.pic) { it.m.emissive.copy(it.e0).lerp(WHITE, k * 0.85); it.m.emissiveIntensity = lerp(it.ei, 1, k); }
    // (round 1) a clean white: no wood grain once bleached, and a cool blue in the shadows (a little blue emissive under the white)
    if (!it.pic) { const bare = k > 0.5; if (bare !== it.bare) { it.bare = bare; it.m.map = bare ? null : it.map0; it.m.needsUpdate = true; }
      if (it.e0) { it.m.emissive.copy(it.e0).lerp(COOL, k); it.m.emissiveIntensity = lerp(it.ei, 0.55, k); } }
  }
}
// a burst of white foam puffs (scaled spheres, never transparent): o.at, o.r, o.n
function foamPuffs(g, n, seed) {
  const ps = [];
  for (let i = 0; i < n; i++) { const m = sphere(1, '#F8FAFC', 1, { unique: true }); m.castShadow = false; m.visible = false; const a = hsh(i + seed) * TAU, e = hsh(i * 3 + seed) * 0.9;
    ps.push({ m, d: [Math.cos(a) * Math.cos(e), Math.sin(e) * 0.8 + 0.2, Math.sin(a) * Math.cos(e)], s: 0.5 + 0.6 * hsh(i * 7 + seed) }); g.add(m); }
  return (t, at, R = 1, dur = 0.7, size = 0.25) => { const u = (t - at) / dur; for (const p of ps) { p.m.visible = u > 0 && u < 1; if (!p.m.visible) continue; const e = easeOut(u), rr = R * e;
    p.m.position.set(p.d[0] * rr, p.d[1] * rr - 0.3 * u * u * R, p.d[2] * rr); p.m.scale.setScalar(Math.max(0.01, size * p.s * (u < 0.3 ? u / 0.3 : 1 - 0.85 * (u - 0.3) / 0.7))); } };
}

export const TACHE_PROPS = {
  // ---------------------------------------------------------------- worn: the hero's shirt front on his chest (attach to the 'torso' joint)
  // o.w / o.wTop / o.h: the panel (bottom width, shoulder width, height); o.stain / o.stainAt / o.slideAt...: see stainState; o.bg: the cloth
  tacheShirtFront(o) {
    const w = o.w ?? 0.34, wTop = o.wTop ?? 0.5, h = o.h ?? 0.6, g = grp();
    const lay = { stainAt: o.at || [0.34, 0.5], sc: o.sc ?? 0.95, pocket: o.pocket || [0.6, 0.83, 0.22, 0.44], bg: o.bg, collar: o.collar, countryAt: o.countryAt || [0.5, 0.62], countrySc: o.countrySc ?? 0.95, res: 512 };
    const f = shirtFace(wTop, h, lay, null); f.geometry.dispose();
    const geo = new THREE.PlaneGeometry(wTop, h); const p = geo.attributes.position; for (let i = 0; i < p.count; i++) { const v = (p.getY(i) + h / 2) / h; p.setX(i, p.getX(i) * lerp(w / wTop, 1, v)); } p.needsUpdate = true;
    f.geometry = geo; f.position.y = h / 2; g.add(f);
    g.userData.update = t => f.userData.draw(stainState(o, t));
    g.userData.update(-1); return g;
  },

  // ---------------------------------------------------------------- the shirt on its hanger (y 0: the bend of the hook, the shirt hangs below)
  // o.s: size (1: a 0.62 m wide torso); o.hanger (true); o.flat: laid on an ironing board (no hanger, sleeves along the sides); o.sway: the idle
  // sway; o.hitAt: [t...] kicks of the jet; o.mapAt / o.mapDur: the map comes down over it; o.mapPulse: the coast flashes when it matches
  tacheHangShirt(o) {
    const s = o.s ?? 1, W0 = 0.62 * s, H0 = 0.8 * s, D0 = (o.flat ? 0.01 : 0.05) * s, top = -0.13 * s, g = grp(), body = grp(); g.add(body);
    const lay = { stainAt: o.at || [0.34, 0.47], sc: o.sc ?? 1.0, pocket: o.pocket || [0.6, 0.82, 0.2, 0.42], bg: o.bg, countryAt: o.countryAt || [0.5, 0.64], countrySc: o.countrySc ?? 1.0, res: 512 };
    const cloth = o.bg || SHIRT, cm = o.bg ? {} : { noGrain: true, emissive: '#2A3A58' };
    body.add(at(box(W0 * 0.98, H0, D0, cloth, { outline: 0.004, ...cm }), 0, top - H0 / 2, 0));
    const face = shirtFace(W0, H0, lay, null); face.position.set(0, top - H0 / 2, D0 / 2 + 0.002); body.add(face);
    // collar band (the silhouette) and a back panel
    if (!o.flat) body.add(at(box(0.24 * s, 0.05 * s, D0 * 1.6, cloth, { outline: 0.004, ...cm }), 0, top + 0.01 * s, 0));
    else body.add(at(box(0.26 * s, 0.035 * s, 0.03 * s, cloth, { outline: 0.004, ...cm }), 0, top + 0.005 * s, 0.006 * s));
    const sleeves = [];
    for (const sd of [-1, 1]) {
      const sl = grp(); sl.position.set(sd * W0 * 0.47, top - 0.03 * s, 0);
      const sd0 = o.flat ? 0.014 : 0.075; sl.add(at(box(0.17 * s, 0.6 * s, sd0 * s, cloth, { pivot: 'top', outline: 0.004, ...cm }), 0, 0, 0), at(box(0.18 * s, 0.07 * s, (sd0 + 0.01) * s, cloth, { pivot: 'top', outline: 0.004, ...cm }), 0, -0.58 * s, 0));
      sl.add(at(box(0.012 * s, 0.07 * s, 0.002, '#E4E8EC'), 0, -0.62 * s, (sd0 / 2 + 0.008) * s));
      if (o.flat) sl.add(at(box(0.004 * s, 0.56 * s, 0.002, SEAM), sd * 0.05 * s, -0.02 * s, (sd0 / 2 + 0.002) * s));
      const base = o.flat ? sd * 0.28 : sd * 0.3; sl.rotation.z = base; sleeves.push({ sl, base, sd }); body.add(sl);
    }
    if (o.hanger !== false && !o.flat) {
      const hc = o.hangerColor || '#9A7650';
      g.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.045 * s, 0.008 * s, 6, 14, PI * 1.25), mat('#B8BEC6')), 0, 0.0, 0, 0, 0, -PI * 0.1));
      g.add(rod([0.045 * s, -0.005 * s, 0], [0, -0.07 * s, 0], 0.008 * s, '#B8BEC6'));
      for (const sd of [-1, 1]) g.add(rod([0, -0.08 * s, 0], [sd * W0 * 0.5, top - 0.005 * s, 0], 0.018 * s, hc));
      g.add(at(box(0.06 * s, 0.04 * s, 0.03 * s, hc), 0, -0.08 * s, 0));
    }
    // the map sheet (transparent: it is an acetate; animated inside this update, never by keys)
    let map = null;
    if (o.mapAt != null) {
      const cv = document.createElement('canvas'); cv.width = 512; cv.height = Math.round(512 * H0 / W0); drawMap(cv.getContext('2d'), cv.width, cv.height, { ...lay, mapTitle: o.mapTitle });
      const tx = new THREE.CanvasTexture(cv); tx.colorSpace = THREE.SRGBColorSpace;
      map = new THREE.Mesh(new THREE.PlaneGeometry(W0 * 1.06, H0 * 1.06), new THREE.MeshBasicMaterial({ map: tx, transparent: true, depthWrite: false, side: THREE.DoubleSide, fog: false }));
      map.renderOrder = 3; map.visible = false; g.add(map);
      const halo = new THREE.Mesh(new THREE.PlaneGeometry(W0 * 1.06, H0 * 1.06), new THREE.MeshBasicMaterial({ map: tx, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending, fog: false }));
      halo.renderOrder = 4; halo.position.z = 0.002; map.add(halo); map.userData.halo = halo;
      // (round 1) the coast alone, thick and bright, flashes twice on the match
      const cv2 = document.createElement('canvas'); cv2.width = 512; cv2.height = cv.height; const c2 = cv2.getContext('2d'); c2.clearRect(0, 0, 512, cv2.height);
      c2.shadowColor = '#FFF6B0'; c2.shadowBlur = 18; drawStain(c2, 512, cv2.height, { u: 1, cx: lay.countryAt[0], cy: lay.countryAt[1], sc: (lay.sc ?? 1) * (lay.countrySc ?? 1), lw: 0.026 }, true, '#FFE23A');
      const tx2 = new THREE.CanvasTexture(cv2); tx2.colorSpace = THREE.SRGBColorSpace;
      const coast = new THREE.Mesh(new THREE.PlaneGeometry(W0 * 1.06, H0 * 1.06), new THREE.MeshBasicMaterial({ map: tx2, transparent: true, opacity: 0, depthWrite: false, fog: false, toneMapped: false }));
      coast.renderOrder = 5; coast.position.z = 0.004; map.add(coast); map.userData.coast = coast;
    }
    const kicks = [].concat(o.hitAt ?? []);
    g.userData.update = t => {
      face.userData.draw(stainState(o, t));
      let sw = (o.sway ?? 0.025) * Math.sin(t * 2.3 + (o.phase ?? 0)), lift = 0;
      for (const k of kicks) { const u = t - k; if (u > 0) { sw += 0.22 * Math.exp(-u * 3.2) * Math.sin(u * 13); lift = Math.max(lift, 0.5 * Math.exp(-u * 4) * (u < 0.08 ? u / 0.08 : 1)); } }
      body.rotation.z = o.flat ? 0 : sw * 0.6; body.rotation.x = o.flat ? 0 : -lift * 0.35 - 0.02 * Math.sin(t * 1.7);
      for (const q of sleeves) q.sl.rotation.z = q.base + (o.flat ? 0 : q.sd * (0.04 * Math.sin(t * 3.1 + q.sd) + lift * 0.6));
      if (map) { const u = (t - o.mapAt) / (o.mapDur ?? 0.55); map.visible = u > 0; if (map.visible) { const e = easeOut(u); map.position.set(body.position.x, top - H0 / 2 + (1 - e) * H0 * 1.3, D0 / 2 + 0.02 + (1 - e) * 0.1);
        map.rotation.set(body.rotation.x, 0, body.rotation.z * 0.5 + (1 - e) * 0.15); const pu = o.mapPulse != null ? (t - o.mapPulse) / 0.5 : -1; map.userData.halo.material.opacity = pu > 0 && pu < 1 ? 0.5 * (1 - pu) : 0;
        const pc = o.mapPulse != null ? t - o.mapPulse : -1; map.userData.coast.material.opacity = pc > 0 && pc < 0.7 ? (pc < 0.15 || (pc > 0.27 && pc < 0.45) ? 1 : 0.15) : 0; } }
    };
    g.userData.update(-1); return g;
  },

  // ---------------------------------------------------------------- a chrome clothes rack (o.w wide, bar at o.h); o.shirt: a tacheHangShirt on it
  tacheRack(o) {
    const w = o.w ?? 1.0, h = o.h ?? 1.95, g = grp(), C = o.color || CHROME;
    for (const sd of [-1, 1]) { g.add(at(cyl(0.022, 0.022, h, C, 8, { pivot: 'bottom', outline: 0.004 }), sd * w / 2, 0.06, 0), at(box(0.06, 0.03, 0.5, C, { outline: 0.004 }), sd * w / 2, 0.075, 0));
      for (const dz of [-0.23, 0.23]) g.add(at(cyl(0.035, 0.035, 0.03, INK, 10), sd * w / 2, 0.035, dz, 0, 0, PI / 2)); }
    g.add(at(cyl(0.022, 0.022, w + 0.06, C, 8, { outline: 0.004 }), 0, h + 0.06, 0, 0, 0, PI / 2));
    let sh = null; if (o.shirt) { sh = TACHE_PROPS.tacheHangShirt(o.shirt); sh.position.set(o.shirtX ?? 0, h + 0.06, 0); g.add(sh); }
    g.userData.update = t => { if (sh) sh.userData.update(t); };
    return g;
  },

  // ---------------------------------------------------------------- a yellow sponge with a green scouring side; o.breakAt: it falls apart
  // (six chunks fly out and drop with the world's gravity, wherever the hand points)
  tacheSponge(o) {
    const s = o.s ?? 1, g = grp(), ch = [], W = 0.16 * s, Hh = 0.07 * s, D = 0.11 * s;
    for (let i = 0; i < 6; i++) { const ix = i % 3, iz = Math.floor(i / 3), cw = W / 3, cd = D / 2, p = grp();
      p.add(at(box(cw * 0.98, Hh * 0.75, cd * 0.98, '#F2CF48', { outline: 0.003 }), 0, -Hh * 0.125, 0), at(box(cw * 0.98, Hh * 0.25, cd * 0.98, '#3E8E4A'), 0, Hh * 0.375, 0));
      p.position.set((ix - 1) * cw, 0, (iz - 0.5) * cd); ch.push({ p, p0: p.position.clone(), v: new THREE.Vector3((ix - 1) * 0.6 + (hsh(i) - 0.5) * 0.5, 0.3 + hsh(i + 4) * 0.5, (iz - 0.5) * 0.8), sp: [(hsh(i + 9) - 0.5) * 14, (hsh(i + 2) - 0.5) * 14] }); g.add(p); }
    const q = new THREE.Quaternion(), down = new THREE.Vector3(), HANG = o.hang ?? 0.22, BURST = 0.07;
    // (round 1) o.strokes [[t, d]...]: each scrub squashes the sponge flat (d 1) or stretches it long (d -1), with a quick wobble back; it swells just
    // before it bursts; the chunks fly out fast, hang in the air (o.hang s, drifting and turning slowly), then drop
    const strokes = (o.strokes || []).slice().sort((a, b) => a[0] - b[0]);
    g.userData.update = t => {
      const u = o.breakAt == null ? -1 : t - o.breakAt;
      if (u <= 0) { ch.forEach(c => { c.p.position.copy(c.p0); c.p.rotation.set(0, 0, 0); c.p.visible = true; });
        let sx = 1, sy = 1; for (const [ts, d] of strokes) { if (ts > t) break; const v = t - ts, a = Math.exp(-v * 14) * Math.cos(v * 30); sx = 1 + 0.45 * d * a; sy = 1 - 0.42 * d * a; }
        if (u > -0.08 && o.breakAt != null) { const b = 1 + 0.35 * smooth((u + 0.08) / 0.08); sx = b; sy = b; }
        g.scale.set(sx, sy, sx); return; }
      g.scale.setScalar(1);
      g.updateWorldMatrix(true, false); g.getWorldQuaternion(q); q.invert(); const sc = new THREE.Vector3(); g.getWorldScale(sc);
      down.set(0, -1, 0).applyQuaternion(q).multiplyScalar(1 / Math.max(0.01, sc.x));
      const ub = Math.min(u, BURST) / BURST, uh = clamp01((u - BURST) / HANG), uf = Math.max(0, u - BURST - HANG);
      const fly = 0.22 * easeOut(ub) + 0.03 * uh + 0.6 * uf;
      ch.forEach(c => { c.p.position.copy(c.p0).addScaledVector(c.v, fly * 1.6).addScaledVector(down, 4.9 * uf * uf + 0.004 * Math.sin(uh * PI)); const sp = 0.12 * ub + 0.05 * uh + uf; c.p.rotation.set(c.sp[0] * sp, 0, c.sp[1] * sp); c.p.visible = u < 1.6; });
    };
    g.userData.update(-1); return g;
  },

  // ---------------------------------------------------------------- the kitchen: a plate of spaghetti with tomato sauce, a fork with a twirl, a glob
  tachePastaPlate(o) {
    const s = o.s ?? 1, g = grp();
    g.add(at(cyl(0.2 * s, 0.17 * s, 0.025 * s, '#F4F3EE', 18, { pivot: 'bottom', outline: 0.004 }), 0, 0, 0), at(cyl(0.13 * s, 0.13 * s, 0.006 * s, '#E6E4DC', 18), 0, 0.026 * s, 0));
    for (let i = 0; i < 9; i++) { const tr = new THREE.Mesh(new THREE.TorusGeometry((0.04 + 0.05 * hsh(i)) * s, 0.006 * s, 4, 16), mat(PASTA)); tr.rotation.set(PI / 2 + (hsh(i + 3) - 0.5) * 0.8, 0, hsh(i + 5) * 3); tr.position.set((hsh(i + 7) - 0.5) * 0.08 * s, (0.04 + 0.015 * hsh(i + 1)) * s, (hsh(i + 8) - 0.5) * 0.06 * s); g.add(tr); }
    for (const [x, z, r] of [[0.0, 0.0, 0.05], [0.035, 0.02, 0.035], [-0.03, 0.015, 0.03]]) { const m = sphere(r * s, STAIN, 1); m.scale.y = 0.45; m.position.set(x * s, 0.06 * s, z * s); g.add(m); }
    return g;
  },
  tacheFork(o) {
    const s = o.s ?? 1.5, g = grp(), f = buildProp('fork', {}); f.scale.setScalar(s); g.add(f);
    const tw = grp(); tw.position.y = 0.19 * s; g.add(tw);
    for (let i = 0; i < 4; i++) { const tr = new THREE.Mesh(new THREE.TorusGeometry(0.022 * s, 0.006 * s, 4, 14), mat(PASTA)); tr.rotation.set(PI / 2, 0, i); tr.position.y = (i - 1.5) * 0.008 * s; tw.add(tr); }
    const sc = sphere(0.016 * s, STAIN, 1); sc.position.set(0.01 * s, 0.012 * s, 0.012 * s); tw.add(sc);
    g.userData.update = t => { tw.visible = !(o.emptyAt != null && t >= o.emptyAt); };
    g.userData.update(-1); return g;
  },
  tachePastaGlob(o) {
    const s = o.s ?? 1, g = grp();
    for (let i = 0; i < 3; i++) { const tr = new THREE.Mesh(new THREE.TorusGeometry(0.03 * s, 0.008 * s, 4, 12), mat(PASTA)); tr.rotation.set(hsh(i) * 3, hsh(i + 1) * 3, 0); g.add(tr); }
    g.add(at(sphere(0.026 * s, STAIN, 1), 0.01 * s, 0.01 * s, 0.01 * s), at(sphere(0.018 * s, STAIN_D, 1), -0.015 * s, -0.005 * s, 0.015 * s));
    return g;
  },

  // ---------------------------------------------------------------- the court: the eviction order (facing +Z), stamped EXPULSÉE at o.stampAt
  tacheEvictOrder(o) {
    const w = o.w ?? 0.62, h = o.h ?? 0.82, g = grp();
    const sheet = canvasPlane(w, h, (c, W, H) => {
      c.fillStyle = '#FBF8EE'; c.fillRect(0, 0, W, H); c.strokeStyle = '#2C3E5C'; c.lineWidth = W * 0.012; c.strokeRect(W * 0.04, W * 0.04, W * 0.92, H - W * 0.08);
      const fit = (txt, y, size, wmax, col) => { let fs = size; c.font = `900 ${fs}px Arial`; const tw = c.measureText(txt).width; if (tw > wmax) { fs *= wmax / tw; c.font = `900 ${fs}px Arial`; } c.fillStyle = col; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(txt, W / 2, y); };
      fit('TRIBUNAL', H * 0.1, W * 0.07, W * 0.6, '#2C3E5C'); fit("ORDRE D'EXPULSION", H * 0.2, W * 0.1, W * 0.84, INK);
      c.fillStyle = '#9AA3AE'; for (let i = 0; i < 6; i++) c.fillRect(W * 0.12, H * (0.34 + i * 0.07), W * (i === 5 ? 0.45 : 0.76), H * 0.014);
      fit('LA TACHE', H * 0.3, W * 0.075, W * 0.6, STAIN_D);
      c.strokeStyle = INK; c.lineWidth = W * 0.008; c.beginPath(); c.moveTo(W * 0.58, H * 0.86); c.bezierCurveTo(W * 0.66, H * 0.8, W * 0.7, H * 0.92, W * 0.78, H * 0.84); c.lineTo(W * 0.88, H * 0.87); c.stroke();
    }, { res: 512 });
    sheet.position.y = h / 2; g.add(sheet);
    const mark = canvasPlane(w * 0.8, w * 0.3, (c, W, H) => { c.fillStyle = '#FBF8EE'; c.fillRect(0, 0, W, H); const col = '#C8202A'; c.strokeStyle = col; c.lineWidth = H * 0.09; c.strokeRect(H * 0.08, H * 0.08, W - H * 0.16, H - H * 0.16);
      let fs = H * 0.56; c.font = `900 ${fs}px Arial`; const tw = c.measureText('EXPULSÉE').width; if (tw > W * 0.84) { fs *= W * 0.84 / tw; c.font = `900 ${fs}px Arial`; } c.fillStyle = col; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('EXPULSÉE', W / 2, H * 0.54); }, { res: 512 });
    mark.position.set(0.0, h * 0.5, 0.004); mark.rotation.z = 0.18; g.add(mark);
    // the stamp itself comes down onto the sheet and lifts away
    const stamp = grp(at(box(w * 0.5, 0.05, 0.12, '#2A2A2E', { outline: 0.004 }), 0, 0, 0), at(cyl(0.035, 0.05, 0.16, '#5A3A28', 8, { pivot: 'bottom' }), 0, 0.025, 0), at(sphere(0.06, '#C23A2E', 1), 0, 0.2, 0));
    stamp.rotation.x = PI / 2; g.add(stamp);
    g.userData.update = t => {
      const u = o.stampAt == null ? 9 : t - o.stampAt;
      mark.visible = u >= 0; if (u >= 0) { const k = u < 0.08 ? 1.35 - 4.4 * u : 1.0; mark.scale.setScalar(Math.max(1, k)); }
      const zz = u < -0.15 ? 0.9 : u < 0 ? lerp(0.9, 0.035, smooth((u + 0.15) / 0.15)) : u < 0.12 ? 0.035 : lerp(0.035, 1.2, easeOut((u - 0.12) / 0.3));
      stamp.position.set(0, h * 0.5, zz); stamp.children.forEach(c => { c.visible = u > -0.35 && u < 0.16; });
    };
    g.userData.update(-1); return g;
  },

  // ---------------------------------------------------------------- the riot police's round shield (facing +Z): see-through, a dark rim
  tacheRoundShield(o) {
    const R = o.r ?? 0.42, g = grp();
    const pane = new THREE.Mesh(new THREE.CircleGeometry(R, 28), new THREE.MeshLambertMaterial({ color: '#BFD6E4', transparent: true, opacity: 0.5, side: THREE.DoubleSide, depthWrite: false }));
    pane.castShadow = false; g.add(pane);
    g.add(new THREE.Mesh(new THREE.TorusGeometry(R, 0.018, 6, 32), mat('#2A2F36')));
    g.add(at(new THREE.Mesh(new THREE.TorusGeometry(R * 0.55, 0.006, 4, 28), mat('#7F95A6')), 0, 0, 0.002));
    g.add(at(box(0.04, 0.16, 0.05, '#2A2F36'), 0, 0, -0.04));
    return g;
  },

  // ---------------------------------------------------------------- the tank (front +Z, no markings) with a giant stain-remover spray bottle
  // strapped to its barrel; o.fireAt: recoil (hull rocks back, the barrel slides), dust at the tracks, a foam puff at the nozzle.
  // userData.muzzle: the nozzle's tip in the prop's frame
  tacheTank(o) {
    const g = grp(), hull = grp(), col = o.color || '#6E7652', dk = '#3A3D30', tr = '#2E302A'; g.add(hull);
    hull.add(at(box(2.5, 0.85, 5.2, col, { outline: 0.012 }), 0, 0.95, 0), at(box(2.5, 0.5, 1.0, col, { outline: 0.01, taper: { x: 1, z: 0.4 } }), 0, 0.98, 2.95));
    for (const sd of [-1, 1]) { hull.add(at(box(0.62, 0.95, 6.0, tr, { outline: 0.01 }), sd * 1.5, 0.5, 0), at(box(0.7, 0.08, 5.4, col, { outline: 0.006 }), sd * 1.5, 1.0, 0));
      for (let i = 0; i < 6; i++) hull.add(at(cyl(0.36, 0.36, 0.66, '#4A4D40', 12, { outline: 0.005 }), sd * 1.5, 0.42, -2.3 + i * 0.92, 0, 0, PI / 2)); }
    const tur = grp(); tur.position.set(0, 1.38, -0.4); hull.add(tur);
    tur.add(at(box(1.9, 0.72, 2.5, col, { pivot: 'bottom', outline: 0.012, taper: { x: 0.82, z: 0.85 } }), 0, 0, 0), at(box(0.7, 0.55, 0.4, dk, { outline: 0.008 }), 0, 0.36, 1.25));
    tur.add(at(cyl(0.22, 0.22, 0.18, dk, 10, { outline: 0.006 }), 0.45, 0.8, -0.4));
    const gun = grp(); gun.position.set(0, 0.38, 1.4); tur.add(gun);
    const BL = 3.6; gun.add(at(cyl(0.11, 0.13, BL, col, 10, { outline: 0.008 }), 0, 0, BL / 2, PI / 2, 0, 0), at(cyl(0.16, 0.16, 0.4, dk, 10, { outline: 0.006 }), 0, 0, BL - 0.1, PI / 2, 0, 0));
    // the spray bottle: white body along the barrel, a blue label band with its word, the trigger head and nozzle at the muzzle
    const bot = grp(); bot.position.set(0, 0.42, BL - 1.15); gun.add(bot);
    bot.add(at(box(0.62, 0.62, 1.3, '#F2F5F7', { outline: 0.008 }), 0, 0, 0), at(box(0.64, 0.4, 0.8, '#2F8FD0', { outline: 0.004 }), 0, 0, 0.0));
    for (const sd of [-1, 1]) { const lb = canvasPlane(0.78, 0.34, (c, W, H) => { c.fillStyle = '#2F8FD0'; c.fillRect(0, 0, W, H); let fs = H * 0.5; c.font = `900 ${fs}px Arial`; const tw = c.measureText('DÉTACHANT').width; if (tw > W * 0.9) { fs *= W * 0.9 / tw; c.font = `900 ${fs}px Arial`; } c.fillStyle = '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('DÉTACHANT', W / 2, H * 0.55); }, { res: 256 });
      lb.position.set(sd * 0.325, 0, 0); lb.rotation.y = sd * PI / 2; bot.add(lb); }
    bot.add(at(box(0.62, 0.4, 0.32, '#F2F5F7', { outline: 0.006 }), 0, 0.05, 0.8), at(box(0.42, 0.46, 0.36, '#E8EDF0', { outline: 0.006, taper: { x: 0.8, z: 0.7 } }), 0, 0.12, 1.1));
    bot.add(at(box(0.12, 0.34, 0.14, '#2F8FD0', { outline: 0.004 }), 0, -0.2, 1.05, -0.4, 0, 0), at(cyl(0.06, 0.07, 0.32, '#2F8FD0', 8, { outline: 0.004 }), 0, 0.2, 1.36, PI / 2, 0, 0));
    for (const dz of [-0.35, 0.35]) bot.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.44, 0.035, 6, 18), mat('#2B2B26')), 0, -0.2, dz));
    const muzzleLocal = [0, 1.38 + 0.38 + 0.42 + 0.2, -0.4 + 1.4 + BL - 1.15 + 1.52];
    const dust = foamPuffs(g, 14, 3), puff = grp(); puff.position.set(...muzzleLocal); g.add(puff); const foam = foamPuffs(puff, 10, 11);
    g.traverse(m => { if (m.isMesh && m.material && m.material.color && m.parent === g && m.geometry.type === 'IcosahedronGeometry') m.material.color.set('#CDBFA2'); });
    g.userData.muzzle = muzzleLocal;
    g.userData.update = t => {
      const u = o.fireAt == null ? -1 : t - o.fireAt;
      const rk = u > 0 ? Math.exp(-u * 4.5) * Math.sin(u * 16) : 0, bk = u > 0 ? (u < 0.05 ? u / 0.05 : Math.exp(-(u - 0.05) * 5)) : 0;
      hull.rotation.x = -0.05 * rk - 0.03 * bk; hull.position.z = -0.25 * bk; gun.position.z = 1.4 - 0.4 * bk;
      dust(t, o.fireAt ?? 99, 3.4, 0.9, 0.3); foam(t, o.fireAt ?? 99, 0.9, 0.5, 0.3);
    };
    g.userData.update(-1); return g;
  },

  // ---------------------------------------------------------------- the thick white jet of stain remover: from the prop's origin to a target that
  // can move (o.hits: [[t, [x, y, z]] ...] in the prop's frame); it grows at o.v m/s from o.fireAt, sags (o.sag), widens toward its end, and a
  // spray of foam boils at the end; o.stopAt: the tail leaves the nozzle and the jet runs out
  tacheJet(o) {
    const g = grp(), N = o.n ?? 30, R = o.r ?? 0.28, segs = [], geo = new THREE.CylinderGeometry(1, 1, 1, 9, 1, true);
    const jm = new THREE.MeshLambertMaterial({ color: '#F6F9FB', emissive: '#A9BDCB', emissiveIntensity: 0.35, side: THREE.DoubleSide });
    for (let i = 0; i < N; i++) { const m = new THREE.Mesh(geo, jm); m.castShadow = false; m.visible = false; segs.push(m); g.add(m); }
    const blobs = []; for (let i = 0; i < 14; i++) { const m = sphere(1, '#F8FBFD', 1, { unique: true }); m.castShadow = false; m.visible = false; blobs.push(m); g.add(m); }
    const end = grp(); g.add(end); const glow = glowSprite('#FFFFFF', (o.mist ?? 3.0), 0.55); end.add(glow);
    const hits = (o.hits || [[0, [0, 0, 20]]]).map(([t, p]) => [t, new THREE.Vector3(...p)]);
    const target = t => { if (t <= hits[0][0]) return hits[0][1].clone(); for (let i = 1; i < hits.length; i++) if (t <= hits[i][0]) { const [a, pa] = hits[i - 1], [b, pb] = hits[i]; return pa.clone().lerp(pb, smooth((t - a) / (b - a))); } return hits[hits.length - 1][1].clone(); };
    const Y = new THREE.Vector3(0, 1, 0), A = new THREE.Vector3(), B = new THREE.Vector3(), D = new THREE.Vector3();
    const pt = (T, s, out) => { const L = T.length(); out.copy(T).multiplyScalar(s); out.y -= (o.sag ?? 0.06) * L * s * (1 - s) * 4 * 0.25; return out; };
    g.userData.update = t => {
      const u = o.fireAt == null ? -1 : t - o.fireAt, on = u > 0;
      glow.visible = on; segs.forEach(m => { m.visible = false; }); blobs.forEach(m => { m.visible = false; }); if (!on) return;
      const T = target(t), L = T.length(), grown = Math.min(1, (o.v ?? 60) * u / Math.max(0.1, L)), tail = o.stopAt != null && t > o.stopAt ? Math.min(1, (o.v ?? 60) * (t - o.stopAt) / Math.max(0.1, L)) : 0;
      for (let i = 0; i < N; i++) { const s0 = i / N, s1 = (i + 1) / N; if (s1 > grown || s0 < tail) continue; pt(T, s0, A); pt(T, s1, B); D.subVectors(B, A); const len = D.length();
        const r = R * lerp(0.55, 1.25, s0) * (1 + 0.08 * Math.sin(t * 40 + i * 1.7)); const m = segs[i]; m.visible = true; m.position.copy(A).addScaledVector(D, 0.5); m.scale.set(r, len * 1.04, r); m.quaternion.setFromUnitVectors(Y, D.normalize()); }
      pt(T, grown, A); end.position.copy(A); glow.material.opacity = 0.55 * (1 - tail);
      blobs.forEach((m, i) => { if (tail >= 1) return; const ph = (t * (2.2 + hsh(i)) + hsh(i + 3)) % 1, rr = R * (1.2 + 3.2 * ph); m.visible = true;
        m.position.set(A.x + Math.cos(i * 2.4) * rr * 0.8, A.y + Math.sin(i * 1.7) * rr * 0.6 + ph * R, A.z + Math.sin(i * 2.4) * rr * 0.8); m.scale.setScalar(R * (0.9 - 0.6 * ph) * (o.splash ?? 1)); });
    };
    g.userData.update(-1); return g;
  },

  // ---------------------------------------------------------------- any prop of the engine, bleached white at o.at (over o.dur), with a puff of foam
  // o.prop: its name, o.popts: its options; o.at -1: white from the start (the white neighbourhood)
  tacheBleach(o) {
    const g = grp(), inner = buildProp(o.prop || 'cottage', o.popts || {}); g.add(inner);
    const L = bleachPrep(inner), puffs = grp(); puffs.position.set(...(o.puffAt || [0, 1.5, 0])); g.add(puffs); const pf = foamPuffs(puffs, o.puffN ?? 12, 5 + (o.seed ?? 0));
    g.userData.update = t => { if (inner.userData.update) inner.userData.update(t); const at0 = o.at ?? 99; bleachSet(L, at0 < 0 ? 1 : clamp01((t - at0) / (o.dur ?? 0.16)));
      if (at0 >= 0 && o.puff !== false) pf(t, at0 - 0.04, o.puffR ?? 2.2, 0.7, o.puffS ?? 0.7); };
    g.userData.update(-1); return g;
  },
  // the neighbourhood's ground, painted over the field without a depth test (renderOrder -1.5, markings -1.2): o.rects [[x, z, w, d, color, ro]],
  // cut into strips o.strip long along z that go white as the jet passes: t = o.t0 + (o.z0 - z) / o.v (o.at -1: white from the start)
  tacheGround(o) {
    const g = grp(), Y = o.y ?? 0.06, sl = o.strip ?? 4, items = [];
    for (const [x, z, w, d, col, ro] of o.rects || []) {
      const n = Math.max(1, Math.round(d / sl));
      for (let i = 0; i < n; i++) { const dz = d / n, zc = z - d / 2 + dz * (i + 0.5);
        const m = new THREE.Mesh(new THREE.PlaneGeometry(w, dz * 1.002), new THREE.MeshLambertMaterial({ color: col, depthTest: false, depthWrite: false })); m.material.userData.ro = ro ?? -1.5;
        m.rotation.x = -PI / 2; m.position.set(x, Y + (ro === -1.2 ? 0.004 : 0), zc); m.renderOrder = ro ?? -1.5; m.receiveShadow = true; g.add(m); items.push({ m, c0: new THREE.Color(col), z: zc }); }
    }
    g.userData.update = t => { for (const it of items) { const a = o.at != null ? o.at : (o.t0 ?? 99) + ((o.z0 ?? 0) - it.z) / (o.v ?? 30); const k = a < 0 ? 1 : clamp01((t - a) / 0.16); it.m.material.color.copy(it.c0).lerp(BLEACH, k); } };
    g.userData.update(-1); return g;
  },

  // ---------------------------------------------------------------- forensic tape round a rectangle (o.w x o.d, posts at the corners), run out post
  // to post between o.runAt[0] and o.runAt[1]
  tacheTape(o) {
    const w = (o.w ?? 2.4) / 2, d = (o.d ?? 2.0) / 2, Hh = o.h ?? 1.0, g = grp(), C = [[-w, d], [-w, -d], [w, -d], [w, d]], segs = [];
    for (const [x, z] of C) { g.add(at(cyl(0.035, 0.045, Hh + 0.1, '#F4F1E8', 8, { pivot: 'bottom', outline: 0.004 }), x, 0, z), at(box(0.22, 0.05, 0.22, '#3A3D44', { outline: 0.003 }), x, 0.025, z));
      for (let i = 0; i < 2; i++) g.add(at(cyl(0.047, 0.047, 0.1, '#C8202A', 8), x, 0.35 + i * 0.35, z)); }
    const order = o.open ? [0, 1, 2, 3] : [0, 1, 2, 3, 0];
    for (let i = 0; i + 1 < order.length; i++) {
      const [x1, z1] = C[order[i]], [x2, z2] = C[order[i + 1]], L = Math.hypot(x2 - x1, z2 - z1);
      const tp = canvasPlane(L, 0.09, (c, W, H) => { c.fillStyle = '#F2D21E'; c.fillRect(0, 0, W, H); c.fillStyle = INK; const txt = 'NE PAS FRANCHIR'; c.font = `900 ${H * 0.62}px Arial`; c.textBaseline = 'middle'; const tw = c.measureText(txt).width + H * 1.2; for (let x = H * 0.4; x < W; x += tw) c.fillText(txt, x, H * 0.55); }, { res: 1024 });
      const pv = grp(); pv.position.set(x1, Hh, z1); pv.rotation.y = Math.atan2(-(z2 - z1), x2 - x1); tp.position.x = L / 2; pv.add(tp); g.add(pv); segs.push({ pv, tp });
    }
    g.userData.update = t => { const [a, b] = o.runAt || [-1, -0.5], n = segs.length; segs.forEach((s, i) => { const k = clamp01(((t - a) / (b - a)) * n - i); s.pv.scale.x = Math.max(0.001, k); s.tp.visible = k > 0.001; s.pv.rotation.z = 0.02 * Math.sin(t * 5 + i); }); };
    g.userData.update(-1); return g;
  },

  // ---------------------------------------------------------------- the president's sign: a washing machine crossed out (held up on a stick)
  tacheNoWashSign(o) {
    const w = o.w ?? 0.62, g = grp();
    const pic = canvasPlane(w, w * 1.18, (c, W, H) => {
      c.fillStyle = '#FBFAF6'; c.fillRect(0, 0, W, H); c.strokeStyle = '#2C3E5C'; c.lineWidth = W * 0.03; c.strokeRect(W * 0.02, W * 0.02, W * 0.96, H - W * 0.04);
      const cx = W / 2, cy = W * 0.5, s = W * 0.27;
      c.fillStyle = '#E6EAEE'; c.strokeStyle = INK; c.lineWidth = W * 0.025; c.fillRect(cx - s, cy - s * 1.1, 2 * s, 2.2 * s); c.strokeRect(cx - s, cy - s * 1.1, 2 * s, 2.2 * s);
      c.beginPath(); c.moveTo(cx - s, cy - s * 0.65); c.lineTo(cx + s, cy - s * 0.65); c.stroke(); c.fillStyle = '#8FC6E8'; c.beginPath(); c.arc(cx, cy + s * 0.25, s * 0.6, 0, TAU); c.fill(); c.stroke();
      c.beginPath(); c.arc(cx - s * 0.6, cy - s * 0.88, s * 0.1, 0, TAU); c.stroke();
      c.strokeStyle = '#D0202A'; c.lineWidth = W * 0.07; c.beginPath(); c.arc(cx, cy, W * 0.4, 0, TAU); c.stroke(); c.beginPath(); c.moveTo(cx - W * 0.28, cy - W * 0.28); c.lineTo(cx + W * 0.28, cy + W * 0.28); c.stroke();
      let fs = W * 0.12; c.font = `900 ${fs}px Arial`; const t1 = 'INTERDIT', tw = c.measureText(t1).width; if (tw > W * 0.86) { fs *= W * 0.86 / tw; c.font = `900 ${fs}px Arial`; } c.fillStyle = '#D0202A'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(t1, W / 2, H * 0.9);
    }, { res: 512 });
    pic.position.y = w * 0.59 + (o.stick ?? 0.3); g.add(pic);
    g.add(at(box(w + 0.03, w * 1.18 + 0.03, 0.02, '#2C3E5C'), 0, pic.position.y, -0.012));
    if (o.stick !== 0) g.add(at(cyl(0.015, 0.015, (o.stick ?? 0.3) + 0.15, '#8A6A48', 6, { pivot: 'bottom' }), 0, 0, -0.03));
    return g;
  },
  // the decree on the podium (lying flat, facing up): DÉCRET, lines, a signature that writes itself from o.signAt
  tacheDecree(o) {
    const w = o.w ?? 0.34, h = o.h ?? 0.46, cv = document.createElement('canvas'); cv.width = 256; cv.height = Math.round(256 * h / w); const c = cv.getContext('2d');
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; let last = -1;
    const draw = p => { const W = cv.width, H = cv.height; c.fillStyle = '#FBF8EE'; c.fillRect(0, 0, W, H); c.fillStyle = INK; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${W * 0.16}px Arial`; c.fillText('DÉCRET', W / 2, H * 0.12);
      c.fillStyle = '#9AA3AE'; for (let i = 0; i < 6; i++) c.fillRect(W * 0.12, H * (0.26 + i * 0.08), W * 0.76, H * 0.016);
      c.strokeStyle = '#1C2E66'; c.lineWidth = W * 0.02; c.beginPath(); const n = Math.floor(p * 30); for (let i = 0; i <= n; i++) { const s = i / 30, x = W * (0.45 + 0.4 * s), y = H * (0.85 + 0.04 * Math.sin(s * 19)); if (i) c.lineTo(x, y); else c.moveTo(x, y); } c.stroke(); tex.needsUpdate = true; };
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshLambertMaterial({ map: tex })); m.rotation.x = -PI / 2; m.position.y = 0.004; const g = grp(m);
    g.userData.update = t => { const p = o.signAt == null ? 1 : clamp01((t - o.signAt) / (o.signDur ?? 0.6)), q = Math.round(p * 10); if (q !== last) { last = q; draw(q / 10); } };
    g.userData.update(-1); return g;
  },

  // ---------------------------------------------------------------- the palace roof (floor top at y 0): a stone terrace with a balustrade along the
  // back and the sides, the zinc roof of the palace behind, and, o.skyline, the town's roofs below all round (the terrace stands o.lift above them)
  tachePalaceRoof(o) {
    const w = o.w ?? 14, d = o.d ?? 10, lift = o.lift ?? 8, g = grp(), st = o.stone || '#E4D9C4', dk = '#CDBFA4';
    g.add(at(box(w, 0.3, d, st, { outline: 0.01 }), 0, -0.15, 0), at(box(w + 0.6, lift, d + 0.6, '#E9DFCB', { pivot: 'top', outline: 0.02 }), 0, -0.3, 0));
    for (let i = 1; i < 10; i++) g.add(at(box(w, 0.006, 0.02, dk), 0, 0.003, -d / 2 + i * d / 10));
    const bal = (x0, z0, x1, z1) => { const L = Math.hypot(x1 - x0, z1 - z0), a = Math.atan2(-(z1 - z0), x1 - x0), b = grp(); b.position.set(x0, 0, z0); b.rotation.y = a;
      b.add(at(box(L, 0.14, 0.32, st, { outline: 0.006 }), L / 2, 1.08, 0), at(box(L, 0.12, 0.3, dk, { outline: 0.005 }), L / 2, 0.06, 0));
      const n = Math.floor(L / 0.32); for (let i = 0; i < n; i++) b.add(at(cyl(0.055, 0.075, 0.9, st, 7, { pivot: 'bottom' }), (i + 0.5) * L / n, 0.12, 0));
      for (let i = 0; i <= Math.floor(L / 3); i++) b.add(at(box(0.4, 1.22, 0.4, dk, { pivot: 'bottom', outline: 0.006 }), Math.min(L, i * 3), 0, 0)); g.add(b); };
    bal(-w / 2, -d / 2, w / 2, -d / 2); if (o.sides !== false) { bal(-w / 2, d / 2, -w / 2, -d / 2); bal(w / 2, -d / 2, w / 2, d / 2); }
    if (o.front) bal(w / 2, d / 2, -w / 2, d / 2);
    if (o.zinc !== false) { const zb = grp(); zb.position.set(o.zincX ?? 0, 0, -d / 2 - 4.5); g.add(zb);
      zb.add(at(box(w * 0.9, 1.8, 6, '#E9DFCB', { pivot: 'bottom', outline: 0.01 }), 0, -0.4, 0), at(box(w * 0.9, 2.6, 6, '#5E6E80', { pivot: 'bottom', outline: 0.012, taper: { x: 0.82, z: 0.45 } }), 0, 1.4, 0));
      zb.add(at(sphere(1.6, '#6E7E90', 1), 0, 4.0, 0), at(cyl(0.3, 0.3, 1.2, '#E2B53C', 8, { pivot: 'bottom' }), 0, 5.4, 0));
      for (const x of [-4, -1.5, 1.5, 4]) zb.add(at(box(0.7, 0.9, 0.5, '#E9DFCB', { pivot: 'bottom', outline: 0.006 }), x, 2.2, 2.4), at(box(0.5, 0.5, 0.05, '#2E3A48'), x, 2.45, 2.66)); }
    if (o.skyline !== false) { for (let i = 0; i < 44; i++) { const a = hsh(i) * TAU, rr = 18 + 30 * hsh(i + 5), bw = 6 + 6 * hsh(i + 2), bh = lift - 2.5 - 3 * hsh(i + 7), x = Math.cos(a) * rr, z = Math.sin(a) * rr;
        if (z > 0 && Math.abs(x) < 12) continue;
        const b = grp(); b.position.set(x, -lift, z); b.rotation.y = hsh(i + 9) * PI; b.add(at(box(bw, bh, bw * 0.7, ['#E8DCC6', '#EFE5D3', '#E0D2BA'][i % 3], { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(bw, 2.2, bw * 0.7, '#5E6C7C', { pivot: 'bottom', taper: { x: 0.8, z: 0.4 }, outline: 0.01 }), 0, bh, 0));
        b.add(at(box(0.5, 1.2, 0.5, '#B86A4A', { pivot: 'bottom' }), bw * 0.3, bh + 0.8, 0)); g.add(b); } }
    return g;
  },
  // ---------------------------------------------------------------- the flagpole of the palace (no crossbar: a gold ball on top) hoisting the shirt on
  // its hanger in front of the pole (it reads as a shirt): o.h, o.hoistAt / o.hoistDur, o.y0 / o.y1 (the hook's height), o.shirt (its options)
  tachePole(o) {
    const H = o.h ?? 7.5, g = grp();
    g.add(at(box(0.7, 0.35, 0.7, '#CDBFA4', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(cyl(0.06, 0.085, H, '#F1EFEA', 10, { pivot: 'bottom', outline: 0.006 }), 0, 0.35, 0), at(sphere(0.16, '#E2B53C', 1), 0, H + 0.45, 0));
    g.add(at(cyl(0.09, 0.09, 0.08, '#B8BEC6', 10), 0, H + 0.25, 0));
    for (const dx of [0.07, -0.02]) g.add(rod([dx, H + 0.25, 0.1], [dx, 1.3, 0.1], 0.008, '#3A3530'));
    g.add(at(box(0.04, 0.16, 0.05, '#B8BEC6'), 0.0, 1.25, 0.09));
    const sh = TACHE_PROPS.tacheHangShirt({ ...(o.shirt || {}), s: o.shirt?.s ?? 1.3 }); sh.position.z = 0.13; g.add(sh);
    const y0 = o.y0 ?? 1.6, y1 = o.y1 ?? H - 0.1;
    g.userData.update = t => { const u = o.hoistAt == null ? 1 : smooth((t - o.hoistAt) / (o.hoistDur ?? 1.2)); sh.position.y = lerp(y0, y1, u) + 0.03 * Math.sin(t * 6) * (u > 0 && u < 1 ? 1 : 0); sh.userData.update(t); };
    g.userData.update(-1); return g;
  },
  // a folded bundle of old cloth (faded beige and grey, never unfolded)
  tacheBundle(o) {
    const s = o.s ?? 1, g = grp(), cols = ['#B9AE98', '#A69C88', '#BDB4A2', '#9E9482'];
    for (let i = 0; i < 4; i++) g.add(at(box(0.5 * s, 0.07 * s, 0.34 * s, cols[i], { outline: 0.004 }), (hsh(i) - 0.5) * 0.02, i * 0.07 * s, (hsh(i + 1) - 0.5) * 0.02, 0, (hsh(i + 2) - 0.5) * 0.1, 0));
    g.add(at(box(0.5 * s, 0.02, 0.08 * s, '#8A806C'), 0, 0.29 * s, 0.13 * s));
    return g;
  },

  // ---------------------------------------------------------------- the upkeep: a steam iron (soleplate down, point toward +Z) and an ironing board
  tacheIron(o) {
    const s = o.s ?? 1, g = grp();
    const sh = new THREE.Shape(); sh.moveTo(-0.07, 0.1); sh.lineTo(0.07, 0.1); sh.quadraticCurveTo(0.075, -0.03, 0.0, -0.14); sh.quadraticCurveTo(-0.075, -0.03, -0.07, 0.1);
    const ex = (dep, col, y, sc) => { const geo = new THREE.ExtrudeGeometry(sh, { depth: dep, bevelEnabled: false }); geo.rotateX(-PI / 2); const m = new THREE.Mesh(geo, mat(col)); m.scale.set(s * sc, s, s * sc); m.position.y = y * s; m.castShadow = true; return m; };
    g.add(ex(0.02, '#C9CED4', 0, 1.0), ex(0.05, '#3FA7B5', 0.02, 0.9));
    g.add(rod([0, 0.075 * s, -0.08 * s], [0, 0.13 * s, -0.06 * s], 0.012 * s, '#2F7F8B'), rod([0, 0.13 * s, -0.06 * s], [0, 0.13 * s, 0.05 * s], 0.014 * s, '#2F7F8B'), rod([0, 0.13 * s, 0.05 * s], [0, 0.075 * s, 0.08 * s], 0.012 * s, '#2F7F8B'));
    const pf = grp(); pf.position.set(0, 0.03 * s, 0.1 * s); g.add(pf); const steam = foamPuffs(pf, 8, 21);
    g.userData.update = t => { for (const a of [].concat(o.steamAt ?? [])) steam(t, a, 0.1 * s, 0.6, 0.016 * s); };
    g.userData.update(-1); return g;
  },
  // o.folded: legs against the board, standing on its square end (handed over); o.form: an official form clipped near the top
  tacheBoard(o) {
    const L = o.len ?? 1.4, Wb = o.w ?? 0.42, hb = o.h ?? 0.95, g = grp(), top = grp(); g.add(top);
    // (round 1) a long pointed nose (it read as a plain panel), a chrome iron rest at the square end
    const sh = new THREE.Shape(); sh.moveTo(-L / 2, -Wb / 2); sh.lineTo(L / 2 - 0.55, -Wb / 2); sh.quadraticCurveTo(L / 2 - 0.05, -Wb * 0.42, L / 2, -Wb * 0.06); sh.quadraticCurveTo(L / 2 + 0.01, 0, L / 2, Wb * 0.06); sh.quadraticCurveTo(L / 2 - 0.05, Wb * 0.42, L / 2 - 0.55, Wb / 2); sh.lineTo(-L / 2, Wb / 2); sh.lineTo(-L / 2, -Wb / 2);
    const geo = new THREE.ExtrudeGeometry(sh, { depth: 0.035, bevelEnabled: false }); geo.rotateX(-PI / 2);
    const cover = new THREE.Mesh(geo, mat(o.color || '#9CC6E2')); cover.castShadow = cover.receiveShadow = true; top.add(cover);
    const geo2 = new THREE.ExtrudeGeometry(sh, { depth: 0.012, bevelEnabled: false }); geo2.rotateX(-PI / 2); const trim = new THREE.Mesh(geo2, mat('#5E8FB0')); trim.scale.set(1.01, 1, 1.03); trim.position.y = -0.006; top.add(trim);
    if (o.form) { const f = canvasPlane(0.3, 0.4, (c, W, H) => { c.fillStyle = '#FBF8EE'; c.fillRect(0, 0, W, H); c.fillStyle = INK; c.textAlign = 'center'; c.textBaseline = 'middle'; let fs = W * 0.13; c.font = `900 ${fs}px Arial`; const t1 = 'ENTRETIEN', tw = c.measureText(t1).width; if (tw > W * 0.86) { fs *= W * 0.86 / tw; c.font = `900 ${fs}px Arial`; } c.fillText(t1, W / 2, H * 0.12);
        c.fillStyle = '#9AA3AE'; for (let i = 0; i < 7; i++) { c.fillRect(W * 0.12, H * (0.26 + i * 0.09), W * 0.5, H * 0.014); c.strokeStyle = '#6E757E'; c.lineWidth = W * 0.01; c.strokeRect(W * 0.72, H * (0.24 + i * 0.09), W * 0.06, W * 0.06); } }, { res: 256 });
      f.rotation.x = -PI / 2; f.rotation.z = 0.08; f.position.set(o.formX ?? 0.18, 0.04, 0); top.add(f); }
    if (o.rest !== false) { const rc = '#B8BEC6'; top.add(rod([-L / 2, 0.02, -Wb * 0.36], [-L / 2 - 0.2, 0.02, -Wb * 0.3], 0.012, rc), rod([-L / 2, 0.02, Wb * 0.36], [-L / 2 - 0.2, 0.02, Wb * 0.3], 0.012, rc), rod([-L / 2 - 0.2, 0.02, -Wb * 0.3], [-L / 2 - 0.2, 0.02, Wb * 0.3], 0.012, rc));
      top.add(at(box(0.16, 0.012, Wb * 0.5, '#8A9098', { outline: 0.003 }), -L / 2 - 0.1, 0.03, 0)); }
    const legs = grp(); g.add(legs);
    if (o.folded) { for (const sd of [-1, 1]) legs.add(rod([-L * 0.38, -0.05, sd * 0.13], [L * 0.22, -0.05, -sd * 0.13], 0.02, '#6E757E')); legs.add(rod([L * 0.22, -0.05, -0.15], [L * 0.22, -0.05, 0.15], 0.022, '#2A2A2E'), rod([-L * 0.38, -0.05, -0.15], [-L * 0.38, -0.05, 0.15], 0.022, '#2A2A2E')); top.position.y = 0; }
    else { top.position.y = hb; for (const sd of [-1, 1]) { legs.add(rod([-L * 0.3, hb - 0.02, sd * 0.13], [L * 0.2, 0.0, sd * 0.13], 0.014, '#8A9098'), rod([L * 0.2, hb - 0.02, sd * 0.13], [-L * 0.3, 0.0, sd * 0.13], 0.014, '#8A9098')); }
      legs.add(rod([L * 0.2, 0.01, -0.15], [L * 0.2, 0.01, 0.15], 0.016, '#2A2A2E'), rod([-L * 0.3, 0.01, -0.15], [-L * 0.3, 0.01, 0.15], 0.016, '#2A2A2E')); }
    return g;
  },

  // ---------------------------------------------------------------- (round 1) life in the white street: foam flakes drifting down through a box
  // (o.w x o.h x o.d, from y 0 up) and drops of white foam dripping from a gutter line (o.drips: [[x, y, z] ...] in the prop's frame), all looping
  tacheFoamDrift(o) {
    const g = grp(), W = o.w ?? 6, Hh = o.h ?? 4, D = o.d ?? 3, n = o.n ?? 26, fl = [], dr = [];
    for (let i = 0; i < n; i++) { const m = sphere(1, '#FBFCFE', 1, { unique: true }); m.castShadow = false; m.material.emissive = new THREE.Color('#5A6E8A'); m.material.emissiveIntensity = 0.35; g.add(m);
      fl.push({ m, x: (hsh(i) - 0.5) * W, z: (hsh(i + 31) - 0.5) * D, ph: hsh(i + 7), v: 0.35 + 0.35 * hsh(i + 13), r: (o.size ?? 0.07) * (0.6 + 0.8 * hsh(i + 19)) }); }
    for (const [j, p] of (o.drips || []).entries()) { const m = sphere(1, '#FBFCFE', 1, { unique: true }); m.castShadow = false; m.material.emissive = new THREE.Color('#5A6E8A'); m.material.emissiveIntensity = 0.35; g.add(m);
      const b = sphere(1, '#FBFCFE', 1, { unique: true }); b.castShadow = false; g.add(b); dr.push({ m, b, p, ph: hsh(j + 3), per: 0.55 + 0.25 * hsh(j + 5) }); }
    g.userData.update = t => {
      for (const f of fl) { const y = Hh - ((f.ph * Hh + f.v * t) % Hh); f.m.position.set(f.x + 0.18 * Math.sin(t * 1.7 + f.ph * 9), y, f.z + 0.12 * Math.cos(t * 1.3 + f.ph * 7)); f.m.scale.set(f.r * 1.3, f.r * 0.8, f.r); f.m.rotation.z = t + f.ph * 6; }
      for (const d of dr) { const u = ((t / d.per) + d.ph) % 1, fall = u < 0.45 ? 0 : (u - 0.45) / 0.55, sw = u < 0.45 ? smooth(u / 0.45) : 1;
        d.b.position.set(d.p[0], d.p[1] - 0.03, d.p[2]); d.b.scale.set(0.06, 0.045, 0.06);
        d.m.position.set(d.p[0], d.p[1] - 0.05 - 0.04 * sw - 5 * fall * fall * d.per * d.per, d.p[2]); const r = 0.025 + 0.025 * sw; d.m.scale.set(r, r * (1 + 1.2 * fall + 0.6 * sw), r); d.m.visible = d.m.position.y > (o.floor ?? -d.p[1]) + 0.02; }
    };
    g.userData.update(0); return g;
  },
  // ---------------------------------------------------------------- (round 1) the town hall's doorway (front +Z): a deep dark opening in a white stone
  // frame, the MAIRIE plate above it in dark letters on white with a dark rim, o.w x o.h (the opening)
  tacheDoorway(o) {
    const w = o.w ?? 1.5, h = o.h ?? 2.6, g = grp(), st = o.stone || '#F4F6F8';
    const hole = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: o.dark || '#161A22' })); hole.position.set(0, h / 2, 0.0); g.add(hole);
    g.add(at(box(w + 0.02, 0.02, 0.5, '#0E1118'), 0, 0.01, -0.25), at(box(w * 0.48, h * 0.96, 0.04, '#232A36', { outline: 0.004 }), -w * 0.26, h * 0.48, -0.42));
    for (const sd of [-1, 1]) g.add(at(box(0.22, h + 0.22, 0.16, st, { outline: 0.008 }), sd * (w / 2 + 0.11), (h + 0.22) / 2, 0.06));
    g.add(at(box(w + 0.66, 0.24, 0.2, st, { outline: 0.008 }), 0, h + 0.12, 0.07));
    const pw = o.plateW ?? w + 0.3, plate = canvasPlane(pw, 0.46, (c, W, H) => { c.fillStyle = '#FBFCFD'; c.fillRect(0, 0, W, H); c.strokeStyle = '#1E2633'; c.lineWidth = H * 0.12; c.strokeRect(H * 0.06, H * 0.06, W - H * 0.12, H - H * 0.12);
      let fs = H * 0.62; c.font = `900 ${fs}px Arial`; const tw = c.measureText('MAIRIE').width; if (tw > W * 0.82) { fs *= W * 0.82 / tw; c.font = `900 ${fs}px Arial`; } c.fillStyle = '#1E2633'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('MAIRIE', W / 2, H * 0.55); }, { res: 512 });
    plate.position.set(0, h + 0.5, 0.2); g.add(plate); g.add(at(box(pw + 0.06, 0.52, 0.03, '#1E2633'), 0, h + 0.5, 0.18));
    return g;
  },
};
