// « La tondeuse » (story 70): this man started his lawnmower and it never stopped: the neighbour's garden, the football stadium, the forest in a
// straight line, circles in the wheat, the gendarmes on foot, the palace lawn, the whole country in three weeks; out of fuel right in front of his
// house; his own garden still not mowed. Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a
// pure function of the shot time.
import * as THREE from 'three';
import { box, cyl } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const hash = n => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const L = c => new THREE.MeshLambertMaterial({ color: c });
const LO = (c, k) => new THREE.MeshLambertMaterial({ color: c, polygonOffset: true, polygonOffsetFactor: -k, polygonOffsetUnits: -4 * k });   // (review 1 of 70) a ground overlay that never sinks into the field under it, however far the camera
const ball = (r, c, seg = 10) => new THREE.Mesh(new THREE.SphereGeometry(r, seg, Math.max(6, seg - 2)), typeof c === 'string' ? L(c) : c);
const UP = new THREE.Vector3(0, 1, 0);

export const TONDEUSE_PROPS = {
  // A field of grass (pivot at its middle on the ground, o.w across x by o.d along z): o.n blades (2400) about o.h high, cut down to o.short of their
  // height where a mower passes along o.path [[t, x, z], ...] (in the field's frame) within o.width of it, at the moment it passes, the stubble turning
  // o.cutCol and a pale strip appearing under it (o.stripCols: alternating colours, one per path segment: a striped lawn); o.cols: the blade colours
  // (golds for wheat), o.ground: the soil between them
  mowField(o) {
    const W = o.w ?? 8, D = o.d ?? 6, H = o.h ?? 0.5, n = o.n ?? 2400, path = o.path || [], half = (o.width ?? 0.55) / 2, sh = o.short ?? 0.12, g = grp();
    const cols = (o.cols || ['#5E9A4A', '#6FB05A', '#4E8A3E', '#7FBF5E']).map(c => new THREE.Color(c)), cutCol = new THREE.Color(o.cutCol || '#9CCB6A');
    if (o.ground !== 'none') g.add(at(new THREE.Mesh(new THREE.PlaneGeometry(W, D).rotateX(-PI / 2), LO(o.ground || '#4E7F3A', 1)), 0, 0.01, 0));   // o.ground 'none': only the mown bands, over a ground of its own
    const geo = new THREE.ConeGeometry(o.bw ?? 0.022, 1, 3); geo.translate(0, 0.5, 0);
    const im = new THREE.InstancedMesh(geo, new THREE.MeshLambertMaterial({ color: '#FFFFFF' }), n); im.frustumCulled = false; im.castShadow = false; im.receiveShadow = true; g.add(im);
    const dm = new THREE.Object3D(), B = [];
    for (let i = 0; i < n; i++) { const x = (hash(i * 3 + 1) - 0.5) * W, z = (hash(i * 3 + 2) - 0.5) * D; let tc = Infinity;
      for (let k = 1; k < path.length; k++) { const [t0, x0, z0] = path[k - 1], [t1, x1, z1] = path[k], dx = x1 - x0, dz = z1 - z0, l2 = dx * dx + dz * dz || 1e-9;
        const u = clamp01(((x - x0) * dx + (z - z0) * dz) / l2); if (Math.hypot(x - x0 - dx * u, z - z0 - dz * u) < half) tc = Math.min(tc, t0 + (t1 - t0) * u); }
      B.push({ x, z, h: H * (0.75 + 0.5 * hash(i * 3 + 3)), lean: (hash(i + 7) - 0.5) * 0.4, ry: hash(i + 9) * TAU, tc, col: cols[i % cols.length], was: null }); }
    const strips = [];
    for (let k = 1; k < path.length; k++) { const [t0, x0, z0] = path[k - 1], [t1, x1, z1] = path[k], len = Math.hypot(x1 - x0, z1 - z0); if (len < 1e-3) continue;
      const m = new THREE.Mesh(new THREE.PlaneGeometry(half * 2, 1).rotateX(-PI / 2).translate(0, 0, 0.5), LO(o.stripCols ? o.stripCols[(k - 1) % o.stripCols.length] : (o.stripCol || '#8DC05E'), 2)); m.position.set(x0, 0.02, z0); m.rotation.y = Math.atan2(x1 - x0, z1 - z0); m.visible = false; g.add(m); strips.push({ m, t0, t1, len }); }
    g.userData.update = t => {
      for (let i = 0; i < n; i++) { const b = B[i], cut = t >= b.tc; dm.position.set(b.x, 0, b.z); dm.rotation.set(b.lean, b.ry, 0); dm.scale.set(1, b.h * (cut ? sh : 1), 1); dm.updateMatrix(); im.setMatrixAt(i, dm.matrix);
        if (cut !== b.was) { im.setColorAt(i, cut ? cutCol : b.col); b.was = cut; } }
      im.instanceMatrix.needsUpdate = true; if (im.instanceColor) im.instanceColor.needsUpdate = true;
      for (const s of strips) { const u = s.t1 > s.t0 ? clamp01((t - s.t0) / (s.t1 - s.t0)) : (t >= s.t0 ? 1 : 0); s.m.visible = u > 0; s.m.scale.set(1, 1, Math.max(0.001, u * s.len)); }
    };
    g.userData.update(0); return g;
  },

  // A push mower that runs by itself (pivot at the floor in its middle, front +Z, handle back -Z): a red deck, a black engine with a chrome cap, a side
  // chute, four wheels, the handle with its grips and the starter cord's handle. While it runs (o.runAt..o.stopAt, lists allowed) it trembles, clippings
  // spray out of the chute on the right and grey exhaust puffs rise; o.cough [t, ...]: a jolt and a black puff; o.sputter [t0, t1]: it splutters (jerks,
  // black puffs, no spray); o.slumpAt: it sags on its wheels and sighs one last pale puff; o.bowAt: it dips its nose like a bow; (review 1 of 70) o.startAt:
  // a squash then a stretch forward as it catches; o.dead: deflated flat, the handle on the ground, no smoke; o.speedLines: white streaks behind it
  mowerLive(o) {
    const g = grp(), body = grp(), red = o.color || '#C8322A';
    body.add(at(box(0.52, 0.16, 0.62, red, { outline: 0.008 }), 0, 0.2, 0), at(box(0.42, 0.04, 0.5, '#9A2620'), 0, 0.29, 0), at(box(0.12, 0.1, 0.22, '#26272B', { outline: 0.006 }), 0.31, 0.2, 0.0));
    body.add(at(cyl(0.12, 0.14, 0.16, '#26272B', 10, { outline: 0.006 }), 0, 0.37, -0.04), at(cyl(0.07, 0.07, 0.04, '#C9D1D8', 10), 0, 0.47, -0.04), at(box(0.06, 0.05, 0.08, red), 0.1, 0.4, 0.06));
    for (const x of [-0.28, 0.28]) for (const z of [-0.24, 0.24]) { const w = at(cyl(0.09, 0.09, 0.05, '#18191C', 10), x, 0.09, z, 0, 0, PI / 2); w.add(at(cyl(0.05, 0.05, 0.052, '#C9D1D8', 8), 0, 0, 0)); body.add(w); }
    const rodM = L('#3A3D44'), rod = (a, b, r) => { const A = new THREE.Vector3(...a), Bv = new THREE.Vector3(...b), dd = Bv.clone().sub(A), m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, dd.length(), 6), rodM);
      m.position.copy(A).add(Bv).multiplyScalar(0.5); m.quaternion.setFromUnitVectors(UP, dd.normalize()); m.castShadow = true; return m; };
    const hdl = grp(); hdl.position.set(0, 0.26, -0.28); body.add(hdl);   // (review 1 of 70) the handle hinges at the back of the deck: it curls in the bow, it falls when the mower dies
    hdl.add(rod([-0.2, 0, 0], [-0.23, 0.72, -0.57], 0.016), rod([0.2, 0, 0], [0.23, 0.72, -0.57], 0.016), rod([-0.26, 0.72, -0.57], [0.26, 0.72, -0.57], 0.02));
    for (const sd of [-1, 1]) hdl.add(at(cyl(0.026, 0.026, 0.12, '#18191C', 8), sd * 0.2, 0.72, -0.57, 0, 0, PI / 2));
    hdl.add(at(box(0.09, 0.03, 0.03, '#18191C'), 0.12, 0.6, -0.47));
    const lines = o.speedLines ? [0, 1, 2].map(i => { const m = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.03, 1), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.8 })); m.position.set(-0.18 + 0.18 * i, 0.16 + 0.12 * (i % 2), -0.9); g.add(m); return m; }) : [];
    g.add(body);
    const N = o.n ?? 80, clip = new THREE.InstancedMesh(new THREE.BoxGeometry(0.05, 0.012, 0.025), L(o.clipColor || '#6DBE4E'), N), dm = new THREE.Object3D(), base = [];
    for (let i = 0; i < N; i++) base.push([hash(i + 1), hash(i + 2) * TAU, 0.8 + hash(i + 3) * 0.9, (hash(i + 4) - 0.5) * 0.7]); clip.frustumCulled = false; g.add(clip);
    const PN = 8, puffs = []; for (let i = 0; i < PN; i++) { const p = ball(0.06, new THREE.MeshLambertMaterial({ color: '#C8C8C2', transparent: true, opacity: 0.9 }), 8); p.visible = false; p.castShadow = false; g.add(p); puffs.push(p); }
    const runs = t => { const ra = [].concat(o.runAt ?? 0), sa = [].concat(o.stopAt ?? []); return ra.some((a, i) => t >= a && t < (sa[i] ?? Infinity)); };
    g.userData.update = t => {
      const on = runs(t), sp = o.sputter, sput = !!sp && t >= sp[0] && t < sp[1], cs = [].concat(o.cough ?? []).filter(c => t >= c), lc = cs.length ? cs[cs.length - 1] : null, cu = lc == null ? 9 : t - lc;
      // (review 1 of 70: a rigid prop) it acts: each cough squashes it then springs it up, bigger each time; the start stretches it forward; the bow is deep and
      // held, the handle curling like a spine; dying, it deflates flat and its handle drops to the ground (o.dead: already so)
      let jx = 0, jy = 0, rx = 0, sy = 1, sz = 1, hr = 0;
      const dead = o.dead || (o.slumpAt != null && t >= o.slumpAt + 0.4), bu = o.bowAt == null ? -1 : t - o.bowAt, bowing = bu > 0 && bu < 0.9;
      if (on && !dead) { jx = 0.007 * Math.sin(t * 90); jy = 0.005 * Math.abs(Math.sin(t * 70)); }
      if (sput) { jy += 0.03 * Math.max(0, Math.sin(t * 22)); rx -= 0.12 * Math.max(0, Math.sin(t * 17)); }
      if (cu < 0.4) { const a = 0.6 + 0.2 * Math.min(2, cs.length - 1), sq_ = cu < 0.1 ? Math.sin(cu / 0.1 * PI / 2) : Math.max(0, 1 - (cu - 0.1) / 0.12);
        sy *= 1 - 0.28 * a * sq_ + (cu > 0.1 && cu < 0.4 ? 0.16 * a * Math.sin((cu - 0.1) / 0.3 * PI) : 0); jy += cu > 0.1 ? 0.07 * a * Math.sin(Math.min(1, (cu - 0.1) / 0.3) * PI) : 0; rx -= 0.2 * a * Math.sin(Math.min(1, cu / 0.3) * PI); }
      if (o.startAt != null) { const u = t - o.startAt; if (u > -0.12 && u < 0) sy *= 1 - 0.18 * (1 + u / 0.12); if (u >= 0 && u < 0.45) { const e = Math.exp(-7 * u); sz *= 1 + 0.32 * e; sy *= 1 - 0.12 * e; rx -= 0.25 * e; } }
      if (bowing) { const d = bu < 0.18 ? bu / 0.18 : bu < 0.5 ? 1 : 1 - (bu - 0.5) / 0.4, e = d * d * (3 - 2 * d); rx += 0.62 * e; hr += 0.4 * e; }
      if (o.slumpAt != null && t >= o.slumpAt && !o.dead) { const u = clamp01((t - o.slumpAt) / 0.35), e = u * u * (3 - 2 * u); sy *= 1 - 0.38 * e + 0.05 * Math.sin(u * PI); hr -= 1.05 * e + (u >= 1 ? 0.04 * Math.exp(-6 * (t - o.slumpAt - 0.35)) * Math.sin((t - o.slumpAt - 0.35) * 20) : 0); }
      if (o.dead) { sy *= 0.62; hr -= 1.05; }
      body.position.set(jx, jy, 0); body.rotation.x = rx; body.scale.set(1 + (1 - sy) * 0.35, sy, sz); hdl.rotation.x = hr;
      lines.forEach((m, i) => { m.visible = on && !dead; m.scale.z = 0.6 + 0.5 * Math.abs(Math.sin(t * 9 + i)); m.position.z = -0.6 - m.scale.z / 2; });
      const spray = on && !sput && !dead && o.spray !== false;
      base.forEach(([ph, rot, v, s2], i) => { const q = ((t * 1.7) + ph) % 1; if (!spray) dm.scale.setScalar(0.0001); else { dm.scale.setScalar(1); dm.position.set(0.38 + q * v * 0.9, 0.22 + q * 0.95 - q * q * 1.1, s2 * q * 0.9); dm.rotation.set(t * 9 + rot, rot, t * 7); } dm.updateMatrix(); clip.setMatrixAt(i, dm.matrix); });
      clip.instanceMatrix.needsUpdate = true;
      const slumped = o.slumpAt != null && t >= o.slumpAt;
      puffs.forEach((p, i) => { let u, black = false;
        if (o.dead || bowing) { p.visible = false; return; }   // no smoke in the bow (it hid the medal) nor from a dead mower
        if (slumped) { u = (t - o.slumpAt) / 0.9; if (i > 0 || u > 1) { p.visible = false; return; } }
        else if (sput) { u = (t * 2.6 + i / PN) % 1; black = true; }
        else if (lc != null && cu < 0.6 && i < 3) { u = cu / 0.6 + i * 0.1; black = true; }
        else if (on) u = (t * 1.3 + i / PN) % 1;
        else { p.visible = false; return; }
        p.visible = u >= 0 && u < 1; p.material.color.set(black ? '#2A2A2E' : '#D4D4CE'); p.material.opacity = 0.9 * (1 - u);
        p.position.set(0.02 + 0.1 * Math.sin(i * 2.1) * u, 0.5 + 0.7 * u, -0.06 - 0.25 * u); p.scale.setScalar((black ? 1.7 : 1) * (0.6 + 1.6 * u)); });
    };
    g.userData.update(0); g.userData.grip = [0, 0.98, -0.85]; return g;
  },

  // A low-poly tree that falls (pivot at the foot of its trunk): a brown trunk and three stacked green cones; at o.fallAt it topples toward o.dir (radians
  // about y, 0 = +Z) in 0.42 s with a little bounce on the ground, leaving its stump; o.s its size
  fallTree(o) {
    const s = o.s ?? 1, g = grp(), pivot = grp(), tree = grp(), green = o.color || ['#3F7A3A', '#4B8A42', '#356B31'][Math.floor(hash(o.seed ?? 1) * 3)];
    g.add(at(cyl(0.16 * s, 0.2 * s, 0.25 * s, '#7A5230', 7, { pivot: 'bottom' }), 0, 0, 0));
    tree.add(at(cyl(0.12 * s, 0.16 * s, 1.4 * s, '#7A5230', 7, { pivot: 'bottom' }), 0, 0, 0));
    [[1.05, 1.3], [1.75, 1.05], [2.35, 0.75]].forEach(([y, r]) => { const c = new THREE.Mesh(new THREE.ConeGeometry(r * s, 1.2 * s, 7), L(green)); c.position.y = y * s; c.castShadow = true; tree.add(c); });
    pivot.position.y = 0.25 * s; pivot.rotation.y = o.dir ?? 0; pivot.add(tree); g.add(pivot);
    g.userData.update = t => { const u = o.fallAt == null ? -1 : t - o.fallAt; let a = 0;
      if (u > 0) { const k = Math.min(1, u / 0.42); a = (PI / 2 - 0.06) * k * k; if (u > 0.42) a = PI / 2 - 0.06 - 0.09 * Math.exp(-(u - 0.42) * 7) * Math.abs(Math.sin((u - 0.42) * 24)); }
      tree.rotation.x = a; };
    g.userData.update(0); return g;
  },

  // A football pitch (pivot at its centre, o.w across x by o.d along z): green, white lines, two goals; o.passes [[t0, t1], ...]: mown stripe i (o.n across,
  // light and dark in turn) grows along the pitch between t0 and t1 (from the near end for even i, the far end for odd)
  stripePitch(o) {
    const W = o.w ?? 34, D = o.d ?? 52, n = o.n ?? 8, g = grp();
    g.add(at(new THREE.Mesh(new THREE.PlaneGeometry(W + 6, D + 6).rotateX(-PI / 2), LO(o.base || '#4F7F34', 1)), 0, 0.01, 0));
    const lines = canvasPlane(W, D, (c, Wc, Hc) => { c.clearRect(0, 0, Wc, Hc); c.strokeStyle = '#F4F4F0'; c.lineWidth = Wc * 0.007; const sx = Wc / W, sz = Hc / D;
      c.strokeRect(Wc * 0.015, Hc * 0.01, Wc * 0.97, Hc * 0.98); c.beginPath(); c.moveTo(Wc * 0.015, Hc / 2); c.lineTo(Wc * 0.985, Hc / 2); c.stroke(); c.beginPath(); c.arc(Wc / 2, Hc / 2, 6 * sx, 0, TAU); c.stroke();
      c.strokeRect(Wc / 2 - 12 * sx, Hc * 0.01, 24 * sx, 10 * sz); c.strokeRect(Wc / 2 - 12 * sx, Hc * 0.99 - 10 * sz, 24 * sx, 10 * sz); }, { res: 512, transparent: true });
    lines.rotation.x = -PI / 2; lines.position.y = 0.03; Object.assign(lines.material, { polygonOffset: true, polygonOffsetFactor: -3, polygonOffsetUnits: -12 }); g.add(lines);
    for (const e of [-1, 1]) { const goal = grp(at(box(0.14, 2.44, 0.14, '#F4F4F0', { outline: 0.006 }), -3.66, 1.22, 0), at(box(0.14, 2.44, 0.14, '#F4F4F0', { outline: 0.006 }), 3.66, 1.22, 0), at(box(7.46, 0.14, 0.14, '#F4F4F0', { outline: 0.006 }), 0, 2.44, 0));
      goal.position.z = e * (D / 2 - 0.25); g.add(goal); }
    const sw = W / n, stripes = [];
    for (let i = 0; i < n; i++) { const m = new THREE.Mesh(new THREE.PlaneGeometry(sw, 1).rotateX(-PI / 2), LO(i % 2 ? (o.light || '#A6E07A') : (o.dark || '#5E9F3E'), 2)); m.position.set(-W / 2 + (i + 0.5) * sw, 0.02, 0); m.visible = false; g.add(m); stripes.push(m); }
    const P_ = o.passes || [];
    g.userData.update = t => { stripes.forEach((m, i) => { const p = P_[i]; if (!p) { m.visible = false; return; } const u = clamp01((t - p[0]) / Math.max(0.01, p[1] - p[0]));
      m.visible = u > 0; m.scale.z = Math.max(0.001, u * D); m.position.z = (i % 2 ? -1 : 1) * (D / 2) * (1 - u); }); };
    g.userData.update(0); return g;
  },

  // Stadium stands (pivot at the foot of the front row in the middle, the rows rising toward -Z, facing +Z): o.rows grey steps o.l long, a crowd of small
  // coloured figures (a head on a body) on them that bob
  bleachers(o) {
    const l = o.l ?? 30, rows = o.rows ?? 6, g = grp(), cols = ['#E0413A', '#2F62B5', '#F2C230', '#F4F4F0', '#3A9B5C', '#C255C8', '#F28C28'], fans = [];
    for (let r = 0; r < rows; r++) g.add(at(box(l, 0.5, 0.9, r % 2 ? '#A9ADB3' : '#9AA0A6', { outline: 0.006 }), 0, 0.25 + r * 0.5, -0.45 - r * 0.9));
    for (let r = 0; r < rows; r++) for (let i = 0; i < Math.floor(l / 0.55); i++) { if (hash(r * 97 + i) < 0.18) continue; const f = grp(at(box(0.3, 0.42, 0.22, cols[(r * 7 + i) % 7]), 0, 0.21, 0), at(ball(0.11, '#E8B98F', 6), 0, 0.53, 0));
      f.position.set(-l / 2 + 0.3 + i * 0.55 + (hash(i + r) - 0.5) * 0.1, 0.5 + r * 0.5, -0.45 - r * 0.9); g.add(f); fans.push({ f, ph: hash(r * 13 + i) * TAU, y: 0.5 + r * 0.5 }); }
    g.userData.update = t => { fans.forEach(({ f, ph, y }) => { f.position.y = y + (o.cheer ? 0.08 * Math.max(0, Math.sin(t * 9 + ph)) : 0.01 * Math.sin(t * 2 + ph)); }); };
    g.userData.update(0); return g;
  },

  // A garden gnome (pivot at its feet, front +Z): a red pointed hat, a white beard, a blue coat, a round pink face with two dots; o.trimAt: the tip of the
  // hat is sliced off and flies away, tumbling; o.popAt: it pops up out of the grass with an overshoot; o.s its size (1: 60 cm)
  gnome(o) {
    const s = o.s ?? 1, g = grp(), body = grp();
    body.add(at(new THREE.Mesh(new THREE.CylinderGeometry(0.1 * s, 0.13 * s, 0.22 * s, 8), L('#2F62B5')), 0, 0.11 * s, 0), at(ball(0.035 * s, '#3A2A1A', 6), -0.05 * s, 0.02 * s, 0.05 * s), at(ball(0.035 * s, '#3A2A1A', 6), 0.05 * s, 0.02 * s, 0.05 * s));
    body.add(at(ball(0.085 * s, '#F2C2A0', 10), 0, 0.3 * s, 0.01 * s), at(new THREE.Mesh(new THREE.ConeGeometry(0.075 * s, 0.14 * s, 8), L('#F4F4F0')), 0, 0.23 * s, 0.06 * s, PI, 0, 0));
    body.add(at(ball(0.012 * s, '#111111', 6), -0.03 * s, 0.32 * s, 0.08 * s), at(ball(0.012 * s, '#111111', 6), 0.03 * s, 0.32 * s, 0.08 * s), at(ball(0.018 * s, '#E0786A', 6), 0, 0.29 * s, 0.09 * s));
    const tip = new THREE.Mesh(new THREE.ConeGeometry(0.045 * s, 0.14 * s, 8), L('#D8342A')); tip.castShadow = true;
    body.add(at(new THREE.Mesh(new THREE.CylinderGeometry(0.045 * s, 0.09 * s, 0.1 * s, 8), L('#D8342A')), 0, 0.42 * s, 0), tip);
    g.add(body);
    g.userData.update = t => {
      if (o.popAt != null) { const u = t - o.popAt; body.visible = u >= -0.02; body.position.y = u < 0 ? -0.6 * s : u < 0.15 ? -0.6 * s * (1 - u / 0.15) : 0.06 * s * Math.exp(-(u - 0.15) * 10) * Math.sin((u - 0.15) * 30); }
      const v = o.trimAt == null ? -1 : t - o.trimAt;
      if (v > 0) { tip.position.set(0.35 * s * v, 0.54 * s + 1.6 * v - 4.9 * v * v, 0.1 * v); tip.rotation.set(v * 12, 0, v * 8); tip.visible = v < 0.9; } else { tip.position.set(0, 0.54 * s, 0); tip.rotation.set(0, 0, 0); tip.visible = true; } };
    g.userData.update(0); return g;
  },

  // A garden hedge (pivot at its foot in the middle, its length along x: o.l long, o.h high, o.d thick): leafy green blocks; at o.holeAt a mower-sized hole
  // o.holeW x o.holeH bursts through it at o.holeX, the leaves flying out toward o.burstDir (+1: +Z, -1: -Z)
  hedgeWall(o) {
    const l = o.l ?? 6, h = o.h ?? 1.4, d = o.d ?? 0.6, hx = o.holeX ?? 0, hw = o.holeW ?? 0.8, hh = o.holeH ?? 0.75, bd = o.burstDir ?? 1, g = grp(), A = '#3E7A34', B2 = '#4C8C3E';
    const left = hx - hw / 2 + l / 2, right = l / 2 - hx - hw / 2;
    g.add(at(box(left, h, d, A, { outline: 0.008 }), -l / 2 + left / 2, h / 2, 0), at(box(right, h, d, A, { outline: 0.008 }), hx + hw / 2 + right / 2, h / 2, 0), at(box(hw, h - hh, d, A, { outline: 0.008 }), hx, hh + (h - hh) / 2, 0));
    const plug = at(box(hw, hh, d, B2, { outline: 0.008 }), hx, hh / 2, 0); g.add(plug);
    for (let i = 0; i < Math.floor(l / 0.35); i++) g.add(at(ball(0.2, i % 2 ? A : B2, 6), -l / 2 + 0.2 + i * 0.35, h, (hash(i) - 0.5) * 0.15));
    const leaves = []; for (let i = 0; i < 30; i++) { const m = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.014, 0.045), L(i % 2 ? A : '#6AAE4E')); m.visible = false; g.add(m); leaves.push({ m, v: [(hash(i + 1) - 0.5) * 2.0, 1.2 + hash(i + 2) * 1.6, 0.6 + hash(i + 3) * 1.4] }); }
    g.userData.update = t => { const u = o.holeAt == null ? -1 : t - o.holeAt; plug.visible = u < 0;
      leaves.forEach(({ m, v }, i) => { const on = u >= 0 && u < 1.0; m.visible = on; if (!on) return; m.position.set(hx + v[0] * u * 0.5, Math.max(0.01, hh * 0.5 + v[1] * u - 4.9 * u * u), bd * v[2] * u); m.rotation.set(u * 10 + i, u * 7, i); }); };
    g.userData.update(0); return g;
  },

  // A little garage (pivot at the foot of its door in the middle, the door +Z): walls o.w x o.d x o.h, a flat grey roof, an up-and-over door folded up under
  // the ceiling until o.closeAt, then swung down shut in 0.25 s with a bounce
  garageShed(o) {
    const W = o.w ?? 2.6, D = o.d ?? 3.2, H = o.h ?? 2.3, g = grp(), wall = o.color || '#E9DFC9', Hd = H - 0.25;
    g.add(at(box(0.15, H, D, wall, { outline: 0.006 }), -W / 2, H / 2, -D / 2), at(box(0.15, H, D, wall, { outline: 0.006 }), W / 2, H / 2, -D / 2), at(box(W + 0.15, H, 0.15, wall), 0, H / 2, -D),
      at(box(W + 0.4, 0.15, D + 0.3, '#8E979F', { outline: 0.006 }), 0, H + 0.07, -D / 2), at(box(W - 0.15, 0.25, 0.15, wall), 0, H - 0.12, 0));
    g.add(at(new THREE.Mesh(new THREE.PlaneGeometry(W - 0.15, D).rotateX(-PI / 2), L('#7E7C78')), 0, 0.006, -D / 2));
    const hinge = grp(); hinge.position.set(0, Hd, 0.03); g.add(hinge);
    const door = at(box(W - 0.2, Hd, 0.05, o.door || '#F4F4F0', { outline: 0.006 }), 0, -Hd / 2, 0); hinge.add(door);
    for (let i = 1; i < 5; i++) door.add(at(box(W - 0.24, 0.02, 0.06, '#C9C7C0'), 0, -Hd / 2 + i * Hd / 5, 0));
    g.userData.update = t => { const u = o.closeAt == null ? -1 : t - o.closeAt; let a;
      if (u < 0) a = PI / 2; else if (u < 0.25) { const k = u / 0.25; a = PI / 2 * (1 - k * k); } else a = -0.06 * Math.exp(-(u - 0.25) * 10) * Math.sin((u - 0.25) * 40);
      hinge.rotation.x = a; };
    g.userData.update(0); return g;
  },
};
