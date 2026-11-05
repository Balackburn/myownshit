// Props for the seven "faits divers" stories (sable, lune, sapin, escargot, grève, colis, heure), tornado-replica style.
// Conventions as in props.js; small loops of motion built in (pure functions of t).
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, sphere, rng, ease, clamp01 } from './style.js';
import { grp, at, mesh, canvasPlane, inst, rod, torus } from './props.js';

const PI = Math.PI, TAU = PI * 2;
const keyAt = (list, t) => { let a0 = null; for (const [a, x] of (list || [])) if (t >= a && x) a0 = a; return a0; };
const pop = (t, a0, d = 0.3) => a0 == null || t < a0 ? 0 : Math.max(0.001, ease.outBack(clamp01((t - a0) / d)));
function sign(text, w, h, bg = '#F4F1E8', fg = '#1E2A33') {
  return canvasPlane(w, h, (c, W, H) => { c.fillStyle = bg; c.fillRect(0, 0, W, H); c.fillStyle = fg; c.textAlign = 'center'; c.textBaseline = 'middle';
    const L = String(text).split('\n'), m = Math.max(...L.map(l => l.length)); let px = Math.min(H * 0.7 / L.length, W * 0.9 / (m * 0.62)); c.font = `900 ${px}px Arial`;
    const wide = Math.max(...L.map(l => c.measureText(l).width)); if (wide > W * 0.9) { px *= W * 0.9 / wide; c.font = `900 ${px}px Arial`; }
    L.forEach((l, i) => c.fillText(l, W / 2, H / 2 + (i - (L.length - 1) / 2) * px * 1.1)); }, { res: 512 });
}
function palm(h = 1) { const g = grp(at(cyl(0.05 * h, 0.08 * h, h, '#8A6440', 6, { pivot: 'bottom' }), 0, 0, 0));
  for (let i = 0; i < 6; i++) { const lf = box(0.7 * h, 0.03, 0.18 * h, '#3E9B5F', { taper: { x: 1, z: 0.3 } }); lf.position.set(Math.cos(i / 6 * TAU) * 0.3 * h, h, Math.sin(i / 6 * TAU) * 0.3 * h); lf.rotation.set(0, -i / 6 * TAU, -0.45); g.add(lf); }
  return g; }


// a real grain of sand: an irregular faceted quartz pebble (icosahedron with per-vertex jitter, squashed), pivot at its bottom
function grainGeo(r, seed, detail = 1) {
  const R = rng(seed), geo = new THREE.IcosahedronGeometry(r, detail), pos = geo.attributes.position, v = new THREE.Vector3(), J = new Map();
  const sx = 0.95 + R() * 0.45, sy = 0.62 + R() * 0.22, sz = 0.8 + R() * 0.3;
  for (let i = 0; i < pos.count; i++) { v.fromBufferAttribute(pos, i); const key = `${v.x.toFixed(3)},${v.y.toFixed(3)},${v.z.toFixed(3)}`;
    if (!J.has(key)) J.set(key, 0.82 + R() * 0.32); const s = J.get(key); pos.setXYZ(i, v.x * s * sx, v.y * s * sy, v.z * s * sz); }
  geo.computeBoundingBox(); geo.translate(0, -geo.boundingBox.min.y, 0); geo.computeVertexNormals(); return geo;
}
const SAND = ['#E6C67E', '#DDB76C', '#EDD39A', '#D3AA62'];
// tiny flags on toothpicks: Brittany (gwenn-ha-du), Sardinia (four Moors), Italy, France
const flagDraw = kind => (c, W, H) => {
    if (kind === 'bzh') { for (let i = 0; i < 9; i++) { c.fillStyle = i % 2 ? '#F4F4F0' : '#17171B'; c.fillRect(0, i * H / 9, W, H / 9 + 1); }
      c.fillStyle = '#F4F4F0'; c.fillRect(0, 0, W * 0.42, H * 5 / 9); c.fillStyle = '#17171B';
      for (let r = 0; r < 3; r++) for (let q = 0; q < 3; q++) { const x = W * (0.07 + q * 0.13 + (r % 2) * 0.06), y = H * (0.1 + r * 0.15); c.beginPath(); c.moveTo(x, y - H * 0.05); c.lineTo(x + W * 0.025, y + H * 0.04); c.lineTo(x - W * 0.025, y + H * 0.04); c.fill(); } }
    else if (kind === 'sard') { c.fillStyle = '#F4F4F0'; c.fillRect(0, 0, W, H); c.fillStyle = '#C8322A'; c.fillRect(W * 0.44, 0, W * 0.12, H); c.fillRect(0, H * 0.41, W, H * 0.18);
      c.fillStyle = '#17171B'; for (const [x, y] of [[0.22, 0.2], [0.78, 0.2], [0.22, 0.8], [0.78, 0.8]]) { c.beginPath(); c.arc(W * x, H * y, H * 0.11, 0, TAU); c.fill(); c.fillStyle = '#F4F4F0'; c.fillRect(W * x - H * 0.12, H * y - H * 0.04, H * 0.24, H * 0.05); c.fillStyle = '#17171B'; } }
    else if (kind === 'mec') { c.fillStyle = '#2F8F7A'; c.fillRect(0, 0, W, H); c.fillStyle = '#F2C94C'; c.fillRect(0, H * 0.8, W, H * 0.2); c.fillRect(0, 0, W, H * 0.08);   // the flag of his apartment: his own face
      c.fillStyle = '#E2B48A'; c.fillRect(W * 0.4, H * 0.2, W * 0.2, H * 0.48); c.fillStyle = '#1C1C20'; c.fillRect(W * 0.4, H * 0.17, W * 0.2, H * 0.07); c.fillRect(W * 0.44, H * 0.34, W * 0.03, H * 0.04); c.fillRect(W * 0.53, H * 0.34, W * 0.03, H * 0.04);
      c.fillRect(W * 0.45, H * 0.5, W * 0.1, H * 0.02); c.fillStyle = '#7A5A48'; for (let i = 0; i < 14; i++) c.fillRect(W * (0.42 + (i * 37 % 16) / 100), H * (0.52 + (i * 53 % 14) / 100), W * 0.008, H * 0.012); c.fillStyle = '#C8322A'; c.fillRect(W * 0.48, H * 0.68, W * 0.04, H * 0.12); }
    else { const cols = kind === 'it' ? ['#2E8B4E', '#F4F4F0', '#C8322A'] : ['#24448E', '#F4F4F0', '#D03A34']; cols.forEach((col, i) => { c.fillStyle = col; c.fillRect(i * W / 3, 0, W / 3 + 1, H); }); }
};
function miniFlag(kind, w = 0.08) {
  const h = w * 0.66, g = grp(at(cyl(0.0025 * w / 0.08, 0.0025 * w / 0.08, h * 2.4, '#E9DDBF', 4, { pivot: 'bottom', noGrain: true }), 0, 0, 0));
  const f = canvasPlane(w, h, flagDraw(kind), { res: 256 });
  f.position.set(w / 2, h * 2.4 - h / 2, 0); g.add(f); g.userData.cloth = f; return g;
}

// the international wheelchair pictogram, drawn white, centred at (cx, cy), u = overall size in px
function wheelchair(g, cx, cy, u) {
  const x0 = cx - u * 0.41, y0 = cy - u * 0.46; g.lineCap = 'round'; g.lineJoin = 'round'; g.fillStyle = g.strokeStyle = '#F4F4F0';
  g.beginPath(); g.arc(x0 + u * 0.28, y0 + u * 0.09, u * 0.085, 0, TAU); g.fill();
  g.lineWidth = u * 0.1; g.beginPath(); g.moveTo(x0 + u * 0.28, y0 + u * 0.24); g.lineTo(x0 + u * 0.3, y0 + u * 0.56); g.lineTo(x0 + u * 0.62, y0 + u * 0.56); g.lineTo(x0 + u * 0.72, y0 + u * 0.84); g.stroke();
  g.beginPath(); g.moveTo(x0 + u * 0.29, y0 + u * 0.36); g.lineTo(x0 + u * 0.52, y0 + u * 0.36); g.stroke();
  g.lineWidth = u * 0.075; g.beginPath(); g.arc(x0 + u * 0.36, y0 + u * 0.66, u * 0.26, -0.3 * PI, 1.25 * PI); g.stroke();
}

// a flat faceted disc (patty, lettuce): n-gon with jittered rim, pivot at its bottom
function facetDisc(r, h, color, seed = 3) {
  const R = rng(seed), shape = new THREE.Shape(), n = 14;
  for (let i = 0; i <= n; i++) { const a = i / n * TAU, rr = r * (0.94 + R() * 0.1); i ? shape.lineTo(Math.cos(a) * rr, Math.sin(a) * rr) : shape.moveTo(Math.cos(a) * rr, Math.sin(a) * rr); }
  const geo = new THREE.ExtrudeGeometry(shape, { depth: h, bevelEnabled: false }); geo.rotateX(-PI / 2);
  const m = new THREE.Mesh(geo, mat(color)); m.castShadow = m.receiveShadow = true; return m;
}

// copper one-cent coins: the face texture (the common side: a big 1, EURO CENT, a ring of stars) and an instanced pile/scatter of plain coins
const CU = ['#C9783F', '#B86A36', '#D48A4E', '#A85F31'];
function centFace(c, W, H, value = '1') {
  c.fillStyle = '#C9783F'; c.beginPath(); c.arc(W / 2, H / 2, W * 0.5, 0, TAU); c.fill(); c.strokeStyle = '#A85F31'; c.lineWidth = W * 0.05; c.beginPath(); c.arc(W / 2, H / 2, W * 0.46, 0, TAU); c.stroke();
  c.fillStyle = '#8E4E26'; for (let i = 0; i < 12; i++) { const a = i / 12 * TAU, x = W / 2 + Math.cos(a) * W * 0.38, y = H / 2 + Math.sin(a) * H * 0.38; c.beginPath(); for (let k = 0; k < 10; k++) { const b = a + k * PI / 5, r = k % 2 ? W * 0.012 : W * 0.03; c.lineTo(x + Math.cos(b) * r, y + Math.sin(b) * r); } c.fill(); }
  c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${W * 0.4}px Arial`; c.fillText(value, W * 0.42, H * 0.47); c.font = `900 ${W * 0.07}px Arial`; c.fillText('EURO', W * 0.66, H * 0.4); c.fillText('CENT', W * 0.66, H * 0.5);
}
function coinScatter(list, r = 0.03) { const geo = new THREE.CylinderGeometry(r, r, r * 0.2, 10); return inst(geo, mat('#C9783F', { noGrain: true }), list.map(q => q.slice(0, 9)), list.map(q => q[9])); }

export const NEWS_PROPS = {
  burger(o) { // a burger at twice life size (Ø 0.25 m): bun, patty, cheese, lettuce, tomato, sesame dome; o.openAt lifts the top;
    // o.pick: a toothpick flag (text, e.g. 'VEGAN') that pops in at o.pickAt
    const g = grp(), BUN = o.bun || '#D9A15A', R0 = 0.12;
    g.add(at(cyl(R0, R0 * 0.96, 0.04, BUN, 14, { pivot: 'bottom', outline: 0.004 }), 0, 0, 0));
    const patty = at(facetDisc(R0 * 1.04, 0.036, o.patty || '#6E4128', 3), 0, 0.04, 0); g.add(patty);
    const ch = at(box(0.19, 0.008, 0.19, '#F2C230'), 0, 0.08, 0, 0, PI / 4, 0); g.add(ch);
    const top = grp(at(facetDisc(R0 * 1.08, 0.012, '#7DBE5A', 9), 0, 0, 0), at(cyl(R0 * 0.82, R0 * 0.82, 0.012, '#D9483B', 12), 0, 0.012, 0));
    const dome = new THREE.Mesh(new THREE.SphereGeometry(R0, 16, 8, 0, TAU, 0, PI / 2), mat(BUN)); dome.scale.y = 0.62; dome.position.y = 0.026; dome.castShadow = true; top.add(dome);
    const rs = rng(4); for (let i = 0; i < 14; i++) { const a = rs() * TAU, rr = R0 * (0.25 + rs() * 0.6), yy = 0.026 + 0.62 * Math.sqrt(Math.max(0, R0 * R0 - rr * rr)); const se = sphere(0.006, '#F6EED8', 0, { noGrain: true }); se.scale.set(1, 0.6, 1.6); se.position.set(Math.cos(a) * rr, yy, Math.sin(a) * rr); se.rotation.y = a; top.add(se); }
    top.position.y = 0.086; g.add(top);
    let pick = null; if (o.pick) { pick = grp(at(cyl(0.003, 0.003, 0.2, '#E9DDBF', 4, { pivot: 'bottom', noGrain: true }), 0, 0, 0)); const f = canvasPlane(0.09, 0.045, (c, W, H) => { c.fillStyle = '#4E9A4A'; c.fillRect(0, 0, W, H); c.fillStyle = '#FFFFFF'; c.font = `900 ${H * 0.62}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.pick, W / 2, H * 0.55); }, { res: 256 });
      f.position.set(0.045, 0.175, 0); pick.add(f); pick.position.set(0.02, 0.1, 0.01); g.add(pick); }
    g.userData.update = t => { const k = o.openAt != null && t > o.openAt ? ease.outBack(clamp01((t - o.openAt) / 0.35)) : 0; top.position.y = 0.086 + 0.17 * k; top.rotation.x = -0.5 * k; top.position.z = -0.05 * k;
      if (pick) { pick.scale.setScalar(o.pickAt != null ? pop(t, o.pickAt, 0.3) : 1); pick.visible = !(o.openAt != null && t > o.openAt); } };
    g.userData.update(0); return g;
  },
  soyCostume(o) { // cardboard sandwich-board costume for the soy character, with a hole for its face: o.kind 'steak' | 'milk' | 'cheese' | 'nugget';
    // attach to the soy's 'head' joint with offset [0, 0.3, 0]; o.popAt pops it on
    const W0 = 0.78, H0 = 0.9, kind = o.kind || 'steak';
    const draw = (c, W, H) => {
      const lab = (t, col, y) => { c.fillStyle = col; c.font = `900 ${H * 0.1}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(t, W / 2, H * y); };
      if (kind === 'steak') { c.fillStyle = '#7A4428'; c.beginPath(); c.ellipse(W / 2, H * 0.52, W * 0.48, H * 0.42, 0.15, 0, TAU); c.fill(); c.strokeStyle = '#4A2814'; c.lineWidth = H * 0.035;
        for (let i = -2; i <= 2; i++) { c.beginPath(); c.moveTo(W * (0.2 + i * 0.16), H * 0.25); c.lineTo(W * (0.45 + i * 0.16), H * 0.85); c.stroke(); } c.fillStyle = '#E8D8C8'; for (let i = 0; i < 9; i++) { c.beginPath(); c.arc(W * (0.2 + (i * 37 % 60) / 100), H * (0.3 + (i * 53 % 50) / 100), H * 0.012, 0, TAU); c.fill(); } lab('STEAK', '#FFF4E0', 0.86); }
      else if (kind === 'milk') { c.fillStyle = '#F6F6F2'; c.fillRect(W * 0.08, H * 0.18, W * 0.84, H * 0.8); c.fillStyle = '#3E6FB5'; c.beginPath(); c.moveTo(W * 0.08, H * 0.18); c.lineTo(W * 0.5, H * 0.02); c.lineTo(W * 0.92, H * 0.18); c.fill(); c.fillRect(W * 0.08, H * 0.76, W * 0.84, H * 0.16);
        c.fillStyle = '#1C1C20'; [[0.22, 0.3, 0.07], [0.78, 0.36, 0.06], [0.7, 0.68, 0.05], [0.25, 0.66, 0.05]].forEach(([x, y, r]) => { c.beginPath(); c.arc(W * x, H * y, W * r, 0, TAU); c.fill(); }); lab('LAIT', '#FFFFFF', 0.84); }
      else if (kind === 'cheese') { c.fillStyle = '#F2C94C'; c.beginPath(); c.moveTo(W * 0.04, H * 0.96); c.lineTo(W * 0.96, H * 0.96); c.lineTo(W * 0.9, H * 0.08); c.closePath(); c.fill(); c.fillStyle = '#D9A92E';
        [[0.72, 0.3, 0.05], [0.8, 0.62, 0.06], [0.3, 0.86, 0.04], [0.62, 0.84, 0.035]].forEach(([x, y, r]) => { c.beginPath(); c.arc(W * x, H * y, W * r, 0, TAU); c.fill(); }); lab('FROMAGE', '#7A4A10', 0.9); }
      else { c.fillStyle = '#D9A04A'; c.beginPath(); for (let i = 0; i <= 14; i++) { const a = i / 14 * TAU, rr = 0.44 + 0.05 * Math.sin(i * 2.7); c.lineTo(W / 2 + Math.cos(a) * W * rr, H * 0.5 + Math.sin(a) * H * rr * 0.92); } c.fill(); c.fillStyle = '#B97A2A'; for (let i = 0; i < 30; i++) { c.beginPath(); c.arc(W * (0.15 + (i * 29 % 70) / 100), H * (0.15 + (i * 41 % 70) / 100), H * 0.01, 0, TAU); c.fill(); } lab('NUGGET', '#FFF4E0', 0.86); }
      c.globalCompositeOperation = 'destination-out'; c.beginPath(); c.arc(W / 2, H * (0.5 - 0.09 / H0), W * 0.2, 0, TAU); c.fill(); c.globalCompositeOperation = 'source-over';
    };
    const g = grp(), front = canvasPlane(W0, H0, draw, { res: 512, transparent: true }), back = canvasPlane(W0, H0, draw, { res: 512, transparent: true });
    front.position.z = 0.285; back.position.z = -0.285; back.rotation.y = PI; g.add(front, back);
    for (const sx of [-1, 1]) g.add(at(box(0.025, 0.012, 0.57, '#C9A27A'), sx * 0.2, 0.36, 0));   // shoulder straps
    g.userData.update = t => { if (o.popAt != null) g.scale.setScalar(pop(t, o.popAt, 0.3)); }; g.userData.update(0); return g;
  },
  conspiracyBoard(o) { // cork board: the soy's mugshot in the middle, its fake identities around, red strings drawing in from o.drawAt
    const w = o.w || 1.6, h = o.h || 1.05, g = grp(at(box(w + 0.08, h + 0.08, 0.04, '#8A5A34', { outline: 0.006 }), 0, 0, 0), at(box(w, h, 0.045, '#C99A62'), 0, 0, 0.002));
    const pins = [['SOJA', 0, 0.02, '#E6C878'], ['STEAK', -0.52, 0.28, '#7A4428'], ['LAIT', 0.52, 0.28, '#F6F6F2'], ['FROMAGE', -0.52, -0.28, '#F2C94C'], ['NUGGETS', 0.52, -0.28, '#D9A04A']];
    const strings = [];
    pins.forEach(([t, x, y, col], i) => { const ph = canvasPlane(0.3, 0.34, (c, W, H) => { c.fillStyle = '#FAFAF4'; c.fillRect(0, 0, W, H); c.fillStyle = col; c.fillRect(W * 0.08, H * 0.07, W * 0.84, H * 0.66);
        if (i === 0) { c.fillStyle = '#1C1C20'; [0.38, 0.62].forEach(ex => { c.beginPath(); c.arc(W * ex, H * 0.36, W * 0.06, 0, TAU); c.fill(); }); c.fillRect(W * 0.4, H * 0.52, W * 0.2, H * 0.03); }
        c.fillStyle = '#1C252A'; c.font = `900 ${H * 0.13}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; const ww = c.measureText(t).width; if (ww > W * 0.9) c.font = `900 ${H * 0.13 * W * 0.9 / ww}px Arial`; c.fillText(t, W / 2, H * 0.86); }, { res: 256 });
      ph.position.set(x, y, 0.03); ph.rotation.z = ((i * 37) % 7 - 3) * 0.02; g.add(ph, at(sphere(0.016, '#C8322A', 0), x, y + 0.15, 0.04));
      if (i) { const dx = x, dy = y, L = Math.hypot(dx, dy), st = grp(at(box(1, 0.012, 0.006, '#C8322A', { noGrain: true }), 0.5, 0, 0)); st.position.set(0, 0.02, 0.05); st.rotation.z = Math.atan2(dy, dx); st.userData.L = L; g.add(st); strings.push(st); } });
    g.userData.update = t => { strings.forEach((st, i) => { const a0 = (o.drawAt ?? 0) + i * 0.18, k = clamp01((t - a0) / 0.25); st.scale.x = Math.max(0.001, st.userData.L * k); }); };
    g.userData.update(0); return g;
  },
  chefHat(o) { // a white chef's toque (for the soy character: attach to its 'head' joint, offset about [0, 0.63, 0])
    const g = grp(at(cyl(0.13, 0.13, 0.12, '#F6F6F2', 12, { pivot: 'bottom', outline: 0.008 }), 0, 0, 0));
    [[0, 0.2, 0, 0.15], [-0.09, 0.17, 0.02, 0.1], [0.09, 0.17, -0.02, 0.1], [0, 0.17, 0.08, 0.1]].forEach(([x, y, z, r]) => g.add(at(sphere(r, '#F6F6F2', 1), x, y, z)));
    return g;
  },
  canteenTray(o) { // a grey prison-canteen tray with compartments: a patty, a glass of milk, a wedge of cheese (all soy, says the menu); o.extra adds a second patty
    const g = grp(at(box(0.46, 0.022, 0.32, '#9AA2A8', { outline: 0.005 }), 0, 0.011, 0));
    for (const [x, z, w, d] of [[0, 0, 0.012, 0.3], [0.08, 0.06, 0.3, 0.012]]) g.add(at(box(w, 0.03, d, '#8A9298'), x, 0.025, z));
    g.add(at(facetDisc(0.07, 0.025, '#6E4128', 5), -0.11, 0.022, 0.0), at(cyl(0.035, 0.03, 0.09, '#F4F6F8', 10, { pivot: 'bottom' }), 0.14, 0.022, -0.08), at(box(0.07, 0.04, 0.05, '#F2C94C', { taper: { x: 0.2, z: 1 } }), 0.12, 0.042, 0.08));
    if (o.extra) g.add(at(facetDisc(0.07, 0.025, '#6E4128', 8), -0.11, 0.048, 0.02));
    return g;
  },
  centCoin(o) { // a one-cent coin at hero size (o.r, default 0.08): copper, drawn faces; o.spin [t0, t1] spins on its edge then falls flat (like a coin on a table)
    const r = o.r || 0.08, face = canvasPlane(2 * r, 2 * r, (c, W, H) => centFace(c, W, H, o.value || '1'), { res: 256, transparent: true });
    const body = at(cyl(r, r, r * 0.16, '#B86A36', 24, { noGrain: true }), 0, 0, 0, PI / 2); const f1 = face, f2 = face.clone(); f1.position.z = r * 0.081; f2.position.z = -r * 0.081; f2.rotation.y = PI;
    const coin = grp(body, f1, f2), g = grp(coin); coin.position.y = r;
    g.userData.update = t => { if (!o.spin) return; const [a, b] = o.spin, k = clamp01((t - a) / (b - a)); coin.rotation.y = (t - a > 0 ? (t - a) : 0) * 14 * (1 - k * 0.7);
      const fall = clamp01((k - 0.6) / 0.4); coin.rotation.x = -fall * PI / 2; coin.position.y = r * (1 - fall) + r * 0.08 * fall + 0.002; };
    g.userData.update(0); return g;
  },
  coinHeap(o) { // a heap of one-cent coins: a copper mound with loose coins on its surface; o.R radius, o.H height, o.n coins; o.grow [t0, t1] piles it up
    const R0 = o.R || 1, H0 = o.H || 0.6, n = o.n || 300, rr = rng(o.seed || 11), g = grp();
    const mound = new THREE.Mesh(new THREE.ConeGeometry(R0, H0, 18, 3), mat('#B86A36', { noGrain: true })); mound.position.y = H0 / 2; mound.castShadow = mound.receiveShadow = true;
    const pos = mound.geometry.attributes.position; for (let i = 0; i < pos.count; i++) { const y = pos.getY(i); if (y < H0 / 2 - 0.001 && y > -H0 / 2 + 0.001) { pos.setX(i, pos.getX(i) * (0.92 + rr() * 0.16)); pos.setZ(i, pos.getZ(i) * (0.92 + rr() * 0.16)); } } mound.geometry.computeVertexNormals(); g.add(mound);
    const list = []; for (let i = 0; i < n; i++) { const a = rr() * TAU, u = Math.sqrt(rr()), d = u * R0, y = H0 * (1 - u) + 0.01; list.push([Math.cos(a) * d, y, Math.sin(a) * d, (rr() - 0.5) * 1.2, rr() * TAU, (rr() - 0.5) * 1.2, 1, 1, 1, CU[i % 4]]); }
    g.add(coinScatter(list, o.coinR || 0.035));
    g.userData.update = t => { if (!o.grow) return; const [a, b] = o.grow, k = Math.max(0.01, ease.out(clamp01((t - a) / (b - a)))); g.scale.set(0.6 + 0.4 * k, k, 0.6 + 0.4 * k); };
    g.userData.update(0); return g;
  },
  coinLayer(o) { // a street buried in coins: a copper slab o.w × o.d, o.h deep, its top strewn with coins and soft bumps
    const w = o.w || 10, d = o.d || 10, h = o.h || 0.8, rr = rng(o.seed || 13), g = grp();
    const geo = new THREE.PlaneGeometry(w, d, 24, 24).rotateX(-PI / 2), pos = geo.attributes.position;
    for (let i = 0; i < pos.count; i++) pos.setY(i, h + 0.12 * Math.sin(pos.getX(i) * 1.3 + rr()) * Math.cos(pos.getZ(i) * 1.1) + rr() * 0.05);
    geo.computeVertexNormals(); const top = new THREE.Mesh(geo, mat('#B86A36', { noGrain: true })); top.receiveShadow = true; g.add(top);
    const list = []; for (let i = 0; i < (o.n || 900); i++) { const x = (rr() - 0.5) * w, z = (rr() - 0.5) * d; list.push([x, h + 0.12 * Math.sin(x * 1.3) * Math.cos(z * 1.1) + 0.07, z, (rr() - 0.5) * 1.0, rr() * TAU, (rr() - 0.5) * 1.0, 1, 1, 1, CU[i % 4]]); }
    g.add(coinScatter(list, o.coinR || 0.04)); return g;
  },
  dumpTruck(o) { // a dump truck facing +X (cab at +X), its bed full of coins; o.tipAt raises the bed and pours a stream of coins out of the back
    const C = o.color || '#E9B23A', g = grp();
    g.add(at(box(4.6, 0.3, 1.9, '#2A2A2E'), 0, 0.75, 0), at(box(1.5, 1.5, 2.0, C, { outline: 0.012 }), 1.7, 1.55, 0), at(box(0.06, 0.7, 1.7, '#7FC2EE', { emissive: '#2A4A60' }), 2.46, 1.85, 0));
    [[1.6, 1.0], [1.6, -1.0], [-0.8, 1.0], [-0.8, -1.0], [-1.7, 1.0], [-1.7, -1.0]].forEach(([x, z]) => g.add(at(cyl(0.45, 0.45, 0.35, '#1C1E22', 12), x, 0.45, z, PI / 2, 0, 0)));
    const bed = grp(); bed.position.set(-2.3, 0.95, 0); g.add(bed);
    bed.add(at(box(3.2, 0.12, 2.0, C), 1.6, 0.06, 0), at(box(3.2, 1.0, 0.1, C, { outline: 0.01 }), 1.6, 0.5, 0.95), at(box(3.2, 1.0, 0.1, C, { outline: 0.01 }), 1.6, 0.5, -0.95), at(box(0.1, 1.1, 2.0, C, { outline: 0.01 }), 3.15, 0.55, 0));
    const fill = new THREE.Mesh(new THREE.SphereGeometry(1, 14, 6, 0, TAU, 0, PI / 2), mat('#B86A36', { noGrain: true })); fill.scale.set(1.5, 0.55, 0.9); fill.position.set(1.6, 0.85, 0); bed.add(fill);
    const rr = rng(o.seed || 17), drops = []; for (let i = 0; i < 70; i++) drops.push([0, 0, 0, rr() * 3, rr() * 3, rr() * 3, 1, 1, 1, CU[i % 4]]);
    const stream = coinScatter(drops, 0.05); g.add(stream); stream.visible = false;
    const M = new THREE.Object3D(), ph = drops.map(() => rr());
    g.userData.update = t => { const k = o.tipAt != null ? ease.inOut(clamp01((t - o.tipAt) / 0.7)) : 0; bed.rotation.z = 0.85 * k; fill.scale.y = 0.55 * (1 - 0.6 * clamp01((t - (o.tipAt ?? 1e9) - 0.4) / 1.5));
      stream.visible = k > 0.4; if (!stream.visible) return;
      drops.forEach((q, i) => { const u = ((t - o.tipAt) * 1.4 + ph[i]) % 1, x = -2.45 - u * 0.9, y = 1.2 - u * u * 1.6 + 0.3, z = (ph[i] - 0.5) * 1.6; M.position.set(x, Math.max(0.05, y), z); M.rotation.set(t * 5 + i, i, t * 3); M.updateMatrix(); stream.setMatrixAt(i, M.matrix); }); stream.instanceMatrix.needsUpdate = true; };
    g.userData.update(0); return g;
  },
  doormat(o) { // a coir doormat "BIENVENUE" (0.7 × 0.45) lying flat; o.line draws a dotted border across it; o.splitAt cuts it in two halves that slide apart
    const w = o.w || 0.7, d = o.d || 0.45, draw = (x0, x1) => (c, W, H) => { c.fillStyle = '#A9773F'; c.fillRect(0, 0, W, H); c.fillStyle = '#8A5E2E'; for (let i = 0; i < 300; i++) c.fillRect(((i * 97) % 1000) / 1000 * W, ((i * 61) % 1000) / 1000 * H, W * 0.006, H * 0.02);
      const Wf = W / (x1 - x0), txt = o.text || 'BIENVENUE'; let fs = H * 0.26; c.font = `900 ${fs}px Arial`; const tw = c.measureText(txt).width; if (tw > Wf * 0.86) fs *= Wf * 0.86 / tw;
      c.save(); c.translate(-x0 * Wf, 0); c.fillStyle = '#3A2A1A'; c.font = `900 ${fs}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(txt, Wf / 2, H / 2); // a half shows its part of the full mat's text
      if (o.line) { c.strokeStyle = '#F4F4F0'; c.lineWidth = Wf * 0.012; c.setLineDash([Wf * 0.03, Wf * 0.025]); c.beginPath(); c.moveTo(Wf * 0.62, 0); c.lineTo(Wf * 0.62, H); c.stroke(); } c.restore(); };
    const half = (x0, x1) => { const pl = canvasPlane(w * (x1 - x0), d, draw(x0, x1), { res: 256 }); pl.rotation.x = -PI / 2; const gg = grp(at(box(w * (x1 - x0), 0.02, d, '#8A5E2E'), 0, 0.01, 0), pl); pl.position.y = 0.021; gg.position.x = (x0 + x1 - 1) / 2 * w; return gg; };
    const g = grp(), a = half(0, o.splitAt != null ? 0.5 : 1); g.add(a); let b = null; if (o.splitAt != null) { b = half(0.5, 1); g.add(b); }
    g.userData.update = t => { if (!b) return; const k = ease.outBack(clamp01((t - o.splitAt) / 0.4)); a.position.x = -w / 4 - 0.12 * k; b.position.x = w / 4 + 0.12 * k; a.rotation.y = 0.12 * k; b.rotation.y = -0.12 * k; };
    g.userData.update(0); return g;
  },
  accordion(o) { // an accordion held in both hands (attach to the right hand): red bellows that squeeze in and out, white keys
    const g = grp(), bel = grp(); g.add(at(box(0.08, 0.32, 0.22, '#1C1C20', { outline: 0.006 }), -0.2, 0, 0), at(box(0.08, 0.32, 0.22, '#1C1C20', { outline: 0.006 }), 0.2, 0, 0), at(box(0.015, 0.28, 0.06, '#F4F4F0'), -0.245, 0, 0.06));
    for (let i = 0; i < 7; i++) bel.add(at(box(0.04, 0.3, 0.21, i % 2 ? '#C8322A' : '#9A2420'), -0.12 + i * 0.04, 0, 0)); g.add(bel);
    g.userData.update = t => { const k = 1 + 0.35 * Math.sin(t * 7); bel.scale.x = k; g.children[1].position.x = 0.2 * (0.6 + 0.4 * k); };
    g.userData.update(0); return g;
  },
  banknote(o) { // a banknote of the apartment republic with his face on it: o.value, o.w (default 0.32 m)
    const w = o.w || 0.32, n = canvasPlane(w, w * 0.5, (c, W, H) => { c.fillStyle = '#BFE0C9'; c.fillRect(0, 0, W, H); c.strokeStyle = '#2F7F5C'; c.lineWidth = H * 0.05; c.strokeRect(H * 0.05, H * 0.05, W - H * 0.1, H - H * 0.1);
      c.fillStyle = '#E2B48A'; c.fillRect(W * 0.1, H * 0.2, W * 0.16, H * 0.6); c.fillStyle = '#1C1C20'; c.fillRect(W * 0.1, H * 0.16, W * 0.16, H * 0.09); c.fillRect(W * 0.13, H * 0.38, W * 0.025, H * 0.05); c.fillRect(W * 0.2, H * 0.38, W * 0.025, H * 0.05); c.fillRect(W * 0.14, H * 0.6, W * 0.08, H * 0.025);
      c.fillStyle = '#C8322A'; c.fillRect(W * 0.17, H * 0.78, W * 0.025, H * 0.12); c.fillStyle = '#1E4E3A'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${H * 0.36}px Arial`; c.fillText(o.value || '100', W * 0.64, H * 0.46);
      c.font = `900 ${H * 0.09}px Arial`; c.fillText(o.text || 'RÉPUBLIQUE DU 3e GAUCHE', W * 0.6, H * 0.82); }, { res: 512 });
    return grp(n);
  },
  livingBike(o) { // a bicycle that rides itself ("Le vélo"): spinning wheels and crank (o.speed m/s), googly eyes on the handlebar stem that
    // look around and blink, a gentle lean and bob; o.jersey (yellow cloth on the top tube), o.bib (race number), o.shades (sunglasses), o.color
    const c = o.color || '#C8322A', A = [-0.52, 0.355, 0], Bb = [0, 0.33, 0], S = [-0.12, 0.85, 0], H = [0.42, 0.86, 0], HL = [0.45, 0.72, 0], F = [0.52, 0.355, 0];
    const body = grp(rod(Bb, S, 0.024, c), rod(S, H, 0.024, c), rod(Bb, HL, 0.026, c), rod(A, Bb, 0.019, c), rod(A, S, 0.017, c), rod(H, F, 0.021, '#9AA0A6'),
      rod(S, [-0.14, 0.95, 0], 0.016, '#9AA0A6'), at(box(0.22, 0.05, 0.1, '#1C1C20'), -0.16, 0.97, 0), rod(H, [0.38, 1.02, 0], 0.017, '#9AA0A6'), rod([0.38, 1.02, -0.27], [0.38, 1.02, 0.27], 0.017, '#1C1C20'));
    const wheels = [A, F].map(p => { const w = grp(at(torus(0.33, 0.026, '#1C1C20', 4, 18), 0, 0, 0), at(cyl(0.04, 0.04, 0.06, '#9AA0A6', 6), 0, 0, 0, PI / 2));
      for (let i = 0; i < 6; i++) { const a = i / 6 * PI; w.add(rod([-Math.cos(a) * 0.31, -Math.sin(a) * 0.31, 0], [Math.cos(a) * 0.31, Math.sin(a) * 0.31, 0], 0.005, '#B9BDC2')); }
      w.position.set(...p); body.add(w); return w; });
    const crank = grp(at(cyl(0.07, 0.07, 0.02, '#9AA0A6', 10), 0, 0, 0.05, PI / 2), rod([0, 0, 0.06], [0, -0.17, 0.06], 0.012, '#5A5E62'), rod([0, 0, -0.06], [0, 0.17, -0.06], 0.012, '#5A5E62'),
      at(box(0.1, 0.02, 0.05, '#1C1C20'), 0, -0.17, 0.09), at(box(0.1, 0.02, 0.05, '#1C1C20'), 0, 0.17, -0.09)); crank.position.set(...Bb); body.add(crank);
    body.add(rod([0, 0.33, 0.05], [-0.52, 0.355, 0.05], 0.006, '#3A3D44'));   // chain
    const eyes = grp(), lids = [], pupils = []; [-1, 1].forEach(sd => { const ball = sphere(0.055, '#FFFFFF', 1, { noGrain: true }); ball.scale.z = 0.7; const pu = sphere(0.025, '#1C1C20', 0, { noGrain: true }); pu.position.set(0, 0, 0.04); ball.add(pu); pupils.push(pu);
      const lid = mesh(new THREE.SphereGeometry(0.058, 12, 6, 0, TAU, 0, PI / 2), mat(c)); lid.rotation.x = -PI / 2; lid.scale.y = 0.01; ball.add(lid); lids.push(lid); ball.position.set(0, 0, sd * 0.065); eyes.add(ball); });
    eyes.position.set(0.47, 0.98, 0); eyes.rotation.y = PI / 2; body.add(eyes);
    if (o.jersey) { const j = grp(at(box(0.36, 0.2, 0.02, '#F2C94C'), 0, -0.07, 0.04), at(box(0.36, 0.2, 0.02, '#F2C94C'), 0, -0.07, -0.04), at(box(0.38, 0.03, 0.1, '#F2C94C'), 0, 0.03, 0)); j.position.set(0.15, 0.86, 0); body.add(j); }
    if (o.bib) { const b = canvasPlane(0.16, 0.12, (cc, W, Hh) => { cc.fillStyle = '#FFFFFF'; cc.fillRect(0, 0, W, Hh); cc.fillStyle = '#1C1C20'; cc.font = `900 ${Hh * 0.7}px Arial`; cc.textAlign = 'center'; cc.textBaseline = 'middle'; cc.fillText(String(o.bib), W / 2, Hh * 0.55); }, { res: 128 });
      b.position.set(0.0, 0.62, 0.045); body.add(b); const b2 = b.clone(); b2.position.z = -0.045; b2.rotation.y = PI; body.add(b2); }
    if (o.shades) { const sh = grp(at(box(0.012, 0.045, 0.06, '#1C1C20'), 0, 0, 0.065), at(box(0.012, 0.045, 0.06, '#1C1C20'), 0, 0, -0.065), at(box(0.01, 0.012, 0.07, '#1C1C20'), 0, 0.01, 0)); sh.position.set(0.53, 0.99, 0); body.add(sh); }
    const g = grp(body), R = rng(o.seed || 7), blink = R() * 3;
    g.userData.update = t => { const v = o.speed ?? 0, a = -t * v / 0.33; wheels.forEach(w => { w.rotation.z = a; }); crank.rotation.z = a * 0.45;
      body.position.y = 0.012 * Math.abs(Math.sin(t * 5)) * (v > 0 ? 1 : 0.3); body.rotation.x = 0.04 * Math.sin(t * 1.7) * (v > 0 ? 1 : 0.4);
      const lk = o.look || [0, 0]; pupils.forEach(pu => { pu.position.x = lk[1] * 0.02; pu.position.y = 0.012 * Math.sin(t * 0.9) + lk[0] * 0.02; });
      const bl = ((t + blink) % 3.1) < 0.12 ? 1 : 0; lids.forEach(l => { l.scale.y = 0.01 + bl * 0.99; }); };
    g.userData.update(0); return g;
  },
  winnersPodium(o) { // the three-step podium with 1 2 3 (centre step tallest), white with blue numbers
    const g = grp(); [[0, 0.6, '1'], [-0.62, 0.42, '2'], [0.62, 0.28, '3']].forEach(([x, h, n]) => { g.add(at(box(0.6, h, 0.6, '#F4F4F0', { pivot: 'bottom', outline: 0.006 }), x, 0, 0));
      const l = canvasPlane(0.3, 0.22, (c, W, H) => { c.fillStyle = '#F4F4F0'; c.fillRect(0, 0, W, H); c.fillStyle = '#2F62B5'; c.font = `900 ${H * 0.8}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(n, W / 2, H * 0.55); }, { res: 128 }); l.position.set(x, h * 0.5, 0.302); g.add(l); });
    return g;
  },
  oilCan(o) { // a small oil can with a long spout; drops fall from the tip from o.dripAt
    const g = grp(at(cyl(0.06, 0.07, 0.12, '#C8322A', 12, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(cyl(0.035, 0.06, 0.04, '#9AA0A6', 12, { pivot: 'bottom' }), 0, 0.12, 0), rod([0, 0.15, 0], [0.18, 0.3, 0], 0.008, '#9AA0A6'));
    const drops = [0, 1, 2].map(() => { const d = sphere(0.012, '#3A2A10', 0, { noGrain: true }); d.scale.y = 1.4; g.add(d); return d; });
    g.userData.update = t => { drops.forEach((d, i) => { const u = o.dripAt == null || t < o.dripAt ? -1 : ((t - o.dripAt) * 1.6 + i / 3) % 1; d.visible = u >= 0; d.position.set(0.18, 0.3 - u * 0.35, 0); }); };
    g.userData.update(0); return g;
  },
  innerTube(o) { return grp(at(torus(o.r || 0.25, 0.03, '#1C1C20', 6, 22), 0, 0, 0)); },
  regionFlag(o) { // a full-size flag on a pole, drawn: o.kind 'bzh' (Brittany), 'sard' (Sardinia), 'it', 'fr'; ripples
    const g = grp(at(cyl(0.015, 0.015, 1.6, '#9AA0A6', 5, { pivot: 'bottom' }), 0, 0, 0)), f = canvasPlane(0.6, 0.4, flagDraw(o.kind || 'bzh'), { res: 512 });
    f.position.set(0.31, 1.38, 0); g.add(f); g.userData.update = t => { f.rotation.y = 0.14 * Math.sin(t * 2.6 + (o.seed || 0)); }; return g;
  },
  disabledSpot(o) { // a disabled parking bay painted on the ground: blue rectangle, white border, white wheelchair pictogram (upright seen from +Z);
    // o.sign: the blue wheelchair sign on a pole at the kerb side (+Z), facing +Z
    const w = o.w || 5.0, d = o.d || 2.6, c = canvasPlane(w, d, (g, W, H) => {
      g.fillStyle = o.color || '#2F62B5'; g.fillRect(0, 0, W, H); g.strokeStyle = '#F4F4F0'; g.lineWidth = H * 0.05; g.strokeRect(H * 0.04, H * 0.04, W - H * 0.08, H - H * 0.08); wheelchair(g, W / 2, H / 2, Math.min(H * 0.7, W * 0.72));
    }, { res: 512 });
    c.rotation.x = -PI / 2; c.position.y = 0.012; c.receiveShadow = true; const gr = grp(c);
    if (o.sign) { const pole = at(cyl(0.03, 0.03, 2.0, '#9AA0A6', 6, { pivot: 'bottom' }), w * 0.32, 0, d / 2 + 0.45), pan = canvasPlane(0.5, 0.5, (g, W, H) => { g.fillStyle = '#2F62B5'; g.fillRect(0, 0, W, H); g.strokeStyle = '#F4F4F0'; g.lineWidth = W * 0.04; g.strokeRect(W * 0.05, H * 0.05, W * 0.9, H * 0.9); wheelchair(g, W / 2, H / 2, W * 0.66); }, { res: 256 });
      pan.position.set(w * 0.32, 1.95, d / 2 + 0.48); gr.add(pole, pan, at(box(0.54, 0.54, 0.02, '#D9DCDF'), w * 0.32, 1.95, d / 2 + 0.465)); }
    return gr;
  },
  sandGrain(o) { // ONE real grain of sand, not a cloud: faceted golden quartz pebble with glints; o.seed, o.color, o.flag 'bzh'|'sard'|'it'|'fr', o.eyes, o.popAt
    const g = grp(), body = new THREE.Mesh(grainGeo(0.05, o.seed || 3, 1), mat(o.color || '#E3C27A', { noGrain: true })); body.castShadow = body.receiveShadow = true; g.add(body);
    const R = rng((o.seed || 3) + 17), gl = [];
    for (let i = 0; i < 3; i++) { const sp = new THREE.Mesh(new THREE.OctahedronGeometry(0.006, 0), new THREE.MeshBasicMaterial({ color: '#FFFDF2' }));
      const a = R() * TAU, y = 0.02 + R() * 0.03; sp.position.set(Math.cos(a) * 0.045, y, Math.abs(Math.sin(a)) * 0.04 + 0.01); sp.userData.ph = R(); g.add(sp); gl.push(sp); }
    if (o.eyes) for (const sx of [-1, 1]) { const e = sphere(0.0055, '#17171B', 0, { noGrain: true }); e.position.set(sx * 0.014, 0.032, 0.048); g.add(e); }
    let fl = null; if (o.flag) { fl = miniFlag(o.flag, o.flagW || 0.08); fl.position.set(0.035, 0.02, -0.01); g.add(fl); }
    const rate = o.glint ?? 0.9;
    g.userData.update = t => { gl.forEach(sp => { const f = ((t * rate + sp.userData.ph) % 1); sp.scale.setScalar(Math.max(0.001, 1 - Math.abs(f - 0.5) * 14)); sp.rotation.y = t * 3; });
      if (fl) fl.userData.cloth.rotation.y = 0.18 * Math.sin(t * 5 + 1);
      if (o.popAt != null) { const k = pop(t, o.popAt, 0.3); g.scale.setScalar(k); } };
    g.userData.update(0); return g;
  },
  sandTray(o) { // a steel evidence tray holding grains in groups: o.groups [[n, x, z, color?, flag?]], o.w/o.d, o.countUp [t0, t1] pops them in one by one, o.label
    const w = o.w || 0.6, d = o.d || 0.4, g = grp(); if (!o.noTray) { g.add(at(box(w, 0.012, d, '#B9C0C6', { noGrain: true }), 0, 0.006, 0));
    for (const [x, z, bw, bd] of [[0, d / 2, w, 0.012], [0, -d / 2, w, 0.012], [w / 2, 0, 0.012, d], [-w / 2, 0, 0.012, d]]) g.add(at(box(bw, 0.03, bd, '#A3ABB2', { noGrain: true }), x, 0.015, z)); }
    const R = rng(o.seed || 5), all = [], flags = [], N = (o.groups || [[40]]).reduce((a, q) => a + q[0], 0), pile = 0.014 * Math.sqrt(N) + 0.008;
    for (const [n, gx, gz, col, flag] of (o.groups || [[40, 0, 0]])) {
      const rad = 0.014 * Math.sqrt(n) + 0.008, geos = [0, 1, 2, 3].map(i => grainGeo(0.011, 40 + i * 7, 0));
      for (let i = 0; i < n; i++) { const a = R() * TAU, r = rad * Math.sqrt(R()), m = new THREE.Mesh(geos[i % 4], mat(col || SAND[i % 4], { noGrain: true }));
        m.position.set(gx + Math.cos(a) * r, o.noTray ? 0 : 0.012, gz + Math.sin(a) * r); m.rotation.y = R() * TAU; m.castShadow = true; g.add(m); all.push(m);
        const a2 = R() * TAU, r2 = pile * Math.sqrt(R()); m.userData.end = m.position.clone(); m.userData.start = new THREE.Vector3(Math.cos(a2) * r2, m.position.y, Math.sin(a2) * r2); m.userData.lag = R(); }
      if (flag) { const f = miniFlag(flag, o.flagW || 0.07); f.position.set(gx + rad * 0.6, 0.012, gz - rad * 0.4); g.add(f); flags.push(f); }
    }
    if (o.label) { const l = sign(o.label, w * 0.7, 0.05, '#F4F1E8', '#1E2A33'); l.position.set(0, 0.016, d / 2 + 0.008); g.add(l); }
    const [c0, c1] = o.countUp || [null, null], order = all.map((m, i) => i).sort((a, b) => all[a].position.x - all[b].position.x);
    const [s0, s1] = o.sortAt || [null, null];   // sortAt [t0, t1]: the grains start mixed in one pile and slide to their groups (staggered), flags pop at t1
    g.userData.update = t => { if (c0 != null) order.forEach((idx, j) => { const tj = c0 + (c1 - c0) * j / Math.max(1, all.length - 1); all[idx].scale.setScalar(pop(t, tj, 0.12)); });
      if (s0 != null) all.forEach(m => { const a = s0 + m.userData.lag * (s1 - s0) * 0.5, k = ease.inOut(clamp01((t - a) / ((s1 - s0) * 0.5))); m.position.lerpVectors(m.userData.start, m.userData.end, k); });
      flags.forEach((f, i) => { f.userData.cloth.rotation.y = 0.15 * Math.sin(t * 4 + i); if (s0 != null) f.scale.setScalar(pop(t, s1, 0.3)); }); };
    g.userData.update(0); return g;
  },
  starsStripes(o) { // a stars-and-stripes flag on a pole (drawn), rippling a little
    const g = grp(at(cyl(0.015, 0.015, 1.6, '#9AA0A6', 5, { pivot: 'bottom' }), 0, 0, 0));
    const f = canvasPlane(0.9, 0.5, (c, W, H) => { for (let i = 0; i < 13; i++) { c.fillStyle = i % 2 ? '#F4F4F0' : '#B22234'; c.fillRect(0, i * H / 13, W, H / 13 + 1); }
      c.fillStyle = '#3C3B6E'; c.fillRect(0, 0, W * 0.42, H * 7 / 13); c.fillStyle = '#F4F4F0'; for (let r = 0; r < 5; r++) for (let q = 0; q < 6; q++) c.fillRect(W * (0.03 + q * 0.065), H * (0.04 + r * 0.1), W * 0.022, H * 0.04); }, { res: 512 });
    f.position.set(0.46, 1.33, 0); g.add(f); g.userData.update = t => { f.rotation.y = 0.12 * Math.sin(t * 2.5); }; return g;
  },
  bigShoe(o) { // a man's derby, open at the top, laces; whatever grows inside goes in at y 0.12
    const c = o.color || '#3A2A22', g = grp();
    g.add(at(box(0.34, 0.13, 0.13, c, { outline: 0.006 }), 0.02, 0.065, 0), at(box(0.12, 0.2, 0.13, c, { outline: 0.006 }), -0.12, 0.1, 0));
    g.add(at(box(0.36, 0.025, 0.14, '#1C1512'), 0.02, 0.012, 0));
    for (let i = 0; i < 3; i++) g.add(at(box(0.012, 0.012, 0.1, '#F4F1E8'), 0.0 + i * 0.04, 0.135, 0));
    return g;
  },
  growIsland(o) { // a grain that grows: sand grain -> pebble -> rock -> island with a palm, at the times in o.stages [[t, 0..3]]
    const g = grp(), sand = sphere(0.012, '#E7D7A8', 1), peb = sphere(0.035, '#9AA0A6', 0), rock = sphere(0.09, '#8A9096', 0);
    const isl = grp(at(sphere(1, '#E7D7A8', 1), 0, -0.05, 0), at(palm(0.9), 0.1, 0.05, 0)); isl.children[0].scale.set(0.42, 0.14, 0.3); isl.scale.setScalar(0.5);
    const water = at(cyl(0.34, 0.34, 0.02, '#3FB7D9', 16), 0, 0.0, 0); isl.add(water);
    [sand, peb, rock, isl].forEach(m => g.add(m)); peb.scale.set(1.3, 0.8, 1); rock.scale.set(1.4, 0.8, 1.1);
    g.userData.update = t => { let st = 0, a0 = 0; for (const [a, s] of (o.stages || [])) if (t >= a) { st = s; a0 = a; }
      [sand, peb, rock, isl].forEach((m, i) => { m.visible = i === st; if (i === st) { const k = Math.max(0.05, ease.outBack(clamp01((t - a0) / 0.35))); m.scale.setScalar(i === 3 ? 0.5 * k : k * (i === 1 ? 1.3 : i === 2 ? 1.4 : 1)); } }); };
    g.userData.update(0); return g;
  },
  shopFront(o) { // small lunar/street shop: box with a door, a window and a sign (o.text); pops up from o.popAt
    const W = o.w || 2.4, H = o.h || 2.2, g = grp(), body = grp(); g.add(body);
    body.add(at(box(W, H, 2, o.color || '#D9DCD6', { outline: 0.01 }), 0, H / 2, -1), at(box(0.6, 1.1, 0.04, '#3A4652'), -W * 0.25, 0.55, 0.01), at(box(0.8, 0.6, 0.04, '#7FC2EE'), W * 0.2, 1.1, 0.01));
    const s = sign(o.text || 'BANQUE', W * 0.9, 0.42, o.signBg || '#203447', '#FFFFFF'); s.position.set(0, H + 0.25, 0.02); body.add(s);
    g.userData.update = t => { if (o.popAt == null) return; const k = pop(t, o.popAt, 0.35); body.visible = k > 0.001; body.scale.setScalar(Math.max(0.001, k)); };
    g.userData.update(0); return g;
  },
  giantFir(o) { // a Christmas tree of any height: stacked cones, baubles, a blinking garland, a star; o.windows lights up flats in the boughs
    const H = o.h || 2.4, g = grp(), r = rng(o.seed || 5), n = Math.max(4, Math.round(H / 0.6)), lights = [];
    g.add(at(cyl(0.08 * H / 2.4, 0.1 * H / 2.4, H * 0.12, '#6B4A2E', 6, { pivot: 'bottom' }), 0, 0, 0));
    for (let i = 0; i < n; i++) { const u = i / n, rr = (1 - u) * 0.55 * H / 2.4 * 1.6 + 0.08, hh = H / n * 1.6; const c = new THREE.Mesh(new THREE.ConeGeometry(rr, hh, 8), mat(i % 2 ? '#2F7F4F' : '#3E9B5F')); c.position.y = H * 0.1 + u * H * 0.85 + hh / 2; g.add(c);
      for (let b = 0; b < 4 + Math.round(rr * 4); b++) { const a = r() * TAU, y = c.position.y - hh * 0.35 + r() * hh * 0.3; const m = sphere(0.035 * Math.max(1, H / 6), ['#E0413A', '#F2C230', '#2F62B5', '#F28CA0'][b % 4], 1); m.position.set(Math.cos(a) * rr * 0.75, y, Math.sin(a) * rr * 0.75); g.add(m);
        const L = new THREE.Mesh(new THREE.SphereGeometry(0.02 * Math.max(1, H / 6), 6, 4), new THREE.MeshBasicMaterial({ color: '#FFF27A' })); L.position.set(Math.cos(a + 1) * rr * 0.8, y + hh * 0.1, Math.sin(a + 1) * rr * 0.8); lights.push(L); g.add(L);
        if (o.windows && r() < 0.5) { const w = new THREE.Mesh(new THREE.BoxGeometry(0.18 * H / 12, 0.14 * H / 12, 0.02), new THREE.MeshBasicMaterial({ color: '#FFE9A8' })); w.position.set(Math.cos(a + 2) * rr * 0.9, y, Math.sin(a + 2) * rr * 0.9); w.lookAt(0, y, 0); w.rotateY(PI); g.add(w); } } }
    const star = new THREE.Mesh(new THREE.OctahedronGeometry(0.12 * H / 2.4, 0), new THREE.MeshBasicMaterial({ color: '#FFD84A' })); star.position.y = H * 1.0; g.add(star);
    const needles = []; if (o.shed) for (let i = 0; i < 60; i++) { const m = new THREE.Mesh(new THREE.BoxGeometry(0.01 * H / 2.4, 0.06 * H / 2.4, 0.01), mat('#3E9B5F')); needles.push({ m, a: r() * TAU, d: r() * 0.5 * H / 2.4, y0: r() * H, ph: r() }); g.add(m); }
    g.userData.update = t => { lights.forEach((L, i) => { L.visible = ((Math.floor(t * 3) + i) % 3) !== 0; }); star.rotation.y = t * 1.2; star.scale.setScalar(1 + 0.08 * Math.sin(t * 6));
      g.rotation.z = (o.sway || 0) * Math.sin(t * 1.3); const s0 = keyAt(o.shed, t);
      needles.forEach(nd => { if (s0 == null) { nd.m.visible = false; return; } const u = (t - s0) * 0.8 + nd.ph; const y = nd.y0 - ((u * 3) % (nd.y0 + 0.1)); nd.m.visible = true; nd.m.position.set(Math.cos(nd.a) * (nd.d + u * 0.2), Math.max(0.01, y), Math.sin(nd.a) * (nd.d + u * 0.2)); nd.m.rotation.z = u * 5; }); };
    g.userData.update(0); return g;
  },
  tortoise(o) { // a tortoise in a lawyer's white collar: domed shell, head that bobs, stubby legs
    const g = grp(), sh = sphere(0.3, o.color || '#6E8A4E', 1); sh.scale.set(1.2, 0.7, 1); sh.position.y = 0.22; g.add(sh);
    g.add(at(box(0.62, 0.05, 0.5, '#8FA86A'), 0, 0.1, 0));
    const head = grp(at(sphere(0.1, '#9DB57A', 1), 0, 0, 0)); [-1, 1].forEach(z => head.add(at(box(0.03, 0.03, 0.01, '#1C252A'), 0.07, 0.03, z * 0.06)));
    head.add(at(box(0.06, 0.08, 0.16, '#F4F4F0'), -0.02, -0.08, 0)); head.position.set(0.42, 0.25, 0); g.add(head);
    [[0.22, 0.2], [0.22, -0.2], [-0.22, 0.2], [-0.22, -0.2]].forEach(([x, z]) => g.add(at(cyl(0.05, 0.06, 0.14, '#9DB57A', 6, { pivot: 'bottom' }), x, 0, z)));
    g.userData.update = t => { head.position.x = 0.42 + 0.03 * Math.sin(t * 2.2); head.rotation.z = 0.08 * Math.sin(t * 1.7); };
    g.userData.update(0); return g;
  },
  motorbike(o) { // a small red motorbike, wheels spinning with o.roll
    const g = grp(), wheels = []; [[0.5, 0], [-0.5, 0]].forEach(([x]) => { const w = at(cyl(0.22, 0.22, 0.08, '#1C1E22', 12), x, 0.22, 0, PI / 2, 0, 0); wheels.push(w); g.add(w); });
    g.add(at(box(0.8, 0.22, 0.2, o.color || '#C8322A', { outline: 0.008 }), 0, 0.5, 0), at(box(0.3, 0.12, 0.22, '#2B2E33'), -0.15, 0.66, 0), at(box(0.06, 0.4, 0.06, '#9AA0A6'), 0.42, 0.62, 0), at(box(0.04, 0.04, 0.45, '#2B2E33'), 0.42, 0.82, 0));
    g.userData.update = t => wheels.forEach(w => { w.rotation.y = (o.roll || 0) * t; });
    g.userData.update(0); return g;
  },
  slug(o) { // a snail without its shell (or a slug): soft body, eye stalks, wiggle
    const g = grp(), b = sphere(0.1, o.color || '#C9A27A', 1); b.scale.set(2.2, 0.55, 0.9); b.position.y = 0.05; g.add(b);
    const st = [-1, 1].map(z => { const s = grp(at(cyl(0.008, 0.01, 0.12, o.color || '#C9A27A', 5, { pivot: 'bottom' }), 0, 0, 0), at(sphere(0.018, '#1C252A', 0), 0, 0.12, 0)); s.position.set(0.18, 0.08, z * 0.03); g.add(s); return s; });
    g.userData.update = t => { b.scale.x = 2.2 + 0.15 * Math.sin(t * 4); st.forEach((s, i) => { s.rotation.z = -0.3 + 0.15 * Math.sin(t * 3 + i); }); };
    g.userData.update(0); return g;
  },
  fireTruck(o) { // red fire engine with a ladder; o.spray [[t, true]] shoots a water jet from the hose
    const g = grp(); g.add(at(box(4.4, 1.6, 1.8, '#C8322A', { outline: 0.015 }), 0, 1.2, 0), at(box(1.3, 1.1, 1.75, '#C8322A'), 2.5, 0.95, 0), at(box(0.5, 0.6, 1.6, '#7FC2EE'), 3.0, 1.25, 0));
    [[-1.4, 0.95], [-1.4, -0.95], [1.9, 0.95], [1.9, -0.95]].forEach(([x, z]) => g.add(at(cyl(0.4, 0.4, 0.3, '#1C1E22', 10), x, 0.4, z, PI / 2, 0, 0)));
    g.add(at(box(3.6, 0.12, 0.5, '#B9BDBF'), -0.3, 2.1, 0));
    const jet = grp(); for (let i = 0; i < 48; i++) { const d = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.26, 0.26), new THREE.MeshBasicMaterial({ color: i % 3 === 2 ? '#F2FAFF' : '#3B8FE0', transparent: true, opacity: 0.92 })); jet.add(d); } jet.position.set(-2.1, 1.9, 0); g.add(jet);   // saturated blue + white foam: reads against sky and clouds
    const RE = o.reach || 9, LI = o.lift || 2.4;   // jet length along local -x and initial rise
    g.userData.update = t => { const a0 = keyAt(o.spray, t); jet.visible = a0 != null; if (a0 == null) return; jet.children.forEach((d, i) => { const k = Math.min(((t - a0) * 2 + i / 48) % 1, (t - a0) * 1.6), x = -k * RE, y = k * LI - k * k * (LI + 1.8); d.position.set(x, y, 0.15 * Math.sin(i)); d.rotation.z = Math.atan2(LI - 2 * (LI + 1.8) * k, -RE); }); };
    g.userData.update(0); return g;
  },
  rainbow(o) { // a rainbow arc of radius o.r, drawing on from o.t0
    const R = o.r || 6, g = grp(), cols = ['#E0413A', '#F28C30', '#F2C230', '#5BB06E', '#2F62B5', '#7A4FB5'], arcs = [];
    cols.forEach((c, i) => { const m = new THREE.Mesh(new THREE.TorusGeometry(R - i * 0.32, 0.16, 6, 48, PI), new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: 0.9 })); g.add(m); arcs.push(m); });
    g.userData.update = t => { const k = o.t0 == null ? 1 : clamp01((t - o.t0) / 0.6); arcs.forEach(m => { m.scale.setScalar(Math.max(0.001, ease.outBack(k))); }); };
    g.userData.update(0); return g;
  },
  train(o) { // a high-speed train (nose + o.cars carriages), moving along its local +X by o.speed m/s from o.t0
    const g = grp(), body = grp(); g.add(body); const n = o.cars || 3, c = o.color || '#F4F4F0', stripe = o.stripe || '#2F62B5';
    const nose = box(4, 1.6, 1.4, c, { taper: { x: 0.35, z: 1 }, taperAxis: 'x', outline: 0.01 }); nose.position.set(2, 1.0, 0); body.add(nose);
    for (let i = 0; i < n; i++) { body.add(at(box(5.6, 1.7, 1.45, c, { outline: 0.01 }), -3 - i * 5.8, 1.05, 0), at(box(5.6, 0.2, 1.47, stripe), -3 - i * 5.8, 0.6, 0));
      for (let w = 0; w < 5; w++) body.add(at(box(0.6, 0.4, 1.48, '#3A4652'), -5.2 + w * 1.1 - i * 5.8, 1.35, 0)); }
    g.userData.update = t => { body.position.x = Math.max(0, t - (o.t0 || 0)) * (o.speed || 0); };
    g.userData.update(0); return g;
  },
  medal(o) { // a gold medal on a tricolour ribbon (hangs from y 0)
    const g = grp(); ['#2F62B5', '#F4F4F0', '#E0413A'].forEach((c, i) => g.add(at(box(0.025, 0.12, 0.004, c), -0.025 + i * 0.025, -0.06, 0)));
    const d = at(cyl(0.045, 0.045, 0.01, '#E8B830', 16), 0, -0.15, 0, PI / 2, 0, 0); g.add(d); g.userData.update = t => { d.rotation.z = 0.3 * Math.sin(t * 2); }; return g;
  },
  bigWatch(o) { // a wrist watch the size of a hand (o.time "HH:MM" digital)
    const g = grp(at(box(0.08, 0.3, 0.012, '#2B2E33'), 0, 0, 0), at(box(0.12, 0.1, 0.03, '#C9CDD2', { outline: 0.004 }), 0, 0, 0.01));
    const f = canvasPlane(0.1, 0.08, (c, W, H) => { c.fillStyle = '#1C2733'; c.fillRect(0, 0, W, H); c.fillStyle = '#9FF0FF'; c.font = `900 ${H * 0.5}px monospace`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.time || '10:00', W / 2, H / 2); }, { res: 256, emissive: 0.8 });
    f.position.z = 0.026; g.add(f); return g;
  },
  splitMap(o) { // France as one shape split in two halves of different colours by a dashed line (two time zones)
    const K = o.k || 10, g = grp(), pr = ([lon, lat]) => [(lon - 3) * K * 0.68, -(lat - 47.5) * K];
    const FR = [[2.55, 51.08], [1.6, 50.9], [1.6, 50.2], [0.1, 49.5], [-1.2, 49.4], [-1.9, 49.7], [-1.6, 48.65], [-3.5, 48.8], [-4.8, 48.4], [-4.7, 47.9], [-2.2, 47.2], [-1.2, 46.2], [-1.2, 44.6], [-1.8, 43.35],
      [-0.6, 42.9], [1.7, 42.5], [3.1, 42.45], [3.2, 43.0], [4.8, 43.4], [6.2, 43.1], [7.5, 43.8], [6.8, 44.4], [7.0, 45.9], [6.1, 46.4], [7.6, 47.6], [8.2, 49.0], [6.4, 49.45], [5.9, 49.5], [4.85, 49.8], [4.8, 50.15], [4.2, 49.95], [3.6, 50.4], [2.9, 50.7]];
    const clip = (pts, west) => pts.map(p => [west ? Math.min(p[0], 2.5) : Math.max(p[0], 2.5), p[1]]);
    [[true, o.west || '#F2C94C'], [false, o.east || '#8CC768']].forEach(([w, c]) => { const s = new THREE.Shape(); clip(FR, w).map(pr).forEach(([x, z], i) => i ? s.lineTo(x, -z) : s.moveTo(x, -z)); const m = mesh(new THREE.ShapeGeometry(s), mat(c)); m.rotation.x = -PI / 2; m.position.y = 0.03; g.add(m); });
    for (let i = 0; i < 16; i++) { const z0 = pr([2.5, 51 - i * 0.55])[1]; g.add(at(box(0.08 * K, 0.04 * K, 0.25 * K, '#FFFFFF'), pr([2.5, 0])[0], 0.06, z0)); }
    const sea = mesh(new THREE.PlaneGeometry(60 * K, 60 * K).rotateX(-PI / 2), mat(o.sea || '#5AA3DB')); sea.position.y = 0; g.add(sea);
    return g;
  },
};
