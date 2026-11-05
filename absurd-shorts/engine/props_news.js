// Props for the seven "faits divers" stories (sable, lune, sapin, escargot, grève, colis, heure), tornado-replica style.
// Conventions as in props.js; small loops of motion built in (pure functions of t).
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, sphere, rng, ease, clamp01 } from './style.js';
import { grp, at, mesh, canvasPlane } from './props.js';

const PI = Math.PI, TAU = PI * 2;
const keyAt = (list, t) => { let a0 = null; for (const [a, x] of (list || [])) if (t >= a && x) a0 = a; return a0; };
const pop = (t, a0, d = 0.3) => a0 == null || t < a0 ? 0 : Math.max(0.001, ease.outBack(clamp01((t - a0) / d)));
function sign(text, w, h, bg = '#F4F1E8', fg = '#1E2A33') {
  return canvasPlane(w, h, (c, W, H) => { c.fillStyle = bg; c.fillRect(0, 0, W, H); c.fillStyle = fg; c.textAlign = 'center'; c.textBaseline = 'middle';
    const L = String(text).split('\n'), m = Math.max(...L.map(l => l.length)); let px = Math.min(H * 0.7 / L.length, W * 0.9 / (m * 0.62)); c.font = `900 ${px}px Arial`;
    const wide = Math.max(...L.map(l => c.measureText(l).width)); if (wide > W * 0.9) { px *= W * 0.9 / wide; c.font = `900 ${px}px Arial`; }
    L.forEach((l, i) => c.fillText(l, W / 2, H / 2 + (i - (L.length - 1) / 2) * px * 1.1)); }, { res: 512 });
}
function palm(h = 1) { const g = grp(at(cyl(0.05 * h, 0.08 * h, h, '#8A6440', 6, { pivot: 'bottom' }), 0, 0, 0));
  for (let i = 0; i < 6; i++) { const lf = box(0.7 * h, 0.03, 0.18 * h, '#3E9B5F', { taper: { x: 1, z: 0.3 } }); lf.position.set(Math.cos(i / 6 * TAU) * 0.3 * h, h, Math.sin(i / 6 * TAU) * 0.3 * h); lf.rotation.set(0, -i / 6 * TAU, -0.45); g.add(lf); }
  return g; }


// a real grain of sand: an irregular faceted quartz pebble (icosahedron with per-vertex jitter, squashed), pivot at its bottom
function grainGeo(r, seed, detail = 1) {
  const R = rng(seed), geo = new THREE.IcosahedronGeometry(r, detail), pos = geo.attributes.position, v = new THREE.Vector3(), J = new Map();
  const sx = 0.95 + R() * 0.45, sy = 0.62 + R() * 0.22, sz = 0.8 + R() * 0.3;
  for (let i = 0; i < pos.count; i++) { v.fromBufferAttribute(pos, i); const key = `${v.x.toFixed(3)},${v.y.toFixed(3)},${v.z.toFixed(3)}`;
    if (!J.has(key)) J.set(key, 0.82 + R() * 0.32); const s = J.get(key); pos.setXYZ(i, v.x * s * sx, v.y * s * sy, v.z * s * sz); }
  geo.computeBoundingBox(); geo.translate(0, -geo.boundingBox.min.y, 0); geo.computeVertexNormals(); return geo;
}
const SAND = ['#E6C67E', '#DDB76C', '#EDD39A', '#D3AA62'];
// tiny flags on toothpicks: Brittany (gwenn-ha-du), Sardinia (four Moors), Italy, France
const flagDraw = kind => (c, W, H) => {
    if (kind === 'bzh') { for (let i = 0; i < 9; i++) { c.fillStyle = i % 2 ? '#F4F4F0' : '#17171B'; c.fillRect(0, i * H / 9, W, H / 9 + 1); }
      c.fillStyle = '#F4F4F0'; c.fillRect(0, 0, W * 0.42, H * 5 / 9); c.fillStyle = '#17171B';
      for (let r = 0; r < 3; r++) for (let q = 0; q < 3; q++) { const x = W * (0.07 + q * 0.13 + (r % 2) * 0.06), y = H * (0.1 + r * 0.15); c.beginPath(); c.moveTo(x, y - H * 0.05); c.lineTo(x + W * 0.025, y + H * 0.04); c.lineTo(x - W * 0.025, y + H * 0.04); c.fill(); } }
    else if (kind === 'sard') { c.fillStyle = '#F4F4F0'; c.fillRect(0, 0, W, H); c.fillStyle = '#C8322A'; c.fillRect(W * 0.44, 0, W * 0.12, H); c.fillRect(0, H * 0.41, W, H * 0.18);
      c.fillStyle = '#17171B'; for (const [x, y] of [[0.22, 0.2], [0.78, 0.2], [0.22, 0.8], [0.78, 0.8]]) { c.beginPath(); c.arc(W * x, H * y, H * 0.11, 0, TAU); c.fill(); c.fillStyle = '#F4F4F0'; c.fillRect(W * x - H * 0.12, H * y - H * 0.04, H * 0.24, H * 0.05); c.fillStyle = '#17171B'; } }
    else { const cols = kind === 'it' ? ['#2E8B4E', '#F4F4F0', '#C8322A'] : ['#24448E', '#F4F4F0', '#D03A34']; cols.forEach((col, i) => { c.fillStyle = col; c.fillRect(i * W / 3, 0, W / 3 + 1, H); }); }
};
function miniFlag(kind, w = 0.08) {
  const h = w * 0.66, g = grp(at(cyl(0.0025 * w / 0.08, 0.0025 * w / 0.08, h * 2.4, '#E9DDBF', 4, { pivot: 'bottom', noGrain: true }), 0, 0, 0));
  const f = canvasPlane(w, h, flagDraw(kind), { res: 256 });
  f.position.set(w / 2, h * 2.4 - h / 2, 0); g.add(f); g.userData.cloth = f; return g;
}

export const NEWS_PROPS = {
  regionFlag(o) { // a full-size flag on a pole, drawn: o.kind 'bzh' (Brittany), 'sard' (Sardinia), 'it', 'fr'; ripples
    const g = grp(at(cyl(0.015, 0.015, 1.6, '#9AA0A6', 5, { pivot: 'bottom' }), 0, 0, 0)), f = canvasPlane(0.6, 0.4, flagDraw(o.kind || 'bzh'), { res: 512 });
    f.position.set(0.31, 1.38, 0); g.add(f); g.userData.update = t => { f.rotation.y = 0.14 * Math.sin(t * 2.6 + (o.seed || 0)); }; return g;
  },
  sandGrain(o) { // ONE real grain of sand, not a cloud: faceted golden quartz pebble with glints; o.seed, o.color, o.flag 'bzh'|'sard'|'it'|'fr', o.eyes, o.popAt
    const g = grp(), body = new THREE.Mesh(grainGeo(0.05, o.seed || 3, 1), mat(o.color || '#E3C27A', { noGrain: true })); body.castShadow = body.receiveShadow = true; g.add(body);
    const R = rng((o.seed || 3) + 17), gl = [];
    for (let i = 0; i < 3; i++) { const sp = new THREE.Mesh(new THREE.OctahedronGeometry(0.006, 0), new THREE.MeshBasicMaterial({ color: '#FFFDF2' }));
      const a = R() * TAU, y = 0.02 + R() * 0.03; sp.position.set(Math.cos(a) * 0.045, y, Math.abs(Math.sin(a)) * 0.04 + 0.01); sp.userData.ph = R(); g.add(sp); gl.push(sp); }
    if (o.eyes) for (const sx of [-1, 1]) { const e = sphere(0.0055, '#17171B', 0, { noGrain: true }); e.position.set(sx * 0.014, 0.032, 0.048); g.add(e); }
    let fl = null; if (o.flag) { fl = miniFlag(o.flag, o.flagW || 0.08); fl.position.set(0.035, 0.02, -0.01); g.add(fl); }
    const rate = o.glint ?? 0.9;
    g.userData.update = t => { gl.forEach(sp => { const f = ((t * rate + sp.userData.ph) % 1); sp.scale.setScalar(Math.max(0.001, 1 - Math.abs(f - 0.5) * 14)); sp.rotation.y = t * 3; });
      if (fl) fl.userData.cloth.rotation.y = 0.18 * Math.sin(t * 5 + 1);
      if (o.popAt != null) { const k = pop(t, o.popAt, 0.3); g.scale.setScalar(k); } };
    g.userData.update(0); return g;
  },
  sandTray(o) { // a steel evidence tray holding grains in groups: o.groups [[n, x, z, color?, flag?]], o.w/o.d, o.countUp [t0, t1] pops them in one by one, o.label
    const w = o.w || 0.6, d = o.d || 0.4, g = grp(); if (!o.noTray) { g.add(at(box(w, 0.012, d, '#B9C0C6', { noGrain: true }), 0, 0.006, 0));
    for (const [x, z, bw, bd] of [[0, d / 2, w, 0.012], [0, -d / 2, w, 0.012], [w / 2, 0, 0.012, d], [-w / 2, 0, 0.012, d]]) g.add(at(box(bw, 0.03, bd, '#A3ABB2', { noGrain: true }), x, 0.015, z)); }
    const R = rng(o.seed || 5), all = [], flags = [], N = (o.groups || [[40]]).reduce((a, q) => a + q[0], 0), pile = 0.014 * Math.sqrt(N) + 0.008;
    for (const [n, gx, gz, col, flag] of (o.groups || [[40, 0, 0]])) {
      const rad = 0.014 * Math.sqrt(n) + 0.008, geos = [0, 1, 2, 3].map(i => grainGeo(0.011, 40 + i * 7, 0));
      for (let i = 0; i < n; i++) { const a = R() * TAU, r = rad * Math.sqrt(R()), m = new THREE.Mesh(geos[i % 4], mat(col || SAND[i % 4], { noGrain: true }));
        m.position.set(gx + Math.cos(a) * r, o.noTray ? 0 : 0.012, gz + Math.sin(a) * r); m.rotation.y = R() * TAU; m.castShadow = true; g.add(m); all.push(m);
        const a2 = R() * TAU, r2 = pile * Math.sqrt(R()); m.userData.end = m.position.clone(); m.userData.start = new THREE.Vector3(Math.cos(a2) * r2, m.position.y, Math.sin(a2) * r2); m.userData.lag = R(); }
      if (flag) { const f = miniFlag(flag, o.flagW || 0.07); f.position.set(gx + rad * 0.6, 0.012, gz - rad * 0.4); g.add(f); flags.push(f); }
    }
    if (o.label) { const l = sign(o.label, w * 0.7, 0.05, '#F4F1E8', '#1E2A33'); l.position.set(0, 0.016, d / 2 + 0.008); g.add(l); }
    const [c0, c1] = o.countUp || [null, null], order = all.map((m, i) => i).sort((a, b) => all[a].position.x - all[b].position.x);
    const [s0, s1] = o.sortAt || [null, null];   // sortAt [t0, t1]: the grains start mixed in one pile and slide to their groups (staggered), flags pop at t1
    g.userData.update = t => { if (c0 != null) order.forEach((idx, j) => { const tj = c0 + (c1 - c0) * j / Math.max(1, all.length - 1); all[idx].scale.setScalar(pop(t, tj, 0.12)); });
      if (s0 != null) all.forEach(m => { const a = s0 + m.userData.lag * (s1 - s0) * 0.5, k = ease.inOut(clamp01((t - a) / ((s1 - s0) * 0.5))); m.position.lerpVectors(m.userData.start, m.userData.end, k); });
      flags.forEach((f, i) => { f.userData.cloth.rotation.y = 0.15 * Math.sin(t * 4 + i); if (s0 != null) f.scale.setScalar(pop(t, s1, 0.3)); }); };
    g.userData.update(0); return g;
  },
  starsStripes(o) { // a stars-and-stripes flag on a pole (drawn), rippling a little
    const g = grp(at(cyl(0.015, 0.015, 1.6, '#9AA0A6', 5, { pivot: 'bottom' }), 0, 0, 0));
    const f = canvasPlane(0.9, 0.5, (c, W, H) => { for (let i = 0; i < 13; i++) { c.fillStyle = i % 2 ? '#F4F4F0' : '#B22234'; c.fillRect(0, i * H / 13, W, H / 13 + 1); }
      c.fillStyle = '#3C3B6E'; c.fillRect(0, 0, W * 0.42, H * 7 / 13); c.fillStyle = '#F4F4F0'; for (let r = 0; r < 5; r++) for (let q = 0; q < 6; q++) c.fillRect(W * (0.03 + q * 0.065), H * (0.04 + r * 0.1), W * 0.022, H * 0.04); }, { res: 512 });
    f.position.set(0.46, 1.33, 0); g.add(f); g.userData.update = t => { f.rotation.y = 0.12 * Math.sin(t * 2.5); }; return g;
  },
  bigShoe(o) { // a man's derby, open at the top, laces; whatever grows inside goes in at y 0.12
    const c = o.color || '#3A2A22', g = grp();
    g.add(at(box(0.34, 0.13, 0.13, c, { outline: 0.006 }), 0.02, 0.065, 0), at(box(0.12, 0.2, 0.13, c, { outline: 0.006 }), -0.12, 0.1, 0));
    g.add(at(box(0.36, 0.025, 0.14, '#1C1512'), 0.02, 0.012, 0));
    for (let i = 0; i < 3; i++) g.add(at(box(0.012, 0.012, 0.1, '#F4F1E8'), 0.0 + i * 0.04, 0.135, 0));
    return g;
  },
  growIsland(o) { // a grain that grows: sand grain -> pebble -> rock -> island with a palm, at the times in o.stages [[t, 0..3]]
    const g = grp(), sand = sphere(0.012, '#E7D7A8', 1), peb = sphere(0.035, '#9AA0A6', 0), rock = sphere(0.09, '#8A9096', 0);
    const isl = grp(at(sphere(1, '#E7D7A8', 1), 0, -0.05, 0), at(palm(0.9), 0.1, 0.05, 0)); isl.children[0].scale.set(0.42, 0.14, 0.3); isl.scale.setScalar(0.5);
    const water = at(cyl(0.34, 0.34, 0.02, '#3FB7D9', 16), 0, 0.0, 0); isl.add(water);
    [sand, peb, rock, isl].forEach(m => g.add(m)); peb.scale.set(1.3, 0.8, 1); rock.scale.set(1.4, 0.8, 1.1);
    g.userData.update = t => { let st = 0, a0 = 0; for (const [a, s] of (o.stages || [])) if (t >= a) { st = s; a0 = a; }
      [sand, peb, rock, isl].forEach((m, i) => { m.visible = i === st; if (i === st) { const k = Math.max(0.05, ease.outBack(clamp01((t - a0) / 0.35))); m.scale.setScalar(i === 3 ? 0.5 * k : k * (i === 1 ? 1.3 : i === 2 ? 1.4 : 1)); } }); };
    g.userData.update(0); return g;
  },
  shopFront(o) { // small lunar/street shop: box with a door, a window and a sign (o.text); pops up from o.popAt
    const W = o.w || 2.4, H = o.h || 2.2, g = grp(), body = grp(); g.add(body);
    body.add(at(box(W, H, 2, o.color || '#D9DCD6', { outline: 0.01 }), 0, H / 2, -1), at(box(0.6, 1.1, 0.04, '#3A4652'), -W * 0.25, 0.55, 0.01), at(box(0.8, 0.6, 0.04, '#7FC2EE'), W * 0.2, 1.1, 0.01));
    const s = sign(o.text || 'BANQUE', W * 0.9, 0.42, o.signBg || '#203447', '#FFFFFF'); s.position.set(0, H + 0.25, 0.02); body.add(s);
    g.userData.update = t => { if (o.popAt == null) return; const k = pop(t, o.popAt, 0.35); body.visible = k > 0.001; body.scale.setScalar(Math.max(0.001, k)); };
    g.userData.update(0); return g;
  },
  giantFir(o) { // a Christmas tree of any height: stacked cones, baubles, a blinking garland, a star; o.windows lights up flats in the boughs
    const H = o.h || 2.4, g = grp(), r = rng(o.seed || 5), n = Math.max(4, Math.round(H / 0.6)), lights = [];
    g.add(at(cyl(0.08 * H / 2.4, 0.1 * H / 2.4, H * 0.12, '#6B4A2E', 6, { pivot: 'bottom' }), 0, 0, 0));
    for (let i = 0; i < n; i++) { const u = i / n, rr = (1 - u) * 0.55 * H / 2.4 * 1.6 + 0.08, hh = H / n * 1.6; const c = new THREE.Mesh(new THREE.ConeGeometry(rr, hh, 8), mat(i % 2 ? '#2F7F4F' : '#3E9B5F')); c.position.y = H * 0.1 + u * H * 0.85 + hh / 2; g.add(c);
      for (let b = 0; b < 4 + Math.round(rr * 4); b++) { const a = r() * TAU, y = c.position.y - hh * 0.35 + r() * hh * 0.3; const m = sphere(0.035 * Math.max(1, H / 6), ['#E0413A', '#F2C230', '#2F62B5', '#F28CA0'][b % 4], 1); m.position.set(Math.cos(a) * rr * 0.75, y, Math.sin(a) * rr * 0.75); g.add(m);
        const L = new THREE.Mesh(new THREE.SphereGeometry(0.02 * Math.max(1, H / 6), 6, 4), new THREE.MeshBasicMaterial({ color: '#FFF27A' })); L.position.set(Math.cos(a + 1) * rr * 0.8, y + hh * 0.1, Math.sin(a + 1) * rr * 0.8); lights.push(L); g.add(L);
        if (o.windows && r() < 0.5) { const w = new THREE.Mesh(new THREE.BoxGeometry(0.18 * H / 12, 0.14 * H / 12, 0.02), new THREE.MeshBasicMaterial({ color: '#FFE9A8' })); w.position.set(Math.cos(a + 2) * rr * 0.9, y, Math.sin(a + 2) * rr * 0.9); w.lookAt(0, y, 0); w.rotateY(PI); g.add(w); } } }
    const star = new THREE.Mesh(new THREE.OctahedronGeometry(0.12 * H / 2.4, 0), new THREE.MeshBasicMaterial({ color: '#FFD84A' })); star.position.y = H * 1.0; g.add(star);
    const needles = []; if (o.shed) for (let i = 0; i < 60; i++) { const m = new THREE.Mesh(new THREE.BoxGeometry(0.01 * H / 2.4, 0.06 * H / 2.4, 0.01), mat('#3E9B5F')); needles.push({ m, a: r() * TAU, d: r() * 0.5 * H / 2.4, y0: r() * H, ph: r() }); g.add(m); }
    g.userData.update = t => { lights.forEach((L, i) => { L.visible = ((Math.floor(t * 3) + i) % 3) !== 0; }); star.rotation.y = t * 1.2; star.scale.setScalar(1 + 0.08 * Math.sin(t * 6));
      g.rotation.z = (o.sway || 0) * Math.sin(t * 1.3); const s0 = keyAt(o.shed, t);
      needles.forEach(nd => { if (s0 == null) { nd.m.visible = false; return; } const u = (t - s0) * 0.8 + nd.ph; const y = nd.y0 - ((u * 3) % (nd.y0 + 0.1)); nd.m.visible = true; nd.m.position.set(Math.cos(nd.a) * (nd.d + u * 0.2), Math.max(0.01, y), Math.sin(nd.a) * (nd.d + u * 0.2)); nd.m.rotation.z = u * 5; }); };
    g.userData.update(0); return g;
  },
  tortoise(o) { // a tortoise in a lawyer's white collar: domed shell, head that bobs, stubby legs
    const g = grp(), sh = sphere(0.3, o.color || '#6E8A4E', 1); sh.scale.set(1.2, 0.7, 1); sh.position.y = 0.22; g.add(sh);
    g.add(at(box(0.62, 0.05, 0.5, '#8FA86A'), 0, 0.1, 0));
    const head = grp(at(sphere(0.1, '#9DB57A', 1), 0, 0, 0)); [-1, 1].forEach(z => head.add(at(box(0.03, 0.03, 0.01, '#1C252A'), 0.07, 0.03, z * 0.06)));
    head.add(at(box(0.06, 0.08, 0.16, '#F4F4F0'), -0.02, -0.08, 0)); head.position.set(0.42, 0.25, 0); g.add(head);
    [[0.22, 0.2], [0.22, -0.2], [-0.22, 0.2], [-0.22, -0.2]].forEach(([x, z]) => g.add(at(cyl(0.05, 0.06, 0.14, '#9DB57A', 6, { pivot: 'bottom' }), x, 0, z)));
    g.userData.update = t => { head.position.x = 0.42 + 0.03 * Math.sin(t * 2.2); head.rotation.z = 0.08 * Math.sin(t * 1.7); };
    g.userData.update(0); return g;
  },
  motorbike(o) { // a small red motorbike, wheels spinning with o.roll
    const g = grp(), wheels = []; [[0.5, 0], [-0.5, 0]].forEach(([x]) => { const w = at(cyl(0.22, 0.22, 0.08, '#1C1E22', 12), x, 0.22, 0, PI / 2, 0, 0); wheels.push(w); g.add(w); });
    g.add(at(box(0.8, 0.22, 0.2, o.color || '#C8322A', { outline: 0.008 }), 0, 0.5, 0), at(box(0.3, 0.12, 0.22, '#2B2E33'), -0.15, 0.66, 0), at(box(0.06, 0.4, 0.06, '#9AA0A6'), 0.42, 0.62, 0), at(box(0.04, 0.04, 0.45, '#2B2E33'), 0.42, 0.82, 0));
    g.userData.update = t => wheels.forEach(w => { w.rotation.y = (o.roll || 0) * t; });
    g.userData.update(0); return g;
  },
  slug(o) { // a snail without its shell (or a slug): soft body, eye stalks, wiggle
    const g = grp(), b = sphere(0.1, o.color || '#C9A27A', 1); b.scale.set(2.2, 0.55, 0.9); b.position.y = 0.05; g.add(b);
    const st = [-1, 1].map(z => { const s = grp(at(cyl(0.008, 0.01, 0.12, o.color || '#C9A27A', 5, { pivot: 'bottom' }), 0, 0, 0), at(sphere(0.018, '#1C252A', 0), 0, 0.12, 0)); s.position.set(0.18, 0.08, z * 0.03); g.add(s); return s; });
    g.userData.update = t => { b.scale.x = 2.2 + 0.15 * Math.sin(t * 4); st.forEach((s, i) => { s.rotation.z = -0.3 + 0.15 * Math.sin(t * 3 + i); }); };
    g.userData.update(0); return g;
  },
  fireTruck(o) { // red fire engine with a ladder; o.spray [[t, true]] shoots a water jet from the hose
    const g = grp(); g.add(at(box(4.4, 1.6, 1.8, '#C8322A', { outline: 0.015 }), 0, 1.2, 0), at(box(1.3, 1.1, 1.75, '#C8322A'), 2.5, 0.95, 0), at(box(0.5, 0.6, 1.6, '#7FC2EE'), 3.0, 1.25, 0));
    [[-1.4, 0.95], [-1.4, -0.95], [1.9, 0.95], [1.9, -0.95]].forEach(([x, z]) => g.add(at(cyl(0.4, 0.4, 0.3, '#1C1E22', 10), x, 0.4, z, PI / 2, 0, 0)));
    g.add(at(box(3.6, 0.12, 0.5, '#B9BDBF'), -0.3, 2.1, 0));
    const jet = grp(); for (let i = 0; i < 48; i++) { const d = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.26, 0.26), new THREE.MeshBasicMaterial({ color: i % 3 === 2 ? '#F2FAFF' : '#3B8FE0', transparent: true, opacity: 0.92 })); jet.add(d); } jet.position.set(-2.1, 1.9, 0); g.add(jet);   // saturated blue + white foam: reads against sky and clouds
    const RE = o.reach || 9, LI = o.lift || 2.4;   // jet length along local -x and initial rise
    g.userData.update = t => { const a0 = keyAt(o.spray, t); jet.visible = a0 != null; if (a0 == null) return; jet.children.forEach((d, i) => { const k = Math.min(((t - a0) * 2 + i / 48) % 1, (t - a0) * 1.6), x = -k * RE, y = k * LI - k * k * (LI + 1.8); d.position.set(x, y, 0.15 * Math.sin(i)); d.rotation.z = Math.atan2(LI - 2 * (LI + 1.8) * k, -RE); }); };
    g.userData.update(0); return g;
  },
  rainbow(o) { // a rainbow arc of radius o.r, drawing on from o.t0
    const R = o.r || 6, g = grp(), cols = ['#E0413A', '#F28C30', '#F2C230', '#5BB06E', '#2F62B5', '#7A4FB5'], arcs = [];
    cols.forEach((c, i) => { const m = new THREE.Mesh(new THREE.TorusGeometry(R - i * 0.32, 0.16, 6, 48, PI), new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: 0.9 })); g.add(m); arcs.push(m); });
    g.userData.update = t => { const k = o.t0 == null ? 1 : clamp01((t - o.t0) / 0.6); arcs.forEach(m => { m.scale.setScalar(Math.max(0.001, ease.outBack(k))); }); };
    g.userData.update(0); return g;
  },
  train(o) { // a high-speed train (nose + o.cars carriages), moving along its local +X by o.speed m/s from o.t0
    const g = grp(), body = grp(); g.add(body); const n = o.cars || 3, c = o.color || '#F4F4F0', stripe = o.stripe || '#2F62B5';
    const nose = box(4, 1.6, 1.4, c, { taper: { x: 0.35, z: 1 }, taperAxis: 'x', outline: 0.01 }); nose.position.set(2, 1.0, 0); body.add(nose);
    for (let i = 0; i < n; i++) { body.add(at(box(5.6, 1.7, 1.45, c, { outline: 0.01 }), -3 - i * 5.8, 1.05, 0), at(box(5.6, 0.2, 1.47, stripe), -3 - i * 5.8, 0.6, 0));
      for (let w = 0; w < 5; w++) body.add(at(box(0.6, 0.4, 1.48, '#3A4652'), -5.2 + w * 1.1 - i * 5.8, 1.35, 0)); }
    g.userData.update = t => { body.position.x = Math.max(0, t - (o.t0 || 0)) * (o.speed || 0); };
    g.userData.update(0); return g;
  },
  medal(o) { // a gold medal on a tricolour ribbon (hangs from y 0)
    const g = grp(); ['#2F62B5', '#F4F4F0', '#E0413A'].forEach((c, i) => g.add(at(box(0.025, 0.12, 0.004, c), -0.025 + i * 0.025, -0.06, 0)));
    const d = at(cyl(0.045, 0.045, 0.01, '#E8B830', 16), 0, -0.15, 0, PI / 2, 0, 0); g.add(d); g.userData.update = t => { d.rotation.z = 0.3 * Math.sin(t * 2); }; return g;
  },
  bigWatch(o) { // a wrist watch the size of a hand (o.time "HH:MM" digital)
    const g = grp(at(box(0.08, 0.3, 0.012, '#2B2E33'), 0, 0, 0), at(box(0.12, 0.1, 0.03, '#C9CDD2', { outline: 0.004 }), 0, 0, 0.01));
    const f = canvasPlane(0.1, 0.08, (c, W, H) => { c.fillStyle = '#1C2733'; c.fillRect(0, 0, W, H); c.fillStyle = '#9FF0FF'; c.font = `900 ${H * 0.5}px monospace`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.time || '10:00', W / 2, H / 2); }, { res: 256, emissive: 0.8 });
    f.position.z = 0.026; g.add(f); return g;
  },
  splitMap(o) { // France as one shape split in two halves of different colours by a dashed line (two time zones)
    const K = o.k || 10, g = grp(), pr = ([lon, lat]) => [(lon - 3) * K * 0.68, -(lat - 47.5) * K];
    const FR = [[2.55, 51.08], [1.6, 50.9], [1.6, 50.2], [0.1, 49.5], [-1.2, 49.4], [-1.9, 49.7], [-1.6, 48.65], [-3.5, 48.8], [-4.8, 48.4], [-4.7, 47.9], [-2.2, 47.2], [-1.2, 46.2], [-1.2, 44.6], [-1.8, 43.35],
      [-0.6, 42.9], [1.7, 42.5], [3.1, 42.45], [3.2, 43.0], [4.8, 43.4], [6.2, 43.1], [7.5, 43.8], [6.8, 44.4], [7.0, 45.9], [6.1, 46.4], [7.6, 47.6], [8.2, 49.0], [6.4, 49.45], [5.9, 49.5], [4.85, 49.8], [4.8, 50.15], [4.2, 49.95], [3.6, 50.4], [2.9, 50.7]];
    const clip = (pts, west) => pts.map(p => [west ? Math.min(p[0], 2.5) : Math.max(p[0], 2.5), p[1]]);
    [[true, o.west || '#F2C94C'], [false, o.east || '#8CC768']].forEach(([w, c]) => { const s = new THREE.Shape(); clip(FR, w).map(pr).forEach(([x, z], i) => i ? s.lineTo(x, -z) : s.moveTo(x, -z)); const m = mesh(new THREE.ShapeGeometry(s), mat(c)); m.rotation.x = -PI / 2; m.position.y = 0.03; g.add(m); });
    for (let i = 0; i < 16; i++) { const z0 = pr([2.5, 51 - i * 0.55])[1]; g.add(at(box(0.08 * K, 0.04 * K, 0.25 * K, '#FFFFFF'), pr([2.5, 0])[0], 0.06, z0)); }
    const sea = mesh(new THREE.PlaneGeometry(60 * K, 60 * K).rotateX(-PI / 2), mat(o.sea || '#5AA3DB')); sea.position.y = 0; g.add(sea);
    return g;
  },
};
