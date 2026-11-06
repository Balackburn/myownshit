// Procedural low-poly creatures in the "paper" style: boxy / faceted bodies, big
// googly eyes (white discs, ink rim, black dot pupils), thick floating ink brows.
// Every creature is a rigid puppet: pivot Groups (joints) + boxes / facet blobs.
//
//   buildCreature(name, opts) -> THREE.Group
//     root            : positioned / rotated by the director (never touched here)
//       scaler        : opts.scale × grow factor
//         mover       : clip root offsets (bob, hop, lean, lie down ...)
//           joints... : userData.joints (biped joints share the human rig names,
//                       so every human clip in animations.js also works on bipeds)
//
// Units: metres, faces +Z, character's left = +X. All motion = pure f(t, params).
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, sphere, rng, ease, clamp01, lerp } from './style.js';
import { CLIPS as HCLIPS } from './animations.js';

const S = Math.sin, C = Math.cos, PI = Math.PI, abs = Math.abs, max = Math.max, min = Math.min;
const INK = P.ink, EYE_WHITE = '#F8F5EC', PUPIL = '#0B0C0F';

export const CREATURE_NAMES = [
  'pigeon', 'seagull', 'chicken', 'duck', 'ant', 'bee', 'spider', 'snail',
  'lion', 'zebra', 'giraffe', 'elephant', 'hippo', 'crocodile', 'monkey', 'gorilla',
  'bear', 'dog', 'cat', 'rat', 'cow', 'pig', 'sheep', 'horse', 'goat', 'rabbit',
  'frog', 'shark', 'fish', 'octopus', 'penguin', 'owl', 'alien', 'robot', 'ghost',
  'snowman', 'banana-man', 'worm', 'avocat',
];
export const CREATURE_CLIPS = ['idle', 'walk', 'run', 'flee', 'fly', 'hop', 'peck', 'sit', 'talk', 'celebrate', 'sleep', 'angry', 'eat', 'grow', 'carry', 'point'];
export const CREATURE_EXPRESSIONS = ['neutral', 'angry', 'sad', 'surprised', 'shocked', 'smug', 'sleepy', 'happy', 'scared', 'suspicious', 'closed', 'blink', 'dead', 'talk'];
const NAME_ALIASES = { banana: 'banana-man', bananaman: 'banana-man', banana_man: 'banana-man', mouse: 'rat', kitten: 'cat', puppy: 'dog', gull: 'seagull', hen: 'chicken', rooster: 'chicken', ape: 'gorilla', donkey: 'horse', bull: 'cow', lamb: 'sheep', bunny: 'rabbit', toad: 'frog', squid: 'octopus', ufo: 'alien', android: 'robot' };

// ---------------------------------------------------------------- mesh kit --
const inkBack = new THREE.MeshBasicMaterial({ color: INK, side: THREE.BackSide });
const _v = new THREE.Vector3(), _c = new THREE.Vector3();
// Constant-thickness inverted-hull outline (works for off-centre / pivoted geometry).
function ink(mesh, t = 0.01) {
  const g = mesh.geometry; if (!g.boundingBox) g.computeBoundingBox();
  g.boundingBox.getSize(_v); g.boundingBox.getCenter(_c);
  const k = [1 + 2 * t / max(_v.x, 0.004), 1 + 2 * t / max(_v.y, 0.004), 1 + 2 * t / max(_v.z, 0.004)];
  const o = new THREE.Mesh(g, inkBack); o.name = 'outline'; o.castShadow = o.receiveShadow = false;
  o.scale.set(k[0], k[1], k[2]); o.position.set(_c.x * (1 - k[0]), _c.y * (1 - k[1]), _c.z * (1 - k[2]));
  mesh.add(o); return mesh;
}
// Faceted ellipsoid (jittered icosphere, shared vertices keep their offset -> no cracks).
function facetGeo(rx, ry, rz, detail = 1, jit = 0.08, seed = 5) {
  const g = new THREE.IcosahedronGeometry(1, detail), p = g.attributes.position, r = rng(seed), off = new Map();
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i), y = p.getY(i), z = p.getZ(i), k = `${Math.round(x * 999)},${Math.round(y * 999)},${Math.round(z * 999)}`;
    if (!off.has(k)) off.set(k, 1 + (r() - 0.5) * 2 * jit);
    const f = off.get(k); p.setXYZ(i, x * rx * f, y * ry * f, z * rz * f);
  }
  g.computeVertexNormals(); return g;
}
function facet(rx, ry, rz, color, o = {}) {
  const m = new THREE.Mesh(facetGeo(rx, ry, rz, o.detail ?? 1, o.jit ?? 0.07, o.seed ?? 5), mat(color, o));
  m.castShadow = m.receiveShadow = true; return m;
}
function cone(r, h, color, seg = 6, o = {}) { // points +Z when o.fwd, else +Y
  const g = new THREE.ConeGeometry(r, h, seg);
  if (o.pivot === 'bottom') g.translate(0, h / 2, 0);
  if (o.fwd) g.rotateX(PI / 2);
  const m = new THREE.Mesh(g, mat(color, o)); m.castShadow = m.receiveShadow = true; return m;
}
function tri(a, b, c, color) { // flat decal triangle (lapels, shirt V)
  const g = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(...a), new THREE.Vector3(...b), new THREE.Vector3(...c)]);
  g.computeVertexNormals(); return new THREE.Mesh(g, mat(color, { doubleSide: true }));
}
// segment box along +Z (legs of bugs, tentacles, tails)
function zbox(w, h, len, color, taper = 1) {
  const m = box(w, h, len, color, taper !== 1 ? { taper, taperAxis: 'z' } : {});
  m.geometry.translate(0, 0, len / 2); m.geometry.computeBoundingBox(); return m;
}
const flipZ = m => { m.geometry.rotateY(PI); m.geometry.computeBoundingBox(); return m; }; // +Z segment -> -Z

// ----------------------------------------------------------------- rig kit --
function makeRig(name, o) {
  const root = new THREE.Group(); root.name = 'creature:' + name;
  const scaler = new THREE.Group(), mover = new THREE.Group(); scaler.name = 'scaler'; mover.name = 'mover';
  root.add(scaler); scaler.add(mover);
  const R = { name, opts: o, root, scaler, mover, J: {}, eyes: [], ol: 0.01, seed: o.seed ?? 1, plan: 'blob' };
  R.joint = (n, parent, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0) => {
    const g = new THREE.Group(); g.name = n; g.position.set(x, y, z); g.rotation.set(rx, ry, rz); parent.add(g); R.J[n] = g; return g;
  };
  // add mesh: a(parent, mesh, [x,y,z], [rx,ry,rz], outline(true|false|thickness))
  R.a = (parent, mesh, p, r, ol = true) => {
    if (p) mesh.position.set(p[0], p[1], p[2]); if (r) mesh.rotation.set(r[0], r[1], r[2]);
    parent.add(mesh); if (ol) ink(mesh, ol === true ? R.ol : ol); return mesh;
  };
  return R;
}

// Googly eyes + floating brows. o: {x, y, z, r, lid, flat, pupil, browY, browW, yaw, cross}
function addEyes(R, parent, o) {
  const r = o.r;
  for (const side of [1, -1]) {
    const g = new THREE.Group(); g.position.set(side * o.x, o.y, o.z); g.rotation.y = side * (o.yaw ?? 0.1); parent.add(g);
    const eye = new THREE.Mesh(new THREE.SphereGeometry(r, 18, 12), mat(EYE_WHITE, { noGrain: true }));
    eye.scale.z = o.flat ?? 0.72; g.add(eye);
    const rim = new THREE.Mesh(eye.geometry, inkBack); rim.scale.setScalar(1 + (o.rim ?? 0.13)); rim.name = 'outline'; eye.add(rim);
    const pupil = new THREE.Mesh(new THREE.SphereGeometry(r * (o.pupil ?? 0.44), 12, 8), mat(PUPIL, { noGrain: true }));
    const px = -side * r * (o.cross ?? 0.14), py = -r * 0.06, pz = r * 0.9;
    pupil.position.set(px, py, pz); eye.add(pupil);
    const lid = new THREE.Mesh(new THREE.SphereGeometry(r * 1.06, 18, 8, 0, PI * 2, 0, PI / 2), mat(o.lid ?? P.grey, { doubleSide: true }));
    lid.rotation.x = -PI / 2; eye.add(lid);
    // brow: low-poly arched torus segment
    const browG = new THREE.Group(); const by = o.y + r * (o.browY ?? 1.32);
    browG.position.set(side * o.x * (o.browX ?? 1), by, o.z + r * (o.browZ ?? 0.35)); parent.add(browG);
    const arc = 1.7, br = r * 0.82 * (o.browW ?? 1);
    const dark = new THREE.Color(o.lid ?? P.grey).getHSL({}).l < 0.2;
    const brow = new THREE.Mesh(new THREE.TorusGeometry(br, r * (o.browT ?? 0.17), 4, 7, arc), mat(o.browColor ?? (dark ? '#E9E1CC' : INK), { noGrain: true }));
    brow.rotation.z = PI / 2 - arc / 2; brow.position.y = -br; browG.add(brow);
    if (o.noBrow) browG.visible = false;
    R.eyes.push({ side, g, eye, pupil, lid, browG, by, r, px, py, pz });
  }
}

// --------------------------------------------------------------- expressions --
const EXPR = {
  neutral: { b: [0, 0] }, talk: { b: [0.05, 0.05] },
  angry: { b: [0.5, -0.3], lid: 0.3, pup: 0.85 },
  sad: { b: [-0.45, 0.12], lid: 0.32, pup: 1.1, look: [0, -0.35] },
  surprised: { b: [0, 0.45], pup: 0.62 }, shocked: { b: [-0.1, 0.62], pup: 0.45 },
  smug: { bL: [0.3, -0.12], bR: [-0.18, 0.35], lid: 0.44, look: [0.25, 0] },
  sleepy: { b: [-0.12, -0.14], lid: 0.64 },
  happy: { b: [-0.18, 0.28], lid: 0.12, pup: 1.1 },
  scared: { b: [-0.42, 0.42], pup: 0.5 },
  suspicious: { bL: [0.4, -0.18], bR: [0, 0.18], lidL: 0.5, lidR: 0.25, look: [0.35, 0] },
  disgusted: { bL: [0.35, -0.1], bR: [-0.1, 0.2], lid: 0.35 },
  closed: { b: [-0.05, -0.1], lid: 1 }, blink: { b: [0, 0], lid: 1 }, dead: { b: [0, 0], lid: 1 },
};
const lidRx = l => l < 0.5 ? -PI / 2 * (1 - 2 * l) : (l - 0.5) * 2 * 1.5;
function applyExpression(R, name, blink = 0, twitch = 0) {
  const e = EXPR[name] || EXPR.neutral;
  for (const E of R.eyes) {
    const L = E.side > 0, b = (L ? e.bL : e.bR) || e.b || [0, 0];
    E.browG.rotation.z = E.side * b[0];
    E.browG.position.y = E.by + (b[1] + twitch) * E.r;
    E.lid.rotation.x = lidRx(min(1, max((L ? e.lidL : e.lidR) ?? e.lid ?? 0, blink)));
    E.pupil.scale.setScalar(e.pup ?? 1);
    const lk = e.look || [0, 0];
    E.pupil.position.set(E.px + lk[0] * E.r * 0.4, E.py + lk[1] * E.r * 0.4, E.pz);
  }
}

// ------------------------------------------------------------- body builders --
function hand(R, parent, type, aw, color, sd) {
  switch (type) {
    case 'mitten': {
      R.a(parent, box(aw * 0.85, aw * 1.3, aw * 0.45, color, { pivot: 'top' }));
      const th = R.a(parent, box(aw * 0.3, aw * 0.6, aw * 0.35, color, { pivot: 'top' }), [sd * aw * 0.45, -aw * 0.1, aw * 0.1]); th.rotation.z = sd * 0.5; break;
    }
    case 'claw': {
      R.a(parent, box(aw * 0.9, aw * 1.6, aw * 0.9, color, { pivot: 'top', taper: 0.25 }));
      R.a(parent, box(aw * 0.5, aw * 1.0, aw * 0.5, color, { pivot: 'top', taper: 0.2 }), [sd * aw * 0.5, -aw * 0.1, 0], [0, 0, sd * 0.6]); break;
    }
    case 'glove': {
      R.a(parent, sphere(aw * 1.15, P.white, 1), [0, -aw * 1.0, 0]);
      R.a(parent, sphere(aw * 0.5, P.white, 0), [sd * aw * 0.95, -aw * 0.6, aw * 0.3]); break;
    }
    case 'clamp': {
      R.a(parent, box(aw * 1.2, aw * 0.5, aw * 1.2, color, { pivot: 'top' }));
      for (const s of [-1, 1]) R.a(parent, box(aw * 0.25, aw * 1.0, aw * 0.8, P.greyDark, { pivot: 'top' }), [s * aw * 0.42, -aw * 0.45, 0]); break;
    }
    case 'ball': R.a(parent, sphere(aw * 0.85, color, 1), [0, -aw * 0.6, 0]); break;
    case 'none': break;
    default: R.a(parent, box(aw * 1.3, aw * 1.15, aw * 1.3, color, { pivot: 'top' }), [0, aw * 0.1, 0.005]); // paw
  }
}

// Anthropomorphic biped. Joint names & conventions match human.js.
function bipedBody(R, o) {
  const c = o.colors;
  const th1 = o.leg ?? 0.45, lw = o.legW ?? 0.12, fh = o.footH ?? 0.07, fl = o.footLen ?? 0.2;
  const hipY = th1 * 2 + fh + 0.04;
  const hips = R.joint('hips', R.mover, 0, hipY, 0);
  const tw = o.tw ?? 0.42, th = o.th ?? 0.6, td = o.td ?? 0.3, tap = o.taper ?? 1.15;
  if (!o.noPelvis) R.a(hips, box(tw * 0.9, o.pelvisH ?? 0.16, td * 0.95, c.pelvis ?? c.leg, { pivot: 'top' }), [0, 0.03, 0]);
  const torso = R.joint('torso', hips, 0, 0, 0, o.lean ?? 0);
  if (!o.noTorso) R.a(torso, box(tw, th, td, c.body, { pivot: 'bottom', taper: { x: tap, z: o.taperZ ?? 1 } }));
  if (c.belly && !o.noTorso) R.a(torso, box(tw * 0.6, th * 0.72, 0.02, c.belly, { pivot: 'bottom', taper: { x: 1.15, z: 1 } }), [0, th * 0.06, td / 2 + 0.008], null, false);
  R.joint('neck', torso, 0, th, 0);
  const aw = o.armW ?? 0.1, au = o.armU ?? 0.32, af = o.armF ?? 0.3;
  const shX = o.shX ?? (tw * (1 + (tap - 1) * (o.shY ?? 0.9)) / 2 + aw * 0.45);
  for (const [s, sd] of [['L', 1], ['R', -1]]) {
    const sh = R.joint('shoulder' + s, torso, sd * shX, th * (o.shY ?? 0.9), 0);
    R.a(sh, box(aw, au + aw * 0.4, aw, c.arm, { pivot: 'top' }), [0, aw * 0.4, 0]);
    const el = R.joint('elbow' + s, sh, 0, -au, 0);
    R.a(el, box(aw * 0.9, af, aw * 0.9, c.arm, { pivot: 'top' }));
    if (o.dots) R.a(el, sphere(aw * 0.8, o.dots, 1), [0, 0, 0], null, R.ol * 0.6);
    const hd = R.joint('hand' + s, el, 0, -af, 0);
    hand(R, hd, o.hand ?? 'paw', aw, c.hand ?? c.arm, sd);
  }
  for (const [s, sd] of [['L', 1], ['R', -1]]) {
    const hp = R.joint('hip' + s, hips, sd * (o.hipX ?? tw * 0.24), -0.04, 0);
    R.a(hp, box(lw, th1 + 0.05, lw * 1.08, c.leg, { pivot: 'top' }), [0, 0.05, 0]);
    const kn = R.joint('knee' + s, hp, 0, -th1, 0);
    R.a(kn, box(lw * 0.92, th1, lw, c.shin ?? c.leg, { pivot: 'top' }));
    if (o.dots) R.a(kn, sphere(lw * 0.85, o.dots, 1), [0, 0, 0], null, R.ol * 0.6);
    const ft = R.joint('foot' + s, kn, 0, -th1, 0);
    R.a(ft, box(lw * (o.footW ?? 1.25), fh, fl, c.foot ?? c.leg, { pivot: 'top', taper: o.footTaper }), [0, 0, fl * 0.3]);
  }
  R.plan = 'biped'; R.legScale = th1 / 0.49;
  R.B = { tw, th, td, tap, aw, au, af, hipY, lw, th1 };
  R.chest = { parent: torso, pos: [0, th * 0.62, td / 2 + 0.01], s: tw / 0.42 };
  return R.B;
}

// Quadruped body: box torso, 4 two-segment legs, angled neck, tail anchor.
function quadBody(R, o) {
  const { L, W, H, legH } = o, lw = o.legW;
  const bodyY = legH + H / 2;
  const body = R.joint('body', R.mover, 0, bodyY, 0);
  R.a(body, o.bodyMesh ?? box(W, H, L, o.color, { taper: o.taper ?? { x: 0.92, z: 0.96 } }));
  if (o.belly) R.a(body, box(W * 0.72, 0.03, L * 0.7, o.belly), [0, -H / 2 - 0.004, 0], null, false);
  const lx = W / 2 - lw * 0.55, lz = L / 2 - lw * 0.75 - (o.legZ ?? 0.02), top = -H * 0.3, len = legH + H * 0.2;
  const lc = o.legColor ?? o.color;
  for (const [n, sx, sz] of [['FL', 1, 1], ['FR', -1, 1], ['BL', 1, -1], ['BR', -1, -1]]) {
    const splay = o.splay ?? 0;
    const up = R.joint('leg' + n, body, sx * (lx + (o.legOut ?? 0)), top, sz * lz, 0, 0, sx * splay);
    const ll = len / C(splay), u = ll * (o.upper ?? 0.5);
    R.a(up, box(lw, u + lw * 0.3, lw * 1.05, lc, { pivot: 'top' }), [0, lw * 0.3, 0]);
    const kn = R.joint('knee' + n, up, 0, -u, 0, 0, 0, -sx * splay);
    R.a(kn, box(lw * 0.86, ll - u, lw * 0.9, lc, { pivot: 'top' }));
    if (o.hoof) R.a(kn, box(lw * 0.98, legH * 0.1, lw * 1.04, o.hoof, { pivot: 'bottom' }), [0, -(ll - u), 0.004]);
    else R.a(kn, box(lw * 1.08, lw * 0.45, lw * 1.35, o.paw ?? lc, { pivot: 'bottom' }), [0, -(ll - u), lw * 0.2]);
  }
  const nk = o.neck || { len: 0.1, w: W * 0.5, d: H * 0.5, rx: 0.6 };
  const neck = R.joint('neck', body, 0, H * (nk.y ?? 0.2), L / 2 - nk.d * (nk.back ?? 0.45), nk.rx);
  if (nk.len > 0.02) R.a(neck, box(nk.w, nk.len + nk.d * 0.3, nk.d, nk.color ?? o.color, { pivot: 'bottom', taper: { x: 0.85, z: 0.85 } }), [0, -nk.d * 0.3, 0]);
  R.joint('neckTop', neck, 0, nk.len, 0, -nk.rx);
  R.joint('tailBase', body, 0, H * 0.3, -L / 2);
  R.plan = 'quad';
  R.Q = { L, W, H, legH, len, bodyY, lz, top, s: legH / 0.5 + 0.3 };
  R.chest = { parent: body, pos: [0, H * 0.18, L / 2 + 0.008], s: W / 0.5 };
  return body;
}

// Boxy mammal head with muzzle + hinged jaw, googly eyes and ears.
function mHead(R, parent, o) {
  const { w, h, d } = o, col = o.color;
  const head = R.joint('head', parent, 0, o.y ?? 0, o.z ?? 0, o.rx ?? 0);
  if (o.scale) head.scale.setScalar(o.scale);
  const hz = o.hz ?? 0;
  R.a(head, o.skull ?? box(w, h, d, col, { taper: o.taper ?? { x: 0.86, z: 0.9 } }), [0, h / 2, hz], null, o.skullOl ?? true);
  const front = hz + d / 2;
  if (o.snout) {
    const s = o.snout, inset = s.inset ?? 0.03;
    const muzzle = new THREE.Group(); muzzle.position.set(0, s.y ?? h * 0.24, front - inset); muzzle.rotation.x = s.rx ?? 0; head.add(muzzle);
    R.a(muzzle, box(s.w, s.h, s.d, s.color ?? col, { taper: s.taper ?? { x: 0.9, z: 0.85 }, taperAxis: 'z' }), [0, 0, s.d / 2]);
    if (o.nose !== null) R.a(muzzle, box(s.w * (o.noseW ?? 0.45), s.h * (o.noseH ?? 0.3), 0.035, o.nose ?? INK, { taper: { x: 0.7, z: 1 } }), [0, s.h * 0.24, s.d * 0.92], null, R.ol * 0.5);
    const jaw = R.joint('jaw', muzzle, 0, -s.h / 2, 0);
    R.a(jaw, box(s.w * 0.9, s.h * (s.jh ?? 0.4), s.d * 0.94, s.jawColor ?? s.color ?? col, { pivot: 'top', taper: { x: 0.9, z: 0.85 }, taperAxis: 'z' }), [0, 0, s.d * 0.47]);
    R.a(jaw, box(s.w * 0.74, 0.01, s.d * 0.8, P.redDark), [0, 0.004, s.d * 0.46], null, false);
    if (s.teeth) for (let i = 0; i < s.teeth; i++) {
      const tz = s.d * (0.25 + 0.7 * i / max(1, s.teeth - 1)) ;
      for (const sd of [1, -1]) R.a(muzzle, box(0.02 * s.w / 0.3, s.h * 0.18, 0.02 * s.w / 0.3, P.white, { taper: 0.2, pivot: 'top' }), [sd * s.w * 0.38, -s.h / 2 + 0.002, tz], [PI, 0, 0], false);
    }
    R.muzzle = muzzle; R.snoutTip = s.d;
  }
  const e = o.eye;
  addEyes(R, head, { x: e.x, y: e.y, z: front - (e.inset ?? 0.015) - (e.z ?? 0), r: e.r, lid: o.lid ?? col, ...e });
  if (o.ears) ears(R, head, o.ears, { w, h, d, hz, col });
  return head;
}
function ears(R, head, E, H) {
  const ec = E.color ?? H.col, inner = E.inner;
  for (const [s, sd] of [['L', 1], ['R', -1]]) {
    const ex = sd * (E.x ?? H.w * 0.4), ey = E.y ?? H.h * 0.95, ez = H.hz + (E.z ?? -H.d * 0.1);
    const j = R.joint('ear' + s, head, ex, ey, ez);
    const sz = E.size ?? 0.08;
    switch (E.type) {
      case 'round': {
        R.a(j, cyl(sz, sz, 0.035, ec, 8), [0, sz * 0.5, 0], [PI / 2, 0, 0]);
        if (inner) R.a(j, cyl(sz * 0.6, sz * 0.6, 0.01, inner, 8), [0, sz * 0.5, 0.02], [PI / 2, 0, 0], false); break;
      }
      case 'pointy': {
        R.a(j, box(sz, sz * 1.25, 0.04, ec, { pivot: 'bottom', taper: { x: 0.12, z: 0.5 } }), null, [0, 0, -sd * (E.tilt ?? 0.18)]);
        if (inner) R.a(j, box(sz * 0.55, sz * 0.8, 0.01, inner, { pivot: 'bottom', taper: { x: 0.12, z: 1 } }), [0, 0.005, 0.022], [0, 0, -sd * (E.tilt ?? 0.18)], false); break;
      }
      case 'floppy': R.a(j, box(0.04, sz * 1.6, sz, ec, { pivot: 'top', taper: { x: 1, z: 1.2 } }), [sd * 0.02, 0, 0], [0, 0, sd * (E.tilt ?? 0.2)]); break;
      case 'side': {
        R.a(j, box(sz * 1.4, sz * 0.55, 0.05, ec, { taper: { x: 1, z: 1 } }), [sd * sz * 0.6, 0, 0], [0, 0, -sd * (E.tilt ?? 0.3)]);
        if (inner) R.a(j, box(sz * 1.0, sz * 0.3, 0.01, inner), [sd * sz * 0.65, -0.004 * sd, 0.028], [0, 0, -sd * (E.tilt ?? 0.3)], false); break;
      }
      case 'long': {
        R.a(j, box(sz * 0.55, sz * 3, 0.04, ec, { pivot: 'bottom', taper: { x: 0.7, z: 1 } }), null, [0, 0, -sd * (E.tilt ?? 0.1)]);
        if (inner) R.a(j, box(sz * 0.3, sz * 2.4, 0.01, inner, { pivot: 'bottom' }), [0, sz * 0.2, 0.022], [0, 0, -sd * (E.tilt ?? 0.1)], false); break;
      }
    }
  }
}
// stripes: thin slabs slightly bigger than a w×h×d box, along axis
function stripes(R, parent, dims, at, axis, n, color, o = {}) {
  const [w, h, d] = dims, th = o.th ?? 0.035, from = o.from ?? 0.1, to = o.to ?? 0.9;
  for (let i = 0; i < n; i++) {
    const f = lerp(from, to, n === 1 ? 0.5 : i / (n - 1));
    let m, p = [...at];
    if (axis === 'z') { m = box(w * 1.04, h * 1.04, th, color); p[2] += (f - 0.5) * d; }
    else if (axis === 'y') { m = box(w * 1.04 * (o.tx ? lerp(1, o.tx, f) : 1), th, d * 1.04, color); p[1] += (f - 0.5) * h; }
    else { m = box(th, h * 1.04, d * 1.04, color); p[0] += (f - 0.5) * w; }
    R.a(parent, m, p, o.rot ? [0, 0, o.rot * (i % 2 ? 1 : -1)] : null, false);
  }
}
// thin decal patches on a box surface (giraffe/cow spots)
function patches(R, parent, n, color, region, seed) {
  const r = rng(seed);
  for (let i = 0; i < n; i++) {
    const s = region.s * (0.6 + r() * 0.6);
    const face = region.faces[i % region.faces.length];
    const u = (r() - 0.5) * 0.8, v = (r() - 0.5) * 0.8;
    let m, p;
    if (face === 'x+' || face === 'x-') { m = box(0.008, s * (0.8 + r() * 0.4), s, color); p = [(face === 'x+' ? 1 : -1) * (region.w / 2 + 0.003), region.y + v * region.h, region.z + u * region.d]; }
    else { m = box(s, 0.008, s * (0.8 + r() * 0.4), color); p = [u * region.w, region.y + region.h / 2 + 0.003, region.z + v * region.d]; }
    R.a(parent, m, p, [0, 0, 0], false);
  }
}
function tail(R, parent, o) { // simple 2-segment tail hanging along -Y, rest tilt rx (PI/2 = straight back)
  const j = R.joint('tail', parent, 0, o.y ?? 0, o.z ?? 0, o.rx ?? 0.6);
  const a = o.len * (o.split ?? 0.55);
  R.a(j, box(o.w, a, o.w, o.color, { pivot: 'top', taper: o.taper ?? 0.9 }));
  const j2 = R.joint('tail2', j, 0, -a, 0, o.rx2 ?? 0.3);
  R.a(j2, box(o.w * 0.85, o.len - a, o.w * 0.85, o.color, { pivot: 'top', taper: o.taper ?? 0.8 }));
  if (o.tuft) R.a(j2, facet(o.w * 1.6, o.w * 2.2, o.w * 1.6, o.tuft, { seed: 9, detail: 0 }), [0, -(o.len - a) - o.w, 0]);
  return j;
}
function tie(R, parent, pos, s = 1) {
  R.a(parent, box(0.11 * s, 0.06 * s, 0.012, P.shirt), [pos[0], pos[1] + 0.02 * s, pos[2]], null, false);
  R.a(parent, box(0.04 * s, 0.035 * s, 0.02, P.tieRed), [pos[0], pos[1], pos[2] + 0.01], null, false);
  const t = R.a(parent, box(0.045 * s, 0.24 * s, 0.014, P.tieRed, { taper: { x: 1.7, z: 1 } }), [pos[0], pos[1] - 0.13 * s, pos[2] + 0.012], [0, 0, PI], false);
  return t;
}
function clothes(R, kind) {
  if (!kind || kind === 'none') return;
  const B = R.B;
  if (!B) { if (R.chest) tie(R, R.chest.parent, R.chest.pos, R.chest.s); return; }
  const T = R.J.torso, th = B.th, s = B.tw / 0.42;
  if (kind === 'tie') { tie(R, T, [0, th * 0.86, B.td / 2 + 0.012], s); return; }
  const jc = kind === 'robe' ? '#121318' : (R.opts.suitColor ?? P.suitNavy);
  R.a(T, box(B.tw * 1.07, th * 0.96, B.td * 1.12, jc, { pivot: 'bottom', taper: { x: B.tap, z: 1 } }), [0, 0.01, 0]);
  for (const sd of ['L', 'R']) {
    R.a(R.J['shoulder' + sd], box(B.aw * 1.3, B.au + B.aw * 0.5, B.aw * 1.3, jc, { pivot: 'top' }), [0, B.aw * 0.5, 0]);
    R.a(R.J['elbow' + sd], box(B.aw * (kind === 'robe' ? 1.6 : 1.22), B.af * 0.8, B.aw * (kind === 'robe' ? 1.6 : 1.22), jc, { pivot: 'top', taper: kind === 'robe' ? 1.25 : 1 }));
  }
  const fz = B.td * 0.56 + 0.012, top = th * 0.96, hw = B.tw * B.tap * 0.5;
  R.a(T, tri([-hw * 0.55, top, 0], [hw * 0.55, top, 0], [0, th * (kind === 'robe' ? 0.7 : 0.32), 0], P.shirt), [0, 0, fz], null, false);
  if (kind === 'suit') {
    for (const sd of [-1, 1]) R.a(T, tri([sd * hw * 0.45, top, 0], [sd * hw * 0.95, top * 0.97, 0], [sd * 0.01, th * 0.3, 0], P.lapelTeal), [0, 0, fz + 0.004], null, false);
    R.a(T, box(0.045 * s, th * 0.5, 0.012, P.tieRed, { taper: { x: 1.6, z: 1 } }), [0, th * 0.68, fz + 0.01], [0, 0, PI], false);
  } else { // judge robe: long skirt + white jabot
    R.a(R.J.hips, box(B.tw * 1.12, B.hipY * 0.82, B.td * 1.18, jc, { pivot: 'top', taper: { x: 1.28, z: 1.12 } }), [0, 0.06, 0]);
    for (const sd of [-1, 1]) R.a(T, box(0.05 * s, 0.13 * s, 0.012, P.white), [sd * 0.028 * s, th * 0.82, fz + 0.01], [0, 0, sd * 0.12], false);
  }
}

// Birds: faceted ellipsoid body, head + hinged beak, panel wings, stick legs, tail fan.
function birdBody(R, o) {
  const [bx, by, bz] = o.body, ll = o.legLen, sd0 = R.seed;
  R.ol = o.ol ?? 0.005;
  const bodyY = ll + by * (o.sit ?? 0.82);
  const pitch = o.pitch ?? -0.12;
  const body = R.joint('body', R.mover, 0, bodyY, 0, pitch);
  R.a(body, facet(bx, by, bz, o.color, { seed: sd0 + 3, jit: 0.06 }));
  if (o.chest) R.a(body, facet(bx * (o.chestS?.[0] ?? 0.9), by * (o.chestS?.[1] ?? 0.78), bz * (o.chestS?.[2] ?? 0.6), o.chest, { seed: sd0 + 4, jit: 0.07 }), [0, by * (o.chestY ?? -0.05), bz * (o.chestZ ?? 0.42)]);
  const neck = R.joint('neck', body, 0, by * (o.neckY ?? 0.5), bz * (o.neckZ ?? 0.6), -pitch);
  const nl = o.neckLen ?? 0;
  if (nl > 0) R.a(neck, cyl(o.neckW * 0.8, o.neckW, nl + o.neckW, o.neckColor ?? o.headColor ?? o.color, 7, { pivot: 'bottom' }), [0, -o.neckW, 0]);
  const head = R.joint('head', neck, 0, nl, o.headZ ?? 0);
  const hr = o.headR, hc = o.headColor ?? o.color;
  R.a(head, facet(hr, hr * (o.headSY ?? 1), hr * (o.headSZ ?? 1), hc, { seed: sd0 + 5, jit: 0.05 }), [0, hr * 0.8, 0]);
  const bk = o.beak, bkY = hr * (bk.y ?? 0.62), bkZ = hr * (bk.z ?? 0.82);
  if (bk.flat) {
    R.a(head, box(bk.w, bk.h * 0.5, bk.len, bk.color, { taper: { x: 1.15, z: 0.8 }, taperAxis: 'z' }), [0, bkY + bk.h * 0.2, bkZ + bk.len / 2]);
  } else {
    const up = R.a(head, cone(bk.w / 2, bk.len, bk.color, 5, { fwd: true }), [0, bkY + bk.h * 0.12, bkZ + bk.len / 2]); up.scale.y = bk.h / bk.w * 1.4;
  }
  const jaw = R.joint('jaw', head, 0, bkY, bkZ);
  if (bk.flat) R.a(jaw, box(bk.w * 0.95, bk.h * 0.32, bk.len * 0.95, bk.color, { taper: { x: 1.1, z: 0.8 }, taperAxis: 'z', pivot: 'top' }), [0, 0, bk.len * 0.47]);
  else { const lo = R.a(jaw, cone(bk.w * 0.4, bk.len * 0.8, bk.lower ?? bk.color, 5, { fwd: true }), [0, -bk.h * 0.12, bk.len * 0.4]); lo.scale.y = 0.6; }
  if (bk.cere) R.a(head, facet(bk.w * 0.35, bk.w * 0.22, bk.w * 0.3, bk.cere, { detail: 0 }), [0, bkY + bk.h * 0.45, bkZ + bk.len * 0.1], null, false);
  if (bk.dot) R.a(jaw, sphere(bk.w * 0.18, bk.dot, 0), [0, -bk.h * 0.12, bk.len * 0.62], null, false);
  addEyes(R, head, { x: hr * (o.eyeX ?? 0.44), y: hr * (o.eyeY ?? 1.05), z: hr * (o.eyeZ ?? 0.72), r: hr * (o.eyeR ?? 0.44), lid: hc, browT: 0.2 });
  // wings
  const span = o.wing?.span ?? by * 1.6, chord = o.wing?.chord ?? bz * 1.1, wt = o.wing?.t ?? 0.012;
  for (const [s, sd] of [['L', 1], ['R', -1]]) {
    const w = R.joint('wing' + s, body, sd * bx * (o.wing?.x ?? 0.78), by * (o.wing?.y ?? 0.4), bz * (o.wing?.z ?? 0.15), 0, 0, -sd * (o.wing?.rz ?? 0.08));
    R.a(w, facet(wt, span / 2, chord / 2, o.wingColor ?? o.color, { seed: sd0 + 7, jit: 0.04 }), [sd * wt, -span * 0.42, -chord * 0.22]);
    if (o.wingTip) R.a(w, facet(wt * 1.3, span * 0.22, chord * 0.32, o.wingTip, { seed: sd0 + 8, detail: 0 }), [sd * wt * 1.6, -span * 0.72, -chord * 0.45]);
    if (o.wingBars) for (const k of [0, 1]) R.a(w, box(wt * 2.6, span * 0.06, chord * 0.45, o.wingBars), [sd * wt * 1.2, -span * (0.48 + k * 0.14), -chord * (0.25 + k * 0.05)], null, false);
  }
  // legs (children of mover: body pitch doesn't swing them)
  for (const [s, sd] of [['L', 1], ['R', -1]]) {
    const hp = R.joint('hip' + s, R.mover, sd * bx * (o.legX ?? 0.38), ll + by * 0.15, o.legZ ?? 0.0);
    const lw = o.legW ?? 0.012;
    R.a(hp, cyl(lw, lw, ll + by * 0.15, o.legColor, 5, { pivot: 'top' }), null, null, R.ol * 0.5);
    const ft = R.joint('foot' + s, hp, 0, -(ll + by * 0.15), 0);
    if (o.webbed) R.a(ft, box(lw * 7, lw * 1.2, lw * 7, o.legColor, { taper: { x: 0.25, z: 1 }, taperAxis: 'z', pivot: 'bottom' }), [0, 0, lw * 2.5]);
    else for (const a of [-0.5, 0, 0.5, PI]) R.a(ft, zbox(lw * 1.1, lw * 1.1, lw * (a === PI ? 3 : 5.5), o.legColor), [0, lw * 0.5, 0], [0, a, 0], false);
  }
  // tail fan
  const tj = R.joint('tail', body, 0, by * (o.tail?.y ?? 0.12), -bz * 0.82, o.tail?.rx ?? 0.25);
  const tn = o.tail?.n ?? 5, tl = o.tail?.len ?? bz * 0.8;
  for (let i = 0; i < tn; i++) {
    const a = tn === 1 ? 0 : (i / (tn - 1) - 0.5) * (o.tail?.spread ?? 0.9);
    R.a(tj, flipZ(zbox(o.tail?.w ?? bx * 0.45, 0.012, tl, o.tail?.color ?? o.color, 0.45)), [0, i * 0.002, 0], [0, a, 0], R.ol * 0.6);
  }
  R.plan = 'bird';
  R.Bd = { ll, by, bz, s: (ll + by * 2) / 0.35, alt: o.alt ?? 0.5, waddle: o.waddle ?? 0.06, upright: !!o.upright, flapF: o.flapF ?? 4 };
  R.chest = { parent: body, pos: [0, 0, bz * 0.95], s: bx / 0.2 };
  return body;
}

// Bug legs: n per side, each = yaw group -> joint (lift/swing) -> knee.
function bugLegs(R, parent, o) {
  R.nLegs = 0; R.legSide = [];
  for (let i = 0; i < o.n; i++) for (const sd of [1, -1]) {
    const k = R.nLegs++; R.legSide.push(sd);
    const yaw = new THREE.Group(); const f = o.n === 1 ? 0.5 : i / (o.n - 1);
    yaw.position.set(sd * o.x, o.y, lerp(o.z0, o.z1, f)); yaw.rotation.y = sd * lerp(o.a0, o.a1, f); parent.add(yaw);
    const lj = R.joint('leg' + k, yaw, 0, 0, 0, -o.lift);
    R.a(lj, zbox(o.w, o.w, o.l1, o.color, 0.8), null, null, R.ol * 0.6);
    const kn = R.joint('knee' + k, lj, 0, 0, o.l1, o.bend);
    if (o.dot) R.a(kn, sphere(o.w * 1.1, o.dot, 1), null, null, false);
    R.a(kn, zbox(o.w * 0.8, o.w * 0.8, o.l2, o.color, 0.5), null, null, R.ol * 0.6);
  }
}
// Antennae (bee, ant): two segments with red tip
function antennae(R, head, o) {
  for (const [s, sd] of [['L', 1], ['R', -1]]) {
    const a = R.joint('ant' + s, head, sd * o.x, o.y, o.z, -0.35, 0, -sd * 0.35);
    R.a(a, cyl(o.w, o.w, o.l1, o.color, 5, { pivot: 'bottom' }), null, null, false);
    const b = R.joint('antTip' + s, a, 0, o.l1, 0, 0.9, 0, 0);
    R.a(b, cyl(o.w * 0.8, o.w, o.l2, o.color, 5, { pivot: 'bottom' }), null, null, false);
    R.a(b, sphere(o.w * 2.4, o.tip, 1), [0, o.l2, 0], null, R.ol * 0.5);
  }
}

// --------------------------------------------------------------- the species --
const col = (o, d) => ({ ...d, ...(o.color ? { body: o.color } : {}), ...(o.colors || {}) });

// Shared mammal assembler: quadruped by default, anthropomorphic biped when upright.
function mammal(R, o, M) {
  const up = o.upright ?? M.upright ?? false;
  if (up) {
    const B = bipedBody(R, M.biped);
    R.a(R.J.neck, box(B.tw * 0.36, 0.14, B.td * 0.55, M.neckColor ?? M.head.color, { pivot: 'bottom' }), [0, -0.03, 0]);
    mHead(R, R.J.neck, { ...M.head, y: M.upY ?? 0.06, hz: M.upHz ?? 0, scale: (M.head.scale ?? 1) * (M.upHead ?? 1.15) });
    if (M.tail) tail(R, R.J.hips, { ...M.tail, y: -0.02, z: -B.td / 2, rx: M.tail.upRx ?? 0.35 });
  } else {
    quadBody(R, M.quad);
    mHead(R, R.J.neckTop, { hz: M.head.d * 0.15, ...M.head });
    if (M.tail) tail(R, R.J.tailBase, M.tail);
  }
  M.extras?.(R, up);
  return up;
}

const SPECIES = {
  // ---------------------------------------------------------------- birds
  pigeon(R, o) {
    const c = col(o, { body: '#8E9FA6', chest: '#5F8A86', head: '#7D8E96', wing: '#A3B2B6', bar: '#3E4A52', tail: '#56656D', leg: P.red, beak: '#3A3F44' });
    birdBody(R, { body: [0.085, 0.085, 0.13], legLen: 0.075, color: c.body, chest: c.chest, chestS: [0.95, 0.85, 0.7], chestY: 0.0, chestZ: 0.45, headR: 0.052, headColor: c.head, neckLen: 0.04, neckW: 0.035, neckColor: c.chest, neckY: 0.55, neckZ: 0.62,
      beak: { len: 0.032, w: 0.016, h: 0.012, color: c.beak, cere: P.white }, wingColor: c.wing, wingBars: c.bar, wingTip: c.tail, legColor: c.leg, legW: 0.007,
      tail: { n: 7, len: 0.1, spread: 1.1, color: c.tail, rx: 0.15, w: 0.035 }, pitch: -0.2, alt: 0.6, eyeR: 0.5 });
    R.height = 0.32;
  },
  seagull(R, o) {
    const c = col(o, { body: P.white, wing: P.grey, tip: P.black, leg: '#E8A36A', beak: P.yellow });
    birdBody(R, { body: [0.09, 0.09, 0.18], legLen: 0.11, color: c.body, headR: 0.06, neckLen: 0.05, neckW: 0.04, beak: { len: 0.07, w: 0.02, h: 0.016, color: c.beak, dot: P.red },
      wingColor: c.wing, wingTip: c.tip, wing: { span: 0.17, chord: 0.24 }, legColor: c.leg, legW: 0.008, webbed: true, tail: { n: 3, len: 0.08, spread: 0.5, color: P.white, rx: 0.15 }, pitch: -0.08, alt: 0.8, eyeR: 0.46 });
    R.height = 0.42;
  },
  chicken(R, o) {
    const c = col(o, { body: '#F4EFE2', tail: '#E3D7B8', comb: P.red, beak: P.yellow, leg: '#E0A93A' });
    birdBody(R, { body: [0.12, 0.12, 0.16], legLen: 0.12, color: c.body, headR: 0.065, neckLen: 0.07, neckW: 0.05, neckY: 0.55, neckZ: 0.55, beak: { len: 0.04, w: 0.026, h: 0.02, color: c.beak },
      legColor: c.leg, legW: 0.01, tail: { n: 5, len: 0.14, spread: 0.7, color: c.tail, rx: -0.75, w: 0.05 }, pitch: -0.15, alt: 0.35, flapF: 6, eyeR: 0.46 });
    const h = R.J.head;
    for (let i = 0; i < 3; i++) R.a(h, box(0.02, 0.04 - abs(i - 1) * 0.008, 0.026, c.comb, { taper: 0.6 }), [0, 0.065 * 1.72, 0.03 - i * 0.025], null, R.ol * 0.5);
    R.a(R.J.jaw, facet(0.012, 0.022, 0.012, c.comb, { detail: 0 }), [0, -0.025, 0.012], null, R.ol * 0.5);
    R.height = 0.5;
  },
  duck(R, o) {
    const c = col(o, { body: '#BDB8AE', chest: '#8A5A3E', head: '#2F6B4A', bill: '#E8A33C', leg: '#E8A33C', tail: '#3A3D44' });
    birdBody(R, { body: [0.13, 0.11, 0.19], legLen: 0.06, color: c.body, chest: c.chest, chestZ: 0.5, headR: 0.07, headColor: c.head, neckLen: 0.07, neckW: 0.045, neckColor: c.head, neckY: 0.5, neckZ: 0.6,
      beak: { len: 0.07, w: 0.05, h: 0.03, color: c.bill, flat: true, y: 0.5, z: 0.75 }, legColor: c.leg, legW: 0.009, webbed: true, wingColor: '#9A958B', wingBars: '#3E6FA0',
      tail: { n: 3, len: 0.06, spread: 0.6, color: c.tail, rx: -0.6 }, pitch: -0.05, waddle: 0.16, alt: 0.6, eyeR: 0.45 });
    R.a(R.J.neck, cyl(0.048, 0.048, 0.012, P.white, 8), [0, 0.015, 0], null, false);
    R.height = 0.42;
  },
  penguin(R, o) {
    const c = col(o, { body: P.navy, belly: P.white, beak: '#E8A33C', leg: '#E8A33C' });
    birdBody(R, { body: [0.17, 0.27, 0.15], legLen: 0.03, sit: 0.95, color: c.body, chest: c.belly, chestS: [0.78, 0.85, 0.55], chestY: -0.08, chestZ: 0.5, headR: 0.13, neckLen: 0, neckY: 0.78, neckZ: 0.05, headZ: 0,
      beak: { len: 0.07, w: 0.04, h: 0.03, color: c.beak, y: 0.5 }, wing: { span: 0.3, chord: 0.12, t: 0.025, x: 0.92, y: 0.45, z: 0.0, rz: 0.12 }, legColor: c.leg, legW: 0.016, webbed: true, legX: 0.5, legZ: 0.04,
      tail: { n: 1, len: 0.06, color: c.body, rx: 0.9 }, pitch: 0, waddle: 0.2, upright: true, eyeR: 0.4, eyeY: 1.15, flapF: 6, alt: 0.3 });
    R.a(R.J.head, facet(0.1, 0.075, 0.06, c.belly, { seed: 3 }), [0, 0.095, 0.075], null, false);
    R.height = 0.8;
  },
  owl(R, o) {
    const c = col(o, { body: '#8C6239', face: P.cream, belly: '#D9B98A', beak: '#4A3A2A', leg: '#D9A23A' });
    birdBody(R, { body: [0.15, 0.17, 0.13], legLen: 0.03, sit: 0.95, color: c.body, chest: c.belly, chestS: [0.75, 0.8, 0.55], chestY: -0.15, chestZ: 0.5, headR: 0.14, neckLen: 0, neckY: 0.75, neckZ: 0, headSY: 0.85,
      beak: { len: 0.04, w: 0.03, h: 0.03, color: c.beak, y: 0.5, z: 0.85 }, wing: { span: 0.26, chord: 0.16, t: 0.02, x: 0.85, y: 0.45, z: -0.05 }, legColor: c.leg, legW: 0.014, legX: 0.4, legZ: 0.05,
      tail: { n: 3, len: 0.08, color: c.body, rx: 0.4, spread: 0.4 }, pitch: 0, upright: true, eyeR: 0.4, eyeY: 0.95, eyeX: 0.45, eyeZ: 0.72, alt: 0.6 });
    R.a(R.J.head, facet(0.13, 0.1, 0.05, c.face, { seed: 4 }), [0, 0.11, 0.085], null, false);
    for (const sd of [1, -1]) R.a(R.J.head, box(0.04, 0.08, 0.04, c.body, { pivot: 'bottom', taper: 0.15 }), [sd * 0.09, 0.2, -0.01], [0, 0, -sd * 0.35]);
    R.height = 0.55;
  },

  // ---------------------------------------------------------------- bugs
  ant(R, o) {
    const c = col(o, { body: '#1A2232', shine: '#3C4E6E', red: P.red, abdomen: P.red, stripe: '#4A1410', leg: '#11141A' });
    R.ol = 0.012;
    if (o.upright === false) {
      const body = R.joint('body', R.mover, 0, 0.35, 0);
      R.a(body, facet(0.13, 0.11, 0.17, c.body, { seed: 2 }), [0, 0, 0.05]);
      const ab = R.joint('abdomen', body, 0, 0.02, -0.12, -0.2);
      R.a(ab, facet(0.17, 0.15, 0.24, c.abdomen, { seed: 3 }), [0, 0, -0.22]);
      for (const z of [-0.12, -0.22, -0.32]) R.a(ab, cyl(0.155 - abs(z + 0.22) * 0.5, 0.155 - abs(z + 0.22) * 0.5, 0.025, c.stripe, 9), [0, 0, z], [PI / 2, 0, 0], false);
      bugLegs(R, body, { n: 3, x: 0.08, y: -0.04, z0: 0.12, z1: -0.04, a0: 0.7, a1: 2.3, lift: 0.7, bend: 1.9, l1: 0.26, l2: 0.42, w: 0.026, color: c.leg, dot: c.red });
      const hd = R.joint('head', body, 0, 0.05, 0.22);
      antHead(R, hd, c, 0.85);
      R.plan = 'legs'; R.height = 0.75; return;
    }
    const B = bipedBody(R, { leg: 0.38, legW: 0.042, footH: 0.04, footLen: 0.16, footW: 1.4, footTaper: { x: 0.6, z: 1 }, tw: 0.3, th: 0.38, td: 0.25, taper: 1.15, armW: 0.042, armU: 0.3, armF: 0.3, hand: 'claw', noTorso: true, noPelvis: true, dots: c.red, shY: 0.85, shX: 0.17,
      colors: { body: c.body, arm: c.leg, leg: c.leg, hand: c.leg, foot: c.leg } });
    const T = R.J.torso;
    R.a(T, facet(0.16, 0.22, 0.14, c.body, { seed: 4, jit: 0.08 }), [0, B.th * 0.58, 0]);
    R.a(T, facet(0.07, 0.11, 0.04, c.shine, { seed: 5, detail: 0 }), [0.05, B.th * 0.72, 0.105], null, false);
    R.a(T, facet(0.07, 0.07, 0.07, c.body, { seed: 6, detail: 0 }), [0, 0.03, 0]); // petiole
    R.a(R.J.hips, facet(0.09, 0.06, 0.08, c.body, { seed: 7, detail: 0 }), [0, -0.03, 0]);
    const ab = R.joint('abdomen', R.J.hips, 0, -0.02, -0.06, 0.55);
    R.a(ab, facet(0.2, 0.19, 0.3, c.abdomen, { seed: 8, jit: 0.06 }), [0, 0, -0.28]);
    for (const [z, rr] of [[-0.14, 0.17], [-0.26, 0.205], [-0.38, 0.18]]) R.a(ab, cyl(rr, rr, 0.035, c.stripe, 9), [0, 0, z], [PI / 2, 0, 0], false);
    R.a(ab, facet(0.06, 0.05, 0.06, c.shine, { seed: 9, detail: 0 }), [0.07, 0.14, -0.25], null, false);
    // middle pair of arms (smaller), they follow the main arms
    for (const [s, sd] of [['L', 1], ['R', -1]]) {
      const sh = R.joint('shoulder2' + s, T, sd * 0.15, B.th * 0.42, 0.03, -0.5, 0, sd * 0.35);
      R.a(sh, box(0.034, 0.24, 0.034, c.leg, { pivot: 'top' }));
      const el = R.joint('elbow2' + s, sh, 0, -0.24, 0, -0.9);
      R.a(el, sphere(0.032, c.red, 1), null, null, R.ol * 0.6);
      R.a(el, box(0.03, 0.22, 0.03, c.leg, { pivot: 'top', taper: 0.4 }));
    }
    R.a(R.J.neck, cyl(0.03, 0.04, 0.08, c.body, 6, { pivot: 'bottom' }), [0, -0.02, 0]);
    const hd = R.joint('head', R.J.neck, 0, 0.05, 0.02);
    antHead(R, hd, c, 1);
    R.height = 1.55;
  },
  bee(R, o) {
    const c = col(o, { body: P.yellow, band: '#17181B', head: '#1E1F24', wing: '#EAF3F4' });
    R.ol = 0.008;
    const body = R.joint('body', R.mover, 0, 0.62, 0);
    R.a(body, facet(0.13, 0.12, 0.17, c.body, { seed: 3 }), [0, 0, -0.08]);
    for (const [z, rr] of [[-0.02, 0.118], [-0.1, 0.128], [-0.18, 0.1]]) R.a(body, cyl(rr, rr, 0.03, c.band, 9), [0, 0, z], [PI / 2, 0, 0], false);
    R.a(body, cone(0.03, 0.08, c.band, 5, { fwd: true }), [0, -0.01, -0.27], [0, PI, 0]);
    R.a(body, facet(0.08, 0.08, 0.08, '#C9962F', { seed: 4 }), [0, 0.01, 0.07]); // fuzzy thorax
    const hd = R.joint('head', body, 0, 0.02, 0.14);
    R.a(hd, facet(0.085, 0.08, 0.075, c.head, { seed: 5 }), [0, 0.02, 0.04]);
    addEyes(R, hd, { x: 0.042, y: 0.04, z: 0.09, r: 0.042, lid: c.head, browColor: c.body === P.yellow ? INK : INK, browT: 0.2 });
    R.a(hd, box(0.03, 0.008, 0.01, P.redDark), [0, -0.025, 0.11], null, false);
    const jaw = R.joint('jaw', hd, 0, -0.025, 0.1); R.a(jaw, box(0.028, 0.012, 0.012, c.head, { pivot: 'top' }), null, null, false);
    antennae(R, hd, { x: 0.025, y: 0.08, z: 0.06, w: 0.006, l1: 0.06, l2: 0.06, color: c.band, tip: c.band });
    for (const [s, sd] of [['L', 1], ['R', -1]]) {
      const w = R.joint('wing' + s, body, sd * 0.04, 0.08, 0.05, 0, 0, sd * 0.35);
      R.a(w, facet(0.13, 0.006, 0.065, c.wing, { seed: 6, opacity: 0.72, detail: 1 }), [sd * 0.12, 0, -0.03], [0, -sd * 0.35, 0], R.ol * 0.5);
      R.a(w, facet(0.08, 0.005, 0.045, c.wing, { seed: 7, opacity: 0.72, detail: 1 }), [sd * 0.08, -0.005, -0.1], [0, sd * 0.4, 0], R.ol * 0.5);
      for (const z of [0.1, 0.05, 0.0]) R.a(body, cyl(0.006, 0.006, 0.12, c.band, 4, { pivot: 'top' }), [sd * 0.05, -0.05, z], [0.25 - z * 3, 0, sd * 0.3], false);
    }
    R.plan = 'flyer'; R.height = 0.85; R.hover = 0.62;
  },
  spider(R, o) {
    const c = col(o, { body: '#1D2130', abdomen: '#262A3A', mark: P.red, leg: '#14171F' });
    R.ol = 0.008;
    const body = R.joint('body', R.mover, 0, 0.2, 0);
    R.a(body, facet(0.11, 0.08, 0.11, c.body, { seed: 2 }), [0, 0, 0.04]);
    const ab = R.joint('abdomen', body, 0, 0.04, -0.06, -0.25);
    R.a(ab, facet(0.17, 0.15, 0.2, c.abdomen, { seed: 3 }), [0, 0.02, -0.17]);
    R.a(ab, box(0.05, 0.012, 0.09, c.mark, { taper: { x: 0.3, z: 1 }, taperAxis: 'z' }), [0, 0.165, -0.15], null, false);
    R.a(ab, box(0.05, 0.012, 0.07, c.mark, { taper: { x: 0.3, z: 1 }, taperAxis: 'z' }), [0, 0.16, -0.23], [0, PI, 0], false);
    bugLegs(R, body, { n: 4, x: 0.07, y: 0.0, z0: 0.1, z1: -0.01, a0: 0.55, a1: 2.45, lift: 0.65, bend: 1.65, l1: 0.2, l2: 0.36, w: 0.02, color: c.leg, dot: c.mark });
    const hd = R.joint('head', body, 0, 0.03, 0.12);
    addEyes(R, hd, { x: 0.042, y: 0.03, z: 0.02, r: 0.045, lid: c.body, browColor: c.mark });
    for (const sd of [1, -1]) R.a(hd, sphere(0.014, PUPIL, 1), [sd * 0.022, 0.085, -0.01], null, false);
    const jaw = R.joint('jaw', hd, 0, -0.03, 0.02);
    for (const sd of [1, -1]) R.a(jaw, box(0.018, 0.05, 0.02, c.mark, { pivot: 'top', taper: 0.2 }), [sd * 0.022, 0, 0], [0.3, 0, 0]);
    R.plan = 'legs'; R.height = 0.42;
  },
  snail(R, o) {
    const c = col(o, { body: '#C9B48A', shell: P.salmon, spiral: P.redDark, stalk: '#B59D72' });
    R.ol = 0.007;
    const body = R.joint('body', R.mover, 0, 0, 0);
    R.a(body, box(0.13, 0.08, 0.42, c.body, { pivot: 'bottom', taper: { x: 0.75, z: 0.65 }, taperAxis: 'z' }), [0, 0, -0.03]);
    const hd = R.joint('head', body, 0, 0.04, 0.16);
    R.a(hd, facet(0.065, 0.075, 0.07, c.body, { seed: 4 }), [0, 0.04, 0.02]);
    const jaw = R.joint('jaw', hd, 0, 0.02, 0.085); R.a(jaw, box(0.035, 0.012, 0.01, P.redDark, { pivot: 'top' }), null, null, false);
    for (const [s, sd] of [['L', 1], ['R', -1]]) {
      const st = R.joint('stalk' + s, hd, sd * 0.03, 0.09, 0.03, 0.25, 0, -sd * 0.25);
      R.a(st, cyl(0.009, 0.013, 0.13, c.stalk, 5, { pivot: 'bottom' }), null, null, R.ol * 0.6);
    }
    // eyes on stalk tips (eyes follow the stalk joints)
    for (const [s, sd] of [['L', 1], ['R', -1]]) {
      const before = R.eyes.length;
      addEyes(R, R.J['stalk' + s], { x: 0, y: 0.15, z: 0.0, r: 0.04, lid: c.stalk, browY: 1.45 });
      // keep only this side's eye
      const pair = R.eyes.splice(before, 2); const keep = pair.find(e => e.side === sd), drop = pair.find(e => e.side !== sd);
      drop.g.parent.remove(drop.g); drop.browG.parent.remove(drop.browG); keep.g.position.x = 0; keep.browG.position.x = 0; keep.g.rotation.y = 0;
      R.eyes.push(keep);
    }
    const sh = R.joint('shell', body, 0, 0.08, -0.08, -0.2);
    R.a(sh, facet(0.075, 0.15, 0.15, c.shell, { seed: 5, detail: 1 }), [0, 0.1, 0]);
    for (const [rr, x] of [[0.11, 0.07], [0.065, 0.078], [0.03, 0.082]]) for (const sd of [1, -1]) R.a(sh, new THREE.Mesh(new THREE.TorusGeometry(rr, 0.008, 3, 12), mat(c.spiral)), [sd * x * (rr > 0.1 ? 0.95 : 1), 0.1, 0], [0, PI / 2, 0], false);
    R.plan = 'blob'; R.loco = 'slide'; R.height = 0.36;
  },

  // ---------------------------------------------------------------- mammals
  lion(R, o) {
    const c = col(o, { body: '#D49A4E', belly: '#EAC98E', mane: '#9A5428', mane2: '#C06A2C', snout: '#EFD8A8', nose: '#5A3020', paw: '#C08840' });
    R.ol = 0.012;
    const head = { w: 0.36, h: 0.36, d: 0.32, color: c.body, snout: { w: 0.24, h: 0.14, d: 0.13, color: c.snout, y: 0.1, teeth: 2 }, nose: c.nose, noseW: 0.42,
      eye: { x: 0.085, y: 0.235, r: 0.075 }, ears: { type: 'round', size: 0.06, x: 0.17, y: 0.36, z: -0.03, color: c.body, inner: c.mane } };
    const up = mammal(R, o, { head,
      quad: { L: 1.25, W: 0.52, H: 0.48, legH: 0.52, legW: 0.15, color: c.body, belly: c.belly, paw: c.paw, neck: { len: 0.2, w: 0.3, d: 0.3, rx: 0.5 } },
      biped: { leg: 0.44, legW: 0.15, tw: 0.46, th: 0.6, td: 0.32, taper: 1.18, armW: 0.13, armU: 0.3, armF: 0.29, hand: 'paw', colors: { body: c.body, belly: c.belly, arm: c.body, leg: c.body, hand: c.paw, foot: c.paw } },
      tail: { len: 0.7, w: 0.045, color: c.body, tuft: c.mane, rx: 0.55, rx2: 0.5 },
      extras: (R, up) => {
        const hd = R.J.head, s = up ? 1 : 1;
        R.a(hd, facet(0.36 * s, 0.36 * s, 0.17, c.mane, { seed: 11, jit: 0.18 }), [0, 0.19, -0.1]);
        R.a(hd, facet(0.27, 0.28, 0.13, c.mane2, { seed: 12, jit: 0.15 }), [0, 0.2, -0.04]);
        R.a(hd, facet(0.11, 0.08, 0.08, c.mane, { seed: 13, jit: 0.2, detail: 0 }), [0, 0.37, 0.08]);
        if (up) R.a(R.J.torso, facet(0.3, 0.2, 0.22, c.mane, { seed: 14, jit: 0.18 }), [0, R.B.th * 0.92, -0.02]);
        else R.a(R.J.neck, facet(0.26, 0.28, 0.24, c.mane, { seed: 14, jit: 0.18 }), [0, 0.1, -0.02]);
      } });
    R.height = up ? 2.0 : 1.25;
  },
  zebra(R, o) { return horseLike(R, o, col(o, { body: '#F2EEE4', stripe: '#1A1B1F', mane: '#1A1B1F', muzzle: '#55555B', hoof: '#1A1B1F' }), true); },
  horse(R, o) { return horseLike(R, o, col(o, { body: '#8C5A35', stripe: null, mane: '#2A1C14', muzzle: '#6E4428', hoof: '#2A1C14', blaze: P.white }), false); },
  giraffe(R, o) {
    const c = col(o, { body: '#E2B85A', spot: '#9A5A2B', muzzle: '#EAD3A2', horn: '#7A4A22', hoof: '#4A3020' });
    R.ol = 0.012;
    const up = mammal(R, o, {
      head: { w: 0.22, h: 0.26, d: 0.24, color: c.body, snout: { w: 0.18, h: 0.13, d: 0.16, color: c.muzzle, y: 0.07, rx: 0.15 }, nose: '#5A3A22', eye: { x: 0.06, y: 0.175, r: 0.06 },
        ears: { type: 'side', size: 0.08, x: 0.1, y: 0.2, color: c.body, inner: c.muzzle, tilt: 0.4 } },
      quad: { L: 1.0, W: 0.45, H: 0.5, legH: 1.25, legW: 0.1, color: c.body, hoof: c.hoof, taper: { x: 0.9, z: 0.9 }, neck: { len: 1.4, w: 0.16, d: 0.18, rx: 0.32, y: 0.3, back: 0.6 } },
      biped: { leg: 0.62, legW: 0.1, tw: 0.38, th: 0.62, td: 0.28, armW: 0.09, armU: 0.33, armF: 0.32, colors: { body: c.body, arm: c.body, leg: c.body, hand: c.hoof, foot: c.hoof } },
      upY: 0.7, neckColor: c.body,
      tail: { len: 0.55, w: 0.03, color: c.body, tuft: c.horn, rx: 0.3 },
      extras: (R, up) => {
        for (const sd of [1, -1]) { R.a(R.J.head, cyl(0.015, 0.018, 0.09, c.horn, 5, { pivot: 'bottom' }), [sd * 0.05, 0.25, -0.03]); R.a(R.J.head, sphere(0.026, c.horn, 0), [sd * 0.05, 0.345, -0.03]); }
        if (!up) {
          patches(R, R.J.body, 14, c.spot, { faces: ['x+', 'x-', 'y+'], w: 0.45 * 0.92, h: 0.5, d: 1.0, y: 0, z: 0, s: 0.13 }, 3);
          const nk = R.J.neck; patches(R, nk, 10, c.spot, { faces: ['x+', 'x-'], w: 0.16 * 0.92, h: 1.2, d: 0.16, y: 0.7, z: 0, s: 0.07 }, 4);
          R.a(nk, box(0.04, 1.35, 0.05, c.horn), [0, 0.7, -0.1], null, false);
        } else { R.a(R.J.neck, box(0.16, 0.75, 0.18, c.body, { pivot: 'bottom' }), [0, 0, 0]); patches(R, R.J.torso, 10, c.spot, { faces: ['x+', 'x-'], w: 0.42, h: 0.5, d: 0.25, y: 0.32, z: 0, s: 0.09 }, 5); }
      } });
    R.height = up ? 2.6 : 3.4;
  },
  elephant(R, o) {
    const c = col(o, { body: '#9EA3A6', dark: '#7E8487', ear: '#B9A2A4', tusk: P.cream, toe: P.cream });
    R.ol = 0.016;
    const up = mammal(R, o, {
      head: { w: 0.62, h: 0.62, d: 0.5, color: c.body, eye: { x: 0.15, y: 0.4, r: 0.1 } },
      quad: { L: 1.7, W: 1.05, H: 1.0, legH: 0.8, legW: 0.3, color: c.body, paw: c.dark, neck: { len: 0.05, w: 0.6, d: 0.5, rx: 0.3, y: 0.05, back: 0.3 } },
      biped: { leg: 0.42, legW: 0.24, tw: 0.7, th: 0.72, td: 0.5, taper: 1.05, armW: 0.2, armU: 0.33, armF: 0.3, colors: { body: c.body, arm: c.body, leg: c.body, hand: c.body, foot: c.dark } },
      upHead: 0.95, upY: 0.0,
      tail: { len: 0.55, w: 0.035, color: c.body, tuft: c.dark, rx: 0.2 },
      extras: (R) => {
        const hd = R.J.head;
        // trunk: 3 segments (talk/eat/celebrate curl it)
        let p = R.joint('trunk0', hd, 0, 0.3, 0.33, -0.25);
        R.a(p, box(0.22, 0.26, 0.2, c.body, { pivot: 'top', taper: 0.85 }));
        p = R.joint('trunk1', p, 0, -0.24, 0, -0.1); R.a(p, box(0.18, 0.26, 0.16, c.body, { pivot: 'top', taper: 0.85 }));
        p = R.joint('trunk2', p, 0, -0.24, 0, -0.55); R.a(p, box(0.15, 0.22, 0.14, c.body, { pivot: 'top', taper: 0.9 }));
        for (let i = 0; i < 3; i++) R.a(R.J.trunk1, box(0.19, 0.012, 0.17, c.dark), [0, -0.06 - i * 0.07, 0], null, false);
        R.a(p, box(0.12, 0.03, 0.11, c.dark), [0, -0.2, 0], null, false);
        const jaw = R.joint('jaw', hd, 0, 0.13, 0.3); R.a(jaw, box(0.2, 0.06, 0.1, c.dark, { pivot: 'top' }), [0, 0, 0.0]);
        R.a(jaw, box(0.16, 0.01, 0.1, P.redDark), [0, 0.003, 0], null, false);
        for (const [s, sd] of [['L', 1], ['R', -1]]) {
          R.a(hd, cone(0.04, 0.26, c.tusk, 5), [sd * 0.15, 0.14, 0.38], [1.25, 0, -sd * 0.25]);
          const e = R.joint('ear' + s, hd, sd * 0.3, 0.38, -0.02, 0, sd * 0.35, 0);
          R.a(e, facet(0.25, 0.32, 0.03, c.body, { seed: 21, jit: 0.1 }), [sd * 0.22, -0.05, 0]);
          R.a(e, facet(0.18, 0.24, 0.02, c.ear, { seed: 22, jit: 0.1 }), [sd * 0.22, -0.05, 0.02], null, false);
        }
      } });
    R.height = up ? 2.3 : 2.5;
  },
  hippo(R, o) {
    const c = col(o, { body: '#8E8AA6', belly: '#D9A3A6', snout: '#9E9AB4', inner: '#D98A94' });
    R.ol = 0.015;
    const up = mammal(R, o, {
      head: { w: 0.56, h: 0.42, d: 0.42, color: c.body, snout: { w: 0.66, h: 0.28, d: 0.38, color: c.snout, y: 0.13, teeth: 2, jh: 0.5, taper: { x: 1.05, z: 0.95 } }, nose: '#5E5A72', noseW: 0.5, noseH: 0.18,
        eye: { x: 0.14, y: 0.36, r: 0.1 }, ears: { type: 'round', size: 0.045, x: 0.2, y: 0.42, color: c.body, inner: c.inner } },
      quad: { L: 1.5, W: 0.9, H: 0.75, legH: 0.32, legW: 0.24, color: c.body, belly: c.belly, paw: '#6E6A86', neck: { len: 0.05, w: 0.6, d: 0.4, rx: 0.2, y: 0.05, back: 0.3 } },
      biped: { leg: 0.36, legW: 0.22, tw: 0.66, th: 0.6, td: 0.5, taper: 0.95, armW: 0.17, armU: 0.28, armF: 0.26, colors: { body: c.body, belly: c.belly, arm: c.body, leg: c.body, hand: c.body, foot: '#6E6A86' } },
      upHead: 1, tail: { len: 0.18, w: 0.04, color: c.body, rx: 0.4 },
    });
    R.height = up ? 1.85 : 1.3;
  },
  crocodile(R, o) {
    const c = col(o, { body: '#5E7F4A', belly: '#C9C08A', ridge: '#45603A' });
    R.ol = 0.012;
    const up = mammal(R, o, {
      head: { w: 0.36, h: 0.2, d: 0.26, color: c.body, taper: { x: 0.9, z: 1 }, snout: { w: 0.28, h: 0.11, d: 0.55, color: c.body, y: 0.07, teeth: 6, jh: 0.55, jawColor: c.belly, taper: { x: 0.75, z: 0.9 } }, nose: c.ridge, noseW: 0.3, noseH: 0.3,
        eye: { x: 0.09, y: 0.2, r: 0.075, inset: 0.06, browY: 1.25 } },
      quad: { L: 1.1, W: 0.5, H: 0.26, legH: 0.14, legW: 0.1, color: c.body, belly: c.belly, splay: 0.6, legOut: 0.02, neck: { len: 0.02, w: 0.36, d: 0.2, rx: 0.0, y: 0.0, back: 0.2 } },
      biped: { leg: 0.36, legW: 0.13, tw: 0.42, th: 0.62, td: 0.3, taper: 1.05, armW: 0.1, armU: 0.28, armF: 0.27, colors: { body: c.body, belly: c.belly, arm: c.body, leg: c.body, hand: c.body, foot: c.ridge } },
      upHead: 1.1,
      extras: (R, up) => {
        const parent = up ? R.J.hips : R.J.tailBase;
        const t = R.joint('tail', parent, 0, up ? -0.05 : -0.06, up ? -0.12 : 0, up ? 0.7 : 0.08);
        R.a(t, flipZ(zbox(0.34, 0.2, 0.55, c.body, 0.7)));
        const t2 = R.joint('tail2', t, 0, 0, -0.52, 0.05); R.a(t2, flipZ(zbox(0.23, 0.14, 0.55, c.body, 0.4)));
        for (let i = 0; i < 4; i++) R.a(t, box(0.04, 0.07, 0.06, c.ridge, { taper: 0.3, pivot: 'bottom' }), [0, 0.09 - i * 0.008, -0.08 - i * 0.12], null, R.ol * 0.5);
        if (!up) for (let i = 0; i < 6; i++) for (const sd of [1, -1]) R.a(R.J.body, box(0.04, 0.06, 0.06, c.ridge, { taper: 0.3, pivot: 'bottom' }), [sd * 0.1, 0.13, 0.4 - i * 0.16], null, R.ol * 0.5);
      } });
    R.height = up ? 1.85 : 0.5;
  },
  bear(R, o) {
    const c = col(o, { body: '#6B4A30', belly: '#8E6A48', snout: '#B08A62', paw: '#4E3522' });
    R.ol = 0.013;
    const up = mammal(R, o, {
      head: { w: 0.42, h: 0.38, d: 0.36, color: c.body, snout: { w: 0.2, h: 0.13, d: 0.14, color: c.snout, y: 0.1 }, eye: { x: 0.1, y: 0.25, r: 0.078 }, ears: { type: 'round', size: 0.065, x: 0.16, y: 0.36, color: c.body, inner: c.snout } },
      quad: { L: 1.15, W: 0.66, H: 0.6, legH: 0.42, legW: 0.19, color: c.body, belly: c.belly, paw: c.paw, taper: { x: 0.9, z: 0.92 }, neck: { len: 0.12, w: 0.4, d: 0.36, rx: 0.65 } },
      biped: { leg: 0.44, legW: 0.19, tw: 0.6, th: 0.7, td: 0.42, taper: 1.05, armW: 0.16, armU: 0.33, armF: 0.3, colors: { body: c.body, belly: c.belly, arm: c.body, leg: c.body, hand: c.paw, foot: c.paw } },
      tail: { len: 0.1, w: 0.07, color: c.body, rx: 1.0 }, upHead: 1.1 });
    R.height = up ? 2.15 : 1.15;
  },
  dog(R, o) {
    const c = col(o, { body: '#C99A62', chest: P.white, ear: '#7A5232', snout: '#E8D2AE', collar: P.red });
    R.ol = 0.009;
    const up = mammal(R, o, {
      head: { w: 0.27, h: 0.25, d: 0.24, color: c.body, snout: { w: 0.15, h: 0.11, d: 0.14, color: c.snout, y: 0.07 }, eye: { x: 0.062, y: 0.165, r: 0.058 }, ears: { type: 'floppy', size: 0.09, x: 0.135, y: 0.23, z: -0.02, color: c.ear } },
      quad: { L: 0.62, W: 0.28, H: 0.27, legH: 0.3, legW: 0.085, color: c.body, belly: c.chest, neck: { len: 0.12, w: 0.16, d: 0.16, rx: 0.55 } },
      biped: { leg: 0.3, legW: 0.1, tw: 0.3, th: 0.42, td: 0.22, armW: 0.08, armU: 0.22, armF: 0.2, colors: { body: c.body, belly: c.chest, arm: c.body, leg: c.body, hand: c.body, foot: c.body } },
      tail: { len: 0.24, w: 0.04, color: c.body, rx: 2.3, rx2: -0.3 },
      extras: (R, up) => { if (!up) R.a(R.J.neck, box(0.18, 0.04, 0.18, c.collar), [0, 0.04, 0], null, R.ol * 0.5); else R.a(R.J.neck, box(0.14, 0.035, 0.14, c.collar), [0, 0.06, 0], null, R.ol * 0.5); } });
    R.height = up ? 1.3 : 0.75;
  },
  cat(R, o) {
    const c = col(o, { body: '#D9863F', stripe: '#A85A22', belly: '#F2E2C8', nose: P.pink });
    R.ol = o.ol ?? 0.007;
    const up = mammal(R, o, {
      head: { w: 0.24, h: 0.2, d: 0.18, color: c.body, taper: { x: 0.92, z: 0.9 }, snout: { w: 0.1, h: 0.06, d: 0.05, color: c.belly, y: 0.05 }, nose: c.nose, noseW: 0.5, noseH: 0.35,
        eye: { x: 0.055, y: 0.12, r: 0.052 }, ears: { type: 'pointy', size: 0.08, x: 0.08, y: 0.18, color: c.body, inner: P.pink } },
      quad: { L: 0.46, W: 0.19, H: 0.19, legH: 0.2, legW: 0.06, color: c.body, belly: c.belly, neck: { len: 0.06, w: 0.12, d: 0.12, rx: 0.5 } },
      biped: { leg: 0.2, legW: 0.07, tw: 0.2, th: 0.28, td: 0.16, armW: 0.06, armU: 0.15, armF: 0.14, colors: { body: c.body, belly: c.belly, arm: c.body, leg: c.body, hand: c.belly, foot: c.belly } },
      tail: { len: 0.36, w: 0.035, color: c.body, rx: 2.6, rx2: -0.6 },
      extras: (R, up) => {
        for (const sd of [1, -1]) for (const a of [-0.15, 0.15]) R.a(R.muzzle, box(0.09, 0.005, 0.005, INK), [sd * 0.085, 0.01, 0.04], [0, 0, a * sd], false);
        if (!up) stripes(R, R.J.body, [0.19 * 0.92, 0.19, 0.46], [0, 0.0, 0], 'z', 4, c.stripe, { th: 0.03, from: 0.15, to: 0.75 });
      } });
    R.height = up ? 0.85 : 0.45;
  },
  rat(R, o) {
    const c = col(o, { body: '#8E8E8A', ear: P.pink, tail: '#D99AA0', snout: '#A6A6A2' });
    R.ol = 0.005;
    const up = mammal(R, o, {
      head: { w: 0.12, h: 0.1, d: 0.1, color: c.body, snout: { w: 0.08, h: 0.06, d: 0.09, color: c.snout, y: 0.035, taper: { x: 0.5, z: 0.6 } }, nose: P.pink, noseW: 0.5, noseH: 0.5,
        eye: { x: 0.03, y: 0.07, r: 0.034 }, ears: { type: 'round', size: 0.035, x: 0.055, y: 0.08, z: -0.02, color: c.body, inner: c.ear } },
      quad: { L: 0.26, W: 0.12, H: 0.11, legH: 0.06, legW: 0.035, color: c.body, paw: c.ear, taper: { x: 0.85, z: 0.85 }, neck: { len: 0.02, w: 0.08, d: 0.08, rx: 0.4 } },
      biped: { leg: 0.12, legW: 0.045, tw: 0.13, th: 0.16, td: 0.1, armW: 0.035, armU: 0.09, armF: 0.08, colors: { body: c.body, arm: c.body, leg: c.body, hand: c.ear, foot: c.ear } },
      upHead: 1.25, tail: { len: 0.3, w: 0.015, color: c.tail, rx: 1.3, rx2: 0.2, upRx: 0.9 } });
    R.height = up ? 0.55 : 0.2;
  },
  cow(R, o) {
    const c = col(o, { body: '#F4F0E6', spot: '#1F2024', snout: '#E8A3A3', horn: P.cream, hoof: '#2A2A2E' });
    R.ol = 0.013;
    const up = mammal(R, o, {
      head: { w: 0.38, h: 0.4, d: 0.32, color: c.body, snout: { w: 0.36, h: 0.17, d: 0.13, color: c.snout, y: 0.09, rx: 0.1 }, nose: '#B56A6A', noseW: 0.6, noseH: 0.2,
        eye: { x: 0.1, y: 0.27, r: 0.08 }, ears: { type: 'side', size: 0.11, x: 0.19, y: 0.3, color: c.body, inner: c.snout } },
      quad: { L: 1.4, W: 0.65, H: 0.62, legH: 0.62, legW: 0.15, color: c.body, hoof: c.hoof, neck: { len: 0.14, w: 0.36, d: 0.34, rx: 0.9 } },
      biped: { leg: 0.44, legW: 0.15, tw: 0.52, th: 0.62, td: 0.36, armW: 0.13, armU: 0.3, armF: 0.29, colors: { body: c.body, arm: c.body, leg: c.body, hand: c.hoof, foot: c.hoof } },
      tail: { len: 0.55, w: 0.035, color: c.body, tuft: c.spot, rx: 0.2 },
      extras: (R, up) => {
        for (const sd of [1, -1]) R.a(R.J.head, box(0.13, 0.04, 0.05, c.horn, { taper: 0.4, taperAxis: 'x' }), [sd * 0.22, 0.4, -0.02], [0, sd > 0 ? 0 : PI, 0.5]);
        R.a(R.J.head, box(0.13, 0.008, 0.11, c.spot), [0.08, 0.402, 0.0], null, false);
        if (!up) { patches(R, R.J.body, 9, c.spot, { faces: ['x+', 'x-', 'y+'], w: 0.65 * 0.92, h: 0.55, d: 1.25, y: 0, z: 0, s: 0.26 }, 7); R.a(R.J.body, facet(0.13, 0.08, 0.15, c.snout, { seed: 2 }), [0, -0.33, -0.25]); }
        else patches(R, R.J.torso, 6, c.spot, { faces: ['x+', 'x-'], w: 0.56, h: 0.5, d: 0.36, y: 0.32, z: 0, s: 0.15 }, 8);
      } });
    R.height = up ? 2.05 : 1.55;
  },
  pig(R, o) {
    const c = col(o, { body: '#EBA5AA', snout: '#D9868E', dark: '#B9606A' });
    R.ol = 0.011;
    const up = mammal(R, o, {
      head: { w: 0.36, h: 0.32, d: 0.3, color: c.body, eye: { x: 0.085, y: 0.22, r: 0.07 }, ears: { type: 'pointy', size: 0.11, x: 0.13, y: 0.29, z: 0.0, color: c.body, inner: c.dark, tilt: 0.5 } },
      quad: { L: 0.85, W: 0.5, H: 0.46, legH: 0.22, legW: 0.11, color: c.body, hoof: c.dark, taper: { x: 0.9, z: 0.9 }, neck: { len: 0.03, w: 0.3, d: 0.3, rx: 0.3 } },
      biped: { leg: 0.3, legW: 0.13, tw: 0.46, th: 0.48, td: 0.36, taper: 0.95, armW: 0.11, armU: 0.22, armF: 0.2, colors: { body: c.body, arm: c.body, leg: c.body, hand: c.dark, foot: c.dark } },
      upHead: 1.05,
      extras: (R, up) => {
        const hd = R.J.head, fz = (up ? 0 : 0.045) + 0.15;
        R.a(hd, cyl(0.085, 0.09, 0.08, c.snout, 8), [0, 0.1, fz + 0.03], [PI / 2, 0, 0]);
        for (const sd of [1, -1]) R.a(hd, box(0.022, 0.035, 0.01, c.dark), [sd * 0.03, 0.1, fz + 0.072], null, false);
        const jaw = R.joint('jaw', hd, 0, 0.045, fz); R.a(jaw, box(0.1, 0.025, 0.06, c.dark, { pivot: 'top' }), [0, 0, 0.0], null, false);
        const tt = R.joint('tail', up ? R.J.hips : R.J.tailBase, 0, 0.02, up ? -0.18 : 0, 0);
        R.a(tt, new THREE.Mesh(new THREE.TorusGeometry(0.035, 0.012, 4, 8, PI * 1.6), mat(c.body)), [0, 0.0, -0.035], [0, PI / 2, 0]);
      } });
    R.height = up ? 1.45 : 0.85;
  },
  sheep(R, o) {
    const c = col(o, { body: '#F4F0E4', face: '#2C2B2E', leg: '#2C2B2E' });
    R.ol = 0.011;
    const up = mammal(R, o, {
      head: { w: 0.22, h: 0.28, d: 0.22, color: c.face, eye: { x: 0.06, y: 0.19, r: 0.065 }, lid: c.face, ears: { type: 'side', size: 0.08, x: 0.1, y: 0.2, color: c.face } },
      quad: { L: 0.78, W: 0.55, H: 0.5, legH: 0.33, legW: 0.07, color: c.body, legColor: c.leg, hoof: c.leg, bodyMesh: facet(0.36, 0.33, 0.5, c.body, { seed: 31, jit: 0.16, detail: 1 }), neck: { len: 0.08, w: 0.18, d: 0.18, rx: 0.45, color: c.face } },
      biped: { leg: 0.32, legW: 0.07, tw: 0.42, th: 0.5, td: 0.36, armW: 0.07, armU: 0.24, armF: 0.22, noTorso: true, colors: { body: c.body, arm: c.leg, leg: c.leg, hand: c.leg, foot: c.leg, pelvis: c.body } },
      neckColor: c.face, upHead: 1.15,
      extras: (R, up) => {
        R.a(R.J.head, facet(0.13, 0.08, 0.12, c.body, { seed: 32, jit: 0.2 }), [0, 0.3, -0.01]);
        if (up) R.a(R.J.torso, facet(0.32, 0.36, 0.27, c.body, { seed: 33, jit: 0.16 }), [0, 0.27, 0]);
        else R.a(R.J.body, facet(0.12, 0.1, 0.1, c.body, { seed: 34, jit: 0.2, detail: 0 }), [0, 0.04, -0.5]);
      } });
    R.height = up ? 1.6 : 1.0;
  },
  goat(R, o) {
    const c = col(o, { body: '#DCD3C2', horn: '#8C7A5E', beard: '#B9AE98', hoof: '#3A332A', snout: '#C9BDA8' });
    R.ol = 0.01;
    const up = mammal(R, o, {
      head: { w: 0.22, h: 0.28, d: 0.24, color: c.body, snout: { w: 0.16, h: 0.12, d: 0.13, color: c.snout, y: 0.07, rx: 0.25 }, nose: '#4A3E32', eye: { x: 0.058, y: 0.19, r: 0.06 }, ears: { type: 'side', size: 0.09, x: 0.1, y: 0.2, color: c.body, tilt: 0.5 } },
      quad: { L: 0.75, W: 0.32, H: 0.36, legH: 0.42, legW: 0.075, color: c.body, hoof: c.hoof, neck: { len: 0.18, w: 0.15, d: 0.16, rx: 0.4 } },
      biped: { leg: 0.36, legW: 0.08, tw: 0.32, th: 0.48, td: 0.24, armW: 0.07, armU: 0.25, armF: 0.24, colors: { body: c.body, arm: c.body, leg: c.body, hand: c.hoof, foot: c.hoof } },
      tail: { len: 0.1, w: 0.04, color: c.body, rx: 2.4 },
      extras: (R) => {
        for (const sd of [1, -1]) { const h = R.joint('horn' + (sd > 0 ? 'L' : 'R'), R.J.head, sd * 0.05, 0.27, 0.0, -0.6, 0, -sd * 0.2); R.a(h, cyl(0.012, 0.03, 0.16, c.horn, 5, { pivot: 'bottom' }), null, [0, 0, 0]); }
        R.a(R.J.jaw, box(0.05, 0.1, 0.04, c.beard, { pivot: 'top', taper: 0.3 }), [0, -0.02, 0.09]);
      } });
    R.height = up ? 1.5 : 1.05;
  },
  rabbit(R, o) {
    const c = col(o, { body: '#CFC6B8', belly: P.white, inner: P.pink, nose: P.pink });
    R.ol = 0.007;
    const up = mammal(R, o, {
      head: { w: 0.2, h: 0.19, d: 0.18, color: c.body, snout: { w: 0.1, h: 0.06, d: 0.05, color: c.belly, y: 0.05 }, nose: c.nose, noseW: 0.5, noseH: 0.4,
        eye: { x: 0.048, y: 0.12, r: 0.05 }, ears: { type: 'long', size: 0.07, x: 0.045, y: 0.17, color: c.body, inner: c.inner, tilt: 0.12 } },
      quad: { L: 0.34, W: 0.24, H: 0.24, legH: 0.08, legW: 0.07, color: c.body, belly: c.belly, upper: 0.5, neck: { len: 0.04, w: 0.12, d: 0.12, rx: 0.3 }, bodyMesh: facet(0.13, 0.13, 0.18, c.body, { seed: 41, jit: 0.06 }) },
      biped: { leg: 0.18, legW: 0.07, footLen: 0.16, tw: 0.2, th: 0.24, td: 0.16, armW: 0.05, armU: 0.12, armF: 0.11, colors: { body: c.body, belly: c.belly, arm: c.body, leg: c.body, hand: c.belly, foot: c.belly } },
      upHead: 1.2,
      extras: (R, up) => { R.a(up ? R.J.hips : R.J.tailBase, sphere(0.05, P.white, 1), [0, 0, up ? -0.09 : 0]); } });
    R.hopper = true;
    R.height = up ? 0.95 : 0.55;
  },
  monkey(R, o) {
    const c = col(o, { body: '#7A5236', face: '#E2B98E', belly: '#C99A6E' });
    R.ol = 0.009;
    const B = bipedBody(R, { leg: 0.2, legW: 0.08, footLen: 0.12, tw: 0.26, th: 0.32, td: 0.18, taper: 1.05, armW: 0.065, armU: 0.24, armF: 0.24, hand: 'mitten', colors: { body: c.body, belly: c.belly, arm: c.body, leg: c.body, hand: c.face, foot: c.face } });
    const hd = mHead(R, R.J.neck, { w: 0.3, h: 0.27, d: 0.24, color: c.body, y: 0.0, scale: 1.3, skull: facet(0.16, 0.145, 0.13, c.body, { seed: 51, jit: 0.05 }),
      snout: { w: 0.16, h: 0.09, d: 0.08, color: c.face, y: 0.07, inset: 0.05 }, nose: '#5A3A22', noseW: 0.25, noseH: 0.25, eye: { x: 0.058, y: 0.17, r: 0.056, inset: 0.0 }, lid: c.face,
      ears: { type: 'round', size: 0.05, x: 0.155, y: 0.11, z: -0.0, color: c.body, inner: c.face } });
    R.a(hd, facet(0.11, 0.08, 0.04, c.face, { seed: 52 }), [0, 0.15, 0.1], null, false);
    tail(R, R.J.hips, { y: -0.05, z: -0.09, len: 0.5, w: 0.03, color: c.body, rx: 1.0, rx2: -1.2 });
    R.height = 0.95;
  },
  gorilla(R, o) {
    const c = col(o, { body: '#2E2F35', chest: '#55565E', face: '#4A4A52', silver: '#8A8C92' });
    R.ol = 0.014;
    bipedBody(R, { leg: 0.36, legW: 0.17, tw: 0.66, th: 0.72, td: 0.44, taper: 1.3, lean: 0.18, armW: 0.17, armU: 0.42, armF: 0.42, hand: 'paw', footLen: 0.24, colors: { body: c.body, belly: c.chest, arm: c.body, leg: c.body, hand: c.face, foot: c.face } });
    R.a(R.J.neck, box(0.22, 0.1, 0.2, c.body, { pivot: 'bottom' }), [0, -0.03, 0.02]);
    mHead(R, R.J.neck, { w: 0.34, h: 0.4, d: 0.3, color: c.body, y: 0.0, z: 0.08, taper: { x: 0.75, z: 0.8 }, snout: { w: 0.26, h: 0.14, d: 0.1, color: c.face, y: 0.1, teeth: 2 }, nose: '#1A1A1E', noseW: 0.5, noseH: 0.3,
      eye: { x: 0.075, y: 0.25, r: 0.068, browT: 0.24 }, lid: c.face, ears: { type: 'round', size: 0.04, x: 0.16, y: 0.22, color: c.face } });
    R.a(R.J.head, box(0.3, 0.05, 0.06, c.body), [0, 0.32, 0.14], null, false);
    R.a(R.J.torso, box(0.5, 0.05, 0.3, c.silver), [0, 0.15, -0.2], null, false);
    R.height = 1.85;
  },
  frog(R, o) {
    const c = col(o, { body: '#6E9C5A', belly: '#D9E0A6', dark: '#4E7A40', mouth: P.redDark });
    R.ol = 0.008;
    const body = R.joint('body', R.mover, 0, 0.0, 0, -0.35);
    R.a(body, facet(0.16, 0.12, 0.17, c.body, { seed: 61 }), [0, 0.12, -0.02]);
    R.a(body, facet(0.12, 0.08, 0.06, c.belly, { seed: 62 }), [0, 0.09, 0.12], null, false);
    const hd = R.joint('head', body, 0, 0.17, 0.06, 0.35);
    R.a(hd, facet(0.14, 0.07, 0.11, c.body, { seed: 63 }), [0, 0.0, 0.03]);
    const jaw = R.joint('jaw', hd, 0, -0.025, -0.04);
    R.a(jaw, facet(0.13, 0.035, 0.1, c.belly, { seed: 64, detail: 0 }), [0, -0.01, 0.08]);
    R.a(jaw, box(0.16, 0.008, 0.1, c.mouth), [0, 0.012, 0.08], null, false);
    const tongue = R.joint('tongue', jaw, 0, 0.02, 0.1);
    R.a(tongue, zbox(0.025, 0.012, 0.08, P.pink), null, null, false); R.a(tongue, sphere(0.02, P.pink, 1), [0, 0, 0.08], null, false);
    addEyes(R, hd, { x: 0.07, y: 0.075, z: 0.03, r: 0.055, lid: c.body, flat: 0.9 });
    for (const sd of [1, -1]) R.a(hd, facet(0.05, 0.04, 0.05, c.body, { seed: 65, detail: 0 }), [sd * 0.07, 0.05, 0.0], null, false);
    for (const [s, sd] of [['L', 1], ['R', -1]]) {
      const sh = R.joint('shoulder' + s, body, sd * 0.1, 0.08, 0.1, 0.35);
      R.a(sh, box(0.035, 0.1, 0.035, c.body, { pivot: 'top' }), null, [0, 0, sd * 0.2]);
      R.a(sh, box(0.06, 0.012, 0.06, c.body), [sd * 0.025, -0.095, 0.02], null, false);
      const hp = R.joint('hip' + s, body, sd * 0.12, 0.07, -0.1, 0.35);
      R.a(hp, zbox(0.06, 0.06, 0.15, c.dark, 0.8), null, [0, sd * 0.4, 0]);
      const kn = R.joint('knee' + s, hp, sd * 0.06, -0.01, 0.14, 0, 0, 0);
      R.a(kn, flipZ(zbox(0.045, 0.045, 0.14, c.body, 0.7)), [0, -0.02, 0], [0.15, -sd * 0.3, 0]);
      R.a(kn, box(0.09, 0.012, 0.08, c.dark, { taper: { x: 1.6, z: 1 }, taperAxis: 'z' }), [sd * 0.03, -0.06, 0.02], null, false);
    }
    R.plan = 'blob'; R.loco = 'hop'; R.height = 0.33;
  },
  octopus(R, o) {
    const c = col(o, { body: '#D9614C', dark: '#B5483A', spot: '#E8957F' });
    R.ol = 0.01;
    const body = R.joint('body', R.mover, 0, 0.28, 0);
    const hd = R.joint('head', body, 0, 0.0, 0);
    R.a(hd, facet(0.25, 0.32, 0.24, c.body, { seed: 71 }), [0, 0.3, -0.04]);
    for (const [x, y] of [[0.12, 0.45], [-0.08, 0.5], [0.0, 0.36]]) R.a(hd, cyl(0.03, 0.03, 0.01, c.spot, 6), [x, y, 0.2 - abs(x) * 0.25 - (y - 0.36) * 0.4], [PI / 2 - 0.3, 0, 0], false);
    addEyes(R, hd, { x: 0.09, y: 0.18, z: 0.19, r: 0.08, lid: c.body });
    const jaw = R.joint('jaw', hd, 0, 0.05, 0.2); R.a(jaw, cyl(0.03, 0.03, 0.03, c.dark, 7), [0, 0, 0], [PI / 2, 0, 0], false);
    R.mouthScale = true;
    for (let i = 0; i < 8; i++) {
      const yaw = new THREE.Group(); yaw.rotation.y = (i + 0.5) / 8 * PI * 2; yaw.position.y = 0.05; body.add(yaw);
      const t = R.joint('t' + i, yaw, 0, 0, 0.1, 0.9);
      R.a(t, zbox(0.09, 0.07, 0.22, c.body, 0.75), null, null, R.ol * 0.7);
      const t2 = R.joint('tb' + i, t, 0, 0, 0.21, -0.5); R.a(t2, zbox(0.068, 0.052, 0.2, c.body, 0.6), null, null, R.ol * 0.7);
      const t3 = R.joint('tc' + i, t2, 0, 0, 0.19, -0.8); R.a(t3, zbox(0.04, 0.032, 0.14, c.body, 0.4), null, null, R.ol * 0.7);
    }
    R.plan = 'blob'; R.loco = 'slide'; R.height = 0.95;
  },
  fish(R, o) {
    const c = col(o, { body: P.salmon, fin: '#E8A33C', belly: '#F2D0A0' });
    R.ol = 0.007;
    swimmer(R, c, { len: 0.34, h: 0.22, w: 0.1, y: 0.55, fin: 0.16, eyeR: 0.06 });
    R.height = 0.8;
  },
  shark(R, o) {
    const c = col(o, { body: '#7C8FA0', fin: '#6A7D8E', belly: '#E8E4D8' });
    R.ol = 0.014;
    swimmer(R, c, { len: 1.3, h: 0.36, w: 0.34, y: 0.75, fin: 0.45, eyeR: 0.09, teeth: true, shark: true });
    R.height = 1.45;
  },

  // ---------------------------------------------------------------- odd ones
  alien(R, o) {
    const c = col(o, { body: '#9DC08B', dark: '#6E9A66', suit: '#B9B9B4' });
    R.ol = 0.008;
    bipedBody(R, { leg: 0.2, legW: 0.06, footLen: 0.1, tw: 0.2, th: 0.26, td: 0.15, taper: 1.0, armW: 0.045, armU: 0.2, armF: 0.2, hand: 'ball', colors: { body: c.suit, arm: c.body, leg: c.suit, hand: c.body, foot: c.dark } });
    R.a(R.J.neck, cyl(0.03, 0.035, 0.08, c.body, 6, { pivot: 'bottom' }), [0, -0.02, 0]);
    const hd = R.joint('head', R.J.neck, 0, 0.05, 0);
    R.a(hd, facet(0.24, 0.22, 0.2, c.body, { seed: 81, jit: 0.05 }), [0, 0.22, 0]);
    R.a(hd, facet(0.11, 0.1, 0.09, c.body, { seed: 82, detail: 0 }), [0, 0.06, 0.06]);
    addEyes(R, hd, { x: 0.09, y: 0.22, z: 0.16, r: 0.085, lid: c.body, pupil: 0.62, yaw: 0.25 });
    const jaw = R.joint('jaw', hd, 0, 0.07, 0.14); R.a(jaw, box(0.06, 0.012, 0.01, P.navy, { pivot: 'top' }), null, null, false);
    R.mouthScale = true;
    for (const sd of [1, -1]) { R.a(hd, cyl(0.006, 0.006, 0.14, c.dark, 4, { pivot: 'bottom' }), [sd * 0.08, 0.38, 0], [0, 0, -sd * 0.35]); R.a(hd, sphere(0.022, P.red, 1), [sd * 0.13, 0.51, 0]); }
    R.a(R.J.torso, cyl(0.04, 0.04, 0.01, P.red, 6), [0, 0.18, 0.08], [PI / 2, 0, 0], false);
    R.height = 1.15;
  },
  robot(R, o) {
    const c = col(o, { body: '#B9B9B4', dark: P.greyDark, panel: P.teal, light: P.red });
    R.ol = 0.012;
    const B = bipedBody(R, { leg: 0.4, legW: 0.13, footLen: 0.22, footH: 0.08, tw: 0.46, th: 0.55, td: 0.32, taper: 1.0, armW: 0.11, armU: 0.3, armF: 0.3, hand: 'clamp', colors: { body: c.body, arm: c.body, leg: c.body, hand: c.dark, foot: c.dark, shin: c.dark } });
    R.a(R.J.torso, box(0.26, 0.2, 0.02, c.panel), [0, 0.3, B.td / 2 + 0.01], null, false);
    for (let i = 0; i < 3; i++) R.a(R.J.torso, box(0.04, 0.04, 0.02, [P.red, P.yellow, P.green][i]), [-0.07 + i * 0.07, 0.3, B.td / 2 + 0.022], null, false);
    R.a(R.J.neck, cyl(0.06, 0.06, 0.08, c.dark, 8, { pivot: 'bottom' }), [0, 0, 0]);
    const hd = R.joint('head', R.J.neck, 0, 0.07, 0);
    R.a(hd, box(0.4, 0.32, 0.32, c.body), [0, 0.16, 0]);
    addEyes(R, hd, { x: 0.09, y: 0.2, z: 0.16, r: 0.075, lid: c.body, flat: 0.6 });
    const jaw = R.joint('jaw', hd, 0, 0.08, 0.15); R.a(jaw, box(0.2, 0.05, 0.03, c.dark, { pivot: 'top' }), null, null, false);
    for (let i = 0; i < 4; i++) R.a(jaw, box(0.008, 0.035, 0.032, c.body), [-0.06 + i * 0.04, -0.025, 0], null, false);
    R.a(hd, cyl(0.01, 0.01, 0.12, c.dark, 4, { pivot: 'bottom' }), [0, 0.32, 0]); R.a(hd, sphere(0.035, c.light, 1), [0, 0.45, 0]);
    for (const sd of [1, -1]) R.a(hd, cyl(0.05, 0.05, 0.04, c.dark, 8), [sd * 0.21, 0.17, 0], [0, 0, PI / 2]);
    R.height = 1.85;
  },
  ghost(R, o) {
    const c = col(o, { body: '#F4F1EA', mouth: P.navy });
    R.ol = 0.012;
    const body = R.joint('body', R.mover, 0, 0.25, 0);
    R.a(body, cyl(0.26, 0.36, 0.95, c.body, 9, { pivot: 'bottom' }), [0, 0.0, 0]);
    const hd = R.joint('head', body, 0, 0.95, 0);
    R.a(hd, new THREE.Mesh(new THREE.SphereGeometry(0.26, 9, 6, 0, PI * 2, 0, PI / 2), mat(c.body)), [0, -0.005, 0]);
    for (let i = 0; i < 9; i++) { const a = i / 9 * PI * 2; R.a(body, cone(0.09, 0.16, c.body, 5), [S(a) * 0.29, -0.06, C(a) * 0.29], [PI, 0, 0], R.ol * 0.7); }
    addEyes(R, hd, { x: 0.1, y: 0.0, z: 0.23, r: 0.085, lid: c.body });
    const jaw = R.joint('jaw', hd, 0, -0.17, 0.27); R.a(jaw, facet(0.05, 0.04, 0.02, c.mouth, { detail: 1 }), null, [-0.25, 0, 0], false);
    R.mouthScale = true;
    for (const [s, sd] of [['L', 1], ['R', -1]]) {
      const sh = R.joint('shoulder' + s, body, sd * 0.29, 0.7, 0, 0, 0, sd * 0.35);
      R.a(sh, box(0.1, 0.32, 0.12, c.body, { pivot: 'top', taper: 0.6 }));
    }
    R.plan = 'blob'; R.loco = 'glide'; R.height = 1.45;
  },
  soja(R, o) { // a living soybean (the "Le burger vegan" short): one big faceted bean is the body and the face, thin arms and legs,
    // the dark hilum on its side; biped rig, so human clips and the walk cycle work; attach costumes to the 'head' joint (the bean)
    const c = col(o, { body: '#E6C878', hilum: '#5A4630', limb: '#CFAE60', foot: '#8C6B3C', mouth: '#4A3220' });
    R.ol = 0.012;
    bipedBody(R, { leg: 0.16, legW: 0.05, footH: 0.04, footLen: 0.12, tw: 0.3, th: 0.1, td: 0.2, taper: 1, armW: 0.045, armU: 0.18, armF: 0.17, hand: 'mitten',
      noTorso: true, noPelvis: true, shY: 2.6, shX: 0.28, colors: { body: c.body, arm: c.limb, leg: c.limb, hand: c.limb, foot: c.foot } });
    const bean = R.joint('head', R.J.torso, 0, 0, 0);
    R.a(bean, facet(0.3, 0.35, 0.26, c.body, { seed: 61, jit: 0.035, detail: 2 }), [0, 0.3, 0]);
    R.a(bean, facet(0.014, 0.085, 0.04, c.hilum, { seed: 62, detail: 1 }), [0.288, 0.3, 0.03], [0, 0, 0.12], false);   // hilum
    addEyes(R, bean, { x: 0.095, y: 0.42, z: 0.215, r: 0.072, lid: c.body });
    const jaw = R.joint('jaw', bean, 0, 0.27, 0.25); R.a(jaw, facet(0.055, 0.022, 0.02, c.mouth, { detail: 0 }), null, null, false);
    R.mouthScale = true;
    R.height = 1.05;
  },
  snowman(R, o) {
    const c = col(o, { body: '#F6F4EE', coal: '#1A1B20', carrot: '#E07A2E', hat: '#17181B', band: P.red, scarf: P.red, stick: P.woodDark });
    R.ol = 0.012;
    const body = R.joint('body', R.mover, 0, 0, 0);
    R.a(body, facet(0.38, 0.34, 0.38, c.body, { seed: 91 }), [0, 0.32, 0]);
    const mid = R.joint('torso', body, 0, 0.62, 0);
    R.a(mid, facet(0.28, 0.26, 0.28, c.body, { seed: 92 }), [0, 0.18, 0]);
    for (const y of [0.1, 0.22, 0.34]) R.a(mid, sphere(0.025, c.coal, 0), [0, y, 0.27 - abs(y - 0.2) * 0.3], null, false);
    R.a(mid, cyl(0.19, 0.22, 0.08, c.scarf, 8), [0, 0.42, 0]);
    R.a(mid, box(0.07, 0.25, 0.03, c.scarf), [0.1, 0.32, 0.2], [0.2, 0, 0.1]);
    const hd = R.joint('head', mid, 0, 0.44, 0);
    R.a(hd, facet(0.2, 0.19, 0.2, c.body, { seed: 93 }), [0, 0.18, 0]);
    addEyes(R, hd, { x: 0.075, y: 0.24, z: 0.16, r: 0.06, lid: c.body });
    R.a(hd, cone(0.03, 0.16, c.carrot, 6, { fwd: true }), [0, 0.18, 0.26]);
    const jaw = R.joint('jaw', hd, 0, 0.1, 0.17);
    for (let i = 0; i < 5; i++) R.a(jaw, sphere(0.014, c.coal, 0), [(i - 2) * 0.03, -abs(i - 2) * -0.008, 0.005], null, false);
    R.a(hd, cyl(0.24, 0.24, 0.02, c.hat, 10), [0, 0.35, 0], [-0.12, 0, 0.05]);
    R.a(hd, cyl(0.15, 0.15, 0.24, c.hat, 10, { pivot: 'bottom' }), [0, 0.35, -0.01], [-0.12, 0, 0.05]);
    R.a(hd, cyl(0.152, 0.152, 0.04, c.band, 10, { pivot: 'bottom' }), [0, 0.37, -0.01], [-0.12, 0, 0.05], false);
    for (const [s, sd] of [['L', 1], ['R', -1]]) {
      const sh = R.joint('shoulder' + s, mid, sd * 0.25, 0.25, 0, 0, 0, sd * 1.0);
      R.a(sh, cyl(0.015, 0.02, 0.4, c.stick, 4, { pivot: 'top' }), null, null, R.ol * 0.6);
      R.a(sh, cyl(0.01, 0.012, 0.12, c.stick, 4, { pivot: 'top' }), [0, -0.28, 0], [0, 0, sd * 0.6], false);
    }
    R.plan = 'blob'; R.loco = 'hop'; R.height = 1.65;
  },
  worm(R, o) { // « Le ver de terre »: a big pink earthworm standing out of the ground — joints seg0..seg8 (seg0 starts 0.15 m under y = 0), a round head
    // with googly eyes, brows and a mouth that opens huge ('gulp' clip), a darker saddle band; o.bowtie adds a little red bow tie under the head (court)
    const c = col(o, { body: '#E79C98', band: '#C66F6C', groove: '#C98480', mouth: '#5A1E22', tongue: '#D9606A' });
    R.ol = 0.008;
    const N = 9, L = o.seg || 0.075, r0 = o.r || 0.058; let parent = R.mover; R.bulges = [];
    for (let i = 0; i < N; i++) {
      const j = R.joint('seg' + i, parent, 0, i === 0 ? -0.15 : L, 0), rr = r0 * (1 - Math.max(0, i - 3) * 0.018);
      R.a(j, cyl(rr * 0.98, rr, L * 1.1, i === 5 || i === 6 ? c.band : c.body, 12, { pivot: 'bottom' }), null, null, R.ol);
      R.a(j, new THREE.Mesh(new THREE.TorusGeometry(rr * 1.0, 0.0045, 4, 14), mat(c.groove)), [0, L * 0.99, 0], [PI / 2, 0, 0], false);
      const b = R.a(j, facet(rr * 1.75, L * 1.1, rr * 1.75, c.body, { seed: 80 + i, jit: 0.04 }), [0, L * 0.5, 0], null, R.ol); b.visible = false; R.bulges.push(b);   // the swallowed lump
      parent = j;
    }
    const hd = R.joint('head', parent, 0, L, 0);
    R.a(hd, facet(r0 * 1.12, r0 * 1.3, r0 * 1.08, c.body, { seed: 71, jit: 0.03, detail: 2 }), [0, r0 * 0.95, 0]);
    addEyes(R, hd, { x: r0 * 0.46, y: r0 * 1.3, z: r0 * 0.86, r: r0 * 0.43, lid: c.body, browY: 1.45, browT: 0.2 });
    const jaw = R.joint('jaw', hd, 0, r0 * 0.6, r0 * 1.02); R.a(jaw, facet(r0 * 0.36, r0 * 0.14, 0.012, c.mouth, { detail: 0 }), null, null, false);
    R.a(jaw, facet(r0 * 0.2, r0 * 0.06, 0.008, c.tongue, { detail: 0 }), [0, -r0 * 0.05, 0.004], null, false);
    if (o.bowtie) { const bt = R.joint('bowtie', parent, 0, L * 0.9, r0 * 0.95); for (const sd of [-1, 1]) R.a(bt, box(0.05, 0.04, 0.012, '#C8322A', { taper: { x: 0.35, z: 1 }, taperAxis: 'x' }), [sd * 0.026, 0, 0], [0, 0, sd * PI / 2], R.ol * 0.6); R.a(bt, box(0.016, 0.02, 0.016, '#A82828'), null, null, R.ol * 0.6); }
    R.mouthScale = true; R.plan = 'worm'; R.height = N * L - 0.15 + r0 * 2.2;
    R.post = (q, cl, t, p) => { const g = q.gulp; R.bulges.forEach((b, i) => { b.visible = g != null && Math.abs(g - (N - 1 - i)) < 0.75; }); };
  },
  avocat(R, o) { // « Le ver de terre »: the lawyer is an avocado — a half avocado standing (the cut face forward: pale flesh with a green rim, the brown stone
    // as a belly), dark skin round the back, thin legs; a black lawyer's robe (back, shoulders, sleeves), the white bands (rabat) under the mouth, the épitoge
    const c = col(o, { skin: '#2E4620', rim: '#94C450', flesh: '#E2EA9A', stone: '#7A4A2A', limb: '#2E4620', robe: '#17181C', white: '#F4F1EA', mouth: '#3A2A18' });
    R.ol = 0.01;
    bipedBody(R, { leg: 0.11, legW: 0.035, footH: 0.035, footLen: 0.09, tw: 0.24, th: 0.08, td: 0.16, taper: 1, armW: 0.034, armU: 0.13, armF: 0.13, hand: 'mitten', noTorso: true, noPelvis: true, shY: 2.6, shX: 0.17,
      colors: { body: c.skin, arm: c.robe, leg: c.limb, hand: c.limb, foot: '#17181C' } });
    const av = R.joint('head', R.J.torso, 0, -0.02, 0);
    const hull = pts => { pts = pts.slice().sort((a, b) => a[0] - b[0] || a[1] - b[1]); const cr = (o2, a, b) => (a[0] - o2[0]) * (b[1] - o2[1]) - (a[1] - o2[1]) * (b[0] - o2[0]); const lo = [], up = [];
      for (const p2 of pts) { while (lo.length >= 2 && cr(lo[lo.length - 2], lo[lo.length - 1], p2) <= 0) lo.pop(); lo.push(p2); } for (const p2 of pts.slice().reverse()) { while (up.length >= 2 && cr(up[up.length - 2], up[up.length - 1], p2) <= 0) up.pop(); up.push(p2); } return lo.slice(0, -1).concat(up.slice(0, -1)); };
    const pear = k => { const pts = []; for (let i = 0; i < 28; i++) { const a = i / 28 * 2 * PI; pts.push([Math.cos(a) * 0.135 * k, 0.14 + Math.sin(a) * 0.135 * k], [Math.cos(a) * 0.08 * k, 0.36 + Math.sin(a) * 0.08 * k]); } return new THREE.Shape(hull(pts).map(([x, y]) => new THREE.Vector2(x, y))); };
    const eg = new THREE.ExtrudeGeometry(pear(1), { depth: 0.08, bevelEnabled: true, bevelThickness: 0.03, bevelSize: 0.02, bevelSegments: 2, curveSegments: 6 }); eg.translate(0, 0, -0.04);
    const body = new THREE.Mesh(eg, [mat(c.rim), mat(c.skin)]); body.castShadow = body.receiveShadow = true; R.a(av, body, [0, 0, 0]);
    const fg = new THREE.ShapeGeometry(pear(0.86)); fg.translate(0, 0.022, 0); R.a(av, new THREE.Mesh(fg, mat(c.flesh)), [0, 0, 0.0712], null, false);   // the pale flesh inside the green rim
    R.a(av, facet(0.072, 0.078, 0.05, c.stone, { seed: 64, jit: 0.04, detail: 2 }), [0, 0.13, 0.068]);
    R.a(av, facet(0.02, 0.014, 0.008, '#B07A52', { detail: 0 }), [-0.025, 0.165, 0.112], null, false);   // shine on the stone
    addEyes(R, av, { x: 0.042, y: 0.335, z: 0.08, r: 0.034, lid: c.flesh, browY: 1.5 });
    const jaw = R.joint('jaw', av, 0, 0.262, 0.078); R.a(jaw, facet(0.026, 0.01, 0.008, c.mouth, { detail: 0 }), null, null, false); R.mouthScale = true;
    // the robe: a back panel and shoulders round the skin side, and the white rabat with its two bands; the épitoge on the left shoulder
    R.a(av, box(0.3, 0.34, 0.025, c.robe, { taper: { x: 0.8, z: 1 } }), [0, 0.18, -0.085], [0.05, 0, 0]);
    for (const sd of [-1, 1]) R.a(av, box(0.07, 0.2, 0.15, c.robe, { taper: { x: 0.7, z: 0.8 } }), [sd * 0.12, 0.22, -0.02], [0, 0, sd * 0.28]);
    R.a(av, box(0.075, 0.016, 0.014, c.white), [0, 0.235, 0.088], null, R.ol * 0.5);
    for (const sd of [-1, 1]) R.a(av, box(0.022, 0.05, 0.008, c.white), [sd * 0.014, 0.205, 0.094], [0, 0, sd * 0.06], R.ol * 0.5);
    R.a(av, box(0.045, 0.16, 0.018, c.robe), [0.135, 0.26, 0.04], [0.15, 0, -0.35]); R.a(av, box(0.05, 0.035, 0.022, c.white), [0.16, 0.19, 0.06], [0.15, 0, -0.35], R.ol * 0.5);
    R.height = 0.72;
  },
  'banana-man'(R, o) {
    const c = col(o, { body: '#E8C34A', dark: '#B8932A', tip: '#5A4022', limb: '#17181B' });
    R.ol = 0.01;
    bipedBody(R, { leg: 0.36, legW: 0.035, footLen: 0.16, footH: 0.06, tw: 0.2, th: 0.5, td: 0.2, armW: 0.03, armU: 0.25, armF: 0.24, hand: 'glove', noTorso: true, noPelvis: true, shX: 0.14, shY: 0.6,
      colors: { body: c.body, arm: c.limb, leg: c.limb, hand: P.white, foot: P.red } });
    const T = R.J.torso;
    // curved banana: stacked tapered segments, bending forward toward the top
    const segs = [[0.16, 0.12, 0.02, -0.1], [0.2, 0.22, 0.0, -0.04], [0.21, 0.26, 0.0, 0.03]];
    let y = -0.12;
    R.a(T, box(0.07, 0.07, 0.07, c.tip, { taper: 0.6 }), [0, y - 0.02, -0.04], [-0.25, 0, 0]);
    for (const [w, h, z, rx] of segs) { R.a(T, box(w, h, w * 0.9, c.body, { pivot: 'bottom', taper: { x: 1.1, z: 1.1 } }), [0, y, z - 0.03], [rx, 0, 0]); y += h * 0.97; }
    const hd = R.joint('head', R.J.neck, 0, -0.01, 0);
    R.a(hd, box(0.23, 0.28, 0.21, c.body, { pivot: 'bottom', taper: { x: 0.85, z: 0.85 } }), [0, 0, 0.0], [0.08, 0, 0]);
    R.a(hd, box(0.18, 0.18, 0.17, c.body, { pivot: 'bottom', taper: { x: 0.45, z: 0.45 } }), [0, 0.27, 0.03], [0.25, 0, 0]);
    R.a(hd, box(0.06, 0.08, 0.06, c.tip, { pivot: 'bottom', taper: 0.8 }), [0, 0.43, 0.08], [0.45, 0, 0]);
    for (const sd of [1, -1]) R.a(hd, box(0.006, 0.42, 0.006, c.dark), [sd * 0.105, 0.14, 0.088], [0.08, 0, 0], false);
    addEyes(R, hd, { x: 0.05, y: 0.19, z: 0.115, r: 0.05, lid: c.body });
    R.a(hd, box(0.08, 0.012, 0.01, P.redDark), [0, 0.07, 0.112], null, false);
    const jaw = R.joint('jaw', hd, 0, 0.075, 0.105); R.a(jaw, box(0.07, 0.025, 0.012, c.body, { pivot: 'top' }), [0, 0, 0.005], null, false);
    R.height = 1.65;
  },
};

function antHead(R, hd, c, s) {
  R.a(hd, facet(0.15 * s, 0.14 * s, 0.13 * s, c.body, { seed: 21, jit: 0.06 }), [0, 0.12 * s, 0.02]);
  R.a(hd, facet(0.05 * s, 0.035 * s, 0.03 * s, c.shine, { seed: 22, detail: 0 }), [0.05 * s, 0.22 * s, 0.1 * s], null, false);
  addEyes(R, hd, { x: 0.068 * s, y: 0.15 * s, z: 0.12 * s, r: 0.068 * s, lid: c.body, browColor: c.red });
  const jaw = R.joint('jaw', hd, 0, 0.05 * s, 0.11 * s);
  for (const sd of [1, -1]) {
    const m = R.a(jaw, zbox(0.04 * s, 0.03 * s, 0.09 * s, c.red, 0.6), [sd * 0.05 * s, 0, -0.01], [0.5, sd * 0.35, 0], R.ol * 0.7);
    R.a(m, zbox(0.03 * s, 0.025 * s, 0.07 * s, c.red, 0.3), [0, 0, 0.085 * s], [0, -sd * 1.2, 0], R.ol * 0.7);
  }
  R.a(jaw, box(0.06 * s, 0.01, 0.03 * s, P.redDark), [0, 0.0, 0.01], null, false);
  antennae(R, hd, { x: 0.05 * s, y: 0.24 * s, z: 0.06 * s, w: 0.011 * s, l1: 0.16 * s, l2: 0.17 * s, color: c.leg, tip: c.red });
}

function horseLike(R, o, c, zebra) {
  R.ol = 0.012;
  const head = { w: 0.26, h: 0.34, d: 0.26, color: c.body, taper: { x: 0.85, z: 0.85 },
    snout: { w: 0.21, h: 0.25, d: 0.15, color: c.muzzle, y: 0.03, rx: 0.15, jh: 0.3, inset: 0.04, taper: { x: 0.95, z: 0.95 } }, nose: '#141414', noseW: 0.6, noseH: 0.14,
    eye: { x: 0.07, y: 0.25, r: 0.066 }, ears: { type: 'pointy', size: 0.08, x: 0.08, y: 0.33, z: -0.04, color: c.body, inner: zebra ? P.grey : c.muzzle, tilt: 0.1 } };
  const up = mammal(R, o, { head,
    quad: { L: 1.3, W: 0.44, H: 0.48, legH: zebra ? 0.72 : 0.82, legW: 0.1, color: c.body, hoof: c.hoof, neck: { len: 0.45, w: 0.18, d: 0.28, rx: 0.5, y: 0.25 } },
    biped: { leg: 0.46, legW: 0.12, tw: 0.42, th: 0.62, td: 0.28, taper: 1.15, armW: 0.1, armU: 0.31, armF: 0.3, hand: 'paw', colors: { body: c.body, arm: c.body, leg: c.body, hand: c.hoof, foot: c.hoof } },
    upHead: 1.15, upY: 0.04,
    tail: { len: 0.55, w: 0.04, color: c.mane, tuft: c.mane, rx: 0.35 },
    extras: (R, up) => {
      const hd = R.J.head;
      R.a(hd, box(0.045, 0.09, 0.12, c.mane, { taper: { x: 1, z: 0.6 } }), [0, 0.37, -0.02], [0.5, 0, 0]); // forelock
      if (c.blaze) R.a(hd, box(0.05, 0.12, 0.01, c.blaze, { taper: { x: 0.6, z: 1 } }), [0, 0.12, 0.135], null, false);
      if (zebra) stripes(R, hd, [0.26 * 0.93, 0.34, 0.26 * 0.93], [0, 0.17, 0], 'y', 4, c.stripe, { th: 0.028, from: 0.3, to: 0.95, tx: 0.88 });
      if (!up) {
        const nk = R.J.neck; R.a(nk, box(0.05, 0.6, 0.1, c.mane), [0, 0.25, -0.15], null, R.ol * 0.6);
        if (zebra) {
          stripes(R, R.J.body, [0.44 * 0.93, 0.48, 1.3], [0, 0, 0], 'z', 9, c.stripe, { th: 0.045, from: 0.08, to: 0.94 });
          stripes(R, nk, [0.19, 0.5, 0.29], [0, 0.22, 0], 'y', 4, c.stripe, { th: 0.04 });
          for (const n of ['FL', 'FR', 'BL', 'BR']) stripes(R, R.J['leg' + n], [0.105, 0.4, 0.11], [0, -0.2, 0], 'y', 3, c.stripe, { th: 0.03 });
        }
      } else {
        R.a(R.J.neck, box(0.05, 0.2, 0.12, c.mane), [0, 0.06, -0.1], null, R.ol * 0.6);
        if (zebra && !['suit', 'robe'].includes(o.clothes)) {
          stripes(R, R.J.torso, [0.42 * 1.08, 0.62, 0.28], [0, 0.31, 0], 'y', 5, c.stripe, { th: 0.04, from: 0.1, to: 0.9, tx: 1.15 });
          for (const s of ['L', 'R']) { stripes(R, R.J['shoulder' + s], [0.1, 0.3, 0.1], [0, -0.15, 0], 'y', 3, c.stripe, { th: 0.03 }); stripes(R, R.J['hip' + s], [0.12, 0.42, 0.13], [0, -0.2, 0], 'y', 3, c.stripe, { th: 0.03 }); stripes(R, R.J['knee' + s], [0.11, 0.42, 0.12], [0, -0.2, 0], 'y', 3, c.stripe, { th: 0.03 }); }
        }
      }
    } });
  R.height = up ? 2.05 : (zebra ? 1.75 : 1.85);
}

function swimmer(R, c, o) {
  const { len, h, w } = o;
  const body = R.joint('body', R.mover, 0, o.y, 0);
  R.a(body, facet(w, h, len * 0.55, c.body, { seed: 101, jit: 0.04 }), [0, 0, 0]);
  R.a(body, facet(w * 0.85, h * 0.55, len * 0.45, c.belly, { seed: 102, jit: 0.04 }), [0, -h * 0.42, len * 0.03], null, false);
  const hd = R.joint('head', body, 0, 0, len * 0.3);
  const er = o.eyeR;
  addEyes(R, hd, { x: w * 0.5, y: h * 0.42, z: len * 0.2, r: er, lid: c.body, yaw: 0.3 });
  const jaw = R.joint('jaw', hd, 0, -h * 0.25, len * 0.12, 0);
  R.a(jaw, facet(w * 0.6, h * 0.14, len * 0.12, c.belly, { seed: 103, detail: 0 }), [0, -h * 0.05, len * 0.08]);
  R.a(jaw, box(w * 0.7, 0.01, len * 0.14, P.redDark), [0, 0.01, len * 0.08], null, false);
  if (o.teeth) for (let i = 0; i < 5; i++) for (const sd of [1, -1]) R.a(hd, cone(0.016, 0.05, P.white, 4), [sd * w * (0.15 + i * 0.07), -h * 0.27, len * (0.26 - i * 0.025)], [PI, 0, 0], false);
  // fins
  R.a(body, box(0.012 + w * 0.05, o.fin * (o.shark ? 1.1 : 0.6), len * 0.32, c.fin, { pivot: 'bottom', taper: { x: 1, z: 0.15 } }), [0, h * 0.85, -len * 0.05], [-0.35, 0, 0]);
  for (const [s, sd] of [['L', 1], ['R', -1]]) {
    const f = R.joint('fin' + s, body, sd * w * 0.8, -h * 0.35, len * 0.15, 0, 0, sd * 0.8);
    R.a(f, box(0.012, o.fin * 0.6, len * 0.18, c.fin, { pivot: 'top', taper: { x: 1, z: 0.4 } }), null, [0.5, 0, 0]);
  }
  const tl = R.joint('tail', body, 0, 0, -len * 0.48);
  R.a(tl, facet(w * 0.55, h * 0.5, len * 0.3, c.body, { seed: 104, jit: 0.04 }), [0, 0, -len * 0.18]);
  const fin = R.joint('tailFin', tl, 0, 0, -len * 0.42);
  for (const sd of [1, -1]) R.a(fin, box(0.012 + w * 0.04, o.fin * (o.shark ? 1.1 : 0.9), len * 0.22, c.fin, { pivot: 'bottom', taper: { x: 1, z: 0.25 } }), [0, 0, 0], [PI / 2 + sd * (PI / 2 - 0.65) + PI, 0, 0]);
  if (o.shark) for (let i = 0; i < 3; i++) for (const sd of [1, -1]) R.a(body, box(0.006, h * 0.4, 0.008, c.fin), [sd * w * 0.86, h * 0.05, len * (0.2 - i * 0.05)], null, false);
  R.plan = 'swim';
}

// ---------------------------------------------------------------- the clips --
const sym = (n, v) => ({ [n + 'L']: v, [n + 'R']: [v[0], -v[1], -v[2]] });
const fwave = (t, f) => S(t * 2 * PI * f);

function bipedPose(c, t, p, R) {
  let q;
  switch (c) {
    case 'idle': case 'grow': q = HCLIPS.idle(t); break;
    case 'sleep': q = { ...HCLIPS.stand(), head: [0.45 + 0.04 * S(t * 1.3), 0, 0.12], torso: [0.08 + 0.015 * S(t * 1.3), 0, 0], root: { y: 0.004 * S(t * 1.3) }, expr: 'closed', noBlink: true }; break;
    case 'angry': {
      const P = t * 2 * PI * 2.4, a = max(0, S(P)), b = max(0, -S(P));
      q = { hipL: [-0.6 * a, 0, 0], kneeL: [1.1 * a, 0, 0], hipR: [-0.6 * b, 0, 0], kneeR: [1.1 * b, 0, 0],
        ...sym('shoulder', [-0.2, 0, 0.55 + 0.2 * S(t * 24)]), ...sym('elbow', [-2.0, 0, 0]),
        torso: [-0.06, 0, 0.05 * S(P)], head: [-0.12, 0, 0.05 * S(t * 24)], root: { y: 0.025 * abs(S(P)), x: 0.01 * S(t * 47) }, expr: 'angry' }; break;
    }
    case 'eat': q = { ...HCLIPS.idle(t), shoulderR: [-0.75, 0, -0.2], elbowR: [-1.9 + 0.3 * S(t * 7), 0, 0], shoulderL: [-0.55, 0, 0.1], elbowL: [-1.3, 0, 0], head: [0.06 * S(t * 7), 0, 0], jaw: [0.3 * abs(S(t * 7)), 0, 0] }; break;
    case 'hop': { const k = abs(S(t * PI * 1.7)); q = { root: { y: 0.28 * k }, ...sym('hip', [-0.5 * (1 - k), 0, 0]), ...sym('knee', [0.9 * (1 - k), 0, 0]), ...sym('shoulder', [0, 0, 0.4 + 1.6 * k]), ...sym('elbow', [0, 0, 0.3]), head: [-0.1 * k, 0, 0] }; break; }
    case 'fly': { const f = fwave(t, 3); q = { root: { y: 0.18 + 0.05 * f }, ...sym('shoulder', [0, 0, 1.3 + 0.9 * f]), ...sym('elbow', [0, 0, 0.2]), hipL: [0.15 + 0.2 * S(t * 9), 0, 0], hipR: [0.15 - 0.2 * S(t * 9), 0, 0], ...sym('knee', [0.4, 0, 0]), head: [-0.15, 0, 0], expr: 'surprised' }; break; }
    case 'talk': q = { ...HCLIPS.talk(t) }; break;
    case 'celebrate': q = { ...HCLIPS.celebrate(t), expr: 'happy' }; break;
    case 'flee': q = { ...HCLIPS.flee(t), expr: 'scared' }; break;
    default: q = { ...(HCLIPS[c] || HCLIPS.idle)(t, p) };
  }
  const ls = R.legScale, hs = (R.height || 1.95) / 1.95;
  if (q.root) q.root = { ...q.root, y: (q.root.y || 0) * ls, x: (q.root.x || 0) * hs, z: (q.root.z || 0) * hs };
  if (!q.tail) q.tail = [0, 0, 0.25 * S(t * (c === 'walk' || c === 'run' || c === 'flee' ? 6 : 1.8))];
  return q;
}

function quadPose(c, t, p, R) {
  const Q = R.Q, q = { root: {} }, fs = 1 / Math.sqrt(Q.s);
  const legs = (fl, fr, bl, br, k = [0, 0, 0, 0]) => Object.assign(q, { legFL: [fl, 0, 0], legFR: [fr, 0, 0], legBL: [bl, 0, 0], legBR: [br, 0, 0], kneeFL: [k[0], 0, 0], kneeFR: [k[1], 0, 0], kneeBL: [k[2], 0, 0], kneeBR: [k[3], 0, 0] });
  const wag = (a, f) => { q.tail = [0, 0, a * S(t * f)]; };
  if (R.hopper && (c === 'walk' || c === 'run' || c === 'flee')) c = c === 'walk' ? 'hop' : 'hopfast';
  switch (c) {
    case 'walk': {
      const P = t * 2 * PI * (p.freq ?? 1.7 * fs), a = 0.36;
      legs(a * S(P), -a * S(P), -a * S(P), a * S(P), [0.75 * max(0, -C(P)), 0.75 * max(0, C(P)), 0.45 * max(0, C(P)), 0.45 * max(0, -C(P))]);
      q.root.y = 0.012 * Q.s * abs(S(P)); q.neck = [0.05 * S(2 * P), 0, 0]; q.head = [0, 0.05 * S(P), 0]; wag(0.25, 5); break;
    }
    case 'run': case 'flee': {
      const P = t * 2 * PI * (p.freq ?? (c === 'flee' ? 3.4 : 2.7) * fs), a = 0.68;
      legs(a * S(P), a * S(P + 0.5), a * S(P + PI), a * S(P + PI + 0.5), [1.1 * max(0, -C(P)), 1.1 * max(0, -C(P + 0.5)), 0.7 * max(0, -C(P + PI)), 0.7 * max(0, -C(P + PI + 0.5))]);
      q.body = [0.1 * S(P + PI / 2), 0, 0]; q.root.y = 0.06 * Q.s * max(0, S(P - 0.6));
      q.neck = [-0.15 + 0.08 * S(P), 0, 0]; q.head = [c === 'flee' ? -0.25 : -0.1, 0, 0]; q.tail = [0.7, 0, 0.2 * S(P)];
      if (c === 'flee') { q.expr = 'scared'; q.earL = [0.6, 0, 0]; q.earR = [0.6, 0, 0]; } break;
    }
    case 'hop': case 'hopfast': case 'celebrate': {
      const f = c === 'hopfast' ? 2.6 : c === 'celebrate' ? 1.9 : 1.6, k = abs(S(t * PI * f));
      q.root.y = (R.hopper ? 0.18 : 0.22) * Q.s * k; legs(-0.5 * k, -0.5 * k, 0.6 * k, 0.6 * k);
      q.body = [-0.15 * k, 0, 0]; q.head = [-0.15 * k, 0, 0];
      if (c === 'celebrate') { q.expr = 'happy'; wag(0.7, 18); q.head = [-0.3, 0.25 * S(t * 6), 0]; q.jaw = [0.3, 0, 0]; } else wag(0.3, 4);
      break;
    }
    case 'sit': {
      const a = 0.55, sa = S(a), ca = C(a);
      const rumpY = Q.legH + Q.H / 2 - (Q.L / 2) * sa - (Q.H / 2) * ca;
      q.root.y = -rumpY + 0.02; q.body = [-a, 0, 0];
      // front legs: vertical, splayed forward if the shoulder is too low
      const hipY = Q.bodyY + Q.top * ca + Q.lz * sa - rumpY;
      const fa = Q.len > hipY ? Math.acos(min(1, hipY / Q.len)) : 0;
      legs(a - fa, a - fa, a - 1.45, a - 1.45); q.kneeFL = q.kneeFR = [fa * 0.0, 0, 0];
      q.neck = [0.1 * S(t), 0, 0]; q.head = [a * 0.6, 0.15 * S(t * 0.5), 0]; wag(0.3, 2); break;
    }
    case 'sleep': {
      q.root.y = -Q.legH + 0.02 * Q.s + 0.004 * S(t * 1.4); legs(-1.45, -1.45, -1.45, -1.45);
      q.neck = [0.55, 0, 0]; q.head = [0.4, 0.3, 0.15]; q.tail = [-0.4, 0, 0.6]; q.expr = 'closed'; q.noBlink = true;
      q.scl = { body: [1, 1 + 0.02 * S(t * 1.4), 1] }; break;
    }
    case 'angry': {
      const P = t * 2 * PI * 2.4;
      legs(-0.55 * max(0, S(P)), -0.55 * max(0, -S(P)), 0, 0, [0.8 * max(0, S(P)), 0.8 * max(0, -S(P)), 0, 0]);
      q.neck = [0.3, 0, 0]; q.head = [-0.25, 0.06 * S(t * 30), 0]; q.root.x = 0.01 * Q.s * S(t * 45); q.root.y = 0.01 * Q.s * abs(S(P)); wag(0.6, 20); q.expr = 'angry'; q.jaw = [0.15 + 0.1 * S(t * 20), 0, 0]; break;
    }
    case 'eat': case 'peck': {
      q.body = [0.18, 0, 0]; legs(-0.18, -0.18, -0.18, -0.18); q.root.y = -0.02 * Q.s;
      q.neck = [R.eatNeck ?? 1.0, 0, 0]; q.head = [0.5, 0, 0]; q.jaw = [0.25 * abs(S(t * 8)), 0, 0]; wag(0.2, 3); break;
    }
    case 'talk': {
      q.root.y = 0.004 * S(t * 2.4); q.neck = [0.04 * S(t * 3), 0, 0]; q.head = [-0.08 + 0.06 * S(t * 7), 0.15 * S(t * 1.1), 0]; wag(0.3, 2);
      if (R.J.trunk0) { q.trunk0 = [-0.4 - 0.2 * S(t * 4), 0, 0]; q.trunk1 = [-0.4, 0, 0]; q.trunk2 = [-0.5, 0, 0]; } break;
    }
    case 'point': { q.head = [-0.1, 0.5, 0]; q.neck = [-0.1, 0, 0]; legs(-0.5 + 0.05 * S(t * 3), 0, 0, 0); wag(0.3, 2); break; }
    default: { // idle
      q.root.y = 0.004 * S(t * 2.4); q.neck = [0.03 * S(t * 0.8), 0, 0]; q.head = [0.04 * S(t * 0.6), 0.18 * S(t * 0.45), 0.05 * S(t * 0.7)]; wag(0.3, 1.6);
      q.scl = { body: [1, 1 + 0.012 * S(t * 2.4), 1] };
    }
  }
  return q;
}

function birdPose(c, t, p, R) {
  const B = R.Bd, q = { root: {} }, s = B.s;
  const wings = a => { q.wingL = [0, 0, a]; q.wingR = [0, 0, -a]; };
  const legs = (l, r) => { q.hipL = [l, 0, 0]; q.hipR = [r, 0, 0]; };
  const lowered = () => { q.root.y = -B.ll * 0.85; legs(-1.45, -1.45); };
  switch (c) {
    case 'walk': case 'run': case 'carry': {
      const f = (c === 'run' ? 3.6 : 2.2) / Math.sqrt(s), P = t * 2 * PI * f, a = c === 'run' ? 0.75 : 0.5;
      legs(a * S(P), -a * S(P)); q.body = [c === 'run' ? 0.2 : 0, 0, B.waddle * S(P)];
      const saw = ((t * f * 2) % 1); q.pos = { neck: [0, 0, B.upright ? 0 : (saw < 0.5 ? saw : 1 - saw) * 0.12 * B.by] };
      q.root.y = 0.012 * s * abs(S(P)) * (B.upright ? 2 : 1);
      if (c === 'run') wings(0.4 + 0.15 * S(P * 2)); break;
    }
    case 'flee': {
      const P = t * 2 * PI * 4.2 / Math.sqrt(s); legs(0.8 * S(P), -0.8 * S(P)); wings(1.3 + 0.8 * S(t * 2 * PI * 7));
      q.body = [0.15, 0, B.waddle * S(P)]; q.root.y = 0.03 * s * abs(S(P)); q.head = [-0.2, 0, 0]; q.expr = 'scared'; break;
    }
    case 'fly': {
      if (B.upright) { // can't fly: frantic flapping hops (penguin, owl hops are fine)
        const k = abs(S(t * PI * 3)); wings(1.4 + 0.8 * S(t * 2 * PI * 7)); q.root.y = (R.name === 'owl' ? 0.4 : 0.08) * s * (R.name === 'owl' ? 1 : k); legs(0.3 * k, 0.3 * k); break;
      }
      const f = B.flapF / Math.sqrt(s); wings(0.9 + 1.1 * S(t * 2 * PI * f)); legs(1.2, 1.2);
      q.body = [0.12, 0, 0]; q.root.y = (p.alt ?? B.alt) + 0.03 * s * S(t * 2 * PI * f - 1); q.tail = [-0.15, 0, 0]; break;
    }
    case 'hop': { const k = abs(S(t * PI * 2.2)); q.root.y = 0.12 * s * k; wings(0.35 * k); legs(-0.35 * k, -0.35 * k); break; }
    case 'peck': case 'eat': {
      const k = Math.pow(max(0, S(t * 2 * PI * 1.6)), 3);
      q.body = [(B.upright ? 0.35 : 0.65) * k, 0, 0]; q.neck = [(B.upright ? 0.4 : 0.6) * k, 0, 0]; q.head = [0.3 * k, 0, 0]; q.jaw = [0.3 * k, 0, 0]; q.tail = [-0.4 * k, 0, 0]; break;
    }
    case 'sit': lowered(); q.head = [0, 0.3 * S(Math.floor(t * 1.1) * 2.3), 0]; q.scl = { body: [1.06, 1, 1] }; break;
    case 'talk': q.jaw = [0.5 * abs(S(t * 12)), 0, 0]; q.head = [-0.1 + 0.1 * S(t * 6), 0.2 * S(t * 1.3), 0]; wings(0.15 + 0.15 * abs(S(t * 3))); break;
    case 'celebrate': { const k = abs(S(t * PI * 2)); q.root.y = 0.15 * s * k; wings(1.9 + 0.5 * S(t * 2 * PI * 4)); q.head = [-0.3, 0, 0]; q.jaw = [0.4, 0, 0]; q.expr = 'happy'; break; }
    case 'sleep': lowered(); q.neck = [0.45, 0, 0]; q.head = [0.55, 0.6, 0.25]; q.expr = 'closed'; q.noBlink = true; q.scl = { body: [1.06, 1 + 0.03 * S(t * 1.5), 1] }; break;
    case 'angry': {
      const P = t * 2 * PI * 2.6; wings(0.9 + 0.25 * S(t * 30)); q.body = [0.25, 0, 0]; q.head = [-0.25, 0, 0]; legs(-0.4 * max(0, S(P)), -0.4 * max(0, -S(P)));
      q.root.x = 0.006 * s * S(t * 45); q.jaw = [0.35 + 0.1 * S(t * 25), 0, 0]; q.expr = 'angry'; q.scl = { body: [1.12, 1.12, 1.05] }; break;
    }
    case 'point': q.wingR = [0, 1.1, -1.4]; q.head = [0, -0.25, 0]; q.jaw = [0.2 * abs(S(t * 8)), 0, 0]; break;
    default: { // idle: jerky bird head
      const st = Math.floor(t * 1.4); q.head = [0.08 * S(st * 3.1), 0.4 * S(st * 2.1), 0.12 * S(st * 1.3)]; q.tail = [0.06 * S(t * 2), 0, 0]; q.root.y = 0.002 * S(t * 3);
      q.scl = { body: [1, 1 + 0.02 * S(t * 3), 1] };
    }
  }
  return q;
}

function legsPose(c, t, p, R) { // spiders / crawling ants
  const q = { root: {} }, n = R.nLegs;
  const gait = (f, a, lift) => {
    const P = t * 2 * PI * f;
    for (let k = 0; k < n; k++) { const g = ((k >> 1) + (k & 1)) % 2 ? PI : 0; q['leg' + k] = [-lift * max(0, S(P + g)), R.legSide[k] * a * C(P + g), 0]; }
    q.root.y = 0.006 * abs(S(2 * P)); q.body = [0, 0.04 * S(P), 0];
  };
  switch (c) {
    case 'walk': case 'carry': gait(2.2, 0.28, 0.35); break;
    case 'run': gait(4, 0.35, 0.45); break;
    case 'flee': gait(5, 0.38, 0.5); q.expr = 'scared'; break;
    case 'hop': case 'fly': { const k = abs(S(t * PI * 2)); q.root.y = 0.18 * k; for (let i = 0; i < n; i++) q['knee' + i] = [-0.5 * k, 0, 0]; break; }
    case 'angry': case 'celebrate': case 'point': {
      q.body = [-0.35, 0, 0]; q.root.y = 0.05;
      for (const k of [0, 1]) q['leg' + k] = [-1.2 + 0.4 * S(t * (c === 'angry' ? 18 : 9) + k * PI), R.legSide[k] * 0.3, 0];
      if (c === 'point') q.leg0 = [-0.6, 0, 0];
      q.expr = c === 'angry' ? 'angry' : c === 'celebrate' ? 'happy' : undefined; q.jaw = [0.3 * abs(S(t * 10)), 0, 0]; break;
    }
    case 'sleep': case 'sit': { q.root.y = -0.06; for (let i = 0; i < n; i++) { q['leg' + i] = [-0.3, 0, 0]; q['knee' + i] = [0.4, 0, 0]; } if (c === 'sleep') { q.expr = 'closed'; q.noBlink = true; } break; }
    case 'eat': case 'peck': q.body = [0.15, 0, 0]; q.leg0 = [-0.9, 0.5, 0]; q.leg1 = [-0.9, -0.5, 0]; q.jaw = [0.4 * abs(S(t * 9)), 0, 0]; break;
    case 'talk': q.jaw = [0.4 * abs(S(t * 11)), 0, 0]; q.head = [0.08 * S(t * 6), 0.1 * S(t * 1.5), 0]; q.leg0 = [-0.5 - 0.3 * abs(S(t * 3)), 0, 0]; break;
    default: q.root.y = 0.004 * S(t * 2); for (let i = 0; i < n; i++) q['leg' + i] = [-0.05 * max(0, S(t * 3 + i * 1.3)), 0, 0];
  }
  if (R.J.antL) { q.antL = [0.15 * S(t * 3.2), 0, 0.1 * S(t * 2.1)]; q.antR = [0.15 * S(t * 2.9 + 1), 0, -0.1 * S(t * 2.4)]; }
  return q;
}

function flyerPose(c, t, p, R) { // bee
  const q = { root: {} };
  let buzz = 1, f = 11;
  switch (c) {
    case 'walk': case 'fly': case 'carry': q.body = [0.25, 0, 0]; q.root.y = 0.04 * S(t * 4); break;
    case 'run': case 'flee': q.body = [0.45, 0, 0.1 * S(t * 7)]; q.root.y = 0.05 * S(t * 7); f = 14; if (c === 'flee') q.expr = 'scared'; break;
    case 'angry': q.root.x = 0.05 * S(t * 18); q.root.y = 0.04 * S(t * 11); q.body = [0.1, 0, 0.25 * S(t * 18)]; q.expr = 'angry'; f = 15; break;
    case 'celebrate': q.root.y = 0.12 * abs(S(t * 3)); q.root.rz = 0.0; q.body = [0, (t * 4) % (2 * PI), 0]; q.expr = 'happy'; break;
    case 'sleep': case 'sit': q.root.y = -R.hover + 0.1; q.body = [-0.1, 0, 0]; buzz = 0; if (c === 'sleep') { q.expr = 'closed'; q.noBlink = true; } break;
    case 'hop': q.root.y = 0.15 * abs(S(t * PI * 2)); break;
    case 'talk': q.root.y = 0.03 * S(t * 3); q.head = [0.1 * S(t * 7), 0.15 * S(t * 1.4), 0]; q.jaw = [0.5 * abs(S(t * 12)), 0, 0]; break;
    case 'eat': case 'peck': q.body = [0.45, 0, 0]; q.head = [0.3, 0, 0]; q.root.y = -0.1 + 0.03 * S(t * 6); q.jaw = [0.5 * abs(S(t * 9)), 0, 0]; break;
    case 'point': q.root.y = 0.03 * S(t * 3); q.head = [0, -0.4, 0]; break;
    default: q.root.y = 0.035 * S(t * 3); q.body = [0.05 * S(t * 2), 0, 0.05 * S(t * 1.3)];
  }
  const w = buzz ? 0.55 * S(t * 2 * PI * f) : 0;
  q.wingL = [0, 0, w + 0.1 * buzz]; q.wingR = [0, 0, -w - 0.1 * buzz];
  if (R.J.antL) { q.antL = [0.2 * S(t * 3.2), 0, 0]; q.antR = [0.2 * S(t * 2.9 + 1), 0, 0]; }
  return q;
}

function swimPose(c, t, p, R) {
  const q = { root: {} };
  const swim = (f, a, ex = {}) => { const P = t * 2 * PI * f; q.tail = [0, a * S(P), 0]; q.tailFin = [0, a * 0.8 * S(P - 0.9), 0]; q.body = [0, -a * 0.25 * S(P), 0]; q.finL = [0, 0, 0.25 * S(P * 1.3)]; q.finR = [0, 0, -0.25 * S(P * 1.3)]; Object.assign(q, ex); };
  switch (c) {
    case 'walk': case 'carry': swim(1.6, 0.45); q.root.y = 0.02 * S(t * 3); break;
    case 'run': swim(3, 0.6); q.root.y = 0.02 * S(t * 5); break;
    case 'flee': swim(4, 0.7); q.expr = 'scared'; q.root.y = 0.03 * S(t * 7); break;
    case 'talk': swim(0.8, 0.25); q.jaw = [0.45 * abs(S(t * 11)), 0, 0]; q.head = [0.05 * S(t * 6), 0, 0]; break;
    case 'angry': swim(3.5, 0.5); q.root.x = 0.02 * S(t * 40); q.jaw = [0.5 * abs(S(t * 9)), 0, 0]; q.expr = 'angry'; break;
    case 'eat': case 'peck': { swim(2, 0.4); const k = max(0, S(t * 2 * PI * 1.2)); q.root.z = 0.1 * k * (R.height / 0.75) * 0.5; q.jaw = [0.6 * k, 0, 0]; break; }
    case 'sleep': case 'sit': swim(0.3, 0.12); q.root.y = -0.1 + 0.02 * S(t * 1.2); if (c === 'sleep') { q.expr = 'closed'; q.noBlink = true; } break;
    case 'celebrate': case 'hop': case 'fly': {
      const k = (t * 0.9) % 1; swim(3, 0.5); q.root.y = 0.7 * 4 * k * (1 - k) * (R.height / 1.0); q.root.rx = -k * 2 * PI * (c === 'celebrate' ? 1 : 0) - (c !== 'celebrate' ? 0.6 * (k - 0.5) * 2 : 0); if (c === 'celebrate') q.expr = 'happy'; break;
    }
    case 'point': swim(0.8, 0.25); q.root.ry = 0.3; break;
    default: swim(1.0, 0.3); q.root.y = 0.025 * S(t * 1.5);
  }
  return q;
}

function blobPose(c, t, p, R) { // ghost, snowman, octopus, snail, frog
  const q = { root: {} }, loco = R.loco, isGhost = loco === 'glide', hs = R.height / 1.5;
  const arms = (a, b = a) => { q.shoulderL = [a[0], a[1], a[2]]; q.shoulderR = [b[0], -b[1], -b[2]]; };
  const tent = (amp, f, base = 0) => { for (let i = 0; i < 8; i++) { const ph = t * f + i * 0.9; q['t' + i] = [base + amp * S(ph), 0, 0]; q['tb' + i] = [amp * 0.8 * S(ph - 0.8), 0, 0]; q['tc' + i] = [amp * S(ph - 1.6), 0, 0]; } };
  const locomote = (f, amp) => {
    const P = t * 2 * PI * f;
    if (loco === 'hop') { const k = abs(S(P / 2)); q.root.y = amp * 0.6 * hs * k; q.scl = { body: [1 + 0.06 * (1 - k), 1 - 0.08 * (1 - k), 1 + 0.06 * (1 - k)] }; if (R.J.hipL) { q.hipL = q.hipR = [-0.6 * k, 0, 0]; q.kneeL = q.kneeR = [-0.6 * k, 0, 0]; } }
    else if (loco === 'glide') { q.root.y = 0.06 * S(P); q.root.rx = 0.12 + amp * 0.2; q.body = [0, 0, 0.05 * S(P)]; }
    else { q.scl = { body: [1, 1, 1 + 0.08 * amp * S(P)] }; q.root.y = 0.006 * abs(S(P)); tent(0.25 * amp, f * 6, 0); }
  };
  switch (c) {
    case 'walk': case 'carry': locomote(1.3, 0.6); if (c === 'carry') arms([-1.2, 0, 0.1]); else arms([0.3 * S(t * 4), 0, 0.3]); break;
    case 'run': locomote(2.4, 0.9); arms([-0.6, 0, 0.5]); break;
    case 'flee': locomote(3, 1); arms([0, 0, 2.4 + 0.2 * S(t * 20)]); q.expr = 'scared'; break;
    case 'hop': case 'fly': locomote(1.6, isGhost ? 0.5 : 1); if (isGhost) q.root.y = 0.25 + 0.08 * S(t * 2); arms([0, 0, 1.2 + 0.4 * S(t * 8)]); break;
    case 'talk': q.root.y = 0.01 * S(t * 2); q.head = [0.06 * S(t * 7), 0.1 * S(t * 1.4), 0]; q.jaw = [0.4 * abs(S(t * 12)), 0, 0]; arms([-0.5 - 0.3 * S(t * 4), 0, 0.4], [0, 0, 0.2]); tent(0.15, 2); break;
    case 'celebrate': { const k = abs(S(t * PI * 2)); q.root.y = 0.12 * hs * k; arms([0, 0, 2.5 + 0.3 * S(t * 10)]); q.expr = 'happy'; q.jaw = [0.4, 0, 0]; tent(0.5, 6, -0.4); break; }
    case 'sleep': case 'sit': q.root.y = isGhost ? -0.15 + 0.03 * S(t * 1.2) : 0; q.head = [0.25, 0, 0.1]; arms([0, 0, 0.1]); q.scl = { body: [1.03, 0.94 + 0.02 * S(t * 1.3), 1.03] }; tent(0.05, 1, 0.25);
      if (c === 'sleep') { q.expr = 'closed'; q.noBlink = true; if (R.J.shell) { q.scl.head = [0.6, 0.6, 0.6]; q.pos = { head: [0, -0.02, -0.1] }; } } break;
    case 'angry': q.root.x = 0.012 * S(t * 45); q.root.y = 0.03 * abs(S(t * 12)); arms([-0.3, 0, 1.6 + 0.3 * S(t * 25)]); q.expr = 'angry'; q.jaw = [0.25, 0, 0]; tent(0.4, 12); break;
    case 'eat': case 'peck': q.head = [0.15 + 0.08 * S(t * 7), 0, 0]; q.jaw = [0.4 * abs(S(t * 7)), 0, 0]; arms([-1.1, 0.3, 0.2]); tent(0.2, 4); if (R.J.tongue) q.scl = { tongue: [1, 1, 1 + 4 * max(0, S(t * 2 * PI * 1.2))] }; break;
    case 'point': arms([0, 0, 0.2], [-1.45, 0.2, 0.1]); q.head = [0, -0.15, 0]; tent(0.1, 2); q.t0 = [-0.6, 0, 0]; break;
    default: q.root.y = isGhost ? 0.05 * S(t * 1.6) : 0.004 * S(t * 2); q.head = [0.02 * S(t * 0.9), 0.08 * S(t * 0.5), 0]; arms([0.05 * S(t * 1.6), 0, isGhost ? 0.35 : 0.06]); tent(0.12, 1.6);
      q.scl = { body: [1, 1 + 0.015 * S(t * 2.2), 1] };
  }
  if (R.J.stalkL) { q.stalkL = [0.15 * S(t * 2.3), 0, 0.15 * S(t * 1.7)]; q.stalkR = [0.15 * S(t * 2.1 + 1), 0, 0.15 * S(t * 1.9 + 2)]; }
  if (R.mouthScale && q.jaw) { const a = q.jaw[0]; delete q.jaw; q.scl = { ...(q.scl || {}), jaw: [1 + a * 0.5, 1 + a * 4, 1] }; }
  return q;
}

function wormPose(c, t, p, R) { // the earthworm: the body sways (segments), talks bobbing, leans toward a phone, shakes with anger, swallows ('gulp')
  const q = { root: {} }, N = 9, sway = (amp, f, lean = 0) => { for (let i = 1; i < N; i++) q['seg' + i] = [lean + amp * 0.45 * S(t * f + i * 0.7), 0, amp * S(t * f * 0.8 + i * 0.6)]; };
  switch (c) {
    case 'talk': sway(0.055, 3.2); q.head = [0.1 * S(t * 7), 0.12 * S(t * 1.6), 0]; q.jaw = [0.5 * abs(S(t * 12)), 0, 0]; break;
    case 'point': sway(0.03, 2.4, 0.13); q.head = [0.35, 0, 0]; q.jaw = [0.45 * abs(S(t * 12)), 0, 0]; break;   // bent down to a phone on the grass, talking
    case 'angry': sway(0.09, 11, 0.04); q.root.x = 0.008 * S(t * 47); q.head = [0.12, 0, 0.1 * S(t * 23)]; q.jaw = [0.3, 0, 0]; q.expr = 'angry'; break;
    case 'celebrate': sway(0.12, 5); q.head = [-0.1, 0.25 * S(t * 6), 0]; q.jaw = [0.4, 0, 0]; q.expr = 'happy'; break;
    case 'grow': { const k = clamp01(t / (p.dur ?? 0.5)); sway(0.08 * (1 - k), 9); q.root.y = -0.6 * (1 - ease.outBack(k)); break; }   // pops out of the ground
    case 'eat': { // the gulp, t from the key: rear back with the mouth opening, lunge (head swells, mouth huge), back up, the lump travels down, a burp
      const u = t, rear = clamp01(u / 0.22), lunge = clamp01((u - 0.22) / 0.16), back = clamp01((u - 0.4) / 0.25);
      const bend = -0.16 * ease.out(rear) * (1 - lunge) + 0.3 * ease.out(lunge) * (1 - ease.inOut(back));
      for (let i = 1; i < N; i++) q['seg' + i] = [bend, 0, 0.02 * S(t * 9 + i)];
      const open = u < 0.4 ? ease.out(clamp01(u / 0.3)) : 1 - ease.inOut(back), sw = 1 + 0.9 * open * (u < 0.55 ? 1 : 0);
      q.jaw = [2.4 * open, 0, 0]; q.scl = { head: [sw, sw, sw] }; q.expr = u < 0.4 ? 'angry' : u < 1.7 ? 'surprised' : 'smug';
      if (u > 0.62 && u < 1.75) q.gulp = (u - 0.62) / 1.1 * (N - 1);   // lump position, from the head (0) to the ground (N - 1)
      if (u > 1.85 && u < 2.15) q.jaw = [0.9, 0, 0];   // burp
      break;
    }
    default: sway(0.05, 1.8); q.head = [0.03 * S(t * 0.9), 0.1 * S(t * 0.5), 0];
  }
  if (R.mouthScale && q.jaw) { const a = q.jaw[0]; delete q.jaw; q.scl = { ...(q.scl || {}), jaw: [1 + a * 0.55, 1 + a * 3.2, 1] }; }
  return q;
}
const PLAN_POSE = { worm: wormPose, biped: bipedPose, quad: quadPose, bird: birdPose, legs: legsPose, flyer: flyerPose, swim: swimPose, blob: blobPose };
const CLIP_ALIAS = { stand: 'idle', stareCamera: 'idle', swim: 'walk', jump: 'hop', dance: 'celebrate', wave: 'celebrate', yell: 'angry', angryFist: 'angry', scared: 'flee', chew: 'eat', lieDown: 'sleep', faint: 'sleep', sitWrite: 'sit', slumpDesk: 'sleep', holdOut: 'carry', sneak: 'walk', startle: 'flee', nod: 'talk', shakeHead: 'angry', float: 'fly' };

function resolveClip(R, clip) {
  if (R.plan === 'biped' && HCLIPS[clip]) return clip; // bipeds accept every human clip
  if (CREATURE_CLIPS.includes(clip)) return clip;
  return CLIP_ALIAS[clip] || 'idle';
}

// --------------------------------------------------------------- public API --
export function buildCreature(name, opts = {}) {
  const key = String(name || '').toLowerCase().trim();
  const nm = NAME_ALIASES[key] || key;
  const o = { seed: 1, ...opts };
  const R = makeRig(nm, o);
  const builder = SPECIES[nm];
  try { (builder || placeholder)(R, o); }
  catch (e) { console.warn('creature build failed for ' + name + ': ' + e.message); return buildCreature('__placeholder__', { ...opts, label: name }); }
  try { clothes(R, o.clothes); } catch (e) { console.warn('creature clothes failed: ' + e.message); }

  // rest snapshot
  const rest = {};
  for (const [k, g] of Object.entries(R.J)) rest[k] = { p: g.position.clone(), r: g.rotation.clone(), s: g.scale.clone() };
  const baseScale = o.scale ?? 1;
  R.scaler.scale.setScalar(baseScale);
  let userExpr = o.expression || 'neutral';
  const phase = (R.seed * 0.137 + nm.length * 0.091) % 1;
  const poseFn = PLAN_POSE[R.plan] || blobPose;

  const animate = (clip = 'idle', t = 0, params = {}) => {
    t = max(0, +t || 0);
    const cl = resolveClip(R, clip);
    let q;
    try { q = poseFn(cl, t, params, R) || {}; } catch (e) { console.warn('creature pose failed: ' + e.message); q = {}; }
    // talk jaw for every plan
    if (cl === 'talk' && !q.jaw && !q.scl?.jaw && R.J.jaw) q.jaw = [0.38 * max(0, S(t * 13)) * (0.6 + 0.4 * S(t * 3.1)), 0, 0];
    if (R.post) R.post(q, cl, t, params);
    // reset joints to rest, then add deltas
    for (const [k, g] of Object.entries(R.J)) { const r = rest[k]; g.position.copy(r.p); g.rotation.copy(r.r); g.scale.copy(r.s); }
    for (const [k, v] of Object.entries(q)) {
      const g = R.J[k]; if (!g || !Array.isArray(v)) continue;
      g.rotation.x += v[0] || 0; g.rotation.y += v[1] || 0; g.rotation.z += v[2] || 0;
    }
    if (q.pos) for (const [k, v] of Object.entries(q.pos)) { const g = R.J[k]; if (g) { g.position.x += v[0]; g.position.y += v[1]; g.position.z += v[2]; } }
    if (q.scl) for (const [k, v] of Object.entries(q.scl)) { const g = R.J[k]; if (g) { g.scale.x *= v[0]; g.scale.y *= v[1]; g.scale.z *= v[2]; } }
    // ant middle arms follow the main arms
    if (R.J.shoulder2L) for (const s of ['L', 'R']) {
      const a = q['shoulder' + s] || [0, 0, 0], e = q['elbow' + s] || [0, 0, 0];
      R.J['shoulder2' + s].rotation.x += a[0] * 0.7; R.J['shoulder2' + s].rotation.z += a[2] * 0.5; R.J['elbow2' + s].rotation.x += e[0] * 0.5;
    }
    if (R.J.antL && R.plan === 'biped') { R.J.antL.rotation.x += 0.15 * S(t * 3.1); R.J.antR.rotation.x += 0.15 * S(t * 2.7 + 1); R.J.antTipL.rotation.x += 0.1 * S(t * 4); R.J.antTipR.rotation.x += 0.1 * S(t * 3.6); }
    if (R.J.earL && R.name === 'elephant') { const f = cl === 'angry' ? 0.6 * S(t * 18) : 0.15 * S(t * 2); R.J.earL.rotation.y += f; R.J.earR.rotation.y -= f; }
    if (R.J.trunk0 && cl !== 'talk') { const sw = cl === 'celebrate' ? -1.6 : cl === 'eat' ? -0.6 * abs(S(t * 3)) : 0.1 * S(t * 1.3); R.J.trunk0.rotation.x += sw * 0.6; R.J.trunk1.rotation.x += sw * 0.6; R.J.trunk2.rotation.x += sw * 0.8; R.J.trunk0.rotation.z += 0.08 * S(t * 1.1); }
    const rt = q.root || {};
    R.mover.position.set(rt.x || 0, rt.y || 0, rt.z || 0);
    R.mover.rotation.set(rt.rx || 0, rt.ry || 0, rt.rz || 0);
    // expression: clip-implied > user-set; deterministic blink + brow twitch
    const bt = (t * 0.37 + phase) % 1, blink = q.noBlink ? 0 : (bt < 0.04 ? S(bt / 0.04 * PI) : 0);
    const tw = (t * 0.23 + phase * 1.7) % 1, twitch = (cl === 'idle' || cl === 'grow') && tw < 0.06 ? 0.18 * S(tw / 0.06 * PI) : 0;
    const ex = params.expression || q.expr || userExpr;
    applyExpression(R, ex === 'neutral' && cl === 'talk' ? 'talk' : ex, blink, twitch);
    // grow / persistent size
    const k = cl === 'grow' ? clamp01(params.k ?? t / (params.dur ?? 2)) : 0;
    const g = lerp(1, params.to ?? 3, ease.inOut(k)) * (cl === 'grow' ? 1 + 0.03 * S(k * PI * 6) * (1 - k) : 1);
    R.scaler.scale.setScalar(baseScale * (params.scale ?? 1) * g);
  };

  // grip point (bipeds): right hand at rest, in root space
  let grip = null;
  if (R.J.handR) {
    R.root.updateMatrixWorld(true);
    const v = new THREE.Vector3(0, -(R.B?.aw ?? 0.08) * 0.8, 0); R.J.handR.localToWorld(v); R.root.worldToLocal(v);
    grip = [v.x * baseScale, v.y * baseScale, v.z * baseScale].map(n => Math.round(n * 1000) / 1000);
  }
  const clips = R.plan === 'biped' ? [...new Set([...CREATURE_CLIPS, ...Object.keys(HCLIPS)])] : [...CREATURE_CLIPS];
  R.root.userData = {
    kind: 'creature', name: nm, plan: R.plan, clips, expressions: CREATURE_EXPRESSIONS,
    joints: R.J, hand: R.J.handR || null, handL: R.J.handL || null, grip, mover: R.mover, scaler: R.scaler, legScale: R.legScale || 1,
    height: (R.height ?? 1) * baseScale, upright: R.plan === 'biped', opts: o,
    animate,
    setExpression: (expr) => { userExpr = EXPR[expr] ? expr : 'neutral'; applyExpression(R, userExpr); },
  };
  R.root.traverse(n => { if (n.isMesh && n.name !== 'outline') n.castShadow = true; });
  animate('idle', 0);
  return R.root;
}

function placeholder(R, o) {
  const c = col(o, { body: P.tealLight, dark: P.teal });
  R.ol = 0.01;
  const body = R.joint('body', R.mover, 0, 0, 0);
  R.a(body, facet(0.3, 0.38, 0.28, c.body, { seed: 7 }), [0, 0.38, 0]);
  const hd = R.joint('head', body, 0, 0.45, 0);
  addEyes(R, hd, { x: 0.1, y: 0.12, z: 0.22, r: 0.09, lid: c.body });
  const jaw = R.joint('jaw', hd, 0, -0.06, 0.26); R.a(jaw, facet(0.06, 0.03, 0.02, P.navy, { detail: 0 }), null, null, false);
  R.mouthScale = true;
  for (const [s, sd] of [['L', 1], ['R', -1]]) { const sh = R.joint('shoulder' + s, body, sd * 0.28, 0.45, 0, 0, 0, sd * 0.3); R.a(sh, box(0.07, 0.22, 0.07, c.dark, { pivot: 'top' })); }
  R.plan = 'blob'; R.loco = 'hop'; R.height = 0.8;
}
