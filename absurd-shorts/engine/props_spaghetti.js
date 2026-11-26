// (cycle 59) « Le spaghetti » (story 112): to see if his pasta is cooked this man flicks one spaghetti at the kitchen tiles. It sticks; the neighbour
// cries masterpiece; critics, a museum, pasta art, a packet of noodles worth a flat. All the while the strand slides down the tiles, a little lower in
// every shot, and nobody looks at it. One night it falls: it was never cooked. The museum gives it back; he puts it back in the pot, still boiling.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time. Every name
// starts with `sg`. No word, no figure, no brand, no price, no logo anywhere (the two title cards are the only words); no flag, emblem or cross.
import * as THREE from 'three';
import { box, cyl, sphere, mat, addOutline } from './style.js';
import { grp, at, canvasPlane, buildProp } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
function kv(keys, t, def = 0) {
  if (keys == null) return def;
  if (typeof keys === 'number') return keys;
  if (!keys.length) return def;
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) { const [a, va] = keys[i], [b, vb] = keys[i + 1]; if (t < b) return va + (vb - va) * smooth((t - a) / Math.max(1e-4, b - a)); }
  return keys[keys.length - 1][1];
}
const YEL = '#F2B300', YEL_D = '#C88A00', DRY = '#F3E3A6', INK = '#1A1410';
const TILE = 0.2, BLUE = '#3C7BC4', GROUT = '#1C2533';

// ---------------------------------------------------------------- the strand
// the signature curve (metres, its top at the origin, in the plane of the tiles): rises from the left, tops out, swirls down to the right
const CURVE = [[-0.46, -0.34], [-0.36, -0.16], [-0.2, -0.03], [0, 0], [0.15, -0.05], [0.25, -0.17], [0.21, -0.3], [0.09, -0.31], [0.1, -0.19], [0.27, -0.13], [0.43, -0.22], [0.5, -0.4]];
// the drooping S (top at the origin) and its end, where the drop hangs
const SCURVE = [[-0.3, -0.06], [-0.14, -0.01], [0, 0], [0.13, -0.07], [0.15, -0.22], [0.03, -0.34], [-0.1, -0.45], [-0.09, -0.6], [0.03, -0.7], [0.07, -0.76]];
// lying on the floor (x, z): a loose squiggle
const FLOOR = [[-0.4, 0.12], [-0.25, 0.2], [-0.08, 0.14], [0.05, 0.22], [0.2, 0.3], [0.34, 0.22], [0.42, 0.3], [0.5, 0.26]];
function tube(pts3, r, color, ink = true) {
  const curve = new THREE.CatmullRomCurve3(pts3, false, 'centripetal'), N = Math.max(12, Math.ceil(curve.getLength() / 0.02));
  const g = grp(), m = new THREE.Mesh(new THREE.TubeGeometry(curve, N, r, 8, false), mat(color)); g.add(m);
  if (ink) g.add(new THREE.Mesh(new THREE.TubeGeometry(curve, N, r + 0.006, 8, false), new THREE.MeshBasicMaterial({ color: INK, side: THREE.BackSide })));
  for (const u of [0, 1]) { const p = curve.getPointAt(u), c = sphere(r, color, 1); c.position.copy(p); g.add(c); }
  return g;
}
// One fat spaghetti on the tiles (pivot: the reference grout line, on the face of the tiles, at the curve's top; faces +Z): a 3 cm opaque deep-yellow
// tube. o.drop [[t, metres below the reference line]]: it slides down; o.shape 'curve' | 'S' (the S carries an opaque drop under its end);
// o.fall [t0, t1, floorY, floorZ]: from t0 it slithers down, drops and lands flat on the floor floorY below the line, floorZ out from the wall (by t1)
export const SPAGHETTI_PROPS = {
  sgStrand(o) {
    const R = 0.015, g = grp(), SG = o.sag ?? 0;
    // (round 1) o.sag 0..1: the curve sags a little more at each callback (the far ends droop, the loops flatten), it does not only go down
    const shape = (o.shape === 'S' ? SCURVE : CURVE).map(([x, y]) => [x, y - SG * (0.22 * Math.pow(Math.abs(x) / 0.5, 1.3) + 0.12 * Math.max(0, -y) / 0.4)]);
    const base = shape.map(([x, y]) => new THREE.Vector3(x, y, R + 0.006));
    const body0 = grp(); g.add(body0); let body = tube(base, R, YEL); body0.add(body);
    let drip = null;
    if (o.shape === 'S') { const e = base[base.length - 1]; drip = grp(at(sphere(0.035, YEL, 1, { outline: 0.014 }), 0, 0, 0)); drip.children[0].scale.set(0.9, 1.35, 0.9); drip.position.set(e.x, e.y - 0.06, e.z + 0.01); g.add(drip); }
    // (round 1) o.splat t: it flies in as a clump from the lens side, lands at t with a squash and recoils
    const fly = o.splat != null ? grp(tube([new THREE.Vector3(-0.12, 0.03, 0), new THREE.Vector3(0, -0.02, 0.02), new THREE.Vector3(0.12, 0.04, 0)], 0.016, YEL)) : null; if (fly) g.add(fly);
    const F = o.fall; let lastU = -1;
    g.userData.update = t => {
      const d = kv(o.drop, t, 0);
      if (fly) { const T = o.splat, u = clamp01((t - (T - 0.22)) / 0.22); fly.visible = t >= T - 0.22 && t < T; fly.position.set(0.05, -0.12 + 0.12 * u, 1.6 * (1 - u)); fly.rotation.z = 4 * u; body0.visible = t >= T; if (drip) drip.visible = t >= T;
        const v = t - T; if (v >= 0) { const sq = v < 0.1 ? 1 : 0, ov = v >= 0.1 && v < 0.2 ? 1 : 0, osc = v >= 0.2 ? Math.exp(-6 * (v - 0.2)) * Math.sin((v - 0.2) * 24) : 0; body0.scale.set(1 + 0.5 * sq - 0.15 * ov - 0.08 * osc, 1 - 0.7 * sq + 0.25 * ov + 0.1 * osc, 1); } }   // (round 2) a flat impact (3 frames), an overshoot, a wobble
      if (!F) { g.position.y = -d; return; }
      const u = clamp01((t - F[0]) / Math.max(0.01, F[1] - F[0]));
      if (u <= 0) { g.position.y = -d; return; }
      g.position.y = 0; const q = Math.round(u * 40) / 40; if (q === lastU) return; lastU = q;
      // slither (first 45 %): down the wall to the floor line; then the drop and the flop: each point lerps to its place on the floor
      const fy = F[2], fz = F[3], slide = smooth(q / 0.45), fl = clamp01((q - 0.45) / 0.55), fe = fl * fl;
      const pts = base.map((p, i) => { const fp = FLOOR[Math.min(FLOOR.length - 1, Math.floor(i * FLOOR.length / base.length))];
        const wy = p.y - d - slide * (fy - 0.35 - d) * (0.6 + 0.4 * i / base.length), wz = p.z;
        return new THREE.Vector3(p.x + (fp[0] * 1.3 - p.x) * fe, wy + (-fy + R - wy) * fe, wz + (fp[1] * fz / 0.3 - wz) * fe); });
      body0.remove(body); body.traverse(n => n.geometry?.dispose()); body = tube(pts, R * 1.1, YEL); body0.add(body);
      if (drip) { const e = pts[pts.length - 1]; drip.position.set(e.x, Math.max(-fy + 0.03, e.y - 0.06), e.z); }
    };
    g.userData.update(0); return g;
  },
  // A strand hanging over a fork (attach to the hand: pivot at the grip): a fork pointing forward-up and the strand draped over its tines
  sgForkStrand(o) {
    const g = grp(), fk = grp(at(cyl(0.008, 0.008, 0.16, '#C8CCD2', 6, { pivot: 'bottom' }), 0, 0, 0));
    for (const x of [-0.015, -0.005, 0.005, 0.015]) fk.add(at(cyl(0.003, 0.003, 0.05, '#C8CCD2', 4, { pivot: 'bottom' }), x, 0.16, 0));
    fk.rotation.x = -0.5; g.add(fk);
    // (round 1) the strand is draped over the tines (fork frame) and hangs down both sides, a long end and a short one
    const st = o.strand !== false ? tube([new THREE.Vector3(-0.02, 0.1, 0.06), new THREE.Vector3(-0.012, 0.17, 0.03), new THREE.Vector3(0, 0.205, 0.0), new THREE.Vector3(0.012, 0.18, -0.03), new THREE.Vector3(0.02, 0.08, -0.08), new THREE.Vector3(0.03, -0.04, -0.1)], 0.015, YEL) : null;
    if (st) fk.add(st);
    g.userData.update = t => { if (st) st.visible = o.hide == null || t < o.hide; }; g.userData.update(0); return g;
  },
  // The dry strand (pivot at its middle, along X): pale and straight; at o.snap it breaks in two halves that jump apart (a crisp crack)
  sgDryStrand(o) {
    const L = o.len ?? 0.5, g = grp(), a = grp(), b = grp(); g.add(a, b);
    a.add(at(cyl(0.02, 0.02, L / 2, DRY, 8, { outline: 0.014 }), -L / 4, 0, 0, 0, 0, PI / 2)); b.add(at(cyl(0.02, 0.02, L / 2, DRY, 8, { outline: 0.014 }), L / 4, 0, 0, 0, 0, PI / 2));
    g.userData.update = t => { const s = o.snap == null ? 0 : clamp01((t - o.snap) / 0.15); a.position.set(-0.07 * s, -0.03 * s, 0); a.rotation.z = 0.5 * s; b.position.set(0.07 * s, -0.05 * s, 0); b.rotation.z = -0.6 * s; };
    g.userData.update(0); return g;
  },
  // The strand stuck on the lens (put it just in front of the camera, facing it): the signature curve as a flat decal, o.w wide, sliding down by
  // o.slide [[t, metres]]
  sgLensStrand(o) {
    const W = o.w ?? 0.3, H = W * 0.6, g = grp();
    const p = canvasPlane(W, H, (c, w, h) => { c.clearRect(0, 0, w, h); c.lineCap = 'round'; c.lineJoin = 'round'; const sx = x => w * (0.5 + x / 1.1), sy = y => h * (0.12 - y / 0.55);
      const path = () => { c.beginPath(); CURVE.forEach(([x, y], i) => { if (i === 0) c.moveTo(sx(x), sy(y)); else { const [px, py] = CURVE[i - 1]; c.quadraticCurveTo(sx(px), sy(py), (sx(px) + sx(x)) / 2, (sy(py) + sy(y)) / 2); } }); c.stroke(); };
      c.strokeStyle = INK; c.lineWidth = w * 0.06; path(); c.strokeStyle = YEL; c.lineWidth = w * 0.045; path(); c.strokeStyle = 'rgba(255,240,180,0.9)'; c.lineWidth = w * 0.012; path(); }, { res: 512, transparent: true });
    g.add(p); g.userData.update = t => { const y = kv(o.slide, t, 0), y2 = kv(o.slide, t + 0.05, 0), v = Math.abs(y2 - y) / 0.05; p.position.y = -y; p.scale.set(1 - Math.min(0.06, v * 0.6), 1 + Math.min(0.12, v * 1.2), 1); g.visible = o.at == null || t >= o.at; }; g.userData.update(0); return g;   // (round 1) it stretches a little as it slides
  },
  // ---------------------------------------------------------------- the tiles
  // A removable panel of mid-blue square tiles, 20 cm, dark grout (pivot at its bottom middle, faces +Z): o.cols (12) x o.rows (8)
  sgTiles(o) {
    const C = o.cols ?? 12, Rw = o.rows ?? 8, W = C * TILE, H = Rw * TILE, g = grp(at(box(W, H, 0.05, '#2A3442', { pivot: 'bottom' }), 0, 0, -0.025));
    const face = canvasPlane(W, H, (c, w, h) => { c.fillStyle = GROUT; c.fillRect(0, 0, w, h); const tw = w / C, th = h / Rw, gw = Math.max(3, tw * 0.07);
      for (let i = 0; i < C; i++) for (let j = 0; j < Rw; j++) { c.fillStyle = BLUE; c.fillRect(i * tw + gw / 2, j * th + gw / 2, tw - gw, th - gw); c.fillStyle = 'rgba(255,255,255,0.13)'; c.fillRect(i * tw + gw, j * th + gw, (tw - gw) * 0.45, (th - gw) * 0.2); }
      const ry = (Rw - (o.refRow ?? 6)) * th; c.fillStyle = GROUT; c.fillRect(0, ry - gw * 1.3, w, gw * 2.6); }, { res: 1024 });   // (round 1) the reference grout line, a little thicker
    face.position.set(0, H / 2, 0.006); g.add(face);
    if (o.strand) { const S = o.strand, st = SPAGHETTI_PROPS.sgStrand(S), holder = grp(st); holder.position.set(S.x ?? 0, (S.ref ?? 6) * TILE, 0.006); g.add(holder); g.userData.update = t => st.userData.update(t); }
    return g;
  },
  // A huge gilt frame (pivot at the bottom middle of its opening, faces +Z): o.w x o.h opening, o.b border; o.empty: a pale wall shows inside
  sgGilt(o) {
    const W = o.w ?? 2.6, H = o.h ?? 1.8, B = o.b ?? 0.28, g = grp(), G = '#C9982E', GL = '#E8C25A';
    for (const [x, y, w, h] of [[0, -B / 2, W + 2 * B, B], [0, H + B / 2, W + 2 * B, B], [-W / 2 - B / 2, H / 2, B, H], [W / 2 + B / 2, H / 2, B, H]]) {
      g.add(at(box(w, h, 0.12, G, { outline: 0.012 }), x, y, 0.06)); g.add(at(box(w * (w > h ? 0.98 : 0.5), h * (w > h ? 0.4 : 0.98), 0.02, GL), x, y, 0.13)); }
    for (const [x, y] of [[-W / 2 - B / 2, -B / 2], [W / 2 + B / 2, -B / 2], [-W / 2 - B / 2, H + B / 2], [W / 2 + B / 2, H + B / 2]]) g.add(at(sphere(B * 0.42, GL, 1, { outline: 0.012 }), x, y, 0.14));
    if (o.empty) g.add(at(box(W, H, 0.01, o.emptyColor || '#EEEAE0'), 0, H / 2, 0.005));
    return g;
  },
  // A small blank white label (pivot at its middle, faces +Z)
  sgLabel(o) { return grp(at(box(o.w ?? 0.16, o.h ?? 0.1, 0.008, '#FBFAF6', { outline: 0.004 }), 0, 0, 0.004)); },
  // A red rope on two brass posts (pivot at the floor middle, along X): o.len (2.4)
  sgRope(o) {
    const L = o.len ?? 2.4, g = grp(), B = '#C9A23A';
    for (const s of [-1, 1]) g.add(at(cyl(0.025, 0.03, 0.9, B, 8, { pivot: 'bottom', outline: 0.008 }), s * L / 2, 0, 0), at(cyl(0.16, 0.18, 0.04, B, 12, { pivot: 'bottom', outline: 0.008 }), s * L / 2, 0, 0), at(sphere(0.045, B, 1, { outline: 0.008 }), s * L / 2, 0.93, 0));
    const pts = []; for (let i = 0; i <= 12; i++) { const u = i / 12; pts.push(new THREE.Vector3(-L / 2 + u * L, 0.86 - 0.22 * Math.sin(PI * u), 0)); }
    g.add(tube(pts, 0.022, '#B8202A')); return g;
  },
  // ---------------------------------------------------------------- the kitchen
  // The kitchen (pivot at the floor middle; the back wall at z = o.back (-1.6), the tiles mounted on it are a separate prop): a terracotta and cream
  // checked floor (one textured box, no coplanar tiles), cream walls, a window in the back wall left of the tiles, a doorway in the right wall, a counter
  // and a hob under the tiles. o.open: no back wall (the kitchen opens onto the street: the street is the sgStreet prop); o.night: a dark-blue window
  sgKitchen(o) {
    const B = o.back ?? -1.6, g = grp(), WC = o.night ? '#3E5088' : '#F1E6CC';
    const fl = new THREE.Mesh(new THREE.BoxGeometry(7, 0.04, 8), mat('#FFFFFF')); const ft = canvasPlane(1, 1, (c, w, h) => { const n = 14; for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) { c.fillStyle = (i + j) % 2 ? (o.night ? '#8A96B4' : '#F2E4C8') : (o.night ? '#4E5A80' : '#D98C5F'); c.fillRect(i * w / n, j * h / n, w / n + 1, h / n + 1); } }, { res: 512 }).material;
    fl.material = [mat('#D98C5F'), mat('#D98C5F'), ft, mat('#D98C5F'), mat('#D98C5F'), mat('#D98C5F')]; fl.position.set(0, -0.02, B + 4.0); fl.receiveShadow = true; g.add(fl);
    if (!o.open) {
      // back wall in pieces round the window opening (x 0.9..1.8, y 1.0..2.2) and the doorway (x 2.0..2.9, y 0..2.2)
      for (const [x0, x1, y0, y1] of [[-3.5, 2.0, 0, 1.0], [2.9, 3.5, 0, 1.0], [-3.5, 0.9, 1.0, 2.2], [1.8, 2.0, 1.0, 2.2], [2.9, 3.5, 1.0, 2.2], [-3.5, 3.5, 2.2, 3.1]]) g.add(at(box(x1 - x0, y1 - y0, 0.12, WC, { pivot: 'bottom' }), (x0 + x1) / 2, y0, B - 0.06));
      g.add(at(box(1.0, 0.08, 0.2, '#FFFFFF', { outline: 0.006 }), 1.35, 0.98, B), at(box(1.0, 0.06, 0.14, '#FFFFFF'), 1.35, 2.22, B), at(box(0.06, 1.24, 0.14, '#FFFFFF'), 0.87, 1.6, B), at(box(0.06, 1.24, 0.14, '#FFFFFF'), 1.83, 1.6, B));
      g.add(at(box(1.6, 1.6, 0.02, o.night ? '#1E2E5A' : '#BFE2F2', { emissive: o.night ? '#0E1630' : '#6A8CA0' }), 1.35, 1.6, B - 1.2));
      g.add(at(box(0.06, 2.24, 0.14, '#FFFFFF'), 1.97, 1.12, B), at(box(0.06, 2.24, 0.14, '#FFFFFF'), 2.93, 1.12, B), at(box(1.0, 0.06, 0.14, '#FFFFFF'), 2.45, 2.22, B));
      g.add(at(box(1.2, 2.4, 0.04, o.night ? '#3A3A48' : '#C8B898'), 2.45, 1.2, B - 0.7), at(box(0.04, 2.4, 0.7, o.night ? '#454556' : '#D4C6A8'), 1.95, 1.2, B - 0.35), at(box(0.04, 2.4, 0.7, o.night ? '#454556' : '#D4C6A8'), 2.95, 1.2, B - 0.35));
    }
    // left and right walls, a ceiling
    g.add(at(box(0.12, 3.1, 8, WC, { pivot: 'bottom' }), -3.5, 0, B + 4.0), at(box(0.12, 3.1, 8, WC, { pivot: 'bottom' }), 3.5, 0, B + 4.0), at(box(7.2, 0.08, o.open ? 6.5 : 8, o.night ? '#2A3866' : '#F6EEDC'), 0, 3.14, B + (o.open ? 4.75 : 4.0)));
    // the counter and the hob under the tiles
    g.add(at(box(2.6, 0.9, 0.6, '#7FB0A8', { pivot: 'bottom', outline: 0.008 }), 0.2, 0, B + 0.32), at(box(2.7, 0.05, 0.66, '#F4EEE0', { outline: 0.006 }), 0.2, 0.925, B + 0.35));
    g.add(at(box(0.62, 0.02, 0.5, '#26282C', { outline: 0.004 }), -0.3, 0.96, B + 0.36), at(cyl(0.12, 0.12, 0.012, '#4A4C52', 16), -0.3, 0.975, B + 0.36));
    for (const x of [-0.45, -0.15]) g.add(at(cyl(0.02, 0.02, 0.03, '#E8E4DA', 8), x, 0.45, B + 0.63, PI / 2));
    if (o.night) { const pool = new THREE.Mesh(new THREE.CircleGeometry(0.95, 28).rotateX(-PI / 2), new THREE.MeshBasicMaterial({ color: '#FFD98A', transparent: true, opacity: 0.24, depthWrite: false })); pool.position.set(o.poolX ?? 0.6, 0.008, B + 1.5); g.add(pool); }   // a warm pool under the lamp
    if (o.lamp !== false) g.add(at(cyl(0.012, 0.012, 0.6, '#3A3A3A', 4, { pivot: 'bottom' }), o.poolX ?? 0, 2.5, B + 1.5), at(cyl(0.05, 0.22, 0.18, o.night ? '#F6E7A8' : '#E8C25A', 12, { emissive: o.night ? '#F2D46A' : undefined }), o.poolX ?? 0, 2.45, B + 1.5));
    return g;
  },
  // A big pot of boiling water (pivot at its bottom middle): a steel pot, two handles, the water's surface heaving with bubbles, a few spaghetti
  // ends sticking out over the rim; o.water [[t, 0/1]] (on: bubbles)
  sgPot(o) {
    const g = grp(at(cyl(0.2, 0.18, 0.28, '#B8BEC6', 16, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(cyl(0.205, 0.205, 0.02, '#D4D8DE', 16), 0, 0.28, 0));
    for (const s of [-1, 1]) g.add(at(box(0.09, 0.03, 0.05, '#1E2024', { outline: 0.006 }), s * 0.25, 0.24, 0));
    const w = at(cyl(0.185, 0.185, 0.01, '#CFE6EE', 16), 0, 0.255, 0); g.add(w);
    const bub = []; for (let i = 0; i < 9; i++) { const b = sphere(0.022 + 0.012 * hsh(i), '#F4FAFC', 1); g.add(b); bub.push(b); }
    if (o.strands === true) for (let i = 0; i < 2; i++) { const a = 0.6 + 1.9 * i; g.add(tube([new THREE.Vector3(Math.cos(a) * 0.1, 0.25, Math.sin(a) * 0.1), new THREE.Vector3(Math.cos(a) * 0.19, 0.33, Math.sin(a) * 0.19), new THREE.Vector3(Math.cos(a) * 0.23, 0.26, Math.sin(a) * 0.23), new THREE.Vector3(Math.cos(a) * 0.235, 0.17, Math.sin(a) * 0.235)], 0.011, YEL)); }   // (round 1) two soft ends over the rim
    g.userData.update = t => { bub.forEach((b, i) => { const ph = (t * (1.6 + hsh(i + 3)) + hsh(i)) % 1, a = hsh(i + 7) * TAU, r = 0.15 * Math.sqrt(hsh(i + 11)); b.position.set(Math.cos(a) * r, 0.262 + 0.02 * Math.sin(ph * PI), Math.sin(a) * r); b.scale.setScalar(0.4 + 0.8 * Math.sin(ph * PI)); }); w.position.y = 0.255 + 0.004 * Math.sin(t * 17); };
    g.userData.update(0); return g;
  },
  // A red egg timer with a plain dial and no marks (pivot at its bottom): a red egg on a cream foot; its top half turns by o.turn [[t, rad]]
  sgTimer(o) {
    const g = grp(at(cyl(0.05, 0.06, 0.02, '#F4EEE0', 12, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0)), lo = sphere(0.06, '#D8262A', 1, { outline: 0.01 }); lo.scale.set(1, 0.9, 1); lo.position.y = 0.07; g.add(lo);
    const top = grp(), hi = sphere(0.058, '#E8383A', 1, { outline: 0.01 }); hi.scale.set(1, 1.1, 1); top.add(hi, at(box(0.02, 0.03, 0.02, '#F4EEE0', { outline: 0.004 }), 0, 0.065, 0), at(box(0.012, 0.03, 0.006, '#F4EEE0'), 0, 0.0, 0.058));
    top.position.y = 0.1; g.add(top); g.userData.update = t => { top.rotation.y = kv(o.turn, t, 0); }; g.userData.update(0); return g;
  },
  // ---------------------------------------------------------------- the street (the kitchen open onto it, the doorstep)
  // A street on a disc of ground (pivot at the middle; the road along X at z = o.roadZ): a 40 m disc of lawn (never the 9 km plane), a road, a
  // pavement, a row of pastel cottages behind a picket fence, trees; o.cottages [[x, z, colour, roof, door]]
  sgStreet(o) {
    const g = grp(), RZ = o.roadZ ?? 0;
    const disc = new THREE.Mesh(new THREE.CircleGeometry(40, 32).rotateX(-PI / 2), mat(o.lawn || '#8DBB5E')); disc.position.y = 0.0; disc.receiveShadow = true; g.add(disc);
    g.add(at(box(80, 0.02, 6, '#7E828C'), 0, 0.012, RZ), at(box(80, 0.12, 2.0, '#E6D7B8'), 0, 0.06, RZ - 4.0), at(box(80, 0.12, 2.0, '#E6D7B8'), 0, 0.06, RZ + 4.0));
    for (let x = -18; x <= 18; x += 2.4) g.add(at(box(1.0, 0.025, 0.14, '#F4F1E8'), x, 0.025, RZ));
    const cs = o.cottages || [[-7.5, RZ - 11, '#F4F2EC', '#C9473A', '#2F7F8C'], [1.0, RZ - 11, '#B8A6D9', '#6A3A30', '#B5302A'], [9.0, RZ - 11, '#E8A08A', '#3E4A5E', '#2F5E8C']];
    for (const [x, z, c, r, d] of cs) g.add(at(buildProp('cottage', { w: 6.4, d: 7, h: 2.7, rh: 1.6, color: c, roof: r, door: d }), x, 0, z));
    g.add(at(buildProp('fence', { length: 40, height: 0.9, color: '#F6F4EE', rail: '#F6F4EE' }), 0, 0, RZ - 6.0));
    for (let i = 0; i < 6; i++) g.add(at(buildProp('tree', { seed: i + 5 }), -16 + i * 6.5, 0, RZ - 17 - 2 * hsh(i)));
    return g;
  },
  // ---------------------------------------------------------------- the museum
  // A small white museum room (pivot at the floor middle; the back wall at z = o.back (-1.5)): a pale wooden floor, white walls, a skirting; no name,
  // no sign. o.night: deep-blue night (never black); o.morning: a warm cast
  sgMuseum(o) {
    const B = o.back ?? -1.5, N = !!o.night, g = grp(), W = N ? '#4A5E9A' : o.morning ? '#F6F0E4' : '#F4F3EF', F = N ? '#34446E' : '#D8C09A';
    const fl = box(12, 0.04, 8, F); fl.position.set(0, -0.02, B + 4.0); fl.receiveShadow = true; g.add(fl);
    g.add(at(box(12, 3.6, 0.12, W, { pivot: 'bottom' }), 0, 0, B - 0.06), at(box(12, 0.12, 0.03, N ? '#2E3C66' : '#CFC8BA'), 0, 0.06, B + 0.015));
    g.add(at(box(0.12, 3.6, 8, W, { pivot: 'bottom' }), -6, 0, B + 4.0), at(box(0.12, 3.6, 8, W, { pivot: 'bottom' }), 6, 0, B + 4.0));
    if (N) g.add(at(box(1.2, 1.6, 0.02, '#BCD2FA', { emissive: '#6A86C8' }), o.winX ?? -4.2, 1.9, B + 0.01), at(box(1.3, 0.06, 0.06, '#E8ECF4'), o.winX ?? -4.2, 1.1, B + 0.03));   // a pale window: the cap pops against it
    g.add(at(box(12.2, 0.08, 8, N ? '#3E5088' : '#F8F7F3'), 0, 3.64, B + 4.0));
    return g;
  },
  // A plain room (pivot at the floor middle, back wall at z o.back (-1.6)): a floor, a back wall and a left wall in o.wall, o.floor; nothing on them
  sgRoom(o) { const B = o.back ?? -1.6, W = o.wall || '#EDE6D6', g = grp(at(box(10, 0.04, 7, o.floor || '#C8A880'), 0, -0.02, B + 3.5), at(box(10, 3.4, 0.12, W, { pivot: 'bottom' }), 0, 0, B - 0.06), at(box(0.12, 3.4, 7, W, { pivot: 'bottom' }), -5, 0, B + 3.5));
    g.add(at(box(10, 0.1, 0.03, '#BFB5A0'), 0, 0.05, B + 0.015)); return g; },
  // The painter's attic (pivot at the floor middle, back wall at z o.back (-1.4)): plank floor, cream walls, a sloping ceiling with a bright skylight,
  // an open window in the back wall at x o.winX (1.4) with a blue sky behind
  sgStudio(o) { const B = o.back ?? -1.4, X = o.winX ?? 1.4, W = '#F0E4CC', g = grp(at(box(8, 0.04, 6, '#B48A5E'), 0, -0.02, B + 3));
    for (let i = 0; i < 12; i++) g.add(at(box(0.012, 0.005, 6, '#8A6440'), -4 + i * 0.66, 0.002, B + 3));
    for (const [x0, x1, y0, y1] of [[-4, X - 0.5, 0, 2.6], [X + 0.5, 4, 0, 2.6], [X - 0.5, X + 0.5, 0, 1.0], [X - 0.5, X + 0.5, 2.1, 2.6]]) g.add(at(box(x1 - x0, y1 - y0, 0.12, W, { pivot: 'bottom' }), (x0 + x1) / 2, y0, B - 0.06));
    g.add(at(box(1.1, 1.1, 0.02, '#A8D6F2', { emissive: '#5A8AB0' }), X, 1.55, B - 0.5), at(box(1.0, 0.05, 0.16, '#FFFFFF', { outline: 0.006 }), X, 1.0, B), at(box(0.05, 1.1, 0.16, '#FFFFFF'), X - 0.5, 1.55, B), at(box(0.05, 1.1, 0.16, '#FFFFFF'), X + 0.5, 1.55, B));
    const ceil = box(8, 0.06, 3.4, '#E8D8B8'); ceil.position.set(0, 3.05, B + 1.4); ceil.rotation.x = -0.45; g.add(ceil, at(box(1.2, 0.9, 0.02, '#FFF8E0', { emissive: '#E8DCA8' }), -0.8, 3.0, B + 1.35, -0.45 - PI / 2, 0, 0));
    g.add(at(box(0.12, 3.2, 6, W, { pivot: 'bottom' }), -4, 0, B + 3)); return g; },
  // A glass of water (attach to the hand: pivot at its bottom)
  sgGlass(o) { const g = grp(), gl = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.03, 0.11, 10, 1, true), new THREE.MeshBasicMaterial({ color: '#DDEEF4', transparent: true, opacity: 0.45, side: THREE.DoubleSide })); gl.position.y = 0.055; g.add(gl, at(cyl(0.032, 0.029, 0.07, '#BFDDEA', 10), 0, 0.036, 0)); return g; },
  // A painter's smock (attach to the torso: pivot at the collar; faces +Z): a loose pale-blue overall with a few paint dabs
  sgSmock(o) { const g = grp(at(box(0.5, 0.8, 0.34, '#BFD4E6', { outline: 0.01, taper: 1.15 }), 0, -0.4, 0.02)); [['#F2662A', -0.1, -0.3], ['#F2B300', 0.12, -0.5], ['#3C7BC4', 0.05, -0.2]].forEach(([c, x, y]) => g.add(at(sphere(0.03, c, 0), x, y, 0.19))); return g; },
  // A spoon (attach to the hand)
  sgSpoon(o) { return grp(at(box(0.012, 0.13, 0.006, '#C8CCD2'), 0, 0.06, 0), at(sphere(0.022, '#C8CCD2', 1), 0, 0.13, 0)); },
  // A plain wooden chair (pivot at the floor, faces +Z)
  sgChair(o) { const C = o.color || '#8A5A36', g = grp(at(box(0.46, 0.05, 0.44, C, { outline: 0.008 }), 0, 0.46, 0), at(box(0.46, 0.5, 0.05, C, { outline: 0.008 }), 0, 0.73, -0.2));
    for (const x of [-0.2, 0.2]) for (const z of [-0.19, 0.19]) g.add(at(box(0.04, 0.46, 0.04, C, { pivot: 'bottom' }), x, 0, z)); return g; },
  // The guard's cap (attach to the head: pivot at its band's bottom): a navy crown and a black peak, no badge; o.pop [t]: it jumps off and lands
  // o.land [x, y, z] (head-local offset) away
  sgCap(o) {
    const g = grp(), c = grp(at(box(0.3, 0.1, 0.3, '#22305A', { outline: 0.012, taper: 1.12 }), 0, 0.08, 0), at(box(0.26, 0.02, 0.15, '#14161A', { outline: 0.01 }), 0, 0.02, 0.19, 0.2, 0, 0)); g.add(c);
    g.userData.update = t => { const u = o.pop == null ? 0 : clamp01((t - o.pop) / 0.45); c.position.set(0.25 * u, 0.5 * Math.sin(PI * Math.min(u, 1)) + (o.land?.[1] ?? -0.4) * u * u, 0.1 * u); c.rotation.set(-1.2 * u, 0, 0.9 * u); };
    g.userData.update(0); return g;
  },
  // Tiny round glasses (attach to the head at the eyes; faces +Z)
  sgSpecs(o) { const g = grp(); for (const s of [-1, 1]) { const r = new THREE.Mesh(new THREE.TorusGeometry(0.032, 0.005, 4, 14), mat('#1A1A1A')); r.position.x = s * 0.055; g.add(r); } g.add(at(box(0.04, 0.006, 0.006, '#1A1A1A'), 0, 0, 0)); return g; },
  // Hair curlers (attach to the head: pivot at the crown): a dozen pink and blue rollers
  sgCurlers(o) { const g = grp(); for (let i = 0; i < 12; i++) { const a = (i % 6) / 6 * PI - PI / 2 + (i < 6 ? 0 : 0.25), row = i < 6 ? 0 : 1; g.add(at(cyl(0.028, 0.028, 0.09, i % 2 ? '#F28AB4' : '#8AB8F2', 8, { outline: 0.008 }), Math.sin(a) * 0.1, 0.02 - 0.07 * row, Math.cos(a) * 0.08 - 0.03 * row, 0, a, PI / 2)); } return g; },
  // A beret (attach to the head: pivot at its band)
  sgBeret(o) { const b = cyl(0.17, 0.15, 0.06, '#2A2A30', 14, { outline: 0.01 }); const g = grp(at(b, 0.02, 0.03, 0, 0, 0, 0.18), at(cyl(0.008, 0.008, 0.04, '#2A2A30', 4), 0.03, 0.08, 0)); return g; },
  // A plain phone (attach to the hand)
  sgPhone(o) { return grp(at(box(0.075, 0.15, 0.012, '#E8E4F0', { outline: 0.008 }), 0, 0.06, 0)); },
  // A camera flash at the edge of the frame (pivot at its middle; turn it to the camera): small white rays bursting at each time of o.at for 0.12 s
  sgFlash(o) {
    const g = grp(), s = canvasPlane(o.w ?? 0.35, o.w ?? 0.35, (c, w, h) => { c.clearRect(0, 0, w, h); c.strokeStyle = '#FFFFFF'; c.lineCap = 'round'; c.lineWidth = w * 0.04; for (let i = 0; i < 8; i++) { const a = i * TAU / 8; c.beginPath(); c.moveTo(w / 2 + Math.cos(a) * w * 0.12, h / 2 + Math.sin(a) * h * 0.12); c.lineTo(w / 2 + Math.cos(a) * w * 0.45, h / 2 + Math.sin(a) * h * 0.45); c.stroke(); } c.fillStyle = '#FFFFFF'; c.beginPath(); c.arc(w / 2, h / 2, w * 0.1, 0, TAU); c.fill(); }, { res: 128, transparent: true, emissive: 1 });
    g.add(s); g.userData.update = t => { let on = 0; for (const a of o.at || []) if (t >= a && t < a + 0.12) on = 1 - (t - a) / 0.12; s.visible = on > 0; s.scale.setScalar(0.6 + 0.6 * on); }; g.userData.update(0); return g;
  },
  // ---------------------------------------------------------------- the artworks
  // An easel with a canvas (pivot at the floor, faces +Z): o.w x o.h canvas, o.art 'blank' | 'splat' (a tomato-orange splat with five strands from
  // o.at)
  sgEasel(o) {
    const W = o.w ?? 0.9, H = o.h ?? 1.1, g = grp(), C = '#9A6A3E';
    g.add(at(box(0.05, 1.9, 0.05, C, { pivot: 'bottom', outline: 0.006 }), -0.35, 0, 0.05, -0.12, 0, 0.1), at(box(0.05, 1.9, 0.05, C, { pivot: 'bottom', outline: 0.006 }), 0.35, 0, 0.05, -0.12, 0, -0.1), at(box(0.05, 1.8, 0.05, C, { pivot: 'bottom', outline: 0.006 }), 0, 0, -0.35, 0.22, 0, 0));
    g.add(at(box(0.9, 0.05, 0.1, C, { outline: 0.006 }), 0, 0.72, 0.18));
    const cv = at(box(W, H, 0.04, '#FBFAF4', { outline: 0.008 }), 0, 0.75 + H / 2, 0.16, -0.1, 0, 0); g.add(cv);
    if (o.art === 'splat') { const sp = SPAGHETTI_PROPS.sgSauce({ at: o.at }); sp.position.set(0, 0.75 + H * 0.55, 0.19); sp.rotation.x = -0.1; g.add(sp); g.userData.update = sp.userData.update; }
    return g;
  },
  // A cartoon tomato splat (pivot at its middle, faces +Z): an opaque bright tomato-orange blob (no drips, no drops) with five fat strands hanging
  // from it; hidden until o.at, then it pops on with a squash
  sgSauce(o) {
    const g = grp(), sh = new THREE.Shape(); for (let i = 0; i <= 24; i++) { const a = i / 24 * TAU, r = 0.2 * (1 + 0.18 * Math.sin(a * 5) + 0.08 * Math.cos(a * 3)); const x = Math.cos(a) * r, y = Math.sin(a) * r * 0.85; if (i === 0) sh.moveTo(x, y); else sh.lineTo(x, y); }
    const blob = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: 0.02, bevelEnabled: true, bevelSize: 0.012, bevelThickness: 0.012, bevelSegments: 2 }), mat('#F2662A')); addOutline(blob, 0.015); g.add(blob);
    const sts = []; for (let i = 0; i < 5; i++) { const x = -0.14 + 0.07 * i, L = 0.18 + 0.12 * hsh(i), st = grp(tube([new THREE.Vector3(0, 0, 0), new THREE.Vector3(0.02, -L * 0.4, 0.005), new THREE.Vector3(-0.01, -L, 0.005)], 0.012, YEL)); st.position.set(x, -0.02, 0.045); g.add(st); sts.push(st); }
    g.userData.update = t => { const v = o.at == null ? 9 : t - o.at, u = clamp01(v / 0.12); g.visible = v >= 0; const sq = v < 0.12 ? 1 + 0.35 * (1 - u) : 1 + 0.08 * Math.exp(-8 * (v - 0.12)) * Math.sin((v - 0.12) * 24); blob.scale.set(u * sq, u * (2 - sq), 1); sts.forEach((st, i) => { st.scale.y = clamp01((v - 0.08 - 0.05 * i) / 0.45); st.visible = st.scale.y > 0.02; }); }; g.userData.update(0); return g;   // (round 1) it grows at the impact, squashes and wobbles; the strands run down after
  },
  // One short strand hanging from a nose (attach to the head: pivot at the nose tip): it slaps on at o.at and swings
  sgNoseStrand(o) { const g = grp(), s = tube([new THREE.Vector3(-0.07, 0.04, 0.0), new THREE.Vector3(0, 0, 0.02), new THREE.Vector3(0.03, -0.12, 0.03), new THREE.Vector3(-0.01, -0.26, 0.03)], 0.016, YEL); g.add(s);
    g.userData.update = t => { const u = o.at == null ? 1 : t - o.at; g.visible = u >= 0; g.rotation.z = u > 0 ? 0.35 * Math.exp(-4 * u) * Math.sin(u * 14) : 0; }; g.userData.update(0); return g; },
  // A fat paintbrush (attach to the hand: pivot at the grip): a short blue handle, a ferrule, a soft rounded tuft; flies off from o.throw along
  // o.path [x, y, z] (hand-local) and spins
  sgBrush(o) { const g = grp(), b = grp(at(cyl(0.02, 0.022, 0.2, '#3A7AC8', 8, { outline: 0.008 }), 0, 0.05, 0), at(cyl(0.026, 0.022, 0.05, '#C8CCD2', 8), 0, 0.17, 0), at(sphere(0.032, '#F2D9A0', 1, { outline: 0.008 }), 0, 0.22, 0)); b.children[2].scale.set(1, 1.4, 0.8); g.add(b);
    g.userData.update = t => { const u = o.throw == null ? 0 : clamp01((t - o.throw) / 0.5); const p = o.path || [0.6, 0.8, -1.5]; b.position.set(p[0] * u, p[1] * u + 0.4 * Math.sin(PI * u), p[2] * u); b.rotation.x = -6 * u; b.visible = u < 1; }; g.userData.update(0); return g; },
  // A colander full of cooked pasta (attach to the hand: pivot at the handle)
  sgColander(o) { const R = 0.19, g = grp(), bowl = new THREE.Mesh(new THREE.SphereGeometry(R, 16, 8, 0, TAU, PI / 2, PI / 2), mat('#9EA6B0', { side: THREE.DoubleSide })); addOutline(bowl, 0.012); g.add(bowl);
    for (let i = 0; i < 26; i++) { const a = (i % 13) / 13 * TAU + (i < 13 ? 0 : 0.24), el = i < 13 ? 0.45 : 0.9; const hole = sphere(0.014, '#2A2E34', 0); hole.position.set(Math.cos(a) * Math.cos(el) * R * 1.01, -Math.sin(el) * R * 1.01, Math.sin(a) * Math.cos(el) * R * 1.01); g.add(hole); }
    g.add(at(new THREE.Mesh(new THREE.TorusGeometry(R, 0.012, 5, 20), mat('#8A929C')), 0, 0, 0, PI / 2), at(box(0.1, 0.02, 0.04, '#8A929C', { outline: 0.006 }), R + 0.05, 0, 0), at(box(0.1, 0.02, 0.04, '#8A929C', { outline: 0.006 }), -R - 0.05, 0, 0));
    for (let i = 0; i < 6; i++) { const a = hsh(i) * TAU; g.add(tube([new THREE.Vector3(Math.cos(a) * 0.12, -0.03, Math.sin(a) * 0.12), new THREE.Vector3(Math.cos(a + 1) * 0.05, 0.02, Math.sin(a + 1) * 0.05), new THREE.Vector3(Math.cos(a + 2) * 0.13, -0.01, Math.sin(a + 2) * 0.13)], 0.011, YEL, false)); }
    return g; },   // (round 1) a perforated steel bowl with two handles, a heap of pasta in it
  // A handful of pasta flying (pivot at the start): o.at, o.to [x, y, z]; a few strands in a clump
  sgFling(o) { const g = grp(), c = grp(); for (let i = 0; i < 6; i++) { const a = i / 6 * TAU, L = 0.22; c.add(tube([new THREE.Vector3(-L * 0.5, 0.03 * Math.sin(a), 0.03 * Math.cos(a)), new THREE.Vector3(-L * 0.15, 0.05 + 0.02 * i, 0.02), new THREE.Vector3(L * 0.15, -0.03 - 0.01 * i, -0.02), new THREE.Vector3(L * 0.5, 0.04 * Math.cos(a), 0.03 * Math.sin(a))], 0.012, YEL)); } g.add(c);
    g.userData.update = t => { const u = o.at == null ? 0 : clamp01((t - o.at) / (o.dur ?? 0.3)); const p = o.to || [0, 0, -1]; c.position.set(p[0] * u, p[1] * u + 0.35 * Math.sin(PI * u), p[2] * u); c.visible = (o.at == null || t >= o.at) && u < 1; c.rotation.set(0.6 * Math.sin(u * 6), 0, 1.2 * Math.sin(u * 3)); c.scale.set(1 + 0.25 * Math.sin(u * 9), 1, 1); }; g.userData.update(0); return g; },   // (round 2) a soft handful of spaghetti, wriggling in flight
  // A cubist face of square raviolis (pivot at the canvas' bottom middle, faces +Z): a canvas, raviolis stacked into a face with one eye on its side;
  // o.slip [t]: the corner ravioli slips; o.fall [t0]: they all drop into a heap under the canvas
  sgRavioli(o) {
    const W = o.w ?? 1.2, H = o.h ?? 1.4, g = grp(at(box(W, H, 0.04, '#FBF6EA', { outline: 0.008 }), 0, H / 2, 0)), rv = [];
    // (round 2) a cubist face in angular planes, not a grid: each plane a block of raviolis turned its own way, offset from the next
    const planes = [[-0.08, 1.12, 0.28, 3, 1, 0.15], [-0.3, 0.8, -0.35, 2, 2, 0.15], [0.26, 0.66, 0.42, 2, 2, 0.15], [0.14, 0.92, 0.65, 1, 3, 0.1], [-0.06, 0.38, -0.5, 2, 1, 0.13], [0.06, 0.18, 0.15, 1, 1, 0.13]];
    const add1 = (x, y, rz, sz, k) => { const r = grp(at(box(sz, sz, 0.04, k % 3 ? '#EFCB78' : '#E4B85E', { outline: 0.008 }), 0, 0, 0), at(box(sz * 0.62, sz * 0.62, 0.012, '#F6DC98'), 0, 0, 0.022)); r.userData.p0 = [x, y, 0.04 + 0.012 * (k % 3)]; r.userData.rz = rz; g.add(r); rv.push(r); };
    let k = 0; for (const [cx, cy, rz, nx, ny, sz] of planes) for (let a = 0; a < nx; a++) for (let b = 0; b < ny; b++) { const lx = (a - (nx - 1) / 2) * sz * 1.05, ly = (b - (ny - 1) / 2) * sz * 1.05; add1(cx + lx * Math.cos(rz) - ly * Math.sin(rz), cy + lx * Math.sin(rz) + ly * Math.cos(rz), rz, sz, k++); }
    const eye = grp(at(sphere(0.065, '#FFFFFF', 1, { outline: 0.01 }), 0, 0, 0), at(sphere(0.032, '#1A1A1A', 0), 0, 0, 0.055)); eye.position.set(-0.3, 0.97, 0.09); g.add(eye);   // the eye seen from the front
    const side = grp(); const al = new THREE.Mesh(new THREE.CircleGeometry(0.075, 12, -PI / 2, PI), mat('#FFFFFF')); addOutline(al, 0.02); side.add(al, at(sphere(0.022, '#1A1A1A', 0), 0.05, 0, 0.01)); side.position.set(0.36, 1.0, 0.09); side.rotation.z = 0.3; g.add(side);   // the eye in profile
    g.add(at(box(0.26, 0.04, 0.03, '#C8402A', { outline: 0.006 }), -0.06, 0.38, 0.09, 0, 0, -0.5));
    g.userData.update = t => { rv.forEach((r, i) => { const [x, y, z] = r.userData.p0; let px = x, py = y, rz = r.userData.rz;
      if (o.slip != null && i >= rv.length - 3) { const u = clamp01((t - o.slip - 0.2 * (rv.length - 1 - i)) / 0.5); py -= (i === rv.length - 1 ? 0.3 : 0.15) * u; rz += 0.8 * u; }
      if (o.fall != null) { const u = clamp01((t - o.fall - 0.12 * hsh(i + 9)) / 0.5); const hx = (hsh(i + 1) - 0.5) * 0.7, hy = 0.05 * Math.floor(hsh(i + 2) * 3); px += (hx - px) * u * u; py += (hy - py) * u * u; rz += 2 * u * (hsh(i + 5) - 0.5); }
      r.position.set(px, py, z + (o.fall != null && t > o.fall ? 0.15 * clamp01((t - o.fall) / 0.5) : 0)); r.rotation.z = rz; });
      const fu = o.fall == null ? 0 : clamp01((t - o.fall) / 0.4); eye.position.y = 0.97 - 0.95 * fu * fu; side.position.y = 1.0 - 0.98 * fu * fu; };
    g.userData.update(0); return g;
  },
  // A pointillist landscape of coquillette dots (pivot at the canvas' bottom middle, faces +Z): green hills, a blue sky, a yellow sun, all in dots;
  // o.slide [t]: three dots slide down; o.fall [t]: the whole sheet of dots drops and breaks into a heap on the floor (o.floor metres below)
  sgCoquillettes(o) {
    const W = o.w ?? 1.3, H = o.h ?? 1.0, g = grp(at(box(W, H, 0.04, '#FBF6EA', { outline: 0.008 }), 0, H / 2, 0)), sheet = grp(); g.add(sheet);
    const geo = new THREE.TorusGeometry(0.018, 0.008, 4, 8, PI * 1.2), dots = [];
    for (let i = 0; i < 26; i++) for (let j = 0; j < 20; j++) { const x = -W / 2 + 0.03 + i * (W - 0.06) / 25, y = 0.03 + j * (H - 0.06) / 19, sx = 0.32, sy = 0.72, sun = Math.hypot((x / W) - sx + 0.5, (y / H) - sy) < 0.1;
      const hill = y < H * (0.35 + 0.1 * Math.sin(x * 4)); const col = sun ? '#F6C21A' : hill ? '#4E9A4A' : '#7FB8E8'; dots.push([x, y, col]); }
    const byCol = {}; dots.forEach(d => (byCol[d[2]] ||= []).push(d));
    for (const [col, list] of Object.entries(byCol)) { const im = new THREE.InstancedMesh(geo, mat(col), list.length); const m4 = new THREE.Matrix4();
      list.forEach(([x, y], k) => { m4.makeRotationZ(hsh(k) * TAU); m4.setPosition(x, y, 0.03); im.setMatrixAt(k, m4); }); sheet.add(im); }
    const sl = []; for (let i = 0; i < 3; i++) { const d = new THREE.Mesh(geo, mat('#F6C21A')); d.position.set(-0.25 + 0.05 * i, H * 0.72, 0.035); sheet.add(d); sl.push(d); }
    const heap = grp(); for (let i = 0; i < 40; i++) { const d = new THREE.Mesh(geo, mat(['#4E9A4A', '#7FB8E8', '#F6C21A'][i % 3])); d.position.set((hsh(i) - 0.5) * 0.6, 0.02 + 0.08 * hsh(i + 3) * (1 - Math.abs(hsh(i) - 0.5) * 2), 0.15 + 0.15 * hsh(i + 5)); d.rotation.set(hsh(i + 1) * 3, hsh(i + 2) * 3, 0); heap.add(d); }
    heap.position.y = -(o.floor ?? 0.6); g.add(heap);
    g.userData.update = t => { sl.forEach((d, i) => { const u = o.slide == null ? 0 : clamp01((t - o.slide - 0.15 * i) / 0.6); d.position.y = H * 0.72 - 0.45 * u * (1 + 0.3 * i); d.scale.setScalar(1.6); });
      const u = o.fall == null ? 0 : clamp01((t - o.fall) / 0.45); sheet.position.y = -((o.floor ?? 0.6) + H * 0.5) * u * u; sheet.position.z = 0.12 * u; sheet.visible = u < 0.98; heap.visible = u >= 0.98; };
    g.userData.update(0); return g;
  },
  // A tagliatelle drape on a canvas (pivot at the canvas' bottom middle, faces +Z): ribbons hanging in loops; o.fall [t]: it slides off the canvas
  // and drops in a heap (o.floor metres below)
  sgTagliatelle(o) {
    const W = o.w ?? 1.1, H = o.h ?? 1.3, g = grp(at(box(W, H, 0.04, '#FBF6EA', { outline: 0.008 }), 0, H / 2, 0)), d = grp(); g.add(d);
    for (let i = 0; i < 9; i++) { const x0 = -W / 2 + 0.12 + i * (W - 0.24) / 8, pts = []; for (let j = 0; j <= 10; j++) { const u = j / 10; pts.push(new THREE.Vector3(x0 + 0.06 * Math.sin(u * 7 + i), H - 0.1 - u * (H - 0.25) * (0.7 + 0.3 * hsh(i)), 0.05 + 0.02 * Math.sin(u * 5 + i))); } d.add(tube(pts, 0.016, i % 2 ? '#F0C24A' : '#E8B23A')); }
    const heap = grp(); for (let i = 0; i < 8; i++) { const pts = []; for (let j = 0; j <= 8; j++) { const a = j / 8 * TAU * 1.3 + i; pts.push(new THREE.Vector3(Math.cos(a) * (0.12 + 0.03 * i), 0.02 + 0.012 * j, 0.2 + Math.sin(a) * 0.1)); } heap.add(tube(pts, 0.016, '#F0C24A')); }
    heap.position.y = -(o.floor ?? 0.6); g.add(heap);
    g.userData.update = t => { const u = o.fall == null ? 0 : clamp01((t - o.fall) / 0.5); d.position.y = -((o.floor ?? 0.6) + H * 0.6) * u * u; d.position.z = 0.1 * u; d.visible = u < 0.98; heap.visible = u >= 0.98; };
    g.userData.update(0); return g;
  },
  // ---------------------------------------------------------------- objects
  // A plain pasta packet (attach to the hand: pivot at its bottom): a pale-blue box with a clear window showing yellow sticks; no brand, no word
  sgPacket(o) { const g = grp(at(box(0.11, 0.36, 0.035, '#7FA8D8', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(box(0.075, 0.24, 0.004, '#EAF4FA'), 0, 0.17, 0.019)); for (let i = 0; i < 7; i++) g.add(at(cyl(0.004, 0.004, 0.22, YEL, 4), -0.03 + 0.01 * i, 0.17, 0.022)); g.add(at(box(0.11, 0.04, 0.03, '#5E86B8'), 0, 0.37, 0)); return g; },   // (round 2) a long pouch with a clear window full of spaghetti, no word
  // A key ring (attach to the hand): the engine's keyRing
  sgKeys(o) { return buildProp('keyRing', {}); },
  // A small grey safe (pivot at its bottom, faces +Z), its door ajar, a packet inside
  sgSafe(o) { const g = grp(at(box(0.4, 0.34, 0.34, '#6A6E76', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(0.34, 0.28, 0.02, '#1E2024'), 0, 0.17, 0.161));
    const dr = grp(at(box(0.34, 0.28, 0.04, '#7A7E86', { outline: 0.008 }), 0.17, 0, 0), at(cyl(0.03, 0.03, 0.02, '#C8CCD2', 10), 0.24, 0, 0.03, PI / 2)); dr.position.set(-0.17, 0.17, 0.19); dr.rotation.y = -1.7; g.add(dr);
    const pk = SPAGHETTI_PROPS.sgPacket({}); pk.rotation.set(0, 0, PI / 2); pk.position.set(0.2, 0.09, 0.2); g.add(pk); return g; },   // (round 2) the door wide open, the packet lying in it, its end sticking out
  // A bowl of plain white rice (pivot at its bottom)
  sgRice(o) { const b = new THREE.Mesh(new THREE.SphereGeometry(0.08, 12, 6, 0, TAU, PI / 2, PI / 2), mat('#F4F2EC', { side: THREE.DoubleSide })); b.position.y = 0.08; addOutline(b, 0.012);
    const rice = sphere(0.075, '#FBFAF6', 1); rice.scale.set(1, 0.4, 1); rice.position.y = 0.085; return grp(b, rice); },
  // A dining table (pivot at the floor middle; o.len along X)
  sgTable(o) { const L = o.len ?? 1.6, g = grp(at(box(L, 0.05, 0.9, '#8A5A36', { outline: 0.008 }), 0, 0.74, 0)); for (const x of [-L / 2 + 0.08, L / 2 - 0.08]) for (const z of [-0.37, 0.37]) g.add(at(box(0.06, 0.72, 0.06, '#6A4226', { pivot: 'bottom' }), x, 0, z)); return g; },
  // A sideboard (pivot at the floor, faces +Z)
  sgSideboard(o) { return grp(at(box(1.4, 0.8, 0.45, '#9A6A44', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(box(1.44, 0.04, 0.48, '#7A4E2E'), 0, 0.82, 0)); },
  // A dining room (pivot at the floor middle, back wall at z o.back (-1.6)): a wooden floor, pale-green walls, a window with a dusk sky
  sgDining(o) { const B = o.back ?? -1.6, g = grp(at(box(8, 0.04, 6, '#B08A60'), 0, -0.02, B + 3), at(box(8, 3, 0.12, '#CFE0C8', { pivot: 'bottom' }), 0, 0, B - 0.06), at(box(0.12, 3, 6, '#CFE0C8', { pivot: 'bottom' }), -3.2, 0, B + 3));
    g.add(at(box(1.1, 0.9, 0.02, '#F4C98A', { emissive: '#8A5A2A' }), 1.6, 1.6, B + 0.01), at(box(1.2, 0.06, 0.08, '#FFFFFF'), 1.6, 1.13, B + 0.04)); return g; },
  // A clipboard with a blank form (attach to the hand: pivot at its middle, faces +Z)
  sgClipboard(o) { return grp(at(box(0.24, 0.32, 0.012, '#9A6A3E', { outline: 0.006 }), 0, 0, 0), at(box(0.2, 0.27, 0.004, '#FBFAF6'), 0, -0.01, 0.009), at(box(0.08, 0.025, 0.02, '#C8CCD2'), 0, 0.15, 0.012)); },
  // A blank tape measure (attach to the hand: pivot at the case; the tape runs out along +X): a yellow case, a plain cream tape with no tick and no
  // figure, a brass hook; o.len [[t, metres]]
  sgTape(o) { const g = grp(at(box(0.08, 0.08, 0.04, '#F2C230', { outline: 0.008 }), 0, 0, 0)), tp = box(1, 0.025, 0.004, '#F6EED2', { outline: 0.003 }), hk = box(0.008, 0.035, 0.012, '#C9A23A');
    tp.geometry.translate(0.5, 0, 0); tp.position.set(0.04, 0, 0); g.add(tp, hk);
    g.userData.update = t => { const L = Math.max(0.01, kv(o.len, t, 0.01)); tp.scale.x = L; hk.position.set(0.04 + L, 0, 0); }; g.userData.update(0); return g; },
  // A wooden rubber stamp (attach to the hand): a handle knob and a block; no ink, no text
  sgStamp(o) { return grp(at(sphere(0.035, '#8A5A36', 1, { outline: 0.008 }), 0, 0.09, 0), at(cyl(0.012, 0.012, 0.06, '#8A5A36', 6), 0, 0.05, 0), at(box(0.08, 0.025, 0.05, '#5A3A22', { outline: 0.006 }), 0, 0.012, 0)); },
  // Tweezers (attach to the hand: pivot at the grip, the tips along +Y): two thin steel blades, small
  sgTweezers(o) { return grp(at(box(0.012, 0.16, 0.008, '#2A2C30', { pivot: 'bottom', outline: 0.004 }), -0.01, 0, 0, 0, 0, 0.06), at(box(0.012, 0.16, 0.008, '#2A2C30', { pivot: 'bottom', outline: 0.004 }), 0.01, 0, 0, 0, 0, -0.06)); },   // (round 2) dark and big enough to read
  // A velvet-lined case (attach to the hand: pivot at its middle; the lid open): dark-blue shell, red velvet, the two dry halves inside
  sgCase(o) { const g = grp(at(box(0.6, 0.08, 0.24, '#1E2A4A', { outline: 0.01 }), 0, 0, 0), at(box(0.56, 0.012, 0.2, '#C8202A'), 0, 0.042, 0));
    const lid = grp(at(box(0.6, 0.24, 0.03, '#1E2A4A', { outline: 0.01 }), 0, 0.12, 0), at(box(0.56, 0.2, 0.01, '#C8202A'), 0, 0.12, 0.02)); lid.position.set(0, 0.04, -0.12); g.add(lid);
    for (const s of [-1, 1]) g.add(at(cyl(0.02, 0.02, 0.24, DRY, 8, { outline: 0.012 }), s * 0.13, 0.065, 0.0, 0, 0, PI / 2 + s * 0.05));
    g.userData.update = t => { lid.rotation.x = -1.6 * kv(o.open, t, 1); g.visible = o.hide == null || t < o.hide; }; g.userData.update(0); return g; },   // (round 2) bigger; the lid opens away from the lens: cream halves on red velvet
  // The two dry halves falling into the pot (pivot at the pot's rim): from o.at they drop in o.dur (0.25) and vanish into the water
  sgHalves(o) { const g = grp(), sp = grp(); for (let i = 0; i < 10; i++) { const d = sphere(0.018, '#F4FAFC', 1); d.userData.a = i / 10 * TAU; sp.add(d); } g.add(sp); const hs = [-1, 1].map(s => { const h = grp(at(cyl(0.02, 0.02, 0.26, DRY, 8, { outline: 0.012 }), 0, 0, 0, 0, 0, PI / 2)); h.userData.s = s; g.add(h); return h; });
    g.userData.update = t => { const u = o.at == null ? 0 : clamp01((t - o.at) / (o.dur ?? 0.35)); hs.forEach(h => { const s = h.userData.s, ud = Math.max(0, u - (s > 0 ? 0.12 : 0)) / 0.88; h.position.set(s * 0.06 * (1 - ud), (o.h ?? 0.3) * (1 - ud * ud) - 0.06 * ud, 0.02 * s); h.rotation.set(2.5 * ud * s, 0.4 * s, 1.4 * ud); h.visible = ud < 1; }); const sv = o.at == null ? -1 : (t - o.at - (o.dur ?? 0.35) * 0.85) / 0.35; sp.visible = sv > 0 && sv < 1; sp.children.forEach(d => { const a = d.userData.a; d.position.set(Math.cos(a) * 0.12 * sv, -0.05 + 0.2 * Math.sin(PI * Math.min(1, sv)), Math.sin(a) * 0.12 * sv); }); }; g.userData.update(0); return g; },   // (round 2) a splash as they go in   // (round 1) they tumble in, one after the other
};
