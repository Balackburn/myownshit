// Props for the "potes poissons" story (the man who drowned and built a city under the sea), tornado-replica style.
// Same conventions as props.js; every prop that holds still on screen keeps a small loop of motion (pure function of t).
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, sphere, rng, ease, clamp01 } from './style.js';
import { grp, at, mesh, canvasPlane, buildProp } from './props.js';

const PI = Math.PI, TAU = PI * 2;
const keyed = (list, t, def) => { let v = def; for (const [a, x] of (list || [])) { if (t >= a) v = x; else break; } return v; };
const keyAt = (list, t) => { let a0 = null; for (const [a, x] of (list || [])) if (t >= a && x) a0 = a; return a0; };
const FISH_COLS = ['#F2C230', '#E8742E', '#4FD1C5', '#F28CA0', '#F2A93B', '#7FD3F0'];

function fishMesh(color, s = 1) { // a small low-poly fish facing +X: tapered body, tail fin, eyes
  const g = grp(), body = box(0.36 * s, 0.2 * s, 0.1 * s, color, { taper: { x: 1, z: 0.6 } }); g.add(body);
  const tail = new THREE.Mesh(new THREE.ConeGeometry(0.1 * s, 0.16 * s, 3), mat(color)); tail.rotation.z = PI / 2; tail.position.x = -0.24 * s; tail.scale.z = 0.35; g.add(tail);
  const fin = box(0.1 * s, 0.07 * s, 0.02 * s, color); fin.position.set(0, 0.12 * s, 0); g.add(fin);
  [-1, 1].forEach(z => { const e = at(box(0.045 * s, 0.045 * s, 0.01, '#FFFFFF'), 0.12 * s, 0.03 * s, z * 0.051 * s), p = at(box(0.022 * s, 0.022 * s, 0.012, '#1C252A'), 0.125 * s, 0.03 * s, z * 0.056 * s); g.add(e, p); });
  g.userData.tail = tail; return g;
}

export const OCEAN_PROPS = {
  fishSchool(o) { // n fish circling an ellipse (rx, rz) between y0 and y1, tails wagging; o.dir 1 / -1
    const r = rng(o.seed || 3), g = grp(), F = [];
    for (let i = 0; i < (o.n || 8); i++) { const f = fishMesh(o.color || FISH_COLS[i % FISH_COLS.length], (o.size || 1) * (0.8 + r() * 0.5)); F.push({ f, ph: r() * TAU, y: (o.y0 ?? 0.5) + r() * ((o.y1 ?? 2.5) - (o.y0 ?? 0.5)), k: 0.8 + r() * 0.4, rr: 0.75 + r() * 0.5 }); g.add(f); }
    const rx = o.rx || 3, rz = o.rz || 2, sp = (o.speed || 0.5) * (o.dir || 1);
    g.userData.update = t => F.forEach(q => { const a = q.ph + t * sp * q.k; const x = Math.cos(a) * rx * q.rr, z = Math.sin(a) * rz * q.rr;
      q.f.position.set(x, q.y + 0.12 * Math.sin(t * 2 + q.ph), z); q.f.rotation.y = -a - (sp > 0 ? PI / 2 : -PI / 2); q.f.userData.tail.rotation.y = 0.5 * Math.sin(t * 12 + q.ph); });
    g.userData.update(0); return g;
  },
  bubbles(o) { // white bubble rings rising and wobbling; o.rate per second (continuous) and/or o.burst [[t, count]]
    const r = rng(o.seed || 5), g = grp(), H = o.h || 4, list = [];
    const ring = R => new THREE.Mesh(new THREE.TorusGeometry(R, R * 0.16, 6, 16), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.9 }));
    const N = Math.ceil((o.rate || 0) * 6); for (let i = 0; i < N; i++) { const m = ring(0.04 + r() * 0.06); list.push({ m, kind: 'loop', ph: r(), x: (r() - 0.5) * (o.area || 0.5), z: (r() - 0.5) * (o.area || 0.5) }); g.add(m); }
    (o.burst || []).forEach(([t0, n]) => { for (let i = 0; i < n; i++) { const m = ring(o.big || 0.09); list.push({ m, kind: 'burst', t0: t0 + i * (o.gap || 0.16), x: 0, z: 0 }); g.add(m); } });
    g.userData.update = t => list.forEach((b, i) => {
      let k; if (b.kind === 'loop') k = (t / 6 * (o.rate ? 6 / N : 1) * (o.speed || 1) + b.ph) % 1; else { const u = t - b.t0; b.m.visible = u >= 0 && u < (o.life || 1.4); if (!b.m.visible) return; k = u / (o.life || 1.4); }
      b.m.position.set(b.x + 0.06 * Math.sin(t * 5 + i), k * H, b.z); b.m.rotation.set((o.facing ? 0 : PI / 2) + 0.3 * Math.sin(t * 3 + i), 0, 0); b.m.material.opacity = 0.9 * (1 - k * 0.6); });
    g.userData.update(0); return g;
  },
  seaweed(o) { // a clump of green blades swaying with a lag up the blade
    const r = rng(o.seed || 7), g = grp(), blades = [], cols = ['#3E9B5F', '#2F7F4F', '#5BB06E', '#4AA866'];
    for (let i = 0; i < (o.n || 7); i++) { const segs = [], H = (o.h || 1.4) * (0.6 + r() * 0.6), n = 6, root = grp(); root.position.set((r() - 0.5) * (o.w || 0.8), 0, (r() - 0.5) * (o.w || 0.8)); let parent = root;
      for (let s = 0; s < n; s++) { const p = grp(at(box(0.09 - s * 0.01, H / n, 0.03, cols[i % 4]), 0, H / n / 2, 0)); p.position.y = s ? H / n : 0; parent.add(p); parent = p; segs.push(p); }
      blades.push({ segs, ph: r() * TAU }); g.add(root); }
    g.userData.update = t => blades.forEach(b => b.segs.forEach((p, s) => { p.rotation.z = 0.13 * Math.sin(t * 1.6 + b.ph - s * 0.5); p.rotation.x = 0.06 * Math.sin(t * 1.1 + b.ph - s * 0.4); }));
    g.userData.update(0); return g;
  },
  lightRays(o) { // soft shafts of light from the surface, swaying
    const r = rng(o.seed || 11), g = grp(), rays = [];
    for (let i = 0; i < (o.n || 6); i++) { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 2.2 + r() * 1.5, o.h || 30, 6, 1, true), new THREE.MeshBasicMaterial({ color: '#E8FBFF', transparent: true, opacity: 0.07, depthWrite: false, side: THREE.DoubleSide, fog: false }));
      m.position.set((r() - 0.5) * (o.w || 30), (o.h || 30) / 2, -r() * (o.d || 30)); m.rotation.z = 0.25; rays.push({ m, ph: r() * TAU }); g.add(m); }
    g.userData.update = t => rays.forEach(q => { q.m.rotation.z = 0.25 + 0.05 * Math.sin(t * 0.7 + q.ph); q.m.material.opacity = 0.06 + 0.025 * Math.sin(t * 1.3 + q.ph); });
    g.userData.update(0); return g;
  },
  barbecue(o) { // charcoal grill: legs, bowl, grill bars, flames, an orange fish grilling, a thread of smoke
    const g = grp(); [-1, 1].forEach(s => g.add(at(box(0.04, 0.7, 0.04, '#2B2E33'), s * 0.22, 0.35, 0.12), at(box(0.04, 0.7, 0.04, '#2B2E33'), s * 0.22, 0.35, -0.12)));
    g.add(at(box(0.62, 0.14, 0.4, '#3A3D44'), 0, 0.72, 0)); for (let i = 0; i < 7; i++) g.add(at(box(0.6, 0.012, 0.012, '#9AA0A6'), 0, 0.8, -0.16 + i * 0.053));
    const fl = grp(); [[-0.15, 0], [0, 0.04], [0.15, -0.03]].forEach(([x, z]) => fl.add(at(buildProp('flame', { scale: 0.5 }), x, 0.78, z))); g.add(fl);
    if (o.fish !== false) { const f = fishMesh('#E8742E', 1.2); f.position.set(0, 0.86, 0); f.rotation.x = PI / 2; g.add(f); }
    g.userData.update = t => { fl.children.forEach((c, i) => { c.userData.update?.(t); c.scale.setScalar(1 + 0.12 * Math.sin(t * 17 + i * 2)); }); fl.visible = !keyed(o.out, t, false); };
    g.userData.update(0); return g;
  },
  fishCart(o) { // wooden cart on four wheels with a fish driver; wheels roll with o.roll (radians per second)
    const g = grp(), cart = at(box(0.9, 0.3, 0.55, '#A0703E', { outline: 0.01 }), 0, 0.35, 0); g.add(cart);
    const wheels = []; [[-0.3, 0.3], [0.3, 0.3], [-0.3, -0.3], [0.3, -0.3]].forEach(([x, z]) => { const w = at(cyl(0.16, 0.16, 0.06, '#5B3A1E', 8), x, 0.16, z, PI / 2, 0, 0); wheels.push(w); g.add(w); });
    const f = fishMesh(o.color || FISH_COLS[(o.seed || 0) % FISH_COLS.length], 1.6); f.position.set(0.05, 0.68, 0); g.add(f);
    g.userData.update = t => { wheels.forEach(w => { w.rotation.y = -(o.roll || 0) * t; }); f.userData.tail.rotation.y = 0.4 * Math.sin(t * 9); f.position.y = 0.68 + 0.02 * Math.sin(t * 6); };
    g.userData.update(0); return g;
  },
  stoneHut(o) { // grey stone hut; o.collapse [[t, true]] knocks its walls flat (the current at night)
    const W = o.w || 2.4, H = o.h || 1.8, g = grp(), walls = [];
    const wall = (w, x, z, ry) => { const p = grp(at(box(w, H, 0.25, o.color || '#9AA3A8', { outline: 0.01 }), 0, H / 2, 0)); p.position.set(x, 0, z); p.rotation.y = ry; walls.push(p); g.add(p); return p; };
    wall(W, 0, W / 2, 0); wall(W, 0, -W / 2, PI); wall(W, W / 2, 0, PI / 2); wall(W, -W / 2, 0, -PI / 2);
    g.add(at(box(0.6, 1.0, 0.27, '#4B4F55'), 0, 0.5, W / 2 + 0.01));
    const roof = new THREE.Mesh(new THREE.ConeGeometry(W * 0.82, 1.1, 4), mat(o.roof || '#7E888E')); roof.rotation.y = PI / 4; roof.position.y = H + 0.55; g.add(roof);
    g.userData.update = t => { const a0 = keyAt(o.collapse, t); const u = a0 == null ? 0 : ease.in(clamp01((t - a0) / 0.5)); walls.forEach((p, i) => { p.rotation.x = -u * 1.45 * (i % 2 ? 1 : 1); }); roof.position.y = H + 0.55 - u * (H + 0.2); roof.rotation.z = u * 0.4; };
    g.userData.update(0); return g;
  },
  neonTower(o) { // slate skyscraper with window grid and glowing neon bands; o.riseAt: grows out of the sand with an overshoot
    const W = o.w || 3, H = o.h || 14, D = o.d || 3, g = grp(), body = grp(); g.add(body);
    const tex = canvasPlane(W, H, (c, Wp, Hp) => { c.fillStyle = o.color || '#4B5C68'; c.fillRect(0, 0, Wp, Hp); c.fillStyle = '#7FA4B8'; const cols = 4, rows = Math.round(H / 1.2);
      for (let rr = 0; rr < rows; rr++) for (let k = 0; k < cols; k++) if ((rr * 7 + k * 3) % 5) c.fillRect((k + 0.25) * Wp / cols, (rr + 0.3) * Hp / rows, Wp / cols * 0.5, Hp / rows * 0.45); }, { res: 256 });
    const core = box(W, H, D, o.color || '#4B5C68'); core.position.y = H / 2; body.add(core); [0, PI / 2, PI, -PI / 2].forEach(a => { const f = tex.clone(); f.position.set(Math.sin(a) * (W / 2 + 0.01), H / 2, Math.cos(a) * (D / 2 + 0.01)); f.rotation.y = a; body.add(f); });
    const bands = [], nc = o.neon || ['#6FE7FF', '#FF6FB0'];
    for (let i = 0; i < (o.bands || 4); i++) { const y = H * (0.25 + i * 0.18); const m = new THREE.Mesh(new THREE.BoxGeometry(W + 0.08, 0.12, D + 0.08), new THREE.MeshBasicMaterial({ color: nc[i % nc.length], transparent: true, opacity: 0.95 })); m.position.y = y; bands.push(m); body.add(m); }
    g.userData.update = t => { bands.forEach((m, i) => { m.material.opacity = 0.75 + 0.25 * Math.sin(t * 7 + i * 1.7) * (keyed(o.flicker, t, true) ? 1 : 0); });
      if (o.riseAt != null) { const u = clamp01((t - o.riseAt) / (o.riseDur || 0.6)); body.scale.y = Math.max(0.001, ease.outBack(u)); body.visible = t >= o.riseAt; } };
    g.userData.update(0); return g;
  },
  eelPlug(o) { // a green eel undulating, its tail cabled to a yellow socket with a face; o.zapAt makes sparks fly
    const g = grp(), segs = [], n = 10, L = o.len || 2.2;
    for (let i = 0; i < n; i++) { const s = at(box(L / n * 1.05, 0.16 - i * 0.008, 0.12 - i * 0.006, '#4FAE5A', { outline: 0.006 }), 0, 0, 0); segs.push(s); g.add(s); }
    const head = segs[0]; [-1, 1].forEach(z => head.add(at(box(0.05, 0.05, 0.01, '#FFFFFF'), 0.06, 0.04, z * 0.062), at(box(0.025, 0.025, 0.012, '#1C252A'), 0.068, 0.04, z * 0.066)));
    const sock = grp(at(box(0.5, 0.5, 0.5, '#F2C94C', { outline: 0.01 }), 0, 0.25, 0)); [-1, 1].forEach(x => sock.add(at(box(0.07, 0.11, 0.01, '#1C252A'), x * 0.1, 0.32, 0.252))); sock.position.set(-L - 0.9, 0, -0.1); g.add(sock);
    const cable = mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.9, 6), mat('#2B2E33')); cable.rotation.z = PI / 2; cable.position.set(-L - 0.42, 0.25, -0.05); g.add(cable);
    const sparks = []; for (let i = 0; i < 10; i++) { const m = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.18, 0.03), new THREE.MeshBasicMaterial({ color: '#FFF27A' })); sparks.push(m); g.add(m); }
    g.userData.update = t => { segs.forEach((s, i) => { const x = -i * L / n; s.position.set(x, 0.5 + 0.12 * Math.sin(t * 6 - i * 0.7), 0.15 * Math.sin(t * 4 - i * 0.6)); s.rotation.y = 0.3 * Math.cos(t * 4 - i * 0.6); });
      const z0 = o.zapAt ?? 1e9, u = t - z0; sparks.forEach((m, i) => { const on = u >= 0 && (u % 0.5) < 0.3; m.visible = on; if (on) { const a = i / 10 * TAU + u * 9; m.position.set(-L * 0.5 + Math.cos(a) * 0.4 * (u % 0.5 + 0.3), 0.6 + Math.sin(a) * 0.4 * (u % 0.5 + 0.3), 0.1); m.rotation.z = a; } }); };
    g.userData.update(0); return g;
  },
  signal6G(o) { // a big screen: "6G" and four signal bars lighting up one by one from o.t0
    const W = o.w || 1.2, H = o.h || 1.6, g = grp(at(box(W + 0.08, H + 0.08, 0.06, '#1C2733'), 0, 0, -0.04));
    const mk = n => canvasPlane(W, H, (c, Wp, Hp) => { c.fillStyle = '#1E3A5A'; c.fillRect(0, 0, Wp, Hp); c.fillStyle = '#9FF0FF'; c.font = `900 ${Hp * 0.24}px Arial`; c.textAlign = 'center'; c.fillText('6G', Wp / 2, Hp * 0.32);
      for (let i = 0; i < 4; i++) { c.fillStyle = i < n ? '#9FF0FF' : '#35506E'; const bw = Wp * 0.12, bh = Hp * (0.12 + i * 0.09); c.fillRect(Wp * (0.2 + i * 0.17), Hp * 0.88 - bh, bw, bh); } }, { res: 256, emissive: 0.9 });
    const planes = [0, 1, 2, 3, 4].map(mk); planes.forEach(p => g.add(p));
    g.userData.update = t => { const n = Math.max(0, Math.min(4, Math.floor((t - (o.t0 || 0)) / 0.15) + 1)); planes.forEach((p, i) => { p.visible = i === n; }); };
    g.userData.update(0); return g;
  },
  oceanTank(o) { // a glass tank full of sea with fish inside, bars on the front, the OCÉAN EN GARDE À VUE sign on top
    const W = o.w || 4, H = o.h || 2.6, D = o.d || 2.4, g = grp();
    const water = new THREE.Mesh(new THREE.BoxGeometry(W - 0.1, H * 0.92, D - 0.1), new THREE.MeshLambertMaterial({ color: '#3FA7D6', transparent: true, opacity: 0.55 })); water.position.y = H * 0.46; g.add(water);
    const glass = new THREE.Mesh(new THREE.BoxGeometry(W, H, D), new THREE.MeshLambertMaterial({ color: '#D9F2FF', transparent: true, opacity: 0.18, depthWrite: false })); glass.position.y = H / 2; g.add(glass);
    g.add(at(box(W + 0.1, 0.12, D + 0.1, '#2B3A4A'), 0, 0.06, 0), at(box(W + 0.1, 0.12, D + 0.1, '#2B3A4A'), 0, H, 0));
    for (let i = 0; i <= 10; i++) g.add(at(box(0.04, H, 0.04, '#3A4652'), -W / 2 + i * W / 10, H / 2, D / 2 + 0.03));
    const school = OCEAN_PROPS.fishSchool({ n: o.fish || 9, rx: W * 0.35, rz: D * 0.3, y0: 0.4, y1: H * 0.8, speed: 0.9, seed: 4 }); g.add(school);
    const sign = canvasPlane(W * 0.62, 0.62, (c, Wp, Hp) => { c.fillStyle = '#F4F1E8'; c.fillRect(0, 0, Wp, Hp); c.strokeStyle = '#1E2A33'; c.lineWidth = Hp * 0.06; c.strokeRect(4, 4, Wp - 8, Hp - 8); c.fillStyle = '#1E2A33'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${Hp * 0.34}px Arial`; c.fillText('OCÉAN', Wp / 2, Hp * 0.32); c.font = `900 ${Hp * 0.24}px Arial`; c.fillText('EN GARDE À VUE', Wp / 2, Hp * 0.72); }, { res: 512 });
    sign.position.set(0, H + 0.45, D / 2); g.add(sign);
    g.userData.update = t => { school.userData.update(t); water.position.y = H * 0.46 + 0.01 * Math.sin(t * 3); };
    g.userData.update(0); return g;
  },
  waterGlass(o) { // an empty drinking glass (o.level 0..1 of water)
    const g = grp(); const gl = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.038, 0.13, 12, 1, true), new THREE.MeshLambertMaterial({ color: '#E8F6FF', transparent: true, opacity: 0.35, side: THREE.DoubleSide, depthWrite: false }));
    gl.position.y = 0.065; g.add(gl, at(cyl(0.038, 0.038, 0.008, '#DCEFF8', 12), 0, 0.004, 0));
    let w = null, wl = null;
    if (o.level) { w = at(cyl(0.042, 0.038, 0.12 * o.level, o.water || '#7FC6EA', 12), 0, 0.06 * o.level + 0.008, 0); g.add(w); }   // (cycle 13) o.water: a deeper blue that reads under a warm grade (the pale one came out white)
    // (pass 3 of 50) o.tumbler: a thick white rim at the mouth, two highlight strips down the side, a firmer glass and a lighter water line (a pale
    // see-through slab with no rim and no water line read as neither a glass nor upside down)
    if (o.tumbler) { gl.material.opacity = 0.5; g.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.045, 0.0065, 6, 16), new THREE.MeshLambertMaterial({ color: '#F6FBFF' })), 0, 0.13, 0, PI / 2, 0, 0));
      for (const a of [0.5, 0.8]) g.add(at(box(0.006, 0.11, 0.002, '#FFFFFF'), Math.sin(a) * 0.043, 0.068, Math.cos(a) * 0.043, 0, a, 0));
      if (o.level) { wl = at(cyl(0.0425, 0.0425, 0.004, o.waterLine || '#9ED8FF', 12), 0, 0.12 * o.level + 0.009, 0); g.add(wl); } }
    // (pass 4 of 50) o.vivid: the water unlit in a saturated blue behind a thinner glass (through the white glass it came out grey: a jar of nothing);
    // o.levels [[t, level], ...]: the level over time, the gulps drinking it down
    if (o.vivid && w) { w.material = new THREE.MeshBasicMaterial({ color: o.water || '#2E8BEA', toneMapped: false }); gl.material.opacity = 0.2; if (wl) wl.material = new THREE.MeshBasicMaterial({ color: o.waterLine || '#CFEFFF', toneMapped: false }); }
    if (o.levels && w) { const L0 = o.level, ks = o.levels;
      g.userData.update = t => { let lv = ks[0][1]; for (let i = 0; i < ks.length; i++) { if (t >= ks[i][0]) lv = ks[i][1]; if (i + 1 < ks.length && t >= ks[i][0] && t < ks[i + 1][0]) { const u = (t - ks[i][0]) / (ks[i + 1][0] - ks[i][0]); lv = ks[i][1] + (ks[i + 1][1] - ks[i][1]) * u; break; } }
        lv = Math.max(0.02, lv); w.scale.y = lv / L0; w.position.y = 0.06 * lv + 0.008; if (wl) wl.position.y = 0.12 * lv + 0.009; };
      g.userData.update(0); }
    g.userData.grip = [0, 0.06, 0]; return g;
  },
  sandPuff(o) { // a ring of sand clouds rising from the floor (current, impacts), from o.t0
    const g = grp(), r = rng(o.seed || 13), P0 = [];
    for (let i = 0; i < (o.n || 10); i++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(0.4, 1), new THREE.MeshLambertMaterial({ color: '#E6DEC4', transparent: true, opacity: 0.8 })); P0.push({ m, a: r() * TAU, v: 0.6 + r() * 0.8 }); g.add(m); }
    g.userData.update = t => { const u = t - (o.t0 || 0); P0.forEach(p => { p.m.visible = u > 0 && u < 1.6; if (!p.m.visible) return; const d = p.v * u * 1.5; p.m.position.set(Math.cos(p.a) * d, 0.2 + u * 0.5, Math.sin(p.a) * d); p.m.scale.setScalar(0.5 + u); p.m.material.opacity = 0.8 * (1 - u / 1.6); }); };
    g.userData.update(0); return g;
  },
};
