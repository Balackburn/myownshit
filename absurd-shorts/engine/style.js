// Visual language of the shorts: flat-shaded low-poly, painterly paper grain,
// a restricted palette (cream / teal / navy / brick red) and black ink outlines.
import * as THREE from 'three';

export const PALETTE = {
  // environment
  cream: '#F1E9D2', creamDark: '#E3D7B8', paper: '#F6F1E3',
  teal: '#3F8A84', tealLight: '#7DB3AC', tealPale: '#A9CBC2',
  navy: '#1E2E44', navyLight: '#2E4563', ink: '#141A22',
  red: '#C23A2E', redDark: '#97291F', salmon: '#E8775F',
  sky: '#9FBBC4', skyNight: '#1B2638', grass: '#8FAE7A', sand: '#C9A86A', sandDark: '#B08F52',
  wood: '#C99A62', woodDark: '#8C6239', grey: '#B9B9B4', greyDark: '#6E726F',
  // characters
  skin: '#D9A877', skinPale: '#E9C9A6', skinDark: '#9A6A45', skinOlive: '#C8955F',
  suitNavy: '#1F3550', suitCharcoal: '#3A3D44', suitBrown: '#5C4330', suitBeige: '#C7B08A', suitGreen: '#2F4A3C',
  shirt: '#FAF8F2', tieRed: '#C8372D', lapelTeal: '#5FA3A0', hair: '#17181B',
  copBlue: '#6F8FAE', copBlueDark: '#3E5A78', swat: '#1C2430',
  white: '#FFFFFF', black: '#0E0F12', yellow: '#E6B84A', pink: '#E58FB0', green: '#6E9C5A',
};

// Deterministic PRNG so every render of the same script is identical.
export function rng(seed = 1) {
  let s = seed >>> 0 || 1;
  return () => { s ^= s << 13; s ^= s >>> 17; s ^= s << 5; return ((s >>> 0) % 100000) / 100000; };
}

// Painterly paper grain shared by every material (multiplied over base colour).
let _grain = null;
export function grainTexture() {
  if (_grain) return _grain;
  const c = document.createElement('canvas'); c.width = c.height = 256;
  const g = c.getContext('2d'); const r = rng(7);
  g.fillStyle = '#ffffff'; g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 9000; i++) {
    const v = 236 + Math.floor(r() * 19);
    g.fillStyle = `rgba(${v},${v},${v},${0.2 + r() * 0.3})`;
    g.fillRect(r() * 256, r() * 256, 1 + r() * 3, 1 + r() * 2);
  }
  // soft brush streaks
  for (let i = 0; i < 70; i++) {
    g.strokeStyle = `rgba(200,200,200,${0.05 + r() * 0.08})`;
    g.lineWidth = 2 + r() * 6; g.beginPath();
    const x = r() * 256, y = r() * 256; g.moveTo(x, y);
    g.bezierCurveTo(x + r() * 60, y + r() * 20, x + r() * 80, y - r() * 20, x + 40 + r() * 80, y + r() * 10);
    g.stroke();
  }
  _grain = new THREE.CanvasTexture(c);
  _grain.wrapS = _grain.wrapT = THREE.RepeatWrapping;
  _grain.colorSpace = THREE.SRGBColorSpace;
  return _grain;
}

const _matCache = new Map();
// Flat-shaded "paper" material. Lambert keeps the soft matte look of the source.
export function mat(color, opts = {}) {
  const key = color + JSON.stringify(opts);
  if (_matCache.has(key) && !opts.unique) return _matCache.get(key);
  const m = new THREE.MeshLambertMaterial({
    color: new THREE.Color(color), map: opts.noGrain ? null : grainTexture(),
    flatShading: true, side: opts.doubleSide ? THREE.DoubleSide : THREE.FrontSide,
    transparent: !!opts.opacity, opacity: opts.opacity ?? 1,
    emissive: opts.emissive ? new THREE.Color(opts.emissive) : new THREE.Color('#000000'),
  });
  if (!opts.unique) _matCache.set(key, m);
  return m;
}

// Box helper — nearly everything in this style is built from (tapered) boxes.
export function box(w, h, d, color, opts = {}) {
  const geo = new THREE.BoxGeometry(w, h, d);
  if (opts.taper) taperGeometry(geo, opts.taper, opts.taperAxis || 'y');
  if (opts.pivot === 'top') geo.translate(0, -h / 2, 0);
  if (opts.pivot === 'bottom') geo.translate(0, h / 2, 0);
  const m = new THREE.Mesh(geo, opts.material || mat(color, opts));
  m.castShadow = true; m.receiveShadow = true;
  if (opts.outline) addOutline(m, opts.outline);
  return m;
}

// Scale top face of a box (taper<1 => narrower top). Gives the trapezoid heads/jackets.
export function taperGeometry(geo, taper, axis = 'y') {
  const p = geo.attributes.position; geo.computeBoundingBox();
  const bb = geo.boundingBox; const ai = { x: 0, y: 1, z: 2 }[axis];
  const min = bb.min.getComponent(ai), max = bb.max.getComponent(ai);
  const tx = typeof taper === 'number' ? taper : taper.x, tz = typeof taper === 'number' ? taper : taper.z;
  for (let i = 0; i < p.count; i++) {
    const t = (p.getComponent(i, ai) - min) / (max - min || 1);
    const sx = 1 + (tx - 1) * t, sz = 1 + (tz - 1) * t;
    if (ai === 1) { p.setX(i, p.getX(i) * sx); p.setZ(i, p.getZ(i) * sz); }
    else if (ai === 0) { p.setY(i, p.getY(i) * sx); p.setZ(i, p.getZ(i) * sz); }
    else { p.setX(i, p.getX(i) * sx); p.setY(i, p.getY(i) * sz); }
  }
  p.needsUpdate = true; geo.computeVertexNormals();
}

// Inverted-hull ink outline (the thick black border around faces/heads).
export function addOutline(mesh, thickness = 0.02, color = PALETTE.ink) {
  const o = new THREE.Mesh(mesh.geometry, new THREE.MeshBasicMaterial({ color, side: THREE.BackSide }));
  o.scale.setScalar(1 + thickness); o.name = 'outline'; o.castShadow = false;
  mesh.add(o); return o;
}

export function cyl(rTop, rBot, h, color, seg = 7, opts = {}) {
  const geo = new THREE.CylinderGeometry(rTop, rBot, h, seg, 1, !!opts.open);
  if (opts.pivot === 'bottom') geo.translate(0, h / 2, 0);
  if (opts.pivot === 'top') geo.translate(0, -h / 2, 0);
  const m = new THREE.Mesh(geo, opts.material || mat(color, opts));
  m.castShadow = m.receiveShadow = true; return m;
}

export function sphere(r, color, detail = 0, opts = {}) {
  const m = new THREE.Mesh(new THREE.IcosahedronGeometry(r, detail), opts.material || mat(color, opts));
  m.castShadow = m.receiveShadow = true; return m;
}

// Canvas-painted text label (signs, "SOLD", "MILK", "60 km/h" ...).
export function textPlane(text, { w = 1, h = 0.4, bg = PALETTE.paper, fg = PALETTE.redDark, font = 'bold 90px Arial', border = null, align = 'center', lines = null } = {}) {
  const c = document.createElement('canvas'); c.width = 512; c.height = Math.round(512 * h / w);
  const g = c.getContext('2d');
  if (bg) { g.fillStyle = bg; g.fillRect(0, 0, c.width, c.height); }
  if (border) { g.strokeStyle = border; g.lineWidth = 14; g.strokeRect(7, 7, c.width - 14, c.height - 14); }
  g.fillStyle = fg; g.font = font; g.textAlign = align; g.textBaseline = 'middle';
  const ls = lines || String(text).split('\n');
  const lh = c.height / (ls.length + 0.4);
  ls.forEach((l, i) => g.fillText(l, align === 'center' ? c.width / 2 : 24, lh * (i + 0.7)));
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshLambertMaterial({ map: tex, transparent: !bg, side: THREE.DoubleSide }));
  return m;
}

export const ease = {
  linear: t => t,
  inOut: t => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2,
  out: t => 1 - Math.pow(1 - t, 3),
  in: t => t * t * t,
  outBack: t => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); },
  outElastic: t => t === 0 || t === 1 ? t : Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * (2 * Math.PI) / 3) + 1,
};
export const clamp01 = x => Math.max(0, Math.min(1, x));
export const lerp = (a, b, t) => a + (b - a) * t;
