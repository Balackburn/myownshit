// Props for « Les chaussettes » (story 36): a washing machine a man can crawl into, the kingdom of lost socks at the bottom of the drum.
// Conventions as in props.js (metres, front +Z, pivot at the floor); every motion is a pure function of t.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, sphere, rng, ease, clamp01 } from './style.js';
import { grp, at, mesh, canvasPlane, torus, glassMat } from './props.js';

const PI = Math.PI, TAU = PI * 2;
const tex = (w, h, draw) => { const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; };
const events = (on, off) => [...[].concat(on ?? []).map(a => [a, 1]), ...[].concat(off ?? []).map(a => [a, 0])].sort((a, b) => a[0] - b[0]);
function openness(ev, t, v0 = 0, upD = 0.45, dnD = 0.35) {
  let v = v0;
  for (const [a, up] of ev) { if (t < a) break; v = up ? Math.max(v, ease.out(clamp01((t - a) / upD))) : Math.min(v, 1 - ease.inOut(clamp01((t - a) / dnD))); }
  return v;
}
const shakeAmt = (ts, t, dur = 0.6) => { let k = 0; for (const a of [].concat(ts ?? [])) { const u = (t - a) / dur; if (u >= 0 && u < 1) k = Math.max(k, (1 - u) * (1 - u)); } return k; };

// the drum's perforated steel, as a repeating texture (light steel, dark holes, a soft sheen band)
let _perf = null;
export function perfTexture() {
  if (_perf) return _perf;
  _perf = tex(256, 256, (g, W, H) => { const gr = g.createLinearGradient(0, 0, W, 0); gr.addColorStop(0, '#B9C0C8'); gr.addColorStop(0.5, '#D9DEE3'); gr.addColorStop(1, '#B9C0C8'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
    g.fillStyle = '#4A4F57'; for (let y = 0; y < 8; y++) for (let x = 0; x < 8; x++) { g.beginPath(); g.arc(x * 32 + (y % 2 ? 16 : 0) + 8, y * 32 + 16, 6.5, 0, TAU); g.fill(); }
    g.fillStyle = 'rgba(255,255,255,0.35)'; for (let y = 0; y < 8; y++) for (let x = 0; x < 8; x++) { g.beginPath(); g.arc(x * 32 + (y % 2 ? 16 : 0) + 6, y * 32 + 13, 2.2, 0, TAU); g.fill(); } });
  _perf.wrapS = _perf.wrapT = THREE.RepeatWrapping; return _perf;
}

// a single sock lying flat (L-shaped boxes): o.colors [body, stripe, toe]
function flatSock(c = ['#D9453A', '#F4F1E8', '#F4F1E8'], s = 1) {
  const [b, st, toe] = c, g = grp();
  g.add(at(box(0.07 * s, 0.025 * s, 0.24 * s, b, { pivot: 'bottom', outline: 0.004 }), 0, 0, 0));
  const foot = grp(at(box(0.07 * s, 0.025 * s, 0.13 * s, b, { pivot: 'bottom', outline: 0.004 }), 0, 0, 0.065 * s), at(box(0.073 * s, 0.027 * s, 0.035 * s, toe, { pivot: 'bottom' }), 0, -0.001, 0.115 * s));
  foot.position.set(0, 0, 0.11 * s); foot.rotation.y = 0.55; g.add(foot);
  for (const z of [-0.07, -0.02]) g.add(at(box(0.073 * s, 0.027 * s, 0.022 * s, st, { pivot: 'bottom' }), 0, -0.001, z * s));
  return g;
}
const SOCK_COLORS = [['#D9453A', '#F4F1E8', '#F4F1E8'], ['#2F5E8C', '#F2C94C', '#F2C94C'], ['#F4F1E8', '#2C3E66', '#2C3E66'], ['#4CA36C', '#F4F1E8', '#2C6E4A'], ['#F2C94C', '#E0413A', '#E0413A'],
  ['#8E5BB5', '#F4F1E8', '#F4F1E8'], ['#E8879E', '#F4F1E8', '#C8322A'], ['#3A3D44', '#C9CCD1', '#C9CCD1'], ['#E07A2E', '#2F5E8C', '#2F5E8C'], ['#7FC4B2', '#F4F1E8', '#2F7F5C']];

export const CHAUSSETTES_PROPS = {
  bigWasher(o) {
    // a front-loading washing machine big enough to crawl into: body o.w × o.h × o.d (1.25 × 1.7 × 1.15), a porthole door (radius 0.46) hinged on the left that
    // opens toward the viewer — o.open (0..1) or o.openAt / o.closeAt; o.shakeAt rocks it; o.spinAt [t, ...] / o.spinStop spin the drum (it vibrates);
    // o.laundry: clothes tumbling in the drum; userData.opening (centre of the porthole), inside (centre of the drum)
    const W = o.w || 1.25, H = o.h || 1.7, D = o.d || 1.15, yc = o.yc || 0.8, R = 0.46, g = grp(), body = grp(), C = o.color || '#F2F2EC'; g.add(body);
    // the shell, with a round hole in the front (a ring of boxes is enough: the door covers the edge)
    // a hollow shell (back, sides, top) so the porthole shows the drum, not a wall
    body.add(at(box(W, H, 0.04, C, { pivot: 'bottom', outline: 0.01 }), 0, 0, -D / 2 + 0.02));
    for (const sx of [-1, 1]) body.add(at(box(0.04, H, D - 0.05, C, { pivot: 'bottom', outline: 0.01 }), sx * (W / 2 - 0.02), 0, -0.025));
    body.add(at(box(W, 0.04, D - 0.05, C, { outline: 0.01 }), 0, H - 0.02, -0.025));
    const front = new THREE.Shape([[-W / 2, 0], [W / 2, 0], [W / 2, H], [-W / 2, H]].map(([x, y]) => new THREE.Vector2(x, y)));
    const hole = new THREE.Path(); hole.absarc(0, yc, R - 0.02, 0, TAU, true); front.holes.push(hole);
    const fg = new THREE.ExtrudeGeometry(front, { depth: 0.05, bevelEnabled: false, curveSegments: 28 }); body.add(at(mesh(fg, mat(C)), 0, 0, D / 2 - 0.05));
    body.add(at(box(W - 0.06, 0.05, D - 0.08, '#E4E6E2'), 0, H + 0.025, -0.02));   // worktop lip
    body.add(at(box(W, 0.06, D, '#3C4650', { pivot: 'bottom' }), 0, 0, 0));        // plinth
    // control panel: a dial, a green display, three buttons, a soap drawer
    const pz = D / 2 + 0.006;
    body.add(at(box(W - 0.02, 0.26, 0.02, '#E1E4E6'), 0, H - 0.15, pz), at(box(0.34, 0.16, 0.03, '#D3D7DA', { outline: 0.006 }), -0.38, H - 0.15, pz + 0.01));
    body.add(at(cyl(0.085, 0.085, 0.05, '#C9CCD1', 16), 0.36, H - 0.15, pz + 0.025, PI / 2, 0, 0), at(box(0.02, 0.07, 0.012, '#5A5E66'), 0.36, H - 0.12, pz + 0.052));
    body.add(at(canvasPlane(0.2, 0.08, (c, Wc, Hc) => { c.fillStyle = '#1F3A2A'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#7CF29A'; c.font = `900 ${Hc * 0.62}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.display || '40°', Wc / 2, Hc / 2); }, { res: 128, emissive: 0.9 }), 0.05, H - 0.15, pz + 0.012));
    for (let i = 0; i < 3; i++) body.add(at(cyl(0.02, 0.02, 0.02, ['#E0413A', '#3C8DD9', '#F2C230'][i], 10), -0.02 + i * 0.07 + 0.12, H - 0.23, pz + 0.012, PI / 2, 0, 0));
    // the drum: perforated steel inside, three lifters, a back plate
    const tx = perfTexture().clone(); tx.needsUpdate = true; tx.repeat.set(10, 3);
    const drumM = new THREE.MeshLambertMaterial({ map: tx, side: THREE.BackSide });
    const drum = grp(); drum.position.set(0, yc, D / 2 - 0.05); body.add(drum);
    const spinG = grp(); drum.add(spinG);
    const dg = new THREE.CylinderGeometry(R - 0.03, R - 0.03, D - 0.2, 28, 1, true); dg.rotateX(PI / 2); dg.translate(0, 0, -(D - 0.2) / 2);
    const dm = new THREE.Mesh(dg, drumM); dm.receiveShadow = true; spinG.add(dm);
    spinG.add(at(cyl(R - 0.03, R - 0.03, 0.01, '#8E959D', 28), 0, 0, -(D - 0.2), PI / 2, 0, 0));
    for (let i = 0; i < 3; i++) { const a = i * TAU / 3; spinG.add(at(box(0.08, 0.06, D - 0.24, '#C9CED4', { outline: 0.004 }), Math.cos(a) * (R - 0.07), Math.sin(a) * (R - 0.07), -(D - 0.2) / 2, 0, 0, a + PI / 2)); }
    const clothes = [];
    if (o.laundry) { const r = rng(o.seed || 3); for (let i = 0; i < 5; i++) { const cl = flatSock(SOCK_COLORS[(i * 3) % SOCK_COLORS.length], 1.1); cl.position.set((r() - 0.5) * 0.4, -R + 0.1 + r() * 0.06, -0.15 - r() * 0.5); cl.rotation.set(r() * 2, r() * 6, r() * 2); spinG.add(cl); clothes.push(cl); } }
    // the door: chrome ring, a smoked glass dome, a handle; it hinges on the left
    const hinge = grp(); hinge.position.set(-R - 0.06, yc, D / 2 + 0.01); g.add(hinge);
    const door = grp(); door.position.x = R + 0.06; hinge.add(door);
    door.add(at(torus(R + 0.02, 0.06, '#C9CCD1', 10, 32), 0, 0, 0.03), at(torus(R - 0.05, 0.035, '#9AA1A8', 8, 32), 0, 0, 0.05));
    door.add(at(mesh(new THREE.SphereGeometry(R - 0.02, 28, 10, 0, TAU, 0, PI / 2.6), glassMat(0.18, '#D7EEF5')), 0, 0, 0.02, PI / 2, 0, 0));
    door.add(at(box(0.05, 0.16, 0.05, '#AEB5BC', { outline: 0.004 }), R + 0.03, 0, 0.06));
    const note = o.note ? CHAUSSETTES_PROPS.noteCard({ text: o.note, w: 0.3, h: 0.22 }) : null; if (note) { note.position.set(0.12, 0.25, 0.1); note.rotation.z = -0.08; door.add(note); }
    const ev = events(o.openAt, o.closeAt), spins = [].concat(o.spinAt ?? []);
    g.userData.update = t => {
      const v = openness(ev, t, o.open ?? 0); hinge.rotation.y = -1.85 * v;
      let rate = 0; for (const a of spins) if (t >= a && (o.spinStop == null || t < o.spinStop)) rate = 9;
      spinG.rotation.z = rate ? (t - spins[0]) * rate : 0;
      const k = shakeAmt(o.shakeAt, t) + (rate ? 0.5 : 0); body.position.set(0.012 * k * Math.sin(t * 61), 0.008 * k * Math.abs(Math.sin(t * 47)), 0); body.rotation.z = 0.02 * k * Math.sin(t * 43);
      hinge.position.x = -R - 0.06 + body.position.x;
    };
    g.userData.update(0); g.userData.opening = [0, yc, D / 2]; g.userData.inside = [0, yc, 0]; return g;
  },

  sockSingle(o) { // one sock hanging from a hand (grip at the cuff): o.colors [body, stripe, toe]
    const [b, st, toe] = o.colors || SOCK_COLORS[0], g = grp();
    g.add(at(box(0.07, 0.24, 0.05, b, { pivot: 'top', outline: 0.004 }), 0, 0, 0), at(box(0.075, 0.035, 0.055, st, { pivot: 'top' }), 0, 0, 0));
    for (const y of [-0.08, -0.14]) g.add(at(box(0.074, 0.022, 0.054, st), 0, y, 0));
    const foot = grp(at(box(0.07, 0.12, 0.05, b, { pivot: 'top', outline: 0.004 }), 0, 0, 0), at(box(0.073, 0.035, 0.053, toe, { pivot: 'top' }), 0, -0.09, 0));
    foot.position.set(0, -0.23, 0.01); foot.rotation.x = -1.2; g.add(foot);
    g.userData.grip = [0, -0.01, 0]; return g;
  },

  sockField(o) { // the lost socks of the whole world, lying around: n socks scattered over a w × d area (avoiding o.clear [x, z, r] circles), random colours
    const r = rng(o.seed || 7), g = grp(), n = o.n || 160, w = o.w || 20, d = o.d || 16, clear = o.clear || [];
    for (let i = 0; i < n; i++) {
      let x, z, tries = 0; do { x = (r() - 0.5) * w; z = (r() - 0.5) * d; tries++; } while (tries < 8 && clear.some(([cx, cz, cr]) => Math.hypot(x - cx, z - cz) < cr));
      const s = flatSock(SOCK_COLORS[Math.floor(r() * SOCK_COLORS.length)], 1.4 + r() * 1.2); s.position.set(x, o.y ?? 0.01, z); s.rotation.y = r() * TAU; g.add(s);
    }
    if (o.piles) o.piles.forEach(([px, pz, ps], j) => { for (let i = 0; i < 14; i++) { const s = flatSock(SOCK_COLORS[(i + j) % SOCK_COLORS.length], 1.6 * ps); const a = r() * TAU, rr = r() * 0.5 * ps; s.position.set(px + Math.cos(a) * rr, 0.02 + i * 0.03 * ps, pz + Math.sin(a) * rr); s.rotation.set((r() - 0.5) * 0.6, r() * TAU, (r() - 0.5) * 0.6); g.add(s); } });
    return g;
  },

  laundryCastle(o) { // the sock queen's castle: a wicker laundry basket as the keep, washing-powder boxes as towers with crenellations, a sock banner on top
    const s = o.size || 1, g = grp(), r = rng(o.seed || 4);
    const wick = tex(256, 128, (c, Wc, Hc) => { c.fillStyle = '#C99A5A'; c.fillRect(0, 0, Wc, Hc); for (let y = 0; y < Hc; y += 16) for (let x = 0; x < Wc; x += 16) { c.fillStyle = (x / 16 + y / 16) % 2 ? '#B58646' : '#DDB373'; c.fillRect(x + 1, y + 2, 14, 12); } });
    wick.wrapS = THREE.RepeatWrapping; wick.repeat.set(4, 2);
    const keep = new THREE.Mesh(new THREE.CylinderGeometry(2.2 * s, 1.9 * s, 3.4 * s, 18, 1, false), new THREE.MeshLambertMaterial({ map: wick })); keep.position.y = 1.7 * s; keep.castShadow = keep.receiveShadow = true; g.add(keep);
    g.add(at(torus(2.22 * s, 0.14 * s, '#A87A3E', 6, 24), 0, 3.4 * s, 0, PI / 2, 0, 0));
    for (let i = 0; i < 12; i++) { const a = i * TAU / 12; g.add(at(box(0.5 * s, 0.45 * s, 0.3 * s, '#C99A5A', { outline: 0.01 }), Math.cos(a) * 2.05 * s, 3.62 * s, Math.sin(a) * 2.05 * s, 0, -a, 0)); }
    const tower = (x, z, h, c, label) => { const tg = grp(at(box(1.1 * s, h * s, 0.8 * s, c, { pivot: 'bottom', outline: 0.012 }), 0, 0, 0));
      tg.add(at(canvasPlane(1.0 * s, 0.5 * s, (cx, Wc, Hc) => { cx.fillStyle = '#FFFFFF'; cx.fillRect(0, 0, Wc, Hc); cx.fillStyle = c; cx.font = `900 ${Hc * 0.42}px Arial`; cx.textAlign = 'center'; cx.textBaseline = 'middle'; cx.fillText(label, Wc / 2, Hc / 2); }, { res: 256 }), 0, h * s * 0.62, 0.401 * s));
      for (const dx of [-0.38, 0, 0.38]) tg.add(at(box(0.26 * s, 0.3 * s, 0.82 * s, c, { pivot: 'bottom', outline: 0.008 }), dx * s, h * s, 0));
      tg.position.set(x * s, 0, z * s); return tg; };
    g.add(tower(-2.6, 0.8, 4.2, '#3C8DD9', 'LESSIVE'), tower(2.6, 0.8, 3.8, '#E0413A', 'LESSIVE'));
    // gate: an arch of clothes pegs
    g.add(at(box(1.3 * s, 1.6 * s, 0.1 * s, '#5A3A22', { pivot: 'bottom' }), 0, 0, 2.18 * s), at(torus(0.65 * s, 0.09 * s, '#E8E1D0', 6, 16, PI), 0, 1.6 * s, 2.24 * s));
    // the banner: a pole and a flag with a sock on it
    const pole = at(cyl(0.05 * s, 0.05 * s, 2.4 * s, '#8C949A', 8, { pivot: 'bottom' }), 0, 3.4 * s, 0); g.add(pole);
    const flag = canvasPlane(1.4 * s, 0.9 * s, (c, Wc, Hc) => { c.fillStyle = '#7A3FB0'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#F2C94C'; c.fillRect(0, Hc * 0.84, Wc, Hc * 0.16);
      const x0 = Wc * 0.42, y0 = Hc * 0.12, lw = Wc * 0.13, lh = Hc * 0.42;   // a sock: cuff band, leg with two stripes, a round heel, the foot and toe to the right
      c.fillStyle = '#F4F1E8'; c.beginPath(); c.moveTo(x0, y0); c.lineTo(x0 + lw, y0); c.lineTo(x0 + lw, y0 + lh); c.lineTo(x0 + lw + Wc * 0.17, y0 + lh); c.arc(x0 + lw + Wc * 0.17, y0 + lh + Hc * 0.1, Hc * 0.1, -Math.PI / 2, Math.PI / 2);
      c.lineTo(x0 + Hc * 0.1, y0 + lh + Hc * 0.2); c.arc(x0 + Hc * 0.1, y0 + lh + Hc * 0.1, Hc * 0.1, Math.PI / 2, Math.PI); c.closePath(); c.fill();
      c.fillStyle = '#E0413A'; c.fillRect(x0, y0 + Hc * 0.1, lw, Hc * 0.06); c.fillRect(x0, y0 + Hc * 0.24, lw, Hc * 0.06); c.fillRect(x0 + lw + Wc * 0.12, y0 + lh, Wc * 0.05, Hc * 0.2);
      c.fillStyle = '#D9D3C0'; c.fillRect(x0 - Wc * 0.01, y0, lw + Wc * 0.02, Hc * 0.06); }, { res: 256 });
    const fl = grp(flag); flag.position.x = 0.7 * s; fl.position.set(0.05 * s, 5.4 * s, 0); g.add(fl);
    g.userData.update = t => { fl.rotation.y = 0.12 * Math.sin(t * 2.1); flag.rotation.y = 0.1 * Math.sin(t * 3.3 + 1); };
    g.userData.update(0); return g;
  },

  throne(o) { // the queen's throne: a washing-powder box with a red cushion, a clothes-peg back with a gold crest; userData.seat
    const s = o.size || 1, g = grp();
    g.add(at(box(0.9 * s, 0.6 * s, 0.7 * s, '#F2C94C', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(0.8 * s, 0.1 * s, 0.6 * s, '#C8322A', { pivot: 'bottom', outline: 0.006 }), 0, 0.6 * s, 0.02 * s));
    for (const sx of [-1, 1]) { const peg = grp(at(box(0.12 * s, 1.5 * s, 0.1 * s, '#E8D9B8', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(0.13 * s, 0.1 * s, 0.11 * s, '#9AA1A8'), 0, 0.85 * s, 0)); peg.position.set(sx * 0.32 * s, 0.6 * s, -0.3 * s); peg.rotation.z = -sx * 0.08; g.add(peg); }
    g.add(at(box(0.8 * s, 0.7 * s, 0.06 * s, '#7A3FB0', { pivot: 'bottom', outline: 0.006 }), 0, 0.7 * s, -0.3 * s), at(sphere(0.12 * s, '#F2C94C', 1), 0, 2.15 * s, -0.3 * s));
    g.add(at(canvasPlane(0.7 * s, 0.24 * s, (c, Wc, Hc) => { c.fillStyle = '#F2C94C'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#7A3FB0'; c.font = `900 ${Hc * 0.6}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('LESSIVE', Wc / 2, Hc / 2); }, { res: 256 }), 0, 0.3 * s, 0.351 * s));
    g.userData.seat = [0, 0.7 * s, 0.05 * s]; return g;
  },

  soapBubbles(o) { // big soap bubbles drifting up in a w × h × d box (iridescent, see-through); deterministic paths
    const r = rng(o.seed || 11), g = grp(), n = o.n || 18, w = o.w || 16, h = o.h || 8, d = o.d || 12, bs = [];
    const bm = new THREE.MeshLambertMaterial({ color: '#E6F4FF', transparent: true, opacity: 0.32, emissive: '#B9D9FF', emissiveIntensity: 0.25, depthWrite: false });
    for (let i = 0; i < n; i++) { const m = new THREE.Mesh(new THREE.SphereGeometry(1, 16, 10), bm); const sc = (o.size || 0.25) * (0.6 + r() * 0.9); m.scale.setScalar(sc); m.renderOrder = 3; m.userData.noAO = true;
      const hl = new THREE.Mesh(new THREE.SphereGeometry(0.22, 8, 6), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.8, toneMapped: false })); hl.position.set(-0.45, 0.45, 0.6); m.add(hl);
      g.add(m); bs.push({ m, x: (r() - 0.5) * w, y: r() * h, z: (r() - 0.5) * d, v: 0.25 + r() * 0.35, ph: r() * TAU }); }
    g.userData.update = t => { for (const b of bs) { const y = (b.y + t * b.v) % h; b.m.position.set(b.x + 0.4 * Math.sin(t * 0.7 + b.ph), y, b.z + 0.3 * Math.cos(t * 0.6 + b.ph)); } };
    g.userData.update(0); return g;
  },

  bindle(o) { // a runaway's bindle: a stick with a red polka-dot bundle at the end (along +X)
    const g = grp(at(cyl(0.012, 0.012, 0.6, '#8A5A32', 6), 0.3, 0, 0, 0, 0, PI / 2));
    const dots = tex(128, 64, (c, Wc, Hc) => { c.fillStyle = '#D9453A'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#FFFFFF'; for (let y = 0; y < 4; y++) for (let x = 0; x < 8; x++) { c.beginPath(); c.arc(x * 16 + (y % 2) * 8 + 4, y * 16 + 8, 3, 0, TAU); c.fill(); } });
    const bag = new THREE.Mesh(new THREE.SphereGeometry(0.075, 12, 8), new THREE.MeshLambertMaterial({ map: dots })); bag.scale.set(1, 0.85, 1); bag.position.set(0.6, -0.06, 0); bag.castShadow = true; g.add(bag);
    g.add(at(box(0.05, 0.035, 0.035, '#D9453A'), 0.6, 0.01, 0));
    return g;
  },

  noteCard(o) { // a note taped up: o.text ('JE REJOINS|MA MOITIÉ', | = new line), o.w × o.h, a small heart; readable from the front (+Z)
    const w = o.w || 0.32, h = o.h || 0.24, g = grp(), lines = String(o.text || 'JE REJOINS|MA MOITIÉ').split('|');
    const paper = canvasPlane(w, h, (c, Wc, Hc) => { c.fillStyle = '#FFF8E6'; c.fillRect(0, 0, Wc, Hc); c.strokeStyle = '#B9D4EA'; c.lineWidth = Hc * 0.008; for (let y = Hc * 0.2; y < Hc; y += Hc * 0.16) { c.beginPath(); c.moveTo(0, y); c.lineTo(Wc, y); c.stroke(); }
      c.fillStyle = '#121418'; c.textAlign = 'center'; c.textBaseline = 'middle'; let px = Hc * 0.21; c.font = `italic 900 ${px}px Arial`;
      const wmax = Math.max(...lines.map(l => c.measureText(l).width)); if (wmax > Wc * 0.82) { px *= Wc * 0.82 / wmax; c.font = `italic 900 ${px}px Arial`; }
      lines.forEach((l, i) => c.fillText(l, Wc / 2, Hc * (0.36 + i * 0.26 - (lines.length - 2) * 0.1)));
      c.fillStyle = '#E0413A'; const hx = Wc * 0.84, hy = Hc * 0.84, hs = Hc * 0.06; c.beginPath(); c.moveTo(hx, hy + hs); c.bezierCurveTo(hx - hs * 2, hy - hs * 0.5, hx - hs, hy - hs * 1.8, hx, hy - hs * 0.6); c.bezierCurveTo(hx + hs, hy - hs * 1.8, hx + hs * 2, hy - hs * 0.5, hx, hy + hs); c.fill(); }, { res: 512 });
    g.add(paper, at(box(w * 0.32, h * 0.12, 0.004, '#F4EBC2'), 0, h * 0.48, 0.003, 0, 0, 0.06));
    return g;
  },

  dryingRack(o) { // a folding clothes horse with socks pegged on it (all in pairs... except one); o.missing: the gap where a sock should be
    const g = grp(), w = o.w || 1.1;
    for (const sx of [-1, 1]) g.add(at(box(0.03, 1.0, 0.03, '#E8E8E4', { outline: 0.004 }), sx * w / 2, 0.5, 0, 0.25, 0, 0), at(box(0.03, 1.0, 0.03, '#E8E8E4', { outline: 0.004 }), sx * w / 2, 0.5, 0, -0.25, 0, 0));
    for (const y of [0.95, 0.7]) g.add(at(box(w, 0.015, 0.015, '#C9CCD1'), 0, y, 0.0));
    const pairs = o.pairs || [[0, 0], [1, 1], [3, 3], [5, -1]];
    pairs.forEach(([a, b], i) => { [a, b].forEach((ci, j) => { if (ci < 0) return; const s = CHAUSSETTES_PROPS.sockSingle({ colors: SOCK_COLORS[ci] }); s.scale.setScalar(1.1); s.position.set(-w / 2 + 0.12 + i * 0.26 + j * 0.09, 0.95, 0.01); g.add(s, at(box(0.02, 0.05, 0.02, '#F2C94C'), s.position.x, 0.96, 0.02)); }); });
    return g;
  },
  giantFoot(o) { // a huge bare foot coming down toes first (the sock's view of being worn): the shin up along +Y with the trouser hem, the foot angled down-forward
    const s = o.size || 1, sk = o.skin || P.skin, g = grp(), leg = grp(); g.add(leg);
    leg.add(at(box(0.36 * s, 1.6 * s, 0.36 * s, sk, { pivot: 'bottom', outline: 0.01 }), 0, 0.12 * s, -0.08 * s), at(box(0.46 * s, 0.9 * s, 0.46 * s, o.pants || P.suitNavy, { pivot: 'bottom', outline: 0.01 }), 0, 1.25 * s, -0.08 * s));
    const foot = grp(at(box(0.4 * s, 0.24 * s, 0.78 * s, sk, { outline: 0.01 }), 0, 0, 0.32 * s)); foot.rotation.x = 1.05; foot.position.set(0, 0.18 * s, 0); leg.add(foot);
    [[0.13, 0.12, 0.16], [0.095, 0.1, 0.13], [0.09, 0.095, 0.12], [0.085, 0.09, 0.11], [0.08, 0.085, 0.1]].forEach(([w, h, d], i) => foot.add(at(box(w * s, h * s, d * s, sk, { outline: 0.008 }), (-0.17 + i * 0.087) * s, -0.04 * s, (0.71 + d / 2 - i * 0.02) * s, 0, (i - 2) * 0.12, 0)));   // big splayed toes
    foot.add(at(box(0.05 * s, 0.03 * s, 0.03 * s, '#F4D7C8'), -0.15 * s, -0.01 * s, 0.79 * s));   // a toenail
    g.userData.update = t => { foot.rotation.x = 1.05 + 0.08 * Math.sin(t * 9); foot.children.slice(1).forEach((c, i) => { c.rotation.x = 0.25 * Math.max(0, Math.sin(t * 12 - i * 0.6)); }); };   // wiggling toes
    g.userData.update(0); return g;
  },

  stinkLines(o) { // green wavy smell lines rising and fading (o.n, o.w wide, o.h tall), from o.at seconds
    const g = grp(), n = o.n || 4, w = o.w || 0.5, h = o.h || 0.7, lines = [];
    for (let i = 0; i < n; i++) {
      const pts = []; for (let j = 0; j <= 12; j++) pts.push(new THREE.Vector3(0.05 * Math.sin(j * 1.1 + i), j / 12 * h, 0));
      const m = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 24, o.r || 0.014, 5, false), new THREE.MeshBasicMaterial({ color: o.color || '#8BCB4A', transparent: true, opacity: 0, toneMapped: false }));
      m.position.x = (i / Math.max(1, n - 1) - 0.5) * w; g.add(m); lines.push(m);
    }
    g.userData.update = t => { lines.forEach((m, i) => { const u = ((t - (o.at || 0)) * 0.9 + i * 0.27) % 1, on = t >= (o.at || 0); m.position.y = u * 0.25; m.material.opacity = on ? Math.sin(u * PI) * 0.95 : 0; m.rotation.y = 0.3 * Math.sin(t * 2 + i); }); };
    g.userData.update(0); return g;
  },
  sockSea(o) { // thousands of lost socks lying in heaps to the horizon (instanced: a handful of draw calls): o.n, o.w × o.d area round the origin,
    // o.clear [[x, z, r], ...] kept free, o.heaps [[x, z, r, h], ...] mounded piles, colours from the lost-sock palette
    const r = rng(o.seed || 31), n = o.n || 1500, w = o.w || 60, d = o.d || 50, clear = o.clear || [], heaps = o.heaps || [];
    const parts = [['leg', [0.07, 0.025, 0.24], [0, 0.0125, 0]], ['foot', [0.07, 0.025, 0.13], [0, 0.0125, 0.17]], ['toe', [0.073, 0.027, 0.04], [0, 0.0125, 0.225]], ['st1', [0.074, 0.027, 0.022], [0, 0.0125, -0.07]], ['st2', [0.074, 0.027, 0.022], [0, 0.0125, -0.02]]];
    const g = grp(), M = new THREE.Matrix4(), Q = new THREE.Quaternion(), E = new THREE.Euler(), S3 = new THREE.Vector3(), P3 = new THREE.Vector3(), C = new THREE.Color();
    const meshes = parts.map(([nm, [bx, by, bz]]) => { const m = new THREE.InstancedMesh(new THREE.BoxGeometry(bx, by, bz), new THREE.MeshLambertMaterial(), n); m.castShadow = false; m.receiveShadow = true; g.add(m); return m; });
    for (let i = 0; i < n; i++) {
      let x, z, y = 0, tries = 0; const hp = heaps.length && r() < (o.heapShare ?? 0.55) ? heaps[Math.floor(r() * heaps.length)] : null;
      if (hp) { const a = r() * TAU, rr = Math.sqrt(r()) * hp[2]; x = hp[0] + Math.cos(a) * rr; z = hp[1] + Math.sin(a) * rr; y = hp[3] * Math.max(0, 1 - (rr / hp[2]) ** 2) * (0.75 + 0.25 * r()); }
      else do { x = (r() - 0.5) * w; z = (r() - 0.5) * d; tries++; } while (tries < 10 && clear.some(([cx, cz, cr]) => Math.hypot(x - cx, z - cz) < cr));
      const sc = 1.3 + r() * 1.4, col = SOCK_COLORS[Math.floor(r() * SOCK_COLORS.length)];
      E.set((r() - 0.5) * (hp ? 1.2 : 0.2), r() * TAU, (r() - 0.5) * (hp ? 1.2 : 0.2)); Q.setFromEuler(E); S3.setScalar(sc);
      parts.forEach(([nm, , off], j) => { P3.set(off[0] * sc, off[1] * sc, off[2] * sc).applyQuaternion(Q).add(new THREE.Vector3(x, y, z)); M.compose(P3, Q, S3); meshes[j].setMatrixAt(i, M);
        meshes[j].setColorAt(i, C.set(nm === 'toe' ? col[2] : nm.startsWith('st') ? col[1] : col[0])); });
    }
    meshes.forEach(m => { m.instanceMatrix.needsUpdate = true; m.instanceColor.needsUpdate = true; m.computeBoundingSphere(); });
    return g;
  },

  sockCrowd(o) { // a crowd of little standing sock people (googly eyes), all turned toward o.face [x, z], bobbing; instanced. o.n, o.w × o.d, o.clear like sockSea
    const r = rng(o.seed || 41), n = o.n || 220, w = o.w || 24, d = o.d || 18, clear = o.clear || [], face = o.face || [0, 30];
    const H = [0.11, 0.45, 0.1];   // foot, leg, cuff heights (a sock person ~0.66 m)
    const defs = [['foot', [0.16, 0.11, 0.3], [0, 0.055, 0.07], 0], ['leg', [0.16, 0.45, 0.15], [0, 0.11 + 0.225, -0.005], 0], ['st1', [0.168, 0.032, 0.158], [0, 0.2, -0.005], 1], ['st2', [0.168, 0.032, 0.158], [0, 0.36, -0.005], 1],
      ['cuff', [0.172, 0.1, 0.162], [0, 0.61, -0.005], 2], ['eyeL', [0.05, 0.05, 0.02], [0.036, 0.47, 0.08], 3], ['eyeR', [0.05, 0.05, 0.02], [-0.036, 0.47, 0.08], 3], ['pupL', [0.022, 0.022, 0.012], [0.036, 0.465, 0.093], 4], ['pupR', [0.022, 0.022, 0.012], [-0.036, 0.465, 0.093], 4]];
    const g = grp(), meshes = defs.map(([nm, [bx, by, bz]]) => { const m = new THREE.InstancedMesh(new THREE.BoxGeometry(bx, by, bz), new THREE.MeshLambertMaterial(), n); m.castShadow = true; m.receiveShadow = true; g.add(m); return m; });
    const people = [], C = new THREE.Color();
    for (let i = 0; i < n; i++) {
      let x, z, tries = 0; do { x = (r() - 0.5) * w; z = (r() - 0.5) * d; tries++; } while (tries < 12 && clear.some(([cx, cz, cr]) => Math.hypot(x - cx, z - cz) < cr));
      const col = SOCK_COLORS[Math.floor(r() * SOCK_COLORS.length)], ry = Math.atan2(face[0] - x, face[1] - z) + (r() - 0.5) * 0.5, sc = 0.85 + r() * 0.4;
      people.push({ x, z, ry, sc, ph: r() * TAU, f: 2 + r() * 2.5, hop: r() < (o.hoppers ?? 0.3) });
      defs.forEach(([nm, , , ci], j) => meshes[j].setColorAt(i, C.set([col[0], col[1], col[1] === '#F4F1E8' ? '#F4F1E8' : col[1], '#F8F5EC', '#0B0C0F'][ci])));
    }
    const M = new THREE.Matrix4(), Q = new THREE.Quaternion(), Y = new THREE.Vector3(0, 1, 0), S3 = new THREE.Vector3(), P3 = new THREE.Vector3(), B = new THREE.Vector3();
    g.userData.update = t => { people.forEach((p, i) => { const up = p.hop ? 0.09 * Math.abs(Math.sin(t * p.f + p.ph)) : 0.012 * Math.sin(t * p.f + p.ph); Q.setFromAxisAngle(Y, p.ry + 0.08 * Math.sin(t * 1.3 + p.ph)); S3.setScalar(p.sc); B.set(p.x, up, p.z);
      defs.forEach(([, , off], j) => { P3.set(off[0] * p.sc, off[1] * p.sc, off[2] * p.sc).applyQuaternion(Q).add(B); M.compose(P3, Q, S3); meshes[j].setMatrixAt(i, M); }); });
      meshes.forEach(m => { m.instanceMatrix.needsUpdate = true; }); };
    g.userData.update(0); meshes.forEach(m => { m.instanceColor.needsUpdate = true; m.computeBoundingSphere(); });
    return g;
  },

  heartPop(o) { // a red heart that pops in at o.at and floats up a little, wobbling (faces +Z)
    const s = o.size || 0.25, sh = new THREE.Shape(); sh.moveTo(0, -0.5); sh.bezierCurveTo(-0.9, 0.1, -0.5, 0.75, 0, 0.35); sh.bezierCurveTo(0.5, 0.75, 0.9, 0.1, 0, -0.5);
    const geo = new THREE.ExtrudeGeometry(sh, { depth: 0.2, bevelEnabled: true, bevelSize: 0.05, bevelThickness: 0.05, bevelSegments: 2, curveSegments: 10 }); geo.center();
    const m = mesh(geo, mat('#E0413A', { outline: 0.01 })), g = grp(m); m.scale.setScalar(s);
    g.userData.update = t => { const u = t - (o.at || 0); const k = u < 0 ? 0 : u < 0.25 ? ease.out(u / 0.25) * 1.15 : 1 + 0.05 * Math.sin(u * 6); g.scale.setScalar(Math.max(0.001, k)); m.position.y = u > 0 ? Math.min(0.15, u * 0.12) : 0; m.rotation.y = 0.25 * Math.sin(u * 2.4); };
    g.userData.update(0); return g;
  },
};
