// « Le chifoumi » (story 96): this man lost at rock-paper-scissors to his wife; he contested; the federation reviewed the action on video; she had
// played a hundredth too late; the match was cancelled and replayed at the national stadium; scientists filmed his hand at ten thousand frames a
// second: he always plays rock, for thirty years; judged too predictable, he was replaced by an unbeatable robot hand; its first rock cost the
// factory two storeys; the president decorated it in advance; in the final the stadium split in two; the hand played rock, his wife played well,
// and the hand fell in the hole; the loser had to take out the bin (the bin that grows from the first shot); the hand contests: the well does not count.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
// Hands are mittens (a palm, one finger block, a thumb): rock is the finger block folded under the palm, paper is the mitten flat, the well is
// the mitten curled into a ring; never five fingers. No flag, ring, emblem or real organisation anywhere; the scoreboard shows words only.
import * as THREE from 'three';
import { box, cyl, sphere, mat, addOutline } from './style.js';
import { grp, at, canvasPlane, rod, glowSprite, inst } from './props.js';
import { makeFaceRig, faceState, hasFaceRig } from './facerig.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const easeOut = x => { const u = clamp01(x); return 1 - (1 - u) * (1 - u); };
const outBack = x => { const u = clamp01(x), c = 1.70158; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const lerp = (a, b, u) => a + (b - a) * u;
const EASE = { linear: u => u, in: u => u * u * u, out: u => 1 - Math.pow(1 - u, 3), inOut: u => u * u * (3 - 2 * u) };
const list = v => [].concat(v ?? []);
const noShadow = m => { m.traverse(c => { c.castShadow = false; }); return m; };
const INK = '#1B1B1E', BAG = '#26282E', BAG2 = '#31343B', CREAM = '#F4EEDF';
const HERO_SKIN = '#E6AE84', WIFE_SKIN = '#EBC29C', NAVY = '#2C3756', CUFF = '#F2F2EE';

// a value keyed in time: [[t, v], ...], linear between keys, held outside them
function keyed(ks, t, d) {
  if (!ks || !ks.length) return d;
  if (t <= ks[0][0]) return ks[0][1];
  for (let i = 1; i < ks.length; i++) if (t < ks[i][0]) return lerp(ks[i - 1][1], ks[i][1], (t - ks[i - 1][0]) / Math.max(1e-6, ks[i][0] - ks[i - 1][0]));
  return ks[ks.length - 1][1];
}
// the last value whose time has come: [[t, v], ...]
function stepK(ks, t, d) { let v = d; for (const k of ks || []) if (t >= k[0]) v = k[1]; return v; }
// a bump that rises and falls over [t0, t0 + d]
const bump = (t, t0, d) => { const u = (t - t0) / d; return u > 0 && u < 1 ? Math.sin(PI * u) : 0; };
// a soft radial or vertical gradient texture (dust, glows, the dark of a hole)
const _tex = {};
function gradTex(kind) {
  if (_tex[kind]) return _tex[kind];
  const cv = document.createElement('canvas'); cv.width = cv.height = 128; const c = cv.getContext('2d');
  if (kind === 'hole') { const gr = c.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, '#000000'); gr.addColorStop(0.62, '#07090B'); gr.addColorStop(0.86, '#1E2226'); gr.addColorStop(1, '#3A3530'); c.fillStyle = gr; c.fillRect(0, 0, 128, 128); }
  else { const gr = c.createRadialGradient(64, 64, 2, 64, 64, 63); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.5, 'rgba(255,255,255,0.55)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); c.fillStyle = gr; c.fillRect(0, 0, 128, 128); }
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return (_tex[kind] = t);
}
function softSprite(color, opacity) { const m = new THREE.Sprite(new THREE.SpriteMaterial({ map: gradTex('soft'), color, transparent: true, opacity, depthWrite: false })); m.castShadow = false; return m; }
const unlit = (color, o = {}) => new THREE.MeshBasicMaterial({ color, transparent: !!o.opacity && o.opacity < 1, opacity: o.opacity ?? 1, depthWrite: o.opacity == null || o.opacity >= 1, side: o.side ?? THREE.FrontSide, ...(o.add ? { blending: THREE.AdditiveBlending, depthWrite: false, transparent: true } : {}) });
// a flat layer painted over the ground without depth test (drawn in renderOrder: the field is -2): no flicker with the grassland
function layer(geo, color, order, o = {}) {
  const m = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ color, map: o.map || null, depthTest: false, depthWrite: false, transparent: !!o.opacity, opacity: o.opacity ?? 1 }));
  m.renderOrder = order; m.receiveShadow = false; m.castShadow = false; return m;
}
// a lumpy bin bag (radius 0.5 before scaling), seeded: one geometry per seed
const _bagGeo = {};
function bagGeo(seed = 1) {
  if (_bagGeo[seed]) return _bagGeo[seed];
  const g = new THREE.IcosahedronGeometry(0.5, 1), p = g.attributes.position;
  for (let i = 0; i < p.count; i++) { const x = p.getX(i), y = p.getY(i), z = p.getZ(i), k = 1 + 0.16 * (hsh(Math.round((x * 7 + y * 13 + z * 17) * 10) + seed * 31) - 0.5); p.setXYZ(i, x * k, y * k * 0.82 + (y > 0.3 ? 0.04 : 0), z * k); }
  g.computeVertexNormals(); return (_bagGeo[seed] = g);
}
// one bag with its knot (pivot at its middle)
function bagMesh(size, color, seed) {
  const m = new THREE.Mesh(bagGeo(seed % 3 + 1), mat(color)); m.scale.setScalar(size); m.castShadow = m.receiveShadow = true; addOutline(m, 0.025);
  const knot = new THREE.Mesh(new THREE.ConeGeometry(0.07, 0.16, 5), mat(color)); knot.position.set(0, 0.47, 0); m.add(knot);
  for (const s of [-1, 1]) m.add(at(box(0.05, 0.13, 0.02, color), s * 0.06, 0.56, 0, 0, 0, -s * 0.6));
  return m;
}

// ---------------------------------------------------------------- the mitten (shared by the human hands and the robot's hand)
// wrist at the origin, the hand along +Z, the back of the hand +Y, the palm -Y; thumb on the side sx (+1: +X). set(curl, thumb): curl 0 is the
// flat mitten (paper), 1 the finger block folded under the palm (rock); thumb 0 out, 1 wrapped across the front of the fist
function mitten({ W = 0.095, T = 0.04, Lp = 0.095, Lf = 0.088, color = HERO_SKIN, sx = 1, ol = 0.05, back = null }) {
  const g = grp(), o = { outline: ol };
  g.add(at(box(W, T, Lp, color, o), 0, 0, Lp / 2));
  if (back) g.add(at(box(W * 0.9, 0.004, Lp * 0.8, back), 0, T / 2 + 0.002, Lp * 0.5));
  const knuck = at(cyl(T * 0.52, T * 0.52, W * 0.98, color, 10), 0, -T * 0.02, Lp, 0, 0, PI / 2); g.add(knuck);
  const piv = grp(); piv.position.set(0, -T / 2, Lp); g.add(piv);
  const fing = grp(at(box(W * 0.96, T * 0.92, Lf, color, o), 0, T * 0.46, Lf / 2), at(cyl(T * 0.46, T * 0.46, W * 0.94, color, 10), 0, T * 0.46, Lf, 0, 0, PI / 2));
  piv.add(fing);
  const tp = grp(); tp.position.set(sx * W * 0.44, -T * 0.05, Lp * 0.28); g.add(tp);
  const th = grp(at(box(T * 0.82, T * 0.78, Lp * 0.62, color, o), 0, 0, Lp * 0.31), at(sphere(T * 0.42, color, 1), 0, 0, Lp * 0.62)); tp.add(th);
  const set = (curl, thumb) => {
    piv.rotation.x = clamp01(curl) * 3.05;
    tp.rotation.set(lerp(0.05, 0.75, thumb), lerp(sx * 0.55, -sx * 1.25, thumb), 0);
    tp.position.y = lerp(-T * 0.05, -T * 0.55, thumb);
  };
  set(0, 0); return { g, set };
}
// the well: the mitten curled into a ring standing on the wrist, its hole facing +Z (R the ring's radius, r the tube)
function wellRing({ R = 0.05, r = 0.024, color = WIFE_SKIN, sx = 1 }) {
  const g = grp(), ring = new THREE.Mesh(new THREE.TorusGeometry(R, r, 8, 20), mat(color)); ring.castShadow = true; addOutline(ring, 0.06);
  g.add(at(ring, 0, R + r * 0.6, 0.02));
  g.add(at(box(r * 2.0, R * 0.9, r * 2.1, color, { outline: 0.06 }), 0, R * 0.2, 0.02));
  const seam = at(box(r * 0.25, r * 2.3, r * 2.3, '#8A5A40'), sx * R * 0.72, R * 1.65 + r * 0.6, 0.02, 0, 0, -sx * 0.75); g.add(seam);
  g.add(at(sphere(r * 1.05, color, 1), sx * R * 0.86, R * 1.45 + r * 0.6, 0.03));
  return g;
}

export const CHIFOUMI_PROPS = {
  // A forearm and a mitten hand, cartoon size (pivot at the elbow: the back end of the sleeve, the hand toward +Z, the back of the hand up): o.s scales
  // it (1: a real hand), o.sleeve (0.3) the forearm's length, o.sleeveColor / o.cuff, o.skin, o.side 'R' | 'L' (the thumb toward -X for 'L'); o.mode
  // 'rock' | 'paper' | 'well' and o.modes [[t, mode], ...] (a switch folds the fingers in 0.07 s with a squash-pop); o.pumps [t, ...]: the forearm
  // pumps up and down once from each time (chi, fou, mi); o.tilt (rad, + down) and o.bend (the wrist, + down); o.tiltK [[t, rad], ...] keyed tilt
  chifHand(o) {
    const s = o.s ?? 1, sx = o.side === 'L' ? -1 : 1, skin = o.skin || HERO_SKIN, SL = o.sleeve ?? 0.3, g = grp(), arm = grp(); g.add(arm);
    const sr = 0.043;
    arm.add(at(cyl(sr * 1.05, sr, SL, o.sleeveColor || NAVY, 9, { outline: 0.05 }), 0, 0, SL / 2, PI / 2, 0, 0));
    arm.add(at(cyl(sr * 1.12, sr * 1.12, 0.035, o.cuff || CUFF, 9), 0, 0, SL - 0.015, PI / 2, 0, 0));
    const wrist = grp(); wrist.position.set(0, 0, SL); arm.add(wrist);
    const hand = grp(); wrist.add(hand);
    const M = mitten({ color: skin, sx }); hand.add(M.g);
    const W = wellRing({ color: skin, sx }); hand.add(W);
    g.scale.setScalar(s);
    const modes = o.modes || [[-99, o.mode || 'paper']];
    const sw = modes.map(m => m[0]);
    g.userData.update = t => {
      const m = stepK(modes, t, o.mode || 'paper');
      let tPrev = -99; for (const x of sw) if (x <= t) tPrev = x;
      const u = clamp01((t - tPrev) / 0.07), pop = tPrev > -50 ? 1 + 0.22 * Math.sin(PI * clamp01((t - tPrev) / 0.16)) : 1;
      const prevM = stepK(modes, tPrev - 1e-4, m);
      const curlOf = q => q === 'rock' ? 1 : 0;
      const c = lerp(curlOf(prevM), curlOf(m), u);
      M.set(c, c);
      const well = m === 'well';
      M.g.visible = !well || u < 0.5; W.visible = well;
      W.scale.setScalar(well ? Math.max(0.01, outBack(clamp01((t - tPrev) / 0.12))) : 1);
      hand.scale.set(pop, 1 / Math.sqrt(pop), pop);
      let pump = 0; for (const p of o.pumps || []) pump += bump(t, p, 0.26);
      arm.rotation.x = keyed(o.tiltK, t, o.tilt ?? 0) - 0.62 * pump;
      wrist.rotation.x = (o.bend ?? 0) + 0.25 * pump;
    };
    g.userData.update(0); return g;
  },

  // A kitchen pedal bin (pivot at the floor, the pedal +Z): a red body o.h (0.62) high, a black liner over the rim, the lid hinged at the back and
  // propped open by what is inside; o.level 0 (full: one bag bulging over the rim), 1 (overflowing: bags heaped on top, lid thrown back, bags on the
  // floor round it), 2 (a heap as tall as the bin itself); o.flies (n), o.stink (wavy green lines rising); o.s scales it
  chifBin(o) {
    const s = o.s ?? 1, h = 0.62, r = 0.2, lvl = o.level ?? 0, g = grp(), C = o.color || '#C8443A';
    g.add(at(cyl(r, r * 0.92, h, C, 10, { pivot: 'bottom', outline: 0.03 }), 0, 0, 0));
    g.add(at(cyl(r * 0.94, r * 0.94, 0.03, '#2A2C30', 10), 0, 0.015, 0), at(box(0.12, 0.03, 0.08, '#2A2C30'), 0, 0.03, r * 0.95));
    g.add(at(cyl(r * 1.04, r * 1.04, 0.07, BAG, 10, { outline: 0.03 }), 0, h - 0.01, 0));
    for (let i = 0; i < 5; i++) { const a = i / 5 * TAU + 0.3; g.add(at(box(0.09, 0.12, 0.02, BAG), Math.sin(a) * r * 1.05, h - 0.06, Math.cos(a) * r * 1.05, 0, a, 0)); }
    const lid = grp(at(cyl(r * 1.02, r * 1.02, 0.035, C, 10, { outline: 0.04 }), 0, 0, r), at(box(0.1, 0.03, 0.05, '#2A2C30'), 0, 0.03, r * 1.9));
    lid.position.set(0, h + 0.02, -r); lid.rotation.x = -(lvl === 0 ? 1.15 : 1.95); g.add(lid);
    const heap = lvl === 0 ? [[0, h + 0.07, 0.02, 0.36]] : lvl === 1 ? [[0, h + 0.1, 0, 0.42], [-0.08, h + 0.32, 0.05, 0.34], [0.1, h + 0.28, -0.04, 0.3], [0.02, h + 0.5, 0.0, 0.28], [0.28, 0.14, 0.18, 0.3], [-0.3, 0.13, 0.12, 0.28], [0.05, 0.13, 0.36, 0.26]]
      : [[0, h + 0.12, 0, 0.46], [-0.12, h + 0.4, 0.06, 0.38], [0.14, h + 0.36, -0.05, 0.36], [0, h + 0.66, 0.02, 0.32], [-0.06, h + 0.9, -0.02, 0.28], [0.32, 0.16, 0.2, 0.34], [-0.34, 0.15, 0.14, 0.32], [0.06, 0.15, 0.42, 0.3], [0.45, 0.42, 0.0, 0.3], [-0.42, 0.4, -0.1, 0.3], [0.3, 0.15, -0.3, 0.32]];
    heap.forEach(([x, y, z, sz], i) => { const b = bagMesh(sz, i % 3 === 2 ? BAG2 : BAG, i); b.position.set(x, y, z); b.rotation.set(0.2 * (hsh(i) - 0.5), hsh(i + 3) * TAU, 0.2 * (hsh(i + 7) - 0.5)); g.add(b); });
    const flies = [];
    for (let i = 0; i < (o.flies ?? 0); i++) { const f = grp(at(sphere(0.022, '#141416', 1), 0, 0, 0), at(box(0.04, 0.003, 0.02, '#F4F8FF', { opacity: 0.85 }), -0.022, 0.012, 0, 0, 0, 0.4), at(box(0.04, 0.003, 0.02, '#F4F8FF', { opacity: 0.85 }), 0.022, 0.012, 0, 0, 0, -0.4)); noShadow(f); g.add(f); flies.push(f); }
    const stinks = [];
    for (let i = 0; i < (o.stink ?? 0); i++) { const p = canvasPlane(0.12, 0.42, (c, W, H) => { c.strokeStyle = '#7FB33C'; c.lineWidth = W * 0.13; c.lineCap = 'round'; c.beginPath(); for (let k = 0; k <= 20; k++) { const y = H * (1 - k / 20), x = W / 2 + Math.sin(k / 20 * TAU * 1.5) * W * 0.3; k ? c.lineTo(x, y) : c.moveTo(x, y); } c.stroke(); }, { res: 64, transparent: true }); noShadow(p); g.add(p); stinks.push(p); }
    const top = lvl === 0 ? h + 0.3 : lvl === 1 ? h + 0.75 : h + 1.1;
    g.scale.setScalar(s);
    g.userData.update = t => {
      flies.forEach((f, i) => { const w = 2.2 + hsh(i) * 1.6, a = t * w + i * 2.1, rr = 0.22 + 0.08 * Math.sin(t * 3.1 + i); f.position.set(Math.cos(a) * rr, top + 0.1 + 0.08 * Math.sin(t * 5.3 + i * 1.7), Math.sin(a) * rr * 0.7 + 0.05); f.rotation.y = -a; });
      stinks.forEach((p, i) => { const u = ((t * 0.55 + i / Math.max(1, stinks.length)) % 1); p.position.set((i - (stinks.length - 1) / 2) * 0.14, top - 0.1 + u * 0.45, 0.1); p.material.opacity = Math.sin(PI * u); p.material.transparent = true; p.scale.set(1, 0.6 + 0.6 * u, 1); });
    };
    g.userData.update(0); return g;
  },

  // A heap of black bin bags (pivot at the middle of its foot): a lumpy cone o.h high on a foot of radius o.r, bags of o.bag (m) across, a few green,
  // blue and yellow ones among the black; o.gulls circling seagulls (o.gullS their size, o.gullR the circle, o.gullH above the top), o.perch gulls
  // standing on top, o.flies buzzing dots (o.flyS); o.rollAt: one more bag rolls down the front (+Z) slope over o.rollDur (1.1 s) and settles
  chifBagHeap(o) {
    const H = o.h ?? 6, R = o.r ?? 4, bs = o.bag ?? 0.7, g = grp();
    const core = new THREE.Mesh(new THREE.ConeGeometry(R * 0.9, H * 0.97, 10, 3), mat('#1E2025')); core.position.y = H * 0.485; core.castShadow = core.receiveShadow = true; g.add(core);
    const area = PI * R * Math.hypot(R, H), n = Math.min(o.n ?? Math.round(area / (bs * bs * 0.55)), 2600), L = [], C = [], KN = [];
    const pal = ['#25272C', '#2B2D33', '#202226', '#33363D', '#2F3B2E', '#25272C', '#2B2D33', '#3A5E8C', '#25272C', '#C9B65A'];
    for (let i = 0; i < n; i++) {
      const u = hsh(i * 3 + 1), y = H * (1 - Math.sqrt(u)) * 0.97, a = i * 2.39996 + hsh(i) * 0.4, rr = Math.max(bs * 0.3, R * (1 - y / H)) * (0.98 + 0.08 * hsh(i + 5)), sz = bs * (0.75 + 0.5 * hsh(i + 2));
      L.push([Math.cos(a) * rr, y + sz * 0.25, Math.sin(a) * rr, 0.3 * (hsh(i + 9) - 0.5), hsh(i + 4) * TAU, 0.3 * (hsh(i + 8) - 0.5), sz, sz, sz]); C.push(pal[Math.floor(hsh(i + 11) * pal.length)]);
      if (i % 2 === 0) KN.push([Math.cos(a) * rr, y + sz * 0.68, Math.sin(a) * rr, 0, 0, 0, sz, sz, sz]);
    }
    const bm = inst(bagGeo(2), mat('#FFFFFF'), L, C); bm.castShadow = bm.receiveShadow = true; g.add(bm);
    const km = inst(new THREE.ConeGeometry(0.08, 0.2, 5), mat('#1C1D21'), KN); g.add(km);
    const gulls = [], mkGull = sz => {
      const q = grp(), body = new THREE.Mesh(new THREE.SphereGeometry(0.5, 8, 6), mat('#F6F6F2')); body.scale.set(0.42, 0.36, 0.9); q.add(body);
      q.add(at(sphere(0.17, '#F6F6F2', 1), 0, 0.14, 0.42), at(new THREE.Mesh(new THREE.ConeGeometry(0.05, 0.18, 5), mat('#F2B233')), 0, 0.12, 0.62, PI / 2, 0, 0), at(sphere(0.03, INK, 0), 0.09, 0.19, 0.5), at(sphere(0.03, INK, 0), -0.09, 0.19, 0.5));
      q.add(at(box(0.2, 0.06, 0.3, '#9EA4AA'), 0, 0.02, -0.5, -0.3, 0, 0));
      const wl = grp(at(box(0.9, 0.04, 0.32, '#A9AFB5'), -0.45, 0, 0), at(box(0.25, 0.045, 0.3, '#2A2C30'), -0.95, 0, 0)), wr = grp(at(box(0.9, 0.04, 0.32, '#A9AFB5'), 0.45, 0, 0), at(box(0.25, 0.045, 0.3, '#2A2C30'), 0.95, 0, 0));
      wl.position.set(-0.15, 0.1, 0); wr.position.set(0.15, 0.1, 0); q.add(wl, wr); q.userData.w = [wl, wr]; q.scale.setScalar(sz); const ms = []; q.traverse(c => { if (c.isMesh) ms.push(c); }); ms.forEach(c => addOutline(c, 0.04)); return q;
    };
    for (let i = 0; i < (o.gulls ?? 0); i++) { const q = mkGull(o.gullS ?? 1); g.add(q); gulls.push(q); }
    const perch = [];
    for (let i = 0; i < (o.perch ?? 0); i++) { const q = mkGull(o.gullS ?? 1); q.userData.w.forEach((w, j) => { w.rotation.z = j ? -1.2 : 1.2; w.scale.set(0.45, 1, 1); }); const a = i * 2.2 + 0.6, rr = R * 0.12 + 0.3 * i; q.position.set(Math.cos(a) * rr, H * (1 - rr / R) + bs * 0.55 * (o.gullS ?? 1), Math.sin(a) * rr); q.rotation.y = 0.9 + i * 1.7; g.add(q); perch.push(q); }
    const flies = [];
    for (let i = 0; i < (o.flies ?? 0); i++) { const f = at(sphere(0.06 * (o.flyS ?? 1), '#121214', 0), 0, 0, 0); noShadow(f); g.add(f); flies.push(f); }
    let roller = null;
    if (o.rollAt != null) { roller = bagMesh(bs * 1.05, BAG, 7); g.add(roller); }
    g.userData.update = t => {
      gulls.forEach((q, i) => { const gr = (o.gullR ?? R * 0.7) * (0.8 + 0.35 * hsh(i)), sp = (0.45 + 0.2 * hsh(i + 2)) * (i % 2 ? 1 : -1), a = t * sp + i * TAU / Math.max(1, gulls.length);
        q.position.set(Math.cos(a) * gr, H + (o.gullH ?? 2.5) + 1.2 * hsh(i + 4) + 0.3 * Math.sin(t * 1.3 + i), Math.sin(a) * gr); q.rotation.set(0, -a + (sp > 0 ? 0 : PI), sp > 0 ? 0.35 : -0.35);
        const fl = 0.55 * Math.sin(t * 7.5 + i * 1.9); q.userData.w[0].rotation.z = fl; q.userData.w[1].rotation.z = -fl; });
      perch.forEach((q, i) => { q.children[1].position.y = 0.14 + 0.03 * Math.max(0, Math.sin(t * 4 + i * 2)); q.rotation.y = 0.9 + i * 1.7 + 0.35 * Math.sin(t * 0.9 + i); });
      flies.forEach((f, i) => { const a = t * (3 + hsh(i) * 2) + i * 1.3, rr = R * 0.18 + R * 0.12 * Math.sin(t * 2.1 + i); f.position.set(Math.cos(a) * rr, H * 0.92 + 0.5 * Math.sin(t * 4.7 + i * 2.3), Math.sin(a) * rr); });
      if (roller) { const d = o.rollDur ?? 1.1, u = clamp01((t - o.rollAt) / d), y0 = H * 0.86, z0 = R * 0.12, z1 = R * 1.08, y1 = bs * 0.5;
        const z = lerp(z0, z1, u), y = Math.max(y1, lerp(y0, y1, Math.pow(u, 0.9))) + 0.35 * bs * Math.abs(Math.sin(u * PI * 3)) * (1 - u);
        roller.visible = t >= o.rollAt - 0.02; roller.position.set(0.2 * Math.sin(u * 2), y, z); roller.rotation.set(u * 9, 0.4, 0); }
    };
    g.userData.update(0); return g;
  },

  // A glowing trail along a polyline (the referee's rectangle drawn in the air): o.pts [[x, y, z], ...] (local), drawn from o.at over o.dur at a
  // constant speed, a hot white core in an additive halo (o.color, o.r the core radius), a spark at the tip while it draws; it then hangs, pulsing,
  // and fades from o.fadeAt over 0.4 s
  chifTrail(o) {
    const P = (o.pts || [[0, 0, 0], [1, 0, 0]]).map(p => new THREE.Vector3(...p)), g = grp(), r = o.r ?? 0.022, col = o.color || '#FFE27A';
    const segs = [], lens = []; let L = 0;
    const coreM = unlit('#FFFFFF'), haloM = unlit(col, { add: true, opacity: 0.55 }), wideM = unlit(col, { add: true, opacity: 0.2 });
    for (let i = 0; i < P.length - 1; i++) {
      const a = P[i], b = P[i + 1], d = b.clone().sub(a), l = d.length(); lens.push(l); L += l;
      const q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(1, 0, 0), d.clone().normalize());
      const parts = [new THREE.Mesh(new THREE.BoxGeometry(1, r * 2, r * 2), coreM), new THREE.Mesh(new THREE.BoxGeometry(1, r * 5, r * 5), haloM), new THREE.Mesh(new THREE.BoxGeometry(1, r * 11, r * 11), wideM)];
      parts.forEach(m => { m.quaternion.copy(q); m.castShadow = false; m.renderOrder = 3; g.add(m); });
      segs.push({ a, d: d.normalize(), parts });
    }
    const corners = P.map(p => { const s = glowSprite(col, r * 12, 0.9); s.position.copy(p); s.renderOrder = 3; g.add(s); return s; });
    const tip = glowSprite('#FFFFFF', r * 22, 1); tip.renderOrder = 4; g.add(tip);
    g.userData.update = t => {
      const u = clamp01((t - (o.at ?? 0)) / (o.dur ?? 1)), drawn = u * L, fade = o.fadeAt == null ? 1 : 1 - clamp01((t - o.fadeAt) / 0.4);
      let acc = 0;
      segs.forEach((s, i) => { const l = Math.max(0, Math.min(lens[i], drawn - acc)); s.parts.forEach(m => { m.visible = l > 0.001 && fade > 0; m.scale.x = Math.max(0.001, l); m.position.copy(s.a).addScaledVector(s.d, l / 2); }); acc += lens[i]; });
      let a2 = 0; corners.forEach((c, i) => { c.visible = t >= (o.at ?? 0) && drawn >= a2 - 1e-6 && fade > 0; c.material.opacity = 0.9 * fade; if (i < lens.length) a2 += lens[i]; });
      const pulse = u >= 1 ? 0.75 + 0.25 * Math.sin((t - (o.at ?? 0) - (o.dur ?? 1)) * 7) : 1;
      haloM.opacity = 0.55 * pulse * fade; wideM.opacity = 0.2 * pulse * fade; coreM.opacity = fade; coreM.transparent = fade < 1;
      let rem = drawn, tp = P[0].clone(); for (let i = 0; i < segs.length; i++) { if (rem <= lens[i]) { tp = segs[i].a.clone().addScaledVector(segs[i].d, rem); break; } rem -= lens[i]; tp = P[i + 1].clone(); }
      tip.position.copy(tp); tip.visible = u > 0 && u < 1; tip.scale.setScalar(r * 22 * (0.85 + 0.3 * Math.sin(t * 40)));
    };
    g.userData.update(-1); return g;
  },

  // A wall of screens (pivot at the foot of the wall in the middle, the screens +Z): o.cols x o.rows screens of o.sw x o.sh, their bottom row at o.y;
  // each loops two frames of the kitchen footage (o.kinds per screen: 'hands' the fist under the flat hand, 'fist' his fist pumping, 'wife' her flat
  // hand, 'slow' the two hands frozen apart with a red line); o.stand: one screen on a pole stand instead (o.y its bottom)
  chifScreens(o) {
    const cols = o.cols ?? 3, rows = o.rows ?? 2, sw = o.sw ?? 1.2, sh = o.sh ?? 0.72, gp = 0.08, y0 = o.y ?? 1.0, g = grp(), W = cols * sw + (cols - 1) * gp, Ht = rows * sh + (rows - 1) * gp;
    if (o.stand) g.add(at(cyl(0.04, 0.04, y0, '#3A3D44', 6, { pivot: 'bottom' }), 0, 0, -0.08), at(box(0.6, 0.04, 0.45, '#3A3D44'), 0, 0.02, -0.08));
    else g.add(at(box(W + 0.24, Ht + 0.24, 0.1, '#161A22', { outline: 0.004 }), 0, y0 + Ht / 2, -0.06));
    const kinds = o.kinds || ['hands', 'fist', 'slow', 'wife', 'hands', 'fist'], frames = [];
    const drawHand = (c, x, y, s, mode, skin, sleeve, dir) => {
      c.save(); c.translate(x, y); c.scale(dir, 1); c.lineJoin = 'round'; c.lineWidth = s * 0.06; c.strokeStyle = '#141414';
      c.fillStyle = sleeve; c.fillRect(-s * 2.4, -s * 0.38, s * 1.6, s * 0.76); c.strokeRect(-s * 2.4, -s * 0.38, s * 1.6, s * 0.76);
      c.fillStyle = '#F2F2EE'; c.fillRect(-s * 0.9, -s * 0.42, s * 0.2, s * 0.84);
      c.fillStyle = skin; c.beginPath();
      if (mode === 'rock') { c.roundRect(-s * 0.72, -s * 0.48, s * 1.1, s * 0.96, s * 0.3); c.fill(); c.stroke(); c.beginPath(); c.moveTo(s * 0.1, -s * 0.3); c.lineTo(s * 0.1, s * 0.3); c.stroke(); c.beginPath(); c.roundRect(-s * 0.55, s * 0.05, s * 0.6, s * 0.32, s * 0.16); c.fill(); c.stroke(); }
      else { c.roundRect(-s * 0.72, -s * 0.22, s * 1.75, s * 0.44, s * 0.2); c.fill(); c.stroke(); c.beginPath(); c.roundRect(-s * 0.45, -s * 0.52, s * 0.55, s * 0.28, s * 0.14); c.fill(); c.stroke(); }
      c.restore();
    };
    const draw = (kind, f) => (c, Wc, Hc) => {
      const gr = c.createLinearGradient(0, 0, 0, Hc); gr.addColorStop(0, '#2C4A6E'); gr.addColorStop(1, '#16283E'); c.fillStyle = gr; c.fillRect(0, 0, Wc, Hc);
      c.fillStyle = '#C98C5A'; c.fillRect(0, Hc * 0.78, Wc, Hc * 0.22);
      const s = Hc * 0.2;
      if (kind === 'fist') drawHand(c, Wc * 0.55, Hc * (f ? 0.42 : 0.56), s * 1.25, 'rock', HERO_SKIN, NAVY, 1);
      else if (kind === 'wife') drawHand(c, Wc * 0.45, Hc * (f ? 0.45 : 0.55), s * 1.2, 'paper', WIFE_SKIN, '#5E8C7A', -1);
      else if (kind === 'slow') { drawHand(c, Wc * 0.38, Hc * 0.6, s, 'rock', HERO_SKIN, NAVY, 1); drawHand(c, Wc * 0.66, Hc * 0.36, s, 'paper', WIFE_SKIN, '#5E8C7A', -1); c.strokeStyle = '#FF2E2E'; c.lineWidth = Hc * 0.05; c.lineCap = 'round'; c.beginPath(); c.moveTo(Wc * 0.47, Hc * 0.18); c.lineTo(Wc * 0.47, Hc * 0.86); c.stroke(); }
      else { drawHand(c, Wc * 0.42, Hc * 0.58, s, 'rock', HERO_SKIN, NAVY, 1); drawHand(c, Wc * (f ? 0.56 : 0.6), Hc * (f ? 0.42 : 0.38), s, 'paper', WIFE_SKIN, '#5E8C7A', -1); }
      c.fillStyle = 'rgba(255,255,255,0.08)'; for (let y = 0; y < Hc; y += 6) c.fillRect(0, y, Wc, 2);
      c.fillStyle = '#FFFFFF'; c.font = `bold ${Math.round(Hc * 0.1)}px Arial`; c.fillText('RALENTI', Wc * 0.05, Hc * 0.14);
      c.fillStyle = '#FF3B30'; c.beginPath(); c.arc(Wc * 0.03, Hc * 0.11, Hc * 0.025, 0, TAU); c.fill();
    };
    for (let j = 0; j < (o.stand ? 1 : rows); j++) for (let i = 0; i < (o.stand ? 1 : cols); i++) {
      const x = -W / 2 + sw / 2 + i * (sw + gp), y = y0 + sh / 2 + j * (sh + gp), kind = kinds[(j * cols + i) % kinds.length];
      g.add(at(box(sw, sh, 0.06, '#0E1014', { outline: 0.004 }), o.stand ? 0 : x, o.stand ? y0 + sh / 2 : y, 0));
      const A = canvasPlane(sw * 0.93, sh * 0.88, draw(kind, 0), { res: 256, emissive: 0.85 }), B = canvasPlane(sw * 0.93, sh * 0.88, draw(kind, 1), { res: 256, emissive: 0.85 });
      [A, B].forEach(p => { p.position.set(o.stand ? 0 : x, o.stand ? y0 + sh / 2 : y, 0.034); p.castShadow = false; g.add(p); });
      frames.push([A, B, hsh(i + j * 7) * 0.6]);
    }
    g.userData.update = t => frames.forEach(([A, B, ph]) => { const f = Math.floor((t + ph) / (o.loop ?? 0.32)) % 2; A.visible = f === 0; B.visible = f === 1; });
    g.userData.update(0); return g;
  },

  // A referee's headset (attach to the head joint, offset [0, 0, 0]): a black band over the crown, two ear cups, a boom mic to the mouth; o.w the
  // head's width (0.31)
  chifHeadset(o) {
    const w = o.w ?? 0.31, g = grp(), K = '#141518';
    const band = new THREE.Mesh(new THREE.TorusGeometry(w / 2 + 0.03, 0.018, 5, 14, PI), mat(K)); band.position.set(0, 0.3, -0.01); g.add(band);
    for (const s of [-1, 1]) g.add(at(cyl(0.065, 0.065, 0.05, K, 10), s * (w / 2 + 0.03), 0.28, -0.01, 0, 0, PI / 2), at(cyl(0.045, 0.045, 0.02, '#5A5E66', 10), s * (w / 2 + 0.058), 0.28, -0.01, 0, 0, PI / 2));
    g.add(rod([w / 2 + 0.04, 0.25, 0.02], [0.07, 0.1, 0.13], 0.009, K), at(sphere(0.024, '#D13A2E', 1), 0.065, 0.1, 0.135));
    return g;
  },

  // A red telestrator line between two points (pivot at o.a), drawn from o.at over o.dur, with a ring round each end (rings face +Z); o.r its
  // thickness (0.03), o.ring the end rings' radius (0.09); unlit, so it reads on any picture
  chifRedLine(o) {
    const a = new THREE.Vector3(...(o.a || [0, 0, 0])), b = new THREE.Vector3(...(o.b || [0, 1, 0])), g = grp(), r = o.r ?? 0.03, M = unlit('#FF2B2B'), WM = unlit('#FFFFFF');
    const d = b.clone().sub(a), L = d.length(), q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.clone().normalize());
    const line = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 1, 8), M), edge = new THREE.Mesh(new THREE.CylinderGeometry(r * 1.6, r * 1.6, 1, 8), WM);
    [edge, line].forEach((m, i) => { m.quaternion.copy(q); m.renderOrder = 5 + i; m.castShadow = false; g.add(m); });
    const rings = [a, b].map(p => { const m = new THREE.Mesh(new THREE.TorusGeometry(o.ring ?? 0.09, r * 0.8, 6, 24), M); m.position.copy(p); m.renderOrder = 6; g.add(m); return m; });
    g.userData.update = t => { const u = EASE.out(clamp01((t - (o.at ?? 0)) / (o.dur ?? 0.3))), l = Math.max(0.001, u * L);
      [edge, line].forEach(m => { m.visible = u > 0; m.scale.set(1, l, 1); m.position.copy(a).addScaledVector(d.clone().normalize(), l / 2); });
      rings[0].visible = u > 0; rings[1].visible = u >= 0.98; rings.forEach((m, i) => m.scale.setScalar(m.visible ? 1 + 0.15 * Math.sin(t * 8 + i) : 1)); };
    g.userData.update(-1); return g;
  },

  // The replay frame laid over the picture (pivot at its middle, facing +Z: place it just in front of the camera, facing it): white corner brackets,
  // « RALENTI » with a blinking red dot, a scrub bar with a moving head at the bottom; o.w x o.h
  chifHud(o) {
    const w = o.w ?? 0.5, h = o.h ?? 0.89, g = grp();
    const p = canvasPlane(w, h, (c, W, H) => { c.strokeStyle = '#FFFFFF'; c.lineWidth = W * 0.012; const k = W * 0.1, m = W * 0.05;
      for (const [x, y, sx, sy] of [[m, m, 1, 1], [W - m, m, -1, 1], [m, H - m, 1, -1], [W - m, H - m, -1, -1]]) { c.beginPath(); c.moveTo(x + sx * k, y); c.lineTo(x, y); c.lineTo(x, y + sy * k); c.stroke(); }
      c.fillStyle = '#FFFFFF'; c.font = `bold ${Math.round(W * 0.075)}px Arial`; c.fillText('RALENTI', W * 0.14, H * 0.075 + W * 0.03);
      c.fillStyle = 'rgba(255,255,255,0.35)'; c.fillRect(W * 0.1, H * 0.71, W * 0.8, W * 0.012); }, { res: 512, transparent: true });
    p.material.depthTest = false; p.renderOrder = 20; g.add(p);
    const dot = new THREE.Mesh(new THREE.CircleGeometry(w * 0.022, 12), unlit('#FF3B30')); dot.position.set(-w * 0.41, h / 2 - h * 0.075 - w * 0.005, 0.001); dot.material.depthTest = false; dot.renderOrder = 21; g.add(dot);
    const head = new THREE.Mesh(new THREE.CircleGeometry(w * 0.02, 12), unlit('#FFFFFF')); head.material.depthTest = false; head.renderOrder = 21; g.add(head);
    g.userData.update = t => { dot.visible = Math.floor(t / 0.4) % 2 === 0; head.position.set(-w * 0.4 + w * 0.8 * (0.62 - 0.04 * Math.min(t, 2)), -h / 2 + h * 0.29 - w * 0.006, 0.001); };
    g.userData.update(0); return g;
  },

  // The national stadium, built from the start as two halves (pivot at the centre spot): an oval of stands round a mown pitch with plain white
  // lines, a crowd of box-headed fans on every step, four floodlight towers and a scoreboard of words (o.board [line1, line2]). o.split [[t, d], ...]:
  // each half slides d metres away along X; o.cheer (0..1) the fans' bounce, o.standAt they rise, o.heartAt their right hands go to their hearts,
  // o.jumps [t, ...] a jolt of the ground (the robot's beats); o.crackAt / o.crackDur: a crack runs across the pitch from end to end through the
  // centre, past the round hole o.hole [x, z] (radius o.holeR) that opens from o.holeAt; o.rimAt: a stone rim rises round it (the well), o.splashAt
  // a splash comes up out of it; o.clear [[x, z, r], ...] leaves the fans out of those spots (real actors sit there); o.rows, o.a0, o.b0 the size
  chifStadium(o) {
    const a0 = o.a0 ?? 30, b0 = o.b0 ?? 21, rows = o.rows ?? 14, rd = o.rowD ?? 1.3, rh = o.rowH ?? 0.7, fh = o.frontH ?? 1.2, g = grp();
    const PL = o.pitchL ?? 44, PW = o.pitchW ?? 27;
    // the ground layers (painted, no depth test): the stadium floor, the pitch with mown stripes, the lines
    const aO = a0 + rows * rd + 3, bO = b0 + rows * rd + 3;
    const ell = (a, b, n = 64) => { const s = new THREE.Shape(); for (let i = 0; i <= n; i++) { const t = i / n * TAU; i ? s.lineTo(a * Math.cos(t), b * Math.sin(t)) : s.moveTo(a, 0); } return s; };
    g.add(at(layer(new THREE.ShapeGeometry(ell(aO, bO)), '#8E9196', -1.8), 0, 0.01, 0, -PI / 2));
    g.add(at(layer(new THREE.ShapeGeometry(ell(a0 + 0.2, b0 + 0.2)), '#4F8A3E', -1.7), 0, 0.011, 0, -PI / 2));
    const pitchTex = (() => { const cv = document.createElement('canvas'); cv.width = 1024; cv.height = 640; const c = cv.getContext('2d'); for (let i = 0; i < 12; i++) { c.fillStyle = i % 2 ? '#62A64A' : '#579C40'; c.fillRect(i * cv.width / 12, 0, cv.width / 12 + 1, cv.height); }
      c.strokeStyle = '#F4F4EE'; c.lineWidth = 7; const W = cv.width, H = cv.height, m = 10; c.strokeRect(m, m, W - 2 * m, H - 2 * m); c.beginPath(); c.moveTo(W / 2, m); c.lineTo(W / 2, H - m); c.stroke();
      c.beginPath(); c.arc(W / 2, H / 2, H * 0.17, 0, TAU); c.stroke(); c.fillStyle = '#F4F4EE'; c.beginPath(); c.arc(W / 2, H / 2, 9, 0, TAU); c.fill();
      for (const sx of [0, 1]) { const x0 = sx ? W - m : m, dx = sx ? -1 : 1; c.strokeRect(Math.min(x0, x0 + dx * W * 0.16), H * 0.22, W * 0.16, H * 0.56); c.strokeRect(Math.min(x0, x0 + dx * W * 0.055), H * 0.38, W * 0.055, H * 0.24); }
      const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t; })();
    g.add(at(layer(new THREE.PlaneGeometry(PL, PW), '#FFFFFF', -1.6, { map: pitchTex }), 0, 0.012, 0, -PI / 2));
    // goals at both ends (white frames, no nets)
    for (const sx of [-1, 1]) { const gx = sx * PL / 2; g.add(rod([gx, 0, -3.6], [gx, 2.4, -3.6], 0.07, '#F4F4EE'), rod([gx, 0, 3.6], [gx, 2.4, 3.6], 0.07, '#F4F4EE'), rod([gx, 2.4, -3.6], [gx, 2.4, 3.6], 0.07, '#F4F4EE')); }
    // the crack: a jagged dark band from z -b0 to +b0 through the centre, bending past the hole
    const hole = o.hole || [-1.3, 1.3], HR = o.holeR ?? 0.75;
    const cp = []; const NC = 46; for (let i = 0; i <= NC; i++) { const v = i / NC, z = lerp(-b0 - 1, b0 + 1, v), near = Math.exp(-Math.pow((z - hole[1]) / 2.2, 2)); cp.push([lerp(0.6 * Math.sin(v * 23) + 0.35 * Math.sin(v * 57), hole[0], near), z]); }
    const crackM = new THREE.MeshLambertMaterial({ color: '#141210', depthTest: false, depthWrite: false }), cGeo = new THREE.BufferGeometry(), cPos = new Float32Array(NC * 6 * 3);
    cGeo.setAttribute('position', new THREE.BufferAttribute(cPos, 3)); cGeo.setAttribute('normal', new THREE.BufferAttribute(new Float32Array(NC * 6 * 3).map((v, i) => i % 3 === 1 ? 1 : 0), 3));
    const crack = new THREE.Mesh(cGeo, crackM); crack.renderOrder = -1.5; crack.frustumCulled = false; crack.position.y = 0.013; g.add(crack);
    const holeM = new THREE.MeshBasicMaterial({ map: gradTex('hole'), depthTest: false, depthWrite: false }), holeD = new THREE.Mesh(new THREE.CircleGeometry(1, 28), holeM); holeD.rotation.x = -PI / 2; holeD.position.set(hole[0], 0.014, hole[1]); holeD.renderOrder = -1.4; g.add(holeD);
    // the well's stone rim (rises out of the ground: the field hides it until then), its dark inner wall and a black floor that swallows what falls in
    const rim = grp(); rim.position.set(hole[0], 0, hole[1]); g.add(rim);
    const ST = ['#9A938A', '#B3ACA2', '#8A847C', '#A7A096'];
    for (let i = 0; i < 14; i++) { const a = i / 14 * TAU; rim.add(at(box(0.36, 0.42, 0.24, ST[i % 4], { outline: 0.03 }), Math.cos(a) * (HR + 0.1), 0.21, Math.sin(a) * (HR + 0.1), 0, -a + PI / 2, 0)); }
    for (let i = 0; i < 14; i++) { const a = (i + 0.5) / 14 * TAU; rim.add(at(box(0.33, 0.1, 0.26, ST[(i + 2) % 4], { outline: 0.03 }), Math.cos(a) * (HR + 0.1), 0.47, Math.sin(a) * (HR + 0.1), 0, -a + PI / 2, 0)); }
    const inner = new THREE.Mesh(new THREE.CylinderGeometry(HR, HR, 0.5, 20, 1, true), new THREE.MeshBasicMaterial({ color: '#1A1816', side: THREE.BackSide })); inner.position.y = 0.26; rim.add(inner);
    const floor = new THREE.Mesh(new THREE.CircleGeometry(HR * 1.01, 24), new THREE.MeshBasicMaterial({ map: gradTex('hole') })); floor.rotation.x = -PI / 2; floor.position.y = 0.035; rim.add(floor);
    const glint = new THREE.Mesh(new THREE.RingGeometry(HR * 0.1, HR * 0.16, 20), unlit('#7FA6C8', { opacity: 0.55 })); glint.rotation.x = -PI / 2; glint.position.y = 0.04; rim.add(glint);
    const splash = []; for (let i = 0; i < 16; i++) { const m = sphere(0.07 + 0.05 * hsh(i), '#EAF4FF', 0, { unique: true }); m.castShadow = false; m.visible = false; rim.add(m); splash.push(m); }
    // the two halves: stepped stands (instanced boxes), the crowd, the outer wall, two floodlights each; the scoreboard rides on the -X half
    const halves = [-1, 1].map(side => {
      const H = grp(); g.add(H);
      const steps = [], scol = [], fans = [];
      for (let k = 0; k < rows; k++) {
        const a = a0 + (k + 0.5) * rd, b = b0 + (k + 0.5) * rd, top = fh + k * rh, n = Math.ceil(PI * (a + b) / 2 / 1.6);
        for (let i = 0; i < n; i++) {
          const t0 = (side > 0 ? -PI / 2 : PI / 2) + (i + 0.5) / n * PI, x = a * Math.cos(t0), z = b * Math.sin(t0), tx = -a * Math.sin(t0), tz = b * Math.cos(t0), len = Math.hypot(tx, tz) * PI / n * 1.04;
          steps.push([x, top / 2, z, 0, -Math.atan2(tz, tx), 0, len, top, rd * 1.02]); scol.push(k % 2 ? '#B7BCC4' : '#A4AAB3');
        }
        const nf = Math.floor(PI * (a + b) / 2 / 0.82);
        for (let i = 0; i < nf; i++) {
          const t0 = (side > 0 ? -PI / 2 : PI / 2) + (i + 0.5 + 0.3 * (hsh(i + k * 131) - 0.5)) / nf * PI, x = a * Math.cos(t0), z = b * Math.sin(t0);
          if (hsh(i * 7 + k * 53 + (side > 0 ? 3 : 0)) < 0.05) continue;
          if ((o.clear || []).some(([cx, cz, cr]) => Math.hypot(x + side * 0 - cx, z - cz) < cr)) continue;
          fans.push({ x, y: fh + k * rh, z, ry: Math.atan2(-x, -z), ph: hsh(i + k * 977) * TAU, c: hsh(i * 3 + k), s: hsh(i * 5 + k * 3) });
        }
      }
      const sm = inst(new THREE.BoxGeometry(1, 1, 1), mat('#FFFFFF'), steps, scol); sm.receiveShadow = true; sm.castShadow = false; H.add(sm);
      // the outer wall
      const wl = [], nw = 70, aw = a0 + rows * rd + 0.15, bw = b0 + rows * rd + 0.15, wh = fh + rows * rh + 1.4;
      for (let i = 0; i < nw; i++) { const t0 = (side > 0 ? -PI / 2 : PI / 2) + (i + 0.5) / nw * PI, tx = -aw * Math.sin(t0), tz = bw * Math.cos(t0), len = Math.hypot(tx, tz) * PI / nw * 1.05; wl.push([aw * Math.cos(t0), wh / 2, bw * Math.sin(t0), 0, -Math.atan2(tz, tx), 0, len, wh, 0.5]); }
      const wm = inst(new THREE.BoxGeometry(1, 1, 1), mat('#E4DED2'), wl); wm.castShadow = true; H.add(wm);
      const bl = wl.map(p => [p[0], wh - 0.5, p[2], 0, p[4], 0, p[6], 0.35, 0.56]); H.add(inst(new THREE.BoxGeometry(1, 1, 1), mat('#3F6FA8'), bl));
      // the crowd: bodies, heads, hair, two arms (the right one goes to the heart)
      const BC = ['#E0413A', '#2F62B5', '#F2C230', '#F4F4F0', '#3A9B5C', '#C255C8', '#F28C28', '#3A3D44', '#7FC4E8'], SK = ['#F0C8A0', '#E2A878', '#C88A5E', '#8E5E3C', '#F4D2B4'], HC = ['#2A2420', '#5A3A28', '#C9A24A', '#1B1B1E', '#8A8A8A'];
      const n = fans.length, bodyM = new THREE.InstancedMesh(new THREE.BoxGeometry(0.62, 1, 0.42).translate(0, 0.5, 0), mat('#FFFFFF'), n), headM = new THREE.InstancedMesh(new THREE.BoxGeometry(0.46, 0.46, 0.38).translate(0, 0.23, 0), mat('#FFFFFF'), n),
        hairM = new THREE.InstancedMesh(new THREE.BoxGeometry(0.48, 0.12, 0.4).translate(0, 0.06, 0), mat('#FFFFFF'), n), armL = new THREE.InstancedMesh(new THREE.BoxGeometry(0.16, 0.62, 0.16).translate(0, 0.31, 0), mat('#FFFFFF'), n), armR = new THREE.InstancedMesh(new THREE.BoxGeometry(0.16, 0.62, 0.16).translate(0, 0.31, 0), mat('#FFFFFF'), n);
      const cc = new THREE.Color();
      fans.forEach((f, i) => { const bc = BC[Math.floor(f.c * BC.length)]; bodyM.setColorAt(i, cc.set(bc)); armL.setColorAt(i, cc.set(bc)); armR.setColorAt(i, cc.set(bc)); headM.setColorAt(i, cc.set(SK[Math.floor(f.s * SK.length)])); hairM.setColorAt(i, cc.set(HC[Math.floor(hsh(i + 17) * HC.length)])); });
      [bodyM, headM, hairM, armL, armR].forEach(m => { m.castShadow = false; m.receiveShadow = false; m.frustumCulled = false; H.add(m); });
      const towers = [];
      for (const sz of [-1, 1]) { const tx = side * (a0 + rows * rd * 0.6) * 0.72, tz = sz * (b0 + rows * rd + 2) * 0.72, tw = grp(at(cyl(0.35, 0.5, 26, '#BFC4CA', 6, { pivot: 'bottom' }), 0, 0, 0), at(box(4.2, 2.2, 0.5, '#4A4E56', { outline: 0.01 }), 0, 26.5, 0));
        for (let i = 0; i < 4; i++) for (let j = 0; j < 2; j++) tw.add(at(box(0.8, 0.7, 0.1, '#FFF6D8', { emissive: '#FFE9A8', noGrain: true }), -1.45 + i * 0.97, 26.05 + j * 0.9, 0.26));
        tw.position.set(tx, 0, tz); tw.rotation.y = Math.atan2(-tx, -tz); H.add(tw); towers.push(tw); }
      return { H, fans, bodyM, headM, hairM, armL, armR, side };
    });
    if (o.board) {
      const bw = 16, bh = 6, bx = -(a0 + rows * rd + 1.5), by = fh + rows * rh + 6.5;
      const board = grp(at(box(bw + 0.8, bh + 0.8, 0.6, '#2A2D33', { outline: 0.006 }), 0, 0, -0.32), at(box(0.6, by, 0.6, '#5A5E66', { pivot: 'bottom' }), -bw * 0.35, -by, -0.5), at(box(0.6, by, 0.6, '#5A5E66', { pivot: 'bottom' }), bw * 0.35, -by, -0.5));
      board.add(at(canvasPlane(bw, bh, (c, W, H) => { c.fillStyle = '#0D1016'; c.fillRect(0, 0, W, H); const ln = list(o.board);
        ln.forEach((s, i) => { let fs = H * (i === 0 ? 0.3 : 0.34); c.font = `900 ${fs}px Arial`; const tw = c.measureText(s).width; if (tw > W * 0.9) { fs *= W * 0.9 / tw; c.font = `900 ${fs}px Arial`; }
          c.fillStyle = i === 0 ? '#FFB43A' : '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(s, W / 2, H * (ln.length === 1 ? 0.5 : i === 0 ? 0.3 : 0.7)); }); }, { res: 1024, emissive: 1 }), 0, 0, 0.0));
      board.position.set(bx, by, 0); board.rotation.y = PI / 2; halves[0].H.add(board);
    }
    const dm = new THREE.Object3D(), qY = new THREE.Quaternion(), qA = new THREE.Quaternion(), AY = new THREE.Vector3(0, 1, 0);
    const jumps = list(o.jumps);
    g.userData.update = t => {
      const d = keyed(o.split, t, 0), jolt = jumps.reduce((s, j) => s + bump(t, j, 0.16), 0);
      halves.forEach(h => { h.H.position.set(h.side * d, 0.12 * jolt, 0); });
      const st = o.standAt == null ? 0 : smooth((t - o.standAt) / 0.45), hr = o.heartAt == null ? 0 : smooth((t - o.heartAt) / 0.3), ch = (o.cheer ?? 0.6) * (1 - 0.8 * hr);
      halves.forEach(h => {
        h.fans.forEach((f, i) => {
          const bob = ch * 0.18 * Math.max(0, Math.sin(t * 8.5 + f.ph)) + 0.25 * jolt, by = f.y + bob, bh = lerp(0.95, 1.4, st), seat = lerp(0, 0, st);
          dm.position.set(f.x, by + seat, f.z); dm.quaternion.identity(); dm.rotation.set(0, f.ry, 0); dm.scale.set(1, bh, 1); dm.updateMatrix(); h.bodyM.setMatrixAt(i, dm.matrix);
          dm.position.set(f.x, by + bh, f.z); dm.scale.set(1, 1, 1); dm.updateMatrix(); h.headM.setMatrixAt(i, dm.matrix);
          dm.position.set(f.x, by + bh + 0.44, f.z); dm.updateMatrix(); h.hairM.setMatrixAt(i, dm.matrix);
          const wave = 0.5 + 0.5 * Math.sin(t * 8.5 + f.ph + 0.6), shY = by + bh - 0.12;
          qY.setFromAxisAngle(AY, f.ry);
          for (const [m, sd] of [[h.armL, 1], [h.armR, -1]]) {
            const up = clamp01((f.s > 0.45 ? 1 : 0.3) * ch * 1.6 * wave), lift = lerp(0.15, 2.7, up);
            const dir = new THREE.Vector3(sd * Math.sin(lift), -Math.cos(lift), 0.15);
            if (sd < 0 && hr > 0) dir.lerp(new THREE.Vector3(0.46, -0.35, 0.3), hr);
            if (sd > 0 && hr > 0) dir.lerp(new THREE.Vector3(0.12, -1, 0.05), hr);
            qA.setFromUnitVectors(AY, dir.normalize()); dm.quaternion.copy(qY).multiply(qA);
            const off = new THREE.Vector3(sd * 0.36, 0, 0).applyQuaternion(qY); dm.position.set(f.x + off.x, shY, f.z + off.z); dm.scale.set(1, 1, 1);
            dm.updateMatrix(); m.setMatrixAt(i, dm.matrix);
          }
        });
        [h.bodyM, h.headM, h.hairM, h.armL, h.armR].forEach(m => { m.instanceMatrix.needsUpdate = true; });
      });
      const cu = o.crackAt == null ? 0 : clamp01((t - o.crackAt) / (o.crackDur ?? 0.5)), wcr = 0.1 + 0.35 * clamp01(d / 4);
      crack.visible = cu > 0;
      for (let i = 0; i < NC; i++) {
        const v0 = i / NC, v1 = (i + 1) / NC, mid = 0.5, on0 = Math.abs(v0 - mid) <= cu * 0.5 + 1e-6, on1 = Math.abs(v1 - mid) <= cu * 0.5 + 1e-6, w0 = on0 ? wcr * (0.6 + 0.8 * hsh(i)) : 0, w1 = on1 ? wcr * (0.6 + 0.8 * hsh(i + 1)) : 0;
        const [x0, z0] = cp[i], [x1, z1] = cp[i + 1], q = [[x0 - w0, z0], [x0 + w0, z0], [x1 + w1, z1], [x0 - w0, z0], [x1 + w1, z1], [x1 - w1, z1]];
        q.forEach(([x, z], j) => { cPos[(i * 6 + j) * 3] = x; cPos[(i * 6 + j) * 3 + 1] = 0; cPos[(i * 6 + j) * 3 + 2] = z; });
      }
      cGeo.attributes.position.needsUpdate = true;
      const hu = o.holeAt == null ? 0 : outBack(clamp01((t - o.holeAt) / 0.35)); holeD.visible = hu > 0.01; holeD.scale.setScalar(Math.max(0.01, HR * 1.05 * hu));
      const ru = o.rimAt == null ? 0 : outBack(clamp01((t - o.rimAt) / 0.3)); rim.visible = ru > 0.001; rim.position.y = lerp(-0.62, 0, ru);
      splash.forEach((m, i) => { const u = o.splashAt == null ? -1 : (t - o.splashAt - 0.02 * i) / 0.7; m.visible = u > 0 && u < 1 && rim.visible; if (!m.visible) return; const a = hsh(i + 2) * TAU, sp = 0.4 + 0.5 * hsh(i + 5);
        m.position.set(Math.cos(a) * sp * u * HR, 0.3 + (1.6 + 1.2 * hsh(i)) * u - 3.2 * u * u, Math.sin(a) * sp * u * HR); m.scale.setScalar(1 - 0.6 * u); });
    };
    g.userData.update(0); return g;
  },

  // A padded lab clamp for a fist (pivot at the floor under the jaws; the fist goes toward +Z out of the jaws): a weighted base, a post, two orange
  // padded jaws o.h (1.2) high round the forearm, a screw knob; o.lamps: two bright lamps on stands aimed at the jaws
  chifClamp(o) {
    const h = o.h ?? 1.2, g = grp(), ST = '#C9CED4', D = '#5A5F68';
    g.add(at(box(0.7, 0.06, 0.6, D, { outline: 0.01 }), 0, 0.03, -0.15), at(cyl(0.045, 0.045, h - 0.06, ST, 8, { pivot: 'bottom' }), 0, 0.06, -0.32));
    g.add(at(box(0.08, 0.08, 0.36, ST, { outline: 0.01 }), 0, h + 0.17, -0.16), at(box(0.42, 0.06, 0.1, ST, { outline: 0.01 }), 0, h + 0.17, 0));
    for (const s of [-1, 1]) g.add(at(box(0.06, 0.3, 0.12, ST, { outline: 0.01 }), s * 0.18, h + 0.03, 0), at(box(0.07, 0.16, 0.2, '#E8822E', { outline: 0.02 }), s * 0.115, h, 0));
    g.add(at(cyl(0.06, 0.06, 0.05, '#2A2C30', 10), 0.25, h + 0.17, 0, 0, 0, PI / 2), at(box(0.05, 0.05, 0.05, '#C8443A'), 0, h + 0.24, 0));
    if (o.lamps) for (const s of [-1, 1]) {
      const L = grp(at(box(0.4, 0.04, 0.4, D), 0, 0.02, 0), at(cyl(0.025, 0.025, 1.9, ST, 6, { pivot: 'bottom' }), 0, 0, 0));
      const head = grp(at(new THREE.Mesh(new THREE.ConeGeometry(0.22, 0.3, 12, 1, true), mat('#E8E8E2', { doubleSide: true })), 0, 0, 0, PI / 2, 0, 0), at(new THREE.Mesh(new THREE.CircleGeometry(0.18, 14), unlit('#FFFBEA')), 0, 0, 0.12));
      const gs = glowSprite('#FFF4C8', 0.9, 0.7); gs.position.set(0, 0, 0.2); head.add(gs);
      head.position.set(0, 1.95, 0); L.add(head); L.position.set(s * 0.95, 0, 0.55);
      const dx = -s * 0.95, dy = h - 1.95, dz = -0.55; head.rotation.order = 'YXZ'; head.rotation.set(Math.atan2(-dy, Math.hypot(dx, dz)), Math.atan2(dx, dz), 0); g.add(L);
    }
    return g;
  },

  // A big film camera on rails (pivot at the rails' middle; the lens looks toward +Z): two rails o.len (4) long on sleepers, a dolly with a column,
  // a dark camera body with a long lens and a red tally light; the dolly slides from o.z0 to o.z1 between o.t0 and o.t1 (slow, eased)
  chifRailCam(o) {
    const len = o.len ?? 4, g = grp(), D = '#2A2C30';
    for (const s of [-1, 1]) g.add(at(box(0.06, 0.06, len, '#9AA0A8', { outline: 0.01 }), s * 0.35, 0.09, 0));
    for (let i = 0; i <= Math.round(len / 0.5); i++) g.add(at(box(0.9, 0.06, 0.12, '#6A4A32'), 0, 0.03, -len / 2 + i * 0.5));
    const dolly = grp(at(box(0.9, 0.14, 0.8, '#3E4250', { outline: 0.01 }), 0, 0.22, 0), at(cyl(0.08, 0.1, 0.75, D, 8, { pivot: 'bottom' }), 0, 0.29, 0));
    for (const s of [-1, 1]) for (const z of [-0.3, 0.3]) dolly.add(at(cyl(0.07, 0.07, 0.06, D, 10), s * 0.35, 0.16, z, 0, 0, PI / 2));
    const cam = grp(at(box(0.48, 0.44, 0.75, '#33363F', { outline: 0.015 }), 0, 0, 0), at(cyl(0.17, 0.2, 0.55, D, 14), 0, 0, 0.62, PI / 2, 0, 0), at(cyl(0.2, 0.2, 0.06, '#15161A', 14), 0, 0, 0.9, PI / 2, 0, 0));
    cam.add(at(new THREE.Mesh(new THREE.CircleGeometry(0.15, 16), mat('#2E5A86', { emissive: '#1A3A5A' })), 0, 0, 0.931), at(box(0.06, 0.04, 0.02, '#FFFFFF', { emissive: '#FFFFFF', noGrain: true }), -0.06, 0.06, 0.935));
    cam.add(at(box(0.3, 0.18, 0.3, '#2A2C34'), 0, 0.3, -0.15), at(sphere(0.04, '#FF2A20', 1, { emissive: '#FF2A20' }), 0.18, 0.18, 0.38), at(box(0.18, 0.14, 0.2, '#1E2026'), 0.32, 0.05, -0.2));
    cam.position.set(0, 1.25, 0); dolly.add(cam); g.add(dolly);
    g.userData.update = t => { dolly.position.z = lerp(o.z0 ?? -len / 2 + 0.5, o.z1 ?? len / 2 - 0.5, EASE.inOut(clamp01((t - (o.t0 ?? 0)) / Math.max(0.01, (o.t1 ?? 3) - (o.t0 ?? 0))))); };
    g.userData.update(0); return g;
  },

  // The scientists' whiteboard on a wheeled stand (pivot at the floor, the face +Z): o.w (2.6) x o.h (1.6), its bottom at o.y (0.8); three big photos
  // of him making a fist (a wedding veil beside him, a bicycle, asleep on a pillow), and under them a thick block of tally marks that fills row by
  // row from o.tallyAt over o.tallyDur (o.rows rows)
  chifBoard(o) {
    const W = o.w ?? 2.6, H = o.h ?? 1.6, y0 = o.y ?? 0.8, g = grp(), AL = '#B9BEC4';
    g.add(at(box(W + 0.1, H + 0.1, 0.05, AL, { outline: 0.006 }), 0, y0 + H / 2, -0.03));
    for (const s of [-1, 1]) g.add(at(box(0.06, y0 + H, 0.06, AL, { pivot: 'bottom' }), s * (W / 2 + 0.05), 0, -0.06), at(box(0.06, 0.06, 0.7, AL), s * (W / 2 + 0.05), 0.1, -0.06), at(sphere(0.05, '#2A2C30', 0), s * (W / 2 + 0.05), 0.05, 0.25), at(sphere(0.05, '#2A2C30', 0), s * (W / 2 + 0.05), 0.05, -0.37));
    g.add(at(box(W * 0.98, H * 0.98, 0.012, '#F8F8F4'), 0, y0 + H / 2, 0.0));
    let faces = null;
    if (hasFaceRig) { try { faces = ['neutral', 'neutral', 'relieved'].map(e => { const fr = makeFaceRig(null); fr.set(faceState(e)); const cv = document.createElement('canvas'); cv.width = fr.canvas.width; cv.height = fr.canvas.height; cv.getContext('2d').drawImage(fr.canvas, 0, 0); return cv; }); } catch (e) { faces = null; } }
    const pw = W * 0.29, ph = H * 0.5;
    const photo = (kind, i) => canvasPlane(pw, ph, (c, Wc, Hc) => {
      c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, Wc, Hc); const m = Wc * 0.05, iw = Wc - 2 * m, ih = Hc - 2 * m; c.save(); c.beginPath(); c.rect(m, m, iw, ih); c.clip();
      c.fillStyle = ['#F2C4CE', '#9FD0EA', '#2E3A62'][i]; c.fillRect(m, m, iw, ih);
      const head = (cx, cy, fw, rot, fi) => { c.save(); c.translate(cx, cy); c.rotate(rot); const fh = fw * 1.12; c.fillStyle = '#D9A877'; c.fillRect(-fw * 0.58, -fh * 0.1, fw * 0.1, fh * 0.25); c.fillRect(fw * 0.48, -fh * 0.1, fw * 0.1, fh * 0.25);
        if (faces) c.drawImage(faces[fi], -fw / 2, -fh / 2, fw, fh); else { c.fillStyle = HERO_SKIN; c.fillRect(-fw / 2, -fh / 2, fw, fh); c.fillStyle = '#1E1A18'; c.fillRect(-fw / 2, -fh / 2, fw, fh * 0.17); c.fillStyle = '#111'; c.fillRect(-fw * 0.25, -fh * 0.02, fw * 0.12, fh * 0.1); c.fillRect(fw * 0.13, -fh * 0.02, fw * 0.12, fh * 0.1); c.fillRect(-fw * 0.15, fh * 0.28, fw * 0.3, fh * 0.03); }
        c.restore(); };
      const fist = (x, y, s) => { c.save(); c.translate(x, y); c.lineWidth = s * 0.07; c.strokeStyle = '#151515'; c.fillStyle = NAVY; c.fillRect(-s * 0.3, s * 0.35, s * 0.6, s * 1.2); c.fillStyle = CUFF; c.fillRect(-s * 0.33, s * 0.3, s * 0.66, s * 0.14);
        c.fillStyle = HERO_SKIN; c.beginPath(); c.roundRect(-s * 0.45, -s * 0.5, s * 0.9, s * 0.85, s * 0.25); c.fill(); c.stroke(); c.beginPath(); c.moveTo(-s * 0.4, -s * 0.12); c.lineTo(s * 0.4, -s * 0.12); c.stroke(); c.beginPath(); c.roundRect(-s * 0.48, -s * 0.06, s * 0.62, s * 0.26, s * 0.12); c.fill(); c.stroke(); c.restore(); };
      const suit = (cx, cy, w) => { c.fillStyle = NAVY; c.beginPath(); c.roundRect(cx - w / 2, cy, w, Hc, w * 0.15); c.fill(); c.fillStyle = CUFF; c.beginPath(); c.moveTo(cx - w * 0.12, cy); c.lineTo(cx, cy + w * 0.3); c.lineTo(cx + w * 0.12, cy); c.fill(); c.fillStyle = '#C8302A'; c.fillRect(cx - w * 0.04, cy + w * 0.05, w * 0.08, w * 0.4); };
      if (kind === 'veil') {
        c.fillStyle = 'rgba(255,255,255,0.95)'; c.beginPath(); c.moveTo(Wc * 0.68, Hc * 0.16); c.quadraticCurveTo(Wc * 1.05, Hc * 0.3, Wc * 0.98, Hc); c.lineTo(Wc * 0.5, Hc); c.quadraticCurveTo(Wc * 0.44, Hc * 0.4, Wc * 0.68, Hc * 0.16); c.fill();
        c.strokeStyle = '#D8C8B8'; c.lineWidth = Wc * 0.012; c.stroke(); c.fillStyle = '#F2D9A0'; c.beginPath(); c.arc(Wc * 0.68, Hc * 0.18, Wc * 0.06, 0, TAU); c.fill();
        suit(Wc * 0.36, Hc * 0.62, Wc * 0.5); head(Wc * 0.36, Hc * 0.42, Wc * 0.34, 0, 0); fist(Wc * 0.5, Hc * 0.75, Wc * 0.2);
      } else if (kind === 'bike') {
        suit(Wc * 0.5, Hc * 0.55, Wc * 0.46); head(Wc * 0.5, Hc * 0.33, Wc * 0.32, 0, 1);
        c.strokeStyle = '#151515'; c.lineWidth = Wc * 0.045; for (const x of [0.24, 0.76]) { c.beginPath(); c.arc(Wc * x, Hc * 0.86, Wc * 0.17, 0, TAU); c.stroke(); }
        c.strokeStyle = '#D8342A'; c.lineWidth = Wc * 0.04; c.beginPath(); c.moveTo(Wc * 0.24, Hc * 0.86); c.lineTo(Wc * 0.45, Hc * 0.68); c.lineTo(Wc * 0.68, Hc * 0.68); c.lineTo(Wc * 0.76, Hc * 0.86); c.moveTo(Wc * 0.45, Hc * 0.68); c.lineTo(Wc * 0.52, Hc * 0.86); c.lineTo(Wc * 0.68, Hc * 0.68); c.stroke();
        c.strokeStyle = '#151515'; c.lineWidth = Wc * 0.03; c.beginPath(); c.moveTo(Wc * 0.62, Hc * 0.62); c.lineTo(Wc * 0.82, Hc * 0.6); c.stroke(); fist(Wc * 0.78, Hc * 0.55, Wc * 0.18);
      } else {
        c.fillStyle = '#F4F4F0'; c.beginPath(); c.roundRect(Wc * 0.08, Hc * 0.18, Wc * 0.55, Hc * 0.42, Wc * 0.1); c.fill(); c.fillStyle = '#5A7FC0'; c.beginPath(); c.roundRect(Wc * 0.1, Hc * 0.58, Wc * 0.95, Hc * 0.5, Wc * 0.05); c.fill();
        head(Wc * 0.36, Hc * 0.38, Wc * 0.32, -0.25, 2); fist(Wc * 0.66, Hc * 0.62, Wc * 0.2);
        c.fillStyle = '#F2E27A'; c.font = `bold ${Math.round(Hc * 0.1)}px Arial`; c.fillText('z', Wc * 0.62, Hc * 0.22); c.fillText('z', Wc * 0.72, Hc * 0.14);
      }
      c.restore();
    }, { res: 384 });
    ['veil', 'bike', 'pillow'].forEach((k, i) => { const p = photo(k, i); p.position.set((i - 1) * W * 0.32, y0 + H * 0.7, 0.012); p.rotation.z = [0.04, -0.02, 0.05][i]; g.add(p); g.add(at(sphere(0.025, '#C8443A', 0), (i - 1) * W * 0.32, y0 + H * 0.7 + ph / 2 - 0.03, 0.025)); });
    const nr = o.rows ?? 5, rw = W * 0.9, rh = H * 0.33 / nr, rowsP = [];
    for (let j = 0; j < nr; j++) {
      const piv = grp(); piv.position.set(-rw / 2, y0 + H * 0.4 - (j + 0.5) * rh, 0.013); g.add(piv);
      const p = canvasPlane(rw, rh * 0.9, (c, Wc, Hc) => { c.strokeStyle = '#1F3F8A'; c.lineWidth = Hc * 0.07; c.lineCap = 'round'; const gw = Hc * 0.62; let x = Hc * 0.15, i = 0;
        while (x < Wc - gw * 0.8) { for (let k = 0; k < 4; k++) { c.beginPath(); c.moveTo(x + k * gw * 0.18, Hc * 0.12); c.lineTo(x + k * gw * 0.18 + Hc * 0.03 * Math.sin(i + k), Hc * 0.88); c.stroke(); } c.beginPath(); c.moveTo(x - gw * 0.08, Hc * 0.78); c.lineTo(x + gw * 0.62, Hc * 0.2); c.stroke(); x += gw * 0.95; i++; } }, { res: 1024, transparent: true });
      p.position.x = rw / 2; piv.add(p); rowsP.push(piv);
    }
    g.userData.update = t => { const u = o.tallyAt == null ? 1 : clamp01((t - o.tallyAt) / (o.tallyDur ?? 0.8)) * nr; rowsP.forEach((p, j) => { const v = clamp01(u - j); p.visible = v > 0.001; p.scale.x = Math.max(0.001, v); }); };
    g.userData.update(0); return g;
  },

  // His file on the federation's desk (pivot at its middle, lying flat, the top edge toward -Z): a cream folder with a big photo of him clipped on,
  // grey lines; at o.stampAt a red stamp mark (a slanted double frame with a big cross: no words) prints across the photo and the folder jumps
  chifFile(o) {
    const w = o.w ?? 0.6, h = o.h ?? 0.78, g = grp(), sheet = grp(); g.add(sheet);
    sheet.add(at(box(w, 0.015, h, '#E9D7A6', { outline: 0.01 }), 0, 0.0075, 0), at(box(w * 0.3, 0.012, 0.06, '#E9D7A6'), -w * 0.28, 0.0075, -h / 2 - 0.02));
    let face = null; if (hasFaceRig) { try { const fr = makeFaceRig(null); fr.set(faceState('neutral')); face = fr.canvas; } catch (e) { face = null; } }
    const pl = canvasPlane(w * 0.92, h * 0.92, (c, W, H) => { c.fillStyle = '#F6EFDC'; c.fillRect(0, 0, W, H); c.fillStyle = '#9CC9E8'; c.fillRect(W * 0.18, H * 0.06, W * 0.64, H * 0.56); c.fillStyle = NAVY; c.fillRect(W * 0.26, H * 0.48, W * 0.48, H * 0.14);
      const fw = W * 0.4, fh = H * 0.36, fx = W * 0.3, fy = H * 0.1; c.fillStyle = '#D9A877'; c.fillRect(fx - W * 0.03, fy + fh * 0.4, W * 0.04, fh * 0.22); c.fillRect(fx + fw - W * 0.01, fy + fh * 0.4, W * 0.04, fh * 0.22);
      if (face) c.drawImage(face, fx, fy, fw, fh); else { c.fillStyle = HERO_SKIN; c.fillRect(fx, fy, fw, fh); c.fillStyle = '#1E1A18'; c.fillRect(fx, fy, fw, fh * 0.17); }
      c.fillStyle = '#A9A08A'; for (let i = 0; i < 5; i++) c.fillRect(W * 0.12, H * (0.7 + i * 0.055), W * (0.76 - 0.1 * (i % 2)), H * 0.018);
      c.fillStyle = '#8A8F96'; c.fillRect(W * 0.46, 0, W * 0.08, H * 0.05); }, { res: 512 });
    pl.rotation.x = -PI / 2; pl.position.y = 0.017; sheet.add(pl);
    const mark = canvasPlane(w * 0.86, h * 0.6, (c, W, H) => { c.save(); c.translate(W / 2, H / 2); c.rotate(-0.22); c.strokeStyle = 'rgba(206,22,30,0.92)'; c.lineWidth = W * 0.035; c.strokeRect(-W * 0.4, -H * 0.36, W * 0.8, H * 0.72); c.lineWidth = W * 0.016; c.strokeRect(-W * 0.36, -H * 0.31, W * 0.72, H * 0.62);
      c.lineWidth = W * 0.06; c.lineCap = 'round'; c.beginPath(); c.moveTo(-W * 0.25, -H * 0.2); c.lineTo(W * 0.25, H * 0.2); c.moveTo(W * 0.25, -H * 0.2); c.lineTo(-W * 0.25, H * 0.2); c.stroke(); c.restore(); }, { res: 512, transparent: true });
    mark.rotation.x = -PI / 2; mark.position.set(0, 0.02, -h * 0.12); sheet.add(mark);
    g.userData.update = t => { const u = o.stampAt == null ? -1 : t - o.stampAt; mark.visible = u >= 0; const j = u >= 0 && u < 0.3 ? Math.sin(u / 0.3 * PI) : 0; sheet.position.y = 0.025 * j * (u < 0.1 ? 0 : 1); sheet.scale.set(1 + 0.04 * j, 1, 1 + 0.04 * j); };
    g.userData.update(0); return g;
  },

  // The robot arm (pivot at the floor under its base, its front +Z): a mobile base on tracks (o.base 'tracks') or a pedestal ('pedestal'), a turret,
  // an orange upper arm and forearm, and a big box mitten hand in graphite with a thumb and four bolts. It is driven by o.path: [{t, p: [x, y, z]
  // (the wrist, prop-local), hp (the hand's pitch, rad, + up), curl (0 paper .. 1 rock), roll, yaw (optional turret yaw, rad), st (stretch of both
  // links, 1), ease ('linear' | 'in' | 'out' | 'inOut': from the previous key)}, ...] with a two-bone solve in the turret's plane (elbow up).
  // o.hits [t, ...]: the hand squashes on an impact and wobbles back; o.smear [[t0, t1], ...]: three ghost hands trail it; o.trail {t0, t1, color}:
  // the hand's centre leaves a glowing trail between those times, which then hangs; o.drip: water drips off the hand and the elbow (out of the well);
  // o.bibAt: a blank bib pops onto the back of the hand; o.medalAt: a plain medal hangs from the wrist (o.medalYaw: which way it faces, prop-local);
  // o.s scales it all (1: shoulder at 2.1 m, links 3.0 and 2.6 m, a hand 1 m wide)
  chifRobot(o) {
    const s = o.s ?? 1, g = grp(), root = grp(); g.add(root); root.scale.setScalar(s);
    const OR = o.color || '#E8902A', DK = '#3A3D44', HC = o.handColor || '#454B55', L1 = 3.0, L2 = 2.6;
    let baseTop;
    if (o.base === 'pedestal') { root.add(at(cyl(0.95, 1.1, 0.5, DK, 12, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(cyl(1.12, 1.12, 0.06, '#E8C030', 12), 0, 0.03, 0)); baseTop = 0.5; }
    else {
      root.add(at(box(1.9, 0.6, 2.6, '#E8B030', { outline: 0.01 }), 0, 0.62, 0), at(box(1.92, 0.12, 0.3, '#2A2C30'), 0, 0.75, 1.3));
      for (let i = 0; i < 5; i++) root.add(at(box(0.18, 0.1, 0.31, '#F2D24A'), -0.8 + i * 0.4, 0.75, 1.31, 0, 0, 0.6));
      for (const sx of [-1, 1]) { root.add(at(box(0.5, 0.62, 2.9, '#2A2C30', { outline: 0.01 }), sx * 1.15, 0.33, 0)); for (const z of [-1.05, -0.35, 0.35, 1.05]) root.add(at(cyl(0.24, 0.24, 0.06, '#8A8F96', 10), sx * 1.42, 0.33, z, 0, 0, PI / 2)); }
      baseTop = 0.92;
    }
    const turret = grp(at(cyl(0.72, 0.8, 0.55, OR, 12, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(0.5, 0.75, 0.9, OR, { outline: 0.01 }), 0, 0.85, 0));
    turret.position.y = baseTop; root.add(turret);
    const hS = baseTop + 1.15;
    const shoulder = grp(at(cyl(0.38, 0.38, 0.95, DK, 12, { outline: 0.01 }), 0, 0, 0, 0, 0, PI / 2)); shoulder.position.y = 1.15; turret.add(shoulder);
    const upper = grp(), upperB = at(box(0.55, 0.55, 1, OR, { outline: 0.02 }), 0, 0, 0.5); upper.add(upperB, at(box(0.57, 0.12, 1, '#C8701E'), 0, 0.22, 0.5)); shoulder.add(upper);
    const elbow = grp(at(cyl(0.33, 0.33, 0.7, DK, 12, { outline: 0.01 }), 0, 0, 0, 0, 0, PI / 2)); turret.add(elbow);
    const fore = grp(), foreB = at(box(0.45, 0.45, 1, OR, { outline: 0.02 }), 0, 0, 0.5); fore.add(foreB, at(box(0.47, 0.1, 1, '#C8701E'), 0, 0.18, 0.5)); elbow.add(fore);
    const piston = grp(at(cyl(0.07, 0.07, 1, '#C9CED4', 6), 0, 0, 0.5, PI / 2, 0, 0)); turret.add(piston);
    const wrist = grp(); turret.add(wrist);
    wrist.add(at(cyl(0.3, 0.3, 0.32, DK, 12, { outline: 0.02 }), 0, 0, 0.0, PI / 2, 0, 0));
    const handG = grp(); handG.position.z = 0.16; wrist.add(handG);
    const M = mitten({ W: 1.0, T: 0.42, Lp: 0.85, Lf: 0.8, color: HC, sx: o.thumb ?? 1, ol: 0.035, back: '#5A616C' }); handG.add(M.g);
    for (const [x, z] of [[-0.3, 0.25], [0.3, 0.25], [-0.3, 0.6], [0.3, 0.6]]) M.g.add(at(cyl(0.05, 0.05, 0.03, '#C9CED4', 8), x, 0.215, z));
    const bib = grp(at(box(0.62, 0.48, 0.02, '#FAFAF6', { outline: 0.03 }), 0, 0, 0)); for (const [x, y] of [[-0.26, 0.19], [0.26, 0.19], [-0.26, -0.19], [0.26, -0.19]]) bib.add(at(sphere(0.025, '#C9CED4', 0), x, y, 0.015));
    bib.position.set(0, 0.225, 0.48); bib.rotation.x = -PI / 2; M.g.add(bib);
    const medal = grp(at(box(0.08, 0.5, 0.02, '#2F5FA8'), -0.09, -0.22, 0, 0, 0, 0.2), at(box(0.08, 0.5, 0.02, '#2F5FA8'), 0.09, -0.22, 0, 0, 0, -0.2), at(cyl(0.2, 0.2, 0.05, '#E8B830', 16, { outline: 0.03 }), 0, -0.6, 0.0, PI / 2, 0, 0), at(cyl(0.14, 0.14, 0.06, '#F2CC50', 16), 0, -0.6, 0.0, PI / 2, 0, 0));
    root.add(medal);
    const ghosts = [0.45, 0.28, 0.15].map(op => { const m = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.84, 0.95), new THREE.MeshBasicMaterial({ color: HC, transparent: true, opacity: op, depthWrite: false })); m.geometry.translate(0, -0.2, 0.47); m.castShadow = false; root.add(m); return m; });
    const P = (o.path && o.path.length) ? o.path : [{ t: 0, p: [0, 3.2, 3.2], hp: 0, curl: 1 }];
    const pose = t => {
      let i = 0; while (i < P.length - 1 && t >= P[i + 1].t) i++;
      const a = P[i], b = P[Math.min(i + 1, P.length - 1)], u = b === a ? 0 : (EASE[b.ease || 'inOut'] || EASE.inOut)(clamp01((t - a.t) / Math.max(1e-4, b.t - a.t)));
      const L = (k, d) => lerp(a[k] ?? d, b[k] ?? d, u);
      return { p: [0, 1, 2].map(j => lerp(a.p[j], b.p[j], u)), hp: L('hp', 0), curl: L('curl', 1), roll: L('roll', 0), st: L('st', 1), yaw: a.yaw != null && b.yaw != null ? lerp(a.yaw, b.yaw, u) : null };
    };
    const solve = q => {
      const [x, y, z] = q.p, yaw = q.yaw != null ? q.yaw : Math.atan2(x, z), rho = x * Math.sin(yaw) + z * Math.cos(yaw), v = y - hS, l1 = L1 * q.st, l2 = L2 * q.st;
      let d = Math.hypot(rho, v); d = Math.min(Math.max(d, Math.abs(l1 - l2) + 0.05), l1 + l2 - 0.02);
      const a = Math.atan2(v, rho), al = Math.acos(clamp01((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d))), th1 = a + al;
      const e = [l1 * Math.cos(th1), l1 * Math.sin(th1)], w = [d * Math.cos(a), d * Math.sin(a)], th2 = Math.atan2(w[1] - e[1], w[0] - e[0]);
      return { yaw, th1, th2, e, w, l1, l2 };
    };
    const local = (yaw, rho, h) => new THREE.Vector3(rho * Math.sin(yaw), h, rho * Math.cos(yaw));
    const handDir = (yaw, hp) => new THREE.Vector3(Math.sin(yaw) * Math.cos(hp), Math.sin(hp), Math.cos(yaw) * Math.cos(hp));
    const centre = t => { const q = pose(t), k = solve(q); return local(k.yaw, k.w[0], hS + k.w[1]).add(handDir(k.yaw, q.hp).multiplyScalar(0.55 + 0.25 * (1 - q.curl))); };
    const TR = o.trail, NS = 56, trailSegs = [];
    if (TR) { const col = TR.color || '#FFE27A', coreM = unlit('#FFFFFF'), haloM = unlit(col, { add: true, opacity: 0.55 }), wideM = unlit(col, { add: true, opacity: 0.2 });
      for (let i = 0; i < NS; i++) { const parts = [[0.07, coreM], [0.18, haloM], [0.4, wideM]].map(([r, m]) => { const x = new THREE.Mesh(new THREE.BoxGeometry(1, r, r), m); x.castShadow = false; x.renderOrder = 3; x.visible = false; root.add(x); return x; }); trailSegs.push(parts); }
      trailSegs.mats = [haloM, wideM]; }
    const tipS = glowSprite('#FFFFFF', 0.9, 1); tipS.visible = false; root.add(tipS);
    const drops = []; if (o.drip) for (let i = 0; i < 10; i++) { const m = sphere(0.07, '#CFE6F5', 1, { unique: true }); m.castShadow = false; m.scale.set(0.8, 1.3, 0.8); root.add(m); drops.push(m); }
    const sheen = o.drip ? at(new THREE.Mesh(new THREE.BoxGeometry(1.02, 0.02, 1.4), unlit('#BFE0F2', { opacity: 0.35 })), 0, 0.23, 0.65) : null; if (sheen) M.g.add(sheen);
    const X = new THREE.Vector3(1, 0, 0);
    g.userData.update = t => {
      const q = pose(t), k = solve(q);
      turret.rotation.y = k.yaw;
      upper.rotation.x = -k.th1; upperB.scale.set(1 / Math.sqrt(q.st), 1 / Math.sqrt(q.st), k.l1); upper.children[1].scale.z = k.l1; upper.children[1].position.z = k.l1 / 2; upperB.position.z = k.l1 / 2;
      elbow.position.set(0, 1.15 + k.e[1], k.e[0]); fore.rotation.x = -k.th2; foreB.scale.set(1 / Math.sqrt(q.st), 1 / Math.sqrt(q.st), k.l2); foreB.position.z = k.l2 / 2; fore.children[1].scale.z = k.l2; fore.children[1].position.z = k.l2 / 2;
      const pA = new THREE.Vector3(0, 1.15 - 0.35, 0.5), pB = new THREE.Vector3(0, 1.15 + k.e[1] * 0.55 - 0.3, k.e[0] * 0.55), pd = pB.clone().sub(pA);
      piston.position.copy(pA); piston.scale.z = pd.length(); piston.rotation.set(-Math.atan2(pd.y, pd.z), 0, 0);
      wrist.position.set(0, 1.15 + k.w[1], k.w[0]); wrist.rotation.set(-q.hp, 0, q.roll);
      let sq = 0; for (const h of list(o.hits)) { const u = t - h; if (u >= 0 && u < 0.45) sq += Math.exp(-u * 9) * Math.cos(u * 34); }
      handG.scale.set(1 + 0.28 * sq, 1 - 0.38 * sq, 1 + 0.18 * sq);
      M.set(q.curl, q.curl);
      const bu = o.bibAt == null ? 0 : outBack(clamp01((t - o.bibAt) / 0.2)); bib.visible = bu > 0.01; bib.scale.setScalar(Math.max(0.01, bu));
      const mu = o.medalAt == null ? 0 : outBack(clamp01((t - o.medalAt) / 0.2)); medal.visible = mu > 0.01; medal.scale.setScalar(Math.max(0.01, mu));
      if (medal.visible) { const wp = local(k.yaw, k.w[0], hS + k.w[1]); medal.position.copy(wp).add(new THREE.Vector3(0, -0.28, 0)); medal.rotation.set(0, o.medalYaw ?? k.yaw, 0.12 * Math.sin((t - o.medalAt) * 6) * Math.exp(-(t - o.medalAt) * 1.5)); }
      const inSm = list(o.smear).some(([a, b]) => t >= a && t <= b);
      ghosts.forEach((m, i) => { m.visible = inSm; if (!inSm) return; const tq = t - 0.03 * (i + 1), qq = pose(tq), kk = solve(qq); m.position.copy(local(kk.yaw, kk.w[0], hS + kk.w[1])); m.rotation.set(0, 0, 0); m.rotation.order = 'YXZ'; m.rotation.set(-qq.hp, kk.yaw, 0); });
      if (TR) { const t1 = Math.min(t, TR.t1), on = t >= TR.t0; let prev = on ? centre(TR.t0) : null;
        trailSegs.forEach((parts, i) => { const tb = TR.t0 + (t1 - TR.t0) * (i + 1) / NS, cur = on ? centre(tb) : null, ok = on && t1 > TR.t0;
          parts.forEach(m => { m.visible = ok; if (!ok) return; const d = cur.clone().sub(prev), l = d.length(); m.scale.x = Math.max(0.001, l + 0.04); m.position.copy(prev).addScaledVector(d, 0.5); if (l > 1e-5) m.quaternion.setFromUnitVectors(X, d.normalize()); });
          prev = cur; });
        const pulse = t > TR.t1 ? 0.75 + 0.25 * Math.sin((t - TR.t1) * 7) : 1; trailSegs.mats[0].opacity = 0.55 * pulse; trailSegs.mats[1].opacity = 0.2 * pulse;
        tipS.visible = t >= TR.t0 && t <= TR.t1; if (tipS.visible) tipS.position.copy(centre(t)); }
      drops.forEach((m, i) => { const per = 0.55, u = ((t + i * 0.137) % per) / per, src = i % 3 === 2 ? local(k.yaw, k.e[0], hS + k.e[1] - 0.3) : local(k.yaw, k.w[0], hS + k.w[1]).add(handDir(k.yaw, q.hp).multiplyScalar(0.3 + 0.12 * i)).add(new THREE.Vector3(0.3 * (hsh(i) - 0.5), -0.35, 0.3 * (hsh(i + 3) - 0.5)));
        m.position.set(src.x, Math.max(0.03, src.y - 4.9 * Math.pow(u * per, 2) * 2.2), src.z); m.visible = src.y - 4.9 * Math.pow(u * per, 2) * 2.2 > 0.05; });
    };
    g.userData.update(0); return g;
  },

  // An interior room for the white void (pivot at the floor's middle): a floor o.w x o.d (raised 1 cm), a back wall at z = -o.d / 2 and two side walls
  // o.h high, a band of o.band up to o.bandH with a trim, o.lights ceiling light panels at o.lightY; o.stripes: yellow floor lines (a factory);
  // o.beams: steel columns along the side walls (a factory); o.sign [text, x, y, w, h]: a plaque on the back wall (o.signBg / o.signFg)
  chifRoom(o) {
    const w = o.w ?? 12, d = o.d ?? 10, h = o.h ?? 3.4, g = grp(), back = -d / 2;
    g.add(at(box(w, 0.02, d, o.floor || '#B9B4AA'), 0, 0.0, 0));
    g.add(at(box(w, h, 0.2, o.wall || '#D9DCD8', { outline: 0.004 }), 0, h / 2, back - 0.1));
    for (const s of [-1, 1]) g.add(at(box(0.2, h, d, o.wall || '#D9DCD8'), s * (w / 2 + 0.1), h / 2, 0));
    if (o.band) { const bh = o.bandH ?? 1.0; g.add(at(box(w, bh, 0.04, o.band), 0, bh / 2, back + 0.02), at(box(w, 0.08, 0.08, o.trim || '#3A3D44'), 0, bh + 0.04, back + 0.04)); for (const s of [-1, 1]) g.add(at(box(0.04, bh, d, o.band), s * (w / 2 - 0.02), bh / 2, 0)); }
    for (let i = 0; i < (o.lights ?? 0); i++) { const x = (i - ((o.lights ?? 1) - 1) / 2) * (w / Math.max(1, o.lights)); g.add(at(box(1.4, 0.06, 0.3, '#FFFFFF', { emissive: '#FFF6DA', noGrain: true }), x, o.lightY ?? h - 0.05, back + d * 0.35)); }
    if (o.stripes) for (const x of [-w * 0.3, w * 0.3]) g.add(at(box(0.14, 0.004, d * 0.9, '#E8C030'), x, 0.012, 0));
    if (o.hazard) { const hz = canvasPlane(w, 0.3, (c, W, H) => { c.fillStyle = '#E8C030'; c.fillRect(0, 0, W, H); c.fillStyle = '#1E1E1E'; for (let x = -H; x < W; x += H * 1.4) { c.beginPath(); c.moveTo(x, H); c.lineTo(x + H * 0.7, 0); c.lineTo(x + H * 1.4, 0); c.lineTo(x + H * 0.7, H); c.fill(); } }, { res: 1024 }); hz.position.set(0, o.hazardY ?? 1.4, back + 0.03); g.add(hz); }
    if (o.beams) for (const s of [-1, 1]) for (let z = back + 1; z < d / 2; z += 3) g.add(at(box(0.35, h, 0.35, '#5E6670', { outline: 0.01 }), s * (w / 2 - 0.25), h / 2, z));
    if (o.sign) { const [txt, x, y, sw, sh] = o.sign; g.add(at(canvasPlane(sw, sh, (c, W, H) => { c.fillStyle = o.signBg || '#2E4563'; c.fillRect(0, 0, W, H); c.fillStyle = o.signFg || '#F2F2EE'; let fs = H * 0.6; c.font = `900 ${fs}px Arial`; const tw = c.measureText(txt).width; if (tw > W * 0.9) { fs *= W * 0.9 / tw; c.font = `900 ${fs}px Arial`; } c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(txt, W / 2, H * 0.54); }, { res: 768, emissive: 0.15 }), x, y, back + 0.04)); }
    return g;
  },

  // Welding sparks (pivot at the torch tip): a blue-white flicker and a spray of short orange streaks that fall, looping; o.s its size, o.ph its phase
  chifSparks(o) {
    const s = o.s ?? 1, g = grp(), fl = glowSprite('#CFE6FF', 0.7 * s, 0.9); g.add(fl);
    const ZA = new THREE.Vector3(0, 0, 1), st = []; for (let i = 0; i < 14; i++) { const m = new THREE.Mesh(new THREE.BoxGeometry(0.012 * s, 0.012 * s, 0.09 * s), unlit(i % 3 ? '#FFB43A' : '#FFF2B0')); m.castShadow = false; g.add(m); st.push(m); }
    g.userData.update = t => { const k = Math.sin(t * 37 + (o.ph ?? 0)) * 0.5 + 0.5; fl.material.opacity = 0.55 + 0.4 * k; fl.scale.setScalar((0.55 + 0.35 * k) * s);
      st.forEach((m, i) => { const per = 0.42, u = ((t + i * 0.031 + (o.ph ?? 0)) % per) / per, a = hsh(i) * TAU, v = (0.9 + hsh(i + 4)) * s; const x = Math.cos(a) * v * u * 0.6, z = Math.sin(a) * v * u * 0.6, y = 0.5 * v * u - 1.6 * u * u * s;
        m.position.set(x, y, z); const dv = new THREE.Vector3(Math.cos(a) * 0.6, 0.5 - 3.2 * u, Math.sin(a) * 0.6).normalize(); m.quaternion.setFromUnitVectors(ZA, dv); m.visible = u < 0.85; }); };
    g.userData.update(0); return g;
  },

  // A welder's mask flipped down (attach to the head joint, offset [0, 0, 0]): a dark green shell over the face with a black visor window
  chifWeldMask(o) {
    const w = o.w ?? 0.31, g = grp(); g.add(at(box(w + 0.04, 0.46, 0.08, '#2F4A3A', { outline: 0.03 }), 0, 0.26, 0.15), at(box(w * 0.6, 0.12, 0.02, '#0E1012'), 0, 0.31, 0.2), at(box(w + 0.06, 0.06, 0.26, '#2F4A3A'), 0, 0.52, 0.03));
    return g;
  },

  // A box factory seen from outside (pivot at the middle of its foot, the front +Z): o.w x o.d, o.floors storeys of o.fh, rows of blue windows, a
  // flat roof with a chimney and « USINE »; at o.sinkAt it slides o.sinkFloors storeys down into the ground (the field hides what goes under) over
  // o.sinkDur with a jolt, and a ring of dust rolls out along the ground; o.open [[floor, col], ...]: windows left open and dark (workers lean out)
  chifFactoryBox(o) {
    const w = o.w ?? 14, d = o.d ?? 9, nf = o.floors ?? 4, fh = o.fh ?? 3.2, H = nf * fh, g = grp(), body = grp(); g.add(body);
    const WALL = o.color || '#CBD2D8';
    body.add(at(box(w, H, d, WALL, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(w + 0.3, 0.5, d + 0.3, '#8E969E'), 0, H + 0.25, 0));
    const open = (o.open || []).map(x => x.join(','));
    const nc = Math.floor(w / 2.2);
    for (let f = 0; f < nf; f++) {
      body.add(at(box(w + 0.04, 0.16, d + 0.04, '#3F6FA8'), 0, f * fh + 0.08, 0));
      for (let c = 0; c < nc; c++) { const x = -w / 2 + (c + 0.5) * w / nc, y = f * fh + fh * 0.55, isOpen = open.includes(`${f},${c}`);
        body.add(at(box(1.5, 1.45, 0.08, '#F2F2EE'), x, y, d / 2 + 0.02), at(box(1.3, 1.25, 0.06, isOpen ? '#1A1C20' : '#5E8FC2', isOpen ? {} : { emissive: '#1E3A5A' }), x, y, d / 2 + 0.05));
        if (!isOpen) body.add(at(box(0.05, 1.25, 0.07, '#F2F2EE'), x, y, d / 2 + 0.06)); }
      for (let c = 0; c < Math.floor(d / 2.2); c++) { const z = -d / 2 + (c + 0.5) * d / Math.floor(d / 2.2), y = f * fh + fh * 0.55; body.add(at(box(0.08, 1.45, 1.5, '#F2F2EE'), w / 2 + 0.02, y, z), at(box(0.06, 1.25, 1.3, '#5E8FC2', { emissive: '#1E3A5A' }), w / 2 + 0.05, y, z)); }
    }
    body.add(at(cyl(0.6, 0.75, 7, '#B04A3A', 10, { pivot: 'bottom', outline: 0.01 }), w * 0.3, H, -d * 0.2), at(cyl(0.65, 0.65, 0.4, '#F2F2EE', 10), w * 0.3, H + 6.2, -d * 0.2));
    body.add(at(canvasPlane(5.5, 1.3, (c, W, Hc) => { c.fillStyle = '#2E4563'; c.fillRect(0, 0, W, Hc); c.fillStyle = '#F2F2EE'; c.font = `900 ${Hc * 0.66}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('USINE', W / 2, Hc * 0.55); }, { res: 512, emissive: 0.1 }), -w * 0.15, H + 1.2, d / 2 - 0.3));
    body.add(at(box(5.7, 1.5, 0.15, '#2A2D33'), -w * 0.15, H + 1.2, d / 2 - 0.4), at(box(0.15, 1.0, 0.15, '#5A5E66', { pivot: 'bottom' }), -w * 0.15 - 2, H + 0.4, d / 2 - 0.4), at(box(0.15, 1.0, 0.15, '#5A5E66', { pivot: 'bottom' }), -w * 0.15 + 2, H + 0.4, d / 2 - 0.4));
    const dust = []; for (let i = 0; i < 34; i++) { const m = softSprite(i % 3 ? '#D9CDB4' : '#C4B696', 0); m.visible = false; g.add(m); dust.push(m); }
    const rub = []; for (let i = 0; i < 26; i++) { const a = i / 26 * TAU, r = 1.0; const m = box(0.5 + 0.4 * hsh(i), 0.3 + 0.3 * hsh(i + 1), 0.5, i % 2 ? '#7A6A55' : '#8E8070', { outline: 0.02 }); const ex = Math.cos(a), ez = Math.sin(a); m.position.set(ex * (w / 2 + 0.4) * r, 0.1, ez * (d / 2 + 0.4) * r); m.rotation.set(hsh(i) - 0.5, a, hsh(i + 2) - 0.5); m.visible = false; g.add(m); rub.push(m); }
    const drop = (o.sinkFloors ?? 2) * fh;
    g.userData.update = t => {
      const u = o.sinkAt == null ? 0 : (t - o.sinkAt) / (o.sinkDur ?? 0.45);
      const e = u <= 0 ? 0 : u < 1 ? Math.pow(u, 1.6) : 1 + 0.035 * Math.exp(-(u - 1) * 5) * Math.sin((u - 1) * 14);
      body.position.y = -drop * e; body.position.x = u > 0 && u < 1.6 ? 0.08 * Math.sin(t * 70) * (1 - clamp01(u / 1.6)) : 0;
      rub.forEach(m => { m.visible = u > 0.6; });
      dust.forEach((m, i) => { const v = (t - (o.sinkAt ?? 99) - (o.sinkDur ?? 0.45) * 0.6 - 0.015 * i) / 1.8; m.visible = v > 0 && v < 1; if (!m.visible) return; const a = i / dust.length * TAU + 0.2 * hsh(i), e2 = 1 - Math.pow(1 - v, 2.2);
        m.position.set(Math.cos(a) * (w / 2 + 0.5 + 6 * e2), 0.8 + 1.6 * e2 + 0.6 * hsh(i), Math.sin(a) * (d / 2 + 0.5 + 6 * e2)); const sc = (2.4 + 2 * hsh(i + 3)) * (0.7 + 0.8 * e2); m.scale.set(sc, sc * 0.75, 1); m.material.opacity = 0.9 * (v < 0.1 ? v / 0.1 : 1 - smooth((v - 0.3) / 0.7)); });
    };
    g.userData.update(0); return g;
  },

  // His house (pivot at the middle of its foot, the front +Z): two storeys o.fh (2.9) each, o.w x o.d, pastel walls (o.color), a tiled gable roof, a
  // teal door with a little porch roof at o.doorX, ground-floor windows with shutters, two first-floor windows
  chifHouse(o) {
    const w = o.w ?? 7, d = o.d ?? 6, fh = o.fh ?? 2.9, g = grp(), C = o.color || '#F2D9B8', T = o.trim || '#FFFFFF', SH = o.shutter || '#4E7FA8', dx = o.doorX ?? -1.2;
    g.add(at(box(w, fh * 2, d, C, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(w + 0.06, 0.12, d + 0.06, T), 0, fh, 0));
    const roof = new THREE.Shape(); roof.moveTo(-w / 2 - 0.4, 0); roof.lineTo(0, 2.4); roof.lineTo(w / 2 + 0.4, 0); roof.lineTo(-w / 2 - 0.4, 0);
    const rg = new THREE.ExtrudeGeometry(roof, { depth: d + 0.6, bevelEnabled: false }); rg.translate(0, 0, -(d + 0.6) / 2); const rm = new THREE.Mesh(rg, mat(o.roof || '#B5523A')); rm.position.y = fh * 2; rm.castShadow = rm.receiveShadow = true; addOutline(rm, 0.01); g.add(rm);
    const gab = new THREE.Shape(); gab.moveTo(-w / 2, 0); gab.lineTo(0, 2.1); gab.lineTo(w / 2, 0); gab.lineTo(-w / 2, 0); const gm = new THREE.Mesh(new THREE.ShapeGeometry(gab), mat(C)); gm.position.set(0, fh * 2, d / 2 + 0.01); g.add(gm);
    const win = (x, y, sh) => { g.add(at(box(1.1, 1.25, 0.06, T), x, y, d / 2 + 0.02), at(box(0.95, 1.1, 0.05, '#7FAFD6', { emissive: '#21405E' }), x, y, d / 2 + 0.05), at(box(0.04, 1.1, 0.06, T), x, y, d / 2 + 0.06));
      if (sh) for (const s of [-1, 1]) g.add(at(box(0.45, 1.3, 0.05, SH), x + s * 0.8, y, d / 2 + 0.03)); };
    win(1.6, 1.45, true); win(dx, fh + 1.45, true); win(1.6, fh + 1.45, true);
    g.add(at(box(1.2, 2.2, 0.08, T), dx, 1.1, d / 2 + 0.02), at(box(1.0, 2.05, 0.08, o.door || '#2F7A72', { outline: 0.01 }), dx, 1.03, d / 2 + 0.05), at(sphere(0.05, '#E8C030', 0), dx + 0.35, 1.0, d / 2 + 0.1));
    g.add(at(box(1.8, 0.1, 0.9, '#7A3A2A'), dx, 2.45, d / 2 + 0.45, -0.25, 0, 0), at(box(1.6, 0.16, 0.8, '#C9C2B2'), dx, 0.08, d / 2 + 0.4));
    return g;
  },

  // A blank race bib to pin on a chest (pivot at its middle, front +Z): white, no number, four safety pins; o.w x o.h (0.28 x 0.22)
  chifBib(o) {
    const w = o.w ?? 0.28, h = o.h ?? 0.22, g = grp(at(box(w, h, 0.01, '#FAFAF6', { outline: 0.03 }), 0, 0, 0));
    for (const [x, y] of [[-1, 1], [1, 1], [-1, -1], [1, -1]]) g.add(at(sphere(0.012, '#B9BEC4', 0), x * w * 0.4, y * h * 0.38, 0.008));
    return g;
  },

  // A plain medal (pivot at the top of the ribbon, hanging down): a plain blue ribbon in a V and a gold disc with a raised rim, no emblem; o.s
  chifMedal(o) {
    const s = o.s ?? 1, g = grp(at(box(0.035, 0.2, 0.008, '#2F5FA8'), -0.04, -0.09, 0, 0, 0, 0.2), at(box(0.035, 0.2, 0.008, '#2F5FA8'), 0.04, -0.09, 0, 0, 0, -0.2), at(cyl(0.075, 0.075, 0.02, '#E8B830', 16, { outline: 0.04 }), 0, -0.24, 0, PI / 2, 0, 0), at(cyl(0.052, 0.052, 0.024, '#F2CC50', 16), 0, -0.24, 0, PI / 2, 0, 0));
    g.scale.setScalar(s); return g;
  },

  // An A-frame stepladder (pivot at the floor, the steps toward +Z): o.h (1.8) high, aluminium, five treads and a top cap
  chifStepladder(o) {
    const h = o.h ?? 1.8, g = grp(), A = '#C9CED4', sp = 0.55;
    for (const s of [-1, 1]) { g.add(rod([s * 0.28, 0, sp], [s * 0.24, h, 0.04], 0.03, A), rod([s * 0.28, 0, -sp], [s * 0.24, h, -0.04], 0.03, A)); }
    for (let i = 1; i <= 5; i++) { const f = i / 6; g.add(at(box(0.5, 0.04, 0.14, '#9AA0A8', { outline: 0.02 }), 0, h * f, sp * (1 - f) + 0.04 * f)); }
    g.add(at(box(0.56, 0.08, 0.3, '#E8822E', { outline: 0.02 }), 0, h + 0.03, 0));
    return g;
  },

  // An apron (attach to the torso joint, offset [0, -0.1, 0.135] like a shirt front): a bib over the chest and a skirt down to the knees, pale
  // yellow with small red dots and a red trim, its strings round the neck; o.h (1.15), o.w (0.4)
  chifApron(o) {
    const w = o.w ?? 0.4, h = o.h ?? 1.15, g = grp();
    const p = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#F6E6A6'; c.beginPath(); c.moveTo(W * 0.22, 0); c.lineTo(W * 0.78, 0); c.lineTo(W * 0.78, H * 0.38); c.lineTo(W, H * 0.44); c.lineTo(W * 0.96, H); c.lineTo(W * 0.04, H); c.lineTo(0, H * 0.44); c.lineTo(W * 0.22, H * 0.38); c.closePath(); c.fill();
      c.save(); c.clip(); c.fillStyle = '#D8463A'; for (let y = 0; y < H; y += W * 0.12) for (let x = (y / (W * 0.12)) % 2 ? W * 0.06 : 0; x < W; x += W * 0.12) { c.beginPath(); c.arc(x, y, W * 0.022, 0, TAU); c.fill(); } c.restore();
      c.strokeStyle = '#C23A30'; c.lineWidth = W * 0.035; c.stroke(); c.fillStyle = '#F2D27A'; c.fillRect(W * 0.3, H * 0.58, W * 0.4, H * 0.14); c.strokeRect(W * 0.3, H * 0.58, W * 0.4, H * 0.14); }, { res: 256, transparent: true });
    p.position.set(0, 0.62 - h / 2 + 0.0, 0); g.add(p);
    return g;
  },
};
