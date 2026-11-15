// « Le poisson rouge » (story 65, cycle 27): this man bought a goldfish. The seller said three grains a day; he put three hundred. The next
// day it took the bathtub, the day after the municipal pool. The town hall closed the pool; the fish moved into the lake and ate every pedal
// boat. The ducks sued; the judge found for the fish; the ducks appealed; the fish ate the courthouse. The army was sent; the fish took the tanks
// for grains. The government negotiated: he got the sea, and guards the coast for three grains a day. Conventions as in props.js (metres, front
// +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const eo = x => 1 - Math.pow(1 - clamp01(x), 3);
const hash = n => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const L = c => new THREE.MeshLambertMaterial({ color: c });
const glass = (c, op) => new THREE.MeshLambertMaterial({ color: c, transparent: true, opacity: op, depthWrite: false, side: THREE.DoubleSide });
const ball = (r, c, seg = 10) => new THREE.Mesh(new THREE.SphereGeometry(r, seg, Math.max(6, seg - 2)), typeof c === 'string' ? L(c) : c);

// a small goldfish (length s, facing +Z): a bright orange body lit a little from inside (pass 2: the fish in the bag and the bowl read as an empty
// grey disc and a cream speck through the water), a dorsal fin, a fan tail, two black eyes that can pop (userData.eyes)
function miniFish(s = 0.06) {
  const orange = new THREE.MeshLambertMaterial({ color: '#FF6A12', emissive: '#6A2400', transparent: true }), finM = new THREE.MeshLambertMaterial({ color: '#FFA238', emissive: '#4A2000', transparent: true });
  const g = new THREE.Group(), body = ball(s * 0.5, orange); body.scale.set(0.55, 0.66, 1); g.add(body);
  const tail = new THREE.Mesh(new THREE.ConeGeometry(s * 0.36, s * 0.55, 6), finM); tail.rotation.x = PI / 2; tail.position.z = -s * 0.64; tail.scale.set(0.3, 1, 1); g.add(tail);
  const dorsal = new THREE.Mesh(new THREE.ConeGeometry(s * 0.14, s * 0.3, 4), finM); dorsal.position.set(0, s * 0.33, -s * 0.05); dorsal.scale.set(0.3, 1, 1.6); g.add(dorsal);
  const eyes = [-1, 1].map(sd => { const e = new THREE.Group(), w = ball(s * 0.13, '#FFFFFF', 8), p = ball(s * 0.075, '#111111', 6); p.position.z = s * 0.08; e.add(w, p); e.position.set(sd * s * 0.21, s * 0.1, s * 0.3); g.add(e); return e; });
  g.traverse(n => { if (n.isMesh) { n.renderOrder = 6; if (!n.material.transparent) { n.material = n.material.clone(); n.material.transparent = true; } } });   // drawn after the glass and the water (two pale layers over it washed it to cream)
  g.userData.eyes = eyes; g.userData.tail = tail; return g;
}

export const POISSON_PROPS = {
  // A pet-shop bag with a goldfish in it (pivot at the knot on top, hang it from a hand): a clear bag of water, the fish circling inside
  fishBag(o) {
    const g = grp(), s = o.s ?? 1, R = 0.1 * s;
    const water = ball(R, glass('#8FD3F2', 0.3), 14); water.scale.y = 1.12; water.position.y = -0.17 * s; g.add(water);
    const shell = ball(R * 1.06, glass('#FFFFFF', 0.1), 14); shell.scale.y = 1.15; shell.position.y = -0.17 * s; g.add(shell);
    const neck = new THREE.Mesh(new THREE.ConeGeometry(R * 0.75, 0.09 * s, 10, 1, true), glass('#FFFFFF', 0.22)); neck.rotation.x = PI; neck.position.y = -0.05 * s; g.add(neck);
    g.add(at(ball(0.012 * s, '#F4F4F4', 6), 0, 0, 0));
    const f = miniFish(o.fishS ?? 0.13 * s); g.add(f);
    g.userData.grip = [0, 0, 0];
    g.userData.update = t => { const a = t * 1.6; f.position.set(Math.sin(a) * R * 0.2, -0.18 * s + 0.01 * Math.sin(t * 3), Math.cos(a) * R * 0.2); f.rotation.y = a + PI / 2; f.userData.tail.rotation.y = 0.4 * Math.sin(t * 12); };
    g.userData.update(0); return g;
  },

  // A round fishbowl (pivot at its foot) with gravel and a goldfish; o.flakes [t0, t1, n (140)]: fish food poured from o.pour (0.42 m over the rim)
  // between t0 and t1, the flakes piling up on the water into a mound that rises over the rim and spills; o.popAt: the fish's eyes pop out
  fishBowl(o) {
    const g = grp(), R = o.r ?? 0.16, cy = R * 0.95;
    const bowl = new THREE.Mesh(new THREE.SphereGeometry(R, 18, 14, 0, 2 * PI, 0.32, PI - 0.32), glass('#E8F6FF', 0.24)); bowl.position.y = cy; g.add(bowl);
    const water = new THREE.Mesh(new THREE.SphereGeometry(R * 0.96, 18, 12, 0, 2 * PI, 0.7, PI - 0.7), glass('#7CCBEB', 0.34)); water.position.y = cy; g.add(water);
    const wy = cy + R * 0.96 * Math.cos(0.7), wr = R * 0.96 * Math.sin(0.7);
    const surf = new THREE.Mesh(new THREE.CircleGeometry(wr, 18), glass('#A9E0F5', 0.55)); surf.rotation.x = -PI / 2; surf.position.y = wy; g.add(surf);
    g.add(at(new THREE.Mesh(new THREE.CylinderGeometry(R * 0.55, R * 0.6, 0.03, 14), L('#C89A6A')), 0, 0.03, 0));
    const f = miniFish(o.fishS ?? 0.14); g.add(f);
    const F = o.flakes, n = F ? (F[2] ?? 140) : 0, cols = ['#F5B83C', '#E8542A', '#F2D06B', '#D9452B'], flakes = [];
    for (let i = 0; i < n; i++) { const m = new THREE.Mesh(new THREE.BoxGeometry(0.016, 0.003, 0.012), L(cols[i % 4])); m.visible = false; g.add(m); flakes.push(m); }
    const pile = new THREE.Mesh(new THREE.ConeGeometry(wr * 1.05, 1, 14), L('#E9A33A')); pile.position.y = wy; pile.visible = false; g.add(pile);
    const pourY = wy + (o.pour ?? 0.42);
    g.userData.update = t => {
      const a = t * 1.3; f.position.set(Math.sin(a) * R * 0.24, cy - R * 0.12 + 0.012 * Math.sin(t * 2.6), Math.cos(a) * R * 0.24); f.rotation.y = a + PI / 2; f.userData.tail.rotation.y = 0.35 * Math.sin(t * 10);
      const pop = o.popAt == null ? 0 : eo((t - o.popAt) / 0.12); f.userData.eyes.forEach(e => e.scale.setScalar(1 + 1.8 * pop));
      if (pop > 0) { f.rotation.y = PI * 0.1; f.position.set(0, cy - R * 0.05, R * 0.2); }
      if (!F) return;
      const landed = clamp01((t - F[0] - 0.25) / Math.max(0.05, F[1] - F[0])), h = 0.13 * landed;
      pile.visible = h > 0.004; pile.scale.set(1 + 0.25 * landed, h, 1 + 0.25 * landed); pile.position.y = wy + h / 2;
      flakes.forEach((m, i) => { const ti = F[0] + (F[1] - F[0]) * i / n, u = t - ti; if (u < 0) { m.visible = false; return; } m.visible = true;
        const jx = (hash(i) - 0.5) * 0.05, jz = (hash(i + 7) - 0.5) * 0.05, out = hash(i + 3) < 0.18 && landed > 0.6;
        const tx = out ? Math.sin(i * 2.4) * (wr * 1.4 + 0.06 * hash(i + 9)) : (hash(i + 5) - 0.5) * wr * 1.6, tz = out ? Math.cos(i * 2.4) * (wr * 1.4 + 0.06 * hash(i + 11)) : (hash(i + 13) - 0.5) * wr * 1.6;
        const ty = out ? 0.006 : wy + h * (1 - Math.min(1, Math.hypot(tx, tz) / (wr * 1.3))) + 0.004;
        const k = clamp01(u / 0.28), fall = k * k;
        m.position.set(jx + (tx - jx) * k, pourY + (ty - pourY) * fall, jz + (tz - jz) * k); m.rotation.set(i, u * 9 * (1 - k), i * 1.7); });
    };
    g.userData.update(0); return g;
  },

  // A box of fish food (pivot at its middle, front +Z): red and yellow card, GRAINS and a little fish on the front; hold it by userData.grip
  grainBox(o) {
    const w = o.w ?? 0.13, h = o.h ?? 0.22, d = o.d ?? 0.06;
    const front = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#E43A2C'; c.fillRect(0, 0, W, H); c.fillStyle = '#F7C531'; c.fillRect(0, H * 0.62, W, H * 0.38);
      c.fillStyle = '#FFFFFF'; c.font = `900 ${W * 0.2}px Arial`; c.textAlign = 'center'; c.fillText('GRAINS', W / 2, H * 0.2);
      c.fillStyle = '#F2701E'; c.beginPath(); c.ellipse(W * 0.48, H * 0.4, W * 0.2, H * 0.08, 0, 0, 2 * PI); c.fill(); c.beginPath(); c.moveTo(W * 0.66, H * 0.4); c.lineTo(W * 0.8, H * 0.33); c.lineTo(W * 0.8, H * 0.47); c.fill();
      c.fillStyle = '#111111'; c.beginPath(); c.arc(W * 0.38, H * 0.38, W * 0.025, 0, 2 * PI); c.fill();
      c.fillStyle = '#B5281E'; c.font = `900 ${W * 0.16}px Arial`; c.fillText('XXL', W / 2, H * 0.85); });
    front.position.z = d / 2 + 0.001;
    const g = grp(box(w, h, d, '#E43A2C'), front); g.userData.grip = [w * 0.5, 0, 0]; return g;
  },

  // Three grains of fish food in a small cluster (pivot at their middle; hold them by userData.grip): the whole wage
  grains(o) {
    const g = grp(), s = o.s ?? 1;
    for (let i = 0; i < (o.n ?? 3); i++) g.add(at(ball(0.012 * s, o.color || '#C9772E', 6), (i - 1) * 0.022 * s, 0.004 * s * (i % 2), 0));   // o.color (pass 2: big orange grains read as oranges)
    g.userData.grip = [0, -0.015 * s, 0]; return g;
  },

  // A municipal pool (pivot at the deck level in the middle of the basin, its length along Z): a pale tiled deck, a basin of blue water o.w x o.l,
  // tiled walls, three lane ropes of red and white floats, a chrome ladder, a lifeguard's chair; o.waves (1): how much the water heaves (a giant
  // fish in it: 3)
  pool(o) {
    const W = o.w ?? 6, Lg = o.l ?? 12, D = 1.4, g = grp(), dk = o.deck ?? 3;
    const deckM = L('#EDEFF2');
    g.add(at(box(W + 2 * dk, 0.1, dk, '#EDEFF2'), 0, -0.05, -(Lg / 2 + dk / 2)), at(box(W + 2 * dk, 0.1, dk, '#EDEFF2'), 0, -0.05, Lg / 2 + dk / 2),
      at(box(dk, 0.1, Lg, '#EDEFF2'), -(W / 2 + dk / 2), -0.05, 0), at(box(dk, 0.1, Lg, '#EDEFF2'), W / 2 + dk / 2, -0.05, 0));
    for (const [x, z, w, l] of [[0, -Lg / 2, W, 0.12], [0, Lg / 2, W, 0.12], [-W / 2, 0, 0.12, Lg], [W / 2, 0, 0.12, Lg]]) g.add(at(box(w + 0.12, 0.06, l + 0.12, '#FFFFFF'), x, 0.01, z));
    const tile = '#8CCFE6';
    g.add(at(box(W, D, 0.06, tile), 0, -D / 2, -Lg / 2), at(box(W, D, 0.06, tile), 0, -D / 2, Lg / 2), at(box(0.06, D, Lg, tile), -W / 2, -D / 2, 0), at(box(0.06, D, Lg, tile), W / 2, -D / 2, 0), at(box(W, 0.06, Lg, '#7CC4DD'), 0, -D, 0));
    const wg = new THREE.PlaneGeometry(W - 0.02, Lg - 0.02, 24, 48).rotateX(-PI / 2), wp = wg.attributes.position, base = wp.array.slice();
    const water = new THREE.Mesh(wg, new THREE.MeshLambertMaterial({ color: '#3FB4E0', transparent: true, opacity: 0.82 })); water.position.y = -0.16; g.add(water);
    const ropes = [];
    for (const x of [-W / 4, 0, W / 4]) for (let i = 0; i < Math.floor(Lg / 0.3); i++) { const b = at(cyl(0.05, 0.05, 0.14, i % 4 < 2 ? '#E8392F' : '#FFFFFF', 8), x, -0.13, -Lg / 2 + 0.15 + i * 0.3, PI / 2, 0, 0); g.add(b); ropes.push(b); }
    const ch = L('#C9D1D8');
    for (const sd of [-0.25, 0.25]) { g.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.025, 6, 12, PI), ch), W / 2 - 0.3 + sd, 0.0, Lg / 2 - 0.05, 0, PI / 2, 0)); g.add(at(cyl(0.025, 0.025, 1.1, '#C9D1D8', 6), W / 2 - 0.3 + sd, -0.55, Lg / 2 - 0.27)); }
    for (let i = 0; i < 3; i++) g.add(at(box(0.5, 0.03, 0.08, '#C9D1D8'), W / 2 - 0.3, -0.25 - i * 0.3, Lg / 2 - 0.27));
    const chair = grp(at(box(0.08, 2.0, 0.08, '#FFFFFF', { pivot: 'bottom' }), -0.3, 0, -0.3), at(box(0.08, 2.0, 0.08, '#FFFFFF', { pivot: 'bottom' }), 0.3, 0, -0.3), at(box(0.08, 2.0, 0.08, '#FFFFFF', { pivot: 'bottom' }), -0.3, 0, 0.3), at(box(0.08, 2.0, 0.08, '#FFFFFF', { pivot: 'bottom' }), 0.3, 0, 0.3),
      at(box(0.75, 0.08, 0.75, '#FFFFFF'), 0, 2.0, 0), at(box(0.75, 0.6, 0.06, '#E8392F'), 0, 2.35, -0.36));
    g.add(at(chair, -(W / 2 + 1.1), 0, Lg * 0.15));
    g.userData.update = t => { const k = o.waves ?? 1; for (let i = 0; i < wp.count; i++) { const x = base[i * 3], z = base[i * 3 + 2]; wp.setY(i, 0.03 * k * Math.sin(x * 1.7 + t * 2.2) * Math.cos(z * 1.1 - t * 1.6)); } wp.needsUpdate = true; wg.computeVertexNormals();
      ropes.forEach((b, i) => { b.position.y = -0.13 + 0.03 * k * Math.sin(i * 0.6 + t * 2.4); }); };
    g.userData.update(0); return g;
  },

  // A folding sign on two legs (pivot at the floor, its face +Z): o.text (PISCINE FERMÉE) in red on white, every line fitted inside the border (pass 2:
  // FERMÉE ran past it); o.icon 'noFish': a crossed-out goldfish above the text; pops up at o.at with an overshoot (no o.at: there from the start)
  closedSign(o) {
    const lines = (o.text || 'PISCINE|FERMÉE').split('|'), w = o.w ?? 0.9, h = o.h ?? 0.7, red = '#D52B1E';
    const face = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.strokeStyle = red; c.lineWidth = W * 0.05; c.strokeRect(W * 0.04, H * 0.04, W * 0.92, H * 0.92);
      let y0 = H * 0.1;
      if (o.icon === 'noFish') { const R = Math.min(W * 0.3, H * 0.24), cx = W / 2, cy = H * 0.1 + R;
        c.fillStyle = '#F2701E'; c.beginPath(); c.ellipse(cx - R * 0.1, cy, R * 0.5, R * 0.3, 0, 0, 2 * PI); c.fill();
        c.beginPath(); c.moveTo(cx + R * 0.32, cy); c.lineTo(cx + R * 0.68, cy - R * 0.28); c.lineTo(cx + R * 0.68, cy + R * 0.28); c.closePath(); c.fill();
        c.fillStyle = '#111111'; c.beginPath(); c.arc(cx - R * 0.38, cy - R * 0.06, R * 0.07, 0, 2 * PI); c.fill();
        c.strokeStyle = red; c.lineWidth = R * 0.17; c.beginPath(); c.arc(cx, cy, R * 0.9, 0, 2 * PI); c.stroke();
        c.beginPath(); c.moveTo(cx - R * 0.64, cy - R * 0.64); c.lineTo(cx + R * 0.64, cy + R * 0.64); c.stroke(); y0 = cy + R * 1.08; }
      const band = (H * 0.9 - y0) / lines.length; c.fillStyle = red; c.textAlign = 'center'; c.textBaseline = 'middle';
      lines.forEach((l, i) => { let fs = band * 0.8; c.font = `900 ${fs}px Arial`; const mw = c.measureText(l).width; if (mw > W * 0.8) { fs *= W * 0.8 / mw; c.font = `900 ${fs}px Arial`; } c.fillText(l, W / 2, y0 + band * (i + 0.5)); }); });
    face.position.set(0, h / 2 + 0.25, 0.02);
    const sign = grp(face, at(box(w + 0.04, h + 0.04, 0.03, '#FFFFFF'), 0, h / 2 + 0.25, 0), at(box(0.04, h + 0.3, 0.04, '#9AA3AB', { pivot: 'bottom' }), -w * 0.4, 0, -0.08), at(box(0.04, h + 0.3, 0.04, '#9AA3AB', { pivot: 'bottom' }), w * 0.4, 0, -0.08));
    const g = grp(sign);
    g.userData.update = t => { const u = o.at == null ? 1 : (t - o.at) / 0.2; const k = u <= 0 ? 0 : u < 1 ? eo(u) * (1 + 0.2 * Math.sin(PI * u)) : 1; sign.scale.setScalar(Math.max(0.001, k)); sign.visible = k > 0.01; };
    g.userData.update(0); return g;
  },

  // A swan pedal boat (pivot at the waterline in its middle, front +Z): a white hull with raised wings and tail feathers, one S-shaped neck with the head,
  // an orange beak and its black knob, two blue seats; it bobs on the water; o.goneAt: gone from then (eaten); over the 0.12 s before, it is sucked
  // by o.suck [x, y, z] (its own frame; default up 0.6 m), shrinking and tipping, into the mouth
  pedalo(o) {
    const g = grp(), boat = grp(), W = L('#FFFFFF'), blue = '#3A7BD5';
    boat.add(at(box(1.05, 0.38, 1.8, '#FFFFFF', { outline: 0.01, taper: { x: 0.85, z: 0.9 } }), 0, 0.05, 0), at(box(0.92, 0.06, 1.55, '#E6EEF2'), 0, 0.25, 0),
      at(box(0.8, 0.12, 0.36, blue), 0, 0.33, -0.32), at(box(0.8, 0.34, 0.08, blue), 0, 0.5, -0.48), at(box(0.8, 0.12, 0.36, blue), 0, 0.33, 0.22), at(box(0.8, 0.34, 0.08, blue), 0, 0.5, 0.06));
    for (const sd of [-1, 1]) { const wg = ball(0.5, W, 10); wg.scale.set(0.16, 0.42, 1.0); wg.position.set(sd * 0.56, 0.42, -0.15); wg.rotation.x = -0.25; boat.add(wg); }
    const tl = new THREE.Mesh(new THREE.ConeGeometry(0.22, 0.5, 6), W); tl.position.set(0, 0.52, -0.98); tl.rotation.x = -0.93; tl.scale.set(1, 1, 0.45); boat.add(tl);
    const curve = new THREE.CatmullRomCurve3([[0, 0.25, 0.78], [0, 0.62, 0.98], [0, 0.97, 0.9], [0, 1.24, 0.72], [0, 1.44, 0.8]].map(v => new THREE.Vector3(...v)));
    const neck = new THREE.Mesh(new THREE.TubeGeometry(curve, 24, 0.1, 8, false), W); neck.castShadow = true; boat.add(neck);
    const head = grp(at(ball(0.15, '#FFFFFF', 10), 0, 0, 0)); head.children[0].scale.set(0.9, 0.9, 1.25);
    const beak = new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.22, 6), L('#F28C28')); beak.rotation.x = PI / 2; beak.position.set(0, -0.03, 0.24); head.add(beak);
    head.add(at(ball(0.045, '#111111', 6), 0, 0.01, 0.14));
    for (const sd of [-1, 1]) head.add(at(ball(0.027, '#111111', 6), sd * 0.1, 0.05, 0.08));
    head.position.set(0, 1.46, 0.84); boat.add(head);
    g.add(boat); const ph = hash(o.seed ?? 1) * 6, sk = o.suck ?? [0, 0.6, 0];
    g.userData.update = t => { boat.visible = o.goneAt == null || t < o.goneAt; const k = o.goneAt == null ? 0 : eo((t - o.goneAt + 0.12) / 0.12);
      boat.position.set(sk[0] * k, 0.04 * Math.sin(t * 2 + ph) + sk[1] * k, sk[2] * k); boat.scale.setScalar(1 - 0.65 * k);
      boat.rotation.z = 0.05 * Math.sin(t * 1.6 + ph) + 0.6 * k; boat.rotation.x = 0.03 * Math.sin(t * 1.3 + ph) - 0.5 * k; };
    g.userData.update(0); return g;
  },

  // A big glass tank for the dock of a courtroom (pivot at the floor, front +Z): a dark plinth, glass walls o.w x o.h x o.d, blue water to
  // 90 % of the height, a metal rim
  glassTank(o) {
    const W = o.w ?? 2.4, H = o.h ?? 1.8, D = o.d ?? 1.6, g = grp(), pl = 0.25;
    g.add(at(box(W + 0.1, pl, D + 0.1, '#2B2F36'), 0, pl / 2, 0));
    const water = new THREE.Mesh(new THREE.BoxGeometry(W - 0.04, H * 0.9, D - 0.04), glass('#5CB8E0', 0.32)); water.position.y = pl + H * 0.45; g.add(water);
    const gl = new THREE.Mesh(new THREE.BoxGeometry(W, H, D), glass('#DDF2FF', 0.16)); gl.position.y = pl + H / 2; g.add(gl);
    const rim = '#3A3F47';
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(at(box(0.05, H, 0.05, rim), sx * W / 2, pl + H / 2, sz * D / 2));
    for (const sz of [-1, 1]) { g.add(at(box(W, 0.05, 0.05, rim), 0, pl + H, sz * D / 2)); g.add(at(box(W, 0.05, 0.05, rim), 0, pl, sz * D / 2)); }
    for (const sx of [-1, 1]) { g.add(at(box(0.05, 0.05, D, rim), sx * W / 2, pl + H, 0)); g.add(at(box(0.05, 0.05, D, rim), sx * W / 2, pl, 0)); }
    return g;
  },

  // (pass 2) A claw-foot bathtub (pivot on the floor in its middle, its length along X): a rounded white basin o.w x o.d x o.h on four gold claw feet, a
  // rolled rim, chrome taps at the +X end, blue water to o.fill of its height that rocks a little; big enough for the goldfish of scale 3.4
  clawTub(o) {
    const W = o.w ?? 2.0, D = o.d ?? 1.0, H = o.h ?? 0.62, y0 = o.feet ?? 0.16, t = 0.06, rr = D * 0.45, g = grp(), white = L('#FAFAF7');
    const rrect = (w, d, r) => { const s = new THREE.Shape(), x0 = -w / 2, z0 = -d / 2; s.moveTo(x0 + r, z0); s.lineTo(x0 + w - r, z0); s.quadraticCurveTo(x0 + w, z0, x0 + w, z0 + r);
      s.lineTo(x0 + w, z0 + d - r); s.quadraticCurveTo(x0 + w, z0 + d, x0 + w - r, z0 + d); s.lineTo(x0 + r, z0 + d); s.quadraticCurveTo(x0, z0 + d, x0, z0 + d - r);
      s.lineTo(x0, z0 + r); s.quadraticCurveTo(x0, z0, x0 + r, z0); return s; };
    const ring = (w, d, r, th, hgt, m, y) => { const s = rrect(w, d, r); s.holes.push(rrect(w - 2 * th, d - 2 * th, Math.max(0.01, r - th))); const ms = new THREE.Mesh(new THREE.ExtrudeGeometry(s, { depth: hgt, bevelEnabled: false, curveSegments: 10 }), m);
      ms.rotation.x = -PI / 2; ms.position.y = y; ms.castShadow = ms.receiveShadow = true; return ms; };
    g.add(ring(W, D, rr, t, H, white, y0), ring(W + 0.07, D + 0.07, rr + 0.035, t + 0.07, 0.06, L('#FFFFFF'), y0 + H - 0.03));
    const floor = new THREE.Mesh(new THREE.ShapeGeometry(rrect(W - 2 * t, D - 2 * t, rr - t), 10), white); floor.rotation.x = -PI / 2; floor.position.y = y0 + 0.02; g.add(floor);
    const water = new THREE.Mesh(new THREE.ShapeGeometry(rrect(W - 2 * t - 0.01, D - 2 * t - 0.01, rr - t), 10), new THREE.MeshLambertMaterial({ color: '#7CCBEB', transparent: true, opacity: 0.9 }));
    water.rotation.x = -PI / 2; const wy = y0 + H * (o.fill ?? 0.82); water.position.y = wy; g.add(water);
    const gold = L('#D8A93A');
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) { const f = grp(at(box(0.09, y0 + 0.04, 0.09, '#D8A93A', { pivot: 'bottom', taper: 1.5 }), 0, 0, 0));
      const pawB = ball(0.07, gold, 8); pawB.scale.set(1.2, 0.6, 1.2); pawB.position.y = 0.03; f.add(pawB); g.add(at(f, sx * (W / 2 - rr * 0.55), 0, sz * (D / 2 - 0.16))); }
    const chrome = '#C9D1D8', tx = W / 2 - 0.12;
    g.add(at(cyl(0.03, 0.03, 0.34, chrome, 8, { pivot: 'bottom' }), tx, y0 + H, 0), at(cyl(0.025, 0.025, 0.24, chrome, 8), tx - 0.11, y0 + H + 0.32, 0, 0, 0, PI / 2));
    for (const sd of [-1, 1]) { g.add(at(cyl(0.022, 0.022, 0.12, chrome, 6, { pivot: 'bottom' }), tx, y0 + H, sd * 0.16), at(box(0.12, 0.025, 0.025, chrome), tx, y0 + H + 0.13, sd * 0.16));
      g.add(at(ball(0.025, sd < 0 ? '#3A7BD5' : '#D83A2E', 6), tx, y0 + H + 0.15, sd * 0.16)); }
    g.userData.update = tt => { water.position.y = wy + 0.012 * Math.sin(tt * 4.2); water.rotation.z = 0.012 * Math.sin(tt * 3.1); };
    g.userData.update(0); g.userData.lie = [0, y0 + 0.2, 0]; return g;
  },

  // (pass 2) A sea captain's cap (pivot at the bottom of the band, front +Z): a white crown wider at the top, a black band with a gold cord, a shiny
  // black peak tipped down, a gold anchor badge (the cap on the fish in S18 read as a navy band over its eyes)
  captainCap(o) {
    const r = o.r ?? 0.12, g = grp(), bh = r * 0.42;
    g.add(at(new THREE.Mesh(new THREE.CylinderGeometry(r * 1.0, r * 0.98, bh, 18), L('#16181D')), 0, bh / 2, 0));
    g.add(at(new THREE.Mesh(new THREE.CylinderGeometry(r * 1.25, r * 1.0, r * 0.5, 18), L('#FAFAF6')), 0, bh + r * 0.25, 0));
    g.add(at(new THREE.Mesh(new THREE.CylinderGeometry(r * 1.22, r * 1.25, r * 0.06, 18), L('#FFFFFF')), 0, bh + r * 0.53, 0));
    g.add(at(box(r * 1.3, r * 0.05, r * 0.05, '#E8B730'), 0, bh * 0.7, r * 0.98));
    const peak = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.95, r * 0.95, r * 0.05, 18, 1, false, -PI / 2, PI), new THREE.MeshPhongMaterial({ color: '#0E0F12', shininess: 80 }));
    peak.scale.z = 0.85; peak.position.set(0, r * 0.02, r * 0.35); peak.rotation.x = 0.3; g.add(peak);
    const badge = canvasPlane(r * 0.7, r * 0.5, (c, Wc, Hc) => { c.clearRect(0, 0, Wc, Hc); c.strokeStyle = '#F2C230'; c.fillStyle = '#F2C230'; c.lineWidth = Wc * 0.07; c.lineCap = 'round';
      const cx = Wc / 2; c.beginPath(); c.moveTo(cx, Hc * 0.16); c.lineTo(cx, Hc * 0.84); c.stroke(); c.beginPath(); c.moveTo(cx - Wc * 0.16, Hc * 0.3); c.lineTo(cx + Wc * 0.16, Hc * 0.3); c.stroke();
      c.beginPath(); c.arc(cx, Hc * 0.5, Hc * 0.34, PI * 0.15, PI * 0.85); c.stroke(); c.beginPath(); c.arc(cx, Hc * 0.12, Hc * 0.07, 0, 2 * PI); c.stroke();
      for (const sd of [-1, 1]) { c.beginPath(); c.ellipse(cx + sd * Wc * 0.36, Hc * 0.55, Wc * 0.07, Hc * 0.28, sd * 0.4, 0, 2 * PI); c.fill(); } }, { res: 256, transparent: true });
    badge.position.set(0, bh + r * 0.22, r * 1.13); badge.rotation.x = -0.45; g.add(badge);
    return g;
  },

  // (pass 2) A lighthouse on its rock (pivot at the foot of the rock, o.h tall): a white tower with two red bands, a dark gallery, the lantern room, a
  // red roof: something of known size beside the fish at sea
  lighthouse(o) {
    const Hh = o.h ?? 12, g = grp(), r0 = Hh * 0.085, r1 = Hh * 0.06, th = Hh * 0.66, rk = Hh * 0.12;
    const rock = new THREE.Mesh(new THREE.DodecahedronGeometry(rk * 1.6, 0), L('#7D7F86')); rock.scale.y = 0.5; rock.position.y = rk * 0.3; rock.castShadow = rock.receiveShadow = true; g.add(rock);
    const tw = new THREE.Mesh(new THREE.CylinderGeometry(r1, r0, th, 16), L('#F7F5EF')); tw.position.y = rk * 0.8 + th / 2; tw.castShadow = true; g.add(tw);
    for (const f of [0.3, 0.68]) { const rf = r0 + (r1 - r0) * f, bd = new THREE.Mesh(new THREE.CylinderGeometry(rf * 1.02 - (r0 - r1) * 0.06, rf * 1.02, th * 0.11, 16), L('#D8342A')); bd.position.y = rk * 0.8 + th * f; g.add(bd); }
    const gy = rk * 0.8 + th;
    g.add(at(new THREE.Mesh(new THREE.CylinderGeometry(r1 * 1.5, r1 * 1.5, Hh * 0.025, 16), L('#2B2F36')), 0, gy, 0));
    const lan = new THREE.Mesh(new THREE.CylinderGeometry(r1 * 0.9, r1 * 0.9, Hh * 0.09, 12), new THREE.MeshLambertMaterial({ color: '#FFE9A0', emissive: '#8A6A10' })); lan.position.y = gy + Hh * 0.055; g.add(lan);
    g.add(at(new THREE.Mesh(new THREE.ConeGeometry(r1 * 1.15, Hh * 0.09, 12), L('#C8322A')), 0, gy + Hh * 0.145, 0));
    for (const f of [0.45, 0.85]) g.add(at(box(r0 * 0.3, Hh * 0.04, 0.05, '#2B2F36'), 0, rk * 0.8 + th * f, (r0 + (r1 - r0) * f) * 0.98));
    return g;
  },
};
