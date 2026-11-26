// « Les moutons » (story 111, cycle 59): this man cannot sleep, so he counts sheep. In the morning there are four thousand of them in his bedroom, for
// real. Their bleating wakes the building, which counts in turn, and the loop runs away (the more they count, the less they sleep): the sheep fill
// the stairwell, the street, the town, white as under snow. Wool is worth nothing: a herbal tea buys a flock. Only the shepherds sleep, standing.
// An accountant finds the answer: count backwards; on TV the whole country counts down and not one sheep is left, neither on the farms nor in the
// jumpers. Except the black sheep, who cannot sleep either: it has been counting him all along, and he jumps the fence four thousand times a night.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
// Running gag drawn here: the black sheep (mtSheep black) and its thought bubble (mtBubble), in which a tiny box-headed man in a dark suit and a red tie
// hops a little white fence, more out of breath each time. Crowds of sheep are faceless fleece blobs (mtFleece, instanced, no head, no legs).
import * as THREE from 'three';
import { box, cyl, sphere, mat, addOutline } from './style.js';
import { grp, at } from './props.js';
import { buildCreature } from './creatures.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const lerp = (a, b, u) => a + (b - a) * u;
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
// [[t, v], ...] -> v at t, smoothstep between keys (a key [t, v, 'lin'] makes its segment linear); v may be a number or an array
const keyAt = (K, t, d = 0) => {
  if (K === undefined || K === null) return d;
  if (typeof K === 'number') return K;
  if (!K.length) return d;
  const mix = (a, b, u) => Array.isArray(a) ? a.map((v, i) => lerp(v, b[i], u)) : lerp(a, b, u);
  if (t <= K[0][0]) return K[0][1];
  for (let i = 1; i < K.length; i++) if (t < K[i][0]) { const u = (t - K[i - 1][0]) / Math.max(1e-6, K[i][0] - K[i - 1][0]); return mix(K[i - 1][1], K[i][1], K[i][2] === 'lin' ? u : smooth(u)); }
  return K[K.length - 1][1];
};
// [[t, v], ...] -> the last v whose time has come (a step)
const stepAt = (K, t, d) => { let v = d; for (const k of K || []) { if (t >= k[0]) v = k[1]; else break; } return v; };
// inside one of the intervals [[t0, t1], ...]: [t0, t1], else null
const within = (I, t) => { for (const iv of I || []) if (t >= iv[0] && t < iv[1]) return iv; return null; };
// a damped wobble summed over times [t, ...]
const shake = (T, t, amp, f, dk) => { let s = 0; for (const t0 of T || []) { const u = t - t0; if (u > 0) s += amp * Math.sin(u * f) * Math.exp(-u * dk); } return s; };
// a pop (0 before t0, overshoot, settle at 1)
const popK = (t0, t, dur = 0.22) => { if (t0 == null) return 1; const u = (t - t0) / dur; if (u <= 0) return 0; if (u >= 2) return 1; return u < 1 ? 1.18 * Math.sin(u * PI / 2) : 1 + 0.18 * Math.cos((u - 1) * PI) * Math.exp(-(u - 1) * 3) * (u < 1.5 ? 1 : 0.6); };
const INK = '#1B1E2A';
const inkMat = new THREE.MeshBasicMaterial({ color: INK, side: THREE.BackSide });
const ink = (m, t = 0.03) => { addOutline(m, t); return m; };
const OFF = { polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -8 };
const canvas = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
const texOf = cv => { const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t; };
const L = (c, o = {}) => new THREE.MeshLambertMaterial({ color: c, ...o });

// a fleece blob geometry: a cluster of round lobes (jittered icospheres with smooth normals, so each lobe shades soft and round, no facets), small curls on
// top, no head, no legs, about 1 m across, its middle at the origin. (round 1 of 111) one fleece look for every wool mass, blob and sheep body
const _blobGeos = {};
function blobGeo(seed = 1) {
  if (_blobGeos[seed]) return _blobGeos[seed];
  const parts = [[0, 0, 0, 0.4], [0.3, 0.06, 0.06, 0.27], [-0.29, 0.04, -0.08, 0.28], [0.06, 0.16, -0.27, 0.26], [-0.06, 0.15, 0.28, 0.25], [0.02, 0.3, 0.0, 0.24], [0.22, -0.04, -0.22, 0.22], [-0.2, 0.1, 0.22, 0.22], [0.2, 0.2, 0.2, 0.2], [-0.22, 0.22, -0.18, 0.2],
    [0.14, 0.34, 0.14, 0.13], [-0.16, 0.33, 0.06, 0.13], [0.36, 0.14, -0.06, 0.13], [-0.36, 0.12, 0.08, 0.13], [0.08, 0.1, 0.4, 0.12], [-0.06, 0.12, -0.4, 0.12]];
  const pos = [], nor = [], uvs = [];
  parts.forEach(([x, y, z, r], pi) => {
    const g = new THREE.IcosahedronGeometry(1, 1), p = g.attributes.position, uv = g.attributes.uv, off = new Map();
    for (let i = 0; i < p.count; i++) {
      const vx = p.getX(i), vy = p.getY(i), vz = p.getZ(i), key = `${Math.round(vx * 99)},${Math.round(vy * 99)},${Math.round(vz * 99)}`;
      if (!off.has(key)) off.set(key, 1 + (hsh(seed * 53 + pi * 17 + off.size * 3.1) - 0.5) * 0.08);
      const f = off.get(key) * r * (0.85 + 0.3 * hsh(seed * 7 + pi));
      pos.push(x + vx * f, y * 0.9 + vy * f * 0.88, z + vz * f); nor.push(vx, vy / 0.88, vz); uvs.push(uv.getX(i) * 2 + pi * 0.37, uv.getY(i) * 2);
    }
    g.dispose();
  });
  for (let i = 0; i < nor.length; i += 3) { const l = Math.hypot(nor[i], nor[i + 1], nor[i + 2]) || 1; nor[i] /= l; nor[i + 1] /= l; nor[i + 2] /= l; }
  const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); geo.setAttribute('normal', new THREE.Float32BufferAttribute(nor, 3));
  geo.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2)); geo.computeBoundingSphere(); geo.computeBoundingBox();
  _blobGeos[seed] = geo; return geo;
}
const WOOL = '#FBFBF8';
// a soft curl pattern (pale blue-grey arcs on white) that the fleece material multiplies: the lobes read as wool, not as paper or ice
let _curlTex = null;
function curlTex() {
  if (_curlTex) return _curlTex;
  const cv = canvas(128, 128), c = cv.getContext('2d'); c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, 128, 128); c.strokeStyle = '#CBD3E2'; c.lineWidth = 3; c.lineCap = 'round';
  for (let i = 0; i < 46; i++) { const x = hsh(i * 3 + 1) * 128, y = hsh(i * 5 + 2) * 128, r = 5 + 5 * hsh(i * 7 + 3), a = hsh(i * 11 + 4) * TAU;
    for (const dx of [-128, 0, 128]) for (const dy of [-128, 0, 128]) { c.beginPath(); c.arc(x + dx, y + dy, r, a, a + PI * 1.3); c.stroke(); } }
  _curlTex = texOf(cv); _curlTex.wrapS = _curlTex.wrapT = THREE.RepeatWrapping; return _curlTex;
}
// the fleece material: soft cool white, smooth shading, a little emissive (it glows a touch in shade and by night), the curl pattern; o.color for a
// dark fleece (the black sheep)
const _woolMats = {};
const woolMat = (color = '#F2F5FA', emissive = '#566078') => _woolMats[color + emissive] || (_woolMats[color + emissive] = new THREE.MeshLambertMaterial({ color, emissive, map: curlTex() }));
// the fleece's outline: thin and cool slate instead of black ink (where two lobes meet, a black hull drew cracks)
const woolInk = new THREE.MeshBasicMaterial({ color: '#363D52', side: THREE.BackSide });
// one fleece blob as a plain mesh (inked), for props that carry a few
function blobMesh(s = 1, seed = 1, color = WOOL) {
  const m = new THREE.Mesh(blobGeo(seed), color === WOOL ? woolMat() : woolMat(color, '#2A2C33')); m.scale.setScalar(s); m.castShadow = m.receiveShadow = true;
  const o = new THREE.Mesh(blobGeo(seed), woolInk); o.scale.setScalar(1.035); o.name = 'outline'; m.add(o); return m;
}
// a burst of opaque inked puffs that fly out and shrink to nothing (never a translucent cloud): o.at, o.r (size), o.color, o.n; o.dz the depth of the
// scatter (0.7; 0.1 keeps them out to the sides, off a chest), o.up their rise
function puffBurst(o = {}) {
  const g = grp(), n = o.n ?? 7, R = o.r ?? 0.2, C = o.color || '#FFFFFF', ps = [];
  for (let i = 0; i < n; i++) { const m = sphere(R, C, 1, { noGrain: true, emissive: '#4A4A50' }); ink(m, 0.08); m.castShadow = false; const a = i / n * TAU + hsh(i + 3) * 0.6;
    ps.push({ m, dx: Math.cos(a), dy: (o.up ?? 0.35) + 0.5 * hsh(i + 9), dz: Math.sin(a) * (o.dz ?? 0.7), k: 0.8 + 0.4 * hsh(i + 5) }); g.add(m); }
  g.userData.burst = (t, t0) => { const u = t0 == null ? -1 : (t - t0) / (o.dur ?? 0.42); const on = u >= 0 && u < 1; g.visible = on; if (!on) return;
    const e = 1 - (1 - u) * (1 - u), s = (u < 0.25 ? u / 0.25 : 1 - (u - 0.25) / 0.75);
    for (const p of ps) { p.m.position.set(p.dx * (o.spread ?? 0.55) * e * p.k, p.dy * (o.spread ?? 0.55) * e, p.dz * (o.spread ?? 0.55) * e * p.k); p.m.scale.setScalar(Math.max(0.001, s * p.k * (0.6 + 0.6 * u))); } };
  g.userData.burst(0, null); return g;
}
// soft inked steam: three small white puffs rising from the pivot, shrinking to nothing as they go
function steamPuffs(o = {}) {
  const g = grp(), ps = [];
  for (let i = 0; i < 4; i++) { const m = sphere(o.r ?? 0.035, '#FFFFFF', 1, { noGrain: true, emissive: '#8A8E96' }); ink(m, 0.1); m.castShadow = false; g.add(m); ps.push({ m, ph: i / 4 }); }
  g.userData.update = t => { for (const p of ps) { const u = (t * (o.rate ?? 0.9) + p.ph) % 1; p.m.position.set(Math.sin(u * 6 + p.ph * 9) * 0.03, u * (o.h ?? 0.28), 0); p.m.scale.setScalar(Math.max(0.001, Math.sin(u * PI) * (1.2 - 0.4 * u))); } };
  g.userData.update(0); return g;
}

export const MOUTONS_PROPS = {
  // ---------------------------------------------------------------- a sheep (the series' creature 'sheep' driven from inside: white fleece, black face and
  // legs, a round body), pivot at its feet, faces +Z. o.s its size (1); o.black: the black sheep (charcoal-grey fleece so its eyes still read, oversized
  // white eyes with thick red rims and grey bags, never a glow); o.clip [[t, clip]] ('idle', 'walk', 'sit', 'eat'...); o.hops [[t0, dur, [x, y, z], h]]:
  // hops to those points (prop frame) in arcs h high, a crouch before, legs tucked in the air, a squash on landing; o.yaw [[t, rad]] the body turns;
  // o.head [[t, rad]] the head turns (+ = to its left), o.chin [[t, rad]] the head tips up (+); o.nod [t...]: one nod each; o.shake [[t0, t1]]: a slow
  // « no »; o.bleat [t...]: the mouth opens wide, the head lifts, the body squashes; o.chew [[t0, t1]]; o.expr [[t, name]]; o.blinks [t...]; o.pop [t0, t1]:
  // eyes on stalks; o.back [[t, 0..1]]: rolled onto its back, hooves up, the face turned to the sky (o.backHead the head's tip); o.tap [t...]: a front hoof
  // taps the belly (o.tapAmp how high, 1.3; o.tapZ a swing in across the belly; o.tapSq the body's bounce on each tap); o.snore [[t0, t1]]: a snot bubble swells and shrinks at the nose; o.appear t / o.vanish t: it pops in / vanishes in a puff of wool;
  // o.sq [[t, [x, y, z]]]: a squash about its feet; o.bob: a slow ride up and down (on a wave)
  mtSheep(o) {
    const blk = !!o.black, S = o.s ?? 1;
    const colors = blk ? { body: '#55555D', face: '#141418', leg: '#141418', ...(o.colors || {}) } : (o.colors || {});
    const cr = buildCreature('sheep', { seed: o.seed ?? 3, colors, scale: S });
    const J = cr.userData.joints, anim = cr.userData.animate, g = grp(), mv = grp(), sqg = grp(), turn = grp(), roll = grp();
    g.add(mv); mv.add(sqg); sqg.add(turn); turn.add(roll); roll.add(cr);
    // (round 1) the faceted body lumps become the same round fleece as the masses (one wool look); o.rim: a pale moonlit rim around the fleece (a dark
    // sheep on a night meadow read as a hole); o.key: a small cool key light above and in front of it (intensity), o.keyPos
    const bodyHex = new THREE.Color(colors.body || '#F4F0E4').getHexString(), swaps = [];
    cr.traverse(m => { if (m.isMesh && m.name !== 'outline' && m.material?.color && m.material.color.getHexString() === bodyHex) swaps.push(m); });
    const rimMat = o.rim ? new THREE.MeshBasicMaterial({ color: o.rim, side: THREE.BackSide }) : null;
    swaps.forEach((m, i) => {
      if (!m.geometry.boundingBox) m.geometry.computeBoundingBox();
      const bb = m.geometry.boundingBox, sz = bb.getSize(new THREE.Vector3()), c = bb.getCenter(new THREE.Vector3()), src = blobGeo(40 + ((o.seed ?? 3) + i) % 6), sb = src.boundingBox, ss = sb.getSize(new THREE.Vector3()), sc = sb.getCenter(new THREE.Vector3());
      const geo = src.clone(); geo.translate(-sc.x, -sc.y, -sc.z); geo.scale(sz.x / ss.x * 1.06, sz.y / ss.y * 1.06, sz.z / ss.z * 1.06); geo.translate(c.x, c.y, c.z); geo.computeBoundingBox(); geo.computeBoundingSphere();
      m.geometry = geo; m.material = blk ? woolMat(colors.body, o.rim ? '#262A3A' : '#1A1C22') : woolMat();
      for (const ch of m.children) if (ch.name === 'outline') { ch.geometry = geo; ch.material = woolInk; }
      if (rimMat) { const rm = new THREE.Mesh(geo, rimMat), k = o.rimT ?? 0.07; rm.scale.set(1 + 2 * k / sz.x, 1 + 2 * k / sz.y, 1 + 2 * k / sz.z); rm.position.set(c.x * (1 - rm.scale.x), c.y * (1 - rm.scale.y), c.z * (1 - rm.scale.z)); rm.name = 'rim'; m.add(rm); }
    });
    if (o.key) { const kl = new THREE.PointLight(o.keyColor || '#C8D8FF', o.key, 4.5 * S, 1.2); kl.position.set(...(o.keyPos || [0.6 * S, 1.8 * S, 1.4 * S])); kl.castShadow = false; turn.add(kl); }
    // the eyes: found by their white; the black sheep's are bigger, wider apart, rimmed thick red, with grey bags under them
    const eyes = [];
    cr.traverse(m => { if (m.isMesh && m.geometry?.type === 'SphereGeometry' && m.material?.color && m.material.color.getHexString() === 'f8f5ec') eyes.push(m); });
    const ES = o.eye ?? (blk ? 1.42 : 1.12), EX = blk ? 1.42 : 1.12;
    const eyeG = eyes.map(e => e.parent), eyeY = eyeG.map(e => e.position.y), rims = [];
    for (const e of eyes) {
      e.parent.scale.setScalar(ES);
      if (blk) { const rim = e.children.find(c => c.name === 'outline'); if (rim) { rim.material = new THREE.MeshBasicMaterial({ color: '#D2333C', side: THREE.BackSide }); rim.scale.setScalar(1.3); rims.push(rim); }
        const bag = new THREE.Mesh(new THREE.TorusGeometry(e.geometry.parameters.radius * 0.82, e.geometry.parameters.radius * 0.17, 5, 12, PI * 0.8), mat('#8E8E9A', { noGrain: true }));
        bag.rotation.z = PI + PI * 0.1; bag.position.set(0, -e.geometry.parameters.radius * 0.62, e.geometry.parameters.radius * 0.4); e.parent.add(bag); }
    }
    // a mouth on the face (the creature has no jaw): a dark slot that opens
    const mouth = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.03, 0.02), mat('#7A1E22', { noGrain: true })); mouth.position.set(0, 0.045, 0.148); if (J.head) J.head.add(mouth);
    // the snot bubble at the nose
    const snot = new THREE.Mesh(new THREE.SphereGeometry(1, 12, 9), new THREE.MeshLambertMaterial({ color: '#BFE3F5', emissive: '#3A5A6A' })); const snHl = new THREE.Mesh(new THREE.SphereGeometry(0.22, 8, 6), new THREE.MeshBasicMaterial({ color: '#FFFFFF' })); snHl.position.set(-0.4, 0.45, 0.7); snot.add(snHl);
    ink(snot, 0.06); snot.visible = false; if (J.head) J.head.add(snot);
    const puff = puffBurst({ r: 0.2 * S, spread: 0.6 * S }); puff.position.y = 0.55 * S; g.add(puff);
    const HOPS = (o.hops || []).map(h => ({ t0: h[0], d: h[1], to: h[2], h: h[3] ?? 0.6 })); let p0 = o.p0 || [0, 0, 0];
    for (const h of HOPS) { h.from = p0; p0 = h.to; }
    const hopState = t => {
      let p = o.p0 || [0, 0, 0], sq = 1, air = 0, pitch = 0;
      for (const h of HOPS) {
        if (t < h.t0 - 0.08) break;
        if (t < h.t0) { p = h.from; const u = (t - (h.t0 - 0.08)) / 0.08; sq = 1 - 0.16 * Math.sin(u * PI / 2); continue; }
        if (t < h.t0 + h.d) { const u = (t - h.t0) / h.d; p = [lerp(h.from[0], h.to[0], u), lerp(h.from[1], h.to[1], u) + h.h * 4 * u * (1 - u), lerp(h.from[2], h.to[2], u)];
          sq = 1 + 0.2 * (1 - 2 * u) * (u < 0.5 ? 1 : 0.6); air = Math.sin(u * PI); pitch = -0.35 * (1 - 2 * u); continue; }
        p = h.to; const v = t - (h.t0 + h.d); if (v < 0.35) sq = 1 - 0.24 * Math.exp(-v * 11) * Math.cos(v * 20);
      }
      return { p, sq, air, pitch };
    };
    const pupBase = [];
    g.userData.update = t => {
      const clip = stepAt(o.clip, t, 'idle'); let ct = t; for (const k of o.clip || []) if (t >= k[0]) ct = t - k[0];
      const ex = stepAt(o.expr, t, null), snoring = within(o.snore, t), back = keyAt(o.back, t, 0);
      anim(clip, Math.max(0, ct), { blinks: o.blinks || [], ...(o.pop ? { popAt: o.pop, popLen: o.popLen ?? 0.12 } : {}), ...(ex ? { expression: ex } : snoring ? { expression: 'closed' } : {}) });
      eyeG.forEach((e, i) => { e.position.x *= EX; e.position.y = eyeY[i] + (blk ? 0.012 : 0.0); e.position.z += 0.01; });
      // shut eyes: the red rims go (two red rings on a shut black face read as angry open eyes)
      const shut = (ex || (snoring ? 'closed' : null)) === 'closed'; for (const rm of rims) rm.visible = !shut;
      // the hop
      const hs = hopState(t); mv.position.set(hs.p[0], hs.p[1] + (o.bob ? o.bob * Math.sin(t * 5.2 + (o.bobPh ?? 0)) : 0), hs.p[2]);
      const ksq = keyAt(o.sq, t, [1, 1, 1]); const sy = hs.sq * ksq[1]; sqg.scale.set(ksq[0] / Math.sqrt(hs.sq), sy, ksq[2] / Math.sqrt(hs.sq));
      if (hs.air > 0.01 && J.legFL) { const a = hs.air; J.legFL.rotation.x -= 0.9 * a; J.legFR.rotation.x -= 0.8 * a; J.legBL.rotation.x += 0.9 * a; J.legBR.rotation.x += 1.0 * a;
        J.kneeFL.rotation.x += 0.9 * a; J.kneeFR.rotation.x += 0.9 * a; J.kneeBL.rotation.x -= 0.6 * a; J.kneeBR.rotation.x -= 0.6 * a; }
      if (J.body) J.body.rotation.x += hs.pitch;
      turn.rotation.y = keyAt(o.yaw, t, 0);
      // head: turn, chin, nods, the slow « no », the bleat
      let hy = keyAt(o.head, t, 0), hx = -keyAt(o.chin, t, 0), mo = 0;
      for (const n of o.nod || []) { const u = (t - n) / 0.26; if (u >= 0 && u < 1) hx += 0.42 * Math.sin(u * PI); }
      const shk = within(o.shake, t); if (shk) { const u = t - shk[0], w = smooth(u / 0.15) * smooth((shk[1] - t) / 0.15); hy += 0.42 * Math.sin(u * TAU * (o.shakeHz ?? 1.6)) * w; }
      let bsq = 1; for (const b of o.bleat || []) { const u = (t - b) / 0.36; if (u >= 0 && u < 1) { const e = Math.sin(u * PI); hx -= 0.4 * e; mo = Math.max(mo, e); bsq = Math.min(bsq, 1 - 0.1 * e); } }
      const chw = within(o.chew, t); if (chw) mo = Math.max(mo, 0.5 + 0.5 * Math.sin((t - chw[0]) * 26));
      if (J.head) { J.head.rotation.y += hy; J.head.rotation.x += hx; }
      if (J.neck) J.neck.rotation.x += hx * 0.4;
      mouth.scale.set(1 + 0.3 * mo, 0.4 + 3.2 * mo, 1);
      if (bsq !== 1) sqg.scale.multiply(new THREE.Vector3(1 / Math.sqrt(bsq), bsq, 1 / Math.sqrt(bsq)));
      // on its back: rolled about its length, the body's middle lowered onto the grass, the face turned up
      const cy = 0.58 * S;
      if (back > 0.001) { roll.rotation.z = PI * back; roll.position.set(0, lerp(cy, 0.36 * S, back) - cy * Math.cos(PI * back), 0);
        if (J.head) J.head.rotation.x += (o.backHead ?? 1.2) * back; if (J.neck) J.neck.rotation.x += 0.35 * back;
        for (const lg of ['legFL', 'legFR', 'legBL', 'legBR']) if (J[lg]) J[lg].rotation.z += (lg.endsWith('L') ? 0.18 : -0.18) * back;
        for (const tp of o.tap || []) { const u = (t - tp) / 0.22; if (u >= 0 && u < 1 && J.legFR) { const e = Math.sin(u * PI); J.legFR.rotation.x += (o.tapAmp ?? 1.3) * e; J.legFR.rotation.z += (o.tapZ ?? 0) * e; J.kneeFR.rotation.x -= 0.6 * e;
          if (o.tapSq) { const b = u > 0.5 ? Math.sin((u - 0.5) * 2 * PI) : 0; sqg.scale.multiply(new THREE.Vector3(1 + o.tapSq * b, 1 - o.tapSq * b, 1 + o.tapSq * b)); } } } }
      else { roll.rotation.z = 0; roll.position.set(0, 0, 0); }
      // the snot bubble
      snot.visible = !!snoring; if (snoring) { const u = (t - snoring[0]) / (o.snorePer ?? 0.9), k = 0.3 + 0.7 * (0.5 - 0.5 * Math.cos(u * TAU)), R = (o.snoreR ?? 0.07) * k; snot.scale.setScalar(R); snot.position.set(0.03, 0.06, 0.16 + R); }
      // appear / vanish
      let sc = popK(o.appear, t, 0.12);
      if (o.vanish != null) { const v = t - o.vanish; if (v >= 0) sc = v < 0.06 ? 1 + 0.25 * (v / 0.06) : Math.max(0, 1.25 * (1 - (v - 0.06) / 0.07)); if (v > 0.06) sqg.scale.multiply(new THREE.Vector3(0.8, 1.3, 0.8)); }
      mv.scale.setScalar(Math.max(0.0001, sc)); mv.visible = sc > 0.001;
      puff.position.set(hs.p[0], hs.p[1] + 0.55 * S, hs.p[2]); puff.userData.burst(t, o.vanish != null ? o.vanish + 0.05 : null);
    };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a mass of faceless fleece: one faceted white lump (no head, no legs) instanced, inked.
  // Pivot at the origin of the set (positions are local). o.fill: a list of placements, each {kind: 'box', x:[a,b], y:[a,b], z:[a,b], n, s:[a,b]} (a room
  // packed floor to ceiling), {kind: 'layer', x, z, y, n, s, h} (a lumpy blanket on the ground), {kind: 'heap', c:[x,y,z], r, h, n, s}, {kind: 'ramp', a, b, w,
  // n, s, h} (down a flight), {kind: 'pts', pts: [[x, y, z, s], ...]}; o.seed; o.grow [t0, dur]: they pop in, lowest first; o.shrink [t0, dur]: they shrink to
  // nothing in a random order; o.front {dir, from, to, t0, t1}: they pop in as a front passes along dir; o.bob: they bob (m); o.color; o.holes
  mtFleece(o) {
    const g = grp(), P = [], R = (i => () => hsh(i++ * 1.37 + (o.seed ?? 1) * 101.3))(1);
    const rr = (a, b) => a + (b - a) * R();
    for (const f of o.fill || []) {
      const s = f.s || [0.7, 1.1];
      if (f.kind === 'box') for (let i = 0; i < f.n; i++) P.push([rr(...f.x), rr(...f.y), rr(...f.z), rr(...s)]);
      else if (f.kind === 'layer') for (let i = 0; i < f.n; i++) { const sc = rr(...s); P.push([rr(...f.x), (f.y ?? 0) + sc * 0.3 + R() * (f.h ?? 0.2), rr(...f.z), sc]); }
      else if (f.kind === 'heap') for (let i = 0; i < f.n; i++) { const a = R() * TAU, q = Math.sqrt(R()), rad = q * f.r, top = f.h * (1 - q * q); P.push([f.c[0] + Math.cos(a) * rad, f.c[1] + R() * top + 0.25, f.c[2] + Math.sin(a) * rad, rr(...s)]); }
      else if (f.kind === 'ramp') for (let i = 0; i < f.n; i++) { const u = R(), w = (R() - 0.5) * f.w; P.push([lerp(f.a[0], f.b[0], u) + w * (f.wx ?? 1), lerp(f.a[1], f.b[1], u) + R() * (f.h ?? 0.4), lerp(f.a[2], f.b[2], u) + w * (f.wz ?? 0), rr(...s)]); }
      else if (f.kind === 'pts') for (const q of f.pts) P.push([q[0], q[1], q[2], q[3] ?? 1]);
    }
    // o.holes [[x, z, r, ymax], ...]: no blob whose top rises above ymax within r of (x, z) (a head that pokes out of the wool, a sheep buried to the chin)
    for (const [hx, hz, hr, hy] of o.holes || []) for (let i = P.length - 1; i >= 0; i--) { const q = P[i]; if (Math.hypot(q[0] - hx, q[2] - hz) < hr + 0.35 * q[3] && q[1] + 0.45 * q[3] > hy) P.splice(i, 1); }
    const n = P.length, geo = blobGeo(o.seed ?? 1), M = new THREE.InstancedMesh(geo, o.color ? woolMat(o.color, '#4A4E58') : woolMat(), Math.max(1, n));
    const OL = new THREE.InstancedMesh(geo, woolInk, Math.max(1, n)); M.castShadow = M.receiveShadow = true; OL.castShadow = false;
    // a slight cool or warm tint per lobe cluster (one flat white read as a sheet of paper)
    const tint = new THREE.Color(); for (let i = 0; i < n; i++) { const v = hsh(i * 4.7 + 1.3); tint.setRGB(0.93 + 0.07 * v, 0.95 + 0.05 * v, 0.98 + 0.02 * hsh(i * 2.9)); M.setColorAt(i, tint); }
    if (M.instanceColor) M.instanceColor.needsUpdate = true;
    g.add(M, OL);
    const rot = P.map((_, i) => [hsh(i * 3.1) * TAU, hsh(i * 5.7) * TAU]), rank = P.map((_, i) => hsh(i * 9.3 + 2)), ph = P.map((_, i) => hsh(i * 2.3) * TAU);
    const ys = P.map(q => q[1]), y0 = Math.min(...ys, 0), y1 = Math.max(...ys, 1);
    const ob = new THREE.Object3D(), FR = o.front, fdir = FR ? new THREE.Vector3(...FR.dir).normalize() : null;
    const setAll = t => {
      for (let i = 0; i < n; i++) {
        const q = P[i]; let k = 1, dy = 0;
        if (o.grow) { const t0 = o.grow[0] + o.grow[1] * (q[1] - y0) / Math.max(0.01, y1 - y0) * 0.85 + 0.12 * rank[i] * o.grow[1]; k *= popK(t0, t, 0.16); }
        if (FR) { const d = fdir.x * q[0] + fdir.y * q[1] + fdir.z * q[2], ft = FR.t0 + (FR.t1 - FR.t0) * clamp01((d - FR.from) / (FR.to - FR.from)); k *= popK(ft, t, 0.18); if (t > ft && t < ft + 0.5) dy += 0.15 * Math.sin((t - ft) / 0.5 * PI); }
        if (o.shrink) { const ts = o.shrink[0] + o.shrink[1] * rank[i], v = t - ts; if (v > 0) k *= v < 0.05 ? 1 + 0.15 * v / 0.05 : Math.max(0, 1.15 * (1 - (v - 0.05) / 0.12)); }
        if (o.bob) dy += o.bob * Math.sin(t * (o.bobF ?? 4.5) + ph[i]);
        const s = Math.max(0.0001, q[3] * k);
        ob.position.set(q[0], q[1] + dy, q[2]); ob.rotation.set(0.25 * Math.sin(rot[i][0]), rot[i][1], 0.25 * Math.cos(rot[i][0])); ob.scale.setScalar(s); ob.updateMatrix(); M.setMatrixAt(i, ob.matrix);
        ob.scale.setScalar(s * 1.03); ob.updateMatrix(); OL.setMatrixAt(i, ob.matrix);
      }
      M.instanceMatrix.needsUpdate = true; OL.instanceMatrix.needsUpdate = true; M.computeBoundingSphere(); OL.computeBoundingSphere();
    };
    const animated = o.grow || o.shrink || o.front || o.bob;
    if (animated) g.userData.update = t => setAll(t);
    setAll(animated ? 0 : 99); g.userData.count = n; return g;
  },

  // ---------------------------------------------------------------- a little white picket fence segment (pivot at the floor in its middle, along X, faces
  // +Z): o.len (1.2), o.h (0.55), pointed pickets, two rails, two posts, inked; o.pop t: it pops up out of the floor with an overshoot; o.rattle [t...]
  mtFence(o) {
    const Lg = o.len ?? 1.2, H = o.h ?? 0.55, C = o.color || '#F7F6F0', g = grp(), k = grp(); g.add(k);
    const n = Math.max(3, Math.round(Lg / 0.17));
    for (let i = 0; i < n; i++) { const x = -Lg / 2 + (i + 0.5) * Lg / n; k.add(at(box(0.075, H - 0.06, 0.03, C, { pivot: 'bottom', outline: 0.04, noGrain: true, emissive: '#3A3C42' }), x, 0.012, 0.03));
      k.add(at(box(0.053, 0.053, 0.03, C, { outline: 0.04, noGrain: true, emissive: '#3A3C42' }), x, H - 0.06, 0.03, 0, 0, PI / 4)); }
    for (const y of [H * 0.28, H * 0.66]) k.add(at(box(Lg + 0.06, 0.05, 0.03, C, { outline: 0.03, noGrain: true, emissive: '#3A3C42' }), 0, y, 0.0));
    for (const sx of [-1, 1]) k.add(at(box(0.07, H + 0.02, 0.07, C, { pivot: 'bottom', outline: 0.03, noGrain: true, emissive: '#3A3C42' }), sx * (Lg / 2 + 0.035), 0.012, 0.0));
    g.userData.update = t => { const p = popK(o.pop, t, 0.14); k.scale.set(1 + 0.12 * (1 - Math.min(1, p)) * (p > 0 ? 1 : 0), Math.max(0.001, p), 1); k.visible = p > 0.001; k.rotation.z = shake(o.rattle, t, 0.06, 40, 8); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the black sheep's thought bubble (pivot at its middle, faces +Z, unlit so it stays white by
  // night): a scalloped cloud with an ink border and three little circles trailing down toward o.tail [x, y] (bubble plane, metres); inside, a 2D loop: a
  // tiny box-headed man in a dark suit and a red tie runs and hops a little white fence. o.w (1.1); o.state 0 plain, 1 leaning forward, 2 panting (tongue
  // out, sweat, a lower, slower hop), or [[t, state]]; o.night: a moonlit meadow inside; o.sheep: a black sheep in the left corner (o.sheepW of the width, 0.3) nods at each hop;
  // o.period (s, 0.9), o.t0 (the phase); o.pop t: it pops in; o.res (512)
  mtBubble(o) {
    const W = o.w ?? 1.1, H = W * (o.aspect ?? 0.72), g = grp(), k = grp(); g.add(k);
    const shape = new THREE.Shape(), NB = 11, rx = W / 2, ry = H / 2;
    for (let i = 0; i <= NB * 8; i++) { const a = i / (NB * 8) * TAU, lob = Math.abs(Math.sin(a * NB / 2)), rr = 1 - 0.07 * (1 - lob) ** 2 + 0.0, x = Math.cos(a) * rx * rr, y = Math.sin(a) * ry * rr; i ? shape.lineTo(x, y) : shape.moveTo(x, y); }
    const geo = new THREE.ShapeGeometry(shape, 4), uv = geo.attributes.uv, ps = geo.attributes.position;
    for (let i = 0; i < uv.count; i++) uv.setXY(i, ps.getX(i) / W + 0.5, ps.getY(i) / H + 0.5);
    const res = o.res ?? 512, cv = canvas(res, Math.round(res * H / W)), cx = cv.getContext('2d'), tx = texOf(cv);
    const face = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ map: tx, toneMapped: false })); face.renderOrder = 2; k.add(face);
    const border = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: INK, toneMapped: false })); border.scale.set(1 + 0.05 / W, 1 + 0.05 / H, 1); border.position.z = -0.012; k.add(border);
    const back = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: '#F4F4F0', toneMapped: false, side: THREE.BackSide })); back.position.z = -0.02; k.add(back);
    const tail = o.tail || [-W * 0.38, -H * 0.85];
    [[0.62, 0.15], [0.8, 0.1], [0.95, 0.065]].forEach(([u, r], i) => { const R_ = r * (1 + 0.25 * (W / 1.1 - 1)), c = new THREE.Mesh(new THREE.CircleGeometry(R_, 16), new THREE.MeshBasicMaterial({ color: '#FFFFFF', toneMapped: false })), b = new THREE.Mesh(new THREE.CircleGeometry(R_ * 1.22, 16), new THREE.MeshBasicMaterial({ color: INK, toneMapped: false }));
      const x = lerp(-W * 0.2, tail[0], u), y = lerp(-H * 0.42, tail[1], u); c.position.set(x, y, 0.001); b.position.set(x, y, -0.012); k.add(c, b); });
    const PER = o.period ?? 0.9, T0 = o.t0 ?? 0;
    let last = -999;
    const draw = (t, st) => {
      const w = cv.width, h = cv.height, night = !!o.night;
      const sky = cx.createLinearGradient(0, 0, 0, h); if (night) { sky.addColorStop(0, '#16224A'); sky.addColorStop(1, '#30477A'); } else { sky.addColorStop(0, '#CFE8FA'); sky.addColorStop(1, '#EAF6FF'); }
      cx.fillStyle = sky; cx.fillRect(0, 0, w, h);
      const gy = h * 0.74;
      if (night) { cx.fillStyle = '#F6F0D2'; cx.beginPath(); cx.arc(w * 0.78, h * 0.24, h * 0.1, 0, TAU); cx.fill(); cx.fillStyle = '#E2DAB4'; cx.beginPath(); cx.arc(w * 0.76, h * 0.22, h * 0.025, 0, TAU); cx.fill();
        cx.fillStyle = '#FFF6D8'; for (let i = 0; i < 14; i++) cx.fillRect(w * hsh(i + 1), h * 0.5 * hsh(i + 7), w * 0.006, w * 0.006); }
      cx.fillStyle = night ? '#2A4E5A' : '#8CCB62'; cx.fillRect(0, gy, w, h - gy); cx.strokeStyle = INK; cx.lineWidth = w * 0.008; cx.beginPath(); cx.moveTo(0, gy); cx.lineTo(w, gy); cx.stroke();
      // the fence
      const fx = w * 0.52, fh = h * 0.17, fw = w * 0.15;
      cx.lineWidth = w * 0.007; cx.fillStyle = '#FBFAF4';
      for (let i = 0; i < 4; i++) { const x = fx - fw / 2 + i * fw / 3 - w * 0.012; cx.beginPath(); cx.moveTo(x, gy); cx.lineTo(x, gy - fh); cx.lineTo(x + w * 0.012, gy - fh - w * 0.015); cx.lineTo(x + w * 0.024, gy - fh); cx.lineTo(x + w * 0.024, gy); cx.closePath(); cx.fill(); cx.stroke(); }
      cx.fillRect(fx - fw / 2 - w * 0.02, gy - fh * 0.75, fw + w * 0.04, h * 0.025); cx.strokeRect(fx - fw / 2 - w * 0.02, gy - fh * 0.75, fw + w * 0.04, h * 0.025);
      // the little man: runs left to right, hops the fence, runs out, comes back in
      const per = st >= 2 ? PER * 1.2 : PER, u = (((t - T0) / per) % 1 + 1) % 1, x0 = o.sheep ? w * 0.36 : w * 0.14, x1 = w * 0.92;
      const xm = lerp(x0, x1, u), ju = clamp01((u - 0.32) / 0.4), hop = Math.sin(ju * PI) * h * (st >= 2 ? 0.2 : 0.27) * (ju > 0 && ju < 1 ? 1 : 0);
      const S_ = h * 0.2, lean = st >= 1 ? 0.32 : 0.08, run = Math.sin(u * TAU * 4);
      cx.save(); cx.translate(xm, gy - hop); cx.rotate(lean);
      cx.lineWidth = w * 0.006; cx.strokeStyle = INK; cx.lineJoin = 'round';
      const inAir = ju > 0 && ju < 1;
      // legs
      cx.fillStyle = '#232838';
      const leg = (a, dx) => { cx.save(); cx.translate(dx, -S_ * 0.42); cx.rotate(a); cx.fillRect(-S_ * 0.06, 0, S_ * 0.12, S_ * 0.42); cx.strokeRect(-S_ * 0.06, 0, S_ * 0.12, S_ * 0.42); cx.restore(); };
      if (inAir) { leg(-1.0, -S_ * 0.06); leg(0.9, S_ * 0.06); } else { leg(0.6 * run, -S_ * 0.05); leg(-0.6 * run, S_ * 0.05); }
      // body: a navy jacket, a white shirt V, a red tie
      cx.fillStyle = '#26324F'; cx.fillRect(-S_ * 0.2, -S_ * 0.95, S_ * 0.4, S_ * 0.55); cx.strokeRect(-S_ * 0.2, -S_ * 0.95, S_ * 0.4, S_ * 0.55);
      cx.fillStyle = '#F4F2EC'; cx.beginPath(); cx.moveTo(-S_ * 0.09, -S_ * 0.95); cx.lineTo(S_ * 0.09, -S_ * 0.95); cx.lineTo(0, -S_ * 0.72); cx.closePath(); cx.fill();
      cx.fillStyle = '#D02A2E'; cx.beginPath(); cx.moveTo(-S_ * 0.03, -S_ * 0.93); cx.lineTo(S_ * 0.03, -S_ * 0.93); cx.lineTo(S_ * 0.04, -S_ * 0.62); cx.lineTo(0, -S_ * 0.55); cx.lineTo(-S_ * 0.04, -S_ * 0.62); cx.closePath(); cx.fill();
      if (inAir || st >= 1) { cx.save(); cx.translate(S_ * 0.3, -S_ * 0.82); cx.rotate(-0.6); cx.fillStyle = '#D02A2E'; cx.fillRect(0, -S_ * 0.03, S_ * 0.2, S_ * 0.06); cx.restore(); }
      // arms
      cx.fillStyle = '#26324F';
      const arm = a => { cx.save(); cx.translate(0, -S_ * 0.9); cx.rotate(a); cx.fillRect(-S_ * 0.05, 0, S_ * 0.1, S_ * 0.38); cx.strokeRect(-S_ * 0.05, 0, S_ * 0.1, S_ * 0.38); cx.restore(); };
      if (inAir) { arm(-2.4); arm(2.4); } else { arm(0.8 * run); arm(-0.8 * run); }
      // the box head: skin, black hair on top, two dot eyes, a mouth
      cx.fillStyle = '#E9B78E'; cx.fillRect(-S_ * 0.17, -S_ * 1.32, S_ * 0.34, S_ * 0.37); cx.strokeRect(-S_ * 0.17, -S_ * 1.32, S_ * 0.34, S_ * 0.37);
      cx.fillStyle = '#1A1A1E'; cx.fillRect(-S_ * 0.18, -S_ * 1.36, S_ * 0.36, S_ * 0.09);
      cx.fillRect(-S_ * 0.08, -S_ * 1.2, S_ * 0.04, S_ * 0.06); cx.fillRect(S_ * 0.05, -S_ * 1.2, S_ * 0.04, S_ * 0.06);
      if (st >= 2) { cx.fillStyle = '#5A1A1E'; cx.beginPath(); cx.arc(S_ * 0.02, -S_ * 1.04, S_ * 0.05, 0, PI); cx.fill(); cx.fillStyle = '#E06A7A'; cx.fillRect(S_ * 0.0, -S_ * 1.03, S_ * 0.05, S_ * 0.1);
        cx.fillStyle = '#9FD3E8'; for (let i = 0; i < 2; i++) { const yy = -S_ * (1.3 - ((t * 1.6 + i * 0.5) % 1) * 0.3); cx.beginPath(); cx.arc(-S_ * 0.26 - i * S_ * 0.06, yy, S_ * 0.035, 0, TAU); cx.fill(); cx.stroke(); } }
      else { cx.fillStyle = '#1A1A1E'; cx.fillRect(-S_ * 0.05, -S_ * 1.04, S_ * 0.1, S_ * 0.02); }
      cx.restore();
      // (round 1) the black sheep in the corner: a clear silhouette about a third of the bubble wide (a dark fleece of round lobes with a pale moonlit
      // rim, black legs, a black head with big white red-rimmed eyes), its head nodding hard at each hop (down at the top of the hop, back up after)
      if (o.sheep) { const nod = Math.sin(clamp01((u - 0.4) / 0.32) * PI), SW = w * (o.sheepW ?? 0.3), sx = w * 0.04 + SW * 0.5, sy = gy - SW * 0.3, R = SW * 0.2;
        const lobes = [[0, 0, 1.25], [-0.85, 0.15, 0.9], [0.85, 0.1, 0.95], [-0.45, -0.55, 0.85], [0.45, -0.6, 0.85], [-0.4, 0.62, 0.8], [0.4, 0.6, 0.8], [-1.15, -0.25, 0.65], [1.1, -0.3, 0.7]];
        cx.fillStyle = '#141418'; for (const dx of [-0.75, -0.3, 0.35, 0.8]) { cx.fillRect(sx + dx * R - R * 0.14, sy + R * 0.5, R * 0.28, SW * 0.3 - R * 0.2 + h * 0.005); }
        cx.fillStyle = '#B9CCF2'; for (const [lx, ly, lr] of lobes) { cx.beginPath(); cx.arc(sx + lx * R, sy + ly * R, lr * R + w * 0.009, 0, TAU); cx.fill(); }
        cx.fillStyle = '#4E5262'; for (const [lx, ly, lr] of lobes) { cx.beginPath(); cx.arc(sx + lx * R, sy + ly * R, lr * R, 0, TAU); cx.fill(); }
        cx.fillStyle = '#5E6274'; for (const [lx, ly, lr] of lobes.slice(0, 3)) { cx.beginPath(); cx.arc(sx + lx * R - lr * R * 0.2, sy + ly * R - lr * R * 0.25, lr * R * 0.5, 0, TAU); cx.fill(); }
        cx.save(); cx.translate(sx + R * 1.55, sy - R * 0.55); cx.rotate(0.15 + 0.85 * nod); const HW = R * 0.95, HH = R * 1.25;
        cx.fillStyle = '#B9CCF2'; cx.beginPath(); cx.ellipse(HW * 0.35, HH * 0.15, HW * 0.62 + w * 0.009, HH * 0.6 + w * 0.009, 0.25, 0, TAU); cx.fill();
        cx.fillStyle = '#141418'; cx.beginPath(); cx.ellipse(HW * 0.35, HH * 0.15, HW * 0.62, HH * 0.6, 0.25, 0, TAU); cx.fill();
        cx.beginPath(); cx.ellipse(HW * -0.1, -HH * 0.25, HW * 0.32, HH * 0.14, -0.5, 0, TAU); cx.fill();
        for (const ex of [0.1, 0.62]) { cx.fillStyle = '#FFFFFF'; cx.strokeStyle = '#D2333C'; cx.lineWidth = w * 0.007; cx.beginPath(); cx.arc(HW * ex, -HH * 0.05, HW * 0.2, 0, TAU); cx.fill(); cx.stroke();
          cx.fillStyle = '#111111'; cx.beginPath(); cx.arc(HW * ex + HW * 0.04, -HH * 0.02 + HW * 0.06 * nod, HW * 0.07, 0, TAU); cx.fill(); }
        cx.restore(); cx.strokeStyle = INK; cx.lineWidth = w * 0.006; }
      tx.needsUpdate = true;
    };
    g.userData.update = t => {
      const st = typeof o.state === 'number' ? o.state : stepAt(o.state, t, 0);
      if (Math.abs(t - last) > 1 / 90) { draw(t, st); last = t; }
      const p = popK(o.pop, t, 0.16), br = 1 + 0.012 * Math.sin(t * 3.1);
      k.scale.set(Math.max(0.001, p * br), Math.max(0.001, p * (2 - br)), 1); k.visible = p > 0.001;
    };
    g.userData.hopTimes = n => Array.from({ length: n }, (_, i) => T0 + PER * (i + 0.52));
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a woolly take: a puff of white fleece that bursts out of his head (attach to the head
  // joint, offset in its frame: the head 0.5 high from the chin); o.pop t: BOING (0 -> 1.35 -> 0.9 -> 1.05 -> 1); o.bob: it bounces as he runs
  mtWoolHair(o) {
    const g = grp(), k = grp(); g.add(k);
    const L_ = [[0, 0.12, 0, 0.2], [0.13, 0.08, 0.02, 0.15], [-0.13, 0.08, 0.02, 0.15], [0.07, 0.15, -0.09, 0.14], [-0.07, 0.15, -0.09, 0.14], [0.0, 0.05, 0.11, 0.12], [0.16, -0.02, -0.06, 0.11], [-0.16, -0.02, -0.06, 0.11]];
    L_.forEach(([x, y, z, s], i) => k.add(at(blobMesh(s, i + 2), x, y, z)));
    g.userData.update = t => { let s = 0; if (o.pop != null) { const u = t - o.pop; s = u < 0 ? 0 : u < 0.06 ? 1.35 * u / 0.06 : u < 0.12 ? lerp(1.35, 0.9, (u - 0.06) / 0.06) : u < 0.2 ? lerp(0.9, 1.05, (u - 0.12) / 0.08) : u < 0.3 ? lerp(1.05, 1, (u - 0.2) / 0.1) : 1; } else s = 1;
      const b = o.bob ? 1 + o.bob * Math.sin(t * 9) : 1; k.scale.set(Math.max(0.001, s), Math.max(0.001, s * b), Math.max(0.001, s)); k.visible = s > 0.001; };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a snowplough (pivot at the floor in its middle, faces +X): an orange cab with a driver
  // behind a clear windscreen, an amber lamp on the roof, a box blade in front and a big fleece roll rolling ahead of it (o.roll: true; o.speed m/s
  // spins it); no lettering
  mtPlough(o) {
    const C = o.color || '#E8782A', g = grp();
    g.add(at(box(2.6, 0.7, 1.8, C, { pivot: 'bottom', outline: 0.012 }), -0.2, 0.5, 0), at(box(1.3, 1.0, 1.7, C, { pivot: 'bottom', outline: 0.012 }), 0.15, 1.2, 0), at(box(1.4, 0.08, 1.8, '#C25A1E', { outline: 0.01 }), 0.15, 2.24, 0));
    const ws = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.75, 1.5), new THREE.MeshLambertMaterial({ color: '#CFEAF5', transparent: true, opacity: 0.3, depthWrite: false })); ws.position.set(0.81, 1.72, 0); g.add(ws);
    g.add(at(box(0.04, 0.85, 0.12, C), 0.8, 1.68, 0.8), at(box(0.04, 0.85, 0.12, C), 0.8, 1.68, -0.8), at(box(0.02, 0.8, 1.5, '#2A2D33'), -0.45, 1.7, 0));
    const drv = grp(at(box(0.32, 0.4, 0.3, '#3E5A3A', { outline: 0.01 }), 0, 0.2, 0), at(box(0.26, 0.26, 0.24, '#E0B48C', { outline: 0.01 }), 0.02, 0.55, 0), at(box(0.27, 0.06, 0.25, '#2A2420'), 0.02, 0.7, 0)); drv.position.set(0.2, 1.25, 0.35); g.add(drv);
    const lamp = at(cyl(0.12, 0.14, 0.16, '#F2A030', 8, { emissive: '#C86A10', noGrain: true, outline: 0.02 }), 0.15, 2.36, 0); g.add(lamp);
    for (const x of [-1.0, 0.7]) for (const z of [-0.9, 0.9]) g.add(at(cyl(0.45, 0.45, 0.3, '#22252A', 12), x, 0.45, z, PI / 2, 0, 0));
    // the box blade: a curved plate of three bands, side plates, two arms
    const BL = grp(); BL.position.set(1.65, 0, 0); g.add(BL);
    [[0.0, 0.25, 0.0], [0.08, 0.6, -0.25], [0.2, 0.92, -0.5]].forEach(([x, y, rz]) => BL.add(at(box(0.1, 0.38, 2.6, '#E8C23A', { outline: 0.012 }), x, y, 0, 0, 0, rz)));
    for (const z of [-1.3, 1.3]) BL.add(at(box(0.6, 1.0, 0.06, '#E8C23A', { pivot: 'bottom', outline: 0.012 }), -0.1, 0.05, z));
    for (const z of [-0.5, 0.5]) g.add(at(box(0.7, 0.12, 0.12, '#3A3D44'), 1.25, 0.65, z));
    let roll = null; if (o.roll !== false) { roll = grp(); roll.position.set(o.rollX ?? 2.45, o.rollR ?? 0.75, 0); g.add(roll); const RR = o.rollR ?? 0.75, LL = o.rollLen ?? 2.4;
      for (let i = 0; i < 26; i++) { const a = i / 26 * TAU * 2.0, z = -LL / 2 + (i % 13) / 12 * LL; roll.add(at(blobMesh(0.55 + 0.12 * hsh(i), (i % 5) + 1), Math.cos(a) * RR * 0.62, Math.sin(a) * RR * 0.62, z)); }
      roll.add(at(cyl(RR * 0.8, RR * 0.8, LL * 0.95, WOOL, 10, { noGrain: true, emissive: '#3A3E48' }), 0, 0, 0, PI / 2, 0, 0)); }
    g.userData.update = t => { lamp.rotation.y = t * 8; if (roll) roll.rotation.z = -(o.speed ?? 2.0) * t / (o.rollR ?? 0.75); drv.rotation.z = 0.03 * Math.sin(t * 7); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a market stall (pivot at the floor in the middle of its counter's front, faces +Z): a wooden
  // counter, four posts, a plain sloping awning with a scalloped edge (one colour: stripes read as flags), one steaming teapot and a pyramid of cups;
  // no lettering, no price. o.awning colour
  mtStall(o) {
    const A = o.awning || '#2F8F8C', g = grp(), Wd = o.w ?? 2.0, D = 0.8;
    g.add(at(box(Wd, 0.9, D, '#B08654', { pivot: 'bottom', outline: 0.008 }), 0, 0, -D / 2), at(box(Wd + 0.08, 0.06, D + 0.08, '#8A6438', { outline: 0.006 }), 0, 0.93, -D / 2));
    for (let i = 0; i < 5; i++) g.add(at(box(0.02, 0.86, 0.01, '#8A6438'), -Wd / 2 + (i + 0.5) * Wd / 5, 0.45, 0.005));
    for (const sx of [-1, 1]) for (const z of [0.02, -D - 0.02]) g.add(at(box(0.07, z > -0.1 ? 2.25 : 2.55, 0.07, '#8A6438', { pivot: 'bottom', outline: 0.01 }), sx * (Wd / 2 + 0.02), 0, z));
    const aw = at(box(Wd + 0.4, 0.05, D + 0.6, A, { outline: 0.008 }), 0, 2.4, -D / 2 + 0.1, -0.28, 0, 0); g.add(aw);
    const nsc = Math.round((Wd + 0.4) / 0.25);
    for (let i = 0; i < nsc; i++) { const s = new THREE.Mesh(new THREE.CircleGeometry(0.13, 10, PI, PI), mat(A, { doubleSide: true })); s.position.set(-(Wd + 0.4) / 2 + (i + 0.5) * (Wd + 0.4) / nsc, 2.25, 0.32); g.add(s); }
    g.add(at(box(Wd + 0.4, 0.06, 0.04, new THREE.Color(A).multiplyScalar(0.8).getStyle(), { outline: 0.01 }), 0, 2.27, 0.31));
    // the teapot (left) with its steam, the cups (right)
    const tp = grp(); tp.position.set(-Wd * 0.28, 0.96, -0.35); g.add(tp);
    const body = sphere(0.17, '#E8E2D2', 1, { emissive: '#3A3A40' }); body.scale.set(1, 0.8, 1); body.position.y = 0.13; ink(body, 0.05); tp.add(body);
    tp.add(at(cyl(0.07, 0.09, 0.05, '#C8402E', 8, { outline: 0.04 }), 0, 0.27, 0), at(sphere(0.03, '#C8402E', 0), 0, 0.31, 0), at(cyl(0.02, 0.035, 0.2, '#E8E2D2', 6, { outline: 0.05 }), 0.2, 0.17, 0, 0, 0, -0.9));
    tp.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.08, 0.018, 5, 10, PI), mat('#E8E2D2')), -0.17, 0.15, 0, 0, 0, PI / 2));
    const st = steamPuffs({ r: 0.04, h: 0.35 }); st.position.set(0.29, 0.26, 0); tp.add(st);
    const cups = grp(); cups.position.set(Wd * 0.22, 0.96, -0.35); g.add(cups);
    const cup = (x, y) => { const c = grp(at(cyl(0.065, 0.05, 0.1, '#F2EEE4', 10, { pivot: 'bottom', outline: 0.05, emissive: '#3A3A40' }), 0, 0, 0)); c.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.03, 0.01, 4, 8), mat('#F2EEE4')), 0.07, 0.05, 0)); c.position.set(x, y, 0); return c; };
    [[-0.14, 0], [0, 0], [0.14, 0], [-0.07, 0.105], [0.07, 0.105], [0, 0.21]].forEach(([x, y]) => cups.add(cup(x, y)));
    g.userData.update = t => st.userData.update(t);
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- one steaming cup of herbal tea (pivot at its foot): a big white mug, pale green tea, a
  // tea-bag tag hanging out, inked steam rising
  mtCup(o) {
    const g = grp(at(cyl(0.075, 0.065, 0.13, '#F4F0E6', 12, { pivot: 'bottom', outline: 0.05, emissive: '#3A3A40' }), 0, 0, 0));
    g.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.035, 0.012, 5, 10), mat('#F4F0E6')), 0.085, 0.07, 0), at(cyl(0.066, 0.066, 0.004, '#B8C86A', 12, { noGrain: true, emissive: '#3A4A1A' }), 0, 0.12, 0));
    g.add(at(box(0.004, 0.08, 0.004, '#E8E2D2'), -0.05, 0.12, 0.05), at(box(0.03, 0.035, 0.004, '#E8C24A', { outline: 0.08 }), -0.05, 0.075, 0.075));
    const st = steamPuffs({ r: 0.028, h: 0.26 }); st.position.y = 0.14; g.add(st);
    g.userData.update = t => st.userData.update(t); g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a rope lead (pivot at the world origin: all points are world points): from the hand end
  // o.a [[t, [x, y, z]]] through the collars o.chain [[x, y, z], ...] (or keyed: o.chainK [[[t, p], ...], ...]), sagging between them; tan, inked
  mtRope(o) {
    const g = grp(), M = mat('#B88A4E', { noGrain: true }); let tube = null, lastKey = '';
    g.userData.update = t => {
      const a = keyAt(o.a, t, [0, 1, 0]), ch = o.chainK ? o.chainK.map(K => keyAt(K, t, [0, 0.6, 0])) : (o.chain || []);
      const pts = [a, ...ch], P_ = [];
      for (let i = 0; i < pts.length; i++) { P_.push(new THREE.Vector3(...pts[i])); if (i < pts.length - 1) { const m = pts[i].map((v, j) => (v + pts[i + 1][j]) / 2); const d = Math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][2] - pts[i][2]); m[1] -= (o.sag ?? 0.12) * Math.min(1.5, d); P_.push(new THREE.Vector3(...m)); } }
      const key = P_.map(v => v.toArray().map(x => x.toFixed(3)).join(',')).join(';'); if (key === lastKey) return; lastKey = key;
      if (tube) { g.remove(tube); tube.geometry.dispose(); }
      const cur = new THREE.CatmullRomCurve3(P_); tube = new THREE.Mesh(new THREE.TubeGeometry(cur, 12 * P_.length, o.r ?? 0.022, 5), M); tube.castShadow = true;
      const olg = new THREE.Mesh(new THREE.TubeGeometry(cur, 12 * P_.length, (o.r ?? 0.022) * 1.6, 5), inkMat); tube.add(olg); g.add(tube);
    };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the shepherd's wool cape (attach to the torso joint, its origin at the waist, shoulders
  // ~0.6 up, +Z his front): a brown mantle over the shoulders and a long cape down his back to the knees
  mtCape(o) {
    const C = o.color || '#7A5636', g = grp();
    g.add(at(box(0.78, 0.26, 0.5, C, { outline: 0.012, taper: { x: 0.8, z: 0.9 } }), 0, 0.56, -0.02));
    const cape = box(0.92, 1.25, 0.07, C, { outline: 0.012 }); cape.position.set(0, 0.05, -0.25); cape.rotation.x = 0.1; g.add(cape);
    for (const sx of [-1, 1]) g.add(at(box(0.1, 0.9, 0.36, C, { outline: 0.012 }), sx * 0.42, 0.2, -0.08, 0, 0, sx * 0.08));
    g.add(at(box(0.18, 0.06, 0.04, '#C9A24A', { outline: 0.03 }), 0, 0.62, 0.24));
    return g;
  },
  // ---------------------------------------------------------------- a wide felt hat (attach to the head joint with offset [0, 0.5, 0]: sits on the hair)
  mtFeltHat(o) {
    const C = o.color || '#4A3A2E', g = grp(at(cyl(0.36, 0.36, 0.03, C, 14, { outline: 0.02 }), 0, 0.06, 0), at(cyl(0.16, 0.18, 0.18, C, 12, { pivot: 'bottom', outline: 0.02 }), 0, 0.07, 0), at(cyl(0.185, 0.185, 0.04, '#2A201A', 12), 0, 0.1, 0));
    return g;
  },
  // ---------------------------------------------------------------- a shepherd's crook (pivot at its foot): a long wooden staff with a hook at the top
  mtCrook(o) {
    const Lc = o.len ?? 1.75, C = o.color || '#8A6034', g = grp(at(cyl(0.022, 0.026, Lc, C, 6, { pivot: 'bottom', outline: 0.04 }), 0, 0, 0));
    const hook = new THREE.Mesh(new THREE.TorusGeometry(0.1, 0.022, 5, 12, PI * 1.25), mat(C)); hook.position.set(0.1, Lc, 0); hook.rotation.z = -PI * 0.12; ink(hook, 0.08); g.add(hook);
    return g;
  },
  // ---------------------------------------------------------------- an accountant's green eyeshade (attach to the head joint: the head 0.24 x 0.5 x 0.17,
  // the eyes at 0.28-0.37 up): a band round the forehead and a green visor above the eyes
  mtEyeshade(o) {
    const C = o.color || '#2E9A5A', Y = o.y ?? 0.49, g = grp();
    g.add(at(box(0.27, 0.035, 0.02, '#1E5E3A', { outline: 0.02 }), 0, Y, 0.096), at(box(0.02, 0.035, 0.2, '#1E5E3A'), 0.132, Y, 0.0), at(box(0.02, 0.035, 0.2, '#1E5E3A'), -0.132, Y, 0.0));
    const v = box(0.3, 0.012, 0.13, C, { outline: 0.02, emissive: '#0E3A1E' }); v.position.set(0, Y + 0.01, 0.15); v.rotation.x = 0.12; g.add(v);
    return g;
  },
  // ---------------------------------------------------------------- a black sleeve protector (attach to an elbow joint): a satin tube down the forearm
  mtSleeve(o) { const Lf = o.len ?? 0.22, g = grp(at(cyl(o.r ?? 0.075, (o.r ?? 0.075) * 0.9, Lf, '#1E2028', 8, { outline: 0.02 }), 0, -(o.y ?? 0.13), 0)); return g; },
  // ---------------------------------------------------------------- a thick ledger lying open (pivot at the middle of its spine, the spine along Z, the pages
  // on +-X, the top +Y): dark green boards, a thick block of ruled pages (lines and columns, no figures); o.flip [t0, n, dt]: n leaves turn BACKWARDS, from
  // the left half over to the right one, each in 0.14 s, fanning; o.w, o.d
  mtLedger(o) {
    const Wp = o.w ?? 0.36, Dp = o.d ?? 0.5, g = grp();
    const ruled = (back) => { const cv = canvas(256, Math.round(256 * Dp / Wp)), c = cv.getContext('2d'); c.fillStyle = '#F6F0DC'; c.fillRect(0, 0, cv.width, cv.height);
      c.strokeStyle = '#8FB0C8'; c.lineWidth = 2; for (let y = 24; y < cv.height; y += 16) { c.beginPath(); c.moveTo(10, y); c.lineTo(cv.width - 10, y); c.stroke(); }
      c.strokeStyle = '#D07070'; c.lineWidth = 2.5; for (const x of back ? [60, 180] : [76, 196]) { c.beginPath(); c.moveTo(x, 10); c.lineTo(x, cv.height - 10); c.stroke(); } return texOf(cv); };
    const tA = ruled(false), tB = ruled(true);
    for (const sx of [-1, 1]) { g.add(at(box(Wp + 0.03, 0.025, Dp + 0.04, '#24523A', { outline: 0.01 }), sx * (Wp / 2 + 0.01), 0.012, 0));
      g.add(at(box(Wp, 0.07, Dp, '#EDE5CC', { outline: 0.006 }), sx * Wp / 2, 0.06, 0));
      const pg = new THREE.Mesh(new THREE.PlaneGeometry(Wp - 0.01, Dp - 0.01), new THREE.MeshLambertMaterial({ map: sx < 0 ? tA : tB, ...OFF })); pg.rotation.x = -PI / 2; pg.position.set(sx * Wp / 2, 0.0955, 0); g.add(pg); }
    const leaves = [], F = o.flip || [0, 0, 0.1];
    for (let i = 0; i < (F[1] || 0); i++) { const piv = grp(); piv.position.y = 0.1 + 0.002 * i; g.add(piv);
      const lf = new THREE.Mesh(new THREE.PlaneGeometry(Wp - 0.01, Dp - 0.01), new THREE.MeshLambertMaterial({ map: tA, side: THREE.DoubleSide })); lf.rotation.x = -PI / 2; lf.position.x = -(Wp - 0.01) / 2; piv.add(lf);
      const ed = at(box(Wp - 0.01, 0.004, 0.004, '#B9AE92'), -(Wp - 0.01) / 2, 0, (Dp - 0.01) / 2); piv.add(ed); leaves.push({ piv, ts: F[0] + i * (F[2] ?? 0.1) }); }
    g.userData.update = t => { for (const { piv, ts } of leaves) { const u = clamp01((t - ts) / 0.14); piv.rotation.z = -PI * (u < 1 ? u * u * (3 - 2 * u) : 1) * 0.985; piv.visible = true; } };
    g.userData.update(0); return g;
  },
  // ---------------------------------------------------------------- a desk lamp (pivot at its base): a dark base, an arm, a green shade with a warm glow and a
  // real light under it (o.power)
  mtDeskLamp(o) {
    const g = grp(at(cyl(0.11, 0.13, 0.04, '#2A2C31', 10, { pivot: 'bottom', outline: 0.02 }), 0, 0, 0), at(cyl(0.015, 0.015, 0.42, '#3A3D44', 6, { pivot: 'bottom' }), 0, 0.04, 0));
    const sh = grp(); sh.position.set(0, 0.46, 0.05); sh.rotation.x = 0.5; g.add(sh);
    sh.add(at(new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.16, 0.14, 12, 1, true), mat('#2E7A4A', { doubleSide: true, outline: 0.02 })), 0, 0, 0), at(sphere(0.045, '#FFF2C0', 1, { emissive: '#FFE08A', noGrain: true }), 0, -0.04, 0));
    const lt = new THREE.PointLight('#FFD8A0', o.power ?? 1.6, 2.6, 1.3); lt.position.set(0, -0.12, 0); lt.castShadow = false; sh.add(lt);
    return g;
  },
  // ---------------------------------------------------------------- a small TV studio (pivot at the floor, faces +Z): a plain news desk and a blue backdrop with
  // a big plain white sheep shape (o.sheepX: where across, 0..1; o.sheepR its size, 0.17 of the height); no logo, no text, no figures on any screen
  mtStudio(o) {
    const g = grp(), BW = o.bw ?? 5.5, BH = o.bh ?? 3.6;
    const cv = canvas(512, Math.round(512 * BH / BW)), c = cv.getContext('2d'), w = cv.width, h = cv.height;
    const gr = c.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#2C5DB0'); gr.addColorStop(1, '#1E3F86'); c.fillStyle = gr; c.fillRect(0, 0, w, h);
    c.fillStyle = 'rgba(255,255,255,0.06)'; for (let i = 0; i < 8; i++) c.fillRect(i * w / 8, 0, w / 16, h);
    // the sheep shape: a fluffy cloud body, a head, four legs, all plain white
    const sx = w * (o.sheepX ?? 0.5), sy = h * 0.42, R = h * (o.sheepR ?? 0.17); c.fillStyle = '#FFFFFF';
    for (let i = 0; i < 9; i++) { const a = i / 9 * TAU; c.beginPath(); c.arc(sx + Math.cos(a) * R * 1.25, sy + Math.sin(a) * R * 0.75, R * 0.5, 0, TAU); c.fill(); }
    c.beginPath(); c.ellipse(sx, sy, R * 1.3, R * 0.85, 0, 0, TAU); c.fill();
    c.beginPath(); c.ellipse(sx + R * 1.55, sy - R * 0.35, R * 0.38, R * 0.5, 0.4, 0, TAU); c.fill();
    for (const dx of [-0.8, -0.35, 0.35, 0.8]) c.fillRect(sx + dx * R - R * 0.1, sy + R * 0.6, R * 0.2, R * 0.75);
    // (round 1) an ear and an eye on the head, so the shape reads as a sheep and not as a cloud
    c.beginPath(); c.ellipse(sx + R * 1.3, sy - R * 0.78, R * 0.22, R * 0.1, -0.5, 0, TAU); c.fill(); c.fillStyle = '#1E3F86'; c.beginPath(); c.arc(sx + R * 1.68, sy - R * 0.45, R * 0.07, 0, TAU); c.fill();
    const bd = new THREE.Mesh(new THREE.PlaneGeometry(BW, BH), new THREE.MeshLambertMaterial({ map: texOf(cv), emissive: '#FFFFFF', emissiveMap: texOf(cv), emissiveIntensity: 0.45 })); bd.position.set(0, BH / 2 + 0.2, -1.6); g.add(bd);
    g.add(at(box(BW + 0.2, BH + 0.2, 0.08, '#1A2238', { outline: 0.004 }), 0, BH / 2 + 0.2, -1.66));
    // the desk: a curved front of three panels, a light top
    const D = grp(); D.position.set(0, 0, 0); g.add(D);
    [[-0.85, 0.35], [0, 0], [0.85, -0.35]].forEach(([x, ry]) => D.add(at(box(0.9, 0.8, 0.08, '#D8DEE8', { pivot: 'bottom', outline: 0.008, emissive: '#2A3040' }), x, 0, 0.3 - Math.abs(x) * 0.18, 0, ry, 0)));
    D.add(at(box(2.8, 0.06, 0.8, '#F2F4F8', { outline: 0.008 }), 0, 0.82, 0.0), at(box(2.4, 0.1, 0.04, '#3A6AC0', { emissive: '#1A3A80', noGrain: true }), 0, 0.55, 0.34));
    return g;
  },
  // ---------------------------------------------------------------- a red bow tie (attach to the torso joint: its origin at the waist, the collar ~0.62 up)
  mtBowTie(o) { const C = o.color || '#C8282E', g = grp(); for (const sx of [-1, 1]) g.add(at(box(0.11, 0.08, 0.03, C, { taper: { x: 1, z: 1 }, outline: 0.04 }), sx * 0.06, 0, 0, 0, 0, sx * 0.25)); g.add(at(box(0.04, 0.05, 0.04, C, { outline: 0.04 }), 0, 0, 0.005)); return g; },
  // ---------------------------------------------------------------- a yellow pencil (attach to a hand with rot [PI, 0, 0]: it sticks out of the fist)
  mtPencil(o) { const g = grp(at(cyl(0.012, 0.012, 0.3, '#F2C230', 6, { pivot: 'bottom', outline: 0.05 }), 0, 0, 0), at(new THREE.Mesh(new THREE.ConeGeometry(0.012, 0.04, 6), mat('#E8C9A0')), 0, 0.32, 0), at(cyl(0.013, 0.013, 0.03, '#E87A8A', 6), 0, -0.01, 0)); return g; },
  // ---------------------------------------------------------------- a chunky wool jumper (attach to the torso joint, offset [0, -0.05, 0]): a knitted body with a
  // ribbed rollneck; o.color; o.pop t: it bursts off into nothing (swells, then gone in a puff of tufts of its colour) and the shirt under it shows;
  // o.shirt: a plain white shirt instead, o.appear t: hidden until then
  mtJumper(o) {
    const C = new THREE.Color(o.color || (o.shirt ? '#F4F4F0' : '#C8402E')), w = o.w ?? 0.6, h = o.h ?? 0.64, d = o.d ?? 0.42, g = grp(), k = grp(); g.add(k);
    let body;
    if (o.shirt) {
      // (round 1) o.shirt: a clean white shirt shell (the rig's white pyjama top showed broken wedges and flaps under a popped jumper): a plain body,
      // a pointed collar, a row of buttons; shown from o.appear
      body = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat(C.getStyle(), { noGrain: true, emissive: '#2A2C30' })); body.position.y = h / 2; ink(body, 0.012); body.castShadow = true; k.add(body);
      for (const sx of [-1, 1]) k.add(at(box(0.13, 0.09, 0.03, C.getStyle(), { outline: 0.04, noGrain: true, emissive: '#2A2C30' }), sx * 0.07, h - 0.04, d / 2 + 0.01, 0, 0, sx * 0.7));
      for (let i = 0; i < 3; i++) k.add(at(sphere(0.012, '#B8BCC6', 0, { noGrain: true }), 0, h - 0.17 - i * 0.14, d / 2 + 0.01));
    } else {
      const cv = canvas(128, 128), c = cv.getContext('2d'); c.fillStyle = C.getStyle(); c.fillRect(0, 0, 128, 128); c.strokeStyle = 'rgba(0,0,0,0.2)'; c.lineWidth = 3;
      for (let x = 0; x < 8; x++) for (let y = 0; y < 10; y++) { const cx = (x + 0.5) * 16, cy = (y + 0.5) * 12.8; c.beginPath(); c.moveTo(cx - 5, cy - 4); c.lineTo(cx, cy + 4); c.lineTo(cx + 5, cy - 4); c.stroke(); }
      c.fillStyle = C.clone().multiplyScalar(0.8).getStyle(); c.fillRect(0, 112, 128, 16);
      const kt = texOf(cv);
      body = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), new THREE.MeshLambertMaterial({ map: kt })); body.position.y = h / 2; ink(body, 0.012); body.castShadow = true; k.add(body);
      k.add(at(cyl(0.15, 0.16, 0.12, C.clone().multiplyScalar(0.85).getStyle(), 10, { outline: 0.03 }), 0, h + 0.02, 0.0));
    }
    // the pop's puffs: of its colour by default; o.puffColor, o.puffDz (0.1 sends them out to the sides, off the chest)
    const puff = puffBurst({ r: 0.1, color: o.puffColor || C.getStyle(), spread: o.puffSpread ?? 0.45, n: o.puffN ?? 8, dz: o.puffDz ?? 0.7, up: o.puffUp ?? 0.35 }); puff.position.y = h * 0.6; g.add(puff);
    g.userData.update = t => { let s = 1; if (o.pop != null) { const v = t - o.pop; if (v >= 0) s = v < 0.05 ? 1 + 0.22 * v / 0.05 : Math.max(0, 1.22 * (1 - (v - 0.05) / 0.06)); }
      if (o.appear != null) s *= popK(o.appear, t, 0.08);
      k.scale.setScalar(Math.max(0.0001, s)); k.visible = s > 0.001; puff.userData.burst(t, o.pop != null ? o.pop + 0.04 : null); };
    g.userData.update(0); return g;
  },
  // ---------------------------------------------------------------- a knitted sleeve (attach to a shoulder or an elbow joint: a tube down the limb, -Y); o.pop;
  // o.appear t: hidden until then (a shirt sleeve under a popped one)
  mtKnitSleeve(o) {
    const C = o.color || '#C8402E', Lk = o.len ?? 0.28, g = grp(), k = grp(at(cyl(o.r ?? 0.085, (o.r ?? 0.085) * 0.9, Lk, C, 8, { outline: 0.02 }), 0, -(o.y ?? Lk / 2), 0)); g.add(k);
    g.userData.update = t => { let s = 1; if (o.pop != null) { const v = t - o.pop; if (v >= 0) s = v < 0.05 ? 1 + 0.2 * v / 0.05 : Math.max(0, 1.2 * (1 - (v - 0.05) / 0.06)); }
      if (o.appear != null) s *= popK(o.appear, t, 0.08);
      k.scale.setScalar(Math.max(0.0001, s)); k.visible = s > 0.001; };
    g.userData.update(0); return g;
  },
  // ---------------------------------------------------------------- a lit window by night with one big silhouette in it (pivot at the window's middle, faces
  // +Z): a warm glowing pane, a frame, a sill; a dark head-and-shoulders figure with white eyes; o.nods [t...] it nods (counting); o.frown [[t, 0..1]]
  // its eyelids slant; o.look [[t, -1..1]] its pupils go sideways; o.lean [[t, x]] it shifts in the frame; o.w, o.h
  mtNightWindow(o) {
    const Wn = o.w ?? 1.5, Hn = o.h ?? 1.5, g = grp();
    g.add(at(box(Wn, Hn, 0.03, '#FFD98A', { emissive: '#E0A040', noGrain: true }), 0, 0, -0.02));
    for (const [dx, dy, bw, bh] of [[0, Hn / 2, Wn + 0.14, 0.1], [0, -Hn / 2, Wn + 0.24, 0.12], [-Wn / 2, 0, 0.1, Hn], [Wn / 2, 0, 0.1, Hn]]) g.add(at(box(bw, bh, 0.1, '#E8E2D2', { outline: 0.01 }), dx, dy, 0.02));
    const fig = grp(); fig.position.set(0, -Hn / 2, 0.0); g.add(fig); const SH = '#2A2440';
    const sil = (m) => { m.material = new THREE.MeshBasicMaterial({ color: SH }); return m; };
    fig.add(sil(at(box(Wn * 0.62, Hn * 0.3, 0.04, SH), 0, Hn * 0.15, 0)));
    const head = grp(); head.position.set(0, Hn * 0.3, 0); fig.add(head);
    head.add(sil(at(box(Wn * 0.32, Hn * 0.4, 0.04, SH), 0, Hn * 0.22, 0)), sil(at(box(Wn * 0.34, Hn * 0.06, 0.04, SH), 0, Hn * 0.43, 0)));
    const eyes = [-1, 1].map(sx => { const e = grp(); e.position.set(sx * Wn * 0.075, Hn * 0.26, 0.03); head.add(e);
      const wht = new THREE.Mesh(new THREE.CircleGeometry(Wn * 0.05, 16), new THREE.MeshBasicMaterial({ color: '#FFFFFF' })); wht.scale.y = 1.25; e.add(wht);
      const pu = new THREE.Mesh(new THREE.CircleGeometry(Wn * 0.022, 12), new THREE.MeshBasicMaterial({ color: '#111111' })); pu.position.z = 0.002; e.add(pu);
      const lid = new THREE.Mesh(new THREE.PlaneGeometry(Wn * 0.13, Wn * 0.08), new THREE.MeshBasicMaterial({ color: SH })); lid.position.set(0, Wn * 0.08, 0.004); e.add(lid);
      return { e, pu, lid, sx }; });
    g.userData.update = t => { let nd = 0; for (const n of o.nods || []) { const u = (t - n) / 0.24; if (u >= 0 && u < 1) nd = Math.max(nd, Math.sin(u * PI)); }
      head.position.y = Hn * 0.3 - Hn * 0.07 * nd; head.rotation.x = 0.3 * nd; fig.position.x = keyAt(o.lean, t, 0);
      const fr = keyAt(o.frown, t, 0), lk = keyAt(o.look, t, 0);
      for (const { pu, lid, sx } of eyes) { pu.position.x = lk * Wn * 0.025; lid.position.y = Wn * (0.085 - 0.04 * fr); lid.rotation.z = -sx * 0.5 * fr; }
      fig.scale.y = 1 + 0.01 * Math.sin(t * 2.5 + (o.ph ?? 0)); };
    g.userData.update(0); return g;
  },
  // ---------------------------------------------------------------- a street of houses by night (pivot at the floor, the fronts face +Z along X): o.n houses
  // of two storeys, every window lit warm; roofs; o.rows rows 14 m apart; o.bare [[row, i], ...]: houses left without windows (a scene puts its own)
  mtNightRow(o) {
    const g = grp(), n = o.n ?? 8, pitch = o.pitch ?? 7, rows = o.rows ?? 2;
    const WC = ['#4A5578', '#55607E', '#4C5A72', '#5A5674'], RC = ['#2E3450', '#3A2E40', '#2A3A4A'];
    const winGeo = new THREE.PlaneGeometry(0.8, 0.95), winM = new THREE.MeshBasicMaterial({ color: '#FFD27A', ...OFF }), wins = [];
    for (let r = 0; r < rows; r++) for (let i = 0; i < n; i++) { const x = (i - (n - 1) / 2) * pitch + (r % 2) * pitch * 0.4, z = -r * 14, hh = 5.6 + (i % 3) * 0.6;
      g.add(at(box(pitch - 0.6, hh, 6, WC[(i + r) % 4], { pivot: 'bottom', outline: 0.004 }), x, 0, z - 3));
      const rf = box(pitch - 0.2, 1.6, 6.6, RC[(i + r) % 3], { pivot: 'bottom', taper: { x: 0.05, z: 1 }, outline: 0.004 }); rf.position.set(x, hh, z - 3); g.add(rf);
      if (!(o.bare || []).some(([br, bi]) => br === r && bi === i)) for (let f = 0; f < 2; f++) for (let c = 0; c < 3; c++) wins.push([x + (c - 1) * 1.8, 1.4 + f * 2.4, z + 0.04]); }
    const M = new THREE.InstancedMesh(winGeo, winM, wins.length), ob = new THREE.Object3D();
    wins.forEach((p, i) => { ob.position.set(...p); ob.updateMatrix(); M.setMatrixAt(i, ob.matrix); }); M.castShadow = false; g.add(M);
    return g;
  },
  // ---------------------------------------------------------------- a big moon (pivot at its middle, faces +Z, unlit): a pale disc with soft craters and a halo
  mtMoon(o) {
    const R = o.r ?? 3, cv = canvas(256, 256), c = cv.getContext('2d');
    const gr = c.createRadialGradient(128, 128, 60, 128, 128, 128); gr.addColorStop(0, 'rgba(255,248,220,0.55)'); gr.addColorStop(0.75, 'rgba(255,248,220,0.12)'); gr.addColorStop(1, 'rgba(255,248,220,0)'); c.fillStyle = gr; c.fillRect(0, 0, 256, 256);
    c.fillStyle = '#FBF5DC'; c.beginPath(); c.arc(128, 128, 70, 0, TAU); c.fill(); c.fillStyle = '#E8DFB8';
    [[100, 110, 14], [150, 95, 9], [140, 150, 18], [105, 160, 8]].forEach(([x, y, r]) => { c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill(); });
    const m = new THREE.Mesh(new THREE.PlaneGeometry(R * 3.65, R * 3.65), new THREE.MeshBasicMaterial({ map: texOf(cv), transparent: true, depthWrite: false, toneMapped: false, fog: false })); m.renderOrder = -1;
    return grp(m);
  },
  // ---------------------------------------------------------------- a milk pail (pivot at its foot): a metal bucket with a handle, white milk inside (the
  // spill is mtMilk)
  mtPail(o) {
    const g = grp(at(cyl(0.16, 0.12, 0.3, '#BCC4CC', 12, { pivot: 'bottom', outline: 0.03 }), 0, 0, 0), at(cyl(0.15, 0.15, 0.01, '#FFFFFF', 12, { noGrain: true, emissive: '#8A8A8A' }), 0, 0.302, 0));
    const hd = new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.008, 4, 12, PI), mat('#5A6068')); hd.position.y = 0.3; g.add(hd);
    return g;
  },
  // ---------------------------------------------------------------- the milk spilled on the ground (pivot at the floor): a white puddle that spreads from o.at,
  // drops that fly out (polygon offset: no flicker on the grass); o.s its size (1), o.n the drops, o.up how high they fly
  mtMilk(o) {
    const g = grp(), S_ = o.s ?? 1, pud = new THREE.Mesh(new THREE.CircleGeometry(0.55 * S_, 20), new THREE.MeshLambertMaterial({ color: '#FFFFFF', emissive: '#9A9A9A', ...OFF })); pud.rotation.x = -PI / 2; pud.position.y = 0.02; g.add(pud);
    const burst = puffBurst({ r: 0.07 * S_, n: o.n ?? 8, spread: 0.6 * S_, up: o.up ?? 0.35 }); burst.position.y = 0.15; g.add(burst);
    g.userData.update = t => { const v = t - (o.at ?? 0); pud.visible = v > 0; pud.scale.set(Math.max(0.001, Math.min(1, v / 0.3)), Math.max(0.001, Math.min(1, v / 0.3)) * 0.7, 1); burst.userData.burst(t, o.at ?? 0); };
    g.userData.update(0); return g;
  },
  // ---------------------------------------------------------------- a burst of opaque inked puffs at o.at (white wool by default): o.r, o.color, o.n, o.spread
  mtPuff(o) { const g = grp(), b = puffBurst(o); g.add(b); g.userData.update = t => b.userData.burst(t, o.at ?? 0); g.userData.update(0); return g; },
  // ---------------------------------------------------------------- one fleece blob (pivot at its middle): o.s, o.seed; o.pop t / o.vanish t; o.toss: it is
  // tossed (handled by keys)
  mtBlob(o) { const g = grp(), m = blobMesh(o.s ?? 1, o.seed ?? 2); g.add(m); const b = puffBurst({ r: 0.15 * (o.s ?? 1), spread: 0.5 * (o.s ?? 1) }); g.add(b);
    g.userData.update = t => { let s = popK(o.pop, t, 0.14); if (o.vanish != null) { const v = t - o.vanish; if (v >= 0) s = v < 0.05 ? 1.15 : Math.max(0, 1.15 * (1 - (v - 0.05) / 0.08)); } m.scale.setScalar(Math.max(0.0001, s * (o.s ?? 1))); m.visible = s > 0.001; b.userData.burst(t, o.vanish != null ? o.vanish + 0.04 : null); };
    g.userData.update(0); return g; },
  // ---------------------------------------------------------------- (round 1) a pale moonlit patch on the ground (pivot at the floor, flat): a soft round
  // glow fading to nothing at its edge, so a dark sheep on a night meadow has a lighter ground behind it; o.r (1.6), o.color, o.a (its opacity at the
  // middle, 0.55); polygon offset, never flickers
  mtGlowPatch(o) {
    const cv = canvas(128, 128), c = cv.getContext('2d'), gr = c.createRadialGradient(64, 64, 4, 64, 64, 64), col = new THREE.Color(o.color || '#7FA6C8'), rgb = `${Math.round(col.r * 255)},${Math.round(col.g * 255)},${Math.round(col.b * 255)}`;
    gr.addColorStop(0, `rgba(${rgb},${o.a ?? 0.55})`); gr.addColorStop(0.55, `rgba(${rgb},${(o.a ?? 0.55) * 0.6})`); gr.addColorStop(1, `rgba(${rgb},0)`); c.fillStyle = gr; c.fillRect(0, 0, 128, 128);
    const m = new THREE.Mesh(new THREE.CircleGeometry(o.r ?? 1.6, 32), new THREE.MeshBasicMaterial({ map: texOf(cv), transparent: true, depthWrite: false, toneMapped: false, ...OFF }));
    m.rotation.x = -PI / 2; m.position.y = 0.03; m.renderOrder = 1; return grp(m);
  },
  // ---------------------------------------------------------------- (round 1) the outside of a block of flats cut open, by night (pivot at the floor in the
  // middle of the cut, faces +Z): two facade strips either side of the cut (o.cw wide, 3.6) with warm lit windows, a cornice, a pitched roof with a
  // chimney over the whole width (o.h tall, 8.8), a deep blue night sky plane with stars behind (o.sky), a dark pavement in front. No lettering
  mtBlockNight(o) {
    const CW = o.cw ?? 3.6, H = o.h ?? 8.8, SW = o.sw ?? 1.5, FC = o.facade || '#7A84A8', g = grp(), WIN = '#FFD27A';
    for (const sx of [-1, 1]) { const x = sx * (CW / 2 + SW / 2);
      g.add(at(box(SW, H, 2.4, FC, { pivot: 'bottom', outline: 0.006 }), x, 0, -0.1));
      for (let f = 0; f < 3; f++) { const y = 1.1 + f * 2.85; g.add(at(box(0.62, 0.85, 0.04, WIN, { emissive: '#E0A040', noGrain: true }), x + sx * 0.05, y + 0.45, 1.12), at(box(0.74, 0.08, 0.1, '#E8E2D2', { outline: 0.02 }), x + sx * 0.05, y, 1.14)); } }
    const TW = CW + 2 * SW + 0.3;
    g.add(at(box(TW, 0.22, 2.7, '#9AA2C4', { outline: 0.006 }), 0, H + 0.11, -0.1));
    const roof = box(TW + 0.2, 1.7, 2.9, '#6A5A7E', { pivot: 'bottom', taper: { x: 1, z: 0.06 }, outline: 0.006 }); roof.position.set(0, H + 0.22, -0.1); g.add(roof);
    g.add(at(box(0.5, 1.2, 0.5, '#5A5470', { pivot: 'bottom', outline: 0.01 }), TW * 0.3, H + 0.9, -0.3));
    g.add(at(box(TW + 6, 0.1, 3.2, '#3A4060', { outline: 0.004 }), 0, -0.05, 1.3));
    const cv = canvas(128, 256), c = cv.getContext('2d'), gr = c.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, '#0E1A44'); gr.addColorStop(1, '#2A3C70'); c.fillStyle = gr; c.fillRect(0, 0, 128, 256);
    c.fillStyle = '#FFF6D8'; for (let i = 0; i < 40; i++) c.fillRect(128 * hsh(i + 1), 200 * hsh(i + 9), 1.6, 1.6);
    const sky = new THREE.Mesh(new THREE.PlaneGeometry(o.skyW ?? 40, o.skyH ?? 40), new THREE.MeshBasicMaterial({ map: texOf(cv), toneMapped: false, fog: false })); sky.position.set(0, (o.skyH ?? 40) / 2 - 8, o.skyZ ?? -12); g.add(sky);
    return g;
  },
};
