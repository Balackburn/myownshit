// « Le stylo » (story 92): this man pocketed the town hall's pen, the only pen of the State. Files piled up to the ceiling, weddings were
// suspended, births put off to Monday; a special edition on the eleventh day without a pen; the president wanted to resign and could not sign;
// customs searched every pencil case; his mother turned him in; special forces jumped onto his balcony, which gave way with the three below; the
// pen was in his pocket, chewed, out of ink for ten years; his own new pen is now chained at the counter, and he visits it on Thursdays.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
// Thin things (the pens, the chain) carry a hull of absolute width (a rim) so they read on every ground (lesson of the cheveu hair).
import * as THREE from 'three';
import { box, cyl, sphere, mat } from './style.js';
import { grp, at, canvasPlane, glassMat, buildProp } from './props.js';

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
// linear interpolation through keys [[t, v], ...]: before the first key its value, after the last its value
function linAt(keys, t, def = 0) {
  if (!keys || !keys.length) return def;
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) if (t < keys[i][0]) { const [a, va] = keys[i - 1], [b, vb] = keys[i]; return va + (vb - va) * (t - a) / Math.max(1e-6, b - a); }
  return keys[keys.length - 1][1];
}
// a damped pendulum angle from kicks [[t0, amp], ...] (rad), f rad/s, k the damping
function swingAt(kicks, t, f = 9, k = 2.6) { let a = 0; for (const [t0, amp] of kicks || []) { const u = t - t0; if (u >= 0) a += amp * Math.exp(-k * u) * Math.sin(f * u + PI / 2) * (u < 0.05 ? u / 0.05 : 1); } return a; }
const lam = (c, o = {}) => new THREE.MeshLambertMaterial({ color: c, ...o });
const phong = (c, sh = 80, spec = '#FFFFFF', em = '#000000') => new THREE.MeshPhongMaterial({ color: c, specular: spec, shininess: sh, emissive: em });
const basic = (c, o = {}) => new THREE.MeshBasicMaterial({ color: c, ...o });
// a mesh with a back-face hull of absolute width w round it (cylinders and boxes: the hull is the same shape grown by w on every side)
function rimmed(geoFn, m, rimColor, w) {
  const g = grp(), ms = new THREE.Mesh(geoFn(0), m); ms.castShadow = true; g.add(ms);
  if (rimColor && w > 0) { const h = new THREE.Mesh(geoFn(w), basic(rimColor, { side: THREE.BackSide })); h.castShadow = false; h.userData.noAO = true; g.add(h); }
  return g;
}
const cylR = (r0, r1, h, seg = 14) => w => new THREE.CylinderGeometry(r0 + w, r1 + w, h + 2 * w, seg);
const boxR = (x, y, z) => w => new THREE.BoxGeometry(x + 2 * w, y + 2 * w, z + 2 * w);
// a text fitted to a canvas box (measured, never a fixed size)
function fitText(c, s, x, y, maxW, maxH, weight = 900) { let px = maxH; c.font = `${weight} ${px}px Arial`; const tw = c.measureText(s).width; if (tw > maxW) { px *= maxW / tw; c.font = `${weight} ${px}px Arial`; } c.fillText(s, x, y); }
// a soft round sprite texture, shared
let _soft = null;
function softTex() {
  if (_soft) return _soft;
  const c = document.createElement('canvas'); c.width = c.height = 64; const x = c.getContext('2d'), gr = x.createRadialGradient(32, 32, 0, 32, 32, 32);
  gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.5, 'rgba(255,255,255,0.5)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  x.fillStyle = gr; x.fillRect(0, 0, 64, 64); _soft = new THREE.CanvasTexture(c); return _soft;
}
const BRASS = '#D4A93C', BRASS_D = '#9C7424', STEEL = '#59606A', INK = '#16181D';
// the ÉTAT tag (pivot at its hanging ring, the plate below it, front +Z): a cream enamel plate with a brass border, the word on both faces
function etatTag(text, s = 1) {
  const W = 0.17 * s, H = 0.11 * s, g = grp();
  g.add(at(box(W + 0.016 * s, H + 0.016 * s, 0.01 * s, BRASS, { outline: 0.03 }), 0, -0.03 * s - H / 2, 0));
  for (const sd of [1, -1]) { const p = canvasPlane(W, H, (c, cw, ch) => { c.fillStyle = '#F6F0DC'; c.fillRect(0, 0, cw, ch); c.strokeStyle = '#1B2A4A'; c.lineWidth = ch * 0.05; c.strokeRect(ch * 0.07, ch * 0.07, cw - ch * 0.14, ch - ch * 0.14);
      c.fillStyle = '#1B2A4A'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, text, cw / 2, ch * 0.55, cw * 0.82, ch * 0.62); }, { res: 256 });
    p.position.set(0, -0.03 * s - H / 2, sd * 0.0056 * s); if (sd < 0) p.rotation.y = PI; g.add(p); }
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.018 * s, 0.005 * s, 6, 14), phong(BRASS, 60)); ring.position.y = -0.012 * s; g.add(ring);
  return g;
}

export const STYLO_PROPS = {
  // THE PEN (pivot at its middle, the tip down -Y, the clip on the +Z side): an oversized ballpoint o.len (0.46) long, o.r (0.024) thick.
  // o.kind 'state': polished brass with a black grip, a ring at the top of the cap for its chain; 'red': glossy red with a black grip and a chrome
  // clip, no ring. o.chewed: the cap's top squashed flat and wide with tooth marks (o.chew 0..1 or keys [[t, v]]). o.rim / o.rimW: the hull round
  // every part (default dark brown round the brass, white round the red); o.s scales it. userData.ring: the chain point (top), userData.tip
  styPen(o) {
    const L = o.len ?? 0.46, R = o.r ?? 0.024, state = (o.kind || 'state') === 'state', g = grp(), b = grp(); g.add(b); if (o.s) b.scale.setScalar(o.s);
    const main = state ? phong(BRASS, 90, '#FFF2C0', '#3A2A08') : phong(o.color || '#D3212B', 110, '#FFFFFF', '#3A0606');
    const rc = o.rim ?? (state ? '#2A1E0A' : '#FFFFFF'), rw = o.rimW ?? 0.006;
    const part = (geoFn, m, y) => { const p = rimmed(geoFn, m, rc, rw); p.position.y = y; b.add(p); return p; };
    const tipL = 0.07, gripL = 0.09, capL = 0.15;
    const tip = part(w => new THREE.ConeGeometry(R * 0.9 + w, tipL + 2 * w, 14), state ? phong(BRASS_D, 60) : phong('#C9CED6', 90), -L / 2 + tipL / 2); tip.rotation.x = PI;
    b.add(at(sphere(R * 0.18, INK, 1), 0, -L / 2 - 0.002, 0));
    part(cylR(R * 0.93, R * 0.9, gripL), lam('#1C1D22'), -L / 2 + tipL + gripL / 2);
    for (let i = 0; i < 4; i++) b.add(at(cyl(R * 0.97, R * 0.97, 0.006, '#34363E', 14), 0, -L / 2 + tipL + 0.012 + i * 0.02, 0));
    const barL = L - tipL - gripL - capL + 0.01;
    part(cylR(R, R, barL), main, -L / 2 + tipL + gripL + barL / 2);
    b.add(at(cyl(R * 1.08, R * 1.08, 0.012, state ? '#F0D78A' : '#E9EDF2', 14), 0, L / 2 - capL, 0));
    const cap = grp(); cap.position.y = L / 2 - capL / 2; b.add(cap);
    const capBody = rimmed(cylR(R * 1.06, R * 1.06, capL * 0.8), main, rc, rw); capBody.position.y = -capL * 0.1; cap.add(capBody);
    const top = grp(); top.position.y = capL * 0.3; cap.add(top);
    const topM = rimmed(w => new THREE.SphereGeometry(R * 1.06 + w, 14, 8, 0, TAU, 0, PI / 2), main, rc, rw); top.add(topM);
    // (stills 3) the chewed top: the dome gives way to a flattened, splayed plate, a little bent, with tooth notches on its faces
    const teeth = grp(); teeth.position.set(0, capL * 0.24, 0); teeth.rotation.z = 0.14; cap.add(teeth);
    const flat = new THREE.Shape([[-1.15, -0.5], [1.15, -0.5], [1.25, 0.1], [0.95, 0.5], [0.55, 0.3], [0.2, 0.55], [-0.2, 0.32], [-0.6, 0.55], [-1.0, 0.35], [-1.25, 0.05]].map(([x, y]) => new THREE.Vector2(x * R, y * 0.05)));
    const fgeo = w => { const g2 = new THREE.ExtrudeGeometry(flat, { depth: R * 0.75 + 2 * w, bevelEnabled: false }); g2.translate(0, 0, -(R * 0.75 + 2 * w) / 2); if (w) g2.scale(1 + w / R, 1 + w / 0.03, 1); return g2; };
    teeth.add(rimmed(fgeo, main, rc, rw));
    // (round 1) deep V notches bitten into both faces, dented lower rim
    for (const sd of [1, -1]) for (let i = 0; i < 6; i++) teeth.add(at(box(R * 0.26, 0.016, 0.004, '#2A1C06'), (i - 2.5) * R * 0.42, 0.004 + 0.008 * (i % 2), sd * (R * 0.375 + 0.003), 0, 0, 0.3 * (i % 3 - 1)));
    for (const sd of [1, -1]) teeth.add(at(box(R * 2.3, 0.004, 0.003, '#2A1C06'), 0, -0.022, sd * (R * 0.375 + 0.003)));
    const clipC = state ? '#F0D78A' : '#E9EDF2';
    const clip = grp(at(box(R * 0.7, capL * 0.82, 0.007, clipC, { outline: 0.06 }), 0, 0, 0), at(sphere(R * 0.32, clipC, 1), 0, -capL * 0.4, 0.004)); clip.position.set(0, -capL * 0.05, R * 1.06 + 0.008); cap.add(clip);
    let ringG = null;
    if (state) { const ring = rimmed(w => new THREE.TorusGeometry(R * 0.85, R * 0.24 + w, 8, 18), phong(BRASS, 70, '#FFF2C0'), rc, rw); ring.position.y = L / 2 + R * 0.95; ring.rotation.y = PI / 2; b.add(ring); ringG = ring; }
    g.userData.ring = [0, (L / 2 + R * 1.6) * (o.s || 1), 0]; g.userData.tip = [0, -L / 2 * (o.s || 1), 0];
    const chew = t => Array.isArray(o.chew) ? keyAt(o.chew, t, 0, 0.1) : (o.chewed ? (o.chew ?? 1) : 0);
    // (round 1) the chewed parts switch by scale: a visible key on the prop re-shows every child
    g.userData.update = t => { const c = chew(t), on = c >= 0.5, z = 0.0001; top.scale.setScalar(on ? z : 1); teeth.scale.setScalar(on ? 1 : z); if (ringG) ringG.scale.setScalar(on && !o.keepRing ? z : 1); capBody.scale.set(1 + 0.2 * c, 1, 1 - 0.15 * c);
      if (o.spinY) b.rotation.y = o.spinY * t; };
    g.userData.update(0); return g;
  },

  // A link chain hanging from its top (pivot at the top link, down -Y): o.len (0.5) long, links of o.link (0.032) with a tube of o.tube (0.009), steel
  // with a dark hull (o.rim, o.rimW); o.tag: the ÉTAT tag at its end (text, null for none; o.tagS scale); o.swing [[t, amp]]: kicks of a damped
  // pendulum (each lower link lags a little); o.tilt: a constant lean (rad, about Z); o.twist (rad/s): the tag turns a little
  styChain(o) {
    const L = o.len ?? 0.5, Rl = o.link ?? 0.032, tb = o.tube ?? 0.009, g = grp(), pitch = Rl * 1.45, n = Math.max(2, Math.round(L / pitch)), links = [];
    const m = phong(o.color || STEEL, 60, '#DDE6F0'), rc = o.rim ?? '#101216', rw = o.rimW ?? 0.005;
    for (let i = 0; i < n; i++) { const lk = rimmed(w => new THREE.TorusGeometry(Rl * 0.72, tb + w, 6, 14), m, rc, rw); lk.scale.set(1, 1.45, 1); lk.rotation.y = i % 2 ? PI / 2 : 0; const holder = grp(lk); g.add(holder); links.push(holder); }
    let tag = null; if (o.tag !== null && o.tag !== false) { tag = etatTag(o.tag || 'ÉTAT', o.tagS ?? 1); g.add(tag); }
    g.userData.update = t => { let x = 0, y = 0; for (let i = 0; i < n; i++) { const a = (o.tilt ?? 0) + swingAt(o.swing, t - i * 0.012, o.f ?? 9, o.k ?? 2.6) * (1 + 0.25 * i / n);
        const xn = x + Math.sin(a) * pitch, yn = y - Math.cos(a) * pitch; links[i].position.set((x + xn) / 2, (y + yn) / 2, 0); links[i].rotation.z = a; x = xn; y = yn; }
      if (tag) { const a = (o.tilt ?? 0) + swingAt(o.swing, t - n * 0.012, o.f ?? 9, o.k ?? 2.6) * 1.3; tag.position.set(x, y + 0.01, 0); tag.rotation.set(0, (o.tagYaw ?? 0) + 0.25 * Math.sin((o.twist ?? 1.3) * t), a); } };
    g.userData.update(0); g.userData.end = () => links.length ? links[links.length - 1].position.toArray() : [0, 0, 0]; return g;
  },

  // The town hall counter (guichet; pivot at the floor under its middle, the public side +Z): a wooden counter o.w (2.2) wide, o.h (1.05) high, 0.62
  // deep, raised panels on its front, a dark top; o.plate: a plate on its front ('ÉTAT CIVIL'); an eyebolt on the top at [o.ax, o.az] (userData.anchor:
  // its ring, local); o.tag: the ÉTAT tag hanging on a stub of chain over the front edge beside the bolt (true by default); o.dust [x, z, ry]: a clean
  // pen-shaped outline in a patch of grey dust on the top; o.cutAt: from then the cut chain lies from the bolt to the edge and hangs down the front
  // (o.cutLen 0.32), swinging (o.swing); o.color / o.top / o.panel: its colours
  styCounter(o) {
    const W = o.w ?? 2.2, H = o.h ?? 1.05, D = 0.62, g = grp(), C = o.color || '#B5834F', T = o.top || '#5E3E26', Pn = o.panel || '#A57444';
    g.add(at(box(W, H - 0.04, D, C, { pivot: 'bottom', outline: 0.005 }), 0, 0, 0), at(box(W + 0.1, 0.05, D + 0.12, T, { pivot: 'bottom', outline: 0.004 }), 0, H - 0.05, 0.02));
    const np = Math.max(2, Math.round(W / 0.75)); for (let i = 0; i < np; i++) { const pw = W / np - 0.12; g.add(at(box(pw, H * 0.55, 0.03, Pn, { outline: 0.006 }), -W / 2 + W / np * (i + 0.5), H * 0.42, D / 2 + 0.012)); }
    g.add(at(box(W, 0.1, 0.03, '#3A2A1C'), 0, 0.05, D / 2 + 0.01));
    if (o.plate !== false) { const pw = o.plateW ?? 0.62, ph = pw * 0.24, pl = canvasPlane(pw, ph, (c, cw, ch) => { c.fillStyle = o.plateBg || '#1B2A4A'; c.fillRect(0, 0, cw, ch); c.fillStyle = '#F4EEDC'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, o.plate || 'ÉTAT CIVIL', cw / 2, ch * 0.55, cw * 0.86, ch * 0.62); }, { res: 256 });
      g.add(at(box(pw + 0.04, ph + 0.04, 0.02, BRASS, { outline: 0.01 }), o.plateX ?? -W * 0.25, H * 0.82, D / 2 + 0.02), at(pl, o.plateX ?? -W * 0.25, H * 0.82, D / 2 + 0.032)); }
    const ax = o.ax ?? 0.3, az = o.az ?? 0.16;
    if (o.bolt !== false) { g.add(at(cyl(0.035, 0.04, 0.012, BRASS_D, 12, { outline: 0.02 }), ax, H + 0.006, az));
      const eye = new THREE.Mesh(new THREE.TorusGeometry(0.024, 0.008, 6, 14), phong(BRASS, 70)); eye.position.set(ax, H + 0.04, az); g.add(eye); }
    g.userData.anchor = [ax, H + 0.045, az]; g.userData.top = H;
    if (o.tag !== false) { const stub = buildProp('styChain', { len: 0.07, tag: 'ÉTAT', tagS: o.tagS ?? 1.25, swing: o.tagSwing || [], tilt: 0 }); stub.position.set(ax + 0.12, H - 0.005, D / 2 + 0.09); g.add(stub); g.userData.stub = stub;
      g.add(at(cyl(0.012, 0.012, 0.03, BRASS_D, 8), ax + 0.12, H + 0.005, D / 2 + 0.06)); }
    if (o.dust) { const [dx, dz, dry] = o.dust, dw = 0.62, dd = 0.2, s = o.dustS ?? 1;
      const d = canvasPlane(dw * s, dd * s, (c, cw, ch) => { c.fillStyle = T; c.fillRect(0, 0, cw, ch); for (let i = 0; i < 900; i++) { c.fillStyle = `rgba(226,220,206,${0.35 + 0.5 * hsh(i)})`; const r = 1 + 3 * hsh(i + 7); c.beginPath(); c.arc(hsh(i + 1) * cw, hsh(i + 3) * ch, r, 0, TAU); c.fill(); }
        const y = ch / 2, x0 = cw * 0.12, x1 = cw * 0.86, r = ch * 0.17; c.beginPath(); c.moveTo(x0 - r * 1.6, y); c.lineTo(x0, y - r); c.lineTo(x1, y - r * 1.12); c.arc(x1, y, r * 1.12, -PI / 2, PI / 2); c.lineTo(x0, y + r); c.closePath();
        c.fillStyle = '#3A2616'; c.fill(); c.lineWidth = ch * 0.07; c.strokeStyle = '#FFFBEF'; c.stroke();
        c.beginPath(); c.arc(x1 + r * 1.75, y, r * 0.55, 0, TAU); c.stroke(); }, { res: 512 });
      d.rotation.set(-PI / 2, 0, dry || 0); d.position.set(dx, H + 0.003, dz); g.add(d); }
    if (o.cutAt != null) { const cut = grp(); g.add(cut); const ez = D / 2 + 0.07, n = Math.max(2, Math.round((ez - az) / 0.045));
      for (let i = 0; i <= n; i++) { const lk = new THREE.Mesh(new THREE.TorusGeometry(0.023, 0.009, 6, 12), phong(STEEL, 60, '#DDE6F0')); lk.scale.set(1.45, 1, 1); lk.position.set(ax + 0.02 * Math.sin(i), H + 0.012, az + (ez - az) * i / n); lk.rotation.set(i % 2 ? 0 : PI / 2, PI / 2, 0); cut.add(lk); }
      const hang = buildProp('styChain', { len: o.cutLen ?? 0.32, tag: null, swing: o.swing || [[o.cutAt, 0.5]], tilt: 0.05 }); hang.position.set(ax, H + 0.005, ez + 0.01); cut.add(hang);
      g.userData.update = t => { cut.visible = t >= o.cutAt; hang.userData.update?.(t); g.userData.stub?.userData.update?.(t); }; }
    else g.userData.update = t => { g.userData.stub?.userData.update?.(t); };
    g.userData.update(0); return g;
  },

  // Towers of unsigned files (pivot at the floor): o.towers [[x, z, phase], ...] each a stack of folders 0.44 x 0.32 (beige, pink, blue, buff, with
  // white paper edges and a few sheets sticking out) that grows to o.ceil (2.9) by o.grow keys [[t, 0..1]] (a fraction of the ceiling; each tower
  // later by its phase, o.blend the rise time, an overshoot squash when it meets the ceiling); o.ceiling: a ceiling slab at o.ceil (true)
  styFiles(o) {
    const CEIL = o.ceil ?? 2.9, th = 0.055, N = Math.ceil(CEIL / th) + 1, g = grp(), towers = [], cols = ['#E8D7A2', '#E3A8A0', '#A9C3E0', '#D9C08A', '#C9E0B4'];
    for (const [x, z, ph = 0] of o.towers || [[0, 0, 0]]) { const tw = grp(); tw.position.set(x, 0, z); g.add(tw); const fs = [];
      for (let i = 0; i < N; i++) { const f = grp(), c = cols[Math.floor(hsh(i * 3 + x * 7) * cols.length)], j = (hsh(i + z * 5) - 0.5) * 0.06;
        f.add(at(box(0.44, th * 0.82, 0.32, c, { outline: 0.012 }), 0, th * 0.41, 0), at(box(0.42, th * 0.18, 0.3, '#FBF8F0'), 0.004, th * 0.86, 0));
        if (hsh(i * 11 + x) > 0.7) f.add(at(box(0.2, 0.004, 0.24, '#FBF8F0'), 0.2, th * 0.5, 0.02, 0, 0.4, 0));
        f.position.set(j, i * th, (hsh(i * 2 + 1) - 0.5) * 0.04); f.rotation.y = (hsh(i * 5 + 2) - 0.5) * 0.18; tw.add(f); fs.push(f); }
      towers.push({ tw, fs, ph }); }
    if (o.ceiling !== false) { const c = at(box(o.ceilW ?? 8, 0.12, o.ceilD ?? 6, o.ceilColor || '#EDE7DA', { outline: 0.003, emissive: o.ceilGlow || '#5A574F', unique: true }), o.ceilX ?? 0, CEIL + 0.06, o.ceilZ ?? 0); c.castShadow = false; g.add(c);
      for (let i = 0; i < 4; i++) { const tl = at(box(1.0, 0.03, 0.25, '#FFF8E0', { emissive: '#FFF0C0', noGrain: true }), (o.ceilX ?? 0) - 1.6 + i * 1.1, CEIL - 0.01, (o.ceilZ ?? 0) + 0.6); tl.castShadow = false; g.add(tl); } }
    g.userData.update = t => { for (const { tw, fs, ph } of towers) { const f = keyAt(o.grow || [[0, 1]], t - ph, 0, o.blend ?? 0.25), h = f * CEIL, k = Math.min(N, Math.floor(h / th + 0.001));
        fs.forEach((m, i) => { m.visible = i < k; });
        const hit = (o.grow || []).length ? (o.grow.find(([, v]) => v >= 0.999) || [null])[0] : null; let sq = 0; if (hit != null) { const u = t - ph - hit - (o.blend ?? 0.25) * 0.7; if (u >= 0 && u < 0.6) sq = Math.exp(-6 * u) * Math.sin(u * 30) * 0.06; }
        tw.scale.set(1 + sq, 1 - sq * 0.5, 1 + sq); } };
    g.userData.update(0); return g;
  },

  // A sign card (pivot at the hook above it when o.string, else its middle; front +Z): o.text in o.fg on o.bg with a frame (o.border), o.w (0.6) x o.h
  // (0.24); o.string: two cords up to a hook o.stringH (0.16) above; o.tape: four strips of tape at the corners; o.popAt: it pops in (outBack, 0.16 s);
  // o.swing [[t, amp]]: it swings from the hook; o.slap [t]: a quick squash (taped on); o.back: a plain back face
  styNotice(o) {
    const W = o.w ?? 0.6, H = o.h ?? 0.24, g = grp(), b = grp(); g.add(b); const sh = o.string ? (o.stringH ?? 0.16) : 0; const card = grp(); card.position.y = o.string ? -sh - H / 2 : 0; b.add(card);
    card.add(at(box(W + 0.03, H + 0.03, 0.012, o.border || '#1B2A4A', { outline: 0.02 }), 0, 0, -0.004));
    const pl = canvasPlane(W, H, (c, cw, ch) => { c.fillStyle = o.bg || '#F6F2E6'; c.fillRect(0, 0, cw, ch); c.strokeStyle = o.fg || '#C8202A'; c.lineWidth = ch * 0.05; c.strokeRect(ch * 0.08, ch * 0.08, cw - ch * 0.16, ch - ch * 0.16);
      c.fillStyle = o.fg || '#C8202A'; c.textAlign = 'center'; c.textBaseline = 'middle'; const lines = String(o.text || 'SUSPENDU').split('\n'); lines.forEach((s, i) => fitText(c, s, cw / 2, ch * (0.5 + (i - (lines.length - 1) / 2) * 0.38), cw * 0.84, ch * (lines.length > 1 ? 0.34 : 0.6))); }, { res: 512 });
    pl.position.z = 0.0035; card.add(pl);
    if (o.tape) for (const [sx, sy] of [[-1, 1], [1, 1], [-1, -1], [1, -1]]) card.add(at(box(0.09, 0.03, 0.004, '#EDE3B8'), sx * W / 2, sy * H / 2, 0.006, 0, 0, sx * sy * 0.6));
    if (o.string) { for (const sx of [-1, 1]) { const len = Math.hypot(W * 0.4, sh), r = new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, len, 4), lam('#2A2A2A')); r.position.set(sx * W * 0.2, -sh / 2, 0); r.rotation.z = sx * Math.atan2(W * 0.4, sh); b.add(r); }
      b.add(at(sphere(0.012, '#2A2A2A', 1), 0, 0, 0)); }
    g.scale.setScalar(o.popAt != null ? 0.001 : 1);
    g.userData.update = t => { const s = o.popAt != null ? (t < o.popAt ? 0.001 : Math.max(0.001, outBack((t - o.popAt) / 0.16))) : 1; let sq = 0; for (const ts of o.slap || []) { const u = t - ts; if (u >= 0 && u < 0.3) sq += Math.exp(-10 * u) * Math.sin(u * 40) * 0.12; }
      g.scale.set(s * (1 + sq), s * (1 - sq), s); b.rotation.z = swingAt(o.swing, t, 8, 2.4); };
    g.userData.update(0); return g;
  },

  // A hospital corridor wall (pivot at the floor under its middle, facing +Z): o.w (8) long, o.h (3) high, pale walls (o.wall) over a teal band, a
  // skirting, a floor strip (o.floor, 3 m deep, raised 5 cm); a double door at o.doorX (1.5 x 2.2) with two round windows and push plates, a plate
  // above it (o.plate 'MATERNITÉ'); a handrail along the wall; userData.door: the door's centre (local)
  styCorridor(o) {
    const W = o.w ?? 8, H = o.h ?? 3, g = grp(), dx = o.doorX ?? 0;
    g.add(at(box(W, H, 0.2, o.wall || '#EAF1EC', { pivot: 'bottom' }), 0, 0, -0.1), at(box(W, 1.0, 0.02, o.band || '#9CCBC0'), 0, 0.5, 0.01), at(box(W, 0.12, 0.04, '#5F8F86'), 0, 0.06, 0.02));
    const fl = at(box(W, 0.05, o.floorD ?? 4, o.floor || '#D6DDD8', { pivot: 'bottom' }), 0, 0, (o.floorD ?? 4) / 2); fl.castShadow = false; g.add(fl);
    for (let i = 0; i < 8; i++) g.add(at(box(0.02, 0.003, o.floorD ?? 4, '#C2CAC4'), -W / 2 + W * (i + 0.5) / 8, 0.052, (o.floorD ?? 4) / 2));
    g.add(at(box(W, 0.05, 0.06, '#C9D2CE', { outline: 0.004 }), 0, 0.9, 0.06));
    const dw = 1.5, dh = 2.2; g.add(at(box(dw + 0.16, dh + 0.08, 0.06, '#7E8E96', { pivot: 'bottom', outline: 0.004 }), dx, 0, 0.03));
    for (const sd of [-1, 1]) { const x = dx + sd * dw / 4; g.add(at(box(dw / 2 - 0.03, dh - 0.02, 0.05, o.door || '#DCE6EE', { pivot: 'bottom', outline: 0.004 }), x, 0.0, 0.07));
      const win = new THREE.Mesh(new THREE.CircleGeometry(0.16, 20), lam('#9FC9DE', { emissive: '#3A5A6A' })); win.position.set(x, 1.6, 0.1); g.add(win);
      const fr = new THREE.Mesh(new THREE.TorusGeometry(0.17, 0.02, 6, 20), lam('#7E8E96')); fr.position.set(x, 1.6, 0.1); g.add(fr);
      g.add(at(box(0.12, 0.3, 0.01, '#B9C2C8'), x - sd * 0.25, 1.05, 0.1)); }
    if (o.plate !== false) { const pw = 1.25, ph = 0.3, pl = canvasPlane(pw, ph, (c, cw, ch) => { c.fillStyle = '#2D6E9E'; c.fillRect(0, 0, cw, ch); c.fillStyle = '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, o.plate || 'MATERNITÉ', cw / 2, ch * 0.55, cw * 0.86, ch * 0.6); }, { res: 512 });
      g.add(at(pl, dx, dh + 0.32, 0.03)); }
    g.userData.door = [dx, 1.3, 0.1]; return g;
  },

  // The news studio (pivot at the floor under the desk's front; front +Z): a curved-front desk (o.desk navy) with a red stripe, behind it at z -1.7 a
  // big screen with a photo of the brass State pen on its chain (o.photo), a red ÉDITION SPÉCIALE banner above it (o.banner), a counter panel at
  // o.countX: JOURS SANS STYLO and a number word flipping from o.from (DIX) to o.to (ONZE) at o.flipAt; a tall paper stack on the desk at o.stackX that
  // topples toward +X at o.toppleAt, a few sheets sliding off; a dark blue studio wall; userData.desk: the top of the desk (local y)
  styStudio(o) {
    const g = grp(), DH = 0.95, bz = -1.75;
    g.add(at(box(9, 4.2, 0.2, o.wall || '#1D3557', { pivot: 'bottom' }), 0, 0, bz - 0.35));
    for (let i = 0; i < 7; i++) g.add(at(box(0.05, 4.2, 0.03, '#2B4A72', { pivot: 'bottom' }), -4.2 + i * 1.4, 0, bz - 0.24));
    const fl = at(box(9, 0.05, 6, '#2A2F3A', { pivot: 'bottom' }), 0, 0, 1.0); fl.castShadow = false; g.add(fl);
    const desk = grp(); g.add(desk);
    desk.add(at(box(2.3, DH - 0.06, 0.75, o.desk || '#24324A', { pivot: 'bottom', outline: 0.004 }), 0, 0, -0.4), at(box(2.4, 0.06, 0.85, '#E9EDF2', { pivot: 'bottom', outline: 0.004 }), 0, DH - 0.06, -0.42));
    desk.add(at(box(2.3, 0.1, 0.02, '#D3212B'), 0, DH * 0.62, -0.02));
    const sw = o.screenW ?? 2.6, shh = sw * 0.56, sy = o.screenY ?? 1.95;
    const photo = canvasPlane(sw, shh, (c, W, H) => { const gr = c.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#3E7CB8'); gr.addColorStop(1, '#173A63'); c.fillStyle = gr; c.fillRect(0, 0, W, H);
      c.save(); c.translate(W * 0.47, H * 0.52); c.rotate(-0.55); const L = W * 0.62, R = H * 0.07;
      c.fillStyle = '#2A1E0A'; c.fillRect(-L / 2 - 6, -R - 6, L + 12, 2 * R + 12);
      c.fillStyle = '#D4A93C'; c.fillRect(-L * 0.28, -R, L * 0.62, 2 * R); c.fillStyle = '#1C1D22'; c.fillRect(-L * 0.42, -R * 0.92, L * 0.14, 2 * R * 0.92);
      c.fillStyle = '#9C7424'; c.beginPath(); c.moveTo(-L * 0.42, -R * 0.9); c.lineTo(-L * 0.52, 0); c.lineTo(-L * 0.42, R * 0.9); c.fill();
      c.fillStyle = '#C99A30'; c.fillRect(L * 0.34, -R * 1.06, L * 0.15, 2 * R * 1.06); c.fillStyle = '#F0D78A'; c.fillRect(L * 0.34, -R * 1.5, L * 0.13, R * 0.36); c.fillRect(-L * 0.25, -R * 0.55, L * 0.55, R * 0.2);
      c.strokeStyle = '#8D959E'; c.lineWidth = R * 0.35; for (let i = 0; i < 6; i++) { c.beginPath(); c.ellipse(L * 0.55 + i * R * 1.1, 0, R * 0.62, R * 0.38, 0, 0, TAU); c.stroke(); } c.restore();
      c.fillStyle = '#F6F0DC'; c.fillRect(W * 0.8, H * 0.12, W * 0.14, H * 0.13); c.fillStyle = '#1B2A4A'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, 'ÉTAT', W * 0.87, H * 0.19, W * 0.12, H * 0.09);
      c.fillStyle = 'rgba(255,255,255,0.9)'; fitText(c, 'RECHERCHÉ', W * 0.5, H * 0.9, W * 0.7, H * 0.12); }, { res: 1024, emissive: 0.55 });
    g.add(at(box(sw + 0.12, shh + 0.12, 0.08, '#101317', { outline: 0.004 }), 0, sy, bz), at(photo, 0, sy, bz + 0.045));
    if (o.banner !== false) { const bw = o.bannerW ?? 2.9, bh = 0.42, bn = canvasPlane(bw, bh, (c, W, H) => { c.fillStyle = '#D3212B'; c.fillRect(0, 0, W, H); c.fillStyle = '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, o.banner || 'ÉDITION SPÉCIALE', W / 2, H * 0.55, W * 0.9, H * 0.66); }, { res: 1024, emissive: 0.4 });
      g.add(at(box(bw + 0.06, bh + 0.06, 0.04, '#7A0E14'), o.bannerX ?? 0, sy + shh / 2 + 0.36, bz + 0.02), at(bn, o.bannerX ?? 0, sy + shh / 2 + 0.36, bz + 0.05)); }
    const cx = o.countX ?? 1.05, cyy = o.countY ?? (DH + 0.42), cw = 0.62, chh = 0.5, cnt = grp(); cnt.position.set(cx, cyy, o.countZ ?? -0.55); g.add(cnt);
    cnt.add(at(box(cw + 0.06, chh + 0.06, 0.08, '#14171C', { outline: 0.004 }), 0, 0, -0.04), at(box(0.06, cyy - DH, 0.06, '#14171C', { pivot: 'top' }), 0, -chh / 2, -0.04));
    const head = canvasPlane(cw, chh * 0.3, (c, W, H) => { c.fillStyle = '#F6F0DC'; c.fillRect(0, 0, W, H); c.fillStyle = '#1B2A4A'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, o.head || 'JOURS SANS STYLO', W / 2, H * 0.55, W * 0.9, H * 0.6); }, { res: 512 });
    head.position.set(0, chh * 0.35, 0.002); cnt.add(head);
    const num = s => canvasPlane(cw, chh * 0.66, (c, W, H) => { c.fillStyle = '#1A1C20'; c.fillRect(0, 0, W, H); c.fillStyle = '#FFD23A'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, s, W / 2, H * 0.55, W * 0.86, H * 0.62); c.fillStyle = 'rgba(0,0,0,0.6)'; c.fillRect(0, H / 2 - 2, W, 4); }, { res: 512, emissive: 0.5 });
    const nA = num(o.from || 'DIX'), nB = num(o.to || 'ONZE'); nA.position.set(0, -chh * 0.16, 0.003); nB.position.set(0, -chh * 0.16, 0.004); cnt.add(nA, nB);
    const flap = num(o.from || 'DIX'); const flapP = grp(flap); flap.position.y = -chh * 0.33 / 2; flap.scale.y = 0.5; flapP.position.set(0, -chh * 0.16 + chh * 0.33 / 2 - chh * 0.33 / 2 + chh * 0.0, 0.006); cnt.add(flapP);
    const stack = grp(), sx = o.stackX ?? -0.7, sz = -0.35, nS = 26; stack.position.set(sx + 0.13, DH, sz); g.add(stack);
    for (let i = 0; i < nS; i++) stack.add(at(box(0.26, 0.017, 0.34, i % 5 === 4 ? '#E8D7A2' : '#FBF8F0', { outline: 0.02 }), -0.13 + (hsh(i) - 0.5) * 0.03, 0.0085 + i * 0.018, (hsh(i + 9) - 0.5) * 0.03, 0, (hsh(i + 4) - 0.5) * 0.2, 0));
    const fly = []; for (let i = 0; i < 4; i++) { const s = at(box(0.24, 0.004, 0.32, '#FBF8F0', { outline: 0.03 }), 0, 0, 0); s.visible = false; g.add(s); fly.push(s); }
    g.userData.desk = DH;
    g.userData.update = t => { const f = o.flipAt ?? 0.5, u = (t - f) / 0.16;
      nA.visible = u < 0; nB.visible = u >= 0; flapP.visible = u >= 0 && u < 1; if (flapP.visible) { flapP.rotation.x = -PI * u; }
      const tp = o.toppleAt ?? 99, v = t - tp; let a = 0; if (v > 0) { a = Math.min(1.45, 1.45 * Math.pow(v / 0.3, 2)); if (v > 0.3) a = 1.45 + 0.08 * Math.exp(-8 * (v - 0.3)) * Math.sin((v - 0.3) * 30); } stack.rotation.z = -a;
      fly.forEach((s, i) => { s.visible = v > 0.18 && v < 2.2; if (!s.visible) return; const w = v - 0.18; s.position.set(sx + 0.4 + w * (0.7 + 0.3 * i), DH + 0.35 + 0.8 * w - 2.4 * w * w + 0.1 * i, sz + 0.1 * i - 0.1); if (s.position.y < 0.06) s.position.y = 0.06; s.rotation.set(w * (2 + i), w * (1 + 0.5 * i), w * 3); }); };
    g.userData.update(0); return g;
  },

  // A resignation letter (pivot at its middle, front +Z): a white sheet o.w (0.42) x o.h (0.56) with a thin dark edge, DÉMISSION in big red capitals,
  // a few lines of text marks and, at the bottom, SIGNATURE : and an empty dotted line (there is nothing to sign with)
  styLetter(o) {
    const W = o.w ?? 0.42, H = o.h ?? 0.56, g = grp();
    g.add(at(box(W + 0.014, H + 0.014, 0.004, '#2A2D33'), 0, 0, -0.003));
    const p = canvasPlane(W, H, (c, cw, ch) => { c.fillStyle = '#FBF9F2'; c.fillRect(0, 0, cw, ch); c.fillStyle = '#B5141C'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, o.title || 'DÉMISSION', cw / 2, ch * 0.14, cw * 0.86, ch * 0.13);
      c.strokeStyle = '#7C8590'; c.lineWidth = ch * 0.012; for (let i = 0; i < 6; i++) { const y = ch * (0.32 + i * 0.075); c.beginPath(); c.moveTo(cw * 0.1, y); c.lineTo(cw * (0.9 - 0.25 * (i === 5)), y); c.stroke(); }
      c.fillStyle = '#1B2A4A'; c.textAlign = 'left'; fitText(c, 'SIGNATURE :', cw * 0.1, ch * 0.86, cw * 0.4, ch * 0.05); c.setLineDash([cw * 0.02, cw * 0.02]); c.beginPath(); c.moveTo(cw * 0.52, ch * 0.88); c.lineTo(cw * 0.9, ch * 0.88); c.stroke(); }, { res: 512 });
    p.position.z = 0.0015; g.add(p);
    const back = new THREE.Mesh(new THREE.PlaneGeometry(W, H), lam('#F2EFE6', { side: THREE.BackSide })); back.position.z = 0.001; g.add(back);
    return g;
  },

  // An official sash in invented colours (pivot at its middle, front +Z): a band o.w (0.15) x o.len (0.9) in three stripes (o.colors: violet, gold,
  // violet by default: no real flag), a gold rosette at o.rose (0.25 from the top) and a gold fringe at the bottom; o.drop [[t, y], ...]: a keyed height
  // offset (it is lowered over a head)
  stySash(o) {
    const W = o.w ?? 0.15, L = o.len ?? 0.9, cols = o.colors || ['#5B2C83', '#E8B820', '#5B2C83'], g = grp(), b = grp(); g.add(b);
    cols.forEach((c, i) => b.add(at(box(W / cols.length, L, 0.012, c, { outline: i === 1 ? 0 : 0.01 }), (i - (cols.length - 1) / 2) * W / cols.length, 0, 0)));
    b.add(at(cyl(0.05, 0.05, 0.02, '#E8B820', 10, { outline: 0.02 }), 0, L / 2 - (o.rose ?? 0.25), 0.012, PI / 2, 0, 0));
    for (let j = 0; j < 7; j++) b.add(at(box(0.008, 0.07, 0.008, '#C9A23E'), (j - 3) * W / 7, -L / 2 - 0.035, 0.004));
    if (o.drop) g.userData.update = t => { b.position.y = linAt(o.drop, t, 0); };
    return g;
  },

  // A cardboard cut-out of the brass pen (pivot at the floor; front +Z): a flat brass pen o.h (1.25) tall on a brown cardboard board, its chain and a
  // printed ÉTAT tag, a strut behind; o.s scales it
  styCutout(o) {
    const Hh = o.h ?? 1.25, g = grp(), b = grp(); g.add(b); if (o.s) b.scale.setScalar(o.s);
    const kraft = '#A07848', y0 = 0.08;
    const pen = [[0, 0.12, 0.08, '#9C7424', 'tip'], [0.12, 0.2, 0.17, '#1C1D22'], [0.2, 0.74, 0.18, BRASS], [0.74, 0.76, 0.2, '#F0D78A'], [0.76, 0.98, 0.2, '#C99A30']];
    for (const [a, c_, w, col, kind] of pen) { const h = (c_ - a) * Hh, y = y0 + a * Hh + h / 2;
      if (kind === 'tip') { const sh = new THREE.Shape([new THREE.Vector2(0, -h / 2), new THREE.Vector2(w * Hh / 2, h / 2), new THREE.Vector2(-w * Hh / 2, h / 2)]); const m = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: 0.02, bevelEnabled: false }), mat(col)); m.position.set(0, y, -0.01); b.add(m);
        const k = new THREE.Mesh(new THREE.ExtrudeGeometry(new THREE.Shape([new THREE.Vector2(0, -h / 2 - 0.03), new THREE.Vector2(w * Hh / 2 + 0.03, h / 2 + 0.01), new THREE.Vector2(-w * Hh / 2 - 0.03, h / 2 + 0.01)]), { depth: 0.012, bevelEnabled: false }), mat(kraft)); k.position.set(0, y, -0.024); b.add(k); }
      else { b.add(at(box(w * Hh, h, 0.02, col), 0, y, 0), at(box(w * Hh + 0.06, h + 0.02, 0.012, kraft), 0, y, -0.016)); } }
    b.add(at(box(0.05 * Hh, 0.2 * Hh, 0.022, '#F0D78A', { outline: 0.02 }), 0, y0 + 0.86 * Hh, 0.006));
    b.add(at(box(0.08 * Hh, 0.04 * Hh, 0.02, '#C99A30'), 0, y0 + 1.0 * Hh, 0), at(box(0.12 * Hh, 0.07 * Hh, 0.012, kraft), 0, y0 + 1.0 * Hh, -0.016));
    const tag = canvasPlane(0.3, 0.19, (c, W, H) => { c.fillStyle = '#F6F0DC'; c.fillRect(0, 0, W, H); c.strokeStyle = '#1B2A4A'; c.lineWidth = H * 0.06; c.strokeRect(H * 0.06, H * 0.06, W - H * 0.12, H - H * 0.12); c.fillStyle = '#1B2A4A'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, 'ÉTAT', W / 2, H * 0.55, W * 0.8, H * 0.6); }, { res: 256 });
    b.add(at(box(0.33, 0.22, 0.012, BRASS, { outline: 0.02 }), 0.26, y0 + 0.86 * Hh, 0.01), at(tag, 0.26, y0 + 0.86 * Hh, 0.018), at(box(0.38, 0.27, 0.01, kraft), 0.26, y0 + 0.86 * Hh, -0.005));
    for (let i = 0; i < 4; i++) b.add(at(box(0.05, 0.03, 0.012, '#6A7078'), 0.06 + i * 0.045, y0 + 1.02 * Hh - i * 0.04, 0.012, 0, 0, -0.7));
    const st = at(box(0.06, Hh * 0.8, 0.02, kraft), 0, Hh * 0.38, -0.2); st.rotation.x = 0.28; b.add(st);
    return g;
  },

  // A breast pocket patch (attach to the torso joint, pivot at its middle, front +Z): a flat pocket o.w (0.2) x o.h (0.13) in the suit's colour (o.color)
  // with a darker top seam and an outline: the pens clipped in it go down behind it
  styPocket(o) {
    const W = o.w ?? 0.2, H = o.h ?? 0.13, g = grp(), c = new THREE.Color(o.color || '#1F3550');
    g.add(at(box(W, H, 0.012, '#' + c.getHexString(), { outline: 0.04 }), 0, 0, 0), at(box(W, 0.016, 0.014, '#' + c.clone().multiplyScalar(0.65).getHexString()), 0, H / 2 - 0.008, 0.001));
    return g;
  },

  // (round 1) A striped pyjama top front (attach to the torso joint, offset [0, 0, 0]): a panel o.w (0.38) wide with vertical stripes (o.color, o.stripe),
  // a round collar band, piped placket with three buttons; hides the suit lapels of the pyjama outfit
  styPyjTop(o) {
    const W = o.w ?? 0.38, Hp = o.h ?? 0.52, Z = o.z ?? 0.172, y0 = o.y0 ?? 0.1, g = grp();
    const p = canvasPlane(W, Hp, (c, cw, ch) => { c.fillStyle = o.color || '#9DB7D9'; c.fillRect(0, 0, cw, ch); c.fillStyle = o.stripe || '#F4F6FA'; const n = 7; for (let i = 0; i < n; i++) c.fillRect(cw * (i + 0.3) / n, 0, cw * 0.32 / n, ch);
      c.fillStyle = o.pipe || '#2E4A7A'; c.fillRect(cw * 0.48, 0, cw * 0.04, ch); for (let i = 0; i < 3; i++) { c.beginPath(); c.arc(cw * 0.5, ch * (0.25 + i * 0.25), cw * 0.025, 0, TAU); c.fill(); } }, { res: 256 });
    p.position.set(0, y0 + Hp / 2, Z + 0.012); g.add(p, at(box(W + 0.01, Hp, 0.01, o.color || '#9DB7D9', { outline: 0.01 }), 0, y0 + Hp / 2, Z + 0.004));
    g.add(at(cyl(0.12, 0.125, 0.05, o.pipe || '#2E4A7A', 12, { outline: 0.004 }), 0, y0 + Hp + 0.01, 0.0));
    return g;
  },

  // A small school pencil (pivot at its middle, the point down -Y): a yellow hexagonal body o.len (0.16) long, a sharpened wooden tip with a graphite
  // point, a metal ferrule and a pink eraser; a dark hull so it reads against a pale ground
  styPencil(o) {
    const L = o.len ?? 0.16, R = 0.008, g = grp(), rc = o.rim ?? '#2A2410', rw = 0.003;
    const body = rimmed(cylR(R, R, L * 0.78, 6), lam(o.color || '#F2C230'), rc, rw); body.position.y = L * 0.03; g.add(body);
    const tip = rimmed(w => new THREE.ConeGeometry(R + w, L * 0.14 + 2 * w, 6), lam('#E8C9A0'), rc, rw); tip.position.y = -L * 0.43; tip.rotation.x = PI; g.add(tip);
    g.add(at(new THREE.Mesh(new THREE.ConeGeometry(R * 0.35, L * 0.05, 6), lam('#2A2A2A')), 0, -L * 0.49, 0, PI, 0, 0));
    g.add(at(cyl(R * 1.05, R * 1.05, L * 0.05, '#B9BEC6', 8), 0, L * 0.44, 0), at(cyl(R, R, L * 0.06, '#F28CA0', 8), 0, L * 0.49, 0));
    if (o.s) g.scale.setScalar(o.s); return g;
  },

  // A folding table at a school gate with the pencil cases being searched (pivot at the floor; front +Z): a grey top o.w (1.6) x 0.7 at 0.74 on crossed
  // legs, o.n (4) open zip pencil cases in bright colours, small pencils, an eraser and a sharpener spilled out; userData.top
  styPencilTable(o) {
    const W = o.w ?? 1.6, D = 0.7, Ht = 0.74, g = grp();
    g.add(at(box(W, 0.04, D, '#C9CED4', { outline: 0.005 }), 0, Ht - 0.02, 0));
    for (const sx of [-1, 1]) for (const sd of [-1, 1]) { const l = at(box(0.03, Ht * 1.08, 0.03, '#6A7078'), sx * (W / 2 - 0.15), Ht / 2, 0); l.rotation.x = sd * 0.42; g.add(l); }
    const cols = ['#E8463C', '#2E8BC0', '#F2B630', '#4FAE5A', '#9B59B6', '#F07EA8'];
    for (let i = 0; i < (o.n ?? 4); i++) { const x = -W / 2 + 0.25 + i * (W - 0.5) / Math.max(1, (o.n ?? 4) - 1), z = (hsh(i) - 0.5) * 0.2, c = cols[i % cols.length], pc = grp(); pc.position.set(x, Ht, z); pc.rotation.y = (hsh(i + 3) - 0.5) * 0.6; g.add(pc);
      pc.add(at(box(0.24, 0.05, 0.1, c, { outline: 0.02 }), 0, 0.025, 0), at(box(0.24, 0.012, 0.012, '#2A2A2A'), 0, 0.052, 0.0));
      const flap = at(box(0.24, 0.006, 0.09, c, { outline: 0.03 }), 0, 0.054, -0.07); flap.rotation.x = -0.9; pc.add(flap); }
    for (let i = 0; i < (o.pencils ?? 14); i++) { const p = grp(at(cyl(0.007, 0.007, 0.16, cols[(i + 2) % cols.length], 6), 0, 0, 0), at(new THREE.Mesh(new THREE.ConeGeometry(0.007, 0.022, 6), mat('#E8C9A0')), 0, -0.091, 0, PI, 0, 0));
      p.position.set((hsh(i * 3) - 0.5) * (W - 0.2), Ht + 0.008, (hsh(i * 7) - 0.5) * 0.5 + 0.05); p.rotation.set(PI / 2, 0, hsh(i * 5) * TAU); g.add(p); }
    g.add(at(box(0.05, 0.02, 0.03, '#F4B8C0', { outline: 0.03 }), 0.3, Ht + 0.01, 0.2), at(box(0.035, 0.025, 0.025, '#3A7BD5', { outline: 0.03 }), -0.35, Ht + 0.012, 0.22));
    g.userData.top = Ht; return g;
  },

  // A framed photo (pivot at its middle, front +Z): a dark wooden frame o.w (0.36) x o.h (0.46), a cream mat and, behind glass, the box-headed hero
  // in his navy suit and red tie, deadpan, with the brass pen standing out of his breast pocket (o.pen false: no pen); o.stand: a strut behind
  styPhoto(o) {
    const W = o.w ?? 0.36, H = o.h ?? 0.46, g = grp();
    g.add(at(box(W + 0.05, H + 0.05, 0.03, o.frame || '#5A3A22', { outline: 0.01 }), 0, 0, -0.015));
    const p = canvasPlane(W, H, (c, cw, ch) => { c.fillStyle = '#F2EBDA'; c.fillRect(0, 0, cw, ch); c.fillStyle = '#BFD6E6'; c.fillRect(cw * 0.08, ch * 0.06, cw * 0.84, ch * 0.88);
      const cx = cw / 2; c.fillStyle = '#1F2D4D'; c.beginPath(); c.moveTo(cx - cw * 0.36, ch * 0.94); c.lineTo(cx - cw * 0.3, ch * 0.62); c.lineTo(cx + cw * 0.3, ch * 0.62); c.lineTo(cx + cw * 0.36, ch * 0.94); c.fill();
      c.fillStyle = '#FFFFFF'; c.beginPath(); c.moveTo(cx - cw * 0.08, ch * 0.62); c.lineTo(cx, ch * 0.78); c.lineTo(cx + cw * 0.08, ch * 0.62); c.fill(); c.fillStyle = '#C8202A'; c.fillRect(cx - cw * 0.025, ch * 0.64, cw * 0.05, ch * 0.2);
      c.fillStyle = '#E2B48E'; c.fillRect(cx - cw * 0.22, ch * 0.2, cw * 0.44, ch * 0.42); c.fillStyle = '#3A2A20'; c.fillRect(cx - cw * 0.23, ch * 0.17, cw * 0.46, ch * 0.07);
      c.fillStyle = 'rgba(60,40,30,0.25)'; c.fillRect(cx - cw * 0.2, ch * 0.48, cw * 0.4, ch * 0.12); c.fillStyle = '#1A1A1A'; c.fillRect(cx - cw * 0.12, ch * 0.33, cw * 0.05, ch * 0.05); c.fillRect(cx + cw * 0.07, ch * 0.33, cw * 0.05, ch * 0.05);
      c.fillRect(cx - cw * 0.14, ch * 0.29, cw * 0.09, ch * 0.012); c.fillRect(cx + cw * 0.05, ch * 0.29, cw * 0.09, ch * 0.012); c.fillRect(cx - cw * 0.07, ch * 0.52, cw * 0.14, ch * 0.012);
      if (o.pen !== false) { c.fillStyle = '#2A1E0A'; c.fillRect(cx + cw * 0.12, ch * 0.5, cw * 0.075, ch * 0.24); c.fillStyle = '#E8B830'; c.fillRect(cx + cw * 0.13, ch * 0.51, cw * 0.055, ch * 0.22); c.fillStyle = '#FFF0A0'; c.fillRect(cx + cw * 0.14, ch * 0.52, cw * 0.012, ch * 0.18);
        c.fillStyle = '#C8202A'; c.fillRect(cx + cw * 0.215, ch * 0.56, cw * 0.04, ch * 0.16); }
      c.fillStyle = '#2E4058'; c.fillRect(cx + cw * 0.1, ch * 0.7, cw * 0.17, ch * 0.03); }, { res: 512 });
    p.position.z = 0.002; g.add(p);
    const gl = new THREE.Mesh(new THREE.PlaneGeometry(W * 0.8, H * 0.12), basic('#FFFFFF', { transparent: true, opacity: 0.18, depthWrite: false })); gl.position.set(-W * 0.12, H * 0.25, 0.004); gl.rotation.z = 0.6; g.add(gl);
    if (o.stand) { const s = at(box(0.04, H * 0.8, 0.012, o.frame || '#5A3A22'), 0, -H * 0.1, -0.12); s.rotation.x = -0.35; g.add(s); }
    return g;
  },

  // THE BLOCK OF FLATS AT NIGHT (pivot at the foot of the facade's middle; front +Z): o.floors (6) storeys of o.storey (2.9) in a stone facade o.w (10)
  // wide, windows on o.cols x positions (lit by a hash, o.litHero the hero's French window), a pale pavement 5 cm high (o.pave, 4 m deep) and a dark road;
  // balconies at x = o.bx on the floors o.balc ([2, 3, 4, 5]): stone slabs 2.2 x 1.1 with iron rails; o.slabs {floor: [[t, y], ...]} keyed heights of a
  // slab's top (it falls), o.land {floor: t}: its rail crumples, o.crackAt / o.breakAt: the top slab shakes and cracks show on the wall; a scar where a
  // fallen balcony was; o.dustAt: a grey dust cloud from the pavement; userData.slabTop(fl): the slab's resting top y
  styBlock(o) {
    const W = o.w ?? 10, NF = o.floors ?? 6, S = o.storey ?? 2.9, g = grp(), Hf = NF * S + 0.6, wallC = o.color || '#B9A88E';
    g.add(at(box(W, Hf, 0.5, wallC, { pivot: 'bottom', outline: 0.002 }), 0, 0, -0.25));
    for (let f = 1; f < NF; f++) g.add(at(box(W, 0.1, 0.06, '#A4937A'), 0, f * S, 0.03));
    g.add(at(box(W + 0.3, 0.25, 0.4, '#8E7E66'), 0, Hf, -0.1));
    const pave = at(box(W + 8, 0.05, o.pave ?? 4, o.paveColor || '#8C8F94', { pivot: 'bottom' }), 0, 0, (o.pave ?? 4) / 2); pave.castShadow = false; g.add(pave);
    const road = at(box(W + 8, 0.03, 12, '#2C2F36', { pivot: 'bottom' }), 0, 0, (o.pave ?? 4) + 6); road.castShadow = false; g.add(road);
    g.add(at(box(W + 8, 0.14, 0.2, '#6E7178', { pivot: 'bottom' }), 0, 0, (o.pave ?? 4)));
    const cols = o.cols || [-3.6, -1.9, 0, 1.9, 3.6], bx = o.bx ?? 0;
    for (let f = 0; f < NF; f++) for (const [ci, x] of cols.entries()) {
      const isB = x === bx && (o.balc || [2, 3, 4, 5]).includes(f), y0 = f * S, lit = (o.lit || []).some(([ff, xx]) => ff === f && xx === x) || (!isB && hsh(f * 7 + ci * 3) > 0.62) || (isB && f === (o.heroFloor ?? 5) && o.litHero !== false);
      if (f === 0 && x === bx) { g.add(at(box(1.3, 2.3, 0.06, '#3A2E26', { pivot: 'bottom', outline: 0.004 }), x, 0.05, 0.02)); continue; }
      const ww = isB ? 1.0 : 0.95, wh = isB ? 2.1 : 1.35, wy = isB ? y0 + 0.05 + wh / 2 : y0 + 1.0 + wh / 2;
      const glass = new THREE.Mesh(new THREE.PlaneGeometry(ww, wh), lit ? lam('#FFD98A', { emissive: '#E8A848' }) : lam('#26334A', { emissive: '#0E1626' })); glass.position.set(x, wy, 0.012); g.add(glass);
      for (const [dx, dy, bw, bh] of [[0, wh / 2, ww + 0.1, 0.07], [0, -wh / 2, ww + 0.14, 0.08], [-ww / 2, 0, 0.07, wh], [ww / 2, 0, 0.07, wh], [0, 0, 0.04, wh]]) g.add(at(box(bw, bh, 0.05, '#E6DCC8'), x + dx, wy + dy, 0.03));
      if (!isB) for (const sd of [-1, 1]) g.add(at(box(0.32, wh, 0.03, o.shutter || '#4E6E8A', { outline: 0.004 }), x + sd * (ww / 2 + 0.18), wy, 0.03)); }
    const slabs = {}, crackG = grp(); g.add(crackG); crackG.visible = false;
    for (const f of o.balc || [2, 3, 4, 5]) { const sb = grp(), wB = 2.2, dB = 1.1; sb.add(at(box(wB, 0.22, dB, '#C7BBA6', { outline: 0.004 }), 0, -0.11, dB / 2), at(box(wB + 0.06, 0.06, dB + 0.03, '#AFA28A'), 0, -0.25, dB / 2 + 0.015));
      const rail = grp(); sb.add(rail); const iron = '#1E2228';
      rail.add(at(box(wB, 0.05, 0.05, iron), 0, 1.0, dB - 0.03), at(box(0.05, 0.05, dB, iron), -wB / 2 + 0.03, 1.0, dB / 2), at(box(0.05, 0.05, dB, iron), wB / 2 - 0.03, 1.0, dB / 2));
      for (let x = -wB / 2 + 0.05; x <= wB / 2 - 0.04; x += 0.14) rail.add(at(box(0.022, 1.0, 0.022, iron), x, 0.5, dB - 0.03));
      for (let z = 0.12; z < dB - 0.05; z += 0.14) for (const sd of [-1, 1]) rail.add(at(box(0.022, 1.0, 0.022, iron), sd * (wB / 2 - 0.03), 0.5, z));
      sb.position.set(bx, f * S, 0); g.add(sb);
      const scar = at(box(wB, 0.26, 0.02, '#6E6252'), bx, f * S - 0.12, 0.012); scar.visible = false; g.add(scar);
      slabs[f] = { sb, rail, scar, y0: f * S }; }
    for (let i = 0; i < 7; i++) { const a = -0.6 + i * 0.2, L = 0.4 + 0.5 * hsh(i); const c = at(box(L, 0.03, 0.01, '#3A3026'), bx + Math.sin(a) * 0.9, (o.heroFloor ?? 5) * S - 0.1 - Math.cos(a) * 0.3 * hsh(i + 2), 0.02); c.rotation.z = a * 2; crackG.add(c); }
    const dust = [], dm = []; for (let i = 0; i < 9; i++) { const m = new THREE.Sprite(new THREE.SpriteMaterial({ map: softTex(), color: '#A8A49C', transparent: true, opacity: 0, depthWrite: false })); g.add(m); dust.push(m); }
    void dm;
    const puffs = []; for (const [t0, y0] of o.puffs || []) for (let i = 0; i < 8; i++) { const m = new THREE.Sprite(new THREE.SpriteMaterial({ map: softTex(), color: o.puffColor || '#CFC8BA', transparent: true, opacity: 0, depthWrite: false })); g.add(m); puffs.push({ m, t0, y0, a: i / 8 * TAU + 0.3 * hsh(i + t0 * 10) }); }
    g.userData.slabTop = f => f * S;
    g.userData.update = t => {
      for (const [f, s] of Object.entries(slabs)) { const ks = (o.slabs || {})[f]; const y = ks ? linAt(ks, t, s.y0) : s.y0; let jx = 0;
        if (+f === (o.heroFloor ?? 5) && o.crackAt != null && t >= o.crackAt && t < (o.breakAt ?? o.crackAt + 0.2)) jx = 0.02 * Math.sin(t * 90);
        const jt = (o.stackJit || {})[f] || [0, 0, 0], kz = (o.slabZ || {})[f] ?? 0; s.sb.position.set(bx + jx + jt[0], y, kz + jt[1]); s.sb.rotation.y = jt[2]; s.scar.visible = y < s.y0 - 0.3;
        const tl = (o.land || {})[f]; const crum = tl != null && t >= tl ? Math.min(1, (t - tl) / 0.08) : 0; s.rail.scale.set(1 + 0.06 * crum, 1 - 0.78 * crum, 1); s.rail.rotation.x = -0.35 * crum; s.rail.rotation.z = 0.12 * crum * (+f % 2 ? 1 : -1); }
      puffs.forEach(({ m, t0, y0, a }) => { const u = t - t0; if (u < 0 || u > 0.9) { m.material.opacity = 0; return; } m.position.set(bx + Math.cos(a) * (1.1 + 1.6 * u), y0 + 0.15 + 0.3 * u, 0.6 + Math.sin(a) * (0.5 + 0.6 * u)); m.scale.setScalar(0.5 + 1.8 * u); m.material.opacity = 0.7 * (1 - u / 0.9); });
      crackG.visible = o.crackAt != null && t >= o.crackAt;
      const da = o.dustAt; dust.forEach((m, i) => { if (da == null || t < da) { m.material.opacity = 0; return; } const u = t - da, a = (i / dust.length) * TAU; m.position.set(bx + Math.cos(a) * (0.6 + 1.6 * u) * 1.3, 0.3 + 0.5 * u + 0.25 * hsh(i), 0.6 + Math.sin(a) * (0.4 + 0.9 * u));
        m.scale.setScalar(0.8 + 2.0 * u); m.material.opacity = (o.dustOp ?? 0.6) * Math.max(0, 1 - u / 1.6); }); };
    g.userData.update(0); return g;
  },

  // The prison visiting booth (pivot at the floor under the glass; the inmate's side, where the camera stands, is +Z; the visitor sits at -Z): a glass
  // partition in a dark frame from a ledge at 0.8 m to 2.1 m (glass with two pale streaks), ledges on both sides, side partitions, a pale green
  // visitor's wall at z -1.7 with a wall calendar showing o.day ('JEUDI') at o.calX, a wall phone box on the visitor's side; on the near side a
  // little stool at o.stool [x, z] with the red pen lying on it (built in), its chain running to a ring on the side partition
  styBooth(o) {
    const g = grp(), W = o.w ?? 1.9, y0 = 0.8, y1 = 2.15, frame = '#2C3138';
    const fl = at(box(6, 0.05, 6, '#B4B9B3', { pivot: 'bottom' }), 0, 0, 0); fl.castShadow = false; g.add(fl);
    g.add(at(box(6, 3.2, 0.2, o.wall || '#CFE0D2', { pivot: 'bottom' }), 0, 0, -1.8), at(box(6, 1.0, 0.03, o.band || '#9DB8A2'), 0, 0.5, -1.69));
    g.add(at(box(W, y0, 0.24, '#9AA2A8', { pivot: 'bottom', outline: 0.004 }), 0, 0, 0), at(box(W + 0.1, 0.05, 0.9, '#7E868C', { pivot: 'bottom', outline: 0.004 }), 0, y0, 0));
    const gl = new THREE.Mesh(new THREE.PlaneGeometry(W, y1 - y0), glassMat(0.1, '#D8ECF0')); gl.position.set(0, (y0 + y1) / 2, 0); g.add(gl);
    for (const [x, w, rz] of [[-0.35, 0.06, 0.6], [-0.2, 0.025, 0.6], [0.5, 0.04, 0.6]]) { const s = new THREE.Mesh(new THREE.PlaneGeometry(w, 0.9), basic('#FFFFFF', { transparent: true, opacity: 0.22, depthWrite: false })); s.position.set(x, 1.55, 0.01); s.rotation.z = rz; g.add(s); }
    for (const [x, y, w, h] of [[0, y1, W + 0.12, 0.08], [0, y0 + 0.06, W + 0.12, 0.06], [-W / 2, (y0 + y1) / 2, 0.08, y1 - y0], [W / 2, (y0 + y1) / 2, 0.08, y1 - y0]]) g.add(at(box(w, h, 0.1, frame, { outline: 0.004 }), x, y, 0));
    for (const sd of [-1, 1]) g.add(at(box(0.08, 2.3, 1.9, '#C2C9C4', { pivot: 'bottom', outline: 0.004 }), sd * (W / 2 + 0.04), 0, -0.85), at(box(0.08, 1.6, 0.9, '#C2C9C4', { pivot: 'bottom', outline: 0.004 }), sd * (W / 2 + 0.04), 0, 0.45));
    g.add(at(box(0.18, 0.28, 0.1, '#3A3F46', { outline: 0.006 }), W / 2 - 0.2, 1.45, -0.12), at(box(0.12, 0.03, 0.04, '#6A7078'), W / 2 - 0.2, 1.62, -0.07));
    if (o.day !== false) { const cw = 0.5, chh = 0.62, cx = o.calX ?? -0.55, cy = o.calY ?? 1.95, cal = canvasPlane(cw, chh, (c, Wc, Hc) => { c.fillStyle = '#FBF8F0'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#C8202A'; c.fillRect(0, 0, Wc, Hc * 0.24);
        c.fillStyle = '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, o.month || 'NOVEMBRE', Wc / 2, Hc * 0.13, Wc * 0.84, Hc * 0.13); c.fillStyle = '#1B2A4A'; fitText(c, o.day || 'JEUDI', Wc / 2, Hc * 0.6, Wc * 0.86, Hc * 0.3);
        c.fillStyle = '#9AA2A8'; for (let i = 0; i < 2; i++) c.fillRect(Wc * 0.2, Hc * (0.82 + i * 0.07), Wc * 0.6, Hc * 0.02); }, { res: 512 });
      g.add(at(box(cw + 0.04, chh + 0.04, 0.02, '#8C949A', { outline: 0.01 }), cx, cy, -1.69), at(cal, cx, cy, -1.675));
      for (const x of [-0.12, 0.12]) g.add(at(cyl(0.012, 0.012, 0.05, '#3A3D44', 6), cx + x, cy + chh / 2 + 0.01, -1.66)); }
    const [sx, sz] = o.stool || [0.35, 0.75], sh = o.stoolH ?? 0.62;
    g.add(at(cyl(0.2, 0.2, 0.05, o.stoolColor || '#7A4A2A', 14, { outline: 0.008 }), sx, sh, sz));
    for (let i = 0; i < 3; i++) { const a = i / 3 * TAU + 0.3, l = at(cyl(0.018, 0.018, sh, '#3A3D44', 6, { pivot: 'bottom' }), sx + Math.cos(a) * 0.13, 0, sz + Math.sin(a) * 0.13); l.rotation.set(Math.sin(a) * 0.12, 0, -Math.cos(a) * 0.12); g.add(l); }
    if (o.pen !== false) { const rs = sx < 0 ? -1 : 1, yw = (o.penYaw ?? 0.35) + (rs > 0 ? PI : 0), Lp = o.penLen ?? 0.46;
      const pen = buildProp('styPen', { kind: 'red', len: Lp }); pen.position.set(sx, sh + 0.05, sz); pen.rotation.set(0, yw, PI / 2); g.add(pen);
      const ring = [rs * (W / 2 - 0.01), 1.05, 0.3]; g.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.03, 0.009, 6, 14), phong(STEEL, 60)), ring[0], ring[1], ring[2], 0, PI / 2, 0));
      const pr = [sx - Math.cos(yw) * (Lp / 2 + 0.02), sh + 0.05, sz + Math.sin(yw) * (Lp / 2 + 0.02)];
      const n = 9; for (let i = 0; i <= n; i++) { const u = i / n, x = pr[0] + (ring[0] - pr[0]) * u, z = pr[2] + (ring[2] - pr[2]) * u, y = pr[1] + (ring[1] - pr[1]) * u - 0.22 * Math.sin(PI * u);
        const lk = rimmed(w => new THREE.TorusGeometry(0.022, 0.0075 + w, 6, 12), phong(STEEL, 60, '#DDE6F0'), '#101216', 0.004); lk.position.set(x, y, z); lk.scale.set(1.45, 1, 1); lk.rotation.set(i % 2 ? PI / 2 : 0, Math.atan2(ring[0] - pr[0], ring[2] - pr[2]) + PI / 2, 0); g.add(lk); }
      g.add(at(etatTag('ÉTAT', 1.1), sx + rs * 0.3, sh + 0.0, sz + 0.06, -0.15, -0.3 * rs, 0)); }
    return g;
  },

  // The forensic bench (pivot at the floor under its middle; front +Z): a steel table o.w (1.4) x 0.9 at 0.9 m, a big white board on it with a dark frame
  // (nothing is ever written on it), a ruler, a numbered evidence plate (o.plate 'SCELLÉ'), an open evidence bag; userData.board: the board's top centre
  styForensic(o) {
    const W = o.w ?? 1.4, Ht = 0.9, g = grp();
    g.add(at(box(W, 0.05, 0.9, '#B8C0C8', { outline: 0.004 }), 0, Ht - 0.025, 0)); for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(at(box(0.05, Ht - 0.05, 0.05, '#7A828A'), sx * (W / 2 - 0.06), (Ht - 0.05) / 2, sz * 0.38));
    g.add(at(box(0.92, 0.024, 0.62, '#2A2E34', { outline: 0.004 }), 0, Ht + 0.012, 0), at(box(0.86, 0.026, 0.56, '#FCFCFA'), 0, Ht + 0.014, 0));
    g.add(at(box(0.5, 0.008, 0.05, '#F2C80F', { outline: 0.02 }), 0, Ht + 0.004, 0.38)); for (let i = 0; i < 10; i++) g.add(at(box(0.004, 0.009, 0.02, '#1B1B1E'), -0.23 + i * 0.05, Ht + 0.008, 0.37));
    const pl = canvasPlane(0.22, 0.1, (c, cw, ch) => { c.fillStyle = '#F2C80F'; c.fillRect(0, 0, cw, ch); c.fillStyle = '#1B1B1E'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, o.plate || 'SCELLÉ', cw / 2, ch * 0.55, cw * 0.86, ch * 0.62); }, { res: 256 });
    const tent = grp(at(box(0.22, 0.1, 0.01, '#F2C80F', { outline: 0.02 }), 0, 0, 0), at(pl, 0, 0, 0.006)); tent.position.set(W / 2 - 0.2, Ht + 0.06, 0.2); tent.rotation.x = -0.5; g.add(tent);
    g.add(at(box(0.26, 0.006, 0.34, '#E8F0F0', { opacity: 0.7 }), -W / 2 + 0.2, Ht + 0.004, -0.15), at(box(0.26, 0.008, 0.04, '#C8202A'), -W / 2 + 0.2, Ht + 0.006, -0.3));
    g.userData.board = [0, Ht + 0.028, 0]; return g;
  },

  // A plain room for a shot (pivot at the floor): a back wall at o.back (z, -2) o.w (8) wide, o.h (3.2) high (o.wall, a band o.band to 1 m), a floor
  // raised 5 cm (o.floor), an optional side wall at x o.side; o.posters [{text, x, y, w, h, bg, fg}] on the back wall; o.ceil: a ceiling at that height
  styRoom(o) {
    const W = o.w ?? 8, Hh = o.h ?? 3.2, bz = o.back ?? -2, g = grp();
    g.add(at(box(W, Hh, 0.2, o.wall || '#E6E1D4', { pivot: 'bottom' }), 0, 0, bz - 0.1));
    if (o.band !== false) g.add(at(box(W, 1.0, 0.02, o.band || '#BFAF92'), 0, 0.5, bz + 0.01), at(box(W, 0.05, 0.04, o.trim || '#7A6A54'), 0, 1.0, bz + 0.02));
    const fl = at(box(W, 0.05, o.floorD ?? 8, o.floor || '#B8AE9C', { pivot: 'bottom' }), 0, 0, bz + (o.floorD ?? 8) / 2); fl.castShadow = false; g.add(fl);
    if (o.side != null) g.add(at(box(0.2, Hh, o.floorD ?? 8, o.wall || '#E6E1D4', { pivot: 'bottom' }), o.side, 0, bz + (o.floorD ?? 8) / 2));
    if (o.ceil) { const c = at(box(W, 0.1, o.floorD ?? 8, o.ceilColor || '#F0ECE4'), 0, o.ceil + 0.05, bz + (o.floorD ?? 8) / 2); c.castShadow = false; g.add(c); }
    for (const q of o.posters || []) { const pw = q.w ?? 0.8, ph = q.h ?? 0.3, pl = canvasPlane(pw, ph, (c, cw, ch) => { c.fillStyle = q.bg || '#1B2A4A'; c.fillRect(0, 0, cw, ch); c.fillStyle = q.fg || '#F4EEDC'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, q.text || '', cw / 2, ch * 0.55, cw * 0.86, ch * 0.6); }, { res: 512 });
      g.add(at(box(pw + 0.05, ph + 0.05, 0.02, q.frame || '#C9A24B', { outline: 0.006 }), q.x ?? 0, q.y ?? 2.4, bz + 0.02), at(pl, q.x ?? 0, q.y ?? 2.4, bz + 0.035)); }
    return g;
  },
};
