// « La poule » (story 104, cycle 55): this man loses a tooth biting an apple from his own tree; his insurer refuses: « when hens have teeth ».
// The next day his hen has one tooth, then two; the insurer pays, the whole country brings out its old promises made on the same condition, the
// minister's retirement at fifty included; the retired feed the hen grain but with teeth she prefers steak; an inspector gets bitten; the hero's
// dentist recognises his work on a plaster mould: the hen's teeth are his, left one by one in his apples. New clause: « when pigs fly ».
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
// Running gag drawn here: every apple he bites keeps one big white tooth (poApple, poApplePile; one of them gold), the hen's grin grows in step
// (poHen: oversized blocky white teeth on the lower beak, one gold with its own sparkle), the plaster mould of his teeth matches it (poMould).
import * as THREE from 'three';
import { box, cyl, sphere, mat, addOutline } from './style.js';
import { grp, at, torus } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = (x, c = 2.2) => { const u = clamp01(x); return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const lerp = (a, b, u) => a + (b - a) * u;
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
// [[t, v], ...] -> v at t, smoothstep between keys (a key [t, v, 'lin'] makes its segment linear)
const keyAt = (K, t, d = 0) => {
  if (!K || !K.length) return d;
  if (t <= K[0][0]) return K[0][1];
  for (let i = 1; i < K.length; i++) if (t < K[i][0]) { const u = (t - K[i - 1][0]) / Math.max(1e-6, K[i][0] - K[i - 1][0]); return lerp(K[i - 1][1], K[i][1], K[i][2] === 'lin' ? u : smooth(u)); }
  return K[K.length - 1][1];
};
// [[t, v], ...] -> the value of the last key at or before t (a step), and that key's time
const stepAt = (K, t, d = 0) => { let v = d, t0 = -1e9; for (const q of K || []) if (t >= q[0]) { v = q[1]; t0 = q[0]; } return [v, t0]; };
// inside one of the intervals [[t0, t1], ...]: the time since its start, else -1
const inside = (I, t) => { for (const [a, b] of I || []) if (t >= a && t < b) return t - a; return -1; };
// a damped wobble summed over [[t0, amp, freq, decay], ...]
const rattle = (R, t) => { let s = 0; for (const [t0, amp, f, dk] of R || []) { const u = t - t0; if (u > 0) s += amp * Math.sin(u * (f ?? 18)) * Math.exp(-u * (dk ?? 3.5)); } return s; };
// a pulse 0..1..0 over d seconds after each time in T
const pulse = (T, t, d = 0.12) => { let v = 0; for (const b of T || []) { const u = (t - b) / d; if (u >= 0 && u < 1) v = Math.max(v, Math.sin(u * PI)); } return v; };
const tex = cv => { const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t; };
const canvas = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
const L = (c, o = {}) => new THREE.MeshLambertMaterial({ color: c, ...o });
const B = (c, o = {}) => new THREE.MeshBasicMaterial({ color: c, ...o });
const INK = '#1B1E2A';
const ink = (m, t = 0.03) => { addOutline(m, t); return m; };
const noShadow = g => { g.traverse(c => { if (c.isMesh) { c.castShadow = false; c.receiveShadow = false; } }); return g; };
// a canvas painted plane (Lambert, lit like the set; o.emissive makes it read in shade); front +Z
function paintPlane(w, h, draw, o = {}) {
  const cv = canvas(o.res ?? 256, Math.max(8, Math.round((o.res ?? 256) * h / w))); draw(cv.getContext('2d'), cv.width, cv.height);
  const t = tex(cv), m = L('#FFFFFF', { map: t, side: o.double ? THREE.DoubleSide : THREE.FrontSide, ...(o.emissive ? { emissive: '#FFFFFF', emissiveMap: t, emissiveIntensity: o.emissive } : {}),
    ...(o.offset ? { polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -8 } : {}) });
  const p = new THREE.Mesh(new THREE.PlaneGeometry(w, h), m); p.receiveShadow = true; return p;
}
// a flat shape (THREE.Shape in metres) with a canvas painted over its bounding box (the UVs remapped to it); opaque, cut to the shape
function shapedPlane(shape, w, h, draw, res = 256, o = {}) {
  const geo = new THREE.ShapeGeometry(shape, 8), p = geo.attributes.position, uv = geo.attributes.uv;
  for (let i = 0; i < p.count; i++) uv.setXY(i, p.getX(i) / w + 0.5, p.getY(i) / h + 0.5);
  const cv = canvas(res, Math.round(res * h / w)); draw(cv.getContext('2d'), cv.width, cv.height);
  const t = tex(cv); return new THREE.Mesh(geo, L('#FFFFFF', { map: t, emissive: '#FFFFFF', emissiveMap: t, emissiveIntensity: o.emissive ?? 0.25, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -8 }));
}
// a faceted ellipsoid (jittered icosphere, shared vertices keep their offset)
function facet(rx, ry, rz, color, seed = 3, jit = 0.06, detail = 1, o = {}) {
  const g = new THREE.IcosahedronGeometry(1, detail), p = g.attributes.position, off = new Map();
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i), y = p.getY(i), z = p.getZ(i), k = `${Math.round(x * 999)},${Math.round(y * 999)},${Math.round(z * 999)}`;
    if (!off.has(k)) off.set(k, 1 + (hsh(seed * 31 + off.size * 7.3) - 0.5) * 2 * jit);
    const f = off.get(k); p.setXYZ(i, x * rx * f, y * ry * f, z * rz * f);
  }
  g.computeVertexNormals(); const m = new THREE.Mesh(g, mat(color, o)); m.castShadow = m.receiveShadow = true; return m;
}
// 4-point star sprite texture (sparkles)
let _starTex = null;
function starTex() {
  if (_starTex) return _starTex;
  const N = 128, cv = canvas(N, N), c = cv.getContext('2d'), g = c.createRadialGradient(N / 2, N / 2, 0, N / 2, N / 2, N * 0.22);
  g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(1, 'rgba(255,255,255,0)'); c.fillStyle = g; c.fillRect(0, 0, N, N);
  c.fillStyle = '#FFFFFF'; c.beginPath();
  for (let i = 0; i < 8; i++) { const a = i * PI / 4 - PI / 2, r = i % 2 === 0 ? N * 0.48 : N * 0.07; c.lineTo(N / 2 + Math.cos(a) * r, N / 2 + Math.sin(a) * r); }
  c.closePath(); c.fill(); _starTex = tex(cv); return _starTex;
}
const starSprite = color => { const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: starTex(), color: color || '#FFFFFF', transparent: true, depthWrite: false, depthTest: false })); sp.renderOrder = 5; return sp; };
// a sparkle pops open and shut in 0.5 s after each time in T, turning
function sparkAt(sp, t, T, size) { let v = 0, d0 = 0; for (const t0 of T || []) { const d = t - t0; if (d >= 0 && d < 0.5) { const w = Math.sin(PI * d / 0.5); if (w > v) { v = w; d0 = d; } } } sp.visible = v > 0.02; sp.scale.setScalar(Math.max(0.001, size * v)); sp.material.rotation = d0 * 3; }

// ---------------------------------------------------------------- teeth: an oversized blocky tooth, crown up (pivot at its root), white with an ink edge or gold
const TOOTH_W = '#FFFFFF', TOOTH_G = '#FFD83A';
function tooth(w, h, d, gold = false) {
  const m = box(w, h, d, gold ? TOOTH_G : TOOTH_W, { pivot: 'bottom', taper: { x: 1.12, z: 1.08 }, noGrain: true, emissive: gold ? '#9A7400' : '#4A4A4A' });
  ink(m, 0.12); const crown = box(w * 0.7, h * 0.12, 0.004, gold ? '#FFE48A' : '#FFFFFF', { noGrain: true, emissive: '#FFFFFF' }); crown.position.set(-w * 0.08, h * 0.78, d / 2 + 0.002); crown.castShadow = false; m.add(crown);
  return m;
}
// where the hen's teeth stand on her lower beak (x, z on its top face, metres at hen size 1), in the order they grow; one tooth stands alone in the middle
const LAYOUT6 = [[-0.022, 0.118], [0.022, 0.118], [-0.052, 0.082], [0.052, 0.082], [-0.06, 0.046], [0.06, 0.046]];
const LAYOUT1 = [[0.0, 0.112]];

// ---------------------------------------------------------------- apples: a big red apple with a bite (pivot at its middle); the bite face (cream, scalloped)
// faces o.dir; o.tooth 'white' | 'gold' | null: one big tooth stuck in the bite; o.pecked: bitten on both sides (a core)
function appleMesh(r, dir, toothKind, pecked, seed = 1) {
  const g = grp(), d = new THREE.Vector3(...dir).normalize(), dirs = pecked ? [d, d.clone().negate()] : [d], c = 0.6;
  const geo = new THREE.IcosahedronGeometry(r, 2), p = geo.attributes.position, v = new THREE.Vector3();
  for (let i = 0; i < p.count; i++) { v.set(p.getX(i), p.getY(i) * 0.9, p.getZ(i));
    if (v.y > r * 0.75) v.y -= (v.y - r * 0.75) * 0.6 * (1 - Math.min(1, Math.hypot(v.x, v.z) / (r * 0.5)));
    for (const q of dirs) { const k = v.dot(q); if (k > c * r) v.addScaledVector(q, -(k - c * r)); }
    p.setXYZ(i, v.x, v.y, v.z); }
  geo.computeVertexNormals();
  const body = new THREE.Mesh(geo, mat('#D42A36')); body.castShadow = body.receiveShadow = true; ink(body, 0.03); g.add(body);
  g.add(at(cyl(0.007, 0.01, r * 0.45, '#5A3A1E', 5), r * 0.04, r * 0.86, 0, 0, 0, -0.25));
  const leaf = facet(r * 0.22, r * 0.035, r * 0.12, '#4E9A3E', seed + 3, 0.02, 0); leaf.position.set(r * 0.17, r * 0.92, 0); leaf.rotation.set(0, 0.4, -0.5); g.add(leaf);
  const cutR = r * Math.sqrt(1 - c * c) * 0.97;
  for (const [j, q] of dirs.entries()) {
    const sh = new THREE.Shape(); for (let i = 0; i <= 28; i++) { const a = i / 28 * TAU, rr = cutR * (0.9 + 0.1 * Math.abs(Math.sin(a * 3.5))); if (i === 0) sh.moveTo(Math.cos(a) * rr, Math.sin(a) * rr * 0.95); else sh.lineTo(Math.cos(a) * rr, Math.sin(a) * rr * 0.95); }
    const face = new THREE.Mesh(new THREE.ShapeGeometry(sh), L('#F7ECC6', { emissive: '#5A4A20', emissiveIntensity: 0.35, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -6 }));
    face.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), q); face.position.copy(q).multiplyScalar(c * r + 0.001); face.receiveShadow = true; g.add(face);
    const pip = sphere(r * 0.06, '#4A2A18', 0); pip.scale.set(0.6, 1, 0.4); pip.quaternion.copy(face.quaternion); pip.position.copy(q).multiplyScalar(c * r + 0.002).add(new THREE.Vector3(0, -r * 0.12, 0)); g.add(pip);
    if (toothKind && j === 0) { const tw = r * 0.5, th = r * 0.78, tt = tooth(tw, th, r * 0.36, toothKind === 'gold'), up = new THREE.Vector3(0, 1, 0);
      const ax = q.clone().multiplyScalar(0.55).add(up).normalize(), inPl = up.clone().addScaledVector(q, -up.dot(q)); if (inPl.lengthSq() > 1e-6) inPl.normalize();
      tt.quaternion.setFromUnitVectors(up, ax); tt.position.copy(q).multiplyScalar(c * r).addScaledVector(inPl, cutR * 0.15).addScaledVector(ax, -th * 0.28); g.add(tt); g.userData.tooth = tt; }
  }
  return g;
}
// where the apples of a heap lie (x, level, z): the bottom row first, then the ones on top
const PILE = [[0, 0, 0], [0.205, 0, 0.02], [0.1, 1, 0.0], [-0.205, 0, 0.03], [-0.1, 1, 0.02], [0.32, 0, -0.17], [-0.31, 0, -0.15], [0.0, 2, 0.0], [0.1, 0, -0.2], [-0.12, 0, -0.22], [0.22, 1, -0.16], [-0.2, 1, -0.17]];

// ---------------------------------------------------------------- the hen's mouth / the hero's mouth overlays
// a grin outline (a wide D: flat top, round bottom), centred, in metres
function grinShape(w, h) { const s = new THREE.Shape(), a = w / 2; s.moveTo(-a, h * 0.32); s.quadraticCurveTo(0, h * 0.5, a, h * 0.32); s.bezierCurveTo(a * 0.95, -h * 0.55, -a * 0.95, -h * 0.55, -a, h * 0.32); return s; }

// ---------------------------------------------------------------- a row of narrow terrace house fronts (pivot at the floor under the middle of the row, along X)
function houseFront(w, h, col, door, i) {
  const sw = (w - 0.94) / 2, g = grp(at(box(sw, h, 0.3, col, { pivot: 'bottom', outline: 0.004 }), -(0.47 + sw / 2), 0, -0.15), at(box(sw, h, 0.3, col, { pivot: 'bottom', outline: 0.004 }), 0.47 + sw / 2, 0, -0.15),
    at(box(0.94, h - 2.1, 0.3, col, { pivot: 'bottom' }), 0, 2.1, -0.15), at(box(1.0, 2.2, 0.04, '#2E2622', { pivot: 'bottom' }), 0, 0, -0.75), at(box(1.0, 0.02, 0.8, '#5A4A3A'), 0, 0.01, -0.4));
  for (const sd of [-1, 1]) g.add(at(box(0.04, 2.2, 0.8, '#3A302A', { pivot: 'bottom' }), sd * 0.49, 0, -0.4));
  g.add(at(box(w + 0.06, 0.22, 0.42, '#F4F1E8', { outline: 0.006 }), 0, h + 0.11, -0.12), at(box(w + 0.1, 0.5, 0.5, ['#B5402F', '#3E4A5E', '#6A3A30', '#5E83C6', '#B5402F'][i % 5], { taper: { x: 0.8, z: 1 }, outline: 0.004 }), 0, h + 0.47, -0.15));
  const win = (x, y) => [at(box(0.7, 0.75, 0.05, '#F4F1E8', { outline: 0.006 }), x, y, 0.02), at(box(0.58, 0.63, 0.02, '#8FBBD8', { emissive: '#2A4A5A' }), x, y, 0.05), at(box(0.04, 0.63, 0.03, '#F4F1E8'), x, y, 0.06)];
  g.add(...win(0, h - 0.75));
  const fr = '#F4F1E8';
  g.add(at(box(0.1, 2.2, 0.1, fr), -0.52, 1.1, 0.04), at(box(0.1, 2.2, 0.1, fr), 0.52, 1.1, 0.04), at(box(1.14, 0.12, 0.1, fr), 0, 2.2, 0.04));
  g.add(at(box(1.3, 0.12, 0.5, '#CFC6B4', { pivot: 'bottom' }), 0, 0, 0.25));
  const piv = grp(); piv.position.set(-0.47, 0, 0.01); g.add(piv);
  const leaf = box(0.94, 2.08, 0.06, door, { outline: 0.006 }); leaf.position.set(0.47, 1.05, 0); piv.add(leaf);
  for (const [y, hh] of [[1.5, 0.6], [0.6, 0.7]]) piv.add(at(box(0.66, hh, 0.02, new THREE.Color(door).multiplyScalar(0.8).getStyle()), 0.47, y, 0.035));
  piv.add(at(sphere(0.04, '#D8B85A', 0), 0.84, 1.0, 0.06));
  return { g, piv };
}

// ---------------------------------------------------------------- a white costume wing (pivot at its root, spreading toward +X and up, face +Z): a feathered shape
// with a round leading edge and four scalloped feathers along the trailing edge, grey feather lines, an ink rim behind; double-sided (mirror it with scale.x -1)
function featherWing(Lw = 0.46) {
  const k = Lw / 0.46, cx = 0.22 * k, cy = 0.1 * k, W_ = 0.48 * k, H_ = 0.44 * k, g = grp();
  const mk = (sc) => { const s = new THREE.Shape(), P = (x, y) => [(x * k - cx) * sc, (y * k - cy) * sc];
    s.moveTo(...P(0.0, 0.05)); s.quadraticCurveTo(...P(0.1, 0.3), ...P(0.46, 0.31));
    const pts = [[0.37, 0.13], [0.27, 0.03], [0.16, -0.05], [0.02, -0.08]]; let px = 0.46, py = 0.31;
    for (const [x, y] of pts) { s.quadraticCurveTo(...P((px + x) / 2 + 0.05, (py + y) / 2 - 0.06), ...P(x, y)); px = x; py = y; }
    s.closePath(); return s; };
  const face = shapedPlane(mk(1), W_, H_, (c, Wc, Hc) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, Wc, Hc); c.strokeStyle = '#B9C0CC'; c.lineWidth = Wc * 0.012; c.lineCap = 'round';
    for (const [x0, y0, x1, y1] of [[0.12, 0.62, 0.78, 0.36], [0.1, 0.74, 0.6, 0.62], [0.1, 0.84, 0.38, 0.86], [0.2, 0.45, 0.86, 0.2]]) { c.beginPath(); c.moveTo(x0 * Wc, y0 * Hc); c.quadraticCurveTo((x0 + x1) / 2 * Wc, (y0 + y1) / 2 * Hc + Hc * 0.05, x1 * Wc, y1 * Hc); c.stroke(); } }, 256, { emissive: 0.45 });
  face.material.side = THREE.DoubleSide; face.position.set(cx, cy, 0.004);
  const rim = new THREE.Mesh(new THREE.ShapeGeometry(mk(1.07), 8), B(INK, { side: THREE.DoubleSide })); rim.position.set(cx, cy, -0.004);
  g.add(face, rim); return g;
}

export const POULE_PROPS = {

  // ---------------------------------------------------------------- the hen (pivot at the floor between her feet, front +Z), about 1.1 m tall at o.s 1
  // A big white hen: a faceted body, a fan tail, wings that flap (o.flap [[t0, t1]]), yellow legs, a long neck, a big red comb and a red wattle, a big
  // yellow beak whose lower half opens (o.open [[t, 0..1]]; o.chew [[t0, t1]]: big up-and-down bites) on a dark mouth; on the lower beak the teeth:
  // oversized white blocks (o.teeth [[t, n]]: n of them, a new one pops in; one alone stands in the middle), o.gold: the index of the gold one, which
  // gets a sparkle at each time in o.spark (o.sparkTooth: another index; o.sparks [[t, index]]: a sparkle on each tooth in turn). Googly eyes with pupils (o.gaze [[t, gx, gy]]), blinks (o.blinks [t...]),
  // a squint for the grin (o.squint), ink brows (o.brow [[t, -1..1]]). The head: o.yaw / o.pitch / o.roll [[t, rad]]; o.peck [[t0, t1]] pecking;
  // the body: o.lean [[t, rad]] pitch, o.waddle [[t0, t1]], o.sq [[t, sx, sy, sz]] squash and stretch about the feet, o.shake [[t0, amp, f, dk]] a shiver
  poHen(o) {
    const s = o.s ?? 1, W = o.color || '#F7F3E8', W2 = '#ECE4CF', RED = '#E3342A', BEAK = '#F6B523', BEAK2 = '#E5801C', LEG = '#E8A92E';
    const g = grp(), rig = grp(), sway = grp(); g.add(rig); rig.add(sway);
    const legs = [];
    for (const sd of [-1, 1]) {
      const hp = grp(); hp.position.set(sd * 0.09, 0.27, 0.02); sway.add(hp);
      hp.add(ink(cyl(0.024, 0.019, 0.26, LEG, 6, { pivot: 'top' }), 0.08));
      const ft = grp(); ft.position.y = -0.26; hp.add(ft);
      for (const a of [-0.55, 0, 0.55]) { const toe = box(0.022, 0.018, 0.12, LEG); toe.geometry.translate(0, 0, 0.055); ink(toe, 0.06); toe.rotation.y = a; toe.position.y = 0.009; ft.add(toe); }
      ft.add(at(box(0.02, 0.016, 0.05, LEG), 0, 0.008, -0.03)); legs.push(hp);
    }
    const body = grp(); body.position.set(0, 0.48, 0); sway.add(body);
    body.add(ink(facet(0.3, 0.26, 0.35, W, 3), 0.025), at(facet(0.22, 0.21, 0.15, W, 5), 0, -0.03, 0.21));
    const tail = grp(); tail.position.set(0, 0.07, -0.27); tail.rotation.x = 0.95; body.add(tail);
    for (let i = 0; i < 5; i++) { const f = box(0.09, 0.03, 0.27, i % 2 ? W2 : W, { taper: { x: 0.45, z: 1 }, taperAxis: 'z' }); f.geometry.translate(0, 0, -0.12); ink(f, 0.04); f.rotation.set(-0.12 * Math.abs(i - 2), (i - 2) * 0.3, 0); tail.add(f); }
    const wings = [];
    for (const sd of [-1, 1]) { const wp = grp(); wp.position.set(sd * 0.26, 0.08, 0.05); body.add(wp); const wm = ink(facet(0.07, 0.17, 0.25, W2, 7), 0.04); wm.position.set(sd * 0.025, -0.085, -0.07); wm.rotation.x = 0.25; wp.add(wm); wings.push([wp, sd]); }
    const neck = grp(); neck.position.set(0, 0.12, 0.17); body.add(neck);
    neck.add(ink(cyl(0.09, 0.115, 0.25, W, 8, { pivot: 'bottom' }), 0.04));
    const head = grp(); head.position.set(0, 0.22, 0.02); neck.add(head);
    head.add(at(ink(facet(0.135, 0.145, 0.15, W, 9, 0.04), 0.03), 0, 0.05, 0));
    for (const [y, z, r] of [[0.23, 0.065, 0.062], [0.262, 0.0, 0.07], [0.248, -0.065, 0.062], [0.21, -0.115, 0.05]]) { const c = sphere(r, RED, 1, { noGrain: true }); c.scale.set(0.66, 1.12, 0.92); c.position.set(0, y, z); ink(c, 0.06); head.add(c); }
    head.scale.setScalar(o.headS ?? 1.15);
    const beak = grp(); beak.position.set(0, 0.03, 0.125); head.add(beak);
    const up = box(0.15, 0.065, 0.17, BEAK, { taper: { x: 0.42, z: 0.35 }, taperAxis: 'z', noGrain: true }); up.geometry.translate(0, 0.0325, 0.085); ink(up, 0.05); beak.add(up);
    const roof = box(0.13, 0.004, 0.15, '#5A1612', { taper: { x: 0.42, z: 1 }, taperAxis: 'z' }); roof.position.set(0, 0.0, 0.076); beak.add(roof);
    const jaw = grp(); jaw.position.set(0, 0.0, 0.004); beak.add(jaw);
    const lo = box(0.14, 0.05, 0.162, BEAK2, { taper: { x: 0.55, z: 0.5 }, taperAxis: 'z', noGrain: true }); lo.geometry.translate(0, -0.025, 0.081); ink(lo, 0.05); jaw.add(lo);
    jaw.add(at(box(0.118, 0.006, 0.14, '#8E2620', { taper: { x: 0.55, z: 1 }, taperAxis: 'z' }), 0, 0.0, 0.074));
    for (const sd of [-1, 1]) { const w = sphere(0.034, RED, 1, { noGrain: true }); w.scale.set(0.8, 1.5, 0.7); w.position.set(sd * 0.024, -0.075, 0.035); ink(w, 0.06); jaw.add(w); }
    // the teeth: built for both layouts, shown by count
    const T6 = LAYOUT6.map(([x, z], i) => { const m = tooth(0.042, 0.05, 0.03, i === o.gold); m.position.set(x, -0.004, z); jaw.add(m); return m; });
    const T1 = LAYOUT1.map(([x, z]) => { const m = tooth(0.058, 0.066, 0.036, false); m.position.set(x, -0.004, z); jaw.add(m); return m; });
    const spk = starSprite('#FFF6D0'); jaw.add(spk);
    const eyes = [];
    for (const sd of [-1, 1]) {
      const eg = grp(); eg.position.set(sd * 0.082, 0.088, 0.106); eg.rotation.y = sd * 0.42; head.add(eg);
      const wht = sphere(0.05, '#FFFFFF', 1, { noGrain: true, emissive: '#3A3A3A' }); wht.scale.z = 0.45; ink(wht, 0.14); eg.add(wht);
      const pup = new THREE.Mesh(new THREE.CircleGeometry(0.025, 16), B('#0B0C0F')); pup.position.z = 0.0235; eg.add(pup);
      pup.add(at(new THREE.Mesh(new THREE.CircleGeometry(0.007, 8), B('#FFFFFF')), -0.008, 0.009, 0.001));
      const brow = box(0.064, 0.015, 0.016, INK, { noGrain: true }); brow.position.set(sd * 0.084, 0.16, 0.115); brow.rotation.y = sd * 0.42; head.add(brow);
      eyes.push({ eg, pup, brow, sd });
    }
    const sq = (o.sq || []).map(q => [q[0], q[1]]), sqy = (o.sq || []).map(q => [q[0], q[2]]), sqz = (o.sq || []).map(q => [q[0], q[3] ?? q[1]]);
    const gzx = (o.gaze || []).map(q => [q[0], q[1]]), gzy = (o.gaze || []).map(q => [q[0], q[2] ?? 0]);
    g.userData.update = t => {
      rig.scale.set(s * keyAt(sq, t, 1), s * keyAt(sqy, t, 1), s * keyAt(sqz, t, 1));
      rig.position.x = rattle(o.shake, t) * s;
      const br = 1 + 0.014 * Math.sin(t * 3.1); body.scale.set(1, br, 1);
      const wd = inside(o.waddle, t) >= 0 ? 1 : 0, ph = t * TAU * 2.3;
      sway.rotation.z = wd * 0.13 * Math.sin(ph); legs[0].rotation.x = wd * 0.55 * Math.sin(ph); legs[1].rotation.x = -wd * 0.55 * Math.sin(ph);
      const pd = inside(o.peck, t), pk = pd >= 0 ? Math.pow(Math.max(0, Math.sin(pd * TAU * 2.6)), 2) : 0;
      body.rotation.x = keyAt(o.lean, t, 0) + pk * 0.4;
      neck.rotation.x = pk * 0.8; neck.rotation.y = keyAt(o.yaw, t, 0) * 0.35;
      head.rotation.set(keyAt(o.pitch, t, 0) + pk * 0.3, keyAt(o.yaw, t, 0) * 0.65, keyAt(o.roll, t, 0));
      const cd = inside(o.chew, t), ch = cd >= 0 ? 0.5 - 0.5 * Math.cos(cd * TAU * 4.2) : 0;
      jaw.rotation.x = 0.85 * clamp01(keyAt(o.open, t, 0) + ch * 0.85);
      head.position.y = 0.22 - 0.012 * ch;
      const [n, tn] = stepAt(o.teeth, t, o.n ?? 0), [n0] = stepAt(o.teeth, tn - 1e-4, o.n ?? 0), pop = clamp01((t - tn) / 0.28);
      const shown = jaw.rotation.x > 0.07;
      T1.forEach(m => { m.visible = n === 1 && shown; m.scale.setScalar(n === 1 && n0 < 1 ? Math.max(0.01, outBack(pop, 2.6)) : 1); });
      const p6 = n0 >= 2 ? n0 : 0;
      // (story 104, review 2) o.teethS: the full set drawn bigger (they read as a white bar at phone size)
      const TS = o.teethS ?? 1;
      T6.forEach((m, i) => { const on = n >= 2 && i < n; m.visible = on && shown; m.scale.setScalar(TS * (on && i >= p6 ? Math.max(0.01, outBack(pop, 2.6)) : 1)); });
      let si = o.sparkTooth ?? o.gold ?? 0; for (const [ts, ix] of o.sparks || []) if (t >= ts) si = ix;
      const sp = n === 1 ? LAYOUT1[0] : (LAYOUT6[si] || LAYOUT6[0]), sx = o.sparks ? Math.sign(sp[0]) * 0.035 : 0;
      spk.position.set(sp[0] + 0.012 + sx, 0.075, sp[1] + 0.02); sparkAt(spk, t, o.sparks ? [...(o.spark || []), ...o.sparks.map(q => q[0])] : o.spark, o.sparkSize ?? 0.16);
      const bl = pulse(o.blinks, t, 0.13), sqn = keyAt(o.squint, t, 0), bv = keyAt(o.brow, t, 0), gx = keyAt(gzx, t, 0), gy = keyAt(gzy, t, 0);
      for (const E of eyes) { E.eg.scale.y = Math.max(0.07, (1 - 0.5 * sqn) * (1 - 0.94 * bl)); E.pup.position.x = gx * 0.015; E.pup.position.y = gy * 0.013 - 0.004 * sqn;
        E.brow.position.y = 0.16 + 0.022 * Math.max(0, bv) - 0.006 * Math.max(0, -bv); E.brow.rotation.z = E.sd * 0.45 * Math.max(0, -bv) - E.sd * 0.15 * Math.max(0, bv); }
      const fd = inside(o.flap, t), fl = fd >= 0 ? 0.9 + 0.6 * Math.sin(fd * TAU * 7) : 0;
      for (const [wp, sd] of wings) wp.rotation.z = sd * (0.04 + fl);
    };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a big apple (pivot at its middle): see appleMesh; o.r (0.1), o.dir [x, y, z] the bite face,
  // o.tooth 'white' | 'gold' | null, o.pecked; o.bitten false: a whole apple; o.wob [[t0, amp, f, dk]] a rock about Z
  poApple(o) {
    const r = o.r ?? 0.1, g = grp(), inner = o.bitten === false ? POULE_PROPS.poWholeApple(o) : appleMesh(r, o.dir || [0, 0.35, 1], o.tooth === undefined ? 'white' : o.tooth, !!o.pecked, o.seed ?? 1);
    g.add(inner);
    g.userData.update = t => { inner.rotation.z = rattle(o.wob, t); };
    g.userData.grip = [0, 0, 0]; return g;
  },
  // a whole apple, unbitten (pivot at its middle); o.r
  poWholeApple(o) {
    const r = o.r ?? 0.1, geo = new THREE.IcosahedronGeometry(r, 2), p = geo.attributes.position;
    for (let i = 0; i < p.count; i++) { const y = p.getY(i) * 0.9, x = p.getX(i), z = p.getZ(i), dd = 1 - Math.min(1, Math.hypot(x, z) / (r * 0.5)); p.setXYZ(i, x, y > r * 0.75 ? y - (y - r * 0.75) * 0.6 * dd : y, z); }
    geo.computeVertexNormals(); const body = new THREE.Mesh(geo, mat('#D42A36')); body.castShadow = body.receiveShadow = true; ink(body, 0.03);
    const g = grp(body, at(cyl(0.007, 0.01, r * 0.45, '#5A3A1E', 5), r * 0.04, r * 0.86, 0, 0, 0, -0.25)); const leaf = facet(r * 0.22, r * 0.035, r * 0.12, '#4E9A3E', 4, 0.02, 0); leaf.position.set(r * 0.17, r * 0.92, 0); leaf.rotation.set(0, 0.4, -0.5); g.add(leaf);
    g.userData.grip = [0, 0, 0]; return g;
  },

  // ---------------------------------------------------------------- a heap of bitten apples (pivot at the floor under its middle): each keeps one big tooth in its
  // bite, the bites turned to +Z and up; o.n apples (o.add [[t, n]]: the count over time, a new one drops in from above); o.gold: the index of the one with the
  // gold tooth; o.r (0.1); o.dropH (0.5): how high a new one drops from (0: it appears in place with a bounce)
  poApplePile(o) {
    const r = o.r ?? 0.1, g = grp(), A = [];
    const N = Math.min(PILE.length, Math.max(o.n ?? 1, ...(o.add || []).map(q => q[1])));
    // (story 104, review 2) o.pick [index...]: which places of PILE the apples take, in order (a compact heap: no apple out on the wings)
    for (let i = 0; i < N; i++) { const [x, lv, z] = PILE[o.pick ? (o.pick[i] ?? i) : i], d = [(hsh(i * 3.3) - 0.5) * 0.7 + x * 1.2, 0.55 + 0.25 * hsh(i * 5.1), 1.0];
      const a = appleMesh(r, d, i === o.gold ? 'gold' : 'white', false, i + 2); a.rotation.y = (hsh(i * 7.7) - 0.5) * 0.4; const y0 = r * 0.9 + lv * r * 1.45; a.position.set(x, y0, z); g.add(a); A.push({ a, y0 }); }
    const sp = starSprite('#FFF6D0'); g.add(sp);
    g.userData.update = t => {
      const [n, tn] = stepAt(o.add, t, o.n ?? 1), [n0] = stepAt(o.add, tn - 1e-4, o.n ?? 1), u = clamp01((t - tn) / 0.3);
      A.forEach(({ a, y0 }, i) => { a.visible = i < n; const fresh = i >= n0 && i < n; a.position.y = y0 + (fresh ? (o.dropH ?? 0.5) * (1 - u * u) : 0); const b = fresh && u > 0.8 ? 1 + 0.25 * Math.sin((u - 0.8) / 0.2 * PI) : 1; a.scale.set(b, 2 - b, b); });
      if (o.gold != null && A[o.gold]) { const q = A[o.gold].a; sp.position.set(q.position.x + 0.03, q.position.y + r * 0.6, q.position.z + r * 0.8); sparkAt(sp, t, o.spark, 0.14); } else sp.visible = false;
    };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- an apple tree (pivot at the foot of the trunk): a short brown trunk, a big round green crown
  // in four masses, big red apples hanging on its front half (o.n, 11); o.s scale
  poAppleTree(o) {
    const s = o.s ?? 1, g = grp(), t = grp(); g.add(t); t.scale.setScalar(s);
    t.add(ink(cyl(0.13, 0.2, 1.55, '#7A5234', 7, { pivot: 'bottom' }), 0.02), at(cyl(0.06, 0.08, 0.7, '#7A5234', 6), 0.32, 1.45, 0.05, 0, 0, -0.9), at(cyl(0.06, 0.08, 0.7, '#7A5234', 6), -0.3, 1.5, -0.05, 0, 0, 0.85));
    for (const [x, y, z, r, c] of [[0, 2.35, 0, 1.05, '#4E9A45'], [0.7, 2.15, 0.2, 0.7, '#5DAA4C'], [-0.72, 2.2, 0.1, 0.72, '#448C3E'], [0.1, 2.95, -0.1, 0.72, '#64B254']]) t.add(at(facet(r, r * 0.9, r, c, 11 + x * 10, 0.07, 1), x, y, z));
    const n = o.n ?? 11;
    for (let i = 0; i < n; i++) { const a = hsh(i * 2.7) * PI * 1.1 - PI * 0.05, e = (hsh(i * 4.9) - 0.35) * 1.2, R = 1.02; const x = Math.cos(a) * Math.cos(e) * R * 1.05, y = 2.35 + Math.sin(e) * R * 0.95, z = Math.sin(a) * Math.cos(e) * R;
      const ap = sphere(0.095, '#D42A36', 1); ap.scale.y = 0.92; ap.position.set(x, y, Math.abs(z) + 0.05); ink(ap, 0.05); t.add(ap); }
    return g;
  },

  // ---------------------------------------------------------------- a henhouse (pivot at the floor, door +Z): a wooden box on four legs, a red gable roof, a dark
  // round door, a slatted ramp, a little straw at the door
  poCoop(o) {
    const g = grp(), Wd = '#C8955E', D = '#9A6A3E';
    for (const [x, z] of [[-0.42, -0.32], [0.42, -0.32], [-0.42, 0.32], [0.42, 0.32]]) g.add(at(box(0.07, 0.42, 0.07, D, { pivot: 'bottom' }), x, 0, z));
    g.add(at(box(1.0, 0.72, 0.8, Wd, { pivot: 'bottom', outline: 0.006 }), 0, 0.42, 0));
    for (let i = 0; i < 4; i++) g.add(at(box(1.01, 0.02, 0.81, D), 0, 0.55 + i * 0.17, 0));
    for (const sd of [-1, 1]) g.add(at(box(0.66, 0.06, 1.0, '#C9473A', { outline: 0.006 }), sd * 0.28, 1.32, 0, 0, 0, -sd * 0.62));
    const tri = new THREE.Shape(); tri.moveTo(-0.5, 0); tri.lineTo(0.5, 0); tri.lineTo(0, 0.36); tri.lineTo(-0.5, 0);
    for (const z of [0.4, -0.4]) { const m = new THREE.Mesh(new THREE.ShapeGeometry(tri), mat(Wd, { doubleSide: true })); m.position.set(0, 1.14, z); g.add(m); }
    const dr = new THREE.Mesh(new THREE.CircleGeometry(0.16, 16), B('#2A1E16')); dr.position.set(0.18, 0.72, 0.405); g.add(dr);
    const ramp = grp(at(box(0.28, 0.03, 0.75, D, { outline: 0.01 }), 0, 0, 0)); for (let i = 0; i < 5; i++) ramp.add(at(box(0.28, 0.025, 0.025, '#7A5234'), 0, 0.02, -0.3 + i * 0.15));
    ramp.position.set(0.18, 0.3, 0.72); ramp.rotation.x = 0.65; g.add(ramp);
    return g;
  },

  // ---------------------------------------------------------------- the hero's mouth, shown twice (attach to the 'head' joint; front +Z on the face): a wide grin
  // drawn over his painted mouth; o.kind 'gap': a row of big white upper teeth with one black gap, 'none': no teeth at all (pink gums, dark mouth, tongue);
  // o.w (0.2) x o.h (0.1), o.y / o.z its place, o.rz a tilt; o.open [[t, v]]: the grin opens (y scale 0.15..1)
  poGrin(o) {
    const w = o.w ?? 0.2, h = o.h ?? 0.1, g = grp(), inner = grp(); g.add(inner);
    const m = shapedPlane(grinShape(w, h), w, h, (c, Wc, Hc) => {
      c.fillStyle = '#3A0E10'; c.fillRect(0, 0, Wc, Hc);
      c.fillStyle = '#C8505A'; c.beginPath(); c.ellipse(Wc * 0.5, Hc * 0.98, Wc * 0.3, Hc * 0.28, 0, 0, TAU); c.fill();
      if (o.kind === 'none') { c.fillStyle = '#E58A92'; c.beginPath(); c.moveTo(0, Hc * 0.1); c.quadraticCurveTo(Wc / 2, -Hc * 0.02, Wc, Hc * 0.1); c.lineTo(Wc, Hc * 0.3); c.quadraticCurveTo(Wc / 2, Hc * 0.22, 0, Hc * 0.3); c.closePath(); c.fill();
        c.strokeStyle = '#B85A64'; c.lineWidth = Hc * 0.02; for (let i = 1; i < 6; i++) { const x = Wc * i / 6; c.beginPath(); c.arc(x, Hc * 0.3, Wc * 0.03, 0, PI); c.stroke(); } }
      else { const n = 6, gap = o.gapAt ?? 3, tw = Wc * 0.8 / n, x0 = Wc * 0.1;
        for (let i = 0; i < n; i++) { if (i === gap) continue; const x = x0 + i * tw; c.fillStyle = '#FFFFFF'; c.fillRect(x + tw * 0.06, Hc * 0.08, tw * 0.88, Hc * 0.42); c.strokeStyle = '#2A2020'; c.lineWidth = Hc * 0.025; c.strokeRect(x + tw * 0.06, Hc * 0.08, tw * 0.88, Hc * 0.42); } }
    }, 256, { emissive: 0.35 });
    const rim = new THREE.Mesh(new THREE.ShapeGeometry(grinShape(w * 1.07, h * 1.12), 8), B('#2A1A1A', { polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -4 })); rim.position.z = -0.001;
    inner.add(rim, m); inner.position.set(0, o.y ?? 0.12, o.z ?? 0.1); inner.rotation.z = o.rz ?? 0;
    g.userData.update = t => { const v = keyAt(o.open, t, 1); inner.scale.set(1, Math.max(0.01, v), 1); inner.visible = v > 0.05; };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the plaster mould of his teeth (pivot at the middle of its base, teeth up, front +Z): a white
  // horseshoe of plaster on a flat plinth, six big white teeth in the hen's layout (LAYOUT6 x o.k, 2.6), o.gold the gold one; o.spark [t...]
  poMould(o) {
    const k = o.k ?? 2.6, g = grp(), P = '#EFEAE0';
    g.add(ink(box(0.42, 0.05, 0.4, '#E3DCCD', { pivot: 'bottom' }), 0.02));
    const R = 0.16 * k / 2.6, base = grp(); base.position.set(0, 0.05, -0.08); g.add(base);
    for (let i = 0; i < 11; i++) { const a = -1.5 + 3.0 * i / 10; base.add(at(ink(box(0.09, 0.075, 0.085, '#E9AFA6', { pivot: 'bottom' }), 0.03), Math.sin(a) * R, 0, Math.cos(a) * R, 0, a, 0)); }
    const sp = starSprite('#FFF6D0'); g.add(sp); let gp = null;
    [-0.27, 0.27, -0.8, 0.8, -1.3, 1.3].forEach((a, i) => { const m = tooth(0.062 * k / 2.6, 0.078 * k / 2.6, 0.046 * k / 2.6, i === o.gold); const X = Math.sin(a) * R, Z = Math.cos(a) * R - 0.08; m.position.set(X, 0.115, Z); m.rotation.y = a; g.add(m); if (i === o.gold) gp = [X, Z]; });
    g.userData.update = t => { if (gp) { sp.position.set(gp[0] + 0.02, 0.22, gp[1] + 0.05); sparkAt(sp, t, o.spark, 0.2); } else sp.visible = false; };
    g.userData.update(0); g.userData.grip = [0, 0, 0]; return g;
  },

  // ---------------------------------------------------------------- a framed photo on a stand (pivot at the middle of its bottom edge, the picture +Z): a wooden frame,
  // a cream mat, a painted holiday: blue sky, sun, sea, sand, a red-and-white striped deckchair with a smiling grey-haired man in a dark jacket stretched out on
  // it, hands behind his head (no text); o.w (0.44) x o.h (0.34); o.stand false: no strut
  poPhoto(o) {
    const w = o.w ?? 0.44, h = o.h ?? 0.34, g = grp(), F = '#7A4A2A';
    g.add(at(box(w, h, 0.03, F, { outline: 0.01 }), 0, h / 2, -0.015));
    const pic = paintPlane(w * 0.86, h * 0.84, (c, Wc, Hc) => {
      const sky = c.createLinearGradient(0, 0, 0, Hc * 0.6); sky.addColorStop(0, '#5FB2E6'); sky.addColorStop(1, '#BDE4F4'); c.fillStyle = sky; c.fillRect(0, 0, Wc, Hc);
      c.fillStyle = '#FFD84A'; c.beginPath(); c.arc(Wc * 0.82, Hc * 0.17, Hc * 0.1, 0, TAU); c.fill();
      c.fillStyle = '#2F8FC9'; c.fillRect(0, Hc * 0.5, Wc, Hc * 0.13); c.fillStyle = '#F1D9A0'; c.fillRect(0, Hc * 0.62, Wc, Hc * 0.38);
      const poly = (pts, col) => { c.fillStyle = col; c.beginPath(); pts.forEach(([x, y], i) => c[i ? 'lineTo' : 'moveTo'](x * Wc, y * Hc)); c.closePath(); c.fill(); c.strokeStyle = '#1B1418'; c.lineWidth = Hc * 0.012; c.stroke(); };
      for (let i = 0; i < 6; i++) { const u0 = i / 6, u1 = (i + 1) / 6, A = [0.12, 0.98], Bp = [0.46, 0.98], C = [0.74, 0.36], D = [0.42, 0.36];
        const l = (P, Q, u) => [P[0] + (Q[0] - P[0]) * u, P[1] + (Q[1] - P[1]) * u]; poly([l(A, Bp, u0), l(A, Bp, u1), l(D, C, u1), l(D, C, u0)], i % 2 ? '#F4F1E8' : '#E2403A'); }
      c.strokeStyle = '#8A5A34'; c.lineWidth = Wc * 0.02; c.beginPath(); c.moveTo(Wc * 0.12, Hc * 0.99); c.lineTo(Wc * 0.44, Hc * 0.34); c.moveTo(Wc * 0.62, Hc * 0.99); c.lineTo(Wc * 0.5, Hc * 0.62); c.stroke();
      poly([[0.3, 0.86], [0.46, 0.86], [0.64, 0.5], [0.5, 0.48]], '#23262E');
      poly([[0.42, 0.84], [0.5, 0.78], [0.94, 0.86], [0.92, 0.95]], '#2E323C');
      poly([[0.5, 0.7], [0.53, 0.68], [0.6, 0.53], [0.57, 0.52]], '#2F62B5');
      poly([[0.5, 0.52], [0.44, 0.34], [0.5, 0.3], [0.56, 0.48]], '#23262E'); poly([[0.62, 0.5], [0.8, 0.36], [0.84, 0.42], [0.66, 0.56]], '#23262E');
      c.save(); c.translate(Wc * 0.6, Hc * 0.3); c.rotate(-0.35); poly([[-0.09, -0.12], [0.09, -0.12], [0.09, 0.12], [-0.09, 0.12]].map(([x, y]) => [x * 1.0, y * Wc / Hc * 1.0]), '#E8B48A');
      c.fillStyle = '#ECE8DE'; c.fillRect(-Wc * 0.1, -Wc * 0.15, Wc * 0.2, Wc * 0.07); c.strokeStyle = '#1B1418'; c.lineWidth = Hc * 0.016;
      c.beginPath(); c.arc(-Wc * 0.04, -Wc * 0.02, Wc * 0.022, PI, TAU); c.stroke(); c.beginPath(); c.arc(Wc * 0.04, -Wc * 0.02, Wc * 0.022, PI, TAU); c.stroke();
      c.fillStyle = '#7A1E22'; c.beginPath(); c.arc(0, Wc * 0.035, Wc * 0.05, 0, PI); c.closePath(); c.fill(); c.stroke(); c.restore();
    }, { res: 256, emissive: 0.25 });
    pic.position.set(0, h / 2, 0.008);
    const mt = box(w * 0.92, h * 0.9, 0.006, '#F4EEDF'); mt.position.set(0, h / 2, 0.0); g.add(mt, pic);
    if (o.stand !== false) g.add(at(box(0.04, h * 0.85, 0.02, F), 0, h * 0.42, -0.12, -0.38, 0, 0));
    g.userData.grip = [0, h / 2, 0]; return g;
  },

  // ---------------------------------------------------------------- a big old yellowed envelope (pivot at its middle, front +Z): stained, the flap lines, a faded
  // stamp corner; o.dust [t...]: a soft translucent cloud of dust blown off its face toward +Z, kept low under the face (o.dustDur 0.85 s); o.letter [[t, 0..1]]: the letter slides up out of it and shows a drawing of
  // a hen with teeth (the condition, no text); o.w (0.42)
  poOldLetter(o) {
    const w = o.w ?? 0.42, h = w * 0.64, g = grp(), env = grp(); g.add(env);
    const front = paintPlane(w, h, (c, Wc, Hc) => { c.fillStyle = '#DCC386'; c.fillRect(0, 0, Wc, Hc);
      for (let i = 0; i < 7; i++) { c.fillStyle = `rgba(140,100,40,${0.12 + 0.1 * hsh(i)})`; c.beginPath(); c.ellipse(Wc * hsh(i * 3.1), Hc * hsh(i * 4.7), Wc * (0.05 + 0.1 * hsh(i * 2)), Hc * (0.05 + 0.08 * hsh(i * 5)), 0, 0, TAU); c.fill(); }
      c.strokeStyle = '#A88A4E'; c.lineWidth = Hc * 0.02; c.beginPath(); c.moveTo(0, Hc); c.lineTo(Wc / 2, Hc * 0.48); c.lineTo(Wc, Hc); c.stroke();
      c.strokeStyle = '#B79A5E'; c.setLineDash([Wc * 0.02, Wc * 0.015]); c.strokeRect(Wc * 0.78, Hc * 0.08, Wc * 0.15, Hc * 0.26); c.setLineDash([]);
      c.strokeStyle = '#9C7E44'; c.lineWidth = Hc * 0.03; c.strokeRect(1, 1, Wc - 2, Hc - 2); }, { res: 256, emissive: 0.2 });
    front.position.z = 0.012; env.add(front, at(box(w, h, 0.022, '#CDB274'), 0, 0, 0));
    const letter = grp(); env.add(letter);
    const sheet = paintPlane(w * 0.86, h * 1.05, (c, Wc, Hc) => { c.fillStyle = '#F4ECD4'; c.fillRect(0, 0, Wc, Hc);
      c.save(); c.translate(Wc * 0.4, Hc * 0.44); const S = Wc * 0.25;
      c.fillStyle = '#FFFFFF'; c.strokeStyle = '#2A2020'; c.lineWidth = S * 0.06; c.beginPath(); c.ellipse(0, S * 0.25, S * 0.95, S * 0.62, 0, 0, TAU); c.fill(); c.stroke();
      c.beginPath(); c.arc(S * 0.75, -S * 0.42, S * 0.42, 0, TAU); c.fill(); c.stroke();
      c.fillStyle = '#E3342A'; for (const [x, y] of [[0.55, -0.85], [0.78, -0.92], [1.0, -0.82]]) { c.beginPath(); c.arc(x * S, y * S, S * 0.15, 0, TAU); c.fill(); }
      c.fillStyle = '#F6B523'; c.beginPath(); c.moveTo(S * 1.1, -S * 0.62); c.lineTo(S * 1.95, -S * 0.52); c.lineTo(S * 1.1, -S * 0.42); c.fill(); c.stroke(); c.fillStyle = '#E5801C'; c.beginPath(); c.moveTo(S * 1.1, -S * 0.12); c.lineTo(S * 1.85, 0.0); c.lineTo(S * 1.1, S * 0.08); c.fill(); c.stroke();
      c.fillStyle = '#FFFFFF'; for (const x of [1.2, 1.5]) { c.fillRect(x * S, -S * 0.46, S * 0.26, S * 0.4); c.strokeRect(x * S, -S * 0.46, S * 0.26, S * 0.4); }
      c.fillStyle = '#1B1418'; c.beginPath(); c.arc(S * 0.86, -S * 0.5, S * 0.07, 0, TAU); c.fill();
      c.restore(); c.fillStyle = '#B7A884'; for (let i = 0; i < 3; i++) c.fillRect(Wc * 0.12, Hc * (0.78 + i * 0.07), Wc * (0.76 - i * 0.2), Hc * 0.025); }, { res: 256, emissive: 0.25 });
    sheet.position.z = 0.0; letter.add(sheet, at(box(w * 0.86, h * 1.05, 0.004, '#E8DFC4'), 0, 0, -0.003)); letter.position.z = 0.006; letter.visible = false;
    const NP = 12, puffs = []; for (let i = 0; i < NP; i++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(0.045 * w / 0.42, 1), new THREE.MeshLambertMaterial({ color: i % 2 ? '#EDE4CE' : '#DCCFB0', transparent: true, opacity: 0.7, depthWrite: false }));
      m.castShadow = false; m.receiveShadow = false; g.add(m); puffs.push(m); }
    g.userData.update = t => {
      const lv = keyAt(o.letter, t, 0); letter.visible = lv > 0.01; letter.position.y = lv * h * 0.95;
      // (story 104, review 2) o.dustReach (1): how far the dust travels toward the lens; o.dustFade (1.6): how fast it thins (a thin late cloud that does not veil the faces behind)
      let d = -1; const DD = o.dustDur ?? 0.85, DR = o.dustReach ?? 1, DF = o.dustFade ?? 1.6; for (const t0 of o.dust || []) if (t >= t0 && t < t0 + DD) d = t - t0;
      puffs.forEach((m, i) => { m.visible = d >= 0; if (d < 0) return; const u = d / DD, a = (i / NP - 0.5) * 2.4 + (hsh(i * 9) - 0.5) * 0.4, k = smooth(Math.min(1, u * 1.8));
        m.position.set(Math.sin(a) * w * 0.85 * (0.3 + k), h * 0.1 + k * w * 0.12 * (hsh(i) - 0.3), 0.03 + k * w * 1.5 * DR * (0.5 + hsh(i * 3)));
        m.scale.setScalar(Math.max(0.01, (1.2 + 1.9 * k * DR) * (0.7 + 0.6 * hsh(i * 5)))); m.material.opacity = 0.75 * Math.pow(1 - u, DF); });
    };
    g.userData.update(0); g.userData.grip = [0, 0, 0]; return g;
  },

  // ---------------------------------------------------------------- a claim form (pivot at its middle, front +Z): white, a grey header band, a big tooth icon, ruled
  // lines and boxes (no text); o.stamp [[t, 0..1]]: a big red stamp mark (a frame with a cross) pops onto it; o.w (0.3)
  poForm(o) {
    const w = o.w ?? 0.3, h = w * 1.36, g = grp();
    const sh = paintPlane(w, h, (c, Wc, Hc) => { c.fillStyle = '#FBFAF4'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#8FA4B8'; c.fillRect(0, 0, Wc, Hc * 0.1);
      c.save(); c.translate(Wc * 0.22, Hc * 0.24); const S = Wc * 0.11; c.fillStyle = '#FFFFFF'; c.strokeStyle = '#2A2A30'; c.lineWidth = S * 0.16;
      c.beginPath(); c.moveTo(-S, -S); c.quadraticCurveTo(0, -S * 1.4, S, -S); c.lineTo(S * 0.85, S * 0.2); c.lineTo(S * 0.55, S * 1.2); c.lineTo(S * 0.2, S * 0.3); c.lineTo(-S * 0.2, S * 0.3); c.lineTo(-S * 0.55, S * 1.2); c.lineTo(-S * 0.85, S * 0.2); c.closePath(); c.fill(); c.stroke(); c.restore();
      c.fillStyle = '#B4BCC8'; for (let i = 0; i < 2; i++) c.fillRect(Wc * 0.42, Hc * (0.18 + i * 0.07), Wc * 0.48, Hc * 0.025);
      for (let i = 0; i < 6; i++) c.fillRect(Wc * 0.1, Hc * (0.42 + i * 0.075), Wc * (0.8 - (i % 3) * 0.12), Hc * 0.02);
      c.strokeStyle = '#8A94A4'; c.lineWidth = Hc * 0.008; c.strokeRect(Wc * 0.62, Hc * 0.86, Wc * 0.28, Hc * 0.08); }, { res: 256, emissive: 0.2 });
    g.add(sh, at(box(w, h, 0.004, '#E8E6DE'), 0, 0, -0.003));
    const mk = paintPlane(w * 0.7, w * 0.5, (c, Wc, Hc) => { c.clearRect(0, 0, Wc, Hc); c.strokeStyle = '#D21F26'; c.lineWidth = Hc * 0.1; c.strokeRect(Hc * 0.07, Hc * 0.07, Wc - Hc * 0.14, Hc * 0.86);
      c.lineWidth = Hc * 0.13; c.lineCap = 'round'; c.beginPath(); c.moveTo(Wc * 0.25, Hc * 0.22); c.lineTo(Wc * 0.75, Hc * 0.78); c.moveTo(Wc * 0.75, Hc * 0.22); c.lineTo(Wc * 0.25, Hc * 0.78); c.stroke(); }, { res: 256, emissive: 0.4 });
    mk.material.transparent = true; mk.material.alphaTest = 0.3; mk.position.set(0, -h * 0.12, 0.004); mk.rotation.z = 0.18; g.add(mk);
    g.userData.update = t => { const v = keyAt(o.stamp, t, 0); mk.visible = v > 0.01; mk.scale.setScalar(Math.max(0.01, v < 1 ? outBack(v, 2.4) : 1)); };
    g.userData.update(0); g.userData.grip = [0, 0, 0]; return g;
  },

  // ---------------------------------------------------------------- a big blank cheque board (pivot at its middle, front +Z): pale green, a double border, wavy
  // security lines, an empty amount box, a signature scribble (no text, no digits); o.w (0.9)
  poCheque(o) {
    const w = o.w ?? 0.9, h = w * 0.46, g = grp();
    g.add(at(box(w, h, 0.02, '#CFE3C8', { outline: 0.008 }), 0, 0, -0.011));
    g.add(paintPlane(w, h, (c, Wc, Hc) => { c.fillStyle = '#E6F2DE'; c.fillRect(0, 0, Wc, Hc); c.strokeStyle = '#B8D4AC'; c.lineWidth = Hc * 0.01;
      for (let j = 0; j < 9; j++) { c.beginPath(); for (let x = 0; x <= Wc; x += 6) c.lineTo(x, Hc * (0.12 + j * 0.09) + Math.sin(x / Wc * TAU * 3 + j) * Hc * 0.02); c.stroke(); }
      c.strokeStyle = '#2C6A4A'; c.lineWidth = Hc * 0.03; c.strokeRect(Hc * 0.05, Hc * 0.05, Wc - Hc * 0.1, Hc * 0.9);
      c.fillStyle = '#FBFAF4'; c.fillRect(Wc * 0.58, Hc * 0.3, Wc * 0.34, Hc * 0.2); c.strokeRect(Wc * 0.58, Hc * 0.3, Wc * 0.34, Hc * 0.2);
      c.fillStyle = '#7FA28A'; c.fillRect(Wc * 0.08, Hc * 0.36, Wc * 0.42, Hc * 0.025); c.fillRect(Wc * 0.08, Hc * 0.58, Wc * 0.82, Hc * 0.025);
      c.strokeStyle = '#1E2A52'; c.lineWidth = Hc * 0.025; c.beginPath(); c.moveTo(Wc * 0.6, Hc * 0.82); for (let i = 0; i < 9; i++) c.quadraticCurveTo(Wc * (0.62 + i * 0.03), Hc * (i % 2 ? 0.66 : 0.9), Wc * (0.64 + i * 0.03), Hc * 0.78); c.stroke(); }, { res: 384, emissive: 0.25 }));
    g.userData.grip = [0, 0, 0]; return g;
  },

  // ---------------------------------------------------------------- the new clause poster (pivot at its top edge, front +Z): cream paper, a pink pig flying with
  // little white wings, two speed lines and a cloud (no text); four red pins; o.unroll [[t, 0..1]]: it unrolls down from the top; o.w (0.8)
  poPoster(o) {
    const w = o.w ?? 0.8, h = w * 1.2, g = grp(), sheet = grp(); g.add(sheet);
    const pl = paintPlane(w, h, (c, Wc, Hc) => { c.fillStyle = '#FBF4E2'; c.fillRect(0, 0, Wc, Hc); c.strokeStyle = '#2C6A8A'; c.lineWidth = Wc * 0.03; c.strokeRect(Wc * 0.04, Wc * 0.04, Wc * 0.92, Hc - Wc * 0.08);
      c.fillStyle = '#FFFFFF'; c.beginPath(); c.arc(Wc * 0.25, Hc * 0.78, Wc * 0.1, 0, TAU); c.arc(Wc * 0.36, Hc * 0.76, Wc * 0.12, 0, TAU); c.arc(Wc * 0.48, Hc * 0.79, Wc * 0.09, 0, TAU); c.fill();
      c.save(); c.translate(Wc * 0.52, Hc * 0.45); const S = Wc * 0.2; c.lineWidth = S * 0.07; c.strokeStyle = '#2A2020';
      c.fillStyle = '#FFFFFF'; for (const sd of [-1, 1]) { c.beginPath(); c.moveTo(-S * 0.1, -S * 0.4); c.quadraticCurveTo(sd * S * 0.4 - S * 0.1, -S * 1.5, sd * S * 0.9, -S * 1.25); c.quadraticCurveTo(sd * S * 0.5, -S * 0.9, S * 0.2, -S * 0.35); c.closePath(); c.fill(); c.stroke(); }
      c.fillStyle = '#F2A2AA'; c.beginPath(); c.ellipse(0, 0, S * 1.05, S * 0.65, 0, 0, TAU); c.fill(); c.stroke();
      c.beginPath(); c.arc(S * 0.95, -S * 0.25, S * 0.48, 0, TAU); c.fill(); c.stroke();
      c.fillStyle = '#E28890'; c.beginPath(); c.ellipse(S * 1.38, -S * 0.15, S * 0.14, S * 0.2, 0, 0, TAU); c.fill(); c.stroke();
      c.fillStyle = '#1B1418'; c.beginPath(); c.arc(S * 1.08, -S * 0.42, S * 0.07, 0, TAU); c.fill(); for (const y of [-0.2, -0.1]) { c.beginPath(); c.arc(S * 1.4, y * S, S * 0.03, 0, TAU); c.fill(); }
      c.fillStyle = '#F2A2AA'; c.beginPath(); c.moveTo(S * 0.75, -S * 0.65); c.lineTo(S * 0.82, -S * 1.0); c.lineTo(S * 1.0, -S * 0.7); c.fill(); c.stroke();
      for (const x of [-0.6, -0.2, 0.25, 0.6]) { c.beginPath(); c.moveTo(x * S, S * 0.5); c.lineTo(x * S + S * 0.05, S * 0.85); c.stroke(); }
      c.strokeStyle = '#5A8AB0'; c.lineWidth = S * 0.08; c.lineCap = 'round'; for (const y of [-0.2, 0.15, 0.45]) { c.beginPath(); c.moveTo(-S * 1.3, y * S); c.lineTo(-S * 1.9, y * S); c.stroke(); }
      c.restore(); }, { res: 320, emissive: 0.25 });
    pl.position.set(0, -h / 2, 0.006); sheet.add(pl, at(box(w, h, 0.008, '#E8DFC8'), 0, -h / 2, 0));
    for (const [x, y] of [[-0.42, -0.04], [0.42, -0.04], [-0.42, -0.96], [0.42, -0.96]]) sheet.add(at(sphere(0.025, '#D12A2A', 1), x * w, y * h, 0.03));
    g.userData.update = t => { const v = keyAt(o.unroll, t, 1); sheet.scale.set(1, Math.max(0.01, v), 1); sheet.visible = v > 0.01; };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the insurer's counter (pivot at the floor, the customer's side +Z; the clerk stands behind it
  // near z -0.6): a pale mint back wall at z -1.6 with a teal band and a plain white sign « MUTUELLE » (o.sign false: none; o.signX / o.signY), a cream counter with a teal front stripe at z 0, a pot
  // plant, a framed umbrella picture, a tiled floor; o.signX, o.w (7)
  poCounter(o) {
    const W = o.w ?? 7, g = grp(), bz = -1.6;
    const fl = paintPlane(W, 5, (c, Wc, Hc) => { c.fillStyle = '#D9D2C2'; c.fillRect(0, 0, Wc, Hc); c.strokeStyle = '#C4BCAA'; c.lineWidth = 2; for (let i = 0; i <= 14; i++) { c.beginPath(); c.moveTo(Wc * i / 14, 0); c.lineTo(Wc * i / 14, Hc); c.stroke(); } for (let j = 0; j <= 10; j++) { c.beginPath(); c.moveTo(0, Hc * j / 10); c.lineTo(Wc, Hc * j / 10); c.stroke(); } }, { res: 512, offset: true });
    fl.rotation.x = -PI / 2; fl.position.set(0, 0.012, bz + 2.5); g.add(fl);
    g.add(at(box(W, 3.4, 0.12, o.wall || '#CFE7DA', { pivot: 'bottom' }), 0, 0, bz - 0.06), at(box(W, 0.9, 0.03, o.band || '#3F8F98'), 0, 0.45, bz + 0.015), at(box(W, 0.06, 0.04, '#F4F1E8'), 0, 0.92, bz + 0.02));
    const sx = o.signX ?? 0;
    const sw = o.signW ?? 1.9, sign = paintPlane(sw, sw * 0.221, (c, Wc, Hc) => { c.fillStyle = '#FBFAF4'; c.fillRect(0, 0, Wc, Hc); c.strokeStyle = '#3F8F98'; c.lineWidth = Hc * 0.08; c.strokeRect(0, 0, Wc, Hc);
      c.fillStyle = '#2E6F78'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${Hc * 0.56}px Arial`; c.fillText('MUTUELLE', Wc / 2, Hc * 0.54); }, { res: 512, emissive: 0.3 });
    sign.position.set(sx, o.signY ?? 2.55, bz + 0.03); if (o.sign !== false) g.add(sign, at(box(sw + 0.06, sw * 0.221 + 0.06, 0.03, '#3F8F98'), sx, o.signY ?? 2.55, bz + 0.01));
    const umb = paintPlane(0.62, 0.78, (c, Wc, Hc) => { c.fillStyle = '#F7F1E2'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#3F8F98'; c.beginPath(); c.arc(Wc / 2, Hc * 0.48, Wc * 0.36, PI, TAU); c.closePath(); c.fill();
      c.strokeStyle = '#2A3A40'; c.lineWidth = Wc * 0.04; c.beginPath(); c.moveTo(Wc / 2, Hc * 0.48); c.lineTo(Wc / 2, Hc * 0.8); c.arc(Wc * 0.45, Hc * 0.8, Wc * 0.05, 0, PI); c.stroke(); }, { res: 128, emissive: 0.2 });
    umb.position.set(o.picX ?? 2.2, 1.75, bz + 0.03); g.add(umb, at(box(0.7, 0.86, 0.03, '#7A4A2A'), o.picX ?? 2.2, 1.75, bz + 0.01));
    g.add(at(box(o.cw ?? 3.2, 1.02, 0.62, '#F1EBDD', { pivot: 'bottom', outline: 0.006 }), 0, 0, -0.31), at(box((o.cw ?? 3.2) + 0.08, 0.05, 0.72, '#E3D9C4', { outline: 0.006 }), 0, 1.045, -0.31), at(box(o.cw ?? 3.2, 0.12, 0.02, '#3F8F98'), 0, 0.78, 0.005));
    g.add(at(box(0.32, 0.36, 0.32, '#C9473A', { pivot: 'bottom', taper: 1.2 }), -2.4, 0, bz + 0.4));
    for (let i = 0; i < 7; i++) { const p = grp(at(box(0.1, 0.7 + 0.25 * hsh(i), 0.025, ['#4E9A45', '#3F8F98', '#6DB352'][i % 3], { pivot: 'bottom', taper: { x: 0.15, z: 1 } }), 0, 0, 0, 0.35 + 0.3 * hsh(i * 2))); p.position.set(-2.4, 0.36, bz + 0.4); p.rotation.y = i * TAU / 7; g.add(p); }
    g.add(at(box(0.36, 0.06, 0.26, '#EDE7D6', { outline: 0.01 }), (o.cw ?? 3.2) / 2 - 0.4, 1.1, -0.35), at(box(0.34, 0.05, 0.24, '#F6F1E4'), (o.cw ?? 3.2) / 2 - 0.4, 1.15, -0.35, 0, 0.1, 0));
    return g;
  },

  // ---------------------------------------------------------------- a big T-bone steak on a white plate (pivot at the bottom of the plate): a brown steak with grill
  // marks and a cream fat rim, a white T bone; o.eat [[t, 0..1]]: the steak shrinks as it is eaten (the bone stays); o.r (0.3)
  poSteak(o) {
    const R = o.r ?? 0.3, g = grp();
    g.add(ink(cyl(R, R * 0.85, 0.035, '#FBFAF4', 24, { pivot: 'bottom' }), 0.02), at(cyl(R * 0.7, R * 0.7, 0.004, '#EDEAE2', 24), 0, 0.037, 0));
    const meat = grp(); meat.position.y = 0.04; g.add(meat);
    const sh = new THREE.Shape(); for (let i = 0; i <= 24; i++) { const a = i / 24 * TAU, rr = R * 0.62 * (1 + 0.16 * Math.cos(a) - 0.08 * Math.sin(2 * a)); if (i === 0) sh.moveTo(Math.cos(a) * rr * 1.15, Math.sin(a) * rr * 0.85); else sh.lineTo(Math.cos(a) * rr * 1.15, Math.sin(a) * rr * 0.85); }
    const geo = new THREE.ExtrudeGeometry(sh, { depth: 0.05, bevelEnabled: true, bevelThickness: 0.012, bevelSize: 0.015, bevelSegments: 1, curveSegments: 4 }); geo.rotateX(-PI / 2);
    const cv = canvas(256, 256), c = cv.getContext('2d'); c.fillStyle = '#9A4426'; c.fillRect(0, 0, 256, 256); c.strokeStyle = '#3E1A0E'; c.lineWidth = 10; for (let i = 0; i < 5; i++) { c.beginPath(); c.moveTo(i * 60 - 20, 0); c.lineTo(i * 60 + 80, 256); c.stroke(); }
    const t_ = tex(cv); t_.wrapS = t_.wrapT = THREE.RepeatWrapping; t_.repeat.set(4, 4); const top = L('#FFFFFF', { map: t_ }), side = L('#6E2E1A', { flatShading: true });
    const m = new THREE.Mesh(geo, [top, side]); m.castShadow = true; ink(m, 0.02); meat.add(m);
    const fat = new THREE.Mesh(new THREE.TorusGeometry(R * 0.58, 0.02, 4, 16, PI * 0.9), mat('#F4E6C4')); fat.rotation.x = -PI / 2; fat.scale.set(1.15, 0.85, 1); fat.position.set(0, 0.035, 0); fat.rotation.z = 0.0; meat.add(fat);
    const bone = grp(at(box(0.05, 0.04, R * 1.0, '#FBF6E8', { outline: 0.03 }), 0.02, 0.05, 0), at(box(R * 0.6, 0.04, 0.05, '#FBF6E8', { outline: 0.03 }), 0.02 - R * 0.25, 0.05, R * 0.28)); g.add(bone); bone.position.y = 0.035;
    g.userData.update = t => { const v = keyAt(o.eat, t, 0); meat.scale.set(Math.max(0.05, 1 - 0.7 * v), 1, Math.max(0.05, 1 - 0.55 * v)); meat.position.x = -R * 0.2 * v; };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- grain: a stream of golden grains falling o.h (0.6) from the pivot during o.pour [[t0, t1]], and a
  // heap on the ground (o.heap: [x, z] under it, its size keyed o.grow [[t, 0..1]])
  poGrain(o) {
    const H = o.h ?? 0.6, g = grp(), gr = [], col = ['#E6C15A', '#D9A93E', '#F2D77A'];
    for (let i = 0; i < 26; i++) { const m = sphere(0.012, col[i % 3], 0, { noGrain: true }); m.scale.set(1, 1.4, 1); m.castShadow = false; g.add(m); gr.push(m); }
    const heap = new THREE.Mesh(new THREE.ConeGeometry(0.2, 0.08, 10), mat('#E0B850')); heap.position.set(...(o.heap ? [o.heap[0], -H + 0.04, o.heap[1]] : [0, -H + 0.04, 0])); heap.receiveShadow = true; g.add(heap);
    const dots = []; for (let i = 0; i < 14; i++) { const m = sphere(0.014, col[i % 3], 0, { noGrain: true }); m.castShadow = false; m.position.set(heap.position.x + (hsh(i) - 0.5) * 0.3, heap.position.y + 0.04 * hsh(i * 3), heap.position.z + (hsh(i * 7) - 0.5) * 0.22); g.add(m); dots.push(m); }
    g.userData.update = t => {
      const on = inside(o.pour, t) >= 0;
      gr.forEach((m, i) => { m.visible = on; if (!on) return; const u = ((t * 1.9 + i / gr.length) % 1); m.position.set((hsh(i) - 0.5) * 0.04 + (hsh(i * 3) - 0.5) * 0.12 * u, -H * u * u * 0.98, (hsh(i * 5) - 0.5) * 0.05 * (1 + u)); });
      const v = keyAt(o.grow, t, o.grow ? 0 : 1); heap.visible = v > 0.02; heap.scale.set(Math.max(0.01, v), Math.max(0.01, v), Math.max(0.01, v)); dots.forEach((m, i) => { m.visible = v > 0.15 + 0.05 * (i % 4); });
    };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a small tin scoop of grain (pivot at the handle's end, the cup along +Z): o.full
  poScoop(o) {
    const g = grp(at(cyl(0.012, 0.012, 0.12, '#8A7A5A', 6), 0, 0, 0.06, PI / 2, 0, 0));
    const cup = ink(cyl(0.085, 0.07, 0.16, '#B9C0C8', 10, { open: true }), 0.03); cup.material = mat('#B9C0C8', { doubleSide: true }); cup.position.set(0, 0.02, 0.2); cup.rotation.x = PI / 2; g.add(cup);
    if (o.full !== false) { const gr = sphere(0.075, '#E6C15A', 1); gr.scale.set(1, 0.45, 1); gr.position.set(0, 0.07, 0.2); g.add(gr); }
    g.userData.grip = [0, 0, 0]; return g;
  },

  // ---------------------------------------------------------------- a dentist's head mirror (attach to the 'head' joint): a dark band round the forehead and a big
  // round silver mirror with a hole, tipped up; o.y (0.4) / o.z (0.12), o.r (0.08)
  poHeadMirror(o) {
    const R = o.r ?? 0.08, g = grp(), y = o.y ?? 0.5, z = o.z ?? 0.12;
    g.add(at(box(o.w ?? 0.36, 0.035, 0.02, '#2A2C34'), 0, y, z - 0.005));
    const m = grp(); m.position.set(0, y + 0.01, z + 0.02); m.rotation.x = -0.35; g.add(m);
    const disc = cyl(R, R, 0.012, '#DCE4EA', 20, { noGrain: true, emissive: '#7A8A94' }); disc.rotation.x = PI / 2; ink(disc, 0.06); m.add(disc);
    m.add(at(new THREE.Mesh(new THREE.CircleGeometry(R * 0.2, 12), B('#2A2C34')), 0, 0, 0.007), at(new THREE.Mesh(new THREE.CircleGeometry(R * 0.35, 12, 0.3, 1.2), B('#FFFFFF')), -R * 0.25, R * 0.2, 0.0068));
    return g;
  },

  // ---------------------------------------------------------------- a big dental mirror (pivot at the grip, the stem along +Y): a steel handle, a thin neck, a round
  // mirror tipped forward; o.L (0.5)
  poDentalMirror(o) {
    const Ln = o.L ?? 0.5, g = grp(at(cyl(0.016, 0.016, Ln * 0.45, '#9AA4AE', 8, { pivot: 'bottom' }), 0, -Ln * 0.1, 0), at(cyl(0.006, 0.008, Ln * 0.5, '#B8C0C8', 6, { pivot: 'bottom' }), 0, Ln * 0.35, 0));
    const hd = grp(); hd.position.set(0, Ln * 0.86, 0.0); hd.rotation.x = 0.6; g.add(hd);
    const d = cyl(0.055, 0.055, 0.012, '#C8D2DA', 18, { noGrain: true }); d.rotation.x = PI / 2; ink(d, 0.06); hd.add(d, at(new THREE.Mesh(new THREE.CircleGeometry(0.048, 18), B('#EAF4FA')), 0, 0, 0.007));
    g.userData.grip = [0, 0, 0]; return g;
  },

  // ---------------------------------------------------------------- a folded deckchair (pivot at its middle, length along Y): two wooden side bars, end rails, the
  // striped canvas folded between them; o.colors
  poFoldedChair(o) {
    const cols = o.colors || ['#E8463A', '#F4F1E8'], Ln = o.L ?? 1.05, Wd = o.w ?? 0.5, g = grp(), wc = '#B88A5A';
    for (const sd of [-1, 1]) g.add(at(ink(box(0.04, Ln, 0.04, wc), 0.03), sd * Wd / 2, 0, 0), at(box(0.035, Ln * 0.9, 0.035, '#A87A4A'), sd * (Wd / 2 - 0.045), 0, -0.03));
    for (const y of [-Ln / 2 + 0.03, Ln / 2 - 0.03]) g.add(at(box(Wd, 0.035, 0.035, wc), 0, y, 0));
    const n = 6; for (let i = 0; i < n; i++) g.add(at(box(Wd / n, Ln * 0.88, 0.012, cols[i % cols.length]), -Wd / 2 + (i + 0.5) * Wd / n, 0, 0.012));
    g.userData.grip = [0, 0, 0]; return g;
  },

  // ---------------------------------------------------------------- a fishing rod (pivot at the grip, the rod along +Y): a cork handle, a reel, a tapering rod o.L
  // (1.7) in six segments, a line hanging from the tip with a red-and-white float; o.droop [[t, rad]]: the rod sags (the line keeps hanging, o.tilt the rod's
  // own pitch; o.axis 'z': it sags about its own z instead, o.tilt then the rod's own roll), o.color, o.r (0.01) its radius at the grip, o.ink: an ink rim,
  // o.line (0.45) the line's length, o.wob [[t0, amp, f, dk]] a wobble of the line
  poFishingRod(o) {
    const Ln = o.L ?? 1.7, NS = 6, sl = Ln / NS, g = grp(at(cyl(0.022, 0.022, 0.28, '#C89A62', 8), 0, 0, 0)), RC = o.color || '#2A3A5A', r0 = o.r ?? 0.01;
    const reel = cyl(0.05, 0.05, 0.035, '#9AA4AE', 12, { outline: 0.03 }); reel.rotation.z = PI / 2; reel.position.set(0.04, 0.02, 0); g.add(reel);
    const segs = []; let par = g;
    for (let i = 0; i < NS; i++) { const sg = grp(); sg.position.y = i ? sl : 0.12; par.add(sg); const rr = r0 * (1 - 0.55 * i / NS), m = cyl(rr * 0.82, rr, sl * 1.02, RC, 6, { pivot: 'bottom' }); if (o.ink) ink(m, 0.12); sg.add(m); segs.push(sg); par = sg; }
    const tip = grp(); tip.position.y = sl; par.add(tip);
    const LL = o.line ?? 0.45; tip.add(at(cyl(0.002, 0.002, LL, '#E8E8E8', 3, { pivot: 'top' }), 0, 0, 0), at(sphere(0.025, '#E23A3A', 1), 0, -LL, 0), at(sphere(0.018, '#FBFAF4', 1), 0, -LL + 0.03, 0));
    const AZ = o.axis === 'z';
    // (story 104, review 2) o.dsign -1: the rod bends the other way about X (a rod leaning toward the lens droops toward it, its tip bouncing in the frame)
    const DS = o.dsign ?? 1;
    g.userData.update = t => { const d = keyAt(o.droop, t, 0), w = rattle(o.wob, t); segs.forEach((sg, i) => { const v = i ? d / (NS - 1) : 0; if (AZ) sg.rotation.z = -v; else sg.rotation.x = v * DS; });
      if (AZ) tip.rotation.z = d + (o.tilt ?? 0) + w; else tip.rotation.x = -(d + (o.tilt ?? 0)) * DS + w; };
    g.userData.update(0); g.userData.grip = [0, 0, 0]; return g;
  },

  // ---------------------------------------------------------------- a row of narrow terrace house fronts (pivot at the floor under the middle, fronts +Z): o.n (5)
  // fronts o.w (2.3) wide, pastel, each with a door that swings in (o.open [[t, 0..1]], each next door o.stagger (0.06 s) later; o.rev: from the last door),
  // a window, a step; o.slam: a hinge wobble from that time (o.wob its amplitude, 0.15); o.swing (1.9 rad): how far a door opens outward at 1 (2.95: flat
  // against the wall beside it)
  poRowHouses(o) {
    const n = o.n ?? 5, w = o.w ?? 2.3, g = grp(), cols = o.colors || ['#F0C6CF', '#B8E0D2', '#F4E1A8', '#C9D4F2', '#F2C9A8'], doors = ['#2F7F8C', '#B5302A', '#2F5E8C', '#3E7A4A', '#7A3E6A'], P_ = [];
    for (let i = 0; i < n; i++) { const { g: f, piv } = houseFront(w, o.h ?? 3.1, cols[i % cols.length], doors[i % doors.length], i); f.position.x = (i - (n - 1) / 2) * w; g.add(f); P_.push(piv); }
    g.add(at(box(n * w + 2, 0.12, 2.6, '#E8DCC2', { pivot: 'bottom' }), 0, 0, 1.3));
    const stg = o.stagger ?? 0.06;
    g.userData.update = t => { P_.forEach((p, i) => { const j = o.rev ? n - 1 - i : i, v = keyAt(o.open, t - j * stg, 0); p.rotation.y = -(o.swing ?? 1.9) * v + rattle(o.slam ? [[o.slam + j * stg, o.wob ?? 0.15, 22, 5]] : null, t); }); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a plain room (pivot at the floor in the middle; back wall at z -o.d/2): walls o.wall with a
  // dado band o.band, a skirting trim, a floor o.floor (raised with a polygon offset); o.side false: no side walls; o.door {x, w, h, glass}: a doorway in the
  // back wall (a glass door shows a pale lit street); o.curtains [x...]: plain drapes; o.panel: wooden wainscot
  poRoom(o) {
    const W = o.w ?? 7, D = o.d ?? 6, H = o.h ?? 3.2, bz = -D / 2, g = grp(), WC = o.wall || '#E9DCC8';
    const fl = new THREE.Mesh(new THREE.PlaneGeometry(W, D), L(o.floor || '#C79E72', { polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -8 })); fl.rotation.x = -PI / 2; fl.position.y = 0.012; fl.receiveShadow = true; g.add(fl);
    const dr = o.door;
    if (dr) { const dx = dr.x ?? 0, dw = dr.w ?? 1.6, dh = dr.h ?? 2.4, lw = dx - dw / 2 + W / 2, rw = W / 2 - (dx + dw / 2);
      g.add(at(box(lw, H, 0.12, WC, { pivot: 'bottom' }), -W / 2 + lw / 2, 0, bz - 0.06), at(box(rw, H, 0.12, WC, { pivot: 'bottom' }), dx + dw / 2 + rw / 2, 0, bz - 0.06), at(box(dw, H - dh, 0.12, WC, { pivot: 'bottom' }), dx, dh, bz - 0.06));
      g.add(at(box(0.1, dh, 0.16, o.trim || '#F4EEE2'), dx - dw / 2 - 0.05, dh / 2, bz), at(box(0.1, dh, 0.16, o.trim || '#F4EEE2'), dx + dw / 2 + 0.05, dh / 2, bz), at(box(dw + 0.2, 0.1, 0.16, o.trim || '#F4EEE2'), dx, dh + 0.05, bz));
      const out = paintPlane(dw + 0.4, dh + 0.3, (c, Wc, Hc) => { const gg = c.createLinearGradient(0, 0, 0, Hc); gg.addColorStop(0, '#BFE3F4'); gg.addColorStop(0.62, '#E8F4F8'); gg.addColorStop(0.63, '#C9C2B2'); gg.addColorStop(1, '#B4AC9A'); c.fillStyle = gg; c.fillRect(0, 0, Wc, Hc);
        c.fillStyle = '#9DBF86'; c.fillRect(0, Hc * 0.5, Wc, Hc * 0.13); }, { res: 128, emissive: 0.9 });
      out.position.set(dx, (dh + 0.3) / 2, bz - 0.4); g.add(out);
      if (dr.glass) for (const sd of [-1, 1]) g.add(at(box(0.05, dh, 0.06, '#5A6470'), dx + sd * dw * 0.0, dh / 2, bz - 0.02));
    } else g.add(at(box(W, H, 0.12, WC, { pivot: 'bottom' }), 0, 0, bz - 0.06));
    if (o.side !== false) g.add(at(box(0.12, H, D, WC, { pivot: 'bottom' }), -W / 2, 0, 0), at(box(0.12, H, D, WC, { pivot: 'bottom' }), W / 2, 0, 0));
    if (o.band !== false) g.add(at(box(W, o.bandH ?? 1.0, 0.025, o.band || '#B8A07A'), 0, (o.bandH ?? 1.0) / 2, bz + 0.012));
    g.add(at(box(W, 0.12, 0.04, o.trim || '#F4EEE2'), 0, 0.06, bz + 0.02));
    if (o.panel) for (let i = 0; i < Math.floor(W / 0.9); i++) g.add(at(box(0.7, 0.6, 0.02, '#9A6A44'), -W / 2 + 0.45 + i * 0.9, 0.5, bz + 0.03));
    for (const x of o.curtains || []) { for (let j = 0; j < 4; j++) g.add(at(box(0.16, H - 0.25, 0.08, o.curtain || '#5A6E8C', { pivot: 'bottom' }), x + (j - 1.5) * 0.15, 0.05, bz + 0.1 + (j % 2) * 0.04)); g.add(at(box(0.8, 0.12, 0.14, '#3E4A5E'), x, H - 0.15, bz + 0.12)); }
    return g;
  },

  // ---------------------------------------------------------------- a wall with a doorway, seen from the corridor (pivot at the floor under the middle of the doorway,
  // the corridor side +Z): o.w (7) x o.h (3.2), the opening o.dw (1.3) x o.dh (2.4) cut through it (the room behind shows), a cream frame; o.color
  poWall(o) {
    const W = o.w ?? 7, H = o.h ?? 3.2, dw = o.dw ?? 1.3, dh = o.dh ?? 2.4, C = o.color || '#E4DCC8', side = (W - dw) / 2, g = grp();
    g.add(at(box(side, H, 0.16, C, { pivot: 'bottom' }), -(dw + side) / 2, 0, 0), at(box(side, H, 0.16, C, { pivot: 'bottom' }), (dw + side) / 2, 0, 0), at(box(dw, H - dh, 0.16, C, { pivot: 'bottom' }), 0, dh, 0));
    const tr = o.trim || '#F4EEE2';
    g.add(at(box(0.1, dh, 0.22, tr), -dw / 2 - 0.05, dh / 2, 0), at(box(0.1, dh, 0.22, tr), dw / 2 + 0.05, dh / 2, 0), at(box(dw + 0.2, 0.1, 0.22, tr), 0, dh + 0.05, 0));
    if (o.band !== false) for (const sd of [-1, 1]) g.add(at(box(side, 1.0, 0.02, o.band || '#B8A07A'), sd * (dw + side) / 2, 0.5, 0.09));
    return g;
  },

  // ---------------------------------------------------------------- a wooden crate (pivot at the floor, front +Z): slatted sides o.w (1.1) x o.h (0.5) x o.d (0.6)
  poCrate(o) {
    const w = o.w ?? 1.1, h = o.h ?? 0.5, d = o.d ?? 0.6, g = grp(at(box(w, h, d, '#C8955E', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0));
    for (let i = 0; i < 3; i++) g.add(at(box(w + 0.01, 0.03, d + 0.01, '#9A6A3E'), 0, 0.08 + i * (h - 0.12) / 2, 0));
    for (const sd of [-1, 1]) g.add(at(box(0.05, h, 0.05, '#9A6A3E'), sd * (w / 2 - 0.02), h / 2, d / 2));
    g.userData.top = [0, h, 0]; return g;
  },

  // ---------------------------------------------------------------- a reception desk (pivot at the floor, the visitor's side +Z): a light wood counter with a teal
  // band and a cream top; o.w (2.0)
  poReception(o) {
    const w = o.w ?? 2.0, g = grp(at(box(w, 1.05, 0.6, '#D8B88A', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(w + 0.08, 0.05, 0.7, '#F1EBDD', { outline: 0.006 }), 0, 1.075, 0), at(box(w, 0.1, 0.02, '#3F8F98'), 0, 0.8, 0.305));
    g.userData.top = [0, 1.1, 0]; return g;
  },

  // ---------------------------------------------------------------- an aeroplane cabin row (pivot at the floor between the two seats, seats facing +Z): a cream side
  // wall at x -o.wx (0.95) with an oval window (white frame, a blue sky with clouds sliding past toward -Z at o.speed), two blue fabric seats with white
  // headrest covers and armrests, a carpet, the overhead bin; o.s (1.25) the seats' scale (the hero is 2.3 m tall); o.wall the side wall's colour
  poCabin(o) {
    const s = o.s ?? 1.25, g = grp(), wx = o.wx ?? 0.95, seatW = 0.62 * s;
    g.add(at(box(3.2, 0.03, 4, '#3A4A72'), 0, 0.0, 0));
    // (story 104, final pass) o.wall: the side wall's colour (a white wing must stand out on it)
    const wall = grp(at(box(0.12, 2.6, 4, o.wall || '#EDE7DA', { pivot: 'bottom' }), 0, 0, 0)); wall.position.x = -wx - 0.06; g.add(wall);
    g.add(at(box(0.6, 0.4, 4, '#E4DDCB', { outline: 0.005 }), -wx + 0.25, 2.75, 0), at(box(0.04, 0.04, 4, '#BFB8A6'), -wx + 0.0, 2.5, 0));
    const cv = canvas(512, 256), c = cv.getContext('2d'), gg = c.createLinearGradient(0, 0, 0, 256); gg.addColorStop(0, '#5FA8E0'); gg.addColorStop(1, '#CFE8F6'); c.fillStyle = gg; c.fillRect(0, 0, 512, 256);
    c.fillStyle = '#FFFFFF'; for (let i = 0; i < 6; i++) { const x = i * 90 + 20, y = 70 + 90 * hsh(i * 3); for (let j = 0; j < 4; j++) { c.beginPath(); c.arc(x + j * 22, y - (j % 2) * 12, 22, 0, TAU); c.fill(); } }
    const st = tex(cv); st.wrapS = THREE.RepeatWrapping; st.repeat.set(0.5, 1);
    const wy = o.wy ?? 1.62, wz = o.wz ?? 0.15, ww = 0.42, wh = 0.58;
    const sky = new THREE.Mesh(new THREE.CircleGeometry(0.5, 28), new THREE.MeshBasicMaterial({ map: st })); sky.scale.set(ww, wh, 1); sky.rotation.y = PI / 2; sky.position.set(-wx + 0.005, wy, wz); g.add(sky);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.5, 0.07, 6, 28), mat('#FBFAF4')); ring.scale.set(ww, wh, 0.6); ring.rotation.y = PI / 2; ring.position.set(-wx + 0.01, wy, wz); g.add(ring);
    const shade = box(0.02, 0.12, ww * 0.9, '#E4DDCB'); shade.position.set(-wx + 0.02, wy + wh * 0.42, wz); g.add(shade);
    const seat = (x) => { const q = grp(); q.position.x = x; q.scale.setScalar(s);
      q.add(at(box(0.56, 0.3, 0.5, '#2A3550', { pivot: 'bottom' }), 0, 0.05, 0), at(ink(box(0.56, 0.14, 0.54, '#3657A0', { pivot: 'bottom' }), 0.01), 0, 0.33, 0.02));
      const back = grp(at(ink(box(0.56, 0.8, 0.16, '#3657A0'), 0.01), 0, 0.4, 0), at(box(0.42, 0.2, 0.02, '#F4F1E8'), 0, 0.68, 0.085)); back.position.set(0, 0.45, -0.24); back.rotation.x = -0.14; q.add(back);
      for (const sd of [-1, 1]) q.add(at(box(0.06, 0.06, 0.42, '#2A3550', { outline: 0.01 }), sd * 0.3, 0.62, 0.0)); return q; };
    g.add(seat(-seatW / 2 - 0.02), seat(seatW / 2 + 0.02));
    g.userData.update = t => { st.offset.x = (t * (o.speed ?? 0.35)) % 1; };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the pig in the window seat (pivot at the seat cushion under it, front +Z): a big pink pig sitting
  // up, a round body, a big head with a snout and nostrils, pointy ears (o.ears [[t0, t1]] flick), googly eyes (o.blinks, o.gaze [[t, gx, gy]]), a smile; little
  // white feathered costume wings on its back with an elastic strap (o.flap [[t0, t1]]; o.wingL); a grey lap belt with a buckle; o.yaw [[t, rad]] the head;
  // o.sq [[t, sx, sy, sz]]; o.wiggle [[t0, t1]] a wiggle in the seat; o.s scale
  poPig(o) {
    const s = o.s ?? 1, P = '#F0A6AC', PD = '#D9868E', DK = '#B9606A', g = grp(), rig = grp(); g.add(rig);
    rig.add(at(ink(facet(0.34, 0.36, 0.3, P, 21, 0.04), 0.025), 0, 0.36, 0), at(facet(0.25, 0.25, 0.12, '#F6B8BD', 22, 0.03), 0, 0.3, 0.22));
    for (const sd of [-1, 1]) { rig.add(at(ink(cyl(0.075, 0.07, 0.3, P, 7), 0.04), sd * 0.16, 0.12, 0.25, PI / 2 - 0.15, 0, 0), at(cyl(0.072, 0.072, 0.06, DK, 7), sd * 0.16, 0.1, 0.42, PI / 2 - 0.15, 0, 0));
      rig.add(at(ink(cyl(0.065, 0.06, 0.28, P, 7), 0.04), sd * 0.27, 0.42, 0.14, 0.9, 0, sd * 0.35), at(cyl(0.062, 0.062, 0.05, DK, 7), sd * 0.24, 0.31, 0.27, 0.9, 0, sd * 0.35)); }
    rig.add(at(box(0.72, 0.07, 0.04, '#7A808A'), 0, 0.2, 0.3), at(box(0.12, 0.09, 0.05, '#C8CED6', { outline: 0.02 }), 0, 0.2, 0.32));
    const wings = [];
    for (const sd of [-1, 1]) { const wp = grp(); wp.position.set(sd * 0.22, 0.6, -0.2); rig.add(wp); const wg = featherWing(o.wingL ?? 0.46); wg.scale.x = sd; wg.rotation.z = sd * 0.25; wp.add(wg); wings.push([wp, sd]); }
    rig.add(at(box(0.5, 0.035, 0.03, '#E8E4DC'), 0, 0.62, 0.0, 0, 0, 0));
    const head = grp(); head.position.set(0, 0.78, 0.05); rig.add(head);
    head.add(ink(facet(0.27, 0.24, 0.24, P, 23, 0.04), 0.025));
    const sn = ink(cyl(0.1, 0.11, 0.09, PD, 10), 0.04); sn.rotation.x = PI / 2; sn.position.set(0, -0.04, 0.24); head.add(sn);
    for (const sd of [-1, 1]) head.add(at(new THREE.Mesh(new THREE.CircleGeometry(0.022, 10), B('#5A2A30')), sd * 0.035, -0.04, 0.287));
    head.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.06, 0.009, 4, 12, PI), B('#3A1A1E')), 0, -0.14, 0.215, 0, 0, PI));
    const ears = [];
    for (const sd of [-1, 1]) { const ep = grp(); ep.position.set(sd * 0.15, 0.17, 0.02); head.add(ep); const e = new THREE.Mesh(new THREE.ConeGeometry(0.075, 0.17, 4), mat(P)); e.position.y = 0.07; ink(e, 0.05); ep.add(e); ep.rotation.set(0.35, 0, -sd * 0.45); ears.push([ep, sd]); }
    const eyes = [];
    for (const sd of [-1, 1]) { const eg = grp(); eg.position.set(sd * 0.1, 0.07, 0.19); eg.rotation.y = sd * 0.3; head.add(eg);
      const w = sphere(0.055, '#FFFFFF', 1, { noGrain: true, emissive: '#3A3A3A' }); w.scale.z = 0.45; ink(w, 0.12); eg.add(w);
      const pup = new THREE.Mesh(new THREE.CircleGeometry(0.024, 14), B('#0B0C0F')); pup.position.z = 0.026; eg.add(pup); eyes.push({ eg, pup }); }
    rig.scale.setScalar(s);
    const sq = (o.sq || []).map(q => [q[0], q[1]]), sqy = (o.sq || []).map(q => [q[0], q[2]]), gzx = (o.gaze || []).map(q => [q[0], q[1]]), gzy = (o.gaze || []).map(q => [q[0], q[2] ?? 0]);
    g.userData.update = t => {
      rig.scale.set(s * keyAt(sq, t, 1), s * keyAt(sqy, t, 1) * (1 + 0.012 * Math.sin(t * 2.6)), s * keyAt(sq, t, 1));
      const wd = inside(o.wiggle, t); rig.rotation.z = wd >= 0 ? 0.13 * Math.sin(wd * TAU * 3.6) * Math.exp(-wd * 1.2) : 0; rig.position.y = wd >= 0 ? 0.035 * Math.abs(Math.sin(wd * TAU * 3.6)) * Math.exp(-wd * 1.2) : 0;
      head.rotation.set(keyAt(o.pitch, t, 0), keyAt(o.yaw, t, 0), keyAt(o.roll, t, 0) + 0.03 * Math.sin(t * 1.3));
      // (story 104, review 2) o.wingRaise (rad, or [its right wing, its left wing]): the wings held raised in a V above the shoulders (clear of the body
      // and of a neighbour beside it); the flutter then half as wide
      const fd = inside(o.flap, t), fl = fd >= 0 ? 0.35 + 0.35 * Math.sin(fd * TAU * 6) : 0;
      for (const [wp, sd] of wings) { const wr = Array.isArray(o.wingRaise) ? o.wingRaise[sd > 0 ? 1 : 0] : (o.wingRaise ?? 0); wp.rotation.z = sd * (wr + fl * (wr ? 0.5 : 1)); }
      const ed = inside(o.ears, t), ew = ed >= 0 ? 0.3 * Math.sin(ed * TAU * 5) : 0; for (const [ep, sd] of ears) ep.rotation.z = -sd * (0.45 + ew);
      const bl = pulse(o.blinks, t, 0.13), gx = keyAt(gzx, t, 0), gy = keyAt(gzy, t, 0);
      for (const E of eyes) { E.eg.scale.y = Math.max(0.07, 1 - 0.94 * bl); E.pup.position.set(gx * 0.016, gy * 0.014, 0.026); }
    };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- two big blank boarding cards, fanned (pivot at their grip, front +Z): white, a blue top band
  // with a small white plane, a dashed tear line and stub, grey lines (no text, no digits); o.w (0.34)
  poCards(o) {
    const w = o.w ?? 0.34, h = w * 0.46, g = grp();
    const card = () => paintPlane(w, h, (c, Wc, Hc) => { c.fillStyle = '#FBFAF4'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#2F62B5'; c.fillRect(0, 0, Wc, Hc * 0.26);
      c.fillStyle = '#FFFFFF'; c.save(); c.translate(Wc * 0.13, Hc * 0.135); const q = Hc * 0.1; c.beginPath(); c.ellipse(0, 0, q * 1.3, q * 0.28, 0, 0, TAU); c.fill();
      c.beginPath(); c.moveTo(-q * 0.2, 0); c.lineTo(-q * 0.55, q * 0.75); c.lineTo(-q * 0.25, q * 0.75); c.lineTo(q * 0.35, 0); c.fill();
      c.beginPath(); c.moveTo(-q * 1.0, 0); c.lineTo(-q * 1.35, -q * 0.65); c.lineTo(-q * 1.1, -q * 0.65); c.lineTo(-q * 0.7, 0); c.fill(); c.restore();
      c.strokeStyle = '#9AA4B4'; c.setLineDash([Hc * 0.05, Hc * 0.04]); c.lineWidth = Hc * 0.02; c.beginPath(); c.moveTo(Wc * 0.72, Hc * 0.3); c.lineTo(Wc * 0.72, Hc); c.stroke(); c.setLineDash([]);
      c.fillStyle = '#B4BCC8'; for (let i = 0; i < 3; i++) c.fillRect(Wc * 0.06, Hc * (0.42 + i * 0.17), Wc * (0.56 - i * 0.12), Hc * 0.06); c.fillRect(Wc * 0.77, Hc * 0.45, Wc * 0.17, Hc * 0.06); c.fillRect(Wc * 0.77, Hc * 0.65, Wc * 0.12, Hc * 0.06);
      c.strokeStyle = '#2F62B5'; c.lineWidth = Hc * 0.04; c.strokeRect(1, 1, Wc - 2, Hc - 2); }, { res: 256, emissive: 0.3, double: true });
    const a = card(), b = card(); a.position.set(-w * 0.12, h * 0.12, -0.004); a.rotation.z = 0.16; b.position.set(w * 0.1, -h * 0.05, 0.004); b.rotation.z = -0.08; g.add(a, b);
    g.userData.grip = [0, 0, 0]; return g;
  },

  // ---------------------------------------------------------------- sparkles (pivot anywhere): 4-point stars at o.pts [[x, y, z, t0, size], ...] that pop open and
  // shut in 0.5 s; o.period: each one comes back that often; o.color
  poSparkle(o) {
    const g = grp(), ps = (o.pts || []).map(([x, y, z, t0, sz]) => { const sp = starSprite(o.color); sp.position.set(x, y, z); g.add(sp); return { sp, t0, s: sz ?? 0.25 }; });
    g.userData.update = t => { for (const p of ps) { let d = t - p.t0; if (o.period && d > 0) d %= o.period; sparkAt(p.sp, d + p.t0, [p.t0], p.s); } };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a soft blob of light on the faces (no visible source; pivot at the light): a warm point light o.I
  // (1.4) with range o.R (2), keyed o.at [[t, k]] (0..1)
  poFill(o) {
    const g = grp(), lt = new THREE.PointLight(o.color || '#FFE8CC', o.I ?? 1.4, o.R ?? 2.0, 1.2); g.add(lt);
    g.userData.update = t => { lt.intensity = (o.I ?? 1.4) * (o.at ? keyAt(o.at, t, 1) : 1); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- an empty prop that keeps the actors named in o.who (ids) and the props named in o.props out of
  // the shadow map every frame (the VSM soft shadows also draw the meshes that receive shadow: castShadow and receiveShadow both off)
  poNoShadow(o) { const g = grp(), names = [].concat(o.who || []);
    g.userData.update = () => { let rt = g; while (rt.parent) rt = rt.parent; if (rt === g) return;
      for (const n of names) { const a = rt.getObjectByName(n); if (a) noShadow(a); } };
    return g; },

  // ---------------------------------------------------------------- a stiff card held up (pivot at its middle, front +Z): a drawing of a hen in profile, her beak wide
  // open and empty (no teeth, a pink gum), a blue dashed ring round the beak (no text); o.w (0.46)
  poHenCard(o) {
    const w = o.w ?? 0.46, h = w * 0.78, g = grp();
    g.add(at(box(w, h, 0.012, '#E8E2D2', { outline: 0.01 }), 0, 0, -0.007));
    g.add(paintPlane(w * 0.94, h * 0.92, (c, Wc, Hc) => { c.fillStyle = '#FBF8EE'; c.fillRect(0, 0, Wc, Hc);
      c.save(); c.translate(Wc * 0.36, Hc * 0.52); const S = Wc * 0.2; c.lineWidth = S * 0.07; c.strokeStyle = '#2A2020'; c.lineJoin = 'round';
      c.strokeStyle = '#2A2020'; c.beginPath(); c.moveTo(-S * 0.3, S * 0.75); c.lineTo(-S * 0.35, S * 1.35); c.moveTo(S * 0.2, S * 0.75); c.lineTo(S * 0.25, S * 1.35); c.stroke();
      c.fillStyle = '#FFFFFF'; c.beginPath(); c.ellipse(0, S * 0.3, S * 1.0, S * 0.62, 0, 0, TAU); c.fill(); c.stroke();
      c.beginPath(); c.arc(S * 0.8, -S * 0.42, S * 0.44, 0, TAU); c.fill(); c.stroke();
      c.fillStyle = '#E3342A'; for (const [x, y] of [[0.58, -0.88], [0.82, -0.96], [1.04, -0.84]]) { c.beginPath(); c.arc(x * S, y * S, S * 0.15, 0, TAU); c.fill(); }
      c.fillStyle = '#7A1E22'; c.beginPath(); c.moveTo(S * 1.12, -S * 0.5); c.lineTo(S * 1.9, -S * 0.7); c.lineTo(S * 1.85, S * 0.05); c.lineTo(S * 1.12, -S * 0.2); c.closePath(); c.fill();
      c.fillStyle = '#F2A2AA'; c.beginPath(); c.moveTo(S * 1.15, -S * 0.27); c.lineTo(S * 1.82, -S * 0.02); c.lineTo(S * 1.82, S * 0.06); c.lineTo(S * 1.15, -S * 0.17); c.closePath(); c.fill();
      c.fillStyle = '#F6B523'; c.beginPath(); c.moveTo(S * 1.12, -S * 0.66); c.lineTo(S * 2.0, -S * 0.82); c.lineTo(S * 1.16, -S * 0.42); c.closePath(); c.fill(); c.stroke();
      c.fillStyle = '#E5801C'; c.beginPath(); c.moveTo(S * 1.12, -S * 0.24); c.lineTo(S * 1.92, S * 0.12); c.lineTo(S * 1.12, -S * 0.08); c.closePath(); c.fill(); c.stroke();
      c.fillStyle = '#1B1418'; c.beginPath(); c.arc(S * 0.92, -S * 0.52, S * 0.08, 0, TAU); c.fill();
      c.strokeStyle = '#2F7FC9'; c.lineWidth = S * 0.06; c.setLineDash([S * 0.14, S * 0.1]); c.beginPath(); c.arc(S * 1.55, -S * 0.3, S * 0.62, 0, TAU); c.stroke(); c.setLineDash([]);
      c.restore(); c.strokeStyle = '#3F8F98'; c.lineWidth = Hc * 0.03; c.strokeRect(Hc * 0.03, Hc * 0.03, Wc - Hc * 0.06, Hc * 0.94); }, { res: 320, emissive: 0.3 }));
    g.userData.grip = [0, 0, 0]; return g;
  },

  // ---------------------------------------------------------------- stars circling a bitten mitten (attach to a hand, face the camera): o.n (3) yellow five-point
  // stars with an ink rim on an ellipse o.r (0.13) wide, o.y above the pivot, going round at o.speed (1.4) turns a second and pulsing; o.on [[t0, t1]] (default always)
  poThrob(o) {
    const n = o.n ?? 3, R = o.r ?? 0.13, sz = o.size ?? 0.045, sh = new THREE.Shape(), g = grp(), S = [];
    for (let i = 0; i < 10; i++) { const a = i * PI / 5 + PI / 2, rr = i % 2 ? 0.45 : 1; sh[i ? 'lineTo' : 'moveTo'](Math.cos(a) * rr, Math.sin(a) * rr); } sh.closePath();
    const geo = new THREE.ShapeGeometry(sh);
    for (let i = 0; i < n; i++) { const st = grp(), f = new THREE.Mesh(geo, B('#FFD83A', { side: THREE.DoubleSide })), rim = new THREE.Mesh(geo, B(INK, { side: THREE.DoubleSide }));
      rim.scale.setScalar(1.3); rim.position.z = -0.002; st.add(f, rim); g.add(st); S.push(st); }
    g.userData.update = t => { const on = !o.on || inside(o.on, t) >= 0; S.forEach((st, i) => { st.visible = on; if (!on) return; const a = t * TAU * (o.speed ?? 1.4) + i * TAU / n;
      st.position.set(Math.cos(a) * R, (o.y ?? 0.08) + Math.sin(a) * R * 0.4, Math.sin(a) * 0.04); st.rotation.z = t * 4 + i; st.scale.setScalar(sz * (0.85 + 0.3 * Math.sin(t * 15 + i * 2))); }); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- (story 104, final pass) a plain wall panel (pivot at the floor under its middle, front +Z): o.w (5)
  // x o.h (3.2), colour o.color, a skirting o.trim; a pale flat ground behind a gesture that must read (a stretched arm against light)
  poBackdrop(o) {
    const W = o.w ?? 5, H = o.h ?? 3.2, g = grp(at(box(W, H, 0.1, o.color || '#DCE6EE', { pivot: 'bottom' }), 0, 0, -0.05));
    g.add(at(box(W, 0.12, 0.04, o.trim || '#F4EEE2'), 0, 0.06, 0.02));
    return noShadow(g);
  },

  // ---------------------------------------------------------------- (story 104, final pass) one cartoon dust cloud (pivot at its root, where it bursts out from; it
  // billows up and out toward +Y and along X): o.n (7) inked grey-beige lumps packed into ONE irregular mass that swells from nothing, then shrinks away
  // to nothing (never transparent, never a row of balls: the row of white puffs read as eggs), plus o.wisps (2) small lumps that curl off sideways and
  // up and vanish (shrinking, the lumps draw in to the core: spread apart they read as balls again); o.at [t0, ...], o.dur (0.75), o.r (0.22) the
  // cloud's radius at its fullest, o.w (1) its spread along X against its height, o.color
  poDustCloud(o) {
    const g = grp(), R = o.r ?? 0.22, D = o.dur ?? 0.75, N = o.n ?? 7, NW = o.wisps ?? 2, C = o.color || '#CBC2B0', C2 = o.color2 || '#B9AF9C', Q = [];
    for (let i = 0; i < N + NW; i++) { const wsp = i >= N, m = ink(new THREE.Mesh(new THREE.IcosahedronGeometry(1, 1), L(i % 3 === 1 ? C2 : C, { emissive: o.emissive || '#3E3A32', flatShading: true })), wsp ? 0.07 : 0.045);
      m.castShadow = m.receiveShadow = false; g.add(m);
      // a lump's place in the cloud at its fullest: spread along X (o.w), up in Y, a little in Z; the first lump is the core
      const a = (i / N) * TAU + hsh(i + 3) * 0.7, sw = o.w ?? 1;
      const home = wsp ? [(i - N) % 2 ? 1 : -1, 0.85, 0.15] : (i === 0 ? [0, 0.45, 0] : [Math.cos(a) * 0.62 * sw, 0.5 + Math.sin(a) * 0.42, 0.2 * Math.sin(a * 1.7)]);
      Q.push({ m, wsp, home, sz: wsp ? 0.32 : (i === 0 ? 0.78 : 0.5 + 0.22 * hsh(i * 5)), ph: hsh(i * 11) }); }
    g.userData.update = t => { let d = -1; for (const t0 of o.at || []) if (t >= t0 && t < t0 + D) d = t - t0;
      for (const q of Q) { q.m.visible = d >= 0; if (d < 0) continue; const u = d / D;
        if (!q.wsp) { const grow = 1 - Math.pow(1 - Math.min(1, u / 0.3), 3), shrink = u < 0.5 ? 1 : Math.max(0, 1 - (u - 0.5) / 0.5), lift = 1 + 0.35 * u;
          const pull = 0.4 + 0.6 * shrink;
          q.m.position.set(q.home[0] * R * (0.35 + 0.65 * grow) * (1 + 0.25 * u) * pull, (q.home[1] * R * (0.3 + 0.7 * grow)) * lift * (0.6 + 0.4 * shrink), q.home[2] * R * pull);
          q.m.scale.setScalar(Math.max(0.001, R * q.sz * grow * Math.pow(shrink, 0.8) * (1 + 0.06 * Math.sin(d * 19 + q.ph * 6)))); }
        else { const v = Math.max(0, (u - 0.15) / 0.85), sd = q.home[0], s = Math.sin(PI * Math.min(1, v * 1.3));
          q.m.position.set(sd * R * (0.7 + 1.6 * v), R * (0.55 + 1.3 * v), R * 0.15 + 0.05 * Math.sin(v * 7));
          q.m.scale.set(Math.max(0.001, R * q.sz * s * 1.5), Math.max(0.001, R * q.sz * s * 0.75), Math.max(0.001, R * q.sz * s)); q.m.rotation.z = sd * (0.4 + v * 1.5); } } };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a dust puff on the floor (pivot at the floor): small beige puffs that burst out at each time in o.at
  // that grow, rise and fade in o.dur (0.75) s (soft translucent puffs, o.n of them); o.r (0.35)
  poPuff(o) {
    const g = grp(), R = o.r ?? 0.35, D = o.dur ?? 0.75, NP = o.n ?? 10, P_ = [];
    // (story 104, review 2) o.ring: an opaque cartoon puff instead of the translucent cloud: inked white balls that burst out flat along the floor of the
    // pivot in a ring, swell, then shrink away to nothing (never transparent: a translucent cloud over a body reads as a ghost); o.rise (m) how high they lift
    if (o.ring) {
      for (let i = 0; i < NP; i++) { const m = ink(new THREE.Mesh(new THREE.IcosahedronGeometry(0.05, 1), L(i % 2 ? '#FFFFFF' : '#F1ECE0', { emissive: '#5A564E' })), 0.1); m.castShadow = m.receiveShadow = false; g.add(m); P_.push(m); }
      g.userData.update = t => { let d = -1; for (const t0 of o.at || []) if (t >= t0 && t < t0 + D) d = t - t0;
        P_.forEach((m, i) => { m.visible = d >= 0; if (d < 0) return; const u = d / D, a = i / NP * TAU + hsh(i) * 0.3, k = 1 - Math.pow(1 - Math.min(1, u * 1.6), 3), rr = R * (0.25 + 0.75 * k) * (0.85 + 0.3 * hsh(i * 2));
          const sz = Math.sin(PI * Math.min(1, u * 1.15)) * (0.75 + 0.5 * hsh(i * 5)); m.position.set(Math.cos(a) * rr, 0.035 + (o.rise ?? 0.05) * k * hsh(i * 7), Math.sin(a) * rr * (o.flat ?? 0.6));
          m.scale.setScalar(Math.max(0.01, (o.size ?? 1) * sz)); }); };
      g.userData.update(0); return g;
    }
    for (let i = 0; i < NP; i++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(0.05, 1), new THREE.MeshLambertMaterial({ color: i % 2 ? '#FBF8F0' : '#F0EADC', emissive: '#4A463E', transparent: true, opacity: 0.4, depthWrite: false })); m.castShadow = m.receiveShadow = false; g.add(m); P_.push(m); }
    g.userData.update = t => { let d = -1; for (const t0 of o.at || []) if (t >= t0 && t < t0 + D) d = t - t0;
      P_.forEach((m, i) => { m.visible = d >= 0; if (d < 0) return; const u = d / D, a = i / NP * TAU + hsh(i) * 0.6, k = smooth(Math.min(1, u * 1.7)), rr = R * k * (0.7 + 0.5 * hsh(i * 2));
        m.position.set(Math.cos(a) * rr, 0.03 + R * 0.6 * k * (0.3 + hsh(i * 7)), Math.sin(a) * rr * 0.6); m.scale.setScalar(Math.max(0.01, (1 + 3.2 * k) * (0.6 + 0.6 * hsh(i * 5)))); m.material.opacity = 0.42 * Math.pow(1 - u, 1.4); }); };
    g.userData.update(0); return g;
  },
};
