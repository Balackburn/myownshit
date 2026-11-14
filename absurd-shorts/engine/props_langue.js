// « La langue » (story 64, cycle 26): a man stuck his tongue on a frozen lamp post. The firemen pulled for two hours. His tongue now crosses the
// street. The town hall hung the Christmas lights on it. The mayor pressed the button: everything blinks, him too. Yesterday the thaw: his tongue
// came back in one go, with the lights. He has been blinking ever since. Conventions as in props.js (metres, front +Z, pivot at the floor unless
// said); every animated prop is a pure function of the shot time. The tongue itself is a tether (director3: td.lift, td.snap, td.bulbs, td.birds).
import * as THREE from 'three';
import { box, cyl } from './style.js';
import { grp, at } from './props.js';

const PI = Math.PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const eo = x => 1 - Math.pow(1 - clamp01(x), 3);
const hash = n => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
let _glowTex = null;
function glowTex() {
  if (_glowTex) return _glowTex;
  const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d'), gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.3, 'rgba(255,255,255,0.6)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
  _glowTex = new THREE.CanvasTexture(c); return _glowTex;
}
function frostTex() {
  const c = document.createElement('canvas'); c.width = 128; c.height = 512; const g = c.getContext('2d');
  g.fillStyle = '#EEF8FF'; g.fillRect(0, 0, 128, 512);
  for (let i = 0; i < 90; i++) { const x = hash(i) * 128, y = hash(i + 50) * 512, l = 8 + 30 * hash(i + 90); g.strokeStyle = hash(i + 7) > 0.5 ? 'rgba(160,205,235,0.75)' : 'rgba(255,255,255,0.95)'; g.lineWidth = 1 + 2 * hash(i + 3);
    g.beginPath(); g.moveTo(x, y); g.lineTo(x + (hash(i + 11) - 0.5) * l * 0.6, y + l); g.stroke(); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; return t;
}
function burstTex() {   // a frost star: white crystals out from a point, pale blue tips
  const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d'); g.translate(128, 128); g.lineCap = 'round';
  for (let i = 0; i < 14; i++) { const a = i / 14 * 2 * PI + 0.2 * hash(i), L = 70 + 50 * hash(i + 20); g.strokeStyle = 'rgba(255,255,255,0.95)'; g.lineWidth = 7;
    g.beginPath(); g.moveTo(0, 0); g.lineTo(Math.cos(a) * L, Math.sin(a) * L); g.stroke();
    for (const f of [0.45, 0.7]) { const bx = Math.cos(a) * L * f, by = Math.sin(a) * L * f; g.lineWidth = 4; g.strokeStyle = 'rgba(200,232,255,0.95)';
      for (const sd of [-1, 1]) { g.beginPath(); g.moveTo(bx, by); g.lineTo(bx + Math.cos(a + sd * 0.7) * 22, by + Math.sin(a + sd * 0.7) * 22); g.stroke(); } } }
  g.fillStyle = 'rgba(255,255,255,1)'; g.beginPath(); g.arc(0, 0, 26, 0, 2 * PI); g.fill();
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

export const LANGUE_PROPS = {
  // Frost and icicles on a street lamp (put it at the same place as a `streetLamp`, pivot at the foot of the pole; o.h 4.2, the pole's radius o.r0 0.1
  // at the foot and o.r1 0.07 at the top, the arm along +X like the lamp's): a frosted sleeve up the pole, icicles under the arm and the lamp head;
  // o.lick [y, angle (deg about Y, 0 = toward +Z)]: where a tongue touches, a frost star that grows from o.lickAt; o.meltAt / o.meltDur (1.2 s): the
  // thaw: icicles shrink and drip, the frost goes clear, a puddle spreads at the foot, a drop runs off the star every so often
  iceSleeve(o) {
    const H = o.h ?? 4.2, r0 = o.r0 ?? 0.1, r1 = o.r1 ?? 0.07, y0 = o.y0 ?? 0.25, y1 = H - 0.08, g = grp();
    const rAt = y => r0 + (r1 - r0) * (y / H);
    const fm = new THREE.MeshLambertMaterial({ map: frostTex(), color: '#FFFFFF', transparent: true, opacity: 0.9, emissive: '#3A5566', emissiveIntensity: 0.25 });
    const sleeve = new THREE.Mesh(new THREE.CylinderGeometry(rAt(y1) + 0.014, rAt(y0) + 0.014, y1 - y0, 10, 1, true), fm); sleeve.position.y = (y0 + y1) / 2; g.add(sleeve);
    const im = new THREE.MeshLambertMaterial({ color: '#D9F1FF', transparent: true, opacity: 0.88, emissive: '#5A8AA8', emissiveIntensity: 0.35 }), ics = [];
    const spots = o.icicles || [[0.12, 0.2], [0.24, 0.34], [0.36, 0.16], [0.48, 0.28], [0.6, 0.22], [0.72, 0.38], [0.84, 0.3], [0.95, 0.2], [0.78, 0.18]];
    spots.forEach(([x, l], i) => { const c = new THREE.Mesh(new THREE.ConeGeometry(0.022 + 0.014 * hash(i + 4), 1, 6), im); c.rotation.x = PI; c.scale.y = l;
      const y = x > 0.62 ? H - 0.2 : H - 0.09; c.position.set(x, y - l / 2, (hash(i + 9) - 0.5) * 0.08); c.userData.l = l; c.userData.y = y; g.add(c); ics.push(c); });
    // o.collar [y, n (8)]: a frosted ring with n icicles round the pole at height y (in a close shot the thaw shows there: they drip and shrink)
    if (o.collar) { const [cy, cn = 8] = o.collar, cr = rAt(cy) + 0.02, ring = new THREE.Mesh(new THREE.TorusGeometry(cr, 0.024, 6, 16), im); ring.rotation.x = PI / 2; ring.position.y = cy; g.add(ring);
      for (let i = 0; i < cn; i++) { const a = i / cn * 2 * PI, l = 0.09 + 0.13 * hash(i + 31), c = new THREE.Mesh(new THREE.ConeGeometry(0.015 + 0.008 * hash(i + 5), 1, 6), im);
        c.rotation.x = PI; c.scale.y = l; c.position.set(Math.sin(a) * cr, cy - l / 2, Math.cos(a) * cr); c.userData.l = l; c.userData.y = cy; g.add(c); ics.push(c); } }
    const drops = ics.map((c, i) => { const d = new THREE.Mesh(new THREE.SphereGeometry(0.014, 6, 4), new THREE.MeshLambertMaterial({ color: '#BFE6FF', transparent: true, opacity: 0.9 })); d.visible = false; g.add(d); return d; });
    let star = null, starDrop = null;
    if (o.lick) { const [ly, la] = o.lick, a = la * PI / 180, rr = rAt(ly) + 0.018;
      star = new THREE.Mesh(new THREE.PlaneGeometry(0.34, 0.34), new THREE.MeshBasicMaterial({ map: burstTex(), transparent: true, depthWrite: false }));
      star.position.set(Math.sin(a) * rr, ly, Math.cos(a) * rr); star.rotation.y = a; g.add(star);
      starDrop = new THREE.Mesh(new THREE.SphereGeometry(0.016, 6, 4), new THREE.MeshLambertMaterial({ color: '#BFE6FF', transparent: true, opacity: 0.9 })); starDrop.visible = false; g.add(starDrop); starDrop.userData.p = star.position.clone(); }
    const puddle = new THREE.Mesh(new THREE.CircleGeometry(1, 18), new THREE.MeshLambertMaterial({ color: '#A8C6D8', transparent: true, opacity: 0.6, depthWrite: false })); puddle.rotation.x = -PI / 2; puddle.position.y = 0.012; puddle.visible = false; g.add(puddle);
    g.userData.update = t => {
      const m = o.meltAt == null ? 0 : clamp01((t - o.meltAt) / (o.meltDur ?? 1.2));
      fm.opacity = 0.9 - 0.7 * m; sleeve.visible = fm.opacity > 0.05;
      ics.forEach((c, i) => { const l = c.userData.l * (1 - 0.75 * m); c.scale.y = Math.max(0.01, l); c.position.y = c.userData.y - l / 2;
        const d = drops[i]; if (m <= 0) { d.visible = false; return; } const per = 0.42 + 0.2 * hash(i), ph = ((t - o.meltAt + hash(i + 2) * per) % per) / per, fall = 4.9 * (ph * per) ** 2;
        d.visible = fall < 2.5; d.position.set(c.position.x, c.userData.y - l - fall, c.position.z); });
      if (star) { const k = o.lickAt == null ? 1 : eo((t - o.lickAt) / 0.25); star.scale.setScalar(Math.max(0.01, k)); star.visible = k > 0.01; star.material.opacity = 1 - 0.85 * m;
        if (m > 0) { const per = 0.5, ph = ((t - o.meltAt) % per) / per, fall = 4.9 * (ph * per) ** 2; starDrop.visible = true; starDrop.position.copy(starDrop.userData.p); starDrop.position.y -= 0.04 + fall; } else starDrop.visible = false; }
      puddle.visible = m > 0; puddle.scale.setScalar(Math.max(0.01, 0.55 * m)); };
    g.userData.update(0); return g;
  },

  // An inauguration button (pivot at the floor, front +Z): a cream pedestal with gold bands, a yellow and black ring on top and a big red dome
  // (top at about 1.02 m); o.pressAt: the dome goes in and squashes for a quarter of a second, then springs back past its rest; o.cable (m): a black
  // cable from its foot along -X on the ground
  bigButton(o) {
    const g = grp(cyl(0.2, 0.24, 0.92, '#F2ECE0', 12, { pivot: 'bottom' }), at(cyl(0.245, 0.245, 0.05, '#D4AF37', 12), 0, 0.05, 0), at(cyl(0.205, 0.205, 0.05, '#D4AF37', 12), 0, 0.88, 0),
      at(cyl(0.18, 0.18, 0.05, '#F5C518', 12), 0, 0.94, 0));
    for (let i = 0; i < 6; i++) g.add(at(box(0.05, 0.052, 0.13, '#1C1C1E'), Math.sin(i / 6 * 2 * PI) * 0.12, 0.94, Math.cos(i / 6 * 2 * PI) * 0.12, 0, i / 6 * 2 * PI, 0));
    const dome = new THREE.Mesh(new THREE.SphereGeometry(0.13, 16, 10, 0, 2 * PI, 0, PI / 2), new THREE.MeshLambertMaterial({ color: '#E8352F', emissive: '#7A0E0B', emissiveIntensity: 0.35 }));
    dome.position.y = 0.965; g.add(dome);
    if (o.cable) g.add(at(box(o.cable, 0.025, 0.025, '#1C1C1E'), -o.cable / 2, 0.012, 0.1));
    g.userData.update = t => { const u = o.pressAt == null ? -1 : t - o.pressAt; let sy = 1, sx = 1, dy = 0;
      if (u >= 0 && u < 0.06) { const k = u / 0.06; sy = 1 - 0.5 * k; sx = 1 + 0.15 * k; dy = -0.03 * k; }
      else if (u >= 0.06 && u < 0.3) { sy = 0.5; sx = 1.15; dy = -0.03; }
      else if (u >= 0.3 && u < 0.5) { const k = (u - 0.3) / 0.2; sy = 0.5 + 0.5 * k + 0.2 * Math.sin(PI * k); sx = 1.15 - 0.15 * k; dy = -0.03 * (1 - k); }
      dome.scale.set(sx, sy, sx); dome.position.y = 0.965 + dy; };
    g.userData.update(0); return g;
  },

  // Christmas lights inside a belly, seen through the shirt (hang it on the torso joint, its middle on the shirt, facing +Z): o.n (5) soft glows in
  // red, green, gold and blue on a small zigzag, each with a bright core, chasing like the garland (each one dark one beat in three, o.period 0.3 s,
  // from o.at), and a light that takes their colour onto the shirt and the hands
  bellyLights(o) {
    const g = grp(), cols = o.colors || ['#FF3B3B', '#3BD45A', '#FFC93B', '#3B8BFF', '#FF3B3B'], n = o.n ?? 5, sp = o.spread ?? 0.075, out = [];
    for (let k = 0; k < n; k++) { const col = new THREE.Color(cols[k % cols.length]);
      const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex(), color: col, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0.95 })); halo.scale.setScalar(o.size ?? 0.17);
      const core = new THREE.Mesh(new THREE.CircleGeometry(0.014, 10), new THREE.MeshBasicMaterial({ color: col.clone().lerp(new THREE.Color('#FFFFFF'), 0.55), transparent: true, depthWrite: false }));
      const x = (k - (n - 1) / 2) * sp * 0.7, y = (k % 2 ? 1 : -1) * sp * 0.5 - k * 0.012; halo.position.set(x, y, 0.01); core.position.set(x, y, 0.012);
      g.add(halo, core); out.push({ halo, core, col, k }); }
    const light = new THREE.PointLight('#FFFFFF', 0, o.dist ?? 1.4, 1.6); light.position.set(0, 0, 0.12); g.add(light);
    g.userData.update = t => { const on = t >= (o.at ?? 0), per = o.period ?? 0.3, beat = Math.floor((t - (o.at ?? 0)) / per); let lit = 0; const mix = new THREE.Color(0, 0, 0);
      out.forEach(e => { const l = on && (beat + e.k) % 3 !== 0; e.halo.visible = l; e.core.visible = on; e.core.material.opacity = l ? 1 : 0.35; if (l) { lit++; mix.add(e.col); } });
      light.intensity = on && lit ? (o.k ?? 1.6) : 0; if (lit) light.color.copy(mix.multiplyScalar(1 / lit)); };
    g.userData.update(0); return g;
  },
  // Snow piling up on a head or a helmet (hang it on the head joint at the top of the head, pivot at its bottom): a white mound with lumps, o.w
  // (0.3) wide, growing from nothing to o.h (0.22 m) between o.t0 and o.t1: time passing while they stand there
  snowCap(o) {
    const W = o.w ?? 0.3, g = grp(), m = new THREE.MeshLambertMaterial({ color: '#FAFCFF', emissive: '#4A5A66', emissiveIntensity: 0.15 }), lumps = [];
    const base = new THREE.Mesh(new THREE.CylinderGeometry(W * 0.44, W * 0.52, 1, 9), m); base.position.y = 0.5; lumps.push(base);
    for (let i = 0; i < 4; i++) { const b = new THREE.Mesh(new THREE.SphereGeometry(W * (0.2 + 0.06 * hash(i + 3)), 8, 6), m); b.position.set((hash(i) - 0.5) * W * 0.5, 1.0, (hash(i + 8) - 0.5) * W * 0.4); lumps.push(b); }
    const pile = grp(...lumps); g.add(pile);
    g.userData.update = t => { const k = clamp01((t - (o.t0 ?? 0)) / Math.max(0.05, (o.t1 ?? 1) - (o.t0 ?? 0))), h = Math.max(0.005, (o.h ?? 0.22) * k);
      pile.scale.set(0.6 + 0.4 * k, h, 0.6 + 0.4 * k); pile.visible = k > 0.02; lumps.slice(1).forEach(b => { b.scale.set(1, Math.min(4, 0.06 / h), 1); }); };
    g.userData.update(0); return g;
  },
};
