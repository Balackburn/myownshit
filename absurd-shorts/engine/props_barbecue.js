// « Le barbecue » (story 83): this man was smoked out by his neighbour's barbecue and cried chemical attack; the president set off the nuclear
// alert; the whole country put on gas masks; the army dropped a whole regiment; one landed on the grill, the others on his house; six sausages
// were taken prisoner; a chipolata refused to talk and was swapped for a spy; the army put the barbecue out with a flamethrower and the
// neighbourhood caught fire; the paratrooper did not move; the minister ate a sausage to reassure everyone and was put in quarantine; the
// president decreed a national barbecue on the embers of the neighbourhood. And he was not invited.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere, addOutline, mat, rng } from './style.js';
import { grp, at, canvasPlane, buildProp, rod } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = x => { const u = clamp01(x), c = 1.70158; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const basic = (c, o = {}) => new THREE.MeshBasicMaterial({ color: c, transparent: o.opacity != null, opacity: o.opacity ?? 1, depthWrite: o.opacity == null, side: o.side || THREE.FrontSide, fog: o.fog ?? true });
const lam = (c, o = {}) => new THREE.MeshLambertMaterial({ color: c, emissive: new THREE.Color(o.emissive || '#000000'), emissiveIntensity: o.ei ?? 1, flatShading: true, transparent: o.opacity != null, opacity: o.opacity ?? 1, depthWrite: o.opacity == null });
const noShadow = m => { m.traverse(c => { c.castShadow = false; }); return m; };
const bez = (P, u) => {
  if (P.length === 2) return P[0].map((a, i) => a + (P[1][i] - a) * u);
  if (P.length === 3) { const v = 1 - u; return [0, 1, 2].map(i => v * v * P[0][i] + 2 * v * u * P[1][i] + u * u * P[2][i]); }
  const v = 1 - u; return [0, 1, 2].map(i => v * v * v * P[0][i] + 3 * v * v * u * P[1][i] + 3 * v * u * u * P[2][i] + u * u * u * P[3][i]);
};
const inWin = (wins, t) => { for (const w of wins || []) if (t >= w[0] && t < w[1]) return w; return null; };

// a sausage along +Y from 0 to len (pivot at its bottom end): a capsule, two twisted tips, three dark grill marks; o.char: black
function sausageMesh(len, r, color, o = {}) {
  const g = grp(), m = mat(color), body = new THREE.Mesh(new THREE.CapsuleGeometry(r, Math.max(0.001, len - 2 * r), 4, 10), m);
  body.position.y = len / 2; body.castShadow = true; addOutline(body, 0.06); g.add(body);
  for (const y of [0, len]) g.add(at(cyl(0.003, r * 0.32, r * 0.55, color, 6), 0, y === 0 ? -r * 0.2 : len + r * 0.2, 0, y === 0 ? PI : 0, 0, 0));
  if (o.marks !== false) for (let i = 0; i < 3; i++) { const ring = new THREE.Mesh(new THREE.TorusGeometry(r * 1.005, r * 0.12, 4, 12, PI * 0.9), mat(o.markColor || '#5A2615')); ring.rotation.set(PI / 2 + 0.5, 0, PI * 0.55); ring.position.y = len * (0.3 + 0.2 * i); g.add(ring); }
  return g;
}

// a fork that holds a sausage at the end of its tines (pivot at the grip, the fork along +Y; the sausage carries on along +Y)
function forkMesh(o = {}) {
  const g = grp(at(box(0.018, 0.13, 0.01, '#C9CDD2', { outline: 0.01 }), 0, 0.02, 0), at(box(0.012, 0.05, 0.006, '#C9CDD2'), 0, 0.11, 0), at(box(0.03, 0.01, 0.006, '#C9CDD2'), 0, 0.135, 0));
  for (const x of [-0.011, 0, 0.011]) g.add(at(box(0.004, 0.06, 0.004, '#D9DDE2'), x, 0.17, 0));
  return g;
}

export const BARBECUE_PROPS = {
  // A sausage on its own (pivot at its bottom end, along +Y, o.upright default; o.lying: on its side along X, pivot at its middle, resting on y 0).
  // o.len (0.3), o.r (0.045), o.color; o.char: burnt black; o.bite [t, frac]: from t its top frac is gone (a pink bitten end); o.hop [[t, h], ...]:
  // it jumps h metres and lands with a squash (a pure function of t, on top of any prop keys)
  sausage(o) {
    const len = o.len ?? 0.3, r = o.r ?? 0.045, col = o.char ? '#2B2420' : (o.color || '#B5532E'), g = grp(), inner = grp(), bf = o.bite ? o.bite[1] : 0;
    const low = sausageMesh(len * (1 - bf), r, col, o), top = o.bite ? at(sausageMesh(len * bf, r, col, { marks: false }), 0, len * (1 - bf), 0) : null;
    inner.add(low); if (top) inner.add(top);
    const cut = o.bite ? at(cyl(r * 0.92, r * 0.92, 0.006, '#E89A8A', 10), 0, len * (1 - bf) + 0.003, 0) : null; if (cut) { cut.visible = false; inner.add(cut); }
    if (o.lying) { inner.rotation.z = -PI / 2; inner.position.set(-len / 2, r, 0); }
    g.add(inner);
    g.userData.update = t => {
      if (top) { const b = t >= o.bite[0]; top.visible = !b; cut.visible = b; }
      let y = 0, sy = 1;
      for (const [t0, h, d = 0.42] of o.hop || []) { const u = (t - t0) / d; if (u >= 0 && u < 1) { y = Math.max(y, 4 * h * u * (1 - u)); sy = u < 0.12 ? 1.18 - u : u > 0.88 ? 1 - (1 - u) * 1.6 : 1.06; } else if (u >= 1 && u < 1.35) sy = Math.min(sy, 0.72 + 0.28 * smooth((u - 1) / 0.35)); }
      inner.position.y = (o.lying ? r : 0) + y; g.scale.set(1 / Math.sqrt(sy), sy, 1 / Math.sqrt(sy));
    };
    g.userData.update(0); return g;
  },

  // A fork with a sausage skewered on its tines (pivot at the grip, the fork along +Y: give the hand a rot so it points where wanted); o.len
  // (0.16), o.r (0.03), o.bite [t, frac] as sausage, o.char
  forkSausage(o) {
    const g = grp(forkMesh(o)), s = buildProp('sausage', { len: o.len ?? 0.16, r: o.r ?? 0.03, bite: o.bite, char: o.char, color: o.color });
    s.position.y = 0.17; g.add(s); g.userData.update = t => s.userData.update?.(t); g.userData.update(0); return g;
  },

  // A long roasting stick with a sausage at its end (pivot at the grip, along +Y, o.L 1.0 m long); o.char
  sausageStick(o) {
    const L = o.L ?? 1.0, g = grp(rod([0, -0.1, 0], [0, L, 0], 0.009, '#8A6A44', 5)), s = buildProp('sausage', { len: o.len ?? 0.18, r: o.r ?? 0.032, char: o.char, color: o.color });
    s.position.y = L - 0.05; g.add(s); return g;
  },

  // A round charcoal kettle grill on three legs (pivot at the floor): a red enamel bowl o.r (0.3) wide, its grate at o.h (0.8), glowing coals, o.n
  // (5) sausages across the grate, little flames, a column of grey smoke (o.smoke, default on: o.smokeH 1.6 high, o.smokeSize 1, o.wind [x, z]
  // drift per metre). o.char: a charred black lump (bowl sagging, sausages black stubs, no flames, a thin dark smoke); o.charAt t: switches to
  // the charred one at t. o.sausages false: an empty grate
  kettleGrill(o) {
    const R = o.r ?? 0.3, H = o.h ?? 0.8, g = grp(), mk = (charred) => {
      const k = grp(), bowlC = charred ? '#1E1B19' : (o.color || '#B8322A'), legC = charred ? '#141210' : '#2B2E33';
      const bowl = new THREE.Mesh(new THREE.SphereGeometry(R, 16, 8, 0, TAU, PI / 2, PI / 2), mat(bowlC, { doubleSide: true })); bowl.position.y = H - 0.02; bowl.castShadow = true; addOutline(bowl, 0.03); k.add(bowl);
      const rim = new THREE.Mesh(new THREE.TorusGeometry(R, 0.014, 5, 20), mat(charred ? '#2A2622' : '#8E2A22')); rim.rotation.x = PI / 2; rim.position.y = H - 0.02; k.add(rim);
      for (let i = 0; i < 3; i++) { const a = i / 3 * TAU + 0.4, bend = charred ? 0.12 * (i - 1) : 0; k.add(rod([Math.cos(a) * R * 0.55, H - R * 0.8, Math.sin(a) * R * 0.55], [Math.cos(a + bend) * R * 1.1, 0, Math.sin(a + bend) * R * 1.1], 0.014, legC, 5)); }
      if (!charred) { k.add(rod([-R * 0.45, H - R * 0.85, 0], [R * 0.45, H - R * 0.85, 0], 0.01, legC, 4)); k.add(at(cyl(0.06, 0.06, 0.02, '#1A1C20', 10), 0, H - R * 1.0, 0)); }
      const coals = grp(), rr = rng(o.seed || 83);
      for (let i = 0; i < 11; i++) { const a = rr() * TAU, d = Math.sqrt(rr()) * R * 0.75; coals.add(at(new THREE.Mesh(new THREE.DodecahedronGeometry(0.035 + rr() * 0.02, 0), lam(charred ? '#2A2220' : '#3A2A22', { emissive: charred ? '#5A1A0A' : '#FF5A1A', ei: 0.8 })), Math.cos(a) * d, H - 0.07, Math.sin(a) * d, rr() * 3, rr() * 3, 0)); }
      k.add(coals); k.userData.coals = coals;
      if (!charred) { const ring = new THREE.Mesh(new THREE.TorusGeometry(R * 0.96, 0.006, 4, 20), mat('#9AA0A6')); ring.rotation.x = PI / 2; ring.position.y = H; k.add(ring);
        for (let i = 0; i < 7; i++) { const z = -R * 0.8 + i * R * 1.6 / 6, hw = Math.sqrt(Math.max(0, R * R * 0.92 - z * z)); k.add(at(box(hw * 2, 0.006, 0.006, '#9AA0A6'), 0, H, z)); } }
      if (o.sausages !== false) { const n = o.n ?? 5; for (let i = 0; i < n; i++) { const z = (i - (n - 1) / 2) * R * 0.32, L = charred ? 0.13 : 0.26, s = sausageMesh(L, charred ? 0.03 : 0.036, charred ? '#1A1614' : '#B5532E', { marks: !charred }); s.rotation.z = -PI / 2; s.position.set(-L / 2 + (charred ? (hsh(i) - 0.5) * 0.1 : 0), H + 0.035, z); if (charred) s.rotation.y = (hsh(i + 5) - 0.5) * 1.2; k.add(s); } }
      if (charred) { for (let i = 0; i < 7; i++) { const a = hsh(i + 20) * TAU, d = hsh(i + 30) * R * 0.7; k.add(at(new THREE.Mesh(new THREE.DodecahedronGeometry(0.05 + 0.04 * hsh(i + 40), 0), mat('#151312')), Math.cos(a) * d, H + 0.02, Math.sin(a) * d, i, i * 2, 0)); }
        bowl.scale.set(1.05, 0.82, 0.97); }
      return k;
    };
    const live = mk(false), dead = mk(true); g.add(live, dead);
    const flames = grp(); if (!o.char) for (let i = 0; i < 6; i++) { const f = grp(); [0, 1, 2].forEach(j => { const c = noShadow(new THREE.Mesh(new THREE.ConeGeometry(0.04 - j * 0.01, 0.12 + j * 0.03, 6), lam(['#FF7A1A', '#FFB03A', '#FFE07A'][j], { emissive: ['#FF5A10', '#FF9A30', '#FFD070'][j] }))); c.position.y = 0.05 + j * 0.01; f.add(c); });
      const a = i / 6 * TAU + 0.3, d = R * (0.35 + 0.35 * hsh(i + 9)); f.position.set(Math.cos(a) * d, H - 0.01, Math.sin(a) * d); flames.add(f); }
    live.add(flames);
    const nP = o.smoke === false ? 0 : (o.smokeN ?? 16), SH = o.smokeH ?? 1.6, SS = o.smokeSize ?? 1, wind = o.wind || [0.25, 0];
    const sm = nP ? new THREE.InstancedMesh(new THREE.IcosahedronGeometry(1, 1), lam(o.smokeColor || '#B4B0A8', { opacity: 0.9 }), nP) : null;
    if (sm) { sm.castShadow = false; sm.frustumCulled = false; g.add(sm); }
    const d = new THREE.Object3D();
    g.userData.update = t => {
      const charred = !!o.char || (o.charAt != null && t >= o.charAt); live.visible = !charred; dead.visible = charred;
      flames.children.forEach((f, i) => f.scale.set(1, 1 + 0.25 * Math.sin(t * 15 + i * 2.1) + 0.1 * Math.sin(t * 31 + i), 1));
      const cl = (charred ? dead : live).userData.coals; cl.children.forEach((c, i) => { c.material.emissiveIntensity = (charred ? 0.35 : 0.7) + 0.3 * Math.sin(t * 4 + i * 1.7); });
      if (sm) for (let i = 0; i < nP; i++) { const u = ((i / nP) + t * 0.32 * (o.smokeRate ?? 1)) % 1, y = H + 0.1 + u * SH * (charred ? 0.8 : 1), s = SS * (0.05 + u * 0.16) * (charred ? 0.55 : 1);
        d.position.set(wind[0] * u * SH + 0.06 * Math.sin(i * 2.3 + t * 1.7), y, wind[1] * u * SH + 0.06 * Math.cos(i * 1.9 + t * 1.3)); d.scale.setScalar(s); d.updateMatrix(); sm.setMatrixAt(i, d.matrix); }
      if (sm) { sm.instanceMatrix.needsUpdate = true; sm.material.color.set(charred ? '#4A4542' : (o.smokeColor || '#B4B0A8')); }
    };
    g.userData.update(0); return g;
  },

  // A thick ribbon of grey smoke flowing along a curve (pivot anywhere: o.pts are in the prop's own frame, 2 to 4 points of a Bézier curve from the
  // source to the end): o.n (36) overlapping puffs travel along it at o.speed (0.4 lengths a second), growing from o.s0 (0.06) to o.s1 (0.17)
  // and wobbling (o.wob 0.05); o.shrink (default on): they shrink into the end point (drawn in); o.at, o.grow: from o.at the ribbon reaches out
  // from its source and gets to the end after o.grow s; o.color; o.curl r: the last fifth spirals round the end
  smokeRibbon(o) {
    const P = o.pts || [[0, 0, 0], [0, 1, 0]], n = o.n ?? 36, s0 = o.s0 ?? 0.06, s1 = o.s1 ?? 0.17, sp = o.speed ?? 0.4, wob = o.wob ?? 0.05;
    const m = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(1, 1), lam(o.color || '#A9A49C', { opacity: o.opacity ?? 0.94 }), n); m.castShadow = false; m.frustumCulled = false;
    const g = grp(m), d = new THREE.Object3D();
    g.userData.update = t => {
      const reach = o.at == null ? 1 : clamp01((t - o.at) / (o.grow ?? 0.6));
      for (let i = 0; i < n; i++) {
        const u = ((i / n) + t * sp) % 1; let p = bez(P, u);
        const w = wob * (0.3 + u) * Math.sin(i * 2.7 + t * 3.1), w2 = wob * (0.3 + u) * Math.cos(i * 1.9 + t * 2.3);
        p = [p[0] + w, p[1] + w2 * 0.6, p[2] + w2];
        if (o.curl && u > 0.78) { const v = (u - 0.78) / 0.22, a = v * TAU * 1.2 + t * 2, rr = o.curl * (1 - v); const e = P[P.length - 1]; p = [e[0] + (p[0] - e[0]) * (1 - v) + Math.cos(a) * rr, e[1] + (p[1] - e[1]) * (1 - v) + Math.sin(a) * rr * 0.6, e[2] + (p[2] - e[2]) * (1 - v) + Math.sin(a) * rr]; }
        let s = s0 + (s1 - s0) * Math.min(1, u * 1.4); if (o.shrink !== false) s *= 1 - 0.85 * smooth((u - 0.82) / 0.18);
        if (u > reach) s = 0.0001;
        d.position.set(...p); d.scale.set(s, s * 0.85, s); d.rotation.set(i, i * 0.7, 0); d.updateMatrix(); m.setMatrixAt(i, d.matrix);
      }
      m.instanceMatrix.needsUpdate = true;
    };
    g.userData.update(0); return g;
  },

  // The president's big red button on its console (pivot at the floor of the console, front +Z): a dark box with a yellow and black hazard band,
  // a clear flip cover propped open behind, a big red dome; o.pressAt: the dome squashes flat (and the console jumps), o.up: it pops back up after
  bigRedButton(o) {
    const g = grp(), cons = grp(), W = o.w ?? 0.34;
    cons.add(at(box(W, 0.1, W * 0.8, '#2A2D33', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0));
    const band = canvasPlane(W, 0.05, (c, w, h) => { c.fillStyle = '#F2C200'; c.fillRect(0, 0, w, h); c.fillStyle = '#16171A'; for (let x = -h; x < w + h; x += h * 1.2) { c.beginPath(); c.moveTo(x, h); c.lineTo(x + h * 0.6, h); c.lineTo(x + h * 1.2, 0); c.lineTo(x + h * 0.6, 0); c.closePath(); c.fill(); } }, { res: 256 });
    band.position.set(0, 0.05, W * 0.4 + 0.002); cons.add(band);
    cons.add(at(cyl(0.09, 0.1, 0.035, '#1C1E22', 16), 0, 0.117, 0));
    const dome = new THREE.Mesh(new THREE.SphereGeometry(0.085, 16, 8, 0, TAU, 0, PI / 2), lam('#D8231E', { emissive: '#5A0A08', ei: 0.6 })); dome.position.y = 0.13; dome.castShadow = true; addOutline(dome, 0.04); cons.add(dome);
    const cover = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.005, 0.2), lam('#CFE6F2', { opacity: 0.35 })); cover.position.set(0, 0.2, -0.12); cover.rotation.x = -1.2; cons.add(cover);
    g.add(cons);
    g.userData.update = t => {
      const u = o.pressAt == null ? -1 : (t - o.pressAt) / 0.06, back = o.up == null ? 0 : smooth((t - o.up) / 0.2);
      let sy = 1, sx = 1; if (u >= 0) { sy = 0.22 + 0.5 * back; sx = 1.3 - 0.25 * back; if (u < 1) { sy = 1 - 0.78 * u; sx = 1 + 0.3 * u; } }
      dome.scale.set(sx, sy, sx); dome.material.emissiveIntensity = u >= 0 ? 1.4 : 0.6;
      const j = u >= 0 && u < 4 ? 0.025 * Math.sin(u * PI) * (1 - u / 4) : 0; cons.position.y = Math.max(0, j);
    };
    g.userData.update(0); return g;
  },

  // A wall alarm light (pivot at its bracket on the wall, front +Z): a dark base, a big red dome and from o.from two red beams turning o.rps (1.5)
  // times a second, the dome flashing and a red light washing the room (o.light, default on: o.power 3)
  alarmSiren(o) {
    const g = grp(), from = o.from ?? 0, rps = o.rps ?? 1.5, s = o.s ?? 1;
    g.add(at(box(0.16 * s, 0.05 * s, 0.2 * s, '#26282C', { outline: 0.01 }), 0, 0, 0.1 * s), at(cyl(0.11 * s, 0.12 * s, 0.05 * s, '#2E3036', 14), 0, 0.05 * s, 0.14 * s));
    const domeM = new THREE.MeshBasicMaterial({ color: '#6A1414' }), dome = new THREE.Mesh(new THREE.SphereGeometry(0.1 * s, 14, 8, 0, TAU, 0, PI / 2), domeM); dome.position.set(0, 0.075 * s, 0.14 * s); g.add(dome);
    const spin = grp(); spin.position.set(0, 0.12 * s, 0.14 * s); g.add(spin);
    const BL = (o.len ?? 1.6) * s;
    for (const sd of [0, PI]) { const geo = new THREE.ConeGeometry(BL * 0.22, BL, 16, 1, true); geo.translate(0, -BL / 2, 0); geo.rotateZ(PI / 2); const b = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: '#FF3A2A', transparent: true, opacity: o.opacity ?? 0.2, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending })); b.rotation.y = sd; spin.add(b); }
    const L = o.light === false ? null : new THREE.PointLight('#FF2A1A', 0, (o.reach ?? 9) * s, 1.4); if (L) { L.position.set(0, 0.2 * s, 0.6 * s); g.add(L); }
    g.userData.update = t => { const on = t >= from, ph = Math.sin((t - from) * rps * TAU); spin.visible = on; domeM.color.set(on ? (ph > -0.3 ? '#FF3A2A' : '#C02020') : '#6A1414'); spin.rotation.y = (t - from) * rps * TAU; if (L) L.intensity = on ? (o.power ?? 3) * (0.55 + 0.45 * ph) : 0; };
    g.userData.update(-1); return g;
  },

  // A sky full of paratroopers coming down (pivot on the ground under the middle of the drop zone): o.n (30) olive-green men under white
  // canopies, spread over o.w × o.d (30 × 30) and between o.y0 (14) and o.y1 (40) high at t 0, falling o.v (2.2) m/s, swaying; those that reach
  // o.floor (0) vanish; o.colors: the canopy colours (alternate per man); o.size (1)
  parachuteSky(o) {
    const n = o.n ?? 30, W = o.w ?? 30, D = o.d ?? 30, y0 = o.y0 ?? 14, y1 = o.y1 ?? 40, v = o.v ?? 2.2, S = o.size ?? 1, cols = o.colors || ['#F4F2EC', '#E4E0D4', '#F4F2EC', '#C9D2B8'];
    const capGeo = new THREE.SphereGeometry(1.1 * S, 14, 5, 0, TAU, 0, PI * 0.36), cap = new THREE.InstancedMesh(capGeo, lam('#FFFFFF'), n), capIn = new THREE.InstancedMesh(capGeo, new THREE.MeshLambertMaterial({ color: '#A8A49A', side: THREE.BackSide }), n);
    const body = new THREE.InstancedMesh(new THREE.BoxGeometry(0.34 * S, 0.5 * S, 0.24 * S), lam('#56633C'), n), legs = new THREE.InstancedMesh(new THREE.BoxGeometry(0.28 * S, 0.5 * S, 0.2 * S), lam('#4A5532'), n);
    const head = new THREE.InstancedMesh(new THREE.BoxGeometry(0.22 * S, 0.24 * S, 0.2 * S), lam('#D9A57C'), n), helm = new THREE.InstancedMesh(new THREE.SphereGeometry(0.14 * S, 8, 4, 0, TAU, 0, PI / 2), lam('#4E5C32'), n);
    const lineGeo = new THREE.CylinderGeometry(0.01 * S, 0.01 * S, 1, 3); lineGeo.translate(0, 0.5, 0); const lines = new THREE.InstancedMesh(lineGeo, basic('#4A4A44'), n * 4);
    const c = new THREE.Color(); for (let i = 0; i < n; i++) cap.setColorAt(i, c.set(cols[i % cols.length]));
    [cap, capIn, body, legs, head, helm, lines].forEach(m => { m.frustumCulled = false; m.castShadow = false; });
    const g = grp(cap, capIn, body, legs, head, helm, lines), d = new THREE.Object3D(), M = new THREE.Matrix4(), Q = new THREE.Matrix4(), hide = new THREE.Matrix4().makeScale(0, 0, 0);
    const ys = [], xs = [], zs = []; for (let i = 0; i < n; i++) { xs.push((hsh(i * 3 + 1) - 0.5) * W); zs.push((hsh(i * 3 + 2) - 0.5) * D); ys.push(y0 + hsh(i * 3 + 3) * (y1 - y0)); }
    const rim = [0, 1, 2, 3].map(j => { const a = j / 4 * TAU + PI / 4; return [Math.cos(a) * 0.95 * S, 0.45 * S, Math.sin(a) * 0.95 * S]; }), bodyTop = [0, -1.25 * S, 0];
    const lineM = rim.map(p => { const dir = new THREE.Vector3(p[0] - bodyTop[0], p[1] - bodyTop[1], p[2] - bodyTop[2]), L = dir.length(); const q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.normalize()); return new THREE.Matrix4().compose(new THREE.Vector3(...bodyTop), q, new THREE.Vector3(1, L, 1)); });
    g.userData.update = t => {
      for (let i = 0; i < n; i++) {
        const y = ys[i] - v * t, ph = hsh(i + 50) * TAU, x = xs[i] + 0.4 * Math.sin(t * 1.1 + ph), z = zs[i] + 0.3 * Math.cos(t * 0.9 + ph);
        if (y < (o.floor ?? 0) + 1.6 * S) { [cap, capIn, body, legs, head, helm].forEach(m => m.setMatrixAt(i, hide)); for (let j = 0; j < 4; j++) lines.setMatrixAt(i * 4 + j, hide); continue; }
        d.position.set(x, y, z); d.rotation.set(0.1 * Math.sin(t * 1.3 + ph), ph, 0.14 * Math.sin(t * 1.1 + ph)); d.scale.set(1, 1, 1); d.updateMatrix(); M.copy(d.matrix);
        cap.setMatrixAt(i, M); capIn.setMatrixAt(i, M);
        Q.makeTranslation(0, -1.5 * S, 0); body.setMatrixAt(i, M.clone().multiply(Q)); Q.makeTranslation(0, -1.98 * S, 0); legs.setMatrixAt(i, M.clone().multiply(Q));
        Q.makeTranslation(0, -1.12 * S, 0); head.setMatrixAt(i, M.clone().multiply(Q)); Q.makeTranslation(0, -1.0 * S, 0); helm.setMatrixAt(i, M.clone().multiply(Q));
        for (let j = 0; j < 4; j++) lines.setMatrixAt(i * 4 + j, M.clone().multiply(lineM[j]));
      }
      [cap, capIn, body, legs, head, helm, lines].forEach(m => { m.instanceMatrix.needsUpdate = true; });
    };
    g.userData.update(0); return g;
  },

  // One parachute over a man (attach to his torso: offset [0, 0, 0]; the canopy o.up (2.3) above it): a white canopy with darker gores, six lines
  // down to his shoulders; o.collapseAt: it deflates, sags behind him (o.fall 1.7 m down, o.back 0.7 m back) and lies still
  parachute(o) {
    const g = grp(), U = o.up ?? 2.3, R = o.r ?? 1.0, can = grp();
    const capGeo = new THREE.SphereGeometry(R, 16, 6, 0, TAU, 0, PI * 0.38);
    const tex = canvasPlane(1, 1, (c, w, h) => { for (let i = 0; i < 8; i++) { c.fillStyle = i % 2 ? '#E9E5DA' : '#FAF8F2'; c.fillRect(i * w / 8, 0, w / 8 + 1, h); } }, { res: 256 });
    const capM = new THREE.MeshLambertMaterial({ map: tex.material.map, side: THREE.DoubleSide }), cap = new THREE.Mesh(capGeo, capM); cap.castShadow = true; addOutline(cap, 0.02); can.add(cap);
    can.position.y = U - R * 0.8; g.add(can);
    const lines = grp(); for (let i = 0; i < 6; i++) { const a = i / 6 * TAU + PI / 6, sx = Math.cos(a) > 0 ? 0.16 : -0.16; lines.add(rod([sx, 0.42, 0], [Math.cos(a) * R * 0.92, U - R * 0.8 + R * 0.38, Math.sin(a) * R * 0.92], 0.006, '#5A5A52', 3)); }
    g.add(lines);
    g.userData.update = t => {
      const u = o.collapseAt == null ? 0 : smooth((t - o.collapseAt) / (o.dur ?? 0.55));
      can.scale.set(1 + 0.3 * u, 1 - 0.82 * u, 1 + 0.3 * u); can.position.set(0, U - R * 0.8 - (o.fall ?? 2.1) * u, (o.back ?? 1.3) * u * (o.backSign ?? 1)); can.rotation.x = 0.7 * u * (o.backSign ?? 1); lines.visible = u < 0.4;
      cap.rotation.y = 0.15 * Math.sin(t * 1.4) * (1 - u);
    };
    g.userData.update(0); return g;
  },

  // His house after the drop (pivot at the floor, front +Z): a pastel cottage whose roof is buried under a heap of white canopies sagging into it,
  // lines trailing down the facade, a few roof tiles on the lawn, and a pair of olive legs with black boots sticking up out of the chimney,
  // kicking (o.kick [t0, t1]); cottage options pass through (w, d, h, color, roof, door)
  cavedHouse(o) {
    const w = o.w ?? 6.4, d = o.d ?? 7, h = o.h ?? 2.9, rh = o.rh ?? 2.3, g = grp(buildProp('cottage', { w, d, h, rh, color: o.color || '#F2D58A', roof: o.roof || '#B5402F', door: o.door || '#2F7F8C', seed: 5 }));
    const rr = rng(o.seed || 87), heap = grp(), whites = ['#F6F4EE', '#E8E4DA', '#F0EDE4', '#DCD8CC'], roofY = x => h + rh * Math.max(0, 1 - Math.abs(x) / (w / 2 + 0.25));
    for (let i = 0; i < 34; i++) { const xx = (rr() - 0.5) * w * 0.85, zz = (rr() - 0.5) * d * 0.95, s = 0.8 + rr() * 0.7;
      const b = new THREE.Mesh(new THREE.IcosahedronGeometry(s, 1), mat(whites[i % 4])); b.scale.set(1.25, 0.5, 1.1); b.position.set(xx, roofY(xx) - 0.55 + 0.25 * rr(), zz); b.rotation.set(rr() * 0.4, rr() * 3, rr() * 0.4); b.castShadow = true; heap.add(b); }
    for (let i = 0; i < 4; i++) { const cp = new THREE.Mesh(new THREE.SphereGeometry(1.9 + 0.3 * (i % 2), 16, 6, 0, TAU, 0, PI * 0.42), mat(whites[(i + 1) % 4], { doubleSide: true })); const xx = (i - 1.5) * 1.35;
      cp.scale.set(1, 0.5, 1); cp.position.set(xx, roofY(xx) + 0.05, (i % 2 ? -1 : 1) * 1.1); cp.rotation.set((rr() - 0.5) * 0.7, rr() * 3, (i - 1.5) * 0.25); addOutline(cp, 0.012); heap.add(cp); }
    for (let i = 0; i < 6; i++) { const x0 = (i - 2.5) * 0.98, L = 1.1 + rr() * 0.9, top = roofY(x0) - 0.1, dr = at(box(1.02, L, 0.04, whites[i % 4], { outline: 0.012 }), x0, top - L / 2, d / 2 + 0.1 + 0.01 * i, 0, 0, (rr() - 0.5) * 0.25); heap.add(dr); }
    for (let i = 0; i < 7; i++) { const x0 = (rr() - 0.5) * w * 0.8; heap.add(rod([x0, roofY(x0) - 0.6, d / 2 + 0.12], [x0 + (rr() - 0.5) * 0.6, 0.25 + rr() * 1.0, d / 2 + 0.3], 0.014, '#4A4A44', 3)); }
    g.add(heap);
    for (let i = 0; i < 7; i++) g.add(at(box(0.5, 0.05, 0.35, o.roof || '#B5402F', { outline: 0.01 }), (rr() - 0.5) * w * 1.2, 0.03 + i * 0.002, d / 2 + 0.8 + rr() * 2.5, rr() * 0.3, rr() * 3, rr() * 0.3));
    const cx = w * 0.27, cz = d * 0.12, cTop = roofY(cx) + 1.25, chim = at(box(0.6, 2.0, 0.6, '#A4523A', { pivot: 'bottom', outline: 0.01 }), cx, cTop - 2.0, cz); g.add(chim, at(box(0.72, 0.14, 0.72, '#7E3E2C', { outline: 0.01 }), cx, cTop, cz));
    const legs = []; for (const sd of [-1, 1]) { const leg = grp(at(box(0.18, 0.8, 0.19, '#56633C', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(0.21, 0.16, 0.42, '#16171A', { outline: 0.01 }), 0, 0.86, 0.09)); leg.position.set(cx + sd * 0.11, cTop + 0.05, cz); g.add(leg); legs.push(leg); }
    g.userData.update = t => { const on = !o.kick || (t >= o.kick[0] && t < o.kick[1]); legs.forEach((l, i) => { l.rotation.x = on ? 0.4 * Math.sin(t * 10 + i * PI) : 0.05; l.rotation.z = (i ? -1 : 1) * (0.12 + (on ? 0.1 * Math.sin(t * 7 + i) : 0)); }); };
    g.userData.update(0); return g;
  },

  // A barred cell front with a barred door that slams (pivot at the floor in the middle of the front, front +Z: the corridor side): fixed bars o.w
  // (6.4) wide and o.h (2.6) high, the door o.dw (1.0) wide centred at o.dx (0.8), hinged at its left edge, swung open o.open (1.5 rad) toward +Z
  // until o.slamAt, then shut with a bounce; a lock box; the wall above (o.header: its colour, o.headerH 4.4)
  cellDoor(o) {
    const W = o.w ?? 6.4, H = o.h ?? 2.6, DW = o.dw ?? 1.0, DX = o.dx ?? 0.8, g = grp(), barC = o.color || '#3A3E44';
    const barGeo = new THREE.CylinderGeometry(0.028, 0.028, H, 6).translate(0, H / 2, 0), list = [];
    for (let x = -W / 2 + 0.1; x < W / 2; x += 0.2) if (x < DX - DW / 2 - 0.02 || x > DX + DW / 2 + 0.02) list.push(x);
    const fixed = new THREE.InstancedMesh(barGeo, mat(barC), list.length), dd = new THREE.Object3D(); list.forEach((x, i) => { dd.position.set(x, 0, 0); dd.updateMatrix(); fixed.setMatrixAt(i, dd.matrix); }); fixed.castShadow = true; g.add(fixed);
    for (const y of [0.04, H - 0.04, H * 0.45]) g.add(at(box(W, 0.06, 0.06, barC), 0, y, 0));
    if (o.header !== false) g.add(at(box(W + 0.4, o.headerH ?? 4.4, 0.2, o.header || '#93A9A4', { pivot: 'bottom' }), 0, H, 0));
    const door = grp(), hinge = grp(door); hinge.position.set(DX - DW / 2, 0, 0.05); g.add(hinge);
    for (let x = 0.1; x < DW; x += 0.2) door.add(at(cyl(0.03, 0.03, H - 0.1, barC, 6), x, H / 2, 0));
    for (const y of [0.08, H - 0.08, H * 0.45]) door.add(at(box(DW, 0.08, 0.07, '#2C3036', { outline: 0.01 }), DW / 2, y, 0));
    door.add(at(box(0.08, H, 0.08, '#2C3036'), 0.02, H / 2, 0), at(box(0.08, H, 0.08, '#2C3036'), DW - 0.02, H / 2, 0), at(box(0.16, 0.22, 0.12, '#55595F', { outline: 0.01 }), DW - 0.1, H * 0.45, 0.06));
    g.userData.update = t => { let a = -(o.open ?? 1.5); if (o.slamAt != null && t >= o.slamAt - 0.12) { const u = (t - (o.slamAt - 0.12)) / 0.12; a = u < 1 ? -(o.open ?? 1.5) * (1 - u * u) : -0.09 * Math.exp(-(t - o.slamAt) * 9) * Math.sin((t - o.slamAt) * 40); } hinge.rotation.y = a; };
    g.userData.update(0); return g;
  },

  // A long bridge in the fog (pivot at the middle of its deck, the deck along X, top at y 0): a concrete deck o.L (40) × o.W (4.2), railings of
  // dark posts on both sides, lamp posts with glowing lanterns every o.lamp (8) m on the far side, layered white fog banks behind (o.banks)
  fogBridge(o) {
    const L = o.L ?? 40, W = o.W ?? 4.2, g = grp(at(box(L, 0.5, W, '#8E949A', { outline: 0.004 }), 0, -0.25, 0), at(box(L, 0.08, W + 0.3, '#767C82'), 0, -0.52, 0));
    const posts = []; for (let x = -L / 2; x <= L / 2; x += 1.1) for (const sd of [-1, 1]) posts.push([x, 0, sd * (W / 2 - 0.08)]);
    const pg = new THREE.BoxGeometry(0.07, 1.05, 0.07).translate(0, 0.525, 0), pm = new THREE.InstancedMesh(pg, mat('#3E444A'), posts.length), dd = new THREE.Object3D();
    posts.forEach((p, i) => { dd.position.set(...p); dd.updateMatrix(); pm.setMatrixAt(i, dd.matrix); }); g.add(pm);
    for (const sd of [-1, 1]) g.add(at(box(L, 0.08, 0.1, '#3E444A'), 0, 1.06, sd * (W / 2 - 0.08)), at(box(L, 0.05, 0.06, '#3E444A'), 0, 0.5, sd * (W / 2 - 0.08)));
    for (let x = -L / 2 + 2; x <= L / 2; x += (o.lamp ?? 8)) { g.add(at(cyl(0.05, 0.06, 3.6, '#2E3338', 6, { pivot: 'bottom' }), x, 0, -W / 2 + 0.1), rod([x, 3.6, -W / 2 + 0.1], [x, 3.6, -W / 2 + 0.6], 0.03, '#2E3338', 5));
      g.add(at(box(0.22, 0.3, 0.22, '#2E3338', { outline: 0.01 }), x, 3.4, -W / 2 + 0.6), at(box(0.16, 0.2, 0.16, '#FFE9B0', { emissive: '#FFD27A' }), x, 3.38, -W / 2 + 0.6)); }
    if (o.banks !== false) for (let i = 0; i < 4; i++) { const fb = canvasPlane(L * 1.6, 9, (c, w, h) => { const gr = c.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, 'rgba(232,236,240,0)'); gr.addColorStop(0.45, 'rgba(232,236,240,0.75)'); gr.addColorStop(1, 'rgba(232,236,240,0.9)'); c.fillStyle = gr; c.fillRect(0, 0, w, h); }, { res: 128, transparent: true });
      fb.material.depthWrite = false; fb.position.set(0, 1.0 - i * 0.6, -W / 2 - 3 - i * 4); g.add(fb); }
    return g;
  },

  // A stretcher (pivot at its middle, at the height of the poles, the poles along Z): two poles o.L (1.9) long with handles, an olive canvas;
  // o.load 'chipolata': one small sausage lying on it under a white sheet tucked to its top end
  stretcher(o) {
    const L = o.L ?? 1.9, Wd = o.w ?? 0.55, g = grp();
    for (const sd of [-1, 1]) g.add(at(cyl(0.022, 0.022, L, '#7A6A4A', 6), sd * Wd / 2, 0, 0, PI / 2, 0, 0));
    g.add(at(box(Wd, 0.012, L * 0.78, '#6E7A4C', { outline: 0.01 }), 0, 0.005, 0));
    if (o.load === 'chipolata') { const s = buildProp('sausage', { len: 0.44, r: 0.055, lying: true, color: '#C8643A' }); s.rotation.y = PI / 2; s.position.set(0, 0.012, 0.0); g.add(s);
      g.add(at(box(0.24, 0.06, 0.26, '#F4F2EC', { outline: 0.02 }), 0, 0.06, 0.08)); }
    return g;
  },

  // A flamethrower lance (pivot at its rear grip, the lance along +Z): a dark tube o.len (0.95) with a front grip, a small pilot flame at the
  // nozzle; o.fire [[t0, t1], ...]: a huge roaring jet of flame shoots o.jet (3.5) m forward, widening (o.spread 0.55), with an orange light
  flameThrower(o) {
    const LN = o.len ?? 0.95, J = o.jet ?? 3.5, SP = o.spread ?? 0.55, g = grp();
    g.add(at(cyl(0.028, 0.028, LN, '#3A3E36', 8, { outline: 0.01 }), 0, 0, LN / 2, PI / 2, 0, 0), at(box(0.04, 0.12, 0.05, '#2A2C28', { outline: 0.01 }), 0, -0.06, 0), at(box(0.04, 0.1, 0.05, '#2A2C28'), 0, -0.05, LN * 0.5));
    g.add(at(cyl(0.045, 0.035, 0.1, '#55594F', 8, { outline: 0.01 }), 0, 0, LN + 0.04, PI / 2, 0, 0));
    const pilot = noShadow(new THREE.Mesh(new THREE.ConeGeometry(0.02, 0.06, 6), lam('#5AA0FF', { emissive: '#3A7AFF' }))); pilot.rotation.x = PI / 2; pilot.position.set(0, 0.02, LN + 0.12); g.add(pilot);
    const n = 70, jet = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(1, 1), new THREE.MeshBasicMaterial({ color: '#FFFFFF', fog: true }), n); jet.frustumCulled = false; jet.castShadow = false; g.add(jet);
    const cols = ['#FFF1A8', '#FFC23A', '#FF8A1E', '#F2441C'], c = new THREE.Color(); for (let i = 0; i < n; i++) jet.setColorAt(i, c.set(cols[Math.min(3, Math.floor(hsh(i + 7) * 4))]));
    const cone = (r0, col, op) => { const geo = new THREE.ConeGeometry(r0, 1, 10, 1, true); geo.rotateX(-PI / 2); geo.translate(0, 0, 0.5); const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: op, depthWrite: false, side: THREE.DoubleSide, fog: true })); m.castShadow = false; m.position.z = LN + 0.08; g.add(m); return m; };
    const outer = cone(SP * 0.9, '#FF6A1A', 0.85), core = cone(SP * 0.45, '#FFE27A', 0.95);
    const L = new THREE.PointLight('#FF8A2A', 0, 9, 1.3); L.position.set(0, 0.3, LN + J * 0.4); g.add(L);
    const d = new THREE.Object3D();
    g.userData.update = t => {
      const w = inWin(o.fire, t), age = w ? t - w[0] : -1, grow = clamp01(age / 0.18);
      for (let i = 0; i < n; i++) {
        const u = ((i / n) + t * 2.6) % 1, z = LN + 0.1 + u * J * grow, r = (0.07 + u * SP) * (0.7 + 0.5 * hsh(i + 3)), jit = u * SP * 0.5;
        if (!w) { d.scale.setScalar(0.0001); } else {
          const colU = u * 3.2; jet.setColorAt(i, c.set(cols[Math.min(3, Math.floor(colU + hsh(i) * 0.8))]));
          d.position.set(jit * Math.sin(i * 2.1 + t * 13), jit * Math.cos(i * 1.7 + t * 11) + u * u * 0.25, z); d.scale.set(r, r * 0.8, r * 1.3);
        }
        d.updateMatrix(); jet.setMatrixAt(i, d.matrix);
      }
      jet.instanceMatrix.needsUpdate = true; if (jet.instanceColor) jet.instanceColor.needsUpdate = true;
      L.intensity = w ? 4 + 1.2 * Math.sin(t * 23) : 0; pilot.scale.setScalar(1 + 0.2 * Math.sin(t * 19));
      for (const [m, k] of [[outer, 1], [core, 0.85]]) { m.visible = !!w; const f = 1 + 0.12 * Math.sin(t * 29 + k * 3) + 0.06 * Math.sin(t * 47 + k); m.scale.set(f, f * (1 + 0.1 * Math.sin(t * 17)), Math.max(0.001, J * grow * k)); }
    };
    g.userData.update(-1); return g;
  },

  // A flamethrower's fuel pack (attach to the back of the torso: offset [0, 0.3, -0.2]): two olive tanks side by side with a strap and a valve
  fuelTanks(o) {
    const g = grp(); for (const sd of [-1, 1]) g.add(at(cyl(0.085, 0.085, 0.5, '#5C6B3C', 10, { outline: 0.01 }), sd * 0.1, 0, 0), at(sphere(0.085, '#5C6B3C', 1), sd * 0.1, 0.25, 0), at(sphere(0.085, '#5C6B3C', 1), sd * 0.1, -0.25, 0));
    g.add(at(box(0.32, 0.05, 0.2, '#3A3E36'), 0, 0.1, 0), at(cyl(0.02, 0.02, 0.08, '#B8BCC0', 6), 0, 0.33, 0));
    return g;
  },

  // A bed of glowing embers (pivot at its middle on the ground; its top 6 cm up): o.w × o.d (8 × 3) of charcoal with orange cracks that pulse,
  // black lumps, a few small flames and sparks rising (o.sparks 24)
  emberBed(o) {
    const W = o.w ?? 8, D = o.d ?? 3, rr = rng(o.seed || 91), g = grp();
    const skin = canvasPlane(W, D, (c, w, h) => { c.fillStyle = '#1E1A18'; c.fillRect(0, 0, w, h); for (let i = 0; i < 90; i++) { const x = rr() * w, y = rr() * h, r = (0.02 + rr() * 0.05) * w; const gr = c.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, 'rgba(255,170,60,0.95)'); gr.addColorStop(0.4, 'rgba(240,80,20,0.7)'); gr.addColorStop(1, 'rgba(60,20,10,0)'); c.fillStyle = gr; c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill(); }
      c.strokeStyle = 'rgba(255,140,40,0.9)'; c.lineWidth = w * 0.004; for (let i = 0; i < 40; i++) { let x = rr() * w, y = rr() * h; c.beginPath(); c.moveTo(x, y); for (let k = 0; k < 4; k++) { x += (rr() - 0.5) * w * 0.06; y += (rr() - 0.5) * h * 0.1; c.lineTo(x, y); } c.stroke(); } }, { res: 1024, emissive: 0.9 });
    skin.rotation.x = -PI / 2; skin.position.y = 0.06; skin.receiveShadow = true; g.add(skin);
    for (let i = 0; i < (o.lumps ?? 40); i++) g.add(at(new THREE.Mesh(new THREE.DodecahedronGeometry(0.04 + rr() * 0.06, 0), mat(rr() < 0.3 ? '#3A2E28' : '#151312')), (rr() - 0.5) * W, 0.07, (rr() - 0.5) * D, rr() * 3, rr() * 3, 0));
    const fl = grp(); for (let i = 0; i < (o.flames ?? 10); i++) { const f = grp(); [0, 1].forEach(j => { const cn = noShadow(new THREE.Mesh(new THREE.ConeGeometry(0.07 - j * 0.03, 0.26 - j * 0.08, 6), basic(['#FF7A1A', '#FFD04A'][j]))); cn.position.y = 0.14; f.add(cn); }); f.position.set((rr() - 0.5) * W * 0.9, 0.06, (rr() - 0.5) * D * 0.9); fl.add(f); }
    g.add(fl);
    const ns = o.sparks ?? 24, sp = new THREE.InstancedMesh(new THREE.BoxGeometry(0.025, 0.025, 0.025), new THREE.MeshBasicMaterial({ color: '#FFB040' }), ns); sp.frustumCulled = false; sp.castShadow = false; g.add(sp);
    const d = new THREE.Object3D(), sx = [], sz = []; for (let i = 0; i < ns; i++) { sx.push((rr() - 0.5) * W); sz.push((rr() - 0.5) * D); }
    g.userData.update = t => { skin.material.emissiveIntensity = 0.75 + 0.2 * Math.sin(t * 2.3) + 0.08 * Math.sin(t * 7.1);
      fl.children.forEach((f, i) => f.scale.set(1, 0.8 + 0.35 * Math.sin(t * 13 + i * 1.9), 1));
      for (let i = 0; i < ns; i++) { const u = ((i / ns) + t * 0.45) % 1; d.position.set(sx[i] + 0.2 * Math.sin(t * 2 + i), 0.1 + u * 2.2, sz[i]); d.scale.setScalar(1 - u); d.updateMatrix(); sp.setMatrixAt(i, d.matrix); }
      sp.instanceMatrix.needsUpdate = true; };
    g.userData.update(0); return g;
  },

  // Soot on a face, in charcoal-grey patches (attach to the head joint: offset [0, 0, 0]): smudges on the forehead, the cheeks, the nose and the
  // chin, leaving the eyes clear; o.w (0.2), o.h (0.3), o.y (0.23), o.z (0.089): the face's size, the middle's height and the front
  sootPatches(o) {
    const W = o.w ?? 0.2, H = o.h ?? 0.3, rr = rng(o.seed || 93);
    const m = canvasPlane(W, H, (c, w, h) => { c.clearRect(0, 0, w, h);
      const blob = (x, y, rx, ry, col) => { c.fillStyle = col; c.beginPath(); for (let i = 0; i <= 12; i++) { const a = i / 12 * TAU, k = 0.75 + 0.35 * rr(); const px = x + Math.cos(a) * rx * k, py = y + Math.sin(a) * ry * k; if (i === 0) c.moveTo(px, py); else c.lineTo(px, py); } c.closePath(); c.fill(); };
      [[0.3, 0.12, 0.16, 0.06], [0.72, 0.1, 0.12, 0.05], [0.18, 0.62, 0.12, 0.09], [0.82, 0.58, 0.11, 0.1], [0.5, 0.5, 0.06, 0.08], [0.45, 0.86, 0.16, 0.07], [0.62, 0.74, 0.08, 0.05]].forEach(([x, y, rx, ry], i) => blob(x * w, y * h, rx * w, ry * h, i % 2 ? 'rgba(58,56,54,0.92)' : 'rgba(78,75,72,0.88)'));
      c.fillStyle = 'rgba(40,38,36,0.9)'; for (let i = 0; i < 18; i++) { c.beginPath(); c.arc(rr() * w, (rr() < 0.5 ? rr() * 0.2 : 0.55 + rr() * 0.4) * h, (0.01 + rr() * 0.02) * w, 0, TAU); c.fill(); } }, { res: 256, transparent: true });
    m.position.set(0, o.y ?? 0.23, o.z ?? 0.089); m.castShadow = false; m.receiveShadow = false; return grp(m);
  },

  // An empty paper plate (pivot at its middle, flat in XZ): white, a fluted rim; o.r (0.11); o.tilt: it droops a little
  paperPlate(o) {
    const R = o.r ?? 0.11, g = grp(at(cyl(R * 0.72, R * 0.7, 0.006, '#F7F5EE', 18), 0, 0, 0));
    const rim = new THREE.Mesh(new THREE.CylinderGeometry(R, R * 0.72, 0.022, 18, 1, true), mat('#EDEAE0', { doubleSide: true })); rim.position.y = 0.012; addOutline(rim, 0.02); g.add(rim);
    if (o.tilt) g.rotation.z = o.tilt; if (o.tiltX) g.rotation.x = o.tiltX; return g;
  },

  // A wine glass (pivot at the middle of its stem, upright +Y): a foot, a stem, a clear bowl with red wine (o.wine) or golden (o.color)
  partyGlass(o) {
    const g = grp(at(cyl(0.035, 0.035, 0.005, '#E6F2F4', 12), 0, -0.05, 0), at(cyl(0.005, 0.005, 0.1, '#E6F2F4', 6), 0, 0, 0));
    const bowl = new THREE.Mesh(new THREE.CylinderGeometry(0.042, 0.025, 0.08, 12, 1, true), lam('#D9EEF2', { opacity: 0.45 })); bowl.position.y = 0.09; g.add(bowl);
    g.add(at(cyl(0.036, 0.024, 0.04, o.color || '#8E1F2E', 12), 0, 0.073, 0)); g.userData.grip = [0, 0, 0]; return g;
  },

  // A garland of little triangle flags between two points (pivot anywhere: o.a and o.b in the prop's frame), sagging o.sag (0.35), o.n (14) flags
  // in o.colors, fluttering
  gardenBunting(o) {
    const A = o.a || [-2, 2, 0], B = o.b || [2, 2, 0], n = o.n ?? 14, sag = o.sag ?? 0.35, cols = o.colors || ['#E8508A', '#F2C94C', '#5FA8D3', '#7CC25A', '#F2A63C'], g = grp(), fl = [];
    const pt = u => [A[0] + (B[0] - A[0]) * u, A[1] + (B[1] - A[1]) * u - sag * 4 * u * (1 - u), A[2] + (B[2] - A[2]) * u];
    for (let i = 0; i < 24; i++) g.add(rod(pt(i / 24), pt((i + 1) / 24), 0.006, '#3A3A3A', 3));
    const tri = new THREE.BufferGeometry(); tri.setAttribute('position', new THREE.Float32BufferAttribute([-0.09, 0, 0, 0.09, 0, 0, 0, -0.2, 0], 3)); tri.computeVertexNormals();
    const ang = Math.atan2(B[2] - A[2], B[0] - A[0]);
    for (let i = 0; i < n; i++) { const m = new THREE.Mesh(tri, new THREE.MeshLambertMaterial({ color: cols[i % cols.length], side: THREE.DoubleSide })); m.position.set(...pt((i + 0.5) / n)); m.rotation.y = -ang; g.add(m); fl.push(m); }
    g.userData.update = t => fl.forEach((m, i) => { m.rotation.x = 0.25 * Math.sin(t * 3 + i * 0.8); });
    g.userData.update(0); return g;
  },

  // An invented flag on a pole (pivot at the foot): a mustard field with a brown sausage crossed with a grey fork, a red stripe at the hoist,
  // waving; o.h (3.2) pole, o.w (1.2) × o.fh (0.8) cloth
  bbqFlag(o) {
    const H = o.h ?? 3.2, FW = o.w ?? 1.2, FH = o.fh ?? 0.8, g = grp(at(cyl(0.03, 0.035, H, '#E8E8E4', 6, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(sphere(0.06, '#E2B53C', 1), 0, H + 0.03, 0));
    const c = document.createElement('canvas'); c.width = 384; c.height = 256; const x = c.getContext('2d');
    x.fillStyle = o.field || '#F2C84B'; x.fillRect(0, 0, 384, 256); x.fillStyle = o.stripe || '#C8322A'; x.fillRect(0, 0, 70, 256);
    x.save(); x.translate(228, 128); x.rotate(-0.6); x.fillStyle = '#9A9EA4'; x.fillRect(-10, -100, 20, 200); for (const dx of [-16, 0, 16]) x.fillRect(dx - 4, -130, 8, 40); x.restore();
    x.save(); x.translate(228, 128); x.rotate(0.6); x.fillStyle = '#8A3A1E'; x.beginPath(); x.ellipse(0, 0, 26, 95, 0, 0, TAU); x.fill(); x.strokeStyle = '#5A2210'; x.lineWidth = 6; for (const yy of [-40, 0, 40]) { x.beginPath(); x.moveTo(-20, yy - 8); x.lineTo(20, yy + 8); x.stroke(); } x.restore();
    const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
    const geo = new THREE.PlaneGeometry(FW, FH, 14, 1); geo.translate(FW / 2, 0, 0); const base = geo.attributes.position.array.slice();
    const cloth = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ map: tex, side: THREE.DoubleSide })); cloth.position.set(0.03, H - FH / 2 - 0.05, 0); cloth.castShadow = true; g.add(cloth);
    g.userData.update = t => { const p = geo.attributes.position; for (let i = 0; i < p.count; i++) { const bx = base[i * 3]; p.setZ(i, 0.12 * (bx / FW) * Math.sin(bx * 5 - t * 6 + (o.phase ?? 0))); } p.needsUpdate = true; };
    g.userData.update(0); return g;
  },

  // What is left of a picket fence after the fire (pivot at its middle, along X): o.L (4) of black stubs of uneven height, two leaning, a rail
  // stump, a faint ember glow at a foot
  charredFence(o) {
    const L = o.L ?? 4, rr = rng(o.seed || 97), g = grp();
    for (let x = -L / 2; x <= L / 2; x += 0.24) { const h = 0.12 + rr() * 0.55, lean = rr() < 0.15 ? (rr() - 0.5) * 0.8 : (rr() - 0.5) * 0.1; g.add(at(box(0.1, h, 0.035, rr() < 0.5 ? '#1D1B1A' : '#2B2725', { pivot: 'bottom', outline: 0.01 }), x, 0, 0, 0, 0, lean)); }
    g.add(at(box(L * 0.45, 0.06, 0.05, '#221F1D'), -L * 0.22, 0.3, 0.03, 0, 0, 0.03));
    g.add(at(sphere(0.05, '#3A2A22', 1, { emissive: '#C04A1A' }), L * 0.18, 0.04, 0.05));
    return g;
  },
};
