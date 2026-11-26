// « Le sel » (story 109, cycle 58): at a family meal this man asks for the salt; mamie passes it from the far end of the table, but the table grows
// faster than the salt moves (cousin Thierry's fiancée and eleven brothers, three babies, the garden, the village, a market between the pear and the
// cheese, the whole country descending from mamie, lorries stopping to let the salt pass); a mathematician proves it will never arrive; then the
// cousins run out, the table stops and the shaker arrives, empty: every hand that passed it sneaked a pinch. The whole country has high blood
// pressure, except him. He has just asked for the pepper.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
// Running gag drawn here: the big salt shaker (seShaker) is an inked glass outline around an opaque white salt column whose level steps down at
// every pinch (o.fill keys: full, three quarters, half, empty), and every cheater keeps a white heap on a blue plate (seHeap).
import * as THREE from 'three';
import { box, cyl, sphere, mat, addOutline } from './style.js';
import { grp, at } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const lerp = (a, b, u) => a + (b - a) * u;
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
// [[t, v], ...] -> v at t, smoothstep between keys (a key [t, v, 'lin'] makes its segment linear)
const keyAt = (K, t, d = 0) => {
  if (K === undefined || K === null) return d;
  if (typeof K === 'number') return K;
  if (!K.length) return d;
  if (t <= K[0][0]) return K[0][1];
  for (let i = 1; i < K.length; i++) if (t < K[i][0]) { const u = (t - K[i - 1][0]) / Math.max(1e-6, K[i][0] - K[i - 1][0]); return lerp(K[i - 1][1], K[i][1], K[i][2] === 'lin' ? u : smooth(u)); }
  return K[K.length - 1][1];
};
// inside one of the intervals [[t0, t1], ...]: the time since its start, else -1
const inside = (I, t) => { for (const [a, b] of I || []) if (t >= a && t < b) return t - a; return -1; };
// a damped wobble summed over [[t0, amp, freq, decay], ...]
const rattle = (R, t) => { let s = 0; for (const [t0, amp, f, dk] of R || []) { const u = t - t0; if (u > 0) s += amp * Math.sin(u * (f ?? 18)) * Math.exp(-u * (dk ?? 3.5)); } return s; };
const tex = cv => { const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t; };
const canvas = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
const L = (c, o = {}) => new THREE.MeshLambertMaterial({ color: c, ...o });
const INK = '#1B1E2A';
const ink = (m, t = 0.03) => { addOutline(m, t); return m; };
const noShadow = g => { g.traverse(c => { if (c.isMesh) { c.castShadow = false; c.receiveShadow = false; } }); return g; };
const OFF = { polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -8 };
// a canvas painted plane (Lambert, lit like the set; o.emissive makes it read in shade); front +Z; o.offset: a polygon offset (laid on a surface)
function paintPlane(w, h, draw, o = {}) {
  const cv = canvas(o.res ?? 256, Math.max(8, Math.round((o.res ?? 256) * h / w))); draw(cv.getContext('2d'), cv.width, cv.height);
  const t = tex(cv), m = L('#FFFFFF', { map: t, side: o.double ? THREE.DoubleSide : THREE.FrontSide, ...(o.emissive ? { emissive: '#FFFFFF', emissiveMap: t, emissiveIntensity: o.emissive } : {}), ...(o.offset ? OFF : {}) });
  const p = new THREE.Mesh(new THREE.PlaneGeometry(w, h), m); p.receiveShadow = true; return p;
}
// a faceted lump (jittered icosphere, shared vertices keep their offset)
function lump(rx, ry, rz, color, seed = 3, jit = 0.12, detail = 1, o = {}) {
  const g = new THREE.IcosahedronGeometry(1, detail), p = g.attributes.position, off = new Map();
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i), y = p.getY(i), z = p.getZ(i), k = `${Math.round(x * 999)},${Math.round(y * 999)},${Math.round(z * 999)}`;
    if (!off.has(k)) off.set(k, 1 + (hsh(seed * 31 + off.size * 7.3) - 0.5) * 2 * jit);
    const f = off.get(k); p.setXYZ(i, x * rx * f, y * ry * f, z * rz * f);
  }
  g.computeVertexNormals(); const m = new THREE.Mesh(g, o.material || mat(color, o)); m.castShadow = m.receiveShadow = true; return m;
}
// a dome of snow (pivot at its base): a flattened lump cut at the bottom, pure white, a faint ink rim
function snowDome(r, seed = 1, h = 0.55) {
  const m = lump(r, r * h, r, '#FFFFFF', seed, 0.14, 1, { emissive: '#7A8A96', noGrain: true }); m.position.y = r * h * 0.15; ink(m, 0.06); return m;
}

// ---------------------------------------------------------------- glass that reads at phone size: an inked silhouette (a Fresnel edge drawn in ink, whatever
// the view), a pale see-through middle; drawn after the opaque salt
function glassShader(tint = '#D6EEF8', edge = 0.8, alpha = 0.1) {
  return new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, side: THREE.DoubleSide,
    uniforms: { cGlass: { value: new THREE.Color(tint) }, cInk: { value: new THREE.Color(INK) }, edge: { value: edge }, a0: { value: alpha } },
    vertexShader: 'varying vec3 vN; varying vec3 vV;\nvoid main() { vec4 mv = modelViewMatrix * vec4(position, 1.0); vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix * mv; }',
    fragmentShader: 'uniform vec3 cGlass; uniform vec3 cInk; uniform float edge; uniform float a0; varying vec3 vN; varying vec3 vV;\nvoid main() { float f = 1.0 - abs(dot(normalize(vN), normalize(vV))); vec3 c = mix(cGlass, vec3(1.0), smoothstep(0.55, 0.75, f) * 0.6); float a = a0 + 0.5 * pow(f, 3.0); if (f > edge) { c = cInk; a = 1.0; } gl_FragColor = vec4(c, a);\n#include <colorspace_fragment>\n}',
  });
}

// ---------------------------------------------------------------- a dining chair (pivot at the floor, the seat faces +Z: the sitter looks +Z), seat at 0.48
function chairMesh(c = '#6A4430', cushion = '#B8544A') {
  const g = grp(at(box(0.46, 0.06, 0.46, c, { outline: 0.01 }), 0, 0.45, 0), at(box(0.42, 0.04, 0.4, cushion), 0, 0.49, 0.01),
    at(box(0.46, 0.5, 0.05, c, { outline: 0.008 }), 0, 0.73, -0.205), at(box(0.36, 0.08, 0.06, c), 0, 0.98, -0.205));
  for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(at(box(0.045, 0.42, 0.045, '#3E2A1E', { pivot: 'bottom' }), sx * 0.19, 0, sz * 0.19));
  return g;
}

// ---------------------------------------------------------------- one place setting (pivot on the table top at the plate's centre, the diner on the -Z side
// facing +Z... i.e. the plate's near edge toward -Z): a blue plate with a white rim (a white heap reads on it), a short tumbler, a folded napkin
function placeMesh(o = {}, flutter = null) {
  const g = grp(), pr = o.plateR ?? 0.13;
  const plate = cyl(pr, pr * 0.82, 0.018, '#F6F3EC', 24, { pivot: 'bottom', noGrain: true }); plate.material = L('#F6F3EC', OFF); ink(plate, 0.03); g.add(plate);
  const well = cyl(pr * 0.72, pr * 0.72, 0.004, '#7FA9CF', 24, { noGrain: true }); well.material = L('#7FA9CF', { emissive: '#1E3A5A', emissiveIntensity: 0.25, ...OFF }); well.position.y = 0.019; g.add(well);
  if (o.glass !== false) { const gl = cyl(0.035, 0.03, 0.1, '#CFE3EE', 10, { pivot: 'bottom', noGrain: true }); gl.material = L('#CFE3EE', { emissive: '#3A5A6A', emissiveIntensity: 0.3 }); ink(gl, 0.05); gl.position.set(pr + 0.07, 0, -0.06); g.add(gl); }
  if (o.napkin !== false) {
    const nap = grp(); const sh = new THREE.Shape(); sh.moveTo(-0.06, 0); sh.lineTo(0.06, 0); sh.lineTo(0, 0.13); sh.closePath();
    const nm = new THREE.Mesh(new THREE.ShapeGeometry(sh), L('#FFFFFF', { side: THREE.DoubleSide, emissive: '#6A6A6A' })); nm.castShadow = true; nap.add(nm);
    const edge = new THREE.Mesh(new THREE.ShapeGeometry(sh), new THREE.MeshBasicMaterial({ color: INK, side: THREE.DoubleSide })); edge.scale.setScalar(1.12); edge.position.set(0, -0.006, -0.002); nap.add(edge);
    nap.position.set(-pr - 0.06, 0.004, 0); nap.rotation.x = -0.25; g.add(nap); if (flutter) flutter.push(nap);
  }
  return g;
}

// ---------------------------------------------------------------- the running gag's heap of salt (pivot at its base): a lumpy opaque white cone with an ink rim
function heapMesh(r, seed = 2) {
  const geo = new THREE.ConeGeometry(r, r * 0.95, 9, 2), p = geo.attributes.position;
  for (let i = 0; i < p.count; i++) { const y = p.getY(i); if (y < r * 0.47) { const f = 1 + (hsh(i * 3 + seed) - 0.5) * 0.28; p.setX(i, p.getX(i) * f); p.setZ(i, p.getZ(i) * f); } }
  geo.translate(0, r * 0.475, 0); geo.computeVertexNormals();
  const m = new THREE.Mesh(geo, mat('#FFFFFF', { emissive: '#8A8A8A', noGrain: true })); m.castShadow = true; m.receiveShadow = true; ink(m, 0.07); return m;
}

export const SEL_PROPS = {

  // ---------------------------------------------------------------- the big salt shaker (pivot at the middle of its base, the cap up), bottle size: o.h (0.36)
  // An inked glass cylinder (glassShader: the outline holds from any side, the middle is see-through) round an opaque bright white salt column
  // whose height is o.fill [[t, 0..1]] (1 full, 0.75, 0.5, 0: empty), a heavy pale glass foot, a chrome cap with dark holes and an ink rim;
  // two white glints. o.r (0.075) the glass radius; at each level step the salt top settles with a small bounce (o.settle [t...])
  seShaker(o) {
    const H = o.h ?? 0.36, R = o.r ?? 0.075, BH = H * 0.72, g = grp();
    // (round 1) the foot is clear glass like the rest (a pale opaque foot read as a white disc of salt left in an empty shaker)
    const foot = new THREE.Mesh(new THREE.CylinderGeometry(R * 1.06, R * 1.1, 0.025, 28).translate(0, 0.0125, 0), glassShader(o.tint || '#C4E4F4', 0.8, 0.16)); foot.renderOrder = 4; foot.castShadow = false; g.add(foot);
    const glass = new THREE.Mesh(new THREE.CylinderGeometry(R, R * 1.03, BH, 40, 1, true), glassShader(o.tint || '#C4E4F4', o.edge ?? 0.8, o.alpha ?? 0.16)); glass.position.y = 0.025 + BH / 2; glass.renderOrder = 4; glass.castShadow = false; g.add(glass);
    // the rims: an ink ring at the shoulder and at the foot
    for (const y of [0.002, 0.026, 0.025 + BH]) { const rr = new THREE.Mesh(new THREE.TorusGeometry(R * 1.02, 0.0055, 5, 32), new THREE.MeshBasicMaterial({ color: INK })); rr.rotation.x = PI / 2; rr.position.y = y; g.add(rr); }
    // the salt: an opaque white column with a lumpy top; scaled in y by the fill level
    const saltG = grp(); saltG.position.y = 0.027; g.add(saltG);
    const sh = BH - 0.012, col = cyl(R * 0.9, R * 0.9, 1, '#FFFFFF', 28, { pivot: 'bottom', noGrain: true }); col.material = L('#FFFFFF', { emissive: '#B9B9B9' }); ink(col, 0.035); saltG.add(col);
    const top = lump(R * 0.88, R * 0.22, R * 0.88, '#FFFFFF', 7, 0.18, 1, { emissive: '#B9B9B9', noGrain: true }); saltG.add(top);
    // the cap: a chrome collar and a dome with dark holes
    const cap = grp(); cap.position.y = 0.025 + BH; g.add(cap);
    const collar = cyl(R * 1.08, R * 1.08, H * 0.1, '#B9C1CB', 24, { pivot: 'bottom', noGrain: true }); collar.material = L('#B9C1CB', { emissive: '#3A4250', emissiveIntensity: 0.4 }); ink(collar, 0.04); cap.add(collar);
    const band = cyl(R * 1.1, R * 1.1, H * 0.022, '#8C96A4', 24, { noGrain: true }); band.position.y = H * 0.03; cap.add(band);
    const dome = new THREE.Mesh(new THREE.SphereGeometry(R * 1.08, 24, 8, 0, TAU, 0, PI / 2), L('#C9D0D8', { emissive: '#3A4250', emissiveIntensity: 0.4 })); dome.scale.y = 0.55; dome.position.y = H * 0.1; ink(dome, 0.04); cap.add(dome);
    for (let i = 0; i < 6; i++) { const a = i / 5 * TAU, rr = i === 5 ? 0 : R * 0.48; const hole = cyl(R * 0.11, R * 0.11, 0.004, '#22262E', 8, { noGrain: true });
      const y0 = H * 0.1 + R * 1.08 * 0.55 * Math.sqrt(Math.max(0, 1 - (rr / (R * 1.08)) ** 2)); hole.position.set(Math.cos(a) * rr, y0 + 0.001, Math.sin(a) * rr); cap.add(hole); }
    // glints: two thin white strokes on the front of the glass
    for (const [x, w_, h_] of [[-0.45, 0.012, 0.6], [-0.2, 0.006, 0.3]]) { const gl = box(w_ * (R / 0.075), BH * h_, 0.002, '#FFFFFF', { noGrain: true }); gl.material = new THREE.MeshBasicMaterial({ color: '#FFFFFF' }); gl.position.set(x * R, 0.025 + BH * 0.55, R * 1.02); gl.castShadow = false; g.add(gl); }
    g.userData.update = t => {
      const f = clamp01(keyAt(o.fill, t, 1)); let b = 0; for (const s of o.settle || []) { const u = t - s; if (u > 0 && u < 0.4) b += 0.12 * Math.sin(u * 30) * Math.exp(-u * 9); }
      const hgt = Math.max(0.0001, sh * f); col.scale.y = hgt; col.visible = f > 0.005; top.visible = f > 0.02; top.position.y = hgt; top.scale.set(1, 1 + b * 3, 1);
    };
    g.userData.update(0); g.userData.grip = [0, BH * 0.5, 0]; return g;
  },

  // ---------------------------------------------------------------- a heap of salt on a plate (pivot at its base): o.r (0.045), o.grow [[t, 0..1]] its size
  seHeap(o) {
    const g = grp(), hm = heapMesh(o.r ?? 0.045, o.seed ?? 2); g.add(hm);
    g.userData.update = t => { const s = keyAt(o.grow, t, 1); hm.visible = s > 0.01; hm.scale.setScalar(Math.max(0.001, s)); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a trickle of salt grains (pivot where they leave the cap; they fall along -Y for o.len
  // (0.3) m): o.on [[t0, t1]]; o.n (14) grains, o.s (0.014) their size (white cubes with an ink edge, oversized to read)
  seGrains(o) {
    const g = grp(), N = o.n ?? 14, Ls = o.len ?? 0.3, S = o.s ?? 0.014, Q = [];
    for (let i = 0; i < N; i++) { const m = box(S, S, S, '#FFFFFF', { noGrain: true, emissive: '#9A9A9A' }); ink(m, 0.12); m.castShadow = false; g.add(m); Q.push({ m, ph: hsh(i + 1), dx: (hsh(i * 5) - 0.5) * 0.04, dz: (hsh(i * 7) - 0.5) * 0.04 }); }
    g.userData.update = t => { const d = inside(o.on, t);
      for (const q of Q) { q.m.visible = d >= 0; if (d < 0) continue; const u = ((d * (o.speed ?? 3.2)) + q.ph) % 1; q.m.position.set(q.dx * (0.4 + u), -Ls * u * u, q.dz * (0.4 + u)); q.m.rotation.set(u * 9, u * 7, 0); } };
    g.userData.update(-1); return g;
  },

  // ---------------------------------------------------------------- a dining-table segment along X (pivot at the floor under its middle): o.len (2) long,
  // o.w (1.0) wide, o.h (0.76); dark wood, a dark red cloth runner down the middle (the white salt reads on it); o.legs (true; false: a leaf, a bare top);
  // o.places [[x, side], ...]: a blue plate, a tumbler and a napkin at x on the side +1 (z > 0) or -1; o.chairs [[x, side], ...]: empty chairs facing
  // the table; o.flutter: the napkins flap in the wind (o.flutter [[t0, t1]] or true); o.wood / o.cloth: colours
  seTable(o) {
    const len = o.len ?? 2, w = o.w ?? 1.0, h = o.h ?? 0.76, g = grp(), WOOD = o.wood || '#5E3B26';
    g.add(at(box(len, 0.06, w, WOOD, { outline: 0.012 }), 0, h - 0.03, 0));
    const run = box(len + 0.002, 0.008, Math.min(0.42, w * 0.42), o.cloth || '#8C1E2C', { noGrain: true }); run.material = L(o.cloth || '#8C1E2C', OFF); run.position.y = h + 0.004; g.add(run);
    for (const sd of [-1, 1]) { const tr = box(len + 0.004, 0.009, 0.022, '#E2B95A', { noGrain: true }); tr.material = L('#E2B95A', OFF); tr.position.set(0, h + 0.0045, sd * Math.min(0.42, w * 0.42) * 0.42); g.add(tr); }
    if (o.legs !== false) { const inset = o.inset ?? 0.1; for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(at(box(0.07, h - 0.06, 0.07, '#3E2618', { pivot: 'bottom' }), sx * (len / 2 - inset), 0, sz * (w / 2 - 0.08)));
      g.add(at(box(len - 0.1, 0.1, 0.03, '#4A2E1E'), 0, h - 0.11, w / 2 - 0.05), at(box(len - 0.1, 0.1, 0.03, '#4A2E1E'), 0, h - 0.11, -w / 2 + 0.05)); }
    const flutter = [];
    for (const [x, sd] of o.places || []) { const p = placeMesh(o, flutter); p.position.set(x, h, sd * (w / 2 - 0.2)); if (sd < 0) p.rotation.y = PI; g.add(p); }
    for (const [x, sd] of o.chairs || []) { const c = chairMesh(o.chairColor, o.cushion); c.position.set(x, 0, sd * (w / 2 + 0.3)); c.rotation.y = sd > 0 ? PI : 0; g.add(c); }
    if (flutter.length && o.flutter) g.userData.update = t => { const on = o.flutter === true || inside(o.flutter, t) >= 0;
      flutter.forEach((n, i) => { n.rotation.x = -0.25 - (on ? 0.9 + 0.45 * Math.sin(t * 17 + i * 1.7) : 0); n.rotation.z = on ? 0.25 * Math.sin(t * 13 + i) : 0; }); };
    g.userData.update?.(0); g.userData.top = [0, h, 0]; return g;
  },

  // ---------------------------------------------------------------- a table leaf (pivot at its middle, top up): a bare top with the runner, o.len (0.9), o.w (1.0);
  // carried like a door (rotate it), slotted between two segments
  seLeaf(o) {
    const len = o.len ?? 0.9, w = o.w ?? 1.0, g = grp(), WOOD = o.wood || '#5E3B26';
    g.add(at(box(len, 0.06, w, WOOD, { outline: 0.014 }), 0, 0, 0));
    const run = box(len + 0.002, 0.008, Math.min(0.42, w * 0.42), o.cloth || '#8C1E2C', { noGrain: true }); run.material = L(o.cloth || '#8C1E2C', OFF); run.position.y = 0.034; g.add(run);
    for (const sd of [-1, 1]) { const tr = box(len + 0.004, 0.009, 0.022, '#E2B95A', { noGrain: true }); tr.material = L('#E2B95A', OFF); tr.position.set(0, 0.0345, sd * Math.min(0.42, w * 0.42) * 0.42); g.add(tr); }
    // the underside: two runners and a pair of brass pegs on the ends (it reads as a table part, not a plank)
    for (const sd of [-1, 1]) g.add(at(box(len - 0.08, 0.05, 0.04, '#4A2E1E'), 0, -0.05, sd * (w / 2 - 0.12)), at(cyl(0.012, 0.012, 0.06, '#D8B54A', 6), sd * (len / 2 + 0.02), 0, sd * 0.25, 0, 0, PI / 2));
    return g;
  },

  // ---------------------------------------------------------------- the hero's roast on its plate (pivot at the plate's base): a big glazed roast tied with string,
  // a bone, potatoes, parsley; o.snow (0..1): a cap of snow on it; o.s (1) its scale
  seRoast(o) {
    const s = o.s ?? 1, g = grp(), pl = cyl(0.2, 0.16, 0.022, '#F6F3EC', 24, { pivot: 'bottom', noGrain: true }); pl.material = L('#F6F3EC', OFF); ink(pl, 0.025); g.add(pl);
    const meat = lump(0.15, 0.085, 0.1, '#8A4424', 4, 0.06, 1); meat.position.y = 0.022 + 0.07; ink(meat, 0.035); g.add(meat);
    const glaze = lump(0.125, 0.04, 0.08, '#C0682E', 5, 0.08, 1, { emissive: '#4A1A06' }); glaze.position.y = 0.022 + 0.125; g.add(glaze);
    for (const x of [-0.07, 0, 0.07]) { const st = new THREE.Mesh(new THREE.TorusGeometry(0.09, 0.006, 4, 16), mat('#F2E6C8', { noGrain: true })); st.position.set(x, 0.022 + 0.08, 0); st.rotation.y = PI / 2; st.scale.set(1, 0.95, 1.18); g.add(st); }
    const bone = grp(at(cyl(0.016, 0.016, 0.09, '#F4ECD8', 8), 0, 0, 0, 0, 0, PI / 2), at(sphere(0.022, '#F4ECD8', 1), 0.05, 0.008, 0.01), at(sphere(0.022, '#F4ECD8', 1), 0.05, -0.008, -0.01));
    bone.position.set(0.17, 0.022 + 0.08, 0); ink(bone.children[0], 0.06); g.add(bone);
    [[-0.13, 0.1], [-0.15, -0.08], [0.1, 0.13], [0.04, -0.13]].forEach(([x, z], i) => { const p = lump(0.035, 0.026, 0.03, '#E8C25A', 11 + i, 0.1, 1); p.position.set(x, 0.022 + 0.022, z); ink(p, 0.05); g.add(p); });
    [[-0.05, 0.13], [0.13, -0.1]].forEach(([x, z], i) => { const p = lump(0.025, 0.012, 0.025, '#4E9A3E', 21 + i, 0.2, 0); p.position.set(x, 0.026, z); g.add(p); });
    const snow = snowDome(0.12, 3, 0.45); snow.position.y = 0.022 + 0.14; snow.scale.set(1.15, 1, 0.85); g.add(snow);
    g.scale.setScalar(s);
    g.userData.update = t => { const v = keyAt(o.snow, t, 0); snow.visible = v > 0.01; snow.scale.set(1.15 * Math.max(0.01, v), Math.max(0.01, v), 0.85 * Math.max(0.01, v)); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a cartoon knife or fork (pivot at the end of the handle, along +Y), o.kind 'knife' | 'fork',
  // o.len (0.46): oversized to read on a phone; a dark wooden handle, a silver blade or tines with an ink rim; o.snow (0..1): a snow cap on the tip
  seUtensil(o) {
    const Lh = o.len ?? 0.46, g = grp(), hl = Lh * 0.38;
    const handle = box(0.036, hl, 0.022, '#4A2C1C', { pivot: 'bottom', outline: 0.04 }); g.add(handle);
    for (const y of [hl * 0.3, hl * 0.7]) g.add(at(cyl(0.006, 0.006, 0.024, '#D8C8A0', 6), 0, y, 0.012, PI / 2));
    g.add(at(box(0.04, 0.02, 0.026, '#C9CED6', { noGrain: true }), 0, hl + 0.01, 0));
    const SV = '#D6DBE2';
    if (o.kind === 'fork') {
      g.add(ink(at(box(0.026, Lh * 0.2, 0.01, SV, { pivot: 'bottom', noGrain: true, emissive: '#3A4250' }), 0, hl + 0.02, 0), 0.06));
      const y0 = hl + 0.02 + Lh * 0.2; g.add(ink(at(box(0.07, 0.022, 0.01, SV, { noGrain: true, emissive: '#3A4250' }), 0, y0 + 0.011, 0), 0.06));
      for (let i = 0; i < 4; i++) g.add(ink(at(box(0.011, Lh * 0.26, 0.01, SV, { pivot: 'bottom', noGrain: true, emissive: '#3A4250' }), -0.028 + i * 0.0187, y0 + 0.02, 0), 0.08));
    } else {
      const bl = box(0.05, Lh * 0.6, 0.008, SV, { pivot: 'bottom', taper: { x: 0.55, z: 1 }, noGrain: true, emissive: '#3A4250' }); bl.position.set(0.004, hl + 0.02, 0); ink(bl, 0.05); g.add(bl);
    }
    const snow = snowDome(0.042, 9, 0.8); snow.position.y = Lh + 0.004; g.add(snow);
    g.userData.update = t => { const v = keyAt(o.snow, t, 0); snow.visible = v > 0.01; snow.scale.setScalar(Math.max(0.01, v)); };
    g.userData.update(0); g.userData.grip = [0, hl * 0.5, 0]; return g;
  },

  // ---------------------------------------------------------------- a cap of snow (pivot at its base): o.r (0.14), o.h (0.55) its height against its width
  seSnowCap(o) {
    if (!o.slab) return grp(snowDome(o.r ?? 0.14, o.seed ?? 5, o.h ?? 0.55));
    // (round 3) o.slab: a flat slab of snow that follows a box head (o.w x o.d, o.t thick), soft drips hanging over its edges, the same white and
    // glow as the domes on the knife and the fork, no ink inside its outline (a dome with two inked facets read as a beret with eyes)
    const W = o.w ?? 0.4, D = o.d ?? 0.34, T = o.t ?? 0.07, SO = { noGrain: true, emissive: '#7A8A96' }, g = grp();
    g.add(box(W, T, D, '#FFFFFF', { pivot: 'bottom', ...SO }), at(box(W * 0.86, T * 0.6, D * 0.84, '#FFFFFF', { pivot: 'bottom', ...SO }), 0, T * 0.9, 0));
    const drips = o.drips || [[-0.3, 1, 0.07], [0.05, 1, 0.1], [0.34, 1, 0.06], [1, -0.2, 0.08], [1, 0.3, 0.05], [-1, 0.1, 0.07], [-0.1, -1, 0.06]];
    const DR = o.dripR ?? 0.03; drips.forEach(([u, v, len], i) => { const dr = lump(DR, len / 2 + DR / 2, DR, '#FFFFFF', 30 + i, 0.08, 1, SO);
      const x = Math.abs(u) === 1 ? u * W / 2 : u * W / 2, z = Math.abs(v) === 1 ? v * D / 2 : v * D / 2; dr.position.set(x, T * 0.5 - len / 2, z); g.add(dr); });
    return g;
  },

  // ---------------------------------------------------------------- a high chair seen from behind (pivot at the floor, the baby faces +Z): splayed legs, a seat at
  // 0.78 with a backrest, a tray in front; the baby is a pastel bonnet with a frill and a bow at the back, the ties of a white bib at the nape, a small
  // arm that bangs a spoon on the tray (o.bang [[t0, t1]]); o.bonnet colour; o.pop (s): it springs in from nothing with an overshoot at that time
  seHighChair(o) {
    const g = grp(), inner = grp(); g.add(inner); const W = '#F2EEE4', C = o.bonnet || '#F2A8BC';
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) { const lg = box(0.04, 0.82, 0.04, W, { pivot: 'bottom', outline: 0.03 }); lg.position.set(sx * 0.2, 0, sz * 0.2); lg.rotation.set(-sz * 0.12, 0, sx * 0.12); inner.add(lg); }
    inner.add(at(box(0.36, 0.05, 0.34, W, { outline: 0.02 }), 0, 0.8, 0), at(box(0.36, 0.42, 0.04, W, { outline: 0.02 }), 0, 1.02, -0.16));
    inner.add(at(box(0.5, 0.03, 0.26, '#9ED6C8', { outline: 0.02 }), 0, 0.98, 0.22), at(box(0.04, 0.16, 0.04, W), -0.2, 0.9, 0.12), at(box(0.04, 0.16, 0.04, W), 0.2, 0.9, 0.12));
    // the baby from behind: a round body in a romper, the bib ties, the bonnet
    const baby = grp(); baby.position.set(0, 0.82, 0.02); inner.add(baby);
    baby.add(ink(at(lump(0.14, 0.15, 0.12, o.romper || '#BFD8F2', 31, 0.05, 1), 0, 0.15, 0), 0.04));
    const head = grp(); head.position.set(0, 0.38, 0); baby.add(head);
    head.add(ink(at(sphere(0.13, '#F2C9A6', 1), 0, 0, 0), 0.04));
    const bon = new THREE.Mesh(new THREE.SphereGeometry(0.145, 16, 10, 0, TAU, 0, PI * 0.62), mat(C, { noGrain: true })); bon.rotation.x = -0.5; bon.position.set(0, 0.005, -0.01); ink(bon, 0.04); head.add(bon);
    const fr = new THREE.Mesh(new THREE.TorusGeometry(0.135, 0.022, 5, 18), mat('#FFFFFF', { noGrain: true })); fr.position.set(0, -0.02, 0.05); fr.rotation.x = 0.35; head.add(fr);
    for (const sd of [-1, 1]) head.add(at(box(0.05, 0.08, 0.02, C, { outline: 0.05 }), sd * 0.045, -0.06, -0.15, 0.3, 0, sd * 0.6));
    head.add(ink(at(sphere(0.03, C, 1), 0, -0.04, -0.15), 0.05));
    for (const sd of [-1, 1]) baby.add(at(box(0.012, 0.09, 0.012, '#FFFFFF', { noGrain: true }), sd * 0.03, 0.26, -0.11, 0.2, 0, sd * 0.4));
    // the arm and the spoon (on the baby's right: -X), banging on the tray
    const arm = grp(); arm.position.set(-0.13, 0.22, 0.02); baby.add(arm);
    arm.add(ink(at(box(0.05, 0.16, 0.05, o.romper || '#BFD8F2'), 0, 0.06, 0.04, -0.6, 0, 0), 0.05), at(sphere(0.035, '#F2C9A6', 1), 0, 0.12, 0.11));
    const spoon = grp(at(box(0.016, 0.16, 0.008, '#C9CED6', { noGrain: true, outline: 0.06 }), 0, 0.08, 0), at(sphere(0.03, '#C9CED6', 1), 0, 0.17, 0)); spoon.children[1].scale.set(1, 1.3, 0.4); spoon.position.set(0, 0.12, 0.11); arm.add(spoon);
    g.userData.update = t => {
      const b = inside(o.bang, t), ph = b >= 0 ? Math.max(0, Math.sin(b * TAU * (o.rate ?? 3.2))) : 0; arm.rotation.x = -1.2 * ph + 0.4; spoon.rotation.x = 0.3 * ph;
      head.rotation.z = 0.12 * Math.sin(t * 2.3 + (o.seed ?? 0)); head.rotation.x = b >= 0 ? 0.06 * ph : 0; head.position.y = 0.38;
      // (round 3) o.twos: the banging drawn on twos (held two frames, 15 drawings a second), a raise, a slam and a rest per beat, o.phase (s) offsets
      // the beat from chair to chair; the bonnet bobs on every hit (a dip and a nod)
      if (o.twos && b >= 0) { const tq = Math.floor((t + 1e-4) * 15) / 15, bq = inside(o.bang, tq), u = (((Math.max(0, bq) + (o.phase ?? 0)) * (o.rate ?? 3.2)) % 1 + 1) % 1;
        const up = u < 0.55 ? smooth(u / 0.55) : u < 0.7 ? 1 - (u - 0.55) / 0.15 : 0, bob = u >= 0.7 && u < 0.9 ? 1 - (u - 0.7) / 0.2 : 0;
        arm.rotation.x = -1.5 * up + 0.4; spoon.rotation.x = 0.35 * up; head.rotation.x = 0.28 * bob; head.position.y = 0.38 - 0.035 * bob; }
      // (round 1) the pop: shoots up stretched (2 frames), squashes flat on landing, overshoots tall, settles (a squash and an overshoot that read at phone size)
      if (o.pop !== undefined) { const u = t - o.pop, K = [[0, 0.05, 0.05], [0.07, 0.72, 1.32], [0.13, 1.28, 0.66], [0.21, 0.9, 1.14], [0.29, 1.05, 0.95], [0.37, 1, 1]];
        let sx = 1, sy = 1; if (u < 0) { sx = sy = 0.01; } else if (u < 0.37) { let i = 0; while (u > K[i + 1][0]) i++; const v = smooth((u - K[i][0]) / (K[i + 1][0] - K[i][0])); sx = lerp(K[i][1], K[i + 1][1], v); sy = lerp(K[i][2], K[i + 1][2], v); }
        inner.visible = u >= 0; inner.scale.set(Math.max(0.01, sx), Math.max(0.01, sy), Math.max(0.01, sx)); }
    };
    g.userData.update(0); return g;
  },

  // (round 3) o.shift may be keyed ([[t, v], ...]): the drawing slides along the paper (paper pulled through the hands by a roll running away)
  // ---------------------------------------------------------------- the family-tree scroll (pivot at its top edge, the paper in the local XY plane facing +Z, it
  // unrolls downward along -Y): o.w (0.7) wide, o.len [[t, L]] (or a number) unrolled length; o.head: the top shows mamie's portrait in a round frame
  // with the first branches; o.tail: the end shows a last bare branch (no face); o.roll: a paper roll at the bottom end that turns as it unrolls;
  // the body repeats a trunk with branches ending in small round faces (no text, no digits). Lay it flat with rot [-PI/2, 0, 0] (it then runs
  // along +Z, the drawing up); o.lift the roll's radius is added under it
  seScroll(o) {
    const W = o.w ?? 0.7, g = grp(), PAPER = '#F4EAD0', BR = '#7A5230', TILE = W * 1.4;
    const faceDot = (c, x, y, r, hair, k) => { c.fillStyle = '#F2C9A6'; c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill(); c.lineWidth = r * 0.18; c.strokeStyle = '#3A2A20'; c.stroke();
      c.fillStyle = hair; c.beginPath(); c.arc(x, y - r * 0.15, r * 1.02, PI * 1.05, PI * 1.95); c.fill();
      c.fillStyle = '#2A1E18'; c.beginPath(); c.arc(x - r * 0.33, y + r * 0.05, r * 0.11, 0, TAU); c.arc(x + r * 0.33, y + r * 0.05, r * 0.11, 0, TAU); c.fill();
      c.beginPath(); c.lineWidth = r * 0.14; c.arc(x, y + r * 0.2, r * 0.38, 0.2 + k * 0.1, PI - 0.2 - k * 0.1); c.stroke(); };
    const HAIR = ['#3A2A20', '#8A5A2A', '#D8B060', '#1E1A18', '#B04A2A', '#6A6A6A'];
    const border = (c, Wc, Hc) => { c.fillStyle = PAPER; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#E6D6B0'; c.fillRect(0, 0, Wc * 0.04, Hc); c.fillRect(Wc * 0.96, 0, Wc * 0.04, Hc); c.strokeStyle = '#A8865A'; c.lineWidth = Wc * 0.008; c.beginPath(); c.moveTo(Wc * 0.06, 0); c.lineTo(Wc * 0.06, Hc); c.moveTo(Wc * 0.94, 0); c.lineTo(Wc * 0.94, Hc); c.stroke(); };
    const branchTile = (c, Wc, Hc, seed) => { border(c, Wc, Hc); c.strokeStyle = BR; c.lineCap = 'round';
      c.lineWidth = Wc * 0.05; c.beginPath(); c.moveTo(Wc / 2, 0); c.lineTo(Wc / 2, Hc); c.stroke();
      for (let i = 0; i < 4; i++) { const y = Hc * (0.14 + i * 0.24), sd = i % 2 ? 1 : -1; c.lineWidth = Wc * 0.025; c.beginPath(); c.moveTo(Wc / 2, y + Hc * 0.06); c.quadraticCurveTo(Wc / 2 + sd * Wc * 0.18, y + Hc * 0.04, Wc / 2 + sd * Wc * 0.3, y - Hc * 0.02); c.stroke();
        c.lineWidth = Wc * 0.015; c.beginPath(); c.moveTo(Wc / 2 + sd * Wc * 0.16, y + Hc * 0.035); c.lineTo(Wc / 2 + sd * Wc * 0.2, y - Hc * 0.06); c.stroke();
        faceDot(c, Wc / 2 + sd * Wc * 0.33, y - Hc * 0.04, Wc * 0.07, HAIR[(i + seed) % HAIR.length], i % 3); faceDot(c, Wc / 2 + sd * Wc * 0.2, y - Hc * 0.085, Wc * 0.055, HAIR[(i * 2 + seed + 1) % HAIR.length], (i + 1) % 3);
        c.fillStyle = '#6E9A4A'; for (let j = 0; j < 3; j++) { c.beginPath(); c.ellipse(Wc / 2 + sd * Wc * (0.08 + j * 0.07), y + Hc * 0.05 - j * Hc * 0.01, Wc * 0.025, Wc * 0.012, sd * 0.6, 0, TAU); c.fill(); } } };
    const RES = 256, RH = Math.round(RES * TILE / W);
    const bodyCv = canvas(RES, RH); branchTile(bodyCv.getContext('2d'), RES, RH, o.seed ?? 0);
    const bodyTex = tex(bodyCv); bodyTex.wrapS = THREE.ClampToEdgeWrapping; bodyTex.wrapT = THREE.RepeatWrapping;
    const bodyMat = L('#FFFFFF', { map: bodyTex, emissive: '#FFFFFF', emissiveMap: bodyTex, emissiveIntensity: 0.22, side: THREE.DoubleSide, ...OFF });
    const body = new THREE.Mesh(new THREE.PlaneGeometry(W, 1).translate(0, -0.5, 0), bodyMat); body.receiveShadow = true; g.add(body);
    let headH = 0; if (o.head) { headH = W * 1.25;
      const hp = paintPlane(W, headH, (c, Wc, Hc) => { border(c, Wc, Hc); c.strokeStyle = BR; c.lineCap = 'round'; c.lineWidth = Wc * 0.05; c.beginPath(); c.moveTo(Wc / 2, Hc * 0.6); c.lineTo(Wc / 2, Hc); c.stroke();
        c.lineWidth = Wc * 0.03; for (const sd of [-1, 1]) { c.beginPath(); c.moveTo(Wc / 2, Hc * 0.78); c.quadraticCurveTo(Wc / 2 + sd * Wc * 0.22, Hc * 0.8, Wc / 2 + sd * Wc * 0.32, Hc * 0.92); c.stroke(); }
        const x = Wc / 2, y = Hc * 0.36, r = Wc * 0.27;
        c.fillStyle = '#C9A0D8'; c.beginPath(); c.arc(x, y, r * 1.22, 0, TAU); c.fill(); c.strokeStyle = '#B58A3A'; c.lineWidth = Wc * 0.03; c.stroke();
        c.fillStyle = '#F2C9A6'; c.beginPath(); c.arc(x, y + r * 0.08, r * 0.78, 0, TAU); c.fill(); c.strokeStyle = '#3A2A20'; c.lineWidth = Wc * 0.012; c.stroke();
        c.fillStyle = '#F4F4F4'; c.beginPath(); c.arc(x, y - r * 0.75, r * 0.38, 0, TAU); c.fill(); c.stroke(); c.beginPath(); c.arc(x, y - r * 0.25, r * 0.8, PI * 1.08, PI * 1.92); c.fill(); c.stroke();
        c.lineWidth = Wc * 0.014; for (const sd of [-1, 1]) { c.beginPath(); c.arc(x + sd * r * 0.3, y + r * 0.05, r * 0.2, 0, TAU); c.stroke(); } c.beginPath(); c.moveTo(x - r * 0.1, y + r * 0.05); c.lineTo(x + r * 0.1, y + r * 0.05); c.stroke();
        c.fillStyle = '#2A1E18'; for (const sd of [-1, 1]) { c.beginPath(); c.arc(x + sd * r * 0.3, y + r * 0.07, r * 0.06, 0, TAU); c.fill(); }
        c.beginPath(); c.lineWidth = Wc * 0.016; c.arc(x, y + r * 0.32, r * 0.25, 0.25, PI - 0.25); c.stroke();
        c.fillStyle = '#E88A8A'; for (const sd of [-1, 1]) { c.beginPath(); c.arc(x + sd * r * 0.5, y + r * 0.35, r * 0.1, 0, TAU); c.fill(); } }, { res: RES, emissive: 0.22, double: true, offset: true });
      hp.position.y = -headH / 2; g.add(hp); }
    let tailH = 0; const tail = o.tail ? paintPlane(W, W * 0.9, (c, Wc, Hc) => { border(c, Wc, Hc); c.strokeStyle = BR; c.lineCap = 'round'; c.lineWidth = Wc * 0.05; c.beginPath(); c.moveTo(Wc / 2, 0); c.lineTo(Wc / 2, Hc * 0.55); c.stroke();
      c.lineWidth = Wc * 0.025; c.beginPath(); c.moveTo(Wc / 2, Hc * 0.45); c.quadraticCurveTo(Wc / 2 + Wc * 0.15, Hc * 0.42, Wc / 2 + Wc * 0.26, Hc * 0.3); c.stroke();
      c.lineWidth = Wc * 0.012; c.beginPath(); c.moveTo(Wc / 2 + Wc * 0.26, Hc * 0.3); c.lineTo(Wc / 2 + Wc * 0.3, Hc * 0.22); c.moveTo(Wc / 2 + Wc * 0.26, Hc * 0.3); c.lineTo(Wc / 2 + Wc * 0.34, Hc * 0.31); c.stroke();
      if (o.empty) { c.lineWidth = Wc * 0.022; c.setLineDash([Wc * 0.035, Wc * 0.03]); c.beginPath(); c.arc(Wc / 2 + Wc * 0.3, Hc * 0.16, Wc * 0.1, 0, TAU); c.stroke(); c.setLineDash([]);
        c.lineWidth = Wc * 0.03; c.beginPath(); c.moveTo(Wc / 2, Hc * 0.62); c.quadraticCurveTo(Wc / 2 - Wc * 0.15, Hc * 0.6, Wc / 2 - Wc * 0.22, Hc * 0.5); c.stroke();
        c.setLineDash([Wc * 0.03, Wc * 0.03]); c.lineWidth = Wc * 0.018; c.beginPath(); c.arc(Wc / 2 - Wc * 0.25, Hc * 0.38, Wc * 0.08, 0, TAU); c.stroke(); c.setLineDash([]); }
      c.fillStyle = '#E6D6B0'; c.fillRect(Wc * 0.06, Hc * 0.92, Wc * 0.88, Hc * 0.08); }, { res: RES, emissive: 0.22, double: true, offset: true }) : null;
    if (tail) { tailH = W * 0.9; g.add(tail); }
    const R0 = o.rollR ?? 0.07, roll = o.roll ? grp() : null;
    if (roll) { const rc = cyl(R0, R0, W * 1.02, PAPER, 18, { noGrain: true }); rc.material = L(PAPER, { emissive: '#3A2E1E', emissiveIntensity: 0.2 }); rc.rotation.z = PI / 2; ink(rc, 0.03); roll.add(rc);
      for (const sd of [-1, 1]) { const end = new THREE.Mesh(new THREE.RingGeometry(R0 * 0.2, R0 * 0.98, 18), new THREE.MeshBasicMaterial({ color: '#C8B48A', side: THREE.DoubleSide })); end.rotation.y = PI / 2; end.position.x = sd * W * 0.512; roll.add(end);
        for (let k = 1; k < 4; k++) { const sp = new THREE.Mesh(new THREE.RingGeometry(R0 * (0.2 + k * 0.2), R0 * (0.2 + k * 0.2) + 0.004, 18), new THREE.MeshBasicMaterial({ color: '#8A7050', side: THREE.DoubleSide })); sp.rotation.y = PI / 2; sp.position.x = sd * W * 0.514; roll.add(sp); } }
      g.add(roll); }
    g.userData.update = t => {
      const Lb = Math.max(0.001, keyAt(o.len, t, 1)); body.scale.y = Lb; body.position.y = -headH;
      bodyTex.repeat.set(1, Lb / TILE); bodyTex.offset.set(0, 1 - Lb / TILE + keyAt(o.shift, t, 0));
      if (tail) tail.position.y = -headH - Lb - tailH / 2;
      if (roll) { roll.position.set(0, -headH - Lb - tailH - R0 * 0.3, R0); roll.rotation.x = -Lb / R0; }
    };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a market awning over a table (pivot at the floor under its middle): four thin poles, a striped
  // canopy (two colours, o.c1 / o.c2) with a scalloped valance at the front; o.w (1.8) along X, o.d (1.3), o.h (2.55)
  seAwning(o) {
    const W = o.w ?? 1.8, D = o.d ?? 1.3, H = o.h ?? 2.55, g = grp(), C1 = o.c1 || '#3E8A5A', C2 = o.c2 || '#F4EEDC';
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(at(cyl(0.022, 0.022, H, '#5A4030', 6, { pivot: 'bottom' }), sx * W / 2, 0, sz * D / 2));
    const n = 8, cv = paintPlane(W, D * 1.05, (c, Wc, Hc) => { for (let i = 0; i < n; i++) { c.fillStyle = i % 2 ? C2 : C1; c.fillRect(i * Wc / n, 0, Wc / n + 1, Hc); } }, { res: 256, emissive: 0.2, double: true });
    cv.rotation.x = -PI / 2 + 0.22; cv.position.set(0, H + 0.05, 0); g.add(cv);
    const val = paintPlane(W, 0.24, (c, Wc, Hc) => { for (let i = 0; i < n; i++) { c.fillStyle = i % 2 ? C2 : C1; c.beginPath(); c.moveTo(i * Wc / n, 0); c.lineTo((i + 1) * Wc / n, 0); c.lineTo((i + 1) * Wc / n, Hc * 0.55); c.arc((i + 0.5) * Wc / n, Hc * 0.55, Wc / n / 2, 0, PI); c.closePath(); c.fill(); } }, { res: 256, emissive: 0.2, double: true });
    val.position.set(0, H - 0.07 - D / 2 * Math.sin(0.22), D / 2 * Math.cos(0.22) + 0.01); g.add(val);
    const back = val.clone(); back.position.z = -back.position.z + 0.02; back.position.y = H + 0.17; g.add(back);
    return g;
  },

  // ---------------------------------------------------------------- a slatted wooden crate of leeks (pivot at its base): long leeks (white, pale green, dark green
  // fans) sticking out at an angle; o.n (7)
  seLeekCrate(o) {
    const g = grp(), W = o.w ?? 0.42, D = o.d ?? 0.3, H = 0.18, WD = '#C89A5E';
    for (let i = 0; i < 3; i++) for (const sd of [-1, 1]) { g.add(at(box(W, 0.045, 0.012, WD, { outline: 0.02 }), 0, 0.03 + i * 0.06, sd * D / 2), at(box(0.012, 0.045, D, WD, { outline: 0.02 }), sd * W / 2, 0.03 + i * 0.06, 0)); }
    g.add(at(box(W, 0.012, D, '#A8783E'), 0, 0.008, 0));
    for (let i = 0; i < (o.n ?? 7); i++) g.add(leekMesh(0.42 + hsh(i) * 0.08, i, (i - 3) * 0.05, 0.05 + (i % 2) * 0.04, (hsh(i * 3) - 0.5) * 0.12, 0.9 + hsh(i * 9) * 0.3));
    return g;
  },
  // one leek (pivot at its root end, along +X, lifted): o.len (0.5)
  seLeek(o) { const g = grp(leekMesh(o.len ?? 0.5, o.seed ?? 1, 0, 0, 0, 0)); return g; },

  // ---------------------------------------------------------------- a fruit bowl topped with one big pear (pivot at its base); o.pearS (1.6) the pear's size
  seFruitBowl(o) {
    const g = grp(), bw = cyl(0.17, 0.09, 0.09, '#F2E6D2', 20, { pivot: 'bottom', noGrain: true }); ink(bw, 0.03); g.add(bw);
    [[-0.07, 0.0, '#D42A36'], [0.07, 0.02, '#F29A2A'], [0.0, -0.07, '#E8D04A'], [0.02, 0.08, '#D42A36']].forEach(([x, z, c], i) => { const f = lump(0.055, 0.055, 0.055, c, 41 + i, 0.05, 1); f.position.set(x, 0.12, z); ink(f, 0.04); g.add(f); });
    const ps = o.pearS ?? 1.6, pear = grp(); pear.position.set(0, 0.16, 0); pear.scale.setScalar(ps); g.add(pear);
    const pb = new THREE.LatheGeometry([[0, 0], [0.05, 0.005], [0.068, 0.04], [0.06, 0.08], [0.036, 0.11], [0.03, 0.14], [0.018, 0.165], [0, 0.17]].map(([x, y]) => new THREE.Vector2(x, y)), 14);
    const pm = new THREE.Mesh(pb, mat('#B7C94A', { emissive: '#3A4A0A' })); pm.castShadow = true; ink(pm, 0.04); pear.add(pm);
    pear.add(at(cyl(0.005, 0.006, 0.05, '#5A3A1E', 5), 0.004, 0.19, 0, 0, 0, -0.2)); const lf = lump(0.03, 0.006, 0.015, '#4E9A3E', 5, 0.05, 0); lf.position.set(0.022, 0.2, 0); lf.rotation.z = -0.5; pear.add(lf);
    return g;
  },

  // ---------------------------------------------------------------- a cheese board (pivot at its base): a round wooden board, a wheel of cheese with a wedge cut
  // out, the wedge beside it, a small wedge of blue
  seCheese(o) {
    const g = grp(), bd = cyl(0.2, 0.2, 0.025, '#B8834A', 20, { pivot: 'bottom' }); ink(bd, 0.03); g.add(bd);
    const wheel = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.075, 24, 1, false, 0.5, TAU - 0.9), mat('#F2D27A', { emissive: '#4A3A0A' })); wheel.position.y = 0.025 + 0.0375; ink(wheel, 0.04); g.add(wheel);
    const rind = new THREE.Mesh(new THREE.CylinderGeometry(0.123, 0.123, 0.077, 24, 1, true, 0.5, TAU - 0.9), mat('#E8B24A', { doubleSide: true })); rind.position.y = wheel.position.y; g.add(rind);
    const wsh = new THREE.Shape(); wsh.moveTo(0, 0); wsh.lineTo(0.11, -0.035); wsh.lineTo(0.11, 0.035); wsh.closePath();
    const wedge = new THREE.Mesh(new THREE.ExtrudeGeometry(wsh, { depth: 0.07, bevelEnabled: false }), mat('#F2D27A', { emissive: '#4A3A0A' })); wedge.rotation.x = -PI / 2; wedge.position.set(0.04, 0.025, 0.12); wedge.rotation.z = 0.6; ink(wedge, 0.05); g.add(wedge);
    return g;
  },

  // ---------------------------------------------------------------- a radish (pivot at its middle): a round red root, a white tip, a fan of leaves; o.s (1.4)
  seRadish(o) {
    const s = o.s ?? 1.4, g = grp(), r = lump(0.03 * s, 0.032 * s, 0.03 * s, '#D82A4A', 3, 0.05, 1, { emissive: '#4A0A1A' }); ink(r, 0.06); g.add(r);
    g.add(at(cyl(0.003 * s, 0.012 * s, 0.03 * s, '#F4ECEC', 5), 0, -0.042 * s, 0));
    for (let i = 0; i < 4; i++) { const lf = lump(0.012 * s, 0.035 * s, 0.006 * s, '#4E9A3E', 7 + i, 0.08, 0); lf.position.set((i - 1.5) * 0.008 * s, 0.055 * s, 0); lf.rotation.z = (i - 1.5) * 0.35; g.add(lf); }
    return g;
  },

  // ---------------------------------------------------------------- a scarecrow sitting at a place (pivot at the floor under the seat, he faces +Z), seat at 0.48:
  // a sack head with a stitched face, a straw hat, a two-tone shirt, straw tufts at the neck and wrists, his arms on the table, a napkin tucked in;
  // o.nod [[t0, t1]]: his head lolls in the wind
  seScarecrow(o) {
    const g = grp(), chair = chairMesh('#6A4430', '#C89A5E'); g.add(chair);
    const body = grp(); body.position.y = 0.5; g.add(body);
    body.add(ink(at(box(0.44, 0.5, 0.26, '#C9483A', { pivot: 'bottom', taper: { x: 0.9, z: 1 } }), 0, 0.02, -0.02), 0.025));
    body.add(at(box(0.12, 0.12, 0.01, '#3E6A9A'), -0.1, 0.32, 0.115), at(box(0.1, 0.1, 0.01, '#E8C25A'), 0.11, 0.18, 0.115));
    for (const sd of [-1, 1]) { body.add(ink(at(box(0.16, 0.12, 0.42, '#5A6E8A'), sd * 0.12, 0.03, 0.18), 0.03), ink(at(box(0.14, 0.42, 0.12, '#5A6E8A', { pivot: 'top' }), sd * 0.12, 0.03, 0.36), 0.03));
      body.add(ink(at(box(0.11, 0.11, 0.36, '#C9483A'), sd * 0.27, 0.36, 0.2, -0.25, 0, 0), 0.03));
      for (let i = 0; i < 3; i++) body.add(at(box(0.02, 0.02, 0.1, '#E8C25A'), sd * 0.27 + (i - 1) * 0.025, 0.31, 0.42, (i - 1) * 0.3, (i - 1) * 0.3, 0)); }
    const head = grp(); head.position.set(0, 0.58, 0); body.add(head);
    for (let i = 0; i < 5; i++) head.add(at(box(0.02, 0.1, 0.02, '#E8C25A'), (i - 2) * 0.04, -0.02, 0.06, 0, 0, (i - 2) * 0.3));
    const sack = lump(0.16, 0.17, 0.15, '#D8C08A', 17, 0.06, 1); sack.position.y = 0.16; ink(sack, 0.03); head.add(sack);
    const face = paintPlane(0.22, 0.2, (c, Wc, Hc) => { c.clearRect(0, 0, Wc, Hc); c.fillStyle = '#D8C08A'; c.fillRect(0, 0, Wc, Hc); c.strokeStyle = '#2A1E18'; c.lineWidth = Wc * 0.04;
      for (const x of [0.3, 0.7]) { c.beginPath(); c.moveTo(Wc * (x - 0.08), Hc * 0.32); c.lineTo(Wc * (x + 0.08), Hc * 0.46); c.moveTo(Wc * (x + 0.08), Hc * 0.32); c.lineTo(Wc * (x - 0.08), Hc * 0.46); c.stroke(); }
      c.beginPath(); c.moveTo(Wc * 0.25, Hc * 0.7); for (let i = 0; i <= 6; i++) c.lineTo(Wc * (0.25 + i * 0.083), Hc * (0.7 + (i % 2 ? 0.05 : 0))); c.stroke(); }, { res: 128, emissive: 0.2 });
    face.position.set(0, 0.16, 0.15); head.add(face);
    head.add(ink(at(cyl(0.3, 0.3, 0.025, '#E8C25A', 14), 0, 0.31, 0), 0.03), ink(at(cyl(0.14, 0.17, 0.14, '#E8C25A', 10, { pivot: 'bottom' }), 0, 0.32, 0), 0.03), at(cyl(0.172, 0.172, 0.035, '#C9483A', 10), 0, 0.35, 0));
    const nap = SEL_PROPS.seBib({ s: 0.8 }); nap.position.set(0, 0.5, 0.145); body.add(nap);
    g.userData.update = t => { const n = inside(o.nod, t); head.rotation.z = (n >= 0 ? (o.loll ?? 0.18) * Math.min(1, n / 0.15) : 0.06) * Math.sin(t * (n >= 0 ? 6 : 2)); head.rotation.x = 0.05 * Math.sin(t * 3.1); head.rotation.y = keyAt(o.turn, t, 0);
      for (const [nap_, k_] of [[nap, 1]]) nap_.rotation.x = n >= 0 ? -0.5 * k_ * (0.6 + 0.4 * Math.sin(t * 17)) : 0; };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a rolling blackboard (pivot at the floor under its middle, the board faces +Z): an A-frame on
  // casters, a dark green board in a wooden frame, a chalk tray; the chalk drawing appears as it is drawn (o.draw [[t, 0..1]]): a salt shaker on the
  // left, a table on the right, a long arrow from the shaker that loops back on itself again and again and never reaches the table (shapes only, no
  // letters, no digits); o.shudder [t...]: the board wobbles on its pivots
  seBoard(o) {
    const W = o.w ?? 1.7, H = o.h ?? 1.15, Y = o.y ?? 1.55, g = grp(), FR = '#8A5A34';
    for (const sd of [-1, 1]) { g.add(at(box(0.05, Y + H / 2 + 0.1, 0.05, FR, { pivot: 'bottom', outline: 0.02 }), sd * (W / 2 + 0.05), 0.08, 0), at(box(0.06, 0.05, 0.6, FR), sd * (W / 2 + 0.05), 0.1, 0));
      for (const z of [-0.27, 0.27]) g.add(ink(at(sphere(0.045, '#2A2A2E', 1), sd * (W / 2 + 0.05), 0.045, z), 0.05)); }
    const piv = grp(); piv.position.y = Y; g.add(piv);
    piv.add(at(box(W + 0.08, H + 0.08, 0.05, FR, { outline: 0.012 }), 0, 0, -0.03));
    // the drawing: a list of strokes, each a polyline in board units (0..1 across, 0..1 down); drawn up to a share of their total length
    const S = [], add = (pts, wdt = 1) => S.push({ pts, wdt });
    add([[0.1, 0.62], [0.1, 0.38], [0.12, 0.34], [0.22, 0.34], [0.24, 0.38], [0.24, 0.62], [0.1, 0.62]]);
    add([[0.11, 0.34], [0.12, 0.28], [0.17, 0.25], [0.22, 0.28], [0.23, 0.34]]);
    add([[0.14, 0.28], [0.145, 0.28]], 2.5); add([[0.17, 0.27], [0.175, 0.27]], 2.5); add([[0.2, 0.28], [0.205, 0.28]], 2.5);
    add([[0.72, 0.5], [0.94, 0.5]], 1.5); add([[0.74, 0.5], [0.74, 0.7]]); add([[0.92, 0.5], [0.92, 0.7]]); add([[0.72, 0.47], [0.94, 0.47]], 0.8);
    const loop = []; let x = 0.27, y = 0.5;
    for (let i = 0; i <= 160; i++) { const u = i / 160, a = u * TAU * 4.2; loop.push([0.27 + u * 0.36 + 0.05 * Math.sin(a), 0.5 - 0.11 * Math.sin(a * 0.5) * Math.sin(a) - 0.06 * (1 - Math.cos(a))]); }
    loop.push([0.6, 0.62], [0.42, 0.74], [0.3, 0.68]); add(loop, 1.1);
    add([[0.27, 0.64], [0.3, 0.68], [0.33, 0.63]], 1.1);
    const segLen = S.map(s => { let l = 0; for (let i = 1; i < s.pts.length; i++) l += Math.hypot(s.pts[i][0] - s.pts[i - 1][0], s.pts[i][1] - s.pts[i - 1][1]); return Math.max(l, 0.01); }), total = segLen.reduce((a, b) => a + b, 0);
    const RES = 512, cv = canvas(RES, Math.round(RES * H / W)), c = cv.getContext('2d'), tx = tex(cv);
    let last = -1;
    const draw = v => { const Wc = cv.width, Hc = cv.height; c.fillStyle = '#24352E'; c.fillRect(0, 0, Wc, Hc);
      c.fillStyle = 'rgba(255,255,255,0.05)'; for (let i = 0; i < 9; i++) { c.beginPath(); c.ellipse(Wc * hsh(i), Hc * hsh(i + 9), Wc * 0.12, Hc * 0.05, hsh(i + 3), 0, TAU); c.fill(); }
      c.strokeStyle = '#F4F2EA'; c.lineCap = 'round'; c.lineJoin = 'round'; let left = v * total;
      for (let k = 0; k < S.length && left > 0; k++) { const s = S[k]; c.lineWidth = Wc * 0.012 * s.wdt; c.beginPath(); c.moveTo(s.pts[0][0] * Wc, s.pts[0][1] * Hc);
        for (let i = 1; i < s.pts.length && left > 0; i++) { const a = s.pts[i - 1], b = s.pts[i], d = Math.hypot(b[0] - a[0], b[1] - a[1]); if (d <= left) { c.lineTo(b[0] * Wc, b[1] * Hc); left -= d; } else { const u = left / d; c.lineTo((a[0] + (b[0] - a[0]) * u) * Wc, (a[1] + (b[1] - a[1]) * u) * Hc); left = 0; } }
        c.stroke(); }
      tx.needsUpdate = true; };
    draw(0);
    const face = new THREE.Mesh(new THREE.PlaneGeometry(W, H), L('#FFFFFF', { map: tx, emissive: '#FFFFFF', emissiveMap: tx, emissiveIntensity: 0.35 })); face.position.z = 0.0; face.receiveShadow = true; piv.add(face);
    piv.add(at(box(W * 0.9, 0.03, 0.08, FR), 0, -H / 2 - 0.02, 0.04), at(box(0.07, 0.018, 0.018, '#FFFFFF', { noGrain: true }), W * 0.3, -H / 2 + 0.005, 0.05), at(box(0.06, 0.018, 0.018, '#F2E27A', { noGrain: true }), W * 0.36, -H / 2 + 0.005, 0.05));
    g.userData.update = t => { const v = Math.round(clamp01(keyAt(o.draw, t, 1)) * 200) / 200; if (v !== last) { last = v; draw(v); } piv.rotation.x = rattle((o.shudder || []).map(s => [s, 0.06, 26, 6]), t); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- steam out of both ears like a kettle (attach to the head joint: offsets in its frame, the head
  // 0.5 high from the chin): opaque white lobed puffs with an ink rim that leave the ears thin and fast, swell, rise and shrink to nothing (never a
  // fade: a translucent cloud over a face reads as a ghost); o.on [[t0, t1]] (default always), o.rate (2.6 puffs a second per ear), o.ear [x, y]
  // (0.16, 0.27), o.s (1) their size
  seSteam(o) {
    const g = grp(), N = 4, E = o.ear || [0.16, 0.27], S = o.s ?? 1, P_ = [];
    for (const sd of [-1, 1]) for (let i = 0; i < N; i++) { const pf = grp(); for (let j = 0; j < 3; j++) { const m = lump(1, 1, 1, '#FFFFFF', 61 + i * 3 + j + (sd > 0 ? 20 : 0), 0.1, 1, { emissive: '#8A949E', noGrain: true }); ink(m, 0.12); m.castShadow = m.receiveShadow = false;
        m.position.set((j - 1) * 0.55, j === 1 ? 0.35 : 0, (j - 1) * 0.1); m.scale.setScalar(j === 1 ? 0.75 : 0.6); pf.add(m); } g.add(pf); P_.push({ pf, sd, i }); }
    // (round 2) o.pop: each puff squash-pops out of the ear (an overshoot to 1.4, a squash, a settle) instead of swelling smoothly; o.burst [t, ...]:
    // a big puff on each side pops at that time (a whistle), squashes, rises and shrinks to nothing in 0.7 s
    const popK = u => u < 0.1 ? 1.4 * u / 0.1 : u < 0.18 ? 1.4 - 0.55 * (u - 0.1) / 0.08 : u < 0.26 ? 0.85 + 0.2 * (u - 0.18) / 0.08 : 1.05;
    const popSq = u => (u >= 0.1 && u < 0.18) ? 1 - 0.3 * Math.sin(PI * (u - 0.1) / 0.08) : 1;
    const B_ = []; for (const tb of o.burst || []) for (const sd of [-1, 1]) { const pf = grp(); for (let j = 0; j < 3; j++) { const m = lump(1, 1, 1, '#FFFFFF', 91 + j + (sd > 0 ? 7 : 0) + B_.length, 0.1, 1, { emissive: '#8A949E', noGrain: true }); ink(m, 0.12); m.castShadow = m.receiveShadow = false;
        m.position.set((j - 1) * 0.55, j === 1 ? 0.35 : 0, (j - 1) * 0.1); m.scale.setScalar(j === 1 ? 0.75 : 0.6); pf.add(m); } pf.visible = false; g.add(pf); B_.push({ pf, sd, tb }); }
    g.userData.update = t => { const on = !o.on || inside(o.on, t) >= 0, rate = o.rate ?? 2.6;
      for (const { pf, sd, i } of P_) { const q = ((t * rate / N) + i / N + (sd > 0 ? 0.13 : 0)) % 1; pf.visible = on; if (!on) continue;
        const grow = o.pop ? popK(q / 1.0) : Math.min(1, q / 0.35), shrink = q < 0.6 ? 1 : Math.max(0, 1 - (q - 0.6) / 0.4), sz = S * 0.045 * (o.pop ? 1.3 * grow : 0.35 + 1.3 * grow) * shrink;
        pf.position.set(sd * (E[0] + 0.05 * S + q * 0.2 * S), E[1] + q * 0.32 * S, 0.0); pf.scale.setScalar(Math.max(0.0005, sz)); if (o.pop) { const k_ = popSq(q); pf.scale.x *= 2 - k_; pf.scale.y *= k_; }
        pf.rotation.z = sd * q * 1.2; pf.visible = sz > 0.001; }
      for (const { pf, sd, tb } of B_) { const u = (t - tb) / 0.7; pf.visible = u >= 0 && u < 1; if (!pf.visible) continue;
        const sz = S * 0.085 * popK(u) * (u < 0.55 ? 1 : Math.max(0, 1 - (u - 0.55) / 0.45)), k_ = popSq(u);
        pf.position.set(sd * (E[0] + 0.08 * S + u * 0.16 * S), E[1] + 0.03 + u * 0.3 * S, 0.0); pf.scale.set(Math.max(0.0005, sz * (2 - k_)), Math.max(0.0005, sz * k_), Math.max(0.0005, sz)); pf.rotation.z = sd * u * 0.8; } };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a big wooden pepper mill (pivot at its base): a turned dark wood body with pale rings, a
  // knob on top; o.h (0.4)
  seMill(o) {
    const Hh = o.h ?? 0.4, g = grp(), prof = [[0, 0], [0.06, 0], [0.065, 0.02], [0.05, 0.05], [0.042, 0.14], [0.058, 0.26], [0.06, 0.32], [0.045, 0.36], [0.05, 0.4], [0.035, 0.43], [0, 0.44]];
    // (round 2) o.color / o.ring / o.knob: a mill that stands out from the dark wood around it (black lacquer and brass on a pale cloth)
    const geo = new THREE.LatheGeometry(prof.map(([x, y]) => new THREE.Vector2(x * Hh / 0.44 * 1.15, y * Hh / 0.44)), 18), m = new THREE.Mesh(geo, mat(o.color || '#6A3A22', { emissive: o.glow || '#1A0A04' })); m.castShadow = true; ink(m, o.inkW ?? 0.04); g.add(m);
    for (const y of [0.05, 0.31, 0.36]) g.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.05 * Hh / 0.44 * 1.15, o.ringW ? o.ringW * Hh / 0.44 : 0.006, 4, 18), mat(o.ring || '#E2B95A', { noGrain: true })), 0, y * Hh / 0.44, 0, PI / 2));
    g.add(ink(at(sphere(0.026 * Hh / 0.44 * 1.3, o.knob || '#3A1E10', 1), 0, Hh + 0.012, 0), 0.06));
    g.userData.grip = [0, Hh * 0.45, 0]; return g;
  },

  // ---------------------------------------------------------------- a lorry with no marking at all (pivot at the floor under the middle of its cab, front +Z):
  // a hollow cab (its side windows open: a driver seated inside shows through, his elbow on the sill), a plain cream box body behind, round
  // headlights, a dark grille, black bumper with no plate, big wheels; o.color the cab
  seLorry(o) {
    const C = o.color || '#3E7AB8', g = grp(), D = '#2A2D33';
    const shell = (w, h, d, x, y, z, c = C) => g.add(at(box(w, h, d, c, { pivot: 'bottom', outline: 0.01 }), x, y, z));
    shell(2.3, 0.6, 1.9, 0, 0.55, 0);
    shell(2.3, 0.18, 1.9, 0, 2.25, 0);
    shell(2.3, 1.1, 0.12, 0, 1.15, -0.89);
    for (const sd of [-1, 1]) { shell(0.1, 0.5, 1.9, sd * 1.1, 1.15, 0); shell(0.1, 0.62, 0.14, sd * 1.1, 1.63, 0.88); shell(0.1, 0.62, 0.14, sd * 1.1, 1.63, -0.88); }
    shell(2.3, 0.25, 0.12, 0, 1.15, 0.89);
    for (const sd of [-1, 1]) shell(0.14, 0.62, 0.12, sd * 1.08, 1.4, 0.89);
    const ws = box(2.04, 0.84, 0.03, '#BFE0EE', { noGrain: true }); ws.material = L('#BFE0EE', { emissive: '#3A6A7A', emissiveIntensity: 0.35 }); ws.position.set(0, 1.83, 0.92); ws.rotation.x = -0.08; ink(ws, 0.01); g.add(ws);
    g.add(at(box(2.1, 1.0, 0.02, '#3A3530'), 0, 1.65, -0.81));
    const seat = box(0.6, 0.12, 0.55, '#2E3238'); seat.position.set(o.seatX ?? 0.55, 1.15, -0.25); g.add(seat);
    g.add(at(box(0.04, 0.4, 0.04, '#222'), 0.55, 1.2, 0.45, 0.6, 0, 0), at(new THREE.Mesh(new THREE.TorusGeometry(0.2, 0.025, 5, 16), mat('#22252A')), 0.55, 1.42, 0.55, -0.9, 0, 0));
    g.add(at(box(2.1, 0.5, 0.06, D, { outline: 0.008 }), 0, 0.82, 0.96));
    for (let i = 0; i < 4; i++) g.add(at(box(1.9, 0.04, 0.04, '#B8BEC4', { noGrain: true }), 0, 0.66 + i * 0.11, 0.99));
    g.add(at(box(2.36, 0.24, 0.2, '#1C1E22', { outline: 0.008 }), 0, 0.45, 1.0));
    for (const sd of [-1, 1]) { const hl = cyl(0.14, 0.14, 0.05, '#FFF3C2', 14); hl.rotation.x = PI / 2; hl.position.set(sd * 0.85, 0.85, 1.0); hl.material = new THREE.MeshBasicMaterial({ color: '#FFF6D6' }); ink(hl, 0.08); g.add(hl);
      if (o.mirrors !== false) g.add(at(box(0.05, 0.05, 0.45, D), sd * 1.28, 1.95, 0.7), at(box(0.06, 0.34, 0.2, D, { outline: 0.006 }), sd * 1.42, 1.85, 0.62)); }
    g.add(at(box(2.5, 2.8, 4.6, o.box || '#EDE8DC', { pivot: 'bottom', outline: 0.012 }), 0, 0.6, -3.35));
    g.add(at(box(2.2, 0.24, 6.4, '#3C3F44'), 0, 0.42, -2.3));
    for (const z of [0.25, -3.4, -4.6]) for (const sd of [-1, 1]) { const w = cyl(0.5, 0.5, 0.36, '#22252A', 16); w.rotation.z = PI / 2; w.position.set(sd * 1.08, 0.5, z); g.add(w); g.add(at(cyl(0.22, 0.22, 0.38, '#9AA0A8', 10), sd * 1.08, 0.5, z, 0, 0, PI / 2)); }
    g.userData.seat = [o.seatX ?? 0.55, 1.21, -0.25]; return g;
  },

  // ---------------------------------------------------------------- the family dining room (pivot at the floor; the table runs along X at z 0): pale sage
  // wallpaper with a small motif above a wooden wainscot, a parquet floor (raised with a polygon offset over the void's floor), a sideboard and a
  // framed landscape on the back wall (z o.back, -2.6), a window; the LEFT wall (x o.left, -4.2) holds the front door (o.door [[t, 0..1]]: it swings
  // into the room toward +Z) onto a sunny garden (lawn and a painted backdrop of sky, hedge and trees beyond); the RIGHT wall (x o.right, 6.8) has an
  // open doorway at z -0.9..0.9 onto a hallway (a floor, a wall with coat hooks); o.front (6.5) a front wall for reverse shots; walls 3.4 high
  seDining(o) {
    const g = grp(), Lw = o.left ?? -4.2, Rw = o.right ?? 6.8, Bk = o.back ?? -2.6, Fr = o.front ?? 6.5, H = o.h ?? 3.4, WALL = o.wall || '#D9E4C9', WAIN = '#8E6A48';
    const wp = canvas(128, 128), c = wp.getContext('2d'); c.fillStyle = WALL; c.fillRect(0, 0, 128, 128); c.fillStyle = '#C3D3B0';
    for (const [x, y] of [[32, 32], [96, 96], [96, 32], [32, 96]]) { c.beginPath(); c.arc(x, y, 9, 0, TAU); c.fill(); }
    c.fillStyle = '#E8A0A0'; for (const [x, y] of [[32, 32], [96, 96]]) { c.beginPath(); c.arc(x, y, 4, 0, TAU); c.fill(); }
    const wpT = tex(wp); wpT.wrapS = wpT.wrapT = THREE.RepeatWrapping;
    const wallM = (w, h) => { const t = wpT.clone(); t.needsUpdate = true; t.repeat.set(w / 0.6, h / 0.6); return L('#FFFFFF', { map: t }); };
    const panel = (w, h, x, y, z, ry) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), wallM(w, h)); m.position.set(x, y, z); m.rotation.y = ry; m.receiveShadow = true; g.add(m); return m; };
    const wain = (w, x, z, ry) => { const m = grp(at(box(w, 1.0, 0.04, WAIN), 0, 0.5, 0), at(box(w, 0.06, 0.07, '#6A4A30'), 0, 1.02, 0.01), at(box(w, 0.12, 0.05, '#5A3A26'), 0, 0.06, 0.01)); m.position.set(x, 0, z); m.rotation.y = ry; g.add(m); };
    const fl = canvas(256, 256), fc = fl.getContext('2d'); fc.fillStyle = '#B98A5E'; fc.fillRect(0, 0, 256, 256);
    for (let i = 0; i < 8; i++) { fc.fillStyle = i % 2 ? '#B0805A' : '#C2946A'; fc.fillRect(0, i * 32, 256, 31); fc.fillStyle = '#8A6040'; fc.fillRect(0, i * 32 + 31, 256, 1); fc.fillRect(((i * 97) % 256), i * 32, 2, 32); }
    const flT = tex(fl); flT.wrapS = flT.wrapT = THREE.RepeatWrapping; flT.repeat.set((Rw - Lw) / 2, (Fr - Bk) / 2);
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(Rw - Lw, Fr - Bk), L('#FFFFFF', { map: flT, ...OFF })); floor.rotation.x = -PI / 2; floor.position.set((Lw + Rw) / 2, 0.012, (Bk + Fr) / 2); floor.receiveShadow = true; g.add(floor);
    // back wall with a window and the sideboard
    panel(Rw - Lw, H, (Lw + Rw) / 2, H / 2, Bk, 0); wain(Rw - Lw, (Lw + Rw) / 2, Bk + 0.025, 0);
    const winX = o.winX ?? 2.2; g.add(at(box(1.3, 1.25, 0.08, '#F4EEE2', { outline: 0.006 }), winX, 1.95, Bk + 0.04));
    g.add(at(paintPlane(1.12, 1.07, (cc, Wc, Hc) => { const gr = cc.createLinearGradient(0, 0, 0, Hc); gr.addColorStop(0, '#7EC0E8'); gr.addColorStop(1, '#CFE8F2'); cc.fillStyle = gr; cc.fillRect(0, 0, Wc, Hc); cc.fillStyle = '#6FA85A'; cc.fillRect(0, Hc * 0.72, Wc, Hc * 0.28); cc.fillStyle = '#4E8A4A'; for (let i = 0; i < 4; i++) { cc.beginPath(); cc.arc(Wc * (0.15 + i * 0.25), Hc * 0.7, Wc * 0.1, 0, TAU); cc.fill(); } cc.fillStyle = '#F4EEE2'; cc.fillRect(Wc * 0.48, 0, Wc * 0.04, Hc); cc.fillRect(0, Hc * 0.48, Wc, Hc * 0.04); }, { res: 256, emissive: 0.7 }), winX, 1.95, Bk + 0.085));
    const sbX = o.sideX ?? -1.2; g.add(at(box(1.8, 0.85, 0.5, '#7A5236', { pivot: 'bottom', outline: 0.008 }), sbX, 0, Bk + 0.27));
    for (const dx of [-0.45, 0.45]) g.add(at(box(0.8, 0.6, 0.02, '#8E6646'), sbX + dx, 0.38, Bk + 0.53), at(sphere(0.025, '#D8B54A', 0), sbX + dx * 0.2, 0.45, Bk + 0.55));
    g.add(at(cyl(0.08, 0.06, 0.22, '#5E8CB8', 10, { pivot: 'bottom', outline: 0.03 }), sbX - 0.5, 0.85, Bk + 0.27), at(lump(0.12, 0.1, 0.12, '#E86A8A', 7, 0.2, 1), sbX - 0.5, 1.13, Bk + 0.27));
    g.add(at(box(1.1, 0.75, 0.05, '#B8913A', { outline: 0.01 }), sbX, 1.85, Bk + 0.03));
    g.add(at(paintPlane(0.96, 0.62, (cc, Wc, Hc) => { const gr = cc.createLinearGradient(0, 0, 0, Hc); gr.addColorStop(0, '#9FCDE8'); gr.addColorStop(1, '#F2E2C2'); cc.fillStyle = gr; cc.fillRect(0, 0, Wc, Hc); cc.fillStyle = '#7FA06A'; cc.beginPath(); cc.moveTo(0, Hc * 0.7); cc.quadraticCurveTo(Wc * 0.4, Hc * 0.45, Wc, Hc * 0.65); cc.lineTo(Wc, Hc); cc.lineTo(0, Hc); cc.fill(); cc.fillStyle = '#5E8A4A'; cc.beginPath(); cc.moveTo(0, Hc * 0.85); cc.quadraticCurveTo(Wc * 0.6, Hc * 0.68, Wc, Hc * 0.82); cc.lineTo(Wc, Hc); cc.lineTo(0, Hc); cc.fill(); cc.fillStyle = '#F6E27A'; cc.beginPath(); cc.arc(Wc * 0.75, Hc * 0.25, Wc * 0.07, 0, TAU); cc.fill(); }, { res: 256, emissive: 0.3 }), sbX, 1.85, Bk + 0.058));
    // the left wall: the front door at z o.doorZ (0), 1.3 wide, 2.6 high, opening into the room; the garden behind it
    const dz = o.doorZ ?? 0, DW = 1.3, DH = 2.6;
    panel(Fr - dz - DW / 2, H, Lw, H / 2, (Fr + dz + DW / 2) / 2, PI / 2).scale.x = 1; panel(dz - DW / 2 - Bk, H, Lw, H / 2, (Bk + dz - DW / 2) / 2, PI / 2); panel(DW, H - DH, Lw, DH + (H - DH) / 2, dz, PI / 2);
    wain(Fr - dz - DW / 2, Lw + 0.025, (Fr + dz + DW / 2) / 2, PI / 2); wain(dz - DW / 2 - Bk, Lw + 0.025, (Bk + dz - DW / 2) / 2, PI / 2);
    for (const sd of [-1, 1]) g.add(at(box(0.14, DH + 0.12, 0.16, '#F4EEE2', { outline: 0.006 }), Lw + 0.03, (DH + 0.12) / 2, dz + sd * (DW / 2 + 0.07)));
    g.add(at(box(0.16, 0.14, DW + 0.42, '#F4EEE2', { outline: 0.006 }), Lw + 0.03, DH + 0.07, dz));
    const piv = grp(); piv.position.set(Lw + 0.02, 0, dz + DW / 2); g.add(piv);
    const leaf = grp(at(box(0.06, DH - 0.02, DW - 0.04, o.doorColor || '#2F6E6A', { outline: 0.006 }), 0, (DH - 0.02) / 2, -(DW - 0.04) / 2));
    for (const [y, hh] of [[1.85, 0.8], [0.75, 0.9]]) leaf.add(at(box(0.02, hh, DW * 0.62, '#255A56'), 0.035, y, -(DW - 0.04) / 2));
    leaf.add(at(sphere(0.05, '#D8B54A', 0), 0.08, 1.15, -(DW - 0.04) + 0.14));
    piv.add(leaf);
    // outside: a lawn, a path, a hedge and a painted garden backdrop
    const lawn = box(14, 0.05, 30, '#86BE5C'); lawn.position.set(Lw - 7.1, 0.005, dz); g.add(lawn);
    const path = box(5, 0.03, 1.4, '#D8CBB0'); path.material = L('#D8CBB0', OFF); path.position.set(Lw - 2.6, 0.045, dz); g.add(path);
    g.add(at(box(0.9, 1.1, 14, '#4E8A4A', { pivot: 'bottom', outline: 0.004 }), Lw - 6.5, 0, dz));
    const bd = paintPlane(30, 12, (cc, Wc, Hc) => { const gr = cc.createLinearGradient(0, 0, 0, Hc); gr.addColorStop(0, '#6FB2E2'); gr.addColorStop(0.75, '#CDE7F2'); cc.fillStyle = gr; cc.fillRect(0, 0, Wc, Hc);
      cc.fillStyle = '#FFFFFF'; for (const [x, y, r] of [[0.2, 0.25, 0.04], [0.26, 0.23, 0.05], [0.33, 0.26, 0.035], [0.7, 0.18, 0.045], [0.76, 0.2, 0.035]]) { cc.beginPath(); cc.arc(Wc * x, Hc * y, Wc * r, 0, TAU); cc.fill(); }
      cc.fillStyle = '#5E9A50'; for (let i = 0; i < 12; i++) { cc.beginPath(); cc.arc(Wc * (i / 11), Hc * 0.8, Wc * 0.05, 0, TAU); cc.fill(); } cc.fillStyle = '#7EB55E'; cc.fillRect(0, Hc * 0.82, Wc, Hc * 0.18); }, { res: 512, emissive: 0.85 });
    bd.position.set(Lw - 9.5, 4.5, dz); bd.rotation.y = PI / 2; noShadow(bd); g.add(bd);
    // the right wall: a doorway onto the hallway
    const hz = 0.95;
    panel(Fr - hz, H, Rw, H / 2, (Fr + hz) / 2, -PI / 2); panel(hz - Bk, H, Rw, H / 2, (Bk - hz) / 2, -PI / 2); panel(2 * hz, H - 2.6, Rw, 2.6 + (H - 2.6) / 2, 0, -PI / 2);
    wain(Fr - hz, Rw - 0.025, (Fr + hz) / 2, -PI / 2); wain(hz - Bk, Rw - 0.025, (Bk - hz) / 2, -PI / 2);
    for (const sd of [-1, 1]) g.add(at(box(0.16, 2.72, 0.14, '#F4EEE2', { outline: 0.006 }), Rw - 0.03, 1.36, sd * (hz + 0.06)));
    g.add(at(box(0.16, 0.14, 2 * hz + 0.3, '#F4EEE2', { outline: 0.006 }), Rw - 0.03, 2.67, 0));
    const hall = new THREE.Mesh(new THREE.PlaneGeometry(4, 6), L('#A8805A', OFF)); hall.rotation.x = -PI / 2; hall.position.set(Rw + 2, 0.012, 0); hall.receiveShadow = true; g.add(hall);
    const hw = new THREE.Mesh(new THREE.PlaneGeometry(6, H), L('#E8D8B0')); hw.position.set(Rw + 3.4, H / 2, 0); hw.rotation.y = -PI / 2; g.add(hw);
    for (let i = 0; i < 4; i++) g.add(at(box(0.05, 0.05, 0.12, '#3A2A20'), Rw + 3.35, 1.75, -0.8 + i * 0.5), at(box(0.06, 0.55, 0.3, ['#B5402F', '#3E6A9A', '#E8C25A', '#5A7A4A'][i], { pivot: 'top', outline: 0.01 }), Rw + 3.3, 1.72, -0.8 + i * 0.5));
    // the front wall (for reverse shots)
    panel(Rw - Lw, H, (Lw + Rw) / 2, H / 2, Fr, PI); wain(Rw - Lw, (Lw + Rw) / 2, Fr - 0.025, PI);
    // (round 1) the ceiling: blue sky and a cloud showed over the wallpaper; it casts no shadow, so the light in the room does not change
    if (o.ceiling !== false) { const ce = new THREE.Mesh(new THREE.PlaneGeometry(Rw - Lw + 0.2, Fr - Bk + 0.2), L(o.ceilColor || '#F2ECDD', { side: THREE.DoubleSide })); ce.rotation.x = PI / 2; ce.position.set((Lw + Rw) / 2, H, (Bk + Fr) / 2);
      const cor = [[Rw - Lw, 0.1, 0.1, (Lw + Rw) / 2, Bk + 0.05, 0], [Rw - Lw, 0.1, 0.1, (Lw + Rw) / 2, Fr - 0.05, 0], [0.1, 0.1, Fr - Bk, Lw + 0.05, (Bk + Fr) / 2, 1], [0.1, 0.1, Fr - Bk, Rw - 0.05, (Bk + Fr) / 2, 1]];
      const cg = grp(ce); for (const [w_, h_, d_, x_, z_] of cor) cg.add(at(box(w_, h_, d_, '#F4EEE2', { outline: 0.006 }), x_, H - 0.05, z_));
      noShadow(cg); g.add(cg); }
    // (round 1) o.doorOut: the door opens outward onto the garden (opened inward it stood across the room, in front of mamie's chair)
    g.userData.update = t => { piv.rotation.y = (o.doorOut ? 1.65 : -1.65) * clamp01(keyAt(o.door, t, 0)) + rattle(o.slam ? [[o.slam, 0.08, 20, 5]] : null, t); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a wheat field (pivot at the floor in its middle): golden ground o.w x o.d (40 x 40) and
  // thousands of thick golden stalks with ears (instanced), clear inside o.clear [x0, x1, z0, z1] (the table's strip); they sway (o.wind)
  seWheat(o) {
    const W = o.w ?? 40, D = o.d ?? 40, g = grp(), cl = o.clear || [-1.5, 1.5, -1.2, 1.2];
    const gnd = new THREE.Mesh(new THREE.PlaneGeometry(W, D), L('#D8B85A', OFF)); gnd.rotation.x = -PI / 2; gnd.position.y = 0.06; gnd.receiveShadow = true; g.add(gnd);
    const stalk = new THREE.CylinderGeometry(0.012, 0.018, 0.9, 4).translate(0, 0.45, 0), ear = new THREE.CylinderGeometry(0.03, 0.022, 0.2, 5).translate(0, 1.0, 0);
    const N = o.n ?? 5000, ms = new THREE.InstancedMesh(stalk, mat('#E2C060'), N), me = new THREE.InstancedMesh(ear, mat('#C8962E', { emissive: '#3A2A0A' }), N), M = new THREE.Matrix4(), Q = new THREE.Quaternion(), Sv = new THREE.Vector3(), Pv = new THREE.Vector3(), E = new THREE.Euler();
    const base = []; let k = 0;
    for (let i = 0; i < N * 3 && k < N; i++) { const x = (hsh(i * 1.7) - 0.5) * W, z = (hsh(i * 2.9 + 5) - 0.5) * D; if (x > cl[0] && x < cl[1] && z > cl[2] && z < cl[3]) continue; base.push([x, z, hsh(i * 4.1) * TAU, 0.85 + hsh(i * 6.3) * 0.4]); k++; }
    ms.count = me.count = base.length;
    // (round 1) o.gust [[t0, dur], ...]: a front of wind crosses the field along o.gustDir at o.gustV m/s and bows every stalk it reaches by up to o.gustA rad
    const gd = o.gustDir || [0, 1], gl = Math.hypot(gd[0], gd[1]) || 1, gx = gd[0] / gl, gz = gd[1] / gl, Qb = new THREE.Quaternion(), AX = new THREE.Vector3(gz, 0, -gx), d0 = o.gustD0 ?? -Math.max(W, D) / 2;
    const bow = (t, x, z) => { let a = 0; for (const [t0, du] of o.gust || []) { const u = (t - t0 - (x * gx + z * gz - d0) / (o.gustV ?? 14)) / du; if (u > 0 && u < 1) a += Math.sin(PI * u) * (1 + 0.25 * Math.sin(u * 19 + x)); } return a * (o.gustA ?? 0.6); };
    const place = t => { base.forEach(([x, z, ph, s], i) => { E.set(0.12 * Math.sin(t * 2 + x * 0.4 + ph * 0.3), ph, 0.1 * Math.sin(t * 1.7 + z * 0.5)); Q.setFromEuler(E); const b = o.gust ? bow(t, x, z) : 0; if (b) { Qb.setFromAxisAngle(AX, b); Q.premultiply(Qb); } Sv.set(s, s, s); Pv.set(x, 0.04, z); M.compose(Pv, Q, Sv); ms.setMatrixAt(i, M); me.setMatrixAt(i, M); });
      ms.instanceMatrix.needsUpdate = true; me.instanceMatrix.needsUpdate = true; };
    place(0); ms.castShadow = false; me.castShadow = false; ms.receiveShadow = true; g.add(ms, me);
    if (o.wind) g.userData.update = t => place(t);
    return g;
  },

  // ---------------------------------------------------------------- a white napkin tucked into a collar (attach to the torso: front +Z, offsets in its frame): a
  // triangle hanging down the chest with an ink rim; o.s (1)
  seBib(o) {
    const s = o.s ?? 1, g = grp(), sh = new THREE.Shape(); sh.moveTo(-0.17 * s, 0); sh.lineTo(0.17 * s, 0); sh.lineTo(0, -0.32 * s); sh.closePath();
    const m = new THREE.Mesh(new THREE.ShapeGeometry(sh), L('#FFFFFF', { side: THREE.DoubleSide, emissive: '#7A7A7A' })); g.add(m);
    const r = new THREE.Mesh(new THREE.ShapeGeometry(sh), new THREE.MeshBasicMaterial({ color: INK, side: THREE.DoubleSide })); r.scale.setScalar(1.1); r.position.set(0, 0.012 * s, -0.004); g.add(r);
    g.add(at(box(0.08 * s, 0.05 * s, 0.03 * s, '#FFFFFF', { noGrain: true, outline: 0.05 }), 0, 0, 0.01));
    return g;
  },

  // ---------------------------------------------------------------- a dining chair (pivot at the floor, the seat faces +Z), seat at 0.48; o.color, o.cushion
  seChair(o) { return chairMesh(o.color, o.cushion); },

  // ---------------------------------------------------------------- hides the parts of the SET that fall inside o.boxes [[x0, x1, y0, y1, z0, z1], ...]
  // (world metres; the set's own meshes only, never an actor or a prop): the lab set's whiteboard of formulas, its tray of blue crystals and its
  // hazmat suits are not for a mathematician
  seHideSet(o) {
    const g = grp(); let done = false;
    g.userData.update = () => { if (done) return; let p = g; while (p.parent && p.parent.type !== 'Scene') p = p.parent; const set = p.children && p.children[0]; if (!set || set === g || p === g) return;
      set.updateMatrixWorld(true); const bb = new THREE.Box3(), c = new THREE.Vector3();
      set.traverse(m => { if (!m.isMesh && !m.isGroup) return; if (m.isGroup && m.children.some(x => x.isMesh)) {
          bb.setFromObject(m); bb.getCenter(c); for (const b of o.boxes || []) if (c.x > b[0] && c.x < b[1] && c.y > b[2] && c.y < b[3] && c.z > b[4] && c.z < b[5]) { m.visible = false; break; } } });
      set.traverse(m => { if (!m.isMesh) return; bb.setFromObject(m); bb.getCenter(c); for (const b of o.boxes || []) if (c.x > b[0] && c.x < b[1] && c.y > b[2] && c.y < b[3] && c.z > b[4] && c.z < b[5]) { m.visible = false; break; } });
      done = true; };
    return g;
  },

  // ---------------------------------------------------------------- (round 1) wild white hair (attach to the head joint: offsets in its frame, the head 0.5 high
  // from the chin): jagged inked tufts sticking out sideways and up from both temples, a bald crown between (a smooth white block read as a chef's
  // toque); o.hw the half width of the head (0.24), o.y the height of the temples (0.36), o.color, o.s (1) the tufts' length
  seWildHair(o) {
    const g = grp(), HW = o.hw ?? 0.24, Y = o.y ?? 0.36, C = o.color || '#F4F4F0', S = o.s ?? 1;
    const T = [[0.0, 0.17, 0.0, 0.25], [0.06, 0.21, 0.04, 0.6], [0.12, 0.19, -0.03, 0.95], [0.17, 0.15, 0.05, 1.3], [-0.06, 0.16, -0.05, 0.4], [0.2, 0.12, -0.06, 1.6], [0.1, 0.14, 0.09, 0.8], [-0.02, 0.13, 0.08, 1.1]];
    for (const sd of [-1, 1]) T.forEach(([dy, len, dz, a], i) => { const tf = box(0.075, len * S, 0.07, C, { pivot: 'bottom', taper: { x: 0.12, z: 0.25 }, noGrain: true, outline: 0.09 });
      tf.position.set(sd * (HW - 0.03), Y + dy, dz); tf.rotation.set((i % 3 - 1) * 0.25, 0, -sd * (a + 0.12 * Math.sin(i * 2.7))); g.add(tf); });
    for (let i = 0; i < 3; i++) { const tf = box(0.06, 0.1 * S, 0.06, C, { pivot: 'bottom', taper: { x: 0.12, z: 0.2 }, noGrain: true, outline: 0.09 }); tf.position.set((i - 1) * 0.1, 0.5, -0.06); tf.rotation.set(-0.3, 0, (1 - i) * 0.5); g.add(tf); }
    return g;
  },

  // ---------------------------------------------------------------- (round 1) the set's ground disc with holes where its own flat strips lie (a road or a path
  // a few millimetres over a 170 m disc fought it for depth: lawn flashed through the asphalt one frame in three). o.holes [[x0, x1, z0, z1], ...] in
  // world metres, each strictly inside a strip that covers it; o.color the ground's colour (to find it), o.r its radius (170)
  seGroundCut(o) {
    const g = grp(); let done = false, tries = 0;
    g.userData.update = () => { if (done || tries++ > 3) return; let rt = g; while (rt.parent) rt = rt.parent; if (rt === g) return;
      const col = new THREE.Color(o.color || '#8DBB5E'); let gm = null;
      // (round 3) o.plane: the set's ground is a huge two-triangle plane (grassland, 9 km): its depth drifts by centimetres under SwiftShader and it
      // painted over a pavement 12 cm above it on some frames; it is matched too and replaced by the finer disc with its holes
      const okType = ty => ty === 'CircleGeometry' || (o.plane && ty === 'PlaneGeometry');
      rt.traverse(n => { if (gm || !n.isMesh || !okType(n.geometry?.type) || !n.material?.color) return; if (n.material.color.getHexString() === col.getHexString()) gm = n; });
      if (!gm) return; const R = o.r ?? 170, sh = new THREE.Shape(); sh.absarc(0, 0, R, 0, TAU, false);
      for (const [x0, x1, z0, z1] of o.holes || []) { const h = new THREE.Path(); h.moveTo(x0, -z0); h.lineTo(x0, -z1); h.lineTo(x1, -z1); h.lineTo(x1, -z0); h.closePath(); sh.holes.push(h); }
      const geo = new THREE.ShapeGeometry(sh, 48).rotateX(-PI / 2), uv = geo.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) / 8, uv.getY(i) / 8);
      gm.geometry.dispose(); gm.geometry = geo; done = true; };
    return g;
  },

  // ---------------------------------------------------------------- (round 2) no snowflake near the lens: the snow set's falling flakes are square points, and
  // one that drifts within a metre or two of a close camera reads as a pale translucent square floating in the frame. While this prop is in the shot,
  // every Points cloud of the scene drops (in its vertex shader, so in the very frame drawn) the flakes nearer than o.near (2.6 m) to the camera
  seSnowClear(o) {
    const g = grp(), NEAR = o.near ?? 2.6; let hooked = false;
    const live = () => { for (let p = g; p; p = p.parent) { if (!p.visible) return false; if (!p.parent) return p.type === 'Scene' || p !== g; } return false; };
    g.userData.update = () => { if (hooked) return; let rt = g; while (rt.parent) rt = rt.parent; if (rt === g) return; let found = 0;
      rt.traverse(n => { if (!n.isPoints || !n.material || Array.isArray(n.material)) return; found++; if (n.userData.seClear) return; const U = { value: 0 }; n.userData.seClear = U;
        const m = n.material, prevC = m.onBeforeCompile;
        m.onBeforeCompile = (sh, r) => { prevC?.(sh, r); sh.uniforms.uSeNear = U; const v = sh.vertexShader, e = v.lastIndexOf('}');
          sh.vertexShader = v.slice(0, e).replace('void main() {', 'uniform float uSeNear;\nvoid main() {') + '  if (-mvPosition.z < uSeNear) gl_Position = vec4(2.0, 2.0, 2.0, 1.0);\n}\n'; };
        m.customProgramCacheKey = () => 'seSnowClear'; m.needsUpdate = true;
        const prev = n.onBeforeRender; n.onBeforeRender = function (...q) { U.value = live() ? NEAR : 0; return prev?.apply(this, q); }; });
      hooked = found > 0; };
    return g;
  },

  // ---------------------------------------------------------------- (round 2) a French letterbox on a gate pillar (pivot at the floor under the pillar, front +Z):
  // a pale rendered pillar with a cap, a dark green metal box on its front with a slot under a little hood, a lock and a nameplate left blank
  // (no lettering, no emblem); o.color the box, o.h (1.25) the pillar
  seLetterbox(o) {
    const g = grp(), H = o.h ?? 1.25, C = o.color || '#2F5E4A';
    g.add(at(box(0.42, H, 0.42, o.pillar || '#E8DCC4', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(0.5, 0.08, 0.5, '#CDBFA4', { outline: 0.012 }), 0, H + 0.04, 0));
    const b = grp(at(box(0.34, 0.4, 0.16, C, { outline: 0.02 }), 0, 0, 0), at(box(0.36, 0.04, 0.05, C, { outline: 0.03 }), 0, 0.12, 0.09), at(box(0.24, 0.02, 0.01, '#14181C'), 0, 0.095, 0.082),
      at(box(0.1, 0.05, 0.01, '#E8E4D8'), 0, -0.04, 0.082), at(cyl(0.018, 0.018, 0.012, '#C9B26A', 8), 0.11, -0.12, 0.085, PI / 2));
    b.position.set(0, H * 0.72, 0.29); g.add(b);
    return g;
  },

  // ---------------------------------------------------------------- (round 2) the inside of a lorry cab seen through its open side window (pivot at the floor of
  // the cab under the steering wheel, the driver looks along +Z): a pale lining on the back wall and the roof (the cab read as a black hole), a big
  // steering wheel high enough to show over the sill (the lorry's own sits under it), its column, and a small warm cab light; o.ry its facing
  seCab(o) {
    const g = grp(), W = o.w ?? 1.9, Hh = o.h ?? 1.1, D = o.d ?? 1.0;
    g.add(at(box(W, Hh, 0.03, o.lining || '#C9C2B4'), 0, Hh / 2 + 0.05, -D), at(box(W, 0.03, D + 0.2, '#D6D0C2'), 0, Hh + 0.08, -D / 2));
    const wh = grp(at(new THREE.Mesh(new THREE.TorusGeometry(o.wr ?? 0.24, 0.032, 6, 20), mat('#24272C')), 0, 0, 0), at(box(0.04, (o.wr ?? 0.24) * 2, 0.03, '#2E3238'), 0, 0, 0), at(cyl(0.05, 0.05, 0.05, '#3A3E46', 10), 0, 0, 0.0, PI / 2));
    ink(wh.children[0], 0.06); wh.position.set(0, o.wy ?? 0.4, 0); wh.rotation.x = o.wTilt ?? -0.55; g.add(wh);
    g.add(at(box(0.06, 0.06, 0.5, '#24272C'), 0, (o.wy ?? 0.4) - 0.15, 0.22, -0.55, 0, 0));
    const lt = new THREE.PointLight(o.lightColor || '#FFF0D8', o.I ?? 1.4, o.R ?? 2.6, 1.2); lt.position.set(0, Hh - 0.05, -D / 2); g.add(lt);
    g.userData.wheel = [0, o.wy ?? 0.4, 0]; return g;
  },

  // ---------------------------------------------------------------- (round 3) a stretched rubber arm drawn as one tapered, sagging sleeve (pivot at the world
  // origin: place it at [0, 0, 0]): from o.from (the shoulder, off frame) to the mitten, whose world position follows o.track [[t, x, y, z], ...]
  // (sampled at the frames, interpolated between them); the elbow sags by o.sag (0.14) of the length along o.sagDir ([0, -1, 0]); the upper arm is
  // o.r0 (0.065) thick, the forearm tapers to o.r1 (0.032); a pale cuff at the wrist (o.cuff) and a mitten (o.hand) on the end; inked. A plain
  // straight stretched limb of the rig read as a plank of wood
  seSleeve(o) {
    const g = grp(), A = new THREE.Vector3(...(o.from || [0, 1, 0])), TR = o.track || [[0, 0, 1, 0.5]], N = 26, RAD = 10, SAG = o.sag ?? 0.14;
    const R0 = o.r0 ?? 0.065, R1 = o.r1 ?? 0.032, SD = new THREE.Vector3(...(o.sagDir || [0, -1, 0])).normalize();
    const C1 = new THREE.Color(o.color || '#B48CD2'), C2 = new THREE.Color(o.cuff || '#F4EEE2');
    const nV = (N + 1) * RAD, pos = new Float32Array(nV * 3), pos2 = new Float32Array(nV * 3), col = new Float32Array(nV * 3), idx = [];
    for (let i = 0; i < N; i++) for (let j = 0; j < RAD; j++) { const a = i * RAD + j, b = i * RAD + (j + 1) % RAD, c = a + RAD, d = b + RAD; idx.push(a, c, b, b, c, d); }
    for (let i = 0; i <= N; i++) { const cc = i / N > 0.9 ? C2 : C1; for (let j = 0; j < RAD; j++) { const q = (i * RAD + j) * 3; col[q] = cc.r; col[q + 1] = cc.g; col[q + 2] = cc.b; } }
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(pos, 3)); geo.setAttribute('color', new THREE.BufferAttribute(col, 3)); geo.setIndex(idx);
    const geo2 = new THREE.BufferGeometry(); geo2.setAttribute('position', new THREE.BufferAttribute(pos2, 3)); geo2.setIndex(idx);
    const tube = new THREE.Mesh(geo, L('#FFFFFF', { vertexColors: true })); tube.castShadow = true; tube.frustumCulled = false; g.add(tube);
    const rim = new THREE.Mesh(geo2, new THREE.MeshBasicMaterial({ color: INK, side: THREE.BackSide })); rim.frustumCulled = false; rim.castShadow = false; rim.name = 'outline'; g.add(rim);
    const mit = grp(), palm = lump(0.06, 0.05, 0.045, o.hand || '#F2C9A6', 6, 0.08, 1), thumb = lump(0.022, 0.03, 0.02, o.hand || '#F2C9A6', 7, 0.08, 1);
    ink(palm, 0.08); ink(thumb, 0.1); thumb.position.set(0.0, 0.04, 0.035); mit.add(palm, thumb); g.add(mit);
    const B = new THREE.Vector3(), E = new THREE.Vector3(), Cq = new THREE.Vector3(), P = new THREE.Vector3(), T = new THREE.Vector3(), Nn = new THREE.Vector3(), Bn = new THREE.Vector3(), UP = new THREE.Vector3(0, 1, 0);
    const at_ = t => { let i = 0; while (i < TR.length - 1 && TR[i + 1][0] <= t) i++; const a = TR[i], b = TR[Math.min(i + 1, TR.length - 1)], u = b[0] > a[0] ? clamp01((t - a[0]) / (b[0] - a[0])) : 0;
      return B.set(lerp(a[1], b[1], u), lerp(a[2], b[2], u), lerp(a[3], b[3], u)); };
    const curve = (u, out) => { const v = 1 - u; return out.set(v * v * A.x + 2 * v * u * Cq.x + u * u * B.x, v * v * A.y + 2 * v * u * Cq.y + u * u * B.y, v * v * A.z + 2 * v * u * Cq.z + u * u * B.z); };
    const radius = u => u < 0.48 ? R0 * (1 - 0.12 * u) : lerp(R0 * 0.9, R1, smooth((u - 0.48) / 0.4));
    g.userData.update = t => {
      at_(t); const len = A.distanceTo(B); E.copy(A).lerp(B, 0.5).addScaledVector(SD, SAG * len); Cq.copy(E).multiplyScalar(2).addScaledVector(A, -0.5).addScaledVector(B, -0.5);
      for (let i = 0; i <= N; i++) {
        const u = i / N; curve(u, P); curve(Math.min(1, u + 0.01), T); if (u >= 1) { curve(0.99, T); T.subVectors(P, T); } else T.sub(P); T.normalize();
        Nn.crossVectors(T, UP); if (Nn.lengthSq() < 1e-6) Nn.set(1, 0, 0); Nn.normalize(); Bn.crossVectors(Nn, T).normalize();
        const rr = radius(u);
        for (let j = 0; j < RAD; j++) { const a = j / RAD * TAU, cx = Math.cos(a), sy = Math.sin(a), q = (i * RAD + j) * 3;
          const dx = Nn.x * cx + Bn.x * sy, dy = Nn.y * cx + Bn.y * sy, dz = Nn.z * cx + Bn.z * sy;
          pos[q] = P.x + dx * rr; pos[q + 1] = P.y + dy * rr; pos[q + 2] = P.z + dz * rr;
          pos2[q] = P.x + dx * (rr + 0.011); pos2[q + 1] = P.y + dy * (rr + 0.011); pos2[q + 2] = P.z + dz * (rr + 0.011); }
      }
      geo.attributes.position.needsUpdate = true; geo2.attributes.position.needsUpdate = true; geo.computeVertexNormals(); geo2.computeVertexNormals(); geo.computeBoundingSphere(); geo2.computeBoundingSphere();
      curve(0.97, P); mit.position.copy(B); mit.lookAt(P); mit.rotateY(PI);
    };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a soft warm fill light on the faces (no visible source; pivot at the light): o.I (1.2), o.R (2.5)
  seFill(o) { const g = grp(), lt = new THREE.PointLight(o.color || '#FFE8CC', o.I ?? 1.2, o.R ?? 2.5, 1.2); g.add(lt); return g; },
};

// one leek (pivot at its root end, along +X tilted up): white shaft, a pale green middle, a fan of dark green leaves
function leekMesh(len, seed, x, z, ry, tilt) {
  const g = grp(), w = cyl(0.022, 0.024, len * 0.45, '#F4F2E6', 8, { noGrain: true }); w.rotation.z = -PI / 2; w.position.x = len * 0.225; ink(w, 0.06); g.add(w);
  const m = cyl(0.024, 0.022, len * 0.2, '#B8D88A', 8, { noGrain: true }); m.rotation.z = -PI / 2; m.position.x = len * 0.55; g.add(m);
  for (let i = 0; i < 3; i++) { const lf = box(len * 0.4, 0.008, 0.05, '#3E7A3A', { taper: { x: 1, z: 0.4 }, taperAxis: 'x', outline: 0.04 }); lf.position.set(len * 0.82, 0.01 * (i - 1), 0.02 * (i - 1)); lf.rotation.set((i - 1) * 0.5, (i - 1) * 0.3, 0.1 * (i - 1)); g.add(lf); }
  for (let i = 0; i < 4; i++) g.add(at(box(0.004, 0.02, 0.004, '#E8E0C8'), -0.005, (i - 1.5) * 0.008, 0, 0, 0, PI / 2 + (i - 1.5) * 0.4));
  g.position.set(x, 0.06 + z * 0.4, z - 0.02); g.rotation.set(0, ry, tilt === 0 ? 0 : 0.5 + tilt * 0.2); return g;
}
