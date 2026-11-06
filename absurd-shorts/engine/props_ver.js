// Props for « Le ver de terre » (story 35): the lawn, the mower's clippings, the earthworm's dirt, the avocado lawyer's salads.
// Conventions as in props.js (metres, front +Z, pivot at the floor); every motion is a pure function of t.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, sphere, rng, ease, clamp01 } from './style.js';
import { grp, at, mesh, canvasPlane, inst, rod, torus, buildProp } from './props.js';

const PI = Math.PI, TAU = PI * 2;
const DIRT = ['#6B4A2E', '#5A3C24', '#7A5636', '#4E3420'];
const LEAF = ['#7CC25A', '#5FA845', '#93D06A', '#6DB84E'];
let _leafTex = null;
function leafTexture() {   // a ruffled lettuce leaf, pale rib, darker edge (transparent around)
  if (_leafTex) return _leafTex;
  const c = document.createElement('canvas'); c.width = 128; c.height = 128; const g = c.getContext('2d');
  g.translate(64, 64); g.beginPath(); for (let i = 0; i <= 40; i++) { const a = i / 40 * TAU, r = 52 + 7 * Math.sin(a * 9) + 4 * Math.sin(a * 23); const x = Math.cos(a) * r * 0.78, y = Math.sin(a) * r; i ? g.lineTo(x, y) : g.moveTo(x, y); } g.closePath();
  g.fillStyle = '#86C95E'; g.fill(); g.lineWidth = 6; g.strokeStyle = '#4E9A3A'; g.stroke();
  g.strokeStyle = '#D9F0B8'; g.lineWidth = 5; g.beginPath(); g.moveTo(0, 50); g.lineTo(0, -40); g.stroke(); g.lineWidth = 3; for (let k = -2; k <= 2; k++) { g.beginPath(); g.moveTo(0, k * 16); g.lineTo(26, k * 16 - 14); g.moveTo(0, k * 16); g.lineTo(-26, k * 16 - 14); g.stroke(); }
  _leafTex = new THREE.CanvasTexture(c); _leafTex.colorSpace = THREE.SRGBColorSpace; return _leafTex;
}

export const VER_PROPS = {
  mowedLawn(o) {   // a lawn o.w × o.d (x across, z along the mowing direction): mowed stripes up to z = o.cut (light / dark bands), tall grass beyond it
    const w = o.w || 8, d = o.d || 10, cut = o.cut ?? 0, n = o.stripes || 8, g = grp();
    for (let i = 0; i < n; i++) { const m = mesh(new THREE.PlaneGeometry(w / n, cut + d / 2).rotateX(-PI / 2), mat(i % 2 ? '#7DBA55' : '#6AA845', { noGrain: false })); m.position.set(-w / 2 + (i + 0.5) * w / n, 0.006, (cut - d / 2) / 2); g.add(m); }
    g.add(buildProp('tallGrass', { w, d: d / 2 - cut, h: o.h || 0.16, count: o.count || 900, thin: 0.012, cols: ['#5E9A4A', '#6FB05A', '#4E8A3E', '#7FBF5E'] }));
    g.children.at(-1).position.set(0, 0, cut + (d / 2 - cut) / 2 - 0.0);
    return g;
  },
  mowerRun(o) {   // the push mower with grass clippings spraying out of its side chute while it runs (o.runAt .. o.stopAt)
    const g = grp(buildProp('lawnmower', { runAt: o.runAt ?? 0, stopAt: o.stopAt })), r = rng(o.seed || 5), N = 70;
    const clip = new THREE.InstancedMesh(new THREE.BoxGeometry(0.045, 0.01, 0.022), mat('#6DBE4E'), N), d = new THREE.Object3D(), base = [];
    for (let i = 0; i < N; i++) base.push([r(), r() * TAU, 0.6 + r() * 0.8, (r() - 0.5) * 0.6]); clip.frustumCulled = false; g.add(clip);
    g.userData.update = t => { g.children[0].userData.update?.(t); const on = t >= (o.runAt ?? 0) && (o.stopAt == null || t < o.stopAt);
      base.forEach(([ph, rot, v, sp], i) => { const q = ((t * 1.6) + ph) % 1; if (!on) { d.scale.setScalar(0.0001); } else { d.scale.setScalar(1); d.position.set(0.3 + q * v * 0.9, 0.22 + q * 0.95 - q * q * 1.1, sp * q * 0.9); d.rotation.set(t * 9 + rot, rot, t * 7); } d.updateMatrix(); clip.setMatrixAt(i, d.matrix); });
      clip.instanceMatrix.needsUpdate = true; };
    g.userData.update(0); return g;
  },
  dirtBurst(o) {   // clods of earth thrown up at o.popAt (the earthworm coming out), falling back
    const r = rng(o.seed || 9), N = o.n || 18, g = grp(), clods = [];
    for (let i = 0; i < N; i++) { const m = sphere(0.018 + r() * 0.02, DIRT[i % 4], 0); const a = r() * TAU, sp = 0.4 + r() * 0.9; clods.push({ m, vx: Math.cos(a) * sp * 0.6, vz: Math.sin(a) * sp * 0.6, vy: 1.4 + r() * 1.4 }); g.add(m); }
    g.userData.update = t => { const u = t - (o.popAt ?? 0); clods.forEach(c => { if (u < 0) { c.m.visible = false; return; } const y = c.vy * u - 4.9 * u * u; c.m.visible = y > -0.02 || u < 0.1; c.m.position.set(c.vx * u, Math.max(0.01, y), c.vz * u); c.m.rotation.set(u * 9, u * 7, 0); }); };
    g.userData.update(0); return g;
  },
  dirtMound(o) {   // a little ring of turned earth round a hole (the earthworm's door)
    const r = rng(o.seed || 3), g = grp(at(mesh(new THREE.CircleGeometry((o.r || 0.11) * 0.8, 10).rotateX(-PI / 2), mat('#2A1E14')), 0, 0.008, 0));
    for (let i = 0; i < 12; i++) { const a = i / 12 * TAU + r() * 0.3, m = sphere(0.035 + r() * 0.02, DIRT[i % 4], 0); m.scale.set(1, 0.55, 1); m.position.set(Math.cos(a) * (o.r || 0.11), 0.012, Math.sin(a) * (o.r || 0.11)); g.add(m); }
    return g;
  },
  flowerPot(o) {   // a terracotta pot full of soil (the earthworm comes to court in its own earth)
    const R = o.r || 0.16, H = o.h || 0.26, g = grp(cyl(R, R * 0.78, H, '#C9683A', 12, { pivot: 'bottom' }), at(cyl(R * 1.08, R * 1.08, 0.05, '#B85A30', 12), 0, H - 0.02, 0), at(cyl(R * 0.96, R * 0.96, 0.012, '#3A2818', 12), 0, H - 0.006, 0));
    g.children[0].add(at(box(0.001, 0.001, 0.001, '#000000'), 0, 0, 0)); g.userData.top = [0, H, 0]; return g;
  },
  saladLeaves(o) {   // lettuce leaves flying out of a mouth toward +Z (« raconter des salades »): o.n leaves cycling between o.onAt and o.offAt
    const n = o.n || 10, r = rng(o.seed || 13), g = grp(), leaves = [], m = new THREE.MeshLambertMaterial({ map: leafTexture(), transparent: true, alphaTest: 0.3, side: THREE.DoubleSide });
    for (let i = 0; i < n; i++) { const L = new THREE.Mesh(new THREE.PlaneGeometry(0.09, 0.11), m); L.userData.noAO = true; g.add(L); leaves.push({ L, ph: i / n, sx: (r() - 0.5) * 0.9, sy: 0.25 + r() * 0.5, sp: 0.7 + r() * 0.5, rot: r() * TAU }); }
    g.userData.update = t => { const a0 = o.onAt ?? 0, a1 = o.offAt ?? 1e9;
      leaves.forEach(l => { const age = ((t - a0) * 0.9 + l.ph) % 1.0, born = t - a0 - (l.ph / 0.9) >= 0 && t - age / 0.9 < a1; l.L.visible = t >= a0 && born && (t < a1 + 1.1);
        const u = age * 1.1; l.L.position.set(l.sx * u * 0.55, l.sy * u - 0.55 * u * u, l.sp * u * 0.65); l.L.rotation.set(l.rot + u * 5, u * 3 + l.rot, Math.sin(u * 7 + l.rot) * 0.6); l.L.scale.setScalar(0.6 + Math.min(1, u * 3) * 0.6); }); };
    g.userData.update(0); return g;
  },
  saladBubble(o) {   // a comic speech bubble with salad in it instead of words (lettuce leaves, tomato and cucumber slices), pops at o.popAt
    const w = o.w || 0.5, h = o.h || 0.32, pl = canvasPlane(w, h * 1.35, (c, W, H) => { const bh = H / 1.35, rad = bh * 0.42; c.clearRect(0, 0, W, H); c.fillStyle = '#FFFFFF'; c.strokeStyle = '#1C252A'; c.lineWidth = bh * 0.05;
      c.beginPath(); c.moveTo(rad, 4); c.arcTo(W - 4, 4, W - 4, bh, rad); c.arcTo(W - 4, bh, 4, bh, rad); c.arcTo(4, bh, 4, 4, rad); c.arcTo(4, 4, W - 4, 4, rad); c.closePath(); c.fill(); c.stroke();
      const tx = o.tail === 'right' ? W * 0.72 : W * 0.28; c.beginPath(); c.moveTo(tx - W * 0.06, bh - 2); c.lineTo(tx + (o.tail === 'right' ? W * 0.1 : -W * 0.1), H - 4); c.lineTo(tx + W * 0.06, bh - 2); c.closePath(); c.fill(); c.stroke(); c.fillStyle = '#FFFFFF'; c.fillRect(tx - W * 0.055, bh - bh * 0.06, W * 0.11, bh * 0.08);
      const leaf = (x, y, s, a) => { c.save(); c.translate(x, y); c.rotate(a); c.beginPath(); c.ellipse(0, 0, s, s * 0.62, 0, 0, TAU); c.fillStyle = '#7CC25A'; c.fill(); c.lineWidth = s * 0.12; c.strokeStyle = '#4E9A3A'; c.stroke(); c.strokeStyle = '#D9F0B8'; c.lineWidth = s * 0.08; c.beginPath(); c.moveTo(-s * 0.8, 0); c.lineTo(s * 0.8, 0); c.stroke(); c.restore(); };
      const tom = (x, y, s) => { c.fillStyle = '#E0413A'; c.beginPath(); c.arc(x, y, s, 0, TAU); c.fill(); c.fillStyle = '#F7B0A0'; for (let k = 0; k < 6; k++) { const a = k / 6 * TAU; c.beginPath(); c.ellipse(x + Math.cos(a) * s * 0.5, y + Math.sin(a) * s * 0.5, s * 0.18, s * 0.28, a, 0, TAU); c.fill(); } };
      const cuc = (x, y, s) => { c.fillStyle = '#3E7A2E'; c.beginPath(); c.arc(x, y, s, 0, TAU); c.fill(); c.fillStyle = '#CDE8A0'; c.beginPath(); c.arc(x, y, s * 0.8, 0, TAU); c.fill(); c.fillStyle = '#F2F6D8'; for (let k = 0; k < 5; k++) { const a = k / 5 * TAU; c.beginPath(); c.arc(x + Math.cos(a) * s * 0.4, y + Math.sin(a) * s * 0.4, s * 0.1, 0, TAU); c.fill(); } };
      leaf(W * 0.24, bh * 0.45, bh * 0.22, -0.4); leaf(W * 0.5, bh * 0.38, bh * 0.25, 0.3); leaf(W * 0.76, bh * 0.5, bh * 0.21, -0.2); tom(W * 0.38, bh * 0.62, bh * 0.13); cuc(W * 0.63, bh * 0.66, bh * 0.12); tom(W * 0.85, bh * 0.3, bh * 0.08);
    }, { res: 512, transparent: true });
    const g = grp(pl); pl.userData.noAO = true;
    g.userData.update = t => { const k = o.popAt == null ? 1 : t < o.popAt ? 0 : Math.max(0.001, ease.outBack(clamp01((t - o.popAt) / 0.3))); g.visible = k > 0.001; g.scale.setScalar(Math.max(0.001, k)); };
    g.userData.update(0); return g;
  },
  avocadoStone(o) {   // the avocado's stone, spat out at o.spitAt from (0,0,0) toward o.to [x, z], bouncing twice on y = 0 (the table top)
    const s = sphere(o.r || 0.06, '#7A4A2A', 2); s.scale.set(1, 1.08, 1); const g = grp(s); s.add(at(sphere((o.r || 0.06) * 0.3, '#B07A52', 0), -(o.r || 0.06) * 0.35, (o.r || 0.06) * 0.45, (o.r || 0.06) * 0.6));
    const to = o.to || [0.4, 0.5], h0 = o.h0 ?? 0.35;
    if (o.still) return g;   // moved by keys instead
    g.userData.update = t => { const u = t - (o.spitAt ?? 0); if (u < 0) { s.visible = false; return; } s.visible = true;
      const T = [0.42, 0.3, 0.18], hs = [h0, 0.12, 0.04]; let tt = u, seg = 0, x0 = 0; const total = T.reduce((a, b) => a + b, 0), fx = Math.min(1, u / total);
      while (seg < 3 && tt > T[seg]) { tt -= T[seg]; seg++; } let y = 0; if (seg < 3) { const q = tt / T[seg]; y = seg === 0 ? h0 * (1 - q) + 4 * hs[0] * 0.6 * q * (1 - q) : 4 * hs[seg] * q * (1 - q); }
      s.position.set(to[0] * ease.out(fx), (o.r || 0.06) + Math.max(0, y), to[1] * ease.out(fx)); s.rotation.set(u * 12 * (1 - fx), 0, -u * 9 * (1 - fx)); void x0; };
    g.userData.update(0); return g;
  },
  policeFlash(o) {   // the light bar's glow sweeping a scene: a blue and a red point light alternating (o.rate Hz), place it behind the camera
    const b = new THREE.PointLight('#3C7BFF', 0, o.dist || 14, 1.4), r = new THREE.PointLight('#FF3A3A', 0, o.dist || 14, 1.4); b.position.x = -0.4; r.position.x = 0.4; const g = grp(b, r);
    g.userData.update = t => { const ph = (t * (o.rate || 3.2)) % 1, k = o.power ?? 9; b.intensity = ph < 0.5 ? k * Math.sin(ph * 2 * PI) ** 2 : 0; r.intensity = ph >= 0.5 ? k * Math.sin((ph - 0.5) * 2 * PI) ** 2 : 0; };
    g.userData.update(0); return g;
  },
  mugshotPlate(o) {   // the black letter board a suspect holds for the mugshot (o.lines)
    const L = o.lines || ['LE MEC', 'N° 0042'], w = o.w || 0.42, h = o.h || 0.24;
    return grp(at(box(w + 0.02, h + 0.02, 0.012, '#5A4A3A'), 0, 0, -0.009), canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#17181C'; c.fillRect(0, 0, W, H); c.fillStyle = '#F4F1EA'; c.textAlign = 'center'; c.textBaseline = 'middle';
      L.forEach((l, i) => { let px = H * 0.26; c.font = `700 ${px}px monospace`; const tw = c.measureText(l).width; if (tw > W * 0.9) { px *= W * 0.9 / tw; c.font = `700 ${px}px monospace`; } c.fillText(l, W / 2, H * (0.3 + i * 0.4)); }); }, { res: 256 }));
  },
};
