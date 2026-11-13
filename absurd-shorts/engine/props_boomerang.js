// « Le boomerang » (story 52, cycle 14): a man threw a boomerang ten years ago; it never came back; the lost-property office refused his declaration
// (a boomerang is not lost: it comes back); the air-traffic controllers opened it a corridor; planes give way to it; yesterday it came back, right in
// the middle of his wedding photo; he left with it; his wife waits for him, ten years. Conventions as in props.js (metres, front +Z, pivot at the floor
// unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, ease, clamp01 } from './style.js';
import { grp, at, label, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const rnd = s => { let x = Math.sin(s * 127.1) * 43758.5453; return x - Math.floor(x); };
const wob = (u, f, d) => u < 0 ? 0 : Math.exp(-u * d) * Math.sin(u * f);
const list = v => [].concat(v ?? []);
// the integral of a piecewise-linear rate given as [[t, rate], ...] (turns per second): how many turns by time t
function turnsAt(ks, t) {
  if (!ks || !ks.length) return 0;
  let acc = 0;
  for (let i = 0; i < ks.length; i++) {
    const [t0, r0] = ks[i], [t1, r1] = ks[i + 1] || [Infinity, r0];
    if (t <= t0) break;
    const te = Math.min(t, t1), u = (te - t0) / Math.max(1e-6, t1 - t0), rEnd = Number.isFinite(t1) ? r0 + (r1 - r0) * u : r0;
    acc += (r0 + rEnd) / 2 * (te - t0);
    if (t <= t1) break;
  }
  return acc;
}
const rateAt = (ks, t) => { if (!ks || !ks.length) return 0; if (t <= ks[0][0]) return 0; for (let i = 0; i < ks.length - 1; i++) { const [t0, r0] = ks[i], [t1, r1] = ks[i + 1]; if (t < t1) return r0 + (r1 - r0) * (t - t0) / Math.max(1e-6, t1 - t0); } return ks[ks.length - 1][1]; };
// a canvas redrawn when its key changes (a radar sweep)
function liveCanvas(w, h, res, opts = {}) {
  const c = document.createElement('canvas'); c.width = res; c.height = Math.max(8, Math.round(res * h / w));
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const m = new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide, toneMapped: false, transparent: !!opts.transparent, alphaTest: opts.transparent ? 0.05 : 0 });
  const pl = new THREE.Mesh(new THREE.PlaneGeometry(w, h), m); pl.userData.noAO = true;
  let last = null;
  const redraw = (key, fn) => { if (key === last) return; last = key; fn(c.getContext('2d'), c.width, c.height); tex.needsUpdate = true; };
  return { pl, redraw };
}

export const BOOMERANG_PROPS = {
  // A wooden boomerang lying flat (in XZ, pivot at its centre of spin, the elbow toward +Z): two arms o.arm (0.32 m) long, o.w (0.075) wide, o.t
  // (0.02) thick, opening at o.angle (1.95 rad), painted bands. o.spin [[t, turns per second], ...]: the spin from each time (linear between, the turns
  // integrated, so slowing down never runs it backwards); from 2.5 turns/s two ghost copies trail it (a smear); o.wobble (rad): the disc rocks as it
  // spins; o.color ('#C8894A'), o.bands (['#C8202A', '#F2C80F']).
  boomerang(o) {
    const L = o.arm ?? 0.32, W = o.w ?? 0.075, T = o.t ?? 0.02, A = o.angle ?? 1.95, C = o.color || '#C8894A', bands = o.bands || ['#C8202A', '#F2C80F'];
    const ex = (L / 2) * Math.cos(A / 2);   // the elbow sits so that the centre of the two arms is the pivot
    const build = (ghost) => {
      const g = grp(), m = ghost ? new THREE.MeshBasicMaterial({ color: C, transparent: true, opacity: ghost, depthWrite: false }) : null;
      for (const s of [-1, 1]) {
        const d = [s * Math.sin(A / 2), -Math.cos(A / 2)], arm = grp();
        const a = ghost ? new THREE.Mesh(new THREE.BoxGeometry(L, T, W), m) : box(L, T, W, C, { outline: 0.004 });
        arm.add(a);
        if (!ghost) { arm.add(at(cyl(W / 2, W / 2, T, C, 10), L / 2, 0, 0));   // the rounded tip
          bands.forEach((bc, i) => arm.add(at(box(0.022, T + 0.002, W + 0.002, bc), -L * 0.05 + i * 0.05, 0, 0))); arm.add(at(box(0.03, T + 0.002, W + 0.002, '#2A1C12'), L * 0.38, 0, 0)); }
        arm.position.set(d[0] * L / 2, 0, ex + d[1] * L / 2); arm.rotation.y = Math.atan2(-d[1], d[0]); g.add(arm);
      }
      g.add(ghost ? new THREE.Mesh(new THREE.CylinderGeometry(W / 2, W / 2, T, 10), m) : cyl(W / 2, W / 2, T, C, 10)); g.children[g.children.length - 1].position.z = ex;   // the elbow
      g.traverse(q => { if (q.isMesh) { q.castShadow = !ghost; q.position.y = q.position.y; } }); return g;
    };
    const body = build(0), gh = [build(0.32), build(0.16)], spin = grp(body, ...gh), g = grp(spin);
    g.userData.update = t => { const turns = turnsAt(o.spin, t), r = Math.abs(rateAt(o.spin, t)), a = -TAU * turns;
      body.rotation.y = a; gh.forEach((q, i) => { q.visible = r > 2.5; q.rotation.y = a + (i + 1) * 0.32 * Math.sign(turns || 1); });
      spin.rotation.x = (o.wobble || 0) * Math.sin(a * 0.5); spin.rotation.z = (o.wobble || 0) * 0.6 * Math.cos(a * 0.5); };
    g.userData.update(0); return g;
  },

  // A lost-property declaration (front +Z, pivot at its centre): an A4 sheet o.s (1: 0.21 x 0.297 m) with DÉCLARATION DE PERTE, its lines (Objet :
  // boomerang, Perdu le, Lieu), a pencil sketch of a boomerang with an arrow going away, and o.stamp { text ('REFUSÉ'), at, rot }: the stamp slams on at
  // that time (from 1.6 times its size to 1 in 0.06 s, a jolt of the sheet).
  lossForm(o) {
    const s = o.s ?? 1, w = 0.21 * s, h = 0.297 * s, g = grp();
    const face = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FBFAF4'; c.fillRect(0, 0, W, H); c.fillStyle = '#1B2A6B'; c.textAlign = 'center'; c.font = `900 ${H * 0.055}px Arial`; c.fillText('DÉCLARATION', W / 2, H * 0.09); c.fillText('DE PERTE', W / 2, H * 0.155);
      c.textAlign = 'left'; c.font = `bold ${H * 0.04}px Arial`; c.fillStyle = '#26262A';
      [['Objet :', 'boomerang'], ['Perdu le :', 'il y a dix ans'], ['Lieu :', 'le parc']].forEach(([a, b], i) => { const y = H * (0.25 + i * 0.075); c.fillText(a, W * 0.08, y); c.fillStyle = '#2F4FA8'; c.font = `italic ${H * 0.042}px Arial`; c.fillText(b, W * 0.4, y); c.fillStyle = '#26262A'; c.font = `bold ${H * 0.04}px Arial`;
        c.strokeStyle = 'rgba(40,40,60,0.35)'; c.lineWidth = H * 0.003; c.beginPath(); c.moveTo(W * 0.38, y + H * 0.012); c.lineTo(W * 0.92, y + H * 0.012); c.stroke(); });
      // the sketch: a boomerang and a dashed arrow flying off (no return)
      c.save(); c.translate(W * 0.36, H * 0.62); c.rotate(-0.3); c.strokeStyle = '#6A4A2A'; c.fillStyle = '#E2B07A'; c.lineWidth = H * 0.008; c.beginPath(); c.moveTo(-W * 0.16, -H * 0.06); c.quadraticCurveTo(0, H * 0.06, W * 0.16, -H * 0.06); c.lineTo(W * 0.13, -H * 0.085); c.quadraticCurveTo(0, H * 0.02, -W * 0.13, -H * 0.085); c.closePath(); c.fill(); c.stroke(); c.restore();
      c.strokeStyle = '#2F4FA8'; c.setLineDash([H * 0.02, H * 0.015]); c.lineWidth = H * 0.006; c.beginPath(); c.moveTo(W * 0.55, H * 0.58); c.quadraticCurveTo(W * 0.75, H * 0.46, W * 0.9, H * 0.52); c.stroke(); c.setLineDash([]);
      c.beginPath(); c.moveTo(W * 0.9, H * 0.52); c.lineTo(W * 0.85, H * 0.49); c.moveTo(W * 0.9, H * 0.52); c.lineTo(W * 0.86, H * 0.555); c.stroke();
      c.fillStyle = '#26262A'; c.font = `${H * 0.032}px Arial`; c.fillText('Signature :', W * 0.08, H * 0.88); c.strokeStyle = '#2F4FA8'; c.beginPath(); c.moveTo(W * 0.42, H * 0.885); for (let i = 0; i < 6; i++) c.lineTo(W * (0.45 + i * 0.07), H * (0.86 + (i % 2) * 0.04)); c.stroke(); }, { res: 512 });
    g.add(at(box(w, h, 0.003, '#F4F2EA'), 0, 0, -0.002), face); face.position.z = 0.0025;
    if (o.stamp) { const S = o.stamp, sw = w * 0.82, sh = sw * 0.34, col = S.color || '#C8202A';
      const sm = canvasPlane(sw, sh, (c, W, H) => { c.clearRect(0, 0, W, H); c.strokeStyle = c.fillStyle = col; c.lineWidth = H * 0.09; c.strokeRect(H * 0.07, H * 0.07, W - H * 0.14, H * 0.86); c.font = `900 ${H * 0.56}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(S.text || 'REFUSÉ', W / 2, H * 0.53); }, { res: 512, transparent: true });
      sm.position.set(0, (S.y ?? 0.05) * s, 0.006); sm.rotation.z = S.rot ?? -0.18; g.add(sm);
      g.userData.update = t => { const u = t - (S.at ?? 0); sm.visible = u >= 0; if (u < 0) return; const k = u < 0.06 ? 1.6 - 0.6 * (u / 0.06) : 1 + 0.06 * wob(u - 0.06, 40, 9); sm.scale.setScalar(k); g.position.y = (u < 0.12 ? -0.006 * Math.sin(u / 0.12 * PI) : 0); };
      g.userData.update(0); }
    return g;
  },

  // The shelves of a lost-property office (front +Z, pivot at the floor): a grey metal unit o.w (1.8 m) x o.h (2.0) with four shelves of things people
  // lost: umbrellas, hats, a teddy bear, odd shoes, gloves, a rubber duck, keys, a bicycle wheel; o.sign ('OBJETS TROUVÉS') on a board on top.
  lostShelf(o) {
    const w = o.w ?? 1.8, h = o.h ?? 2.0, d = 0.45, g = grp(), M = '#8C949B', n = 4;
    for (const x of [-w / 2, w / 2]) g.add(at(box(0.04, h, d, M, { pivot: 'bottom', outline: 0.004 }), x, 0, 0));
    for (let i = 0; i <= n; i++) g.add(at(box(w, 0.03, d, M, { outline: 0.004 }), 0, 0.12 + i * (h - 0.15) / n, 0));
    const shelfY = i => 0.135 + i * (h - 0.15) / n, cols = ['#C8202A', '#2F6FB5', '#2E8A4E', '#F2C80F', '#7A3E9C', '#1B1B1E'];
    // shelf 0: shoes and a duck; 1: hats; 2: umbrellas; 3: a teddy, gloves, keys; (top) a bicycle wheel
    for (let k = 0; k < 4; k++) g.add(at(box(0.11, 0.07, 0.26, cols[(k * 2) % 6], { pivot: 'bottom', outline: 0.004 }), -w / 2 + 0.25 + k * 0.32, shelfY(0), 0.02, 0, (rnd(k) - 0.5) * 0.8, 0));
    g.add(at(new THREE.Mesh(new THREE.SphereGeometry(0.07, 8, 6), mat('#F2C80F')), w / 2 - 0.3, shelfY(0) + 0.07, 0.05), at(new THREE.Mesh(new THREE.SphereGeometry(0.045, 8, 6), mat('#F2C80F')), w / 2 - 0.25, shelfY(0) + 0.16, 0.08), at(box(0.05, 0.02, 0.04, '#E8811A'), w / 2 - 0.21, shelfY(0) + 0.16, 0.12));
    for (let k = 0; k < 4; k++) { const x = -w / 2 + 0.28 + k * 0.42, c = cols[(k + 1) % 6]; g.add(at(cyl(0.13, 0.13, 0.02, c, 12), x, shelfY(1) + 0.01, 0), at(cyl(0.08, 0.09, 0.1, c, 12, { pivot: 'bottom', outline: 0.004 }), x, shelfY(1) + 0.02, 0)); }
    for (let k = 0; k < 6; k++) { const x = -w / 2 + 0.2 + k * 0.27, c = cols[k % 6]; g.add(at(cyl(0.025, 0.06, 0.62, c, 8, { outline: 0.004 }), x, shelfY(2) + 0.06, 0.02, 0, 0, PI / 2 - 0.15 + rnd(k + 3) * 0.3)); }
    const bear = grp(at(new THREE.Mesh(new THREE.SphereGeometry(0.12, 8, 6), mat('#A0683A')), 0, 0.12, 0), at(new THREE.Mesh(new THREE.SphereGeometry(0.085, 8, 6), mat('#A0683A')), 0, 0.3, 0.01),
      at(new THREE.Mesh(new THREE.SphereGeometry(0.035, 6, 4), mat('#A0683A')), -0.06, 0.38, 0), at(new THREE.Mesh(new THREE.SphereGeometry(0.035, 6, 4), mat('#A0683A')), 0.06, 0.38, 0), at(new THREE.Mesh(new THREE.SphereGeometry(0.03, 6, 4), mat('#E8C8A0')), 0, 0.29, 0.085));
    bear.position.set(-w / 2 + 0.3, shelfY(3), 0.02); g.add(bear);
    for (let k = 0; k < 3; k++) g.add(at(box(0.09, 0.025, 0.17, ['#C8202A', '#1B1B1E', '#2F6FB5'][k], { pivot: 'bottom' }), 0.05 + k * 0.17, shelfY(3), 0.03, 0, (rnd(k + 9) - 0.5) * 0.9, 0));
    g.add(at(cyl(0.03, 0.03, 0.01, '#C9A13A', 10), w / 2 - 0.25, shelfY(3) + 0.01, 0.05), at(box(0.07, 0.008, 0.02, '#C9A13A'), w / 2 - 0.2, shelfY(3) + 0.01, 0.05));
    const wheel = grp(new THREE.Mesh(new THREE.TorusGeometry(0.3, 0.02, 6, 20), mat('#2A2A2E'))); for (let k = 0; k < 6; k++) wheel.add(at(box(0.008, 0.6, 0.008, '#B9BEC4'), 0, 0, 0, 0, 0, k * PI / 6)); wheel.position.set(w / 2 - 0.4, h + 0.2, -0.05); wheel.rotation.z = 0.15; g.add(wheel);
    if (o.sign !== '') g.add(at(label(o.sign || 'OBJETS TROUVÉS', w * 0.62, 0.24, { bg: '#1D3F8A', fg: '#FFFFFF', wrap: false }), -0.25, h + 0.16, d / 2 + 0.01));
    return g;
  },

  // An air-traffic radar scope on its console (front +Z, pivot at the floor): a dark console o.w (0.9 m) wide, a round green screen o.r (0.3) tilted
  // toward the operator, range rings, the sweep turning with its afterglow, a few blips, and the boomerang's route: a big dashed loop labelled
  // o.tag ('BOOMERANG') with a bright blip running round it; o.corridor (t): from then on two solid parallel lines are drawn along the loop in 0.5 s
  // (the corridor); o.label (a small plate on the console).
  radarScope(o) {
    const W = o.w ?? 0.9, R = o.r ?? 0.3, g = grp(), scr = liveCanvas(2 * R, 2 * R, 512, { transparent: true });
    if (o.wall) {   // (first look) o.wall: a big round screen on the wall facing +Z (pivot at its centre), in a dark square bezel: on a console the screen faced its operator, away from any camera that saw his face
      g.add(at(box(2.3 * R, 2.3 * R, 0.06, '#2A2F35', { outline: 0.008 }), 0, 0, -0.03), scr.pl, at(new THREE.Mesh(new THREE.TorusGeometry(R * 1.02, 0.03, 6, 40), mat('#1B1E22')), 0, 0, 0.012));
      scr.pl.position.z = 0.008;
      if (o.label) g.add(at(label(o.label, R * 1.2, R * 0.16, { bg: '#1B1B1E', fg: '#E8E8E8', wrap: false }), 0, -1.27 * R, 0.01));
    } else {
      g.add(at(box(W, 0.95, 0.6, '#3A4048', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(W, 0.06, 0.66, '#2A2F35'), 0, 0.98, 0.02));
      scr.pl.position.set(0, 1.12, 0.12); scr.pl.rotation.x = -0.75; g.add(scr.pl);
      g.add(at(new THREE.Mesh(new THREE.TorusGeometry(R * 1.02, 0.025, 6, 32), mat('#22262B')), 0, 1.12, 0.12, -0.75, 0, 0));
      g.add(at(box(W * 0.9, 0.2, 0.25, '#30363D', { outline: 0.004 }), 0, 1.06, -0.12, -0.75, 0, 0));
      for (let i = 0; i < 6; i++) g.add(at(box(0.04, 0.02, 0.04, ['#C8202A', '#F2C80F', '#2E8A4E'][i % 3]), -W / 2 + 0.12 + i * 0.13, 1.0, 0.27));
      if (o.label) g.add(at(label(o.label, W * 0.5, 0.08, { bg: '#1B1B1E', fg: '#E8E8E8', wrap: false }), 0, 0.8, 0.305));
    }
    const route = th => [Math.cos(th) * 0.62 - 0.05, Math.sin(th) * 0.38 + 0.08 * Math.sin(2 * th)];   // a looping route in screen units (-1..1)
    g.userData.update = t => scr.redraw(Math.round(t * 30), (c, Wc, Hc) => { const cx = Wc / 2, cy = Hc / 2, r = Wc * 0.48; c.clearRect(0, 0, Wc, Hc);
      c.fillStyle = '#0C2A1A'; c.beginPath(); c.arc(cx, cy, r, 0, TAU); c.fill(); c.save(); c.beginPath(); c.arc(cx, cy, r, 0, TAU); c.clip();
      c.strokeStyle = 'rgba(90,230,140,0.35)'; c.lineWidth = Wc * 0.004; for (const k of [0.33, 0.66, 1]) { c.beginPath(); c.arc(cx, cy, r * k, 0, TAU); c.stroke(); } c.beginPath(); c.moveTo(cx - r, cy); c.lineTo(cx + r, cy); c.moveTo(cx, cy - r); c.lineTo(cx, cy + r); c.stroke();
      const sw = t * 2.2; for (let i = 0; i < 18; i++) { const a = sw - i * 0.045; c.strokeStyle = `rgba(120,255,160,${0.5 * (1 - i / 18)})`; c.lineWidth = Wc * 0.01; c.beginPath(); c.moveTo(cx, cy); c.lineTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r); c.stroke(); }
      for (let i = 0; i < 4; i++) { const a = rnd(i) * TAU, d = r * (0.3 + 0.6 * rnd(i + 5)); c.fillStyle = 'rgba(160,255,190,0.8)'; c.fillRect(cx + Math.cos(a) * d - 3, cy + Math.sin(a) * d - 3, 6, 6); }
      c.strokeStyle = '#FFD54A'; c.lineWidth = Wc * 0.012; c.setLineDash([Wc * 0.03, Wc * 0.022]); c.beginPath(); for (let j = 0; j <= 64; j++) { const [x, y] = route(j / 64 * TAU); j ? c.lineTo(cx + x * r, cy + y * r) : c.moveTo(cx + x * r, cy + y * r); } c.stroke(); c.setLineDash([]);
      if (o.corridor != null && t >= o.corridor) { const k = Math.min(1, (t - o.corridor) / 0.5); c.strokeStyle = '#FFFFFF'; c.lineWidth = Wc * 0.008;
        for (const off of [-0.07, 0.07]) { c.beginPath(); for (let j = 0; j <= Math.round(64 * k); j++) { const th = j / 64 * TAU, [x, y] = route(th), [x2, y2] = route(th + 0.01), nx = -(y2 - y), ny = x2 - x, nl = Math.hypot(nx, ny) || 1; const px = cx + (x + off * nx / nl) * r, py = cy + (y + off * ny / nl) * r; j ? c.lineTo(px, py) : c.moveTo(px, py); } c.stroke(); } }
      const [bx, by] = route(t * 1.3); c.fillStyle = '#FFE680'; c.beginPath(); c.arc(cx + bx * r, cy + by * r, Wc * 0.025, 0, TAU); c.fill();
      c.font = `900 ${Wc * 0.07}px Arial`; c.fillStyle = '#FFE680'; c.textAlign = 'left'; c.fillText(o.tag || 'BOOMERANG', cx + bx * r + Wc * 0.04, cy + by * r - Wc * 0.03);
      c.restore(); });
    g.userData.update(0); return g;
  },

  // An orange traffic cone with two white bands (pivot at its foot): o.h (0.75 m); o.puff: a little cloud under it (it stands on the clouds)
  skyCone(o) {
    const H = o.h ?? 0.75, g = grp(at(box(H * 0.55, 0.04, H * 0.55, '#E8661A', { pivot: 'bottom', outline: 0.004 }), 0, 0, 0), at(cyl(H * 0.04, H * 0.22, H, '#F07A22', 12, { pivot: 'bottom', outline: 0.005 }), 0, 0.03, 0));
    for (const y of [0.42, 0.65]) g.add(at(cyl(H * (0.22 - 0.18 * y) + 0.004, H * (0.22 - 0.18 * (y - 0.09)) + 0.004, H * 0.09, '#F4F2EA', 12), 0, 0.03 + H * y, 0));
    if (o.puff) for (let i = 0; i < 4; i++) g.add(at(new THREE.Mesh(new THREE.SphereGeometry(0.16 + 0.06 * rnd(i), 7, 5), mat('#FFFFFF')), (rnd(i + 2) - 0.5) * 0.4, -0.05, (rnd(i + 7) - 0.5) * 0.3));
    return g;
  },

  // A zebra crossing floating on the clouds (pivot at its middle, lying flat): o.w (across, 3 m) x o.l (along, 2 m), white bars on nothing
  skyCrossing(o) {
    const w = o.w ?? 3, L = o.l ?? 2, n = o.n ?? 6, g = grp(), bw = w / (2 * n - 1);
    for (let i = 0; i < n; i++) g.add(at(box(bw, 0.03, L, '#FBFBF6', { outline: 0.004 }), -w / 2 + bw / 2 + i * 2 * bw, 0, 0));
    return g;
  },

  // An old wooden plate camera on a tripod (front +Z, pivot at the floor): the back box o.h (1.45 m) up, black bellows, a brass lens; a black cloth
  // hanging from the back (the photographer's head goes under it: o.cloth); o.flashAt (t): a flash tray raised on a rod fires a white burst.
  bellowsCamera(o) {
    const H = o.h ?? 1.45, g = grp();
    for (let i = 0; i < 3; i++) { const a = i * TAU / 3 + 0.4; g.add(at(cyl(0.015, 0.02, H, '#8A5A32', 6), Math.sin(a) * 0.2, H / 2 - 0.02, Math.cos(a) * 0.2, Math.cos(a) * 0.14, 0, -Math.sin(a) * 0.14)); }
    g.add(at(box(0.3, 0.3, 0.12, '#A8713E', { outline: 0.005 }), 0, H + 0.12, -0.12));
    for (let i = 0; i < 4; i++) g.add(at(box(0.27 - i * 0.03, 0.27 - i * 0.03, 0.07, i % 2 ? '#1B1B1E' : '#2A2A2E', { outline: 0.003 }), 0, H + 0.12, -0.02 + i * 0.065));
    g.add(at(box(0.18, 0.18, 0.03, '#A8713E', { outline: 0.004 }), 0, H + 0.12, 0.24), at(cyl(0.055, 0.055, 0.1, '#C9A13A', 12), 0, H + 0.12, 0.3, PI / 2, 0, 0), at(cyl(0.04, 0.04, 0.005, '#7FA6CC', 12), 0, H + 0.12, 0.353, PI / 2, 0, 0));
    if (o.cloth !== false) g.add(at(box(0.42, 0.62, 0.02, '#141416', { outline: 0.004 }), 0, H - 0.08, -0.2));
    if (o.flashAt != null) { const rod = grp(at(cyl(0.01, 0.01, 0.5, '#2A2A2E', 6), 0, 0.25, 0), at(box(0.2, 0.02, 0.06, '#5A5F66'), 0, 0.5, 0)); rod.position.set(0.25, H + 0.1, -0.1); g.add(rod);
      const burst = new THREE.Mesh(new THREE.SphereGeometry(0.18, 10, 8), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.95, toneMapped: false, depthWrite: false })); burst.position.set(0.25, H + 0.62, -0.1); g.add(burst);
      g.userData.update = t => { const u = t - o.flashAt; const on = u >= 0 && u < 0.25; burst.visible = on; if (on) { burst.scale.setScalar(0.4 + 3.2 * Math.min(1, u / 0.05)); burst.material.opacity = 0.95 * (1 - u / 0.25); } };
      g.userData.update(0); }
    return g;
  },

  // A bride's bouquet (pivot at the hand, the stems down): a dome of white and pink flowers on green stems, a white ribbon
  bouquet(o) {
    const g = grp(at(cyl(0.03, 0.02, 0.18, '#4E8A3A', 6), 0, -0.08, 0), at(box(0.07, 0.03, 0.07, '#FFFFFF'), 0, 0.0, 0));
    for (let i = 0; i < 9; i++) { const a = i * 2.399, r = i ? 0.06 + 0.02 * (i % 3) : 0; g.add(at(new THREE.Mesh(new THREE.IcosahedronGeometry(0.04, 0), mat(i % 3 ? '#FFFFFF' : '#F4A6C0')), Math.cos(a) * r, 0.06 + (i ? 0.0 : 0.03), Math.sin(a) * r)); }
    return g;
  },
};
