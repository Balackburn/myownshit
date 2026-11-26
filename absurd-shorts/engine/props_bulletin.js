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
  c.save(); c.translate(W * 0.45, y0); c.rotate(-0.1); const txt = 'PEUT MIEUX FAIRE'; let fs = H * 0.12; c.font = `bold ${fs}px Arial Black, Arial`;
  const tw = c.measureText(txt).width, target = W * 0.7; fs *= target / tw; c.font = `bold ${fs}px Arial Black, Arial`;
  const w2 = c.measureText(txt).width; c.fillStyle = 'rgba(200,24,28,0.92)'; c.strokeStyle = 'rgba(200,24,28,0.92)'; c.lineWidth = fs * 0.09; c.textBaseline = 'middle';
  c.strokeRect(-w2 / 2 - fs * 0.25, -fs * 0.7, w2 + fs * 0.5, fs * 1.4); c.fillText(txt, -w2 / 2, fs * 0.04);
  const bx = w2 / 2 + fs * 0.42; c.beginPath(); c.arc(bx, fs * 0.25, fs * 0.36, 0, TAU); c.fill(); c.beginPath(); c.ellipse(bx - fs * 0.32, fs * 0.36, fs * 0.22, fs * 0.1, 0.3, 0, TAU); c.fill();   // the blot runs off the last letter, beside it (the E stays legible)
  for (let i = 0; i < 5; i++) { c.beginPath(); c.arc(bx + fs * 0.1 + Math.cos(i * 1.3) * fs * 0.45, fs * 0.1 + Math.sin(i * 1.3) * fs * 0.5, fs * (0.08 + 0.05 * (i % 2)), 0, TAU); c.fill(); }
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
      const lw = W * 0.8, lh = H * 0.14, tx = canvasPlane(lw, lh, (c, w, h) => { c.fillStyle = '#1E4FC8'; c.strokeStyle = '#1E4FC8'; c.lineJoin = 'round'; c.lineCap = 'round';
        let fs = h * 0.72; const F = s_ => `italic ${s_}px "DejaVu Sans", Verdana, sans-serif`; c.font = F(fs); let tw = c.measureText(txt).width * 1.12; if (tw > w * 0.9) { fs *= w * 0.9 / tw; c.font = F(fs); tw = c.measureText(txt).width * 1.12; }
        c.lineWidth = fs * 0.075; c.textBaseline = 'alphabetic'; let x = (w - tw) / 2; const by = h * 0.7; let prev = null;   // hand-drawn: letters a little tilted and bobbing, joined at the baseline by round strokes
        for (let i = 0; i < txt.length; i++) { const ch = txt[i], cw = c.measureText(ch).width * 1.12; if (ch === ' ') { prev = null; x += cw; continue; }
          const dy = Math.sin(i * 1.7) * fs * 0.04, rot = Math.sin(i * 2.3) * 0.06;
          if (prev && /[a-z]/.test(ch)) { c.beginPath(); c.moveTo(prev[0], prev[1]); c.quadraticCurveTo((prev[0] + x) / 2, by + fs * 0.08, x + cw * 0.12, by - fs * 0.18 + dy); c.stroke(); }
          c.save(); c.translate(x + cw / 2, by + dy); c.rotate(rot); c.strokeText(ch, -cw / 2.24, 0); c.fillText(ch, -cw / 2.24, 0); c.restore();
          prev = /[a-z]/.test(ch) ? [x + cw * 0.86, by - fs * 0.05 + dy] : null; x += cw; }
      }, { res: 768, transparent: true });   // (round 1) round strokes, centred, inside safe margins
      const piv = grp(tx); tx.position.x = lw / 2; piv.position.set(-lw / 2, H * (-0.08 - 0.16 * i), 0.005); k.add(piv); lines.push({ piv, tx, i });
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
    for (let i = 0; i < pts.length - 1; i++) { const a = pts[i], b = pts[i + 1], d = b.clone().sub(a), L = d.length(); const m = new THREE.Mesh(new THREE.CapsuleGeometry(0.035, Math.max(0.001, L - 0.07), 3, 8), tex); m.geometry.rotateX(PI / 2); m.scale.set(W / 0.07, 1, 1); m.position.copy(a).addScaledVector(d, 0.5); m.lookAt(b.clone().add(g.position)); m.lookAt(b); addOutline(m, 0.01); g.add(m); segs.push({ m, L }); }
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
  buTinyDesk(o) { const g = grp(at(box(0.62, 0.035, 0.42, '#C99A62', { outline: 0.01 }), 0, 0.52, 0), at(box(0.56, 0.02, 0.36, '#A87A4A'), 0, 0.38, 0)); if (o.panel) g.add(at(box(0.6, 0.5, 0.02, '#B08A5A', { outline: 0.008 }), 0, 0.27, 0.2)); for (const x of [-0.28, 0.28]) for (const z of [-0.18, 0.18]) g.add(at(box(0.03, 0.52, 0.03, '#6E726F', { pivot: 'bottom' }), x, 0, z)); return g; },   // o.panel: a front panel down to the floor
  // The attic (pivot at the floor in the middle, the open side +Z): plank floor, a sloping roof wall at the back-left with one dusty skylight shaft
  buAttic(o) {
    const g = grp(); g.add(at(box(6, 0.05, 5, '#9A7A58', { outline: 0.004 }), 0, -0.025, 0), at(box(6, 2.8, 0.1, '#C8B490', { pivot: 'bottom' }), 0, 0, -2.5));
    const roof = at(box(6, 0.08, 3.2, '#B89A70', { outline: 0.004 }), 0, 2.3, -1.4); roof.rotation.x = 0.6; g.add(roof);
    g.add(at(box(0.7, 0.04, 0.6, '#BCD8EA', { emissive: '#4A6070' }), 0.6, 2.33, -1.38, 0.6, 0, 0)); const beam = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.55, 2.4, 10, 1, true), new THREE.MeshBasicMaterial({ color: '#FFF4D0', transparent: true, opacity: 0.16, depthWrite: false, side: THREE.DoubleSide })); beam.position.set(0.5, 1.2, -0.7); beam.rotation.x = 0.35; if (o.beam) g.add(beam);
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
    const BX = o.boardX ?? 0.4; g.add(at(box(2.76, 1.26, 0.05, '#6B4A2E', { outline: 0.006 }), BX, 1.75, B + 0.07), at(bb, BX, 1.75, B + 0.105));   // o.boardX: the board along the back wall
    for (const [x, col] of [[-2.4, '#F2E27A'], [2.9, '#9FC6D4']]) g.add(at(box(0.8, 0.55, 0.02, col, { outline: 0.006 }), x, 1.85, B + 0.06));
    const ck = grp(at(cyl(0.22, 0.22, 0.04, '#2A2C30', 20), 0, 0, 0, PI / 2), at(cyl(0.19, 0.19, 0.045, '#F8F5EC', 20), 0, 0, 0.004, PI / 2), at(box(0.014, 0.11, 0.008, '#2A2C30', { pivot: 'bottom' }), 0, 0, 0.03, 0, 0, -2.0), at(box(0.01, 0.16, 0.008, '#2A2C30', { pivot: 'bottom' }), 0, 0, 0.034, 0, 0, 0.4));
    ck.position.set(2.2, 2.65, B + 0.08); g.add(ck);
    g.add(at(box(0.04, 1.3, 1.6, '#BCD8EA', { emissive: '#3A5060' }), -4.14, 1.75, B + 2.6), at(box(0.06, 1.4, 0.06, '#E8E2D4'), -4.12, 1.75, B + 2.6), at(box(0.12, 0.55, 1.3, '#E8E4DA', { pivot: 'bottom', outline: 0.008 }), -4.08, 0.2, B + 2.6));
    for (let i = 0; i < 8; i++) g.add(at(box(0.13, 0.5, 0.03, '#D8D4CA'), -4.0, 0.47, B + 2.05 + i * 0.16));
    if (o.doorOpen) { const dp = grp(at(box(0.05, 2.1, 0.95, '#8A6A45', { pivot: 'bottom', outline: 0.008 }), 0, 0, -0.475), at(sphere(0.035, '#D8C060', 1), 0.05, 1.0, -0.82)); dp.position.set(-4.1, 0, B + 5.12); dp.rotation.y = -1.15; g.add(dp, at(box(0.02, 2.1, 0.95, '#2E2A26', { pivot: 'bottom' }), -4.14, 0, B + 4.65), at(box(0.08, 0.08, 1.1, '#E8E2D4', { pivot: 'bottom' }), -4.12, 2.1, B + 4.65)); }   // o.doorOpen: the door wide open into the room, a dark corridor beyond
    else g.add(at(box(0.06, 2.1, 0.95, '#8A6A45', { pivot: 'bottom', outline: 0.008 }), -4.12, 0, B + 4.65, 0, 0.0, 0), at(box(0.04, 2.1, 0.1, '#3A2A1A', { pivot: 'bottom' }), -4.1, 0, B + 4.15));   // a door ajar on the left wall (the scarf runs out under it)
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
    for (let i = 0; i < N; i++) { const s = grp(at(box(W, 0.14, 0.12, '#8A5A32', { outline: 0.006 }), 0, 0, 0)); const nj = 3 + Math.floor(hsh(i * 11) * 4); for (let j = 0; j < nj; j++) s.add(at(box(W - 0.06 - 0.06 * hsh(i * 13 + j), 0.012 + 0.02 * hsh(i * 17 + j), 0.15 + 0.05 * hsh(i * 19 + j), ['#F4F0E4', '#E8E2D0', '#EFE6C8', '#DCD6C6'][(i + j) % 4], { outline: 0.004 }), 0.08 * (hsh(i * 7 + j) - 0.5), 0.07 + 0.026 * j + 0.03 * hsh(i), 0.06 * (hsh(i * 3 + j) - 0.5), 0.35 * (hsh(i * 23 + j) - 0.5), 0.3 * (hsh(i * 5 + j) - 0.5), 0.12 * (hsh(i * 29 + j) - 0.5))); s.position.z = -i * 0.12; d.add(s);   // (round 2) uneven heaps of sheets, tilted and overlapping, never a keyboard
      const mk = at(box(0.14, 0.005, 0.04, '#C8181C'), 0.05, 0.095 + 0.026 * (nj - 1) + 0.03 * hsh(i), 0.0, 0, 0.12, 0); s.add(mk); }
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
  buPen(o) { const S = o.s ?? 1, g0 = grp(), g = grp(); g0.add(g); g.scale.setScalar(S); g.add(at(cyl(0.011, 0.011, 0.15, o.color || '#1E2E5A', 8, { outline: 0.02 }), 0, 0, 0), at(box(0.004, 0.06, 0.006, '#C8A030'), 0.012, 0.04, 0)); if (o.cap !== false) g.add(at(cyl(0.012, 0.012, 0.06, '#1E2E5A', 8), 0, 0.06, 0)); else g.add(at(new THREE.Mesh(new THREE.ConeGeometry(0.009, 0.03, 6), mat('#C8A030')), 0, -0.09, 0, PI, 0, 0)); return g0; },
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
    for (const s of [-1, 1]) g.add(at(box(0.42, 2.1, 0.42, '#D8C8A8', { pivot: 'bottom', outline: 0.01 }), s * 0.85, 0, 0), at(box(0.5, 0.12, 0.5, '#B8A888', { pivot: 'bottom', outline: 0.008 }), s * 0.85, 2.1, 0)); return g; },   // (round 2) two stone pillars
  // A plain school front (pivot at the floor in its middle, faces +Z): a long cream wall, a row of windows, a double door, a grey roof; no lettering
  buFacade(o) { const W = o.w ?? 12, H = o.h ?? 4.2, g = grp(at(box(W, H, 0.8, '#EADBB8', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(W + 0.4, 0.3, 1.1, '#7A7E86', { pivot: 'bottom', outline: 0.008 }), 0, H, 0), at(box(1.4, 2.0, 0.05, '#7A5A3A', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0.41), at(box(0.03, 2.0, 0.06, '#4A3420', { pivot: 'bottom' }), 0, 0, 0.43));
    for (const y of [1.0, 2.7]) for (let x = -W / 2 + 0.9; x < W / 2 - 0.5; x += 1.5) { if (y < 2 && Math.abs(x) < 1.0) continue; g.add(at(box(0.9, 1.0, 0.05, '#9CC4DC', { outline: 0.006 }), x, y + 0.5, 0.41), at(box(1.0, 0.08, 0.1, '#F6F0E0'), x, y - 0.02, 0.43)); } return g; },
  // A stack of thick binders (pivot at the floor): o.n (4) coloured binders, flat
  buBinders(o) { const g = grp(), n = o.n ?? 10, cols = ['#7A7E84', '#C8BCA0']; for (let i = 0; i < n; i++) g.add(at(box(0.38, 0.035, 0.3, cols[i % 2], { outline: 0.004 }), 0.015 * (hsh(i) - 0.5), 0.0175 + i * 0.036, 0.015 * (hsh(i + 3) - 0.5), 0, 0.06 * (hsh(i + 5) - 0.5), 0)); return g; },   // (round 2) thin flat slices only (no vertical bar that reads as a figure)
  // An oversized suit jacket for a child (attach to the torso: pivot at the collar; faces +Z): a big box jacket and two long empty sleeves hanging
  // past the hands; o.color
  buBigJacket(o) { const C = o.color || '#3A4A6A', L = o.len ?? 1.0, D = o.depth ?? 0.42, g = grp(at(box(0.56, L, D, C, { outline: 0.01 }), 0, -L / 2, 0.04 + (D - 0.42) / 2), at(box(0.12, 0.2, 0.01, '#F4F1EA'), 0, -0.12, 0.155)); for (const s of [-1, 1]) g.add(at(box(0.13, 0.75 * Math.min(1, L + 0.2), 0.13, C, { pivot: 'top', outline: 0.01 }), s * 0.3, -0.05, 0.02, 0.15, 0, s * 0.12)); return g; },   // o.len: a shorter jacket (kids seated: it stops above the lap)
  // A juice box (pivot at its bottom): a small coloured carton and a straw
  buJuice(o) { return grp(at(box(0.07, 0.11, 0.045, o.color || '#F2A030', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(cyl(0.004, 0.004, 0.08, '#FFFFFF', 4, { pivot: 'bottom' }), 0.02, 0.1, 0)); },
  // A pain au chocolat (pivot at its bottom): a puffed golden roll with two dark stripes
  buPain(o) { const m = new THREE.Mesh(new THREE.CapsuleGeometry(0.035, 0.08, 4, 8), mat('#D89A48')); m.rotation.z = PI / 2; m.position.y = 0.03; addOutline(m, 0.015); return grp(m, at(box(0.012, 0.02, 0.07, '#4A2A14'), -0.025, 0.06, 0), at(box(0.012, 0.02, 0.07, '#4A2A14'), 0.025, 0.06, 0)); },
  // A long boardroom table (pivot at the floor in its middle, length along X): o.len (3.6)
  buTable(o) { const L = o.len ?? 3.6, g = grp(at(box(L, 0.06, 1.1, '#6A4A2E', { outline: 0.006 }), 0, 0.74, 0)); for (const x of [-L / 2 + 0.3, L / 2 - 0.3]) g.add(at(box(0.12, 0.72, 0.7, '#4A3420', { pivot: 'bottom' }), x, 0, 0)); return g; },
  // A wall clock with hands only (pivot at its middle, faces +Z): o.time [[t, hour (0-12)]]: the hands go there; a click at each change
  buClock(o) {
    const g = grp(at(cyl(0.3, 0.3, 0.05, '#2A2C30', 20), 0, 0, 0, PI / 2), at(cyl(0.26, 0.26, 0.055, '#F8F5EC', 20), 0, 0, 0.004, PI / 2)), hh = grp(at(box(0.045, 0.14, 0.012, '#1A1C20', { pivot: 'bottom' }), 0, -0.02, 0)), mh = grp(at(box(0.026, 0.235, 0.012, '#1A1C20', { pivot: 'bottom' }), 0, -0.02, 0), at(cyl(0.03, 0.03, 0.02, '#C83A2A', 10), 0, 0, 0.004, PI / 2));   // (round 2) bold hands, longer minute hand
    hh.position.z = 0.04; mh.position.z = 0.05; g.add(hh, mh); for (let i = 0; i < 12; i++) { const a = i * PI / 6; g.add(at(cyl(0.012, 0.012, 0.01, '#8A8C90', 6), Math.sin(a) * 0.235, Math.cos(a) * 0.235, 0.033, PI / 2)); }   // small grey dots, never a bar
    g.userData.update = t => { let h = 4; for (const [a, v] of o.time || [[0, 4.4]]) if (t >= a) h = v; hh.rotation.z = -h / 12 * TAU; mh.rotation.z = -(h % 1) * TAU; }; g.userData.update(0); return g;
  },
  // A crayon drawing on the wall and the ceiling (pivot at the wall's middle bottom; the wall plane faces +Z, the ceiling part bends out toward +Z at
  // o.h): a fat red arrow that shoots up toward a smiling yellow sun, carries on over the top of the wall and across the ceiling; no digit, no letter
  buArrow(o) {
    const H = o.h ?? 3.0, W = o.w ?? 3.0, D = o.d ?? 2.0, g = grp();
    const wall = canvasPlane(W, H, (c, w, h) => { c.clearRect(0, 0, w, h); c.strokeStyle = '#D02A2A'; c.fillStyle = '#D02A2A'; c.lineWidth = w * 0.045; c.lineCap = 'round'; c.lineJoin = 'round';
      c.beginPath(); c.moveTo(w * 0.08, h * 0.92); c.lineTo(w * 0.22, h * 0.78); c.lineTo(w * 0.3, h * 0.84); c.lineTo(w * 0.42, h * 0.6); c.lineTo(w * 0.5, h * 0.66); c.lineTo(w * 0.62, h * 0.18); c.stroke();   // one stroke, going up
      c.beginPath(); c.moveTo(w * 0.56, h * 0.2); c.lineTo(w * 0.66, h * 0.04); c.lineTo(w * 0.7, h * 0.24); c.closePath(); c.fill();   // its head, attached, pointing up
      c.fillStyle = '#F2C230'; c.beginPath(); c.arc(w * 0.84, h * 0.2, w * 0.1, 0, TAU); c.fill(); c.strokeStyle = '#E09A20'; c.lineWidth = w * 0.015; for (let i = 0; i < 12; i++) { const a = i * TAU / 12; c.beginPath(); c.moveTo(w * 0.84 + Math.cos(a) * w * 0.12, h * 0.2 + Math.sin(a) * w * 0.12); c.lineTo(w * 0.84 + Math.cos(a) * w * 0.17, h * 0.2 + Math.sin(a) * w * 0.17); c.stroke(); }
      c.strokeStyle = '#3A2A1A'; c.lineWidth = w * 0.01; c.beginPath(); c.arc(w * 0.84, h * 0.215, w * 0.05, 0.3, PI - 0.3); c.stroke(); c.fillStyle = '#3A2A1A'; c.beginPath(); c.arc(w * 0.81, h * 0.18, w * 0.01, 0, TAU); c.arc(w * 0.87, h * 0.18, w * 0.01, 0, TAU); c.fill(); }, { res: 768, transparent: true });
    wall.position.set(0, H / 2, 0.01); g.add(wall);
    const ceil = canvasPlane(W, D, (c, w, h) => { c.clearRect(0, 0, w, h); }, { res: 64, transparent: true });
    ceil.rotation.x = PI / 2; ceil.position.set(0, H - 0.01, D / 2); g.add(ceil); return g;
  },
  // A crumb (pivot at the table)
  buCrumb(o) { return grp(at(sphere(0.012, '#D89A48', 0), 0, 0.01, 0)); },
  // A squared pile of files (pivot at its bottom)
  buFiles(o) { const g = grp(); for (let i = 0; i < (o.n ?? 6); i++) g.add(at(box(0.3, 0.025, 0.22, i % 2 ? '#F4F0E4' : '#E8E2D0', { outline: 0.004 }), 0, 0.0125 + i * 0.026, 0)); return g; },
  // An office desk with a monitor (pivot at the floor in the middle, the user's side +Z)
  buDesk(o) { return grp(at(box(1.3, 0.05, 0.7, '#B8BEC6', { outline: 0.006 }), 0, 0.74, 0), at(box(0.06, 0.74, 0.6, '#6E726F', { pivot: 'bottom' }), -0.6, 0, 0), at(box(0.06, 0.74, 0.6, '#6E726F', { pivot: 'bottom' }), 0.6, 0, 0), at(box(0.5, 0.32, 0.03, '#2A2C30', { outline: 0.006 }), 0, 1.0, -0.2), at(box(0.46, 0.28, 0.01, '#3A6A8A', { emissive: '#1A3A4A' }), 0, 1.0, -0.183), at(box(0.08, 0.1, 0.06, '#2A2C30'), 0, 0.82, -0.2)); },
  // A gulp lump (pivot at its middle): a skin-coloured bulge o.r (0.05) seen in a throat
  buLump(o) { const m = new THREE.Mesh(new THREE.SphereGeometry(o.r ?? 0.05, 10, 8), mat(o.color || '#E8B88A')); m.scale.set(1.2, 0.8, 0.9); addOutline(m, 0.02); return grp(m); },
  // A red tie drooping over a desk's edge (pivot at its top): a knot and a blade hanging down; o.droop [[t, rad]]
  buTie(o) { const g = grp(), k = grp(); g.add(k); k.add(at(box(0.07, 0.05, 0.03, '#C8202A', { outline: 0.01 }), 0, 0, 0)); const b = new THREE.Shape(); b.moveTo(-0.03, 0); b.lineTo(0.03, 0); b.lineTo(0.05, -0.32); b.lineTo(0, -0.38); b.lineTo(-0.05, -0.32); b.closePath(); const m = new THREE.Mesh(new THREE.ExtrudeGeometry(b, { depth: 0.015, bevelEnabled: false }), mat('#C8202A')); m.position.y = -0.02; addOutline(m, 0.02); k.add(m);
    g.userData.update = t => { k.rotation.x = kv(o.droop, t); }; g.userData.update(0); return g; },
};
