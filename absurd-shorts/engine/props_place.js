// « La place » (story 85): this man had his parking space taken at the supermarket; the army confirmed the invasion; the navy imposed a blockade
// on the roundabout; ultimatum: ten minutes to surrender; the invader was in the cheese aisle; six planes bombed his car, and the two hundred
// spaces round it; the supermarket too, it was badly parked; the invader was put under witness protection; the space was retaken; three thousand
// soldiers paraded on it; the other countries called a summit; the summit lasted forty laps; the treaty declared the space a neutral zone; every
// country parked a tank in it; this man pays the war reparations; the blockade was never lifted; he parks in the neighbouring country.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere, addOutline, mat, rng } from './style.js';
import { grp, at, canvasPlane, buildProp, rod, label, inst } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = x => { const u = clamp01(x), c = 1.70158; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const easeIn = x => { const u = clamp01(x); return u * u; };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const basic = (c, o = {}) => new THREE.MeshBasicMaterial({ color: c, transparent: o.opacity != null, opacity: o.opacity ?? 1, depthWrite: o.opacity == null, side: o.side || THREE.FrontSide });
const noShadow = m => { m.traverse(c => { c.castShadow = false; }); return m; };
// a value keyed in time: keys [[t, v], ...] (sorted); linear between keys over `blend` seconds after each key (0: a step)
function keyAt(keys, t, def = 0, blend = 0.25) {
  if (!keys || !keys.length) return def;
  let v = def, prev = def, t0 = -1e9;
  for (const [kt, kv] of keys) { if (t >= kt) { prev = v; v = kv; t0 = kt; } else break; }
  if (blend <= 0) return v;
  const w = smooth((t - t0) / blend);
  return prev + (v - prev) * w;
}
// an invented flag drawn on a canvas: horizontal bands o.colors, an emblem ('star', 'disc', 'chevron' or none) in o.mark colour
function flagDraw(colors, emblem, markColor) {
  return (c, W, H) => {
    const n = colors.length; colors.forEach((col, i) => { c.fillStyle = col; c.fillRect(0, i * H / n, W, H / n + 1); });
    c.fillStyle = markColor || '#F4F1E8';
    if (emblem === 'star') { c.beginPath(); for (let i = 0; i < 10; i++) { const a = -PI / 2 + i * PI / 5, r = i % 2 ? H * 0.12 : H * 0.28; c.lineTo(W * 0.3 + r * Math.cos(a), H * 0.5 + r * Math.sin(a)); } c.closePath(); c.fill(); }
    else if (emblem === 'disc') { c.beginPath(); c.arc(W * 0.5, H * 0.5, H * 0.24, 0, TAU); c.fill(); }
    else if (emblem === 'chevron') { c.beginPath(); c.moveTo(0, 0); c.lineTo(W * 0.38, H / 2); c.lineTo(0, H); c.closePath(); c.fill(); }
    c.strokeStyle = 'rgba(0,0,0,0.25)'; c.lineWidth = W * 0.012; c.strokeRect(0, 0, W, H);
  };
}
// a waving flag of `segs` vertical strips (origin at its hoist edge, top corner at y 0, hanging down h), drawn by `draw`
function wavingFlag(w, h, draw, segs = 6) {
  const g = grp(), cv = document.createElement('canvas'); cv.width = 256; cv.height = Math.max(8, Math.round(256 * h / w)); draw(cv.getContext('2d'), cv.width, cv.height);
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
  const strips = []; let parent = g;
  for (let i = 0; i < segs; i++) {
    const geo = new THREE.PlaneGeometry(w / segs, h); geo.translate(w / segs / 2, -h / 2, 0);
    const uv = geo.attributes.uv; for (let j = 0; j < uv.count; j++) uv.setX(j, (i + uv.getX(j)) / segs);
    const m = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ map: tex, side: THREE.DoubleSide })); m.castShadow = true;
    const piv = grp(m); if (i > 0) piv.position.x = w / segs; parent.add(piv); strips.push(piv); parent = piv;
  }
  g.userData.wave = (t, amp = 0.28, ph = 0) => { strips.forEach((s, i) => { s.rotation.y = (i === 0 ? 0.1 : amp) * Math.sin(t * 5.2 - i * 0.9 + ph); }); };
  return g;
}

export const PLACE_PROPS = {
  // The car park (pivot at its centre, on the field): an asphalt slab o.w (60) x o.d (46), its top at o.y (0.06), a pale kerb round it, painted bays
  // in rows o.rows [[zc, x0, n, depth (5)], ...] (bays 2.5 m wide, side by side along +X from x0, centred on zc), lamp posts o.lamps [[x, z]], a
  // zebra crossing o.zebra [x, z, w]. The bays' outlines are white strips 0.1 m wide
  parkLot(o) {
    const W = o.w ?? 60, D = o.d ?? 46, Y = o.y ?? 0.06, g = grp(), bw = 2.5;
    g.add(at(box(W, Y, D, o.color || '#6E7178', { pivot: 'bottom' }), 0, 0, 0));
    for (const [x, z, w, d] of [[0, -D / 2, W + 0.4, 0.3], [0, D / 2, W + 0.4, 0.3], [-W / 2, 0, 0.3, D], [W / 2, 0, 0.3, D]]) g.add(at(box(w, Y + 0.1, d, '#C9C5BA', { pivot: 'bottom' }), x, 0, z));
    const lines = [], wm = mat('#F1F0E8', { noGrain: true });
    for (const [zc, x0, n, dep] of o.rows || []) {
      const dd = dep ?? 5;
      for (let i = 0; i <= n; i++) lines.push([x0 - bw / 2 + i * bw, Y + 0.006, zc, 0, 0, 0, 0.1, 0.012, dd]);
      lines.push([x0 - bw / 2 + n * bw / 2, Y + 0.006, zc - dd / 2, 0, 0, 0, n * bw, 0.012, 0.1]);
    }
    if (lines.length) g.add(inst(new THREE.BoxGeometry(1, 1, 1), wm, lines));
    if (o.zebra) { const [x, z, w] = o.zebra; for (let i = 0; i < 7; i++) g.add(at(box(w ?? 4, 0.012, 0.45, '', { material: wm }), x, Y + 0.006, z - 1.6 + i * 0.55)); }
    for (const [x, z] of o.lamps || []) g.add(at(cyl(0.08, 0.1, 7, '#9AA0A8', 6, { pivot: 'bottom' }), x, Y, z), at(box(0.9, 0.16, 0.36, '#7A8088'), x + 0.35, Y + 7.0, z), at(box(0.7, 0.04, 0.26, '#FFF6D2', { emissive: '#4A4430', noGrain: true }), x + 0.4, Y + 6.91, z));
    for (const [x, z, ry] of o.arrows || []) {
      const s = new THREE.Shape(); s.moveTo(-0.18, -1.0); s.lineTo(0.18, -1.0); s.lineTo(0.18, 0.2); s.lineTo(0.45, 0.2); s.lineTo(0, 1.0); s.lineTo(-0.45, 0.2); s.lineTo(-0.18, 0.2); s.closePath();
      const m = new THREE.Mesh(new THREE.ShapeGeometry(s), wm); m.rotation.set(-PI / 2, 0, ry || 0); m.position.set(x, Y + 0.008, z); g.add(m);
    }
    return g;
  },

  // A small hatchback (pivot at the floor under its middle, its nose +Z; 3.7 x 1.66 x 1.45 m): o.color, opaque pale windows, round wheels, head and
  // tail lights, amber indicators at the four corners. o.blink 'L' | 'R' | 'both' (its left is +X): those indicators flash (0.38 s on, 0.32 s off,
  // o.phase); o.flatAt (s): it is squashed flat in 0.1 s with a bounce and stays a pancake; o.flat: already flat; o.brake [t0, dur]: the nose dips
  // and rocks back; o.flag [c1, c2]: a small flag on a rod at the front right wing; o.open 'L' | 'R': that front side window is an open dark hole;
  // o.plate (text); o.hop [[t, h]]: little jumps; o.dark: an official black car with chrome trim
  bayCar(o) {
    const C = o.color || (o.dark ? '#1C1E22' : '#C9473A'), L = 3.7, Wd = 1.66, g = grp(), body = grp(); g.add(body);
    const GL = o.glass || (o.dark ? '#2C3440' : '#BFDCE8'), DK = '#2E3138';
    const sl = Math.atan2(0.26, 0.5);
    const clearM = o.clear ? new THREE.MeshLambertMaterial({ color: '#DCEFF5', transparent: true, opacity: 0.18, depthWrite: false }) : null;
    const pane = (w, h, d, open) => box(w, h, d, open ? '#141518' : GL, clearM && !open ? { material: clearM } : { noGrain: true });
    body.add(at(box(Wd, 0.56, L, C, { outline: 0.012 }), 0, 0.63, 0), at(box(Wd + 0.04, 0.14, L + 0.06, DK), 0, 0.4, 0));
    if (o.clear) { body.add(at(box(1.26, 0.06, 1.5, C, { outline: 0.008 }), 0, 1.42, -0.42)); for (const sx of [-1, 1]) for (const z of [0.42, -0.32, -1.08]) body.add(at(box(0.07, 0.5, 0.07, C), sx * 0.66, 1.16, z, z > 0 ? -sl * 0.8 : z < -1 ? sl * 0.8 : 0, 0, sx * 0.25)); body.add(at(box(1.3, 0.18, 0.4, '#3A3D44'), 0, 0.98, 0.42)); }
    else body.add(at(box(1.5, 0.5, 2.0, C, { outline: 0.01, taper: { x: 0.82, z: 0.74 } }), 0, 1.16, -0.32));
    body.add(at(pane(1.18, 0.4, 0.02), 0, 1.15, 0.555, -sl, 0, 0), at(box(1.14, 0.36, 0.02, GL, { noGrain: true }), 0, 1.15, -1.19, sl, 0, 0));
    for (const sx of [-1, 1]) {
      const sa = Math.atan2(0.135, 0.5);
      for (const [z, w] of [[0.05, 0.62], [-0.68, 0.62]]) {
        const open = o.open && ((o.open === 'L' && sx > 0) || (o.open === 'R' && sx < 0)) && z > 0;
        body.add(at(pane(0.02, 0.34, w, open && !o.clear), sx * 0.69, 1.15, z, 0, 0, sx * sa));
      }
    }
    if (o.dark) for (const sx of [-1, 1]) body.add(at(box(0.02, 0.04, L * 0.9, '#C9CED6', { noGrain: true }), sx * (Wd / 2 + 0.012), 0.8, 0));
    for (const x of [-0.78, 0.78]) for (const z of [-1.18, 1.18]) body.add(at(cyl(0.3, 0.3, 0.22, '#1B1B1E', 12), x, 0.3, z, 0, 0, PI / 2), at(cyl(0.14, 0.14, 0.02, '#C9CDD3', 8), x * 1.15, 0.3, z, 0, 0, PI / 2));
    for (const sx of [-1, 1]) body.add(at(box(0.36, 0.13, 0.04, '#FFF6CC', { emissive: '#3A3420', noGrain: true }), sx * 0.52, 0.74, L / 2 + 0.02), at(box(0.32, 0.12, 0.04, '#C8302A', { noGrain: true }), sx * 0.55, 0.76, -L / 2 - 0.02));
    body.add(at(box(0.7, 0.18, 0.03, '#2A2C31'), 0, 0.55, L / 2 + 0.02));
    body.add(at(label(o.plate || 'AB-123-CD', 0.52, 0.12, { bg: '#FFFFFF', fg: '#1B1B1E', wrap: false }), 0, 0.46, L / 2 + 0.05), at(label(o.plate || 'AB-123-CD', 0.52, 0.12, { bg: '#FFFFFF', fg: '#1B1B1E', wrap: false }), 0, 0.5, -L / 2 - 0.05, 0, PI, 0));
    // indicators: an on copy (bright, emissive) and an off copy, swapped
    const onM = mat('#FFB21E', { emissive: '#FF9A00', noGrain: true, unique: true }), offM = mat('#A8661E', { noGrain: true, unique: true }), ind = [];
    for (const sx of [-1, 1]) for (const [z, dz] of [[L / 2 + 0.025, 1], [-L / 2 - 0.025, -1]]) {
      const pos = [sx * 0.74, 0.76, z];
      const on = at(box(0.14, 0.1, 0.05, '', { material: onM }), ...pos), off = at(box(0.14, 0.1, 0.05, '', { material: offM }), ...pos);
      const side = at(box(0.03, 0.06, 0.16, '', { material: onM }), sx * (Wd / 2 + 0.02), 0.8, dz * 1.3), sideOff = at(box(0.03, 0.06, 0.16, '', { material: offM }), sx * (Wd / 2 + 0.02), 0.8, dz * 1.3);
      const glowS = new THREE.Sprite(new THREE.SpriteMaterial({ color: '#FFB030', transparent: true, opacity: 0.55, depthWrite: false })); glowS.scale.setScalar(0.42); glowS.position.set(pos[0], pos[1], pos[2] + dz * 0.04);
      body.add(on, off, side, sideOff, glowS); ind.push({ sx, on, off, side, sideOff, glowS });
    }
    if (o.flag) {
      const fl = wavingFlag(0.3, 0.2, flagDraw(o.flag, o.flagMark || null, o.flagMarkColor), 4); fl.position.set(-0.7, 1.27, L / 2 - 0.25); fl.rotation.y = PI / 2;
      body.add(at(cyl(0.008, 0.008, 0.4, '#C9CED6', 5, { pivot: 'bottom' }), -0.7, 0.9, L / 2 - 0.25), fl); g.userData.flag = fl;
    }
    const blinkSide = o.blink === 'both' ? 0 : o.blink === 'L' ? 1 : o.blink === 'R' ? -1 : null;
    g.userData.update = t => {
      const lit = blinkSide !== null && ((t + (o.phase ?? 0)) % 0.7 + 0.7) % 0.7 < 0.38;
      for (const d of ind) { const on = lit && (blinkSide === 0 || d.sx === blinkSide); d.on.visible = d.side.visible = d.glowS.visible = on; d.off.visible = d.sideOff.visible = !on; }
      let sy = 1, sxz = 1, pitch = 0, y = 0;
      const fa = o.flat ? -10 : o.flatAt;
      if (fa != null && t >= fa) { const u = (t - fa) / 0.1; sy = u >= 1 ? 0.2 + 0.05 * Math.exp(-(t - fa - 0.1) * 9) * Math.cos((t - fa - 0.1) * 40) : 1 - 0.8 * easeIn(u); sxz = 1 + 0.14 * clamp01(u); }
      if (o.brake) { const [b0, bd] = o.brake, u = (t - b0) / (bd ?? 0.5); if (u >= 0 && u < 1.6) pitch = 0.09 * Math.sin(Math.min(u, 1) * PI) * (u < 1 ? 1 : Math.exp(-(u - 1) * 6)) + (u >= 1 ? -0.025 * Math.sin((u - 1) * 14) * Math.exp(-(u - 1) * 4) : 0); }
      for (const [ht, hh] of o.hop || []) { const u = (t - ht) / 0.32; if (u >= 0 && u < 1) y = Math.max(y, hh * 4 * u * (1 - u)); }
      body.scale.set(sxz, sy, sxz); body.rotation.x = pitch; body.position.y = y;
      if (g.userData.flag) g.userData.flag.userData.wave(t, 0.4, (o.phase ?? 0) * 3);
    };
    g.userData.update(0); g.userData.seat = [0.36, 0.45, 0.05]; return g;
  },

  // Rows of cars squashed flat in their bays (pivot at the car park's centre): o.rows [[zc, x0, n, facing (1: nose +Z, -1: nose -Z)], ...] like
  // parkLot's, o.skip ['row:i', ...] bays left out (keep them for real props), o.y (0.06) the asphalt's top, o.seed; a pancake is a crumpled slab with
  // a flattened cabin bump and four wheels splayed flat; o.wisps: that many thin smoke wisps rise from random wrecks
  flatRows(o) {
    const Y = o.y ?? 0.06, r = rng(o.seed || 85), g = grp(), skip = new Set(o.skip || []), cols = o.colors || ['#C9473A', '#5E8FD0', '#F2C94C', '#7FB069', '#E8E4DA', '#3E4A5A', '#D98AA8', '#8C6BB8', '#E8833A', '#9AA0A8'];
    const slabs = [], bumps = [], wheels = [], slabC = [], bumpC = [], spots = [];
    (o.rows || []).forEach(([zc, x0, n, fc], ri) => { for (let i = 0; i < n; i++) {
      if (skip.has(`${ri}:${i}`)) continue;
      const x = x0 + i * 2.5 + (r() - 0.5) * 0.3, z = zc + (r() - 0.5) * 0.4, ry = (fc ?? 1) < 0 ? PI : 0, tw = (r() - 0.5) * 0.25, c = cols[Math.floor(r() * cols.length)];
      slabs.push([x, Y + 0.07, z, (r() - 0.5) * 0.06, ry + tw, (r() - 0.5) * 0.05, 1.95 + r() * 0.15, 0.14, 4.0 + r() * 0.2]); slabC.push(c);
      bumps.push([x + Math.sin(ry + tw) * -0.3, Y + 0.16, z + Math.cos(ry + tw) * -0.3, 0, ry + tw, (r() - 0.5) * 0.1, 1.5, 0.08, 1.9]); bumpC.push(c);
      for (const [dx, dz] of [[-1.05, -1.25], [1.05, -1.25], [-1.05, 1.25], [1.05, 1.25]]) { const a = ry + tw, wx = x + dx * Math.cos(a) + dz * Math.sin(a), wz = z - dx * Math.sin(a) + dz * Math.cos(a); wheels.push([wx, Y + 0.04, wz, 0, 0, 0, 1, 1, 1]); }
      spots.push([x, z]);
    } });
    if (slabs.length) {
      const sm = inst(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshLambertMaterial({ flatShading: true }), slabs, slabC);
      const bm = inst(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshLambertMaterial({ flatShading: true }), bumps, bumpC);
      const wm = inst(new THREE.CylinderGeometry(0.36, 0.36, 0.08, 10), new THREE.MeshLambertMaterial({ color: '#1B1B1E', flatShading: true }), wheels);
      g.add(sm, bm, wm);
    }
    const wisps = [];
    for (let i = 0; i < (o.wisps ?? 0) && spots.length; i++) { const [x, z] = spots[Math.floor(hsh(i + 3) * spots.length)]; const w = buildProp('softWisp', { n: 10, rise: 2.6, life: 2.2, s0: 0.25, s1: 0.9, drift: [0.4, 0.1], color: o.smokeColor || '#6E6A66', opacity: 0.55 }); w.position.set(x, Y + 0.25, z); g.add(w); wisps.push(w); }
    g.userData.update = t => { for (const w of wisps) w.userData.update?.(t); };
    return g;
  },

  // Rows of intact parked cars, instanced (pivot at the car park's centre): o.rows [[zc, x0, n, facing], ...] as flatRows, o.skip ['row:i'], o.y (0.06),
  // o.s (1.25) their size, o.seed; a body, bumpers, a pale glass cabin with a roof in the body colour, four wheels; for the background
  parkedRows(o) {
    const Y = o.y ?? 0.06, s = o.s ?? 1.25, r = rng(o.seed || 58), g = grp(), skip = new Set(o.skip || []), cols = o.colors || ['#C9473A', '#E8E4DA', '#F2C94C', '#7FB069', '#3E4A5A', '#D98AA8', '#8C6BB8', '#E8833A', '#9AA0A8', '#2E6B8C'];
    const bodies = [], bodyC = [], bumps = [], cabs = [], roofs = [], roofC = [], wheels = [];
    (o.rows || []).forEach(([zc, x0, n, fc], ri) => { for (let i = 0; i < n; i++) {
      if (skip.has(`${ri}:${i}`)) continue;
      const x = x0 + i * 2.5 + (r() - 0.5) * 0.2, z = zc + (r() - 0.5) * 0.3, a = ((fc ?? 1) < 0 ? PI : 0) + (r() - 0.5) * 0.06, c = cols[Math.floor(r() * cols.length)], ca = Math.cos(a), sa = Math.sin(a);
      const L = (lx, lz) => [x + (lx * ca + lz * sa) * s, z + (-lx * sa + lz * ca) * s];
      const q = (lx, y, lz, sx, sy, sz) => { const [wx, wz] = L(lx, lz); return [wx, Y + y * s, wz, 0, a, 0, sx * s, sy * s, sz * s]; };
      bodies.push(q(0, 0.63, 0, 1.66, 0.56, 3.7)); bodyC.push(c); bumps.push(q(0, 0.4, 0, 1.7, 0.14, 3.76));
      cabs.push(q(0, 1.15, -0.32, 1.42, 0.46, 1.86)); roofs.push(q(0, 1.4, -0.36, 1.26, 0.06, 1.5)); roofC.push(c);
      for (const [dx, dz] of [[-0.78, -1.18], [0.78, -1.18], [-0.78, 1.18], [0.78, 1.18]]) { const [wx, wz] = L(dx, dz); wheels.push([wx, Y + 0.3 * s, wz, 0, a, PI / 2, s, s, s]); }
    } });
    if (bodies.length) {
      const B = new THREE.BoxGeometry(1, 1, 1), M = c => new THREE.MeshLambertMaterial({ color: c, flatShading: true });
      g.add(inst(B, M('#FFFFFF'), bodies, bodyC), inst(B, M('#2E3138'), bumps), inst(B, M('#BFDCE8'), cabs), inst(B, M('#FFFFFF'), roofs, roofC), inst(new THREE.CylinderGeometry(0.3, 0.3, 0.22, 10), M('#1B1B1E'), wheels));
    }
    return g;
  },

  // The supermarket (pivot at the middle of its front wall, on the ground; the front faces +Z): o.w (28) x o.d (14) x o.h (6.5), cream walls, a red
  // band, a glass entrance with a canopy, a red roof sign o.sign ('SUPERMARCHÉ'), o.clock {x, base, flipAt}: a countdownClock on the roof.
  // o.foldAt (s): it folds flat like a cardboard box (the front falls in, the sides fold in, the roof drops, the sign tips over onto the pile, dust
  // bursts out); o.folded: already flat
  superStore(o) {
    const W = o.w ?? 28, D = o.d ?? 14, H = o.h ?? 6.5, g = grp(), CR = o.wall || '#EFE7D4', RED = '#C8322A';
    g.add(at(box(W, 0.06, D, '#B9B2A2', { pivot: 'bottom' }), 0, 0, -D / 2));
    const panel = (w, h, col, deco) => { const p = grp(at(box(w, h, 0.24, col, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(w + 0.02, 1.1, 0.26, RED, { pivot: 'bottom' }), 0, h - 1.1, 0), at(box(w + 0.02, 0.5, 0.26, '#8A857A', { pivot: 'bottom' }), 0, 0, 0)); if (deco) deco(p); return p; };
    let canopy = null; const front = grp(), fp = panel(W, H, CR, p => {
      p.add(at(box(5.2, 2.8, 0.06, '#9CC9DC', { pivot: 'bottom', noGrain: true }), 0, 0.02, 0.14), at(box(0.12, 2.8, 0.08, '#5A6470', { pivot: 'bottom' }), 0, 0.02, 0.17));
      for (const x of [-9, -5.2, 5.2, 9]) p.add(at(box(2.8, 1.8, 0.05, '#B5D7E4', { pivot: 'bottom', noGrain: true }), x, 1.2, 0.14));
      canopy = grp(at(box(7, 0.24, 2.4, '#D9D3C4', { outline: 0.006 }), 0, 3.25, 1.2), at(cyl(0.08, 0.08, 3.2, '#9AA0A8', 6, { pivot: 'bottom' }), -3.3, 0, 2.2), at(cyl(0.08, 0.08, 3.2, '#9AA0A8', 6, { pivot: 'bottom' }), 3.3, 0, 2.2)); p.add(canopy);
    });
    front.add(fp); g.add(front);
    const side = () => { const sp = panel(D, H, CR); sp.rotation.y = PI / 2; sp.position.set(0, 0, -D / 2); return grp(sp); };
    const left = side(), right = side(); left.position.set(-W / 2, 0, 0); right.position.set(W / 2, 0, 0);
    const back = grp(panel(W, H, CR)); back.position.set(0, 0, -D);
    g.add(left, right, back);
    const roof = grp(at(box(W + 0.3, 0.3, D + 0.3, '#A8A39A', { pivot: 'bottom', outline: 0.006 }), 0, 0, -D / 2)); roof.position.y = H; g.add(roof);
    const signP = grp(), sw = o.signW ?? 10.5;
    signP.add(at(box(sw, 1.8, 0.3, RED, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(label(o.sign || 'SUPERMARCHÉ', sw - 0.5, 1.4, { bg: RED, fg: '#FFFFFF', wrap: false }), 0, 0.9, 0.16));
    signP.add(at(box(0.2, 0.6, 0.2, '#6A6E76', { pivot: 'bottom' }), -sw * 0.35, -0.6, -0.2), at(box(0.2, 0.6, 0.2, '#6A6E76', { pivot: 'bottom' }), sw * 0.35, -0.6, -0.2));
    const signG = grp(signP); signP.position.set(0, 0.9, 0); signG.position.set(0, H, -0.4); g.add(signG);
    let clk = null; if (o.clock) { clk = buildProp('countdownClock', o.clock); clk.position.set(o.clock.x ?? -8, 0.6, -0.6); signG.add(clk); }
    const dust = []; if (o.foldAt != null) for (const [x, z, s] of [[-W * 0.3, 1, 3.2], [0, 1.5, 3.6], [W * 0.3, 1, 3.2], [-W / 2 - 1, -D / 2, 2.6], [W / 2 + 1, -D / 2, 2.6]]) { const d = buildProp('softDust', { at: o.foldAt + 0.32, n: 9, size: s, life: 1.6, rise: 2.5, spread: 5, color: '#E2DCCD', opacity: 0.85 }); d.position.set(x, 0.4, z); g.add(d); dust.push(d); }
    g.userData.update = t => {
      const f0 = o.folded ? -100 : o.foldAt; let a = 0, b = 0, c = 0, rf = 0, sg = 0;
      if (f0 != null) { a = easeIn((t - f0) / 0.34); b = easeIn((t - f0 - 0.05) / 0.36); c = easeIn((t - f0 - 0.1) / 0.36); rf = easeIn((t - f0) / 0.4); sg = clamp01((t - f0 - 0.38) / 0.3); }
      if (canopy) canopy.visible = a < 0.5; front.rotation.x = -PI / 2 * a; back.rotation.x = PI / 2 * c; left.rotation.z = -PI / 2 * b; right.rotation.z = PI / 2 * b;
      const bounce = rf >= 1 ? 0.12 * Math.exp(-(t - f0 - 0.4) * 7) * Math.abs(Math.sin((t - f0 - 0.4) * 16)) : 0;
      roof.position.y = H + (0.62 - H) * rf + bounce;
      signG.position.y = roof.position.y + 0.3; signG.position.z = -0.4 - 3.2 * sg; signP.rotation.x = -PI / 2 * outBack(sg) * 0.98;
      if (clk) clk.userData.update?.(t);
      for (const d of dust) d.userData.update?.(t);
    };
    g.userData.update(0); return g;
  },

  // A giant red countdown clock (pivot at the foot of its legs; faces +Z): a red box 3.4 x 1.4 with a black panel of glowing orange digits MM:SS
  // counting down from o.base seconds (600) at t = o.flipAt (before it: blank dashes, and it flips on with a pop); o.rate (1 s a second)
  countdownClock(o) {
    const g = grp(), Wc = o.w ?? 3.4, Hc = Wc * 0.42;
    g.add(at(box(0.16, 0.6, 0.16, '#5A5E66', { pivot: 'bottom' }), -Wc * 0.3, 0, 0), at(box(0.16, 0.6, 0.16, '#5A5E66', { pivot: 'bottom' }), Wc * 0.3, 0, 0));
    const face = grp(); face.position.y = 0.6; g.add(face);
    face.add(at(box(Wc, Hc, 0.4, '#C8322A', { pivot: 'bottom', outline: 0.012 }), 0, 0, 0));
    const cv = document.createElement('canvas'); cv.width = 512; cv.height = Math.round(512 * (Hc - 0.3) / (Wc - 0.3)); const cx = cv.getContext('2d');
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
    const scr = new THREE.Mesh(new THREE.PlaneGeometry(Wc - 0.3, Hc - 0.3), new THREE.MeshBasicMaterial({ map: tex })); scr.position.set(0, Hc / 2, 0.205); face.add(scr);
    let last = null;
    const draw = s => { cx.fillStyle = '#16120F'; cx.fillRect(0, 0, cv.width, cv.height); cx.fillStyle = '#FF8A1E'; cx.font = `bold ${Math.round(cv.height * 0.78)}px "Courier New", monospace`; cx.textAlign = 'center'; cx.textBaseline = 'middle'; cx.fillText(s, cv.width / 2, cv.height * 0.54); tex.needsUpdate = true; };
    g.userData.update = t => {
      const fl = o.flipAt ?? -1; let s;
      if (t < fl) s = '--:--'; else { const rem = Math.max(0, Math.ceil((o.base ?? 600) - (t - fl) * (o.rate ?? 1) - 1e-6)); s = `${String(Math.floor(rem / 60)).padStart(2, '0')}:${String(rem % 60).padStart(2, '0')}`; }
      if (s !== last) { draw(s); last = s; }
      const u = t - fl; face.scale.setScalar(u >= 0 && u < 0.25 ? 1 + 0.12 * Math.sin(u / 0.25 * PI) : 1);
    };
    g.userData.update(0); return g;
  },

  // The war-room map table (pivot at the floor under its middle; the long side along X): a dark wooden table 2.4 x 1.4, 0.92 high, with a printed
  // plan of the car park on top (rows of bays, the store, the roundabout), small toy cars in the bays and, at o.red [x, z] on the table top, the red
  // toy car; o.blue [x, z]: a blue toy car in the lane (his)
  warMap(o) {
    const Wt = 2.4, Dt = 1.4, Ht = 0.92, g = grp();
    g.add(at(box(Wt, 0.08, Dt, '#4A3526', { outline: 0.008 }), 0, Ht - 0.04, 0));
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(at(box(0.1, Ht - 0.08, 0.1, '#3A291E', { pivot: 'bottom' }), sx * (Wt / 2 - 0.12), 0, sz * (Dt / 2 - 0.12)));
    const map = canvasPlane(Wt - 0.12, Dt - 0.12, (c, W, H) => {
      c.fillStyle = '#7FAE6A'; c.fillRect(0, 0, W, H); c.fillStyle = '#80838A'; c.fillRect(W * 0.04, H * 0.18, W * 0.72, H * 0.78);
      c.fillStyle = '#E9DFC6'; c.fillRect(W * 0.12, H * 0.02, W * 0.56, H * 0.15); c.fillStyle = '#C8322A'; c.fillRect(W * 0.3, H * 0.04, W * 0.2, H * 0.03);
      c.strokeStyle = '#F2F1EA'; c.lineWidth = W * 0.003;
      for (const yy of [0.24, 0.48, 0.58, 0.82]) { const bh = H * 0.1; for (let i = 0; i <= 16; i++) { const x = W * (0.06 + i * 0.042); c.beginPath(); c.moveTo(x, H * yy); c.lineTo(x, H * yy + bh); c.stroke(); } }
      c.fillStyle = '#80838A'; c.beginPath(); c.arc(W * 0.88, H * 0.62, H * 0.2, 0, TAU); c.fill(); c.fillStyle = '#6FAE57'; c.beginPath(); c.arc(W * 0.88, H * 0.62, H * 0.1, 0, TAU); c.fill();
      c.fillStyle = '#80838A'; c.fillRect(W * 0.76, H * 0.56, W * 0.04, H * 0.12);
      c.strokeStyle = '#1E2A3A'; c.lineWidth = W * 0.004; c.setLineDash([W * 0.01, W * 0.008]); c.beginPath(); c.arc(W * 0.88, H * 0.62, H * 0.26, 0, TAU); c.stroke(); c.setLineDash([]);
    }, { res: 1024 });
    map.rotation.x = -PI / 2; map.position.set(0, Ht + 0.003, 0); g.add(map);
    const toy = (x, z, col, s = 1) => grp(at(box(0.07 * s, 0.035 * s, 0.13 * s, col, { pivot: 'bottom', outline: 0.004 }), 0, 0, 0), at(box(0.055 * s, 0.03 * s, 0.07 * s, col, { pivot: 'bottom' }), 0, 0.035 * s, -0.01 * s));
    const r = rng(o.seed || 8), cols = ['#5E8FD0', '#F2C94C', '#7FB069', '#E8E4DA', '#3E4A5A', '#D98AA8', '#8C6BB8', '#E8833A'];
    const mx = x => -Wt / 2 + 0.06 + x * (Wt - 0.12), mz = y => -Dt / 2 + 0.06 + y * (Dt - 0.12);
    for (const yy of [0.29, 0.53, 0.63, 0.87]) for (let i = 0; i < 16; i++) { if (r() < 0.12) continue; const tc = toy(0, 0, cols[Math.floor(r() * cols.length)]); tc.position.set(mx(0.081 + i * 0.042), Ht + 0.004, mz(yy)); tc.rotation.y = (r() - 0.5) * 0.15; g.add(tc); }
    if (o.red) { const rc = toy(0, 0, '#D8392B', 1.25); rc.position.set(o.red[0], Ht + 0.004, o.red[1]); g.add(rc); }
    if (o.blue) { const bc = toy(0, 0, '#5E8FD0', 1.25); bc.position.set(o.blue[0], Ht + 0.004, o.blue[1]); bc.rotation.y = PI / 2; g.add(bc); }
    return g;
  },

  // A pin with a little red flag (pivot at its point; it stands up +Y): o.s (1): 0.26 m tall, the flag 0.12 x 0.08
  flagPin(o) {
    const s = o.s ?? 1, g = grp(at(cyl(0.006 * s, 0.002 * s, 0.26 * s, '#C9CCD1', 6, { pivot: 'bottom' }), 0, 0, 0), at(sphere(0.016 * s, '#D8392B', 1), 0, 0.262 * s, 0));
    const f = wavingFlag(0.12 * s, 0.08 * s, flagDraw(['#D8392B']), 3); f.position.set(0.004 * s, 0.25 * s, 0); g.add(f);
    g.userData.update = t => f.userData.wave(t, 0.2); g.userData.update(0); return g;
  },

  // A grey warship (pivot at the floor under its middle; the bow +Z; 11 m long, 2.8 wide): a hull pointed at the bow with a dark red waterline, a
  // deck, a bridge with dark windows, a mast with a radar that turns, a funnel, a gun turret on the foredeck that turns to o.aim [[t, yaw rad], ...]
  // (0: straight ahead, positive: to its left), o.counter: a black board on the bridge front showing the lap count o.laps [[t, n], ...] (it pops on
  // each change)
  warship(o) {
    const g = grp(), G1 = '#8E979F', G2 = '#A9B1B8', G3 = '#6F777E';
    g.add(at(box(2.8, 1.5, 11, G1, { pivot: 'bottom', outline: 0.012, taper: { x: 0.14, z: 1 }, taperAxis: 'z' }), 0, 0.25, 0.4));
    g.add(at(box(2.62, 0.28, 10.6, '#8C2E2A', { pivot: 'bottom', taper: { x: 0.12, z: 1 }, taperAxis: 'z' }), 0, 0.0, 0.35));
    g.add(at(box(2.5, 0.08, 9.8, G2, { taper: { x: 0.12, z: 1 }, taperAxis: 'z' }), 0, 1.76, 0.2));
    const br = grp(); br.position.set(0, 1.8, -1.2); g.add(br);
    br.add(at(box(2.1, 1.3, 2.6, G2, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(1.7, 0.9, 1.8, G2, { pivot: 'bottom', outline: 0.01 }), 0, 1.3, 0.1), at(box(1.72, 0.32, 0.02, '#1E2630', { noGrain: true }), 0, 1.85, 1.01));
    br.add(at(cyl(0.07, 0.09, 2.6, G3, 6, { pivot: 'bottom' }), 0, 2.2, -0.2), at(box(1.2, 0.08, 0.08, G3), 0, 3.8, -0.2), at(box(0.06, 0.6, 0.06, G3), 0, 4.4, -0.2));
    const radar = grp(at(box(0.9, 0.22, 0.08, '#C9CED6', { outline: 0.006 }), 0, 0, 0)); radar.position.set(0, 4.8, -0.2); br.add(radar);
    g.add(at(box(1.0, 1.4, 1.3, G1, { pivot: 'bottom', outline: 0.01, taper: { x: 0.85, z: 0.8 } }), 0, 1.8, -3.4), at(box(1.02, 0.25, 1.32, '#2E3236'), 0, 3.05, -3.4));
    const tur = grp(); tur.position.set(0, 1.8, 2.4); g.add(tur);
    tur.add(at(box(1.2, 0.55, 1.4, G2, { pivot: 'bottom', outline: 0.01, taper: { x: 0.8, z: 0.8 } }), 0, 0, 0));
    const gun = grp(at(cyl(0.09, 0.11, 2.4, G3, 8, { outline: 0.01 }), 0, 0, 1.2, PI / 2, 0, 0)); gun.position.set(0, 0.32, 0.5); tur.add(gun);
    const aft = grp(at(box(0.9, 0.42, 1.0, G2, { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(cyl(0.06, 0.07, 1.4, G3, 6, { outline: 0.008 }), 0, 0.25, -0.75, PI / 2, 0, 0)); aft.position.set(0, 1.8, -4.6); g.add(aft);
    for (const sx of [-1, 1]) g.add(at(box(0.04, 0.32, 8.4, '#D9DDE2'), sx * 1.18, 1.98, 0.0));
    let ctr = null, cvx = null, ctex = null, cv = null, lastN = null;
    if (o.counter) {
      cv = document.createElement('canvas'); cv.width = 256; cv.height = 160; cvx = cv.getContext('2d'); ctex = new THREE.CanvasTexture(cv); ctex.colorSpace = THREE.SRGBColorSpace;
      ctr = grp(at(box(1.5, 0.95, 0.12, '#1B1B1E', { outline: 0.01 }), 0, 0, 0)); const sc = new THREE.Mesh(new THREE.PlaneGeometry(1.36, 0.82), new THREE.MeshBasicMaterial({ map: ctex })); sc.position.z = 0.065; ctr.add(sc);
      ctr.position.set(0, 2.72, 0.55); br.add(ctr, at(box(0.3, 0.1, 0.3, '#6F777E'), 0, 2.22, 0.55));
    }
    g.userData.update = t => {
      tur.rotation.y = keyAt(o.aim, t, 0, o.aimBlend ?? 0.3); radar.rotation.y = t * 2.4;
      if (ctr) {
        const n = Math.round(keyAt(o.laps, t, 0, 0));
        if (n !== lastN) { cvx.fillStyle = '#121212'; cvx.fillRect(0, 0, 256, 160); cvx.fillStyle = '#FFD23C'; cvx.font = 'bold 128px "Courier New", monospace'; cvx.textAlign = 'center'; cvx.textBaseline = 'middle'; cvx.fillText(String(n), 128, 86); ctex.needsUpdate = true; lastN = n; }
        let lt = -1; for (const [kt] of o.laps || []) if (t >= kt) lt = kt; const u = t - lt; ctr.scale.setScalar(lt >= 0 && u < 0.22 ? 1 + 0.18 * Math.sin(u / 0.22 * PI) : 1);
      }
    };
    g.userData.update(0); return g;
  },

  // The roundabout (pivot at its centre, on the field): an island of radius o.ri (6.5) with a kerb and grass, an asphalt ring out to o.ro (13), a
  // dashed lane line, exits (o.exits: their bearings in degrees, 0 = +Z, 90 = +X; default the four) 7 m wide and o.exitLen (24) long, a give-way
  // line at each, and a striped boom across each exit (o.booms: 'up', 'down' or a time: they slam down then). o.grass: tall grass round the booms and
  // the kerb (months later). o.cars [{color, a0 (deg), r, dark, flag, open}]: cars driving round anticlockwise seen from above at o.speed (deg/s, 18)
  // until o.stopAt
  ringRoad(o) {
    const Ri = o.ri ?? 6.5, Ro = o.ro ?? 13, Y = o.y ?? 0.06, g = grp(), wm = mat('#F1F0E8', { noGrain: true }), road = '#6E7178';
    const ring = new THREE.Mesh(new THREE.RingGeometry(Ri, Ro, 64), mat(road)); ring.rotation.x = -PI / 2; ring.position.y = Y + 0.002; ring.receiveShadow = true; g.add(ring, at(cyl(Ro, Ro, Y, road, 64, { open: true, pivot: 'bottom' }), 0, 0, 0));
    g.add(at(cyl(Ri, Ri, 0.2, '#C9C5BA', 48, { pivot: 'bottom' }), 0, 0, 0), at(cyl(Ri - 0.25, Ri - 0.25, 0.03, o.island || '#79B85E', 48, { pivot: 'bottom' }), 0, 0.2, 0));
    const ex = o.exits || [0, 90, 180, 270], EL = o.exitLen ?? 24, EW = 7;
    const dashes = []; const rm = (Ri + Ro) / 2; for (let i = 0; i < 40; i++) { const a = i / 40 * TAU; dashes.push([Math.sin(a) * rm, Y + 0.006, Math.cos(a) * rm, 0, a, 0, 0.12, 0.012, 1.0]); }
    for (const b of ex) {
      const a = b * PI / 180, ca = Math.cos(a), sa = Math.sin(a), d0 = Ro - 1.5;
      const rd = at(box(EW, Y, EL, road, { pivot: 'bottom' }), sa * (d0 + EL / 2), 0, ca * (d0 + EL / 2), 0, a, 0); rd.receiveShadow = true; g.add(rd);
      for (let i = 0; i < 12; i++) { const off = -EW / 2 + 0.3 + i * 0.58; dashes.push([sa * (Ro + 0.3) + ca * off, Y + 0.006, ca * (Ro + 0.3) - sa * off, 0, a + PI / 2, 0, 0.14, 0.012, 0.32]); }
      for (let i = 0; i < Math.floor(EL / 3); i++) { const d = Ro + 2 + i * 3; dashes.push([sa * d, Y + 0.006, ca * d, 0, a, 0, 0.12, 0.012, 1.5]); }
    }
    g.add(inst(new THREE.BoxGeometry(1, 1, 1), wm, dashes));
    const booms = [];
    if (o.booms !== 'none') for (const b of ex) {
      const a = b * PI / 180, ca = Math.cos(a), sa = Math.sin(a), d = Ro + 1.2, side = -EW / 2 - 0.4;
      const bt = typeof o.booms === 'number' ? o.booms : null, down = o.booms === 'down';
      const gate = buildProp('barrierGate', { length: EW, angle: down ? 0 : 80, open: bt != null ? [[bt, 0]] : [] });
      gate.position.set(sa * d + ca * side, 0, ca * d - sa * side); gate.rotation.y = a; g.add(gate); booms.push(gate);
      if (o.grass) { const gr = buildProp('tallGrass', { w: 3.2, d: 2.2, h: 1.1, count: 220, seed: Math.round(b) + 5, thin: 0.03 }); gr.position.set(sa * d + ca * side, 0, ca * d - sa * side); g.add(gr);
        const gr2 = buildProp('tallGrass', { w: 2.5, d: 1.6, h: 0.8, count: 140, seed: Math.round(b) + 9, thin: 0.03 }); gr2.position.set(sa * (d + 0.5) - ca * side, 0, ca * (d + 0.5) + sa * side); g.add(gr2); }
    }
    if (o.grass) for (let i = 0; i < 8; i++) { const a = i / 8 * TAU + 0.2, gr = buildProp('tallGrass', { w: 2.6, d: 1.0, h: 0.9, count: 120, seed: 40 + i, thin: 0.03 }); gr.position.set(Math.sin(a) * (Ri + 0.4), 0, Math.cos(a) * (Ri + 0.4)); gr.rotation.y = a + PI / 2; g.add(gr); }
    const cars = (o.cars || []).map(c => { const m = buildProp('bayCar', { color: c.color, dark: c.dark, flag: c.flag, open: c.open, blink: c.blink, plate: c.plate }); g.add(m); return { m, c }; });
    g.userData.update = t => {
      for (const b of booms) b.userData.update?.(t);
      const tt = o.stopAt != null ? Math.min(t, o.stopAt) : t;
      for (const { m, c } of cars) { const a = ((c.a0 ?? 0) + (o.speed ?? 18) * tt) * PI / 180, r = c.r ?? (Ri + Ro) / 2 + 1.2; m.position.set(Math.sin(a) * r, Y, Math.cos(a) * r); m.rotation.y = a + PI / 2; m.userData.update?.(t); }
    };
    g.userData.update(0); return g;
  },

  // A big plain wheel of cheese (pivot at its bottom centre): smooth pale rind, no holes, no label; o.r (0.22), o.h (0.13)
  plainCheese(o) {
    const R = o.r ?? 0.22, Hh = o.h ?? 0.13, g = grp(at(cyl(R, R, Hh, '#E8C26A', 18, { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(cyl(R * 0.97, R * 0.97, 0.006, '#F4DC98', 18), 0, Hh + 0.003, 0), at(cyl(R * 1.003, R * 1.003, Hh * 0.3, '#D3A548', 18), 0, Hh * 0.5, 0));
    g.userData.grip = [0, Hh / 2, 0]; return g;
  },

  // The cheese aisle's fridge shelf (pivot at the floor under its front middle; faces +Z): a white unit o.w (3) x 2.1 x 0.75 with three shelves
  // of plain cheese wheels and wedges (no labels, no holes), blue price strips and a blue header board 'FROMAGES'
  cheeseShelf(o) {
    const Ws = o.w ?? 3.0, g = grp(), r = rng(o.seed || 12);
    g.add(at(box(Ws, 2.1, 0.06, '#F2F2EE', { pivot: 'bottom' }), 0, 0, -0.72), at(box(0.06, 2.1, 0.75, '#E4E4E0', { pivot: 'bottom' }), -Ws / 2, 0, -0.37), at(box(0.06, 2.1, 0.75, '#E4E4E0', { pivot: 'bottom' }), Ws / 2, 0, -0.37));
    g.add(at(box(Ws, 0.3, 0.75, '#D9D9D4', { pivot: 'bottom' }), 0, 0, -0.37));
    const cheeseCols = ['#E8C26A', '#F2D88A', '#E0A94A', '#F4E6B8', '#D99A3C'];
    for (const [y, dz] of [[0.3, 0.0], [0.85, -0.05], [1.4, -0.1]]) {
      g.add(at(box(Ws - 0.06, 0.04, 0.68 + dz, '#F4F4F2'), 0, y, -0.36 + dz / 2), at(box(Ws - 0.06, 0.06, 0.02, '#2E6FB5', { noGrain: true }), 0, y + 0.02, -0.02 + dz));
      let x = -Ws / 2 + 0.2;
      while (x < Ws / 2 - 0.2) {
        const big = r() < 0.55, c = cheeseCols[Math.floor(r() * cheeseCols.length)];
        if (big) { const R = 0.13 + r() * 0.05; const n = 1 + Math.floor(r() * 2); for (let k = 0; k < n; k++) g.add(at(cyl(R, R, 0.09, c, 14, { pivot: 'bottom', outline: 0.004 }), x + R, y + 0.02 + k * 0.09, -0.3 + dz)); x += 2 * R + 0.05; }
        else { const wd = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.09, 8, 1, false, 0, PI / 3), mat(c)); wd.position.set(x + 0.08, y + 0.065, -0.24 + dz); wd.rotation.y = r() * TAU; wd.castShadow = true; g.add(wd); x += 0.2; }
      }
    }
    g.add(at(box(1.6, 0.4, 0.06, '#2E6FB5', { outline: 0.006 }), 0, 2.35, -0.6), at(label(o.text || 'FROMAGES', 1.5, 0.32, { bg: '#2E6FB5', fg: '#FFFFFF', wrap: false }), 0, 2.35, -0.565));
    g.add(at(box(0.04, 0.3, 0.04, '#9AA0A8'), -0.5, 2.0, -0.62), at(box(0.04, 0.3, 0.04, '#9AA0A8'), 0.5, 2.0, -0.62));
    return g;
  },

  // A laser sight's red dot (world space): the dot follows o.pts [[t, x, y, z], ...] (linear between points, a small jitter), a soft red glow round
  // it, and a thin red beam from o.src [x, y, z] to it; from o.at (0)
  laserDot(o) {
    const g = grp(), dot = new THREE.Mesh(new THREE.SphereGeometry(o.r ?? 0.03, 10, 8), basic('#FF2A1A'));
    const cv = document.createElement('canvas'); cv.width = cv.height = 64; const x = cv.getContext('2d'); const gr = x.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, 'rgba(255,60,40,0.9)'); gr.addColorStop(1, 'rgba(255,0,0,0)'); x.fillStyle = gr; x.fillRect(0, 0, 64, 64);
    const glow = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(cv), transparent: true, depthWrite: false })); glow.scale.setScalar((o.r ?? 0.03) * 7);
    const beam = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 1, 5), basic('#FF3A2A', { opacity: o.beamOpacity ?? 0.45 })); beam.castShadow = false;
    g.add(dot, glow, beam); noShadow(g);
    const pts = o.pts || [[0, 0, 1, 0]], src = new THREE.Vector3(...(o.src || [0, 3, 6])), P0 = new THREE.Vector3(), up = new THREE.Vector3(0, 1, 0);
    g.userData.update = t => {
      const on = t >= (o.at ?? 0); dot.visible = glow.visible = beam.visible = on; if (!on) return;
      let i = 0; while (i < pts.length - 1 && t > pts[i + 1][0]) i++;
      const a = pts[i], b = pts[Math.min(i + 1, pts.length - 1)], w = b[0] > a[0] ? clamp01((t - a[0]) / (b[0] - a[0])) : 0, j = o.jitter ?? 0.012;
      P0.set(a[1] + (b[1] - a[1]) * w + j * Math.sin(t * 31), a[2] + (b[2] - a[2]) * w + j * Math.sin(t * 27 + 1), a[3] + (b[3] - a[3]) * w + j * Math.sin(t * 23 + 2));
      dot.position.copy(P0); glow.position.copy(P0);
      const d = P0.clone().sub(src), L = d.length(); beam.position.copy(src).addScaledVector(d, 0.5); beam.scale.set(1, L, 1); beam.quaternion.setFromUnitVectors(up, d.normalize());
    };
    g.userData.update(0); return g;
  },

  // Falling bombs (world space): o.drops [{from, to, t0, dur}]: a fat olive bomb with tail fins and a yellow band falls from `from` to `to` (gravity:
  // slow then fast), nose down along its path, hidden before t0 and after t0 + dur; o.s (1) scales them
  bombDrop(o) {
    const s = o.s ?? 1, g = grp(), bombs = [];
    for (const d of o.drops || []) {
      const b = grp(), body = new THREE.Mesh(new THREE.CapsuleGeometry(0.22 * s, 0.7 * s, 4, 10), mat('#4A5236')); body.castShadow = true; addOutline(body, 0.03); b.add(body);
      b.add(at(cyl(0.225 * s, 0.225 * s, 0.08 * s, '#E2B53C', 10), 0, 0.12 * s, 0));
      for (let i = 0; i < 4; i++) { const fp = grp(at(box(0.02 * s, 0.32 * s, 0.26 * s, '#3A4128', { outline: 0.02 }), 0, 0.62 * s, 0.15 * s)); fp.rotation.y = i * PI / 2; b.add(fp); }
      b.visible = false; g.add(b); bombs.push({ b, d, A: new THREE.Vector3(...d.from), B: new THREE.Vector3(...d.to) });
    }
    const up = new THREE.Vector3(0, 1, 0);
    g.userData.update = t => { for (const { b, d, A, B } of bombs) {
      const u = (t - d.t0) / d.dur; b.visible = u >= 0 && u < 1; if (!b.visible) continue;
      const w = 0.35 * u + 0.65 * u * u; b.position.copy(A).lerp(B, w);
      const dir = B.clone().sub(A).normalize(); b.quaternion.setFromUnitVectors(up, dir.negate()); b.rotateY(t * 6 + d.t0);
    } };
    g.userData.update(-1); return g;
  },

  // A hubcap rolling on its edge (pivot at its centre; it rolls along +Z, its axle along X): a silver disc r o.r (0.22) with a dark hub and spokes;
  // o.spin (rad/s, 9), o.wobble (0.15 rad)
  hubcap(o) {
    const R = o.r ?? 0.22, g = grp(), w = grp(at(cyl(R, R, 0.04, '#C9CDD3', 16, { outline: 0.01 }), 0, 0, 0, 0, 0, PI / 2), at(cyl(R * 0.28, R * 0.28, 0.05, '#5A6068', 10), 0, 0, 0, 0, 0, PI / 2));
    for (let i = 0; i < 5; i++) { const sp = grp(at(box(0.05, R * 0.75, 0.04, '#8E949C'), 0.026, R * 0.5, 0)); sp.rotation.x = i * TAU / 5; w.add(sp); }
    g.add(w);
    g.userData.update = t => { w.rotation.x = (o.spin ?? 9) * t; g.rotation.z = (o.wobble ?? 0.15) * Math.sin(t * 7); };
    g.userData.update(0); return g;
  },

  // A tower of tanks (pivot at the floor under its middle): o.n (5) army tanks (battleTank) at o.s (0.62) stacked one on another, turned a little
  // each, every one with its own small invented flag on a rod (o.flags [[c1, c2, (c3)], ...]); the turrets point every which way
  tankTower(o) {
    const n = o.n ?? 5, s = o.s ?? 0.62, g = grp(), fl = [], cols = o.colors || ['#66753E', '#5E6B3A', '#707A48', '#5A6640', '#6B7444'];
    const flags = o.flags || [['#2E8B57', '#F2C94C'], ['#7A2E8C', '#F4F1E8'], ['#E07A1F', '#1F4E8C'], ['#1E7A8C', '#E8504A', '#F4F1E8'], ['#C8322A', '#F4F1E8']];
    const marks = ['disc', 'star', 'chevron', null, 'disc'];
    for (let i = 0; i < n; i++) {
      const tk = buildProp('battleTank', { color: cols[i % cols.length], turret: [[0, (hsh(i + 2) - 0.5) * 2.4]] }); tk.scale.setScalar(s);
      tk.position.set((hsh(i) - 0.5) * 0.3, i * 1.55 * s, (hsh(i + 5) - 0.5) * 0.35); tk.rotation.y = (i % 2 ? 1 : -1) * (0.1 + 0.14 * hsh(i + 7)) + (i === 2 ? PI : 0);
      g.add(tk);
      const f = wavingFlag(0.62, 0.4, flagDraw(flags[i % flags.length], marks[i % marks.length]), 4);
      const pole = grp(at(cyl(0.015, 0.015, 1.1, '#8A8F96', 5, { pivot: 'bottom' }), 0, 0, 0)); f.position.set(0.016, 1.1, 0); pole.add(f);
      pole.scale.setScalar(1 / s); pole.position.set(0.55, 1.58, -0.9); pole.rotation.y = 0.5 * (hsh(i + 9) - 0.5) + PI / 2; tk.add(pole); fl.push(f);
    }
    g.userData.update = t => { fl.forEach((f, i) => f.userData.wave(t, 0.32, i * 1.7)); for (const c of g.children) c.userData.update?.(t); };
    g.userData.update(0); return g;
  },

  // A flagpole with an invented flag (pivot at the foot of the pole): o.h (3.4) tall, the flag o.fw (1.2) x 0.8 in bands o.colors with o.mark
  // ('star', 'disc', 'chevron'); o.plantAt (s): it is driven straight down into the ground from o.drop (0.9 m) higher over 0.12 s with a small
  // shudder (hold it above its spot before)
  bayFlag(o) {
    const Hp = o.h ?? 3.4, fw = o.fw ?? 1.2, g = grp(), pole = grp(); g.add(pole);
    pole.add(at(cyl(0.035, 0.045, Hp, '#E8E8E4', 8, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(sphere(0.07, '#E2B53C', 1), 0, Hp + 0.04, 0));
    const f = wavingFlag(fw, fw * 0.66, flagDraw(o.colors || ['#3E5A2E', '#3E5A2E'], o.mark ?? 'star', o.markColor || '#E2B53C'), 6); f.position.set(0.04, Hp - 0.05, 0); pole.add(f);
    g.userData.update = t => {
      let y = 0, sh = 0; if (o.plantAt != null) { const u = (t - o.plantAt) / 0.12; y = (o.drop ?? 0.9) * (1 - easeIn(u)); if (u >= 1) sh = 0.04 * Math.exp(-(t - o.plantAt - 0.12) * 8) * Math.sin((t - o.plantAt) * 50); }
      pole.position.y = y; pole.rotation.z = sh; f.userData.wave(t, 0.3);
    };
    g.userData.update(0); return g;
  },

  // A border post (pivot at the foot of the barrier's post; the road runs along Z, the boom across it along +X): a white booth with a blue band and
  // a window, a sign 'FRONTIÈRE' on its roof, a striped boom o.length (6) long (o.open [[t, deg]] as barrierGate), an invented flag on a pole
  borderPost(o) {
    const g = grp(), L = o.length ?? 6;
    const gate = buildProp('barrierGate', { length: L, angle: o.angle ?? 0, open: o.open || [] }); g.add(gate);
    const bo = grp(at(box(1.8, 2.4, 1.8, '#F2F2EE', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(1.82, 0.3, 1.82, '#2E5E9C'), 0, 1.9, 0), at(box(1.2, 0.8, 0.04, '#9CC9DC', { noGrain: true }), 0, 1.15, 0.92), at(box(2.1, 0.14, 2.1, '#5A6470'), 0, 2.45, 0));
    bo.add(at(box(2.2, 0.55, 0.12, '#2E5E9C', { outline: 0.008 }), 0, 2.85, 0), at(label(o.text || 'FRONTIÈRE', 2.0, 0.42, { bg: '#2E5E9C', fg: '#FFFFFF', wrap: false }), 0, 2.85, 0.065));
    bo.position.set(-1.7, 0, -1.2); g.add(bo);
    const fp = buildProp('bayFlag', { h: 4.2, fw: 1.3, colors: o.colors || ['#1E7A8C', '#F4F1E8', '#1E7A8C'], mark: o.mark ?? 'disc', markColor: o.markColor || '#E8504A' }); fp.position.set(-3.2, 0, -2.0); g.add(fp);
    g.userData.update = t => { gate.userData.update?.(t); fp.userData.update?.(t); };
    g.userData.update(0); return g;
  },

  // Striped tape round a parking bay (pivot at the bay's centre, on the asphalt; the bay o.w (2.5) x o.l (5) along X x Z): four short red-and-white
  // posts at the corners and a striped tape between them at 0.85 m; o.stretch [t0, dur]: the tape runs out round the four sides one after another
  bayTape(o) {
    const w = (o.w ?? 2.5) / 2 + 0.05, l = (o.l ?? 5) / 2 + 0.05, g = grp(), C = [[-w, -l], [w, -l], [w, l], [-w, l]], Hh = 0.85;
    for (const [x, z] of C) { g.add(at(cyl(0.04, 0.05, Hh + 0.1, '#F4F1E8', 8, { pivot: 'bottom', outline: 0.004 }), x, 0, z), at(box(0.22, 0.04, 0.22, '#3A3D44'), x, 0.02, z)); for (let i = 0; i < 3; i++) g.add(at(cyl(0.042, 0.042, 0.1, '#C8202A', 8), x, 0.25 + i * 0.28, z)); }
    const cv = document.createElement('canvas'); cv.width = 128; cv.height = 32; const x = cv.getContext('2d'); x.fillStyle = '#F6F2EA'; x.fillRect(0, 0, 128, 32); x.fillStyle = '#D8322C';
    for (let i = -2; i < 8; i++) { x.beginPath(); x.moveTo(i * 24, 32); x.lineTo(i * 24 + 12, 32); x.lineTo(i * 24 + 24, 0); x.lineTo(i * 24 + 12, 0); x.closePath(); x.fill(); }
    const sides = [];
    for (let i = 0; i < 4; i++) {
      const [ax, az] = C[i], [bx, bz] = C[(i + 1) % 4], L = Math.hypot(bx - ax, bz - az), tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.wrapS = THREE.RepeatWrapping; tex.repeat.set(Math.max(1, L / 0.4), 1);
      const geo = new THREE.PlaneGeometry(1, 0.09); geo.translate(0.5, 0, 0);
      const m = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ map: tex, side: THREE.DoubleSide })); m.position.set(ax, Hh, az); m.rotation.y = -Math.atan2(bz - az, bx - ax); g.add(m); sides.push({ m, L });
    }
    g.userData.update = t => { sides.forEach(({ m, L }, i) => { let k = 1; if (o.stretch) { const [t0, d] = o.stretch; k = clamp01((t - t0 - i * d / 4) / (d / 4)); } m.visible = k > 0.01; m.scale.set(Math.max(0.01, L * k), 1, 1); }); };
    g.userData.update(0); return g;
  },

  // A shopping trolley full of groceries (pivot at the floor; the trolley's long axis along X, the handle at -X): shoppingCart with boxes, bottles
  // and a baguette piled in the basket
  fullTrolley(o) {
    const g = grp(buildProp('shoppingCart', {})), r = rng(o.seed || 4), cols = ['#E8504A', '#F2C94C', '#5E8FD0', '#7FB069', '#F4F1E8', '#E8833A'];
    for (let i = 0; i < 7; i++) g.add(at(box(0.16 + r() * 0.1, 0.18 + r() * 0.14, 0.16 + r() * 0.08, cols[i % cols.length], { pivot: 'bottom', outline: 0.004 }), -0.3 + (i % 4) * 0.2, 0.5 + (i > 3 ? 0.2 : 0), (r() - 0.5) * 0.3, 0, r() * 0.6, 0));
    g.add(at(cyl(0.035, 0.035, 0.5, '#D9A55A', 6, { outline: 0.004 }), 0.1, 0.95, 0.05, 0.3, 0, 1.1), at(cyl(0.045, 0.045, 0.3, '#2E6B3A', 8), -0.2, 0.95, -0.1), at(cyl(0.045, 0.045, 0.3, '#B03030', 8), -0.12, 0.95, 0.12));
    return g;
  },

  // An open, empty wallet (pivot at its spine; it opens along X, the inside facing +Z): two brown leather leaves at o.open (0.5 rad) with empty card
  // slots
  emptyWallet(o) {
    const g = grp(), a = o.open ?? 0.5;
    for (const sx of [-1, 1]) { const leaf = grp(at(box(0.11, 0.09, 0.012, '#6B4226', { outline: 0.004 }), sx * 0.055, 0, 0), at(box(0.09, 0.012, 0.004, '#4E2E1A'), sx * 0.055, 0.015, 0.008), at(box(0.09, 0.012, 0.004, '#4E2E1A'), sx * 0.055, -0.01, 0.008)); leaf.rotation.y = -sx * a; g.add(leaf); }
    return g;
  },

  // A line of small soldiers holding out upturned helmets (pivot at the start of the line): o.path [[x, z], ...] every o.gap (1.0 m), facing o.face
  // (rad, the same for all; default: back along the line), instanced: olive bodies, legs, tan box heads with helmets, both hands holding a helmet
  // out like a bowl; o.size (1); o.skip (n first left out); o.max
  helmetLine(o) {
    const path = o.path || [[0, 0], [20, 0]], gap = o.gap ?? 1.0, s = o.size ?? 1, Y = o.y ?? 0.06, pts = [];
    const seg = []; let tot = 0; for (let i = 1; i < path.length; i++) { const [ax, az] = path[i - 1], [bx, bz] = path[i], L = Math.hypot(bx - ax, bz - az); seg.push([ax, az, bx, bz, L, tot]); tot += L; }
    for (let d = 0; d <= tot + 1e-6; d += gap) { const sg = seg.find(q => d <= q[5] + q[4] + 1e-6) || seg[seg.length - 1], w = sg[4] ? (d - sg[5]) / sg[4] : 0; pts.push([sg[0] + (sg[2] - sg[0]) * w, sg[1] + (sg[3] - sg[1]) * w, Math.atan2(sg[0] - sg[2], sg[1] - sg[3])]); }
    const list = pts.slice(o.skip ?? 0, o.max ?? 400), g = grp(), parts = { body: [], leg: [], head: [], helm: [], arm: [], bowl: [] };
    const r = rng(o.seed || 21);
    for (const [x, z, h0] of list) {
      const a = o.face ?? h0, ca = Math.cos(a), sa = Math.sin(a), j = (r() - 0.5) * 0.06, L = (lx, lz) => [x + lx * ca + lz * sa, z - lx * sa + lz * ca];
      const p = (lx, y, lz, sx, sy, sz, rx = 0) => { const [wx, wz] = L(lx, lz); return [wx, Y + y * s, wz, rx, a + j, 0, sx * s, sy * s, sz * s]; };
      parts.body.push(p(0, 1.15, 0, 0.5, 0.75, 0.3)); parts.leg.push(p(-0.12, 0.4, 0, 0.17, 0.8, 0.2), p(0.12, 0.4, 0, 0.17, 0.8, 0.2));
      parts.head.push(p(0, 1.78, 0, 0.27, 0.36, 0.25)); parts.helm.push(p(0, 2.0, 0, 0.36, 0.18, 0.34));
      parts.arm.push(p(-0.2, 1.25, 0.22, 0.12, 0.12, 0.45), p(0.2, 1.25, 0.22, 0.12, 0.12, 0.45)); parts.bowl.push(p(0, 1.28, 0.48, 0.34, 0.14, 0.32));
    }
    const B = new THREE.BoxGeometry(1, 1, 1), M = c => new THREE.MeshLambertMaterial({ color: c, flatShading: true });
    if (list.length) g.add(inst(B, M('#5B6638'), parts.body), inst(B, M('#4E5730'), parts.leg), inst(B, M('#E0B48A'), parts.head), inst(new THREE.SphereGeometry(0.5, 8, 5, 0, TAU, 0, PI / 2), M('#4E5A34'), parts.helm), inst(B, M('#5B6638'), parts.arm), inst(new THREE.SphereGeometry(0.5, 8, 5, 0, TAU, PI / 2, PI / 2), M('#4E5A34'), parts.bowl));
    return g;
  },
};
