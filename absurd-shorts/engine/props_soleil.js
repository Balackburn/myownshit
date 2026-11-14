// « Le coup de soleil » (story 62, cycle 24): a man got sunburnt. He turned bright red. At night he lights up the whole neighbourhood. The town hall
// installed him as a red light. The cars stop in front of him all day. Yesterday a lorry honked at him. He turned green with fear. All the cars went
// through. The town hall painted him red again. Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is
// a pure function of the shot time.
import * as THREE from 'three';
import { mat, box, cyl } from './style.js';
import { grp, at } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const list = v => [].concat(v ?? []);
const clamp01 = x => Math.max(0, Math.min(1, x));
const eo = x => 1 - Math.pow(1 - clamp01(x), 3);

export const SOLEIL_PROPS = {
  // A striped deckchair (pivot at the floor, the sitter faces +Z): a wooden frame leaning back and a sagging canvas of o.colors stripes; the seat is
  // 0.32 m high at the front, the back reclines to 0.95 m
  deckChair(o) {
    const g = grp(), cols = o.colors || ['#E8463A', '#F4F1E8'], W = 0.56;
    for (const s of [-1, 1]) { g.add(at(box(0.04, 0.04, 1.05, '#B88A5A', { outline: 0.006 }), s * W / 2, 0.42, -0.05, 0.62, 0, 0), at(box(0.04, 0.04, 0.85, '#B88A5A', { outline: 0.006 }), s * W / 2, 0.3, 0.12, -0.75, 0, 0)); }
    const n = 6;
    for (let i = 0; i < n; i++) { const st = box(W / n, 0.012, 0.86, cols[i % cols.length]); st.position.set(-W / 2 + (i + 0.5) * W / n, 0.5, -0.08); st.rotation.x = 0.66; g.add(st); }
    g.add(at(box(W + 0.06, 0.04, 0.04, '#B88A5A'), 0, 0.84, -0.42), at(box(W + 0.06, 0.04, 0.04, '#B88A5A'), 0, 0.3, 0.33));
    return g;
  },

  // A fried egg cooking where it is put (pivot at its underside, its face +Y: lay it on a forehead with the head's frame): from o.at the white spreads
  // out from the cracked egg in 0.25 s, bubbling at its edge, the yolk sits up, little puffs of steam rise from o.at + 0.2 for o.dur (1.5 s);
  // o.r (0.12) the white's radius; before o.at only the whole egg, held (o.whole false: none)
  friedEgg(o) {
    const R = o.r ?? 0.12, g = grp(), wm = new THREE.MeshLambertMaterial({ color: '#FBFAF4' });
    const white = new THREE.Mesh(new THREE.CylinderGeometry(R, R * 1.02, 0.012, 18), wm); white.position.y = 0.006; g.add(white);
    const blobs = []; for (let i = 0; i < 6; i++) { const b = new THREE.Mesh(new THREE.SphereGeometry(R * 0.32, 8, 6), wm); const a = i / 6 * TAU + 0.3; b.userData.p0 = [Math.cos(a) * R * 0.85, Math.sin(a) * R * 0.85]; b.scale.y = 0.25; g.add(b); blobs.push(b); }
    const yolk = new THREE.Mesh(new THREE.SphereGeometry(R * 0.36, 12, 8), new THREE.MeshLambertMaterial({ color: '#F6B21E' })); yolk.position.set(R * 0.08, 0.02, -R * 0.05); yolk.scale.y = 0.6; g.add(yolk);
    const whole = new THREE.Mesh(new THREE.SphereGeometry(R * 0.42, 12, 10), new THREE.MeshLambertMaterial({ color: '#F2E6D0' })); whole.scale.y = 1.3; whole.position.y = R * 0.5; if (o.whole !== false) g.add(whole);
    const puffs = []; for (let i = 0; i < 4; i++) { const p = new THREE.Mesh(new THREE.SphereGeometry(R * 0.28, 8, 6), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0, depthWrite: false })); g.add(p); puffs.push(p); }
    g.userData.update = t => {
      const u = t - (o.at ?? 0), k = u < 0 ? 0 : eo(u / 0.25);
      whole.visible = u < 0.02; white.visible = yolk.visible = u >= 0; blobs.forEach((b, i) => { b.visible = u >= 0; b.scale.set(1 + 0.25 * Math.sin(t * 22 + i * 1.7), 0.25, 1 + 0.25 * Math.sin(t * 22 + i * 1.7)); });
      white.scale.set(Math.max(0.05, k), 1, Math.max(0.05, k)); blobs.forEach(b => b.position.set(b.userData.p0[0] * k, 0.008, b.userData.p0[1] * k)); yolk.scale.set(Math.max(0.2, k), 0.6 * Math.max(0.3, k), Math.max(0.2, k));
      puffs.forEach((p, i) => { const v = (u - 0.2 - i * 0.18) % 0.72, on = u > 0.2 + i * 0.18 && u < (o.dur ?? 1.5) + 0.2; p.visible = on; if (!on) return;
        const w = clamp01(v / 0.72); p.position.set(Math.sin(i * 2.1) * R * 0.5, 0.05 + w * R * 3.2, Math.cos(i * 2.1) * R * 0.4); p.scale.setScalar(0.6 + w * 1.2); p.material.opacity = 0.75 * (1 - w); });
    };
    g.userData.update(0); return g;
  },

  // Moths (pivot at the light they circle): o.n (6) little grey-white moths fluttering round it in wobbling loops of radius o.r (0.35), wings beating
  moths(o) {
    const n = o.n ?? 6, R = o.r ?? 0.35, g = grp(), ms = [];
    for (let i = 0; i < n; i++) { const m = grp(), wm = new THREE.MeshLambertMaterial({ color: i % 2 ? '#E6E0D2' : '#CFC6B4', side: THREE.DoubleSide });
      const wl = new THREE.Mesh(new THREE.PlaneGeometry(0.05, 0.035), wm), wr = wl.clone(); wl.position.x = -0.025; wr.position.x = 0.025; m.add(wl, wr, at(box(0.012, 0.012, 0.03, '#6E6658'), 0, 0, 0)); g.add(m); ms.push({ m, wl, wr, ph: i * 1.7, rr: R * (0.7 + 0.5 * ((i * 37) % 10) / 10), sp: 4.5 + (i % 3) }); }
    g.userData.update = t => ms.forEach(q => { const a = t * q.sp + q.ph; q.m.position.set(Math.cos(a) * q.rr, Math.sin(a * 1.7) * q.rr * 0.5, Math.sin(a) * q.rr); q.m.rotation.y = -a; const f = Math.sin(t * 40 + q.ph) * 0.9; q.wl.rotation.y = f; q.wr.rotation.y = -f; });
    g.userData.update(0); return g;
  },

  // A traffic light made for a head (pivot at the foot of its pole): a dark green box o.w (0.8) wide on a pole o.pole (2.0) high, its front panel
  // pierced by three round holes (radius o.hole 0.24) with hoods over them, at 0.32, 0.85 and 1.38 m over the box's base; a ring round each hole in
  // its colour (green, amber, red, from the bottom). A man standing behind the panel shows his face through a hole; the box is open at the back;
  // o.column: a cabinet instead of the pole, his body inside it; o.shake [[t, k], ...]: it rattles from t; o.open: which hole is open when
  headLight(o) {
    const W = o.w ?? 0.8, H = 1.7, D = 0.34, P = o.pole ?? 2.0, HR = o.hole ?? 0.24, C = o.color || '#2F4A3A', g = grp(), ys = [0.32, 0.85, 1.38], rc = ['#3FB84A', '#F2A81E', '#E2312A'];
    const sh = new THREE.Shape(); sh.moveTo(-W / 2, 0); sh.lineTo(W / 2, 0); sh.lineTo(W / 2, H); sh.lineTo(-W / 2, H); sh.lineTo(-W / 2, 0);
    for (const y of ys) { const h = new THREE.Path(); h.absarc(0, y, HR, 0, TAU, true); sh.holes.push(h); }
    const panel = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: 0.04, bevelEnabled: false, curveSegments: 20 }), mat(C)); panel.position.set(0, P, D / 2 - 0.04); panel.castShadow = true; g.add(panel);
    g.add(at(box(0.04, H, D, C, { pivot: 'bottom', outline: 0.008 }), -W / 2 + 0.02, P, 0), at(box(0.04, H, D, C, { pivot: 'bottom', outline: 0.008 }), W / 2 - 0.02, P, 0),
      at(box(W, 0.04, D, C, { outline: 0.008 }), 0, P + H - 0.02, 0), at(box(W, 0.04, D, C, { outline: 0.008 }), 0, P + 0.02, 0));
    ys.forEach((y, i) => { const ring = new THREE.Mesh(new THREE.TorusGeometry(HR + 0.02, 0.022, 8, 28), new THREE.MeshLambertMaterial({ color: rc[i], emissive: rc[i], emissiveIntensity: 0.25 })); ring.position.set(0, P + y, D / 2 + 0.005); g.add(ring);
      const hood = new THREE.Mesh(new THREE.CylinderGeometry(HR + 0.05, HR + 0.05, 0.22, 20, 1, true, -PI / 2, PI), mat(C)); hood.material.side = THREE.DoubleSide; hood.rotation.x = PI / 2; hood.position.set(0, P + y + 0.01, D / 2 + 0.11); g.add(hood); });
    if (o.column) g.add(at(box(W * 0.9, P, 0.55, '#3C3F44', { pivot: 'bottom', outline: 0.01 }), 0, 0, -0.08), at(box(W * 0.94, 0.05, 0.6, '#2E3135', { outline: 0.006 }), 0, P - 0.02, -0.08));   // o.column: a cabinet under it (his body hides inside)
    else g.add(at(cyl(0.07, 0.08, P, '#3C3F44', 10, { pivot: 'bottom' }), 0, 0, 0), at(cyl(0.18, 0.2, 0.08, '#3C3F44', 12), 0, 0.04, 0));
    // (stills 1 of 62) the unlit holes behind dark glass (open, they showed his suit and tie); o.open [[t, i], ...]: from t, hole i (0 green .. 2 red)
    // is the open one, where his face shows (default: the red one)
    const glass = ys.map(y => { const d = new THREE.Mesh(new THREE.CircleGeometry(HR + 0.004, 24), new THREE.MeshLambertMaterial({ color: '#1A2420', emissive: '#0C1210' })); d.position.set(0, P + y, D / 2 + 0.002); g.add(d); return d; });
    const opens = o.open ? o.open : [[0, 2]];
    g.userData.update = t => { let a = 0; for (const [t0, k] of list(o.shake)) { const u = t - t0; if (u > 0 && u < 0.8) a += k * Math.exp(-u * 5) * Math.sin(u * 46); } g.rotation.z = a;
      let op = opens[0][1]; for (const [t0, i] of opens) if (t >= t0) op = i; glass.forEach((d, i) => { d.visible = i !== op; }); };
    g.userData.update(0);
    return g;
  },

  // A box lorry (pivot at the floor, it faces +X like the car prop): a cab with a windscreen, a tall cargo box, six wheels, a chrome grille, two air
  // horns on the cab roof; o.color (cab), o.box (cargo box)
  truck(o) {
    const C = o.color || '#2F6FB2', BX = o.box || '#ECE8DE', g = grp();
    g.add(at(box(1.9, 1.75, 2.3, C, { pivot: 'bottom', outline: 0.012 }), 2.6, 0.55, 0), at(box(0.04, 0.85, 2.0, '#BFE3F0'), 3.56, 1.6, 0), at(box(0.06, 0.55, 1.9, '#C9CED4'), 3.57, 0.85, 0),
      at(box(4.6, 2.7, 2.4, BX, { pivot: 'bottom', outline: 0.014 }), -0.75, 0.6, 0), at(box(6.9, 0.22, 2.2, '#3C3F44'), 0.4, 0.45, 0));
    for (const x of [-2.4, -1.4, 2.9]) for (const z of [-1.08, 1.08]) { const w = cyl(0.48, 0.48, 0.32, '#22252A', 14); w.rotation.x = PI / 2; w.position.set(x, 0.48, z); g.add(w); }
    for (const z of [-0.6, 0.6]) { const h = cyl(0.07, 0.12, 0.55, '#D8DCE0', 10); h.rotation.z = -PI / 2; h.position.set(3.0, 2.42, z); g.add(h); }
    for (const z of [-0.85, 0.85]) g.add(at(box(0.04, 0.16, 0.3, '#FFF3C2', { emissive: '#FFE38A', noGrain: true }), 3.58, 0.75, z));
    return g;
  },

  // A glow (pivot at its centre): a coloured point light of o.k (6) over o.dist (7 m) from o.at, so a glowing face lights the walls round it
  glowLight(o) {
    const g = grp(), l = new THREE.PointLight(o.color || '#FF3A22', 0, o.dist ?? 7, 1.4); g.add(l);
    g.userData.update = t => { l.intensity = (o.k ?? 6) * clamp01((t - (o.at ?? 0)) / 0.2) * (1 + 0.04 * Math.sin(t * 9)); };
    g.userData.update(0); return g;
  },
};
