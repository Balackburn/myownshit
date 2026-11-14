// Set library: full environments for shots. buildSet(name, opts) -> THREE.Group with
//   userData.lighting = LIGHTING key (scene.js), userData.anchors = { name: [x,y,z] },
//   optional userData.update(t) (pure function of t).
// Layout contract: camera sits around z=+3..+8 looking toward -Z; walls / backdrops live
// behind (negative z) and at the sides; a ~2.5 m radius around the origin stays clear for
// actors; ground extends far (>=150 m) so wide shots never show an edge.
import * as THREE from 'three';
import { imageTexture, TEXTURES } from './models.js';
import { PALETTE as P, mat, box, cyl, sphere, rng } from './style.js';
import { buildProp, grp, at, rod, label, canvasPlane, glow, glassMat, inst, mesh, torus } from './props.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { holeOutline } from './props_trou.js';

const PI = Math.PI, TAU = PI * 2;
const SKY_DAY = ['#8CAFBD', '#D6E1DA'], SKY_NIGHT = ['#111A2A', '#2C3B57'];

/* ------------------------------------------------------------------ helpers */
const prop = (name, o = {}, x = 0, y = 0, z = 0, ry = 0, s = 1) => { const p = at(buildProp(name, o), x, y, z, 0, ry, 0); p.scale.setScalar(s); p.userData.update?.(0); return p; };
// Repeat the paper grain on big surfaces instead of stretching it.
function tileUV(geo, s) { const uv = geo.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) * s, uv.getY(i) * s); return geo; }
// Horizontal plane (geometry pre-rotated, so at() is safe).
function flat(w, d, color, x = 0, y = 0, z = 0, opts) {
  const m = mesh(tileUV(new THREE.PlaneGeometry(w, d).rotateX(-PI / 2), Math.max(w, d) / 3), mat(color, opts));
  m.castShadow = false; m.position.set(x, y, z); return m;
}
// Round ground disc (edge hides inside the sky dome).
function ground(color, r = 170) { const m = mesh(tileUV(new THREE.CircleGeometry(r, 32).rotateX(-PI / 2), r / 4), mat(color)); m.castShadow = false; return m; }
// The same pieces with a hole cut in them (hole: world [x, z] points): real geometry, so a character can fall through the ground.
function holedGeo(outer, holePts, x, z, uvS) {
  const sh = new THREE.Shape(); outer(sh); const h = new THREE.Path(); holePts.forEach(([px, pz], i) => h[i ? 'lineTo' : 'moveTo'](px - x, -(pz - z))); h.closePath(); sh.holes.push(h);
  const geo = new THREE.ShapeGeometry(sh, 24).rotateX(-PI / 2), uv = geo.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) * uvS, uv.getY(i) * uvS); return geo;
}
function flatHoled(w, d, color, x, y, z, holePts) { const m = mesh(holedGeo(sh => { sh.moveTo(-w / 2, -d / 2); sh.lineTo(w / 2, -d / 2); sh.lineTo(w / 2, d / 2); sh.lineTo(-w / 2, d / 2); sh.closePath(); }, holePts, x, z, 1 / 3), mat(color)); m.castShadow = false; m.position.set(x, y, z); return m; }
function groundHoled(color, holePts, r = 170) { const m = mesh(holedGeo(sh => sh.absarc(0, 0, r, 0, TAU, false), holePts, 0, 0, 1 / 4), mat(color)); m.castShadow = false; return m; }
// Wall slab: receives shadows but never casts them (so rooms aren't darkened by their own walls).
function wall(w, h, d, color, x, y, z) { const m = box(w, h, d, color); tileUV(m.geometry, Math.max(w, h) / 2.5); m.castShadow = false; m.position.set(x, y, z); return m; }
// Inward-facing low-poly sky dome with a vertical gradient.
function sky(g, [top, bottom] = SKY_DAY) {
  const geo = new THREE.IcosahedronGeometry(180, 2), c = new THREE.Color(), ct = new THREE.Color(top), cb = new THREE.Color(bottom), pos = geo.attributes.position, col = [];
  for (let i = 0; i < pos.count; i++) { const k = Math.min(1, Math.max(0, pos.getY(i) / 180 * 1.5)); c.lerpColors(cb, ct, Math.sqrt(k)); col.push(c.r, c.g, c.b); }
  geo.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
  const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.BackSide, fog: false }));
  m.renderOrder = -10; g.add(m); return m;
}
function nightSky(g, moon = [-30, 38, -120]) { sky(g, SKY_NIGHT); g.add(prop('stars', { radius: 150, count: 420 })); if (moon) g.add(prop('moon', { radius: 5 }, ...moon)); }
function clouds(g, seed = 2, n = 7) {
  const r = rng(seed);
  for (let i = 0; i < n; i++) g.add(prop('cloud', { seed: seed * 10 + i, scale: 3 + r() * 3 }, (i / (n - 1) - 0.5) * 150 + (r() - 0.5) * 20, 12 + r() * 14, -55 - r() * 60, r() * 0.4));
}
// Low rolling hills (flattened low-poly spheres) along the horizon.
function hills(g, cols, { seed = 3, n = 7, z0 = -45, z1 = -85, sx = 22, sy = 6 } = {}) {
  const r = rng(seed);
  for (let i = 0; i < n; i++) { const m = sphere(1, cols[i % cols.length], 1); m.scale.set(sx * (0.7 + r() * 0.6), sy * (0.6 + r() * 0.7), sx * 0.5);
    m.position.set((i / (n - 1) - 0.5) * 170 + (r() - 0.5) * 20, -sy * 0.15, z0 + (z1 - z0) * r()); m.rotation.y = r() * PI; m.castShadow = false; g.add(m); }
}
// Interior shell: floor, back wall, side walls, optional wainscot band + trim.
function room(g, o = {}) {
  const back = o.back ?? -3.6, half = o.half ?? 7, H = o.height ?? 7, front = o.front ?? 14, W = o.wall || P.cream, len = front - back, mz = (front + back) / 2;
  if (!o.noFloor) g.add(flat(300, 300, o.floor || P.creamDark));
  if (!o.noBack) g.add(wall(2 * half + 0.4, H, 0.2, W, 0, H / 2, back - 0.1));
  for (const s of [-1, 1]) g.add(wall(0.2, H, len, W, s * (half + 0.1), H / 2, mz));
  if (!o.noFront) g.add(wall(2 * half + 0.4, H, 0.2, W, 0, H / 2, front + 0.1)); // far front wall: reverse shots never look into the void
  if (o.band) {
    const bh = o.bandH ?? 1.0, t = o.trim || P.navy;
    if (!o.noBack) g.add(wall(2 * half, bh, 0.04, o.band, 0, bh / 2, back + 0.02), wall(2 * half, 0.08, 0.08, t, 0, bh + 0.04, back + 0.04));
    for (const s of [-1, 1]) g.add(wall(0.04, bh, len, o.band, s * (half - 0.02), bh / 2, mz), wall(0.08, 0.08, len, t, s * (half - 0.04), bh + 0.04, mz));
  }
  return { back, half };
}
// Flat curved path (single mesh -> no z-fighting at joins).
function ribbon(pts, w, color, y = 0.006) {
  const curve = new THREE.CatmullRomCurve3(pts.map(([x, z]) => new THREE.Vector3(x, y, z))), n = 120, pos = [], uv = [], idx = [];
  for (let i = 0; i <= n; i++) { const p = curve.getPoint(i / n), t = curve.getTangent(i / n), nx = -t.z * w / 2, nz = t.x * w / 2;
    pos.push(p.x + nx, y, p.z + nz, p.x - nx, y, p.z - nz); uv.push(0, i, 1, i); if (i) { const k = i * 2; idx.push(k - 2, k - 1, k, k - 1, k + 1, k); } }
  const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); geo.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); geo.setIndex(idx); geo.computeVertexNormals();
  if (geo.attributes.normal.getY(0) < 0) { idx.reverse(); geo.setIndex(idx); geo.computeVertexNormals(); }
  const m = mesh(geo, mat(color)); m.castShadow = false; return m;
}
function catenary(a, b, sag, n = 16) { const pts = []; for (let i = 0; i <= n; i++) { const k = i / n; pts.push(new THREE.Vector3(a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k - sag * 4 * k * (1 - k), a[2] + (b[2] - a[2]) * k)); } return pts; }
const wire = (pts, r = 0.015, c = P.ink) => mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), pts.length * 2, r, 4), mat(c));
// String of triangular bunting flags.
function bunting(a, b, sag, cols = [P.red, P.teal, P.cream]) {
  const pts = catenary(a, b, sag, 20), g = grp(wire(pts, 0.012)), tri = new THREE.ShapeGeometry(new THREE.Shape([new THREE.Vector2(-0.16, 0), new THREE.Vector2(0.16, 0), new THREE.Vector2(0, -0.38)]));
  const dir = new THREE.Vector3(b[0] - a[0], 0, b[2] - a[2]).normalize(), ry = Math.atan2(-dir.z, dir.x);
  pts.slice(1, -1).forEach((p, i) => g.add(at(mesh(tri, mat(cols[i % cols.length], { doubleSide: true })), p.x, p.y, p.z, 0, ry, 0)));
  return g;
}
// Painted canvas picture in a frame (wall decoration).
function picture(w, h, frame = P.navy, scene = 'hills') {
  const ft = imageTexture(TEXTURES.paintings[scene === 'sea' ? 1 : 0]);   // FLUX paintings (assets/textures) when loaded
  const art = ft ? new THREE.Mesh(new THREE.PlaneGeometry(w - 0.12, h - 0.12), new THREE.MeshLambertMaterial({ map: ft })) : canvasPlane(w - 0.12, h - 0.12, (g, W, H) => {
    g.fillStyle = scene === 'sea' ? '#BFD6D3' : P.tealPale; g.fillRect(0, 0, W, H);
    g.fillStyle = P.yellow; g.beginPath(); g.arc(W * 0.72, H * 0.3, H * 0.12, 0, TAU); g.fill();
    g.fillStyle = scene === 'sea' ? P.teal : P.green; g.beginPath(); g.moveTo(0, H); g.lineTo(0, H * 0.62); g.quadraticCurveTo(W * 0.3, H * 0.35, W * 0.55, H * 0.66); g.quadraticCurveTo(W * 0.8, H * 0.5, W, H * 0.6); g.lineTo(W, H); g.fill();
    g.fillStyle = P.red; g.fillRect(W * 0.25, H * 0.62, W * 0.12, H * 0.12);
  }, { res: 256 });
  return grp(box(w, h, 0.05, frame, { outline: 0.01 }), at(art, 0, 0, 0.027));
}
function tableLamp(x, y, z, shade = P.cream) { return at(grp(cyl(0.1, 0.12, 0.04, P.navy, 8, { pivot: 'bottom' }), at(cyl(0.015, 0.015, 0.35, P.navy, 6, { pivot: 'bottom' }), 0, 0.04, 0), at(cyl(0.11, 0.2, 0.22, shade, 8, { pivot: 'bottom', emissive: '#6B5A2A' }), 0, 0.35, 0)), x, y, z); }
function floorLamp(x, z, shade = P.cream) { return at(grp(cyl(0.16, 0.2, 0.05, P.navy, 8, { pivot: 'bottom' }), at(cyl(0.02, 0.02, 1.45, P.navy, 6, { pivot: 'bottom' }), 0, 0.05, 0), at(cyl(0.18, 0.3, 0.34, shade, 8, { pivot: 'bottom', emissive: '#6B5A2A' }), 0, 1.45, 0)), x, 0, z); }
function hangLamp(x, y, z, shade = P.yellow, light = 0) {
  const g = at(grp(at(cyl(0.01, 0.01, 6, P.ink, 4, { pivot: 'bottom' }), 0, 0.2, 0), at(mesh(new THREE.ConeGeometry(0.35, 0.3, 8, 1, true), mat(shade, { doubleSide: true })), 0, 0.05, 0), at(sphere(0.09, '#FFE7B0', 1, { emissive: '#FFD27A', noGrain: true }), 0, -0.07, 0)), x, y, z);
  if (light) { const l = new THREE.PointLight('#FFC98A', light, 10, 1.3); l.position.y = -0.3; g.add(l); }
  return g;
}
function sofa(c = P.teal, c2 = P.tealLight) {
  return grp(box(2.4, 0.42, 0.9, c, { pivot: 'bottom', outline: 0.005 }), at(box(1.1, 0.14, 0.75, c2), -0.57, 0.49, 0.05), at(box(1.1, 0.14, 0.75, c2), 0.57, 0.49, 0.05),
    at(box(2.4, 0.62, 0.24, c), 0, 0.73, -0.33), at(box(0.24, 0.66, 0.9, c, { pivot: 'bottom' }), -1.2, 0, 0), at(box(0.24, 0.66, 0.9, c, { pivot: 'bottom' }), 1.2, 0, 0),
    at(box(0.4, 0.38, 0.12, P.red), -0.75, 0.72, -0.18, -0.2, 0.1, 0.1), at(box(0.38, 0.36, 0.12, P.yellow), 0.8, 0.72, -0.18, -0.2, -0.15, -0.08));
}
function rock(s, c, r) { const m = sphere(s, c || P.grey, 0); m.scale.set(1.2, 0.6 + r() * 0.3, 1); m.position.y = s * 0.25; m.rotation.set(r(), r() * TAU, r()); return m; }
function pine(seed, snow = false, s = 1) {
  const r = rng(seed), g = grp(cyl(0.12, 0.16, 0.8, P.woodDark, 6, { pivot: 'bottom' }));
  for (let i = 0; i < 3; i++) { const rad = (1.3 - i * 0.35) * s, h = 1.3 * s, y = (0.6 + i * 0.85) * s;
    g.add(at(mesh(new THREE.ConeGeometry(rad, h, 7), mat(i % 2 ? '#2F5E58' : '#3A6E64')), 0, y + h / 2, 0, 0, r() * TAU, 0));
    if (snow) g.add(at(mesh(new THREE.ConeGeometry(rad * 0.55, h * 0.45, 7), mat(P.white)), 0, y + h * 0.78, 0, 0, r() * TAU, 0)); }
  return g;
}
function cactus(seed, s = 1) {
  const r = rng(seed), C = '#6E9C5A', g = grp(cyl(0.22, 0.25, 2.6, C, 8, { pivot: 'bottom', outline: 0.02 }));
  [[-1, 0.9 + r() * 0.4], [1, 1.3 + r() * 0.4]].forEach(([sd, y]) => g.add(at(cyl(0.13, 0.13, 0.45, C, 8), sd * 0.4, y, 0, 0, 0, PI / 2), at(cyl(0.13, 0.15, 0.7 + r() * 0.3, C, 8, { pivot: 'bottom' }), sd * 0.6, y - 0.08, 0)));
  g.scale.setScalar(s); return g;
}
function palm(seed) {
  const r = rng(seed), g = grp(); let p = [0, 0, 0];
  for (let i = 0; i < 6; i++) { const q = [p[0] + 0.12 + i * 0.03, p[1] + 0.6, p[2]]; g.add(rod(p, q, 0.13 - i * 0.012, i % 2 ? P.woodDark : P.wood)); p = q; }
  for (let i = 0; i < 7; i++) { const a = i * TAU / 7 + r() * 0.3, leaf = box(1.6, 0.04, 0.32, i % 2 ? P.green : '#7FA86A', { taper: { x: 1, z: 0.2 }, taperAxis: 'x' }); leaf.geometry.translate(0.8, 0, 0);
    g.add(at(leaf, p[0], p[1], p[2], 0, a, -0.45)); }
  return g;
}
// Product shelf with instanced, palette-coloured goods.
function shelf(len, seed, levels = 4) {
  const r = rng(seed), g = grp(), list = [], cols = [], pal = [P.red, P.teal, P.yellow, P.cream, P.navy, P.salmon, P.green, P.pink, P.tealLight];
  for (let i = 0; i <= Math.round(len / 1.2); i++) g.add(at(box(0.06, 2.1, 0.5, P.navyLight, { pivot: 'bottom' }), -len / 2 + i * len / Math.round(len / 1.2), 0, 0));
  for (let l = 0; l < levels; l++) { const y = 0.12 + l * 0.5; g.add(at(box(len, 0.04, 0.5, P.white), 0, y, 0));
    for (let x = -len / 2 + 0.12; x < len / 2 - 0.12;) { const w = 0.14 + r() * 0.14, h = 0.18 + r() * 0.2; list.push([x + w / 2, y + 0.02 + h / 2, 0.05, 0, 0, 0, w * 0.9, h, 0.3]); cols.push(pal[Math.floor(r() * pal.length)]); x += w; } }
  g.add(inst(new THREE.BoxGeometry(1, 1, 1), mat(P.white), list, cols), at(box(len, 0.15, 0.04, P.red), 0, 2.05, 0.25));
  return g;
}
// (cycle 10, story 48) A grocery shelf: rows of identical products in facings (water bottles, cans stacked two high, cereal boxes with a white
// front panel, oil and soda bottles), price strips along the shelf edges and a few yellow promo tags (the old shelf's random blocks read as books)
function grocerShelf(len, seed, levels = 4) {
  const r = rng(seed), g = grp(), cyl = [], cylC = [], bx = [], bxC = [], pan = [], cap = [], capC = [];
  for (let i = 0; i <= Math.round(len / 1.2); i++) g.add(at(box(0.06, 2.1, 0.5, P.navyLight, { pivot: 'bottom' }), -len / 2 + i * len / Math.round(len / 1.2), 0, 0));
  const kinds = ['water', 'cans', 'cereal', 'bottles'];
  for (let l = 0; l < levels; l++) { const y = 0.12 + l * 0.5; g.add(at(box(len, 0.04, 0.5, P.white), 0, y, 0), at(box(len, 0.045, 0.012, '#F7F5EE'), 0, y - 0.005, 0.256));
    const kind = kinds[(l + seed) % kinds.length], y0 = y + 0.02;
    for (let x = -len / 2 + 0.1; x < len / 2 - 0.2;) {
      const n = 3 + Math.floor(r() * 4), c = [P.red, P.teal, P.yellow, P.navy, P.green, '#E8742A', '#7A3E9C', P.salmon][Math.floor(r() * 8)];
      for (let k = 0; k < n && x < len / 2 - 0.15; k++) {
        if (kind === 'water') { cyl.push([x + 0.05, y0 + 0.15, 0.05, 0, 0, 0, 0.09, 0.3, 0.09]); cylC.push('#A8D8EE'); cap.push([x + 0.05, y0 + 0.315, 0.05, 0, 0, 0, 0.035, 0.03, 0.035]); capC.push(c); x += 0.105; }
        else if (kind === 'cans') { for (const hy of [0, 0.125]) cyl.push([x + 0.04, y0 + 0.06 + hy, 0.06, 0, 0, 0, 0.07, 0.12, 0.07]), cylC.push(c); x += 0.085; }
        else if (kind === 'cereal') { bx.push([x + 0.1, y0 + 0.16, 0.02, 0, 0, 0, 0.19, 0.32, 0.08]); bxC.push(c); pan.push([x + 0.1, y0 + 0.19, 0.062, 0, 0, 0, 0.12, 0.1, 0.005]); x += 0.21; }
        else { cyl.push([x + 0.045, y0 + 0.13, 0.05, 0, 0, 0, 0.08, 0.26, 0.08]); cylC.push(['#C98A2E', '#3E8A4A', '#D9EEF2', c][k % 4]); cap.push([x + 0.045, y0 + 0.285, 0.05, 0, 0, 0, 0.03, 0.05, 0.03]); capC.push(P.ink); x += 0.1; }
      }
      x += 0.04 + r() * 0.06;
    }
    for (let x = -len / 2 + 0.6 + r() * 0.5; x < len / 2 - 0.3; x += 1.2 + r() * 0.8) g.add(at(box(0.13, 0.08, 0.008, P.yellow), x, y - 0.015, 0.265));
  }
  const cg = new THREE.CylinderGeometry(0.5, 0.5, 1, 10), bg = new THREE.BoxGeometry(1, 1, 1);
  if (cyl.length) g.add(inst(cg, mat(P.white), cyl, cylC)); if (cap.length) g.add(inst(cg, mat(P.white), cap, capC));
  if (bx.length) g.add(inst(bg, mat(P.white), bx, bxC)); if (pan.length) g.add(inst(bg, mat('#F7F5EE'), pan));
  g.add(at(box(len, 0.15, 0.04, P.red), 0, 2.05, 0.25));
  return g;
}
function windowsGrid(g, list, lit, dark) { if (list.lit.length) g.add(inst(new THREE.BoxGeometry(0.7, 0.9, 0.06), lit, list.lit)); if (list.dark.length) g.add(inst(new THREE.BoxGeometry(0.7, 0.9, 0.06), dark, list.dark)); }

// Sky dome centred on the camera every frame (userData.followCam): the horizon stays at eye level at any altitude, and it writes no
// depth, so terrain kilometres away still draws over it. R must stay below the camera's far plane.
function skyFollow(g, [top, bottom], R = 3000, below) {
  const geo = new THREE.IcosahedronGeometry(R, 3), c = new THREE.Color(), ct = new THREE.Color(top), cb = new THREE.Color(bottom), cl = new THREE.Color(below || bottom), pos = geo.attributes.position, col = [];
  for (let i = 0; i < pos.count; i++) { const y = pos.getY(i) / R; if (y < 0) c.copy(cb).lerp(cl, Math.min(1, -y * 4)); else c.lerpColors(cb, ct, Math.pow(Math.min(1, y * 1.4), 0.6)); col.push(c.r, c.g, c.b); }
  geo.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
  const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.BackSide, fog: false, depthWrite: false }));
  m.renderOrder = -10; m.userData.followCam = true; m.castShadow = m.receiveShadow = false; g.add(m); return m;
}
// Merge a static group into one mesh per material (world transforms baked): hundreds of houses in a handful of draw calls.
function mergeStatic(root) {
  root.updateMatrixWorld(true);
  const groups = new Map();
  root.traverse(n => {
    if (!n.isMesh || n.isInstancedMesh || !n.geometry || Array.isArray(n.material)) return;
    let geo = n.geometry.index ? n.geometry.toNonIndexed() : n.geometry.clone(); geo.applyMatrix4(n.matrixWorld);
    for (const k of Object.keys(geo.attributes)) if (!['position', 'normal', 'uv'].includes(k)) geo.deleteAttribute(k);
    if (!geo.attributes.normal) geo.computeVertexNormals();
    if (!geo.attributes.uv) geo.setAttribute('uv', new THREE.Float32BufferAttribute(new Float32Array(geo.attributes.position.count * 2), 2));
    geo.morphAttributes = {};
    const key = n.material.uuid + (n.castShadow ? 'c' : '');
    if (!groups.has(key)) groups.set(key, { m: n.material, geos: [], cast: n.castShadow }); groups.get(key).geos.push(geo);
  });
  const out = new THREE.Group();
  for (const { m, geos, cast } of groups.values()) { const merged = mergeGeometries(geos, false); if (!merged) continue; const mm = new THREE.Mesh(merged, m); mm.castShadow = cast; mm.receiveShadow = true; out.add(mm); }
  return out;
}
/* ------------------------------------------------------------------ sets */
const S = {
  office(o = {}) { // o.door === false: no door (a scene prop door replaces it); o.printer === false: free the right corner
    // (pass 4 of 50) o.wall / o.band / o.trim: walls of its own (a lab in the living room's peach and teal read as his flat); o.picture === false: no
    // landscape painting; o.carpet === false: no rug (its red band was the hottest colour of the frame, under the map)
    const g = grp(), { back } = room(g, { wall: o.wall || P.cream, band: o.band || P.teal, bandH: 1.05, trim: o.trim || P.navy, floor: o.floor || '#CDB894' });
    g.add(...(o.carpet === false ? [] : [prop('carpet', { w: 4.8, d: 2.6, color: o.carpet || P.red }, 0, 0, -0.4)]), prop('window', { w: 1.3, h: 1.3, color: P.teal }, -1.75, 1.0, back),
      prop('table', { color: P.red, legs: P.redDark, w: 0.75, d: 0.5, h: 0.72 }, 2.0, 0, back + 0.45), tableLamp(1.8, 0.72, back + 0.4), prop('mug', { color: P.cream }, 2.2, 0.72, back + 0.5),
      ...(o.picture === false ? [] : [at(picture(0.9, 0.7), 2.0, 2.05, back + 0.03)]), prop('plant', {}, -3.9, 0, back + 0.4),
      prop('desk', {}, -4.6, 0, -1.4, 0.35), prop('chair', { color: P.navy }, -4.9, 0, -2.1, 0.35));
    if (o.door !== false) g.add(prop('door', {}, 4.7, 0, back));
    g.add(at(grp(cyl(0.28, 0.28, 0.05, P.white, 12), at(torus(0.28, 0.03, P.navy, 4, 16), 0, 0, 0, PI / 2), at(box(0.02, 0.18, 0.01, P.ink), 0, 0.07, 0.03), at(box(0.13, 0.02, 0.01, P.ink), 0.05, 0, 0.03)), 3.4, 2.6, back + 0.03, PI / 2));
    // viz3d pass (lived-in office): background workstations under the window, filing cabinet, cork board with memos,
    // whiteboard, printer, water cooler, archive boxes, tube lights — acting areas (centre, desk front, door) stay clear
    const ws = x => grp(at(box(1.3, 0.05, 0.65, P.wood, { outline: 0.006 }), 0, 0.73, 0), at(box(0.05, 0.71, 0.6, P.navyLight, { pivot: 'bottom' }), -0.6, 0, 0), at(box(0.05, 0.71, 0.6, P.navyLight, { pivot: 'bottom' }), 0.6, 0, 0),
      at(box(0.5, 0.32, 0.04, P.ink, { outline: 0.006 }), 0, 1.0, -0.15), at(box(0.44, 0.26, 0.01, '#9FC6D4', { emissive: '#3E6A7A' }), 0, 1.0, -0.128), at(box(0.06, 0.12, 0.06, P.ink, { pivot: 'bottom' }), 0, 0.755, -0.18), at(box(0.4, 0.02, 0.14, P.ink), 0, 0.765, 0.1), prop('chair', { color: P.navy }, 0, 0, 0.55, PI));
    g.add(at(ws(), -1.2, 0, back + 0.45), at(ws(), 0.35, 0, back + 0.45));
    const fc = grp(at(box(0.5, 1.3, 0.6, '#8C949A', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0)); for (let d = 0; d < 3; d++) fc.add(at(box(0.44, 0.38, 0.01, '#9AA2A8'), 0, 0.23 + d * 0.42, 0.305), at(box(0.12, 0.03, 0.03, P.ink), 0, 0.33 + d * 0.42, 0.31));
    g.add(at(fc, -3.1, 0, back + 0.32));
    g.add(at(box(1.0, 0.7, 0.03, '#B98A5A', { outline: 0.006 }), 1.15, 1.75, back + 0.03));
    [[0.85, 1.85, 0.05], [1.2, 1.62, -0.04], [1.45, 1.88, 0.02]].forEach(([x, y, rz], i) => g.add(at(box(0.24, 0.3, 0.01, ['#F7F3EA', '#F2E27A', '#F7F3EA'][i]), x, y, back + 0.05, 0, 0, rz)));
    const wbd = canvasPlane(1.8, 1.0, (c, W, H) => { c.fillStyle = '#F7F7F2'; c.fillRect(0, 0, W, H); c.strokeStyle = '#2C4A8A'; c.lineWidth = 4; c.beginPath(); c.moveTo(W * 0.08, H * 0.8); [0.25, 0.4, 0.55, 0.7, 0.85].forEach((x, i) => c.lineTo(W * x, H * (0.7 - i * 0.12 + (i % 2) * 0.1))); c.stroke();
      c.fillStyle = '#B5302A'; c.font = `bold ${H * 0.13}px Arial`; c.fillText('OBJECTIFS Q3', W * 0.06, H * 0.18); c.fillStyle = '#2C4A8A'; c.font = `${H * 0.09}px Arial`; c.fillText('• synergies', W * 0.6, H * 0.4); c.fillText('• yaourts +12%', W * 0.6, H * 0.55); });
    g.add(at(box(1.9, 1.1, 0.04, '#C9CDCF', { outline: 0.006 }), 6.95, 1.6, -0.8, 0, -PI / 2, 0), at(wbd, 6.92, 1.6, -0.8, 0, -PI / 2, 0));
    if (o.printer !== false) g.add(at(box(0.7, 0.75, 0.5, P.navyLight, { pivot: 'bottom', outline: 0.006 }), 6.2, 0, back + 0.4), at(box(0.55, 0.3, 0.42, '#E8E8E4', { outline: 0.006 }), 6.2, 0.9, back + 0.4), at(box(0.4, 0.02, 0.3, P.white), 6.2, 1.06, back + 0.45));
    g.add(at(grp(at(box(0.36, 1.0, 0.36, '#E8E8E4', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(cyl(0.15, 0.15, 0.42, '#9FD3E8', 10, { pivot: 'bottom', opacity: 0.7 }), 0, 1.0, 0)), -6.3, 0, back + 0.35));
    [[6.3, 0, 1.0], [6.3, 0.45, 1.05], [5.8, 0, 1.4]].forEach(([x, y, z]) => g.add(at(box(0.5, 0.45, 0.4, '#C49A66', { pivot: 'bottom', outline: 0.006 }), x, y, z, 0, 0.2, 0)));
    [-2.5, 2.5].forEach(x => g.add(rod([x - 0.7, 3.6, -0.8], [x - 0.7, 3.35, -0.8], 0.006, P.ink), rod([x + 0.7, 3.6, -0.8], [x + 0.7, 3.35, -0.8], 0.006, P.ink), at(box(1.6, 0.06, 0.2, '#FFFFFF', { emissive: '#FFF6DA', noGrain: true }), x, 3.33, -0.8)));
    g.userData.anchors = { center: [0, 0, 0], window: [-1.75, 0, back + 0.7], sideTable: [2.0, 0.72, back + 0.45], door: [4.7, 0, back + 0.6], desk: [-4.6, 0, -1.4], deskChair: [-4.9, 0, -2.1], picture: [2.0, 2.05, back] };
    g.userData.lighting = 'interior'; return g;
  },
  livingRoom(o = {}) { // o.sofa / o.plant / o.tv / o.lamp === false: leave them out (a scene supplies movable ones)
    const g = grp(), { back } = room(g, { wall: P.cream, band: P.tealLight, bandH: 0.95, trim: P.teal, floor: P.wood });
    if (o.sofa !== false) g.add(at(sofa(), 0, 0, back + 0.55));
    if (o.lamp !== false) g.add(floorLamp(1.85, back + 0.45));
    if (o.plant !== false) g.add(prop('plant', {}, -1.85, 0, back + 0.4));
    if (o.tv !== false) g.add(prop('tv', { text: '' }, 3.7, 0, -1.2, -0.6));
    if (o.picture !== false) g.add(at(picture(o.pictureW ?? 1.4, (o.pictureW ?? 1.4) * 0.643, P.navy), o.pictureX ?? 0, o.pictureY ?? 2.35, back + 0.03));   // o.picture false / o.pictureX / o.pictureY / o.pictureW: no painting, or elsewhere (behind two heads it filled the gap between them, its border on their chins)
    if (o.carpet !== false) g.add(prop('carpet', { w: 3.6, d: 2.4, color: o.carpetColor || P.red }, 0, 0, -0.6));   // (50) o.carpet false: no rug (seen from above, its big red rectangle ate a third of the frame and the rings drawn on the floor)
    g.add(prop('window', { w: 1.2, h: 1.3, color: P.teal, curtains: P.red }, 3.6, 0.95, back),
      prop('table', { w: 0.5, d: 0.5, h: 0.55, color: P.teal }, -3.4, 0, back + 0.5), tableLamp(-3.4, 0.55, back + 0.5, P.salmon));
    g.userData.anchors = { center: [0, 0, 0], sofa: [0, 0, back + 0.55], sofaSeat: [0, 0.5, back + 0.75], lamp: [1.85, 0, back + 0.45], plant: [-1.85, 0, back + 0.4], picture: [0, 2.35, back], tv: [3.7, 0, -1.2], window: [3.6, 0, back + 0.7] };
    g.userData.lighting = 'interior'; return g;
  },
  kitchenNight(o = {}) { // o.fridge === false: no fridge (a scene fridge with an animated door replaces it)
    const g = grp(), { back } = room(g, { wall: '#2E5C59', band: '#24494A', bandH: 0.95, trim: P.navy, floor: P.navy });
    const tiles = []; for (let i = -12; i < 12; i++) for (let j = 0; j < 22; j++) if ((i + j) % 2 === 0) tiles.push([i * 0.8 + 0.4, 0.003, back + j * 0.8 + 0.4]);
    g.add(inst(new THREE.PlaneGeometry(0.8, 0.8).rotateX(-PI / 2), mat(P.redDark), tiles));
    if (o.fridge !== false) g.add(prop('fridge', { notes: 7 }, -2.7, 0, back + 0.38));
    // counter + upper cabinets
    g.add(at(box(3.0, 0.9, 0.6, '#3F7470', { pivot: 'bottom' }), -0.6, 0, back + 0.3), at(box(3.1, 0.05, 0.66, P.cream), -0.6, 0.925, back + 0.33));
    [-1.6, -0.6, 0.4].forEach(x => g.add(at(box(0.04, 0.7, 0.01, P.navy), x + 0.5, 0.45, back + 0.605), at(box(0.12, 0.03, 0.03, P.cream), x + 0.35, 0.75, back + 0.62)));
    g.add(at(box(0.9, 0.7, 0.36, '#3F7470', { pivot: 'bottom' }), -1.65, 1.75, back + 0.18), at(box(0.9, 0.7, 0.36, '#3F7470', { pivot: 'bottom' }), 0.45, 1.75, back + 0.18));
    g.add(prop('window', { w: 0.9, h: 0.8, color: P.cream, night: true }, -0.6, 1.25, back), at(cyl(0.12, 0.12, 0.01, P.cream, 10, { emissive: '#8A8460' }), -0.4, 1.95, back + 0.025, PI / 2));
    if (o.toaster !== false) g.add(prop('toaster', { color: P.red }, 0.3, 0.95, back + 0.3)); g.add(prop('mug', { color: P.yellow }, -1.4, 0.95, back + 0.35));
    // arched doorway (dark opening + cream frame)
    const ax = 2.8, ay = 1.9;
    g.add(at(box(1.1, ay, 0.02, '#0E1218'), ax, ay / 2, back + 0.01), at(mesh(new THREE.CylinderGeometry(0.55, 0.55, 0.02, 12, 1, false, PI / 2, PI), mat('#0E1218')), ax, ay, back + 0.01, PI / 2),
      at(torus(0.61, 0.06, P.cream, 4, 12, PI), ax, ay, back + 0.04), at(box(0.12, ay, 0.12, P.cream, { pivot: 'bottom' }), ax - 0.61, 0, back + 0.04), at(box(0.12, ay, 0.12, P.cream, { pivot: 'bottom' }), ax + 0.61, 0, back + 0.04));
    g.add(hangLamp(0, 2.7, -1.0, P.yellow, 7));
    g.userData.anchors = { center: [0, 0, 0], fridge: [-2.7, 0, back + 0.38], fridgeFront: [-2.7, 0, back + 1.5], counter: [-0.6, 0.95, back + 0.3], door: [ax, 0, back + 0.4], window: [-0.6, 1.25, back], lamp: [0, 2.6, -1.0] };
    g.userData.lighting = 'dark'; return g;
  },
  kitchenDay(o = {}) { // « La canicule »: a sunny pastel kitchen in a heatwave — peach walls, mint tiled band, a blazing window, a counter with a fan and a wilting plant;
    // o.fridge === false (a scene bigFridge replaces it; anchors.fridge is its spot)
    const g = grp(), { back } = room(g, { wall: '#F6D7AE', band: '#9FD8C8', bandH: 1.05, trim: '#E8A97E', floor: '#F4E6CC' });
    const tiles = []; for (let i = -12; i < 12; i++) for (let j = 0; j < 22; j++) if ((i + j) % 2 === 0) tiles.push([i * 0.6 + 0.3, 0.003, back + j * 0.6 + 0.3]);
    g.add(inst(new THREE.PlaneGeometry(0.6, 0.6).rotateX(-PI / 2), mat('#E9B88E'), tiles));
    if (o.fridge !== false) g.add(prop('bigFridge', { mode: 'full', open: 0 }, -2.7, 0, back + 0.5));
    g.add(at(box(3.0, 0.9, 0.6, '#7FC4B2', { pivot: 'bottom' }), 0.2, 0, back + 0.3), at(box(3.1, 0.05, 0.66, P.cream), 0.2, 0.925, back + 0.33));
    [-0.8, 0.2, 1.2].forEach(x => g.add(at(box(0.04, 0.7, 0.01, '#5E9E8E'), x + 0.5, 0.45, back + 0.605), at(box(0.12, 0.03, 0.03, P.cream), x + 0.35, 0.75, back + 0.62)));
    g.add(at(box(0.9, 0.7, 0.36, '#7FC4B2', { pivot: 'bottom' }), -0.85, 1.75, back + 0.18), at(box(0.9, 0.7, 0.36, '#7FC4B2', { pivot: 'bottom' }), 1.25, 1.75, back + 0.18));
    // the blazing window: a white-hot sky with the sun in it, and its light on the floor
    g.add(prop('window', { w: 1.0, h: 0.85, color: P.cream }, 0.2, 1.3, back));
    if (o.cold) g.add(at(canvasPlane(0.96, 0.8, (c, W, H) => { const gr = c.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#9FB2C4'); gr.addColorStop(1, '#E4EBF0'); c.fillStyle = gr; c.fillRect(0, 0, W, H);   // o.cold (September): a grey snowy sky, flakes, frost in the corners
      c.fillStyle = '#FFFFFF'; for (let i = 0; i < 46; i++) { c.beginPath(); c.arc((i * 53 % 97) / 97 * W, (i * 37 % 89) / 89 * H, 2 + (i % 3), 0, 2 * PI); c.fill(); }
      c.fillStyle = 'rgba(255,255,255,0.85)'; for (const [x, y] of [[0, 0], [W, 0], [0, H], [W, H]]) { c.beginPath(); c.arc(x, y, W * 0.22, 0, 2 * PI); c.fill(); } }, { res: 256, emissive: 0.8 }), 0.2, 1.3, back + 0.012));
    else g.add(at(canvasPlane(0.96, 0.8, (c, W, H) => { const gr = c.createRadialGradient(W * 0.65, H * 0.35, 4, W * 0.65, H * 0.35, W * 0.9); gr.addColorStop(0, '#FFFFF4'); gr.addColorStop(0.18, '#FFF1B0'); gr.addColorStop(0.5, '#FFD27A'); gr.addColorStop(1, '#F6B65C'); c.fillStyle = gr; c.fillRect(0, 0, W, H); }, { res: 256, emissive: 1 }), 0.2, 1.3, back + 0.012));
    const patch = new THREE.Mesh(new THREE.PlaneGeometry(1.1, 1.6).rotateX(-PI / 2), new THREE.MeshBasicMaterial({ color: '#FFE7A8', transparent: true, opacity: 0.35, depthWrite: false })); patch.position.set(0.35, 0.006, back + 1.6); patch.rotation.y = 0.15; if (!o.cold) g.add(patch);
    g.add(prop('deskFan', { color: '#5FA8D3' }, 1.2, 0.95, back + 0.32, -0.3), prop('wiltPlant', { wilt: 1 }, -0.9, 0.95, back + 0.32), prop('mug', { color: P.yellow }, 0.6, 0.95, back + 0.35));
    const ax = 2.8, ay = 1.9;   // arched doorway
    g.add(at(box(1.1, ay, 0.02, '#3A2E28'), ax, ay / 2, back + 0.01), at(mesh(new THREE.CylinderGeometry(0.55, 0.55, 0.02, 12, 1, false, PI / 2, PI), mat('#3A2E28')), ax, ay, back + 0.01, PI / 2),
      at(torus(0.61, 0.06, P.cream, 4, 12, PI), ax, ay, back + 0.04), at(box(0.12, ay, 0.12, P.cream, { pivot: 'bottom' }), ax - 0.61, 0, back + 0.04), at(box(0.12, ay, 0.12, P.cream, { pivot: 'bottom' }), ax + 0.61, 0, back + 0.04));
    g.add(hangLamp(0, 2.7, -1.0, P.yellow, 7));
    g.userData.anchors = { center: [0, 0, 0], fridge: [-2.7, 0, back + 0.5], fridgeFront: [-2.7, 0, back + 1.6], counter: [0.2, 0.95, back + 0.3], window: [0.2, 1.3, back], door: [ax, 0, back + 0.4], wall: [-1.2, 1.5, back] };
    g.userData.sun = [-0.4, 0.62, 0.68]; g.userData.lighting = 'interior'; return g;
  },
  suburbDay(o = {}) {   // o.sky [top, bottom]: e.g. an evening sky
    const g = grp(); sky(g, o.sky); clouds(g, 3);
    g.add(ground('#9DAF88'), flat(240, 3.4, P.cream, 0, 0.01, 0), flat(240, 0.25, P.creamDark, 0, 0.012, -1.75), flat(1.5, 4.6, P.cream, 0, 0.011, -5.9));
    g.add(prop('fence', { length: 11 }, -6.5, 0, -3.5), prop('fence', { length: 11 }, 6.5, 0, -3.5), prop('house', {}, -0.6, 0, -10), prop('mailbox', {}, 1.5, 0, -3.1));
    g.add(prop('house', { color: P.tealPale, roof: P.red, door: P.navy }, -11, 0, -15), prop('house', { color: P.creamDark, roof: P.teal }, 10, 0, -16, -0.2));
    [[-5.2, -7, 1], [5.5, -8, 2], [-9, -11, 3], [9.5, -12.5, 4], [15, -20, 5], [-16, -22, 6], [2.5, -18, 7]].forEach(([x, z, s]) => g.add(prop('tree', { seed: s }, x, 0, z)));
    [[-2.6, -4.2], [2.4, -4.3], [-4, -8.3], [3.2, -8.4]].forEach(([x, z], i) => g.add(prop('bush', { seed: i + 2 }, x, 0, z, 0, 0.8)));
    hills(g, ['#9DB48A', '#8FA87E', '#A9BC96']);
    g.userData.anchors = { center: [0, 0, 0], sidewalk: [0, 0, 0], fence: [0, 0, -3.5], gate: [0, 0, -3.5], path: [0, 0, -5.5], house: [-0.6, 0, -10], door: [0, 0, -7.9], mailbox: [1.5, 0, -3.1] };
    g.userData.lighting = 'day'; return g;
  },
  savannah(o) {
    const g = grp(), r = rng(o.seed || 8); sky(g, ['#93B1BE', '#DCD8C2']); clouds(g, 5, 5);
    g.add(ground(P.sand));
    for (let i = -6; i <= 6; i++) for (let j = 0; j < 10; j++) if (r() < 0.45) { const m = mesh(new THREE.CircleGeometry(1 + r() * 2.2, 7).rotateX(-PI / 2), mat(r() < 0.7 ? P.sandDark : '#D3B67C')); m.scale.z = 0.5 + r() * 0.4; m.position.set(i * 8 + (r() - 0.5) * 4, 0.006, 6 - j * 8 + (r() - 0.5) * 4); m.rotation.y = r() * PI; m.castShadow = false; g.add(m); }
    [[-4.6, -6, 11, 1], [6.5, -11, 12, 1.1], [-12, -20, 13, 1.2], [16, -28, 14, 1.3], [-3, -38, 15, 1.4], [28, -45, 16, 1.5]].forEach(([x, z, s, k]) => g.add(prop('acaciaTree', { seed: s }, x, 0, z, 0, k)));
    for (let i = 0; i < 26; i++) { const x = (r() - 0.5) * 40, z = 3 - r() * 30; if (Math.hypot(x, z) < 3) continue; const t = grp(); for (let k = 0; k < 4; k++) t.add(at(box(0.04, 0.3 + r() * 0.2, 0.02, '#A39A5C', { pivot: 'bottom', taper: { x: 0.2, z: 1 } }), (k - 1.5) * 0.05, 0, 0, 0, 0, (k - 1.5) * 0.3)); t.position.set(x, 0, z); t.rotation.y = r() * PI; g.add(t); }
    [[3.4, -1.6, 0.35], [4.0, -2.2, 0.22], [-5.5, -2.5, 0.5], [9, -6, 0.7]].forEach(([x, z, s]) => g.add(at(rock(s, P.greyDark, r), x, 0, z)));
    // distant mesas + hazy far range
    [[-60, -70, 34, 7, '#B79F74'], [25, -80, 44, 5, '#B79F74'], [70, -65, 30, 8, '#AF9871']].forEach(([x, z, w, h, c]) => g.add(at(box(w, h, 10, c, { pivot: 'bottom', taper: { x: 0.75, z: 0.7 } }), x, 0, z)));
    hills(g, ['#A9B2A8', '#B4BBAE'], { seed: 9, z0: -110, z1: -130, sx: 30, sy: 7 });
    g.userData.anchors = { center: [0, 0, 0], tree: [-4.6, 0, -6], rock: [3.4, 0, -1.6], farTree: [6.5, 0, -11], horizon: [0, 0, -60] };
    g.userData.lighting = 'savannah'; return g;
  },
  courtroom(o) {
    const g = grp(), { back } = room(g, { wall: '#F3EFE6', floor: '#B98A5A', back: -4.6 });
    g.add(flat(2.2, 18, o.runner || P.red, 0, 0.004, 4.4));
    [-6.2, -4.4, -2.6, 2.6, 4.4, 6.2].forEach((x, i) => { const c = i % 2 ? P.teal : P.red; g.add(at(box(0.8, 5.2, 0.12, c, { outline: 0.004 }), x, 3.1, back + 0.07), at(box(0.8, 0.5, 0.12, c, { taper: { x: 0.02, z: 1 } }), x, 0.25, back + 0.07, 0, 0, PI), at(cyl(0.22, 0.22, 0.03, P.cream, 10), x, 4.6, back + 0.15, PI / 2)); });
    g.add(prop('courtBench', {}, 0, 0, back + 1.2), prop('signBoard', { text: o.sign || 'TRIBUNAL', bg: P.navy, fg: P.cream, w: 2.6, h: 0.6, posts: false, height: 0, frame: P.yellow }, 0, 3.0, back + 0.04));
    const sy = 4.25; // seal above the sign (kept off the actor's head line)
    g.add(at(cyl(0.38, 0.38, 0.04, P.yellow, 14), 0, sy, back + 0.03, PI / 2), at(cyl(0.3, 0.3, 0.04, P.cream, 14), 0, sy, back + 0.05, PI / 2), at(box(0.06, 0.32, 0.02, P.navy), 0, sy, back + 0.075), at(box(0.34, 0.04, 0.02, P.navy), 0, sy + 0.1, back + 0.075));
    // witness stand + long white desks with chairs
    g.add(at(box(0.9, 1.05, 0.9, P.teal, { pivot: 'bottom', outline: 0.006 }), 2.5, 0, back + 1.25), at(box(1.0, 0.06, 1.0, P.wood), 2.5, 1.08, back + 1.25));
    [-3.3, 3.3].forEach(x => { g.add(at(box(2.4, 0.06, 0.7, P.white, { outline: 0.006 }), x, 0.76, 0.3), at(box(2.4, 0.72, 0.05, P.white), x, 0.37, -0.03), at(box(0.06, 0.73, 0.65, P.white, { pivot: 'bottom' }), x - 1.17, 0, 0.3), at(box(0.06, 0.73, 0.65, P.white, { pivot: 'bottom' }), x + 1.17, 0, 0.3));
      g.add(prop('chair', { color: P.navy }, x - 0.55, 0, 1.0, PI), prop('chair', { color: P.navy }, x + 0.55, 0, 1.0, PI), prop('documents', {}, x + 0.3, 0.79, 0.3)); });
    g.userData.anchors = { center: [0, 0, 0], judge: [0, 0.3, back + 0.25], bench: [0, 0, back + 1.2], witness: [2.5, 0, back + 1.25], deskLeft: [-3.3, 0, 1.0], deskRight: [3.3, 0, 1.0], sign: [0, 3.3, back] };
    g.userData.lighting = 'interior'; return g;
  },
  replicaStreet(o = {}) { // the "tornado" reference street: dashed road along Z (x -10.5..-1.5), sidewalks, lawns, picket fences and rows of
    // pastel 2-storey townhouses on both sides (near side +X facing -X, far side -X facing +X), trees, green hills, soft sky
    const g = grp(), r = rng(o.seed || 7);
    sky(g, o.sky || ['#8FC2DF', '#D6E9F0']); clouds(g, 5, 9);
    g.add(ground(o.groundColor || '#93BC6A'));
    const FF = o.farFenceX ?? -13.05, FW = -10.5 - FF;                                  // far sidewalk: from the curb (x -10.5) out to the far fence
    g.add(flat(9, 400, '#6E6E72', -6, 0.004, 0), flat(4.5, 400, '#E4D6BE', 0.75, 0.006, 0), flat(FW, 400, '#E4D6BE', -10.5 - FW / 2, 0.006, 0));
    g.add(at(box(0.2, 0.16, 400, '#D9CDB4'), -1.5, 0.0, 0), at(box(0.2, 0.16, 400, '#D9CDB4'), -10.5, 0.0, 0));
    const dash = []; for (let z = -190; z <= 190; z += 4) dash.push([-6, 0.008, z]);
    g.add(inst(new THREE.BoxGeometry(0.16, 0.01, 1.8), mat('#F4F1E8'), dash));
    const cols = o.houseColors || ['#F2F0EA', '#B9A6D6', '#F2D06B', '#9EC7E8', '#F2B8C6', '#D9604C'], roofs = ['#3A4152', '#3A4152', '#7A3A2A', '#3A4152', '#B5302A', '#3A4152'];
    const z0 = o.z0 ?? -60, n = o.n ?? 22, step = o.near === 'cottage' ? 7.2 : 5.6;
    const NC = [{ color: '#F4F2EC', roof: '#C9473A', eaves: true, door: '#2F7F8C', shutters: '#E3B33A', porchRoof: '#C9473A', w: 7.0 }, { color: '#B8A6D9', roof: '#6A3A30', door: '#B5302A', w: 5.6 },
      { color: '#E8A08A', roof: '#3E4A5E', door: '#2F5E8C', w: 5.6 }, { color: '#EDCF7A', roof: '#B5402F', w: 5.8 }, { color: '#F0C6CF', roof: '#5E83C6', w: 5.8 }, { color: '#A9C7E8', roof: '#B5402F', eaves: true, w: 6.0 }];
    for (let i = 0; i < n; i++) {
      const z = z0 + i * step;
      if (o.near === 'cottage') { const c = (o.nearTown || []).includes(i) ? null : NC[i % NC.length];
        if (c) g.add(prop('cottage', { w: c.w || 6.4, d: 8, h: 2.6, rh: 1.5, yard: 3.6, ...c }, 10.9, 0, z, -PI / 2));
        else g.add(prop('townhouse', { color: '#F2F0EA', roof: '#3A4152', door: '#2F5E8C', frame: '#2F5E9C', shutter: '#F2F0EA' }, 7.4, 0, z, -PI / 2)); }
      else g.add(prop('townhouse', { color: cols[i % 6], roof: roofs[i % 6], door: i % 3 ? '#B5302A' : '#2F5E8C' }, 7.4, 0, z, -PI / 2));
      g.add(prop('townhouse', { color: cols[(i + 3) % 6], roof: roofs[(i + 3) % 6], door: i % 2 ? '#24324A' : '#F2D06B' }, o.farX ?? -21.2, 0, z + 2.8, PI / 2));
      if (i % 2 === 0) { g.add(prop('tree', { seed: i + 3 }, 4.2, 0, z + 2.6, 0, 0.9 + r() * 0.3)); g.add(prop('tree', { seed: i + 40 }, (o.farX ?? -21.2) + 3.9, 0, z + 0.4, 0, 0.9 + r() * 0.3)); }
    }
    g.add(prop('fence', { length: 400, height: 0.85, color: P.white }, 2.6, 0, 0, PI / 2), prop('fence', { length: 400, height: 0.85, color: P.white }, FF, 0, 0, PI / 2));
    // hills all around the horizon
    const hc = ['#9DB48A', '#8FA87E', '#A9BC96', '#86A271'];
    for (let i = 0; i < 18; i++) { const a = i / 18 * TAU + r() * 0.2, d = 95 + r() * 30, m = sphere(1, hc[i % 4], 1);
      m.scale.set(26 * (0.7 + r() * 0.6), 7 * (0.6 + r() * 0.7), 14); m.position.set(Math.cos(a) * d, -1, Math.sin(a) * d); m.rotation.y = -a + PI / 2; m.castShadow = false; g.add(m); }
    g.userData.anchors = { center: [0, 0, 0], sidewalk: [0, 0, 0], road: [-6, 0, 0], farSidewalk: [-11.75, 0, 0] };
    g.userData.lighting = 'day'; return g;
  },
  runway(o = {}) { // airbase runway along Z: concrete strip with white centre dashes and edge lines, grass, distant hills, hazy sky
    const g = grp(), r = rng(o.seed || 11);
    sky(g, o.sky || ['#5EADE0', '#A7D4EC']); clouds(g, 8, 6);
    g.add(ground('#9DBB7A'), flat(46, 400, o.concrete || '#BEBEB9', 0, 0.004, 0), flat(46.5, 400, '#B0B0AA', 0, 0.002, 0));
    const dash = []; for (let z = -190; z <= 190; z += 12) dash.push([0, 0.008, z]);
    g.add(inst(new THREE.BoxGeometry(0.6, 0.01, 6), mat('#F4F1E8'), dash), at(box(0.4, 0.01, 400, '#F4F1E8'), -21, 0.007, 0), at(box(0.4, 0.01, 400, '#F4F1E8'), 21, 0.007, 0));
    const hc = ['#9DB48A', '#8FA87E', '#A9BC96'];
    for (let i = 0; i < 14; i++) { const a = i / 14 * TAU, d = 130 + r() * 30, m = sphere(1, hc[i % 3], 1); m.scale.set(30, 8 * (0.6 + r() * 0.6), 16); m.position.set(Math.cos(a) * d, -1, Math.sin(a) * d); m.castShadow = false; g.add(m); }
    g.add(at(box(14, 6, 10, '#B8BEC4', { pivot: 'bottom' }), -40, 0, -60), at(box(9, 4, 8, '#A8AEB4', { pivot: 'bottom' }), -55, 0, -45));      // hangars
    g.userData.anchors = { center: [0, 0, 0] }; g.userData.lighting = 'day'; return g;
  },
  // --- "tornado" replica, act 2 -----------------------------------------------------------------------------------
  skyHigh(o = {}) { // above the clouds: blue sky centred on the camera and a deck of cumulus tops at y = 0
    const g = grp(); skyFollow(g, o.sky || ['#5AA8DE', '#9ACDEB'], 3000, o.below || '#DCE5EA');
    if (o.layer !== false) g.add(prop('cloudLayer', { w: o.w || 1400, d: o.d || 1400, n: o.n || 420, h: o.h || 36, seed: o.seed || 5, color: o.cloudColor }, o.cx || 0, 0, o.cz || 0));
    Object.assign(g.userData, { lighting: 'aerial', near: 0.5, far: 5000, fog: o.fog === false ? null : { color: o.fogColor || '#BFDCEF', near: o.fogNear || 500, far: o.fogFar || 2200 }, anchors: { center: [0, 0, 0] } });
    return g;
  },
  aerialSuburb(o = {}) { // the strike seen from ~150 m: an endless grid of small gabled houses (instanced), lawns, streets, round trees, haze
    const g = grp(), r = rng(o.seed || 13);
    skyFollow(g, o.sky || ['#6BB4E3', '#BFDCEB'], 3000, o.haze || '#C3D5D2');
    g.add(flat(9000, 9000, o.lawn || '#8EC07A', 0, 0, 0));
    const K = o.houseScale || 1, X = o.x || 720, Z0 = o.z0 ?? -2300, Z1 = o.z1 ?? 500, hx = (o.pitch || 14) * K, pair = (o.pair || 50) * K, blockN = o.block || 7;
    const walls = [], wallC = [], roofs = [], roofC = [], trees = [], treeC = [], roads = [], wins = [];
    const WC = o.walls || ['#F4F1EA', '#EFE2C4', '#F0C6CF', '#EDCF7A', '#C3B2DE', '#A9C7E8', '#F2F0EA', '#E6D8C2', '#E8B9A8'];
    const RC = o.roofs || ['#D9675C', '#E58A84', '#5E83C6', '#A0604E', '#D9675C', '#7A8FB8', '#C85A50', '#8C5446', '#6F8AC8'];
    const TC = ['#3F7A45', '#4E8A4A', '#5A9450', '#3A6E44'];
    for (let z = Z0; z < Z1; z += pair) {
      roads.push([0, 0.03, z + 12.5 * K, 0, 0, 0, 2 * X, 0.06, 7 * K]);
      for (let x = -X; x < X; x += hx) {
        if (Math.floor((x + X) / hx) % (blockN + 1) === blockN) continue;
        for (const [dz0, face] of [[0, 1], [-(o.back || 21), -1]]) {
          if (r() < 0.04) continue;
          const dz = dz0 * K, w = (8 + r() * 1.6) * K, d = (7 + r() * 1.2) * K, h = (3.3 + r() * 0.7) * K * (o.wallH || 1), cx = x + (r() - 0.5) * 1.2 * K, cz = z + dz + (r() - 0.5) * 0.8 * K;
          walls.push([cx, 0, cz, 0, 0, 0, w, h, d]); wallC.push(WC[Math.floor(r() * WC.length)]);
          roofs.push([cx, h - 0.05, cz, 0, 0, 0, w + 0.9 * K, (2.5 + r() * 0.7) * K, d + 1.2 * K]); roofC.push(RC[Math.floor(r() * RC.length)]);
          wins.push([cx - w * 0.25, h * 0.5, cz + face * (d / 2 + 0.05), 0, 0, 0, 1.3 * K, 1.2 * K, 0.1], [cx + w * 0.25, h * 0.5, cz + face * (d / 2 + 0.05), 0, 0, 0, 1.3 * K, 1.2 * K, 0.1]);
          if (r() < 0.6) { const s = (2.2 + r() * 1.6) * K; trees.push([cx + (r() - 0.5) * 12 * K, s * 0.9, cz + face * (5.5 + r() * 3.5) * K, r() * 3, r() * 3, r() * 3, s, s * 0.95, s]); treeC.push(TC[Math.floor(r() * 4)]); }
        }
      }
    }
    for (let x = -X; x < X; x += hx * (blockN + 1)) roads.push([x + hx * blockN, 0.035, (Z0 + Z1) / 2, 0, 0, 0, 7 * K, 0.06, Z1 - Z0]);
    const roofGeo = (() => { const s = new THREE.Shape([new THREE.Vector2(-0.5, 0), new THREE.Vector2(0.5, 0), new THREE.Vector2(0, 1)]); const geo = new THREE.ExtrudeGeometry(s, { depth: 1, bevelEnabled: false }); geo.translate(0, 0, -0.5); geo.rotateY(PI / 2); return geo; })();
    const unitBox = new THREE.BoxGeometry(1, 1, 1).translate(0, 0.5, 0), white = mat('#FFFFFF');
    const grid = grp(inst(unitBox, white, walls, wallC), inst(roofGeo, white, roofs, roofC), inst(new THREE.BoxGeometry(1, 1, 1), mat(o.road || '#A7A6A6'), roads), inst(new THREE.BoxGeometry(1, 1, 1), mat('#3E5872'), wins),
      inst(new THREE.IcosahedronGeometry(1, 0), white, trees, treeC));
    grid.children.forEach(c => { c.frustumCulled = false; }); grid.rotation.y = o.gridRot || 0; g.add(grid);
    Object.assign(g.userData, { lighting: 'aerial', near: 1, far: 5000, fog: { color: o.haze || '#C3D5D2', near: o.fogNear || 90, far: o.fogFar || 1050 }, anchors: { center: [0, 0, 0] } });
    return g;
  },
  cottageStreet(o = {}) { // S11: street-level view across a road at single-storey pastel cottages behind a picket fence (road along X)
    const g = grp(), r = rng(o.seed || 17);
    sky(g, o.sky || ['#86C0DF', '#C6E3EF']); clouds(g, 6, 8);
    g.add(ground(o.lawn || '#8DBB5E'), flat(400, 9, o.roadColor || '#7E828C', 0, 0.004, 4.5), flat(400, 2.6, '#EEDDBD', 0, 0.12, -1.3), flat(400, 3, '#EEDDBD', 0, 0.12, 10.5));
    g.add(at(box(400, 0.16, 0.22, '#D7C9AC'), 0, 0.04, 0), at(box(400, 0.16, 0.22, '#D7C9AC'), 0, 0.04, 9));
    const fz = -2.9; g.add(prop('fence', { length: 400, height: 1.05, color: '#F6F4EE', rail: '#F6F4EE' }, 0, 0, fz));
    const spec = o.houses || [
      { x: -7.2, color: '#F4F2EC', roof: '#C9473A', eaves: true, door: '#2F7F8C', shutters: '#E3B33A', porchRoof: '#C9473A' },
      { x: 1.6, color: '#B8A6D9', roof: '#6A3A30', door: '#B5302A' },
      { x: 9.6, color: '#E8A08A', roof: '#3E4A5E', door: '#2F5E8C' },
      { x: -15.4, color: '#F0C6CF', roof: '#5E83C6', eaves: true, porchRoof: '#5E83C6' },
      { x: 17.6, color: '#EDCF7A', roof: '#B5402F' }, { x: -23.6, color: '#A9C7E8', roof: '#B5402F' }, { x: 25.6, color: '#F4F2EC', roof: '#3E4A5E', eaves: true }];
    spec.forEach(h => { g.add(prop('cottage', { w: 6.8, d: 8, h: 2.6, rh: 1.5, ...h }, h.x, 0, o.houseZ ?? -9.2)); });
    for (let i = 0; i < 14; i++) g.add(prop('tree', { seed: i + 5 }, -60 + i * 9 + r() * 3, 0, -17 - r() * 6, 0, 1.4 + r() * 0.6));
    [-3.4, 5.6, 13.5, -11.2].forEach((x, i) => g.add(prop('bush', { seed: i + 3 }, x, 0, fz - 0.9, 0, 0.9)));
    g.add(prop('mailbox', {}, -9.6, 0, fz + 0.4));
    const hc = ['#9DB48A', '#8FA87E', '#A9BC96'];
    for (let i = 0; i < 12; i++) { const a = PI + 0.15 + i / 11 * (PI - 0.3), d = 120 + r() * 25, m = sphere(1, hc[i % 3], 1); m.scale.set(30, 9 * (0.6 + r() * 0.6), 16); m.position.set(Math.cos(a) * d, -1, Math.sin(a) * d); m.castShadow = false; g.add(m); }
    Object.assign(g.userData, { lighting: 'day', anchors: { center: [0, 0, 0], road: [0, 0, 4.5] } });
    return g;
  },
  cottageRows(o = {}) { // S12/S13: rows of pastel cottages facing +Z with front paths and flower beds, a field and green hills behind;
    // o.burnt: the same streets as charred shells under a grey sky (fires and smoke are scene props: flameField / smokeField)
    const g = grp(), r = rng(o.seed || 19), B = !!o.burnt;
    skyFollow(g, o.sky || (B ? ['#8E8073', '#B5A898'] : ['#9FD0E6', '#D3EAF0']), 3000, B ? '#7A6E64' : '#C9E0E6');
    g.add(flat(9000, 9000, o.field || (B ? '#4D4640' : '#97BE63'), 0, 0, 0));
    const rows = o.rows || 10, perRow = o.perRow || 15, px = o.pitch || 10.5, pz = o.rowPitch || 23, houses = grp();
    const WC = o.walls || ['#F4EED8', '#EFC7C7', '#B9DDB0', '#F2D58A', '#F2B49A', '#C9DDF0', '#F4F2EC', '#E6CDE6'], RC = o.roofs || ['#B5402F', '#6A3A30', '#4E5E7E', '#B5402F', '#7A3A2A', '#5E83C6'];
    for (let j = 0; j < rows; j++) {
      const z = -j * pz;
      houses.add(at(box(perRow * px + 40, 0.05, 1.6, B ? '#6B645E' : '#E8E6E0'), 0, 0.03, z + 12.2));                           // sidewalk
      if (!B) houses.add(at(box(perRow * px + 40, 0.03, 4.5, '#8DB75A'), 0, 0.015, z + 15.2));
      for (let i = 0; i < perRow; i++) {
        const x = (i - (perRow - 1) / 2) * px + (j % 2 ? px * 0.35 : 0) + (r() - 0.5) * 0.6, c = WC[Math.floor(r() * WC.length)], rf = RC[Math.floor(r() * RC.length)];
        const hb = prop('cottage', { w: 6.6, d: 7.2, h: 3.0, eaves: !!o.eaves, porch: o.porch ?? !o.eaves, overhang: o.overhang, color: B ? ['#5E5853', '#56504B', '#625B55'][i % 3] : c, roof: rf, door: ['#2F7F8C', '#B5302A', '#3E6E3E', '#E3B33A'][Math.floor(r() * 4)], yard: 7, burnt: B, seed: j * 31 + i, flowers: ['#D9405A', '#B04FC8', '#E86A3A'][i % 3] }, x, 0, z, 0, o.houseScale || 1);
        houses.add(hb);
        if (!B && r() < 0.35) houses.add(prop('tree', { seed: j * 17 + i, color: '#4E8A4A' }, x + px / 2, 0, z - 2 - r() * 4, 0, 1.6 + r() * 0.8));
        if (B && r() < 0.3) houses.add(prop('burntTree', { seed: j * 17 + i, h: 5 + r() * 2 }, x + px / 2, 0, z - 2 - r() * 4));
      }
    }
    const merged = mergeStatic(houses); g.add(merged);
    const hc = B ? ['#6E5F55', '#5A4C43', '#7C6C60'] : ['#A9C9A0', '#9DBE94', '#B4D2AA'];
    for (let i = 0; i < 9; i++) { const m = sphere(1, hc[i % 3], 1); m.scale.set(260 + r() * 140, (40 + r() * 35) * (B ? 1.1 : 1), 120); m.position.set(-900 + i * 230 + (r() - 0.5) * 80, -8, -650 - r() * 300); m.castShadow = false; g.add(m); }
    if (B) for (let i = 0; i < 6; i++) { const m = sphere(1, '#3C322C', 1); m.scale.set(300, 30 + r() * 20, 80); m.position.set(-700 + i * 280, -6, -420 - r() * 60); m.castShadow = false; g.add(m); }
    Object.assign(g.userData, { lighting: B ? 'ruins' : 'day', near: 0.5, far: 5000, fog: { color: B ? '#8C8074' : '#C2DCE4', near: o.fogNear || 120, far: o.fogFar || 1300 }, anchors: { center: [0, 0, 0] } });
    return g;
  },
  ruinedStreet(o = {}) { // S14: after the strike, street level along a dark road (along Z): charred shells, fires, dead trees, grey sky
    const g = grp(), r = rng(o.seed || 23);
    skyFollow(g, o.sky || ['#6E6966', '#7C7672'], 3000, '#5E5854');
    g.add(flat(9000, 9000, o.ground || '#4A433D', 0, 0, 0), flat(9, 2000, o.road || '#2C2B30', 0, 0.06, 0), flat(3, 2000, '#5F5955', -6, 0.13, 0), flat(3, 2000, '#5F5955', 6, 0.13, 0));
    g.add(at(box(0.22, 0.16, 2000, '#55504C'), -4.5, 0.05, 0), at(box(0.22, 0.16, 2000, '#55504C'), 4.5, 0.05, 0));
    const dash = []; for (let z = -900; z <= 100; z += 9) dash.push([0, 0.12, z]); g.add(inst(new THREE.BoxGeometry(0.22, 0.01, 3.2), mat('#E8E6E0'), dash));   // well above the road plane: 1 cm offsets z-fight in the headless renderer
    const shells = grp(), flames = [], smoke = [];
    for (let i = 0; i < 40; i++) for (const s of [-1, 1]) {
      const z = 20 - i * 12 + (s > 0 ? 6 : 0) + (r() - 0.5) * 2;
      shells.add(prop('cottage', { w: 7, d: 8, h: 3.2, burnt: true, seed: i * 7 + (s > 0 ? 3 : 0) }, s * (15 + r() * 2), 0, z, s > 0 ? -PI / 2 : PI / 2));
      if (r() < 0.75) flames.push([s * (14 + r() * 3), 0.2 + r() * 1.5, z + (r() - 0.5) * 4, (1.4 + r() * 1.6) * (o.flameScale || 1)]);
      if (i % 2 === 0) shells.add(prop('burntTree', { seed: i * 3 + (s > 0 ? 1 : 0), h: 5.5 + r() * 2.5 }, s * (8.2 + r() * 0.6), 0, z + 3));
      if (i % 3 === 1) shells.add(prop('streetLamp', {}, s * 7.6, 0, z - 2, s > 0 ? -PI / 2 : PI / 2));
      if (r() < 0.12 && i > 4) smoke.push([s * (16 + r() * 6), z, 20 + r() * 14]);
    }
    shells.add(prop('fence', { length: 2000, height: 1.0, color: '#2A2726', rail: '#2A2726' }, -9.2, 0, 0, PI / 2), prop('fence', { length: 2000, height: 1.0, color: '#2A2726', rail: '#2A2726' }, 9.2, 0, 0, PI / 2));
    g.add(mergeStatic(shells));
    const fl = prop('flameField', { points: flames, seed: 5 }); g.add(fl); const sm = prop('smokeField', { points: smoke, size: 2.2, seed: 7 }); g.add(sm);
    const hc = ['#77706B', '#6C645F', '#827A73'];
    for (let i = 0; i < 12; i++) { const a = i / 12 * TAU, d = 700 + r() * 200, m = sphere(1, hc[i % 3], 1); m.scale.set(300, 40 + r() * 30, 160); m.position.set(Math.cos(a) * d, -8, Math.sin(a) * d); m.castShadow = false; g.add(m); }
    g.userData.update = t => { fl.userData.update(t); sm.userData.update(t); };
    Object.assign(g.userData, { lighting: 'ruins', near: 0.2, far: 5000, fog: { color: '#6E6966', near: 60, far: 900 }, anchors: { center: [0, 0, 0] } });
    return g;
  },
  replicaCourt(o = {}) { // S15/S16: white courtroom with navy/teal wall bands; the dock near the camera end (z = 0) and the judge's bench at
    // z = -14: cream bench, navy high-backed chair with gold studs and finials, a gold-framed nameplate (o.handle), a red pillar, a pale window
    const g = grp(), W = '#EEEBE4';
    g.add(flat(300, 300, '#DCD6CA'), wall(60, 9, 0.3, W, 0, 4.5, -16), wall(0.3, 9, 60, W, -12, 4.5, 0), wall(0.3, 9, 60, W, 12, 4.5, 0), wall(60, 9, 0.3, W, 0, 4.5, 30));
    const band = (y, h, c) => { g.add(wall(24, h, 0.05, c, 0, y, -15.83), wall(0.05, h, 46, c, -11.83, y, 7), wall(0.05, h, 46, c, 11.83, y, 7)); };
    band(6.3, 0.35, '#1F2D4E'); band(4.5, 0.25, '#1F2D4E'); band(3.9, 0.14, '#3E7F86');
    g.add(wall(5, 1.5, 0.06, '#C2342A', 6.5, 0.75, -15.8), wall(0.06, 1.5, 12, '#C2342A', 11.8, 0.75, -9));                  // red wainscot panels
    g.add(at(box(2.2, 3.4, 0.05, '#A9D3E6'), o.windowX ?? -6.5, 3.2, -15.82), at(box(2.4, 3.6, 0.04, '#F7F6F2'), o.windowX ?? -6.5, 3.2, -15.84));         // window
    // judge's bench
    const bz = -13, cz = -14.6, CW = o.chairW || 1.9, CH = o.chairH || 3.2, cx = o.chairX || 0;
    g.add(at(box(4.4, 1.12, 1.2, '#EDE7DA', { pivot: 'bottom', outline: 0.003, emissive: o.benchGlow }), 0, 0, bz), at(box(4.6, 0.06, 1.4, '#F4F0E6', { emissive: o.benchGlow }), 0, 1.15, bz));
    g.add(at(box(CW, CH, 0.25, '#1F2D4E', { pivot: 'bottom', outline: 0.003 }), cx, 0, cz));
    const studs = []; for (let i = 0; i < 4; i++) for (let j = 0; j < 6; j++) studs.push([cx + (-0.6 + i * 0.4 + (j % 2) * 0.2) * CW / 1.9, 1.1 + j * 0.32 * CH / 3.2, cz + 0.14]);
    g.add(inst(new THREE.BoxGeometry(0.045, 0.045, 0.02), mat('#D6A43A'), studs));
    [-1, 1].forEach(s => g.add(at(box(0.16, 0.22, 0.16, '#D6A43A'), cx + s * (CW / 2 - 0.03), CH + 0.1, cz)));
    const plate = canvasPlane(1.5, 0.36, (c, Wc, Hc) => { c.fillStyle = '#D6A43A'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#1B2747'; c.fillRect(Wc * 0.03, Hc * 0.12, Wc * 0.94, Hc * 0.76);
      c.fillStyle = '#F2EEE2'; c.font = `bold italic ${Hc * 0.36}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.handle || '', Wc / 2, Hc / 2); }, { res: 512 });
    plate.position.set(cx, o.plateY ?? CH - 0.65, cz + 0.135); plate.rotation.z = 0.06; plate.scale.setScalar(Math.min(1, CW / 1.7)); g.add(plate);
    g.add(at(box(0.5, 4.5, 0.3, '#C2342A', { pivot: 'bottom' }), 0, 3.0, -15.6));                                                  // red pillar
    Object.assign(g.userData, { lighting: 'interior', anchors: { center: [0, 0, 0], judge: [0, 0, -14.0], bench: [0, 1.15, bz], dock: [0, 0, 0] } });
    return g;
  },
  grassland(o = {}) { // S17-S22: open green field, a bank of cumulus all round the horizon, scattered low-poly trees, blue sky
    const g = grp(), r = rng(o.seed || 29);
    skyFollow(g, o.sky || ['#86C3E6', '#CFE7F1'], 3000, '#D8E8E8');
    const field = flat(9000, 9000, o.grass || '#86BE5C', 0, 0, 0); field.renderOrder = -2; g.add(field);   // drawn first: a road strip is painted over it (props_elan.js: roadStrip)
    for (let i = 0; i < (o.clouds ?? 40); i++) { const a = i / (o.clouds ?? 40) * TAU + r() * 0.12, d = (o.cloudR || 650) * (0.85 + r() * 0.35);
      g.add(prop('cumulus', { w: 150 + r() * 120, h: 55 + r() * 35, n: 22, seed: i + 3 }, Math.cos(a) * d, -8, Math.sin(a) * d)); }
    // (story 56, pass 3) o.treeColors [main, top, side]: snowy trees in winter (the summer greens stayed on a snowed-in field)
    const tcs = o.treeColors || ['#4E8A4A'];
    for (let i = 0; i < 26; i++) { const a = r() * TAU, d = 60 + r() * 240; g.add(prop('tree', { seed: i + 9, color: tcs[0], ...(tcs[1] ? { color2: tcs[1] } : {}), ...(tcs[2] ? { color3: tcs[2] } : {}) }, Math.cos(a) * d, 0, Math.sin(a) * d, 0, 2.2 + r() * 1.6)); }
    Object.assign(g.userData, { lighting: 'day', near: 0.1, far: 5000, fog: { color: '#CFE3E6', near: 300, far: 2400 }, anchors: { center: [0, 0, 0] } });
    return g;
  },
  street(o) { return streetSet(o, false); },
  streetNight(o) { return streetSet(o, true); },
  fair(o) {
    const g = grp(); sky(g); clouds(g, 6);
    g.add(ground('#93B07C'), flat(4, 30, P.cream, 0, 0.005, 16));
    hills(g, ['#8FAE7A', '#7FA06C', '#9DB88A'], { seed: 4, z0: -30, z1: -55, sx: 18, sy: 5 }); hills(g, ['#A9BCA0'], { seed: 7, z0: -90, z1: -110, sx: 30, sy: 8 });
    const bz = -5.6;
    [-3.6, 3.6].forEach(x => g.add(at(cyl(0.1, 0.12, 5.4, P.woodDark, 6, { pivot: 'bottom' }), x, 0, bz)));
    g.add(at(box(6.7, 1.2, 0.06, P.navy), 0, 3.6, bz - 0.04), at(label(o.banner || 'FOIRE AUX ANIMAUX', 6.5, 1.0, { bg: P.cream, fg: P.red, wrap: false }), 0, 3.6, bz));
    g.add(bunting([-3.6, 5.3, bz], [3.6, 5.3, bz], 0.45), bunting([-3.6, 5.2, bz], [-9, 3.4, -3], 0.5), bunting([3.6, 5.2, bz], [9, 3.4, -3], 0.5));
    // red display platform
    g.add(at(box(3.2, 0.36, 1.8, P.red, { pivot: 'bottom', outline: 0.006 }), 0, 0, -3.4), at(box(3.3, 0.05, 1.9, P.cream), 0, 0.385, -3.4), at(box(1.0, 0.18, 0.4, P.redDark, { pivot: 'bottom' }), 0, 0, -2.3));
    // striped tents
    [[-6.8, -6, P.red], [6.8, -6.5, P.teal]].forEach(([x, z, c]) => { g.add(at(box(3, 2, 3, P.cream, { pivot: 'bottom' }), x, 0, z));
      for (let i = 0; i < 8; i++) g.add(at(mesh(new THREE.ConeGeometry(2.5, 1.6, 1, 1, false, i * TAU / 8, TAU / 8), mat(i % 2 ? c : P.cream)), x, 2.8, z));
      g.add(at(box(1.0, 1.4, 0.02, P.navy), x, 0.7, z + 1.51)); });
    g.add(prop('fence', { length: 3, color: P.white }, -4.6, 0, -1.2, 0.4), prop('fence', { length: 3 }, 4.6, 0, -1.2, -0.4), prop('signBoard', { text: 'ENTRÉE', w: 1.0, h: 0.4, height: 1.1, bg: P.yellow, fg: P.navy }, -3.0, 0, 1.5, 0.4));
    g.userData.anchors = { center: [0, 0, 0], platform: [0, 0.41, -3.4], banner: [0, 3.6, bz], tentLeft: [-6.8, 0, -4.2], tentRight: [6.8, 0, -4.7], penLeft: [-4.6, 0, -1.2], penRight: [4.6, 0, -1.2] };
    g.userData.lighting = 'day'; return g;
  },
  prisonCell(o) {
    const g = grp(), back = -3, fz = 2.6, hw = 3.2, Wc = '#93A9A4';
    g.add(flat(300, 300, '#9A9E98'), wall(2 * hw + 0.4, 7, 0.2, Wc, 0, 3.5, back - 0.1), wall(2 * hw, 1.0, 0.04, '#6F8C88', 0, 0.5, back + 0.02));
    [-1, 1].forEach(s => g.add(wall(0.2, 7, 14, Wc, s * (hw + 0.1), 3.5, back + 7), wall(0.04, 1.0, fz - back, '#6F8C88', s * (hw - 0.02), 0.5, (fz + back) / 2)));
    if (o.bars !== false) g.add(prop('jailBars', { width: 2 * hw, height: 2.6 }, 0, 0, fz), wall(2 * hw + 0.4, 4.4, 0.2, Wc, 0, 2.6 + 2.2, fz));
    // bunk bed
    const bx = 2.0, bz = back + 0.45;
    [[-0.95, -0.38], [0.95, -0.38], [-0.95, 0.38], [0.95, 0.38]].forEach(([x, z]) => g.add(at(box(0.06, 1.9, 0.06, P.greyDark, { pivot: 'bottom' }), bx + x, 0, bz + z)));
    [0.45, 1.45].forEach(y => g.add(at(box(2.0, 0.08, 0.8, P.greyDark), bx, y, bz), at(box(1.9, 0.14, 0.72, P.white), bx, y + 0.11, bz), at(box(1.2, 0.15, 0.74, '#E07A2E'), bx + 0.35, y + 0.12, bz), at(box(0.4, 0.1, 0.5, P.paper), bx - 0.7, y + 0.23, bz)));
    // high barred window
    g.add(at(box(0.8, 0.6, 0.02, o.dark ? '#2A3A55' : P.sky, o.dark ? {} : { emissive: '#3A4A50' }), -0.6, 2.45, back + 0.01), at(box(0.92, 0.72, 0.03, P.greyDark), -0.6, 2.45, back + 0.005));
    for (let i = 0; i < 4; i++) g.add(at(cyl(0.02, 0.02, 0.6, P.ink, 5), -0.9 + i * 0.2, 2.45, back + 0.04));
    g.add(prop('toilet', {}, -2.5, 0, back + 0.45), at(box(0.5, 0.05, 0.35, P.grey), -1.5, 0.8, back + 0.18));
    g.userData.anchors = { center: [0, 0, 0], bunk: [bx, 0.6, bz], bunkTop: [bx, 1.6, bz], window: [-0.6, 2.45, back], bars: [0, 0, fz], outside: [0, 0, fz + 1.5], toilet: [-2.5, 0, back + 0.45] };
    g.userData.lighting = o.dark ? 'dark' : 'interior'; return g;
  },
  rooftopPowerLine(o) {
    const g = grp(), night = !!o.night, r = rng(12);
    if (night) nightSky(g, [35, 40, -120]); else { sky(g); clouds(g, 9, 6); }
    const roof = at(box(16, 0.4, 18, '#B8B3A6', { pivot: 'top' }), 0, 0, 2); tileUV(roof.geometry, 3);
    g.add(roof, at(box(16.2, 12, 18.2, P.creamDark, { pivot: 'top' }), 0, -0.4, 2), flat(400, 400, '#8E928C', 0, -12.4, 0));
    [-1, 1].forEach(s => g.add(at(box(0.3, 0.5, 18, P.creamDark, { pivot: 'bottom' }), s * 7.85, 0, 2)));
    g.add(at(box(16, 0.5, 0.3, P.creamDark, { pivot: 'bottom' }), 0, 0, -6.85));
    // neighbouring building wall with teal windows
    g.add(at(box(14, 18, 1, P.cream, { pivot: 'top' }), 0, 4.6, -8.2), at(box(14.2, 0.25, 1.2, P.navy), 0, 4.65, -8.2));
    g.children.slice(-2).forEach(m => m.castShadow = false);
    [-3.5, 1.5, 5.5].forEach(x => g.add(prop('window', { w: 1.1, h: 1.2, color: P.teal, lit: night && x !== -3.5 }, x, 1.2, -7.7)));
    g.add(prop('powerLine', { length: 12.4, height: 3.2 }, 0, 0, -1.5));
    // rooftop clutter: AC unit, vent pipe, water tank
    g.add(at(box(1.2, 0.8, 0.9, P.grey, { pivot: 'bottom', outline: 0.01 }), -4.6, 0, -4.8), at(cyl(0.3, 0.3, 0.05, P.greyDark, 10), -4.6, 0.82, -4.8), at(cyl(0.12, 0.12, 1.2, P.greyDark, 8, { pivot: 'bottom' }), 4.8, 0, -5.2), at(cyl(0.2, 0.15, 0.2, P.greyDark, 8), 4.8, 1.25, -5.2));
    // skyline far below / around
    for (let i = 0; i < 18; i++) { const x = (i / 17 - 0.5) * 120 + (r() - 0.5) * 6, h = 4 + r() * 14, w = 5 + r() * 6, z = -25 - r() * 25;
      if (Math.abs(x) < 9) continue; g.add(at(box(w, h + 12, 5, [P.creamDark, P.tealPale, P.greyDark, P.cream][i % 4], { pivot: 'bottom' }), x, -12.4, z)); }
    g.userData.anchors = { center: [0, 0, 0], wire: [0, 3.2, -1.5], wireLeft: [-6.2, 3.55, -1.5], wireRight: [6.2, 3.55, -1.5], edge: [0, 0, -6.6], wall: [0, 0, -7.7], window: [1.5, 1.2, -7.7] };
    g.userData.lighting = night ? 'night' : 'day'; return g;
  },
  supermarket(o = {}) {   // (cycle 10) o.fr: French signs and a euro till (the defaults are the old English ones); o.signs [[text, bg, fg, x, z], ...] to choose them
    const g = grp(), { back } = room(g, { wall: P.paper, band: P.red, bandH: 0.35, trim: P.navy, floor: '#E9E4D6', back: -4 });
    const lines = []; for (let i = -20; i <= 20; i++) lines.push([i * 0.8, 0.003, 4], [0, 0.003, back + i * 0.8 + 16, 0, PI / 2]);
    g.add(inst(new THREE.BoxGeometry(0.02, 0.002, 40), mat('#CFC8B4'), lines.map(l => l.length > 3 ? [l[0], l[1], l[2], 0, PI / 2, 0, 1, 1, 1] : l)));
    const SH = o.fr ? grocerShelf : shelf;   // (cycle 10) French: grocery stock
    g.add(at(SH(9, 3), 0, 0, back + 0.35), at(SH(6, 4), -4.2, 0, 0.5, 0, PI / 2), at(SH(6, 5), -6.0, 0, 0.5, 0, -PI / 2));
    // checkout counter with register + conveyor
    g.add(at(box(0.8, 0.9, 2.4, P.teal, { pivot: 'bottom', outline: 0.006 }), 3.6, 0, -0.6), at(box(0.62, 0.03, 2.2, P.ink), 3.6, 0.915, -0.6), prop('cashRegister', o.fr ? { text: '0,00 €' } : {}, 3.6, 0.93, 0.3, -PI / 2));
    if (o.fr) g.add(at(box(0.05, 0.06, 2.2, '#9AA1A8'), 3.29, 0.93, -0.6), at(box(0.05, 0.06, 2.2, '#9AA1A8'), 3.91, 0.93, -0.6), at(box(0.6, 0.05, 0.05, '#C9CDD3', { outline: 0.004 }), 3.6, 0.955, -1.55));   // (cycle 10) the belt's steel frame and a divider bar
    g.add(prop('shoppingCart', {}, -2.6, 0, -2.4, 0.5));
    (o.signs || (o.fr ? [['PROMOTIONS', P.red, P.white, -1.3, -3.0], ['RAYON 3', P.navy, P.white, 1.3, -2.6]] : [['PROMO -50%', P.red, P.white, -1.3, -3.0], ['AISLE 3', P.navy, P.white, 1.3, -2.6]])).forEach(([t, bg, fg, x, z]) => { g.add(prop('signBoard', { text: t, bg, fg, w: 1.3, h: 0.42, posts: false, height: 0, frame: bg }, x, 2.75, z), rod([x - 0.5, 3.2, z], [x - 0.5, 7, z], 0.01, P.ink), rod([x + 0.5, 3.2, z], [x + 0.5, 7, z], 0.01, P.ink)); });
    g.userData.anchors = { center: [0, 0, 0], shelf: [0, 0, back + 1.1], aisle: [-5.1, 0, 0.5], checkout: [3.0, 0, -0.6], register: [3.6, 0.93, 0.3], cart: [-2.6, 0, -2.4] };
    g.userData.lighting = 'interior'; return g;
  },
  beach() {
    const g = grp(); sky(g, ['#86B0C2', '#DCE6E0']); clouds(g, 11, 6);
    const r = rng(14);
    g.add(ground('#DCC48E'), flat(340, 1.6, '#C7AE78', 0, 0.006, -7.4), flat(340, 160, P.teal, 0, 0.012, -88.2));
    const foam = flat(340, 0.35, P.white, 0, 0.016, -8.25), band = flat(340, 1.4, P.tealLight, 0, 0.014, -8.9);
    const waves = [-16, -25, -38, -55].map((z, i) => { const m = flat(340, 0.4 + i * 0.2, P.tealLight, 0, 0.015, z); g.add(m); return m; });
    g.add(foam, band);
    const umb = prop('umbrella', { radius: 1.4, height: 2.2, colors: [P.red, P.cream] }, -2.1, 0, -2.8); umb.rotation.z = 0.1;
    g.add(umb, prop('carpet', { w: 0.95, d: 1.9, color: P.teal, inner: P.cream }, -2.6, 0, -1.6, 0.15), at(palm(2), 5.5, 0, -5), at(palm(3), 7.2, 0, -7.5));
    // little sand castle
    const castle = grp(at(box(0.7, 0.3, 0.5, P.sandDark, { pivot: 'bottom' }), 0, 0, 0)); [[-0.3, -0.2], [0.3, -0.2], [-0.3, 0.2], [0.3, 0.2]].forEach(([x, z]) => castle.add(at(cyl(0.1, 0.12, 0.45, P.sandDark, 6, { pivot: 'bottom' }), x, 0, z), at(new THREE.Mesh(new THREE.ConeGeometry(0.12, 0.15, 6), mat(P.sand)), x, 0.52, z)));
    castle.add(at(box(0.01, 0.2, 0.01, P.ink), 0.3, 0.68, 0.2), at(box(0.1, 0.06, 0.005, P.red), 0.35, 0.74, 0.2)); g.add(at(castle, 2.0, 0, -2.6));
    [[-7, -5, 0.8], [-8.2, -6, 0.5], [9, -3, 0.6]].forEach(([x, z, s]) => g.add(at(rock(s, P.greyDark, r), x, 0, z)));
    g.userData.update = t => { foam.position.z = -8.25 + Math.sin(t * 1.1) * 0.25; band.position.z = -8.9 + Math.sin(t * 1.1 - 0.4) * 0.15; waves.forEach((w, i) => w.position.z = [-16, -25, -38, -55][i] + Math.sin(t * 0.7 + i) * 0.6); };
    g.userData.anchors = { center: [0, 0, 0], umbrella: [-2.1, 0, -2.8], towel: [-2.6, 0.03, -1.6], sea: [0, 0, -9], shore: [0, 0, -7.5], castle: [2.0, 0, -2.6], palm: [5.5, 0, -5] };
    g.userData.lighting = 'day'; return g;
  },
  hospital(o = {}) {   // (story 53, final pass) o.monitor === false: no heart monitor on its stand; o.cross === false: no red cross on the wall (an osteopath's room)
    const g = grp(), { back } = room(g, { wall: '#F4F4EE', band: P.tealPale, bandH: 1.1, trim: P.teal, floor: '#DCE3DD' });
    g.add(prop('bed', { blanket: P.tealLight }, -2.5, 0, back + 1.15));
    g.add(at(grp(cyl(0.2, 0.22, 0.05, P.greyDark, 6, { pivot: 'bottom' }), at(cyl(0.02, 0.02, 2.0, P.grey, 6, { pivot: 'bottom' }), 0, 0.05, 0), at(box(0.4, 0.02, 0.02, P.grey), 0, 2.02, 0), at(box(0.18, 0.28, 0.06, '#CFE6E8', { opacity: 0.7 }), 0.15, 1.82, 0), rod([0.15, 1.68, 0], [0.4, 0.8, 0.4], 0.006, P.white)), -3.9, 0, back + 0.9));
    if (o.monitor !== false) {
      const mon = canvasPlane(0.5, 0.34, (c, W, H) => { c.fillStyle = '#10201E'; c.fillRect(0, 0, W, H); c.strokeStyle = LCDc; c.lineWidth = 6; c.beginPath(); c.moveTo(0, H * 0.6); [0.3, 0.36, 0.4, 0.45, 0.5, 1].forEach((k, i) => c.lineTo(W * k, H * [0.6, 0.6, 0.15, 0.85, 0.6, 0.6][i])); c.stroke(); c.fillStyle = LCDc; c.font = `bold ${H * 0.2}px Arial`; c.fillText('72', W * 0.75, H * 0.3); }, { res: 256, emissive: 0.6 });
      g.add(at(grp(cyl(0.04, 0.04, 1.3, P.grey, 6, { pivot: 'bottom' }), cyl(0.2, 0.22, 0.05, P.greyDark, 6, { pivot: 'bottom' }), at(box(0.58, 0.42, 0.12, P.greyDark, { outline: 0.02 }), 0, 1.45, 0), at(mon, 0, 1.45, 0.062)), -1.0, 0, back + 0.45));
    }
    // curtain on a rail
    g.add(rod([1.7, 2.35, back], [1.7, 2.35, -1.2], 0.02, P.grey));
    for (let i = 0; i < 7; i++) g.add(at(box(0.04, 2.0, 0.36, i % 2 ? P.tealLight : '#8DBDB5'), 1.7 + (i % 2 ? 0.06 : -0.06), 1.33, back + 0.2 + i * 0.32, 0, i % 2 ? 0.35 : -0.35, 0));
    g.add(prop('window', { w: 1.3, h: 1.3, color: P.teal }, 3.6, 1.0, back));
    if (o.cross !== false) g.add(at(box(0.6, 0.6, 0.02, P.white), 0.6, 2.5, back + 0.01), at(box(0.42, 0.12, 0.03, P.red), 0.6, 2.5, back + 0.03), at(box(0.12, 0.42, 0.03, P.red), 0.6, 2.5, back + 0.03));
    g.userData.anchors = { center: [0, 0, 0], bed: [-2.5, 0, back + 1.15], bedLie: [-2.5, 0.62, back + 1.15], bedSide: [-1.4, 0, back + 1.4], monitor: [-1.0, 0, back + 0.45], iv: [-3.9, 0, back + 0.9], curtain: [1.7, 0, -2.0], window: [3.6, 1.0, back] };
    g.userData.lighting = 'interior'; return g;
  },
  restaurant(o) { // fried-chicken fast food — viz3d pass from real counter-service layouts: service counter with tills and tray stack,
                  // backlit menu boards, steel fryers with golden baskets + heat lamps behind, drinks fridge, chicken mascot, dining tables
    const g = grp(), { back } = room(g, { wall: '#F3E6D3', band: '#B5302A', bandH: 1.0, trim: '#7A1E18', floor: '#C9B79C' });
    const cloth = checkerMat(P.red, P.white);
    const table = (x, z, chairs = true) => { const t = at(grp(prop('table', { w: 0.9, d: 0.9, h: 0.76, color: P.white }), at(new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.25, 1.0), cloth), 0, 0.665, 0),
        at(cyl(0.12, 0.12, 0.012, P.white, 10), -0.2, 0.8, 0.15), at(cyl(0.12, 0.12, 0.012, P.white, 10), 0.2, 0.8, -0.15), at(cyl(0.04, 0.045, 0.28, P.navy, 6, { pivot: 'bottom' }), 0, 0.795, 0), at(cyl(0.02, 0.02, 0.05, P.red, 6, { pivot: 'bottom' }), 0, 1.07, 0)), x, 0, z);
      if (chairs) t.add(prop('chair', { color: P.navy }, -0.75, 0, 0, PI / 2), prop('chair', { color: P.navy }, 0.75, 0, 0, -PI / 2)); return t; };
    g.add(table(0, -2.6), table(-3.6, -0.6), table(3.6, -1.6), table(-3.4, 2.2), table(3.4, 2.4));
    [[0, -2.6], [3.6, -1.6]].forEach(([x, z]) => g.add(hangLamp(x, 3.1, z, P.red)));
    // service counter (left half of the back wall): red front, yellow stripe, steel top, two tills, tray stack, napkin box
    const cx = -3.4, cz = back + 1.15;
    g.add(at(box(3.6, 1.0, 0.6, '#B5302A', { pivot: 'bottom', outline: 0.006 }), cx, 0, cz), at(box(3.7, 0.06, 0.7, '#D8D8D4'), cx, 1.03, cz), at(box(3.6, 0.12, 0.02, '#F2C230'), cx, 0.62, cz + 0.31));
    g.add(prop('cashRegister', {}, -4.5, 1.06, cz), prop('cashRegister', {}, -2.6, 1.06, cz), at(box(0.42, 0.22, 0.32, '#7A1E18'), -1.85, 1.17, cz), at(box(0.16, 0.14, 0.12, '#F2EDE4'), -3.5, 1.13, cz + 0.12));
    // kitchen line behind the counter: steel back counter, two fryers with golden baskets, heat lamps
    g.add(at(box(3.6, 0.95, 0.6, '#C9CDCF', { pivot: 'bottom', outline: 0.006 }), cx, 0, back + 0.35));
    [-4.6, -3.8].forEach(x => g.add(at(box(0.7, 0.22, 0.5, '#A9AEB0', { outline: 0.004 }), x, 1.06, back + 0.35), at(box(0.28, 0.08, 0.24, '#E0A840'), x - 0.16, 1.21, back + 0.35), at(box(0.28, 0.08, 0.24, '#E0A840'), x + 0.16, 1.21, back + 0.35)));
    [-2.9, -2.2].forEach(x => g.add(rod([x, 2.2, back + 0.4], [x, 1.75, back + 0.4], 0.008, P.ink), at(box(0.5, 0.08, 0.3, '#3A3A3A'), x, 1.72, back + 0.4), at(box(0.44, 0.02, 0.24, '#FFB25A', { emissive: '#FF8A2A', noGrain: true }), x, 1.67, back + 0.4), at(box(0.5, 0.1, 0.36, '#E0A840'), x, 1.0, back + 0.4)));
    // backlit menu boards above the counter
    const panel = (title, price, kind) => canvasPlane(1.1, 0.66, (c, W, H) => { c.fillStyle = '#1E1A18'; c.fillRect(0, 0, W, H); c.textAlign = 'center';
      c.fillStyle = '#F2C230'; c.font = `bold ${H * 0.15}px Arial`; c.fillText(title, W / 2, H * 0.19);
      if (kind === 0) { c.fillStyle = '#B5302A'; c.beginPath(); c.moveTo(W * 0.37, H * 0.36); c.lineTo(W * 0.63, H * 0.36); c.lineTo(W * 0.59, H * 0.72); c.lineTo(W * 0.41, H * 0.72); c.closePath(); c.fill(); c.fillStyle = '#F2EDE4'; c.fillRect(W * 0.4, H * 0.47, W * 0.2, H * 0.07); }
      c.fillStyle = '#E0A840'; for (let i = 0; i < (kind === 0 ? 4 : 5); i++) { c.beginPath(); c.ellipse(W * (0.39 + i * 0.055), H * (kind === 0 ? 0.33 : 0.5), W * 0.035, H * 0.07, 0.5, 0, TAU); c.fill(); }
      c.fillStyle = '#FFFFFF'; c.font = `bold ${H * 0.14}px Arial`; c.fillText(price, W / 2, H * 0.9); }, { emissive: 0.55 });
    [['SEAU x8', '12,90 €', 0], ['TENDERS', '6,50 €', 1], ['MENU BOX', '9,90 €', 0]].forEach(([t, p, k], i) => g.add(at(box(1.18, 0.74, 0.06, '#2A2522'), -4.6 + i * 1.2, 2.35, back + 0.04), at(panel(t, p, k), -4.6 + i * 1.2, 2.35, back + 0.08)));
    if (o.brand) g.add(at(box(3.7, 0.62, 0.08, '#7A1E18', { outline: 0.006 }), cx, 3.15, back + 0.05), at(label(o.brand, 3.5, 0.5, { bg: '#B5302A', fg: '#FFE7A0', wrap: false }), cx, 3.15, back + 0.1));
    // drinks fridge (glass door, coloured bottles), chicken mascot on a plinth, specials board (menu anchor), door, plants
    const fr = grp(at(box(0.85, 2.0, 0.7, '#B5302A', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(box(0.72, 1.6, 0.02, '#1E2A30'), 0, 1.05, 0.355));
    const bl = [], bc = []; for (let s = 0; s < 4; s++) for (let i = 0; i < 5; i++) { bl.push([-0.28 + i * 0.14, 0.4 + s * 0.38, 0.3, 0, 0, 0, 0.07, 0.22, 0.07]); bc.push(['#E8C04A', '#B5302A', '#3A7A4A', '#F2EDE4', '#2C4A8A'][(i + s) % 5]); }
    fr.add(inst(new THREE.BoxGeometry(1, 1, 1), mat(P.white), bl, bc), at(mesh(new THREE.BoxGeometry(0.72, 1.6, 0.01), glassMat(0.25)), 0, 1.05, 0.37));
    g.add(at(fr, -6.2, 0, back + 0.6));
    const masc = grp(at(box(0.6, 0.6, 0.6, '#7A1E18', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(sphere(0.38, '#F7F3EA', 1), 0, 0.98, 0), at(sphere(0.22, '#F7F3EA', 1), 0, 1.45, 0.12),
      at(box(0.1, 0.08, 0.14, '#E0A840'), 0, 1.42, 0.36), at(box(0.06, 0.16, 0.12, '#C4301E'), 0, 1.7, 0.1), at(cyl(0.16, 0.13, 0.22, '#FFFFFF', 8, { pivot: 'bottom' }), 0, 1.62, 0.08), at(sphere(0.035, P.ink, 0), -0.1, 1.5, 0.31), at(sphere(0.035, P.ink, 0), 0.1, 1.5, 0.31));
    g.add(at(masc, 5.6, 0, back + 1.0, 0, -0.4, 0));
    g.add(at(box(1.4, 1.0, 0.05, P.woodDark, { outline: 0.01 }), 1.4, 1.9, back + 0.03), at(label('MENU\nSOUPE 5€\nPIZZA 9€', 1.28, 0.88, { bg: '#22302D', fg: P.cream }), 1.4, 1.9, back + 0.057));
    g.add(prop('door', { color: P.teal, frame: P.navy }, -0.9, 0, back), at(picture(0.9, 0.7, P.woodDark, 'sea'), 3.4, 2.0, back + 0.03), prop('plant', {}, 6.5, 0, back + 0.5), prop('plant', {}, -6.6, 0, 1.6));
    g.userData.anchors = { center: [0, 0, 0], table: [0, 0, -2.6], tableTop: [0, 0.79, -2.6], chairLeft: [-0.75, 0, -2.6], chairRight: [0.75, 0, -2.6], menu: [1.4, 1.9, back], kitchenDoor: [-0.9, 0, back + 0.6], counter: [cx, 0, cz] };
    g.userData.lighting = 'interior'; return g;
  },
  park() {
    const g = grp(), r = rng(21); sky(g); clouds(g, 12, 7);
    g.add(ground(P.grass));
    g.add(ribbon([[-60, -14], [-25, -5], [-10, -1.2], [0, 0], [10, 1.0], [25, 3], [60, 8]], 2.4, P.cream));
    g.add(prop('bench', {}, 0, 0, -2.4), prop('trashCan', { color: P.teal }, -1.6, 0, -2.6), prop('streetLamp', {}, 3.2, 0, -2.2, PI / 2));
    [[-4.2, -5, 1], [4.8, -6, 2], [-9, -9, 3], [10, -12, 4], [-15, -16, 5], [2, -14, 6], [-6, 4, 7], [7, 5, 8], [18, -20, 9], [-22, -24, 10]].forEach(([x, z, s]) => g.add(prop('tree', { seed: s }, x, 0, z, 0, 1 + r() * 0.3)));
    [[-2.6, -3.6], [2.0, -3.8], [-7, -4], [6.5, -3]].forEach(([x, z], i) => g.add(prop('bush', { seed: i + 30 }, x, 0, z, 0, 0.8 + r() * 0.4)));
    const pond = mesh(new THREE.CircleGeometry(3, 12).rotateX(-PI / 2), mat(P.tealLight)); pond.scale.z = 0.55; pond.position.set(8, 0.008, -8.5); g.add(pond);
    hills(g, ['#8FAE7A', '#9DB88A', '#86A472']);
    g.userData.anchors = { center: [0, 0, 0], path: [0, 0, 0], bench: [0, 0, -2.4], benchSeat: [0, 0.47, -2.4], tree: [-4.2, 0, -5], pond: [8, 0, -8.5], lamp: [3.2, 0, -2.2], trash: [-1.6, 0, -2.6] };
    g.userData.lighting = 'day'; return g;
  },
  bathroom() {
    const g = grp(), back = -3.4, half = 6;
    room(g, { wall: P.cream, floor: P.white, back, half });
    // tiled lower wall: ~0.3 m tiles (u x40, v x5.3 on a 12 x 1.6 m slab)
    const tg = new THREE.BoxGeometry(2 * half, 1.6, 0.03), fl = []; tg.attributes.uv.array.forEach((v, i, a) => { a[i] = i % 2 ? v * 5.3 : v * 40; });
    g.add(at(new THREE.Mesh(tg, tileMat('#BFDCD6', '#F2F2EC')), 0, 0.8, back + 0.015));
    for (let i = -12; i < 12; i++) for (let j = 0; j < 30; j++) if ((i + j) % 2 === 0) fl.push([i * 0.5 + 0.25, 0.003, back + j * 0.5 + 0.25]);
    g.add(inst(new THREE.PlaneGeometry(0.5, 0.5).rotateX(-PI / 2), mat(P.navy), fl));
    g.add(prop('bathtub', {}, -2.4, 0, back + 0.45), prop('toilet', {}, 1.4, 0, back + 0.45));
    // pedestal sink + mirror
    g.add(at(grp(cyl(0.1, 0.14, 0.8, P.white, 8, { pivot: 'bottom' }), at(box(0.6, 0.14, 0.42, P.white, { outline: 0.01 }), 0, 0.85, 0), at(box(0.44, 0.02, 0.28, P.tealLight), 0, 0.92, 0.02), at(cyl(0.02, 0.02, 0.2, P.grey, 6, { pivot: 'bottom' }), 0, 0.92, -0.16), at(box(0.04, 0.03, 0.14, P.grey), 0, 1.11, -0.1)), 3.2, 0, back + 0.25));
    g.add(at(box(0.8, 1.0, 0.04, P.teal, { outline: 0.01 }), 3.2, 1.75, back + 0.04), at(box(0.66, 0.86, 0.01, '#D3E6E6'), 3.2, 1.75, back + 0.065), at(box(0.06, 0.5, 0.005, P.white, { noGrain: true }), 3.0, 1.85, back + 0.072, 0, 0, -0.5));
    g.add(at(box(0.5, 0.7, 0.04, P.red), -0.2, 1.25, back + 0.05), at(box(0.62, 0.04, 0.06, P.grey), -0.2, 1.62, back + 0.05), prop('carpet', { w: 0.9, d: 0.6, color: P.teal, inner: P.white }, -2.2, 0, back + 1.3));
    g.userData.anchors = { center: [0, 0, 0], bathtub: [-2.4, 0, back + 0.45], tubLie: [-2.4, 0.32, back + 0.45], toilet: [1.4, 0, back + 0.45], toiletSeat: [1.4, 0.5, back + 0.6], sink: [3.2, 0, back + 0.25], mirror: [3.2, 1.75, back], sinkFront: [3.2, 0, back + 1.0] };
    g.userData.lighting = 'interior'; return g;
  },
  policeStation() {
    const g = grp(), { back } = room(g, { wall: '#DCE3E6', band: P.navy, bandH: 1.1, trim: P.copBlue, floor: '#A9ADA6' });
    g.add(prop('signBoard', { text: 'POLICE', bg: P.navy, fg: P.white, w: 2.4, h: 0.6, posts: false, height: 0, frame: P.copBlue }, 0, 2.7, back + 0.04));
    const star = new THREE.Shape(); for (let i = 0; i < 10; i++) { const a = i / 10 * TAU + PI / 2, rr = i % 2 ? 0.14 : 0.32; i ? star.lineTo(Math.cos(a) * rr, Math.sin(a) * rr) : star.moveTo(Math.cos(a) * rr, Math.sin(a) * rr); }
    g.add(at(mesh(new THREE.ExtrudeGeometry(star, { depth: 0.04, bevelEnabled: false }), mat(P.yellow)), -1.9, 3.0, back + 0.01), at(mesh(new THREE.ExtrudeGeometry(star, { depth: 0.04, bevelEnabled: false }), mat(P.yellow)), 1.9, 3.0, back + 0.01));
    g.add(prop('desk', { color: P.navyLight }, -2.7, 0, back + 1.5), prop('chair', { color: P.navy }, -2.7, 0, back + 0.8), at(box(0.5, 0.35, 0.05, P.ink, { outline: 0.02 }), -2.9, 1.0, back + 1.3), at(box(0.44, 0.29, 0.01, P.copBlue, { emissive: '#1E3550' }), -2.9, 1.0, back + 1.33), prop('documents', {}, -2.3, 0.76, back + 1.55), prop('mug', {}, -3.3, 0.76, back + 1.6));
    g.add(at(box(1.7, 1.1, 0.04, P.wood, { outline: 0.01 }), 2.1, 1.75, back + 0.02));
    [[1.65, 1.8, -0.06], [2.15, 1.75, 0.05], [2.6, 1.82, -0.03]].forEach(([x, y, rz]) => g.add(at(label('WANTED', 0.34, 0.45, { bg: P.paper, fg: P.red }), x, y, back + 0.045, 0, 0, rz)));
    // holding cell on the right
    g.add(wall(0.2, 2.7, 1.6, P.greyDark, 3.5, 1.35, back + 0.8), prop('jailBars', { width: 3.2, height: 2.6 }, 5.1, 0, back + 1.6), at(box(3.2, 0.3, 0.12, P.navy), 5.1, 2.75, back + 1.6));
    g.add(at(box(0.5, 1.3, 0.6, P.greyDark, { pivot: 'bottom', outline: 0.006 }), -4.6, 0, back + 0.32));
    // viz3d pass: a working station is furnished — lockers, filing cabinets, a water cooler, a coffee corner, a wall clock,
    // tube lights, a notice board with memos, potted plants (nothing in the acting areas: desk front, cell front, centre)
    for (let i = 0; i < 4; i++) { const lk = grp(at(box(0.5, 1.9, 0.5, '#6F8796', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0)); for (let v = 0; v < 3; v++) lk.add(at(box(0.3, 0.02, 0.01, '#2A3640'), 0, 1.6 + v * 0.06, 0.255)); lk.add(at(box(0.03, 0.12, 0.02, P.grey), 0.17, 1.0, 0.26)); g.add(at(lk, -6.75, 0, -0.4 + i * 0.52, 0, PI / 2, 0)); }
    [-5.5, -6.1].forEach(x => { const fc = grp(at(box(0.5, 1.3, 0.6, '#8C949A', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0)); for (let d = 0; d < 3; d++) fc.add(at(box(0.44, 0.38, 0.01, '#9AA2A8'), 0, 0.23 + d * 0.42, 0.305), at(box(0.12, 0.03, 0.03, P.ink), 0, 0.33 + d * 0.42, 0.31)); g.add(at(fc, x, 0, back + 0.32)); });
    g.add(at(grp(at(box(0.36, 1.0, 0.36, '#E8E8E4', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(cyl(0.15, 0.15, 0.42, '#9FD3E8', 10, { pivot: 'bottom', opacity: 0.7 }), 0, 1.0, 0), at(box(0.06, 0.05, 0.06, '#2C4A8A'), 0.08, 0.75, 0.19)), -0.9, 0, back + 0.3));
    g.add(at(box(0.9, 0.85, 0.5, '#5E6B66', { pivot: 'bottom', outline: 0.006 }), 0.4, 0, back + 0.3), prop('coffeeMachine', {}, 0.25, 0.85, back + 0.3), prop('mug', { color: P.white }, 0.62, 0.85, back + 0.35));
    g.add(prop('wallClock', { rate: 1 / 3600 }, -4.0, 2.6, back + 0.03));
    [-3.0, 1.2].forEach(x => g.add(rod([x - 0.7, 3.8, -1.0], [x - 0.7, 3.5, -1.0], 0.006, P.ink), rod([x + 0.7, 3.8, -1.0], [x + 0.7, 3.5, -1.0], 0.006, P.ink), at(box(1.6, 0.06, 0.2, '#FFFFFF', { emissive: '#FFF6DA', noGrain: true }), x, 3.48, -1.0)));
    g.add(at(box(1.1, 0.8, 0.03, '#B98A5A', { outline: 0.006 }), -5.4, 1.8, back + 0.03));
    [[-5.7, 1.95, 0.06], [-5.3, 1.7, -0.04], [-5.05, 1.95, 0.02]].forEach(([x, y, rz], i) => g.add(at(box(0.26, 0.32, 0.01, ['#F7F3EA', '#F2E27A', '#F7F3EA'][i]), x, y, back + 0.05, 0, 0, rz)));
    g.add(prop('plant', {}, -6.5, 0, 2.4), prop('plant', {}, 2.9, 0, back + 0.45));
    g.userData.anchors = { center: [0, 0, 0], desk: [-2.7, 0, back + 1.5], deskChair: [-2.7, 0, back + 0.8], deskFront: [-2.7, 0, back + 2.5], sign: [0, 2.7, back], board: [2.1, 1.75, back], cell: [5.1, 0, back + 0.8], cellFront: [5.1, 0, back + 2.4] };
    g.userData.lighting = 'interior'; return g;
  },
  spaceVoid() {
    const g = grp(); sky(g, ['#070B16', '#18223A']);
    const stars = prop('stars', { radius: 150, count: 1400, seed: 77 }); g.add(stars, prop('moon', { radius: 4 }, -18, 10, -60));
    const planet = grp(sphere(9, P.salmon, 1, { emissive: '#3A1A12' }), at(torus(15, 1.2, P.tealLight, 2, 28, TAU, { emissive: '#1C3330' }), 0, 0, 0, PI / 2 - 0.35, 0, 0.2)); planet.children[1].scale.z = 0.12;
    g.add(at(planet, 40, 22, -120), at(sphere(3, P.teal, 1, { emissive: '#0F2A28' }), -45, 30, -110), at(sphere(1.6, P.yellow, 1, { emissive: '#4A3A10' }), 20, -6, -70));
    g.userData.update = t => { stars.rotation.y = t * 0.01; planet.rotation.y = t * 0.05; };
    g.userData.anchors = { center: [0, 0, 0], planet: [40, 22, -120], moon: [-18, 14, -60] };
    g.userData.lighting = 'dark'; return g;
  },
  whiteVoid(o) {
    const c = o.color || P.cream, g = grp();
    // unlit floor + dome of the same colour = no horizon; a shadow-catcher keeps contact shadows
    g.add(new THREE.Mesh(new THREE.SphereGeometry(180, 16, 8), new THREE.MeshBasicMaterial({ color: c, side: THREE.BackSide })));
    // (cycle 19) the floor 4 mm under y 0: props whose own floors sit at y 0 (a platform, a carriage) fought with it for the same pixels and strobed
    const f = new THREE.Mesh(new THREE.CircleGeometry(170, 24).rotateX(-PI / 2), new THREE.MeshBasicMaterial({ color: c })); f.position.y = -0.004; g.add(f);
    const sh = new THREE.Mesh(new THREE.CircleGeometry(40, 24).rotateX(-PI / 2), new THREE.ShadowMaterial({ opacity: 0.18 })); sh.position.y = 0.002; sh.receiveShadow = true; g.add(sh);
    g.userData.anchors = { center: [0, 0, 0] };
    g.userData.lighting = 'interior'; return g;
  },
  farm() {
    const g = grp(), r = rng(31); sky(g); clouds(g, 15, 6);
    g.add(ground('#9CB27F'));
    // crop field: sand base + green rows
    g.add(flat(18, 24, P.sandDark, 13, 0.006, -18)); for (let i = 0; i < 14; i++) g.add(at(box(0.5, 0.3, 23, i % 2 ? P.green : '#7FA86A', { pivot: 'bottom', taper: { x: 0.4, z: 1 } }), 4.8 + i * 1.25, 0, -18));
    // red barn with gable roof, white X door trim, hay loft
    const barn = grp(box(5, 3.2, 6, P.red, { pivot: 'bottom', outline: 0.004 }), at(box(5.6, 1.9, 6.5, P.greyDark, { taper: { x: 0.02, z: 1 } }), 0, 4.15, 0), at(box(1.9, 2.3, 0.06, P.redDark), 0, 1.15, 3.03));
    [[0, 2.33, 2.0, 0.12], [0, 0.03, 2.0, 0.12]].forEach(([x, y, w, h]) => barn.add(at(box(w, h, 0.08, P.white), x, y + h / 2 - 0.06, 3.05)));
    [-1, 1].forEach(s => barn.add(at(box(0.12, 2.3, 0.08, P.white), s * 0.95, 1.15, 3.05), at(box(0.1, 2.9, 0.07, P.white), 0, 1.15, 3.06, 0, 0, s * 0.68)));
    barn.add(at(box(0.9, 0.7, 0.06, P.white), 0, 3.6, 3.03), at(box(0.7, 0.5, 0.07, P.woodDark), 0, 3.6, 3.04));
    g.add(at(barn, -5, 0, -12), at(cyl(1.1, 1.1, 6.5, P.grey, 10, { pivot: 'bottom', outline: 0.006 }), -9.2, 0, -14), at(sphere(1.1, P.red, 1), -9.2, 6.5, -14));
    // rail fence
    for (let x = -14; x <= 14; x += 2) g.add(at(box(0.12, 1.1, 0.12, P.woodDark, { pivot: 'bottom' }), x, 0, -4));
    [0.45, 0.85].forEach(y => g.add(at(box(28, 0.1, 0.06, P.wood), 0, y, -4.05)));
    [[3.2, -2.8, 0], [4.4, -3.0, 0.2], [3.8, -2.9, 0, 0.8]].forEach(([x, z, ry, y = 0]) => g.add(at(box(1.2, 0.8, 0.8, P.yellow, { pivot: 'bottom', outline: 0.01 }), x, y, z, 0, ry, 0)));
    [[-14, -9, 1], [14, -6, 2], [-18, -18, 3], [22, -30, 4]].forEach(([x, z, s]) => g.add(prop('tree', { seed: s + 40 }, x, 0, z, 0, 1.2 + r() * 0.3)));
    hills(g, ['#9DB48A', '#8FA87E', '#A9BC96'], { seed: 6 });
    g.userData.anchors = { center: [0, 0, 0], barn: [-5, 0, -12], barnDoor: [-5, 0, -8.4], silo: [-9.2, 0, -14], field: [13, 0, -14], fence: [0, 0, -4], hay: [3.8, 0, -2.9] };
    g.userData.lighting = 'day'; return g;
  },
  airport() {
    const g = grp(), back = -5; room(g, { wall: '#E6E9E6', back, noFloor: true, noBack: true });
    sky(g); clouds(g, 17, 5);
    g.add(flat(300, 160, '#C7CBC6', 0, 0, back + 80), flat(300, 160, '#9A9C96', 0, -0.01, back - 80));
    // glazed back wall: navy mullions + transparent panes, solid header above
    for (let x = -7; x <= 7; x += 2) g.add(at(box(0.14, 4.2, 0.14, P.navy, { pivot: 'bottom' }), x, 0, back));
    g.add(at(new THREE.Mesh(new THREE.PlaneGeometry(14, 4.2), glassMat(0.16, '#CFE6EE')), 0, 2.1, back), wall(14.4, 3, 0.2, '#E6E9E6', 0, 5.7, back - 0.1), at(box(14, 0.14, 0.2, P.navy), 0, 4.2, back), at(box(14, 0.12, 0.2, P.navy), 0, 0.06, back));
    // parked plane outside
    const plane = grp(at(cyl(1.3, 1.3, 16, P.white, 10), 0, 0, 0, 0, 0, PI / 2), at(mesh(new THREE.ConeGeometry(1.3, 2.4, 10), mat(P.white)), 9.2, 0, 0, 0, 0, -PI / 2), at(box(4, 0.2, 18, P.white, { taper: { x: 0.5, z: 1 }, taperAxis: 'y' }), 0, -0.4, 0),
      at(box(2.5, 3, 0.2, P.red, { taper: { x: 0.4, z: 1 } }), -7, 2.3, 0), at(box(16, 0.4, 2.62, P.teal), 0, 0, 0));
    g.add(at(plane, 6, 2.6, -28, 0, 0.25, 0));
    // check-in counter
    g.add(at(box(3.2, 1.05, 0.7, P.teal, { pivot: 'bottom', outline: 0.005 }), -3.4, 0, back + 1.8), at(box(3.3, 0.06, 0.8, P.white), -3.4, 1.08, back + 1.8), prop('signBoard', { text: 'CHECK-IN', bg: P.teal, fg: P.white, w: 1.6, h: 0.4, height: 1.8, frame: P.navy }, -3.4, 0, back + 1.4));
    // departure board
    const board = canvasPlane(3.0, 1.3, (c, W, H) => { c.fillStyle = '#141C28'; c.fillRect(0, 0, W, H); c.font = `bold ${H * 0.13}px monospace`; c.fillStyle = P.white; c.fillText('DEPARTURES', W * 0.04, H * 0.17);
      [['PARIS', '10:45', 'ON TIME'], ['TOKYO', '11:20', 'DELAYED'], ['MARS', '12:00', 'CANCELLED'], ['LYON', '12:35', 'BOARDING']].forEach(([a, b, s], i) => { c.fillStyle = '#F2C46B'; c.fillText(a, W * 0.04, H * (0.36 + i * 0.17)); c.fillText(b, W * 0.42, H * (0.36 + i * 0.17)); c.fillStyle = s === 'CANCELLED' ? '#FF6B5A' : s === 'DELAYED' ? '#FFB347' : LCDc; c.fillText(s, W * 0.62, H * (0.36 + i * 0.17)); }); }, { emissive: 0.6 });
    g.add(at(box(3.15, 1.45, 0.12, P.ink), 1.9, 3.3, back + 0.8), at(board, 1.9, 3.3, back + 0.865), rod([1.1, 4.0, back + 0.8], [1.1, 6, back + 0.8], 0.02, P.ink), rod([2.7, 4.0, back + 0.8], [2.7, 6, back + 0.8], 0.02, P.ink));
    // seating rows + luggage
    [0.4, 1.5].forEach(z => { g.add(at(box(3.0, 0.06, 0.1, P.grey), 4.2, 0.3, z)); for (let i = 0; i < 4; i++) g.add(at(box(0.6, 0.08, 0.5, P.navy), 3.1 + i * 0.72, 0.42, z), at(box(0.6, 0.5, 0.08, P.navy), 3.1 + i * 0.72, 0.72, z - 0.25, -0.12)); [-1.3, 1.3].forEach(dx => g.add(at(box(0.08, 0.38, 0.08, P.grey, { pivot: 'bottom' }), 4.2 + dx, 0, z))); });
    [[-1.4, back + 2.6, P.red], [-1.0, back + 2.5, P.teal]].forEach(([x, z, c]) => g.add(at(box(0.42, 0.6, 0.24, c, { pivot: 'bottom', outline: 0.02 }), x, 0.05, z), at(box(0.2, 0.04, 0.04, P.ink), x, 0.72, z)));
    g.userData.anchors = { center: [0, 0, 0], counter: [-3.4, 0, back + 1.8], counterFront: [-3.4, 0, back + 2.7], counterBehind: [-3.4, 0, back + 1.1], board: [1.9, 3.3, back + 0.8], seats: [3.1, 0.45, 0.4], window: [0, 0, back + 0.4], plane: [6, 0, -28] };
    g.userData.lighting = 'interior'; return g;
  },
  zoo(o) { // gorilla habitat — viz3d pass, built from real exhibit layouts: rockwork cliff with the night-house cave,
           // wooden climbing frame (poles, deck, ropes, fire-hose hammock, log ramp), dead climbing tree, hay, logs, worn dirt;
           // visitor promenade with the barrier wall + bars, benches, bins, lamps, hedges and trees behind
    const night = !!o.night, g = grp(), r = rng(41);
    const GR = night ? '#43593E' : P.grass, DIRT = night ? '#4C4438' : '#A88C66';
    const RK = night ? ['#6E6B65', '#5E5B56', '#7A766F'] : ['#A49C8E', '#8F887B', '#B5AD9E'];
    const WOOD = night ? '#5A4634' : '#8A6A4A', WOODD = night ? '#45362A' : '#6A503A', HAY = night ? '#8A7A45' : '#D9BE6A';
    g.add(flat(160, 160, GR, 0, 0, 0));
    [[-5.0, -2.4, 2.1], [3.4, -5.0, 1.9], [0.4, -0.4, 2.4], [-1.8, -4.4, 1.3], [5.4, -1.4, 1.2]].forEach(([x, z, rr], i) => { // worn dirt, 2 cm up
      const d = mesh(new THREE.CircleGeometry(rr, 9).rotateX(-PI / 2), mat(DIRT)); d.scale.set(1 + r() * 0.5, 1, 0.7 + r() * 0.3); d.rotation.y = r() * PI;
      d.position.set(x, 0.02 + i * 0.003, z); d.castShadow = false; g.add(d); });
    // visitor promenade (a 2.5 cm slab, not a coplanar plane) with a kerb at the back
    g.add(at(box(160, 0.025, 8, '#CFC6B2', { pivot: 'bottom', noGrain: false }), 0, 0, 7.5), at(box(160, 0.1, 0.25, '#B4AB98', { pivot: 'bottom' }), 0, 0, 11.4));
    // backdrop: the old big rock mass, pushed back, then a cliff of faceted blocks in front of it (two tiers, ledges)
    const wallM = new THREE.Mesh(new THREE.DodecahedronGeometry(6, 1), mat(RK[1])); wallM.scale.set(3.2, 1.25, 0.8); wallM.position.set(0, 1.5, -13.6); g.add(wallM);
    const block = (x, y, z, sx, sy, sz, c, rx, ry, rz) => { const m = new THREE.Mesh(new THREE.DodecahedronGeometry(1, 0), mat(c)); m.scale.set(sx, sy, sz); m.position.set(x, y, z); m.rotation.set(rx, ry, rz); m.castShadow = m.receiveShadow = true; g.add(m); return m; };
    for (let i = 0; i < 16; i++) {
      const x = -18 + i * 2.4 + (r() - 0.5) * 0.8; if (Math.abs(x - 3.6) < 2.0) continue;   // the cave mouth stays open
      const h = 2.2 + r() * 2.2;
      block(x, h * 0.45, -8.1 - r() * 0.7, 1.5 + r() * 0.6, h * 0.6, 1.3 + r() * 0.4, RK[i % 3], r() * 0.5, r() * PI, r() * 0.3);
      block(x + (r() - 0.5), h + 0.8 + r(), -9.8 - r(), 1.7 + r() * 0.8, 1.5 + r() * 0.9, 1.4, RK[(i + 1) % 3], r() * 0.4, r() * PI, r() * 0.4);
    }
    // the cave = the night-house entrance in the rockwork: dark recess between two jamb rocks under a lintel rock
    block(1.85, 1.35, -7.25, 0.95, 1.7, 1.0, RK[1], 0.2, 0.4, 0.1); block(5.35, 1.45, -7.25, 0.95, 1.8, 1.0, RK[2], 0.1, 1.1, 0.2);
    block(3.6, 3.35, -7.5, 2.3, 0.85, 1.1, RK[0], 0.1, 0.3, 0.05);
    const cave = new THREE.Mesh(new THREE.CircleGeometry(1.25, 10), mat('#0E0E0E', { noGrain: true })); cave.scale.y = 1.25; cave.position.set(3.6, 1.45, -6.9); g.add(cave);
    g.add(at(box(2.6, 3.2, 0.3, '#0E0E0E', { noGrain: true }), 3.6, 1.6, -7.7));
    // trees above / behind the cliff (depth), and two inside the habitat
    [[-14, -12.5, 1.6], [-8, -13.5, 1.9], [-2.5, -14, 1.5], [9, -13, 1.8], [15, -12, 1.5], [12, -15, 2.0]].forEach(([x, z, s], i) => g.add(prop('tree', { seed: 11 + i }, x, 2.0, z, 0, s)));
    g.add(prop('tree', { seed: 4 }, -6.6, 0, -6.2), prop('tree', { seed: 9 }, 7.4, 0, -6.4), prop('bush', { seed: 2 }, -2.2, 0, -2.6), prop('bush', { seed: 5 }, 6.6, 0, 1.6));
    [[-3.6, -3.6, 1.6], [2.2, -2.6, 1.3], [-1.2, -6.0, 1.8], [5.6, -4.6, 1.4]].forEach(([x, z, sz]) => g.add(at(prop('rock', { size: sz, color: RK[2] }), x, 0, z)));
    // wooden climbing frame: four round poles, a deck, top beams, hanging ropes, a fire-hose hammock and a log ramp
    const cf = grp();
    [[-1.0, -0.8], [1.0, -0.8], [-1.0, 0.8], [1.0, 0.8]].forEach(([x, z]) => cf.add(at(cyl(0.11, 0.13, 4.0, WOOD, 7, { pivot: 'bottom', outline: 0.01 }), x, 0, z)));
    cf.add(at(box(2.3, 0.1, 1.9, WOODD, { outline: 0.008 }), 0, 2.1, 0));
    [[-1, -0.8, 1, -0.8], [-1, 0.8, 1, 0.8], [-1, -0.8, -1, 0.8], [1, -0.8, 1, 0.8]].forEach(([x0, z0, x1, z1]) => cf.add(rod([x0, 3.85, z0], [x1, 3.85, z1], 0.07, WOOD)));
    [[-0.5, 0.8], [0.4, 0.8], [0.95, -0.1]].forEach(([x, z], i) => cf.add(rod([x, 3.85, z], [x + 0.08, 1.0 + i * 0.3, z + 0.05], 0.025, '#C9B48A')));
    cf.add(wire(catenary([-1.0, 1.75, -0.8], [-1.0, 1.75, 0.8], 0.45), 0.09, '#9A4A32'));
    cf.add(rod([1.0, 2.1, 0.6], [2.5, 0.08, 1.3], 0.14, WOODD));
    g.add(at(cf, -5.3, 0, -2.7, 0, 0.35, 0));
    // dead climbing tree (bare trunk + three limbs), hay piles, logs
    const dt = grp(at(cyl(0.16, 0.24, 3.4, '#7A6650', 7, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0));
    [[0.6, 2.2, 0.2, 1.1], [-0.7, 2.8, -0.3, 0.9], [0.3, 3.2, -0.6, 0.8]].forEach(([dx, y, dz, l]) => dt.add(rod([0, y - 0.3, 0], [dx * 1.6, y + l * 0.5, dz * 1.6], 0.07, '#7A6650')));
    g.add(at(dt, 6.2, 0, -3.6));
    [[5.9, -1.5, 1.0], [-2.6, -5.0, 0.8], [-6.4, 0.2, 0.7]].forEach(([x, z, s]) => { const h = sphere(0.6 * s, HAY, 0); h.scale.set(1.5, 0.38, 1.15); h.position.set(x, 0.12 * s, z); g.add(h); });
    g.add(rod([-5.8, 0.2, 1.3], [-3.9, 0.2, 1.75], 0.2, WOODD), rod([5.0, 0.18, 0.7], [6.8, 0.18, 0.3], 0.18, WOODD));
    // barrier (low wall + bars) and the visitor side: benches facing the habitat, bins, lamps, hedges, trees
    g.add(at(prop('zooFence', { length: 30 }), 0, 0, 4.2));
    g.add(at(prop('signBoard', { text: o.sign || 'ZOO · GORILLES', bg: P.teal, fg: P.cream, w: 2.4, h: 0.6 }), o.signX ?? -2.5, 0, o.signZ ?? 5.2));
    g.add(prop('bench', {}, -4.9, 0.025, 7.4, PI), prop('bench', {}, 4.7, 0.025, 7.4, PI), prop('trashCan', {}, -6.8, 0.025, 5.0), prop('trashCan', {}, 8.2, 0.025, 5.0));
    [-10, 10].forEach(x => g.add(prop('streetLamp', { on: night, light: night ? 4 : 0 }, x, 0.025, 4.9, PI / 2)));
    for (let x = -14; x <= 14; x += 2.2) g.add(prop('bush', { seed: 20 + Math.round(x) }, x, 0, 12.2, 0, 0.8));
    [[-9, 14.5], [-3, 15.5], [4, 14.8], [11, 15.2]].forEach(([x, z], i) => g.add(prop('tree', { seed: 30 + i }, x, 0, z, 0, 1.4)));
    if (night) nightSky(g); else { sky(g); clouds(g, 5); }
    g.userData.anchors = { center: [0, 0, 0], rock: [2.2, 0, -2.6], behindRock: [2.2, 0, -3.8], cave: [3.6, 0, -6.4], fence: [0, 0, 4.2], visitor: [0, 0, 6.5], tree: [-6, 0, -6], frame: [-5.3, 0, -2.7] };
    g.userData.lighting = night ? 'night' : 'day'; return g;
  },
  secretGym(o) { // the hidden gym under the zoo — viz3d pass: rubber floor, power cage, cable tower, kettlebell rack, plate tree,
                 // protein shelf, lockers, exposed duct + pipes, green LED strips, a training screen (the generic gym stays as is)
    const g = S.gym(), back = -3.6, r = rng(77);
    g.add(at(label(o.sign || 'GORILLA GYM · PRIVÉ', 2.6, 0.5, { bg: P.ink, fg: '#E8FF5A' }), 0.8, 3.4, -3.5));
    g.add(at(box(14, 0.02, 9.2, '#5A5F66', { pivot: 'bottom' }), 0, 0, 1.0));                                   // rubber floor slab (mid grey: dark subjects must read on it)
    const cage = grp(); [[-0.6, -0.5], [0.6, -0.5], [-0.6, 0.5], [0.6, 0.5]].forEach(([x, z]) => cage.add(at(box(0.08, 2.3, 0.08, P.ink, { pivot: 'bottom', outline: 0.01 }), x, 0, z)));
    [[-0.6, -0.5, 0.6, -0.5], [-0.6, 0.5, 0.6, 0.5], [-0.6, -0.5, -0.6, 0.5], [0.6, -0.5, 0.6, 0.5]].forEach(([a, b, c, d]) => cage.add(rod([a, 2.28, b], [c, 2.28, d], 0.03, P.ink)));
    cage.add(rod([-0.95, 1.4, 0.38], [0.95, 1.4, 0.38], 0.016, P.grey)); [-0.82, 0.82].forEach(x => cage.add(at(cyl(0.2, 0.2, 0.05, '#1E1F24', 10), x, 1.4, 0.38, 0, 0, PI / 2)));
    g.add(at(cage, -1.6, 0, -2.75));
    const tower = grp(at(box(0.9, 2.4, 0.1, P.ink, { pivot: 'bottom', outline: 0.01 }), 0, 0, -0.3), at(box(0.36, 1.0, 0.22, '#1E1F24', { pivot: 'bottom' }), 0, 0.05, -0.12),
      at(cyl(0.08, 0.08, 0.04, P.grey, 10), 0, 2.3, 0.0, PI / 2), rod([0, 2.25, 0.02], [0, 1.2, 0.35], 0.006, '#DDDDDD'), at(box(0.25, 0.04, 0.04, P.grey), 0, 1.18, 0.36));
    g.add(at(tower, -5.6, 0, -2.9));
    const kb = grp(at(box(2.6, 0.06, 0.45, P.ink), 0, 0.42, 0), at(box(0.06, 0.42, 0.45, P.ink, { pivot: 'bottom' }), -1.25, 0, 0), at(box(0.06, 0.42, 0.45, P.ink, { pivot: 'bottom' }), 1.25, 0, 0));
    for (let i = 0; i < 7; i++) { const s = 0.11 + i * 0.012; kb.add(at(sphere(s, i % 2 ? '#2B2D33' : P.red, 1), -1.05 + i * 0.35, 0.45 + s, 0), at(torus(s * 0.55, 0.018, '#2B2D33', 4, 10), -1.05 + i * 0.35, 0.45 + s * 2, 0)); }
    g.add(at(kb, 6.45, 0, -1.2, 0, -PI / 2, 0));
    const tree = grp(at(cyl(0.04, 0.05, 1.3, P.ink, 6, { pivot: 'bottom' }), 0, 0, 0), at(cyl(0.3, 0.3, 0.04, P.ink, 8), 0, 0.02, 0));
    [[0.5, 0.18], [0.85, 0.16], [1.15, 0.14]].forEach(([y, rr], i) => [-1, 1].forEach(s => tree.add(at(cyl(rr, rr, 0.05, i % 2 ? P.red : '#1E1F24', 10), s * 0.08, y, 0, 0, 0, PI / 2))));
    g.add(at(tree, 2.5, 0, -3.15));
    const tubs = grp(at(box(0.4, 0.04, 1.8, P.ink), 0, 1.1, 0), at(box(0.4, 0.04, 1.8, P.ink), 0, 1.55, 0));
    for (let i = 0; i < 8; i++) tubs.add(at(cyl(0.09, 0.09, 0.22, ['#1E1F24', '#E8FF5A', P.red, '#2C4A8A'][i % 4], 10, { pivot: 'bottom' }), 0, i < 4 ? 1.12 : 1.57, -0.65 + (i % 4) * 0.43));
    g.add(at(tubs, -6.7, 0, 0.0));
    for (let i = 0; i < 4; i++) { const lk = grp(at(box(0.5, 1.9, 0.5, '#5E6C78', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0)); for (let v = 0; v < 3; v++) lk.add(at(box(0.3, 0.02, 0.01, '#2A3036'), 0, 1.6 + v * 0.06, 0.255)); lk.add(at(box(0.03, 0.12, 0.02, P.grey), 0.17, 1.0, 0.26)); g.add(at(lk, -6.75, 0, 1.4 + i * 0.52, 0, PI / 2, 0)); }
    g.add(at(cyl(0.32, 0.32, 13, '#8E949A', 10), 0, 3.85, -2.2, 0, 0, PI / 2), rod([-6.8, 3.55, -3.3], [6.8, 3.55, -3.3], 0.05, '#B5302A'), rod([-6.8, 3.4, -3.35], [6.8, 3.4, -3.35], 0.04, '#7E868D'));
    [[-6.95, 2.7, 0.4, PI / 2], [6.95, 2.7, 0.4, -PI / 2]].forEach(([x, y, z, ry]) => g.add(at(box(8.5, 0.05, 0.03, '#E8FF5A', { emissive: '#C8E83A', noGrain: true }), x, y, z, 0, ry, 0)));
    const scr = canvasPlane(1.6, 0.9, (c, W, H) => { c.fillStyle = '#0E1116'; c.fillRect(0, 0, W, H); c.fillStyle = '#E8FF5A'; for (let i = 0; i < 9; i++) { const h = H * (0.15 + 0.7 * ((i * 37) % 10) / 10); c.fillRect(W * (0.08 + i * 0.095), H * 0.9 - h, W * 0.06, h); } c.font = `bold ${H * 0.12}px Arial`; c.fillText('BPM 188', W * 0.06, H * 0.16); }, { emissive: 0.6 });
    g.add(at(box(1.7, 1.0, 0.06, P.ink, { outline: 0.006 }), -4.0, 2.35, back + 0.05), at(scr, -4.0, 2.35, back + 0.085));
    g.userData.lighting = 'interior'; return g; // lit like a real gym; the neon strips + screen carry the 'secret' mood
  },
  lab(o) { // the chemist's lab — viz3d pass from clandestine-lab references: stainless worktables with glassware and tubing, a burner,
           // a tray of blue crystals, reactor vat, blue drums, fume hood, chemical shelves, gas cylinders, whiteboard, yellow hazmat suits, tube lights
    const g = grp(), { back } = room(g, { wall: '#A9BDB5', band: '#7E978F', bandH: 1.25, trim: '#3E4A48', floor: '#5E6B66' }), r = rng(5);
    const ST = '#B9C0C2', STD = '#8E9698', GL = { opacity: 0.55 };
    const table = (w, d) => { const t = grp(at(box(w, 0.05, d, ST, { outline: 0.006 }), 0, 0.92, 0), at(box(w - 0.1, 0.03, d - 0.1, STD), 0, 0.3, 0));
      [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([sx, sz]) => t.add(at(box(0.05, 0.9, 0.05, STD, { pivot: 'bottom' }), sx * (w / 2 - 0.06), 0, sz * (d / 2 - 0.06)))); return t; };
    g.add(at(table(2.6, 0.9), 0, 0, back + 1.2), at(table(1.6, 0.8), -3.4, 0, back + 0.55));
    const y0 = 0.945, tz = back + 1.2;
    const flask = (x, z, c, round) => { const f = grp(); if (round) { f.add(at(sphere(0.085, c, 1, GL), 0, 0.085, 0), at(cyl(0.022, 0.022, 0.12, '#DDEFEF', 8, GL), 0, 0.22, 0)); f.add(rod([0.16, 0, 0], [0.16, 0.42, 0], 0.008, STD), at(torus(0.09, 0.006, STD, 4, 12), 0, 0.12, 0, PI / 2)); }
      else f.add(at(cyl(0.022, 0.085, 0.17, c, 8, { ...GL, pivot: 'bottom' }), 0, 0, 0), at(cyl(0.022, 0.022, 0.07, '#DDEFEF', 8, { ...GL, pivot: 'bottom' }), 0, 0.17, 0)); return at(f, x, y0, z); };
    g.add(flask(-0.95, tz - 0.15, '#9FE0D0', true), flask(-0.55, tz + 0.1, '#E8C04A', false), flask(-0.2, tz - 0.2, '#7BC0E8', false), flask(0.6, tz + 0.05, '#C9E8F0', true));
    [0.15, 0.32].forEach((x, i) => g.add(at(cyl(0.06, 0.06, 0.13, '#DDEFEF', 10, { ...GL, pivot: 'bottom' }), x, y0, tz + 0.15), at(cyl(0.052, 0.052, 0.06, i ? '#7FD4F5' : '#E8C04A', 10, { pivot: 'bottom' }), x, y0 + 0.005, tz + 0.15)));
    const rack = grp(at(box(0.3, 0.04, 0.1, '#E7E2D6'), 0, 0.06, 0)); for (let i = 0; i < 5; i++) rack.add(at(cyl(0.012, 0.012, 0.14, ['#9FE0D0', '#E8C04A', '#7BC0E8'][i % 3], 6, { ...GL, pivot: 'bottom' }), -0.12 + i * 0.06, 0.0, 0)); g.add(at(rack, 1.05, y0, tz - 0.2));
    g.add(wire(catenary([-0.95, y0 + 0.33, tz - 0.15], [-0.55, y0 + 0.24, tz + 0.1], 0.12), 0.008, '#E8C96A'), wire(catenary([-0.55, y0 + 0.24, tz + 0.1], [0.6, y0 + 0.34, tz + 0.05], 0.2), 0.008, '#E8C96A'));
    g.add(at(cyl(0.05, 0.06, 0.06, STD, 8, { pivot: 'bottom' }), 0.6, y0, tz + 0.05), at(mesh(new THREE.ConeGeometry(0.03, 0.09, 8), mat('#7FB8FF', { emissive: '#3C7BFF', noGrain: true })), 0.6, y0 + 0.1, tz + 0.05));
    const tray = grp(at(box(0.5, 0.03, 0.32, ST), 0, 0.015, 0)); for (let i = 0; i < 22; i++) tray.add(at(box(0.03 + r() * 0.03, 0.02, 0.02 + r() * 0.03, '#7FD4F5', { emissive: '#3BA8D8', noGrain: true }), (r() - 0.5) * 0.4, 0.035, (r() - 0.5) * 0.22, 0, r() * 3, 0));
    g.add(at(tray, -3.4, y0, back + 0.55));
    const vat = grp(at(cyl(0.55, 0.55, 1.1, ST, 12, { pivot: 'bottom', outline: 0.01 }), 0, 0.35, 0), at(sphere(0.55, ST, 1), 0, 1.45, 0), at(cyl(0.08, 0.08, 0.25, STD, 8, { pivot: 'bottom' }), 0, 1.9, 0), at(cyl(0.09, 0.09, 0.02, '#F2F2F2', 10), 0.4, 1.1, 0.4, PI / 2.6));
    [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([sx, sz]) => vat.add(at(box(0.06, 0.38, 0.06, STD, { pivot: 'bottom' }), sx * 0.4, 0, sz * 0.4)));
    vat.children[1].scale.y = 0.45; vat.add(rod([0, 2.1, 0], [0, 2.1, -0.9], 0.04, STD)); g.add(at(vat, -5.6, 0, back + 1.4));
    [[4.4, back + 0.5], [5.1, back + 0.6], [4.75, back + 1.2]].forEach(([x, z]) => g.add(at(cyl(0.29, 0.29, 0.88, '#2F5FA8', 12, { pivot: 'bottom', outline: 0.008 }), x, 0, z), at(torus(0.29, 0.02, '#244B86', 4, 14), x, 0.3, z, PI / 2), at(torus(0.29, 0.02, '#244B86', 4, 14), x, 0.62, z, PI / 2), at(cyl(0.05, 0.05, 0.02, '#244B86', 8), x + 0.12, 0.89, z)));
    const hood = grp(at(box(1.5, 2.1, 0.85, '#D9DEDD', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(box(1.3, 0.8, 0.02, '#1F2A2A'), 0, 1.35, 0.42), at(mesh(new THREE.BoxGeometry(1.3, 0.8, 0.01), glassMat(0.3)), 0, 1.35, 0.44), at(box(1.2, 0.04, 0.02, '#FFF6DA', { emissive: '#FFF0C0', noGrain: true }), 0, 1.72, 0.43));
    g.add(at(hood, 2.6, 0, back + 0.45));
    const sh = shelf(2.2, 8, 3); g.add(at(sh, -6.75, 0, -0.15, 0, PI / 2, 0));
    [-6.45, -6.05].forEach((x, i) => g.add(at(cyl(0.12, 0.12, 1.45, i ? '#5E7E5E' : '#8E9698', 10, { pivot: 'bottom', outline: 0.008 }), x, 0, back + 0.35), at(sphere(0.12, i ? '#5E7E5E' : '#8E9698', 1), x, 1.45, back + 0.35), at(cyl(0.03, 0.03, 0.12, '#3A3A3A', 6, { pivot: 'bottom' }), x, 1.52, back + 0.35)));
    g.add(rod([-6.6, 1.0, back + 0.2], [-5.9, 1.0, back + 0.2], 0.008, '#C9C9C9'));
    const wb = canvasPlane(1.6, 0.95, (c, W, H) => { c.fillStyle = '#F7F7F2'; c.fillRect(0, 0, W, H); c.strokeStyle = '#2C4A8A'; c.fillStyle = '#2C4A8A'; c.lineWidth = 3; c.font = `${H * 0.11}px Arial`;
      ['C10H15N', 'P2P  →  +H2', '99,1 %', 'T 80°C / 4 h'].forEach((s, i) => c.fillText(s, W * 0.06, H * (0.2 + i * 0.2))); c.beginPath(); c.moveTo(W * 0.62, H * 0.3); for (let i = 0; i < 6; i++) c.lineTo(W * (0.62 + i * 0.06), H * (0.3 + (i % 2) * 0.12)); c.stroke(); c.strokeStyle = '#B5302A'; c.strokeRect(W * 0.6, H * 0.62, W * 0.32, H * 0.22); });
    g.add(at(box(1.7, 1.05, 0.03, '#C9CDCF', { outline: 0.006 }), -2.2, 1.75, back + 0.03), at(wb, -2.2, 1.75, back + 0.05));
    [0.9, 1.55].forEach(x => { const s = grp(at(box(0.5, 0.75, 0.09, '#E8C93A', { outline: 0.006 }), 0, 1.45, 0), at(box(0.2, 0.62, 0.08, '#E8C93A'), -0.13, 0.75, 0), at(box(0.2, 0.62, 0.08, '#E8C93A'), 0.13, 0.75, 0),
        at(box(0.36, 0.36, 0.1, '#E8C93A'), 0, 2.0, 0), at(box(0.22, 0.14, 0.02, '#2A2A2A'), 0, 2.0, 0.06), at(box(0.12, 0.5, 0.08, '#E8C93A'), -0.31, 1.45, 0, 0, 0, 0.15), at(box(0.12, 0.5, 0.08, '#E8C93A'), 0.31, 1.45, 0, 0, 0, -0.15), at(box(0.04, 0.12, 0.04, P.ink), 0, 2.25, -0.03));
      g.add(at(s, x, 0.25, back + 0.08)); });
    [-1.6, 1.6].forEach(x => g.add(rod([x - 0.7, 3.6, -1.2], [x - 0.7, 3.4, -1.2], 0.006, P.ink), rod([x + 0.7, 3.6, -1.2], [x + 0.7, 3.4, -1.2], 0.006, P.ink), at(box(1.6, 0.06, 0.2, '#FFFFFF', { emissive: '#FFF6DA', noGrain: true }), x, 3.38, -1.2)));
    g.add(at(box(0.4, 0.012, 0.4, '#2A2F2E'), 1.8, 0.006, -0.4));
    g.add(at(label('LABO', 1.4, 0.4, { bg: P.yellow, fg: P.ink }), 0, 2.6, back + 0.02));
    g.userData.anchors = { center: [0, 0, 0], table: [0, 0, back + 1.2] }; g.userData.lighting = 'interior'; return g;
  },
  interrogation(o = {}) { // police interrogation room: grey walls, metal table, two chairs, hanging lamp, one-way mirror, door
    const g = grp(), { back } = room(g, { wall: '#5A6066', band: '#474C52', bandH: 1.0, trim: '#2F3338', floor: '#6A6E70', back: -3.2, half: 4.5, front: 6 });
    g.add(at(box(1.5, 0.05, 0.85, '#8C949A', { outline: 0.008 }), 0, 0.76, -0.75));
    [[-0.68, -0.38], [0.68, -0.38], [-0.68, -1.12], [0.68, -1.12]].forEach(([x, z]) => g.add(at(box(0.05, 0.74, 0.05, '#4A4F55', { pivot: 'bottom' }), x, 0, z)));
    g.add(prop('chair', { color: '#3A3F45' }, 0, 0, -1.45), prop('chair', { color: '#3A3F45' }, 0.85, 0, 0.15, PI - 0.4));
    g.add(rod([0, 3.4, -0.75], [0, 2.25, -0.75], 0.008, P.ink), at(mesh(new THREE.ConeGeometry(0.32, 0.26, 12, 1, true), mat('#2C3036', { doubleSide: true })), 0, 2.15, -0.75),
      at(sphere(0.08, '#FFF2C0', 1, { emissive: '#FFE9A0', noGrain: true }), 0, 2.06, -0.75));
    g.add(at(box(0.06, 1.2, 2.6, '#1B2026', { outline: 0.004 }), -4.46, 1.6, -0.6), at(box(0.04, 1.1, 2.5, '#2E3A44', { emissive: '#0A0F14' }), -4.42, 1.6, -0.6));
    g.add(at(prop('door', { color: '#6F7A82' }), 4.45, 0, -1.2, 0, -PI / 2, 0));
    g.add(prop('wallClock', { rate: 1 / 3600 }, 1.8, 2.5, back + 0.03));
    g.add(at(box(1.4, 0.9, 0.03, '#B98A5A', { outline: 0.006 }), -1.9, 1.7, back + 0.03));
    [[-2.25, 1.85, 0.05], [-1.9, 1.6, -0.04], [-1.55, 1.82, 0.03]].forEach(([x, y, rz], i) => g.add(at(box(0.26, 0.34, 0.01, ['#F7F3EA', '#F2E27A', '#F7F3EA'][i]), x, y, back + 0.05, 0, 0, rz)));
    g.add(rod([-2.25, 1.85, back + 0.07], [-1.55, 1.82, back + 0.07], 0.006, P.red));
    g.add(prop('documents', {}, 0.45, 0.785, -0.7), prop('mug', { color: P.white }, -0.5, 0.785, -0.6));
    g.userData.anchors = { center: [0, 0, 0], table: [0, 0.785, -0.75], suspect: [0, 0, -1.45], cop: [0.35, 0, -0.05], mirror: [-4.4, 1.6, -0.6], door: [4.3, 0, -1.2] };
    g.userData.lighting = 'interior'; return g;
  },
  pressRoom(o = {}) { // press conference: backdrop with repeated words (o.backdrop 'A|B|C'), podium with microphones, flags, chairs, cameras
    const g = grp(), { back } = room(g, { wall: o.wall || '#2E4563', band: o.band || '#24384F', bandH: 0.8, trim: o.trim || '#1E2E44', floor: o.floor || '#3A3F45', back: -3.0 });
    const bd = canvasPlane(6.0, 2.6, (c, W, H) => { c.fillStyle = o.bg || '#2E4563'; c.fillRect(0, 0, W, H); c.fillStyle = o.fg || 'rgba(255,255,255,0.85)'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${H * 0.085 * (o.fontScale || 1)}px Arial`;
      const words = String(o.backdrop || 'CONFÉRENCE DE PRESSE').split('|'); for (let r = 0; r < 6; r++) for (let k = 0; k < 4; k++) c.fillText(words[(r * 4 + k) % words.length], W * (0.14 + k * 0.24 + (r % 2) * 0.06), H * (0.1 + r * 0.16)); }, { res: 1024 });
    g.add(at(bd, 0, 1.9, back + 0.02));
    if (o.podium !== false) { g.add(prop('podium', {}, 0, 0, back + 1.0)); [-0.08, 0.08].forEach(x => g.add(rod([x, 1.15, back + 1.05], [x * 1.6, 1.42, back + 0.86], 0.008, P.ink), at(sphere(0.025, P.ink, 0), x * 1.6, 1.43, back + 0.85))); }
    const fc = o.flag || ['#2C4A8A', P.white, P.red], fo = o.flagOpts || { colors: fc }; if (o.flags !== false) g.add(prop('flag', fo, -1.5, 0, back + 0.4), prop('flag', fo, 1.5, 0, back + 0.4));
    if (o.chairs !== false) for (let r = 0; r < 2; r++) for (let i = 0; i < 5; i++) g.add(prop('chair', { color: o.chairColor || '#8C949A' }, -2.4 + i * 1.2, 0, 2.2 + r * 1.1, PI));
    [-3.2, 3.2].forEach(x => g.add(rod([x, 0, 3.9], [x, 1.45, 3.6], 0.015, P.ink), rod([x - 0.25, 0, 3.4], [x, 1.45, 3.6], 0.015, P.ink), rod([x + 0.25, 0, 3.4], [x, 1.45, 3.6], 0.015, P.ink),
      at(box(0.3, 0.22, 0.42, P.ink, { outline: 0.01 }), x, 1.55, 3.55), at(cyl(0.06, 0.06, 0.1, P.greyDark, 8), x, 1.55, 3.3, PI / 2)));
    g.userData.anchors = { center: [0, 0, 0], podium: [0, 0, back + 1.0], speaker: [0, 0, back + 0.55], press: [0, 0, 2.2] };
    g.userData.lighting = 'interior'; return g;
  },
  classroom(o = {}) { // high-school classroom: chalk board (o.board / o.board2), 3x3 student desks with chairs facing it, teacher desk, clock, posters
    const g = grp(), { back } = room(g, { wall: '#E9E1CC', band: '#8FAE9A', bandH: 1.0, trim: '#5C7A66', floor: '#C9A27A' });
    const bb = canvasPlane(3.2, 1.2, (c, W, H) => { c.fillStyle = '#2F4A3A'; c.fillRect(0, 0, W, H); c.fillStyle = 'rgba(240,240,232,0.92)'; c.textAlign = 'left';
      c.font = `bold ${H * 0.2}px Arial`; c.fillText(o.board || 'BAC — JUIN', W * 0.06, H * 0.3); c.font = `${H * 0.13}px Arial`; c.fillText(o.board2 || "Sujet : la bataille d'aura", W * 0.06, H * 0.58); c.fillText(o.board3 || '6 + 7 = 67', W * 0.06, H * 0.82); }, { res: 768 });
    g.add(at(box(3.36, 1.36, 0.05, '#6B4A2E', { outline: 0.006 }), 0, 1.75, back + 0.03), at(bb, 0, 1.75, back + 0.06), at(box(3.2, 0.05, 0.08, '#6B4A2E'), 0, 1.07, back + 0.08));
    g.add(prop('desk', { color: '#7A5C3A', w: 1.4 }, -2.9, 0, back + 1.15, PI), prop('chair', { color: '#5C4330' }, -2.9, 0, back + 0.45));
    for (let r = 0; r < 3; r++) for (let cc = 0; cc < 3; cc++) { const x = -1.6 + cc * 1.6, z = -0.9 + r * 1.35;
      g.add(prop('table', { w: 0.9, d: 0.55, h: 0.72, color: '#C99A62', legs: '#6E726F' }, x, 0, z), prop('chair', { color: '#2F62B5' }, x, 0, z + 0.55, PI)); }
    g.add(prop('wallClock', { rate: 1 / 3600 }, 2.6, 2.7, back + 0.03));
    [[3.4, 1.7, '#F2E27A', 'PARCOURSUP'], [-4.4, 1.8, '#9FC6D4', 'SILENCE']].forEach(([x, y, bg, t]) => g.add(at(label(t, 0.9, 0.5, { bg, fg: P.ink }), x, y, back + 0.03)));
    g.userData.anchors = { center: [0, 0, 0], board: [0, 1.75, back], teacher: [-2.9, 0, back + 0.45], desk: [0, 0, -0.9] };
    g.userData.lighting = 'interior'; return g;
  },
  bar() { // old-school bar: long counter, bottles on shelves, stools, neon sign
    const g = grp(), { back } = room(g, { wall: '#5A3A2E', band: P.red, bandH: 1.0, trim: P.ink, floor: '#3A2A22' });
    g.add(at(box(6, 1.05, 0.7, P.woodDark, { pivot: 'bottom', outline: 0.005 }), 0, 0, back + 1.6), at(box(6.1, 0.06, 0.8, P.wood), 0, 1.08, back + 1.6));
    for (let y of [1.4, 1.9]) { g.add(at(box(5, 0.04, 0.3, P.woodDark), 0, y, back + 0.2)); for (let i = 0; i < 14; i++) g.add(at(cyl(0.04, 0.05, 0.28, ['#2F6B4A', '#8A3A2A', '#C9A86A', '#3A4A6A'][i % 4], 6, { pivot: 'bottom' }), -2.3 + i * 0.35, y + 0.02, back + 0.2)); }
    for (let i = 0; i < 6; i++) g.add(at(prop('barStool'), -2.5 + i * 1.0, 0, back + 2.35));
    g.add(at(label('CHEZ JO', 1.6, 0.45, { bg: P.ink, fg: '#F2A65A' }), 0, 2.6, back + 0.02));
    // viz3d pass (lived-in bar): beer taps, back-bar mirror, hanging lamps, dartboard, jukebox, side tables, posters
    [-0.7, 0, 0.7].forEach((x, i) => g.add(at(box(0.08, 0.32, 0.08, '#C9A86A', { pivot: 'bottom' }), x, 1.11, back + 1.4), at(box(0.06, 0.16, 0.06, ['#B5302A', '#2F6B4A', P.ink][i]), x, 1.5, back + 1.4), rod([x, 1.38, back + 1.4], [x, 1.38, back + 1.5], 0.012, '#C9A86A')));
    g.add(at(box(5.3, 1.15, 0.04, '#3A2A22', { outline: 0.006 }), 0, 1.7, back + 0.04), at(box(5.1, 1.0, 0.02, '#6E7E86'), 0, 1.7, back + 0.07));
    [-2.0, 0, 2.0].forEach(x => g.add(hangLamp(x, 3.0, back + 1.6, '#2F6B4A')));
    g.add(prop('dartboard', {}, 6.95, 1.7, -0.6, -PI / 2));
    const jb = grp(at(box(0.8, 1.2, 0.55, '#8A3A2A', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(cyl(0.4, 0.4, 0.55, '#8A3A2A', 12, { outline: 0.008 }), 0, 1.2, 0, PI / 2), at(box(0.6, 0.35, 0.02, '#F2A65A', { emissive: '#E0802A', noGrain: true }), 0, 0.85, 0.28));
    for (let i = 0; i < 5; i++) jb.add(at(box(0.08, 0.5, 0.02, ['#E8C04A', '#B5302A', '#4A9A7A', '#E8C04A', '#B5302A'][i], { emissive: '#553311' }), -0.24 + i * 0.12, 0.35, 0.28));
    g.add(at(jb, 5.7, 0, back + 0.45));
    [[5.2, 0.6], [5.5, 2.5]].forEach(([x, z]) => g.add(prop('table', { color: P.woodDark, w: 0.7, d: 0.7, h: 0.74 }, x, 0, z), prop('chair', { color: P.ink }, x - 0.6, 0, z, PI / 2), prop('chair', { color: P.ink }, x + 0.6, 0, z, -PI / 2), at(box(0.08, 0.16, 0.08, '#C9A86A', { opacity: 0.8 }), x, 0.82, z)));
    [[3.9, 2.0, '#2F6B4A'], [4.8, 1.9, '#8A3A2A']].forEach(([x, y, c]) => g.add(at(box(0.6, 0.8, 0.03, P.ink, { outline: 0.006 }), x, y, back + 0.03), at(box(0.5, 0.7, 0.01, c), x, y, back + 0.05)));
    g.userData.anchors = { center: [0, 0, 0], counter: [0, 1.11, back + 1.6], behind: [0, 0, back + 1.0], stool: [0, 0, back + 2.35], shelf: [0, 1.6, back + 0.2], sign: [0, 2.6, back] };
    g.userData.lighting = 'dusk'; return g;
  },
  bank() { // marble hall: counter with windows, big vault door, BANQUE sign
    const g = grp(), { back } = room(g, { wall: '#E9E3D6', band: P.teal, bandH: 0.9, trim: P.navy, floor: '#CFC6B2' });
    g.add(at(box(5, 1.1, 0.5, P.teal, { pivot: 'bottom', outline: 0.005 }), -1.2, 0, back + 2.0), at(box(5.1, 0.06, 0.6, P.cream), -1.2, 1.13, back + 2.0));
    for (let i = 0; i < 4; i++) g.add(at(box(0.04, 0.8, 0.04, P.yellow, { pivot: 'bottom' }), -3.4 + i * 1.4, 1.16, back + 2.0));
    g.add(at(prop('vaultDoor'), 2.6, 0, back + 0.2));
    g.add(at(label('BANQUE', 1.8, 0.45, { bg: P.navy, fg: P.yellow }), -1.0, 2.7, back + 0.02));
    // viz3d pass (real banking hall): marble columns, queue stanchions with red ropes, a wall clock, a security camera,
    // an ATM on the side wall, a slip desk, plants — the robbery path (right) and the frozen extras stay clear
    [-5.0, 5.0].forEach(x => g.add(at(cyl(0.34, 0.38, 4.2, '#E2DBCB', 10, { pivot: 'bottom', outline: 0.008 }), x, 0, -0.6), at(box(0.9, 0.2, 0.9, '#CFC6B2', { pivot: 'bottom' }), x, 0, -0.6), at(box(0.85, 0.18, 0.85, '#CFC6B2'), x, 4.1, -0.6)));
    const posts = [-3.9, -3.1, -2.3, -1.5];
    posts.forEach(x => g.add(at(cyl(0.12, 0.14, 0.03, '#C9A86A', 10, { pivot: 'bottom' }), x, 0, -0.55), at(cyl(0.025, 0.025, 0.95, '#C9A86A', 8, { pivot: 'bottom' }), x, 0, -0.55), at(sphere(0.04, '#C9A86A', 1), x, 0.97, -0.55)));
    for (let i = 0; i < posts.length - 1; i++) g.add(wire(catenary([posts[i], 0.9, -0.55], [posts[i + 1], 0.9, -0.55], 0.12), 0.022, P.redDark));
    g.add(prop('wallClock', { rate: 1 / 3600 }, 3.8, 2.9, back + 0.03));
    g.add(at(grp(at(box(0.08, 0.08, 0.3, P.greyDark), 0, 0, 0.15), at(box(0.16, 0.12, 0.26, '#E8E8E4', { outline: 0.006 }), 0, -0.08, 0.36, 0.35, 0, 0), at(cyl(0.035, 0.035, 0.02, P.ink, 8), 0, -0.1, 0.5, PI / 2)), -6.7, 3.3, back + 0.2, 0, 0.6, 0));
    g.add(prop('ATM', {}, -6.75, 0, 1.4, PI / 2));
    g.add(at(box(0.9, 1.05, 0.5, '#7A6650', { pivot: 'bottom', outline: 0.006 }), 4.7, 0, 1.8), at(box(1.0, 0.04, 0.6, '#E2DBCB'), 4.7, 1.07, 1.8), at(box(0.25, 0.02, 0.18, P.white), 4.6, 1.1, 1.8, 0, 0.3, 0));
    g.add(prop('plant', {}, -6.3, 0, back + 0.5), prop('plant', {}, 6.3, 0, back + 0.6));
    g.userData.anchors = { center: [0, 0, 0], counter: [-1.2, 0, back + 2.0], teller: [-1.2, 0, back + 1.5], vault: [2.6, 0, back + 0.6], sign: [-1.0, 2.7, back], door: [0, 0, 4] };
    g.userData.lighting = 'interior'; return g;
  },
  gym() {
    const g = grp(), { back } = room(g, { wall: P.cream, band: P.red, bandH: 1.2, trim: P.navy, floor: '#C08D5A' });
    g.add(at(box(4.2, 2.0, 0.04, P.woodDark), 0.8, 1.35, back + 0.03), at(box(4.0, 1.85, 0.01, '#D3E3E3'), 0.8, 1.35, back + 0.055), at(box(0.08, 1.2, 0.005, P.white, { noGrain: true }), -0.4, 1.5, back + 0.062, 0, 0, -0.5), at(box(0.04, 0.8, 0.005, P.white, { noGrain: true }), -0.2, 1.4, back + 0.062, 0, 0, -0.5));
    g.add(at(label('NO PAIN NO GAIN', 2.2, 0.5, { bg: P.navy, fg: P.yellow }), 0.8, 2.85, back + 0.02));
    // dumbbell rack
    const rack = grp(at(box(1.6, 0.06, 0.45, P.ink), 0, 0.5, 0), at(box(1.6, 0.06, 0.45, P.ink), 0, 0.9, 0.05), at(box(0.06, 1.0, 0.06, P.ink, { pivot: 'bottom' }), -0.78, 0, 0), at(box(0.06, 1.0, 0.06, P.ink, { pivot: 'bottom' }), 0.78, 0, 0));
    for (let i = 0; i < 5; i++) for (const y of [0.6, 1.0]) { const x = -0.6 + i * 0.3, c = i % 2 ? P.red : P.navy; rack.add(rod([x - 0.12, y, 0.05], [x + 0.12, y, 0.05], 0.015, P.grey), at(cyl(0.06, 0.06, 0.06, c, 8), x - 0.1, y, 0.05, 0, 0, PI / 2), at(cyl(0.06, 0.06, 0.06, c, 8), x + 0.1, y, 0.05, 0, 0, PI / 2)); }
    g.add(at(rack, -3.6, 0, back + 0.4));
    // bench press
    const bp = grp(at(box(0.32, 0.12, 1.2, P.navy, { outline: 0.01 }), 0, 0.45, 0), at(box(0.1, 0.4, 0.1, P.ink, { pivot: 'bottom' }), 0, 0, 0.45), at(box(0.1, 0.4, 0.1, P.ink, { pivot: 'bottom' }), 0, 0, -0.45),
      at(box(0.06, 1.1, 0.06, P.ink, { pivot: 'bottom' }), -0.5, 0, -0.5), at(box(0.06, 1.1, 0.06, P.ink, { pivot: 'bottom' }), 0.5, 0, -0.5), rod([-1.0, 1.08, -0.5], [1.0, 1.08, -0.5], 0.018, P.grey));
    [-0.85, 0.85].forEach(x => bp.add(at(cyl(0.22, 0.22, 0.06, P.ink, 10), x, 1.08, -0.5, 0, 0, PI / 2), at(cyl(0.16, 0.16, 0.05, P.red, 10), x * 0.92, 1.08, -0.5, 0, 0, PI / 2)));
    g.add(at(bp, 3.4, 0, -2.0));
    // treadmill
    g.add(at(grp(box(0.8, 0.18, 1.8, P.ink, { pivot: 'bottom', outline: 0.01 }), at(box(0.64, 0.02, 1.7, P.greyDark), 0, 0.19, 0), rod([-0.35, 0.18, -0.75], [-0.35, 1.25, -0.85], 0.03, P.grey), rod([0.35, 0.18, -0.75], [0.35, 1.25, -0.85], 0.03, P.grey), at(box(0.8, 0.25, 0.12, P.teal, { outline: 0.02 }), 0, 1.3, -0.85, -0.5)), -3.6, 0, -0.6));
    // punching bag on a stand
    const bag = grp(rod([0, 2.7, 0], [0, 2.1, 0], 0.01, P.ink), at(cyl(0.25, 0.25, 1.1, P.red, 8, { outline: 0.02 }), 0, 1.55, 0), at(cyl(0.26, 0.26, 0.08, P.ink, 8), 0, 2.08, 0));
    const stand = grp(at(box(0.08, 2.9, 0.08, P.ink, { pivot: 'bottom' }), -0.9, 0, 0), at(box(1.0, 0.08, 0.08, P.ink), -0.45, 2.86, 0), at(box(0.6, 0.06, 0.6, P.ink), -0.9, 0.03, 0), bag);
    g.add(at(stand, 4.4, 0, 0.6));
    g.userData.update = t => { bag.rotation.z = Math.sin(t * 2.2) * 0.04; };
    g.userData.anchors = { center: [0, 0, 0], bench: [3.4, 0, -2.0], benchLie: [3.4, 0.52, -2.0], bag: [4.4, 0, 0.6], bagFront: [4.4, 0, 1.4], treadmill: [-3.6, 0.2, -0.6], rack: [-3.6, 0, back + 0.4], mirror: [0.8, 1.35, back] };
    g.userData.lighting = 'interior'; return g;
  },
  chineseRestaurant(o = {}) { // French "restaurant chinois" — viz3d pass from real dining rooms: red walls with a gold-trimmed dado, dark wood
                              // floor, round tables with white cloths and glass lazy Susans, red lanterns, the brand sign over a lacquered bar,
                              // a fish tank, ink landscape scrolls, round fans, a menu board, the kitchen door, bamboo in pots
    const g = grp(), { back } = room(g, { wall: '#A8322A', band: '#5A1E16', bandH: 1.05, trim: '#D8A83A', floor: '#6B4A34', back: -3.6, half: 6 }), anim = [];
    const teapot = () => grp(at(sphere(0.07, '#F4EFE6', 1), 0, 0.06, 0), at(cyl(0.03, 0.03, 0.02, '#F4EFE6', 8), 0, 0.125, 0), rod([0.05, 0.05, 0], [0.11, 0.1, 0], 0.012, '#F4EFE6'), at(torus(0.035, 0.008, '#F4EFE6', 4, 10), -0.075, 0.07, 0));
    const roundTable = (x, z, chairs = 4, main = false) => {
      const t = grp(at(cyl(0.6, 0.6, 0.03, '#F4EFE6', 22, { outline: 0.004 }), 0, 0.77, 0), at(cyl(0.6, 0.63, 0.3, '#ECE4D6', 22, { pivot: 'top' }), 0, 0.755, 0),
        at(cyl(0.3, 0.3, 0.012, '#CFE3E3', 20), 0, 0.792, 0));
      if (!main) t.add(at(buildProp('riceBowl', {}), -0.12, 0.798, 0.05), at(buildProp('noodlePlate', { seed: x * 7 + z }), 0.12, 0.798, -0.05), at(teapot(), 0.05, 0.798, 0.2));
      for (let i = 0; i < chairs; i++) { const a = (main ? PI : 0) + i * TAU / chairs; t.add(prop('chair', { color: '#3A2418' }, Math.sin(a) * 0.85, 0, Math.cos(a) * 0.85, a + PI)); }
      return at(t, x, 0, z); };
    g.add(roundTable(0, -1.2, 1, true), roundTable(-3.5, -1.7), roundTable(3.5, -1.5), roundTable(-3.4, 1.7), roundTable(3.4, 1.9));
    [[0, -1.2], [-3.5, -1.7], [3.5, -1.5], [-3.4, 1.7], [3.4, 1.9], [0, 1.4]].forEach(([x, z]) => g.add(prop('lantern', { cord: 4.4 }, x, 2.6, z)));
    // lacquered bar under the brand sign, till, menus, vase; the kitchen swing door
    g.add(at(box(3.0, 1.05, 0.6, '#3A2418', { pivot: 'bottom', outline: 0.006 }), -1.4, 0, back + 0.85), at(box(3.1, 0.05, 0.7, '#5A3A28'), -1.4, 1.075, back + 0.85), at(box(3.0, 0.06, 0.02, '#D8A83A'), -1.4, 0.82, back + 1.16));
    g.add(prop('cashRegister', {}, -0.5, 1.1, back + 0.85), at(box(0.25, 0.05, 0.34, '#B5302A'), -2.3, 1.125, back + 0.85), at(cyl(0.08, 0.12, 0.42, '#2C4A8A', 10, { pivot: 'bottom', outline: 0.008 }), -2.75, 1.1, back + 0.8));
    g.add(at(box(3.5, 0.74, 0.08, '#1A1412', { outline: 0.006 }), -1.4, 2.75, back + 0.05), at(label(o.brand || "LE LOTUS D'OR", 3.3, 0.58, { bg: '#B5302A', fg: '#F2D16B', wrap: false }), -1.4, 2.75, back + 0.1));
    g.add(prop('door', { color: '#7A1E18', frame: '#D8A83A' }, 2.3, 0, back), at(cyl(0.15, 0.15, 0.02, '#F2E2B0', 14, { emissive: '#5A4A20' }), 2.3, 1.55, back + 0.07, PI / 2, 0, 0));
    // decoration: ink-landscape scrolls, round fans, menu board, fish tank, bamboo
    const scroll = (w, h) => grp(at(canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#EFE6CF'; c.fillRect(0, 0, W, H); c.fillStyle = '#5A5A5A';
        c.beginPath(); c.moveTo(0, H * 0.75); c.lineTo(W * 0.25, H * 0.35); c.lineTo(W * 0.45, H * 0.62); c.lineTo(W * 0.7, H * 0.25); c.lineTo(W, H * 0.7); c.lineTo(W, H); c.lineTo(0, H); c.fill();
        c.fillStyle = '#9A9A9A'; c.beginPath(); c.moveTo(0, H * 0.85); c.lineTo(W * 0.35, H * 0.6); c.lineTo(W * 0.6, H * 0.82); c.lineTo(W, H * 0.78); c.lineTo(W, H); c.lineTo(0, H); c.fill();
        c.fillStyle = '#B5302A'; c.fillRect(W * 0.78, H * 0.08, W * 0.1, W * 0.1); }, { res: 256 }), 0, 0, 0.012), at(box(w + 0.1, 0.04, 0.04, '#3A2418'), 0, h / 2, 0.02), at(box(w + 0.1, 0.04, 0.04, '#3A2418'), 0, -h / 2, 0.02));
    g.add(at(scroll(0.7, 1.4), 4.2, 2.1, back + 0.02), at(scroll(0.6, 1.2), -5.98, 2.1, -0.6, 0, PI / 2, 0));
    [[-3.6, 2.75], [0.8, 2.75]].forEach(([x, y]) => g.add(at(cyl(0.32, 0.32, 0.02, '#C8281E', 18, { outline: 0.006 }), x, y, back + 0.03, PI / 2, 0, 0), at(torus(0.32, 0.012, '#D8A83A', 4, 24), x, y, back + 0.045)));
    g.add(at(box(1.3, 0.95, 0.05, '#1A1412', { outline: 0.006 }), 4.2, 0.0 + 1.95 - 1.0, back + 0.03), at(label('NEMS ......... 6 €\nCANARD LAQUÉ .. 14 €\nRIZ CANTONAIS .. 7 €\nNOUILLES ....... 9 €', 1.2, 0.85, { bg: '#1A1412', fg: '#F2D16B' }), 4.2, 0.95, back + 0.06));
    const tank = prop('aquarium', { w: 1.3 }, -5.55, 0, -1.4, PI / 2); anim.push(tank); g.add(tank);
    [[-5.4, back + 0.5], [5.4, back + 0.5]].forEach(([x, z], i) => { const b = grp(at(cyl(0.22, 0.18, 0.4, '#2C4A8A', 10, { pivot: 'bottom', outline: 0.008 }), 0, 0, 0));
      for (let k = 0; k < 5; k++) b.add(at(cyl(0.02, 0.025, 1.6 + (k % 3) * 0.3, '#7FA35A', 6, { pivot: 'bottom' }), Math.cos(k * 1.3) * 0.08, 0.35, Math.sin(k * 1.3) * 0.08, (k - 2) * 0.05, 0, (k % 2 ? 1 : -1) * 0.06), at(box(0.25, 0.02, 0.07, '#8DB86A'), Math.cos(k * 1.3) * 0.12, 1.3 + k * 0.12, Math.sin(k * 1.3) * 0.08, 0, k, 0.4));
      g.add(at(b, x, 0, z)); });
    g.userData.update = t => anim.forEach(p => p.userData.update(t));
    g.userData.anchors = { center: [0, 0, 0], table: [0, 0, -1.2], tableTop: [0, 0.785, -1.2], seat: [0, 0.12, -1.93], door: [2.3, 0, back + 0.6], bar: [-1.4, 0, back + 0.85], sign: [-1.4, 2.75, back] };
    g.userData.lighting = 'interior'; return g;
  },
  proKitchen(o = {}) { // restaurant kitchen — viz3d pass from real wok-kitchen layouts: wok range with jet burners and live flames under a steel
                       // hood, stock pot, steel prep island, shelves with sauces and bamboo steamers, rice cooker, utensil rail, white tiles,
                       // red quarry-tile floor, a back door, a big wall clock
    const g = grp(), { back } = room(g, { wall: '#E6ECEA', band: '#C9D2D0', bandH: 1.25, trim: '#8C949A', floor: '#9A4A3A', back: -3.2, half: 5.5 }), anim = [];
    const steel = '#B9BEC0', top = '#D5D9DB';
    g.add(at(box(4.2, 0.85, 0.75, steel, { pivot: 'bottom', outline: 0.006 }), 0.6, 0, back + 0.45), at(box(4.3, 0.05, 0.8, top), 0.6, 0.875, back + 0.45));
    const wok = x => grp(at(mesh(new THREE.SphereGeometry(0.28, 14, 6, 0, TAU, PI / 2, PI / 2), mat('#2A2A2E', { doubleSide: true })), x, 1.24, back + 0.45), rod([x + 0.27, 1.22, back + 0.45], [x + 0.62, 1.3, back + 0.45], 0.018, '#3A2418'));
    [-0.7, 0.6].forEach(x => { const fl = prop('flame', {}, x, 0.9, back + 0.45); anim.push(fl); g.add(fl, wok(x)); });
    g.add(at(cyl(0.26, 0.26, 0.5, '#C9CDCF', 14, { pivot: 'bottom', outline: 0.008 }), 1.9, 0.9, back + 0.45), at(cyl(0.27, 0.27, 0.03, '#A9AEB0', 14), 1.9, 1.41, back + 0.45));
    g.add(at(box(4.6, 0.55, 1.1, '#C9CDCF', { outline: 0.006, taper: { x: 0.94, z: 0.7 } }), 0.6, 2.55, back + 0.55), at(box(4.4, 0.04, 0.9, '#8C949A'), 0.6, 2.27, back + 0.6));
    for (let i = 0; i < 6; i++) { const x = -1.1 + i * 0.5; g.add(rod([x, 2.25, back + 1.02], [x, 1.95, back + 1.02], 0.006, '#8C949A'), at(sphere(0.05, '#A9AEB0', 0), x, 1.92, back + 1.02)); }
    g.add(rod([-1.3, 2.26, back + 1.02], [1.6, 2.26, back + 1.02], 0.01, '#8C949A'));
    // prep island in the middle: cutting board, cleaver, bowl of vegetables
    g.add(at(box(2.0, 0.88, 0.85, steel, { pivot: 'bottom', outline: 0.006 }), 0, 0, -0.6), at(box(2.1, 0.045, 0.9, top), 0, 0.9, -0.6), at(box(1.9, 0.03, 0.75, '#A9AEB0'), 0, 0.2, -0.6));
    g.add(at(box(0.45, 0.03, 0.3, '#C9A06A', { outline: 0.006 }), -0.55, 0.94, -0.55), at(box(0.2, 0.09, 0.005, '#C9CCD1'), -0.5, 0.958, -0.5, -PI / 2, 0, 0.2), at(cyl(0.16, 0.1, 0.09, P.white, 12, { pivot: 'bottom', outline: 0.006 }), -0.15, 0.925, -0.35));
    [[-0.2, -0.32, '#5E9A4A'], [-0.1, -0.38, '#E8775F'], [-0.16, -0.4, '#F2C230']].forEach(([x, z, c]) => g.add(at(sphere(0.045, c, 0), x, 1.01, z)));
    // shelves (right of the hood): sauces, bamboo steamers; rice cooker on a side table
    [1.1, 1.6, 2.1].forEach(y => g.add(at(box(1.6, 0.04, 0.4, top), 4.3, y, back + 0.22)));
    for (let i = 0; i < 5; i++) g.add(prop('sauceBottle', { text: ['SOJA', 'HUÎTRE', 'SÉSAME', 'SOJA', 'PIMENT'][i] }, 3.7 + i * 0.28, 1.12, back + 0.22, 0, 0.8));
    for (let s = 0; s < 2; s++) for (let k = 0; k < 3; k++) g.add(at(cyl(0.17, 0.17, 0.09, '#C9A06A', 12, { outline: 0.006 }), 3.9 + s * 0.7, 1.67 + k * 0.095, back + 0.22));
    g.add(at(box(1.1, 0.8, 0.6, steel, { pivot: 'bottom', outline: 0.006 }), -2.9, 0, back + 0.4), at(cyl(0.2, 0.2, 0.28, P.white, 14, { pivot: 'bottom', outline: 0.008 }), -2.9, 0.8, back + 0.4), at(sphere(0.2, P.white, 1), -2.9, 1.06, back + 0.4));
    g.add(prop('door', { color: '#8C949A', frame: '#6F7A82' }, -4.4, 0, back));
    g.add(prop('wallClock', { rate: o.clockRate ?? 1 / 60 }, -2.9, 2.35, back + 0.03, 0, 1.5));
    g.userData.update = t => anim.forEach(p => p.userData.update(t));
    g.userData.anchors = { center: [0, 0, 0], island: [0, 0, -0.6], islandTop: [0, 0.925, -0.6], behindIsland: [0.3, 0, -1.4], range: [0.6, 0, back + 0.45], door: [-4.4, 0, back + 0.6], clock: [-2.9, 2.35, back] };
    g.userData.lighting = 'interior'; return g;
  },
  maoStreet(o = {}) { // a 1970s Beijing hutong lane — viz3d pass from period photographs: grey brick courtyard walls with tiled copings, a red
                      // gate, a slogan banner, propaganda posters, bicycles, a loudspeaker on a pole, coal briquettes, crates at the mouth of a
                      // side alley (the black market), grey tiled roofs behind
    const g = grp(); sky(g, ['#B8C0BC', '#E2E2D8']); g.add(ground('#A89A84'));
    const BR = '#8E8C86', bz = -4.2;
    const bricks = (w, h) => canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#8E8C86'; c.fillRect(0, 0, W, H); const bw = W / (w / 0.48), bh = H / (h / 0.12); c.fillStyle = '#7A7872';
      for (let r = 0, y = 0; y < H; r++, y += bh) { c.fillRect(0, y, W, Math.max(1, bh * 0.14)); for (let x = (r % 2) * bw / 2; x < W; x += bw) c.fillRect(x, y, Math.max(1, bw * 0.05), bh); } }, { res: 2048 });
    // back wall split by the side alley (x 3.0..4.2), alley walls going back, coping tiles on top
    [[-9.0, 12], [9.6, 10.8]].forEach(([x, w]) => g.add(wall(w, 3, 0.4, BR, x, 1.5, bz), at(bricks(w, 3), x, 1.5, bz + 0.205), at(box(w + 0.1, 0.16, 0.6, '#4A4A4E'), x, 3.08, bz)));
    [3.0, 4.2].forEach(x => g.add(wall(0.4, 3, 6, BR, x + (x < 4 ? -0.2 : 0.2), 1.5, bz - 3.2), at(box(0.6, 0.16, 6.1, '#4A4A4E'), x + (x < 4 ? -0.2 : 0.2), 3.08, bz - 3.2)));
    g.add(wall(1.6, 3, 0.4, '#7A7872', 3.6, 1.5, bz - 6.2), wall(0.4, 3, 9, BR, -6.2, 1.5, bz + 4.5), at(box(0.6, 0.16, 9.1, '#4A4A4E'), -6.2, 3.08, bz + 4.5));
    // red gate under a little tiled roof, the slogan banner, posters
    g.add(at(box(1.9, 2.5, 0.3, '#6E241C', { pivot: 'bottom', outline: 0.006 }), -1.6, 0, bz + 0.2), at(box(0.78, 2.15, 0.06, '#B5302A', { pivot: 'bottom' }), -2.0, 0.05, bz + 0.37), at(box(0.78, 2.15, 0.06, '#B5302A', { pivot: 'bottom' }), -1.2, 0.05, bz + 0.37),
      at(box(2.4, 0.22, 0.9, '#4A4A4E', { taper: { x: 0.8, z: 0.4 } }), -1.6, 2.62, bz + 0.3));
    for (let k = 0; k < 9; k++) g.add(at(sphere(0.025, '#D8A83A', 0), -2.0 + ((k % 3) - 1) * 0.22, 0.7 + Math.floor(k / 3) * 0.45, bz + 0.41), at(sphere(0.025, '#D8A83A', 0), -1.2 + ((k % 3) - 1) * 0.22, 0.7 + Math.floor(k / 3) * 0.45, bz + 0.41));
    g.add(at(label('为人民服务', 3.0, 0.55, { bg: '#B5302A', fg: '#F2D16B', wrap: false }), -4.6, 2.35, bz + 0.22));
    g.add(at(buildProp('memePoster', { text: '禁止西方产品', skin: '#E0B48A' }), 0.9, 1.65, bz + 0.21), at(buildProp('memePoster', { text: '万岁', skin: '#E0B48A' }), 6.0, 1.65, bz + 0.21));
    // bicycles against the wall, loudspeaker pole, coal briquettes, crates at the alley mouth, grey roofs behind
    g.add(prop('bicycle', { color: '#2A2A30' }, -4.0, 0, bz + 0.5), prop('bicycle', { color: '#3E5A4A' }, -3.0, 0, bz + 0.55, 0.15));
    g.add(at(cyl(0.07, 0.09, 4.2, '#6B4A34', 6, { pivot: 'bottom' }), -5.3, 0, -1.8), prop('hornSpeaker', {}, -5.3, 4.0, -1.75, 0.6), prop('hornSpeaker', {}, -5.3, 3.85, -1.85, 2.4));
    const coal = []; for (let i = 0; i < 18; i++) coal.push([-5.6 + (i % 6) * 0.16, 0.06 + Math.floor(i / 6) * 0.11, bz + 0.6 + (i % 2) * 0.05]); g.add(inst(new THREE.CylinderGeometry(0.07, 0.07, 0.1, 8), mat('#232326'), coal));
    [[2.5, -3.6, 0.55], [2.6, -3.0, 0.45], [4.7, -3.7, 0.5], [3.5, -5.6, 0.6]].forEach(([x, z, s], i) => g.add(at(box(s, s, s, '#8A6A44', { pivot: 'bottom', outline: 0.008 }), x, 0, z, 0, i * 0.3, 0)));
    [[-7, -9, 9], [3, -10.5, 8], [12, -9, 7]].forEach(([x, z, w]) => g.add(at(box(w, 2.6, 5, '#7E7C76', { pivot: 'bottom' }), x, 0, z), at(box(w + 0.6, 1.3, 5.6, '#3E3E42', { taper: { x: 1, z: 0.1 } }), x, 3.25, z)));
    g.add(prop('tree', { seed: 31, color: '#6E8A5A' }, -8.5, 0, -6.5, 0, 1.6));
    g.userData.anchors = { center: [0, 0, 0], gate: [-1.6, 0, bz], alley: [3.6, 0, -4.9], poster: [0.9, 1.65, bz], pole: [-5.3, 0, -1.8], crates: [2.5, 0, -3.6] };
    g.userData.lighting = 'day'; return g;
  },
  tinyCell(o = {}) { // the absurd cell: a concrete niche 0.62 m wide behind bars in a dim corridor; a drawn "window" high on its back wall,
                     // years of tally marks on the block, a loudspeaker, one bare bulb
    const g = grp(), { back } = room(g, { wall: '#7C8079', band: '#5E625C', bandH: 1.0, trim: '#4A4E48', floor: '#6A6C66', back: -2.0, half: 4, height: 4.4 });
    const cw = 0.62, cd = 0.62, ch = 2.45, fz = back + cd, C = '#8A8D86';
    g.add(at(box(3.6, ch + 0.5, cd, C, { pivot: 'bottom', outline: 0.006 }), -cw / 2 - 1.8, 0, back + cd / 2), at(box(3.6, ch + 0.5, cd, C, { pivot: 'bottom', outline: 0.006 }), cw / 2 + 1.8, 0, back + cd / 2),
      at(box(cw, 0.5, cd, C), 0, ch + 0.25, back + cd / 2));
    g.add(prop('jailBars', { width: cw, height: ch }, 0, 0, fz), prop('windowDrawing', {}, 0.16, 2.22, back + 0.012, 0, 0.6));
    g.add(at(canvasPlane(1.7, 1.3, (c, W, H) => { c.fillStyle = '#8A8D86'; c.fillRect(0, 0, W, H); c.strokeStyle = 'rgba(240,238,228,0.85)'; c.lineWidth = W * 0.004;
      for (let r = 0; r < 14; r++) for (let k = 0; k < 9; k++) { const x0 = W * (0.04 + k * 0.105), y0 = H * (0.04 + r * 0.068); for (let s = 0; s < 4; s++) { c.beginPath(); c.moveTo(x0 + s * W * 0.016, y0); c.lineTo(x0 + s * W * 0.016 + W * 0.003, y0 + H * 0.05); c.stroke(); }
        c.beginPath(); c.moveTo(x0 - W * 0.008, y0 + H * 0.04); c.lineTo(x0 + W * 0.065, y0 + H * 0.012); c.stroke(); } }, { res: 1024, transparent: false }), -cw / 2 - 1.15, 1.45, fz + 0.006));
    g.add(prop('hornSpeaker', {}, 1.6, 3.0, fz + 0.01), hangLamp(0, 3.35, fz + 1.0, '#3A3A3A', 3));
    g.userData.anchors = { center: [0, 0, 0], cell: [0, 0, back + cd / 2], bars: [0, 0, fz], outside: [0, 0, fz + 0.7], drawing: [0.16, 2.22, back] };
    g.userData.lighting = 'interior'; return g;
  },
  pavillon(o = {}) { // suburban French house front: lawn, garden path, low fence with a gate, mailbox, trees, the pavement in front
    const g = grp(); sky(g); clouds(g, 9, 6); g.add(ground(P.grass));
    if (o.house !== false) g.add(prop('house', { w: 6.5, d: 5, h: 2.9, color: o.houseColor || '#EDE3CF', roof: o.roof || '#7A3A2A', door: o.door || '#2F5E58', frame: o.frame || '#2F5E58' }, 0, 0, -6.6));   // o.houseColor / o.roof (the green house), o.house === false (a scene supplies its own)
    g.add(flat(1.2, 6.2, '#CFC6B4', 0.97, 0.004, -0.95), flat(60, 2.4, '#C9C2B2', 0, 0.006, 3.6), flat(60, 8, '#4A4F55', 0, -0.02, 9));
    g.add(prop('fence', { length: 5.4, height: 0.85, color: P.white }, -3.4, 0, 2.2), prop('fence', { length: 5.4, height: 0.85, color: P.white }, 4.9, 0, 2.2), prop('mailbox', { color: '#B5302A' }, 2.8, 0, 2.5));
    [[-6.5, -3, 2], [6.8, -2.5, 5], [-9, 0.5, 8], [9.5, 0, 11]].forEach(([x, z, s]) => g.add(prop('tree', { seed: s }, x, 0, z, 0, 1.2)));
    [[-2.6, -3.6], [3.8, -3.7], [-4.3, -3.5]].forEach(([x, z], i) => g.add(prop('bush', { seed: i + 40 }, x, 0, z, 0, 0.9)));
    g.userData.anchors = { center: [0, 0, 0], door: [0.97, 0, -3.6], path: [0.97, 0, -1.0], gate: [0.97, 0, 2.2], pavement: [0, 0, 3.6] };
    g.userData.sun = [0.55, 0.62, 0.56];   // shader look: from the front right, long shadows across the lawn
    g.userData.lighting = 'day'; return g;
  },
  poste(o = {}) { // French post office — viz3d pass from real branch layouts: counter with three glazed windows, "now serving" board,
                  // ticket dispenser, rows of waiting chairs, parcel shelves, posters, plants, a wall clock (o.clockRate)
    const g = grp(), { back } = room(g, { wall: '#EDE8DC', band: '#F2C230', bandH: 1.0, trim: '#2C4A8A', floor: '#C9C2B2', back: -3.4, half: 6 });
    g.add(at(box(6.0, 1.05, 0.7, '#2C4A8A', { pivot: 'bottom', outline: 0.006 }), 0, 0, back + 1.0), at(box(6.1, 0.05, 0.8, '#E6E2D8'), 0, 1.075, back + 1.0), at(box(6.0, 0.1, 0.02, '#F2C230'), 0, 0.8, back + 1.36));
    [-2.0, 0, 2.0].forEach(x => { g.add(at(mesh(new THREE.BoxGeometry(1.5, 1.0, 0.012), glassMat(0.18, '#DDEEF2')), x, 1.6, back + 1.2), at(box(1.56, 0.05, 0.05, '#2A2A2E'), x, 2.12, back + 1.2), at(box(0.05, 1.05, 0.05, '#2A2A2E'), x - 0.78, 1.6, back + 1.2), at(box(0.05, 1.05, 0.05, '#2A2A2E'), x + 0.78, 1.6, back + 1.2), at(box(0.3, 0.04, 0.12, '#C9CCD1'), x, 1.1, back + 1.32)); });
    if (o.guichets !== false) [-2.0, 0, 2.0].forEach((x, i) => g.add(at(label(`GUICHET ${i + 1}`, 0.7, 0.16, { bg: '#2C4A8A', fg: '#F6F1E3', wrap: false }), x, 2.3, back + 1.22)));   // o.guichets false: no window signs
    g.add(at(label(o.title || 'BUREAU DE POSTE', 3.4, 0.4, { bg: '#F2C230', fg: '#2C4A8A', wrap: false }), 0, 3.2, back + 0.02));
    for (let r = 0; r < 2; r++) for (let i = 0; i < 5; i++) g.add(prop('chair', { color: '#2C4A8A' }, -2.6 + i * 0.9 + (r ? 3.0 : 0) * 0, 0, 0.9 + r * 1.2, PI));
    g.add(prop('ticketMachine', { num: o.ticketNum || '4000' }, 3.6, 0, -0.3, -0.5));
    [[-5.2, 'COLIS'], [5.2, 'TIMBRES']].forEach(([x, t]) => g.add(at(buildProp('fitPoster', { text: t, bg: '#2C4A8A', fg: '#F2C230' }), x, 1.8, back + 0.02)));
    for (let k = 0; k < 3; k++) g.add(at(box(1.4, 0.04, 0.4, '#C9A06A'), -4.6, 0.9 + k * 0.5, back + 0.22));
    for (let k = 0; k < 9; k++) g.add(at(box(0.32, 0.22, 0.3, '#C49A66', { outline: 0.006 }), -5.1 + (k % 3) * 0.45, 1.03 + Math.floor(k / 3) * 0.5, back + 0.24));
    g.add(prop('plant', { seed: 21 }, 5.4, 0, back + 0.5), prop('plant', { seed: 22 }, -5.4, 0, 2.0));
    g.add(prop('wallClock', { rate: o.clockRate ?? 1 / 60 }, 3.9, 2.4, back + 0.03));
    g.userData.anchors = { center: [0, 0, 0], counter: [0, 0, back + 1.0], clerk: [0, 0, back + 0.55], window: [0, 1.6, back + 1.2], customer: [0, 0, back + 1.75], chairs: [-2.6, 0, 0.9], ticket: [3.6, 0, -0.3] };
    g.userData.lighting = 'interior'; return g;
  },
  cave(o = {}) { // cellar: rough concrete, a low ceiling (bottom at 2.45 m), pipes, a bare bulb, cardboard boxes, a mattress on the floor, a tiny high window
    const g = grp(), { back } = room(g, { wall: '#8E918A', band: '#7C7F78', bandH: 0.6, trim: '#6A6D66', floor: '#6E6F69', back: -2.8, half: 3.6, height: 3.2, front: 6 });
    const ceil = at(box(7.6, 0.24, 9.0, '#86898A', { outline: 0.006 }), 0, 2.57, 1.6); ceil.traverse(n => { n.castShadow = false; }); g.add(ceil);
    [[2.12, 0.05], [2.26, 0.04]].forEach(([y, r]) => g.add(rod([-3.5, y, back + 0.15], [3.5, y, back + 0.15], r, '#5A5E66')));
    g.add(rod([2.6, 0, back + 0.2], [2.6, 2.45, back + 0.2], 0.05, '#5A5E66'), at(box(0.6, 0.3, 0.03, '#2A3A55'), -0.9, 2.05, back + 0.02), at(box(0.7, 0.4, 0.04, '#6A6D66'), -0.9, 2.05, back + 0.005));
    g.add(rod([0.5, 2.45, -0.9], [0.5, 1.98, -0.9], 0.008, P.ink), at(sphere(0.07, '#FFF2C0', 1, { emissive: '#FFD27A', noGrain: true }), 0.5, 1.92, -0.9));
    const bulb = new THREE.PointLight('#FFD9A0', 6, 7, 1.4); bulb.position.set(0.5, 1.85, -0.9); g.add(bulb);
    [[2.2, 0, -2.2, 0.7], [2.9, 0, -2.0, 0.6], [2.5, 0.55, -2.15, 0.55], [-3.0, 0, -2.3, 0.6]].forEach(([x, y, z, sz]) => g.add(at(box(sz, sz * 0.8, sz * 0.9, '#C49A66', { pivot: 'bottom', outline: 0.006 }), x, y, z, 0, (x * 7 % 1) * 0.4, 0)));
    g.add(at(box(0.95, 0.16, 1.95, '#D8D2C4', { pivot: 'bottom', outline: 0.006 }), -1.5, 0, -1.6), at(box(0.6, 0.12, 0.35, P.white), -1.5, 0.22, -2.35), at(box(0.97, 0.06, 1.1, '#5A6E8C'), -1.5, 0.17, -1.25));
    g.userData.anchors = { center: [0, 0, 0], mattress: [-1.5, 0.16, -1.6], bulb: [0.5, 1.92, -0.9], window: [-0.9, 2.05, back] };
    g.userData.lighting = 'dark'; return g;
  },
  chambre(o = {}) { // small bedroom: single bed, desk with a computer, wardrobe, full-length mirror, gym-guru poster, clothes on the floor,
                    // window with curtains; o.wall / o.poster / o.blanket restyle it (Glucksmann's room at the end)
    const g = grp(), { back } = room(g, { wall: o.wall || '#C9D3D6', band: o.band || '#AEB9BC', bandH: 0.9, trim: '#8A969A', floor: o.floor || '#B08A64', back: -3.0, half: 4.5 });
    g.add(prop('bed', { w: 0.95, blanket: o.blanket || '#5A6E8C' }, -2.6, 0, back + 1.1, o.bedFlip ? PI : 0));   // o.bedFlip: the pillow at the other end (toward +Z)
    g.add(at(box(1.3, 0.05, 0.6, '#E6E2D8', { outline: 0.006 }), 2.5, 0.74, back + 0.35));
    [[-0.6, -0.25], [0.6, -0.25], [-0.6, 0.25], [0.6, 0.25]].forEach(([x, z]) => g.add(at(box(0.04, 0.74, 0.04, '#8A969A', { pivot: 'bottom' }), 2.5 + x, 0, back + 0.35 + z)));
    g.add(at(box(0.6, 0.38, 0.04, P.ink, { outline: 0.006 }), 2.5, 1.0, back + 0.2), at(box(0.54, 0.32, 0.01, '#3E6FB5', { emissive: '#1A3A6A' }), 2.5, 1.0, back + 0.225), at(box(0.06, 0.2, 0.06, P.ink, { pivot: 'bottom' }), 2.5, 0.765, back + 0.18));
    g.add(prop('chair', { color: '#3A3D44' }, 2.5, 0, back + 1.0, PI));
    g.add(at(box(1.0, 2.1, 0.55, '#C9A06A', { pivot: 'bottom', outline: 0.008 }), 4.0, 0, back + 0.3), at(box(0.01, 2.0, 0.02, '#8A6A44'), 4.0, 1.05, back + 0.58), at(box(0.04, 0.12, 0.03, '#8A6A44'), 3.94, 1.1, back + 0.6), at(box(0.04, 0.12, 0.03, '#8A6A44'), 4.06, 1.1, back + 0.6));
    g.add(prop('mirrorFull', {}, 0.9, 0, back + 0.05));
    if (o.poster !== false) g.add(at(buildProp('fitPoster', { text: o.poster || 'CLAVICULE\nLARGE', bg: o.posterBg, fg: o.posterFg }), -0.6, 1.75, back + 0.02));   // (pass 2 of 53) o.poster false: no gym poster (it fought his face)
    g.add(at(box(0.05, 1.2, 1.4, '#F2F2EC', { outline: 0.006 }), -4.48, 1.75, -0.6), at(box(0.03, 1.1, 1.3, o.pane || '#9CC8E8', { emissive: o.paneGlow || '#2A4A5A' }), -4.45, 1.75, -0.6),   // o.pane / o.paneGlow: the window by night
      at(box(0.06, 1.6, 0.35, o.curtain || '#B5302A'), -4.42, 1.65, -1.45), at(box(0.06, 1.6, 0.35, o.curtain || '#B5302A'), -4.42, 1.65, 0.25));
    if (o.clutter !== false) [[-0.9, 0.02, 0.4, 0.4, '#2C4A8A'], [-0.6, 0.05, 0.6, -0.3, '#E8742E'], [1.9, 0.02, -1.5, 0.9, '#5E9A4A']].forEach(([x, y, z, ry, c]) => g.add(at(box(0.45, 0.05, 0.32, c, { outline: 0.004 }), x, y, z, 0, ry, 0)));   // o.clutter false: no clothes on the floor (a shot where somebody lies or lands there)
    g.add(prop('plant', { pot: '#C9A06A', seed: 9 }, 3.3, 0, back + 0.35, 0, 0.8));
    g.userData.anchors = { center: [0, 0, 0], bed: [-2.6, 0, back + 1.1], bedSit: [-2.6, 0.45, back + 1.6], desk: [2.5, 0, back + 0.35], chair: [2.5, 0, back + 1.0], mirror: [0.9, 0, back + 0.05], poster: [-0.6, 1.75, back] };
    g.userData.lighting = 'interior'; return g;
  },
  cinema(o) {
    const g = grp(), { back } = room(g, { wall: '#3A1E22', floor: '#2A1F24', back: -9, half: 7 });
    const scr = canvasPlane(9, 4.0, (c, W, H) => { c.fillStyle = o.screenColor || '#C9D6DE'; c.fillRect(0, 0, W, H); if (o.screenText) { c.fillStyle = P.navy; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `bold ${H * 0.18}px Arial`; c.fillText(o.screenText, W / 2, H / 2); } }, { emissive: 0.3 });
    g.add(at(box(9.4, 4.4, 0.1, P.ink), 0, 3.2, back + 0.06), at(scr, 0, 3.2, back + 0.12));
    for (const s of [-1, 1]) for (let i = 0; i < 6; i++) g.add(at(box(0.32, 6.4, 0.18, i % 2 ? P.red : P.redDark), s * (5.0 + i * 0.3), 3.2, back + 0.3, 0, s * (i % 2 ? 0.4 : -0.4), 0));
    g.add(at(box(14, 0.6, 0.3, P.redDark), 0, 6.3, back + 0.3));
    // seat rows facing the screen (camera sees their backs) + a centre aisle
    const seat = () => grp(at(box(0.5, 0.12, 0.5, P.red), 0, 0.42, 0), at(box(0.52, 0.6, 0.12, P.red, { outline: 0.01 }), 0, 0.75, 0.24), at(box(0.06, 0.25, 0.5, P.ink, { pivot: 'bottom' }), -0.28, 0.4, 0), at(box(0.06, 0.4, 0.4, P.ink, { pivot: 'bottom' }), 0, 0, 0));
    for (let row = 0; row < 4; row++) { const z = -3.4 - row * 1.25, y = row * 0.0; for (let i = 0; i < 12; i++) { const x = (i - 5.5) * 0.6 + (i < 6 ? -0.5 : 0.5); g.add(at(seat(), x, y, z)); } }
    for (let i = 0; i < 6; i++) g.add(at(box(0.1, 0.02, 0.3, '#FFD27A', { emissive: '#C9922E', noGrain: true }), -1.0, 0.01, -2.4 - i * 1.25), at(box(0.1, 0.02, 0.3, '#FFD27A', { emissive: '#C9922E', noGrain: true }), 1.0, 0.01, -2.4 - i * 1.25));
    const l = new THREE.PointLight('#BFD3FF', 10, 22, 1.2); l.position.set(0, 3.2, back + 3); g.add(l);
    g.userData.anchors = { center: [0, 0, 0], screen: [0, 3.2, back], aisle: [0, 0, -3.4], seat: [-1.1, 0.48, -3.4], seatRight: [1.1, 0.48, -3.4] };
    g.userData.lighting = 'dark'; return g;
  },
  church() {
    const g = grp(), { back } = room(g, { wall: '#E9E1CF', floor: '#B9AE9A', back: -7 });
    g.add(flat(1.8, 30, P.red, 0, 0.004, back + 15));
    // stained-glass lancet windows
    const lancet = (w, h) => canvasPlane(w, h, (c, W, H) => { c.save(); c.beginPath(); c.moveTo(0, H); c.lineTo(0, W / 2); c.arc(W / 2, W / 2, W / 2, PI, 0); c.lineTo(W, H); c.closePath(); c.clip();
      const cols = [P.teal, P.red, P.yellow, P.navyLight, P.tealLight]; let k = 0; for (let y = 0; y < H; y += H / 9) for (let x = 0; x < W; x += W / 3) { c.fillStyle = cols[(k++ * 7) % 5]; c.fillRect(x, y, W / 3, H / 9); }
      c.strokeStyle = P.ink; c.lineWidth = W * 0.04; for (let y = 0; y < H; y += H / 9) { c.beginPath(); c.moveTo(0, y); c.lineTo(W, y); c.stroke(); } for (let x = 0; x <= W; x += W / 3) { c.beginPath(); c.moveTo(x, 0); c.lineTo(x, H); c.stroke(); } c.restore(); }, { res: 128, emissive: 0.55, transparent: true });
    g.add(at(lancet(1.4, 3.8), 0, 4.2, back + 0.02), at(lancet(0.9, 2.8), -3.2, 3.6, back + 0.02), at(lancet(0.9, 2.8), 3.2, 3.6, back + 0.02));
    // altar on a step + candles
    g.add(at(box(4.4, 0.22, 2.6, P.creamDark, { pivot: 'bottom' }), 0, 0, back + 1.3), at(box(2.4, 1.0, 0.9, P.cream, { pivot: 'bottom', outline: 0.006 }), 0, 0.22, back + 1.3), at(box(0.6, 0.98, 0.92, P.red, { pivot: 'bottom' }), 0, 0.23, back + 1.3), at(box(0.62, 0.06, 0.94, P.yellow), 0, 0.3, back + 1.3));
    [-0.9, -0.6, 0.6, 0.9].forEach(x => g.add(at(cyl(0.04, 0.04, 0.3, P.white, 6, { pivot: 'bottom' }), x, 1.22, back + 1.3), at(mesh(new THREE.ConeGeometry(0.03, 0.08, 5), glow('#FFD27A')), x, 1.56, back + 1.3)));
    // pillars + pews on both sides of the aisle
    [-1, 1].forEach(s => { [-1.8, -4.8].forEach(z => g.add(at(cyl(0.35, 0.4, 7, P.creamDark, 8, { pivot: 'bottom' }), s * 4.2, 0, z)));
      [-3.4, -2.0, 1.3, 2.7].forEach(z => g.add(at(grp(at(box(2.2, 0.06, 0.45, P.woodDark), 0, 0.45, 0), at(box(2.2, 0.5, 0.06, P.woodDark, { outline: 0.008 }), 0, 0.75, 0.22), at(box(0.06, 0.95, 0.5, P.woodDark, { pivot: 'bottom' }), -1.07, 0, 0.02), at(box(0.06, 0.95, 0.5, P.woodDark, { pivot: 'bottom' }), 1.07, 0, 0.02)), s * 2.15, 0, z))); });
    g.userData.anchors = { center: [0, 0, 0], altar: [0, 0.22, back + 2.2], altarBehind: [0, 0.22, back + 0.5], pew: [-2.15, 0.48, -3.4], aisle: [0, 0, 0], window: [0, 4.2, back] };
    g.userData.lighting = 'interior'; return g;
  },
  desert() {
    const g = grp(), r = rng(41); sky(g, ['#9CBCC8', '#EBD9B5']);
    g.add(ground('#D9BC82'), at(mesh(new THREE.CircleGeometry(8, 16), new THREE.MeshBasicMaterial({ color: '#F6E3A6', fog: false })), 40, 55, -150, 0, -0.25, 0));
    for (let i = 0; i < 9; i++) { const m = sphere(1, i % 2 ? '#D3B47A' : '#CDAE72', 1); m.scale.set(10 + r() * 10, 2 + r() * 2.5, 6 + r() * 5); m.position.set((r() - 0.5) * 120, -0.6, -18 - r() * 40); if (Math.abs(m.position.x) < 12 && m.position.z > -22) m.position.z -= 12; m.castShadow = false; g.add(m); }
    [[-55, -90, 30, 12], [10, -100, 40, 9], [60, -85, 28, 14]].forEach(([x, z, w, h]) => g.add(at(box(w, h, 12, '#B9734E', { pivot: 'bottom', taper: { x: 0.8, z: 0.75 } }), x, 0, z)));
    [[-2.4, -4, 1], [5.2, -8, 2, 1.2], [-10, -15, 3, 1.4], [14, -20, 4, 1.3]].forEach(([x, z, s, k = 1]) => g.add(at(cactus(s, k), x, 0, z)));
    [[3.0, -2.0, 0.3], [-6, -6, 0.6], [8, -4, 0.45]].forEach(([x, z, s]) => g.add(at(rock(s, '#B08F6A', r), x, 0, z)));
    g.add(at(grp(at(box(0.36, 0.22, 0.28, P.paper, { taper: 0.8 }), 0, 0.12, 0), at(box(0.07, 0.07, 0.02, P.ink), -0.08, 0.15, 0.14), at(box(0.07, 0.07, 0.02, P.ink), 0.08, 0.15, 0.14), at(box(0.5, 0.05, 0.05, P.paper), 0.4, 0.03, 0.1, 0, 0.5, 0)), -2.2, 0, -2.6, 0, 0.3, 0));
    const weed = new THREE.Mesh(new THREE.IcosahedronGeometry(0.35, 1), new THREE.MeshBasicMaterial({ color: P.woodDark, wireframe: true })); g.add(weed);
    g.userData.update = t => { const x = -14 + ((t * 2.2) % 28); weed.position.set(x, 0.35 + Math.abs(Math.sin(t * 4)) * 0.25, -4.5); weed.rotation.z = -x / 0.35; };
    g.userData.update(0);
    g.userData.anchors = { center: [0, 0, 0], cactus: [-2.4, 0, -4], skull: [-2.2, 0, -2.6], rock: [3.0, 0, -2.0], dune: [0, 0, -25], tumbleweedLane: [0, 0, -4.5] };
    g.userData.lighting = 'savannah'; return g;
  },
  snow() {
    const g = grp(), r = rng(51); sky(g, ['#AFC4CE', '#E8EDEC']);
    g.add(ground('#F3F5F1'));
    hills(g, ['#E9EEEC', '#DCE4E3'], { seed: 13, z0: -40, z1: -80, sx: 24, sy: 7 });
    for (let i = 0; i < 46; i++) { const a = r() * TAU, d = 6 + r() * 40, x = Math.cos(a) * d, z = Math.sin(a) * d; if ((z > 1 && Math.abs(x) < 10) || (Math.abs(x) < 3.5 && z > -16)) continue; g.add(at(pine(i + 3, true, 0.8 + r() * 0.6), x, 0, z)); }
    g.add(at(pine(2, true, 1.1), -3.8, 0, -4.2), at(pine(5, true, 0.9), 4.6, 0, -5.5));
    const sm = grp(at(sphere(0.5, P.white, 1), 0, 0.45, 0), at(sphere(0.36, P.white, 1), 0, 1.13, 0), at(sphere(0.26, P.white, 1), 0, 1.62, 0), at(mesh(new THREE.ConeGeometry(0.05, 0.3, 6), mat('#E07A2E')), 0, 1.6, 0.36, PI / 2),
      at(box(0.05, 0.05, 0.02, P.ink), -0.09, 1.7, 0.23), at(box(0.05, 0.05, 0.02, P.ink), 0.09, 1.7, 0.23), at(torus(0.27, 0.06, P.red, 4, 10), 0, 1.4, 0, PI / 2), at(cyl(0.2, 0.2, 0.3, P.navy, 8, { pivot: 'bottom' }), 0, 1.8, 0), at(cyl(0.3, 0.3, 0.03, P.navy, 8), 0, 1.81, 0));
    g.add(at(sm, 2.0, 0, -2.8, 0, -0.3, 0));
    // falling snow: deterministic function of t
    const N = 700, base = new Float32Array(N * 4), pos = new Float32Array(N * 3); for (let i = 0; i < N; i++) base.set([(r() - 0.5) * 26, r() * 10, -14 + r() * 22, r() * TAU], i * 4);
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    g.add(new THREE.Points(geo, new THREE.PointsMaterial({ color: P.white, size: 0.06 })));
    g.userData.update = t => { for (let i = 0; i < N; i++) { const [x, y, z, ph] = base.subarray(i * 4, i * 4 + 4); pos[i * 3] = x + Math.sin(t * 0.8 + ph) * 0.3; pos[i * 3 + 1] = ((y - t * (0.6 + (ph % 1) * 0.4)) % 10 + 10) % 10; pos[i * 3 + 2] = z; } geo.attributes.position.needsUpdate = true; };
    g.userData.update(0);
    g.userData.anchors = { center: [0, 0, 0], snowman: [2.0, 0, -2.8], pine: [-3.8, 0, -4.2], pineRight: [4.6, 0, -5.5] };
    g.userData.lighting = 'day'; return g;
  },
};

const LCDc = '#7CE38B';
// Red/white checker cloth (restaurant).
function checkerMat(a, b) {
  const c = document.createElement('canvas'); c.width = c.height = 64; const x = c.getContext('2d');
  for (let i = 0; i < 8; i++) for (let j = 0; j < 8; j++) { x.fillStyle = (i + j) % 2 ? a : b; x.fillRect(i * 8, j * 8, 8, 8); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.magFilter = THREE.NearestFilter; return new THREE.MeshLambertMaterial({ map: t });
}
// Square wall tiles with grout lines (bathroom), repeat via geometry UVs.
function tileMat(tile, grout) {
  const c = document.createElement('canvas'); c.width = c.height = 64; const x = c.getContext('2d');
  x.fillStyle = grout; x.fillRect(0, 0, 64, 64); x.fillStyle = tile; x.fillRect(3, 3, 58, 58);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; return new THREE.MeshLambertMaterial({ map: t });
}

// Street (day or night): near sidewalk at y=0 (actors), road at y=-0.14, buildings behind.
function streetSet(o, night) {
  const g = grp(), r = rng(o.seed || 5);
  if (night) nightSky(g); else { sky(g); clouds(g, 4, 6); }
  g.add(flat(340, 60, P.creamDark, 0, 0, 28.4), flat(340, 7, '#4A4F55', 0, -0.14, -5.1), flat(340, 4, P.creamDark, 0, 0, -10.6), flat(340, 150, '#A3A79D', 0, -0.01, -87.6));
  g.add(at(box(340, 0.16, 0.2, P.cream), 0, -0.08, -1.6), at(box(340, 0.16, 0.2, P.cream), 0, -0.08, -8.6));
  const dash = [], seams = []; for (let x = -80; x <= 80; x += 4) dash.push([x, -0.135, -5.1]); for (let x = -60; x <= 60; x += 1.6) seams.push([x, 0.002, 2.2], [x, 0.002, -10.6, 0, 0, 0, 1, 1, 0.5]);
  g.add(inst(new THREE.BoxGeometry(2, 0.01, 0.16), mat(P.white), dash), inst(new THREE.BoxGeometry(0.03, 0.004, 7.6), mat('#C9BC9C'), seams));
  // buildings with window grids
  const win = { lit: [], dark: [] }, cols = [P.cream, P.tealLight, P.creamDark, P.red, P.salmon, P.tealPale, P.cream];
  for (let x = -45; x < 45;) { const w = 3.5 + r() * 2.5, h = 3.5 + Math.floor(r() * 4) * 1.6, c = cols[Math.floor(r() * cols.length)], cx = x + w / 2;
    g.add(at(box(w - 0.1, h, 5, c, { pivot: 'bottom' }), cx, 0, -15.3), at(box(w, 0.25, 5.2, P.navy), cx, h + 0.12, -15.3), at(box(0.9, 1.7, 0.06, P.navy), cx + (r() - 0.5) * (w - 2), 0.85, -12.78));
    for (let fy = 2.1; fy < h - 0.6; fy += 1.6) for (let fx = cx - w / 2 + 0.9; fx < cx + w / 2 - 0.6; fx += 1.25) (night && r() < 0.55 ? win.lit : win.dark).push([fx, fy, -12.78]);
    x += w; }
  windowsGrid(g, win, glow('#F2C46B'), mat(night ? '#2A3A55' : P.navyLight));
  const on = night;
  [[-4.5, -1.25, PI / 2], [5.5, -1.25, PI / 2], [-14, -1.25, PI / 2], [14.5, -1.25, PI / 2], [-8.5, -9.0, -PI / 2], [9.5, -9.0, -PI / 2], [22, -9.0, -PI / 2]].forEach(([x, z, ry], i) => g.add(prop('streetLamp', { on, light: on && i < 2 ? 5 : 0 }, x, 0, z, ry)));
  g.add(prop('fireHydrant', {}, 2.8, 0, -1.0), prop('trashCan', {}, -2.9, 0, -1.05), prop('speedSign', { value: 50 }, 8.5, 0, -1.25));
  g.userData.anchors = { center: [0, 0, 0], sidewalk: [0, 0, 0], curb: [0, 0, -1.6], road: [0, -0.14, -5.1], laneNear: [0, -0.14, -3.4], laneFar: [0, -0.14, -6.8], farSidewalk: [0, 0, -10.6], buildings: [0, 0, -12.8], lamp: [-4.5, 0, -1.25], hydrant: [2.8, 0, -1.0] };
  g.userData.lighting = night ? 'night' : 'day'; return g;
}

Object.assign(S, {
  parisStreet(o = {}) { // bright Paris street for the tornado-style remakes: asphalt road along Z, pale sidewalks, Haussmann blocks both sides (o.night: stars, lit windows and lamps),
    // (review 1 of 62) o.lampsOff / o.windowsOff: at night the street lamps unlit / every window dark (the street lit by one glowing man alone)
    // round trees, lamps, the Eiffel tower at the far end, the replica's blue sky and white clouds
    const g = grp(), r = rng(o.seed || 12), night = !!o.night, snow = !!o.snow;   // o.snow: snowed-in street, flakes falling round the origin
    if (night) nightSky(g, [26, 44, -150]); else { sky(g, o.sky || (snow ? ['#C3CCD5', '#EEF1F3'] : ['#62AEE2', '#A7D4EC'])); if ((o.clouds ?? 8) >= 2) clouds(g, o.cloudSeed ?? 6, o.clouds ?? 8); }   // o.cloudSeed / o.clouds: other clouds, or fewer (a cloud right behind a head reads as a hat)
    const hole = o.hole ? holeOutline(o.hole[2] ?? 0.9, o.hole[3] ?? 5).map(([x, z]) => [x + o.hole[0], z + o.hole[1]]) : null;   // o.hole [x, z, r, seed]: a real hole in the right-hand pavement (prop streetHole underneath)
    const base = hole ? groundHoled(night ? '#8E8A80' : snow ? '#F3F5F7' : '#C9C2B3', hole) : ground(night ? '#8E8A80' : snow ? '#F3F5F7' : '#C9C2B3'); base.position.y = -0.12; g.add(base);   // well under the road and the pavements (4 and 6 mm above it, they flickered against it in long views down the street)
    const pw = o.paveW ?? 5;   // o.paveW: the width of the pavements (5 m: they stop 0.2 m short of the house fronts, and the ground under them shows there as a dark gutter along the foot of the walls; 6.5 closes it, and the floor of the gaps between two blocks)
    g.add(flat(10, 400, snow ? '#C9CED4' : '#6E6E72', 0, 0.004, 0), hole ? flatHoled(pw, 400, snow ? '#F7F8FA' : '#E4D6BE', 5 + pw / 2, 0.006, 0, hole) : flat(pw, 400, snow ? '#F7F8FA' : '#E4D6BE', 5 + pw / 2, 0.006, 0), flat(pw, 400, snow ? '#F7F8FA' : '#E4D6BE', -(5 + pw / 2), 0.006, 0));
    if (hole) g.add(prop('streetHole', { r: o.hole[2] ?? 0.9, seed: o.hole[3] ?? 5, depth: o.holeDepth ?? 6 }, o.hole[0], 0.006, o.hole[1]));
    if (snow) { for (const x of [-1.6, -0.9, 1.0, 1.7]) g.add(flat(0.35, 400, '#A9AFB6', x, 0.007, 0)); g.add(prop('snowfall', { w: 30, h: 12, d: 40, n: o.snowN || 3200, size: o.snowSize || 0.13 }, o.snowX || 0, 0, 0), prop('snowBank', { len: 30 }, 5.4, 0, 0, PI / 2), prop('snowBank', { len: 30, seed: 7 }, -5.4, 0, 0, PI / 2)); }
    g.add(at(box(0.2, 0.16, 400, '#D9CDB4'), 5, 0, 0), at(box(0.2, 0.16, 400, '#D9CDB4'), -5, 0, 0));
    const dash = []; for (let z = -190; z <= 190; z += 4) dash.push([0, 0.008, z]);
    g.add(inst(new THREE.BoxGeometry(0.16, 0.01, 1.8), mat('#F4F1E8'), dash));
    const WC = o.walls || ['#EFE6D2', '#F2DCCB', '#F3E9C9', '#E8E1EE', '#EFE6D2', '#F0D9D9', '#E2EAF0'], AW = ['#B5302A', '#2F7F5C', '#2F5E8C', '#C9822E'];
    const z0 = o.z0 ?? -120, n = o.n ?? 16;
    for (let i = 0; i < n; i++) {
      const z = z0 + i * 13, h = 15 + r() * 5;
      g.add(prop('haussmann', { color: WC[i % WC.length], awning: AW[i % 4], h, floors: 6, cols: 5, w: o.blockW ?? 13.04, night, dark: !!o.windowsOff, seed: i }, 10.2, 0, z, -PI / 2));   // (review 2 of 61) 13.04 m every 13 m: at 12.6 a slit of sky ran up between two blocks
      g.add(prop('haussmann', { color: WC[(i + 3) % WC.length], awning: AW[(i + 2) % 4], h: 15 + r() * 5, floors: 6, cols: 5, w: o.blockW ?? 13.04, night, dark: !!o.windowsOff, seed: i + 40 }, -10.2, 0, z + 5, PI / 2));
      const clr = (zz) => o.clear && zz > o.clear[0] && zz < o.clear[1];   // o.clear [zmin, zmax]: no tree and no lamp on the right-hand pavement there (nothing growing out of a head)
      const clrL = (zz) => o.clearL && zz > o.clearL[0] && zz < o.clearL[1];   // (cycle 24, review 3 of 59) o.clearL [zmin, zmax]: no tree on the left-hand pavement there (one stood behind his neck like a green ruff)
      if (i % 2 === 0) { if (!clr(z + 4)) g.add(prop('tree', { seed: i + 7 }, 6.6, 0, z + 4, 0, 1.1)); if (!clrL(z - 2)) g.add(prop('tree', { seed: i + 50 }, -6.6, 0, z - 2, 0, 1.1)); if (!clr(z + 9)) g.add(prop('streetLamp', { on: night && !o.lampsOff }, 5.6, 0, z + 9)); }
    }
    if (o.eiffel !== false) g.add(prop('eiffelTower', { h: o.eiffelH || 70, style: o.eiffelStyle }, o.eiffelX ?? -8, 0, o.eiffelZ ?? -175));   // (cycle 14) o.eiffelStyle 'v2': the connected silhouette
    g.userData.anchors = { center: [0, 0, 0], sidewalk: [7.5, 0, 0], road: [0, 0, 0], ...(o.hole ? { hole: [o.hole[0], 0, o.hole[1]] } : {}) };
    g.userData.sun = o.sun || [-0.35, 0.78, 0.52];   // shader look: down the street, the pavements lit
    if (snow) g.userData.snow = true;
    g.userData.lighting = night ? 'night' : 'day'; return g;
  },
  // (cycle 7) the ground-floor hall of a block of flats, seen from the street door: in the back wall a lift door (o.doors [[t, 0..1], ...]: its two
  // leaves slide apart, eased; 0 = shut), over it the floor display (o.floor [[t, 'RC' | '1' | ...], ...]: amber on black) and beside it the call
  // button; letter boxes at the left (o.names: the name tags), a notice board at the right (o.notice: its heading, 'SYNDIC'), a tiled floor.
  // userData.anchors: lift (the foot of the door), seam (the top of the seam between the two leaves: where a tie goes up), boxes, board
  immeubleHall(o = {}) {
    const g = grp(), { back } = room(g, { wall: o.wall || '#EAE3D2', band: o.band || '#B9AA8C', bandH: 1.1, trim: o.trim || '#8C7B5E', floor: o.floor || '#DAD1C2', back: o.back ?? -3.0, half: 3.4, height: 3.6 });
    for (let i = -5; i <= 5; i++) g.add(flat(0.02, 16, '#C2B8A6', i * 0.6, 0.004, 4)); for (let k_ = 0; k_ < 24; k_++) g.add(flat(6.8, 0.02, '#C2B8A6', 0, 0.004, back + 0.3 + k_ * 0.6));
    const LX = o.liftX ?? 0, DW = 1.1, DH = 2.1, FR = '#6F7680', LC = o.leaf || '#AEB6BF', zf = back + 0.06;
    g.add(at(box(DW, DH, 0.02, '#14161B'), LX, DH / 2, back + 0.012));                                                                       // the dark of the shaft behind the leaves
    for (const sd of [-1, 1]) g.add(at(box(0.09, DH + 0.1, 0.12, FR, { outline: 0.006 }), LX + sd * (DW / 2 + 0.045), (DH + 0.1) / 2, zf));     // the frame
    g.add(at(box(DW + 0.18, 0.12, 0.12, FR, { outline: 0.006 }), LX, DH + 0.06, zf));
    const leaves = [-1, 1].map(sd => { const l = grp(at(box(DW / 2, DH, 0.035, LC, { outline: 0.004 }), 0, DH / 2, 0), at(box(0.012, DH * 0.86, 0.04, '#8E97A1'), sd * (DW / 4 - 0.05), DH / 2, 0.002)); l.userData.sd = sd; g.add(l); return l; });
    const texts = [...new Set((o.floor || [[0, 'RC']]).map(e => String(e[1])))], disp = {};
    g.add(at(box(0.5, 0.26, 0.05, '#0E0F13', { outline: 0.006 }), LX, DH + 0.3, zf));
    for (const tx of texts) { const pl = canvasPlane(0.44, 0.2, (c, W, H) => { c.fillStyle = '#0E0F13'; c.fillRect(0, 0, W, H); c.fillStyle = '#FFB02E'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `bold ${H * 0.78}px Arial`; c.fillText(tx, W / 2, H * 0.54); }, { res: 256, emissive: 0.9 }); pl.position.set(LX, DH + 0.3, zf + 0.03); g.add(pl); disp[tx] = pl; }
    const btn = at(box(0.1, 0.16, 0.03, '#8E97A1', { outline: 0.004 }), LX + DW / 2 + 0.28, 1.12, back + 0.03), lamp = at(cyl(0.022, 0.022, 0.012, '#FFD27A', 10), LX + DW / 2 + 0.28, 1.14, back + 0.052); lamp.rotation.x = PI / 2; g.add(btn, lamp);
    const names = o.names || ['DUPONT', 'MARTIN', 'PETIT', 'ROUX', 'MOREL', 'GIRARD', 'LEROY', 'FAURE'], BX = o.boxesX ?? -2.25;   // letter boxes: two rows of four
    names.forEach((nm, i) => { const x = BX + (i % 4 - 1.5) * 0.34, y = 1.52 - Math.floor(i / 4) * 0.3; g.add(at(box(0.31, 0.27, 0.1, i % 2 ? '#7E8C6E' : '#8A977A', { outline: 0.005 }), x, y, back + 0.06), at(box(0.2, 0.02, 0.012, '#1F2228'), x, y + 0.07, back + 0.115), at(label(nm, 0.2, 0.05, { bg: '#F4F1E8', fg: '#1B1B1E', wrap: false }), x, y - 0.03, back + 0.113)); });
    const NX = o.boardX ?? 2.3; g.add(at(box(0.9, 0.7, 0.03, '#B98A5A', { outline: 0.006 }), NX, 1.55, back + 0.03), at(label(o.notice || 'SYNDIC', 0.6, 0.14, { bg: '#1B2F6B', fg: '#FFFFFF', wrap: false }), NX, 1.8, back + 0.05));
    for (const [dx, dy, ry_, c_] of [[-0.2, -0.02, 0.05, '#F4F1E8'], [0.2, 0.0, -0.06, '#F3E9C9'], [0.0, -0.22, 0.03, '#E2EAF0']]) g.add(at(box(0.26, 0.2, 0.006, c_, { outline: 0.003 }), NX + dx, 1.53 + dy, back + 0.05, 0, 0, ry_));
    g.add(at(box(1.0, 0.02, 0.6, '#6B4F3A', { outline: 0.004 }), LX, 0.012, back + 0.55));                                                      // the doormat
    if (o.plant !== false) g.add(prop('plant', { pot: '#C9A06A', seed: 5 }, o.plantX ?? 3.0, 0, back + 0.4, 0, 0.9));
    const DOORS = o.doors || [[0, 0]], FLOOR = o.floor || [[0, 'RC']];
    const ease = x => x * x * (3 - 2 * x), doorAt = t => { let a = DOORS[0][1]; for (let i = 0; i < DOORS.length; i++) { const [t0, v0] = DOORS[i], nx = DOORS[i + 1]; if (t >= t0) a = nx && t < nx[0] ? v0 + (nx[1] - v0) * ease((t - t0) / (nx[0] - t0)) : v0; } return a; };
    g.userData.update = t => { const a = doorAt(t); for (const l of leaves) l.position.set(LX + l.userData.sd * (DW / 4 + a * (DW / 2 - 0.03)), 0, zf); let cur = String(FLOOR[0][1]); for (const [tt, v] of FLOOR) if (t >= tt) cur = String(v); for (const k_ in disp) disp[k_].visible = k_ === cur; };
    g.userData.update(0);
    g.userData.anchors = { center: [0, 0, 0], lift: [LX, 0, back], seam: [LX, DH - 0.03, zf + 0.03], boxes: [BX, 0, back], board: [NX, 0, back] };
    g.userData.lighting = 'interior'; return g;
  },
  // (cycle 7) a block of flats cut open, seen from the front (the camera looks toward -Z): o.floors (6) levels over the ground floor, each o.fh
  // (2.8 m) high. At the left the landings (a coloured wall, a flat door, the number of the floor); at the right the lift shaft, dark, with its cabin
  // (o.cabin [[t, level], ...], eased between keys) hanging from two cables. Actors stand on a landing at y = level * fh (userData.fh), x between -2.9
  // and 1.1; the shaft is centred on userData.shaftX. o.walls: the colours of the landings; o.sky. The street: a pavement in front, the sky behind.
  immeubleCoupe(o = {}) {
    const g = grp(), N = o.floors ?? 6, FH = o.fh ?? 2.8, W = 6.4, D = 2.2, SW = 1.7, SX = W / 2 - SW / 2 - 0.12, LW = W - SW - 0.24, LXc = -W / 2 + 0.12 + LW / 2, H = (N + 1) * FH;
    sky(g, o.sky || ['#62AEE2', '#A7D4EC']); if ((o.clouds ?? 6) >= 2) clouds(g, o.cloudSeed ?? 4, o.clouds ?? 6);
    const base = ground('#C9C2B3'); base.position.y = -0.12; g.add(base, flat(40, 9, '#E4D6BE', 0, 0.006, 4.5), flat(40, 30, '#6E6E72', 0, 0.004, 24));
    const WC = o.walls || ['#EFE6D2', '#F2DCCB', '#E2EAF0', '#F3E9C9', '#E8E1EE', '#F0D9D9', '#DDE8D8'], DC = ['#7A5A3C', '#2F5E8C', '#8A3B32', '#2F7F5C', '#6B4F8A', '#B5762E', '#3F4A5A'];
    g.add(wall(SW, H, 0.1, '#2E323C', SX, H / 2, -D / 2));                                                                                    // the shaft: its back
    // (cycle 8) o.doorZ [z0, z1]: the partition has a landing door on every floor (2.1 m high, from z0 to z1): a neighbour leans into the shaft through
    // it (through a solid partition her head came out on the shaft side)
    const PX = SX - SW / 2 - 0.06;
    if (o.doorZ) { const [z0, z1] = o.doorZ, DH = 2.1;
      for (let lv = 0; lv <= N; lv++) { const y0 = lv * FH;
        g.add(wall(0.12, FH - DH, D, '#B9AE9A', PX, y0 + DH + (FH - DH) / 2, 0), wall(0.12, DH, z0 + D / 2, '#B9AE9A', PX, y0 + DH / 2, (z0 - D / 2) / 2), wall(0.12, DH, D / 2 - z1, '#B9AE9A', PX, y0 + DH / 2, (z1 + D / 2) / 2));
        g.add(at(box(0.16, 0.06, z1 - z0 + 0.08, '#8C8478'), PX, y0 + DH + 0.03, (z0 + z1) / 2)); } }   // the door's lintel
    else g.add(wall(0.12, H, D, '#B9AE9A', PX, H / 2, 0));                                                                                       // the partition
    for (const sd of [-1, 1]) g.add(wall(0.24, H + 0.3, D + 0.1, '#CFC6B4', sd * (W / 2), (H + 0.3) / 2, 0));                                        // the outer walls
    for (let lv = 0; lv <= N; lv++) { const y0 = lv * FH;
      if (lv) g.add(at(box(LW + 0.02, 0.2, D, '#B9AE9A'), LXc, y0 - 0.1, 0));                                                                       // the slab of the landing
      g.add(wall(LW, FH - 0.2, 0.1, WC[lv % WC.length], LXc, y0 + (FH - 0.2) / 2, -D / 2), at(box(LW, 0.12, 0.03, '#8C7B5E'), LXc, y0 + 0.06, -D / 2 + 0.07));
      g.add(at(box(0.92, 2.05, 0.06, DC[lv % DC.length], { outline: 0.006 }), LXc - 0.9, y0 + 1.025, -D / 2 + 0.08), at(box(0.05, 0.05, 0.05, '#E3C56A'), LXc - 0.56, y0 + 1.0, -D / 2 + 0.13), at(box(0.8, 0.015, 0.45, '#6B4F3A'), LXc - 0.9, y0 + 0.01, -D / 2 + 0.36));
      g.add(at(label(lv ? String(lv) : 'RC', 0.5, 0.5, { bg: WC[lv % WC.length], fg: '#8C7B5E', wrap: false }), LXc + 0.95, y0 + 1.75, -D / 2 + 0.06));
      g.add(at(box(0.16, 0.1, 0.1, '#F4E3A8', { emissive: '#C9A24A' }), LXc + 0.1, y0 + 2.3, -D / 2 + 0.1));                                          // a wall lamp
    }
    g.add(at(box(W + 0.9, 0.3, D + 0.5, '#8E8A84', { outline: 0.006 }), 0, H + 0.15, 0), at(box(SW + 0.3, 0.9, D * 0.8, '#A39C90', { outline: 0.006 }), SX, H + 0.75, 0));   // the roof, the machine room
    const cab = grp(at(box(SW - 0.24, 2.3, D - 0.5, '#AEB6BF', { outline: 0.006 }), 0, 1.15, -0.1), at(box(SW - 0.36, 2.1, 0.02, '#F4EBD0', { emissive: '#8A7A4A' }), 0, 1.15, D / 2 - 0.36)); g.add(cab);
    const cables = [-0.3, 0.3].map(dx => { const c_ = cyl(0.012, 0.012, 1, '#1F2228', 5, { pivot: 'bottom' }); c_.position.set(SX + dx, 0, -0.1); g.add(c_); return c_; });
    const CAB = o.cabin || [[0, 0]], ease = x => x * x * (3 - 2 * x), lvAt = t => { let a = CAB[0][1]; for (let i = 0; i < CAB.length; i++) { const [t0, v0] = CAB[i], nx = CAB[i + 1]; if (t >= t0) a = nx && t < nx[0] ? v0 + (nx[1] - v0) * ease((t - t0) / (nx[0] - t0)) : v0; } return a; };
    g.userData.update = t => { const y = lvAt(t) * FH + 0.02; cab.position.set(SX, y, 0); for (const c_ of cables) { c_.position.y = y + 2.3; c_.scale.y = Math.max(0.01, H + 0.3 - y - 2.3); } };
    g.userData.update(0);
    g.userData.fh = FH; g.userData.shaftX = SX;
    g.userData.anchors = { center: [0, 0, 0], shaft: [SX, 0, 0], landing: [LXc, 0, 0], roof: [0, H, 0] };
    g.userData.sun = o.sun || [0.35, 0.7, 0.62];   // from the front, a little from the right: the open landings are lit
    g.userData.lighting = 'day'; return g;
  },
  holeSection(o = {}) { // the hole seen in cross-section, like a cartoon cutaway: the earth cut flat in front of the camera (strata, stones, a pipe, a bone, roots),
    // the shaft a slot 2*R wide down to its floor at y = 0, the street surface at y = o.depth (4.6) with the sky above. Characters stand at the bottom.
    const g = grp(), R = o.r ?? 1.0, D = o.depth ?? 4.6, X = 12, Y0 = -3, zc = R + 0.02;
    sky(g, o.sky || ['#62AEE2', '#A7D4EC']); clouds(g, 6, 8);
    const earth = (() => { const c = document.createElement('canvas'); c.width = 2048; c.height = Math.round(2048 * (D - Y0) / (2 * X)); const q = c.getContext('2d'), W = c.width, H = c.height, r = rng(o.seed || 21), yy = y => (D - y) / (D - Y0) * H, xx = x => (x + X) / (2 * X) * W;
      const bands = [[D, '#C9BEAC'], [D - 0.2, '#B8926A'], [D - 1.1, '#AC865E'], [D - 2.2, '#9E7953'], [D - 3.3, '#906C49'], [0.4, '#825F40'], [-1.2, '#735338'], [Y0, '#664930']];
      for (let i = 0; i < bands.length - 1; i++) { q.fillStyle = bands[i][1]; q.beginPath(); q.moveTo(0, yy(bands[i][0])); for (let x = 0; x <= W; x += 32) q.lineTo(x, yy(bands[i][0]) + (i ? 14 * Math.sin(x * 0.006 + i * 1.7) + 8 * Math.sin(x * 0.021 + i) : 0)); q.lineTo(W, H); q.lineTo(0, H); q.closePath(); q.fill(); }
      for (let i = 0; i < 520; i++) { const x = r() * W, y = yy(D - 0.25) + r() * (H - yy(D - 0.25)), s = 3 + r() * 12; q.fillStyle = ['#A08A70', '#5C4636', '#B9A88E', '#3E2E24'][i % 4]; q.globalAlpha = 0.55; q.beginPath(); q.ellipse(x, y, s, s * (0.5 + 0.4 * r()), r() * 3, 0, TAU); q.fill(); } q.globalAlpha = 1;
      for (let i = 0; i < 46; i++) { const x = r() * W, y = yy(D - 0.6) + r() * (H - yy(D - 0.6)) * 0.9, s = 16 + r() * 30; q.fillStyle = ['#84766A', '#93856F', '#6E6257'][i % 3]; q.beginPath(); q.ellipse(x, y, s, s * (0.55 + 0.3 * r()), r() * 3, 0, TAU); q.fill(); }   // stones: darker than the soil's light bands and without an outline (pale outlined ones were the brightest shapes of the shot, on the caption line)
      q.strokeStyle = '#4E3A2A'; q.lineCap = 'round'; for (let i = 0; i < 16; i++) { let x = r() * W, y = yy(D - 0.2); q.lineWidth = 6; q.beginPath(); q.moveTo(x, y); for (let k = 0; k < 6; k++) { x += (r() - 0.5) * 70; y += 16 + r() * 34; q.lineTo(x, y); q.lineWidth = Math.max(1.5, 6 - k); } q.stroke(); }   // roots
      const pipeY = yy(D - 1.55); q.fillStyle = '#7F8A93'; q.fillRect(0, pipeY - 20, W, 40); q.fillStyle = '#A5B0B8'; q.fillRect(0, pipeY - 20, W, 9); q.fillStyle = '#5E6870'; for (let x = 60; x < W; x += 230) q.fillRect(x, pipeY - 25, 16, 50);   // a water pipe (cut by the shaft)
      const bone = (x, y, a) => { q.save(); q.translate(xx(x), yy(y)); q.rotate(a); q.fillStyle = '#EFE9D8'; q.strokeStyle = '#3A2E26'; q.lineWidth = 3; q.beginPath(); q.rect(-34, -7, 68, 14); q.fill(); q.stroke(); for (const sx of [-1, 1]) for (const sy of [-1, 1]) { q.beginPath(); q.arc(sx * 36, sy * 8, 11, 0, TAU); q.fill(); q.stroke(); } q.fillRect(-33, -6, 66, 12); q.restore(); };
      bone(-3.1, 1.2, 0.4); bone(3.6, 2.5, -0.5);
      const amm = (x, y, s) => { q.save(); q.translate(xx(x), yy(y)); q.strokeStyle = '#D9CFB8'; q.lineWidth = 5; q.beginPath(); for (let a = 0; a < 15; a += 0.2) { const rr = 2 + a * s; q.lineTo(Math.cos(a) * rr, Math.sin(a) * rr); } q.stroke(); q.restore(); }; amm(2.4, 0.7, 2.6); amm(-4.4, 3.0, 2.0);
      const sock = (x, y) => { q.save(); q.translate(xx(x), yy(y)); q.rotate(0.5); q.fillStyle = '#E8E2D2'; q.strokeStyle = '#3A2E26'; q.lineWidth = 3; q.beginPath(); q.moveTo(-12, -40); q.lineTo(12, -40); q.lineTo(12, 6); q.lineTo(44, 14); q.lineTo(44, 34); q.lineTo(-12, 34); q.closePath(); q.fill(); q.stroke(); q.fillStyle = '#C8202A'; q.fillRect(-12, -34, 24, 7); q.fillRect(-12, -21, 24, 7); q.restore(); }; sock(-2.3, 2.1);   // a lost sock (story 36)
      const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t; })();
    const face = (x0, x1, y0, y1) => { const geo = new THREE.PlaneGeometry(x1 - x0, y1 - y0), uv = geo.attributes.uv, p = geo.attributes.position; for (let i = 0; i < uv.count; i++) uv.setXY(i, (p.getX(i) + (x0 + x1) / 2 + X) / (2 * X), (p.getY(i) + (y0 + y1) / 2 - Y0) / (D - Y0));
      const m = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ map: earth })); m.position.set((x0 + x1) / 2, (y0 + y1) / 2, zc); m.receiveShadow = true; return m; };
    g.add(face(-X, -R, Y0, D), face(R, X, Y0, D), face(-R, R, Y0, 0));
    // the shaft: back wall, side walls, floor (lighter near the top where the daylight comes in)
    const wallTex = (() => { const c = document.createElement('canvas'); c.width = 256; c.height = 1024; const q = c.getContext('2d'), gr = q.createLinearGradient(0, 0, 0, 1024); gr.addColorStop(0, '#D2B48E'); gr.addColorStop(0.35, '#BE9E78'); gr.addColorStop(1, '#9C7C5A'); q.fillStyle = gr; q.fillRect(0, 0, 256, 1024);
      const r = rng(5); for (let i = 0; i < 260; i++) { q.fillStyle = i % 2 ? 'rgba(60,44,32,0.35)' : 'rgba(200,180,150,0.3)'; const s = 3 + r() * 10; q.beginPath(); q.ellipse(r() * 256, r() * 1024, s, s * 0.6, r() * 3, 0, TAU); q.fill(); }
      for (let y = 60; y < 1024; y += 120) { q.strokeStyle = 'rgba(50,36,26,0.4)'; q.lineWidth = 4; q.beginPath(); q.moveTo(0, y); for (let x = 0; x <= 256; x += 32) q.lineTo(x, y + 8 * Math.sin(x * 0.05 + y)); q.stroke(); }
      const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
    const wm = new THREE.MeshLambertMaterial({ map: wallTex, color: '#FFF6E6' }), wm2 = new THREE.MeshLambertMaterial({ map: wallTex, color: '#E6D8C2' });
    const bw = new THREE.Mesh(new THREE.PlaneGeometry(2 * R, D), wm); bw.position.set(0, D / 2, -R); bw.receiveShadow = true; g.add(bw);
    for (const sd of [-1, 1]) { const sw = new THREE.Mesh(new THREE.PlaneGeometry(2 * R + 0.04, D), wm2); sw.position.set(sd * R, D / 2, 0.01); sw.rotation.y = -sd * PI / 2; sw.receiveShadow = true; g.add(sw); }
    const fl = mesh(new THREE.PlaneGeometry(2 * R, 2 * R + 0.04).rotateX(-PI / 2), mat('#A58260')); fl.position.set(0, 0.002, 0.01); fl.castShadow = false; g.add(fl);
    const rr = rng(8); for (let i = 0; i < 9; i++) g.add(at(box(0.06 + 0.08 * rr(), 0.04 + 0.04 * rr(), 0.06 + 0.07 * rr(), ['#8C7C68', '#7A6C5C', '#978570'][i % 3]), (rr() - 0.5) * 1.7 * R, 0.02, (rr() - 0.5) * 1.5 * R, 0, rr() * 3, 0));
    // the surface: pavement slabs either side of the hole, the street behind, a facade, a lamp, a tree
    for (const sd of [-1, 1]) { g.add(at(box(X - R, 0.2, 2 * R + 6, '#E4D6BE'), sd * (R + (X - R) / 2), D - 0.1, -3 + zc - R - 0.02 + R)); }
    g.add(at(box(2 * R, 0.2, 6, '#E4D6BE'), 0, D - 0.1, -R - 3));
    g.add(prop('haussmann', { color: '#EFE6D2', awning: '#B5302A', h: 15, floors: 6, cols: 5, w: 12.6, seed: o.facade ?? 9 }, 0.5, D, -7.5, 0), prop('haussmann', { color: '#F2DCCB', awning: '#2F7F5C', h: 17, floors: 6, cols: 5, w: 12.6, seed: (o.facade ?? 9) - 1 }, -12.2, D, -7.5, 0), prop('haussmann', { color: '#E8E1EE', awning: '#2F5E8C', h: 16, floors: 6, cols: 5, w: 12.6, seed: (o.facade ?? 9) + 1 }, 13.2, D, -7.5, 0));   // o.facade: the seed of the building behind the hole in the street set (parisStreet: seed = its index along the street)
    g.add(prop('streetLamp', {}, 2.9, D, -2.2), prop('tree', { seed: 11 }, -3.4, D, -2.6, 0, 1.0));
    if (o.light !== false) { const hl = prop('holeLight', { w: 2 * R * 0.9, h: D }, 0, 0, -R * 0.4); g.add(hl); g.userData.update = t => hl.userData.update(t); }
    g.userData.anchors = { center: [0, 0, 0], bottom: [0, 0, 0], surface: [0, D, 0], edgeL: [-R - 0.5, D, 0], edgeR: [R + 0.5, D, 0] };
    g.userData.sun = o.sun || [0.15, 0.62, 0.77]; g.userData.lighting = 'day'; return g;
  },
  mairie(o = {}) { // a town-hall office: cream walls with a wooden band, parquet, a tricolour "MAIRIE" banner, the official map on the back wall (x = o.mapX), a flag, filing cabinets, a big desk
    // o.wall / o.band / o.trim / o.floor / o.joint: its colours (another office in the same building: an insurer's in grey-green); o.banner false: no tricolour banner
    // (cycle 7) o.front (14): where the wall behind the visitor stands; o.frontSign { text, x, y, w, h }: a board on that wall, read from the clerk's side (a reverse shot must say where we are)
    const g = grp(), { back } = room(g, { wall: o.wall || '#EFE7D6', band: o.band || '#B98A5A', bandH: 1.0, trim: o.trim || '#7A5A3C', floor: o.floor || '#C7A77C', back: o.back ?? -2.6, half: 5, front: o.front });
    if (o.front != null) g.add(wall(10, 1.0, 0.04, o.band || '#B98A5A', 0, 0.5, o.front - 0.02), wall(10, 0.08, 0.08, o.trim || '#7A5A3C', 0, 1.04, o.front - 0.04));
    // (cycle 24, review 2 of 61) o.ceiling (m, or true = 3.6): a ceiling over the office with a plaster rose at (o.roseX, o.roseZ) for a hanging lamp
    // (a camera that looked up saw a pale void over the walls and the lamp hung from nothing); o.posters [{ text, x, y, w, h, bg, fg }]: boards on the
    // back wall; o.window { x, y, w, h }: a window in the back wall, sky behind the panes (another institution's room must not be the same brown box)
    if (o.ceiling) { const ch = o.ceiling === true ? 3.6 : +o.ceiling, fz = o.front ?? 14, bz = o.back ?? -2.6;
      const ceil = at(box(10.4, 0.12, fz - bz + 0.4, o.ceilingColor || '#F3EFE7'), 0, ch + 0.06, (fz + bz) / 2); ceil.castShadow = false;   // (stills 3 of 61) no shadow: casting one it put the whole office in the dark
      g.add(ceil, at(box(10.0, 0.1, 0.1, o.trim || '#7A5A3C'), 0, ch - 0.05, bz + 0.06));
      if (o.rose !== false) g.add(at(cyl(0.2, 0.25, 0.05, o.roseColor || '#E9E3D6', 18), o.roseX ?? 0, ch - 0.025, o.roseZ ?? 0)); }
    for (const q of o.posters || []) { const pw = q.w ?? 0.6, ph = q.h ?? 0.8, lb = label(q.text || '', pw, ph, { bg: q.bg || '#1B3A6B', fg: q.fg || '#F4F1E8', wrap: true });
      lb.position.set(q.x ?? 0, q.y ?? 2.0, (o.back ?? -2.6) + 0.05); g.add(lb, at(box(pw + 0.06, ph + 0.06, 0.03, q.frame || '#D9D2C2'), q.x ?? 0, q.y ?? 2.0, (o.back ?? -2.6) + 0.03)); }
    if (o.window) { const q = o.window, ww = q.w ?? 1.2, wh = q.h ?? 1.4, wx = q.x ?? 0, wy = q.y ?? 1.9, wz = (o.back ?? -2.6) + 0.04;
      g.add(at(box(ww, wh, 0.02, q.sky || '#A9D4EE', { emissive: q.sky || '#A9D4EE', noGrain: true }), wx, wy, wz));
      for (const [dx, dy, bw, bh] of [[0, wh / 2, ww + 0.1, 0.08], [0, -wh / 2, ww + 0.16, 0.1], [-ww / 2, 0, 0.08, wh], [ww / 2, 0, 0.08, wh], [0, 0, 0.05, wh], [0, wh * 0.15, ww, 0.05]])
        g.add(at(box(bw, bh, 0.06, q.frame || '#F4F1E8', { outline: 0.004 }), wx + dx, wy + dy, wz + 0.02)); }
    if (o.frontSign) { const q = o.frontSign, sw = q.w ?? 1.3, sh = q.h ?? sw * 0.26, z = (o.front ?? 14) - 0.03, lb = label(q.text || 'ÉTAT CIVIL', sw, sh, { bg: q.bg || '#1B2A4A', fg: q.fg || '#F4F1E8', wrap: false });
      lb.position.set(q.x ?? 0, q.y ?? 2.6, z - 0.03); lb.rotation.y = PI; g.add(lb, at(box(sw + 0.08, sh + 0.08, 0.04, '#C9A24B'), q.x ?? 0, q.y ?? 2.6, z)); }
    for (let i = -6; i <= 6; i++) g.add(flat(0.03, 12, o.joint || '#A88A62', i * 0.8, 0.004, 1));   // parquet joints
    const bx = o.bannerX ?? 0, by = o.bannerY ?? 3.25;
    if (o.banner !== false) { g.add(at(box(3.3, 0.5, 0.03, '#F4F1E8', { outline: 0.004 }), bx, by, back + 0.03), at(box(1.1, 0.5, 0.032, '#2A4B9B'), bx - 1.1, by, back + 0.032), at(box(1.1, 0.5, 0.032, '#C8202A'), bx + 1.1, by, back + 0.032));
      g.add(at(label(o.title || 'MAIRIE', 1.05, 0.36, { bg: '#F4F1E8', fg: '#1B2A4A', wrap: false }), bx, by, back + 0.05)); }
    if (o.map !== false) g.add(at(buildProp('officialMap', { stamp: o.stamp }), o.mapX ?? -1.35, o.mapY ?? 2.05, back + 0.04));
    if (o.board) { const b = at(buildProp('nowhereBoard', o.board), o.boardX ?? 1.3, o.boardY ?? 2.05, back + 0.04); g.add(b); const up = g.userData.update; g.userData.update = t => { up?.(t); b.userData.update?.(t); }; }
    g.add(prop('flag', { colors: ['#2A4B9B', '#F4F1E8', '#C8202A'] }, o.flagX ?? 2.9, 0, back + 0.45, 0, 1.5));
    for (const x of [-3.6, -4.3]) { g.add(at(box(0.62, 1.5, 0.5, '#9AA3A8', { pivot: 'bottom', outline: 0.006 }), x, 0, back + 0.3)); for (let k = 0; k < 4; k++) g.add(at(box(0.52, 0.3, 0.02, '#B4BCC1', { outline: 0.01 }), x, 0.2 + k * 0.36, back + 0.56), at(box(0.14, 0.03, 0.03, '#5A6268'), x, 0.24 + k * 0.36, back + 0.58)); }
    g.add(prop('plant', { seed: 5 }, 4.2, 0, back + 0.6), prop('wallClock', { rate: 1 / 60 }, o.clockX ?? 3.6, 2.9, back + 0.03));
    const dz = o.deskZ ?? -0.9, dx = o.deskX ?? 0, dk = o.desk || '#8A6A45', ds = o.deskSide || '#7A5A3C'; if (o.desk !== false) g.add(at(box(1.9, 0.07, 0.85, dk, { outline: 0.005 }), dx, 0.78, dz), at(box(1.8, 0.74, 0.04, ds), dx, 0.37, dz + 0.38), at(box(0.06, 0.76, 0.75, ds), dx - 0.88, 0.38, dz), at(box(0.06, 0.76, 0.75, ds), dx + 0.88, 0.38, dz));   // o.desk / o.deskSide: its colours; o.deskX / o.deskZ: where it stands
    if (o.desk !== false) g.add(at(box(0.34, 0.012, 0.24, '#F4F1E8'), dx - 0.5, 0.822, dz + 0.05, 0, 0.2, 0), at(box(0.3, 0.05, 0.22, '#5A3A28', { outline: 0.01 }), dx + 0.62, 0.84, dz - 0.1), at(box(0.16, 0.03, 0.1, '#2A2A2E'), dx + 0.62, 0.875, dz - 0.1));   // papers, an in-tray, an ink pad (o.desk false: no desk and nothing on it: a scene prop replaces it, e.g. splitDesk)
    if (o.plate !== false && o.desk !== false) g.add(at(label(o.plate || 'ÉTAT CIVIL', 0.5, 0.11, { bg: '#1B2A4A', fg: '#F4F1E8', wrap: false }), dx, 0.55, dz + 0.405));
    g.userData.anchors = { center: [0, 0, 0], desk: [dx, 0.82, dz], clerk: [dx, 0, dz - 0.75], visitor: [dx, 0, dz + 1.3] };
    g.userData.sun = o.sun || [0.3, 0.75, 0.6]; g.userData.lighting = 'day'; return g;
  },
  stationInside(o = {}) { // inside a space module: pale panelled walls with handrails and lockers, grey consoles, a round window on the Earth (back wall, x = o.winX), soft white light
    const g = grp(), back = -2.4, half = 3.2;
    room(g, { wall: '#EFE6D2', floor: '#D9CFBC', back, half, height: 4, front: 6 });
    g.add(at(box(2 * half + 0.6, 0.2, 9.0, '#DCE1E6'), 0, 4.1, 1.8));   // ceiling (a module, not a room under the sky)
    for (let i = -3; i <= 3; i++) g.add(at(box(0.04, 3.6, 0.03, '#C3C9CF'), i * 0.9, 1.9, back + 0.02));
    for (const y of [0.9, 2.6]) g.add(at(box(2 * half - 0.4, 0.05, 0.08, '#F2C230'), 0, y, back + 0.08));
    const cable = (pts, c) => { for (let q = 0; q < pts.length - 1; q++) { const [x0, y0] = pts[q], [x1, y1] = pts[q + 1], L = Math.hypot(x1 - x0, y1 - y0), m = at(box(L, 0.035, 0.035, c), (x0 + x1) / 2, (y0 + y1) / 2, back + 0.1); m.rotation.z = Math.atan2(y1 - y0, x1 - x0); g.add(m); } };
    cable([[-3.0, 3.4], [-2.2, 3.1], [-1.4, 3.35], [-0.4, 3.0], [0.8, 3.3]], '#2A2D33'); cable([[0.6, 3.6], [1.5, 3.2], [2.4, 3.45], [3.0, 3.1]], '#D7262E'); cable([[-3.0, 0.5], [-2.1, 0.35], [-1.0, 0.55]], '#2C4A8A');
    [[-2.7, 2.2, '#4F7FB5'], [2.75, 2.4, '#7A8794'], [-1.9, 0.25, '#4F7FB5'], [2.2, 0.3, '#C9824E']].forEach(([x, y, c]) => g.add(at(box(0.55, 0.42, 0.25, c, { outline: 0.008 }), x, y, back + 0.16), at(box(0.5, 0.04, 0.26, '#F2C230'), x, y + 0.12, back + 0.17)));   // stowage bags
    for (const x of [-1.6, 1.6]) g.add(at(box(0.6, 0.06, 0.4, '#FFF4C8', { emissive: '#FFE7A0', noGrain: true }), x, 3.85, -0.6));   // warm ceiling lights
    [[-2.4, 1.5], [-1.5, 0.6], [1.6, 0.7], [2.5, 1.6]].forEach(([x, y]) => { g.add(at(box(0.7, 0.5, 0.12, '#B9C0C7', { outline: 0.008 }), x, y, back + 0.07));
      for (let k = 0; k < 4; k++) g.add(at(box(0.07, 0.07, 0.02, ['#3CC46E', '#D7262E', '#F2C230', '#3C8DD9'][k]), x - 0.2 + k * 0.13, y + 0.1, back + 0.14)); });
    const wx = o.winX ?? 0.2, win = canvasPlane(1.1, 1.1, (c, W, H) => { c.fillStyle = '#05091A'; c.fillRect(0, 0, W, H); c.fillStyle = '#FFFFFF'; for (let i = 0; i < 40; i++) c.fillRect((i * 53 % 97) / 97 * W, (i * 31 % 89) / 89 * H, 2, 2);
      const gr = c.createRadialGradient(W * 0.55, H * 1.25, H * 0.2, W * 0.55, H * 1.25, H * 0.95); gr.addColorStop(0, '#2E7FD1'); gr.addColorStop(0.85, '#4FA3E0'); gr.addColorStop(1, '#BFE3FF'); c.fillStyle = gr; c.beginPath(); c.arc(W * 0.55, H * 1.25, H * 0.9, 0, TAU); c.fill();
      c.fillStyle = '#5FAF5A'; c.beginPath(); c.ellipse(W * 0.42, H * 0.62, W * 0.12, H * 0.06, 0.3, 0, TAU); c.fill(); c.beginPath(); c.ellipse(W * 0.7, H * 0.74, W * 0.1, H * 0.05, -0.2, 0, TAU); c.fill(); }, { res: 256, emissive: 0.9 });
    g.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.6, 0.08, 6, 24), mat('#AEB5BC')), wx, 2.0, back + 0.06), at(win, wx, 2.0, back + 0.04));
    g.userData.anchors = { center: [0, 0, 0], window: [wx, 2.0, back] }; g.userData.lighting = 'day'; return g;
  },
  spaceDark(o = {}) { // deep space: navy gradient dome + stars; the Earth goes in as a prop
    const g = grp(); sky(g, o.sky || ['#050913', '#0E1A33']); g.add(prop('stars', { radius: 150, count: o.stars || 600 }));
    g.userData.anchors = { center: [0, 0, 0] }; g.userData.lighting = o.lighting || 'day'; return g;
  },
  brightCell(o = {}) { // a clean, sunlit prison cell: pale concrete walls, bunk, toilet, a small barred window of blue sky, bars across the front (z = 1.6)
    const g = grp(), W = o.w || 3.2, D = o.d || 3.4, H = o.h || 2.8;
    g.add(flat(W + 6, D + 8, '#B9BCB8', 0, 0, 0));
    g.add(wall(W, H, 0.2, '#D9DAD3', 0, H / 2, -D / 2), wall(0.2, H, D, '#CFD1CA', -W / 2, H / 2, 0), wall(0.2, H, D, '#CFD1CA', W / 2, H / 2, 0), wall(W, 0.2, D, '#E4E5DF', 0, H, 0));
    const win = grp(at(box(0.7, 0.5, 0.05, '#7FC2EE', { emissive: '#7FC2EE' }), 0, 0, 0)); for (let i = 0; i < 4; i++) win.add(at(box(0.04, 0.5, 0.06, '#3A3D44'), -0.27 + i * 0.18, 0, 0.03)); win.position.set(0.4, 2.0, -D / 2 + 0.12); g.add(win);
    g.add(at(box(0.9, 0.12, 1.9, '#8E7A62'), -W / 2 + 0.55, 0.45, -0.4), at(box(0.85, 0.1, 1.8, '#E8E4D8'), -W / 2 + 0.55, 0.56, -0.4));
    g.add(at(box(0.4, 0.42, 0.5, '#F2F2EE'), W / 2 - 0.35, 0.21, -D / 2 + 0.4));
    if (o.bars !== false) g.add(prop('jailBars', { width: W, height: H }, 0, 0, D / 2 - 0.1));
    if (o.sign) g.add(at(label(o.sign, 1.1, 0.42, { bg: '#F4F1E8', fg: '#1E2A33' }), 0.75, 1.75, -D / 2 + 0.12));
    g.add(at(box(W + 10, H + 3, 0.3, '#C9CBC4'), 0, (H + 3) / 2, D / 2 + 3.2));   // corridor wall behind the camera
    g.userData.anchors = { center: [0, 0, 0] }; g.userData.lighting = 'day'; return g;
  },
});

Object.assign(S, {
  seaSurface(o = {}) { // open sea in the replica's light: low-poly waves (moving), a sandy beach toward +Z, parasols, the bright sky
    const g = grp(), r = rng(o.seed || 21);
    sky(g, o.sky || ['#62AEE2', '#A7D4EC']); clouds(g, 9, 8);
    const geo = new THREE.PlaneGeometry(420, 420, 84, 84).rotateX(-PI / 2), pos = geo.attributes.position, base = pos.array.slice();
    const shore = o.shore ?? 6, sea = mesh(geo, mat(o.sea || '#2FA5D2')); sea.receiveShadow = true; sea.castShadow = false; sea.position.z = -210 + shore + 0.6; g.add(sea);   // the sea ends under the foam line: the beach stays dry
    const sand = flat(420, 60, o.sand || '#EAD9A8', 0, 0.02, (o.shore ?? 6) + 30); g.add(sand);
    const foam = flat(420, 1.2, '#F4FBFF', 0, 0.05, (o.shore ?? 6) + 0.4); g.add(foam);
    if (o.parasols !== false) { g.add(prop('parasol', {}, 6, 0, (o.shore ?? 6) + 6)); g.add(prop('parasol', { color: '#F2C230' }, -9, 0, (o.shore ?? 6) + 9)); }
    g.userData.update = t => { for (let i = 0; i < pos.count; i++) { const x = base[i * 3], z = base[i * 3 + 2], damp = Math.min(1, Math.max(0.1, (shore - z - sea.position.z) / 5));   // calmer near the beach
        pos.array[i * 3 + 1] = damp * (0.16 * Math.sin(x * 0.45 + t * 1.6) + 0.12 * Math.sin(z * 0.6 + t * 1.2) + 0.05 * Math.sin((x + z) * 1.3 + t * 2.4)); } pos.needsUpdate = true; geo.computeVertexNormals(); };
    g.userData.update(0);
    g.userData.anchors = { center: [0, 0, 0] }; g.userData.lighting = 'day'; return g;
  },
  seabed(o = {}) { // under the sea: pale sand with dunes and rocks, seaweed, light shafts, the rippling surface overhead, blue haze
    const g = grp(), r = rng(o.seed || 23), W = o.dry ? null : true;
    sky(g, o.dry ? (o.sky || ['#62AEE2', '#A7D4EC']) : (o.water || ['#2E8DB5', '#1C6A8F']));
    g.add(ground(o.sand || (o.dry ? '#D8C99E' : '#E2DBC1')));
    for (let i = 0; i < 26; i++) { const a = r() * TAU, d = 8 + r() * 60, m = sphere(1, o.dry ? '#CDBE93' : '#D9D2B6', 1); m.scale.set(4 + r() * 6, 0.6 + r() * 1.2, 3 + r() * 5); m.position.set(Math.cos(a) * d, -0.3, Math.sin(a) * d - 10); m.castShadow = false; g.add(m); }
    const rocks = new THREE.DodecahedronGeometry(1, 0);
    for (let i = 0; i < 30; i++) { const m = mesh(rocks, mat(['#8E99A0', '#7F8A91', '#9AA4AA'][i % 3])); const s = 0.3 + r() * 1.1; m.scale.set(s * 1.4, s * 0.7, s); m.position.set((r() - 0.5) * 70, s * 0.25, -r() * 70 + 12); m.rotation.set(r() * 3, r() * 3, r() * 3); g.add(m); }
    if (!o.dry) {
      for (let i = 0; i < 18; i++) g.add(prop('seaweed', { seed: i + 3, n: 4 + (i % 4), h: 1.0 + r() * 1.4 }, (r() - 0.5) * 40, 0, -r() * 45 + 8));
      g.add(prop('lightRays', { n: 7, w: 50, d: 50, h: 32 }, 0, 0, 0));
      const surf = mesh(new THREE.PlaneGeometry(400, 400, 1, 1).rotateX(PI / 2), new THREE.MeshBasicMaterial({ color: '#7FD3F0', transparent: true, opacity: 0.35, side: THREE.DoubleSide, fog: false })); surf.position.y = o.surfaceY || 30; g.add(surf);
      g.add(prop('bubbles', { rate: 1.2, h: 12, area: 30, seed: 9 }, 0, 0, -12));
      Object.assign(g.userData, { fog: { color: o.fog || '#2678A0', near: o.fogNear || 10, far: o.fogFar || 75 }, light: { sky: '#A8DCF2', ground: '#6A9AAA', key: '#EAF7FF' } });
    } else {
      for (let i = 0; i < 10; i++) g.add(prop('seaweed', { seed: i + 30, n: 3, h: 0.5 }, (r() - 0.5) * 30, 0, -r() * 30 + 5));
    }
    g.userData.anchors = { center: [0, 0, 0] }; g.userData.lighting = 'day'; return g;
  },
});


Object.assign(S, {
  laundryRoom(o = {}) { // « Les chaussettes »: a bright laundry corner — pale blue walls, a white tiled band, the big washing machine (o.washer === false: a scene
    // bigWasher replaces it; anchors.washer is its spot), a shelf of washing powder, a basket of laundry, a clothes horse with socks, a sunny window
    const g = grp(), { back, half } = room(g, { wall: '#C9DFEA', band: '#F4F6F8', bandH: 1.1, trim: '#6F9DB5', floor: '#D9DEE1', half: 6 });
    const tiles = []; for (let i = -10; i < 10; i++) for (let j = 0; j < 20; j++) if ((i + j) % 2 === 0) tiles.push([i * 0.5 + 0.25, 0.003, back + j * 0.5 + 0.25]);
    g.add(inst(new THREE.PlaneGeometry(0.5, 0.5).rotateX(-PI / 2), mat('#B7C2CA'), tiles));
    g.add(at(box(2 * half, 0.12, 0.03, '#4F6B7D', { pivot: 'bottom' }), 0, 0, back + 0.03));   // a dark skirting board: one deeper value for depth
    for (const sx of [-1, 1]) g.add(at(box(0.03, 0.12, 20, '#4F6B7D', { pivot: 'bottom' }), sx * (half - 0.03), 0, back + 10));
    if (o.washer !== false) g.add(prop('bigWasher', { open: o.open ?? 0 }, -1.2, 0, back + 0.62));
    g.add(at(box(2.2, 0.05, 0.4, '#E8E1D0', { outline: 0.006 }), 1.4, 2.0, back + 0.2));   // shelf
    [['#3C8DD9', 0.7], ['#E0413A', 1.15], ['#F2C230', 1.55], ['#7FC4B2', 1.95]].forEach(([c, x]) => g.add(at(box(0.3, 0.42, 0.22, c, { pivot: 'bottom', outline: 0.006 }), x, 2.025, back + 0.2),
      at(box(0.31, 0.1, 0.225, '#FFFFFF', { pivot: 'bottom' }), x, 2.2, back + 0.2)));
    g.add(prop('window', { w: 1.1, h: 0.9, color: P.cream }, 1.5, 1.35, back));
    g.add(at(canvasPlane(1.06, 0.86, (c, W, H) => { const gr = c.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#8CC8F0'); gr.addColorStop(1, '#D8EEFA'); c.fillStyle = gr; c.fillRect(0, 0, W, H); c.fillStyle = '#FFFFFF'; c.beginPath(); c.ellipse(W * 0.3, H * 0.35, W * 0.16, H * 0.07, 0, 0, TAU); c.fill(); }, { res: 256, emissive: 0.9 }), 1.5, 1.35, back + 0.01));
    // laundry basket with clothes, a clothes horse with socks (all in pairs but one)
    const bask = mesh(new THREE.CylinderGeometry(0.34, 0.28, 0.42, 14, 1, true), mat('#C99A5A', { doubleSide: true })); bask.position.set(0.55, 0.21, back + 0.75); g.add(bask, at(cyl(0.3, 0.3, 0.1, '#7FA8D9', 10), 0.55, 0.36, back + 0.75), at(cyl(0.22, 0.22, 0.1, '#F2C94C', 10), 0.62, 0.42, back + 0.72));
    g.add(prop('dryingRack', { w: 1.2 }, 2.6, 0, back + 1.4, -0.3));
    g.add(hangLamp(0, 3.2, -0.5, '#F4F6F8', 6));
    g.userData.anchors = { center: [0, 0, 0], washer: [-1.2, 0, back + 0.62], washerFront: [-1.2, 0, back + 1.9] };
    g.userData.sun = [0.45, 0.6, 0.66]; g.userData.lighting = 'interior'; return g;
  },
  drumTunnel(o = {}) { // inside the drum: a perforated steel tube running away along -Z (axis y = R, so its bottom is the floor at y = 0), three lifters,
    // socks drifting in the air, a bright round exit far down the tube (the kingdom's light), the porthole behind (z = 9)
    const g = grp(), R = o.r || 1.3, L = o.len || 34, z0 = 9;
    const geo = new THREE.CylinderGeometry(R, R, L, 40, 1, true); geo.rotateX(PI / 2); geo.translate(0, R, z0 - L / 2);
    const c = document.createElement('canvas'); c.width = c.height = 256; const x2 = c.getContext('2d'); const gr = x2.createLinearGradient(0, 0, 256, 0); gr.addColorStop(0, '#B9C0C8'); gr.addColorStop(0.5, '#DDE2E7'); gr.addColorStop(1, '#B9C0C8'); x2.fillStyle = gr; x2.fillRect(0, 0, 256, 256);
    x2.fillStyle = '#4A4F57'; for (let y = 0; y < 8; y++) for (let x = 0; x < 8; x++) { x2.beginPath(); x2.arc(x * 32 + (y % 2 ? 16 : 0) + 8, y * 32 + 16, 6.5, 0, TAU); x2.fill(); }
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(14, 22);
    const tube = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ map: t, side: THREE.BackSide })); tube.receiveShadow = true; g.add(tube);
    for (let i = 0; i < 3; i++) { const a = -PI / 2 + i * TAU / 3 + PI / 3; g.add(at(box(0.22, 0.16, L, '#C9CED4', { outline: 0.008 }), Math.cos(a) * (R - 0.08), R + Math.sin(a) * (R - 0.08), z0 - L / 2, 0, 0, a + PI / 2)); }
    const exitZ = z0 - L + 0.05;
    g.add(at(new THREE.Mesh(new THREE.CircleGeometry(R * 0.98, 40), new THREE.MeshBasicMaterial({ color: '#FFF4D8', toneMapped: false })), 0, R, exitZ));
    const lamp = new THREE.PointLight('#FFE7B8', o.exitLight ?? 9, 30, 1.4); lamp.position.set(0, R, exitZ + 1.5); g.add(lamp);
    g.add(at(new THREE.Mesh(new THREE.CircleGeometry(R, 40), new THREE.MeshLambertMaterial({ color: '#7FA6BE', side: THREE.DoubleSide })), 0, R, z0 + 0.02, 0, PI, 0));   // the porthole glass, from inside
    g.add(at(torus(R, 0.12, '#C9CCD1', 8, 40), 0, R, z0));
    const r = rng(o.seed || 5), socks = []; for (let i = 0; i < (o.socks ?? 7); i++) { const s = prop('sockSingle', { colors: [['#D9453A', '#F4F1E8', '#F4F1E8'], ['#2F5E8C', '#F2C94C', '#F2C94C'], ['#4CA36C', '#F4F1E8', '#2C6E4A'], ['#F2C94C', '#E0413A', '#E0413A'], ['#8E5BB5', '#F4F1E8', '#F4F1E8']][i % 5] }); s.scale.setScalar(1.4); g.add(s); socks.push({ s, x: (r() - 0.5) * 1.4, y: 0.7 + r() * 1.2, z: z0 - 3 - r() * 22, ph: r() * TAU }); }
    g.userData.update = tt => { for (const k of socks) { k.s.position.set(k.x + 0.25 * Math.sin(tt * 0.9 + k.ph), k.y + 0.15 * Math.sin(tt * 1.3 + k.ph), k.z + tt * 0.6); k.s.rotation.set(tt * 0.7 + k.ph, tt * 0.5, 0.4 * Math.sin(tt + k.ph)); } };
    g.userData.update(0);
    g.userData.anchors = { center: [0, 0, 0], exit: [0, 0, exitZ] };
    g.userData.lighting = 'interior'; return g;
  },
  sockKingdom(o = {}) { // the kingdom of lost socks at the bottom of the drum: soft lint plains and hills, thousands of socks lying about, a laundry-basket castle,
    // soap bubbles in a lilac sky, and high in the sky the porthole of the machine (the way home); throne at anchors.throne
    const g = grp(); sky(g, o.sky || ['#8FC2EE', '#F3DDF0']);
    for (let i = 0; i < 6; i++) g.add(prop('cloud', { seed: 70 + i, scale: 3 + (i % 3) }, (i / 5 - 0.5) * 140, 16 + (i % 2) * 8, -60 - (i % 3) * 15, 0.2 * i));
    g.add(ground('#CBD3E2'));
    hills(g, ['#C3CDE0', '#D8CFE6', '#C9DCE0'], { seed: 6, n: 7, z0: -30, z1: -60, sx: 16, sy: 5 });
    const r = rng(o.seed || 8);
    for (let i = 0; i < 9; i++) { const m = sphere(1, ['#D3DAE8', '#DCD2EA', '#CFE0E4'][i % 3], 1); m.scale.set(2.5 + r() * 2, 0.5 + r() * 0.6, 2 + r() * 1.5); m.position.set((r() - 0.5) * 30, 0, -6 - r() * 16); m.castShadow = false; m.receiveShadow = true; g.add(m); }   // lint mounds
    g.add(prop('sockSea', { n: o.n ?? 2200, w: 74, d: 56, seed: 9, clear: [[0, -3, 4.2], [0, 4, 3.0]], heaps: [[-15, -22, 7, 4.5], [13, -25, 8, 5.5], [-27, -11, 6, 3.2], [25, -10, 6.5, 3.5], [-6, -27, 5, 3], [4, -12, 2.2, 1.0], [-9, -6, 2.0, 0.8], [9, -4, 1.8, 0.7]] }, 0, 0, -6));
    if (o.crowd) g.add(prop('sockCrowd', { n: o.crowd === true ? 240 : o.crowd, w: 26, d: 16, seed: 12, face: o.crowdFace || [1.2, 9], clear: [[0, 3.5, 2.6], [0, -2.6, 3.0], ...(o.crowdClear || [])] }, 0, 0, -3));
    if (o.castle !== false) { g.add(prop('laundryCastle', { size: 1.1 }, 0, 0, -13)); g.add(prop('throne', { size: 1 }, 0, 0, -8.6)); }
    g.add(prop('soapBubbles', { n: 22, w: 26, h: 10, d: 16, size: 0.35 }, 0, 0.5, -8));
    const port = grp(at(torus(16, 1.6, '#C9CCD1', 10, 48), 0, 0, 0), at(new THREE.Mesh(new THREE.CircleGeometry(16, 48), new THREE.MeshBasicMaterial({ color: '#BFD9E6', transparent: true, opacity: 0.55, fog: false, toneMapped: false })), 0, 0, -0.2));
    port.position.set(-30, 46, -120); port.lookAt(0, 0, 0); port.traverse(n => { if (n.isMesh) { n.castShadow = false; n.material.fog = false; } }); g.add(port);
    g.userData.anchors = { center: [0, 0, 0], throne: [0, 0, -8.6], seat: [0, 0.7, -8.55], gate: [0, 0, -10.4] };
    g.userData.sun = [0.35, 0.72, 0.6]; g.userData.lighting = 'day'; return g;
  },
});

export const SET_NAMES = Object.keys(S);

export function buildSet(name, opts = {}) {
  let g;
  try { g = S[name] ? S[name](opts || {}) : null; } catch (e) { console.warn('[sets] failed to build', name, e.message); g = null; }
  if (!g) { // unknown or broken set -> clean void with a sign so it's obvious
    g = S.whiteVoid({}); g.add(prop('signBoard', { text: String(name), w: 2, h: 0.6, height: 2.2 }, 0, 0, -4));
  }
  g.name = 'set:' + name; g.userData.set = name;
  g.userData.anchors ||= { center: [0, 0, 0] };
  return g;
}
