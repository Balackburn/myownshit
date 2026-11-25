// « La pelle » (story 100, cycle 53): his friends bury this man in the sand up to the neck, and for the town hall someone under the ground is
// buried, so dead. Digging him out would be an exhumation (six months for the permit), so the State runs the whole funeral round a live man:
// a headstone that gives him the only shade on the beach, a wreath and a replacement from his boss, his wife on the next towel, the friends
// inherit his car, the beach becomes a cemetery with gates (spades forbidden), the holidaymakers tan in mourning; only the tax office does not
// believe he is dead; the permit comes, he refuses to come out and asks for a perpetual plot. In the shade.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
// Running gags drawn here: the crabs' sand wall (plCrabWall: rows of stepped blocks in a horseshoe round his head, open to the front, a row popping
// in at each time of o.add; o.mausoleum: the finished crab-built mausoleum) and the tan (two pale ovals with his own eyes drawn in, plOvals,
// revealed when the sunglasses, plShades, slide up). No symbol, no text, no plaque on the headstone (plHeadstone).
import * as THREE from 'three';
import { box, cyl, sphere, mat } from './style.js';
import { grp, at, canvasPlane, rod, inst } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = (x, c = 2.2) => { const u = clamp01(x); return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const lerp = (a, b, u) => a + (b - a) * u;
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
// [[t, v], ...] -> v at t, smoothstep between keys (a key [t, v, 'lin'] makes its segment linear)
const keyAt = (K, t, d = 0) => {
  if (!K || !K.length) return d;
  if (t <= K[0][0]) return K[0][1];
  for (let i = 1; i < K.length; i++) if (t < K[i][0]) { const u = (t - K[i - 1][0]) / Math.max(1e-6, K[i][0] - K[i - 1][0]); return lerp(K[i - 1][1], K[i][1], K[i][2] === 'lin' ? u : smooth(u)); }
  return K[K.length - 1][1];
};
// a damped wobble summed over [[t0, amp, freq, decay], ...]
const rattle = (R, t) => { let s = 0; for (const [t0, amp, f, dk] of R || []) { const u = t - t0; if (u > 0) s += amp * Math.sin(u * (f ?? 18)) * Math.exp(-u * (dk ?? 3.5)); } return s; };
const INK = '#1B1E2A';
const SAND = '#E6CF94';
const L = (c, o = {}) => new THREE.MeshLambertMaterial({ color: c, ...o });
const B = (c, o = {}) => new THREE.MeshBasicMaterial({ color: c, ...o });
const tex = cv => { const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t; };
const canvas = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
const fitText = (c, s, x, y, maxW, maxH, weight = 900, family = 'Arial') => { let fs = maxH; c.font = `${weight} ${fs}px ${family}`; const w = c.measureText(s).width; if (w > maxW) { fs *= maxW / w; c.font = `${weight} ${fs}px ${family}`; } c.fillText(s, x, y); };
const flatDisc = (r, c, y, seg = 32) => { const m = new THREE.Mesh(new THREE.CircleGeometry(r, seg).rotateX(-PI / 2), c); m.position.y = y; m.receiveShadow = true; return m; };
// a painted ground layer drawn without depth test after the field (like roadStrip): no flicker with the field under it
// (always opaque: a transparent layer would be drawn after the actors, over them)
const groundLayer = (w, d, color, x, z, order) => {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, d).rotateX(-PI / 2), new THREE.MeshLambertMaterial({ color, depthTest: false, depthWrite: false }));
  m.position.set(x, 0.01, z); m.renderOrder = order; m.receiveShadow = true; return m;
};

export const PELLE_PROPS = {

  // ---------------------------------------------------------------- the beach (put on the grassland set with grass: SAND)
  // The sea from z o.shore (-8) to the horizon toward -Z: a teal sheet, a darker wet-sand band, a foam line that laps in and out, three lighter swell
  // bands rolling in; painted without depth test after the field. Hides the grassland's trees (none on a beach). o.sunset: a warm pink-orange sea,
  // a low sun disc over the horizon (o.sunX) and its glitter path, for the evening shots; o.sea, o.wet colours
  plWorld(o) {
    const g = grp(), S = o.shore ?? -8, ss = !!o.sunset;
    const seaC = o.sea || (ss ? '#E59A86' : '#3FA9BE'), wetC = o.wet || (ss ? '#C9A27E' : '#CDB079'), foamC = ss ? '#FFE6D2' : '#F6FBFA', swellC = ss ? '#F2BC98' : '#6CC3D1';
    g.add(groundLayer(4000, 3, wetC, 0, S + 1.2, -1.8), groundLayer(4000, 2000, seaC, 0, S - 1000, -1.7));
    const foam = groundLayer(4000, 0.45, foamC, 0, S + 0.1, -1.5), foam2 = groundLayer(4000, 0.25, foamC, 0, S - 0.6, -1.5);
    const swells = [-4, -9, -16, -26].map((dz, i) => { const m = groundLayer(4000, 0.7 + i * 0.35, swellC, 0, S + dz, -1.6); g.add(m); return m; });
    g.add(foam, foam2);
    let sun = null, glit = [];
    if (ss) {
      const N = 128, cv = canvas(N, N), c = cv.getContext('2d'), gr = c.createRadialGradient(N / 2, N / 2, 0, N / 2, N / 2, N / 2);
      gr.addColorStop(0, '#FFF6D8'); gr.addColorStop(0.3, '#FFE2A0'); gr.addColorStop(0.55, 'rgba(255,170,110,0.55)'); gr.addColorStop(1, 'rgba(255,140,90,0)'); c.fillStyle = gr; c.fillRect(0, 0, N, N);
      sun = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: tex(cv), transparent: true, depthWrite: false, fog: false, toneMapped: false }));
      sun.scale.setScalar(o.sunSize ?? 90); sun.position.set(o.sunX ?? 0, o.sunY ?? 22, -900); sun.renderOrder = -1; g.add(sun);
      for (let i = 0; i < 26; i++) { const m = groundLayer(lerp(30, 3, i / 25) * (0.6 + hsh(i) * 0.8), 1.2 + i * 0.1, '#FFE8B8', (o.sunX ?? 0) * (1 - i / 26) + (hsh(i + 3) - 0.5) * 3, -880 + i * 32 + S, -1.55); g.add(m); glit.push(m); }
    }
    g.userData.update = t => {
      foam.position.z = S + 0.1 + 0.35 * Math.sin(t * 1.3); foam2.position.z = S - 0.6 + 0.3 * Math.sin(t * 1.3 - 0.9);
      swells.forEach((m, i) => { m.position.z = S + [-4, -9, -16, -26][i] + ((t * 0.9 + i * 1.7) % 4); });
      glit.forEach((m, i) => { m.visible = Math.sin(t * 5 + i * 1.9) > -0.4; });
      let rt = g; while (rt.parent) rt = rt.parent;
      if (rt !== g && !g.userData._hid) { rt.traverse(c => { if (c.name === 'tree') c.visible = false; }); g.userData._hid = 1; }
    };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the seafront (facing -Z toward the beach; pivot at the middle of the kerb)
  // A row of pastel buildings (o.n, 3 to 5 storeys, windows, balconies, flat roofs), the road before them (o.road, a strip painted over the sand
  // with dashes), the promenade's low white wall on the beach side; o.lit: the windows glow warm (evening); o.hide [[x0, x1], ...] leaves gaps
  plSeafront(o) {
    const g = grp(), n = o.n ?? 9, W = o.bw ?? 7.5, lit = o.lit ?? 0, cols = o.colors || ['#F2C9A0', '#F4E2B0', '#B9D8E0', '#F2B8B0', '#E9E4D6', '#C9DDB8', '#F6D58E'];
    const winC = lit ? '#FFC46A' : '#6E8BA8', winM = lit ? mat(winC, { emissive: '#FF9A3A', noGrain: true }) : mat(winC);
    for (let i = 0; i < n; i++) {
      const x = (i - (n - 1) / 2) * W, fl = 3 + Math.floor(hsh(i + (o.seed ?? 1)) * 3), H = fl * 3.0 + 1, c = cols[i % cols.length];
      if ((o.hide || []).some(([a, b]) => x > a && x < b)) continue;
      const b = grp(at(box(W - 0.3, H, 9, c, { pivot: 'bottom', outline: 0.004 }), 0, 0, 4.5), at(box(W - 0.1, 0.4, 9.2, '#E9E4D6', { pivot: 'bottom' }), 0, H, 4.5));
      const wl = [];
      for (let f = 0; f < fl; f++) for (let j = 0; j < 3; j++) wl.push([(j - 1) * 2.2, 2.2 + f * 3.0, -0.02, 0, 0, 0, 1, 1, 1]);
      b.add(inst(new THREE.BoxGeometry(1.1, 1.5, 0.08), winM, wl));
      const bl = []; for (let f = 1; f < fl; f++) for (let j = 0; j < 3; j++) bl.push([(j - 1) * 2.2, 1.35 + f * 3.0, -0.35, 0, 0, 0, 1, 1, 1]);
      if (bl.length) b.add(inst(new THREE.BoxGeometry(1.5, 0.12, 0.7), mat('#F4F4F0'), bl));
      b.add(at(box(W - 0.3, 0.9, 0.12, i % 2 ? '#2F7F8C' : '#C8463A', { outline: 0.004 }), 0, 0.45 + 2.6 - 0.45, -0.1));
      g.add(at(b, x, 0, o.road === false ? 0 : 9));
    }
    if (o.road !== false) {
      g.add(groundLayer(n * W + 40, 7, '#7C7E84', 0, 4.6, -1.4), groundLayer(n * W + 40, 2.2, '#D9D2C2', 0, 8.6, -1.35));
      for (let i = -30; i <= 30; i++) g.add(groundLayer(1.6, 0.14, '#F2F2EE', i * 3.6, 4.6, -1.3));
    }
    if (o.wall !== false) { const ww = n * W + 40, [ga, gb] = o.gap || [0, 0];
      if (gb > ga) { const lw = ga + ww / 2, rw = ww / 2 - gb; g.add(at(box(lw, 0.55, 0.35, '#F2EFE6', { pivot: 'bottom', outline: 0.004 }), -ww / 2 + lw / 2, 0, 0.6), at(box(rw, 0.55, 0.35, '#F2EFE6', { pivot: 'bottom', outline: 0.004 }), gb + rw / 2, 0, 0.6)); }
      else g.add(at(box(ww, 0.55, 0.35, '#F2EFE6', { pivot: 'bottom', outline: 0.004 }), 0, 0, 0.6)); }
    g.userData.update = () => {};
    return g;
  },

  // ---------------------------------------------------------------- the sand mound round his neck (pivot at his neck, on the sand)
  // A smooth low dome (o.r 0.62, o.h 0.17) a shade lighter than the beach, the flat pats of the spades on it, and a collar that hides the base of
  // his head; o.pat [[t, x, z], ...]: a spade pat lands there at t (a little squash ring)
  plMound(o) {
    const g = grp(), R = o.r ?? 0.62, Hh = o.h ?? 0.17, c = o.color || '#EBD7A2';
    const d = new THREE.Mesh(new THREE.SphereGeometry(1, 28, 10, 0, TAU, 0, PI / 2), L(c)); d.scale.set(R, Hh, R); d.castShadow = d.receiveShadow = true; g.add(d);
    const col = new THREE.Mesh(new THREE.SphereGeometry(1, 20, 8, 0, TAU, 0, PI / 2), L(c)); col.scale.set(o.cw ?? 0.24, o.ch ?? 0.12, o.cd ?? 0.17); col.position.y = (o.ct ?? 0.2) - (o.ch ?? 0.12); col.castShadow = col.receiveShadow = true; g.add(col);
    for (let i = 0; i < 7; i++) { const a = i / 7 * TAU + 0.4, rr = R * (0.45 + 0.25 * hsh(i)); const p = new THREE.Mesh(new THREE.CircleGeometry(0.075, 10).rotateX(-PI / 2), L('#F2E2B4')); p.position.set(Math.cos(a) * rr, Hh * Math.sqrt(Math.max(0, 1 - (rr / R) ** 2)) + 0.004, Math.sin(a) * rr); p.rotation.set(0, 0, 0); g.add(p); }
    const pats = (o.pat || []).map(([t0, x, z]) => { const m = new THREE.Mesh(new THREE.RingGeometry(0.03, 0.06, 14).rotateX(-PI / 2), B('#F8EED0', { transparent: true, opacity: 0 })); m.position.set(x, Hh * Math.sqrt(Math.max(0, 1 - (Math.hypot(x, z) / R) ** 2)) + 0.01, z); g.add(m); return [m, t0]; });
    g.userData.update = t => { for (const [m, t0] of pats) { const u = (t - t0) / 0.35; m.visible = u > 0 && u < 1; if (m.visible) { m.scale.setScalar(1 + u * 2.4); m.material.opacity = 0.9 * (1 - u); } } };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the crabs' sand wall round his head (pivot at his neck, on the mound)
  // Rows of sand blocks in a horseshoe of radius o.R (0.34) open toward +Z (his face) by o.open (1.0 rad each side), each row a little smaller and
  // stepped in; o.rows rows at the start, one more row pops (outBack) at each time in o.add; o.y0: the foot of the wall (on the mound). o.mausoleum:
  // the finished mausoleum instead: high crenellated walls, two round corner towers with cone roofs beside his face, a lintel and a pediment above
  // his head, a shell on the pediment, steps of sand blocks in front (o.H its wall height, 0.7)
  plCrabWall(o) {
    const g = grp(), R = o.R ?? 0.36, op = o.open ?? 1.0, bh = o.bh ?? 0.068, y0 = o.y0 ?? 0.1, c1 = o.color || '#E2C686', c2 = '#D4B470';
    const rowAt = i => { const r = R - i * 0.008, n = Math.max(6, Math.round((TAU - 2 * op) * r / 0.1)), list = [];
      for (let j = 0; j < n; j++) { const a = op + (TAU - 2 * op) * (j + 0.5 * (i % 2)) / n; if (a > TAU - op + 1e-3) continue; list.push([Math.sin(a) * r, y0 + bh * (i + 0.5), Math.cos(a) * r, 0, a, 0, 1 + 0.06 * (hsh(i * 31 + j) - 0.5), 1, 1]); }
      const m = inst(new THREE.BoxGeometry(0.094, bh * 0.96, 0.085), mat(i % 2 ? c2 : c1), list); return m; };
    if (o.mausoleum) {
      const H = o.H ?? 0.72, nr = Math.round(H / bh);
      for (let i = 0; i < nr; i++) g.add(rowAt(i));
      const top = []; for (let j = 0; j < 22; j++) { const a = op + (TAU - 2 * op) * (j + 0.5) / 22; if (j % 2) continue; top.push([Math.sin(a) * (R - nr * 0.008), y0 + H + 0.04, Math.cos(a) * (R - nr * 0.008), 0, a, 0, 1, 1, 1]); }
      g.add(inst(new THREE.BoxGeometry(0.09, 0.08, 0.09), mat(c1), top));
      for (const sd of [-1, 1]) { const x = Math.sin(op) * (R + 0.04) * sd, z = Math.cos(op) * (R + 0.04);
        g.add(at(cyl(0.085, 0.1, H + 0.22, c1, 10, { pivot: 'bottom', outline: 0.01 }), x, y0, z));
        for (let k = 0; k < 5; k++) g.add(at(box(0.05, 0.05, 0.03, c2), x + Math.sin(k / 5 * TAU) * 0.085, y0 + H + 0.24, z + Math.cos(k / 5 * TAU) * 0.085, 0, k / 5 * TAU, 0));
        const cone = new THREE.Mesh(new THREE.ConeGeometry(0.11, 0.24, 10), mat('#D9BB78')); cone.position.set(x, y0 + H + 0.38, z); cone.castShadow = true; g.add(cone); }
      const sx = Math.sin(op) * (R + 0.04), zl = Math.cos(op) * (R + 0.04);
      g.add(at(box(sx * 2 + 0.12, 0.1, 0.16, c1, { outline: 0.01 }), 0, y0 + H + 0.05, zl));
      const tri = new THREE.Shape([new THREE.Vector2(-sx - 0.06, 0), new THREE.Vector2(sx + 0.06, 0), new THREE.Vector2(0, 0.26)].map(v => v));
      const ped = new THREE.Mesh(new THREE.ExtrudeGeometry(tri, { depth: 0.12, bevelEnabled: false }), mat(c2)); ped.position.set(0, y0 + H + 0.1, zl - 0.06); ped.castShadow = true; g.add(ped);
      const shell = grp(); for (let k = 0; k < 7; k++) shell.add(at(box(0.016, 0.09, 0.012, '#F4E8D0'), Math.sin((k - 3) * 0.32) * 0.03, 0.04 + Math.cos((k - 3) * 0.32) * 0.01, 0, 0, 0, -(k - 3) * 0.32));
      shell.position.set(0, y0 + H + 0.16, zl + 0.07); g.add(shell);
      // (stills 1) two low rows of steps well in front of the opening: three rows close in hid his chin and mouth from a low camera
      const steps = []; for (let i = 0; i < 2; i++) for (let j = -2 + i; j <= 2 - i; j++) steps.push([j * 0.1, 0.02 + bh * (i + 0.5), zl + 0.48 - i * 0.07, 0, 0, 0, 1, 1, 1]);
      g.add(inst(new THREE.BoxGeometry(0.095, bh * 0.95, 0.08), mat(c1), steps));
      return g;
    }
    const rows0 = o.rows ?? 0, add = o.add || [], N = rows0 + add.length, rows = [];
    for (let i = 0; i < N; i++) { const m = rowAt(i), w = grp(m); g.add(w); rows.push(w); }
    g.userData.update = t => rows.forEach((w, i) => { if (i < rows0) { w.visible = true; w.scale.setScalar(1); return; } const u = (t - add[i - rows0]) / 0.22; w.visible = u > 0; w.scale.set(1, Math.max(0.01, outBack(u, 2.6)), 1); w.position.y = 0; });
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a plain grey headstone (pivot under its middle, front +Z): no symbol, no text
  plHeadstone(o) {
    const W = o.w ?? 0.82, H = o.h ?? 1.3, T = 0.16, stone = o.color || '#A9ABB0', g = grp(), sw = grp(); g.add(sw);
    sw.add(at(box(W, H - W / 2, T, stone, { pivot: 'bottom', outline: 0.008 }), 0, 0.16, 0));
    const arch = new THREE.Mesh(new THREE.CylinderGeometry(W / 2, W / 2, T, 28, 1, false, -PI / 2, PI), mat(stone)); arch.rotation.x = -PI / 2; arch.position.set(0, 0.16 + H - W / 2, 0); arch.castShadow = true; sw.add(arch);
    sw.add(at(box(W * 1.3, 0.16, T * 2.2, '#9C9EA3', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0.04));
    sw.add(at(box(W * 0.86, 0.012, 0.01, '#8E9095'), 0, 0.3, T / 2 + 0.003));
    g.userData.update = t => { const r = rattle(o.rattle, t); sw.rotation.z = r; sw.scale.y = 1 - Math.abs(r) * 0.6; };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- big wraparound sunglasses (attach to the head joint at eye height)
  // Two dark lenses (o.op opacity: his eyes show dimly behind), thick black frames, a bridge, arms back to the ears; o.w the width (0.34), o.tilt
  // their roll (rad, to follow his painted eyes); o.lift [[t, u], ...]: u 1 pushes them up onto his hair, tipped back; o.dip [[t, d], ...] slides
  // them down his face by d (m); o.wob [[t0, amp, f, dk], ...]: a wobble on a take; o.y0 their height on the head joint (m) and o.sq
  // [[t, sx, sy], ...] the head's own squash at t (an attached prop does not inherit the joint's scale), so they ride on his eyes
  plShades(o) {
    const g = grp(), inner = grp(), s = o.w ?? 0.34; g.add(inner);
    const lensM = new THREE.MeshPhongMaterial({ color: '#1A2030', shininess: 80, transparent: true, opacity: o.op ?? 0.86, depthWrite: true });
    const lensShape = (w, h) => { const sh = new THREE.Shape(), r = h * 0.42; sh.moveTo(-w / 2 + r, h / 2); sh.lineTo(w / 2 - r * 0.3, h / 2); sh.quadraticCurveTo(w / 2, h / 2, w / 2, h / 2 - r * 0.6); sh.lineTo(w / 2 - r * 0.3, -h / 2 + r); sh.quadraticCurveTo(w / 2 - r * 0.6, -h / 2, w / 2 - r * 1.4, -h / 2); sh.lineTo(-w / 2 + r, -h / 2); sh.quadraticCurveTo(-w / 2, -h / 2, -w / 2, -h / 2 + r); sh.lineTo(-w / 2, h / 2 - r); sh.quadraticCurveTo(-w / 2, h / 2, -w / 2 + r, h / 2); return sh; };
    const lw = s * 0.4, lh = s * 0.27;
    for (const sd of [-1, 1]) {
      const shp = lensShape(lw, lh), lens = new THREE.Mesh(new THREE.ShapeGeometry(shp), lensM); lens.scale.x = sd; lens.position.set(sd * s * 0.245, 0, 0.012); inner.add(lens);
      const rim = new THREE.Mesh(new THREE.ExtrudeGeometry(shp, { depth: 0.012, bevelEnabled: false }), B('#0B0C10')); rim.scale.set(sd * 1.12, 1.16, 1); rim.position.set(sd * s * 0.245, 0, -0.002); inner.add(rim);
      const gl = new THREE.Mesh(new THREE.PlaneGeometry(lw * 0.18, lh * 0.5), B('#FFFFFF', { transparent: true, opacity: 0.55 })); gl.position.set(sd * s * 0.245 - lw * 0.22, lh * 0.12, 0.016); gl.rotation.z = -0.5; inner.add(gl);
      inner.add(at(box(0.012, 0.02, 0.2, '#0B0C10'), sd * s * 0.49, lh * 0.25, -0.1));
    }
    inner.add(at(box(s * 0.12, 0.022, 0.014, '#0B0C10'), 0, lh * 0.22, 0.006));
    inner.rotation.z = o.tilt ?? 0;
    const sqx = o.sq ? o.sq.map(q => [q[0], q[1]]) : null, sqy = o.sq ? o.sq.map(q => [q[0], q[2]]) : null;
    g.userData.update = t => { const u = keyAt(o.lift, t, 0), d = keyAt(o.dip, t, 0), w = rattle(o.wob, t), sx = keyAt(sqx, t, 1), sy = keyAt(sqy, t, 1);
      inner.position.set(0, (o.y0 ?? 0) * sy - d + u * 0.27, -u * 0.07); inner.rotation.set(-u * 1.0, 0, (o.tilt ?? 0) + w); inner.scale.set(sx * (1 + Math.abs(w) * 1.5), 1 + Math.abs(w) * 1.5, 1); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the two pale ovals of the sunglasses tan, his own eyes drawn in (attach to the head
  // joint on the face, under plShades): a soft pale oval round each eye in o.color (his untanned skin), eyes drawn in the hero's heavy-lidded style
  // with pupils; o.close [[t, u], ...] u 1: closed in blissful arcs; o.eyes [[lx, ly], [rx, ry]] the eye centres (m, in the head frame); o.look [gx, gy]
  plOvals(o) {
    const g = grp(), E = o.eyes || [[-0.075, 0.33], [0.075, 0.31]], ow = o.ow ?? 0.12, oh = o.oh ?? 0.085, tl = o.tilt ?? 0;
    const mk = (state) => { const N = 256, cv = canvas(N, Math.round(N * oh / ow)), c = cv.getContext('2d'), Wc = cv.width, Hc = cv.height;
      const gr = c.createRadialGradient(Wc / 2, Hc / 2, Hc * 0.2, Wc / 2, Hc / 2, Wc / 2); gr.addColorStop(0, o.color || '#F0C49A'); gr.addColorStop(0.78, o.color || '#F0C49A'); gr.addColorStop(1, 'rgba(240,196,154,0)');
      c.save(); c.scale(1, Hc / Wc); c.fillStyle = gr; c.beginPath(); c.arc(Wc / 2, Wc / 2, Wc / 2, 0, TAU); c.fill(); c.restore();
      c.lineCap = 'round'; c.strokeStyle = '#1A1412';
      if (state === 'open') {
        c.fillStyle = '#FFFFFF'; c.beginPath(); c.ellipse(Wc / 2, Hc * 0.55, Wc * 0.27, Hc * 0.26, 0, 0, TAU); c.fill();
        c.fillStyle = '#1A1412'; c.beginPath(); c.arc(Wc / 2 + Wc * 0.03 * (o.look ? o.look[0] : 0), Hc * 0.58 + Hc * 0.05 * (o.look ? o.look[1] : 0), Hc * 0.17, 0, TAU); c.fill();
        c.fillStyle = o.lidColor || o.color || '#F0C49A'; c.beginPath(); c.ellipse(Wc / 2, Hc * 0.28, Wc * 0.31, Hc * 0.22, 0, 0, TAU); c.fill();
        c.lineWidth = Hc * 0.07; c.beginPath(); c.ellipse(Wc / 2, Hc * 0.55, Wc * 0.27, Hc * 0.26, 0, PI * 1.08, PI * 1.92); c.stroke();
        c.lineWidth = Hc * 0.05; c.beginPath(); c.ellipse(Wc / 2, Hc * 0.55, Wc * 0.27, Hc * 0.26, 0, PI * 0.15, PI * 0.85); c.stroke();
      } else { c.lineWidth = Hc * 0.08; c.beginPath(); c.ellipse(Wc / 2, Hc * 0.42, Wc * 0.26, Hc * 0.22, 0, PI * 0.1, PI * 0.9); c.stroke(); }
      const m = new THREE.Mesh(new THREE.PlaneGeometry(ow, oh), new THREE.MeshBasicMaterial({ map: tex(cv), transparent: true, depthWrite: false })); m.renderOrder = 2; return m; };
    const sets = { open: [], shut: [] };
    E.forEach(([x, y], i) => { for (const st of ['open', 'shut']) { const m = mk(st); m.position.set(x, y, o.z ?? 0.097); m.rotation.z = tl; g.add(m); sets[st].push(m); } });
    const sqx = o.sq ? o.sq.map(q => [q[0], q[1]]) : null, sqy = o.sq ? o.sq.map(q => [q[0], q[2]]) : null;
    g.userData.update = t => { const u = keyAt(o.close, t, 0), sx = keyAt(sqx, t, 1), sy = keyAt(sqy, t, 1); g.scale.set(sx, sy, 1); for (const m of sets.open) m.visible = u < 0.5; for (const m of sets.shut) m.visible = u >= 0.5; };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a big death certificate (pivot at its bottom edge, front +Z): white, a thick black
  // mourning border, grey bars for lines and a grey seal, no text; o.w (0.44), o.lean (rad, tipped back)
  plCertificate(o) {
    const w = o.w ?? 0.44, h = w * 1.36, g = grp();
    const p = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.fillStyle = '#121214'; const b = W * 0.085; c.fillRect(0, 0, W, b); c.fillRect(0, H - b, W, b); c.fillRect(0, 0, b, H); c.fillRect(W - b, 0, b, H);
      c.lineWidth = W * 0.012; c.strokeStyle = '#121214'; c.strokeRect(b * 1.6, b * 1.6, W - b * 3.2, H - b * 3.2);
      c.fillStyle = '#7A7E86'; c.fillRect(W * 0.28, H * 0.17, W * 0.44, H * 0.035); for (let i = 0; i < 6; i++) c.fillRect(W * 0.22, H * (0.3 + i * 0.07), W * (i % 3 === 2 ? 0.36 : 0.56), H * 0.018);
      c.strokeStyle = '#7A7E86'; c.lineWidth = W * 0.014; c.beginPath(); c.arc(W * 0.68, H * 0.8, W * 0.09, 0, TAU); c.stroke(); c.beginPath(); c.arc(W * 0.68, H * 0.8, W * 0.06, 0, TAU); c.stroke(); }, { res: 512 });
    const back = at(box(w, h, 0.008, '#E8E8E4'), 0, h / 2, -0.006), pl = grp(back, at(p, 0, h / 2, 0)); pl.rotation.x = -(o.lean ?? 0.18); g.add(pl);
    return g;
  },

  // ---------------------------------------------------------------- a funeral wreath on a little easel (pivot at the easel's feet, front +Z)
  // A thick green ring (o.R 0.36) studded with red, white and yellow flowers, a violet ribbon sash across its foot (no words); o.stand false: the
  // wreath alone (carried), its centre at the pivot
  plWreath(o) {
    const R = o.R ?? 0.36, g = grp(), w = grp(), cy = o.stand === false ? 0 : 0.62 + R; g.add(w);
    w.add(at(new THREE.Mesh(new THREE.TorusGeometry(R, R * 0.22, 8, 22), mat('#3E7A3A')), 0, 0, 0));
    const fl = [], fc = []; for (let i = 0; i < 26; i++) { const a = i / 26 * TAU; fl.push([Math.cos(a) * R + (hsh(i) - 0.5) * 0.04, Math.sin(a) * R + (hsh(i + 9) - 0.5) * 0.04, R * 0.16, 0, 0, 0, 1, 1, 0.8]); fc.push(['#D9302A', '#F4F2EC', '#F2C23A', '#E8742E'][i % 4]); }
    w.add(inst(new THREE.IcosahedronGeometry(R * 0.11, 0), mat('#FFFFFF'), fl, fc));
    w.add(at(box(R * 1.5, R * 0.3, 0.02, '#6A3A9A', { outline: 0.01 }), 0, -R * 0.78, R * 0.22, 0, 0, 0.1), at(box(R * 0.2, R * 0.6, 0.02, '#6A3A9A'), -R * 0.25, -R * 1.15, R * 0.2, 0, 0, 0.2), at(box(R * 0.2, R * 0.6, 0.02, '#6A3A9A'), R * 0.15, -R * 1.15, R * 0.2, 0, 0, -0.15));
    w.position.y = cy;
    if (o.stand !== false) for (const [x, z] of [[-0.25, 0.12], [0.25, 0.12], [0, -0.25]]) g.add(rod([x, 0, z], [0, cy + R * 0.2, -0.04], 0.012, '#6B4A2E'));
    return g;
  },

  // ---------------------------------------------------------------- wrought-iron cemetery gates on two stone posts (pivot at the middle of the
  // sill, front +Z): o.w (2.8) wide, o.h (2.4) high, black bars with gold spear tips, rails, an arch of scrolls; o.swing [[t, a], ...] opens both
  // leaves by a (rad, toward -Z); o.rise [[t, u], ...] u 0: the leaves lie flat on the sand (falling toward +Z), 1 stood up; o.lockAt: a big
  // brass padlock snaps on the meeting bars (pop, the shackle drops shut); o.rattle [[t0, amp, f, dk], ...]
  plGates(o) {
    const W = o.w ?? 2.8, H = o.h ?? 2.4, g = grp(), iron = mat('#1E1F24'), gold = mat('#D8A93A');
    for (const sd of [-1, 1]) { g.add(at(box(0.42, H + 0.4, 0.42, '#E4DCCB', { pivot: 'bottom', outline: 0.01 }), sd * (W / 2 + 0.21), 0, 0), at(box(0.52, 0.14, 0.52, '#D2C8B4', { pivot: 'bottom' }), sd * (W / 2 + 0.21), H + 0.4, 0), at(sphere(0.16, '#E4DCCB', 1), sd * (W / 2 + 0.21), H + 0.68, 0)); }
    const leaves = [-1, 1].map(sd => { const piv = grp(), lf = grp(); piv.position.set(sd * W / 2, 0, 0); piv.add(lf); g.add(piv);
      const lw = W / 2 - 0.02, nb = 7;
      for (let i = 0; i < nb; i++) { const x = -sd * (0.08 + i * (lw - 0.12) / (nb - 1)), hh = H - 0.12 * Math.abs(i - (nb - 1) / 2) / ((nb - 1) / 2) * (sd > 0 ? 1 : 1);
        lf.add(at(new THREE.Mesh(new THREE.BoxGeometry(0.035, hh, 0.035), iron), x, hh / 2 + 0.05, 0));
        const tip = new THREE.Mesh(new THREE.ConeGeometry(0.045, 0.14, 4), gold); tip.position.set(x, hh + 0.12, 0); lf.add(tip); }
      for (const y of [0.25, H * 0.55, H - 0.25]) lf.add(at(new THREE.Mesh(new THREE.BoxGeometry(lw, 0.06, 0.05), iron), -sd * lw / 2, y, 0));
      for (let k = 0; k < 3; k++) { const ring = new THREE.Mesh(new THREE.TorusGeometry(0.11, 0.016, 5, 16), iron); ring.position.set(-sd * (0.25 + k * (lw - 0.4) / 2), H * 0.55 + 0.17, 0); lf.add(ring); }
      lf.add(at(new THREE.Mesh(new THREE.BoxGeometry(0.06, H - 0.05, 0.06), iron), -sd * (lw - 0.02), H / 2, 0));
      return [piv, lf, sd]; });
    const lock = grp(at(box(0.2, 0.2, 0.08, '#C9972E', { outline: 0.02 }), 0, 0, 0), at(cyl(0.025, 0.025, 0.012, '#3A2A10', 8), 0, -0.02, 0.045, PI / 2));
    const shackle = new THREE.Mesh(new THREE.TorusGeometry(0.075, 0.022, 6, 16, PI), mat('#B8BCC4')); shackle.position.y = 0.1; lock.add(shackle);
    lock.position.set(0, H * 0.55 - 0.18, 0.09); g.add(lock); lock.visible = false;
    g.userData.update = t => { const a = keyAt(o.swing, t, 0), u = keyAt(o.rise, t, 1), r = rattle(o.rattle, t);
      for (const [piv, lf, sd] of leaves) { piv.rotation.set(-(1 - u) * PI / 2 * -1, sd * a + r * sd, 0); }
      if (o.lockAt != null) { const q = (t - o.lockAt) / 0.2; lock.visible = q > 0; lock.scale.setScalar(Math.max(0.01, outBack(q, 3))); shackle.position.y = 0.1 + 0.06 * (1 - clamp01((t - o.lockAt - 0.12) / 0.06)); lock.rotation.z = rattle([[o.lockAt + 0.18, 0.25, 22, 6]], t); } };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a big galvanised bin with two handles (pivot at its floor, front +Z), o.r (0.3)
  plBin(o) {
    const r = o.r ?? 0.3, h = r * 2.1, g = grp(), b = grp(); g.add(b);
    b.add(at(cyl(r, r * 0.86, h, '#AEB4BC', 14, { pivot: 'bottom', outline: 0.012 }), 0, 0, 0), at(new THREE.Mesh(new THREE.TorusGeometry(r, 0.02, 6, 20), mat('#8E949C')), 0, h, 0, PI / 2, 0, 0));
    for (const y of [0.3, 0.65]) b.add(at(new THREE.Mesh(new THREE.TorusGeometry(r * (1 - 0.14 * (1 - y)) + 0.004, 0.012, 5, 20), mat('#9AA0A8')), 0, h * y, 0, PI / 2, 0, 0));
    b.add(at(cyl(r * 0.96, r * 0.96, 0.01, '#3A3E46', 14), 0, h - 0.02, 0));
    for (const sd of [-1, 1]) b.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.06, 0.014, 5, 10, PI), mat('#8E949C')), sd * (r + 0.03), h * 0.8, 0, 0, PI / 2, sd * PI / 2));
    g.userData.update = t => { const q = rattle(o.bump, t); b.scale.set(1 + q, 1 - q, 1 + q); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a child's plastic spade, cartoon size (pivot at its grip, the blade down -Y)
  plSpade(o) {
    const Ln = o.len ?? 0.62, c = o.color || '#E8452E', g = grp();
    g.add(at(cyl(0.022, 0.022, Ln, c, 6, { pivot: 'top' }), 0, 0, 0), at(box(0.13, 0.04, 0.04, c, { outline: 0.02 }), 0, 0, 0));
    const sh = new THREE.Shape(); sh.moveTo(-0.08, 0); sh.lineTo(0.08, 0); sh.lineTo(0.09, -0.15); sh.quadraticCurveTo(0, -0.24, -0.09, -0.15); sh.lineTo(-0.08, 0);
    const bl = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: 0.02, bevelEnabled: false }), mat(c, { doubleSide: true })); bl.position.set(0, -Ln + 0.02, -0.01); bl.castShadow = true; g.add(bl);
    g.userData.grip = [0, 0, 0]; return g;
  },

  // ---------------------------------------------------------------- a black folding fan (pivot at its rivet, opening upward in its XY plane)
  // o.flap [[t0, t1], ...]: it flutters (quick back-and-forth) between t0 and t1; o.rate (11 rad/s)
  plFan(o) {
    const g = grp(), f = grp(), R = o.r ?? 0.28; g.add(f);
    const sh = new THREE.Shape(); sh.moveTo(0, 0); sh.absarc(0, 0, R, PI * 0.15, PI * 0.85, false); sh.lineTo(0, 0);
    f.add(new THREE.Mesh(new THREE.ShapeGeometry(sh, 12), mat(o.color || '#141418', { doubleSide: true })));
    for (let i = 0; i < 9; i++) { const a = PI * (0.15 + 0.7 * i / 8); f.add(at(box(0.008, R, 0.006, '#4A4A52'), Math.cos(a) * R / 2, Math.sin(a) * R / 2, 0.004, 0, 0, a - PI / 2)); }
    f.add(at(new THREE.Mesh(new THREE.RingGeometry(R * 0.96, R * 1.0, 24, 1, PI * 0.15, PI * 0.7), B('#C9A23A', { side: THREE.DoubleSide })), 0, 0, 0.005));
    g.userData.update = t => { let a = 0; for (const [t0, t1] of o.flap || []) if (t >= t0 && t < t1) a = 0.45 * Math.sin((t - t0) * (o.rate ?? 11)) * Math.min(1, (t - t0) * 8, (t1 - t) * 8); f.rotation.z = a; };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a black beach ball that rolls along o.path [[t, x, z], ...] (pivot on the sand)
  plBall(o) {
    const r = o.r ?? 0.24, g = grp(), b = grp(); g.add(b);
    for (let i = 0; i < 6; i++) { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 12, 10, i * TAU / 6, TAU / 6), mat(i % 2 ? '#141418' : '#3A3C44')); b.add(m); }
    b.add(at(sphere(r * 0.18, '#141418', 1), 0, r, 0), at(new THREE.Mesh(new THREE.PlaneGeometry(r * 0.35, r * 0.18), B('#FFFFFF', { transparent: true, opacity: 0.6 })), -r * 0.35, r * 0.5, r * 0.82, 0, -0.4, 0.5));
    b.position.y = r;
    const path = o.path || [[0, 0, 0]];
    g.userData.update = t => { let x = path[0][1], z = path[0][2], dist = 0;
      for (let i = 1; i < path.length; i++) { const seg = Math.hypot(path[i][1] - path[i - 1][1], path[i][2] - path[i - 1][2]); if (t >= path[i][0]) { x = path[i][1]; z = path[i][2]; dist += seg; } else if (t > path[i - 1][0]) { const u = (t - path[i - 1][0]) / (path[i][0] - path[i - 1][0]); x = lerp(path[i - 1][1], path[i][1], u); z = lerp(path[i - 1][2], path[i][2], u); dist += seg * u; } }
      g.position.set(x, 0, z); const dx = path[path.length - 1][1] - path[0][1], dz = path[path.length - 1][2] - path[0][2], a = Math.atan2(dx, dz);
      b.rotation.set(0, 0, 0); b.rotateOnWorldAxis(new THREE.Vector3(Math.cos(a), 0, -Math.sin(a)), dist / r); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a lifeguard tower (pivot at its feet, front +Z): stilts, a deck at 1.7 m, a hut
  // with a striped awning roof, a ladder; no cross, no words
  plTower(o) {
    const g = grp(), wd = '#C9A06A', dk = '#8A6A42', Hd = 1.7;
    for (const [x, z] of [[-0.6, -0.5], [0.6, -0.5], [-0.6, 0.5], [0.6, 0.5]]) g.add(rod([x * 1.15, 0, z * 1.15], [x, Hd, z], 0.05, wd));
    g.add(rod([-0.68, 0.6, 0.57], [0.68, 1.2, 0.57], 0.025, dk), rod([0.68, 0.6, 0.57], [-0.68, 1.2, 0.57], 0.025, dk));
    g.add(at(box(1.5, 0.1, 1.3, wd, { pivot: 'bottom', outline: 0.008 }), 0, Hd, 0), at(box(1.1, 1.0, 0.9, '#F4F1E8', { pivot: 'bottom', outline: 0.008 }), 0, Hd + 0.1, -0.12), at(box(0.7, 0.45, 0.02, '#2A3A4A'), 0, Hd + 0.75, 0.34));
    for (let i = 0; i < 5; i++) g.add(at(box(1.5 / 5, 0.08, 1.4, i % 2 ? '#F4F1E8' : '#2F6FB5', { outline: 0.006 }), -0.6 + i * 0.3, Hd + 1.18, -0.05, 0.18, 0, 0));
    for (const sd of [-1, 1]) g.add(at(box(0.04, 0.5, 0.04, wd), sd * 0.72, Hd + 0.35, 0.62));
    g.add(at(box(1.48, 0.04, 0.04, wd), 0, Hd + 0.6, 0.62));
    for (const sd of [-0.18, 0.18]) g.add(rod([sd, 0, 1.4], [sd, Hd, 0.66], 0.025, dk));
    for (let i = 1; i < 7; i++) { const u = i / 7; g.add(at(box(0.38, 0.03, 0.05, dk), 0, Hd * u, 1.4 - 0.74 * u)); }
    return g;
  },

  // ---------------------------------------------------------------- a one-piece swimsuit body (attach to the torso joint) and its bottom (hips joint)
  plSwimTop(o) { const w = o.w ?? 0.47, d = o.d ?? 0.27, h = o.h ?? 0.5, c = o.color || '#141418', g = grp(at(box(w, h, d, c, { pivot: 'bottom' }), 0, o.y ?? -0.02, o.z ?? 0.0));
    for (const sd of [-1, 1]) g.add(at(box(0.05, 0.12, d * 0.9, c), sd * w * 0.3, (o.y ?? -0.02) + h + 0.05, o.z ?? 0)); return g; },
  plSwimBottom(o) { const w = o.w ?? 0.47, d = o.d ?? 0.28, c = o.color || '#141418'; return grp(at(box(w, o.h ?? 0.2, d, c), 0, o.y ?? -0.06, 0)); },

  // ---------------------------------------------------------------- a wide straw sunhat with a ribbon (attach to the head joint, offset [0, 0.5, 0])
  plSunHat(o) { const R = o.R ?? 0.42, g = grp(at(cyl(R, R, 0.02, o.color || '#E8D29A', 20, { outline: 0.02 }), 0, 0.01, 0), at(cyl(0.17, 0.19, 0.16, o.color || '#E8D29A', 14, { pivot: 'bottom' }), 0, 0.01, 0), at(cyl(0.195, 0.195, 0.05, o.band || '#C8322A', 14, { pivot: 'bottom' }), 0, 0.02, 0));
    g.children[0].rotation.x = o.tip ?? 0.1; return g; },

  // ---------------------------------------------------------------- a black mourning veil (attach to the head joint, offset [0, 0.5, 0]): a little
  // pillbox hat and a short net over the brow that stops above the eyes (the face shows)
  plVeil(o) { const g = grp(at(cyl(0.12, 0.13, 0.08, '#141418', 12, { pivot: 'bottom' }), 0, 0, -0.02)); const net = new THREE.Mesh(new THREE.PlaneGeometry(o.w ?? 0.36, o.h ?? 0.14), B('#141418', { transparent: true, opacity: 0.55, side: THREE.DoubleSide, depthWrite: false }));
    net.position.set(0, -0.05, 0.11); net.rotation.x = 0.25; g.add(net); return g; },

  // ---------------------------------------------------------------- a big crumpled white tissue (attach to a hand)
  // a rolled beach towel carried under an arm (attach to the torso joint): a striped roll
  plTowelRoll(o) { const g = grp(), cols = o.colors || ['#2E8AC9', '#F4F1E8']; for (let i = 0; i < 6; i++) g.add(at(cyl(0.1, 0.1, 0.09, cols[i % 2], 10), -0.27 + i * 0.09, 0, 0, 0, 0, PI / 2)); return g; },
  plTissue(o) { const g = grp(), s = o.s ?? 1; for (let i = 0; i < 4; i++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(0.05 * s, 0), mat('#FFFFFF', { noGrain: true })); m.position.set((hsh(i) - 0.5) * 0.05 * s, -0.04 * s - i * 0.02 * s, (hsh(i + 5) - 0.5) * 0.04 * s); m.scale.set(1.2, 0.8, 0.5); g.add(m); }
    g.add(at(box(0.11 * s, 0.1 * s, 0.004, '#FFFFFF', { noGrain: true }), 0, -0.11 * s, 0, 0, 0, 0.3)); return g; },

  // ---------------------------------------------------------------- a stamped permit held up to the lens (pivot at its middle, front +Z): a cream sheet,
  // the title PERMIS D'EXHUMER, grey lines, and at o.stampAt a big red round stamp ACCORDÉ pops on it (tilted, with an overshoot); o.w (0.5)
  plPermit(o) {
    const w = o.w ?? 0.5, h = w * 1.3, g = grp();
    const p = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FBF6E6'; c.fillRect(0, 0, W, H); c.strokeStyle = '#2F4A7A'; c.lineWidth = W * 0.02; c.strokeRect(W * 0.04, H * 0.04, W * 0.92, H * 0.92);
      c.fillStyle = '#1E2A44'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, 'PERMIS', W / 2, H * 0.12, W * 0.8, H * 0.09); fitText(c, "D'EXHUMER", W / 2, H * 0.22, W * 0.8, H * 0.07);
      c.fillStyle = '#9AA0AA'; for (let i = 0; i < 7; i++) c.fillRect(W * 0.14, H * (0.34 + i * 0.07), W * (i % 3 === 2 ? 0.4 : 0.72), H * 0.016); }, { res: 512 });
    const back = at(box(w, h, 0.01, '#E8E2CE', { outline: 0.01 }), 0, 0, -0.008); g.add(back, p);
    const st = canvasPlane(w * 0.7, w * 0.7, (c, W, H) => { c.clearRect(0, 0, W, H); c.strokeStyle = '#D0262A'; c.lineWidth = W * 0.06; c.beginPath(); c.arc(W / 2, H / 2, W * 0.44, 0, TAU); c.stroke(); c.lineWidth = W * 0.025; c.beginPath(); c.arc(W / 2, H / 2, W * 0.34, 0, TAU); c.stroke();
      c.fillStyle = '#D0262A'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, 'ACCORDÉ', W / 2, H / 2, W * 0.62, H * 0.2); }, { res: 512, transparent: true });
    st.position.set(0, -h * 0.17, 0.008); g.add(st);
    g.userData.update = t => { const q = o.stampAt == null ? 1 : (t - o.stampAt) / 0.16; st.visible = q > 0; st.scale.setScalar(Math.max(0.01, q < 1 ? 1.8 - 0.8 * outBack(q, 2) : 1)); st.rotation.z = -0.3; };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a fat kraft envelope (pivot at its middle, front +Z), o.w (0.4), o.fat (0.07)
  plEnvelope(o) { const w = o.w ?? 0.4, h = w * 0.66, f = o.fat ?? 0.07, g = grp(at(box(w, h, f, '#E2C98E', { outline: 0.012 }), 0, 0, 0));
    const fr = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#E2C98E'; c.fillRect(0, 0, W, H); c.fillStyle = '#FFFFFF'; c.fillRect(W * 0.45, H * 0.5, W * 0.45, H * 0.3); c.fillStyle = '#8A8E96'; for (let i = 0; i < 3; i++) c.fillRect(W * 0.49, H * (0.56 + i * 0.08), W * 0.34, H * 0.035); c.fillStyle = '#C8322A'; c.fillRect(W * 0.07, H * 0.1, W * 0.18, H * 0.2); }, { res: 256 });
    fr.position.z = f / 2 + 0.002; g.add(fr); return g; },

  // ---------------------------------------------------------------- the tax form held up to the lens (pivot at its middle): AVIS D'IMPOSITION, lines,
  // a red box À PAYER with a long amount of zeros drawn as bars
  plTaxForm(o) { const w = o.w ?? 0.46, h = w * 1.35;
    return grp(at(box(w, h, 0.01, '#E8E8E4', { outline: 0.01 }), 0, 0, -0.008), canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.fillStyle = '#1E2A44'; c.textAlign = 'center'; c.textBaseline = 'middle';
      fitText(c, "AVIS D'IMPOSITION", W / 2, H * 0.1, W * 0.84, H * 0.07); c.fillStyle = '#9AA0AA'; for (let i = 0; i < 6; i++) c.fillRect(W * 0.1, H * (0.22 + i * 0.065), W * (i % 2 ? 0.5 : 0.78), H * 0.016);
      c.strokeStyle = '#C8322A'; c.lineWidth = W * 0.02; c.strokeRect(W * 0.1, H * 0.66, W * 0.8, H * 0.22); c.fillStyle = '#C8322A'; fitText(c, 'À PAYER', W / 2, H * 0.72, W * 0.6, H * 0.06); fitText(c, '9 999 €', W / 2, H * 0.82, W * 0.66, H * 0.09); }, { res: 512 })); },

  // ---------------------------------------------------------------- a burst of sand thrown off his head (pivot at its source): o.at [t, ...], o.n
  // grains per burst flying out in a fan toward o.dir (+Z) and to the sides, falling under gravity, o.s their size
  plSandSpray(o) {
    const g = grp(), n = o.n ?? 40, s = o.s ?? 0.035, grains = [];
    for (const t0 of o.at || []) for (let i = 0; i < n; i++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(s * (0.6 + hsh(i * 7 + t0) * 0.8), 0), mat(i % 3 ? '#D9BC7A' : '#C9A862')); m.castShadow = false; g.add(m);
      const a = (hsh(i * 3 + t0 * 11) - 0.5) * PI * 1.5, sp = 2.2 + hsh(i + 1.3) * 2.2, up = 1.2 + hsh(i * 5.1) * 2.2; grains.push([m, t0, Math.sin(a) * sp * (o.side ?? 1), up, Math.cos(a) * sp * 0.6 + (o.fwd ?? 1.2)]); }
    g.userData.update = t => { for (const [m, t0, vx, vy, vz] of grains) { const u = t - t0; m.visible = u > 0 && u < 0.9; if (!m.visible) continue; m.position.set(vx * u, Math.max(-0.2, vy * u - 4.9 * u * u), vz * u); m.rotation.set(u * 9, u * 7, 0); } };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- sand stuck on a face (attach to the head joint, offset to the face): a cluster of
  // grains that pops on at o.at
  plSandSpeck(o) { const g = grp(), s = o.s ?? 1; for (let i = 0; i < 22; i++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(0.012 * s * (0.7 + hsh(i) * 0.8), 0), mat(i % 2 ? '#D9BC7A' : '#B8984E', { noGrain: true })); m.position.set((hsh(i * 3) - 0.5) * 0.22 * s, (hsh(i * 5 + 1) - 0.5) * 0.26 * s, 0); g.add(m); }
    g.userData.update = t => { g.visible = o.at == null || t >= o.at; }; g.userData.update(0); return g; },

  // ---------------------------------------------------------------- a cardboard box of office things (pivot at its floor, front +Z): a desk lamp's
  // arm, a potted plant, folders and a mug stick out
  plOfficeBox(o) { const w = 0.5, h = 0.32, d = 0.38, C = '#C49A66', g = grp(at(box(w, h, d, C, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0));
    for (const sd of [-1, 1]) g.add(at(box(w, 0.012, 0.16, '#B8895A'), 0, h + 0.03, sd * (d / 2 + 0.05), sd * 0.6, 0, 0));
    g.add(at(cyl(0.07, 0.06, 0.12, '#C8463A', 8, { pivot: 'bottom' }), -0.14, h - 0.06, 0.04), at(sphere(0.12, '#3E8A3A', 0), -0.14, h + 0.17, 0.04), at(sphere(0.08, '#4E9A4A', 0), -0.08, h + 0.27, 0.0));
    g.add(at(box(0.04, 0.3, 0.22, '#2F62B5'), 0.04, h + 0.05, -0.04, 0, 0, -0.15), at(box(0.04, 0.28, 0.22, '#E8B020'), 0.1, h + 0.04, -0.04, 0, 0, 0.1));
    g.add(rod([0.18, h - 0.05, 0.0], [0.2, h + 0.25, 0.0], 0.015, '#3A3D44'), rod([0.2, h + 0.25, 0.0], [0.12, h + 0.38, 0.05], 0.015, '#3A3D44'), at(cyl(0.03, 0.07, 0.08, '#3A3D44', 8), 0.1, h + 0.36, 0.06, 0.6, 0, 0));
    g.add(at(cyl(0.04, 0.04, 0.08, '#F4F4F0', 8, { pivot: 'bottom' }), 0.16, h - 0.03, 0.12)); return g; },

  // ---------------------------------------------------------------- an open glossy magazine held flat between two readers (pivot at its spine)
  plMagazine(o) { const w = o.w ?? 0.34, h = w * 1.3, g = grp();
    for (const sd of [-1, 1]) { const p = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FAF6EE'; c.fillRect(0, 0, W, H); c.fillStyle = sd < 0 ? '#E8742E' : '#2F8AC9'; c.fillRect(W * 0.08, H * 0.08, W * 0.84, H * 0.45); c.fillStyle = '#F2C23A'; c.beginPath(); c.arc(W * 0.5, H * 0.3, W * 0.15, 0, TAU); c.fill(); c.fillStyle = '#9AA0AA'; for (let i = 0; i < 5; i++) c.fillRect(W * 0.08, H * (0.62 + i * 0.07), W * 0.8, H * 0.02); }, { res: 256 });
      p.position.set(sd * w / 2, 0, 0); const piv = grp(p); piv.rotation.y = -sd * 0.25; g.add(piv); }
    return g; },

  // ---------------------------------------------------------------- gulls gliding round a point in the sky, all the same way, each at its own height
  // (pivot at the centre of their circle): o.n (3), o.R (6), o.h (heights step 0.8 m), o.rate (rad/s), wings flapping now and then
  plGulls(o) { const g = grp(), gs = [];
    for (let i = 0; i < (o.n ?? 3); i++) { const q = grp(), bd = sphere(0.12, '#F4F4F0', 1); bd.scale.set(0.7, 0.6, 1.6); q.add(bd); const hd = sphere(0.07, '#F4F4F0', 1); hd.position.set(0, 0.05, 0.2); q.add(hd); const bk = new THREE.Mesh(new THREE.ConeGeometry(0.02, 0.07, 5), mat('#F2B23A')); bk.rotation.x = PI / 2; bk.position.set(0, 0.04, 0.29); q.add(bk);
      const ws = [-1, 1].map(sd => { const w = grp(at(box(0.45, 0.015, 0.14, '#C9CDD3', { outline: 0.03 }), sd * 0.22, 0, 0), at(box(0.12, 0.016, 0.1, '#2A2C30'), sd * 0.42, 0.001, -0.01)); q.add(w); return [w, sd]; });
      q.scale.setScalar(o.s ?? 1.4); g.add(q); gs.push([q, ws, i]); }
    g.userData.update = t => gs.forEach(([q, ws, i]) => { const a = t * (o.rate ?? 0.35) + i * TAU / gs.length, R = (o.R ?? 6) * (0.85 + 0.15 * i); q.position.set(Math.cos(a) * R, i * (o.h ?? 0.8) + 0.2 * Math.sin(t * 1.3 + i), Math.sin(a) * R); q.rotation.set(0, -a + PI, 0.35);
      const fl = Math.sin(t * 9 + i) > 0.2 ? Math.sin(t * 14 + i) * 0.5 : 0.08; for (const [w, sd] of ws) w.rotation.z = sd * fl; });
    g.userData.update(0); return g; },
};
