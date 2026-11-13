// Cartoon rig layer (opt-in: cast `toon: true` or script `"rig": "toon"`). The puppet stays a hierarchy of boxes, but every long part
// becomes a bendable, stretchable strip, the whole body squashes and stretches, and the head gets pop-out eyes and a jaw that drops.
// Everything is a pure function of the pose (no state between frames), like the rest of the engine. Old stories never load this path.
//
// Pose channels (a clip returns them under `toon`; all optional, all blend numerically between clips):
//   sq:   [sx, sy, sz]                 whole-body squash & stretch about the feet (use sqv(s) to keep the volume)
//   scl:  { head: [sx, sy, sz], handL / handR: [sx, sy, sz] }   local squash & stretch of the head (its hat, hair and face follow), of a hand
//   bend: { spine|neck|armL|foreL|armR|foreR|legL|shinL|legR|shinR: [bx, bz, twist, stretch, fat] }
//         bx and bz are the rotation of the far end (radians), with the signs of a joint's rotation.x / rotation.z: on the spine bx > 0
//         bows forward and bz > 0 leans toward -X; on a hanging arm or leg bx > 0 swings the end back, bz > 0 toward +X. stretch
//         multiplies the length (the far joint moves with it), fat multiplies the thickness (default: volume kept, 1/sqrt(stretch))
//   ears: radians (both ears flap outward)        hat: [lift (m), tilt, spin]  (a hat that jumps off the head)
//   yaw: rad   (cycle 19) the whole body turned about its own vertical axis, on top of its facing (keys in turns: k(t, toon={'yaw': 2 * PI * n},
//         toonEase='linear') spins him n times without the stutter of a chain of facing keys)
//   lay: [rx, rz] (rad)   (cycle 6) the whole body tipped about his feet, in his own frame: -PI / 2 lays him on his back, his head behind him (with
//         sq [1, 1, 0.03]: a shadow on the ground, a man flat as paper); key it back to 0 and he stands up like a board
//   tie: [length, forward, aside]   the tie taken in a hand (engine/cloth.js, needs `cloth`): it stretches (1 = its own length, 1.7 = pulled like the cord of a
//         lamp) and swings toward the hand (radians: forward away from the chest, aside toward his left). Key it back through 0.85 and 1.05: it snaps
//   wave: { spine|neck|armL|foreL|...: [amp (m), waves, phase (turns), free, axis (rad)] }   a ripple along a part, on top of its bend: `waves` periods
//         over its length, moved along by `phase` (key it from 0 to 2 and the ripple travels twice down the limb). The two ends stay where they are (a guided
//         hand keeps its point); free: 1 lets the far end whip (a head on a noodle neck). axis: 0 = across (x), PI / 2 = front to back (z)
//   wind: [x, y, z] (m/s, in his own frame: +Z in front of him, +X to his left)   a wind of his own on the tie and the hair (engine/cloth.js): an inhale pulls
//         them up toward the nose ([0, 9, 2]), a spin flings them out. It adds to the scene wind
//   reach: { L | R: [x, y, z, w, tip] }   a hand guided to a point of the world (two-bone IK; the arm stretches when the point is too far; tip (m): the
//                                          fingertips reach it, that far beyond the wrist)
//   plant: { L | R: [x, y, z, w, [px, py, pz], flat] }   (cycle 13) a foot held at a point of the world (two-bone IK on the hip and the knee; the leg
//                                          stretches when the point is too far: the foot glued to the pavement while he walks on; [px, py, pz]: where the
//                                          knee goes, in the frame of the hips, default forward; flat false: the foot turns with the shin)
//   pin: { joint ('head'), off [x, y, z] (in the joint's frame), at [x, y, z] (world), w }   (cycle 17) that point of him stays on `at`: the whole body
//         moves so that it does (stuck by the forehead to a lamp post, a bus window, a carriage ceiling): pose the body to hang, `lay` swings it
//         (cycle 18) solved in the rig before the guided hands, with `lay` already set: hands held by others stay on their points while he hangs and swings
//   hose: 0..0.35   (cycle 9) a guided arm keeps a bend at the elbow however far it reaches: it grows that much longer than the distance (0.15: a rubber
//                   hose with an elbow; at 0 a far reach is a straight rod, the reviewers' "five reaches, the same rod")
//   touch: { L | R: [joint, x, y, z, w, tip] }   the same, to a point given in the frame of one of his own joints ('torso', 'head'...: the joint's own units, a
//         scaled head counts in unscaled metres), or on his face: ['face', across (-0.5..0.5, + = his left), up (0 = chin .. 1 = top of the skull; under the
//         nose: 0.31, the mouth: 0.23, an eye: 0.62), metres in front of the face, w, tip]. The hand follows the head wherever the spine and the neck take it
//         both take one more value, [px, py, pz]: where the elbow goes, a direction in the frame of the chest (default: low, a little out and back)
//   face: { pop: 0..1 (eyes out on stalks; euro: 1 puts a euro sign on them), pupil: 0.3..1.6, eyeScale, popLen, jaw: 0..1 (the lower face stretches down, jawLen in head
//           heights; (cycle 19) jawBlock 1: the chin drops as a block below a dark open mouth instead), tongue: 0..1 (tongueLen in m; tongueYaw / tongueDip: blown aside), steam: 0..1 (ears; steamInk: 1: inked, opaque puffs), bump: 0..1 (a lump on the skull), stars: 0..1 (circling the head),
//           expr + exprW: pull the painted face toward a named expression of the face rig (engine/facerig.js),
//           gx / gy (-1..1): the pupils alone look aside (- = toward his right) / down (+) or up (-): the head stays where it is (painted faces of the face rig),
//           eyeYaw / eyePitch / eyeRoll (rad: the popped eyeballs turn on their stalks; pitch > 0: the pupils go down), stalkYaw / stalkPitch (rad: the stalks themselves swing), popBlink: 1 (lids over the popped eyes), stalkRed: 0..1, stalkBow (m),
//           lid: 0..1 (the painted eyes close: a keyed blink), cross: 0..1 (cross-eyed),
//           one feature at a time, one side at a time, as offsets from the expression in place (0 = unchanged; L = the left of the picture when he faces us,
//           his own right eye: the high one): brow / browL / browR (1 = up to the hairline, -1 = down on the eye), browTilt / browTiltL / browTiltR (deg, > 0 lifts the inner end),
//           lidL / lidR (0..1: a wink, a heavy eye), low / lowL / lowR (0..0.5: the lower lid, a squint), eye / eyeL / eyeR (0.4 = 40 % bigger),
//           mouth: 'name' (a mouth of the face set: O, o, open, scream, teeth, grimace, clench, kiss, pout, whistle, smirk, wavy, zigzag, tongueout, evil, sob...),
//           mouthW / mouthH (0.5 = half as wide / tall again), mouthTilt, mouthDx / mouthDy (px on the 400 px face: a mouth pulled to one side),
//           cheeks, puff, sweat, blush, tears, tear, vein, shadow: 0..1,
//           (cycle 6) tremble: 0..1 (the lip trembles), pupilShake: 0..1 (the pupils shiver), gulp: 0..1 (a lump goes down the neck: key it from 0 to 1 in 0.25 s) }
import * as THREE from 'three';
import { blendHands } from './fingers.js';

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
  const frame = (u, x, z, prm, outP, outQ, wv) => {
    const [bx = 0, bz = 0, tw = 0, st = 1, fatIn] = prm, fat = fatIn ?? 1 / Math.sqrt(Math.max(0.05, st)), th = Math.hypot(bx, bz), Ls = L * st;
    _d.set(0, dir, 0);
    if (th > 1e-4) { _a.set(bx / th, 0, bz / th); const s = Math.sin(th * u), c = Math.cos(th * u); _c.crossVectors(_a, _d); outP.copy(_d).multiplyScalar(s * Ls / th).addScaledVector(_c, (1 - c) * Ls / th); outQ.setFromAxisAngle(_a, th * u); }
    else { outP.copy(_d).multiplyScalar(u * Ls); outQ.identity(); }
    if (tw) outQ.multiply(_q2.setFromAxisAngle(Y, tw * u));
    _v.set(x * fat, 0, z * fat).applyQuaternion(outQ); outP.add(_v);
    if (wv && wv[0]) {   // the ripple: across the part, nil at the joint (and at the far end unless it is free)
      const uu = Math.min(1, u), env = wv[3] ? Math.min(1, uu * 2.5) : Math.sin(Math.PI * uu), ax = wv[4] || 0;
      _v.set(Math.cos(ax), 0, Math.sin(ax)).applyQuaternion(outQ); outP.addScaledVector(_v, wv[0] * env * Math.sin(2 * Math.PI * ((wv[1] ?? 1) * uu - (wv[2] || 0))));
    }
  };
  const P0 = new THREE.Vector3(), Q0 = new THREE.Quaternion();
  return {
    joint, kids,
    apply(prm, wv) {
      if (wv && !wv[0]) wv = null; if (wv && !prm) prm = NEUTRAL_B;
      const key = (prm ? prm.map(v => (v ?? 1).toFixed(4)).join() : '') + (wv ? '|' + wv.map(v => (v || 0).toFixed(4)).join() : '');
      const idle = !wv && (!prm || (!prm[0] && !prm[1] && !prm[2] && (prm[3] ?? 1) === 1 && (prm[4] ?? 1) === 1));
      if (key !== last) {
        last = key;
        for (const it of items) {
          const p = it.m.geometry.attributes.position, n = it.m.geometry.attributes.normal, r = it.rest;
          for (let i = 0; i < p.count; i++) {
            const x = r[i * 3], y = r[i * 3 + 1], z = r[i * 3 + 2];
            if (idle) _v.set(x, y, z); else { const u = (y * dir) / L; frame(u < 0 ? 0 : u > 1 ? 1 : u, x, z, prm, P0, Q0, wv); _v.copy(P0); if (u < 0) _v.y += y;   // below the joint (a coat tail): rigid
              else if (u > 1) _v.addScaledVector(_d.set(0, dir, 0).applyQuaternion(Q0), (u - 1) * L); }   // past the far joint (the part of a neck that sits inside the head): rigid too, not stretched (a neck x8 bent 30 degrees came out through the face)
            _v.applyMatrix4(it.Mi); p.setXYZ(i, _v.x, _v.y, _v.z);
            if (n && it.restN) { _c.set(it.restN[i * 3], it.restN[i * 3 + 1], it.restN[i * 3 + 2]); if (!idle) { _c.applyQuaternion(it.rot).applyQuaternion(Q0).applyQuaternion(_q.copy(it.rot).invert()); } n.setXYZ(i, _c.x, _c.y, _c.z); }
          }
          p.needsUpdate = true; if (n) n.needsUpdate = true; it.m.geometry.computeBoundingSphere();
        }
      }
      // child joints ride on the deformed part: position and an extra rotation in front of their pose rotation
      for (const k of kids) {
        if (idle) { k.j.position.copy(k.rest); continue; }
        const u = Math.max(0, (k.rest.y * dir) / L); frame(u, k.rest.x, k.rest.z, prm, P0, Q0, wv); k.j.position.copy(P0); k.j.quaternion.premultiply(Q0);
      }
    },
  };
}

// ---- the head: the lower face stretches down when the jaw drops (the painted mouth stretches with it), and overlays: pop-out eyes
// on stalks, a tongue, steam from the ears, a bump growing on the skull, stars circling above
function puffTex() { const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d'); const gr = g.createRadialGradient(32, 32, 2, 32, 32, 31); gr.addColorStop(0, 'rgba(255,255,255,0.95)'); gr.addColorStop(0.6, 'rgba(255,255,255,0.5)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 64); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; }
// (cycle 6) an inked puff (face.steamInk): an opaque white disc with a slate rim and a pale blue shade: steam that reads on a pale wall as on a dark one
function puffInkTex() { const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d'), disc = (x, y, r, col) => { g.fillStyle = col; g.beginPath(); g.arc(x, y, r, 0, 6.2832); g.fill(); };
  const L = [[46, 70, 30], [78, 64, 34], [62, 44, 26], [92, 82, 20]];   // four lobes: a cloud, not a bubble (a string of clean white discs growing away from the head is the sign of a thought)
  for (const [x, y, r] of L) disc(x, y, r + 6, 'rgba(58,74,104,0.95)'); for (const [x, y, r] of L) disc(x, y, r, '#FFFFFF'); disc(74, 78, 22, '#D4E0F2'); disc(66, 66, 26, '#FFFFFF'); disc(48, 76, 18, '#FFFFFF');
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; }
const JAW_TOP = 0.31, MOUTH_Y = 0.227;   // as fractions of the head height from the chin: the stretch starts under the nose; the mouth's centre
const JAW_B = 0.28;                      // (cycle 19) face.jawBlock: below this the chin drops as one block; the band above it stretches (the open mouth)
function headDeform(hm, dim) {
  const sub = subdivideY(hm.geometry, 13); if (!sub) return null;
  const old = hm.geometry; hm.geometry = sub; hm.traverse(c => { if (c !== hm && c.isMesh && c.geometry === old) c.geometry = sub; }); hm.frustumCulled = false; hm.traverse(c => { c.frustumCulled = false; });
  const p = sub.attributes.position, rest = new Float32Array(p.array), yM = dim.y0 + JAW_TOP * dim.hh; let last = 0;
  const yB = dim.y0 + JAW_B * dim.hh; let lastB = 0;
  return (drop, block = 0) => {
    if (drop === last && block === lastB) return; last = drop; lastB = block; const fwd = Math.min(0.055, drop * 0.5);
    for (let i = 0; i < p.count; i++) { const y = rest[i * 3 + 1], kL = y < yM ? (yM - y) / (yM - dim.y0) : 0, k = kL + ((y < yB ? 1 : 0) - kL) * block; p.setXYZ(i, rest[i * 3], y - drop * k, rest[i * 3 + 2] + fwd * k); }
    p.needsUpdate = true;
  };
}
const STALK_RED = new THREE.Color('#E0566E');
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
    const stalk = new THREE.Mesh(new THREE.CylinderGeometry(0.011, 0.014, 1, 6, 8).rotateX(Math.PI / 2).translate(0, 0, 0.5), new THREE.MeshLambertMaterial({ color: skin })); e.add(stalk);
    const sp = stalk.geometry.attributes.position, srest = new Float32Array(sp.array), skin0 = stalk.material.color.clone(); let bow0 = 0;
    const bow = b => { if (b === bow0) return; bow0 = b; for (let j = 0; j < sp.count; j++) sp.setX(j, srest[j * 3] + b * Math.sin(Math.PI * srest[j * 3 + 2])); sp.needsUpdate = true; };   // face.stalkBow: the stalks bow outward (a rubber hose, not a rod)
    const ball = new THREE.Group(); ball.rotation.order = 'ZYX'; e.add(ball);
    ball.add(outlined(new THREE.Mesh(new THREE.IcosahedronGeometry(r, 1), white), 1.12));
    const lid = new THREE.Mesh(new THREE.IcosahedronGeometry(r * 1.1, 1), new THREE.MeshLambertMaterial({ color: skin })); lid.visible = false; ball.add(lid);   // face.popBlink: the lids close over the popped eyes
    const pupil = new THREE.Mesh(new THREE.CircleGeometry(r * 0.42, 12), black); pupil.position.z = r * 0.98; ball.add(pupil);
    const sign = new THREE.Mesh(new THREE.CircleGeometry(r * 0.92, 16), new THREE.MeshBasicMaterial({ map: euroTex(), transparent: true, depthWrite: false })); sign.position.z = r * 1.02; sign.visible = false; ball.add(sign);   // money eyes: a euro sign in place of the pupil (face.euro)
    e.traverse(o => o.layers.enable(1));   // popped eyes show in a shot in the dark too (layer 1: engine/look.js)
    e.visible = false; return { e, stalk, ball, pupil, sign, lid, bow, skin0, r, ph: i * 1.7 };
  });
  const deform = hm ? headDeform(hm, dim) : null;
  // (cycle 19) face.jawBlock 0..1: the jaw drops as a block (a hinge, not a stretch) and the gap is a dark open mouth from under the nose to the dropped
  // lip: the take reads as a jaw on the floor (stretched evenly, the lower face was a tall box with a thin painted arch at its foot, story 54)
  const cavity = new THREE.Mesh(new THREE.PlaneGeometry(1, 1).translate(0, -0.5, 0), new THREE.MeshBasicMaterial({ color: '#2A1014' })); cavity.visible = false; cavity.userData.noAO = true; g.add(cavity);
  // the tongue hangs out of the mouth (the mouth moves down with the jaw)
  const tongue = outlined(new THREE.Mesh(new THREE.BoxGeometry(hw * 0.3, 0.016, 1).translate(0, 0, 0.5), new THREE.MeshLambertMaterial({ color: '#D9606A' })), 1.06); tongue.visible = false; g.add(tongue);
  // (cycle 5) the tongue blown aside by a run (face.tongueYaw): a pink ribbon on edge, wide at the mouth, narrow and round at the tip, a wave running along
  // it (the flat tongue, seen from the front, was a thin red rod, the colour of the tie)
  const TFN = 7, tfGeo = new THREE.BufferGeometry(), tfPos = new Float32Array((TFN + 1) * 12), tfCol = new Float32Array((TFN + 1) * 12), tfIdx = [], TC = [new THREE.Color('#A03E5C'), new THREE.Color('#F58FA9')];
  for (let i = 0; i <= TFN; i++) [0, 1, 1, 0].forEach((c, j) => tfCol.set([TC[c].r, TC[c].g, TC[c].b], (i * 4 + j) * 3));   // across the ribbon: a dark rim, pink, pink, a dark rim (one mesh: nothing to fight for depth)
  for (let i = 0; i < TFN; i++) for (let j = 0; j < 3; j++) { const a = i * 4 + j; tfIdx.push(a, a + 1, a + 4, a + 1, a + 5, a + 4); }
  tfGeo.setAttribute('position', new THREE.BufferAttribute(tfPos, 3)); tfGeo.setAttribute('color', new THREE.BufferAttribute(tfCol, 3)); tfGeo.setIndex(tfIdx);
  const tongueFly = new THREE.Mesh(tfGeo, new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.DoubleSide, toneMapped: false, fog: false })); tongueFly.visible = false; tongueFly.frustumCulled = false; tongueFly.castShadow = false; tongueFly.userData.noAO = true; g.add(tongueFly);
  let ptInk = null; const pt = puffTex(), puffs = [0, 1, 2, 3, 4, 5].map(() => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: pt, transparent: true, depthWrite: false, opacity: 0 })); s.userData.noAO = true; g.add(s); return s; });
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
      const cx = -Math.sign(E.e.position.x) * E.r * 0.5 * (f.cross || 0); E.pupil.position.x = cx; E.sign.position.x = cx;   // face.cross 0..1: the pupils go to the nose
      // face.eyeYaw / eyeRoll (rad): the eyeballs turn at the end of their stalks (yaw: the pupils go to one side, e.g. to a camera that films the stalks
      // from the side; roll: round the stalk, a look round). face.stalkRed 0..1: the stalks go from skin to pink (they read on a pale ground)
      E.ball.rotation.set((f.eyePitch || 0) + 0.05 * Math.sin(t * 23 + E.ph) * pop, (f.eyeYaw || 0) + 0.07 * Math.sin(t * 19 + E.ph) * pop, f.eyeRoll || 0);
      E.lid.visible = (f.popBlink || 0) > 0.5; E.bow(Math.sign(E.e.position.x) * (f.stalkBow || 0) / th);
      E.e.rotation.set(-(f.stalkPitch || 0), f.stalkYaw || 0, 0);   // (cycle 9) face.stalkYaw / stalkPitch (rad): both stalks swing together (+ yaw toward his left, + pitch down): they follow a bus that goes by
      E.stalk.material.color.copy(E.skin0).lerp(STALK_RED, f.stalkRed || 0);
    }
    const blk = Math.max(0, Math.min(1, f.jawBlock || 0)); deform?.(Math.round(drop * 500) / 500, Math.round(blk * 20) / 20);
    cavity.visible = blk > 0.5 && drop > 0.01; if (cavity.visible) { const top = 0.3 * hh, bot = 0.24 * hh - drop; cavity.position.set(0, top, hd / 2 + Math.min(0.055, drop * 0.5) + 0.007); cavity.scale.set(hw * 0.56, Math.max(0.001, top - bot), 1); }
    const tg = f.tongue || 0, fly = !!f.tongueYaw && tg > 0.01; tongue.visible = tg > 0.01 && !fly; tongueFly.visible = fly;
    const kMo = (1 - MOUTH_Y / JAW_TOP) * (1 - blk) + blk;   // how much of the drop the mouth takes: all of it when the jaw drops as a block
    if (fly) { const k = kMo, L = tg * (f.tongueLen ?? 0.3), w0 = hw * 0.11 * (f.tongueW ?? 1);
      tongueFly.position.set(0, MOUTH_Y * hh - drop * k - 0.004, hd / 2 + 0.006); tongueFly.rotation.set(0, f.tongueYaw, 0);
      for (let i = 0; i <= TFN; i++) { const u = i / TFN, z = u * L, y = (f.tongueDip ?? -0.1) * z * 0.5 + 0.03 * u * Math.sin(t * 26 - u * 7), hwd = w0 * (1 - 0.5 * u) * (i === TFN ? 0.3 : 1), e = 0.008;
        tfPos.set([0, y + hwd + e, z, 0, y + hwd, z, 0, y - hwd, z, 0, y - hwd - e, z], i * 12); }
      tfGeo.attributes.position.needsUpdate = true; }
    if (tongue.visible) { const k = kMo; tongue.position.set(0, MOUTH_Y * hh - drop * k - 0.01, hd / 2 + Math.min(0.055, drop * 0.5) * k - 0.01); tongue.scale.set(1, 1, Math.max(0.001, tg * (f.tongueLen ?? 0.3))); tongue.rotation.x = 0.35 + 0.9 * Math.min(1, tg) + 0.06 * Math.sin(t * 9);
      if (f.tongueYaw) { tongue.rotation.set((f.tongueDip ?? -0.1) + 0.05 * Math.sin(t * 19), f.tongueYaw + 0.14 * Math.sin(t * 23), 0); tongue.position.z += 0.012; } }   // (cycle 5) face.tongueYaw (rad, + = toward his left): the tongue blown aside by the wind of a run (1.5: flat across the cheek and out past the head), fluttering; face.tongueDip: its pitch
    const ink = f.steamInk || 0; if (ink && !ptInk) ptInk = puffInkTex();   // (cycle 6) steamInk 0..1: inked steam: a jet that leaves the ear thin and fast, swells into lobed clouds and thins as it rises
    puffs.forEach((p, i) => { const side = i % 2 ? 1 : -1; p.visible = steam > 0.01; if (!p.visible) return; const m = ink ? ptInk : pt; if (p.material.map !== m) { p.material.map = m; p.material.needsUpdate = true; }
      if (ink) { const q = (t * 2.3 + Math.floor(i / 2) / 3 + (side > 0 ? 0.17 : 0)) % 1, s0 = (0.07 + 0.2 * q) * steam;
        p.position.set(side * (hw / 2 + 0.02 + 0.3 * Math.pow(q, 0.8)), hh * 0.5 + 0.04 * q + 0.34 * q * q, -hd * 0.1); p.scale.set(s0 * (1.5 - 0.5 * q), s0 * (0.7 + 0.3 * q), 1);
        p.material.rotation = side * (0.25 - 0.9 * q) + i * 1.9; p.material.opacity = Math.min(1, 5 * q) * Math.pow(1 - q, 0.55) * Math.min(1, steam); return; }
      const q = (t * 1.6 + i * 0.37) % 1; p.material.rotation = 0;
      p.position.set(side * (hw / 2 + 0.03 + q * 0.16), hh * 0.5 + q * 0.2, -hd * 0.1); p.scale.setScalar((0.05 + q * 0.14) * steam); p.material.opacity = 0.85 * Math.sin(Math.PI * q) * Math.min(1, steam); });
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
  const add = (name, joint, child, dir) => { if (J[joint] && J[child]) { const L0 = len(joint, child); parts[name] = makePart(J[joint], jointSet, L0, dir); parts[name].L = L0; } };   // .L: the rest length (the child joint's position moves with a stretch)
  add('spine', 'torso', 'neck', 1); add('neck', 'neck', 'head', 1);
  for (const s of ['L', 'R']) { add('arm' + s, 'shoulder' + s, 'elbow' + s, -1); add('fore' + s, 'elbow' + s, 'hand' + s, -1); add('leg' + s, 'hip' + s, 'knee' + s, -1); add('shin' + s, 'knee' + s, 'foot' + s, -1); }
  const hm = ud.headMesh; let dim = null;
  if (hm) { hm.geometry.computeBoundingBox(); const bb = hm.geometry.boundingBox; dim = { hw: bb.max.x - bb.min.x, hh: bb.max.y - bb.min.y, hd: bb.max.z - bb.min.z, y0: bb.min.y, cx: (bb.max.x + bb.min.x) / 2, z1: bb.max.z }; }
  const skin = ud.spec?.skin || '#E2B48A', face = dim ? headOverlays(J.head, hm, dim, skin) : null;
  const ORDER = ['spine', 'neck', 'armL', 'foreL', 'armR', 'foreR', 'legL', 'shinL', 'legR', 'shinR'], ZERO3 = [0, 0, 0];
  // (cycle 6) a gulp: a lump that goes down the front of the neck (face.gulp 0..1: from under the chin to the collar, swelling in the middle of its way)
  let gulp = null; if (J.neck) { gulp = new THREE.Mesh(new THREE.IcosahedronGeometry(0.05, 1), new THREE.MeshLambertMaterial({ color: new THREE.Color(skin) })); gulp.visible = false; gulp.castShadow = false; J.neck.add(gulp); }
  const ears = J.head ? J.head.children.filter(c => c.name === 'ear').map(m => ({ m, r: m.rotation.clone() })) : [], hm0 = J.head?.children.find(c => c.name === 'hat'), hat = hm0 ? { m: hm0, y: hm0.position.y } : null;
  // reach: { L | R: [x, y, z, w] }: a hand brought to a point of the world (w 0..1 blends from the clip's pose). Two-bone IK on the shoulder and the elbow, the
  // elbow kept low and a little out; a point further than the arm is long stretches both parts of the arm equally (the cartoon reach). The hand keeps the
  // rotation the clip gives it. Call order: the spine and the neck are bent first (the shoulder rides on them)
  const _S = new THREE.Vector3(), _T = new THREE.Vector3(), _u = new THREE.Vector3(), _p = new THREE.Vector3(), _n = new THREE.Vector3(), _qv = new THREE.Vector3(), _ad = new THREE.Vector3(), _fd = new THREE.Vector3(),
    _X = new THREE.Vector3(), _Yv = new THREE.Vector3(), _Z = new THREE.Vector3(), _M = new THREE.Matrix4(), _Q = new THREE.Quaternion();
  function solveReach(reach, b, hose = 0) {
    const out = { ...b };
    for (const s of ['L', 'R']) {
      const r = reach[s], Sj = J['shoulder' + s], Ej = J['elbow' + s], pa = parts['arm' + s], pf = parts['fore' + s]; if (!r || !Sj || !Ej || !pa || !pf) continue;
      const w = Math.max(0, Math.min(1, r[3] ?? 1)); if (w < 0.001) continue;
      const L1 = pa.L, L2 = pf.L, ba = b['arm' + s] || NEUTRAL_B, bf = b['fore' + s] || NEUTRAL_B;
      Sj.parent.updateWorldMatrix(true, false); _T.set(r[0], r[1], r[2]); Sj.parent.worldToLocal(_T); _S.copy(Sj.position);
      // r[4] (tip, m): the point is reached by the fingertips, not by the wrist: the forearm and the hand are one straight bone, that much longer
      const tip = r[4] || 0; let s1 = ba[3] ?? 1, s2 = bf[3] ?? 1;
      const d = Math.max(1e-4, _T.distanceTo(_S)), e = (d - tip) / (L1 * s1 + L2 * s2);
      const need = e * (1 + hose); if (need > 1) { s1 *= need * 1.001; s2 *= need * 1.001; }   // (cycle 9) hose: longer than needed, so the elbow stays bent
      const a = L1 * s1, c = L2 * s2 + tip, cosA = Math.max(-1, Math.min(1, (a * a + d * d - c * c) / (2 * a * d))), sinA = Math.sqrt(1 - cosA * cosA);
      _u.copy(_T).sub(_S).divideScalar(d); if (r[5]) _p.set(r[5][0], r[5][1], r[5][2]).normalize(); else _p.set((s === 'L' ? 1 : -1) * 0.45, -1, -0.55).normalize();   // r[5]: where the elbow goes (a direction in the frame of the chest); default: low, a little out and back
      _n.crossVectors(_u, _p); if (_n.lengthSq() < 1e-6) _n.set(1, 0, 0); _n.normalize(); _qv.crossVectors(_n, _u).normalize();
      _ad.copy(_u).multiplyScalar(cosA).addScaledVector(_qv, sinA);                                  // the upper arm
      _fd.copy(_T).sub(_S).addScaledVector(_ad, -a).normalize();                                      // the forearm (from the elbow to the point)
      _Yv.copy(_ad).negate(); _Z.copy(_fd).addScaledVector(_Yv, -_fd.dot(_Yv)); if (_Z.lengthSq() < 1e-6) _Z.copy(_qv).negate(); _Z.normalize(); _X.crossVectors(_Yv, _Z).normalize();
      _Q.setFromRotationMatrix(_M.makeBasis(_X, _Yv, _Z)); const bend = Math.acos(Math.max(-1, Math.min(1, _ad.dot(_fd))));
      Sj.quaternion.slerp(_Q, w); Ej.rotation.set(Ej.rotation.x + (-bend - Ej.rotation.x) * w, Ej.rotation.y * (1 - w), Ej.rotation.z * (1 - w));
      out['arm' + s] = [ba[0] * (1 - w), ba[1] * (1 - w), ba[2] || 0, (ba[3] ?? 1) + (s1 - (ba[3] ?? 1)) * w, ba[4] ?? null];
      out['fore' + s] = [bf[0] * (1 - w), bf[1] * (1 - w), bf[2] || 0, (bf[3] ?? 1) + (s2 - (bf[3] ?? 1)) * w, bf[4] ?? null];
    }
    return out;
  }
  // (cycle 13) plant: { L | R: [x, y, z, w, [px, py, pz], flat] }: a foot held at a point of the world (the gum on the pavement, a step, a door it is caught in).
  // Two-bone IK on the hip and the knee, the knee toward [px, py, pz] in the frame of the hips (default forward, a little down); a point further than the leg
  // is long stretches the thigh and the shin equally (the cartoon leg left behind while the body walks on). The foot stays flat in the frame of the body
  // unless flat is false. Called after the clip's joint rotations, before the parts are bent.
  const _Q2 = new THREE.Quaternion(), _Q3 = new THREE.Quaternion();
  function solvePlant(plant, b) {
    const out = { ...b };
    for (const s of ['L', 'R']) {
      const r = plant[s], Hj = J['hip' + s], Kj = J['knee' + s], pa = parts['leg' + s], pf = parts['shin' + s]; if (!r || !Hj || !Kj || !pa || !pf) continue;
      const w = Math.max(0, Math.min(1, r[3] ?? 1)); if (w < 0.001) continue;
      const L1 = pa.L, L2 = pf.L, ba = b['leg' + s] || NEUTRAL_B, bf = b['shin' + s] || NEUTRAL_B;
      Hj.parent.updateWorldMatrix(true, false); _T.set(r[0], r[1], r[2]); Hj.parent.worldToLocal(_T); _S.copy(Hj.position);
      let s1 = ba[3] ?? 1, s2 = bf[3] ?? 1;
      const d = Math.max(1e-4, _T.distanceTo(_S)), e = d / (L1 * s1 + L2 * s2);
      if (e > 0.985) { s1 *= e / 0.985; s2 *= e / 0.985; }   // a little longer than needed: the knee keeps a hint of a bend even at full stretch
      const a = L1 * s1, c = L2 * s2, cosA = Math.max(-1, Math.min(1, (a * a + d * d - c * c) / (2 * a * d))), sinA = Math.sqrt(1 - cosA * cosA);
      _u.copy(_T).sub(_S).divideScalar(d); if (r[4]) _p.set(r[4][0], r[4][1], r[4][2]).normalize(); else _p.set(0, -0.15, 1).normalize();
      _n.crossVectors(_u, _p); if (_n.lengthSq() < 1e-6) _n.set(1, 0, 0); _n.normalize(); _qv.crossVectors(_n, _u).normalize();
      _ad.copy(_u).multiplyScalar(cosA).addScaledVector(_qv, sinA);                                  // the thigh
      _fd.copy(_T).sub(_S).addScaledVector(_ad, -a).normalize();                                      // the shin (from the knee to the ankle)
      _Yv.copy(_ad).negate(); _Z.copy(_qv).addScaledVector(_Yv, -_qv.dot(_Yv)); if (_Z.lengthSq() < 1e-6) _Z.set(0, 0, 1); _Z.normalize(); _X.crossVectors(_Yv, _Z).normalize();   // the front of the thigh toward the knee
      _Q.setFromRotationMatrix(_M.makeBasis(_X, _Yv, _Z)); const bend = Math.acos(Math.max(-1, Math.min(1, _ad.dot(_fd))));
      Hj.quaternion.slerp(_Q, w); Kj.rotation.set(Kj.rotation.x + (bend - Kj.rotation.x) * w, Kj.rotation.y * (1 - w), Kj.rotation.z * (1 - w));   // the knee bends back (rx > 0)
      const Fj = J['foot' + s];
      if (Fj && r[5] !== false) { Kj.updateWorldMatrix(true, false); obj.getWorldQuaternion(_Q2); Kj.getWorldQuaternion(_Q3); _Q3.invert().multiply(_Q2); Fj.quaternion.slerp(_Q3, w); }   // the sole flat in the frame of the body
      out['leg' + s] = [ba[0] * (1 - w), ba[1] * (1 - w), ba[2] || 0, (ba[3] ?? 1) + (s1 - (ba[3] ?? 1)) * w, ba[4] ?? null];
      out['shin' + s] = [bf[0] * (1 - w), bf[1] * (1 - w), bf[2] || 0, (bf[3] ?? 1) + (s2 - (bf[3] ?? 1)) * w, bf[4] ?? null];
    }
    return out;
  }
  ud.toon = {
    parts,
    // call after the joint rotations of the frame are set (applyHuman): bends, local scales, whole-body squash, head overlays
    apply(tp = {}, t = 0, baseScale = 1) {
      let b = tp.bend || {}, first = 0; const wv = tp.wave || NOWAVE;
      // (cycle 18) pin, moved here from the director: the whole body shifted so that a point of one of his joints sits on its point of the world, once the
      // spine and the neck are bent and before the guided hands are solved (shifted after them, a body hung by the forehead carried its held hands away)
      let pinned = false;
      const doPin = () => { const pn = tp.pin; pinned = true; if (!pn || !pn.at || (pn.w ?? 1) <= 0.001) return; const jn = J[pn.joint || 'head']; if (!jn) return;
        obj.updateMatrixWorld(true); const o = pn.off || ZERO3; _T.set(o[0], o[1], o[2]); jn.localToWorld(_T);
        obj.position.x += (pn.at[0] - _T.x) * (pn.w ?? 1); obj.position.y += (pn.at[1] - _T.y) * (pn.w ?? 1); obj.position.z += (pn.at[2] - _T.z) * (pn.w ?? 1); obj.updateMatrixWorld(true); };
      const hs = tp.scl?.head; if (J.head) { const k0 = J.head.scale.x; J.head.scale.set(k0 * (hs?.[0] ?? 1), k0 * (hs?.[1] ?? 1), k0 * (hs?.[2] ?? 1)); }   // before the guided hands: a touch on a swollen head must land on its surface
      if (tp.reach || tp.touch) {   // the spine and the neck are bent first (the shoulders and the head ride on them), once: a part turns its child joints each time it is applied
        const sq0 = tp.sq; if (sq0) obj.scale.set(baseScale * sq0[0], baseScale * sq0[1], baseScale * sq0[2]); parts.spine?.apply(b.spine || null, wv.spine); parts.neck?.apply(b.neck || null, wv.neck);
        doPin();
        let rc = tp.reach;
        if (tp.touch) { rc = { ...(rc || {}) }; for (const sd of ['L', 'R']) { const q = tp.touch[sd]; if (!q) continue;
          if (q[0] === 'face') { if (!hm || !dim) continue; hm.updateWorldMatrix(true, false); _T.set(dim.cx + q[1] * dim.hw, dim.y0 + q[2] * dim.hh, dim.z1 + q[3] / (hm.getWorldScale(_X).z || 1)); hm.localToWorld(_T); }   // on the face: across (-0.5..0.5), up from the chin (0..1), metres in front
          else { const j = J[q[0]]; if (!j) continue; j.updateWorldMatrix(true, false); _T.set(q[1], q[2], q[3]); j.localToWorld(_T); }
          rc[sd] = [_T.x, _T.y, _T.z, q[4] ?? 1, q[5] || 0, q[6] || null]; } }
        b = solveReach(rc, b, tp.hose || 0); first = 2;
      }
      if (tp.plant) { const sq1 = tp.sq; if (sq1) obj.scale.set(baseScale * sq1[0], baseScale * sq1[1], baseScale * sq1[2]); obj.updateWorldMatrix(true, false); b = solvePlant(tp.plant, b); }   // (cycle 13) feet held at points of the world
      for (let i = first; i < ORDER.length; i++) parts[ORDER[i]]?.apply(b[ORDER[i]] || null, wv[ORDER[i]]);
      for (const hn of HANDS) { const h = J[hn]; if (!h) continue; const v = tp.scl?.[hn]; h.scale.set(v?.[0] ?? 1, v?.[1] ?? 1, v?.[2] ?? 1); }   // scl.handL / handR: a hand that swells (the big glove of a cartoon wave)
      const sq = tp.sq; if (sq) obj.scale.set(baseScale * sq[0], baseScale * sq[1], baseScale * sq[2]);
      if (!pinned) doPin();
      const er = tp.ears || 0; for (const e of ears) { e.m.rotation.set(e.r.x, e.r.y + e.m.userData.side * er, e.r.z); }
      if (hat) { const h = tp.hat || ZERO3; hat.m.position.y = hat.y + h[0]; hat.m.rotation.set(0, h[2], h[1]); }
      face?.(tp.face || {}, t);
      if (gulp) { const gp = tp.face?.gulp || 0; gulp.visible = gp > 0.02 && gp < 0.98; if (gulp.visible) { const sw = Math.pow(Math.sin(Math.PI * gp), 0.6); gulp.position.set(0, 0.135 - 0.115 * gp, 0.034); gulp.scale.set(0.95 * sw, 0.75 * sw, 0.62 * sw); } }
    },
  };
  return ud.toon;
}

// ---- numeric blend of two toon channel sets (missing = neutral)
const NEUTRAL_B = [0, 0, 0, 1, null], NOWAVE = {}, TIE0 = [1, 0, 0], SCL_KEYS = ['head', 'handL', 'handR'], HANDS = ['handL', 'handR'], ONE3 = [1, 1, 1], ZERO = [0, 0, 0];
export function blendToon(a = {}, b = {}, w = 1) {
  if (w >= 1 && !a) return b; const L = (x, y) => x + (y - x) * w, out = {};
  const POLE = (x, y) => (x && y) ? [L(x[0], y[0]), L(x[1], y[1]), L(x[2], y[2])] : (x || y || null);   // the elbow hint of a guided hand
  const sa = a.sq || [1, 1, 1], sb = b.sq || [1, 1, 1]; if (a.sq || b.sq) out.sq = [L(sa[0], sb[0]), L(sa[1], sb[1]), L(sa[2], sb[2])];
  for (const n of SCL_KEYS) { const ha = a.scl?.[n], hb = b.scl?.[n]; if (ha || hb) { const x = ha || ONE3, y = hb || ONE3; (out.scl ||= {})[n] = [L(x[0], y[0]), L(x[1], y[1]), L(x[2], y[2])]; } }
  const ks = new Set([...Object.keys(a.bend || {}), ...Object.keys(b.bend || {})]);
  if (ks.size) { out.bend = {}; for (const k of ks) { const x = a.bend?.[k] || NEUTRAL_B, y = b.bend?.[k] || NEUTRAL_B, fx = x[4] ?? 1 / Math.sqrt(x[3] ?? 1), fy = y[4] ?? 1 / Math.sqrt(y[3] ?? 1); out.bend[k] = [L(x[0] || 0, y[0] || 0), L(x[1] || 0, y[1] || 0), L(x[2] || 0, y[2] || 0), L(x[3] ?? 1, y[3] ?? 1), L(fx, fy)]; } }
  if (a.ears || b.ears) out.ears = L(a.ears || 0, b.ears || 0);
  if (a.wave || b.wave) { out.wave = {}; for (const k of new Set([...Object.keys(a.wave || {}), ...Object.keys(b.wave || {})])) { const x = a.wave?.[k], y = b.wave?.[k], p = x || y, q = y || x;   // the ripple of a part: it swells and dies down, its shape stays
    out.wave[k] = [L(x ? x[0] || 0 : 0, y ? y[0] || 0 : 0), L(p[1] ?? 1, q[1] ?? 1), L(p[2] || 0, q[2] || 0), (w < 0.5 ? p : q)[3] || 0, L(p[4] || 0, q[4] || 0)]; } }
  if (a.hairUp || b.hairUp) out.hairUp = L(a.hairUp || 0, b.hairUp || 0);
  if (a.hose || b.hose) out.hose = L(a.hose || 0, b.hose || 0);   // (cycle 9) the bend kept in a far reach
  if (a.knot || b.knot) out.knot = w < 0.5 ? (a.knot || b.knot) : (b.knot || a.knot);   // (cycle 7) the colour of his tie knot (a colour switches half-way between two keys)   // hair left on end (engine/cloth.js)
  if (a.tie || b.tie) { const x = a.tie || TIE0, y = b.tie || TIE0; out.tie = [L(x[0] ?? 1, y[0] ?? 1), L(x[1] || 0, y[1] || 0), L(x[2] || 0, y[2] || 0)]; }   // the tie taken in a hand: [length, forward, aside] (engine/cloth.js)
  if (a.wind || b.wind) { const x = a.wind || ZERO, y = b.wind || ZERO; out.wind = [L(x[0], y[0]), L(x[1], y[1]), L(x[2], y[2])]; }   // a wind of his own on what trails (an inhale lifts the tie)
  if (a.hands || b.hands) out.hands = blendHands(a.hands, b.hands, w);   // finger poses (engine/fingers.js): {L, R}, by name or as numbers
  if (a.hat || b.hat) { const x = a.hat || [0, 0, 0], y = b.hat || [0, 0, 0]; out.hat = [L(x[0], y[0]), L(x[1], y[1]), L(x[2], y[2])]; }
  if (a.lay || b.lay) { const x = a.lay || [0, 0], y = b.lay || [0, 0]; out.lay = [L(x[0] || 0, y[0] || 0), L(x[1] || 0, y[1] || 0)]; }
  if (a.yaw || b.yaw) out.yaw = L(a.yaw || 0, b.yaw || 0);   // (cycle 19) the whole body turned about its own vertical axis on top of its facing (rad): a spin keyed in turns
  if (a.pin || b.pin) { const x = a.pin, y = b.pin, p = x || y, q = y || x, po = p.off || [0, 0, 0], qo = q.off || [0, 0, 0];   // (cycle 17) a body point pinned to the world: it lets go and takes hold by its weight
    out.pin = { joint: (w < 0.5 ? p : q).joint, off: [L(po[0], qo[0]), L(po[1], qo[1]), L(po[2], qo[2])], at: [L(p.at[0], q.at[0]), L(p.at[1], q.at[1]), L(p.at[2], q.at[2])], w: L(x ? (x.w ?? 1) : 0, y ? (y.w ?? 1) : 0) }; }   // (cycle 6) the whole body tipped about his feet
  if (a.touch || b.touch) { out.touch = {}; for (const sd of ['L', 'R']) { const x = a.touch?.[sd], y = b.touch?.[sd]; if (!x && !y) continue;
    if (x && y && x[0] === y[0]) out.touch[sd] = [x[0], L(x[1], y[1]), L(x[2], y[2]), L(x[3], y[3]), L(x[4] ?? 1, y[4] ?? 1), L(x[5] || 0, y[5] || 0), POLE(x[6], y[6])];
    else { const q = !x ? y : !y ? x : (w < 0.5 ? x : y), k = !x ? w : !y ? 1 - w : Math.abs(2 * w - 1); out.touch[sd] = [q[0], q[1], q[2], q[3], (q[4] ?? 1) * k, q[5] || 0, q[6] || null]; } } }   // fades in and out; between two joints it lets go and takes again
  if (a.reach || b.reach) { out.reach = {}; for (const sd of ['L', 'R']) { const x = a.reach?.[sd], y = b.reach?.[sd]; if (!x && !y) continue; const p0 = x || y, p1 = y || x; out.reach[sd] = [L(p0[0], p1[0]), L(p0[1], p1[1]), L(p0[2], p1[2]), L(x ? (x[3] ?? 1) : 0, y ? (y[3] ?? 1) : 0), L(p0[4] || 0, p1[4] || 0), POLE(x?.[5], y?.[5])]; } }   // a hand guided to a point: fades in and out through its weight
  if (a.plant || b.plant) { out.plant = {}; for (const sd of ['L', 'R']) { const x = a.plant?.[sd], y = b.plant?.[sd]; if (!x && !y) continue; const p0 = x || y, p1 = y || x; out.plant[sd] = [L(p0[0], p1[0]), L(p0[1], p1[1]), L(p0[2], p1[2]), L(x ? (x[3] ?? 1) : 0, y ? (y[3] ?? 1) : 0), POLE(x?.[4], y?.[4]), (w < 0.5 ? p0 : p1)[5]]; } }   // (cycle 13) a foot held at a point: fades in and out through its weight
  const fa = a.face || {}, fb = b.face || {}, fk = new Set([...Object.keys(fa), ...Object.keys(fb)]);
  if (fk.size) { out.face = {}; for (const k of fk) { const dflt = (k === 'pupil' || k === 'eyeScale') ? 1 : 0; const keep = k === 'popLen' || k === 'jawLen' || k === 'tongueLen' || k === 'expr', x = fa[k] ?? (keep ? fb[k] : dflt), y = fb[k] ?? (keep ? fa[k] : dflt); out.face[k] = typeof x === 'number' && typeof y === 'number' ? L(x, y) : (w < 0.5 ? x : y); } }
  return out;
}
// add b onto a (automatic layers on top of the clip's channels)
export function addToon(a = {}, b = {}) {
  const out = { ...a };
  if (b.sq) { const s = a.sq || [1, 1, 1]; out.sq = [s[0] * b.sq[0], s[1] * b.sq[1], s[2] * b.sq[2]]; }
  if (b.scl) { out.scl = { ...(a.scl || {}) }; for (const n of SCL_KEYS) { const h = b.scl[n]; if (!h) continue; const s = a.scl?.[n] || ONE3; out.scl[n] = [s[0] * h[0], s[1] * h[1], s[2] * h[2]]; } }
  if (b.bend) { out.bend = { ...(a.bend || {}) }; for (const [k, y] of Object.entries(b.bend)) { const x = out.bend[k] || NEUTRAL_B, fx = x[4] ?? 1 / Math.sqrt(x[3] ?? 1), fy = y[4] ?? 1 / Math.sqrt(y[3] ?? 1); out.bend[k] = [(x[0] || 0) + (y[0] || 0), (x[1] || 0) + (y[1] || 0), (x[2] || 0) + (y[2] || 0), (x[3] ?? 1) * (y[3] ?? 1), fx * fy]; } }
  if (b.face) out.face = { ...(a.face || {}), ...b.face };
  if (b.wave) out.wave = { ...(a.wave || {}), ...b.wave };
  if (b.tie) out.tie = b.tie; if (b.lay) out.lay = b.lay; if (b.knot) out.knot = b.knot; if (b.yaw) out.yaw = (a.yaw || 0) + b.yaw;
  if (b.pin) out.pin = b.pin;   // (cycle 17)
  if (b.ears) out.ears = (a.ears || 0) + b.ears;
  if (b.hands) out.hands = { ...(a.hands || {}), ...b.hands };
  if (b.reach) out.reach = { ...(a.reach || {}), ...b.reach };
  if (b.touch) out.touch = { ...(a.touch || {}), ...b.touch };
  if (b.plant) out.plant = { ...(a.plant || {}), ...b.plant };
  if (b.hairUp) out.hairUp = (a.hairUp || 0) + b.hairUp;
  if (b.hose) out.hose = (a.hose || 0) + b.hose;
  if (b.wind) { const x = a.wind || ZERO; out.wind = [x[0] + b.wind[0], x[1] + b.wind[1], x[2] + b.wind[2]]; }
  if (b.hat) { const x = a.hat || [0, 0, 0]; out.hat = [x[0] + b.hat[0], x[1] + b.hat[1], x[2] + b.hat[2]]; }
  return out;
}
