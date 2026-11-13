// Props for "Vos papiers" in the tornado-replica style: a cloud character with a face, rain, the Earth with its
// atmosphere, a France/Belgium map, a border barrier, the Eiffel tower, a prison front and a few text boards.
// Same conventions as props.js: origin at the base, front +Z, metres, userData.update(t) is a pure function of the
// scene time. Small movements are built in (blinks, bobbing, wobble, spin, rain loops) so a held shot never freezes.
import * as THREE from 'three';
import { imageTexture, TEXTURES } from './models.js';
import { PALETTE as P, mat, box, cyl, sphere, rng, ease, clamp01 } from './style.js';
import { grp, at, mesh, canvasPlane, label } from './props.js';

const PI = Math.PI, TAU = PI * 2;
const keyed = (list, t, def) => { let v = def; for (const [a, x] of (list || [])) { if (t >= a) v = x; else break; } return v; };
const lerp = (a, b, u) => a + (b - a) * u;

// a board with centred bold text (canvas), front +Z, centred on its origin
function textBoard(text, w, h, { bg = '#F4F1E8', fg = '#1E2A33', frame = null, font = 'Arial', weight = 900, size = 0.72 } = {}) {
  const lines = String(text).split('\n');
  const c = canvasPlane(w, h, (g, W, H) => {
    g.fillStyle = bg; g.fillRect(0, 0, W, H);
    if (frame) { g.strokeStyle = frame; g.lineWidth = H * 0.06; g.strokeRect(H * 0.04, H * 0.04, W - H * 0.08, H - H * 0.08); }
    g.fillStyle = fg; g.textAlign = 'center'; g.textBaseline = 'middle';
    const maxLen = Math.max(...lines.map(l => l.length));
    let px = Math.min(H * size / lines.length, W * 0.9 / (maxLen * 0.62));
    g.font = `${weight} ${px}px ${font}`;
    const wide = Math.max(...lines.map(l => g.measureText(l).width)), room = (W - (frame ? 2 * H * 0.1 : 0)) * 0.92;   // measured fit: bold capitals are wider than the estimate (inside the frame stroke)
    if (wide > room) { px *= room / wide; g.font = `${weight} ${px}px ${font}`; }
    lines.forEach((l, i) => g.fillText(l, W / 2, H / 2 + (i - (lines.length - 1) / 2) * px * 1.12));
  }, { res: 512 });
  return c;
}

// (cycle 14) the Eiffel tower as one connected low-poly silhouette, o.h tall: four legs that curve in from splayed feet to the first deck, an arch
// between each pair of feet, the first and second decks, the four upper legs converging to the top deck, the spire; every part touches the next
function eiffelV2(o) {
  const H = o.h || 30, c = o.color || '#7A5C44', dk = o.deck || '#5E4532', g = grp();
  const seg = (a, b, w0, w1, col = c) => {   // a tapered beam from point a to point b (widths w0 at a, w1 at b)
    const A = new THREE.Vector3(...a), B = new THREE.Vector3(...b), L = A.distanceTo(B);
    const m = box(w0, L, w0, col, { taper: { x: w1 / w0, z: w1 / w0 }, outline: 0.004 * H });
    m.position.copy(A.clone().add(B).multiplyScalar(0.5)); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), B.clone().sub(A).normalize()); g.add(m);
  };
  const F = 0.21 * H, D1 = 0.115 * H, D2 = 0.062 * H, T = 0.022 * H, y1 = 0.2 * H, y2 = 0.4 * H, yT = 0.86 * H;
  for (const [sx, sz] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) {
    // the leg: three beams on a curve bowed outward, from the foot to the first deck
    const pts = [0, 0.33, 0.66, 1].map(u => { const r = F + (D1 - F) * (1 - Math.pow(1 - u, 1.7)); return [sx * r, y1 * u, sz * r]; });
    for (let i = 0; i < 3; i++) seg(pts[i], pts[i + 1], 0.07 * H * (1 - 0.18 * i), 0.07 * H * (1 - 0.18 * (i + 1)));
    seg([sx * D1, y1, sz * D1], [sx * D2, y2, sz * D2], 0.045 * H, 0.032 * H);   // first deck to the second
    seg([sx * D2, y2, sz * D2], [sx * T, yT, sz * T], 0.03 * H, 0.016 * H);      // the long upper legs to the top
  }
  // the arches between the feet, on the four sides (half tori standing in the plane of each side)
  for (let k = 0; k < 4; k++) { const ar = new THREE.Mesh(new THREE.TorusGeometry(0.105 * H, 0.016 * H, 5, 12, Math.PI), mat(c)); ar.castShadow = true;
    const ang = k * Math.PI / 2; ar.position.set(Math.sin(ang) * 0.165 * H, 0.06 * H, Math.cos(ang) * 0.165 * H); ar.rotation.y = ang; g.add(ar); }
  // decks (a dark band under each reads as the platform's shadow), the core of the upper tower, the top, the spire
  g.add(at(box(2.2 * D1, 0.028 * H, 2.2 * D1, dk, { outline: 0.004 * H }), 0, y1, 0), at(box(2.5 * D1, 0.012 * H, 2.5 * D1, c), 0, y1 + 0.02 * H, 0));
  g.add(at(box(2.3 * D2, 0.022 * H, 2.3 * D2, dk, { outline: 0.004 * H }), 0, y2, 0), at(box(2.6 * D2, 0.01 * H, 2.6 * D2, c), 0, y2 + 0.015 * H, 0));
  g.add(at(box(0.075 * H, yT - y2, 0.075 * H, c, { pivot: 'bottom', taper: { x: 0.35, z: 0.35 } }), 0, y2, 0));
  g.add(at(box(0.06 * H, 0.035 * H, 0.06 * H, dk, { outline: 0.004 * H }), 0, yT, 0), at(cyl(0.006 * H, 0.012 * H, H - yT - 0.03 * H, c, 6, { pivot: 'bottom' }), 0, yT + 0.03 * H, 0));
  return g;
}

export const VP_PROPS = {
  cloudChar(o) { // faceted grey (or white) cloud with a face: blinks, bobs and wobbles; o.expr [[t, name]]; o.rain [[t, true|false]]
    const r = rng(o.seed || 31), g = grp(), body = grp(); g.add(body);
    const c1 = o.color || '#9EA8B2', c2 = o.color2 || '#B3BCC5', S = o.size || 1;
    const geo = new THREE.IcosahedronGeometry(1, 1);
    [[0, 0.62, 0, 0.78], [-0.66, 0.46, 0.04, 0.58], [0.66, 0.44, 0.02, 0.6], [-0.28, 0.98, -0.06, 0.52], [0.32, 1.0, -0.1, 0.54],
     [-1.12, 0.32, 0, 0.38], [1.12, 0.3, 0, 0.4], [0, 0.36, 0.28, 0.54], [-0.5, 0.2, 0.3, 0.36], [0.55, 0.2, 0.3, 0.36]]
      .forEach(([x, y, z, s], i) => { const m = mesh(geo, mat(i % 3 === 1 ? c2 : c1)); m.scale.set(s, s * 0.82, s * 0.86); m.position.set(x, y, z); m.rotation.set(r() * 3, r() * 3, r() * 3); body.add(m); });
    // face (on the front puffs): eyes with pupils, brows, mouth; all small flat boxes so they read like the replica's faces
    const face = grp(); face.position.set(0, 0.62, 0.86); body.add(face);
    const eyeW = mat('#FBFBF8'), ink = mat('#1C252A'), mouthM = mat('#3A2A2A');
    const eyes = [-1, 1].map(s => { const e = grp(at(mesh(new THREE.BoxGeometry(0.2, 0.24, 0.04), eyeW), 0, 0, 0), at(mesh(new THREE.BoxGeometry(0.09, 0.11, 0.05), ink), 0.02 * s, -0.02, 0.012)); e.position.set(0.21 * s, 0.08, 0); face.add(e); return e; });
    const brows = [-1, 1].map(s => { const b = mesh(new THREE.BoxGeometry(0.24, 0.05, 0.05), ink); b.position.set(0.21 * s, 0.25, 0.01); face.add(b); return b; });
    const mouth = mesh(new THREE.BoxGeometry(0.26, 0.05, 0.04), mouthM); mouth.position.set(0, -0.14, 0.01); face.add(mouth);
    const E = { neutral: [0, 0, 0.26, 0.05, 0], grumpy: [0.32, 0.03, 0.24, 0.04, -0.12], angry: [0.5, -0.02, 0.2, 0.07, -0.2], smug: [-0.15, 0.06, 0.3, 0.05, 0.22], happy: [-0.25, 0.06, 0.3, 0.08, 0.3], shocked: [-0.2, 0.08, 0.14, 0.14, 0] };
    // rain: thin streaks falling from the cloud's belly, looped (pure function of t)
    const rainG = grp(), drops = [], RW = (o.rainW || 1.8), RH = (o.rainH || 2.2), N = o.drops || 70;
    const dropGeo = new THREE.BoxGeometry(0.009, 0.16, 0.009), dropM = new THREE.MeshBasicMaterial({ color: '#DDEBF6', transparent: true, opacity: 0.55, depthWrite: false });
    for (let i = 0; i < N; i++) { const m = mesh(dropGeo, dropM); m.castShadow = false; drops.push({ m, x: (r() - 0.5) * RW, z: (r() - 0.5) * RW * 0.5, ph: r(), v: 0.85 + r() * 0.3 }); rainG.add(m); }
    rainG.position.y = 0.18; body.add(rainG);
    body.scale.setScalar(S);
    g.userData.update = t => {
      const ex = E[keyed(o.expr, t, o.face || 'grumpy')] || E.grumpy;
      brows.forEach((b, i) => { b.rotation.z = (i ? -1 : 1) * ex[0]; b.position.y = 0.25 + ex[1]; });
      mouth.scale.set(ex[2] / 0.26, ex[3] / 0.05, 1); mouth.rotation.z = 0; mouth.position.y = -0.14 + ex[4] * 0.1;
      const blink = ((t + (o.seed || 0) * 0.37) % 3.1) < 0.1;
      eyes.forEach(e => { e.scale.y = blink ? 0.12 : 1; });
      body.position.y = (o.bob ?? 0.06) * Math.sin(t * 1.9 + (o.seed || 0));
      body.rotation.z = 0.035 * Math.sin(t * 1.3 + 0.5); body.rotation.x = 0.02 * Math.sin(t * 1.1);
      // breathing: the cloud swells a little (a slow scale pulse) and squashes when it rains
      const raining = keyed(o.rain, t, !!o.raining);
      const pulse = 1 + 0.025 * Math.sin(t * 2.4) + (raining ? 0.02 * Math.sin(t * 9) : 0);
      body.scale.set(S * pulse, S * (2 - pulse), S * pulse);
      rainG.visible = raining;
      if (raining) drops.forEach(d => { const k = ((t * 1.6 * d.v + d.ph) % 1); d.m.position.set(d.x, -k * RH, d.z); });
    };
    g.userData.update(0); return g;
  },
  haussmann(o) { // Paris building: cream stone facade (canvas: windows, wrought-iron balconies, shop fronts with awnings), grey-blue mansard roof with dormers; front +Z
    const W = o.w || 12, H = o.h || 16, D = o.d || 10, floors = o.floors || 6, cols = o.cols || 5, g = grp();
    const wallC = o.color || '#EFE6D2', awn = o.awning || '#B5302A';
    const ft = !o.night && o.flux !== false ? imageTexture(TEXTURES.facades[Math.abs(o.seed ?? 0) % TEXTURES.facades.length]) : null;   // FLUX facades by day
    const tex = ft ? new THREE.Mesh(new THREE.PlaneGeometry(W, H), new THREE.MeshLambertMaterial({ map: ft })) : canvasPlane(W, H, (c, Wp, Hp) => {
      c.fillStyle = wallC; c.fillRect(0, 0, Wp, Hp);
      const fh = Hp / (floors + 0.3);
      c.strokeStyle = 'rgba(120,100,70,0.18)'; c.lineWidth = Hp * 0.004; for (let f = 1; f < floors; f++) { c.beginPath(); c.moveTo(0, Hp - f * fh); c.lineTo(Wp, Hp - f * fh); c.stroke(); }
      const cw = Wp / cols;
      for (let f = 0; f < floors; f++) for (let k = 0; k < cols; k++) {
        const x = k * cw + cw * 0.28, y = Hp - (f + 1) * fh + fh * 0.18, w = cw * 0.44, h = fh * 0.62;
        if (f === 0) { // shop front: big dark window + awning stripe
          c.fillStyle = '#2E3A46'; c.fillRect(k * cw + cw * 0.12, Hp - fh * 0.92, cw * 0.76, fh * 0.8);
          c.fillStyle = k % 2 ? awn : '#F4F1E8'; c.fillRect(k * cw + cw * 0.08, Hp - fh * 1.0, cw * 0.84, fh * 0.16);
          continue; }
        c.fillStyle = '#F6F2E8'; c.fillRect(x - w * 0.12, y - h * 0.06, w * 1.24, h * 1.12);
        c.fillStyle = o.night ? ((((f * 7 + k * 13 + (o.seed || 0) * 5) % 10) < 4) ? '#F2C46B' : '#27303D') : '#5B7894'; c.fillRect(x, y, w, h);   // night: about 40 % of the windows lit
        c.fillStyle = 'rgba(255,255,255,0.35)'; c.fillRect(x + w * 0.08, y + h * 0.08, w * 0.25, h * 0.5);
        if (f === 1 || f === floors - 1) { c.fillStyle = '#23262B'; c.fillRect(f === 1 ? 0 : x - w * 0.2, y + h * 0.72, f === 1 ? Wp : w * 1.4, h * 0.07); for (let b = 0; b < 6; b++) c.fillRect((f === 1 ? x - w * 0.2 : x - w * 0.2) + b * w * 0.28, y + h * 0.72, w * 0.035, h * 0.28); }
      }
    }, { res: 512 });
    const body = box(W, H, D, wallC); body.position.set(0, H / 2, -D / 2); g.add(body);
    tex.position.set(0, H / 2, 0.012); g.add(tex);
    const roofC = o.roof || '#7C8A99';
    const roof = box(W, 2.6, D, roofC, { taper: { x: 1, z: 0.55 } }); roof.position.set(0, H + 1.3, -D / 2); g.add(roof);
    for (let k = 0; k < cols; k++) g.add(at(box(1.0, 1.1, 0.9, '#E9E2D2'), -W / 2 + (k + 0.5) * W / cols, H + 1.0, -0.9));
    [-0.3, 0.25].forEach(u => g.add(at(box(0.9, 1.5, 0.9, '#C9824E'), u * W, H + 2.9, -D / 2)));   // chimney pots
    return g;
  },
  rain(o) { // a sheet of rain over w x d, h tall (streaks loop down); o.on [[t, bool]]
    const r = rng(o.seed || 41), g = grp(), W = o.w || 3, D = o.d || 2, H = o.h || 4, N = o.n || 160, L = o.len || 0.3;
    const geo = new THREE.BoxGeometry(o.thick || 0.008, L, o.thick || 0.008), m = new THREE.MeshBasicMaterial({ color: o.color || '#E2EEF8', transparent: true, opacity: o.opacity ?? 0.5, depthWrite: false }), drops = [];
    for (let i = 0; i < N; i++) { const d = mesh(geo, m); d.castShadow = false; drops.push({ d, x: (r() - 0.5) * W, z: (r() - 0.5) * D, ph: r(), v: 0.8 + r() * 0.4 }); g.add(d); }
    g.userData.update = t => { const on = keyed(o.on, t, true); g.visible = on; if (on) drops.forEach(p => { const k = (t * (o.speed || 2.2) * p.v / H * 3 + p.ph) % 1; p.d.position.set(p.x + (o.slant || 0) * k, H * (1 - k), p.z); }); };
    g.userData.update(0); return g;
  },
  earthGlobe(o) { // low-poly Earth (blue faceted sphere, green continents from seeded noise) + a soft atmosphere shell; spins
    const R = o.radius || 1, r = rng(o.seed || 5);
    const geo = new THREE.IcosahedronGeometry(R, 3).toNonIndexed(), pos = geo.attributes.position, cols = [];
    const seeds = Array.from({ length: 9 }, () => { const v = new THREE.Vector3(r() - 0.5, r() - 0.5, r() - 0.5).normalize(); return [v, 0.45 + r() * 0.35]; });
    const sea = new THREE.Color(o.sea || '#3E8FD0'), land = new THREE.Color(o.land || '#7DC46A'), land2 = new THREE.Color('#9AD07A'), ice = new THREE.Color('#F2F6F8');
    for (let i = 0; i < pos.count; i += 3) {
      const c = new THREE.Vector3(); for (let k = 0; k < 3; k++) c.add(new THREE.Vector3(pos.getX(i + k), pos.getY(i + k), pos.getZ(i + k))); c.normalize();
      let s = 0; seeds.forEach(([v, w]) => { s = Math.max(s, w - c.distanceTo(v)); });
      const col = Math.abs(c.y) > 0.9 ? ice : s > 0.12 ? (s > 0.3 ? land2 : land) : sea;
      for (let k = 0; k < 3; k++) cols.push(col.r, col.g, col.b);
    }
    geo.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3)); geo.computeVertexNormals();
    const earth = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ vertexColors: true, flatShading: true }));
    const atmo = new THREE.Mesh(new THREE.IcosahedronGeometry(R * 1.07, 3), new THREE.MeshBasicMaterial({ color: '#9FD8FF', transparent: true, opacity: 0.16, depthWrite: false }));
    const spinG = grp(earth); spinG.rotation.z = 0.41; const g = grp(spinG, atmo); g.position.y = R;
    const holder = grp(g);
    holder.userData.update = t => { earth.rotation.y = (o.spin ?? 0.35) * t; atmo.scale.setScalar(1 + 0.012 * Math.sin(t * 3)); };
    holder.userData.update(0); return holder;
  },
  orbitTrail(o) { // a wind streak looping round a sphere (radius o.r): bright ribbon whose head runs round, tail fading
    const R = o.r || 1.25, N = 48, g = grp(), segs = [];
    for (let i = 0; i < N; i++) { const m = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.05, R * TAU / N * 1.15), new THREE.MeshBasicMaterial({ color: o.color || '#FFFFFF', transparent: true, opacity: 0, depthWrite: false })); segs.push(m); g.add(m); }
    g.rotation.x = o.tilt ?? 0.5;
    g.userData.update = t => { const head = (t * (o.speed || 1.4)) % 1; segs.forEach((m, i) => { const a = i / N * TAU; m.position.set(Math.cos(a) * R, 0, Math.sin(a) * R); m.rotation.y = -a; const d = ((head - i / N) % 1 + 1) % 1; m.material.opacity = d < 0.6 ? 0.95 * (1 - d / 0.6) : 0; }); };
    g.userData.update(0); return g;
  },
  windSwirl(o) { // a fist-sized knot of wind: curved white streaks spinning round a vertical axis (the "wind" they arrest)
    const g = grp(), arcs = [], r = rng(o.seed || 9);
    for (let i = 0; i < (o.n || 7); i++) { const R = 0.25 + r() * 0.35, arc = 1.2 + r() * 1.6; const m = new THREE.Mesh(new THREE.TorusGeometry(R, 0.022, 4, 24, arc), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.85 })); m.rotation.x = PI / 2 + (r() - 0.5) * 0.8; m.position.y = 0.2 + r() * 0.9; arcs.push({ m, w: 3 + r() * 4, ph: r() * TAU }); g.add(m); }
    g.userData.update = t => arcs.forEach(a => { a.m.rotation.z = a.ph + t * a.w; a.m.position.x = 0.05 * Math.sin(t * 7 + a.ph); });
    g.userData.update(0); return g;
  },
  barrierGate(o) { // border checkpoint: white post, red/white boom pivoting at the post; o.open [[t, angleDeg]] with an overshoot
    const g = grp(), L = o.length || 4;
    g.add(at(box(0.32, 1.1, 0.32, '#F2F2EE', { outline: 0.01 }), 0, 0.55, 0), at(box(0.42, 0.12, 0.42, '#C8322A'), 0, 1.12, 0));
    if (o.sign) g.add(at(textBoard(o.sign, 0.9, 0.3, { bg: '#1E4E8C', fg: '#FFFFFF' }), 0, 1.45, 0.17));
    const piv = grp(); piv.position.set(0, 0.98, 0); g.add(piv);
    for (let i = 0; i < 8; i++) piv.add(at(box(L / 8, 0.12, 0.1, i % 2 ? '#F4F4F0' : '#D63A2F'), 0.25 + (i + 0.5) * L / 8, 0, 0));
    piv.add(at(box(0.5, 0.2, 0.2, '#3A3D44'), -0.35, 0, 0));   // counterweight
    g.userData.update = t => {
      let a = o.angle ?? 0, prev = a, at0 = -1;
      for (const [k, v] of (o.open || [])) { if (t >= k) { prev = a; a = v; at0 = k; } }
      const u = at0 < 0 ? 1 : clamp01((t - at0) / 0.35), e = ease.outBack(u);
      piv.rotation.z = (prev + (a - prev) * e) * PI / 180;
    };
    g.userData.update(0); return g;
  },
  eiffelTower(o) { // low-poly Eiffel tower (four splayed legs, two decks, tapering spire), o.h tall
    if (o.style === 'v2') return eiffelV2(o);   // (cycle 14) one connected silhouette (the reviews of 51: the old one read as a stepladder)
    const H = o.h || 30, c = o.color || '#8E6E4C', g = grp();
    [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([sx, sz]) => {
      const leg = box(0.09 * H, 0.42 * H, 0.09 * H, c, { taper: { x: 0.45, z: 0.45 } }); leg.position.set(sx * 0.12 * H, 0.2 * H, sz * 0.12 * H); leg.rotation.set(-sz * 0.32, 0, sx * 0.32); g.add(leg);
    });
    g.add(at(box(0.36 * H, 0.025 * H, 0.36 * H, c), 0, 0.2 * H, 0), at(box(0.2 * H, 0.025 * H, 0.2 * H, c), 0, 0.42 * H, 0));
    g.add(at(box(0.13 * H, 0.38 * H, 0.13 * H, c, { taper: { x: 0.35, z: 0.35 } }), 0, 0.62 * H, 0), at(box(0.035 * H, 0.18 * H, 0.035 * H, c, { taper: { x: 0.4, z: 0.4 } }), 0, 0.9 * H, 0));
    // the arch between the legs (a dark gap reads from afar)
    return g;
  },
  frMap(o) { // flat map of France + Belgium (1 degree = o.k metres): sea, neighbours, the two countries, borders, labels, Paris/Brussels pins
    const K = o.k || 10, g = grp(), Y = 0.02;
    const pr = ([lon, lat]) => [(lon - 3) * K * 0.68, -(lat - 47.5) * K];
    const shape = pts => { const s = new THREE.Shape(); pts.map(pr).forEach(([x, z], i) => i ? s.lineTo(x, -z) : s.moveTo(x, -z)); return s; };
    const flat = (pts, color, y, emissive) => { const m = mesh(new THREE.ShapeGeometry(shape(pts)), mat(color, emissive ? { emissive } : {})); m.rotation.x = -PI / 2; m.position.y = y; m.receiveShadow = true; m.castShadow = false; return m; };
    const FR = [[2.55, 51.08], [1.6, 50.9], [1.6, 50.2], [0.1, 49.5], [-1.2, 49.4], [-1.9, 49.7], [-1.6, 48.65], [-3.5, 48.8], [-4.8, 48.4], [-4.7, 47.9], [-2.2, 47.2], [-1.2, 46.2], [-1.2, 44.6], [-1.8, 43.35],
      [-0.6, 42.9], [1.7, 42.5], [3.1, 42.45], [3.2, 43.0], [4.8, 43.4], [6.2, 43.1], [7.5, 43.8], [6.8, 44.4], [7.0, 45.9], [6.1, 46.4], [7.6, 47.6], [8.2, 49.0], [6.4, 49.45], [5.9, 49.5], [4.85, 49.8], [4.8, 50.15], [4.2, 49.95], [3.6, 50.4], [2.9, 50.7]];
    const BE = [[2.55, 51.08], [2.9, 50.7], [3.6, 50.4], [4.2, 49.95], [4.8, 50.15], [4.85, 49.8], [5.4, 49.6], [5.9, 49.5], [6.4, 50.32], [6.1, 50.6], [5.7, 50.75], [5.85, 51.15], [5.0, 51.48], [4.3, 51.37], [3.4, 51.37]];
    const LAND = [[-12, 36], [16, 36], [16, 58], [-12, 58]];
    const SEA_W = [[-12, 58], [9, 58], [8, 53.5], [4.8, 52.9], [4.0, 51.9], [3.4, 51.37], [2.55, 51.08], [1.6, 50.9], [1.6, 50.2], [0.1, 49.5], [-1.2, 49.4], [-1.9, 49.7], [-1.6, 48.65], [-3.5, 48.8], [-4.8, 48.4], [-4.7, 47.9], [-2.2, 47.2], [-1.2, 46.2], [-1.2, 44.6], [-1.8, 43.35], [-3.8, 43.45], [-8.0, 43.7], [-9.3, 43.0], [-12, 42.5]];
    const UK = [[-5.7, 50.0], [-3.5, 50.3], [-1.0, 50.7], [1.4, 51.1], [1.7, 52.7], [0.3, 53.4], [-0.3, 54.5], [-3.0, 55.5], [-6.0, 56.5], [-5.5, 54.0], [-3.0, 53.3], [-4.5, 52.0], [-5.3, 51.7]];
    const MED = [[3.1, 42.45], [3.2, 43.0], [4.8, 43.4], [6.2, 43.1], [7.5, 43.8], [9.5, 44.2], [12, 42], [12, 36], [-1, 36], [0.5, 40.5], [3.2, 41.9]];
    g.add(flat(LAND, o.landOther || '#D8DFC2', 0), flat(SEA_W, o.sea || '#5AA3DB', Y), flat(MED, o.sea || '#5AA3DB', Y), flat(UK, o.landOther || '#D8DFC2', Y * 2));
    const fr = flat(FR, o.france || '#8CC768', Y * 3), be = flat(BE, o.belgium || '#F2C94C', Y * 3.2); g.add(fr, be);
    // borders: white tubes along the outlines
    const outline = (pts, col, r) => { const v = pts.concat([pts[0]]).map(pr); for (let i = 0; i < v.length - 1; i++) { const a = v[i], b = v[i + 1], d = Math.hypot(b[0] - a[0], b[1] - a[1]); const m = mesh(new THREE.BoxGeometry(r, r * 0.5, d), mat(col)); m.position.set((a[0] + b[0]) / 2, Y * 4, (a[1] + b[1]) / 2); m.rotation.y = Math.atan2(b[0] - a[0], b[1] - a[1]); m.castShadow = false; g.add(m); } };
    outline(FR, '#FFFFFF', 0.06 * K); outline(BE, '#FFFFFF', 0.06 * K);
    const lab = (txt, ll, w, size, col) => { const p = canvasPlane(w, w * 0.28, (c, W, H) => { c.clearRect(0, 0, W, H); c.font = `900 ${H * size}px Nunito, Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.lineWidth = H * 0.12; c.strokeStyle = '#1C252A'; c.lineJoin = 'round'; c.strokeText(txt, W / 2, H / 2); c.fillStyle = col; c.fillText(txt, W / 2, H / 2); }, { res: 512, transparent: true }); const [x, z] = pr(ll); p.rotation.x = -PI / 2; p.position.set(x, Y * 6, z); g.add(p); return p; };
    lab('FRANCE', [2.4, 46.6], 3.6 * K, 0.62, '#FFFFFF'); lab('BELGIQUE', [4.6, 50.62], 2.4 * K, 0.6, '#FFFFFF');
    const pin = (ll, col) => { const [x, z] = pr(ll); const p = grp(at(cyl(0.02 * K, 0.02 * K, 0.5 * K, '#3A3D44', 6), 0, 0.25 * K, 0), at(sphere(0.09 * K, col, 1), 0, 0.52 * K, 0)); p.position.set(x, 0, z); g.add(p); return p; };
    pin([2.35, 48.86], '#E0413A'); pin([4.35, 50.85], '#2F62B5');
    lab('PARIS', [2.35, 48.35], 1.6 * K, 0.6, '#FFFFFF'); lab('BRUXELLES', [4.35, 51.3], 1.8 * K, 0.5, '#FFFFFF');
    g.userData.project = pr;
    return g;
  },
  dashRoute(o) { // red dashes from A to B on the map (lon/lat via o.k like frMap), drawn progressively from o.t0 over o.dur
    const K = o.k || 10, pr = ([lon, lat]) => [(lon - 3) * K * 0.68, -(lat - 47.5) * K];
    const A = pr(o.from || [4.35, 50.85]), B = pr(o.to || [2.35, 48.86]), n = o.n || 14, g = grp(), ds = [];
    for (let i = 0; i < n; i++) { const u = (i + 0.25) / n, x = lerp(A[0], B[0], u), z = lerp(A[1], B[1], u) - Math.sin(u * PI) * 0.4 * K; const m = mesh(new THREE.BoxGeometry(0.1 * K, 0.04 * K, 0.22 * K), mat('#E0413A', { emissive: '#702018' })); m.position.set(x, 0.08 * K, z); m.rotation.y = Math.atan2(B[0] - A[0], B[1] - A[1]); ds.push(m); g.add(m); }
    g.userData.update = t => { const p = clamp01((t - (o.t0 || 0)) / (o.dur || 1)); ds.forEach((m, i) => { m.visible = i / n < p; }); };
    g.userData.update(0); return g;
  },
  prisonFront(o) { // grey prison block: barred windows, a gate, a big PRISON sign on the roof edge; o.sold [[t, true]] pops a VENDU sign
    const W = o.w || 14, H = o.h || 7, g = grp();
    g.add(at(box(W, H, 6, '#B9BDBF', { outline: 0.02 }), 0, H / 2, -3), at(box(W + 0.4, 0.4, 6.4, '#8E9396'), 0, H + 0.2, -3));
    for (let r = 0; r < 2; r++) for (let c = 0; c < 6; c++) {
      const x = -W / 2 + 1.3 + c * (W - 2.6) / 5, y = 2.2 + r * 2.6;
      g.add(at(box(0.9, 1.2, 0.08, '#2B3238'), x, y, 0.02));
      for (let b = 0; b < 4; b++) g.add(at(box(0.05, 1.2, 0.06, '#8E9396'), x - 0.33 + b * 0.22, y, 0.08));
    }
    g.add(at(box(3, 3.2, 0.1, '#5B6166'), 0, 1.6, 0.05));
    const sign = textBoard(o.text || 'PRISON', 6.4, 1.3, { bg: '#F4F1E8', fg: '#1E2A33', frame: '#1E2A33' }); sign.position.set(0, H + 1.15, 0.1); g.add(sign);
    const sold = grp(at(box(3.4, 1.5, 0.1, '#C8322A'), 0, 0, 0), at(textBoard(o.soldText || 'VENDU', 3.1, 1.2, { bg: '#C8322A', fg: '#FFFFFF' }), 0, 0, 0.06));
    sold.position.set(W * 0.22, H * 0.62, 0.3); sold.rotation.z = -0.12; g.add(sold);
    g.userData.update = t => { const on = keyed(o.sold, t, false); let at0 = -1; for (const [k, v] of (o.sold || [])) if (t >= k && v) at0 = k; sold.visible = !!on; if (on) sold.scale.setScalar(Math.max(0.01, ease.outBack(clamp01((t - at0) / 0.3)))); };
    g.userData.update(0); return g;
  },
  noticeBoard(o) { // a sign / document with text that can pop in (scale with overshoot from o.popAt); o.style 'doc' | 'sign' | 'tag'
    const w = o.w || 1.2, h = o.h || 0.8, g = grp();
    const st = o.style || 'sign';
    const bg = o.bg || (st === 'doc' ? '#F7F3E6' : st === 'tag' ? '#FFF6D8' : '#F4F1E8');   // o.bg: e.g. a chalkboard
    const b = textBoard(o.text || 'TEXTE', w, h, { bg, fg: o.fg || '#1E2A33', frame: st === 'doc' ? null : (o.frame || '#1E2A33'), size: o.textSize || 0.62 });
    const back = at(box(w + 0.04, h + 0.04, 0.03, st === 'doc' ? '#E2DCC8' : '#3A3D44'), 0, 0, -0.02);
    const inner = grp(back, b); g.add(inner);
    if (st === 'doc' && o.stamp) { const s = textBoard(o.stamp, w * 0.5, h * 0.16, { bg: '#F7F3E6', fg: '#C8322A', frame: '#C8322A', size: 0.7 }); s.position.set(w * 0.18, -h * 0.34, 0.005); s.rotation.z = 0.18; inner.add(s); }
    g.userData.update = t => { if (o.popAt == null) return; const u = clamp01((t - o.popAt) / (o.popDur || 0.32)); inner.visible = t >= o.popAt; inner.scale.setScalar(Math.max(0.01, ease.outBack(u))); inner.rotation.z = (o.tilt || 0) + 0.12 * (1 - u) * Math.sin(u * 9); };
    g.userData.update(0); return g;
  },
};
