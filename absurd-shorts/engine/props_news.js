// Props for the seven "faits divers" stories (sable, lune, sapin, escargot, grève, colis, heure), tornado-replica style.
// Conventions as in props.js; small loops of motion built in (pure functions of t).
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, sphere, rng, ease, clamp01 } from './style.js';
import { grp, at, mesh, canvasPlane, inst, rod, torus, label } from './props.js';

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
    for (const [y0, y1, r0, r1] of [[0.33 + 0.07, 0.355 + 0.045, 0, -0.52], [0.33 - 0.07, 0.355 - 0.045, 0, -0.52]]) {   // chain: two runs of dark links
      const n = 13, ang = Math.atan2(y1 - y0, r1 - r0); for (let i = 0; i <= n; i++) { const u = i / n, lk = box(0.034, 0.014, 0.016, i % 2 ? '#2A2C30' : '#4A4E54'); lk.position.set(r0 + (r1 - r0) * u, y0 + (y1 - y0) * u, 0.05); lk.rotation.z = ang; body.add(lk); } }
    body.add(at(cyl(0.045, 0.045, 0.018, '#5A5E62', 10), -0.52, 0.355, 0.05, PI / 2));   // rear sprocket
    const er = o.eyeR || 0.068, eyes = grp(), lids = [], pupils = []; [-1, 1].forEach(sd => {   // two googly eyes side by side across the stem, looking forward (+x)
      const ball = sphere(er, '#FFFFFF', 1, { noGrain: true }); ball.scale.z = 0.82; const pu = sphere(er * 0.46, '#1C1C20', 0, { noGrain: true }); pu.position.set(0, 0, er * 0.7); ball.add(pu); pupils.push(pu);
      const lid = mesh(new THREE.SphereGeometry(er * 1.06, 12, 6, 0, TAU, 0, PI / 2), mat(c)); lid.rotation.x = PI / 2; lid.scale.y = 0.01; ball.add(lid); lids.push(lid);
      ball.rotation.y = PI / 2 - sd * 0.14; ball.position.set(0, 0, sd * er * 1.12); eyes.add(ball); });
    eyes.position.set(0.47, 1.0, 0); body.add(eyes);
    if (o.jersey) { const j = grp(), tee = canvasPlane(0.56, 0.44, (cc, W, Hh) => { cc.fillStyle = '#F2C94C'; cc.strokeStyle = '#B88A1E'; cc.lineWidth = W * 0.018;   // the maillot jaune: a T-shirt shape on each side
        cc.beginPath(); [[0.3, 0.04], [0.42, 0.04], [0.5, 0.14], [0.58, 0.04], [0.7, 0.04], [0.98, 0.26], [0.86, 0.42], [0.76, 0.34], [0.76, 0.97], [0.24, 0.97], [0.24, 0.34], [0.14, 0.42], [0.02, 0.26]].forEach(([x, y], i) => i ? cc.lineTo(x * W, y * Hh) : cc.moveTo(x * W, y * Hh));
        cc.closePath(); cc.fill(); cc.stroke(); cc.fillStyle = '#B88A1E'; cc.fillRect(W * 0.24, Hh * 0.86, W * 0.52, Hh * 0.05); cc.beginPath(); cc.moveTo(W * 0.42, Hh * 0.04); cc.lineTo(W * 0.5, Hh * 0.2); cc.lineTo(W * 0.58, Hh * 0.04); cc.stroke(); }, { res: 256, transparent: true });
      for (const sz of [-1, 1]) { const t = tee.clone(); t.position.set(0.15, 0.68, sz * 0.05); if (sz < 0) t.rotation.y = PI; j.add(t); }
      j.add(at(box(0.3, 0.025, 0.11, '#F2C94C'), 0.15, 0.88, 0), at(torus(0.045, 0.014, '#B88A1E', 6, 14), 0.42, 0.985, 0, PI / 2, 0, 0)); body.add(j); }
    if (o.bib) { const b = canvasPlane(0.16, 0.12, (cc, W, Hh) => { cc.fillStyle = '#FFFFFF'; cc.fillRect(0, 0, W, Hh); cc.fillStyle = '#1C1C20'; cc.font = `900 ${Hh * 0.7}px Arial`; cc.textAlign = 'center'; cc.textBaseline = 'middle'; cc.fillText(String(o.bib), W / 2, Hh * 0.55); }, { res: 128 });
      b.position.set(0.0, 0.62, 0.045); body.add(b); const b2 = b.clone(); b2.position.z = -0.045; b2.rotation.y = PI; body.add(b2); }
    if (o.shades) { const ez = er * 1.12, lw = er * 1.85, lh = er * 1.5, sh = grp(at(box(0.016, lh, lw, '#141418'), 0, 0, ez), at(box(0.016, lh, lw, '#141418'), 0, 0, -ez), at(box(0.014, 0.018, ez * 2 - lw + 0.03, '#141418'), 0, lh * 0.3, 0),   // star sunglasses
        at(box(0.004, lh * 0.32, lw * 0.28, '#FFFFFF', { noGrain: true }), 0.01, lh * 0.2, ez + lw * 0.22), at(box(0.004, lh * 0.32, lw * 0.28, '#FFFFFF', { noGrain: true }), 0.01, lh * 0.2, -ez + lw * 0.22));
      sh.position.set(0.47 + er * 0.82 + 0.014, 1.0, 0); body.add(sh); }
    const g = grp(body), R = rng(o.seed || 7), blink = R() * 3;
    const dist = t => { const v = o.speed ?? 0; if (o.goAt == null) return v * t; const u = t - o.goAt; return u <= 0 ? 0 : u < 0.3 ? v * u * u / 0.6 : v * (u - 0.15); };
    g.userData.update = t => { const v = o.goAt != null && t < o.goAt ? 0 : (o.speed ?? 0), a = -dist(t) / 0.33; wheels.forEach(w => { w.rotation.z = a; }); crank.rotation.z = a * 0.45;
      body.position.y = 0.012 * Math.abs(Math.sin(t * 5)) * (v > 0 ? 1 : 0.3); body.rotation.x = 0.04 * Math.sin(t * 1.7) * (v > 0 ? 1 : 0.4);
      const K = o.lookKeys; let lk = o.look || [0, 0];   // o.lookKeys: [[t, up, side], ...] eases the gaze between keys
      if (K) { lk = K[K.length - 1].slice(1); if (t <= K[0][0]) lk = K[0].slice(1); else for (let i = 1; i < K.length; i++) if (t < K[i][0]) { let u = (t - K[i - 1][0]) / (K[i][0] - K[i - 1][0]); u = u * u * (3 - 2 * u); lk = [K[i - 1][1] + (K[i][1] - K[i - 1][1]) * u, K[i - 1][2] + (K[i][2] - K[i - 1][2]) * u]; break; } }
      pupils.forEach(pu => { pu.position.x = lk[1] * er * 0.38; pu.position.y = er * 0.15 * Math.sin(t * 0.9) + lk[0] * er * 0.38; });
      const bl = ((t + blink) % 3.1) < 0.12 ? 1 : 0; lids.forEach(l => { l.scale.y = 0.01 + bl * 0.99; }); pupils.forEach(pu => { pu.visible = !bl; }); };
    g.userData.update(0); return g;
  },
  winnersPodium(o) { // the three-step podium with 1 2 3 (centre step tallest), white with blue numbers; o.w step width, o.hs height scale
    const w = o.w || 0.6, hs = o.hs || 1, g = grp(); [[0, 0.6, '1'], [-1.03 * w, 0.42, '2'], [1.03 * w, 0.28, '3']].forEach(([x, h0, n]) => { const h = h0 * hs; g.add(at(box(w, h, w, '#F4F4F0', { pivot: 'bottom', outline: 0.006 }), x, 0, 0));
      const l = canvasPlane(w * 0.5, w * 0.37, (c, W, H) => { c.fillStyle = '#F4F4F0'; c.fillRect(0, 0, W, H); c.fillStyle = '#2F62B5'; c.font = `900 ${H * 0.8}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(n, W / 2, H * 0.55); }, { res: 128 }); l.position.set(x, Math.min(h * 0.5, h - w * 0.25), w / 2 + 0.002); g.add(l); });
    return g;
  },
  oilCan(o) { // a small oil can with a long spout; drops fall from the tip from o.dripAt. o.pour: the can tilted with the spout aiming down-forward, the drops fall straight down
    // (tip at userData.tip); o.color, o.drop (colour), o.dropR
    const g = grp(), can = grp(at(cyl(0.06, 0.07, 0.12, o.color || '#C8322A', 12, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(cyl(0.035, 0.06, 0.04, '#9AA0A6', 12, { pivot: 'bottom' }), 0, 0.12, 0));
    const tip = o.pour ? [0.24, 0.05, 0] : [0.18, 0.3, 0]; if (o.pour) { can.rotation.z = -0.5; can.position.set(-0.04, 0.02, 0); } g.add(can, rod(o.pour ? [0.07, 0.17, 0] : [0, 0.15, 0], tip, 0.008, '#9AA0A6'));
    const dr = o.dropR || 0.012, drops = [0, 1, 2].map(() => { const d = sphere(dr, o.drop || '#3A2A10', 0, { noGrain: true }); d.scale.y = 1.4; if (o.pour) d.add(at(sphere(dr * 0.35, '#FFF6D0', 0, { noGrain: true }), -dr * 0.35, dr * 0.35, dr * 0.6)); g.add(d); return d; });
    const fall = o.fall || 0.35;
    g.userData.update = t => { drops.forEach((d, i) => { const u = o.dripAt == null || t < o.dripAt ? -1 : ((t - o.dripAt) * 1.6 + i / 3) % 1; d.visible = u >= 0; d.position.set(tip[0], tip[1] - 0.01 - u * fall, 0); }); };
    g.userData.tip = tip; g.userData.update(0); return g;
  },
  innerTube(o) { return grp(at(torus(o.r || 0.25, 0.03, '#1C1C20', 6, 22), 0, 0, 0)); },
  petRock(o) { // "Le caillou": Gérard, a pet rock (about 0.4 m) with googly eyes that look around and blink; o.look / o.lookKeys [[t, up, side]], o.brows 'smug'|'angry',
    // o.cap 'grad' (mortarboard) | 'guard' (security cap), o.sash (tricolour mayor's sash), o.medal, o.eyes false (a plain stone: the statue), o.color, o.seed. Grow it with scale keys.
    const r = 0.2, col = o.color || '#9C9A94', g = grp(), geo = grainGeo(r, o.seed || 11, 1); if (o.sy) { geo.scale(1, o.sy, 1); geo.computeVertexNormals(); }
    const body = new THREE.Mesh(geo, mat(col, { noGrain: true })); body.castShadow = body.receiveShadow = true; g.add(body);
    body.geometry.computeBoundingBox(); const bb = body.geometry.boundingBox, H = bb.max.y, F = bb.max.z, Wd = bb.max.x;
    const spots = []; const R = rng((o.seed || 11) + 5); for (let i = 0; i < 7; i++) { const sp = mesh(new THREE.CircleGeometry(r * (0.06 + R() * 0.07), 6), mat(i % 2 ? '#86847E' : '#B2B0A9', { noGrain: true }));
      const a = R() * TAU, yy = H * (0.15 + R() * 0.55); sp.position.set(Math.cos(a) * Wd * 0.98, yy, Math.sin(a) * F * 0.98); sp.lookAt(sp.position.x * 2, yy, sp.position.z * 2); g.add(sp); spots.push(sp); }
    const lids = [], pupils = [], er = r * 0.34;
    if (o.eyes !== false) [-1, 1].forEach(sd => { const ball = sphere(er, '#FFFFFF', 1, { noGrain: true }); ball.scale.z = 0.8; const pu = sphere(er * 0.46, '#1C1C20', 0, { noGrain: true }); pu.position.set(0, 0, er * 0.7); ball.add(pu); pupils.push(pu);
      const lid = mesh(new THREE.SphereGeometry(er * 1.06, 12, 6, 0, TAU, 0, PI / 2), mat(col)); lid.rotation.x = PI / 2; lid.scale.y = 0.01; ball.add(lid); lids.push(lid);
      ball.rotation.y = sd * 0.16; ball.position.set(sd * er * 1.08, H * 0.62, F * 0.9); g.add(ball);
      if (o.brows) { const b = box(er * 1.3, er * 0.28, er * 0.3, '#3A3A3E'); b.position.set(sd * er * 1.08, H * 0.62 + er * 1.15, F * 0.95); b.rotation.z = (o.brows === 'angry' ? -1 : 1) * sd * 0.35; g.add(b); } });
    if (o.cap === 'grad') { const c = grp(at(box(r * 1.0, r * 0.28, r * 1.0, '#1C1C22'), 0, r * 0.12, 0), at(box(r * 1.7, r * 0.06, r * 1.7, '#1C1C22', { outline: 0.004 }), 0, r * 0.29, 0, 0, PI / 4, 0), rod([r * 0.6, r * 0.32, r * 0.6], [r * 0.72, -r * 0.1, r * 0.72], 0.006, '#E8B830'));
      c.position.y = H * 0.92; g.add(c); }
    if (o.cap === 'guard') { const c = grp(at(box(r * 1.15, r * 0.4, r * 1.1, '#2A3D66', { taper: 1.1, outline: 0.006 }), 0, r * 0.2, 0), at(box(r * 1.25, r * 0.06, r * 0.7, '#111318', { outline: 0.004 }), 0, r * 0.02, r * 0.78, 0.18, 0, 0),
        at(box(r * 1.2, r * 0.07, r * 1.15, '#C9CCD1'), 0, r * 0.05, 0), at(label('SÉCURITÉ', r * 1.05, r * 0.16, { bg: '#F2C94C', fg: '#1C1C20', wrap: false }), 0, r * 0.24, r * 0.56),
        at(cyl(r * 0.1, r * 0.1, 0.01, '#F2C94C', 8), 0, r * 0.36, r * 0.52, PI / 2)); c.position.y = H * 0.9; c.rotation.x = -0.12; g.add(c); }
    if (o.sash) { const sg = grp(); ['#2F62B5', '#F4F4F0', '#E0413A'].forEach((c, i) => sg.add(at(box(r * 0.14, H * 1.25, r * 0.03, c), (i - 1) * r * 0.14, 0, 0))); sg.rotation.z = -0.75; sg.position.set(0, H * 0.42, F * 0.99); g.add(sg); }
    if (o.medal) { const m = grp(rod([-r * 0.3, H * 0.42, F * 0.95], [0, H * 0.18, F + 0.01], 0.006, '#2F62B5'), rod([r * 0.3, H * 0.42, F * 0.95], [0, H * 0.18, F + 0.01], 0.006, '#E0413A'), at(cyl(r * 0.2, r * 0.2, 0.012, '#E8B830', 16), 0, H * 0.14, F + 0.02, PI / 2)); g.add(m); }
    const blink = rng(o.seed || 11)() * 3;
    g.userData.update = t => { const K = o.lookKeys; let lk = o.look || [0, 0];
      if (K) { lk = K[K.length - 1].slice(1); if (t <= K[0][0]) lk = K[0].slice(1); else for (let i = 1; i < K.length; i++) if (t < K[i][0]) { let u = (t - K[i - 1][0]) / (K[i][0] - K[i - 1][0]); u = u * u * (3 - 2 * u); lk = [K[i - 1][1] + (K[i][1] - K[i - 1][1]) * u, K[i - 1][2] + (K[i][2] - K[i - 1][2]) * u]; break; } }
      pupils.forEach(pu => { pu.position.x = lk[1] * er * 0.38; pu.position.y = er * 0.1 * Math.sin(t * 0.8) + lk[0] * er * 0.38; });
      const bl = ((t + blink) % 3.4) < 0.12 ? 1 : 0; lids.forEach(l => { l.scale.y = 0.01 + bl * 0.99; }); pupils.forEach(pu => { pu.visible = !bl; }); g.rotation.z = (o.wobble ?? 0) * Math.sin(t * 9); };
    g.userData.update(0); return g; },
  doghouse(o) { // a wooden dog kennel facing +z: plank walls, red gable roof, dark arched doorway (an actor at y 0 inside shows his head out); o.text plaque over the door
    const w = o.w || 1.1, d = o.d || 1.3, h = o.h || 0.85, c = o.color || '#C9955A', g = grp();
    g.add(at(box(w, h, 0.05, c, { pivot: 'bottom', outline: 0.006 }), 0, 0, -d / 2), at(box(0.05, h, d, c, { pivot: 'bottom', outline: 0.006 }), -w / 2, 0, 0), at(box(0.05, h, d, c, { pivot: 'bottom', outline: 0.006 }), w / 2, 0, 0));
    const ow = w * 0.56, oh = h * 0.8; g.add(at(box((w - ow) / 2, h, 0.05, c, { pivot: 'bottom', outline: 0.006 }), -(w + ow) / 4, 0, d / 2), at(box((w - ow) / 2, h, 0.05, c, { pivot: 'bottom', outline: 0.006 }), (w + ow) / 4, 0, d / 2), at(box(ow, h - oh, 0.05, c, { pivot: 'bottom' }), 0, oh, d / 2));
    for (let i = 1; i < 5; i++) for (const x of [-w / 2 - 0.028, w / 2 + 0.028]) g.add(at(box(0.004, 0.01, d, '#9C6E3E'), x, h * i / 5, 0));
    const tri = new THREE.Shape([new THREE.Vector2(-w / 2 - 0.02, 0), new THREE.Vector2(w / 2 + 0.02, 0), new THREE.Vector2(0, h * 0.55)]);
    for (const z of [-d / 2, d / 2]) { const gm = mesh(new THREE.ExtrudeGeometry(tri, { depth: 0.05, bevelEnabled: false }), mat(c)); gm.position.set(0, h, z - 0.025); g.add(gm); }
    const sl = Math.hypot(w / 2 + 0.12, h * 0.55) + 0.05, ang = Math.atan2(h * 0.55, w / 2 + 0.12);
    for (const sd of [-1, 1]) g.add(at(box(sl, 0.06, d + 0.24, o.roof || '#B5302A', { outline: 0.006 }), sd * (w / 4 + 0.03), h + h * 0.275 + 0.02, 0, 0, 0, -sd * ang));
    if (o.text) g.add(at(label(o.text, ow * 0.95, 0.12, { bg: '#F4EBD6', fg: '#3A2A1A', wrap: false }), 0, oh + (h - oh) / 2, d / 2 + 0.03));
    return g; },
  collar(o) { // a red dog collar with a gold round tag (o.text) - attach to the torso joint at the neck, offset up
    const g = grp(at(torus(o.r || 0.085, 0.018, o.color || '#C8322A', 6, 18), 0, 0, 0, PI / 2, 0, 0)), tg = grp(at(torus(0.014, 0.004, '#C9CCD1', 4, 10), 0, -0.012, 0));
    const disc = at(cyl(0.05, 0.05, 0.01, '#E8B830', 18, { outline: 0.003 }), 0, -0.075, 0, PI / 2, 0, 0); tg.add(disc);
    const tx = canvasPlane(0.088, 0.04, (c, W, H) => { c.fillStyle = '#E8B830'; c.fillRect(0, 0, W, H); c.fillStyle = '#2A2010'; let fs = H * 0.78; c.font = `900 ${fs}px Arial`; const tw = c.measureText(o.text || 'MÉDOR').width; if (tw > W * 0.94) fs *= W * 0.94 / tw;
      c.font = `900 ${fs}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.text || 'MÉDOR', W / 2, H * 0.55); }, { res: 256 }); tx.position.set(0, -0.075, 0.0065); tg.add(tx);
    tg.position.set(0, 0.03, (o.r || 0.085) + (o.tagOut ?? 0.06)); g.add(tg); g.userData.update = t => { tg.rotation.x = 0.06 * Math.sin(t * 3.3); }; return g; },
  pedestal(o) { // a stone plinth (o.h) with a bronze plaque (o.text) on its front
    const h = o.h || 1.0, w = o.w || 0.8, g = grp(at(box(w + 0.16, 0.12, w + 0.16, '#BDB6A8', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(w, h - 0.24, w, '#D8D1C2', { pivot: 'bottom', outline: 0.006 }), 0, 0.12, 0),
      at(box(w + 0.12, 0.12, w + 0.12, '#BDB6A8', { pivot: 'bottom', outline: 0.006 }), 0, h - 0.12, 0));
    if (o.text) g.add(at(label(o.text, w * 0.8, 0.16, { bg: '#9A7A3A', fg: '#F6E7B8', wrap: false }), 0, h * 0.55, w / 2 + 0.006)); return g; },
  rockPoster(o) { // an election poster on a stand: a drawn rock with googly eyes, "VOTEZ" / o.name; o.popAt
    const w = o.w || 0.9, h = w * 1.35, pl = canvasPlane(w, h, (c, W, Hh) => { c.fillStyle = '#2F62B5'; c.fillRect(0, 0, W, Hh); c.fillStyle = '#F4F4F0'; c.fillRect(W * 0.06, Hh * 0.2, W * 0.88, Hh * 0.58);
      c.fillStyle = '#9C9A94'; c.beginPath(); [[0.2, 0.68], [0.26, 0.42], [0.42, 0.33], [0.62, 0.34], [0.78, 0.45], [0.82, 0.68]].forEach(([x, y], i) => i ? c.lineTo(x * W, y * Hh) : c.moveTo(x * W, y * Hh)); c.closePath(); c.fill();
      c.strokeStyle = '#6E6C66'; c.lineWidth = W * 0.012; c.stroke();
      for (const x of [0.43, 0.59]) { c.fillStyle = '#FFFFFF'; c.beginPath(); c.arc(x * W, Hh * 0.47, W * 0.07, 0, TAU); c.fill(); c.fillStyle = '#1C1C20'; c.beginPath(); c.arc(x * W + W * 0.015, Hh * 0.48, W * 0.032, 0, TAU); c.fill(); }
      c.fillStyle = '#F4F4F0'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${Hh * 0.11}px Arial`; c.fillText('VOTEZ', W / 2, Hh * 0.11);
      let fs = Hh * 0.12; c.font = `900 ${fs}px Arial`; const tw = c.measureText(o.name || 'GÉRARD').width; if (tw > W * 0.9) fs *= W * 0.9 / tw; c.font = `900 ${fs}px Arial`; c.fillStyle = '#F2C94C'; c.fillText(o.name || 'GÉRARD', W / 2, Hh * 0.89); }, { res: 512 });
    const g = grp(), board = grp(at(box(w + 0.06, h + 0.06, 0.04, '#E8E1D0', { outline: 0.005 }), 0, 0, -0.025), pl); board.position.y = (o.lift ?? 0.55) + h / 2; g.add(board);
    for (const x of [-w * 0.35, w * 0.35]) g.add(rod([x, 0, -0.05], [x, (o.lift ?? 0.55) + 0.1, -0.05], 0.025, '#6B4A2E'));
    if (o.popAt != null) g.userData.update = t => { board.scale.setScalar(Math.max(0.001, ease.outBack(clamp01((t - o.popAt) / 0.3)))); };
    if (g.userData.update) g.userData.update(0); return g; },
  resultsBoard(o) { // election night: "RÉSULTATS" board, o.name with a bar filling to 100 % from o.fillAt, "AUTRES 0 %"
    const w = o.w || 1.4, h = o.h || 0.9, g = grp(at(box(w + 0.08, h + 0.08, 0.05, '#1C252A', { outline: 0.006 }), 0, 0, -0.03));
    const head = canvasPlane(w, h, (c, W, Hh) => { c.fillStyle = '#F4F4F0'; c.fillRect(0, 0, W, Hh); c.fillStyle = '#1C252A'; c.textAlign = 'left'; c.textBaseline = 'middle'; c.font = `900 ${Hh * 0.14}px Arial`; c.fillText('RÉSULTATS', W * 0.06, Hh * 0.13);
      c.font = `800 ${Hh * 0.11}px Arial`; c.fillText(o.name || 'GÉRARD', W * 0.06, Hh * 0.36); c.fillText('AUTRES', W * 0.06, Hh * 0.72); c.textAlign = 'right'; c.fillText('0 %', W * 0.94, Hh * 0.88);
      c.fillStyle = '#D9D5CB'; c.fillRect(W * 0.06, Hh * 0.45, W * 0.88, Hh * 0.13); c.fillRect(W * 0.06, Hh * 0.8, W * 0.62, Hh * 0.13); }, { res: 512 }); g.add(head);
    const bar = at(box(w * 0.88, h * 0.13, 0.012, '#2F62B5'), 0, 0, 0.008); const pct = canvasPlane(w * 0.3, h * 0.13, (c, W, Hh) => { c.fillStyle = '#2F62B5'; c.fillRect(0, 0, W, Hh); c.fillStyle = '#FFFFFF'; c.font = `900 ${Hh * 0.8}px Arial`; c.textAlign = 'right'; c.textBaseline = 'middle'; c.fillText('100 %', W * 0.95, Hh * 0.55); }, { res: 256 });
    const bg = grp(bar); g.add(bg); pct.position.set(w * 0.29, h * (0.5 - 0.515), 0.016); g.add(pct);
    g.userData.update = t => { const k = o.fillAt == null ? 1 : ease.outCubic ? ease.outCubic(clamp01((t - o.fillAt) / 0.6)) : clamp01((t - o.fillAt) / 0.6); bar.scale.x = Math.max(0.001, k); bar.position.set(-w * 0.44 * (1 - k), h * (0.5 - 0.515), 0.008); pct.visible = k > 0.95; };
    g.userData.update(0); return g; },
  trophy(o) { // a gold cup on a black base (o.text plate)
    const G = '#E8B830', g = grp(at(box(0.16, 0.08, 0.16, '#1C1C20', { pivot: 'bottom' }), 0, 0, 0), at(cyl(0.025, 0.04, 0.1, G, 10, { pivot: 'bottom' }), 0, 0.08, 0), at(cyl(0.1, 0.05, 0.16, G, 12, { pivot: 'bottom', outline: 0.004 }), 0, 0.18, 0));
    for (const sd of [-1, 1]) g.add(at(torus(0.045, 0.01, G, 4, 10), sd * 0.105, 0.28, 0, 0, 0, 0)); return g; },
  yearCalendar(o) { // a wall calendar showing the year: o.years [y0, y1] flips one page per year between o.flipAt and o.flipAt + o.dur (or holds o.years[0])
    const ys = o.years || [2026, 2026], n = ys[1] - ys[0] + 1, g = grp(at(box(0.56, 0.62, 0.02, '#F4F1E8', { outline: 0.005 }), 0, 0, 0), at(box(0.56, 0.12, 0.025, '#C8322A'), 0, 0.25, 0.003));
    for (const x of [-0.16, 0.16]) g.add(at(cyl(0.012, 0.012, 0.05, '#3A3D44', 6), x, 0.31, 0.02));
    const pages = []; for (let i = 0; i < n; i++) { const p = canvasPlane(0.5, 0.42, (c, W, H) => { c.fillStyle = '#F4F1E8'; c.fillRect(0, 0, W, H); c.fillStyle = '#1C252A'; c.font = `900 ${H * 0.4}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(String(ys[0] + i), W / 2, H * 0.42);
        c.fillStyle = '#8A8F96'; c.font = `700 ${H * 0.12}px Arial`; c.fillText('JANVIER', W / 2, H * 0.82); }, { res: 256 }); p.position.set(0, -0.06, 0.012); g.add(p); pages.push(p); }
    g.userData.update = t => { const k = o.flipAt == null ? 0 : Math.max(0, Math.min(n - 1, Math.floor((t - o.flipAt) / ((o.dur || 1) / Math.max(1, n - 1)) + 1e-6))); pages.forEach((p, i) => { p.visible = i === k; }); };
    g.userData.update(0); return g; },
  magazine(o) { // an old magazine held open-faced (cover facing +z): masthead, date, headline, a gold cup; held like a phone (HAND_FLAT)
    const w = o.w || 0.3, h = w * 1.3, pl = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#F2EEE4'; c.fillRect(0, 0, W, H); c.fillStyle = '#C8322A'; c.fillRect(0, 0, W, H * 0.17);
      c.fillStyle = '#FFFFFF'; c.font = `900 ${H * 0.11}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.title || 'ACTU MAG', W / 2, H * 0.09);
      c.fillStyle = '#1C252A'; c.font = `800 ${H * 0.055}px Arial`; c.fillText(o.date || 'JUILLET 1998', W / 2, H * 0.23);
      c.fillStyle = '#E8B830'; c.beginPath(); c.moveTo(W * 0.38, H * 0.33); c.lineTo(W * 0.62, H * 0.33); c.lineTo(W * 0.57, H * 0.5); c.lineTo(W * 0.43, H * 0.5); c.closePath(); c.fill(); c.fillRect(W * 0.47, H * 0.5, W * 0.06, H * 0.08); c.fillRect(W * 0.4, H * 0.58, W * 0.2, H * 0.04);
      c.fillStyle = '#1C252A'; let fs = H * 0.085; const t = o.headline || 'CHAMPIONS DU MONDE !'; c.font = `900 ${fs}px Arial`; const tw = c.measureText(t).width; if (tw > W * 0.92) fs *= W * 0.92 / tw; c.font = `900 ${fs}px Arial`;
      c.fillText(t, W / 2, H * 0.74); c.fillStyle = '#8A8F96'; c.font = `700 ${H * 0.04}px Arial`; c.fillText('N° 1998', W / 2, H * 0.92); }, { res: 512 });
    const g = grp(at(box(w + 0.01, h + 0.01, 0.012, '#D9D3C6'), 0, 0, -0.008), pl); g.userData.grip = [0, -h * 0.4, 0]; return g; },
  eyeChart(o) { // an optician's letter chart on the wall
    const w = o.w || 0.5, h = w * 1.4, pl = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FBFAF6'; c.fillRect(0, 0, W, H); c.fillStyle = '#1C1C20'; c.textAlign = 'center'; c.textBaseline = 'middle';
      [['E', 0.22], ['F P', 0.14], ['T O Z', 0.1], ['L P E D', 0.075], ['P E C F D', 0.055], ['E D F C Z P', 0.04]].forEach(([t, s], i, a) => { c.font = `900 ${H * s}px Arial`; c.fillText(t, W / 2, H * (0.14 + i * 0.15)); }); }, { res: 512 });
    return grp(at(box(w + 0.03, h + 0.03, 0.015, '#3A3D44'), 0, 0, -0.01), pl); },
  envelope(o) { // a letter in a white envelope (address lines, a stamp) - hold it like a card
    const w = o.w || 0.22, h = w * 0.62, pl = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#F7F4EC'; c.fillRect(0, 0, W, H); c.fillStyle = '#C8322A'; c.fillRect(W * 0.78, H * 0.08, W * 0.15, H * 0.24);
      c.fillStyle = '#3A3D44'; c.font = `700 ${H * 0.12}px Arial`; c.textAlign = 'left'; c.fillText(o.to || 'M. LE MEC', W * 0.32, H * 0.55); c.font = `600 ${H * 0.1}px Arial`; c.fillText(o.addr || "SALLE D'ATTENTE", W * 0.32, H * 0.72); }, { res: 256 });
    return grp(at(box(w, h, 0.004, '#EDE8DC'), 0, 0, -0.003), pl); },
  veil(o) { // a bride's veil (attach to the head joint, offset up): a little white headband with a translucent fall at the back
    const g = grp(at(torus(o.r || 0.14, 0.015, '#FFFFFF', 4, 16), 0, 0, 0, PI / 2, 0, 0));
    const v = mesh(new THREE.ConeGeometry(0.32, 0.9, 10, 1, true), new THREE.MeshLambertMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.55, side: THREE.DoubleSide, depthWrite: false }));
    v.position.set(0, -0.4, -0.12); g.add(v); g.add(at(sphere(0.03, '#F4C2C2', 0), 0.12, 0.02, 0.06), at(sphere(0.025, '#FFFFFF', 0), 0.09, 0.03, 0.09)); return g; },
  handset(o) { // a smartphone held to the ear (attach to the hand; o.screen colour)
    return grp(at(box(0.075, 0.15, 0.014, '#1C1C22', { outline: 0.004 }), 0, -0.06, 0), at(box(0.062, 0.12, 0.002, o.screen || '#5FA8E8', { noGrain: true }), 0, -0.06, 0.008)); },
  mole(o) { return grp(at(sphere(o.r || 0.014, o.color || '#4A2E22', 0, { noGrain: true }), 0, 0, 0)); },   // a grain de beauté: stick it on a cheek (head joint offset)
  ringMark(o) { // a red highlight ring that pops in at o.popAt (face the camera)
    const g = grp(at(torus(o.r || 0.06, 0.008, o.color || '#E0302A', 4, 24), 0, 0, 0)); if (o.popAt != null) { g.userData.update = t => { g.scale.setScalar(Math.max(0.001, ease.outBack(clamp01((t - o.popAt) / 0.25)))); }; g.userData.update(0); }
    return g; },
  briefcase(o) { // a leather briefcase (hold it by the handle: attach to the hand)
    const c = o.color || '#6B3E22', g = grp(at(box(0.42, 0.3, 0.1, c, { outline: 0.005 }), 0, -0.2, 0), at(box(0.43, 0.03, 0.105, '#4A2A16'), 0, -0.1, 0), at(box(0.05, 0.03, 0.11, '#D9B85A'), 0.12, -0.11, 0),
      at(box(0.05, 0.03, 0.11, '#D9B85A'), -0.12, -0.11, 0), at(torus(0.05, 0.01, '#3A2210', 4, 10), 0, -0.04, 0)); return g; },
  scoreCard(o) { // a jury score paddle held up (o.text, e.g. '10'), white card on a stick
    const w = o.w || 0.26, h = w * 0.75, pl = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FBFAF6'; c.fillRect(0, 0, W, H); c.strokeStyle = '#1C252A'; c.lineWidth = H * 0.05; c.strokeRect(H * 0.04, H * 0.04, W - H * 0.08, H - H * 0.08);
      c.fillStyle = o.color || '#1C252A'; c.font = `900 ${H * 0.62}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(String(o.text ?? '10'), W / 2, H * 0.55); }, { res: 256 });
    const g = grp(rod([0, -0.32, 0], [0, 0, 0], 0.012, '#8A6A44'), at(box(w + 0.01, h + 0.01, 0.008, '#D9D3C6'), 0, h / 2, -0.006), pl); pl.position.set(0, h / 2, 0.001); g.userData.grip = [0, -0.25, 0]; return g; },
  portraitPoster(o) { // a framed poster of the mec's face (drawn like his passport photo) with a caption (o.text) under it
    const w = o.w || 0.7, h = w * 1.3, pl = canvasPlane(w, h, (c, W, H) => { c.fillStyle = o.bg || '#DCE8F2'; c.fillRect(0, 0, W, H); const fw = W * 0.5, fh = H * 0.5, fx = (W - fw) / 2, fy = H * 0.1;
      c.fillStyle = '#1C1C20'; c.fillRect(fx + fw * 0.04, fy - H * 0.02, fw * 0.92, fh * 0.16); c.fillStyle = '#E8B48A'; c.fillRect(fx, fy + fh * 0.1, fw, fh * 0.9); c.fillStyle = '#1C1C20'; c.fillRect(fx, fy, fw, fh * 0.12);
      c.fillStyle = '#FFFFFF'; [0.3, 0.68].forEach(x => { c.beginPath(); c.arc(fx + fw * x, fy + fh * 0.42, fw * 0.08, 0, Math.PI * 2); c.fill(); }); c.fillStyle = '#1C1C20'; [0.3, 0.68].forEach(x => { c.beginPath(); c.arc(fx + fw * x, fy + fh * 0.43, fw * 0.035, 0, Math.PI * 2); c.fill(); });
      c.fillRect(fx + fw * 0.32, fy + fh * 0.78, fw * 0.36, fh * 0.03); c.fillStyle = '#7A5A44'; for (let i = 0; i < 40; i++) c.fillRect(fx + fw * (0.12 + ((i * 37) % 76) / 100), fy + fh * (0.66 + ((i * 53) % 28) / 100), 2, 2);
      c.fillStyle = '#1C252A'; c.fillRect(fx + fw * 0.2, fy + fh * 1.0, fw * 0.6, H * 0.12); c.fillStyle = '#C8322A'; c.fillRect(fx + fw * 0.45, fy + fh * 1.0, fw * 0.1, H * 0.1);
      c.fillStyle = '#1C252A'; let fs = H * 0.08; const t = o.text || "L'ORIGINAL"; c.font = `900 ${fs}px Arial`; const tw = c.measureText(t).width; if (tw > W * 0.88) fs *= W * 0.88 / tw; c.font = `900 ${fs}px Arial`;
      c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(t, W / 2, H * 0.88); }, { res: 512 });
    return grp(at(box(w + 0.06, h + 0.06, 0.04, o.frame || '#C9A227', { outline: 0.005 }), 0, 0, -0.025), pl); },
  cutChain(o) { // a cut bike chain hanging from the grip (hold it with HAND_FLAT), an open padlock at its end; it swings a little
    const g = grp(), L = o.color || '#6A6E74', n = o.n || 8, sw = grp(); g.add(sw);
    for (let i = 0; i < n; i++) { const lk = torus(0.032, 0.01, L, 4, 8); lk.position.set(0, -0.02 - i * 0.055, 0); lk.rotation.y = i % 2 ? PI / 2 : 0; sw.add(lk); }
    const lock = grp(at(box(0.1, 0.11, 0.045, '#D4A82A', { outline: 0.005 }), 0, -0.055, 0), at(torus(0.035, 0.009, '#C9CCD1', 4, 10), 0.035, 0.03, 0, 0, 0, 0.8), at(box(0.02, 0.03, 0.002, '#1C1C20'), 0, -0.06, 0.024));
    lock.position.set(0, -0.02 - n * 0.055, 0); sw.add(lock);
    const qw = new THREE.Quaternion(), qs = new THREE.Quaternion(), eu = new THREE.Euler();
    g.userData.update = t => { eu.set(0.06 * Math.sin(t * 2.3 + 1), 0, 0.1 * Math.sin(t * 3.1)); qs.setFromEuler(eu);   // hang in world space: undo the hand's rotation
      if (g.parent) { g.updateWorldMatrix(true, false); g.getWorldQuaternion(qw); qw.invert(); sw.quaternion.copy(qw).multiply(qs); } else sw.quaternion.copy(qs); };
    g.userData.update(0); return g; },
  bikeSign(o) { // the blue "bike parking" sign on a pole: white bicycle pictogram (o.h pole height)
    const h = o.h || 2.3, s = 0.5, g = grp(rod([0, 0, 0], [0, h, 0], 0.03, '#9AA0A6')), pl = canvasPlane(s, s, (c, W, H) => { c.fillStyle = '#2F62B5'; c.fillRect(0, 0, W, H); c.strokeStyle = '#FFFFFF'; c.lineWidth = W * 0.035;
      c.strokeRect(W * 0.04, H * 0.04, W * 0.92, H * 0.92); c.lineWidth = W * 0.045; c.lineCap = 'round'; c.lineJoin = 'round'; const wr = W * 0.16, y = H * 0.66;
      c.beginPath(); c.arc(W * 0.27, y, wr, 0, TAU); c.moveTo(W * 0.73 + wr, y); c.arc(W * 0.73, y, wr, 0, TAU); c.stroke();
      c.beginPath(); c.moveTo(W * 0.27, y); c.lineTo(W * 0.45, y); c.lineTo(W * 0.62, H * 0.42); c.lineTo(W * 0.38, H * 0.42); c.lineTo(W * 0.27, y); c.moveTo(W * 0.45, y); c.lineTo(W * 0.36, H * 0.34);
      c.moveTo(W * 0.3, H * 0.34); c.lineTo(W * 0.42, H * 0.34); c.moveTo(W * 0.73, y); c.lineTo(W * 0.62, H * 0.3); c.lineTo(W * 0.68, H * 0.27); c.stroke(); }, { res: 256 });
    const back = at(box(s + 0.02, s + 0.02, 0.02, '#C9CCD1'), 0, h - s / 2, -0.012); pl.position.set(0, h - s / 2, 0.001); g.add(back, pl); return g; },
  bikeRack(o) { // a steel hoop bike rack (inverted U along x), empty; o.n hoops 0.8 m apart
    const g = grp(), R = '#A4AAB0', w = 0.62, h = 0.82, n = o.n || 1;
    for (let k = 0; k < n; k++) { const x0 = (k - (n - 1) / 2) * 0.8;
      g.add(rod([x0 - w / 2, 0, 0], [x0 - w / 2, h - 0.12, 0], 0.025, R), rod([x0 + w / 2, 0, 0], [x0 + w / 2, h - 0.12, 0], 0.025, R), rod([x0 - w / 2 + 0.1, h, 0], [x0 + w / 2 - 0.1, h, 0], 0.025, R),
        rod([x0 - w / 2, h - 0.12, 0], [x0 - w / 2 + 0.1, h, 0], 0.025, R), rod([x0 + w / 2, h - 0.12, 0], [x0 + w / 2 - 0.1, h, 0], 0.025, R)); }
    return g; },
  crowdBarrier(o) { // a steel crowd-control barrier along x (o.length m), vertical bars, splayed feet; o.sign: a coloured panel with text
    const L = o.length || 2.0, H = o.height || 1.0, R = '#C2C6CC', g = grp(grp(rod([-L / 2, 0.14, 0], [L / 2, 0.14, 0], 0.016, R), rod([-L / 2, H, 0], [L / 2, H, 0], 0.022, R), rod([-L / 2, 0.08, 0], [-L / 2, H, 0], 0.022, R), rod([L / 2, 0.08, 0], [L / 2, H, 0], 0.022, R)));
    const n = Math.round(L / 0.13); for (let i = 1; i < n; i++) { const x = -L / 2 + i * L / n; g.add(rod([x, 0.14, 0], [x, H, 0], 0.009, R)); }
    for (const x of [-L / 2 + 0.12, L / 2 - 0.12]) g.add(rod([x, 0, -0.28], [x, 0.14, 0], 0.014, R), rod([x, 0, 0.28], [x, 0.14, 0], 0.014, R));
    if (o.sign) { const sg = canvasPlane(L * 0.7, 0.24, (c, W, Hh) => { c.fillStyle = o.bg || '#F2C94C'; c.fillRect(0, 0, W, Hh); c.fillStyle = o.fg || '#1C252A'; let fs = Hh * 0.62; c.font = `900 ${fs}px Arial`; const tw = c.measureText(o.sign).width; if (tw > W * 0.9) fs *= W * 0.9 / tw;
        c.font = `900 ${fs}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.sign, W / 2, Hh * 0.54); }, { res: 512 }); sg.position.set(0, H * 0.62, 0.014); g.add(sg); const sb = sg.clone(); sb.position.z = -0.014; sb.rotation.y = PI; g.add(sb); }
    return g; },
  pressCamera(o) { // a press photographer's camera, lens along +z; its flash fires (a white burst) at o.flashAt (seconds)
    const g = grp(at(box(0.16, 0.11, 0.075, '#1C1C20', { outline: 0.004 }), 0, 0, 0), at(cyl(0.045, 0.045, 0.11, '#2A2A2E', 10), 0, 0, 0.09, PI / 2), at(cyl(0.036, 0.036, 0.006, '#7FA6CC', 10), 0, 0, 0.147, PI / 2),
      at(box(0.07, 0.06, 0.06, '#1C1C20'), 0, 0.09, 0.0));
    const fl = mesh(new THREE.PlaneGeometry(0.06, 0.04), new THREE.MeshBasicMaterial({ color: '#C9CCD1' })); fl.position.set(0, 0.095, 0.031); g.add(fl);
    const bc = document.createElement('canvas'); bc.width = bc.height = 128; const bx = bc.getContext('2d'), gr = bx.createRadialGradient(64, 64, 2, 64, 64, 64);
    gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.25, 'rgba(255,255,240,0.95)'); gr.addColorStop(0.55, 'rgba(255,250,220,0.35)'); gr.addColorStop(1, 'rgba(255,250,220,0)'); bx.fillStyle = gr; bx.fillRect(0, 0, 128, 128);
    for (let i = 0; i < 8; i++) { bx.save(); bx.translate(64, 64); bx.rotate(i * PI / 4); bx.fillStyle = 'rgba(255,255,255,0.55)'; bx.fillRect(-1.5, 0, 3, 62); bx.restore(); }
    const btex = new THREE.CanvasTexture(bc); btex.colorSpace = THREE.SRGBColorSpace;
    const burst = new THREE.Sprite(new THREE.SpriteMaterial({ map: btex, transparent: true, depthWrite: false, depthTest: false })); const bs = (o.burst || 0.22) * 2.6; burst.scale.set(bs, bs, 1); burst.position.set(0, 0.095, 0.06); burst.renderOrder = 10; g.add(burst);
    const fa = [].concat(o.flashAt ?? []); g.userData.update = t => { const on = fa.some(a => t >= a && t < a + 0.09); burst.visible = on; fl.material.color.set(on ? '#FFFFFF' : '#C9CCD1'); };
    g.userData.update(0); return g; },
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
  bathScale(o) { // la balance: a digital bathroom scale (o.w square, white, glass top), a flat LCD near its front (+Z) edge read from above.
    // o.show [[t, v, from]]: v a number (counts up from `from` over 0.35 s, then blinks twice), 'plane' (airplane-mode icon), '' (off). o.pressAt: the red button sinks.
    // o.wingsAt: wings, a tail fin (back, -Z), a nose propeller and blinking wingtip lights pop out: a little plane whose nose is the display edge. o.bob [amp, freq, t0]
    const w = o.w || 0.36, d = w * 0.92, h = 0.04, g = grp(), body = grp(); g.add(body);
    body.add(at(box(w, h, d, '#F6F6F2', { pivot: 'bottom', outline: o.outline ?? 0.004 }), 0, 0.012, 0), at(box(w * 0.93, 0.004, d * 0.9, '#CFDDE4'), 0, h + 0.013, 0));
    for (const [sx, sz] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) body.add(at(cyl(0.014, 0.016, 0.012, '#4A5058', 8, { pivot: 'bottom' }), sx * w * 0.38, 0, sz * d * 0.38));
    const dw = w * 0.46, dh = w * 0.17, cv = document.createElement('canvas'); cv.width = 320; cv.height = Math.round(320 * dh / dw);
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
    const lcd = new THREE.Mesh(new THREE.PlaneGeometry(dw, dh), new THREE.MeshBasicMaterial({ map: tex })); lcd.rotation.x = -PI / 2; lcd.position.set(0, h + 0.0165, d / 2 - dh / 2 - 0.022); body.add(lcd);
    body.add(at(box(dw + 0.014, 0.003, dh + 0.014, '#2A3236'), 0, h + 0.0145, d / 2 - dh / 2 - 0.022));
    const btn = at(cyl(0.013, 0.013, 0.008, '#C8322A', 10, { pivot: 'bottom' }), -w * 0.38, h + 0.012, d / 2 - 0.03); body.add(btn);
    const SEG = { 0: 'abcdef', 1: 'bc', 2: 'abdeg', 3: 'abcdg', 4: 'bcfg', 5: 'acdfg', 6: 'acdefg', 7: 'abc', 8: 'abcdefg', 9: 'abcdfg', '-': 'g' };
    const seg7 = (c, x, y, sw, sh, ch, on, off) => { const t = sw * 0.18, v = sh / 2 - 1.5 * t, R = { a: [x + t, y, sw - 2 * t, t], g: [x + t, y + sh / 2 - t / 2, sw - 2 * t, t], d: [x + t, y + sh - t, sw - 2 * t, t],
      f: [x, y + t, t, v], b: [x + sw - t, y + t, t, v], e: [x, y + sh / 2 + t / 2, t, v], c: [x + sw - t, y + sh / 2 + t / 2, t, v] };
      for (const [k, r] of Object.entries(R)) { c.fillStyle = (SEG[ch] || '').includes(k) ? on : off; c.fillRect(...r); } };
    let cur = null; const draw = s => { if (s === cur) return; cur = s; const c = cv.getContext('2d'), W = cv.width, H = cv.height, on = '#93F8E8', off = 'rgba(147,248,232,0.035)';
      c.fillStyle = '#132327'; c.fillRect(0, 0, W, H); c.fillStyle = on;
      if (s === 'plane') { c.save(); c.translate(W / 2, H / 2); const q = H * 0.43; const poly = pts => { c.beginPath(); pts.forEach(([x, y], i) => i ? c.lineTo(x * q, y * q) : c.moveTo(x * q, y * q)); c.closePath(); c.fill(); };
        c.beginPath(); c.moveTo(-1.0 * q, -0.1 * q); c.lineTo(0.78 * q, -0.1 * q); c.quadraticCurveTo(1.08 * q, 0, 0.78 * q, 0.1 * q); c.lineTo(-1.0 * q, 0.1 * q); c.closePath(); c.fill();
        poly([[0.18, -0.08], [-0.28, -0.98], [-0.06, -0.98], [0.5, -0.08]]); poly([[0.18, 0.08], [-0.28, 0.98], [-0.06, 0.98], [0.5, 0.08]]);
        poly([[-0.74, -0.08], [-0.96, -0.44], [-0.83, -0.44], [-0.54, -0.08]]); poly([[-0.74, 0.08], [-0.96, 0.44], [-0.83, 0.44], [-0.54, 0.08]]); c.restore(); }
      else if (s !== '') { const n = 3, sh = H * 0.7, sw = sh * 0.56, gap = sh * 0.16, kg = H * 0.3, tot = n * sw + (n - 1) * gap + kg * 1.3, x0 = (W - tot) / 2, y0 = (H - sh) / 2, str = String(s).padStart(n, ' ');
        for (let i = 0; i < n; i++) seg7(c, x0 + i * (sw + gap), y0, sw, sh, str[i], on, off);
        c.fillStyle = on; c.font = `bold ${kg}px Arial`; c.textAlign = 'left'; c.textBaseline = 'alphabetic'; c.fillText('kg', x0 + n * (sw + gap) + kg * 0.1, y0 + sh); }
      tex.needsUpdate = true; };
    const show = (o.show || []).map(([t0, v, from]) => ({ t0, v, from })).sort((a, b) => a.t0 - b.t0);
    const textAt = t => { let k = null; for (const x of show) if (t >= x.t0) k = x; if (!k) return o.idle ?? '';
      if (typeof k.v === 'number') { const u = clamp01((t - k.t0) / 0.35); if (k.from != null && u < 1) return String(Math.round(k.from + (k.v - k.from) * ease.out(u)));
        const b = t - k.t0 - (k.from != null ? 0.35 : 0); return b < 0.3 && Math.floor(b / 0.075) % 2 === 1 ? '   ' : String(k.v); }
      if (k.v === 'plane') return t - k.t0 < 0.3 && Math.floor((t - k.t0) / 0.075) % 2 === 1 ? '' : 'plane';
      return k.v; };
    body.add(at(box(w * 0.96, 0.006, d * 0.94, '#3A4048'), 0, 0.009, 0));   // dark underside: reads against white tiles and clouds
    const WC = o.wingColor || '#D8382E';
    const wing = sd => { const p = grp(at(box(0.3, 0.014, 0.12, WC, { outline: 0.004 }), sd * 0.15, 0, 0), at(box(0.06, 0.016, 0.125, '#F6F6F2'), sd * 0.27, 0.001, 0), at(sphere(0.016, sd < 0 ? '#FF3B30' : '#34C759', 1, { emissive: sd < 0 ? '#FF3B30' : '#34C759' }), sd * 0.31, 0.006, -0.03));
      p.position.set(sd * w / 2, h * 0.6, 0.0); p.rotation.y = sd * 0.28; body.add(p); return p; };
    const wL = wing(-1), wR = wing(1);
    const tail = grp(at(box(0.014, 0.13, 0.1, WC, { pivot: 'bottom', outline: 0.004 }), 0, 0, 0), at(box(0.2, 0.012, 0.06, WC, { outline: 0.004 }), 0, 0.01, 0.0), at(box(0.016, 0.03, 0.05, '#F6F6F2'), 0, 0.12, -0.02));
    const trails = grp(); if (o.trail) for (const sd of [-1, 1]) { const L = o.trail, m = new THREE.Mesh(new THREE.BoxGeometry(0.035, 0.035, L), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.55, depthWrite: false })); m.position.set(sd * (w / 2 + 0.3), h * 0.6, -L / 2 - 0.05); trails.add(m); }
    body.add(trails);
    tail.position.set(0, h + 0.012, -d / 2 + 0.05); body.add(tail);
    const blades = grp(at(box(0.17, 0.02, 0.006, '#3A3F46'), 0, 0, 0), at(box(0.02, 0.17, 0.006, '#3A3F46'), 0, 0, 0));
    const blur = new THREE.Mesh(new THREE.CircleGeometry(0.09, 20), new THREE.MeshBasicMaterial({ color: '#C9D3DA', transparent: true, opacity: 0.35, depthWrite: false }));
    const nose = grp(at(cyl(0.018, 0.022, 0.03, '#C8322A', 10), 0, 0, 0, PI / 2, 0, 0), blades, blur); blades.position.z = 0.02; blur.position.z = 0.021;
    nose.position.set(0, h * 0.55 + 0.012, d / 2 + 0.018); body.add(nose);
    const lights = [wL.children[1], wR.children[1]];
    g.userData.update = t => { draw(textAt(t)); btn.position.y = h + 0.012 - (o.pressAt != null && t >= o.pressAt && t < o.pressAt + 0.3 ? 0.006 : 0);
      const s = Math.max(0.001, pop(t, o.wingsAt ?? null, 0.32)); for (const x of [wL, wR, tail, nose]) x.scale.setScalar(s);
      if (o.grow) g.scale.setScalar(1 + (o.grow - 1) * Math.min(1, Math.max(0, s)));   // it grows into a little plane as the wings come out
      trails.visible = !!o.trail && t >= (o.trailAt ?? 0); trails.scale.z = o.trail ? Math.min(1, Math.max(0.01, (t - (o.trailAt ?? 0)) / 0.35)) : 1;
      blades.rotation.z = t * 31; lights.forEach(l => { l.visible = Math.floor(t * 2.5) % 2 === 0; });
      if (o.bob) { const [a, f, t0] = o.bob, u = clamp01((t - t0) / 0.4); body.position.y = u * a * Math.sin(TAU * f * (t - t0)); body.rotation.z = u * 0.07 * Math.sin(TAU * f * 0.7 * (t - t0)); } };
    g.userData.update(0); return g;
  },
  serviceCloud(o) { // a big flat-topped cumulus to land on (o.w wide, top at y = o.top), with a scale-like LCD on its front (+Z) reading o.text ('HORS SERVICE'),
    // blinking from o.blinkAt; o.squashAt: squash-and-bounce when something lands (pivot at its bottom)
    const W = o.w || 3.4, D = W * 0.55, TOP = o.top || 1.1, r = rng(o.seed || 23), g = grp(), body = grp(); g.add(body);
    const geo = new THREE.IcosahedronGeometry(1, 1), mw = mat('#FFFFFF', { flat: true }), ms = mat('#E6EEF5', { flat: true }), L = [];
    for (let i = 0; i < 7; i++) { const u = i / 6 - 0.5, R = (0.4 + r() * 0.16) * W / 3.4; L.push([u * W * 0.86, R * 0.8, (r() - 0.5) * D * 0.3, R * 1.15, R * 0.8, R * 1.05]); }
    for (let i = 0; i < 5; i++) { const u = i / 4 - 0.5, R = (0.46 + r() * 0.16) * W / 3.4; L.push([u * W * 0.66, TOP - R * 0.5, (r() - 0.5) * D * 0.3 - 0.05, R * 1.2, R * 0.55, R * 1.05]); }
    const mlow = mat(o.lowColor || '#D3DEE9', { flat: true });
    for (const [x, y, z, sx, sy, sz] of L) { const m = mesh(geo, y < TOP * 0.45 ? mlow : r() < 0.3 ? ms : mw); m.position.set(x, y, z); m.scale.set(sx, sy, sz); body.add(m); }
    body.add(at(cyl(W * 0.3, W * 0.34, 0.1, '#FFFFFF', 14), 0, TOP - 0.05, -0.05));
    const front = Math.max(...L.filter(l => Math.abs(l[0]) < W * 0.25 && l[1] < TOP * 0.85).map(l => l[2] + l[5] * 0.82));
    const dw = o.dw || W * 0.42, dh = dw * 0.3, txt = o.text || 'HORS SERVICE';
    const lcdBg = (c, Wc, Hc) => { c.fillStyle = '#132327'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = 'rgba(255,90,70,0.07)'; const n = 12, cw = Wc * 0.86 / n;   // unlit ghost cells, like the scale's LCD
      for (let i = 0; i < n; i++) { const x = Wc * 0.07 + i * cw; c.fillRect(x + cw * 0.12, Hc * 0.2, cw * 0.76, Hc * 0.08); c.fillRect(x + cw * 0.12, Hc * 0.72, cw * 0.76, Hc * 0.08); c.fillRect(x + cw * 0.08, Hc * 0.26, cw * 0.1, Hc * 0.48); c.fillRect(x + cw * 0.78, Hc * 0.26, cw * 0.1, Hc * 0.48); } };
    const pl = canvasPlane(dw, dh, (c, Wc, Hc) => { lcdBg(c, Wc, Hc); c.fillStyle = o.textColor || '#FF3B3B'; c.textAlign = 'center'; c.textBaseline = 'middle';
      let px = Hc * 0.5; c.font = `900 ${px}px Arial`; const tw = c.measureText(txt).width; if (tw > Wc * 0.88) { px *= Wc * 0.88 / tw; c.font = `900 ${px}px Arial`; } c.fillText(txt, Wc / 2, Hc * 0.54);
      c.fillStyle = 'rgba(19,35,39,0.35)'; for (let y = 0; y < Hc; y += Math.max(2, Hc / 40)) c.fillRect(0, y, Wc, Math.max(1, Hc / 120)); }, { res: 512, emissive: 0.9 });
    const dark = canvasPlane(dw, dh, (c, Wc, Hc) => lcdBg(c, Wc, Hc), { res: 256 }); dark.position.z = 0.001;
    const led = at(sphere(dh * 0.09, '#FF3B30', 1, { emissive: '#FF3B30' }), dw / 2 - dh * 0.02, dh / 2 + 0.005, 0.02);
    const panel = grp(at(box(dw + 0.08, dh + 0.08, 0.06, '#2A3236', { outline: 0.006 }), 0, 0, -0.03), at(pl, 0, 0, 0.002), dark, led); panel.position.set(o.panelX || 0, TOP * (o.panelY ?? 0.45), front + 0.16); body.add(panel);
    g.userData.update = t => { const on = o.bootAt == null || (t >= o.bootAt && (t - o.bootAt > 0.32 || Math.floor((t - o.bootAt) / 0.06) % 2 === 1)); pl.visible = on; dark.visible = !on;
      const bl = o.blinkAt != null && t >= o.blinkAt ? (t - o.blinkAt) % 0.5 : 0; led.visible = on && bl < 0.25; pl.material.emissiveIntensity = o.blinkAt != null && t >= o.blinkAt && bl >= 0.25 ? 0.6 : 0.9;
      const u = o.squashAt == null ? -1 : t - o.squashAt; if (u >= 0 && u < 0.7) { const s = 1 - 0.2 * Math.sin(u / 0.7 * TAU) * (1 - u / 0.7); body.scale.set(1 + (1 - s) * 0.45, s, 1 + (1 - s) * 0.45); } else body.scale.set(1, 1, 1); };
    g.userData.update(0); return g;
  },
  gymBuilding(o) { // a flat-roofed sports hall o.w × o.d × o.h (front +Z): pale walls, a band of big windows, its name painted huge on the roof (o.text) with a dumbbell (canvas top = -Z), the name on the facade
    const W = o.w || 26, D = o.d || 30, H = o.h || 9, g = grp(), name = o.text || 'SALLE DE SPORT', rc = o.roof || '#C8463C';
    g.add(at(box(W, H, D, o.color || '#E4E7EA', { pivot: 'bottom', outline: 0.02 }), 0, 0, 0));
    for (const [x, z, ry, len] of [[0, D / 2 + 0.03, 0, W], [0, -D / 2 - 0.03, PI, W], [W / 2 + 0.03, 0, PI / 2, D], [-W / 2 - 0.03, 0, -PI / 2, D]]) g.add(at(box(len * 0.9, H * 0.3, 0.06, '#3E6A8E'), x, H * 0.52, z, 0, ry, 0));
    for (const [x, z, sx, sz] of [[0, D / 2, W + 0.4, 0.4], [0, -D / 2, W + 0.4, 0.4], [W / 2, 0, 0.4, D], [-W / 2, 0, 0.4, D]]) g.add(at(box(sx, 0.5, sz, '#B9BEC4'), x, H + 0.25, z));
    const roof = canvasPlane(W - 0.5, D - 0.5, (c, Wc, Hc) => { c.fillStyle = rc; c.fillRect(0, 0, Wc, Hc); c.strokeStyle = 'rgba(255,255,255,0.9)'; c.lineWidth = Wc * 0.012; c.strokeRect(Wc * 0.04, Hc * 0.04, Wc * 0.92, Hc * 0.92);
      c.fillStyle = '#FFFFFF'; const cx = Wc / 2, cy = Hc * 0.27, u = Wc * 0.1; c.fillRect(cx - u * 1.6, cy - u * 0.12, u * 3.2, u * 0.24);
      for (const sd of [-1, 1]) { c.fillRect(cx + sd * u * 1.15 - u * 0.17, cy - u * 0.62, u * 0.34, u * 1.24); c.fillRect(cx + sd * u * 1.6 - u * 0.13, cy - u * 0.42, u * 0.26, u * 0.84); }
      c.textAlign = 'center'; c.textBaseline = 'middle'; const lines = o.stack ? name.split(' ') : name.split(' ').length > 2 ? [name.split(' ')[0], name.split(' ').slice(1).join(' ')] : [name], mw = Wc * (o.textW || 0.86);
      let px = Hc * (o.stack ? 0.15 : 0.17); c.font = `900 ${px}px Arial`; const tw = Math.max(...lines.map(l => c.measureText(l).width)); if (tw > mw) { px *= mw / tw; c.font = `900 ${px}px Arial`; }
      lines.forEach((l, i) => c.fillText(l, Wc / 2, Hc * 0.6 + (i - (lines.length - 1) / 2) * px * 1.12)); }, { res: 1024 });
    roof.rotation.x = -PI / 2; roof.position.set(0, H + 0.03, 0); g.add(roof);
    const sl = name.split(' '); g.add(at(box(8.3, 2.7, 0.12, '#FFFFFF'), 0, H * 0.83, D / 2 + 0.05), at(sign(sl.length > 2 ? sl[0] + '\n' + sl.slice(1).join(' ') : name, 8, 2.4, rc, '#FFFFFF'), 0, H * 0.83, D / 2 + 0.12));
    return g;
  },
  openWindow(o) { // an open French window on a facade (front +Z): the dark room behind, a white frame, a stone sill to stand on (top at y = 0), two blue shutters folded flat on the wall; o.w × o.h
    const w = o.w || 1.2, h = o.h || 2.2, g = grp(), fc = '#F4F1E8';
    g.add(at(box(w, h, 0.02, '#1E252D'), 0, h / 2, 0.01), at(box(w, h * 0.3, 0.01, '#5E8F88'), 0, h * 0.15, 0.022), at(box(w * 0.5, 0.06, 0.012, '#C8322A'), -w * 0.12, h * 0.55, 0.023));
    g.add(at(box(w + 0.14, 0.08, 0.06, fc), 0, h + 0.04, 0.03), at(box(0.07, h, 0.06, fc), -w / 2 - 0.035, h / 2, 0.03), at(box(0.07, h, 0.06, fc), w / 2 + 0.035, h / 2, 0.03));
    g.add(at(box(w + 0.32, 0.1, 0.34, '#E2D8C4', { outline: 0.004 }), 0, -0.05, 0.13));
    for (const sd of [-1, 1]) g.add(at(box(w * 0.5, h, 0.04, o.shutter || '#5B7894', { outline: 0.004 }), sd * (w / 2 + 0.08 + w * 0.25), h / 2, 0.04));
    return g;
  },
  idCardMec(o) { // le sosie: a French ID card (o.w wide) with the mec's photo (box face, black hair, stubble, red tie) and o.name; front +Z, grip at its left edge
    const w = o.w || 0.16, h = w * 0.63, pl = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#DCE9F2'; c.fillRect(0, 0, W, H); c.fillStyle = '#F2D9E0'; c.fillRect(0, H * 0.55, W, H * 0.45);
      c.fillStyle = '#2C4A8A'; c.fillRect(0, 0, W, H * 0.17); c.fillStyle = '#FFFFFF'; c.font = `bold ${H * 0.09}px Arial`; c.textAlign = 'left'; c.textBaseline = 'middle'; c.fillText("CARTE NATIONALE D'IDENTITÉ", W * 0.05, H * 0.085);
      const fx = W * 0.06, fy = H * 0.24, fw = W * 0.3, fh = H * 0.68; c.fillStyle = '#C9D6DE'; c.fillRect(fx, fy, fw, fh);
      c.fillStyle = '#1E2A3A'; c.fillRect(fx + fw * 0.08, fy + fh * 0.78, fw * 0.84, fh * 0.22); c.fillStyle = '#FFFFFF'; c.fillRect(fx + fw * 0.42, fy + fh * 0.78, fw * 0.16, fh * 0.22); c.fillStyle = '#C8322A'; c.fillRect(fx + fw * 0.46, fy + fh * 0.8, fw * 0.08, fh * 0.2);
      const hx = fx + fw * 0.22, hy = fy + fh * 0.08, hw = fw * 0.56, hh = fh * 0.66; c.fillStyle = '#E2A97C'; c.fillRect(hx, hy, hw, hh); c.fillStyle = '#17161A'; c.fillRect(hx - fw * 0.02, hy - fh * 0.03, hw + fw * 0.04, hh * 0.18);
      c.fillStyle = '#FFFFFF'; [0.3, 0.7].forEach(u => c.fillRect(hx + hw * u - hw * 0.1, hy + hh * 0.36, hw * 0.2, hh * 0.1)); c.fillStyle = '#17161A'; [0.3, 0.7].forEach(u => c.fillRect(hx + hw * u - hw * 0.03, hy + hh * 0.37, hw * 0.07, hh * 0.08));
      c.fillRect(hx + hw * 0.3, hy + hh * 0.74, hw * 0.4, hh * 0.04); c.fillStyle = 'rgba(60,40,30,0.55)'; for (let i = 0; i < 26; i++) c.fillRect(hx + hw * (0.12 + ((i * 37) % 76) / 100), hy + hh * (0.6 + ((i * 53) % 34) / 100), 2, 2);
      c.fillStyle = '#1C252A'; c.font = `bold ${H * 0.1}px Arial`; c.fillText('NOM :', W * 0.42, H * 0.34); c.font = `900 ${H * 0.13}px Arial`; c.fillText(o.name || 'LE MEC', W * 0.42, H * 0.48);
      c.font = `bold ${H * 0.08}px Arial`; c.fillText('NÉ LE : 03.05.1988', W * 0.42, H * 0.64); c.strokeStyle = '#2C4A8A'; c.lineWidth = H * 0.02; c.beginPath(); c.moveTo(W * 0.45, H * 0.85);
      for (let i = 0; i < 8; i++) c.lineTo(W * (0.47 + i * 0.05), H * (0.85 + (i % 2 ? -0.07 : 0.04))); c.stroke(); }, { res: 512 });
    const g = grp(at(box(w + 0.004, h + 0.004, 0.003, '#FFFFFF'), 0, 0, -0.002), pl); pl.position.z = 0.0005; g.userData.grip = [-w * 0.42, 0, 0]; return g;
  },
  cheekPuff(o) { // a puffed cheek (skin-coloured flattened ball) that inflates from o.growAt over o.dur; attach to a head joint
    const m = at(sphere(o.r || 0.06, o.color || '#E2A97C', 1), 0, 0, 0); m.scale.set(0.9, 0.8, 0.55); const g = grp(m);
    g.userData.update = t => { const u = o.growAt == null ? 1 : clamp01((t - o.growAt) / (o.dur || 0.6)); m.visible = u > 0.02; const k = ease.outBack(u) * (1 + 0.04 * Math.sin(t * 13)); m.scale.set(0.9 * k, 0.8 * k, 0.55 * k); };
    g.userData.update(0); return g;
  },
  speechBubble(o) { // a white comic speech bubble (o.text) with a tail toward o.tail ('left' | 'right' | 'down'), pops in at o.popAt; faces +Z
    const w = o.w || 0.7, h = o.h || 0.36, pl = canvasPlane(w, h * 1.35, (c, W, H) => { const bh = H / 1.35, r = bh * 0.45; c.clearRect(0, 0, W, H);
      c.fillStyle = '#FFFFFF'; c.strokeStyle = '#1C252A'; c.lineWidth = bh * 0.06;
      const rr = (x, y, ww, hh, rad) => { c.beginPath(); c.moveTo(x + rad, y); c.arcTo(x + ww, y, x + ww, y + hh, rad); c.arcTo(x + ww, y + hh, x, y + hh, rad); c.arcTo(x, y + hh, x, y, rad); c.arcTo(x, y, x + ww, y, rad); c.closePath(); };
      rr(c.lineWidth, c.lineWidth, W - 2 * c.lineWidth, bh - 2 * c.lineWidth, r); c.fill(); c.stroke();
      const tx = o.tail === 'right' ? W * 0.72 : o.tail === 'down' ? W * 0.5 : W * 0.28; c.beginPath(); c.moveTo(tx - bh * 0.18, bh - c.lineWidth * 1.5); c.lineTo(tx + (o.tail === 'right' ? bh * 0.3 : o.tail === 'down' ? 0 : -bh * 0.3), H - c.lineWidth); c.lineTo(tx + bh * 0.18, bh - c.lineWidth * 1.5); c.closePath(); c.fill(); c.stroke();
      c.fillStyle = '#FFFFFF'; c.fillRect(tx - bh * 0.15, bh - c.lineWidth * 3, bh * 0.3, c.lineWidth * 2.4);
      c.fillStyle = o.fg || '#1C252A'; c.textAlign = 'center'; c.textBaseline = 'middle'; let px = bh * 0.46; c.font = `900 ${px}px Arial`; const tw = c.measureText(o.text || 'WOUF !').width; if (tw > W * 0.82) { px *= W * 0.82 / tw; c.font = `900 ${px}px Arial`; }
      c.fillText(o.text || 'WOUF !', W / 2, bh * 0.52); }, { res: 512, transparent: true });
    const inner = grp(pl); pl.position.y = -h * 0.175; const g = grp(inner);
    g.userData.update = t => { if (o.popAt == null) return; const u = clamp01((t - o.popAt) / 0.28); inner.visible = t >= o.popAt; inner.scale.setScalar(Math.max(0.01, ease.outBack(u))); };
    g.userData.update(0); return g;
  },
  giftBone(o) { // a red gift box with a gold ribbon whose lid pops off at o.openAt, revealing a big cartoon bone that rises out of it
    const g = grp(at(box(0.32, 0.22, 0.32, '#C8322A', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(0.06, 0.225, 0.325, '#F2C94C'), 0, 0.112, 0), at(box(0.325, 0.225, 0.06, '#F2C94C'), 0, 0.112, 0));
    const lid = grp(at(box(0.35, 0.06, 0.35, '#C8322A', { outline: 0.006 }), 0, 0.03, 0), at(box(0.07, 0.065, 0.355, '#F2C94C'), 0, 0.03, 0), at(torus(0.05, 0.015, '#F2C94C', 6, 12), 0, 0.09, 0, PI / 2, 0, 0)); lid.position.y = 0.22; g.add(lid);
    const bone = grp(at(cyl(0.035, 0.035, 0.34, '#F4EFE2', 8), 0, 0, 0, 0, 0, PI / 2)); for (const sx of [-1, 1]) for (const sz of [-1, 1]) bone.add(at(sphere(0.05, '#F4EFE2', 1), sx * 0.18, 0, sz * 0.035));
    bone.position.y = 0.12; g.add(bone);
    g.userData.update = t => { const u = o.openAt == null ? 0 : clamp01((t - o.openAt) / 0.35); lid.position.set(0.25 * u, 0.22 + 0.25 * Math.sin(u * PI) * 1.2, 0); lid.rotation.z = -1.4 * u; bone.position.y = 0.12 + 0.28 * ease.outBack(clamp01((t - (o.openAt ?? 1e9) - 0.1) / 0.35)); bone.rotation.z = 0.3 * Math.sin(t * 3) * u; };
    g.userData.update(0); return g;
  },
  folderDoc(o) { // a manila folder with papers (o.text on its tab label); hold it or throw it
    const fc = o.color || '#E2B866', g = grp(at(box(0.32, 0.02, 0.24, fc, { outline: 0.004 }), 0, 0, 0), at(box(0.29, 0.012, 0.22, '#F7F3EA'), 0, 0.012, 0.005), at(box(0.1, 0.022, 0.03, fc), -0.08, 0, -0.13));
    if (o.text) g.add(at(label(o.text, 0.24, 0.08, { bg: '#FFFFFF', fg: '#1C252A' }), 0, 0.022, 0.0, -PI / 2, 0, 0));
    return g;
  },
  sugarCube(o) { return grp(at(box(0.035, 0.035, 0.035, '#FFFFFF', { outline: 0.002 }), 0, 0.0175, 0)); },  // a sugar cube
  callGrid(o) { // a laptop-style video call: o.tiles faces in a 2x2 grid (o.labels), o.bark tile index shows a "WOUF" bubble from o.barkAt; front +Z, o.w wide
    const w = o.w || 0.34, h = w * 0.62, labels = o.labels || ['CHIEN', 'BOSS', 'RH', 'COMPTA'];
    const pl = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#1E2229'; c.fillRect(0, 0, W, H); const tw = W / 2, th = H / 2;
      const bgs = ['#7FA7C9', '#C9A27A', '#9FC49A', '#C99AB8'];
      for (let i = 0; i < 4; i++) { const x = (i % 2) * tw, y = Math.floor(i / 2) * th; c.fillStyle = bgs[i]; c.fillRect(x + 3, y + 3, tw - 6, th - 6);
        if (i === 0) { c.fillStyle = '#C99A62'; c.fillRect(x + tw * 0.32, y + th * 0.22, tw * 0.36, th * 0.55); c.fillStyle = '#7A5232'; c.fillRect(x + tw * 0.24, y + th * 0.24, tw * 0.1, th * 0.3); c.fillRect(x + tw * 0.66, y + th * 0.24, tw * 0.1, th * 0.3);
          c.fillStyle = '#E8D2AE'; c.fillRect(x + tw * 0.42, y + th * 0.5, tw * 0.16, th * 0.16); c.fillStyle = '#1C1C20'; c.fillRect(x + tw * 0.47, y + th * 0.5, tw * 0.06, th * 0.05); c.fillRect(x + tw * 0.39, y + th * 0.38, tw * 0.04, th * 0.06); c.fillRect(x + tw * 0.57, y + th * 0.38, tw * 0.04, th * 0.06);
          c.fillStyle = '#C8322A'; c.fillRect(x + tw * 0.46, y + th * 0.78, tw * 0.08, th * 0.2); }
        else { c.fillStyle = ['#E2A97C', '#D9AA80', '#C98A5A'][i - 1]; c.fillRect(x + tw * 0.36, y + th * 0.2, tw * 0.28, th * 0.48); c.fillStyle = ['#2A2420', '#8A8A86', '#17161A'][i - 1]; c.fillRect(x + tw * 0.34, y + th * 0.16, tw * 0.32, th * 0.1);
          c.fillStyle = '#1C1C20'; c.fillRect(x + tw * 0.42, y + th * 0.36, tw * 0.04, th * 0.06); c.fillRect(x + tw * 0.54, y + th * 0.36, tw * 0.04, th * 0.06); c.fillRect(x + tw * 0.44, y + th * 0.55, tw * 0.12, th * 0.03);
          c.fillStyle = ['#2E4563', '#3A3D44', '#5C4330'][i - 1]; c.fillRect(x + tw * 0.26, y + th * 0.72, tw * 0.48, th * 0.26); }
        c.fillStyle = 'rgba(0,0,0,0.55)'; c.fillRect(x + 6, y + th - 6 - th * 0.16, tw * 0.5, th * 0.14); c.fillStyle = '#FFFFFF'; c.font = `bold ${th * 0.1}px Arial`; c.textAlign = 'left'; c.textBaseline = 'middle'; c.fillText(labels[i] || '', x + 10, y + th - 6 - th * 0.09); } }, { res: 512, emissive: 0.6 });
    return grp(at(box(w + 0.02, h + 0.02, 0.01, '#3A3D44'), 0, 0, -0.006), pl);
  },
  necktie(o) { // a necktie (knot at y 0, blade hanging down o.len), o.color; attach to a torso joint at the collar, front +Z
    const c = o.color || '#C8322A', L = o.len || 0.26, g = grp(at(box(0.05, 0.04, 0.025, c, { outline: 0.003 }), 0, -0.02, 0), at(box(0.06, L, 0.018, c, { pivot: 'top', outline: 0.003 }), 0, -0.035, 0),
      at(box(0.042, 0.042, 0.018, c), 0, -0.035 - L, 0, 0, 0, PI / 4));   // straight blade with a pointed tip
    return g;
  },
  birthdayCake(o) { // a two-tier birthday cake (pink icing, white drips) with lit candles (flames flicker)
    const g = grp(at(cyl(0.2, 0.2, 0.14, '#F4E3C3', 16, { pivot: 'bottom', outline: 0.004 }), 0, 0, 0), at(cyl(0.205, 0.205, 0.035, '#F29AB8', 16, { pivot: 'bottom' }), 0, 0.12, 0),
      at(cyl(0.13, 0.13, 0.1, '#F4E3C3', 14, { pivot: 'bottom', outline: 0.004 }), 0, 0.155, 0), at(cyl(0.135, 0.135, 0.03, '#F29AB8', 14, { pivot: 'bottom' }), 0, 0.235, 0));
    const flames = [];
    for (let i = 0; i < (o.candles || 5); i++) { const a = i / (o.candles || 5) * TAU, x = Math.cos(a) * 0.07, z = Math.sin(a) * 0.07;
      g.add(at(cyl(0.008, 0.008, 0.07, ['#5FA8D3', '#F2C94C', '#C8322A', '#4CAF50', '#9B6FD0'][i % 5], 6, { pivot: 'bottom' }), x, 0.265, z));
      const f = at(sphere(0.014, '#FFB13B', 1, { emissive: '#FF9A2E' }), x, 0.345, z); f.scale.set(0.7, 1.3, 0.7); g.add(f); flames.push(f); }
    g.userData.update = t => flames.forEach((f, i) => { const k = 1 + 0.18 * Math.sin(t * 17 + i * 1.7); f.scale.set(0.7 * k, 1.3 / k, 0.7 * k); });
    return g;
  },
  problemCloud(o) { // le GPS: one of his "problems": a small grey storm cloud with a face (o.mood 'smug' | 'angry' | 'happy'), bobbing; o.bolt a yellow lightning bolt under it,
    // o.glasses sunglasses, o.suitcase a little suitcase beside it, o.skis two red skis under it, o.belt a seat belt strap; o.size scales it (default 0.7 m wide)
    const k = o.size || 1, r = rng(o.seed || 7), g = grp(), body = grp(); g.add(body);
    const geo = new THREE.IcosahedronGeometry(1, 1), m1 = mat(o.color || '#7D8896'), m2 = mat('#6A7482');
    [[0, 0, 0, 0.3], [-0.22, -0.04, 0.02, 0.22], [0.22, -0.03, 0.01, 0.23], [-0.1, 0.12, -0.02, 0.2], [0.12, 0.13, -0.01, 0.21], [0, -0.1, 0.04, 0.24]].forEach(([x, y, z, rr], i) => { const mm = mesh(geo, i % 3 ? m1 : m2); mm.position.set(x * k, y * k, z * k); mm.scale.set(rr * k * 1.1, rr * k * 0.85, rr * k * 0.95); body.add(mm); });
    const fz = 0.27 * k, eye = (x) => grp(at(sphere(0.055 * k, '#FFFFFF', 1), x * k, 0.03 * k, fz), at(sphere(0.026 * k, '#1C1C20', 1), x * k + (o.look || 0) * 0.012 * k, 0.025 * k, fz + 0.04 * k));
    body.add(eye(-0.085), eye(0.085));
    const mood = o.mood || 'smug', bc = '#2A2E35';
    for (const sd of [-1, 1]) { const b = at(box(0.09 * k, 0.018 * k, 0.02 * k, bc), sd * 0.085 * k, 0.1 * k, fz + 0.02 * k); b.rotation.z = sd * (mood === 'angry' ? -0.45 : mood === 'happy' ? 0.25 : -0.15); body.add(b); }
    const mouth = at(box(0.1 * k, 0.018 * k, 0.02 * k, bc), 0.01 * k, -0.06 * k, fz + 0.03 * k); mouth.rotation.z = mood === 'smug' ? 0.25 : 0; body.add(mouth);
    if (mood === 'happy') { mouth.scale.set(1.2, 2.5, 1); }
    if (o.glasses) body.add(at(box(0.25 * k, 0.05 * k, 0.02 * k, '#111114'), 0, 0.035 * k, fz + 0.06 * k), at(box(0.3 * k, 0.012 * k, 0.012 * k, '#111114'), 0, 0.055 * k, fz + 0.055 * k));
    if (o.bolt) { const sh = new THREE.Shape([[0, 0], [0.06, 0], [0.02, -0.08], [0.07, -0.08], [-0.03, -0.22], [0.0, -0.11], [-0.05, -0.11]].map(([x, y]) => new THREE.Vector2(x * k, y * k))); body.add(at(new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: 0.02 * k, bevelEnabled: false }), mat('#F2C94C', { emissive: '#B8860B' })), 0.02 * k, -0.25 * k, 0.05 * k)); }
    if (o.suitcase) g.add(at(box(0.22 * k, 0.16 * k, 0.08 * k, '#8A5A34', { outline: 0.004 }), 0.33 * k, -0.28 * k, 0.05 * k), at(torus(0.03 * k, 0.008 * k, '#3A2210', 4, 10), 0.33 * k, -0.18 * k, 0.05 * k));
    if (o.skis) for (const sd of [-1, 1]) { g.add(at(box(0.05 * k, 0.012 * k, 1.0 * k, '#C8322A', { outline: 0.003 }), sd * 0.09 * k, -0.33 * k, 0.05 * k), at(box(0.05 * k, 0.03 * k, 0.06 * k, '#C8322A'), sd * 0.09 * k, -0.32 * k, 0.55 * k, 0.5, 0, 0));
      g.add(rod([sd * 0.3 * k, -0.05 * k, 0.1 * k], [sd * 0.36 * k, -0.42 * k, -0.15 * k], 0.006 * k, '#2F3540')); }
    if (o.belt) body.add(at(box(0.5 * k, 0.04 * k, 0.03 * k, '#2F3540'), 0, -0.13 * k, 0.24 * k, 0, 0, 0.5));
    if (o.ticket) g.add(at(label('VOL 404', 0.16 * k, 0.07 * k, { bg: '#F4F1E8', fg: '#2C4A8A' }), -0.36 * k, -0.06 * k, 0.12 * k, 0, 0, 0.25));
    const ph = r() * TAU; g.userData.update = t => { body.position.y = 0.035 * k * Math.sin(t * 2.2 + ph); body.rotation.z = 0.05 * Math.sin(t * 1.6 + ph); };
    g.userData.update(0); return g;
  },
  gpsScreen(o) { // a big GPS screen (o.w wide) with a bezel: top bar instruction (o.text), a map with a route to o.dest (white callout on a red pin) and an arrow;
    // o.long: a dead-straight route running off the top with a big distance readout (o.km) and a tiny right turn at the far end; o.recalc: a « RECALCUL… » overlay;
    // o.off: a black screen; o.offAt: the picture collapses like an old TV (to a line, then a dot) at that time
    const w = o.w || 0.5, h = w * 0.62, pl = canvasPlane(w, h, (c, W, H) => {
      if (o.off) { c.fillStyle = '#0E1012'; c.fillRect(0, 0, W, H); return; }
      c.fillStyle = '#A6D1A8'; c.fillRect(0, 0, W, H); c.fillStyle = '#7FB585'; for (let i = 0; i < 6; i++) c.fillRect(W * (0.05 + i * 0.17), H * (0.3 + (i % 3) * 0.18), W * 0.1, H * 0.12);
      const road = (pts, lw, col) => { c.strokeStyle = col; c.lineWidth = lw; c.beginPath(); pts.forEach(([x, y], k) => k ? c.lineTo(x * W, y * H) : c.moveTo(x * W, y * H)); c.stroke(); };
      const R = o.long ? [[0.5, 1.05], [0.5, 0.27], [0.56, 0.27]] : [[0.5, 1.05], [0.5, 0.62], [0.82, 0.4]];
      road(R, H * 0.06, '#F1EDE2'); road(R, H * 0.035, '#2F7BD8');
      if (o.long) { c.fillStyle = '#1E2229'; c.beginPath(); c.roundRect(W * 0.6, H * 0.45, W * 0.36, H * 0.22, H * 0.04); c.fill(); c.fillStyle = '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle';
        c.font = `900 ${H * 0.11}px Arial`; c.fillText(o.km || '3000 km', W * 0.78, H * 0.56); c.fillStyle = '#C8322A'; c.beginPath(); c.moveTo(W * 0.56, H * 0.24); c.lineTo(W * 0.6, H * 0.27); c.lineTo(W * 0.56, H * 0.3); c.fill(); }
      if (o.dest) { const px = W * 0.83, py = H * 0.41; c.fillStyle = '#C8322A'; c.beginPath(); c.arc(px, py, H * 0.05, 0, TAU); c.fill(); c.beginPath(); c.moveTo(px - H * 0.035, py + H * 0.02); c.lineTo(px, py + H * 0.1); c.lineTo(px + H * 0.035, py + H * 0.02); c.fill();
        c.font = `900 ${H * 0.1}px Arial`; const tw = c.measureText(o.dest).width, bx = Math.min(W - tw - H * 0.12, px - tw / 2 - H * 0.06), by = H * 0.52;
        c.fillStyle = '#FFFFFF'; c.strokeStyle = '#1C252A'; c.lineWidth = H * 0.012; c.beginPath(); c.roundRect(bx, by, tw + H * 0.12, H * 0.15, H * 0.04); c.fill(); c.stroke();
        c.fillStyle = '#C8322A'; c.textAlign = 'left'; c.textBaseline = 'middle'; c.fillText(o.dest, bx + H * 0.06, by + H * 0.077); }
      c.fillStyle = '#2F7BD8'; c.beginPath(); c.moveTo(W * 0.5, H * 0.72); c.lineTo(W * 0.56, H * 0.86); c.lineTo(W * 0.44, H * 0.86); c.closePath(); c.fill();
      c.fillStyle = '#1E2229'; c.fillRect(0, 0, W, H * 0.24); c.fillStyle = '#F6F1E3'; c.textAlign = 'center'; c.textBaseline = 'middle'; const L = String(o.text || '').split('\n');
      let px = H * 0.1; c.font = `900 ${px}px Arial`; const tw = Math.max(...L.map(l => c.measureText(l).width)); if (tw > W * 0.92) { px *= W * 0.92 / tw; c.font = `900 ${px}px Arial`; }
      L.forEach((l, i) => c.fillText(l, W / 2, H * 0.12 + (i - (L.length - 1) / 2) * px * 1.1));
      if (o.recalc) { c.fillStyle = 'rgba(30,34,41,0.75)'; c.fillRect(W * 0.18, H * 0.42, W * 0.64, H * 0.2); c.fillStyle = '#F6F1E3'; c.font = `900 ${H * 0.09}px Arial`; c.fillText('RECALCUL…', W / 2, H * 0.52); } }, { res: 640, emissive: 0.6 });
    const black = at(box(w, h, 0.004, '#0E1012'), 0, 0, -0.003), line = at(box(w, h * 0.04, 0.002, '#FFFFFF', { emissive: '#FFFFFF' }), 0, 0, 0.002); line.visible = false;
    const g = grp(at(box(w + 0.05, h + 0.05, 0.035, '#1E1E22', { outline: 0.006 }), 0, 0, -0.02), black, pl, line, at(sphere(0.012, '#34C759', 1, { emissive: '#34C759' }), w / 2 + 0.008, -h / 2 - 0.012, 0.0));
    g.userData.update = t => { if (o.offAt == null) return; const u = t - o.offAt; if (u < 0) { pl.visible = true; line.visible = false; pl.scale.set(1, 1, 1); return; }
      if (u < 0.12) { pl.visible = true; pl.scale.set(1, Math.max(0.02, 1 - u / 0.12), 1); line.visible = false; }
      else if (u < 0.26) { pl.visible = false; line.visible = true; line.scale.set(Math.max(0.02, 1 - (u - 0.12) / 0.14), 1, 1); }
      else { pl.visible = false; line.visible = u < 0.34; line.scale.set(0.02, 1, 1); } };
    g.userData.update(0); return g;
  },
  robotVacuum(o) { // l'aspirateur: a round robot vacuum (r 0.17) with two glowing LED eyes on its front (+Z), spinning side brushes, a status light
    // (o.low: red light + sleepy half-closed eyes), o.mood 'happy' | 'menace' | 'tired'; o.suckAt: a white suction swirl in front of its mouth from that time
    // (o.suckUntil); o.binWindow: a clear window on top showing a seated cat-silhouette (« le chat va bien »)
    const R = 0.17, H = 0.085, g = grp(), body = grp(); g.add(body);
    body.add(at(cyl(R, R, H, o.color || '#2B2F36', 28, { pivot: 'bottom', outline: 0.004 }), 0, 0.012, 0), at(cyl(R * 0.98, R * 0.98, 0.006, '#C9CED4', 28), 0, H + 0.012, 0),
      at(cyl(R * 0.9, R * 0.9, 0.004, o.color || '#2B2F36', 28), 0, H + 0.016, 0));
    const bump = new THREE.Mesh(new THREE.CylinderGeometry(R * 1.01, R * 1.01, H * 0.6, 28, 1, true, -PI * 0.42, PI * 0.84), mat('#9AA3AD', { doubleSide: true })); bump.position.set(0, 0.012 + H * 0.45, 0); body.add(bump);
    body.add(at(box(R * 0.9, 0.01, 0.02, '#111316'), 0, 0.02, R * 0.95));   // mouth slot
    const mood = o.mood || 'happy', ec = o.low ? '#FF5A3C' : '#6FF2E4', eyes = grp();
    for (const sd of [-1, 1]) { const e = at(box(0.045, mood === 'tired' || o.low ? 0.008 : 0.024, 0.006, ec, { emissive: ec }), sd * 0.055, H * 0.62 + 0.012, R * 1.0); e.rotation.z = mood === 'menace' ? sd * -0.35 : 0; eyes.add(e); }
    body.add(eyes);
    const light = at(sphere(0.012, o.low ? '#FF3B30' : '#34C759', 1, { emissive: o.low ? '#FF3B30' : '#34C759' }), 0, H + 0.02, R * 0.55); body.add(light);
    if (o.binWindow) { body.add(at(cyl(R * 0.5, R * 0.5, 0.006, '#BFE3EE', 20), 0, H + 0.02, -R * 0.15)); body.add(at(box(0.05, 0.04, 0.03, '#E0A35A'), 0, H + 0.04, -R * 0.15), at(box(0.035, 0.03, 0.025, '#E0A35A'), 0, H + 0.065, -R * 0.12)); }
    const brushes = [-1, 1].map(sd => { const b = grp(); for (let i = 0; i < 3; i++) { const a = at(box(0.07, 0.003, 0.006, '#D9D2C2'), 0, 0, 0); a.position.set(0.035 * Math.cos(i * TAU / 3), 0, 0.035 * Math.sin(i * TAU / 3)); a.rotation.y = -i * TAU / 3; b.add(a); }
      b.position.set(sd * R * 0.72, 0.006, R * 0.68); body.add(b); return b; });
    const swirl = grp(); for (let i = 0; i < 4; i++) { const t = new THREE.Mesh(new THREE.TorusGeometry(0.03 + i * 0.018, 0.0025, 4, 20, PI * 1.2), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.45 - i * 0.09, depthWrite: false })); t.rotation.y = PI / 2; t.position.set(0, 0.035, R + 0.02 + i * 0.035); swirl.add(t); }
    body.add(swirl);
    g.userData.update = t => { brushes.forEach((b, i) => { b.rotation.y = (i ? -1 : 1) * t * 18; });
      const on = o.suckAt != null && t >= o.suckAt && (o.suckUntil == null || t < o.suckUntil); swirl.visible = on; swirl.children.forEach((r, i) => { r.rotation.x = t * 9 + i; });
      light.visible = !o.low || Math.floor(t * 3) % 2 === 0; body.position.y = o.idleBob ? 0.004 * Math.sin(t * 11) : 0; };
    g.userData.update(0); return g;
  },
  chargingDock(o) { // the robot vacuum's charging base (front +Z): a slanted back with a green/red light and two contacts
    const g = grp(at(box(0.22, 0.012, 0.12, '#2B2F36', { pivot: 'bottom', outline: 0.004 }), 0, 0, 0.04), at(box(0.22, 0.12, 0.06, '#2B2F36', { pivot: 'bottom', outline: 0.004 }), 0, 0, -0.03, -0.25, 0, 0),
      at(sphere(0.01, o.low ? '#FF3B30' : '#34C759', 1, { emissive: o.low ? '#FF3B30' : '#34C759' }), 0, 0.1, 0.0));
    for (const sd of [-1, 1]) g.add(at(box(0.03, 0.01, 0.02, '#D9B85A'), sd * 0.05, 0.03, 0.02));
    return g;
  },
  armyTank(o) { // a low-poly army tank (front +Z), olive with a white star; o.len ~ 1 (scale it); turret faces front
    const c = o.color || '#5E6B3A', d = '#2F3324', g = grp();
    g.add(at(box(0.5, 0.14, 0.9, c, { pivot: 'bottom', outline: 0.01 }), 0, 0.1, 0), at(box(0.4, 0.06, 0.2, c, { taper: { x: 1, z: 0.6 } }), 0, 0.27, 0.42));
    for (const sd of [-1, 1]) { g.add(at(box(0.12, 0.16, 0.98, d, { pivot: 'bottom', outline: 0.008 }), sd * 0.3, 0, 0)); for (let i = 0; i < 5; i++) g.add(at(cyl(0.055, 0.055, 0.13, '#4A4F3A', 10), sd * 0.3, 0.06, -0.36 + i * 0.18, 0, 0, PI / 2)); }
    const tur = grp(at(box(0.32, 0.12, 0.36, c, { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(cyl(0.025, 0.03, 0.55, c, 8), 0, 0.06, 0.42, PI / 2, 0, 0), at(cyl(0.05, 0.05, 0.03, d, 8), 0, 0.12, -0.05));
    tur.position.y = 0.24; g.add(tur);
    const st = canvasPlane(0.14, 0.14, (cc, W, Hh) => { cc.clearRect(0, 0, W, Hh); cc.fillStyle = '#F4F1E8'; cc.beginPath(); for (let i = 0; i < 10; i++) { const a = -PI / 2 + i * PI / 5, rr = i % 2 ? W * 0.2 : W * 0.48; cc.lineTo(W / 2 + rr * Math.cos(a), Hh / 2 + rr * Math.sin(a)); } cc.closePath(); cc.fill(); }, { res: 128, transparent: true });
    st.rotation.y = PI / 2; st.position.set(0.161, 0.3, 0.0); tur.add(st);
    return g;
  },
  townHall(o) { // « MAIRIE »: a pale stone town hall (front +Z, o.w wide): steps, columns, pediment with a clock, the name, a French flag on top
    const W = o.w || 6, H = o.h || 4.5, D = o.d || 4, g = grp(), st = '#EDE4D0';
    g.add(at(box(W, H, D, st, { pivot: 'bottom', outline: 0.03 }), 0, 0, 0), at(box(W + 0.4, 0.25, D + 0.6, '#D9CDB4', { pivot: 'bottom' }), 0, 0, 0.1), at(box(W * 0.5, 0.15, 0.6, '#D9CDB4', { pivot: 'bottom' }), 0, 0.25, D / 2 + 0.3));
    for (let i = 0; i < 6; i++) g.add(at(cyl(0.16, 0.18, H * 0.72, '#F6F1E3', 10, { pivot: 'bottom', outline: 0.01 }), -W * 0.36 + i * W * 0.144, 0.25, D / 2 + 0.25));
    g.add(at(box(W + 0.2, 0.35, D + 0.7, '#E2D8C4'), 0, H * 0.75, 0.15));
    const ped = new THREE.Mesh(new THREE.CylinderGeometry(0.01, W * 0.62, H * 0.32, 3, 1), mat('#E2D8C4')); ped.rotation.y = PI / 2; ped.scale.set(1, 1, 0.12); ped.position.set(0, H * 0.75 + 0.18 + H * 0.16, D / 2 + 0.25); g.add(ped);
    g.add(at(sign(o.text || 'MAIRIE', W * 0.55, 0.55, '#1C2E4A', '#F4F1E8'), 0, H * 0.75, D / 2 + 0.52));
    g.add(at(cyl(0.32, 0.32, 0.05, '#F4F1E8', 18), 0, H * 0.75 + 0.62, D / 2 + 0.3, PI / 2, 0, 0), at(box(0.03, 0.22, 0.01, '#1C252A'), 0, H * 0.75 + 0.69, D / 2 + 0.34), at(box(0.16, 0.03, 0.01, '#1C252A'), 0.06, H * 0.75 + 0.62, D / 2 + 0.34));
    g.add(rod([0, H, 0], [0, H + 2.2, 0], 0.035, '#8C949A'));
    ['#2F62B5', '#F4F4F0', '#E0413A'].forEach((c, i) => g.add(at(box(0.36, 0.7, 0.02, c), 0.18 + i * 0.36, H + 1.75, 0)));
    return g;
  },
  sockPair(o) { // two striped socks (L-shaped), lying or flying
    const g = grp(); [[-0.06, '#C8322A'], [0.06, '#2F62B5']].forEach(([x, c]) => { g.add(at(box(0.06, 0.03, 0.22, c, { outline: 0.003 }), x, 0.015, 0), at(box(0.06, 0.03, 0.1, c, { outline: 0.003 }), x, 0.015, 0.14, 0, 0.5, 0), at(box(0.062, 0.032, 0.03, '#F4F1E8'), x, 0.015, -0.09)); });
    return g;
  },
};
