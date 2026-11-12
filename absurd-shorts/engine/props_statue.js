// « La statue » (story 44): a man waiting for the bus; a pigeon lands on his head; he does not dare move; the town hall lists him as a historic monument.
// Conventions as in props.js (metres, front +Z, pivot at the floor); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, clamp01 } from './style.js';
import { grp, at } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const rnd = s => { let x = Math.sin(s * 127.1) * 43758.5453; return x - Math.floor(x); };

export const STATUE_PROPS = {
  // A cleaner's high-pressure lance and its jet: origin at the grip, the lance o.lance (0.9 m) along +Z. Between o.on [t0, t1] a pale blue jet o.len
  // (1.3 m) long leaves the nozzle along +Z, wobbling, and drops burst where it ends (it hits a face there). o.on may be a list of [t0, t1].
  waterJet(o) {
    const L = o.lance ?? 0.9, J = o.len ?? 1.3, g = grp(at(box(0.05, 0.15, 0.13, '#E3C24A', { outline: 0.005 }), 0, -0.02, -0.02), at(cyl(0.014, 0.014, L, '#5B5F67', 6), 0, 0.03, L / 2, PI / 2, 0, 0),
      at(cyl(0.024, 0.018, 0.08, '#2A2C31', 6), 0, 0.03, L + 0.02, PI / 2, 0, 0));
    const jm = new THREE.MeshBasicMaterial({ color: '#CFEFFF', transparent: true, opacity: 0.82, depthWrite: false });
    const jet = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.05, J, 8, 1, true).rotateX(PI / 2), jm); jet.position.set(0, 0.03, L + 0.06 + J / 2); jet.userData.noAO = true; g.add(jet);
    const dm = new THREE.MeshBasicMaterial({ color: '#E8F8FF', transparent: true, opacity: 0.9, depthWrite: false });
    const drops = Array.from({ length: 16 }, (_, i) => { const d = new THREE.Mesh(new THREE.BoxGeometry(0.025, 0.025, 0.025), dm); d.userData.noAO = true; d.userData.i = i; g.add(d); return d; });
    const ons = Array.isArray(o.on?.[0]) ? o.on : [o.on || [0, 1e9]], end = L + 0.06 + J;
    g.userData.update = t => {
      const on = ons.some(([a, b]) => t >= a && t < b); jet.visible = on;
      jet.scale.set(1 + 0.18 * Math.sin(t * 61), 1 + 0.18 * Math.cos(t * 53), 1); jet.position.x = 0.006 * Math.sin(t * 37);
      for (const d of drops) { const i = d.userData.i, ph = (t * 3.2 + rnd(i)) % 1, a = rnd(i + 7) * TAU, sp = 0.35 + 0.5 * rnd(i + 3); d.visible = on;
        d.position.set(Math.cos(a) * sp * ph, 0.03 + Math.sin(a) * sp * ph + 0.25 * ph * (1 - ph), end - 0.1 * ph - 0.05); d.scale.setScalar(1 - 0.6 * ph); }
    };
    g.userData.update(0); return g;
  },

  // A crane's hook coming down from out of the frame: a cable from y = o.top (world, 14 m) down to the hook block at the origin; o.sling: two straps hang
  // from the hook, o.slingLen (1.0 m) long, apart by o.slingW (0.5 m) (to go round a body under its arms). Move it with keys (to); the cable always
  // reaches o.top.
  craneHook(o) {
    const g = grp(), cab = cyl(0.016, 0.016, 1, '#2A2C31', 6, { pivot: 'bottom' }); g.add(cab);
    g.add(at(box(0.24, 0.3, 0.16, '#E3B02A', { outline: 0.006 }), 0, -0.05, 0), at(box(0.07, 0.07, 0.07, '#2A2C31'), 0, -0.24, 0));
    const hook = new THREE.Mesh(new THREE.TorusGeometry(0.07, 0.022, 6, 12, PI * 1.5), mat('#3A3D44')); hook.position.set(0, -0.36, 0); hook.rotation.z = PI * 0.25; g.add(hook);
    if (o.sling) { const sl = o.slingLen ?? 1.0, sw = o.slingW ?? 0.5;
      for (const sd of [-1, 1]) { const s = at(box(0.05, sl, 0.012, o.slingColor || '#E86A2A', { outline: 0.003 }), sd * sw / 4, -0.4 - sl / 2, 0, 0, 0, -sd * Math.atan2(sw / 2, sl)); g.add(s); } }
    const v = new THREE.Vector3(), sc = new THREE.Vector3();
    g.userData.update = () => { g.getWorldPosition(v); g.getWorldScale(sc); cab.position.y = 0.1; cab.scale.y = Math.max(0.01, ((o.top ?? 14) - v.y) / (sc.y || 1) - 0.1); };
    return g;
  },

  // A roundabout island: a round kerb o.r (3.0 m) across, grass, a ring of flowers and a few low shrubs; origin at its middle, at road level
  roundabout(o) {
    const R = o.r ?? 3.0, g = grp(at(cyl(R, R, 0.16, '#B9B4AA', 40, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(cyl(R - 0.16, R - 0.16, 0.02, o.grass || '#6FAE57', 40, { pivot: 'bottom' }), 0, 0.16, 0));
    const cols = o.flowers || ['#E8504A', '#F2C94C', '#F4F1E8', '#C96AB8'], n = Math.round(R * 18);
    for (let i = 0; i < n; i++) { const a = i / n * TAU + 0.07 * Math.sin(i * 3.1), r = R * (0.62 + 0.14 * rnd(i)), h = 0.12 + 0.08 * rnd(i + 11);
      g.add(at(box(0.012, h, 0.012, '#4F8A3E'), Math.cos(a) * r, 0.18 + h / 2, Math.sin(a) * r), at(box(0.07, 0.05, 0.07, cols[i % cols.length], { outline: 0.003 }), Math.cos(a) * r, 0.18 + h, Math.sin(a) * r)); }
    for (let i = 0; i < 6; i++) { const a = i / 6 * TAU + 0.4, r = R * 0.86; g.add(at(box(0.36, 0.3, 0.36, '#4F8A3E', { outline: 0.004 }), Math.cos(a) * r, 0.3, Math.sin(a) * r, 0, a, 0)); }
    return g;
  },
};
