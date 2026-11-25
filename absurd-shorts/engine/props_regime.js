// « Le régime » (story 101, cycle 53): this man went on a diet and the State took it the political way: the president packed, the army swore
// allegiance to a broccoli, a curfew on dessert, the old regime's cheeses fled abroad, the heaviest minister was relieved of his duties, éclairs passed
// under coats, a clandestine raclette was raided; one evening a square of chocolate appeared (his wife's mitten), he cracked, the regime fell.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time. Every name
// starts with `rg` (props.js merges all the story tables into one: a plain name could override another story's). No word, no figure, no flag drawn.
import * as THREE from 'three';
import { box, cyl, sphere, mat, addOutline } from './style.js';
import { grp, at, canvasPlane, rod } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = x => { const u = clamp01(x), c = 1.70158; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const noShadow = m => { m.traverse(c => { c.castShadow = false; }); return m; };
// a value keyed in time: keys [[t, v], ...] (sorted), eased (smoothstep) between keys; a plain number is a constant
function kv(keys, t, def = 0) {
  if (keys == null) return def;
  if (typeof keys === 'number') return keys;
  if (!keys.length) return def;
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) { const [a, va] = keys[i], [b, vb] = keys[i + 1]; if (t < b) return va + (vb - va) * smooth((t - a) / Math.max(1e-4, b - a)); }
  return keys[keys.length - 1][1];
}
const popS = (t, t0, d = 0.22) => t < t0 ? 0 : outBack((t - t0) / d);
const wrap01 = x => ((x % 1) + 1) % 1;
// a dusk picture (canvas): an orange-to-rose sky, a row of dark-blue roofs with lit yellow windows (never a black night)
function paintDusk(c, W, H, seed = 1) {
  const g = c.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#E8794A'); g.addColorStop(0.45, '#F4A25A'); g.addColorStop(0.75, '#F7C27A'); g.addColorStop(1, '#F2D49A');
  c.fillStyle = g; c.fillRect(0, 0, W, H);
  c.fillStyle = 'rgba(255,236,190,0.9)'; c.beginPath(); c.arc(W * 0.7, H * 0.66, H * 0.07, 0, TAU); c.fill();   // a low sun
  let x = 0, i = 0; while (x < W) { const bw = W * (0.08 + 0.08 * hsh(seed + i)), bh = H * (0.16 + 0.14 * hsh(seed + i + 7)); c.fillStyle = i % 2 ? '#4A3A5E' : '#3E3354';
    c.fillRect(x, H - bh, bw, bh); c.beginPath(); c.moveTo(x - 2, H - bh); c.lineTo(x + bw / 2, H - bh - H * 0.05); c.lineTo(x + bw + 2, H - bh); c.fill();
    c.fillStyle = '#FFD878'; for (let r = 0; r < 3; r++) for (let q = 0; q < 2; q++) if (hsh(seed + i * 9 + r * 3 + q) > 0.35) c.fillRect(x + bw * (0.2 + 0.42 * q), H - bh + bh * (0.18 + 0.27 * r), bw * 0.2, bh * 0.13);
    x += bw; i++; }
}

export const REGIME_PROPS = {
  // A broccoli (pivot at the bottom of its stalk, or of its plinth): a pale fat stalk, three branches, a tight bumpy dome of florets; o.s its height
  // (1 = 1 m tall); o.plinth: a stone plinth under it (its height); o.topple [t0, t1, dir]: it tips over about the plinth's front edge (dir +1 toward
  // +Z) in slow motion and bounces once on the ground; o.ropes [[x, y, z], ...]: taut ropes from its head to those points (relative), slack once it goes
  rgBroccoli(o) {
    const s = o.s ?? 1, PH = o.plinth ?? 0, g = grp(), tip = grp(), b = grp(); g.add(tip); tip.add(b);
    if (PH) { g.add(at(box(1.15 * s, PH, 1.15 * s, '#B9B2A4', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(1.3 * s, 0.12, 1.3 * s, '#A39C8E', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(1.25 * s, 0.1, 1.25 * s, '#A39C8E', { pivot: 'bottom' }), 0, PH - 0.1, 0)); }
    b.position.y = PH; const ST = o.stalk || '#C9DE92', FL = o.floret || '#3E8A3A', FL2 = o.floret2 || '#2F7030';
    b.add(at(cyl(0.11 * s, 0.15 * s, 0.42 * s, ST, 10, { pivot: 'bottom', outline: 0.02 }), 0, 0, 0));
    for (const [a, tl] of [[0.3, 0.42], [2.4, 0.4], [4.4, 0.45]]) { const br = rod([0, 0.36 * s, 0], [Math.cos(a) * 0.17 * s, (0.36 + tl * 0.55) * s, Math.sin(a) * 0.17 * s], 0.055 * s, ST); b.add(br); }
    const dome = grp(); dome.position.y = 0.66 * s; b.add(dome);
    for (let i = 0; i < 46; i++) { const u = hsh(i) * TAU, v = Math.acos(1 - hsh(i + 50) * 1.05), r = (0.085 + 0.045 * hsh(i + 9)) * s;
      const m = sphere(r, i % 3 ? FL : FL2, 1, { outline: 0.015 }); m.position.set(Math.sin(v) * Math.cos(u) * 0.27 * s, Math.cos(v) * 0.2 * s, Math.sin(v) * Math.sin(u) * 0.27 * s); dome.add(m); }
    dome.add(at(sphere(0.26 * s, FL2, 1), 0, 0, 0));
    const ropes = (o.ropes || []).map(() => { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 1, 5), mat('#B89A6A')); g.add(m); return m; });
    const head = new THREE.Vector3(), up = new THREE.Vector3(0, 1, 0);
    g.userData.update = t => {
      let a = 0, lift = 0; const T = o.topple, dir = T ? (T[2] ?? 1) : 1;
      if (T) { const u = (t - T[0]) / (T[1] - T[0]); if (u > 0) { a = u < 1 ? (PI / 2) * u * u : PI / 2; if (u >= 1) { const w = t - T[1]; a = PI / 2 - 0.12 * Math.abs(Math.sin(w * 9)) * Math.exp(-4 * w); lift = 0; } } }
      tip.position.set(0, PH, dir * 0.6 * s); b.position.set(0, 0, -dir * 0.6 * s); tip.rotation.x = dir * a; tip.position.y = PH * (1 - smooth(a / (PI / 2))) + lift;
      b.position.y = 0;
      head.set(0, 0.7 * s, -dir * 0.6 * s).applyAxisAngle(new THREE.Vector3(1, 0, 0), dir * a).add(tip.position);
      ropes.forEach((m, i) => { const e = new THREE.Vector3(...o.ropes[i]); const slack = a > 0.35; m.visible = !slack; if (slack) return; const d = e.clone().sub(head); m.position.copy(head).addScaledVector(d, 0.5); m.scale.set(1, d.length(), 1); m.quaternion.setFromUnitVectors(up, d.normalize()); });
    };
    g.userData.update(-1); return g;
  },

  // A plate (pivot at its bottom, flat): o.food 'fries' (a heap of sticks) | 'broccoli' (one real-size broccoli lying on it) | 'cake' (a cream slice)
  // | 'crepe' (a folded crêpe) | none; o.r its radius
  rgPlate(o) {
    const r = o.r ?? 0.16, g = grp(at(cyl(r, r * 0.82, 0.025, '#F6F4EE', 18, { pivot: 'bottom', outline: 0.03 }), 0, 0, 0));
    if (o.food === 'fries') for (let i = 0; i < 16; i++) { const a = hsh(i) * TAU, rr = r * 0.5 * hsh(i + 3); g.add(at(box(0.018, 0.018, 0.11, '#F2C14E', { outline: 0.03 }), Math.cos(a) * rr, 0.035 + 0.02 * (i % 3), Math.sin(a) * rr, 0.2 * (hsh(i + 5) - 0.5), a, 0.3 * (hsh(i + 7) - 0.5))); }
    if (o.food === 'broccoli') { const b = REGIME_PROPS.rgBroccoli({ s: r * 1.15 }); b.rotation.z = PI / 2 - 0.25; b.position.set(r * 0.42, 0.06, 0); g.add(b); }
    if (o.food === 'cake') { const c = REGIME_PROPS.rgCake({ slice: true, s: r * 1.6 }); c.position.y = 0.025; g.add(c); }
    if (o.food === 'crepe') { const c = REGIME_PROPS.rgCrepe({ s: r * 2.2 }); c.position.y = 0.025; g.add(c); }
    return g;
  },
  // A cream cake (pivot at its bottom): whole (a round sponge, a thick cream top, piped rosettes, a strawberry) or o.slice (a wedge); o.s its width
  rgCake(o) {
    const s = o.s ?? 0.3, g = grp();
    if (o.slice) { const sh = new THREE.Shape(); sh.moveTo(0, 0); sh.lineTo(s * 0.5, -s * 0.18); sh.lineTo(s * 0.5, s * 0.18); sh.lineTo(0, 0);
      const lay = (h, y, c) => { const m = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: h, bevelEnabled: false }), mat(c)); m.rotation.x = -PI / 2; m.position.y = y; addOutline(m, 0.02); g.add(m); };
      lay(s * 0.14, 0, '#E8B66A'); lay(s * 0.05, s * 0.14, '#FFF6E6'); lay(s * 0.12, s * 0.19, '#E8B66A'); lay(s * 0.07, s * 0.31, '#FFFBF2');
      g.add(at(sphere(s * 0.06, '#E0413A', 1), s * 0.38, s * 0.42, 0)); return g; }
    g.add(at(cyl(s * 0.5, s * 0.5, s * 0.3, '#E8B66A', 18, { pivot: 'bottom', outline: 0.012 }), 0, 0, 0), at(cyl(s * 0.52, s * 0.52, s * 0.1, '#FFFBF2', 18, { pivot: 'bottom', outline: 0.012 }), 0, s * 0.3, 0));
    for (let i = 0; i < 8; i++) { const a = i / 8 * TAU; g.add(at(sphere(s * 0.06, '#FFFBF2', 1), Math.cos(a) * s * 0.4, s * 0.43, Math.sin(a) * s * 0.4)); }
    g.add(at(sphere(s * 0.08, '#E0413A', 1), 0, s * 0.45, 0)); return g;
  },
  // A folded crêpe (pivot at its bottom): a golden quarter-fold with brown freckles and a drip of chocolate; o.s its size
  rgCrepe(o) {
    const s = o.s ?? 0.25, sh = new THREE.Shape(); sh.moveTo(0, 0); sh.absarc(0, 0, s * 0.5, 0, PI / 2, false); sh.lineTo(0, 0);
    const m = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: s * 0.06, bevelEnabled: true, bevelSize: s * 0.02, bevelThickness: s * 0.02, bevelSegments: 2 }), mat('#E9B65C')); m.rotation.x = -PI / 2; addOutline(m, 0.02);
    const g = grp(m); for (let i = 0; i < 7; i++) g.add(at(sphere(s * 0.025, '#A8682A', 0), s * (0.08 + 0.3 * hsh(i)), s * 0.085, -s * (0.08 + 0.3 * hsh(i + 4))));
    g.add(at(box(s * 0.05, s * 0.02, s * 0.2, '#5A3420'), s * 0.3, s * 0.09, -s * 0.12, 0, 0.7, 0)); return g;
  },
  // A dessert fork with a bite on it (pivot at the handle end, tines toward +Z): o.bite a colour (none: bare)
  rgFork(o) {
    const g = grp(at(box(0.012, 0.006, 0.12, '#C9CED4', { outline: 0.04 }), 0, 0, 0.06));
    for (const x of [-0.009, 0, 0.009]) g.add(at(box(0.003, 0.004, 0.04, '#C9CED4'), x, 0, 0.14));
    if (o.bite) g.add(at(box(0.03, 0.025, 0.03, o.bite, { outline: 0.04 }), 0, 0.012, 0.15));
    return g;
  },

  // A plain room (pivot at the middle of its floor; back wall at z = -o.d/2, open toward +Z): floor, back and two side walls, a skirting board;
  // o.w / o.d / o.h, o.wall / o.floor colours; o.window { x, y, w, h, dusk }: a window in the back wall (a pale sky, or the dusk picture)
  rgRoom(o) {
    const W = o.w ?? 6, D = o.d ?? 5, H = o.h ?? 3, WC = o.wall || '#E9DCC8', g = grp(), bz = -D / 2;
    const fl = new THREE.Mesh(new THREE.PlaneGeometry(W, D), mat(o.floor || '#C79E72')); fl.rotation.x = -PI / 2; fl.position.y = 0.003; fl.receiveShadow = true; g.add(fl);
    g.add(at(box(W, H, 0.12, WC, { pivot: 'bottom' }), 0, 0, bz - 0.06), at(box(0.12, H, D, WC, { pivot: 'bottom' }), -W / 2, 0, 0), at(box(0.12, H, D, WC, { pivot: 'bottom' }), W / 2, 0, 0));
    g.add(at(box(W, 0.12, 0.03, o.trim || '#F4EEE2'), 0, 0.06, bz + 0.015));
    if (o.window) { const q = o.window, ww = q.w ?? 1.2, wh = q.h ?? 1.2, wx = q.x ?? 0, wy = q.y ?? 1.6;
      const pic = canvasPlane(ww, wh, (c, Wc, Hc) => { if (q.dusk) paintDusk(c, Wc, Hc, 3); else { c.fillStyle = '#BFE0F2'; c.fillRect(0, 0, Wc, Hc); } }, { res: 256, emissive: 0.9 }); pic.position.set(wx, wy, bz + 0.005); g.add(pic);
      for (const [dx, dy, bw, bh] of [[0, wh / 2, ww + 0.1, 0.08], [0, -wh / 2, ww + 0.2, 0.08], [-ww / 2, 0, 0.08, wh], [ww / 2, 0, 0.08, wh], [0, 0, 0.05, wh]]) g.add(at(box(bw, bh, 0.06, '#F4EEE2', { outline: 0.006 }), wx + dx, wy + dy, bz + 0.03)); }
    return g;
  },
  // A dusk backdrop (pivot at its bottom middle, faces +Z): a big emissive picture of the orange sky over roofs with lit windows; o.w / o.h
  rgDusk(o) { const w = o.w ?? 60, h = o.h ?? 18, p = canvasPlane(w, h, (c, W, H) => paintDusk(c, W, H, o.seed ?? 1), { res: 1024, emissive: 1 }); p.position.y = h / 2 + (o.y ?? -0.5); return noShadow(grp(p)); },

  // A plain red-and-white barrier on a country road (pivot at the floor under its middle, pole along X): two short grey posts, a striped pole at
  // 1.05 m; no booth, no sign; o.w its span; o.lift [[t, rad]]: it swings up about its left post
  rgBarrier(o) {
    const w = o.w ?? 4, g = grp(at(cyl(0.07, 0.08, 1.1, '#8A939B', 8, { pivot: 'bottom', outline: 0.02 }), -w / 2, 0, 0), at(cyl(0.07, 0.08, 1.0, '#8A939B', 8, { pivot: 'bottom', outline: 0.02 }), w / 2, 0, 0));
    const pv = grp(); pv.position.set(-w / 2, 1.05, 0); g.add(pv); const n = 10;
    for (let i = 0; i < n; i++) pv.add(at(box(w / n, 0.1, 0.1, i % 2 ? '#F4F1EA' : '#D8262E', { outline: 0.012 }), (i + 0.5) * w / n, 0, 0));
    g.userData.update = t => { pv.rotation.z = kv(o.lift, t, 0); };
    g.userData.update(-1); return g;
  },
  // A cheese wheel standing on its edge (pivot at the floor under it, rolls along +X): o.r its radius, o.soft: a white soft round cheese (camembert,
  // pale rind with a few dimples), else a yellow hard wheel with a darker rind band; o.roll [t0, t1, dist]: it rolls dist metres along +X, spinning;
  // o.flat: lying flat instead (carried)
  rgCheese(o) {
    const r = o.r ?? 0.35, th = o.th ?? (o.soft ? r * 0.45 : r * 0.55), g = grp(), w = grp(); g.add(w);
    const body = cyl(r, r, th, o.soft ? '#F6F1E2' : '#F0C24E', 22, { outline: 0.01 }); w.add(body);
    if (!o.soft) for (const sd of [-1, 1]) w.add(at(cyl(r * 1.005, r * 1.005, th * 0.12, '#C98E2E', 22), 0, sd * th * 0.44, 0));
    else for (let i = 0; i < 9; i++) w.add(at(sphere(r * 0.05, '#E2DAC4', 0), Math.cos(i * 2.4) * r * 0.6 * hsh(i), th * 0.5, Math.sin(i * 2.4) * r * 0.6 * hsh(i)));
    if (o.flat) { w.position.y = th / 2; } else { w.rotation.x = PI / 2; w.position.y = r; }
    g.userData.update = t => { if (!o.roll || o.flat) return; const [a, b, d] = o.roll, u = clamp01((t - a) / (b - a)), x = d * u; w.position.x = x; w.rotation.set(PI / 2, 0, 0); w.rotateOnWorldAxis(new THREE.Vector3(0, 0, 1), -x / r); w.position.y = r + 0.03 * Math.abs(Math.sin(x / r * 2)); };
    g.userData.update(-1); return g;
  },

  // A doctor's column scale (pivot at the floor, front +Z): a platform, a column, a beam at the top with a big sliding weight; o.jumpAt: the weight
  // jumps to the far end of the beam with an overshoot and a clunk (the beam tips and shakes); o.nudge [t, d]: it slides back by d (a hair)
  rgScale(o) {
    const g = grp(at(box(0.55, 0.09, 0.55, '#E4E6E2', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(0.45, 0.012, 0.45, '#3A3D44'), 0, 0.095, 0));
    g.add(at(cyl(0.04, 0.05, 1.45, '#E4E6E2', 10, { pivot: 'bottom', outline: 0.02 }), 0, 0.09, -0.24));
    const beam = grp(); beam.position.set(0, 1.55, -0.2); g.add(beam);
    beam.add(at(box(0.7, 0.05, 0.05, '#C9CED4', { outline: 0.02 }), 0.15, 0, 0), at(box(0.04, 0.12, 0.06, '#3A3D44'), 0.52, 0, 0));
    for (let i = 0; i < 8; i++) beam.add(at(box(0.006, 0.03, 0.052, '#5E656D'), -0.15 + i * 0.08, 0.03, 0));
    const wt = at(box(0.11, 0.1, 0.09, '#2A2C31', { outline: 0.03 }), -0.12, 0, 0); beam.add(wt);
    g.userData.update = t => { let x = -0.12, rz = 0;
      if (o.jumpAt != null && t >= o.jumpAt) { const u = t - o.jumpAt; x = -0.12 + 0.58 * outBack(u / 0.18); const j = u < 0.5 ? Math.exp(-7 * u) * Math.sin(u * 40) : 0; rz = 0.05 * j + (u < 0.15 ? -0.12 * Math.sin(u / 0.15 * PI) : 0); }
      if (o.nudge && t >= o.nudge[0]) x += -(o.nudge[1] ?? 0.02) * smooth((t - o.nudge[0]) / 0.15) + (o.nudge[2] ?? 0);
      wt.position.x = Math.min(0.44, x); beam.rotation.z = rz; };
    g.userData.update(-1); return g;
  },
  // A straight wooden bench (pivot at the floor in its middle, seat along X, back toward -Z); o.w its length
  rgBench(o) { const w = o.w ?? 3, g = grp(at(box(w, 0.07, 0.42, '#A9784A', { outline: 0.008 }), 0, 0.46, 0), at(box(w, 0.42, 0.06, '#9A6A3E', { outline: 0.008 }), 0, 0.72, -0.2));
    for (const x of [-w / 2 + 0.1, 0, w / 2 - 0.1]) g.add(at(box(0.07, 0.46, 0.38, '#7E5530', { pivot: 'bottom' }), x, 0, 0)); return g; },
  // A plain coloured board (pivot at its middle, faces +Z): bands of colour and a circle, no word, no emblem; o.w / o.h
  rgSign(o) { const w = o.w ?? 1.6, h = o.h ?? 0.9; return grp(at(box(w + 0.08, h + 0.08, 0.04, '#7A5A3C', { outline: 0.008 }), 0, 0, -0.02),
      canvasPlane(w, h, (c, W, H) => { c.fillStyle = o.bg || '#3E7A9E'; c.fillRect(0, 0, W, H); c.fillStyle = o.band || '#F2C94C'; c.fillRect(0, H * 0.72, W, H * 0.1); c.fillStyle = '#F4F1E8'; c.fillRect(0, H * 0.18, W, H * 0.06); c.fillRect(0, H * 0.5, W, H * 0.04); }, { res: 256 })); },
  // A wooden office chair with arms (pivot at the floor, seat facing +Z)
  rgChair(o) { const g = grp(at(box(0.55, 0.08, 0.52, '#7E5530', { outline: 0.01 }), 0, 0.46, 0), at(box(0.55, 0.62, 0.07, '#7E5530', { outline: 0.01 }), 0, 0.8, -0.24));
    for (const x of [-0.24, 0.24]) for (const z of [-0.22, 0.22]) g.add(at(box(0.05, 0.46, 0.05, '#6A4628', { pivot: 'bottom' }), x, 0, z));
    for (const x of [-0.3, 0.3]) g.add(at(box(0.06, 0.06, 0.5, '#6A4628', { outline: 0.01 }), x, 0.68, 0), at(box(0.05, 0.22, 0.05, '#6A4628'), x, 0.57, 0.2)); return g; },

  // The two front flaps of a trench coat (attach to the torso joint; pivot at the chest): beige flaps hinged at the sides that swing open toward the
  // camera at o.openAt, showing a lining full of rows of big glossy éclairs (brown top, cream line) and a few choux buns; o.takeAt: the éclair at
  // o.take [side, row] is gone (taken); o.w / o.h
  rgCoat(o) {
    const w = o.w ?? 0.5, h = o.h ?? 0.9, g = grp(), flaps = [];
    for (const sd of [-1, 1]) { const piv = grp(); piv.position.set(sd * w / 2, 0, 0.02); g.add(piv);
      const fl = grp(at(box(w / 2, h, 0.03, '#C8A87A', { outline: 0.012 }), -sd * w / 4, -h * 0.35, 0)); piv.add(fl);
      fl.add(at(box(w / 2 - 0.02, h - 0.04, 0.005, '#7A2E2E'), -sd * w / 4, -h * 0.35, -0.018));   // the lining (seen once open: it faces -Z when closed)
      const items = [];
      for (let r = 0; r < 4; r++) for (let q = 0; q < 2; q++) { const ec = grp(), x = -sd * (0.07 + 0.12 * q), y = -h * 0.03 - r * 0.16;
        if ((r + q) % 3 === 2) ec.add(at(sphere(0.045, '#D9A35C', 1, { outline: 0.03 }), 0, 0, 0), at(sphere(0.03, '#F4EEE2', 0), 0, 0.03, 0));   // a choux bun
        else { ec.add(at(cyl(0.028, 0.028, 0.15, '#D9A35C', 8, { outline: 0.03 }), 0, 0, 0, 0, 0, PI / 2), at(box(0.15, 0.018, 0.04, '#4A2A18', { outline: 0.03 }), 0, 0.022, 0), at(box(0.13, 0.008, 0.012, '#FFF6E6'), 0, 0.006, 0.026)); }
        ec.position.set(x, y, -0.035); fl.add(ec); items.push({ ec, r, q }); }
      flaps.push({ piv, sd, items }); }
    g.userData.update = t => { const u = o.openAt != null ? outBack((t - o.openAt) / 0.3) : 0;
      for (const { piv, sd, items } of flaps) { piv.rotation.y = sd * 2.6 * u;
        for (const it of items) it.ec.visible = !(o.takeAt != null && t >= o.takeAt && o.take && o.take[0] === sd && o.take[1] === it.r && it.q === 0); } };
    g.userData.update(-1); return g;
  },
  // One éclair (pivot at its middle, along X): a choux finger, a brown glaze top, a cream line
  rgEclair(o) { return grp(at(cyl(0.028, 0.028, 0.15, '#D9A35C', 8, { outline: 0.03 }), 0, 0, 0, 0, 0, PI / 2), at(box(0.15, 0.018, 0.04, '#4A2A18', { outline: 0.03 }), 0, 0.022, 0), at(box(0.13, 0.008, 0.012, '#FFF6E6'), 0, 0.006, 0.026)); },
  // A forearm in a sleeve ending in a knitted mitten (pivot at the mitten's tip, the arm runs back along -Z): o.color the sleeve, o.mitten its
  // colour, o.len the sleeve's length; o.path [[t, x, y, z], ...]: it slides along those points (relative), eased; o.holds: a prop name it carries
  rgSleeve(o) {
    const L = o.len ?? 0.7, k = grp(), g = grp(k);
    k.add(at(box(0.15, 0.12, L, o.color || '#5E8C7A', { outline: 0.01 }), 0, 0, -0.14 - L / 2), at(box(0.17, 0.14, 0.06, o.cuff || '#F2EDE4', { outline: 0.01 }), 0, 0, -0.14));
    k.add(at(box(0.13, 0.08, 0.16, o.mitten || '#C8322A', { outline: 0.02 }), 0, 0, -0.06), at(box(0.05, 0.06, 0.07, o.mitten || '#C8322A', { outline: 0.02 }), 0.07, 0, -0.06, 0, -0.5, 0));
    for (let i = 0; i < 3; i++) k.add(at(box(0.135, 0.005, 0.01, '#F4EEE2'), 0, 0.041, -0.12 + i * 0.04));   // a knit stripe
    if (o.holds) { const h = REGIME_PROPS[o.holds]?.({ ...(o.holdOpts || {}) }); if (h) { h.position.set(0, -0.06, 0.04); k.add(h); g.userData.held = h; } }
    g.userData.update = t => { if (g.userData.held) g.userData.held.visible = (o.holdFrom == null || t >= o.holdFrom) && (o.dropAt == null || t < o.dropAt);   // o.holdFrom / o.dropAt: when it holds its prop
      const P = o.path; if (!P || !P.length) return; let p = P[0]; for (let i = 0; i < P.length - 1; i++) { if (t >= P[i + 1][0]) { p = P[i + 1]; continue; } if (t >= P[i][0]) { const u = smooth((t - P[i][0]) / (P[i + 1][0] - P[i][0])); p = [t, ...[1, 2, 3].map(j => P[i][j] + (P[i + 1][j] - P[i][j]) * u)]; } break; }
      k.position.set(p[1], p[2], p[3]); };
    g.userData.update(-1); return g;
  },

  // A raclette machine (pivot at the table top, front +Z): a dark base, a half wheel of cheese under a glowing orange element, its melted face
  // dripping; little pans round it; it lights the cellar (pair it with darkPool on it)
  rgRaclette(o) {
    const g = grp(at(box(0.6, 0.06, 0.4, '#2A2C31', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(0.05, 0.38, 0.05, '#3A3D44', { pivot: 'bottom' }), -0.25, 0, -0.1));
    const ch = at(cyl(0.18, 0.18, 0.12, '#F0C24E', 20, { outline: 0.02 }), 0, 0.2, 0.0, 0, 0, PI / 2); ch.scale.set(1, 1, 1); g.add(ch);
    g.add(at(box(0.4, 0.04, 0.3, '#3A3D44', { outline: 0.01 }), -0.02, 0.42, -0.02), at(box(0.34, 0.02, 0.22, '#FF8A2A', { emissive: '#FF6A10', noGrain: true }), -0.02, 0.395, 0.0));   // the hot element
    const face = at(box(0.02, 0.3, 0.3, '#FFD86A', { emissive: '#B8820A' }), 0.065, 0.2, 0); g.add(face);
    const drops = [0, 1, 2, 3].map(i => { const m = new THREE.Mesh(new THREE.SphereGeometry(0.02, 6, 5), mat('#FFD86A', { emissive: '#B8820A' })); g.add(m); return m; });
    for (const [x, z] of [[-0.45, 0.25], [0.45, 0.25], [-0.45, -0.25], [0.45, -0.25]]) g.add(at(box(0.16, 0.02, 0.1, '#2A2C31', { outline: 0.02 }), x, 0.01, z));
    const glow = noShadow(at(new THREE.Mesh(new THREE.SphereGeometry(0.5, 12, 8), new THREE.MeshBasicMaterial({ color: '#FF9A3A', transparent: true, opacity: 0.12, depthWrite: false })), 0, 0.3, 0)); g.add(glow);
    g.userData.update = t => { drops.forEach((m, i) => { const u = wrap01(t * 1.1 + i / 4); m.position.set(0.08, 0.1 - 0.12 * u * u, -0.08 + i * 0.05); m.scale.set(1, 1 + 1.5 * u, 1); }); glow.material.opacity = 0.11 + 0.02 * Math.sin(t * 13); };
    g.userData.update(-1); return g;
  },
  // A door in a frame that bursts open (pivot at the floor in the middle of the doorway, front +Z): o.burstAt: it slams open with a swing, an
  // overshoot, a bounce and a puff of dust; behind it a bright doorway; o.color
  rgDoor(o) {
    const g = grp(at(box(1.1, 2.2, 0.04, o.light || '#FFE6B0', { emissive: o.light || '#FFE6B0', noGrain: true }), 0, 1.1, -0.06));
    for (const [x, y, w, h] of [[-0.55, 1.1, 0.1, 2.2], [0.55, 1.1, 0.1, 2.2], [0, 2.25, 1.2, 0.1]]) g.add(at(box(w, h, 0.12, '#6A4A30', { outline: 0.008 }), x, y, 0));
    const piv = grp(); piv.position.set(-0.5, 0, 0); g.add(piv); piv.add(at(box(1.0, 2.15, 0.06, o.color || '#8A6A45', { outline: 0.01 }), 0.5, 1.08, 0), at(sphere(0.04, '#D9A93A', 1), 0.9, 1.0, 0.05));
    const dust = [0, 1, 2, 3, 4, 5].map(() => { const m = noShadow(new THREE.Mesh(new THREE.SphereGeometry(0.1, 8, 6), new THREE.MeshLambertMaterial({ color: '#D9D2C4', transparent: true, opacity: 0.6, depthWrite: false }))); g.add(m); return m; });
    g.userData.update = t => { const b = o.burstAt != null && t >= o.burstAt ? t - o.burstAt : -1; piv.rotation.y = b < 0 ? 0 : -1.75 * (1 - Math.exp(-b * 8) * Math.cos(b * 15));
      dust.forEach((m, i) => { const du = b - 0.04 * i; m.visible = du > 0 && du < 0.8; if (!m.visible) return; const a = (i / 6 - 0.5) * 2.6; m.position.set(Math.sin(a) * (0.3 + 0.6 * du), 0.1 + 0.3 * du, 0.2 + Math.cos(a) * 0.5 * du); m.scale.setScalar(0.5 + 1.5 * du); m.material.opacity = 0.6 * (1 - du / 0.8); }); };
    g.userData.update(-1); return g;
  },

  // A giant weighbridge (pivot at the ground in the middle of its deck, front +Z): a steel deck carrying a whole block of houses (pastel walls, red
  // roofs, windows), a big round dial on a post beside it; o.swing [t0, t1, a0, a1]: the needle swings from a0 to a1 (radians, eased with an
  // overshoot); o.sink [t0, t1, d]: the deck sinks a little as it reads; o.w the deck width
  rgWeighbridge(o) {
    const w = o.w ?? 9, g = grp(at(box(w + 0.6, 0.3, 5.4, '#6E767E', { pivot: 'bottom', outline: 0.006 }), 0, -0.25, 0));
    const deck = grp(at(box(w, 0.25, 5, '#9AA3A8', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0)); g.add(deck);
    const cols = ['#F2D6A2', '#E8B9A0', '#CFE0C4', '#F4E2C8', '#D9C9E6'];
    for (let i = 0; i < 5; i++) { const x = -w / 2 + 0.9 + i * (w - 1.8) / 4, hh = 2.4 + 0.9 * hsh(i), hw = 1.6;
      deck.add(at(box(hw, hh, 2.4, cols[i], { pivot: 'bottom', outline: 0.006 }), x, 0.25, -0.6));
      const roof = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 1.3, 0.9, 4), mat('#B5452E')); roof.rotation.y = PI / 4; roof.scale.set(0.88, 1, 1.3); roof.position.set(x, 0.25 + hh + 0.45, -0.6); addOutline(roof, 0.01); deck.add(roof);
      for (let r = 0; r < 2; r++) for (let q = 0; q < 2; q++) deck.add(at(box(0.32, 0.36, 0.02, '#7FB6D6', { outline: 0.02 }), x - 0.38 + 0.76 * q, 0.25 + 0.7 + r * 0.9, 0.61));
      deck.add(at(box(0.36, 0.7, 0.02, '#6A4A30'), x, 0.25 + 0.35, 0.615)); }
    const dial = grp(); dial.position.set(w / 2 + 1.6, 0, 1.4); g.add(dial);
    dial.add(at(box(0.25, 2.6, 0.25, '#5E656D', { pivot: 'bottom' }), 0, 0, -0.2), at(cyl(1.25, 1.25, 0.2, '#3A3D44', 32, { outline: 0.008 }), 0, 3.6, 0, PI / 2, 0, 0), at(cyl(1.12, 1.12, 0.05, '#FBF8F0', 32), 0, 3.6, 0.11, PI / 2, 0, 0));
    for (let i = 0; i < 24; i++) { const a = i / 24 * TAU; dial.add(at(box(0.04, i % 6 ? 0.12 : 0.24, 0.02, '#1E2126'), Math.sin(a) * 1.0, 3.6 + Math.cos(a) * 1.0, 0.14, 0, 0, -a)); }
    const ndl = grp(at(box(0.07, 1.0, 0.03, '#D8262E', { outline: 0.03 }), 0, 0.42, 0)); ndl.position.set(0, 3.6, 0.17); dial.add(ndl); dial.add(at(sphere(0.09, '#1E2126', 1), 0, 3.6, 0.19));
    g.userData.update = t => { const S = o.swing; let a = S ? S[2] : 0; if (S && t >= S[0]) { const u = (t - S[0]) / (S[1] - S[0]); a = S[2] + (S[3] - S[2]) * outBack(u); }
      ndl.rotation.z = -a; const K = o.sink; deck.position.y = K ? -K[2] * smooth((t - K[0]) / (K[1] - K[0])) : 0; };
    g.userData.update(-1); return g;
  },

  // A big glossy chocolate square (pivot at its bottom middle, flat): a 2 x 2 grid of raised blocks with a white glint; o.s its width; o.snapAt: it
  // breaks in two (the halves part along X, tilt) with a puff of crumbs
  rgChoco(o) {
    const s = o.s ?? 0.12, g = grp(), halves = [];
    for (const sd of [-1, 1]) { const h = grp(); g.add(h); halves.push(h);
      h.add(at(box(s / 2 - 0.002, s * 0.12, s, '#4A2616', { pivot: 'bottom', outline: 0.03 }), sd * s / 4, 0, 0));
      for (const z of [-s / 4, s / 4]) h.add(at(box(s * 0.4, s * 0.06, s * 0.4, '#5A3020', { outline: 0.03 }), sd * s / 4, s * 0.12, z), at(box(s * 0.12, s * 0.005, s * 0.04, '#E8D2C0', { emissive: '#8A6A5A' }), sd * s / 4 - s * 0.08, s * 0.152, z - s * 0.1)); }
    const crumbs = [0, 1, 2, 3, 4, 5, 6, 7].map(() => { const m = at(box(s * 0.08, s * 0.06, s * 0.07, '#4A2616'), 0, 0, 0); g.add(m); return m; });
    g.userData.update = t => { const u = o.snapAt != null ? t - o.snapAt : -1, k = u > 0 ? smooth(u / 0.12) : 0;
      halves.forEach((h, i) => { const sd = i ? 1 : -1; h.position.set(sd * 0.06 * k, 0.04 * k, 0); h.rotation.z = -sd * 0.5 * k; });
      crumbs.forEach((m, i) => { const du = u - 0.01 * i; m.visible = du > 0 && du < 0.7; if (!m.visible) return; const a = i / 8 * TAU; m.position.set(Math.cos(a) * 0.4 * du, s * 0.15 + 0.9 * du - 2.2 * du * du, Math.sin(a) * 0.25 * du + 0.05); m.rotation.set(du * 9, du * 7, 0); }); };
    g.userData.update(-1); return g;
  },
  // A hanging lamp (pivot at the ceiling point, hangs down -Y): a cord, a wide enamel shade, a glowing bulb under it; o.len the cord
  rgLamp(o) { const L = o.len ?? 0.9, g = grp(at(cyl(0.008, 0.008, L, '#2A2C31', 4), 0, -L / 2, 0), at(cyl(0.06, 0.32, 0.22, o.color || '#2E5E58', 16, { outline: 0.02 }), 0, -L - 0.1, 0));
    g.add(at(sphere(0.07, '#FFF2C8', 1, { emissive: '#FFE08A' }), 0, -L - 0.2, 0)); return g; },
  // A wall calendar with no figure on it (pivot at its middle, faces +Z): a coloured header band, a grid of blank day boxes, the first column (Monday)
  // tinted; o.circleAt: a red ring is drawn round one Monday box (it grows in a stroke); o.w / o.h
  rgCalendar(o) {
    const w = o.w ?? 0.5, h = o.h ?? 0.62, g = grp(at(box(w + 0.02, h + 0.02, 0.012, '#3A3D44'), 0, 0, -0.008));
    g.add(canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FBF8F0'; c.fillRect(0, 0, W, H); c.fillStyle = o.band || '#3E7FB6'; c.fillRect(0, 0, W, H * 0.2);
      const cw = W / 7, ch = (H * 0.78) / 5; c.fillStyle = '#E4EEF6'; c.fillRect(0, H * 0.2, cw, H * 0.8); c.strokeStyle = '#9AA3A8'; c.lineWidth = 2;
      for (let r = 0; r < 5; r++) for (let q = 0; q < 7; q++) c.strokeRect(q * cw + 2, H * 0.21 + r * ch + 2, cw - 4, ch - 4);
      c.fillStyle = '#5E656D'; for (let r = 0; r < 5; r++) for (let q = 0; q < 7; q++) { c.beginPath(); c.arc(q * cw + cw * 0.3, H * 0.21 + r * ch + ch * 0.3, 3, 0, TAU); c.fill(); } }, { res: 256 }));
    const ring = new THREE.Mesh(new THREE.TorusGeometry(w / 7 * 0.6, 0.009, 5, 24, TAU), new THREE.MeshBasicMaterial({ color: '#D8262E' })); ring.position.set(-w / 2 + w / 14, h / 2 - h * 0.21 - (h * 0.78 / 5) * ((o.row ?? 2) + 0.5), 0.006); ring.scale.set(1, 0.8, 1); g.add(ring);
    g.userData.update = t => { const u = o.circleAt == null ? 1 : clamp01((t - o.circleAt) / 0.35); ring.visible = u > 0.01; ring.geometry.setDrawRange(0, Math.floor(ring.geometry.index.count * u / 6) * 6); };
    g.userData.update(-1); return g;
  },
  // A fat red marker pen (pivot at its tip, along +Y)
  rgMarker(o) { return grp(at(cyl(0.016, 0.016, 0.13, '#D8262E', 8, { pivot: 'bottom', outline: 0.04 }), 0, 0.012, 0), at(cyl(0.006, 0.012, 0.014, '#2A2C31', 6, { pivot: 'bottom' }), 0, 0, 0)); },

  // A bakery front (pivot at the floor in the middle, faces +Z): a cream facade, a striped awning, a window full of loaves, an open dark doorway
  // (x = o.doorX), no name; o.w
  rgBakery(o) {
    const w = o.w ?? 7, dx = o.doorX ?? 0, g = grp();
    for (const [x0, x1] of [[-w / 2, dx - 0.65], [dx + 0.65, w / 2]]) g.add(at(box(x1 - x0, 4.2, 0.3, '#F2E2C2', { pivot: 'bottom', outline: 0.005 }), (x0 + x1) / 2, 0, -0.15));
    g.add(at(box(1.3, 1.85, 0.3, '#F2E2C2', { pivot: 'bottom' }), dx, 2.35, -0.15), at(box(1.2, 2.3, 0.05, '#2A1E16'), dx, 1.15, -0.25));
    for (let i = 0; i < 12; i++) g.add(at(box(w / 12, 0.08, 0.9, i % 2 ? '#F4F1EA' : '#C8322A', { outline: 0.006 }), -w / 2 + (i + 0.5) * w / 12, 2.75, 0.35, -0.35, 0, 0));
    for (const sx of [-1, 1]) { const wx = dx + sx * 2.0; g.add(at(box(1.8, 1.3, 0.05, '#FFE9B8', { emissive: '#8A6A2A', noGrain: true }), wx, 1.4, 0.02), at(box(1.9, 0.08, 0.2, '#7A5A3C'), wx, 0.75, 0.08));
      for (let i = 0; i < 5; i++) g.add(at(cyl(0.05, 0.045, 0.6, '#D9A35C', 8, { outline: 0.02 }), wx - 0.6 + i * 0.3, 1.0 + 0.3 * (i % 2), 0.1, 0.3, 0, PI / 2 - 0.4)); }
    return g;
  },
  // Croissants thrown over a crowd (pivot at the thrower's hand): n of them fly out on arcs every o.every from o.from; o.dir their direction (x, z)
  rgCroissants(o) {
    const n = o.n ?? 8, g = grp(), D = o.dir || [0, 1], cs = [];
    for (let i = 0; i < n; i++) { const c = grp(); for (let j = 0; j < 5; j++) { const a = -0.9 + j * 0.45, r = j === 2 ? 0.05 : j % 4 === 0 ? 0.03 : 0.042; c.add(at(sphere(r, '#D9A35C', 1, { outline: 0.03 }), Math.sin(a) * 0.1, 0, -Math.cos(a) * 0.055)); } g.add(c); cs.push(c); }
    g.userData.update = t => { cs.forEach((c, i) => { const u = t - (o.from ?? 0) - i * (o.every ?? 0.15); c.visible = u > 0 && u < 1.2; if (!c.visible) return; const sp = (hsh(i) - 0.5) * 1.4;
      c.position.set((D[0] + sp) * 2.2 * u, 2.6 * u - 3.2 * u * u, (D[1] + sp * 0.3) * 2.2 * u); c.rotation.set(u * 8, u * 5, 0); }); };
    g.userData.update(-1); return g;
  },
  // A jacket button that pops (pivot where it sits): at o.popAt it shoots out on an arc to o.to (relative), lands and rolls on along o.roll (x, z)
  rgButton(o) {
    const b = at(cyl(0.035, 0.035, 0.012, '#2A2C31', 14, { outline: 0.04 }), 0, 0, 0, PI / 2, 0, 0), g = grp(b); for (const [x, y] of [[-0.01, 0.01], [0.01, 0.01], [-0.01, -0.01], [0.01, -0.01]]) b.add(at(cyl(0.004, 0.004, 0.014, '#8A939B', 4), x, 0, y));
    const to = o.to || [0.4, -1.2, 1.2], ro = o.roll || [0.5, 1.5];
    g.userData.update = t => { const u = o.popAt != null ? t - o.popAt : -1; if (u <= 0) { b.position.set(0, 0, 0); b.rotation.set(PI / 2, 0, 0); return; }
      if (u < 0.45) { const f = u / 0.45; b.position.set(to[0] * f, 0.5 * Math.sin(f * PI) * 0.8 + to[1] * f * f, to[2] * f); b.rotation.set(PI / 2 + u * 20, 0, u * 9); }
      else { const v = u - 0.45; b.position.set(to[0] + ro[0] * v, to[1] + 0.035, to[2] + ro[1] * v); b.rotation.set(0, Math.atan2(ro[0], ro[1]), -v * 30); } };
    g.userData.update(-1); return g;
  },
};
