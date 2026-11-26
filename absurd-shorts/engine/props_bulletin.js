// « Le bulletin » (story 110, cycle 58): this man found his primary-school report: « Peut mieux faire ». Thirty years on he goes back to school, gets
// gold stars everywhere, and the same teacher stamps « Peut mieux faire » again without looking up from her knitting. Every report in the country
// carries the same crooked red stamp; the grown-ups go back to school, the kindergarten runs the offices, and the teacher's drawer holds forty years
// of unread papers. At last she reads one, his, and writes it by hand: « Peut mieux faire. »
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time. Every name
// starts with `bu`. No figure anywhere (no digit on a board, a clock or a report), no flag, emblem or upright cross; the only words are those of the
// reports: « PEUT MIEUX FAIRE » (one shared stamp texture), « Très bien », and the handwritten « Peut mieux / faire. ».
import * as THREE from 'three';
import { box, cyl, sphere, mat, addOutline } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
function kv(keys, t, def = 0) {
  if (keys == null) return def;
  if (typeof keys === 'number') return keys;
  if (!keys.length) return def;
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) { const [a, va] = keys[i], [b, vb] = keys[i + 1]; if (t < b) return va + (vb - va) * smooth((t - a) / Math.max(1e-4, b - a)); }
  return keys[keys.length - 1][1];
}
const bump = (ts, t, k = 9, f = 28) => (ts || []).reduce((s, t0) => { const u = t - t0; return u > 0 && u < 0.8 ? s + Math.exp(-k * u) * Math.cos(u * f) : s; }, 0);

// THE stamp: « PEUT MIEUX FAIRE », red, tilted to the right, sized with measureText to the sheet's width, a big ink blot on the last letter. One
// function for every report and sheet: they must all carry exactly the same mark
function drawStamp(c, W, H, y0) {
  c.save(); c.translate(W * 0.47, y0); c.rotate(-0.1); const txt = 'PEUT MIEUX FAIRE'; let fs = H * 0.12; c.font = `bold ${fs}px Arial Black, Arial`;
  const tw = c.measureText(txt).width, target = W * 0.8; fs *= target / tw; c.font = `bold ${fs}px Arial Black, Arial`;
  const w2 = c.measureText(txt).width; c.fillStyle = 'rgba(200,24,28,0.92)'; c.strokeStyle = 'rgba(200,24,28,0.92)'; c.lineWidth = fs * 0.09; c.textBaseline = 'middle';
  c.strokeRect(-w2 / 2 - fs * 0.25, -fs * 0.7, w2 + fs * 0.5, fs * 1.4); c.fillText(txt, -w2 / 2, fs * 0.04);
  const lastW = c.measureText('E').width, bx = w2 / 2 - lastW * 0.45; c.beginPath(); c.arc(bx, fs * 0.1, fs * 0.42, 0, TAU); c.fill();   // the blot on the last letter
  for (let i = 0; i < 5; i++) { c.beginPath(); c.arc(bx + Math.cos(i * 1.3) * fs * 0.55, fs * 0.1 + Math.sin(i * 1.3) * fs * 0.5, fs * (0.08 + 0.05 * (i % 2)), 0, TAU); c.fill(); }
  c.restore();
}
function scribbleRows(c, W, H, n, y0, y1) { c.strokeStyle = 'rgba(110,110,110,0.75)'; c.lineWidth = H * 0.008; for (let r = 0; r < n; r++) { const y = y0 + (y1 - y0) * r / Math.max(1, n - 1); c.beginPath(); c.moveTo(W * 0.1, y); for (let x = W * 0.1; x < W * (0.62 + 0.25 * hsh(r)); x += W * 0.02) c.lineTo(x, y + Math.sin(x * 0.11 + r) * H * 0.006); c.stroke(); } }
function star(c, x, y, R) { c.beginPath(); for (let i = 0; i < 10; i++) { const a = -PI / 2 + i * PI / 5, r = i % 2 ? R * 0.45 : R; c.lineTo(x + Math.cos(a) * r, y + Math.sin(a) * r); } c.closePath(); c.fill(); c.strokeStyle = '#B8860B'; c.lineWidth = R * 0.1; c.stroke(); }

export const BULLETIN_PROPS = {
  // A school report / test sheet (pivot at its middle, faces +Z, portrait): o.state 'old' (yellowed, grey scribble rows), 'new' (three handwritten
  // rows « Très bien »), 'blank', 'stars' (a row of big gold stars, no stamp); o.stamp (default true except 'stars'); o.w (0.42); o.write [t0, t1]:
  // the blue handwriting « Peut mieux / faire. » writes on under the stars, line by line; o.crumple [t0, t1]: crushed into a ball
  buReport(o) {
    const W = o.w ?? 0.42, H = W * 1.36, st = o.state || 'old', g = grp(), k = grp(); g.add(k);
    const pl = canvasPlane(W, H, (c, w, h) => {
      c.fillStyle = st === 'old' ? '#EADBB0' : '#F8F5EC'; c.fillRect(0, 0, w, h); c.strokeStyle = st === 'old' ? '#B89A60' : '#C8C4B8'; c.lineWidth = w * 0.012; c.strokeRect(w * 0.03, w * 0.03, w * 0.94, h - w * 0.06);
      if (st === 'old') { for (let i = 0; i < 40; i++) { c.fillStyle = `rgba(150,110,50,${0.05 + 0.08 * hsh(i)})`; c.beginPath(); c.arc(w * hsh(i + 3), h * hsh(i + 7), w * 0.03 * hsh(i + 11) + 2, 0, TAU); c.fill(); } scribbleRows(c, w, h, 7, h * 0.12, h * 0.58); }
      if (st === 'new') { scribbleRows(c, w, h, 2, h * 0.08, h * 0.13); c.fillStyle = '#1E3A8A'; c.font = `italic ${h * 0.07}px Georgia, serif`; for (let r = 0; r < 3; r++) c.fillText('Très bien', w * 0.14, h * (0.26 + 0.12 * r)); }
      if (st === 'stars') { c.fillStyle = '#F2C230'; for (let i = 0; i < 4; i++) star(c, w * (0.16 + 0.225 * i), h * 0.2, w * 0.09); for (let i = 0; i < 4; i++) star(c, w * (0.16 + 0.225 * i), h * 0.36, w * 0.09); }
      if (o.stamp ?? (st !== 'stars')) drawStamp(c, w, h, h * 0.78);
    }, { res: 768 });
    pl.position.z = 0.002; k.add(pl, at(box(W, H, 0.003, st === 'old' ? '#D8C898' : '#E8E4DA'), 0, 0, -0.001));
    const lines = [];
    if (o.write) for (const [i, txt] of ['Peut mieux', 'faire.'].entries()) {
      const lw = W * 0.86, lh = H * 0.13, tx = canvasPlane(lw, lh, (c, w, h) => { c.fillStyle = '#1E4FC8'; c.font = `italic ${h * 0.8}px "Comic Sans MS", Georgia, cursive`; c.textBaseline = 'middle'; c.fillText(txt, w * 0.02, h * 0.55); }, { res: 768, transparent: true });
      const piv = grp(tx); tx.position.x = lw / 2; piv.position.set(-lw / 2, H * (0.04 - 0.16 * i), 0.005); k.add(piv); lines.push({ piv, tx, i });
    }
    g.userData.update = t => {
      if (o.write) { const [a, b] = o.write, m = (a + b) / 2; for (const L of lines) { const u = L.i === 0 ? clamp01((t - a) / (m - a)) : clamp01((t - m) / (b - m)); L.piv.scale.x = Math.max(0.001, u); L.tx.material.map.repeat.x = Math.max(0.001, u); L.tx.material.map.offset.x = 0; L.tx.visible = u > 0.001; } }
      if (o.crumple) { const u = smooth((t - o.crumple[0]) / Math.max(0.05, o.crumple[1] - o.crumple[0])); k.scale.set(1 - 0.75 * u, 1 - 0.8 * u, 1 + 30 * u); k.rotation.z = 2 * u; }
    };
    g.userData.update(0); return g;
  },
  // A big wooden rubber stamp (pivot at its grip's top; the rubber face toward -Y): a round knob, a turned handle, a wide block with red rubber
  buStamp(o) { return grp(at(sphere(0.045, '#8A5A32', 1, { outline: 0.02 }), 0, -0.02, 0), at(cyl(0.025, 0.035, 0.14, '#A8784A', 8, { outline: 0.02 }), 0, -0.12, 0), at(box(0.2, 0.06, 0.12, '#7A4E2A', { outline: 0.015 }), 0, -0.22, 0), at(box(0.19, 0.02, 0.11, '#C8181C'), 0, -0.26, 0)); },
  // Knitting (pivot at the hands' middle, in the lap; front +Z): two needles, a knitted orange piece between them, a ball of wool; o.click: the needles
  // tick (t-periodic); the scarf is a separate prop (buScarf)
  buKnit(o) {
    const g = grp(), C = '#F07A1E', nl = [], nr = []; const piece = at(box(0.18, 0.1, 0.02, C, { outline: 0.01 }), 0, -0.06, 0.02); g.add(piece);
    for (const s of [-1, 1]) { const n = grp(at(cyl(0.006, 0.006, 0.32, '#C8CED6', 6), 0, 0, 0, 0, 0, s * 1.1), at(sphere(0.012, '#E8C030', 0), s * -0.15, 0.06, 0)); g.add(n); (s < 0 ? nl : nr).push(n); }
    g.add(at(sphere(0.07, C, 1, { outline: 0.02 }), 0.25, -0.2, 0.05));
    g.userData.update = t => { const a = 0.18 * Math.sin(t * 14); nl[0].rotation.z = a; nr[0].rotation.z = -a; piece.position.y = -0.06 - 0.01 * Math.abs(Math.sin(t * 7)); }; g.userData.update(0); return g;
  },
  // The orange scarf (pivot at its start, in the world): a knitted band o.w (0.16) wide along the polyline o.pts [[x, y, z], ...] (world offsets from
  // the pivot), with a rib texture; o.grow [[t, share]]: how much of it is there
  buScarf(o) {
    const pts = (o.pts || [[0, 0, 0], [0, -0.5, 0.2]]).map(p => new THREE.Vector3(...p)), W = o.w ?? 0.16, g = grp(), segs = [];
    const tex = canvasPlane(1, 1, (c, w, h) => { c.fillStyle = '#F07A1E'; c.fillRect(0, 0, w, h); c.strokeStyle = '#D0601A'; c.lineWidth = w * 0.03; for (let i = 0; i < 8; i++) { c.beginPath(); c.moveTo(0, (i + 0.5) * h / 8); c.lineTo(w, (i + 0.5) * h / 8); c.stroke(); } }, { res: 64 }).material;
    for (let i = 0; i < pts.length - 1; i++) { const a = pts[i], b = pts[i + 1], d = b.clone().sub(a), L = d.length(); const m = new THREE.Mesh(new THREE.BoxGeometry(W, 0.025, L), tex); m.position.copy(a).addScaledVector(d, 0.5); m.lookAt(b.clone().add(g.position)); m.lookAt(b); addOutline(m, 0.01); g.add(m); segs.push({ m, L }); }
    const tot = segs.reduce((s, x) => s + x.L, 0);
    g.userData.update = t => { const sh = o.grow ? kv(o.grow, t) : 1; let acc = 0; for (const s of segs) { s.m.visible = acc < sh * tot; acc += s.L; } }; g.userData.update(0); return g;
  },
  // Short white curly perm (attach to the head: pivot at the crown's base): a cap of small white curls
  buPerm(o) { const g = grp(), S = o.s ?? 1; for (let i = 0; i < 26; i++) { const a = hsh(i) * TAU, b = hsh(i + 9) * PI * 0.45; g.add(at(sphere(0.055 * S, '#F4F2EC', 1, { outline: 0.02 }), Math.cos(a) * Math.cos(b) * 0.15 * S, Math.sin(b) * 0.1 * S, Math.sin(a) * Math.cos(b) * 0.13 * S)); } return g; },
  // Half-moon glasses on a chain (attach to the head at the eyes; faces +Z): two half lenses in gold rims and a chain looping down behind
  buHalfMoon(o) {
    const g = grp(); for (const s of [-1, 1]) { const r = new THREE.Mesh(new THREE.TorusGeometry(0.03, 0.004, 4, 12, PI), mat('#C8A030')); r.rotation.z = PI; r.position.x = s * 0.04; g.add(r); const l = new THREE.Mesh(new THREE.CircleGeometry(0.03, 12, PI, PI), new THREE.MeshBasicMaterial({ color: '#DDEEFF', transparent: true, opacity: 0.35 })); l.position.x = s * 0.04; g.add(l); }
    const ch = new THREE.Mesh(new THREE.TorusGeometry(0.11, 0.003, 3, 20, PI), mat('#C8A030')); ch.rotation.set(PI, 0, 0); ch.position.set(0, -0.0, -0.05); ch.rotation.x = PI + 0.3; g.add(ch); return g;
  },
  // A tiny school chair (pivot at the floor, facing +Z): seat 0.32 high; o.color
  buTinyChair(o) { const C = o.color || '#2F62B5', g = grp(at(box(0.3, 0.03, 0.28, C, { outline: 0.01 }), 0, 0.32, 0), at(box(0.3, 0.22, 0.025, C, { outline: 0.01 }), 0, 0.5, -0.13)); for (const x of [-0.13, 0.13]) for (const z of [-0.12, 0.12]) g.add(at(box(0.025, 0.32, 0.025, '#6E726F', { pivot: 'bottom' }), x, 0, z)); return g; },
  // A tiny school desk (pivot at the floor, facing +Z): a top 0.52 high, a shelf under it
  buTinyDesk(o) { const g = grp(at(box(0.62, 0.035, 0.42, '#C99A62', { outline: 0.01 }), 0, 0.52, 0), at(box(0.56, 0.02, 0.36, '#A87A4A'), 0, 0.38, 0)); for (const x of [-0.28, 0.28]) for (const z of [-0.18, 0.18]) g.add(at(box(0.03, 0.52, 0.03, '#6E726F', { pivot: 'bottom' }), x, 0, z)); return g; },
  // The attic (pivot at the floor in the middle, the open side +Z): plank floor, a sloping roof wall at the back-left with one dusty skylight shaft
  buAttic(o) {
    const g = grp(); g.add(at(box(6, 0.05, 5, '#9A7A58', { outline: 0.004 }), 0, -0.025, 0), at(box(6, 2.8, 0.1, '#C8B490', { pivot: 'bottom' }), 0, 0, -2.5));
    const roof = at(box(6, 0.08, 3.2, '#B89A70', { outline: 0.004 }), 0, 2.3, -1.4); roof.rotation.x = 0.6; g.add(roof);
    g.add(at(box(0.7, 0.04, 0.6, '#BCD8EA', { emissive: '#4A6070' }), 0.6, 2.33, -1.38, 0.6, 0, 0)); const beam = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.55, 2.4, 10, 1, true), new THREE.MeshBasicMaterial({ color: '#FFF4D0', transparent: true, opacity: 0.16, depthWrite: false, side: THREE.DoubleSide })); beam.position.set(0.5, 1.2, -0.7); beam.rotation.x = 0.35; g.add(beam);
    for (let i = 0; i < 7; i++) g.add(at(box(6, 0.012, 0.004, '#7A5A3A'), 0, 0.002, -2.2 + i * 0.7));
    return g;
  },
  // A cardboard box (pivot at the floor): o.w (0.55), its four flaps open
  buBox(o) { const W = o.w ?? 0.55, H = W * 0.7, g = grp(at(box(W, H, W * 0.75, '#C8A06A', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0)); for (const [x, z, ry, rx] of [[0, W * 0.375, 0, -0.9], [0, -W * 0.375, 0, 0.9]]) { const f = at(box(W, 0.01, W * 0.3, '#B89058', { outline: 0.01 }), x, H, z + Math.sign(z) * W * 0.12); f.rotation.x = rx; g.add(f); } return g; },
  // The primary classroom (pivot at the floor in the middle, the board wall at -Z): cream walls, a green band, a chalkboard with only a chalk sun drawn
  // on it, two blank posters, a clock with hands only, a window on the left wall, a radiator under it; o.back (-3.2)
  buClass(o) {
    const B = o.back ?? -3.2, g = grp(); g.add(at(box(9, 0.05, 9, '#C9A27A'), 0, -0.025, 0), at(box(9, 3.2, 0.1, '#EDE3C8', { pivot: 'bottom' }), 0, 0, B), at(box(0.1, 3.2, 9, '#EDE3C8', { pivot: 'bottom' }), -4.2, 0, B + 4.5), at(box(9, 1.0, 0.02, '#8FAE9A'), 0, 0.5, B + 0.06));
    const bb = canvasPlane(2.6, 1.1, (c, w, h) => { c.fillStyle = '#2F4A3A'; c.fillRect(0, 0, w, h); c.strokeStyle = 'rgba(245,245,235,0.9)'; c.lineWidth = h * 0.025; c.beginPath(); c.arc(w * 0.5, h * 0.5, h * 0.18, 0, TAU); c.stroke();
      for (let i = 0; i < 10; i++) { const a = i * TAU / 10; c.beginPath(); c.moveTo(w * 0.5 + Math.cos(a) * h * 0.25, h * 0.5 + Math.sin(a) * h * 0.25); c.lineTo(w * 0.5 + Math.cos(a) * h * 0.36, h * 0.5 + Math.sin(a) * h * 0.36); c.stroke(); }
      c.beginPath(); c.arc(w * 0.5 - h * 0.06, h * 0.46, h * 0.02, 0, TAU); c.arc(w * 0.5 + h * 0.06, h * 0.46, h * 0.02, 0, TAU); c.stroke(); c.beginPath(); c.arc(w * 0.5, h * 0.52, h * 0.08, 0.2, PI - 0.2); c.stroke(); }, { res: 512 });
    g.add(at(box(2.76, 1.26, 0.05, '#6B4A2E', { outline: 0.006 }), 0.4, 1.75, B + 0.07), at(bb, 0.4, 1.75, B + 0.105));
    for (const [x, col] of [[-2.4, '#F2E27A'], [2.9, '#9FC6D4']]) g.add(at(box(0.8, 0.55, 0.02, col, { outline: 0.006 }), x, 1.85, B + 0.06));
    const ck = grp(at(cyl(0.22, 0.22, 0.04, '#2A2C30', 20), 0, 0, 0, PI / 2), at(cyl(0.19, 0.19, 0.045, '#F8F5EC', 20), 0, 0, 0.004, PI / 2), at(box(0.014, 0.11, 0.008, '#2A2C30', { pivot: 'bottom' }), 0, 0, 0.03, 0, 0, -2.0), at(box(0.01, 0.16, 0.008, '#2A2C30', { pivot: 'bottom' }), 0, 0, 0.034, 0, 0, 0.4));
    ck.position.set(2.2, 2.65, B + 0.08); g.add(ck);
    g.add(at(box(0.04, 1.3, 1.6, '#BCD8EA', { emissive: '#3A5060' }), -4.14, 1.75, B + 2.6), at(box(0.06, 1.4, 0.06, '#E8E2D4'), -4.12, 1.75, B + 2.6), at(box(0.12, 0.55, 1.3, '#E8E4DA', { pivot: 'bottom', outline: 0.008 }), -4.08, 0.2, B + 2.6));
    for (let i = 0; i < 8; i++) g.add(at(box(0.13, 0.5, 0.03, '#D8D4CA'), -4.0, 0.47, B + 2.05 + i * 0.16));
    return g;
  },
  // The gym (pivot at the floor in the middle, the back wall -Z): a wooden floor, a cream wall, wall bars, a long bench, a ceiling at o.ceil (4.2)
  buGym(o) {
    const B = o.back ?? -3.0, Hc = o.ceil ?? 4.2, g = grp(); g.add(at(box(9, 0.05, 8, '#C08D5A'), 0, -0.025, 0), at(box(9, Hc, 0.1, '#EDE6D2', { pivot: 'bottom' }), 0, 0, B), at(box(9, 0.08, 8, '#D8D4CA'), 0, Hc, 0));
    for (let i = 0; i < 4; i++) { const x = 1.6 + i * 0.6; g.add(at(box(0.06, 2.6, 0.06, '#A8784A', { pivot: 'bottom' }), x, 0, B + 0.1)); } for (let j = 0; j < 12; j++) g.add(at(cyl(0.02, 0.02, 1.9, '#C49A62', 6), 2.5, 0.2 + j * 0.2, B + 0.13, 0, 0, PI / 2));
    g.add(at(box(3.2, 0.06, 0.32, '#B08050', { outline: 0.008 }), o.benchX ?? -1.2, 0.42, o.benchZ ?? -0.6)); for (const dx of [-1.4, 1.4]) g.add(at(box(0.06, 0.42, 0.28, '#5E656D', { pivot: 'bottom' }), (o.benchX ?? -1.2) + dx, 0, o.benchZ ?? -0.6));
    return g;
  },
  // An office (pivot at the floor in the middle, the back wall -Z): grey-blue walls, a door on the right wall at o.doorZ, a window, a big desk with a
  // drawer, a plant; o.open: the door ajar
  buOffice(o) {
    const B = o.back ?? -2.8, g = grp(); g.add(at(box(9, 0.05, 8, '#8A8F96'), 0, -0.025, 0), at(box(9, 3.0, 0.1, '#C8D2DA', { pivot: 'bottom' }), 0, 0, B), at(box(0.1, 3.0, 8, '#C8D2DA', { pivot: 'bottom' }), 3.6, 0, B + 4));
    g.add(at(box(0.06, 2.1, 0.95, '#8A6A45', { pivot: 'bottom', outline: 0.008 }), 3.54, 0, o.doorZ ?? 0.2), at(sphere(0.035, '#D8C060', 1), 3.5, 1.0, (o.doorZ ?? 0.2) - 0.35));
    g.add(at(box(1.6, 1.1, 0.03, '#BCD8EA', { emissive: '#3A5060' }), -1.4, 1.75, B + 0.06), at(box(1.7, 0.06, 0.06, '#E8E2D4'), -1.4, 1.17, B + 0.08));
    if (o.desk !== false) { g.add(at(box(1.6, 0.06, 0.8, '#6A4A2E', { outline: 0.008 }), 0, 0.76, o.deskZ ?? -1.2), at(box(1.5, 0.7, 0.7, '#5A3E26', { pivot: 'bottom', outline: 0.006 }), 0, 0.03, o.deskZ ?? -1.2)); }
    g.add(at(cyl(0.16, 0.12, 0.35, '#B86A3A', 8, { pivot: 'bottom', outline: 0.01 }), -2.6, 0, B + 0.4), at(sphere(0.32, '#4E8A4A', 1, { outline: 0.01 }), -2.6, 0.62, B + 0.4));
    return g;
  },
  // A big desk drawer that slides out and out (pivot at its front's middle, sliding toward +Z): a drawer crammed with stacked papers, each with the
  // stamp; o.out [[t, metres]]
  buDrawer(o) {
    const g = grp(), d = grp(); g.add(d); const N = o.n ?? 26, W = 0.5;
    for (let i = 0; i < N; i++) { const s = grp(at(box(W, 0.14, 0.12, '#8A5A32', { outline: 0.006 }), 0, 0, 0), at(box(W - 0.06, 0.1, 0.11, '#F4F0E4'), 0, 0.03, 0)); s.position.z = -i * 0.12; d.add(s);
      const mk = at(box(0.2, 0.006, 0.05, '#C8181C'), 0.05, 0.081, 0.0, 0, 0.12, 0); s.add(mk); }
    d.add(at(box(W + 0.04, 0.18, 0.03, '#6A4A2E', { outline: 0.008 }), 0, 0, 0.07), at(box(0.12, 0.03, 0.03, '#C8A030'), 0, 0, 0.1));
    g.userData.update = t => { d.position.z = kv(o.out, t); }; g.userData.update(0); return g;
  },
  // A bundle of memos with a plain red wax seal (pivot at its middle, faces +Z): a thick stack of white sheets tied with a cord, a round plain wax seal
  // on top, an unreadable signature scribble; o.w (0.36)
  buMemos(o) {
    const W = o.w ?? 0.36, H = W * 1.3, g = grp(); g.add(at(box(W, H, 0.06, '#F2EEE4', { outline: 0.008 }), 0, 0, -0.03));
    const face = canvasPlane(W, H, (c, w, h) => { c.fillStyle = '#FBF9F2'; c.fillRect(0, 0, w, h); scribbleRows(c, w, h, 6, h * 0.12, h * 0.5); c.strokeStyle = '#1E2E5A'; c.lineWidth = h * 0.012; c.beginPath(); c.moveTo(w * 0.45, h * 0.82);
      for (let i = 0; i < 9; i++) c.bezierCurveTo(w * (0.47 + 0.05 * i), h * (0.72 + 0.1 * hsh(i)), w * (0.5 + 0.05 * i), h * (0.9 - 0.12 * hsh(i + 3)), w * (0.5 + 0.05 * i), h * 0.82); c.stroke(); }, { res: 512 });
    face.position.z = 0.003; g.add(face, at(box(W + 0.01, 0.02, 0.07, '#B89A60'), 0, 0, -0.03));
    const seal = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.065, 0.02, 20), mat('#B8141A')); seal.rotation.x = PI / 2; seal.position.set(-W * 0.22, -H * 0.3, 0.012); addOutline(seal, 0.02); g.add(seal, at(new THREE.Mesh(new THREE.TorusGeometry(0.042, 0.006, 4, 16), mat('#8A0E12')), -W * 0.22, -H * 0.3, 0.023));
    return g;
  },
  // A fountain pen (pivot at its middle, along Y): a dark body, a gold clip and nib; o.cap false: uncapped
  buPen(o) { const g = grp(at(cyl(0.011, 0.011, 0.15, '#1E2E5A', 8, { outline: 0.02 }), 0, 0, 0), at(box(0.004, 0.06, 0.006, '#C8A030'), 0.012, 0.04, 0)); if (o.cap !== false) g.add(at(cyl(0.012, 0.012, 0.06, '#1E2E5A', 8), 0, 0.06, 0)); else g.add(at(new THREE.Mesh(new THREE.ConeGeometry(0.009, 0.03, 6), mat('#C8A030')), 0, -0.09, 0, PI, 0, 0)); return g; },
  // A grey moustache (attach to the head; faces +Z)
  buMoustache(o) { const g = grp(); for (const s of [-1, 1]) { const m = new THREE.Mesh(new THREE.SphereGeometry(0.04, 8, 6), mat(o.color || '#9A9A9A')); m.scale.set(1.3, 0.45, 0.6); m.position.set(s * 0.04, 0, 0); m.rotation.z = s * 0.25; addOutline(m, 0.02); g.add(m); } return g; },
  // A hair cap of another colour and cut (attach to the head: pivot at the crown's base): o.color, o.kind 'flat' (slicked) | 'bald' (a fringe ring)
  buHair(o) { const C = o.color || '#9A9A9A', g = grp(); if (o.kind === 'bald') { const r = new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.045, 6, 16), mat(C)); r.rotation.x = PI / 2; r.position.y = -0.04; g.add(r); } else { const m = new THREE.Mesh(new THREE.SphereGeometry(0.16, 12, 6, 0, TAU, 0, PI / 2), mat(C)); m.scale.set(1.0, 0.35, 0.95); addOutline(m, 0.02); g.add(m); } return g; },
  // A small bright school backpack (pivot at its middle; front +Z is the side against the back): o.color
  buBackpack(o) { const C = o.color || '#E8C030', g = grp(at(box(0.26, 0.3, 0.12, C, { outline: 0.01 }), 0, 0, 0), at(box(0.2, 0.12, 0.03, '#FFFFFF'), 0, -0.05, -0.07)); for (const s of [-1, 1]) g.add(at(box(0.03, 0.3, 0.02, '#3A3D44'), s * 0.08, 0, 0.07)); return g; },
  // A little lunchbox (pivot at its handle's top)
  buLunchbox(o) { return grp(at(box(0.18, 0.12, 0.08, o.color || '#3E8ACC', { outline: 0.01 }), 0, -0.1, 0), at(new THREE.Mesh(new THREE.TorusGeometry(0.035, 0.008, 4, 10, PI), mat('#3A3D44')), 0, -0.04, 0)); },
  // A lollipop lady's sign (pivot at the grip, the pole up +Y): a pole and a plain coloured disc, no word
  buDisc(o) { const g = grp(at(cyl(0.02, 0.02, 1.4, '#E8E4DA', 6, { pivot: 'bottom' }), 0, -0.3, 0)); const d = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.28, 0.03, 24), mat(o.color || '#F2C230')); d.rotation.x = PI / 2; d.position.y = 1.35; addOutline(d, 0.015); g.add(d, at(new THREE.Mesh(new THREE.TorusGeometry(0.27, 0.025, 4, 24), mat('#FFFFFF')), 0, 1.35, 0.017)); return g; },
  // A school gate (pivot at the ground in the middle, along X): plain green railings both sides of an open gate, no lettering, no flag
  buGate(o) { const W = o.w ?? 7, g = grp(); for (let x = -W / 2; x <= W / 2; x += 0.16) { if (Math.abs(x) < 0.7) continue; g.add(at(box(0.03, 1.5, 0.03, '#2E5E3E', { pivot: 'bottom' }), x, 0, 0)); } for (const y of [0.15, 1.4]) for (const s of [-1, 1]) g.add(at(box(W / 2 - 0.7, 0.05, 0.04, '#2E5E3E'), s * (W / 4 + 0.35), y, 0));
    for (const s of [-1, 1]) g.add(at(box(0.12, 1.8, 0.12, '#24482E', { pivot: 'bottom', outline: 0.008 }), s * 0.7, 0, 0)); return g; },
  // A stack of thick binders (pivot at the floor): o.n (4) coloured binders, flat
  buBinders(o) { const g = grp(), n = o.n ?? 4, cols = ['#3E6A9A', '#5EAA4A', '#E8C030', '#8A5AB0']; for (let i = 0; i < n; i++) g.add(at(box(0.36, 0.08, 0.3, cols[i % 4], { outline: 0.008 }), 0.02 * (hsh(i) - 0.5), 0.04 + i * 0.08, 0.02 * (hsh(i + 3) - 0.5), 0, 0.1 * (hsh(i + 5) - 0.5), 0)); return g; },
  // An oversized suit jacket for a child (attach to the torso: pivot at the collar; faces +Z): a big box jacket and two long empty sleeves hanging
  // past the hands; o.color
  buBigJacket(o) { const C = o.color || '#3A4A6A', g = grp(at(box(0.5, 0.62, 0.3, C, { outline: 0.01 }), 0, -0.32, 0), at(box(0.12, 0.2, 0.01, '#F4F1EA'), 0, -0.12, 0.155)); for (const s of [-1, 1]) g.add(at(box(0.13, 0.75, 0.13, C, { pivot: 'top', outline: 0.01 }), s * 0.3, -0.05, 0.02, 0.15, 0, s * 0.12)); return g; },
  // A juice box (pivot at its bottom): a small coloured carton and a straw
  buJuice(o) { return grp(at(box(0.07, 0.11, 0.045, o.color || '#F2A030', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(cyl(0.004, 0.004, 0.08, '#FFFFFF', 4, { pivot: 'bottom' }), 0.02, 0.1, 0)); },
  // A pain au chocolat (pivot at its bottom): a puffed golden roll with two dark stripes
  buPain(o) { const m = new THREE.Mesh(new THREE.CapsuleGeometry(0.035, 0.08, 4, 8), mat('#D89A48')); m.rotation.z = PI / 2; m.position.y = 0.03; addOutline(m, 0.015); return grp(m, at(box(0.012, 0.02, 0.07, '#4A2A14'), -0.025, 0.06, 0), at(box(0.012, 0.02, 0.07, '#4A2A14'), 0.025, 0.06, 0)); },
  // A long boardroom table (pivot at the floor in its middle, length along X): o.len (3.6)
  buTable(o) { const L = o.len ?? 3.6, g = grp(at(box(L, 0.06, 1.1, '#6A4A2E', { outline: 0.006 }), 0, 0.74, 0)); for (const x of [-L / 2 + 0.3, L / 2 - 0.3]) g.add(at(box(0.12, 0.72, 0.7, '#4A3420', { pivot: 'bottom' }), x, 0, 0)); return g; },
  // A wall clock with hands only (pivot at its middle, faces +Z): o.time [[t, hour (0-12)]]: the hands go there; a click at each change
  buClock(o) {
    const g = grp(at(cyl(0.3, 0.3, 0.05, '#2A2C30', 20), 0, 0, 0, PI / 2), at(cyl(0.26, 0.26, 0.055, '#F8F5EC', 20), 0, 0, 0.004, PI / 2)), hh = grp(at(box(0.02, 0.13, 0.01, '#2A2C30', { pivot: 'bottom' }), 0, 0, 0)), mh = grp(at(box(0.013, 0.2, 0.01, '#2A2C30', { pivot: 'bottom' }), 0, 0, 0));
    hh.position.z = 0.035; mh.position.z = 0.04; g.add(hh, mh);
    g.userData.update = t => { let h = 4; for (const [a, v] of o.time || [[0, 4.4]]) if (t >= a) h = v; hh.rotation.z = -h / 12 * TAU; mh.rotation.z = -(h % 1) * TAU; }; g.userData.update(0); return g;
  },
  // A crayon drawing on the wall and the ceiling (pivot at the wall's middle bottom; the wall plane faces +Z, the ceiling part bends out toward +Z at
  // o.h): a fat red arrow that shoots up toward a smiling yellow sun, carries on over the top of the wall and across the ceiling; no digit, no letter
  buArrow(o) {
    const H = o.h ?? 3.0, W = o.w ?? 3.0, D = o.d ?? 2.0, g = grp();
    const wall = canvasPlane(W, H, (c, w, h) => { c.clearRect(0, 0, w, h); c.strokeStyle = '#D02A2A'; c.lineWidth = w * 0.04; c.lineCap = 'round'; c.beginPath(); c.moveTo(w * 0.1, h * 0.95); c.bezierCurveTo(w * 0.4, h * 0.8, w * 0.45, h * 0.4, w * 0.7, h * 0.0); c.stroke();
      c.fillStyle = '#F2C230'; c.beginPath(); c.arc(w * 0.82, h * 0.3, w * 0.12, 0, TAU); c.fill(); c.strokeStyle = '#E09A20'; c.lineWidth = w * 0.015; for (let i = 0; i < 12; i++) { const a = i * TAU / 12; c.beginPath(); c.moveTo(w * 0.82 + Math.cos(a) * w * 0.14, h * 0.3 + Math.sin(a) * w * 0.14); c.lineTo(w * 0.82 + Math.cos(a) * w * 0.2, h * 0.3 + Math.sin(a) * w * 0.2); c.stroke(); }
      c.strokeStyle = '#3A2A1A'; c.lineWidth = w * 0.01; c.beginPath(); c.arc(w * 0.82, h * 0.32, w * 0.06, 0.3, PI - 0.3); c.stroke(); c.fillStyle = '#3A2A1A'; c.beginPath(); c.arc(w * 0.78, h * 0.27, w * 0.012, 0, TAU); c.arc(w * 0.86, h * 0.27, w * 0.012, 0, TAU); c.fill(); }, { res: 768, transparent: true });
    wall.position.set(0, H / 2, 0.01); g.add(wall);
    const ceil = canvasPlane(W, D, (c, w, h) => { c.clearRect(0, 0, w, h); c.strokeStyle = '#D02A2A'; c.lineWidth = w * 0.04; c.lineCap = 'round'; c.beginPath(); c.moveTo(w * 0.7, 0); c.lineTo(w * 0.62, h * 0.85); c.stroke(); c.fillStyle = '#D02A2A'; c.beginPath(); c.moveTo(w * 0.52, h * 0.78); c.lineTo(w * 0.72, h * 0.8); c.lineTo(w * 0.6, h * 0.98); c.closePath(); c.fill(); }, { res: 512, transparent: true });
    ceil.rotation.x = PI / 2; ceil.position.set(0, H - 0.01, D / 2); g.add(ceil); return g;
  },
  // A crumb (pivot at the table)
  buCrumb(o) { return grp(at(sphere(0.012, '#D89A48', 0), 0, 0.01, 0)); },
  // A squared pile of files (pivot at its bottom)
  buFiles(o) { const g = grp(); for (let i = 0; i < (o.n ?? 6); i++) g.add(at(box(0.3, 0.025, 0.22, i % 2 ? '#F4F0E4' : '#E8E2D0', { outline: 0.004 }), 0, 0.0125 + i * 0.026, 0)); return g; },
  // An office desk with a monitor (pivot at the floor in the middle, the user's side +Z)
  buDesk(o) { return grp(at(box(1.3, 0.05, 0.7, '#B8BEC6', { outline: 0.006 }), 0, 0.74, 0), at(box(0.06, 0.74, 0.6, '#6E726F', { pivot: 'bottom' }), -0.6, 0, 0), at(box(0.06, 0.74, 0.6, '#6E726F', { pivot: 'bottom' }), 0.6, 0, 0), at(box(0.5, 0.32, 0.03, '#2A2C30', { outline: 0.006 }), 0, 1.0, -0.2), at(box(0.46, 0.28, 0.01, '#3A6A8A', { emissive: '#1A3A4A' }), 0, 1.0, -0.183), at(box(0.08, 0.1, 0.06, '#2A2C30'), 0, 0.82, -0.2)); },
};
