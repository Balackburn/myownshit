// Props of story « tonnerre » (story 89): this man was woken by the thunder; he filed a noise complaint; the thunder was arrested at three
// thousand metres; two helicopters were struck; in court the thunder kept silent; the judge insisted; it answered; the district lost its windows;
// the twelve jurors are deaf; the experts confirmed it was loud; a padded cell, a mime cellmate who asks for a transfer out loud; no address on
// release, so house arrest at the victim's home: it took the window side.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere, addOutline, mat, rng } from './style.js';
import { grp, at, canvasPlane, label, torus, extrude, poly } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = x => { const u = clamp01(x), c = 1.70158; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const easeOut = x => 1 - Math.pow(1 - clamp01(x), 3);
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const noShadow = m => { m.traverse(c => { c.castShadow = false; }); return m; };
const basic = (color, opacity = 1, extra = {}) => new THREE.MeshBasicMaterial({ color, transparent: opacity < 1, opacity, depthWrite: opacity >= 1, side: THREE.DoubleSide, toneMapped: false, ...extra });
// a value keyed in time: keys [[t, v], ...] (sorted); eased between keys over `blend` seconds after each key (0: a step)
function keyAt(keys, t, def = 0, blend = 0.2) {
  if (!keys || !keys.length) return def;
  let v = def, prev = def, t0 = -1e9;
  for (const [kt, kv] of keys) { if (t >= kt) { prev = v; v = kv; t0 = kt; } else break; }
  if (blend <= 0 || typeof v !== 'number') return v;
  return prev + (v - prev) * smooth((t - t0) / blend);
}
// keyed vectors: keys [[t, a, b, c...], ...]; eased over `blend` after each key
function keyVec(keys, t, def, blend = 0.15) {
  if (!keys || !keys.length) return def.slice();
  let v = def.slice(), prev = def.slice(), t0 = -1e9;
  for (const k of keys) { if (t >= k[0]) { prev = v; v = k.slice(1); t0 = k[0]; } else break; }
  const w = blend <= 0 ? 1 : smooth((t - t0) / blend);
  return v.map((x, i) => (prev[i] ?? x) + (x - (prev[i] ?? x)) * w);
}
// a pulse list [[t, dur], ...]: 1 at t falling to 0 over dur
function pulseAt(list, t) { let v = 0; for (const [a, d] of list || []) { const u = (t - a) / (d || 0.3); if (u >= 0 && u < 1) v = Math.max(v, 1 - u); } return v; }
// a cylinder from a to b (radius r)
function segment(a, b, r, material, seg = 5) {
  const A = new THREE.Vector3(...a), B = new THREE.Vector3(...b), d = B.clone().sub(A), L = d.length();
  const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, Math.max(1e-4, L), seg), material);
  m.position.copy(A).add(B).multiplyScalar(0.5); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize()); m.castShadow = false; return m;
}
const radialTex = (() => { let tex = null; return () => { if (tex) return tex; const c = document.createElement('canvas'); c.width = c.height = 64; const x = c.getContext('2d');
  const gr = x.createRadialGradient(32, 32, 2, 32, 32, 31); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.45, 'rgba(255,255,255,0.55)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  x.fillStyle = gr; x.fillRect(0, 0, 64, 64); tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; return tex; }; })();
const softSprite = (color, opacity = 1) => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: radialTex(), color, transparent: true, opacity, depthWrite: false, toneMapped: false })); s.castShadow = false; return s; };

// the thunder's face expressions: [brow angle, brow lift, lid, mouth width, mouth open, mouth curve, cheeks]
const TFACE = {
  neutral: [0.05, 0, 0.1, 0.28, 0, 0, 0], angry: [0.48, -0.03, 0.18, 0.24, 0, -0.4, 0], shut: [0.55, -0.05, 0.22, 0.42, 0, -0.08, 1],
  shout: [0.55, 0.03, 0.0, 0.36, 1, 0, 0], calm: [0.0, 0.0, 0.38, 0.2, 0, 0.12, 0], smug: [-0.12, 0.03, 0.32, 0.24, 0, 0.4, 0],
  surprised: [-0.28, 0.07, 0.0, 0.16, 0.45, 0, 0], sad: [-0.35, 0.0, 0.3, 0.2, 0, -0.35, 0], blank: [0.0, 0.02, 0.05, 0.2, 0, 0, 0],
  // (pass 2) flat: calm, heavy lids, a level mouth (no smile); tight: the shut mouth without the swelling; clench: furious, a thick clenched line
  flat: [0.0, 0.0, 0.3, 0.22, 0, 0, 0], tight: [0.5, -0.04, 0.2, 0.3, 0, -0.05, 0], clench: [0.62, -0.06, 0.12, 0.4, 0, -0.12, 0],
  droopy: [-0.4, -0.02, 0.42, 0.18, 0, -0.3, 0]
};
const THICK = { shut: 1.8, tight: 1.7, clench: 2.2 };
// the bolt arms' directions (the left arm; the right one is mirrored), in the cloud's frame
const TARMS = { rest: [-0.55, -0.83, 0.12], up: [-0.45, 0.88, 0.15], out: [-1, 0.05, 0.15], cuff: [0.62, -0.33, 0.71], hold: [-0.55, 0.15, 0.82], tuck: [0.2, -0.9, 0.35], shrug: [-0.85, 0.45, 0.3], point: [-0.3, 0.1, 0.95], cradle: [-0.35, -0.2, 0.92],
  // (final pass) cuffLow: the cuffed arms lower and further forward, clear of the plate's sides (the puffed cheeks show)
  cuffLow: [0.5, -0.66, 0.56] };

export const TONNERRE_PROPS = {
  // The thunder: one black anvil cumulonimbus (pivot at the middle of its flat base, front +Z; about 3.3 o.s wide at the anvil, 2.1 o.s tall): a
  // puffy charcoal body under a flat, wide, overhanging anvil top, a lighter box face plate (white eyes, thick black brows, a mouth that opens on a
  // glowing yellow inside), two small yellow zigzag bolt arms. It never rains.
  // o.expr [[t, name]] (TFACE), o.mouth [[t, 0..1]] (extra opening), o.look [[t, gx, gy]] (pupils, -1..1), o.blinks [t, ...] (else every 3.3 s),
  // o.arms [[t, poseL, poseR]] (TARMS names), o.sq [[t, sx, sy, sz]] (squeeze of the body), o.flash [[t, dur]] (the body lights up),
  // o.flashK (1), o.glow (0: a moonlit lift for night shots, neutral grey since pass 2), o.cuffs (oversized handcuffs on the bolt arms; o.cuffsAt: they snap shut then), o.tag (an electronic tag on the right arm; o.tagSide -1: the left), o.bundle (a tiny
  // bundle hanging from the left arm), o.bob (0.04), o.lean [[t, rz]]
  // (pass 2) o.tint (a colour multiplied into the body and plate, to bring the charcoal back to neutral under a warm or a blue light), o.emis (a
  // constant emissive colour), o.strain [[t, amp]] (a fast trembling of the body: holding it in), o.blinkDur (0.1), o.shadows false (no shadows:
  // the aerial shots), o.lampS / o.tagYaw (the tag's lamp size, the tag turned round the arm), o.bundleS (the bundle's size)
  thunderCloud(o) {
    const g = grp(), root = grp(), body = grp(); g.add(root); root.add(body); root.scale.setScalar(o.s ?? 1);
    const r = rng(o.seed || 89), geo = new THREE.IcosahedronGeometry(1, 1), lit = [];
    const TN = new THREE.Color(o.tint || '#FFFFFF'), tc = c => new THREE.Color(c).multiply(TN).getStyle(), EM = new THREE.Color(o.emis || '#000000');
    const M = c => { const m = mat(tc(c), { unique: true }); lit.push(m); return m; };
    const C = [o.color || '#252526', o.color2 || '#2E2E30', o.under || '#1C1C1D'], TOP = o.top || '#3A3A3D';
    const puff = (x, y, z, s, c, sy = 0.82) => { const m = new THREE.Mesh(geo, M(c)); m.scale.set(s, s * sy, s * 0.9); m.position.set(x, y, z); m.rotation.set(r() * 3, r() * 3, r() * 3); m.castShadow = true; body.add(m); return m; };
    // the base: flattened puffs; the body: a column that narrows a little; the anvil: a flat wide top that overhangs on the right
    [[-0.85, 0.28, 0.0, 0.44], [-0.3, 0.24, 0.12, 0.46], [0.3, 0.25, 0.1, 0.46], [0.85, 0.28, -0.02, 0.44], [0, 0.3, -0.25, 0.5]].forEach(([x, y, z, s]) => puff(x, y, z, s, C[2], 0.62));
    [[-0.62, 0.72, 0.0, 0.56], [0.6, 0.7, 0.02, 0.56], [0.0, 0.8, -0.12, 0.6], [-0.3, 1.12, -0.05, 0.5], [0.32, 1.14, -0.08, 0.52], [0.0, 1.05, -0.3, 0.55], [-0.95, 0.55, -0.05, 0.36], [0.98, 0.52, -0.05, 0.38]]
      .forEach(([x, y, z, s], i) => puff(x, y, z, s, C[i % 2]));
    const anvil = new THREE.Mesh(new THREE.CylinderGeometry(1.3, 0.78, 0.26, 11), M(C[0])); anvil.scale.set(1.22, 1, 0.82); anvil.position.set(0.12, 1.46, -0.08); anvil.castShadow = true; body.add(anvil);
    // (pass 1) a soft dome on the anvil (the flat cap read as a tabletop), with three low bumps
    const cap = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 2), M(TOP)); cap.scale.set(1.62, 0.3, 1.08); cap.position.set(0.12, 1.57, -0.08); cap.castShadow = true; body.add(cap);
    // (pass 2) the bumps smooth and unrotated (a flat-shaded tilted facet read as a crater from above), plus a low crown filling the middle
    [[-0.6, 1.74, 0.0, 0.46], [0.5, 1.76, -0.15, 0.5], [1.15, 1.67, 0.05, 0.36], [-0.05, 1.72, -0.1, 0.62]].forEach(([x, y, z, s]) => { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 2), M(TOP)); m.scale.set(s, s * 0.4, s * 0.85); m.position.set(x, y, z); m.castShadow = true; body.add(m); });
    for (let i = 0; i < 9; i++) { const a = i / 9 * TAU; puff(0.12 + Math.cos(a) * 1.2, 1.42, -0.08 + Math.sin(a) * 0.8, 0.3, C[1], 0.55); }
    // the face: a box plate on the front, a little lighter than the body
    const face = grp(); face.position.set(0, 0.82, 0.68); body.add(face);
    const plate = box(1.0, 0.66, 0.14, tc(o.plate || '#4A4C52'), { outline: 0.012, unique: true }); lit.push(plate.material); face.add(plate);
    const eyeW = mat('#FBFBF6'), ink = mat('#0D0E12'), plateM = plate.material;
    const eyes = [-1, 1].map(s => { const e = grp(); e.position.set(0.21 * s, 0.07, 0.075); face.add(e);
      const white = box(0.22, 0.22, 0.03, '#FBFBF6', { material: eyeW }), pup = box(0.09, 0.1, 0.02, '#0D0E12', { material: ink }); pup.position.z = 0.018; e.add(white, pup);
      const lid = box(0.24, 0.23, 0.035, '#4A4C52', { material: plateM }); lid.geometry.translate(0, -0.115, 0); lid.position.set(0, 0.115, 0.022); e.add(lid);
      return { e, pup, lid }; });
    const brows = [-1, 1].map(s => { const b = box(0.3, 0.075, 0.05, '#0D0E12', { material: ink }); b.position.set(0.21 * s, 0.25, 0.08); face.add(b); return b; });
    const mouth = grp(); mouth.position.set(0, -0.18, 0.075); face.add(mouth);
    const mseg = [-1, 0, 1].map(i => { const m = box(0.1, 0.05, 0.03, '#0D0E12', { material: ink }); mouth.add(m); return m; });
    const cav = box(1, 1, 0.02, '#0B0B0E'); cav.geometry.translate(0, -0.5, 0); mouth.add(cav);
    const glowM = new THREE.MeshBasicMaterial({ color: '#FFE97A', toneMapped: false });
    const inner = new THREE.Mesh(new THREE.PlaneGeometry(1, 1).translate(0, -0.5, 0), glowM); inner.position.z = 0.012; mouth.add(inner);
    const teeth = box(1, 1, 0.025, '#F4F2EA'); teeth.geometry.translate(0, -0.5, 0); teeth.position.z = 0.016; mouth.add(teeth);
    // (pass 2) the puffed cheeks are the plate itself swelling: two blocks of the plate's own material at its sides, at the mouth's height, that
    // push out past its edges (separate balls read as earmuffs)
    const cheekM = mat(new THREE.Color(tc(o.plate || '#4A4C52')).multiplyScalar(o.cheekK ?? 0.85).getStyle(), { unique: true }); lit.push(cheekM);
    const cheeks = [-1, 1].map(s => { const c = box(0.22, 0.36, 0.13, '', { material: cheekM, outline: 0.012, taper: { x: 0.8, z: 0.9 } }); c.rotation.z = s * 0.12; c.position.set(0.4 * s, -0.13, 0.0); face.add(c); return c; });
    // the bolt arms: yellow zigzags pointing along -Y from the shoulder, aimed by direction
    const BOLT = poly([[-0.06, 0], [0.1, 0], [0.035, -0.26], [0.15, -0.26], [-0.07, -0.74], [0.0, -0.37], [-0.12, -0.37]]);
    const boltM = mat('#F6C518', { emissive: '#6E5200' }), steel = mat('#C9CED6'), arms = [], AL = o.armLen ?? 1.3;
    [-1, 1].forEach(s => {
      const sh = grp(); sh.position.set(0.98 * s, 0.75, 0.18); body.add(sh);
      const b = new THREE.Mesh(new THREE.ExtrudeGeometry(BOLT, { depth: 0.07, bevelEnabled: false }), boltM); b.geometry.translate(0, 0, -0.035); b.scale.set((s > 0 ? -1 : 1) * 1.35, AL, 1.3); b.castShadow = true; addOutline(b, 0.03); sh.add(b);
      const arm = { sh, s, extra: grp() }; sh.add(arm.extra); arms.push(arm);
    });
    // the handcuffs: one big steel ring round each bolt tip, a chain between them (in the body frame)
    const cuffs = [], chain = [];
    if (o.cuffs) {
      arms.forEach(a => { const c = grp(torus(0.17, 0.05, '#B9BEC6', 6, 16), at(box(0.13, 0.1, 0.11, '#7E848C', { outline: 0.01 }), 0.2, 0, 0)); c.children[0].rotation.x = PI / 2; c.position.set(0, -0.6 * AL, 0); a.sh.add(c); cuffs.push(c); });
      for (let i = 0; i < 5; i++) { const l = torus(0.06, 0.02, '#6E747C', 4, 10); body.add(l); chain.push(l); }
    }
    // the electronic tag: a black box with a green lamp, strapped round the right arm
    let lamp = null, lampGlow = null;
    if (o.tag) { const a = arms[(o.tagSide ?? 1) < 0 ? 0 : 1]; const t = grp(at(torus(0.075, 0.025, '#1C1D21', 5, 14), 0, 0, 0, PI / 2, 0, 0), at(box(0.2, 0.13, 0.11, '#1E1F24', { outline: 0.01 }), 0.0, 0, 0.1));
      const ls = o.lampS ?? 1; lamp = sphere(0.032 * ls, '#3CE06A', 1, { emissive: '#2AD05A', unique: true }); lamp.position.set(0.04, 0.02, 0.16); t.add(lamp);
      lampGlow = softSprite('#6BFF94', 0.85); lampGlow.scale.set(0.16 * ls, 0.16 * ls, 1); lampGlow.position.set(0.04, 0.02, 0.2); t.add(lampGlow);
      t.position.set(0, -0.38 * AL, 0); t.rotation.y = o.tagYaw ?? 0; t.scale.setScalar(o.tagS ?? 1.3); a.sh.add(t); }
    // the bundle: a red cloth with white dots, knotted, hanging from the left arm's tip
    if (o.bundle) { const cv = canvasPlane(0.2, 0.2, (c, W, H) => { c.fillStyle = '#C8322A'; c.fillRect(0, 0, W, H); c.fillStyle = '#F4F1E8'; for (let i = 0; i < 5; i++) for (let j = 0; j < 5; j++) if ((i + j) % 2 === 0) { c.beginPath(); c.arc((i + 0.5) * W / 5, (j + 0.5) * H / 5, W * 0.045, 0, TAU); c.fill(); } }, { res: 128 });
      const bm = new THREE.MeshLambertMaterial({ map: cv.material.map }); const bun = new THREE.Mesh(new THREE.IcosahedronGeometry(0.16, 1), bm); bun.scale.set(1, 0.85, 1); bun.position.set(0, -0.98 * AL, 0); bun.castShadow = true;
      const knot = new THREE.Mesh(new THREE.IcosahedronGeometry(0.07, 0), bm); knot.position.set(0, -0.1 * AL, 0); bun.position.set(0, -0.28 * AL, 0);
      const bg = grp(bun, knot, segment([0, 0, 0], [0, -0.12 * AL, 0], 0.012, mat('#3A2A1A')));
      // (final pass) o.bundleStick: the knot tied in two ears on top of the bundle, a wooden stick through it (a bindle, not a ball)
      if (o.bundleStick) { knot.position.set(0, -0.28 * AL + 0.13, 0); [-1, 1].forEach(e => { const ear = new THREE.Mesh(new THREE.IcosahedronGeometry(0.05, 0), bm); ear.scale.set(0.7, 1.6, 0.7); ear.rotation.z = -e * 0.7; ear.position.set(e * 0.06, -0.28 * AL + 0.19, 0); bg.add(ear); });
        bg.children[2].visible = false; bg.add(segment([-0.05, 0.12, 0.02], [0.05, -0.28 * AL + 0.16, 0.02], 0.02, mat('#7A5230'))); } bg.position.set(0, -0.7 * AL, 0); bg.scale.setScalar(o.bundleS ?? 1); arms[0].sh.add(bg); }
    const V3 = THREE.Vector3, down = new V3(0, -1, 0), tips = [new V3(), new V3()];
    g.userData.update = t => {
      const sq = keyVec(o.sq, t, [1, 1, 1], 0.15), br = 1 + 0.02 * Math.sin(t * 2.1 + (o.seed || 0));
      body.scale.set(sq[0] * br, sq[1] * (2 - br), sq[2] * br);
      body.position.y = (o.bob ?? 0.04) * Math.sin(t * 1.7 + (o.seed || 0));
      const stn = keyAt(o.strain, t, 0, 0.12);
      body.rotation.z = keyAt(o.lean, t, 0, 0.25) + 0.02 * Math.sin(t * 1.1) + stn * 0.03 * Math.sin(t * 47); body.rotation.x = 0.015 * Math.sin(t * 0.9) + stn * 0.012 * Math.sin(t * 39);
      if (stn) { body.scale.x *= 1 + stn * 0.02 * Math.sin(t * 61); body.position.x = stn * 0.012 * Math.sin(t * 53); }
      // the face
      const e0 = (o.expr && o.expr.length) ? o.expr[0][1] : 'angry'; let name = e0; for (const [kt, kv] of o.expr || []) if (t >= kt) name = kv;
      const prevName = (() => { let p = e0, q = e0; for (const [kt, kv] of o.expr || []) if (t >= kt) { p = q; q = kv; } return p; })();
      const kt0 = (() => { let a = -1e9; for (const [kt] of o.expr || []) if (t >= kt) a = kt; return a; })();
      const A = TFACE[prevName] || TFACE.angry, B = TFACE[name] || TFACE.angry, w = smooth((t - kt0) / 0.1), F = A.map((x, i) => x + (B[i] - x) * w);
      const open = clamp01(F[4] + keyAt(o.mouth, t, 0, 0.06));
      brows.forEach((b, i) => { const s = i ? 1 : -1; b.rotation.z = s * F[0]; b.position.y = 0.25 + F[1]; });
      const gl = keyVec(o.look, t, [0, 0], 0.1);
      let blink = false; if (o.blinks) blink = o.blinks.some(b => t >= b && t < b + (o.blinkDur ?? 0.1)); else blink = ((t + (o.seed || 0) * 0.41) % 3.3) < 0.09;
      eyes.forEach(e => { e.pup.position.x = 0.055 * gl[0]; e.pup.position.y = -0.055 * gl[1] - 0.01; e.lid.scale.y = blink ? 1 : Math.max(0.02, F[2]); });
      const mw = F[3] * (1 - 0.45 * F[6]), cu = F[5], th = THICK[name] || 1;
      mseg[1].scale.set(mw * 0.5 / 0.1, th, 1); mseg[1].position.set(0, 0, 0);
      [0, 2].forEach((i, j) => { const s = j ? 1 : -1, m = mseg[i]; m.scale.set(mw * 0.3 / 0.1, th, 1); m.position.set(s * (mw * 0.25 + mw * 0.13 * Math.cos(cu)), mw * 0.13 * Math.sin(cu) * 0.9, 0); m.rotation.z = s * cu; });
      // (final pass) shut: a tight wavy pressed line (the three segments zigzag)
      if (name === 'shut') { mseg[0].rotation.z = 0.42; mseg[1].rotation.z = -0.42; mseg[2].rotation.z = 0.42; mseg.forEach((m, i) => { m.position.y = 0; m.scale.y = 1.3; }); }
      mseg.forEach(m => { m.visible = open < 0.08; });
      const oh = 0.04 + 0.3 * open, ow = Math.max(mw, 0.2 + 0.12 * open);
      cav.visible = inner.visible = teeth.visible = open >= 0.08; cav.scale.set(ow, oh, 1); cav.position.y = 0.02;
      inner.scale.set(ow * 0.84, oh * 0.8, 1); inner.position.y = 0.02 - oh * 0.12; teeth.scale.set(ow * 0.9, Math.min(0.05, oh * 0.25), 1); teeth.position.y = 0.02;
      const ck = F[6] * (1 + 0.08 * Math.sin(t * 9) * (stn ? 1 : 0)); plate.scale.set(1 + 0.08 * ck, 1 - 0.04 * ck, 1);
      cheeks.forEach((c, i) => { const s = i ? 1 : -1; c.visible = ck > 0.05; c.scale.set(0.4 + 0.6 * ck, 0.5 + 0.5 * ck, 1); c.position.x = s * (0.42 + 0.1 * ck); });
      // the arms
      const P = (() => { const a0 = (o.arms && o.arms.length) ? [o.arms[0][1], o.arms[0][2] ?? o.arms[0][1]] : ['rest', 'rest']; let p = a0, q = a0, k0 = -1e9; for (const k of o.arms || []) if (t >= k[0]) { p = q; q = [k[1], k[2] ?? k[1]]; k0 = k[0]; } return [p, q, k0]; })();
      const aw = smooth((t - P[2]) / 0.16);
      arms.forEach((a, i) => { const pick = n => { const d = TARMS[n] || TARMS.rest; return new V3(i ? -d[0] : d[0], d[1], d[2]); };
        const d = pick(P[0][i]).lerp(pick(P[1][i]), aw).normalize(); const wob = 0.12 * Math.sin(t * 5 + i * 2); d.x += wob * 0.2; d.normalize();
        a.sh.quaternion.setFromUnitVectors(down, d); tips[i].copy(a.sh.position).addScaledVector(d, 0.6 * AL); });
      if (cuffs.length) { const ca = o.cuffsAt ?? -1, u = clamp01((t - ca) / 0.18), s = t < ca ? 0.001 : outBack(u); cuffs.forEach(c => c.scale.setScalar(Math.max(0.001, s)));
        chain.forEach((l, j) => { const f = (j + 1) / (chain.length + 1); l.position.lerpVectors(tips[0], tips[1], f); l.position.y -= 0.12 * Math.sin(f * PI); l.position.z += 0.02; l.rotation.set(j % 2 ? PI / 2 : 0, 0, 0); l.visible = t >= ca; }); }
      if (lamp) { lamp.visible = (t % 0.6) < 0.3; lampGlow.visible = lamp.visible; }
      const fl = pulseAt(o.flash, t) * (o.flashK ?? 1), gw = o.glow ?? 0; lit.forEach(m => m.emissive.setRGB(0.9 * fl + 0.17 * gw + EM.r, 0.85 * fl + 0.17 * gw + EM.g, 0.55 * fl + 0.18 * gw + EM.b));
    };
    if (o.shadows === false) g.traverse(c => { c.castShadow = false; c.receiveShadow = false; });
    if (cuffs.length) { cuffs.forEach(noShadow); chain.forEach(noShadow); }
    g.userData.update(0); return g;
  },

  // A shockwave: o.n (3) rings that leave the origin along +Z, grow from o.r0 (0.3) to o.r (5) and fade, o.dur (0.55) each, 0.07 s apart from o.at;
  // a white glow at the origin on the blast. Rings: a pale band with a darker blue edge so they read on pale walls
  shockRing(o) {
    const g = grp(), n = o.n ?? 3, at0 = o.at ?? 0, dur = o.dur ?? 0.55, R0 = o.r0 ?? 0.3, R1 = o.r ?? 5, tr = o.travel ?? 2.5, rings = [];
    for (let i = 0; i < n; i++) {
      const band = new THREE.Mesh(new THREE.RingGeometry(0.8, 1.0, 64), basic(o.color || '#E6F6FF', 0.7)), edge = new THREE.Mesh(new THREE.RingGeometry(1.0, 1.05, 64), basic(o.edge || '#3B88C9', 0.9));
      const inr = new THREE.Mesh(new THREE.RingGeometry(0.76, 0.8, 64), basic(o.edge || '#3B88C9', 0.6));
      const rg = grp(band, edge, inr); rg.renderOrder = 5; noShadow(rg); g.add(rg); rings.push({ rg, mats: [band.material, edge.material, inr.material] });
    }
    const core = softSprite('#FFFFFF', 1); g.add(core); const core2 = softSprite(o.coreColor || '#FFF2A8', 1); g.add(core2);
    g.userData.update = t => {
      rings.forEach((R, i) => { const u = (t - at0 - 0.07 * i) / dur; R.rg.visible = u >= 0 && u < 1; if (!R.rg.visible) return;
        const s = R0 + (R1 - R0) * easeOut(u) * (1 - 0.18 * i); R.rg.scale.set(s, s, 1); R.rg.position.z = tr * u; const a = 1 - smooth((u - 0.35) / 0.65); R.mats[0].opacity = 0.7 * a; R.mats[1].opacity = 0.95 * a; R.mats[2].opacity = 0.6 * a; });
      const u = (t - at0) / 0.3; core.visible = core2.visible = u >= 0 && u < 1; if (core.visible) { const s = (o.core ?? 1.6) * (0.4 + easeOut(u)); core.scale.set(s, s, 1); core2.scale.set(s * 1.5, s * 1.5, 1); core.material.opacity = 1 - u; core2.material.opacity = 0.7 * (1 - u); }
    };
    g.userData.update(-1); return g;
  },

  // A lightning bolt from o.from to o.to (local points): a jagged white-hot core in a yellow glow, with a fork; shown during [o.at, o.at + o.dur]
  // (0.3) with one flicker; o.w (0.06) core radius, o.jag (0.18) jitter of the bends, o.seed
  boltStrike(o) {
    const g = grp(), a = o.from || [0, 3, 0], b = o.to || [0, 0, 0], n = o.n ?? 9, q = rng(o.seed || 5), jag = o.jag ?? 0.18, W = o.w ?? 0.06;
    const coreM = basic('#FFFBE8', 1), glowM = basic('#FFE04A', 0.5, { blending: THREE.AdditiveBlending });
    const pts = []; for (let i = 0; i <= n; i++) { const f = i / n, j = i === 0 || i === n ? 0 : 1; pts.push([a[0] + (b[0] - a[0]) * f + (q() - 0.5) * 2 * jag * j * (o.span ?? 1), a[1] + (b[1] - a[1]) * f + (q() - 0.5) * jag * 0.5 * j, a[2] + (b[2] - a[2]) * f + (q() - 0.5) * 2 * jag * j * 0.5]); }
    for (let i = 0; i < n; i++) { g.add(segment(pts[i], pts[i + 1], W, coreM), segment(pts[i], pts[i + 1], W * 3.2, glowM)); }
    const m = pts[Math.floor(n / 2)], fk = [m[0] + (q() - 0.3) * 1.2 * jag * 5, m[1] - Math.abs(b[1] - a[1]) * 0.22, m[2]];
    const mid = [(m[0] + fk[0]) / 2 + jag, (m[1] + fk[1]) / 2, m[2]]; g.add(segment(m, mid, W * 0.7, coreM), segment(mid, fk, W * 0.6, coreM), segment(m, mid, W * 2.2, glowM), segment(mid, fk, W * 2, glowM));
    const halo = softSprite('#FFF4B8', 0.9); halo.position.set(...b); halo.scale.set(1.5, 1.5, 1); g.add(halo);
    noShadow(g);
    g.userData.update = t => { const u = (t - (o.at ?? 0)) / (o.dur ?? 0.3); g.visible = u >= 0 && u < 1 && !(u > 0.38 && u < 0.52); };
    g.userData.update(-1); return g;
  },

  // The hero's bedroom by night (pivot at the middle of the floor; the back wall at z = -3, the room from x -3.5 to 3.5): a double bed against the
  // back wall (its middle at x = o.bedX, 0; the mattress top at 0.62, the pillows at z -2.65, the duvet over the bodies from z o.duvetZ (-2.2) to the
  // foot, its top at o.duvetTop (0.88)), a window cut in the back wall on the bed's left (o.winX -1.45, 0.95 x 1.15) on a night sky with a moon
  // (o.flash [[t, dur]]: the sky turns white, a bolt in it), a door on the right (o.doorX 2.15), bedside tables, a lamp on the right (o.lamp)
  tonBedroom(o) {
    const g = grp(), WALL = o.wall || '#8592BA', DADO = o.dado || '#6B78A0', H = o.wallH ?? 5.0, bz = -3.0, wx = o.winX ?? -1.45, ww = o.winW ?? 0.95, wy0 = 1.15, wy1 = wy0 + (o.winH ?? 1.15);
    g.add(at(box(7.2, 0.06, 6.8, o.floor || '#8C6A4C'), 0, -0.02, 0.2));
    const wallPiece = (x0, x1, y0, y1) => { if (x1 - x0 < 0.01 || y1 - y0 < 0.01) return; g.add(at(box(x1 - x0, y1 - y0, 0.2, WALL), (x0 + x1) / 2, (y0 + y1) / 2, bz - 0.1)); };
    wallPiece(-3.6, wx - ww / 2, 0, H); wallPiece(wx + ww / 2, 3.6, 0, H); wallPiece(wx - ww / 2, wx + ww / 2, 0, wy0); wallPiece(wx - ww / 2, wx + ww / 2, wy1, H);
    [-1, 1].forEach(s => g.add(at(box(0.2, H, 6.8, WALL), s * 3.6, H / 2, 0.2)));
    g.add(at(box(7.0, 0.9, 0.02, DADO), 0, 0.45, bz + 0.01), at(box(7.0, 0.05, 0.04, '#E8E4DA'), 0, 0.92, bz + 0.02));
    [-1, 1].forEach(s => g.add(at(box(0.02, 0.9, 6.6, DADO), s * 3.49, 0.45, 0.2), at(box(0.04, 0.05, 6.6, '#E8E4DA'), s * 3.48, 0.92, 0.2)));
    // the window: a white frame, a cross, a sill, two curtains; outside a night sky (unlit) with a moon, rooftops, and a flash
    const fr = '#EDEBE4';
    g.add(at(box(ww + 0.16, 0.08, 0.12, fr), wx, wy1 + 0.04, bz + 0.02), at(box(ww + 0.26, 0.07, 0.2, fr), wx, wy0 - 0.03, bz + 0.06));
    [-1, 1].forEach(s => g.add(at(box(0.08, wy1 - wy0, 0.12, fr), wx + s * (ww / 2 + 0.04), (wy0 + wy1) / 2, bz + 0.02)));
    g.add(at(box(0.04, wy1 - wy0, 0.05, fr), wx, (wy0 + wy1) / 2, bz - 0.06), at(box(ww, 0.04, 0.05, fr), wx, wy0 + (wy1 - wy0) * 0.55, bz - 0.06));
    if (o.curtains !== false) [-1, 1].forEach(s => g.add(at(box(0.32, wy1 - wy0 + 0.5, 0.06, o.curtain || '#8E2E3A', { outline: 0.006 }), wx + s * (ww / 2 + 0.24), (wy0 + wy1) / 2 + 0.05, bz + 0.1)));
    const SW = o.skyW ?? 14, SH = o.skyH ?? 9, sz = o.skyZ ?? -9;
    const sky = canvasPlane(SW, SH, (c, Wp, Hp) => { const gr = c.createLinearGradient(0, 0, 0, Hp); gr.addColorStop(0, o.skyTop || '#1C2A58'); gr.addColorStop(1, o.skyBottom || '#4E68B0'); c.fillStyle = gr; c.fillRect(0, 0, Wp, Hp);
      const q = rng(11); c.fillStyle = 'rgba(255,250,232,0.9)'; for (let i = 0; i < 60; i++) { const s = Wp * (0.002 + 0.002 * q()); c.fillRect(q() * Wp, q() * Hp * 0.6, s, s); }
      if (o.moon !== false) { const [mu, mv, mr] = o.moonAt || [0.44, 0.3, 0.035]; const hg = c.createRadialGradient(mu * Wp, mv * Hp, 1, mu * Wp, mv * Hp, mr * Wp * 3); hg.addColorStop(0, 'rgba(244,239,216,0.55)'); hg.addColorStop(1, 'rgba(244,239,216,0)'); c.fillStyle = hg; c.fillRect(0, 0, Wp, Hp);
        c.fillStyle = '#F4EFD8'; c.beginPath(); c.arc(mu * Wp, mv * Hp, mr * Wp, 0, TAU); c.fill(); }
      c.fillStyle = o.roofs || '#141B33'; let x = 0; const q2 = rng(4); while (x < Wp) { const w = Wp * (0.06 + 0.06 * q2()), h = Hp * (0.12 + 0.12 * q2()); c.fillRect(x, Hp - h, w, h); if (q2() > 0.5) c.fillRect(x + w * 0.3, Hp - h - Hp * 0.03, w * 0.12, Hp * 0.03); x += w; }
      c.fillStyle = '#E9C76A'; const q3 = rng(8); for (let i = 0; i < 26; i++) c.fillRect(q3() * Wp, Hp * (0.8 + 0.17 * q3()), Wp * 0.006, Hp * 0.01); }, { res: 768 });
    sky.material = new THREE.MeshBasicMaterial({ map: sky.material.map, toneMapped: false, fog: false }); sky.position.set(wx, 1.6, sz); noShadow(sky); g.add(sky);
    const flashM = basic('#FFFFFF', 0); const flashP = new THREE.Mesh(new THREE.PlaneGeometry(SW, SH), flashM); flashP.position.set(wx, 1.6, sz + 0.05); g.add(flashP);
    const sb = TONNERRE_PROPS.boltStrike({ from: [wx - 0.9, 4.6, sz + 0.2], to: [wx - 0.2, 0.2, sz + 0.2], w: 0.06, jag: 0.35, at: -10, dur: 0.01, seed: 3 }); g.add(sb);
    // the bed
    const bx = o.bedX ?? 0, BW = 1.8, L = 2.1, bz0 = bz, bz1 = bz + L, wood = o.wood || '#6E4A30';
    g.add(at(box(BW + 0.12, 0.28, L + 0.06, wood, { pivot: 'bottom', outline: 0.006 }), bx, 0.12, (bz0 + bz1) / 2));
    [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([sx, sz2]) => g.add(at(box(0.08, 0.14, 0.08, wood, { pivot: 'bottom' }), bx + sx * (BW / 2), 0, sz2 > 0 ? bz1 - 0.04 : bz0 + 0.06)));
    g.add(at(box(BW, 0.22, L - 0.04, '#F1EEE6', { pivot: 'bottom' }), bx, 0.4, (bz0 + bz1) / 2 + 0.02));
    g.add(at(box(BW + 0.16, 1.15, 0.1, o.headboard || '#5A3A26', { pivot: 'bottom', outline: 0.008 }), bx, 0.2, bz0 + 0.05), at(box(BW + 0.24, 0.08, 0.14, wood), bx, 1.37, bz0 + 0.05));
    if (o.pillows !== false) [-1, 1].forEach(s => { const p = at(box(0.66, 0.16, 0.42, '#FAF8F2', { outline: 0.008, taper: { x: 0.92, z: 0.85 } }), bx + s * 0.45, 0.72, bz0 + 0.33, -0.3, 0, 0); g.add(p); });
    const chests = [];
    if (o.duvet !== false) {
      const dz0 = o.duvetZ ?? -2.2, top = o.duvetTop ?? 0.88, dl = bz1 + 0.06 - dz0, dc = o.duvet || '#E2C277';
      g.add(at(box(BW + 0.14, top - 0.34, dl, dc, { pivot: 'bottom', outline: 0.008 }), bx, 0.34, dz0 + dl / 2));
      g.add(at(box(BW + 0.16, 0.07, 0.3, '#F7F4EC', { outline: 0.006 }), bx, top + 0.005, dz0 + 0.15));
      // (pass 1) o.chest [[x, z, r]]: a hump over a sleeper's chest that rises and falls (a slow breath, o.breath 3.2 s)
      for (const [cx, cz, cr] of o.chest || []) { const c = sphere(cr ?? 0.3, dc, 1); c.scale.set(1.2, 0.5, 1.5); c.position.set(bx + cx, top - 0.06, cz); g.add(c); chests.push(c); }
      for (const [fx, fz, fr] of o.feet || []) { const f = sphere(fr ?? 0.13, dc, 1); f.scale.set(1.1, 0.75, 1.3); f.position.set(bx + fx, top, fz); g.add(f); }
      const st = mat(new THREE.Color(dc).multiplyScalar(0.86).getStyle()); for (let i = 1; i < 4; i++) g.add(at(box(BW + 0.15, 0.012, 0.03, '', { material: st }), bx, top + 0.003, dz0 + dl * i / 4));
    }
    // bedside tables, the lamp on the right, the door
    [-1, 1].forEach(s => { const x = bx + s * 1.25; g.add(at(box(0.48, 0.55, 0.42, wood, { pivot: 'bottom', outline: 0.006 }), x, 0, bz0 + 0.26), at(box(0.3, 0.02, 0.01, '#C9A86A'), x, 0.38, bz0 + 0.475)); });
    const lx = bx + 1.25; g.add(at(cyl(0.07, 0.09, 0.05, '#3A3A3E', 8, { pivot: 'bottom' }), lx, 0.55, bz0 + 0.22), at(cyl(0.012, 0.012, 0.32, '#3A3A3E', 5, { pivot: 'bottom' }), lx, 0.6, bz0 + 0.22));
    const on = o.lamp !== false; g.add(at(cyl(0.11, 0.17, 0.2, on ? '#FFE6A8' : '#D9CFB4', 10, { pivot: 'bottom', emissive: on ? '#E8B860' : undefined }), lx, 0.86, bz0 + 0.22));
    if (on && o.lampLight !== false) { const l = new THREE.PointLight('#FFC97A', o.lampPower ?? 3, 5, 1.4); l.position.set(lx, 1.0, bz0 + 0.4); g.add(l); }
    if (o.door !== false) { const dx = o.doorX ?? 2.15; g.add(at(box(0.95, 2.15, 0.06, '#EDEBE4'), dx, 1.075, bz + 0.02), at(box(0.83, 2.05, 0.05, o.doorColor || '#9A6B45', { outline: 0.006 }), dx, 1.03, bz + 0.05),
      at(box(0.62, 0.7, 0.012, '#87593A'), dx, 1.55, bz + 0.08), at(box(0.62, 0.7, 0.012, '#87593A'), dx, 0.6, bz + 0.08), at(sphere(0.04, '#D8B54A', 0), dx - 0.32, 1.0, bz + 0.1)); }
    g.userData.update = t => { chests.forEach(c => { c.scale.y = 0.5 + 0.12 * Math.sin(t * TAU / (o.breath ?? 3.2)); }); const f = pulseAt(o.flash, t); flashM.opacity = 0.95 * f; flashP.visible = f > 0.001; sb.visible = (o.flash || []).some(([a, d]) => t >= a && t < a + Math.min(0.2, d)); };
    g.userData.update(0); return g;
  },

  // A block's facade whose windows pop out (pivot at the foot of the facade, the middle; it faces +Z): o.w (12) x o.h (13), o.floors (4) x o.cols (4)
  // tall windows with white frames and pale blue glass, a cornice, a darker ground floor; at o.popAt (+ up to 0.05 s at random) every pane flies out
  // (o.kick 0.6 m/s forward) and falls (o.grav 12) to the pavement at y = 0 (o.walk: it lands about that far in front) and breaks into glinting
  // shards; the openings stay dark. o.color, o.glass, o.winW (m), o.winH (fraction of a floor)
  popFacade(o) {
    const W = o.w ?? 12, H = o.h ?? 13, F = o.floors ?? 4, Cn = o.cols ?? 4, g = grp(), q = rng(o.seed || 17), col = o.color || '#EADFC8';
    g.add(at(box(W, H, 0.6, col, { outline: 0.01 }), 0, H / 2, -0.3), at(box(W + 0.3, 0.35, 0.8, '#D8CBB0', { outline: 0.008 }), 0, H - 0.2, -0.3), at(box(W, 2.6, 0.04, o.ground || '#B9AA8E'), 0, 1.3, 0.01));
    const fh = (H - 3.0) / F, cw = W / Cn, wW = o.winW ?? Math.min(1.2, cw * 0.48), wH = fh * (o.winH ?? 0.62), panes = [];   // (pass 2) o.winW / o.winH: bigger windows
    const glassM = mat(o.glass || '#8FB9D8', { emissive: '#203040' }), frameM = mat('#F6F3EC'), holeM = mat('#262B33'), shardM = basic('#CDE6F5', 0.9);
    for (let f = 0; f < F; f++) for (let c = 0; c < Cn; c++) {
      const x = -W / 2 + (c + 0.5) * cw, y = 3.0 + f * fh + fh * 0.2 + wH / 2;
      g.add(at(box(wW, wH, 0.02, '', { material: holeM }), x, y, 0.005), at(box(wW + 0.2, 0.1, 0.18, '#E4DACA'), x, y - wH / 2 - 0.05, 0.08));
      const pn = grp(at(box(wW, wH, 0.04, '', { material: glassM }), 0, 0, 0), at(box(wW + 0.08, 0.07, 0.07, '', { material: frameM }), 0, wH / 2, 0), at(box(wW + 0.08, 0.07, 0.07, '', { material: frameM }), 0, -wH / 2, 0),
        at(box(0.07, wH, 0.07, '', { material: frameM }), -wW / 2, 0, 0), at(box(0.07, wH, 0.07, '', { material: frameM }), wW / 2, 0, 0), at(box(0.05, wH, 0.06, '', { material: frameM }), 0, 0, 0), at(box(wW, 0.05, 0.06, '', { material: frameM }), 0, wH * 0.15, 0));
      pn.position.set(x, y, 0.06); g.add(pn);
      const sh = grp(); for (let i = 0; i < 7; i++) { const s = new THREE.Mesh(new THREE.CircleGeometry(0.12 + 0.12 * q(), 3), shardM); s.rotation.set(-PI / 2, 0, q() * TAU); s.position.set((q() - 0.5) * 1.2, 0.02 + 0.004 * i, (q() - 0.5) * 0.7); sh.add(s); }
      sh.add(at(box(wW * 0.9, 0.05, 0.08, '', { material: frameM }), (q() - 0.5) * 0.4, 0.03, 0, 0, q() * 2, 0)); sh.visible = false; g.add(sh);
      panes.push({ pn, sh, x, y, dt: q() * 0.05, spin: (q() - 0.5) * 3, tilt: 0.8 + q() * 0.9, vz: (o.kick ?? 0.6) * (0.8 + 0.5 * q()) });
    }
    const G = o.grav ?? 12, glint = [];
    g.userData.update = t => panes.forEach(P => {
      const u = t - (o.popAt ?? 1e9) - P.dt;
      if (u < 0) { P.pn.position.set(P.x, P.y, 0.06); P.pn.rotation.set(0, 0, 0); P.pn.visible = true; P.sh.visible = false; return; }
      const yy = P.y + 1.2 * u - 0.5 * G * u * u, land = yy <= 0.08;
      if (land) { P.pn.visible = false; P.sh.visible = true; const tl = (1.2 + Math.sqrt(1.44 + 2 * G * (P.y - 0.08))) / G; P.sh.position.set(P.x, 0, 0.06 + 0.4 + P.vz * tl); return; }
      P.pn.visible = true; P.sh.visible = false; P.pn.position.set(P.x + P.spin * 0.05 * u, yy, 0.06 + 0.4 * Math.min(1, u * 8) + P.vz * u); P.pn.rotation.set(P.tilt * u * 1.6, P.spin * u * 0.3, P.spin * u * 0.4);
    });
    void glint; g.userData.update(0); return g;
  },

  // The jury stand: o.tiers (3) wooden tiers rising to the back (o.step 0.42 high, o.deep 0.85 deep), o.w (3.2) wide, each with a bench and a front
  // panel (o.panel 0.62 high over its tier); pivot at the floor, front middle; the jurors face +Z. Tier i's floor: y = i * step, z = -(i + 0.5) * deep
  juryTiers(o) {
    const g = grp(), n = o.tiers ?? 3, st = o.step ?? 0.42, dp = o.deep ?? 0.85, W = o.w ?? 3.2, c = o.color || '#7A4E2E', c2 = o.color2 || '#5E3A20', ph = o.panel ?? 0.62;
    for (let i = 0; i < n; i++) {
      const y = i * st, z = -(i + 0.5) * dp;
      if (i > 0) g.add(at(box(W, y, dp, c2, { pivot: 'bottom' }), 0, 0, z));
      g.add(at(box(W, 0.45, 0.38, c2, { pivot: 'bottom', outline: 0.006 }), 0, y, z - dp * 0.2));
      g.add(at(box(W + 0.08, ph, 0.06, c, { pivot: 'bottom', outline: 0.008 }), 0, y, z + dp / 2 - 0.03), at(box(W + 0.14, 0.06, 0.12, c2), 0, y + ph, z + dp / 2 - 0.03));
    }
    [-1, 1].forEach(s => g.add(at(box(0.08, n * st + ph, n * dp, c, { pivot: 'bottom', outline: 0.006 }), s * (W / 2 + 0.04), 0, -n * dp / 2)));
    return g;
  },

  // A small open booklet held up (pivot at its spine's middle; open toward +Z, pages in the XY plane): o.w (0.3) per page x o.h (0.4); one page turns
  // from right to left at o.flipAt over o.flipDur (0.45)
  pageBook(o) {
    const w = o.w ?? 0.3, h = o.h ?? 0.4, g = grp(), page = side => canvasPlane(w, h, (c, W, Hh) => { c.fillStyle = '#F7F4EA'; c.fillRect(0, 0, W, Hh); c.fillStyle = '#7A7A80'; for (let i = 0; i < 10; i++) c.fillRect(W * 0.12, Hh * (0.12 + i * 0.075), W * (0.76 - (i % 4 === 3 ? 0.3 : 0)), Hh * 0.018); c.strokeStyle = '#BDB6A4'; c.lineWidth = W * 0.02; c.strokeRect(0, 0, W, Hh); }, { res: 128 });
    const cover = at(box(2 * w + 0.03, h + 0.03, 0.012, o.cover || '#2E4A6E', { outline: 0.006 }), 0, 0, -0.01); g.add(cover);
    const L = page(); L.position.set(-w / 2, 0, 0.002); L.rotation.y = 0.12; const R = page(); R.position.set(w / 2, 0, 0.002); R.rotation.y = -0.12; g.add(L, R);
    const fp = grp(), fpg = page(); fpg.position.x = w / 2; fp.add(fpg); fp.position.z = 0.006; g.add(fp);
    g.userData.update = t => { const u = smooth((t - (o.flipAt ?? 1e9)) / (o.flipDur ?? 0.45)); fp.rotation.y = -0.12 - u * (PI - 0.24); fp.position.z = 0.006 + 0.04 * Math.sin(u * PI); };
    g.userData.update(0); return g;
  },

  // A big sound-level meter held up (pivot at the middle of its back; face +Z): a yellow case o.w (0.62) x o.h (0.5), a white dial with green / yellow /
  // red bands, the word DÉCIBELS, and the needle bent: it has gone past the red, through the top of the case, and sticks out crooked above it, still
  // quivering (o.twangAt: a springy shake); a thin smoke wisp from the bend
  soundMeter(o) {
    const w = o.w ?? 0.62, h = o.h ?? 0.5, g = grp(), s = o.s ?? 1; const in_ = grp(); in_.scale.setScalar(s); g.add(in_);
    in_.add(at(box(w, h, 0.16, o.color || '#F2B42A', { outline: 0.01 }), 0, 0, 0.08), at(box(w * 0.3, 0.06, 0.06, '#2A2A2E'), 0, h / 2 + 0.06, 0.08), at(box(0.04, 0.08, 0.04, '#2A2A2E'), -w * 0.13, h / 2 + 0.02, 0.08), at(box(0.04, 0.08, 0.04, '#2A2A2E'), w * 0.13, h / 2 + 0.02, 0.08));
    const dial = canvasPlane(w * 0.86, h * 0.7, (c, W, H) => { c.fillStyle = '#FAF8F0'; c.fillRect(0, 0, W, H); const cx = W / 2, cy = H * 0.92, R = W * 0.42;
      [['#4CAF50', PI * 1.08, PI * 1.45], ['#F2C230', PI * 1.45, PI * 1.68], ['#D9342B', PI * 1.68, PI * 1.92]].forEach(([cl, a0, a1]) => { c.strokeStyle = cl; c.lineWidth = W * 0.07; c.beginPath(); c.arc(cx, cy, R, a0, a1); c.stroke(); });
      c.strokeStyle = '#2A2A2E'; c.lineWidth = W * 0.012; for (let i = 0; i <= 10; i++) { const a = PI * (1.08 + 0.084 * i); c.beginPath(); c.moveTo(cx + Math.cos(a) * R * 0.78, cy + Math.sin(a) * R * 0.78); c.lineTo(cx + Math.cos(a) * R * 0.9, cy + Math.sin(a) * R * 0.9); c.stroke(); }
      c.fillStyle = '#2A2A2E'; c.font = `bold ${H * 0.13}px Arial`; c.textAlign = 'center'; c.fillText(o.text || 'DÉCIBELS', cx, H * 0.62); c.beginPath(); c.arc(cx, cy, W * 0.035, 0, TAU); c.fill(); }, { res: 384 });
    dial.position.set(0, h * 0.08, 0.162); in_.add(dial);
    const pv = [0, h * 0.08 - h * 0.35 + h * 0.7 * 0.08, 0.17], needle = grp(); needle.position.set(...pv); in_.add(needle);
    const nm = mat('#C8202A'), P1 = [0.0, 0.0, 0], P2 = [w * 0.33, h * 0.42, 0.01], P3 = [w * 0.38, h * 0.68, 0.06], P4 = [w * 0.22, h * 0.86, 0.1];
    needle.add(segment(P1, P2, 0.009, nm), segment(P2, P3, 0.009, nm), segment(P3, P4, 0.009, nm));
    in_.add(at(box(0.07, 0.03, 0.17, '#1E1E22'), P3[0] * 0.95, h / 2 + 0.005, 0.085), at(sphere(0.022, '#2A2A2E', 0), pv[0], pv[1], pv[2] + 0.005));
    const wisps = []; for (let i = 0; i < 5; i++) { const s2 = softSprite('#B9B4AA', 0.6); in_.add(s2); wisps.push(s2); }
    g.userData.update = t => { const u = t - (o.twangAt ?? 1e9); needle.rotation.z = u >= 0 ? 0.12 * Math.exp(-u * 4) * Math.sin(u * 38) : 0;
      wisps.forEach((s2, i) => { const k = ((t * 0.6 + i / 5) % 1); s2.position.set(P3[0] + 0.03 * Math.sin(t * 3 + i), pv[1] + P3[1] + 0.05 + k * 0.45, 0.12); const sc = 0.06 + 0.16 * k; s2.scale.set(sc, sc, 1); s2.material.opacity = 0.55 * (1 - k); }); };
    g.userData.update(0); return g;
  },

  // The padded cell (pivot at the middle of its floor; inside x ±o.w/2 (3.6), z from -o.d/2 to +o.d/2 (3.6), o.h (3.2) high): white quilted walls
  // and ceiling (diamond tufting, buttons, soft grey shading), a darker warm grey padded floor; a narrow padded door (o.doorW 0.85) in the front wall
  // (z = +d/2) at x = o.doorX (0) with a hatch (an opening at head height, o.hatchY 2.02); o.open [[t, 0..1]] swings the door outward (hinge on the
  // left from inside); outside, a grey corridor (o.corr 2.6 deep) with a steel-grey outer face
  paddedCell(o) {
    const W = o.w ?? 3.6, D = o.d ?? 3.6, H = o.h ?? 3.2, g = grp(), dx = o.doorX ?? 0, dW = o.doorW ?? 0.85, dH = o.doorH ?? 2.15, hy = o.hatchY ?? 2.02, hw = o.hatchW ?? 0.46, hh = o.hatchH ?? 0.36, fz = D / 2;
    // (final pass) puffy square cushions: each tile a pillow (bright middle, soft grey falling to its seams), a dark button at every seam crossing;
    // slightly self-lit (o.glowK 0.22) so the cell reads near-white
    const quilt = (w, h, base) => { const cv = document.createElement('canvas'); const res = 512; cv.width = res; cv.height = Math.max(8, Math.round(res * h / w)); const c = cv.getContext('2d'), Wp = cv.width, Hp = cv.height;
      c.fillStyle = '#C4C8CE'; c.fillRect(0, 0, Wp, Hp); const cell = Wp / Math.max(2, Math.round(w / 0.5)); const rows = Math.ceil(Hp / cell) + 1, cols = Math.ceil(Wp / cell) + 1;
      for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) { const x = (i + 0.5) * cell, y = (j + 0.5) * cell; const gr = c.createRadialGradient(x - cell * 0.12, y - cell * 0.14, cell * 0.04, x, y, cell * 0.62);
        gr.addColorStop(0, '#FFFFFF'); gr.addColorStop(0.45, base); gr.addColorStop(0.8, '#D3D6DB'); gr.addColorStop(1, '#AEB3BA'); c.fillStyle = gr; c.beginPath(); c.ellipse(x, y, cell * 0.5, cell * 0.5, 0, 0, TAU); c.fill(); c.fillRect(x - cell * 0.42, y - cell * 0.42, cell * 0.84, cell * 0.84); }
      for (let j = 0; j <= rows; j++) for (let i = 0; i <= cols; i++) { const x = i * cell, y = j * cell; c.fillStyle = 'rgba(150,156,166,0.55)'; c.beginPath(); c.arc(x, y, cell * 0.11, 0, TAU); c.fill(); c.fillStyle = '#5E646E'; c.beginPath(); c.arc(x, y, cell * 0.05, 0, TAU); c.fill(); }
      const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; return new THREE.MeshLambertMaterial({ map: tex, emissive: '#FFFFFF', emissiveMap: tex, emissiveIntensity: o.glowK ?? 0.22 }); };
    const panel = (w, h, base, x, y, z, ry = 0, rx = 0) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, 0.12), [mat(base), mat(base), mat(base), mat(base), quilt(w, h, base), mat(base)]); m.position.set(x, y, z); m.rotation.set(rx, ry, 0); m.receiveShadow = true; m.castShadow = true; g.add(m); return m; };
    const WC = o.wallColor || '#F1EFEA';
    panel(W, H, WC, 0, H / 2, -D / 2 - 0.06); panel(D, H, WC, -W / 2 - 0.06, H / 2, 0, PI / 2); panel(D, H, WC, W / 2 + 0.06, H / 2, 0, -PI / 2);
    panel(W, D, '#E9E6E0', 0, H + 0.06, 0, 0, PI / 2);
    // the front wall with the doorway, quilted inside (facing -Z), steel grey outside
    const fl = dx - dW / 2, frr = dx + dW / 2;
    const front = (x0, x1, y0, y1) => { const w = x1 - x0, h = y1 - y0; if (w < 0.01 || h < 0.01) return; panel(w, h, WC, (x0 + x1) / 2, (y0 + y1) / 2, fz + 0.06, PI); g.add(at(box(w, h, 0.04, o.outer || '#8A939C'), (x0 + x1) / 2, (y0 + y1) / 2, fz + 0.14)); };
    front(-W / 2 - 0.12, fl, 0, H + 0.12); front(frr, W / 2 + 0.12, 0, H + 0.12); front(fl, frr, dH, H + 0.12);
    g.add(at(box(dW + 0.2, 0.1, 0.36, '#6E7780'), dx, dH + 0.05, fz + 0.06));
    // the floor: padded, warm grey, darker than the walls
    const flr = new THREE.Mesh(new THREE.BoxGeometry(W, 0.1, D), [mat('#8E867C'), mat('#8E867C'), quilt(W, D, o.floor || '#A39A8E'), mat('#8E867C'), mat('#8E867C'), mat('#8E867C')]); flr.position.set(0, -0.04, 0); flr.receiveShadow = true; g.add(flr);
    // the door: padded inside, steel outside, the hatch at head height (an opening with a frame; o.hatch [[t, 0..1]]: its outer flap slides down open)
    const hinge = grp(); hinge.position.set(fl, 0, fz + 0.06); g.add(hinge);
    const leaf = (x0, x1, y0, y1) => { const w = x1 - x0, h = y1 - y0; if (w < 0.01 || h < 0.01) return; const p = new THREE.Mesh(new THREE.BoxGeometry(w, h, 0.1), [mat('#E4E1DA'), mat('#E4E1DA'), mat('#E4E1DA'), mat('#E4E1DA'), mat(o.doorOut || '#7E8892'), quilt(w, h, '#ECE9E3')]); p.position.set((x0 + x1) / 2, (y0 + y1) / 2, 0); p.castShadow = true; hinge.add(p); };
    const hx0 = dW / 2 - hw / 2, hx1 = dW / 2 + hw / 2, hy0 = hy - hh / 2, hy1 = hy + hh / 2;
    leaf(0, dW, 0, hy0); leaf(0, dW, hy1, dH); leaf(0, hx0, hy0, hy1); leaf(hx1, dW, hy0, hy1);
    [[hx0 - 0.03, hy, 0.06, hh + 0.06], [hx1 + 0.03, hy, 0.06, hh + 0.06]].forEach(([x, y, w, h]) => hinge.add(at(box(w, h, 0.14, '#5E666E'), x, y, 0)));
    hinge.add(at(box(hw + 0.12, 0.06, 0.14, '#5E666E'), dW / 2, hy1 + 0.03, 0), at(box(hw + 0.12, 0.06, 0.14, '#5E666E'), dW / 2, hy0 - 0.03, 0));
    const flap = at(box(hw + 0.04, hh + 0.04, 0.03, '#5E666E', { outline: 0.006 }), dW / 2, hy, 0.08); hinge.add(flap);
    hinge.add(at(box(0.05, 0.22, 0.06, '#C9CED6'), dW - 0.12, 1.05, 0.08));
    // the corridor outside
    const cd = o.corr ?? 2.6;
    g.add(at(box(W + 6, 0.06, cd + 0.4, '#8F949A'), 0, -0.03, fz + 0.2 + cd / 2), at(box(W + 6, H + 0.4, 0.2, '#B8BEC4'), 0, (H + 0.4) / 2, fz + 0.2 + cd + 0.1), at(box(W + 6, 0.12, cd + 0.4, '#A9AFB5'), 0, H + 0.4, fz + 0.2 + cd / 2));
    g.add(at(box(W + 6, 1.0, 0.02, '#7E868E'), 0, 0.5, fz + 0.2 + cd - 0.01));
    if (o.light !== false) { const l = new THREE.PointLight('#FFF1D8', o.lightPower ?? 6, 9, 1.2); l.position.set(0, H - 0.4, 0); g.add(l); g.add(at(box(0.6, 0.05, 0.6, '#FFF8E8', { emissive: '#FFF2D0' }), 0, H - 0.03, 0)); }
    g.userData.update = t => { hinge.rotation.y = -1.6 * keyAt(o.open, t, 0, 0.3); const hp = keyAt(o.hatch, t, 1, 0.12); flap.position.y = hy - (hh + 0.06) * hp; flap.visible = hp < 0.98; };
    g.userData.update(0); return g;
  },

  // The prison gate by day (pivot on the ground at the middle of the wall's foot; the wall faces +Z): a pale stone wall o.w (16) x o.h (5.5) with a
  // coping, a big shut steel gate (o.gateW 4.2) under a stone lintel and the word PRISON, a guard's booth with a window at the right of the gate
  prisonGate(o) {
    const W = o.w ?? 16, H = o.h ?? 5.5, gw = o.gateW ?? 4.2, gh = 3.8, g = grp(), stone = o.stone || '#D6CDBA';
    const wall = canvasPlane(W, H, (c, Wp, Hp) => { c.fillStyle = stone; c.fillRect(0, 0, Wp, Hp); c.strokeStyle = 'rgba(120,108,88,0.35)'; c.lineWidth = Wp * 0.0015; const bh = Hp / 14, bw = Wp / 24;
      for (let j = 0; j < 14; j++) { c.beginPath(); c.moveTo(0, j * bh); c.lineTo(Wp, j * bh); c.stroke(); for (let i = 0; i < 25; i++) { const x = i * bw + (j % 2 ? bw / 2 : 0); c.beginPath(); c.moveTo(x, j * bh); c.lineTo(x, (j + 1) * bh); c.stroke(); } } }, { res: 1024 });
    wall.position.set(0, H / 2, 0.31); g.add(at(box(W, H, 0.6, stone, { outline: 0.01 }), 0, H / 2, 0), wall, at(box(W + 0.3, 0.3, 0.8, '#BFB49E', { outline: 0.008 }), 0, H + 0.15, 0));
    g.add(at(box(gw + 0.8, 0.7, 0.75, '#C6BCA6', { outline: 0.008 }), 0, gh + 0.35, 0.1));
    g.add(at(label(o.text || 'PRISON', gw * 0.8, 0.5, { bg: '#C6BCA6', fg: '#2A2D33' }), 0, gh + 0.35, 0.49));
    g.add(at(box(gw, gh, 0.12, o.gate || '#4A535C', { outline: 0.01 }), 0, gh / 2, 0.36));
    for (let i = 1; i < 8; i++) g.add(at(box(0.06, gh - 0.2, 0.06, '#353C44'), -gw / 2 + i * gw / 8, gh / 2, 0.45));
    g.add(at(box(gw - 0.1, 0.12, 0.06, '#353C44'), 0, gh * 0.33, 0.47), at(box(gw - 0.1, 0.12, 0.06, '#353C44'), 0, gh * 0.72, 0.47), at(box(0.04, gh - 0.1, 0.02, '#2A3036'), 0, gh / 2, 0.43));
    const bx = gw / 2 + 1.5; g.add(at(box(1.6, 2.6, 1.3, '#E8E2D4', { pivot: 'bottom', outline: 0.008 }), bx, 0, 0.95), at(box(1.75, 0.12, 1.45, '#8A6A4A'), bx, 2.66, 0.95));
    g.add(at(box(1.0, 0.7, 0.03, '#2E3A46'), bx, 1.55, 1.61), at(box(1.1, 0.06, 0.25, '#8A6A4A'), bx, 1.17, 1.68));
    // (final pass) the ground slabs drawn with a depth offset: at 5-15 mm over the grassland's 9 km field it flashed green for single frames
    const slab = c => { const m = mat(c, { unique: true }); m.polygonOffset = true; m.polygonOffsetFactor = -4; m.polygonOffsetUnits = -16; return m; };
    g.add(at(box(W + 40, 0.05, 14, '', { material: slab('#BDB6A8') }), 0, -0.02, 7), at(box(W + 40, 0.03, 3.2, '', { material: slab('#D9D2C2') }), 0, 0.0, 2.2));
    return g;
  },

  // An open register held up (pivot at the middle of its spine; open toward +Z): two blank ruled pages with a heading row, o.w (0.42) per page x o.h (0.55)
  // (pass 2) o.big: the heading in big bold ink on a pale band over a thick rule (readable at phone size); o.stand: on a wooden lectern (its foot
  // o.standH (1.2) below the spine, the book tilted back)
  emptyRegister(o) {
    const w = o.w ?? 0.42, h = o.h ?? 0.55, g = grp();
    g.add(at(box(2 * w + 0.05, h + 0.05, 0.03, o.cover || '#3E5A3A', { outline: 0.008 }), 0, 0, -0.016));
    if (o.stand) { const sh = o.standH ?? 1.2; g.add(at(box(2 * w + 0.1, 0.05, 0.12, '#6E4A30', { outline: 0.006 }), 0, -h / 2 - 0.03, 0.03), at(box(0.1, sh - h / 2, 0.1, '#6E4A30', { pivot: 'top', outline: 0.006 }), 0, -h / 2 - 0.03, -0.08), at(box(0.6, 0.06, 0.45, '#5A3A26', { outline: 0.006 }), 0, -sh, -0.08)); }
    const page = (txt) => canvasPlane(w, h, (c, W, Hh) => { c.fillStyle = '#F8F5EA'; c.fillRect(0, 0, W, Hh);
      if (o.big && txt) { c.fillStyle = '#E9DFC2'; c.fillRect(0, 0, W, Hh * 0.17); c.fillStyle = '#1E2A55'; c.fillRect(W * 0.04, Hh * 0.17, W * 0.92, Hh * 0.02); c.fillStyle = '#B0262A'; c.font = `900 ${Hh * 0.13}px Arial`; c.textAlign = 'center'; c.fillText(txt, W / 2, Hh * 0.135, W * 0.94); }
      else { c.fillStyle = '#2A3A6A'; c.fillRect(W * 0.06, Hh * 0.1, W * 0.88, Hh * 0.008); if (txt) { c.font = `bold ${Hh * 0.07}px Arial`; c.textAlign = 'center'; c.fillText(txt, W / 2, Hh * 0.08); } }
      c.strokeStyle = '#9DB2D0'; c.lineWidth = Hh * 0.004; for (let i = 0; i < 12; i++) { const y = Hh * ((o.big ? 0.26 : 0.18) + i * (o.big ? 0.06 : 0.065)); if (y > Hh * 0.97) break; c.beginPath(); c.moveTo(W * 0.06, y); c.lineTo(W * 0.94, y); c.stroke(); }
      c.strokeStyle = '#D98A8A'; c.beginPath(); c.moveTo(W * 0.22, Hh * 0.12); c.lineTo(W * 0.22, Hh * 0.95); c.stroke(); }, { res: 256 });
    const L = page(o.big ? ' ' : (o.left || 'ADRESSE')), R = page(o.big ? ' ' : (o.right || '')); L.position.set(-w / 2, 0, 0.03); L.rotation.y = 0.06; R.position.set(w / 2, 0, 0.03); R.rotation.y = -0.06; g.add(L, R);
    // (pass 2) o.big: one heading band across the whole spread, the word as big as the band allows
    if (o.big) { const bh = h * 0.2, band = canvasPlane(2 * w, bh, (c, W, Hh) => { c.fillStyle = '#EFE6CC'; c.fillRect(0, 0, W, Hh); c.fillStyle = '#1E2A55'; c.fillRect(0, Hh * 0.9, W, Hh * 0.1);
      c.fillStyle = '#B0262A'; c.font = `900 ${Hh * 0.78}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.left || 'ADRESSE', W / 2, Hh * 0.47, W * 0.92); }, { res: 512 });
      band.position.set(0, h / 2 - bh / 2, 0.045); g.add(band); }
    return g;
  },

  // (pass 2) A smear frame for a fast swing: a translucent ribbon along o.pts (local points, in order) with speed lines on it, o.w (0.25) wide at
  // the end (tapering to the start), in the plane facing o.normal ([0, 0, 1]); shown during [o.at, o.at + o.dur (0.07)]; o.color
  smearTrail(o) {
    const g = grp(), pts = (o.pts || [[0, 1, 0], [0, 0, 0]]).map(p => new THREE.Vector3(...p)), n = new THREE.Vector3(...(o.normal || [0, 0, 1])).normalize(), W = o.w ?? 0.25;
    const pos = [], idx = [];
    pts.forEach((p, i) => { const f = i / (pts.length - 1), d = (pts[Math.min(i + 1, pts.length - 1)].clone().sub(pts[Math.max(i - 1, 0)])).normalize(), side = d.clone().cross(n).normalize().multiplyScalar(W * (0.25 + 0.75 * f) / 2);
      pos.push(...p.clone().add(side).toArray(), ...p.clone().sub(side).toArray()); if (i) { const a = 2 * (i - 1); idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); } });
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); geo.setIndex(idx);
    const rib = new THREE.Mesh(geo, basic(o.color || '#8A5A30', o.opacity ?? 0.55)); rib.renderOrder = 4; g.add(rib);
    const lm = basic(o.lines || '#FFF6DC', 0.85);
    [-0.3, 0, 0.3].forEach(k => { for (let i = 1; i < pts.length; i++) { const f = i / (pts.length - 1), d = pts[i].clone().sub(pts[i - 1]), side = d.clone().normalize().cross(n).normalize().multiplyScalar(W * k * (0.25 + 0.75 * f));
      const a = pts[i - 1].clone().add(side).addScaledVector(n, 0.01), b = pts[i].clone().add(side).addScaledVector(n, 0.01); g.add(segment(a.toArray(), b.toArray(), 0.006, lm, 4)); } });
    noShadow(g);
    g.userData.update = t => { g.visible = t >= (o.at ?? 0) && t < (o.at ?? 0) + (o.dur ?? 0.07); };
    g.userData.update(-1); return g;
  },

  // (pass 2) A burst of speed lines out of a hole (pivot at its middle; lines in the XY plane, pushed toward +Z): o.n (14) wedges from o.r0 (0.4)
  // shooting out to o.r1 (1.6) over o.dur (0.35) from o.at, then fading; o.color, o.edge
  burstLines(o) {
    const g = grp(), n = o.n ?? 14, R0 = o.r0 ?? 0.4, R1 = o.r1 ?? 1.6, L = [];
    for (let i = 0; i < n; i++) { const a = (i + 0.5 * hsh(i)) / n * TAU, sh = new THREE.Shape(); sh.moveTo(0, -0.025); sh.lineTo(1, -0.006); sh.lineTo(1, 0.006); sh.lineTo(0, 0.025);
      const m = new THREE.Mesh(new THREE.ShapeGeometry(sh), basic(i % 2 ? (o.color || '#FFFFFF') : (o.edge || '#3B88C9'), 0.9)); m.rotation.z = a; m.renderOrder = 6; const hold = grp(m); g.add(hold); L.push({ hold, m, a, k: 0.7 + 0.5 * hsh(i + 5) }); }
    noShadow(g);
    g.userData.update = t => { const u = (t - (o.at ?? 0)) / (o.dur ?? 0.35); g.visible = u >= 0 && u < 1.4;
      L.forEach(l => { const r0 = R0 + (R1 - R0) * 0.6 * easeOut(u) * l.k, len = (R1 - R0) * 0.5 * l.k * (1 - 0.5 * clamp01(u)); l.m.position.set(Math.cos(l.a) * r0, Math.sin(l.a) * r0, 0.05 * u); l.m.scale.set(len, 1.6, 1); l.m.material.opacity = 0.9 * (1 - smooth((u - 0.7) / 0.7)); }); };
    g.userData.update(-1); return g;
  },

  // A black beret for the mime (pivot at its band; sits on a head at offset [0, 0.5, 0]): a flat disc tilted to one side with a stalk
  mimeBeret(o) {
    const g = grp(at(cyl(0.2, 0.17, 0.07, o.color || '#16161A', 12, { outline: 0.006 }), 0.03, 0.03, 0, 0, 0, -0.18), at(cyl(0.012, 0.012, 0.05, o.color || '#16161A', 5), 0.04, 0.09, 0));
    return g;
  },

  // A striped jersey for the mime, worn over a dark top (attach to the torso joint, offset [0, 0, 0]): o.n (6) white bands round the chest, o.w (0.4)
  // wide, o.d (0.25) deep, from o.y0 (0.08) to o.y1 (0.55) up the torso; plus a boat neck
  mimeStripes(o) {
    const g = grp(), n = o.n ?? 6, w = o.w ?? 0.5, d = o.d ?? 0.32, y0 = o.y0 ?? 0.08, y1 = o.y1 ?? 0.55, c = o.color || '#F4F2EC';
    for (let i = 0; i < n; i++) g.add(at(box(w, (y1 - y0) / n * 0.45, d, c), 0, y0 + (i + 0.5) * (y1 - y0) / n, 0));
    return g;
  },

  // Dust and plaster falling from a ceiling (pivot on the floor at the middle of the area): o.n (60) pale flakes over o.w x o.d (4 x 3) from o.top (4)
  // to the floor, looping (o.speed 1.2 m/s), tumbling; plus soft haze puffs (o.haze 8) drifting down; from o.at on
  plasterFall(o) {
    const g = grp(), n = o.n ?? 60, W = o.w ?? 4, D = o.d ?? 3, top = o.top ?? 4, sp = o.speed ?? 1.2, fl = [], hz = [];
    const fm = mat(o.color || '#E6DFD0', { doubleSide: true });
    for (let i = 0; i < n; i++) { const s = (o.size ?? 0.05) * (0.6 + 0.9 * hsh(i + 2)); const m = new THREE.Mesh(new THREE.PlaneGeometry(s, s * 0.7), fm); m.castShadow = false; g.add(m); fl.push(m); }
    for (let i = 0; i < (o.haze ?? 8); i++) { const s = softSprite(o.hazeColor || '#E9E3D6', 0.35); g.add(s); hz.push(s); }
    g.userData.update = t => { const u0 = t - (o.at ?? 0);
      fl.forEach((m, i) => { m.visible = u0 >= 0; if (!m.visible) return; const ph = hsh(i + 7), y = top - ((u0 * sp * (0.8 + 0.4 * hsh(i + 3)) + ph * top) % top);
        m.position.set((hsh(i + 11) - 0.5) * W + 0.1 * Math.sin(t * 2 + i), y, (hsh(i + 13) - 0.5) * D); m.rotation.set(t * 3 + i, t * 2 + i * 0.5, 0); });
      hz.forEach((s, i) => { s.visible = u0 >= 0; if (!s.visible) return; const k = ((u0 * 0.25 + i / hz.length) % 1); s.position.set((hsh(i + 21) - 0.5) * W, top * (1 - k), (hsh(i + 23) - 0.5) * D); const sc = 0.8 + 0.8 * k; s.scale.set(sc, sc, 1); s.material.opacity = (o.hazeOp ?? 0.3) * Math.sin(k * PI); }); };
    g.userData.update(0); return g;
  },

  // Soot smoke rising from something burnt (pivot at the source): o.n (8) dark soft puffs rising o.rise (2.5) m and spreading, looping, from o.at
  sootSmoke(o) {
    const g = grp(), n = o.n ?? 8, sp = [];
    for (let i = 0; i < n; i++) { const s = softSprite(o.color || '#3A3836', o.opacity ?? 0.8); g.add(s); sp.push(s); }
    g.userData.update = t => sp.forEach((s, i) => { const u0 = t - (o.at ?? 0); s.visible = u0 >= 0; if (!s.visible) return; const k = ((u0 * (o.speed ?? 0.6) + i / n) % 1);
      s.position.set(0.3 * Math.sin(i * 2.1 + k * 3) * k + (o.drift ?? 0.4) * k, k * (o.rise ?? 2.5), 0.2 * Math.cos(i * 1.7) * k); const sc = (o.s0 ?? 0.4) + (o.s1 ?? 1.4) * k; s.scale.set(sc, sc, 1); s.material.opacity = (o.opacity ?? 0.8) * (k < 0.15 ? k / 0.15 : 1 - k); });
    g.userData.update(0); return g;
  },

  // A front desk by night (pivot on the floor, the counter's front middle, facing +Z): a counter o.w (2.6) x 1.1 high with a sign over the back wall
  // area (o.sign 'ACCUEIL', put at o.signY 2.6 above the counter, 0.9 behind it), a desk lamp, a bell, papers
  frontCounter(o) {
    const W = o.w ?? 2.6, g = grp(), c = o.color || '#5E6E7E';
    g.add(at(box(W, 1.1, 0.6, c, { pivot: 'bottom', outline: 0.008 }), 0, 0, -0.3), at(box(W + 0.1, 0.06, 0.75, '#C9B48A', { outline: 0.006 }), 0, 1.13, -0.32), at(box(W, 0.08, 0.01, '#3E4A56'), 0, 0.85, 0.005));
    g.add(at(box(W - 0.1, 0.05, 0.6, '#C9B48A'), 0, 0.76, -0.95), at(box(W - 0.1, 0.76, 0.05, c), 0, 0.38, -1.22));
    if (o.sign !== false) g.add(at(label(o.sign || 'ACCUEIL', 1.5, 0.42, { bg: '#2E4058', fg: '#F2EEE2' }), 0, o.signY ?? 2.6, -1.4));
    g.add(at(cyl(0.06, 0.07, 0.04, '#C9A84A', 10, { pivot: 'bottom' }), W / 2 - 0.3, 1.16, -0.25), at(sphere(0.05, '#D8B85A', 1), W / 2 - 0.3, 1.22, -0.25));
    g.add(at(box(0.32, 0.01, 0.24, '#F4F1E8'), -W / 2 + 0.45, 1.165, -0.35, 0, 0.2, 0), at(box(0.3, 0.01, 0.22, '#ECE8DA'), -W / 2 + 0.5, 1.175, -0.33, 0, -0.15, 0));
    return g;
  }
};
