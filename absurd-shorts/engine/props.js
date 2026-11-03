// Prop library: compact low-poly props in the paper style. buildProp(name, opts) -> Object3D.
// Conventions: origin at the prop's base (y = 0), front faces +Z, 1 unit = 1 m.
//   userData.grip   = local point a hand holds (handheld props)
//   userData.update = (t) => {...} for animated props (pure function of t, no clocks)
//   userData.center = visual centre for floating FX (explosion, zzz, ...)
// The root returned by buildProp is never transformed by builders, so the director can
// freely set position / rotation / scale on it.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, sphere, textPlane, addOutline, rng, ease, clamp01, grainTexture } from './style.js';

const PI = Math.PI, TAU = PI * 2;
const ORANGE = '#E07A2E', BLUE = '#2F62B5', LCD = '#7CE38B';

/* ------------------------------------------------------------------ helpers (shared with sets.js) */
const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
export const grp = (...kids) => { const g = new THREE.Group(); kids.forEach(k => k && g.add(k)); return g; };
export function at(o, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0) { o.position.set(x, y, z); o.rotation.set(rx, ry, rz); return o; }
export function mesh(geo, material) { const m = new THREE.Mesh(geo, material); m.castShadow = m.receiveShadow = true; return m; }
// Cylinder spanning two points (wires, frame tubes, ladder ropes...).
export function rod(a, b, r, color, seg = 6) {
  const A = new THREE.Vector3(...a), B = new THREE.Vector3(...b);
  const m = cyl(r, r, A.distanceTo(B), color, seg);
  m.position.copy(A).add(B).multiplyScalar(0.5);
  m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), B.sub(A).normalize());
  return m;
}
export const torus = (R, r, color, rs = 6, ts = 14, arc = TAU, o) => mesh(new THREE.TorusGeometry(R, r, rs, ts, arc), mat(color, o));
export const extrude = (shape, depth, color, o = {}) => mesh(new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled: false, curveSegments: o.curve || 4 }), mat(color, o));
export const poly = pts => new THREE.Shape(pts.map(([x, y]) => new THREE.Vector2(x, y)));
// Emissive "light" material (lamps, LEDs, lit windows).
export const glow = color => mat(color, { emissive: color, noGrain: true });
const _glass = new Map();
export function glassMat(opacity = 0.25, color = '#D9EEEE') {
  const k = opacity + color;
  if (!_glass.has(k)) _glass.set(k, new THREE.MeshLambertMaterial({ color, transparent: true, opacity, depthWrite: false, side: THREE.DoubleSide }));
  return _glass.get(k);
}
// Unlit FX material (bursts, speed lines) — stays bright under any lighting.
export const fxMat = (color, opacity = 1) => new THREE.MeshBasicMaterial({ color, map: grainTexture(), side: THREE.DoubleSide, transparent: opacity < 1, opacity, depthWrite: opacity >= 1 });
// Text label with automatic font size (and auto line-wrap for long single lines).
export function label(text, w, h, o = {}) {
  let s = String(text);
  if (o.wrap !== false && !s.includes('\n') && s.length > 12 && s.includes(' ')) { const mid = s.length / 2; let best = -1; for (let i = 0; i < s.length; i++) if (s[i] === ' ' && (best < 0 || Math.abs(i - mid) < Math.abs(best - mid))) best = i; s = s.slice(0, best) + '\n' + s.slice(best + 1); }
  const lines = s.split('\n'), maxLen = Math.max(1, ...lines.map(l => l.length)), H = 512 * h / w;
  const px = Math.floor(Math.min(H * 0.74 / (lines.length + 0.15), 512 * 0.9 / (maxLen * 0.66)));
  const { wrap, ...rest } = o; void wrap;
  return textPlane(s, { w, h, font: `bold ${px}px Arial`, ...rest, lines });
}
// Plane painted with an arbitrary canvas drawing (screens, boards, glyphs).
export function canvasPlane(w, h, draw, { res = 512, emissive = 0, transparent = false } = {}) {
  const c = document.createElement('canvas'); c.width = res; c.height = Math.max(8, Math.round(res * h / w));
  draw(c.getContext('2d'), c.width, c.height);
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const m = new THREE.MeshLambertMaterial({ map: tex, transparent, side: THREE.DoubleSide, alphaTest: transparent ? 0.05 : 0 });
  if (emissive) { m.emissive = new THREE.Color('#ffffff'); m.emissiveMap = tex; m.emissiveIntensity = emissive; }
  return new THREE.Mesh(new THREE.PlaneGeometry(w, h), m);
}
// Outlined glyph cut-out ("?", "!", "Z") with a darker back layer for paper thickness.
function glyph(ch, fill, size, opacity = 1) {
  const draw = (g, W, H) => { g.font = `900 ${W * 0.82}px Arial`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.lineJoin = 'round'; g.lineWidth = W * 0.09; g.strokeStyle = P.ink; g.strokeText(ch, W / 2, H * 0.54); g.fillStyle = fill; g.fillText(ch, W / 2, H * 0.54); };
  const f = canvasPlane(size, size, draw, { res: 256, transparent: true, emissive: 0.8 });
  const b = canvasPlane(size, size, (g, W, H) => { draw(g, W, H); }, { res: 256, transparent: true });
  b.material.color.set('#3a3a3a'); b.position.set(0.012, -0.012, -0.02);
  f.material.opacity = b.material.opacity = opacity;
  return grp(f, b);
}
// Instanced copies of one geometry: list of [x, y, z, rx, ry, rz, sx, sy, sz]; optional per-instance colours.
export function inst(geo, material, list, colors) {
  const m = new THREE.InstancedMesh(geo, material, list.length), o = new THREE.Object3D(), c = new THREE.Color();
  list.forEach((p, i) => { o.position.set(p[0], p[1], p[2]); o.rotation.set(p[3] || 0, p[4] || 0, p[5] || 0); o.scale.set(p[6] ?? 1, p[7] ?? 1, p[8] ?? 1); o.updateMatrix(); m.setMatrixAt(i, o.matrix); if (colors) m.setColorAt(i, c.set(colors[i])); });
  m.castShadow = m.receiveShadow = true; m.computeBoundingSphere(); return m;
}
const boxGeo = (w, h, d, pivotBottom) => { const g = new THREE.BoxGeometry(w, h, d); if (pivotBottom) g.translate(0, h / 2, 0); return g; };
const noShadow = o => { o.traverse(n => { n.castShadow = false; }); return o; };
// Star outline shape for bursts.
function starShape(n, R, r, rnd) {
  const s = new THREE.Shape();
  for (let i = 0; i < n * 2; i++) { const a = i / (n * 2) * TAU + PI / 2, rad = (i % 2 ? r : R) * (rnd ? 0.82 + rnd() * 0.36 : 1); i ? s.lineTo(Math.cos(a) * rad, Math.sin(a) * rad) : s.moveTo(Math.cos(a) * rad, Math.sin(a) * rad); }
  s.closePath(); return s;
}
// Pie wedge (pizza, slices) lying flat, bottom at y=0.
function wedge(r, h, color, a0 = 0, a1 = TAU, seg = 12) {
  const s = new THREE.Shape(); s.moveTo(0, 0); s.absarc(0, 0, r, a0, a1, false); s.lineTo(0, 0);
  return mesh(new THREE.ExtrudeGeometry(s, { depth: h, bevelEnabled: false, curveSegments: seg }).rotateX(-PI / 2), mat(color));
}

// A social-media post card (avatar, name, handle, "translated from" line, text, counters) drawn on a canvas.
function tweetCard(g, W, H, o) {
  g.fillStyle = '#FFFFFF'; g.fillRect(0, 0, W, H);
  let top = 0;
  if (o.repost) { // "X a reposté" banner above the post, bold and readable
    g.fillStyle = '#00A86B'; g.fillRect(0, 0, W, W * 0.2); g.fillStyle = '#FFFFFF'; g.font = `bold ${W * 0.068}px Arial`; g.textAlign = 'left'; g.textBaseline = 'middle';
    const words = String(o.repost).split(' '); let line = '', yy = W * 0.065; for (const w of words) { const t = line ? line + ' ' + w : w; if (g.measureText(t).width > W * 0.88 && line) { g.fillText(line, W * 0.06, yy); yy += W * 0.075; line = w; } else line = t; } g.fillText(line, W * 0.06, yy);
    top = W * 0.22; }
  const pad = W * 0.07, av = W * 0.16; g.fillStyle = o.avatar || '#E8775F'; g.beginPath(); g.arc(pad + av / 2, top + pad + av / 2, av / 2, 0, TAU); g.fill();
  g.fillStyle = '#FFFFFF'; g.font = `900 ${av * 0.5}px Arial`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(o.initial || 'K', pad + av / 2, top + pad + av / 2);
  g.textAlign = 'left'; g.textBaseline = 'alphabetic'; g.fillStyle = '#14171A'; g.font = `bold ${W * 0.075}px Arial`; g.fillText(o.name || 'Kenji', pad * 1.4 + av, top + pad + av * 0.45);
  g.fillStyle = '#657786'; g.font = `${W * 0.06}px Arial`; g.fillText(o.handle || '@kenji_lol', pad * 1.4 + av, top + pad + av * 0.95);
  let y = top + pad * 2 + av; g.fillStyle = '#1D9BF0'; g.font = `${W * 0.055}px Arial`; g.fillText(o.via || 'Traduit du japonais par X', pad, y); y += W * 0.1;
  g.fillStyle = '#14171A'; const fs = W * (o.fs || 0.082); g.font = `bold ${fs}px Arial`;
  const words = String(o.text || '').split(' '); let line = '';
  for (const w of words) { const t = line ? line + ' ' + w : w; if (g.measureText(t).width > W - pad * 2 && line) { g.fillText(line, pad, y); y += fs * 1.25; line = w; } else line = t; }
  if (line) { g.fillText(line, pad, y); y += fs * 1.25; }
  y += fs * 0.6; g.fillStyle = '#E1E8ED'; g.fillRect(pad, y, W - pad * 2, Math.max(2, W * 0.006)); y += fs * 1.2;
  g.fillStyle = '#657786'; g.font = `${W * 0.06}px Arial`; g.fillText(o.likes || '0 rire · 0 like', pad, y);
}

/* ------------------------------------------------------------------ felt-pen handwriting (shared) */
// Canvas texture of wobbly marker letters. draw(k) reveals the text left to right (k = 0..1, a pure function of k:
// the same jitter on every redraw, so frames render identically in any order).
function scrawlTexture(text, aspect, o = {}) {
  const res = o.res || 512, cv = document.createElement('canvas'); cv.width = res; cv.height = Math.max(8, Math.round(res / aspect));
  const g = cv.getContext('2d'), W = cv.width, H = cv.height, tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
  const chars = [...String(text)], n = Math.max(1, chars.length), r = rng(o.seed || 7 + n);
  const fs = Math.min(H * (o.fill || 0.78), W * 0.92 / (n * 0.74)), font = `italic 900 ${Math.round(fs)}px Arial, "Liberation Sans", sans-serif`;
  g.font = font; const ws = chars.map(ch => g.measureText(ch).width * 1.04), tot = ws.reduce((a, b) => a + b, 0), x0 = (W - tot) / 2;
  const jit = chars.map((_, i) => ({ dy: (r() - 0.5) * H * 0.12 - (i - n / 2) * H * 0.018, rot: (r() - 0.5) * 0.26 }));
  const color = o.color || '#15171C'; let last = -1;
  const draw = k => {
    k = Math.round(clamp01(k) * 200) / 200; if (k === last) return; last = k;
    g.clearRect(0, 0, W, H);
    if (k > 0) {
      g.save(); g.beginPath(); g.rect(0, 0, x0 + k * (tot + fs * 0.25), H); g.clip();
      g.font = font; g.textAlign = 'center'; g.textBaseline = 'middle'; g.lineJoin = 'round'; g.lineCap = 'round'; g.fillStyle = g.strokeStyle = color; g.lineWidth = fs * 0.09;
      let x = x0; chars.forEach((ch, i) => { g.save(); g.translate(x + ws[i] / 2, H / 2 + jit[i].dy); g.rotate(jit[i].rot); g.strokeText(ch, 0, 0); g.fillText(ch, 0, 0); g.restore(); x += ws[i]; });
      if (o.underline) { g.lineWidth = fs * 0.07; g.beginPath(); g.moveTo(x0, H / 2 + fs * 0.55); g.quadraticCurveTo(W / 2, H / 2 + fs * 0.72, x0 + tot + fs * 0.2, H / 2 + fs * 0.42); g.stroke(); }
      g.restore();
      if (o.strike) { g.save(); g.strokeStyle = o.strikeColor || color; g.lineCap = 'round'; g.lineWidth = fs * 0.12; g.beginPath(); g.moveTo(x0 - fs * 0.15, H * 0.64); g.lineTo(x0 + tot + fs * 0.15, H * 0.38); g.stroke(); g.restore(); }
    }
    tex.needsUpdate = true;
  };
  draw(1);
  return { tex, draw };
}
const scrawlK = (o, t) => o.writeAt == null ? 1 : clamp01((t - o.writeAt) / (o.writeDur || 0.8));
const scrawlMat = tex => new THREE.MeshLambertMaterial({ map: tex, transparent: true, alphaTest: 0.05, side: THREE.DoubleSide, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });

/* ------------------------------------------------------------------ prop builders */
const B = {
  // --- handheld / small objects -------------------------------------------------
  leafBlower() {
    const g = grp(
      at(box(0.32, 0.28, 0.38, P.red, { outline: 0.03 }), 0, 0.14, 0),
      at(cyl(0.11, 0.11, 0.05, P.greyDark, 8), 0.18, 0.15, -0.02, 0, 0, PI / 2),
      at(box(0.04, 0.12, 0.04, P.ink), 0, 0.34, 0.13), at(box(0.04, 0.12, 0.04, P.ink), 0, 0.34, -0.13),
      at(box(0.05, 0.05, 0.32, P.ink), 0, 0.41, 0),
      rod([0, 0.14, 0.15], [0, 0.08, 1.05], 0.055, P.navy, 8),
      rod([0, 0.08, 1.05], [0, 0.07, 1.2], 0.042, P.teal, 8));
    g.userData.grip = [0, 0.41, 0]; return g;
  },
  magnifyingGlass() {
    const R = 0.26, cy = 0.46 + R;
    const lens = at(new THREE.Mesh(new THREE.CylinderGeometry(R, R, 0.015, 16), glassMat(0.35, '#CFE6E8')), 0, cy, 0, PI / 2);
    const g = grp(cyl(0.032, 0.04, 0.4, P.woodDark, 6, { pivot: 'bottom' }), at(cyl(0.05, 0.05, 0.07, P.navy, 8), 0, 0.42, 0),
      at(torus(R, 0.038, P.navy, 6, 16), 0, cy, 0), lens,
      at(box(0.035, 0.2, 0.02, P.white, { noGrain: true }), -0.09, cy + 0.06, 0, 0, 0, -0.55));
    g.userData.grip = [0, 0.2, 0]; return g;
  },
  sandwich(o) {
    const s = grp(), layers = [[P.creamDark, 0.09, 0.5, 0], [P.teal, 0.035, 0.58, 0.2], [P.red, 0.05, 0.42, 0], [P.yellow, 0.025, 0.52, 0.78], [P.tealLight, 0.035, 0.56, -0.25]];
    let y = 0;
    layers.forEach(([c, h, w, ry]) => { s.add(at(box(w, h, w, c), 0, y + h / 2, 0, 0, ry, 0)); y += h; });
    s.add(at(box(0.5, 0.12, 0.5, P.creamDark, { taper: 0.82, outline: 0.02 }), 0, y + 0.06, 0));
    s.add(rod([0, y, 0], [0, y + 0.32, 0], 0.008, P.wood), at(sphere(0.04, P.green, 0), 0, y + 0.3, 0));
    s.scale.setScalar(o.scale || 1);
    const g = grp(s); g.userData.grip = [0, (y + 0.06) * (o.scale || 1), 0.25 * (o.scale || 1)]; return g;
  },
  milkBottle() {
    const r = 0.11;
    const g = grp(at(cyl(r, r, 0.26, P.white, 6, { pivot: 'bottom' }), 0, 0, 0, 0, PI / 6), at(cyl(0.05, r, 0.09, P.white, 6, { pivot: 'bottom' }), 0, 0.26, 0, 0, PI / 6),
      at(cyl(0.05, 0.05, 0.05, P.white, 6, { pivot: 'bottom' }), 0, 0.35, 0), at(cyl(0.056, 0.056, 0.035, P.red, 8, { pivot: 'bottom' }), 0, 0.4, 0),
      at(label('MILK', 0.11, 0.07, { bg: P.tealLight, fg: P.navy }), 0, 0.13, r * Math.cos(PI / 6) + 0.002));
    g.userData.grip = [0, 0.16, 0]; return g;
  },
  donut() {
    const R = 0.14, r = 0.065, rr = rng(4);
    const g = grp(at(torus(R, r, P.wood, 6, 10), 0, r, 0, -PI / 2));
    const icing = at(torus(R, r * 1.06, P.pink, 6, 10), 0, r + 0.022, 0, -PI / 2); icing.scale.z = 0.55; g.add(icing);
    for (let i = 0; i < 12; i++) { const a = rr() * TAU, d = R + (rr() - 0.5) * 0.07; g.add(at(box(0.03, 0.012, 0.01, [P.white, P.teal, P.yellow, P.navy][i % 4]), Math.cos(a) * d, r + 0.058, Math.sin(a) * d, 0, rr() * PI, 0)); }
    g.userData.grip = [0.2, r, 0]; return g;
  },
  phone911(o = {}) {
    const screen = canvasPlane(0.125, 0.25, (g, W, H) => {
      g.fillStyle = BLUE; g.fillRect(0, 0, W, H); g.fillStyle = '#fff'; g.textAlign = 'center'; g.textBaseline = 'middle';
      if (o.screen === 'tiktok') { // generic short-video app: black feed, a flexing silhouette, colour-offset note, side buttons
        g.fillStyle = '#0B0B0D'; g.fillRect(0, 0, W, H);
        g.fillStyle = '#E8E8E8'; g.fillRect(W * 0.38, H * 0.3, W * 0.24, H * 0.28); g.beginPath(); g.arc(W * 0.5, H * 0.25, W * 0.1, 0, TAU); g.fill();
        g.fillRect(W * 0.14, H * 0.3, W * 0.24, W * 0.1); g.fillRect(W * 0.62, H * 0.3, W * 0.24, W * 0.1); g.fillRect(W * 0.12, H * 0.2, W * 0.1, H * 0.12); g.fillRect(W * 0.78, H * 0.2, W * 0.1, H * 0.12);
        g.font = `900 ${W * 0.3}px Arial`; [['#25F4EE', -3], ['#FE2C55', 3], ['#FFFFFF', 0]].forEach(([c, d]) => { g.fillStyle = c; g.fillText('♪', W / 2 + d, H * 0.8 + d); });
        for (let i = 0; i < 3; i++) { g.fillStyle = '#FFFFFF'; g.beginPath(); g.arc(W * 0.86, H * (0.5 + i * 0.1), W * 0.045, 0, TAU); g.fill(); }
        return;
      }
      g.font = `900 ${W * 0.42}px Arial`; g.fillText(o.text || '911', W / 2, H * 0.36); g.font = `bold ${W * 0.17}px Arial`; g.fillText(o.sub || 'POLICE', W / 2, H * 0.53);
      g.beginPath(); g.arc(W / 2, H * 0.78, W * 0.13, 0, TAU); g.fillStyle = '#3DAA6A'; g.fill();
    }, { res: 256, emissive: 0.55 });
    const g = grp(box(0.14, 0.28, 0.018, P.ink, { pivot: 'bottom', outline: 0.03 }), at(screen, 0, 0.14, 0.0095));
    g.userData.grip = [0, 0.08, -0.01]; return g;
  },
  handcuffs() {
    const g = grp();
    [-1, 1].forEach(s => { const ring = at(torus(0.13, 0.026, P.white, 6, 12), s * 0.24, 0.16, 0); addOutline(ring, 0.07); g.add(ring, at(box(0.07, 0.09, 0.07, P.white, { outline: 0.06 }), s * 0.1, 0.16, 0)); });
    for (let i = 0; i < 3; i++) g.add(at(torus(0.025, 0.007, P.grey, 4, 8), -0.04 + i * 0.04, 0.16, 0, i % 2 ? PI / 2 : 0, 0, PI / 2));
    g.userData.grip = [0, 0.16, 0]; return g;
  },
  gavel(o) {
    const g = grp(cyl(0.024, 0.03, 0.42, P.woodDark, 6, { pivot: 'bottom' }), at(cyl(0.08, 0.08, 0.3, P.wood, 8), 0, 0.47, 0, 0, 0, PI / 2),
      at(cyl(0.085, 0.085, 0.03, P.woodDark, 8), 0.09, 0.47, 0, 0, 0, PI / 2), at(cyl(0.085, 0.085, 0.03, P.woodDark, 8), -0.09, 0.47, 0, 0, 0, PI / 2));
    if (o.block) g.add(at(cyl(0.14, 0.15, 0.06, P.woodDark, 10, { pivot: 'bottom' }), 0.4, 0, 0));
    g.userData.grip = [0, 0.14, 0]; return g;
  },
  briefcase() {
    const g = grp(box(0.5, 0.36, 0.13, P.suitBrown, { pivot: 'bottom', outline: 0.02 }), at(box(0.505, 0.02, 0.135, P.woodDark), 0, 0.27, 0),
      at(box(0.05, 0.035, 0.02, P.yellow), -0.14, 0.27, 0.07), at(box(0.05, 0.035, 0.02, P.yellow), 0.14, 0.27, 0.07),
      at(box(0.03, 0.06, 0.04, P.ink), -0.08, 0.39, 0), at(box(0.03, 0.06, 0.04, P.ink), 0.08, 0.39, 0), at(box(0.19, 0.03, 0.04, P.ink), 0, 0.42, 0));
    g.userData.grip = [0, 0.42, 0]; return g;
  },
  documents(o) {
    const g = grp(), r = rng(o.seed || 9), n = o.count || 6;
    for (let i = 0; i < n; i++) g.add(at(box(0.3, 0.012, 0.4, i % 2 ? P.paper : P.white), (r() - 0.5) * 0.03, i * 0.013 + 0.006, (r() - 0.5) * 0.03, 0, (r() - 0.5) * 0.22, 0));
    const top = n * 0.013 + 0.001, lines = grp(at(box(0.16, 0.003, 0.025, P.red), -0.04, 0, -0.14));
    for (let i = 0; i < 7; i++) lines.add(at(box(i % 3 === 2 ? 0.14 : 0.22, 0.003, 0.012, P.ink), i % 3 === 2 ? -0.04 : 0, 0, -0.08 + i * 0.035));
    lines.position.y = top; lines.rotation.y = g.children[n - 1].rotation.y; g.add(lines);
    g.userData.grip = [0, top / 2, 0.18]; return g;
  },
  mug(o) {
    const c = o.color || P.teal;
    const g = grp(cyl(0.075, 0.068, 0.14, c, 8, { pivot: 'bottom', open: true, doubleSide: true }), at(cyl(0.068, 0.068, 0.01, c, 8), 0, 0.005, 0),
      at(cyl(0.07, 0.07, 0.006, P.woodDark, 8), 0, 0.115, 0), at(torus(0.045, 0.014, c, 4, 8, PI), 0.074, 0.07, 0, 0, 0, -PI / 2));
    g.userData.grip = [0.115, 0.07, 0]; return g;
  },
  glueTube() {
    const g = grp(at(box(0.15, 0.03, 0.02, P.grey), 0, 0.015, 0), at(box(0.14, 0.3, 0.03, P.white, { pivot: 'bottom', taper: { x: 0.6, z: 2 }, outline: 0.02 }), 0, 0.02, 0),
      at(cyl(0.025, 0.042, 0.03, P.white, 8, { pivot: 'bottom' }), 0, 0.32, 0), at(cyl(0.022, 0.03, 0.08, P.red, 8, { pivot: 'bottom' }), 0, 0.35, 0),
      at(label('GLUE', 0.1, 0.05, { bg: P.yellow, fg: P.red }), 0, 0.15, 0.026, -0.05));
    g.userData.grip = [0, 0.15, 0]; return g;
  },
  banana() {
    const g = grp(), R = 0.35, n = 7, a0 = -0.95, a1 = 0.95;
    for (let i = 0; i < n; i++) {
      const a = a0 + (i + 0.5) * (a1 - a0) / n, th = 0.04 + 0.05 * Math.pow(Math.sin(PI * (i + 0.5) / n), 0.6);
      g.add(at(box(R * (a1 - a0) / n * 1.12, th, 0.08, P.yellow), R * Math.sin(a), R * (1 - Math.cos(a)) + th / 2, 0, 0, 0, a));
    }
    [a0, a1].forEach(a => g.add(at(box(0.04, 0.035, 0.04, P.woodDark), R * 1.0 * Math.sin(a), R * (1 - Math.cos(a)) + 0.03, 0, 0, 0, a)));
    g.userData.grip = [0, 0.04, 0]; return g;
  },
  hairDryer(o) {
    const c = o.color || P.pink;
    const g = grp(at(box(0.07, 0.2, 0.08, c, { pivot: 'bottom' }), 0, 0, -0.03, -0.25), at(cyl(0.075, 0.075, 0.24, c, 8), 0, 0.25, 0, PI / 2),
      at(cyl(0.045, 0.068, 0.12, P.ink, 8), 0, 0.25, 0.18, PI / 2), at(cyl(0.07, 0.07, 0.02, P.greyDark, 8), 0, 0.25, -0.125, PI / 2),
      at(box(0.02, 0.04, 0.03, P.white), 0, 0.14, 0.02, -0.25));
    g.userData.grip = [0, 0.08, -0.02]; return g;
  },
  umbrella(o) {
    const R = o.radius || 0.75, H = o.height || 1.0, cols = o.colors || [P.red, P.cream], op = o.open ?? 1;
    const g = grp(at(cyl(0.018, 0.018, H, P.navy, 6, { pivot: 'bottom' }), 0, 0.1, 0), at(torus(0.07, 0.018, P.woodDark, 4, 8, PI), 0.07, 0.1, 0, 0, 0, PI));
    const can = grp(); can.position.y = H + 0.1;
    for (let i = 0; i < 8; i++) can.add(mesh(new THREE.ConeGeometry(R, R * 0.42, 1, 1, true, i * TAU / 8, TAU / 8), mat(cols[i % cols.length], { doubleSide: true })));
    can.scale.set(0.12 + 0.88 * op, 1 + (1 - op) * 1.5, 0.12 + 0.88 * op);
    g.add(can, at(cyl(0.02, 0.02, 0.1, P.navy, 6, { pivot: 'bottom' }), 0, H + 0.1 + R * 0.2, 0));
    g.userData.grip = [0, 0.3, 0]; return g;
  },
  balloon(o) {
    const L = o.string || 1.2, piv = grp(box(0.006, L, 0.006, P.ink, { pivot: 'bottom' }));
    const ball = at(sphere(0.26, o.color || P.red, 1), 0, L + 0.32, 0); ball.scale.y = 1.18;
    piv.add(ball, at(new THREE.Mesh(new THREE.ConeGeometry(0.04, 0.05, 6), mat(o.color || P.red)), 0, L + 0.02, 0),
      at(box(0.05, 0.12, 0.02, P.white, { noGrain: true }), -0.11, L + 0.42, 0.2, 0, -0.4, 0.3));
    const g = grp(piv); g.userData.grip = [0, 0.03, 0];
    g.userData.update = t => { piv.rotation.z = Math.sin(t * 1.3) * 0.06; piv.rotation.x = Math.sin(t * 0.9 + 1) * 0.04; };
    return g;
  },
  money(o) {
    const g = grp(), n = o.count || 6, stacks = o.stacks || 1;
    const stack = () => { const s = grp(); for (let i = 0; i < n; i++) s.add(at(box(0.36, 0.024, 0.16, i % 2 ? P.green : '#7FAA6A'), 0, i * 0.025 + 0.012, 0)); const h = n * 0.025;
      s.add(at(box(0.07, h + 0.004, 0.164, P.paper), 0, h / 2 + 0.001, 0), at(box(0.28, 0.003, 0.11, '#A8C894'), 0.0, h + 0.0015, 0));
      s.add(at(label('$', 0.08, 0.08, { bg: null, fg: P.navy }), 0.1, h + 0.004, 0, -PI / 2)); return s; };
    for (let k = 0; k < stacks; k++) { const row = k < 3 ? 0 : 1; g.add(at(stack(), ((k % 3) - Math.min(2, stacks - 1) / 2) * 0.38, row * n * 0.025, row * 0.0, 0, (k * 0.37) % 0.2, 0)); }
    g.userData.grip = [0, n * 0.0125, 0]; return g;
  },
  // --- food ---------------------------------------------------------------------
  pizza(o) {
    const g = grp(), r = rng(o.seed || 3), a0 = 0, a1 = o.slice ? TAU / 8 : TAU - TAU / 8; // whole pie minus one slice
    g.add(wedge(0.42, 0.045, '#D9A35A', a0, a1), at(wedge(0.37, 0.012, P.yellow, a0 + 0.03, a1 - 0.03), 0, 0.045, 0));
    for (let i = 0; i < (o.slice ? 2 : 9); i++) { const a = a0 + 0.15 + r() * (a1 - a0 - 0.3), d = 0.1 + r() * 0.22; g.add(at(cyl(0.045, 0.045, 0.012, P.red, 8), Math.cos(a) * d, 0.062, -Math.sin(a) * d)); }
    g.userData.grip = [0.3, 0.03, 0]; return g;
  },
  // --- furniture ----------------------------------------------------------------
  table(o) {
    const w = o.w || 1.4, d = o.d || 0.8, h = o.h || 0.76;
    const g = grp(at(box(w, 0.07, d, o.color || P.wood, { outline: 0.01 }), 0, h - 0.035, 0));
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(at(box(0.07, h - 0.07, 0.07, o.legs || P.woodDark, { pivot: 'bottom' }), sx * (w / 2 - 0.08), 0, sz * (d / 2 - 0.08)));
    g.userData.top = [0, h, 0]; return g;
  },
  desk(o) {
    const w = o.w || 1.7, d = o.d || 0.8, h = 0.76, c = o.color || P.teal;
    const g = grp(at(box(w, 0.06, d, o.top || P.wood, { outline: 0.008 }), 0, h - 0.03, 0),
      at(box(0.5, h - 0.06, d - 0.06, c, { pivot: 'bottom' }), w / 2 - 0.28, 0, 0), at(box(0.06, h - 0.06, d - 0.06, c, { pivot: 'bottom' }), -w / 2 + 0.05, 0, 0),
      at(box(w - 0.1, 0.45, 0.03, c), 0, h - 0.29, d / 2 - 0.06));
    for (let i = 0; i < 3; i++) g.add(at(box(0.16, 0.03, 0.02, P.creamDark), w / 2 - 0.28, 0.15 + i * 0.2, -(d - 0.06) / 2 - 0.01));
    g.userData.top = [0, h, 0]; g.userData.seat = [0, 0, -0.75]; return g;
  },
  chair(o) {
    const c = o.color || P.wood;
    const g = grp(at(box(0.46, 0.06, 0.46, c, { outline: 0.01 }), 0, 0.45, 0), at(box(0.46, 0.5, 0.05, c), 0, 0.73, -0.205));
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(at(box(0.045, 0.42, 0.045, P.woodDark, { pivot: 'bottom' }), sx * 0.19, 0, sz * 0.19));
    g.userData.seat = [0, 0.48, 0]; return g;
  },
  courtBench() {
    const g = grp(at(box(3.4, 0.3, 1.4, P.woodDark, { pivot: 'bottom' }), 0, 0, -1.0),
      at(box(3.2, 1.45, 0.9, P.red, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(3.24, 0.14, 0.94, P.navy, { pivot: 'bottom' }), 0, 0, 0),
      at(box(3.45, 0.08, 1.15, P.wood, { outline: 0.01 }), 0, 1.49, -0.05),
      at(cyl(0.32, 0.32, 0.03, P.cream, 12), 0, 0.82, 0.46, PI / 2), at(torus(0.26, 0.025, P.navy, 4, 16), 0, 0.82, 0.48), at(cyl(0.1, 0.1, 0.03, P.yellow, 6), 0, 0.82, 0.475, PI / 2));
    [-1.1, 1.1].forEach(x => g.add(at(box(0.05, 1.1, 0.02, P.redDark), x, 0.8, 0.455)));
    g.userData.judgeSpot = [0, 0.3, -0.95]; return g;
  },
  bench(o) {
    const w = o.w || 1.7, g = grp();
    [-0.15, 0, 0.15].forEach(z => g.add(at(box(w, 0.04, 0.12, P.wood), 0, 0.45, z)));
    [0.62, 0.8].forEach(y => g.add(at(box(w, 0.1, 0.035, P.wood), 0, y, -0.26 - (y - 0.62) * 0.15, -0.15)));
    [-1, 1].forEach(s => { const x = s * (w / 2 - 0.15); g.add(at(box(0.06, 0.43, 0.06, P.ink, { pivot: 'bottom' }), x, 0, 0.17), at(box(0.06, 0.9, 0.06, P.ink, { pivot: 'bottom' }), x, 0, -0.24, -0.08), at(box(0.06, 0.04, 0.5, P.ink), x, 0.43, -0.03)); });
    g.userData.seat = [0, 0.47, 0]; return g;
  },
  bed(o) {
    const L = 2.0, W = o.w || 1.3, Lb = L * 0.62;
    const g = grp(at(box(W + 0.1, 0.25, L + 0.1, P.woodDark, { pivot: 'bottom' }), 0, 0.12, 0), at(box(W, 0.24, L, P.white), 0, 0.49, 0),
      at(box(W + 0.04, 0.26, Lb, o.blanket || P.teal), 0, 0.5, L / 2 - Lb / 2 + 0.01), at(box(W + 0.05, 0.27, 0.12, P.paper), 0, 0.5, L / 2 - Lb + 0.05),
      at(box(0.7, 0.13, 0.36, P.paper, { taper: 0.85 }), 0, 0.675, -L / 2 + 0.28),
      at(box(W + 0.16, 1.1, 0.08, P.woodDark, { pivot: 'bottom', outline: 0.01 }), 0, 0, -L / 2 - 0.07));
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(at(box(0.08, 0.12, 0.08, P.woodDark, { pivot: 'bottom' }), sx * W / 2, 0, sz * L / 2));
    g.userData.lie = [0, 0.62, 0]; return g;
  },
  stairs(o) {
    const n = o.steps || 8, w = o.w || 1.2, rise = 0.2, run = 0.28, g = grp();
    for (let i = 0; i < n; i++) g.add(at(box(w, rise * (i + 1), run, i % 2 ? P.cream : P.creamDark, { pivot: 'bottom' }), 0, 0, -i * run - run / 2), at(box(w + 0.01, 0.03, 0.04, P.navy), 0, rise * (i + 1) - 0.015, -i * run - 0.02));
    const x = w / 2 + 0.04, top = [x, rise * n + 0.9, -(n - 1) * run - run / 2], bot = [x, rise + 0.9, -run / 2];
    g.add(rod(bot, top, 0.025, P.woodDark), rod([x, rise, -run / 2], bot, 0.02, P.navy), rod([x, rise * n, top[2]], top, 0.02, P.navy));
    g.userData.top = [0, rise * n, -(n - 0.5) * run]; return g;
  },
  carpet(o) {
    const w = o.w || 2.4, d = o.d || 1.6, c = o.color || P.red;
    return grp(at(box(w, 0.015, d, c), 0, 0.0075, 0), at(box(w - 0.24, 0.006, d - 0.24, o.inner || P.cream), 0, 0.018, 0), at(box(w - 0.44, 0.006, d - 0.44, c), 0, 0.024, 0));
  },
  bathtub(o) {
    const W = 1.7, D = 0.78, H = 0.56, t = 0.07, y0 = 0.12, c = o.color || P.white;
    const g = grp(at(box(W, H, t, c), 0, y0 + H / 2, D / 2 - t / 2), at(box(W, H, t, c), 0, y0 + H / 2, -D / 2 + t / 2),
      at(box(t, H, D, c), W / 2 - t / 2, y0 + H / 2, 0), at(box(t, H, D, c), -W / 2 + t / 2, y0 + H / 2, 0), at(box(W, t, D, c), 0, y0 + t / 2, 0),
      at(box(W + 0.04, 0.04, 0.06, c, { outline: 0.01 }), 0, y0 + H, D / 2 - 0.02),
      at(cyl(0.025, 0.025, 0.3, P.grey, 6, { pivot: 'bottom' }), -W / 2 + 0.05, y0 + H, 0), at(box(0.16, 0.04, 0.05, P.grey), -W / 2 + 0.11, y0 + H + 0.28, 0));
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(at(box(0.1, y0, 0.1, P.yellow, { pivot: 'bottom', taper: 1.4 }), sx * (W / 2 - 0.12), 0, sz * (D / 2 - 0.1)));
    if (o.water !== false) { g.add(at(box(W - 2 * t, 0.01, D - 2 * t, P.tealLight), 0, y0 + H * 0.78, 0)); [[0.2, 0.1], [0.35, -0.12], [0.5, 0.05]].forEach(([x, z]) => g.add(at(sphere(0.07, P.white, 0), x, y0 + H * 0.78 + 0.03, z))); }
    g.userData.lie = [0, y0 + 0.2, 0]; return g;
  },
  toilet() {
    return grp(at(box(0.3, 0.38, 0.4, P.white, { pivot: 'bottom', taper: { x: 1.3, z: 1.15 } }), 0, 0, 0.05), at(box(0.42, 0.08, 0.5, P.white), 0, 0.42, 0.06),
      at(box(0.44, 0.04, 0.5, P.white, { outline: 0.01 }), 0, 0.48, 0.06), at(box(0.26, 0.042, 0.3, P.tealLight), 0, 0.482, 0.08),
      at(box(0.42, 0.48, 0.03, P.white), 0, 0.74, -0.2, -0.12), at(box(0.5, 0.42, 0.2, P.white, { outline: 0.01 }), 0, 0.72, -0.32), at(box(0.08, 0.02, 0.03, P.grey), 0.17, 0.86, -0.21));
  },
  // --- appliances ---------------------------------------------------------------
  fridge(o) {
    const W = 0.85, H = 1.9, D = 0.72, c = o.color || P.paper, inside = mat(P.tealPale, { unique: true });
    const g = grp(at(box(W, H, 0.05, c), 0, H / 2, -D / 2 + 0.025), at(box(0.05, H, D, c), W / 2 - 0.025, H / 2, 0), at(box(0.05, H, D, c), -W / 2 + 0.025, H / 2, 0),
      at(box(W, 0.05, D, c), 0, H - 0.025, 0), at(box(W, 0.08, D, c), 0, 0.04, 0), at(new THREE.Mesh(new THREE.BoxGeometry(W - 0.1, H - 0.14, 0.01), inside), 0, H / 2, -D / 2 + 0.056));
    [0.55, 0.95, 1.35].forEach(y => g.add(at(box(W - 0.1, 0.03, D - 0.1, P.white), 0, y, -0.02)));
    g.add(at(B.milkBottle({}), -0.18, 0.97, -0.05), at(box(0.18, 0.14, 0.14, P.red), 0.15, 1.04, -0.08), at(box(0.22, 0.1, 0.2, P.yellow), 0.1, 0.62, -0.05), at(sphere(0.07, P.green, 0), -0.2, 0.64, 0));
    const piv = grp(); piv.position.set(-W / 2, 0, D / 2); g.add(piv);
    piv.add(at(box(W, H - 0.02, 0.07, c, { outline: 0.008 }), W / 2, H / 2, 0.035), at(box(0.04, 0.5, 0.05, P.greyDark), W - 0.08, H * 0.58, 0.095),
      at(box(0.04, 0.22, 0.05, P.greyDark), W - 0.08, H * 0.85, 0.095), at(box(W - 0.02, 0.015, 0.075, P.greyDark), W / 2, 1.38, 0.036));
    const r = rng(o.seed || 21);
    for (let i = 0; i < (o.notes || 0); i++) piv.add(at(box(0.12, 0.12, 0.004, i % 4 === 3 ? P.pink : P.yellow), 0.15 + r() * 0.55, 0.85 + r() * 0.85, 0.073, 0, 0, (r() - 0.5) * 0.4));
    const setOpen = v => { piv.rotation.y = -clamp01(v) * 1.9; inside.emissive.set(v > 0.02 ? '#BFE3DA' : '#000000'); };
    setOpen(o.open || 0); g.userData.setOpen = setOpen;
    if (o.openAt !== undefined) { // open / close cycles: openAt and closeAt may be single times or lists
      const ev = [...[].concat(o.openAt).map(a => [a, 1]), ...[].concat(o.closeAt ?? []).map(a => [a, 0])].sort((a, b) => a[0] - b[0]);
      g.userData.update = t => { let v = o.open || 0; for (const [a, up] of ev) { if (t < a) break; v = up ? Math.max(v, ease.out(clamp01((t - a) / 0.5))) : Math.min(v, 1 - ease.inOut(clamp01((t - a) / 0.4))); } setOpen(v); };
    }
    if (o.hinge === 'R') g.scale.x = -1; // mirrored: door hinged on the right
    g.userData.front = [0, 0, D / 2 + 0.6]; return g;
  },
  toaster(o) {
    const g = grp(at(box(0.36, 0.03, 0.22, P.greyDark), 0, 0.015, 0), box(0.34, 0.24, 0.2, o.color || P.tealLight, { pivot: 'bottom', outline: 0.02 }),
      at(box(0.04, 0.04, 0.06, P.ink), 0.19, 0.17, 0));
    const toasts = [-0.05, 0.05].map(z => { const t = at(box(0.2, 0.18, 0.03, '#D9A35C'), 0, 0.17, z); g.add(t, at(box(0.24, 0.006, 0.045, P.ink), 0, 0.243, z)); return t; });
    if (o.popAt !== undefined) g.userData.update = t => { const p = clamp01((t - o.popAt) / 0.6); toasts.forEach((m, i) => m.position.y = 0.17 + 0.06 * ease.out(p) + (0.45 + i * 0.08) * Math.sin(PI * p)); };
    return g;
  },
  tv(o) {
    const scr = canvasPlane(0.6, 0.45, (g, W, H) => { g.fillStyle = o.screen || P.tealPale; g.fillRect(0, 0, W, H); g.fillStyle = P.navy; g.textAlign = 'center'; g.textBaseline = 'middle'; g.font = `bold ${H * 0.28}px Arial`;
      if (o.match) { g.fillStyle = '#3F8A4A'; g.fillRect(0, 0, W, H); g.strokeStyle = '#E8F2E8'; g.lineWidth = W * 0.012; g.strokeRect(W * 0.06, H * 0.1, W * 0.88, H * 0.8); g.beginPath(); g.moveTo(W / 2, H * 0.1); g.lineTo(W / 2, H * 0.9); g.stroke(); g.beginPath(); g.arc(W / 2, H / 2, H * 0.14, 0, 6.3); g.stroke();
        [[0.3, 0.4, '#B5302A'], [0.42, 0.62, '#B5302A'], [0.6, 0.35, '#2C4A8A'], [0.7, 0.58, '#2C4A8A'], [0.52, 0.5, '#F2F2F2']].forEach(([x, y, cc]) => { g.fillStyle = cc; g.beginPath(); g.arc(W * x, H * y, H * 0.035, 0, 6.3); g.fill(); }); }
      else if (o.text) g.fillText(o.text, W / 2, H / 2); else for (let i = 0; i < 9; i++) { g.fillStyle = `rgba(30,46,68,${0.08 + (i % 3) * 0.05})`; g.fillRect(0, i * H / 9, W, H / 18); } }, { res: 256, emissive: o.on === false ? 0 : 0.45 });
    const g = grp(at(box(0.9, 0.66, 0.55, P.woodDark, { pivot: 'bottom', outline: 0.01 }), 0, 0.3, 0), at(box(0.66, 0.5, 0.02, P.ink), -0.06, 0.63, 0.276), at(scr, -0.06, 0.63, 0.288),
      at(cyl(0.035, 0.035, 0.03, P.cream, 8), 0.36, 0.75, 0.28, PI / 2), at(cyl(0.035, 0.035, 0.03, P.cream, 8), 0.36, 0.6, 0.28, PI / 2),
      rod([0, 0.96, 0], [-0.25, 1.35, -0.05], 0.008, P.ink), rod([0, 0.96, 0], [0.22, 1.32, -0.05], 0.008, P.ink));
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(at(box(0.05, 0.3, 0.05, P.ink, { pivot: 'bottom' }), sx * 0.38, 0, sz * 0.2));
    return g;
  },
  microwave(o) {
    return grp(box(0.56, 0.33, 0.4, P.paper, { pivot: 'bottom', outline: 0.01 }), at(box(0.34, 0.22, 0.01, o.on ? '#F2C46B' : P.navy, o.on ? { emissive: '#B98A2E' } : {}), -0.06, 0.165, 0.205),
      at(box(0.03, 0.22, 0.04, P.grey), 0.135, 0.165, 0.21), at(label('12:00', 0.1, 0.04, { bg: P.ink, fg: LCD }), 0.21, 0.26, 0.202),
      ...[0, 1, 2].flatMap(i => [at(box(0.03, 0.02, 0.01, P.greyDark), 0.19, 0.19 - i * 0.04, 0.204), at(box(0.03, 0.02, 0.01, P.greyDark), 0.235, 0.19 - i * 0.04, 0.204)]));
  },
  cashRegister() {
    const keys = grp(); keys.position.set(0, 0.25, 0.08); keys.rotation.x = 0.45;
    for (let i = 0; i < 12; i++) keys.add(at(box(0.05, 0.02, 0.04, i === 11 ? P.red : P.navy), -0.1 + (i % 4) * 0.065, 0.012, -0.06 + Math.floor(i / 4) * 0.055));
    return grp(box(0.5, 0.12, 0.45, P.greyDark, { pivot: 'bottom' }), at(box(0.46, 0.16, 0.42, P.cream, { pivot: 'bottom', outline: 0.01 }), 0, 0.12, -0.01),
      at(box(0.44, 0.02, 0.26, P.cream), 0, 0.25, 0.08, 0.45), keys,
      at(box(0.04, 0.12, 0.04, P.greyDark, { pivot: 'bottom' }), 0, 0.28, -0.15), at(box(0.3, 0.12, 0.06, P.ink), 0, 0.44, -0.15), at(label('$0.00', 0.26, 0.08, { bg: P.ink, fg: LCD }), 0, 0.44, -0.118),
      at(box(0.04, 0.012, 0.01, P.cream), 0, 0.06, 0.226));
  },
  ATM() {
    const scr = canvasPlane(0.42, 0.28, (g, W, H) => { g.fillStyle = BLUE; g.fillRect(0, 0, W, H); g.fillStyle = '#fff'; g.font = `bold ${H * 0.2}px Arial`; g.textAlign = 'center'; g.fillText('INSERT CARD', W / 2, H * 0.55); }, { res: 256, emissive: 0.5 });
    const g = grp(box(0.85, 1.75, 0.65, P.teal, { pivot: 'bottom', outline: 0.006 }), at(box(0.89, 0.3, 0.69, P.red), 0, 1.9, 0),
      at(label('ATM', 0.7, 0.24, { bg: P.red, fg: P.white }), 0, 1.9, 0.347), at(box(0.7, 0.75, 0.04, P.cream), 0, 1.15, 0.34),
      at(box(0.46, 0.32, 0.01, P.ink), 0, 1.32, 0.365), at(scr, 0, 1.32, 0.372), at(box(0.4, 0.04, 0.02, P.ink), 0, 0.85, 0.37), at(box(0.12, 0.02, 0.02, P.ink), 0.2, 1.05, 0.37));
    for (let i = 0; i < 12; i++) g.add(at(box(0.04, 0.03, 0.015, P.greyDark), -0.07 + (i % 3) * 0.055, 1.08 - Math.floor(i / 3) * 0.04, 0.367));
    return g;
  },
  // --- big objects & vehicles ---------------------------------------------------
  helicopter() {
    const N = P.navy, y0 = 0.55, g = grp(), rotor = grp(), tr = grp();
    g.add(at(box(2.6, 1.3, 1.4, N, { outline: 0.012 }), 0, y0 + 0.65, 0), at(box(0.9, 1.1, 1.3, P.tealPale, { taper: { x: 0.45, z: 0.75 }, taperAxis: 'x' }), 1.74, y0 + 0.6, 0),
      at(box(2.6, 0.4, 0.34, N, { taper: 0.45, taperAxis: 'x' }), -2.4, y0 + 1.0, 0, 0, PI, 0),
      at(box(0.55, 0.95, 0.08, N, { taper: { x: 0.6, z: 1 } }), -3.55, y0 + 1.35, 0, 0, 0, 0.25),
      at(cyl(0.08, 0.1, 0.3, P.greyDark, 6, { pivot: 'bottom' }), 0, y0 + 1.3, 0));
    [-1, 1].forEach(s => { g.add(at(box(3.0, 0.08, 0.1, P.greyDark), 0.1, 0.04, s * 0.62), at(box(0.06, y0, 0.06, P.greyDark, { pivot: 'bottom' }), 0.8, 0, s * 0.55), at(box(0.06, y0, 0.06, P.greyDark, { pivot: 'bottom' }), -0.7, 0, s * 0.55));
      g.add(at(box(0.7, 0.5, 0.02, P.tealPale), 0.55, y0 + 0.88, s * 0.71), at(label('SWAT', 1.0, 0.36, { bg: null, fg: P.white }), -0.55, y0 + 0.45, s * 0.705, 0, s > 0 ? 0 : PI, 0)); });
    rotor.position.set(0, y0 + 1.62, 0);
    rotor.add(box(5.0, 0.04, 0.22, P.ink), at(box(5.0, 0.04, 0.22, P.ink), 0, 0, 0, 0, PI / 2, 0), cyl(0.16, 0.16, 0.12, P.greyDark, 8));
    tr.position.set(-3.6, y0 + 1.45, 0.1); tr.add(box(0.08, 0.95, 0.02, P.ink), at(box(0.08, 0.95, 0.02, P.ink), 0, 0, 0, 0, 0, PI / 2));
    g.add(rotor, tr);
    g.userData.update = t => { rotor.rotation.y = t * 17; tr.rotation.z = t * 29; };
    g.userData.ladder = [0.2, y0, 0]; return g;
  },
  ropeLadder(o) {
    const L = o.length || 4, sw = grp(); sw.position.y = L;
    [-0.22, 0.22].forEach(x => sw.add(at(box(0.035, L, 0.035, P.white, { pivot: 'top' }), x, 0, 0)));
    const n = Math.max(2, Math.floor(L / 0.32));
    for (let i = 0; i < n; i++) sw.add(at(box(0.52, 0.05, 0.06, P.red), 0, -(i + 0.6) * L / n, 0));
    const g = grp(sw); g.userData.top = [0, L, 0]; g.userData.grip = [0.22, L * 0.5, 0];
    g.userData.update = t => { sw.rotation.z = Math.sin(t * 1.8) * 0.06; sw.rotation.x = Math.sin(t * 1.3 + 1) * 0.04; };
    return g;
  },
  policeCar() {
    const W = P.white, N = P.navy, g = grp();
    const blue = mat('#2A4C8A', { unique: true, noGrain: true }), red = mat(P.redDark, { unique: true, noGrain: true });
    g.add(at(box(4.2, 0.6, 1.8, W, { outline: 0.012 }), 0, 0.62, 0), at(box(4.22, 0.22, 1.82, N), 0, 0.42, 0),
      at(box(2.3, 0.62, 1.6, W, { taper: { x: 0.78, z: 0.85 } }), -0.2, 1.23, 0), at(box(1.95, 0.38, 1.62, P.tealPale, { taper: { x: 0.8, z: 0.88 } }), -0.2, 1.24, 0),
      at(box(0.08, 0.42, 1.64, W), -0.15, 1.24, 0), at(box(0.12, 0.16, 1.84, P.greyDark), 2.12, 0.42, 0), at(box(0.12, 0.16, 1.84, P.greyDark), -2.12, 0.42, 0),
      at(box(0.4, 0.08, 1.1, P.ink), -0.2, 1.58, 0), at(new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.16, 0.45), blue), -0.2, 1.7, 0.27), at(new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.16, 0.45), red), -0.2, 1.7, -0.27));
    [-1, 1].forEach(s => { g.add(at(box(0.04, 0.14, 0.3, P.yellow, { noGrain: true }), 2.1, 0.72, s * 0.55), at(box(0.04, 0.14, 0.3, P.red), -2.1, 0.72, s * 0.55),
      at(label('POLICE', 1.6, 0.3, { bg: null, fg: N }), 0.1, 0.76, s * 0.905, 0, s > 0 ? 0 : PI, 0));
      [-1.35, 1.35].forEach(x => g.add(at(cyl(0.36, 0.36, 0.3, P.ink, 10), x, 0.36, s * 0.8, PI / 2), at(cyl(0.16, 0.16, 0.02, P.grey, 8), x, 0.36, s * 0.96, PI / 2))); });
    g.userData.update = t => { const on = Math.floor(t * 5) % 2 === 0;
      blue.color.set(on ? '#8FB4FF' : '#2A4C8A'); blue.emissive.set(on ? '#3C7BFF' : '#000000'); red.color.set(on ? P.redDark : '#FF8A7A'); red.emissive.set(on ? '#000000' : '#E0402E'); };
    g.userData.update(0); return g;
  },
  rocket(o) {
    const g = grp(at(cyl(0.45, 0.45, 2.4, P.white, 10, { pivot: 'bottom' }), 0, 0.5, 0), at(new THREE.Mesh(new THREE.ConeGeometry(0.45, 0.9, 10), mat(P.red)), 0, 3.35, 0),
      at(cyl(0.46, 0.46, 0.2, P.red, 10), 0, 0.75, 0), at(cyl(0.25, 0.35, 0.3, P.greyDark, 8, { pivot: 'bottom' }), 0, 0.2, 0),
      at(cyl(0.16, 0.16, 0.04, P.tealPale, 10), 0, 2.1, 0.44, PI / 2), at(torus(0.17, 0.035, P.navy, 4, 12), 0, 2.1, 0.45));
    for (let i = 0; i < 3; i++) { const a = i * TAU / 3 + PI / 6; g.add(at(box(0.06, 1.0, 0.6, P.red, { pivot: 'bottom', taper: { x: 1, z: 0.3 }, outline: 0.02 }), Math.sin(a) * 0.6, 0, Math.cos(a) * 0.6, 0, a, 0)); }
    if (o.flame) {
      const fl = grp(at(new THREE.Mesh(new THREE.ConeGeometry(0.32, 1.0, 8), fxMat(P.yellow)), 0, -0.5, 0, PI), at(new THREE.Mesh(new THREE.ConeGeometry(0.18, 0.6, 8), fxMat(P.salmon)), 0, -0.3, 0, PI));
      fl.position.y = 0.2; g.add(fl); g.userData.update = t => fl.scale.set(1, 1 + 0.25 * Math.sin(t * 40) + 0.15 * Math.sin(t * 23), 1);
    }
    return g;
  },
  bicycle(o) {
    const c = o.color || P.red, A = [-0.52, 0.355, 0], Bb = [0, 0.33, 0], S = [-0.12, 0.85, 0], H = [0.42, 0.86, 0], HL = [0.45, 0.72, 0], F = [0.52, 0.355, 0];
    const g = grp(rod(Bb, S, 0.022, c), rod(S, H, 0.022, c), rod(Bb, HL, 0.024, c), rod(A, Bb, 0.018, c), rod(A, S, 0.016, c), rod(H, F, 0.02, P.grey),
      rod(S, [-0.14, 0.95, 0], 0.015, P.grey), at(box(0.22, 0.05, 0.1, P.ink), -0.16, 0.97, 0), rod(H, [0.38, 1.02, 0], 0.016, P.grey), rod([0.38, 1.02, -0.27], [0.38, 1.02, 0.27], 0.016, P.ink),
      at(box(0.06, 0.12, 0.02, P.greyDark), 0, 0.33, 0.04));
    [A, F].forEach(p => g.add(at(torus(0.33, 0.025, P.ink, 4, 16), ...p), at(cyl(0.04, 0.04, 0.06, P.grey, 6), p[0], p[1], 0, PI / 2), rod([p[0] - 0.31, p[1], 0], [p[0] + 0.31, p[1], 0], 0.005, P.grey), rod([p[0], p[1] - 0.31, 0], [p[0], p[1] + 0.31, 0], 0.005, P.grey)));
    g.userData.seat = [-0.16, 1.0, 0]; return g;
  },
  shoppingCart() {
    const g = grp(), C = P.grey, b0 = 0.45, b1 = 0.98, X0 = [-0.42, 0.34], X1 = [-0.5, 0.45], Z0 = 0.26, Z1 = 0.32;
    const corner = (lvl, sx, sz) => lvl ? [sx < 0 ? X1[0] : X1[1], b1, sz * Z1] : [sx < 0 ? X0[0] : X0[1], b0, sz * Z0];
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(rod(corner(0, sx, sz), corner(1, sx, sz), 0.01, C));
    for (const lvl of [0, 1]) for (const [a, b] of [[[-1, -1], [1, -1]], [[-1, 1], [1, 1]], [[-1, -1], [-1, 1]], [[1, -1], [1, 1]]]) g.add(rod(corner(lvl, ...a), corner(lvl, ...b), 0.01, C));
    for (let i = 1; i < 8; i++) { const k = i / 8; for (const sz of [-1, 1]) g.add(rod([X0[0] + (X0[1] - X0[0]) * k, b0, sz * Z0], [X1[0] + (X1[1] - X1[0]) * k, b1, sz * Z1], 0.006, C)); }
    for (let i = 1; i < 5; i++) { const k = i / 5; g.add(rod([X0[1], b0, -Z0 + 2 * Z0 * k], [X1[1], b1, -Z1 + 2 * Z1 * k], 0.006, C)); }
    for (const sz of [-1, 1]) g.add(rod([X0[0], b0 + 0.27, sz * (Z0 + 0.03)], [X0[1] + 0.05, b0 + 0.27, sz * (Z0 + 0.03)], 0.006, C), rod([X1[0], b1, sz * Z1], [-0.62, 1.04, sz * Z1], 0.012, C));
    g.add(rod([-0.62, 1.04, -0.34], [-0.62, 1.04, 0.34], 0.025, P.red));
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) { const x = sx < 0 ? -0.38 : 0.3; g.add(rod([x, b0, sz * 0.24], [x, 0.1, sz * 0.24], 0.012, C), at(cyl(0.06, 0.06, 0.04, P.ink, 8), x, 0.06, sz * 0.24, PI / 2)); }
    g.add(rod([-0.38, 0.12, 0], [0.3, 0.12, 0], 0.01, C));
    g.userData.grip = [-0.62, 1.04, 0]; return g;
  },
  coffinVampire(o) {
    const pts = [[-0.24, -1.08], [0.24, -1.08], [0.42, 0.5], [0.29, 1.08], [-0.29, 1.08], [-0.42, 0.5]];
    const body = at(extrude(poly(pts), 0.42, '#1C1C22'), 0, 0, 0, -PI / 2);
    const inner = at(extrude(poly(pts.map(([x, y]) => [x * 0.84, y * 0.92])), 0.01, P.red), 0, 0.421, 0, -PI / 2);
    const lid = grp(at(extrude(poly(pts.map(([x, y]) => [x * 1.04, y * 1.03])), 0.07, '#2A2A33', { }), 0.42, 0, 0, -PI / 2),
      at(box(0.09, 0.02, 0.9, P.red), 0.42, 0.08, -0.25), at(box(0.42, 0.02, 0.09, P.red), 0.42, 0.08, -0.45));
    const piv = grp(lid); piv.position.set(-0.42, 0.42, 0); piv.rotation.z = (o.open || 0) * 1.9;
    addOutline(body, 0.015);
    const g = grp(body, inner, piv); g.userData.lie = [0, 0.43, 0]; return g;
  },
  // --- buildings, street furniture --------------------------------------------
  fence(o) {
    const L = o.length || 3, H = o.height || 0.95, n = Math.max(2, Math.round(L / 0.24)), pick = [], tips = [];
    for (let i = 0; i < n; i++) { const x = -L / 2 + (i + 0.5) * L / n; pick.push([x, 0, 0.03]); tips.push([x, H - 0.08, 0.03, 0, 0, PI / 4]); }
    const g = grp(inst(boxGeo(0.11, H - 0.08, 0.035, true), mat(o.color || P.white), pick), inst(boxGeo(0.078, 0.078, 0.035), mat(o.color || P.white), tips),
      at(box(L, 0.07, 0.04, o.rail || P.red), 0, H * 0.28, -0.01), at(box(L, 0.07, 0.04, o.rail || P.red), 0, H * 0.68, -0.01));
    return g;
  },
  house(o) {
    const w = o.w || 4, d = o.d || 3.4, h = o.h || 2.5, dx = w * 0.15;
    const g = grp(box(w, h, d, o.color || P.cream, { pivot: 'bottom', outline: 0.005 }), at(box(w + 0.5, 1.5, d + 0.5, o.roof || P.navy, { taper: { x: 1, z: 0.02 } }), 0, h + 0.75, 0),
      at(box(0.4, 1.3, 0.4, P.red), w * 0.3, h + 0.9, -0.5),
      at(box(0.78, 1.45, 0.06, o.door || P.red, { outline: 0.02 }), dx, 0.725, d / 2 + 0.03), at(sphere(0.04, P.yellow, 0), dx + 0.27, 0.72, d / 2 + 0.07),
      at(box(1.1, 0.12, 0.45, P.creamDark), dx, 0.06, d / 2 + 0.22));
    const win = (x, y, z, ry) => g.add(at(grp(box(0.9, 0.9, 0.05, o.frame || P.teal), at(box(0.72, 0.72, 0.06, P.tealPale), 0, 0, 0.003), at(box(0.72, 0.05, 0.07, o.frame || P.teal), 0, 0, 0.004), at(box(0.05, 0.72, 0.07, o.frame || P.teal), 0, 0, 0.004)), x, y, z, 0, ry, 0));
    win(-w * 0.25, 1.4, d / 2 + 0.025, 0); win(w / 2 + 0.025, 1.4, 0, PI / 2); win(-w / 2 - 0.025, 1.4, 0, -PI / 2);
    g.userData.door = [dx, 0, d / 2 + 0.5]; return g;
  },
  door(o) {
    const w = o.w || 0.95, h = o.h || 2.1, fr = o.frame || P.cream, piv = grp();
    const g = grp(at(box(0.1, h + 0.1, 0.12, fr), -w / 2 - 0.05, (h + 0.1) / 2, 0.06), at(box(0.1, h + 0.1, 0.12, fr), w / 2 + 0.05, (h + 0.1) / 2, 0.06),
      at(box(w + 0.3, 0.1, 0.12, fr), 0, h + 0.05, 0.06), at(box(w, h, 0.01, P.ink), 0, h / 2, 0.005), piv);
    piv.position.set(-w / 2, 0, 0.035);
    piv.add(at(box(w, h, 0.05, o.color || P.red, { outline: 0.006 }), w / 2, h / 2, 0), at(box(w * 0.62, h * 0.3, 0.012, P.redDark), w / 2, h * 0.72, 0.03),
      at(box(w * 0.62, h * 0.3, 0.012, P.redDark), w / 2, h * 0.3, 0.03), at(sphere(0.045, P.yellow, 0), w - 0.11, h * 0.48, 0.06));
    if (o.color && o.color !== P.red) piv.children.slice(1, 3).forEach(m => m.material = mat(new THREE.Color(o.color).multiplyScalar(0.82).getStyle()));
    if (o.plaque) piv.add(at(box(0.44, 0.13, 0.012, '#B8913A', { outline: 0.02 }), w / 2, h * 0.86, 0.042), at(label(o.plaque, 0.4, 0.1, { bg: '#D8B54A', fg: P.ink }), w / 2, h * 0.86, 0.049));
    let nameUp = null; // felt-pen name on the leaf (moves with the door)
    if (o.name) { const nw = w * 0.66, s = scrawlTexture(o.name, nw / 0.18, { ...o, color: o.inkColor || '#15171C' }); const m = new THREE.Mesh(new THREE.PlaneGeometry(nw, 0.18), scrawlMat(s.tex)); m.position.set(w / 2, o.nameY ?? h * 0.68, 0.046); m.renderOrder = 3; piv.add(m); nameUp = t => s.draw(scrawlK(o, t)); nameUp(-1e9); }
    const setOpen = v => { piv.rotation.y = -clamp01(v) * 1.6; }; setOpen(o.open || 0); g.userData.setOpen = setOpen;
    if (o.openAt !== undefined || nameUp) g.userData.update = t => { if (o.openAt !== undefined) setOpen(ease.out(clamp01((t - o.openAt) / 0.5)) - (o.closeAt !== undefined ? ease.inOut(clamp01((t - o.closeAt) / 0.4)) : 0)); nameUp?.(t); };
    return g;
  },
  window(o) {
    const w = o.w || 1.2, h = o.h || 1.2, c = o.color || P.teal, y = 0.14, gc = o.glass || (o.lit ? '#F2C46B' : o.night ? '#2A3A55' : P.sky);
    const g = grp(at(box(w, h, 0.02, gc, o.lit ? { emissive: '#C9922E' } : {}), 0, y + h / 2, 0.01),
      at(box(w + 0.18, 0.09, 0.08, c), 0, y + h + 0.045, 0.04), at(box(w + 0.18, 0.09, 0.08, c), 0, y - 0.045, 0.04),
      at(box(0.09, h, 0.08, c), -w / 2 - 0.045, y + h / 2, 0.04), at(box(0.09, h, 0.08, c), w / 2 + 0.045, y + h / 2, 0.04),
      at(box(w, 0.05, 0.05, c), 0, y + h / 2, 0.03), at(box(0.05, h, 0.05, c), 0, y + h / 2, 0.03), at(box(w + 0.36, 0.06, 0.18, o.sill || P.cream), 0, 0.03, 0.09));
    if (!o.lit && !o.night) g.add(at(box(0.05, h * 0.5, 0.005, P.white, { noGrain: true }), -w * 0.3, y + h * 0.7, 0.022, 0, 0, -0.5));
    if (o.curtains) [-1, 1].forEach(s => g.add(at(box(w * 0.28, h + 0.4, 0.06, o.curtains), s * (w / 2 + 0.05), y + h / 2 - 0.05, 0.12)));
    return g;
  },
  lightSwitch(o) {
    return grp(at(box(0.12, 0.18, 0.015, P.paper, { outline: 0.04 }), 0, 0.09, 0.0075), at(box(0.03, 0.06, 0.03, P.white), 0, 0.09, 0.025, (o.on ?? true) ? -0.35 : 0.35));
  },
  jailBars(o) {
    const w = o.width || 3, h = o.height || 2.6, n = Math.round(w / 0.2), list = [];
    for (let i = 1; i < n; i++) list.push([-w / 2 + i * w / n, 0, 0]);
    return grp(inst(new THREE.CylinderGeometry(0.028, 0.028, h, 6).translate(0, h / 2, 0), mat(P.greyDark), list),
      at(box(w, 0.1, 0.07, P.navy), 0, 0.05, 0), at(box(w, 0.1, 0.07, P.navy), 0, 1.1, 0), at(box(w, 0.12, 0.07, P.navy), 0, h - 0.06, 0),
      at(box(0.12, h, 0.12, P.navy, { pivot: 'bottom' }), -w / 2, 0, 0), at(box(0.12, h, 0.12, P.navy, { pivot: 'bottom' }), w / 2, 0, 0), at(box(0.12, 0.16, 0.1, P.yellow), w * 0.2, 1.1, 0));
  },
  powerLine(o) {
    const L = o.length || 8, sag = o.sag ?? 0.35, Ha = (o.height || 3.2) + sag, g = grp();
    const wireY = x => Ha - sag * (1 - Math.pow(2 * x / L, 2));
    [-1, 1].forEach(s => { g.add(at(cyl(0.1, 0.14, Ha + 0.5, P.woodDark, 6, { pivot: 'bottom' }), s * L / 2, 0, 0), at(box(0.12, 0.1, 1.3, P.woodDark), s * L / 2, Ha - 0.17, 0));
      [-0.45, 0, 0.45].forEach(z => g.add(at(cyl(0.04, 0.05, 0.12, P.white, 6, { pivot: 'bottom' }), s * L / 2, Ha - 0.12, z))); });
    [-0.45, 0, 0.45].forEach(z => { const pts = []; for (let i = 0; i <= 24; i++) { const x = -L / 2 + i * L / 24; pts.push(new THREE.Vector3(x, wireY(x), z)); }
      g.add(mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 32, 0.018, 4), mat(P.ink))); });
    g.userData.wireAt = wireY; g.userData.wireZ = [-0.45, 0, 0.45]; return g;
  },
  trafficCamera(o = {}) { // o.flashAt: time or list of times -> a white flash at the lens
    const led = mat(P.redDark, { unique: true, noGrain: true }), cam = grp();
    cam.position.set(0.8, 2.86, 0); cam.rotation.x = 0.25;
    cam.add(at(box(0.32, 0.24, 0.5, P.white, { outline: 0.03 }), 0, -0.12, 0.05), at(box(0.38, 0.04, 0.6, P.greyDark), 0, 0.02, 0.07),
      at(cyl(0.08, 0.08, 0.06, P.ink, 8), 0, -0.12, 0.32, PI / 2), at(new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.04, 0.02), led), 0.11, -0.03, 0.31));
    const g = grp(cyl(0.06, 0.08, 3.0, P.grey, 6, { pivot: 'bottom' }), at(box(0.9, 0.07, 0.07, P.grey), 0.42, 2.95, 0), at(box(0.06, 0.08, 0.06, P.grey), 0.8, 2.9, 0), cam);
    const fl = at(sphere(0.32, '#FFFFFF', 1, { emissive: '#FFFFFF', noGrain: true }), 0, -0.12, 0.45); fl.visible = false; cam.add(fl); const fls = [].concat(o.flashAt ?? []);
    g.userData.update = t => { const on = (t % 1) < 0.15; led.emissive.set(on ? '#FF3B2E' : '#000000'); fl.visible = fls.some(f => t >= f && t < f + 0.12); }; return g;
  },
  speedSign(o) {
    return grp(cyl(0.04, 0.04, 2.2, P.grey, 6, { pivot: 'bottom' }), at(cyl(0.42, 0.42, 0.04, P.white, 16), 0, 2.3, 0, PI / 2), at(torus(0.37, 0.05, P.red, 4, 18), 0, 2.3, 0.0),
      at(label(String(o.value ?? 30), 0.46, 0.34, { bg: null, fg: P.ink }), 0, 2.29, 0.026));
  },
  signBoard(o) {
    const w = o.w || 1.6, h = o.h || 0.8, y = o.height ?? 1.0, g = grp(at(box(w + 0.08, h + 0.08, 0.06, o.frame || P.navy, { outline: 0.01 }), 0, y + h / 2 + 0.04, 0),
      at(label(o.text || 'SIGN', w, h, { bg: o.bg || P.paper, fg: o.fg || P.redDark }), 0, y + h / 2 + 0.04, 0.032));
    if (o.posts !== false && y > 0) [-1, 1].forEach(s => g.add(at(box(0.08, y + h, 0.08, P.woodDark, { pivot: 'bottom' }), s * w * 0.35, 0, -0.07)));
    return g;
  },
  priceTag(o) {
    const tag = grp(at(box(0.42, 0.24, 0.012, P.paper, { outline: 0.03 }), 0.06, 0, 0), at(box(0.17, 0.17, 0.012, P.paper), -0.15, 0, 0, 0, 0, PI / 4),
      at(cyl(0.025, 0.025, 0.014, P.ink, 8), -0.17, 0, 0, PI / 2), at(label(o.text || '$5', 0.32, 0.2, { bg: null, fg: P.red }), 0.08, 0, 0.008));
    tag.position.set(0.05, 0.18, 0); tag.rotation.z = 0.12;
    const g = grp(tag, rod([-0.1, 0.17, 0], [-0.22, 0.42, 0], 0.005, P.ink)); g.userData.grip = [-0.22, 0.42, 0]; return g;
  },
  soldSign() {
    const g = grp(box(0.08, 1.6, 0.08, P.white, { pivot: 'bottom', outline: 0.03 }), at(box(0.95, 0.07, 0.07, P.white), 0.44, 1.55, 0),
      rod([0.15, 1.52, 0], [0.15, 1.42, 0], 0.008, P.ink), rod([0.75, 1.52, 0], [0.75, 1.42, 0], 0.008, P.ink),
      at(box(0.82, 0.46, 0.04, P.red, { outline: 0.02 }), 0.45, 1.19, 0));
    [-1, 1].forEach(s => g.add(at(label('SOLD', 0.74, 0.38, { bg: P.red, fg: P.white }), 0.45, 1.19, s * 0.022, 0, s > 0 ? 0 : PI, 0)));
    return g;
  },
  cardboardBox(o) {
    const w = 0.6, h = 0.45, d = 0.5, t = 0.02, C = '#C49A66', g = grp(at(box(w, t, d, C), 0, t / 2, 0), at(box(w - 0.04, 0.004, d - 0.04, P.woodDark), 0, t + 0.002, 0),
      at(box(w, h, t, C, { outline: 0.02 }), 0, h / 2, d / 2), at(box(w, h, t, C), 0, h / 2, -d / 2), at(box(t, h, d, C), w / 2, h / 2, 0), at(box(t, h, d, C), -w / 2, h / 2, 0));
    const flap = (px, pz, cx, cz, rx, rz, fw, fd) => { const p = grp(at(box(fw, t, fd, C), cx, 0, cz)); p.position.set(px, h, pz); p.rotation.set(rx, 0, rz); g.add(p); };
    flap(0, d / 2, 0, 0.11, 0.55, 0, w, 0.22); flap(0, -d / 2, 0, -0.11, -0.4, 0, w, 0.22); flap(w / 2, 0, 0.1, 0, 0, -0.5, 0.2, d); flap(-w / 2, 0, -0.1, 0, 0, 0.6, 0.2, d);
    const txt = o.text ?? 'SPARE CHANGE?';
    if (txt) { const s = grp(at(box(0.6, 0.42, 0.015, C, { pivot: 'bottom' }), 0, 0, 0), at(label(txt, 0.54, 0.36, { bg: '#D8B582', fg: P.ink }), 0, 0.21, 0.009));
      s.position.set(0, 0, d / 2 + 0.25); s.rotation.x = -0.36; g.add(s); }
    return g;
  },
  streetLamp(o) {
    const H = o.height || 4.2, on = !!o.on;
    const g = grp(cyl(0.07, 0.1, H, P.navy, 6, { pivot: 'bottom' }), cyl(0.16, 0.2, 0.4, P.navy, 6, { pivot: 'bottom' }), at(box(0.9, 0.07, 0.07, P.navy), 0.42, H - 0.05, 0),
      at(box(0.5, 0.14, 0.3, P.navy, { taper: 0.8 }), 0.85, H - 0.06, 0), at(box(0.4, 0.03, 0.22, on ? '#FFE3A0' : P.creamDark, on ? { emissive: '#FFD27A', noGrain: true } : {}), 0.85, H - 0.145, 0));
    if (on && o.glow !== false) { const c = noShadow(new THREE.Mesh(new THREE.ConeGeometry(1.5, H - 0.2, 12, 1, true), new THREE.MeshBasicMaterial({ color: '#FFE2A0', transparent: true, opacity: 0.09, depthWrite: false, side: THREE.DoubleSide })));
      g.add(at(c, 0.85, (H - 0.2) / 2, 0)); }
    if (on && o.light) { const l = new THREE.PointLight('#FFD9A0', o.light === true ? 6 : o.light, 9, 1.4); l.position.set(0.85, H - 0.35, 0); g.add(l); }
    g.userData.lamp = [0.85, H - 0.15, 0]; return g;
  },
  trafficCone() {
    return grp(box(0.42, 0.04, 0.42, ORANGE, { pivot: 'bottom' }), at(cyl(0.035, 0.17, 0.62, ORANGE, 8, { pivot: 'bottom' }), 0, 0.04, 0), at(cyl(0.093, 0.119, 0.12, P.white, 8), 0, 0.35, 0));
  },
  fireHydrant() {
    return grp(cyl(0.16, 0.18, 0.06, P.red, 8, { pivot: 'bottom' }), at(cyl(0.12, 0.12, 0.47, P.red, 8, { pivot: 'bottom' }), 0, 0.06, 0), at(cyl(0.145, 0.145, 0.05, P.redDark, 8), 0, 0.53, 0),
      at(sphere(0.12, P.red, 1), 0, 0.56, 0), at(cyl(0.03, 0.04, 0.07, P.redDark, 6), 0, 0.69, 0),
      at(cyl(0.05, 0.05, 0.14, P.redDark, 6), 0.13, 0.38, 0, 0, 0, PI / 2), at(cyl(0.05, 0.05, 0.14, P.redDark, 6), -0.13, 0.38, 0, 0, 0, PI / 2), at(cyl(0.065, 0.065, 0.1, P.redDark, 8), 0, 0.33, 0.13, PI / 2));
  },
  mailbox(o) {
    const c = o.color || P.navy;
    return grp(box(0.08, 1.0, 0.08, P.woodDark, { pivot: 'bottom' }), at(box(0.24, 0.16, 0.5, c, { outline: 0.02 }), 0, 1.08, 0),
      at(mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.5, 8, 1, false, PI / 2, PI), mat(c)), 0, 1.16, 0, PI / 2), at(box(0.2, 0.2, 0.01, P.cream), 0, 1.13, 0.252),
      at(box(0.03, 0.22, 0.03, P.red), 0.14, 1.2, 0.05), at(box(0.03, 0.09, 0.13, P.red), 0.14, 1.27, 0.0));
  },
  trashCan(o) {
    const c = o.color || '#7E8A84';
    const g = grp(cyl(0.26, 0.22, 0.75, c, 8, { pivot: 'bottom' }), at(cyl(0.29, 0.29, 0.06, P.greyDark, 8), 0, 0.78, 0), at(box(0.12, 0.04, 0.04, P.ink), 0, 0.83, 0));
    for (let i = 0; i < 4; i++) { const a = i * TAU / 4 + PI / 8; g.add(at(box(0.04, 0.7, 0.02, P.greyDark), Math.sin(a) * 0.245, 0.38, Math.cos(a) * 0.245, -0.05 * 0, a, 0)); }
    return g;
  },
  bush(o) {
    const r = rng(o.seed || 5), g = grp(), cols = [P.green, '#7FA86A', '#5F8F63'];
    [[0, 0.45], [0.38, 0.34], [-0.36, 0.3]].forEach(([x, s], i) => { const m = at(sphere(s, cols[i], 0), x, s * 0.7, (r() - 0.5) * 0.2, r(), r(), r()); m.scale.y = 0.8; g.add(m); });
    return g;
  },
  tree(o) {
    const r = rng(o.seed || 7), c = o.color || P.green, s = 0.85 + r() * 0.35;
    const g = grp(cyl(0.1, 0.15, 1.3 * s, P.woodDark, 6, { pivot: 'bottom' }));
    const top = at(sphere(0.9 * s, c, 0), 0, 1.9 * s, 0, r(), r(), r()); top.scale.y = 1.1; g.add(top, at(sphere(0.55 * s, '#7FA86A', 0), 0.35 * s, 2.45 * s, 0.1, r(), r(), r()), at(sphere(0.5 * s, '#5F8F63', 0), -0.45 * s, 1.75 * s, 0.25, r(), r(), r()));
    return g;
  },
  acaciaTree(o) {
    const r = rng(o.seed || 11), h = 3.0 + r() * 1.2, top = [0.1, h * 0.55, 0], g = grp(rod([0, 0, 0], top, 0.13, P.woodDark));
    const tips = [[-1.1, h * 0.92, 0.3], [1.0, h * 0.95, -0.2], [0.2, h, 0.6]];
    tips.forEach(p => g.add(rod(top, p, 0.06, P.woodDark)));
    [[0, h + 0.05, 0, 1.8, 0.32, '#7E9658'], [-0.6, h + 0.3, 0.2, 1.1, 0.26, '#91A866'], [0.7, h + 0.25, -0.2, 1.0, 0.24, '#869E5E']].forEach(([x, y, z, rad, th, c]) => g.add(at(cyl(rad, rad * 1.08, th, c, 7), x, y, z, 0, r() * TAU, 0)));
    return g;
  },
  plant(o) {
    const r = rng(o.seed || 13), g = grp(box(0.32, 0.38, 0.32, o.pot || P.red, { pivot: 'bottom', taper: 1.25 }), at(box(0.44, 0.06, 0.44, P.redDark), 0, 0.4, 0), at(box(0.38, 0.02, 0.38, P.woodDark), 0, 0.42, 0));
    for (let i = 0; i < 8; i++) { const p = grp(at(box(0.1, 0.55 + r() * 0.3, 0.025, [P.green, P.teal, '#7FA86A'][i % 3], { pivot: 'bottom', taper: { x: 0.15, z: 1 } }), 0, 0, 0, 0.3 + r() * 0.4)); p.position.y = 0.42; p.rotation.y = i * TAU / 8 + r() * 0.3; g.add(p); }
    return g;
  },
  cloud(o) {
    const r = rng(o.seed || 17), c = grp(at(box(2.2, 0.6, 1.0, P.white), 0, 0.3, 0), at(box(1.3, 0.5, 0.85, P.paper), -0.35 + r() * 0.2, 0.8, 0.05), at(box(1.0, 0.42, 0.75, P.white), 0.5 + r() * 0.2, 0.7, -0.05), at(box(0.8, 0.35, 0.7, P.paper), -1.1, 0.45, 0.02));
    c.scale.setScalar(o.scale || 1); return grp(c);
  },
  moon(o) {
    const R = o.radius || 1, m = at(sphere(R, P.cream, 1, { emissive: '#6B6550' }), 0, R, 0), g = grp(m);
    [[0.3, 0.35, 1], [-0.4, -0.1, 1], [0.1, -0.45, 1]].forEach(([x, y, z], i) => { const d = new THREE.Vector3(x, y, z).normalize(), c = sphere(R * (0.16 + i * 0.04), P.creamDark, 0, { emissive: '#4F4A3A' });
      c.position.copy(d).multiplyScalar(R * 0.93); c.position.y += R; c.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), d); c.scale.z = 0.35; g.add(c); });
    return noShadow(g);
  },
  stars(o) {
    const n = o.count || 220, R = o.radius || 60, r = rng(o.seed || 31), mk = (cnt, size) => {
      const pos = new Float32Array(cnt * 3);
      for (let i = 0; i < cnt; i++) { const y = R * (0.06 + 0.94 * r()), a = r() * TAU, rx = Math.sqrt(R * R - y * y); pos.set([Math.cos(a) * rx, y, Math.sin(a) * rx], i * 3); }
      const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
      return new THREE.Points(geo, new THREE.PointsMaterial({ color: '#FFF4D6', size: R * size, sizeAttenuation: true, fog: false }));
    };
    return grp(mk(Math.floor(n * 0.8), 0.0032), mk(Math.ceil(n * 0.2), 0.006));
  },
  crown() {
    const g = grp(cyl(0.15, 0.14, 0.11, P.yellow, 8, { pivot: 'bottom', open: true, doubleSide: true }));
    for (let i = 0; i < 8; i++) { const a = i * TAU / 8 + PI / 8; g.add(at(box(0.1, 0.13, 0.025, P.yellow, { pivot: 'bottom', taper: { x: 0.05, z: 1 } }), Math.sin(a) * 0.14, 0.11, Math.cos(a) * 0.14, 0, a, 0));
      if (i % 2 === 0) g.add(at(box(0.04, 0.04, 0.02, i % 4 ? P.teal : P.red), Math.sin(a) * 0.15, 0.055, Math.cos(a) * 0.15, 0, a, 0)); }
    g.userData.grip = [0, 0.05, 0.14]; return g;
  },
  // --- FX -------------------------------------------------------------------------
  explosionBurst(o) {
    const piv = grp(), c = o.size || 1.1, layers = [[P.ink, 1.07, -0.02], [P.red, 1.0, 0], [ORANGE, 0.76, 0.02], [P.yellow, 0.56, 0.04], [P.paper, 0.3, 0.06]];
    // same seed per layer -> concentric, aligned spikes
    layers.forEach(([col, R, z], i) => piv.add(at(noShadow(new THREE.Mesh(new THREE.ShapeGeometry(starShape(11, R, R * 0.58, rng((o.seed || 41) + (i > 1 ? i : 0)))), fxMat(col))), 0, 0, z)));
    piv.position.y = c; const g = grp(piv); g.userData.center = [0, c, 0];
    g.userData.update = t => { const s = ease.outBack(clamp01(t / 0.35)) * (1 + 0.05 * Math.sin(t * 25)); piv.scale.setScalar(Math.max(0.001, s) * c); piv.rotation.z = t * 0.4; piv.children.forEach((m, i) => { if (i > 1) m.rotation.z = (i % 2 ? -1 : 1) * t * 0.3; }); };
    g.userData.update(o.t ?? 1); return g;
  },
  speedLines(o) {
    const r = rng(o.seed || 43), n = o.count || 7, len = o.length || 2.4, dir = o.dir || 1, lines = [];
    const g = grp(); for (let i = 0; i < n; i++) { const m = noShadow(new THREE.Mesh(new THREE.BoxGeometry(len * (0.4 + r() * 0.5), 0.03, 0.03), fxMat(o.color || P.white, 0.9))); m.position.set(0, 0.2 + r() * 1.6, (r() - 0.5) * 0.6); g.add(m); lines.push({ m, ph: r(), sp: 1.5 + r() * 1.5 }); }
    g.userData.update = t => lines.forEach(({ m, ph, sp }) => { const f = (t * sp + ph) % 1; m.position.x = -dir * (f - 0.5) * len; m.scale.x = 0.05 + Math.sin(PI * f); });
    g.userData.update(0); return g;
  },
  dustPuff(o) {
    const r = rng(o.seed || 47), per = o.period || 1.2, puffs = [], g = grp();
    for (let i = 0; i < 7; i++) { const m = sphere(0.16 + r() * 0.06, o.color || '#D8CFBA', 0, { unique: true, opacity: 0.99 }); m.castShadow = false; const a = i / 7 * TAU + r() * 0.5; puffs.push({ m, dx: Math.cos(a), dz: Math.sin(a) * 0.6, d: 0.4 + r() * 0.4 }); g.add(m); }
    g.userData.update = t => { const p = o.once ? clamp01(t / per) : (t % per) / per, e = ease.out(p);
      puffs.forEach(({ m, dx, dz, d }) => { m.position.set(dx * d * e, 0.12 + 0.35 * p, dz * d * e); m.scale.setScalar(0.4 + 1.1 * e); m.material.opacity = 1 - p * p; }); };
    g.userData.update(0.3); return g;
  },
  sweatDrop(o) {
    const piv = grp(), drop = at(sphere(0.07, '#9FD3E8', 1), 0, 0.07, 0), tip = at(new THREE.Mesh(new THREE.ConeGeometry(0.052, 0.1, 8), mat('#9FD3E8')), 0, 0.16, 0);
    drop.scale.z = 0.6; tip.scale.z = 0.6; addOutline(drop, 0.08);
    piv.add(drop, tip, at(box(0.02, 0.04, 0.01, P.white, { noGrain: true }), -0.025, 0.09, 0.045, 0, 0, 0.4)); piv.scale.setScalar(o.scale || 1.6);
    const g = grp(piv); g.userData.update = t => { piv.position.y = -((t * 0.6) % 1) * 0.12; }; return g;
  },
  zzz() {
    const g = grp(), zs = [0.22, 0.32, 0.42].map((s, i) => { const z = glyph('Z', P.white, s); g.add(z); return { z, i }; });
    g.userData.update = t => zs.forEach(({ z, i }) => { const p = (t * 0.45 + i / 3) % 1; z.position.set(i * 0.18 + Math.sin(t * 2 + i) * 0.04, 0.15 + p * 0.9, 0); z.scale.setScalar(0.5 + 0.7 * p); z.children.forEach(c => c.material.opacity = Math.min(1, Math.min(p * 5, (1 - p) * 4))); z.children.forEach(c => c.material.transparent = true); });
    g.userData.update(0); g.userData.center = [0.2, 0.6, 0]; return g;
  },
  questionMark() {
    const s = glyph('?', P.yellow, 0.75), g = grp(at(s, 0, 0.38, 0));
    g.userData.update = t => { s.rotation.z = Math.sin(t * 3) * 0.12; s.position.y = 0.38 + Math.sin(t * 2.4) * 0.03; }; g.userData.center = [0, 0.38, 0]; return g;
  },
  exclamationMark() {
    const s = glyph('!', P.red, 0.75), g = grp(at(s, 0, 0.38, 0));
    g.userData.update = t => { s.scale.setScalar(1 + 0.08 * Math.max(0, Math.sin(t * 9))); }; g.userData.center = [0, 0.38, 0]; return g;
  },
  heart(o) {
    const s = new THREE.Shape(); s.moveTo(25, 25); s.bezierCurveTo(25, 25, 20, 0, 0, 0); s.bezierCurveTo(-30, 0, -30, 35, -30, 35); s.bezierCurveTo(-30, 55, -10, 77, 25, 95);
    s.bezierCurveTo(60, 77, 80, 55, 80, 35); s.bezierCurveTo(80, 35, 80, 0, 50, 0); s.bezierCurveTo(35, 0, 25, 25, 25, 25);
    const geo = new THREE.ExtrudeGeometry(s, { depth: 18, bevelEnabled: false, curveSegments: 4 }); geo.center(); geo.rotateZ(PI); geo.scale(0.006, 0.006, 0.006);
    const h = mesh(geo, mat(o.color || P.red, { emissive: '#3A0C08' })); addOutline(h, 0.06);
    const piv = grp(h); piv.position.y = 0.32; const g = grp(piv); g.userData.center = [0, 0.32, 0];
    g.userData.update = t => piv.scale.setScalar(1 + 0.14 * Math.pow(Math.max(0, Math.sin(t * 7)), 4)); return g;
  },
  // --- outdoor big set pieces ---------------------------------------------------
  tornado(o) {
    const g = grp(), r = rng(o.seed || 5), rings = [], chips = [], N = 10, H = o.height || 5.5, cols = ['#8E9B8B', '#A9B4A2', '#7A8778', '#B8C1AE'];
    const rad = i => 0.25 + Math.pow(i / N, 1.4) * 1.9;
    for (let i = 0; i < N; i++) {
      const m = cyl(rad(i + 1) + 0.12, rad(i), H / N * 1.3, cols[i % 4], 7, { open: true, doubleSide: true, pivot: 'bottom' });
      const piv = grp(m); piv.position.y = i * H / N; piv.rotation.z = (r() - 0.5) * 0.12; g.add(piv);
      rings.push({ piv, m, sp: (3 + r() * 2.5) * (1 - i * 0.045) * (i % 3 === 1 ? 0.6 : 1), ph: r() * TAU, i });
    }
    for (let i = 0; i < 16; i++) { const y = 0.4 + r() * H * 0.9, R = rad(y / H * N) + 0.35 + r() * 0.7;
      const m = box(0.1 + r() * 0.18, 0.04, 0.08 + r() * 0.14, i % 3 ? P.red : P.white); g.add(m); chips.push({ m, y, R, a: r() * TAU, w: 2.2 + r() * 1.8, ph: r() * TAU }); }
    g.userData.update = t => {
      rings.forEach(({ piv, m, sp, ph, i }) => { m.rotation.y = t * sp + ph; piv.position.x = Math.sin(t * 1.6 + i * 0.45) * 0.2 * (i / N); piv.position.z = Math.cos(t * 1.3 + i * 0.5) * 0.12 * (i / N); });
      chips.forEach(({ m, y, R, a, w, ph }) => { const ang = a + t * w; m.position.set(Math.cos(ang) * R, y + Math.sin(t * 2 + ph) * 0.2, Math.sin(ang) * R); m.rotation.set(t * 3 + ph, t * 2, ph); });
    };
    g.userData.update(0); return g;
  },
  vacuum(o) {
    const c = o.color || P.red, N = P.navy;
    const g = grp(at(box(0.4, 0.08, 0.26, c, { outline: 0.02 }), 0, 0.05, 0.06), at(box(0.36, 0.025, 0.04, P.ink), 0, 0.0125, 0.18), // floor nozzle + brush strip
      at(cyl(0.05, 0.05, 0.05, P.ink, 8), -0.17, 0.05, -0.1, 0, 0, PI / 2), at(cyl(0.05, 0.05, 0.05, P.ink, 8), 0.17, 0.05, -0.1, 0, 0, PI / 2), // wheels
      at(box(0.12, 0.06, 0.1, P.greyDark), 0, 0.1, -0.06),                                     // pivot joint
      at(box(0.27, 0.52, 0.19, c, { pivot: 'bottom', taper: { x: 0.85, z: 0.8 }, outline: 0.015 }), 0, 0.13, -0.06), // upright body
      at(box(0.16, 0.24, 0.02, P.tealPale), 0, 0.36, 0.035), at(box(0.18, 0.03, 0.022, N), 0, 0.5, 0.034), // dust bin window + band
      rod([0, 0.64, -0.06], [0, 0.98, -0.06], 0.02, N), at(box(0.04, 0.12, 0.05, N), 0, 1.0, -0.06),  // handle shaft + grip
      at(box(0.14, 0.035, 0.05, N), 0, 1.04, -0.06),                                           // T handle
      mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([[0, 0.16, -0.15], [0, 0.3, -0.24], [0, 0.6, -0.22], [0, 0.85, -0.14], [0, 0.9, -0.08]].map(v => new THREE.Vector3(...v))), 20, 0.022, 6), mat(N)));
    g.userData.grip = [0, 0.94, -0.06]; return g; // on the grip; with the director's -0.1 hand offset the nozzle rests at floor level in idle
  },
  newspaper(o) {
    const pg = canvasPlane(0.32, 0.44, (c, W, H) => { c.fillStyle = P.paper; c.fillRect(0, 0, W, H); c.fillStyle = P.ink; c.textAlign = 'center'; c.font = `900 ${W * 0.11}px Georgia, serif`; c.fillText(o.title || 'LE JOURNAL', W / 2, H * 0.1);
      c.fillRect(W * 0.05, H * 0.13, W * 0.9, 3); c.font = `bold ${W * 0.085}px Arial`; c.fillText(o.headline || 'INCROYABLE !', W / 2, H * 0.22);
      c.fillStyle = '#9AA0A0'; c.fillRect(W * 0.05, H * 0.27, W * 0.42, H * 0.2);
      c.fillStyle = '#555'; for (let i = 0; i < 16; i++) c.fillRect(i < 6 ? W * 0.52 : W * 0.05, H * (0.28 + (i < 6 ? i : i - 6 + 4.2) * 0.045), (i < 6 ? W * 0.43 : W * 0.9) * (i % 4 === 3 ? 0.6 : 1), 4); }, { res: 256 });
    const g = grp(at(box(0.33, 0.012, 0.45, '#E9E3D3'), 0, 0.006, 0), at(box(0.33, 0.012, 0.45, P.paper), 0.004, 0.018, -0.004, 0, 0.03, 0), at(pg, 0.004, 0.0245, -0.004, -PI / 2, 0, 0.03));
    g.userData.grip = [0.12, 0.012, 0.2]; return g;
  },
  scarecrow() {
    const hay = P.yellow, g = grp(box(0.09, 1.95, 0.09, P.woodDark, { pivot: 'bottom' }), at(box(1.5, 0.08, 0.08, P.woodDark), 0, 1.45, -0.02),
      at(box(0.5, 0.62, 0.26, P.red, { pivot: 'bottom', taper: { x: 1.15, z: 1 }, outline: 0.012 }), 0, 0.95, 0), at(box(0.13, 0.13, 0.01, P.teal), 0.1, 1.15, 0.135, 0, 0, 0.2),
      at(box(1.15, 0.13, 0.15, P.red), 0, 1.45, 0), at(box(0.52, 0.28, 0.27, P.navy, { pivot: 'bottom' }), 0, 0.72, 0),
      at(sphere(0.2, P.creamDark, 1), 0, 1.78, 0), at(box(0.05, 0.05, 0.02, P.ink), -0.07, 1.82, 0.19), at(box(0.05, 0.05, 0.02, P.ink), 0.07, 1.82, 0.19), at(box(0.16, 0.025, 0.02, P.ink), 0, 1.71, 0.19),
      at(cyl(0.38, 0.38, 0.03, P.wood, 10), 0, 1.93, 0), at(cyl(0.14, 0.2, 0.2, P.wood, 8, { pivot: 'bottom' }), 0, 1.94, 0), at(cyl(0.205, 0.205, 0.04, P.red, 8), 0, 1.97, 0));
    [-1, 1].forEach(sd => { for (let i = 0; i < 3; i++) g.add(at(box(0.16, 0.025, 0.025, hay), sd * 0.66, 1.42 + (i - 1) * 0.035, 0.03, 0, 0, sd * (i - 1) * 0.35)); });
    for (let i = 0; i < 5; i++) g.add(at(box(0.025, 0.16, 0.025, hay, { pivot: 'top' }), -0.16 + i * 0.08, 0.74, 0.1, 0, 0, (i - 2) * 0.15));
    return g;
  },
  glassDome(o) {
    const r = o.radius || 0.75, h = o.height || 2.2, hc = h - r * 0.8, y0 = o.base === false ? 0 : 0.08, gm = glassMat(o.opacity || 0.25);
    const wall = at(new THREE.Mesh(new THREE.CylinderGeometry(r, r, hc, 16, 1, true), gm), 0, y0 + hc / 2, 0);
    const cap = at(new THREE.Mesh(new THREE.SphereGeometry(r, 16, 6, 0, TAU, 0, PI / 2), gm), 0, y0 + hc, 0); cap.scale.y = 0.8;
    const g = grp(wall, cap, at(new THREE.Mesh(new THREE.SphereGeometry(0.07, 8, 4), gm), 0, y0 + h + 0.04, 0));
    if (y0) g.add(cyl(r + 0.08, r + 0.12, y0, P.woodDark, 16, { pivot: 'bottom' }));
    const hi = new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: 0.55, depthWrite: false });
    [[-0.55, 0.06, 0.8], [-0.35, 0.03, 0.55]].forEach(([a, w, k]) => g.add(at(new THREE.Mesh(new THREE.BoxGeometry(w, hc * k, 0.005), hi), Math.sin(a) * (r + 0.01), y0 + hc * 0.5, Math.cos(a) * (r + 0.01), 0, a, 0)));
    g.children.forEach(c => { c.castShadow = false; }); return g;
  },
  // ---- additions for "gorille" episode ----------------------------------------------------
  rock(o) { // faceted boulder (enclosure rock, the gorilla hides behind it)
    const sz = o.size || 1.2; const m = new THREE.Mesh(new THREE.DodecahedronGeometry(sz * 0.6, 0), mat(o.color || '#8E918C'));
    m.scale.set(1.3, 0.8, 1); m.position.y = sz * 0.42; m.castShadow = m.receiveShadow = true; return grp(m);
  },
  syringe(o) {
    const g = grp(at(cyl(0.025, 0.025, 0.16, '#E8F2F2', 8, { opacity: 0.8 }), 0, 0.08, 0), at(cyl(0.02, 0.02, 0.1, P.yellow, 8), 0, 0.07, 0),
      at(cyl(0.004, 0.004, 0.08, P.grey, 4), 0, -0.04, 0), at(box(0.07, 0.008, 0.02, P.grey), 0, 0.16, 0), at(cyl(0.006, 0.006, 0.06, P.grey, 4), 0, 0.19, 0));
    g.userData.grip = [0, 0.1, 0]; return g;
  },
  preWorkout(o) { // tub with a loud label
    const g = grp(at(cyl(0.11, 0.11, 0.24, o.color || P.black, 12), 0, 0.12, 0), at(cyl(0.115, 0.115, 0.05, P.red, 12), 0, 0.245, 0),
      at(label(o.text || 'PRE-WORKOUT', 0.2, 0.1, { bg: P.yellow, fg: P.black }), 0, 0.13, 0.112));
    g.userData.grip = [0, 0.12, 0]; return g;
  },
  steroidVial(o) { const g = grp(at(cyl(0.03, 0.03, 0.09, '#CDE8F0', 8, { opacity: 0.85 }), 0, 0.045, 0), at(cyl(0.032, 0.032, 0.02, P.red, 8), 0, 0.1, 0), at(label(o.text || 'STÉROÏDES', 0.07, 0.035, { bg: P.white, fg: P.red }), 0, 0.045, 0.031)); g.userData.grip = [0, 0.05, 0]; return g; },
  foodSack(o) { // big kibble sack
    const g = grp(at(box(0.55, 0.75, 0.25, o.color || '#C9A86A', { pivot: 'bottom', taper: { x: 0.85, z: 0.7 }, outline: 0.01 }), 0, 0, 0),
      at(label(o.text || 'HIGH PROTEIN', 0.46, 0.3, { bg: P.red, fg: P.white }), 0, 0.42, 0.128));
    return g;
  },
  eggs(o) { const g = grp(at(box(0.32, 0.06, 0.12, '#B9A27A', { pivot: 'bottom' }), 0, 0, 0)); for (let i = 0; i < 6; i++) g.add(at(sphere(0.026, P.paper, 1), -0.12 + (i % 3) * 0.12 + (i > 2 ? 0 : 0), 0.08, i > 2 ? 0.03 : -0.03)); return g; },
  barbell(o) {
    const w = o.width || 1.6, g = grp(rod([-w / 2, 0, 0], [w / 2, 0, 0], 0.016, P.grey));
    [-1, 1].forEach(sd => { for (let i = 0; i < (o.plates || 3); i++) g.add(at(cyl(0.2 - i * 0.03, 0.2 - i * 0.03, 0.05, i % 2 ? P.red : P.ink, 12), sd * (w / 2 - 0.12 - i * 0.055), 0, 0, 0, 0, Math.PI / 2)); });
    g.userData.grip = [w * 0.18, 0, 0]; return g;
  },
  dumbbell(o) { const g = grp(rod([-0.14, 0, 0], [0.14, 0, 0], 0.014, P.grey)); [-1, 1].forEach(sd => g.add(at(cyl(0.07, 0.07, 0.07, o.color || P.ink, 10), sd * 0.13, 0, 0, 0, 0, Math.PI / 2))); g.userData.grip = [0, 0, 0]; return g; },
  glasses(o) { // wire glasses to stick on a face (origin = bridge)
    const g = grp(); const r = o.r || 0.05, dx = o.dx || 0.065;
    [-1, 1].forEach(sd => { g.add(at(torus(r, 0.006, P.ink, 4, 12), sd * dx, 0, 0)); g.add(rod([sd * (dx + r), 0, 0], [sd * (dx + r + 0.01), 0, -0.12], 0.005, P.ink)); });
    g.add(rod([-dx + r, 0, 0], [dx - r, 0, 0], 0.005, P.ink)); return g;
  },
  porkpieHat(o) { // the chemist's black hat
    const g = grp(at(cyl(o.r || 0.24, o.r || 0.24, 0.02, P.ink, 16), 0, 0.01, 0), at(cyl((o.r || 0.24) * 0.66, (o.r || 0.24) * 0.7, 0.12, P.ink, 16, { pivot: 'bottom' }), 0, 0.02, 0),
      at(cyl((o.r || 0.24) * 0.71, (o.r || 0.24) * 0.71, 0.03, '#3A3D44', 16, { pivot: 'bottom' }), 0, 0.02, 0)); return g;
  },
  censorBar(o) { // TV-style censor block (nudity gag)
    const w = o.w || 0.42, h = o.h || 0.2; const g = grp(at(box(w, h, 0.02, P.black), 0, 0, 0));
    const n = 6; for (let i = 0; i < n; i++) for (let j = 0; j < 3; j++) if ((i + j) % 2) g.add(at(box(w / n, h / 3, 0.022, '#2A2A2E'), -w / 2 + w / n * (i + 0.5), -h / 2 + h / 3 * (j + 0.5), 0));
    return g;
  },
  zooFence(o) { // low wall + bars in front of an enclosure
    const L = o.length || 8, g = grp(at(box(L, 0.7, 0.3, '#B7B2A6', { pivot: 'bottom', outline: 0.004 }), 0, 0, 0));
    for (let x = -L / 2 + 0.15; x <= L / 2; x += 0.3) g.add(at(box(0.04, 0.9, 0.04, P.ink, { pivot: 'bottom' }), x, 0.7, 0));
    g.add(at(box(L, 0.05, 0.06, P.ink), 0, 1.6, 0)); return g;
  },
  // discreet in-world watermark: looks like a real poster / sticker / street sign of the set (muted colours, small)
  wmSign(o) {
    const text = o.text || 'Follow @drkurtcobaye', kind = o.kind || 'poster';
    const bg = o.bg || '#EFE6CF', fg = o.fg || '#2E4563';
    if (kind === 'stand') { // small sign on a post (outdoor)
      const g = grp(at(box(0.05, 1.0, 0.05, P.greyDark, { pivot: 'bottom' }), 0, 0, 0), at(box(0.72, 0.3, 0.03, P.greyDark), 0, 1.1, 0), at(label(text, 0.68, 0.26, { bg, fg }), 0, 1.1, 0.017));
      return g;
    }
    if (kind === 'sticker') return grp(at(label(text, 0.36, 0.12, { bg, fg }), 0, 0, 0));
    // poster: paper with a thin border, slightly rotated like it was taped on
    const g = grp(at(box(0.62, 0.42, 0.01, fg), 0, 0, 0), at(label(text, 0.58, 0.38, { bg, fg }), 0, 0, 0.006));
    g.rotation.z = o.tilt ?? -0.04; return g;
  },
  stopwatch(o) { // brass pocket stopwatch; opts.broken -> cracked glass, bent crown, spring popping out
    const g = grp(at(cyl(0.07, 0.07, 0.025, P.yellow, 16), 0, 0, 0, Math.PI / 2), at(cyl(0.06, 0.06, 0.027, P.paper, 16), 0, 0, 0.002, Math.PI / 2),
      at(box(0.004, 0.045, 0.004, P.ink), 0, 0.018, 0.016), at(cyl(0.012, 0.012, 0.03, P.yellow, 8), 0, 0.085, 0), at(torus(0.02, 0.005, P.yellow, 4, 10), 0, 0.11, 0));
    if (o.broken) {
      g.children[3].rotation.z = 0.9; g.children[3].position.x = 0.03;
      for (let i = 0; i < 5; i++) g.add(at(box(0.07, 0.003, 0.002, P.ink), 0, 0, 0.017, 0, 0, i * 0.7));
      for (let i = 0; i < 4; i++) g.add(at(torus(0.012 + i * 0.006, 0.0025, P.grey, 3, 8, Math.PI * 1.5), 0.05 + i * 0.01, 0.05 + i * 0.012, 0.01));
    }
    if (o.taped) for (let i = 0; i < 3; i++) g.add(at(box(0.16, 0.025, 0.004, '#C9B48A', { opacity: 0.85 }), 0, -0.03 + i * 0.03, 0.019, 0, 0, -0.5 + i * 0.5));
    g.userData.grip = [0, 0.11, 0]; return g;
  },
  suggestionBox(o) {
    return grp(at(box(0.45, 0.4, 0.32, P.red, { pivot: 'bottom', outline: 0.01 }), 0, 0.9, 0), at(box(0.2, 0.02, 0.01, P.ink), 0, 1.25, 0.161),
      at(box(0.05, 0.9, 0.05, P.ink, { pivot: 'bottom' }), 0, 0, 0), at(label(o.text || 'IDÉES', 0.36, 0.12, { bg: P.paper, fg: P.red }), 0, 1.08, 0.162));
  },
  paperPile(o) { const g = grp(), r = rng(o.seed || 3), n = o.count || 40; for (let i = 0; i < n; i++) g.add(at(box(0.21, 0.004, 0.29, P.paper), (r() - 0.5) * 0.04, i * 0.006, (r() - 0.5) * 0.04, 0, (r() - 0.5) * 0.4, 0)); return g; },
  beerGlass(o) { const g = grp(at(cyl(0.04, 0.035, 0.14, '#E8B84A', 10, { opacity: 0.85 }), 0, 0.07, 0), at(cyl(0.042, 0.042, 0.03, P.white, 10), 0, 0.15, 0)); g.userData.grip = [0, 0.07, 0]; return g; },
  barStool(o) { return grp(at(cyl(0.18, 0.18, 0.06, P.red, 12), 0, 0.72, 0), at(cyl(0.03, 0.03, 0.7, P.ink, 6, { pivot: 'bottom' }), 0, 0, 0), at(cyl(0.2, 0.2, 0.03, P.ink, 12), 0, 0.015, 0)); },
  vaultDoor(o) { return grp(at(cyl(1.0, 1.0, 0.3, P.grey, 20, { outline: 0.01 }), 0, 1.05, 0, Math.PI / 2), at(cyl(0.8, 0.8, 0.32, '#9A9C98', 20), 0, 1.05, 0, Math.PI / 2), at(torus(0.25, 0.03, P.ink, 4, 12), 0, 1.05, 0.17), ...[0, 1, 2, 3].map(i => at(box(0.04, 0.5, 0.04, P.ink), 0, 1.05, 0.17, 0, 0, i * Math.PI / 4))); },
  mustache3d(o) { // big hand-drawn-looking handlebar moustache to stick on a face
    const g = grp(); [-1, 1].forEach(sd => { g.add(at(box(0.07, 0.025, 0.012, P.ink), sd * 0.04, 0, 0, 0, 0, sd * 0.25)); g.add(at(box(0.035, 0.018, 0.012, P.ink), sd * 0.085, 0.012, 0, 0, 0, sd * 0.9)); });
    return g;
  },
  // ---- v3 film props ---------------------------------------------------------------------------------
  marker(o) { const g = grp(at(cyl(0.012, 0.012, 0.13, o.color || P.ink, 6), 0, 0.065, 0), at(cyl(0.012, 0.004, 0.025, P.ink, 6), 0, -0.012, 0)); g.userData.grip = [0, 0.07, 0]; return g; },
  coffeeMachine(o) { return grp(at(box(0.5, 1.5, 0.45, P.greyDark, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(0.4, 0.3, 0.02, '#1E2A33'), 0, 1.15, 0.23), at(box(0.22, 0.18, 0.12, P.ink), 0, 0.62, 0.2),
    at(label('CAFÉ', 0.3, 0.1, { bg: P.red, fg: P.white }), 0, 1.38, 0.231), at(cyl(0.04, 0.035, 0.08, P.white, 8), 0, 0.5, 0.2)); },
  beerStream(o) { const h = o.length || 0.45; const m = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.018, h, 8), new THREE.MeshLambertMaterial({ color: '#E6B44A', transparent: true, opacity: 0.85 })); m.position.y = -h / 2; return grp(m); },
  dartboard(o) { const g = grp(); [[0.25, P.ink], [0.2, P.red], [0.14, P.cream], [0.08, P.green], [0.03, P.red]].forEach(([r, c], i) => g.add(at(cyl(r, r, 0.03 + i * 0.004, c, 16), 0, 0, i * 0.004, Math.PI / 2))); return g; },
  dart(o) { return grp(at(cyl(0.006, 0.006, 0.12, P.grey, 5), 0, 0, 0, Math.PI / 2), at(box(0.04, 0.002, 0.04, P.red), 0, 0, -0.07), at(box(0.002, 0.04, 0.04, P.red), 0, 0, -0.07)); },
  beard(o) { // grows by scaling (scale keys): pointed strands hanging from the chin, fanning out
    const g = grp(); const r = rng(o.seed || 5), n = 13;
    for (let i = 0; i < n; i++) { const u = i / (n - 1) - 0.5, len = 0.22 + 0.2 * (1 - Math.abs(u) * 1.6) + r() * 0.05;
      g.add(at(box(0.022, len, 0.02, o.color || '#2A2420', { pivot: 'top', taper: { x: 0.25, z: 0.5 } }), u * 0.2, 0, 0.012 * Math.cos(u * 3) + r() * 0.01, 0.08, 0, -u * 0.55 + (r() - 0.5) * 0.1)); }
    return g; },
  spiderWeb(o) { const g = grp(); const R = o.r || 0.35, m = new THREE.LineBasicMaterial({ color: '#F4F4F0', transparent: true, opacity: 0.8 });
    for (let i = 0; i < 8; i++) { const a = i / 8 * Math.PI * 2; g.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([V3(0, 0, 0), V3(Math.cos(a) * R, Math.sin(a) * R, 0)]), m)); }
    for (let k = 1; k <= 4; k++) { const pts = []; for (let i = 0; i <= 8; i++) { const a = i / 8 * Math.PI * 2, rr = R * k / 4.4; pts.push(V3(Math.cos(a) * rr, Math.sin(a) * rr, 0)); } g.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), m)); }
    return g; },
  coin(o) { return grp(at(cyl(0.025, 0.025, 0.006, P.yellow, 12), 0, 0, 0, Math.PI / 2)); },
  wallClock(o) { // hands spin at opts.rate turns/s (time passing)
    const g = grp(at(cyl(0.32, 0.32, 0.05, P.ink, 20), 0, 0, 0, Math.PI / 2), at(cyl(0.28, 0.28, 0.055, P.paper, 20), 0, 0, 0.004, Math.PI / 2));
    for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2; g.add(at(box(0.015, 0.05, 0.01, P.ink), Math.sin(a) * 0.23, Math.cos(a) * 0.23, 0.03, 0, 0, -a)); }
    const hh = grp(at(box(0.02, 0.15, 0.01, P.ink, { pivot: 'bottom' }), 0, 0, 0)), mh = grp(at(box(0.012, 0.22, 0.01, P.red, { pivot: 'bottom' }), 0, 0, 0));
    hh.position.z = 0.035; mh.position.z = 0.04; g.add(hh, mh);
    const rate = o.rate ?? 1 / 60; g.userData.update = t => { mh.rotation.z = -t * rate * Math.PI * 2; hh.rotation.z = -t * rate * Math.PI * 2 / 12; };
    return g; },
  calendar(o) { // page number flips with time: opts.rate pages/s from opts.start
    const g = grp(at(box(0.42, 0.5, 0.02, P.paper, { outline: 0.004 }), 0, 0, 0), at(box(0.42, 0.1, 0.025, P.red), 0, 0.2, 0.002));
    const pages = []; for (let d = 1; d <= 31; d++) { const p = at(label(String(d), 0.36, 0.3, { bg: P.paper, fg: P.ink }), 0, -0.05, 0.012); p.visible = d === 1; g.add(p); pages.push(p); }
    const rate = o.rate ?? 0, t0 = o.start ?? 0; g.userData.update = t => { const d = Math.min(30, Math.max(0, Math.floor((t - t0) * rate))); pages.forEach((p, i) => p.visible = i === d); };
    return g; },
  whistle(o) { const g = grp(at(box(0.05, 0.025, 0.025, P.yellow), 0, 0, 0), at(cyl(0.016, 0.016, 0.03, P.yellow, 8), 0.025, -0.005, 0, Math.PI / 2)); g.userData.grip = [0, 0, 0]; return g; },
  clipboardProp(o) { const g = grp(at(box(0.24, 0.32, 0.012, P.woodDark), 0, 0, 0), at(box(0.2, 0.26, 0.004, P.paper), 0, -0.01, 0.008), at(box(0.1, 0.03, 0.02, P.grey), 0, 0.15, 0.01)); for (let i = 0; i < 6; i++) g.add(at(box(0.14, 0.006, 0.002, P.ink), 0, 0.08 - i * 0.035, 0.011)); g.userData.grip = [0, -0.1, 0]; return g; },
  binoculars(o) { const g = grp(); [-1, 1].forEach(sd => g.add(at(cyl(0.032, 0.035, 0.12, P.ink, 8), sd * 0.04, 0, 0, Math.PI / 2))); g.add(at(box(0.05, 0.02, 0.04, P.ink), 0, 0, -0.02)); g.userData.grip = [0, 0, 0]; return g; },
  podium(o) { const g = grp(at(box(0.7, 1.1, 0.5, P.navy, { pivot: 'bottom', taper: { x: 0.85, z: 0.85 }, outline: 0.006 }), 0, 0, 0), at(box(0.8, 0.05, 0.55, P.navyLight), 0, 1.12, 0));
    if (o.text) g.add(at(label(o.text, 0.62, 0.3, { bg: P.paper, fg: P.red }), 0, 0.75, 0.24));
    for (const x of [-0.12, 0.12]) g.add(rod([x, 1.14, 0.15], [x * 0.6, 1.42, 0.24], 0.008, P.ink), at(sphere(0.03, P.ink, 0), x * 0.6, 1.44, 0.25));
    return g; },
  chickenBucket(o) { const g = grp(at(cyl(0.16, 0.12, 0.26, P.red, 12, { pivot: 'bottom' }), 0, 0, 0), at(cyl(0.165, 0.165, 0.03, P.white, 12), 0, 0.25, 0));
    for (let i = 0; i < 4; i++) { const a = i * 1.6; g.add(at(box(0.06, 0.08, 0.05, P.sand), Math.cos(a) * 0.06, 0.3, Math.sin(a) * 0.06, 0.3, a, 0)); }
    g.add(at(label(o.text || 'MASTER POULET', 0.26, 0.09, { bg: P.white, fg: P.red }), 0, 0.14, 0.142)); g.userData.grip = [0, 0.12, 0]; return g; },
  drumstick(o) { const g = grp(at(sphere(0.045, P.sand, 1), 0, 0.03, 0), at(cyl(0.012, 0.012, 0.08, P.cream, 6), 0, -0.04, 0)); g.children[0].scale.set(1, 1.4, 1); g.userData.grip = [0, -0.05, 0]; return g; },
  pullUpBar(o) { const h = o.height || 2.35, w = o.width || 1.3; return grp(at(box(0.08, h, 0.08, P.greyDark, { pivot: 'bottom' }), -w / 2, 0, 0), at(box(0.08, h, 0.08, P.greyDark, { pivot: 'bottom' }), w / 2, 0, 0), rod([-w / 2, h - 0.04, 0], [w / 2, h - 0.04, 0], 0.025, P.grey)); },
  mapBoard(o) { const g = grp(at(box(1.6, 1.0, 0.04, '#B98A5A', { outline: 0.004 }), 0, 0, 0), at(box(1.45, 0.85, 0.01, '#DCCFA8'), 0, 0, 0.025));
    const pins = [[-0.5, 0.2], [0.1, 0.25], [0.5, -0.1], [-0.2, -0.25], [0.35, 0.3], [-0.55, -0.2]];
    pins.forEach(([x, y], i) => { g.add(at(sphere(0.025, P.red, 0), x, y, 0.04)); g.add(at(box(0.16, 0.11, 0.005, P.paper), x + 0.1, y - 0.06, 0.03)); });
    const m = new THREE.LineBasicMaterial({ color: P.red }); g.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pins.map(([x, y]) => V3(x, y, 0.045))), m));
    return g; },
  evidenceBag(o) { const g = grp(at(box(0.22, 0.3, 0.02, '#E8F0F0', { opacity: 0.6 }), 0, 0, 0), at(box(0.22, 0.04, 0.025, P.red), 0, 0.14, 0)); if (o.with) { const inner = B[o.with] ? B[o.with]({}) : null; if (inner) { inner.scale.setScalar(0.7); g.add(at(inner, 0, -0.05, 0)); } } g.userData.grip = [0, 0.13, 0]; return g; },
  tumbleweed(o) { const g = grp(); const r = rng(o.seed || 3); for (let i = 0; i < 14; i++) g.add(at(torus(0.18 + r() * 0.08, 0.008, '#A88A55', 3, 10), 0, 0.22, 0, r() * 3, r() * 3, r() * 3)); g.userData.update = t => { g.children.forEach(c => { c.rotation.x = t * 3; }); }; return g; },
  leafFan(o) { const g = grp(at(cyl(0.008, 0.008, 0.4, P.woodDark, 5), 0, 0.2, 0)); for (let i = 0; i < 7; i++) g.add(at(box(0.08, 0.28, 0.01, P.green), Math.sin((i - 3) * 0.3) * 0.12, 0.5 + Math.cos((i - 3) * 0.3) * 0.08, 0, 0, 0, -(i - 3) * 0.3)); g.userData.grip = [0, 0.05, 0]; return g; },
  flag(o) { const c = o.colors || [P.ink, P.yellow, P.red], vertical = o.vertical !== false; const g = grp(at(cyl(0.015, 0.015, 1.6, P.grey, 5, { pivot: 'bottom' }), 0, 0, 0));
    c.forEach((col, i) => g.add(vertical ? at(box(0.6 / c.length, 0.4, 0.01, col), 0.03 + 0.3 / c.length + i * 0.6 / c.length, 1.38, 0) : at(box(0.6, 0.4 / c.length, 0.01, col), 0.33, 1.58 - 0.2 / c.length - i * 0.4 / c.length, 0)));
    if (o.cross) g.add(at(box(0.6, 0.06, 0.012, o.cross), 0.33, 1.38, 0), at(box(0.06, 0.4, 0.012, o.cross), 0.33, 1.38, 0));
    if (o.disc) [-1, 1].forEach(sd => g.add(at(cyl(0.11, 0.11, 0.004, o.disc, 16), 0.33, 1.38, sd * 0.0075, PI / 2))); // Japan: red disc; pirate: white skull disc
    if (o.skull) [-1, 1].forEach(sd => g.add(at(box(0.2, 0.03, 0.004, '#E6B84A'), 0.33, 1.47, sd * 0.009), at(box(0.04, 0.04, 0.004, P.ink), 0.29, 1.39, sd * 0.011), at(box(0.04, 0.04, 0.004, P.ink), 0.37, 1.39, sd * 0.011)));
    if (o.grip) g.userData.grip = [0, 0.4, 0];
    return g; },
  boxHide(o) { // wearable cardboard box (Metal Gear gag): attach to the torso joint, legs stick out underneath
    const w = o.w || 0.8, h = o.h || 1.2, d = o.d || 0.75, c = '#B8925E', g = grp();
    g.add(at(box(w, 0.04, d, c, { outline: 0.006 }), 0, h, 0));
    g.add(at(box(w, h, 0.03, c, { outline: 0.006 }), 0, h / 2, d / 2), at(box(w, h, 0.03, c, { outline: 0.006 }), 0, h / 2, -d / 2), at(box(0.03, h, d, c, { outline: 0.006 }), w / 2, h / 2, 0), at(box(0.03, h, d, c, { outline: 0.006 }), -w / 2, h / 2, 0));
    g.add(at(box(0.36, 0.06, 0.035, P.ink), 0, h * 0.78, d / 2 + 0.002), at(box(w, 0.05, 0.034, '#D8B88A'), 0, h * 0.5, d / 2 + 0.003));
    g.add(at(label(o.text || 'FRAGILE', 0.4, 0.14, { bg: null, fg: P.red }), 0, h * 0.3, d / 2 + 0.02));
    return g; },
  syringeBig(o) { const g = B.syringe(o); g.scale.setScalar(o.k || 2); return g; },
  drawingSheet(o) { // a suggestion sheet with a sketch: opts.kind 'rocket' | 'sub' | 'idea'
    const kind = o.kind || 'rocket';
    const pic = canvasPlane(0.3, 0.42, (c, W, H) => { c.fillStyle = '#F7F3EA'; c.fillRect(0, 0, W, H); c.strokeStyle = '#2C4A8A'; c.fillStyle = '#2C4A8A'; c.lineWidth = W * 0.02; c.lineJoin = 'round';
      if (kind === 'rocket') { c.beginPath(); c.moveTo(W * 0.5, H * 0.12); c.lineTo(W * 0.65, H * 0.4); c.lineTo(W * 0.65, H * 0.72); c.lineTo(W * 0.35, H * 0.72); c.lineTo(W * 0.35, H * 0.4); c.closePath(); c.stroke();
        c.beginPath(); c.arc(W * 0.5, H * 0.45, W * 0.06, 0, 6.3); c.stroke(); c.beginPath(); c.moveTo(W * 0.35, H * 0.6); c.lineTo(W * 0.22, H * 0.78); c.lineTo(W * 0.35, H * 0.72); c.moveTo(W * 0.65, H * 0.6); c.lineTo(W * 0.78, H * 0.78); c.lineTo(W * 0.65, H * 0.72); c.stroke();
        c.strokeStyle = '#B5302A'; c.beginPath(); c.moveTo(W * 0.42, H * 0.76); c.lineTo(W * 0.5, H * 0.92); c.lineTo(W * 0.58, H * 0.76); c.stroke(); }
      else if (kind === 'sub') { c.beginPath(); c.ellipse(W * 0.5, H * 0.55, W * 0.36, H * 0.1, 0, 0, 6.3); c.stroke(); c.strokeRect(W * 0.42, H * 0.36, W * 0.14, H * 0.1); c.beginPath(); c.moveTo(W * 0.49, H * 0.36); c.lineTo(W * 0.49, H * 0.26); c.lineTo(W * 0.56, H * 0.26); c.stroke();
        for (let i = 0; i < 3; i++) { c.beginPath(); c.arc(W * (0.32 + i * 0.12), H * 0.55, W * 0.03, 0, 6.3); c.stroke(); } c.strokeStyle = '#7BC0E8'; for (let i = 0; i < 3; i++) { c.beginPath(); c.moveTo(W * 0.08, H * (0.75 + i * 0.05)); c.quadraticCurveTo(W * 0.5, H * (0.7 + i * 0.05), W * 0.92, H * (0.75 + i * 0.05)); c.stroke(); } }
      else { c.font = `bold ${H * 0.12}px Arial`; c.fillText('IDÉE', W * 0.3, H * 0.2); for (let i = 0; i < 6; i++) c.fillRect(W * 0.12, H * (0.32 + i * 0.09), W * (0.5 + (i % 3) * 0.12), H * 0.02); }
      c.fillStyle = '#B5302A'; c.font = `bold ${H * 0.07}px Arial`; c.fillText(`IDÉE N°${o.num || 312}`, W * 0.08, H * 0.07); });
    const g = grp(at(box(0.31, 0.43, 0.004, P.paper), 0, 0, 0), at(pic, 0, 0, 0.003)); g.userData.grip = [0, -0.18, 0]; return g; },
  squareBall(o) { // "le ballon est carré": a white cube football with black patches
    const s = o.size || 0.22, g = grp(at(box(s, s, s, P.white, { outline: 0.006 }), 0, s / 2, 0));
    [[0, s / 2, s / 2 + 0.002, 0, 0], [0, s / 2, -s / 2 - 0.002, 0, 0], [s / 2 + 0.002, s / 2, 0, 0, Math.PI / 2], [-s / 2 - 0.002, s / 2, 0, 0, Math.PI / 2], [0, s + 0.002, 0, Math.PI / 2, 0]].forEach(([x, y, z, rx, ry]) => g.add(at(box(s * 0.42, s * 0.42, 0.004, P.ink), x, y, z, rx, ry, Math.PI / 4)));
    g.userData.grip = [0, s / 2, 0]; return g; },
  ticketMachine(o) { // bank queue ticket dispenser with a number display
    const g = grp(at(box(0.08, 1.0, 0.08, P.greyDark, { pivot: 'bottom' }), 0, 0, 0), at(box(0.32, 0.4, 0.22, P.red, { outline: 0.008 }), 0, 1.15, 0),
      at(label(o.num || '042', 0.24, 0.1, { bg: P.ink, fg: '#FF5A3A' }), 0, 1.25, 0.112), at(box(0.12, 0.012, 0.03, P.ink), 0, 1.06, 0.112), at(box(0.07, 0.05, 0.004, P.paper), 0, 1.03, 0.115), at(box(0.3, 0.03, 0.3, P.greyDark), 0, 0.015, 0));
    return g; },
  idCard(o) { const c = canvasPlane(0.086, 0.054, (g, W, H) => { g.fillStyle = '#DCE8F2'; g.fillRect(0, 0, W, H); g.fillStyle = '#2C4A8A'; g.fillRect(0, 0, W, H * 0.18); g.fillStyle = '#B9A48A'; g.fillRect(W * 0.07, H * 0.28, W * 0.26, H * 0.58); g.fillStyle = '#3A3A3A'; for (let i = 0; i < 4; i++) g.fillRect(W * 0.4, H * (0.32 + i * 0.14), W * (0.45 - i * 0.06), H * 0.05); }, { res: 128 });
    const g = grp(at(box(0.088, 0.056, 0.002, P.white), 0, 0, 0), at(c, 0, 0, 0.0015)); g.userData.grip = [-0.035, 0, 0]; return g; },
  bill(o) { // "l'addition"
    const c = canvasPlane(0.15, 0.2, (g, W, H) => { g.fillStyle = '#F7F3EA'; g.fillRect(0, 0, W, H); g.fillStyle = '#2A2A2A'; g.textAlign = 'center'; g.font = `bold ${H * 0.1}px Arial`; g.fillText(o.title || 'ADDITION', W / 2, H * 0.14);
      g.font = `${H * 0.052}px Arial`; g.textAlign = 'left'; (o.items || [['1 demi', '4,50'], ['1 godet', '3,00'], ['', '']]).forEach(([a, b], i) => { g.fillText(a, W * 0.08, H * (0.32 + i * 0.12)); g.textAlign = 'right'; g.fillText(b, W * 0.92, H * (0.32 + i * 0.12)); g.textAlign = 'left'; });
      g.fillRect(W * 0.08, H * 0.66, W * 0.84, H * 0.01); g.font = `bold ${H * 0.068}px Arial`; g.fillText('TOTAL', W * 0.08, H * 0.8); g.textAlign = 'right'; g.fillText(o.total || '7,50 €', W * 0.92, H * 0.8); }, { res: 384 });
    const g = grp(at(box(0.152, 0.202, 0.002, P.paper), 0, 0, 0), at(c, 0, 0, 0.0015)); g.userData.grip = [0, -0.09, 0]; return g; },
  bookStack(o) { // every book he read in ten thousand years
    const g = grp(), r = rng(o.seed || 7), n = o.n || 38, cols = [P.red, P.teal, P.navy, P.yellow, P.cream, '#5E7E5E', P.salmon, P.woodDark]; let y = 0;
    for (let i = 0; i < n; i++) { const h = 0.035 + r() * 0.03; g.add(at(box(0.2 + r() * 0.08, h, 0.28 + r() * 0.06, cols[i % cols.length], { outline: 0.004 }), (r() - 0.5) * 0.04, y + h / 2, (r() - 0.5) * 0.04, 0, (r() - 0.5) * 0.5, 0)); y += h; }
    return g; },
  tallyBoard(o) { // chalk tally marks: he counted his sleeps
    const w = o.w || 1.6, h = o.h || 1.0;
    const c = canvasPlane(w, h, (g, W, H) => { g.fillStyle = '#26302C'; g.fillRect(0, 0, W, H); g.strokeStyle = 'rgba(240,240,232,0.9)'; g.lineWidth = Math.max(2, W * 0.004); const r = rng(5);
      for (let row = 0; row < 14; row++) for (let grp5 = 0; grp5 < 18; grp5++) { const x0 = W * (0.03 + grp5 * 0.053), y0 = H * (0.04 + row * 0.068), dx = W * 0.008, hh = H * 0.05;
        for (let i = 0; i < 4; i++) { g.beginPath(); g.moveTo(x0 + i * dx + (r() - 0.5) * 2, y0); g.lineTo(x0 + i * dx + (r() - 0.5) * 2, y0 + hh); g.stroke(); }
        g.beginPath(); g.moveTo(x0 - dx * 0.5, y0 + hh * 0.85); g.lineTo(x0 + dx * 3.5, y0 + hh * 0.15); g.stroke(); } });
    return grp(at(box(w + 0.06, h + 0.06, 0.03, P.woodDark, { outline: 0.006 }), 0, 0, 0), at(c, 0, 0, 0.017)); },
  busStop(o) { // bus shelter: two posts, roof, back glass, bench, BUS sign on a pole
    const w = o.w || 2.4, g = grp(at(box(w, 0.08, 1.1, P.greyDark, { outline: 0.008 }), 0, 2.4, 0));
    [-w / 2 + 0.05, w / 2 - 0.05].forEach(x => g.add(at(box(0.06, 2.4, 0.06, P.greyDark, { pivot: 'bottom' }), x, 0, -0.45), at(box(0.06, 2.4, 0.06, P.greyDark, { pivot: 'bottom' }), x, 0, 0.45)));
    g.add(at(mesh(new THREE.BoxGeometry(w - 0.1, 1.8, 0.02), glassMat(0.3)), 0, 1.25, -0.5), at(box(w - 0.1, 0.06, 0.03, P.greyDark), 0, 2.16, -0.5));
    g.add(at(box(1.4, 0.05, 0.36, P.wood), 0, 0.45, -0.25), at(box(0.05, 0.45, 0.3, P.greyDark, { pivot: 'bottom' }), -0.6, 0, -0.25), at(box(0.05, 0.45, 0.3, P.greyDark, { pivot: 'bottom' }), 0.6, 0, -0.25));
    g.add(at(box(0.05, 2.6, 0.05, P.greyDark, { pivot: 'bottom' }), w / 2 + 0.35, 0, 0.4), at(label('BUS', 0.4, 0.3, { bg: '#2C4A8A', fg: P.white }), w / 2 + 0.35, 2.45, 0.43));
    return g; },
  tapeRoll(o) { return grp(at(torus(0.035, 0.014, '#C9B48A', 6, 14), 0, 0, 0, Math.PI / 2)); },
  buffArms(o) { // bodybuilder arms to strap on a creature (the over-muscled chickens): flexed biceps both sides
    const c = o.color || '#F4EFE2', fist = o.fist || '#E0A93A', g = grp();
    for (const s of [-1, 1]) {
      const arm = grp(at(box(0.11, 0.05, 0.055, c, { outline: 0.004 }), s * 0.055, 0, 0), at(box(0.065, 0.05, 0.06, c, { outline: 0.004 }), s * 0.058, 0.038, 0),
        at(box(0.048, 0.105, 0.05, c, { outline: 0.004 }), s * 0.112, 0.055, 0), at(box(0.055, 0.045, 0.055, fist, { outline: 0.004 }), s * 0.112, 0.115, 0));
      arm.position.set(s * 0.1, 0.0, 0); g.add(arm);
    }
    return g; },
  baldCap(o) { // shiny bald pate to sit on a creature's head ("un gorille chauve")
    const w = o.w || 0.3, d = o.d || 0.26, c = o.color || '#C9B9A6';
    const g = grp(at(box(w, 0.07, d, c, { outline: 0.006, taper: { x: 0.8, z: 0.8 } }), 0, 0.035, 0), at(box(w * 0.25, 0.01, d * 0.2, '#EFE6DA', { noGrain: true }), -w * 0.15, 0.072, d * 0.1));
    return g; },
  
  // --- "son nom dessus": felt pen, yogurt, broom closet, shopping, bank sack --------------------------------
  scrawl(o) { // felt-pen handwriting on any surface (door, chair, forehead, vault, car): opts text, w, h, color, writeAt, writeDur, strike, underline
    const w = o.w || 0.6, h = o.h || 0.16, s = scrawlTexture(o.text || 'BERNARD', w / h, o);
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), scrawlMat(s.tex)); m.renderOrder = 3;
    const g = grp(m); g.userData.update = t => s.draw(scrawlK(o, t)); g.userData.update(-1e9); return g; },
  yogurt(o) { // strawberry yogurt pot with a foil lid; opts: name (felt pen, writeAt), strike (crossed out), name2 (new owner, writeAt2), open (lid peeled back)
    const R = 0.06, rb = 0.048, H = 0.12, g = grp(cyl(R, rb, H, '#F7F4EC', 14, { pivot: 'bottom', outline: 0.006 }),
      at(cyl(R + 0.0015, R - 0.0035, 0.028, o.color || P.pink, 14), 0, H - 0.017, 0), at(cyl(R * 0.8, R * 0.8, 0.003, '#F2D6DE', 12), 0, H - 0.0005, 0));
    const lid = grp(at(cyl(R + 0.006, R + 0.006, 0.005, '#C9CCD1', 14, { outline: 0.02 }), -R, 0, 0)); lid.position.set(R, H + 0.003, 0); lid.rotation.z = o.open ? -2.25 : 0; g.add(lid);
    const ups = [], rAt = y => rb + (R - rb) * y / H;
    const name = (text, y, opt) => { const s = scrawlTexture(text, 3.8, { res: 320, ...opt });
      const m = new THREE.Mesh(new THREE.CylinderGeometry(rAt(y + 0.017) + 0.002, rAt(y - 0.017) + 0.002, 0.034, 14, 1, true, -1.15, 2.3), scrawlMat(s.tex));
      m.position.y = y; m.renderOrder = 3; g.add(m); ups.push(t => s.draw(scrawlK(opt, t))); };
    if (o.name) name(o.name, o.name2 ? 0.074 : 0.062, { writeAt: o.writeAt, writeDur: o.writeDur, strike: o.strike, color: o.inkColor });
    if (o.name2) name(o.name2, 0.034, { writeAt: o.writeAt2, writeDur: o.writeDur2, color: o.inkColor2 || '#B3261E', seed: 21 });
    if (ups.length) { g.userData.update = t => ups.forEach(f => f(t)); g.userData.update(-1e9); }
    g.userData.grip = [0, 0.06, 0]; return g; },
  spoon(o) { const g = grp(at(box(0.012, 0.13, 0.005, '#C9CCD1'), 0, 0.065, 0), at(sphere(0.02, '#C9CCD1', 1), 0, 0.14, 0)); g.children[1].scale.set(0.9, 1.25, 0.35); g.userData.grip = [0, 0.03, 0]; return g; },
  moneySack(o) { // tied burlap sack with a big euro sign
    const c = o.color || '#B89462', body = sphere(0.26, c, 1); body.scale.set(1, 0.95, 0.85); body.position.y = 0.24; addOutline(body, 0.03);
    const g = grp(body, at(cyl(0.06, 0.1, 0.12, c, 8), 0, 0.5, 0), at(torus(0.065, 0.015, '#8C6239', 4, 10), 0, 0.5, 0, PI / 2), at(cyl(0.1, 0.05, 0.08, c, 8), 0, 0.59, 0),
      at(label(o.text || '€', 0.24, 0.24, { bg: null, fg: '#2E5E3A' }), 0, 0.25, 0.225));
    g.userData.grip = [0, 0.58, 0]; return g; },
  shoppingBag(o) { // kraft paper grocery bag with a baguette and a leek
    const C = o.color || '#C9A06A', w = 0.34, h = 0.36, d = 0.2, g = grp(box(w, h, d, C, { pivot: 'bottom', outline: 0.008 }), at(box(w + 0.006, 0.04, d + 0.006, '#B48A55'), 0, h - 0.03, 0));
    g.add(at(cyl(0.032, 0.03, 0.62, '#D9A35C', 7), -0.08, h + 0.1, -0.03, 0.12, 0, 0.22), at(cyl(0.024, 0.024, 0.26, P.white, 7), 0.08, h + 0.03, 0.03, -0.1, 0, -0.18), at(cyl(0.034, 0.012, 0.3, '#5E9C4A', 6), 0.115, h + 0.29, 0.06, -0.1, 0, -0.3));
    [-1, 1].forEach(sd => g.add(at(torus(0.07, 0.008, '#8C6239', 4, 10, PI), 0, h, sd * 0.06)));
    if (o.text) g.add(at(label(o.text, w * 0.8, 0.1, { bg: null, fg: P.redDark }), 0, h * 0.45, d / 2 + 0.004));
    g.userData.grip = [0, h + 0.07, 0]; return g; },
  cupboard(o) { // broom closet, door open: broom, bucket + mop, shelf with bottles, ceiling light; opts.sign on the header plate
    const W = o.w || 1.0, H = o.h || 2.3, D = o.d || 0.7, c = o.color || '#C9C2AE', t = 0.04, g = grp();
    g.add(at(box(W, H, t, c), 0, H / 2, -D / 2 + t / 2), at(box(t, H, D, c, { outline: 0.006 }), -W / 2 + t / 2, H / 2, 0), at(box(t, H, D, c, { outline: 0.006 }), W / 2 - t / 2, H / 2, 0),
      at(box(W, t, D, c, { outline: 0.006 }), 0, H - t / 2, 0), at(box(W, 0.05, D, '#8C8676'), 0, 0.025, 0), at(box(W - 2 * t, H - 0.1, 0.01, '#E3DCC9'), 0, H / 2, -D / 2 + t + 0.006));
    g.add(at(box(W, 0.2, 0.03, c, { outline: 0.006 }), 0, H - 0.1, D / 2 - 0.015));
    if (o.sign) g.add(at(label(o.sign, W * 0.72, 0.13, { bg: '#2C2C2C', fg: '#E8D9A0' }), 0, H - 0.1, D / 2 + 0.002));
    g.add(at(box(W - 2 * t, 0.025, D * 0.5, '#B9B2A2'), 0, H - 0.52, -D / 2 + D * 0.29), at(box(0.3, 0.02, 0.2, '#FFFFFF', { emissive: '#FFF3C8', noGrain: true }), 0, H - t - 0.012, -0.05));
    [[-0.3, P.teal, 0.2], [-0.14, P.yellow, 0.24], [0.2, P.red, 0.18], [0.33, P.white, 0.22]].forEach(([x, col, hh]) => g.add(at(cyl(0.04, 0.045, hh, col, 7, { pivot: 'bottom' }), x * W, H - 0.507, -D / 2 + 0.14)));
    g.add(rod([-W / 2 + 0.16, 0.12, -D / 2 + 0.24], [-W / 2 + 0.1, 1.45, -D / 2 + 0.08], 0.014, P.wood), at(box(0.28, 0.1, 0.07, '#C9A86A', { outline: 0.01 }), -W / 2 + 0.17, 0.1, -D / 2 + 0.25, 0, 0.3, 0));
    g.add(at(cyl(0.15, 0.12, 0.28, '#3E6FB5', 9, { pivot: 'bottom', outline: 0.01 }), W / 2 - 0.2, 0.05, -D / 2 + 0.22), rod([W / 2 - 0.2, 0.2, -D / 2 + 0.22], [W / 2 - 0.12, 1.42, -D / 2 + 0.08], 0.013, P.grey));
    const piv = grp(); piv.position.set(W / 2, 0.05, D / 2); g.add(piv); const dh = H - 0.27;
    piv.add(at(box(W - 0.02, dh, 0.035, c, { outline: 0.006 }), -(W - 0.02) / 2, dh / 2, 0.0175), at(sphere(0.03, P.yellow, 0), -(W - 0.1), dh * 0.5, 0.05),
      at(label('ENTRETIEN', 0.42, 0.1, { bg: '#E8E2D0', fg: P.ink }), -W / 2, dh * 0.8, 0.037));
    piv.rotation.y = (o.open ?? 1) * 1.75;
    g.userData.front = [0, 0, D / 2 + 0.6]; return g; },
  officeChair(o) { // swivel office chair with a tall backrest on a 5-star base; front +Z, backrest front face ~ z -0.19
    const c = o.color || '#B8BEC6', g = grp();
    for (let i = 0; i < 5; i++) { const a = i * TAU / 5; g.add(at(box(0.04, 0.035, 0.3, P.greyDark), Math.sin(a) * 0.14, 0.06, Math.cos(a) * 0.14, 0, a, 0), at(sphere(0.03, P.ink, 0), Math.sin(a) * 0.28, 0.03, Math.cos(a) * 0.28)); }
    g.add(at(cyl(0.025, 0.025, 0.36, P.grey, 8, { pivot: 'bottom' }), 0, 0.08, 0), at(box(0.5, 0.08, 0.48, c, { outline: 0.01 }), 0, 0.48, 0.01),
      at(box(0.46, 0.7, 0.07, c, { outline: 0.01 }), 0, 0.92, -0.23, -0.08, 0, 0), at(box(0.06, 0.4, 0.04, P.greyDark), 0, 0.6, -0.25));
    [-1, 1].forEach(sd => g.add(at(box(0.05, 0.03, 0.3, P.ink), sd * 0.27, 0.68, 0.0), at(box(0.03, 0.17, 0.03, P.ink, { pivot: 'bottom' }), sd * 0.27, 0.52, -0.05)));
    g.userData.seat = [0, 0.52, 0]; return g; },
  // --- autumn-2026 news series --------------------------------------------------------------------------------
  tweetPhone(o) { // phone showing a post with its machine translation: opts name, handle, via, text, likes, avatar
    const scr = canvasPlane(0.1, 0.2, (g, W, H) => tweetCard(g, W, H, o), { res: 360, emissive: 0.55 });
    const g = grp(at(box(0.11, 0.21, 0.012, P.ink, { outline: 0.03 }), 0, 0, 0), at(scr, 0, 0, 0.0065)); g.userData.grip = [0, -0.07, 0]; return g; },
  tweetMonitor(o) { // desk monitor showing the same post, readable in a medium shot
    const scr = canvasPlane(0.62, 0.86, (g, W, H) => tweetCard(g, W, H, o), { res: 512, emissive: 0.5 });
    return grp(at(box(0.68, 0.92, 0.04, P.ink, { outline: 0.008 }), 0, 0.72, 0), at(scr, 0, 0.72, 0.021), at(box(0.06, 0.26, 0.06, P.greyDark, { pivot: 'bottom' }), 0, 0, -0.05), at(box(0.3, 0.02, 0.22, P.greyDark), 0, 0.01, -0.05)); },
  protestSign(o) { // cardboard sign on a stick, felt-pen text (2 lines max)
    const w = o.w || 0.62, h = o.h || 0.42, txt = o.text || '6-7', g = grp(at(box(0.03, 1.0, 0.03, P.wood, { pivot: 'bottom' }), 0, 0, 0), at(box(w, h, 0.015, '#C9A06A', { outline: 0.01 }), 0, 1.0 + h / 2, 0.02));
    const c = canvasPlane(w * 0.94, h * 0.9, (gg, W, H) => { const lines = String(txt).split('\n'); gg.fillStyle = '#D8B582'; gg.fillRect(0, 0, W, H); gg.fillStyle = o.color || P.ink; gg.textAlign = 'center'; gg.textBaseline = 'middle';
      const fs = Math.min(H * 0.8 / lines.length, W * 0.95 / (Math.max(...lines.map(l => l.length)) * 0.62)); gg.font = `900 ${fs}px Arial`; lines.forEach((l, i) => gg.fillText(l, W / 2, H * (i + 0.5) / lines.length)); }, { res: 384 });
    g.add(at(c, 0, 1.0 + h / 2, 0.029)); g.userData.grip = [0, 0.35, 0]; return g; },
  flourBag(o) { const g = grp(at(box(0.22, 0.3, 0.12, '#EDE6D6', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(label(o.text || 'FARINE', 0.2, 0.08, { bg: '#EDE6D6', fg: P.navy }), 0, 0.17, 0.062)); g.userData.grip = [0, 0.28, 0]; return g; },
  cheeseWheel(o) { const g = grp(at(cyl(0.2, 0.2, 0.12, '#E9C46A', 16, { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(cyl(0.2, 0.2, 0.005, '#B8862E', 16), 0, 0.122, 0), at(label(o.text || 'COMTÉ', 0.2, 0.06, { bg: '#F4E6B8', fg: P.redDark }), 0, 0.06, 0.201)); g.userData.grip = [0, 0.06, 0]; return g; },
  milkCarton(o) { const g = grp(at(box(0.12, 0.24, 0.12, P.white, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(0.12, 0.06, 0.12, '#3E6FB5', { taper: { x: 1, z: 0.1 } }), 0, 0.27, 0), at(label(o.text || 'LAIT', 0.11, 0.06, { bg: P.white, fg: '#3E6FB5' }), 0, 0.13, 0.061)); g.userData.grip = [0, 0.12, 0]; return g; },
  drinkCan(o) { const g = grp(at(cyl(0.045, 0.045, 0.16, o.color || P.red, 12, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(cyl(0.04, 0.045, 0.012, P.grey, 12), 0, 0.166, 0), at(label(o.text || 'SODA', 0.08, 0.04, { bg: null, fg: P.white }), 0, 0.08, 0.046)); g.userData.grip = [0, 0.08, 0]; return g; },
  sushiPlate(o) { const g = grp(at(box(0.5, 0.04, 0.22, P.wood, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0));
    for (let i = 0; i < 5; i++) g.add(at(box(0.07, 0.035, 0.045, '#F4F1EA'), -0.18 + i * 0.09, 0.058, 0), at(box(0.075, 0.015, 0.05, i % 2 ? '#E8775F' : '#F08A6A'), -0.18 + i * 0.09, 0.083, 0));
    return g; },
  sauceBottle(o) { const g = grp(at(cyl(0.05, 0.05, 0.18, '#E07A2E', 10, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(cyl(0.02, 0.05, 0.05, P.white, 10), 0, 0.205, 0), at(cyl(0.006, 0.02, 0.04, P.white, 6), 0, 0.25, 0),
      at(label(o.text || 'ALGÉRIENNE', 0.1, 0.05, { bg: P.white, fg: P.redDark }), 0, 0.09, 0.051)); g.userData.grip = [0, 0.09, 0]; return g; },
  croissant(o) { const g = grp(); for (let i = 0; i < 5; i++) { const a = -0.9 + i * 0.45, r = i === 2 ? 0.045 : i % 4 === 0 ? 0.025 : 0.038; g.add(at(sphere(r, '#D9A35C', 1), Math.sin(a) * 0.09, r * 0.8, -Math.cos(a) * 0.05 + 0.03)); } g.userData.grip = [0, 0.04, 0]; return g; },
  notebook(o) { // small notebook with a printed cover (the undercover cop's slang guide)
    const c = canvasPlane(0.15, 0.21, (gg, W, H) => { gg.fillStyle = o.bg || '#C23A2E'; gg.fillRect(0, 0, W, H); gg.fillStyle = '#F6F1E3'; gg.textAlign = 'center'; gg.textBaseline = 'middle';
      const lines = String(o.text || 'LEXIQUE\nJEUNE\n—\nÉDITION\n2019').split('\n'); gg.font = `900 ${H * 0.11}px Arial`; lines.forEach((l, i) => gg.fillText(l, W / 2, H * (0.18 + i * 0.16))); }, { res: 256 });
    const g = grp(at(box(0.155, 0.215, 0.02, '#8E2A21', { outline: 0.02 }), 0, 0, 0), at(c, 0, 0, 0.0105)); g.userData.grip = [0, -0.09, 0]; return g; },
  ballonDor(o) { const g = grp(at(cyl(0.09, 0.11, 0.08, P.ink, 10, { pivot: 'bottom' }), 0, 0, 0), at(sphere(0.12, '#E6B84A', 1, { outline: 0.02 }), 0, 0.2, 0)); g.userData.grip = [0, 0.05, 0]; return g; },
  memePoster(o) { // propaganda-style meme poster: a figure in a grey tunic, red background, caption
    const c = canvasPlane(0.6, 0.85, (gg, W, H) => { gg.fillStyle = '#B5302A'; gg.fillRect(0, 0, W, H); gg.fillStyle = '#E6B84A'; for (let i = 0; i < 12; i++) { gg.save(); gg.translate(W / 2, H * 0.42); gg.rotate(i * Math.PI / 6); gg.fillRect(-W * 0.02, 0, W * 0.04, H * 0.6); gg.restore(); }
      gg.fillStyle = '#7C7E68'; gg.beginPath(); gg.moveTo(W * 0.2, H * 0.92); gg.lineTo(W * 0.3, H * 0.55); gg.lineTo(W * 0.7, H * 0.55); gg.lineTo(W * 0.8, H * 0.92); gg.fill();
      gg.fillStyle = o.skin || '#5E3F2C'; gg.fillRect(W * 0.4, H * 0.24, W * 0.2, H * 0.3); gg.fillStyle = '#17181B'; gg.fillRect(W * 0.4, H * 0.22, W * 0.2, H * 0.04);
      gg.fillStyle = '#F6F1E3'; gg.textAlign = 'center'; gg.font = `900 ${H * 0.07}px Arial`; gg.fillText(o.text || 'MÈME', W / 2, H * 0.12); }, { res: 384 });
    const g = grp(at(box(0.64, 0.89, 0.01, P.ink), 0, 0, 0), at(c, 0, 0, 0.006)); g.rotation.z = o.tilt ?? 0.03; return g; },
  parasol(o) { // beach parasol on a pole with a weighted base; furled (closed) by default, opens at openAt
    const R = o.radius || 1.0, H = o.height || 2.1, cols = o.colors || ['#C23A2E', '#F6F1E3'];
    const g = grp(at(cyl(0.22, 0.25, 0.08, P.greyDark, 12, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(cyl(0.025, 0.025, H, P.wood, 6, { pivot: 'bottom' }), 0, 0.08, 0));
    const can = grp(); g.add(can);
    for (let i = 0; i < 8; i++) can.add(mesh(new THREE.ConeGeometry(R, R * 0.35, 1, 1, true, i * TAU / 8, TAU / 8), mat(cols[i % cols.length], { doubleSide: true })));
    const strap = at(box(0.07, 0.05, 0.07, P.ink), 0, H - 0.35, 0); g.add(strap);
    const setOpen = op => { can.scale.set(0.09 + 0.91 * op, 1 + (1 - op) * 2.6, 0.09 + 0.91 * op); can.position.y = H + 0.08 - (1 - op) * R * 0.455; strap.visible = op < 0.3; };
    setOpen(o.open ?? 0);
    if (o.openAt != null) g.userData.update = t => setOpen(ease.out(clamp01((t - o.openAt) / 0.5)));
    g.userData.grip = [0, 1.0, 0]; return g; },
  dogBowl(o) { const g = grp(cyl(0.17, 0.14, 0.08, o.color || P.red, 14, { pivot: 'bottom', outline: 0.01 }), at(cyl(0.13, 0.13, 0.01, '#3A2A20', 14), 0, 0.075, 0)); if (o.full) for (let i = 0; i < 9; i++) g.add(at(sphere(0.025, '#8C6239', 0), Math.cos(i) * 0.07, 0.09, Math.sin(i * 1.7) * 0.07)); return g; },
  copCap(o) { const g = grp(at(cyl(0.11, 0.1, 0.07, P.navy, 12, { outline: 0.02 }), 0, 0.035, 0), at(cyl(0.12, 0.12, 0.012, P.navy, 12), 0, 0.075, 0), at(box(0.16, 0.012, 0.09, P.ink), 0, 0.012, 0.1, 0.25, 0, 0), at(box(0.04, 0.035, 0.01, P.yellow), 0, 0.04, 0.105)); return g; },
  leash(o) { const L = o.length || 1.3, el = o.elev ?? 0.45; return grp(rod([0, 0, 0], [0, Math.sin(el) * L, -Math.cos(el) * L], 0.012, o.color || P.red), at(torus(0.05, 0.012, o.color || P.red, 4, 10), 0, Math.sin(el) * L, -Math.cos(el) * L)); },
  speedDisplay(o) { // "radar pédagogique": LED speed readout on a pole
    const c = canvasPlane(0.5, 0.28, (gg, W, H) => { gg.fillStyle = '#111'; gg.fillRect(0, 0, W, H); gg.fillStyle = o.color || '#FF8A2E'; gg.textAlign = 'center'; gg.textBaseline = 'middle'; gg.font = `900 ${H * 0.8}px "Courier New", monospace`; gg.fillText(String(o.value ?? 67), W / 2, H * 0.55); }, { res: 256, emissive: 0.9 });
    return grp(cyl(0.04, 0.04, 2.0, P.grey, 6, { pivot: 'bottom' }), at(box(0.6, 0.38, 0.12, P.greyDark, { outline: 0.01 }), 0, 2.2, 0), at(c, 0, 2.2, 0.062), at(label('km/h', 0.3, 0.07, { bg: P.greyDark, fg: P.white }), 0, 1.97, 0.062)); },
  toast(o) { const c = o.raw ? '#F2E6CC' : '#D9A35C'; const g = grp(at(box(0.13, 0.13, 0.025, c, { outline: 0.02 }), 0, 0.065, 0), at(box(0.135, 0.02, 0.028, o.raw ? '#D9B98A' : '#9A6232'), 0, 0.13, 0)); g.userData.grip = [0, 0.03, 0]; return g; },
  torii(o) { const R = '#C23A2E', g = grp(); [-1, 1].forEach(sd => g.add(at(cyl(0.12, 0.14, 3.0, R, 10, { pivot: 'bottom', outline: 0.01 }), sd * 1.3, 0, 0), at(box(0.34, 0.22, 0.34, P.ink), sd * 1.3, 0.11, 0)));
    g.add(at(box(3.4, 0.2, 0.3, R, { outline: 0.01 }), 0, 2.55, 0), at(box(3.9, 0.18, 0.4, P.ink, { taper: { x: 1.0, z: 1.0 } }), 0, 3.05, 0), at(box(0.16, 0.5, 0.18, R), 0, 2.8, 0)); return g; },
  boule(o) { const r = o.r || 0.045; const g = grp(at(sphere(r, o.color || '#9AA2A8', 1, { outline: 0.02 }), 0, r, 0), at(torus(r * 0.75, r * 0.06, '#5E666C', 4, 12), 0, r, 0, PI / 2)); return g; },
  baguette(o) { const g = grp(at(cyl(0.035, 0.03, 0.62, '#D9A35C', 8, { outline: 0.02 }), 0, 0.035, 0, 0, 0, PI / 2)); for (let i = 0; i < 4; i++) g.add(at(box(0.05, 0.006, 0.03, '#B5793A'), -0.2 + i * 0.13, 0.068, 0, 0, 0.5, 0)); g.userData.grip = [0, 0.035, 0]; return g; },
  clickCounter(o) { const g = grp(at(box(0.05, 0.06, 0.03, P.grey, { outline: 0.02 }), 0, 0, 0), at(box(0.02, 0.015, 0.02, P.greyDark), 0.0, 0.035, 0)); g.userData.grip = [0, 0, 0]; return g; },
  fastForward(o) { return grp(at(label('▶▶ x16', 0.8, 0.3, { bg: P.ink, fg: P.white }), 0, 0, 0)); },
  
};

export const PROP_NAMES = Object.keys(B);

// Labelled placeholder for unknown names — never throws.
function placeholder(name) {
  return grp(at(box(0.6, 0.6, 0.6, P.creamDark, { outline: 0.02 }), 0, 0.3, 0), at(label(name, 0.58, 0.2, { bg: P.paper, fg: P.red }), 0, 0.3, 0.302));
}

export function buildProp(name, opts = {}) {
  let inner;
  try { inner = B[name] ? B[name](opts || {}) : placeholder(String(name)); }
  catch (e) { console.warn('[props] failed to build', name, e.message); inner = placeholder(String(name)); }
  // Wrap so the root's transform is free for the director; hoist userData.
  const root = new THREE.Group(); root.add(inner); root.userData = inner.userData; inner.userData = {};
  root.name = String(name); root.userData.kind = 'prop'; root.userData.prop = name;
  return root;
}
