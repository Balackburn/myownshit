// « Le chat » (story 87): this man has a cat that will not come down; the cat was holding the tree hostage; no demands; the special forces stormed
// it and do not come down either; a tank aimed at the cat at point-blank range; the cat ducked, not the street opposite; three days of air strikes;
// toll: the hostage lost a twig; the man was arrested for feeding the enemy; the cat was charged with the damage, tried at the foot of the tree in
// absentia; the hostage asked to stay with the cat; sentenced to come down, escorted by the soldiers; that night the cat came down to eat the seized
// evidence, then went back up to sleep.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere, addOutline, mat } from './style.js';
import { grp, at, canvasPlane, buildProp, rod } from './props.js';
import { buildCreature } from './creatures.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = x => { const u = clamp01(x), c = 1.70158; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
// a value keyed in time: keys [[t, v], ...] (sorted); eased between keys over `blend` seconds after each key (0: a step)
function keyAt(keys, t, def = 0, blend = 0.2) {
  if (!keys || !keys.length) return def;
  let v = def, prev = def, t0 = -1e9;
  for (const [kt, kv] of keys) { if (t >= kt) { prev = v; v = kv; t0 = kt; } else break; }
  if (blend <= 0) return v;
  return prev + (v - prev) * smooth((t - t0) / blend);
}
// the value of a stepped key list (a clip name, an expression)
function stepAt(keys, t, def) { let v = def; for (const [kt, kv] of keys || []) { if (t >= kt) v = kv; else break; } return v; }
// a damped wobble started at each time of `ts` (amplitude a, rad/s w, damping d)
function wob(ts, t, a = 1, w = 22, d = 4.3) { let s = 0; for (const t0 of [].concat(ts ?? [])) { const u = t - t0; if (u >= 0) s += a * Math.sin(u * w) * Math.exp(-u * d); } return s; }
const BARK = '#6A4529', BARK_D = '#4E3220', LEAF = '#3E7A36', LEAF2 = '#5C9A45', LEAF3 = '#2F6430';
// a faceted foliage clump (pivot at its centre)
function clump(r, color, seed) {
  const m = new THREE.Mesh(new THREE.IcosahedronGeometry(r, 1), mat(color));
  const p = m.geometry.attributes.position; for (let i = 0; i < p.count; i++) { const k = 1 + (hsh(seed * 31 + Math.round(p.getX(i) * 97 + p.getY(i) * 57 + p.getZ(i) * 13)) - 0.5) * 0.22; p.setXYZ(i, p.getX(i) * k, p.getY(i) * k * 0.86, p.getZ(i) * k); }
  m.geometry.computeVertexNormals(); m.castShadow = m.receiveShadow = true; addOutline(m, 0.025); return m;
}
// a tapered branch between two points (radius r0 at a, r1 at b), outlined
function limb(a, b, r0, r1, color = BARK) {
  const A = new THREE.Vector3(...a), Bv = new THREE.Vector3(...b), m = cyl(r1, r0, A.distanceTo(Bv), color, 7);
  m.position.copy(A).add(Bv).multiplyScalar(0.5); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), Bv.clone().sub(A).normalize()); addOutline(m, 0.04); return m;
}
// a paper sheet's canvas: a title word, ruled lines, a red stamp
function sheetDraw(text, stamp) {
  return (c, W, H) => {
    c.fillStyle = '#FBFAF4'; c.fillRect(0, 0, W, H); c.strokeStyle = '#1B1B1E'; c.lineWidth = W * 0.02; c.strokeRect(W * 0.01, H * 0.01, W * 0.98, H * 0.98);
    c.fillStyle = '#1B1B1E'; c.textAlign = 'center'; c.textBaseline = 'middle'; let fs = Math.round(H * 0.17); c.font = `900 ${fs}px Arial`;
    while (c.measureText(text).width > W * 0.88 && fs > 8) { fs -= 2; c.font = `900 ${fs}px Arial`; }
    c.fillText(text, W / 2, H * 0.2);
    c.fillStyle = 'rgba(27,27,30,0.55)'; for (let i = 0; i < 4; i++) c.fillRect(W * 0.12, H * (0.4 + i * 0.09), W * (0.76 - (i === 3 ? 0.3 : 0)), Math.max(2, H * 0.025));
    if (stamp) { c.strokeStyle = '#C8202A'; c.lineWidth = W * 0.035; c.beginPath(); c.arc(W * 0.7, H * 0.82, W * 0.14, 0, TAU); c.stroke(); c.fillStyle = '#C8202A'; c.beginPath(); c.arc(W * 0.7, H * 0.82, W * 0.06, 0, TAU); c.fill(); }
  };
}

export const CHAT_PROPS = {
  // THE tree (pivot at the foot of the trunk; the top branch points +X): a tapered trunk 5.7 m high, a bare top branch from (0.05, 5.45) to (2.2, 5.62)
  // where the cat lies (its top surface at y 5.6 near x 0.8), a small leaf clump at its tip, three lower branches with clumps (left at 4.5 m reaching to
  // (-2.1, 5.1), right at 3.7 m to (2.0, 4.2), left at 2.9 m to (-1.8, 3.3)) and a crown behind the trunk top on the left (so the cat has sky behind it
  // from the front; o.tip false: no clump at its tip). o.sag [[t, rad]]: the outer half of the top branch (from x 1.25) bends down; o.wobAt [t, ...]: it wobbles after a landing;
  // o.curl [[t, 0..1]]: a leafy side shoot from the top branch at x 0.3 that stands up (0) curls over the cat like an arm (1, its leafy hand resting
  // beyond the cat at x ~1.3); o.twig (true): a small twig with two leaves sticking up from the top branch at x 1.35 (the one the air strikes take);
  // o.summons {at, text}: a sheet stapled to the trunk's front (+Z) at 1.75 m, popping in at `at`; o.leaf (colours)
  loneTree(o) {
    const g = grp(), lc = o.leaf || [LEAF, LEAF2, LEAF3];
    // the trunk: three tapered pieces with a slight bend, a root flare, a few dark bark stripes
    const T = [[0, 0, 0], [0.04, 2.0, 0.02], [-0.03, 4.0, 0], [0.05, 5.7, 0]], R = [0.36, 0.29, 0.22, 0.16];
    for (let i = 0; i < 3; i++) g.add(limb(T[i], T[i + 1], R[i], R[i + 1]));
    for (let i = 0; i < 5; i++) { const a = i / 5 * TAU + 0.4; g.add(at(box(0.14, 0.32, 0.5, BARK_D, { taper: { x: 0.4, z: 0.3 } }), Math.cos(a) * 0.32, 0.12, Math.sin(a) * 0.32, 0, -a, 0)); }
    for (let i = 0; i < 9; i++) { const y = 0.5 + i * 0.55, a = hsh(i + 3) * TAU, rr = 0.36 - 0.035 * y; g.add(at(box(0.03, 0.34, 0.02, BARK_D), Math.cos(a) * rr, y, Math.sin(a) * rr, 0, -a + PI / 2, 0)); }
    // lower branches and their clumps
    const LB = [[[0, 4.4, 0], [-2.1, 5.1, 0.2], 0.13, 0.75, 0], [[0, 3.6, 0], [2.0, 4.2, -0.2], 0.12, 0.7, 1], [[0, 2.8, 0], [-1.8, 3.3, -0.3], 0.11, 0.62, 2], [[0, 3.9, 0], [0.4, 4.7, -1.7], 0.11, 0.8, 0]];
    LB.forEach(([a, b, r, cr, ci], i) => { g.add(limb(a, b, r, r * 0.45)); g.add(at(clump(cr, lc[ci], i + 1), b[0] + (b[0] > 0 ? 0.25 : -0.25), b[1] + 0.25, b[2])); });
    // the crown, behind and left of the trunk top
    g.add(at(clump(1.15, lc[0], 7), -1.05, 6.45, -0.45), at(clump(0.8, lc[2], 8), -0.25, 6.95, -0.75), at(clump(0.7, lc[1], 9), -1.6, 5.85, 0.25));
    // the top branch: inner part fixed, outer part on a pivot (sag / wobble)
    g.add(limb([0.0, 5.42, 0], [1.3, 5.55, 0], 0.15, 0.11));
    const outer = grp(); outer.position.set(1.25, 5.545, 0); g.add(outer);
    outer.add(limb([0, 0, 0], [0.95, 0.08, 0], 0.11, 0.065)); if (o.tip !== false) outer.add(at(clump(0.45, lc[1], 11), 1.05, 0.25, 0));
    // the twig the strikes take
    if (o.twig !== false) { const tw = grp(limb([0, 0, 0], [0.06, 0.3, 0], 0.022, 0.012, BARK_D)); for (const [x, y, rz] of [[0.0, 0.2, 0.7], [0.08, 0.31, -0.6]]) tw.add(at(box(0.09, 0.012, 0.05, LEAF2, { outline: 0.01 }), x, y, 0, 0, 0, rz)); tw.position.set(0.1, 0.1, 0.02); outer.add(tw); }
    // the side shoot that curls round the cat: 8 segments with leaves and a leafy "hand" at its tip
    const N = 8, segL = 0.17, segs = []; let par = grp(); par.position.set(0.3, 5.56, 0.0); g.add(par);
    for (let i = 0; i < N; i++) {
      const s = grp(); s.add(limb([0, 0, 0], [0, segL, 0], 0.05 - i * 0.0035, 0.046 - i * 0.0035, i % 2 ? BARK : BARK_D));
      if (i % 2 === 1) s.add(at(box(0.11, 0.014, 0.06, lc[1], { outline: 0.01 }), 0.06, segL * 0.6, 0, 0, 0, -0.5));
      if (i > 0) s.position.y = segL; par.add(s); segs.push(s); par = s;
    }
    const hand = grp(); hand.position.y = segL; par.add(hand);
    for (const [rz, ry] of [[0.5, 0], [-0.1, 0.6], [-0.6, -0.5], [0.2, 1.4]]) hand.add(at(box(0.16, 0.016, 0.08, lc[1], { outline: 0.01 }), 0.05, 0.02, 0, 0, ry, rz));
    // the summons stapled on the trunk
    let sheet = null;
    if (o.summons) { sheet = grp(at(canvasPlane(0.44, 0.58, sheetDraw(o.summons.text || 'CONVOCATION', true), { res: 256 }), 0, 0, 0)); for (const [x, y] of [[-0.17, 0.25], [0.17, 0.25]]) sheet.add(at(box(0.04, 0.01, 0.01, '#9AA3AC'), x, y, 0.006));
      sheet.position.set(0.04, o.summons.y ?? 1.75, 0.31); sheet.rotation.x = -0.03; g.add(sheet); }
    g.userData.update = t => {
      outer.rotation.z = -keyAt(o.sag, t, 0, 0.12) - 0.08 * wob(o.wobAt, t, 1, 20, 4);
      const c = keyAt(o.curl, t, 0, 0.9);
      segs.forEach((s, i) => { s.rotation.z = i === 0 ? 0.25 - c * 0.55 : -0.04 - c * (0.36 + 0.02 * i) + 0.03 * Math.sin(t * 1.3 + i); });
      if (sheet) { const u = o.summons.at == null ? 1 : (t - o.summons.at) / 0.14; sheet.visible = u >= 0; sheet.scale.setScalar(Math.max(0.01, outBack(u))); }
    };
    g.userData.update(0); return g;
  },

  // The cat (pivot under its feet, nose +Z): the series' ginger creature cat at o.s (1.6). o.clips [[t, clip]] (sleep, sit, idle, walk, eat, run;
  // clip time counts from its key), o.expr [[t, expression]] (sleepy, closed, neutral, smug, surprised...), o.blinks [t, ...], o.duck [[t, 0..1]]
  // (head and chest pressed flat on the branch), o.lick [[t0, t1]] (a front paw up to the mouth, the head bobbing over it), o.yawn [[t0, t1]] (head
  // back, jaw wide, eyes shut), o.ear [t, ...] (one ear flicks), o.tail 'dangle' (the tail hangs straight down, swinging; o.tailS lengthens it),
  // o.head [[t, yaw]] (head turn, rad), o.crunch [[t0, t1]] (head down in the bowl, chewing); o.flat (0..1): ducking also squashes it flat
  // (o.duckBlend: how fast it ducks, 0.12 s)
  treeCat(o) {
    const s = o.s ?? 1.6, g = grp(), cat = buildCreature('cat', { seed: 6, ol: o.ol ?? 0.007 }); cat.scale.setScalar(s); g.add(cat);
    const J = cat.userData.joints, anim = cat.userData.animate;
    // (review 1) the creature's two whiskers per side cross at their middle and read as an "x" (a KO eye) on the white muzzle: spread them apart
    cat.traverse(m => { const p = m.geometry && m.geometry.parameters; if (m.isMesh && m.geometry.type === 'BoxGeometry' && p && Math.abs(p.width - 0.09) < 1e-6 && Math.abs(p.height - 0.005) < 1e-6) { const up = Math.sign(m.rotation.z * Math.sign(m.position.x || 1)) || 1; m.position.y += 0.014 * up; m.position.x *= 1.15; m.rotation.z *= 0.5; } });
    const in_ = (ivs, t) => { for (const [a, b] of ivs || []) if (t >= a && t < b) return [a, b]; return null; };
    g.userData.update = t => {
      let t0 = -1e6; for (const [kt] of o.clips || []) { if (t >= kt) t0 = kt; else break; }
      const clip = stepAt(o.clips, t, 'sit'), ct = Math.max(0, t - (t0 < -1e5 ? -10 : t0));
      const ex = stepAt(o.expr, t, null), yw = in_(o.yawn, t);
      anim(clip, ct, { blinks: o.blinks || [], ...(yw ? { expression: 'closed' } : ex ? { expression: ex } : {}) });
      const d = keyAt(o.duck, t, 0, o.duckBlend ?? 0.12), fl = (o.flat ?? 0) * d; cat.scale.set(s * (1 + 0.3 * fl), s * (1 - 0.55 * fl), s * (1 + 0.2 * fl));
      if (d > 0.001) { if (J.neck) J.neck.rotation.x += 0.9 * d; if (J.head) J.head.rotation.x += 0.5 * d; if (J.body) J.body.rotation.x += 0.12 * d; cat.userData.mover.position.y -= 0.05 * d; }
      const hy = keyAt(o.head, t, 0, 0.15); if (J.head && hy) J.head.rotation.y += hy;
      const lk = in_(o.lick, t);
      if (lk) { const u = clamp01((t - lk[0]) / 0.15) * clamp01((lk[1] - t) / 0.15), bob = Math.sin((t - lk[0]) * 14);
        if (J.legFL) J.legFL.rotation.x -= 1.9 * u; if (J.kneeFL) J.kneeFL.rotation.x -= 1.2 * u;
        if (J.neck) J.neck.rotation.x += (0.35 + 0.12 * bob) * u; if (J.head) { J.head.rotation.x += 0.25 * u; J.head.rotation.y += 0.35 * u; } if (J.jaw) J.jaw.rotation.x += 0.18 * u * (0.5 + 0.5 * bob); }
      if (yw) { const u = Math.sin(clamp01((t - yw[0]) / (yw[1] - yw[0])) * PI);
        if (J.neck) J.neck.rotation.x -= 0.4 * u; if (J.head) { J.head.rotation.x -= 0.55 * u; J.head.scale.y *= 1 + 0.25 * u; } if (J.jaw) { J.jaw.rotation.x += 1.25 * u; J.jaw.scale.y *= 1 + 0.6 * u; } }
      const cr = in_(o.crunch, t);
      if (cr) { const u = clamp01((t - cr[0]) / 0.12); if (J.neck) J.neck.rotation.x += 0.75 * u; if (J.head) J.head.rotation.x += 0.35 * u; if (J.jaw) J.jaw.rotation.x += 0.3 * u * Math.abs(Math.sin((t - cr[0]) * 11)); }
      const ef = wob(o.ear, t, 0.7, 30, 7); if (J.earL) J.earL.rotation.z += ef; if (J.earR) J.earR.rotation.x -= 0.3 * Math.abs(ef);
      if (o.tailS && J.tail) J.tail.scale.y *= o.tailS;   // (review 1) after animate(), which puts every joint back to its rest scale
      if (o.tail === 'dangle' && J.tail) { J.tail.rotation.set(0.05 + 0.08 * Math.sin(t * 2.1), 0, 0.1 * Math.sin(t * 1.6)); if (J.tail2) J.tail2.rotation.set(0.05 * Math.sin(t * 2.6 + 1), 0, 0.12 * Math.sin(t * 1.9)); }
    };
    g.userData.update(0); return g;
  },

  // A pet bowl full of croquettes (pivot at its base, the tag at the front +Z): o.r (0.19) top radius, o.color, o.tag: a big red evidence tag tied
  // to the rim with SCELLÉ in white (o.tagS scales it); o.eat [t0, t1]: the croquettes go one by one; o.empty: none left; o.shake [[t0, t1]]: the
  // croquettes jump in the bowl
  kibbleBowl(o) {
    const r = o.r ?? 0.19, h = r * 0.48, g = grp(), bowl = cyl(r, r * 0.78, h, o.color || '#2F7FC4', 14, { pivot: 'bottom' }); addOutline(bowl, 0.03); g.add(bowl);
    g.add(at(cyl(r * 0.84, r * 0.84, 0.01, '#1E4F7E', 14), 0, h + 0.002, 0));
    const kib = [], km = mat('#9A5F2E'), km2 = mat('#7A4520');
    for (let i = 0; i < 26; i++) { const a = hsh(i) * TAU, rr = r * 0.78 * Math.sqrt(hsh(i + 50)), m = new THREE.Mesh(new THREE.IcosahedronGeometry(r * 0.14, 0), i % 3 ? km : km2);
      m.position.set(Math.cos(a) * rr, h + 0.01 + r * 0.08 * hsh(i + 9) + (rr < r * 0.4 ? r * 0.1 : 0), Math.sin(a) * rr); m.rotation.set(hsh(i + 2) * 3, hsh(i + 4) * 3, 0); m.castShadow = true; g.add(m); kib.push({ m, y: m.position.y }); }
    let tag = null;
    if (o.tag) { const ts = o.tagS ?? 1; tag = grp();
      const card = canvasPlane(0.4 * ts, 0.18 * ts, (c, W, H) => { c.fillStyle = '#D0202A'; c.fillRect(0, 0, W, H); c.fillStyle = '#FFFFFF'; c.beginPath(); c.arc(W * 0.07, H * 0.5, H * 0.1, 0, TAU); c.fill();
        c.textAlign = 'center'; c.textBaseline = 'middle'; let fs = Math.round(H * 0.62); c.font = `900 ${fs}px Arial`; while (c.measureText('SCELLÉ').width > W * 0.78 && fs > 8) { fs -= 2; c.font = `900 ${fs}px Arial`; } c.fillText('SCELLÉ', W * 0.54, H * 0.55);
        c.strokeStyle = '#FFFFFF'; c.lineWidth = H * 0.05; c.strokeRect(H * 0.06, H * 0.06, W - H * 0.12, H - H * 0.12); }, { res: 512, emissive: 0.15 });
      const back = at(box(0.41 * ts, 0.19 * ts, 0.008, '#8E1218'), 0, 0, -0.006); tag.add(back, card);
      tag.add(rod([-0.2 * ts, 0, -0.003], [-0.33 * ts, 0.12 * ts, -0.06], 0.006, '#F4F1E8'));
      tag.position.set(r * 0.25, h + 0.12 * ts, r + 0.05); tag.rotation.set(-0.12, 0, -0.08); g.add(tag); }
    g.userData.update = t => {
      const e = o.empty ? 1 : o.eat ? clamp01((t - o.eat[0]) / (o.eat[1] - o.eat[0])) : 0, sh = o.shake && o.shake.some(([a, b]) => t >= a && t < b);
      kib.forEach((k, i) => { k.m.visible = hsh(i + 77) >= e; k.m.position.y = k.y + (sh ? r * 0.18 * Math.abs(Math.sin(t * 26 + i * 1.3)) : 0); });
      if (tag) tag.rotation.z = -0.08 + 0.05 * Math.sin(t * 2.2);
    };
    g.userData.update(0); return g;
  },

  // Striped tape wound round a trunk and run out to posts (pivot at the foot of the trunk): o.y (1.25) height of the bands, o.r (0.33) the trunk's radius
  // there, o.posts [[x, z], ...] (posts 1.0 m high round the tree), o.wrap [t0, dur]: the three turns wind on one after another, then the runs out to the
  // posts (without it: all there); red and white blocks with NE PAS FRANCHIR in the white ones
  trunkTape(o) {
    const g = grp(), y0 = o.y ?? 1.25, r = o.r ?? 0.33, W = 0.12;
    const tex = (len) => { const cv = document.createElement('canvas'); cv.width = 1024; cv.height = 64; const c = cv.getContext('2d'); const n = Math.max(2, Math.round(len / 0.9));
      for (let i = 0; i < n; i++) { c.fillStyle = i % 2 ? '#D0202A' : '#F6F4EE'; c.fillRect(i * 1024 / n, 0, 1024 / n + 1, 64); if (i % 2 === 0) { c.fillStyle = '#D0202A'; c.font = '900 34px Arial'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('NE PAS FRANCHIR', (i + 0.5) * 1024 / n, 34); } }
      const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t; };
    const bands = [];
    for (let i = 0; i < 3; i++) { const m = new THREE.Mesh(new THREE.CylinderGeometry(r + 0.015 * i, r + 0.015 * i, W, 20, 1, true), new THREE.MeshLambertMaterial({ map: tex(2 * PI * r), side: THREE.DoubleSide }));
      m.position.y = y0 + (i - 1) * 0.16; m.rotation.z = (i - 1) * 0.12; g.add(m); bands.push(m); }
    const runs = [];
    for (const [px, pz] of o.posts || []) { const post = at(cyl(0.035, 0.04, 1.0, '#D0202A', 6, { pivot: 'bottom' }), px, 0, pz); g.add(post, at(box(0.09, 0.05, 0.09, '#F6F4EE'), px, 1.0, pz));
      const A = new THREE.Vector3(0, y0, 0), Bp = new THREE.Vector3(px, 0.92, pz), len = A.distanceTo(Bp), pl = new THREE.Mesh(new THREE.PlaneGeometry(len, W), new THREE.MeshLambertMaterial({ map: tex(len), side: THREE.DoubleSide }));
      const run = grp(); run.position.copy(A); run.lookAt(Bp); pl.rotation.y = -PI / 2; pl.position.z = len / 2; run.add(pl); g.add(run); runs.push({ run, pl, len }); }
    g.userData.update = t => {
      const [a, d] = o.wrap || [-10, 0.1], u = (t - a) / Math.max(0.01, d);
      bands.forEach((b, i) => { b.visible = u >= i * 0.2; });
      runs.forEach((R, i) => { const k = clamp01((u - 0.6 - i * 0.08) / 0.3); R.run.visible = k > 0.01; R.pl.scale.x = Math.max(0.01, k); R.pl.position.z = R.len * k / 2; });
    };
    g.userData.update(0); return g;
  },

  // The street opposite (pivot at the foot of the row's middle, the row along X, the fronts toward +Z): o.n (5) blocks of flats (holedBlock, whole)
  // o.w (5.2) wide and o.h (11) high side by side. o.foldAt (s): from then each block, one after another (o.stagger 0.12 s), folds down onto itself
  // in 0.32 s, from block o.from (default the middle) outward (it squashes to a slab and tips a little), dust bursts at its foot, then a heap of rubble and a column of smoke stay; o.ruined: already
  // down and smoking from the start; o.noSmoke: no smoke columns
  foldRow(o) {
    const n = o.n ?? 5, w = o.w ?? 5.2, h = o.h ?? 11, g = grp(), cols = o.colors || ['#EADFC8', '#E8C9B4', '#D9DDE0', '#EBD9A8', '#DCC8C0', '#E4E0D2'], B = [];
    for (let i = 0; i < n; i++) {
      const x = (i - (n - 1) / 2) * (w + 0.3), piv = grp(); piv.position.set(x, 0, 0); g.add(piv);
      const blk = buildProp('holedBlock', { w, h: h * (0.85 + 0.25 * hsh(i + 3)), d: 5, holeAt: 99, color: cols[i % cols.length] }); piv.add(blk);
      const heap = grp(); for (let j = 0; j < 16; j++) { const m = box(0.8 + hsh(i * 9 + j) * 1.3, 0.4 + hsh(i * 7 + j) * 0.8, 0.8 + hsh(i * 5 + j), j % 3 ? '#B8AFA2' : cols[i % cols.length], { outline: 0.02 }); m.position.set((hsh(j + i * 3) - 0.5) * w * 0.9, 0.3 + hsh(j * 2 + i) * 0.9, -1.5 - hsh(j + 40) * 2.5); m.rotation.set(hsh(j) * 2, hsh(j + 1) * 3, hsh(j + 2)); heap.add(m); }
      heap.position.x = x; g.add(heap);
      const dust = []; for (let j = 0; j < 7; j++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 1), new THREE.MeshLambertMaterial({ color: '#CFC6B8', emissive: new THREE.Color('#5A5248'), transparent: true, opacity: 0.95 })); addOutline(m, 0.04); m.visible = false; g.add(m); dust.push(m); }
      B.push({ piv, heap, dust, x, t0: o.ruined ? -10 : (o.foldAt ?? 1e6) + Math.abs(i - (o.from ?? (n - 1) / 2)) * (o.stagger ?? 0.12), sgn: hsh(i + 11) > 0.5 ? 1 : -1 });
    }
    const smoke = buildProp('smokeField', { points: B.filter((b, i) => i % 2 === 0).map((b, i) => [b.x + (hsh(i) - 0.5) * 2, -2.5, o.smokeH ?? 9 + 3 * hsh(i + 1), 0.5]), color: o.smoke || '#9A948E', size: o.smokeS ?? 0.7, per: 8, seed: 17 }); g.add(smoke);
    g.userData.update = t => {
      let any = false;
      for (const b of B) { const u = (t - b.t0) / 0.32, k = smooth(u);
        b.piv.scale.y = Math.max(0.05, 1 - 0.95 * k); b.piv.rotation.z = b.sgn * 0.08 * k; b.piv.visible = u < 1.6;
        b.heap.visible = u > 0.5; b.heap.scale.y = clamp01((u - 0.5) * 2) * 0.9 + 0.1;
        const du = (t - b.t0 - 0.12) / 1.2;
        b.dust.forEach((m, j) => { const v = du - j * 0.03; m.visible = v > 0 && v < 1; if (!m.visible) return; const a = (j / 7) * PI + 0.2, rr = 3.5 * Math.sqrt(v); m.position.set(b.x + Math.cos(a) * rr * (w / 4), 1 + 4 * v * (0.5 + hsh(j)), 1 + Math.sin(a) * 0.5); m.scale.setScalar((1.2 + 1.6 * hsh(j + 3)) * Math.sin(Math.min(1, v * 1.4) * PI * 0.5 + 0.2) * (1 - 0.5 * v)); });
        if (u > 0.2) any = true; }
      smoke.visible = any && !o.noSmoke; if (smoke.visible) smoke.userData.update?.(t);
    };
    g.userData.update(0); return g;
  },

  // An army tank whose gun telescopes (pivot on the ground under its middle, front +Z): plainTank (no markings) with o.gun [[t, rad]] (pitch,
  // negative: up) and o.turret [[t, rad]] passed through; o.ext [[t, m]]: the gun slides out in nested sleeves (o.segs 8) by that many metres
  // beyond its 2.9 m (eased between keys over o.extBlend 0.3 s); the muzzle sits at gun z 2.95 + ext; o.fireAt (s): a white flash and a puff at the
  // muzzle and a recoil of the sleeves (o.flashS, o.puffS scale them); o.rumble as battleTank
  extendTank(o) {
    const tk = buildProp('plainTank', { gun: o.gun, turret: o.turret, rumble: o.rumble, color: o.color }), g = grp(tk); let gun = null;
    tk.traverse(m => { const p = m.geometry && m.geometry.parameters; if (!gun && m.isMesh && m.geometry.type === 'CylinderGeometry' && p && Math.abs(p.height - 2.6) < 1e-6) gun = m.parent; });
    const n = o.segs ?? 8, maxE = Math.max(0.1, ...(o.ext || [[0, 0]]).map(e => e[1])), Ls = maxE / n + 0.25, sl = [], C = o.color || '#66753E';
    if (gun) {
      for (let i = 0; i < n; i++) { const r0 = 0.1 - i * 0.004, m = cyl(r0, r0, Ls, i % 2 ? C : '#5C6A38', 10, { pivot: 'top' }); m.rotation.x = -PI / 2; addOutline(m, 0.04); const ring = at(cyl(r0 + 0.02, r0 + 0.02, 0.08, '#2B2E22', 10), 0, 0, Ls, PI / 2, 0, 0); const sg = grp(m, ring); gun.add(sg); sl.push(sg); }
      var brake = grp(at(cyl(0.16, 0.16, 0.36, '#3A3E30', 12), 0, 0, 0.18, PI / 2, 0, 0), at(cyl(0.1, 0.1, 0.37, '#050505', 12), 0, 0, 0.19, PI / 2, 0, 0), at(new THREE.Mesh(new THREE.TorusGeometry(0.13, 0.03, 6, 16), mat('#9AA08A')), 0, 0, 0.37), at(box(0.06, 0.2, 0.2, '#2B2E22'), 0.17, 0, 0.2), at(box(0.06, 0.2, 0.2, '#2B2E22'), -0.17, 0, 0.2)); gun.add(brake);
      var flash = new THREE.Mesh(new THREE.IcosahedronGeometry(0.5, 1), new THREE.MeshBasicMaterial({ color: '#FFF4C8' })); flash.visible = false; gun.add(flash);
      var puff = new THREE.Mesh(new THREE.IcosahedronGeometry(0.45, 2), new THREE.MeshLambertMaterial({ color: '#FFFFFF', emissive: new THREE.Color('#888888') })); addOutline(puff, 0.05); puff.visible = false; gun.add(puff);
    }
    const base = 2.95;
    g.userData.update = t => {
      tk.userData.update?.(t);
      if (!gun) return;
      const u = o.fireAt == null ? -1 : t - o.fireAt, rec = u >= 0 ? 0.35 * Math.exp(-u * 7) * Math.cos(u * 18) : 0;
      const e = Math.max(0, keyAt(o.ext, t, 0, o.extBlend ?? 0.3) - rec);
      sl.forEach((s, i) => { s.visible = e > 0.02; s.position.z = base + e * (i + 1) / n - Ls; });
      brake.position.z = base + e - 0.05;
      flash.visible = u >= 0 && u < 0.07; flash.position.z = base + e + 0.35; flash.scale.set(o.flashS ?? 1.3, o.flashS ?? 1.3, 2 * (o.flashS ?? 1.2));
      puff.visible = u >= 0.05 && u < 0.9; if (puff.visible) { const v = (u - 0.05) / 0.85; puff.position.set(0.5 * v, 0.6 * v, base + e + 0.3 + 0.3 * v); puff.scale.setScalar((o.puffS ?? 1) * (0.6 + 1.6 * Math.sin(Math.min(1, v * 1.5) * PI * 0.5) * (1 - 0.6 * v))); }
    };
    g.userData.update(0); return g;
  },

  // A tank shell in flight (pivot anywhere: it draws in world space from o.from to o.to): a bright yellow-white slug with a fading white streak behind
  // it, from o.t0 over o.dur (0.18 s), gone after; o.r (0.09), o.len (0.5) its body
  shellStreak(o) {
    const g = grp(), A = new THREE.Vector3(...(o.from || [0, 0, 0])), Bv = new THREE.Vector3(...(o.to || [0, 0, -10])), dir = Bv.clone().sub(A), L = dir.length(); dir.normalize();
    const slug = new THREE.Mesh(new THREE.CapsuleGeometry(o.r ?? 0.09, o.len ?? 0.5, 4, 8), new THREE.MeshBasicMaterial({ color: '#FFF2A8' })); addOutline(slug, 0.3);
    const trail = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.07, 1, 8, 1, true), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.85, side: THREE.DoubleSide, depthWrite: false }));
    const q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir); slug.quaternion.copy(q); trail.quaternion.copy(q); g.add(slug, trail);
    g.userData.update = t => {
      const u = (t - (o.t0 ?? 0)) / (o.dur ?? 0.18); slug.visible = u >= 0 && u <= 1; trail.visible = u >= 0 && u < 1.4;
      const p = A.clone().addScaledVector(dir, L * clamp01(u)), back = Math.min(L * clamp01(u), L * 0.45), fade = u > 1 ? 1 - (u - 1) / 0.4 : 1;
      slug.position.copy(p); trail.scale.set(1, Math.max(0.01, back), 1); trail.position.copy(p).addScaledVector(dir, -back / 2); trail.material.opacity = 0.85 * clamp01(fade);
    };
    g.userData.update(-1); return g;
  },

  // A rope hanging from its pivot that reels up: o.len [[t, m]] (eased over 0.25 s between keys), o.r (0.03), o.color; a small black clip at its end
  reelRope(o) {
    const g = grp(), r = cyl(o.r ?? 0.03, o.r ?? 0.03, 1, o.color || '#2A2A2E', 6, { pivot: 'top' }), end = at(box(0.08, 0.1, 0.08, '#111214'), 0, -1, 0); g.add(r, end);
    g.userData.update = t => { const L = Math.max(0.05, keyAt(o.len, t, 6, 0.25)); r.scale.y = L; end.position.y = -L; g.rotation.z = 0.03 * Math.sin(t * 2.4 + (o.seed || 0)); };
    g.userData.update(0); return g;
  },

  // A stretcher carrying one twig (pivot at its middle at the poles' height, the poles along Z): the stretcher of props_barbecue (o.L 1.9) with a
  // crinkled survival blanket in shining silver over a small lump, a twig with three bright leaves poking up out of its head end (+Z) on the pillow
  // (o.twigUp: its tilt up from flat, rad, 1.25; o.twigS: its size, 1.3)
  twigStretcher(o) {
    const L = o.L ?? 1.9, g = grp(buildProp('stretcher', { L, w: o.w ?? 0.55 }));
    const foil = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 2), new THREE.MeshLambertMaterial({ color: '#E8EEF6', emissive: new THREE.Color('#8A94A6'), flatShading: true }));
    const p = foil.geometry.attributes.position; for (let i = 0; i < p.count; i++) { const k = 1 + (hsh(Math.round(p.getX(i) * 91 + p.getY(i) * 37 + p.getZ(i) * 53)) - 0.5) * 0.3; p.setXYZ(i, p.getX(i) * k, p.getY(i) * k, p.getZ(i) * k); } foil.geometry.computeVertexNormals();
    foil.scale.set(0.25, 0.11, L * 0.3); foil.position.set(0, 0.06, -0.05); addOutline(foil, 0.05); g.add(foil);
    g.add(at(box(0.3, 0.07, 0.2, '#F4F4F0', { outline: 0.01 }), 0, 0.05, L * 0.3));
    const tw = grp(limb([0, 0, 0], [0, 0, 0.62], 0.035, 0.018, '#6A4529')); for (const [z, rx, ry] of [[0.36, 0.4, 0.6], [0.5, -0.5, -0.5], [0.63, 0.2, 0.1]]) tw.add(at(box(0.18, 0.02, 0.11, '#5FB043', { outline: 0.015 }), 0.04, 0.02, z, rx, ry, 0));
    tw.position.set(0, 0.14, L * 0.12); tw.rotation.x = -(o.twigUp ?? 1.25); tw.scale.setScalar(o.twigS ?? 1.3); g.add(tw);
    return g;
  },

  // A judge's bench set up outdoors (pivot at the floor under its middle, the front +Z): a wooden box o.w (2.0) x o.h (1.15) x 0.8 with a raised front
  // panel, a moulded top and a brass plate (o.plate 'TRIBUNAL'); userData.top: the height of its top
  fieldBench(o) {
    const w = o.w ?? 2.0, h = o.h ?? 1.15, g = grp(), wd = o.color || '#7A4E2E', dk = '#5A3720';
    g.add(at(box(w, h, 0.8, wd, { pivot: 'bottom', outline: 0.012 }), 0, 0, 0), at(box(w + 0.12, 0.07, 0.95, dk, { outline: 0.01 }), 0, h, 0));
    for (const sx of [-1, 1]) g.add(at(box(w * 0.4, h * 0.62, 0.03, dk), sx * w * 0.24, h * 0.18, 0.41));
    const pl = canvasPlane(w * 0.6, 0.2, (c, W, H) => { c.fillStyle = '#D9A93A'; c.fillRect(0, 0, W, H); c.fillStyle = '#3A2410'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${H * 0.62}px Arial`; c.fillText(o.plate || 'TRIBUNAL', W / 2, H * 0.55); }, { res: 512 });
    g.add(at(pl, 0, h * 0.82, 0.43)); g.userData.top = h + 0.035; return g;
  },

  // A staple gun (pivot at its grip, the nose +Z, the head up): orange body, black head and trigger; o.s (1.4); o.clacks [t, ...]: the head snaps
  stapleGun(o) {
    const g = grp(), b = grp(); g.add(b);
    b.add(at(box(0.07, 0.07, 0.3, '#E8742A', { outline: 0.008 }), 0, 0.1, 0.06), at(box(0.075, 0.04, 0.3, '#1E1F22'), 0, 0.055, 0.07), at(box(0.05, 0.13, 0.05, '#1E1F22', { pivot: 'top' }), 0, 0.08, -0.05, -0.25, 0, 0));
    const lever = at(box(0.06, 0.03, 0.24, '#1E1F22', { outline: 0.006 }), 0, 0.16, -0.0); b.add(lever);
    b.scale.setScalar(o.s ?? 1.4);
    g.userData.update = t => { let k = 0; for (const c of o.clacks || []) { const u = t - c; if (u >= 0 && u < 0.15) k = Math.max(k, 1 - u / 0.15); } lever.position.y = 0.16 - 0.03 * k; b.rotation.x = -0.15 * k; };
    g.userData.update(0); return g;
  },

  // A stapled sheet (pivot at its centre, face +Z): o.w (0.32) x o.h (0.42), o.text (ESCORTE) in black, ruled lines and a red stamp, two staples at the
  // top; o.at (s): it pops in (before: hidden); o.flap: it flutters in the wind (rad)
  stapledSheet(o) {
    const w = o.w ?? 0.32, h = o.h ?? 0.42, g = grp(), s = grp(); g.add(s);
    s.add(at(canvasPlane(w, h, sheetDraw(o.text || 'ESCORTE', true), { res: 256 }), 0, -h / 2, 0)); for (const x of [-w * 0.35, w * 0.35]) s.add(at(box(0.035, 0.008, 0.01, '#9AA3AC'), x, -0.03, 0.006));
    s.position.y = h / 2;
    g.userData.update = t => { const u = o.at == null ? 1 : (t - o.at) / 0.14; g.visible = u >= 0; s.scale.setScalar(Math.max(0.01, outBack(u))); s.rotation.x = (o.flap ?? 0) * (0.6 + 0.4 * Math.sin(t * 7.3)) * Math.sin(t * 5.1 + (o.seed || 0)); };
    g.userData.update(0); return g;
  },

  // The clerk's arm (pivot at the elbow, the forearm up +Y and leaning by o.lean): a dark sleeve with a white cuff, a hand gripping a hand microphone
  // (handMic, no lettering) whose head points along +Z+Y toward the bark; o.len (0.4) the forearm shown; o.push [[t, m]]: it reaches forward
  clerkArm(o) {
    const g = grp(), arm = grp(); g.add(arm); const L = o.len ?? 0.42;
    arm.add(at(cyl(0.06, 0.07, L, o.sleeve || '#23262E', 8, { pivot: 'bottom', outline: 0.03 }), 0, 0, 0), at(cyl(0.062, 0.062, 0.05, '#F4F1E8', 8), 0, L, 0));
    const hand = at(box(0.1, 0.11, 0.09, o.skin || '#E8B48C', { outline: 0.01 }), 0, L + 0.07, 0.01); arm.add(hand);
    const mic = buildProp('handMic', { text: ' ', s: o.micS ?? 1.4 }); mic.position.set(0, L + 0.06, 0.04); mic.rotation.x = 0.9; arm.add(mic);
    arm.rotation.x = o.lean ?? 0.5;
    g.userData.update = t => { arm.position.z = keyAt(o.push, t, 0, 0.3); arm.rotation.x = (o.lean ?? 0.5) + 0.03 * Math.sin(t * 3.1); };
    g.userData.update(0); return g;
  },

  // A fighter jet without any national marking (fighterJet with the wing roundels taken off): same options
  plainJet(o) {
    const j = buildProp('fighterJet', o || {}), hide = [];
    j.traverse(m => { const p = m.geometry && m.geometry.parameters; if (m.isMesh && m.geometry.type === 'PlaneGeometry' && p && Math.abs(p.width - 1.7) < 1e-6 && Math.abs(p.height - 1.7) < 1e-6) hide.push(m); });
    for (const m of hide) m.visible = false;
    return j;
  },

  // A page that turns on a lectern (pivot at its spine, the left edge; the sheet lies along +X, its face up +Y): o.w (0.3) x o.h (0.4), ruled lines;
  // o.flipAt (s): it turns over the spine to the left in 0.25 s
  flipPage(o) {
    const w = o.w ?? 0.3, h = o.h ?? 0.4, g = grp(), pg = grp(); g.add(pg);
    const sh = canvasPlane(w, h, sheetDraw(o.text || 'BILAN', false), { res: 256 }); sh.rotation.x = -PI / 2; sh.position.x = w / 2; pg.add(sh);
    g.userData.update = t => { const u = o.flipAt == null ? 0 : clamp01((t - o.flipAt) / 0.25); pg.rotation.z = PI * smooth(u); pg.position.y = 0.002 + 0.05 * Math.sin(PI * u); };
    g.userData.update(0); return g;
  },

  // A coloured stripe across a medic's chest and back (attach to the torso joint, offset about [0, 0.3, 0]): a band o.w (0.56) wide, o.h (0.09) high,
  // o.d (0.36) deep, o.color (green): an invented service mark, no cross
  medicStripe(o) {
    const g = grp(at(box(o.w ?? 0.56, o.h ?? 0.09, o.d ?? 0.36, o.color || '#2E9A58', { outline: 0.004 }), 0, 0, 0)); return g;
  },
};
