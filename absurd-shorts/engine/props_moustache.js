// « La moustache » (story 67): props big enough to read on a phone (review 1: the razor was a 2 px blue sliver, there was no key, the jar was an
// opaque white box, the minister signed with no pen). Conventions as in props.js (metres, front +Z, pivot as said); every animated prop is a pure
// function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere } from './style.js';
import { grp, at } from './props.js';

const PI = Math.PI;

export const MOUSTACHE_PROPS = {
  // A safety razor held in a fist (pivot at the grip): a light handle o.len long (0.22) running down -Y with dark grip rings, a T head up +Y with a
  // steel blade edge along its top, o.color the handle
  // (review 2 of 67) o.style 'safety': a chrome safety razor that reads as one on a phone (the pale handle with rings read as a test tube): a short
  // dark knurled grip, a chrome neck and a wide chrome T head, the blade's dark edge showing between its plate and its cap
  razor(o) {
    if (o.style === 'safety') { const L = o.len ?? 0.15, g = grp();
      g.add(at(cyl(0.017, 0.015, L, '#3A3F46', 10, { outline: 0.004 }), 0, -L * 0.3, 0));
      for (let i = 0; i < 4; i++) g.add(at(cyl(0.019, 0.019, 0.008, '#C9D0D8', 10), 0, -L * 0.62 + i * 0.03, 0));
      g.add(at(cyl(0.011, 0.014, 0.05, '#D5DBE2', 10, { outline: 0.003 }), 0, L * 0.2 + 0.025, 0));
      const hy = L * 0.2 + 0.055;
      g.add(at(box(0.165, 0.016, 0.05, '#C4CBD3', { outline: 0.004 }), 0, hy, 0), at(box(0.172, 0.006, 0.054, '#1F2328'), 0, hy + 0.011, 0),
            at(box(0.168, 0.02, 0.05, '#F2F5F8', { outline: 0.004 }), 0, hy + 0.024, 0));
      g.add(at(box(0.14, 0.004, 0.004, '#FFFFFF'), 0, hy + 0.035, 0.024));   // a glint along the cap
      return g; }
    const L = o.len ?? 0.22, c = o.color || '#A8DAF2', g = grp();
    g.add(at(cyl(0.016, 0.013, L, c, 10, { outline: 0.004 }), 0, -L * 0.25, 0));
    for (let i = 0; i < 3; i++) g.add(at(cyl(0.018, 0.018, 0.01, '#4F7FA8', 10), 0, -L * 0.55 + i * 0.035, 0));
    g.add(at(box(0.012, 0.03, 0.012, '#C9CFD6'), 0, L * 0.26, 0));
    g.add(at(box(0.11, 0.026, 0.034, '#EEF2F6', { outline: 0.004 }), 0, L * 0.26 + 0.026, 0), at(box(0.116, 0.006, 0.038, '#9AA3AE'), 0, L * 0.26 + 0.042, 0));
    return g;
  },

  // A big gold key (pivot at the tip of its shaft, the shaft running out along +Z, the bow at the far end): o.len long (0.26); the bit's teeth at
  // the tip go into a keyhole; turn it with rotTo about Z
  bigKey(o) {
    const L = o.len ?? 0.26, G = o.color || '#E2B53C', g = grp();
    const sh = at(cyl(0.012, 0.012, L * 0.72, G, 8, { outline: 0.003 }), 0, 0, L * 0.36); sh.rotation.x = PI / 2; g.add(sh);
    g.add(at(box(0.012, 0.05, 0.05, G, { outline: 0.003 }), 0, -0.03, 0.05), at(box(0.012, 0.02, 0.016, G), 0, -0.06, 0.03));   // the bit and a tooth
    const bow = new THREE.Mesh(new THREE.TorusGeometry(0.05, 0.016, 8, 16), sh.material); bow.position.set(0, 0, L * 0.72 + 0.045); bow.rotation.y = PI / 2; g.add(bow);
    return g;
  },

  // A brass keyhole plate for a door (pivot at its middle, front +Z): an oval plate with a dark keyhole
  keyholePlate(o) {
    const s = o.s ?? 1, g = grp();
    const pl = at(box(0.07 * s, 0.13 * s, 0.012, '#C9A043', { outline: 0.004 }), 0, 0, 0.006); g.add(pl);
    g.add(at(cyl(0.012 * s, 0.012 * s, 0.004, '#121316', 10), 0, 0.012 * s, 0.013).rotateX(PI / 2), at(box(0.01 * s, 0.03 * s, 0.004, '#121316'), 0, -0.008 * s, 0.013));
    return g;
  },

  // A glass jar held upside down (pivot at its rim, the open mouth down -Y): clear walls o.h high (0.3) and o.r round (0.13) with white glints,
  // a frosted screw rim at the mouth and a closed bottom on top
  glassJar(o) {
    const h = o.h ?? 0.3, r = o.r ?? 0.13, g = grp();
    const glass = new THREE.MeshLambertMaterial({ color: '#DDF3FB', emissive: '#6FA8C0', emissiveIntensity: 0.15, transparent: true, opacity: 0.32, depthWrite: false, side: THREE.DoubleSide });
    const wall = new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, 20, 1, true), glass); wall.position.y = h / 2; wall.renderOrder = 3; g.add(wall);
    const top = new THREE.Mesh(new THREE.CircleGeometry(r, 20), glass); top.rotation.x = -PI / 2; top.position.y = h; top.renderOrder = 3; g.add(top);
    const edge = new THREE.MeshBasicMaterial({ color: '#2A5C70', transparent: true, opacity: 0.6 });
    for (const y of [0.004, h]) { const t = new THREE.Mesh(new THREE.TorusGeometry(r, 0.006, 4, 24), edge); t.rotation.x = PI / 2; t.position.y = y; g.add(t); }
    g.add(at(cyl(r * 1.04, r * 1.04, 0.03, '#E6EEF2', 20, { outline: 0.003 }), 0, 0.015, 0));   // the rim
    for (const [a, w] of [[0.5, 0.022], [0.8, 0.01]]) { const s = at(box(w, h * 0.7, 0.004, '#FFFFFF'), Math.sin(a) * r * 0.98, h * 0.5, Math.cos(a) * r * 0.98); s.rotation.y = a; g.add(s); }   // glints
    return g;
  },

  // A fountain pen (pivot at its middle, the nib down -Y): a black barrel o.len long (0.16) with a gold band, a gold clip and a gold nib
  pen(o) {
    const L = o.len ?? 0.16, g = grp();
    g.add(at(cyl(0.011, 0.011, L * 0.8, '#1A1B20', 10, { outline: 0.003 }), 0, L * 0.1, 0), at(cyl(0.0115, 0.0115, 0.012, '#D9AE3A', 10), 0, -L * 0.06, 0));
    g.add(at(box(0.004, L * 0.35, 0.006, '#D9AE3A'), 0.012, L * 0.3, 0));
    const nib = at(new THREE.Mesh(new THREE.ConeGeometry(0.008, L * 0.2, 8), new THREE.MeshLambertMaterial({ color: '#D9AE3A' })), 0, -L * 0.4, 0); nib.rotation.x = PI; g.add(nib);
    return g;
  },

  // Press flashes going off (pivot at the middle): o.n bright starbursts spread over o.w x o.h, each popping at its own time in o.at (or o.rate a
  // second from o.from), a white disc and four rays, gone in 0.12 s
  flashBursts(o) {
    const n = o.n ?? 5, W = o.w ?? 2.4, H = o.h ?? 1.2, g = grp(), fl = [];
    const m = new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.95, depthWrite: false });
    for (let i = 0; i < n; i++) { const f = grp(); const d = new THREE.Mesh(new THREE.CircleGeometry(0.07, 12), m); f.add(d);
      for (let k = 0; k < 4; k++) { const ray = new THREE.Mesh(new THREE.PlaneGeometry(0.02, 0.3), m); ray.rotation.z = k * PI / 4 + PI / 8; f.add(ray); }
      f.position.set((((i * 0.618) % 1) - 0.5) * W, (((i * 0.382 + 0.2) % 1) - 0.5) * H, 0); f.visible = false; g.add(f); fl.push(f); }
    const times = o.at || Array.from({ length: n }, (_, i) => (o.from ?? 0.1) + i / (o.rate ?? 6));
    g.userData.update = t => fl.forEach((f, i) => { const u = t - times[i % times.length]; f.visible = u >= 0 && u < 0.12; if (f.visible) f.scale.setScalar(0.6 + 3.5 * u); });
    g.userData.update(-1); return g;
  },
};
