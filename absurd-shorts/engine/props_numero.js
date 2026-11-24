// « Le faux numéro » (story 94): this man called his barber and got the wrong number: the general staff took every barber phrase as an order;
// the sides cleared (the army evacuated both coasts), a little off the front (the front fell back ten kilometres, a village changed country),
// a fade at the back (the excavators cut the hinterland into steps), a parting down the middle (the country cut in two), a little gel (the
// government froze the wages); seen from space the country has a perfect haircut and two jets hold the mirror behind it; the same day the
// general got the wrong number too, the barber answered: shave it all; this man was in the chair, he only wanted the tips.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere, mat, rng } from './style.js';
import { grp, at, canvasPlane, buildProp, rod } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const noShadow = m => { m.traverse(c => { c.castShadow = false; }); return m; };
// a value keyed in time: keys [[t, v], ...] (sorted), linear between keys (a number: constant)
function lin(keys, t, def = 0) {
  if (keys == null) return def;
  if (typeof keys === 'number') return keys;
  if (!keys.length) return def;
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) if (t < keys[i][0]) { const [a, va] = keys[i - 1], [b, vb] = keys[i]; return va + (vb - va) * clamp01((t - a) / Math.max(1e-6, b - a)); }
  return keys[keys.length - 1][1];
}
const inWin = (wins, t) => (wins || []).some(([a, b]) => t >= a && t < b);
function wob(ts, t, a = 1, w = 22, d = 4.3) { let s = 0; for (const t0 of [].concat(ts ?? [])) { const u = t - t0; if (u >= 0) s += a * Math.sin(u * w) * Math.exp(-u * d); } return s; }
const lerpC = (a, b, u) => new THREE.Color(a).lerp(new THREE.Color(b), clamp01(u));

// ---------------------------------------------------------------------------------------------------------------- the felt country
// The made-up country (no real outline): an oval a little taller than wide with soft bumps, in map units u, v in [-1, 1] (u across, v up).
// The same function is copied in story_numero.py (shape()) to aim the tools at its edges.
function shapeR(u, v) { const th = Math.atan2(v, u); return 1 + 0.06 * Math.sin(3 * th + 0.6) + 0.045 * Math.sin(5 * th + 2.1) + 0.025 * Math.sin(8 * th + 0.4); }
function inside(u, v) { return Math.hypot(u / 0.9, v / 0.94) < shapeR(u, v); }
const GREENS = ['#3E8A36', '#4A9A3E', '#357E30', '#56A646', '#43913A'];
const SAND = '#D8C98E';
// The felt hair (pivot at the middle of the map, the map in the XY plane, the hair growing toward +Z): o.w x o.h metres, a tuft every o.step,
// tufts o.len long (thick green felt), a dark green ground under them. The states, each a progress 0..1 keyed in time:
//   o.sides: the sides buzzed (|lateral| > 0.6), swept from the top down: short sandy stubble;
//   o.top: the front (the top band, v > 0.62) trimmed, swept left to right: short, darker; o.dropAt: the cut strip of felt falls off toward +Z;
//   o.back: the back (v < -0.3) combed into four big ridges, swept left to right: the hair stands straight, ridged, light crests and dark troughs;
//   o.part: a parting down the middle (|u| < 0.035), swept from the top down: bare dark line, the hair beside it combed away from it;
//   o.gel: the whole head gelled: brighter, combed smooth and a white shine streak; o.blob [[t, 0..1]]: a blob of blue gel at o.blobAt [u, v];
//   o.fly: tufts that fly off toward +Z where the sides are buzzed (o.flyN per side, o.flyS size); a number of keys: all states at that value.
function feltCore(o) {
  const W = o.w ?? 1.6, H = o.h ?? 1.9, step = o.step ?? 0.04, L0 = o.len ?? 0.09, g = grp();
  const nx = Math.round(W / step), ny = Math.round(H / step), cells = [];
  // the half-width of each row (left and right extents) for the lateral coordinate
  const rowL = [], rowR = [];
  for (let j = 0; j < ny; j++) { const v = -1 + (j + 0.5) * 2 / ny; let l = 0, r = 0; for (let i = 0; i < 400; i++) { const u = -1.2 + i * 2.4 / 400; if (inside(u, v)) { if (u < l) l = u; if (u > r) r = u; } } rowL.push(l); rowR.push(r); }
  let vTop = -1, vBot = 1; for (let j = 0; j < ny; j++) { const v = -1 + (j + 0.5) * 2 / ny; if (rowR[j] > 0.01) { vTop = Math.max(vTop, v); vBot = Math.min(vBot, v); } }
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
    const k = j * nx + i, u = -1 + (i + 0.5 + (hsh(k) - 0.5) * 0.5) * 2 / nx, v = -1 + (j + 0.5 + (hsh(k + 7) - 0.5) * 0.5) * 2 / ny;
    if (!inside(u, v)) continue;
    const lat = u < 0 ? -u / Math.max(0.05, -rowL[j]) : u / Math.max(0.05, rowR[j]);
    cells.push({ u, v, lat, x: u * W / 2, y: v * H / 2, h: 0.75 + 0.5 * hsh(k + 3), ax: (hsh(k + 11) - 0.5) * 0.7, ay: (hsh(k + 13) - 0.5) * 0.7, c: GREENS[Math.floor(hsh(k + 17) * GREENS.length)], k });
  }
  // the ground under the hair: the country's shape, dark green
  const sh = new THREE.Shape(); for (let i = 0; i <= 96; i++) { const th = i / 96 * TAU, R = shapeR(Math.cos(th), Math.sin(th)), u = 0.9 * R * Math.cos(th) * 0.995, v = 0.94 * R * Math.sin(th) * 0.995; const x = u * W / 2, y = v * H / 2; i ? sh.lineTo(x, y) : sh.moveTo(x, y); }
  const ground = new THREE.Mesh(new THREE.ShapeGeometry(sh), mat(o.ground || '#2C5A28')); ground.position.z = 0.002; ground.receiveShadow = true; g.add(ground);
  const geo = new THREE.BoxGeometry(1, 1, 1); geo.translate(0, 0.5, 0);
  const pos = geo.attributes.position; for (let i = 0; i < pos.count; i++) { const y = pos.getY(i); pos.setX(i, pos.getX(i) * (1 - 0.55 * y)); pos.setZ(i, pos.getZ(i) * (1 - 0.55 * y)); } geo.computeVertexNormals();
  const hm = new THREE.MeshLambertMaterial({ color: '#FFFFFF', flatShading: true });
  const im = new THREE.InstancedMesh(geo, hm, cells.length); im.castShadow = false; im.receiveShadow = true; g.add(im);
  const dum = new THREE.Object3D(), col = new THREE.Color(), wid = step * 1.5;
  // the cut strip of the front (a felt band that falls off)
  let strip = null;
  if (o.dropAt != null) { strip = grp(); const sw = W * 0.62, shh = H * 0.1; strip.add(at(box(sw, shh, L0 * 0.7, '#3F8A36', { outline: 0.004 }), 0, 0, L0 * 0.35));
    for (let i = 0; i < 26; i++) strip.add(at(box(step * 1.4, step * 1.4, L0 * 0.8, GREENS[i % 5], { taper: 0.5, taperAxis: 'z' }), -sw / 2 + (i + 0.5) * sw / 26, (hsh(i) - 0.5) * shh * 0.6, L0 * 0.8));
    g.add(strip); }
  // tufts that fly off the buzzed sides
  const flies = [];
  if (o.fly && o.sides && o.sides.length > 1) { const s0 = o.sides.find(kv => kv[1] > 0) || o.sides[0], t0 = (o.sides[Math.max(0, o.sides.indexOf(s0) - 1)] || s0)[0], t1 = o.sides[o.sides.length - 1][0], n = o.flyN ?? 6;
    for (const sd of [-1, 1]) for (let i = 0; i < n; i++) { const tg = grp(), fs = o.flyS ?? 0.09; for (let q = 0; q < 4; q++) tg.add(at(box(fs * (0.5 + 0.3 * hsh(i + q)), fs * (0.9 + 0.4 * hsh(i * 3 + q)), fs * 0.5, GREENS[(i + q) % 5], { taper: 0.4 }), (hsh(q + i) - 0.5) * fs, 0, (hsh(q + 2 * i) - 0.5) * fs * 0.5, 0, 0, (q - 1.5) * 0.4)); tg.visible = false; g.add(tg);
      flies.push({ tg, sd, te: t0 + (t1 - t0) * (i + 0.5) / n, vx: sd * (0.5 + 0.6 * hsh(i * 5 + sd)), vz: 1.6 + 0.9 * hsh(i * 7 + sd), vy: 0.5 + 0.6 * hsh(i * 9), sp: (hsh(i) - 0.5) * 14 }); } }
  // the gel: a shine streak and a blob
  const shine = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0, depthWrite: false }));
  shine.scale.set(W * (o.shineW ?? 0.05), H * 0.55, 1); shine.rotation.z = -0.3; shine.position.set(-W * 0.2, H * 0.12, L0 * 1.4); g.add(noShadow(shine));
  const shine2 = shine.clone(); shine2.material = shine.material; shine2.scale.set(W * (o.shineW ?? 0.05) * 0.45, H * 0.35, 1); shine2.position.set(-W * 0.1, H * 0.14, L0 * 1.42); g.add(shine2);
  let blob = null; if (o.blob) { blob = new THREE.Mesh(new THREE.SphereGeometry(1, 14, 8), new THREE.MeshLambertMaterial({ color: '#9FD8F0', emissive: '#2A5A70', transparent: true, opacity: 0.85 })); blob.position.set((o.blobAt || [0, 0.2])[0] * W / 2, (o.blobAt || [0, 0.2])[1] * H / 2, L0 * 1.1); g.add(noShadow(blob)); }
  const P = n => { const v = o[n]; return v; };
  const partLine = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), mat('#141E14')); partLine.position.z = L0 * 0.08; g.add(partLine);
  g.userData.update = t => {
    const all = typeof o.state === 'number' ? o.state : null;
    const ps = all ?? lin(P('sides'), t, 0), pt = all ?? lin(P('top'), t, 0), pb = all ?? lin(P('back'), t, 0), pp = all ?? lin(P('part'), t, 0), pg = all ?? lin(P('gel'), t, 0);
    cells.forEach((c, idx) => {
      let h = L0 * c.h, ax = c.ax, ay = c.ay, cc = new THREE.Color(c.c), w = wid;
      const vn = (vTop - c.v) / Math.max(0.01, vTop - vBot);                       // 0 at the top, 1 at the bottom
      if (Math.abs(c.lat) > 0.6 && vn <= ps * 1.04 && ps > 0) { h = L0 * 0.1; ax = ay = 0; cc = lerpC(SAND, '#B8B070', hsh(c.k + 21) * 0.5); }
      else if (c.v > vTop - 0.3 && (c.u + 1) / 2 <= pt * 1.02 && pt > 0) { h = L0 * 0.32; ax *= 0.15; ay *= 0.15; cc = lerpC(c.c, '#2F6E2A', 0.4); }
      else if (c.v < -0.3 && (c.u + 1) / 2 <= pb * 1.02 && pb > 0) {
        const f = (c.v - vBot) / (-0.3 - vBot), kk = Math.min(3, Math.floor(f * 4)), fr = f * 4 - kk;
        h = L0 * (0.22 + 0.24 * kk) * (fr > 0.72 ? 1.12 : 1.0); ax = 0; ay = 0; cc = new THREE.Color(fr > 0.72 ? '#8AD06A' : (kk % 2 ? '#2E6A2A' : '#4C9A3E'));
      }
      if (Math.abs(c.u) < 0.04 && vn <= pp * 1.04 && pp > 0) { h = 0.002; cc = new THREE.Color('#1C2E1C'); }
      if (pg > 0) { cc.lerp(new THREE.Color('#69C957'), 0.45 * pg); ax *= 1 - 0.7 * pg; ay = ay * (1 - 0.7 * pg) - 0.25 * pg; }
      const partLean = Math.abs(c.u) < 0.16 && Math.abs(c.u) >= 0.04 && vn <= pp * 1.04 && pp > 0 ? -Math.sign(c.u) * 0.6 : 0;
      dum.position.set(c.x, c.y, 0); dum.rotation.set(PI / 2 + ay, 0, ax + partLean, 'XYZ'); dum.scale.set(w, Math.max(0.001, h), w); dum.updateMatrix();
      im.setMatrixAt(idx, dum.matrix); im.setColorAt(idx, cc);
    });
    im.instanceMatrix.needsUpdate = true; if (im.instanceColor) im.instanceColor.needsUpdate = true;
    if (strip) { const u = t - o.dropAt; strip.visible = u >= 0 && u < 1.6; if (u >= 0) { strip.position.set(0.05 * u, H * 0.4 - 2.6 * u * u, L0 + 0.7 * u); strip.rotation.set(1.6 * u, 0, 0.5 * u); } }
    for (const f of flies) { const u = t - f.te; f.tg.visible = u >= 0 && u < 0.9; if (!f.tg.visible) continue;
      const vv = vTop - (vTop - vBot) * clamp01((f.te - (o.sides[0][0])) / Math.max(0.01, o.sides[o.sides.length - 1][0] - o.sides[0][0])), j = Math.max(0, Math.min(ny - 1, Math.round((vv + 1) / 2 * ny - 0.5)));
      const ex = (f.sd < 0 ? rowL[j] : rowR[j]) * W / 2;
      f.tg.position.set(ex + f.vx * u, vv * H / 2 + f.vy * u - 2.2 * u * u, L0 + f.vz * u); f.tg.rotation.set(f.sp * u * 0.5, f.sp * u, f.sp * u * 0.3); f.tg.scale.setScalar(1 + 0.6 * u); }
    shine.material.opacity = Math.min(0.85, 0.7 * clamp01(pg) * (o.shine ?? 1));
    { const ppv = clamp01(pp); partLine.visible = ppv > 0.01; const len = (vTop - vBot) * H / 2 * ppv; partLine.scale.set(W * (o.partW ?? 0.022), Math.max(0.001, len), L0 * 0.15); partLine.position.y = vTop * H / 2 - len / 2; }
    if (blob) { const b = lin(o.blob, t, 0); blob.visible = b > 0.01; const r = (o.blobR ?? 0.09) * b; blob.scale.set(r * (1 + 0.6 * pg), r * (1 + 0.3 * pg), r * 0.5); }
  };
  g.userData.update(0); g.userData.extent = { vTop, vBot, rowL, rowR, ny };
  return g;
}

export const NUMERO_PROPS = {
  // The war-room board on an easel, tilted back toward the lens (pivot at the floor under the easel; front +Z): a dark wooden frame, a sea-blue
  // backing with pale wave lines and the made-up country in thick green felt hair (feltCore: o.w 1.6, o.h 1.9 and every hair state); the board's
  // middle at o.hc (1.3) high, tilted back by o.tilt (0.2 rad, the top away). The felt's front is 0.05 m in front of the backing.
  feltBoard(o) {
    const W = o.w ?? 1.6, H = o.h ?? 1.9, HC = o.hc ?? 1.3, TL = o.tilt ?? 0.2, g = grp(), board = grp(); g.add(board);
    board.position.set(0, HC, 0); board.rotation.x = -TL;
    const FW = W + 0.34, FH = H + 0.3, wood = '#5A3E26';
    board.add(at(box(FW, FH, 0.04, wood, { outline: 0.006 }), 0, 0, -0.02));
    const sea = canvasPlane(FW - 0.1, FH - 0.1, (c, w, h) => { c.fillStyle = o.sea || '#8CC3D8'; c.fillRect(0, 0, w, h); c.strokeStyle = 'rgba(255,255,255,0.35)'; c.lineWidth = w * 0.006;
      for (let i = 0; i < 26; i++) { const x = (hsh(i) * 0.9 + 0.05) * w, y = (hsh(i + 40) * 0.9 + 0.05) * h; c.beginPath(); c.moveTo(x, y); c.quadraticCurveTo(x + w * 0.03, y - h * 0.012, x + w * 0.06, y); c.stroke(); } }, { res: 512 });
    sea.position.z = 0.002; board.add(sea);
    const felt = feltCore({ ...o, w: W, h: H }); felt.position.z = 0.006; board.add(felt);
    // easel: two front legs, a back leg, a ledge under the board
    const yb = HC - (FH / 2) * Math.cos(TL), zb = (FH / 2) * Math.sin(TL);
    for (const s of [-1, 1]) g.add(rod([s * (FW / 2 - 0.12), 0, 0.25], [s * (FW / 2 - 0.2), HC + FH * 0.45, -0.25], 0.03, wood));
    g.add(rod([0, 0, -0.75], [0, HC + FH * 0.42, -0.3], 0.03, wood));
    g.add(at(box(FW + 0.06, 0.05, 0.14, wood, { outline: 0.005 }), 0, yb - 0.02, zb + 0.04));
    g.userData.update = t => felt.userData.update(t);
    g.userData.update(0); return g;
  },

  // The country seen from space, drawn like the top of a hairdo (pivot at the middle of the country on the ground, lying flat, its top +Z far
  // side... the map's v axis along -Z, so the back (bottom of the map) is toward +Z, the lens side): feltCore with every state done (o.state 1)
  // at o.s (14) times the board's size, bigger tufts, on a blue ocean disc o.sea (r o.seaR 60) and a white gel streak; o.planet: a big blue
  // sphere under it (r o.planetR 400) curving away to the horizon
  hairCountry(o) {
    const S = o.s ?? 14, g = grp(), c = grp(); g.add(c);
    const felt = feltCore({ w: 1.6, h: 1.9, step: o.step ?? 0.04, len: o.len ?? 0.07, partW: 0.03, shineW: 0.035, state: o.state ?? 1, sides: o.sides, top: o.top, back: o.back, part: o.part, gel: o.gel, shine: o.shine ?? 1.2 });
    felt.scale.setScalar(S); felt.rotation.x = -PI / 2; felt.position.y = 0.05; c.add(felt);
    if (o.planet !== false) { const R = o.planetR ?? 400, pl = new THREE.Mesh(new THREE.SphereGeometry(R, 96, 48), mat(o.sea || '#2F7FB8', { noGrain: true })); pl.position.y = -R - 0.4; pl.receiveShadow = true; g.add(pl);
      for (let i = 0; i < (o.clouds ?? 0); i++) { const a = hsh(i + 3) * TAU, d = S * 1.6 + hsh(i + 7) * R * 0.5, th = d / R, cl = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 1), mat('#F4F8FA', { noGrain: true }));
        cl.scale.set(3 + 4 * hsh(i), 0.4, 2 + 3 * hsh(i + 1)); cl.position.set(Math.sin(th) * R * Math.cos(a), Math.cos(th) * R - R - 0.2, Math.sin(th) * R * Math.sin(a)); cl.lookAt(0, -R, 0); cl.rotateX(PI / 2); g.add(noShadow(cl)); }
      const sh = new THREE.Mesh(new THREE.CircleGeometry(S * 1.25, 48), mat('#5AA7D2', { noGrain: true })); sh.rotation.x = -PI / 2; sh.position.y = -0.2; g.add(sh); }
    g.userData.update = t => felt.userData.update(t);
    g.userData.update(0); return g;
  },

  // A big red desk telephone without its handset (pivot at its underside, front +Z): a chunky red body, the cradle forks on top, a white rotary dial
  // with ten holes facing up and forward; o.dial [[t0, t1]]: the dial turns (a finger dials); o.ring [[t0, t1]]: it rattles
  redDeskPhone(o) {
    const S = o.s ?? 1, g = grp(), b = grp(); b.scale.setScalar(S); g.add(b); const R = o.color || '#D8262C', D = '#9E1B20';
    b.add(at(box(0.3, 0.1, 0.26, R, { outline: 0.006, taper: { x: 0.82, z: 0.78 }, pivot: 'bottom' }), 0, 0, 0));
    b.add(at(box(0.24, 0.05, 0.08, D, { outline: 0.004 }), 0, 0.12, -0.04));
    for (const s of [-1, 1]) b.add(at(box(0.04, 0.06, 0.05, R, { outline: 0.004 }), s * 0.1, 0.15, -0.04));
    const dial = grp(); dial.position.set(0, 0.108, 0.06); dial.rotation.x = -1.1; b.add(dial);
    dial.add(at(cyl(0.075, 0.075, 0.012, '#F4F1E8', 18, { outline: 0.004 }), 0, 0, 0, PI / 2, 0, 0));
    const wheel = grp(); dial.add(wheel); for (let i = 0; i < 10; i++) { const a = -0.6 + i * 0.5; wheel.add(at(cyl(0.011, 0.011, 0.016, '#2A2420', 8), Math.cos(a) * 0.052, Math.sin(a) * 0.052, 0.002, PI / 2, 0, 0)); }
    dial.add(at(cyl(0.022, 0.022, 0.016, R, 10), 0, 0, 0.003, PI / 2, 0, 0));
    g.userData.update = t => { wheel.rotation.z = inWin(o.dial, t) ? -2.2 * Math.abs(Math.sin((t - (o.dial.find(w => t >= w[0] && t < w[1])[0])) * 6)) : 0;
      const on = inWin(o.ring, t); b.position.set(on ? 0.006 * Math.sin(t * 90) : 0, on ? 0.008 * Math.abs(Math.sin(t * 70)) : 0, 0); };
    g.userData.update(0); return g;
  },

  // A giant comb (pivot at the middle of its spine; the spine along X, the teeth hanging toward -Y, faces ±Z): o.len (0.6) long, dark brown with a
  // pale outline so it reads on the green felt and on a dark wall
  bigComb(o) {
    const L = o.len ?? 0.6, g = grp(), C = o.color || '#2A1E18';
    g.add(at(box(L, 0.07, 0.025, C, { outline: 0.01 }), 0, 0, 0));
    const n = Math.round(L / 0.03); for (let i = 0; i < n; i++) g.add(at(box(0.014, i < n * 0.45 ? 0.11 : 0.08, 0.02, C, { outline: 0.005, pivot: 'top' }), -L / 2 + (i + 0.5) * L / n, -0.03, 0));
    return g;
  },

  // A giant tube of hair gel (pivot at its middle, the nozzle toward +Y): a light-blue tube o.len (0.45) long, crimped at the bottom, a white cap
  // and nozzle on top, a big drop « GEL » printed on it; o.squeeze [[t, 0..1]]: the tube flattens in the middle and a blob of gel swells out of
  // the nozzle (o.drop 0.07)
  gelTube(o) {
    const L = o.len ?? 0.45, g = grp(), tube = grp(); g.add(tube);
    const body = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.075, L, 14), mat('#7EC8E8', { unique: true })); tube.add(body);
    tube.add(at(box(0.17, 0.035, 0.03, '#5FAED0', { outline: 0.004 }), 0, -L / 2 - 0.01, 0));
    tube.add(at(cyl(0.05, 0.075, 0.05, '#F4F1E8', 12, { outline: 0.004 }), 0, L / 2 + 0.02, 0), at(cyl(0.018, 0.03, 0.06, '#F4F1E8', 10, { outline: 0.003 }), 0, L / 2 + 0.07, 0));
    const lab = canvasPlane(0.12, 0.2, (c, w, h) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, w, h); c.fillStyle = '#2A7FB8'; c.font = `900 ${w * 0.42}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('GEL', w / 2, h * 0.72);
      c.beginPath(); c.moveTo(w / 2, h * 0.12); c.quadraticCurveTo(w * 0.78, h * 0.38, w / 2, h * 0.48); c.quadraticCurveTo(w * 0.22, h * 0.38, w / 2, h * 0.12); c.fill(); }, { res: 128 });
    lab.position.set(0, 0, 0.0765); tube.add(lab);
    const drop = new THREE.Mesh(new THREE.SphereGeometry(1, 12, 8), new THREE.MeshLambertMaterial({ color: '#A8E0F4', emissive: '#2A5A70' })); drop.position.y = L / 2 + 0.1; g.add(drop);
    g.userData.update = t => { const s = clamp01(lin(o.squeeze, t, 0)); body.scale.set(1 + 0.25 * s, 1, 1 - 0.55 * s); lab.position.z = 0.0765 * (1 - 0.55 * s) + 0.002;
      const r = (o.drop ?? 0.07) * s; drop.visible = r > 0.004; drop.scale.set(r, r * 1.2, r); drop.position.y = L / 2 + 0.1 + r; };
    g.userData.update(0); return g;
  },

  // His big messy tuft (attach to the head joint at the top of the head; or o.floor: lying on the floor, pivot at the floor): nine thick tapered
  // locks, dark brown, sticking up and out at odd angles from a tight base, two curling over; o.s (1); o.pat [t, ...]: it squashes and springs back
  heroTuft(o) {
    const S = o.s ?? 1, g = grp(), t = grp(); t.scale.setScalar(S); g.add(t); const C = o.color || '#2B1D16', C2 = '#3E2A1E';
    const locks = [[0, 0.2, 0.0, 0], [-0.5, 0.17, 0.25, 1], [0.55, 0.16, -0.2, 0], [-0.25, 0.22, -0.5, 1], [0.3, 0.2, 0.55, 0], [-0.85, 0.12, -0.1, 1], [0.8, 0.13, 0.3, 0], [0.1, 0.15, 0.9, 1], [-0.1, 0.14, -0.95, 0]];
    locks.forEach(([rz, len, rx, c], i) => { const l = box(0.055, len, 0.05, c ? C2 : C, { taper: 0.25, pivot: 'bottom', outline: 0.004 }); l.rotation.set(rx * 0.6, i * 0.7, rz); l.position.set(Math.sin(rz) * 0.02, 0, Math.sin(rx) * 0.02); t.add(l); });
    for (const s of [-1, 1]) { const q = []; for (let j = 0; j <= 10; j++) { const a = j / 10 * 2.6; q.push(new THREE.Vector3(s * (0.02 + 0.06 * Math.sin(a)), 0.05 + 0.12 * j / 10 + 0.04 * Math.sin(a * 1.3), 0.03 * Math.cos(a))); }
      t.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(q), 16, 0.014, 5), mat(C))); }
    t.add(at(sphere(0.05, C, 1), 0, 0.01, 0));
    if (o.floor) { t.clear(); const base = grp(); t.add(base);
      for (let i = 0; i < 14; i++) { const a = i / 14 * TAU + hsh(i) * 0.4, len = 0.14 + 0.1 * hsh(i + 3), l = box(0.05, len, 0.035, i % 3 ? C : C2, { taper: 0.2, pivot: 'bottom', outline: 0.004 });
        l.rotation.set(PI / 2 - 0.25 - 0.3 * hsh(i + 5), 0, 0); const h = grp(l); h.rotation.y = a; h.position.y = 0.02; base.add(h); }
      for (let i = 0; i < 5; i++) { const q = [], a0 = hsh(i + 9) * TAU; for (let j = 0; j <= 12; j++) { const a = a0 + j / 12 * 3.4; q.push(new THREE.Vector3(Math.cos(a) * (0.03 + 0.07 * j / 12), 0.03 + 0.03 * Math.sin(j), Math.sin(a) * (0.03 + 0.07 * j / 12))); }
        base.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(q), 18, 0.012, 5), mat(i % 2 ? C2 : C))); }
      base.add(at(sphere(0.06, C, 1), 0, 0.03, 0)); }
    if (o.pat) g.userData.update = tt => { const w = wob(o.pat, tt, 0.25, 26, 7); t.scale.set(S * (1 + 0.5 * Math.max(0, w)), S * (1 - Math.max(-0.2, w)), S); };
    g.userData.update?.(0); return g;
  },

  // A plain officer's peaked cap without any badge (attach to the head joint at the top of the head): an olive crown wider at the top, a darker
  // band, a black visor toward +Z; o.w / o.d the head's width and depth (0.24 / 0.18); o.color
  plainCap(o) {
    const W = o.w ?? 0.24, D = o.d ?? 0.18, C = o.color || '#55603A', g = grp();
    g.add(at(box(W * 1.02, 0.05, D * 1.02, o.band || '#3A4226', { outline: 0.004 }), 0, 0.025, 0));
    g.add(at(box(W * 1.18, 0.06, D * 1.25, C, { outline: 0.005, taper: { x: 1.08, z: 1.08 } }), 0, 0.08, -0.01));
    g.add(at(box(W * 0.9, 0.012, 0.09, '#1A1A1C', { outline: 0.003 }), 0, 0.012, D / 2 + 0.04, 0.25, 0, 0));
    return g;
  },

  // Blank shoulder boards (attach to the torso joint at shoulder height): two plain khaki boards, no mark of any kind; o.w (0.5) apart
  blankEpaulettes(o) {
    const W = o.w ?? 0.5, g = grp(); for (const s of [-1, 1]) g.add(at(box(0.13, 0.025, 0.09, o.color || '#6E7A48', { outline: 0.004 }), s * W / 2, 0, 0));
    return g;
  },

  // A border barrier carried upright by soldiers (pivot at the floor under its middle; the boom along X): a striped boom o.len (3.4) long in red and
  // white bands (many short bands: no flag) at o.y (1.15) high on two white posts with feet lifted o.lift (0.05) off the ground; o.sway (rad): a
  // little rocking as they walk
  fieldBarrier(o) {
    const L = o.len ?? 3.4, Y = o.y ?? 1.15, g = grp(), in_ = grp(); g.add(in_);
    const n = Math.round(L / 0.22); for (let i = 0; i < n; i++) in_.add(at(box(L / n, 0.1, 0.1, i % 2 ? '#F4F1E8' : '#D8262C', { outline: 0.004 }), -L / 2 + (i + 0.5) * L / n, Y, 0));
    for (const s of [-1, 1]) { in_.add(at(box(0.1, Y + 0.06, 0.1, '#F4F1E8', { outline: 0.004, pivot: 'bottom' }), s * (L / 2 - 0.15), o.lift ?? 0.05, 0)); in_.add(at(box(0.3, 0.06, 0.3, '#7A7E84', { outline: 0.004 }), s * (L / 2 - 0.15), (o.lift ?? 0.05) + 0.03, 0)); }
    g.userData.update = t => { in_.rotation.z = (o.sway ?? 0.03) * Math.sin(t * 9); in_.position.y = 0.03 * Math.abs(Math.sin(t * 9)); };
    g.userData.update(0); return g;
  },

  // A little sentry box carried on two poles (pivot at the floor under its middle, front +Z): a plain pale grey hut 0.9 x 0.9 x 2.0 with a dark
  // doorway, a small window either side, a sloping roof, no mark, no sign; o.lift (0.2): its floor that high; two long carrying poles along Z
  sentryBox(o) {
    const g = grp(), in_ = grp(), Y = o.lift ?? 0.2; g.add(in_); const C = o.color || '#D9D6CC', T = '#7A7E84';
    in_.add(at(box(0.9, 1.9, 0.9, C, { outline: 0.006, pivot: 'bottom' }), 0, Y, 0));
    in_.add(at(box(0.5, 1.4, 0.02, '#3A3E44'), 0, Y + 0.15 + 0.7, 0.452));
    for (const s of [-1, 1]) in_.add(at(box(0.02, 0.35, 0.35, '#9FC6D8', { outline: 0.003 }), s * 0.452, Y + 1.35, 0));
    in_.add(at(box(1.1, 0.12, 1.1, T, { outline: 0.006 }), 0, Y + 1.96, 0), at(box(0.8, 0.12, 0.8, T, { outline: 0.006 }), 0, Y + 2.08, 0));
    for (const s of [-1, 1]) in_.add(at(box(0.07, 0.07, 2.6, '#8A6A44', { outline: 0.004 }), s * 0.52, Y + 0.25, 0));
    g.userData.update = t => { in_.rotation.x = (o.sway ?? 0.03) * Math.sin(t * 9 + 1); in_.position.y = 0.025 * Math.abs(Math.sin(t * 9 + 1)); };
    g.userData.update(0); return g;
  },

  // A village square (pivot at its middle on the ground; the houses along the back at z -o.back (7) and down both sides): a gravel square
  // o.w (16) x o.d (12) a few centimetres up, old stone houses with tiled roofs and painted shutters, two plane trees, a bench, a small fountain
  // at the back; nothing written anywhere
  villageSquare(o) {
    const W = o.w ?? 16, D = o.d ?? 12, BK = o.back ?? 7, g = grp(), r = rng(o.seed || 94);
    const gr = new THREE.Mesh(new THREE.PlaneGeometry(W, D), mat('#D9C9A3', { unique: true })); gr.renderOrder = -1; gr.rotation.x = -PI / 2; gr.position.y = 0.07; gr.receiveShadow = true; gr.material.polygonOffset = true; gr.material.polygonOffsetFactor = -2; g.add(gr);
    const stones = ['#E6D7B8', '#EBDDC4', '#D9C7A2', '#E9D2B0', '#DCCFB8'], shut = ['#5E8C9A', '#7A9A5A', '#B5523A', '#4E6E9A', '#8A6A9A'];
    const house = (x, z, ry, w, h, i) => { const hg = grp(); hg.position.set(x, 0, z); hg.rotation.y = ry; g.add(hg);
      hg.add(at(box(w, h, 4, stones[i % 5], { outline: 0.01, pivot: 'bottom' }), 0, 0, -2));
      for (const sd of [-1, 1]) hg.add(at(box(w + 0.4, 0.12, 2.5, '#B85C3A', { outline: 0.008 }), 0, h + 0.55, -2 + sd * 1.05, sd * 0.45, 0, 0));
      const nw = Math.max(1, Math.round(w / 1.6));
      for (let f = 0; f < (h > 5 ? 2 : 1); f++) for (let k = 0; k < nw; k++) { const wx = -w / 2 + (k + 0.5) * w / nw, wy = 1.6 + f * 2.6; hg.add(at(box(0.7, 1.05, 0.05, '#3A4450'), wx, wy, 0.02), at(box(0.32, 1.05, 0.06, shut[i % 5], { outline: 0.004 }), wx - 0.52, wy, 0.03), at(box(0.32, 1.05, 0.06, shut[i % 5], { outline: 0.004 }), wx + 0.52, wy, 0.03)); }
      if (i % 2 === 0) hg.add(at(box(1.0, 2.0, 0.06, '#6A4A2E', { outline: 0.005, pivot: 'bottom' }), w * 0.3 - 0.5, 0, 0.03)); };
    let x = -W / 2 - 1; [5.2, 4.2, 6.0, 4.6, 5.4].forEach((w, i) => { house(x + w / 2, -BK, 0, w, i % 2 ? 6.2 : 4.8, i); x += w + 0.1; });
    house(-W / 2 - 1.5, -BK + 6, PI / 2, 6, 5.4, 6); house(W / 2 + 1.5, -BK + 6, -PI / 2, 6, 6.0, 7);
    const tree = (tx, tz) => { g.add(at(cyl(0.18, 0.24, 2.6, '#9A8A70', 7, { pivot: 'bottom', outline: 0.006 }), tx, 0, tz)); for (let k = 0; k < 4; k++) g.add(at(sphere(1.2 + 0.3 * r(), k % 2 ? '#6FA04A' : '#5E9040', 1, { outline: 0.01 }), tx + (r() - 0.5) * 1.4, 3.2 + r() * 0.8, tz + (r() - 0.5) * 1.4)); };
    (o.trees || [[-5.5, -4.5], [5.8, -4.0]]).forEach(([a, b]) => tree(a, b));
    g.add(at(cyl(0.9, 1.0, 0.5, '#CFC3A8', 12, { pivot: 'bottom', outline: 0.008 }), o.fountainX ?? 2.5, 0.05, -BK + 1.6), at(cyl(0.12, 0.15, 1.1, '#CFC3A8', 8, { pivot: 'bottom' }), o.fountainX ?? 2.5, 0.05, -BK + 1.6), at(cyl(0.82, 0.82, 0.04, '#8CC3D8', 12), o.fountainX ?? 2.5, 0.53, -BK + 1.6));
    const bench = grp(at(box(1.6, 0.06, 0.4, '#7A5A3A', { outline: 0.004 }), 0, 0.45, 0), at(box(1.6, 0.4, 0.05, '#7A5A3A', { outline: 0.004 }), 0, 0.7, -0.2), at(box(0.06, 0.45, 0.4, '#3A3A3E', { pivot: 'bottom' }), -0.7, 0, 0), at(box(0.06, 0.45, 0.4, '#3A3A3E', { pivot: 'bottom' }), 0.7, 0, 0));
    bench.position.set(o.benchX ?? -2.8, 0.05, -BK + 1.2); g.add(bench);
    return g;
  },

  // A round green hill carved into o.n (4) terraced steps (pivot at its foot's middle): from o.carve (0..1 or keys) the smooth dome of radius o.r
  // (5.5), height o.h (3.4) becomes four flat green treads with brown earth risers (the profile morphs); o.dirt keys: little puffs on the risers
  terraceHill(o) {
    const R = o.r ?? 5.5, H = o.h ?? 3.4, N = o.n ?? 4, g = grp(), SEG = 16 * N;
    const dome = [], step = [], kind = [];
    for (let i = 0; i <= SEG; i++) { const u = i / SEG; const rr = R * (1 - u), dh = H * Math.sqrt(Math.max(0, 1 - Math.pow(rr / R, 2.2))); dome.push([rr, dh]);
      const k = Math.min(N - 1, Math.floor(u * N)), f = u * N - k; const r0 = R * (1 - k / N) * 0.98 + 0.02 * R, r1 = R * (1 - (k + 1) / N);
      const y0 = H * k / N, y1 = H * (k + 1) / N; let px, py, kd;
      if (f < 0.25) { px = r0 - (r0 - r1) * 0.12 * (f / 0.25); py = y0 + (y1 - y0) * (f / 0.25); kd = 1; } else { px = r0 - (r0 - r1) * (0.12 + 0.88 * (f - 0.25) / 0.75); py = y1; kd = 0; }
      if (k === N - 1 && f >= 0.25) { px = Math.max(0, r0 - (r0 - 0) * (0.12 + 0.88 * (f - 0.25) / 0.75)); }
      step.push([px, py]); kind.push(kd); }
    step[SEG] = [0, H]; dome[SEG] = [0, H];
    const LS = 40, geo = new THREE.LatheGeometry(dome.map(([x, y]) => new THREE.Vector2(x, y)), LS).toNonIndexed();
    const posA = geo.attributes.position, nV = posA.count, base = new Float32Array(posA.array), cols = new Float32Array(nV * 3);
    // which profile point each vertex came from: recover by matching radius/height to the dome profile index
    const idx = new Int16Array(nV); for (let v = 0; v < nV; v++) { const x = base[v * 3], y = base[v * 3 + 1], z = base[v * 3 + 2], rr = Math.hypot(x, z); let best = 0, bd = 1e9; for (let i = 0; i <= SEG; i++) { const d = Math.abs(dome[i][0] - rr) + Math.abs(dome[i][1] - y); if (d < bd) { bd = d; best = i; } } idx[v] = best; }
    geo.setAttribute('color', new THREE.BufferAttribute(cols, 3));
    const m = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ vertexColors: true, flatShading: true })); m.castShadow = m.receiveShadow = true; g.add(m);
    const cG = new THREE.Color('#6DB04E'), cG2 = new THREE.Color('#5E9E42'), cE = new THREE.Color('#9A6A3E');
    g.userData.update = t => { const p = smooth(lin(o.carve, t, 1));
      const pc = o.cut != null ? smooth(lin(o.cut, t, 1)) : p;
      for (let v = 0; v < nV; v++) { const i = idx[v], x = base[v * 3], z = base[v * 3 + 2], rr = Math.hypot(x, z) || 1e-6, a = Math.atan2(z, x);
        const pv = i < SEG / N ? pc : p, ramp = [dome[i][0], i < SEG / N ? (H / N) * (i / (SEG / N)) : dome[i][1]];
        const src = o.cut != null && i < SEG / N ? ramp : dome[i];
        const R1 = src[0] + (step[i][0] - src[0]) * pv, Y1 = src[1] + (step[i][1] - src[1]) * pv;
        posA.array[v * 3] = Math.cos(a) * R1; posA.array[v * 3 + 1] = Y1 + 0.05; posA.array[v * 3 + 2] = Math.sin(a) * R1;
        const pk = i < SEG / N && o.cut != null ? pc : p; const c = kind[i] && pk > 0.2 ? cE.clone().lerp(cG, 1 - pk) : (Math.floor(i / 16) % 2 ? cG : cG2); cols[v * 3] = c.r; cols[v * 3 + 1] = c.g; cols[v * 3 + 2] = c.b; }
      posA.needsUpdate = true; geo.attributes.color.needsUpdate = true; geo.computeVertexNormals(); geo.computeBoundingSphere(); };
    g.userData.update(0); return g;
  },

  // An army excavator (pivot at the ground under its tracks' middle, the arm toward +Z): olive tracks and body, a cab with a pale window, a
  // boom, a stick and a bucket with teeth; o.dig [[t, 0..1]]: the arm's pose (0 raised, 1 bucket down and curled in); o.swing [[t, rad]]: the
  // upper body turns; o.s (1)
  excavator(o) {
    const S = o.s ?? 1, g = grp(), b = grp(); b.scale.setScalar(S); g.add(b); const OL = '#6B7A3E', DK = '#3E4626';
    for (const s of [-1, 1]) b.add(at(box(0.55, 0.55, 3.0, '#2E3226', { outline: 0.01, pivot: 'bottom' }), s * 0.95, 0, 0));
    const up = grp(); up.position.y = 0.6; b.add(up);
    up.add(at(box(2.1, 0.8, 2.4, OL, { outline: 0.01, pivot: 'bottom' }), 0, 0, -0.2), at(box(0.95, 1.05, 1.0, OL, { outline: 0.01, pivot: 'bottom' }), -0.55, 0.8, 0.45), at(box(0.8, 0.6, 0.02, '#BFDCE8'), -0.55, 1.4, 0.96));
    const boom = grp(); boom.position.set(0.45, 1.0, 0.8); up.add(boom); boom.add(at(box(0.42, 0.5, 3.0, '#8A9A4E', { outline: 0.012 }), 0, 0, 1.5), at(box(0.12, 0.12, 2.2, '#C9CED6', { outline: 0.004 }), 0, -0.32, 1.2));
    const stick = grp(); stick.position.set(0, 0, 3.0); boom.add(stick); stick.add(at(box(0.34, 0.4, 2.2, '#7A8A44', { outline: 0.012 }), 0, 0, 1.1));
    const bucket = grp(); bucket.position.set(0, 0, 2.2); stick.add(bucket); bucket.add(at(box(0.95, 0.7, 0.6, DK, { outline: 0.012 }), 0, -0.3, 0.2));
    for (let i = 0; i < 5; i++) bucket.add(at(box(0.1, 0.2, 0.1, '#D0D4D8', { taper: 0.3, pivot: 'top' }), -0.36 + i * 0.18, -0.62, 0.45));
    const dirt = at(sphere(0.42, '#8A5E36', 1), 0, -0.2, 0.25); dirt.scale.set(1, 0.6, 0.8); bucket.add(dirt);
    g.userData.update = t => { const d = clamp01(lin(o.dig, t, 0)); boom.rotation.x = -0.55 + 0.95 * d; stick.rotation.x = 0.9 + 0.5 * d; bucket.rotation.x = 0.4 + 1.1 * d; dirt.visible = d > 0.6; up.rotation.y = lin(o.swing, t, 0);
      const sh = inWin(o.shake, t); b.position.set(sh ? 0.015 * Math.sin(t * 60) : 0, 0, 0); };
    g.userData.update(0); return g;
  },

  // The country seen from just above (pivot at the middle on the ground; the stripe along Z from z -o.d/2 to +o.d/2): fields in patches and a
  // dark forest of instanced cones o.w (40) x o.d (70); a bare bright earth stripe o.sw (3.2) wide grows from the +Z coast toward -Z behind the
  // lead tank: o.lead [[t, z]] (z of the lead tank's tail, decreasing); trees on the stripe disappear behind it; the sea at both ends (o.coast: the country's edge at
  // z = ±o.d/2)
  forestStripe(o) {
    const W = o.w ?? 40, D = o.d ?? 70, SW = o.sw ?? 3.2, g = grp(), r = rng(o.seed || 31);
    const sea = new THREE.Mesh(new THREE.PlaneGeometry(W * 3, D * 3), mat('#3D8DC0', { noGrain: true })); sea.rotation.x = -PI / 2; sea.position.y = 0.0; g.add(sea);
    const land = new THREE.Mesh(new THREE.PlaneGeometry(W * 1.6, D), mat('#4F7E36')); land.rotation.x = -PI / 2; land.position.y = 0.05; land.receiveShadow = true; g.add(land);
    const beach = (z, s) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(W * 1.6, 1.4), mat('#E2D2A0')); m.rotation.x = -PI / 2; m.position.set(0, 0.06, z + s * 0.7); g.add(m); };
    beach(-D / 2, 1); beach(D / 2, -1);
    const fc = ['#C9B456', '#9DBE5A', '#D8C27A', '#7FAE4E'];
    for (let i = 0; i < 18; i++) { const fw = 6 + r() * 8, fd = 5 + r() * 8, fx = (r() - 0.5) * W * 1.3, fz = (r() - 0.5) * (D - 12); if (Math.abs(fx) < SW / 2 + fw / 2 + 0.6) continue; const m = new THREE.Mesh(new THREE.PlaneGeometry(fw, fd), mat(fc[i % 4])); m.rotation.x = -PI / 2; m.position.set(fx, 0.08 + i * 0.002, fz); m.receiveShadow = true; g.add(m); }
    const stripe = new THREE.Mesh(new THREE.PlaneGeometry(SW, 1), mat('#E8C890', { unique: true })); stripe.rotation.x = -PI / 2; stripe.position.y = 0.12; stripe.receiveShadow = true; g.add(stripe);
    const trees = []; const tg = new THREE.ConeGeometry(0.9, 2.6, 6); tg.translate(0, 1.3, 0);
    for (let i = 0; i < (o.n ?? 1400); i++) { const x = (r() - 0.5) * W * 1.5, z = -D / 2 + 2 + r() * (D - 4); if (Math.abs(x) > SW / 2 + 0.8 && r() < 0.45) continue; trees.push([x, z, 0.7 + r() * 0.6, r()]); }
    const tm = new THREE.InstancedMesh(tg, new THREE.MeshLambertMaterial({ color: '#FFFFFF', flatShading: false }), trees.length); tm.castShadow = true; g.add(tm);
    const dm = new THREE.Object3D(), cc = new THREE.Color(), tcs = ['#1E4A26', '#244F2A', '#18401F', '#2A5A30'];
    trees.forEach((tr, i) => tm.setColorAt(i, cc.set(tcs[Math.floor(tr[3] * 4)])));
    g.userData.update = t => { const z0 = D / 2 - 0.5, z1 = Math.min(z0 - 0.01, Math.max(-D / 2 + 0.5, lin(o.lead, t, z0))); stripe.scale.y = z0 - z1; stripe.position.z = (z0 + z1) / 2; stripe.visible = z0 - z1 > 0.05;
      trees.forEach(([x, z, s], i) => { const gone = Math.abs(x) < SW / 2 + 0.3 && z > z1 - 1.2; dm.position.set(x, 0.05, z); dm.scale.setScalar(gone ? 0.0001 : s); dm.updateMatrix(); tm.setMatrixAt(i, dm.matrix); });
      tm.instanceMatrix.needsUpdate = true; if (tm.instanceColor) tm.instanceColor.needsUpdate = true; };
    g.userData.update(0); return g;
  },

  // A factory gate (pivot at the middle of the gateway on the ground, front +Z): a brick wall o.w (14) long, 3 m high, an open gateway with two
  // pale piers and an arch sign « USINE », a long factory hall behind with saw-tooth roofs and two chimneys with slow white smoke
  factoryGate(o) {
    const W = o.w ?? 14, g = grp(), BR = '#B8664A';
    for (const s of [-1, 1]) { g.add(at(box(W / 2 - 2, 2.6, 0.4, BR, { outline: 0.01, pivot: 'bottom' }), s * (W / 4 + 1), 0, 0)); g.add(at(box(W / 2 - 2, 0.15, 0.5, '#D9CFC0', { outline: 0.006 }), s * (W / 4 + 1), 2.65, 0));
      g.add(at(box(0.7, 3.6, 0.7, '#D9CFC0', { outline: 0.01, pivot: 'bottom' }), s * 2.1, 0, 0)); }
    const sign = canvasPlane(4.6, 0.8, (c, w, h) => { c.fillStyle = '#2E3A46'; c.fillRect(0, 0, w, h); c.fillStyle = '#F4F1E8'; c.font = `900 ${h * 0.62}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.text || 'USINE', w / 2, h * 0.55); }, { res: 512 });
    sign.position.set(0, 4.0, 0.36); g.add(sign, at(box(4.8, 0.95, 0.12, '#1E262E', { outline: 0.006 }), 0, 4.0, 0.28));
    const hall = grp(); hall.position.set(0, 0, -9); g.add(hall); hall.add(at(box(W + 6, 5.5, 10, '#C9BBA6', { outline: 0.01, pivot: 'bottom' }), 0, 0, 0));
    for (let i = 0; i < 7; i++) { const tooth = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 1.6, W + 6, 3), mat('#8A9AA6')); tooth.rotation.z = PI / 2; tooth.position.set(0, 6.2, -4.3 + i * 1.45); tooth.scale.set(1, 1, 0.5); hall.add(tooth); }
    for (let k = 0; k < 8; k++) hall.add(at(box(1.2, 1.4, 0.05, '#4A5A6A'), -W / 2 + 1 + k * 2.3, 3.0, 5.03));
    const puffs = [];
    for (const cx of [-4.5, 3.8]) { hall.add(at(cyl(0.55, 0.7, 11, '#A85A44', 10, { pivot: 'bottom', outline: 0.01 }), cx, 0, -2)); hall.add(at(cyl(0.6, 0.6, 0.4, '#E8E2D6', 10), cx, 10.5, -2));
      for (let i = 0; i < 6; i++) { const p = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 1), mat('#F4F1EC', { opacity: 0.9, unique: true })); hall.add(noShadow(p)); puffs.push([p, cx, i]); } }
    g.userData.update = t => { for (const [p, cx, i] of puffs) { const u = ((t * 0.25 + i / 6) % 1); p.position.set(cx + u * 3, 11.5 + u * 5, -2 - u * 1.5); p.scale.setScalar(0.6 + u * 1.6); p.material.opacity = 0.9 * (1 - u); } };
    g.userData.update(0); return g;
  },

  // A block of ice with a pay envelope frozen inside (pivot at its middle; the big face toward +Z): an opaque pale blue block o.w (0.55) x o.h
  // (0.4) x 0.18 with lighter bevel edges; on its front, under the frost, a bright yellow envelope with its flap (no sign, no logo, nothing
  // written), frost streaks and a white glint in a corner
  iceBlock(o) {
    const W = o.w ?? 0.55, H = o.h ?? 0.4, Dd = o.d ?? 0.26, g = grp();
    g.add(at(box(W, H, Dd, '#86D8F0', { outline: 0.006 }), 0, 0, 0));
    const face = canvasPlane(W * 0.96, H * 0.94, (c, w, h) => { const gr = c.createLinearGradient(0, 0, w, h); gr.addColorStop(0, '#C8F2FF'); gr.addColorStop(1, '#6CCDEB'); c.fillStyle = gr; c.fillRect(0, 0, w, h);
      c.fillStyle = o.env || '#F8C828'; const ex = w * 0.2, ey = h * 0.25, ew = w * 0.6, eh = h * 0.5; c.fillRect(ex, ey, ew, eh); c.strokeStyle = '#C8961A'; c.lineWidth = w * 0.014; c.strokeRect(ex, ey, ew, eh);
      c.beginPath(); c.moveTo(ex, ey); c.lineTo(ex + ew / 2, ey + eh * 0.55); c.lineTo(ex + ew, ey); c.stroke();
      c.fillStyle = 'rgba(170,230,250,0.38)'; c.fillRect(0, 0, w, h);
      c.strokeStyle = 'rgba(255,255,255,0.9)'; c.lineWidth = w * 0.012; for (let i = 0; i < 9; i++) { const x = hsh(i + (o.seed || 0)) * w, y = hsh(i + 9 + (o.seed || 0)) * h; c.beginPath(); c.moveTo(x, y); c.lineTo(x + w * 0.1, y + h * 0.05); c.lineTo(x + w * 0.14, y - h * 0.03); c.stroke(); }
      c.fillStyle = 'rgba(255,255,255,0.85)'; c.fillRect(0, 0, w, h * 0.05); c.fillRect(0, 0, w * 0.04, h);
      c.fillStyle = '#FFFFFF'; c.beginPath(); c.arc(w * 0.86, h * 0.17, w * 0.035, 0, TAU); c.fill(); }, { res: 256, emissive: 0.3 });
    face.position.z = Dd / 2 + 0.002; g.add(face);
    const hi = '#F4FDFF';
    g.add(at(box(W + 0.01, 0.018, 0.018, hi), 0, H / 2, Dd / 2), at(box(0.018, H + 0.01, 0.018, hi), -W / 2, 0, Dd / 2), at(box(W + 0.01, 0.018, Dd, hi), 0, H / 2, 0));
    for (let i = 0; i < 4; i++) g.add(at(box(0.025, 0.05 + 0.04 * hsh(i + 3), 0.025, '#BFEFFF', { taper: 0.2, pivot: 'top' }), -W / 2 + 0.08 + i * (W - 0.16) / 3, -H / 2, Dd / 2 - 0.03));
    const puffs = []; for (let i = 0; i < 4; i++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 1), mat('#F4FBFF', { opacity: 0.6, unique: true })); g.add(noShadow(m)); puffs.push(m); }
    g.userData.update = t => { puffs.forEach((m, i) => { const u = ((t * 0.5 + i / 4 + (o.seed || 0) * 0.13) % 1); m.position.set((i - 1.5) * W * 0.22, H / 2 + 0.03 + u * 0.3, Dd * 0.2); m.scale.setScalar(0.03 + u * 0.07); m.material.opacity = 0.6 * (1 - u); }); };
    g.userData.update(0); return g;
  },

  // Two plain fighter jets (no roundel, no lettering) flying noses up on either side of a giant oval hand mirror they hold by its rim (pivot at
  // the mirror's middle, its glass toward +Z): the mirror o.mw (10) x o.mh (13) in a silver frame with a long handle hanging down, the glass a
  // painted reflection of the back of the hairdo (sandy buzzed sides, four stepped green ridges, a dark parting line at the top, a white gel
  // shine) on a pale blue-grey ground; the jets at o.js (0.55) of their size, their wing tips clamped on the rim; o.tilt (rad) the mirror leans
  // back; o.wob: a slow sway; o.burner flames
  mirrorJets(o) {
    const MW = o.mw ?? 10, MH = o.mh ?? 13, g = grp(), m = grp(); g.add(m);
    const ell = new THREE.Shape(); ell.absellipse(0, 0, MW / 2 + 0.5, MH / 2 + 0.5, 0, TAU);
    const frame = new THREE.Mesh(new THREE.ExtrudeGeometry(ell, { depth: 0.5, bevelEnabled: false, curveSegments: 40 }), mat('#C9CED6')); frame.position.z = -0.5; m.add(frame);
    m.add(at(box(1.4, MH * 0.55, 0.5, '#B0B6BE', { outline: 0.02, pivot: 'top' }), 0, -MH / 2 - 0.2, -0.25), at(box(1.8, 0.9, 0.6, '#9AA0A8', { outline: 0.02 }), 0, -MH / 2 - 0.2, -0.25));
    const glassTex = canvasPlane(MW, MH, (c, w, h) => { c.fillStyle = '#C8DCE6'; c.fillRect(0, 0, w, h);
      c.save(); c.beginPath(); c.ellipse(w / 2, h * 0.56, w * 0.4, h * 0.38, 0, 0, TAU); c.clip();
      c.fillStyle = SAND; c.fillRect(0, 0, w, h); c.fillStyle = '#3E8A36'; c.fillRect(w * 0.25, 0, w * 0.5, h);
      const rows = 4; for (let k = 0; k < rows; k++) { const y0 = h * (0.5 + k * 0.11); c.fillStyle = k % 2 ? '#4E9E40' : '#2E6E2A'; c.fillRect(w * 0.25, y0, w * 0.5, h * 0.11); c.fillStyle = '#7CC45E'; c.fillRect(w * 0.25, y0, w * 0.5, h * 0.025); }
      c.fillStyle = '#1C2E1C'; c.fillRect(w * 0.49, 0, w * 0.02, h * 0.5);
      c.restore(); c.strokeStyle = 'rgba(255,255,255,0.55)'; c.lineWidth = w * 0.03; c.beginPath(); c.moveTo(w * 0.2, h * 0.2); c.lineTo(w * 0.32, h * 0.12); c.stroke(); c.beginPath(); c.moveTo(w * 0.72, h * 0.86); c.lineTo(w * 0.82, h * 0.78); c.stroke(); }, { res: 512, emissive: 0.35 });
    const gm = new THREE.Mesh(new THREE.ShapeGeometry((() => { const s = new THREE.Shape(); s.absellipse(0, 0, MW / 2, MH / 2, 0, TAU); return s; })(), 48), glassTex.material);
    const uv = gm.geometry.attributes.uv, p = gm.geometry.attributes.position; for (let i = 0; i < uv.count; i++) uv.setXY(i, p.getX(i) / MW + 0.5, p.getY(i) / MH + 0.5);
    gm.position.z = 0.02; m.add(gm);
    const JS = o.js ?? 0.55, jets = [];
    for (const s of [-1, 1]) { const j = buildProp('plainJet', { burner: o.burner ?? 0.7, glow: 0 });
      j.traverse(q => { const pr = q.geometry && q.geometry.parameters; if (q.isMesh && q.geometry.type === 'PlaneGeometry' && pr && Math.abs(pr.width - 2.6) < 1e-6 && Math.abs(pr.height - 0.45) < 1e-6) q.visible = false; });
      j.scale.setScalar(JS); const jg = grp(j); j.rotation.set(-PI / 2, 0, 0); j.position.set(0, -1.6 * JS, 0);
      jg.position.set(s * (MW / 2 + 0.5 + 5.6 * JS), o.jy ?? 0.0, -1.2); jg.rotation.y = s * 0.25; g.add(jg); jets.push([jg, s]);
      m.add(at(box(5.0 * JS, 0.35, 0.35, '#8A9097', { outline: 0.02 }), s * (MW / 2 + 0.5 + 2.5 * JS), 0, -0.4)); }
    m.rotation.x = -(o.tilt ?? 0.2);
    g.userData.update = t => { const w = (o.wob ?? 0.03) * Math.sin(t * 1.7); g.rotation.z = w; jets.forEach(([jg, s], i) => { jg.position.y = (o.jy ?? 0) + 0.15 * Math.sin(t * 3 + i); jg.children[0].userData.update?.(t); }); };
    g.userData.update(0); return g;
  },

  // A barber shop (pivot at the middle of the floor, the back wall at z -o.back (2.2), the lens side +Z): a black and white tiled floor raised 3 cm,
  // a mint back wall with a wide mirror (a pale blue-grey glass with soft streaks), a shelf of bottles and a brush under it, a red-and-white barber
  // pole and a small framed price board with pictures only; side walls; a wall phone at o.phone [x, y] on the left wall (separate prop)
  barberShop(o) {
    const BK = o.back ?? 2.2, W = o.w ?? 7, g = grp();
    const tiles = canvasPlane(W, 6, (c, w, h) => { const n = 14, m = Math.round(n * 6 / W); for (let i = 0; i < n; i++) for (let j = 0; j < m; j++) { c.fillStyle = (i + j) % 2 ? '#2A2A2E' : '#F2EFE6'; c.fillRect(i * w / n, j * h / m, w / n + 1, h / m + 1); } }, { res: 512 });
    tiles.rotation.x = -PI / 2; tiles.position.set(0, 0.03, -BK + 3); g.add(tiles);
    g.add(at(box(W, 4.2, 0.2, o.wall || '#A8D5C4', { pivot: 'bottom' }), 0, 0, -BK - 0.1), at(box(W, 1.0, 0.04, '#E8E2D6', { pivot: 'bottom' }), 0, 0, -BK + 0.02));
    for (const s of [-1, 1]) g.add(at(box(0.2, 4.2, 6, o.wall || '#A8D5C4', { pivot: 'bottom' }), s * W / 2, 0, -BK + 3), at(box(0.04, 1.0, 6, '#E8E2D6', { pivot: 'bottom' }), s * (W / 2 - 0.12), 0, -BK + 3));
    const mir = canvasPlane(o.mirW ?? 3.0, 1.3, (c, w, h) => { const gr = c.createLinearGradient(0, 0, w, h); gr.addColorStop(0, '#DCE8EE'); gr.addColorStop(1, '#B4C8D2'); c.fillStyle = gr; c.fillRect(0, 0, w, h); c.strokeStyle = 'rgba(255,255,255,0.7)'; c.lineWidth = w * 0.01; for (const x of [0.15, 0.62]) { c.beginPath(); c.moveTo(w * x, h * 0.9); c.lineTo(w * (x + 0.12), h * 0.1); c.stroke(); } }, { res: 256 });
    mir.position.set(o.mirX ?? 0, 1.95, -BK + 0.03); g.add(mir, at(box((o.mirW ?? 3.0) + 0.12, 1.42, 0.04, '#E8E2D6', { outline: 0.004 }), o.mirX ?? 0, 1.95, -BK + 0.01));
    g.add(at(box(2.6, 0.05, 0.25, '#E8E2D6', { outline: 0.004 }), o.mirX ?? 0, 1.18, -BK + 0.13));
    const bc = ['#3A8AC8', '#E8A030', '#7AC85A', '#C84A7A', '#F2F0EA'];
    for (let i = 0; i < 7; i++) g.add(at(cyl(0.045, 0.05, 0.18 + 0.05 * (i % 3), bc[i % 5], 8, { pivot: 'bottom', outline: 0.003 }), (o.mirX ?? 0) - 1.1 + i * 0.36, 1.205, -BK + 0.13));
    const pole = grp(); pole.position.set(o.poleX ?? 2.6, 1.7, -BK + 0.18); g.add(pole);
    pole.add(at(cyl(0.11, 0.11, 0.12, '#C9CED6', 10), 0, 0.56, 0), at(cyl(0.11, 0.11, 0.12, '#C9CED6', 10), 0, -0.56, 0));
    const stripes = canvasPlane(0.7, 1.0, (c, w, h) => { c.fillStyle = '#F4F1E8'; c.fillRect(0, 0, w, h); c.fillStyle = '#D8262C'; for (let i = -6; i < 12; i++) { c.beginPath(); c.moveTo(0, i * h / 6); c.lineTo(w, i * h / 6 - h * 0.35); c.lineTo(w, i * h / 6 - h * 0.35 + h / 14); c.lineTo(0, i * h / 6 + h / 14); c.fill(); } }, { res: 128 });
    const cylm = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 1.0, 16, 1, true), stripes.material); pole.add(cylm);
    if (o.board !== false) { const bd = canvasPlane(0.7, 0.9, (c, w, h) => { c.fillStyle = '#2E3A46'; c.fillRect(0, 0, w, h); c.fillStyle = '#F4F1E8';
        for (let i = 0; i < 3; i++) { const y = h * (0.2 + i * 0.3); c.beginPath(); c.arc(w * 0.3, y, w * 0.11, 0, TAU); c.fill(); c.fillRect(w * 0.5, y - h * 0.02, w * 0.35, h * 0.04); c.fillStyle = '#2E3A46'; c.fillRect(w * 0.19, y - w * 0.11, w * 0.22, w * (0.04 + 0.05 * i)); c.fillStyle = '#F4F1E8'; } }, { res: 256 });
      bd.position.set(o.boardX ?? -2.6, 2.0, -BK + 0.03); g.add(bd, at(box(0.78, 0.98, 0.03, '#8A6A44'), o.boardX ?? -2.6, 2.0, -BK + 0.01)); }
    return g;
  },

  // A barber's chair (pivot at the floor under the seat, the sitter facing +Z; the seat cushion top at 0.56): a chrome pedestal on a round
  // foot, a red leather seat and back, padded arms, a headrest, a foot bar
  barberChair(o) {
    const C = o.color || '#B8262C', CH = '#C9CED6', g = grp();
    g.add(at(cyl(0.32, 0.36, 0.06, CH, 16, { outline: 0.004 }), 0, 0.03, 0), at(cyl(0.08, 0.1, 0.38, CH, 10, { pivot: 'bottom' }), 0, 0.06, 0));
    g.add(at(box(0.62, 0.12, 0.6, C, { outline: 0.008 }), 0, 0.5, 0), at(box(0.6, 0.06, 0.54, '#D8383E'), 0, 0.57, 0.01));
    g.add(at(box(0.62, 0.75, 0.12, C, { outline: 0.008 }), 0, 0.92, -0.3, -0.12, 0, 0), at(box(0.3, 0.16, 0.1, '#2A2A2E', { outline: 0.004 }), 0, 1.38, -0.36, -0.12, 0, 0), at(box(0.04, 0.2, 0.04, CH), 0, 1.25, -0.35));
    for (const s of [-1, 1]) g.add(at(box(0.1, 0.08, 0.5, C, { outline: 0.006 }), s * 0.34, 0.76, 0.02), at(box(0.04, 0.2, 0.04, CH), s * 0.34, 0.64, 0.2), at(box(0.04, 0.2, 0.04, CH), s * 0.34, 0.64, -0.2));
    g.add(at(box(0.5, 0.04, 0.16, CH, { outline: 0.004 }), 0, 0.22, 0.42), at(box(0.04, 0.3, 0.04, CH), 0, 0.36, 0.33, 0.6, 0, 0));
    g.userData.seat = [0, 0.57, 0]; return g;
  },

  // A barber's cape over a seated man (attach to the torso joint at the collar, offset about [0, 0.42, 0.04]): a wide pale blue-and-white striped
  // cloth falling from a neck band to below the knees, spread over the arms of the chair; o.len (1.0), o.w (0.95), o.fwd (0.45: how far it
  // reaches forward over the lap)
  barberCape(o) {
    const L = o.len ?? 0.72, Wd = o.w ?? 0.78, F = o.fwd ?? 0.55, g = grp();
    const cloth = canvasPlane(1, 1, (c, w, h) => { c.fillStyle = '#F4F7F8'; c.fillRect(0, 0, w, h); c.fillStyle = '#8CC0DC'; for (let i = 0; i < 8; i++) c.fillRect(i * w / 8, 0, w / 16, h); }, { res: 128 });
    const geo = new THREE.CylinderGeometry(0.16, Wd / 2, L, 18, 4, true); geo.translate(0, -L / 2, 0);
    const pa = geo.attributes.position; for (let i = 0; i < pa.count; i++) { const y = -pa.getY(i) / L, z = pa.getZ(i); pa.setZ(i, z * (0.55 + 0.2 * y) + (z > 0 ? F * y * y : 0) + 0.04); pa.setX(i, pa.getX(i) * (1 + 0.08 * Math.sin(Math.atan2(z, pa.getX(i)) * 7) * y)); }
    geo.computeVertexNormals();
    const cm = cloth.material.clone(); cm.side = THREE.DoubleSide; const cape = new THREE.Mesh(geo, cm); cape.castShadow = true; g.add(cape);
    g.add(at(cyl(0.17, 0.17, 0.05, '#F4F7F8', 14, { outline: 0.004 }), 0, -0.01, 0.02));
    return g;
  },

  // A wall telephone (pivot on the wall at its middle, front +Z): a cream box with a dial and the cradle hook; the handset is a separate prop
  wallPhone(o) {
    const g = grp(), C = o.color || '#EDE6D2';
    g.add(at(box(0.2, 0.3, 0.08, C, { outline: 0.005 }), 0, 0, 0.04), at(cyl(0.06, 0.06, 0.012, '#F8F6F0', 14, { outline: 0.003 }), 0, -0.04, 0.085, PI / 2, 0, 0));
    for (let i = 0; i < 8; i++) { const a = i * 0.7; g.add(at(cyl(0.008, 0.008, 0.014, '#2A2420', 6), Math.cos(a) * 0.04, -0.04 + Math.sin(a) * 0.04, 0.09, PI / 2, 0, 0)); }
    g.add(at(box(0.04, 0.05, 0.06, '#8A8070'), 0.12, 0.08, 0.06));
    return g;
  },
  // A barber's clipper with a clear silhouette (pivot at the middle of its body, the blade toward +Y, the switch toward +Z): a long narrow
  // dark body o.len (0.26) tapering to the head, a chrome band, a wide black toothed blade head on top (two rows of teeth), a red switch, a
  // short straight cord out of the bottom; o.buzz [[t0, t1]]: it vibrates and short white buzz lines flicker either side of the head; o.s
  barberClippers(o) {
    const S = o.s ?? 1, L = o.len ?? 0.26, g = grp(), b = grp(); b.scale.setScalar(S); g.add(b);
    b.add(at(box(0.055, L, 0.042, o.color || '#2C3038', { outline: 0.006, taper: { x: 1.25, z: 1.1 } }), 0, 0, 0));
    b.add(at(box(0.07, 0.025, 0.048, '#C9CED6', { outline: 0.004 }), 0, L * 0.36, 0));
    b.add(at(box(0.085, 0.03, 0.03, '#141518', { outline: 0.005 }), 0, L / 2 + 0.012, 0));
    for (let i = 0; i < 11; i++) { b.add(at(box(0.005, 0.03, 0.012, '#0E0F12'), -0.04 + i * 0.008, L / 2 + 0.04, 0.008)); b.add(at(box(0.005, 0.022, 0.01, '#E8ECF0'), -0.04 + i * 0.008, L / 2 + 0.036, -0.008)); }
    b.add(at(box(0.018, 0.035, 0.012, '#D23A2E', { outline: 0.003 }), 0, L * 0.12, 0.024));
    b.add(at(cyl(0.006, 0.006, 0.12, '#1E2026', 5), 0, -L / 2 - 0.06, 0));
    const lines = []; for (const sd of [-1, 1]) for (let j = 0; j < 3; j++) { const m = new THREE.Mesh(new THREE.BoxGeometry(0.004, 0.035, 0.004), new THREE.MeshBasicMaterial({ color: '#FFFFFF' })); m.position.set(sd * (0.065 + j * 0.018), L / 2 + 0.02 + (j - 1) * 0.025, 0); m.rotation.z = sd * (0.6 - j * 0.3); b.add(m); lines.push([m, j]); }
    g.userData.update = t => { const on = inWin(o.buzz, t); b.position.set(on ? 0.003 * Math.sin(t * 260) : 0, on ? 0.002 * Math.sin(t * 310) : 0, 0); b.rotation.z = on ? 0.03 * Math.sin(t * 190) : 0;
      lines.forEach(([m, j]) => { m.visible = on && (Math.floor(t * 30) + j) % 2 === 0; }); };
    g.userData.update(0); return g;
  },

  // A bald cap in skin colour over a box head (attach to the head joint, offset [0, 0, 0]: the head's base): it covers the top, the sides and the
  // back down to o.down (0.22) below the top, a thin band across the top of the forehead; o.w / o.h / o.d the head box (0.24 / 0.5 / 0.17);
  // o.skin; o.shine: a soft white highlight on the top
  baldCap(o) {
    const W = o.w ?? 0.24, H = o.h ?? 0.5, D = o.d ?? 0.17, DN = o.down ?? 0.22, C = o.skin || '#E2B48E', e = 0.006, g = grp();
    g.add(at(box(W + 2 * e, e * 2, D + 2 * e, C), 0, H + e, 0));
    for (const s of [-1, 1]) g.add(at(box(e, DN, D + e, C), s * (W / 2 + e / 2), H - DN / 2, -e / 2));
    g.add(at(box(W + 2 * e, DN, e, C), 0, H - DN / 2, -D / 2 - e / 2));
    g.add(at(box(W + 2 * e, o.band ?? 0.035, e, C), 0, H - (o.band ?? 0.035) / 2, D / 2 + e / 2));
    if (o.shine !== false) { const hl = new THREE.Mesh(new THREE.PlaneGeometry(W * 0.6, D * 0.35), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.7, depthWrite: false })); hl.rotation.x = -PI / 2; hl.position.set(-W * 0.1, H + 2.2 * e, D * 0.1); g.add(noShadow(hl)); }
    return g;
  },

  // A sun lounger carried overhead (pivot at its middle underside; its length along Z, the head end toward -Z): a flat white frame o.len (1.8)
  // x 0.62 with a plain o.color (teal) cushion and a raised head rest, short legs
  sunLounger(o) {
    const L = o.len ?? 1.8, g = grp(), C = o.color || '#2EA8A0';
    g.add(at(box(0.64, 0.05, L, '#F4F1E8', { outline: 0.006 }), 0, 0.025, 0), at(box(0.58, 0.06, L * 0.72, C, { outline: 0.004 }), 0, 0.08, L * 0.12));
    g.add(at(box(0.58, 0.06, L * 0.3, C, { outline: 0.004 }), 0, 0.17, -L * 0.36, -0.45, 0, 0));
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(at(box(0.04, 0.12, 0.04, '#F4F1E8'), sx * 0.28, -0.05, sz * (L / 2 - 0.08)));
    return g;
  },
};
