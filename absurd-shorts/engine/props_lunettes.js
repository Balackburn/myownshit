// « Les lunettes » (story 69, cycle 31): this man lost his glasses. He looked everywhere: under the sofa, in the fridge. He filed a complaint; the
// police searched the whole district, divers drained the river, the army sent helicopters, satellites scanned the planet, the other countries sent
// their dogs, the government promised a million euros, the whole world searched for a year. Yesterday a child found them: on his head. The child
// got the million. The man is looking for his keys. Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every
// animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = PI * 2;
const clamp01 = x => Math.max(0, Math.min(1, x));
const eo = x => 1 - Math.pow(1 - clamp01(x), 3);
const hash = n => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const inWin = (w, t) => (w || []).some(([a, b]) => t >= a && t < b);
const lam = (color, opacity = 1) => new THREE.MeshLambertMaterial({ color, transparent: opacity < 1, opacity, depthWrite: opacity >= 1 });
const basic = (color, opacity = 1) => new THREE.MeshBasicMaterial({ color, transparent: opacity < 1, opacity, depthWrite: opacity >= 1 });
function keyAt(k, t, d = 0) {
  if (k == null) return d; if (typeof k === 'number') return k; if (!k.length) return d; if (t <= k[0][0]) return k[0][1];
  for (let i = 0; i < k.length - 1; i++) { const [t0, v0] = k[i], [t1, v1] = k[i + 1]; if (t < t1) { const u = (t - t0) / Math.max(1e-6, t1 - t0); return v0 + (v1 - v0) * u * u * (3 - 2 * u); } }
  return k[k.length - 1][1];
}
let _spark = null;
function sparkTex() {   // a four-pointed white sparkle with a soft core (the glint on a lens)
  if (_spark) return _spark;
  const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d'), m = 64;
  const gr = g.createRadialGradient(m, m, 0, m, m, 40); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.25, 'rgba(255,255,240,0.8)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
  g.fillStyle = '#FFFFFF'; for (const a of [0, PI / 2]) { g.save(); g.translate(m, m); g.rotate(a); g.beginPath(); g.moveTo(-60, 0); g.lineTo(0, -5); g.lineTo(60, 0); g.lineTo(0, 5); g.closePath(); g.fill(); g.restore(); }
  _spark = new THREE.CanvasTexture(c); return _spark;
}

export const LUNETTES_PROPS = {
  // Big black-rimmed glasses that read at phone size (origin at the bridge, the lenses facing +Z, the temples back along -Z): o.r (0.055 lens radius),
  // o.dx (0.075 from the bridge to a lens centre), o.color (rims, '#151515'); pale lenses with a white streak; o.glint [t, ...]: a sparkle flashes on the
  // left lens at each (0.35 s: it swells and turns), o.glintSize (0.12)
  // (pass 3 of 69) o.rim (0.2: the rims' thickness as a share of the lens radius); o.tap [t, ...]: knocked by a finger at each, they rock on the head
  // and settle (o.tapAmp, 0.5 rad); the parts hang in an inner group so that the rocking survives a prop turned to the camera
  bigGlasses(o) {
    const R = o.r ?? 0.055, dx = o.dx ?? 0.075, C = o.color || '#151515', g0 = grp(), g = grp(); g0.add(g);
    for (const s of [-1, 1]) {
      g.add(at(new THREE.Mesh(new THREE.TorusGeometry(R, R * (o.rim ?? 0.2), 6, 20), lam(C)), s * dx, 0, 0));
      g.add(at(new THREE.Mesh(new THREE.CircleGeometry(R * 0.96, 20), new THREE.MeshLambertMaterial({ color: '#CFE8F6', transparent: true, opacity: 0.55, side: THREE.DoubleSide, depthWrite: false })), s * dx, 0, 0.001));
      g.add(at(new THREE.Mesh(new THREE.PlaneGeometry(R * 0.28, R * 1.1), basic('#FFFFFF', 0.8)), s * dx - R * 0.35, R * 0.1, 0.003, 0, 0, -0.6));
      const tl = 0.16; g.add(at(box(0.012, 0.012, tl, C), s * (dx + R * 1.1), 0, -tl / 2), at(box(0.012, 0.03, 0.012, C), s * (dx + R * 1.1), -0.012, -tl));
    }
    g.add(at(box(dx * 2 - R * 2 + 0.01, 0.012, 0.012, C), 0, R * 0.25, 0));
    const sp = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: sparkTex(), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending })); sp.position.set(-dx + R * 0.3, R * 0.3, 0.01); g.add(sp);
    g0.userData.update = t => { let k = 0; for (const t0 of o.glint || []) { const u = (t - t0) / 0.35; if (u >= 0 && u < 1) k = Math.max(k, Math.sin(PI * u)); } sp.visible = k > 0.01; if (sp.visible) { const s = (o.glintSize ?? 0.12) * k; sp.scale.set(s, s, 1); sp.rotation.z = t * 3; }
      let rock = 0, hop = 0; for (const t0 of o.tap || []) { const u = t - t0; if (u >= 0 && u < 1.2) { rock += (o.tapAmp ?? 0.5) * Math.exp(-u * 5) * Math.sin(u * 30); hop += 0.03 * Math.exp(-u * 9) * Math.abs(Math.sin(u * 30)); } }
      g.rotation.z = rock; g.position.y = hop; };
    g0.userData.update(0); return g0;
  },

  // (pass 3 of 69) A big magnifying glass with a huge magnified eye in it (pivot at the middle of the lens, facing +Z, the handle down to the right):
  // o.r (0.16: the lens radius); the eye looks about by itself (a slow scan) or follows o.look [[t, x, y], ...] (-1..1), and blinks at o.blink [t, ...];
  // o.iris ('#4A7FB5'), o.skin ('#E2A878')
  eyeLens(o) {
    const R = o.r ?? 0.16, g = grp(), flat = (r, c, z, seg = 28) => at(new THREE.Mesh(new THREE.CircleGeometry(r, seg), basic(c)), 0, 0, z);
    g.add(new THREE.Mesh(new THREE.TorusGeometry(R, R * 0.1, 8, 28), lam('#C9A23A')));
    g.add(at(cyl(R * 0.11, R * 0.13, R * 1.3, '#3B2A20', 8, { outline: 0.004 }), R * 1.2, -R * 1.2, 0, 0, 0, PI / 4));
    g.add(flat(R * 0.97, o.skin || '#E2A878', 0.001));
    const white = flat(R * 0.84, '#FBFBF6', 0.002), eye = grp(); white.scale.y = 0.62; g.add(white, eye);
    eye.add(flat(R * 0.4, o.iris || '#4A7FB5', 0.003), flat(R * 0.2, '#15151A', 0.004), at(new THREE.Mesh(new THREE.CircleGeometry(R * 0.07, 10), basic('#FFFFFF')), R * 0.1, R * 0.12, 0.005));
    g.add(at(box(R * 1.1, R * 0.13, 0.004, '#2A2420'), 0, R * 0.7, 0.003, 0, 0, 0.12));
    g.add(at(new THREE.Mesh(new THREE.CircleGeometry(R * 0.97, 28), basic('#DDF0FF', 0.14)), 0, 0, 0.006), at(new THREE.Mesh(new THREE.RingGeometry(R * 0.62, R * 0.76, 14, 1, 2.1, 0.9), basic('#FFFFFF', 0.7)), 0, 0, 0.007));
    g.userData.update = t => { let gx = 0.8 * Math.sin(t * 2.6), gy = 0.25 * Math.sin(t * 1.7 + 1), op = 0.62;
      if (o.look) { gx = keyAt(o.look.map(q => [q[0], q[1]]), t, 0); gy = keyAt(o.look.map(q => [q[0], q[2]]), t, 0); }
      for (const t0 of o.blink || []) { const u = (t - t0) / 0.16; if (u >= 0 && u < 1) op = 0.62 * Math.max(0.06, Math.abs(1 - 2 * u)); }
      white.scale.y = op; eye.position.set(gx * R * 0.36, gy * R * 0.2, 0); eye.scale.y = Math.min(1, op / 0.5); };
    g.userData.update(0); return g;
  },

  // (pass 3 of 69) A big wall calendar that sheds its months toward us (pivot at its middle, on the wall, facing +Z): o.months (names), o.w (0.9) x
  // o.h (1.15); from o.flipAt a page tears off every o.dur (0.17 s): it lifts, comes off, flies o.fly ([dx, dy, dz] m, [0.5, -0.9, 1.6]) tumbling and
  // growing, and is gone after o.life (0.5 s); the last month stays on the wall
  shedCalendar(o) {
    const W = o.w ?? 0.9, H = o.h ?? 1.15, months = o.months || ['JANVIER', 'FÉVRIER', 'MARS'], g = grp(), fly = o.fly || [0.5, -0.9, 1.6], life = o.life ?? 0.5;
    g.add(at(box(W + 0.06, H + 0.06, 0.03, '#3A3D44', { outline: 0.006 }), 0, 0, -0.02));
    for (let i = 0; i < 6; i++) g.add(at(cyl(0.022, 0.022, 0.02, '#9AA0A8', 8), -W * 0.36 + i * W * 0.144, H / 2 + 0.01, 0.01, PI / 2, 0, 0));
    const pages = months.map((m, i) => { const pg = canvasPlane(W, H, (c, cw, ch) => { c.fillStyle = '#FBF8F0'; c.fillRect(0, 0, cw, ch); c.fillStyle = '#C8322A'; c.fillRect(0, 0, cw, ch * 0.3);
        c.fillStyle = '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle'; let px = ch * 0.2; c.font = `900 ${px}px Arial`; const tw = c.measureText(m).width; if (tw > cw * 0.9) { px *= cw * 0.9 / tw; c.font = `900 ${px}px Arial`; } c.fillText(m, cw / 2, ch * 0.16);
        c.fillStyle = '#3A3D44'; c.font = `700 ${ch * 0.06}px Arial`; for (let d = 0; d < 31; d++) c.fillText(String(d + 1), (d % 7 + 0.5) / 7 * cw, ch * (0.42 + Math.floor(d / 7) * 0.115)); }, { res: 256, emissive: 0.12 });
      pg.position.z = 0.004 + (months.length - i) * 0.0015; g.add(pg); return pg; });
    g.userData.update = t => pages.forEach((pg, i) => { const z0 = 0.004 + (months.length - i) * 0.0015;
      if (i === pages.length - 1 || o.flipAt == null) { pg.visible = true; pg.position.set(0, 0, z0); pg.rotation.set(0, 0, 0); pg.scale.setScalar(1); return; }
      const u = (t - o.flipAt - i * (o.dur ?? 0.17)) / life; pg.visible = u < 1;
      if (u <= 0) { pg.position.set(0, 0, z0); pg.rotation.set(0, 0, 0); pg.scale.setScalar(1); return; }
      const sd = hash(i + 5) - 0.5; pg.position.set(fly[0] * u * (1 + sd), fly[1] * u * u + 0.18 * Math.sin(PI * u), z0 + 0.05 + fly[2] * u);
      pg.rotation.set(-0.5 - 2.2 * u, sd * 1.2 * u, sd * 2.4 * u); pg.scale.setScalar(1 + 0.25 * u); });
    g.userData.update(0); return g;
  },

  // (pass 3 of 69) Big field binoculars seen from the front (pivot between the barrels at the eyepieces, the objectives toward +Z): o.r (0.06), o.len
  // (0.17), o.color ('#22252B'); pale-blue objective glasses with a white streak, a bridge between the barrels
  bigBinoculars(o) {
    const R = o.r ?? 0.06, L = o.len ?? 0.17, C = o.color || '#22252B', g = grp();
    for (const s of [-1, 1]) {
      g.add(at(cyl(R, R * 0.72, L, C, 12, { outline: 0.006 }), s * R * 1.12, 0, L / 2, PI / 2, 0, 0));
      g.add(at(new THREE.Mesh(new THREE.CircleGeometry(R * 0.82, 16), basic('#9FD0EA')), s * R * 1.12, 0, L + 0.002), at(new THREE.Mesh(new THREE.PlaneGeometry(R * 0.26, R * 1.0), basic('#FFFFFF', 0.85)), s * R * 1.12 - R * 0.3, R * 0.1, L + 0.004, 0, 0, -0.6));
    }
    g.add(at(box(R * 0.9, R * 0.5, L * 0.5, C), 0, 0, L * 0.45));
    return g;
  },

  // (pass 3 of 69) A sitting dog that stares (pivot on the ground under its rump, facing +Z; about 0.75 m to the top of the head): o.body
  // ('#8A6A4A'), o.ear ('#5E4630'), o.collar ('#F2C94E'). It sniffs the ground in front of it; at o.sitAt its rump drops with a squash; at o.lookAt
  // the neck stretches up and the nose goes up (o.up: rad, 0.85); at o.tiltAt the head tilts o.tilt (0.55 rad) and the ears flop after it; at
  // o.backAt it goes back to sniffing. The tail wags all along. (The engine's four-legged creatures have no head keys: their look is fixed by the clip)
  stareDog(o) {
    const C = o.body || '#8A6A4A', E = o.ear || '#5E4630', ol = { outline: 0.012 }, g = grp(), all = grp(); g.add(all);
    const body = grp(at(box(0.27, 0.3, 0.56, C, ol), 0, 0, 0)); body.position.set(0, 0.33, 0.04); body.rotation.x = -0.85; all.add(body);
    all.add(at(box(0.3, 0.2, 0.3, C, ol), 0, 0.11, -0.14));
    for (const sd of [-1, 1]) all.add(at(box(0.075, 0.4, 0.075, C, ol), sd * 0.085, 0.2, 0.24), at(box(0.09, 0.06, 0.2, C, ol), sd * 0.13, 0.03, -0.02));
    const tail = grp(at(box(0.05, 0.26, 0.05, C, ol), 0, 0.13, 0)); tail.position.set(0, 0.16, -0.3); all.add(tail);
    const neck = grp(); neck.position.set(0, 0.5, 0.22); all.add(neck);
    const nk = at(box(0.15, 0.16, 0.15, C, ol), 0, 0.08, 0); neck.add(nk, at(box(0.17, 0.045, 0.17, o.collar || '#F2C94E'), 0, 0.03, 0));
    const head = grp(); neck.add(head);
    head.add(at(box(0.25, 0.22, 0.25, C, ol), 0, 0.1, 0.02), at(box(0.14, 0.11, 0.17, C, ol), 0, 0.055, 0.21), at(box(0.06, 0.05, 0.04, '#1C1C20'), 0, 0.085, 0.3));
    const ears = [-1, 1].map(sd => { const e = grp(at(box(0.03, 0.17, 0.13, E, ol), 0, -0.085, 0)); e.position.set(sd * 0.14, 0.2, -0.02); head.add(e); return e; });
    for (const sd of [-1, 1]) { head.add(at(new THREE.Mesh(new THREE.CircleGeometry(0.036, 12), basic('#FFFFFF')), sd * 0.126, 0.14, 0.09, 0, sd * PI / 2, 0), at(new THREE.Mesh(new THREE.CircleGeometry(0.018, 10), basic('#15151A')), sd * 0.127, 0.15, 0.1, 0, sd * PI / 2, 0));
      head.add(at(new THREE.Mesh(new THREE.CircleGeometry(0.034, 12), basic('#FFFFFF')), sd * 0.06, 0.15, 0.146), at(new THREE.Mesh(new THREE.CircleGeometry(0.017, 10), basic('#15151A')), sd * 0.06, 0.157, 0.147)); }
    const sm = (a, d) => { const u = clamp01(a / d); return u * u * (3 - 2 * u); }, back = (a, d) => { const u = clamp01(a / d); return 1 + 2.2 * Math.pow(u - 1, 3) + 1.2 * Math.pow(u - 1, 2); };
    g.userData.update = t => {
      const tb = o.backAt ?? 1e9, lk = (o.lookAt == null ? 0 : back(t - o.lookAt, 0.22) * (t >= o.lookAt ? 1 : 0)) * (1 - sm(t - tb, 0.18)), tl = (o.tiltAt == null ? 0 : back(t - o.tiltAt, 0.2) * (t >= o.tiltAt ? 1 : 0)) * (1 - sm(t - tb, 0.15));
      const sniff = 1 - Math.min(1, Math.max(0, lk)), su = o.sitAt == null ? 9 : t - o.sitAt, sq = su >= 0 && su < 0.5 ? 1 - 0.22 * Math.exp(-su * 9) * Math.cos(su * 22) : 1;
      all.scale.set(1 / Math.sqrt(sq), sq, 1 / Math.sqrt(sq)); all.position.y = su < 0 ? 0.1 : 0;
      neck.rotation.x = 1.25 * sniff + 0.05 * sniff * Math.sin(t * 17); nk.scale.y = 1 + 1.3 * lk; nk.position.y = 0.08 * (1 + 1.3 * lk); head.position.y = 0.16 * (1 + 1.3 * lk) - 0.02;
      head.rotation.set(-(o.up ?? 0.85) * lk + 0.25 * sniff, 0, (o.tilt ?? 0.55) * tl);
      const lag = o.tiltAt == null ? 0 : (o.tilt ?? 0.55) * 0.9 * Math.exp(-Math.max(0, t - o.tiltAt) * 6) * Math.cos(Math.max(0, t - o.tiltAt) * 16) * (t >= o.tiltAt ? 1 : 0);
      ears.forEach((e, i) => { e.rotation.z = -(o.tilt ?? 0.55) * tl * 0.8 + lag + (i ? -0.06 : 0.06); e.rotation.x = 0.5 * lk; });
      tail.rotation.set(-0.6, 0, 0.5 * Math.sin(t * (lk > 0.5 ? 6 : 15)));
    };
    g.userData.update(0); return g;
  },

  // A low-poly military helicopter facing +Z (pivot at its centre of mass, about 9 m long at scale 1): olive body, a glazed nose, the tail boom with
  // its rotor, skids, the main rotor turning (two blades and a pale blur disc), o.spin (rotor turns per second, 6); o.beam: a searchlight under the
  // nose, a soft cone down to o.beamLen (14 m) and o.beamR (2.2 m) wide at its end, swept by o.sweep [[t, deg about Y], ...] and tilted by o.tilt
  // (deg forward of straight down, 20); o.color ('#56603F')
  helicopter(o) {
    const C = o.color || '#56603F', D = '#33392A', ol = { outline: 0.02 }, g = grp();
    const body = new THREE.Mesh(new THREE.SphereGeometry(1, 14, 10), lam(C)); body.scale.set(1.1, 1.05, 2.2); g.add(body);
    const nose = new THREE.Mesh(new THREE.SphereGeometry(1, 12, 8, 0, TAU, 0, PI / 2), new THREE.MeshLambertMaterial({ color: '#9FC4D8', transparent: true, opacity: 0.75 })); nose.scale.set(0.95, 0.85, 1.1); nose.rotation.x = PI / 2; nose.position.set(0, 0.15, 1.35); g.add(nose);
    g.add(at(cyl(0.22, 0.38, 5.0, C, 8, ol), 0, 0.35, -3.6, PI / 2, 0, 0), at(box(0.1, 1.3, 0.8, C, ol), 0, 1.0, -6.0), at(box(1.6, 0.08, 0.5, C, ol), 0, 0.4, -5.6));
    const tr = grp(at(box(0.06, 1.3, 0.12, D), 0, 0, 0), at(box(0.06, 0.12, 1.3, D), 0, 0, 0)); tr.position.set(0.12, 1.1, -6.05); g.add(tr);
    for (const s of [-1, 1]) { g.add(at(box(0.1, 0.1, 3.0, D), s * 0.9, -1.35, 0.1)); for (const z of [-0.8, 0.9]) g.add(at(box(0.08, 0.45, 0.08, D), s * 0.75, -1.1, z, 0, 0, s * 0.35)); }
    g.add(at(cyl(0.12, 0.16, 0.4, D, 8), 0, 1.15, 0));
    const rotor = grp(at(box(10.5, 0.05, 0.38, D), 0, 0, 0), at(box(0.38, 0.05, 10.5, D), 0, 0, 0)); rotor.position.y = 1.36; g.add(rotor);
    const disc = new THREE.Mesh(new THREE.CircleGeometry(5.3, 32), new THREE.MeshBasicMaterial({ color: '#D8DCD0', transparent: true, opacity: 0.18, side: THREE.DoubleSide, depthWrite: false })); disc.rotation.x = -PI / 2; disc.position.y = 1.4; g.add(disc);
    let beam = null, lamp = null;
    if (o.beam) {
      const L = o.beamLen ?? 14, BR = o.beamR ?? 2.2; beam = grp(); const cone = new THREE.Mesh(new THREE.ConeGeometry(BR, L, 24, 1, true), new THREE.MeshBasicMaterial({ color: '#FFF6C8', transparent: true, opacity: 0.16, side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending }));
      cone.position.y = -L / 2; beam.add(cone); const core = new THREE.Mesh(new THREE.ConeGeometry(BR * 0.45, L, 18, 1, true), cone.material.clone()); core.material.opacity = 0.2; core.position.y = -L / 2; beam.add(core);
      beam.position.set(0, -0.9, 1.6); g.add(beam); lamp = at(cyl(0.22, 0.18, 0.2, '#FFF6C8', 10, { emissive: '#FFF0B0' }), 0, -0.9, 1.6); g.add(lamp);
    }
    g.userData.update = t => {
      rotor.rotation.y = (o.spin ?? 6) * TAU * t; tr.rotation.x = 4 * (o.spin ?? 6) * TAU * t;
      if (beam) { const sw = keyAt(o.sweep, t, 0) * PI / 180, tl = (o.tilt ?? 20) * PI / 180; beam.rotation.set(0, 0, 0); beam.rotateY(sw); beam.rotateX(tl); }
    };
    g.userData.update(0); return g;
  },

  // A satellite (pivot at its middle, the dish toward -Y: the Earth below): a gold-foil body, two long blue solar wings, a white dish, an antenna;
  // o.scan [[t0, t1], ...]: a red scanning fan from the dish to o.scanLen (6) below, sweeping to and fro (o.sweepDeg 35 either side)
  // (review 1 of 69) o.fanColor / o.fanOpacity (0.22) / o.fanBlend 'normal': a saturated red fan over the globe (the faint additive one was lost in the facets)
  // (stills 7 of 69) o.fanWidth (0.35): the fan's half-width over its length (a long fan reaching a distant globe was as wide as the planet)
  satellite(o) {
    const g = grp(), body = grp(); g.add(body);
    body.add(at(box(0.9, 1.1, 0.9, '#D9B44A', { outline: 0.012 }), 0, 0, 0), at(box(0.92, 0.08, 0.92, '#B8902A'), 0, 0.3, 0), at(box(0.92, 0.08, 0.92, '#B8902A'), 0, -0.3, 0));
    for (const s of [-1, 1]) { body.add(at(cyl(0.04, 0.04, 0.6, '#9AA0A6', 6), s * 0.75, 0, 0, 0, 0, PI / 2)); const w = at(box(2.6, 0.04, 0.95, '#2F5FB5', { outline: 0.008 }), s * 2.35, 0, 0); body.add(w);
      for (let j = 1; j < 6; j++) body.add(at(box(0.02, 0.05, 0.95, '#9CC3F0'), s * (1.05 + j * 0.43), 0, 0)); }
    const dish = new THREE.Mesh(new THREE.SphereGeometry(0.5, 16, 6, 0, TAU, 0, 0.9), new THREE.MeshLambertMaterial({ color: '#F2F2EE', side: THREE.DoubleSide })); dish.rotation.x = PI; dish.position.y = -0.95; body.add(dish);
    body.add(at(cyl(0.025, 0.025, 0.5, '#9AA0A6', 5), 0, -0.85, 0), at(cyl(0.02, 0.02, 0.9, '#9AA0A6', 5), 0.25, 0.95, 0.2));
    const L = o.scanLen ?? 6, fan = new THREE.Mesh(new THREE.ConeGeometry(L * (o.fanWidth ?? 0.35), L, 4, 1, true), new THREE.MeshBasicMaterial({ color: o.fanColor || '#FF4A3A', transparent: true, opacity: o.fanOpacity ?? 0.22, side: THREE.DoubleSide, depthWrite: false, blending: o.fanBlend === 'normal' ? THREE.NormalBlending : THREE.AdditiveBlending }));
    fan.scale.set(1, 1, 0.12); const fg = grp(); fan.position.y = -L / 2 - 1.0; fg.add(fan); g.add(fg);
    // (pass 3 of 69) o.foot: a bright footprint where the fan ends (the beam stops on the ground instead of running on past the planet)
    if (o.foot) { const ft = new THREE.Mesh(new THREE.CircleGeometry(L * (o.fanWidth ?? 0.35) * 1.05, 20), new THREE.MeshBasicMaterial({ color: o.footColor || '#FFD0C0', transparent: true, opacity: 0.75, side: THREE.DoubleSide, depthWrite: false })); ft.rotation.x = -PI / 2; ft.scale.set(1, 0.3, 1); ft.position.y = -L - 1.0; fg.add(ft); }
    g.userData.update = t => { fg.visible = inWin(o.scan, t); if (fg.visible) fg.rotation.z = (o.sweepDeg ?? 35) * PI / 180 * Math.sin(t * 3.2); body.rotation.y = 0.05 * Math.sin(t * 0.7); };
    g.userData.update(0); return g;
  },

  // A diving mask and snorkel to wear on a head (attach it to the head joint: origin at the joint, the face toward +Z): a black frame round a pale
  // glass over the eyes (o.y: its height above the joint, 0.32; o.w 0.3, o.d: the face's depth, 0.17), a strap round the head, a yellow snorkel up
  // the side
  diveMask(o) {
    const W = o.w ?? 0.3, Y = o.y ?? 0.32, Dz = (o.d ?? 0.17) / 2 + 0.02, g = grp();
    g.add(at(box(W * 0.92, 0.14, 0.05, '#1C1C20', { outline: 0.004 }), 0, Y, Dz), at(new THREE.Mesh(new THREE.PlaneGeometry(W * 0.78, 0.1), new THREE.MeshLambertMaterial({ color: '#BFE4F2', transparent: true, opacity: 0.7 })), 0, Y, Dz + 0.027));
    g.add(at(box(W + 0.04, 0.04, (o.d ?? 0.17) + 0.06, '#1C1C20'), 0, Y, 0));
    g.add(at(cyl(0.018, 0.018, 0.42, '#F2C21E', 6), W / 2 + 0.03, Y + 0.08, 0.02), at(cyl(0.02, 0.02, 0.12, '#1C1C20', 6), W / 2 + 0.03, Y + 0.31, 0.02));
    return g;
  },

  // A drained river between stone quays (pivot on the mud in the middle of the bed, the river along Z): a brown mud bed o.w (8 m) wide and o.len
  // (40 m) long with puddles, stone quay walls o.qh (2.4 m) high with a pavement and a railing on top, a stone bridge arch across at o.bridgeZ (-16),
  // and junk in the mud: a bicycle wheel, a shopping basket, a boot
  drainedRiver(o) {
    const W = o.w ?? 8, L = o.len ?? 40, QH = o.qh ?? 2.4, g = grp();
    const mud = at(box(W, 0.1, L, '#6B5638'), 0, -0.05, 0); g.add(mud);
    for (let i = 0; i < 14; i++) { const p = new THREE.Mesh(new THREE.CircleGeometry(0.4 + 0.9 * hash(i + 3), 12), new THREE.MeshLambertMaterial({ color: '#6E8E9E', transparent: true, opacity: 0.85 })); p.rotation.x = -PI / 2; p.scale.set(1, 0.6 + 0.5 * hash(i + 9), 1); p.position.set((hash(i + 1) - 0.5) * (W - 1.5), 0.006, (hash(i + 5) - 0.5) * L); g.add(p); }
    for (let i = 0; i < 30; i++) g.add(at(box(0.2 + 0.3 * hash(i + 40), 0.08, 0.2 + 0.3 * hash(i + 41), '#594629'), (hash(i + 42) - 0.5) * (W - 1), 0.02, (hash(i + 43) - 0.5) * L, 0, hash(i + 44) * PI, 0));
    for (const s of [-1, 1]) {
      g.add(at(box(1.2, QH, L, '#BDB4A2', { pivot: 'bottom', outline: 0.01 }), s * (W / 2 + 0.6), 0, 0), at(box(3.0, 0.15, L, '#D8D0BE', { pivot: 'bottom' }), s * (W / 2 + 1.5), QH, 0));
      for (let z = -L / 2; z < L / 2; z += 1.4) g.add(at(box(0.04, 0.9, 0.04, '#2B2B2E', { pivot: 'bottom' }), s * (W / 2 + 0.1), QH + 0.15, z));
      g.add(at(box(0.05, 0.05, L, '#2B2B2E'), s * (W / 2 + 0.1), QH + 1.0, 0));
      for (let j = 0; j < 12; j++) g.add(at(box(0.02, 0.6, 1.0 + hash(j + s * 7), '#A89F8C'), s * (W / 2 + 0.005), 0.4 + 0.18 * (j % 4), -L / 2 + (j + 0.5) * L / 12));
    }
    const bz = o.bridgeZ ?? -16, arch = grp();
    arch.add(at(box(W + 6, 1.0, 2.0, '#C9BFA9', { outline: 0.01 }), 0, QH + 0.6, 0));
    for (const s of [-1, 1]) arch.add(at(box(1.4, QH + 0.1, 2.0, '#BFB59E', { pivot: 'bottom', outline: 0.01 }), s * (W / 2 - 0.2), 0, 0));
    const shape = new THREE.Shape(); shape.moveTo(-W / 2 + 0.5, 0); shape.lineTo(-W / 2 + 0.5, QH * 0.5); shape.absarc(0, QH * 0.5, W / 2 - 0.5, PI, 0, true); shape.lineTo(W / 2 - 0.5, 0); shape.lineTo(W / 2 + 0.5, 0); shape.lineTo(W / 2 + 0.5, QH + 0.1); shape.lineTo(-W / 2 - 0.5, QH + 0.1); shape.lineTo(-W / 2 - 0.5, 0); shape.closePath();
    const sp = new THREE.Mesh(new THREE.ExtrudeGeometry(shape, { depth: 1.8, bevelEnabled: false }), lam('#C4BAA4')); sp.position.set(0, 0, -0.9); arch.add(sp);
    arch.position.z = bz; g.add(arch);
    const wheel = at(new THREE.Mesh(new THREE.TorusGeometry(0.35, 0.03, 6, 20), lam('#2B2B2E')), 1.6, 0.25, 2.5, 0.3, 0.6, 0); g.add(wheel);
    for (let i = 0; i < 8; i++) { const a = i / 8 * PI; g.add(at(cyl(0.008, 0.008, 0.68, '#9AA0A6', 4), 1.6, 0.25, 2.5, 0.3, 0.6, a)); }
    const basket = grp(at(box(0.6, 0.35, 0.4, '#9AA0A6', { outline: 0.004 }), 0, 0.17, 0)); basket.position.set(-2.2, 0, -3.5); basket.rotation.set(0.2, 0.7, 0.3); g.add(basket);
    g.add(at(box(0.14, 0.32, 0.12, '#3B2A20'), -1.0, 0.16, 4.2, 0, 0.4, 1.3), at(box(0.28, 0.1, 0.12, '#3B2A20'), -0.85, 0.06, 4.15, 0, 0.4, 0));
    return g;
  },

  // A reward poster on a board (pivot at the bottom of its stand, facing +Z): o.w (1.3) x o.h (1.8): « RÉCOMPENSE » in red at the top, a big drawing of
  // glasses, o.sum (« UN MILLION D'EUROS ») under it; on a stand o.stand (1.0 m) high; o.at: it pops up with an overshoot
  rewardPoster(o) {
    const W = o.w ?? 1.3, H = o.h ?? 1.8, S = o.stand ?? 1.0, g = grp(), pop = grp(); g.add(pop);
    pop.add(at(box(0.08, S, 0.08, '#5A4632', { pivot: 'bottom' }), 0, 0, -0.05), at(box(W + 0.1, H + 0.1, 0.05, '#2B2B2E', { outline: 0.008 }), 0, S + H / 2, 0));
    const face = canvasPlane(W, H, (x, cw, ch) => {
      x.fillStyle = '#F7F1DE'; x.fillRect(0, 0, cw, ch); x.fillStyle = '#C8302A'; x.fillRect(0, 0, cw, ch * 0.2);
      x.fillStyle = '#FFFFFF'; x.textAlign = 'center'; x.textBaseline = 'middle'; let fs = ch * 0.11; x.font = `900 ${fs}px Arial`; while (x.measureText('RÉCOMPENSE').width > cw * 0.9) { fs -= 2; x.font = `900 ${fs}px Arial`; } x.fillText('RÉCOMPENSE', cw / 2, ch * 0.1);
      x.strokeStyle = '#151515'; x.lineWidth = cw * 0.035; const cy = ch * 0.45, r = cw * 0.17; x.beginPath(); x.arc(cw * 0.3, cy, r, 0, TAU); x.stroke(); x.beginPath(); x.arc(cw * 0.7, cy, r, 0, TAU); x.stroke();
      x.beginPath(); x.moveTo(cw * 0.3 + r, cy - r * 0.2); x.quadraticCurveTo(cw / 2, cy - r * 0.6, cw * 0.7 - r, cy - r * 0.2); x.stroke();
      x.fillStyle = '#151515'; const sum = o.sum || "UN MILLION D'EUROS"; fs = ch * 0.085; x.font = `900 ${fs}px Arial`; while (x.measureText(sum).width > cw * 0.9) { fs -= 2; x.font = `900 ${fs}px Arial`; } x.fillText(sum, cw / 2, ch * 0.78);
      x.font = `600 ${ch * 0.035}px Arial`; x.fillStyle = '#5A5246'; x.fillText('À QUI RETROUVERA SES LUNETTES', cw / 2, ch * 0.9);
    }, { res: 512, emissive: 0.15 });
    face.position.set(0, S + H / 2, 0.03); pop.add(face);
    g.userData.update = t => { const u = o.at == null ? 9 : t - o.at; pop.visible = u >= 0; if (u >= 0) { const k = u < 0.12 ? eo(u / 0.12) * 1.12 : 1.12 - 0.12 * clamp01((u - 0.12) / 0.1); pop.scale.set(1, Math.max(0.01, k), 1); } };
    g.userData.update(0); return g;
  },
};
