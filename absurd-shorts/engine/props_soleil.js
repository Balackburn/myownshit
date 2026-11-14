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
    // (review 1 of 62) o.wholeR: the whole egg's size against the white (0.42; at 0.42 of a 0.085 white it was a crumb nobody saw in her hand); o.shells
    // (true): at o.at two half shells spring apart from the crack and drop
    // (review 2 of 62) o.shellSpread (1): how far the shells fly (at 1 they stayed under the burst; 2.5 throws them clear of the head)
    const whole = new THREE.Mesh(new THREE.SphereGeometry(R * (o.wholeR ?? 0.42), 12, 10), new THREE.MeshLambertMaterial({ color: '#F2E6D0' })); whole.scale.y = 1.3; whole.position.y = R * (o.wholeR ?? 0.42) * 1.2; if (o.whole !== false) g.add(whole);
    const shells = []; if (o.shells !== false) for (const sd of [-1, 1]) { const sg = new THREE.SphereGeometry(R * (o.wholeR ?? 0.42), 12, 6, 0, TAU, 0, PI / 2), sm = new THREE.MeshLambertMaterial({ color: '#F2E6D0', side: THREE.DoubleSide });
      const sh = new THREE.Mesh(sg, sm); sh.scale.y = 1.3; sh.visible = false; g.add(sh); shells.push({ sh, sd }); }
    const puffs = []; for (let i = 0; i < 4; i++) { const p = new THREE.Mesh(new THREE.SphereGeometry(R * 0.28, 8, 6), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0, depthWrite: false })); g.add(p); puffs.push(p); }
    g.userData.update = t => {
      const u = t - (o.at ?? 0), k = u < 0 ? 0 : eo(u / 0.25);
      whole.visible = u < 0.02; white.visible = yolk.visible = u >= 0;
      shells.forEach(({ sh, sd }) => { const v = u / 0.45; sh.visible = u >= 0 && v < 1; if (!sh.visible) return; const wr = R * (o.wholeR ?? 0.42);
        const sp = o.shellSpread ?? 1; sh.position.set(sd * (0.6 * wr + 2.2 * R * v * sp), wr * 1.2 + 3.0 * R * v * sp - 9.0 * R * v * v * sp, R * 0.2 * v * sp); sh.rotation.set(0, 0, sd * (PI / 2 + 2.5 * v)); }); blobs.forEach((b, i) => { b.visible = u >= 0; b.scale.set(1 + 0.25 * Math.sin(t * 22 + i * 1.7), 0.25, 1 + 0.25 * Math.sin(t * 22 + i * 1.7)); });
      white.scale.set(Math.max(0.05, k), 1, Math.max(0.05, k)); blobs.forEach(b => b.position.set(b.userData.p0[0] * k, 0.008, b.userData.p0[1] * k)); yolk.scale.set(Math.max(0.2, k), 0.6 * Math.max(0.3, k), Math.max(0.2, k));
      puffs.forEach((p, i) => { const v = (u - 0.2 - i * 0.18) % 0.72, on = u > 0.2 + i * 0.18 && u < (o.dur ?? 1.5) + 0.2; p.visible = on; if (!on) return;
        const w = clamp01(v / 0.72); p.position.set(Math.sin(i * 2.1) * R * 0.5, 0.05 + w * R * 3.2, Math.cos(i * 2.1) * R * 0.4); p.scale.setScalar(0.6 + w * 1.2); p.material.opacity = 0.75 * (1 - w); });
    };
    g.userData.update(0); return g;
  },

  // Moths (pivot at the light they circle): o.n (6) little moths fluttering round it in wobbling loops of radius o.r (0.35), wings beating.
  // (review 1 of 62) grey-brown triangular wings swept back, a furry body and two antennae, lit (they take his red glow on the side toward him): the
  // cream rectangles read as envelopes or banknotes; o.size (1)
  moths(o) {
    const n = o.n ?? 6, R = o.r ?? 0.35, g = grp(), ms = [], z = o.size ?? 1;
    const tri = new THREE.Shape(); tri.moveTo(0, 0); tri.lineTo(0.055 * z, -0.012 * z); tri.lineTo(0.046 * z, -0.042 * z); tri.lineTo(0, -0.024 * z); tri.lineTo(0, 0);
    const wgeo = new THREE.ShapeGeometry(tri); wgeo.rotateX(-PI / 2);
    const cols = list(o.color ?? ['#8A7A66', '#9C8C76']);   // (review 2 of 62) o.color (one or two), o.basic: unlit wings that keep their grey-brown under his red glow (lit, they read as red birds)
    for (let i = 0; i < n; i++) { const m = grp(), wm = o.basic ? new THREE.MeshBasicMaterial({ color: cols[i % cols.length], side: THREE.DoubleSide }) : new THREE.MeshLambertMaterial({ color: cols[i % cols.length], side: THREE.DoubleSide });
      const wl = new THREE.Group(), wr = new THREE.Group(); const ml = new THREE.Mesh(wgeo, wm), mr = new THREE.Mesh(wgeo, wm); mr.scale.x = -1; wl.add(ml); wr.add(mr);
      const body = new THREE.Mesh(new THREE.CylinderGeometry(0.007 * z, 0.005 * z, 0.04 * z, 6), mat('#5E5244')); body.rotation.x = PI / 2;
      m.add(wl, wr, body); for (const sd of [-1, 1]) { const an = new THREE.Mesh(new THREE.CylinderGeometry(0.0015 * z, 0.0015 * z, 0.03 * z, 4), mat('#4A4036')); an.position.set(sd * 0.006 * z, 0.004 * z, 0.026 * z); an.rotation.set(PI / 2 - 0.5, 0, sd * 0.5); m.add(an); }
      g.add(m); ms.push({ m, wl, wr, ph: i * 1.7, rr: R * (0.7 + 0.5 * ((i * 37) % 10) / 10), sp: 4.5 + (i % 3) }); }
    g.userData.update = t => ms.forEach(q => { const a = t * q.sp + q.ph; q.m.position.set(Math.cos(a) * q.rr, Math.sin(a * 1.7) * q.rr * 0.5, Math.sin(a) * q.rr); q.m.rotation.y = -a; const f = Math.sin(t * 40 + q.ph) * 0.9; q.wl.rotation.z = f; q.wr.rotation.z = -f; });
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
    // (stills 2 of 62) a dark back inside the box: open at the back, the sky showed through the hole round his face
    g.add(at(box(W - 0.08, H - 0.08, 0.02, '#121815', { noGrain: true }), 0, P + H / 2, -D / 2 + 0.012));
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
    const ws = o.front === false ? at(box(0.04, 0.85, 2.0, '#BFE3F0'), 3.56, 1.6, 0) : at(new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.85, 2.0), new THREE.MeshLambertMaterial({ color: '#CFEAF5', transparent: true, opacity: 0.28, depthWrite: false })), 3.56, 1.6, 0);   // (review 2 of 62) a see-through windscreen: the driver showed as a blank panel
    g.add(at(box(1.9, 1.75, 2.3, C, { pivot: 'bottom', outline: 0.012 }), 2.6, 0.55, 0), ws, at(box(0.06, 0.55, 1.9, '#C9CED4'), 3.57, 0.85, 0),
      at(box(4.6, 2.7, 2.4, BX, { pivot: 'bottom', outline: 0.014 }), -0.75, 0.6, 0), at(box(6.9, 0.22, 2.2, '#3C3F44'), 0.4, 0.45, 0));
    for (const x of [-2.4, -1.4, 2.9]) for (const z of [-1.08, 1.08]) { const w = cyl(0.48, 0.48, 0.32, '#22252A', 14); w.rotation.x = PI / 2; w.position.set(x, 0.48, z); g.add(w); }
    // (review 1 of 62) seen from the side it read as a blue wall: o.front (true): a cab face that reads from three-quarter front, a dark grille with
    // chrome bars, a black bumper, round headlights, mirrors on arms, a driver behind the windscreen, and two big chrome trumpet horns on the roof
    // pointing forward (o.hornLen 1.0 m); without it the old small horns
    if (o.front === false) { for (const z of [-0.6, 0.6]) { const h = cyl(0.07, 0.12, 0.55, '#D8DCE0', 10); h.rotation.z = -PI / 2; h.position.set(3.0, 2.42, z); g.add(h); }
      for (const z of [-0.85, 0.85]) g.add(at(box(0.04, 0.16, 0.3, '#FFF3C2', { emissive: '#FFE38A', noGrain: true }), 3.58, 0.75, z)); return g; }
    g.add(at(box(0.08, 0.62, 1.5, '#23262B', { outline: 0.006 }), 3.58, 0.86, 0));
    for (let i = 0; i < 5; i++) g.add(at(box(0.03, 0.04, 1.42, '#D8DCE0'), 3.63, 0.62 + i * 0.12, 0));
    g.add(at(box(0.18, 0.26, 2.36, '#1C1E22', { outline: 0.008 }), 3.6, 0.42, 0));
    for (const z of [-0.9, 0.9]) { const hl = cyl(0.13, 0.13, 0.05, '#FFF3C2', 14); hl.rotation.z = PI / 2; hl.position.set(3.62, 0.86, z); hl.material = new THREE.MeshBasicMaterial({ color: '#FFF3C2', toneMapped: false }); g.add(hl);
      g.add(at(box(0.05, 0.05, 0.42, '#2A2C31'), 3.4, 2.0, z * 1.28), at(box(0.06, 0.34, 0.2, '#2A2C31', { outline: 0.004 }), 3.4, 1.86, z * 1.48)); }
    // (review 2 of 62) the driver leans on the horn: o.honkAt (s), o.honkDur (0.6): his body tips forward, his raised arm pulls a cord down from the cab roof;
    // the chrome trumpets (a banded chrome texture, unlit so the white streak stays hot against the sky) flare, recoil and shiver, and sound rings fly
    // out of their bells for as long as the horn lasts
    const drv = grp(at(box(0.3, 0.42, 0.3, '#3A3F4A'), 0, 0.21, 0), at(box(0.26, 0.24, 0.24, '#E0B48C'), 0.02, 0.57, 0)); drv.position.set(3.25, 1.41, -0.45); g.add(drv);
    const arm = grp(at(box(0.08, 0.36, 0.08, '#3A3F4A'), 0, 0.18, 0), at(box(0.08, 0.08, 0.08, '#E0B48C'), 0, 0.38, 0)); arm.position.set(0.0, 0.36, 0.12); drv.add(arm);
    const cord = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.4, 4), mat('#1C1C1C')); cord.position.set(3.25, 2.1, -0.33); g.add(cord);
    const cv = document.createElement('canvas'); cv.width = 64; cv.height = 8; const cx = cv.getContext('2d'), gr = cx.createLinearGradient(0, 0, 64, 0);
    [[0, '#5A6068'], [0.18, '#E8EEF4'], [0.27, '#FFFFFF'], [0.36, '#AEB8C4'], [0.55, '#4A5058'], [0.72, '#C8D2DC'], [0.86, '#FFFFFF'], [1, '#6A7078']].forEach(([a, c_]) => gr.addColorStop(a, c_)); cx.fillStyle = gr; cx.fillRect(0, 0, 64, 8);
    const chrome = new THREE.CanvasTexture(cv); chrome.colorSpace = THREE.SRGBColorSpace;
    const HL = o.hornLen ?? 1.0, horns = [], rings = [];
    for (const z of [-0.55, 0.55]) { const tr = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.05, HL, 18, 1, true), new THREE.MeshBasicMaterial({ map: chrome, side: THREE.DoubleSide }));
      tr.rotation.z = -PI / 2; tr.position.set(3.0 + HL / 2 - 0.25, 2.55, z); g.add(tr); horns.push(tr); g.add(at(box(0.5, 0.08, 0.08, '#B8BEC4'), 2.9, 2.36, z));
      for (let i = 0; i < 4; i++) { const rg = new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.012, 6, 24), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0, depthWrite: false })); rg.rotation.y = PI / 2; rg.position.set(3.0 + HL - 0.2, 2.55, z); rg.visible = false; g.add(rg); rings.push({ rg, i, x0: 3.0 + HL - 0.2 }); } }
    g.userData.update = t => { const u = o.honkAt == null ? -1 : t - o.honkAt, D = o.honkDur ?? 0.6, on = u >= 0 && u < D;
      const fl = on ? (u < 0.08 ? eo(u / 0.08) : 1) * (1 + 0.04 * Math.sin(u * 90)) : (u >= D && u < D + 0.15 ? 1 - (u - D) / 0.15 : 0);
      horns.forEach(h => { h.scale.set(1 + 0.45 * fl, 1 - 0.12 * fl, 1 + 0.45 * fl); h.position.x = 3.0 + HL / 2 - 0.25 - 0.08 * fl; });
      rings.forEach(({ rg, i, x0 }) => { const v = on ? ((u - i * 0.1) % 0.4) / 0.4 : -1; rg.visible = on && u >= i * 0.1 && v >= 0; if (!rg.visible) return; rg.position.x = x0 + 1.6 * v; rg.scale.setScalar(1 + 2.6 * v); rg.material.opacity = 0.85 * (1 - v); });
      const lean = on ? (u < 0.1 ? eo(u / 0.1) : 1) : (u >= D && u < D + 0.2 ? 1 - (u - D) / 0.2 : 0); drv.rotation.z = -0.35 * lean; arm.rotation.z = 0.5 * lean; cord.scale.y = 1 + 0.5 * lean; cord.position.y = 2.1 - 0.1 * lean; };
    g.userData.update(0); return g;
  },

  // (review 2 of 62) An open newspaper held up (pivot at its centre, its print toward +Z): two pages o.w (0.56) x o.h (0.4), a masthead, headlines and
  // columns, unlit and tinted o.tint (a pale pink: it reads by his light; lit by the night it was a black slab)
  glowPaper(o) {
    const W = o.w ?? 0.56, H = o.h ?? 0.4, cv = document.createElement('canvas'); cv.width = 512; cv.height = Math.round(512 * H / W); const c = cv.getContext('2d'), CW = cv.width, CH = cv.height;
    c.fillStyle = '#F4F0E6'; c.fillRect(0, 0, CW, CH); c.fillStyle = '#2A2A2A'; c.textAlign = 'center'; c.font = `900 ${CH * 0.13}px Georgia, serif`; c.fillText(o.title || 'LE SOIR', CW * 0.25, CH * 0.16);
    c.fillRect(CW * 0.03, CH * 0.2, CW * 0.44, 3); c.fillRect(CW * 0.53, CH * 0.2, CW * 0.44, 3); c.font = `bold ${CH * 0.07}px Arial`; c.fillText(o.headline || 'NUIT ROUGE', CW * 0.75, CH * 0.15);
    c.fillStyle = '#8E8E8E'; c.fillRect(CW * 0.55, CH * 0.26, CW * 0.4, CH * 0.24); c.fillStyle = '#4A4A4A';
    for (const x0 of [0.03, 0.18, 0.33, 0.55, 0.7, 0.85]) for (let i = 0; i < 14; i++) { const y = 0.27 + i * 0.05; if (x0 >= 0.55 && y < 0.52) continue; c.fillRect(CW * x0, CH * y, CW * 0.12 * (i % 5 === 4 ? 0.6 : 1), 3); }
    c.fillStyle = '#C8C2B4'; c.fillRect(CW / 2 - 1, 0, 2, CH);
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
    const m = new THREE.Mesh(new THREE.PlaneGeometry(W, H), new THREE.MeshBasicMaterial({ map: tex, color: o.tint || '#FFC9D2', side: THREE.DoubleSide })); m.castShadow = false;
    return grp(m);
  },

  // A glow (pivot at its centre): a coloured point light of o.k (6) over o.dist (7 m) from o.at, so a glowing face lights the walls round it
  glowLight(o) {
    const g = grp(), l = new THREE.PointLight(o.color || '#FF3A22', 0, o.dist ?? 7, 1.4); g.add(l);
    g.userData.update = t => { l.intensity = (o.k ?? 6) * clamp01((t - (o.at ?? 0)) / 0.2) * (1 + 0.04 * Math.sin(t * 9)); };
    g.userData.update(0); return g;
  },

  // (review 1 of 62) A glow halo (pivot at its centre; turn it to the camera): a soft disc of light o.r (0.5 m) fading out from a hot core, added to the
  // picture, set just behind a glowing head so its outline burns (at night the glowing head was no brighter than the pavement); o.color, o.core, o.k
  // (1) its strength, from o.at
  halo(o) {
    const cv = document.createElement('canvas'); cv.width = cv.height = 128; const c = cv.getContext('2d'), gr = c.createRadialGradient(64, 64, 0, 64, 64, 64);
    gr.addColorStop(0, o.core || '#FFE2DA'); gr.addColorStop(0.3, o.color || '#FF4A3A'); gr.addColorStop(1, 'rgba(255, 40, 30, 0)'); c.fillStyle = gr; c.fillRect(0, 0, 128, 128);
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
    const m = new THREE.Mesh(new THREE.PlaneGeometry(2 * (o.r ?? 0.5), 2 * (o.r ?? 0.5)), new THREE.MeshBasicMaterial({ map: tex, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false, opacity: 0 }));
    m.castShadow = false; const g = grp(m);
    g.userData.update = t => { m.material.opacity = (o.k ?? 1) * clamp01((t - (o.at ?? 0)) / 0.2) * (1 + 0.05 * Math.sin(t * 7)); }; g.userData.update(0); return g;
  },

  // (review 1 of 62) Skid marks (pivot on the road where the wheels stop, the car's nose toward +Z): two dark streaks o.len (2.2 m) long behind the front
  // wheels, o.track (1.6 m) apart, drawn out from o.at over 0.25 s
  skidMarks(o) {
    const L = o.len ?? 2.2, g = grp(), ms = [];
    for (const sd of [-1, 1]) { const m = new THREE.Mesh(new THREE.PlaneGeometry(0.22, 1), new THREE.MeshBasicMaterial({ color: '#202124', transparent: true, opacity: 0.8, depthWrite: false })); m.rotation.x = -PI / 2; m.position.set(sd * (o.track ?? 1.6) / 2, 0.015, 0); g.add(m); ms.push(m); }
    g.userData.update = t => { const k = clamp01((t - (o.at ?? 0)) / 0.25); ms.forEach(m => { m.visible = k > 0.01; m.scale.y = Math.max(0.01, L * k); m.position.z = -L * k / 2; }); }; g.userData.update(0); return g;
  },
};
