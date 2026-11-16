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
    // (pass 3) the lit button is called out the way the call button is in the hall: a wide amber ring that breathes and a halo round it (a fingertip
    // on the button hid the only lit thing), and its name on a plate under it, clear of a hand that comes in from either side
    const yR = h / 2 - 0.08 - 8 * (h - 0.14) / 8.5, isRC = (o.lit ?? 'RC') === 'RC';
    const ringR = at(cyl(0.064, 0.064, 0.008, '#FFB02E', 22, { emissive: '#FF8A10', noGrain: true }), 0, yR, 0.0125, PI / 2, 0, 0);
    const haloR = new THREE.Mesh(new THREE.CircleGeometry(0.12, 24), new THREE.MeshBasicMaterial({ color: '#FF9A2E', transparent: true, opacity: 0.4, blending: THREE.AdditiveBlending, depthWrite: false })); haloR.position.set(0, yR, 0.0112);
    const tag = canvasPlane(0.07, 0.05, (c, W, H) => { c.fillStyle = '#F2EFE6'; c.fillRect(0, 0, W, H); c.strokeStyle = '#1E2228'; c.lineWidth = H * 0.08; c.strokeRect(H * 0.04, H * 0.04, W - H * 0.08, H - H * 0.08); c.fillStyle = '#1E2228'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${H * 0.66}px Arial`; c.fillText('RC', W / 2, H * 0.56); }, { res: 128 });
    tag.position.set(0, yR - 0.1, 0.0115);
    if (isRC) g.add(ringR, haloR, tag);
    if (o.dusty) { const d = canvasPlane(w, h, (c, W, H) => { const gr = c.createRadialGradient(W * 0.4, H * 0.6, W * 0.05, W * 0.5, H * 0.5, W * 0.9); gr.addColorStop(0, 'rgba(150,140,125,0.15)'); gr.addColorStop(1, 'rgba(120,110,95,0.55)'); c.fillStyle = gr; c.fillRect(0, 0, W, H);
        c.globalCompositeOperation = 'destination-out'; c.beginPath(); c.ellipse(W * 0.5, H * (0.5 - (yR - 0.03) / h), W * 0.34, W * 0.42, 0, 0, TAU); c.fill(); c.globalCompositeOperation = 'source-over'; }, { res: 128, transparent: true });   /* twenty years of one finger: no dust round the button and its name */
      d.position.z = 0.03; g.add(d); const cw = ASCENSEUR_PROPS.cobweb({ s: 0.16 }); cw.position.set(-w / 2, h / 2, 0.034); g.add(cw); }
    g.userData.update = t => { const pu = 0.5 + 0.5 * Math.sin(t * 5.5); ringR.scale.set(1 + 0.1 * pu, 1, 1 + 0.1 * pu); haloR.material.opacity = 0.3 + 0.3 * pu; };
    g.userData.update(0);
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
    // (pass 3) the arrow points up (a call from the ground floor goes up; it pointed down: o.arrow 'down' keeps that); once lit the ring breathes and
    // throws an amber halo on the plate and the wall round it (o.pulse false: steady), so the lit button reads from across the hall and a held
    // insert on it is never a still picture
    arrow.position.set(0, -0.055, 0.012); arrow.rotation.z = o.arrow === 'down' ? PI : 0; g.add(arrow);
    const halo = new THREE.Mesh(new THREE.CircleGeometry(0.072, 24), new THREE.MeshBasicMaterial({ color: '#FF9A2E', transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false }));
    halo.position.set(0, 0.01, 0.0108); g.add(halo);
    g.userData.update = t => { const p = o.pressAt != null && t >= o.pressAt, d = p && t < o.pressAt + 0.25; b.position.z = d ? 0.012 : 0.02; lit.visible = p || (o.litAfter != null && t >= o.litAfter); ring.visible = !lit.visible;
      const pu = lit.visible && o.pulse !== false ? 0.5 + 0.5 * Math.sin((t - (o.pressAt ?? o.litAfter ?? 0)) * 5.5 - PI / 2) : 0; lit.scale.set(1 + 0.12 * pu, 1, 1 + 0.12 * pu); halo.material.opacity = lit.visible ? 0.2 + 0.26 * pu : 0; };
    g.userData.update(-1); return g;
  },

  // (pass 3) A tiled floor laid over the set's (pivot at the foot of the back wall, the floor running out along +Z): terracotta slabs o.w (6.8) wide
  // and o.d (16) deep with darker joints every o.tile (0.6) m. The hall set reads its floor display from the option that also names its floor
  // colour, so its tiles came out near white (luma 0.87) and the white captions sat on them.
  tileFloor(o) {
    const w = o.w ?? 6.8, d = o.d ?? 16, s = o.tile ?? 0.6, J = o.joint || '#72604F', g = grp(at(box(w, 0.008, d, o.color || '#988474'), 0, 0.005, d / 2));
    for (let x = -Math.floor(w / 2 / s) * s; x <= w / 2 - 0.01; x += s) g.add(at(box(0.022, 0.003, d, J), x, 0.0095, d / 2));
    for (let z = s / 2; z < d; z += s) g.add(at(box(w, 0.003, 0.022, J), 0, 0.0095, z));
    g.traverse(m => { if (m.isMesh) m.castShadow = false; });
    return g;
  },

  // (pass 3) The light of an open lift car (pivot at the foot of the doorway, the hall out along +Z): a warm trapezoid on the hall floor that widens
  // with the doors (o.doors [[t, 0..1], ...]: the set's own door keys, eased the same way), a warm point light in the doorway (o.light,
  // 3) that falls on whoever sits near it, another inside the car (o.carLight, 3: with 7 and 4 the man in the car was bleached; the car's own walls are unlit paint, the people in it are not)
  // and a glow on the car's back wall (o.wall, 0.14; o.depth 1.3: how deep the car is). o.len (2.6): how far the trapezoid runs, o.spread (1.9): how
  // much wider it is at its far end.
  doorGlow(o) {
    const DW = o.w ?? 1.1, Ln = o.len ?? 2.6, sp = o.spread ?? 1.9, g = grp(), D = o.doors || [[0, 1]], Y = 0.027;
    const es = x => x * x * (3 - 2 * x), openAt = t => { let a = D[0][1]; for (let i = 0; i < D.length; i++) { const [t0, v0] = D[i], nx = D[i + 1]; if (t >= t0) a = nx && t < nx[0] ? v0 + (nx[1] - v0) * es((t - t0) / (nx[0] - t0)) : v0; } return a; };
    const c = document.createElement('canvas'); c.width = 64; c.height = 128; const x2 = c.getContext('2d');
    const gy = x2.createLinearGradient(0, 0, 0, 128); gy.addColorStop(0, 'rgba(255,255,255,1)'); gy.addColorStop(0.5, 'rgba(255,255,255,0.6)'); gy.addColorStop(1, 'rgba(255,255,255,0)'); x2.fillStyle = gy; x2.fillRect(0, 0, 64, 128);
    x2.globalCompositeOperation = 'destination-in'; const gx = x2.createLinearGradient(0, 0, 64, 0); gx.addColorStop(0, 'rgba(0,0,0,0)'); gx.addColorStop(0.14, 'rgba(0,0,0,1)'); gx.addColorStop(0.86, 'rgba(0,0,0,1)'); gx.addColorStop(1, 'rgba(0,0,0,0)'); x2.fillStyle = gx; x2.fillRect(0, 0, 64, 128);
    const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
    const geo = new THREE.BufferGeometry(), pos = new Float32Array(12); geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    geo.setAttribute('uv', new THREE.BufferAttribute(new Float32Array([0, 1, 1, 1, 0, 0, 1, 0]), 2)); geo.setIndex([0, 2, 1, 2, 3, 1]);
    const beam = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ map: tex, color: o.color || '#FFD49A', transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }));
    beam.frustumCulled = false; g.add(beam);
    const hall = new THREE.PointLight(o.color || '#FFD49A', 0, 5.5, 1.2); hall.position.set(0, 1.4, -0.15); g.add(hall);   // just inside the doorway: it lights the floor and whoever faces the doors, not the hall wall round them (in front of the doorway it lifted that wall to the car's own brightness)
    const car = new THREE.PointLight('#FFE2B8', 0, 4, 1.2); car.position.set(0, 1.85, -0.45); g.add(car);
    const wall = new THREE.Mesh(new THREE.PlaneGeometry(DW + 0.4, 2.3), new THREE.MeshBasicMaterial({ color: '#FFC98A', transparent: true, opacity: o.wall ?? 0.14, blending: THREE.AdditiveBlending, depthWrite: false }));
    wall.position.set(0, 1.2, -(o.depth ?? 1.3) + 0.07); g.add(wall);
    g.userData.update = t => { const a = openAt(t), h0 = a * (DW / 2 - 0.03), h1 = h0 * sp + 0.12 * a;
      pos.set([-h0, Y, 0.02, h0, Y, 0.02, -h1, Y, Ln, h1, Y, Ln]); geo.attributes.position.needsUpdate = true;
      beam.visible = a > 0.01; beam.material.opacity = (o.floor ?? 0.5) * Math.min(1, a * 1.6); hall.intensity = (o.light ?? 3) * a; car.intensity = (o.carLight ?? 3) * Math.min(1, a * 2); wall.visible = a > 0.01; };
    g.userData.update(0); return g;
  },

  // (pass 3) A walking stick that swats (pivot at the handle, the shaft up along +Y, o.len 0.95; a short crook at the handle): o.swing [t0, a0, a1,
  // dur]: it waits at the angle a0 (radians about the prop's X: 0 = upright, PI / 2 = flat along +Z), goes back o.antic (0.3) more over the 0.12 s
  // before t0, comes down to a1 in dur (0.07) s with a translucent fan behind it on those frames (the smear), bounces, and settles o.rest (0.22)
  // above the thing it hit. Turn the prop (ry) so that its +Z points from the hand to the target.
  cane(o) {
    const Ln = o.len ?? 0.95, C = o.color || '#6B4A2E', g = grp(), sw = grp(); g.add(sw);
    sw.add(at(cyl(0.022, 0.019, Ln, C, 8, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(0.04, 0.04, 0.15, C, { outline: 0.005 }), 0, 0, -0.055), at(cyl(0.025, 0.025, 0.035, '#2A2622', 8), 0, Ln - 0.017, 0));
    const fanG = grp(); fanG.rotation.y = -PI / 2; g.add(fanG);
    const fan = new THREE.Mesh(new THREE.CircleGeometry(Ln, 10, 0, 0.5), new THREE.MeshBasicMaterial({ color: C, transparent: true, opacity: 0.38, side: THREE.DoubleSide, depthWrite: false })); fan.visible = false; fanG.add(fan);
    const S = o.swing, an = o.antic ?? 0.3, rest = o.rest ?? 0.22, ad = o.anticDur ?? 0.12; let last = null;   // (final pass) o.anticDur: how long the wind-up lasts (0.12 s was one frame of the draft)
    const ang = t => { if (!S) return o.a ?? 0; const [t0, a0, a1, dur = 0.07] = S, u = t - t0;
      if (u < -ad) return a0; if (u < 0) { const k = (u + ad) / ad; return a0 - an * k * k * (3 - 2 * k); }
      if (u < dur) { const k = u / dur; return a0 - an + (a1 - a0 + an) * k * k; }
      const v = u - dur; return a1 - rest * (1 - Math.exp(-7 * v)) - 0.3 * Math.exp(-9 * v) * Math.abs(Math.sin(17 * v)); };
    g.userData.update = t => { const a = ang(t); sw.rotation.x = a;
      const sm = S && t >= S[0] && t < S[0] + (S[3] ?? 0.07) + 0.05; fan.visible = !!sm;
      if (sm) { const a0 = S[1] - an, key = Math.round(a * 50); if (key !== last) { last = key; fan.geometry.dispose(); fan.geometry = new THREE.CircleGeometry(Ln, 10, PI / 2 - a, Math.max(0.05, a - a0)); } } };
    g.userData.update(0); return g;
  },

  // (pass 3) A wall calendar that sheds its years (front +Z, pivot at its middle): one page per entry of o.months, page i lifts away at o.flipAt + i *
  // o.dur. The shared monthCalendar with blank backs to its pages (a page seen from behind as it lifts showed its print mirrored).
  yearCalendar(o) {
    const w = o.w || 0.34, h = o.h || 0.46, months = o.months || ['2006'], g = grp(at(box(w + 0.02, h + 0.02, 0.012, '#3A3D44'), 0, 0, -0.008));
    const io = x => x < 0.5 ? 2 * x * x : 1 - 2 * (1 - x) * (1 - x);
    const pages = months.map((m, i) => { const piv = grp(); piv.position.set(0, h / 2, 0.002 + (months.length - i) * 0.002); g.add(piv);
      const pg = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FBF8F0'; c.fillRect(0, 0, W, H); c.fillStyle = '#C8322A'; c.fillRect(0, 0, W, H * 0.22);
        c.fillStyle = '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${H * 0.13}px Arial`; c.fillText(m, W / 2, H * 0.12);
        c.fillStyle = '#F2C94C'; c.beginPath(); c.arc(W * 0.5, H * 0.36, H * 0.08, 0, TAU); c.fill();
        c.fillStyle = '#3A3D44'; c.font = `700 ${H * 0.045}px Arial`; for (let d = 0; d < 31; d++) c.fillText(String(d + 1), (d % 7 + 0.5) / 7 * W, H * (0.52 + Math.floor(d / 7) * 0.1)); }, { res: 256 });
      pg.position.y = -h / 2; piv.add(pg);
      const bk = at(box(w, h, 0.0006, '#F1ECDF'), 0, -h / 2, -0.0011); bk.castShadow = false; piv.add(bk); return piv; });
    for (let i = 0; i < 5; i++) g.add(at(cyl(0.012, 0.012, 0.006, '#9AA0A8', 8), -w * 0.3 + i * w * 0.15, h / 2, 0.012, PI / 2, 0, 0));
    // (final pass) o.fly: once lifted, each page tears off and flies away on an arc (out and up, then down), spinning, several in the air at once
    // (the pages piled up on the wall as a grey stack)
    g.userData.update = t => pages.forEach((p, i) => { if (i === pages.length - 1) return; const t0 = o.flipAt == null ? 1e9 : o.flipAt + i * (o.dur || 0.5), q = clamp01((t - t0) / 0.28);
      if (!o.fly) { p.rotation.x = -io(q) * 2.6; p.visible = q < 0.98; return; }
      const u = Math.max(0, t - t0 - 0.12), sd = i % 2 ? 1 : -1, sp = 0.7 + 0.5 * hash(i + 3);
      p.rotation.set(-io(Math.min(1, q * 1.6)) * 1.4 - u * 6 * sp, sd * u * 4 * sp, sd * u * 3);
      p.position.set(sd * (0.45 + 0.3 * hash(i + 7)) * u * 2.2, h / 2 + 1.6 * u - 4.2 * u * u, 0.002 + (months.length - i) * 0.002 + 0.9 * u);
      p.visible = u < 0.75; });
    g.userData.update(0); return g;
  },

  // (pass 3) The dust of the works (pivot on the floor at the chisel's tip): o.n (7) round opaque puffs that swell, drift along o.drift ([-0.5, 0,
  // 0.1] m: away from whoever must stay readable), rise 0.55 m and shrink to nothing, one after the other over o.period (0.55 s). Nothing
  // see-through: translucent boulders with stippled edges ghosted him out.
  workDust(o) {
    const n = o.n ?? 7, per = o.period ?? 0.55, dr = o.drift || [-0.5, 0, 0.1], g = grp(), ps = [];
    for (let i = 0; i < n; i++) { const m = sphere(0.11 + 0.05 * hash(i + 2), o.color || '#E6DFD0', 1); m.castShadow = false; g.add(m); ps.push(m); }
    g.userData.update = t => ps.forEach((m, i) => { const u = ((((t - (o.from ?? 0)) / per + i / n) % 1) + 1) % 1, a = hash(i + 9) * TAU, k = Math.sin(PI * Math.min(1, u * 1.15));
      m.visible = t >= (o.from ?? 0) && k > 0.03; m.position.set(dr[0] * u + 0.18 * Math.cos(a) * u, 0.08 + 0.55 * u, dr[2] * u + 0.18 * Math.sin(a) * u); m.scale.setScalar(Math.max(0.03, k) * (o.s ?? 1)); });
    g.userData.update(0); return g;
  },

  // (pass 3) The way up at the head of a flight of stairs (front +Z, pivot at the middle of its sill): a dark opening o.w (1.2) wide and o.h (1.6)
  // high in the wall, a frame round it, and beside it a green sign (o.text 'ESCALIER') at o.sign ([-(w / 2 + 0.5), 0.45] from the sill). A flight
  // that ran into a blank wall read as a free-standing block.
  stairDoor(o) {
    const w = o.w ?? 1.2, h = o.h ?? 1.6, g = grp(at(box(w, h, 0.02, '#2A2622'), 0, h / 2, 0)), sg = o.sign || [-(w / 2 + 0.5), 0.45];
    for (const sd of [-1, 1]) g.add(at(box(0.08, h + 0.08, 0.06, '#8C7B5E', { outline: 0.005 }), sd * (w / 2 + 0.04), (h + 0.08) / 2, 0.02));
    g.add(at(box(w + 0.16, 0.08, 0.06, '#8C7B5E', { outline: 0.005 }), 0, h + 0.04, 0.02));
    const s = canvasPlane(0.62, 0.2, (c, W, H) => { c.fillStyle = '#1F6B4A'; c.fillRect(0, 0, W, H); c.fillStyle = '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${H * 0.56}px Arial`; c.fillText(o.text || 'ESCALIER', W / 2, H * 0.54); }, { res: 256, emissive: 0.4 });
    s.position.set(sg[0], sg[1], 0.03); g.add(s); return g;
  },

  // (final pass) A deep soup bowl held level (pivot at its foot): a white bowl with a blue rim, orange soup near the brim, a spoon, and three wisps
  // of steam that rise, sway and fade on a loop (the flat plate of the champagne story read as a blue plate)
  steamBowl(o) {
    const g = grp(), R = o.r ?? 0.1;
    g.add(at(cyl(R, R * 0.6, R * 0.9, '#F4F2EC', 18, { pivot: 'bottom', outline: 0.004 }), 0, 0, 0), at(new THREE.Mesh(new THREE.TorusGeometry(R, 0.008, 5, 24), new THREE.MeshLambertMaterial({ color: '#3A6FB5' })), 0, R * 0.9, 0, PI / 2, 0, 0));
    g.add(at(cyl(R * 0.93, R * 0.93, 0.006, o.soup || '#E39A3A', 18), 0, R * 0.8, 0), at(box(0.014, 0.006, 0.17, '#C9CDD2', { outline: 0.002 }), R * 0.45, R * 0.95, 0.02, 0.5, 0.4, 0));
    const wisps = [0, 1, 2].map(i => { const w = new THREE.Mesh(new THREE.SphereGeometry(1, 8, 6), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.6, depthWrite: false })); w.castShadow = false; g.add(w); return w; });
    g.userData.update = t => wisps.forEach((w, i) => { const u = ((t * 0.9 + i / 3) % 1 + 1) % 1, k = Math.sin(PI * u);
      w.position.set(Math.sin(t * 3 + i * 2.1) * 0.025 + (i - 1) * 0.03, R * 0.9 + 0.04 + 0.22 * u, 0); w.scale.set(0.022 + 0.03 * u, 0.035 + 0.05 * u, 0.022 + 0.03 * u); w.material.opacity = 0.55 * k; });
    g.userData.update(0); return g;
  },

  // (final pass) A baguette (pivot and grip at its middle, along X): a long golden loaf, paler rounded ends, five diagonal slashes on top (the
  // square plank of the shared one read as wood)
  loaf(o) {
    const L = o.len ?? 0.62, r = o.r ?? 0.036, g = grp(at(cyl(r, r, L - 2 * r, '#D9A35C', 10, { outline: 0.006 }), 0, 0, 0, 0, 0, PI / 2));
    for (const sd of [-1, 1]) { const e = sphere(r, '#E8C48A', 1); e.scale.set(1.25, 1, 1); e.position.set(sd * (L / 2 - r), 0, 0); g.add(e); }
    for (let i = 0; i < 5; i++) g.add(at(box(0.07, 0.008, 0.016, '#F2DDB0'), -L * 0.32 + i * L * 0.16, r * 0.92, 0, 0, 0.55, 0));
    g.userData.grip = [0, 0, 0]; return g;
  },

  // (final pass) A folding table (front +Z, pivot on the floor): a pale wooden top o.w (1.0) x o.d (0.55) at 0.74, two pairs of crossed steel legs
  // (the teal office desk with drawers did not read as the folding table of a residents' meeting)
  foldTable(o) {
    const w = o.w ?? 1.0, d = o.d ?? 0.55, h = 0.74, g = grp(at(box(w, 0.04, d, o.top || '#D9B98A', { outline: 0.006 }), 0, h - 0.02, 0));
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(rod([sx * (w / 2 - 0.08), 0, sz * (d / 2 - 0.04)], [sx * (w / 2 - 0.08), h - 0.04, -sz * (d / 2 - 0.04)], 0.014, '#7A7F88'));
    g.add(at(box(w - 0.1, 0.012, 0.012, '#7A7F88'), 0, h * 0.5, 0)); return g;
  },

  // (final pass) Dust motes in a spotlight (pivot at the lamp, the cone opening down -Y): o.n (40) small bright specks inside a cone o.h (2.3) high
  // and o.r (0.42) wide at its foot, each drifting slowly down and round and twinkling; the light pool held still for most of the shot
  coneDust(o) {
    const n = o.n ?? 40, H = o.h ?? 2.3, R = o.r ?? 0.42, g = grp(), ps = [];
    const mat = new THREE.MeshBasicMaterial({ color: o.color || '#FFF4D8', transparent: true, opacity: 0.9, depthWrite: false });
    for (let i = 0; i < n; i++) { const m = new THREE.Mesh(new THREE.SphereGeometry(o.s ?? 0.008, 5, 4), mat.clone()); m.castShadow = false; g.add(m); ps.push(m); }
    g.userData.update = t => ps.forEach((m, i) => { const f = ((hash(i + 1) + t * (0.03 + 0.04 * hash(i + 5))) % 1), y = -0.2 - f * (H - 0.4), rr = R * (-y / H) * Math.sqrt(hash(i + 9)), a = hash(i + 13) * TAU + t * (0.25 + 0.3 * hash(i + 17));
      m.position.set(Math.cos(a) * rr, y, Math.sin(a) * rr); m.material.opacity = 0.35 + 0.55 * Math.max(0, Math.sin(t * (3 + 4 * hash(i + 21)) + i)); });
    g.userData.update(0); return g;
  },

  // (final pass) A stair banister (pivot at the foot of its first post): a wooden rail from (0, o.h0 (0.9), 0) up to (0, o.rise + o.h0, -o.run) on
  // o.posts (5) thin posts, for the open side of a flight (o.rise 1.4, o.run 1.96)
  banister(o) {
    const rise = o.rise ?? 1.4, run = o.run ?? 1.96, h0 = o.h0 ?? 0.9, n = o.posts ?? 5, g = grp(rod([0, h0, 0], [0, rise + h0, -run], 0.028, o.color || '#6B4A2E'));
    for (let i = 0; i < n; i++) { const k = i / (n - 1), y = rise * k; g.add(rod([0, y, -run * k], [0, y + h0, -run * k], 0.014, '#3A3D44')); }
    return g;
  },
};
