// « La fuite » (story 99, cycle 53): this man reported a leak and the secret service landed: a leak under the sink. An hour later his sink was
// classified; every drop was filed. The drops fell in morse and gave the palace password; the palace changed it, the next drop gave the new one.
// The press calls it the leak of the century; the interior minister resigned (he had let it run); the president ordered it sealed: the army
// drowned the sink in concrete, the fridge too. The leak came out at the neighbour's below, arrested for receiving. The service sent its best
// plumber: a new washer, ten cents; invoice, three million, classified. The tap no longer leaks. It listens.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time. Every name
// starts with `fu` (props.js merges all the story tables into one: a plain name could override another story's).
import * as THREE from 'three';
import { box, cyl, sphere, mat, addOutline } from './style.js';
import { grp, at, canvasPlane, rod } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = x => { const u = clamp01(x), c = 1.70158; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const noShadow = m => { m.traverse(c => { c.castShadow = false; }); return m; };
// a value keyed in time: keys [[t, v], ...] (sorted), eased (smoothstep) between keys
function kv(keys, t, def = 0) {
  if (keys == null) return def;
  if (typeof keys === 'number') return keys;
  if (!keys.length) return def;
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) { const [a, va] = keys[i], [b, vb] = keys[i + 1]; if (t < b) return va + (vb - va) * smooth((t - a) / Math.max(1e-4, b - a)); }
  return keys[keys.length - 1][1];
}
const popS = (t, t0, d = 0.22) => t < t0 ? 0 : outBack((t - t0) / d);

// a fat glossy drop (pivot at its middle, tip up): a blue sphere drawn into a cone at the top, a white highlight, an ink outline; s its height
function dropMesh(s = 0.3, color = '#3FA4E8') {
  const g = grp(), m = mat(color, { emissive: '#14507A' });
  const b = new THREE.Mesh(new THREE.SphereGeometry(s * 0.32, 14, 10), m); b.position.y = -s * 0.1; addOutline(b, 0.05);
  const tip = new THREE.Mesh(new THREE.ConeGeometry(s * 0.27, s * 0.42, 14, 1, true), m); tip.position.y = s * 0.24; addOutline(tip, 0.05);
  const hl = noShadow(at(new THREE.Mesh(new THREE.SphereGeometry(s * 0.07, 8, 6), new THREE.MeshBasicMaterial({ color: '#FFFFFF' })), -s * 0.12, s * 0.0, s * 0.25));
  g.add(b, tip, hl); return g;
}

export const FUITE_PROPS = {
  // The drop (pivot at its middle): head-sized, glossy blue, tip up (see dropMesh); o.s (0.3 m tall); o.fall [t0, period, drop m]: it swells at the
  // pivot then falls o.drop metres and splashes, looping every period from t0 (or o.once); o.eyes: two dot eyes and a flat mouth (the mugshot)
  fuDrop(o) {
    const s = o.s ?? 0.3, g = grp(), d = dropMesh(s, o.color); g.add(d);
    if (o.eyes) for (const x of [-1, 1]) d.add(at(sphere(s * 0.035, '#14161A', 1), x * s * 0.09, -s * 0.05, s * 0.3));
    if (o.eyes) d.add(at(box(s * 0.12, s * 0.015, s * 0.01, '#14161A'), 0, -s * 0.16, s * 0.29));
    const spl = grp(); for (let i = 0; i < 6; i++) { const m = noShadow(sphere(s * 0.06, o.color || '#3FA4E8', 0)); spl.add(m); } g.add(spl);
    g.userData.update = t => {
      if (!o.fall) { d.position.set(0, 0, 0); spl.visible = false; d.scale.setScalar(1 + 0.03 * Math.sin(t * 3)); return; }
      const [t0, per, H] = o.fall, tt = t - t0;
      if (tt < 0) { d.visible = false; spl.visible = false; return; }
      const n = Math.floor(tt / per), u = (tt % per) / per; if (o.once && n > 0) { d.visible = false; spl.visible = false; return; }
      const grow = 0.45, fall = 0.75, sq = 0.3 * (1 - fall);
      d.visible = u < fall + sq; spl.visible = u >= fall && u < 0.98;
      if (u < grow) { const k = smooth(u / grow); d.scale.set(0.4 + 0.6 * k, (0.4 + 0.6 * k) * (1 + 0.25 * k), 0.4 + 0.6 * k); d.position.y = -0.1 * s * k; }
      else if (u < fall) { const v = (u - grow) / (fall - grow), st = 1 + 0.9 * v * v; d.scale.set(0.9 / Math.sqrt(st), 1.15 * st, 0.9 / Math.sqrt(st)); d.position.y = -0.1 * s - H * v * v; }   // stretched by its speed
      else { const w = clamp01((u - fall) / sq), q = 1 - w; d.scale.set(1.5 + 0.9 * w, 0.28 * q + 0.04, 1.5 + 0.9 * w); d.position.y = -H - 0.38 * s; }   // the squash: a flat puddle spreading out
      const v2 = (u - fall) / (1 - fall), hang = Math.sqrt(Math.max(0, Math.sin(Math.min(1, v2) * PI)));
      spl.children.forEach((m, i) => { const a = i / 6 * TAU; m.position.set(Math.cos(a) * s * 0.9 * v2, -H - 0.3 * s + s * 0.9 * hang, Math.sin(a) * s * 0.6 * v2); m.scale.setScalar(1.3 * (1 - v2 * v2)); });   // the splash flies up and hangs
    };
    g.userData.update(-1); return g;
  },

  // A dirty plate (pivot at its middle, flat in the XZ plane; attach to a hand with rot [PI/2, 0, 0] to hold it up): white, a rim, brown smears
  fuPlate(o) {
    const r = o.r ?? 0.14, g = grp(at(cyl(r, r * 0.8, 0.02, '#F6F4EE', 16, { outline: 0.04 }), 0, 0, 0));
    const sm = canvasPlane(r * 1.4, r * 1.4, (c, W, H) => { c.clearRect(0, 0, W, H); c.fillStyle = 'rgba(140,90,40,0.85)'; for (const [x, y, rr] of [[0.4, 0.45, 0.16], [0.62, 0.6, 0.1], [0.35, 0.68, 0.07], [0.6, 0.33, 0.06]]) { c.beginPath(); c.ellipse(W * x, H * y, W * rr, H * rr * 0.7, 0.5, 0, TAU); c.fill(); } }, { res: 128, transparent: true });
    sm.rotation.x = -PI / 2; sm.position.y = 0.011; g.add(sm);
    if (o.cleanAt != null) { sm.material.transparent = true; g.userData.update = t => { const u = smooth((t - o.cleanAt) / (o.cleanDur ?? 0.6)); sm.material.opacity = 1 - u; sm.visible = u < 0.99; }; g.userData.update(-1); }   // o.cleanAt: the stains rinse away
    return g;
  },

  // A small saucepan (pivot at the floor in its middle): steel pot o.r (0.13), a long dark handle along +X, a little water inside
  fuPan(o) {
    const r = o.r ?? 0.13, g = grp(at(cyl(r, r * 0.92, r * 0.9, '#C9CED4', 16, { pivot: 'bottom', outline: 0.02 }), 0, 0, 0), at(cyl(r * 0.94, r * 0.94, 0.01, '#5FB7E8', 16), 0, r * 0.5, 0));
    g.add(at(box(r * 2.2, 0.03, 0.05, '#2A2C31', { outline: 0.02 }), r * 1.9, r * 0.82, 0));
    return g;
  },

  // A giant padlock (pivot at its body's middle, front +Z): a brass body o.w (0.45) wide, a dark keyhole, a steel shackle; o.openAt: the shackle
  // pops up and swings open (with a jolt of the body); o.shutAt: it snaps shut (from open)
  fuPadlock(o) {
    const w = o.w ?? 0.45, g = grp(), k = grp(); g.add(k);
    k.add(at(box(w, w * 0.8, w * 0.32, '#D9A93A', { outline: 0.03 }), 0, 0, 0), at(box(w * 0.92, w * 0.06, w * 0.33, '#B88A26'), 0, w * 0.25, 0));
    k.add(at(cyl(w * 0.07, w * 0.07, 0.01, '#1E2126', 10), 0, w * 0.02, w * 0.165, PI / 2), at(box(w * 0.05, w * 0.14, 0.01, '#1E2126'), 0, -w * 0.08, w * 0.165));
    const sh = grp(); sh.position.set(-w * 0.28, w * 0.4, 0); k.add(sh);
    const arc = new THREE.Mesh(new THREE.TorusGeometry(w * 0.28, w * 0.065, 8, 16, PI), mat('#C9CED4')); arc.position.set(w * 0.28, w * 0.18, 0); addOutline(arc, 0.04); sh.add(arc);
    for (const x of [0, w * 0.56]) sh.add(at(cyl(w * 0.065, w * 0.065, w * 0.2, '#C9CED4', 10, { outline: 0.04 }), x, w * 0.08, 0));
    g.userData.update = t => {
      let open = o.open ? 1 : 0;
      if (o.openAt != null && t >= o.openAt) open = smooth((t - o.openAt) / 0.12);
      if (o.shutAt != null && t >= o.shutAt) open = 1 - smooth((t - o.shutAt) / 0.08);
      sh.position.y = w * 0.4 + w * 0.22 * open; sh.rotation.y = -1.2 * Math.max(0, open - 0.6) / 0.4;
      const j = o.openAt != null && t >= o.openAt && t < o.openAt + 0.4 ? 0.08 * Math.exp(-8 * (t - o.openAt)) * Math.sin((t - o.openAt) * 40) : 0; k.rotation.z = j;
    };
    g.userData.update(-1); return g;
  },

  // Black-and-yellow tape (pivot at its middle, faces +Z): a band o.len (2) long, o.w (0.12) wide, tilted o.tilt (rad); o.wrapAt: it unrolls along
  // its length from its left end over 0.35 s
  fuTape(o) {
    const L = o.len ?? 2, w = o.w ?? 0.12, g = grp(), k = grp(); g.add(k);
    const pl = canvasPlane(L, w, (c, W, H) => { c.fillStyle = '#F2C230'; c.fillRect(0, 0, W, H); c.fillStyle = '#16181C'; for (let x = -H; x < W; x += H * 1.6) { c.beginPath(); c.moveTo(x, H); c.lineTo(x + H * 0.8, 0); c.lineTo(x + H * 1.6, 0); c.lineTo(x + H * 0.8, H); c.fill(); } }, { res: 512 });
    pl.position.x = L / 2; k.add(pl); k.position.x = -L / 2; g.rotation.z = o.tilt ?? 0;
    g.userData.update = t => { const u = o.wrapAt == null ? 1 : smooth((t - o.wrapAt) / 0.35); k.scale.x = Math.max(0.001, u); k.visible = u > 0.01; };
    g.userData.update(-1); return g;
  },

  // A kitchen (pivot at the floor in the middle of the back wall's foot; the room opens toward +Z): pale green walls with a tiled band, a counter
  // 3 m long along the back wall (top at 0.92) with a steel sink at x 0 (opening 0.6 x 0.42), the cupboard under the sink with two doors that
  // open (o.doors [[t, 0..1]]; open shows the dark inside, the U-trap pipe and its drip point userData.drip), a window over the sink, a wall phone
  // at x -1.0 (userData.phone the handset's rest), a white fridge at x -2.1 with one magnet, a door at x 2.0 in the side wall (o.burstAt: it flies
  // open), o.tape (bands round the sink), o.lock (a giant padlock on the cupboard doors), o.tap (false: no tap, a scene supplies fuTap)
  fuKitchen(o) {
    const g = grp(), W = o.w ?? 7, WALL = o.wall || '#CFE3D6', BAND = '#F1F3EE', WH = o.wallH ?? 3.2;   // o.wallH: taller walls so no sky shows over them
    g.add(at(box(W, WH, 0.12, WALL, { pivot: 'bottom' }), 0, 0, -0.06), at(box(W, 0.9, 0.02, BAND), 0, 1.0 + 0.45, 0.005));
    for (let i = 0; i < 20; i++) g.add(at(box(0.008, 0.9, 0.01, '#D8DDD6'), -W / 2 + 0.35 * i, 1.45, 0.012));
    g.add(at(box(0.12, WH, 6, WALL, { pivot: 'bottom' }), W / 2, 0, 3), at(box(0.12, WH, 6, WALL, { pivot: 'bottom' }), -W / 2, 0, 3));
    const fl = new THREE.Mesh(new THREE.PlaneGeometry(W, 6), mat('#E9DCC4')); fl.rotation.x = -PI / 2; fl.position.set(0, 0.002, 3); fl.receiveShadow = true; g.add(fl);
    // counter with the sink
    const C = '#F4F0E6', T = '#B7C2C9';
    g.add(at(box(1.0, 0.86, 0.6, C, { pivot: 'bottom', outline: 0.006 }), -1.0, 0.06, 0.3), at(box(0.9, 0.86, 0.6, C, { pivot: 'bottom', outline: 0.006 }), 0.95, 0.06, 0.3));
    g.add(at(box(3.0, 0.06, 0.66, '#3E4A54'), 0, 0.03, 0.3));
    for (const x of [-1.0, 0.95]) g.add(at(box(0.02, 0.7, 0.01, '#C9C2B2'), x, 0.5, 0.605), at(box(0.12, 0.025, 0.03, '#8A939B'), x + 0.18, 0.72, 0.62));
    // the top with a hole for the basin
    for (const [x, w] of [[-0.95, 1.1], [0.95, 1.1]]) g.add(at(box(w, 0.05, 0.66, T, { outline: 0.004 }), x, 0.92, 0.33));
    g.add(at(box(0.8, 0.05, 0.12, T), 0, 0.92, 0.6), at(box(0.8, 0.05, 0.12, T), 0, 0.92, 0.06));
    g.add(at(box(0.6, 0.2, 0.42, '#9AA3AB'), 0, 0.82, 0.33), at(box(0.56, 0.02, 0.38, '#6E7880'), 0, 0.93, 0.33));
    // the cupboard under the sink: dark inside, the trap, two doors
    g.add(at(box(0.8, 0.86, 0.02, '#2A2E33'), 0, 0.49, 0.04), at(box(0.8, 0.02, 0.58, '#3A3F45'), 0, 0.07, 0.31));
    for (const x of [-0.41, 0.41]) g.add(at(box(0.02, 0.86, 0.6, C), x, 0.49, 0.3));
    g.add(rod([0, 0.72, 0.33], [0, 0.5, 0.33], 0.035, '#C9CED4'), rod([0, 0.5, 0.33], [0.16, 0.5, 0.33], 0.035, '#C9CED4'), rod([0.16, 0.5, 0.33], [0.16, 0.6, 0.33], 0.035, '#C9CED4'), rod([0.16, 0.6, 0.33], [0.16, 0.6, 0.06], 0.035, '#C9CED4'));
    g.userData.drip = [0, 0.48, 0.33];
    const doors = [-1, 1].map(s => { const h = grp(at(box(0.39, 0.82, 0.025, C, { outline: 0.006 }), -s * 0.195, 0, 0), at(box(0.025, 0.12, 0.03, '#8A939B'), -s * 0.34, 0.12, 0.02)); h.position.set(s * 0.4, 0.49, 0.615); g.add(h); return { h, s }; });
    const subs = [];   // nested animated props: their update is called from this one
    if (o.lock) { const lk = FUITE_PROPS.fuPadlock({ w: 0.36 }); lk.position.set(0, 0.6, 0.72); g.add(lk); }
    if (o.tape) for (const [y, tl] of [[0.62, 0.32], [0.38, -0.3]]) { const tp = FUITE_PROPS.fuTape({ len: 1.5, w: 0.17, tilt: tl, wrapAt: o.tape === true ? null : o.tape }); tp.position.set(0, y, 0.66); g.add(tp); subs.push(tp); }
    if (o.tape) { const tp2 = FUITE_PROPS.fuTape({ len: 2.2, w: 0.15, wrapAt: o.tape === true ? null : o.tape }); tp2.position.set(0, 0.96, 0.67); g.add(tp2); subs.push(tp2); }
    // the tap
    if (o.tap !== false) g.add(at(cyl(0.025, 0.03, 0.26, '#C9CED4', 10, { pivot: 'bottom', outline: 0.04 }), 0, 0.94, 0.1), rod([0, 1.18, 0.1], [0, 1.18, 0.28], 0.022, '#C9CED4'));
    // the window
    g.add(at(box(1.0, 0.9, 0.06, '#F4F0E6', { outline: 0.006 }), 0, 1.75, 0.01), at(box(0.88, 0.78, 0.02, '#BFE3F2', { emissive: '#6A9AB0', noGrain: true }), 0, 1.75, 0.045), at(box(0.04, 0.78, 0.03, '#F4F0E6'), 0, 1.75, 0.05));
    // o.upper: a row of wall cupboards high up (seen over the concrete)
    if (o.upper) for (let i = 0; i < 6; i++) { const x = -2.75 + i * 1.1; g.add(at(box(1.04, 0.72, 0.36, '#F4F0E6', { outline: 0.008 }), x, 2.42 + 0.36, 0.18), at(box(0.02, 0.66, 0.01, '#C9C2B2'), x, 2.78, 0.365), at(box(0.12, 0.025, 0.03, '#8A939B'), x + 0.16, 2.5, 0.375)); }
    // the wall phone
    const px = o.phoneX ?? -1.0;   // (o.phoneX: where the wall phone hangs)
    g.add(at(box(0.18, 0.28, 0.06, '#E8E2D2', { outline: 0.02 }), px, 1.5, 0.03), at(box(0.1, 0.1, 0.01, '#3A3F45'), px, 1.43, 0.065));
    const hs = grp(at(box(0.06, 0.26, 0.06, '#E8E2D2', { outline: 0.03 }), 0, 0, 0)); hs.position.set(px - 0.07, 1.52, 0.09); g.add(hs);
    g.userData.phone = [px - 0.07, 1.52, 0.09];
    // the fridge
    const fr = grp(at(box(0.8, 1.85, 0.7, '#F6F6F2', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(box(0.78, 0.015, 0.02, '#C9CED4'), 0, 1.25, 0.355), at(box(0.04, 0.4, 0.04, '#B7C2C9'), 0.3, 1.45, 0.37));
    fr.add(at(cyl(0.05, 0.05, 0.02, '#E8463C', 12), -0.2, 1.62, 0.36, PI / 2));
    if (o.fridge !== false) { fr.position.set(-2.1, 0, 0.36); g.add(fr); }
    // the door in the right side wall
    // o.doorX: the door in the back wall at that x instead (hinged at its left edge, opening into the room)
    const dh = o.doorX != null ? grp(at(box(0.9, 2.05, 0.05, '#B98A5E', { outline: 0.006 }), 0.45, 1.025, 0), at(sphere(0.035, '#D9A93A', 1), 0.8, 1.0, 0.04)) : grp(at(box(0.05, 2.05, 0.9, '#B98A5E', { outline: 0.006 }), 0, 1.025, 0.45), at(sphere(0.035, '#D9A93A', 1), -0.04, 1.0, 0.8));
    if (o.doorX != null) { dh.position.set(o.doorX - 0.45, 0, 0.04); g.add(at(box(1.04, 2.15, 0.012, '#2A2622'), o.doorX, 1.075, 0.022)); } else dh.position.set(W / 2 - 0.08, 0, 1.4);   // (the dark doorway clear of the wall face: no z-fight)
    g.add(dh);
    g.userData.update = t => {
      const dv = clamp01(kv(o.doors, t, 0)); for (const { h, s } of doors) h.rotation.y = s * 1.6 * dv; subs.forEach(c => c.userData.update?.(t));
      hs.visible = o.handsetFrom == null || t >= o.handsetFrom;
      const b = o.burstAt != null && t >= o.burstAt ? t - o.burstAt : -1; dh.rotation.y = (o.doorX != null ? 1 : -1) * (b < 0 ? 0 : 1.75 * Math.min(1, b / 0.12)) + (o.doorX != null ? 1 : -1) * (b > 0.12 ? 0.12 * Math.exp(-6 * (b - 0.12)) * Math.sin((b - 0.12) * 25) : 0);
    };
    g.userData.update(-1); return g;
  },

  // A mugshot height chart (pivot at the floor under its middle, front +Z): a dark slate wall o.w (2.4) x 2.6 with white height lines every 10 cm,
  // thicker every 50 cm, no figure
  fuChart(o) {
    const W = o.w ?? 2.4, H = 2.6;
    return grp(at(canvasPlane(W, H, (c, Wc, Hc) => { c.fillStyle = '#3A4652'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#E8ECEF'; for (let i = 0; i <= 26; i++) { const y = Hc - i / 26 * Hc, th = i % 5 === 0 ? Hc * 0.008 : Hc * 0.003; c.fillRect(i % 5 === 0 ? 0 : Wc * 0.1, y - th / 2, i % 5 === 0 ? Wc : Wc * 0.8, th); } }, { res: 512 }), 0, H / 2, 0));
  },

  // A wall-phone handset held (attach to a hand): the cream receiver with ear and mouth cups
  fuHandset(o) { return grp(at(box(0.06, 0.26, 0.06, '#E8E2D2', { outline: 0.03 }), 0, 0, 0), at(box(0.08, 0.06, 0.07, '#E8E2D2'), 0, 0.12, 0.02), at(box(0.08, 0.06, 0.07, '#E8E2D2'), 0, -0.12, 0.02)); },

  // Big headphones (attach to the head joint): two black cups at the ears and a band over the skull; o.w (0.36) between the cups, o.y the cups' height
  fuPhones(o) {
    const w = o.w ?? 0.36, y = o.y ?? 0.2, g = grp();
    for (const s of [-1, 1]) g.add(at(cyl(0.085, 0.085, 0.06, '#1E2126', 12, { outline: 0.04 }), s * w / 2, y, 0, 0, 0, PI / 2), at(cyl(0.06, 0.06, 0.07, '#C23A2E', 12), s * (w / 2 + 0.005), y, 0, 0, 0, PI / 2));
    const band = new THREE.Mesh(new THREE.TorusGeometry(w / 2, 0.022, 6, 16, PI), mat('#1E2126')); band.position.y = y + 0.06; band.scale.y = 1.15; g.add(band);
    return g;
  },

  // A hand microphone (attach to a hand): a black grip and a big grey mesh ball, its cable dangling
  fuMic(o) { return grp(at(cyl(0.025, 0.02, 0.18, '#1E2126', 8, { outline: 0.04 }), 0, 0, 0), at(sphere(0.055, '#9AA0A8', 1, { outline: 0.04 }), 0, 0.12, 0), rod([0, -0.09, 0], [0.04, -0.3, 0.02], 0.008, '#1E2126')); },

  // A small morse printer (pivot at the floor in its middle, front +Z): a grey box with a red light, a fat white paper strip coming out of its front
  // slot toward +Z and curling down, printed with thick black dots and dashes that scroll out as it feeds (o.feed [t0, t1]); o.s scale
  fuMorse(o) {
    const s = o.s ?? 1, g = grp(), k = grp(); g.add(k); k.scale.setScalar(s);
    k.add(at(box(0.36, 0.2, 0.28, '#8A939B', { pivot: 'bottom', outline: 0.02 }), 0, 0, 0), at(box(0.3, 0.02, 0.01, '#1E2126'), 0, 0.12, 0.142), at(sphere(0.02, '#E8463C', 1), 0.13, 0.17, 0.142));
    const Wd = 0.2, L = 1.2, code = '.-.. . -- --- - -.. . .--. .- ... ... .';
    const c = document.createElement('canvas'); c.width = 128; c.height = 1024; const x = c.getContext('2d');
    x.fillStyle = '#FBFAF4'; x.fillRect(0, 0, 128, 1024); x.fillStyle = '#14161A'; let yy = 20;
    for (const ch of code) { if (ch === '.') { x.beginPath(); x.arc(64, yy + 18, 17, 0, TAU); x.fill(); yy += 52; } else if (ch === '-') { x.fillRect(46, yy, 36, 70); yy += 92; } else yy += 40; if (yy > 1000) break; }
    const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
    const strip = new THREE.Mesh(new THREE.PlaneGeometry(Wd, L), new THREE.MeshLambertMaterial({ map: tex, side: THREE.DoubleSide })); strip.rotation.x = -PI / 2; k.add(strip);
    g.userData.update = t => { const u = o.feed ? smooth((t - o.feed[0]) / (o.feed[1] - o.feed[0])) : 1, len = 0.05 + (L - 0.05) * u;
      strip.scale.y = len / L; strip.position.set(0, 0.12, 0.14 + len / 2); tex.offset.y = 1 - len / L; tex.repeat.y = len / L; };
    g.userData.update(-1); return g;
  },

  // A generic palace front (pivot at the floor in the middle of its front, faces +Z): a pale stone block 14 m wide and 7 m high with rows of tall
  // windows, a portico of six columns under a plain pediment (no emblem, no flag, no word), steps, and a black iron fence with a double gate at x 0
  // (o.gateAt: its two leaves swing open)
  fuPalace(o) {
    const g = grp(), S = '#EDE6D6', D = '#D8CFBC';
    g.add(at(box(14, 7, 4, S, { pivot: 'bottom', outline: 0.006 }), 0, 0, -2), at(box(14.4, 0.4, 4.4, D), 0, 7.0, -2), at(box(14.2, 0.5, 4.2, D, { pivot: 'bottom' }), 0, 0, -2));
    for (let r = 0; r < 2; r++) for (let i = 0; i < 9; i++) { const x = -6 + i * 1.5; if (Math.abs(x) < 2.6) continue; g.add(at(box(0.8, 1.7, 0.06, '#5E7C92', { noGrain: true }), x, 1.6 + r * 2.9, 0.02), at(box(1.0, 0.12, 0.12, D), x, 2.5 + r * 2.9, 0.06)); }
    for (let i = 0; i < 6; i++) g.add(at(cyl(0.28, 0.32, 5.4, '#F6F1E6', 12, { pivot: 'bottom', outline: 0.01 }), -2.5 + i, 0.9, 1.2));
    g.add(at(box(6.2, 0.4, 1.6, D), 0, 6.5, 1.0));
    const ped = new THREE.Shape(); ped.moveTo(-3.2, 0); ped.lineTo(3.2, 0); ped.lineTo(0, 1.4); ped.closePath();
    const pm = new THREE.Mesh(new THREE.ExtrudeGeometry(ped, { depth: 1.4, bevelEnabled: false }), mat(S)); pm.position.set(0, 6.7, 0.3); addOutline(pm, 0.01); g.add(pm);
    for (let i = 0; i < 3; i++) g.add(at(box(7 - i * 0.4, 0.3, 0.6, D, { pivot: 'bottom' }), 0, i * 0.3, 2.4 - i * 0.55));
    g.add(at(box(2.2, 3.4, 0.08, '#5A3A28'), 0, 2.6, 0.03));
    // the fence and the gate
    const fz = o.fenceZ ?? 7;
    for (const sd of [-1, 1]) for (let x = 1.6; x < 7.2; x += 0.22) g.add(at(box(0.04, 2.2, 0.04, '#1E2126', { pivot: 'bottom' }), sd * x, 0, fz));
    for (const sd of [-1, 1]) g.add(at(box(5.6, 0.06, 0.06, '#1E2126'), sd * 4.4, 2.0, fz), at(box(5.6, 0.06, 0.06, '#1E2126'), sd * 4.4, 0.3, fz), at(box(0.18, 2.8, 0.18, '#2A2C31', { pivot: 'bottom', outline: 0.01 }), sd * 1.55, 0, fz));
    const leaves = [-1, 1].map(sd => { const h = grp(); for (let x = 0.1; x < 1.45; x += 0.2) h.add(at(box(0.04, 2.4, 0.04, '#1E2126', { pivot: 'bottom' }), -sd * x, 0, 0)); h.add(at(box(1.45, 0.06, 0.06, '#1E2126'), -sd * 0.72, 2.2, 0), at(box(1.45, 0.06, 0.06, '#1E2126'), -sd * 0.72, 0.3, 0)); h.position.set(sd * 1.45, 0, fz); g.add(h); return { h, sd }; });
    g.userData.gate = [0, 1.25, fz + 0.12];
    g.userData.update = t => { const u = o.gateAt == null ? 0 : smooth((t - o.gateAt) / 0.6); leaves.forEach(({ h, sd }) => { h.rotation.y = -sd * 1.2 * u; }); };
    g.userData.update(-1); return g;
  },

  // A big monitor on a stand with a keyboard (pivot at the desk top in its middle, faces +Z): a dark screen showing a big padlock icon, white and
  // open, that snaps shut and turns green at o.shutAt; o.keys [t, ...]: keys flash as they are typed
  fuScreen(o) {
    const g = grp(at(box(1.1, 0.7, 0.06, '#1E2126', { outline: 0.01 }), 0, 0.6, 0), at(box(0.08, 0.25, 0.08, '#2A2C31'), 0, 0.12, -0.02), at(box(0.4, 0.02, 0.25, '#2A2C31'), 0, 0.01, -0.02));
    const draw = shut => (c, W, H) => { c.fillStyle = '#16202A'; c.fillRect(0, 0, W, H); const col = shut ? '#3FD07A' : '#E8ECEF'; c.fillStyle = col; c.strokeStyle = col; c.lineWidth = W * 0.05;
      c.fillRect(W * 0.34, H * 0.48, W * 0.32, H * 0.36); c.beginPath(); const lift = shut ? 0 : H * 0.12; c.arc(W * 0.5, H * 0.48 - lift, W * 0.11, PI, 0); c.lineTo(W * 0.61, H * 0.48 - lift + (shut ? 0 : H * 0.02)); c.moveTo(W * 0.39, H * 0.48 - lift); c.lineTo(W * 0.39, H * 0.48); c.stroke(); };
    const a = canvasPlane(1.0, 0.6, draw(false), { res: 256, emissive: 0.7 }), b = canvasPlane(1.0, 0.6, draw(true), { res: 256, emissive: 0.7 });
    a.position.set(0, 0.6, 0.032); b.position.set(0, 0.6, 0.032); g.add(a, b);
    const kb = grp(at(box(0.9, 0.04, 0.3, '#2A2C31', { outline: 0.01 }), 0, 0.02, 0.45)); g.add(kb);
    const keys = []; for (let r = 0; r < 4; r++) for (let i = 0; i < 12; i++) { const m = at(box(0.055, 0.02, 0.05, '#DDE1E6', { unique: true }), -0.36 + i * 0.065, 0.05, 0.34 + r * 0.065); kb.add(m); keys.push(m); }
    g.userData.update = t => { const sh = o.shutAt != null && t >= o.shutAt; a.visible = !sh; b.visible = sh; const sc = sh ? 1 + 0.12 * Math.exp(-10 * (t - o.shutAt)) : 1; b.scale.setScalar(sc);
      keys.forEach((m, i) => { const hit = (o.keys || []).some(k => t >= k && t < k + 0.1 && (Math.floor(k * 37) % keys.length) === i); m.position.y = hit ? 0.035 : 0.05; m.material.color.set(hit ? '#3FD07A' : '#DDE1E6'); }); };
    g.userData.update(-1); return g;
  },

  // A newspaper front page (pivot at its middle, faces +Z): a newsprint sheet o.w (0.42) x 1.35 o.w, a huge photo of one blue drop on a grey
  // ground filling most of it, grey column bars below and a thick dark band where a headline would be (no word)
  fuPaper(o) {
    const w = o.w ?? 0.42, h = w * 1.35;
    return grp(at(box(w + 0.01, h + 0.01, 0.006, '#D9D4C6'), 0, 0, -0.004), canvasPlane(w, h, (c, W, H) => {
      c.fillStyle = '#F2EEE2'; c.fillRect(0, 0, W, H); c.fillStyle = '#2A2C31'; c.fillRect(W * 0.06, H * 0.04, W * 0.88, H * 0.09);
      c.fillStyle = '#C9CED4'; c.fillRect(W * 0.06, H * 0.17, W * 0.88, H * 0.55); c.fillStyle = '#2F8FD8'; c.strokeStyle = '#14161A'; c.lineWidth = W * 0.015;
      c.beginPath(); c.moveTo(W * 0.5, H * 0.22); c.bezierCurveTo(W * 0.62, H * 0.38, W * 0.7, H * 0.48, W * 0.66, H * 0.56); c.arc(W * 0.5, H * 0.56, W * 0.16, 0, PI); c.bezierCurveTo(W * 0.3, H * 0.48, W * 0.38, H * 0.38, W * 0.5, H * 0.22); c.fill(); c.stroke();
      c.fillStyle = '#FFFFFF'; c.beginPath(); c.arc(W * 0.44, H * 0.52, W * 0.035, 0, TAU); c.fill();
      c.fillStyle = '#9AA0A8'; for (let r = 0; r < 5; r++) for (let k = 0; k < 3; k++) c.fillRect(W * (0.06 + k * 0.3), H * (0.76 + r * 0.04), W * 0.26, H * 0.018);
    }, { res: 256 }));
  },

  // A newsstand (pivot at the floor in its middle, faces +Z): a green kiosk 2.4 wide with a roof, its counter and back wall covered with the same
  // front page (fuPaper) in rows, no word on it
  fuKiosk(o) {
    const g = grp(at(box(2.4, 2.3, 1.2, '#2F6A4E', { pivot: 'bottom', outline: 0.008 }), 0, 0, -0.6), at(box(2.7, 0.15, 1.6, '#24543E', { outline: 0.006 }), 0, 2.4, -0.5));
    g.add(at(box(2.2, 1.3, 0.04, '#F2EEE2'), 0, 1.45, 0.02), at(box(2.4, 0.08, 0.5, '#24543E'), 0, 0.85, 0.25), at(box(2.4, 0.8, 0.5, '#2F6A4E', { pivot: 'bottom' }), 0, 0, 0.25));
    for (let r = 0; r < 2; r++) for (let i = 0; i < 5; i++) { const p = FUITE_PROPS.fuPaper({ w: 0.38 }); p.position.set(-0.88 + i * 0.44, 1.75 - r * 0.62, 0.05); g.add(p); }
    for (let i = 0; i < 5; i++) { const p = FUITE_PROPS.fuPaper({ w: 0.38 }); p.position.set(-0.88 + i * 0.44, 0.92, 0.42); p.rotation.x = -1.2; g.add(p); }
    return g;
  },

  // A cardboard box that drips (pivot at its bottom middle; carry it at the hands): a brown box with folded flaps, papers and a desk lamp
  // sticking out, and a drop falling from its bottom corner every o.rate s (0.4), splashing below at o.fallH (1.1 m)
  fuDripBox(o) {
    const g = grp(at(box(0.5, 0.36, 0.4, '#C49A66', { pivot: 'bottom', outline: 0.02 }), 0, 0, 0), at(box(0.5, 0.02, 0.2, '#B08656'), 0, 0.37, 0.27, -0.6), at(box(0.5, 0.02, 0.2, '#B08656'), 0, 0.37, -0.27, 0.6));
    g.add(at(box(0.3, 0.12, 0.02, '#F6F4EE'), -0.05, 0.42, 0), at(cyl(0.03, 0.06, 0.08, '#2E6A9E', 8), 0.14, 0.42, 0.05), rod([0.14, 0.44, 0.05], [0.18, 0.62, 0.0], 0.012, '#2E6A9E'), at(cyl(0.07, 0.04, 0.08, '#2E6A9E', 8), 0.2, 0.64, 0.0, 0, 0, -0.6));
    g.add(at(box(0.5, 0.06, 0.4, '#8E6A44'), 0, 0.03, 0));
    const drops = []; for (let i = 0; i < 4; i++) { const d = dropMesh(0.09); g.add(d); drops.push(d); }
    const H = o.fallH ?? 1.1, per = o.rate ?? 0.4;
    g.userData.update = t => drops.forEach((d, i) => { const u = ((t + i * per) % (per * 4)) / (per * 4) * 4; d.visible = u < 1; const v = clamp01(u); d.position.set(0.2, -0.02 - H * v * v, 0.17); d.scale.setScalar(0.6 + 0.4 * Math.min(1, v * 4)); });
    g.userData.update(-1); return g;
  },

  // A decree held up (pivot at its middle, faces +Z): a cream sheet o.w (0.5) x 1.35 o.w with a thick blue border and grey bars (no word); o.stampAt: a big
  // red round seal mark (plain rings, no word or emblem) slams onto its lower half
  fuDecree(o) {
    const w = o.w ?? 0.5, h = w * 1.35, g = grp(at(box(w + 0.02, h + 0.02, 0.008, '#C9C2B2'), 0, 0, -0.005));
    g.add(canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FBF7EA'; c.fillRect(0, 0, W, H); c.strokeStyle = '#2E4A7A'; c.lineWidth = W * 0.03; c.strokeRect(W * 0.05, H * 0.04, W * 0.9, H * 0.92);
      c.fillStyle = '#2A2C31'; c.fillRect(W * 0.2, H * 0.1, W * 0.6, H * 0.05); c.fillStyle = '#A9AEB6'; for (let i = 0; i < 7; i++) c.fillRect(W * 0.14, H * (0.24 + i * 0.065), W * (i === 6 ? 0.4 : 0.72), H * 0.022); }, { res: 256 }));
    const seal = canvasPlane(w * 0.5, w * 0.5, (c, W, H) => { c.clearRect(0, 0, W, H); c.strokeStyle = '#C8202A'; c.lineWidth = W * 0.07; c.beginPath(); c.arc(W / 2, H / 2, W * 0.42, 0, TAU); c.stroke(); c.lineWidth = W * 0.04; c.beginPath(); c.arc(W / 2, H / 2, W * 0.28, 0, TAU); c.stroke();
      c.fillStyle = '#C8202A'; c.beginPath(); c.arc(W / 2, H / 2, W * 0.12, 0, TAU); c.fill(); }, { res: 128, transparent: true });
    seal.position.set(w * 0.12, -h * 0.26, 0.006); g.add(seal);
    g.userData.update = t => { const on = o.stampAt == null || t >= o.stampAt; seal.visible = o.stampAt != null && on; if (seal.visible) seal.scale.setScalar(1 + 0.4 * Math.exp(-14 * (t - o.stampAt))); };
    g.userData.update(-1); return g;
  },

  // A big rubber stamp (pivot at its handle grip; held upright, the pad at -Y): a red ball handle, a wooden neck and a dark pad 0.2 wide
  fuStamp(o) { const s = o.s ?? 1, g = grp(at(sphere(0.07 * s, '#C23A2E', 1, { outline: 0.04 }), 0, 0, 0), at(cyl(0.035 * s, 0.045 * s, 0.14 * s, '#8A5A38', 8, { outline: 0.03 }), 0, -0.1 * s, 0), at(box(0.2 * s, 0.05 * s, 0.14 * s, '#2A2C31', { outline: 0.03 }), 0, -0.19 * s, 0)); return g; },

  // A drawing board on an easel (pivot at the floor in its middle, faces +Z): a white board with a blue drawing of a sink with its tap and the drop
  // under it, circled in red (no word)
  fuSinkBoard(o) {
    const w = o.w ?? 1.0, h = w * 0.75, y0 = o.y0 ?? 0.9, g = grp(at(box(w + 0.06, h + 0.06, 0.04, '#3A3D44', { outline: 0.01 }), 0, y0 + h / 2, -0.03));
    g.add(at(canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FBFAF4'; c.fillRect(0, 0, W, H); c.strokeStyle = '#2E4A7A'; c.lineWidth = W * 0.015; c.lineJoin = 'round';
      c.strokeRect(W * 0.25, H * 0.42, W * 0.5, H * 0.38); c.beginPath(); c.moveTo(W * 0.22, H * 0.42); c.lineTo(W * 0.78, H * 0.42); c.stroke();
      c.beginPath(); c.moveTo(W * 0.5, H * 0.42); c.lineTo(W * 0.5, H * 0.24); c.lineTo(W * 0.62, H * 0.24); c.lineTo(W * 0.62, H * 0.3); c.stroke();
      c.beginPath(); c.moveTo(W * 0.5, H * 0.52); c.lineTo(W * 0.5, H * 0.6); c.lineTo(W * 0.58, H * 0.6); c.stroke();
      c.fillStyle = '#2F8FD8'; c.beginPath(); c.arc(W * 0.5, H * 0.7, W * 0.025, 0, TAU); c.fill();
      c.strokeStyle = '#D8262E'; c.lineWidth = W * 0.025; c.beginPath(); c.ellipse(W * 0.5, H * 0.55, W * 0.36, H * 0.4, -0.1, 0, TAU); c.stroke(); }, { res: 512 }), 0, y0 + h / 2, 0));
    for (const s of [-1, 1]) g.add(rod([s * w * 0.3, 0, 0.12], [s * w * 0.3, y0 + 0.1, -0.06], 0.025, '#5E656D'));
    return g;
  },

  // A concrete mixer truck facing +X (pivot at the floor in its middle; 6.5 long): a white cab, a dark chassis, a striped orange-and-grey drum turning
  // on its slanted axis, a chute at the back (-X end) pouring a grey stream o.pour [t0, t1] that runs o.pourLen (3) m along -X and down
  // A kitchen window in a house front (pivot at its middle, front +Z): a white frame and sill, the kitchen glimpsed inside (a green wall band,
  // a cupboard top); o.fill [t0, t1]: grey concrete rises inside it to 0.7 of its height
  fuWindow(o) {
    const w = o.w ?? 1.2, h = o.h ?? 1.0, g = grp();
    g.add(at(box(w + 0.18, h + 0.18, 0.08, '#F4F0E6', { outline: 0.01 }), 0, 0, -0.06), at(box(w, h, 0.02, '#2E2B28'), 0, 0, -0.005), at(box(w + 0.34, 0.07, 0.24, '#E8E2D2', { outline: 0.01 }), 0, -h / 2 - 0.05, 0.06));
    g.add(at(box(w * 0.96, h * 0.3, 0.01, '#9FC0AE'), 0, h * 0.12, 0.008), at(box(w * 0.5, h * 0.22, 0.01, '#C9B79A'), -w * 0.18, -h * 0.34, 0.01));
    const fill = at(box(w * 0.98, h, 0.02, '#9AA0A3', { pivot: 'bottom' }), 0, -h / 2, 0.014); g.add(fill);
    g.userData.update = t => { const u = o.fill ? smooth((t - o.fill[0]) / (o.fill[1] - o.fill[0])) : 0; fill.visible = u > 0.01; fill.scale.y = Math.max(0.001, 0.7 * u); };
    g.userData.update(-1); return g;
  },
  // A boom microphone (pivot at the hand end): a thin black pole to o.b (relative point), a fat mic standing up at its end; o.s mic scale
  fuBoom(o) {
    const b = o.b ?? [0, 0.3, -1.2], g = grp(rod([0, 0, 0], b, 0.014, '#2A2C31')), m = FUITE_PROPS.fuMic({}); m.scale.setScalar(o.s ?? 1.4); m.position.set(b[0], b[1] + 0.1 * (o.s ?? 1.4), b[2]); g.add(m);
    return g;
  },
  fuMixer(o) {
    const g = grp();
    g.add(at(box(6.4, 0.3, 2.0, '#2A2C31'), 0, 0.75, 0), at(box(1.6, 1.7, 2.1, '#F2F2EE', { outline: 0.012 }), 2.4, 1.75, 0), at(box(0.06, 0.7, 1.8, '#5E7C92', { noGrain: true }), 3.21, 2.05, 0));
    for (const x of [2.4, -1.0, -2.2]) for (const z of [-0.95, 0.95]) g.add(at(cyl(0.48, 0.48, 0.34, '#1E2126', 12), x, 0.48, z, PI / 2), at(cyl(0.2, 0.2, 0.36, '#C9CED4', 8), x, 0.48, z, PI / 2));
    const drum = grp(); drum.position.set(-0.9, 2.05, 0); drum.rotation.z = 0.18; g.add(drum);
    const dm = new THREE.Mesh(new THREE.CylinderGeometry(0.95, 1.05, 3.4, 16), mat('#E8742A')); dm.rotation.z = PI / 2; addOutline(dm, 0.01); drum.add(dm);
    for (let i = 0; i < 4; i++) { const st = new THREE.Mesh(new THREE.TorusGeometry(1.0, 0.07, 4, 16), mat('#D8DDE2')); st.rotation.y = PI / 2; st.position.x = -1.3 + i * 0.85; drum.add(st); }
    g.add(rod([-2.6, 1.6, 0], [-3.4, 1.1, 0], 0.12, '#8A939B'));
    const R0 = o.ribbon ?? 0.2, sm = new THREE.MeshLambertMaterial({ color: '#9AA0A3' }), stream = new THREE.Mesh(new THREE.CylinderGeometry(R0 * 0.85, R0 * 1.1, 1, 10), sm); g.add(stream);
    const lumps = [0, 1, 2, 3].map(() => { const m = new THREE.Mesh(new THREE.SphereGeometry(R0 * 1.2, 8, 6), sm); g.add(m); return m; });
    const splat = new THREE.Mesh(new THREE.SphereGeometry(R0 * 2.0, 12, 8), sm); g.add(splat);
    const L = o.pourLen ?? 3, DR = o.pourDrop ?? 0.6;   // o.ribbon: its radius; o.pourDrop: how far it falls over its length
    g.userData.update = t => { drum.rotation.x = t * 2.2;
      const on = o.pour && t >= o.pour[0] && t <= o.pour[1] + 0.3; stream.visible = !!on; splat.visible = false; lumps.forEach(m => { m.visible = false; }); if (!on) return; const u = Math.min(1, (t - o.pour[0]) / 0.3), end = Math.max(0, (t - o.pour[1]) / 0.3);
      const a = new THREE.Vector3(-3.4, 1.1, 0), b = new THREE.Vector3(-3.4 - L * u, 1.1 - DR * u, 0); const mid = a.clone().lerp(b, 0.5 + end * 0.5);
      stream.position.copy(mid); stream.scale.set(1 + 0.14 * Math.sin(t * 19), Math.max(0.01, a.distanceTo(b) * (1 - end)), 1 + 0.14 * Math.sin(t * 23)); stream.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), b.clone().sub(a).normalize());
      lumps.forEach((m, i) => { const f = (t * 1.7 + i / 4) % 1; m.visible = u >= 1 && end === 0; m.position.copy(a.clone().lerp(b, f)); m.scale.setScalar(0.8 + 0.3 * Math.sin(i * 2 + t * 9)); });
      const w = t - o.pour[0] - 0.3; splat.visible = w > 0 && end < 1; splat.position.copy(b);   // where it lands: a big squash, then a fat pulsing splat
      const hit = w < 0.25 ? Math.sin(clamp01(w / 0.25) * PI) : 0; splat.scale.set(1.2 + 0.7 * hit + 0.15 * Math.sin(t * 14), 0.5 - 0.3 * hit + 0.08 * Math.sin(t * 14 + 1), 1.2 + 0.7 * hit + 0.15 * Math.sin(t * 13)); };
    g.userData.update(-1); return g;
  },

  // The concrete block filling the kitchen (pivot at the floor in the middle of the back wall's foot): a smooth grey block o.w (6.8) x o.h (2.6) x o.d
  // (2.6) with slightly rounded edges and pour marks, the top corner of a white fridge (with one red magnet) sticking out of its top at o.fx;
  // o.rise [t0, t1]: it rises from the floor; o.hole [x, y]: a chiselled hole in its front (dark, with chipped edges)
  fuConcrete(o) {
    const W = o.w ?? 6.8, H = o.h ?? 2.6, D = o.d ?? 2.6, g = grp(), k = grp(); g.add(k);
    const m = mat('#A7ABAD'); k.add(at(box(W, H, D, '#A7ABAD', { pivot: 'bottom', outline: 0.004 }), 0, 0, D / 2));
    for (let i = 0; i < 3; i++) k.add(at(box(W + 0.01, 0.02, D + 0.01, '#979B9D'), 0, 0.7 + i * 0.7, D / 2));
    void m;
    const fx = o.fx ?? -2.1, FH = o.fh ?? 0.5, fr = grp(at(box(0.8, FH, 0.7, '#F6F6F2', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(0.8, 0.02, 0.71, '#E2E2DC'), 0, FH * 0.64, 0));   // the freezer seam, no handle
    const mg = grp(at(cyl(0.1, 0.1, 0.03, '#E8463C', 16, { outline: 0.03 }), 0, 0, 0, PI / 2), at(sphere(0.025, '#FFFFFF', 0), -0.035, 0.035, 0.02), at(box(0.035, 0.05, 0.02, '#3E8E3A'), 0.0, 0.11, 0));   // a big red apple magnet, a leaf
    mg.position.set(-0.12, FH * 0.36, 0.37); fr.add(mg);
    fr.position.set(fx, H - 0.12, o.fz ?? 0.4); if (!o.upright) fr.rotation.set(0.1, 0.45, 0.22); k.add(fr);   // o.fz: how far forward the fridge corner sticks out; o.upright: square to the block
    if (o.hole) { const [hx, hy] = o.hole, sh = new THREE.Shape(); for (let i = 0; i <= 12; i++) { const a = i / 12 * TAU, rr = 1 + 0.12 * Math.sin(i * 2.7); const px = Math.cos(a) * 0.46 * rr, py = Math.sin(a) * 0.38 * rr; if (i) sh.lineTo(px, py); else sh.moveTo(px, py); }
      k.add(at(new THREE.Mesh(new THREE.ShapeGeometry(sh), new THREE.MeshBasicMaterial({ color: '#2A2C30' })), hx, hy, D + 0.012), at(box(0.55, 0.04, 0.02, '#C9CED4'), hx, hy - 0.08, D + 0.015));   // a rough dark hole, the old pipe in it
      for (let i = 0; i < 14; i++) { const a = i / 14 * TAU; k.add(at(box(0.16 + 0.06 * hsh(i), 0.12 + 0.05 * hsh(i + 4), 0.12, i % 2 ? '#8E9294' : '#B8BCBE', { outline: 0.02 }), hx + Math.cos(a) * 0.52, hy + Math.sin(a) * 0.43, D + 0.04, hsh(i) * 0.4, 0, a)); } }
    const blob = new THREE.Mesh(new THREE.SphereGeometry(0.22, 12, 8), mat('#9EA2A4')); addOutline(blob, 0.02); g.add(blob);
    const dust = [0, 1, 2, 3, 4, 5, 6, 7].map(i => { const m = noShadow(new THREE.Mesh(new THREE.SphereGeometry(0.12, 8, 6), new THREE.MeshLambertMaterial({ color: '#C9CBC8', transparent: true, opacity: 0.6, depthWrite: false }))); g.add(m); return m; });
    g.userData.update = t => { const u = o.rise ? smooth((t - o.rise[0]) / (o.rise[1] - o.rise[0])) : 1; k.scale.y = Math.max(0.001, u); k.visible = u > 0.002;
      // o.plop [t, x, z]: a last dollop falls on the top, squashes and wobbles flat
      const pl = o.plop, pu = pl ? t - pl[0] : -1; blob.visible = pu > -0.3; if (pl) { if (pu < 0) { const f = 1 + pu / 0.3; blob.position.set(pl[1], H + 1.3 - 1.3 * f * f + 0.15, pl[2]); blob.scale.set(0.85, 1.25, 0.85); }
        else { const wb = Math.exp(-5 * pu) * Math.sin(pu * 26); blob.position.set(pl[1], H + 0.04, pl[2]); blob.scale.set(1.7 + 0.25 * wb, 0.32 - 0.12 * wb, 1.7 + 0.25 * wb); } }
      // o.slide [t0, t1]: the magnet slips down and tilts
      const sl = o.slide ? smooth((t - o.slide[0]) / (o.slide[1] - o.slide[0])) : 0; mg.position.y = FH * 0.36 - 0.14 * sl; mg.rotation.z = 0.35 * sl;
      // o.dust [t0]: a puff of dust rolls off the top
      dust.forEach((m, i) => { const du = o.dust != null ? t - o.dust[0] - 0.08 * i : -1; m.visible = du > 0 && du < 1.6; if (!m.visible) return; const a = hsh(i + 20) * TAU;
        m.position.set((o.dust[1] ?? 0) + Math.cos(a) * (0.3 + 0.5 * du), H + 0.1 + 0.35 * du, (o.dust[2] ?? D) + Math.sin(a) * 0.3 * du); m.scale.setScalar(0.6 + 1.4 * du); m.material.opacity = 0.55 * (1 - du / 1.6); }); };
    g.userData.update(-1); return g;
  },

  // A bowl (pivot at its bottom; carry it at the hands): a red plastic bowl o.r (0.17) full of yellow crisps, or (o.water [[t, 0..1]]) filling with
  // water that rises over the crisps; o.splashAt: a drop lands in it (a ring)
  fuBowl(o) {
    const r = o.r ?? 0.17, g = grp(at(cyl(r, r * 0.6, r * 0.6, '#D9473A', 14, { pivot: 'bottom', outline: 0.03 }), 0, 0, 0));
    const crisps = []; for (let i = 0; i < 14; i++) { const a = hsh(i) * TAU, rr = r * 0.75 * Math.sqrt(hsh(i + 3)); const c = at(box(0.06, 0.008, 0.045, '#F2C94C', { outline: 0.05 }), Math.cos(a) * rr, r * 0.55 + hsh(i + 5) * 0.03, Math.sin(a) * rr, hsh(i + 7) - 0.5, a, hsh(i + 9) - 0.5); g.add(c); crisps.push(c); }
    const w = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.97, r * 0.7, 0.01, 14), new THREE.MeshLambertMaterial({ color: '#5FB7E8', transparent: true, opacity: 0.8 })); g.add(w);
    const ring = noShadow(new THREE.Mesh(new THREE.RingGeometry(0.02, 0.035, 14), new THREE.MeshBasicMaterial({ color: '#FFFFFF', side: THREE.DoubleSide }))); ring.rotation.x = -PI / 2; g.add(ring);
    g.userData.update = t => { const lv = clamp01(kv(o.water, t, 0)); w.visible = lv > 0.01; w.position.y = r * 0.1 + r * 0.5 * lv; const sc = 0.7 + 0.3 * lv; w.scale.set(sc, 1, sc);
      const u = o.splashAt != null ? t - o.splashAt : -1; ring.visible = u > 0 && u < 0.5; ring.position.y = r * 0.6 + 0.01; ring.scale.setScalar(1 + u * 6);
      // o.chipsAt: eight crisps fly up, hang at the top, then rain back
      crisps.forEach((c, i) => { if (!c.userData.p0) c.userData.p0 = c.position.clone(); const p0 = c.userData.p0, cu = o.chipsAt != null && i < 8 ? t - o.chipsAt - 0.02 * i : -1;
        if (cu <= 0) { c.position.copy(p0); return; } const f = Math.min(1, cu / 1.0), hy = 0.6 * Math.sqrt(Math.max(0, Math.sin(f * PI))), a = i / 8 * TAU;
        c.position.set(p0.x + Math.cos(a) * 0.22 * f, p0.y + hy, p0.z + Math.sin(a) * 0.22 * f); c.rotation.x = p0.x + cu * 9; c.rotation.z = cu * 7; }); };
    g.userData.update(-1); return g;
  },

  // An oversized rubber washer (pivot at its middle, lying flat in XZ): a fat black ring o.R (0.09) with a soft sheen
  fuRing(o) { const R = o.R ?? 0.09, m = new THREE.Mesh(new THREE.TorusGeometry(R, R * 0.42, 10, 20), mat('#1C1D21')); m.rotation.x = PI / 2; addOutline(m, 0.04);
    const hl = noShadow(new THREE.Mesh(new THREE.TorusGeometry(R, R * 0.1, 4, 10, PI * 0.5), new THREE.MeshBasicMaterial({ color: '#8A9098' }))); hl.rotation.x = PI / 2; hl.position.y = R * 0.32; return grp(m, hl); },

  // A price tag on a string (pivot at the string's top, faces +Z): a white tag with a small round coin drawn on it (a yellow disc with a rim, no
  // figure, no money sign); o.popAt: it springs in
  fuTag(o) {
    const w = o.w ?? 0.3, g = grp(), k = grp(); g.add(k);
    k.add(at(canvasPlane(w, w * 0.6, (c, W, H) => { c.fillStyle = '#FBFAF4'; c.beginPath(); c.moveTo(W * 0.18, 0); c.lineTo(W, 0); c.lineTo(W, H); c.lineTo(W * 0.18, H); c.lineTo(0, H / 2); c.closePath(); c.fill(); c.lineWidth = W * 0.02; c.strokeStyle = '#1E2126'; c.stroke();
      c.fillStyle = '#1E2126'; c.beginPath(); c.arc(W * 0.16, H / 2, H * 0.07, 0, TAU); c.fill();
      c.fillStyle = '#E8B83A'; c.beginPath(); c.arc(W * 0.6, H / 2, H * 0.26, 0, TAU); c.fill(); c.strokeStyle = '#A07A1E'; c.lineWidth = W * 0.025; c.stroke(); c.beginPath(); c.arc(W * 0.6, H / 2, H * 0.16, 0, TAU); c.stroke(); }, { res: 256, transparent: true }), w * 0.45, -0.16, 0));
    k.add(rod([0, 0, 0], [0.01, -0.16, 0], 0.004, '#1E2126'));
    g.userData.update = t => { const s = o.popAt == null ? 1 : popS(t, o.popAt, 0.25); k.visible = s > 0.01; k.scale.setScalar(Math.max(0.001, s)); k.rotation.z = 0.15 * Math.sin(t * 3); };
    g.userData.update(-1); return g;
  },

  // An invoice that unrolls (pivot at its roll's start on a desk edge, the strip running toward +Z then down to the floor and along it): a white strip
  // 0.42 wide printed with rows of thick grey bars (no figure), unrolling o.unroll [[t, metres]] up to o.len (6); the roll itself shrinks at the end
  fuInvoice(o) {
    const g = grp(), Wd = o.w ?? 0.42, L = o.len ?? 6, drop = o.drop ?? 0.78;
    const c = document.createElement('canvas'); c.width = 128; c.height = 2048; const x = c.getContext('2d'); x.fillStyle = '#FBFAF4'; x.fillRect(0, 0, 128, 2048);
    for (let y = 16; y < 2048; y += 34) { x.fillStyle = '#7E848C'; x.fillRect(12, y, 64 + (y * 7 % 30), 12); x.fillStyle = '#2A2C31'; x.fillRect(92, y, 24, 12); }
    const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.wrapT = THREE.RepeatWrapping;
    const ml = new THREE.MeshLambertMaterial({ map: tex, side: THREE.DoubleSide });
    const hang = new THREE.Mesh(new THREE.PlaneGeometry(Wd, 1), ml), floor = new THREE.Mesh(new THREE.PlaneGeometry(Wd, 1), ml.clone()); floor.material.map = tex.clone(); floor.material.map.needsUpdate = true; floor.rotation.x = -PI / 2; g.add(hang, floor);
    const roll = at(cyl(0.07, 0.07, Wd + 0.02, '#F2EEE2', 12, { outline: 0.03 }), 0, 0.07, 0, 0, 0, PI / 2); g.add(roll);
    g.userData.update = t => { const u = Math.min(L, kv(o.unroll, t, 0)); const hl = Math.min(drop, u); hang.visible = u > 0.01; hang.scale.y = Math.max(0.001, hl); hang.position.set(0, -hl / 2, 0.08);
      tex.repeat.set(1, hl / 3); const fl = Math.max(0, u - drop); floor.visible = fl > 0.01; floor.scale.y = Math.max(0.001, fl); floor.position.set(0, -drop + 0.004, 0.08 + fl / 2); floor.material.map.repeat.set(1, fl / 3);
      roll.scale.setScalar(Math.max(0.35, 1 - u / L * 0.65)); };
    g.userData.update(-1); return g;
  },

  // A big safe (pivot at the floor in its middle, faces +Z): a dark green steel box 1.0 x 1.3 x 0.9 on feet, a thick door hinged at its left with a
  // dial and a wheel handle; o.door [[t, 0..1]] (1 open); o.slamAt: it slams shut (a jolt)
  fuSafe(o) {
    const g = grp(), k = grp(); g.add(k);
    k.add(at(box(1.0, 1.3, 0.9, '#2F4A3E', { pivot: 'bottom', outline: 0.01 }), 0, 0.08, 0), at(box(0.86, 1.16, 0.02, '#141618'), 0, 0.73, 0.451));
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) k.add(at(box(0.1, 0.08, 0.1, '#1E2126', { pivot: 'bottom' }), sx * 0.4, 0, sz * 0.35));
    const door = grp(at(box(0.88, 1.18, 0.1, '#3A5A4C', { outline: 0.01 }), 0.44, 0, 0.05), at(cyl(0.11, 0.11, 0.05, '#C9CED4', 16, { outline: 0.04 }), 0.44, 0.2, 0.12, PI / 2), at(torus2(0.14), 0.44, -0.2, 0.12));
    door.position.set(-0.44, 0.73, 0.45); k.add(door);
    function torus2(r) { const m = new THREE.Mesh(new THREE.TorusGeometry(r, 0.025, 6, 16), mat('#C9CED4')); return m; }
    g.userData.update = t => { let d = clamp01(kv(o.door, t, 0)); if (o.slamAt != null && t >= o.slamAt) d = 0; door.rotation.y = -1.7 * d;
      const j = o.slamAt != null && t >= o.slamAt && t < o.slamAt + 0.4 ? Math.exp(-9 * (t - o.slamAt)) * Math.sin((t - o.slamAt) * 45) : 0; k.position.x = 0.03 * j; k.rotation.z = 0.02 * j; };
    g.userData.update(-1); return g;
  },

  // The tap (pivot at the counter top under it, faces +Z): a chrome column and a long spout reaching toward +Z (o.len 0.32) that turns about the
  // column (o.swivel [[t, rad]]); inside its opening a small round black grille whose red light comes on at o.lightAt (it blinks); o.flow [[t0, t1]]:
  // a stream of water from the spout; o.s scale (big for the close-up)
  fuTap(o) {
    const s = o.s ?? 1, L = o.len ?? 0.32, g = grp(), k = grp(); g.add(k); k.scale.setScalar(s);
    k.add(at(cyl(0.035, 0.045, 0.3, '#D8DDE2', 14, { pivot: 'bottom', outline: 0.03 }), 0, 0, 0), at(cyl(0.05, 0.05, 0.03, '#C9CED4', 14), 0, 0.01, 0));
    k.add(at(cyl(0.02, 0.02, 0.12, '#C9CED4', 10), 0.08, 0.2, 0, 0, 0, PI / 2), at(sphere(0.012, '#D8DDE2', 1), 0.15, 0.2, 0));   // the lever's stem (its knob: lev, a red knob read as the light)
    const lev = grp(at(box(0.04, 0.03, 0.03, '#D8DDE2', { outline: 0.03 }), 0, 0, 0)); lev.position.set(0.15, 0.2, 0); k.add(lev);
    const sp = grp(); sp.position.y = 0.3; sp.rotation.order = 'YXZ'; k.add(sp);
    sp.add(at(sphere(0.04, '#D8DDE2', 1), 0, 0, 0), rod([0, 0, 0], [0, 0.03, L * 0.8], 0.03, '#D8DDE2'), rod([0, 0.03, L * 0.8], [0, -0.04, L], 0.03, '#D8DDE2'));
    const mouth = grp(); mouth.position.set(0, -0.05, L); sp.add(mouth);
    mouth.add(at(cyl(0.034, 0.034, 0.03, '#1A1C20', 14), 0, 0, 0));
    const rim = new THREE.Mesh(new THREE.TorusGeometry(0.032, 0.005, 6, 18), mat('#B7BEC6')); rim.rotation.x = PI / 2; rim.position.y = -0.016; mouth.add(rim);
    for (let i = -1; i <= 1; i++) mouth.add(at(box(0.058, 0.004, 0.006, '#AEB5BD'), 0, -0.017, i * 0.014), at(box(0.006, 0.004, 0.058, '#AEB5BD'), i * 0.014, -0.017, 0));   // the grille: light bars on the dark disc
    const led = noShadow(new THREE.Mesh(new THREE.SphereGeometry(o.ledR ?? 0.013, 8, 6), new THREE.MeshBasicMaterial({ color: '#FF2A2A' }))); led.position.set(0.0, -0.018, 0.0); mouth.add(led);
    const glow = noShadow(new THREE.Mesh(new THREE.CircleGeometry(o.glowR ?? 0.032, 18), new THREE.MeshBasicMaterial({ color: '#FF4A4A', transparent: true, opacity: 0.5, depthWrite: false, side: THREE.DoubleSide }))); glow.rotation.x = PI / 2; glow.position.y = -0.024; mouth.add(glow);
    const water = new THREE.Mesh(new THREE.CylinderGeometry(o.flowR ?? 0.014, (o.flowR ?? 0.014) * 1.3, 1, 8), new THREE.MeshLambertMaterial({ color: '#8FCDF2', transparent: true, opacity: 0.85 })); mouth.add(water);
    g.userData.update = t => { sp.rotation.y = kv(o.swivel, t, 0); sp.rotation.x = kv(o.tilt, t, 0); mouth.rotation.x = kv(o.peek, t, 0);   // o.tilt: the spout's pitch (negative lifts it); o.peek: the nozzle turns its opening (negative: toward the front)
      lev.rotation.y = o.leverAt != null ? -1.1 * smooth((t - o.leverAt) / 0.18) : 0;   // o.leverAt: the lever is turned off
      const on = o.lightAt != null && t >= o.lightAt, bl = on ? (((t - o.lightAt) % 0.8) < 0.55 ? 1 : 0.25) : 0; led.visible = on; glow.visible = on; glow.material.opacity = 0.8 * bl; led.scale.setScalar(on ? 0.6 + 0.6 * bl : 1);
      const f = (o.flow || []).some(([a, b]) => t >= a && t <= b); water.visible = f; water.scale.y = o.flowLen ?? 0.3; water.position.y = -(o.flowLen ?? 0.3) / 2 - 0.02; };
    g.userData.update(-1); return g;
  },

  // A black van facing +X (pivot at the floor in its middle; 5 m): a black box van, dark windows, chrome bumpers, no word or emblem; o.stopAt: it
  // brakes (the nose dips and rebounds); its side door at -X slides open from o.doorAt
  fuVan(o) {
    const g = grp(), b = grp(); g.add(b); const K = o.color || '#1C1E22';
    b.add(at(box(3.6, 1.9, 1.9, K, { pivot: 'bottom', outline: 0.012 }), -0.6, 0.45, 0), at(box(1.4, 0.8, 1.9, K, { pivot: 'bottom', outline: 0.012 }), 1.75, 0.45, 0), at(box(0.9, 0.85, 1.86, K, { outline: 0.01, taper: { x: 0.6, z: 1 } }), 1.45, 1.66, 0));
    b.add(at(box(0.04, 0.6, 1.6, '#2E3A46', { noGrain: true }), 1.92, 1.62, 0, 0, 0, 0.5), at(box(0.62, 0.5, 0.03, '#2E3A46', { noGrain: true }), 1.4, 1.62, 0.955));
    b.add(at(box(0.15, 0.18, 1.96, '#C9CED4'), 2.47, 0.55, 0), at(box(0.15, 0.18, 1.96, '#C9CED4'), -2.45, 0.55, 0));
    for (const z of [-0.7, 0.7]) b.add(at(box(0.03, 0.15, 0.3, '#FFF6D8', { emissive: '#7A6A3A' }), 2.46, 0.82, z));
    const sd = at(box(1.1, 1.6, 0.04, '#24272C', { outline: 0.006 }), -0.2, 1.3, 0.97); b.add(sd);
    for (const x of [1.55, -1.55]) for (const z of [-0.88, 0.88]) g.add(at(cyl(0.38, 0.38, 0.28, '#141618', 12), x, 0.38, z, PI / 2), at(cyl(0.18, 0.18, 0.3, '#8A939B', 8), x, 0.38, z, PI / 2));
    g.userData.update = t => { const u = o.stopAt != null ? t - o.stopAt : -1; b.rotation.z = u > 0 && u < 0.8 ? -0.06 * Math.exp(-5 * u) * Math.cos(u * 14) : 0; const d = o.doorAt != null ? smooth((t - o.doorAt) / 0.3) : 0; sd.position.x = -0.2 - 1.0 * d; };
    g.userData.update(-1); return g;
  },

  // Plumber's cap (attach to the head joint, offset to the skull top): a dark navy cap with a peak toward +Z
  fuCap(o) { return grp(at(box(o.w ?? 0.34, 0.1, o.w ?? 0.34, '#1E2E44', { outline: 0.03 }), 0, 0, 0), at(box((o.w ?? 0.34) * 0.9, 0.025, 0.16, '#1E2E44', { outline: 0.03 }), 0, -0.035, (o.w ?? 0.34) / 2 + 0.06)); },

  // A small toolbox (pivot at its handle; carry it in a hand): a red box with a steel handle
  fuToolbox(o) { return grp(at(box(0.36, 0.18, 0.16, '#C23A2E', { outline: 0.03 }), 0, -0.15, 0), rod([-0.1, -0.06, 0], [-0.1, 0, 0], 0.01, '#C9CED4'), rod([0.1, -0.06, 0], [0.1, 0, 0], 0.01, '#C9CED4'), rod([-0.1, 0, 0], [0.1, 0, 0], 0.012, '#C9CED4')); },
};
