// « La flaque » (story 82): this man stepped in a puddle and reported a flood; the navy declared it enemy waters; a submarine dived into it and
// came up a block away with the street on its back; its torpedo went through the bakery and the fire station; the puddle was unhurt; the air
// force promised a surgical strike: three hundred bombs, three hundred craters; then it rained: three hundred puddles; the minister ordered three
// hundred submarines, one per puddle, with the town on their backs; they parked it in the harbour; officially the town moved. Not him. Nor the puddle.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere, addOutline, mat, rng } from './style.js';
import { grp, at, canvasPlane, glowSprite, buildProp } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = x => { const u = clamp01(x), c = 1.70158; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const keyAt = (keys, t, d) => { if (!keys || !keys.length) return d; if (t <= keys[0][0]) return keys[0][1]; for (let i = 1; i < keys.length; i++) { const [t1, v1] = keys[i]; if (t <= t1) { const [t0, v0] = keys[i - 1], u = clamp01((t - t0) / Math.max(1e-6, t1 - t0)), e = u * u * (3 - 2 * u); return v0 + (v1 - v0) * e; } } return keys[keys.length - 1][1]; };
const basic = (c, o = {}) => new THREE.MeshBasicMaterial({ color: c, transparent: o.opacity != null, opacity: o.opacity ?? 1, depthWrite: o.opacity == null, side: o.side || THREE.FrontSide });
const noShadow = m => { m.traverse(c => { c.castShadow = false; }); return m; };

// the mirror surface of a puddle, drawn on a canvas: an irregular blob (seeded) of bright sky blue, a paler band where the sky is lighter, a white
// cloud and two glint streaks; transparent outside the blob. w × d metres, flat on the ground (pivot at its middle).
function puddleSkin(w, d, seed = 3, tint = null) {
  const r = rng(seed), pts = []; const N = 14;
  for (let i = 0; i < N; i++) { const a = i / N * TAU, k = 0.78 + 0.22 * r(); pts.push([0.5 + 0.47 * k * Math.cos(a), 0.5 + 0.47 * k * Math.sin(a)]); }
  const m = canvasPlane(w, d, (c, W, H) => {
    c.clearRect(0, 0, W, H); c.beginPath();
    for (let i = 0; i <= N; i++) { const p = pts[i % N], q = pts[(i + 1) % N], mx = (p[0] + q[0]) / 2 * W, my = (p[1] + q[1]) / 2 * H; if (i === 0) c.moveTo(mx, my); else c.quadraticCurveTo(p[0] * W, p[1] * H, mx, my); }
    c.closePath(); c.save(); c.clip();
    const gr = c.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, tint ? tint[0] : '#4FA8E8'); gr.addColorStop(0.55, tint ? tint[1] : '#8FCFF5'); gr.addColorStop(1, tint ? tint[0] : '#5AB2EC');
    c.fillStyle = gr; c.fillRect(0, 0, W, H);
    c.fillStyle = 'rgba(255,255,255,0.92)'; for (const [x, y, rr] of [[0.38, 0.42, 0.11], [0.5, 0.38, 0.13], [0.6, 0.44, 0.1], [0.47, 0.48, 0.12]]) { c.beginPath(); c.arc(x * W, y * H, rr * W, 0, TAU); c.fill(); }
    c.strokeStyle = 'rgba(255,255,255,0.85)'; c.lineCap = 'round'; c.lineWidth = W * 0.03; c.beginPath(); c.moveTo(W * 0.2, H * 0.7); c.lineTo(W * 0.42, H * 0.62); c.stroke();
    c.lineWidth = W * 0.018; c.beginPath(); c.moveTo(W * 0.62, H * 0.74); c.lineTo(W * 0.78, H * 0.68); c.stroke();
    c.restore(); c.lineWidth = W * 0.022; c.strokeStyle = 'rgba(40,70,100,0.55)'; c.beginPath();
    for (let i = 0; i <= N; i++) { const p = pts[i % N], q = pts[(i + 1) % N], mx = (p[0] + q[0]) / 2 * W, my = (p[1] + q[1]) / 2 * H; if (i === 0) c.moveTo(mx, my); else c.quadraticCurveTo(p[0] * W, p[1] * H, mx, my); }
    c.closePath(); c.stroke();
  }, { res: 256, transparent: true, emissive: 0.55 });
  m.rotation.x = -PI / 2; m.receiveShadow = false; m.castShadow = false; return m;
}

// a brown dish seen from above: a crater o.r wide (dark centre, a lighter rim of rocks), drawn on a canvas
function craterSkin(R, seed = 5) {
  const r = rng(seed); const m = canvasPlane(R * 2.6, R * 2.6, (c, W, H) => {
    c.clearRect(0, 0, W, H); const cx = W / 2, cy = H / 2, rr = W / 2.6;
    c.fillStyle = 'rgba(176,150,118,0.95)'; c.beginPath(); for (let i = 0; i <= 24; i++) { const a = i / 24 * TAU, k = 1.18 + 0.12 * r(); c.lineTo(cx + Math.cos(a) * rr * k, cy + Math.sin(a) * rr * k); } c.closePath(); c.fill();
    const gr = c.createRadialGradient(cx - rr * 0.15, cy - rr * 0.15, rr * 0.1, cx, cy, rr); gr.addColorStop(0, '#4A3A2C'); gr.addColorStop(0.7, '#6E5843'); gr.addColorStop(1, '#8F7558');
    c.fillStyle = gr; c.beginPath(); c.arc(cx, cy, rr, 0, TAU); c.fill();
    c.fillStyle = '#C9B89C'; for (let i = 0; i < 22; i++) { const a = r() * TAU, d = rr * (1.02 + 0.18 * r()), s = W * (0.012 + 0.018 * r()); c.beginPath(); c.arc(cx + Math.cos(a) * d, cy + Math.sin(a) * d, s, 0, TAU); c.fill(); }
    c.strokeStyle = 'rgba(40,28,18,0.6)'; c.lineWidth = W * 0.015; c.beginPath(); c.arc(cx, cy, rr, 0, TAU); c.stroke();
  }, { res: 256, transparent: true });
  m.rotation.x = -PI / 2; m.castShadow = false; m.receiveShadow = true; return m;
}

// a facade texture for blocks seen from far: cream wall with window rows
const facadeTex = (() => { let t = null; return () => { if (t) return t; const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d');
  g.fillStyle = '#FFFFFF'; g.fillRect(0, 0, 256, 256); g.fillStyle = '#6E86A0'; for (let f = 0; f < 5; f++) for (let k = 0; k < 6; k++) g.fillRect(k * 256 / 6 + 8, f * 256 / 5 + 12, 256 / 6 - 16, 256 / 5 - 26);
  t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; return t; }; })();

// (round 1) a clock tower (pivot at its foot): a cream stone shaft w × w × h, a cornice, a white clock face with black hands on each side, a
// zinc pyramid roof; userData.ropeY: the height where a rope can loop round the shaft (under the clocks)
function clockTower(w = 1.6, h = 7) {
  const g = grp(at(box(w, h, w, '#EFE3C8', { pivot: 'bottom', outline: 0.012 }), 0, 0, 0), at(box(w * 1.18, 0.25, w * 1.18, '#D8C9A8', { outline: 0.01 }), 0, h, 0));
  const face = canvasPlane(w * 0.78, w * 0.78, (c, W, H) => { c.clearRect(0, 0, W, H); c.fillStyle = '#FFFFFF'; c.beginPath(); c.arc(W / 2, H / 2, W * 0.47, 0, TAU); c.fill(); c.strokeStyle = '#1E2126'; c.lineWidth = W * 0.05; c.stroke();
    c.lineWidth = W * 0.035; for (let i = 0; i < 12; i++) { const a = i / 12 * TAU; c.beginPath(); c.moveTo(W / 2 + Math.cos(a) * W * 0.36, H / 2 + Math.sin(a) * W * 0.36); c.lineTo(W / 2 + Math.cos(a) * W * 0.42, H / 2 + Math.sin(a) * W * 0.42); c.stroke(); }
    c.lineWidth = W * 0.05; c.lineCap = 'round'; c.beginPath(); c.moveTo(W / 2, H / 2); c.lineTo(W / 2, H * 0.2); c.moveTo(W / 2, H / 2); c.lineTo(W * 0.7, H * 0.56); c.stroke(); }, { res: 256, transparent: true });
  for (let k = 0; k < 4; k++) { const f = face.clone(); const a = k * PI / 2; f.position.set(Math.sin(a) * (w / 2 + 0.01), h - w * 0.62, Math.cos(a) * (w / 2 + 0.01)); f.rotation.y = a; g.add(f); }
  const roof = new THREE.Mesh(new THREE.ConeGeometry(w * 0.85, w * 1.1, 4).rotateY(PI / 4), mat('#5F6E7E')); roof.position.y = h + 0.25 + w * 0.55; roof.castShadow = true; addOutline(roof, 0.02); g.add(roof);
  g.userData.ropeY = h - w * 1.35; return g;
}

// (round 1) a fat golden baguette that reads as bread from far: a long capsule, darker gold ends, five pale diagonal score marks on top (length
// o.len 0.7 m, girth o.r 0.06); pivot at its middle
function bread(len = 0.7, rad = 0.06) {
  const g = grp(), body = new THREE.Mesh(new THREE.CapsuleGeometry(rad, len - 2 * rad, 4, 10), mat('#D99A45')); body.rotation.z = PI / 2; body.castShadow = true; addOutline(body, 0.05); g.add(body);
  for (let i = 0; i < 5; i++) { const sc = box(rad * 1.1, rad * 0.18, rad * 0.55, '#F3D08A'); sc.position.set(-len * 0.32 + i * len * 0.16, rad * 0.92, 0); sc.rotation.y = 0.7; g.add(sc); }
  for (const sd of [-1, 1]) { const e = sphere(rad * 0.82, '#B9762E', 0); e.position.set(sd * (len / 2 - rad * 0.9), 0, 0); g.add(e); }
  return g;
}

// (round 3) a town plan that reads as streets: paper, blocks of buildings with darker outlines, white streets with grey kerb lines between them, a
// wide boulevard across on the diagonal, a little park and a blue river along one side (nx × nz blocks)
function streetPlan(c, Wc, Hc, nx, nz) {
  c.fillStyle = '#ECEAE0'; c.fillRect(0, 0, Wc, Hc);
  c.fillStyle = '#8FC3E6'; c.beginPath(); c.moveTo(0, Hc * 0.86); c.bezierCurveTo(Wc * 0.3, Hc * 0.8, Wc * 0.6, Hc * 0.97, Wc, Hc * 0.9); c.lineTo(Wc, Hc); c.lineTo(0, Hc); c.closePath(); c.fill();
  const bw = Wc / nx, bh = Hc * 0.84 / nz, gap = Math.min(bw, bh) * 0.2;
  for (let i = 0; i < nx; i++) for (let k = 0; k < nz; k++) { const x = i * bw + gap / 2, y = k * bh + gap / 2, w = bw - gap, h = bh - gap;
    c.fillStyle = (i * 7 + k * 3) % 11 === 4 ? '#A9D3A0' : '#D9CFB4'; c.fillRect(x, y, w, h); c.strokeStyle = '#9A8F78'; c.lineWidth = Math.max(1, Wc * 0.004); c.strokeRect(x, y, w, h);
    c.strokeStyle = 'rgba(120,108,88,0.45)'; c.beginPath(); c.moveTo(x + w / 2, y); c.lineTo(x + w / 2, y + h); c.moveTo(x, y + h / 2); c.lineTo(x + w, y + h / 2); c.stroke(); }
  c.strokeStyle = '#FFFFFF'; c.lineWidth = gap * 1.6; c.beginPath(); c.moveTo(0, Hc * 0.12); c.lineTo(Wc, Hc * 0.7); c.stroke();
  c.strokeStyle = '#B9AF98'; c.lineWidth = Math.max(1, Wc * 0.004); c.beginPath(); c.moveTo(0, Hc * 0.12 - gap * 0.8); c.lineTo(Wc, Hc * 0.7 - gap * 0.8); c.moveTo(0, Hc * 0.12 + gap * 0.8); c.lineTo(Wc, Hc * 0.7 + gap * 0.8); c.stroke();
}

export const FLAQUE_PROPS = {
  // (round 1) A starburst that is not there before o.at (explosionBurst runs on the shot clock and is fully out from its first frame): built from
  // explosionBurst (o.size, o.seed), run on t - o.at, gone after o.life (s, default: stays)
  timedBurst(o) {
    const g = grp(), b = buildProp('explosionBurst', { size: o.size ?? 1.1, seed: o.seed }); g.add(b);
    g.userData.update = t => { const u = t - (o.at ?? 0); b.visible = u >= 0 && u < (o.life ?? 99); if (b.visible) b.userData.update?.(u); };
    g.userData.update(0); return g;
  },

  // (round 1) A fat golden baguette lying about (pivot at its middle, on the ground): o.len (0.7), o.r (0.06)
  fatBaguette(o) { const g = grp(), b = bread(o.len ?? 0.7, o.r ?? 0.06); b.position.y = o.r ?? 0.06; g.add(b); return g; },

  // The hero puddle (pivot at its middle, on the ground): a doormat-sized mirror of the sky, o.w (0.95) × o.d (0.62), an irregular outline, a white
  // cloud and glints in it. o.ripple [t, ...]: a thin ring spreads out and fades (0.7 s each); o.splash [t, ...]: a crown of drops thrown up and
  // falling back (a foot came down in it), o.splashDir [x, z] tips the crown that way; o.shine (m): a twinkling star over it (seen from the air);
  // o.grow [t0, t1]: it spreads from nothing (rain filling a crater); o.seed: another outline
  puddle(o) {
    const W = o.w ?? 0.95, D = o.d ?? 0.62, g = grp(), skin = puddleSkin(W, D, o.seed ?? 3, o.tint); skin.position.y = 0.012; g.add(skin);
    const ring = new THREE.Mesh(new THREE.RingGeometry(0.9, 1.0, 40).rotateX(-PI / 2), basic('#FFFFFF', { opacity: 0.8 })); ring.position.y = 0.016; ring.visible = false; g.add(ring);
    const ring2 = ring.clone(); ring2.material = ring.material.clone(); g.add(ring2);
    const drops = []; for (let i = 0; i < 16; i++) { const d = new THREE.Mesh(new THREE.SphereGeometry(0.022 + 0.014 * hsh(i), 6, 4), basic('#BFE6FF')); d.visible = false; g.add(d); drops.push(d); }
    // (round 3) the splash is a crown: a thin see-through wall of water that flares out from the foot, its rim pulled up into eight points, a fat
    // drop on each point (the inverted cone with balls read as a plastic cup)
    const crownGeo = new THREE.CylinderGeometry(0.2, 0.12, 0.2, 24, 1, true), cp = crownGeo.attributes.position;
    for (let i = 0; i < cp.count; i++) { if (cp.getY(i) > 0) { const a = Math.atan2(cp.getZ(i), cp.getX(i)); cp.setY(i, 0.1 + 0.07 * Math.pow(Math.max(0, Math.cos(a * 4)), 3) - 0.03); } }
    crownGeo.translate(0, 0.1, 0); crownGeo.computeVertexNormals();
    const sheet = new THREE.Mesh(crownGeo, basic('#CFEBFF', { opacity: 0.55, side: THREE.DoubleSide })); sheet.visible = false; g.add(sheet);
    const tips = []; for (let i = 0; i < 8; i++) { const d = new THREE.Mesh(new THREE.SphereGeometry(0.024, 7, 5), basic('#E8F7FF')); d.visible = false; g.add(d); tips.push(d); }
    let star = null; if (o.shine) { star = glowSprite('#FFFFFF', o.shine, 0.95); star.position.y = 0.2; g.add(star); }
    g.userData.update = t => {
      if (o.grow) { const s = smooth((t - o.grow[0]) / Math.max(0.01, o.grow[1] - o.grow[0])); skin.visible = s > 0.01; skin.scale.set(Math.max(0.01, s), Math.max(0.01, s), 1); }
      const rp = (o.ripple || []).filter(a => t >= a && t < a + 0.7);
      [ring, ring2].forEach((rg, j) => { const a = rp[j]; rg.visible = a != null; if (a == null) return; const u = (t - a) / 0.7; rg.scale.set(0.12 + u * Math.min(W, D) * 0.45, 1, 0.12 + u * Math.min(W, D) * 0.45); rg.material.opacity = 0.85 * (1 - u); });
      const sp = (o.splash || []).filter(a => t >= a && t < a + 0.75).pop(); const dir = o.splashDir || [0, 0];
      drops.forEach((d, i) => { d.visible = sp != null; if (sp == null) return; const u = t - sp, a = i / drops.length * TAU, v = 1.2 + 1.1 * hsh(i + 3), vy = 2.1 + 1.6 * hsh(i + 7);
        const y = vy * u - 4.9 * u * u; if (y < -0.01) { d.visible = false; return; } d.position.set(Math.cos(a) * v * u * 0.45 + dir[0] * u, 0.02 + y, Math.sin(a) * v * u * 0.45 + dir[1] * u); });
      sheet.visible = sp != null && t - sp < 0.32; if (sheet.visible) { const u = (t - sp) / 0.32, hh = Math.sin(Math.min(1, u * 1.6) * PI * 0.5) * (1 - u * u); sheet.scale.set(0.7 + 1.1 * u, Math.max(0.02, 1.5 * hh), 0.7 + 1.1 * u); sheet.position.set(dir[0] * 0.06, 0.0, dir[1] * 0.06); sheet.material.opacity = 0.6 * (1 - u * 0.7); }
      tips.forEach((d, i) => { d.visible = sp != null && t - sp < 0.42; if (!d.visible) return; const u = t - sp, a = i / 8 * TAU + PI / 8 * 0, rr = 0.14 + 0.55 * u, y = 0.06 + 1.5 * u - 4.9 * u * u; if (y < 0.01) { d.visible = false; return; } d.position.set(Math.cos(a) * rr + dir[0] * 0.12 * u, y, Math.sin(a) * rr + dir[1] * 0.12 * u); d.scale.set(1, 1.4, 1); });
      if (star) { const k = 0.75 + 0.25 * Math.sin(t * 9); star.scale.setScalar(o.shine * k); }
    };
    g.userData.update(0); return g;
  },

  // A full-size submarine that dives nose first into a puddle and is gone (pivot at the puddle's middle). o.L (6 m long); o.tilt (rad, 1.15: how
  // steeply the nose points down); o.touch (s): the bow meets the surface; o.gone (s): the stern is under; before o.touch it falls along its axis at
  // the same speed (visible from o.at); as it goes through, its girth squeezes to o.r (0.36 m: the puddle's half width) and it stretches (a cartoon
  // squeeze through a hole). The ground hides what is under it. o.ry: its heading (rad).
  divingSub(o) {
    const L = o.L ?? 6, Hh = L * 0.26, g = grp(), A = grp(), S = grp(), sub = buildProp('submarine', { len: L, color: o.color || '#5E6B7A', peri: o.peri });   // (round 3) o.peri: the periscope up ([[0, 1]])
    sub.position.set(0, -Hh / 2, -L / 2); S.add(sub); A.add(S); g.add(A);
    const th = o.tilt ?? 1.15, dir = new THREE.Vector3(0, -Math.sin(th), Math.cos(th)); A.rotation.set(th, 0, 0); g.rotation.y = o.ry ?? 0;
    const t1 = o.touch ?? 0.5, t2 = o.gone ?? 1.1, v = L * 1.15 / Math.max(0.05, t2 - t1), squeeze = Math.min(1, 2 * (o.r ?? 0.36) / Hh);
    // (round 2) o.collar: a fat ring of hull bunched up at the rim while it is sucked through (a neck at the surface: the hull is fat above it and
    // thin below), flattened, shrinking away as the stern goes in
    // (round 3) o.collarWater: the collar is water bulging up round the hull (pale blue, see-through, thinner), not a grey tyre that hid the rim
    const CR = o.r ?? 0.36, CW = !!o.collarWater; let col = null; if (o.collar) { col = new THREE.Mesh(new THREE.TorusGeometry(CR * (CW ? 1.0 : 1.05), CR * (CW ? 0.26 : 0.42), 10, 24).rotateX(PI / 2), CW ? basic('#A8DCFA', { opacity: 0.72 }) : mat(o.collarColor || '#7C8996')); col.position.y = 0.06; col.visible = false; col.castShadow = !CW; if (!CW) addOutline(col, 0.02); g.add(col); }
    // (round 3) o.approach [t0, d0]: from t0 the bow is d0 metres up its axis from the puddle and it comes down slowly, speeding up to the dive speed at
    // o.touch (it fell at the full dive speed all the way, so the whole hull was never in the picture)
    const ap = o.approach, apS = (t) => { const [a0, d0] = ap, T = Math.max(0.05, t1 - a0), u = clamp01((t - a0) / T);
      const h00 = 2 * u ** 3 - 3 * u ** 2 + 1, h11 = u ** 3 - u ** 2; return -d0 * h00 + v * T * h11; };
    g.userData.update = t => {
      sub.userData.update?.(t);
      if (col) { const u = (t - t1) / Math.max(0.05, t2 - t1); col.visible = u > 0.02 && u < 0.98; if (col.visible) { const k = Math.sin(clamp01(u) * PI); col.scale.set(0.8 + 0.5 * k, 0.5 + 0.7 * k, 0.8 + 0.5 * k); col.position.y = 0.06 + 0.1 * k; } }
      const on = t >= (o.at ?? 0) && t <= t2 + 0.05; A.visible = on; if (!on) return;
      const s = (ap && t < t1) ? apS(t) / v : t - t1; A.position.copy(dir).multiplyScalar(v * s);
      // (round 1) the hull stays fat down to the surface and is sucked thin as it goes in (it was already thin when it reached the puddle)
      const w = smooth((t - (t1 - (o.lead ?? 0.03))) / (o.suck ?? 0.22)), gs = 1 + (squeeze - 1) * w; S.scale.set(gs, gs, 1 + 0.5 * w);
    };
    g.userData.update(0); return g;
  },

  // A submarine surfacing through the road a block away with a slab of street on its back (pivot on the road over its middle, the bow toward +Z).
  // o.L (7 m); o.at (s) it starts rising, o.dur (0.55 s); it rises from o.y0 (-3.4: the deck under the road) to o.y1 (-0.55: the slab's top 1.1 m up),
  // overshoots and bobs; the slab (o.slab [w 7, d 9]: asphalt, a dashed white line, a kerb strip) rides on its deck and tips by o.tip (0.32 rad, from
  // o.tipAt); two parked cars on it (o.cars colours) slide down the tipped slab and fall off its low edge from o.slideAt; a street lamp on its far edge
  // leans and topples; chunks of asphalt fly up when it breaks through
  surfacingSub(o) {
    const L = o.L ?? 7, Hh = L * 0.26, g = grp(), R = grp(); g.add(R);
    // (round 3) o.subRy: the hull's heading under the slab (PI / 2: lying along X, side-on to a camera down the street, so its conning tower and
    // periscope read; bow-on it read as a grey mound); o.peri: the periscope up
    const sub = buildProp('submarine', { len: L, color: o.color || '#5E6B7A', peri: o.peri }); sub.rotation.y = o.subRy ?? 0; R.add(sub);
    // (round 3) the slab reads as a piece of road: dark asphalt sides with a pale cut line of gravel under the black top, a white lane line along it
    // and a grey stone kerb (the cream kerb strip and the even grey made it read as a wooden plank)
    const [sw, sd] = o.slab || [7, 9], slab = grp(); const top = box(sw, 0.35, sd, '#3F4044', { outline: 0.02 }); top.position.y = -0.175; slab.add(top);
    slab.add(at(box(sw + 0.01, 0.08, sd + 0.01, '#9A948A'), 0, -0.3, 0), at(box(sw - 0.02, 0.02, sd - 0.02, '#55565B'), 0, 0.006, 0));
    slab.add(at(box(0.18, 0.014, 1.8, '#F4F1E8'), 0, 0.02, -2.2), at(box(0.18, 0.014, 1.8, '#F4F1E8'), 0, 0.02, 1.8), at(box(sw - 0.4, 0.014, 0.16, '#F4F1E8'), 0, 0.02, sd / 2 - 0.45), at(box(1.3, 0.06, sd, '#B9B4AA', { outline: 0.008 }), sw / 2 - 0.65, 0.03, 0));
    const deckY = Hh * 0.9 + Hh * 0.62 + 0.18; slab.position.y = deckY; R.add(slab);
    const cx0 = o.carX0 || [-sw / 2 + 1.2, -sw / 2 + 2.9];
    const cars = (o.cars || ['#C9452E', '#3D7FC4']).map((c, i) => { const car = buildProp('car', { color: c }); car.rotation.y = PI / 2; car.position.set(cx0[i], 0, -1.5 + i * 3.0); slab.add(car); return car; });
    const lamp = buildProp('streetLamp', {}); lamp.position.set(sw / 2 - 0.4, 0, 0.5); slab.add(lamp);
    const chunks = []; for (let i = 0; i < 18; i++) { const b = box(0.3 + 0.3 * hsh(i), 0.12, 0.25 + 0.2 * hsh(i + 1), i % 3 ? '#5E5E62' : '#7A7A7E', { outline: 0.008 }); b.visible = false; g.add(b); chunks.push(b); }
    const pit = new THREE.Mesh(new THREE.PlaneGeometry(sw + 0.6, sd + 0.6).rotateX(-PI / 2), basic('#15171A')); pit.position.y = 0.02; pit.visible = false; g.add(pit);
    const t0 = o.at ?? 0.2, du = o.dur ?? 0.55, y0 = o.y0 ?? -3.4, y1 = o.y1 ?? (-deckY + 1.1), ts = o.tipAt ?? (t0 + du + 0.1), tl = o.slideAt ?? (ts + 0.15);
    g.userData.update = t => {
      sub.userData.update?.(t);
      const u = (t - t0) / du; R.position.y = u <= 0 ? y0 : u < 1 ? y0 + (y1 - y0) * outBack(u) : y1 + 0.06 * Math.sin((t - t0 - du) * 7) * Math.exp(-(t - t0 - du) * 2.5);
      const tip = (o.tip ?? 0.32) * smooth((t - ts) / 0.35); slab.rotation.z = tip;
      // (round 1) each car slides down the tipped slab, teeters 0.12 s on the low lip (front wheels over the edge, nose dipping), then drops off,
      // turning, lands on the road (worked out in the slab's frame: the road plane is tilted there) and bounces once
      const sT = Math.sin(Math.max(0.05, tip)), cT = Math.cos(tip), lip = -sw / 2 + 0.35, acc = 9.8 * sT * 0.9 * (o.accK ?? 1), hang = o.hang ?? 0.12;   // (round 2) o.accK: a slicker slide
      cars.forEach((car, i) => { const s = Math.max(0, t - tl - i * 0.14), x0 = cx0[i], dl = Math.max(0, x0 - lip), sl = Math.sqrt(2 * dl / acc), vl = acc * sl;
        if (s <= sl) { car.position.set(x0 - 0.5 * acc * s * s, 0, car.position.z); car.rotation.set(0, PI / 2, 0); return; }
        const h = s - sl; if (h <= hang) { const w = Math.sin(h / hang * PI * 1.5) * 0.12 + 0.25 * (h / hang); car.position.set(lip - 0.15 * (h / hang), 0, car.position.z); car.rotation.set(0, PI / 2, w); return; }
        const q = h - hang, vx = Math.max(1.6, vl * 0.6), xq = lip - 0.15 - vx * q, floor = (0.05 - R.position.y - slab.position.y - xq * sT) / cT;
        let y = -4.9 * q * q, rz = Math.min(1.0, 0.25 + 2.2 * q); const qf = Math.sqrt(Math.max(0, -floor) / 4.9);
        if (y <= floor) { const b = q - qf, rf = Math.min(1.0, 0.25 + 2.2 * qf); y = floor + Math.max(0, 2.2 * b - 4.9 * b * b); rz = rf + (-tip - rf) * smooth(b / 0.12) + 0.25 * Math.sin(b * 16) * Math.exp(-b * 6); }
        car.position.set(xq, y, car.position.z); car.rotation.set(0, PI / 2, rz); });
      lamp.rotation.z = -1.5 * smooth((t - tl + 0.1) / 0.4) + 0.12 * Math.sin(Math.max(0, t - tl - 0.3) * 14) * Math.exp(-Math.max(0, t - tl - 0.3) * 4) * (t > tl + 0.3 ? 1 : 0);
      pit.visible = t >= t0 + du * 0.3; if (pit.visible) pit.scale.setScalar(Math.min(1, 0.4 + (t - t0 - du * 0.3) * 3));
      const cu = t - t0 - du * 0.35; chunks.forEach((b, i) => { b.visible = cu > 0 && cu < 1.6; if (!b.visible) return; const a = hsh(i + 9) * TAU, sp = 2 + 3 * hsh(i + 4), vy = 4 + 4 * hsh(i + 2), y = vy * cu - 4.9 * cu * cu;
        b.position.set(Math.cos(a) * sp * cu * (sw / 5), Math.max(0.05, y), Math.sin(a) * sp * cu * (sd / 5)); b.rotation.set(cu * 6 * hsh(i), cu * 5, cu * 7 * hsh(i + 1)); });
    };
    g.userData.update(0); return g;
  },

  // A bakery's front (pivot at the middle of its foot, front +Z): o.w (8) × o.h (10) of cream stone over a shop front: a wide window full of
  // baguettes and loaves, a door, a red-and-white striped awning, the gilded sign BOULANGERIE; three floors of windows above. o.hitAt (s): a torpedo
  // punches through at o.hit [x, y] (a ragged dark hole, stone chunks), and baguettes spin out of every window toward +Z (o.n per window)
  bakeryFront(o) {
    const W = o.w ?? 8, H = o.h ?? 10, g = grp(), r = rng(o.seed || 7);
    const wall = canvasPlane(W, H, (c, Wc, Hc) => {
      c.fillStyle = o.wall || '#F1E3C8'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = 'rgba(0,0,0,0.06)'; for (let y = 0; y < Hc; y += Hc / 30) c.fillRect(0, y, Wc, 2);
      c.fillStyle = '#7B4A2A'; c.fillRect(0, Hc * 0.72, Wc, Hc * 0.28); c.fillStyle = '#E9C46A'; c.font = `900 ${Hc * 0.05}px Georgia`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.sign || 'BOULANGERIE', Wc / 2, Hc * 0.755);
      c.fillStyle = '#FCEFD8'; c.fillRect(Wc * 0.06, Hc * 0.8, Wc * 0.58, Hc * 0.17); c.fillStyle = '#C98A44'; for (let i = 0; i < 9; i++) { c.save(); c.translate(Wc * (0.1 + i * 0.06), Hc * 0.9); c.rotate(-0.5 + 0.12 * i); c.fillRect(-Wc * 0.012, -Hc * 0.065, Wc * 0.024, Hc * 0.13); c.restore(); }
      c.fillStyle = '#D9A35C'; for (let i = 0; i < 6; i++) { c.beginPath(); c.ellipse(Wc * (0.12 + i * 0.085), Hc * 0.955, Wc * 0.03, Hc * 0.012, 0, 0, TAU); c.fill(); }
      c.fillStyle = '#5A3A22'; c.fillRect(Wc * 0.72, Hc * 0.8, Wc * 0.18, Hc * 0.2); c.fillStyle = '#9FC7DD'; c.fillRect(Wc * 0.75, Hc * 0.82, Wc * 0.12, Hc * 0.1);
      for (let f = 0; f < 3; f++) for (let k = 0; k < 4; k++) { const x = Wc * (0.08 + k * 0.235), y = Hc * (0.06 + f * 0.215); c.fillStyle = '#3E5B78'; c.fillRect(x, y, Wc * 0.13, Hc * 0.15); c.strokeStyle = '#FFFFFF'; c.lineWidth = Wc * 0.008; c.strokeRect(x, y, Wc * 0.13, Hc * 0.15);
        c.fillStyle = '#2B2F33'; c.fillRect(x - Wc * 0.01, y + Hc * 0.15, Wc * 0.15, Hc * 0.012); }
    }, { res: 512 });
    wall.position.set(0, H / 2, 0); g.add(wall, at(box(W, H, 0.3, '#E8D8BA'), 0, H / 2, -0.16));
    const aw = canvasPlane(W * 0.66, 0.9, (c, Wc, Hc) => { for (let i = 0; i < 12; i++) { c.fillStyle = i % 2 ? '#FFFFFF' : '#C8322A'; c.fillRect(i * Wc / 12, 0, Wc / 12 + 1, Hc); } }, { res: 256 });
    aw.position.set(-W * 0.12, H * 0.69, 0.42); aw.rotation.x = -0.75; g.add(aw);
    const hole = canvasPlane(2.2, 2.2, (c, Wc, Hc) => { c.clearRect(0, 0, Wc, Hc); c.fillStyle = '#1B1612'; c.beginPath(); for (let i = 0; i <= 18; i++) { const a = i / 18 * TAU, k = 0.32 + 0.16 * r(); c.lineTo(Wc / 2 + Math.cos(a) * Wc * k, Hc / 2 + Math.sin(a) * Hc * k); } c.closePath(); c.fill(); }, { res: 128, transparent: true });
    const hp = o.hit || [-W * 0.18, H * 0.86]; hole.position.set(hp[0], hp[1], 0.02); hole.visible = false; g.add(hole);
    const wins = []; for (let f = 0; f < 3; f++) for (let k = 0; k < 4; k++) wins.push([-W / 2 + W * (0.08 + k * 0.235 + 0.065), H - H * (0.06 + f * 0.215 + 0.075)]);
    wins.push([hp[0], hp[1]], [hp[0] + 0.8, hp[1] - 0.3], [hp[0] - 0.7, hp[1] + 0.2]);
    const N = o.n ?? 2, bags = []; wins.forEach((w, i) => { for (let j = 0; j < N + (i >= wins.length - 3 ? 3 : 0); j++) { const b = bread(0.75, 0.07); b.visible = false; g.add(b); bags.push({ b, w, i: i * 7 + j }); } });
    const chunks = []; for (let i = 0; i < 14; i++) { const b = box(0.28, 0.16, 0.2, i % 2 ? '#E8D8BA' : '#C9B89A', { outline: 0.008 }); b.visible = false; g.add(b); chunks.push(b); }
    g.userData.update = t => {
      const u = t - (o.hitAt ?? 99); hole.visible = u >= 0; if (u >= 0) hole.scale.setScalar(Math.min(1, 0.3 + u * 8));
      bags.forEach(({ b, w, i }) => { const s = u - 0.03 * (i % 9); b.visible = s > 0; if (!b.visible) return; const vx = (hsh(i) - 0.5) * 3, vy = 1.5 + 3 * hsh(i + 1), vz = 2.5 + 3.5 * hsh(i + 2), y = w[1] + vy * s - 4.9 * s * s;
        b.position.set(w[0] + vx * s, Math.max(0.05, y), 0.3 + vz * s); b.rotation.set(s * 9 * hsh(i + 3), s * 7, s * 11 * (hsh(i + 4) - 0.5)); });
      chunks.forEach((b, i) => { b.visible = u > 0 && u < 2; if (!b.visible) return; const a = hsh(i + 20) * TAU, sp = 2 + 3 * hsh(i + 21), y = hp[1] + (2 + 3 * hsh(i + 22)) * u - 4.9 * u * u;
        b.position.set(hp[0] + Math.cos(a) * sp * u, Math.max(0.08, y), 0.2 + (2.5 + 2 * hsh(i + 23)) * u); b.rotation.set(u * 8, u * 6 * hsh(i), u * 5); });
    };
    g.userData.update(0); return g;
  },

  // A fire station (pivot at the middle of its foot, front +Z): o.w (10) × o.h (7) of red brick, two tall arched garage doors (red, white frames),
  // the word POMPIERS over them, a round window and a little clock tower. o.burstAt (s): the doors blow out toward +Z (panels spinning away), the
  // openings go dark and smoke rolls out
  fireStation(o) {
    const W = o.w ?? 10, H = o.h ?? 7, g = grp();
    const front = canvasPlane(W, H, (c, Wc, Hc) => {
      c.fillStyle = '#B5523A'; c.fillRect(0, 0, Wc, Hc); c.strokeStyle = 'rgba(80,30,20,0.35)'; c.lineWidth = 2; for (let y = 0; y < Hc; y += Hc / 40) { c.beginPath(); c.moveTo(0, y); c.lineTo(Wc, y); c.stroke(); }
      c.fillStyle = '#F4EFE6'; c.fillRect(0, Hc * 0.16, Wc, Hc * 0.1); c.fillStyle = '#B5232A'; c.font = `900 ${Hc * 0.085}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.text || 'POMPIERS', Wc / 2, Hc * 0.212);
      c.fillStyle = '#2B3036'; c.beginPath(); c.arc(Wc / 2, Hc * 0.08, Hc * 0.05, 0, TAU); c.fill(); c.strokeStyle = '#F4EFE6'; c.lineWidth = Wc * 0.008; c.stroke();
      for (const x of [0.1, 0.55]) { c.fillStyle = '#F4EFE6'; c.fillRect(Wc * x - Wc * 0.015, Hc * 0.33, Wc * 0.38, Hc * 0.67); c.fillStyle = '#20232A'; c.fillRect(Wc * x, Hc * 0.36, Wc * 0.35, Hc * 0.64); }
    }, { res: 512 });
    front.position.set(0, H / 2, 0); g.add(front, at(box(W, H, 6, '#A9483A', { outline: 0.02 }), 0, H / 2, -3.02), at(box(W + 0.3, 0.3, 6.3, '#7A2F25'), 0, H + 0.15, -3.0));
    const doors = []; for (const x of [0.1, 0.55]) { const d = grp(); const p = canvasPlane(W * 0.35, H * 0.64, (c, Wc, Hc) => { c.fillStyle = '#C8322A'; c.fillRect(0, 0, Wc, Hc); c.strokeStyle = '#FFFFFF'; c.lineWidth = Wc * 0.03;
      for (let i = 1; i < 4; i++) { c.beginPath(); c.moveTo(0, Hc * i / 4); c.lineTo(Wc, Hc * i / 4); c.stroke(); } c.fillStyle = '#9FC7DD'; for (let k = 0; k < 4; k++) c.fillRect(Wc * (0.06 + k * 0.235), Hc * 0.06, Wc * 0.18, Hc * 0.14); }, { res: 256 });
      d.add(p); d.position.set(-W / 2 + W * (x + 0.175), H * 0.32, 0.04); g.add(d); doors.push(d); }
    const smoke = []; for (let i = 0; i < 12; i++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(0.6, 1), new THREE.MeshLambertMaterial({ color: i % 3 ? '#8A8580' : '#6B6662', transparent: true, opacity: 0.9 })); m.visible = false; g.add(m); smoke.push(m); }
    g.userData.update = t => {
      const u = t - (o.burstAt ?? 99);
      doors.forEach((d, i) => { if (u < 0) { d.position.set(-W / 2 + W * ([0.1, 0.55][i] + 0.175), H * 0.32, 0.04); d.rotation.set(0, 0, 0); return; }
        d.position.set(-W / 2 + W * ([0.1, 0.55][i] + 0.175) + (i ? 2 : -2) * u, H * 0.32 + 4 * u - 4.9 * u * u, 0.04 + 7 * u); d.rotation.set(-3 * u, (i ? 1 : -1) * 2 * u, (i ? -1 : 1) * 1.5 * u); });
      smoke.forEach((m, i) => { const v = (u - 0.04 * i) / 1.6; m.visible = v > 0 && v < 1; if (!m.visible) return; const x = (i % 2 ? 0.3 : -0.2) * W + (hsh(i) - 0.5) * 2;
        m.position.set(x, 1.2 + 3.5 * v, 1 + 3 * v); m.scale.setScalar(0.6 + 1.8 * v); m.material.opacity = 0.9 * (1 - v); });
    };
    g.userData.update(0); return g;
  },

  // The navy's street plan lying on a desk (pivot at its middle, flat, the top edge toward -Z): a sheet o.w (0.9) × o.d (0.62) with pale blocks,
  // white streets and a tiny blue puddle circled in fat red (o.circle [u, v]); o.markAt (s): a red stamp « EAUX ENNEMIES » lands across it, popping
  deskMap(o) {
    const W = o.w ?? 0.9, D = o.d ?? 0.62, g = grp(), [cu, cv] = o.circle || [0.56, 0.5];
    const sheet = canvasPlane(W, D, (c, Wc, Hc) => { streetPlan(c, Wc, Hc, 6, 4); c.fillStyle = '#2E86D9'; c.beginPath(); c.ellipse(Wc * cu, Hc * cv, Wc * 0.012, Hc * 0.012, 0, 0, TAU); c.fill();
      c.strokeStyle = '#D8262C'; c.lineWidth = Wc * 0.012; c.beginPath(); c.ellipse(Wc * cu, Hc * cv, Wc * 0.06, Hc * 0.08, 0.3, 0, TAU); c.stroke(); c.strokeStyle = '#3A3F45'; c.lineWidth = Wc * 0.008; c.strokeRect(2, 2, Wc - 4, Hc - 4); }, { res: 512 });
    sheet.rotation.x = -PI / 2; sheet.position.y = 0.002; sheet.receiveShadow = true; g.add(sheet);
    const mark = canvasPlane(W * 0.62, W * 0.2, (c, Wc, Hc) => { c.clearRect(0, 0, Wc, Hc); c.strokeStyle = '#D8262C'; c.lineWidth = Hc * 0.08; c.strokeRect(Hc * 0.06, Hc * 0.06, Wc - Hc * 0.12, Hc - Hc * 0.12); c.fillStyle = '#D8262C'; let fs = Hc * 0.5; c.font = `900 ${fs}px Arial`; const tw = c.measureText(o.text || 'EAUX ENNEMIES').width; if (tw > Wc * 0.84) { fs *= Wc * 0.84 / tw; c.font = `900 ${fs}px Arial`; } c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.text || 'EAUX ENNEMIES', Wc / 2, Hc * 0.54); }, { res: 512, transparent: true });   // (round 3) the text is fitted inside the frame (it was clipped to « UX ENNEMI »)
    mark.rotation.set(-PI / 2, 0, 0.22); mark.position.set((cu - 0.5) * W - 0.05, 0.006, (cv - 0.5) * D + 0.03); g.add(mark);
    g.userData.update = t => { const u = t - (o.markAt ?? 99); mark.visible = u >= 0; if (u >= 0) mark.scale.setScalar(u < 0.06 ? 1.4 - 2 * u : 1); };
    g.userData.update(0); return g;
  },

  // An easel with the strike map (pivot at the foot of the easel, front +Z): a sheet o.w (1.0) wide with a street plan (pale blocks, white
  // streets) and in its middle a tiny blue dot (the puddle) under a tiny red crosshair; o.tapAt [t, ...]: the crosshair blinks bigger
  strikeEasel(o) {
    const W = o.w ?? 1.0, H = W * 1.25, g = grp(), wood = '#8A5A34';
    for (const [x, z, rz, rx] of [[-0.42, 0.12, 0.12, -0.1], [0.42, 0.12, -0.12, -0.1], [0, -0.3, 0, 0.3]]) g.add(at(cyl(0.02, 0.025, 2.0, wood, 5, { pivot: 'bottom' }), x * W, 0, z, rx, 0, rz));
    g.add(at(box(W * 1.05, 0.04, 0.08, wood), 0, 0.92, 0.2));
    const sheet = canvasPlane(W, H, (c, Wc, Hc) => { streetPlan(c, Wc, Hc, 5, 6); c.strokeStyle = '#3A3F45'; c.lineWidth = Wc * 0.012; c.strokeRect(Wc * 0.01, Hc * 0.01, Wc * 0.98, Hc * 0.98);
      c.fillStyle = '#2E86D9'; c.beginPath(); c.ellipse(Wc * 0.52, Hc * 0.47, Wc * 0.012, Hc * 0.007, 0, 0, TAU); c.fill(); }, { res: 512 });
    sheet.position.set(0, 0.95 + H / 2, 0.24); sheet.rotation.x = -0.12; g.add(sheet);
    const ch = canvasPlane(0.12, 0.12, (c, Wc, Hc) => { c.clearRect(0, 0, Wc, Hc); c.strokeStyle = '#E0302A'; c.lineWidth = Wc * 0.07; c.beginPath(); c.arc(Wc / 2, Hc / 2, Wc * 0.3, 0, TAU); c.stroke();
      c.beginPath(); c.moveTo(Wc / 2, 0); c.lineTo(Wc / 2, Hc * 0.35); c.moveTo(Wc / 2, Hc); c.lineTo(Wc / 2, Hc * 0.65); c.moveTo(0, Hc / 2); c.lineTo(Wc * 0.35, Hc / 2); c.moveTo(Wc, Hc / 2); c.lineTo(Wc * 0.65, Hc / 2); c.stroke(); }, { res: 128, transparent: true, emissive: 0.6 });
    ch.position.set(W * 0.02, 0.95 + H * 0.53, 0.255); ch.rotation.x = -0.12; g.add(ch);
    g.userData.update = t => { let k = 1; for (const a of (o.tapAt || [])) if (t >= a && t < a + 0.3) k = 1 + 1.2 * Math.sin((t - a) / 0.3 * PI); ch.scale.setScalar(k); };
    g.userData.update(0); g.userData.dot = [W * 0.02, 0.95 + H * 0.53, 0.26]; return g;
  },

  // A carpet of bombs (pivot at the release point of the middle of the first row): o.rows (6) × o.cols (5) dark olive bombs with fins, o.gap
  // (2.4 m) apart; row j is let go at o.at + j * o.dt (0.07 s) at o.v (forward speed, m/s, along +Z) and falls under gravity; o.fall (40 m) then gone
  bombCarpet(o) {
    const rows = o.rows ?? 6, cols = o.cols ?? 5, gap = o.gap ?? 2.4, g = grp(), bombs = [], sc = o.s ?? 1;
    for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) { const b = grp(); const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.18 * sc, 0.55 * sc, 4, 10), mat('#3F4A33')); body.rotation.x = PI / 2; b.add(body);
      for (let k = 0; k < 4; k++) { const f = box(0.02 * sc, 0.26 * sc, 0.2 * sc, '#2E3626'); f.position.set(0, 0, -0.42 * sc); f.rotation.z = k * PI / 4 * 2; f.translateY(0.12 * sc); b.add(f); }
      b.add(at(cyl(0.19 * sc, 0.19 * sc, 0.05 * sc, '#C9A43E', 12), 0, 0, 0.18 * sc, PI / 2, 0, 0)); b.visible = false; g.add(b); bombs.push({ b, i, j }); }
    g.userData.update = t => { bombs.forEach(({ b, i, j }) => { const s = t - (o.at ?? 0) - j * (o.dt ?? 0.07); b.visible = s >= 0 && 4.9 * s * s < (o.fall ?? 40); if (!b.visible) return;
      b.position.set((i - (cols - 1) / 2) * gap, -4.9 * s * s, j * gap * 0.0 + (o.v ?? 30) * s * 0.35 - j * gap); b.rotation.x = Math.min(1.3, 0.25 + s * 1.6); }); };
    g.userData.update(-1); return g;
  },

  // The neighbourhood seen from the air after the strike (pivot at its middle, on the ground): o.w (34) × o.d (60) of dusty ground with a few
  // broken block stubs, a grid of craters o.nx (5) × o.nz (9), o.gapX / o.gapZ apart (r o.r 1.7 m); o.home [x, z]: his original puddle there,
  // always water and twinkling; o.fill [t0, t1]: the craters fill with water one after another along X as a cloud passes (each puddle grows in 0.35 s)
  craterField(o) {
    const W = o.w ?? 34, D = o.d ?? 60, g = grp(), r = rng(o.seed || 9), R = o.r ?? 1.7;
    const gnd = new THREE.Mesh(new THREE.PlaneGeometry(W * 3, D * 3).rotateX(-PI / 2), mat(o.ground || '#C9BFA9')); gnd.position.y = -0.02; gnd.receiveShadow = true; g.add(gnd);
    const road = (x, z, w, d) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, d).rotateX(-PI / 2), mat('#8E8B86')); m.position.set(x, -0.01, z); m.receiveShadow = true; g.add(m); };
    const RW = o.roadW ?? 6; road(0, 0, RW, D * 3); road(0, -D * 0.25, W * 3, RW); road(0, D * 0.25, W * 3, RW);
    const stubs = []; for (let i = 0; i < 26; i++) { const x = (r() - 0.5) * W * 2.6, z = (r() - 0.5) * D * 2.4; if (Math.abs(x) < W / 2 + 2 && Math.abs(z) < D / 2 + 2) continue; stubs.push([x, z, 2 + r() * 10, 8 + r() * 6]); }
    const tex = facadeTex(); stubs.forEach(([x, z, h, s]) => { const m = new THREE.Mesh(new THREE.BoxGeometry(s, h, s), new THREE.MeshLambertMaterial({ color: ['#EFE6D2', '#F2DCCB', '#E8E1EE'][Math.floor(r() * 3)], map: tex })); m.position.set(x, h / 2, z); m.castShadow = m.receiveShadow = true; g.add(m); });
    const nx = o.nx ?? 5, nz = o.nz ?? 9, gx = o.gapX ?? (W / nx), gz = o.gapZ ?? (D / nz), cr = [];
    for (let i = 0; i < nx; i++) for (let j = 0; j < nz; j++) { const x = (i - (nx - 1) / 2) * gx, z = (j - (nz - 1) / 2) * gz; if (o.home && Math.hypot(x - o.home[0], z - o.home[1]) < gx * 0.6) continue;
      const c = craterSkin(R, 11 + i * 13 + j); c.position.set(x, 0.0 + 0.001 * j, z); g.add(c);
      const p = FLAQUE_PROPS.puddle({ w: R * 1.75, d: R * 1.75, seed: 21 + i * 7 + j }); p.position.set(x, 0.02, z); g.add(p);
      if (o.fill && o.ripples) { const tf0 = o.fill[0] + (o.fill[1] - o.fill[0]) * ((i - 0) / Math.max(1, nx - 1)); p.userData.rip = [0.38, 0.95, 1.5, 2.05].map(d => tf0 + d + 0.12 * hsh(i * 3 + j)); }
      // (round 1) o.pop [t0, t1]: the craters are not there before the bombs land: they pop in row after row (along Z), each with a dust puff
      const dust = []; if (o.pop) for (let k = 0; k < 4; k++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(R * 0.55, 1), new THREE.MeshLambertMaterial({ color: k % 2 ? '#D9CDB4' : '#C4B79C', transparent: true, opacity: 0.9 })); m.castShadow = false; m.visible = false; g.add(m); dust.push(m); }
      cr.push({ p, c, x, z, dust, i, j }); }
    // (round 1) o.blocks: roofed blocks of houses between the craters (the same town as the street shots, seen from the air): cream walls with
    // windows, zinc-grey roofs, o.blockH [min, max] metres
    // (round 2) o.paris: the blocks are the street's own Haussmann buildings (cream stone, the grey-blue mansard roofs with dormers and chimney pots)
    // scaled down to o.blockS, with a round tree on every other corner (from the air the cream boxes with blue pyramids read as another town)
    if (o.blocks && o.paris) { const bs = o.blockS ?? Math.min(gx, gz) * 0.5, sc = bs / 12, WC = ['#EFE6D2', '#F2DCCB', '#F3E9C9', '#E8E1EE', '#F0D9D9'], AW = ['#B5302A', '#2F7F5C', '#2F5E8C', '#C9822E']; let k = 0;
      for (let i = 0; i < nx - 1; i++) for (let j = 0; j < nz - 1; j++) { const x = (i - (nx - 2) / 2) * gx, z = (j - (nz - 2) / 2) * gz; if (o.home && Math.hypot(x - o.home[0], z - o.home[1]) < gx * 0.75) continue; if (Math.abs(x) < RW / 2 + 0.2) continue;
        if (o.clear && Math.hypot(x - o.clear[0], z - o.clear[1]) < o.clear[2]) continue;   // (round 2) o.clear [x, z, r]: no block there (the Eiffel tower stands there)
        const b = buildProp('haussmann', { w: 12, d: 12, h: 15 + 5 * r(), floors: 6, cols: 5, color: WC[k % 5], awning: AW[k % 4], seed: k }); b.scale.setScalar(sc); b.position.set(x, 0, z + bs / 2); b.rotation.y = (k % 2) * PI; if (b.rotation.y) b.position.z = z - bs / 2; g.add(b);
        if (o.trees && k % 2 === 0) { const tr = buildProp('tree', { seed: k + 7 }); tr.scale.setScalar(o.treeS ?? 0.45); tr.position.set(x + (x > 0 ? -1 : 1) * (bs / 2 + 0.7), 0, z + gz * 0.42); g.add(tr); }
        k++; } }
    if (o.blocks && !o.paris) { const pts = []; for (let i = 0; i < nx - 1; i++) for (let j = 0; j < nz - 1; j++) { const x = (i - (nx - 2) / 2) * gx, z = (j - (nz - 2) / 2) * gz; if (o.home && Math.hypot(x - o.home[0], z - o.home[1]) < gx * 0.75) continue; if (Math.abs(x) < RW / 2 + 0.2) continue; pts.push([x, z, (o.blockH?.[0] ?? 4) + r() * ((o.blockH?.[1] ?? 8) - (o.blockH?.[0] ?? 4))]); }
      const bs = o.blockS ?? Math.min(gx, gz) * 0.5, wall = new THREE.InstancedMesh(new THREE.BoxGeometry(bs, 1, bs).translate(0, 0.5, 0), new THREE.MeshLambertMaterial({ map: facadeTex() }), pts.length), roof = new THREE.InstancedMesh(new THREE.ConeGeometry(bs * 0.74, bs * 0.38, 4).rotateY(PI / 4), mat('#66788A'), pts.length);
      const o3 = new THREE.Object3D(), col = new THREE.Color(), WC = ['#EFE6D2', '#F2DCCB', '#F3E9C9', '#E8E1EE'];
      pts.forEach(([x, z, h], k) => { o3.position.set(x, 0, z); o3.rotation.set(0, 0, 0); o3.scale.set(1, h, 1); o3.updateMatrix(); wall.setMatrixAt(k, o3.matrix); wall.setColorAt(k, col.set(WC[k % 4])); o3.position.set(x, h + bs * 0.19, z); o3.scale.set(1, 1, 1); o3.updateMatrix(); roof.setMatrixAt(k, o3.matrix); });
      if (wall.instanceColor) wall.instanceColor.needsUpdate = true; wall.castShadow = roof.castShadow = wall.receiveShadow = true; g.add(wall, roof); }
    // his own puddle: a white ring round it instead of a glow sprite (the square glow patch showed); o.homeW wide
    let home = null, halo = null; if (o.home) { home = FLAQUE_PROPS.puddle({ w: o.homeW ?? 1.0, d: (o.homeW ?? 1.0) * 0.66 }); home.position.set(o.home[0], 0.03, o.home[1]); g.add(home);
      halo = new THREE.Mesh(new THREE.RingGeometry(0.62, 0.7, 40).rotateX(-PI / 2), basic('#FFFFFF', { opacity: 0.9 })); halo.scale.set((o.homeW ?? 1) * 1.05, 1, (o.homeW ?? 1) * 0.8); halo.position.set(o.home[0], 0.035, o.home[1]); g.add(halo); }
    // twinkles: small white crosses that flash on the filled puddles (o.twinkle: how many), so the held frame stays alive
    const tw = []; if (o.twinkle) { const geo = new THREE.PlaneGeometry(1, 0.12).rotateX(-PI / 2); for (let k = 0; k < o.twinkle; k++) { const q = grp(); const a = new THREE.Mesh(geo, basic('#FFFFFF', { opacity: 0.95 })), b2 = a.clone(); b2.rotation.y = PI / 2; q.add(a, b2); q.visible = false; g.add(q); tw.push({ q, c: cr[Math.floor(hsh(k + 40) * cr.length)] }); } }
    const xs = cr.map(c => c.x), xmin = Math.min(...xs), xmax = Math.max(...xs), zs = cr.map(c => c.z), zmin = Math.min(...zs), zmax = Math.max(...zs);
    g.userData.update = t => { cr.forEach(({ p, c, x, z, dust, i, j }) => {
        if (o.pop) { const tp = o.pop[0] + (o.pop[1] - o.pop[0]) * (zmax > zmin ? (z - zmin) / (zmax - zmin) : 0) + 0.06 * hsh(i * 5 + j), u = t - tp; c.visible = u >= 0; if (u >= 0) c.scale.setScalar(Math.max(0.01, outBack(u / 0.16)));
          dust.forEach((m, k) => { const v = (u - 0.02 * k) / 1.3; m.visible = v > 0 && v < 1; if (!m.visible) return; const a = k * TAU / dust.length + hsh(i + j) * 2; m.position.set(x + Math.cos(a) * R * 0.9 * Math.sqrt(v), 0.6 + 3.5 * v, z + Math.sin(a) * R * 0.9 * Math.sqrt(v)); m.scale.setScalar(0.5 + 1.4 * Math.sqrt(v)); m.material.opacity = 0.9 * (1 - v) * (1 - v); }); }
        if (!o.fill) { p.visible = !!o.wet; return; } const tf = o.fill[0] + (o.fill[1] - o.fill[0]) * (xmax > xmin ? (x - xmin) / (xmax - xmin) : 0) + hsh(x * 3) * 0.1;
        const s = smooth((t - tf) / 0.35); p.visible = s > 0.01; p.scale.set(Math.max(0.01, s), 1, Math.max(0.01, s));
        if (p.userData.rip) { const pr = p.children.filter(c => c.isMesh && c.geometry?.type === 'RingGeometry'); const live = p.userData.rip.filter(a => t >= a && t < a + 0.9);
          pr.forEach((rg, q) => { const a = live[q]; rg.visible = s > 0.9 && a != null; if (!rg.visible) return; const u = (t - a) / 0.9; rg.scale.set(0.1 + u * 0.8, 1, 0.1 + u * 0.8); rg.material.opacity = 0.9 * (1 - u); }); } });
      home?.userData.update(t); if (halo) { const k = 1 + 0.08 * Math.sin(t * 6); halo.scale.set((o.homeW ?? 1) * 1.05 * k, 1, (o.homeW ?? 1) * 0.8 * k); }
      tw.forEach(({ q, c }, k) => { if (!c || !c.p.visible || c.p.scale.x < 0.9) { q.visible = false; return; } const ph = (t * 1.3 + hsh(k + 7)) % 1, f = Math.max(0, Math.sin(ph * PI * 2.2)) ** 6; q.visible = f > 0.05; if (!q.visible) return;
        q.position.set(c.x + (hsh(k + 3) - 0.5) * R, 0.06, c.z + (hsh(k + 5) - 0.5) * R); q.scale.setScalar((0.3 + 1.1 * f) * (o.twinkleS ?? 1)); q.rotation.y = 0.4 + ph; }); };
    g.userData.update(0); return g;
  },

  // The minister's order form (pivot on the top of the podium where it starts): a white sheet o.w (0.36) wide, printed with lines and a row of
  // submarine pictograms, that unrolls along the polyline o.path [[x, y, z], ...] (relative to the pivot) as o.unroll [[t, 0..1], ...] says; a fat
  // paper roll rides its leading edge. The sheet is laid flat on each segment (tilted on the vertical ones)
  orderForm(o) {
    const W = o.w ?? 0.36, path = o.path || [[0, 0, 0], [0, 0, 0.3], [0, -1.1, 0.35], [0, -1.12, 3]], g = grp();
    const segs = []; let total = 0; for (let i = 1; i < path.length; i++) { const a = new THREE.Vector3(...path[i - 1]), b = new THREE.Vector3(...path[i]), L = a.distanceTo(b); segs.push({ a, b, L, s0: total }); total += L; }
    const tex = (() => { const c = document.createElement('canvas'); c.width = 128; c.height = 256; const x = c.getContext('2d'); x.fillStyle = o.paper || '#E8E4D6'; x.fillRect(0, 0, 128, 256);
      x.fillStyle = '#7E8890'; for (let i = 0; i < 9; i++) x.fillRect(14, 12 + i * 26, 100 - (i % 3) * 18, 5); x.fillStyle = '#4E5B68'; x.beginPath(); x.ellipse(64, 236, 34, 9, 0, 0, TAU); x.fill(); x.fillRect(58, 222, 10, 8);
      const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; return t; })();
    const meshes = segs.map(s => { const m = new THREE.Mesh(new THREE.PlaneGeometry(W, 1), new THREE.MeshLambertMaterial({ map: tex.clone(), side: THREE.DoubleSide })); m.material.map.needsUpdate = true; m.castShadow = true; m.receiveShadow = true; g.add(m); return m; });
    const RR = o.rollR ?? 0.1, roll = new THREE.Mesh(new THREE.CylinderGeometry(RR, RR, W * 1.02, 14), mat(o.paper || '#E8E4D6')); roll.rotation.z = PI / 2; addOutline(roll, 0.08); g.add(roll);
    const up = new THREE.Vector3(0, 1, 0), tmp = new THREE.Vector3(), q = new THREE.Quaternion();
    g.userData.update = t => {
      const u = keyAt(o.unroll, t, 0), len = Math.max(0.001, u * total); let end = segs[0].a.clone(), lastDir = new THREE.Vector3(0, 0, 1);
      segs.forEach((s, i) => { const m = meshes[i], l = Math.max(0, Math.min(s.L, len - s.s0)); m.visible = l > 0.002; if (!m.visible) return;
        const dir = tmp.copy(s.b).sub(s.a).normalize().clone(), mid = s.a.clone().addScaledVector(dir, l / 2); m.position.copy(mid); m.scale.set(1, l, 1);
        m.quaternion.setFromUnitVectors(up, dir);
        const want = Math.abs(dir.y) < 0.7 ? new THREE.Vector3(0, 1, 0) : new THREE.Vector3(0, 0, 1); want.addScaledVector(dir, -want.dot(dir)).normalize();
        const n0 = new THREE.Vector3(0, 0, 1).applyQuaternion(m.quaternion), ang = Math.atan2(new THREE.Vector3().crossVectors(n0, want).dot(dir), n0.dot(want));
        m.quaternion.premultiply(q.setFromAxisAngle(dir, ang));
        m.material.map.repeat.set(1, l / (W * 2)); if (l > 0) { end = s.a.clone().addScaledVector(dir, l); lastDir = dir.clone(); } });
      roll.position.copy(end); roll.position.y += RR + (o.hop ? o.hop[1] * Math.max(0, Math.sin(clamp01((t - o.hop[0]) / (o.hop[2] ?? 0.3)) * PI)) : 0); const ax = new THREE.Vector3().crossVectors(lastDir, Math.abs(lastDir.y) < 0.7 ? up : new THREE.Vector3(0, 0, 1)).normalize(); roll.quaternion.setFromUnitVectors(up, ax.lengthSq() > 0.5 ? ax : new THREE.Vector3(1, 0, 0)); roll.visible = u > 0.001 && (o.keepRoll || u < 0.999);
    };
    g.userData.update(0); return g;
  },

  // Periscopes popping out of a field of puddles (pivot at the middle of the field): o.pts [[x, z], ...] (or a grid o.nx × o.nz, o.gap 3.2 m over
  // o.w × o.d), each a dark grey pipe with a head and a black lens, in a little puddle; they shoot up together at o.at (a few hundredths apart),
  // overshoot and settle at o.h (0.9 m); o.turnAt [t, x, z]: every head turns to look at that point; o.skip [x, z, r]: none there (his puddle)
  periscopeField(o) {
    const g = grp(), pts = []; const gap = o.gap ?? 3.2, r = rng(o.seed || 4);
    if (o.pts) pts.push(...o.pts); else for (let x = -(o.w ?? 40) / 2; x <= (o.w ?? 40) / 2; x += gap) for (let z = -(o.d ?? 60); z <= 0; z += gap) pts.push([x + (r() - 0.5) * gap * 0.5, z + (r() - 0.5) * gap * 0.5]);
    const keep = pts.filter(([x, z]) => !o.skip || Math.hypot(x - o.skip[0], z - o.skip[1]) > o.skip[2]);
    // (round 1) a periscope that reads as one: a lighter grey pipe with a collar, a bent elbow, a head reaching forward with a bright glass window
    // and a white glint (the dark box heads read as bollards or cameras)
    const n = keep.length, H = o.h ?? 0.9, S = o.s ?? 1, PC = o.color || '#6F7B86', pipe = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.05 * S, 0.055 * S, 1, 8).translate(0, 0.5, 0), mat(PC), n);
    // (round 2) the head is a round tube lying forward with an angled hood over its mouth and a dark round lens with a white glint (the square head with
    // a flat pale window read as a parking meter or a speed camera, and had no direction): when the heads turn, the dark lenses swing round to him
    const HS = o.headS ?? 1, hr = 0.085 * S * HS, hl = 0.36 * S * HS;
    const headGeo = new THREE.CylinderGeometry(hr, hr, hl, 14).rotateX(PI / 2).translate(0, 0.03 * S, hl * 0.32), head = new THREE.InstancedMesh(headGeo, mat(PC), n);
    const hood = new THREE.InstancedMesh(new THREE.BoxGeometry(hr * 2.3, hr * 0.5, hl * 0.42).translate(0, 0.03 * S + hr * 0.95, hl * 0.62).rotateX(0), mat('#4E5862'), n); g.add(hood);
    const lens = new THREE.InstancedMesh(new THREE.CircleGeometry(hr * 0.86, 16).translate(0, 0.03 * S, hl * 0.82 + 0.004), basic('#141B24'), n);
    const ring = new THREE.InstancedMesh(new THREE.CircleGeometry(hr * 0.26, 8).translate(hr * 0.3, 0.03 * S + hr * 0.32, hl * 0.82 + 0.008), basic('#FFFFFF'), n); g.add(ring);
    const elbow = new THREE.InstancedMesh(new THREE.SphereGeometry(0.075 * S, 8, 6), mat(PC), n), collar = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.075 * S, 0.075 * S, 0.06 * S, 8), mat('#4E5862'), n); g.add(elbow, collar);
    const pud = new THREE.InstancedMesh(new THREE.CircleGeometry(0.55, 14).rotateX(-PI / 2), new THREE.MeshLambertMaterial({ color: '#7FC2EE', emissive: new THREE.Color('#5AA8DE'), emissiveIntensity: 0.4 }), n);
    pipe.castShadow = head.castShadow = true; g.add(pipe, head, lens, pud);
    const o3 = new THREE.Object3D(); keep.forEach(([x, z], i) => { o3.position.set(x, 0.012, z); o3.rotation.set(0, 0, 0); o3.scale.set(1 + 0.4 * hsh(i), 1, 0.8 + 0.4 * hsh(i + 1)); o3.updateMatrix(); pud.setMatrixAt(i, o3.matrix); }); pud.instanceMatrix.needsUpdate = true;
    g.userData.update = t => { keep.forEach(([x, z], i) => { const s = t - (o.at ?? 0) - 0.04 * hsh(i + 5), h = s <= 0 ? 0.001 : H * outBack(s / 0.22);
      let yaw = (hsh(i + 9) - 0.5) * 1.2; if (o.turnAt && t > o.turnAt[0]) { const want = Math.atan2(o.turnAt[1] - x, o.turnAt[2] - z), w = outBack((t - o.turnAt[0] - 0.02 * hsh(i + 2)) / (o.turnDur ?? 0.16)); yaw = yaw + (want - yaw) * w; }
      o3.position.set(x, -0.05, z); o3.rotation.set(0, 0, 0); o3.scale.set(1, Math.max(0.001, h + 0.05), 1); o3.updateMatrix(); pipe.setMatrixAt(i, o3.matrix);
      o3.position.set(x, -0.05 + h + 0.05, z); o3.rotation.set(0, yaw, 0); o3.scale.set(1, h > 0.01 ? 1 : 0.001, 1); o3.updateMatrix(); head.setMatrixAt(i, o3.matrix); lens.setMatrixAt(i, o3.matrix); ring.setMatrixAt(i, o3.matrix); elbow.setMatrixAt(i, o3.matrix); hood.setMatrixAt(i, o3.matrix);
      o3.position.set(x, 0.02, z); o3.rotation.set(0, 0, 0); o3.scale.set(1, h > 0.01 ? 1 : 0.001, 1); o3.updateMatrix(); collar.setMatrixAt(i, o3.matrix); });
      pipe.instanceMatrix.needsUpdate = head.instanceMatrix.needsUpdate = lens.instanceMatrix.needsUpdate = ring.instanceMatrix.needsUpdate = elbow.instanceMatrix.needsUpdate = collar.instanceMatrix.needsUpdate = hood.instanceMatrix.needsUpdate = true; };
    g.userData.update(0); return g;
  },

  // The town on its submarines (pivot at the middle of the slab's foot): a slab o.w (40) × o.d (40) × o.t (0.5) of street with blocks of buildings
  // on it (instanced, cream with windows and grey roofs, a street through the middle) and a round hole o.hole [x, z, r] where it does not reach
  // (his patch stays behind); a grid of grey hulls under it; o.liftAt (s): it rises by o.lift (3 m) in o.dur (0.45 s) with an overshoot and a bob,
  // spray bursting all round the edge; o.float: it rides on water instead (bobbing from the start, the hulls half sunk, o.lift ignored);
  // o.townHall: a town hall on it at o.thPos [x, z] facing +Z
  townLid(o) {
    const W = o.w ?? 40, D = o.d ?? 40, T = o.t ?? 0.5, g = grp(), R = grp(); g.add(R); const r = rng(o.seed || 13);
    const sh = new THREE.Shape(); sh.moveTo(-W / 2, -D / 2); sh.lineTo(W / 2, -D / 2); sh.lineTo(W / 2, D / 2); sh.lineTo(-W / 2, D / 2); sh.lineTo(-W / 2, -D / 2);
    if (o.hole) { const hp = new THREE.Path(); hp.absarc(o.hole[0], -o.hole[1], o.hole[2], 0, TAU, true); sh.holes.push(hp); }
    const slabGeo = new THREE.ExtrudeGeometry(sh, { depth: T, bevelEnabled: false, curveSegments: 28 }); slabGeo.rotateX(-PI / 2); slabGeo.translate(0, -T, 0);
    const slab = new THREE.Mesh(slabGeo, [mat(o.cap || '#6E6E72'), mat(o.side || '#8A847A')]); slab.castShadow = slab.receiveShadow = true; R.add(slab);   // (round 2) o.cap: the underside (earth) when it is seen from below
    const pave = new THREE.Mesh(new THREE.ShapeGeometry(sh, 28).rotateX(-PI / 2), mat('#E4D6BE')); pave.position.y = 0.006; pave.receiveShadow = true; R.add(pave);
    // (round 2) the floor under the town and his patch stand 5-7 cm proud of the set's ground: at 4-12 mm the grassland showed through them for a frame
    // (a bright green flash of the pit's floor); o.underY / o.patchY move them
    const UY = o.underY ?? 0.05, PY = o.patchY ?? 0.065;
    let un = null; if (o.under) { un = new THREE.Mesh(new THREE.PlaneGeometry(W, D).rotateX(-PI / 2), mat(o.under === true ? '#3E362F' : o.under)); un.position.y = UY; un.receiveShadow = true; g.add(un); }
    if (o.hole && o.patch !== false) { const PR = o.patchR ?? o.hole[2] * 0.985, PC = o.patchAt || [o.hole[0], o.hole[1]]; const pt = new THREE.Mesh(new THREE.CircleGeometry(PR, 32).rotateX(-PI / 2), mat(o.patchColor || '#6E6E72')); pt.position.set(PC[0], PY, PC[1]); pt.receiveShadow = true; g.add(pt);
      const kerb = new THREE.Mesh(new THREE.RingGeometry(PR * 0.93, PR, 32).rotateX(-PI / 2), mat('#D9CDB4')); kerb.position.set(PC[0], PY + 0.004, PC[1]); g.add(kerb); }
    const rx = o.roadX ?? 0, RH = (o.roadW ?? 9) / 2, rs = new THREE.Shape(); rs.moveTo(rx - RH, -D / 2); rs.lineTo(rx + RH, -D / 2); rs.lineTo(rx + RH, D / 2); rs.lineTo(rx - RH, D / 2); rs.lineTo(rx - RH, -D / 2);
    // (round 1) a hole wider than the road cuts it in two: a hole path that pokes out of the strip's outline is ignored by the triangulation (the
    // road then covered the hole), so the strip is built as two pieces that stop on the circle
    const roadShapes = []; const [hx, hz, hr] = o.hole || [0, 0, 0];
    if (o.hole && Math.abs(hx - rx) < RH + hr && hr >= RH + Math.abs(hx - rx) - 0.01) {
      const arc = (z0, side) => { const pts = []; for (let k = 0; k <= 16; k++) { const x = rx - RH + 2 * RH * k / 16, dz = Math.sqrt(Math.max(0, hr * hr - (x - hx) * (x - hx))); pts.push([x, hz + side * dz]); } return pts; };
      const lo = arc(0, -1), hi = arc(0, 1);
      const A = new THREE.Shape(); A.moveTo(rx - RH, D / 2); A.lineTo(rx + RH, D / 2); for (let k = lo.length - 1; k >= 0; k--) A.lineTo(lo[k][0], -lo[k][1]); A.closePath(); roadShapes.push(A);
      const Bs = new THREE.Shape(); Bs.moveTo(rx - RH, -D / 2); hi.forEach(([x, z]) => Bs.lineTo(x, -z)); Bs.lineTo(rx + RH, -D / 2); Bs.closePath(); roadShapes.push(Bs);
    } else { if (o.hole && Math.abs(hx - rx) < RH + hr) { const hp2 = new THREE.Path(); hp2.absarc(hx, -hz, hr, 0, TAU, true); rs.holes.push(hp2); } roadShapes.push(rs); }
    roadShapes.forEach(sh_ => { const road = new THREE.Mesh(new THREE.ShapeGeometry(sh_, 28).rotateX(-PI / 2), mat('#6E6E72')); road.position.y = 0.012; road.receiveShadow = true; R.add(road); });
    // (round 1) o.blockAlign 'road': the block columns start at the road's kerbs and go outward (with a narrow road, the default grid from the
    // slab's edge left no column beside the road)
    const blocks = []; const B = o.block ?? 9, xsB = [];
    if (o.blockAlign === 'road') { for (let k = 0; ; k++) { const d = RH + 0.6 + B / 2 + k * (B + 1.5); if (rx + d > W / 2 - B / 2 + 0.01 && rx - d < -W / 2 + B / 2 - 0.01) break; if (rx + d <= W / 2 - B / 2 + 0.01) xsB.push(rx + d); if (rx - d >= -W / 2 + B / 2 - 0.01) xsB.push(rx - d); } }
    else for (let x = -W / 2 + B / 2 + 0.5; x <= W / 2 - B / 2; x += B + 1.5) xsB.push(x);
    for (const x of xsB) for (let z = -D / 2 + B / 2 + 0.5; z <= D / 2 - B / 2; z += B + 1.5) {
      if (Math.abs(x - (o.roadX ?? 0)) < RH + B / 2) continue; if (o.hole && Math.hypot(x - o.hole[0], z - o.hole[1]) < o.hole[2] + (o.holeGap ?? B * 0.75)) continue; if (o.thPos && Math.hypot(x - o.thPos[0], z - o.thPos[1]) < 9) continue; if (o.tower && Math.hypot(x - o.tower[0], z - o.tower[1]) < B * 0.75 + (o.tower[3] ?? 1.6)) continue; blocks.push([x, z, (o.hMin ?? 10) + r() * ((o.hMax ?? 17) - (o.hMin ?? 10))]); }
    const WC = ['#EFE6D2', '#F2DCCB', '#F3E9C9', '#E8E1EE', '#F0D9D9'];
    // (round 2) o.paris: the blocks are the street's own Haussmann buildings (scaled to the block, facades toward +Z, the grey-blue mansard roofs,
    // dormers, chimney pots): the cream boxes with pyramid roofs read as a modern town, not the Paris street of the first shots
    if (o.paris) { const AW = ['#B5302A', '#2F7F5C', '#2F5E8C', '#C9822E'], sc = B / 12;
      blocks.forEach(([x, z, h], i) => { const b = buildProp('haussmann', { w: 12, d: 12, h: Math.max(10, h / sc), floors: 6, cols: 5, color: WC[i % WC.length], awning: AW[i % 4], seed: i + (o.seed || 0) }); b.scale.setScalar(sc); b.position.set(x, 0, z + B / 2); b.traverse(c => { if (c.isMesh) { c.castShadow = true; c.receiveShadow = true; } }); R.add(b); }); }
    else { const tex = facadeTex(); const bw = new THREE.InstancedMesh(new THREE.BoxGeometry(B, 1, B).translate(0, 0.5, 0), new THREE.MeshLambertMaterial({ map: tex }), Math.max(1, blocks.length)), br = new THREE.InstancedMesh(o.pitched ? new THREE.ConeGeometry(B * 0.72, B * 0.4, 4).rotateY(PI / 4) : new THREE.BoxGeometry(B * 0.96, 2.2, B * 0.96), mat(o.roof || '#7C8A99'), Math.max(1, blocks.length));
      const o3 = new THREE.Object3D(), col = new THREE.Color();
      blocks.forEach(([x, z, h], i) => { o3.position.set(x, 0, z); o3.scale.set(1, h, 1); o3.updateMatrix(); bw.setMatrixAt(i, o3.matrix); bw.setColorAt(i, col.set(WC[i % WC.length])); o3.position.set(x, h + (o.pitched ? B * 0.2 : 1.1), z); o3.scale.set(1, 1, 1); o3.updateMatrix(); br.setMatrixAt(i, o3.matrix); });
      if (bw.instanceColor) bw.instanceColor.needsUpdate = true; bw.count = br.count = blocks.length; bw.castShadow = br.castShadow = bw.receiveShadow = true; R.add(bw, br); }
    // (round 2) o.thW / o.thH / o.thD: the town hall's size; o.thDoor: a dark double door between its two middle columns with a lit gap under it
    // (a parking ticket goes under it); userData.thDoor: the foot of that door (lid frame)
    const thW = o.thW ?? 8, thH = o.thH ?? 5.5, thD = o.thD ?? 4.5;
    if (o.townHall) { const th = buildProp('townHall', { w: thW, h: thH, d: thD, gable: 'v2' }); th.position.set(o.thPos[0], 0, o.thPos[1]); R.add(th);
      if (o.thDoor) { const dw = o.thDoor.w ?? 0.95, dh = o.thDoor.h ?? 2.0, dz = o.thPos[1] + thD / 2 + 0.012;
        R.add(at(box(dw + 0.16, dh + 0.1, 0.05, '#E2D8C4', { pivot: 'bottom', outline: 0.006 }), o.thPos[0], 0.25, dz - 0.02), at(box(dw, dh, 0.06, o.thDoor.color || '#2F4A3A', { pivot: 'bottom', outline: 0.006 }), o.thPos[0], 0.29, dz),
          at(box(0.02, dh * 0.92, 0.065, '#1E2E26'), o.thPos[0], 0.29 + dh * 0.5, dz + 0.004), at(box(dw, 0.04, 0.07, '#141814'), o.thPos[0], 0.27, dz + 0.004));
        for (const sx of [-1, 1]) { const kn = sphere(0.035, '#D8B64A', 0); kn.position.set(o.thPos[0] + sx * 0.08, 0.29 + dh * 0.48, dz + 0.05); R.add(kn); } } }
    let tower = null; if (o.tower) { tower = clockTower(o.tower[3] ?? 1.6, o.tower[2] ?? 8); tower.position.set(o.tower[0], o.towerY ?? 0, o.tower[1]); R.add(tower); }
    const hulls = []; const HL = o.hullL ?? 9, Hh = HL * 0.26, NO = o.noseOut ?? 0, zA = -D / 2 + HL / 2 - NO, zB = D / 2 - HL / 2 + NO, nzH = Math.max(1, Math.round((zB - zA) / (HL + 1)) + 1), zs = Array.from({ length: nzH }, (_, k) => nzH === 1 ? 0 : zA + (zB - zA) * k / (nzH - 1));
    if (!o.subs) for (let x = -W / 2 + 3; x <= W / 2 - 3; x += o.hullGap ?? 6) for (const z of zs) {
      if (o.hole && Math.abs(x - o.hole[0]) < o.hole[2] + Hh && Math.abs(z - o.hole[1]) < o.hole[2] + HL / 2 + 0.5) continue;
      const h = new THREE.Mesh(new THREE.CapsuleGeometry(Hh / 2, HL - Hh, 5, 12), mat('#5E6B7A')); h.rotation.x = PI / 2; h.position.set(x, -T - Hh / 2 + 0.15, z); h.castShadow = true; R.add(h); hulls.push(h);
      const tw = box(Hh * 0.4, Hh * 0.5, HL * 0.18, '#5E6B7A', { outline: 0.01 }); tw.position.set(x, -T - Hh * 0.27, z); R.add(tw);
      if (NO > 0) { const bandM = new THREE.Mesh(new THREE.CylinderGeometry(Hh * 0.51, Hh * 0.51, HL * 0.05, 18, 1, true), mat('#C8322A')); bandM.rotation.x = PI / 2; bandM.position.set(x, -T - Hh / 2 + 0.15, z + (z >= 0 ? 1 : -1) * HL * 0.3); R.add(bandM); } }
    // (round 3) o.subs [[x, z, ry], ...]: real submarines (the S04 / S05 model: conning tower, red band, fins, propeller) carry the slab on the tops of
    // their conning towers, lying where they are put (ry PI / 2: along X, side-on to a camera on Z), instead of the grid of plain capsules (o.hullL
    // etc. then unused); o.subLen (6 m); each one rose out of its own puddle on the ground, and throws white spray off its sides as it comes up
    const subs = []; if (o.subs) { const SL = o.subLen ?? 6, SH = SL * 0.26, top = SH * 1.52;
      o.subs.forEach(([x, z, ry]) => { const s = buildProp('submarine', { len: SL, color: o.subColor || '#5E6B7A' }); s.rotation.y = ry ?? PI / 2; s.position.set(x, -T - top + 0.02, z); s.traverse(c => { if (c.isMesh) c.castShadow = true; }); R.add(s);
        const pd = FLAQUE_PROPS.puddle({ w: SL * 0.95, d: SH * 1.6, seed: 31 + subs.length }); pd.rotation.y = (ry ?? PI / 2) - PI / 2; pd.position.set(x, UY + 0.012, z); pd.visible = false; g.add(pd);
        const puffs = []; for (let k = 0; k < 7; k++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(0.45, 1), basic('#FFFFFF', { opacity: 0.9 })); m.visible = false; g.add(m); puffs.push(m); }
        subs.push({ s, x, z, ry: ry ?? PI / 2, pd, puffs, SL }); }); }
    // (round 3) o.shaft: a column of sunlight falling through the hole onto his patch once the town is up (o.shaft {r, color, opacity}), and a bright
    // pool on the patch
    let shaft = null, pool = null; if (o.shaft && o.hole) { const sr = o.shaft.r ?? o.hole[2] * 0.8, PC = o.patchAt || [o.hole[0], o.hole[1]];
      // soft: the column fades out toward the ground and at its sides (an open cylinder with even alpha read as a glass jar round him)
      const grad = (() => { const c = document.createElement('canvas'); c.width = 64; c.height = 64; const x = c.getContext('2d'), gy = x.createLinearGradient(0, 0, 0, 64); gy.addColorStop(0, 'rgba(255,255,255,1)'); gy.addColorStop(0.7, 'rgba(255,255,255,0.45)'); gy.addColorStop(1, 'rgba(255,255,255,0)');
        x.fillStyle = gy; x.fillRect(0, 0, 64, 64); const gx = x.createLinearGradient(0, 0, 64, 0); gx.addColorStop(0, 'rgba(0,0,0,1)'); gx.addColorStop(0.5, 'rgba(0,0,0,0)'); gx.addColorStop(1, 'rgba(0,0,0,1)'); x.globalCompositeOperation = 'destination-out'; x.fillStyle = gx; x.fillRect(0, 0, 64, 64);
        const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
      shaft = new THREE.Mesh(new THREE.CylinderGeometry(sr * 0.8, sr * 1.1, 1, 28, 1, true).translate(0, 0.5, 0), new THREE.MeshBasicMaterial({ color: o.shaft.color || '#FFF4D2', map: grad, transparent: true, opacity: o.shaft.opacity ?? 0.22, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.FrontSide }));
      shaft.position.set(PC[0], PY + 0.01, PC[1]); shaft.visible = false; shaft.castShadow = false; g.add(shaft);
      const rad = (() => { const c = document.createElement('canvas'); c.width = c.height = 64; const x = c.getContext('2d'), gr = x.createRadialGradient(32, 32, 1, 32, 32, 31); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.6, 'rgba(255,255,255,0.6)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = gr; x.fillRect(0, 0, 64, 64); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
      pool = new THREE.Mesh(new THREE.PlaneGeometry(sr * 2.4, sr * 2.4).rotateX(-PI / 2), new THREE.MeshBasicMaterial({ color: '#FFF0C0', map: rad, transparent: true, opacity: 0.4, depthWrite: false, blending: THREE.AdditiveBlending })); pool.position.set(PC[0], PY + 0.012, PC[1]); pool.visible = false; g.add(pool); }
    const spray = []; for (let i = 0; i < (o.subs ? 0 : 40); i++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(0.7, 1), new THREE.MeshLambertMaterial({ color: '#FFFFFF', emissive: new THREE.Color('#DDEFFF'), emissiveIntensity: 0.3, transparent: true, opacity: 0.95 })); m.visible = false; g.add(m); spray.push(m); }
    const per = (i) => { const k = i / 40 * 4, side = Math.floor(k), f = k - side; return side === 0 ? [-W / 2 + W * f, D / 2] : side === 1 ? [W / 2, D / 2 - D * f] : side === 2 ? [W / 2 - W * f, -D / 2] : [-W / 2, -D / 2 + D * f]; };
    g.userData.update = t => {
      if (o.float) { R.position.y = (o.floatY ?? 0.9) + (o.bob ?? 0.08) * Math.sin(t * 1.6); R.rotation.z = 0.01 * Math.sin(t * 1.1); R.rotation.x = 0.008 * Math.sin(t * 1.3 + 1); }
      else { const u = (t - (o.liftAt ?? 99)) / (o.dur ?? 0.45), L = o.lift ?? 3, B0 = o.baseY ?? 0;   // (round 2) o.baseY: the town stands that much proud of the set's ground at rest (on grassland its street flickered)
        // (round 3) o.sink [dur, depth, shake]: for dur s before o.liftAt the town shudders and sinks by depth (anticipation), then rises from there
        const [sd0, sdp, ssh] = o.sink || [0, 0, 0], us = sd0 > 0 ? (t - (o.liftAt ?? 99) + sd0) / sd0 : -1, dn = u > 0 ? sdp : sdp * smooth(us);
        R.position.y = (u <= 0 ? B0 - dn : u < 1 ? B0 - sdp + (L + sdp) * outBack(u) : B0 + L + 0.12 * Math.sin((u - 1) * 9) * Math.exp(-(u - 1) * 2));
        const sh = (us > 0 && u < 0.35) ? (ssh || 0) : 0; R.position.x = sh * Math.sin(t * 97); R.position.z = sh * 0.6 * Math.sin(t * 71 + 1); }
      if (un) un.visible = R.position.y > (o.baseY ?? 0) + 0.08;   // (round 2) the dark floor under the town shows only once it has lifted (at rest it lay over the street)
      const up = R.position.y - (o.baseY ?? 0);
      if (shaft) { shaft.visible = pool.visible = up > 0.6; if (shaft.visible) { shaft.scale.y = Math.max(0.1, R.position.y - T - PY); const k = clamp01((up - 0.6) / 1.2); shaft.material.opacity = (o.shaft.opacity ?? 0.22) * k; pool.material.opacity = 0.4 * k; } }
      subs.forEach(({ pd, puffs, x, z, ry, SL }, j) => { pd.visible = up > 0.3; const su = t - (o.liftAt ?? 99) - 0.03 * j;
        puffs.forEach((m, k) => { const v = (su - 0.02 * k) / 0.8; m.visible = !o.float && v > 0 && v < 1; if (!m.visible) return; const along = (k / 6 - 0.5) * SL * 0.9, side = (k % 2 ? 1 : -1) * (SL * 0.16 + 0.9 * v);
          const lx = Math.abs(Math.sin(ry)) > 0.5 ? along : side, lz = Math.abs(Math.sin(ry)) > 0.5 ? side : along; m.position.set(x + lx, 0.3 + 2.2 * Math.sin(v * PI * 0.7), z + lz); m.scale.setScalar(0.6 + 1.3 * Math.sqrt(v)); m.material.opacity = 0.92 * (1 - v); }); });
      const su = t - (o.liftAt ?? 99), SS = o.sprayS ?? 1; spray.forEach((m, i) => { const v = (su - 0.01 * (i % 7)) / (o.sprayLife ?? 1.1); m.visible = !o.float && v > 0 && v < 1; if (!m.visible) return; const [x, z] = per(i);   // (round 2) o.sprayS, o.sprayLife: smaller, shorter spray (near the lens the puffs hid the whole town)
        m.position.set(x * (1 + 0.05 * v), 0.4 + 4 * SS * Math.sin(v * PI * 0.8), z * (1 + 0.05 * v)); m.scale.setScalar((0.5 + 1.6 * Math.sqrt(v)) * SS); m.material.opacity = 0.95 * (1 - v); });
    };
    g.userData.update(0); g.userData.thDoor = o.thPos ? [o.thPos[0], 0.29, o.thPos[1] + thD / 2 + 0.05] : null; g.userData.ropeY = tower?.userData.ropeY; return g;
  },

  // A harbour quay (pivot at the middle of its sea edge, the sea toward -Z): a stone quay o.len (30) long, o.h (1.4) above the water, o.dep (6) deep
  // toward +Z, a kerb and two black bollards (userData.bollard: the one at o.bx); o.rope {to: [x, y, z], sag}: a thick mooring rope from that
  // bollard to a point (relative to the pivot), sagging, with a loop at its far end
  harbourQuay(o) {
    const Lq = o.len ?? 30, H = o.h ?? 1.4, Dp = o.dep ?? 6, g = grp();
    const wall = canvasPlane(Lq, H + 2, (c, Wc, Hc) => { c.fillStyle = '#B9AE98'; c.fillRect(0, 0, Wc, Hc); c.strokeStyle = 'rgba(70,60,45,0.5)'; c.lineWidth = 3; for (let y = 0; y < Hc; y += Hc / 6) { c.beginPath(); c.moveTo(0, y); c.lineTo(Wc, y); c.stroke(); for (let x = (y / (Hc / 6)) % 2 ? 0 : Wc / 40; x < Wc; x += Wc / 20) { c.beginPath(); c.moveTo(x, y); c.lineTo(x, y + Hc / 6); c.stroke(); } }
      c.fillStyle = 'rgba(40,70,60,0.5)'; c.fillRect(0, Hc * 0.82, Wc, Hc * 0.18); }, { res: 1024 });
    wall.position.set(0, H / 2 - 1, 0); g.add(wall, at(box(Lq, H + 2, Dp, '#A69B85'), 0, H / 2 - 1, Dp / 2 + 0.01), at(box(Lq, 0.25, 0.6, '#D3C9B4', { outline: 0.01 }), 0, H + 0.12, 0.3));
    const top = new THREE.Mesh(new THREE.PlaneGeometry(Lq, Dp).rotateX(-PI / 2), mat('#CFC5AE')); top.position.set(0, H + 0.005, Dp / 2); top.receiveShadow = true; g.add(top);
    // (round 1) a mooring bollard that reads as one: a squat cast-iron post that flares into a rounded cap (the straight post with a flat disc read
    // as a top hat), and a hemp rope (no black outline: it read as a rigid black-and-gold beam) that sags in a real curve
    // (round 2) a squat metal-grey bollard (it still read as a black top hat): a wide square foot plate, a fat body that narrows to a waist, then flares
    // out into a broad rounded head that leans toward the sea, a pale rim of wear on the head; o.bollardS scales it
    // (round 3) o.bollardStyle 'mushroom': a short black cast-iron mushroom, no band or rim (the grey dome with a pale rim and the rope's eye round its
    // waist read as a giant kepi or a drum next to the gendarme's kepi): a squat post, then a broad flat round head
    // (round 3) o.bxs [x, ...]: where the bollards stand (the rope leaves from the first); default [o.bx, o.bx + 8]
    const bx = o.bxs ? o.bxs[0] : (o.bx ?? 0), BS = o.bollardS ?? 1.3, MU = o.bollardStyle === 'mushroom', BC = o.bollardColor || (MU ? '#1E2226' : '#5C646C'); const bol = []; for (const x of (o.bxs || [bx, bx + 8])) {
      const b = MU ? grp(at(cyl(0.15, 0.19, 0.5, BC, 16, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0)) : grp(at(box(0.62, 0.06, 0.62, '#474D53', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(cyl(0.18, 0.26, 0.26, BC, 14, { pivot: 'bottom', outline: 0.01 }), 0, 0.06, 0), at(cyl(0.26, 0.18, 0.14, BC, 14, { pivot: 'bottom', outline: 0.01 }), 0, 0.32, 0));
      const head = sphere(MU ? 0.23 : 0.3, BC, 0); head.scale.set(MU ? 1.0 : 1.12, MU ? 0.62 : 0.5, MU ? 1.0 : 1.12); head.position.set(0, MU ? 0.5 : 0.5, MU ? 0 : -0.04); addOutline(head, 0.02); b.add(head);   // (round 3) mushroom: a taller post, a head only a little wider (a wide flat head read as a hat from above)
      if (!MU) { const rim = new THREE.Mesh(new THREE.TorusGeometry(0.3, 0.025, 6, 20).rotateX(PI / 2), mat('#9AA3AB')); rim.position.set(0, 0.5, -0.04); b.add(rim); }
      b.scale.setScalar(BS); b.position.set(x, H, 0.9); g.add(b); bol.push(b); }
    const RC = o.rope?.color || '#B88E55';
    if (o.rope) { const a = new THREE.Vector3(bx, H + (MU ? 0.3 : 0.33) * BS, 0.9), b = new THREE.Vector3(...o.rope.to), sag = o.rope.sag ?? 1.2, pts = [];
      for (let k = 0; k <= 16; k++) { const u = k / 16, p = a.clone().lerp(b, u); p.y -= sag * 4 * u * (1 - u); pts.push(p); }
      const curve = new THREE.CatmullRomCurve3(pts), tube = new THREE.Mesh(new THREE.TubeGeometry(curve, 64, o.rope.r ?? 0.09, 8, false), mat(RC)); tube.castShadow = true; g.add(tube);
      const loop = new THREE.Mesh(new THREE.TorusGeometry(o.rope.loopR ?? 0.9, (o.rope.r ?? 0.09) * 1.05, 8, 24), mat(RC)); loop.position.set(...(o.rope.loopAt || [b.x, b.y, b.z])); loop.rotation.x = PI / 2; g.add(loop);   // (round 3) o.rope.loopAt: the loop's centre (round the belfry) when the rope ends on its front
      const loop2 = new THREE.Mesh(new THREE.TorusGeometry((MU ? 0.175 : 0.21) * BS, MU ? 0.035 : 0.07, 6, 14), mat(RC)); loop2.position.set(bx, H + (MU ? 0.3 : 0.33) * BS, 0.9); loop2.rotation.x = PI / 2; g.add(loop2); }
    g.userData.bollard = [bx, H, 0.9]; return g;
  },

  // A wall map (pivot at its middle, front +Z): a pale country o.w (2.4) × o.h (1.7) with a blue sea along its left side, a few rivers and dotted
  // roads, and a town pictogram (three roofs and a little clock tower, in a white disc) that slides from inland o.from [u, v] to the coast o.to
  // between o.slide [t0, t1] (eased), leaving a dashed trail; userData.at(t): where the pictogram is (local metres)
  townMapWall(o) {
    const W = o.w ?? 2.4, H = o.h ?? 1.7, g = grp(at(box(W + 0.1, H + 0.1, 0.04, '#6B4F3A', { outline: 0.008 }), 0, 0, -0.025));
    const map = canvasPlane(W, H, (c, Wc, Hc) => { c.fillStyle = '#7DC3E8'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#F2E6C4';
      c.beginPath(); c.moveTo(Wc * 0.28, 0); for (let i = 0; i <= 10; i++) c.lineTo(Wc * (0.24 + 0.06 * Math.sin(i * 1.7)), Hc * i / 10); c.lineTo(Wc, Hc); c.lineTo(Wc, 0); c.closePath(); c.fill();
      c.lineWidth = Wc * 0.006; c.strokeStyle = '#4A3B2A'; c.stroke(); c.strokeStyle = '#5B9BD0'; c.lineWidth = Wc * 0.004; for (const [y0, y1] of [[0.15, 0.4], [0.55, 0.85]]) { c.beginPath(); c.moveTo(Wc * 0.9, Hc * y0); c.quadraticCurveTo(Wc * 0.6, Hc * (y0 + y1) / 2, Wc * 0.3, Hc * y1); c.stroke(); }
      c.setLineDash([Wc * 0.012, Wc * 0.01]); c.strokeStyle = '#B28A5A'; c.beginPath(); c.moveTo(Wc * 0.4, Hc * 0.2); c.lineTo(Wc * 0.85, Hc * 0.7); c.stroke(); c.setLineDash([]);
      c.fillStyle = '#4A3B2A'; for (const [x, y] of [[0.5, 0.3], [0.8, 0.25], [0.45, 0.75], [0.7, 0.85]]) { c.beginPath(); c.arc(x * Wc, y * Hc, Wc * 0.008, 0, TAU); c.fill(); }
      c.fillStyle = '#FFFFFF'; c.font = `900 ${Hc * 0.06}px Arial`; c.textAlign = 'center'; c.fillText('MER', Wc * 0.11, Hc * 0.5); }, { res: 768 });
    g.add(map);
    const icon = canvasPlane(0.3, 0.3, (c, Wc, Hc) => { c.clearRect(0, 0, Wc, Hc); c.fillStyle = '#FFFFFF'; c.beginPath(); c.arc(Wc / 2, Hc / 2, Wc * 0.46, 0, TAU); c.fill(); c.strokeStyle = '#C8322A'; c.lineWidth = Wc * 0.05; c.stroke();
      c.fillStyle = '#2E4563'; for (const [x, w, h] of [[0.22, 0.16, 0.22], [0.42, 0.16, 0.34], [0.62, 0.16, 0.26]]) { c.fillRect(Wc * x, Hc * (0.72 - h), Wc * w, Hc * h); c.beginPath(); c.moveTo(Wc * (x - 0.02), Hc * (0.72 - h)); c.lineTo(Wc * (x + w / 2), Hc * (0.6 - h)); c.lineTo(Wc * (x + w + 0.02), Hc * (0.72 - h)); c.fill(); } }, { res: 128, transparent: true, emissive: 0.4 });
    g.add(icon);
    const trail = []; for (let i = 0; i < 9; i++) { const d = new THREE.Mesh(new THREE.CircleGeometry(0.018, 8), basic('#C8322A')); g.add(d); trail.push(d); }
    const [fu, fv] = o.from || [0.7, 0.45], [tu, tv] = o.to || [0.3, 0.55], P = (u, v) => [(u - 0.5) * W, (0.5 - v) * H];
    const pos = t => { const s = o.slide ? smooth((t - o.slide[0]) / Math.max(0.01, o.slide[1] - o.slide[0])) : 0; return [fu + (tu - fu) * s, fv + (tv - fv) * s, s]; };
    g.userData.update = t => { const [u, v, s] = pos(t), [x, y] = P(u, v); icon.position.set(x, y, 0.01); trail.forEach((d, i) => { const k = (i + 1) / 10; d.visible = k < s; const [a, b] = P(fu + (tu - fu) * k, fv + (tv - fv) * k); d.position.set(a, b, 0.006); }); };
    g.userData.at = t => { const [u, v] = pos(t); const [x, y] = P(u, v); return [x, y, 0.01]; };
    g.userData.update(0); return g;
  },

  // Where the town used to be (pivot at the middle): a wide disc of bare brown earth o.r (90 m) with rows of empty pits (where the hulls rose out),
  // and in its middle a small round patch of pavement o.patch (2.6 m radius) with a kerb on one side and a stub of road with a dashed line
  barePlain(o) {
    const R = o.r ?? 90, g = grp(), r = rng(o.seed || 17);
    const gnd = new THREE.Mesh(new THREE.CircleGeometry(R, 48).rotateX(-PI / 2), mat(o.ground || '#B39A78')); gnd.position.y = 0.002; gnd.receiveShadow = true; g.add(gnd);
    const pr = o.patch ?? 2.6, patch = new THREE.Mesh(new THREE.CylinderGeometry(pr, pr * 1.04, 0.14, 32), mat('#E4D6BE')); patch.position.y = 0.07; patch.receiveShadow = true; patch.castShadow = true; addOutline(patch, 0.02); g.add(patch);
    const roadPart = new THREE.Mesh(new THREE.CircleGeometry(pr * 0.995, 32, PI * 0.5, PI).rotateX(-PI / 2), mat('#6E6E72')); roadPart.position.set(-pr * 0.35, 0.142, 0); roadPart.scale.set(0.65, 1, 1); g.add(roadPart);
    g.add(at(box(0.22, 0.12, pr * 1.6, '#D9CDB4', { outline: 0.006 }), -pr * 0.36, 0.2, 0));
    const pits = []; for (let x = -R * 0.6; x <= R * 0.6; x += o.pitGap ?? 7) for (let z = -R * 0.7; z <= -6; z += 11) { if (Math.abs(x) < 6 && z > -12) continue; pits.push([x + (r() - 0.5) * 1.5, z]); }
    const pit = new THREE.InstancedMesh(new THREE.CircleGeometry(1, 16).rotateX(-PI / 2), mat('#6E5843'), pits.length), o3 = new THREE.Object3D();
    // (round 2) the pits 4 cm over the disc and never culled (at 8 mm they and the disc's colour vanished for a single frame, twice, in a slow push)
    pits.forEach(([x, z], i) => { o3.position.set(x, 0.042, z); o3.scale.set(1.3, 1, 4.2); o3.updateMatrix(); pit.setMatrixAt(i, o3.matrix); }); pit.receiveShadow = true; pit.frustumCulled = false; g.add(pit);
    gnd.frustumCulled = false;
    return g;
  },

  // (round 1) A press podium without the microphones on its front edge (they stood in front of the order form and read as drumsticks): the same
  // navy box and top as the podium (top at 1.145 m); o.mics [x, ...]: microphones at those x on the back edge instead
  plainPodium(o) {
    const g = grp(at(box(0.7, 1.1, 0.5, '#2E3A5C', { pivot: 'bottom', taper: { x: 0.85, z: 0.85 }, outline: 0.006 }), 0, 0, 0), at(box(0.8, 0.05, 0.55, '#43527A'), 0, 1.12, 0));
    for (const x of (o.mics || [])) { g.add(at(cyl(0.008, 0.008, 0.3, '#1E2126', 5, { pivot: 'bottom' }), x, 1.14, -0.2, -0.3, 0, 0)); const b = sphere(0.03, '#1E2126', 0); b.position.set(x, 1.42, -0.12); g.add(b); }
    return g;
  },

  // (round 1) A wet sock being wrung (attach to a hand: it hangs from the grip): a square-section striped tube o.len (0.42 m) in o.n (9) segments;
  // o.wring [[t, 0..1], ...]: how wrung it is (the segments turn into a spiral, the tube gets thinner and shorter, drops squeeze out); o.spring t:
  // it springs back (untwists past zero, overshoots and wobbles, a burst of drops); o.colors [body, stripe, toe]
  wrungSock(o) {
    const [cb, cs, ct] = o.colors || ['#E9E4D6', '#C8322A', '#2E4563'], n = o.n ?? 9, L = o.len ?? 0.42, seg = L / n, g = grp(), S = [];
    const TW = o.w ?? 0.075;   // (round 2) o.w: the sock's thickness (a bigger sock reads at phone size)
    for (let i = 0; i < n; i++) { const m = box(TW, seg * 1.02, TW, i % 3 === 1 ? cs : (i === n - 1 ? ct : cb), { pivot: 'top', outline: 0.004 }); g.add(m); S.push(m); }
    const toe = box(TW, TW * 1.35, TW * 1.07, ct, { pivot: 'top', outline: 0.004 }); g.add(toe);
    const drops = []; for (let i = 0; i < 10; i++) { const d = new THREE.Mesh(new THREE.SphereGeometry(0.012, 6, 4), basic('#9FD8FF')); d.visible = false; g.add(d); drops.push(d); }
    g.userData.update = t => {
      let w = keyAt(o.wring, t, 0); const sp = o.spring != null ? t - o.spring : -1; if (sp >= 0) w = w * Math.exp(-sp * 5) * Math.cos(sp * 22);
      const k = 1 - 0.35 * Math.abs(w);
      let y = 0; S.forEach((m, i) => { m.position.set(0, y, 0); m.rotation.set(0, w * i * 0.55, 0); m.scale.set(k, 1 - 0.25 * Math.abs(w), k); y -= seg * (1 - 0.25 * Math.abs(w)); });
      toe.position.set(0, y, 0.0); toe.rotation.set(-1.0 + 0.5 * Math.abs(w), w * n * 0.55, 0);
      drops.forEach((d, i) => { const per = 0.35, ph = ((t + hsh(i) * per) % per) / per, burst = sp >= 0 && sp < 0.4; const on = Math.abs(w) > 0.3 || burst; d.visible = on; if (!on) return;
        const yy = -L * (0.3 + 0.6 * hsh(i + 2)) * (1 - 0.25 * Math.abs(w)), a = hsh(i + 5) * TAU, out = burst ? 0.6 * sp : 0.03 * ph; d.position.set(Math.cos(a) * (0.05 + out), yy - 0.6 * ph * ph, Math.sin(a) * (0.05 + out)); });
    };
    g.userData.update(0); g.userData.grip = [0, -0.01, 0]; return g;
  },

  // Drips running off a soaked trouser hem (attach to a foot joint): o.n (6) drops forming at the hem and falling o.fall (0.1 m to the ground,
  // pivot height) every 0.3 s or so, and a darker wet band round the lower leg (o.sleeve [r, h]: radius and height above the pivot, o.color)
  legDrips(o) {
    const g = grp(), n = o.n ?? 6, drops = [];
    if (o.sleeve) { const [rr, hh] = o.sleeve, s = new THREE.Mesh(new THREE.CylinderGeometry(rr, rr * 1.06, hh, 12, 1, true), new THREE.MeshPhongMaterial({ color: o.color || '#070B13', transparent: true, opacity: o.opacity ?? 0.8, side: THREE.DoubleSide, shininess: 60, specular: new THREE.Color('#5A6A80') })); s.position.y = hh / 2 + (o.sleeveY ?? 0.05); g.add(s);
      const edge = new THREE.Mesh(new THREE.TorusGeometry(rr * 1.02, 0.008, 4, 16), basic('#3E5A7A')); edge.rotation.x = PI / 2; edge.position.y = hh + (o.sleeveY ?? 0.05); g.add(edge); }
    for (let i = 0; i < n; i++) { const d = new THREE.Mesh(new THREE.SphereGeometry(0.014, 6, 4), basic('#9FD8FF')); d.scale.y = 1.5; g.add(d); drops.push(d); }
    g.userData.update = t => { drops.forEach((d, i) => { const a = (i / n) * TAU, ph = (t * (1.6 + 0.5 * hsh(i)) + hsh(i + 3)) % 1, y = ph < 0.4 ? 0 : -(ph - 0.4) * (ph - 0.4) * 4 * (o.fall ?? 0.12) * 2.8;
      d.position.set(Math.cos(a) * (o.r ?? 0.08), (o.y0 ?? 0.08) + y, Math.sin(a) * (o.r ?? 0.08)); d.scale.setScalar(ph < 0.4 ? 0.5 + ph * 1.2 : 1); d.scale.y = 1.4; }); };
    g.userData.update(0); return g;
  },

  // (round 2) A soaked trouser leg (attach to a knee joint: on={'actor': ..., 'joint': 'kneeL'}): a darker, glossy skin drawn ON the shin itself, not a
  // separate sleeve (the black cylinder read as a bin, then as a wellington boot). On its first update it finds the shin mesh beside it on the knee
  // joint and lays a translucent dark copy over it that shares its geometry (so it bends and stretches with the cartoon leg), cut off above o.h (the
  // wet part's share of the shin from the hem, 0.55) by a shader test on the shin's own height; o.color, o.opacity (0.5)
  wetShin(o) {
    const g = grp(); let over = null, shin = null, tries = 0;
    const mk = () => {
      if (!g.parent) return; tries++; const isLeg = c => c.isMesh && c.name !== 'outline' && c !== over && c.geometry?.attributes?.position;
      // buildProp wraps the prop in a group of its own: the knee joint is the first ancestor that holds a leg mesh
      for (let a = g.parent, n = 0; a && n < 4 && !shin; a = a.parent, n++) shin = a.children.find(isLeg) || null; if (!shin) return;
      shin.geometry.computeBoundingBox(); const bb = shin.geometry.boundingBox, cut = bb.min.y + (bb.max.y - bb.min.y) * (o.h ?? 0.55);
      const m = new THREE.MeshPhongMaterial({ color: o.color || '#03060C', transparent: true, opacity: o.opacity ?? 0.5, shininess: 90, specular: new THREE.Color('#8FA4C0'), depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });
      m.onBeforeCompile = sh => { sh.uniforms.uCut = { value: cut };
        sh.vertexShader = 'varying float vLY;\n' + sh.vertexShader.replace('#include <begin_vertex>', '#include <begin_vertex>\nvLY = position.y;');
        sh.fragmentShader = 'uniform float uCut;\nvarying float vLY;\n' + sh.fragmentShader.replace('void main() {', 'void main() {\nif (vLY > uCut) discard;'); };
      over = new THREE.Mesh(shin.geometry, m); over.castShadow = false; over.receiveShadow = false; over.renderOrder = 2; g.add(over);
    };
    // the overlay is placed from the shin's world matrix (the engine scales an attached prop by 1 / the actor's scale: a copy of the shin's local
    // transform under this group came out smaller than the shin, inside it, and never showed)
    const Mi = new THREE.Matrix4(), Ms = new THREE.Matrix4().makeScale(1.04, 1.0, 1.04);
    g.userData.update = () => { if (!over && tries < 5) mk(); if (!over || !shin) return; g.updateWorldMatrix(true, false); shin.updateWorldMatrix(true, false);
      over.matrixAutoUpdate = false; over.matrix.copy(Mi.copy(g.matrixWorld).invert()).multiply(shin.matrixWorld).multiply(Ms); over.matrixWorldNeedsUpdate = true; };
    return g;
  },

  // (round 3) A big old telephone handset (attach to a hand, held like the smartphone: long axis Y, the cups toward +Z, the face): a bright red bar
  // o.len (0.3 m) bowed in the middle, an earpiece cup at the top and a mouthpiece cup at the bottom, white highlights (the small black smartphone
  // did not show: the pose read as scratching his head); o.color; o.rot [x, y, z] turns it in the hand
  handset(o) {
    const Lh = o.len ?? 0.3, C = o.color || '#D8262C', g = grp(), H = grp(); g.add(H);
    H.add(at(box(0.055, Lh * 0.62, 0.045, C, { outline: 0.006 }), 0, 0, -0.02));
    for (const sd of [-1, 1]) { const cup = cyl(0.058, 0.05, 0.06, C, 16, { outline: 0.006 }); cup.rotation.x = PI / 2; cup.position.set(0, sd * Lh * 0.38, 0.012); H.add(cup);
      const face = new THREE.Mesh(new THREE.CircleGeometry(0.044, 16), basic('#2A1416')); face.position.set(0, sd * Lh * 0.38, 0.043); H.add(face);
      for (let k = 0; k < 4; k++) { const hole = new THREE.Mesh(new THREE.CircleGeometry(0.006, 6), basic('#F2E8E0')); hole.position.set(Math.cos(k * PI / 2) * 0.018, sd * Lh * 0.38 + Math.sin(k * PI / 2) * 0.018, 0.045); H.add(hole); } }
    H.add(at(box(0.012, Lh * 0.5, 0.004, '#FFB3AE'), -0.018, 0, 0.003));
    const rt = o.rot || [0, 0, 0]; H.rotation.set(rt[0], rt[1], rt[2]); g.userData.grip = [0, 0, 0]; return g;
  },

  // (round 3) A big lit parking ticket (pivot at its middle, front +Z): a white card o.w (0.6) × 1.3 o.w with a red band, AVIS DE CONTRAVENTION and a
  // barcode, slightly emissive so it reads in the shade of a door; o.flat true: lying flat (front up)
  bigTicket(o) {
    const w = o.w ?? 0.6, h = w * 1.3, g = grp();
    const card = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.fillStyle = '#C8202A'; c.fillRect(0, 0, W, H * 0.18); c.fillStyle = '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle';
      c.font = `900 ${Math.round(H * 0.09)}px Arial`; c.fillText('AMENDE', W / 2, H * 0.095); c.fillStyle = '#1E2126'; c.font = `900 ${Math.round(H * 0.055)}px Arial`; c.fillText('AVIS DE', W / 2, H * 0.3); c.fillText('CONTRAVENTION', W / 2, H * 0.38);
      c.fillStyle = '#9AA0A6'; for (let i = 0; i < 4; i++) c.fillRect(W * 0.12, H * (0.5 + i * 0.07), W * (0.76 - (i % 2) * 0.2), H * 0.025);
      c.fillStyle = '#1E2126'; for (let i = 0; i < 26; i++) if (i % 3 !== 1) c.fillRect(W * (0.14 + i * 0.028), H * 0.82, W * (i % 4 ? 0.012 : 0.02), H * 0.1); }, { res: 256, emissive: 0.75 });
    card.material.side = THREE.DoubleSide; if (o.flat) card.rotation.x = -PI / 2; g.add(card); g.userData.grip = [0, -h * 0.4, 0]; return g;
  },

  // (round 3) A small harbour boat bobbing on the water (pivot at the waterline, bow +X): a white hull with a red stripe, a little blue wheelhouse,
  // a mast with a pennant; o.s scale
  harbourBoat(o) {
    const g = grp(), B = grp(); g.add(B);
    B.add(at(box(3.2, 0.7, 1.2, '#F4F1EA', { taper: { x: 0.8, z: 0.75 }, outline: 0.01 }), 0, 0.1, 0), at(box(3.25, 0.12, 1.22, '#C8322A'), 0, 0.38, 0), at(box(1.1, 0.75, 0.9, '#2F5E8C', { pivot: 'bottom', outline: 0.01 }), -0.4, 0.45, 0),
      at(box(0.9, 0.3, 0.92, '#BFE3F5'), -0.4, 0.95, 0), at(cyl(0.04, 0.04, 2.2, '#3A3F45', 6, { pivot: 'bottom' }), 0.6, 0.45, 0), at(box(0.5, 0.25, 0.02, '#E9C46A'), 0.85, 2.45, 0));
    B.scale.setScalar(o.s ?? 1);
    g.userData.update = t => { B.position.y = 0.06 * Math.sin(t * 2.1); B.rotation.z = 0.04 * Math.sin(t * 1.7); B.rotation.x = 0.03 * Math.sin(t * 1.3 + 1); };
    g.userData.update(0); return g;
  },

  // (round 3) Soft see-through dust drifting across the ground (pivot where it starts): o.n (5) round sprites with a soft edge (the toon puffs read as
  // beige eggs), o.size (1.2 m), o.color, o.opacity (0.35), o.life (s per puff, they loop), o.drift [x, z] (m/s), o.spread (m)
  softDust(o) {
    const g = grp(), n = o.n ?? 5, tex = (() => { const c = document.createElement('canvas'); c.width = c.height = 64; const x = c.getContext('2d'), gr = x.createRadialGradient(32, 32, 2, 32, 32, 31);
      gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.5, 'rgba(255,255,255,0.55)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = gr; x.fillRect(0, 0, 64, 64); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
    const sp = []; for (let i = 0; i < n; i++) { const m = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, color: o.color || '#E2D2B4', transparent: true, opacity: 0, depthWrite: false })); g.add(m); sp.push(m); }
    const L = o.life ?? 2.2, [dx, dz] = o.drift || [1.5, 0], S = o.size ?? 1.2, SP = o.spread ?? 2.5;
    g.userData.update = t => { sp.forEach((m, i) => { const ph = ((t + hsh(i) * L) % L) / L; m.position.set(dx * ph * L + (hsh(i + 2) - 0.5) * SP, 0.25 + 0.5 * ph + 0.3 * hsh(i + 4), dz * ph * L + (hsh(i + 6) - 0.5) * SP);
      m.scale.setScalar(S * (0.6 + 0.8 * ph)); m.material.opacity = (o.opacity ?? 0.35) * Math.sin(ph * PI); }); };
    g.userData.update(0); return g;
  },
};
