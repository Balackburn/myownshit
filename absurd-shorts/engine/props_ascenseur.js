// « L'ascenseur » (story 76): this man called the lift twenty years ago; it never came; the neighbours feed him, the concierge brought him an
// armchair, fifteen years of works, he grew old in front of the button, which became a listed monument that schools visit; yesterday the doors
// opened on a man who had been waiting twenty years for the ground floor; they shook hands and took the stairs. Conventions as in props.js (metres,
// front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere } from './style.js';
import { grp, at, canvasPlane, rod } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const hash = i => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

export const ASCENSEUR_PROPS = {
  // A deep old armchair (front +Z): a padded seat whose top is at 0.48 (sit an actor at its foot), a tall back, two rolled arms, short turned legs,
  // in o.color with a darker piping; a crocheted doily on the back (o.doily); o.sinkAt: the seat cushion squashes as someone drops in and springs
  // back with a wobble.
  armchair(o) {
    const C = o.color || '#B5523A', D = new THREE.Color(C).multiplyScalar(0.72).getStyle(), g = grp();
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(at(cyl(0.035, 0.025, 0.12, '#5A3A22', 8, { pivot: 'bottom' }), sx * 0.33, 0, sz * 0.3));
    g.add(at(box(0.86, 0.22, 0.78, C, { pivot: 'bottom', outline: 0.008 }), 0, 0.12, 0));                                   // the base
    const cushion = grp(at(box(0.62, 0.14, 0.62, C, { outline: 0.006 }), 0, 0.07, 0)); cushion.position.set(0, 0.34, 0.06); g.add(cushion);
    g.add(at(box(0.86, 0.78, 0.18, C, { pivot: 'bottom', outline: 0.008 }), 0, 0.34, -0.3), at(cyl(0.09, 0.09, 0.86, C, 12, { outline: 0.006 }), 0, 1.12, -0.3, 0, 0, PI / 2));   // the back and its rolled top
    for (const sx of [-1, 1]) g.add(at(box(0.14, 0.26, 0.74, C, { pivot: 'bottom', outline: 0.006 }), sx * 0.36, 0.34, 0.0), at(cyl(0.08, 0.08, 0.74, C, 10, { outline: 0.005 }), sx * 0.36, 0.62, 0.0, PI / 2, 0, 0),
      at(box(0.15, 0.02, 0.02, D), sx * 0.36, 0.34, 0.375));
    if (o.doily !== false) { const d = canvasPlane(0.34, 0.24, (c, W, H) => { c.clearRect(0, 0, W, H); c.strokeStyle = '#FFFFFF'; c.fillStyle = 'rgba(255,255,255,0.85)'; c.lineWidth = W * 0.012;
        c.beginPath(); c.ellipse(W / 2, H / 2, W * 0.46, H * 0.44, 0, 0, TAU); c.stroke(); for (let k = 0; k < 18; k++) { const a = k / 18 * TAU; c.beginPath(); c.arc(W / 2 + Math.cos(a) * W * 0.42, H / 2 + Math.sin(a) * H * 0.4, W * 0.04, 0, TAU); c.fill(); }
        for (let r = 1; r < 4; r++) { c.beginPath(); c.ellipse(W / 2, H / 2, W * 0.1 * r, H * 0.1 * r, 0, 0, TAU); c.stroke(); } }, { res: 256, transparent: true });
      d.position.set(0, 1.0, -0.2); g.add(d); }
    g.userData.update = t => { const u = o.sinkAt == null ? -1 : t - o.sinkAt, a = u >= 0 && u < 0.8 ? Math.exp(-6 * u) * Math.cos(u * 22) : 0; cushion.scale.set(1 + 0.12 * Math.max(0, a), 1 - 0.45 * a, 1 + 0.12 * Math.max(0, a)); };
    g.userData.update(-1); return g;
  },

  // A jackhammer held by its T handle (pivot at the handle, the chisel down along -Y, about 0.95 m): a red body, a black hose loop, a steel chisel;
  // from o.from to o.until (s) it hammers: the body judders up and down and grit and dust spit from the tip on the floor o.floorY (-0.95) below.
  jackhammer(o) {
    const g = grp(), body = grp(); g.add(body);
    body.add(at(box(0.5, 0.05, 0.05, '#2A2C31', { outline: 0.004 }), 0, 0, 0), at(box(0.16, 0.42, 0.16, '#C8322A', { outline: 0.006 }), 0, -0.26, 0), at(cyl(0.05, 0.05, 0.2, '#3A3D44', 10), 0, -0.56, 0),
      at(cyl(0.018, 0.008, 0.32, '#B9BEC4', 8, { outline: 0.003 }), 0, -0.82, 0), at(box(0.06, 0.1, 0.04, '#2A2C31'), 0.2, -0.04, 0), at(box(0.06, 0.1, 0.04, '#2A2C31'), -0.2, -0.04, 0));
    const hose = new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.018, 6, 16, PI * 1.3), new THREE.MeshLambertMaterial({ color: '#1A1B1E' })); hose.position.set(0.12, -0.3, -0.12); hose.rotation.y = PI / 2; body.add(hose);
    const fy = o.floorY ?? -0.95, bits = []; for (let i = 0; i < 14; i++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 0), new THREE.MeshLambertMaterial({ color: i % 3 ? '#D8D2C4' : '#9A948A', transparent: true, depthWrite: false })); g.add(m); bits.push(m); }
    g.userData.update = t => { const on = o.from != null && t >= o.from && t < (o.until ?? 1e9); body.position.y = on ? 0.018 * Math.sin(t * 95) : 0; body.position.x = on ? 0.006 * Math.sin(t * 61) : 0;
      bits.forEach((m, i) => { const per = 0.5, b = (o.from ?? 0) + (i / bits.length) * per, u = on && t >= b ? ((t - b) % per) / per : -1; m.visible = u >= 0;
        if (u < 0) return; const ang = hash(i) * TAU, sp = 0.4 + 0.6 * hash(i + 7), dust = i % 2 === 0;
        m.position.set(Math.cos(ang) * sp * u * (dust ? 0.5 : 0.9), fy + (dust ? 0.6 * u : 0.5 * u - 1.4 * u * u) + 0.03, Math.sin(ang) * sp * u * (dust ? 0.5 : 0.9));
        m.scale.setScalar(dust ? 0.05 + 0.18 * u : 0.015); m.material.opacity = dust ? 0.7 * (1 - u) : 1; }); };
    g.userData.update(-1); return g;
  },

  // A cobweb across a corner (pivot at the corner, the web in the XY plane spanning +X and -Y over o.s, 0.5): radial threads and a sagging spiral,
  // pale grey; it breathes a little in the draught.
  cobweb(o) {
    const s = o.s ?? 0.5, g = grp(), web = canvasPlane(s, s, (c, W, H) => { c.clearRect(0, 0, W, H); c.strokeStyle = 'rgba(240,240,236,0.9)'; c.lineWidth = W * 0.006;
      const N = 7, R = [0.2, 0.36, 0.52, 0.68, 0.84, 1.0]; for (let k = 0; k <= N; k++) { const a = k / N * PI / 2; c.beginPath(); c.moveTo(0, 0); c.lineTo(Math.cos(a) * W, Math.sin(a) * H); c.stroke(); }
      for (const r of R) { c.beginPath(); for (let k = 0; k <= N; k++) { const a = k / N * PI / 2, sag = k > 0 && k < N + 1 ? 0.92 : 1, x = Math.cos(a) * W * r, y = Math.sin(a) * H * r;
        if (k === 0) c.moveTo(x, y); else { const am = (k - 0.5) / N * PI / 2; c.quadraticCurveTo(Math.cos(am) * W * r * sag * 0.97, Math.sin(am) * H * r * sag * 0.97, x, y); } } c.stroke(); } }, { res: 256, transparent: true });
    web.position.set(s / 2, -s / 2, 0); g.add(web);
    g.userData.update = t => { web.rotation.x = 0.06 * Math.sin(t * 1.3); };
    g.userData.update(0); return g;
  },

  // The lift car's button panel (front +Z, pivot at its middle): brushed steel, round buttons 1 to 8 and RC, o.lit ('RC') glowing orange; o.dusty: a
  // grey bloom of dust over it and a cobweb in its corner.
  liftPanel(o) {
    const w = o.w ?? 0.26, h = o.h ?? 0.62, g = grp(at(box(w, h, 0.02, '#B9C0C7', { outline: 0.004 }), 0, 0, 0)), labels = ['8', '7', '6', '5', '4', '3', '2', '1', 'RC'];
    labels.forEach((L, i) => { const x = (i % 2 ? 0.055 : -0.055) * (L === 'RC' ? 0 : 1), y = h / 2 - 0.08 - i * (h - 0.14) / 8.5, lit = L === (o.lit ?? 'RC');
      const b = at(cyl(0.028, 0.028, 0.012, lit ? '#FFB02E' : '#8E97A1', 14, lit ? { emissive: '#FF8A10', noGrain: true } : {}), x, y, 0.016, PI / 2, 0, 0); g.add(b);
      const t = canvasPlane(0.05, 0.05, (c, W, H) => { c.clearRect(0, 0, W, H); c.fillStyle = lit ? '#3A1A00' : '#1E2228'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${H * (L.length > 1 ? 0.42 : 0.6)}px Arial`; c.fillText(L, W / 2, H * 0.55); }, { res: 64, transparent: true });
      t.position.set(x, y, 0.024); g.add(t); });
    if (o.dusty) { const d = canvasPlane(w, h, (c, W, H) => { const gr = c.createRadialGradient(W * 0.4, H * 0.6, W * 0.05, W * 0.5, H * 0.5, W * 0.9); gr.addColorStop(0, 'rgba(150,140,125,0.15)'); gr.addColorStop(1, 'rgba(120,110,95,0.55)'); c.fillStyle = gr; c.fillRect(0, 0, W, H); }, { res: 128, transparent: true });
      d.position.z = 0.03; g.add(d); const cw = ASCENSEUR_PROPS.cobweb({ s: 0.16 }); cw.position.set(-w / 2, h / 2, 0.034); g.add(cw); }
    return g;
  },

  // A museum spotlight's beam (pivot at the lamp, the beam down along -Y): a translucent warm cone o.h (2.2) long, o.r (0.45) wide at its foot, and a
  // small black lamp housing at the top.
  lightCone(o) {
    const h = o.h ?? 2.2, r = o.r ?? 0.45, g = grp(at(cyl(0.07, 0.09, 0.16, '#1E2024', 10, { outline: 0.004 }), 0, 0, 0));
    const geo = new THREE.ConeGeometry(r, h, 24, 1, true); geo.translate(0, -h / 2, 0);
    g.add(new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: o.color || '#FFE9B0', transparent: true, opacity: o.opacity ?? 0.22, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending })));
    return g;
  },

  // A lift call button big enough for an insert (front +Z, pivot at its middle): a steel plate with a round button in a ring and an arrow; o.pressAt:
  // the button sinks for 0.25 s and its ring lights orange from then on (o.litAfter: lit from that time without a press).
  callButton(o) {
    const g = grp(at(box(0.12, 0.18, 0.02, '#A8B0B8', { outline: 0.004 }), 0, 0, 0)), ring = at(cyl(0.036, 0.036, 0.008, '#5A6068', 18), 0, 0.01, 0.012, PI / 2, 0, 0);
    const lit = at(cyl(0.038, 0.038, 0.009, '#FFB02E', 18, { emissive: '#FF8A10', noGrain: true }), 0, 0.01, 0.012, PI / 2, 0, 0); lit.visible = false;
    const b = at(cyl(0.026, 0.026, 0.02, '#E8ECEF', 18, { outline: 0.003 }), 0, 0.01, 0.02, PI / 2, 0, 0); g.add(ring, lit, b);
    const arrow = canvasPlane(0.05, 0.04, (c, W, H) => { c.clearRect(0, 0, W, H); c.fillStyle = '#1E2228'; c.beginPath(); c.moveTo(W / 2, H * 0.1); c.lineTo(W * 0.85, H * 0.9); c.lineTo(W * 0.15, H * 0.9); c.closePath(); c.fill(); }, { res: 64, transparent: true });
    arrow.position.set(0, -0.055, 0.012); arrow.rotation.z = PI; g.add(arrow);
    g.userData.update = t => { const p = o.pressAt != null && t >= o.pressAt, d = p && t < o.pressAt + 0.25; b.position.z = d ? 0.012 : 0.02; lit.visible = p || (o.litAfter != null && t >= o.litAfter); ring.visible = !lit.visible; };
    g.userData.update(-1); return g;
  },
};
