// « La rambarde » (story 84): this man got his head stuck in the railing of his balcony; the firemen brought out the big ladder; he lives on the
// ground floor; twelve firemen pulled his legs and he grew twenty centimetres; the railing was declared a natural disaster; the president ordered
// the head out and the head held its ground; the district was evacuated by helicopter, except him; the bomb squad blew the building up around the
// railing; the building got a state funeral; the railing was listed as a historic monument, head included; he tilted his head and it came out; he
// was arrested for theft; his head was seized; he rents his head from the State.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere, addOutline, mat, rng } from './style.js';
import { grp, at, canvasPlane, buildProp, rod } from './props.js';

const PI = Math.PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = x => { const u = clamp01(x), c = 1.70158; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const basic = (c, o = {}) => new THREE.MeshBasicMaterial({ color: c, transparent: o.opacity != null, opacity: o.opacity ?? 1, depthWrite: o.opacity == null, side: o.side || THREE.FrontSide });
const lam = (c, o = {}) => new THREE.MeshLambertMaterial({ color: c, emissive: new THREE.Color(o.emissive || '#000000'), emissiveIntensity: o.ei ?? 1, flatShading: true, transparent: o.opacity != null, opacity: o.opacity ?? 1, depthWrite: o.opacity == null, side: o.side || THREE.FrontSide });
const noShadow = m => { m.traverse(c => { c.castShadow = false; }); return m; };

// red-and-white hazard stripes on a canvas (diagonal), for tape
function stripeTex(red = '#D8322C', white = '#F6F2EA') {
  const c = document.createElement('canvas'); c.width = 128; c.height = 32; const x = c.getContext('2d');
  x.fillStyle = white; x.fillRect(0, 0, 128, 32); x.fillStyle = red;
  for (let i = -2; i < 8; i++) { x.beginPath(); x.moveTo(i * 24, 32); x.lineTo(i * 24 + 12, 32); x.lineTo(i * 24 + 24, 0); x.lineTo(i * 24 + 12, 0); x.closePath(); x.fill(); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = THREE.RepeatWrapping; return t;
}
// a strip of tape from a to b (world-ish points in the prop frame), w wide, its flat face turned to `face` (a direction)
function tapeStrip(a, b, w, face = [0, 0, 1]) {
  const A = new THREE.Vector3(...a), B = new THREE.Vector3(...b), L = A.distanceTo(B), tex = stripeTex(); tex.repeat.set(Math.max(1, L / 0.35), 1);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(L, w), new THREE.MeshLambertMaterial({ map: tex, side: THREE.DoubleSide }));
  const X = B.clone().sub(A).normalize(), F = new THREE.Vector3(...face).normalize(), Y = F.clone().cross(X).normalize(), Z = X.clone().cross(Y).normalize();
  m.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(X, Y, Z)); m.position.copy(A).add(B).multiplyScalar(0.5); m.castShadow = false; return m;
}

export const RAMBARDE_PROPS = {
  // The firemen's giant telescopic ladder (pivot at its foot, the turntable: put it on the roof of a fireTruck): a red turntable and three nested
  // silver sections that lean toward +Z at o.elev degrees (72) and slide out to o.len (54 m) over o.extend [t0, dur] (without it: fully out);
  // o.cloud (default true): a bank of white cloud puffs round the top, so the tip vanishes into the clouds; o.cloudR (5 m)
  skyLadder(o) {
    const L = o.len ?? 54, el = (o.elev ?? 72) * PI / 180, g = grp(), arm = grp(), sec = [], SL = L / 3;
    g.add(at(cyl(0.7, 0.8, 0.35, '#B7281F', 12, { pivot: 'bottom' }), 0, 0, 0), at(box(0.9, 0.7, 1.1, '#C8322A', { outline: 0.012 }), 0, 0.6, 0));
    arm.position.set(0, 0.9, 0); arm.rotation.x = PI / 2 - el; g.add(arm);
    const W = [0.62, 0.52, 0.42], RC = ['#B9BDBF', '#C9CDCF', '#D9DCDE'];
    for (let s = 0; s < 3; s++) {
      const sg = grp(), w = W[s], rails = [], n = Math.floor(SL / 0.42);
      for (const sd of [-1, 1]) { const r_ = at(box(o.rail ?? 0.12, SL, 0.12, RC[s], { pivot: 'bottom', outline: 0.012 }), sd * w / 2, 0, 0.02 * s); sg.add(r_); rails.push(r_); }
      const rungs = new THREE.InstancedMesh(new THREE.BoxGeometry(w, 0.07, 0.07), mat('#E2E5E7'), n), M = new THREE.Matrix4();
      for (let i = 0; i < n; i++) { M.makeTranslation(0, 0.2 + i * 0.42, 0.02 * s); rungs.setMatrixAt(i, M); }
      sg.add(rungs); arm.add(sg); sec.push(sg);
    }
    const cloud = grp();
    if (o.cloud !== false) {
      const R = o.cloudR ?? 5, r = rng(o.seed || 84), m = lam('#FFFFFF', { emissive: '#FFFFFF', ei: 0.35 });
      for (let i = 0; i < 16; i++) { const a = r() * 2 * PI, d = R * (0.2 + 0.8 * r()), s = R * (0.35 + 0.45 * r()), b = new THREE.Mesh(new THREE.IcosahedronGeometry(s, 1), m);
        b.position.set(Math.cos(a) * d, (r() - 0.4) * R * 0.5, Math.sin(a) * d); b.scale.y = 0.62; b.castShadow = false; cloud.add(b); }
      cloud.position.set(0, 0.9 + Math.sin(el) * L * 0.97, Math.cos(el) * L * 0.97); g.add(cloud);
    }
    g.userData.update = t => {
      const e = o.extend ? smooth((t - o.extend[0]) / Math.max(0.01, o.extend[1])) : 1, k = o.extend ? outBack(clamp01((t - o.extend[0]) / Math.max(0.01, o.extend[1]))) : 1;
      sec[1].position.y = SL * 0.98 * Math.min(1.03, k); sec[2].position.y = 2 * SL * 0.98 * Math.min(1.03, k);
      arm.rotation.z = o.extend ? 0.01 * Math.sin(t * 9) * (1 - e) : 0.004 * Math.sin(t * 1.3);
    };
    g.userData.update(0); return g;
  },

  // His raised ground-floor balcony on the facade (pivot on the pavement at the foot of the wall, under the middle of the balcony; the wall at local
  // z 0, the street toward +Z): o.wall (true): a patch of cream stone facade o.ww (5) x o.wh (2.75) with a dark plinth, a French window behind the
  // balcony; the slab at o.fy (1.15 m) projecting o.d (0.55) on two corbels; an iron railing at its front edge, o.w (2.0) wide, o.rh (1.25) tall,
  // upright bars every o.gap (0.11 m); the two bars round o.hx (0) are bowed apart by o.bow (0.05 m) at o.bowY (0.62) of their height (where
  // the head went in).
  // o.quiver [t0, dur, amp]: the bars ring like a tuning fork (decaying side-to-side shiver); o.tape: red-and-white tape wound round the railing;
  // o.char: blackened iron and soot-dark stone; o.ruin: no wall, the slab stands on a cracked blackened pier with chunks round its foot
  balconyRail(o) {
    const g = grp(), fy = o.fy ?? 1.15, d = o.d ?? 0.55, w = o.w ?? 2.0, rh = o.rh ?? 1.25, gap = o.gap ?? 0.11, hx = o.hx ?? 0, ch = !!o.char;
    const iron = ch ? '#1A1714' : '#20242C', stone = ch ? '#5A524A' : (o.stone || '#EFE6D2'), plinth = ch ? '#3E3833' : '#CFC3AA';
    if (o.wall !== false && !o.ruin) {
      const ww = o.ww ?? 5, wh = o.wh ?? 2.75;
      g.add(at(box(ww, wh, 0.3, stone), 0, wh / 2, -0.15), at(box(ww + 0.02, fy - 0.05, 0.32, plinth), 0, (fy - 0.05) / 2, -0.15));
      for (const y of [0.45, 1.6, 2.15]) g.add(at(box(ww + 0.03, 0.025, 0.31, ch ? '#3A3430' : '#D8CCB2'), 0, y, -0.14));
      const wx = 1.1, wy = fy + 0.08, wht = Math.min(wh - fy - 0.15, 1.75);
      g.add(at(box(wx + 0.12, wht + 0.1, 0.06, '#2E3640'), 0, wy + wht / 2, 0.01), at(box(wx, wht, 0.04, ch ? '#141210' : '#5D7891', { emissive: ch ? '#000000' : '#1A2A38' }), 0, wy + wht / 2, 0.03));
      g.add(at(box(0.05, wht, 0.06, '#2E3640'), 0, wy + wht / 2, 0.05), at(box(wx, 0.05, 0.06, '#2E3640'), 0, wy + wht * 0.62, 0.05));
      if (!ch) g.add(at(box(0.3, wht * 0.7, 0.01, '#9FC0D8', { emissive: '#3A5870' }), -0.27, wy + wht * 0.55, 0.055, 0, 0, 0.12));
    }
    if (o.ruin) {
      const r = rng(o.seed || 7);
      g.add(at(box(0.55, fy, 0.5, '#4A433D', { outline: 0.01 }), 0, fy / 2, d * 0.45), at(box(0.62, 0.05, 0.56, '#2E2A27'), 0, fy * 0.55, d * 0.45, 0, 0, 0.08));
      for (let i = 0; i < 9; i++) { const s = 0.12 + r() * 0.22, b = sphere(s, ['#5F5650', '#4A433D', '#7A7068'][i % 3], 0); b.position.set((r() - 0.5) * 1.6, s * 0.5, d * 0.45 + (r() - 0.5) * 1.2); b.rotation.set(r() * 3, r() * 3, 0); g.add(b); }
    }
    g.add(at(box(w + 0.1, 0.14, d, ch ? '#4E4640' : '#E3D8C2', { outline: 0.01 }), 0, fy, d / 2));
    for (const sd of [-1, 1]) g.add(at(box(0.14, 0.32, d * 0.9, ch ? '#463F39' : '#DACDB2', { taper: { x: 1, z: 0.3 } }), sd * (w / 2 - 0.15), fy - 0.22, d * 0.45, PI, 0, 0));
    const zr = d - 0.04, y0 = fy + 0.07, y1 = fy + rh, bars = grp(); g.add(bars);
    g.add(at(box(w, 0.06, 0.07, iron, { outline: 0.01 }), 0, y1, zr), at(box(w, 0.04, 0.05, iron), 0, y0 + 0.06, zr));
    for (const sd of [-1, 1]) g.add(at(box(0.06, rh, 0.06, iron), sd * w / 2, fy + rh / 2, zr));
    const nb = Math.floor(w / gap) - 1;
    for (let i = 1; i <= nb; i++) {
      const x = -w / 2 + i * gap, near = Math.abs(x - hx) < gap * 0.75, piv = grp();
      piv.position.set(x, y0, zr); piv.userData.ph = hsh(i) * 6;
      if (near) { const sd = Math.sign(x - hx) || 1, mid = [sd * (o.bow ?? 0.05), (y1 - y0) * (o.bowY ?? 0.62), 0];
        piv.add(rod([0, 0, 0], mid, 0.013, iron), rod(mid, [0, y1 - y0, 0], 0.013, iron)); }
      else piv.add(at(cyl(0.012, 0.012, y1 - y0, iron, 6, { pivot: 'bottom' }), 0, 0, 0));
      bars.add(piv);
    }
    if (o.tape) {
      const tz = zr + 0.05, ys = [fy + 0.25, fy + 0.62, fy + 1.0];
      g.add(tapeStrip([-w / 2 - 0.05, ys[0], tz], [w / 2 + 0.05, ys[2], tz], 0.11), tapeStrip([-w / 2 - 0.05, ys[2], tz + 0.01], [w / 2 + 0.05, ys[0], tz + 0.01], 0.11),
            tapeStrip([-w / 2 - 0.05, ys[1], tz + 0.02], [w / 2 + 0.05, ys[1] + 0.05, tz + 0.02], 0.11), tapeStrip([-w / 2 - 0.05, y1 + 0.02, zr], [w / 2 + 0.05, y1 + 0.02, zr], 0.1, [0, 1, 0.3]));
    }
    g.userData.update = t => {
      const q = o.quiver; let a = 0;
      if (q && t >= q[0]) { const u = t - q[0]; a = (q[2] ?? 0.12) * Math.exp(-u * 3.2 / Math.max(0.2, q[1] ?? 1.2)) * (u < (q[1] ?? 1.2) * 1.6 ? 1 : 0); }
      bars.children.forEach(p => { p.rotation.z = a ? a * Math.sin((t - q[0]) * 62 + p.userData.ph) : 0; });
    };
    g.userData.update(0); return g;
  },

  // A white site hard hat (pivot at the bottom of its band; attach to the head with offset [0, ~0.45, 0]): a dome, a ridge, a front peak; o.w (0.26)
  hardHat(o) {
    const w = o.w ?? 0.26, c = o.color || '#F4F2EC', g = grp(), dome = new THREE.Mesh(new THREE.SphereGeometry(w * 0.6, 14, 8, 0, 2 * PI, 0, PI / 2), mat(c));
    dome.scale.set(1, 0.85, 1.1); dome.castShadow = true; addOutline(dome, 0.04); g.add(dome);
    g.add(at(box(w * 0.12, w * 0.12, w * 1.25, c), 0, w * 0.5, 0), at(cyl(w * 0.66, w * 0.66, 0.018, c, 16), 0, 0.01, 0), at(box(w * 0.7, 0.02, w * 0.32, c), 0, 0.012, w * 0.66));
    return g;
  },

  // A bomb-disposal helmet (pivot at the bottom; attach to the head with offset [0, ~0.02, 0]): a big padded olive dome down over the shoulders with a
  // dark tinted visor in front; o.w (0.5)
  bombHelmet(o) {
    const w = o.w ?? 0.5, c = o.color || '#4E5A3A', g = grp(), dome = sphere(w * 0.55, c, 1); dome.scale.set(1, 1.1, 1); dome.position.y = w * 0.62; addOutline(dome, 0.03); g.add(dome);
    g.add(at(box(w * 0.78, w * 0.4, 0.04, '#141A20', { emissive: '#0A1218' }), 0, w * 0.68, w * 0.5), at(box(w * 0.5, w * 0.08, 0.02, '#6A8090', { emissive: '#2A4050' }), -w * 0.1, w * 0.8, w * 0.53, 0, 0, 0.15));
    g.add(at(cyl(w * 0.6, w * 0.7, w * 0.28, c, 12), 0, w * 0.1, 0));
    return g;
  },

  // A bomb-disposal suit's padded front (pivot at the chest; attach to the torso): a thick olive slab with quilted lines and a high collar; o.w (0.62)
  bombVest(o) {
    const w = o.w ?? 0.62, c = o.color || '#56623F', g = grp();
    g.add(at(box(w, w * 1.15, 0.2, c, { outline: 0.012 }), 0, 0, 0.12), at(box(w * 0.9, w * 0.25, 0.3, c), 0, w * 0.6, 0.02));
    for (let i = 0; i < 4; i++) g.add(at(box(w * 0.92, 0.02, 0.01, '#3E4730'), 0, -w * 0.4 + i * w * 0.27, 0.225));
    return g;
  },

  // A detonator box (front +Z): a wooden crate, a T-handle on a rod that goes down at o.pushAt (s) in 0.1 s, two terminals and a wire that runs along the
  // ground toward +X for o.wire (8 m)
  detonator(o) {
    const g = grp(), h = grp(), up = 0.3;
    g.add(at(box(0.36, 0.28, 0.26, '#8A5A32', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(0.38, 0.03, 0.28, '#5A3A20'), 0, 0.28, 0));
    for (const sd of [-1, 1]) g.add(at(cyl(0.02, 0.02, 0.04, '#C9A040', 6), sd * 0.12, 0.31, 0.08));
    h.add(at(cyl(0.012, 0.012, 0.32, '#9A9EA2', 6, { pivot: 'top' }), 0, 0, 0), at(box(0.3, 0.04, 0.04, '#1E1E22', { outline: 0.005 }), 0, 0.02, 0));
    h.position.set(0, 0.29 + up, 0); g.add(h);
    if (o.wire !== 0) g.add(rod([0.12, 0.31, 0.08], [0.6, 0.02, 0.2], 0.008, '#C2302A'), rod([0.6, 0.02, 0.2], [o.wire ?? 8, 0.02, 0.6], 0.008, '#C2302A'));
    g.userData.update = t => { const k = o.pushAt == null ? 0 : clamp01((t - o.pushAt) / 0.1); h.position.y = 0.29 + up * (1 - k * k) + 0.02 * k * Math.sin(Math.max(0, t - o.pushAt - 0.1) * 40) * Math.exp(-Math.max(0, t - o.pushAt - 0.1) * 12); };
    g.userData.update(0); return g;
  },

  // A black balaclava over a box head (attach to the head joint, offset [0, 0, 0]): a black shell o.w (0.29) x o.h (0.47) x o.d (0.27) with the eye band
  // left open (o.eye [y0, y1], 0.25-0.33 m up the head) so the painted eyes show
  balaclava(o) {
    const w = o.w ?? 0.29, h = o.h ?? 0.47, d = o.d ?? 0.27, e = o.eye || [0.25, 0.33], c = '#16171A', g = grp(), s = 1.08;
    g.add(at(box(w * s, h - e[1] + 0.02, d * s, c), 0, (h + e[1]) / 2 + 0.01, 0), at(box(w * s, e[0] + 0.01, d * s, c), 0, e[0] / 2, 0));
    for (const sd of [-1, 1]) g.add(at(box(w * 0.14, e[1] - e[0], d * s, c), sd * w * 0.47, (e[0] + e[1]) / 2, 0));
    g.add(at(box(w * 0.2, e[1] - e[0], d * 0.6, c), 0, (e[0] + e[1]) / 2, -d * 0.25));
    return g;
  },

  // A brick (pivot at its bottom middle): terracotta, 0.24 x 0.075 x 0.115, chipped edges; o.char: sooty
  brick(o) {
    const c = o.char ? '#5A3A2E' : (o.color || '#B5553A'), g = grp(); g.add(at(box(0.24, 0.075, 0.115, c, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0));
    g.add(at(box(0.04, 0.02, 0.02, '#D8C9AA'), -0.1, 0.075, 0.05), at(box(0.25, 0.012, 0.118, '#D8CDB4'), 0, 0.0, 0));
    return g;
  },

  // A rifle (pivot at the grip; the barrel along +Y): a wooden stock and a dark barrel, 0.95 m long; held upright on a shoulder
  rifle(o) {
    const g = grp(); g.add(at(box(0.05, 0.36, 0.08, '#6A4A2E', { outline: 0.005 }), 0, -0.2, 0), at(cyl(0.014, 0.014, 0.62, '#26282C', 6, { pivot: 'bottom' }), 0, -0.02, 0.01));
    g.add(at(box(0.03, 0.08, 0.04, '#26282C'), 0, 0.02, 0.03)); g.userData.grip = [0, 0, 0]; return g;
  },

  // A big bronze plaque on a stone stand (pivot on the ground under its front edge; front +Z): a plate o.w (1.2) x o.h (0.9) with a raised border, a
  // thick engraved arrow pointing o.dir degrees in its plane (0 = toward +X, 90 = up) and a few lines of inscription marks; o.drapeAt [t, dur]: a red
  // velvet drape that covered it slides down and away (unveiled); o.post (1.0 m): the stand's height
  bronzePlaque(o) {
    const W = o.w ?? 1.2, H = o.h ?? 0.9, ph = o.post ?? 1.0, g = grp(), plate = grp(), bz = '#B07A3A', dk = '#6E4A22';
    g.add(at(box(W * 0.5, ph, 0.3, '#C9BFA8', { pivot: 'bottom', outline: 0.01 }), 0, 0, -0.1));
    plate.position.set(0, ph + H / 2, 0.08); plate.rotation.x = -0.12; g.add(plate);
    plate.add(at(box(W, H, 0.06, bz, { outline: 0.012, emissive: '#2A1A08' }), 0, 0, 0));
    for (const [w_, h_, x, y] of [[W, 0.06, 0, H / 2 - 0.03], [W, 0.06, 0, -H / 2 + 0.03], [0.06, H, -W / 2 + 0.03, 0], [0.06, H, W / 2 - 0.03, 0]]) plate.add(at(box(w_, h_, 0.08, '#D49A52'), x, y, 0.01));
    const s = Math.min(W, H) * 0.36, sh = new THREE.Shape([[-1, 0.18], [0.25, 0.18], [0.25, 0.55], [1, 0], [0.25, -0.55], [0.25, -0.18], [-1, -0.18]].map(([x, y]) => new THREE.Vector2(x * s, y * s)));
    const arrow = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: 0.03, bevelEnabled: false }), mat(dk)); addOutline(arrow, 0.02);
    arrow.rotation.z = (o.dir ?? 0) * PI / 180; arrow.position.set(0, -H * 0.08, 0.03); plate.add(arrow);
    for (let i = 0; i < 2; i++) plate.add(at(box(W * (0.7 - i * 0.2), 0.035, 0.02, dk), 0, H * 0.32 - i * 0.09, 0.035));
    const drape = grp(); drape.add(at(box(W * 1.12, H * 1.15, 0.05, '#9A1E28', { outline: 0.01 }), 0, 0, 0), at(box(W * 1.14, 0.06, 0.07, '#E2B53C'), 0, -H * 0.56, 0.01));
    drape.position.set(0, 0, 0.07); plate.add(drape);
    g.userData.update = t => { const dr = o.drapeAt; if (!dr) { drape.visible = false; return; } const k = clamp01((t - dr[0]) / (dr[1] ?? 0.45));
      drape.visible = k < 1; drape.position.y = -k * k * H * 1.6; drape.rotation.x = 0.6 * k; drape.scale.y = 1 - 0.5 * k; };
    g.userData.update(0); return g;
  },

  // A red inauguration ribbon between two brass posts (pivot on the ground between them; across X, o.w 1.6 apart, o.h 0.95 high); at o.cutAt it parts
  // in the middle and the two halves drop and swing
  ribbonCut(o) {
    const W = o.w ?? 1.6, Hh = o.h ?? 0.95, g = grp(), L = grp(), R = grp(), half = W / 2;
    for (const sd of [-1, 1]) g.add(at(cyl(0.03, 0.05, Hh, '#D4A848', 8, { pivot: 'bottom' }), sd * half, 0, 0), at(sphere(0.05, '#E2B53C', 1), sd * half, Hh, 0), at(cyl(0.12, 0.14, 0.04, '#B08A38', 10), sd * half, 0.02, 0));
    L.position.set(-half, Hh - 0.03, 0); R.position.set(half, Hh - 0.03, 0);
    L.add(at(box(half, 0.08, 0.01, '#D02A30', { outline: 0.01 }), half / 2, 0, 0)); R.add(at(box(half, 0.08, 0.01, '#D02A30', { outline: 0.01 }), -half / 2, 0, 0));
    g.add(L, R, at(box(0.16, 0.12, 0.03, '#D02A30', { outline: 0.01 }), 0, Hh - 0.03, 0.01));
    const bow = g.children[g.children.length - 1];
    g.userData.update = t => { const u = o.cutAt == null ? -1 : t - o.cutAt, k = u < 0 ? 0 : 1 - Math.exp(-u * 7) * Math.cos(u * 14);
      L.rotation.z = -1.35 * Math.min(1.08, k); R.rotation.z = 1.35 * Math.min(1.08, k); bow.visible = u < 0; };
    g.userData.update(0); return g;
  },

  // Big ceremonial scissors (pivot at the grip; the blades along +Y): gold rings, long silver blades that close at o.cutAt
  scissors(o) {
    const g = grp(), a = grp(), b = grp();
    for (const [p, sd] of [[a, 1], [b, -1]]) { p.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.045, 0.012, 6, 12), mat('#E2B53C')), sd * 0.04, -0.05, 0), at(box(0.03, 0.34, 0.008, '#D9DCDE', { pivot: 'bottom', taper: { x: 0.25, z: 1 }, outline: 0.004 }), 0, 0, 0)); g.add(p); }
    g.userData.update = t => { const u = o.cutAt == null ? -1 : t - o.cutAt, open = u < 0 ? 0.38 : 0.38 * clamp01(1 - u / 0.07); a.rotation.z = open; b.rotation.z = -open; };
    g.userData.update(0); g.userData.grip = [0, -0.05, 0]; return g;
  },

  // Red-and-white seal tape wound round a box head (attach to the head joint, offset [0, 0, 0]): three bands round the head (o.w 0.3 x o.d 0.28, up to
  // o.h 0.47), across the forehead, the chin and on a slant, that appear one after another from o.at (s) every o.every (0.22 s); the face stays open
  sealTape(o) {
    const w = (o.w ?? 0.3) * 1.07, d = (o.d ?? 0.28) * 1.07, h = o.h ?? 0.47, g = grp(), bands = [];
    const band = (y, tilt) => { const b = grp(), tw = 0.07; for (const [x, z, len, ry] of [[0, d / 2, w, 0], [0, -d / 2, w, PI], [w / 2, 0, d, PI / 2], [-w / 2, 0, d, -PI / 2]]) b.add(at(tapeStrip([-len / 2, 0, 0], [len / 2, 0, 0], tw), x, 0, z, 0, ry, 0));
      b.position.y = y; b.rotation.z = tilt; return b; };
    for (const [y, tl] of [[h * 0.84, 0.0], [h * 0.12, 0.0], [h * 0.5, 0.42]]) { const b = band(y, tl); g.add(b); bands.push(b); }
    g.userData.update = t => bands.forEach((b, i) => { const u = t - (o.at ?? 0) - i * (o.every ?? 0.22); b.visible = u >= 0; const s = u < 0 ? 0.01 : Math.min(1, 0.6 + u * 6); b.scale.set(s, 1, s); });
    g.userData.update(0); return g;
  },

  // A blob of red sealing wax with an embossed seal (pivot at its back; front +Z: attach to the face, e.g. head joint offset [0, 0.36, 0.15]): it is
  // not there before o.at, then lands with a squash and settles; o.r (0.075)
  waxSeal(o) {
    const r = o.r ?? 0.075, g = grp(), s = grp(); g.add(s);
    s.add(at(cyl(r, r * 1.08, 0.025, '#B01E22', 12, { emissive: '#300508' }), 0, 0, 0.0125, PI / 2, 0, 0), at(new THREE.Mesh(new THREE.TorusGeometry(r * 0.62, r * 0.09, 5, 14), mat('#7E1218')), 0, 0, 0.027));
    s.add(at(box(r * 0.5, r * 0.12, 0.01, '#7E1218'), 0, 0, 0.03), at(box(r * 0.12, r * 0.5, 0.01, '#7E1218'), 0, 0, 0.03));
    s.add(at(box(0.03, 0.09, 0.004, '#D8C9AA'), r * 0.4, -r * 1.3, 0.004, 0, 0, 0.25), at(box(0.03, 0.09, 0.004, '#D8C9AA'), -r * 0.4, -r * 1.3, 0.004, 0, 0, -0.25));
    g.userData.update = t => { const u = t - (o.at ?? 0); s.visible = u >= 0; if (u < 0) return; const k = 1 + 0.45 * Math.exp(-u * 14) * Math.cos(u * 30); s.scale.set(k, k, 1 / k); };
    g.userData.update(0); return g;
  },

  // An ink ring left by a round stamp (pivot at its back; attach to the forehead like waxSeal): a violet ring with a star in the middle, not there before
  // o.at; o.r (0.07)
  inkRing(o) {
    const r = o.r ?? 0.07, g = grp(), m = canvasPlane(r * 2.2, r * 2.2, (c, W, H) => { c.clearRect(0, 0, W, H); c.strokeStyle = 'rgba(78,46,150,0.92)'; c.lineWidth = W * 0.07;
      c.beginPath(); c.arc(W / 2, H / 2, W * 0.4, 0, 2 * PI); c.stroke(); c.lineWidth = W * 0.03; c.beginPath(); c.arc(W / 2, H / 2, W * 0.3, 0, 2 * PI); c.stroke();
      c.fillStyle = 'rgba(78,46,150,0.92)'; c.beginPath(); for (let i = 0; i < 10; i++) { const a = -PI / 2 + i * PI / 5, rr = i % 2 ? W * 0.07 : W * 0.16; c.lineTo(W / 2 + Math.cos(a) * rr, H / 2 + Math.sin(a) * rr); } c.closePath(); c.fill(); },
      { res: 256, transparent: true });
    m.position.z = 0.004; m.castShadow = false; g.add(m);
    g.userData.update = t => { m.visible = t >= (o.at ?? 0); };
    g.userData.update(0); return g;
  },

  // A big official round stamp (pivot at the grip; the stamp face at -Y): a turned wooden handle and a brass head with a violet ink pad face, o.r (0.11)
  roundStamp(o) {
    const r = o.r ?? 0.11, g = grp();
    g.add(at(sphere(0.06, '#6A4A2E', 1), 0, 0.02, 0), at(cyl(0.025, 0.03, 0.16, '#7A5634', 8), 0, -0.07, 0), at(cyl(r, r, 0.07, '#C9A040', 16, { outline: 0.008 }), 0, -0.19, 0), at(cyl(r * 0.94, r * 0.94, 0.012, '#4E2E96', 16), 0, -0.23, 0));
    g.userData.grip = [0, 0, 0]; return g;
  },

  // A window in a wall that looks out on the street (pivot at its middle; front +Z): a painted view (blue sky, clouds, the roofs and the firemen's red
  // ladder rising across it into a cloud) in a white frame with a cross bar; o.w (1.2) x o.h (1.4)
  skyWindow(o) {
    const W = o.w ?? 1.2, H = o.h ?? 1.4, g = grp();
    const view = canvasPlane(W, H, (c, X, Y) => {
      const gr = c.createLinearGradient(0, 0, 0, Y); gr.addColorStop(0, '#5FA9DE'); gr.addColorStop(1, '#B5DBF0'); c.fillStyle = gr; c.fillRect(0, 0, X, Y);
      c.fillStyle = '#EDE3CF'; c.fillRect(0, Y * 0.78, X, Y * 0.22); c.fillStyle = '#5D6B80'; for (let i = 0; i < 4; i++) c.fillRect(X * (0.04 + i * 0.26), Y * 0.72, X * 0.2, Y * 0.06);
      c.strokeStyle = '#C8322A'; c.lineWidth = X * 0.045; c.beginPath(); c.moveTo(X * 0.12, Y * 1.0); c.lineTo(X * 0.78, Y * 0.12); c.stroke();
      c.strokeStyle = '#E8ECEE'; c.lineWidth = X * 0.012; for (let i = 0; i < 14; i++) { const u = i / 14, x = X * (0.12 + 0.66 * u), y = Y * (1.0 - 0.88 * u); c.beginPath(); c.moveTo(x - X * 0.03, y - Y * 0.012); c.lineTo(x + X * 0.03, y + Y * 0.012); c.stroke(); }
      c.fillStyle = '#FFFFFF'; for (const [x, y, rr] of [[0.72, 0.13, 0.17], [0.88, 0.17, 0.13], [0.6, 0.18, 0.12], [0.8, 0.06, 0.12], [0.2, 0.24, 0.08], [0.3, 0.22, 0.07]]) { c.beginPath(); c.arc(X * x, Y * y, X * rr, 0, 2 * PI); c.fill(); }
    }, { res: 512, emissive: 0.3 });
    view.position.z = 0.01; g.add(view);
    for (const [w_, h_, x, y] of [[W + 0.14, 0.08, 0, H / 2 + 0.03], [W + 0.14, 0.1, 0, -H / 2 - 0.04], [0.08, H + 0.1, -W / 2 - 0.03, 0], [0.08, H + 0.1, W / 2 + 0.03, 0], [0.05, H, 0, 0], [W, 0.05, 0, H * 0.12]]) g.add(at(box(w_, h_, 0.06, '#F4F2EC', { outline: 0.006 }), x, y, 0.03));
    g.add(at(box(W + 0.24, 0.06, 0.18, '#E8E2D6'), 0, -H / 2 - 0.1, 0.08));
    return g;
  },

  // A crater where a building stood (pivot at its middle, on the ground): a dark scorched floor disc o.r (6 m) a few cm above the ground, a lower dark
  // pit, a ring of grey-brown boulders and broken slabs round the rim, a few charred beams sticking out; o.seed
  craterPit(o) {
    const R = o.r ?? 6, g = grp(), r = rng(o.seed || 41);
    const floor = new THREE.Mesh(new THREE.CircleGeometry(R, 28), lam('#4A3F36')); floor.rotation.x = -PI / 2; floor.position.y = 0.05; floor.receiveShadow = true; g.add(floor);
    const pit = new THREE.Mesh(new THREE.CircleGeometry(R * 0.62, 24), lam('#2C2520')); pit.rotation.x = -PI / 2; pit.position.y = 0.06; g.add(pit);
    const ring = new THREE.Mesh(new THREE.RingGeometry(R * 0.6, R * 0.75, 24), lam('#5E5248')); ring.rotation.x = -PI / 2; ring.position.y = 0.065; g.add(ring);
    const geo = new THREE.DodecahedronGeometry(1, 0), cols = ['#8F857A', '#6E655C', '#A39880', '#5A524A'];
    for (let i = 0; i < 46; i++) { const a = (i / 46) * 2 * PI + r() * 0.12, d = R * (0.88 + r() * 0.22), s = 0.2 + r() * 0.55, m = new THREE.Mesh(geo, mat(cols[i % 4]));
      m.scale.set(s * (1 + r()), s * 0.7, s); m.position.set(Math.cos(a) * d, s * 0.35, Math.sin(a) * d); m.rotation.set(r() * 3, r() * 3, r() * 3); m.castShadow = true; g.add(m); }
    for (let i = 0; i < 6; i++) { const a = r() * 2 * PI, d = R * (0.3 + r() * 0.5), L = 1.2 + r() * 1.6; g.add(at(box(0.14, L, 0.14, '#2A2420', { pivot: 'bottom' }), Math.cos(a) * d, 0.02, Math.sin(a) * d, (r() - 0.5) * 1.2, r() * 3, (r() - 0.5) * 1.2)); }
    return g;
  },

  // A cloud of dust that hides the scene and clears (pivot at its middle, on the ground): o.n (22) soft beige puffs over o.r (5 m) up to o.h (5 m) that
  // swell from o.at (s) and then thin out and drift off between o.clear [t0, t1]; translucent, unlit
  dustCloud(o) {
    const n = o.n ?? 22, R = o.r ?? 5, Hh = o.h ?? 5, g = grp(), r = rng(o.seed || 12), puffs = [];
    for (let i = 0; i < n; i++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 1), basic(o.color || '#D8CDB8', { opacity: 0.9 })); const a = r() * 2 * PI, d = R * Math.sqrt(r());
      m.userData.p = [Math.cos(a) * d, Hh * (0.15 + 0.7 * r()), Math.sin(a) * d, R * (0.25 + 0.25 * r()), a]; m.castShadow = false; g.add(m); puffs.push(m); }
    g.userData.update = t => { const u = t - (o.at ?? 0), c = o.clear || [1e9, 1e9], k = clamp01((t - c[0]) / Math.max(0.05, c[1] - c[0]));
      puffs.forEach((m, i) => { const [x, y, z, s, a] = m.userData.p; m.visible = u >= 0 && k < 0.999; if (!m.visible) return; const sw = Math.min(1, 0.4 + u * 2.5);
        m.scale.setScalar(s * sw * (1 + 0.5 * k)); m.position.set(x + Math.cos(a) * k * R * 0.8, y + k * 1.5, z + Math.sin(a) * k * R * 0.8); m.material.opacity = 0.9 * (1 - k * k); }); };
    g.userData.update(0); return g;
  },

  // A winch cable from a helicopter down to a hand (pivot at its bottom end: attach to a hand; it rises along +Y o.len (12 m)), a hook at the bottom
  winchCable(o) {
    const L = o.len ?? 12, g = grp(); g.add(at(cyl(0.012, 0.012, L, '#2A2C30', 5, { pivot: 'bottom' }), 0, 0.06, 0), at(new THREE.Mesh(new THREE.TorusGeometry(0.04, 0.012, 5, 10, PI * 1.4), mat('#8A8E92')), 0, 0.03, 0, 0, 0, PI));
    return g;
  },
};
