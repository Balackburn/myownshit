// « Le pneu » (story 97, cycle 52): this man took his flat tyre to the doctor. Diagnosis: flat, it is a depression. Three weeks off, no driving. Then
// to the psychiatrist, pushing the car: the tyre spoke of its childhood, a wheelbarrow. At a mountain spa it met an inner tube. The three other tyres
// went off sick in solidarity, then every car in the country, the ambulances too (the patients push them). The minister declared the epidemic and
// a national vaccination: one shot of air per tyre. The vaccine is a pump, refunded at sixty-five percent, and the minister patented it. The tyre came
// home pumped up, the inner tube moved in. This man, who pushed everything, is flat himself. Sick leave refused: he has no valve.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time. Every name
// starts with `pn` (props.js merges all the story tables into one: a plain `tyre` could override another story's).
import * as THREE from 'three';
import { box, cyl, sphere, mat, addOutline } from './style.js';
import { grp, at, canvasPlane, rod } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = x => { const u = clamp01(x), c = 1.70158; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const noShadow = m => { m.traverse(c => { c.castShadow = false; }); return m; };
// a value keyed in time: keys [[t, v], ...] (sorted), eased (smoothstep) from each key to the next over the gap between them
function kv(keys, t, def = 0) {
  if (keys == null) return def;
  if (typeof keys === 'number') return keys;
  if (!keys.length) return def;
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) { const [a, va] = keys[i], [b, vb] = keys[i + 1]; if (t < b) return va + (vb - va) * smooth((t - a) / Math.max(1e-4, b - a)); }
  return keys[keys.length - 1][1];
}
// the start of the last change of a keyed value before t (for the bounce after a drop or a pop), or null
function lastChange(keys, t) {
  if (!Array.isArray(keys)) return null;
  let tc = null;
  for (let i = 0; i < keys.length - 1; i++) if (keys[i + 1][1] !== keys[i][1] && keys[i][0] <= t) tc = keys[i][0];
  return tc;
}
// the last change of a keyed value before t with its sign (+1 rising, -1 falling), or null
function lastStep(keys, t) {
  if (!Array.isArray(keys)) return null;
  let r = null;
  for (let i = 0; i < keys.length - 1; i++) if (keys[i + 1][1] !== keys[i][1] && keys[i][0] <= t) r = { tc: keys[i][0], dir: Math.sign(keys[i + 1][1] - keys[i][1]), dt: keys[i + 1][0] - keys[i][0] };
  return r;
}
// a pop-in scale: 0 before t0, a springy overshoot to 1 over d s
const popS = (t, t0, d = 0.22) => t < t0 ? 0 : outBack((t - t0) / d);
// a quick swell for each time of a list (a puff): 1 + a over 0.12 s, back over 0.25 s
function puffK(list, t, a = 0.12) { let v = 1; for (const p of [].concat(list || [])) { const u = t - p; if (u >= 0 && u < 0.37) v *= 1 + a * (u < 0.12 ? smooth(u / 0.12) : 1 - smooth((u - 0.12) / 0.25)); } return v; }

const RUBBER = '#2E3036', RIM = '#B9C0C8', HUB = '#8C949D';

// ================================================================= the tyre
// The deformable rubber of a tyre: a torus around +Z (major radius R, tube r) whose vertices are rebuilt each frame from its rest shape for a
// flatness f (0 plump, 1 flat). 'up' (standing on its tread): it sinks to 64 % of its height, the bottom presses flat on the floor and bulges
// sideways (the flat-tyre look), the top droops; 'lie' (lying on its side, the axis vertical once the group is turned): it thins to 45 % and
// spreads a little (a pancake). Returns the parts so the caller can place the rim and the valve.
function rubber(R, r, color, seg = [9, 26]) {
  const geo = new THREE.TorusGeometry(R, r, seg[0], seg[1]), base = Float32Array.from(geo.attributes.position.array);
  const m = new THREE.Mesh(geo, mat(color, { unique: true }));
  m.castShadow = m.receiveShadow = true; addOutline(m, 0.025);
  const Rt = R + r;
  // the deformed place of a rest point (x, y, z) for flatness f in a mode; also used for the tread blocks and the valve
  const warp = (x, y, z, f, mode) => {
    if (f <= 0) return [x, y, z];
    if (mode === 'lie') { const s = 1 + 0.14 * f, rho = Math.hypot(x, y) / Rt; return [x * s, y * s, z * (1 - 0.6 * f) - 0.25 * f * r * rho * rho]; }
    const s = 1 - 0.26 * f, floor = -Rt * (1 - 0.45 * f), k = clamp01(-y / Rt), top = clamp01(y / Rt);
    let ny = y * s - 0.12 * f * Rt * top * (1 - Math.abs(x) / Rt);
    if (ny < floor) ny = floor + (ny - floor) * 0.1;
    return [x * (1 + 0.28 * f * k), ny, z * (1 + 1.1 * f * k * k)];
  };
  let lastF = -1, lastMode = '';
  const set = (f, mode) => {
    if (Math.abs(f - lastF) < 1e-4 && mode === lastMode) return;
    lastF = f; lastMode = mode; const p = geo.attributes.position;
    for (let i = 0; i < p.count; i++) { const [x, y, z] = warp(base[i * 3], base[i * 3 + 1], base[i * 3 + 2], f, mode); p.setXYZ(i, x, y, z); }
    p.needsUpdate = true; geo.computeVertexNormals(); geo.computeBoundingSphere();
  };
  // the height of the axle above the floor for the mode
  const axle = (f, mode) => mode === 'lie' ? r * (1 - 0.6 * f) : Rt * (1 - 0.45 * f);
  return { m, set, warp, axle, Rt };
}

// A loose tyre (pivot at the floor under it; standing on its tread, its side wall faces +Z): o.R (0.27) and o.r (0.1); a grey rim with five bolts
// and a big valve stem (chrome stem with a red cap, o.valveS 1.6 x a real one) on the rim face at the upper right (userData.valve: its tip, local,
// for the doctor's fingers); o.flat [[t, f]] (0 plump, 1 pancake flat); o.lie: lying on its side, the rim face up (the valve sticking up);
// o.rim === false: no rim (the hole open, for the inner tube); o.shine: a white highlight arc (plump and shiny); o.towel 'drape' (a white towel
// over its top, two ends hanging) or 'scarf' (wrapped round its top, one end hanging in front); o.blanket: a tartan blanket draped over its top
// half; o.roll [[t, d]]: rolled d metres (it turns about its axle; the caller moves it with to keys); o.puff [t, ...]: a swell (a sigh, a pump);
// o.breathe (0): a slow faint swell (alive); o.color.
function tyreMesh(o = {}) {
  const R = o.R ?? 0.27, r = o.r ?? 0.1, g = grp(), lift = grp(), spin = grp(); g.add(lift); lift.add(spin);
  const ru = rubber(R, r, o.color || RUBBER); lift.add(ru.m);   // (pass 2) the rubber rides on lift: a flat tyre keeps its flat spot at the floor while the rim and valve turn
  // tread blocks round the outside (they follow the rubber)
  const NB = o.tread ? 26 : 0, blocks = [];   // (pass 1) o.tread: tread blocks (a ring of them read as gear teeth on the lying tyre: off by default)
  for (let i = 0; i < NB; i++) { const a = i / NB * TAU, b = box(0.03, 0.012, r * 1.2, '#1E2025'); spin.add(b); blocks.push({ b, a }); }
  // the rim, its bolts and the valve
  const rimG = grp(), rr = R - r * 0.75; spin.add(rimG);
  if (o.rim !== false) {
    rimG.add(at(cyl(rr, rr, r * 1.3, RIM, 16, { outline: 0.01 }), 0, 0, 0, PI / 2), at(cyl(rr * 0.42, rr * 0.42, r * 1.42, HUB, 10), 0, 0, 0, PI / 2));
    for (let i = 0; i < 5; i++) { const a = i / 5 * TAU; rimG.add(at(cyl(0.012, 0.012, r * 1.5, '#5E656D', 6), Math.cos(a) * rr * 0.25, Math.sin(a) * rr * 0.25, 0, PI / 2)); }
  }
  const vs = o.valveS ?? 1.6, va = PI * 0.3, vr = rr * 0.78, valve = grp();
  valve.add(at(cyl(0.012 * vs, 0.014 * vs, 0.07 * vs, '#D8DCE0', 8, { pivot: 'bottom', outline: 0.04 }), 0, 0, 0), at(cyl(0.017 * vs, 0.017 * vs, 0.03 * vs, '#D23A2E', 8, { pivot: 'bottom', outline: 0.04 }), 0, 0.07 * vs, 0));
  valve.rotation.x = PI / 2 - 0.35; if (o.rim !== false) spin.add(valve);
  const vBase = [Math.cos(va) * vr, Math.sin(va) * vr, r * 0.65];
  g.userData.valve = [vBase[0], vBase[1] + ru.Rt, vBase[2] + 0.1 * vs];
  // a shine arc on the front wall
  let shine = null;
  if (o.shine) { shine = noShadow(new THREE.Mesh(new THREE.TorusGeometry(R + r * 0.35, 0.012, 4, 12, PI * 0.38), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.75 }))); shine.position.z = r * 0.75; shine.rotation.z = PI * 0.52; spin.add(shine); }
  // drapes over the top: an open cylinder shell round the axle (they ride on lift, not spin: they do not turn when it rolls)
  // (pass 1) the shell is centred on the top: the cylinder's theta 0 lies on +Z, which the quarter turn about X sends to -Y (the arc hung under the water)
  const drape = (arc, width, material, rad) => { const geo = new THREE.CylinderGeometry(rad, rad, width, 18, 1, true, PI - arc / 2, arc); const m = new THREE.Mesh(geo, material); m.rotation.x = PI / 2; m.castShadow = true; return m; };
  const drapes = grp(); lift.add(drapes);
  // a flat panel of cloth over the upper part of a side wall (the part of a disc of radius rad above the height cut), at z
  const cap = (rad, cut, z, material) => { const sh = new THREE.Shape(), a0 = Math.asin(Math.max(-0.99, Math.min(0.99, cut / rad))); sh.absarc(0, 0, rad, a0, PI - a0, false); sh.lineTo(Math.cos(a0) * rad, cut);
    const m = new THREE.Mesh(new THREE.ShapeGeometry(sh, 16), material); m.position.z = z; m.castShadow = true; return m; };
  if (o.towel) {
    const tm = mat('#F6F4EE', { doubleSide: true });
    if (o.towel === 'scarf') {
      // (pass 3) a short thick towel wound round the top like a scarf (a long arc read as a mudguard): a fat white roll over the top third, a knot
      // on the front and two short stubby ends sticking out
      const roll = new THREE.Mesh(new THREE.TorusGeometry(ru.Rt + 0.02, r * 0.95, 8, 14, PI * 0.42), mat('#F6F4EE')); roll.rotation.z = PI * 0.29; roll.castShadow = true; addOutline(roll, 0.05); drapes.add(roll);
      for (let i = 0; i < 3; i++) { const st = new THREE.Mesh(new THREE.TorusGeometry(ru.Rt + 0.02, r * 0.97, 6, 3, 0.05), mat('#6E9FD4')); st.rotation.z = PI * (0.36 + i * 0.12); drapes.add(st); }
      const knot = sphere(r * 1.05, '#F6F4EE', 1, { outline: 0.06 }); knot.position.set(0, ru.Rt + 0.02, r * 0.9); drapes.add(knot);
      for (const sd of [-1, 1]) drapes.add(at(box(0.11, 0.2, 0.07, '#F6F4EE', { pivot: 'top', outline: 0.04 }), sd * 0.07, ru.Rt + 0.0, r * 1.3, 0.25, 0, sd * 0.55));
    } else {
      // (pass 2) folded over the top, not a hood: a narrower arc, small side flaps, two ends hanging at the sides
      drapes.add(drape(PI * 0.62, r * 2.4, tm, ru.Rt + 0.02));
      for (const z of [-1, 1]) drapes.add(cap(ru.Rt + 0.02, ru.Rt * 0.72, z * r * 1.2, tm));
      for (const s of [-1, 1]) drapes.add(at(box(0.18, 0.04, r * 2.4, '#F6F4EE', { outline: 0.01 }), s * ru.Rt * 0.55, ru.Rt * 0.86, 0, 0, 0, -s * 0.9));
      drapes.add(at(box(0.3, 0.02, r * 2.62, '#C9D6DE'), 0, ru.Rt + 0.03, 0));
    }
  }
  if (o.blanket) {
        const c = document.createElement('canvas'); c.width = c.height = 128; const x = c.getContext('2d');
    x.fillStyle = '#B5322E'; x.fillRect(0, 0, 128, 128); x.fillStyle = 'rgba(30,60,40,0.55)'; for (let i = 0; i < 128; i += 32) { x.fillRect(i, 0, 12, 128); x.fillRect(0, i, 128, 12); }
    x.fillStyle = 'rgba(240,200,80,0.7)'; for (let i = 16; i < 128; i += 32) { x.fillRect(i, 0, 3, 128); x.fillRect(0, i, 128, 3); }
    const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.repeat.set(3, 1); tex.magFilter = THREE.NearestFilter;
    const tart = new THREE.MeshLambertMaterial({ map: tex, side: THREE.DoubleSide });
    drapes.add(drape(PI * 1.2, r * 3.2, tart, ru.Rt + 0.03));
    for (const z of [-1, 1]) drapes.add(cap(ru.Rt + 0.03, ru.Rt * 0.05, z * r * 1.6, tart));
    for (const s of [-1, 1]) { const f = new THREE.Mesh(new THREE.PlaneGeometry(r * 3.2, 0.34), tart); f.position.set(s * (ru.Rt * 0.93 + 0.03), -0.12, 0); f.rotation.set(0, PI / 2, s * 0.12); drapes.add(f); }
  }
  const mode = o.lie ? 'lie' : 'up';
  g.userData.update = t => {
    const f = clamp01(kv(o.flat, t, 0)), pf = puffK(o.puff, t, 0.1) * (1 + (o.breathe ?? 0) * 0.5 * (1 + Math.sin(t * 2.4)));
    ru.set(f, mode);
    for (const { b, a } of blocks) { const [x, y, z] = ru.warp(Math.cos(a) * (ru.Rt - 0.004), Math.sin(a) * (ru.Rt - 0.004), 0, f, mode); b.position.set(x, y, z); b.rotation.z = a - PI / 2; }
    const s = mode === 'lie' ? 1 : 1 - 0.26 * f, rolling = !!o.roll && f > 0;
    if (rolling) rimG.scale.setScalar(s * 0.86); else rimG.scale.set(1, s, 1);   // a flat tyre that rolls: a smaller round rim (an oval one would turn)
    const [vx, vy, vz] = ru.warp(vBase[0], vBase[1], vBase[2], f, mode); if (rolling) valve.position.set(vBase[0] * s * 0.86, vBase[1] * s * 0.86, vz); else valve.position.set(vx, mode === 'lie' ? vy : vBase[1] * s, vz);
    spin.rotation.z = o.roll ? -kv(o.roll, t, 0) / ru.Rt : 0;
    const h = ru.axle(f, mode);
    if (mode === 'lie') { lift.rotation.x = -PI / 2; lift.position.y = h; } else lift.position.y = h;
    drapes.visible = f < 0.5 || mode === 'up'; drapes.position.y = mode === 'up' ? -0.45 * f * ru.Rt : 0; drapes.scale.set(1, 1 - 0.3 * f, 1 + 0.4 * f);
    const sv = kv(o.stretch, t, 0); lift.scale.set(pf * (1 - 0.5 * sv), pf * (1 + sv), pf);   // (pass 2) o.stretch [[t, v]]: taller and thinner (a pumped-up stretch)
  };
  g.userData.axle = f => ru.axle(f, mode);
  g.userData.update(-1); return g;
}

// ================================================================= a car's wheel (for pnCar, pnWave and pnVan)
// a wheel group (axle at its origin, the side wall facing +Z or -Z by side s); state 0 plump, 1 flat (the tyre squashed), 2 bare rim (no tyre,
// the rim on the road); returns { g, set(state, spinAngle), axle(state) }
function carWheel(s, R = 0.2, r = 0.11, lite = false) {
  const g = grp(), spin = grp(); g.add(spin);
  const ru = rubber(R, r, RUBBER, lite ? [6, 16] : [8, 22]); g.add(ru.m);   // (pass 2) the rubber does not turn: its flat spot stays down
  const rr = R - r * 0.7, rim = grp(at(cyl(rr, rr, r * 1.4, RIM, 14, { outline: 0.01 }), 0, 0, 0, PI / 2), at(cyl(rr * 0.4, rr * 0.4, r * 1.5, HUB, 8), 0, 0, 0, PI / 2));
  if (!lite) for (let i = 0; i < 4; i++) { const a = i / 4 * TAU; rim.add(at(box(0.03, 0.012, r * 1.45, '#6B727A'), Math.cos(a) * rr * 0.62, Math.sin(a) * rr * 0.62, 0, 0, 0, a)); }
  spin.add(rim); g.scale.z = s;
  // sv: a stretch (pumped up: taller and thinner, then the snap round overshoots)
  const set = (st, ang = 0, sv = 0) => {
    const f = clamp01(st), bare = st > 1.5;
    ru.m.visible = !bare; ru.set(f, 'up'); rim.scale.setScalar(bare ? 1 : 1 - 0.26 * f); spin.rotation.z = ang;
    ru.m.scale.set(1 - 0.45 * sv, 1 + sv, 1); spin.scale.set(1 - 0.3 * sv, 1 + 0.6 * sv, 1);
  };
  const axle = st => st > 1.5 ? rr : ru.axle(clamp01(st), 'up');
  return { g, set, axle };
}

// a box head looking out of a car (pivot at its neck): skin box, two dot eyes, a dark hair cap
function boxHead(skin = '#E7B98F', hair = '#3A2E26') {
  const g = grp(at(box(0.3, 0.3, 0.3, skin, { pivot: 'bottom', outline: 0.02 }), 0, 0, 0), at(box(0.31, 0.07, 0.31, hair), 0, 0.29, 0));
  for (const z of [-0.07, 0.07]) g.add(at(box(0.02, 0.05, 0.03, '#1B1B1E'), 0.152, 0.17, z));
  return g;
}

// ================================================================= the car
// One small city car facing +X (pivot at the floor in its middle; 3.5 long, 1.62 wide): opts as pnCar's (o.lite: fewer faces, for crowds).
// Returns { g, update }.
function carBuild(o = {}) {
  const C = o.color || '#6CC4A4', L = 3.5, Wd = 1.62, g = grp(), body = grp(), lite = !!o.lite; g.add(body);
  const DARK = '#3E434C', GLASS = o.glassColor || '#BFE3EE', D = new THREE.Color(C).multiplyScalar(0.82).getStyle();
  body.add(at(box(L, 0.56, Wd, C, { outline: 0.012 }), 0, 0.64, 0));                       // the lower body, 0.36 .. 0.92
  body.add(at(box(L + 0.05, 0.14, Wd + 0.04, DARK), 0, 0.4, 0));                         // bumpers and sills
  for (const z of [-1, 1]) for (const x of [-1.15, 1.15]) body.add(at(box(0.78, 0.1, 0.04, D), x, 0.86, z * (Wd / 2 + 0.005)));   // wheel arches' lips
  const cx = -0.3, cy0 = 0.92, ch = 0.62;
  if (o.open) {
    // a soft-top folded at the back, a windscreen in a frame, two front seats and a bench
    body.add(at(box(0.04, ch * 0.75, 1.36, GLASS, { noGrain: true }), 0.62, cy0 + ch * 0.36, 0, 0, 0, 0.35), at(box(0.06, 0.06, 1.42, DARK), 0.74, cy0 + ch * 0.72, 0));
    body.add(at(box(0.55, 0.2, Wd - 0.08, '#2F3238', { outline: 0.008 }), -1.5, cy0 + 0.08, 0));
    for (const z of [-0.38, 0.38]) body.add(at(box(0.42, 0.1, 0.5, '#4A3A2E'), 0.15, cy0 - 0.02, z), at(box(0.1, 0.48, 0.5, '#4A3A2E'), -0.08, cy0 + 0.2, z, 0, 0, 0.12));
    body.add(at(box(0.5, 0.1, 1.3, '#4A3A2E'), -0.75, cy0 - 0.02, 0), at(box(0.1, 0.42, 1.3, '#4A3A2E'), -1.02, cy0 + 0.18, 0, 0, 0, 0.12));
    body.add(at(box(L * 0.92, 0.06, 0.1, D), -0.05, cy0 + 0.02, Wd / 2 - 0.05), at(box(L * 0.92, 0.06, 0.1, D), -0.05, cy0 + 0.02, -Wd / 2 + 0.05));
  } else {
    body.add(at(box(1.95, ch, 1.48, C, { outline: 0.01, taper: { x: 0.76, z: 0.84 } }), cx, cy0 + ch / 2, 0));
    const slope = Math.atan2(1.95 * 0.12, ch), sideA = Math.atan2(0.74 * 0.16, ch);
    body.add(at(box(0.02, ch * 0.8, 1.2, GLASS, { noGrain: true }), cx + 1.95 / 2 - 1.95 * 0.06 + 0.012, cy0 + ch * 0.48, 0, 0, 0, slope));
    body.add(at(box(0.02, ch * 0.72, 1.14, GLASS, { noGrain: true }), cx - 1.95 / 2 + 1.95 * 0.06 - 0.012, cy0 + ch * 0.48, 0, 0, 0, -slope));
    for (const sz of [-1, 1]) for (const [x, w] of [[0.24, 0.6], [-0.5, 0.6]]) body.add(at(box(w, ch * 0.62, 0.02, GLASS, { noGrain: true }), cx + x, cy0 + ch * 0.47, sz * (0.74 * 0.92 + 0.012), -sz * sideA, 0, 0));
  }
  if (!lite) {
    for (const z of [-0.55, 0.55]) body.add(at(box(0.03, 0.14, 0.3, '#FFF6D8', { emissive: '#7A6A3A' }), L / 2 + 0.02, 0.72, z), at(box(0.03, 0.1, 0.26, '#C8392E'), -L / 2 - 0.02, 0.74, z));
    body.add(at(box(0.03, 0.12, 0.4, '#F2F0E8'), L / 2 + 0.035, 0.42, 0), at(box(0.03, 0.12, 0.4, '#F2F0E8'), -L / 2 - 0.035, 0.42, 0));   // blank plates
    for (const z of [-1, 1]) body.add(at(box(0.16, 0.03, 0.03, '#2A2C31'), 0.15, 0.82, z * (Wd / 2 + 0.01)));   // door handles
  }
  // the driver's head (o.driver: a skin colour or true) in the left seat (+Z), leaning out of the window between o.leanOut [t0, t1]
  let head = null;
  if (o.driver) { head = boxHead(typeof o.driver === 'string' ? o.driver : '#E7B98F', o.hair || '#3A2E26'); head.position.set(0.05, cy0 + 0.16, 0.38); body.add(head); }
  // the cargo tyre standing on the back bench (o.cargo: tyre opts), under its blanket
  let cargo = null;
  if (o.cargo) { cargo = tyreMesh({ R: 0.24, r: 0.09, ...o.cargo }); cargo.position.set(-0.78, cy0 + 0.12, 0); body.add(cargo); }
  // wheels: o.wheels [fl, fr, rl, rr] each a keyed state [[t, s], ...] or a number (or o.state for all four); 0 plump, 1 flat, 2 bare rim
  const WP = [[1.15, 0.74], [1.15, -0.74], [-1.15, 0.74], [-1.15, -0.74]], wheels = WP.map(([x, z]) => { const w = carWheel(z > 0 ? 1 : -1, 0.2, 0.11, lite); w.g.position.set(x, 0.31, z); g.add(w.g); return w; });
  const keysOf = i => (o.wheels && o.wheels[i] != null) ? o.wheels[i] : (o.state ?? 0);
  // sparks from each bare wheel's contact (o.sparks [[t0, t1], ...]: they spray while it moves)
  const sparkSets = [];
  if (o.sparks) for (const [x, z] of WP) { const sg = grp(), st = []; for (let i = 0; i < 9; i++) { const m = noShadow(new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.014, 0.014), new THREE.MeshBasicMaterial({ color: i % 3 ? '#FFB23A' : '#FFF2A8' }))); sg.add(m); st.push(m); } sg.position.set(x, 0.02, z + Math.sign(z) * 0.08); g.add(sg); sparkSets.push({ sg, st }); }
  // a dust puff at each wheel when it drops (o.dust: true)
  const puffs = [];
  if (o.dust) for (const [x, z] of WP) { const pg = grp(); for (let i = 0; i < 4; i++) { const m = noShadow(sphere(0.22, '#D8CFBA', 0, { unique: true, opacity: 0.9 })); pg.add(m); } pg.position.set(x, 0.05, z + Math.sign(z) * 0.15); g.add(pg); puffs.push(pg); }
  const R0 = 0.31;
  const update = t => {
    const st = [0, 1, 2, 3].map(i => kv(keysOf(i), t, 0)), roll = o.roll ? kv(o.roll, t, 0) : 0;
    const h = st.map((s, i) => wheels[i].axle(s));
    // (pass 2) a wheel pumped up (its state falls) stretches tall while it fills, then snaps round with an overshoot; a wheel that drops (its
    // state rises) squashes the whole body on the bounce
    let bounce = 0, squash = 0;
    wheels.forEach((w, i) => {
      const ls = lastStep(keysOf(i), t); let sv = 0;
      if (ls && ls.dir < 0) { const u = t - ls.tc, A = o.stretchAmp ?? 0.45; if (u >= 0 && u < ls.dt) sv = A * smooth(u / ls.dt); else if (u >= ls.dt && u < ls.dt + 0.8) { const v = u - ls.dt; sv = v < 0.07 ? A : A * Math.exp(-5 * (v - 0.07)) * Math.cos((v - 0.07) * 16); } }   // (pass 3) o.stretchAmp; the stretch held two frames before the snap
      if (ls && ls.dir > 0) { const u = t - ls.tc - ls.dt; if (u > 0 && u < 0.9) { bounce += -0.11 * Math.exp(-5 * u) * Math.sin(u * 17 + 0.6); squash += 0.16 * Math.exp(-6 * u) * Math.cos(u * 17); } }
      w.set(st[i], -roll / R0, sv); w.g.position.y = h[i] * (1 + sv);
    });
    const front = (h[0] + h[1]) / 2, back = (h[2] + h[3]) / 2, left = (h[0] + h[2]) / 2, right = (h[1] + h[3]) / 2;
    const sq = Math.max(-0.12, Math.min(0.18, squash)); body.scale.set(1 + 0.4 * sq, 1 - sq, 1 + 0.4 * sq);
    body.position.y = (front + back) / 2 - R0 + bounce; body.rotation.z = Math.atan2(front - back, 2.3); body.rotation.x = -Math.atan2(left - right, 1.48);
    if (head && o.leanOut) { const k = smooth((t - o.leanOut[0]) / 0.3) * (1 - smooth((t - o.leanOut[1]) / 0.3)); head.position.z = 0.38 + 0.72 * k; head.position.y = cy0 + 0.16 + 0.12 * k; head.rotation.x = -0.35 * k; }
    sparkSets.forEach(({ sg, st: ss }, i) => {
      const on = st[i] > 1.5 && o.sparks.some(([a, b]) => t >= a && t <= b); sg.visible = on; if (!on) return;
      ss.forEach((m, j) => { const per = 0.3, u = ((t + j * 0.037) % per) / per, a = PI * (0.75 + 0.5 * hsh(j)); m.position.set(Math.cos(a) * 0.9 * u, 0.02 + 0.35 * u * (1 - u) * (1 + hsh(j + 3)), (hsh(j + 7) - 0.5) * 0.3 * u); m.rotation.z = -a; m.scale.x = 1 - u * 0.6; });
    });
    puffs.forEach((pg, i) => { const tc = lastChange(keysOf(i), t), u = tc == null ? -1 : t - tc - 0.05; const on = u > 0 && u < 0.9; pg.visible = on; if (!on) return;
      pg.children.forEach((m, j) => { const a = j / 4 * TAU + 0.6; m.position.set(Math.cos(a) * 0.5 * smooth(u * 1.6), 0.1 + 0.25 * u, Math.sin(a) * 0.3 * smooth(u * 1.6)); m.scale.setScalar(0.5 + 1.4 * smooth(u * 1.4)); m.material.opacity = 0.85 * (1 - smooth((u - 0.3) / 0.6)); }); });
    if (cargo) cargo.userData.update(t);
  };
  return { g, update };
}

// ================================================================= a white ambulance van
// A white box van facing +X (pivot at the floor in its middle; 5.2 long, 2.0 wide, 2.5 tall): a plain orange stripe along both sides and round the
// back, no cross, no word, no emblem; two back doors at -X with a handle each (userData.back: the middle of the doors, local, for the hands that
// push); a dark cab window; o.state / o.wheels as pnCar (o.state 1: flat on all four); o.driver: a box head behind the windscreen.
function vanBuild(o = {}) {
  const g = grp(), body = grp(); g.add(body); const W = 2.0, Wc = '#F4F4F0', OR = o.stripe || '#E8742A';
  body.add(at(box(3.7, 2.05, W, Wc, { pivot: 'bottom', outline: 0.014 }), -0.75, 0.45, 0));
  body.add(at(box(1.5, 0.75, W, Wc, { pivot: 'bottom', outline: 0.012 }), 1.85, 0.45, 0), at(box(0.9, 0.85, W - 0.04, Wc, { outline: 0.01, taper: { x: 0.6, z: 1 } }), 1.55, 1.62, 0));
  body.add(at(box(0.04, 0.6, W - 0.3, '#5E7C92', { noGrain: true }), 2.03, 1.62, 0, 0, 0, 0.5));
  for (const z of [-1, 1]) body.add(at(box(0.62, 0.48, 0.03, '#5E7C92', { noGrain: true }), 1.5, 1.62, z * (W / 2 + 0.005)));
  for (const z of [-1, 1]) body.add(at(box(5.25, 0.26, 0.03, OR), 0.0, 1.05, z * (W / 2 + 0.01)));
  body.add(at(box(0.03, 0.26, W + 0.02, OR), -2.615, 1.05, 0));
  body.add(at(box(0.03, 1.9, 0.02, '#9AA3AD'), -2.615, 1.47, 0));                              // the seam between the back doors
  for (const z of [-0.12, 0.12]) body.add(at(box(0.05, 0.05, 0.14, '#4A4F55'), -2.64, 1.35, z));
  body.add(at(box(0.18, 0.18, W + 0.04, '#3A3D44'), 2.55, 0.52, 0), at(box(0.18, 0.18, W + 0.04, '#3A3D44'), -2.62, 0.52, 0));
  for (const z of [-0.7, 0.7]) body.add(at(box(0.03, 0.16, 0.34, '#FFF6D8', { emissive: '#7A6A3A' }), 2.62, 0.82, z));
  if (o.driver) { const hd = boxHead(); hd.position.set(1.45, 1.22, 0.4); body.add(hd); }
  const WP = [[1.7, 0.86], [1.7, -0.86], [-1.65, 0.86], [-1.65, -0.86]], wheels = WP.map(([x, z]) => { const w = carWheel(z > 0 ? 1 : -1, 0.25, 0.13); w.g.position.set(x, 0.38, z); w.g.scale.setScalar(1.0); g.add(w.g); return w; });
  const keysOf = i => (o.wheels && o.wheels[i] != null) ? o.wheels[i] : (o.state ?? 0), R0 = 0.38;
  const update = t => {
    const st = [0, 1, 2, 3].map(i => kv(keysOf(i), t, 0)), h = st.map((s, i) => wheels[i].axle(s)), roll = o.roll ? kv(o.roll, t, 0) : 0;
    wheels.forEach((w, i) => { w.set(st[i], -roll / R0); w.g.position.y = h[i]; });
    const front = (h[0] + h[1]) / 2, back = (h[2] + h[3]) / 2; body.position.y = (front + back) / 2 - R0; body.rotation.z = Math.atan2(front - back, 3.35);
  };
  g.userData.back = [-2.64, 1.3, 0];
  return { g, update };
}

// ================================================================= small things
// a sick note's paper (front +Z, pivot at its middle): white, a pale blue header band, six grey writing lines left blank, a box for a signature,
// a strip of tape across its top
function noteMesh(w = 0.2, h = 0.27, tape = true) {
  const g = grp(), p = canvasPlane(w, h, (c, W, H) => {
    c.fillStyle = '#FBFAF4'; c.fillRect(0, 0, W, H); c.fillStyle = '#BFD8EA'; c.fillRect(0, 0, W, H * 0.12);
    c.strokeStyle = '#A9AEB6'; c.lineWidth = Math.max(2, H * 0.008); for (let i = 0; i < 6; i++) { const y = H * (0.25 + i * 0.1); c.beginPath(); c.moveTo(W * 0.1, y); c.lineTo(W * 0.9, y); c.stroke(); }
    c.strokeRect(W * 0.55, H * 0.84, W * 0.35, H * 0.1); c.strokeStyle = '#7F8792'; c.lineWidth = H * 0.012; c.strokeRect(2, 2, W - 4, H - 4);
  }, { res: 256 });
  g.add(p, at(box(w + 0.01, h + 0.01, 0.004, '#E9E6DC'), 0, 0, -0.004));
  if (tape) g.add(at(box(w * 0.7, 0.035, 0.004, '#F3E7B5', { opacity: 0.85 }), 0, h / 2 - 0.01, 0.004, 0, 0, 0.04));
  return g;
}

// the one-wheeled wheelbarrow drawn on a canvas (centre cx, cy, size S): a green tray, one red wheel in front, two handles, two legs
function drawBarrow(c, cx, cy, S) {
  c.lineJoin = 'round'; c.lineCap = 'round'; c.strokeStyle = '#1E2126'; c.lineWidth = S * 0.035;
  // handles and legs
  c.beginPath(); c.moveTo(cx - S * 0.55, cy - S * 0.02); c.lineTo(cx + S * 0.32, cy + S * 0.12); c.stroke();
  c.beginPath(); c.moveTo(cx - S * 0.2, cy + S * 0.07); c.lineTo(cx - S * 0.26, cy + S * 0.3); c.stroke();
  c.beginPath(); c.moveTo(cx + S * 0.05, cy + S * 0.1); c.lineTo(cx + S * 0.0, cy + S * 0.3); c.stroke();
  // the tray
  c.fillStyle = '#4FA36A'; c.beginPath(); c.moveTo(cx - S * 0.35, cy - S * 0.2); c.lineTo(cx + S * 0.38, cy - S * 0.2); c.lineTo(cx + S * 0.2, cy + S * 0.1); c.lineTo(cx - S * 0.2, cy + S * 0.1); c.closePath(); c.fill(); c.stroke();
  c.fillStyle = '#3C8754'; c.fillRect(cx - S * 0.33, cy - S * 0.2, S * 0.69, S * 0.05); c.strokeRect(cx - S * 0.33, cy - S * 0.2, S * 0.69, S * 0.05);
  // the wheel: one, in front
  c.fillStyle = '#D9473A'; c.beginPath(); c.arc(cx + S * 0.33, cy + S * 0.17, S * 0.13, 0, TAU); c.fill(); c.stroke();
  c.fillStyle = '#F2F0E8'; c.beginPath(); c.arc(cx + S * 0.33, cy + S * 0.17, S * 0.04, 0, TAU); c.fill(); c.stroke();
}

export const PNEU_PROPS = {
  // The tyre (see tyreMesh): pivot at the floor under it, standing on its tread with its side wall to +Z; o.flat [[t, f]], o.lie, o.rim, o.shine,
  // o.towel ('drape' or 'scarf'), o.blanket, o.roll [[t, d]], o.puff, o.breathe, o.valveS (1.6), o.R (0.27), o.r (0.1); o.bob [amp, rate]: it bobs
  // up and down (floating), o.sink: it sits that low (in water)
  pnTyre(o) {
    const g = grp(), t0 = tyreMesh(o); g.add(t0);
    const up = t0.userData.update;
    g.userData.update = t => { up(t); t0.position.y = -(o.sink ?? 0) + (o.bob ? o.bob[0] * Math.sin(t * TAU * (o.bob[1] ?? 0.5)) : 0); };
    g.userData.valve = t0.userData.valve; g.userData.update(-1); return g;
  },

  // The inner tube (pivot at its middle; the ring faces +Z): thinner and smaller than the tyre (o.R 0.2, o.r 0.055), reddish rubber (o.color
  // '#C4553F', never black), its own valve stem pointing into the hole (a red-brown stem with a brass tip); o.puff [t, ...]: it swells (twice in
  // S15); o.bob [amp, rate]: floating; o.squash (1): its thickness (a little slack)
  pnTube(o) {
    const R = o.R ?? 0.2, r = o.r ?? 0.055, g = grp(), k = grp(); g.add(k);
    const m = new THREE.Mesh(new THREE.TorusGeometry(R, r, 8, 28), mat(o.color || '#C4553F')); m.castShadow = m.receiveShadow = true; addOutline(m, 0.03); k.add(m);
    const hl = noShadow(new THREE.Mesh(new THREE.TorusGeometry(R, r * 0.25, 4, 12, PI * 0.35), new THREE.MeshBasicMaterial({ color: '#F0A090' }))); hl.position.z = r * 0.8; hl.rotation.z = PI * 0.55; k.add(hl);
    const v = grp(at(cyl(r * 0.32, r * 0.4, 0.1, '#8A3A2C', 8, { pivot: 'bottom', outline: 0.04 }), 0, 0, 0), at(cyl(r * 0.26, r * 0.26, 0.04, '#D9B04A', 8, { pivot: 'bottom', outline: 0.04 }), 0, 0.1, 0));
    v.position.set(0, -(R - r * 0.6), 0); v.rotation.x = 0.35; k.add(v);
    g.userData.update = t => { const p = puffK(o.puff, t, 0.18); k.scale.set(p, p, (o.squash ?? 1) * (1 + (p - 1) * 2)); k.position.y = o.bob ? o.bob[0] * Math.sin(t * TAU * (o.bob[1] ?? 0.5) + 1.3) : 0; };
    g.userData.update(-1); return g;
  },

  // The car (see carBuild): a small city car facing +X, pivot at the floor in its middle; o.color; o.open (a convertible: the soft-top folded, the
  // windscreen in a frame, seats); o.cargo (tyre opts: a tyre standing on the back bench, e.g. { flat: 1, blanket: true }); o.state or o.wheels
  // [fl, fr, rl, rr] keyed states (0 plump, 1 flat, 2 bare rim; front wheels at +X, left at +Z); o.roll [[t, d]] (the wheels turn as it is pushed
  // d metres; move it with to keys); o.sparks [[t0, t1]] (sparks at the bare rims); o.dust (a puff at each wheel that changes); o.driver, o.leanOut
  pnCar(o) { const c = carBuild(o); c.g.userData.update = c.update; c.update(-1); return c.g; },

  // A motorway jam (pivot at the road's middle; the road runs along X, the traffic faces +X): o.lanes [[z, x0, n, gap], ...] rows of n cars from x0
  // toward -X, o.gap apart; every car drops onto flat tyres with a bounce and a dust puff at t0 + d / o.speed, d its distance from the far end
  // (o.farX, the wave rolls toward +X); o.colors; o.road: the asphalt (o.len 90 m, o.w by the lanes), white lane dashes and grey crash barriers
  // on both sides; o.drivers: one car in three has a driver who leans out of his window after the drop
  pnWave(o) {
    const g = grp(), cars = [], lanes = o.lanes || [[0, 0, 8, 5.2]], cols = o.colors || ['#E05A47', '#F2C94C', '#7FB069', '#E8E4DA', '#5A7FB8', '#D98AA8', '#8C6BB8', '#E8833A', '#9AA0A8', '#6CC4A4'];
    const farX = o.farX ?? -60, speed = o.speed ?? 30, t0 = o.t0 ?? 0.3;
    let n = 0;
    for (const [z, x0, cnt, gap] of lanes) for (let i = 0; i < cnt; i++) {
      const x = x0 - i * (gap ?? 5.2) + (hsh(n) - 0.5) * 0.6, td = t0 + Math.max(0, x - farX) / speed + (hsh(n + 9) - 0.5) * 0.08;
      const drv = o.drivers && (o.drivers === 'all' || n % 3 === 1);
      const c = carBuild({ color: cols[n % cols.length], lite: o.lite ?? true, state: [[td, 0], [td + 0.07, 1]], dust: true, driver: drv ? '#E0B48A' : null, leanOut: drv ? [td + 0.35, 99] : null });
      c.g.position.set(x, 0, z + (hsh(n + 3) - 0.5) * 0.25); c.g.rotation.y = (hsh(n + 5) - 0.5) * 0.05; g.add(c.g); cars.push(c); n++;
    }
    if (o.road !== false) {
      const len = o.len ?? 90, zs = lanes.map(l => l[0]), zmin = Math.min(...zs) - 2.2, zmax = Math.max(...zs) + 2.2 + (o.shoulder ?? 0),   // (pass 3) o.shoulder: a wide hard shoulder on the +Z side (a camera stands on it)
        w = zmax - zmin, zc = (zmin + zmax) / 2;
      // (pass 3) painted over the field without a depth test, like parkLot (an offset was not enough at a grazing angle: the field showed through)
      const am = new THREE.MeshLambertMaterial({ color: '#666A70', depthTest: false, depthWrite: false }), dm = new THREE.MeshLambertMaterial({ color: '#F1F0E8', depthTest: false, depthWrite: false });
      const asph = new THREE.Mesh(new THREE.PlaneGeometry(len, w), am); asph.rotation.x = -PI / 2; asph.position.set(-len / 2 + 30, 0.05, zc); asph.receiveShadow = true; asph.renderOrder = -1.5; g.add(asph);
      for (let li = 0; li < zs.length - 1; li++) { const zz = (zs[li] + zs[li + 1]) / 2; for (let x = 30; x > -len + 30; x -= 6) { const d = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 0.14), dm); d.renderOrder = -1.2; d.rotation.x = -PI / 2; d.position.set(x, 0.09, zz); g.add(d); } }
      for (const zz of [zmin, zmax]) { g.add(at(box(len, 0.08, 0.3, '#B8BCC2', { outline: 0.004 }), -len / 2 + 30, 0.62, zz)); for (let x = 30; x > -len + 30; x -= 3) g.add(at(box(0.1, 0.62, 0.1, '#7E848B', { pivot: 'bottom' }), x, 0, zz)); }
    }
    g.userData.update = t => cars.forEach(c => c.update(t));
    g.userData.update(-1); return g;
  },

  // The ambulance (see vanBuild): a white van facing +X, a plain orange stripe, no cross and no emblem (put a blueBeacon on its cab roof at local
  // [1.55, 2.08, 0]); o.state (1: flat), o.roll [[t, d]] (pushed), o.driver; userData.back the middle of its back doors
  pnVan(o) { const v = vanBuild(o); v.g.userData.update = v.update; v.g.userData.back = [-2.64, 1.3, 0]; v.update(-1); return v.g; },

  // A sick note (pivot at its middle, front +Z): blank grey lines, no word; o.w (0.2) x o.h (0.27); o.slapAt: it pops on with a squash (slapped on);
  // o.from / o.until: shown only between; o.tape (true)
  pnNote(o) {
    const g = grp(), n = noteMesh(o.w ?? 0.2, o.h ?? 0.27, o.tape !== false); g.add(n);
    g.userData.update = t => { const vis = (o.from == null || t >= o.from) && (o.until == null || t < o.until); let s = 1;
      if (o.slapAt != null) { const u = t - o.slapAt; s = u < 0 ? 0 : u < 0.06 ? 1.35 - 0.35 * u / 0.06 : 1 + 0.08 * Math.exp(-12 * (u - 0.06)) * Math.sin((u - 0.06) * 40); }
      g.visible = vis && s > 0.01; n.scale.set(s, s, 1); };
    g.userData.update(-1); return g;
  },

  // A sick-note pad on a desk (pivot at its bottom middle): a thick block of the same notes, the top one torn off at o.tearAt (it vanishes: the
  // script shows a pnNote in the doctor's hand from then)
  pnPad(o) {
    const g = grp(at(box(0.22, 0.04, 0.29, '#E9E6DC', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(0.22, 0.012, 0.035, '#5A6A7A'), 0, 0.04, -0.13));
    const top = noteMesh(0.2, 0.27, false); top.rotation.x = -PI / 2; top.position.y = 0.043; g.add(top);
    const under = noteMesh(0.2, 0.27, false); under.rotation.x = -PI / 2; under.position.y = 0.041; g.add(under);
    g.userData.update = t => { top.visible = o.tearAt == null || t < o.tearAt; };
    g.userData.update(-1); return g;
  },

  // An examination table (pivot at the floor in its middle, long along X): a padded pale green top at 0.82 m on a white base, a paper sheet down
  // its middle, a raised head end at -X
  pnExam(o) {
    const L = o.len ?? 1.9, g = grp(at(box(L * 0.8, 0.62, 0.5, '#E9ECEA', { pivot: 'bottom', outline: 0.008 }), 0, 0.1, 0), at(box(L, 0.12, 0.72, o.color || '#8FC1B2', { pivot: 'bottom', outline: 0.008 }), 0, 0.72, 0));
    g.add(at(box(L * 0.92, 0.006, 0.42, '#FBFAF4'), 0.04, 0.843, 0));
    if (o.head !== false) g.add(at(box(0.55, 0.12, 0.72, o.color || '#8FC1B2', { outline: 0.008 }), -L / 2 + 0.3, 0.9, 0, 0, 0, -0.32));   // (pass 2) o.head false: flat (the raised end read as a stray green slab)
    for (const x of [-L * 0.36, L * 0.36]) for (const z of [-0.2, 0.2]) g.add(at(box(0.08, 0.1, 0.08, '#5E656D', { pivot: 'bottom' }), x, 0, z));
    return g;
  },

  // A stethoscope's chest piece (pivot at its middle; attach to a hand): a steel disc with a black rim and a short black tube curling up
  pnSteth(o) {
    const s = o.s ?? 1, g = grp(at(cyl(0.035 * s, 0.035 * s, 0.018 * s, '#D3D8DD', 10, { outline: 0.05 }), 0, 0, 0, PI / 2), at(cyl(0.038 * s, 0.038 * s, 0.008 * s, '#1E2126', 10), 0, 0, -0.01 * s, PI / 2));
    g.add(rod([0, 0, -0.012 * s], [0, 0.08 * s, -0.05 * s], 0.007 * s, '#1E2126'), rod([0, 0.08 * s, -0.05 * s], [0.04 * s, 0.2 * s, -0.06 * s], 0.007 * s, '#1E2126'));
    return g;
  },

  // A stethoscope worn round the neck (attach to the 'neck' joint): a black U hanging on the chest with two steel ear tips at the collar
  pnStethNeck(o) {
    const g = grp(), y = o.y ?? -0.12, z = o.z ?? 0.13, w = o.w ?? 0.14;
    const curve = new THREE.CatmullRomCurve3([new THREE.Vector3(-w, y + 0.1, z - 0.06), new THREE.Vector3(-w * 0.9, y - 0.12, z), new THREE.Vector3(0, y - 0.24, z + 0.03), new THREE.Vector3(w * 0.9, y - 0.12, z), new THREE.Vector3(w, y + 0.1, z - 0.06)]);
    const m = new THREE.Mesh(new THREE.TubeGeometry(curve, 16, 0.01, 5), mat('#1E2126')); g.add(m);
    g.add(at(cyl(0.028, 0.028, 0.014, '#D3D8DD', 8), 0, y - 0.25, z + 0.04, PI / 2));
    return g;
  },

  // Car keys (pivot at the ring; attach to a hand): a steel ring, two keys and a dark fob
  pnKeys(o) {
    const s = o.s ?? 1.4, g = grp(at(new THREE.Mesh(new THREE.TorusGeometry(0.022 * s, 0.004 * s, 4, 10), mat('#C9CED4')), 0, 0, 0));
    g.add(at(box(0.012 * s, 0.07 * s, 0.004 * s, '#C9CED4'), 0.012 * s, -0.05 * s, 0, 0, 0, 0.2), at(box(0.012 * s, 0.06 * s, 0.004 * s, '#B89A4A'), -0.012 * s, -0.045 * s, 0, 0, 0, -0.25));
    g.add(at(box(0.04 * s, 0.06 * s, 0.016 * s, '#26282D', { outline: 0.04 }), 0, -0.04 * s, 0.012 * s));
    return g;
  },

  // A psychiatrist's couch (pivot at the floor in its middle, long along X, front +Z): a brown leather chaise longue, its head end raised at -X,
  // a round bolster, short dark legs
  pnCouch(o) {
    // (pass 2) a real chaise longue: a tufted oxblood leather seat at 0.45 on turned legs, a high curled head end at -X rising to 1.0 m with a
    // rolled top, a bolster; userData.headRest: the point (local) a reclining tyre leans on
    const C = o.color || '#8B3A2E', D = new THREE.Color(C).multiplyScalar(0.72).getStyle(), Lt = new THREE.Color(C).multiplyScalar(1.15).getStyle(), L = o.len ?? 1.9, g = grp();
    for (const x of [-L / 2 + 0.12, L / 2 - 0.12]) for (const z of [-0.3, 0.3]) g.add(at(cyl(0.04, 0.025, 0.22, '#3A2618', 8, { pivot: 'bottom', outline: 0.02 }), x, 0, z));
    g.add(at(box(L, 0.12, 0.76, '#5A3A22', { pivot: 'bottom', outline: 0.01 }), 0, 0.2, 0));
    g.add(at(box(L - 0.08, 0.14, 0.7, C, { pivot: 'bottom', outline: 0.01 }), 0.02, 0.31, 0));
    for (let i = 0; i < 5; i++) for (const z of [-0.18, 0.18]) g.add(at(sphere(0.018, D, 0), -L / 2 + 0.5 + i * 0.3, 0.452, z));
    const back = grp(at(box(0.16, 0.62, 0.76, C, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(cyl(0.11, 0.11, 0.8, Lt, 12, { outline: 0.02 }), 0.03, 0.64, 0, PI / 2));
    back.position.set(-L / 2 + 0.1, 0.36, 0); back.rotation.z = -0.32; g.add(back);
    g.add(at(cyl(0.1, 0.1, 0.66, Lt, 12, { outline: 0.02 }), -L / 2 + 0.38, 0.54, 0, PI / 2));
    g.userData.headRest = [-L / 2 + 0.45, 0.6, 0];
    return g;
  },


  // A thought bubble (pivot at its middle, faces +Z; turn it to the camera): a white cloud with a dark outline and a trail of three small circles
  // down to the lower left (toward the thinker), a one-wheeled wheelbarrow drawn inside filling half of it; o.w (1.3); o.popAt: it springs in
  pnBubble(o) {
    const w = o.w ?? 1.3, h = w * 0.85, g = grp(), k = grp(); g.add(k);
    const pl = canvasPlane(w, h, (c, W, H) => {
      c.clearRect(0, 0, W, H); c.lineWidth = W * 0.014; c.strokeStyle = '#1E2126'; c.fillStyle = '#FFFFFF';
      const cx = W * 0.56, cy = H * 0.4, rx = W * 0.4, ry = H * 0.32, bumps = 9;
      const path = () => { c.beginPath(); for (let i = 0; i < bumps; i++) { const a = i / bumps * TAU, x = cx + Math.cos(a) * rx, y = cy + Math.sin(a) * ry; c.moveTo(x + W * 0.1, y); c.arc(x, y, W * 0.1, 0, TAU); } c.moveTo(cx + rx, cy); c.ellipse(cx, cy, rx, ry, 0, 0, TAU); };
      path(); c.stroke(); path(); c.fill();
      for (const [x, y, rr] of [[0.2, 0.8, 0.045], [0.12, 0.89, 0.03], [0.07, 0.95, 0.02]]) { c.beginPath(); c.arc(W * x, H * y, W * rr, 0, TAU); c.fill(); c.stroke(); }
      drawBarrow(c, cx - W * 0.02, cy, W * 0.5);
    }, { res: 512, transparent: true, emissive: 0.35 });
    k.add(pl);
    g.userData.update = t => { const s = o.popAt == null ? 1 : popS(t, o.popAt, 0.28); k.visible = s > 0.01; k.scale.setScalar(Math.max(0.001, s)); k.position.y = 0.02 * Math.sin(t * 2); };
    g.userData.update(-1); return g;
  },

  // A small mountain spa (pivot at the pool's middle): a round thermal pool (o.r 1.7) in a stone rim, turquoise water that ripples, steam
  // puffs rising and fading, a wooden chalet with a snowy roof behind it at -Z (o.chalet false: none), two pine trees
  pnSpa(o) {
    const R = o.r ?? 1.7, g = grp();
    const rimG = new THREE.Mesh(new THREE.TorusGeometry(R + 0.12, 0.2, 6, 26), mat('#9C9A94')); rimG.rotation.x = PI / 2; rimG.position.y = 0.12; rimG.castShadow = rimG.receiveShadow = true; g.add(rimG);
    const water = new THREE.Mesh(new THREE.CircleGeometry(R, 32), mat('#4FC2C9', { noGrain: true })); water.rotation.x = -PI / 2; water.position.y = 0.16; g.add(water);
    const rings = []; for (let i = 0; i < 3; i++) { const m = noShadow(new THREE.Mesh(new THREE.RingGeometry(0.4, 0.44, 24), new THREE.MeshBasicMaterial({ color: '#BFF1F2', transparent: true, opacity: 0.6 }))); m.rotation.x = -PI / 2; m.position.y = 0.165; g.add(m); rings.push(m); }
    // (pass 2) steam as soft translucent wisps (additive curls drawn on a canvas), not spheres
    const wc = document.createElement('canvas'); wc.width = 64; wc.height = 128; { const x = wc.getContext('2d'); x.clearRect(0, 0, 64, 128); x.lineCap = 'round';
      for (let k2 = 0; k2 < 3; k2++) { x.strokeStyle = `rgba(255,255,255,${0.35 - k2 * 0.1})`; x.lineWidth = 18 - k2 * 5; x.beginPath(); x.moveTo(32, 124); x.bezierCurveTo(6, 90, 58, 60, 30, 30); x.bezierCurveTo(16, 14, 40, 6, 34, 2); x.stroke(); } }
    const wt = new THREE.CanvasTexture(wc); wt.colorSpace = THREE.SRGBColorSpace;
    const steam = []; for (let i = 0; i < 9; i++) { const m = noShadow(new THREE.Mesh(new THREE.PlaneGeometry(0.35, 0.7), new THREE.MeshBasicMaterial({ map: wt, transparent: true, opacity: 0.5, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide }))); g.add(m); steam.push(m); }
    if (o.chalet !== false) {
      const ch = grp(at(box(3.4, 2.2, 2.4, '#A8744A', { pivot: 'bottom', outline: 0.012 }), 0, 0, 0));
      for (let i = 0; i < 6; i++) ch.add(at(box(3.42, 0.04, 2.42, '#8C5E3A'), 0, 0.3 + i * 0.35, 0));
      for (const s of [-1, 1]) ch.add(at(box(1.95, 0.14, 2.9, '#F4F6F4', { outline: 0.01 }), s * 0.85, 2.62, 0, 0, 0, -s * 0.62));
      ch.add(at(box(0.7, 1.3, 0.04, '#5E3A22'), 0.6, 0.65, 1.21), at(box(0.6, 0.5, 0.04, '#FFE7A8', { emissive: '#6A5A30' }), -0.8, 1.3, 1.21));
      ch.position.set(o.chaletX ?? 0.5, 0, -(R + 2.4)); g.add(ch);
    }
    for (const [x, z, s] of (o.pines || [[-3.2, -2.6, 1.1], [3.4, -3.4, 1.3]])) { const p = grp(at(cyl(0.12, 0.14, 0.5, '#6A4A30', 6, { pivot: 'bottom' }), 0, 0, 0)); for (let i = 0; i < 3; i++) p.add(at(cyl(0.05, 0.9 - i * 0.22, 0.9, i % 2 ? '#2F6A48' : '#3A7A52', 7, { pivot: 'bottom', outline: 0.01 }), 0, 0.4 + i * 0.55, 0)); p.add(at(cyl(0.03, 0.5, 0.25, '#F4F6F4', 7, { pivot: 'bottom' }), 0, 1.75, 0)); p.scale.setScalar(s); p.position.set(x, 0, z); g.add(p); }
    g.userData.update = t => {
      rings.forEach((m, i) => { const u = ((t * 0.5 + i / 3) % 1); m.scale.setScalar(0.4 + u * 3.2); m.material.opacity = 0.55 * (1 - u); m.position.x = (o.ringAt || [0, 0])[0]; m.position.z = (o.ringAt || [0, 0])[1]; });
      steam.forEach((m, i) => { const per = 2.6, u = ((t + i * per / steam.length) % per) / per, a = hsh(i) * TAU, rr = R * 0.75 * Math.sqrt(hsh(i + 2)); m.position.set(Math.cos(a) * rr + 0.15 * Math.sin(t + i), 0.45 + u * 0.9, Math.sin(a) * rr * 0.8); m.scale.set(0.7 + u * 0.8, 0.6 + u * 0.9, 1); m.rotation.z = 0.3 * Math.sin(t * 0.8 + i); m.material.opacity = 0.55 * Math.sin(PI * u); });
    };
    g.userData.update(-1); return g;
  },

  // A snowy road climbing behind the spa (pivot at its foot; it runs up toward -X): a grey band o.len (16) long rising o.rise (3.5) m, snow banks
  // along both sides; userData.slope (rad)
  pnRamp(o) {
    const L = o.len ?? 16, H = o.rise ?? 3.5, w = o.w ?? 3.2, a = Math.atan2(H, L), g = grp();
    const road = at(box(Math.hypot(L, H), 0.1, w, '#8E9298', { outline: 0.004 }), -L / 2, H / 2, 0, 0, 0, -a); g.add(road);
    for (const s of [-1, 1]) g.add(at(box(Math.hypot(L, H), 0.35, 0.6, '#F4F6F4'), -L / 2, H / 2 + 0.1, s * (w / 2 + 0.3), 0, 0, -a));
    const fill = new THREE.Mesh(new THREE.BufferGeometry(), mat('#E6ECEB')); const v = new Float32Array([0, 0, -w / 2 - 0.6, -L, 0, -w / 2 - 0.6, -L, H, -w / 2 - 0.6, 0, 0, w / 2 + 0.6, -L, 0, w / 2 + 0.6, -L, H, w / 2 + 0.6]);
    fill.geometry.setAttribute('position', new THREE.BufferAttribute(v, 3)); fill.geometry.setIndex([0, 2, 1, 3, 4, 5, 1, 2, 5, 1, 5, 4, 0, 3, 5, 0, 5, 2]); fill.geometry.computeVertexNormals(); fill.material.side = THREE.DoubleSide; g.add(fill);
    g.userData.slope = a; return g;
  },

  // A giant syringe of air (pivot at the needle's tip, the syringe along -X from it): a clear barrel 0.75 long, a blunt steel needle, finger
  // flanges, a plunger rod and thumb disc; o.pushAt [[t0, t1], ...]: the plunger goes in over each span (out again 0.3 s after); userData.grip
  // the barrel's flanges (local) and userData.thumb the plunger's disc at rest
  pnSyringe(o) {
    const g = grp(), Lb = 0.75, rb = o.rb ?? 0.075, nd = 0.16;   // (pass 2) o.rb: a fatter barrel
    g.add(at(cyl(0.012 * rb / 0.075, 0.012 * rb / 0.075, nd, '#C9CED4', 6), -nd / 2, 0, 0, 0, 0, PI / 2), at(cyl(0.03, rb, 0.08, '#C9CED4', 10), -nd - 0.04, 0, 0, 0, 0, PI / 2));
    const barrel = new THREE.Mesh(new THREE.CylinderGeometry(rb, rb, Lb, 14, 1, true), new THREE.MeshLambertMaterial({ color: '#CDEFF8', transparent: true, opacity: 0.78, side: THREE.DoubleSide, depthWrite: false }));
    barrel.rotation.z = PI / 2; barrel.position.x = -nd - 0.08 - Lb / 2; addOutline(barrel, 0.03); g.add(barrel);   // (pass 1) a near-opaque pale barrel with an ink edge: at 0.45 it vanished on the asphalt
    for (let i = 1; i < 6; i++) g.add(at(box(0.006, 0.05, 0.004, '#5E6670'), -nd - 0.08 - i * Lb / 6, rb * 0.62, rb * 0.78));
    const xf = -nd - 0.08 - Lb; g.add(at(box(0.03, 0.34, 0.06, '#E8ECEE', { outline: 0.02 }), xf, 0, 0));
    const pl = grp(at(cyl(rb * 0.92, rb * 0.92, 0.05, '#2E3238', 12), 0, 0, 0, 0, 0, PI / 2), at(cyl(0.018, 0.018, Lb, '#E8ECEE', 6), -Lb / 2, 0, 0, 0, 0, PI / 2), at(cyl(0.1, 0.1, 0.03, '#E8ECEE', 12, { outline: 0.02 }), -Lb, 0, 0, 0, 0, PI / 2));
    g.add(pl);
    g.userData.grip = [xf, 0, 0]; g.userData.thumb = [xf - Lb + 0.05, 0, 0];
    g.userData.update = t => { let p = 0; for (const [a, b] of (o.pushAt || [])) { if (t >= a && t < b + 0.3) p = Math.max(p, t < b ? smooth((t - a) / (b - a)) : 1 - smooth((t - b) / 0.3)); } pl.position.x = -nd - 0.08 - Lb * 0.06 - Lb * 0.86 * (1 - p); };
    g.userData.update(-1); return g;
  },

  // A plain foot pump (pivot at the floor in its middle, front +Z): a dark grey footplate, a yellow pedal hinged at the back over a fat red-orange
  // cylinder, a round dial with a needle and no figure, a black hose coiling out to a brass nozzle; o.pumpAt [t, ...]: the pedal goes down and up
  pnPump(o) {
    // (pass 2) a plain foot pump read side on (long along X, seen from +Z): a dark base plate, a long red pedal hinged at the -X end and raised at
    // +X on a silver piston, a spring, a black hose from the hinge curling back to a brass nozzle; o.pumpAt [t, ...]: the pedal goes down and up
    const s = o.s ?? 1, g = grp(), k = grp(); g.add(k); k.scale.setScalar(s);
    k.add(at(box(0.44, 0.03, 0.14, '#33363C', { pivot: 'bottom', outline: 0.03 }), 0, 0, 0), at(cyl(0.025, 0.025, 0.16, '#33363C', 8), -0.2, 0.05, 0, PI / 2));
    const piston = at(cyl(0.035, 0.035, 0.12, '#C9CED4', 10, { outline: 0.03 }), 0.12, 0.09, 0); k.add(piston);
    const rod2 = at(cyl(0.014, 0.014, 0.1, '#8A9098', 6), 0.12, 0.16, 0); k.add(rod2);
    const ped = grp(at(box(0.42, 0.035, 0.12, '#D23A2E', { outline: 0.03 }), 0.21, 0, 0), at(box(0.12, 0.012, 0.1, '#1E2126'), 0.33, 0.022, 0)); ped.position.set(-0.2, 0.06, 0); k.add(ped);
    const curve = new THREE.CatmullRomCurve3([[-0.2, 0.05, 0.0], [-0.32, 0.06, 0.03], [-0.36, 0.2, 0.04], [-0.24, 0.3, 0.03], [-0.1, 0.24, 0.02]].map(p => new THREE.Vector3(...p)));
    k.add(new THREE.Mesh(new THREE.TubeGeometry(curve, 24, 0.014, 6), mat('#1E2126')), at(cyl(0.018, 0.018, 0.06, '#C9A23A', 8, { outline: 0.03 }), -0.08, 0.23, 0.02, 0, 0, -1.0));
    g.userData.update = t => { let p = 0; for (const a of (o.pumpAt || [])) { const u = t - a; if (u >= 0 && u < 0.35) p = Math.max(p, u < 0.12 ? u / 0.12 : 1 - (u - 0.12) / 0.23); }
      const a = 0.36 * (1 - 0.6 * p); ped.rotation.z = a; const yTip = 0.06 + Math.sin(a) * 0.32; rod2.position.y = (0.15 + yTip) / 2; rod2.scale.y = Math.max(0.2, (yTip - 0.15) / 0.1 + 1); };
    g.userData.update(-1); return g;
  },


  // A round sticker (pivot at its middle, faces +Z): a disc o.r (0.16) two thirds green and one third pale (a pie chart), a white border and a
  // dark outline, no figure; o.popAt: it slaps on with a spring and a spin
  pnPie(o) {
    const R = o.r ?? 0.16, g = grp(), k = grp(); g.add(k);
    const pl = canvasPlane(R * 2.2, R * 2.2, (c, W, H) => {
      c.clearRect(0, 0, W, H); const cx = W / 2, cy = H / 2, rr = W * 0.45;
      c.fillStyle = '#FFFFFF'; c.beginPath(); c.arc(cx, cy, rr, 0, TAU); c.fill(); c.lineWidth = W * 0.025; c.strokeStyle = '#1E2126'; c.stroke();
      c.fillStyle = '#E4E1D8'; c.beginPath(); c.arc(cx, cy, rr * 0.86, 0, TAU); c.fill();
      c.fillStyle = '#2FA35A'; c.beginPath(); c.moveTo(cx, cy); c.arc(cx, cy, rr * 0.86, -PI / 2, -PI / 2 + TAU * 0.65); c.closePath(); c.fill();
      c.strokeStyle = '#FFFFFF'; c.lineWidth = W * 0.02; c.beginPath(); c.moveTo(cx, cy); c.lineTo(cx, cy - rr * 0.86); c.moveTo(cx, cy); c.lineTo(cx + Math.cos(-PI / 2 + TAU * 0.65) * rr * 0.86, cy + Math.sin(-PI / 2 + TAU * 0.65) * rr * 0.86); c.stroke();
    }, { res: 256, transparent: true, emissive: 0.25 });
    k.add(pl);
    g.userData.update = t => { const s = o.popAt == null ? 1 : popS(t, o.popAt, 0.25); k.visible = s > 0.01; k.scale.setScalar(Math.max(0.001, s)); k.rotation.z = o.popAt == null ? 0 : -0.6 * (1 - clamp01((t - o.popAt) / 0.25)); };
    g.userData.update(-1); return g;
  },

  // A chart board on a stand (pivot at the floor in its middle, front +Z): a white board o.w (1.3) x o.h (0.95) whose bottom is at 0.95 m, two
  // grey axes and one thick red curve climbing steeply to the top right, no figure and no word; o.grow [t0, t1]: the curve draws itself from the
  // left (a white cover slides off it); the two legs stay behind and below the board
  pnChart(o) {
    const w = o.w ?? 1.3, h = o.h ?? 0.95, y0 = o.y0 ?? 0.95, g = grp();
    g.add(at(box(w + 0.08, h + 0.08, 0.04, '#3A3D44', { outline: 0.01 }), 0, y0 + h / 2, -0.03));
    const pl = canvasPlane(w, h, (c, W, H) => {
      c.fillStyle = '#FBFAF4'; c.fillRect(0, 0, W, H); c.strokeStyle = '#8A9098'; c.lineWidth = W * 0.012; c.lineCap = 'round';
      c.beginPath(); c.moveTo(W * 0.08, H * 0.08); c.lineTo(W * 0.08, H * 0.9); c.lineTo(W * 0.94, H * 0.9); c.stroke();
      c.strokeStyle = '#E3E3DC'; c.lineWidth = W * 0.004; for (let i = 1; i < 4; i++) { c.beginPath(); c.moveTo(W * 0.08, H * (0.9 - i * 0.2)); c.lineTo(W * 0.94, H * (0.9 - i * 0.2)); c.stroke(); }
      c.strokeStyle = '#D8262E'; c.lineWidth = W * 0.035; c.lineJoin = 'round'; c.beginPath();
      for (let i = 0; i <= 40; i++) { const u = i / 40, x = W * (0.1 + 0.8 * u), y = H * (0.86 - 0.74 * Math.pow(u, 2.6)); i ? c.lineTo(x, y) : c.moveTo(x, y); } c.stroke();
      c.fillStyle = '#D8262E'; c.beginPath(); c.moveTo(W * 0.93, H * 0.06); c.lineTo(W * 0.86, H * 0.16); c.lineTo(W * 0.95, H * 0.17); c.closePath(); c.fill();
    }, { res: 512, emissive: 0.15 });
    g.add(at(pl, 0, y0 + h / 2, 0));
    const cover = at(box(1, h * 0.86, 0.01, '#FBFAF4', { noGrain: true }), 0, y0 + h * 0.5, 0.006); g.add(cover);
    for (const s of [-1, 1]) g.add(rod([s * w * 0.32, 0, 0.12], [s * w * 0.32, y0 + 0.1, -0.06], 0.025, '#5E656D'));
    g.add(rod([0, 0, -0.45], [0, y0 + h * 0.5, -0.07], 0.022, '#5E656D'));
    g.userData.update = t => { const u = o.grow ? smooth((t - o.grow[0]) / (o.grow[1] - o.grow[0])) : 1, cw = w * 0.84 * (1 - u); cover.visible = cw > 0.005; cover.scale.x = Math.max(0.001, cw); cover.position.x = w * 0.46 - cw / 2; };
    g.userData.update(-1); return g;
  },

  // A white plinth with the pump under a glass dome (pivot at the floor in its middle): a white column 1.0 m tall, a foot pump on its top, a clear
  // dome over it with a dark base ring and a knob; o.pumpS (1.4) the pump's size
  pnPlinth(o) {
    const g = grp(at(box(0.8, 1.0, 0.8, '#F2F0EA', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(0.88, 0.06, 0.88, '#DCD8CE', { outline: 0.008 }), 0, 1.0, 0), at(box(0.88, 0.08, 0.88, '#DCD8CE'), 0, 0.04, 0));   // (pass 2) wider, for the side-on pump
    const pump = PNEU_PROPS.pnPump({ s: o.pumpS ?? 1.2 }); pump.position.y = 1.03; g.add(pump);
    const gm = new THREE.MeshLambertMaterial({ color: '#E2F2F4', transparent: true, opacity: 0.28, side: THREE.DoubleSide, depthWrite: false });
    const wall = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.38, 0.4, 20, 1, true), gm); wall.position.y = 1.03 + 0.2; g.add(wall);
    const cap = new THREE.Mesh(new THREE.SphereGeometry(0.38, 20, 8, 0, TAU, 0, PI / 2), gm); cap.position.y = 1.43; cap.scale.y = 0.6; g.add(cap);
    g.add(at(cyl(0.39, 0.39, 0.03, '#2E3238', 20), 0, 1.045, 0), at(sphere(0.03, '#2E3238', 1), 0, 1.67, 0));
    const hl = noShadow(at(box(0.02, 0.3, 0.005, '#FFFFFF', { opacity: 0.6, noGrain: true }), -0.2, 1.28, 0.32, 0, -0.5, 0)); g.add(hl);
    return g;
  },

  // A pharmacy counter (pivot at the floor in its middle, front +Z): a pale wood counter 2.4 wide, 1.0 tall, and behind it a wall of shelves with
  // plain coloured boxes (no word, no cross)
  pnCounter(o) {
    const w = o.w ?? 2.4, g = grp(at(box(w, 0.96, 0.6, '#E7D8BC', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(box(w + 0.1, 0.05, 0.7, '#F4F1EA', { outline: 0.006 }), 0, 0.96, 0));
    g.add(at(box(w, 0.12, 0.02, '#4FA36A'), 0, 0.75, 0.305));
    const sz = o.shelfZ ?? -1.4, sw = o.shelfW ?? 4.2, cols = ['#E8F0F2', '#BFD8EA', '#F2D6A2', '#D9E8C8', '#F4C7C0', '#FFFFFF', '#C9D2E8'];
    g.add(at(box(sw, 2.4, 0.36, '#F4F1EA', { pivot: 'bottom', outline: 0.006 }), 0, 0, sz));
    for (let r = 0; r < 4; r++) { g.add(at(box(sw, 0.03, 0.4, '#D8D2C4'), 0, 0.5 + r * 0.5, sz + 0.02)); for (let i = 0; i < 16; i++) { const bw = 0.12 + hsh(r * 20 + i) * 0.1, bh = 0.18 + hsh(r * 30 + i) * 0.16; g.add(at(box(bw, bh, 0.16, cols[(r * 5 + i) % cols.length], { pivot: 'bottom' }), -sw / 2 + 0.2 + i * (sw - 0.4) / 15, 0.515 + r * 0.5, sz + 0.12)); } }
    return g;
  },

  // A surgical mask (attach to the 'head' joint): a pale blue pad over the lower face with two white ear loops; o.y / o.z its place (local)
  pnMask(o) {
    const w = o.w ?? 0.34, g = grp(at(box(w, o.h ?? 0.13, 0.03, '#BFE0EE', { outline: 0.03 }), 0, o.y ?? 0.08, o.z ?? 0.17));
    for (const s of [-1, 1]) g.add(at(box(0.012, 0.012, 0.16, '#FFFFFF'), s * (w / 2 + 0.005), (o.y ?? 0.08) + 0.04, (o.z ?? 0.17) - 0.08));
    return g;
  },
};
