// « Le bus » (story 72): this man missed his bus by two seconds and ran after it for three years, escorted by the gendarmes, followed by the cycle
// race, fed by an Italian waiter on the run; when the bus stopped he got on: it was not his bus. Conventions as in props.js (metres, front +Z, pivot
// at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const hash = i => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

export const BUS_PROPS = {
  // A French town sign on its post (front +Z): a white plate with a red border and the town's name; o.exit: the red bar across it (leaving the
  // town); o.name, o.w (1.3), o.h (post height to the plate's bottom, 1.5)
  townSign(o) {
    const w = o.w ?? 1.3, ph = w * 0.42, y = o.h ?? 1.5, g = grp();
    g.add(at(box(0.07, y + ph, 0.07, '#8E949A', { pivot: 'bottom' }), 0, 0, -0.06));
    const face = canvasPlane(w, ph, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.strokeStyle = '#D22B2B'; c.lineWidth = H * 0.1; c.strokeRect(H * 0.07, H * 0.07, W - H * 0.14, H - H * 0.14);
      c.fillStyle = '#17181C'; c.textAlign = 'center'; c.textBaseline = 'middle'; let fs = H * 0.42; c.font = `900 ${fs}px Arial`; const tw = c.measureText(o.name || 'VILLE').width; if (tw > W * 0.82) { fs *= W * 0.82 / tw; c.font = `900 ${fs}px Arial`; }
      c.fillText(o.name || 'VILLE', W / 2, H * 0.53);
      if (o.exit) { c.strokeStyle = '#D22B2B'; c.lineWidth = H * 0.12; c.beginPath(); c.moveTo(W * 0.08, H * 0.88); c.lineTo(W * 0.92, H * 0.12); c.stroke(); } }, { res: 512 });
    g.add(at(box(w + 0.04, ph + 0.04, 0.03, '#C9CDD2', { outline: 0.006 }), 0, y + ph / 2, 0)); face.position.set(0, y + ph / 2, 0.017); g.add(face);
    return g;
  },

  // A race number to pin on a back or a chest (pivot at its middle, front +Z): a white bib with the number o.num big in black, a red strip along
  // the top and four safety pins at the corners, o.w x o.h (0.26 x 0.2)
  raceBib(o) {
    const w = o.w ?? 0.26, h = o.h ?? 0.2, g = grp();
    const face = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.fillStyle = '#D22B2B'; c.fillRect(0, 0, W, H * 0.16);
      c.fillStyle = '#16181C'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${H * 0.62}px Arial`; c.fillText(String(o.num ?? '1'), W / 2, H * 0.6); }, { res: 256 });
    g.add(at(box(w, h, 0.004, '#F4F4F0'), 0, 0, 0)); face.position.z = 0.003; g.add(face);
    for (const [x, y] of [[-1, 1], [1, 1], [-1, -1], [1, -1]]) g.add(at(sphere(0.008, '#C9CDD2', 0), x * (w / 2 - 0.018), y * (h / 2 - 0.018), 0.006));
    return g;
  },

  // The yellow jersey thrown over his suit (pivot at the bottom middle of his torso, front +Z): a yellow shell o.w x o.h x o.d (0.5 x 0.6 x 0.3)
  // with short sleeves and a black collar band; o.at: it drops on from above at that time, squashing down onto his shoulders (before it, hidden)
  jersey(o) {
    const w = o.w ?? 0.5, h = o.h ?? 0.6, d = o.d ?? 0.3, Y = o.color || '#F7D23A', g = grp(), shell = grp(); g.add(shell);
    shell.add(at(box(w, h, d, Y, { outline: 0.008 }), 0, h / 2, 0), at(box(w * 0.42, 0.05, d * 1.02, '#1C1E22'), 0, h - 0.02, 0));
    for (const s of [-1, 1]) shell.add(at(box(0.16, 0.16, d * 0.9, Y, { outline: 0.006 }), s * (w / 2 + 0.06), h - 0.1, 0));
    g.userData.update = t => { if (o.at == null) return; const u = t - o.at; shell.visible = u >= 0; if (u < 0) return;
      const f = clamp01(u / 0.12); shell.position.y = (1 - f) * 0.6; const sq = u < 0.12 ? 1 : 1 + 0.18 * Math.exp(-14 * (u - 0.12)) * Math.cos((u - 0.12) * 30); shell.scale.set(2 - sq, sq, 2 - sq); };
    g.userData.update(-1); return g;
  },

  // A plate of spaghetti held out (pivot at the plate's middle): a white plate, a yellow nest of noodles and two meatballs; o.noodle [x, y, z]
  // (local): one long noodle from the nest to that point (his mouth), slurped in between o.slurp [t0, t1] (it shortens to nothing, wobbling)
  pastaPlate(o) {
    const g = grp(), Rp = o.r ?? 0.14;
    g.add(at(cyl(Rp, Rp * 0.8, 0.025, '#F7F5EF', 20, { outline: 0.004 }), 0, 0, 0));
    for (let i = 0; i < 9; i++) { const a = i * 0.7, rr = Rp * (0.25 + 0.45 * hash(i)); const t = new THREE.Mesh(new THREE.TorusGeometry(Rp * 0.22, 0.008, 5, 14), new THREE.MeshLambertMaterial({ color: '#F2D27A' }));
      t.position.set(Math.cos(a) * rr * 0.6, 0.025 + 0.012 * (i % 3), Math.sin(a) * rr * 0.6); t.rotation.set(PI / 2 + 0.3 * (hash(i + 4) - 0.5), 0, a); g.add(t); }
    for (const x of [-0.035, 0.04]) g.add(at(sphere(0.022, '#8A3B26', 1), x, 0.06, 0.01));
    if (o.noodle) { const N = 14, segs = [], m = new THREE.MeshLambertMaterial({ color: '#F2D27A' }); for (let i = 0; i < N; i++) { const s = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 1, 5), m); g.add(s); segs.push(s); }
      const A = new THREE.Vector3(0, 0.05, 0), B = new THREE.Vector3(...o.noodle), p = new THREE.Vector3(), q = new THREE.Vector3(), d = new THREE.Vector3();
      const pt = (u, t, out) => { out.lerpVectors(A, B, u); out.y += Math.sin(u * PI) * 0.06 + 0.012 * Math.sin(u * 18 + t * 30) * (1 - u); return out; };
      g.userData.update = t => { const [t0, t1] = o.slurp || [1e9, 1e9], k = clamp01((t - t0) / (t1 - t0)), u0 = k;   // the eaten part comes off the plate end
        for (let i = 0; i < N; i++) { const ua = u0 + (1 - u0) * i / N, ub = u0 + (1 - u0) * (i + 1) / N; pt(ua, t, p); pt(ub, t, q); d.subVectors(q, p); const L = d.length(), s = segs[i];
          s.visible = k < 0.999 && L > 1e-4; s.position.copy(p).add(q).multiplyScalar(0.5); s.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize()); s.scale.set(1, L, 1); } };
      g.userData.update(0); }
    return g;
  },

  // A heap of worn-out shoes by the road (pivot at the floor middle): o.n (60) shoes, brown and black, each with a pale sole and a hole, piled in a
  // cone o.r round (0.9) and o.h high (0.8)
  shoePile(o) {
    const n = o.n ?? 60, R = o.r ?? 0.9, H = o.h ?? 0.8, g = grp(), cols = ['#5A3A24', '#2B2620', '#7A4E2C', '#3E3A36'];
    if (o.core) g.add(cyl(R * 0.06, R * 0.8, H * 0.9, '#4A3526', 12, { pivot: 'bottom' }));   // (pass 2) o.core: a dark cone inside (a big heap of few shoes stays a heap, not a scatter)
    for (let i = 0; i < n; i++) { const f = i / n, rr = R * Math.sqrt(1 - f) * (0.4 + 0.6 * hash(i + 2)), a = i * 2.399, y = H * f * 0.95;
      const sh = grp(at(box(0.26, 0.09, 0.1, cols[i % 4], { outline: 0.004 }), 0, 0.05, 0), at(box(0.27, 0.025, 0.105, '#D8CFBF'), 0, 0.0, 0), at(box(0.1, 0.05, 0.08, cols[(i + 1) % 4]), -0.07, 0.11, 0));
      sh.position.set(Math.cos(a) * rr, y, Math.sin(a) * rr); sh.rotation.set(0.5 * (hash(i + 5) - 0.5), a + hash(i) * 2, 0.6 * (hash(i + 9) - 0.5)); g.add(sh); }
    return g;
  },

  // (pass 2 of 72) An LED destination plate (pivot at its middle, front +Z): heavy amber type on a black panel in a grey frame, o.text
  // ('21  ROME'), o.w x o.h (1.2 x 0.4); it glows by itself (it reads under the shade of a roof)
  busPlate(o) {
    const w = o.w ?? 1.2, h = o.h ?? 0.4, g = grp(), tx = o.text || '21  ROME';
    const face = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#0D0E11'; c.fillRect(0, 0, W, H); c.fillStyle = '#FFB21E'; c.textAlign = 'center'; c.textBaseline = 'middle';
      let fs = H * 0.8; c.font = `900 ${fs}px Arial`; const tw = c.measureText(tx).width; if (tw > W * 0.9) { fs *= W * 0.9 / tw; c.font = `900 ${fs}px Arial`; }
      c.fillText(tx, W / 2, H * 0.55); }, { res: 1024 });
    face.material = new THREE.MeshBasicMaterial({ map: face.material.map, toneMapped: false });
    g.add(at(box(w + 0.08, h + 0.08, 0.05, '#3A3E46', { outline: 0.008 }), 0, 0, 0)); face.position.z = 0.028; g.add(face);
    return g;
  },

  // (pass 2 of 72) A cartoon-size bus ticket (pivot at its middle, front +Z, printed on both sides): pale paper o.w x o.h (0.44 x 0.32) with a
  // thick ink edge, a blue band along the top with o.title ('LIGNE') and under it o.num ('12') as big as the paper allows; it glows by itself
  busTicket(o) {
    const w = o.w ?? 0.44, h = o.h ?? 0.32, g = grp();
    const draw = (c, W, H) => { c.fillStyle = o.paper || '#FFF4CF'; c.fillRect(0, 0, W, H); c.fillStyle = o.band || '#2F62B5'; c.fillRect(0, 0, W, H * 0.3);
      c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillStyle = '#FFFFFF'; c.font = `900 ${H * 0.24}px Arial`; c.fillText(o.title || 'LIGNE', W / 2, H * 0.165);
      c.fillStyle = '#14161A'; c.font = `900 ${H * 0.66}px Arial`; c.fillText(String(o.num ?? '12'), W / 2, H * 0.67);
      c.strokeStyle = '#14161A'; c.lineWidth = H * 0.06; c.strokeRect(H * 0.03, H * 0.03, W - H * 0.06, H - H * 0.06); };
    const f = canvasPlane(w, h, draw, { res: 768 }), b = canvasPlane(w, h, draw, { res: 256 });
    for (const m of [f, b]) m.material = new THREE.MeshBasicMaterial({ map: m.material.map, toneMapped: false });
    f.position.z = 0.005; b.position.z = -0.005; b.rotation.y = PI; g.add(at(box(w + 0.02, h + 0.02, 0.006, '#14161A'), 0, 0, 0), f, b);
    return g;
  },

  // (pass 2 of 72) A wheel of legs (pivot at its hub, in the XY plane, front +Z: put it on his hips with face camera): a blurred disc o.r (0.6) in
  // the trouser colour with swirl streaks, and o.n (5) ghost legs with a shoe at the rim, turning o.rate turns a second (2.3; o.dir -1: clockwise
  // seen from the front, a run toward the right of the picture). o.at [t0, t1]: there between those times only; o.fwd: that far toward the lens
  // (0.3: in front of his real legs); o.sx: wider than tall (1.15)
  legWheel(o) {
    const R = o.r ?? 0.6, n = o.n ?? 5, g = grp(), spin = grp(), col = o.color || '#2E3442', dir = o.dir ?? -1; g.add(spin); spin.position.z = o.fwd ?? 0.3;
    const disc = canvasPlane(2 * R, 2 * R, (c, W, H) => { const gr = c.createRadialGradient(W / 2, H / 2, W * 0.05, W / 2, H / 2, W / 2); gr.addColorStop(0, col); gr.addColorStop(0.6, col + 'E6'); gr.addColorStop(1, col + '00');
      c.fillStyle = gr; c.fillRect(0, 0, W, H); c.lineCap = 'round';
      for (let i = 0; i < 10; i++) { const a0 = i * 0.66, rr = W * (0.14 + 0.3 * hash(i + 1)); c.strokeStyle = i % 2 ? 'rgba(255,255,255,0.8)' : 'rgba(16,18,24,0.65)'; c.lineWidth = W * 0.018; c.beginPath(); c.arc(W / 2, H / 2, rr, a0, a0 + 1.0 + hash(i) * 0.9); c.stroke(); } }, { res: 512 });
    disc.material = new THREE.MeshBasicMaterial({ map: disc.material.map, transparent: true, depthWrite: false, toneMapped: false, opacity: o.alpha ?? 0.95 });
    const legs = grp(); legs.position.z = 0.01; spin.add(disc, legs);
    for (let i = 0; i < n; i++) { const solid = i % 2 === 0, lg = grp();
      const lm = new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: solid ? 0.95 : 0.5, depthWrite: false, toneMapped: false }), sm = new THREE.MeshBasicMaterial({ color: o.shoe || '#111317', transparent: true, opacity: solid ? 1 : 0.6, depthWrite: false, toneMapped: false });
      const th = new THREE.Mesh(new THREE.PlaneGeometry(0.13, R * 0.8), lm), sh = new THREE.Mesh(new THREE.PlaneGeometry(0.32, 0.13), sm); th.position.y = -R * 0.45; sh.position.set(-dir * 0.1, -R * 0.9, 0.002);
      lg.add(th, sh); lg.rotation.z = i / n * TAU; legs.add(lg); }
    g.userData.update = t => { const on = !o.at || (t >= o.at[0] && t < o.at[1]); g.visible = on; if (!on) return;
      disc.rotation.z = dir * t * 11; legs.rotation.z = dir * t * TAU * (o.rate ?? 2.3); const wv = 1 + 0.04 * Math.sin(t * 43); spin.scale.set((o.sx ?? 1.15) * wv, 2 - wv, 1); };
    g.userData.update(0); return g;
  },

  // (pass 2 of 72) A calf swollen like a balloon (pivot at the knee, hanging down -Y: put it on kneeL / kneeR): an egg o.r thick (0.21) and
  // o.len long (0.5), bulging to the back, in the trouser colour (o.color), throbbing. o.tape: a yellow measuring tape round its widest part.
  // o.grow [t0, t1]: it swells from a third of its size to all of it between those times, with a bounce (full from the start without it)
  bigCalf(o) {
    const R = o.r ?? 0.21, len = o.len ?? 0.5, g = grp(), b = grp(); g.add(b); b.position.set(0, -len * 0.48, -R * 0.3);
    const egg = sphere(1, o.color || '#2E3442', 2); egg.scale.set(R, len * 0.54, R * 1.12); b.add(egg);
    if (o.tape) { const tp = new THREE.Mesh(new THREE.TorusGeometry(1, 0.1, 6, 24), new THREE.MeshLambertMaterial({ color: '#F5CE2E' })); tp.rotation.x = PI / 2; tp.scale.set(R * 1.04, R * 1.16, 0.3); b.add(tp); }
    g.userData.update = t => { let f = 1; if (o.grow) { const u = clamp01((t - o.grow[0]) / (o.grow[1] - o.grow[0])); f = 0.34 + 0.66 * (u >= 1 ? 1 + 0.12 * Math.exp(-9 * (t - o.grow[1])) * Math.cos((t - o.grow[1]) * 26) : u * u * (3 - 2 * u)); }
      const th = f * (1 + 0.04 * Math.sin(t * 11 + (o.phase ?? 0))); b.scale.set(th, 0.8 + 0.2 * f, th); };
    g.userData.update(0); return g;
  },

  // (pass 2 of 72) A small blue beacon (pivot at its foot): a dark base and a blue dome o.r (0.07) that glows by itself, a pale spot turning
  // inside it o.rate turns a second (2). It puts no light on the scene (the two alternating lamps of policeFlash strobed the whole road)
  beacon(o) {
    const R = o.r ?? 0.07, g = grp(), m = new THREE.MeshBasicMaterial({ color: '#2F7BFF', toneMapped: false });
    const dome = new THREE.Mesh(new THREE.SphereGeometry(R, 10, 6, 0, TAU, 0, PI / 2), m), spot = new THREE.Mesh(new THREE.SphereGeometry(R * 0.42, 8, 6), new THREE.MeshBasicMaterial({ color: '#D6EAFF', toneMapped: false }));
    dome.position.y = R * 0.5; g.add(at(cyl(R * 1.15, R * 1.15, R * 0.5, '#1C1E22', 10, { pivot: 'bottom' }), 0, 0, 0), dome, spot);
    g.userData.update = t => { const a = t * TAU * (o.rate ?? 2) + (o.phase ?? 0); spot.position.set(Math.cos(a) * R * 0.8, R * 0.95, Math.sin(a) * R * 0.8); m.color.set(Math.sin(a) > 0 ? '#4A93FF' : '#2466E0'); };
    g.userData.update(0); return g;
  },

  // (pass 2 of 72) One long noodle as a thick yellow rope (pivot at its first end, the plate; o.to [x, y, z] its other end, his mouth; o.r thick,
  // 0.022): it flies up from the plate to the mouth between o.rise [t0, t1], stays stretched taut and trembling until o.snap, then lets go of the
  // plate and is sucked into the mouth in o.suck s (0.16), its free end whipping
  noodleRope(o) {
    const N = 16, g = grp(), R = o.r ?? 0.022, m = new THREE.MeshLambertMaterial({ color: o.color || '#F6CF3F' }), segs = [], balls = [];
    for (let i = 0; i < N; i++) { const s = new THREE.Mesh(new THREE.CylinderGeometry(R, R, 1, 7), m); g.add(s); segs.push(s); }
    for (let i = 0; i <= N; i++) { const s = new THREE.Mesh(new THREE.SphereGeometry(R, 7, 5), m); g.add(s); balls.push(s); }
    const A = new THREE.Vector3(0, 0, 0), B = new THREE.Vector3(...(o.to || [0, 0.3, 0.3])), p = new THREE.Vector3(), q = new THREE.Vector3(), d = new THREE.Vector3(), up = new THREE.Vector3(0, 1, 0);
    const [r0, r1] = o.rise || [0, 0.15], snap = o.snap ?? 1e9, suck = o.suck ?? 0.16;
    g.userData.update = t => {
      const u1 = clamp01((t - r0) / (r1 - r0)), u0 = t < snap ? 0 : clamp01((t - snap) / suck), on = t >= r0 && u0 < 0.999 && u1 > 0.01; g.visible = on; if (!on) return;
      const sag = 0.1 * (1 - u1), trem = t >= r1 && t < snap ? 0.012 * Math.sin(t * 75) : 0, whip = u0 > 0 ? 0.14 * Math.sin(u0 * 13) * (1 - u0) : 0;
      const pt = (u, out) => { out.lerpVectors(A, B, u); out.y += Math.sin(u * PI) * (trem - sag) + whip * (1 - u); out.x += whip * 0.6 * (1 - u); return out; };
      for (let i = 0; i <= N; i++) { pt(u0 + (u1 - u0) * i / N, p); balls[i].position.copy(p); }
      for (let i = 0; i < N; i++) { pt(u0 + (u1 - u0) * i / N, p); pt(u0 + (u1 - u0) * (i + 1) / N, q); d.subVectors(q, p); const L = d.length(), s = segs[i];
        s.visible = L > 1e-4; s.position.copy(p).add(q).multiplyScalar(0.5); if (L > 1e-4) s.quaternion.setFromUnitVectors(up, d.normalize()); s.scale.set(1, Math.max(L, 1e-4), 1); } };
    g.userData.update(0); return g;
  },

  // (pass 2 of 72) The driver's big inside mirror (pivot at the top of its arm, the glass toward +Z): a dark arm o.arm long (0.14) and a mirror
  // o.w x o.h (0.6 x 0.3) in a dark frame that shows nothing but sky and a cloud: turned away from the road behind
  rearMirror(o) {
    const w = o.w ?? 0.6, h = o.h ?? 0.3, arm = o.arm ?? 0.14, g = grp();
    const glass = canvasPlane(w, h, (c, W, H) => { const gr = c.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#6FB6E6'); gr.addColorStop(1, '#CFE9F5'); c.fillStyle = gr; c.fillRect(0, 0, W, H);
      c.fillStyle = '#FFFFFF'; for (const [x, y, rr] of [[0.3, 0.6, 0.2], [0.45, 0.5, 0.26], [0.62, 0.6, 0.2], [0.78, 0.66, 0.13]]) { c.beginPath(); c.arc(W * x, H * y, H * rr, 0, TAU); c.fill(); }
      c.strokeStyle = 'rgba(255,255,255,0.7)'; c.lineWidth = H * 0.05; c.beginPath(); c.moveTo(W * 0.08, H * 0.42); c.lineTo(W * 0.2, H * 0.1); c.stroke(); }, { res: 384 });
    glass.material = new THREE.MeshBasicMaterial({ map: glass.material.map, toneMapped: false });
    g.add(at(box(0.04, arm, 0.04, '#1C1E22'), 0, -arm / 2, 0), at(box(w + 0.06, h + 0.06, 0.04, '#1C1E22', { outline: 0.006 }), 0, -arm - h / 2, 0)); glass.position.set(0, -arm - h / 2, 0.022); g.add(glass);
    return g;
  },

  // (pass 2 of 72) A mountain flank with a road that zig-zags up it (pivot at the middle of its foot, the flank rising away toward -Z at o.slope
  // rad, 0.6): a painted slab o.w wide (60) and o.up long up the slope (44): alpine green going to rock and snow at the top, a grey road in
  // o.legs hairpin legs (5) that narrow with the height, a white line along it, dark pines beside the bends
  alpSlope(o) {
    const w = o.w ?? 60, up = o.up ?? 44, legs = o.legs ?? 5, g = grp();
    const pl = canvasPlane(w, up, (c, W, H) => { const gr = c.createLinearGradient(0, H, 0, 0); gr.addColorStop(0, '#8FBF6A'); gr.addColorStop(0.5, '#9DB88C'); gr.addColorStop(0.74, '#9AA39A'); gr.addColorStop(0.9, '#E9EEF2'); gr.addColorStop(1, '#FFFFFF');
      c.fillStyle = gr; c.fillRect(0, 0, W, H);
      const pts = [[W / 2, H * 0.995]]; for (let i = 1; i <= legs; i++) { const f = i / legs, y = H * (0.995 - 0.8 * f), half = W * (0.36 - 0.2 * f); pts.push([W / 2 + (i % 2 ? 1 : -1) * half, y]); }   // the first leg leaves the middle of the foot (where the real road arrives)
      for (let i = 0; i < 46; i++) { const f = hash(i + 11), x = W * hash(i + 3), y = H * (0.95 - 0.6 * f), s = H * 0.022 * (1.2 - f * 0.7); c.fillStyle = i % 2 ? '#3E6B48' : '#4E7F52'; c.beginPath(); c.moveTo(x, y - s * 2.2); c.lineTo(x - s * 0.8, y); c.lineTo(x + s * 0.8, y); c.closePath(); c.fill(); }
      c.lineCap = 'round'; c.lineJoin = 'round';
      for (const [col, k0] of [['#6C6F74', 1.25], ['#8C8C88', 1], ['#F2F0E8', 0.08]]) for (let i = 0; i < legs; i++) { const f = (i + 0.5) / legs; c.strokeStyle = col; c.lineWidth = H * 0.05 * (1 - 0.62 * f) * k0; if (k0 < 0.5) c.setLineDash([H * 0.02, H * 0.02]); else c.setLineDash([]);
        c.beginPath(); c.moveTo(pts[i][0], pts[i][1]); c.lineTo(pts[i + 1][0], pts[i + 1][1]); c.stroke(); } }, { res: 1024 });
    pl.rotation.x = -(PI / 2 - (o.slope ?? 0.6)); pl.position.set(0, Math.sin(o.slope ?? 0.6) * up / 2, -Math.cos(o.slope ?? 0.6) * up / 2); pl.castShadow = false; g.add(pl);
    return g;
  },

  // (pass 2 of 72) A worn sole coming off a shoe (pivot at the toe, the sole running back along -Z): a pale slab o.len long (0.34) that hangs
  // open and slaps shut o.rate times a second (7) between o.at [t0, t1] (hidden outside those times)
  flapSole(o) {
    const len = o.len ?? 0.34, g = grp(), fl = grp(at(box(0.13, 0.025, len, '#E6DCC8', { outline: 0.004 }), 0, 0, -len / 2)); g.add(fl);
    g.userData.update = t => { const on = !o.at || (t >= o.at[0] && t < o.at[1]); g.visible = on; if (!on) return; fl.rotation.x = -(0.15 + 0.8 * Math.abs(Math.sin(t * PI * (o.rate ?? 7)))); };
    g.userData.update(0); return g;
  },

  // (pass 2 of 72) A brand-new shoe (pivot under its heel, the toe toward +Z): a bright red trainer o.len long (0.4) with a white sole, a white
  // toe cap and a white stripe; o.color
  newShoe(o) {
    const L = o.len ?? 0.4, C = o.color || '#E0302A', g = grp();
    g.add(at(box(0.16, 0.05, L, '#FFFFFF', { outline: 0.006 }), 0, 0.025, L / 2 - 0.06), at(box(0.15, 0.11, L * 0.92, C, { outline: 0.006 }), 0, 0.105, L / 2 - 0.07), at(box(0.15, 0.08, L * 0.42, C), 0, 0.2, 0.02),
      at(box(0.152, 0.06, L * 0.2, '#FFFFFF'), 0, 0.085, L * 0.86 - 0.06), at(box(0.155, 0.03, L * 0.3, '#FFFFFF'), 0, 0.13, L * 0.42));
    return g;
  },

  // (pass 2 of 72) An Italian café front (pivot at the middle of its foot, front +Z): an ochre wall o.w x o.h (6.5 x 4.6) with green shutters, a
  // door, a red and white striped awning on two posts over the terrace and the sign o.name ('TRATTORIA')
  trattoria(o) {
    const w = o.w ?? 6.5, h = o.h ?? 4.6, g = grp();
    g.add(at(box(w, h, 0.4, o.wall || '#E9B569', { outline: 0.012 }), 0, h / 2, -0.2), at(box(w + 0.3, 0.3, 0.6, '#C8553A'), 0, h + 0.15, -0.2), at(box(1.3, 2.9, 0.1, '#6B3F26', { outline: 0.008 }), 0, 1.45, 0.03));
    for (const x of [-w * 0.32, w * 0.32]) { g.add(at(box(1.1, 1.5, 0.06, '#DCEFF2'), x, 2.2, 0.02)); for (const s of [-1, 1]) g.add(at(box(0.5, 1.6, 0.08, '#2E7D4F', { outline: 0.006 }), x + s * 0.82, 2.2, 0.05)); }
    const aw = canvasPlane(w * 0.96, 1.9, (c, W, H) => { const n = 12; for (let i = 0; i < n; i++) { c.fillStyle = i % 2 ? '#F7F3E8' : '#D23A2E'; c.fillRect(i * W / n, 0, W / n + 1, H); } c.fillStyle = 'rgba(0,0,0,0.12)'; c.fillRect(0, H * 0.86, W, H * 0.14); }, { res: 512 });
    aw.rotation.x = -PI / 2 + 0.42; aw.position.set(0, 3.25, 0.85); g.add(aw);
    for (const x of [-w * 0.46, w * 0.46]) g.add(at(box(0.06, 2.9, 0.06, '#F4F1E8', { pivot: 'bottom' }), x, 0, 1.6));
    const sg = canvasPlane(w * 0.6, 0.62, (c, W, H) => { c.fillStyle = '#2E7D4F'; c.fillRect(0, 0, W, H); c.fillStyle = '#FFF6D8'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${H * 0.72}px Arial`; c.fillText(o.name || 'TRATTORIA', W / 2, H * 0.55); }, { res: 512 });
    sg.position.set(0, 4.05, 0.02); g.add(sg);
    return g;
  },
};
