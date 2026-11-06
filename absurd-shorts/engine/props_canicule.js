// Props for « La canicule » (story 34): a fridge a man can live in, the heatwave and the snow.
// Conventions as in props.js (metres, front +Z, pivot at the floor); every motion is a pure function of t.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, sphere, rng, ease, clamp01 } from './style.js';
import { grp, at, mesh, canvasPlane, inst, rod, torus, glassMat } from './props.js';

const PI = Math.PI, TAU = PI * 2, MINUS = '−';
const tex = (w, h, draw) => { const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; };
const events = (on, off) => [...[].concat(on ?? []).map(a => [a, 1]), ...[].concat(off ?? []).map(a => [a, 0])].sort((a, b) => a[0] - b[0]);
// door-like 0..1 value from open/close events (opening 0.45 s, closing 0.35 s)
function openness(ev, t, v0 = 0, upD = 0.45, dnD = 0.35) {
  let v = v0;
  for (const [a, up] of ev) { if (t < a) break; v = up ? Math.max(v, ease.out(clamp01((t - a) / upD))) : Math.min(v, 1 - ease.inOut(clamp01((t - a) / dnD))); }
  return v;
}
const lastOpen = (ev, t) => { let a0 = null; for (const [a, up] of ev) { if (t < a) break; if (up) a0 = a; } return a0; };
const tempTxt = v => (v < 0 ? MINUS : '') + Math.abs(Math.round(v)) + '°';

let _puff = null;
export function puffTexture() {   // soft round vapour puff (mist, breath, steam)
  if (_puff) return _puff;
  _puff = tex(128, 128, (g, W, H) => { const gr = g.createRadialGradient(W / 2, H / 2, 4, W / 2, H / 2, W / 2); gr.addColorStop(0, 'rgba(255,255,255,0.95)'); gr.addColorStop(0.45, 'rgba(240,248,255,0.55)'); gr.addColorStop(1, 'rgba(235,245,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, W, H); });
  return _puff;
}
let _flake = null;
function flakeTexture() { if (_flake) return _flake; _flake = tex(64, 64, (g, W) => { const gr = g.createRadialGradient(32, 32, 2, 32, 32, 30); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.55, 'rgba(255,255,255,0.9)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, W, W); }); return _flake; }
const puffSprite = (color = '#FFFFFF') => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: puffTexture(), color, transparent: true, depthWrite: false, opacity: 0 })); s.renderOrder = 4; return s; };

// a small labelled food pack (canvas front on a box): milk, butter, jam
function pack(w, h, d, color, text, fg = '#FFFFFF', band = null) {
  const g = grp(box(w, h, d, color, { pivot: 'bottom', outline: 0.01 }));
  const f = canvasPlane(w * 0.96, h * 0.6, (c, W, H) => { c.fillStyle = band || color; c.fillRect(0, 0, W, H); c.fillStyle = fg; c.textAlign = 'center'; c.textBaseline = 'middle';
    let px = H * 0.62; c.font = `900 ${px}px Arial`; const tw = c.measureText(text).width; if (tw > W * 0.9) { px *= W * 0.9 / tw; c.font = `900 ${px}px Arial`; } c.fillText(text, W / 2, H / 2); }, { res: 256 });
  f.position.set(0, h * 0.45, d / 2 + 0.002); g.add(f); return g;
}
function milk() { const g = pack(0.11, 0.24, 0.11, '#F4F6F8', 'LAIT', '#2F62B5', '#F4F6F8'); g.add(at(box(0.11, 0.05, 0.08, '#F4F6F8', { taper: { x: 1, z: 0.05 } }), 0, 0.265, 0), at(cyl(0.015, 0.015, 0.02, '#2F62B5', 8), 0.025, 0.29, 0.02), at(box(0.112, 0.03, 0.112, '#2F62B5'), 0, 0.03, 0)); return g; }
function jar(color, lid = '#C8322A', s = 1) { return grp(cyl(0.045 * s, 0.045 * s, 0.1 * s, color, 10, { pivot: 'bottom', outline: 0.01 }), at(cyl(0.048 * s, 0.048 * s, 0.025 * s, lid, 10, { pivot: 'bottom' }), 0, 0.1 * s, 0), at(box(0.07 * s, 0.045 * s, 0.002, '#F7F2E4'), 0, 0.05 * s, 0.046 * s)); }
function cheese() { const sh = new THREE.Shape([[0, 0], [0.16, 0], [0, 0.1]].map(([x, y]) => new THREE.Vector2(x, y))); const geo = new THREE.ExtrudeGeometry(sh, { depth: 0.08, bevelEnabled: false }); geo.rotateX(-PI / 2);
  const m = mesh(geo, mat('#F2C94C')); const g = grp(at(m, -0.08, 0, 0.04)); [[0.03, 0.03], [0.07, 0.02], [0.05, 0.05]].forEach(([x, y]) => g.add(at(cyl(0.008, 0.008, 0.002, '#D9A93A', 8), -0.08 + x, y, 0.041, PI / 2))); return g; }
function yogurtPot(color) { return grp(cyl(0.035, 0.028, 0.07, '#F7F4EC', 10, { pivot: 'bottom', outline: 0.01 }), at(cyl(0.036, 0.034, 0.018, color, 10), 0, 0.055, 0), at(cyl(0.037, 0.037, 0.004, '#C9CCD1', 10), 0, 0.072, 0)); }
function lettuce(s = 1, seed = 1) { const r = rng(seed), g = grp(); for (let i = 0; i < 7; i++) { const l = sphere(0.07 * s * (0.8 + r() * 0.4), i % 2 ? '#7CC25A' : '#5FA845', 1); l.scale.set(1, 0.7, 1); l.position.set((r() - 0.5) * 0.08 * s, 0.05 * s + r() * 0.04 * s, (r() - 0.5) * 0.08 * s); g.add(l); } return g; }
function carrot(len = 0.18) { const g = grp(at(mesh(new THREE.ConeGeometry(0.022, len, 7), mat('#E8792E')), 0, 0, 0, 0, 0, PI / 2)); g.add(at(box(0.04, 0.008, 0.012, '#4CA64C'), len / 2 + 0.015, 0.01, 0, 0, 0, 0.4), at(box(0.04, 0.008, 0.012, '#4CA64C'), len / 2 + 0.015, -0.006, 0, 0, 0, -0.3)); return g; }
const hatTex = (a, b) => tex(128, 64, (g, W, H) => { g.fillStyle = a; g.fillRect(0, 0, W, H); g.fillStyle = b; for (let i = -2; i < 10; i++) { g.beginPath(); g.moveTo(i * 16, H); g.lineTo(i * 16 + 8, H); g.lineTo(i * 16 + 26, 0); g.lineTo(i * 16 + 18, 0); g.fill(); } g.fillStyle = '#FFFFFF'; for (let i = 0; i < 9; i++) g.fillRect((i * 37) % W, (i * 23) % H, 4, 4); });
function coneHat(r, h, a = '#E8508A', b = '#F2C94C', pom = '#FFFFFF') {
  const c = new THREE.Mesh(new THREE.ConeGeometry(r, h, 14, 1, true), new THREE.MeshLambertMaterial({ map: hatTex(a, b), side: THREE.DoubleSide }));
  c.position.y = h / 2; c.castShadow = true; return grp(c, at(sphere(r * 0.32, pom, 1), 0, h, 0));
}
function googly(s) { return grp(at(sphere(s, '#FFFFFF', 1), 0, 0, 0), at(sphere(s * 0.5, '#1C1C20', 1), 0, -s * 0.15, s * 0.65)); }

export const CANICULE_PROPS = {
  bigFridge(o) {
    // a retro pastel fridge big enough for a man sitting cross-legged on the crisper: inner o.w × o.h × o.d (1.04 × 2.06 × 0.82), walls 0.06;
    // the door hinges on the left edge (x -W/2) and opens toward the viewer: o.open (0..1) or o.openAt / o.closeAt (times or lists); o.shakeAt rattles it;
    // o.light: interior lit even with the door shut (the "inside" shots); o.mode 'full' (food on four shelves) | 'lived' (shelves out, he lives there) | 'party' | 'cosy';
    // o.drawerAt / o.drawerCloseAt slide the crisper out; o.letters n envelopes in the crisper; o.mist cold vapour spills out while the door is open;
    // userData: seat (top of the crisper, where he sits), inside (centre of the cabin), front (in front of the door)
    const W = o.w || 1.04, H = o.h || 2.06, D = o.d || 0.82, t = 0.06, C = o.color || '#A8D8CC', mode = o.mode || 'full', g = grp(), out = grp(g);   // g shakes inside out
    const liner = mat(o.cosy || mode === 'cosy' ? '#FFF3E0' : '#EEF7F8', { unique: true }), y0 = 0.06;   // plinth
    g.add(at(box(W + 2 * t, y0, D + t, '#3C4650', { pivot: 'bottom' }), 0, 0, -t / 2));
    g.add(at(box(W + 2 * t, t, D + t, C, { outline: 0.006 }), 0, y0 + H + t / 2, -t / 2), at(box(W + 2 * t - 0.06, 0.05, D + t - 0.06, C), 0, y0 + H + t + 0.025, -t / 2));   // top + rounded crown
    for (const s of [-1, 1]) g.add(at(box(t, H, D + t, C, { outline: 0.006 }), s * (W / 2 + t / 2), y0 + H / 2, -t / 2));
    g.add(at(box(W + 2 * t, H + t, t, C), 0, y0 + H / 2, -D / 2 - t / 2));
    // inner liner (back, sides, floor, ceiling) slightly inset, so the cabin reads as white plastic
    g.add(at(new THREE.Mesh(new THREE.BoxGeometry(W - 0.01, H - 0.01, 0.01), liner), 0, y0 + H / 2, -D / 2 + 0.006));
    for (const s of [-1, 1]) g.add(at(new THREE.Mesh(new THREE.BoxGeometry(0.01, H - 0.01, D - 0.01), liner), s * (W / 2 - 0.006), y0 + H / 2, 0));
    g.add(at(new THREE.Mesh(new THREE.BoxGeometry(W, 0.01, D), liner), 0, y0 + 0.005, 0), at(new THREE.Mesh(new THREE.BoxGeometry(W, 0.01, D), liner), 0, y0 + H - 0.005, 0));
    // front frame (seal) and a chrome logo plate
    g.add(at(box(W + 2 * t, 0.03, 0.02, '#D9DDE2'), 0, y0 + 0.015, D / 2 + 0.01));
    // frost on the back corners and the freezer box at the top
    const fr = rng(o.seed || 9), frost = mat('#FFFFFF', { noGrain: true });
    for (let i = 0; i < 14; i++) { const x = (fr() < 0.5 ? -1 : 1) * (W / 2 - 0.05 - fr() * 0.18), y = y0 + H - 0.35 - fr() * 0.5; g.add(at(new THREE.Mesh(new THREE.CircleGeometry(0.03 + fr() * 0.05, 6), frost), x, y, -D / 2 + 0.013)); }
    const FZ = y0 + H - 0.28;   // freezer compartment: frosted box with a flap
    g.add(at(box(W - 0.04, 0.27, D - 0.06, '#DDEFF5', { pivot: 'bottom', outline: 0.006 }), 0, FZ, -0.02), at(box(W - 0.1, 0.2, 0.012, '#F4FBFE'), 0, FZ + 0.135, D / 2 - 0.045, -0.12, 0, 0));
    for (let i = 0; i < 6; i++) g.add(at(mesh(new THREE.ConeGeometry(0.01, 0.04 + fr() * 0.05, 5), mat('#E6F6FF', { noGrain: true })), -W / 2 + 0.12 + i * 0.16, FZ - 0.03, D / 2 - 0.06, PI, 0, 0));   // icicles under the freezer
    // the interior light (bulb under the freezer) + a point light that comes on with the door
    const bulbM = mat('#FFFFFF', { unique: true, noGrain: true }), bulb = at(box(0.16, 0.05, 0.08, '#FFFFFF', { material: bulbM }), 0, FZ - 0.03, -D / 2 + 0.12);
    const lamp = new THREE.PointLight(o.cosy || mode === 'cosy' ? '#FFD9A0' : '#E3F4FF', 0, 3.2, 1.2); lamp.position.set(0, FZ - 0.25, D / 2 - 0.05); g.add(bulb, lamp);
    // the crisper (vegetable drawer) at the bottom, glass shelf on top of it = the seat
    const DR = 0.3, seatY = y0 + DR + 0.03, drawer = grp(); g.add(drawer);
    drawer.add(at(box(W - 0.06, DR - 0.02, D - 0.1, '#DCEFE8', { pivot: 'bottom', material: glassMat(0.35, '#CFEDE3') }), 0, y0 + 0.01, 0),
      at(box(W - 0.06, DR - 0.02, 0.02, '#BFE6D8', { pivot: 'bottom', material: glassMat(0.55, '#B6E2D2') }), 0, y0 + 0.01, D / 2 - 0.06),
      at(box(0.3, 0.035, 0.03, '#FFFFFF', { outline: 0.02 }), 0, y0 + DR - 0.05, D / 2 - 0.045));
    [[-0.28, 0.1, 1.1, 2], [0.05, 0.12, 1.0, 5], [0.32, 0.09, 0.9, 7]].forEach(([x, z, s, sd]) => drawer.add(at(lettuce(s, sd), x, y0 + 0.02, z - 0.1)));
    [[-0.05, 0.05, 0.2], [0.18, 0.08, -0.4], [-0.38, 0.06, 0.9]].forEach(([x, z, ry]) => drawer.add(at(carrot(), x, y0 + 0.13, z, 0, ry, 0)));
    [[0.4, -0.15], [-0.15, -0.2]].forEach(([x, z]) => drawer.add(at(sphere(0.045, '#E0413A', 1), x, y0 + 0.08, z)));
    const letters = []; for (let i = 0; i < (o.letters || 0); i++) { const e = canvasPlane(0.2, 0.124, (c, Wc, Hc) => { c.fillStyle = '#F7F4EC'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#C8322A'; c.fillRect(Wc * 0.78, Hc * 0.08, Wc * 0.15, Hc * 0.24); c.fillStyle = '#3A3D44'; c.font = `700 ${Hc * 0.12}px Arial`; c.fillText('M. LE MEC', Wc * 0.3, Hc * 0.55); c.font = `600 ${Hc * 0.1}px Arial`; c.fillText('BAC À LÉGUMES', Wc * 0.3, Hc * 0.72); }, { res: 256 });
      const L = at(grp(at(box(0.2, 0.124, 0.003, '#EDE8DC'), 0, 0, -0.002), e), (fr() - 0.5) * 0.5, y0 + DR - 0.06 + i * 0.004, (fr() - 0.5) * 0.3, -PI / 2 + 0.05, 0, (fr() - 0.5) * 1.2); drawer.add(L); letters.push(L); }
    g.add(at(box(W - 0.02, 0.022, D - 0.04, '#E6F4F8', { material: glassMat(0.45, '#E4F4FA') }), 0, seatY - 0.011, 0), at(box(W - 0.02, 0.03, 0.025, '#FFFFFF'), 0, seatY - 0.015, D / 2 - 0.03));
    // shelves and food
    const shelf = y => { g.add(at(box(W - 0.02, 0.018, D - 0.06, '#E6F4F8', { material: glassMat(0.4, '#E4F4FA') }), 0, y, -0.02), at(box(W - 0.02, 0.028, 0.024, '#FFFFFF'), 0, y, D / 2 - 0.05)); };
    const top = y0 + 1.55; shelf(top);
    g.add(at(milk(), -0.36, top + 0.01, -0.12), at(jar('#B5302A', '#F2F2F2'), -0.18, top + 0.01, 0.05), at(pack(0.14, 0.06, 0.08, '#F2D25C', 'BEURRE', '#B5302A'), 0.0, top + 0.01, 0.08),
      at(cheese(), 0.2, top + 0.01, 0.02), at(yogurtPot('#E8508A'), 0.38, top + 0.01, 0.1), at(yogurtPot('#7CC25A'), 0.3, top + 0.01, -0.08), at(jar('#E8A33C', '#2F62B5', 0.9), 0.42, top + 0.01, -0.18));
    if (mode === 'full') { [y0 + 0.75, y0 + 1.15].forEach(shelf);
      g.add(at(lettuce(1.2, 11), -0.3, y0 + 0.77, -0.05), at(pack(0.22, 0.12, 0.16, '#E0413A', 'JAMBON', '#FFFFFF'), 0.12, y0 + 0.77, 0.0), at(jar('#7A3E2A', '#F2C94C'), 0.38, y0 + 0.77, 0.08),
        at(yogurtPot('#9B6FD0'), -0.38, y0 + 1.17, 0.12), at(yogurtPot('#E8508A'), -0.3, y0 + 1.17, 0.12), at(yogurtPot('#F2C94C'), -0.22, y0 + 1.17, 0.12), at(cyl(0.12, 0.12, 0.09, '#F2F2F2', 12, { pivot: 'bottom', outline: 0.01 }), 0.2, y0 + 1.17, -0.05)); }
    // a thermostat dial on the right wall
    g.add(at(cyl(0.04, 0.04, 0.02, '#FFFFFF', 12, { outline: 0.02 }), W / 2 - 0.02, y0 + 1.35, 0.15, 0, 0, PI / 2), at(box(0.012, 0.05, 0.006, '#2F62B5'), W / 2 - 0.032, y0 + 1.35, 0.15));
    // party: garland, balloons, confetti
    const conf = [];
    if (mode === 'party') {
      g.add(at(CANICULE_PROPS.bunting({ len: W - 0.04, sag: 0.16, n: 9 }), 0, top - 0.06, D / 2 - 0.12));
      [[-W / 2 + 0.14, '#E8508A'], [W / 2 - 0.14, '#5FA8D3']].forEach(([x, c], i) => { g.add(at(sphere(0.1, c, 1, { outline: 0.02 }), x, top - 0.28 + i * 0.06, -0.15), rod([x, top - 0.38 + i * 0.06, -0.15], [x * 0.9, seatY + 0.02, -0.1], 0.002, '#3A3D44')); });
      const cf = CANICULE_PROPS.confetti({ w: W - 0.1, h: top - seatY - 0.05, d: D - 0.2, n: 90 }); cf.position.set(0, seatY + 0.02, 0); g.add(cf); conf.push(cf);
    }
    if (mode === 'cosy') {   // fairy lights along the top edge, a plaid rug on the seat, a framed photo on the side wall
      const fl = []; for (let i = 0; i < 11; i++) { const L = new THREE.Mesh(new THREE.SphereGeometry(0.014, 6, 4), new THREE.MeshBasicMaterial({ color: ['#FFD27A', '#FF8F8F', '#9FE0A0', '#8FC8FF'][i % 4] })); L.position.set(-W / 2 + 0.06 + i * (W - 0.12) / 10, top - 0.06 - 0.05 * Math.sin(i / 10 * PI), D / 2 - 0.08); g.add(L); fl.push(L); }
      g.userData.fairy = fl;
      g.add(at(box(W - 0.1, 0.012, D - 0.16, '#C8423A'), 0, seatY + 0.006, -0.02));
      g.add(at(canvasPlane(0.16, 0.2, (c, Wc, Hc) => { c.fillStyle = '#B98A5A'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#9FD3F0'; c.fillRect(Wc * 0.12, Hc * 0.1, Wc * 0.76, Hc * 0.8); c.fillStyle = '#F2C94C'; c.beginPath(); c.arc(Wc * 0.65, Hc * 0.3, Wc * 0.12, 0, TAU); c.fill(); c.fillStyle = '#E8D3A0'; c.fillRect(Wc * 0.12, Hc * 0.62, Wc * 0.76, Hc * 0.28); }, { res: 128 }), -W / 2 + 0.013, seatY + 0.95, -0.1, 0, PI / 2, 0));
    }
    // the door: hinge on the left edge, opens toward -x / +z
    const piv = grp(); piv.position.set(-W / 2 - t, 0, D / 2); g.add(piv);
    const DW = W + 2 * t, DH = H + t;
    piv.add(at(box(DW, DH, 0.08, C, { outline: 0.006, pivot: 'bottom' }), DW / 2, y0, 0.04), at(box(DW - 0.08, DH - 0.1, 0.012, C), DW / 2, y0 + DH / 2, 0.086));
    piv.add(at(box(0.04, 0.55, 0.05, '#D9DDE2', { outline: 0.02 }), DW - 0.08, y0 + DH * 0.58, 0.11), at(box(0.12, 0.05, 0.02, '#D9DDE2'), DW / 2, y0 + DH - 0.1, 0.09));
    const notes = rng(o.seed || 21); for (let i = 0; i < (o.notes ?? 5); i++) piv.add(at(box(0.11, 0.11, 0.004, ['#F2E36B', '#F2A0B8', '#9FD8F0', '#F2E36B'][i % 4]), 0.2 + notes() * 0.7, y0 + 0.95 + notes() * 0.75, 0.094, 0, 0, (notes() - 0.5) * 0.4));
    if (o.drawing !== false) piv.add(at(canvasPlane(0.24, 0.18, (c, Wc, Hc) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#F2C94C'; c.beginPath(); c.arc(Wc * 0.78, Hc * 0.25, Hc * 0.14, 0, TAU); c.fill(); c.strokeStyle = '#F2C94C'; c.lineWidth = 4; for (let k = 0; k < 8; k++) { const a = k / 8 * TAU; c.beginPath(); c.moveTo(Wc * 0.78 + Math.cos(a) * Hc * 0.18, Hc * 0.25 + Math.sin(a) * Hc * 0.18); c.lineTo(Wc * 0.78 + Math.cos(a) * Hc * 0.26, Hc * 0.25 + Math.sin(a) * Hc * 0.26); c.stroke(); }
      c.fillStyle = '#3F7FD1'; c.fillRect(Wc * 0.25, Hc * 0.4, Wc * 0.2, Hc * 0.4); c.fillStyle = '#E2B48A'; c.fillRect(Wc * 0.27, Hc * 0.2, Wc * 0.16, Hc * 0.2); c.strokeStyle = '#1C1C20'; c.lineWidth = 3; c.strokeRect(Wc * 0.25, Hc * 0.4, Wc * 0.2, Hc * 0.4); }, { res: 256 }), 0.45, y0 + 1.25, 0.093, 0, 0, 0.06));
    // inside of the door: liner, three bins with eggs and bottles
    const din = grp(); din.position.set(DW / 2, y0, -0.005); piv.add(din);
    din.add(at(box(DW - 0.12, DH - 0.14, 0.012, '#F2F8F9', { pivot: 'bottom' }), 0, 0.07, 0));
    const bins = [0.45, 1.0, 1.5], eggs = [];
    bins.forEach(y => din.add(at(box(DW - 0.2, 0.09, 0.11, '#E9F5F8', { pivot: 'bottom', material: glassMat(0.5, '#DDF0F5') }), 0, y, -0.065), at(box(DW - 0.2, 0.02, 0.012, '#FFFFFF'), 0, y + 0.08, -0.12)));
    for (let i = 0; i < 6; i++) { const e = sphere(0.032, '#F7EEDC', 1, { outline: 0.03 }); e.scale.set(1, 1.3, 1); const eg = grp(e); eg.position.set(-0.3 + i * 0.12, 1.5 + 0.075, -0.06); din.add(eg); eggs.push(eg);
      if (mode === 'party') { eg.add(at(coneHat(0.022, 0.06, ['#E8508A', '#5FA8D3', '#7CC25A'][i % 3], '#F2C94C'), 0, 0.035, 0, 0, 0, (i % 2 ? 1 : -1) * 0.2), at(googly(0.01), -0.012, 0.012, -0.03, 0, PI, 0), at(googly(0.01), 0.012, 0.012, -0.03, 0, PI, 0)); } }
    [[-0.3, '#F2F2F2', 0.3, '#2F62B5'], [-0.12, '#F2A63C', 0.26, '#F2F2F2'], [0.08, '#C8322A', 0.22, '#F2F2F2'], [0.26, '#F2C94C', 0.2, '#C8322A']].forEach(([x, c, h, cap]) => din.add(at(cyl(0.04, 0.04, h, c, 8, { pivot: 'bottom', outline: 0.01 }), x, 0.47, -0.065), at(cyl(0.018, 0.018, 0.04, cap, 8, { pivot: 'bottom' }), x, 0.47 + h, -0.065)));
    [[-0.2, '#7A3E2A'], [0.05, '#F2F2F2'], [0.28, '#5FA845']].forEach(([x, c]) => din.add(at(jar(c, '#F2C94C', 0.8), x, 1.02, -0.065)));
    // mist: vapour puffs spilling out of the bottom while the door is open
    const puffs = []; if (o.mist !== false) for (let i = 0; i < 10; i++) { const s = puffSprite('#F4FAFF'); g.add(s); puffs.push({ s, ph: i / 10, x: (fr() - 0.5) * W * 0.8, y: 0.35 + fr() * 0.9 }); }
    const ev = events(o.openAt, o.closeAt), dev = events(o.drawerAt, o.drawerCloseAt), shakes = [].concat(o.shakeAt ?? []);
    const setOpen = v => { piv.rotation.y = -clamp01(v) * 1.95; };
    g.userData.update = tt => {
      const v = openness(ev, tt, o.open || 0); setOpen(v);
      const lit = o.light ? 1 : clamp01(v * 3); bulbM.emissive.set(lit > 0.05 ? (o.cosy || mode === 'cosy' ? '#FFD59A' : '#DFF3FF') : '#000000'); liner.emissive.set(lit > 0.05 ? (o.cosy || mode === 'cosy' ? '#3A2A10' : '#1A2A30') : '#000000');
      lamp.intensity = lit * (o.lamp ?? 2.2);
      drawer.position.z = 0.36 * openness(dev, tt, 0, 0.35, 0.3);
      if (shakes.length) { let sk = 0; for (const a of shakes) if (tt >= a && tt < a + 0.5) sk = Math.sin((tt - a) * 60) * 0.012 * (1 - (tt - a) / 0.5); g.rotation.z = sk; g.position.x = sk * 0.6; }
      const tO = lastOpen(ev, tt), burst = tO == null ? 0 : 0.45 + 0.55 * Math.exp(-(tt - tO) / 1.2);
      puffs.forEach(p => { const q = ((tt * 0.45) + p.ph) % 1; p.s.position.set(p.x + 0.15 * Math.sin(q * 5 + p.ph * 9), Math.max(0.08, p.y - 0.85 * q * q), D / 2 + 0.08 + 0.7 * q); p.s.scale.setScalar(0.22 + 0.75 * q); p.s.material.opacity = v * burst * 0.5 * Math.sin(PI * Math.min(1, q * 1.15)); p.s.visible = p.s.material.opacity > 0.01; });
      eggs.forEach((e, i) => { if (mode === 'party') e.rotation.z = 0.12 * Math.sin(tt * 7 + i * 1.3); });
      (g.userData.fairy || []).forEach((L, i) => L.material.color.set(Math.sin(tt * 4 + i * 1.7) > -0.2 ? ['#FFD27A', '#FF8F8F', '#9FE0A0', '#8FC8FF'][i % 4] : '#5A5040'));
      conf.forEach(c => c.userData.update?.(tt));
    };
    out.userData.update = g.userData.update; out.userData.fairy = g.userData.fairy; out.userData.update(0);
    out.userData.seat = [0, seatY, -0.08]; out.userData.inside = [0, y0 + 1.0, 0]; out.userData.front = [0, 0, D / 2 + 0.7];
    return out;
  },
  bunting(o) {   // a party garland of triangle flags, o.len wide (centred on x), sagging o.sag, o.n flags
    const L = o.len || 1, n = o.n || 8, sag = o.sag ?? 0.12, g = grp(), cols = o.colors || ['#E8508A', '#F2C94C', '#5FA8D3', '#7CC25A', '#F2A63C'];
    const yAt = u => -sag * 4 * u * (1 - u), pts = []; for (let i = 0; i <= 20; i++) { const u = i / 20; pts.push(new THREE.Vector3(-L / 2 + u * L, yAt(u), 0)); }
    g.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: '#3A3D44' })));
    const tri = new THREE.ShapeGeometry(new THREE.Shape([[-0.045, 0], [0.045, 0], [0, -0.1]].map(([x, y]) => new THREE.Vector2(x * (o.size || 1), y * (o.size || 1)))));
    const flags = []; for (let i = 0; i < n; i++) { const u = (i + 0.5) / n, f = new THREE.Mesh(tri, new THREE.MeshLambertMaterial({ color: cols[i % cols.length], side: THREE.DoubleSide })); f.position.set(-L / 2 + u * L, yAt(u), 0.002); g.add(f); flags.push(f); }
    g.userData.update = t => flags.forEach((f, i) => { f.rotation.x = 0.18 * Math.sin(t * 3.1 + i * 0.9); });
    return g;
  },
  confetti(o) {   // falling confetti in an o.w × o.h × o.d box (origin at its bottom centre), o.n pieces, fluttering
    const n = o.n || 80, r = rng(o.seed || 17), geo = new THREE.PlaneGeometry(o.size || 0.03, (o.size || 0.03) * 0.6), cols = ['#E8508A', '#F2C94C', '#5FA8D3', '#7CC25A', '#F2A63C', '#FFFFFF'];
    const m = new THREE.InstancedMesh(geo, new THREE.MeshBasicMaterial({ side: THREE.DoubleSide }), n), base = [], d = new THREE.Object3D(), c = new THREE.Color();
    for (let i = 0; i < n; i++) { base.push([(r() - 0.5) * (o.w || 1), r(), (r() - 0.5) * (o.d || 1), r() * TAU, 0.25 + r() * 0.25]); m.setColorAt(i, c.set(cols[i % cols.length])); }
    const g = grp(m); m.frustumCulled = false;
    g.userData.update = t => { base.forEach(([x, y, z, ph, v], i) => { const q = ((y - t * v) % 1 + 1) % 1; d.position.set(x + 0.04 * Math.sin(t * 3 + ph), q * (o.h || 1), z + 0.03 * Math.cos(t * 2.4 + ph)); d.rotation.set(t * 4 + ph, t * 3 + ph * 2, ph); d.updateMatrix(); m.setMatrixAt(i, d.matrix); }); m.instanceMatrix.needsUpdate = true; };
    g.userData.update(0); return g;
  },
  partyHat(o) {   // a striped cone hat with a pompom (attach to the head joint)
    const g = coneHat(o.r || 0.075, o.h || 0.22, o.color || '#E8508A', o.stripe || '#F2C94C', o.pom || '#FFFFFF');
    g.add(at(torus(o.r || 0.075, 0.004, '#3A3D44', 4, 14), 0, 0.004, 0, PI / 2, 0, 0)); g.rotation.z = o.tilt ?? -0.15; return g;
  },
  thermometer(o) {   // a big wall thermometer: board, glass tube, coloured column that runs from o.from to o.temp between o.riseAt and riseAt + o.dur, the value written large on top
    const w = o.w || 0.2, h = o.h || 0.7, lo = o.min ?? -20, hi = o.max ?? 50, g = grp(), body = grp(); g.add(body);
    const hot = (o.temp ?? 40) >= 15, colC = o.color || (hot ? '#E0413A' : '#3C8DD9');
    body.add(at(box(w, h, 0.03, o.board || '#F7F2E4', { outline: 0.01 }), 0, 0, 0), at(cyl(w / 2, w / 2, 0.03, o.board || '#F7F2E4', 14), 0, h / 2, 0, PI / 2));
    const tubeH = h * 0.66, yB = -h * 0.36, tubeTop = yB + tubeH;
    body.add(at(box(w * 0.16, tubeH, 0.02, '#FFFFFF', { outline: 0.02 }), 0, yB + tubeH / 2, 0.022), at(sphere(w * 0.16, colC, 1), 0, yB, 0.03));
    const col = box(w * 0.08, 1, 0.012, colC, { pivot: 'bottom', noGrain: true }); col.position.set(0, yB, 0.034); body.add(col);
    const ticks = canvasPlane(w * 0.9, tubeH, (c, W, H) => { c.fillStyle = '#3A3D44'; c.font = `700 ${W * 0.13}px Arial`; c.textBaseline = 'middle';
      for (let v = lo; v <= hi; v += 5) { const y = H - (v - lo) / (hi - lo) * H; c.fillRect(W * 0.58, y - 1, v % 10 === 0 ? W * 0.12 : W * 0.07, 2); if (v % 10 === 0) { c.textAlign = 'left'; c.fillText((v < 0 ? MINUS : '') + Math.abs(v), W * 0.72, y); } } }, { res: 256, transparent: true });
    ticks.position.set(0, yB + tubeH / 2, 0.018); body.add(ticks);
    let shown = null; const val = canvasPlane(w * 0.95, w * 0.5, () => {}, { res: 256, transparent: true }); val.position.set(0, h * 0.42, 0.032); body.add(val);
    const draw = v => { const tx = tempTxt(v); if (tx === shown) return; shown = tx; const cv = val.material.map.image, c = cv.getContext('2d'); c.clearRect(0, 0, cv.width, cv.height);
      c.fillStyle = colC; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${cv.height * 0.8}px Arial`; c.fillText(tx, cv.width / 2, cv.height / 2); val.material.map.needsUpdate = true; };
    const yOf = v => clamp01((v - lo) / (hi - lo)) * tubeH;
    g.userData.update = t => { const from = o.from ?? o.temp ?? 40, to = o.temp ?? 40, q = o.riseAt == null ? 1 : ease.out(clamp01((t - o.riseAt) / (o.dur || 0.8))), v = from + (to - from) * q;
      col.scale.y = Math.max(0.001, yOf(v)); draw(v);
      body.position.x = v >= 38 ? 0.004 * Math.sin(t * 55) : 0; body.rotation.z = v >= 38 ? 0.012 * Math.sin(t * 41) : 0; };
    g.userData.update(0); return g;
  },
  monthCalendar(o) {   // a wall calendar: one page per month (o.months), page i lifts away at o.flipAt + i * o.dur
    const w = o.w || 0.34, h = o.h || 0.46, months = o.months || ['JUILLET', 'AOÛT', 'SEPTEMBRE'], g = grp();
    g.add(at(box(w + 0.02, h + 0.02, 0.012, '#3A3D44'), 0, 0, -0.008));
    const art = { 'JUIN': '#F2C94C', 'JUILLET': '#F2A63C', 'AOÛT': '#E0413A', 'SEPTEMBRE': '#C9824E', 'OCTOBRE': '#B5642E' };
    const pages = months.map((m, i) => { const piv = grp(); piv.position.set(0, h / 2, 0.002 + (months.length - i) * 0.002); g.add(piv);
      const pg = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FBF8F0'; c.fillRect(0, 0, W, H); c.fillStyle = '#C8322A'; c.fillRect(0, 0, W, H * 0.22);
        c.fillStyle = '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle'; let px = H * 0.13; c.font = `900 ${px}px Arial`; const tw = c.measureText(m).width; if (tw > W * 0.88) { px *= W * 0.88 / tw; c.font = `900 ${px}px Arial`; } c.fillText(m, W / 2, H * 0.12);
        c.fillStyle = art[m] || '#F2C94C'; c.beginPath(); c.arc(W * 0.5, H * 0.36, H * 0.08, 0, TAU); c.fill();
        c.fillStyle = '#3A3D44'; c.font = `700 ${H * 0.045}px Arial`; for (let d = 0; d < 31; d++) { const cx = (d % 7 + 0.5) / 7 * W, cy = H * (0.52 + Math.floor(d / 7) * 0.1); c.fillText(String(d + 1), cx, cy); }
        if (o.cross) { c.strokeStyle = '#C8322A'; c.lineWidth = H * 0.012; for (let d = 0; d < 31; d++) { const cx = (d % 7 + 0.5) / 7 * W, cy = H * (0.52 + Math.floor(d / 7) * 0.1); c.beginPath(); c.moveTo(cx - W * 0.04, cy - H * 0.03); c.lineTo(cx + W * 0.04, cy + H * 0.03); c.moveTo(cx + W * 0.04, cy - H * 0.03); c.lineTo(cx - W * 0.04, cy + H * 0.03); c.stroke(); } } }, { res: 256 });
      pg.position.y = -h / 2; piv.add(pg); return piv; });
    for (let i = 0; i < 5; i++) g.add(at(torus(0.012, 0.003, '#9AA0A8', 4, 8), -w * 0.3 + i * w * 0.15, h / 2, 0.012, 0, PI / 2, 0));
    g.userData.update = t => pages.forEach((p, i) => { if (i === pages.length - 1) return; const q = o.flipAt == null ? 0 : clamp01((t - o.flipAt - i * (o.dur || 0.5)) / 0.28); p.rotation.x = -ease.inOut(q) * 2.6; p.visible = q < 0.98; });
    g.userData.update(0); return g;
  },
  hotMug(o) {   // a big mug of hot chocolate with steam curling up
    const r = o.r || 0.06, g = grp(cyl(r, r * 0.92, r * 1.7, o.color || '#E0413A', 12, { pivot: 'bottom', outline: 0.02 }), at(cyl(r * 0.88, r * 0.88, 0.004, '#6B3E26', 12), 0, r * 1.6, 0),
      at(torus(r * 0.45, r * 0.12, o.color || '#E0413A', 6, 10, PI), r * 1.05, r * 0.85, 0, 0, 0, -PI / 2), at(box(r * 0.9, r * 0.5, 0.002, '#FFFFFF'), 0, r * 0.85, r * 0.93));
    const steam = []; for (let i = 0; i < 6; i++) { const s = puffSprite('#FFFFFF'); g.add(s); steam.push(s); }
    g.userData.update = t => steam.forEach((s, i) => { const q = ((t * 0.55) + i / 6) % 1; s.position.set(0.02 * Math.sin(q * 7 + i), r * 1.7 + q * 0.28, 0.01 * Math.cos(q * 5 + i)); s.scale.setScalar(0.04 + q * 0.09); s.material.opacity = 0.7 * Math.sin(PI * q); });
    g.userData.update(0); g.userData.grip = [0, r * 0.8, 0]; return g;
  },
  shoulderBlanket(o) {   // a tartan blanket draped over the shoulders (attach to the torso joint): a back panel, two front flaps, a rolled top
    const tartan = tex(128, 128, (c, W) => { c.fillStyle = o.color || '#C8423A'; c.fillRect(0, 0, W, W); c.fillStyle = 'rgba(30,40,60,0.45)'; for (let i = 0; i < 4; i++) { c.fillRect(i * 32 + 8, 0, 10, W); c.fillRect(0, i * 32 + 8, W, 10); } c.fillStyle = 'rgba(250,240,210,0.5)'; for (let i = 0; i < 4; i++) { c.fillRect(i * 32 + 24, 0, 3, W); c.fillRect(0, i * 32 + 24, W, 3); } });
    tartan.wrapS = tartan.wrapT = THREE.RepeatWrapping; tartan.repeat.set(2, 2);
    const m = new THREE.MeshLambertMaterial({ map: tartan }), w = o.w || 0.62, hb = o.h || 0.62;
    const part = (pw, ph, pd, x, y, z, rx = 0, rz = 0) => { const b = new THREE.Mesh(new THREE.BoxGeometry(pw, ph, pd), m); b.position.set(x, y, z); b.rotation.set(rx, 0, rz); b.castShadow = true; return b; };
    const g = grp(part(w, hb, 0.04, 0, -hb / 2 + 0.05, -0.17, 0.08), part(0.17, hb * 0.8, 0.04, -w / 2 + 0.1, -hb * 0.4 + 0.05, 0.16, -0.05, 0.08), part(0.17, hb * 0.8, 0.04, w / 2 - 0.1, -hb * 0.4 + 0.05, 0.16, -0.05, -0.08));
    const roll = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, w + 0.04, 8), m); roll.rotation.z = PI / 2; roll.position.set(0, 0.06, -0.02); roll.scale.set(1, 1, 3.6); g.add(roll);
    return g;
  },
  pharmacyCross(o) {   // a French pharmacy's green LED cross on a wall bracket, alternating the cross and o.text (the temperature) every o.period s
    const s = o.size || 0.9, g = grp(), face = () => canvasPlane(s, s, () => {}, { res: 256, emissive: 1 });
    const front = face(), back = face(); front.position.z = 0.061; back.position.z = -0.061; back.rotation.y = PI;
    const arm = s / 3, sh = new THREE.Shape([[-arm / 2, s / 2], [arm / 2, s / 2], [arm / 2, arm / 2], [s / 2, arm / 2], [s / 2, -arm / 2], [arm / 2, -arm / 2], [arm / 2, -s / 2], [-arm / 2, -s / 2], [-arm / 2, -arm / 2], [-s / 2, -arm / 2], [-s / 2, arm / 2], [-arm / 2, arm / 2]].map(([x, y]) => new THREE.Vector2(x, y)));
    const body = mesh(new THREE.ExtrudeGeometry(sh, { depth: 0.12, bevelEnabled: false }), mat('#1F5A3A')); body.position.z = -0.06;
    const mask = c => { c.beginPath(); const W = c.canvas.width, a = W / 3; c.moveTo(a, 0); c.lineTo(2 * a, 0); c.lineTo(2 * a, a); c.lineTo(W, a); c.lineTo(W, 2 * a); c.lineTo(2 * a, 2 * a); c.lineTo(2 * a, W); c.lineTo(a, W); c.lineTo(a, 2 * a); c.lineTo(0, 2 * a); c.lineTo(0, a); c.lineTo(a, a); c.closePath(); };
    [front, back].forEach(f => { f.material.transparent = true; f.material.alphaTest = 0.05; });
    let shown = -1; const paint = k => { if (k === shown) return; shown = k; [front, back].forEach(f => { const cv = f.material.map.image, c = cv.getContext('2d'), W = cv.width; c.clearRect(0, 0, W, W); c.save(); mask(c); c.clip(); c.fillStyle = '#0E2A1C'; c.fillRect(0, 0, W, W);
      if (k === 0) { c.fillStyle = '#3CF07A'; for (let x = 4; x < W; x += 10) for (let y = 4; y < W; y += 10) { c.beginPath(); c.arc(x, y, 3.6, 0, TAU); c.fill(); } }
      else { c.fillStyle = '#E8FFE8'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${W * 0.27}px Arial`; c.fillText(o.text || '40°', W / 2, W / 2); }
      c.restore(); f.material.map.needsUpdate = true; }); };
    g.add(body, front, back, at(box(0.06, 0.06, 0.5, '#3A3D44'), 0, 0, -0.3));
    g.userData.update = t => paint(Math.floor(t / (o.period || 0.9) + (o.phase || 0.5)) % 2); g.userData.update(0); return g;
  },
  deskFan(o) {   // a little desk fan: base, stem, cage, three blades spinning, slow oscillation
    const c = o.color || '#5FA8D3', g = grp(at(cyl(0.11, 0.13, 0.04, c, 12, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(cyl(0.015, 0.015, 0.22, '#D9DDE2', 6, { pivot: 'bottom' }), 0, 0.04, 0));
    const head = grp(); head.position.set(0, 0.28, 0); g.add(head);
    head.add(at(cyl(0.05, 0.06, 0.09, c, 10), 0, 0, -0.06, PI / 2), at(torus(0.15, 0.006, '#D9DDE2', 4, 20), 0, 0, 0.02), at(torus(0.15, 0.006, '#D9DDE2', 4, 20), 0, 0, -0.01));
    for (let i = 0; i < 8; i++) head.add(at(box(0.004, 0.3, 0.004, '#D9DDE2'), 0, 0, 0.025, 0, 0, i / 8 * PI));
    const rot = grp(); rot.position.z = 0.005; head.add(rot); for (let i = 0; i < 3; i++) { const b = box(0.07, 0.13, 0.006, '#F4F1EA', { outline: 0.02 }); b.position.set(0, 0.07, 0); const arm = grp(b); arm.rotation.z = i / 3 * TAU; rot.add(arm); }
    rot.add(cyl(0.025, 0.025, 0.03, c, 8)); rot.children.at(-1).rotation.x = PI / 2;
    g.userData.update = t => { rot.rotation.z = -t * (o.speed ?? 28); head.rotation.y = 0.55 * Math.sin(t * 0.9); }; g.userData.update(0); return g;
  },
  wiltPlant(o) {   // a pot plant wilting in the heat: the leaves droop more and more from o.wiltAt (or are drooped by o.wilt)
    const g = grp(at(cyl(0.09, 0.07, 0.16, '#C9683A', 8, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(cyl(0.085, 0.085, 0.01, '#5A3A22', 8), 0, 0.155, 0)), leaves = [];
    for (let i = 0; i < 6; i++) { const a = i / 6 * TAU, piv = grp(); piv.position.set(0, 0.16, 0); piv.rotation.y = a; const st = at(box(0.012, 0.22, 0.012, '#4C8F3A', { pivot: 'bottom' }), 0, 0, 0); const lf = at(box(0.07, 0.12, 0.01, '#5FA845', { pivot: 'bottom', taper: { x: 0.2, z: 1 } }), 0, 0.2, 0); const up = grp(st, lf); piv.add(up); g.add(piv); leaves.push(up); }
    g.userData.update = t => { const w = o.wiltAt == null ? (o.wilt ?? 0.8) : clamp01((t - o.wiltAt) / 1.5) * (o.wilt ?? 1); leaves.forEach((l, i) => { l.rotation.x = 0.25 + w * (1.9 + 0.2 * Math.sin(i * 2.1)) + 0.03 * Math.sin(t * 2 + i); }); };
    g.userData.update(0); return g;
  },
  snowfall(o) {   // falling snowflakes in an o.w × o.h × o.d box (origin at its bottom centre), o.n flakes, drifting
    const n = o.n || 900, r = rng(o.seed || 23), base = new Float32Array(n * 5), pos = new Float32Array(n * 3), W = o.w || 12, H = o.h || 8, D = o.d || 12;
    for (let i = 0; i < n; i++) base.set([(r() - 0.5) * W, r() * H, (r() - 0.5) * D, r() * TAU, 0.5 + r() * 0.6], i * 5);
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    const pts = new THREE.Points(geo, new THREE.PointsMaterial({ color: '#FFFFFF', size: o.size || 0.07, map: flakeTexture(), transparent: true, depthWrite: false, alphaTest: 0.02 })); pts.frustumCulled = false;
    const g = grp(pts);
    g.userData.update = t => { for (let i = 0; i < n; i++) { const b = i * 5; pos[i * 3] = base[b] + Math.sin(t * 0.9 + base[b + 3]) * 0.35 + (o.wind || 0) * t; pos[i * 3 + 1] = ((base[b + 1] - t * base[b + 4]) % H + H) % H; pos[i * 3 + 2] = base[b + 2] + Math.cos(t * 0.7 + base[b + 3]) * 0.2; } geo.attributes.position.needsUpdate = true; };
    g.userData.update(0); return g;
  },
  snowBank(o) {   // a heap of snow along a wall or a kerb: lumpy white mounds, o.len long
    const L = o.len || 3, r = rng(o.seed || 31), g = grp();
    for (let i = 0; i < Math.round(L * 4); i++) { const m = sphere(0.18 + r() * 0.2, i % 3 ? '#FFFFFF' : '#EEF3F8', 1); m.scale.set(1.2, 0.45 + r() * 0.25, 1); m.position.set(-L / 2 + r() * L, 0.02, (r() - 0.5) * 0.3); g.add(m); }
    return g;
  },
};
