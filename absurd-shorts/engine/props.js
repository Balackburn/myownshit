// Prop library: compact low-poly props in the paper style. buildProp(name, opts) -> Object3D.
// Conventions: origin at the prop's base (y = 0), front faces +Z, 1 unit = 1 m.
//   userData.grip   = local point a hand holds (handheld props)
//   userData.update = (t) => {...} for animated props (pure function of t, no clocks)
//   userData.center = visual centre for floating FX (explosion, zzz, ...)
// The root returned by buildProp is never transformed by builders, so the director can
// freely set position / rotation / scale on it.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, sphere, textPlane, addOutline, rng, ease, clamp01, grainTexture } from './style.js';
import { VP_PROPS } from './props_vp.js';
import { OCEAN_PROPS } from './props_ocean.js';
import { NEWS_PROPS } from './props_news.js';
import { CANICULE_PROPS } from './props_canicule.js';
import { VER_PROPS } from './props_ver.js';
import { CHAUSSETTES_PROPS } from './props_chaussettes.js';
import { TROU_PROPS } from './props_trou.js';
import { ETERNUEMENT_PROPS } from './props_eternuement.js';
import { PORTE_PROPS } from './props_porte.js';
import { INTERRUPTEUR_PROPS } from './props_interrupteur.js';
import { ELAN_PROPS } from './props_elan.js';
import { OMBRE_PROPS } from './props_ombre.js';
import { CRAVATE_PROPS } from './props_cravate.js';
import { STATUE_PROPS } from './props_statue.js';
import { FOURRIERE_PROPS } from './props_fourriere.js';
import { RADAR_PROPS } from './props_radar.js';
import { HOQUET_PROPS } from './props_hoquet.js';
import { AIMANT_PROPS } from './props_aimant.js';
import { CODEBARRE_PROPS } from './props_codebarre.js';

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

// Additive soft glow (afterburners, flames, explosion flash): a camera-facing sprite with a radial falloff, never fogged or shadowed.
let _glowTex = null;
function glowTex() {
  if (_glowTex) return _glowTex;
  const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d'), gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.22, 'rgba(255,255,255,0.75)'); gr.addColorStop(0.55, 'rgba(255,255,255,0.2)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 128, 128); _glowTex = new THREE.CanvasTexture(c); _glowTex.colorSpace = THREE.SRGBColorSpace; return _glowTex;
}
export function glowSprite(color, size, opacity = 1) {
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex(), color, blending: THREE.AdditiveBlending, transparent: true, opacity, depthWrite: false, fog: false }));
  s.scale.set(size, size, 1); return s;
}
// Smooth-shaded puff material and geometry (clouds, fireballs, smoke): soft round forms, unlike the faceted paper look.
const _cloudMats = new Map();
export function cloudMat(color = '#BEBEBA', emissive = '#97A6B6') { // stylised cloud: a blue-grey glow (the shadow side) + a diffuse share lit by the warm sun
  const k = color + emissive; if (!_cloudMats.has(k)) _cloudMats.set(k, new THREE.MeshLambertMaterial({ color, emissive, map: grainTexture() })); return _cloudMats.get(k); }
const _sph = {};
export const sphereGeo = (detail = 2) => (_sph[detail] ||= new THREE.IcosahedronGeometry(1, detail));
// Ring of jagged "teeth" (the reference tornado's skin): n trapezoid teeth from radius r0 at y=0 to r1 at the shoulder, each ending in a
// spike at height h; gap = fraction of each sector left open (the striped inner cone shows through). Non-indexed -> flat facets.
function toothBand(r0, r1, h, n, gap = 0.18, spike = 0.35, seed = 1) {
  const pos = [], uv = [], r = rng(seed), P = (a, rr, y) => [Math.cos(a) * rr, y, Math.sin(a) * rr];
  for (let i = 0; i < n; i++) {
    const a0 = (i + r() * 0.15) / n * TAU, a1 = a0 + TAU / n * (1 - gap), am = (a0 + a1) / 2, sh = h * (1 - spike) * (0.9 + r() * 0.2), tip = sh + h * spike * (0.9 + r() * 0.25); // spike 0 -> flat-topped tab
    const b0 = P(a0, r0, 0), b1 = P(a1, r0, 0), t0 = P(a0 + (a1 - a0) * 0.08, r1, sh), t1 = P(a1 - (a1 - a0) * 0.08, r1, sh), tp = P(am, r1 * 1.04, tip);
    pos.push(...b0, ...b1, ...t1, ...b0, ...t1, ...t0, ...t0, ...t1, ...tp);
    uv.push(0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0.5, 1.4);
  }
  const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); geo.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); geo.computeVertexNormals(); return geo;
}
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
      if (o.screen === 'handle') { // the creator's handle in a white-outlined box on a black screen (reference S4)
        g.fillStyle = '#0D0D0F'; g.fillRect(0, 0, W, H); g.strokeStyle = '#F2F2F2'; g.lineWidth = W * 0.035; g.strokeRect(W * 0.1, H * 0.2, W * 0.8, H * 0.5);
        g.fillStyle = '#F4F4F4'; g.font = `900 ${W * 0.2}px Arial`; (o.lines || ['@outof', 'this', 'world_9']).forEach((l, i) => g.fillText(l, W / 2, H * (0.32 + i * 0.13)));
        return;
      }
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
    if (o.hand) { // a blocky hand gripping the lower half (reference S4): four fingers over the right edge, the thumb on the left, the palm behind
      const sk = typeof o.hand === 'string' ? o.hand : '#D9A377';
      for (let i = 0; i < 4; i++) g.add(at(box(0.05, 0.03, 0.034, sk, { outline: 0.02 }), 0.072, 0.035 + i * 0.033, 0.006, 0, 0, -0.12));
      g.add(at(box(0.034, 0.075, 0.03, sk, { outline: 0.02 }), -0.066, 0.06, 0.012, 0, 0, 0.35), at(box(0.13, 0.12, 0.03, sk), 0.0, 0.06, -0.026));
    }
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
  cashRegister(o = {}) {   // (cycle 10) o.text: the display ('$0.00' by default; '0,00 €' in French stories)
    const keys = grp(); keys.position.set(0, 0.25, 0.08); keys.rotation.x = 0.45;
    for (let i = 0; i < 12; i++) keys.add(at(box(0.05, 0.02, 0.04, i === 11 ? P.red : P.navy), -0.1 + (i % 4) * 0.065, 0.012, -0.06 + Math.floor(i / 4) * 0.055));
    return grp(box(0.5, 0.12, 0.45, P.greyDark, { pivot: 'bottom' }), at(box(0.46, 0.16, 0.42, P.cream, { pivot: 'bottom', outline: 0.01 }), 0, 0.12, -0.01),
      at(box(0.44, 0.02, 0.26, P.cream), 0, 0.25, 0.08, 0.45), keys,
      at(box(0.04, 0.12, 0.04, P.greyDark, { pivot: 'bottom' }), 0, 0.28, -0.15), at(box(0.3, 0.12, 0.06, P.ink), 0, 0.44, -0.15), at(label(o.text || '$0.00', 0.26, 0.08, { bg: P.ink, fg: LCD }), 0, 0.44, -0.118),
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
  townhouse(o) { // narrow 2-storey American suburban house, front gable on the street (reference "tornado" short): siding lines, framed windows with shutters, porch
    const w = o.w || 5, d = o.d || 7.5, h = o.h || 5.4, c = o.color || '#B9A6D6', roof = o.roof || '#3A4152', trim = o.trim || '#F4F1E8';
    const frame = o.frame || '#24324A', shutter = o.shutter || '#E8B83A', door = o.door || P.red;
    const darker = new THREE.Color(c).multiplyScalar(0.9).getStyle();
    const g = grp(box(w, h, d, c, { pivot: 'bottom', outline: 0.004 }));
    const rh = w * 0.42, pitch = Math.atan2(rh, w / 2), slope = Math.hypot(w / 2, rh) + 0.35;
    [-1, 1].forEach(s => g.add(at(box(slope, 0.16, d + 0.5, roof, { outline: 0.004 }), s * (w / 4 + 0.05), h + rh / 2 + 0.02, 0, 0, 0, -s * pitch)));
    // gable wall: a triangular prism under the roof
    const tri = new THREE.Shape(); tri.moveTo(-w / 2, 0); tri.lineTo(w / 2, 0); tri.lineTo(0, rh); tri.lineTo(-w / 2, 0);
    const gable = mesh(new THREE.ExtrudeGeometry(tri, { depth: d - 0.02, bevelEnabled: false }), mat(c)); gable.position.set(0, h, -d / 2 + 0.01); g.add(gable);
    // siding: thin darker strips on the front and the gable
    for (let y = 0.35; y < h + rh - 0.3; y += 0.32) { const ww = y < h ? w : w * (1 - (y - h) / rh) - 0.2; if (ww > 0.3) g.add(at(box(ww, 0.035, 0.02, darker), 0, y, d / 2 + 0.012)); }
    g.add(at(box(w + 0.08, 0.14, 0.06, trim), 0, h, d / 2 + 0.03), at(box(0.14, h, 0.06, trim), -w / 2 + 0.05, h / 2, d / 2 + 0.03), at(box(0.14, h, 0.06, trim), w / 2 - 0.05, h / 2, d / 2 + 0.03));
    const win = (x, y, sh = true) => {
      g.add(at(box(1.0, 1.35, 0.06, frame), x, y, d / 2 + 0.04), at(box(0.82, 1.17, 0.07, '#9CC9D6'), x, y, d / 2 + 0.045), at(box(0.82, 0.06, 0.08, frame), x, y, d / 2 + 0.05), at(box(0.06, 1.17, 0.08, frame), x, y, d / 2 + 0.05),
        at(box(1.2, 0.1, 0.16, trim), x, y - 0.72, d / 2 + 0.08));
      if (sh) [-1, 1].forEach(s => g.add(at(box(0.36, 1.35, 0.05, shutter, { outline: 0.01 }), x + s * 0.72, y, d / 2 + 0.035)));
    };
    win(-w * 0.22, h * 0.72); win(w * 0.22, h * 0.72); win(-w * 0.24, h * 0.27); win(0, h + rh * 0.38, false);
    // door + porch
    const dx = w * 0.24;
    g.add(at(box(0.95, 2.05, 0.08, door, { outline: 0.01 }), dx, 1.025 + 0.3, d / 2 + 0.04), at(sphere(0.045, P.yellow, 0), dx - 0.32, 1.35, d / 2 + 0.1),
      at(box(1.9, 0.3, 1.2, trim), dx, 0.15, d / 2 + 0.6), at(box(2.1, 0.12, 1.4, roof), dx, 2.75, d / 2 + 0.65),
      at(box(0.12, 2.45, 0.12, trim, { pivot: 'bottom' }), dx - 0.85, 0.3, d / 2 + 1.15), at(box(0.12, 2.45, 0.12, trim, { pivot: 'bottom' }), dx + 0.85, 0.3, d / 2 + 1.15));
    g.userData.door = [dx, 0, d / 2 + 1.4]; return g;
  },
  voxelDog(o) { // blocky tan dog of the reference short: cube head, black muzzle block, big white eyes with black pupils, red collar
    const tan = o.color || '#D9A15A', dark = new THREE.Color(tan).multiplyScalar(0.8).getStyle(), muzzle = o.muzzle || '#3A2A22';
    const g = grp(at(box(0.3, 0.26, 0.56, tan, { outline: 0.01 }), 0, 0.42, 0));                              // body
    [[-0.1, 0.18], [0.1, 0.18], [-0.1, -0.18], [0.1, -0.18]].forEach(([x, z]) => { const leg = grp(at(box(0.09, 0.3, 0.09, tan, { outline: 0.01 }), 0, -0.15, 0), at(box(0.095, 0.05, 0.1, dark), 0, -0.28, 0.005)); leg.position.set(x, 0.3, z); leg.userData.leg = true; g.add(leg); }); // legs hinge at the hip
    g.add(at(box(0.07, 0.24, 0.07, tan, { outline: 0.01 }), 0, 0.62, -0.27, -0.5, 0, 0));                     // tail, up
    const head = grp(box(0.34, 0.32, 0.32, tan, { outline: 0.01 }),
      at(box(0.2, 0.15, 0.14, muzzle, { outline: 0.01 }), 0, -0.07, 0.21),                                       // muzzle block
      at(box(0.09, 0.06, 0.04, '#121212'), 0, -0.02, 0.29),                                                       // nose
      at(box(0.1 * (o.eyes || 1), 0.1 * (o.eyes || 1), 0.02, '#FFFFFF'), -0.085 - 0.01 * ((o.eyes || 1) - 1), 0.06 + 0.02 * ((o.eyes || 1) - 1), 0.162),
      at(box(0.1 * (o.eyes || 1), 0.1 * (o.eyes || 1), 0.02, '#FFFFFF'), 0.085 + 0.01 * ((o.eyes || 1) - 1), 0.06 + 0.02 * ((o.eyes || 1) - 1), 0.162), // eyes (o.eyes scales them)
      at(box(0.045 * (o.eyes || 1), 0.05 * (o.eyes || 1), 0.02, '#141414'), -0.075 - 0.01 * ((o.eyes || 1) - 1), 0.055 + 0.03 * ((o.eyes || 1) - 1), 0.172),
      at(box(0.045 * (o.eyes || 1), 0.05 * (o.eyes || 1), 0.02, '#141414'), 0.075 + 0.01 * ((o.eyes || 1) - 1), 0.055 + 0.03 * ((o.eyes || 1) - 1), 0.172),
      at(box(0.08, 0.12, 0.06, dark), -0.19, 0.12, -0.02), at(box(0.08, 0.12, 0.06, dark), 0.19, 0.12, -0.02));  // ears
    if (o.open) { // mouth wide open (S2 of the tornado short): the dark muzzle splits, red mouth and a big pink tongue inside
      head.children[1].position.y = -0.03; head.children[1].scale.y = 0.75;
      head.add(at(box(0.2, 0.05, 0.13, muzzle, { outline: 0.01 }), 0, -0.2, 0.2, 0.25, 0, 0), at(box(0.17, 0.08, 0.1, '#7A1E22'), 0, -0.135, 0.2), at(box(0.1, 0.03, 0.12, '#E86A84'), 0, -0.17, 0.25, 0.2, 0, 0));
    } else if (o.tongue === 'long') head.add(at(box(0.085, 0.13, 0.03, '#EE7890', { outline: 0.006 }), 0.04, -0.195, 0.27, 0.12, 0, 0.14));   // the portrait's tongue, hanging out
    else if (o.tongue) head.add(at(box(0.07, 0.02, 0.1, '#E05A6A'), 0, -0.15, 0.26, 0.4, 0, 0));
    head.position.set(0, 0.66, 0.3); g.add(head);
    g.add(at(box(0.32, 0.06, 0.06, P.red), 0, 0.53, 0.26, 0.3, 0, 0));                                            // collar
    g.userData.head = head;
    const legs = g.children.filter(c => c.userData.leg);
    if (o.walk || o.paddle) g.userData.update = t => {
      const f = (o.walk ? 2.2 : 3.2) * Math.PI * 2;                       // trot, or frantic paddling in mid-air
      legs.forEach((l, i) => { l.rotation.x = Math.sin(t * f + (i === 0 || i === 3 ? 0 : Math.PI)) * (o.walk ? 0.45 : 0.8); });
      head.position.y = 0.66 + Math.abs(Math.sin(t * f)) * 0.02; head.rotation.x = Math.sin(t * f * 0.5) * 0.06;
    };
    return g;
  },
  fighterJet(o) { // low-poly twin-tail fighter facing +Z, ~18 m long (reference "tornado" short): chined faceted fuselage, long faceted nose,
    // bubble canopy, LEX, swept trapezoid wings, outward-canted fins, stabilisers, two round nozzles with fiery rims; o.burner 0..1 flame,
    // o.glow sprite size (afterburner bloom), o.missiles per wing (white, red tips), o.gear landing gear
    const grey = o.color || '#737980', light = o.panel || '#8C929A', dark = '#4A4F56', g = grp(), Y = 1.6;
    const flatPart = (pts, depth, color, y) => { // shape given in world (x, z) pairs, lying flat at height y
      const m = mesh(new THREE.ExtrudeGeometry(new THREE.Shape(pts.map(([x, z]) => new THREE.Vector2(x, -z))), { depth, bevelEnabled: false }), mat(color)); m.rotation.x = -PI / 2; m.position.y = y - depth / 2; return m; };
    // fuselage: wide engine section aft, tapering forward, chined (octagonal) cross-section via 8-sided cylinders scaled flat
    const sec = (z0, z1, w0, w1, h0, h1, color) => { const m = mesh(new THREE.CylinderGeometry(1, 1, 1, 8, 1), mat(color)); m.geometry = new THREE.CylinderGeometry(w1, w0, Math.abs(z1 - z0), 8, 1);
      m.geometry.rotateX(PI / 2); m.geometry.rotateZ(PI / 8); m.scale.y = (h0 + h1) / (w0 + w1); m.position.set(0, Y, (z0 + z1) / 2); addOutline(m, 0.004); return m; };
    g.add(sec(-6.4, -1.0, 1.25, 1.2, 0.75, 0.75, grey), sec(-1.0, 3.6, 1.2, 0.85, 0.75, 0.62, grey), sec(3.6, 7.4, 0.85, 0.45, 0.62, 0.4, grey));
    const nose = mesh(new THREE.ConeGeometry(0.45, 2.6, 6), mat(dark)); nose.rotation.x = PI / 2; nose.scale.y = 1; nose.position.set(0, Y - 0.04, 8.7); nose.scale.set(1, 1, 0.82); g.add(nose);
    g.add(at(box(1.9, 0.08, 6.5, light), 0, Y + 0.7, -2.4));                                                                         // light dorsal panel
    const can = mesh(new THREE.SphereGeometry(0.42, 8, 6), mat('#B9C8D6', { emissive: '#22303C' })); can.scale.set(1, 0.85, 3.0); can.position.set(0, Y + 0.55, 5.2); g.add(can);
    g.add(flatPart([[0, 7.2], [1.15, 2.6], [1.15, 1.6], [0, 1.6]], 0.1, grey, Y + 0.05), flatPart([[0, 7.2], [-1.15, 2.6], [-1.15, 1.6], [0, 1.6]], 0.1, grey, Y + 0.05)); // LEX
    [-1, 1].forEach(s => {
      g.add(at(box(0.55, 0.62, 2.2, '#16181B'), s * 1.02, Y - 0.42, 2.4));                                                           // intake
      g.add(flatPart([[s * 1.0, 2.2], [s * 5.7, -2.1], [s * 5.7, -3.2], [s * 1.0, -3.8]], 0.16, grey, Y));                            // wing
      g.add(flatPart([[s * 1.0, -4.3], [s * 3.6, -5.8], [s * 3.6, -6.6], [s * 1.0, -6.6]], 0.1, grey, Y - 0.05));                       // stabiliser
      const fin = mesh(new THREE.ExtrudeGeometry(new THREE.Shape([new THREE.Vector2(-3.4, 0), new THREE.Vector2(-6.2, 0), new THREE.Vector2(-6.5, 3.0), new THREE.Vector2(-5.3, 3.0)]), { depth: 0.12, bevelEnabled: false }), mat(grey));
      fin.rotation.y = -PI / 2; fin.position.set(s * 0.06, 0, 0); const finP = grp(fin); finP.position.set(s * 0.75, Y + 0.4, 0); finP.rotation.z = -s * 0.36; g.add(finP);
      const noz = cyl(0.56, 0.5, 1.1, dark, 12, {}); noz.rotation.x = PI / 2; noz.position.set(s * 0.6, Y, -6.85); g.add(noz);
      const inner = cyl(0.4, 0.4, 0.05, o.hotCore ? '#FFE2A0' : '#1A1412', 12, o.hotCore ? { emissive: '#FFB040', noGrain: true } : {}); inner.rotation.x = PI / 2; inner.position.set(s * 0.6, Y, -7.42); g.add(inner);   // o.hotCore: the mouth glows
      const ring = mesh(new THREE.TorusGeometry(0.48, 0.08, 4, 14), mat('#E8642A', { emissive: '#E8541A', noGrain: true })); ring.position.set(s * 0.6, Y, -7.42); g.add(ring);
      for (let k = 0; k < 14; k++) { const a = k / 14 * TAU, pt = box(0.2, 0.05, 1.05, '#3A3E44'); pt.position.set(s * 0.6 + Math.cos(a) * 0.55, Y + Math.sin(a) * 0.55, -6.85); pt.rotation.z = a + PI / 2; g.add(pt);
        const seam = box(0.03, 0.055, 1.0, '#FF7A22', { emissive: '#FF6A12', noGrain: true }); seam.position.set(s * 0.6 + Math.cos(a + PI / 14) * 0.555, Y + Math.sin(a + PI / 14) * 0.555, -6.85); seam.rotation.z = a + PI / 14 + PI / 2; g.add(seam); }
      const bu = o.burner ?? 1, flame = cyl(0.36, 0.06, 2.6 * bu, '#FFE9A8', 10, { emissive: '#FFB84A', transparent: true, opacity: 0.92, noGrain: true });
      flame.rotation.x = -PI / 2; flame.position.set(s * 0.6, Y, -7.45 - 1.3 * bu); flame.visible = bu > 0; flame.castShadow = false; g.add(flame);
      const outer = cyl(0.5, 0.12, 3.2 * bu, '#FF9A3A', 12, { emissive: '#FF7A1A', transparent: true, opacity: 0.55, noGrain: true });
      outer.rotation.x = -PI / 2; outer.position.set(s * 0.6, Y, -7.45 - 1.6 * bu); outer.visible = bu > 0.5; outer.castShadow = false; outer.material.depthWrite = false; g.add(outer);
      // star roundel on the wing
      const star = canvasPlane(1.7, 1.7, (c, W, H) => { c.fillStyle = '#1F3A6E'; c.beginPath(); c.arc(W / 2, H / 2, H * 0.46, 0, Math.PI * 2); c.fill();
        c.fillStyle = '#FFFFFF'; c.beginPath(); for (let k = 0; k < 10; k++) { const a = -Math.PI / 2 + k * Math.PI / 5, r = k % 2 ? H * 0.16 : H * 0.4; c.lineTo(W / 2 + Math.cos(a) * r, H / 2 + Math.sin(a) * r); } c.fill(); }, { res: 128, transparent: true });
      star.rotation.x = -PI / 2; star.position.set(s * 4.3, Y + 0.1, -2.0); g.add(star);
      if (o.missiles) for (let i = 0; i < o.missiles; i++) { const x = s * (2.0 + i * 0.95), z = 0.2 - i * 0.55;
        g.add(at(box(0.08, 0.3, 1.2, dark), x, Y - 0.2, z - 0.6),
          at(grp(at(cyl(0.12, 0.12, 2.3, '#E6E6E2', 7), 0, 0, 0, PI / 2, 0, 0), at(mesh(new THREE.ConeGeometry(0.12, 0.42, 7), mat('#C8432E')), 0, 0, 1.36, PI / 2, 0, 0),
            at(box(0.55, 0.03, 0.3, '#E6E6E2'), 0, 0, -1.0), at(box(0.03, 0.55, 0.3, '#E6E6E2'), 0, 0, -1.0)), x, Y - 0.48, z - 0.4)); }
    });
    const side = canvasPlane(2.6, 0.45, (c, W, H) => { c.fillStyle = '#2A2F36'; c.font = `bold ${H * 0.55}px Arial`; c.textAlign = 'center'; c.fillText('U.S. AIR FORCE', W / 2, H * 0.68); }, { res: 256, transparent: true });
    side.rotation.y = PI / 2; side.position.set(1.14, Y + 0.05, -2.6); g.add(side);
    const side2 = side.clone(); side2.rotation.y = -PI / 2; side2.position.set(-1.14, Y + 0.05, -2.6); g.add(side2);
    [-1, 1].forEach(sd => { const st = box(0.02, 0.1, 1.4, '#E8902A'); st.position.set(sd * 1.15, Y - 0.25, -0.6); g.add(st); });
    if (o.glow) [-1, 1].forEach(s => { const a = glowSprite(o.glowColor || '#FF9A3C', o.glow, 0.95), b = glowSprite('#FFF1C8', o.glow * 0.45, 1); a.position.set(s * 0.6, Y, -7.6); b.position.set(s * 0.6, Y, -7.5); g.add(a, b); });
    if (o.gear) [[-1.5, 0.6, -1.5], [1.5, 0.6, -1.5], [0, 0.6, 6.0]].forEach(([x, y, z]) => g.add(at(cyl(0.32, 0.32, 0.26, '#1A1A1E', 10), x, 0.32, z, 0, 0, Math.PI / 2), at(box(0.12, Y - 0.6, 0.12, dark), x, Y / 2, z)));
    if (o.contrail) { // a contrail fixed to the jet (with a locked chase camera it stays crisp on screen, as in the reference): it grows
      // from contrail.t0 (scene time) at contrail.speed m/s up to contrail.len metres behind the nozzles; opaque core + soft sheath
      const C = o.contrail, cg = grp(), tg = new THREE.CylinderGeometry(1, 1, 1, 12, 1, true).translate(0, -0.5, 0).rotateX(PI / 2), col = C.color || '#F4EFE6';
      const core = new THREE.Mesh(tg, new THREE.MeshBasicMaterial({ color: col, fog: false })), sheath = new THREE.Mesh(tg, new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: C.soft ?? 0.35, depthWrite: false, fog: false }));
      [core, sheath].forEach(m => { m.castShadow = false; cg.add(m); }); cg.position.set(0, Y, -7.5); g.add(cg);
      const r = C.r || 0.12;
      g.userData.update = t => { const L = Math.min(C.len || 60, Math.max(0, (t - (C.t0 || 0)) * (C.speed || 270))); cg.visible = L > 0.01;
        core.scale.set(r, r, Math.max(L, 0.01)); sheath.scale.set(r * (C.sheath || 1.6), r * (C.sheath || 1.6), Math.max(L, 0.01)); };
      g.userData.update(0);
    }
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
      at(box(w + 0.3, 0.1, 0.12, fr), 0, h + 0.05, 0.06), o.inside === 'empty' ? at(canvasPlane(w, h, (c, W, H) => {   // an empty, lit cupboard: walls in perspective, a bare bulb on a cord
        c.fillStyle = '#B9AE92'; c.fillRect(0, 0, W, H); c.fillStyle = '#E8DFC4'; c.fillRect(W * 0.2, H * 0.14, W * 0.6, H * 0.62);
        c.fillStyle = '#CFC5A8'; c.beginPath(); c.moveTo(0, 0); c.lineTo(W * 0.2, H * 0.14); c.lineTo(W * 0.2, H * 0.76); c.lineTo(0, H); c.fill(); c.beginPath(); c.moveTo(W, 0); c.lineTo(W * 0.8, H * 0.14); c.lineTo(W * 0.8, H * 0.76); c.lineTo(W, H); c.fill();
        c.fillStyle = '#9C8F72'; c.beginPath(); c.moveTo(0, H); c.lineTo(W * 0.2, H * 0.76); c.lineTo(W * 0.8, H * 0.76); c.lineTo(W, H); c.fill();
        c.strokeStyle = '#3A3530'; c.lineWidth = W * 0.012; c.beginPath(); c.moveTo(W / 2, 0); c.lineTo(W / 2, H * 0.3); c.stroke();
        const gr = c.createRadialGradient(W / 2, H * 0.33, 1, W / 2, H * 0.33, W * 0.45); gr.addColorStop(0, 'rgba(255,240,180,0.9)'); gr.addColorStop(1, 'rgba(255,240,180,0)'); c.fillStyle = gr; c.fillRect(0, 0, W, H);
        c.fillStyle = '#FFF4C8'; c.beginPath(); c.arc(W / 2, H * 0.33, W * 0.05, 0, Math.PI * 2); c.fill(); }, { res: 256, emissive: 0.85 }), 0, h / 2, 0.006) : at(box(w, h, 0.01, P.ink), 0, h / 2, 0.005), piv);
    piv.position.set(o.hinge === 'right' ? w / 2 : -w / 2, 0, 0.035); if (o.hinge === 'right') piv.scale.x = -1;   // o.hinge 'right': mirrored leaf, swings to the other side
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
    const pane = o.clouds ? at(canvasPlane(w, h, (c, W, H) => { const gr = c.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#62AEE2'); gr.addColorStop(1, '#BFE0F0'); c.fillStyle = gr; c.fillRect(0, 0, W, H);
      c.fillStyle = '#FFFFFF'; [[0.3, 0.32, 0.16], [0.42, 0.28, 0.12], [0.2, 0.36, 0.1], [0.72, 0.6, 0.11], [0.82, 0.57, 0.08]].forEach(([x, yy, r]) => { c.beginPath(); c.arc(x * W, yy * H, r * W, 0, Math.PI * 2); c.fill(); }); }, { res: 256 }), 0, y + h / 2, 0.021)
      : at(box(w, h, 0.02, gc, o.lit ? { emissive: '#C9922E' } : {}), 0, y + h / 2, 0.01);
    const g = grp(pane,
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
      at(cyl(0.025, 0.025, 0.014, P.ink, 8), -0.17, 0, 0, PI / 2), at(label(o.text || '5 €', 0.32, 0.2, { bg: null, fg: P.red }), 0.08, 0, 0.008));
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
    const txt = o.text ?? 'UNE PIÈCE ?';   // the beggar's sign; text '' for a plain box (French only on screen)
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
    if (on && o.pool) { const r = o.pool === true ? 1.7 : o.pool;   // o.pool (radius): the lamp's pool of light on the ground, two flat warm discs (a night shot graded in post dims the real light: this stays)
      for (const [k, a] of [[1, 0.2], [0.62, 0.22]]) { const d = noShadow(new THREE.Mesh(new THREE.CircleGeometry(r * k, 20), new THREE.MeshBasicMaterial({ color: '#FFDFA6', transparent: true, opacity: a, depthWrite: false }))); g.add(at(d, 0.85, 0.02 + 0.004 * (1 - k), 0, -PI / 2)); } }
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
    const g = o.open ? grp(at(new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.22, 0.75, 8, 1, true), mat(c, { doubleSide: true })), 0, 0.375, 0),   // o.open: no lid, a dark inside
        at(cyl(0.235, 0.235, 0.01, '#2A2D30', 8), 0, 0.6, 0), at(new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.28, 0.05, 8, 1, true), mat(P.greyDark, { doubleSide: true })), 0, 0.76, 0))
      : grp(cyl(0.26, 0.22, 0.75, c, 8, { pivot: 'bottom' }), at(cyl(0.29, 0.29, 0.06, P.greyDark, 8), 0, 0.78, 0), at(box(0.12, 0.04, 0.04, P.ink), 0, 0.83, 0));
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
    const top = at(sphere(0.9 * s, c, 0), 0, 1.9 * s, 0, r(), r(), r()); top.scale.y = 1.1; g.add(top, at(sphere(0.55 * s, o.color2 || '#7FA86A', 0), 0.35 * s, 2.45 * s, 0.1, r(), r(), r()), at(sphere(0.5 * s, o.color3 || '#5F8F63', 0), -0.45 * s, 1.75 * s, 0.25, r(), r(), r()));   // o.color2 / o.color3: the two smaller masses (a tree in blossom: three pinks)
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
    g.userData.update = t => { const tt = Math.max(0, t - (o.startAt ?? 0)), p = o.once ? clamp01(tt / per) : (tt % per) / per, e = ease.out(p);   // startAt: when a `once` puff starts
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
    const g = grp(), r = rng(o.seed || 5), rings = [], chips = [], N = o.rings || 10, H = o.height || 5.5, cols = o.cols || ['#8E9B8B', '#A9B4A2', '#7A8778', '#B8C1AE'];
    const rad = i => (o.base ?? 0.25) + Math.pow(i / N, o.taper ?? 1.4) * (o.top ?? 1.9) + (o.flare && i >= N - 1 ? o.flare : 0);
    let inner = null;
    if (o.teeth) { // striped inner funnel (pale bands seen through the gaps between the teeth, and as rings from above)
      inner = grp(); const M = N * 2;
      for (let i = 0; i < M; i++) { const m = cyl(rad((i + 1) / 2) * 0.84, rad(i / 2) * 0.84, H / M * 1.02, i % 2 ? (o.stripeDark || '#55615A') : (o.stripe || '#D9D2C0'), 12, { open: true, doubleSide: true, pivot: 'bottom' });
        m.position.y = i * H / M; m.castShadow = false; inner.add(m); }
      g.add(inner);
    }
    for (let i = 0; i < N; i++) {
      const crown = i === N - 1;
      const col = o.pale && !crown && i % o.pale === o.pale - 1 ? (o.paleColor || '#D3CCB8') : cols[i % cols.length];
      const nT = Math.round((9 + rad(i + 1) * 3.2) * (crown ? (o.crownTeeth || 1) : 1));   // o.crownTeeth: denser crown plates
      const m = o.teeth ? mesh(toothBand(rad(i), rad(i + 1) * (crown ? (o.crownFlare ?? 1.16) : 1.05) + 0.06, H / N * (crown ? (o.crownH ?? 2.3) : (o.band ?? 1.75)), nT, o.gap ?? 0.2, crown ? (o.crownSpike ?? 0.6) : (o.spike ?? 0.2), i + 1), mat(col, { doubleSide: true }))
        : cyl(rad(i + 1) + 0.12, rad(i), H / N * 1.3, cols[i % 4], 7, { open: true, doubleSide: true, pivot: 'bottom' });
      const piv = grp(m); piv.position.y = i * H / N; piv.rotation.z = (r() - 0.5) * 0.12; g.add(piv);
      if (crown && o.teeth && o.crownLayers === 2) { // a second, staggered ring of plates just inside: the original's dense, overlapping crown
        const m2 = mesh(toothBand(rad(i) * 0.97, (rad(i + 1) * (o.crownFlare ?? 1.16) + 0.06) * 0.95, H / N * (o.crownH ?? 2.3) * 0.88, nT, o.gap ?? 0.2, o.crownSpike ?? 0.6, i + 9), mat(cols[(i + 1) % cols.length], { doubleSide: true }));
        m2.rotation.y = PI / nT; piv.add(m2); }
      if (o.bands && i > 0 && !crown && i % (o.bandEvery || 1) === 0) { // a thin continuous pale band round the ring (reads as horizontal stripes)
        const bh = H / N * (o.bands === true ? 0.32 : o.bands), bm = cyl(rad(i + 0.4) * 1.07 + 0.07, rad(i) * 1.07 + 0.07, bh, o.paleColor || '#D3CCB8', 16, { open: true, doubleSide: true, pivot: 'bottom' });
        bm.castShadow = false; bm.position.y = H / N * 0.25; m.add(bm); }
      rings.push({ piv, m, sp: (3 + r() * 2.5) * (1 - i * 0.045) * (i % 3 === 1 ? 0.6 : 1), ph: r() * TAU, i });
    }
    for (let i = 0; i < (o.chips ?? 16); i++) { const y = 0.4 + r() * H * 0.9, R = rad(y / H * N) + 0.35 + r() * 0.7;
      const m = box(0.1 + r() * 0.18, 0.04, 0.08 + r() * 0.14, i % 3 ? P.red : P.white); g.add(m); chips.push({ m, y, R, a: r() * TAU, w: 2.2 + r() * 1.8, ph: r() * TAU }); }
    const ribbons = [], dust = grp(); g.add(dust);
    if (o.collar) { // the aerial look: a wide flat dark collar (slightly dished) at the crown top + a tan inner ring; o.collar = [inner, outer] radii
      const [c0, c1] = o.collar, yC = o.collarY ?? H * (1 + 0.9 / N), cg = new THREE.CylinderGeometry(c1, c0, (c1 - c0) * 0.18, 30, 1, true).translate(0, (c1 - c0) * 0.09, 0);
      const col = mesh(cg, mat(o.collarColor || '#56615A', { doubleSide: true })); col.position.y = yC; col.castShadow = true;
      const tan = mesh(new THREE.RingGeometry(c0 * 0.78, c0 * 1.01, 30, 1).rotateX(-PI / 2), mat(o.lidColor || '#D2C29E', { doubleSide: true })); tan.position.y = yC - 0.02; tan.castShadow = false;
      const cp = grp(col, tan); g.add(cp); ribbons.push({ piv: cp, sp: 2.4, ph: 0 });
    }
    if (o.crater) { // the aerial crown seen from above (reference S8b/S10): a shallow dark dish round the hole, an inner wall of big rocks,
      // a cream debris band on the dish, an outer ring of rocks. o.crater = {r0 hole radius, r1 outer radius, y, band: [b0, b1], rocksIn, rocksOut}
      const C = o.crater, yC = C.y ?? H * (1 + 0.4 / N), cp = grp(), dh = (C.r1 - C.r0) * (C.dish ?? 0.22);
      const dish = mesh(new THREE.CylinderGeometry(C.r1, C.r0, dh, 36, 1, true).translate(0, dh / 2, 0), mat(C.color || '#5E6A62', { doubleSide: true }));
      const bm = mat(C.bandColor || '#E2D3B2', { doubleSide: true }); dish.castShadow = false;
      for (const [b0, b1] of C.bands || [C.band || [C.r0 + (C.r1 - C.r0) * 0.38, C.r0 + (C.r1 - C.r0) * 0.62]]) { // cream debris bands lying on the dish
        const band = mesh(new THREE.RingGeometry(b0, b1, 48, 1).rotateX(-PI / 2), bm); band.position.y = dh * ((b0 + b1) / 2 - C.r0) / (C.r1 - C.r0) + 0.04; band.castShadow = false; cp.add(band); }
      const rgeo = new THREE.DodecahedronGeometry(1, 0), rmat = mat(C.rockColor || '#66726B');
      const rockRing = (n, rr, sz, yy) => { for (let i = 0; i < n; i++) { const a = i / n * TAU + r() * 0.3, sc = sz * (0.75 + r() * 0.6), m = mesh(rgeo, rmat), R_ = rr * (0.93 + r() * 0.14);
        m.scale.set(sc * 1.3, sc * 0.75, sc * 1.1); m.position.set(Math.cos(a) * R_, yy + sc * 0.25, Math.sin(a) * R_); m.rotation.set(r() * 3, r() * 3, r() * 3); m.castShadow = false; cp.add(m); } };
      rockRing(C.rocksIn ?? 14, C.r0 * 1.15, C.rockIn ?? 0.42, dh * 0.08); rockRing(C.rocksOut ?? 24, C.r1 * 0.96, C.rockOut ?? 0.3, dh * 0.92);
      cp.add(dish); cp.position.y = yC; if (C.tilt) cp.rotation.x = C.tilt; g.add(cp); ribbons.push({ piv: cp, sp: C.spin ?? 2.0, ph: 0 });   // C.tilt: lean the dish (rad, -: away from a camera on +z)
    }
    if (o.lid) { // the aerial "lid": a flat tan debris annulus around the crown (seen from above as a pale ring)
      const topR = rad(N) * (o.crownFlare ?? 1.16), ring = mesh(new THREE.RingGeometry(topR * o.lid[0], topR * o.lid[1], 28, 1).rotateX(-PI / 2), mat(o.lidColor || '#D6C49E', { doubleSide: true }));
      ring.position.y = H * (1 + 0.6 / N); ring.castShadow = false; const lp = grp(ring); g.add(lp); ribbons.push({ piv: lp, sp: 2.2, ph: 0 });
    }
    if (o.rim) { // chunky low-poly rocks crowning the top ring (the reference's jagged rim, very visible from above)
      const top = rings[N - 1], topR = (rad(N) + 0.12) * (o.rimAt || 1), geo = new THREE.DodecahedronGeometry(1, 0), rm = mat(o.rimColor || '#5B655E');
      for (let i = 0; i < o.rim; i++) { const a = i / o.rim * TAU + r() * 0.25, s = (o.rimSize || 0.26) * (0.8 + r() * 0.6), m = mesh(geo, rm), rr = topR * (0.9 + r() * 0.16);
        m.scale.set(s * 1.4, s, s * 1.2); m.position.set(Math.cos(a) * rr, H / N * 1.3 * (0.8 + r() * 0.3), Math.sin(a) * rr); m.rotation.set(r() * 3, r() * 3, r() * 3); top.m.add(m); }
    }
    for (let i = 0; i < (o.ribbons || 0); i++) { // tan dust bands whipping round the top
      const yk = (o.ribbonY0 ?? 0.8) + r() * (o.ribbonDY ?? 0.22);
      const R = o.ribbonFollow ? (rad(Math.min(N, yk * N)) * (o.ribbonGap ?? 1.08) + 0.08) * (1.0 + r() * 0.06) : (o.ribbonR || (rad(N) + 0.12)) * (1.02 + r() * 0.5), arc = o.ribbonArc ? o.ribbonArc * (0.8 + r() * 0.4) : 1.6 + r() * 2.6;
      const m = o.ribbonFlat ? mesh(new THREE.RingGeometry(R, R + (0.08 + r() * 0.1) * (o.ribbonW || 1), 40, 1, 0, arc).rotateX(-PI / 2), mat(o.ribbonColor || '#D9C7A3', { doubleSide: true }))
        : mesh(new THREE.TorusGeometry(R, 0.035 + r() * 0.03, 3, 40, arc), mat(o.ribbonColor || '#D9C7A3', { doubleSide: true }));
      if (o.ribbonFlat) m.rotation.set((r() - 0.5) * (o.ribbonFlatTilt ?? 0.12), 0, (r() - 0.5) * (o.ribbonFlatTilt ?? 0.12)); else { m.rotation.x = PI / 2 + (r() - 0.5) * (o.ribbonTilt ?? 0.25); m.scale.z = o.ribbonH || 3.5; }
      m.castShadow = false; const piv = grp(m); piv.position.y = H * yk; g.add(piv); ribbons.push({ piv, sp: (o.ribbonSpeed || 5) + r() * 3, ph: r() * TAU });
    }
    if (o.dust) { const dm = mat(o.dustColor || '#CDB896'); for (let i = 0; i < 10; i++) { const a = i / 10 * TAU + r() * 0.3, s = (0.35 + r() * 0.35) * (o.dust === true ? 1 : o.dust), m = new THREE.Mesh(sphereGeo(1), dm);
      m.scale.set(s * 1.5, s * 0.55, s * 1.5); m.position.set(Math.cos(a) * (rad(0) + 0.35 + r() * 0.3), s * 0.25, Math.sin(a) * (rad(0) + 0.35 + r() * 0.3)); m.castShadow = false; dust.add(m); } }
    g.userData.update = t => {
      ribbons.forEach(({ piv, sp, ph }) => { piv.rotation.y = t * sp + ph; }); dust.rotation.y = t * 1.5; if (inner) inner.rotation.y = t * 1.3;
      const SP = o.spin ?? 1; rings.forEach(({ piv, m, sp, ph, i }) => { m.rotation.y = t * sp * SP * (1 + (o.spinJitter || 0) * Math.sin(t * 2.3 + i * 1.7)) + ph; piv.position.x = Math.sin(t * 1.6 + i * 0.45) * 0.2 * (i / N); piv.position.z = Math.cos(t * 1.3 + i * 0.5) * 0.12 * (i / N); });
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
  beerStream(o) { const h = o.length || 0.45, r = o.r || 0.012; const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r * (o.flare || 1.5), h, 8), new THREE.MeshLambertMaterial({ color: o.color || '#E6B44A', transparent: true, opacity: 0.85 })); m.position.y = -h / 2; return grp(m); },
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
    const rate = o.rate ?? 1 / 60, H0 = o.hours ?? 0; g.userData.update = t => { const turns = H0 + Math.min(t, o.until ?? 1e9) * rate; mh.rotation.z = -turns * Math.PI * 2; hh.rotation.z = -turns * Math.PI * 2 / 12; };   // o.hours: the time shown at t = 0 (8 = eight o'clock); o.until: the hands stop at that time (an hour that goes by in half a second)
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
    if (o.prc) { const draw = (c, W, H) => { c.fillStyle = '#DE2910'; c.fillRect(0, 0, W, H); c.fillStyle = '#FFDE00';
        const star = (x, y, r, rot) => { c.beginPath(); for (let i = 0; i < 10; i++) { const a = rot + i * PI / 5, rr = i % 2 ? r * 0.38 : r; c.lineTo(x + Math.sin(a) * rr, y - Math.cos(a) * rr); } c.closePath(); c.fill(); };
        const bx = W * 0.167, by = H * 0.25; star(bx, by, H * 0.15, 0); [[0.333, 0.1], [0.4, 0.2], [0.4, 0.35], [0.333, 0.45]].forEach(([x, y]) => star(W * x, H * y, H * 0.05, Math.atan2(bx - W * x, H * y - by))); };
      [-1, 1].forEach(sd => g.add(at(canvasPlane(0.6, 0.4, draw, { res: 256 }), 0.33, 1.38, sd * 0.0065, 0, sd < 0 ? PI : 0, 0))); }
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
  // ---- six classic stories: the alarm clock, the sun, the washing machine, the fridge camera, honey, the nest of eggs
  alarmClock(o) { // a huge twin-bell alarm clock with a digital face (o.time, then o.time2 from switchAt) and a snooze button on top;
                  // shakes between ringAt and stopAt
    const C = o.color || '#B5302A', face = t => canvasPlane(0.3, 0.14, (c, W, H) => { c.fillStyle = '#141414'; c.fillRect(0, 0, W, H); c.fillStyle = '#FF5A3A'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `bold ${H * 0.72}px monospace`; c.fillText(t, W / 2, H * 0.55); }, { res: 256, emissive: 0.9 });
    const f1 = face(o.time || '06:00'), f2 = face(o.time2 || '03:09'); f1.position.set(0, 0.2, 0.096); f2.position.copy(f1.position); f2.visible = false;
    const body = grp(at(box(0.42, 0.34, 0.18, C, { outline: 0.01 }), 0, 0.2, 0), at(box(0.34, 0.18, 0.02, '#1E1E22'), 0, 0.2, 0.082), f1, f2,
      at(box(0.06, 0.05, 0.06, '#2A2A2E'), -0.15, 0.02, 0), at(box(0.06, 0.05, 0.06, '#2A2A2E'), 0.15, 0.02, 0), at(box(0.2, 0.05, 0.12, '#F2C230', { outline: 0.006 }), 0, 0.39, 0),
      at(label(o.button ?? 'SNOOZE', 0.16, 0.035, { bg: '#F2C230', fg: '#1E1E22', wrap: false }), 0, 0.4, 0.061));   // o.button: the word on the button (a French film: 'ARRÊT')
    const bells = [-1, 1].map(s => { const b = grp(at(sphere(0.1, '#C9CCD1', 1), 0, 0, 0), rod([0, -0.05, 0], [0, -0.12, 0], 0.012, '#8C949A')); b.children[0].scale.y = 0.7; b.position.set(s * 0.17, 0.48, 0); body.add(b); return b; });
    const g = grp(body);
    g.userData.update = t => { const ring = o.ringAt != null && t >= o.ringAt && (o.stopAt == null || t < o.stopAt); body.rotation.z = ring ? 0.05 * Math.sin(t * 70) : 0; body.position.y = ring ? 0.01 * Math.abs(Math.sin(t * 55)) : 0;
      bells.forEach((b, i) => b.rotation.z = ring ? 0.25 * Math.sin(t * 90 + i) : 0); const sw = o.switchAt != null && t >= o.switchAt; f1.visible = !sw; f2.visible = sw; };
    g.userData.update(0); return g; },
  perfume(o) { // a perfume bottle with a gold cap and a spray head
    return grp(at(box(0.07, 0.09, 0.04, '#E89AB8', { outline: 0.004, opacity: 0.85 }), 0, 0.045, 0), at(cyl(0.012, 0.012, 0.02, '#D8A83A', 8), 0, 0.1, 0), at(box(0.026, 0.02, 0.026, '#D8A83A'), 0, 0.12, 0)); },
  jean(o) { // a pair of jeans folded over the hand (o.color)
    const c = o.color || '#3E5A8A'; return grp(at(box(0.3, 0.05, 0.22, c, { outline: 0.005 }), 0, 0, 0), at(box(0.12, 0.38, 0.04, c), -0.07, -0.2, 0.08), at(box(0.12, 0.38, 0.04, c), 0.07, -0.2, 0.08), at(box(0.3, 0.02, 0.01, '#C9A06A'), 0, 0.03, 0.111)); },
  sun(o) { // a big cartoon sun: emissive disc-sphere with rays (move it with keys)
    const R = o.r || 1.2, g = grp(at(sphere(R, '#FFD23A', 2, { emissive: '#FFB01A', noGrain: true }), 0, 0, 0));
    for (let i = 0; i < 12; i++) { const a = i * PI / 6, r = box(0.12 * R, 0.55 * R, 0.05, '#FFE07A', { emissive: '#FFC03A', noGrain: true }); r.position.set(Math.sin(a) * R * 1.35, Math.cos(a) * R * 1.35, 0); r.rotation.z = -a; g.add(r); }
    return g; },
  washingMachine(o) { // front-loading washing machine: the drum turns at spinRates[i] (rad/s) from spinAt[i]; door at the front;
                      // the drum window is a shallow dome in front of the body, so small things can live "inside" it
    const W = 0.62, H = 0.86, D = 0.62, yc = 0.42, R = 0.21, body = grp(at(box(W, H, D, '#F2F2EC', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0),
      at(box(W, 0.12, 0.02, '#D8DCDD'), 0, H - 0.07, D / 2 + 0.006), at(cyl(0.035, 0.035, 0.03, '#8C949A', 12), 0.2, H - 0.07, D / 2 + 0.02, PI / 2, 0, 0),
      at(box(0.14, 0.05, 0.01, '#9CE8A0', { emissive: '#3A8A40', noGrain: true }), -0.1, H - 0.07, D / 2 + 0.018),
      at(torus(R + 0.03, 0.035, '#C9CCD1', 8, 28), 0, yc, D / 2 + 0.035), at(cyl(R + 0.02, R + 0.02, 0.01, '#2A2A2E', 28), 0, yc, D / 2 + 0.006, PI / 2, 0, 0));
    const drum = grp(); drum.position.set(0, yc, D / 2 + 0.012);
    drum.add(at(cyl(R, R, 0.008, '#8C949A', 28), 0, 0, 0, PI / 2, 0, 0));
    for (let i = 0; i < 18; i++) { const a = i * TAU / 18, rr = (i % 2 ? 0.1 : 0.16); drum.add(at(cyl(0.012, 0.012, 0.01, '#5A5E66', 8), Math.cos(a) * rr, Math.sin(a) * rr, 0.003, PI / 2, 0, 0)); }
    [0, 1, 2].forEach(i => drum.add(at(box(0.05, 0.03, 0.02, '#C9CCD1'), Math.cos(i * TAU / 3) * (R - 0.03), Math.sin(i * TAU / 3) * (R - 0.03), 0.01, 0, 0, i * TAU / 3)));
    const lb = o.laundry ? at(box(0.16, 0.08, 0.03, o.laundry, { outline: 0.004 }), 0.02, -0.1, 0.02, 0, 0, 0.3) : null; if (lb) drum.add(lb);   // laundryAt: when it is put in
    body.add(drum, at(mesh(new THREE.SphereGeometry(R + 0.01, 24, 8, 0, TAU, 0, PI / 2), glassMat(0.2, '#DDEEF2')), 0, yc, D / 2 + 0.02, PI / 2, 0, 0)); const g = grp(body);
    const ts = [].concat(o.spinAt ?? []), rates = [].concat(o.spinRates ?? []);
    g.userData.update = t => { let a = 0, rate = 0; for (let i = 0; i < ts.length; i++) { const t0 = ts[i], t1 = i + 1 < ts.length ? ts[i + 1] : Infinity; if (t > t0) a += (Math.min(t, t1) - t0) * (rates[i] || 0); if (t >= t0 && t < t1) rate = rates[i] || 0; } drum.rotation.z = -a;
      const j = Math.min(1, Math.abs(rate) / 25) * (o.shake ?? 1); body.position.set(0.012 * j * Math.sin(t * 61), 0.006 * j * Math.abs(Math.sin(t * 47)), 0.008 * j * Math.sin(t * 53)); body.rotation.z = 0.012 * j * Math.sin(t * 43);   // vibrates on fast spins
      if (lb) lb.visible = o.laundryAt == null || t >= o.laundryAt; };
    g.userData.update(0); g.userData.drum = [0, yc, D / 2 + 0.03]; return g; },
  car(o) { // civilian car facing +x, see-through cabin so a driver shows (clip 'drive' at userData.seat); o.color, o.plate; o.convertible: an open-top limousine
    if (o.convertible) return B.convertible(o);
    const C = o.color || '#C9473A', g = grp(), gl = glassMat(o.glass ?? 0.07, '#E6F2F5');
    g.add(at(box(4.0, 0.56, 1.8, C, { outline: 0.012 }), 0, 0.63, 0), at(box(4.02, 0.16, 1.82, P.greyDark), 0, 0.42, 0),
      at(box(3.0, 0.07, 1.72, C, { outline: 0.008 }), -0.25, 2.02, 0));
    for (const z of [-0.84, 0.84]) g.add(at(box(0.07, 1.2, 0.07, C), 1.32, 1.46, z, 0, 0, 0.4), at(box(0.07, 1.16, 0.07, C), -1.72, 1.46, z, 0, 0, -0.3), at(box(0.06, 1.1, 0.06, C), -0.25, 1.46, z));
    g.add(at(mesh(new THREE.BoxGeometry(0.02, 1.2, 1.62), gl), 1.32, 1.46, 0, 0, 0, 0.4), at(mesh(new THREE.BoxGeometry(0.02, 1.16, 1.62), gl), -1.72, 1.46, 0, 0, 0, -0.3));
    for (const z of [-0.86, 0.86]) g.add(at(mesh(new THREE.BoxGeometry(2.85, 1.05, 0.02), gl), -0.25, 1.46, z));
    for (const z of [-0.4, 0.4]) g.add(at(box(0.5, 0.12, 0.48, '#3A3D44'), 0.05, 0.5, z), at(box(0.1, 0.62, 0.48, '#3A3D44'), -0.25, 0.82, z, 0, 0, 0.15));
    g.add(at(box(0.3, 0.3, 1.6, '#2A2A2E'), 0.95, 0.85, 0), at(torus(0.16, 0.025, P.ink, 6, 16), 0.62, 1.06, -0.4, 0, PI / 2, 0));
    for (const x of [-1.3, 1.3]) for (const z of [-0.8, 0.8]) g.add(at(cyl(0.34, 0.34, 0.26, P.ink, 12), x, 0.34, z, PI / 2), at(cyl(0.15, 0.15, 0.02, P.grey, 8), x, 0.34, z * 1.17, PI / 2));
    for (const z of [-0.6, 0.6]) g.add(at(box(0.04, 0.14, 0.32, '#FFF6C8', { noGrain: true }), 2.01, 0.74, z), at(box(0.04, 0.14, 0.32, P.red), -2.01, 0.74, z));
    for (const sx of [-1, 1]) g.add(at(label(o.plate || 'AB-123-CD', 0.52, 0.12, { bg: P.white, fg: P.ink, wrap: false }), sx * 2.012, 0.5, 0, 0, sx * PI / 2, 0));
    g.userData.seat = [0.05, 0.12, -0.4]; g.userData.seat2 = [0.05, 0.12, 0.4]; return g; },
  convertible(o) { // open-top car facing +x (a star's limousine): hollow tub, front bucket seats, a rear bench (userData.rear), chrome grille and bumpers,
    // a low windscreen; o.rearDoor (radians) or o.rearDoorAt (s) swings the right rear door (+z side) open; driver at userData.seat (clip 'drive')
    const C = o.color || '#1C1C22', g = grp(), gl = glassMat(o.glass ?? 0.1, '#E6F2F5'), CH = '#D9DDE2', IN = o.interior || '#C9A27A', y0 = 0.36, yt = 0.92;
    g.add(at(box(4.4, 0.14, 1.84, P.greyDark), 0, 0.42, 0), at(box(1.5, yt - y0, 1.84, C, { pivot: 'bottom', outline: 0.012 }), 1.45, y0, 0), at(box(0.95, yt - y0, 1.84, C, { pivot: 'bottom', outline: 0.012 }), -1.725, y0, 0),
      at(box(2.5, 0.1, 1.72, '#2A2A2E'), -0.0, y0 + 0.05, 0));                                  // hood, trunk, cabin floor
    g.add(at(box(1.0, yt - y0, 0.08, C, { pivot: 'bottom', outline: 0.008 }), 0.2, y0, -0.88), at(box(0.95, yt - y0, 0.08, C, { pivot: 'bottom', outline: 0.008 }), -0.775, y0, -0.88),
      at(box(1.0, yt - y0, 0.08, C, { pivot: 'bottom', outline: 0.008 }), 0.2, y0, 0.88));        // sides (the right rear door is separate)
    const door = grp(at(box(0.95, yt - y0, 0.08, C, { outline: 0.008 }), -0.475, (yt - y0) / 2, 0), at(box(0.12, 0.03, 0.03, CH), -0.82, (yt - y0) * 0.78, 0.05)); door.position.set(-0.3, y0, 0.88); g.add(door);
    for (const z of [-0.88, 0.88]) g.add(at(box(2.7, 0.04, 0.1, CH), -0.25, yt + 0.02, z));      // chrome trim
    const ws = grp(at(box(0.05, 0.05, 1.7, CH), 0, 0.22, 0), at(box(0.05, 0.04, 1.7, CH), 0, -0.22, 0), at(box(0.05, 0.48, 0.05, CH), 0, 0, -0.83), at(box(0.05, 0.48, 0.05, CH), 0, 0, 0.83),
      at(mesh(new THREE.BoxGeometry(0.015, 0.42, 1.6), gl), 0, 0, 0)); ws.position.set(0.68, yt + 0.22, 0); ws.rotation.z = 0.45; g.add(ws);   // windscreen: chrome frame + glass
    for (const z of [-0.4, 0.4]) g.add(at(box(0.5, 0.14, 0.5, IN), 0.15, 0.52, z), at(box(0.12, 0.62, 0.5, IN), -0.15, 0.84, z, 0, 0, 0.12));   // front seats
    g.add(at(box(0.55, 0.16, 1.56, IN), -1.0, 0.53, 0), at(box(0.14, 0.62, 1.6, IN), -1.36, 0.86, 0, 0, 0, 0.14));   // rear bench
    g.add(at(box(0.3, 0.3, 1.5, '#2A2A2E'), 0.5, 0.78, 0), at(torus(0.16, 0.025, P.ink, 6, 16), 0.42, 1.04, -0.4, 0, PI / 2, 0.35));   // dash + wheel
    g.add(at(box(0.06, 0.34, 1.0, '#1C1C20'), 2.205, 0.66, 0)); for (let i = 0; i < 6; i++) g.add(at(box(0.065, 0.3, 0.02, CH), 2.21, 0.66, -0.4 + i * 0.16));   // grille
    for (const sx of [-1, 1]) g.add(at(box(0.08, 0.1, 1.9, CH), sx * 2.22, 0.42, 0));            // bumpers
    for (const x of [-1.38, 1.38]) for (const z of [-0.82, 0.82]) g.add(at(cyl(0.36, 0.36, 0.26, P.ink, 12), x, 0.36, z, PI / 2), at(cyl(0.17, 0.17, 0.02, CH, 8), x, 0.36, z * 1.17, PI / 2));
    for (const z of [-0.66, 0.66]) g.add(at(cyl(0.11, 0.11, 0.04, '#FFF6C8', 10, { noGrain: true }), 2.2, 0.74, z, 0, 0, PI / 2), at(box(0.04, 0.12, 0.3, P.red), -2.21, 0.74, z));
    for (const sx of [-1, 1]) g.add(at(label(o.plate || 'AB-123-CD', 0.72, 0.17, { bg: P.white, fg: P.ink, wrap: false }), sx * 2.27, 0.55, 0, 0, sx * PI / 2, 0));
    g.userData.update = t => { const a = o.rearDoorAt != null ? (o.rearDoor ?? 1.1) * ease.outBack(clamp01((t - o.rearDoorAt) / 0.45)) : (o.rearDoor || 0); door.rotation.y = a; };
    g.userData.update(0); g.userData.seat = [0.15, 0.12, -0.4]; g.userData.seat2 = [0.15, 0.12, 0.4]; g.userData.rear = [-1.0, 0.61, 0]; return g; },
  brickWall(o) { // a low brick wall along x (o.w, o.h): bricks drawn on both faces, a cap on top
    const w = o.w || 2, h = o.h || 1.2, t = 0.22, col = o.color || '#B5532E';
    const face = () => canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#E2D6C2'; c.fillRect(0, 0, W, H); const bw = W / (w / 0.26), bh = H / (h / 0.09); c.fillStyle = col;
      for (let r = 0; r * bh < H; r++) for (let k = -1; k * bw < W; k++) { const x = k * bw + (r % 2 ? bw / 2 : 0); c.fillRect(x + 2, r * bh + 2, bw - 4, bh - 4); } }, { res: Math.min(1024, Math.round(256 * w)) });
    const f = face(), b = face(); f.position.set(0, h / 2, t / 2 + 0.003); b.position.set(0, h / 2, -t / 2 - 0.003); b.rotation.y = PI;
    return grp(at(box(w, h, t, col, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), f, b, at(box(w + 0.04, 0.05, t + 0.05, '#CFC3AE'), 0, h + 0.025, 0)); },
  broom(o) { // household broom along +y, bristles at the top end (held overhead with rot [π,0,0] it pokes the ceiling)
    const g = grp(cyl(0.018, 0.018, 1.3, o.color || '#C9A06A', 6, { pivot: 'bottom' }), at(box(0.3, 0.08, 0.06, '#C23A2E', { outline: 0.005 }), 0, 1.33, 0), at(box(0.28, 0.13, 0.05, '#E6C46A'), 0, 1.43, 0));
    g.userData.grip = [0, o.grip ?? 0.95, 0]; return g; },
  floorSlab(o) { // floor/ceiling slab seen in cross-section (o.w x o.d, 0.28 thick): floor on top, plaster below, a ceiling lamp that swings; shakes at shakeAt
    const w = o.w || 6, d = o.d || 4, t = 0.28, body = grp(at(box(w, t, d, '#D8D2C4', { outline: 0.01 }), 0, 0, 0), at(box(w, 0.02, d, o.floor || '#B08A64'), 0, t / 2 + 0.01, 0));
    let lamp = null; if (o.lamp !== false) { lamp = grp(rod([0, 0, 0], [0, -0.42, 0], 0.01, P.ink), at(cyl(0.05, 0.2, 0.16, o.lampColor || '#F2C230', 10), 0, -0.5, 0), at(sphere(0.06, '#FFF2C0', 1, { emissive: '#FFE08A', noGrain: true }), 0, -0.58, 0)); lamp.position.set(o.lampX ?? 0, -t / 2, o.lampZ ?? 0); body.add(lamp); }
    const g = grp(body), sh = [].concat(o.shakeAt ?? []);
    g.userData.update = tt => { const s = sh.some(a => tt >= a && tt < a + 0.4); body.position.set(s ? 0.025 * Math.sin(tt * 70) : 0, s ? 0.02 * Math.sin(tt * 55) : 0, 0); if (lamp) lamp.rotation.z = (o.swing ?? 0.12) * Math.sin(tt * (o.swingRate ?? 4.5)); };
    g.userData.update(0); return g; },
  pedometer(o) { // handheld step counter with a big LCD: o.value fixed, or counting up from o.start at o.rate steps/s from countAt; held like a phone
    const lcd = v => { const p = canvasPlane(0.09, 0.06, (c, W, H) => { c.fillStyle = '#B8C9A0'; c.fillRect(0, 0, W, H); c.fillStyle = '#1E2A18'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `bold ${H * 0.46}px monospace`; c.fillText(String(v), W / 2, H * 0.42); c.font = `bold ${H * 0.18}px Arial`; c.fillText(o.label || 'PAS', W / 2, H * 0.84); }, { res: 256 }); p.position.set(0, 0.02, 0.0158); return p; };
    const frames = o.countAt != null ? Array.from({ length: 12 }, (_, i) => lcd((o.start ?? 0) + i)) : [lcd(o.value ?? '9 999')];
    frames.forEach((f, i) => f.visible = i === 0);
    const g = grp(at(box(0.11, 0.15, 0.025, o.color || '#2E7D5B', { outline: 0.004 }), 0, 0, 0), at(box(0.098, 0.072, 0.004, '#141414'), 0, 0.02, 0.012), ...frames, at(cyl(0.013, 0.013, 0.01, '#E8E2D0', 8), 0, -0.048, 0.013, PI / 2));
    if (o.countAt != null) g.userData.update = t => { const i = t < o.countAt ? 0 : Math.min(11, Math.floor((t - o.countAt) * (o.rate || 2))); frames.forEach((f, j) => f.visible = j === i); };
    g.userData.grip = [0, -0.06, 0]; return g; },
  rubberStamp(o) { const g = grp(at(box(0.1, 0.03, 0.065, '#2A2A2E'), 0, 0.015, 0), at(box(0.06, 0.05, 0.04, '#5A3A28'), 0, 0.055, 0), at(sphere(0.035, o.color || '#C23A2E', 1), 0, 0.1, 0)); g.userData.grip = [0, 0.09, 0]; return g; },
  stampMark(o) { // red rubber-stamp mark (o.text) with a transparent surround; lay it on a sheet or face the camera
    const w = o.w || 0.3, h = o.h || 0.11, col = o.color || '#C8202A';
    return grp(canvasPlane(w, h, (c, W, H) => { c.clearRect(0, 0, W, H); const lw = Math.min(W, H) * 0.09; c.strokeStyle = col; c.lineWidth = lw; c.strokeRect(lw, lw, W - 2 * lw, H - 2 * lw); c.fillStyle = col; c.textAlign = 'center'; c.textBaseline = 'middle';
      const lines = String(o.text || 'REFUSÉ').split('\n'), n = lines.length; let fs = (H - 4 * lw) / n * 0.82; c.font = `900 ${fs}px Arial`; const mw = Math.max(...lines.map(t => c.measureText(t).width)); if (mw > W * 0.86) fs *= W * 0.86 / mw;
      c.font = `900 ${fs}px Arial`; lines.forEach((t, i) => c.fillText(t, W / 2, H / 2 + (i - (n - 1) / 2) * fs * 1.05 + fs * 0.05)); }, { res: 512, transparent: true })); },   // o.text may hold several lines
  idPhoto(o) { // passport photo of the mec (o.smile), light-blue background, white border; scale it up for inserts
    const c = canvasPlane(0.07, 0.09, (g2, W, H) => { g2.fillStyle = '#DCE8F2'; g2.fillRect(0, 0, W, H);
      g2.fillStyle = '#1E2A3A'; g2.fillRect(W * 0.12, H * 0.8, W * 0.76, H * 0.2); g2.fillStyle = '#F2F2EC'; g2.fillRect(W * 0.42, H * 0.8, W * 0.16, H * 0.2); g2.fillStyle = '#C23A2E'; g2.fillRect(W * 0.47, H * 0.82, W * 0.06, H * 0.18);
      g2.fillStyle = o.skin || '#E2B07E'; g2.fillRect(W * 0.31, H * 0.12, W * 0.38, H * 0.66); g2.fillStyle = '#1A1A1A'; g2.fillRect(W * 0.29, H * 0.08, W * 0.42, H * 0.12);
      g2.fillRect(W * 0.39, H * 0.37, W * 0.05, H * 0.03); g2.fillRect(W * 0.56, H * 0.37, W * 0.05, H * 0.03); g2.fillStyle = '#B07A50'; g2.fillRect(W * 0.485, H * 0.42, W * 0.03, H * 0.1);
      g2.strokeStyle = '#3A1A10'; g2.lineWidth = W * 0.03; g2.lineCap = 'round'; g2.beginPath();
      if (o.smile) g2.arc(W * 0.5, H * 0.53, W * 0.1, 0.12 * PI, 0.88 * PI); else { g2.moveTo(W * 0.42, H * 0.64); g2.lineTo(W * 0.58, H * 0.64); } g2.stroke(); }, { res: 256 });
    const g = grp(at(box(0.078, 0.098, 0.002, P.white), 0, 0, 0), at(c, 0, 0, 0.0015)); g.userData.grip = [0, -0.04, 0]; return g; },
  photoBooth(o) { // photo booth facing +z: cabin, curtain on the right half, stool (actor at userData.seat, clip 'sit'), "PHOTO" sign, a flash inside at flashAt
    const W = 1.1, H = 2.0, D = 1.0, c = o.color || '#2C4A8A', g = grp(), fm = mat('#F2F2EC', { unique: true, noGrain: true }), fls = [].concat(o.flashAt ?? []);
    g.add(at(box(W, H, 0.06, c, { pivot: 'bottom', outline: 0.008 }), 0, 0, -D / 2), at(box(0.06, H, D, c, { pivot: 'bottom', outline: 0.008 }), -W / 2, 0, 0),
      at(box(0.06, H, D, c, { pivot: 'bottom', outline: 0.008 }), W / 2, 0, 0), at(box(W + 0.08, 0.08, D + 0.04, c), 0, H, 0),
      at(box(0.95, 0.3, 0.06, '#1E2A3A'), 0, H + 0.2, D / 2 - 0.05), at(label(o.text || 'PHOTO', 0.9, 0.26, { bg: '#F2C230', fg: '#1E2A3A', wrap: false }), 0, H + 0.2, D / 2 - 0.015),
      at(box(0.16, 1.55, 0.05, o.curtain || '#C23A2E', { pivot: 'bottom' }), W / 2 - 0.1, 0.35, D / 2 + 0.03), at(box(W, 0.04, 0.04, P.grey), 0, 1.92, D / 2 + 0.02),
      at(cyl(0.18, 0.2, 0.06, '#2A2A2E', 10), 0, 0.45, -0.1), at(cyl(0.04, 0.05, 0.42, P.grey, 6, { pivot: 'bottom' }), 0, 0, -0.1),
      at(box(0.3, 0.22, 0.04, '#141414'), 0, 1.32, -D / 2 + 0.05), at(cyl(0.05, 0.05, 0.03, '#3A5A7A', 10), 0, 1.32, -D / 2 + 0.08, PI / 2),
      at(new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.06, 0.02), fm), 0, 1.52, -D / 2 + 0.07), at(box(0.18, 0.03, 0.05, '#141414'), W / 2 + 0.03, 1.0, 0.25));
    g.userData.update = t => { const on = fls.some(f => t >= f && t < f + 0.1); fm.emissive.set(on ? '#FFFFFF' : '#000000'); };
    g.userData.update(0); g.userData.seat = [0, 0.12, -0.1]; g.userData.lens = [0, 1.32, -D / 2 + 0.1]; return g; },
  mugshotBoard(o) { // police mugshot wall: height lines every 10 cm with labels, against a wall (o.w x o.h)
    const w = o.w || 1.6, h = o.h || 2.3;
    const c = canvasPlane(w, h, (g2, W, H) => { g2.fillStyle = '#E9ECEF'; g2.fillRect(0, 0, W, H); g2.fillStyle = '#2A2A2E'; g2.textAlign = 'left'; g2.textBaseline = 'middle'; g2.font = `bold ${H * 0.026}px Arial`;
      for (let cm = 100; cm <= 220; cm += 10) { const y = H * (1 - cm / 100 / h); g2.fillRect(0, y - H * 0.002, W, H * (cm % 50 === 0 ? 0.006 : 0.003)); g2.fillText(`${Math.floor(cm / 100)}m${String(cm % 100).padStart(2, '0')}`, W * 0.03, y - H * 0.016); } }, { res: 512 });
    return grp(at(box(w + 0.06, h + 0.06, 0.03, '#9CA3A8'), 0, h / 2, 0), at(c, 0, h / 2, 0.017)); },
  placard(o) { // black mugshot board with white text, held at chest height (HAND_FLAT)
    const c = canvasPlane(0.42, 0.2, (g2, W, H) => { g2.fillStyle = '#141414'; g2.fillRect(0, 0, W, H); g2.fillStyle = '#F2F2EC'; g2.textAlign = 'center'; g2.textBaseline = 'middle';
      const L = String(o.text || 'POLICE\n38-2026').split('\n'); g2.font = `bold ${H * 0.3}px monospace`; L.forEach((l, i) => g2.fillText(l, W / 2, H * (0.3 + i * 0.4))); }, { res: 256 });
    const g = grp(at(box(0.43, 0.21, 0.015, '#2A2A2E'), 0, 0, 0), at(c, 0, 0, 0.009)); g.userData.grip = [0, -0.09, 0]; return g; },
  selfCheckout(o) { // self-checkout kiosk: screen (BIENVENUE, then the red alert from alertAt), scanner glass, and a wide low bagging scale on its right (+x)
    const scr = (txt, bg, fg) => { const p = canvasPlane(0.42, 0.3, (c, W, H) => { c.fillStyle = bg; c.fillRect(0, 0, W, H); c.fillStyle = fg; c.textAlign = 'center'; c.textBaseline = 'middle'; const L = String(txt).split('\n'); c.font = `900 ${H * (L.length > 2 ? 0.13 : 0.18)}px Arial`; L.forEach((l, i) => c.fillText(l, W / 2, H * (0.5 + (i - (L.length - 1) / 2) * 0.2))); }, { res: 256, emissive: 0.6 }); p.position.set(0, 1.42, 0.13); p.rotation.x = -0.25; return p; };
    const ok = scr(o.text || 'BIENVENUE', '#2C6E49', '#F6F1E3'), bad = scr(o.alert || 'ARTICLE\nINATTENDU\nZONE\nD\'ENSACHAGE', '#B5302A', '#F6F1E3'); bad.visible = false;
    const lamp = mat('#5A1A14', { unique: true, noGrain: true });
    const g = grp(at(box(0.7, 0.95, 0.55, '#E6E2D8', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(box(0.66, 0.04, 0.5, '#2A2A2E'), 0, 0.97, 0.01),
      at(box(0.3, 0.02, 0.22, '#141414', { emissive: '#3A0A0A' }), -0.12, 0.995, 0.05), at(box(0.06, 0.45, 0.06, P.grey), 0, 1.2, -0.02),
      at(box(0.46, 0.34, 0.05, '#2A2A2E', { outline: 0.006 }), 0, 1.42, 0.1, -0.25, 0, 0), ok, bad,
      at(box(1.0, 0.18, 0.95, '#C9CCD1', { pivot: 'bottom', outline: 0.008 }), 0.95, 0, 0.1), at(box(0.96, 0.02, 0.9, '#9CA3A8'), 0.95, 0.19, 0.1),
      rod([0.5, 0.19, -0.3], [0.5, 1.1, -0.3], 0.02, P.grey), rod([1.4, 0.19, -0.3], [1.4, 1.1, -0.3], 0.02, P.grey), rod([0.5, 1.1, -0.3], [1.4, 1.1, -0.3], 0.02, P.grey),
      at(label(o.zone || 'ZONE D\'ENSACHAGE', 0.8, 0.12, { bg: '#F2C230', fg: '#1E1E22', wrap: false }), 0.95, 1.18, -0.3),
      rod([0.32, 0.97, -0.2], [0.32, 1.85, -0.2], 0.015, P.grey), at(new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.12, 10), lamp), 0.32, 1.9, -0.2));
    g.userData.update = t => { const a = o.alertAt != null && t >= o.alertAt && (o.alertEndAt == null || t < o.alertEndAt); ok.visible = !a; bad.visible = a; const on = a && Math.floor(t * 4) % 2 === 0; lamp.color.set(on ? '#FF3A2A' : '#5A1A14'); lamp.emissive.set(on ? '#FF2A1A' : '#000000'); };
    g.userData.update(0); g.userData.scale = [0.95, 0.2, 0.1]; return g; },
  vitrine(o) { // china cabinet with a glass front: plates on side shelves, a tall empty middle compartment (someone can stand in it)
    const w = o.w || 1.5, h = o.h || 2.1, d = 0.55, c = o.color || '#8A5A3A', g = grp(at(box(w, 0.08, d, c, { outline: 0.008 }), 0, 0.04, 0), at(box(w, 0.08, d, c, { outline: 0.008 }), 0, h, 0),
      at(box(0.06, h, d, c), -w / 2, h / 2, 0), at(box(0.06, h, d, c), w / 2, h / 2, 0), at(box(w, h, 0.03, '#C9B48A'), 0, h / 2, -d / 2), at(box(0.04, h, d, c), -w / 2 + 0.36, h / 2, 0), at(box(0.04, h, d, c), w / 2 - 0.36, h / 2, 0));
    for (const sx of [-1, 1]) for (let i = 0; i < 4; i++) { const x = sx * (w / 2 - 0.18), y = 0.45 + i * 0.45; g.add(at(box(0.32, 0.025, d - 0.05, c), x, y, 0)); for (let k = 0; k < 2; k++) g.add(at(cyl(0.11, 0.11, 0.015, P.white, 14), x, y + 0.13, -0.12 + k * 0.03, 1.3, 0, 0)); }
    g.add(at(mesh(new THREE.BoxGeometry(w, h, 0.015), glassMat(0.16, '#DDEEF2')), 0, h / 2, d / 2), at(box(0.025, h, 0.03, c), 0, h / 2, d / 2 + 0.01));
    return g; },
  catBasket(o) { // round pet basket with a cushion (scale it up for a person)
    const c = o.color || '#C49A66'; return grp(at(torus(0.3, 0.07, c, 8, 18), 0, 0.1, 0, PI / 2, 0, 0), at(cyl(0.32, 0.3, 0.06, c, 18), 0, 0.03, 0), at(cyl(0.27, 0.27, 0.08, o.cushion || '#B5302A', 18), 0, 0.08, 0)); },
  pcMonitor(o) { // office computer with a face on the screen: calm, then angry from angryAt; a keyboard in front
    const face = mood => { const p = canvasPlane(0.5, 0.31, (c, W, H) => { c.fillStyle = '#2C6EB5'; c.fillRect(0, 0, W, H); c.fillStyle = '#F6F1E3'; c.strokeStyle = '#F6F1E3'; c.lineWidth = H * 0.06; c.lineCap = 'round';
        const ey = H * 0.4; if (mood === 'angry') { c.beginPath(); c.moveTo(W * 0.28, ey - H * 0.14); c.lineTo(W * 0.42, ey - H * 0.04); c.moveTo(W * 0.72, ey - H * 0.14); c.lineTo(W * 0.58, ey - H * 0.04); c.stroke(); }
        c.beginPath(); c.arc(W * 0.36, ey + H * 0.04, H * 0.06, 0, TAU); c.arc(W * 0.64, ey + H * 0.04, H * 0.06, 0, TAU); c.fill();
        c.beginPath(); if (mood === 'angry') c.arc(W / 2, H * 0.86, W * 0.12, 1.15 * PI, 1.85 * PI); else c.arc(W / 2, H * 0.6, W * 0.1, 0.15 * PI, 0.85 * PI); c.stroke(); }, { res: 256, emissive: 0.7 }); p.position.set(0, 0.42, 0.028); return p; };
    const calm = face('calm'), angry = face('angry'); angry.visible = false;
    const g = grp(at(box(0.56, 0.37, 0.05, '#2A2A2E', { outline: 0.008 }), 0, 0.42, 0), calm, angry, at(box(0.06, 0.2, 0.05, '#2A2A2E'), 0, 0.15, -0.02), at(box(0.25, 0.02, 0.18, '#2A2A2E'), 0, 0.01, 0),
      at(box(0.45, 0.025, 0.15, '#3A3D44', { outline: 0.004 }), 0, 0.012, 0.25));
    g.userData.update = t => { const a = o.angryAt != null && [].concat(o.angryAt).some((x, i, arr) => t >= x && t < x + (o.angryFor ?? 1.2)); calm.visible = !a; angry.visible = a; };
    g.userData.update(0); return g; },
  laptop(o) { // open laptop: o.text on the screen (o.bg / o.fg), keyboard base
    const scr = canvasPlane(0.34, 0.21, (c, W, H) => { c.fillStyle = o.bg || '#F2F2EC'; c.fillRect(0, 0, W, H); c.fillStyle = o.fg || '#B5302A'; c.textAlign = 'center'; c.textBaseline = 'middle'; const L = String(o.text || 'MOT DE PASSE\nINCORRECT').split('\n'); c.font = `900 ${H * 0.17}px Arial`; L.forEach((l, i) => c.fillText(l, W / 2, H * (0.5 + (i - (L.length - 1) / 2) * 0.24))); }, { res: 256, emissive: 0.5 });
    const lid = grp(at(box(0.37, 0.24, 0.015, '#3A3D44', { outline: 0.004 }), 0, 0.12, 0), at(scr, 0, 0.12, 0.009)); lid.rotation.x = -0.25;
    return grp(at(box(0.37, 0.018, 0.25, '#3A3D44', { outline: 0.004 }), 0, 0.009, 0.12), at(box(0.32, 0.004, 0.13, '#1E1E22'), 0, 0.02, 0.1), lid); },
  doorKeypad(o) { // keypad box for a door (o.text on its small screen)
    const scr = canvasPlane(0.12, 0.05, (c, W, H) => { c.fillStyle = '#141414'; c.fillRect(0, 0, W, H); c.fillStyle = o.fg || '#FF5A3A'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `bold ${H * 0.36}px monospace`; String(o.text || 'MOT DE PASSE ?').split('\n').forEach((l, i, a) => c.fillText(l, W / 2, H * (0.5 + (i - (a.length - 1) / 2) * 0.42))); }, { res: 256, emissive: 0.8 });
    const g = grp(at(box(0.16, 0.24, 0.03, '#2A2A2E', { outline: 0.004 }), 0, 0, 0), at(scr, 0, 0.07, 0.016));
    for (let r = 0; r < 3; r++) for (let k = 0; k < 3; k++) g.add(at(box(0.03, 0.025, 0.01, '#C9CCD1'), -0.04 + k * 0.04, 0.0 - r * 0.035, 0.018)); return g; },
  stanchions(o) { // museum posts with a red velvet rope (o.w apart)
    const w = o.w || 1.6, post = x => grp(at(cyl(0.12, 0.14, 0.04, '#C9A64A', 12), x, 0.02, 0), at(cyl(0.025, 0.025, 0.92, '#C9A64A', 8, { pivot: 'bottom' }), x, 0, 0), at(sphere(0.045, '#C9A64A', 1), x, 0.95, 0));
    const g = grp(post(-w / 2), post(w / 2)); const N = 10; for (let i = 0; i < N; i++) { const a = i / N, b = (i + 1) / N, y = k => 0.88 - 0.18 * Math.sin(PI * k); g.add(rod([-w / 2 + a * w, y(a), 0], [-w / 2 + b * w, y(b), 0], 0.018, '#9A1E28')); } return g; },
  gpsDevice(o) { // dashboard GPS: map + arrow + o.text
    const scr = canvasPlane(0.16, 0.1, (c, W, H) => { c.fillStyle = '#9CC8A0'; c.fillRect(0, 0, W, H); c.fillStyle = '#E6E2D8'; c.fillRect(W * 0.4, 0, W * 0.2, H); c.fillRect(W * 0.4, H * 0.35, W * 0.6, H * 0.2); c.fillStyle = '#2C6EB5';
      c.beginPath(); c.moveTo(W * 0.5, H * 0.55); c.lineTo(W * 0.62, H * 0.9); c.lineTo(W * 0.38, H * 0.9); c.fill(); c.fillStyle = '#1E1E22'; c.fillRect(0, 0, W, H * 0.22); c.fillStyle = '#F6F1E3'; c.font = `bold ${H * 0.17}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.text || '→ 200 m', W / 2, H * 0.11); }, { res: 256, emissive: 0.6 });
    return grp(at(box(0.18, 0.12, 0.025, '#1E1E22', { outline: 0.004 }), 0, 0, 0), at(scr, 0, 0, 0.0135), rod([0, -0.06, -0.01], [0, -0.14, -0.06], 0.008, '#2A2A2E')); },
  iceCreamCart(o) { // beach ice-cream cart: box on wheels with a sign, a parasol pole
    return grp(at(box(1.1, 0.75, 0.6, '#F2F2EC', { pivot: 'bottom', outline: 0.008 }), 0, 0.18, 0), at(box(1.12, 0.12, 0.62, '#E8778A'), 0, 0.88, 0), at(cyl(0.18, 0.18, 0.06, P.ink, 10), -0.4, 0.18, 0.32, PI / 2), at(cyl(0.18, 0.18, 0.06, P.ink, 10), 0.4, 0.18, 0.32, PI / 2),
      at(label(o.text || 'GLACES', 0.8, 0.22, { bg: '#E8778A', fg: '#F6F1E3', wrap: false }), 0, 0.6, 0.302), rod([0.45, 0.94, -0.2], [0.45, 2.2, -0.2], 0.02, P.grey),
      at(mesh(new THREE.ConeGeometry(0.9, 0.35, 10), mat('#F2C230')), 0.45, 2.3, -0.2)); },
  iceCream(o) { const g = grp(at(mesh(new THREE.ConeGeometry(0.035, 0.12, 8), mat('#D9A35C')), 0, -0.06, 0, PI, 0, 0), at(sphere(0.045, o.color || '#F2B8D0', 1), 0, 0.02, 0)); g.userData.grip = [0, -0.07, 0]; return g; },
  elevator(o) { // elevator cabin (front = +z): glass walls (o.glass) so the rider shows, sliding doors (openAt / closeAt), a floor display counting up from countAt
    const W = 1.6, H = 2.4, D = 1.5, c = o.color || '#9CA3A8', gl = glassMat(o.glass ? 0.12 : 0.9, o.glass ? '#DDEEF2' : c), g = grp();
    g.add(at(box(W, 0.12, D, c, { outline: 0.008 }), 0, 0.06, 0), at(box(W, 0.12, D, c, { outline: 0.008 }), 0, H, 0), at(mesh(new THREE.BoxGeometry(0.03, H, D), gl), -W / 2, H / 2, 0), at(mesh(new THREE.BoxGeometry(0.03, H, D), gl), W / 2, H / 2, 0),
      at(mesh(new THREE.BoxGeometry(W, H, 0.03), gl), 0, H / 2, -D / 2), at(box(0.08, H, 0.08, c), -W / 2, H / 2, D / 2), at(box(0.08, H, 0.08, c), W / 2, H / 2, D / 2),
      at(box(0.18, 0.4, 0.03, '#2A2A2E'), W / 2 - 0.2, 1.2, D / 2 - 0.12, 0, PI, 0));
    const doors = [-1, 1].map(s => { const d = o.glass ? at(mesh(new THREE.BoxGeometry(W / 2 - 0.05, H - 0.14, 0.03), glassMat(0.2, '#DDEEF2')), s * W / 4, H / 2, D / 2 + 0.02) : at(box(W / 2 - 0.05, H - 0.14, 0.03, '#C9CCD1', { outline: 0.006 }), s * W / 4, H / 2, D / 2 + 0.02); g.add(d); return d; });
    const disp = n => { const p = canvasPlane(0.4, 0.16, (c2, W2, H2) => { c2.fillStyle = '#141414'; c2.fillRect(0, 0, W2, H2); c2.fillStyle = '#FF5A3A'; c2.textAlign = 'center'; c2.textBaseline = 'middle'; c2.font = `bold ${H2 * 0.7}px monospace`; c2.fillText(String(n), W2 / 2, H2 * 0.55); }, { res: 256, emissive: 0.9 }); p.position.set(0, H + 0.2, D / 2 + 0.01); return p; };
    const vals = [].concat(o.floors ?? [0, 1, 2, 3, 4, 7, 10, 25, 99, '∞']), frames = vals.map(disp); frames.forEach((f, i) => { f.visible = i === 0; g.add(f); });
    g.add(at(box(0.44, 0.2, 0.03, '#2A2A2E'), 0, H + 0.2, D / 2 - 0.01));
    g.userData.update = t => { const op = o.openAt != null && t >= o.openAt && (o.closeAt == null || t < o.closeAt); doors.forEach((d, i) => d.position.x = (i ? 1 : -1) * (W / 4 + (op ? W / 2 - 0.1 : 0)));
      const i = o.countAt == null || t < o.countAt ? 0 : Math.min(frames.length - 1, Math.floor((t - o.countAt) * (o.rate || 2.5))); frames.forEach((f, j) => f.visible = j === i); };
    g.userData.update(0); return g; },
  moonSurface(o) { // grey lunar ground disc with craters (spaceVoid has no floor)
    const R = o.r || 30, g = grp(at(cyl(R, R, 0.2, '#B8B6AE', 40), 0, -0.1, 0)), r = rng(o.seed || 12);
    for (let i = 0; i < 26; i++) { const a = r() * TAU, d = 2 + r() * (R - 4), s = 0.4 + r() * 1.6; g.add(at(torus(s, s * 0.18, '#9E9C94', 6, 16), Math.cos(a) * d, 0.02, Math.sin(a) * d, PI / 2, 0, 0), at(cyl(s * 0.9, s * 0.9, 0.02, '#A8A69E', 16), Math.cos(a) * d, 0.005, Math.sin(a) * d)); }
    return g; },
  avisPassage(o) { // yellow "avis de passage" slip
    const c = canvasPlane(0.15, 0.1, (g2, W, H) => { g2.fillStyle = '#F2D45A'; g2.fillRect(0, 0, W, H); g2.fillStyle = '#1E1E22'; g2.textAlign = 'center'; g2.font = `bold ${H * 0.16}px Arial`; g2.fillText(o.title || 'AVIS DE PASSAGE', W / 2, H * 0.24); g2.font = `${H * 0.12}px Arial`;
      String(o.text || 'Vous étiez absent.\nLe technicien\nrepassera.').split('\n').forEach((l, i) => g2.fillText(l, W / 2, H * (0.48 + i * 0.17))); }, { res: 256 });
    return grp(at(box(0.152, 0.102, 0.002, '#F2D45A'), 0, 0, 0), at(c, 0, 0, 0.0015)); },
  fountain(o) { // park fountain: round basin with water, a column, a bowl and spouts; coins in the water
    const R = o.r || 1.4, g = grp(at(torus(R, 0.16, '#C9C2B2', 8, 32), 0, 0.42, 0, PI / 2, 0, 0), at(cyl(R + 0.1, R + 0.15, 0.38, '#B8B0A0', 32, { pivot: 'bottom' }), 0, 0, 0),
      at(cyl(R - 0.05, R - 0.05, 0.02, '#7FB8C8', 32, { opacity: 0.85 }), 0, 0.39, 0), at(cyl(0.16, 0.22, 1.2, '#C9C2B2', 12, { pivot: 'bottom' }), 0, 0.38, 0),
      at(cyl(0.55, 0.25, 0.22, '#C9C2B2', 16, { outline: 0.006 }), 0, 1.65, 0), at(cyl(0.5, 0.5, 0.02, '#7FB8C8', 16), 0, 1.75, 0), at(sphere(0.12, '#C9C2B2', 1), 0, 1.85, 0));
    for (let i = 0; i < 6; i++) { const a = i * TAU / 6; g.add(rod([Math.cos(a) * 0.45, 1.68, Math.sin(a) * 0.45], [Math.cos(a) * 1.0, 0.42, Math.sin(a) * 1.0], 0.025, '#BFE3EE')); }
    const r = rng(o.seed || 5); for (let i = 0; i < 9; i++) { const a = r() * TAU, d = 0.4 + r() * (R - 0.6); g.add(at(cyl(0.03, 0.03, 0.006, '#E0B84A', 8), Math.cos(a) * d, 0.405, Math.sin(a) * d)); }
    return g; },
  cheque(o) { // a bank cheque (o.amount, o.text)
    const c = canvasPlane(0.2, 0.09, (g2, W, H) => { g2.fillStyle = '#E8F0E4'; g2.fillRect(0, 0, W, H); g2.fillStyle = '#2C4A3A'; g2.font = `bold ${H * 0.14}px Arial`; g2.textAlign = 'left'; g2.fillText(o.bank || 'BANQUE', W * 0.04, H * 0.2);
      g2.textAlign = 'right'; g2.font = `bold ${H * 0.2}px Arial`; g2.fillText(o.amount || '2 000,00 €', W * 0.96, H * 0.24); g2.textAlign = 'left'; g2.font = `${H * 0.12}px Arial`; g2.fillText(o.text || 'Payez contre ce chèque : deux mille euros', W * 0.04, H * 0.5);
      g2.strokeStyle = '#2C4A3A'; g2.lineWidth = H * 0.03; g2.beginPath(); g2.moveTo(W * 0.62, H * 0.82); for (let i = 0; i < 6; i++) g2.lineTo(W * (0.64 + i * 0.05), H * (i % 2 ? 0.68 : 0.86)); g2.stroke(); }, { res: 384 });
    const g = grp(at(box(0.202, 0.092, 0.002, '#E8F0E4'), 0, 0, 0), at(c, 0, 0, 0.0015)); g.userData.grip = [-0.09, 0, 0]; return g; },
  lawnmower(o) { // push mower: deck, wheels, handle; shakes while running (runAt..stopAt)
    const body = grp(at(box(0.5, 0.18, 0.6, o.color || '#B5302A', { outline: 0.008 }), 0, 0.2, 0), at(cyl(0.12, 0.14, 0.14, '#2A2A2E', 10), 0, 0.36, -0.05), at(cyl(0.06, 0.06, 0.05, P.grey, 8), 0, 0.46, -0.05));
    for (const x of [-0.27, 0.27]) for (const z of [-0.24, 0.24]) body.add(at(cyl(0.09, 0.09, 0.05, P.ink, 10), x, 0.09, z, 0, 0, PI / 2));
    body.add(rod([-0.2, 0.28, -0.3], [-0.22, 0.98, -0.85], 0.015, P.greyDark), rod([0.2, 0.28, -0.3], [0.22, 0.98, -0.85], 0.015, P.greyDark), rod([-0.24, 0.98, -0.85], [0.24, 0.98, -0.85], 0.02, P.ink));
    const g = grp(body); g.userData.update = t => { const on = o.runAt != null && [].concat(o.runAt).some((a, i) => t >= a && t < (([].concat(o.stopAt ?? []))[i] ?? Infinity)); body.position.set(on ? 0.006 * Math.sin(t * 90) : 0, on ? 0.004 * Math.abs(Math.sin(t * 70)) : 0, 0); };
    g.userData.update(0); g.userData.grip = [0, 0.98, -0.85]; return g; },
  grassPatch(o) { // a square of lawn (the plaintiff): turf block with blades; add googlyEyes on top
    const r = rng(o.seed || 3), g = grp(at(box(0.6, 0.12, 0.6, '#6A4A2A', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(0.6, 0.03, 0.6, '#5E9A4A'), 0, 0.13, 0));
    for (let i = 0; i < 70; i++) g.add(at(box(0.012, 0.06 + r() * 0.06, 0.012, r() < 0.5 ? '#5E9A4A' : '#6FB05A', { pivot: 'bottom' }), (r() - 0.5) * 0.56, 0.14, (r() - 0.5) * 0.56, (r() - 0.5) * 0.3, 0, (r() - 0.5) * 0.3));
    return g; },
  tallGrass(o) { // a field of tall grass blades (o.w x o.d, o.h high): grow it with scale keys
    const w = o.w || 6, d = o.d || 6, h = o.h || 1, r = rng(o.seed || 9), n = o.count || 420, cols = o.cols || ['#5E9A4A', '#6FB05A', '#4E8A3E', '#7FBF5E'], g = grp();
    const geo = o.thin ? new THREE.ConeGeometry(o.thin, 1, 3) : new THREE.BoxGeometry(0.06, 1, 0.03); geo.translate(0, 0.5, 0);   // o.thin: tapered blades of that base radius
    const gm = c => { if (!o.soft) return mat(c); const m_ = mat(c).clone(); m_.transparent = true; m_.opacity = o.soft; m_.depthWrite = false; return m_; };   // o.soft: out-of-focus foreground blades
    cols.forEach((c, ci) => { const m = new THREE.InstancedMesh(geo, gm(c), Math.ceil(n / 4)); const M = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler();
      for (let i = 0; i < m.count; i++) { e.set((r() - 0.5) * 0.35, r() * TAU, (r() - 0.5) * 0.35); q.setFromEuler(e); M.compose(new THREE.Vector3((r() - 0.5) * w, 0, (r() - 0.5) * d), q, new THREE.Vector3(1 + r(), h * (0.7 + r() * 0.5), 1)); m.setMatrixAt(i, M); }
      m.castShadow = true; g.add(m); });
    return g; },
  wateringCan(o) { const c = o.color || '#2C8A6A', g = grp(at(cyl(0.12, 0.13, 0.24, c, 12, { outline: 0.006 }), 0, 0.12, 0), rod([0.1, 0.08, 0], [0.32, 0.26, 0], 0.018, c), at(cyl(0.035, 0.02, 0.05, c, 8), 0.33, 0.27, 0, 0, 0, -0.8),
      at(torus(0.09, 0.015, c, 6, 12, PI), -0.02, 0.26, 0, 0, 0, 0)); g.userData.grip = [-0.02, 0.32, 0]; return g; },
  topiaryRabbit(o) { // a huge clipped hedge in the shape of a rabbit (house-sized at scale 1: ~5 m)
    const c = o.color || '#4E8A3E', c2 = o.color2 || '#5E9A4A', g = grp(at(sphere(2.0, c, 1), 0, 1.8, 0), at(sphere(1.25, c2, 1), 0.2, 3.9, 0.9), at(sphere(0.55, c, 1), -0.2, 1.2, -2.0));
    g.children[0].scale.set(1.15, 0.95, 1.25);
    for (const s of [-1, 1]) g.add(at(sphere(0.45, c2, 1), s * 0.45, 5.6, 0.7), at(sphere(0.6, c, 1), s * 1.1, 0.5, 1.5));
    g.children.slice(-4).forEach((m, i) => { if (i % 2 === 0) m.scale.set(0.55, 2.2, 0.45); });
    g.add(at(box(0.8, 1.6, 0.06, o.door || '#2F5E58', { outline: 0.01 }), 0.0, 0.8, 2.48), at(box(1.0, 0.9, 0.06, '#9CC8E8'), 1.0, 2.1, 2.2, 0, 0.35, 0));
    return g; },
  ladder(o) { // a straight ladder (o.h tall), leaning slightly with o.lean
    const h = o.h || 3, c = o.color || '#C9A06A', g = grp(rod([-0.22, 0, 0], [-0.22, h, 0], 0.03, c), rod([0.22, 0, 0], [0.22, h, 0], 0.03, c));
    for (let y = 0.3; y < h; y += 0.3) g.add(rod([-0.22, y, 0], [0.22, y, 0], 0.02, c)); g.rotation.x = -(o.lean ?? 0); return g; },
  securityCam(o) { // small surveillance camera on a wall bracket, red LED
    return grp(at(box(0.04, 0.04, 0.12, '#2A2A2E'), 0, 0, -0.06), at(box(0.1, 0.08, 0.18, '#F2F2EC', { outline: 0.006 }), 0, -0.02, 0.05, 0.35, 0, 0),
      at(cyl(0.03, 0.03, 0.02, '#141414', 12), 0, -0.05, 0.14, PI / 2 + 0.35, 0, 0), at(sphere(0.012, '#FF3A2A', 0, { emissive: '#FF2A1A', noGrain: true }), 0.035, 0.015, 0.1)); },
  honeyJar(o) { // honey jar with a gingham lid and a label
    return grp(at(cyl(0.06, 0.06, 0.13, '#E8A62A', 12, { pivot: 'bottom', outline: 0.006, emissive: '#3A2400' }), 0, 0, 0), at(cyl(0.065, 0.065, 0.025, o.lid || '#B5302A', 12), 0, 0.142, 0),
      at(label(o.text || 'MIEL', 0.09, 0.05, { bg: '#F6F1E3', fg: '#B5302A', wrap: false }), 0, 0.065, 0.061)); },
  nest(o) { // a big straw nest; eggs appear one by one at the layAt times (or all, o.eggs)
    const g = grp(at(torus(0.42, 0.14, '#C9A06A', 6, 16), 0, 0.12, 0, PI / 2, 0, 0), at(cyl(0.4, 0.3, 0.1, '#A8844E', 16, { pivot: 'bottom' }), 0, 0, 0));
    for (let i = 0; i < 16; i++) g.add(at(box(0.3, 0.02, 0.02, '#B8925E'), Math.cos(i * 2.2) * 0.42, 0.18 + (i % 3) * 0.03, Math.sin(i * 2.2) * 0.42, 0, i * 1.3, 0.3));
    const eggs = []; for (let i = 0; i < (o.max || 14); i++) { const a = i * 2.39, r = 0.08 + (i % 5) * 0.06, e = sphere(0.07, '#F6F1E3', 1); e.scale.y = 1.3; e.position.set(Math.cos(a) * r, 0.16 + Math.floor(i / 7) * 0.09, Math.sin(a) * r); g.add(e); eggs.push(e); }
    const lay = [].concat(o.layAt ?? []);
    g.userData.update = t => { const n = lay.length ? lay.filter(x => t >= x).length * Math.ceil(eggs.length / lay.length) : (o.eggs ?? 0); eggs.forEach((e, i) => e.visible = i < n); };
    g.userData.update(0); return g; },
  // ---- "Le distributeur", "Le ticket", "La plante"
  vending(o) { // snack vending machine: hollow cabinet, glass front with 5 rows of spirals and packets, keypad + LCD, coin slot,
               // pickup flap; wobbles for 0.6 s after each shakeAt; o.stuck: a packet hanging at the front of B4; o.empty: no packet in B4
    const w = 0.95, h = 1.9, d = 0.8, gx = -0.14, gw = 0.6, C = o.color || '#B5302A', IN = '#3A3A40';
    const body = grp(at(box(w, h, 0.04, IN, { pivot: 'bottom', outline: 0.01 }), 0, 0, -d / 2 + 0.02),
      at(box(0.04, h, d, C, { pivot: 'bottom', outline: 0.01 }), -w / 2 + 0.02, 0, 0), at(box(0.04, h, d, C, { pivot: 'bottom', outline: 0.01 }), w / 2 - 0.02, 0, 0),
      at(box(w, 0.1, d, C, { outline: 0.01 }), 0, h - 0.05, 0), at(box(w, 0.42, d, C, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0),
      at(box(w / 2 - (gx + gw / 2) - 0.02, h - 0.52, 0.06, C, { outline: 0.008 }), (gx + gw / 2 + w / 2 - 0.02) / 2, 0.42 + (h - 0.52) / 2, d / 2 - 0.03),
      at(mesh(new THREE.BoxGeometry(gw, 1.36, 0.01), glassMat(0.18, '#DDEEF2')), gx, 1.12, d / 2 - 0.004),
      at(box(gw + 0.05, 0.03, 0.03, '#2A2A2E'), gx, 1.81, d / 2 - 0.01), at(box(gw + 0.05, 0.03, 0.03, '#2A2A2E'), gx, 0.43, d / 2 - 0.01),
      at(box(0.22, 0.6, 0.012, '#2A2A2E'), 0.32, 1.3, d / 2 + 0.006), at(box(0.17, 0.07, 0.006, '#9CE8A0', { emissive: '#3A8A40', noGrain: true }), 0.32, 1.52, d / 2 + 0.014),
      at(box(0.5, 0.16, 0.02, '#1E1E22'), gx, 0.22, d / 2 + 0.01), at(box(0.045, 0.06, 0.01, '#C9CCD1'), 0.32, 1.08, d / 2 + 0.014),
      at(label(o.text || 'SNACKS', 0.7, 0.14, { bg: '#F2C230', fg: '#1E1E22', wrap: false }), 0, 1.86, d / 2 + 0.012));
    const keys = []; for (let r = 0; r < 4; r++) for (let c = 0; c < 3; c++) keys.push([0.28 + c * 0.04, 1.4 - r * 0.045, d / 2 + 0.014]);
    body.add(inst(new THREE.BoxGeometry(0.03, 0.03, 0.01), mat('#E6E2D8'), keys));
    const packs = [], pc = [], cols = ['#E8742E', '#2C4A8A', '#5E9A4A', '#F2C230', '#9A5AB5', '#B5302A'];
    for (let r = 0; r < 5; r++) { const y = 1.68 - r * 0.27; body.add(at(box(gw - 0.02, 0.012, d - 0.12, '#C9CCD1'), gx, y, -0.02));
      for (let c = 0; c < 5; c++) { const x = gx - gw / 2 + 0.07 + c * (gw - 0.14) / 4;
        body.add(at(torus(0.035, 0.004, '#8C949A', 3, 10), x, y + 0.05, d / 2 - 0.12, 0, PI / 2, 0));
        if (!(o.empty && r === 1 && c === 3)) for (let k = 0; k < 3; k++) { packs.push([x, y + 0.085, d / 2 - 0.12 - k * 0.12, 0, 0, 0, 0.085, 0.15, 0.035]); pc.push(cols[(r * 2 + c + k) % cols.length]); } } }
    body.add(inst(new THREE.BoxGeometry(1, 1, 1), mat(P.white), packs, pc));
    const xB4 = gx - gw / 2 + 0.07 + 3 * (gw - 0.14) / 4;
    body.add(at(label('B4', 0.07, 0.03, { bg: '#F2C230', fg: '#1E1E22', wrap: false }), xB4, 1.41 - 0.025, d / 2 - 0.05));
    if (o.stuck) body.add(at(B.chipsPack({}), xB4, 1.41 + 0.02, d / 2 - 0.05, -0.5, 0, 0.12));
    const g = grp(body);
    const at0 = [].concat(o.shakeAt ?? []).filter(v => v != null);
    if (at0.length) g.userData.update = t => { let a = 0; for (const s of at0) { const k = (t - s) / 0.6; if (k >= 0 && k < 1) a = Math.sin(k * PI * 6) * 0.07 * (1 - k); } body.rotation.z = a; body.position.x = a * 0.4; };
    return g; },
  chipsPack(o) { // a bag of crisps with a crimped top
    const c = o.color || '#E8742E';
    return grp(at(box(0.11, 0.15, 0.04, c, { outline: 0.004 }), 0, 0.075, 0), at(box(0.112, 0.012, 0.02, '#C9CCD1'), 0, 0.152, 0), at(label(o.text || 'CHIPS', 0.09, 0.04, { bg: '#F2C230', fg: '#B5302A', wrap: false }), 0, 0.085, 0.021)); },
  queueDisplay(o) { // "now serving" number board; shows o.num, then o.num2 from switchAt (with a short blink)
    const mk = n => canvasPlane(0.7, 0.3, (c, W, H) => { c.fillStyle = '#141414'; c.fillRect(0, 0, W, H); c.fillStyle = '#FF5A3A'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `bold ${H * 0.62}px monospace`; c.fillText(String(n), W / 2, H * 0.55); }, { res: 256, emissive: 0.85 });
    const a = mk(o.num ?? '12'), b = mk(o.num2 ?? '4000'); a.position.z = b.position.z = 0.032; b.visible = false;
    const g = grp(at(box(0.78, 0.38, 0.06, '#2A2A2E', { outline: 0.008 }), 0, 0, 0), a, b, at(label(o.title || 'GUICHET', 0.5, 0.08, { bg: '#2C4A8A', fg: '#F6F1E3', wrap: false }), 0, 0.25, 0.03));
    if (o.switchAt != null) g.userData.update = t => { const k = t - o.switchAt; const on2 = k >= 0 && !(k < 0.3 && Math.floor(k * 10) % 2 === 0); b.visible = on2; a.visible = !on2 && k < 0; };
    return g; },
  queueTicket(o) { // the paper queue ticket, a big number on it (held like a card)
    const pic = canvasPlane(0.07, 0.1, (c, W, H) => { c.fillStyle = '#F7F3EA'; c.fillRect(0, 0, W, H); c.fillStyle = '#2C4A8A'; c.fillRect(0, 0, W, H * 0.16); c.fillStyle = '#F6F1E3'; c.font = `bold ${H * 0.09}px Arial`; c.textAlign = 'center'; { const w = c.measureText('VOTRE NUMÉRO').width; if (w > W * 0.88) c.font = `bold ${H * 0.09 * W * 0.88 / w}px Arial`; } c.fillText('VOTRE NUMÉRO', W / 2, H * 0.11);
      c.fillStyle = '#141414'; c.font = `bold ${H * 0.3}px Arial`; c.fillText(String(o.num ?? '4000'), W / 2, H * 0.58); c.font = `${H * 0.07}px Arial`; c.fillText(o.sub || 'Merci de patienter', W / 2, H * 0.85); }, { res: 256 });
    const g = grp(at(box(0.071, 0.101, 0.002, P.white), 0, 0, 0), at(pic, 0, 0, 0.0015)); g.userData.grip = [0, -0.04, 0]; return g; },
  sofaProp(o) { // a movable three-seat sofa (same design as the living room's)
    const c = o.color || P.teal, c2 = o.color2 || P.tealLight;
    return grp(box(2.2, 0.42, 0.9, c, { pivot: 'bottom', outline: 0.006 }), at(box(1.0, 0.14, 0.75, c2), -0.52, 0.49, 0.05), at(box(1.0, 0.14, 0.75, c2), 0.52, 0.49, 0.05),
      at(box(2.2, 0.62, 0.24, c), 0, 0.73, -0.33), at(box(0.22, 0.66, 0.9, c, { pivot: 'bottom' }), -1.1, 0, 0), at(box(0.22, 0.66, 0.9, c, { pivot: 'bottom' }), 1.1, 0, 0),
      at(box(0.4, 0.38, 0.12, P.red), -0.7, 0.72, -0.18, -0.2, 0.1, 0.1)); },
  oxyMeter(o) { // wall-mounted "oxygen meter": a dial and digits that count up from countAt at o.rate per second
    const draw = n => (c, W, H) => { c.fillStyle = '#F6F1E3'; c.fillRect(0, 0, W, H); c.fillStyle = '#1E1E22'; c.font = `bold ${H * 0.16}px Arial`; c.textAlign = 'center'; c.fillText(o.title || 'COMPTEUR O₂', W / 2, H * 0.2);
      c.fillStyle = '#141414'; c.fillRect(W * 0.1, H * 0.34, W * 0.8, H * 0.3); c.fillStyle = '#F2C230'; c.font = `bold ${H * 0.24}px monospace`; c.fillText(String(n).padStart(6, '0') + ' €', W / 2, H * 0.57);
      c.fillStyle = '#B5302A'; c.font = `bold ${H * 0.11}px Arial`; c.fillText(o.sub || 'À CRÉDIT', W / 2, H * 0.85); };
    const frames = []; for (let i = 0; i < 12; i++) { const p = canvasPlane(0.5, 0.36, draw((o.start ?? 84312) + i * 3), { res: 256 }); p.position.z = 0.032; p.visible = i === 0; frames.push(p); }
    const g = grp(at(box(0.56, 0.42, 0.06, '#8C949A', { outline: 0.008 }), 0, 0, 0), ...frames);
    if (o.countAt != null) g.userData.update = t => { const i = Math.max(0, Math.min(11, Math.floor((t - o.countAt) * (o.rate || 1.5)))); frames.forEach((f, j) => f.visible = j === (t < o.countAt ? 0 : i)); };
    return g; },
  cactusPot(o) { // a cactus in a pot (the bailiff gets eyes, a hat and a briefcase in the scene)
    const C = '#6E9C5A', g = grp(at(cyl(0.2, 0.16, 0.3, '#B8643A', 10, { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(cyl(0.21, 0.21, 0.04, '#9C4F2C', 10), 0, 0.3, 0),
      at(cyl(0.13, 0.15, 0.85, C, 8, { pivot: 'bottom', outline: 0.012 }), 0, 0.3, 0), at(sphere(0.13, C, 1), 0, 1.15, 0));
    [[-1, 0.62], [1, 0.8]].forEach(([s, y]) => g.add(at(cyl(0.07, 0.07, 0.22, C, 8, { outline: 0.008 }), s * 0.2, y, 0, 0, 0, PI / 2), at(cyl(0.07, 0.08, 0.3, C, 8, { pivot: 'bottom', outline: 0.008 }), s * 0.3, y - 0.04, 0)));
    for (let i = 0; i < 14; i++) g.add(at(box(0.006, 0.04, 0.006, '#F2EDE4'), Math.cos(i * 2.4) * 0.135, 0.45 + (i % 7) * 0.1, Math.sin(i * 2.4) * 0.135, 0, 0, Math.cos(i) * 0.8));
    return g; },
  // ---- "Le looksmaxing": the course kit, the chainsaw, the face add-ons (jaw, eyes, lumps), the ring light, mirror, poster
  kit72(o) { // the course kit: a case of 72 coloured vials, the lid standing open with the label
    const w = 0.7, d = 0.45, h = 0.12, g = grp(at(box(w, h, d, '#1E1E22', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0));
    const vl = [], vc = [], cols = ['#E8742E', '#5E9A4A', '#2C4A8A', '#B5302A', '#F2C230', '#9A5AB5', '#3E8A8A', '#F2EDE4'];
    for (let r = 0; r < 6; r++) for (let c = 0; c < 12; c++) { vl.push([-w / 2 + 0.05 + c * (w - 0.1) / 11, h + 0.03, -d / 2 + 0.07 + r * (d - 0.14) / 5, 0, 0, 0, 0.024, 0.06, 0.024]); vc.push(cols[(r * 5 + c * 3) % cols.length]); }
    g.add(inst(new THREE.BoxGeometry(1, 1, 1), mat(P.white), vl, vc));
    const lid = grp(at(box(w, 0.03, d, '#1E1E22', { outline: 0.008 }), 0, 0, d / 2), at(label(o.text || 'MÉTHODE\nCLAVICULE LARGE\n72 PRODUITS', w * 0.9, d * 0.8, { bg: '#F2C230', fg: '#1E1E22' }), 0, -0.017, d / 2, PI / 2, 0, 0));
    lid.position.set(0, h, -d / 2); lid.rotation.x = -1.75; g.add(lid);
    return g; },
  chainsaw(o) { // orange chainsaw, bar along +z; the chain shivers between runAt and stopAt
    const body = at(box(0.22, 0.2, 0.36, '#E8742E', { outline: 0.01 }), 0, 0, 0);
    const chain = at(box(0.05, 0.1, 0.54, '#3A3A3E', { outline: 0.006 }), 0, -0.02, 0.44);
    const g = grp(body, at(box(0.2, 0.06, 0.12, '#2A2A2E'), 0, 0.13, -0.08), rod([-0.09, 0.1, 0.13], [0.09, 0.1, 0.13], 0.016, '#2A2A2E'), rod([-0.09, 0.0, 0.13], [-0.09, 0.1, 0.13], 0.016, '#2A2A2E'), chain,
      at(box(0.03, 0.08, 0.5, '#C9CCD1'), 0, -0.02, 0.44), at(label(o.text || 'MASCU 3000', 0.2, 0.06, { bg: '#E8742E', fg: '#1E1E22', wrap: false }), 0.111, 0.02, 0, 0, PI / 2, 0));
    if (o.runAt != null) g.userData.update = t => { const on = t >= o.runAt && (o.stopAt == null || t < o.stopAt); chain.position.y = -0.02 + (on ? 0.005 * Math.sin(t * 140) : 0); body.position.x = on ? 0.004 * Math.sin(t * 95) : 0; };
    g.userData.grip = [0, 0.13, -0.08]; return g; },
  squareJaw(o) { // surgically "squared" jaw: a big block under the face (attach to the head joint)
    const c = o.color || '#E8B48A', w = o.w || 0.3, h = o.h || 0.15, d = o.d || 0.24;
    return grp(at(box(w, h, d, c, { outline: 0.008 }), 0, 0, 0), at(box(w * 0.5, 0.012, 0.01, '#7A3A2A'), 0, h * 0.1, d / 2 + 0.003)); },
  googlyEyes(o) { // "more attractive eyes": two big googly eyes (attach to the head, on the face)
    const r = o.r || 0.045, g = grp();
    [-1, 1].forEach(s => { const ball = sphere(r, P.white, 1); ball.scale.z = 0.6; const e = grp(ball, at(sphere(r * 0.42, P.ink, 1), (o.cross ? -s : s) * r * 0.25, -r * 0.18, r * 0.5)); e.position.x = s * (o.sep || 0.052); g.add(e); });
    return g; },
  faceLumps(o) { // micro-fracture bumps and bandages on the face (attach to the head, on the face)
    const c = o.color || '#E8B48A', r = rng(o.seed || 3), g = grp();
    for (let i = 0; i < (o.n || 8); i++) { const b = sphere(0.022 + r() * 0.026, c, 0); b.scale.z = 0.6; b.position.set((r() - 0.5) * 0.15, (r() - 0.5) * 0.3, 0); g.add(b); }
    if (o.bandage !== false) g.add(at(box(0.21, 0.036, 0.012, '#F2EDE4', { outline: 0.004 }), 0, 0.09, 0.016, 0, 0, 0.5), at(box(0.036, 0.13, 0.012, '#F2EDE4', { outline: 0.004 }), -0.045, -0.06, 0.016, 0, 0, 0.25), at(box(0.12, 0.03, 0.012, '#F2EDE4', { outline: 0.004 }), 0.04, -0.11, 0.016, 0, 0, -0.3));
    return g; },
  ringLight(o) { // influencer ring light on a stand, phone in the middle
    const H = o.height || 1.5, ring = torus(0.21, 0.026, '#FFF6E0', 6, 24); ring.material = glow('#FFF6E0'); ring.position.y = H + 0.21;
    return grp(at(cyl(0.18, 0.2, 0.03, P.ink, 10, { pivot: 'bottom' }), 0, 0, 0), at(cyl(0.012, 0.012, H, P.ink, 6, { pivot: 'bottom' }), 0, 0.03, 0), ring, at(box(0.075, 0.14, 0.012, P.ink), 0, H + 0.21, 0.012)); },
  mirrorFull(o) { // full-length standing mirror
    const w = o.w || 0.62, h = o.h || 1.7;
    return grp(at(box(w + 0.08, h + 0.08, 0.04, o.frame || '#C9A06A', { pivot: 'bottom', outline: 0.008 }), 0, 0.12, 0), at(box(w, h, 0.01, '#CFE0E6', { emissive: '#22323A' }), 0, 0.16 + h / 2, 0.024),
      at(box(0.07, 0.12, 0.3, '#8A6A44', { pivot: 'bottom' }), -w / 2, 0, 0), at(box(0.07, 0.12, 0.3, '#8A6A44', { pivot: 'bottom' }), w / 2, 0, 0)); },
  halo(o) { const r = torus(o.r || 0.16, 0.018, '#FFE7A0', 6, 24); r.material = glow('#FFE7A0'); r.rotation.x = PI / 2; return grp(r); }, // compared to God (attach above the head)
  fitPoster(o) { // gym-guru poster: a V-shaped silhouette and a slogan
    const c = canvasPlane(0.62, 0.88, (gg, W, H) => { gg.fillStyle = o.bg || '#1E1E22'; gg.fillRect(0, 0, W, H); gg.fillStyle = o.fg || '#F2C230';
      gg.beginPath(); gg.moveTo(W * 0.12, H * 0.38); gg.lineTo(W * 0.88, H * 0.38); gg.lineTo(W * 0.62, H * 0.86); gg.lineTo(W * 0.38, H * 0.86); gg.closePath(); gg.fill();
      gg.beginPath(); gg.arc(W / 2, H * 0.3, W * 0.07, 0, TAU); gg.fill(); gg.textAlign = 'center'; gg.font = `900 ${H * 0.07}px Arial`;
      String(o.text || 'CLAVICULE LARGE').split('\n').forEach((l, i) => gg.fillText(l, W / 2, H * (0.1 + i * 0.08))); }, { res: 384 });
    return grp(at(box(0.64, 0.9, 0.01, P.ink), 0, 0, 0), at(c, 0, 0, 0.006)); },
  // ---- "Le resto chinois": cutlery, chopsticks, dishes, the black market, the prison, the mob, the plane
  fork(o) { // table fork along +y (handle end at y = 0, tines up); o.shine = glowing Western treasure
    const c = o.color || '#C9CCD1', m = o.shine ? { emissive: '#7A6A30' } : {};
    const g = grp(at(box(0.014, 0.12, 0.005, o.handle || c, o.handle ? { outline: 0.004 } : m), 0, 0.06, 0), at(box(0.009, 0.032, 0.005, c, m), 0, 0.136, 0), at(box(0.028, 0.012, 0.005, c, m), 0, 0.157, 0));
    for (let i = 0; i < 4; i++) g.add(at(box(0.0045, 0.046, 0.0045, c, m), -0.0115 + i * 0.0077, 0.185, 0));
    g.userData.grip = [0, 0.03, 0]; return g; },
  knife(o) { // table knife along +y: handle 0-0.09, blade 0.09-0.21
    const c = o.color || '#C9CCD1', m = o.shine ? { emissive: '#7A6A30' } : {};
    const g = grp(at(box(0.017, 0.09, 0.009, o.handle || c, m), 0, 0.045, 0), at(box(0.021, 0.012, 0.007, c, m), 0, 0.096, 0),
      at(box(0.02, 0.11, 0.003, c, { ...m, taper: { x: 0.7, z: 1 } }), 0.002, 0.157, 0));
    g.userData.grip = [0, 0.04, 0]; return g; },
  chopsticks(o) { // a pair of tapered chopsticks along +y (o.single: only one)
    const c = o.color || '#7A3A22', g = grp();
    (o.single ? [0] : [-0.009, 0.009]).forEach((x, i) => g.add(at(box(0.009, 0.24, 0.009, c, { pivot: 'bottom', taper: 0.45 }), x, 0, 0, 0, 0, o.single ? 0 : (i ? -0.03 : 0.03))));
    g.userData.grip = [0, 0.08, 0]; return g; },
  riceBowl(o) { // porcelain bowl, blue band, dome of rice
    const rice = sphere(0.058, '#F7F3EA', 1); rice.scale.set(1, 0.42, 1); rice.position.y = 0.06;
    return grp(at(cyl(0.065, 0.04, 0.06, P.white, 12, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(cyl(0.0665, 0.0665, 0.012, '#2C4A8A', 12), 0, 0.044, 0), rice); },
  noodlePlate(o) { // plate of stir-fried noodles with greens and shrimps
    const r = rng(o.seed || 8), pile = sphere(0.1, '#E2B65A', 1); pile.scale.set(1, 0.33, 0.85); pile.position.y = 0.034;
    const g = grp(at(cyl(0.14, 0.12, 0.02, P.white, 16, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(torus(0.132, 0.006, '#B5302A', 4, 20), 0, 0.021, 0, PI / 2, 0, 0), pile);
    for (let i = 0; i < 7; i++) g.add(at(box(0.032, 0.012, 0.016, i % 2 ? '#5E9A4A' : '#E8775F'), (r() - 0.5) * 0.12, 0.062, (r() - 0.5) * 0.1, 0, r() * 3, 0));
    return g; },
  powderLine(o) { // thin line of white powder on a counter; vanishes left to right from goneAt (0.35 s)
    const Ln = o.length || 0.14, line = box(Ln, 0.006, 0.012, '#F4F4F2', { noGrain: true }); line.geometry.translate(Ln / 2, 0.003, 0); line.position.x = -Ln / 2;
    const g = grp(line);
    if (o.goneAt != null) g.userData.update = t => { const k = clamp01((t - o.goneAt) / 0.35); line.scale.x = Math.max(0.001, 1 - k); line.position.x = -Ln / 2 + Ln * k; line.visible = k < 1; };
    return g; },
  cutleryCase(o) { // the dealer's case: lid hinged at the back opens at openAt on red velvet, fork + knife + spoon, golden light
    const w = 0.5, d = 0.34, h = 0.07;
    const g = grp(at(box(w, h, d, '#2A2420', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(box(w - 0.04, 0.01, d - 0.04, '#9E1F24', { emissive: '#4A080C' }), 0, h - 0.002, 0),
      at(box(0.16, 0.025, 0.03, P.ink), 0, h * 0.5, d / 2 + 0.015), at(box(0.04, 0.03, 0.012, '#D8A83A'), -0.15, h - 0.01, d / 2 + 0.006), at(box(0.04, 0.03, 0.012, '#D8A83A'), 0.15, h - 0.01, d / 2 + 0.006));
    const sp = B.spoon({}); sp.scale.setScalar(1.25);
    const items = grp(at(B.fork({ shine: true }), -0.11, h + 0.006, 0.11, -PI / 2, 0, 0), at(B.knife({ shine: true }), 0, h + 0.006, 0.11, -PI / 2, 0, 0), at(sp, 0.11, h + 0.006, 0.1, -PI / 2, 0, 0));
    g.add(items);
    const lid = grp(at(box(w, 0.05, d, '#2A2420', { outline: 0.008 }), 0, 0.025, d / 2), at(box(w - 0.04, 0.006, d - 0.04, '#9E1F24'), 0, -0.002, d / 2)); lid.position.set(0, h, -d / 2); g.add(lid);
    const light = new THREE.PointLight('#FFD27A', 0, 2.4, 1.4); light.position.set(0, 0.3, 0.12); g.add(light);
    const beam = mesh(new THREE.CylinderGeometry(0.2, 0.26, 0.9, 12, 1, true), fxMat('#FFE7A0', 0.22)); beam.position.y = h + 0.45; beam.castShadow = false; g.add(beam);
    const setOpen = k => { lid.rotation.x = -1.95 * k; light.intensity = 2.4 * k; items.visible = k > 0.05; beam.visible = !!o.beam && k > 0.3; beam.scale.set(1, Math.max(0.01, (k - 0.3) / 0.7), 1); };
    setOpen(o.open ?? 0); if (o.openAt != null) g.userData.update = t => setOpen(ease.out(clamp01((t - o.openAt) / 0.6)));
    g.userData.grip = [0, 0.03, d / 2 + 0.03]; return g; },
  boombox(o) { // cassette player: the two speaker cones pulse on the beat from playAt (o.bpm) until stopAt; the tape label shows o.text
    const g = grp(at(box(0.46, 0.24, 0.13, '#3A3D44', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(box(0.32, 0.022, 0.022, P.greyDark), 0, 0.31, 0),
      rod([-0.15, 0.24, 0], [-0.15, 0.31, 0], 0.008, P.greyDark), rod([0.15, 0.24, 0], [0.15, 0.31, 0], 0.008, P.greyDark));
    const cones = [-0.15, 0.15].map(x => { const c = grp(at(cyl(0.072, 0.072, 0.01, '#1A1C20', 14), 0, 0, 0, PI / 2, 0, 0), at(cyl(0.046, 0.046, 0.012, '#5A5E66', 14), 0, 0, 0.004, PI / 2, 0, 0), at(cyl(0.016, 0.016, 0.016, '#C9CCD1', 8), 0, 0, 0.008, PI / 2, 0, 0)); c.position.set(x, 0.12, 0.066); g.add(c); return c; });
    g.add(at(box(0.13, 0.08, 0.006, '#9AA6AC', { emissive: '#1A2024' }), 0, 0.14, 0.067), at(label(o.text || 'MUSIQUE', 0.11, 0.034, { bg: '#F2E8C8', fg: '#B5302A', wrap: false }), 0, 0.14, 0.0712));
    for (let i = 0; i < 5; i++) g.add(at(box(0.02, 0.012, 0.02, i === 1 ? P.red : '#C9CCD1'), -0.05 + i * 0.025, 0.247, 0.03));
    const bpm = o.bpm || 120;
    if (o.playAt != null) g.userData.update = t => { const on = t >= o.playAt && (o.stopAt == null || t < o.stopAt), ph = ((t - o.playAt) * bpm / 60) % 1, s = on ? 1 + 0.22 * Math.exp(-ph * 6) : 1; cones.forEach(c => c.scale.set(s, s, 1)); };
    return g; },
  megaphone(o) { // hand megaphone: horn mouth along +z, pistol grip underneath
    const c = o.color || '#E8E4D8';
    const g = grp(at(cyl(0.05, 0.05, 0.12, c, 10, { outline: 0.01 }), 0, 0.1, 0, PI / 2, 0, 0), at(mesh(new THREE.CylinderGeometry(0.13, 0.05, 0.2, 12, 1, true), mat(c, { doubleSide: true })), 0, 0.1, 0.16, PI / 2, 0, 0),
      at(torus(0.13, 0.009, '#B5302A', 4, 16), 0, 0.1, 0.26), at(box(0.03, 0.09, 0.04, '#3A3D44'), 0, 0.03, -0.01), at(cyl(0.022, 0.022, 0.02, '#3A3D44', 8), 0, 0.1, -0.07, PI / 2, 0, 0));
    g.userData.grip = [0, 0.03, -0.01]; return g; },
  planter(o) { // garden planter box with soil (o.w, o.d, o.h) and a few sprouts: what you "plant" animals in
    const w = o.w || 1.1, d = o.d || 0.5, h = o.h || 0.45, r = rng(o.seed || 4);
    const g = grp(at(box(w, h, d, o.color || '#B8643A', { pivot: 'bottom', outline: 0.008, taper: 1.08 }), 0, 0, 0), at(box(w * 1.08 + 0.06, 0.05, d * 1.08 + 0.06, '#9C4F2C'), 0, h, 0), at(box(w * 1.08 - 0.02, 0.03, d * 1.08 - 0.02, '#4A3424'), 0, h + 0.005, 0));
    for (let i = 0; i < (o.sprouts ?? 4); i++) g.add(at(box(0.02, 0.09, 0.02, '#5E9A4A', { pivot: 'bottom' }), (r() - 0.5) * (w - 0.2), h + 0.02, (r() - 0.5) * (d - 0.15), 0, 0, (r() - 0.5) * 0.6));
    return g; },
  plane(o) { // airliner, nose along +x, about 15 m long (o.livery colour)
    const c = o.livery || '#B5302A';
    const g = grp(at(cyl(0.9, 0.9, 11, P.white, 12, { outline: 0.02 }), 0, 0, 0, 0, 0, PI / 2), at(mesh(new THREE.ConeGeometry(0.9, 1.8, 12), mat(P.white)), 6.4, 0, 0, 0, 0, -PI / 2),
      at(mesh(new THREE.ConeGeometry(0.9, 2.6, 12), mat(P.white)), -6.8, 0.2, 0, 0, 0, PI / 2),
      at(box(3.2, 0.16, 13, P.white, { taper: { x: 0.45, z: 1 }, taperAxis: 'y', outline: 0.02 }), -0.3, -0.35, 0), at(box(1.6, 2.4, 0.16, c, { taper: { x: 0.45, z: 1 } }), -6.6, 1.5, 0),
      at(box(1.2, 0.1, 4.4, P.white, { taper: { x: 0.5, z: 1 }, taperAxis: 'y' }), -6.7, 0.5, 0), at(box(11, 0.32, 1.84, c), 0, -0.2, 0));
    [-3.2, 3.2].forEach(z => g.add(at(cyl(0.38, 0.32, 1.4, '#C9CCD1', 10, { outline: 0.01 }), 0.6, -0.85, z, 0, 0, PI / 2)));
    for (let i = 0; i < 12; i++) [-1, 1].forEach(s => g.add(at(box(0.2, 0.24, 0.02, '#2A3A55'), 3.9 - i * 0.75, 0.3, s * 0.915)));
    return g; },
  photo(o) { // small print photo with a white border (the yearly meal: a photo of rice); held like a card
    const pic = canvasPlane(0.1, 0.122, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.fillStyle = '#C9B48A'; c.fillRect(W * 0.07, H * 0.06, W * 0.86, H * 0.7);
      c.fillStyle = '#F7F3EA'; c.beginPath(); c.ellipse(W / 2, H * 0.42, W * 0.3, H * 0.14, 0, PI, TAU); c.fill(); c.fillStyle = '#E6DFCC'; for (let i = 0; i < 26; i++) { const a = PI + (i * 0.618 % 1) * PI, rr = (i * 0.37 % 1); c.fillRect(W / 2 + Math.cos(a) * W * 0.27 * rr - 2, H * 0.42 + Math.sin(a) * H * 0.12 * rr - 1, 5, 2); }
      c.fillStyle = '#FFFFFF'; c.strokeStyle = '#2C4A8A'; c.lineWidth = W * 0.035; c.beginPath(); c.moveTo(W * 0.18, H * 0.42); c.quadraticCurveTo(W / 2, H * 0.74, W * 0.82, H * 0.42); c.closePath(); c.fill(); c.stroke();
      c.fillStyle = '#3A3A3A'; c.font = `bold ${H * 0.1}px Arial`; c.textAlign = 'center'; c.fillText(o.caption || 'RIZ', W / 2, H * 0.92); }, { res: 256 });
    const g = grp(at(box(0.102, 0.124, 0.002, P.white), 0, 0, 0), at(pic, 0, 0, 0.0016)); g.userData.grip = [0, -0.05, 0]; return g; },
  windowDrawing(o) { // a child-like crayon drawing of a window taped to a wall (the prisoner's only window)
    const pic = canvasPlane(0.42, 0.42, (c, W, H) => { c.fillStyle = '#F7F3EA'; c.fillRect(0, 0, W, H); c.fillStyle = '#9CC8E8'; c.fillRect(W * 0.16, H * 0.16, W * 0.68, H * 0.62);
      c.fillStyle = '#F2C230'; c.beginPath(); c.arc(W * 0.66, H * 0.31, W * 0.075, 0, TAU); c.fill(); c.fillStyle = '#FFFFFF'; c.beginPath(); c.ellipse(W * 0.33, H * 0.34, W * 0.1, H * 0.05, 0, 0, TAU); c.fill();
      c.fillStyle = '#6FAE5A'; c.fillRect(W * 0.16, H * 0.64, W * 0.68, H * 0.14); c.strokeStyle = '#7A4A2A'; c.lineWidth = W * 0.045; c.lineJoin = 'round';
      c.beginPath(); c.moveTo(W * 0.15, H * 0.17); c.lineTo(W * 0.85, H * 0.15); c.lineTo(W * 0.84, H * 0.79); c.lineTo(W * 0.16, H * 0.78); c.closePath(); c.moveTo(W * 0.51, H * 0.16); c.lineTo(W * 0.49, H * 0.78); c.moveTo(W * 0.16, H * 0.47); c.lineTo(W * 0.84, H * 0.48); c.stroke();
      c.fillStyle = '#7A4A2A'; c.fillRect(W * 0.1, H * 0.8, W * 0.8, H * 0.05); }, { res: 384 });
    const inner = grp(at(box(0.43, 0.43, 0.003, P.paper), 0, 0, 0), at(pic, 0, 0, 0.002)); [[-0.17, 0.2, 0.5], [0.17, 0.2, -0.5]].forEach(([x, y, rz]) => inner.add(at(box(0.09, 0.026, 0.004, '#E8DDB0'), x, y, 0.004, 0, 0, rz)));
    inner.rotation.z = o.tilt ?? -0.04; return grp(inner); },
  lantern(o) { // red paper lantern hanging from a cord (origin = top of the lantern, cord goes up o.cord metres)
    const c = o.color || '#C8281E', s = sphere(0.22, c, 1, { emissive: '#4A0C06' }); s.scale.set(1, 0.82, 1); s.position.y = -0.26;
    const ribs = grp(); for (let i = 0; i < 6; i++) ribs.add(at(torus(0.205, 0.004, '#7A1610', 3, 16), 0, 0, 0, 0, i * PI / 6, 0)); ribs.scale.set(1, 0.82, 1); ribs.position.y = -0.26;
    return grp(s, ribs, at(cyl(0.09, 0.09, 0.05, '#D8A83A', 10), 0, -0.075, 0), at(cyl(0.09, 0.09, 0.05, '#D8A83A', 10), 0, -0.445, 0), at(box(0.03, 0.16, 0.03, '#D8A83A', { pivot: 'top' }), 0, -0.47, 0), rod([0, -0.05, 0], [0, o.cord ?? 1.2, 0], 0.006, P.ink)); },
  aquarium(o) { // fish tank on a black cabinet: blue water, gravel, weeds, three fish swimming (pure function of t)
    const w = o.w || 1.2, h = 0.6, d = 0.4, y0 = 0.8;
    const g = grp(at(box(w + 0.04, y0, d + 0.04, '#1E1A18', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(box(w, 0.06, d, '#C9B48A'), 0, y0 + 0.03, 0),
      at(mesh(new THREE.BoxGeometry(w, h, d), glassMat(0.32, '#6FB8D8')), 0, y0 + h / 2, 0), at(box(w + 0.04, 0.05, d + 0.04, '#1E1A18'), 0, y0 + h + 0.025, 0));
    for (let i = 0; i < 4; i++) g.add(at(box(0.04, 0.2 + i * 0.05, 0.02, '#4E8A4A', { pivot: 'bottom', taper: 0.3 }), -w / 2 + 0.15 + i * 0.3, y0 + 0.06, -0.1 + (i % 2) * 0.15));
    const fish = [0, 1, 2].map(i => { const f = grp(at(box(0.09, 0.05, 0.022, ['#E8742E', '#F2C230', '#E8742E'][i]), 0, 0, 0), at(box(0.035, 0.05, 0.01, '#C85A1E'), -0.06, 0, 0)); g.add(f); return f; });
    g.userData.update = t => fish.forEach((f, i) => { const a = t * (0.5 + i * 0.17) + i * 2.1; f.position.set(Math.sin(a) * (w / 2 - 0.12), y0 + 0.22 + i * 0.1 + Math.sin(t * 1.3 + i) * 0.03, -0.08 + i * 0.08); f.rotation.y = Math.cos(a) > 0 ? 0 : PI; });
    g.userData.update(0); return g; },
  hornSpeaker(o) { // grey propaganda loudspeaker horn on a bracket, mouth along +z (tilted down)
    const c = o.color || '#8C949A';
    return grp(at(box(0.06, 0.06, 0.25, P.greyDark), 0, 0, 0.1), at(mesh(new THREE.CylinderGeometry(0.2, 0.05, 0.42, 12, 1, true), mat(c, { doubleSide: true })), 0, -0.07, 0.42, PI / 2 + 0.25, 0, 0), at(cyl(0.07, 0.07, 0.1, P.greyDark, 10), 0, -0.02, 0.22, PI / 2 + 0.25, 0, 0)); },
  flame(o) { // gas burner flame: three flickering emissive cones (pure function of t)
    const g = grp(), cones = [0, 1, 2].map(i => { const m = mesh(new THREE.ConeGeometry(0.075 - i * 0.017, 0.16 + i * 0.05, 7), mat(['#FF8A2A', '#FFB25A', '#FFE08A'][i], { emissive: ['#FF6A1A', '#FF9A3A', '#FFD27A'][i], noGrain: true })); m.castShadow = false; m.position.y = 0.08 + i * 0.02; g.add(m); return m; });
    g.userData.update = t => cones.forEach((c, i) => c.scale.set(1, 1 + 0.18 * Math.sin(t * (17 + i * 5) + i) + 0.1 * Math.sin(t * 31 + i * 2), 1));
    g.userData.update(0); return g; },
  
  // --- "tornado" replica, act 2: aerial strike, explosions, ruins -------------------------------------------------
  cottage(o) { // one-storey pastel suburban house, front faces +Z. Default: front gable (ridge along Z). o.eaves: ridge along X with a porch
    // roof over the door. o.yard: front path + flower beds. o.burnt: roofless charred shell with dark window holes (rubble inside)
    const w = o.w || 6.4, d = o.d || 7, h = o.h || 2.9, rh = o.rh || (o.eaves ? 2.1 : 2.3), c = o.color || '#F2F0EA', roof = o.roof || '#B5402F';
    const trim = o.trim || '#F4F1E8', glass = o.glass || '#7FAFCF', door = o.door || '#B5302A', g = grp(), F = d / 2;
    if (o.burnt) {
      const soot = o.color || '#5E5853', dark = '#262322', r = rng(o.seed || 9);
      const wallT = 0.25, hh = h * (0.75 + r() * 0.25);
      g.add(at(box(w, hh, wallT, soot), 0, hh / 2, F - wallT / 2), at(box(w, hh * (0.6 + r() * 0.4), wallT, soot), 0, hh * 0.4, -F + wallT / 2),
        at(box(wallT, hh, d, soot), -w / 2 + wallT / 2, hh / 2, 0), at(box(wallT, hh * (0.5 + r() * 0.5), d, soot), w / 2 - wallT / 2, hh * 0.35, 0));
      [-w * 0.27, w * 0.27].forEach(x => g.add(at(box(0.95, 0.95, 0.05, dark), x, h * 0.5, F + 0.01)));
      g.add(at(box(0.9, 1.8, 0.05, dark), w * 0.02, 0.9, F + 0.01));
      if (r() < 0.6) g.add(at(box(w * 0.7, 0.14, d * 0.6, '#3A3432'), (r() - 0.5) * 1.2, hh * 0.55, (r() - 0.5) * 1.5, (r() - 0.5) * 0.5, 0, (r() - 0.5) * 0.7));   // fallen roof slab
      for (let i = 0; i < 6; i++) g.add(at(box(0.5 + r() * 0.8, 0.3 + r() * 0.4, 0.5 + r() * 0.8, i % 2 ? '#6E6862' : '#4A4542'), (r() - 0.5) * (w - 1), 0.2, (r() - 0.5) * (d - 1), 0, r() * 3, 0));
      if (r() < 0.5) g.add(at(box(0.5, 1.6 + r(), 0.5, '#4A4542', { pivot: 'bottom' }), w * 0.28, hh * 0.6, -0.8));                                       // chimney stump
      return g;
    }
    g.add(box(w, h, d, c, { pivot: 'bottom', outline: 0.003 }));
    if (!o.eaves) {
      const pitch = Math.atan2(rh, w / 2), sl = Math.hypot(w / 2, rh) + 0.4;
      [-1, 1].forEach(s => g.add(at(box(sl, 0.18, d + 0.7, roof, { outline: 0.004 }), s * (w / 4 + 0.1), h + rh / 2 + 0.04, 0, 0, 0, -s * pitch)));
      const tri = new THREE.Shape(); tri.moveTo(-w / 2, 0); tri.lineTo(w / 2, 0); tri.lineTo(0, rh); tri.lineTo(-w / 2, 0);
      const gab = mesh(new THREE.ExtrudeGeometry(tri, { depth: d - 0.02, bevelEnabled: false }), mat(c)); gab.position.set(0, h, -F + 0.01); g.add(gab);
      g.add(at(box(0.55, 0.55, 0.06, trim), 0, h + rh * 0.38, F + 0.02), at(box(0.42, 0.42, 0.07, glass), 0, h + rh * 0.38, F + 0.025));
    } else {
      const pitch = Math.atan2(rh, d / 2), sl = Math.hypot(d / 2, rh) + 0.5;
      [-1, 1].forEach(s => g.add(at(box(w + (o.overhang ?? 0.7), 0.18, sl, roof, { outline: 0.004 }), 0, h + rh / 2 + 0.04, s * (d / 4 + 0.12), s * pitch, 0, 0)));
      const tri = new THREE.Shape(); tri.moveTo(-F, 0); tri.lineTo(F, 0); tri.lineTo(0, rh); tri.lineTo(-F, 0);
      const gab = mesh(new THREE.ExtrudeGeometry(tri, { depth: w - 0.02, bevelEnabled: false }), mat(c)); gab.rotation.y = PI / 2; gab.position.set(-w / 2 + 0.01, h, 0); g.add(gab);
      if (o.porch !== false) g.add(at(box(w * 0.62, 0.12, 1.5, o.porchRoof || roof, { outline: 0.004 }), -w * 0.12, h * 0.86, F + 0.7, 0.32, 0, 0));      // porch awning
    }
    if (o.chimney !== false) g.add(at(box(0.6, 1.5, 0.6, o.chimneyColor || trim, { pivot: 'bottom' }), w * 0.22, h + rh * 0.35, -d * 0.18));
    const dx = o.doorX ?? w * 0.08, win = (x, y) => {
      g.add(at(box(1.15, 1.15, 0.06, trim), x, y, F + 0.03), at(box(0.95, 0.95, 0.07, glass), x, y, F + 0.035), at(box(0.06, 0.95, 0.08, trim), x, y, F + 0.04), at(box(0.95, 0.06, 0.08, trim), x, y, F + 0.04));
      if (o.shutters) [-1, 1].forEach(s => g.add(at(box(0.32, 1.15, 0.05, o.shutters), x + s * 0.76, y, F + 0.03)));
      g.add(at(box(1.2, 0.22, 0.28, '#6A4632'), x, y - 0.7, F + 0.14), at(box(1.1, 0.12, 0.2, o.flowers || '#D9405A'), x, y - 0.55, F + 0.14));
    };
    win(-w * 0.3, h * 0.55); win(w * 0.3 + (o.eaves ? 0.3 : 0), h * 0.55);
    g.add(at(box(0.95, 1.95, 0.08, door, { outline: 0.01 }), dx, 0.975, F + 0.04), at(box(1.15, 2.1, 0.06, trim), dx, 1.05, F + 0.02), at(box(1.3, 0.16, 0.6, '#D8D2C4'), dx, 0.08, F + 0.3));
    if (o.yard) {
      const L = o.yard === true ? 6 : o.yard;
      g.add(at(box(1.1, 0.04, L, '#E6E2D8'), dx, 0.02, F + 0.6 + L / 2));
      [-1, 1].forEach(s => { const bx = dx + s * 2.2, bed = at(box(2.2, 0.08, 1.1, '#5C3B2A'), bx, 0.04, F + L - 0.4); g.add(bed);
        for (let i = 0; i < 5; i++) g.add(at(box(0.22, 0.14, 0.22, ['#D9405A', '#B04FC8', '#F2F0EA', '#E86A3A'][(i + (s > 0 ? 1 : 0)) % 4]), bx - 0.8 + i * 0.4, 0.12, F + L - 0.4 + (i % 2 ? 0.25 : -0.25))); });
    }
    g.userData.door = [dx, 0, F + 0.6]; return g;
  },
  cumulus(o) { // fluffy cumulus heap: smooth white puffs, flat-ish bottom, bigger in the middle (o.w wide, o.h tall)
    const r = rng(o.seed || 21), n = o.n || 14, W = o.w || 30, H = o.h || 12, g = grp(), m = cloudMat(o.color, o.emissive);
    for (let i = 0; i < n; i++) { const a = r() * TAU, dd = Math.sqrt(r()), x = Math.cos(a) * dd * W * 0.5, z = Math.sin(a) * dd * W * 0.32, k = 1 - dd;
      const rad = (0.22 + 0.32 * k + r() * 0.14) * H, s = new THREE.Mesh(sphereGeo(), m); s.scale.set(rad, rad * 0.86, rad); s.position.set(x, rad * 0.35 + k * H * 0.32, z); s.castShadow = false; s.receiveShadow = true; g.add(s); }
    return g;
  },
  cloudLayer(o) { // a sea of cumulus tops over o.w x o.d metres (one instanced mesh); y = 0 is the cloud deck
    const r = rng(o.seed || 23), W = o.w || 800, D = o.d || 800, n = o.n || 260, H = o.h || 40, list = [];
    for (let i = 0; i < n; i++) { const cx = (r() - 0.5) * W, cz = (r() - 0.5) * D, big = 0.6 + r() * 0.7, per = 5 + Math.floor(r() * 5);
      for (let j = 0; j < per; j++) { const a = r() * TAU, dd = Math.sqrt(r()), k = 1 - dd, rad = (0.3 + 0.45 * k + r() * 0.2) * H * big;
        list.push([cx + Math.cos(a) * dd * H * 1.6 * big, rad * 0.25 + k * H * 0.35 * big - H * 0.25, cz + Math.sin(a) * dd * H * 1.2 * big, 0, 0, 0, rad, rad * 0.8, rad]); } }
    const m = inst(sphereGeo(), cloudMat(o.color, o.emissive), list); m.castShadow = false; m.frustumCulled = false; return grp(m);
  },
  cloudCurtain(o) { // a bank of soft cloud lumps in the local XY plane facing +Z, its scalloped lower edge at y = 0, o.w wide and o.h tall;
    // self-shaded (cream tops, blue-grey undersides in its own frame, whatever the scene light) so it can be locked to a camera and slid
    // across the frame: the jet punching into the deck. o.r lump radius, o.bright / o.shadow colours, o.edgeTint for the bluish lower rows
    const r = rng(o.seed || 31), W = o.w || 6, H = o.h || 8, R = o.r || 0.5, list = [], cols = [];
    const geo = new THREE.IcosahedronGeometry(1, 3), nrm = geo.attributes.normal, vc = [], cb = new THREE.Color(o.bright || '#F6EDDF'), cs = new THREE.Color(o.shadow || '#B7CADB'), c = new THREE.Color();
    for (let i = 0; i < nrm.count; i++) { const k = Math.min(1, Math.max(0, (o.mid ?? 0.45) + (o.ky ?? 0.6) * nrm.getY(i) + (o.kz ?? 0.25) * nrm.getZ(i))); c.copy(cs).lerp(cb, k * k * (3 - 2 * k)); vc.push(c.r, c.g, c.b); }
    geo.setAttribute('color', new THREE.Float32BufferAttribute(vc, 3));
    const et = new THREE.Color(o.edgeTint || '#D6E2EE'), white = new THREE.Color('#FFFFFF');
    const dn = o.down ? -1 : 1;   // o.down: the scalloped edge on top, the lumps hanging below y = 0 (the bank's far edge)
    for (let y = 0; y < H; y += R * 0.85) for (let x = -W / 2; x < W / 2; x += R * 1.0) {
      const rad = R * (0.7 + r() * 0.65), px = x + (r() - 0.5) * R * 0.9, py = y + (r() - 0.5) * R * 0.7 + rad * 0.55;
      list.push([px, dn * py, -r() * R * 1.4, 0, 0, 0, rad, rad * 0.92, rad * 0.75]);
      cols.push('#' + (o.down ? white : c.copy(et).lerp(white, Math.min(1, py / (R * 3.2)))).getHexString()); }
    const m = inst(geo, new THREE.MeshBasicMaterial({ vertexColors: true, fog: false }), list, cols); m.castShadow = m.receiveShadow = false; m.frustumCulled = false;
    const plateH = H - R * 1.3, plate = new THREE.Mesh(new THREE.PlaneGeometry(W, plateH), new THREE.MeshBasicMaterial({ color: o.plate || '#D2DBE3', fog: false }));
    plate.position.set(0, (o.down ? -1 : 1) * (R * 1.3 + plateH / 2), -R * 1.6); plate.castShadow = false;   // backing: nothing behind shows through the gaps
    return grp(m, plate);
  },
  missileSalvo(o) { // missiles flying from launch points to a target: grey body, orange flame + glow, white smoke trail (pure function of t)
    // o.shots: [{from:[x,y,z], to:[x,y,z], ctrl?:[x,y,z], t0, dur}] in prop-local metres; o.size scales body/trail; o.trail: trail length (0..1 of path)
    const S = o.size || 1, g = grp(), body = mat(o.bodyColor || '#D8DADC'), finM = mat('#5C626B'), trailM = new THREE.MeshBasicMaterial({ color: o.trailColor || '#F4F4F2', transparent: true, opacity: o.trailOpacity ?? 0.85, depthWrite: false, fog: true });
    const FL = o.flame || 1, FW = o.flameW || FL, flameM = new THREE.MeshBasicMaterial({ color: o.flameColor || '#FFB04A', fog: false }), coreM = new THREE.MeshBasicMaterial({ color: o.core || '#FFF0B8', fog: false }), trailGeo = new THREE.CylinderGeometry(1, 1, 1, 6, 1, true).translate(0, 0.5, 0);
    const SEG = 6, shots = (o.shots || []).map(sh => {
      const m = grp(at(cyl(0.16 * S, 0.16 * S, 2.6 * S, '#D8DADC', 7, { material: body }), 0, 0, 0, PI / 2, 0, 0), at(mesh(new THREE.ConeGeometry(0.16 * S, 0.5 * S, 7), body), 0, 0, 1.55 * S, PI / 2, 0, 0),
        at(box(0.7 * S, 0.04 * S, 0.4 * S, '#5C626B', { material: finM }), 0, 0, -1.1 * S), at(box(0.04 * S, 0.7 * S, 0.4 * S, '#5C626B', { material: finM }), 0, 0, -1.1 * S),
        at(new THREE.Mesh(new THREE.ConeGeometry(0.2 * S * FW, 1.6 * S * FL, 7), flameM), 0, 0, -1.3 * S - 0.8 * S * FL, -PI / 2, 0, 0), at(glowSprite(o.glowColor || '#FFA040', (o.glow ?? 1.1) * S, 0.9), 0, 0, -1.3 * S - 0.5 * S * FL));
      if (o.core) { const c = at(new THREE.Mesh(sphereGeo(1), coreM), 0, 0, -1.3 * S - 0.12 * S * FL); c.scale.setScalar(0.25 * S * FW); m.add(c); }   // o.core: a yellow-white heart where the flame leaves the body
      m.traverse(n => { n.castShadow = false; }); g.add(m);
      const trail = []; for (let i = 0; i < SEG; i++) { const tm = new THREE.Mesh(trailGeo, trailM); tm.castShadow = false; g.add(tm); trail.push(tm); }
      const A = V3(...sh.from), Bp = V3(...sh.to), C = sh.ctrl ? V3(...sh.ctrl) : A.clone().lerp(Bp, 0.5);
      if (sh.body === false) m.children.slice(0, 4).forEach(c => { c.visible = false; });
      if (sh.head === false) m.children.slice(4).forEach(c => { c.visible = false; });   // trail only (a contrail left by another object)
      return { m, trail, A, B: Bp, C, t0: sh.t0 || 0, dur: sh.dur || 1, len: sh.trail ?? o.trail ?? 0.6, hit: sh.hide !== false, lin: !!sh.lin, v0: sh.v0 ?? o.v0 };
    });
    const pt = (s, u) => { const a = s.A.clone().multiplyScalar((1 - u) * (1 - u)), b = s.C.clone().multiplyScalar(2 * u * (1 - u)), c = s.B.clone().multiplyScalar(u * u); return a.add(b).add(c); };
    const up = V3(0, 1, 0);
    g.userData.update = t => shots.forEach(s => {
      const k = (t - s.t0) / s.dur, on = k >= 0 && (k < 1 || !s.hit);
      s.m.visible = on; s.trail.forEach(tm => { tm.visible = on && k > 0.001; });
      if (!on) return;
      const kk = Math.min(1, k), u = s.lin ? kk : s.v0 != null ? s.v0 * kk + (1 - s.v0) * kk * kk : Math.min(1, ease.in(kk) * 0.75 + kk * 0.25), p = pt(s, u), q = pt(s, Math.min(1, u + 0.01));
      s.m.position.copy(p); if (q.distanceTo(p) > 1e-6) s.m.lookAt(q);
      const u0 = Math.max(0, u - s.len);
      for (let i = 0; i < SEG; i++) { const a = pt(s, u0 + (u - u0) * i / SEG), b = pt(s, u0 + (u - u0) * (i + 1) / SEG), dir = b.clone().sub(a), L = dir.length(), tm = s.trail[i];
        if (L < 1e-4) { tm.visible = false; continue; }
        const rad = ((o.trailBase ?? 0.05) + (o.trailWidth ?? 0.22) * (1 - (i + 0.5) / SEG)) * S; tm.position.copy(a); tm.quaternion.setFromUnitVectors(up, dir.normalize()); tm.scale.set(rad, L, rad); }
    });
    g.userData.update(0); return g;
  },
  fireball(o) { // explosion at prop origin starting at o.t0: white flash and glare -> lumpy fireball (yellow core, orange rim) -> dark rolling
    // smoke with embers; paper chips fly out under gravity. o.size ~ fireball radius (m)
    const r = rng(o.seed || 61), S = o.size || 4, t0 = o.t0 || 0, g = grp(), puffs = [], chips = [];
    for (let i = 0; i < (o.n || 26); i++) { const dir = V3(r() - 0.5, r() * 0.9 - 0.25, r() - 0.5).normalize(), heat = 1 - Math.min(1, r() * 1.3);
      const m = new THREE.Mesh(sphereGeo(1), new THREE.MeshLambertMaterial({ color: '#FFD45A', emissive: '#FF9A2A', map: grainTexture(), transparent: true, flatShading: !!o.facets }));
      m.castShadow = false; g.add(m); puffs.push({ m, dir, d: 0.25 + (1 - heat) * 0.75 + r() * 0.15, s: (0.22 + r() * 0.26 + heat * 0.12) * (o.puff || 1), lag: r() * (o.lag ?? 0.08), heat, smoke: r() < (o.smoke ?? 0.6) }); }
    const FS = o.flashScale || 1, flash = glowSprite('#FFE7A8', S * 6 * FS, 1), glare = glowSprite('#FFF4D8', S * 9 * FS, 0.7); g.add(flash, glare);
    const cc = ['#B5302A', '#F2F0EA', '#2E3A55', '#D9A15A', '#5B7FC0', '#1E1E22'];
    for (let i = 0; i < (o.chips ?? 26); i++) { const m = box(0.25 + r() * 0.6, 0.05, 0.2 + r() * 0.5, cc[i % 6]); m.castShadow = false; g.add(m); chips.push({ m, v: V3((r() - 0.5) * 2, 0.3 + r() * 1.3, (r() - 0.5) * 2).multiplyScalar(S * (1.2 + r() * 1.8)), sp: 3 + r() * 10 }); }
    const c = new THREE.Color(), e = new THREE.Color(), white = new THREE.Color('#FFF8D8'), yellow = new THREE.Color('#FFC628'), orange = new THREE.Color('#F2650E'), red = new THREE.Color('#A8300E');
    const smoke = new THREE.Color(o.smokeColor || '#3E3634'), eY = new THREE.Color('#FFB01E'), eO = new THREE.Color('#C8460A'), black = new THREE.Color('#000000');
    g.userData.update = t => {
      const tt = t - t0; g.visible = tt >= 0; if (tt < 0) return;
      flash.material.opacity = Math.max(0, 1 - tt / (o.flash || 0.6)); flash.scale.setScalar(S * FS * (3 + 5 * Math.min(1, tt / 0.15)));
      glare.material.opacity = 0.8 * Math.max(0, 1 - tt / (o.glare || 1.3)); glare.scale.setScalar(S * 9 * FS);
      puffs.forEach(p => { const GT = o.growT || 0.3, k = Math.max(0, tt - p.lag), grow = ease.out(Math.min(1, k / GT)), drift = Math.max(0, k - GT);   // o.growT: seconds to full size (o.lag: max puff delay)
        const SP = o.spread ?? 1, RI = o.rise ?? 1, rad = S * p.s * (0.3 + 0.9 * grow + (p.smoke ? 0.45 * drift : 0.15 * drift) * SP);   // o.spread / o.rise: how fast the smoke swells and climbs after 0.3 s
        p.m.position.copy(p.dir).multiplyScalar(S * p.d * (0.25 + 0.95 * grow) + drift * S * 0.22 * SP); p.m.position.y += drift * S * (p.smoke ? 0.55 : 0.3) * RI;
        p.m.scale.setScalar(Math.max(0.01, rad));
        const life = (o.life || 1) * (0.55 + 0.6 * p.heat), u = clamp01(k / life);             // 0 hot .. 1 burnt out
        if (u < 0.25) { c.copy(white).lerp(yellow, u / 0.25); e.copy(eY); }
        else if (u < 0.55) { c.copy(yellow).lerp(orange, (u - 0.25) / 0.3); e.copy(eY).lerp(eO, (u - 0.25) / 0.3); }
        else { const w = clamp01((u - 0.55) / 0.45); c.copy(orange).lerp(red, Math.min(1, w * 2)); if (p.smoke) c.lerp(smoke, w); e.copy(eO).lerp(black, w); }
        if (p.heat < 0.3 && u < 0.5) c.lerp(orange, 0.5);                                        // the rim is orange from the start
        p.m.material.color.copy(c); p.m.material.emissive.copy(e).multiplyScalar(o.glowShare ?? 0.5);
        p.m.material.opacity = p.smoke ? 1 : 1 - clamp01((k - life) / 0.35); p.m.visible = p.m.material.opacity > 0.02; });
      chips.forEach(ch => { ch.m.position.copy(ch.v).multiplyScalar(tt); ch.m.position.y -= 4.9 * tt * tt * (o.gravity ?? 0.6); ch.m.rotation.set(tt * ch.sp, tt * ch.sp * 0.7, 0); });
    };
    g.userData.update(o.at ?? 1); return g;
  },
  smokeField(o) { // dark smoke columns rising from o.points [[x, z, height, base y?]] (instanced puffs, loop upward, pure function of t)
    const r = rng(o.seed || 71), list = [], cols = o.points || [[0, 0, 12]], puffs = [], per = o.per || 11;
    cols.forEach(([x, z, hgt, y0 = 0], ci) => { for (let i = 0; i < per; i++) puffs.push({ x, z, y0, hgt, ph: i / per, wob: r() * TAU, s: (o.size || 1) * (0.8 + r() * 0.5), ci }); });
    const m = new THREE.InstancedMesh(sphereGeo(1), new THREE.MeshLambertMaterial({ color: o.color || '#2E2A28', map: grainTexture(), flatShading: true }), puffs.length);
    m.castShadow = false; m.frustumCulled = false; const d = new THREE.Object3D();
    g_set(m, puffs, d, 0);
    function g_set(mm, pp, dd, t) { pp.forEach((p, i) => { const f = (p.ph + t * (o.speed || 0.06)) % 1, y = p.y0 + f * p.hgt, rad = p.s * (0.6 + 1.1 * f);
      const tw = o.twist ? f * o.twist + p.ci * 1.7 + t * (o.twistSpeed ?? 1.2) : 0, ta = o.twist ? (o.twistAmp || 0.8) * p.s * (0.5 + f) : 0;   // o.twist: rope-like spiral columns
      dd.position.set(p.x + Math.sin(f * 5 + p.wob) * 0.6 * f * p.s + f * (o.drift || 0) * p.hgt + Math.sin(tw) * ta, y, p.z + Math.cos(f * 4 + p.wob) * 0.4 * f + Math.cos(tw) * ta); dd.scale.set(rad, rad * 0.85, rad); dd.rotation.set(p.wob, f * 2, 0); dd.updateMatrix(); mm.setMatrixAt(i, dd.matrix); });
      mm.instanceMatrix.needsUpdate = true; }
    const g = grp(m); g.userData.update = t => g_set(m, puffs, d, t); return g;
  },
  flameField(o) { // flat jagged cartoon flames (crossed cards, red-orange with an orange-yellow core) at o.points [[x, y, z, scale]] flickering
    const r = rng(o.seed || 73), pts = o.points || [[0, 0, 0, 1]];
    const shape = (k) => { const s = new THREE.Shape(), n = 5; s.moveTo(-0.5, 0); for (let i = 0; i <= n * 2; i++) { const x = -0.5 + i / (n * 2), tall = i % 2 ? 0.45 + 0.35 * Math.sin(i * 1.7 + k) ** 2 : 1.0 - Math.abs(x) * 0.9 + 0.15 * Math.cos(i * 2.3 + k); s.lineTo(x * (1 - 0.15 * (i % 2)), Math.max(0.2, i % 2 ? tall * 0.6 : tall)); } s.lineTo(0.5, 0); s.lineTo(-0.5, 0); return new THREE.ShapeGeometry(s); };
    const outer = new THREE.InstancedMesh(shape(0), new THREE.MeshBasicMaterial({ color: o.color || '#F2441C', side: THREE.DoubleSide, fog: true }), pts.length * 2);
    const inner = new THREE.InstancedMesh(shape(1.3), new THREE.MeshBasicMaterial({ color: o.core || '#FF9A2E', side: THREE.DoubleSide, fog: true }), pts.length * 2);
    [outer, inner].forEach(m => { m.castShadow = false; m.frustumCulled = false; });
    const ph = pts.map(() => r() * TAU), d = new THREE.Object3D();
    const set = t => { pts.forEach(([x, y, z, s = 1, ry = 0], i) => { const fl = 1 + 0.16 * Math.sin(t * 13 + ph[i]) + 0.08 * Math.sin(t * 29 + ph[i] * 2);
      for (let k = 0; k < 2; k++) { d.position.set(x, y, z); d.rotation.set(0, ry + k * PI / 2 + ph[i] * 0.2, 0); d.scale.set(s * (1.6 + 0.1 * Math.sin(t * 7 + i)), s * 1.6 * fl, 1); d.updateMatrix(); outer.setMatrixAt(i * 2 + k, d.matrix);
        d.position.y = y + 0.01 * s; d.scale.set(s * 1.0, s * 1.0 * fl * (1 + 0.1 * Math.sin(t * 17 + i)), 1); d.position.x = x + Math.sin(ry + k * PI / 2) * 0.02; d.updateMatrix(); inner.setMatrixAt(i * 2 + k, d.matrix); } });
      outer.instanceMatrix.needsUpdate = inner.instanceMatrix.needsUpdate = true; };
    set(0); const g = grp(outer, inner); g.userData.update = set; return g;
  },
  burntTree(o) { // black dead tree: trunk + bare angled branches
    const r = rng(o.seed || 79), H = o.h || 5, c = o.color || '#151414', g = grp(rod([0, 0, 0], [0.15, H, 0], 0.14, c, 5));
    for (let i = 0; i < (o.n || 6); i++) { const y = H * (0.45 + r() * 0.5), a = r() * TAU, L = H * (0.25 + r() * 0.3); g.add(rod([0.15 * y / H, y, 0], [Math.cos(a) * L, y + L * (0.5 + r() * 0.6), Math.sin(a) * L], 0.05, c, 4)); }
    return g;
  },
  whiteFlag(o) { // white flag on a dark pole, cloth waving (o.w x o.h metres, pole o.pole tall), pure function of t
    const W = o.w || 1.6, Hh = o.h || 1.0, PL = o.pole || 3, g = grp(at(cyl(0.04, 0.05, PL, o.poleColor || '#3A2E28', 6, { pivot: 'bottom' }), 0, 0, 0));
    const geo = new THREE.PlaneGeometry(W, Hh, 14, 6); geo.translate(W / 2, PL - Hh / 2 - 0.05, 0); const base = geo.attributes.position.array.slice();
    const cloth = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ color: o.color || '#F2F1EC', map: grainTexture(), side: THREE.DoubleSide, emissive: new THREE.Color(o.glow || '#000000') })); cloth.castShadow = true; g.add(cloth);
    g.userData.update = t => { const p = geo.attributes.position; for (let i = 0; i < p.count; i++) { const x = base[i * 3], y = base[i * 3 + 1], k = x / W;
        p.setZ(i, Math.sin(x * 3.2 - t * (o.speed || 7)) * 0.16 * W * k + Math.sin(y * 4 + t * 3) * 0.04 * k); p.setY(i, y - k * k * 0.12 * Hh * (1 + 0.3 * Math.sin(t * 2))); }
      p.needsUpdate = true; geo.computeVertexNormals(); };
    g.userData.update(0); return g;
  },
  // --- "tornado" replica, act 3: court, hard labour, grave ----------------------------------------------------------
  soundBlock(o) { return grp(at(cyl(0.16, 0.17, 0.07, '#5A321C', 14, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(cyl(0.14, 0.14, 0.01, '#6E4026', 14), 0, 0.072, 0)); },
  bigCuffs(o) { // giant white handcuffs facing +Z: two thick rings with dark rivets joined by a short chain (o.r ring radius)
    const R = o.r || 0.5, t = R * (o.thick || 0.13), c = o.color || '#F4F4F0', g = grp(), mk = x => { const ring = torus(R, t, c, 6, 28); ring.position.x = x; g.add(ring);
      [-1, 1].forEach(s => g.add(at(cyl(t * 0.6, t * 0.6, t * 0.5, '#2A2A2A', 8), x + s * R * 0.92, R * 0.18 * s, t * 0.9, PI / 2, 0, 0))); };
    mk(-R * 1.15); mk(R * 1.15);
    for (let i = 0; i < 3; i++) { const l = torus(R * 0.12, t * 0.45, c, 5, 10); l.position.set(-R * 0.18 + i * R * 0.18, -R * 0.05, 0); l.rotation.y = i % 2 ? PI / 2 : 0; g.add(l); }
    g.userData.update = tt => { g.rotation.z = Math.sin(tt * 2.1) * 0.05; }; return g;
  },
  dock(o) { // courtroom dock: navy platform, white rails on red posts round three sides (front open toward the bench at -Z)
    const W = o.w || 6, D = o.d || 5, H = o.h || 1.4, g = grp(at(box(W + 0.6, 0.35, D + 0.6, '#1F2D4E', { pivot: 'bottom' }), 0, 0, 0), at(box(W + 0.7, 0.08, D + 0.7, '#2E3F66'), 0, 0.35, 0));
    const post = (x, z) => g.add(at(box(0.14, H, 0.14, '#C2342A', { pivot: 'bottom' }), x, 0.39, z));
    [[-W / 2, D / 2], [W / 2, D / 2], [-W / 2, -D / 2], [W / 2, -D / 2], [0, D / 2], [-W / 2, 0], [W / 2, 0]].forEach(([x, z]) => post(x, z));
    [0.55, 1.0].forEach(k => { const y = 0.39 + H * k; g.add(at(box(W + 0.2, 0.1, 0.12, '#F4F2EC'), 0, y, D / 2), at(box(0.12, 0.1, D + 0.2, '#F4F2EC'), -W / 2, y, 0), at(box(0.12, 0.1, D + 0.2, '#F4F2EC'), W / 2, y, 0)); });
    return g;
  },
  windTurbine(o) { // white wind turbine: tapered tower (o.h m), base door, nacelle, hub, three blades with red tips turning about +Z (o.rpm);
    // o.blur 0..1 adds lagging ghost blades (rotor motion blur, the reference's S18)
    const H = o.h || 60, L = o.blade || H * 0.48, g = grp(cyl(H * 0.022, H * 0.04, H, '#F4F4F2', 14, { pivot: 'bottom' }));
    g.add(at(box(H * 0.03, H * 0.045, 0.1, '#24345A'), 0, H * 0.025, H * 0.04), at(box(H * 0.08, 0.03, H * 0.09, '#DCDCD8'), 0, 0.015, 0));
    if (o.label) { const lb = canvasPlane(H * 0.05, H * 0.008, (c, W, Hh) => { c.fillStyle = '#6A6E74'; c.font = `bold ${Hh * 0.8}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.label, W / 2, Hh / 2); }, { res: 256, transparent: true }); lb.position.set(0, H * 0.42, H * 0.031); g.add(lb); }
    g.add(at(box(H * 0.05, H * 0.05, H * 0.12, '#F2F2F0', { outline: 0.004 }), 0, H + H * 0.02, -H * 0.02));
    const rotor = grp(at(mesh(new THREE.ConeGeometry(H * 0.032, H * 0.06, 10), mat('#F7F7F5')), 0, 0, H * 0.03, PI / 2, 0, 0));
    const blade = (a, op) => { const sh = new THREE.Shape([new THREE.Vector2(-L * 0.045, 0), new THREE.Vector2(L * 0.04, 0), new THREE.Vector2(L * 0.012, L), new THREE.Vector2(-L * 0.012, L)]);
      const m = mesh(new THREE.ExtrudeGeometry(sh, { depth: L * 0.012, bevelEnabled: false }), op < 1 ? new THREE.MeshLambertMaterial({ color: '#F4F4F2', transparent: true, opacity: op, depthWrite: false, side: THREE.DoubleSide }) : mat('#F4F4F2'));
      const tip = mesh(new THREE.BoxGeometry(L * 0.026, L * 0.07, L * 0.014), op < 1 ? new THREE.MeshLambertMaterial({ color: '#C8352B', transparent: true, opacity: op, depthWrite: false }) : mat('#C8352B')); tip.position.set(0, L * 0.95, L * 0.006);
      const b = grp(m, tip); b.rotation.z = a; b.rotation.y = 0.12; if (op < 1) b.traverse(n => { n.castShadow = false; }); return b; };
    for (let i = 0; i < 3; i++) rotor.add(blade(i * TAU / 3, 1));
    const ghosts = [], NG = o.ghosts || 16; if (o.blur) for (let k = 1; k <= NG; k++) { const gg = grp(); for (let i = 0; i < 3; i++) gg.add(blade(i * TAU / 3, 0.3 * o.blur * (1 - k / (NG + 1)))); rotor.add(gg); ghosts.push({ gg, k }); }
    rotor.position.set(0, H + H * 0.02, H * 0.045); g.add(rotor);
    const w = (o.rpm ?? 14) / 60 * TAU, rk = o.rpmKeys;   // o.rpmKeys [[t, rpm], ...]: the rotor speeds up or slows down (linear between keys) in place of the constant o.rpm
    const angle = t => { if (!rk) return t * w; let a = 0, t0 = 0, v0 = rk[0][1]; for (const [t1, v1] of rk) { if (t <= t1) { const u = t1 > t0 ? (t - t0) / (t1 - t0) : 0, v = v0 + (v1 - v0) * u; return a + (v0 + v) / 2 * (t - t0) / 60 * TAU; } a += (v0 + v1) / 2 * (t1 - t0) / 60 * TAU; t0 = t1; v0 = v1; } return a + v0 * (t - t0) / 60 * TAU; };
    const speed = t => { if (!rk) return o.rpm ?? 14; let t0 = 0, v0 = rk[0][1]; for (const [t1, v1] of rk) { if (t <= t1) return t1 > t0 ? v0 + (v1 - v0) * (t - t0) / (t1 - t0) : v1; t0 = t1; v0 = v1; } return v0; };
    g.userData.update = t => { rotor.rotation.z = -(angle(t) + (o.phase || 0)); const fast = !rk || Math.abs(speed(t)) > 25; ghosts.forEach(({ gg, k }) => { gg.visible = fast; gg.rotation.z = k * 0.045 * (o.blurSpread || 1); }); };   // with rpmKeys the ghost blades only show once the rotor is fast
    g.userData.update(0); return g;
  },
  whip(o) { // bullwhip held at the grip: dark leather handle and a long cord whose shape is a travelling wave (o.period s per crack)
    const L = o.length || 2.6, N = 22, g = grp(at(cyl(0.022, 0.028, 0.3, '#3A2618', 6), 0, -0.15, 0)), cord = new THREE.Mesh(new THREE.BufferGeometry(), mat('#2A1A10'));
    cord.castShadow = true; g.add(cord); const per = o.period || 0.55, pts = [];
    for (let i = 0; i <= N; i++) pts.push(new THREE.Vector3());
    g.userData.update = t => {
      const ph = ((t + (o.phase || 0)) % per) / per;
      for (let i = 0; i <= N; i++) { const s = i / N, wave = Math.sin(s * 7 - ph * TAU * 1.2) * s * (0.25 + 0.6 * Math.sin(ph * PI)), lift = Math.sin(ph * TAU) * s * s * 0.9;
        pts[i].set(wave * L * 0.35, -0.3 - s * L * (0.75 + 0.2 * Math.cos(ph * TAU)), s * L * 0.55 * Math.sin(ph * PI) + lift * 0.3); }
      cord.geometry.dispose(); cord.geometry = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 40, 0.012, 4); };
    g.userData.update(0); g.userData.grip = [0, -0.05, 0]; return g;
  },
  gravestone(o) { // arched grey headstone: R.I.P. carved at the top, a framed 3D portrait of the voxel dog, a handle line on the base slab
    const W = o.w || 1.0, H = o.h || 1.25, T = 0.2, stone = o.color || '#ABABA8', g = grp();
    g.add(at(box(W, H - W / 2, T, stone, { pivot: 'bottom', outline: 0.004 }), 0, 0.25, 0));
    const arch = mesh(new THREE.CylinderGeometry(W / 2, W / 2, T, 24, 1, false, -PI / 2, PI), mat(stone)); arch.rotation.x = -PI / 2; arch.position.set(0, 0.25 + H - W / 2, 0); g.add(arch);   // the +z half-disc turned up (it was turned down, inside the slab)
    g.add(at(box(W * (o.baseW || 1.45), 0.25, T * 2.6, '#A2A29E', { pivot: 'bottom', outline: 0.004 }), 0, 0, 0.08));
    const rip = canvasPlane(W * (o.ripW || 0.8), W * (o.ripH || 0.22), (c, Wc, Hc) => { c.fillStyle = '#2E2E2C'; c.font = `bold ${Hc * 0.92}px "Times New Roman", Georgia, serif`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.text || 'R.I.P.', Wc / 2, Hc * 0.55); }, { res: 512, transparent: true });
    rip.position.set(0, 0.25 + H - W * (o.ripY || 0.22), T / 2 + 0.004); g.add(rip);
    const fw = W * (o.frameW || 0.72), fh = W * (o.frameH || 0.8), fy = 0.25 + H - W * (o.frameTop || 0.37) - fh / 2;   // the portrait frame (width, height, top below the arch)
    g.add(at(box(fw, fh, 0.05, '#6B3E26'), 0, fy, T / 2 + 0.025), at(box(fw * 0.86, fh * 0.88, 0.052, '#EADDB9'), 0, fy, T / 2 + 0.028));
    const dog = B.voxelDog({ tongue: o.dogTongue || true, eyes: o.dogEyes, color: o.dogColor, muzzle: o.dogMuzzle }), head = dog.userData.head; head.parent.remove(head);
    head.scale.setScalar(fw * (o.dogScale || 1.7)); head.position.set(0, fy + fh * (o.dogY ?? -0.04), T / 2 + 0.06); head.rotation.set(o.dogPitch || 0, o.dogYaw || 0, o.dogRoll || 0); g.add(head);   // dogPitch: + tips the head's top toward us
    if (o.handle) { const hl = canvasPlane(W * 1.1, W * 0.1, (c, Wc, Hc) => { c.fillStyle = '#4A4A48'; c.font = `bold ${Hc * 0.62}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.handle, Wc / 2, Hc / 2); }, { res: 512, transparent: true });
      hl.position.set(0, 0.17, 0.08 + T * 1.3 + 0.004); g.add(hl); }
    return g;
  },
  flowers(o) { // a little bunch of low-poly tulips (red, yellow, white) on green stems
    const r = rng(o.seed || 5), g = grp(), cols = o.colors || ['#D9302A', '#F2C23A', '#F4F2EC', '#D9302A', '#E8452E'];
    cols.forEach((c, i) => { const x = (i - (cols.length - 1) / 2) * 0.06 + (r() - 0.5) * 0.03, h = 0.22 + r() * 0.12, lean = (r() - 0.5) * 0.4;
      g.add(rod([x, 0, 0], [x + lean * 0.12, h, (r() - 0.5) * 0.04], 0.006, '#4E8A3E', 4));
      const b = mesh(new THREE.IcosahedronGeometry(0.035, 0), mat(c)); b.scale.set(1, 1.15, 1); b.position.set(x + lean * 0.12, h + 0.02, 0); g.add(b);
      g.add(at(box(0.02, 0.08, 0.004, '#5E9A4A'), x + 0.02, h * 0.35, 0.01, 0, 0, -0.5)); });
    return g;
  },
  dirtMound(o) { // fresh grave: a long faceted mound of brown earth
    const m = mesh(new THREE.IcosahedronGeometry(1, 1), mat(o.color || '#7B4A2E')); m.scale.set((o.w || 1.2) / 2, o.h || 0.35, (o.d || 2) / 2); m.position.y = 0;
    const r = rng(o.seed || 3), p = m.geometry.attributes.position; for (let i = 0; i < p.count; i++) { const y = p.getY(i); if (y < 0) p.setY(i, y * 0.05); else p.setY(i, y * (0.85 + r() * 0.3)); }
    p.needsUpdate = true; m.geometry.computeVertexNormals(); return grp(m);
  },
  rubble(o) { // a ring of tan/grey boulders round a point (the tornado's base); o.fly > 0 throws some outward (pure function of t)
    const r = rng(o.seed || 7), g = grp(), geo = new THREE.DodecahedronGeometry(1, 0), cols = o.colors || ['#B9AE94', '#A39880', '#CDBFA0', '#8F877A'], fl = [];
    for (let i = 0; i < (o.n || 24); i++) { const a = r() * TAU, d = (o.r || 2) * (0.7 + r() * 0.6), s = (o.size || 0.45) * (0.5 + r()), m = mesh(geo, mat(cols[i % cols.length]));
      m.scale.set(s * 1.3, s * 0.8, s); m.position.set(Math.cos(a) * d, s * 0.4, Math.sin(a) * d); m.rotation.set(r() * 3, r() * 3, r() * 3); g.add(m);
      if (o.fly && r() < o.fly) fl.push({ m, a, d, v: 2 + r() * 4, up: 3 + r() * 5, ph: r(), s }); }
    g.userData.update = t => fl.forEach(f => { const k = ((t * 0.9 + f.ph) % 1.2), d = f.d + f.v * k, y = f.s * 0.4 + f.up * k - 4.9 * k * k * 0.8; f.m.position.set(Math.cos(f.a + k * 2) * d, Math.max(f.s * 0.4, y), Math.sin(f.a + k * 2) * d); f.m.rotation.x = k * 6; });
    g.userData.update(0); return g;
  },
};

Object.assign(B, VP_PROPS, OCEAN_PROPS, NEWS_PROPS, CANICULE_PROPS, VER_PROPS, CHAUSSETTES_PROPS, TROU_PROPS, ETERNUEMENT_PROPS, PORTE_PROPS, INTERRUPTEUR_PROPS, ELAN_PROPS, OMBRE_PROPS, CRAVATE_PROPS, STATUE_PROPS, FOURRIERE_PROPS, RADAR_PROPS, HOQUET_PROPS, AIMANT_PROPS, CODEBARRE_PROPS);   // Vos papiers props (cloud character, Earth, map, barrier, ...)
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
