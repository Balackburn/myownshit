// « La pizza » (story 91): this man got his pizza cold; the president spoke of national shame; the army re-delivered it by fighter jet; it arrived
// in flames, braked with the street, the pavement arrived before it; he found it overcooked; the general staff decided to cool it on the way: a
// missile took it up to space; it made a crater in his garden; his front door is what is left; at the bottom of the crater, sixty degrees; the
// president opened the crater; the other countries order their pizzas cold; it took him three hours to climb down; one star, it was cold.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere, mat, rng } from './style.js';
import { grp, at, canvasPlane, buildProp, rod, glowSprite } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = x => { const u = clamp01(x), c = 1.70158; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
// a value keyed in time: keys [[t, v], ...] (sorted); eased toward each key over `blend` seconds after it
function keyAt(keys, t, def = 0, blend = 0.2) {
  if (keys == null) return def;
  if (!Array.isArray(keys)) return keys;
  if (!keys.length) return def;
  let v = def, prev = def, t0 = -1e9;
  for (const [kt, kv] of keys) { if (t >= kt) { prev = v; v = kv; t0 = kt; } else break; }
  if (blend <= 0) return v;
  return prev + (v - prev) * smooth((t - t0) / blend);
}
// piecewise linear between keys [[t, v], ...]
function lin(keys, t, def = 0) {
  if (!keys || !keys.length) return def;
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) if (t < keys[i][0]) { const [a, va] = keys[i - 1], [b, vb] = keys[i]; return va + (vb - va) * smooth((t - a) / Math.max(1e-6, b - a)); }
  return keys[keys.length - 1][1];
}
// a damped wobble started at each time of `ts`
function wob(ts, t, a = 1, w = 22, d = 4.3) { let s = 0; for (const t0 of [].concat(ts ?? [])) { const u = t - t0; if (u >= 0) s += a * Math.sin(u * w) * Math.exp(-u * d); } return s; }
// inside one of the windows [[t0, t1], ...] (true: always)
const inWin = (w, t) => w === true || (Array.isArray(w) && w.some(([a, b]) => t >= a && t < b));
const lam = (c, o = {}) => new THREE.MeshLambertMaterial({ color: c, flatShading: true, ...o });
const KRAFT = '#C9995A', KRAFT_IN = '#E2BE84', ICE = '#DDF0FB', CHAR = '#2E2622';
const BLUE = '#2F86E0', GREEN = '#22C044', RED = '#E8402F';

// ---------------------------------------------------------------------------------------------------------------- the stick thermometer
// The running gag: a meat thermometer stuck in every pizza (pivot at the tip of its stick, the stick along +Y, the dial facing +Z): a big round
// dial (o.r 0.14 m: cartoon size, it must read on a phone) with a wide blue zone (with a snowflake) on the left, a narrow green notch at the top
// and a wide red zone (with a flame) on the right, a black needle and a big centre bulb in the colour of the state; o.temp: a value or keys
// [[t, v], ...] with v -1 (deep blue) .. 0 (exactly green) .. +1 (red); the needle swings to each key over o.blend (0.22 s) with a damped
// overshoot (o.wobA 0.2); o.len (0.36) the stick; the back of the dial is a disc in the state colour (it reads from behind too)
function thermoColor(v, c) {
  const a = Math.abs(v), side = v < 0 ? BLUE : RED;
  if (a <= 0.07) return c.set(GREEN);
  if (a >= 0.17) return c.set(side);
  return c.set(GREEN).lerp(new THREE.Color(side), (a - 0.07) / 0.1);
}
function thermo(o) {
  const L = o.len ?? 0.36, R = o.r ?? 0.14, g = grp(), dial = grp(), A = 1.95;
  g.add(cyl(0.011, 0.005, L, '#C9CED3', 6, { pivot: 'bottom' }));
  dial.position.set(0, L + R * 0.98, 0); g.add(dial);
  const rim = cyl(R * 1.1, R * 1.1, 0.034, '#E8EBEE', 24, { outline: 0.008 }); rim.rotation.x = PI / 2; dial.add(rim);
  const face = canvasPlane(2 * R, 2 * R, (c, W, H) => {
    const cx = W / 2, cy = H / 2, r = W * 0.47; c.fillStyle = '#FBFAF4'; c.beginPath(); c.arc(cx, cy, r, 0, TAU); c.fill();
    const arc = (t1, t2, col, r0, r1) => { c.fillStyle = col; c.beginPath(); c.arc(cx, cy, r1, -PI / 2 - t2, -PI / 2 - t1); c.arc(cx, cy, r0, -PI / 2 - t1, -PI / 2 - t2, true); c.closePath(); c.fill(); };
    arc(0.24, 2.2, BLUE, r * 0.5, r * 0.97); arc(-0.17, 0.17, GREEN, r * 0.42, r * 0.99); arc(-2.2, -0.24, RED, r * 0.5, r * 0.97);
    c.strokeStyle = '#FFFFFF'; c.lineWidth = W * 0.022; c.lineCap = 'round';   // a snowflake on the blue
    const sx = cx - Math.sin(1.25) * r * 0.74, sy = cy - Math.cos(1.25) * r * 0.74, sr = r * 0.16;
    for (let k = 0; k < 3; k++) { const a = k * PI / 3; c.beginPath(); c.moveTo(sx - Math.cos(a) * sr, sy - Math.sin(a) * sr); c.lineTo(sx + Math.cos(a) * sr, sy + Math.sin(a) * sr); c.stroke(); }
    const fx = cx + Math.sin(1.25) * r * 0.74, fy = cy - Math.cos(1.25) * r * 0.74, fr = r * 0.17;   // a flame on the red
    c.fillStyle = '#FFE08A'; c.beginPath(); c.moveTo(fx, fy - fr * 1.2); c.quadraticCurveTo(fx + fr, fy, fx + fr * 0.6, fy + fr * 0.7); c.lineTo(fx - fr * 0.6, fy + fr * 0.7); c.quadraticCurveTo(fx - fr, fy, fx, fy - fr * 1.2); c.fill();
    c.strokeStyle = '#2A2C30'; c.lineWidth = W * 0.02; c.beginPath(); c.arc(cx, cy, r, 0, TAU); c.stroke();
  }, { res: 256, transparent: true, emissive: 0.35 });
  face.position.z = 0.0175; dial.add(face);
  const stateM = mat(BLUE, { unique: true, noGrain: true }), col = new THREE.Color();
  const back = cyl(R * 1.02, R * 1.02, 0.004, BLUE, 20, { material: stateM }); back.rotation.x = PI / 2; back.position.z = -0.019; dial.add(back);
  const needle = grp(at(box(0.02, R * 0.86, 0.008, '#1E1E22', { pivot: 'bottom' }), 0, 0, 0)); needle.position.z = 0.024; dial.add(needle);
  const bulb = sphere(R * 0.34, BLUE, 2, { material: stateM }); bulb.scale.z = 0.45; bulb.position.z = 0.03; dial.add(bulb);
  const shine = sphere(R * 0.09, '#FFFFFF', 1, { noGrain: true, emissive: '#FFFFFF' }); shine.position.set(-R * 0.1, R * 0.1, 0.045); dial.add(shine);
  const keys = Array.isArray(o.temp) ? o.temp : null, kt = keys ? keys.map(k => k[0]).filter(x => x > 0) : [];
  g.userData.update = t => {
    const v = Math.max(-1.1, Math.min(1.1, keyAt(o.temp ?? -1, t, keys ? keys[0][1] : (o.temp ?? -1), o.blend ?? 0.22) + wob(kt.map(x => x + (o.blend ?? 0.22) * 0.6), t, o.wobA ?? 0.2, 24, 5)));
    needle.rotation.z = -v * A; thermoColor(v, col); stateM.color.copy(col); stateM.emissive.copy(col).multiplyScalar(0.28);
  };
  g.userData.update(0); g.userData.dialY = L + R * 0.98; return g;
}

// ---------------------------------------------------------------------------------------------------------------- the pizza itself
// a whole pizza (pivot at the middle of its bottom), radius R: crust, cheese, pepperoni, basil; state 'fresh' or 'charred'; o.missing: one slice gone
function pie(R, o = {}) {
  const g = grp(), ch = o.charred, r = rng(o.seed || 5), t0 = o.missing ? PI / 8 : 0, tl = o.missing ? TAU - PI / 4 : TAU;
  const disc = (rr, h, c, y) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(rr, rr, h, 24, 1, false, t0, tl), mat(c)); m.position.y = y + h / 2; m.castShadow = m.receiveShadow = true; return m; };
  g.add(disc(R, 0.03, ch ? '#2B2420' : '#D9A35A', 0), disc(R * 0.86, 0.012, ch ? '#1A1614' : '#C8402E', 0.03), disc(R * 0.8, 0.01, ch ? '#221C18' : '#F4CF52', 0.04));
  const ang = a => o.missing ? (Math.abs(((a % TAU) + TAU) % TAU) < PI / 8 || Math.abs(((a % TAU) + TAU) % TAU) > TAU - PI / 8) : false;
  for (let i = 0; i < 9; i++) { const a = i / 9 * TAU + r() * 0.3, d = R * (0.25 + 0.45 * r()); if (ang(a + PI / 2)) continue;
    g.add(at(cyl(R * 0.13, R * 0.13, 0.012, ch ? '#3A2A22' : '#B32A22', 10), Math.cos(a) * d, 0.056, Math.sin(a) * d)); }
  for (let i = 0; i < 5; i++) { const a = r() * TAU, d = R * (0.2 + 0.5 * r()); if (ang(a + PI / 2)) continue; g.add(at(box(R * 0.12, 0.008, R * 0.07, ch ? '#2A2622' : '#3E8A3A'), Math.cos(a) * d, 0.058, Math.sin(a) * d, 0, r() * 3, 0)); }
  if (ch) for (let i = 0; i < 7; i++) { const a = r() * TAU, d = R * r() * 0.8; g.add(at(sphere(R * 0.035, '#FF7A22', 0, { emissive: '#FF5A10', noGrain: true }), Math.cos(a) * d, 0.055, Math.sin(a) * d)); }
  return g;
}
// frost over a thing (pivot where you put it): a pale see-through layer and white crystals that grow with v (0..1)
function frostCap(w, d, y, seed = 9) {
  const g = grp(), r = rng(seed), m = mat('#F4FBFF', { unique: true, noGrain: true, opacity: 0.0 }), cr = [];
  const lay = new THREE.Mesh(new THREE.BoxGeometry(w, 0.006, d), m); lay.position.y = y; g.add(lay);
  for (let i = 0; i < 26; i++) { const c = new THREE.Mesh(new THREE.TetrahedronGeometry(0.018 + r() * 0.02), mat('#FFFFFF', { noGrain: true, emissive: '#C8E6F8' })); c.position.set((r() - 0.5) * w * 0.95, y + 0.008, (r() - 0.5) * d * 0.95); c.rotation.set(r() * 3, r() * 3, r() * 3); g.add(c); cr.push(c); }
  g.userData.set = v => { m.opacity = 0.62 * v; m.transparent = true; lay.visible = v > 0.01; cr.forEach((c, i) => { const k = clamp01(v * 1.6 - hsh(i) * 0.6); c.visible = k > 0.02; c.scale.setScalar(Math.max(0.01, k)); }); };
  g.userData.set(0); return g;
}

// ---------------------------------------------------------------------------------------------------------------- the pizza box
// A pizza box (pivot at the middle of its bottom, the hinge at the back -Z, the front +Z): o.w (0.62) square, o.h (0.075) deep, plain kraft with a
// red band round the lid and a drawn pizza circle on top (no words, no brand); o.open: angle (rad) or keys [[t, rad]] (each opening snaps with a
// small bounce); o.pizza (true): the pie inside (o.charred: black and glowing, o.missing: a slice gone); o.thermo: the stick thermometer's
// temperature (see thermo) stuck at o.tAt [x, z] (local), o.tR (0.14) dial, o.tLen (0.36), o.tRy (0) turn of the dial; o.fire: true or
// [[t0, t1]]: cartoon flames on the box; o.smoke: a dark wisp; o.frost: 0..1 or keys: icy lid and walls, crystals, icicles under the front edge;
// o.puffAt: a cold white puff out of the box at that time; o.side (±1): the hinge on the -X / +X side instead of the back (the thermometer stays
// placed in the prop's own frame); o.glow: 0..1 or keys: the box glows red-hot; o.charredBox: the box itself burnt
// black; o.scorch: the kraft browned by the flames but still a box; o.fireK keys [[t, 0..1]]: the flames' strength (they die down smoothly
// into the smoke instead of cutting out); o.s (1) overall size
function pizzaBox(o = {}) {
  const S = o.s ?? 1, W = o.w ?? 0.62, H = o.h ?? 0.075, g = grp(), b = grp(); b.scale.setScalar(S); g.add(b);
  const K = mat(o.charredBox ? CHAR : (o.scorch ? '#7A5634' : KRAFT), { unique: true }), KI = mat(o.charredBox ? '#3A302A' : KRAFT_IN, { unique: true });
  b.add(at(box(W, 0.012, W, KRAFT, { material: KI }), 0, 0.006, 0));
  b.add(at(box(W, H, 0.012, KRAFT, { material: K, outline: 0.004 }), 0, H / 2, W / 2), at(box(W, H, 0.012, KRAFT, { material: K, outline: 0.004 }), 0, H / 2, -W / 2),
    at(box(0.012, H, W, KRAFT, { material: K, outline: 0.004 }), W / 2, H / 2, 0), at(box(0.012, H, W, KRAFT, { material: K, outline: 0.004 }), -W / 2, H / 2, 0));
  const lid = grp(); lid.position.set(0, H, -W / 2); b.add(lid);
  lid.add(at(box(W + 0.01, 0.012, W + 0.01, KRAFT, { material: K, outline: 0.004 }), 0, 0.006, W / 2), at(box(W + 0.01, H * 0.85, 0.012, KRAFT, { material: K }), 0, -H * 0.42, W + 0.004));
  if (!o.charredBox) {
    const top = canvasPlane(W * 0.96, W * 0.96, (c, Wd, Hd) => { c.fillStyle = KRAFT; c.fillRect(0, 0, Wd, Hd); c.strokeStyle = '#C23A2E'; c.lineWidth = Wd * 0.05; c.strokeRect(Wd * 0.04, Hd * 0.04, Wd * 0.92, Hd * 0.92);
      c.fillStyle = '#C23A2E'; c.beginPath(); c.arc(Wd / 2, Hd * 0.55, Wd * 0.22, 0, TAU); c.fill(); c.fillStyle = '#F2C94C'; c.beginPath(); c.arc(Wd / 2, Hd * 0.55, Wd * 0.17, 0, TAU); c.fill();
      c.fillStyle = '#C23A2E'; [[-0.07, -0.05], [0.06, 0.02], [-0.02, 0.08], [0.08, -0.08]].forEach(([x, y]) => { c.beginPath(); c.arc(Wd * (0.5 + x), Hd * (0.55 + y), Wd * 0.03, 0, TAU); c.fill(); });
      c.strokeStyle = '#8A5A2A'; c.lineWidth = Wd * 0.018; for (const x of [0.4, 0.5, 0.6]) { c.beginPath(); c.moveTo(Wd * x, Hd * 0.28); c.bezierCurveTo(Wd * (x - 0.03), Hd * 0.22, Wd * (x + 0.03), Hd * 0.17, Wd * x, Hd * 0.1); c.stroke(); } }, { res: 256 });
    top.rotation.x = -PI / 2; top.position.set(0, 0.0125, W / 2); lid.add(top);
  }
  if (o.pizza !== false) { const p = pie(W * 0.44, { charred: o.charred, missing: o.missing, seed: o.seed }); p.position.y = 0.012; b.add(p); }
  let th = null; if (o.thermo != null) { th = thermo({ temp: o.thermo, r: o.tR ?? 0.14, len: o.tLen ?? 0.36, blend: o.tBlend, wobA: o.wobA }); const ta = o.tAt || [0.07, 0.06]; th.position.set(ta[0] * S, 0.04 * S, ta[1] * S); th.scale.setScalar(S); th.rotation.set(o.tTilt ?? -0.12, o.tRy ?? 0, o.tRoll ?? 0.1); g.add(th); }
  if (o.side) b.rotation.y = o.side * PI / 2;   // the hinge on a side (1: at -X, -1: at +X): the lid stands beside the box, not between it and whoever holds it
  const fz = frostCap(W, W, 0.0, o.seed || 9); fz.position.set(0, 0.013, W / 2); lid.add(fz);
  const fzIn = frostCap(W * 0.86, W * 0.86, 0.065, (o.seed || 9) + 4); b.add(fzIn);
  const ice = grp(); for (let i = 0; i < 9; i++) { const c = new THREE.Mesh(new THREE.ConeGeometry(0.012 + hsh(i) * 0.01, 1, 5), mat('#EAF7FF', { noGrain: true, emissive: '#9CC8E6' })); c.rotation.x = PI; c.position.set(-W / 2 + 0.04 + i * (W - 0.08) / 8, 0, 0); c.userData.l = 0.04 + hsh(i + 3) * 0.07; ice.add(c); }
  ice.position.set(0, 0.0, W / 2 + 0.012); b.add(ice);
  let fire = null, fglow = null; if (o.fire) {
    fire = buildProp('flameField', { points: [[0, H, 0, 0.32], [0.18, H, 0.12, 0.22, 0.6], [-0.2, H, -0.08, 0.24, 1.1], [0.05, H, -0.2, 0.2, 2.0], [-0.1, H, 0.2, 0.18, 0.3]], seed: o.seed || 73 });
    b.add(fire); fglow = glowSprite('#FF8A2A', 1.6, 0.85); fglow.position.y = 0.3; b.add(fglow);
  }
  let smoke = null; if (o.smoke) { smoke = buildProp('softWisp', { n: 14, rise: 1.8, life: 1.7, s0: 0.1, s1: 0.5, color: o.smokeColor || '#4A4440', opacity: 0.7, drift: [0.25, -0.1] }); smoke.position.y = 0.12; b.add(smoke); }
  let puff = null; if (o.puffAt != null) { puff = buildProp('softDust', { at: o.puffAt, n: 10, size: o.puffS ?? 0.2, rise: 0.9, spread: 0.45, life: 0.9, color: '#EEF8FF', opacity: 0.6 }); puff.position.y = 0.1; b.add(puff); }
  const hglow = glowSprite('#FF5A1A', 1.4, 0); hglow.position.y = 0.06; b.add(hglow);
  const kraft = new THREE.Color(o.charredBox ? CHAR : (o.scorch ? '#7A5634' : KRAFT)), icy = new THREE.Color(ICE), hot = new THREE.Color('#FF5A10');
  const openKeys = Array.isArray(o.open) ? o.open : null, okt = openKeys ? openKeys.map(k => k[0]).filter(x => x > 0) : [];
  g.userData.update = t => {
    const ang = keyAt(o.open ?? 0, t, openKeys ? openKeys[0][1] : (o.open ?? 0), o.openBlend ?? 0.12) + wob(okt.map(x => x + (o.openBlend ?? 0.12)), t, 0.14, 26, 6);
    lid.rotation.x = -ang;
    const fr = keyAt(o.frost ?? 0, t, 0, 0.5), gl = keyAt(o.glow ?? 0, t, 0, 0.3);
    K.color.copy(kraft).lerp(icy, fr * 0.85); K.emissive.copy(hot).multiplyScalar(gl * 0.75); KI.color.set(o.charredBox ? '#3A302A' : KRAFT_IN).lerp(icy, fr * 0.7);
    fz.userData.set(fr); fzIn.userData.set(ang > 0.3 ? fr : 0); ice.children.forEach((c, i) => { const l = c.userData.l * clamp01(fr * 1.4 - hsh(i + 7) * 0.4); c.visible = l > 0.003; c.scale.set(1, Math.max(0.001, l), 1); c.position.y = -l / 2; });
    hglow.material.opacity = 0.9 * gl; hglow.visible = gl > 0.01;
    if (fire) { const fk = o.fireK ? lin(o.fireK, t, 1) : (inWin(o.fire, t) ? 1 : 0), on = fk > 0.02; fire.visible = on; fglow.visible = on; if (on) { fire.userData.update(t); fire.scale.set(0.4 + 0.6 * fk, fk, 0.4 + 0.6 * fk); fglow.material.opacity = (0.7 + 0.2 * Math.sin(t * 23)) * fk; } }
    if (smoke) smoke.userData.update(t); if (puff) puff.userData.update(t); if (th) th.userData.update(t);
  };
  g.userData.update(0); g.userData.grip = [0, 0.04 * S, W / 2 * S]; return g;
}

// ---------------------------------------------------------------------------------------------------------------- a slice
// A slice held by its crust (pivot at the middle of the crust, the tip toward -Z, the top +Y): o.r (0.34) long, a flat wedge of dough with a
// cheese layer and pepperoni set into it, a round rolled crust along the back edge; its front half is hinged at mid-length and sags by o.droop
// (rad, the tip going down); o.charred: lighter charred greys with a few glowing specks; o.crumbleAt: it falls to dust in 0.14 s, crumbs drop
// o.fall (1.3 m) and a dark puff rises; o.frost: blue-white frosted colours with thin frost flakes lying flat on the cheese and tiny icicles under
// the tip (nothing floats above it)
function pizzaSlice(o = {}) {
  const R = o.r ?? 0.34, g = grp(), sl = grp(), ch = o.charred, fr = o.frost && !ch, half = PI / 9, W2 = R * Math.sin(half), ZM = R * 0.48;
  const C = ch ? { dough: '#6A5C52', cheese: '#4A403A', crust: '#7A6656', top: '#3A302A' } : fr ? { dough: '#D6E2EC', cheese: '#EEF6FC', crust: '#C9D8E6', top: '#B88A9A' } : { dough: '#D9A35A', cheese: '#F4CF52', crust: '#C98A42', top: '#B32A22' };
  const hw = y => W2 * (1 - y / R);   // half width at distance y from the crust
  const part = (y0, y1, th, col, inset = 0, lift = 0) => { const sh = new THREE.Shape(); sh.moveTo(-hw(y0) + inset, y0 - y0); sh.lineTo(hw(y0) - inset, 0); sh.lineTo(Math.max(0.001, hw(y1) - inset), y1 - y0); sh.lineTo(-Math.max(0.001, hw(y1) - inset), y1 - y0); sh.closePath();
    const geo = new THREE.ExtrudeGeometry(sh, { depth: th, bevelEnabled: false }); geo.rotateX(-PI / 2); const m = new THREE.Mesh(geo, mat(col)); m.position.y = lift; m.castShadow = true; return m; };
  const tip = grp(); tip.position.z = -ZM; sl.add(tip);
  sl.add(part(0, ZM, 0.03, C.dough), part(0.02, ZM, 0.012, C.cheese, 0.012, 0.03));
  tip.add(part(ZM, R, 0.03, C.dough), part(ZM, R - 0.015, 0.012, C.cheese, 0.012, 0.03));
  const crust = cyl(0.032, 0.032, 2 * W2 + 0.02, C.crust, 8, { outline: 0.004 }); crust.rotation.z = PI / 2; crust.position.set(0, 0.03, 0); sl.add(crust);
  const topY = 0.042;
  if (!ch) { for (const [x, y, host] of [[0.0, 0.1, sl], [0.03, 0.2, sl], [-0.025, 0.06, tip], [0.01, 0.13, tip]]) { const d = cyl(0.03 * R / 0.34, 0.03 * R / 0.34, 0.008, C.top, 10); d.position.set(x * R / 0.34, topY, host === tip ? -(y * R / 0.34 * 0.9) : -(y * R / 0.34) * 0.9); host.add(d); } }
  if (ch) for (let i = 0; i < 4; i++) sl.add(at(sphere(0.011, '#FF8A3A', 0, { emissive: '#FF5A10', noGrain: true }), (hsh(i) - 0.5) * 0.06, topY, -0.04 - hsh(i + 2) * ZM * 0.8));
  if (fr) { for (let i = 0; i < 14; i++) { const host = i % 2 ? tip : sl, yy = hsh(i + 5) * (i % 2 ? (R - ZM) * 0.7 : ZM * 0.8); const f = box(0.018 + 0.015 * hsh(i), 0.003, 0.012, '#FFFFFF', { noGrain: true, emissive: '#B8D8F0' }); f.position.set((hsh(i + 1) - 0.5) * hw(yy + (i % 2 ? ZM : 0)) * 1.2, topY + 0.001, -yy - 0.02); f.rotation.y = hsh(i) * 3; host.add(f); }
    for (let i = 0; i < 3; i++) { const c = new THREE.Mesh(new THREE.ConeGeometry(0.007, 0.04 + 0.02 * hsh(i), 5), mat('#EAF7FF', { noGrain: true, emissive: '#9CC8E6' })); c.rotation.x = PI; c.position.set((i - 1) * 0.015, -0.015, -(R - ZM) * (0.4 + 0.2 * i)); tip.add(c); } }
  tip.rotation.x = -(o.droop ?? 0);
  g.add(sl);
  const crumbs = [], cg = grp(); g.add(cg);
  if (o.crumbleAt != null) for (let i = 0; i < 22; i++) { const m = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.025, 0.03), mat(i % 3 ? '#3A322C' : '#5A4C42')); m.userData.p = [(hsh(i) - 0.5) * 0.12, 0.03, -hsh(i + 4) * R, (hsh(i + 9) - 0.5) * 0.8, hsh(i + 11) * 0.6]; m.visible = false; cg.add(m); crumbs.push(m); }
  let dust = null; if (o.crumbleAt != null) { dust = buildProp('softDust', { at: o.crumbleAt, n: 12, size: 0.22, rise: 0.35, spread: 0.35, life: 1.0, color: '#3E3834', opacity: 0.85 }); dust.position.set(0, 0.05, -R * 0.45); g.add(dust); }
  g.userData.update = t => {
    if (o.crumbleAt == null) return;
    const u = t - o.crumbleAt, k = clamp01(u / 0.14); sl.visible = k < 1; sl.scale.set(1 - 0.3 * k, 1 - 0.8 * k, 1 - 0.2 * k);
    crumbs.forEach(m => { m.visible = u >= 0; if (u < 0) return; const [x, y, z, vx, vy] = m.userData.p, yy = Math.max(-(o.fall ?? 1.3), y + vy * u - 4.9 * u * u); m.position.set(x + vx * u * 0.4, yy, z); m.rotation.set(u * 6 + x * 20, u * 4, 0); });
    dust.userData.update(t);
  };
  g.userData.update(0); g.userData.grip = [0, 0, 0]; g.userData.tip = [0, 0, -R]; return g;
}

// ---------------------------------------------------------------------------------------------------------------- the rating phone
// The phone with the rating screen (pivot at its middle, screen +Z): a black handset o.w (0.24) wide, twice as tall; on a dark screen a pizza
// slice icon at the top and a row of five grey star shapes (no words); at o.rateAt the first star fills yellow with a pop and a ring; o.tapAt:
// the first star dips like a pressed key
function ratingPhone(o = {}) {
  const w = o.w ?? 0.24, h = w * 2.0, g = grp();
  g.add(at(box(w, h, 0.032, '#1C1E24', { outline: 0.006 }), 0, 0, 0));
  const scr = canvasPlane(w * 0.88, h * 0.9, (c, W, H) => { const gr = c.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#1F2B3C'); gr.addColorStop(1, '#141C28'); c.fillStyle = gr; c.fillRect(0, 0, W, H);
    c.fillStyle = '#E8A33A'; c.beginPath(); c.moveTo(W * 0.5, H * 0.36); c.lineTo(W * 0.3, H * 0.1); c.quadraticCurveTo(W * 0.5, H * 0.03, W * 0.7, H * 0.1); c.closePath(); c.fill();
    c.fillStyle = '#F4CF52'; c.beginPath(); c.moveTo(W * 0.5, H * 0.32); c.lineTo(W * 0.34, H * 0.12); c.quadraticCurveTo(W * 0.5, H * 0.07, W * 0.66, H * 0.12); c.closePath(); c.fill();
    c.fillStyle = '#C8402E'; [[0.47, 0.15], [0.56, 0.18], [0.5, 0.24]].forEach(([x, y]) => { c.beginPath(); c.arc(W * x, H * y, W * 0.035, 0, TAU); c.fill(); });
    c.fillStyle = '#3A475A'; c.fillRect(W * 0.12, H * 0.72, W * 0.76, H * 0.012); c.fillRect(W * 0.2, H * 0.78, W * 0.6, H * 0.012); }, { res: 256, emissive: 0.55 });
  scr.position.z = 0.0165; g.add(scr);
  const starShape = (ro, ri) => { const s = new THREE.Shape(); for (let i = 0; i < 10; i++) { const a = PI / 2 + i * PI / 5, rr = i % 2 ? ri : ro; const x = Math.cos(a) * rr, y = Math.sin(a) * rr; if (i === 0) s.moveTo(x, y); else s.lineTo(x, y); } s.closePath(); return s; };
  const ro = w * 0.092, sg = new THREE.ExtrudeGeometry(starShape(ro, ro * 0.45), { depth: 0.006, bevelEnabled: false });
  const sy = -h * 0.06, gap = w * 0.168, stars = [];
  for (let i = 0; i < 5; i++) { const m = new THREE.Mesh(sg, new THREE.MeshBasicMaterial({ color: '#9AA3AE' })); m.position.set((i - 2) * gap, sy, 0.017); g.add(m); stars.push(m); }
  const gold = new THREE.Mesh(new THREE.ExtrudeGeometry(starShape(ro * 1.08, ro * 0.5), { depth: 0.008, bevelEnabled: false }), new THREE.MeshBasicMaterial({ color: '#FFC21A' })); gold.position.set(-2 * gap, sy, 0.02); g.add(gold);
  const ring = new THREE.Mesh(new THREE.RingGeometry(ro * 1.2, ro * 1.45, 20), new THREE.MeshBasicMaterial({ color: '#FFD84A', transparent: true, opacity: 0, depthWrite: false })); ring.position.set(-2 * gap, sy, 0.024); g.add(ring);
  g.userData.update = t => {
    const u = o.rateAt == null ? -1 : t - o.rateAt; gold.visible = u >= 0; if (u >= 0) gold.scale.setScalar(Math.max(0.01, outBack(u / 0.2)));
    ring.visible = u >= 0 && u < 0.4; if (ring.visible) { ring.scale.setScalar(1 + u * 3); ring.material.opacity = 0.9 * (1 - u / 0.4); }
    const v = o.tapAt == null ? 0 : Math.max(0, 1 - Math.abs(t - o.tapAt) / 0.08); stars[0].position.z = 0.017 - 0.006 * v;
  };
  g.userData.update(0); g.userData.star1 = [-2 * gap, sy, 0.03]; return g;
}

// ---------------------------------------------------------------------------------------------------------------- the jet with the box
// The fighter jet that re-delivers it (a plainJet: no roundels; the lettering on its flanks hidden too), front +Z, with ONE pizza box bolted
// under its left wing (o.side 1: +X) on a pylon with two steel straps, like a missile: o.boxS (1.6) the box's size; o.glow 0..1 or keys: the
// box glows red-hot; o.flames [[t0, t1]]: it catches fire; o.stretch keys [[t, v]]: a cartoon stretch along +Z (v 0.4: 40 % longer, thinner),
// with a squash back; o.burner / o.glowS / o.gear as on the fighterJet; o.shake: the jet trembles before take-off; o.upright: the box hangs on
// its edge under the pylon, its printed lid facing +Z (it reads from the front instead of as a dark slab in the wing's shadow); o.boxYaw (rad): that
// face turned toward +X; o.slaps [t, ...]: the hanging box rocks with a damped shake at each slap
function jetBox(o = {}) {
  const g = grp(), inner = grp(); g.add(inner);
  const j = buildProp('plainJet', { burner: o.burner ?? 0.9, glow: o.glowS ?? 0, gear: o.gear, hotCore: true }); inner.add(j);
  j.traverse(m => { const p = m.geometry && m.geometry.parameters; if (m.isMesh && m.geometry.type === 'PlaneGeometry' && p && Math.abs(p.width - 2.6) < 1e-6 && Math.abs(p.height - 0.45) < 1e-6) m.visible = false; });
  const sd = o.side ?? 1, X = sd * 3.1, Z = -1.1, S = o.boxS ?? 1.6, bw = 0.62 * S;
  inner.add(at(box(0.14, 0.42, 1.7, '#4A4F56', { outline: 0.005 }), X, 1.32, Z));
  const bx = pizzaBox({ s: S, pizza: false, glow: o.glow, smoke: o.smoke, seed: 21 }); bx.position.set(X, 1.1 - 0.075 * S, Z); inner.add(bx);
  if (o.upright) { bx.rotation.set(PI / 2, 0, 0); bx.rotation.order = 'YXZ'; bx.rotation.y = o.boxYaw ?? 0; bx.position.set(X, 1.1 - bw / 2 - 0.02, Z); for (const dx of [-0.3, 0.3]) inner.add(at(box(0.08, 0.12, 0.14, '#9AA0A6', { outline: 0.004 }), X + dx * S, 1.07, Z)); }
  else for (const dz of [-0.3, 0.3]) inner.add(at(box(bw + 0.06, 0.035, 0.07, '#9AA0A6', { outline: 0.004 }), X, 1.1 + 0.01, Z + dz * S), at(box(0.035, 0.075 * S + 0.07, 0.07, '#9AA0A6'), X + bw / 2 + 0.03, 1.1 - 0.0375 * S, Z + dz * S), at(box(0.035, 0.075 * S + 0.07, 0.07, '#9AA0A6'), X - bw / 2 - 0.03, 1.1 - 0.0375 * S, Z + dz * S));
  let jf = null, jg = null; if (o.flames) { jf = buildProp('flameField', { points: [[0, 0, 0, 0.5], [0.25, -0.1, -0.2, 0.35, 0.8], [-0.25, -0.1, -0.25, 0.4, 1.7]], seed: 23 }); jf.position.set(X, 1.1 - bw * 0.3, Z - 0.1); jf.rotation.x = -1.2; inner.add(jf);
    jg = glowSprite('#FF7A2A', 3.2, 0.9); jg.position.set(X, 1.1 - bw / 2, Z - 0.3); inner.add(jg); }
  const hg = glowSprite('#FF4A10', 2.6, 0); hg.position.set(X, 1.1 - bw / 2, Z); inner.add(hg);
  g.userData.update = t => {
    if (jf) { const on = inWin(o.flames, t); jf.visible = jg.visible = on; if (on) jf.userData.update(t); }
    hg.material.opacity = 0.9 * keyAt(o.glow ?? 0, t, 0, 0.3);
    if (o.upright && o.slaps) { const w = wob(o.slaps, t, 0.22, 30, 6); bx.rotation.z = w; bx.position.x = X + 0.04 * w; }
    const v = lin(o.stretch, t, 0); inner.scale.set(1 - 0.3 * v, 1 - 0.25 * v, 1 + v);
    const sh = inWin(o.shake, t) ? 1 : 0; inner.position.set(0.02 * sh * Math.sin(t * 71), 0.015 * sh * Math.sin(t * 53), 0);
    bx.userData.update(t); j.userData.update?.(t);
  };
  g.userData.update(0); g.userData.box = [X, 1.1, Z]; return g;
}

// ---------------------------------------------------------------------------------------------------------------- the missile
// The missile that takes it to space (pivot at the middle of its body, the nose +Y): a white body o.len (5) long with red bands and four red fins,
// a flat cradle on a cut nose with the pizza box strapped on top (o.boxS 1.4), the box frosting over with o.frost (0..1 or keys), a flame and a
// glow at the nozzle (o.flame 1), and a white smoke trail o.trail (16 m) of soft puffs behind it
function pizzaMissile(o = {}) {
  const L = o.len ?? 5, Rr = 0.38, g = grp();
  g.add(at(cyl(Rr, Rr, L, '#EEF0F2', 14, { outline: 0.008 }), 0, 0, 0), at(cyl(Rr * 1.01, Rr * 1.01, 0.3, '#D23A2E', 14), 0, L * 0.3, 0), at(cyl(Rr * 1.01, Rr * 1.01, 0.3, '#D23A2E', 14), 0, -L * 0.25, 0));
  g.add(at(cyl(0.2, Rr, 0.9, '#EEF0F2', 14, { outline: 0.008 }), 0, L / 2 + 0.45, 0), at(cyl(0.42, 0.22, 0.08, '#5A6068', 12), 0, L / 2 + 0.94, 0));
  for (let i = 0; i < 4; i++) { const a = i * PI / 2 + PI / 4; g.add(at(box(0.06, 1.1, 0.75, '#D23A2E', { taper: { x: 1, z: 0.35 }, outline: 0.01 }), Math.sin(a) * (Rr + 0.33), -L / 2 + 0.5, Math.cos(a) * (Rr + 0.33), 0, a, 0)); }
  g.add(at(cyl(Rr * 0.8, Rr * 0.6, 0.4, '#3A3E44', 12), 0, -L / 2 - 0.2, 0));
  const S = o.boxS ?? 1.4, bw = 0.62 * S, top = L / 2 + 0.98;
  const bx = pizzaBox({ s: S, pizza: false, frost: o.frost, seed: 31 }); bx.position.set(0, top, 0); g.add(bx);
  for (const dx of [-0.25, 0.25]) { const x = dx * S; g.add(rod([x, top + 0.075 * S + 0.012, -bw / 2 - 0.01], [x, top + 0.075 * S + 0.012, bw / 2 + 0.01], 0.022, '#2E3036'), rod([x, top + 0.075 * S, bw / 2 + 0.01], [x * 0.5, L / 2 + 0.2, Rr * 0.95], 0.022, '#2E3036'), rod([x, top + 0.075 * S, -bw / 2 - 0.01], [x * 0.5, L / 2 + 0.2, -Rr * 0.95], 0.022, '#2E3036')); }
  const fl = grp(), f1 = new THREE.Mesh(new THREE.ConeGeometry(0.34, 1.8, 10), new THREE.MeshBasicMaterial({ color: '#FFE9A8' })), f2 = new THREE.Mesh(new THREE.ConeGeometry(0.5, 2.6, 10), new THREE.MeshBasicMaterial({ color: '#FF8A2A', transparent: true, opacity: 0.7, depthWrite: false }));
  f1.rotation.x = PI; f2.rotation.x = PI; f1.position.y = -0.9; f2.position.y = -1.3; fl.add(f1, f2); fl.position.y = -L / 2 - 0.4; g.add(fl);
  const gw = glowSprite('#FFB04A', 3.2, 0.9); gw.position.y = -L / 2 - 0.8; g.add(gw);
  const cv = document.createElement('canvas'); cv.width = cv.height = 64; const x = cv.getContext('2d'); const gr = x.createRadialGradient(32, 32, 2, 32, 32, 31); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.6, 'rgba(255,255,255,0.5)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = gr; x.fillRect(0, 0, 64, 64);
  const tex = new THREE.CanvasTexture(cv), puffs = [], NT = 22, TL = o.trail ?? 16;
  for (let i = 0; i < NT; i++) { const m = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, color: '#F4F2EE', transparent: true, opacity: 0.8, depthWrite: false })); g.add(m); puffs.push(m); }
  g.userData.update = t => {
    const fk = o.flame ?? 1; fl.visible = fk > 0; fl.scale.set(1, fk * (1 + 0.2 * Math.sin(t * 40) + 0.1 * Math.sin(t * 23)), 1); gw.visible = fk > 0;
    puffs.forEach((m, i) => { const u = ((i + (t * 6) % 1) / NT); m.position.set(0.15 * Math.sin(i * 1.7 + t), -L / 2 - 1.6 - u * TL, 0.15 * Math.cos(i * 1.3)); const s = 0.8 + u * 3.2; m.scale.set(s, s, 1); m.material.opacity = 0.85 * (1 - u); });
    bx.userData.update(t);
  };
  g.userData.update(0); g.userData.box = [0, top, 0]; return g;
}

// ---------------------------------------------------------------------------------------------------------------- the war-room map
// The general staff's map table (pivot at the floor under its middle, the long side along X, the viewers on +Z): a dark table 2.6 x 1.7, 0.92
// high, with a drawn elevation chart on top: a strip of ground with little houses at the bottom (+Z; his has a red roof), blue sky with a band
// of white clouds across the middle, dark space with stars at the far side (-Z) and a big pale-blue snowflake there; a white chalk arrow climbs
// from his house up the left to the snowflake and comes back down the right to his house (arrowhead); a small pizza-box token rides the arrow:
// o.token keys [[t, u]] (u 0: his house, 1: the snowflake, 2: back home); o.tokS (0.24) its size, o.tokGlow: a warm halo that size; no words
const MAP_PATH = [[[-0.05, 0.5], [-1.05, 0.35], [-0.95, -0.62], [-0.08, -0.56]], [[0.08, -0.56], [0.95, -0.62], [1.05, 0.35], [0.1, 0.48]]];
function bez(p, u) { const a = 1 - u; return [0, 1].map(i => a * a * a * p[0][i] + 3 * a * a * u * p[1][i] + 3 * a * u * u * p[2][i] + u * u * u * p[3][i]); }
function pizzaWarMap(o = {}) {
  const Wt = 2.6, Dt = 1.7, Ht = 0.92, g = grp();
  g.add(at(box(Wt, 0.08, Dt, '#3E2E22', { outline: 0.008 }), 0, Ht - 0.04, 0));
  for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(at(box(0.1, Ht - 0.08, 0.1, '#2E2219', { pivot: 'bottom' }), sx * (Wt / 2 - 0.12), 0, sz * (Dt / 2 - 0.12)));
  const mw = Wt - 0.12, md = Dt - 0.12, ux = x => (x + mw / 2) / mw, uz = z => (z + md / 2) / md;
  const map = canvasPlane(mw, md, (c, W, H) => {
    const gr = c.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#141C38'); gr.addColorStop(0.3, '#24345E'); gr.addColorStop(0.55, '#5E9AD0'); gr.addColorStop(0.85, '#9CCBEA'); gr.addColorStop(0.86, '#6FA858'); gr.addColorStop(1, '#5E9448');
    c.fillStyle = gr; c.fillRect(0, 0, W, H);
    const r = rng(4); c.fillStyle = '#FFFFFF'; for (let i = 0; i < 60; i++) { const x = r() * W, y = r() * H * 0.28; c.fillRect(x, y, 2 + r() * 2, 2 + r() * 2); }
    c.fillStyle = 'rgba(255,255,255,0.92)'; for (let i = 0; i < 9; i++) { const x = W * (0.04 + i * 0.12), y = H * (0.52 + 0.03 * Math.sin(i * 2.1)); for (const [dx, dy, rr] of [[0, 0, 0.05], [0.04, -0.02, 0.06], [0.08, 0.005, 0.045]]) { c.beginPath(); c.arc(x + dx * W * 0.5, y + dy * H, rr * H, 0, TAU); c.fill(); } }
    for (let i = 0; i < 7; i++) { const x = W * (0.08 + i * 0.14), y = H * 0.885, mine = i === 3; c.fillStyle = mine ? '#F2E2B0' : '#E8E0D0'; c.fillRect(x - W * 0.035, y, W * 0.07, H * 0.08); c.fillStyle = mine ? '#D2322A' : '#7A6A5E'; c.beginPath(); c.moveTo(x - W * 0.045, y); c.lineTo(x, y - H * 0.065); c.lineTo(x + W * 0.045, y); c.fill(); c.fillStyle = '#3A4A5A'; c.fillRect(x - W * 0.008, y + H * 0.035, W * 0.016, H * 0.045); }
    const sx = W * 0.5, sy = H * 0.13, sr = H * 0.12; c.strokeStyle = '#D6F0FF'; c.lineWidth = W * 0.014; c.lineCap = 'round';
    for (let k = 0; k < 3; k++) { const a = k * PI / 3 + PI / 6; c.beginPath(); c.moveTo(sx - Math.cos(a) * sr, sy - Math.sin(a) * sr); c.lineTo(sx + Math.cos(a) * sr, sy + Math.sin(a) * sr); c.stroke();
      for (const e of [-1, 1]) { const ex = sx + e * Math.cos(a) * sr * 0.62, ey = sy + e * Math.sin(a) * sr * 0.62; for (const q of [-1, 1]) { const b = a + e * (PI - 0.6 * q); c.beginPath(); c.moveTo(ex, ey); c.lineTo(ex + Math.cos(b) * sr * 0.32 * e * -1, ey + Math.sin(b) * sr * 0.32 * e * -1); c.stroke(); } } }
    c.strokeStyle = 'rgba(255,255,250,1)'; c.lineWidth = W * 0.02; c.setLineDash([W * 0.03, W * 0.01]);
    for (const p of MAP_PATH) { c.beginPath(); c.moveTo(ux(p[0][0]) * W, uz(p[0][1]) * H); c.bezierCurveTo(ux(p[1][0]) * W, uz(p[1][1]) * H, ux(p[2][0]) * W, uz(p[2][1]) * H, ux(p[3][0]) * W, uz(p[3][1]) * H); c.stroke(); }
    c.setLineDash([]); c.fillStyle = 'rgba(250,250,245,0.95)';
    const head = (p, q) => { const ax = ux(p[0]) * W, ay = uz(p[1]) * H, bx = ux(q[0]) * W, by = uz(q[1]) * H, a = Math.atan2(ay - by, ax - bx), s = W * 0.045; c.beginPath(); c.moveTo(ax, ay); c.lineTo(ax - Math.cos(a - 0.5) * s, ay - Math.sin(a - 0.5) * s); c.lineTo(ax - Math.cos(a + 0.5) * s, ay - Math.sin(a + 0.5) * s); c.fill(); };
    head(MAP_PATH[0][3], bez(MAP_PATH[0], 0.93)); head(MAP_PATH[1][3], bez(MAP_PATH[1], 0.93));
  }, { res: 1024 });
  map.rotation.x = -PI / 2; map.position.set(0, Ht + 0.003, 0); g.add(map);
  const tok = pizzaBox({ s: o.tokS ?? 0.24, pizza: false, seed: 5 }); g.add(tok); if (o.tokGlow) { const tg = glowSprite('#FFD27A', o.tokGlow, 0.7); tg.position.y = 0.05; tok.add(tg); }
  g.userData.update = t => { const u = lin(o.token, t, 0), seg = u <= 1 ? 0 : 1, p = bez(MAP_PATH[seg], clamp01(u - seg)); tok.position.set(p[0], Ht + 0.006, p[1]); tok.rotation.y = 0.3 * Math.sin(u * 3); };
  g.userData.update(0); g.userData.at = u => { const seg = u <= 1 ? 0 : 1, p = bez(MAP_PATH[seg], clamp01(u - seg)); return [p[0], Ht, p[1]]; }; return g;
}

// ---------------------------------------------------------------------------------------------------------------- the street
// His house (pivot at the floor in the middle of its front wall, front +Z): a one-storey pale yellow house o.w (7) wide, o.d (7) deep, walls 3 m
// high, a terracotta roof, a tall doorway (2.75 m: the box heads fit) in the middle with a white frame, a teal door leaf hinged on the left (o.door:
// angle or keys [[t, rad]], opening inward), a warm lit hall behind, a doorstep, two windows, a chimney; o.frameOnly: only the door frame, its leaf
// and the doorstep (what is left on the crater's rim; o.lean: the frame tilts a little)
function heroHouse(o = {}) {
  const W = o.w ?? 7, D = o.d ?? 7, Hh = 3.0, dw = 1.3, dh = 2.75, g = grp(), wc = o.color || '#EFD98A', trim = '#F6F3EA', T = 0.25;
  const frame = grp(); g.add(frame);
  frame.add(at(box(0.16, dh + 0.12, 0.3, trim, { outline: 0.006 }), -dw / 2 - 0.08, (dh + 0.12) / 2, 0), at(box(0.16, dh + 0.12, 0.3, trim, { outline: 0.006 }), dw / 2 + 0.08, (dh + 0.12) / 2, 0), at(box(dw + 0.48, 0.16, 0.32, trim, { outline: 0.006 }), 0, dh + 0.1, 0));
  frame.add(at(box(dw + 0.9, 0.18, 0.9, '#CFC6B4', { pivot: 'bottom', outline: 0.005 }), 0, 0, 0.45));
  const leaf = grp(); leaf.position.set(-dw / 2, 0, -0.05); frame.add(leaf);
  leaf.add(at(box(dw, dh, 0.07, o.doorColor || '#2F7F8C', { outline: 0.006 }), dw / 2, dh / 2, 0), at(box(dw * 0.6, dh * 0.3, 0.02, '#276A75'), dw / 2, dh * 0.72, 0.045), at(box(dw * 0.6, dh * 0.3, 0.02, '#276A75'), dw / 2, dh * 0.3, 0.045),
    at(sphere(0.06, '#E2B53C', 1), dw * 0.86, dh * 0.47, 0.07));
  if (!o.frameOnly) {
    const fw = (W - dw) / 2 - 0.08;
    g.add(at(box(fw, Hh, T, wc, { outline: 0.004 }), -(dw / 2 + 0.08 + fw / 2), Hh / 2, -T / 2), at(box(fw, Hh, T, wc, { outline: 0.004 }), dw / 2 + 0.08 + fw / 2, Hh / 2, -T / 2), at(box(dw + 0.16, Hh - dh - 0.18, T, wc), 0, dh + 0.18 + (Hh - dh - 0.18) / 2, -T / 2));
    g.add(at(box(W, Hh, T, wc), 0, Hh / 2, -D + T / 2), at(box(T, Hh, D, wc), -W / 2 + T / 2, Hh / 2, -D / 2), at(box(T, Hh, D, wc), W / 2 - T / 2, Hh / 2, -D / 2), at(box(W, 0.05, D, '#B9A68A'), 0, 0.03, -D / 2));
    g.add(at(box(dw + 0.2, Hh, 0.1, '#EAD9B8'), 0, Hh / 2, -1.6), at(box(0.1, Hh, 1.6, '#E2CFA8'), -dw / 2 - 0.1, Hh / 2, -0.8), at(box(0.1, Hh, 1.6, '#E2CFA8'), dw / 2 + 0.1, Hh / 2, -0.8));
    const lamp = glowSprite('#FFE2A8', 1.2, 0.5); lamp.position.set(0, 2.4, -1.2); g.add(lamp);
    const rh = 2.0, pitch = Math.atan2(rh, D / 2), sl = Math.hypot(D / 2, rh) + 0.55;
    for (const s of [-1, 1]) g.add(at(box(W + 0.8, 0.2, sl, o.roof || '#C9573A', { outline: 0.005 }), 0, Hh + rh / 2 + 0.05, -D / 2 + s * (D / 4 + 0.15), s * pitch, 0, 0));
    const tri = new THREE.Shape(); tri.moveTo(-D / 2, 0); tri.lineTo(D / 2, 0); tri.lineTo(0, rh); tri.lineTo(-D / 2, 0);
    for (const s of [-1, 1]) { const m = new THREE.Mesh(new THREE.ExtrudeGeometry(tri, { depth: 0.2, bevelEnabled: false }), mat(wc)); m.rotation.y = PI / 2; m.position.set(s * (W / 2) - (s > 0 ? 0.2 : 0), Hh, -D / 2); g.add(m); }
    g.add(at(box(0.6, 1.8, 0.6, '#B5402F', { pivot: 'bottom', outline: 0.005 }), W * 0.28, Hh + 0.7, -D * 0.62));
    for (const x of [-W * 0.3, W * 0.3]) g.add(at(box(1.2, 1.2, 0.08, trim, { outline: 0.005 }), x, 1.6, 0.02), at(box(1.0, 1.0, 0.09, '#7FAFCF'), x, 1.6, 0.03), at(box(0.06, 1.0, 0.1, trim), x, 1.6, 0.04), at(box(1.4, 0.08, 0.2, trim), x, 0.98, 0.08));
  }
  if (o.lean) frame.rotation.z = o.lean;
  g.userData.update = t => { leaf.rotation.y = -keyAt(o.door ?? 0, t, Array.isArray(o.door) ? o.door[0][1] : (o.door ?? 0), 0.18) - wob(Array.isArray(o.door) ? o.door.slice(1).map(k => k[0] + 0.18) : [], t, 0.08, 18, 4); };
  g.userData.update(0); return g;
}
// A lamppost (pivot at its foot): a dark green pole 4.4 m with a curved arm and a lantern toward +Z; o.bend (rad): bent over sideways from 1.3 m
// (toward +X), o.bendX (rad): toward +Z; o.droop keys [[t, rad]]: the top droops further toward +Z, easing in, with a springy overshoot
function townLamp(o = {}) {
  const g = grp(), top = grp(), c = o.color || '#2E4A3E';
  g.add(cyl(0.12, 0.16, 0.5, c, 8, { pivot: 'bottom' }), cyl(0.06, 0.07, 1.3, c, 7, { pivot: 'bottom' }));
  top.position.y = 1.3; g.add(top);
  top.add(cyl(0.055, 0.06, 3.1, c, 7, { pivot: 'bottom' }), rod([0, 3.0, 0], [0, 3.25, 0.5], 0.04, c), at(box(0.3, 0.36, 0.3, '#F4EAC0', { emissive: '#3A3010' }), 0, 2.98, 0.6), at(box(0.38, 0.08, 0.38, c), 0, 3.2, 0.6));
  top.rotation.set(o.bendX ?? 0, 0, -(o.bend ?? 0));
  if (o.droop) { const kt = o.droop.map(k => k[0]).filter(x => x > 0); g.userData.update = t => { top.rotation.x = (o.bendX ?? 0) + keyAt(o.droop, t, o.droop[0][1], o.droopBlend ?? 0.28) + wob(kt.map(x => x + (o.droopBlend ?? 0.28)), t, o.droopWob ?? 0.18, 14, 3.5); }; g.userData.update(0); }
  return g;
}
// The pavement rolled up like a carpet (pivot at the floor in its middle, the roll along X): a roll o.len (2.8) long, radius o.r (0.85), of pale
// paving slabs (joints drawn), its ends showing the spiral of slab and earth; a short flap of slabs still lying flat toward +Z; a kerb stone band
function pavementRoll(o = {}) {
  const L = o.len ?? 2.8, R = o.r ?? 0.85, g = grp();
  const skin = canvasPlane(2 * PI * R, L, (c, W, H) => { c.fillStyle = '#E2D6B8'; c.fillRect(0, 0, W, H); c.strokeStyle = '#A89A7C'; c.lineWidth = W * 0.004; const n = Math.round(2 * PI * R / 0.5);
    for (let i = 0; i <= n; i++) { c.beginPath(); c.moveTo(i / n * W, 0); c.lineTo(i / n * W, H); c.stroke(); } for (let j = 0; j <= 6; j++) { c.beginPath(); c.moveTo(0, j / 6 * H); c.lineTo(W, j / 6 * H); c.stroke(); }
    c.fillStyle = '#9A9488'; c.fillRect(0, H * 0.94, W, H * 0.06); c.fillStyle = 'rgba(40,30,20,0.25)'; for (let i = 0; i < 40; i++) { c.beginPath(); c.arc(hsh(i) * W, hsh(i + 50) * H, W * 0.006, 0, TAU); c.fill(); } }, { res: 512 });
  const geo = new THREE.CylinderGeometry(R, R, L, 28, 1, true); const tube = new THREE.Mesh(geo, skin.material); tube.material.side = THREE.DoubleSide; tube.rotation.z = PI / 2; tube.position.y = R; tube.castShadow = tube.receiveShadow = true; g.add(tube);
  const end = canvasPlane(2 * R, 2 * R, (c, W, H) => { const cx = W / 2, cy = H / 2; c.fillStyle = '#6E5A44'; c.beginPath(); c.arc(cx, cy, W / 2, 0, TAU); c.fill(); c.lineWidth = W * 0.035;
    c.strokeStyle = '#E2D6B8'; c.beginPath(); for (let a = 0; a < 6.5 * TAU; a += 0.05) { const rr = W * 0.48 * (1 - a / (6.5 * TAU) * 0.9); c.lineTo(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr); } c.stroke();
    c.strokeStyle = '#4A3C2E'; c.lineWidth = W * 0.012; c.beginPath(); c.arc(cx, cy, W * 0.497, 0, TAU); c.stroke(); }, { res: 256, transparent: true });
  for (const s of [-1, 1]) { const e = end.clone(); e.position.set(s * L / 2, R, 0); e.rotation.y = s * PI / 2; g.add(e); }
  g.add(at(box(L, 0.1, 0.7, '#E2D6B8', { outline: 0.004 }), 0, 0.05, R + 0.2));
  return g;
}

// The neighbourhood (one world for every outdoor shot of his street; pivot at the world origin): the road along X (z 0..8, its middle z 4), the
// near pavement z -2.6..0 (top 0.14), his house at x 0 with its front wall at z -3.2 (door facing the road), cottages beside it every 13 m, a row
// of cottages across the road (front at z 15), back gardens with hedges, lampposts, parked cars on the far side, trees, hills and a ring of
// cumulus on the horizon. o.furrow: a scorched furrow down the middle of the road from far +X that swerves onto his doorstep, with dirt ridges
// and soot; o.peel [x0, x1]: the near pavement there is gone (bare earth): it is rolled up at his door (o.roll: the roll there, at o.rollAt [x, z]);
// o.nudge: the parked cars pushed askew; o.bent: the lampposts near the furrow bent over; o.crater {c: [x, z], R, D}: a deep clean crater (round,
// near-vertical striped walls, a flat floor at -D) where the house and garden were (cottages within its reach removed), his door frame alone on
// the rim (o.frameDoor keys), a rope ladder from the rim to the floor (o.ladder: true); o.house (true): his house; o.cars (true)
function pizzaTown(o = {}) {
  const g = grp(), r = rng(o.seed || 91), FZ = -3.2;
  const C = o.crater ? { c: o.crater.c || [0, -15], R: o.crater.R ?? 11.6, D: o.crater.D ?? 14 } : null;
  const inCrater = (x, z, pad = 0) => C && Math.hypot(x - C.c[0], z - C.c[1]) < C.R + pad;
  // the ground: a big flat with a round hole for the crater
  const GS = 1600, sh = new THREE.Shape([new THREE.Vector2(-GS, -GS), new THREE.Vector2(GS, -GS), new THREE.Vector2(GS, GS), new THREE.Vector2(-GS, GS)]);
  if (C) { const hole = new THREE.Path(); for (let i = 0; i <= 64; i++) { const a = -i / 64 * TAU; hole.lineTo(C.c[0] + Math.cos(a) * C.R, -(C.c[1]) + Math.sin(a) * C.R); } sh.holes.push(hole); }
  const ground = new THREE.Mesh(new THREE.ShapeGeometry(sh, 16), lam(o.grass || '#8DBB5E')); ground.rotation.x = -PI / 2; ground.receiveShadow = true; g.add(ground);
  // road, pavements, kerbs
  g.add(at(box(700, 0.06, 8, '#7E828C'), 0, 0.03, 4));
  for (let x = -340; x < 340; x += 6) g.add(at(box(2.6, 0.012, 0.2, '#F4F1E8'), x, 0.066, 4));
  const peel = o.peel || null, pavN = (x0, x1) => { if (x1 - x0 > 0.01) g.add(at(box(x1 - x0, 0.14, 2.6, '#E6DABE', { outline: 0.002 }), (x0 + x1) / 2, 0.07, -1.3)); };
  if (peel) { pavN(-350, peel[0]); pavN(peel[1], 350); g.add(at(box(peel[1] - peel[0], 0.05, 2.6, '#7A5E44'), (peel[0] + peel[1]) / 2, 0.03, -1.3)); } else pavN(-350, 350);
  g.add(at(box(700, 0.14, 2.6, '#E6DABE'), 0, 0.07, 9.3), at(box(700, 0.18, 0.22, '#C9C2B2'), 0, 0.09, 0.0), at(box(700, 0.18, 0.22, '#C9C2B2'), 0, 0.09, 8.0));
  // his house (or, with the crater, its door frame on the rim)
  const pieces = {};
  if (o.house !== false && !C) { pieces.house = heroHouse({ door: o.door }); pieces.house.position.set(0, 0, FZ); g.add(pieces.house); }
  if (C) { pieces.house = heroHouse({ frameOnly: true, door: o.frameDoor ?? 0.25, lean: 0.02 }); pieces.house.position.set(0, 0, FZ); g.add(pieces.house); }
  // the cottages beside it and across the road
  const cols = ['#B8A6D9', '#E8A08A', '#A9C7E8', '#F0C6CF', '#F4F2EC', '#9FD3C0', '#EDCF7A'], roofs = ['#6A3A30', '#3E4A5E', '#B5402F', '#5E83C6', '#C9473A'];
  for (let i = -5; i <= 5; i++) { if (i === 0) continue; const x = i * 13; if (inCrater(x, FZ - 4, 4)) continue; const cg = buildProp('cottage', { w: 7.2, d: 8, h: 2.9, rh: 1.7, color: cols[(i + 7) % 7], roof: roofs[(i + 9) % 5], eaves: i % 2 === 0, door: '#7A4A2A' }); cg.position.set(x, 0, FZ - 4); g.add(cg); }
  for (let i = -5; i <= 5; i++) { const x = i * 13 + 6.5; const cg = buildProp('cottage', { w: 7.2, d: 8, h: 2.9, rh: 1.7, color: cols[(i + 10) % 7], roof: roofs[(i + 12) % 5], eaves: i % 2 !== 0, door: '#2F5E8C' }); cg.position.set(x, 0, 15 + 4); cg.rotation.y = PI; g.add(cg); }
  // back gardens: hedges between plots, a lawn, a shed, a tree, a washing line (his has a table and parasol); nobody in them
  for (let i = -5; i <= 5; i++) { const x = i * 13 + 6.5; if (!inCrater(x, -16, 1)) g.add(at(box(0.7, 1.5, 14, '#3E7A36', { pivot: 'bottom', outline: 0.004 }), x, 0, -16)); }
  if (!C) { g.add(at(box(13, 1.5, 0.7, '#3E7A36', { pivot: 'bottom' }), 0, 0, -23)); const tr = buildProp('tree', { seed: 4 }); tr.position.set(-3.5, 0, -18); tr.scale.setScalar(1.6); g.add(tr);
    g.add(at(box(2.2, 2.0, 1.8, '#9A7A5A', { pivot: 'bottom', outline: 0.005 }), 3.8, 0, -20), at(box(2.5, 0.12, 2.1, '#6A4A32'), 3.8, 2.05, -20), at(cyl(0.6, 0.6, 0.05, '#F4F2EC', 10), 0.5, 0.75, -14), at(cyl(0.04, 0.04, 0.75, '#9AA0A6', 6, { pivot: 'bottom' }), 0.5, 0, -14)); }
  for (let i = -5; i <= 5; i++) { const x = i * 13 + 2; if (i === 0 || inCrater(x, -19, 2)) continue; const tr = buildProp('tree', { seed: i + 20 }); tr.position.set(x, 0, -19 - r() * 2); tr.scale.setScalar(1.3 + r() * 0.5); g.add(tr); }
  for (let i = 0; i < 18; i++) { const tr = buildProp('tree', { seed: i + 40 }); tr.position.set(-110 + i * 13 + r() * 4, 0, -32 - r() * 8); tr.scale.setScalar(1.6 + r() * 0.6); g.add(tr); const t2 = buildProp('tree', { seed: i + 60 }); t2.position.set(-110 + i * 13 + r() * 4, 0, 30 + r() * 6); t2.scale.setScalar(1.6 + r() * 0.6); g.add(t2); }
  // lampposts (bent along the furrow) and parked cars (pushed askew)
  const lamps = [];
  for (let i = -6; i <= 6; i++) { const x = i * 11 + 5.5; for (const [z, ry] of [[-0.45, 0], [8.5, PI]]) { const near = o.bent && x > 2 && x < 45 && Math.abs(z - 4) < 5; const lp = townLamp({ bend: near ? (0.35 + 0.5 * hsh(i + z)) * (i % 2 ? 1 : -1) : 0, bendX: near ? -(0.7 + 0.5 * hsh(i * 3 + z)) : 0 }); lp.position.set(x, 0.14, z); lp.rotation.y = ry; g.add(lp); lamps.push(lp); } }
  if (o.cars !== false) { const cc = ['#D8392B', '#5E8FD0', '#F2C94C', '#E8E4DA', '#3E4A5A', '#7FB069', '#D98AA8'];
    for (let i = -6; i <= 6; i++) { const x = i * 9 + 2; if (Math.abs(x) < 3) continue; const cr = buildProp('car', { color: cc[(i + 7) % cc.length], plate: ' ' }); const nudge = o.nudge && x > 0 && x < 50;
      cr.scale.setScalar(1.15); cr.position.set(x + (nudge ? 0.6 * hsh(i) : 0), 0, nudge ? 7.0 + 0.8 * hsh(i + 2) : 6.9); cr.rotation.y = (i % 2 ? 0 : PI) + (nudge ? (0.35 + 0.3 * hsh(i + 5)) * (i % 2 ? 1 : -1) : 0); g.add(cr); } }
  // horizon: soft hills and a ring of cumulus
  const hc = ['#9DB48A', '#8FA87E', '#A9BC96'];
  for (let i = 0; i < 16; i++) { const a = i / 16 * TAU + r() * 0.2, d = 230 + r() * 40, m = sphere(1, hc[i % 3], 1); m.scale.set(60, 16 * (0.6 + r() * 0.6), 30); m.position.set(Math.cos(a) * d, -3, Math.sin(a) * d); m.castShadow = false; g.add(m); }
  for (let i = 0; i < 26; i++) { const a = i / 26 * TAU + r() * 0.12, d = 620 * (0.85 + r() * 0.35); const cu = buildProp('cumulus', { w: 150 + r() * 120, h: 55 + r() * 35, n: 22, seed: i + 3 }); cu.position.set(Math.cos(a) * d, -8, Math.sin(a) * d); g.add(cu); }
  // the furrow: a dark trench with soot and dirt ridges along a path (x, z) that swerves onto his doorstep
  if (o.furrow) {
    const path = o.furrowPath || [[80, 4.2], [30, 4.0], [12, 3.6], [5.5, 2.0], [2.2, -0.6], [0.6, -2.4]];
    for (let i = 1; i < path.length; i++) { const [x0, z0] = path[i - 1], [x1, z1] = path[i], L = Math.hypot(x1 - x0, z1 - z0), a = Math.atan2(-(z1 - z0), x1 - x0), mx = (x0 + x1) / 2, mz = (z0 + z1) / 2, wk = i === path.length - 1 ? 0.8 : 1;
      g.add(at(box(L + 0.6, 0.02, 3.4 * wk, '#3A3632'), mx, 0.075, mz, 0, a, 0), at(box(L + 0.4, 0.03, 1.3 * wk, '#141210'), mx, 0.085, mz, 0, a, 0));
      for (const s of [-1, 1]) { const ox = -Math.sin(a) * s * 0.95 * wk, oz = -Math.cos(a) * s * 0.95 * wk; g.add(at(box(L + 0.3, 0.16, 0.5, '#5E4C3A'), mx + ox, 0.1, mz + oz, 0, a, 0)); }
      for (let k = 0; k < L / 2; k++) { const u = (k + 0.5) / Math.ceil(L / 2), x = x0 + (x1 - x0) * u, z = z0 + (z1 - z0) * u; if (r() < 0.45) g.add(at(box(0.25 + r() * 0.25, 0.12 + r() * 0.1, 0.25 + r() * 0.25, r() < 0.5 ? '#6A5A4A' : '#4E4032'), x + (r() - 0.5) * 0.6, 0.1, z + (r() < 0.5 ? -1 : 1) * (1.2 + r() * 0.5), r(), r() * 3, r())); else { r(); r(); r(); r(); r(); r(); r(); r(); } } }
    pieces.wisps = []; for (const [x, z] of [[40, 4.1], [22, 4.0], [10, 3.4], [3.5, 0.6]]) { const w = buildProp('softWisp', { n: 12, rise: 2.4, life: 2.0, s0: 0.3, s1: 1.1, color: '#5A5450', opacity: 0.55, drift: [0.4, -0.2] }); w.position.set(x, 0.2, z); g.add(w); pieces.wisps.push(w); }
  }
  if (o.roll) { const rp = o.rollAt || [0, -2.0]; const rl = pavementRoll({ len: 2.9, r: o.rollR ?? 0.85 }); rl.position.set(rp[0], 0.05, rp[1]); g.add(rl); pieces.roll = rl; }
  // the crater: striped walls (lathe), a flat floor, a raised lip with a little clean rubble, the ladder
  if (C) {
    const Rr = C.R, D = C.D, prof = [[Rr * 0.86, -D], [Rr * 0.92, -D * 0.97], [Rr * 0.95, -D * 0.9]];
    for (let i = 1; i <= 24; i++) { const u = i / 24, y = -D * 0.9 * (1 - u); prof.push([Rr * (0.95 + 0.05 * Math.sqrt(u)) + (i % 2 ? 0.12 : 0), y]); }
    const lg = new THREE.LatheGeometry(prof.map(([x, y]) => new THREE.Vector2(x, y)), 64).toNonIndexed(), pa = lg.attributes.position, colArr = [], cA = new THREE.Color(), bands = ['#8A6A4A', '#A9845A', '#6E5038', '#B89466', '#7A5A3E', '#5E4632'];
    const strata = ['#C9A066', '#8E5E3A', '#E2C48E', '#6E4A30', '#B07A48', '#F0DCB0', '#7A5236', '#A87048'];
    for (let i = 0; i < pa.count; i += 3) { const y = (pa.getY(i) + pa.getY(i + 1) + pa.getY(i + 2)) / 3, k = Math.floor(clamp01(-y / D) * 13); cA.set(strata[k % strata.length]).multiplyScalar(0.94 + 0.08 * hsh(Math.floor(i / 6))); for (let q = 0; q < 3; q++) colArr.push(cA.r, cA.g, cA.b); }
    lg.setAttribute('color', new THREE.Float32BufferAttribute(colArr, 3)); lg.computeVertexNormals();
    const wall = new THREE.Mesh(lg, new THREE.MeshLambertMaterial({ vertexColors: true, flatShading: true, side: THREE.DoubleSide })); wall.position.set(C.c[0], 0, C.c[1]); wall.receiveShadow = true; wall.castShadow = true; g.add(wall);
    const floor = new THREE.Mesh(new THREE.CircleGeometry(Rr * 0.87, 48), lam('#5A4634')); floor.rotation.x = -PI / 2; floor.position.set(C.c[0], -D + 0.01, C.c[1]); floor.receiveShadow = true; g.add(floor);
    for (let i = 0; i < 10; i++) { const a = r() * TAU, d = Rr * (0.15 + 0.65 * Math.sqrt(r())); g.add(at(new THREE.Mesh(new THREE.DodecahedronGeometry(0.15 + r() * 0.3, 0), mat(i % 2 ? '#6E5A44' : '#8A7258')), C.c[0] + Math.cos(a) * d, -D + 0.1, C.c[1] + Math.sin(a) * d, r() * 3, r() * 3, 0)); }
    const lip = new THREE.Mesh(new THREE.RingGeometry(Rr, Rr + 1.6, 64, 1), lam('#7A6248', { side: THREE.DoubleSide })); lip.rotation.x = -PI / 2; lip.position.set(C.c[0], 0.03, C.c[1]); g.add(lip);
    for (let i = 0; i < 14; i++) { const a = i / 14 * TAU + r() * 0.1, d = Rr + 0.4 + r() * 1.4, x = C.c[0] + Math.cos(a) * d, z = C.c[1] + Math.sin(a) * d; if (Math.abs(x) < 2.2 && z > C.c[1] + Rr - 2) continue; g.add(at(new THREE.Mesh(new THREE.DodecahedronGeometry(0.12 + r() * 0.22, 0), mat(i % 3 ? '#8A7258' : '#6E5A44')), x, 0.08, z, r() * 3, r() * 3, 0)); }
    if (o.ladder) { const top = o.ladderTop || [0.0, 0.05, FZ - 0.35], bot = o.ladderBot || [0.0, -D, FZ - 2.6]; pieces.ladder = craterLadder({ top, bot, thick: o.ladderThick }); g.add(pieces.ladder); }
  }
  g.userData.update = t => { if (pieces.house) pieces.house.userData.update(t); (pieces.wisps || []).forEach(w => w.userData.update(t)); };
  g.userData.update(0); g.userData.crater = C; return g;
}
// A rope ladder hung from a point on the rim to a point on the crater floor (world points o.top, o.bot; pivot at the origin): two pale twisted
// ropes that sag in a gentle curve away from the wall, small wooden slats tied across every 0.4 m, each a little askew; o.thick (1): fatter
// ropes and slats so it reads as a line from far away
function craterLadder(o) {
  const g = grp(), T = o.thick ?? 1, [tx, ty, tz] = o.top, [bx, by, bz] = o.bot, L = Math.hypot(tx - bx, ty - by, tz - bz), n = Math.floor(L / 0.4), N = 16;
  const pt = (u, sx) => { const sag = 0.35 * Math.sin(PI * u), wig = 0.03 * Math.sin(u * 23 + sx * 3); return [tx + (bx - tx) * u + sx + wig, ty + (by - ty) * u, tz + (bz - tz) * u - sag]; };
  for (const sx of [-0.27, 0.27]) for (let i = 0; i < N; i++) g.add(rod(pt(i / N, sx), pt((i + 1) / N, sx), 0.03 * T, '#F2E8C8'));
  for (let i = 1; i < n; i++) { const u = i / n, a = pt(u, -0.29), c = pt(u, 0.29), tw = (hsh(i) - 0.5) * 0.12; a[1] += tw; c[1] -= tw; g.add(rod(a, c, 0.028 * T, '#A07A4A')); }
  g.add(at(box(0.9, 0.12, 0.3, '#5A4634'), tx, ty, tz + 0.1));
  return g;
}

// ---------------------------------------------------------------------------------------------------------------- other places
// A foreign official's front door (pivot at the floor in the middle of the facade's foot, front +Z): a facade slice o.w (3.4) wide, 3.8 high in
// o.wall colour with a cornice, a tall door in o.door colour with a white frame, a doorstep, a blank brass plaque, and a flag on a short pole
// slanting out over the door: two or three bands o.colors (invented: check them against real flags), o.vertical bands; the flag ripples
function embassyDoor(o = {}) {
  const W = o.w ?? 3.4, H = 3.8, g = grp(), dw = 1.25, dh = 2.75;
  g.add(at(box((W - dw) / 2, H, 0.4, o.wall || '#E8E0D0', { outline: 0.004 }), -(dw + (W - dw) / 2) / 2, H / 2, -0.2), at(box((W - dw) / 2, H, 0.4, o.wall || '#E8E0D0', { outline: 0.004 }), (dw + (W - dw) / 2) / 2, H / 2, -0.2), at(box(dw, H - dh, 0.4, o.wall || '#E8E0D0'), 0, dh + (H - dh) / 2, -0.2));
  g.add(at(box(W + 0.2, 0.25, 0.55, '#F4F1E8', { outline: 0.004 }), 0, H, -0.18), at(box(dw, dh, 0.06, '#3A2E26'), 0, dh / 2, -0.35));
  g.add(at(box(0.14, dh + 0.1, 0.12, '#F6F3EA'), -dw / 2 - 0.07, (dh + 0.1) / 2, 0.02), at(box(0.14, dh + 0.1, 0.12, '#F6F3EA'), dw / 2 + 0.07, (dh + 0.1) / 2, 0.02), at(box(dw + 0.28, 0.14, 0.12, '#F6F3EA'), 0, dh + 0.07, 0.02));
  const leaf = grp(at(box(dw * 0.95, dh * 0.98, 0.06, o.door || '#6A2E3A', { outline: 0.006 }), dw * 0.475, dh * 0.49, 0)); leaf.position.set(-dw / 2, 0, -0.1); leaf.rotation.y = -(o.open ?? 1.45); g.add(leaf);
  g.add(at(box(dw + 0.8, 0.16, 0.8, '#CFC6B4', { pivot: 'bottom', outline: 0.004 }), 0, 0, 0.4), at(box(0.34, 0.24, 0.03, '#C9A646', { outline: 0.004 }), dw / 2 + 0.45, 1.6, 0.01));
  const pole = grp(); pole.position.set(-dw / 2 - 0.55, H - 0.6, 0.02); pole.rotation.x = 0.75; g.add(pole);
  pole.add(cyl(0.03, 0.03, 1.8, '#C9A646', 6, { pivot: 'bottom' }), at(sphere(0.06, '#C9A646', 1), 0, 1.82, 0));
  const cl = grp(); cl.position.set(0.03, 1.75, 0); pole.add(cl); const c = o.colors || ['#1E7A8C', '#E88AA8'], n = c.length, fw = 1.05, fh = 0.7;
  c.forEach((col, i) => cl.add(o.vertical ? at(box(fw / n, fh, 0.012, col), fw / n * (i + 0.5), -fh / 2, 0) : at(box(fw, fh / n, 0.012, col), fw / 2, -fh / n * (i + 0.5), 0)));
  cl.rotation.x = -0.75;
  g.userData.update = t => { cl.rotation.y = 0.12 * Math.sin(t * 3.1 + (o.seed || 0)); };
  g.userData.update(0); return g;
}
// The exhibit stand in the press room (pivot at the floor): a slim navy pedestal 1.05 m high with a sloping top (o.tilt 0.5 rad toward +Z) that
// holds the open box face up to the room
function exhibitStand(o = {}) {
  const g = grp(), h = o.h ?? 1.05; g.add(at(box(0.5, h, 0.5, '#24384F', { pivot: 'bottom', taper: { x: 0.8, z: 0.8 }, outline: 0.006 }), 0, 0, 0), at(box(0.9, 0.05, 0.75, '#2E4563', { outline: 0.005 }), 0, h + 0.02, 0, o.tilt ?? 0.5, 0, 0));
  return g;
}
// The time-lapse sun (no mesh; pivot anywhere): from o.from (s) it swings the scene's sun round the sky once every o.period (1.1 s) on an arc
// from east to west (o.az0 rad: its azimuth at noon), never below o.minEl (0.1 rad), so the shadows race round the crater; pair it with the shot's
// daynight cycle of the same period; o.disc: a big sun disc on the same arc (o.discEl: its highest elevation, rad) so the sweep shows in the sky
function sunRacer(o = {}) {
  const g = grp(); let L = null; const v = new THREE.Vector3();
  g.userData.update = t => {
    if (!L) { let root = g; while (root.parent) root = root.parent; if (root === g) return; root.traverse(n => { if (!L && n.isDirectionalLight && n.castShadow) L = n; }); if (!L) root.traverse(n => { if (!L && n.isDirectionalLight) L = n; }); if (!L) return; }
    const p = Math.max(0, t - (o.from ?? 0)) / (o.period ?? 1.1), el = Math.max(o.minEl ?? 0.1, Math.cos(p * TAU) * (o.maxEl ?? 1.1)), az = (o.az0 ?? 0.6) + p * TAU;
    const len = L.position.distanceTo(L.target.position) || 50; v.set(Math.cos(az) * Math.cos(el), Math.sin(el), Math.sin(az) * Math.cos(el)); L.position.copy(L.target.position).addScaledVector(v, len);
    if (disc) { const day = Math.cos(p * TAU); disc.visible = day > 0.05; const de = Math.max(0.0, day) * (o.discEl ?? 0.25); disc.position.set(Math.cos(az) * Math.cos(de) * 380, Math.sin(de) * 380 + (o.discY ?? 0), Math.sin(az) * Math.cos(de) * 380); }
  };
  let disc = null; if (o.disc) { disc = grp(glowSprite('#FFE6A0', 120, 0.9), glowSprite('#FFFFFF', 45, 1)); g.add(disc); }
  return g;
}

// A napkin tucked in a collar (attach to the torso joint at the collar, e.g. offset [0, 0.4, 0.2]; pivot at its top edge): a white cloth triangle
// o.w (0.5) wide hanging o.h (0.55) down the chest, its tip down, with two tucked corners at the top
function napkinBib(o = {}) {
  const w = o.w ?? 0.5, h = o.h ?? 0.55, g = grp(), s = new THREE.Shape();
  s.moveTo(-w / 2, 0); s.lineTo(w / 2, 0); s.lineTo(w * 0.08, -h); s.lineTo(-w * 0.08, -h); s.closePath();
  const m = new THREE.Mesh(new THREE.ExtrudeGeometry(s, { depth: 0.012, bevelEnabled: false }), mat('#FAFAF6')); m.castShadow = true; m.rotation.x = -0.12; g.add(m);
  for (const sd of [-1, 1]) g.add(at(box(0.09, 0.07, 0.03, '#EFEFEA', { outline: 0.004 }), sd * w * 0.32, -0.02, 0.0, 0, 0, sd * 0.4));
  return g;
}

// A lump of crater rubble with a flat top to set something on (pivot at its foot): o.h (0.55) high, o.w (0.9) wide, faceted brown
function rubbleRock(o = {}) {
  const h = o.h ?? 0.55, w = o.w ?? 0.9, g = grp(), m = new THREE.Mesh(new THREE.DodecahedronGeometry(0.5, 0), mat(o.color || '#7A6248'));
  m.scale.set(w, h * 1.25, w * 0.85); m.position.y = h * 0.38; m.castShadow = m.receiveShadow = true; g.add(m);
  g.add(at(box(w * 0.7, 0.08, w * 0.6, o.color || '#7A6248', { outline: 0.004 }), 0, h - 0.04, 0));
  return g;
}

// Breath steam (attach to the head joint at the mouth, e.g. offset [0, 0.12, 0.2]; pivot at the mouth): at each time of o.times a few small pale
// grey-blue puffs leave the mouth, drift o.dir ([0.25, -0.12, 0.2] m) sideways and down, swell and fade in o.life (0.8 s); unlit, no glow
function breathPuffs(o = {}) {
  const g = grp(), cv = document.createElement('canvas'); cv.width = cv.height = 64; const x = cv.getContext('2d');
  const gr = x.createRadialGradient(32, 32, 2, 32, 32, 31); gr.addColorStop(0, 'rgba(255,255,255,0.9)'); gr.addColorStop(0.6, 'rgba(255,255,255,0.35)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = gr; x.fillRect(0, 0, 64, 64);
  const tex = new THREE.CanvasTexture(cv), sp = [], times = o.times || [0], life = o.life ?? 0.8, d = o.dir || [0.25, -0.12, 0.2];
  for (const t0 of times) for (let i = 0; i < 4; i++) { const m = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, color: o.color || '#C9D6E0', transparent: true, opacity: 0, depthWrite: false, toneMapped: false })); m.userData.p = [t0 + i * 0.07, hsh(i + t0 * 10)]; m.visible = false; g.add(m); sp.push(m); }
  g.userData.update = t => sp.forEach(m => { const [t0, h] = m.userData.p, u = (t - t0) / life; m.visible = u >= 0 && u < 1; if (!m.visible) return; const e = 1 - (1 - u) * (1 - u);
    m.position.set(d[0] * e * (0.8 + 0.4 * h), d[1] * e + 0.03 * Math.sin(u * 6 + h * 5), d[2] * e); const sc = (o.s ?? 0.06) * (1 + 2.2 * u); m.scale.set(sc, sc, 1); m.material.opacity = (o.opacity ?? 0.55) * (u < 0.15 ? u / 0.15 : 1 - smooth((u - 0.15) / 0.85)); });
  g.userData.update(-1); return g;
}
// A planet Earth seen from orbit (pivot at its centre): a faceted blue ocean sphere o.r (40) with green and sand continents, white cloud
// patches floating just above the surface and a thin pale-blue rim of atmosphere; turns slowly (o.spin 0.02 rad/s)
function planetEarth(o = {}) {
  const R = o.r ?? 40, g = grp(), r = rng(o.seed || 11), spin = grp(); g.add(spin);
  const geo = new THREE.IcosahedronGeometry(R, 4), pos = geo.attributes.position, cols = [], c = new THREE.Color();
  const seeds = Array.from({ length: 11 }, () => [new THREE.Vector3(r() - 0.5, (r() - 0.5) * 0.8, r() - 0.5).normalize(), 0.35 + r() * 0.35]);
  for (let i = 0; i < pos.count; i += 3) { const v = new THREE.Vector3(); for (let k = 0; k < 3; k++) v.add(new THREE.Vector3(pos.getX(i + k), pos.getY(i + k), pos.getZ(i + k))); v.normalize();
    let s = 0; seeds.forEach(([q, w]) => { s = Math.max(s, w - v.distanceTo(q)); });
    c.set(Math.abs(v.y) > 0.95 ? '#F2F6F8' : s > 0.15 ? (s > 0.3 ? '#4E9A40' : '#62AE50') : s > 0.12 ? '#B8A46A' : (s > 0.06 ? '#3A86D0' : '#2A64B8')); for (let k = 0; k < 3; k++) cols.push(c.r, c.g, c.b); }
  geo.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3)); geo.computeVertexNormals();
  spin.add(new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ vertexColors: true, flatShading: true })));
  for (let i = 0; i < 46; i++) { const v = new THREE.Vector3(r() - 0.5, (r() - 0.5) * 1.2, r() - 0.5).normalize(), m = sphere(1, '#FFFFFF', 1, { noGrain: true }); m.scale.set(R * (0.06 + 0.08 * r()), R * 0.012, R * (0.04 + 0.06 * r()));
    m.position.copy(v.clone().multiplyScalar(R * 1.012)); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), v); m.castShadow = false; spin.add(m); }
  g.add(new THREE.Mesh(new THREE.SphereGeometry(R * 1.035, 40, 24), new THREE.MeshBasicMaterial({ color: '#8FD0FF', transparent: true, opacity: 0.18, depthWrite: false, side: THREE.BackSide })));
  spin.rotation.set(o.tilt ?? 0.4, 0, 0.2);
  g.userData.update = t => { spin.rotation.y = (o.spin ?? 0.02) * t; }; g.userData.update(0); return g;
}

// A soft pale halo to make a tiny far figure read (attach to the torso joint; pivot at its middle): an additive white glow o.s (1.8 m) at
// o.opacity (0.35) behind the figure, so a dot on a dark wall gets a bright rim
function haloGlow(o = {}) { const g = grp(), h = glowSprite(o.color || '#FFF4DA', o.s ?? 1.8, o.opacity ?? 0.35); h.position.z = -0.25; g.add(h); return g; }

export const PIZZA_PROPS = {
  pizzaThermo(o = {}) { return thermo(o); },
  pizzaPie(o = {}) { return pie(o.r ?? 0.27, o); },
  pizzaBox(o = {}) { return pizzaBox(o); },
  pizzaSlice(o = {}) { return pizzaSlice(o); },
  ratingPhone(o = {}) { return ratingPhone(o); },
  jetBox(o = {}) { return jetBox(o); },
  pizzaMissile(o = {}) { return pizzaMissile(o); },
  pizzaWarMap(o = {}) { return pizzaWarMap(o); },
  heroHouse(o = {}) { return heroHouse(o); },
  townLamp(o = {}) { return townLamp(o); },
  pavementRoll(o = {}) { return pavementRoll(o); },
  pizzaTown(o = {}) { return pizzaTown(o); },
  craterLadder(o = {}) { return craterLadder(o); },
  embassyDoor(o = {}) { return embassyDoor(o); },
  exhibitStand(o = {}) { return exhibitStand(o); },
  sunRacer(o = {}) { return sunRacer(o); },
  napkinBib(o = {}) { return napkinBib(o); },
  rubbleRock(o = {}) { return rubbleRock(o); },
  breathPuffs(o = {}) { return breathPuffs(o); },
  planetEarth(o = {}) { return planetEarth(o); },
  haloGlow(o = {}) { return haloGlow(o); },
};
