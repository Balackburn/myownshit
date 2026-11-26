// « La notice » (story 107, cycle 57): this man only wants to check the dose of his medicine. He unfolds the leaflet and, like everybody, cannot fold it
// back: it covers the kitchen, the block, the street, the town and the country. Whoever reads it catches its side effects (the street itches, the town
// falls asleep at noon, the country empties the bakeries, the health minister walks like a crab). The last line, on a cliff at the coast, says to ask the
// pharmacist: his pharmacist folds the whole country in two seconds. The dose was drawn on the box all along: one pill and a sun. He unfolds it again.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
// Paper everywhere: off-white, covered in grey bars of « text » (no letter, no digit), fold creases and one curled corner, so that it never reads as snow.
// No cross, no digit, no lettering on the pharmacy or the box: the box's only marking is a big white pill and a big yellow sun (the dose, one a day).
import * as THREE from 'three';
import { box, cyl, sphere, mat, addOutline } from './style.js';
import { grp, at } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = (x, c = 2.2) => { const u = clamp01(x); return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const lerp = (a, b, u) => a + (b - a) * u;
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
// [[t, v], ...] -> v at t, smoothstep between keys (a key [t, v, 'lin'] makes its segment linear)
const keyAt = (K, t, d = 0) => {
  if (K == null) return d;
  if (typeof K === 'number') return K;
  if (!K.length) return d;
  if (t <= K[0][0]) return K[0][1];
  for (let i = 1; i < K.length; i++) if (t < K[i][0]) { const u = (t - K[i - 1][0]) / Math.max(1e-6, K[i][0] - K[i - 1][0]); return lerp(K[i - 1][1], K[i][1], K[i][2] === 'lin' ? u : smooth(u)); }
  return K[K.length - 1][1];
};
// inside one of the intervals [[t0, t1], ...]: the time since its start, else -1
const inside = (I, t) => { for (const [a, b] of I || []) if (t >= a && t < b) return t - a; return -1; };
const tex = cv => { const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t; };
const canvas = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
const L = (c, o = {}) => new THREE.MeshLambertMaterial({ color: c, ...o });
const B = (c, o = {}) => new THREE.MeshBasicMaterial({ color: c, ...o });
const INK = '#1B1E2A';
const ink = (m, t = 0.03) => { addOutline(m, t); return m; };
const noShadow = g => { g.traverse(c => { if (c.isMesh) { c.castShadow = false; c.receiveShadow = false; } }); return g; };
const OFF = { polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -8 };
const PAPER = '#F8F6EF';

// ---------------------------------------------------------------- the paper: grey bars of « text » in columns and paragraphs (no letter), fold creases
function drawPaper(c, W, H, o = {}) {
  c.fillStyle = o.paper || PAPER; c.fillRect(0, 0, W, H);
  const cols = o.cols ?? 2, m = W * (o.margin ?? 0.07), gap = W * 0.05, cw = (W - 2 * m - gap * (cols - 1)) / cols;
  const lh = H * (o.lh ?? 0.026), bar = Math.max(1.5, lh * (o.bar ?? 0.4)), top = H * (o.top ?? 0.07), bottom = H * (1 - (o.bottom ?? 0.07));
  let s = (o.seed ?? 1) * 17;
  for (let k = 0; k < cols; k++) {
    const x0 = m + k * (cw + gap); let y = top, n = 0, para = 3 + Math.floor(hsh(s++) * 5);
    while (y < bottom - bar) {
      if (n === 0 && hsh(s++) < 0.35) { c.fillStyle = o.head || '#6F737C'; c.fillRect(x0, y, cw * (0.3 + 0.3 * hsh(s++)), bar * 1.5); y += lh * 1.25; }
      const last = n === para - 1, len = last ? cw * (0.25 + 0.5 * hsh(s++)) : cw * (0.86 + 0.14 * hsh(s++));
      c.fillStyle = o.ink || '#A2A5AD';
      let x = x0; while (x < x0 + len) { const wl = Math.min(x0 + len - x, cw * (0.05 + 0.13 * hsh(s++))); c.fillRect(x, y, wl, bar); x += wl + bar * 1.3; }
      y += lh; n++;
      if (last) { n = 0; para = 3 + Math.floor(hsh(s++) * 5); y += lh * 0.7; }
    }
  }
  const [nx, ny] = o.creases || [0, 0];
  for (let i = 1; i < nx; i++) { const x = W * i / nx; c.fillStyle = 'rgba(105,108,122,0.24)'; c.fillRect(x - 1.5, 0, 3, H); c.fillStyle = 'rgba(255,255,255,0.6)'; c.fillRect(x + 1.5, 0, 2, H); }
  for (let j = 1; j < ny; j++) { const y = H * j / ny; c.fillStyle = 'rgba(105,108,122,0.24)'; c.fillRect(0, y - 1.5, W, 3); c.fillStyle = 'rgba(255,255,255,0.6)'; c.fillRect(0, y + 1.5, W, 2); }
  if (o.border) { c.strokeStyle = 'rgba(120,122,132,0.5)'; c.lineWidth = Math.max(2, W * 0.004); c.strokeRect(1, 1, W - 2, H - 2); }
}
// big bold lines, one common letter size, fitted to wf of the width, stacked in hf of the height round cy (fractions); a pale band under them
function drawBig(c, W, H, lines, o = {}) {
  const n = lines.length, hf = o.hf ?? 0.6, cy = H * (o.cy ?? 0.5), lhp = H * hf / n, wf = W * (o.wf ?? 0.9);
  if (o.band !== false) { c.fillStyle = o.paper || PAPER; c.fillRect(W * 0.02, cy - H * hf / 2 - lhp * 0.15, W * 0.96, H * hf + lhp * 0.3); }
  let fs = lhp * 0.82; c.font = `900 ${fs}px Arial`;
  for (const l of lines) { const w = c.measureText(l).width; if (w > wf) fs = Math.min(fs, lhp * 0.82 * wf / w); }
  c.font = `900 ${fs}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillStyle = o.color || '#15171D';
  lines.forEach((l, i) => c.fillText(l, W / 2, cy + (i - (n - 1) / 2) * lhp));
}
// a pair of paper materials (front, back: no text on the back, so nothing reads mirrored) on a canvas of res x res*h/w
function paperMats(w, h, o = {}) {
  const res = o.res ?? 512, cw = res, ch = Math.max(16, Math.round(res * h / w));
  const cvF = canvas(cw, ch), cF = cvF.getContext('2d'); drawPaper(cF, cw, ch, o);
  if (o.text) drawBig(cF, cw, ch, [].concat(o.text), { cy: o.textY ?? 0.8, hf: o.textH ?? 0.22, wf: o.textW ?? 0.9 });
  const cvB = canvas(cw, ch), cB = cvB.getContext('2d'); drawPaper(cB, cw, ch, { ...o, seed: (o.seed ?? 1) + 7 });
  const tF = tex(cvF), tB = tex(cvB);
  if (o.repeat) for (const t of [tF, tB]) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(o.repeat[0], o.repeat[1]); }
  const e = o.glow ?? 0.2, mo = o.offset ? OFF : {};
  return [L('#FFFFFF', { map: tF, emissive: '#FFFFFF', emissiveMap: tF, emissiveIntensity: e, side: THREE.FrontSide, ...mo }),
          L('#FFFFFF', { map: tB, emissive: '#FFFFFF', emissiveMap: tB, emissiveIntensity: e, side: THREE.BackSide, ...mo })];
}
function paperPair(geo, mats, shadow = true) {
  const a = new THREE.Mesh(geo, mats[0]), b = new THREE.Mesh(geo, mats[1]);
  for (const m of [a, b]) { m.castShadow = shadow; m.receiveShadow = true; m.frustumCulled = false; }
  return grp(a, b);
}
// a faceted rock (jittered icosphere)
function facet(rx, ry, rz, color, seed = 3, jit = 0.12) {
  const g = new THREE.IcosahedronGeometry(1, 1), p = g.attributes.position, off = new Map();
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i), y = p.getY(i), z = p.getZ(i), k = `${Math.round(x * 999)},${Math.round(y * 999)},${Math.round(z * 999)}`;
    if (!off.has(k)) off.set(k, 1 + (hsh(seed * 31 + off.size * 7.3) - 0.5) * 2 * jit);
    const f = off.get(k); p.setXYZ(i, x * rx * f, y * ry * f, z * rz * f);
  }
  g.computeVertexNormals(); const m = new THREE.Mesh(g, mat(color, { flatShading: true })); m.castShadow = m.receiveShadow = true; return m;
}

export const NOTICE_PROPS = {
  // ---------------------------------------------------------------- the leaflet (pivot at its middle, in its own XY plane, front +Z; lay it on a table with
  // rot [-PI/2, 0, 0]: then local +Y points to world -Z and +Z up). o.w (1.4) x o.h (1.0) open; o.unfold [[t, u]]: 0 = a tiny folded square (o.fsize of
  // the size, a few sheets thick, its panels zigzag like an accordion), 1 = open (above 1: bigger, the overshoot of a spring); o.fold [[t, f]]: the half on
  // local +Y folds about the middle crease toward +Z and over (1 = folded in half); o.bulge [[t, b]]: the folded sheet puffs up like a pillow; o.flap
  // [[t, a]]: the far edge ripples; o.curl (0.2): one corner curled; o.creases ([4, 3]); o.text: big bold lines printed at o.textY; o.offset: a polygon
  // offset (lying on a floor); (review 2) o.ink / o.bar: the colour and the thickness of its grey bars; (review 1) o.ripple [[t, c]]: a hump o.rippleA (0.5 m) high runs across it (c: where along local Y, 0..1; below -0.5: none)
  noLeaflet(o) {
    const W = o.w ?? 1.4, H = o.h ?? 1.0, NX = o.nx ?? 28, NY = o.ny ?? 20, g = grp(), body = grp(); g.add(body);
    const geo = new THREE.PlaneGeometry(W, H, NX, NY), pos = geo.attributes.position, base = pos.array.slice();
    body.add(paperPair(geo, paperMats(W, H, { creases: o.creases ?? [4, 3], seed: o.seed ?? 1, cols: o.cols ?? 2, lh: o.lh, ink: o.ink, bar: o.bar, text: o.text, textY: o.textY, textH: o.textH, offset: o.offset, glow: o.glow, res: o.res, border: true }), o.shadow !== false));
    const stack = box(1, 1, 1, '#ECE9E0', { outline: 0.004 }); stack.castShadow = false; body.add(stack);
    const PAN = o.panels ?? 6;
    g.userData.update = t => {
      const u = keyAt(o.unfold, t, 1), f = clamp01(keyAt(o.fold, t, 0)), b = keyAt(o.bulge, t, 0), fl = keyAt(o.flap, t, 0), cu = o.curl ?? 0.2;
      const fs = o.fsize ?? 0.09, s = fs + (1 - fs) * Math.max(0, u), acc = 1 - clamp01(u), th = f * PI * 0.985;
      for (let i = 0; i < pos.count; i++) {
        const x0 = base[i * 3], y0 = base[i * 3 + 1], nx = x0 / W + 0.5, ny = y0 / H + 0.5;
        let x = x0 * s, y = y0 * s, z = 0;
        const ph = (nx * PAN) % 2, tri = ph < 1 ? ph : 2 - ph;
        z += acc * (tri - 0.5) * W * s / PAN * 0.9;
        const cx = clamp01((nx - 0.72) / 0.28), cy = clamp01((ny - 0.62) / 0.38);
        z += cu * H * s * 0.35 * Math.pow(cx * cy, 1.6);
        z += fl * W * s * 0.035 * Math.sin(t * (o.flapF ?? 16) + nx * 7 + ny * 3) * ny * ny;
        if (o.ripple) { const rc = keyAt(o.ripple, t, -1); if (rc > -0.5) z += (o.rippleA ?? 0.5) * Math.exp(-Math.pow((ny - rc) / (o.rippleW ?? 0.07), 2)) * (0.7 + 0.3 * Math.sin(nx * 9 + t * 6)); }
        if (y > 0 && th > 0) { const yy = y, zz = z; y = yy * Math.cos(th) - zz * Math.sin(th); z = yy * Math.sin(th) + zz * Math.cos(th) + 0.004 * f; }
        if (b && y0 > 0) z += b * H * s * 0.2 * Math.sin(PI * nx) * Math.sin(PI * clamp01(y0 / (H / 2)));
        pos.setXYZ(i, x, y, z);
      }
      pos.needsUpdate = true; geo.computeVertexNormals();
      stack.visible = u < 0.3;
      if (stack.visible) { stack.scale.set(W * s * 0.98, H * s * 0.98, 0.016 * (1 - u / 0.3) + 0.001); stack.position.set(0, 0, -0.009); }
    };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the leaflet slapped flat over a face like a mask (attach to the head joint, offset [0, 0, 0]:
  // the head frame, chin at 0, the face front at z ~0.1): flat over the face (o.fw, its half width), wrapped back round the corners of the head, the top
  // edge curling forward, wider and taller than the face. o.at: the slap (it flies in from in front in o.fly s, bigger, then wobbles flat); o.breath
  // [[t, b]]: the paper over the mouth puffs out (+) and sucks in (-) with his breath
  noFaceSheet(o) {
    const W = o.w ?? 0.54, H = o.h ?? 0.5, NX = 24, NY = 20, g = grp(), body = grp(); g.add(body);
    const Y0 = o.y ?? 0.27, Z0 = o.z ?? 0.1, FW = o.fw ?? 0.16, R = o.r ?? 0.06, MY = (o.mouth ?? 0.12) - Y0, FLY = o.fly ?? 0.07;
    const geo = new THREE.PlaneGeometry(W, H, NX, NY), pos = geo.attributes.position, base = pos.array.slice();
    body.add(paperPair(geo, paperMats(W, H, { creases: [2, 2], seed: o.seed ?? 5, cols: 1, lh: 0.06, bar: 0.36, glow: 0.25, res: 256, border: true }), false));
    g.userData.update = t => {
      const d = t - (o.at ?? 0); body.visible = d >= 0; if (d < 0) return;
      const fly = clamp01(d / FLY), e = d - FLY, wob = e > 0 ? Math.exp(-e * 9) * Math.sin(e * 38) : 0, br = keyAt(o.breath, t, 0);
      const sF = 1 + 0.7 * (1 - fly) * (1 - fly) + 0.1 * wob, zF = 0.5 * (1 - fly) * (1 - fly);
      for (let i = 0; i < pos.count; i++) {
        const x0 = base[i * 3], y0 = base[i * 3 + 1], yt = y0 / H + 0.5;
        let x = x0 * sF, y = y0 * sF * (1 - 0.07 * wob), z = 0;
        const ax = Math.abs(x), sg = Math.sign(x) || 1;
        if (ax > FW) {
          const a = (ax - FW) / R * fly;
          if (a <= PI / 2) { x = sg * (FW + R * Math.sin(a)); z = -R * (1 - Math.cos(a)); }
          else { const ex = (a - PI / 2) * R; x = sg * (FW + R); z = -R - ex; }
        }
        if (yt > 0.84) z += (yt - 0.84) * (yt - 0.84) * 3.0;
        if (yt < 0.1) z += (0.1 - yt) * 0.35 * Math.sin(t * 13 + x0 * 9);
        z += br * 0.04 * Math.exp(-((x0 / 0.09) ** 2 + ((y0 - MY) / 0.07) ** 2));
        pos.setXYZ(i, x, Y0 + y, Z0 + z + zF);
      }
      pos.needsUpdate = true; geo.computeVertexNormals();
      body.rotation.x = -0.5 * (1 - fly);
    };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the pill box (pivot at its middle, front +Z): a white brick-size box whose only marking
  // is drawn on its front: one big pill (a white and blue capsule, inked) and one big yellow sun: the dose, one a day. o.w (0.36) x o.h (0.24) x o.d (0.11);
  // o.open [[t, v]]: the top flap opens back (0..1), its dark opening shows
  noPillBox(o) {
    const W = o.w ?? 0.36, H = o.h ?? 0.24, D = o.d ?? 0.11, g = grp();
    g.add(box(W, H, D, '#FAFAF6', { outline: 0.01 }));
    const cv = canvas(512, Math.round(512 * H / W)), c = cv.getContext('2d'), Wc = cv.width, Hc = cv.height;
    c.fillStyle = '#FAFAF6'; c.fillRect(0, 0, Wc, Hc);
    c.strokeStyle = '#C9D6E2'; c.lineWidth = Wc * 0.012; c.strokeRect(Wc * 0.03, Hc * 0.045, Wc * 0.94, Hc * 0.91);
    // the pill: a big two-tone capsule lying at a slant, inked (review 1: a scored disc read as a no-entry sign at phone size)
    const px = Wc * 0.28, py = Hc * 0.5, cl = Hc * 0.9, cw = Hc * 0.36, ang = -0.62;
    const caps = (dx, dy) => { c.beginPath(); c.moveTo(-cl / 2 + cw / 2 + dx, -cw / 2 + dy); c.lineTo(cl / 2 - cw / 2 + dx, -cw / 2 + dy); c.arc(cl / 2 - cw / 2 + dx, dy, cw / 2, -PI / 2, PI / 2);
      c.lineTo(-cl / 2 + cw / 2 + dx, cw / 2 + dy); c.arc(-cl / 2 + cw / 2 + dx, dy, cw / 2, PI / 2, 3 * PI / 2); c.closePath(); };
    c.save(); c.translate(px, py); c.rotate(ang);
    c.fillStyle = '#DDE2EA'; caps(cw * 0.1, cw * 0.14); c.fill();
    c.save(); caps(0, 0); c.clip(); c.fillStyle = '#FFFFFF'; c.fillRect(-cl / 2, -cw, cl / 2, cw * 2); c.fillStyle = '#5E9BD6'; c.fillRect(0, -cw, cl / 2 + 2, cw * 2);
    c.fillStyle = 'rgba(255,255,255,0.55)'; c.fillRect(-cl * 0.36, -cw * 0.3, cl * 0.6, cw * 0.14); c.restore();
    c.strokeStyle = '#24314F'; c.lineWidth = Wc * 0.02; caps(0, 0); c.stroke();
    c.lineWidth = Wc * 0.012; c.beginPath(); c.moveTo(0, -cw / 2); c.lineTo(0, cw / 2); c.stroke(); c.restore();
    // the sun: a yellow disc with an orange ink line and ten rays
    const sx = Wc * 0.73, sy = Hc * 0.5, sr = Hc * 0.2;
    c.fillStyle = '#FFB52E'; c.strokeStyle = '#D9761E'; c.lineWidth = Wc * 0.01;
    for (let i = 0; i < 10; i++) { const a = i * TAU / 10; c.beginPath(); c.moveTo(sx + Math.cos(a - 0.17) * sr * 1.18, sy + Math.sin(a - 0.17) * sr * 1.18);
      c.lineTo(sx + Math.cos(a) * sr * 2.0, sy + Math.sin(a) * sr * 2.0); c.lineTo(sx + Math.cos(a + 0.17) * sr * 1.18, sy + Math.sin(a + 0.17) * sr * 1.18); c.closePath(); c.fill(); c.stroke(); }
    c.fillStyle = '#FFD83A'; c.beginPath(); c.arc(sx, sy, sr, 0, TAU); c.fill(); c.lineWidth = Wc * 0.016; c.stroke();
    const t1 = tex(cv), face = new THREE.Mesh(new THREE.PlaneGeometry(W * 0.985, H * 0.98), L('#FFFFFF', { map: t1, emissive: '#FFFFFF', emissiveMap: t1, emissiveIntensity: o.glow ?? 0.22 }));
    face.position.z = D / 2 + 0.002; face.castShadow = false; face.receiveShadow = true; g.add(face);
    const hole = box(W * 0.9, 0.004, D * 0.82, '#2E3036'); hole.position.y = H / 2 - 0.002; hole.visible = false; g.add(hole);
    const hinge = grp(); hinge.position.set(0, H / 2 + 0.006, -D / 2); g.add(hinge);
    const flap = box(W, 0.012, D, '#F4F4EE', { outline: 0.008 }); flap.position.z = D / 2; hinge.add(flap);
    g.userData.update = t => { const v = clamp01(keyAt(o.open, t, 0)); hinge.rotation.x = -v * 2.1; hole.visible = v > 0.04; };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the kitchen papered over (kitchenDay: back wall at z o.back -3.6): the back wall covered
  // from the floor to o.h, the paper draped over the fridge, the counter and the cupboards (bumps [x0, x1, y0, y1, depth]) and curling forward at its top
  // edge; the floor covered; a heap of paper petals standing round o.mound [x, z] up to o.mh (his neck), open at the top (o.rt) for his head and the box;
  // o.burst [t]: the petals spring outward and wobble (his head pops out)
  noPaperRoom(o) {
    const g = grp(), back = o.back ?? -3.6, Wd = o.w ?? 12, Hh = o.h ?? 3.4, NX = 72, NY = 26;
    const bumps = o.bumps ?? [[-3.25, -2.15, 0, 2.05, 0.95], [-1.35, 1.75, 0, 0.95, 0.66], [-1.3, -0.4, 1.75, 2.45, 0.38], [0.8, 1.7, 1.75, 2.45, 0.38]];
    const ed = (v, a, b, w) => smooth((v - a) / w) * smooth((b - v) / w);
    const wgeo = new THREE.PlaneGeometry(Wd, Hh, NX, NY), wp = wgeo.attributes.position;
    for (let i = 0; i < wp.count; i++) {
      const x = wp.getX(i), y = wp.getY(i) + Hh / 2; let z = 0;
      for (const [x0, x1, y0, y1, d] of bumps) z = Math.max(z, d * ed(x, x0, x1, 0.22) * (y0 <= 0.01 ? smooth((y1 - y) / 0.22) : ed(y, y0, y1, 0.18)));
      z += 0.04 * Math.sin(x * 2.1 + y * 0.7) + 0.03 * Math.sin(y * 3.3 - x);
      if (y > Hh - 0.6) z += Math.pow((y - (Hh - 0.6)) / 0.6, 2) * 0.55;
      wp.setXYZ(i, x, y, z);
    }
    wgeo.computeVertexNormals();
    const wall = paperPair(wgeo, paperMats(1.2, 0.9, { creases: [2, 2], seed: 3, repeat: [Wd / 1.2, Hh / 0.9], res: 512, glow: 0.16, border: true }), false);
    wall.position.set(o.x ?? 0, 0, back + 0.03); g.add(wall);
    const fgeo = new THREE.PlaneGeometry(Wd, o.fd ?? 8, 36, 20), fp = fgeo.attributes.position;
    for (let i = 0; i < fp.count; i++) fp.setZ(i, 0.025 * Math.sin(fp.getX(i) * 1.7 + fp.getY(i) * 2.3));
    fgeo.computeVertexNormals();
    const floor = paperPair(fgeo, paperMats(1.2, 0.9, { creases: [2, 2], seed: 4, repeat: [Wd / 1.2, (o.fd ?? 8) / 0.9], res: 512, glow: 0.12, offset: true }), false);
    floor.rotation.x = -PI / 2; floor.position.set(o.x ?? 0, 0.03, back + (o.fd ?? 8) / 2); g.add(floor);
    const [mx, mz] = o.mound ?? [0, -0.5], N = o.n ?? 9, MR = o.mr ?? 0.78, MH = o.mh ?? 1.72, RT = o.rt ?? 0.4, PW = TAU * MR / N * 1.45, petals = [];
    const pm = paperMats(0.9, 1.2, { creases: [2, 3], seed: 6, cols: 1, res: 256, glow: 0.18, border: true });
    for (let k = 0; k < N; k++) {
      const a = k / N * TAU + 0.2, pg = new THREE.PlaneGeometry(PW, MH, 6, 10), pp = pg.attributes.position;
      for (let i = 0; i < pp.count; i++) { const x = pp.getX(i), y = pp.getY(i) + MH / 2; pp.setXYZ(i, x, y, 0.06 * Math.sin(y * 4 + k) + 0.08 * Math.sin(PI * clamp01(y / MH)) - 0.25 * (x / PW) * (x / PW)); }
      pg.computeVertexNormals();
      const piv = grp(paperPair(pg, pm, false)); piv.position.set(mx + Math.sin(a) * MR, 0, mz + Math.cos(a) * MR); piv.rotation.order = 'YXZ'; piv.rotation.y = a;
      g.add(piv); petals.push({ piv, lean: -Math.atan((MR - RT) / MH), k });
    }
    g.userData.update = t => { for (const p of petals) { let e = 0; for (const tb of o.burst || []) { const u = t - tb - 0.02 * (p.k % 3); if (u >= 0) e += 0.32 * Math.exp(-u * 6) * Math.cos(u * 24); } p.piv.rotation.x = p.lean + e; } };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a building front (pivot at the foot of its middle, front +Z): o.floors (5) of o.fh (3) m,
  // o.cols (4) windows a floor, a plain shop front on the ground floor (no lettering), cornices, a grey-blue mansard roof with chimney stacks; out of every
  // window above the ground floor the leaflet bulges (a paper dome filling the window and a tongue of lined paper hanging over the sill), popping out one
  // window after the other from o.pop every o.stagger s (o.order 'down' from the top floor, 'up'), with an overshoot, then breathing
  noFacade(o) {
    const W = o.w ?? 10, F = o.floors ?? 5, FH = o.fh ?? 3.0, C = o.cols ?? 4, Ht = F * FH, g = grp(), col = o.color || '#F2DCCB';
    g.add(at(box(W, Ht, 0.5, col, { pivot: 'bottom', outline: 0.012 }), 0, 0, -0.25));
    g.add(at(box(W - 0.5, 2.7, 0.1, '#2E5A3E', { pivot: 'bottom', outline: 0.008 }), 0, 0.0, 0.04), at(box(W * 0.5, 1.8, 0.05, '#5C7E8E', { pivot: 'bottom', emissive: '#22323A' }), -W * 0.16, 0.55, 0.1),
      at(box(1.0, 2.3, 0.05, '#3A2E28', { pivot: 'bottom' }), W * 0.28, 0.05, 0.1));
    for (let f = 1; f <= F; f++) g.add(at(box(W + 0.24, 0.16, 0.24, '#EAE2D3', { outline: 0.006 }), 0, f * FH - 0.04, 0.1));
    g.add(at(box(W, 2.3, 1.9, '#7D8DA0', { pivot: 'bottom', taper: { x: 1, z: 0.3 }, outline: 0.01 }), 0, Ht + 0.04, -0.75));
    for (const [x, h] of [[-W * 0.3, 1.3], [W * 0.33, 1.5]]) { g.add(at(box(0.7, h, 0.55, '#C9785A', { pivot: 'bottom', outline: 0.008 }), x, Ht + 1.6, -1.0)); for (let k = 0; k < 3; k++) g.add(at(cyl(0.07, 0.08, 0.3, '#B5582E', 6, { pivot: 'bottom' }), x - 0.2 + 0.2 * k, Ht + 1.6 + h, -1.0)); }
    const pm = paperMats(0.9, 1.3, { creases: [2, 2], seed: 9, cols: 1, res: 256, glow: 0.2, border: true, lh: 0.07, bar: 0.45 });
    // the paper pushing out of the window: a crumpled wad (a jittered half icosphere, flat shaded), lined like the rest
    const dg = new THREE.IcosahedronGeometry(1, 1), dp = dg.attributes.position;
    for (let i = 0; i < dp.count; i++) { const x = dp.getX(i), y = dp.getY(i), z = dp.getZ(i), f = 1 + 0.14 * Math.sin(x * 9.1 + y * 7.3 + z * 5.7); dp.setXYZ(i, x * f, y * f, Math.max(-0.1, z) * f); }
    dg.computeVertexNormals();
    const tg = new THREE.PlaneGeometry(0.95, 1.5, 6, 12), tp = tg.attributes.position;
    for (let i = 0; i < tp.count; i++) { const x = tp.getX(i), v = 0.5 - tp.getY(i) / 1.5; tp.setXYZ(i, x * (1 + 0.15 * v), -v * 1.25, 0.12 + 0.42 * Math.sin(v * PI * 0.62) + 0.05 * Math.sin(x * 9 + v * 6)); }
    tg.computeVertexNormals();
    const papers = []; let idx = 0;
    for (let f = F - 1; f >= 1; f--) for (let k = 0; k < C; k++) {
      const x = (k - (C - 1) / 2) * W / C, y = f * FH + 0.55, ord = (o.order ?? 'down') === 'down' ? idx : (F - 1) * C - 1 - idx; idx++;
      g.add(at(box(1.05, 1.75, 0.06, '#2E3440', { pivot: 'bottom' }), x, y, 0.01), at(box(1.24, 0.1, 0.16, '#F7F2E8', { outline: 0.005 }), x, y, 0.07), at(box(1.24, 0.1, 0.1, '#F7F2E8'), x, y + 1.8, 0.05));
      g.add(at(box(1.36, 0.05, 0.05, '#20242C'), x, y + 0.52, 0.32)); for (let b = 0; b < 6; b++) g.add(at(box(0.025, 0.5, 0.025, '#20242C', { pivot: 'bottom' }), x - 0.62 + b * 0.248, y + 0.02, 0.32));
      const pw = grp(), dome = new THREE.Mesh(dg, pm[0]); dome.scale.set(0.5, 0.82, 0.3); dome.position.set(0, 0.87, 0.02);
      const tongue = paperPair(tg, pm, false); tongue.position.set(0, 0.06, 0.02);
      pw.add(dome, tongue); pw.position.set(x, y, 0.05); g.add(pw);
      papers.push({ pw, tp: (o.pop ?? 0.1) + (o.stagger ?? 0.05) * ord, i: idx });
    }
    g.userData.update = t => { for (const p of papers) { const d = t - p.tp; p.pw.visible = d >= 0; if (d < 0) continue; const s = outBack(d / 0.13, 2.8) * (1 + 0.04 * Math.sin(t * 8 + p.i * 1.7)); p.pw.scale.set(Math.max(0.01, s), Math.max(0.01, s), Math.max(0.01, s)); } };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the leaflet rolling down a pavement like a carpet (pivot at its start, it unrolls toward +Z):
  // a strip o.w (2.2) wide whose length grows from o.len0 at o.speed m/s from o.t0, up to o.max; at its front the roll (radius o.r, a paper spiral on its
  // ends) turns as it goes; the lines stay where they were printed
  noPaperCarpet(o) {
    const Wd = o.w ?? 2.2, R = o.r ?? 0.3, TILE = o.tile ?? 1.4, g = grp();
    const sgeo = new THREE.PlaneGeometry(Wd, 1, 1, 1).rotateX(-PI / 2).translate(0, 0, 0.5);
    // (review 1) o.cols / o.res: more columns and a finer canvas for a carpet as wide as a road (2 columns over 9 m blurred into slabs)
    const sm = paperMats(Wd, TILE, { creases: [2, 1], seed: 11, repeat: [1, 1], res: o.res ?? 512, cols: o.cols ?? 2, glow: 0.18, offset: true });
    const strip = new THREE.Mesh(sgeo, sm[0]); strip.position.y = 0.012; strip.receiveShadow = true; g.add(strip);
    const rm = paperMats(Wd, TAU * R, { creases: [0, 0], seed: 12, cols: o.cols ?? 2, res: o.rollRes ?? 256, glow: 0.2, lh: o.rollLh });
    const roll = grp(), rc = new THREE.Mesh(new THREE.CylinderGeometry(R, R, Wd, 20, 1, true), rm[0]); rc.rotation.z = PI / 2; roll.add(rc);
    const cv = canvas(128, 128), c = cv.getContext('2d'); c.fillStyle = '#EEEBE2'; c.fillRect(0, 0, 128, 128); c.strokeStyle = '#9A9DA6'; c.lineWidth = 2.5; c.beginPath();
    for (let a = 0; a < TAU * 5; a += 0.1) { const rr = 4 + a * 1.9; c.lineTo(64 + Math.cos(a) * rr, 64 + Math.sin(a) * rr); } c.stroke();
    const capT = tex(cv);
    for (const sx of [-1, 1]) { const cap = new THREE.Mesh(new THREE.CircleGeometry(R, 20), L('#FFFFFF', { map: capT, emissive: '#FFFFFF', emissiveMap: capT, emissiveIntensity: 0.2 })); cap.rotation.y = sx * PI / 2; cap.position.x = sx * Wd / 2; roll.add(cap); }
    ink(rc, 0.01); g.add(roll);
    g.userData.update = t => {
      const len = Math.min(o.max ?? 60, Math.max(0.01, (o.len0 ?? 2) + (o.speed ?? 6) * (t - (o.t0 ?? 0))));
      strip.scale.z = len; sm[0].map.repeat.set(1, len / TILE); sm[0].map.offset.set(0, -len / TILE); sm[0].emissiveMap.repeat.copy(sm[0].map.repeat); sm[0].emissiveMap.offset.copy(sm[0].map.offset);
      roll.position.set(0, R + 0.012, len); roll.rotation.x = len / R;
    };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a word that pops up off the paper like a pop-up book (pivot at its foot, front +Z): a card
  // o.w (1.0) x o.h (0.42) of lined paper with o.lines (or o.text) in big bold black letters fitted to it; o.up [[t, u]]: 0 = lying flat face up, 1 =
  // upright (above 1 it leans back past upright: the overshoot); as it rises its foot lifts to o.lift on two paper struts
  noWordCard(o) {
    const Wc = o.w ?? 1.0, Hc = o.h ?? 0.42, lines = [].concat(o.lines || o.text || ['MOT']), g = grp(), hinge = grp(); g.add(hinge);
    const cvF = canvas(1024, Math.round(1024 * Hc / Wc)), cF = cvF.getContext('2d');
    drawPaper(cF, cvF.width, cvF.height, { creases: [0, 0], seed: 21, cols: 2, lh: 0.06, border: true });
    drawBig(cF, cvF.width, cvF.height, lines, { cy: 0.5, hf: 0.8, wf: 0.9 });
    const tF = tex(cvF), front = new THREE.Mesh(new THREE.PlaneGeometry(Wc, Hc), L('#FFFFFF', { map: tF, emissive: '#FFFFFF', emissiveMap: tF, emissiveIntensity: o.glow ?? 0.3 }));
    front.position.y = Hc / 2; front.castShadow = true; front.receiveShadow = true; hinge.add(front);
    const bk = paperMats(Wc, Hc, { creases: [0, 0], seed: 22, cols: 2, res: 256 })[1], back = new THREE.Mesh(new THREE.PlaneGeometry(Wc, Hc), bk); back.position.y = Hc / 2; hinge.add(back);
    const struts = [-1, 1].map(sx => { const s = box(0.03, 1, 0.16, '#ECE9E0', { outline: 0.004 }); s.position.x = sx * Wc * 0.42; g.add(s); return s; });
    const lift = o.lift ?? 0.3;
    g.userData.update = t => {
      const u = keyAt(o.up, t, 1), uc = clamp01(u), yh = 0.012 + lift * uc;
      hinge.rotation.x = -(1 - u) * PI / 2; hinge.position.set(0, yh, 0);
      for (const s of struts) { s.visible = yh > 0.03; s.scale.y = Math.max(0.01, yh); s.position.set(s.position.x, yh / 2, -0.09); }
    };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the leaflet as the sky (pivot on the ground under the middle of its fixed far edge, its
  // sheet spreads along local +X): a paper ceiling at height o.y (24) from x 0 to the edge at o.len (220), o.d (300) wide along Z; tiny grey lines printed
  // on it (a tile every o.tile m, anchored in the world), soft sags, and its edge curling down and flapping; o.roll [[t, v]]: the edge snaps back toward x 0
  // like a roller blind (1 = all rolled up), a fat paper roll at the edge
  noPaperSky(o) {
    const Y = o.y ?? 24, LEN = o.len ?? 220, D = o.d ?? 300, TILE = o.tile ?? 7, NX = 48, NY = 24, RR = o.rollR ?? 2.2, g = grp();
    const cv = canvas(512, 512), c = cv.getContext('2d'); drawPaper(c, 512, 512, { creases: [2, 2], seed: 31, cols: 2, lh: 0.03, bar: 0.42, paper: '#F3F0E6', ink: '#A6A6A4', head: '#8C8C8A' });
    const tx = tex(cv); tx.wrapS = tx.wrapT = THREE.RepeatWrapping;
    const geo = new THREE.PlaneGeometry(1, 1, NX, NY), pos = geo.attributes.position, uv = geo.attributes.uv;
    const m = new THREE.Mesh(geo, B('#FFFFFF', { map: tx, side: THREE.DoubleSide })); m.frustumCulled = false; m.castShadow = false; m.receiveShadow = false; g.add(m);
    const roll = new THREE.Mesh(new THREE.CylinderGeometry(RR, RR, D, 24, 1, true), B('#FFFFFF', { map: tx, side: THREE.DoubleSide })); roll.rotation.x = PI / 2; roll.frustumCulled = false; g.add(roll);
    g.userData.update = t => {
      const v = clamp01(keyAt(o.roll, t, 0)), xe = Math.max(2, LEN * (1 - v)), fl = o.flap ?? 1;
      for (let j = 0; j <= NY; j++) for (let i = 0; i <= NX; i++) {
        const n = j * (NX + 1) + i, x = xe * i / NX, z = -D / 2 + D * j / NY, k = clamp01((x - (xe - 9)) / 9);
        let y = Y - (o.sag ?? 0.9) * (0.5 + 0.5 * Math.sin(x * 0.05 + z * 0.04) * Math.sin(z * 0.07 - x * 0.02));
        y -= k * k * 4.5 - fl * k * k * 1.6 * Math.sin(t * 5 + z * 0.15);
        pos.setXYZ(n, x, y, z); uv.setXY(n, x / TILE, z / TILE);
      }
      pos.needsUpdate = true; uv.needsUpdate = true;
      roll.visible = v > 0.002; roll.position.set(xe, Y - 4.5 + RR * 0.4, 0); roll.rotation.y = xe / RR;
    };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a rooftop terrace (pivot at the middle of its deck, deck top at y 0): a wooden deck
  // o.w (9) x o.d (8), parapets with iron rails round it, chimney stacks with pots, a zinc roof slope beyond the back parapet, a potted bay tree
  noTerrace(o) {
    const W = o.w ?? 9, D = o.d ?? 8, g = grp();
    g.add(at(box(W, 0.4, D, '#B98E62', { pivot: 'top', outline: 0.01 }), 0, 0, 0));
    for (let x = -W / 2 + 0.3; x < W / 2; x += 0.3) g.add(at(box(0.012, 0.004, D, '#8E6440'), x, 0.002, 0));
    const par = (w, d, x, z) => { g.add(at(box(w, 0.95, d, '#E9E1D2', { pivot: 'bottom', outline: 0.008 }), x, 0, z)); g.add(at(box(w, 0.04, d + 0.04, '#20242C'), x, 1.55, z)); };
    par(W, 0.28, 0, -D / 2); par(0.28, D, -W / 2, 0); par(0.28, D, W / 2, 0);
    for (let x = -W / 2 + 0.15; x <= W / 2; x += 0.3) g.add(at(box(0.025, 0.6, 0.025, '#20242C', { pivot: 'bottom' }), x, 0.95, -D / 2));
    for (let z = -D / 2 + 0.15; z <= D / 2; z += 0.3) for (const sx of [-1, 1]) g.add(at(box(0.025, 0.6, 0.025, '#20242C', { pivot: 'bottom' }), sx * W / 2, 0.95, z));
    g.add(at(box(W + 4, 2.0, 2.4, '#7D8DA0', { pivot: 'bottom', taper: { x: 1, z: 0.25 }, outline: 0.01 }), 0, -1.2, -D / 2 - 1.6));
    for (const [x, z, h] of o.chimneys ?? [[-W / 2 + 0.8, -D / 2 + 0.6, 1.7], [W / 2 - 1.0, -D / 2 + 0.6, 2.1]]) {
      g.add(at(box(1.0, h, 0.6, '#C9785A', { pivot: 'bottom', outline: 0.008 }), x, 0, z), at(box(1.1, 0.12, 0.7, '#E9E1D2'), x, h, z));
      for (let k = 0; k < 3; k++) g.add(at(cyl(0.08, 0.09, 0.34, '#B5582E', 6, { pivot: 'bottom' }), x - 0.3 + 0.3 * k, h + 0.06, z));
    }
    if (o.plant !== false) { const [px, pz] = o.plant ?? [W / 2 - 1.0, 0.8]; g.add(at(cyl(0.28, 0.22, 0.5, '#B85C3E', 8, { pivot: 'bottom', outline: 0.008 }), px, 0, pz), at(sphere(0.48, '#4E8A4A', 1), px, 1.0, pz), at(cyl(0.03, 0.03, 0.5, '#6A4A30', 5, { pivot: 'bottom' }), px, 0.45, pz)); }
    return g;
  },

  // ---------------------------------------------------------------- an umbrella (pivot at the grip of its crook handle, shaft up +Y): o.open [[t, v]] 0 = furled
  // tight along the shaft, 1 = open (above 1: the canopy overshoots flatter and wider); eight panels in o.colors; o.L (0.95) the shaft, o.r (0.62) the canopy
  noUmbrella(o) {
    const Ls = o.L ?? 0.95, Rr = o.r ?? 0.62, cols = o.colors || ['#2F7F8C', '#F4F1E8'], g = grp();
    g.add(at(cyl(0.014, 0.014, Ls, '#2A2E36', 6, { pivot: 'bottom' }), 0, 0.06, 0));
    const crook = new THREE.Mesh(new THREE.TorusGeometry(0.06, 0.016, 5, 10, PI), mat('#6A4A30')); crook.position.set(0.06, 0.06, 0); crook.rotation.z = PI; g.add(crook);
    const can = grp(); can.position.y = Ls + 0.06; g.add(can);
    for (let k = 0; k < 8; k++) {
      const a0 = k / 8 * TAU, a1 = (k + 1) / 8 * TAU, geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.Float32BufferAttribute([0, 0, 0, Math.sin(a0), -1, Math.cos(a0), Math.sin(a1), -1, Math.cos(a1)], 3)); geo.computeVertexNormals();
      const p = new THREE.Mesh(geo, L(cols[k % cols.length], { side: THREE.DoubleSide })); p.castShadow = true; can.add(p);
    }
    const tip = cyl(0.012, 0.004, 0.1, '#2A2E36', 5, { pivot: 'bottom' }); tip.position.y = Ls + 0.06; g.add(tip);
    g.userData.update = t => { const v = Math.max(0, keyAt(o.open, t, 1)), rr = Rr * (0.07 + 0.93 * v), hh = 0.62 - 0.4 * clamp01(v) - 0.06 * Math.max(0, v - 1) * 4; can.scale.set(Math.max(0.01, rr), Math.max(0.05, hh), Math.max(0.01, rr)); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- an armful of baguettes (pivot at the middle of the bundle, hugged against a chest, front
  // +Z): o.n (5) baguettes fanned at angles, golden with slashes
  noArmful(o) {
    const n = o.n ?? 5, g = grp();
    for (let i = 0; i < n; i++) {
      const b = grp(at(ink(cyl(0.042, 0.036, 0.78, '#D9A35C', 8), 0.05), 0, 0, 0, 0, 0, PI / 2));
      for (let k = 0; k < 4; k++) b.add(at(box(0.06, 0.008, 0.035, '#A8692E'), -0.24 + k * 0.16, 0.038, 0, 0, 0.5, 0));
      b.position.set((i - (n - 1) / 2) * 0.03, (i - (n - 1) / 2) * 0.05, (i % 2) * 0.05); b.rotation.set(0, 0.15 * (i % 2 ? 1 : -1), 0.55 + (i - (n - 1) / 2) * 0.16); g.add(b);
    }
    return g;
  },

  // ---------------------------------------------------------------- an emptied bakery counter (pivot at the floor under the counter's middle, front +Z): a
  // back wall at o.back (-1.5) with three bare shelves of empty wicker baskets, a wooden counter with a marble top; o.crumb t0: the last crumb tips off
  // the top shelf, bounces on the middle one and drops on the bottom one
  noBakeryCounter(o) {
    const W = o.w ?? 3.2, back = o.back ?? -1.5, wood = '#A56A3E', g = grp();
    g.add(at(box(W + 3, 3.4, 0.12, o.wall || '#F3E3C6', { pivot: 'bottom' }), 0, 0, back - 0.06));
    const SY = [1.05, 1.6, 2.15];
    for (const y of SY) { g.add(at(box(W, 0.05, 0.42, wood, { outline: 0.006 }), 0, y, back + 0.21));
      for (let k = 0; k < 4; k++) { const x = (k - 1.5) * W / 4; g.add(at(box(0.58, 0.15, 0.32, '#C9995A', { pivot: 'bottom', outline: 0.006 }), x, y + 0.025, back + 0.22), at(box(0.5, 0.012, 0.25, '#7A5530'), x, y + 0.172, back + 0.22)); } }
    g.add(at(box(W, 1.0, 0.62, wood, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(W + 0.1, 0.06, 0.7, '#F2EEE6', { outline: 0.006 }), 0, 1.03, 0));
    for (let k = 0; k < 4; k++) g.add(at(box(W / 4 - 0.12, 0.7, 0.02, '#8E5A34'), (k - 1.5) * W / 4, 0.48, 0.32));
    const cx = o.cx ?? 0.35, cr = box(0.05, 0.035, 0.04, '#C98A44', { outline: 0.01 }); g.add(cr);
    const z0 = back + 0.4, path = [[0, SY[2] + 0.045, 0], [0.06, SY[2] + 0.07, 0.02], [0.28, SY[1] + 0.045, 0], [0.38, SY[1] + 0.14, 0.03], [0.48, SY[1] + 0.045, 0.06], [0.74, SY[0] + 0.045, 0.06], [0.82, SY[0] + 0.09, 0.07], [0.9, SY[0] + 0.045, 0.08]];
    g.userData.update = t => { const d = t - (o.crumb ?? 99); cr.visible = true; const dd = Math.max(0, d); let y = path[0][1], dz = 0;
      for (let i = 1; i < path.length; i++) if (dd >= path[i - 1][0]) { const u = clamp01((dd - path[i - 1][0]) / (path[i][0] - path[i - 1][0])), fall = path[i][1] < path[i - 1][1]; y = lerp(path[i - 1][1], path[i][1], fall ? u * u : 1 - (1 - u) * (1 - u)); dz = lerp(path[i - 1][2], path[i][2], u); }
      cr.position.set(cx, y, z0 + dz); cr.rotation.set(dd * 9, dd * 4, dd * 7); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the steps of a plain official building (pivot at the middle of the lowest step's front edge,
  // the steps climb toward -Z): o.n (7) steps of 0.17 x 0.36, o.w (7) wide, a landing, a pale stone front with four plain columns, a plain pediment and a
  // tall double door (no flag, no emblem, no lettering); o.open [[t, v]] opens the doors
  noSteps(o) {
    const N = o.n ?? 7, W = o.w ?? 7, SH = 0.17, SD = 0.36, g = grp(), stone = '#E4DCCB', Ht = N * SH, zt = -N * SD;
    for (let i = 0; i < N; i++) g.add(at(box(W, SH * (i + 1), SD, i % 2 ? stone : '#DCD3C0', { pivot: 'bottom', outline: 0.006 }), 0, 0, -SD * (i + 0.5)));
    g.add(at(box(W, Ht, 3.0, stone, { pivot: 'bottom' }), 0, 0, zt - 1.5));
    const fz = zt - 2.2, FW = W + 2, FHt = 6.4;
    g.add(at(box(FW, FHt, 0.4, '#EFE8DA', { pivot: 'bottom', outline: 0.01 }), 0, Ht, fz - 0.2));
    for (let k = 0; k < 4; k++) { const x = (k - 1.5) * 2.0; g.add(at(cyl(0.26, 0.3, 4.6, '#F6F1E6', 12, { pivot: 'bottom', outline: 0.008 }), x, Ht, fz + 0.9), at(box(0.75, 0.22, 0.75, '#E9E1D2'), x, Ht + 0.11, fz + 0.9), at(box(0.75, 0.22, 0.75, '#E9E1D2'), x, Ht + 4.6 - 0.11, fz + 0.9)); }
    g.add(at(box(FW, 0.5, 1.6, '#E9E1D2', { pivot: 'bottom', outline: 0.008 }), 0, Ht + 4.6, fz + 0.5));
    const ped = new THREE.Shape(); ped.moveTo(-FW / 2, 0); ped.lineTo(FW / 2, 0); ped.lineTo(0, 1.3); ped.closePath();
    const pm = new THREE.Mesh(new THREE.ExtrudeGeometry(ped, { depth: 1.2, bevelEnabled: false }), mat('#EFE8DA')); pm.position.set(0, Ht + 5.1, fz - 0.2); pm.castShadow = true; g.add(pm);
    g.add(at(box(2.0, 3.1, 0.05, '#2A2422', { pivot: 'bottom' }), 0, Ht, fz + 0.01));
    const doors = [-1, 1].map(sd => { const h = grp(); h.position.set(sd * 1.0, Ht, fz + 0.04); const d = box(1.0, 3.0, 0.08, '#6A4A34', { pivot: 'bottom', outline: 0.006 }); d.position.x = -sd * 0.5; h.add(d);
      h.add(at(box(0.06, 0.3, 0.04, '#C9A23A'), -sd * 0.88, 1.4, 0.06)); g.add(h); return { h, sd }; });
    g.userData.update = t => { const v = keyAt(o.open, t, 0); for (const { h, sd } of doors) h.rotation.y = sd * v * 1.75; };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- an oversized blister pack (pivot at its middle, front +Z): a silver card o.w (0.5) x o.h
  // (0.34) with 2 x 4 domes, every pill still sealed inside (a white tablet in a pale dome with a highlight)
  noBlister(o) {
    const W = o.w ?? 0.5, H = o.h ?? 0.34, g = grp(); g.add(box(W, H, 0.012, '#D3D8DE', { outline: 0.008 }));
    for (let r = 0; r < 2; r++) for (let k = 0; k < 4; k++) {
      const x = (k - 1.5) * W / 4.3, y = (r - 0.5) * H / 2.1;
      const dome = new THREE.Mesh(new THREE.SphereGeometry(0.05, 14, 8, 0, TAU, 0, PI / 2), L('#9FC9E2', { emissive: '#2A4656' })); dome.rotation.x = PI / 2; dome.scale.set(1, 1, 0.55); dome.position.set(x, y, 0.006); g.add(dome);
      g.add(at(ink(cyl(0.034, 0.034, 0.01, '#FFFFFF', 14, { emissive: '#606060' }), 0.12), x, y, 0.036, PI / 2, 0, 0));
      g.add(at(new THREE.Mesh(new THREE.CircleGeometry(0.009, 8), B('#FFFFFF')), x - 0.022, y + 0.02, 0.036));
    }
    return g;
  },

  // ---------------------------------------------------------------- a sea cliff (pivot at the middle of its top edge, y 0): a grass top running toward +Z o.d
  // (40) deep, a pale rock face dropping o.h (19) toward the sea on -Z, faceted boulders on the face (kept under the rim) and at its foot, a foam line
  // where it meets the water, grass tufts on the top (none within o.clearX ± 2.4 m of the rim, where the paper lies)
  noCliff(o) {
    const W = o.w ?? 60, H = o.h ?? 19, D = o.d ?? 40, g = grp();
    g.add(at(box(W, 0.5, D, '#7DB25A', { pivot: 'top' }), 0, 0.0, D / 2 - 0.3));
    // (review 1) the rock's top face lay in the grass top's plane: under SwiftShader they fought, the ground strobing green / grey every few frames
    g.add(at(box(W, H, D, '#C4B294', { pivot: 'top' }), 0, -0.15, D / 2 + 0.4));
    const cols = ['#B9A68A', '#C9B898', '#A89478', '#D3C4A6'];
    for (let i = 0; i < 70; i++) { const s = 0.8 + 2.2 * hsh(i + 9), x = (hsh(i) - 0.5) * W, y = -s - hsh(i + 50) * (H - s);
      g.add(at(facet(s * 1.3, s, s * 0.7, cols[i % 4], i + 3), x, y, 0.3 + 0.3 * hsh(i + 7))); }
    for (let i = 0; i < 26; i++) g.add(at(facet(1 + hsh(i + 80) * 1.5, 0.8 + hsh(i + 81), 1 + hsh(i + 82), cols[(i + 1) % 4], i + 90), (hsh(i + 83) - 0.5) * W, -H + 0.3, -0.8 - hsh(i + 84) * 1.6));
    g.add(at(box(W, 0.06, 0.9, '#F4FBFF'), 0, -H + 0.08, -2.4));
    for (let i = 0; i < 40; i++) { const x = (hsh(i + 200) - 0.5) * 14, z = 0.4 + hsh(i + 201) * 7; if (Math.abs(x - (o.clearX ?? 0.6)) < 2.4 && z < 4.5) continue; g.add(at(cyl(0.0, 0.09, 0.28, i % 2 ? '#5E9A44' : '#8CC266', 4, { pivot: 'bottom' }), x, 0.02, z)); }
    return g;
  },

  // ---------------------------------------------------------------- the corner of the giant leaflet hanging over an edge (pivot at the middle of the edge: the
  // flat part lies on the ground toward +Z, o.d (1.8) deep, the rest rounds the edge and hangs o.drop (1.6) down toward -Y), o.w (2.6) wide; the hanging
  // part flaps in the wind (o.flap, o.flapF); o.text: the last line printed in big bold letters on the flat part, o.textAt m from the edge, reading
  // upright for somebody at the edge looking inland (from the sea side: the canvas runs toward -X)
  noDrape(o) {
    const W = o.w ?? 2.6, Dd = o.d ?? 1.8, Dr = o.drop ?? 1.6, RR = 0.1, Lt = Dd + RR * PI / 2 + Dr, NX = 24, NY = 40, g = grp();
    const ch = 1024, cw = Math.round(1024 * W / Lt), cvF = canvas(cw, ch), cF = cvF.getContext('2d');
    drawPaper(cF, cw, ch, { creases: [2, 0], seed: 41, cols: 2, lh: 0.022, border: true });
    if (o.text) drawBig(cF, cw, ch, [].concat(o.text), { cy: (Dd - (o.textAt ?? 0.45)) / Lt, hf: (o.textH ?? 0.42) / Lt, wf: o.textW ?? 0.92 });
    const cvB = canvas(256, 256), cB = cvB.getContext('2d'); drawPaper(cB, 256, 256, { seed: 42, cols: 2 });
    const tF = tex(cvF), tB = tex(cvB);
    const P_ = [], U = [], I = [];
    for (let j = 0; j <= NY; j++) for (let i = 0; i <= NX; i++) { P_.push(0, 0, 0); U.push(1 - i / NX, 1 - j / NY); }
    for (let j = 0; j < NY; j++) for (let i = 0; i < NX; i++) { const a = j * (NX + 1) + i, b = a + 1, c = a + NX + 1, d = c + 1; I.push(a, b, c, b, d, c); }
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(P_, 3)); geo.setAttribute('uv', new THREE.Float32BufferAttribute(U, 2)); geo.setIndex(I);
    const mf = new THREE.Mesh(geo, L('#FFFFFF', { map: tF, emissive: '#FFFFFF', emissiveMap: tF, emissiveIntensity: o.glow ?? 0.22, side: THREE.FrontSide, ...OFF }));
    const mb = new THREE.Mesh(geo, L('#FFFFFF', { map: tB, emissive: '#FFFFFF', emissiveMap: tB, emissiveIntensity: 0.18, side: THREE.BackSide }));
    for (const m of [mf, mb]) { m.frustumCulled = false; m.receiveShadow = true; m.castShadow = true; } g.add(mf, mb);
    const pos = geo.attributes.position;
    g.userData.update = t => {
      for (let j = 0; j <= NY; j++) for (let i = 0; i <= NX; i++) {
        const n = j * (NX + 1) + i, x = (i / NX - 0.5) * W, s = j / NY * Lt; let y, z;
        if (s < Dd) { y = 0.065 + 0.012 * Math.sin(x * 3 + s * 2); z = Dd - s; if (s > Dd - 0.5) y += (o.lip ?? 0.05) * Math.sin(t * (o.flapF ?? 9) + x * 2) * Math.pow((s - (Dd - 0.5)) / 0.5, 2); }
        else if (s < Dd + RR * PI / 2) { const a = (s - Dd) / RR; y = 0.065 - RR * (1 - Math.cos(a)); z = -RR * Math.sin(a); }
        else { const h = s - Dd - RR * PI / 2, k = h / Dr, w = (o.flap ?? 0.5) * (0.6 + 0.4 * Math.sin(t * (o.flapF ?? 9) + x * 1.7 + h * 2.2));
          y = 0.065 - RR - h * Math.cos(w * k * 0.9); z = -RR - h * Math.sin(w * k * 0.9) - 0.08 * k * Math.sin(t * 13 + x * 3); }
        pos.setXYZ(n, x, y, z);
      }
      pos.needsUpdate = true; geo.computeVertexNormals();
    };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a magnifying glass with the holder's eye huge in it (review 1: the cartoon read of « he
  // peers through it »), pivot at the end of its handle, the lens up +Y facing +Z as magnifier (props_champagne): a dark handle, a brass ring, a big
  // painted eye on the front of the lens (white, inked, lashes on top), its iris moving with o.gx / o.gy [[t, v]] (-1..1, gy > 0 = down), the back of the
  // lens pale glass; o.r (0.07), o.iris colour, o.flip (hanging under the handle)
  noLoupe(o) {
    const R = o.r ?? 0.07, cy = 0.145 + R, g = grp(at(cyl(0.012, 0.014, 0.13, '#3B2A20', 8, { outline: 0.002 }), 0, 0.065, 0), at(cyl(0.015, 0.015, 0.02, '#B8902A', 8), 0, 0.135, 0));
    g.add(at(ink(new THREE.Mesh(new THREE.TorusGeometry(R, 0.008, 6, 28), L('#C9A23A')), 0.004), 0, cy, 0));
    const cv = canvas(256, 256), c = cv.getContext('2d');
    c.fillStyle = '#D8ECF6'; c.fillRect(0, 0, 256, 256);
    c.fillStyle = '#FFFFFF'; c.beginPath(); c.ellipse(128, 132, 118, 84, 0, 0, TAU); c.fill();
    c.strokeStyle = INK; c.lineWidth = 9; c.beginPath(); c.ellipse(128, 132, 118, 84, 0, 0, TAU); c.stroke();
    c.lineWidth = 7; for (let i = 0; i < 7; i++) { const a = PI + 0.35 + i * (PI - 0.7) / 6, x = 128 + Math.cos(a) * 118, y = 132 + Math.sin(a) * 84; c.beginPath(); c.moveTo(x, y); c.lineTo(x + Math.cos(a) * 26, y + Math.sin(a) * 30); c.stroke(); }
    const t1 = tex(cv), disc = new THREE.Mesh(new THREE.CircleGeometry(R * 0.98, 32), B('#FFFFFF', { map: t1 })); disc.position.set(0, cy, 0.001); g.add(disc);
    const back = new THREE.Mesh(new THREE.CircleGeometry(R * 0.98, 32), B('#DDF0FF', { side: THREE.BackSide })); back.position.set(0, cy, 0.0); g.add(back);
    const iris = grp(new THREE.Mesh(new THREE.CircleGeometry(R * 0.36, 24), B(o.iris || '#6B4A2A')), at(new THREE.Mesh(new THREE.CircleGeometry(R * 0.19, 20), B('#111318')), 0, 0, 0.001),
      at(new THREE.Mesh(new THREE.CircleGeometry(R * 0.08, 12), B('#FFFFFF')), R * 0.1, R * 0.1, 0.002));
    g.add(iris);
    // o.flip: the loupe hangs under its handle (rot z PI): the painted eye turned back upright
    const sg = o.flip ? -1 : 1; if (o.flip) { disc.rotation.z = PI; iris.rotation.z = PI; }
    const glint = new THREE.Mesh(new THREE.RingGeometry(R * 0.72, R * 0.84, 14, 1, 2.3, 0.7), B('#FFFFFF', { transparent: true, opacity: 0.8, side: THREE.DoubleSide, depthWrite: false })); glint.position.set(0, cy, 0.006); g.add(glint);
    g.userData.update = t => { iris.position.set(sg * (clamp01(0.5 + 0.5 * keyAt(o.gx, t, 0)) * R * 0.7 - R * 0.35), cy + sg * (0.04 * R - keyAt(o.gy, t, 0) * R * 0.28), 0.003); };
    g.userData.grip = [0, 0.05, 0]; g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a plain pharmacy front (pivot at the foot of its middle, front +Z): a white wall o.w (6.4)
  // wide with a green band, a shop window with shelves of plain white boxes behind the glass, a glass door with a green frame, and above the door a big
  // capsule-shaped sign, half white half green, glowing a little (no cross, no digit, no lettering); two plain windows upstairs
  noPharmacy(o) {
    const W = o.w ?? 6.4, Hh = o.h ?? 7.5, G = '#2E9A5E', g = grp();
    g.add(at(box(W, Hh, 0.3, o.wall || '#F2F0EA', { pivot: 'bottom', outline: 0.01 }), 0, 0, -0.15), at(box(W, 0.32, 0.08, G), 0, 3.15, 0.03), at(box(W, 0.5, 0.06, '#C9C4B8', { pivot: 'bottom' }), 0, 0, 0.02));
    const wx = -W * 0.17, ww = W * 0.5;
    g.add(at(box(ww, 2.0, 0.04, '#7FA6B0', { pivot: 'bottom', emissive: '#2A3E44' }), wx, 0.6, 0.05));
    for (const y of [0.95, 1.5, 2.05]) { g.add(at(box(ww - 0.1, 0.03, 0.2, '#E8E6E0'), wx, y, 0.12)); for (let k = 0; k < 9; k++) g.add(at(box(0.18, 0.24, 0.12, '#FBFBF8', { pivot: 'bottom', outline: 0.004 }), wx - ww / 2 + 0.22 + k * (ww - 0.4) / 8, y + 0.015, 0.14)); }
    for (const [x, y, w, h] of [[wx, 0.6, ww + 0.1, 0.08], [wx, 2.6, ww + 0.1, 0.08], [wx - ww / 2, 1.6, 0.08, 2.08], [wx + ww / 2, 1.6, 0.08, 2.08]]) g.add(at(box(w, h, 0.1, G, { outline: 0.004 }), x, y, 0.08));
    const dx = W * 0.3;
    g.add(at(box(1.15, 2.5, 0.06, G, { pivot: 'bottom', outline: 0.006 }), dx, 0.0, 0.04), at(box(0.85, 2.05, 0.03, '#9CC4C8', { pivot: 'bottom', emissive: '#2A3E44' }), dx, 0.22, 0.08));
    const sg = grp(); sg.position.set(dx, 3.7, 0.28); sg.rotation.z = o.tilt ?? 0;
    const cr = 0.33, cl = 0.8;
    const halfW = grp(at(cyl(cr, cr, cl / 2, '#FBFBF6', 16, { outline: 0.012, emissive: '#5A5A56' }), -cl / 4, 0, 0, 0, 0, PI / 2), at(sphere(cr, '#FBFBF6', 2, { emissive: '#5A5A56' }), -cl / 2, 0, 0));
    const halfG = grp(at(cyl(cr, cr, cl / 2, G, 16, { outline: 0.012, emissive: '#145A30' }), cl / 4, 0, 0, 0, 0, PI / 2), at(sphere(cr, G, 2, { emissive: '#145A30' }), cl / 2, 0, 0));
    for (const h of [halfW, halfG]) h.children.forEach(m => ink(m, 0.012));
    sg.add(halfW, halfG, at(box(0.06, 0.06, 0.3, '#3A3F48'), 0, 0, -0.17)); g.add(sg);
    for (const x of [-W * 0.25, W * 0.25]) g.add(at(box(1.1, 1.6, 0.05, '#4A6070', { pivot: 'bottom', emissive: '#1E2A32' }), x, 4.9, 0.02), at(box(1.3, 0.1, 0.14, '#FFFFFF'), x, 4.85, 0.06));
    g.userData.update = t => { const s = 1 + 0.06 * Math.sin(t * 3.2); sg.scale.set(s, s, s); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a plain pharmacy counter (pivot at the floor under the counter's middle, front +Z): a white
  // counter with a green band (no lettering), its top at 1.05; a back wall at o.back (-1.8) with shelves of identical plain white boxes
  noPharmaCounter(o) {
    const W = o.w ?? 3.0, back = o.back ?? -1.8, G = '#2E9A5E', g = grp();
    g.add(at(box(W + 6, 3.6, 0.12, o.wall || '#E6F0EA', { pivot: 'bottom' }), 0, 0, back - 0.06));
    for (const y of [0.7, 1.15, 1.6, 2.05, 2.5]) { g.add(at(box(W + 1.6, 0.04, 0.34, '#F2F2EE', { outline: 0.004 }), 0, y, back + 0.17));
      for (let k = 0; k < 13; k++) g.add(at(box(0.2, 0.28, 0.16, '#FDFDFA', { pivot: 'bottom', outline: 0.004 }), -(W + 1.4) / 2 + 0.15 + k * (W + 1.3) / 12, y + 0.02, back + 0.18)); }
    g.add(at(box(W, 1.0, 0.62, '#F6F6F2', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(W + 0.08, 0.05, 0.7, '#D9DCD6', { outline: 0.006 }), 0, 1.025, 0), at(box(W, 0.12, 0.02, G), 0, 0.82, 0.32));
    return g;
  },

  // ---------------------------------------------------------------- the referee's card (pivot at the middle of its foot, front +Z): white, o.w (0.26) x o.h
  // (0.34), with only a green laurel wreath drawn on it (no lettering)
  noLaurelCard(o) {
    const Wc = o.w ?? 0.26, Hc = o.h ?? 0.34, cv = canvas(256, Math.round(256 * Hc / Wc)), c = cv.getContext('2d'), W = cv.width, H = cv.height;
    c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.strokeStyle = '#C9A23A'; c.lineWidth = W * 0.03; c.strokeRect(W * 0.04, H * 0.03, W * 0.92, H * 0.94);
    const cx = W / 2, cy = H * 0.5, R = W * 0.33;
    for (const sd of [-1, 1]) { c.strokeStyle = '#3E7A3A'; c.lineWidth = W * 0.025; c.beginPath(); c.arc(cx, cy, R, PI / 2 + sd * 0.25, PI / 2 + sd * 2.6, sd < 0); c.stroke();
      for (let i = 0; i < 7; i++) { const a = PI / 2 + sd * (0.45 + i * 0.32), x = cx + Math.cos(a) * R, y = cy + Math.sin(a) * R;
        c.save(); c.translate(x, y); c.rotate(a + sd * 0.9); c.fillStyle = i % 2 ? '#4E9A48' : '#3E8A3A'; c.beginPath(); c.ellipse(0, 0, W * 0.07, W * 0.03, 0, 0, TAU); c.fill(); c.restore(); } }
    c.fillStyle = '#C8322A'; c.beginPath(); c.moveTo(cx - W * 0.06, cy + R + H * 0.02); c.lineTo(cx + W * 0.06, cy + R + H * 0.02); c.lineTo(cx + W * 0.09, cy + R + H * 0.11); c.lineTo(cx, cy + R + H * 0.06); c.lineTo(cx - W * 0.09, cy + R + H * 0.11); c.closePath(); c.fill();
    const t1 = tex(cv), g = grp(at(box(Wc + 0.012, Hc + 0.012, 0.008, '#E8E4DA', { outline: 0.004 }), 0, Hc / 2, 0));
    const f = new THREE.Mesh(new THREE.PlaneGeometry(Wc, Hc), L('#FFFFFF', { map: t1, emissive: '#FFFFFF', emissiveMap: t1, emissiveIntensity: 0.25 })); f.position.set(0, Hc / 2, 0.006); g.add(f);
    return g;
  },

  // ---------------------------------------------------------------- one chalk stroke drawn on a board (pivot at its top end, it grows down -Y): o.L (0.12),
  // o.draw [[t, v]] 0..1; o.tilt (rad); a chalk dust puff at its tip while it draws
  noChalkStroke(o) {
    const Ls = o.L ?? 0.12, g = grp(), s = box(o.wd ?? 0.012, 1, 0.003, '#F0F0E8', { pivot: 'top', emissive: '#808078' }); s.castShadow = false; g.add(s); g.rotation.z = o.tilt ?? 0;
    g.userData.update = t => { const v = clamp01(keyAt(o.draw, t, 0)); s.visible = v > 0.01; s.scale.y = Math.max(0.001, Ls * v); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- (review 2) a crab's pincer over a mitten (attach to a hand joint with face: 'camera'; pivot
  // at its hinge, the wrist): a fixed lower jaw and an upper jaw hinged on it, both tapered blocks the colour of the skin, inked, pointing along o.dir (+1:
  // +X, -1: -X) and tipped up o.up (rad); o.open [[t, v]] 0..1 opens the upper jaw up to o.a (0.95 rad) and drops the lower one a third as far: the clack
  // reads face-on at phone size whatever the hand does; o.s scales the whole claw (0.16 m jaws at 1)
  noPincer(o) {
    const S = o.s ?? 1, C = o.color || '#E2A878', DIR = o.dir ?? 1, g = grp(), root = grp(); g.add(root); root.scale.setScalar(S); root.rotation.z = DIR * (o.up ?? 0.5);
    if (DIR < 0) root.scale.x = -S;
    const jaw = (len, th) => { const p = grp(), b = box(len, th, 0.06, C, { outline: 0.012, taper: { x: 0.55, z: 0.8 }, taperAxis: 'x' }); b.position.x = len / 2; p.add(b);
      const tip = box(0.05, th * 0.55, 0.055, C, { outline: 0.012 }); tip.position.set(len + 0.012, 0, 0); p.add(tip); return p; };
    const lo = jaw(0.15, 0.055), hi = jaw(0.17, 0.07); lo.position.y = -0.028; hi.position.y = 0.028; root.add(lo, hi);
    const knuckle = box(0.075, 0.11, 0.07, C, { outline: 0.012 }); knuckle.position.x = -0.01; root.add(knuckle);
    g.userData.update = t => { const v = clamp01(keyAt(o.open, t, 0)), A = o.a ?? 0.95; hi.rotation.z = v * A; lo.rotation.z = -v * A * 0.35; };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- (review 2) a referee's shirt (attach to the torso joint; pivot at its collar, hangs -Y): a
  // box tunic to the hips with o.n (9) black and white vertical stripes painted all round, a black collar band; nothing else on it (no badge, no number)
  noRefShirt(o) {
    const w = o.w ?? 0.6, d = o.d ?? 0.38, h = o.h ?? 0.72, n = o.n ?? 9, g = grp();
    const plane = (W, H) => { const cv = canvas(256, 256), c = cv.getContext('2d'); for (let i = 0; i < n; i++) { c.fillStyle = i % 2 ? '#1C1D22' : '#F4F2EC'; c.fillRect(i * 256 / n, 0, 256 / n + 1, 256); }
      c.fillStyle = '#1C1D22'; c.fillRect(0, 0, 256, 18); const t1 = tex(cv); return new THREE.Mesh(new THREE.PlaneGeometry(W, H), L('#FFFFFF', { map: t1 })); };
    for (const [W, x, z, ry] of [[w, 0, d / 2, 0], [w, 0, -d / 2, PI], [d, w / 2, 0, PI / 2], [d, -w / 2, 0, -PI / 2]]) { const p = plane(W, h); p.position.set(x, -h / 2, z); p.rotation.y = ry; p.castShadow = true; g.add(p); }
    g.add(at(box(w, 0.02, d, '#1C1D22'), 0, -0.01, 0)); g.add(at(box(w * 0.42, 0.05, 0.04, '#1C1D22', { outline: 0.006 }), 0, -0.02, d / 2 + 0.01));
    return g;
  },

  // ---------------------------------------------------------------- sleep letters (pivot where they rise from, above a sleeper's head): inked white Z sprites
  // that float up and sideways, growing then fading, from o.at, one every o.every (0.35) s
  noZzz(o) {
    const g = grp(), N = 3, cv = canvas(128, 128), c = cv.getContext('2d');
    c.font = '900 104px Arial'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.lineJoin = 'round'; c.lineWidth = 12; c.strokeStyle = INK; c.strokeText('Z', 64, 68); c.fillStyle = '#FFFFFF'; c.fillText('Z', 64, 68);
    const tx = tex(cv), S = [];
    for (let i = 0; i < N; i++) { const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: tx, transparent: true, depthWrite: false })); g.add(sp); S.push(sp); }
    const E = o.every ?? 0.35, LIFE = E * N, sz = o.s ?? 0.22;
    g.userData.update = t => { const d = t - (o.at ?? 0); S.forEach((sp, i) => { const u = ((d - i * E) % LIFE + LIFE) % LIFE / LIFE, on = d - i * E >= 0; sp.visible = on;
      if (!on) return; sp.position.set((o.dir ?? 1) * u * 0.32 + 0.04 * Math.sin(u * 9), u * 0.6, 0); const k = sz * (0.5 + 0.9 * u); sp.scale.set(k, k, k); sp.material.opacity = Math.min(1, u * 6, (1 - u) * 3); }); };
    g.userData.update(0); return g;
  },
};
