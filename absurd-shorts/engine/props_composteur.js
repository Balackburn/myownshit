// « Le composteur » (story 106, cycle 57): this man did not punch his train ticket: a fine. So he composts it at the bottom of the garden, with the
// fine. In spring a tree grows: a money tree. The whole country buries train tickets; in autumn every note falls at once; and one morning the fine
// has grown too: an inspector, who asks for his ticket. All along, a shoot in a navy cap grows beside the money tree.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time. Every name
// starts with `co`. No word, figure, currency sign, flag, emblem or cross anywhere: the notes are blank lilac sheets with an empty oval, the ticket a
// pale yellow card with one empty dotted circle, the fine a blank pink slip.
import * as THREE from 'three';
import { box, cyl, sphere, mat, addOutline } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
// a value keyed in time: keys [[t, v], ...] (sorted), eased (smoothstep) between keys; a plain number is a constant
function kv(keys, t, def = 0) {
  if (keys == null) return def;
  if (typeof keys === 'number') return keys;
  if (!keys.length) return def;
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) { const [a, va] = keys[i], [b, vb] = keys[i + 1]; if (t < b) return va + (vb - va) * smooth((t - a) / Math.max(1e-4, b - a)); }
  return keys[keys.length - 1][1];
}
// a damped shake after each time in ts (amplitude a, frequency f, decay k)
const shake = (ts, t, a = 1, f = 40, k = 8) => (ts || []).reduce((s, t0) => { const u = t - t0; return u > 0 && u < 1.2 ? s + a * Math.exp(-k * u) * Math.sin(u * f) : s; }, 0);
// a bounce after each time in ts: 1 at the hit, decaying (for squashes)
const bump = (ts, t, k = 9, f = 28) => (ts || []).reduce((s, t0) => { const u = t - t0; return u > 0 && u < 0.8 ? s + Math.exp(-k * u) * Math.cos(u * f) : s; }, 0);

// a generic banknote: invented pale lilac (autumn: brown), a paler border, an empty oval in the middle; no portrait, figure or sign
function paintNote(c, W, H, brown = false) {
  c.fillStyle = brown ? '#9A6A3E' : '#C9B3E6'; c.fillRect(0, 0, W, H);
  c.strokeStyle = brown ? '#C49A6A' : '#E6DAF4'; c.lineWidth = H * 0.12; c.strokeRect(H * 0.08, H * 0.08, W - H * 0.16, H - H * 0.16);
  c.fillStyle = brown ? '#B4865A' : '#DCCDF0'; c.beginPath(); c.ellipse(W / 2, H / 2, W * 0.16, H * 0.3, 0, 0, TAU); c.fill();
  c.strokeStyle = brown ? '#7A4E2A' : '#A890CC'; c.lineWidth = H * 0.03; c.stroke();
}
// the note texture is self-lit a little: in shade the lilac turned grey-green
const NOTE_TEX = {};
function noteMesh(w, h, brown) { const key = brown ? 'b' : 'l'; if (!NOTE_TEX[key]) NOTE_TEX[key] = canvasPlane(0.3, 0.15, (c, W, H) => paintNote(c, W, H, brown), { res: 128, emissive: 0.45 }); const m = new THREE.Mesh(NOTE_TEX[key].geometry, NOTE_TEX[key].material); m.scale.set(w / 0.3, h / 0.15, 1); return m; }
// the train ticket: pale yellow card, one empty dotted circle
function paintTicket(c, W, H) { c.fillStyle = '#F4E6A0'; c.fillRect(0, 0, W, H); c.strokeStyle = '#D8C470'; c.lineWidth = H * 0.06; c.strokeRect(0, 0, W, H);
  c.setLineDash([H * 0.06, H * 0.05]); c.strokeStyle = '#6A5A2A'; c.lineWidth = H * 0.035; c.beginPath(); c.arc(W * 0.68, H * 0.5, H * 0.24, 0, TAU); c.stroke(); c.setLineDash([]); }
// a navy peaked cap (pivot at its band's bottom): crown, band, black peak; no badge
function capMesh(s = 1, col = '#1E2A44') { const g = grp(at(box(0.46, 0.14, 0.46, col, { outline: 0.02, taper: 1.14 }), 0, 0.11, 0), at(box(0.42, 0.07, 0.42, '#14182A', { outline: 0.02 }), 0, 0.035, 0), at(box(0.38, 0.025, 0.2, '#14161A', { outline: 0.02 }), 0, 0.0, 0.27, 0.22, 0, 0)); g.scale.setScalar(s); return g; }
// a big chrome ticket punch (pivot at the hinge, jaws toward +Y): two chrome jaws, black handles; returns {g, A, B}
function punchMesh(s = 1) { const g = grp(), A = grp(), B = grp(), ch = mat('#D8DDE4', { emissive: '#3A4048' });
  for (const [G, sg] of [[A, 1], [B, -1]]) { const j = new THREE.Mesh(new THREE.BoxGeometry(0.035, 0.16, 0.05), ch); j.position.set(sg * 0.02, 0.08, 0); addOutline(j, 0.03); G.add(j, at(box(0.045, 0.2, 0.05, '#1E2024', { outline: 0.02 }), sg * 0.03, -0.11, 0), at(box(0.07, 0.03, 0.055, '#D8DDE4'), sg * 0.008, 0.165, 0)); g.add(G); }
  g.add(at(cyl(0.025, 0.025, 0.07, '#8A9098', 8), 0, 0, 0, PI / 2, 0, 0)); g.scale.setScalar(s); return { g, A, B }; }
function punchUpdate(A, B, snaps, t) { let open = 0.3; for (const t0 of snaps || []) { const u = t - t0; if (u >= -0.05 && u < 0) open = Math.min(open, 0.3 * (-u / 0.05)); else if (u >= 0 && u < 0.2) open = Math.min(open, 0.3 * (u / 0.2)); } A.rotation.z = -open; B.rotation.z = open; }
// a leafy cluster of low-poly spheres (green), for the bush stages
function leafBall(r, n, seed, col = '#4E9A3A') { const g = grp(); for (let i = 0; i < n; i++) { const a = hsh(seed + i) * TAU, b = (hsh(seed + i + 40) - 0.3) * PI * 0.8, rr = r * (0.55 + 0.35 * hsh(seed + i + 80));
    const s = new THREE.Mesh(new THREE.IcosahedronGeometry(r * (0.38 + 0.2 * hsh(seed + i + 9)), 0), mat(i % 3 ? col : '#62B046')); s.position.set(Math.cos(a) * Math.cos(b) * rr, Math.sin(b) * rr, Math.sin(a) * Math.cos(b) * rr); addOutline(s, 0.02); g.add(s); } return g; }

export const COMPOSTEUR_PROPS = {
  // A mainline carriage seen from inside (pivot at the floor in the middle, length along X, window wall at -Z): grey floor, cream walls, a long
  // window band on the back wall with fields and hedges scrolling past (o.scroll m/s), two rows of blue seats facing each other, a luggage rack
  coCarriage(o) { const L = o.len ?? 6, g = grp(), W = o.w ?? 2.8;
    g.add(at(box(L, 0.06, W, '#8A9096', { outline: 0.006 }), 0, -0.02, 0), at(box(L, 2.5, 0.08, '#ECE6D6', { pivot: 'bottom', outline: 0.006 }), 0, 0, -W / 2), at(box(L, 0.08, W, '#F2EEE4'), 0, 2.5, 0));
    const field = canvasPlane(L * 2, 1.0, (c, Wc, Hc) => { c.fillStyle = '#BFE0F2'; c.fillRect(0, 0, Wc, Hc * 0.45); for (let i = 0; i < 16; i++) { c.fillStyle = ['#8CC060', '#A8CC6A', '#D8C870', '#7AAE58'][i % 4]; c.fillRect(i * Wc / 16, Hc * 0.45, Wc / 16 + 1, Hc * 0.55); }
      c.fillStyle = '#4E8A3A'; for (let i = 0; i < 9; i++) { c.beginPath(); c.ellipse((i + 0.4) * Wc / 9, Hc * 0.45, Wc * 0.03, Hc * 0.12, 0, 0, TAU); c.fill(); } }, { res: 512, emissive: 0.4 });
    field.material.map.wrapS = THREE.RepeatWrapping; field.material.map.repeat.set(0.5, 1);
    field.position.set(0, 1.45, -W / 2 + 0.05); g.add(field);
    for (const y of [0.92, 1.98]) g.add(at(box(L, 0.08, 0.06, '#B9BEC4', { outline: 0.01 }), 0, y, -W / 2 + 0.07));
    for (let x = -L / 2 + 1.0; x < L / 2; x += 1.6) g.add(at(box(0.12, 1.1, 0.07, '#ECE6D6', { outline: 0.006 }), x, 1.45, -W / 2 + 0.08));
    // two pairs of seats facing each other along the window (each seat faces +X or -X), a small table between each pair
    for (const cx of [0, -2.6, 2.6]) { for (const sx of [-1, 1]) { const sg = grp(at(box(0.55, 0.14, 1.1, '#2F5C9E', { outline: 0.01 }), 0, 0.46, 0), at(box(0.14, 0.8, 1.1, '#2F5C9E', { outline: 0.01 }), -0.27, 0.9, 0), at(box(0.12, 0.2, 1.0, '#3E6CB0'), -0.27, 1.38, 0)); sg.position.set(cx + sx * 0.75, 0, -W / 2 + 0.75); sg.rotation.y = sx < 0 ? 0 : PI; g.add(sg); }
      g.add(at(box(0.5, 0.04, 0.6, '#C8B89A', { outline: 0.01 }), cx, 0.75, -W / 2 + 0.45), at(cyl(0.03, 0.03, 0.73, '#5E656D', 6, { pivot: 'bottom' }), cx, 0, -W / 2 + 0.45)); }
    g.add(at(box(L, 0.04, 0.4, '#9AA0A6', { outline: 0.01 }), 0, 2.2, -W / 2 + 0.3));
    g.userData.update = t => { field.material.map.offset.x = (t * (o.scroll ?? 4)) / (L * 2); g.rotation.x = 0.004 * Math.sin(t * 11); };
    g.userData.update(0); return g; },
  // The inspector's big chrome ticket punch (pivot at its hinge, jaws +Y); o.snap [t, ...]: the jaws clack shut and spring open; o.s its size
  coPunch(o) { const { g, A, B } = punchMesh(o.s ?? 1); const w = grp(g); w.userData.update = t => punchUpdate(A, B, o.snap, t); w.userData.update(0); return w; },
  // The train ticket (pivot at its middle, faces +Z): a pale yellow card with one empty dotted circle, nothing printed
  coTicket(o) { const w = o.w ?? 0.3, h = o.h ?? 0.15; return grp(canvasPlane(w, h, paintTicket, { res: 256 }), at(box(w, h, 0.004, '#E8D890'), 0, 0, -0.004)); },
  // The fine (pivot at its middle, faces +Z): a big blank pink slip, nothing printed; o.punchAt: a small hole appears with a jolt
  coFine(o) { const w = o.w ?? 0.24, h = o.h ?? 0.32, g = grp(), k = grp(); g.add(k);
    k.add(canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#F4A8C4'; c.fillRect(0, 0, W, H); c.strokeStyle = '#E486AA'; c.lineWidth = W * 0.05; c.strokeRect(W * 0.04, H * 0.04, W * 0.92, H * 0.92); }, { res: 256 }), at(box(w, h, 0.004, '#E898B8'), 0, 0, -0.004));
    const hole = at(cyl(0.018, 0.018, 0.01, '#3A2A30', 10), w * 0.25, h * 0.36, 0.004, PI / 2, 0, 0); k.add(hole);
    g.userData.update = t => { hole.visible = o.punchAt != null && t >= o.punchAt; const q = o.punchAt != null ? bump([o.punchAt], t) : 0; k.scale.set(1 + 0.08 * q, 1 - 0.1 * q, 1); }; g.userData.update(0); return g; },
  // The hero's back garden (pivot at the middle of the lawn, the house wall behind at z = -o.d/2): a lawn, the pale back wall of the house with a door
  // and a window, low wooden fences left and right, a hedge; o.lawn / o.sky colours (spring, dawn); o.w, o.d
  coGarden(o) { const W = o.w ?? 7, D = o.d ?? 6, g = grp(), lawn = new THREE.Mesh(new THREE.PlaneGeometry(W + 6, D + 6), mat(o.lawn || '#7FB85A')); lawn.rotation.x = -PI / 2; lawn.position.y = 0.012; lawn.receiveShadow = true; g.add(lawn);
    g.add(at(box(W + 2, 3.2, 0.3, o.wall || '#EFE2C8', { pivot: 'bottom', outline: 0.004 }), 0, 0, -D / 2), at(box(1.0, 2.1, 0.06, '#7A5A3C', { pivot: 'bottom', outline: 0.006 }), -1.6, 0, -D / 2 + 0.17), at(box(1.2, 1.0, 0.06, '#BFD8EA', { outline: 0.006 }), 1.2, 1.7, -D / 2 + 0.17), at(box(1.3, 0.08, 0.12, '#F4F1EA', { outline: 0.006 }), 1.2, 1.16, -D / 2 + 0.2));
    for (const sx of [-1, 1]) { for (let z = -D / 2 + 0.3; z < D / 2; z += 0.5) g.add(at(box(0.08, 0.9, 0.08, '#A8845A', { pivot: 'bottom', outline: 0.01 }), sx * W / 2, 0, z)); for (const y of [0.35, 0.75]) g.add(at(box(0.04, 0.08, D, '#B8946A', { outline: 0.006 }), sx * W / 2, y, 0)); }
    g.add(at(box(W, 1.1, 0.5, '#4E8A3A', { pivot: 'bottom', outline: 0.006 }), 0, 0, -D / 2 + 0.45));
    return g; },
  // A row of neighbours' back gardens (pivot at the middle; gardens side by side along X, each o.gw wide, separated by low fences; house backs behind)
  coGardens(o) { const n = o.n ?? 4, gw = o.gw ?? 1.6, D = o.d ?? 4, g = grp(), lawn = new THREE.Mesh(new THREE.PlaneGeometry(n * gw + 8, D + 6), mat('#7FB85A')); lawn.rotation.x = -PI / 2; lawn.position.y = 0.012; g.add(lawn);
    for (let i = 0; i < n; i++) { const x = (i - (n - 1) / 2) * gw; g.add(at(box(gw - 0.05, 2.8, 0.3, ['#EFE2C8', '#E8D4C0', '#E4E0CC', '#EEDACA'][i % 4], { pivot: 'bottom', outline: 0.004 }), x, 0, -D / 2), at(box(0.7, 0.7, 0.05, '#BFD8EA', { outline: 0.006 }), x + 0.2, 1.5, -D / 2 + 0.16));
      const soil = new THREE.Mesh(new THREE.PlaneGeometry(gw * 0.7, 0.7), mat('#7A5434')); soil.rotation.x = -PI / 2; soil.position.set(x, 0.018, -0.1); g.add(soil); }
    for (let i = 0; i <= n; i++) { const x = (i - n / 2) * gw; for (let z = -D / 2 + 0.3; z < D / 2 - 0.5; z += 0.45) g.add(at(box(0.06, 0.6, 0.06, '#A8845A', { pivot: 'bottom', outline: 0.01 }), x, 0, z)); g.add(at(box(0.04, 0.07, D - 0.6, '#B8946A', { outline: 0.006 }), x, 0.45, -0.3)); }
    return g; },
  // A wooden compost bin full of peelings (pivot at its floor middle, faces +Z): slatted plank walls, a heap of peelings in green, orange and brown;
  // o.pat [t, ...]: the heap squashes (patted down)
  coCompost(o) { const g = grp(), k = grp(); for (const [w, d, x, z] of [[1.0, 0.06, 0, 0.47], [1.0, 0.06, 0, -0.47], [0.06, 1.0, 0.47, 0], [0.06, 1.0, -0.47, 0]]) for (let i = 0; i < 4; i++) g.add(at(box(w, 0.14, d, i % 2 ? '#9A7448' : '#8A6640', { outline: 0.01 }), x, 0.08 + i * 0.17, z));
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(at(box(0.08, 0.75, 0.08, '#6E5030', { pivot: 'bottom', outline: 0.01 }), sx * 0.47, 0, sz * 0.47));
    k.position.y = 0.5; g.add(k); k.add(at(sphere(0.42, '#6A4A2C', 1), 0, 0, 0)); k.children[0].scale.y = 0.45;
    for (let i = 0; i < 26; i++) k.add(at(box(0.09 + 0.05 * hsh(i), 0.03, 0.04, ['#8CC060', '#E8842A', '#C8A040', '#F2E8A0', '#7A5434'][i % 5]), (hsh(i + 3) - 0.5) * 0.7, 0.12 + 0.05 * hsh(i + 7), (hsh(i + 5) - 0.5) * 0.7, 0, hsh(i) * PI, 0));
    g.userData.update = t => { const q = bump(o.pat, t, 10, 30); k.scale.set(1 + 0.12 * q, 1 - 0.25 * q, 1 + 0.12 * q); }; g.userData.update(0); return g; },
  // A garden spade (pivot at the end of the grip, the blade toward -Y) with a clod of peelings on it; o.load false: clean
  coSpade(o) { const g = grp(at(cyl(0.025, 0.025, 1.0, '#A8845A', 6, { outline: 0.02 }), 0, -0.5, 0), at(box(0.14, 0.04, 0.04, '#5E3E22', { outline: 0.02 }), 0, 0, 0), at(box(0.2, 0.26, 0.02, '#9AA0A6', { outline: 0.02 }), 0, -1.12, 0));
    if (o.load !== false) g.add(at(sphere(0.1, '#6A4A2C', 1), 0, -1.08, 0.06)); return g; },
  // A trowel (pivot at the grip's end, the blade toward -Y)
  coTrowel(o) { return grp(at(cyl(0.02, 0.02, 0.12, '#A8845A', 6, { outline: 0.02 }), 0, -0.06, 0), at(box(0.07, 0.13, 0.012, '#9AA0A6', { outline: 0.02 }), 0, -0.19, 0)); },
  // A big pink earthworm (pivot at the hole in the soil): o.up [[t0, t1], ...]: it pops up, looks round (to the camera) and goes back down; a ring of
  // dark soil round the hole
  coWorm(o) { const g = grp(), w = grp(); g.add(w); const ring = new THREE.Mesh(new THREE.RingGeometry(0.03, 0.12, 12), mat('#5A3A22')); ring.rotation.x = -PI / 2; ring.position.y = 0.02; g.add(ring);
    for (let i = 0; i < 6; i++) w.add(at(sphere(0.045, i % 2 ? '#E8909A' : '#F0A0AA', 1, { outline: 0.03 }), 0, 0.04 + i * 0.06, 0));
    for (const sx of [-1, 1]) w.add(at(sphere(0.016, '#FFFFFF', 0), sx * 0.022, 0.36, 0.035), at(sphere(0.008, '#14161A', 0), sx * 0.022, 0.36, 0.05));
    g.userData.update = t => { let h = 0; for (const [a, b] of o.up || []) { if (t > a && t < b) h = Math.max(h, Math.min(1, (t - a) / 0.15, (b - t) / 0.15)); } w.position.y = -0.42 * (1 - h); w.visible = h > 0.02; w.rotation.y = 0.5 * Math.sin(t * 3) * h; w.rotation.z = 0.15 * Math.sin(t * 6); }; g.userData.update(0); return g; },
  // A money tree (pivot at the foot of the trunk): a brown trunk, a round crown of generic lilac banknote leaves that flutter; o.s its size; o.grow
  // [[t, s], ...]: it grows (a sapling popping up); o.brown: the autumn notes (brown, curled); o.dropAt: every note falls at once to a ring of heap on
  // the ground round the trunk (opaque), the crown left bare; o.n leaves
  coMoneyTree(o) { const S = o.s ?? 1, g = grp(), k = grp(); g.add(k); const n = o.n ?? 140, R = 0.95;
    k.add(at(cyl(0.09, 0.14, 1.5, '#7A5434', 7, { pivot: 'bottom', outline: 0.02 }), 0, 0, 0)); for (const [a, l] of [[0.6, 0.6], [-0.7, 0.5], [2.4, 0.55]]) k.add(at(cyl(0.035, 0.05, l, '#7A5434', 5, { pivot: 'bottom', outline: 0.02 }), 0, 1.3, 0, 0.7 * Math.sin(a), 0, 0.7 * Math.cos(a)));
    const leaves = []; for (let i = 0; i < n; i++) { const m = noteMesh(0.26, 0.13, !!o.brown); const a = hsh(i) * TAU, b = (hsh(i + 50) - 0.35) * PI * 0.9, rr = R * (0.55 + 0.45 * Math.sqrt(hsh(i + 90)));
      const p = [Math.cos(a) * Math.cos(b) * rr, 2.05 + Math.sin(b) * rr * 0.85, Math.sin(a) * Math.cos(b) * rr]; const r0 = [hsh(i + 3) * PI, hsh(i + 7) * TAU, (hsh(i + 11) - 0.5) * 0.8];
      const d = (hsh(i + 13) - 0.5) * 2, end = [p[0] * (1.1 + 0.9 * hsh(i + 17)) * 0.9, 0.03 + 0.12 * hsh(i + 19), p[2] * (1.1 + 0.9 * hsh(i + 17)) * 0.9];
      if (o.brown) m.scale.z = 1; m.position.set(...p); m.rotation.set(...r0); k.add(m); leaves.push({ m, p, r0, d, end, ph: hsh(i + 23) * TAU }); }
    // the brown notes curl: a second, bent copy would be costly; they read curled through a tilt and a darker edge drawn in the texture
    g.userData.update = t => { const s = o.grow ? kv(o.grow, t, S) : S; k.scale.setScalar(Math.max(0.001, s)); k.visible = s > 0.01;
      const u = o.dropAt != null ? clamp01((t - o.dropAt) / 0.55) : -1;
      for (const L of leaves) { if (u <= 0) { L.m.position.set(L.p[0], L.p[1], L.p[2]); L.m.rotation.set(L.r0[0] + 0.25 * Math.sin(t * 6 + L.ph), L.r0[1], L.r0[2] + 0.2 * Math.sin(t * 5 + L.ph)); }
        else { const e = u * u; L.m.position.set(L.p[0] + (L.end[0] - L.p[0]) * u + 0.15 * L.d * Math.sin(u * PI), L.p[1] + (L.end[1] - L.p[1]) * e, L.p[2] + (L.end[2] - L.p[2]) * u); L.m.rotation.set(L.r0[0] * (1 - u) - PI / 2 * u + 0.4 * L.d * (1 - u), L.r0[1], L.r0[2] * (1 - u)); } } };
    g.userData.update(0); return g; },
  // One leafy lilac money branch (pivot at its cut end, it points +Y): a twig with a dozen lilac note leaves
  coBranch(o) { const g = grp(at(cyl(0.015, 0.025, 0.55, '#7A5434', 5, { pivot: 'bottom', outline: 0.02 }), 0, 0, 0)); for (let i = 0; i < 12; i++) { const m = noteMesh(0.18, 0.09, false); m.position.set((hsh(i) - 0.5) * 0.25, 0.2 + 0.035 * i, (hsh(i + 4) - 0.5) * 0.15); m.rotation.set(hsh(i + 1) * PI, hsh(i + 2) * TAU, 0); g.add(m); } return g; },
  // A single generic banknote (pivot at its middle, faces +Z); o.brown
  coNote(o) { const m = noteMesh(o.w ?? 0.3, (o.w ?? 0.3) / 2, !!o.brown); return grp(m); },
  // The capped shoot that grows beside the money tree (pivot at the soil), one prop in four stages (o.stage): 1 a bright-green shoot under a navy cap
  // half its width; 2 a knee-high bush, a branch ending in a chrome ticket punch (o.snap [t, ...]: it clacks; o.twitch [t, ...]); 3 a man-sized bush
  // shaped like a man in uniform, painted eyes closed (o.openAt: they open; o.burstAt: the leafy shell bursts into a puff of leaves and is gone)
  coShoot(o) { const st = o.stage ?? 1, g = grp(), k = grp(); g.add(k); let A = null, B = null, eyes = null, shell = null, puff = [], arm = null;
    if (st === 1) { k.add(at(cyl(0.012, 0.018, 0.22, '#5EBA3A', 5, { pivot: 'bottom', outline: 0.02 }), 0, 0, 0));
      for (const sx of [-1, 1]) { const l = new THREE.Mesh(new THREE.SphereGeometry(0.06, 8, 6), mat('#6ACC44')); l.scale.set(1.6, 0.35, 0.8); l.position.set(sx * 0.08, 0.18, 0); l.rotation.z = -sx * 0.4; addOutline(l, 0.03); k.add(l); }
      k.add(at(capMesh(0.34), 0, 0.22, 0)); }
    if (st === 2) { const b = leafBall(0.26, 16, 7); b.position.y = 0.32; k.add(b); k.add(at(capMesh(0.42), 0, 0.56, 0.02));
      arm = grp(); arm.position.set(0.2, 0.36, 0.05); k.add(arm); arm.add(at(cyl(0.015, 0.02, 0.3, '#5E8A3A', 5, { pivot: 'bottom', outline: 0.02 }), 0, 0, 0, 0, 0, -0.9));
      const p = punchMesh(0.7); p.g.position.set(0.25, 0.18, 0); p.g.rotation.z = -0.9; arm.add(p.g); A = p.A; B = p.B; }
    if (st === 3) { shell = grp(); k.add(shell); const C = '#4E9A3A';
      const parts = [[0, 1.25, 0, 0.3, 14], [0, 0.95, 0, 0.3, 12], [-0.12, 0.45, 0, 0.16, 8], [0.12, 0.45, 0, 0.16, 8], [-0.12, 0.15, 0, 0.14, 7], [0.12, 0.15, 0, 0.14, 7], [-0.34, 1.1, 0, 0.13, 6], [0.34, 1.1, 0, 0.13, 6], [-0.38, 0.8, 0.03, 0.12, 6], [0, 1.85, 0, 0.24, 10]];
      parts.forEach(([x, y, z, r, nn], i) => { const b = leafBall(r, nn, 30 + i * 13, C); b.position.set(x, y, z); b.scale.y = i === 0 || i === 1 ? 1.25 : 1; shell.add(b); });
      shell.add(at(capMesh(0.85), 0, 2.03, 0.02));
      eyes = []; for (const sx of [-1, 1]) { const e = grp(); e.position.set(sx * 0.09, 1.9, 0.22); shell.add(e); const shut = at(box(0.09, 0.018, 0.01, '#1E2A14'), 0, 0, 0); const open = grp(at(sphere(0.045, '#FFFFFF', 1, { outline: 0.03 }), 0, 0, 0), at(sphere(0.02, '#14161A', 0), 0, 0, 0.035)); e.add(shut, open); eyes.push({ shut, open }); }
      arm = grp(); arm.position.set(0.36, 1.15, 0.05); shell.add(arm); arm.add(at(cyl(0.02, 0.025, 0.4, '#5E8A3A', 5, { pivot: 'bottom', outline: 0.02 }), 0, 0, 0, 0, 0, -0.5));
      const p = punchMesh(1.0); p.g.position.set(0.2, 0.36, 0); p.g.rotation.z = -0.4; arm.add(p.g); A = p.A; B = p.B;
      for (let i = 0; i < 40; i++) { const l = new THREE.Mesh(new THREE.IcosahedronGeometry(0.07 + 0.04 * hsh(i), 0), mat(i % 3 ? '#4E9A3A' : '#62B046')); addOutline(l, 0.02); l.visible = false; g.add(l);
        const a = hsh(i + 1) * TAU, y = 0.2 + 1.9 * hsh(i + 2); puff.push({ l, p0: [0.3 * Math.cos(a), y, 0.2 * Math.sin(a)], v: [Math.cos(a) * (1.2 + hsh(i + 3)), 1.5 + 1.5 * hsh(i + 4), Math.sin(a) * (1.2 + hsh(i + 3)) * 0.6 + 0.5] }); } }
    g.userData.update = t => { k.rotation.z = 0.04 * Math.sin(t * 2.2); if (A) { punchUpdate(A, B, o.snap, t); if (arm) arm.rotation.z = shake(o.snap, t, 0.25, 30, 6) + shake(o.twitch, t, 0.12, 40, 6); }
      if (eyes) { const op = o.openAt != null && t >= o.openAt; for (const e of eyes) { e.shut.visible = !op; e.open.visible = op; } }
      if (shell) { const u = o.burstAt != null ? t - o.burstAt : -1; shell.visible = u < 0; if (u < 0 && o.openAt != null) { const q = bump([o.openAt], t); shell.scale.set(1 + 0.05 * q, 1 - 0.04 * q, 1); }
        for (const L of puff) { L.l.visible = u >= 0 && u < 0.9; if (L.l.visible) { L.l.position.set(L.p0[0] + L.v[0] * u, L.p0[1] + L.v[1] * u - 4.5 * u * u, L.p0[2] + L.v[2] * u); L.l.rotation.set(u * 9, u * 7, 0); L.l.scale.setScalar(1 - 0.6 * u); } } } };
    g.userData.update(0); return g; },
  // A big squirrel (pivot at its feet, faces +Z): a russet body, a huge bushy tail curled up behind, a head with ears and black eyes; o.hop [[t0, t1], ...]:
  // it bounces while it moves; o.dig [[t0, t1], ...]: it digs (head down, fast paws); o.cheeks [t0, t1]: cheeks puffed; o.startle t: it leaps back
  coSquirrel(o) { const g = grp(), k = grp(), C = '#B8642E', D = '#8A4A22'; g.add(k);
    const body = new THREE.Mesh(new THREE.SphereGeometry(0.14, 12, 8), mat(C)); body.scale.set(0.9, 1.1, 1.2); body.position.set(0, 0.16, 0); addOutline(body, 0.03); k.add(body);
    const tail = grp(); tail.position.set(0, 0.14, -0.14); k.add(tail); for (let i = 0; i < 7; i++) { const s = new THREE.Mesh(new THREE.SphereGeometry(0.09 + 0.03 * Math.sin(i * 0.6), 10, 7), mat(i % 2 ? C : '#C8743A')); const a = i * 0.42; s.position.set(0, 0.08 + Math.sin(a) * 0.3, -0.06 - (1 - Math.cos(a)) * 0.2 + i * 0.01); addOutline(s, 0.03); tail.add(s); }
    const hd = grp(); hd.position.set(0, 0.32, 0.1); k.add(hd); hd.add(at(sphere(0.09, C, 1, { outline: 0.03 }), 0, 0, 0), at(sphere(0.05, '#F2E2C8', 1), 0, -0.03, 0.06));
    const ch = [-1, 1].map(sx => { const c = at(sphere(0.05, '#C8743A', 1, { outline: 0.03 }), sx * 0.06, -0.02, 0.04); hd.add(c); return c; });
    for (const sx of [-1, 1]) hd.add(at(new THREE.Mesh(new THREE.ConeGeometry(0.03, 0.08, 4), mat(D)), sx * 0.05, 0.1, -0.01), at(sphere(0.018, '#14161A', 0), sx * 0.045, 0.02, 0.075));
    const paws = [-1, 1].map(sx => { const p = at(box(0.04, 0.08, 0.04, D, { outline: 0.03 }), sx * 0.06, 0.12, 0.14); k.add(p); return p; });
    g.userData.update = t => { let y = 0, dig = 0; for (const [a, b] of o.hop || []) if (t > a && t < b) y = Math.abs(Math.sin((t - a) * 14)) * 0.12; for (const [a, b] of o.dig || []) if (t > a && t < b) dig = 1;
      const st = o.startle != null ? t - o.startle : -1; let sy = 0, sz = 0; if (st > 0 && st < 0.5) { sy = Math.sin(st / 0.5 * PI) * 0.35; sz = -0.3 * Math.min(1, st / 0.4); } else if (st >= 0.5) sz = -0.3;
      k.position.set(0, y + sy, sz); hd.rotation.x = dig ? 0.6 : 0.1 * Math.sin(t * 4); for (const [i, p] of paws.entries()) p.position.y = 0.12 + (dig ? 0.04 * Math.sin(t * 40 + i * PI) : 0) - (dig ? 0.06 : 0);
      tail.rotation.x = 0.15 * Math.sin(t * 3) + (st > 0 && st < 0.5 ? 0.6 : 0); const cp = o.cheeks && t > o.cheeks[0] && t < o.cheeks[1]; for (const c of ch) c.scale.setScalar(cp ? 1.7 : 1); k.scale.set(1, 1 + (st > 0 && st < 0.15 ? 0.3 : 0), 1); };
    g.userData.update(0); return g; },
  // A railway platform seen from the platform (pivot at the edge in the middle, the track toward +Z): grey slab, a yellow edge line, a plain wall behind
  // with a plain colour band where a sign would be, a clock with hands only (no figures) on a post, a bench; no name, number or timetable
  coPlatform(o) { const L = o.len ?? 16, D = o.depth ?? 4, g = grp();
    g.add(at(box(L, 1.0, D, '#B9B2A6', { outline: 0.006 }), 0, -0.49, -D / 2), at(box(L, 0.012, 0.16, '#F2C230'), 0, 0.016, -0.25), at(box(L, 0.4, 3.0, '#2A2C30'), 0, -1.2, 1.5));
    g.add(at(box(L, 3.6, 0.2, '#E8E2D4', { pivot: 'bottom', outline: 0.004 }), 0, 0, -D), at(box(L, 0.5, 0.06, '#3E6A9A', { outline: 0.006 }), 0, 2.6, -D + 0.12));
    const ck = grp(); ck.position.set(o.clockX ?? -2.5, 0, o.clockZ ?? -1.6); g.add(ck); ck.add(at(cyl(0.05, 0.05, 2.4, '#3A3D44', 8, { pivot: 'bottom', outline: 0.02 }), 0, 0, 0), at(cyl(0.32, 0.32, 0.08, '#F4F1EA', 20, { outline: 0.03 }), 0, 2.6, 0, PI / 2, 0, 0));
    const hh = at(box(0.03, 0.17, 0.02, '#14161A'), 0, 0.07, 0), mh = at(box(0.02, 0.26, 0.02, '#14161A'), 0, 0.11, 0), hg = grp(hh), mg = grp(mh); hg.position.set(0, 2.6, 0.05); mg.position.set(0, 2.6, 0.06); hg.rotation.z = -2.1; ck.add(hg, mg);
    g.add(at(box(1.6, 0.08, 0.45, '#8A6A45', { outline: 0.01 }), o.benchX ?? 2.5, 0.45, -D + 0.6), at(box(1.6, 0.4, 0.06, '#8A6A45', { outline: 0.01 }), o.benchX ?? 2.5, 0.75, -D + 0.38));
    g.userData.update = t => { mg.rotation.z = -0.3 - t * 0.05; }; g.userData.update(0); return g; },
  // A mainline carriage seen from outside (pivot at the floor in its middle, length along X, side toward +Z): a blue-and-white body, a row of windows
  // showing empty seats, a cab at the +X end with a window (the driver behind it); no logo, number or name; o.len
  coTrain(o) { const L = o.len ?? 9, g = grp(), C = '#F2F0EA', B = '#2E5E9E';
    g.add(at(box(L, 2.6, 2.8, C, { pivot: 'bottom', outline: 0.004 }), 0, 0.3, 0), at(box(L, 0.3, 2.82, B), 0, 0.8, 0), at(box(L, 0.12, 2.82, B), 0, 2.5, 0));
    for (let x = -L / 2 + 0.9; x < L / 2 - 1.6; x += 1.3) { g.add(at(box(1.0, 0.8, 0.02, '#CFE6F4', { emissive: '#4A6A80' }), x, 1.75, 1.41)); g.add(at(box(0.5, 0.45, 0.1, '#2F5C9E', { outline: 0.01 }), x - 0.15, 1.6, 1.32), at(box(0.5, 0.12, 0.1, '#3E6CB0'), x - 0.15, 1.88, 1.32)); }
    const cab = at(box(1.4, 2.4, 2.8, B, { pivot: 'bottom', outline: 0.004, taper: 0.92 }), L / 2 + 0.6, 0.3, 0); g.add(cab, at(box(0.7, 0.7, 0.02, '#CFE6F4', { emissive: '#4A6A80' }), L / 2 + 0.55, 1.85, 1.41));
    for (let x = -L / 2 + 1; x < L / 2 + 1; x += 2.2) g.add(at(cyl(0.35, 0.35, 0.25, '#1E2024', 12), x, 0.35, 1.3, PI / 2, 0, 0));
    return g; },
  // A ticket window (pivot at the floor in the middle, faces +Z): a wall with a glass hatch (the clerk is behind it), a counter with a slot; nothing written
  coHatch(o) { const g = grp(), W = o.w ?? 4;
    g.add(at(box((W - 1.4) / 2, 3, 0.2, '#D8CBB4', { pivot: 'bottom', outline: 0.004 }), -(W + 1.4) / 4, 0, 0), at(box((W - 1.4) / 2, 3, 0.2, '#D8CBB4', { pivot: 'bottom', outline: 0.004 }), (W + 1.4) / 4, 0, 0), at(box(1.4, 1.05, 0.2, '#D8CBB4', { pivot: 'bottom', outline: 0.004 }), 0, 0, 0), at(box(1.4, 0.75, 0.2, '#D8CBB4', { pivot: 'bottom', outline: 0.004 }), 0, 2.25, 0));
    g.add(at(box(1.6, 0.08, 0.5, '#8A6A45', { outline: 0.01 }), 0, 1.07, 0.15), at(box(1.4, 0.06, 0.06, '#5E656D'), 0, 2.25, 0.08), at(box(0.06, 1.2, 0.06, '#5E656D'), -0.7, 1.65, 0.08), at(box(0.06, 1.2, 0.06, '#5E656D'), 0.7, 1.65, 0.08), at(box(0.5, 0.05, 0.12, '#3A3D44'), 0, 1.13, 0.1));
    const glass = new THREE.Mesh(new THREE.BoxGeometry(1.34, 1.1, 0.02), new THREE.MeshLambertMaterial({ color: '#CFE6F4', transparent: true, opacity: 0.18 })); glass.position.set(0, 1.68, 0.06); g.add(glass);
    const room = new THREE.Mesh(new THREE.BoxGeometry(W, 3, 0.1), mat('#E8DCC4')); room.position.set(0, 1.5, -1.6); g.add(room);
    return g; },
  // A blank red price tag (pivot at its middle, faces +Z): a red card with a white string hole; o.w; o.slapAt: it lands with a squash
  coTag(o) { const w = o.w ?? 0.2, h = w * 0.6, g = grp(), k = grp(); g.add(k); k.add(at(box(w, h, 0.01, '#D8322A', { outline: 0.02 }), 0, 0, 0), at(cyl(w * 0.06, w * 0.06, 0.012, '#F4F1EA', 10), -w * 0.38, 0, 0.006, PI / 2, 0, 0));
    g.userData.update = t => { const q = o.slapAt != null ? bump([o.slapAt], t) : 0; k.scale.set(1 + 0.12 * q, 1 - 0.15 * q, 1); k.visible = o.slapAt == null || t >= o.slapAt - 0.02; }; g.userData.update(0); return g; },
  // Rolling hills covered with money trees seen from the air (pivot at the middle): a wavy green ground, o.n round lilac crowns on trunks that sway in
  // waves like a sea; o.w x o.d
  coForest(o) { const W = o.w ?? 40, D = o.d ?? 40, g = grp(), hz = (x, z) => 1.2 * Math.sin(x * 0.25) * Math.cos(z * 0.2) + 0.6 * Math.sin(z * 0.37 + 1);
    const geo = new THREE.PlaneGeometry(W, D, 40, 40); geo.rotateX(-PI / 2); const pa = geo.attributes.position; for (let i = 0; i < pa.count; i++) pa.setY(i, hz(pa.getX(i), pa.getZ(i))); geo.computeVertexNormals(); g.add(new THREE.Mesh(geo, mat('#7FB85A')));
    const tex = canvasPlane(1, 1, (c, Wc, Hc) => { c.fillStyle = '#C9B3E6'; c.fillRect(0, 0, Wc, Hc); for (let i = 0; i < 40; i++) { c.save(); c.translate(hsh(i) * Wc, hsh(i + 1) * Hc); c.rotate(hsh(i + 2) * PI); c.fillStyle = i % 2 ? '#DCCDF0' : '#B49CD6'; c.fillRect(-Wc * 0.07, -Hc * 0.035, Wc * 0.14, Hc * 0.07); c.restore(); } }, { res: 128 }).material;
    const crowns = []; const n = o.n ?? 160; for (let i = 0; i < n; i++) { const x = (hsh(i) - 0.5) * W * 0.9, z = (hsh(i + 7) - 0.5) * D * 0.9, y = hz(x, z), s = 0.8 + 0.5 * hsh(i + 3);
      g.add(at(cyl(0.12 * s, 0.16 * s, 1.0 * s, '#7A5434', 5, { pivot: 'bottom' }), x, y, z)); const c = new THREE.Mesh(new THREE.IcosahedronGeometry(1.0 * s, 1), tex); c.position.set(x, y + 1.6 * s, z); addOutline(c, 0.015); g.add(c); crowns.push({ c, x, z, y: y + 1.6 * s }); }
    g.userData.update = t => { for (const C of crowns) { const w = Math.sin(t * 2.2 - C.x * 0.35 - C.z * 0.15); C.c.position.y = C.y + 0.12 * w; C.c.rotation.z = 0.08 * w; } }; g.userData.update(0); return g; },
  // A forest path (pivot at the middle): a dirt strip through grass, a few money trees either side
  coPath(o) { const g = grp(), gr = new THREE.Mesh(new THREE.PlaneGeometry(20, 20), mat('#7FB85A')); gr.rotation.x = -PI / 2; gr.position.y = 0.01; g.add(gr); const p = new THREE.Mesh(new THREE.PlaneGeometry(1.4, 20), mat('#B8946A')); p.rotation.x = -PI / 2; p.position.y = 0.015; g.add(p); return g; },
  // An autumn street (pivot at the middle of the pavement, houses behind at -Z): a row of plain house fronts with windows and doors, a pavement; no sign
  coStreet(o) { const W = o.w ?? 14, g = grp(), gr = new THREE.Mesh(new THREE.PlaneGeometry(W + 8, 12), mat('#C8BCA8')); gr.rotation.x = -PI / 2; gr.position.y = 0.01; g.add(gr);
    for (let i = 0; i < Math.ceil(W / 3.2); i++) { const x = -W / 2 + 1.6 + i * 3.2; g.add(at(box(3.1, 5 + (i % 2) * 0.8, 0.4, ['#E8C8A0', '#D8B890', '#ECD4B4', '#D4A888'][i % 4], { pivot: 'bottom', outline: 0.004 }), x, 0, -3.2), at(box(0.9, 1.9, 0.05, '#6A4A30', { pivot: 'bottom', outline: 0.006 }), x - 0.7, 0, -2.98));
      for (const wx of [0.6]) for (const wy of [1.5, 3.3]) g.add(at(box(0.8, 1.0, 0.05, '#BFD0DA', { outline: 0.006 }), x + wx, wy, -2.98)); }
    return g; },
  // A mound of opaque brown banknote leaves (pivot at its middle on the ground): o.h, o.r; o.growAt [t0, t1]: it piles up from nothing (a man vanishes
  // under it); o.n leaves
  coHeap(o) { const H = o.h ?? 1.0, R = o.r ?? 1.0, n = o.n ?? 160, g = grp(), k = grp(); g.add(k);
    const core = new THREE.Mesh(new THREE.SphereGeometry(R, 16, 8, 0, TAU, 0, PI / 2), mat(o.brown === false ? '#B49CD6' : '#8A5A32')); core.scale.y = H / R * 0.92; k.add(core);
    for (let i = 0; i < n; i++) { const m = noteMesh(0.26, 0.13, o.brown !== false); m.rotation.order = 'YXZ'; const a = hsh(i) * TAU, rr = R * Math.sqrt(hsh(i + 2)), y = H * Math.sqrt(Math.max(0, 1 - (rr / R) ** 2));
      m.position.set(Math.cos(a) * rr, y + 0.02, Math.sin(a) * rr); m.rotation.set(-PI / 2 + Math.atan2(rr, R) * 0.9 + (hsh(i + 5) - 0.5) * 0.5, hsh(i + 6) * TAU, (hsh(i + 8) - 0.5) * 0.3); k.add(m); }
    g.userData.update = t => { const s = o.growAt ? smooth((t - o.growAt[0]) / Math.max(0.01, o.growAt[1] - o.growAt[0])) : 1; k.scale.set(Math.max(0.001, 0.4 + 0.6 * s), Math.max(0.001, s), Math.max(0.001, 0.4 + 0.6 * s)); k.visible = s > 0.01; };
    g.userData.update(0); return g; },
  // A bonfire on a heap of brown notes (pivot at the middle on the ground): the heap, flame tongues (cones, opaque orange and yellow) that flicker, a few
  // sparks rising; o.r; never a disc or a glow halo
  coBonfire(o) { const R = o.r ?? 0.9, g = grp(), fl = []; const heap = COMPOSTEUR_PROPS.coHeap({ h: 0.6, r: R, n: 90 }); g.add(heap);
    for (let i = 0; i < 9; i++) { const a = i / 9 * TAU, rr = i === 0 ? 0 : R * 0.45, f = new THREE.Mesh(new THREE.ConeGeometry(0.18 + 0.06 * hsh(i), 0.9 + 0.5 * hsh(i + 1), 6), mat(i % 2 ? '#F2A030' : '#F2D04A', { emissive: i % 2 ? '#C05010' : '#C0901A', noGrain: true })); f.position.set(Math.cos(a) * rr, 0.75, Math.sin(a) * rr); g.add(f); fl.push({ f, ph: hsh(i + 3) * TAU, h0: 0.75 }); }
    const sp = []; for (let i = 0; i < 8; i++) { const s = at(box(0.03, 0.03, 0.03, '#F8D86A', { emissive: '#E09020', noGrain: true }), 0, 0, 0); g.add(s); sp.push(s); }
    g.userData.update = t => { for (const F of fl) { const w = Math.sin(t * 13 + F.ph); F.f.scale.set(1 - 0.12 * w, 1 + 0.22 * w, 1 - 0.12 * w); F.f.rotation.z = 0.12 * Math.sin(t * 7 + F.ph); }
      sp.forEach((s, i) => { const u = (t * 0.7 + hsh(i)) % 1; s.position.set((hsh(i + 2) - 0.5) * R + 0.2 * Math.sin(t * 3 + i), 0.9 + 1.6 * u, (hsh(i + 4) - 0.5) * R * 0.6); s.visible = u < 0.85; }); };
    g.userData.update(0); return g; },
  // A leaf blower (pivot at the handle, the nozzle toward +Z): an orange motor box, a long grey tube; o.on: white gust lines stream from the nozzle
  coBlower(o) { const g = grp(at(box(0.25, 0.28, 0.3, '#E8742A', { outline: 0.02 }), 0, -0.1, -0.1), at(cyl(0.05, 0.06, 0.9, '#8A9098', 8, { outline: 0.02 }), 0, -0.2, 0.45, PI / 2 - 0.3, 0, 0)), ls = [];
    for (let i = 0; i < 4; i++) { const b = box(0.02, 0.02, 0.35, '#FFFFFF', { emissive: '#B8C4D4', noGrain: true }); g.add(b); ls.push(b); }
    g.userData.update = t => ls.forEach((b, i) => { const u = (t * 2.5 + i / 4) % 1; b.visible = !!o.on; b.position.set((hsh(i) - 0.5) * 0.2, -0.45 - 0.3 * u, 0.95 + 0.9 * u); }); g.userData.update(0); return g; },
  // A garden rake (pivot at the grip's end, the head toward -Y)
  coRake(o) { const g = grp(at(cyl(0.02, 0.02, 1.4, '#A8845A', 6, { outline: 0.02 }), 0, -0.7, 0), at(box(0.45, 0.04, 0.04, '#5E656D', { outline: 0.02 }), 0, -1.4, 0)); for (let i = 0; i < 8; i++) g.add(at(box(0.015, 0.1, 0.015, '#5E656D'), -0.2 + i * 0.057, -1.46, 0.02)); return g; },
  // A sausage on a stick (pivot at the stick's end, pointing +Y)
  coSausage(o) { return grp(at(cyl(0.012, 0.012, 0.9, '#A8845A', 5, { pivot: 'bottom', outline: 0.02 }), 0, 0, 0), at(cyl(0.035, 0.035, 0.18, '#B8582E', 8, { outline: 0.03 }), 0, 0.95, 0)); },
  // A flatbed truck (pivot at the floor in its middle, faces +X): a plain cab, a flatbed with o.trees money trees strapped on; nothing written;
  // o.beep [t, ...]: the back lights blink
  coTruck(o) { const g = grp(), C = '#5E8CB0'; g.add(at(box(3.6, 0.5, 2.0, '#4A4D54', { pivot: 'bottom', outline: 0.004 }), -0.4, 0.5, 0), at(box(1.4, 1.7, 2.0, C, { pivot: 'bottom', outline: 0.004 }), 2.0, 0.5, 0), at(box(0.9, 0.7, 2.02, '#CFE6F4', { emissive: '#4A6A80' }), 2.25, 1.6, 0));
    for (const x of [-1.6, 1.9]) for (const z of [-1.0, 1.0]) g.add(at(cyl(0.42, 0.42, 0.28, '#1E2024', 12), x, 0.42, z, PI / 2, 0, 0));
    const lights = [-0.6, 0.6].map(z => { const m = mat('#802018', { unique: true, emissive: '#200000' }); const b = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.15, 0.25), m); b.position.set(-2.23, 0.8, z); g.add(b); return m; });
    for (let i = 0; i < (o.trees ?? 3); i++) { const tr = COMPOSTEUR_PROPS.coMoneyTree({ s: 0.75, n: 70 }); tr.position.set(-1.6 + i * 1.05, 1.0, (i % 2 ? 0.3 : -0.3)); tr.rotation.z = 0.25; g.add(tr); }
    g.userData.update = t => { const on = (o.beep || []).some(t0 => t > t0 && t - t0 < 0.12); for (const m of lights) m.emissive.set(on ? '#FF3020' : '#200000'); for (const ch of g.children) if (ch.userData && ch.userData.update && ch !== g) ch.userData.update(t); };
    g.userData.update(0); return g; },
  // The hero's pyjamas (attach to the torso joint; pivot at the collar, hangs -Y): a loose pale blue top with a white collar and piping and big buttons;
  // o.w / o.d / o.h (painted: the rig ignores outfit colours)
  coPyjama(o) { const w = o.w ?? 0.62, d = o.d ?? 0.42, h = o.h ?? 0.95, g = grp();
    const tex = (W, H, front) => canvasPlane(W, H, (c, Wc, Hc) => { c.fillStyle = '#A8C8E8'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#8EB2D8'; for (let i = 0; i < 6; i++) c.fillRect(i * Wc / 6 + Wc / 24, 0, Wc / 36, Hc);
      if (front) { c.fillStyle = '#F4F4F0'; c.beginPath(); c.moveTo(Wc * 0.2, 0); c.lineTo(Wc * 0.5, Hc * 0.18); c.lineTo(Wc * 0.8, 0); c.lineTo(Wc * 0.68, 0); c.lineTo(Wc * 0.5, Hc * 0.1); c.lineTo(Wc * 0.32, 0); c.fill(); c.fillRect(Wc * 0.48, Hc * 0.15, Wc * 0.04, Hc * 0.85);
        c.fillStyle = '#F4F4F0'; for (let i = 0; i < 4; i++) { c.beginPath(); c.arc(Wc * 0.56, Hc * (0.3 + i * 0.17), Wc * 0.03, 0, TAU); c.fill(); } } }, { res: 128 });
    for (const [W, x, z, ry, f] of [[w, 0, d / 2, 0, true], [w, 0, -d / 2, PI, false], [d, w / 2, 0, PI / 2, false], [d, -w / 2, 0, -PI / 2, false]]) { const p = tex(W, h, f); p.position.set(x, -h / 2, z); p.rotation.y = ry; g.add(p); }
    g.add(at(box(w, 0.02, d, '#A8C8E8'), 0, -0.01, 0)); return g; },
  // A mug (pivot at its base, the handle at +X): a plain white mug, steam wisps
  coMug(o) { const g = grp(at(cyl(0.06, 0.055, 0.12, '#F4F1EA', 12, { pivot: 'bottom', outline: 0.02 }), 0, 0, 0), at(cyl(0.05, 0.05, 0.005, '#5A3A22', 12), 0, 0.11, 0)); const hd = new THREE.Mesh(new THREE.TorusGeometry(0.035, 0.012, 6, 10, PI), mat('#F4F1EA')); hd.position.set(0.06, 0.06, 0); hd.rotation.z = -PI / 2; g.add(hd); return g; },
  // A navy peaked cap, no badge (attach to the head joint; pivot at its band's bottom); o.s its size
  coCap(o) { return grp(capMesh(o.s ?? 1, o.color)); },
  // A pigeon on the ground (pivot at its feet, faces +Z): grey body, green neck, small head that bobs; o.turn [[t, yaw]]
  coPigeon(o) { const g = grp(), hd = grp(), body = new THREE.Mesh(new THREE.SphereGeometry(0.16, 12, 8), mat('#8E959E')); body.scale.set(0.9, 0.85, 1.3); body.position.y = 0.2; addOutline(body, 0.03); g.add(body);
    g.add(at(box(0.12, 0.05, 0.2, '#5E656D', { outline: 0.03 }), 0, 0.2, -0.22, 0.3, 0, 0), at(cyl(0.08, 0.1, 0.12, '#5E8C7A', 8), 0, 0.32, 0.08));
    for (const sx of [-1, 1]) g.add(at(cyl(0.01, 0.01, 0.1, '#D86A6A', 4, { pivot: 'bottom' }), sx * 0.05, 0, 0.02));
    hd.position.set(0, 0.42, 0.1); g.add(hd); hd.add(at(sphere(0.07, '#8E959E', 1, { outline: 0.04 }), 0, 0, 0), at(new THREE.Mesh(new THREE.ConeGeometry(0.018, 0.05, 5), mat('#3A3D44')), 0, -0.01, 0.08, PI / 2, 0, 0));
    for (const sx of [-1, 1]) hd.add(at(sphere(0.02, '#E8742A', 0), sx * 0.05, 0.015, 0.045));
    g.userData.update = t => { hd.rotation.y = kv(o.turn, t, 0); hd.position.z = 0.1 + Math.max(0, Math.sin(t * 5.5)) ** 6 * 0.04; }; g.userData.update(0); return g; },
  // A puff of sparkles where a sapling pops up (pivot at the middle): small four-point stars (thin crossed bars, never a disc) at o.at, for 0.5 s
  coSparkle(o) { const g = grp(), ss = []; for (let i = 0; i < 6; i++) { const s = grp(at(box(0.16, 0.025, 0.01, '#FFF2A0', { emissive: '#E8C040', noGrain: true }), 0, 0, 0), at(box(0.025, 0.16, 0.01, '#FFF2A0', { emissive: '#E8C040', noGrain: true }), 0, 0, 0)); s.rotation.z = PI / 4 * (i % 2); g.add(s); ss.push(s); }
    g.userData.update = t => ss.forEach((s, i) => { const u = o.at != null ? (t - o.at) / 0.5 : -1; s.visible = u >= 0 && u < 1; if (s.visible) { const a = i / 6 * TAU; s.position.set(Math.cos(a) * 0.35 * (0.3 + u), 0.3 + Math.sin(a) * 0.3 * (0.3 + u) + 0.2 * u, 0); s.scale.setScalar(Math.sin(u * PI)); } }); g.userData.update(0); return g; },
  // A wide-brimmed hat (pivot at its brim): sits on top of a heap of notes (o.dropAt: it lands with a bounce)
  coHat(o) { const g = grp(), k = grp(at(cyl(0.3, 0.3, 0.03, '#5A4A3A', 16, { outline: 0.03 }), 0, 0, 0), at(cyl(0.16, 0.18, 0.18, '#5A4A3A', 12, { pivot: 'bottom', outline: 0.03 }), 0, 0.01, 0), at(cyl(0.185, 0.185, 0.05, '#2A1E16', 12), 0, 0.05, 0)); g.add(k);
    g.userData.update = t => { const q = o.bumpAt != null ? bump([o.bumpAt], t, 8, 25) : 0; k.scale.set(1 + 0.1 * q, 1 - 0.15 * q, 1 + 0.1 * q); k.rotation.z = 0.15 * shake(o.bumpAt != null ? [o.bumpAt] : [], t, 1, 20, 5); }; g.userData.update(0); return g; },
};
