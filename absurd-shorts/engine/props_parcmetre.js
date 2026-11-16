// « Le parcmètre » (story 75): this man paid for his parking for four hundred years (the wrong button); the ticket is three kilometres long; the
// town hall would not refund him, so he stayed parked: he lives in his car, married on his bay, raised his children between the white lines; the
// postman slips the mail under the wiper, the mayor opens his bay every year, tourists photograph it; yesterday a delivery van double-parked beside
// him and paid for five hundred years. Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure
// function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere } from './style.js';
import { grp, at, canvasPlane, label, rod } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const lcd = (text, w, h) => canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#B9E4A6'; c.fillRect(0, 0, W, H); c.fillStyle = '#17301A'; c.textAlign = 'center'; c.textBaseline = 'middle';
  c.font = `900 ${Math.min(H * 0.62, W * 1.55 / Math.max(3, text.length))}px Arial`; c.fillText(text, W / 2, H * 0.54); }, { res: 256 });
const lin = (keys, t, d) => { if (!keys || !keys.length) return d; if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) if (t <= keys[i][0]) { const [t0, v0] = keys[i - 1], [t1, v1] = keys[i]; return v0 + (v1 - v0) * (t - t0) / Math.max(1e-6, t1 - t0); }
  return keys[keys.length - 1][1]; };
const lamp = (w, h, d, on) => box(w, h, d, on ? '#FFB22E' : '#B86A1E', on ? { emissive: '#FF9A10', noGrain: true } : {});

export const PARCMETRE_PROPS = {
  // A pay-and-display machine big enough to read in close-up (front +Z): a dark grey column, a blue P on a stalk, a green screen (o.screen 'PAYEZ ICI';
  // o.screens [[t, 'TEXT'], ...]: each text from its time; o.count {at, dur, values [1, 2, 5 ...], unit 'ANS'}: a counter rolling up through the values,
  // fast then slower), small grey keys under two big buttons (o.labels ['1 H', '400 ANS']: green left, red right; o.pressAt [t...]: the right one sinks
  // and lights for 0.3 s, o.pressLeftAt the left one; o.litAfter: the right one stays lit), the ticket slot (userData.slot, for ticketRibbon), a bronze
  // plaque (o.plaque, two lines split on a slash) and growth marks pencilled down its +X side (o.marks [[height m, 'LÉO'], ...]).
  // (pass 3 of 75) o.kickAt [t...]: at each time it kicks back about its foot (o.kickAmp 0.09 rad) and rocks to rest: a machine that spits.
  horodateur(o) {
    const g = grp(), M = grp(), D = '#3B4048', K = '#2A2C31'; g.add(M);   // (pass 3 of 75) M: everything, in a group that rocks (o.kickAt)
    M.add(at(box(0.56, 0.1, 0.42, K), 0, 0.05, 0), at(box(0.48, 1.32, 0.34, D, { outline: 0.008 }), 0, 0.76, 0), at(box(0.52, 0.08, 0.38, K), 0, 1.46, 0), at(box(0.04, 0.26, 0.04, K), 0, 1.63, 0));
    for (const s of [1, -1]) M.add(at(label('P', 0.34, 0.34, { bg: '#1E5BB8', fg: '#FFFFFF', wrap: false }), 0, 1.92, s * 0.012, 0, s > 0 ? 0 : PI, 0));
    const seq = [[-1e9, o.screen || 'PAYEZ ICI'], ...(o.screens || [])];
    if (o.count) { const c0 = o.count.at ?? 0, dur = o.count.dur ?? 1, vals = o.count.values || [1, 400], unit = o.count.unit ?? 'ANS';
      vals.forEach((v, i) => seq.push([c0 + dur * Math.pow(i / Math.max(1, vals.length - 1), 1.6), `${v} ${unit}`])); }
    seq.sort((a, b) => a[0] - b[0]);
    M.add(at(box(0.4, 0.19, 0.012, '#1B1C20'), 0, 1.25, 0.172));   // the screen's bezel
    const scr = seq.map(([, txt]) => { const p = lcd(txt, 0.36, 0.15); p.position.set(0, 1.25, 0.18); M.add(p); return p; });
    const [lA, lB] = o.labels || ['1 H', '400 ANS'];
    const btn = (txt, col, x) => { const b = grp(at(box(0.15, 0.1, 0.04, col, { outline: 0.004 }), 0, 0, 0)), t = label(txt, 0.13, 0.06, { bg: col, fg: '#FFFFFF', wrap: false });
      t.position.set(0, 0, 0.021); b.add(t); b.position.set(x, 1.06, 0.19); M.add(b); return b; };
    const bL = btn(lA, '#2E9A4E', -0.09), bR = btn(lB, '#D23A2E', 0.09);
    const lit = at(box(0.17, 0.12, 0.03, '#FF6A50', { emissive: '#FF3A20', noGrain: true }), 0, 0, -0.006); lit.visible = false; bR.add(lit);
    for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) M.add(at(box(0.06, 0.04, 0.02, '#C9CDD3'), -0.08 + 0.08 * c, 0.94 - 0.055 * r, 0.176));
    M.add(at(box(0.22, 0.035, 0.03, '#111215'), 0, 0.66, 0.176), at(box(0.26, 0.07, 0.06, '#1B1C20'), 0, 0.6, 0.18), at(box(0.12, 0.02, 0.02, '#111215'), 0.12, 0.8, 0.176));   // ticket slot, its lip, the card slot
    if (o.plaque) { const [a, b] = String(o.plaque).split('/');
      const pl = canvasPlane(0.36, 0.17, (c, W, H) => { c.fillStyle = '#B58A3C'; c.fillRect(0, 0, W, H); c.strokeStyle = '#6E5020'; c.lineWidth = W * 0.02; c.strokeRect(W * 0.04, H * 0.08, W * 0.92, H * 0.84);
        c.fillStyle = '#4A3410'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${H * 0.25}px Arial`; c.fillText(a.trim(), W / 2, b ? H * 0.37 : H * 0.52); if (b) c.fillText(b.trim(), W / 2, H * 0.68); }, { res: 256 });
      pl.position.set(0, 0.36, 0.172); M.add(pl); }
    if (o.marks) { const y0 = 0.15, y1 = 1.45;
      const side = canvasPlane(0.3, y1 - y0, (c, W, H) => { c.clearRect(0, 0, W, H);
        for (const [y, txt] of o.marks) { const py = H * (1 - (y - y0) / (y1 - y0)); c.strokeStyle = '#F2EEE2'; c.lineWidth = H * 0.007; c.beginPath(); c.moveTo(W * 0.06, py); c.lineTo(W * 0.7, py); c.stroke();
          c.fillStyle = '#F2EEE2'; c.font = `700 ${H * 0.04}px Arial`; c.textAlign = 'left'; c.textBaseline = 'bottom'; c.fillText(txt, W * 0.08, py - H * 0.008); } }, { res: 512, transparent: true });
      side.position.set(0.242, (y0 + y1) / 2, 0); side.rotation.y = PI / 2; M.add(side); }
    g.userData.update = t => { let k = 0; seq.forEach(([t0], i) => { if (t >= t0) k = i; }); scr.forEach((p, i) => { p.visible = i === k; });
      const on = list => (list || []).some(p => t >= p && t < p + 0.3), pR = on(o.pressAt), pL = on(o.pressLeftAt);
      bR.position.z = 0.19 - (pR ? 0.016 : 0); bL.position.z = 0.19 - (pL ? 0.016 : 0); lit.visible = pR || (o.litAfter != null && t >= o.litAfter);
      let ka = 0; for (const t0 of (o.kickAt || [])) { const u = t - t0; if (u >= 0 && u < 0.6) ka += (o.kickAmp ?? 0.09) * Math.exp(-u * 8) * Math.cos(u * 24); }
      M.rotation.x = -ka; M.position.z = -0.25 * ka; };
    g.userData.update(-1); g.userData.slot = [0, 0.64, 0.2]; return g;
  },

  // A pay-and-display ticket that will not stop printing (pivot at the machine's slot, the paper coming out toward +Z): a white strip o.w (0.09) wide
  // comes out, curls down to the ground o.drop (0.64) below and runs along o.path [[x, z], ...] (on the ground, relative to the pivot; a straight run
  // toward +Z when absent); from o.from it prints at o.rate m/s (1.6, with o.accel s of ramp, 0.3), from o.len0 m already out (0); the printed marks
  // (o.text '400 ANS') travel with the paper; the head lifts and flutters; o.color the print (blue).
  // (pass 3 of 75) o.jet (m): the paper shoots out level for that far, like water from a hose (drooping o.jetDrop, 0.12 m), then falls to the ground
  // (give o.path from there on); o.wave (m): the part in the air ripples; o.edge: a coloured line along both edges (a ribbon that reads on a pale
  // pavement); o.rep (0.6 m): the length of one print; o.textH (0.42): the height of the print across the paper.
  // o.across: the print written across the paper, upright for someone the ticket runs toward (a low lens in its way); o.turn: the print turned
  // half a turn (it reads upright from the other side of the run).
  ticketRibbon(o) {
    const w = o.w ?? 0.09, drop = o.drop ?? 0.64, g = grp(), R = Math.min(0.2, drop * 0.4), yg = -drop + 0.006;
    const raw = [new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, 0.05)];
    const jet = o.jet ?? 0, jd = o.jetDrop ?? 0.12, rp = o.rep ?? 0.6;
    if (jet > 0) { for (let i = 1; i <= 10; i++) { const f = i / 10; raw.push(new THREE.Vector3(0, -jd * f * f, 0.05 + jet * f)); }
      const fall = Math.max(0.25, (-jd - yg) * 0.8); for (let i = 1; i <= 8; i++) { const f = i / 8; raw.push(new THREE.Vector3(0, -jd + (yg + jd) * f * f, 0.05 + jet + fall * f)); } }
    else { for (let i = 1; i <= 8; i++) { const a = i / 8 * PI / 2; raw.push(new THREE.Vector3(0, -R + R * Math.cos(a), 0.05 + R * Math.sin(a))); }
      raw.push(new THREE.Vector3(0, yg + R, 0.05 + R));
      for (let i = 1; i <= 8; i++) { const a = i / 8 * PI / 2; raw.push(new THREE.Vector3(0, yg + R - R * Math.sin(a), 0.05 + R + R * (1 - Math.cos(a)))); } }
    for (const [x, z] of (o.path || [[0, 1.0], [0, 6.0]])) raw.push(new THREE.Vector3(x, yg, z));
    const P = [raw[0].clone()], S = [0], step = 0.05;   // resample every 5 cm
    for (let i = 1; i < raw.length; i++) { const A = raw[i - 1], B = raw[i], L = A.distanceTo(B); if (L < 1e-4) continue;
      const n = Math.max(1, Math.ceil(L / step)); for (let j = 1; j <= n; j++) { P.push(A.clone().lerp(B, j / n)); S.push(S[S.length - 1] + L / n); } }
    const N = P.length, Ltot = S[N - 1], pos = new Float32Array(N * 6), uv = new Float32Array(N * 4), idx = [];
    let prev = new THREE.Vector3(1, 0, 0);
    for (let i = 0; i < N; i++) { const tg = P[Math.min(N - 1, i + 1)].clone().sub(P[Math.max(0, i - 1)]).normalize(), sd = new THREE.Vector3(tg.z, 0, -tg.x);
      if (sd.length() < 0.3) sd.copy(prev); else { sd.normalize(); if (sd.dot(prev) < 0) sd.negate(); } prev = sd;
      const a = P[i].clone().addScaledVector(sd, -w / 2), b = P[i].clone().addScaledVector(sd, w / 2);
      pos.set([a.x, a.y, a.z, b.x, b.y, b.z], i * 6); uv.set([-S[i] / rp, 0, -S[i] / rp, 1], i * 4);
      if (i < N - 1) idx.push(i * 2, i * 2 + 1, i * 2 + 2, i * 2 + 1, i * 2 + 3, i * 2 + 2); }
    const base = pos.slice(), geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3)); geo.setAttribute('uv', new THREE.BufferAttribute(uv, 2)); geo.setIndex(idx); geo.computeVertexNormals();
    const tex = canvasPlane(rp, w, (c, W, H) => { c.fillStyle = '#FBFBF6'; c.fillRect(0, 0, W, H); if (o.edge) { c.fillStyle = o.edge; c.fillRect(0, 0, W, H * 0.08); c.fillRect(0, H * 0.92, W, H * 0.08); }
      c.fillStyle = o.color || '#2A4FA0'; c.textBaseline = 'middle'; const txt = o.text || '400 ANS';
      c.save();
      if (o.across) { c.translate(W / 2, H / 2); c.transform(0, -1, -1, 0, 0, 0); c.textAlign = 'center'; c.font = `900 ${Math.min(W * 0.62, H * 0.88 / (0.6 * txt.length))}px Arial`; c.fillText(txt, 0, 0); }
      else { c.font = `900 ${Math.min(H * (o.textH ?? 0.42), W * 0.19)}px Arial`; c.translate(W, 0); c.scale(-1, 1); if (o.turn) { c.translate(W / 2, H / 2); c.rotate(PI); c.translate(-W / 2, -H / 2); } c.fillText(txt, W * 0.08, H * 0.5); }
      c.restore();
      if (!o.across) { c.fillStyle = 'rgba(40,60,110,0.35)'; for (let k = 0; k < 6; k++) c.fillRect(W * (0.55 + k * 0.06), H * 0.3, W * 0.03, H * 0.4); } }, { res: 256 }).material.map;
    tex.wrapS = THREE.RepeatWrapping;
    const strip = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ map: tex, side: THREE.DoubleSide })); strip.castShadow = strip.receiveShadow = true; g.add(strip);
    const len = t => { const u = t - (o.from ?? 0), A = o.accel ?? 0.3, r = o.rate ?? 1.6; const d = u <= 0 ? 0 : u < A ? r * u * u / (2 * A) : r * (u - A / 2); return Math.min(Ltot, (o.len0 ?? 0) + d); };
    let lifted = []; const wv = o.wave ?? 0, air = []; for (let i = 0; i < N; i++) if (base[i * 6 + 1] > yg + 0.02 && S[i] > 0.1) air.push(i);
    g.userData.update = t => { const L = len(t); for (const i of lifted) for (const e of [0, 3]) pos[i * 6 + e + 1] = base[i * 6 + e + 1]; lifted = [];
      let n = 0; while (n < N - 1 && S[n + 1] <= L) n++;
      geo.setDrawRange(0, n * 6); tex.offset.x = L / rp; strip.visible = n > 0;
      for (let i = n; i >= 0 && S[i] > L - 0.3; i--) { if (base[i * 6 + 1] > yg + 0.02) break; const f = (S[i] - (L - 0.3)) / 0.3, lift = 0.07 * f * f * (1 + 0.35 * Math.sin(t * 19 + i));
        for (const e of [0, 3]) pos[i * 6 + e + 1] = base[i * 6 + e + 1] + lift; lifted.push(i); }
      if (wv) for (const i of air) { const dy = wv * Math.min(1, S[i] / 0.4) * Math.sin(t * 31 - S[i] * 9); for (const e of [0, 3]) pos[i * 6 + e + 1] = base[i * 6 + e + 1] + dy; }
      geo.attributes.position.needsUpdate = true; };
    g.userData.update(-1); g.userData.length = Ltot; return g;
  },

  // A parked car made into a home (pivot at the car prop's origin, the car facing +X: put it at the same place and ry): gingham curtains tied back in
  // the rear side windows and a scalloped valance (o.curtains), a stove pipe through the roof puffing smoke (o.smoke), a geranium on the roof (o.plant),
  // a fishbone TV aerial (o.aerial), a BIENVENUE doormat under the driver's door (o.mat), two wipers at the foot of the windscreen; o.letterAt: an envelope
  // slides in under the driver's-side wiper at that time and flutters there (o.letter: already there).
  // (pass 3 of 75) o.matAt [x, z]: where the mat lies (car-local); o.matRot (rad): the mat turned about the vertical (PI: its word reads from the other side).
  carHome(o) {
    const g = grp(), on = k => o[k] !== false;
    if (on('curtains')) { const cur = (flip) => canvasPlane(0.42, 0.98, (c, W, H) => { c.clearRect(0, 0, W, H); c.save(); if (flip) { c.translate(W, 0); c.scale(-1, 1); }
        c.beginPath(); c.moveTo(0, 0); c.lineTo(W * 0.95, 0); c.quadraticCurveTo(W * 0.55, H * 0.45, W * 0.32, H * 0.6); c.quadraticCurveTo(W * 0.62, H * 0.8, W * 0.7, H); c.lineTo(0, H); c.closePath(); c.clip();
        c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.fillStyle = 'rgba(226,92,122,0.75)'; const q = W / 6; for (let x = 0; x < W; x += q) c.fillRect(x, 0, q / 2, H); for (let y = 0; y < H; y += q) c.fillRect(0, y, W, q / 2);
        c.fillStyle = '#C83A5E'; c.fillRect(0, H * 0.585, W * 0.5, H * 0.03); c.restore(); }, { res: 256, transparent: true });
      for (const sz of [-1, 1]) { for (const [x, flip] of [[-1.48, false], [-0.44, true]]) { const p = cur(flip !== (sz < 0)); p.position.set(x, 1.46, sz * 0.83); if (sz < 0) p.rotation.y = PI; g.add(p); }
        const val = canvasPlane(1.42, 0.16, (c, W, H) => { c.clearRect(0, 0, W, H); c.fillStyle = '#E25C7A'; c.beginPath(); c.moveTo(0, 0); c.lineTo(W, 0); c.lineTo(W, H * 0.55);
          const n = 9; for (let i = n; i >= 0; i--) c.quadraticCurveTo(W * (i + 0.5) / n, H * 1.05, W * i / n, H * 0.55); c.closePath(); c.fill(); }, { res: 256, transparent: true });
        val.position.set(-0.96, 1.92, sz * 0.825); if (sz < 0) val.rotation.y = PI; g.add(val); } }
    let puffs = [];
    if (on('smoke')) { g.add(at(cyl(0.065, 0.065, 0.5, '#4A4E55', 10, { pivot: 'bottom', outline: 0.005 }), -1.15, 2.05, 0.42), at(cyl(0.11, 0.11, 0.04, '#33363B', 10), -1.15, 2.57, 0.42));
      puffs = [0, 1, 2, 3].map(i => { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 1), new THREE.MeshLambertMaterial({ color: '#D9DCDF', transparent: true, depthWrite: false })); g.add(m); return m; }); }
    if (on('plant')) { g.add(at(cyl(0.11, 0.085, 0.16, '#C2653A', 10, { pivot: 'bottom', outline: 0.005 }), 0.5, 2.055, -0.32));
      [[0, 0.24, 0, 0.1], [0.08, 0.2, 0.05, 0.08], [-0.08, 0.21, -0.04, 0.08], [0.03, 0.19, -0.09, 0.07]].forEach(([x, y, z, r]) => g.add(at(sphere(r, '#3E8E4A', 1), 0.5 + x, 2.055 + y, -0.32 + z)));
      [[0.02, 0.33, 0.02], [0.1, 0.28, 0.06], [-0.08, 0.3, -0.05], [0.05, 0.29, -0.1], [-0.04, 0.34, 0.08]].forEach(([x, y, z]) => g.add(at(sphere(0.045, '#E0303A', 1), 0.5 + x, 2.055 + y, -0.32 + z))); }
    if (on('aerial')) { const ax = -0.45, az = -0.5, top = 2.62; g.add(rod([ax, 2.05, az], [ax, top, az], 0.015, '#9AA0A6'), rod([ax - 0.3, top, az], [ax + 0.3, top, az], 0.012, '#9AA0A6'));
      for (let i = 0; i < 5; i++) { const x = ax - 0.26 + i * 0.13, hw = 0.2 - i * 0.025; g.add(rod([x, top, az - hw], [x, top, az + hw], 0.008, '#9AA0A6')); } }
    if (on('mat')) { const mx = o.matAt?.[0] ?? 0.05, mz = o.matAt?.[1] ?? -1.22; g.add(at(box(0.74, 0.025, 0.44, '#9A6B3A', { outline: 0.004 }), mx, 0.012, mz));
      const t = canvasPlane(0.66, 0.36, (c, W, H) => { c.fillStyle = '#9A6B3A'; c.fillRect(0, 0, W, H); c.fillStyle = '#3E2A16'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${H * 0.3}px Arial`; c.fillText('BIENVENUE', W / 2, H * 0.52); }, { res: 256 });
      t.position.set(mx, 0.026, mz); t.rotation.x = -PI / 2; t.rotation.z = o.matRot ?? 0; g.add(t); }
    const wip = grp(); wip.position.set(1.5, 0.935, 0); wip.rotation.z = 0.4; g.add(wip);   // in the windscreen's tilt: +Y up the glass, +X out of it
    for (const z0 of [-0.72, 0.02]) wip.add(rod([0.035, 0.0, z0], [0.035, 0.06, z0 + 0.62], 0.012, '#1E2024'), at(box(0.02, 0.02, 0.62, '#2A2C31'), 0.045, 0.03, z0 + 0.31));
    let env = null;
    if (o.letterAt != null || o.letter) { env = canvasPlane(0.26, 0.16, (c, W, H) => { c.fillStyle = '#F6F2E6'; c.fillRect(0, 0, W, H); c.strokeStyle = '#B9B2A0'; c.lineWidth = W * 0.012; c.beginPath(); c.moveTo(0, 0); c.lineTo(W / 2, H * 0.55); c.lineTo(W, 0); c.stroke();
        c.fillStyle = '#C8322A'; c.fillRect(W * 0.78, H * 0.12, W * 0.14, H * 0.26); c.fillStyle = '#4A4A4A'; c.fillRect(W * 0.12, H * 0.62, W * 0.4, H * 0.06); c.fillRect(W * 0.12, H * 0.74, W * 0.3, H * 0.06); }, { res: 256 });
      env.rotation.y = PI / 2; wip.add(env); }
    g.userData.update = t => {
      puffs.forEach((m, i) => { const u = ((t * 0.55 + i / 4) % 1 + 1) % 1, s = 0.07 + 0.2 * u; m.position.set(-1.15 - 0.35 * u * u, 2.65 + 0.95 * u, 0.42 + 0.05 * Math.sin(t * 2 + i)); m.scale.setScalar(s); m.material.opacity = 0.85 * (1 - u) * Math.min(1, u * 8); });
      if (env) { const a = o.letter ? 1 : clamp01((t - o.letterAt) / 0.3); env.visible = a > 0; env.position.set(0.03, 0.1 + 0.25 * (1 - a) * (1 - a), -0.38); env.rotation.x = a >= 1 ? 0.06 * Math.sin(t * 9) : 0; } };
    g.userData.update(-1); return g;
  },

  // A delivery van (pivot at the floor in its middle, facing +X like the car prop): a white cargo box with LIVRAISON on both sides (o.text), a cab in
  // o.color with a see-through windscreen, open side windows, two seats (userData.seat driver at -Z, userData.seat2 passenger at +Z, for clip 'drive'
  // or 'sitTalk'), a dash and wheel; four orange hazard lamps blinking from o.hazardFrom (1.6 Hz); o.brakeAt: the nose dips and the body rebounds as it stops.
  // (review 1 of 75) o.brakeAmp (1): scales that dip and rebound (2.5: a cartoon stop, the rear lifting)
  deliveryVan(o) {
    const C = o.color || '#E9E6DE', g = grp(), body = grp(); g.add(body);
    const glass = new THREE.MeshLambertMaterial({ color: '#CFEAF5', transparent: true, opacity: 0.2, depthWrite: false });
    body.add(at(box(3.4, 2.3, 2.0, '#F4F4F0', { pivot: 'bottom', outline: 0.014 }), -0.9, 0.45, 0));                 // the cargo box
    body.add(at(box(1.5, 0.55, 2.0, C, { pivot: 'bottom', outline: 0.012 }), 1.55, 0.45, 0), at(box(0.55, 0.3, 2.0, C, { outline: 0.01 }), 2.03, 1.12, 0));   // cab lower body, bonnet
    body.add(at(box(1.15, 0.08, 2.0, C, { outline: 0.01 }), 1.32, 2.44, 0));                                          // cab roof
    for (const z of [-0.96, 0.96]) { body.add(at(box(1.2, 0.36, 0.08, C, { outline: 0.006 }), 1.4, 1.18, z), rod([2.28, 1.27, z], [1.86, 2.42, z], 0.045, C), at(box(0.08, 1.0, 0.08, C), 0.84, 1.9, z)); }   // door tops, A pillars, B pillars
    const ws = new THREE.Mesh(new THREE.BoxGeometry(0.02, 1.23, 1.86), glass); ws.position.set(2.07, 1.85, 0); ws.rotation.z = 0.35; body.add(ws);
    for (const z of [-0.45, 0.45]) body.add(at(box(0.45, 0.12, 0.46, '#3A3D44'), 1.15, 0.95, z), at(box(0.1, 0.62, 0.46, '#3A3D44'), 0.92, 1.3, z, 0, 0, 0.12));   // seats
    body.add(at(box(0.3, 0.26, 1.8, '#2A2A2E'), 1.88, 1.28, 0), at(new THREE.Mesh(new THREE.TorusGeometry(0.17, 0.025, 6, 16), new THREE.MeshLambertMaterial({ color: '#1A1B1E' })), 1.62, 1.5, -0.45, 0, PI / 2, 0.35));
    body.add(at(box(0.06, 0.32, 1.5, '#23262B', { outline: 0.005 }), 2.3, 0.78, 0), at(box(0.12, 0.2, 2.06, '#1C1E22', { outline: 0.006 }), 2.33, 0.5, 0));   // grille, bumper
    for (const z of [-0.78, 0.78]) body.add(at(box(0.04, 0.14, 0.3, '#FFF3C2', { emissive: '#FFE38A', noGrain: true }), 2.31, 1.02, z));
    for (const s of [1, -1]) { const t = label(o.text || 'LIVRAISON', 2.6, 0.5, { bg: '#F4F4F0', fg: '#2F62B5', wrap: false }); t.position.set(-0.9, 1.75, s * 1.004); if (s < 0) t.rotation.y = PI; body.add(t);
      body.add(at(box(2.8, 0.1, 0.01, '#2F62B5'), -0.9, 1.35, s * 1.004)); }
    for (const x of [-1.9, 1.55]) for (const z of [-0.9, 0.9]) { const wh = cyl(0.4, 0.4, 0.26, '#22252A', 14); wh.rotation.x = PI / 2; wh.position.set(x, 0.4, z); g.add(wh);
      const hub = cyl(0.17, 0.17, 0.02, '#B9BEC4', 8); hub.rotation.x = PI / 2; hub.position.set(x, 0.4, z * 1.16); g.add(hub); }
    const hz = [[2.31, 0.92, -0.85], [2.31, 0.92, 0.85], [-2.61, 0.95, -0.82], [-2.61, 0.95, 0.82]].map(([x, y, z]) => { const off = at(lamp(0.04, 0.12, 0.2, false), x, y, z), lit = at(lamp(0.05, 0.14, 0.22, true), x, y, z); lit.visible = false; body.add(off, lit); return lit; });
    g.userData.update = t => { const blink = o.hazardFrom != null && t >= o.hazardFrom && ((t - o.hazardFrom) * (o.hazardRate ?? 1.6)) % 1 < 0.5; hz.forEach(l => { l.visible = blink; });
      const u = o.brakeAt == null ? -1 : t - o.brakeAt, a = u >= 0 && u < 1.2 ? Math.exp(-4.5 * u) * Math.sin(u * 13) : 0;
      const ba = o.brakeAmp ?? 1; body.rotation.z = -0.07 * ba * a; body.position.y = -0.04 * ba * Math.abs(a); body.scale.set(1 + 0.05 * ba * Math.max(0, a), 1 - 0.04 * ba * Math.max(0, a), 1); };
    g.userData.update(-1); g.userData.seat = [1.15, 0.5, -0.45]; g.userData.seat2 = [1.15, 0.5, 0.45]; return g;
  },

  // A washing line (pivot at its first end): a sagging cord to o.to [x, y, z] (o.sag 0.18) with o.n (4) things pegged on it, swaying: a shirt, socks,
  // trousers, a vest, in o.colors.
  clothesline(o) {
    const to = new THREE.Vector3(...(o.to || [2, 0, 0])), n = o.n ?? 4, sag = o.sag ?? 0.18, g = grp(), cols = o.colors || ['#5B8BD9', '#E25C7A', '#3A4A6A', '#F2C94E', '#FFFFFF'];
    const P = u => new THREE.Vector3(to.x * u, to.y * u - 4 * sag * u * (1 - u), to.z * u);
    for (let i = 0; i < 12; i++) g.add(rod(P(i / 12).toArray(), P((i + 1) / 12).toArray(), 0.006, '#E8E4D8'));
    const ry = Math.atan2(-to.z, to.x), items = [];
    for (let i = 0; i < n; i++) { const u = (i + 1) / (n + 1), it = grp(), c = cols[i % cols.length], kind = i % 4;
      if (kind === 0) it.add(at(box(0.3, 0.32, 0.012, c, { outline: 0.004 }), 0, -0.18, 0), at(box(0.12, 0.1, 0.012, c), -0.2, -0.07, 0, 0, 0, 0.5), at(box(0.12, 0.1, 0.012, c), 0.2, -0.07, 0, 0, 0, -0.5));
      else if (kind === 1) for (const dx of [-0.07, 0.07]) it.add(at(box(0.07, 0.2, 0.012, c, { outline: 0.003 }), dx, -0.11, 0), at(box(0.1, 0.06, 0.012, c), dx + 0.02, -0.2, 0));
      else if (kind === 2) it.add(at(box(0.28, 0.1, 0.012, c, { outline: 0.004 }), 0, -0.06, 0), at(box(0.12, 0.42, 0.012, c), -0.075, -0.32, 0), at(box(0.12, 0.42, 0.012, c), 0.075, -0.32, 0));
      else it.add(at(box(0.24, 0.3, 0.012, c, { outline: 0.004 }), 0, -0.16, 0));
      for (const dx of [-0.08, 0.08]) it.add(at(box(0.02, 0.05, 0.02, '#C9A06A'), dx, 0.0, 0.01));
      const holder = grp(it); holder.position.copy(P(u)); holder.rotation.y = ry; g.add(holder); items.push(it); }
    g.userData.update = t => items.forEach((it, i) => { it.rotation.x = 0.18 * Math.sin(t * 2.3 + i * 1.4); it.rotation.z = 0.05 * Math.sin(t * 1.7 + i); });
    g.userData.update(0); return g;
  },

  // A chalk hopscotch on the asphalt (pivot at its start, running along +X): squares 1 to 8 with the doubled ones side by side and CIEL at the end,
  // o.len (2.7) long, o.w (0.8) wide, chalk o.color (white).
  hopscotch(o) {
    const L = o.len ?? 2.7, W = o.w ?? 0.8;
    const p = canvasPlane(L, W, (c, CW, CH) => { c.clearRect(0, 0, CW, CH); c.strokeStyle = o.color || 'rgba(250,250,245,0.92)'; c.fillStyle = c.strokeStyle; c.lineWidth = CH * 0.03; c.lineJoin = 'round';
      const cell = CW / 6.2, h = CH * 0.9, y0 = CH * 0.05, sq = (x, y, w, hh, txt) => { c.strokeRect(x, y, w, hh); c.font = `700 ${Math.min(w, hh) * 0.5}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(txt, x + w / 2, y + hh / 2); };
      sq(0, y0 + h * 0.25, cell, h * 0.5, '1'); sq(cell, y0 + h * 0.25, cell, h * 0.5, '2'); sq(cell * 2, y0, cell, h / 2, '3'); sq(cell * 2, y0 + h / 2, cell, h / 2, '4');
      sq(cell * 3, y0 + h * 0.25, cell, h * 0.5, '5'); sq(cell * 4, y0, cell, h / 2, '6'); sq(cell * 4, y0 + h / 2, cell, h / 2, '7'); sq(cell * 5, y0 + h * 0.25, cell, h * 0.5, '8');
      c.beginPath(); c.arc(cell * 6, CH / 2, h * 0.3, -PI / 2, PI / 2); c.stroke(); c.font = `700 ${h * 0.16}px Arial`; c.fillText('CIEL', cell * 5.95, CH / 2); }, { res: 512, transparent: true });
    p.rotation.x = -PI / 2; p.position.set(L / 2, 0.012, 0); return grp(p);
  },

  // A giant roll of ticket paper (pivot at its lowest point, its axis along X): radius o.r (0.5), o.w (0.12) wide, the sides drawn as a tight spiral,
  // the rim white with blue print; o.tail (0.5): the loose end hanging from the front and lying on the floor ahead of it.
  // (pass 3 of 75) o.text: printed big across both sides and as blue marks round the rim (an unprinted roll read as a white wheel).
  paperRoll(o) {
    const r = o.r ?? 0.5, w = o.w ?? 0.12, g = grp();
    const side = canvasPlane(2 * r, 2 * r, (c, W, H) => { c.clearRect(0, 0, W, H); c.fillStyle = '#FBFBF6'; c.beginPath(); c.arc(W / 2, H / 2, W / 2, 0, TAU); c.fill(); c.strokeStyle = 'rgba(150,150,140,0.55)'; c.lineWidth = W * 0.004;
      for (let k = 1; k < 34; k++) { c.beginPath(); c.arc(W / 2, H / 2, W / 2 * (0.12 + 0.88 * k / 34), 0, TAU); c.stroke(); } c.fillStyle = '#8A7A5C'; c.beginPath(); c.arc(W / 2, H / 2, W * 0.06, 0, TAU); c.fill();
      if (o.text) { c.fillStyle = o.textColor || '#2A4FA0'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${W * 0.2}px Arial`; c.fillText(o.text, W / 2, H * 0.32); c.fillText(o.text, W / 2, H * 0.7); } }, { res: 512, transparent: true });
    for (const s of [-1, 1]) { const m = side.clone(); m.position.set(s * (w / 2 + 0.002), r, 0); m.rotation.y = s * PI / 2; g.add(m); }
    const rim = cyl(r, r, w, '#F4F4EE', 28, { outline: 0.006 }); rim.rotation.z = PI / 2; rim.position.set(0, r, 0); g.add(rim);
    if (o.text) for (let k = 0; k < 22; k++) { const a = k / 22 * TAU; g.add(at(box(w * 0.62, 0.012, 0.05, o.textColor || '#2A4FA0'), 0, r + (r + 0.004) * Math.cos(a), (r + 0.004) * Math.sin(a), a, 0, 0)); }
    const tail = o.tail ?? 0.5; if (tail > 0) g.add(at(box(w * 0.95, 0.004, tail, '#FBFBF6', { outline: 0.002 }), 0, 0.004, r * 0.75 + tail / 2), at(box(w * 0.95, r * 0.9, 0.004, '#FBFBF6'), 0, r * 0.45, r * 0.98));
    return g;
  },

  // A card game on a little tray (pivot at the middle of the tray's underside): a wooden tray o.w (0.6) x o.d (0.34), a face-down deck at one end, a
  // pile in the middle; o.slapAt [t...]: a card slaps down on the pile (from 0.25 m up in 0.09 s, a little bounce) and stays, the pile growing.
  // (review 1 of 75) o.cardScale (1): bigger cards (2: they read at phone size); o.top: the tray's colour (a light one under white cards)
  // (pass 3 of 75) o.bounce (m): at each slap the tray dips that far and springs back, and the cards already down hop.
  cardTray(o) {
    const cs = o.cardScale ?? 1, w = o.w ?? 0.6, d = o.d ?? 0.34, G = grp(), g = grp(at(box(w, 0.03, d, o.top || '#B98A5A', { outline: 0.004 }), 0, 0.015, 0), at(box(w, 0.04, 0.02, '#8A6238'), 0, 0.04, d / 2 - 0.01), at(box(w, 0.04, 0.02, '#8A6238'), 0, 0.04, -d / 2 + 0.01));
    g.add(at(box(0.07 * cs, 0.04, 0.1 * cs, '#2F62B5', { outline: 0.003 }), -w / 2 + 0.05 + 0.035 * cs, 0.05, 0));
    const face = (suit, red) => canvasPlane(0.07 * cs, 0.1 * cs, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.strokeStyle = '#9A9A9A'; c.lineWidth = W * 0.04; c.strokeRect(0, 0, W, H);
      c.fillStyle = red ? '#D22B2B' : '#1C1C1C'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${H * 0.5}px Arial`; c.fillText(suit, W / 2, H * 0.55); }, { res: 128 });
    const S = ['♥', '♠', '♦', '♣'], cards = (o.slapAt || []).map((t0, i) => { const f = face(S[i % 4], i % 2 === 0); f.rotation.x = -PI / 2; const h = grp(f); g.add(h); return { t0, h, i }; });
    G.add(g); const bn = o.bounce ?? 0, hit = t => (o.slapAt || []).reduce((a, t0) => { const u = t - t0 - 0.09; return a + (u >= 0 && u < 0.5 ? Math.exp(-u * 9) * Math.cos(u * 28) : 0); }, 0);
    G.userData.update = t => { g.position.y = -bn * hit(t); g.rotation.x = 0.6 * bn * hit(t); cards.forEach(({ t0, h, i }) => { const u = t - t0; h.visible = u >= 0; if (u < 0) return; const fall = clamp01(u / 0.09), y = 0.035 + 0.003 * i + (u > 0.3 ? 1.6 * bn * Math.max(0, hit(t)) : 0);
      h.position.set(0.04 * cs * Math.sin(i * 2.1), y + 0.25 * (1 - fall) * (1 - fall) + (u > 0.09 && u < 0.25 ? 0.02 * Math.sin((u - 0.09) / 0.16 * PI) : 0), 0.03 * cs * Math.cos(i * 1.7)); h.rotation.y = 0.3 * Math.sin(i * 1.3); }); };
    G.userData.update(-1); return G;
  },

  // (review 1 of 75) A hand of playing cards fanned out (pivot at the hand, the fan rising along +Y, faces toward +Z): o.n (5) white cards o.s (1: 0.12 x
  // 0.17 m) with red and black suits, spread over o.spread (1.1 rad); a blue back on the other side
  cardFan(o) {
    const n = o.n ?? 5, sc = o.s ?? 1, cw = 0.12 * sc, ch = 0.17 * sc, sp = o.spread ?? 1.1, g = grp(), S = ['♥', '♠', '♦', '♣', '♥'];
    for (let i = 0; i < n; i++) { const a = (i / Math.max(1, n - 1) - 0.5) * sp, piv = grp(); piv.rotation.z = -a; piv.position.z = 0.002 * i;
      const front = canvasPlane(cw, ch, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.strokeStyle = '#8A8A8A'; c.lineWidth = W * 0.04; c.strokeRect(0, 0, W, H);
        c.fillStyle = i % 2 === 0 ? '#D22B2B' : '#1C1C1C'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${H * 0.42}px Arial`; c.fillText(S[i % S.length], W / 2, H * 0.55); }, { res: 128 });
      front.position.set(0, ch * 0.42, 0.001); const back = at(box(cw * 0.96, ch * 0.96, 0.002, '#2F62B5'), 0, ch * 0.42, -0.001); piv.add(back, front); g.add(piv); }
    return g;
  },

  // (pass 3 of 75) The ribbon across his bay (pivot on the ground at its middle, running along X): two brass posts o.w (2.3) apart, a wide
  // blue-white-red ribbon o.h (0.95) up (three inked bands, o.band 0.055 m each), a big rosette in the middle with two tails; o.cutAt: the two
  // halves swing down from the posts and the rosette drops, spinning. (The thin shared ribbon was 6 px thick in a wide shot.)
  bayRibbon(o) {
    const w = o.w ?? 2.3, h = o.h ?? 0.95, bd = o.band ?? 0.055, g = grp(), cols = ['#2A4B9B', '#F4F1E8', '#D2282E'];
    for (const s of [-1, 1]) g.add(at(cyl(0.04, 0.05, h + 0.12, '#C8A24A', 8, { pivot: 'bottom', outline: 0.006 }), s * w / 2, 0, 0), at(sphere(0.065, '#E0B84E', 1), s * w / 2, h + 0.16, 0));
    const halves = [-1, 1].map(s => { const hg = grp(...cols.map((c, i) => at(box(w / 2, bd, 0.01, c, { outline: 0.006 }), -s * w / 4, (1 - i) * bd, 0))); hg.position.set(s * w / 2, h, 0); g.add(hg); return { hg, s }; });
    const ros = grp();
    for (const [r, c, z] of [[0.17, '#D2282E', 0.008], [0.115, '#F4F1E8', 0.018], [0.06, '#2A4B9B', 0.028]]) for (const sz of [-1, 1]) ros.add(at(cyl(r, r, 0.012, c, 18), 0, 0, sz * z, PI / 2, 0, 0));
    for (const sx of [-1, 1]) ros.add(at(box(0.07, 0.3, 0.008, sx < 0 ? '#2A4B9B' : '#D2282E', { outline: 0.004 }), sx * 0.06, -0.26, 0, 0, 0, sx * 0.18));
    ros.position.set(0, h, 0); g.add(ros);
    g.userData.update = t => { const u = o.cutAt == null ? -1 : t - o.cutAt, f = Math.max(0, u);
      for (const { hg, s } of halves) { const a = u < 0 ? 0 : Math.min(1.35, u * 9) - 0.18 * Math.sin(Math.max(0, u - 0.15) * 11) * Math.exp(-Math.max(0, u - 0.15) * 3); hg.rotation.z = s * a; }
      ros.position.y = Math.max(0.1, h - 4.9 * f * f); ros.rotation.z = u > 0 ? 7 * Math.min(f, 0.42) : 0.06 * Math.sin(t * 5); };
    g.userData.update(0); return g;
  },

  // (pass 3 of 75) Giant ceremonial scissors that read against a red car and a grey road (pivot at their screw, the blades along +X): white blades
  // with an ink outline, gold rings (o.handle); o.snip [[t, 0..1]]: 1 open, 0 shut, linear between the keys; o.open (0.35 rad): how far each blade opens.
  goldScissors(o) {
    const L = o.len ?? 0.5, g = grp(), H = o.handle || '#F0B92E';
    const mk = s => { const b = grp(at(box(L, 0.05, 0.014, '#FFFFFF', { outline: 0.022 }), L / 2, 0, 0), at(cyl(0.085, 0.085, 0.024, H, 14, { outline: 0.012 }), -0.11, -s * 0.06, 0, PI / 2, 0, 0),
      at(cyl(0.04, 0.04, 0.028, '#5A3E12', 12), -0.11, -s * 0.06, 0, PI / 2, 0, 0)); g.add(b); return b; };
    const a = mk(1), b = mk(-1); g.add(at(sphere(0.024, '#8A9097', 1), 0, 0, 0.014));
    g.userData.update = t => { const op = clamp01(lin(o.snip, t, 1)) * (o.open ?? 0.35); a.rotation.z = op; b.rotation.z = -op; };
    g.userData.update(0); return g;
  },
};
