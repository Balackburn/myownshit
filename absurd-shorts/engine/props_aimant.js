// « L'aimant » (story 47): a man swallowed a magnet; since then all metal jumps on him (forks, keys, the frying pan), the street lamps bow as he passes,
// and the compasses no longer show the north: they show him. Hikers, boats and planes all come to his door. The cartographers rule that the north is now
// him; all the maps are redrawn; he lives at the North Pole, third floor, no lift.
// Conventions as in props.js (metres, front +Z, pivot at the floor); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, ease, clamp01 } from './style.js';
import { grp, at, label, canvasPlane, torus } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const rnd = s => { let x = Math.sin(s * 127.1) * 43758.5453; return x - Math.floor(x); };
const wob = (u, f, d) => u < 0 ? 0 : Math.exp(-u * d) * Math.sin(u * f);
const list = v => [].concat(v ?? []);
const _v = new THREE.Vector3();
function liveCanvas(w, h, res, basic = true) {
  const c = document.createElement('canvas'); c.width = res; c.height = Math.max(8, Math.round(res * h / w));
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const m = basic ? new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide, toneMapped: false }) : new THREE.MeshLambertMaterial({ map: tex, side: THREE.DoubleSide });
  const pl = new THREE.Mesh(new THREE.PlaneGeometry(w, h), m); pl.userData.noAO = true; let last = null;
  return { pl, redraw: (key, fn) => { if (key === last) return; last = key; fn(c.getContext('2d'), c.width, c.height); tex.needsUpdate = true; } };
}

export const AIMANT_PROPS = {
  // A red horseshoe magnet, the opening up (+Y), front +Z, about o.s (0.12 m) tall, pivot at its centre: two red arms joined by a half ring, silver poles.
  // o.glow [t0, t1]: three white arcs of "force" flicker round it.
  magnet(o) {
    const s = o.s ?? 0.12, r = s * 0.28, t = s * 0.14, g = grp();
    const red = '#D3202A', u = new THREE.Mesh(new THREE.TorusGeometry(r, t / 2, 6, 14, PI), mat(red)); u.rotation.z = PI; u.position.y = -s * 0.18; g.add(u);
    for (const sx of [-1, 1]) g.add(at(box(t, s * 0.42, t, red, { outline: 0.003 }), sx * r, s * 0.03, 0), at(box(t * 1.02, s * 0.16, t * 1.02, '#D9DDE3', { noGrain: true }), sx * r, s * 0.3, 0));
    if (o.glow) { const gm = new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.9, depthWrite: false }), arcs = [0, 1, 2].map(i => { const a = new THREE.Mesh(new THREE.TorusGeometry(s * (0.5 + 0.18 * i), 0.004, 4, 16, PI * 0.6), gm.clone()); a.rotation.z = PI * 0.2; a.position.y = s * 0.3; a.userData.noAO = true; g.add(a); return a; });
      const [a0, a1] = o.glow; g.userData.update = tt => arcs.forEach((a, i) => { const on = tt >= a0 && tt < a1; a.visible = on && Math.floor(tt * 15 + i) % 3 !== 0; a.scale.setScalar(1 + 0.08 * Math.sin(tt * 30 + i)); }); g.userData.update(0); }
    g.userData.grip = [0, -s * 0.2, 0]; return g;
  },

  // A frying pan (a poêle): black, o.r (0.15 m) across, its handle along +X; pivot at the centre of its bottom, the inside up (+Y). userData.grip on the handle.
  pan(o) {
    const r = o.r ?? 0.15, g = grp(at(cyl(r, r * 0.86, 0.045, '#2A2C31', 16, { outline: 0.006 }), 0, 0.022, 0), at(cyl(r * 0.84, r * 0.84, 0.004, '#45484F', 16, { noGrain: true }), 0, 0.044, 0),
      at(box(0.26, 0.022, 0.035, '#5A3A28', { outline: 0.004 }), r + 0.14, 0.04, 0), at(box(0.05, 0.024, 0.03, '#2A2C31'), r + 0.02, 0.04, 0));
    g.userData.grip = [r + 0.18, 0.04, 0]; return g;
  },

  // A hiker's compass, dial up (+Y; hold it with rot to show it to a camera), o.r (0.06 m): brass rim, white dial with N E S O, a needle red at its north
  // end. Its needle points at o.target [x, y, z] (world) — a man with a magnet in his stomach — from o.at (default 0); before that, at o.north (the world
  // direction of the true north, default -Z); between o.spin [t0, t1] it whirls, then swings to the target with a decaying wobble. o.n: the N letter in red.
  compass(o) {
    const r = o.r ?? 0.06, g = grp(at(cyl(r * 1.08, r * 1.12, r * 0.28, '#C9A24A', 20, { outline: 0.004 }), 0, r * 0.14, 0));
    const dial = canvasPlane(r * 1.9, r * 1.9, (c, W, H) => { c.fillStyle = '#F7F4EA'; c.beginPath(); c.arc(W / 2, H / 2, W / 2, 0, TAU); c.fill(); c.strokeStyle = '#1B1B1E'; c.lineWidth = W * 0.012;
      for (let i = 0; i < 36; i++) { const a = i * TAU / 36, L = i % 9 === 0 ? 0.12 : 0.06; c.beginPath(); c.moveTo(W / 2 + Math.sin(a) * W * 0.46, H / 2 - Math.cos(a) * H * 0.46); c.lineTo(W / 2 + Math.sin(a) * W * (0.46 - L), H / 2 - Math.cos(a) * H * (0.46 - L)); c.stroke(); }
      c.font = `900 ${H * 0.15}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; [['N', 0], ['E', 1], ['S', 2], ['O', 3]].forEach(([l, i]) => { c.fillStyle = l === 'N' ? '#C8202A' : '#1B1B1E'; const a = i * PI / 2; c.fillText(l, W / 2 + Math.sin(a) * W * 0.27, H / 2 - Math.cos(a) * H * 0.27); }); }, { res: 256 });
    dial.material = new THREE.MeshBasicMaterial({ map: dial.material.map, transparent: true, alphaTest: 0.05, side: THREE.DoubleSide }); dial.rotation.x = -PI / 2; dial.position.y = r * 0.29; dial.userData.noAO = true; g.add(dial);
    const needle = grp(at(box(r * 0.16, r * 0.04, r * 0.8, '#D3202A', { noGrain: true }), 0, 0, -r * 0.4), at(box(r * 0.16, r * 0.04, r * 0.8, '#F4F2EA', { noGrain: true }), 0, 0, r * 0.4), at(cyl(r * 0.08, r * 0.08, r * 0.06, '#1B1B1E', 8), 0, 0, 0));
    needle.position.y = r * 0.33; g.add(needle);
    const T = o.target ? new THREE.Vector3(...o.target) : null, N = new THREE.Vector3(...(o.north || [0, 0, -1])), sp = o.spin, t0 = o.at ?? 0;
    const angTo = (wp) => { _v.copy(wp); g.worldToLocal(_v); return Math.atan2(-_v.x, -_v.z); };   // the needle's red end lies along local -Z
    g.userData.update = t => { g.updateWorldMatrix(true, false); let a;
      const north = (() => { const p = new THREE.Vector3(); g.getWorldPosition(p); return angTo(p.add(N.clone().multiplyScalar(10))); })();
      const tgt = T ? angTo(T) : north;
      if (sp && t >= sp[0] && t < sp[1]) a = north + (t - sp[0]) * 26 + 0.3 * Math.sin(t * 40);
      else if (T && t >= (sp ? sp[1] : t0)) { const u = t - (sp ? sp[1] : t0); a = tgt + 0.6 * wob(u, 18, 4.5); }
      else a = north + 0.05 * Math.sin(t * 2.3);
      needle.rotation.y = a; };
    g.userData.update(0); g.userData.grip = [0, 0, 0]; return g;
  },

  // A hiker's backpack (front +Z is the side against the back): a rucksack with a lid, two side pockets and a rolled orange mat on top; pivot at its centre.
  backpack(o) {
    const c = o.color || '#2F7F5C', g = grp(at(box(0.36, 0.5, 0.2, c, { outline: 0.006 }), 0, 0, 0), at(box(0.38, 0.12, 0.22, '#25624A'), 0, 0.22, 0.0), at(box(0.07, 0.2, 0.12, '#25624A'), -0.21, -0.1, 0), at(box(0.07, 0.2, 0.12, '#25624A'), 0.21, -0.1, 0));
    g.add(at(cyl(0.06, 0.06, 0.44, o.mat || '#E8742A', 10, { outline: 0.004 }), 0, 0.33, 0, 0, 0, PI / 2));
    return g;
  },

  // A wall map of France (front +Z, o.w 1.5 x o.h 1.2): sea, the hexagon in sand, Paris, a compass rose with its N at the top left; o.cross t: a red cross
  // drawn over the rose (0.25 s); o.arrow [t0, t1]: a fat red arrow drawn from the rose to the pin o.pin [u, v] (fractions of the map; his building, a
  // little head with black hair) with the word o.word ('NORD') at its tip; o.rotate [[t, deg]]: the map turns on the wall (0.5 s ease-in-out from the
  // previous angle) so that the pin comes to the top.
  mapFrance(o) {
    const w = o.w ?? 1.5, h = o.h ?? 1.2, g = grp(), spin = grp(); g.add(spin);
    spin.add(at(box(w + 0.08, h + 0.08, 0.04, '#5A3A28', { outline: 0.008 }), 0, 0, -0.025));
    const scr = liveCanvas(w, h, 512, false); scr.pl.position.z = 0.001; spin.add(scr.pl);
    const FR = [[0.42, 0.06], [0.58, 0.1], [0.8, 0.22], [0.84, 0.34], [0.78, 0.5], [0.86, 0.72], [0.74, 0.9], [0.55, 0.86], [0.42, 0.96], [0.24, 0.88], [0.27, 0.62], [0.12, 0.42], [0.04, 0.33], [0.2, 0.3], [0.34, 0.18]];
    const pin = o.pin || [0.62, 0.66], cr = list(o.cross)[0], ar = o.arrow, rot = o.rotate || [];
    g.userData.update = t => {
      let deg = 0, prev = 0; for (const [a, d] of rot) { if (t >= a) { const u = clamp01((t - a) / 0.5); deg = prev + (d - prev) * ease.inOut(u); prev = d; } } spin.rotation.z = deg * PI / 180;
      const kc = cr == null ? 0 : clamp01((t - cr) / 0.25), ka = !ar ? 0 : clamp01((t - ar[0]) / Math.max(0.05, ar[1] - ar[0]));
      scr.redraw(`${Math.round(kc * 20)}_${Math.round(ka * 30)}`, (c, W, H) => {
        c.fillStyle = '#9CC9E2'; c.fillRect(0, 0, W, H); c.strokeStyle = 'rgba(255,255,255,0.35)'; c.lineWidth = 2; for (let i = 1; i < 8; i++) { c.beginPath(); c.moveTo(W * i / 8, 0); c.lineTo(W * i / 8, H); c.stroke(); c.beginPath(); c.moveTo(0, H * i / 8); c.lineTo(W, H * i / 8); c.stroke(); }
        c.beginPath(); FR.forEach(([x, y], i) => { const X = W * (0.12 + 0.82 * x), Y = H * (0.04 + 0.9 * y); if (i) c.lineTo(X, Y); else c.moveTo(X, Y); }); c.closePath(); c.fillStyle = '#EAD9A8'; c.fill(); c.strokeStyle = '#8A6A3A'; c.lineWidth = W * 0.006; c.stroke();
        const px = W * (0.12 + 0.82 * 0.55), py = H * (0.04 + 0.9 * 0.3); c.fillStyle = '#1B1B1E'; c.beginPath(); c.arc(px, py, W * 0.01, 0, TAU); c.fill(); c.font = `bold ${H * 0.04}px Arial`; c.textAlign = 'left'; c.fillText('PARIS', px + W * 0.015, py - H * 0.01);
        const rx = W * 0.12, ry = H * 0.18, rr = W * 0.08;   // the compass rose
        c.fillStyle = '#1B2A6B'; c.beginPath(); c.moveTo(rx, ry - rr); c.lineTo(rx + rr * 0.22, ry); c.lineTo(rx, ry + rr); c.lineTo(rx - rr * 0.22, ry); c.closePath(); c.fill(); c.beginPath(); c.moveTo(rx - rr, ry); c.lineTo(rx, ry + rr * 0.22); c.lineTo(rx + rr, ry); c.lineTo(rx, ry - rr * 0.22); c.closePath(); c.fill();
        c.fillStyle = '#1B2A6B'; c.font = `900 ${H * 0.07}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('N', rx, ry - rr - H * 0.05);
        if (kc > 0) { c.strokeStyle = '#D3202A'; c.lineWidth = W * 0.016; c.lineCap = 'round'; const d = rr * 1.25; c.beginPath(); c.moveTo(rx - d, ry - d - H * 0.03); c.lineTo(rx - d + 2 * d * Math.min(1, kc * 2), ry - d - H * 0.03 + 2 * d * Math.min(1, kc * 2)); c.stroke();
          if (kc > 0.5) { const k2 = (kc - 0.5) * 2; c.beginPath(); c.moveTo(rx + d, ry - d - H * 0.03); c.lineTo(rx + d - 2 * d * k2, ry - d - H * 0.03 + 2 * d * k2); c.stroke(); } }
        const PX = W * (0.12 + 0.82 * pin[0]), PY = H * (0.04 + 0.9 * pin[1]);
        if (ka > 0) { const x0 = rx + rr * 0.6, y0 = ry + rr * 0.6, x1 = x0 + (PX - x0) * ka, y1 = y0 + (PY - y0) * ka; c.strokeStyle = '#D3202A'; c.lineWidth = W * 0.02; c.lineCap = 'round'; c.beginPath(); c.moveTo(x0, y0); c.lineTo(x1, y1); c.stroke();
          if (ka >= 1) { const a = Math.atan2(PY - y0, PX - x0), L = W * 0.06; c.fillStyle = '#D3202A'; c.beginPath(); c.moveTo(PX, PY); c.lineTo(PX - L * Math.cos(a - 0.45), PY - L * Math.sin(a - 0.45)); c.lineTo(PX - L * Math.cos(a + 0.45), PY - L * Math.sin(a + 0.45)); c.closePath(); c.fill();
            c.font = `900 ${H * 0.09}px Arial`; c.fillStyle = '#D3202A'; c.textAlign = 'center'; c.fillText(o.word || 'NORD', PX, PY + H * 0.1); } }
        c.fillStyle = '#E3B98C'; c.fillRect(PX - W * 0.025, PY - H * 0.045, W * 0.05, H * 0.06); c.fillStyle = '#17181B'; c.fillRect(PX - W * 0.027, PY - H * 0.058, W * 0.054, H * 0.02); c.strokeStyle = '#1B1B1E'; c.lineWidth = 2; c.strokeRect(PX - W * 0.025, PY - H * 0.045, W * 0.05, H * 0.06);
        c.fillStyle = '#1B1B1E'; c.fillRect(PX - W * 0.012, PY - H * 0.025, W * 0.005, H * 0.008); c.fillRect(PX + W * 0.007, PY - H * 0.025, W * 0.005, H * 0.008);
      });
    };
    g.userData.update(0); return g;
  },

  // A globe on a stand (pivot at the foot, o.r 0.32 m): blue seas with sandy continents, a white polar cap at the top, and on the pole a tiny block of
  // flats with a little red flag (o.house, default true); o.spin [[t0, t1, turns]]: it turns about its vertical axis with an ease-out and stops so that
  // the house faces +Z (o.face0, rad: where it faces before).
  globe(o) {
    const r = o.r ?? 0.32, g = grp(at(cyl(0.14, 0.18, 0.05, '#5A3A28', 12, { outline: 0.005 }), 0, 0.025, 0), at(cyl(0.02, 0.02, 0.28, '#C9A24A', 6), 0, 0.17, 0));
    const ball = grp(); ball.position.y = 0.32 + r; g.add(ball);
    g.add(at(new THREE.Mesh(new THREE.TorusGeometry(r * 1.08, 0.01, 4, 32, PI * 1.2), mat('#C9A24A')), 0, 0.32 + r, 0, 0, PI / 2, -PI * 0.1));
    const cv = document.createElement('canvas'); cv.width = 512; cv.height = 256; const c = cv.getContext('2d'); c.fillStyle = '#4F93C8'; c.fillRect(0, 0, 512, 256); c.fillStyle = '#E3D29A';
    for (let i = 0; i < 9; i++) { const x = rnd(i) * 512, y = 70 + rnd(i + 3) * 120, s = 30 + rnd(i + 7) * 50; c.beginPath(); for (let j = 0; j < 9; j++) { const a = j * TAU / 9, rr = s * (0.6 + 0.5 * rnd(i * 9 + j)); if (j) c.lineTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr * 0.7); else c.moveTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr * 0.7); } c.closePath(); c.fill(); }
    c.fillStyle = '#F8FAFC'; c.fillRect(0, 0, 512, 26);
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
    ball.add(new THREE.Mesh(new THREE.SphereGeometry(r, 28, 18), new THREE.MeshLambertMaterial({ map: tex })));
    if (o.house !== false) { const hs = r * 0.16, hg = grp(at(box(hs, hs * 1.4, hs * 0.8, '#F1E6CF', { outline: 0.003 }), 0, hs * 0.7, 0), at(box(hs * 1.1, hs * 0.12, hs * 0.9, '#B5302A'), 0, hs * 1.45, 0));
      for (const yy of [0.35, 0.75, 1.1]) hg.add(at(box(hs * 0.7, hs * 0.14, 0.004, '#5C8FA8'), 0, hs * yy, hs * 0.41));
      hg.add(at(cyl(0.003, 0.003, hs * 1.4, '#3A3D44', 4, { pivot: 'bottom' }), hs * 0.4, hs * 1.5, 0), at(box(hs * 0.5, hs * 0.3, 0.003, '#D3202A'), hs * 0.65, hs * 2.7, 0));
      hg.position.y = r * 0.985; ball.add(hg); }
    const sp = o.spin || [], f0 = o.face0 ?? 2.4;
    g.userData.update = t => { let a = f0; for (const [t0, t1, turns] of sp) { if (t < t0) break; const u = clamp01((t - t0) / Math.max(0.05, t1 - t0)); a = f0 + (TAU * (turns ?? 2) - f0) * ease.out(u) + (u >= 1 ? 0.06 * wob(t - t1, 14, 5) : 0); } ball.rotation.y = a; };
    g.userData.update(0); return g;
  },

  // A small sailboat on a road trailer (front +X, o.len 3.2 m): white hull with a blue band, a mast, a white sail, a little pennant, two wheels.
  sailboat(o) {
    const L = o.len ?? 3.2, g = grp(at(box(L, 0.5, 1.1, '#F4F2EA', { outline: 0.01, taper: { x: 0.7, z: 0.55 }, taperAxis: 'x' }), 0, 0.85, 0), at(box(L * 0.9, 0.1, 1.12, '#2F5E8C'), 0, 0.98, 0));
    for (const z of [-0.5, 0.5]) g.add(at(cyl(0.22, 0.22, 0.12, P.ink, 12), -0.2, 0.22, z, PI / 2), at(box(0.06, 0.32, 0.06, '#7A8088'), -0.2, 0.45, z * 0.9));
    g.add(at(box(L * 0.8, 0.06, 0.08, '#7A8088'), 0, 0.6, 0), at(cyl(0.03, 0.035, 3.0, '#C9CDD3', 6, { pivot: 'bottom' }), 0.2, 1.05, 0));
    const sail = new THREE.Shape(); sail.moveTo(0, 0); sail.lineTo(-1.3, 0); sail.lineTo(-0.05, 2.6); sail.closePath();
    g.add(at(new THREE.Mesh(new THREE.ShapeGeometry(sail), new THREE.MeshLambertMaterial({ color: '#FBFAF4', side: THREE.DoubleSide })), 0.18, 1.2, 0.02));
    g.add(at(box(0.32, 0.18, 0.01, o.pennant || '#D3202A'), 0.36, 3.95, 0));
    return g;
  },

  // A small propeller plane (front +X, about 6.5 m long, 8 m across the wing): a white fuselage with a red band, a high wing, the tail, three wheels and a
  // propeller that turns (o.prop rev/s, default 6; 0 stops it). Pivot under the wheels.
  propPlane(o) {
    const g = grp(), red = o.color || '#C8202A';
    g.add(at(box(5.2, 1.1, 1.1, '#F4F2EA', { outline: 0.012, taper: { x: 0.45, z: 0.6 }, taperAxis: 'x' }), -0.4, 1.35, 0), at(box(5.0, 0.18, 1.12, red), -0.5, 1.25, 0));
    g.add(at(box(1.4, 0.12, 8.2, '#F4F2EA', { outline: 0.01 }), 0.6, 1.98, 0), at(box(0.9, 0.08, 2.6, '#F4F2EA', { outline: 0.008 }), -2.9, 1.5, 0), at(box(0.9, 1.1, 0.08, red, { outline: 0.008 }), -2.95, 2.0, 0));
    g.add(at(box(1.0, 0.45, 1.0, '#9CC9E2', { noGrain: true }), 0.9, 1.75, 0), at(cyl(0.22, 0.25, 0.3, '#3A3D44', 10), 2.25, 1.35, 0, 0, 0, PI / 2));
    for (const [x, z] of [[1.4, 0], [0.0, -0.8], [0.0, 0.8]]) g.add(at(cyl(0.22, 0.22, 0.14, P.ink, 10), x, 0.22, z, PI / 2), at(box(0.06, 0.6, 0.06, '#7A8088'), x, 0.6, z));
    const prop = grp(at(box(0.06, 1.6, 0.12, '#2A2C31'), 0, 0, 0)); prop.position.set(2.42, 1.35, 0); g.add(prop);
    const rs = o.prop ?? 6; g.userData.update = t => { prop.rotation.x = t * rs * TAU; }; g.userData.update(0); return g;
  },
};
