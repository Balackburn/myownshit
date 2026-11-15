// « Le robinet » (story 71): this man forgot to turn off his bath tap: the water ran down the stairs and into the street, the town became a seaside
// resort, the navy's submarine parked outside the bakery, the president came by pedalo; three years later he pulled the plug and the sea drained
// into his bathtub in six seconds, the submarine too. Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every
// animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl } from './style.js';
import { grp, at, canvasPlane, buildProp } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { x = clamp01(x); return x * x * (3 - 2 * x); };
const outBack = x => { x = clamp01(x); const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const hash = n => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const L = c => new THREE.MeshLambertMaterial({ color: c });
const ball = (r, c, seg = 10) => new THREE.Mesh(new THREE.SphereGeometry(r, seg, Math.max(6, seg - 2)), typeof c === 'string' ? L(c) : c);
const WATER = '#5DB8E6';
// [[t, v], ...] eased between keys, held before the first key and after the last
const keyAt = (keys, t, def = 0) => {
  if (!keys || !keys.length) return def;
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) if (t < keys[i][0]) { const [t0, v0] = keys[i - 1], [t1, v1] = keys[i]; return v0 + (v1 - v0) * smooth((t - t0) / Math.max(1e-6, t1 - t0)); }
  return keys[keys.length - 1][1];
};
// streaks running along v (white on transparent), to scroll down a sheet of water
const streaks = (seed = 1, alpha = 0.6) => {
  const c = document.createElement('canvas'); c.width = 64; c.height = 256; const x = c.getContext('2d');
  for (let i = 0; i < 26; i++) { const px = hash(seed * 31 + i) * 64, len = 30 + hash(seed * 17 + i) * 90, py = hash(seed * 7 + i) * 256, w = 1 + hash(i + seed) * 2.5;
    x.fillStyle = `rgba(255,255,255,${((0.35 + 0.65 * hash(i * 3 + seed)) * alpha).toFixed(3)})`; x.fillRect(px, py, w, len); if (py + len > 256) x.fillRect(px, py - 256, w, len); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t;
};
// a spiral of foam (log spiral arms, tight at the centre) on a radial blue (bg) or on nothing
const spiralTex = (arms = 6, bg = true) => {
  const S = 512, R = S / 2, c = document.createElement('canvas'); c.width = c.height = S; const x = c.getContext('2d');
  if (bg) { const g = x.createRadialGradient(R, R, 0, R, R, R); g.addColorStop(0, '#0E3F66'); g.addColorStop(0.3, '#2475AE'); g.addColorStop(1, '#5DB8E6'); x.fillStyle = g; x.fillRect(0, 0, S, S); }
  x.lineCap = 'round';
  for (let k = 0; k < arms; k++) for (let j = 0; j < 3; j++) {
    x.beginPath(); const a0 = k * TAU / arms + j * 0.14;
    for (let i = 0; i <= 140; i++) { const u = i / 140, r = R * (0.03 + 0.95 * u), a = a0 + 3.4 * Math.log(1 + 7 * u), px = R + r * Math.cos(a), py = R + r * Math.sin(a); if (i) x.lineTo(px, py); else x.moveTo(px, py); }
    x.strokeStyle = j === 0 ? 'rgba(255,255,255,0.9)' : 'rgba(205,238,255,0.5)'; x.lineWidth = j === 0 ? 8 : 3.5; x.stroke(); }
  return new THREE.CanvasTexture(c);
};
const waterMat = (opacity = 0.78, color = WATER) => new THREE.MeshLambertMaterial({ color, transparent: true, opacity, depthWrite: false, side: THREE.DoubleSide });
const streakMat = (tex, opacity = 0.9) => new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity, depthWrite: false, side: THREE.DoubleSide });
const rrect = (w, d, r) => { const s = new THREE.Shape(), x0 = -w / 2, z0 = -d / 2; s.moveTo(x0 + r, z0); s.lineTo(x0 + w - r, z0); s.quadraticCurveTo(x0 + w, z0, x0 + w, z0 + r);
  s.lineTo(x0 + w, z0 + d - r); s.quadraticCurveTo(x0 + w, z0 + d, x0 + w - r, z0 + d); s.lineTo(x0 + r, z0 + d); s.quadraticCurveTo(x0, z0 + d, x0, z0 + d - r);
  s.lineTo(x0, z0 + r); s.quadraticCurveTo(x0, z0, x0 + r, z0); return s; };

export const ROBINET_PROPS = {
  // A claw-foot bathtub (front +Z, its length along x, the taps at +x) that fills, overflows, drains and drips. o.fill (0..1 of the inside height) or
  // o.fillKeys [[t, fill], ...] (eased; above 1 the water stands at the rim and spills over the front in a sheet, a puddle spreading on the floor);
  // o.tap [t0, t1]: the tap runs (a stream from the spout, a ring of splash where it lands, drops jumping); o.swirl [t0, t1]: the plug is out: a
  // spiral turns on the water over the plughole, faster and faster; o.plugOut: the plug and its chain leave the tub then (they are in his hand);
  // o.drips [t, ...]: a drop swells at the spout and falls; o.weed: seaweed hangs from the spout; o.barnacles: shells on the front; o.sub: the tail
  // of a submarine stuck in the plughole (its periscope turning by o.subYaw [[t, deg], ...]); userData.drain, userData.mouth (in the tub's frame)
  bathTub(o) {
    const W = o.w ?? 1.9, D = o.d ?? 0.95, H = o.h ?? 0.6, y0 = o.feet ?? 0.16, t = 0.06, rr = D * 0.45, g = grp(), white = L('#FAFAF7');
    const ring = (w, d, r, th, hgt, m, y) => { const s = rrect(w, d, r); s.holes.push(rrect(w - 2 * th, d - 2 * th, Math.max(0.01, r - th))); const ms = new THREE.Mesh(new THREE.ExtrudeGeometry(s, { depth: hgt, bevelEnabled: false, curveSegments: 10 }), m);
      ms.rotation.x = -PI / 2; ms.position.y = y; ms.castShadow = ms.receiveShadow = true; return ms; };
    g.add(ring(W, D, rr, t, H, white, y0), ring(W + 0.07, D + 0.07, rr + 0.035, t + 0.07, 0.06, L('#FFFFFF'), y0 + H - 0.03));
    const floor = new THREE.Mesh(new THREE.ShapeGeometry(rrect(W - 2 * t, D - 2 * t, rr - t), 10), white); floor.rotation.x = -PI / 2; floor.position.y = y0 + 0.02; g.add(floor);
    const gold = L('#D8A93A');
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) { const f = grp(at(box(0.09, y0 + 0.04, 0.09, '#D8A93A', { pivot: 'bottom', taper: 1.5 }), 0, 0, 0));
      const paw = ball(0.07, gold, 8); paw.scale.set(1.2, 0.6, 1.2); paw.position.y = 0.03; f.add(paw); g.add(at(f, sx * (W / 2 - rr * 0.55), 0, sz * (D / 2 - 0.16))); }
    const chrome = '#C9D1D8', tx = W / 2 - 0.12, mouth = [tx - 0.23, y0 + H + 0.3, 0], hole = [tx - 0.3, y0 + 0.025, 0];
    g.add(at(cyl(0.03, 0.03, 0.34, chrome, 8, { pivot: 'bottom' }), tx, y0 + H, 0), at(cyl(0.025, 0.025, 0.24, chrome, 8), tx - 0.11, y0 + H + 0.32, 0, 0, 0, PI / 2),
      at(cyl(0.028, 0.022, 0.05, chrome, 8), mouth[0], mouth[1] + 0.005, 0));
    for (const sd of [-1, 1]) { g.add(at(cyl(0.022, 0.022, 0.12, chrome, 6, { pivot: 'bottom' }), tx, y0 + H, sd * 0.16), at(box(0.12, 0.025, 0.025, chrome), tx, y0 + H + 0.13, sd * 0.16));
      g.add(at(ball(0.025, sd < 0 ? '#3A7BD5' : '#D83A2E', 6), tx, y0 + H + 0.15, sd * 0.16)); }
    // the water, its spill over the front rim and the puddle
    const water = new THREE.Mesh(new THREE.ShapeGeometry(rrect(W - 2 * t - 0.01, D - 2 * t - 0.01, rr - t), 10), new THREE.MeshLambertMaterial({ color: '#7CCBEB', transparent: true, opacity: 0.88, depthWrite: false }));
    water.rotation.x = -PI / 2; water.renderOrder = 3; g.add(water);
    const sTex = streaks(5); sTex.repeat.set(3, 1.1);
    const spill = grp(at(new THREE.Mesh(new THREE.PlaneGeometry(W * 0.84, y0 + H), waterMat(0.72)), 0, (y0 + H) / 2, D / 2 + 0.06), at(new THREE.Mesh(new THREE.PlaneGeometry(W * 0.84, y0 + H), streakMat(sTex)), 0, (y0 + H) / 2, D / 2 + 0.07),
      at(new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, W * 0.84, 10, 1), waterMat(0.85)), 0, y0 + H + 0.03, D / 2 + 0.02, 0, 0, PI / 2));
    spill.children.forEach(m => { m.renderOrder = 4; }); g.add(spill);
    const puddle = new THREE.Mesh(new THREE.CircleGeometry(1, 36), waterMat(0.62)); puddle.rotation.x = -PI / 2; puddle.position.set(0, 0.006, D / 2 + 0.15); g.add(puddle);
    const fk = o.fillKeys || [[0, o.fill ?? 0.8]];
    let tOver = null; for (let s = fk[0][0]; s <= fk[fk.length - 1][0] + 0.01; s += 0.02) if (keyAt(fk, s) >= 1) { tOver = s; break; }
    // the stream from the tap, the ring where it lands, the drops it throws
    const stTex = streaks(9, 0.85); stTex.repeat.set(1, 2.5);
    const stream = grp(at(new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.034, 1, 10, 1, true), waterMat(0.92, '#BFE8FA')), 0, -0.5, 0), at(new THREE.Mesh(new THREE.CylinderGeometry(0.049, 0.038, 1, 10, 1, true), streakMat(stTex)), 0, -0.5, 0));   // (stills 1 of 71) thicker and paler: at 26 mm it did not show
    stream.position.set(...mouth); g.add(stream);
    const splash = new THREE.Mesh(new THREE.TorusGeometry(0.07, 0.014, 5, 18), waterMat(0.85, '#E8F7FF')); splash.rotation.x = PI / 2; g.add(splash);
    const jumps = []; for (let i = 0; i < 7; i++) { const d = ball(0.013, '#E8F7FF', 6); g.add(d); jumps.push(d); }
    // the swirl over the plughole
    const sw = new THREE.Mesh(new THREE.CircleGeometry(Math.min(0.42, D * 0.42), 40), new THREE.MeshBasicMaterial({ map: spiralTex(5, false), transparent: true, opacity: 0, depthWrite: false }));
    sw.rotation.x = -PI / 2; sw.renderOrder = 5; g.add(sw);
    // the plug and its ball chain up to the rim
    const plug = grp(at(cyl(0.045, 0.038, 0.035, '#1C1C20', 12), 0, 0.017, 0), at(new THREE.Mesh(new THREE.TorusGeometry(0.015, 0.004, 4, 10), L(chrome)), 0, 0.045, 0));
    plug.position.set(hole[0], y0 + 0.02, 0); g.add(plug, at(new THREE.Mesh(new THREE.RingGeometry(0.03, 0.05, 16), L('#9AA3AB')), hole[0], y0 + 0.024, 0, -PI / 2, 0, 0));
    const chain = grp(); const c0 = new THREE.Vector3(hole[0], y0 + 0.07, 0), c1 = new THREE.Vector3(tx - 0.02, y0 + H + 0.02, D / 2 - t - 0.04);
    for (let i = 0; i <= 14; i++) { const u = i / 14, p = c0.clone().lerp(c1, u); p.y -= 0.08 * Math.sin(PI * u); const b = ball(0.007, chrome, 5); b.position.copy(p); chain.add(b); } g.add(chain);
    // a drop at the spout
    const drop = ball(0.02, new THREE.MeshLambertMaterial({ color: '#BDE6F7', transparent: true, opacity: 0.9 }), 8); g.add(drop);
    const dring = new THREE.Mesh(new THREE.TorusGeometry(0.05, 0.006, 4, 16), waterMat(0.8, '#E8F7FF')); dring.rotation.x = PI / 2; g.add(dring);
    // seaweed, barnacles
    const weed = []; if (o.weed) for (let i = 0; i < 4; i++) { const s = grp(); let par = s; for (let j = 0; j < 5; j++) { const seg = grp(at(box(0.02, 0.07, 0.008, i % 2 ? '#3E7A3A' : '#5C9A3E'), 0, -0.035, 0)); seg.position.y = j ? -0.07 : 0; par.add(seg); par = seg; }
      s.position.set(tx - 0.2 + i * 0.045, y0 + H + 0.3, (i - 1.5) * 0.012); g.add(s); weed.push(s); }
    if (o.barnacles) for (let i = 0; i < 16; i++) { const b = new THREE.Mesh(new THREE.ConeGeometry(0.022, 0.03, 6), L(i % 3 ? '#E8E2D2' : '#B9B2A0')); b.position.set((hash(i * 2 + 1) - 0.5) * W * 0.8, y0 + 0.08 + hash(i * 2 + 2) * H * 0.75, D / 2 + 0.035); b.rotation.x = PI / 2; g.add(b); }
    // the tail of a submarine stuck in the plughole: the stern, its fins and propeller, the periscope beside it
    let subTail = null, subPeri = null; if (o.sub) { subTail = grp(); const hull = '#5E6B7A';
      const cone = new THREE.Mesh(new THREE.ConeGeometry(0.11, 0.42, 14), L(hull)); cone.position.y = 0.21; subTail.add(cone, at(box(0.36, 0.016, 0.06, hull), 0, 0.12, 0), at(box(0.016, 0.16, 0.06, hull), 0, 0.14, 0));
      const pr = grp(at(box(0.03, 0.13, 0.012, '#C9A43E'), 0, 0.06, 0), at(box(0.03, 0.13, 0.012, '#C9A43E'), 0, -0.06, 0)); pr.position.y = 0.44; pr.rotation.x = PI / 2; subTail.add(pr); subTail.userData.pr = pr;
      subTail.position.set(hole[0], y0 + 0.03, 0); subTail.rotation.z = 0.25; g.add(subTail);
      subPeri = grp(at(cyl(0.012, 0.012, 0.3, '#3A424C', 6, { pivot: 'bottom' }), 0, 0, 0)); const hd = grp(at(box(0.04, 0.05, 0.08, '#3A424C'), 0, 0, 0.02), at(new THREE.Mesh(new THREE.CircleGeometry(0.017, 12), L('#14161B')), 0, 0, 0.061), at(ball(0.006, '#FFFFFF', 5), 0.006, 0.007, 0.064));
      hd.position.y = 0.3; subPeri.add(hd); subPeri.userData.hd = hd; subPeri.position.set(hole[0] - 0.12, y0 + 0.03, 0.06); g.add(subPeri); }
    g.userData.update = tt => {
      const f = keyAt(fk, tt), over = f > 1, wy = y0 + 0.03 + (H - 0.04) * Math.min(1, Math.max(0, f));
      water.visible = f > 0.02; water.position.y = wy + 0.01 * Math.sin(tt * 4.2); water.scale.setScalar(1);
      spill.visible = over; sTex.offset.y = -tt * 2.2;
      const pr = tOver == null ? 0 : Math.max(0, tt - tOver); puddle.visible = pr > 0; puddle.scale.setScalar(Math.min(o.puddle ?? 2.6, 0.25 + 1.4 * pr));
      const tapOn = o.tap && tt >= o.tap[0] && tt < o.tap[1];
      stream.visible = !!tapOn; stTex.offset.y = tt * 3.0; const land = over ? y0 + H : wy; stream.scale.set(1, Math.max(0.02, mouth[1] - land), 1);
      splash.visible = !!tapOn; splash.position.set(mouth[0], land + 0.006, 0); splash.scale.setScalar(1 + 0.35 * Math.sin(tt * 15));
      jumps.forEach((d, i) => { d.visible = !!tapOn; if (!tapOn) return; const ph = (tt * 2.4 + i / 7) % 1, a = i * 2.4; d.position.set(mouth[0] + Math.cos(a) * 0.2 * ph, land + 0.16 * Math.sin(PI * ph), Math.sin(a) * 0.2 * ph); });
      const sv = o.swirl ? clamp01((tt - o.swirl[0]) / 0.3) * (tt < o.swirl[1] ? 1 : clamp01(1 - (tt - o.swirl[1]) / 0.2)) : 0;
      sw.visible = sv > 0 && f > 0.03; sw.material.opacity = 0.9 * sv; sw.position.set(hole[0] - 0.08, wy + 0.012, 0); if (o.swirl) { const u = Math.max(0, tt - o.swirl[0]); sw.rotation.z = (o.dir ?? 1) * (4 * u + 9 * u * u); }
      const out = o.plugOut != null && tt >= o.plugOut; plug.visible = chain.visible = !out && !o.sub;
      let dv = false; dring.visible = false; for (const td of o.drips || []) { const a = tt - (td - 0.35); if (a < 0) continue; if (tt < td) { dv = true; drop.position.set(mouth[0], mouth[1] - 0.02 - 0.015 * smooth(a / 0.35), 0); drop.scale.set(0.5 + 0.5 * smooth(a / 0.35), 0.5 + 0.8 * smooth(a / 0.35), 0.5 + 0.5 * smooth(a / 0.35)); }
        else { const fall = tt - td, y = mouth[1] - 0.04 - 4.9 * fall * fall, lv = f > 0.03 ? wy : y0 + 0.03; if (y > lv) { dv = true; drop.position.set(mouth[0], y, 0); drop.scale.set(0.8, 1.3, 0.8); }
          else { const tl = Math.sqrt(Math.max(0, (mouth[1] - 0.04 - lv) / 4.9)), rs = fall - tl; if (rs < 0.45) { dring.visible = true; dring.position.set(mouth[0], lv + 0.005, 0); dring.scale.setScalar(0.4 + 2.2 * rs); dring.material.opacity = 0.8 * (1 - rs / 0.45); } } } }
      drop.visible = dv;
      weed.forEach((s, i) => { let seg = s.children[0], j = 0; while (seg) { seg.rotation.z = 0.18 * Math.sin(tt * 1.6 + i * 1.3 + j * 0.7); seg.rotation.x = 0.08 * Math.sin(tt * 1.2 + i); j++; seg = seg.children.find(c => c.type === 'Group'); } });
      if (subTail) { subTail.userData.pr.rotation.y = tt * 9; subTail.rotation.x = 0.04 * Math.sin(tt * 3.1); if (subPeri) subPeri.userData.hd.rotation.y = keyAt(o.subYaw, tt, 0) * PI / 180; }
    };
    g.userData.update(0); g.userData.drain = hole; g.userData.mouth = mouth; g.userData.lie = [0, y0 + 0.2, 0]; return g;
  },
  // the bath plug in the hand (attach it to a hand): a black rubber plug and its ball chain hanging below, swinging; water dripping off it
  bathPlug(o) {
    const g = grp(at(cyl(0.045, 0.038, 0.035, '#1C1C20', 12), 0, -0.04, 0), at(new THREE.Mesh(new THREE.TorusGeometry(0.015, 0.004, 4, 10), L('#C9D1D8')), 0, -0.012, 0));
    const chain = grp(); for (let i = 0; i < 12; i++) { const b = ball(0.007, '#C9D1D8', 5); b.position.set(0, -0.07 - i * 0.022, 0); chain.add(b); } g.add(chain);
    const drips = []; for (let i = 0; i < 3; i++) { const d = ball(0.009, '#BDE6F7', 6); g.add(d); drips.push(d); }
    g.userData.update = t => { chain.rotation.z = 0.35 * Math.sin(t * 5.2) * Math.exp(-0.6 * Math.max(0, t - (o.at ?? 0))); chain.rotation.x = 0.15 * Math.sin(t * 3.7);
      drips.forEach((d, i) => { const ph = (t * 1.3 + i / 3) % 1; d.position.set(0, -0.06 - 0.9 * ph * ph, 0); d.visible = ph < 0.8; }); };
    g.userData.update(0); return g;
  },
  // A sheet of water running down a profile (the water runs toward +Z, the sheet o.w wide across x): o.profile [[z, y], ...] from the source down (a
  // staircase: its step noses), o.at the moment it starts, o.speed m/s along the profile, o.thick its depth over the profile; a rolling lip of white
  // foam at its front, streaks running down; o.pool: metres of flat spread past the foot of the profile; userData.front(t) = [z, y] of the front
  cascade(o) {
    const P = o.profile || [[0, 1], [2, 0]], W = o.w ?? 1.2, th = o.thick ?? 0.07, sp = o.speed ?? 2.5, t0 = o.at ?? 0, g = grp();
    const S = [{ z: P[0][0], y: P[0][1], s: 0 }]; let acc = 0;
    for (let i = 1; i < P.length; i++) { const [za, ya] = P[i - 1], [zb, yb] = P[i], l = Math.hypot(zb - za, yb - ya), n = Math.max(1, Math.ceil(l / 0.05));
      for (let j = 1; j <= n; j++) { const u = j / n; acc += l / n; S.push({ z: za + (zb - za) * u, y: ya + (yb - ya) * u, s: acc }); } }
    const N = S.length, pos = new Float32Array(N * 6), uv = new Float32Array(N * 4), idx = [];
    for (let i = 0; i < N; i++) { const a = S[Math.max(0, i - 1)], b = S[Math.min(N - 1, i + 1)], dz = b.z - a.z, dy = b.y - a.y, l = Math.hypot(dz, dy) || 1, nz = -dy / l, ny = dz / l;
      for (const k of [0, 1]) { const v = i * 2 + k; pos[v * 3] = (k - 0.5) * W; pos[v * 3 + 1] = S[i].y + ny * th; pos[v * 3 + 2] = S[i].z + nz * th; uv[v * 2] = k * W; uv[v * 2 + 1] = S[i].s; }
      if (i) idx.push((i - 1) * 2, (i - 1) * 2 + 1, i * 2 + 1, (i - 1) * 2, i * 2 + 1, i * 2); }
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(pos, 3)); geo.setAttribute('uv', new THREE.BufferAttribute(uv, 2)); geo.setIndex(idx); geo.computeVertexNormals();
    const tex = streaks(o.seed ?? 3); tex.repeat.set(1.4, 0.7);
    const body = new THREE.Mesh(geo, waterMat(o.opacity ?? 0.8, o.color || WATER)), skin = new THREE.Mesh(geo, streakMat(tex)); body.renderOrder = 3; skin.renderOrder = 4; g.add(body, skin);
    const lip = grp(); for (let i = 0; i < 10; i++) { const b = ball(0.07 + 0.035 * hash(i), '#F4FBFF', 8); b.position.set(-W / 2 + W * (i + 0.5) / 10, 0.03 * hash(i + 4), 0); lip.add(b); } g.add(lip);
    const pool = new THREE.Mesh(new THREE.PlaneGeometry(W * 1.15, 1).rotateX(-PI / 2).translate(0, 0, 0.5), waterMat(0.78, o.color || WATER)); pool.renderOrder = 3; g.add(pool);
    const reach = t => Math.max(0, (t - t0) * sp);
    g.userData.front = t => { const s = reach(t); let n = 0; while (n < N - 1 && S[n + 1].s <= s) n++; const over = Math.min(o.pool ?? 0, Math.max(0, s - S[N - 1].s)); return [S[n].z + over, S[n].y]; };
    g.userData.update = t => {
      const s = reach(t), vis = s > 0.01; let n = 0; while (n < N - 1 && S[n + 1].s <= s) n++;
      body.visible = skin.visible = lip.visible = vis && n > 0; geo.setDrawRange(0, n * 6); tex.offset.y = -t * (o.flow ?? 2.4);
      const over = Math.min(o.pool ?? 0, Math.max(0, s - S[N - 1].s)); pool.visible = over > 0.01; pool.position.set(0, S[N - 1].y + 0.012, S[N - 1].z); pool.scale.set(1, 1, Math.max(0.01, over));
      const f = S[n]; lip.position.set(0, f.y + th * 0.8, f.z + over); lip.scale.setScalar(0.85 + 0.2 * Math.sin(t * 13));
    };
    g.userData.update(0); return g;
  },
  // A whirlpool in a sheet of water (pivot at its centre on the surface, radius o.r): spiral bands turning faster and faster from o.at (o.spin rad/s
  // reached after o.dur), a funnel hollowing at the centre (radius o.funnel, depth o.depth) and o.items riding the spiral in and down: [{kind:
  // 'duck' | 'ring' | 'chair' | 'boat' | 'pedalo' | 'parasol' | 'sub' | 'car' | 'fish', r, a (rad), s, from, dur, turns}]; o.dir: the turning sense
  whirlpool(o) {
    const R = o.r ?? 12, rf = o.funnel ?? R * 0.16, dep = o.depth ?? R * 0.4, t0 = o.at ?? 0, Du = o.dur ?? 2, wm = o.spin ?? 3, dir = o.dir ?? 1, g = grp(), spin = grp();
    const disc = new THREE.Mesh(new THREE.RingGeometry(rf * 0.98, R, 80, 1), new THREE.MeshLambertMaterial({ map: spiralTex(o.arms ?? 6, true) })); disc.rotation.x = -PI / 2; disc.receiveShadow = true; spin.add(disc); g.add(spin);
    const ft = (() => { const c = document.createElement('canvas'); c.width = 256; c.height = 256; const x = c.getContext('2d'); const gr = x.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, '#2C7DB6'); gr.addColorStop(1, '#06223A'); x.fillStyle = gr; x.fillRect(0, 0, 256, 256);
      x.strokeStyle = 'rgba(255,255,255,0.55)'; x.lineWidth = 6; for (let i = -4; i < 12; i++) { x.beginPath(); x.moveTo(i * 32, 0); x.lineTo(i * 32 + 128, 256); x.stroke(); } const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(3, 1); return t; })();
    const funnel = new THREE.Mesh(new THREE.ConeGeometry(rf, dep, 48, 1, true), new THREE.MeshLambertMaterial({ map: ft, side: THREE.DoubleSide })); funnel.rotation.x = PI; g.add(funnel);
    const mk = it => { const s = it.s ?? 1, k = it.kind; let m;
      if (k === 'duck') { m = grp(); const b = ball(0.5, '#F7D23A', 12); b.scale.set(1.1, 0.75, 1.3); b.position.y = 0.2; const h = ball(0.3, '#F7D23A', 10); h.position.set(0, 0.62, 0.42); const bk = new THREE.Mesh(new THREE.ConeGeometry(0.1, 0.24, 8), L('#F08A24')); bk.rotation.x = PI / 2; bk.position.set(0, 0.6, 0.78);
        m.add(b, h, bk); for (const sd of [-1, 1]) m.add(at(ball(0.05, '#14161B', 6), sd * 0.14, 0.7, 0.66)); }
      else if (k === 'ring') { m = grp(); for (let i = 0; i < 4; i++) m.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.42, 0.14, 8, 10, PI / 2), L(i % 2 ? '#FFFFFF' : '#E8452E')), 0, 0.08, 0, PI / 2, 0, i * PI / 2)); }
      else if (k === 'sub') m = ROBINET_PROPS.submarine({ len: 4.5 });
      else if (k === 'fish') m = ROBINET_PROPS.fishFlop({ s: 0.6, rate: 3 });
      else m = buildProp({ chair: 'deckChair', boat: 'sailboat', pedalo: 'pedalo', parasol: 'parasol', car: 'car' }[k] || k, k === 'parasol' ? { openAt: -1 } : {});
      m.scale.multiplyScalar(s); g.add(m); return m; };
    const items = (o.items || []).map(it => ({ ...it, m: mk(it) }));
    const ang = t => { const u = Math.max(0, t - t0); return dir * (u < Du ? 0.5 * wm * u * u / Du : 0.5 * wm * Du + wm * (u - Du)); };
    g.userData.update = t => {
      const a = ang(t), u = clamp01((t - t0) / Du); spin.rotation.y = a; funnel.rotation.y = a * 1.7; ft.offset.x = -a * 0.15;
      const dd = 0.15 + 0.85 * smooth(u); funnel.scale.set(1, dd, 1); funnel.position.y = -dep * dd / 2 + 0.02;
      for (const it of items) { const v = clamp01((t - (it.from ?? t0)) / (it.dur ?? Du)), r = it.r * Math.pow(1 - v, 1.25), ai = (it.a ?? 0) + dir * TAU * (it.turns ?? 1.5) * Math.pow(v, 1.4);
        const y = r < rf ? -dep * dd * (1 - r / rf) * 0.85 : 0.03 * Math.sin(t * 3 + it.r); it.m.visible = v < 0.995;
        it.m.position.set(r * Math.cos(ai), y, r * Math.sin(ai)); it.m.rotation.set(0, -ai + dir * t * (it.selfSpin ?? 2), 0.5 * v * dir); }
    };
    g.userData.update(0); return g;
  },
  // A cartoon submarine (front +Z: the bow; o.len long, 6 m): a fat grey-blue hull, a red band, lit portholes, a conning tower with a hatch that
  // opens at o.hatchAt (userData.hatch: the hole, an actor pops out of it), diving planes, tail fins and a turning propeller; the periscope rises and
  // drops by o.peri [[t, 0..1], ...] and turns by o.periYaw [[t, deg], ...] (0 looks along +Z); o.periOnly: only the periscope (its foot at the pivot)
  submarine(o) {
    const Lh = o.len ?? 6, Hh = Lh * 0.26, g = grp(), hull = o.color || '#5E6B7A', dark = '#2E3640';
    const twH = Hh * 0.62, twL = Lh * 0.24, twW = Hh * 0.42, twZ = -Lh * 0.04, twY = Hh * 0.9, PL = Hh * 0.9;
    const peri = grp(at(cyl(Hh * 0.035, Hh * 0.035, PL, '#3A424C', 8, { pivot: 'bottom' }), 0, 0, 0)); const ph = grp();
    ph.add(at(box(Hh * 0.1, Hh * 0.12, Hh * 0.2, '#3A424C', { outline: 0.01 }), 0, 0, Hh * 0.05), at(new THREE.Mesh(new THREE.CircleGeometry(Hh * 0.042, 14), L('#101216')), 0, 0, Hh * 0.152),
      at(ball(Hh * 0.012, '#FFFFFF', 5), Hh * 0.014, Hh * 0.016, Hh * 0.156)); ph.position.y = PL; peri.add(ph);
    if (o.periOnly) { g.add(peri); g.userData.update = t => { peri.position.y = -PL + PL * keyAt(o.peri, t, 1); peri.rotation.y = keyAt(o.periYaw, t, 0) * PI / 180; }; g.userData.update(0); return g; }
    const body = new THREE.Mesh(new THREE.CapsuleGeometry(Hh / 2, Lh - Hh, 6, 18), L(hull)); body.rotation.x = PI / 2; body.position.y = Hh / 2; body.castShadow = true; g.add(body);
    const band = new THREE.Mesh(new THREE.CylinderGeometry(Hh * 0.51, Hh * 0.51, Lh * 0.05, 22, 1, true), L('#C8322A')); band.rotation.x = PI / 2; band.position.set(0, Hh / 2, Lh * 0.24); g.add(band);
    for (let i = 0; i < 4; i++) for (const sd of [-1, 1]) { const p = grp(at(new THREE.Mesh(new THREE.CircleGeometry(Hh * 0.075, 14), new THREE.MeshLambertMaterial({ color: '#FFE9A0', emissive: '#8A6A10' })), 0, 0, 0.004),
        at(new THREE.Mesh(new THREE.TorusGeometry(Hh * 0.08, Hh * 0.014, 5, 14), L('#C9D1D8')), 0, 0, 0)); p.position.set(sd * Hh * 0.5, Hh * 0.52, -Lh * 0.12 + i * Lh * 0.13); p.rotation.y = sd * PI / 2; g.add(p); }
    const tw = grp(at(box(twW, twH, twL - twW, hull, { outline: 0.015 }), 0, twH / 2, -twW / 2 * 0), at(cyl(twW / 2, twW / 2, twH, hull, 14), 0, twH / 2, (twL - twW) / 2), at(cyl(twW / 2, twW / 2, twH, hull, 14), 0, twH / 2, -(twL - twW) / 2));
    for (const sd of [-1, 1]) tw.add(at(box(Hh * 0.42, Hh * 0.025, Hh * 0.16, hull, { outline: 0.01 }), sd * (twW / 2 + Hh * 0.2), twH * 0.6, (twL - twW) * 0.2));
    tw.add(at(new THREE.Mesh(new THREE.CircleGeometry(twW * 0.3, 14), L('#0A0B0E')), 0, twH + 0.006, -(twL - twW) * 0.25, -PI / 2, 0, 0));
    const hatch = grp(at(cyl(twW * 0.32, twW * 0.32, Hh * 0.035, dark, 14), 0, Hh * 0.0175, twW * 0.32)); hatch.position.set(0, twH + 0.004, -(twL - twW) * 0.25 - twW * 0.32); tw.add(hatch);
    peri.position.set(0, twH - PL, (twL - twW) * 0.3); tw.add(peri); tw.position.set(0, twY, twZ); g.add(tw);
    for (const sd of [-1, 1]) g.add(at(box(Hh * 0.5, Hh * 0.03, Hh * 0.22, hull, { outline: 0.01 }), sd * Hh * 0.55, Hh * 0.45, -Lh * 0.42));
    g.add(at(box(Hh * 0.03, Hh * 0.5, Hh * 0.22, hull, { outline: 0.01 }), 0, Hh * 0.75, -Lh * 0.42));
    const pr = grp(at(new THREE.Mesh(new THREE.ConeGeometry(Hh * 0.07, Hh * 0.16, 8), L('#C9A43E')), 0, 0, -Hh * 0.04, -PI / 2, 0, 0));
    for (let i = 0; i < 3; i++) pr.add(at(box(Hh * 0.07, Hh * 0.3, Hh * 0.02, '#C9A43E', { outline: 0.006 }), 0, 0, 0, 0, 0, i * TAU / 3).translateY(Hh * 0.15));
    pr.position.set(0, Hh / 2, -Lh / 2 - Hh * 0.06); g.add(pr);
    g.userData.update = t => {
      pr.rotation.z = t * 10; hatch.rotation.x = o.hatchAt == null ? 0 : -1.9 * outBack(clamp01((t - o.hatchAt) / 0.3));
      peri.position.y = twH - PL + PL * keyAt(o.peri, t, 0); peri.rotation.y = keyAt(o.periYaw, t, 0) * PI / 180;
    };
    g.userData.update(0); g.userData.hatch = [0, twY + twH, twZ - (twL - twW) * 0.25]; return g;
  },
  // A wall map (front +Z, o.w × o.h, the pivot at its middle): a pale country with a dark coast, rivers and towns, and a new blue sea in the middle
  // shaped like a bathtub on four feet, painted on from left to right between o.paint [t0, t1] (a wet edge where the roller is), the word MER and a
  // little boat appearing in it at o.labelAt; o.paint absent: already painted
  seaMap(o) {
    const W = o.w ?? 2.4, H = o.h ?? 1.7, g = grp(at(box(W + 0.1, H + 0.1, 0.04, '#6B4F3A', { outline: 0.008 }), 0, 0, -0.025));
    const C = [[0.5, 0.06], [0.7, 0.14], [0.86, 0.2], [0.82, 0.42], [0.9, 0.62], [0.78, 0.84], [0.56, 0.93], [0.36, 0.9], [0.2, 0.8], [0.18, 0.62], [0.08, 0.5], [0.14, 0.32], [0.3, 0.24], [0.36, 0.1]];
    g.add(canvasPlane(W, H, (c, Wc, Hc) => { c.fillStyle = '#BFE3F2'; c.fillRect(0, 0, Wc, Hc); c.beginPath(); C.forEach(([x, y], i) => { const px = x * Wc, py = y * Hc; if (i) c.lineTo(px, py); else c.moveTo(px, py); }); c.closePath();
      c.fillStyle = '#F2E6C4'; c.fill(); c.lineWidth = Wc * 0.008; c.strokeStyle = '#4A3B2A'; c.stroke(); c.strokeStyle = '#5B9BD0'; c.lineWidth = Wc * 0.004;
      for (const r of [[[0.55, 0.2], [0.5, 0.35], [0.56, 0.5]], [[0.3, 0.4], [0.36, 0.55], [0.3, 0.7]], [[0.7, 0.55], [0.64, 0.7], [0.68, 0.85]]]) { c.beginPath(); r.forEach(([x, y], i) => { if (i) c.lineTo(x * Wc, y * Hc); else c.moveTo(x * Wc, y * Hc); }); c.stroke(); }
      c.fillStyle = '#4A3B2A'; for (const [x, y] of [[0.48, 0.26], [0.72, 0.36], [0.28, 0.66], [0.62, 0.78], [0.4, 0.82]]) { c.beginPath(); c.arc(x * Wc, y * Hc, Wc * 0.009, 0, TAU); c.fill(); }
      c.font = `900 ${Hc * 0.06}px Arial`; c.textAlign = 'center'; c.fillText('CARTE', Wc / 2, Hc * 0.045); }, { res: 768 }));
    const sea = canvasPlane(W, H, (c, Wc, Hc) => { c.clearRect(0, 0, Wc, Hc); const x0 = Wc * 0.3, y0 = Hc * 0.4, w = Wc * 0.4, h = Hc * 0.2, r = h * 0.5;
      c.beginPath(); c.moveTo(x0, y0); c.lineTo(x0 + w, y0); c.lineTo(x0 + w, y0 + h - r); c.quadraticCurveTo(x0 + w, y0 + h, x0 + w - r, y0 + h); c.lineTo(x0 + r, y0 + h); c.quadraticCurveTo(x0, y0 + h, x0, y0 + h - r); c.closePath();
      c.fillStyle = '#2F7FC4'; c.fill(); c.lineWidth = Wc * 0.007; c.strokeStyle = '#173F66'; c.stroke();
      c.fillStyle = '#173F66'; for (const fx of [0.12, 0.88]) { c.beginPath(); c.ellipse(x0 + w * fx, y0 + h + Hc * 0.025, Wc * 0.016, Hc * 0.028, 0, 0, TAU); c.fill(); }
      c.fillRect(x0 + w - Wc * 0.012, y0 - Hc * 0.07, Wc * 0.012, Hc * 0.07); c.fillRect(x0 + w - Wc * 0.05, y0 - Hc * 0.075, Wc * 0.05, Hc * 0.014);
      c.strokeStyle = 'rgba(255,255,255,0.75)'; c.lineWidth = Wc * 0.004; for (let i = 0; i < 4; i++) { c.beginPath(); const yy = y0 + h * (0.25 + 0.17 * i); for (let k = 0; k <= 12; k++) { const xx = x0 + w * (0.08 + 0.84 * k / 12); c.lineTo(xx, yy + Math.sin(k * 1.6) * Hc * 0.006); } c.stroke(); } }, { res: 768, transparent: true });
    sea.position.z = 0.004; g.add(sea); const map = sea.material.map; map.wrapS = THREE.ClampToEdgeWrapping;
    const edge = at(box(0.025, H * 0.26, 0.012, '#5FA8E0'), 0, H * 0.0, 0.01); g.add(edge);
    const lab = canvasPlane(W * 0.3, H * 0.12, (c, Wc, Hc) => { c.clearRect(0, 0, Wc, Hc); c.fillStyle = '#FFFFFF'; c.font = `900 ${Hc * 0.8}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('MER', Wc * 0.42, Hc * 0.55);
      c.beginPath(); c.moveTo(Wc * 0.8, Hc * 0.62); c.lineTo(Wc * 0.96, Hc * 0.62); c.lineTo(Wc * 0.92, Hc * 0.78); c.lineTo(Wc * 0.84, Hc * 0.78); c.closePath(); c.fill(); c.fillRect(Wc * 0.875, Hc * 0.2, Wc * 0.012, Hc * 0.42);
      c.beginPath(); c.moveTo(Wc * 0.89, Hc * 0.22); c.lineTo(Wc * 0.95, Hc * 0.55); c.lineTo(Wc * 0.89, Hc * 0.55); c.closePath(); c.fill(); }, { res: 384, transparent: true });
    lab.position.set(0, -H * 0.0, 0.008); g.add(lab);
    g.userData.update = t => { const u = o.paint ? clamp01((t - o.paint[0]) / (o.paint[1] - o.paint[0])) : 1; sea.visible = u > 0.002; sea.scale.x = Math.max(0.002, u); sea.position.x = -W / 2 + W * u / 2; map.repeat.x = Math.max(0.002, u); map.offset.x = 0;
      edge.visible = !!o.paint && u > 0.29 && u < 0.71; edge.position.x = -W / 2 + W * u; const lu = o.labelAt == null ? (o.paint ? 0 : 1) : clamp01((t - o.labelAt) / 0.2); lab.visible = lu > 0; lab.scale.setScalar(Math.max(0.01, outBack(lu))); };
    g.userData.update(0); return g;
  },
  // A fish on dry ground, flopping (pivot under it): it hops and flips from one side to the other o.rate times a second (o.phase), the tail wagging;
  // o.s its length (0.3 m), o.color
  fishFlop(o) {
    const s = o.s ?? 0.3, g = grp(), f = grp(), col = o.color || '#9AA7B2';
    const b = ball(1, col, 12); b.scale.set(0.09 * s, 0.22 * s, 0.5 * s); f.add(b);
    const tail = new THREE.Mesh(new THREE.ConeGeometry(0.16 * s, 0.24 * s, 3), L(col)); tail.scale.z = 0.25; tail.rotation.x = -PI / 2; tail.position.z = -0.55 * s; f.add(tail);
    for (const sd of [-1, 1]) f.add(at(ball(0.04 * s, '#FFFFFF', 6), sd * 0.07 * s, 0.05 * s, 0.32 * s), at(ball(0.022 * s, '#14161B', 5), sd * 0.095 * s, 0.05 * s, 0.34 * s));
    g.add(f);
    g.userData.update = t => { const x = t * (o.rate ?? 1.6) + (o.phase ?? 0), n = Math.floor(x), ph = x - n, side = n % 2 ? 1 : -1;
      f.position.y = 0.09 * s + 0.35 * s * Math.sin(PI * ph); f.rotation.z = side * (PI / 2) * (1 - 2 * smooth(ph)) * 0.92; tail.rotation.y = 0.6 * Math.sin(t * 22); };
    g.userData.update(0); return g;
  },
  // A little red crab (pivot under it, facing +Z): it scuttles sideways along o.path [[t, x, z], ...] (in the parent's frame), legs flickering while it
  // moves, and snaps its claws at o.snap [t, ...]; o.s its width (0.2 m)
  crab(o) {
    const s = o.s ?? 0.2, g = grp(), red = o.color || '#D8452E', body = ball(1, red, 12); body.scale.set(0.5 * s, 0.2 * s, 0.36 * s); body.position.y = 0.18 * s; g.add(body);
    for (const sd of [-1, 1]) g.add(at(cyl(0.012 * s, 0.012 * s, 0.14 * s, red, 5, { pivot: 'bottom' }), sd * 0.1 * s, 0.3 * s, 0.22 * s), at(ball(0.045 * s, '#FFFFFF', 6), sd * 0.1 * s, 0.45 * s, 0.22 * s), at(ball(0.022 * s, '#14161B', 5), sd * 0.1 * s, 0.46 * s, 0.26 * s));
    const claws = [-1, 1].map(sd => { const c = grp(at(box(0.16 * s, 0.06 * s, 0.06 * s, red), 0, 0, 0.06 * s)); const up = grp(at(box(0.12 * s, 0.05 * s, 0.14 * s, red), 0, 0.03 * s, 0.07 * s)), lo = grp(at(box(0.1 * s, 0.04 * s, 0.12 * s, red), 0, -0.03 * s, 0.06 * s));
      up.position.z = 0.12 * s; lo.position.z = 0.12 * s; c.add(up, lo); c.userData = { up, lo }; c.position.set(sd * 0.42 * s, 0.2 * s, 0.22 * s); c.rotation.y = -sd * 0.5; g.add(c); return c; });
    const legs = []; for (const sd of [-1, 1]) for (let i = 0; i < 3; i++) { const l = grp(at(box(0.3 * s, 0.025 * s, 0.025 * s, red), sd * 0.15 * s, 0, 0)); l.position.set(sd * 0.32 * s, 0.16 * s, (i - 1) * 0.12 * s); l.rotation.z = -sd * 0.55; g.add(l); legs.push([l, sd, i]); }
    const path = o.path || [[0, 0, 0]];
    g.userData.update = t => { let x = path[0][1], z = path[0][2], moving = false;
      for (let i = 1; i < path.length; i++) if (t >= path[i - 1][0] && t < path[i][0]) { const u = (t - path[i - 1][0]) / (path[i][0] - path[i - 1][0]); x = path[i - 1][1] + (path[i][1] - path[i - 1][1]) * u; z = path[i - 1][2] + (path[i][2] - path[i - 1][2]) * u; moving = Math.hypot(path[i][1] - path[i - 1][1], path[i][2] - path[i - 1][2]) > 0.01; } else if (t >= path[i][0]) { x = path[i][1]; z = path[i][2]; }
      g.position.set(x, 0, z); for (const [l, sd, i] of legs) l.rotation.z = -sd * (0.55 + (moving ? 0.3 * Math.sin(t * 30 + i * 2.1 + (sd > 0 ? PI : 0)) : 0.04 * Math.sin(t * 2 + i)));
      let sn = 0; for (const ts of o.snap || []) { const a = t - ts; if (a >= 0 && a < 0.3) sn = Math.max(sn, Math.sin(PI * a / 0.3)); }
      for (const c of claws) { c.userData.up.rotation.x = -0.6 * sn - 0.05; c.userData.lo.rotation.x = 0.4 * sn; } body.position.y = 0.18 * s + (moving ? 0.012 * s * Math.abs(Math.sin(t * 30)) : 0); };
    g.userData.update(0); return g;
  },
  // An inflatable duck ring (pivot at its middle, the head at +Z): flat and crumpled until o.inflate [t0, t1] blows it up with an overshoot; o.r, o.bob
  duckRing(o) {
    const R = o.r ?? 0.42, g = grp(), inner = grp(); g.add(inner);
    inner.add(at(new THREE.Mesh(new THREE.TorusGeometry(R, R * 0.36, 10, 22), L('#F7D23A')), 0, 0, 0, PI / 2, 0, 0));
    const head = grp(at(cyl(R * 0.16, R * 0.2, R * 0.5, '#F7D23A', 8, { pivot: 'bottom' }), 0, 0, 0), at(ball(R * 0.3, '#F7D23A', 10), 0, R * 0.62, R * 0.06));
    const bk = new THREE.Mesh(new THREE.ConeGeometry(R * 0.1, R * 0.26, 8), L('#F08A24')); bk.rotation.x = PI / 2; bk.position.set(0, R * 0.58, R * 0.42); head.add(bk);
    for (const sd of [-1, 1]) head.add(at(ball(R * 0.05, '#14161B', 6), sd * R * 0.14, R * 0.72, R * 0.3));
    head.position.set(0, R * 0.2, R); inner.add(head);
    g.userData.update = t => { const u = o.inflate ? clamp01((t - o.inflate[0]) / (o.inflate[1] - o.inflate[0])) : 1, sc = 0.15 + 0.85 * outBack(u);
      inner.scale.set(sc, Math.max(0.08, sc * (0.3 + 0.7 * u)), sc); head.rotation.x = (1 - u) * 1.2; inner.position.y = o.bob ? 0.03 * Math.sin(t * 3) : 0; };
    g.userData.update(0); return g;
  },
  // A lighthouse whose lamp turns a beam of light round (pivot at the foot of its rock): o.h its height, the beam o.len long from o.onAt, turning
  // o.rate turns a second from o.yaw0 degrees, or aimed by o.aim [[t, deg], ...]; userData.lamp: the lamp's height
  lighthouseLive(o) {
    const Hh = o.h ?? 6, g = grp(buildProp('lighthouse', { h: Hh })), ly = Hh * 0.811, len = o.len ?? Hh * 2.2;
    const geo = new THREE.ConeGeometry(o.spread ?? Hh * 0.28, len, 24, 1, true); geo.translate(0, -len / 2, 0); geo.rotateX(-PI / 2);
    const beam = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: '#FFF3B0', transparent: true, opacity: o.opacity ?? 0.32, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }));
    const glowB = ball(Hh * 0.05, new THREE.MeshBasicMaterial({ color: '#FFF6C8' }), 10); const bg = grp(beam); bg.position.y = ly; glowB.position.y = ly; g.add(bg, glowB);
    g.userData.update = t => { const on = o.onAt == null || t >= o.onAt; bg.visible = glowB.visible = on;
      bg.rotation.y = o.aim ? keyAt(o.aim, t, 0) * PI / 180 : ((o.yaw0 ?? 0) * PI / 180 + Math.max(0, t - (o.onAt ?? 0)) * (o.rate ?? 0.35) * TAU); glowB.scale.setScalar(on ? 1 + 0.15 * Math.sin(t * 8) : 1); };
    g.userData.update(0); g.userData.lamp = [0, ly, 0]; return g;
  },
  // (pass 2 of 71) A stream of water arcing through the air (pivot at the nozzle, world space): from the pivot it climbs o.h (0.7 m) over the straight line
  // and lands at o.to [dx, dy, dz]; from o.from (0) it shoots out along the curve in o.grow (0.2 s); white foam blobs run along it so it reads as
  // flowing, and drops spring up where it lands; o.r (0.06) its thickness, o.color the water
  hoseArc(o) {
    const g = grp(), to = new THREE.Vector3(...(o.to || [-2, -0.5, -1])), H = o.h ?? 0.7, R = o.r ?? 0.06, from = o.from ?? 0, grow = o.grow ?? 0.2;
    const a = new THREE.Vector3(0, 0, 0), c = a.clone().lerp(to, 0.5); c.y = Math.max(a.y, to.y) + 2 * H;
    const curve = new THREE.QuadraticBezierCurve3(a, c, to), N = 48;
    const tube = new THREE.Mesh(new THREE.TubeGeometry(curve, N, R, 8, false), new THREE.MeshBasicMaterial({ color: o.color || '#BFE6FF', transparent: true, opacity: o.opacity ?? 0.88, depthWrite: false }));
    const core = new THREE.Mesh(new THREE.TubeGeometry(curve, N, R * 0.45, 6, false), new THREE.MeshBasicMaterial({ color: '#F4FBFF' })); g.add(tube, core);
    const total = tube.geometry.index.count, totalC = core.geometry.index.count;
    const foam = Array.from({ length: 7 }, (_, i) => { const m = ball(R * 0.9, new THREE.MeshBasicMaterial({ color: '#FFFFFF' }), 6); g.add(m); return m; });
    const drops = Array.from({ length: 10 }, (_, i) => { const m = ball(R * 0.7, new THREE.MeshBasicMaterial({ color: '#E8F7FF' }), 6); g.add(m); return { m, ph: hash(i + 1), ang: i * 2.399 }; });
    g.userData.update = t => {
      const u = t - from, on = u >= 0, k = on ? clamp01(u / grow) : 0;
      tube.visible = core.visible = on; tube.geometry.setDrawRange(0, Math.floor(total * k / 6) * 6); core.geometry.setDrawRange(0, Math.floor(totalC * k / 6) * 6);
      foam.forEach((m, i) => { const f = ((u * 1.6 + i / foam.length) % 1); m.visible = on && f <= k; if (m.visible) m.position.copy(curve.getPoint(f)); });
      drops.forEach(d => { const f = ((u * 2.2 + d.ph) % 1), vis = on && k >= 1; d.m.visible = vis; if (!vis) return;
        d.m.position.set(to.x + Math.cos(d.ang) * 0.35 * f, to.y + 0.9 * f - 1.6 * f * f, to.z + Math.sin(d.ang) * 0.35 * f); d.m.scale.setScalar(1 - 0.6 * f); });
    };
    g.userData.update(-1); return g;
  },
};
