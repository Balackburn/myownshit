// « La tartine » (story 102, cycle 54): this man picks his toast up in six seconds and an inspector crawls out from under the table, stopwatch
// in hand: the rule is five. The toast is confiscated; the inspector lives under the table. A law follows (five seconds on the floor and it
// belongs to the State), every kitchen gets its agent, butter side down is taxed double, the ministers eat off the floor; the country becomes
// deft, the State has every floor polished, the hero slips, gets up in six seconds and is assigned under a table: the inspector's. He was seven.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
// Running gags drawn here: the big brown luggage tag round the neck of every State agent (ttTag: kraft card, eyelet, string; its back carries the
// stopwatch drawing with the owner's own time, shown by o.flip), the stopwatch with a green wedge up to five and a red zone after (ttStopwatch, no
// digits), the toast that always shows its buttered side (ttToast: a thick yellow butter layer, a pat on top, a yellow splat ring when it lands).
import * as THREE from 'three';
import { box, cyl, sphere, mat } from './style.js';
import { grp, at, rod, torus } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = (x, c = 2.2) => { const u = clamp01(x); return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const lerp = (a, b, u) => a + (b - a) * u;
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
// [[t, v], ...] -> v at t, smoothstep between keys (a key [t, v, 'lin'] makes its segment linear)
const keyAt = (K, t, d = 0) => {
  if (!K || !K.length) return d;
  if (t <= K[0][0]) return K[0][1];
  for (let i = 1; i < K.length; i++) if (t < K[i][0]) { const u = (t - K[i - 1][0]) / Math.max(1e-6, K[i][0] - K[i - 1][0]); return lerp(K[i - 1][1], K[i][1], K[i][2] === 'lin' ? u : smooth(u)); }
  return K[K.length - 1][1];
};
// a damped wobble summed over [[t0, amp, freq, decay], ...]
const rattle = (R, t) => { let s = 0; for (const [t0, amp, f, dk] of R || []) { const u = t - t0; if (u > 0) s += amp * Math.sin(u * (f ?? 18)) * Math.exp(-u * (dk ?? 3.5)); } return s; };
const tex = cv => { const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t; };
const canvas = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
const L = (c, o = {}) => new THREE.MeshLambertMaterial({ color: c, ...o });
const INK = '#1B1E2A';
const BUTTER = '#FFD21F';
const KRAFT = '#B98247';

// the stopwatch dial drawn on a 2D context in a square (x0, y0, size): white, a green wedge from twelve o'clock up to five units, a red zone
// after it up to the full turn (o.full units, 8), ticks (no digits), a thick black needle at u units with a white edge; ink: a drawing (for the tag)
function drawDial(c, x0, y0, S, u, full = 8, ink = false) {
  const cx = x0 + S / 2, cy = y0 + S / 2, R = S * 0.47, a0 = -PI / 2, a5 = a0 + TAU * 5 / full;
  c.fillStyle = ink ? '#F3E6CC' : '#FBFAF4'; c.beginPath(); c.arc(cx, cy, R, 0, TAU); c.fill();
  c.fillStyle = ink ? '#4FA64A' : '#35B449'; c.beginPath(); c.moveTo(cx, cy); c.arc(cx, cy, R * 0.9, a0, a5); c.closePath(); c.fill();
  c.fillStyle = ink ? '#DE2E1F' : '#E2352B'; c.beginPath(); c.moveTo(cx, cy); c.arc(cx, cy, R * 0.9, a5, a0 + TAU); c.closePath(); c.fill();
  c.fillStyle = ink ? '#F3E6CC' : '#FBFAF4'; c.beginPath(); c.arc(cx, cy, R * 0.22, 0, TAU); c.fill();
  c.strokeStyle = INK; c.lineCap = 'round';
  for (let i = 0; i < full * 2; i++) { const a = a0 + TAU * i / (full * 2), big = i % 2 === 0; c.lineWidth = S * (big ? 0.03 : 0.016); c.beginPath(); c.moveTo(cx + Math.cos(a) * R * (big ? 0.72 : 0.8), cy + Math.sin(a) * R * (big ? 0.72 : 0.8)); c.lineTo(cx + Math.cos(a) * R * 0.92, cy + Math.sin(a) * R * 0.92); c.stroke(); }
  c.lineWidth = S * 0.05; c.beginPath(); c.arc(cx, cy, R, 0, TAU); c.stroke();
  if (u != null) { const a = a0 + TAU * u / full;
    c.strokeStyle = '#FFFFFF'; c.lineWidth = S * 0.085; c.beginPath(); c.moveTo(cx, cy); c.lineTo(cx + Math.cos(a) * R * 0.86, cy + Math.sin(a) * R * 0.86); c.stroke();
    c.strokeStyle = INK; c.lineWidth = S * 0.05; c.beginPath(); c.moveTo(cx, cy); c.lineTo(cx + Math.cos(a) * R * 0.84, cy + Math.sin(a) * R * 0.84); c.stroke();
    c.fillStyle = INK; c.beginPath(); c.arc(cx, cy, S * 0.06, 0, TAU); c.fill(); }
}
// a flat shape (THREE.Shape in metres) with a canvas painted over its bounding box (the UVs remapped to it)
function shapedPlane(shape, w, h, draw, res = 256, o = {}) {
  const geo = new THREE.ShapeGeometry(shape, 6), p = geo.attributes.position, uv = geo.attributes.uv;
  for (let i = 0; i < p.count; i++) uv.setXY(i, p.getX(i) / w + 0.5, p.getY(i) / h + 0.5);
  const cv = canvas(res, Math.round(res * h / w)); draw(cv.getContext('2d'), cv.width, cv.height);
  return new THREE.Mesh(geo, L('#FFFFFF', { map: tex(cv), ...o }));
}
// a toast slice outline (a square with a domed crown on its far side), centred, in metres
function sliceShape(W, D, k = 1) {
  const s = new THREE.Shape(), w = W * k / 2, d = D * k / 2, cr = w * 0.28;
  s.moveTo(-w, -d); s.lineTo(w, -d); s.lineTo(w, d * 0.55);
  s.bezierCurveTo(w + cr * 0.3, d + cr * 0.9, w * 0.25, d + cr * 0.7, 0, d + cr * 0.45);
  s.bezierCurveTo(-w * 0.25, d + cr * 0.7, -w - cr * 0.3, d + cr * 0.9, -w, d * 0.55);
  s.lineTo(-w, -d); return s;
}
// a 4-point star sprite texture (sparkles)
let _starTex = null;
function starTex() {
  if (_starTex) return _starTex;
  const N = 128, cv = canvas(N, N), c = cv.getContext('2d'), g = c.createRadialGradient(N / 2, N / 2, 0, N / 2, N / 2, N * 0.22);
  g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(1, 'rgba(255,255,255,0)'); c.fillStyle = g; c.fillRect(0, 0, N, N);
  c.fillStyle = '#FFFFFF'; c.beginPath();
  for (let i = 0; i < 8; i++) { const a = i * PI / 4 - PI / 2, r = i % 2 === 0 ? N * 0.48 : N * 0.07; c.lineTo(N / 2 + Math.cos(a) * r, N / 2 + Math.sin(a) * r); }
  c.closePath(); c.fill(); _starTex = tex(cv); return _starTex;
}
let _softTex = null;
function softTex() {
  if (_softTex) return _softTex;
  const N = 64, cv = canvas(N, N), c = cv.getContext('2d'), g = c.createRadialGradient(N / 2, N / 2, 0, N / 2, N / 2, N / 2);
  g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(1, 'rgba(255,255,255,0)'); c.fillStyle = g; c.fillRect(0, 0, N, N); _softTex = tex(cv); return _softTex;
}
// gingham: white ground, two crossed sets of translucent coloured bands, a few soft vertical folds
function gingham(c, W, H, col, n = 8, folds = 0) {
  c.fillStyle = '#FBF7EE'; c.fillRect(0, 0, W, H);
  const s = W / n; c.fillStyle = col; c.globalAlpha = 0.5;
  for (let x = 0; x < W; x += s * 2) c.fillRect(x, 0, s, H);
  for (let y = 0; y < H; y += s * 2) c.fillRect(0, y, W, s);
  c.globalAlpha = 1;
  for (let i = 0; i < folds; i++) { const x = W * (i + 0.5) / folds, g = c.createLinearGradient(x - s, 0, x + s, 0); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(0.5, 'rgba(60,30,20,0.18)'); g.addColorStop(1, 'rgba(0,0,0,0)'); c.fillStyle = g; c.fillRect(x - s, 0, 2 * s, H); }
}

export const TARTINE_PROPS = {

  // ---------------------------------------------------------------- the toast (pivot at the middle of the bread; the buttered face is +Y)
  // A thick slice o.w (0.3) square with a domed crown: golden crumb faces, a dark crust round the edge; on +Y a thick bright yellow butter layer
  // (inset, wavy-edged, glossy streak) and a butter pat on it, so the buttered side reads from any angle; o.butter false: dry toast.
  // o.splat [[t, v]]: the butter squeezed out flat round it on the butter face (0..1), a yellow ring on the floor when it lands butter down;
  // o.wob [[t0, amp, f, dk]]: a rock about its own Z axis (a toast teetering on its edge); o.ooze [[t, v]]: fat yellow blobs of butter squeezed
// out all round its edge on the butter face (0..1), they show from a low camera when it lies butter side down
  ttToast(o) {
    const W = o.w ?? 0.3, D = W, T = W * 0.15, g = grp(), body = grp(); g.add(body);
    const geo = new THREE.ExtrudeGeometry(sliceShape(W, D * 0.86), { depth: T, bevelEnabled: true, bevelThickness: T * 0.12, bevelSize: W * 0.02, bevelSegments: 1, curveSegments: 8 });
    geo.rotateX(-PI / 2); geo.translate(0, -T / 2, -D * 0.05);
    const crumb = L(o.crumb || '#E9B862', { flatShading: true }), crust = L(o.crust || '#9C5826', { flatShading: true });
    const bread = new THREE.Mesh(geo, [crumb, crust]); bread.castShadow = true; bread.receiveShadow = true; body.add(bread);
    if (o.butter !== false) {
      const bs = sliceShape(W, D * 0.86, 0.84), bg = new THREE.ExtrudeGeometry(bs, { depth: T * 0.32, bevelEnabled: false, curveSegments: 8 });
      bg.rotateX(-PI / 2); bg.translate(0, T / 2 + T * 0.05, -D * 0.05);
      const bm = L(BUTTER, { emissive: '#6A4A00', emissiveIntensity: 0.45, flatShading: true }); const bl = new THREE.Mesh(bg, bm); bl.castShadow = true; body.add(bl);
      const sh = box(W * 0.5, 0.004, W * 0.07, '#FFF6C2', { noGrain: true, emissive: '#B89A3A' }); sh.position.set(-W * 0.06, T / 2 + T * 0.38, W * 0.04); sh.rotation.y = 0.5; body.add(sh);
      const pat = box(W * 0.26, T * 0.55, W * 0.2, '#FFE45A', { outline: 0.004, noGrain: true, emissive: '#6A5200' }); pat.position.set(W * 0.12, T / 2 + T * 0.62, -W * 0.08); pat.rotation.y = 0.35; body.add(pat);
    }
    let splat = null;
    if (o.splat) {
      const s = new THREE.Shape(); for (let i = 0; i <= 18; i++) { const a = i / 18 * TAU, r = W * (0.62 + 0.12 * hsh(i * 3.1) + 0.06 * Math.sin(a * 5)); if (i === 0) s.moveTo(Math.cos(a) * r, Math.sin(a) * r); else s.lineTo(Math.cos(a) * r, Math.sin(a) * r); }
      const sg = new THREE.ShapeGeometry(s); sg.rotateX(-PI / 2);
      splat = new THREE.Mesh(sg, L(BUTTER, { emissive: '#6A4A00', emissiveIntensity: 0.4, polygonOffset: true, polygonOffsetFactor: -4, polygonOffsetUnits: -16, side: THREE.DoubleSide }));
      splat.position.y = T / 2 + T * 0.36; splat.receiveShadow = true; body.add(splat);
    }
    const blobs = [];
    if (o.ooze) for (let i = 0; i < 9; i++) { const a = (i + 0.3 * hsh(i)) / 9 * TAU, rr = W * (0.5 + 0.06 * hsh(i + 3)), b = sphere(W * (0.1 + 0.04 * hsh(i + 5)), BUTTER, 1);
      b.material = L(BUTTER, { emissive: '#6A4A00', emissiveIntensity: 0.45, flatShading: true }); b.position.set(Math.cos(a) * rr, T / 2 + T * 0.2, Math.sin(a) * rr * 0.86 - D * 0.05); body.add(b); blobs.push(b); }
    g.userData.update = t => {
      if (blobs.length) { const v = keyAt(o.ooze, t, 0); blobs.forEach((b, i) => { const s = Math.max(0.01, outBack(clamp01(v * 1.3 - 0.03 * i), 1.6)); b.visible = v > 0.01; b.scale.set(s * 1.3, s * 0.7, s * 1.3); }); }
      if (splat) { const v = keyAt(o.splat, t, 0); splat.visible = v > 0.01; splat.scale.setScalar(Math.max(0.01, outBack(v, 1.4))); }
      body.rotation.z = rattle(o.wob, t);
    };
    g.userData.update(0); g.userData.grip = [0, 0, 0]; return g;
  },

  // ---------------------------------------------------------------- the stopwatch (pivot at the middle of the dial, the dial facing +Z)
  // A big chrome stopwatch o.r (0.16): a white dial with a green wedge from twelve o'clock up to five, a red zone after it up to the full turn
  // (o.full, 8), ticks and no digits, a thick black needle (o.needle [[t, units]], 'lin' keys for a running needle; o.at: a fixed value), a crown
  // with its button on top and a ring; o.clicks [t...]: the button goes down for 0.08 s (sound: sfx:click in the script)
  ttStopwatch(o) {
    const R = o.r ?? 0.16, full = o.full ?? 8, g = grp();
    const caseM = cyl(R * 1.13, R * 1.13, R * 0.38, o.case || '#C3C8D0', 32, { outline: 0.006 }); caseM.rotation.x = PI / 2; caseM.position.z = -R * 0.2; g.add(caseM);
    const bez = torus(R * 1.06, R * 0.07, '#8A9099', 6, 40); bez.position.z = 0.0; g.add(bez);
    const cv = canvas(256, 256); drawDial(cv.getContext('2d'), 0, 0, 256, null, full);
    const dial = new THREE.Mesh(new THREE.CircleGeometry(R, 48), (() => { const t_ = tex(cv); return L('#FFFFFF', { map: t_, emissive: '#FFFFFF', emissiveMap: t_, emissiveIntensity: 0.3 }); })()); dial.position.z = 0.002; g.add(dial);
    const nd = grp(), nl = box(R * 0.11, R * 0.86, 0.012, INK, { pivot: 'bottom', noGrain: true }), nw = box(R * 0.19, R * 0.9, 0.006, '#FFFFFF', { pivot: 'bottom', noGrain: true });
    nw.position.z = -0.004; nd.add(nw, nl, at(cyl(R * 0.1, R * 0.1, 0.02, INK, 12), 0, 0, 0.004, PI / 2)); nd.position.z = 0.012; g.add(nd);
    g.add(at(cyl(R * 0.12, R * 0.12, R * 0.3, '#A9AFB8', 10), 0, R * 1.24, -R * 0.15));
    const btn = at(cyl(R * 0.2, R * 0.2, R * 0.16, '#D7DBE1', 12, { outline: 0.004 }), 0, R * 1.45, -R * 0.15); g.add(btn);
    const ring = torus(R * 0.26, R * 0.05, '#A9AFB8', 6, 18); ring.position.set(0, R * 1.68, -R * 0.15); g.add(ring);
    const side = at(cyl(R * 0.09, R * 0.09, R * 0.22, '#D7DBE1', 8), R * 0.9, R * 0.9, -R * 0.15, 0, 0, -PI / 4); g.add(side);
    g.userData.update = t => {
      const u = o.needle ? keyAt(o.needle, t, 0) : (o.at ?? 0); nd.rotation.z = -TAU * u / full;
      let p = 0; for (const c of o.clicks || []) { const d = t - c; if (d >= 0 && d < 0.1) p = 1; }
      btn.position.y = R * (1.45 - 0.14 * p);
    };
    g.userData.update(0); g.userData.grip = [0, -R * 0.9, -R * 0.2]; return g;
  },

  // ---------------------------------------------------------------- the big brown luggage tag worn round the neck (pivot at its eyelet, the card
  // hanging below, its front +Z): a kraft card o.w (0.24) x o.h (0.34) with clipped top corners, a dark brown border, a white reinforcing ring
  // round the eyelet and three ruled lines; its back: the same card with a big stopwatch drawing, the needle at o.needle units (the owner's time);
  // a string from the eyelet up to the collar on both sides (o.cord [dx, dy, dz] of its top ends, toward the neck); o.flip [[t, 0..1]]: turned
  // round about its vertical axis (1: the back to the front); o.swing [[t0, amp, f, dk]]: it swings about the eyelet; o.color: the card;
// o.backFull: the full turn of the drawn dial (8; a larger one shrinks the green wedge so the red zone dominates the drawing)
  ttTag(o) {
    const W = o.w ?? 0.24, H = o.h ?? 0.34, g = grp(), card = grp(); g.add(card);
    const cutK = 0.22, sh = new THREE.Shape();
    sh.moveTo(-W / 2, -H / 2); sh.lineTo(W / 2, -H / 2); sh.lineTo(W / 2, H / 2 - W * cutK); sh.lineTo(W / 2 - W * cutK, H / 2); sh.lineTo(-W / 2 + W * cutK, H / 2); sh.lineTo(-W / 2, H / 2 - W * cutK); sh.lineTo(-W / 2, -H / 2);
    const col = o.color || KRAFT;
    const front = (c, w, h) => {
      const gr = c.createLinearGradient(0, 0, w, h); gr.addColorStop(0, col); gr.addColorStop(1, '#A06C36'); c.fillStyle = gr; c.fillRect(0, 0, w, h);
      c.strokeStyle = '#5E3A18'; c.lineWidth = w * 0.06; c.strokeRect(w * 0.06, h * 0.05, w * 0.88, h * 0.9);
      c.fillStyle = '#F4EEE2'; c.beginPath(); c.arc(w / 2, h * 0.13, w * 0.13, 0, TAU); c.fill(); c.fillStyle = '#3A2410'; c.beginPath(); c.arc(w / 2, h * 0.13, w * 0.06, 0, TAU); c.fill();
      c.fillStyle = '#5E3A18'; for (const y of [0.52, 0.66, 0.8]) c.fillRect(w * 0.18, h * y, w * 0.64, h * 0.025);
    };
    const back = (c, w, h) => { front(c, w, h); c.fillStyle = col; c.fillRect(w * 0.12, h * 0.26, w * 0.76, h * 0.64); drawDial(c, w * 0.12, h * 0.3 + (h * 0.6 - w * 0.76) / 2, w * 0.76, o.needle ?? 7, o.backFull ?? 8, true); };
    const F = shapedPlane(sh, W, H, front, 256, { side: THREE.FrontSide }), Bk = shapedPlane(sh, W, H, back, 256, { side: THREE.FrontSide });
    F.position.z = 0.004; Bk.rotation.y = PI; Bk.position.z = -0.004; F.castShadow = true; Bk.castShadow = true;
    const edge = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: 0.006, bevelEnabled: false }), L('#6E4420')); edge.position.z = -0.003;
    card.add(edge, F, Bk); card.position.y = -H / 2 + H * 0.06;
    const cd = o.cord || [0.11, 0.22, -0.06], cord = '#4E3A26';
    g.add(rod([0, 0, 0.004], [cd[0], cd[1], cd[2]], 0.006, cord), rod([0, 0, 0.004], [-cd[0], cd[1], cd[2]], 0.006, cord));
    g.userData.update = t => { card.rotation.y = PI * keyAt(o.flip, t, 0); g.rotation.z = rattle(o.swing, t); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the kitchen table under a long gingham cloth (pivot at the floor centre)
  // A top o.w (1.5) x o.d (0.9) at o.h (1.05) under a cloth whose skirt falls on all four sides to o.gap (0.04) over the floor; the front skirt
  // (+Z) is two halves: o.open [[t, 0..1]] draws them aside like curtains (gathered at the corners), o.lift [[t, 0..1]] lifts the whole front
  // skirt outward and up (someone crawls out); o.front false: no front skirt (a camera inside); o.cloth: the check colour; o.sides [left, right]:
  // false drops that side skirt (someone crawls in from the side)
  ttTable(o) {
    const W = o.w ?? 1.5, Dd = o.d ?? 0.9, Hh = o.h ?? 1.05, gap = o.gap ?? 0.04, col = o.cloth || '#D9473E', g = grp(), m = 0.05;
    g.add(at(box(W, 0.06, Dd, '#A8743E', { outline: 0.006 }), 0, Hh - 0.03, 0));
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(at(box(0.07, Hh - 0.06, 0.07, '#7A5230', { pivot: 'bottom' }), sx * (W / 2 - 0.1), 0, sz * (Dd / 2 - 0.1)));
    const top = new THREE.Mesh(new THREE.BoxGeometry(W + 2 * m, 0.012, Dd + 2 * m), L('#FFFFFF', { map: tex((() => { const cv = canvas(256, Math.round(256 * (Dd + 2 * m) / (W + 2 * m))); gingham(cv.getContext('2d'), cv.width, cv.height, col, 10); return cv; })()) }));
    top.position.y = Hh + 0.006; top.receiveShadow = true; top.castShadow = true; g.add(top);
    const SH = Hh + 0.012 - gap;
    const panel = (w, folds) => { const cv = canvas(256, Math.round(256 * SH / w)); gingham(cv.getContext('2d'), cv.width, cv.height, col, Math.max(4, Math.round(10 * w / (W + 2 * m))), folds);
      const p = new THREE.Mesh(new THREE.PlaneGeometry(w, SH).translate(0, -SH / 2, 0), L('#FFFFFF', { map: tex(cv), side: THREE.DoubleSide })); p.castShadow = true; p.receiveShadow = true; return p; };
    const back = panel(W + 2 * m, 5); back.position.set(0, Hh + 0.012, -Dd / 2 - m); g.add(back);
    const sides = o.sides || [true, true];
    for (const s of [-1, 1]) { if (!sides[s > 0 ? 1 : 0]) continue; const p = panel(Dd + 2 * m, 3); p.rotation.y = PI / 2; p.position.set(s * (W / 2 + m), Hh + 0.012, 0); g.add(p); }
    const lift = grp(); lift.position.set(0, Hh + 0.012, Dd / 2 + m); g.add(lift);
    const halves = [];
    if (o.front !== false) for (const s of [-1, 1]) {
      const hw = (W + 2 * m) / 2, piv = grp(), p = panel(hw, 3); p.position.x = -s * hw / 2; piv.position.x = s * hw; piv.add(p); lift.add(piv); halves.push(piv);
    }
    g.userData.update = t => {
      const op = keyAt(o.open, t, 0), lf = keyAt(o.lift, t, 0);
      halves.forEach(h => { h.scale.x = Math.max(0.16, 1 - 0.84 * op); h.scale.z = 1 + 2 * op; });
      lift.rotation.x = -1.35 * lf;
    };
    g.userData.update(0); g.userData.top = [0, Hh + 0.012, 0]; return g;
  },

  // ---------------------------------------------------------------- a white plate (pivot at its underside): o.r (0.17)
  ttPlate(o) {
    const R = o.r ?? 0.17;
    return grp(at(cyl(R * 0.62, R * 0.55, 0.012, '#E9ECEF', 20), 0, 0.006, 0), at(cyl(R, R * 0.66, 0.03, '#FBFCFD', 28, { outline: 0.004 }), 0, 0.027, 0), at(cyl(R * 0.62, R * 0.62, 0.004, '#F1F3F5', 24), 0, 0.03, 0));
  },

  // ---------------------------------------------------------------- the inspector's home under the table: a big white pillow with a blue ticking
  // stripe (pivot at its middle), o.w (0.75) x o.h (0.42) x o.d (0.2)
  ttPillow(o) {
    const w = o.w ?? 0.75, h = o.h ?? 0.42, d = o.d ?? 0.2;
    return grp(at(box(w, h, d, '#F6F3EA', { outline: 0.012, taper: { x: 0.9, z: 0.7 } }), 0, 0, 0), at(box(w * 0.9, h * 0.1, d * 0.78, '#7EA6D8'), 0, h * 0.18, 0), at(box(w * 0.9, h * 0.1, d * 0.78, '#7EA6D8'), 0, -h * 0.18, 0));
  },
  // a small bedside lamp standing on the floor (pivot at the floor): a round base, a stem, a cream shade that glows, a warm point light (o.power 1.2)
  ttNookLamp(o) {
    const s = o.s ?? 1, g = grp();
    g.add(at(cyl(0.08 * s, 0.09 * s, 0.03 * s, '#5A3A28', 14, { outline: 0.004 }), 0, 0.015 * s, 0), at(cyl(0.012 * s, 0.012 * s, 0.26 * s, '#C9A55A', 6, { pivot: 'bottom' }), 0, 0.03 * s, 0));
    const shade = cyl(0.07 * s, 0.12 * s, 0.13 * s, '#FFE7B0', 16, { emissive: '#E8A040', noGrain: true }); shade.position.y = 0.3 * s; shade.castShadow = false; g.add(shade);
    const lt = new THREE.PointLight('#FFC27A', o.power ?? 1.2, o.range ?? 2.2, 1.4); lt.position.set(0, 0.26 * s, 0.05); g.add(lt);
    const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: softTex(), color: '#FFD08A', transparent: true, opacity: 0.55, depthWrite: false, blending: THREE.AdditiveBlending })); halo.position.y = 0.28 * s; halo.scale.setScalar(0.42 * s); g.add(halo);
    return g;
  },
  // a big mug (pivot at its foot) o.r (0.07), a handle, steam-free
  ttMug(o) {
    const R = o.r ?? 0.07, c = o.color || '#E8573C';
    return grp(at(cyl(R, R * 0.92, R * 2.0, c, 14, { pivot: 'bottom', outline: 0.004 }), 0, 0, 0), at(cyl(R * 0.86, R * 0.86, 0.006, '#5A3420', 12), 0, R * 1.9, 0), at(torus(R * 0.5, R * 0.14, c, 5, 10), R * 1.05, R, 0, 0, 0, 0));
  },

  // ---------------------------------------------------------------- the stamped form held up to the camera (pivot at its middle, facing +Z)
  // An official sheet o.w (0.42) x o.h (0.56): a grey header band, boxes and blank lines (no words, no digits); o.stampAt t: a big red stamp mark
  // pops onto it (two toast icons inside a double frame, slightly tilted) with an overshoot and ink specks
  ttForm(o) {
    const W = o.w ?? 0.42, Hh = o.h ?? 0.56, g = grp();
    const sheet = (stamp, sc) => (c, w, h) => {
      c.fillStyle = '#FBFAF6'; c.fillRect(0, 0, w, h); c.fillStyle = '#9AA3AE'; c.fillRect(w * 0.06, h * 0.04, w * 0.88, h * 0.08);
      c.fillStyle = '#C3C9D0'; for (let i = 0; i < 8; i++) c.fillRect(w * 0.08, h * (0.2 + i * 0.075), w * (i % 3 === 2 ? 0.5 : 0.84), h * 0.012);
      c.strokeStyle = '#9AA3AE'; c.lineWidth = w * 0.01; for (let i = 0; i < 3; i++) c.strokeRect(w * (0.08 + i * 0.1), h * 0.84, w * 0.06, w * 0.06);
      if (!stamp) return;
      c.save(); c.translate(w * 0.52, h * 0.5); c.rotate(-0.16); c.scale(sc, sc); const sw = w * 0.8, sh2 = h * 0.4;
      c.strokeStyle = '#D42A22'; c.lineWidth = w * 0.035; c.strokeRect(-sw / 2, -sh2 / 2, sw, sh2); c.lineWidth = w * 0.014; c.strokeRect(-sw / 2 + w * 0.04, -sh2 / 2 + w * 0.04, sw - w * 0.08, sh2 - w * 0.08);
      c.fillStyle = '#D42A22';
      for (const dx of [-0.19, 0.19]) { c.save(); c.translate(w * dx, h * 0.01); const tw = w * 0.24;
        c.beginPath(); c.moveTo(-tw / 2, tw * 0.5); c.lineTo(tw / 2, tw * 0.5); c.lineTo(tw / 2, -tw * 0.2); c.bezierCurveTo(tw * 0.62, -tw * 0.62, tw * 0.1, -tw * 0.66, 0, -tw * 0.56); c.bezierCurveTo(-tw * 0.1, -tw * 0.66, -tw * 0.62, -tw * 0.62, -tw / 2, -tw * 0.2); c.closePath(); c.fill();
        c.fillStyle = '#FBFAF6'; c.fillRect(-tw * 0.32, -tw * 0.18, tw * 0.64, tw * 0.1); c.fillStyle = '#D42A22'; c.restore(); }
      for (let i = 0; i < 14; i++) { c.beginPath(); c.arc((hsh(i) - 0.5) * sw * 1.1, (hsh(i + 9) - 0.5) * sh2 * 1.3, w * 0.008 * (1 + hsh(i + 4)), 0, TAU); c.fill(); }
      c.restore();
    };
    const mk = draw => { const cv = canvas(256, Math.round(256 * Hh / W)); draw(cv.getContext('2d'), cv.width, cv.height); const m = new THREE.Mesh(new THREE.PlaneGeometry(W, Hh), L('#FFFFFF', { map: tex(cv) })); m.position.z = 0.003; return m; };
    const blank = mk(sheet(false)), stamped = mk(sheet(true, 1)), big = mk(sheet(true, 1.25));
    g.add(at(box(W + 0.01, Hh + 0.01, 0.004, '#E4E2DA'), 0, 0, 0), blank, stamped, big);
    g.userData.update = t => { const d = o.stampAt == null ? -1 : t - o.stampAt; blank.visible = d < 0; big.visible = d >= 0 && d < 0.07; stamped.visible = d >= 0.07; };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the wall chart (pivot at its nail, facing +Z): a framed board o.w (1.5) x
  // o.h (1.1) hanging from a nail, a pale grid and a huge green arrow rising steeply out through its top-right corner; o.grow [t0, t1]: the
  // arrow shoots up; o.fall [t0, t1]: it comes off the nail, turns over as it drops and lands upside down leaning on the wall (the arrow now
  // pointing down) with a bounce; o.floor: the floor height under the nail (m, default 2.3 below it); o.plain: no grid (a clean board);
  // o.thick: the arrow's width (1); o.frameW: the frame's margin (0.08); o.paper: the board's colour; o.burst: see below
  ttChart(o) {
    const W = o.w ?? 1.5, Hh = o.h ?? 1.1, g = grp(), board = grp(); g.add(board);
    g.add(at(cyl(0.015, 0.015, 0.08, '#3A3D44', 6), 0, 0, 0.02, PI / 2));
    const N = 10, frames = [];
    const draw = f => (c, w, h) => {
      c.fillStyle = o.paper || '#FBFAF4'; c.fillRect(0, 0, w, h); c.strokeStyle = 'rgba(40,60,90,0.18)'; c.lineWidth = h * 0.006;
      if (!o.plain) for (let i = 1; i < 6; i++) { c.beginPath(); c.moveTo(0, h * i / 6); c.lineTo(w, h * i / 6); c.stroke(); c.beginPath(); c.moveTo(w * i / 6, 0); c.lineTo(w * i / 6, h); c.stroke(); }
      c.strokeStyle = '#2E3440'; c.lineWidth = h * 0.02; c.beginPath(); c.moveTo(w * 0.08, h * 0.06); c.lineTo(w * 0.08, h * 0.92); c.lineTo(w * 0.96, h * 0.92); c.stroke();
      const pts = [], n = 40; for (let i = 0; i <= n * f; i++) { const u = i / n; pts.push([w * (0.1 + 0.74 * u), h * (0.86 - 0.95 * Math.pow(u, 2.2) - 0.03 * Math.sin(u * 22) * (1 - u))]); }
      if (pts.length < 2) return;
      const th = o.thick ?? 1; c.strokeStyle = '#1F8A3A'; c.lineWidth = h * 0.13 * th; c.lineJoin = 'round'; c.lineCap = 'round'; c.beginPath(); pts.forEach(([x, y], i) => i ? c.lineTo(x, y) : c.moveTo(x, y)); c.stroke();
      c.strokeStyle = '#3CC45A'; c.lineWidth = h * 0.085 * th; c.beginPath(); pts.forEach(([x, y], i) => i ? c.lineTo(x, y) : c.moveTo(x, y)); c.stroke();
      const [x1, y1] = pts[pts.length - 1], [x0, y0] = pts[Math.max(0, pts.length - 4)], a = Math.atan2(y1 - y0, x1 - x0), s = h * 0.2;
      c.fillStyle = '#3CC45A'; c.strokeStyle = '#1F8A3A'; c.lineWidth = h * 0.02; c.beginPath(); c.moveTo(x1 + Math.cos(a) * s, y1 + Math.sin(a) * s); c.lineTo(x1 + Math.cos(a + 2.4) * s, y1 + Math.sin(a + 2.4) * s); c.lineTo(x1 + Math.cos(a - 2.4) * s, y1 + Math.sin(a - 2.4) * s); c.closePath(); c.fill(); c.stroke();
    };
    const frameC = o.frame || '#3A2E28';
    const fw = o.frameW ?? 0.08; board.add(at(box(W + fw, Hh + fw, 0.04, frameC, { outline: 0.006 }), 0, -Hh / 2 - 0.06, -0.02));
    for (let i = 0; i < N; i++) { const cv = canvas(512, Math.round(512 * Hh / W)); draw((i + 1) / N)(cv.getContext('2d'), cv.width, cv.height); const p = new THREE.Mesh(new THREE.PlaneGeometry(W, Hh), L('#FFFFFF', { map: tex(cv) })); p.position.set(0, -Hh / 2 - 0.06, 0.002); p.visible = false; board.add(p); frames.push(p); }
    board.add(rod([0, 0, 0.01], [-W * 0.3, -0.06, 0.01], 0.006, '#2E2622'), rod([0, 0, 0.01], [W * 0.3, -0.06, 0.01], 0.006, '#2E2622'));
    // o.burst (m): a thick 3D arrow that bursts out of the board's top edge where the curve leaves it, tilted o.burstAng (0.47 rad) to the right
    let burst = null;
    if (o.burst) {
      const L0 = o.burst, sw = Hh * 0.11 * (o.thick ?? 1), hw = sw * 2.3, hl = sw * 2.4, a = new THREE.Shape();
      a.moveTo(-sw / 2, 0); a.lineTo(sw / 2, 0); a.lineTo(sw / 2, L0 - hl); a.lineTo(hw / 2, L0 - hl); a.lineTo(0, L0); a.lineTo(-hw / 2, L0 - hl); a.lineTo(-sw / 2, L0 - hl); a.lineTo(-sw / 2, 0);
      const front = new THREE.Mesh(new THREE.ExtrudeGeometry(a, { depth: 0.05, bevelEnabled: false }), L('#3CC45A', { emissive: '#1F8A3A', emissiveIntensity: 0.25 }));
      const rim = new THREE.Mesh(new THREE.ShapeGeometry(a), L('#145C27')); rim.scale.set(1.18, 1.04, 1); rim.position.set(0, -0.02, -0.004);
      const piv = grp(); piv.add(rim, front); piv.rotation.z = -(o.burstAng ?? 0.47); piv.position.set(W * 0.307, -0.1, 0.03); board.add(piv); burst = piv;
    }
    const drop = o.floor ?? 2.3, cy0 = -Hh / 2 - 0.06;
    g.userData.update = t => {
      const u = o.grow ? clamp01((t - o.grow[0]) / Math.max(0.01, o.grow[1] - o.grow[0])) : 1, i = Math.max(0, Math.min(N - 1, Math.ceil(u * N) - 1)); frames.forEach((f, j) => { f.visible = j === i; });
      if (burst) { const g0 = o.grow ? o.grow[0] + 0.55 * (o.grow[1] - o.grow[0]) : -9, d = o.grow ? 0.45 * (o.grow[1] - o.grow[0]) + 0.1 : 1, v = clamp01((t - g0) / d); burst.visible = v > 0.01; burst.scale.set(1, Math.max(0.01, outBack(v, 1.6)), 1); }
      if (!o.fall) return;
      const v = clamp01((t - o.fall[0]) / Math.max(0.01, o.fall[1] - o.fall[0])), landed = t - o.fall[1];
      const yc = lerp(cy0, -drop + Hh / 2 + 0.06, v * v), bounce = landed > 0 ? Math.abs(Math.sin(landed * 22)) * 0.05 * Math.exp(-landed * 7) : 0;
      const rz = PI * smooth(v) + (landed > 0 ? rattle([[o.fall[1], 0.06, 26, 6]], t) : 0.25 * Math.sin(v * PI));
      board.rotation.set(-0.14 * smooth((v - 0.7) / 0.3), 0, rz);
      board.position.set(cy0 * Math.sin(rz), yc + bounce - cy0 * Math.cos(rz), 0.06 * smooth((v - 0.7) / 0.3));
    };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a round floor polisher (pivot at the floor centre, the handle toward -Z)
  // A round base o.r (0.34) with a rubber bumper, a dark pad that spins under it, a motor dome, a shaft rising back to a T handle at about 1.15 m;
  // o.hum: it buzzes (a small jitter); o.color; o.run [[t, v]]: the motor's speed (1 running, 0 dead stop, above 1 bucking: the jitter grows)
  ttPolisher(o) {
    const R = o.r ?? 0.34, c = o.color || '#D8452F', g = grp(), body = grp(); g.add(body);
    body.add(at(cyl(R * 0.96, R * 0.96, 0.04, '#2A2C31', 20), 0, 0.02, 0));
    const pad = grp(at(cyl(R * 0.94, R * 0.94, 0.03, '#3E4148', 16), 0, 0.0, 0)); for (let i = 0; i < 4; i++) pad.add(at(box(R * 1.7, 0.032, 0.03, '#5A5E66'), 0, 0.0, 0, 0, i * PI / 4, 0)); pad.position.y = 0.035; body.add(pad);
    body.add(at(cyl(R, R * 1.02, 0.16, c, 24, { outline: 0.006 }), 0, 0.13, 0), at(torus(R * 1.02, 0.035, '#1E2024', 6, 28), 0, 0.08, 0, PI / 2));
    body.add(at(cyl(R * 0.55, R * 0.7, 0.16, '#E9ECEF', 18, { outline: 0.005 }), 0, 0.29, -R * 0.1), at(sphere(R * 0.5, '#E9ECEF', 1), 0, 0.37, -R * 0.1));
    const hb = [0, 0.3, -R * 0.4], ht = [0, 1.12, -0.62]; body.add(rod(hb, ht, 0.022, '#B7BCC4', 8), rod([ht[0] - 0.24, ht[1], ht[2]], [ht[0] + 0.24, ht[1], ht[2]], 0.026, '#2A2C31', 8));
    for (const s of [-1, 1]) body.add(at(cyl(0.032, 0.032, 0.12, '#1E2024', 8), ht[0] + s * 0.26, ht[1], ht[2], 0, 0, PI / 2));
    const spin = t => { if (!o.run) return t * 28; let a = 0; const n = Math.max(1, Math.ceil(Math.abs(t) * 60)), h = t / n; for (let i = 0; i < n; i++) a += keyAt(o.run, (i + 0.5) * h, 1) * h; return a * 28; };
    g.userData.update = t => { pad.rotation.y = spin(t); const v = o.run ? keyAt(o.run, t, 1) : 1;
      if (o.hum !== false) { body.position.set(Math.sin(t * 61) * 0.004 * v, Math.abs(Math.sin(t * 47)) * 0.005 * v, Math.cos(t * 53) * 0.004 * v); body.rotation.y = v > 1 ? Math.sin(t * 37) * 0.06 * (v - 1) : 0; } };
    g.userData.update(0); g.userData.handle = ht; return g;
  },

  // ---------------------------------------------------------------- sparkles on a gleaming floor (pivot anywhere): 4-point white stars at
  // o.pts [[x, y, z, t0, size], ...] that pop open and shut in 0.4 s; o.period: each one comes back that often
  ttSparkle(o) {
    const g = grp(), ps = (o.pts || []).map(([x, y, z, t0, s]) => { const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: starTex(), color: o.color || '#FFFFFF', transparent: true, depthWrite: false, opacity: 0.95 })); sp.position.set(x, y, z); g.add(sp); return { sp, t0, s: s ?? 0.25 }; });
    g.userData.update = t => { for (const p of ps) { let d = t - p.t0; if (o.period && d > 0) d %= o.period; const v = d >= 0 && d < 0.4 ? Math.sin(PI * d / 0.4) : 0; p.sp.visible = v > 0.02; p.sp.scale.setScalar(Math.max(0.01, p.s * v)); p.sp.material.rotation = d * 2; } };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a gleaming waxed floor (pivot at its middle, on the floor): a sheet o.w x o.d
  // painted with soft diagonal white sheen streaks and a few bright glints (transparent, depth-tested, a polygon offset toward the camera);
  // o.tint: a faint colour over the floor under it (o.tintA its strength, 0.25); o.k: streak strength (1), o.n: streak count (7), o.wide: streak
// width (1), o.glints: bright dabs (0)
  ttShine(o) {
    const w = o.w ?? 6, d = o.d ?? 6, N = 512, cv = canvas(N, Math.round(N * d / w)), c = cv.getContext('2d'), H = cv.height;
    if (o.tint) { c.fillStyle = o.tint; c.globalAlpha = o.tintA ?? 0.25; c.fillRect(0, 0, N, H); c.globalAlpha = 1; }
    const nS = o.n ?? 7, kS = o.k ?? 1;
    for (let i = 0; i < nS; i++) { const x = N * (i / (nS - 1)) + (hsh(i) - 0.5) * N * 0.1, gw = N * (0.04 + 0.05 * hsh(i + 2)) * (o.wide ?? 1);
      c.save(); c.translate(x, H / 2); c.rotate(0.5); const gr = c.createLinearGradient(-gw, 0, gw, 0); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(0.5, `rgba(255,255,255,${Math.min(1, (0.35 + 0.25 * hsh(i + 5)) * kS)})`); gr.addColorStop(1, 'rgba(255,255,255,0)'); c.fillStyle = gr; c.fillRect(-gw, -H, 2 * gw, 2 * H); c.restore(); }
    for (let i = 0; i < (o.glints ?? 0); i++) { const x = N * hsh(i * 3.1 + 7), y = H * hsh(i * 5.7 + 2), r0 = N * (0.012 + 0.018 * hsh(i + 11)), gg = c.createRadialGradient(x, y, 0, x, y, r0 * 3);
      gg.addColorStop(0, 'rgba(255,255,255,1)'); gg.addColorStop(0.3, 'rgba(255,255,255,0.7)'); gg.addColorStop(1, 'rgba(255,255,255,0)'); c.fillStyle = gg; c.beginPath(); c.ellipse(x, y, r0 * 3.4, r0 * 1.6, 0.5, 0, TAU); c.fill(); }
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, d).rotateX(-PI / 2), new THREE.MeshBasicMaterial({ map: tex(cv), transparent: true, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -6, polygonOffsetUnits: -20 }));
    m.position.y = o.y ?? 0.012; m.renderOrder = 1; return grp(m);
  },

  // ---------------------------------------------------------------- a white napkin tucked into a collar (pivot at its top edge, facing +Z): a
  // triangle o.w (0.36) wide hanging o.h (0.4), a fold line, a little bulge
  ttNapkin(o) {
    const w = o.w ?? 0.36, h = o.h ?? 0.4, s = new THREE.Shape(); s.moveTo(-w / 2, 0); s.lineTo(w / 2, 0); s.lineTo(w * 0.06, -h); s.lineTo(-w * 0.06, -h); s.lineTo(-w / 2, 0);
    const m = new THREE.Mesh(new THREE.ExtrudeGeometry(s, { depth: 0.012, bevelEnabled: false }), L('#FBFBF8', { flatShading: true })); m.castShadow = true;
    return grp(m, at(box(w * 0.04, h * 0.8, 0.004, '#D8DCE0'), 0, -h * 0.45, 0.014), at(box(w * 0.55, 0.035, 0.03, '#FBFBF8', { outline: 0.004 }), 0, -0.01, 0.01));
  },

  // ---------------------------------------------------------------- a waiter's tower of plates on a round tray (pivot at the tray's underside)
  // o.n (12) white plates stacked o.step (0.035) apart, a steel tray o.r (0.26); o.sway [[t0, amp]]: a lean (none: it does not wobble)
  ttPlateTower(o) {
    const n = o.n ?? 12, st = o.step ?? 0.035, R = o.r ?? 0.26, g = grp(), stack = grp(); g.add(stack);
    g.add(at(cyl(R, R, 0.02, '#C9CED6', 24, { outline: 0.005 }), 0, 0.01, 0));
    for (let i = 0; i < n; i++) stack.add(at(cyl(0.16, 0.12, 0.028, i % 2 ? '#FBFCFD' : '#EEF1F4', 20, { outline: 0.004 }), (hsh(i) - 0.5) * 0.012, 0.035 + i * st, (hsh(i + 7) - 0.5) * 0.012));
    g.userData.update = t => { stack.rotation.z = rattle(o.sway, t); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a café front (pivot at the foot of its wall, facing +Z): a cream wall o.w (6)
  // x o.h (4), a big window with a dark-green frame, a door, a striped red-and-white awning over both with a scalloped valance, a plain board
  // reading o.sign ('CAFÉ'); o.awning color
  ttCafeFront(o) {
    const W = o.w ?? 6, Hh = o.h ?? 4, g = grp(), ac = o.awning || '#C8322A', fr = '#2E5A3E';
    g.add(at(box(W, Hh, 0.2, o.wall || '#EFE2C4'), 0, Hh / 2, -0.1), at(box(W, 0.5, 0.06, '#8E6A48'), 0, 0.25, 0.02));
    g.add(at(box(2.6, 1.7, 0.04, '#3E5A6A', { emissive: '#22323A' }), -0.9, 1.55, 0.02));
    for (const [x, y, w, h] of [[-0.9, 0.7, 2.7, 0.08], [-0.9, 2.4, 2.7, 0.08], [-2.2, 1.55, 0.08, 1.78], [0.4, 1.55, 0.08, 1.78], [-0.9, 1.55, 0.06, 1.7]]) g.add(at(box(w, h, 0.07, fr, { outline: 0.004 }), x, y, 0.04));
    g.add(at(box(1.0, 2.3, 0.06, fr, { pivot: 'bottom', outline: 0.004 }), 1.5, 0, 0.03), at(box(0.7, 1.2, 0.02, '#3E5A6A', { emissive: '#22323A' }), 1.5, 1.4, 0.07));
    const N = 256, cv = canvas(N, 64), c = cv.getContext('2d'); for (let i = 0; i < 8; i++) { c.fillStyle = i % 2 ? '#FBF6EC' : ac; c.fillRect(i * N / 8, 0, N / 8 + 1, 64); }
    const aw = new THREE.Mesh(new THREE.PlaneGeometry(W * 0.86, 1.2), L('#FFFFFF', { map: tex(cv), side: THREE.DoubleSide })); aw.position.set(0, 2.95, 0.55); aw.rotation.x = -1.05; aw.castShadow = true; g.add(aw);
    for (let i = 0; i < 16; i++) { const x = -W * 0.43 + (i + 0.5) * W * 0.86 / 16; const v = new THREE.Mesh(new THREE.CircleGeometry(W * 0.86 / 32, 10, PI, PI), L(i % 2 ? '#FBF6EC' : ac, { side: THREE.DoubleSide })); v.position.set(x, 2.43, 1.06); g.add(v); }
    g.add(at(box(W * 0.86, 0.14, 0.02, ac), 0, 2.49, 1.05));
    // (review 2) the board taller and the acute accent drawn as a thick stroke of its own: at phone size the font's accent vanished (« CAFE »)
    if (o.sign !== false) { const sc = canvas(256, 96), x = sc.getContext('2d'), word = (o.sign || 'CAFÉ').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      x.fillStyle = fr; x.fillRect(0, 0, 256, 96); x.fillStyle = '#F4E6B8'; x.font = '900 50px Arial'; x.textAlign = 'center'; x.textBaseline = 'alphabetic'; x.fillText(word, 128, 82);
      if (/É/.test(o.sign || 'CAFÉ')) { const tw = x.measureText(word).width, ex = 128 + tw / 2 - x.measureText('E').width * 0.42;
        x.beginPath(); x.moveTo(ex - 9, 30); x.lineTo(ex + 5, 10); x.lineTo(ex + 16, 14); x.lineTo(ex - 1, 32); x.closePath(); x.fill(); }
      g.add(at(new THREE.Mesh(new THREE.PlaneGeometry(1.6, 0.6), L('#FFFFFF', { map: tex(sc) })), -0.9, 3.5, 0.05)); }
    return g;
  },

  // ---------------------------------------------------------------- a long straight council desk (pivot at the floor centre, the councillors'
  // side -Z): a wood top o.w (4) x 0.6 at 0.8, a front modesty panel, a short microphone per seat at o.mics [x...]
  ttCouncilDesk(o) {
    const W = o.w ?? 4, g = grp(), wc = o.color || '#7A5232';
    g.add(at(box(W, 0.06, 0.6, wc, { outline: 0.006 }), 0, 0.79, 0), at(box(W, 0.74, 0.04, wc, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0.28), at(box(W, 0.05, 0.05, '#C9A55A'), 0, 0.6, 0.31));
    for (const x of o.mics || []) g.add(at(cyl(0.04, 0.05, 0.03, INK, 10), x, 0.835, 0.1), rod([x, 0.84, 0.1], [x, 1.0, 0.22], 0.008, INK), at(sphere(0.025, INK, 1), x, 1.0, 0.22));
    return g;
  },

  // ---------------------------------------------------------------- a plain coloured wall sign (pivot at its middle, facing +Z): o.text on o.bg
  ttSign(o) {
    const W = o.w ?? 2.2, Hh = o.h ?? 0.45, cv = canvas(512, Math.round(512 * Hh / W)), c = cv.getContext('2d');
    c.fillStyle = o.bg || '#2E5A8A'; c.fillRect(0, 0, cv.width, cv.height); c.fillStyle = o.fg || '#F4EFE2'; c.textAlign = 'center'; c.textBaseline = 'middle';
    let fs = cv.height * 0.56; c.font = `900 ${fs}px Arial`; const tw = c.measureText(o.text || '').width; if (tw > cv.width * 0.9) { fs *= cv.width * 0.9 / tw; c.font = `900 ${fs}px Arial`; } c.fillText(o.text || '', cv.width / 2, cv.height * 0.54);
    return grp(at(box(W + 0.06, Hh + 0.06, 0.03, o.frame || '#C9A55A'), 0, 0, -0.016), new THREE.Mesh(new THREE.PlaneGeometry(W, Hh), L('#FFFFFF', { map: tex(cv) })));
  },

  // ---------------------------------------------------------------- a section wall between two flats of a cut-away building (pivot at the floor
  // at its front edge, running back along -Z): a thick partition o.t (0.36) x o.h (3.0) x o.d (5), its front face the dark hatched section of
  // a cut wall, with the cut floor slab and ceiling slab at its foot and head (sections too)
  ttCutWall(o) {
    const T = o.t ?? 0.36, Hh = o.h ?? 3.0, Dd = o.d ?? 5, g = grp(), sec = '#5A4C44';
    g.add(at(box(T, Hh, Dd, o.wall || '#EFE6D2', { pivot: 'bottom' }), 0, 0, -Dd / 2));
    const cv = canvas(64, 512), c = cv.getContext('2d'); c.fillStyle = sec; c.fillRect(0, 0, 64, 512); c.strokeStyle = 'rgba(255,255,255,0.22)'; c.lineWidth = 4; for (let y = -64; y < 600; y += 22) { c.beginPath(); c.moveTo(0, y); c.lineTo(64, y + 40); c.stroke(); }
    g.add(at(new THREE.Mesh(new THREE.PlaneGeometry(T + 0.02, Hh), L('#FFFFFF', { map: tex(cv) })), 0, Hh / 2, 0.002));
    if (o.slabs !== false) { const sw = o.slabW ?? 14; g.add(at(box(sw, 0.3, 0.3, sec), 0, Hh + 0.15, -0.15), at(box(sw, 0.03, 0.02, '#EFE6D2'), 0, Hh, 0.01)); }
    return g;
  },

  // ---------------------------------------------------------------- a soft blob of light on the faces (no visible source; pivot at the light):
  // a warm point light o.I (1.4) with range o.R (2), keyed o.at [[t, k]] (0..1)
  ttFill(o) {
    const g = grp(), lt = new THREE.PointLight(o.color || '#FFE8CC', o.I ?? 1.4, o.R ?? 2.0, 1.2); g.add(lt);
    g.userData.update = t => { lt.intensity = (o.I ?? 1.4) * (o.at ? keyAt(o.at, t, 1) : 1); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- an empty prop that keeps the actors named in o.who (ids) out of the shadow
  // map every frame (the VSM soft shadows also draw the meshes that receive shadow: castShadow and receiveShadow both off)
  ttNoShadow(o) { const g = grp(), names = [].concat(o.who || []);
    g.userData.update = () => { let rt = g; while (rt.parent) rt = rt.parent; if (rt === g) return;
      for (const n of names) { const a = rt.getObjectByName(n); if (a) a.traverse(c => { if (c.isMesh) { c.castShadow = false; c.receiveShadow = false; } }); } };
    return g; },

  // ---------------------------------------------------------------- impact lines round a landing (pivot on the floor at the impact, facing +Z):
  // short white strokes radiating out, popping at o.at for 0.3 s (o.r 0.5); o.ring: a full circle of o.n (12) strokes with a dark edge (an impact
// all round a body that lands flat), o.dur (0.3 s)
  ttImpact(o) {
    const g = grp(), R = o.r ?? 0.5, ls = [], n = o.ring ? (o.n ?? 12) : 7, dur = o.dur ?? 0.3;
    for (let i = 0; i < n; i++) { const a = o.ring ? TAU * (i + 0.5 * (i % 2)) / n : PI * (0.08 + 0.84 * i / 6), l = box(0.035, R * 0.42, 0.01, '#FFFFFF', { noGrain: true, emissive: '#FFFFFF' }); l.castShadow = false; const p = grp(l); if (o.ring) { const e = box(0.06, R * 0.44, 0.006, INK, { noGrain: true }); e.position.z = -0.006; l.add(e); } p.rotation.z = a - PI / 2; g.add(p); ls.push([p, l]); }
    g.userData.update = t => { const d = t - (o.at ?? 0), v = d >= 0 && d < dur ? d / dur : -1; ls.forEach(([p, l]) => { l.visible = v >= 0; l.position.y = R * (0.6 + 0.6 * Math.max(0, v)); l.scale.y = Math.max(0.05, 1 - v); }); };
    g.userData.update(0); return g;
  },
  // ---------------------------------------------------------------- a butter splat left on the floor (pivot on the floor at its middle): a flat
  // bright yellow blob o.r (0.24), drawn with a polygon offset; o.at [[t, v]]: it spreads (0..1) with an overshoot
  ttSplat(o) {
    const R = o.r ?? 0.24, s = new THREE.Shape(); for (let i = 0; i <= 22; i++) { const a = i / 22 * TAU, r = R * (0.8 + 0.18 * hsh(i * 2.3) + 0.08 * Math.sin(a * 6)); if (i === 0) s.moveTo(Math.cos(a) * r, Math.sin(a) * r); else s.lineTo(Math.cos(a) * r, Math.sin(a) * r); }
    const geo = new THREE.ShapeGeometry(s); geo.rotateX(-PI / 2);
    const m = new THREE.Mesh(geo, L(BUTTER, { emissive: '#6A4A00', emissiveIntensity: 0.4, polygonOffset: true, polygonOffsetFactor: -4, polygonOffsetUnits: -16 })); m.position.y = o.y ?? 0.01; m.receiveShadow = true;
    const g = grp(m); g.userData.update = t => { const v = o.at ? keyAt(o.at, t, 0) : 1; m.visible = v > 0.01; m.scale.setScalar(Math.max(0.01, outBack(v, 1.6))); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the kitchen wall clock (pivot at its middle, facing +Z): a round white face
  // o.r (0.3) in a thick red rim, twelve ticks (no digits), hour and minute hands, a red second hand that jumps a twelfth of a turn at each of
  // o.ticks [t...] with a little overshoot while the whole clock pulses (a cartoon tick); o.h0: where the second hand starts (turns); o.pulse:
// how much it swells on a tick (0.08); o.jump (m): how high it hops on a tick (0)
  ttWallClock(o) {
    const R = o.r ?? 0.3, g = grp(), body = grp(); g.add(body);
    body.add(at(cyl(R * 1.12, R * 1.12, 0.07, o.rim || '#D8453A', 32, { outline: 0.006 }), 0, 0, -0.03, PI / 2), at(cyl(R, R, 0.02, '#FBFAF4', 32), 0, 0, 0.012, PI / 2));
    for (let i = 0; i < 12; i++) { const a = i / 12 * TAU; body.add(at(box(i % 3 ? 0.018 : 0.034, R * (i % 3 ? 0.12 : 0.2), 0.01, INK), Math.sin(a) * R * 0.8, Math.cos(a) * R * 0.8, 0.026, 0, 0, -a)); }
    const hh = grp(at(box(0.03, R * 0.5, 0.01, INK, { pivot: 'bottom' }), 0, 0, 0)), mh = grp(at(box(0.022, R * 0.75, 0.01, INK, { pivot: 'bottom' }), 0, 0, 0)), sh = grp(at(box(0.012, R * 0.88, 0.01, '#E2352B', { pivot: 'bottom' }), 0, -R * 0.15, 0));
    hh.position.z = 0.03; mh.position.z = 0.036; sh.position.z = 0.042; hh.rotation.z = -2.1; mh.rotation.z = -0.4; body.add(hh, mh, sh, at(cyl(0.025, 0.025, 0.02, '#E2352B', 10), 0, 0, 0.048, PI / 2));
    g.userData.update = t => {
      let n = 0, last = -9; for (const c of o.ticks || []) if (t >= c) { n++; last = c; }
      const d = t - last, ov = n && d < 0.12 ? Math.sin(d / 0.12 * PI) * 0.12 : 0; sh.rotation.z = -TAU * ((o.h0 ?? 0) + n / 12 + ov / 12);
      const k = n && d < 0.1 ? 1 - d / 0.1 : 0; body.scale.setScalar(1 + (o.pulse ?? 0.08) * k); body.position.y = (o.jump ?? 0) * k;
    };
    g.userData.update(0); return g;
  },
  // ---------------------------------------------------------------- mirror reflections on a waxed floor for ONE camera (place the prop at the
  // world origin): each item [x, z, w, y0, y1, color, moves?] is the front face (toward +Z) of an upright slab from height y0 to y1; its mirror
  // image under the floor, seen from o.cam [x, y, z], is painted flat on the floor (where the camera ray to the mirrored point meets it),
  // fading from the contact line (o.alpha 0.55) to the far end; moves: [[t, dx], ...] slides it along X (a chair). Depth-tested, a polygon
  // offset, drawn before the sheen (ttShine): what stands on the floor still covers it
  ttMirror(o) {
    const C = o.cam || [0, 1.5, 5], g = grp(), gcv = canvas(4, 64), gc = gcv.getContext('2d'), gr = gc.createLinearGradient(0, 0, 0, 64);
    gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.55, 'rgba(255,255,255,0.45)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); gc.fillStyle = gr; gc.fillRect(0, 0, 4, 64);
    const gt = tex(gcv), its = [];
    const q = (x, y, z) => { const k = C[1] / (C[1] + y); return [C[0] + (x - C[0]) * k, 0, C[2] + (z - C[2]) * k]; };
    for (const [x, z, w, y0, y1, col, mv] of o.items || []) {
      const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(new Float32Array(12), 3)); geo.setAttribute('uv', new THREE.Float32BufferAttribute([0, 1, 1, 1, 1, 0, 0, 0], 2)); geo.setIndex([0, 2, 1, 0, 3, 2]);
      const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col, map: gt, transparent: true, opacity: o.alpha ?? 0.55, depthWrite: false, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: -3, polygonOffsetUnits: -10 }));
      m.position.y = o.y ?? 0.008; m.renderOrder = 0; g.add(m); its.push({ m, x, z, w, y0, y1, mv });
    }
    g.userData.update = t => { for (const it of its) { const dx = it.mv ? keyAt(it.mv, t, 0) : 0, xa = it.x + dx - it.w / 2, xb = it.x + dx + it.w / 2;
      const P = [q(xa, it.y0, it.z), q(xb, it.y0, it.z), q(xb, it.y1, it.z), q(xa, it.y1, it.z)], a = it.m.geometry.attributes.position;
      P.forEach((p, i) => a.setXYZ(i, p[0], 0, p[2])); a.needsUpdate = true; it.m.geometry.computeBoundingSphere(); } };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a flat coloured wall panel (pivot at the floor in its middle, facing +Z):
  // o.w x o.h, o.color, a skirting o.trim; another flat's wallpaper in front of a set's back wall
  ttPanel(o) {
    const W = o.w ?? 3, Hh = o.h ?? 3, g = grp(at(box(W, Hh, 0.03, o.color || '#CFE3F2', { pivot: 'bottom' }), 0, 0, 0));
    if (o.trim) g.add(at(box(W, 0.12, 0.05, o.trim, { pivot: 'bottom' }), 0, 0, 0.02));
    if (o.band) g.add(at(box(W, o.bandH ?? 1.0, 0.035, o.band, { pivot: 'bottom' }), 0, 0, 0.01));
    return g;
  },

  // ---------------------------------------------------------------- a floor slab (pivot at its top middle, at o.y 0): o.w x o.d, a tile pattern
  // of o.tile metres in two colours o.colors (opaque, receives shadows)
  ttFloor(o) {
    const W = o.w ?? 12, Dd = o.d ?? 12, ts = o.tile ?? 0.5, cols = o.colors || ['#D9D2C4', '#C9C1B2'], N = 64, cv = canvas(N, N), c = cv.getContext('2d');
    c.fillStyle = cols[0]; c.fillRect(0, 0, N, N); c.fillStyle = cols[1]; c.fillRect(0, 0, N / 2, N / 2); c.fillRect(N / 2, N / 2, N / 2, N / 2);
    if (o.grout) { c.fillStyle = o.grout; c.fillRect(0, 0, N, 2); c.fillRect(0, 0, 2, N); c.fillRect(0, N / 2, N, 2); c.fillRect(N / 2, 0, 2, N); }
    const t = tex(cv); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(W / (2 * ts), Dd / (2 * ts));
    const m = new THREE.Mesh(new THREE.BoxGeometry(W, 0.1, Dd), L('#FFFFFF', { map: t })); m.position.y = (o.y ?? 0) - 0.05; m.receiveShadow = true; return grp(m);
  },
};
