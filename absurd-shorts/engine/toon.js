// Cartoon rig layer (opt-in: cast `toon: true` or script `"rig": "toon"`). The puppet stays a hierarchy of boxes, but every long part
// becomes a bendable, stretchable strip, the whole body squashes and stretches, and the head gets pop-out eyes and a jaw that drops.
// Everything is a pure function of the pose (no state between frames), like the rest of the engine. Old stories never load this path.
//
// Pose channels (a clip returns them under `toon`; all optional, all blend numerically between clips):
//   sq:   [sx, sy, sz]                 whole-body squash & stretch about the feet (use sqv(s) to keep the volume)
//   scl:  { head: [sx, sy, sz] }       local squash & stretch of the head (its hat, hair and face follow)
//   bend: { spine|neck|armL|foreL|armR|foreR|legL|shinL|legR|shinR: [bx, bz, twist, stretch, fat] }
//         bx and bz are the rotation of the far end (radians), with the signs of a joint's rotation.x / rotation.z: on the spine bx > 0
//         bows forward and bz > 0 leans toward -X; on a hanging arm or leg bx > 0 swings the end back, bz > 0 toward +X. stretch
//         multiplies the length (the far joint moves with it), fat multiplies the thickness (default: volume kept, 1/sqrt(stretch))
//   ears: radians (both ears flap outward)        hat: [lift (m), tilt, spin]  (a hat that jumps off the head)
//   face: { pop: 0..1 (eyes out on stalks; euro: 1 puts a euro sign on them), pupil: 0.3..1.6, eyeScale, popLen, jaw: 0..1 (the lower face stretches down, jawLen in head
//           heights), tongue: 0..1 (tongueLen in m), steam: 0..1 (ears), bump: 0..1 (a lump on the skull), stars: 0..1 (circling the head),
//           expr + exprW: pull the painted face toward a named expression of the face rig (engine/facerig.js) }
import * as THREE from 'three';

export const sqv = s => { const k = 1 / Math.sqrt(Math.max(0.05, s)); return [k, s, k]; };   // volume-preserving squash (s < 1) / stretch (s > 1) along Y

// ---- geometry: cut the four side faces of a box (BoxGeometry layout, any taper/pivot/UVs) into n strips along Y
export function subdivideY(geo, n = 6) {
  const pos = geo.attributes.position, nor = geo.attributes.normal, uv = geo.attributes.uv;
  if (!geo.index || pos.count !== 24 || !geo.groups || geo.groups.length !== 6) return null;
  const P = [], N = [], U = [], I = [], G = [];
  const push = (p, nn, u) => { P.push(p.x, p.y, p.z); N.push(nn.x, nn.y, nn.z); U.push(u.x, u.y); return P.length / 3 - 1; };
  const v3 = (a, i) => new THREE.Vector3().fromBufferAttribute(a, i), v2 = i => new THREE.Vector2().fromBufferAttribute(uv, i);
  for (let f = 0; f < 6; f++) {
    const b = f * 4, start = I.length, nn = v3(nor, b), mi = geo.groups[f].materialIndex;
    if (Math.abs(nn.y) > 0.5) { const a = [0, 1, 2, 3].map(k => push(v3(pos, b + k), nn, v2(b + k))); I.push(a[0], a[2], a[1], a[2], a[3], a[1]); }
    else {   // rows 0..n from the (v0, v1) edge to the (v2, v3) edge
      const p0 = v3(pos, b), p1 = v3(pos, b + 1), p2 = v3(pos, b + 2), p3 = v3(pos, b + 3), u0 = v2(b), u1 = v2(b + 1), u2 = v2(b + 2), u3 = v2(b + 3), rows = [];
      for (let k = 0; k <= n; k++) { const t = k / n; rows.push([push(p0.clone().lerp(p2, t), nn, u0.clone().lerp(u2, t)), push(p1.clone().lerp(p3, t), nn, u1.clone().lerp(u3, t))]); }
      for (let k = 0; k < n; k++) { const [a, d] = rows[k], [bb, c] = rows[k + 1]; I.push(a, bb, d, bb, c, d); }
    }
    G.push([start, I.length - start, mi]);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(N, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(U, 2));
  g.setIndex(I); G.forEach(([s, c, m]) => g.addGroup(s, c, m)); return g;
}

// ---- a bendable part: the meshes that belong to one joint (not to its child joints), deformed in the joint's space
const _q = new THREE.Quaternion(), _q2 = new THREE.Quaternion(), _v = new THREE.Vector3(), _a = new THREE.Vector3(), _d = new THREE.Vector3(), _c = new THREE.Vector3(), Y = new THREE.Vector3(0, 1, 0);
function makePart(joint, jointSet, L, dir, seg = 6) {
  const meshes = [], kids = [];
  const walk = (n, top) => { for (const c of n.children) { if (jointSet.has(c)) { if (top) kids.push({ j: c, rest: c.position.clone() }); continue; } if (c.isMesh && c.name !== 'outline' && c.geometry?.attributes?.position && !c.userData.noBend) meshes.push(c); if (!c.isMesh || c.name !== 'outline') walk(c, false); } };
  walk(joint, true);
  const items = [];
  for (const m of meshes) {
    if (m.parent !== joint) continue;   // nested decorations ride on their parent mesh
    const sub = subdivideY(m.geometry, seg); if (sub) { const old = m.geometry; m.geometry = sub; m.traverse(c => { if (c !== m && c.isMesh && c.geometry === old) c.geometry = sub; }); }
    m.updateMatrix(); const M = m.matrix.clone(), Mi = M.clone().invert(), p = m.geometry.attributes.position, n = m.geometry.attributes.normal;
    const rest = new Float32Array(p.count * 3), restN = n ? new Float32Array(n.array) : null, nm = new THREE.Matrix3().getNormalMatrix(M);
    for (let i = 0; i < p.count; i++) { _v.fromBufferAttribute(p, i).applyMatrix4(M); rest[i * 3] = _v.x; rest[i * 3 + 1] = _v.y; rest[i * 3 + 2] = _v.z; }
    items.push({ m, Mi, rest, restN, nm, rot: new THREE.Quaternion().setFromRotationMatrix(M) });
  }
  let last = '';
  // frame at u (0 = at the joint, 1 = far end): out position of the point (x, ., z) of the cross-section, and the section's rotation
  const frame = (u, x, z, prm, outP, outQ) => {
    const [bx = 0, bz = 0, tw = 0, st = 1, fatIn] = prm, fat = fatIn ?? 1 / Math.sqrt(Math.max(0.05, st)), th = Math.hypot(bx, bz), Ls = L * st;
    _d.set(0, dir, 0);
    if (th > 1e-4) { _a.set(bx / th, 0, bz / th); const s = Math.sin(th * u), c = Math.cos(th * u); _c.crossVectors(_a, _d); outP.copy(_d).multiplyScalar(s * Ls / th).addScaledVector(_c, (1 - c) * Ls / th); outQ.setFromAxisAngle(_a, th * u); }
    else { outP.copy(_d).multiplyScalar(u * Ls); outQ.identity(); }
    if (tw) outQ.multiply(_q2.setFromAxisAngle(Y, tw * u));
    _v.set(x * fat, 0, z * fat).applyQuaternion(outQ); outP.add(_v);
  };
  const P0 = new THREE.Vector3(), Q0 = new THREE.Quaternion();
  return {
    joint, kids,
    apply(prm) {
      const key = prm ? prm.map(v => (v ?? 1).toFixed(4)).join() : '';
      const idle = !prm || (!prm[0] && !prm[1] && !prm[2] && (prm[3] ?? 1) === 1 && (prm[4] ?? 1) === 1);
      if (key !== last) {
        last = key;
        for (const it of items) {
          const p = it.m.geometry.attributes.position, n = it.m.geometry.attributes.normal, r = it.rest;
          for (let i = 0; i < p.count; i++) {
            const x = r[i * 3], y = r[i * 3 + 1], z = r[i * 3 + 2];
            if (idle) _v.set(x, y, z); else { const u = (y * dir) / L; frame(u < 0 ? 0 : u, x, z, prm, P0, Q0); _v.copy(P0); if (u < 0) _v.y += y; }   // below the joint (a coat tail): rigid
            _v.applyMatrix4(it.Mi); p.setXYZ(i, _v.x, _v.y, _v.z);
            if (n && it.restN) { _c.set(it.restN[i * 3], it.restN[i * 3 + 1], it.restN[i * 3 + 2]); if (!idle) { _c.applyQuaternion(it.rot).applyQuaternion(Q0).applyQuaternion(_q.copy(it.rot).invert()); } n.setXYZ(i, _c.x, _c.y, _c.z); }
          }
          p.needsUpdate = true; if (n) n.needsUpdate = true; it.m.geometry.computeBoundingSphere();
        }
      }
      // child joints ride on the deformed part: position and an extra rotation in front of their pose rotation
      for (const k of kids) {
        if (idle) { k.j.position.copy(k.rest); continue; }
        const u = Math.max(0, (k.rest.y * dir) / L); frame(u, k.rest.x, k.rest.z, prm, P0, Q0); k.j.position.copy(P0); k.j.quaternion.premultiply(Q0);
      }
    },
  };
}

// ---- the head: the lower face stretches down when the jaw drops (the painted mouth stretches with it), and overlays: pop-out eyes
// on stalks, a tongue, steam from the ears, a bump growing on the skull, stars circling above
function puffTex() { const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d'); const gr = g.createRadialGradient(32, 32, 2, 32, 32, 31); gr.addColorStop(0, 'rgba(255,255,255,0.95)'); gr.addColorStop(0.6, 'rgba(255,255,255,0.5)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 64); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; }
const JAW_TOP = 0.31, MOUTH_Y = 0.227;   // as fractions of the head height from the chin: the stretch starts under the nose; the mouth's centre
function headDeform(hm, dim) {
  const sub = subdivideY(hm.geometry, 13); if (!sub) return null;
  const old = hm.geometry; hm.geometry = sub; hm.traverse(c => { if (c !== hm && c.isMesh && c.geometry === old) c.geometry = sub; }); hm.frustumCulled = false; hm.traverse(c => { c.frustumCulled = false; });
  const p = sub.attributes.position, rest = new Float32Array(p.array), yM = dim.y0 + JAW_TOP * dim.hh; let last = 0;
  return drop => {
    if (drop === last) return; last = drop; const fwd = Math.min(0.055, drop * 0.5);
    for (let i = 0; i < p.count; i++) { const y = rest[i * 3 + 1], k = y < yM ? (yM - y) / (yM - dim.y0) : 0; p.setXYZ(i, rest[i * 3], y - drop * k, rest[i * 3 + 2] + fwd * k); }
    p.needsUpdate = true;
  };
}
let _euro = null;
function euroTex() { if (_euro) return _euro; const c = document.createElement('canvas'); c.width = c.height = 128; const q = c.getContext('2d'); q.fillStyle = '#12662A'; q.font = '900 118px Arial'; q.textAlign = 'center'; q.textBaseline = 'middle'; q.fillText('€', 64, 72); _euro = new THREE.CanvasTexture(c); _euro.colorSpace = THREE.SRGBColorSpace; return _euro; }
function starGeo(r = 0.06) { const sh = new THREE.Shape(); for (let i = 0; i < 10; i++) { const a = i * Math.PI / 5, q = i % 2 ? r * 0.45 : r; sh[i ? 'lineTo' : 'moveTo'](Math.sin(a) * q, Math.cos(a) * q); } sh.closePath(); return new THREE.ExtrudeGeometry(sh, { depth: 0.012, bevelEnabled: false }).translate(0, 0, -0.006); }
function headOverlays(head, hm, dim, skin) {
  const { hw, hh, hd } = dim, g = new THREE.Group(); g.name = 'toonHead'; head.add(g);
  const P2 = (cx, cy) => [(cx / 400 - 0.5) * hw, (1 - cy / 1080) * hh], zf = y => hd / 2 - 0.015 * (y / hh) + 0.004;
  const ink = new THREE.MeshBasicMaterial({ color: '#16130F', side: THREE.BackSide }), white = new THREE.MeshBasicMaterial({ color: '#F4F0E6' }), black = new THREE.MeshBasicMaterial({ color: '#16130F' });
  const outlined = (m, k = 1.1) => { const o = new THREE.Mesh(m.geometry, ink); o.scale.setScalar(k); o.name = 'outline'; m.add(o); return m; };
  const eyes = [[84.5, 281.5, 0.036], [301, 493.5, 0.03]].map(([cx, cy, r], i) => {
    const [x, y] = P2(cx, cy), e = new THREE.Group(); e.position.set(x, y, zf(y)); g.add(e);
    const stalk = new THREE.Mesh(new THREE.CylinderGeometry(0.011, 0.014, 1, 6).rotateX(Math.PI / 2).translate(0, 0, 0.5), new THREE.MeshLambertMaterial({ color: skin })); e.add(stalk);
    const ball = new THREE.Group(); e.add(ball);
    ball.add(outlined(new THREE.Mesh(new THREE.IcosahedronGeometry(r, 1), white), 1.12));
    const pupil = new THREE.Mesh(new THREE.CircleGeometry(r * 0.42, 12), black); pupil.position.z = r * 0.98; ball.add(pupil);
    const sign = new THREE.Mesh(new THREE.CircleGeometry(r * 0.92, 16), new THREE.MeshBasicMaterial({ map: euroTex(), transparent: true, depthWrite: false })); sign.position.z = r * 1.02; sign.visible = false; ball.add(sign);   // money eyes: a euro sign in place of the pupil (face.euro)
    e.visible = false; return { e, stalk, ball, pupil, sign, r, ph: i * 1.7 };
  });
  const deform = hm ? headDeform(hm, dim) : null;
  // the tongue hangs out of the mouth (the mouth moves down with the jaw)
  const tongue = outlined(new THREE.Mesh(new THREE.BoxGeometry(hw * 0.3, 0.016, 1).translate(0, 0, 0.5), new THREE.MeshLambertMaterial({ color: '#D9606A' })), 1.06); tongue.visible = false; g.add(tongue);
  const pt = puffTex(), puffs = [0, 1, 2, 3, 4, 5].map(() => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: pt, transparent: true, depthWrite: false, opacity: 0 })); s.userData.noAO = true; g.add(s); return s; });
  // a bump that grows on the skull after a blow, and stars that circle the head
  const bump = outlined(new THREE.Mesh(new THREE.IcosahedronGeometry(0.075, 1).scale(1, 1.25, 0.9), new THREE.MeshLambertMaterial({ color: new THREE.Color(skin).multiply(new THREE.Color(1.0, 0.72, 0.68)) })), 1.07); bump.visible = false; g.add(bump);
  const sg = starGeo(), sm = new THREE.MeshBasicMaterial({ color: '#F6C93C' }), stars = [0, 1, 2, 3].map(i => { const m = outlined(new THREE.Mesh(sg, sm), 1.25); m.visible = false; g.add(m); return m; });
  return (f = {}, t = 0) => {
    const pop = f.pop || 0, jawK = f.jaw || 0, steam = f.steam || 0, drop = jawK * (f.jawLen ?? 0.5) * hh;
    for (const E of eyes) {
      E.e.visible = pop > 0.01; if (!E.e.visible) continue;
      const out = 0.02 + pop * (f.popLen ?? 0.2), s = (f.eyeScale ?? 1) * (1 + 0.9 * Math.min(1, pop * 1.5)) * (1 + 0.04 * Math.sin(t * 31 + E.ph) * pop);
      const th = 1 + Math.min(2.2, Math.max(0, out - 0.3) * 1.3); E.stalk.scale.set(th, th, Math.max(0.001, out)); E.ball.position.z = out; E.ball.scale.setScalar(s); E.pupil.scale.setScalar(f.pupil ?? (1 - 0.45 * pop));   // th: a long stalk is a thick rubber hose (it must read from far)
      const eu = (f.euro || 0) > 0.5; E.sign.visible = eu; E.pupil.visible = !eu;
      E.ball.rotation.set(0.05 * Math.sin(t * 23 + E.ph) * pop, 0.07 * Math.sin(t * 19 + E.ph) * pop, 0);
    }
    deform?.(Math.round(drop * 500) / 500);
    const tg = f.tongue || 0; tongue.visible = tg > 0.01;
    if (tongue.visible) { const k = 1 - MOUTH_Y / JAW_TOP; tongue.position.set(0, MOUTH_Y * hh - drop * k - 0.01, hd / 2 + Math.min(0.055, drop * 0.5) * k - 0.01); tongue.scale.set(1, 1, Math.max(0.001, tg * (f.tongueLen ?? 0.3))); tongue.rotation.x = 0.35 + 0.9 * Math.min(1, tg) + 0.06 * Math.sin(t * 9); }
    puffs.forEach((p, i) => { const side = i % 2 ? 1 : -1, q = (t * 1.6 + i * 0.37) % 1; p.visible = steam > 0.01; if (!p.visible) return; p.position.set(side * (hw / 2 + 0.03 + q * 0.16), hh * 0.5 + q * 0.2, -hd * 0.1); p.scale.setScalar((0.05 + q * 0.14) * steam); p.material.opacity = 0.85 * Math.sin(Math.PI * q) * Math.min(1, steam); });
    const bk = f.bump || 0; bump.visible = bk > 0.01; if (bump.visible) { bump.position.set(hw * 0.08, hh - 0.05 + 0.07 * bk, -hd * 0.05); bump.scale.setScalar(bk * (1 + 0.07 * Math.sin(t * 13))); }
    const sk = f.stars || 0; stars.forEach((m, i) => { m.visible = sk > 0.01; if (!m.visible) return; const a = t * 5.2 + i * Math.PI / 2; m.position.set(Math.sin(a) * 0.27, hh + 0.13 + 0.04 * Math.sin(t * 7 + i), Math.cos(a) * 0.27); m.rotation.set(0.3, -a, t * 4 + i); m.scale.setScalar(sk * (0.8 + 0.25 * Math.sin(t * 9 + i * 2))); });
  };
}

// ---- upgrade a built human to the cartoon rig
export function toonUpgrade(obj) {
  const ud = obj.userData, J = ud.joints; if (!J || ud.toon) return ud.toon;
  const jointSet = new Set(Object.values(J)), rest = {};
  const len = (a, b) => Math.abs(J[b].position.y) || 0.3;
  const parts = {};
  const add = (name, joint, child, dir) => { if (J[joint] && J[child]) parts[name] = makePart(J[joint], jointSet, len(joint, child), dir); };
  add('spine', 'torso', 'neck', 1); add('neck', 'neck', 'head', 1);
  for (const s of ['L', 'R']) { add('arm' + s, 'shoulder' + s, 'elbow' + s, -1); add('fore' + s, 'elbow' + s, 'hand' + s, -1); add('leg' + s, 'hip' + s, 'knee' + s, -1); add('shin' + s, 'knee' + s, 'foot' + s, -1); }
  const hm = ud.headMesh; let dim = null;
  if (hm) { hm.geometry.computeBoundingBox(); const bb = hm.geometry.boundingBox; dim = { hw: bb.max.x - bb.min.x, hh: bb.max.y - bb.min.y, hd: bb.max.z - bb.min.z, y0: bb.min.y }; }
  const skin = ud.spec?.skin || '#E2B48A', face = dim ? headOverlays(J.head, hm, dim, skin) : null;
  const ORDER = ['spine', 'neck', 'armL', 'foreL', 'armR', 'foreR', 'legL', 'shinL', 'legR', 'shinR'], ZERO3 = [0, 0, 0];
  const ears = J.head ? J.head.children.filter(c => c.name === 'ear').map(m => ({ m, r: m.rotation.clone() })) : [], hm0 = J.head?.children.find(c => c.name === 'hat'), hat = hm0 ? { m: hm0, y: hm0.position.y } : null;
  ud.toon = {
    parts,
    // call after the joint rotations of the frame are set (applyHuman): bends, local scales, whole-body squash, head overlays
    apply(tp = {}, t = 0, baseScale = 1) {
      const b = tp.bend || {};
      for (const k of ORDER) parts[k]?.apply(b[k] || null);
      const hs = tp.scl?.head; if (J.head) { const k0 = J.head.scale.x; J.head.scale.set(k0 * (hs?.[0] ?? 1), k0 * (hs?.[1] ?? 1), k0 * (hs?.[2] ?? 1)); }
      const sq = tp.sq; if (sq) obj.scale.set(baseScale * sq[0], baseScale * sq[1], baseScale * sq[2]);
      const er = tp.ears || 0; for (const e of ears) { e.m.rotation.set(e.r.x, e.r.y + e.m.userData.side * er, e.r.z); }
      if (hat) { const h = tp.hat || ZERO3; hat.m.position.y = hat.y + h[0]; hat.m.rotation.set(0, h[2], h[1]); }
      face?.(tp.face || {}, t);
    },
  };
  return ud.toon;
}

// ---- numeric blend of two toon channel sets (missing = neutral)
const NEUTRAL_B = [0, 0, 0, 1, null];
export function blendToon(a = {}, b = {}, w = 1) {
  if (w >= 1 && !a) return b; const L = (x, y) => x + (y - x) * w, out = {};
  const sa = a.sq || [1, 1, 1], sb = b.sq || [1, 1, 1]; if (a.sq || b.sq) out.sq = [L(sa[0], sb[0]), L(sa[1], sb[1]), L(sa[2], sb[2])];
  const ha = a.scl?.head, hb = b.scl?.head; if (ha || hb) { const x = ha || [1, 1, 1], y = hb || [1, 1, 1]; out.scl = { head: [L(x[0], y[0]), L(x[1], y[1]), L(x[2], y[2])] }; }
  const ks = new Set([...Object.keys(a.bend || {}), ...Object.keys(b.bend || {})]);
  if (ks.size) { out.bend = {}; for (const k of ks) { const x = a.bend?.[k] || NEUTRAL_B, y = b.bend?.[k] || NEUTRAL_B, fx = x[4] ?? 1 / Math.sqrt(x[3] ?? 1), fy = y[4] ?? 1 / Math.sqrt(y[3] ?? 1); out.bend[k] = [L(x[0] || 0, y[0] || 0), L(x[1] || 0, y[1] || 0), L(x[2] || 0, y[2] || 0), L(x[3] ?? 1, y[3] ?? 1), L(fx, fy)]; } }
  if (a.ears || b.ears) out.ears = L(a.ears || 0, b.ears || 0);
  if (a.hat || b.hat) { const x = a.hat || [0, 0, 0], y = b.hat || [0, 0, 0]; out.hat = [L(x[0], y[0]), L(x[1], y[1]), L(x[2], y[2])]; }
  const fa = a.face || {}, fb = b.face || {}, fk = new Set([...Object.keys(fa), ...Object.keys(fb)]);
  if (fk.size) { out.face = {}; for (const k of fk) { const dflt = (k === 'pupil' || k === 'eyeScale') ? 1 : 0; const keep = k === 'popLen' || k === 'jawLen' || k === 'tongueLen' || k === 'expr', x = fa[k] ?? (keep ? fb[k] : dflt), y = fb[k] ?? (keep ? fa[k] : dflt); out.face[k] = typeof x === 'number' && typeof y === 'number' ? L(x, y) : (w < 0.5 ? x : y); } }
  return out;
}
// add b onto a (automatic layers on top of the clip's channels)
export function addToon(a = {}, b = {}) {
  const out = { ...a };
  if (b.sq) { const s = a.sq || [1, 1, 1]; out.sq = [s[0] * b.sq[0], s[1] * b.sq[1], s[2] * b.sq[2]]; }
  if (b.scl?.head) { const s = a.scl?.head || [1, 1, 1], h = b.scl.head; out.scl = { head: [s[0] * h[0], s[1] * h[1], s[2] * h[2]] }; }
  if (b.bend) { out.bend = { ...(a.bend || {}) }; for (const [k, y] of Object.entries(b.bend)) { const x = out.bend[k] || NEUTRAL_B, fx = x[4] ?? 1 / Math.sqrt(x[3] ?? 1), fy = y[4] ?? 1 / Math.sqrt(y[3] ?? 1); out.bend[k] = [(x[0] || 0) + (y[0] || 0), (x[1] || 0) + (y[1] || 0), (x[2] || 0) + (y[2] || 0), (x[3] ?? 1) * (y[3] ?? 1), fx * fy]; } }
  if (b.face) out.face = { ...(a.face || {}), ...b.face };
  if (b.ears) out.ears = (a.ears || 0) + b.ears;
  if (b.hat) { const x = a.hat || [0, 0, 0]; out.hat = [x[0] + b.hat[0], x[1] + b.hat[1], x[2] + b.hat[2]]; }
  return out;
}
