// « Le rayon » (story 90): this man had the sun in his eyes; the space agency gathered three hundred scientists; chosen solution: a parasol in
// space; twelve rockets took off from his garden; his tomatoes orbit the Earth; the parasol is the size of the country; opening, it mowed down
// three satellites; the whole country went grey; the sunflowers hung their heads; the solar panels were laid off; the agency declared the mission
// a success; the country marched with torches; the gendarmes handcuffed the torches; a tank shot a hole in the parasol; just one; above his
// garden; right in his eyes; the whole country picnics at his place; he had a parasol in the garage.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere, addOutline, mat, rng } from './style.js';
import { grp, at, canvasPlane, buildProp, rod, glowSprite, cloudMat, sphereGeo } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = x => { const u = clamp01(x), c = 1.70158; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const easeOut = x => { const u = clamp01(x); return 1 - (1 - u) * (1 - u); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const noShadow = m => { m.traverse(c => { c.castShadow = false; }); return m; };
const INK = '#1B1B1E', SKIN = '#F2C9A0', HAIR = '#3A2A20', RED = '#D2382E', CREAM = '#F4EEDF';
// a soft additive plane (light shafts, glows on the ground) without a texture: a radial or vertical gradient canvas
function softTex(kind) {
  const cv = document.createElement('canvas'); cv.width = cv.height = 128; const c = cv.getContext('2d');
  const gr = kind === 'radial' ? c.createRadialGradient(64, 64, 0, 64, 64, 64) : c.createLinearGradient(0, 0, 128, 0);
  if (kind === 'radial') { gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.6, 'rgba(255,255,255,0.55)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); }
  else { gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(0.3, 'rgba(255,255,255,0.8)'); gr.addColorStop(0.5, 'rgba(255,255,255,1)'); gr.addColorStop(0.7, 'rgba(255,255,255,0.8)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); }
  c.fillStyle = gr; c.fillRect(0, 0, 128, 128); const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t;
}
const addMat = (color, opacity, map) => new THREE.MeshBasicMaterial({ color, map: map || null, transparent: true, opacity, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, fog: false });
// his squinting face, as a photo (the agency's screens, the press screen): a box head under a blazing sun, eyes screwed shut, a hand for a visor
function drawSquint(c, W, H, o = {}) {
  c.fillStyle = o.bg || '#8EC8EE'; c.fillRect(0, 0, W, H);
  c.fillStyle = '#FFD23A'; c.beginPath(); c.arc(W * 0.86, H * 0.16, H * 0.11, 0, TAU); c.fill();
  c.strokeStyle = '#FFC23A'; c.lineWidth = H * 0.025; for (let i = 0; i < 10; i++) { const a = i * TAU / 10; c.beginPath(); c.moveTo(W * 0.86 + Math.cos(a) * H * 0.14, H * 0.16 + Math.sin(a) * H * 0.14); c.lineTo(W * 0.86 + Math.cos(a) * H * 0.2, H * 0.16 + Math.sin(a) * H * 0.2); c.stroke(); }
  c.fillStyle = '#7CB36A'; c.fillRect(0, H * 0.82, W, H * 0.18);
  const hx = W * 0.44, hy = H * 0.22, hw = W * 0.36, hh = H * 0.5;
  c.fillStyle = '#2B3A5C'; c.fillRect(hx - hw * 0.15, hy + hh, hw * 1.3, H);            // the suit
  c.fillStyle = '#F4F1E8'; c.beginPath(); c.moveTo(hx + hw * 0.32, hy + hh); c.lineTo(hx + hw * 0.5, H * 0.95); c.lineTo(hx + hw * 0.68, hy + hh); c.fill();
  c.fillStyle = SKIN; c.fillRect(hx, hy, hw, hh); c.strokeStyle = INK; c.lineWidth = H * 0.018; c.strokeRect(hx, hy, hw, hh);
  c.fillStyle = HAIR; c.fillRect(hx - 2, hy - H * 0.04, hw + 4, H * 0.1);
  c.strokeStyle = INK; c.lineWidth = H * 0.028; c.lineCap = 'round';
  for (const ex of [0.3, 0.7]) { c.beginPath(); c.moveTo(hx + hw * (ex - 0.13), hy + hh * 0.38); c.lineTo(hx + hw * ex, hy + hh * 0.46); c.lineTo(hx + hw * (ex - 0.13), hy + hh * 0.54); c.stroke(); }
  c.beginPath(); c.moveTo(hx + hw * 0.3, hy + hh * 0.78); c.lineTo(hx + hw * 0.4, hy + hh * 0.72); c.lineTo(hx + hw * 0.5, hy + hh * 0.8); c.lineTo(hx + hw * 0.6, hy + hh * 0.72); c.lineTo(hx + hw * 0.7, hy + hh * 0.78); c.stroke();   // the grimace
  c.fillStyle = SKIN; c.save(); c.translate(hx + hw * 0.72, hy + hh * 0.2); c.rotate(-0.25); c.fillRect(-hw * 0.05, -H * 0.04, hw * 0.62, H * 0.08); c.strokeRect(-hw * 0.05, -H * 0.04, hw * 0.62, H * 0.08); c.restore();   // the hand visor
  if (o.frame !== false) { c.strokeStyle = '#F4F1E8'; c.lineWidth = H * 0.03; c.strokeRect(H * 0.015, H * 0.015, W - H * 0.03, H * 0.97); }
}
// the made-up country (a blobby outline, an ochre interior) seen from above on a canvas
function drawCountry(c, cx, cy, s, fill, line) {
  c.beginPath(); for (let i = 0; i <= 24; i++) { const a = i * TAU / 24, rr = s * (0.78 + 0.22 * Math.sin(a * 3 + 1.3) * Math.cos(a * 2 - 0.4)); c.lineTo(cx + Math.cos(a) * rr * 1.15, cy + Math.sin(a) * rr * 0.9); } c.closePath();
  c.fillStyle = fill; c.fill(); c.strokeStyle = line; c.lineWidth = s * 0.05; c.stroke();
}

export const RAYON_PROPS = {
  // a desk monitor showing his squinting photo; o.w the screen width (0.56), o.desk: on a small desk; o.emit the screen glow
  squintScreen(o) {
    const w = o.w ?? 0.56, h = w * 0.66, g = grp();
    const scr = canvasPlane(w * 0.93, h * 0.88, (c, W, H) => drawSquint(c, W, H, { frame: false }), { res: 384, emissive: o.emit ?? 0.55 });
    const y = o.desk ? 0.76 + h / 2 + 0.16 : h / 2 + 0.16;
    g.add(at(box(w, h, 0.05, '#2A2A2E', { outline: 0.008 }), 0, y, 0), at(scr, 0, y, 0.027), at(box(0.06, 0.16, 0.05, '#2A2A2E', { pivot: 'bottom' }), 0, y - h / 2 - 0.16, -0.02));
    if (o.desk) g.add(at(box(o.deskW ?? 1.2, 0.05, 0.7, '#D8D2C4', { outline: 0.006 }), 0, 0.735, 0.1), at(box(0.05, 0.71, 0.6, '#9AA0A6', { pivot: 'bottom' }), -(o.deskW ?? 1.2) / 2 + 0.06, 0, 0.1),
      at(box(0.05, 0.71, 0.6, '#9AA0A6', { pivot: 'bottom' }), (o.deskW ?? 1.2) / 2 - 0.06, 0, 0.1), at(box(0.42, 0.02, 0.14, '#3A3D44'), 0, 0.77, 0.3));
    return g;
  },
  // the wall of the control room: one big screen of his squinting photo, a red banner over it, a row of small status screens under it
  squintWall(o) {
    const W = o.w ?? 4.4, H = W * 0.56, g = grp();
    const big = canvasPlane(W, H, (c, Wc, Hc) => drawSquint(c, Wc, Hc), { res: 768, emissive: o.emit ?? 0.6 });
    g.add(at(box(W + 0.16, H + 0.16, 0.08, '#24272D', { outline: 0.008 }), 0, 0, -0.05), at(big, 0, 0, 0.0));
    const ban = canvasPlane(W * 0.7, 0.32, (c, Wc, Hc) => { c.fillStyle = '#B5302A'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#F4F1E8'; c.font = `900 ${Hc * 0.62}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.banner || 'CIBLE PRIORITAIRE', Wc / 2, Hc * 0.55); }, { res: 512, emissive: 0.4 });
    g.add(at(ban, 0, H / 2 + 0.3, 0.02));
    return g;
  },
  // the whiteboard on its stand: the sun on the left, the Earth (a house and a tiny man) on the right, a red and white parasol between them, a
  // dotted line of the sun's rays stopping on it; o.title; o.ringAt: a red marker circle around the parasol drawn at that time
  diagramBoard(o) {
    const W = o.w ?? 2.4, H = W * 0.58, g = grp();
    const draw = (c, Wc, Hc, ring) => {
      c.fillStyle = '#FBFBF7'; c.fillRect(0, 0, Wc, Hc); c.lineCap = 'round'; c.lineJoin = 'round';
      c.fillStyle = '#1F3A78'; c.font = `900 ${Hc * 0.09}px Arial`; c.textAlign = 'center'; c.fillText(o.title || 'SOLUTION RETENUE', Wc / 2, Hc * 0.13);
      c.fillStyle = '#FFD23A'; c.strokeStyle = '#E09A1A'; c.lineWidth = Hc * 0.012; c.beginPath(); c.arc(Wc * 0.13, Hc * 0.55, Hc * 0.13, 0, TAU); c.fill(); c.stroke();
      for (let i = 0; i < 12; i++) { const a = i * TAU / 12; c.beginPath(); c.moveTo(Wc * 0.13 + Math.cos(a) * Hc * 0.16, Hc * 0.55 + Math.sin(a) * Hc * 0.16); c.lineTo(Wc * 0.13 + Math.cos(a) * Hc * 0.22, Hc * 0.55 + Math.sin(a) * Hc * 0.22); c.stroke(); }
      c.strokeStyle = '#E09A1A'; c.setLineDash([Hc * 0.03, Hc * 0.03]); c.lineWidth = Hc * 0.014;
      for (const dy of [-0.12, 0, 0.12]) { c.beginPath(); c.moveTo(Wc * 0.25, Hc * (0.55 + dy * 0.6)); c.lineTo(Wc * 0.46, Hc * (0.55 + dy)); c.stroke(); }
      c.setLineDash([]);
      // the parasol, canopy toward the sun
      const px = Wc * 0.5, py = Hc * 0.55; c.save(); c.translate(px, py); c.rotate(-PI / 2);
      for (let i = 0; i < 6; i++) { c.fillStyle = i % 2 ? '#F4F1E8' : RED; c.beginPath(); c.moveTo(0, 0); c.lineTo(-Hc * 0.3 + i * Hc * 0.1, -Hc * 0.13); c.lineTo(-Hc * 0.3 + (i + 1) * Hc * 0.1, -Hc * 0.13); c.closePath(); c.fill(); }
      c.strokeStyle = INK; c.lineWidth = Hc * 0.012; c.beginPath(); c.moveTo(-Hc * 0.3, -Hc * 0.13); c.quadraticCurveTo(0, -Hc * 0.24, Hc * 0.3, -Hc * 0.13); c.lineTo(0, 0); c.closePath(); c.stroke();
      c.beginPath(); c.moveTo(0, -Hc * 0.05); c.lineTo(0, Hc * 0.2); c.stroke(); c.restore();
      // the Earth, a house on it and a tiny man with his hand over his eyes
      c.fillStyle = '#3E8FD0'; c.beginPath(); c.arc(Wc * 0.84, Hc * 0.62, Hc * 0.2, 0, TAU); c.fill(); c.strokeStyle = INK; c.lineWidth = Hc * 0.012; c.stroke();
      c.fillStyle = '#7DC46A'; c.beginPath(); c.ellipse(Wc * 0.8, Hc * 0.58, Hc * 0.08, Hc * 0.06, 0.4, 0, TAU); c.fill(); c.beginPath(); c.ellipse(Wc * 0.9, Hc * 0.7, Hc * 0.05, Hc * 0.07, -0.3, 0, TAU); c.fill();
      c.fillStyle = '#F4F1E8'; c.fillRect(Wc * 0.78, Hc * 0.33, Hc * 0.08, Hc * 0.07); c.fillStyle = RED; c.beginPath(); c.moveTo(Wc * 0.775, Hc * 0.335); c.lineTo(Wc * 0.78 + Hc * 0.04, Hc * 0.29); c.lineTo(Wc * 0.785 + Hc * 0.08, Hc * 0.335); c.fill();
      c.strokeStyle = INK; c.lineWidth = Hc * 0.01; c.beginPath(); c.moveTo(Wc * 0.86, Hc * 0.4); c.lineTo(Wc * 0.86, Hc * 0.35); c.moveTo(Wc * 0.86, Hc * 0.4); c.lineTo(Wc * 0.85, Hc * 0.42); c.moveTo(Wc * 0.86, Hc * 0.4); c.lineTo(Wc * 0.87, Hc * 0.42); c.stroke();
      c.beginPath(); c.arc(Wc * 0.86, Hc * 0.33, Hc * 0.016, 0, TAU); c.stroke();
      c.fillStyle = '#1F3A78'; c.font = `900 ${Hc * 0.06}px Arial`; c.fillText('SOLEIL', Wc * 0.13, Hc * 0.86); c.fillText('LUI', Wc * 0.92, Hc * 0.3); c.fillText('PARASOL', Wc * 0.5, Hc * 0.86);
      c.strokeStyle = '#1F3A78'; c.lineWidth = Hc * 0.01; c.beginPath(); c.moveTo(Wc * 0.905, Hc * 0.31); c.lineTo(Wc * 0.875, Hc * 0.33); c.stroke();
      if (ring) { c.strokeStyle = '#D2382E'; c.lineWidth = Hc * 0.022; c.beginPath(); c.ellipse(px, py, Hc * 0.2, Hc * 0.36, 0.05, 0, TAU); c.stroke(); }
    };
    const a = canvasPlane(W, H, (c, Wc, Hc) => draw(c, Wc, Hc, false), { res: 1024 }), b = canvasPlane(W, H, (c, Wc, Hc) => draw(c, Wc, Hc, true), { res: 1024 });
    const yb = o.y ?? 1.55; b.visible = false; g.add(at(a, 0, yb, 0.03), at(b, 0, yb, 0.031));
    g.add(at(box(W + 0.1, H + 0.1, 0.05, '#B9BEC4', { outline: 0.008 }), 0, yb, 0), at(box(W * 0.6, 0.05, 0.12, '#B9BEC4'), 0, yb - H / 2 - 0.05, 0.06));
    for (const s of [-1, 1]) g.add(at(box(0.05, yb + H / 2, 0.05, '#7E858C', { pivot: 'bottom' }), s * (W / 2 - 0.15), 0, -0.04), at(box(0.06, 0.05, 0.7, '#7E858C', { pivot: 'bottom' }), s * (W / 2 - 0.15), 0, -0.04));
    if (o.ringAt != null) g.userData.update = t => { b.visible = t >= o.ringAt; a.visible = !b.visible; };
    return g;
  },
  // o.n rockets (props.js rocket, flame on) standing on the lawn at o.spots [[x, z], ...] (a 4 x 3 grid by default), scale o.s; rocket i lifts off at
  // o.t0 + o.order[i] * o.gap and climbs with acceleration o.acc; a puff of smoke swells at its foot and a scorch is left on the grass; (round 1)
  // o.clear [x0, x1]: no puff spreads into that strip of x (the garden path, kept clear for a close camera on the doorway)
  rocketLawn(o) {
    const g = grp(), s = o.s ?? 0.6, n = o.n ?? 12, acc = o.acc ?? 14, t0 = o.t0 ?? 0.3, gap = o.gap ?? 0.07;
    const spots = o.spots || Array.from({ length: n }, (_, i) => [((i % 4) - 1.5) * 1.6, -Math.floor(i / 4) * 1.6]);
    const order = o.order || spots.map((_, i) => [3, 7, 0, 10, 5, 1, 9, 4, 11, 2, 8, 6][i % 12]);
    const items = spots.map(([x, z], i) => {
      const rk = buildProp('rocket', { flame: true }); rk.scale.setScalar(s); rk.position.set(x, 0, z); rk.rotation.y = hsh(i + 3) * TAU;
      const sc = at(new THREE.Mesh(new THREE.CircleGeometry(0.75 * s * 1.6, 14).rotateX(-PI / 2), mat('#4A4A3A')), x, 0.012, z); sc.receiveShadow = true; sc.visible = false;
      const puffs = []; for (let j = 0; j < 6; j++) { const m = new THREE.Mesh(sphereGeo(2), cloudMat('#F2F0EA', '#B9C2CE')); m.scale.setScalar(0.4 * s * 1.6); m.userData.r0 = 0.4 * s * 1.6; m.castShadow = false; const a = j / 6 * TAU + i; puffs.push({ m, dx: Math.cos(a), dz: Math.sin(a) }); g.add(m); }
      g.add(rk, sc); return { rk, sc, puffs, x, z, tl: t0 + order[i] * gap };
    });
    g.userData.update = t => {
      for (const it of items) {
        const u = t - it.tl, up = u > 0 ? 0.5 * acc * u * u : 0; it.rk.position.y = up; it.rk.visible = up < (o.ceiling ?? 60);
        it.rk.rotation.z = u > 0 ? 0.04 * Math.sin(u * 30 + it.x) * Math.min(1, u * 3) : 0;
        it.rk.traverse(c => { if (c.userData.update && c !== it.rk) c.userData.update(t); }); if (it.rk.userData.update) it.rk.userData.update(t);
        it.rk.children.forEach(c => { if (c.isGroup && c.position.y === 0.2) c.visible = u > -0.15; });   // the flame lights just before lift-off
        it.sc.visible = u > 0.05;
        it.puffs.forEach((p, j) => { const v = clamp01((u + 0.1) / 1.4), r = 0.3 + 1.6 * easeOut(v); p.m.visible = u > -0.1; let px = it.x + p.dx * r * s * 1.4; if (o.clear && px > o.clear[0] && px < o.clear[1]) px = it.x < (o.clear[0] + o.clear[1]) / 2 ? o.clear[0] : o.clear[1]; p.m.position.set(px, 0.25 * s + 0.35 * v * (1 + (j % 2)), it.z + p.dz * r * s * 1.4); p.m.scale.setScalar(p.m.userData.r0 * (0.4 + 1.3 * easeOut(v))); });   // (stills 1) soft cloud puffs: faceted spheres read as white boulders
      }
    };
    g.userData.update(-1); return g;
  },
  // his vegetable patch in orbit: three tomato stakes with their plants and string, loose tomatoes, a watering can, slowly tumbling (o.spin)
  orbitTomatoes(o) {
    const g = grp(), r = rng(o.seed || 9), parts = [];
    const tomato = sz => { const t = grp(sphere(sz, '#D8352A', 1, { outline: 0.01 })); t.children[0].scale.y = 0.85; for (let k = 0; k < 5; k++) t.add(at(box(sz * 0.18, sz * 0.05, sz * 0.7, '#3E7A3A'), 0, sz * 0.82, 0, 0, k * TAU / 5, 0)); return t; };
    for (let i = 0; i < 3; i++) {
      const p = grp(at(cyl(0.025, 0.03, 1.5, '#A67C52', 6, { pivot: 'bottom' }), 0, -0.75, 0));
      for (let k = 0; k < 7; k++) { const y = -0.6 + k * 0.2, a = k * 2.1 + i; p.add(at(box(0.2, 0.03, 0.12, '#4E9A45', { outline: 0.004 }), Math.cos(a) * 0.12, y, Math.sin(a) * 0.12, 0, a, 0.3)); }
      for (let k = 0; k < 4; k++) { const tm = tomato(0.07 + r() * 0.03); tm.position.set((r() - 0.5) * 0.3, -0.4 + k * 0.25, (r() - 0.5) * 0.3); p.add(tm); }
      p.add(rod([0, 0.3, 0], [0.18, 0.1, 0.05], 0.006, '#E8DCC0'));
      p.position.set((i - 1) * 1.1, (r() - 0.5) * 0.6, (r() - 0.5) * 0.8); p.rotation.set(r() * 0.8, r() * TAU, (r() - 0.5) * 1.2); parts.push({ m: p, w: [r() - 0.5, r() - 0.5, r() - 0.5].map(v => v * 0.9) }); g.add(p);
    }
    for (let i = 0; i < (o.loose ?? 7); i++) { const tm = tomato(0.08 + r() * 0.04); tm.position.set((r() - 0.5) * 4, (r() - 0.5) * 2, (r() - 0.5) * 2); parts.push({ m: tm, w: [r() - 0.5, r() - 0.5, r() - 0.5].map(v => v * 2) }); g.add(tm); }
    const can = grp(at(cyl(0.14, 0.16, 0.26, '#2F8A6A', 10, { outline: 0.01 }), 0, 0, 0), rod([0.12, -0.05, 0], [0.38, 0.14, 0], 0.02, '#2F8A6A'), at(cyl(0.05, 0.03, 0.06, '#2F8A6A', 8), 0.4, 0.16, 0, 0, 0, -0.9));
    can.position.set(1.7, 0.7, 0.4); parts.push({ m: can, w: [0.4, 0.9, -0.3] }); g.add(can);
    const base = parts.map(p => p.m.rotation.clone());
    g.userData.update = t => { parts.forEach((p, i) => { p.m.rotation.set(base[i].x + p.w[0] * t, base[i].y + p.w[1] * t, base[i].z + p.w[2] * t); }); g.rotation.y = (o.spin ?? 0.12) * t; };
    return g;
  },
  // the space parasol: a red and white canopy of o.ribs gores (radius o.r), a pole and a hub; axis +Y (the canopy's top toward +Y); furled (a thin
  // spike) before o.openAt, open over o.openDur with an ease out and a small overshoot; o.open: already open; o.spin: slow turn about its axis
  orbitParasol(o) {
    const R = o.r ?? 6, H = R * 0.32, n = o.ribs ?? 12, g = grp(), can = grp(); g.add(can);
    const cols = o.colors || [RED, '#F4F1E8'];
    for (let i = 0; i < n; i++) { const m = new THREE.Mesh(new THREE.ConeGeometry(R, H, 1, 1, true, i * TAU / n, TAU / n), mat(cols[i % cols.length], { doubleSide: true })); m.position.y = -H / 2; can.add(m); }
    for (let i = 0; i < n; i++) { const a = i * TAU / n; can.add(rod([0, 0, 0], [Math.sin(a) * R, -H, Math.cos(a) * R], R * 0.006, '#9AA0A6', 4)); }
    can.add(at(new THREE.Mesh(new THREE.TorusGeometry(R, R * 0.008, 4, 48).rotateX(PI / 2), mat('#9AA0A6')), 0, -H, 0));
    g.add(at(cyl(R * 0.012, R * 0.012, R * 1.2, '#C9CDD3', 8, { pivot: 'top' }), 0, 0, 0), at(sphere(R * 0.04, '#C9CDD3', 1), 0, 0.02 * R, 0));
    g.add(at(box(R * 0.12, R * 0.08, R * 0.12, '#D9B44A', { outline: 0.01 }), 0, -R * 1.2, 0));   // the service module at the foot of the pole
    const set = op => { can.scale.set(0.05 + 0.95 * op, 1 + (1 - op) * 3.2, 0.05 + 0.95 * op); };
    set(o.open ?? 0);
    g.userData.update = t => {
      if (o.openAt != null) { const u = clamp01((t - o.openAt) / (o.openDur ?? 0.55)); set(Math.min(1.04, outBack(u) * 0.96 + 0.04 * u)); }
      can.rotation.y = (o.spin ?? 0) * t;
    };
    g.userData.update(-1); return g;
  },
  // the Earth (earthGlobe, held still) with the made-up country (ochre blobs, a darker border) facing +Z, and the parasol's round shadow, a dark cap
  // that swells over it from o.shadowAt over o.shadowDur up to o.shadowAng radians (0: none); o.shadow1: already there
  countryGlobe(o) {
    // (staging 2) earthGlobe stands on its south pole (its centre at y = R): the country and the shadow caps go in a group at that centre (at the
    // origin they made a black disc under the globe)
    const R = o.radius ?? 3, g0 = grp(buildProp('earthGlobe', { radius: R, seed: o.seed ?? 5 })), g = grp(); g.position.y = R; g0.add(g);
    const cap = (ang, rr, col, rx, ry) => { const m = new THREE.Mesh(new THREE.SphereGeometry(R * rr, 32, 6, 0, TAU, 0, ang), mat(col, { noGrain: true })); m.rotation.set(PI / 2 + rx, 0, ry); m.receiveShadow = true; m.castShadow = false; return m; };
    const blobs = [[0.32, 0, 0], [0.22, 0.18, 0.15], [0.2, -0.16, 0.2], [0.18, 0.1, -0.22], [0.16, -0.2, -0.14]];
    for (const [a, rx, ry] of blobs) { g.add(cap(a + 0.03, 1.004, '#8A5A2A', rx, ry), cap(a, 1.008, o.country || '#E8B44A', rx, ry)); }
    const sh = cap(1, 1.016, '#1E2430', 0, 0), sh2 = cap(1, 1.012, '#3A4250', 0, 0); g.add(sh2, sh);
    const angMax = o.shadowAng ?? 0.62;
    const setSh = v => { const a = Math.max(0.001, angMax * v); sh.geometry.dispose(); sh.geometry = new THREE.SphereGeometry(R * 1.016, 40, 6, 0, TAU, 0, a); sh2.geometry.dispose(); sh2.geometry = new THREE.SphereGeometry(R * 1.012, 40, 6, 0, TAU, 0, Math.min(PI / 2, a * 1.12)); sh.visible = sh2.visible = v > 0.01; };
    setSh(o.shadow1 ? 1 : 0); let last = -1;
    if (o.shadowAt != null) g0.userData.update = t => { const v = smooth((t - o.shadowAt) / (o.shadowDur ?? 0.5)); if (Math.abs(v - last) > 1e-4) { setSh(v); last = v; } };
    return g0;
  },
  // the parasol's shadow front sweeping over the land, seen from the air: a huge dark disc (o.r) laid o.y above the ground, unlit, see-through
  // (o.op), with two softer rims; move it with keys
  shadowFront(o) {
    const Rr = o.r ?? 600, g = grp(), op = o.op ?? 0.5;
    const disc = new THREE.Mesh(new THREE.CircleGeometry(Rr, 96).rotateX(-PI / 2), new THREE.MeshBasicMaterial({ color: o.color || '#121826', transparent: true, opacity: op, depthWrite: false, depthTest: o.depthTest ?? false, fog: false }));
    g.add(disc);
    [[1.0, 1.03, 0.6], [1.03, 1.07, 0.3]].forEach(([a, b, k]) => g.add(new THREE.Mesh(new THREE.RingGeometry(Rr * a, Rr * b, 96).rotateX(-PI / 2), new THREE.MeshBasicMaterial({ color: o.color || '#121826', transparent: true, opacity: op * k, depthWrite: false, depthTest: o.depthTest ?? false, fog: false }))));
    // (staging 2) no depth test by default: in the whole film the disc, 16 m over a ground seen from 400 m, lost the depth test to the lawn (the
    // camera's depth range is set for the close shots) and never showed, while the shot rendered alone showed it; it lies above everything anyway
    g.position.y = o.y ?? 14; g.traverse(m => { if (m.isMesh) m.renderOrder = 5; });
    // (staging 2) o.dx0 + o.moveAt/o.moveDur: the front slides by itself from dx0 (m along X) back to the prop's place, eased; a key move of the prop
    // left the disc out of the whole-film render (the shot rendered alone, or with its neighbours, showed it)
    if (o.moveAt != null) { const inner = grp(...g.children); g.add(inner); g.userData.update = t => { const u = smooth((t - o.moveAt) / (o.moveDur ?? 1)); inner.position.x = (o.dx0 ?? 0) * (1 - u); }; g.userData.update(0); }
    return g;
  },
  // a field of sunflowers (o.cols x o.rows, o.gap apart) facing +Z and up toward the sun; from o.droopAt each head, in a wave running from the
  // front row back (o.wave s per row), swings down to hang on its stem
  sunflowers(o) {
    const g = grp(), heads = [], C = o.cols ?? 7, Rw = o.rows ?? 5, gap = o.gap ?? 0.9, r = rng(o.seed || 21);
    for (let j = 0; j < Rw; j++) for (let i = 0; i < C; i++) {
      const x = (i - (C - 1) / 2) * gap + (r() - 0.5) * 0.25, z = -j * gap + (r() - 0.5) * 0.2, h = 1.5 + r() * 0.5, s = grp(); s.position.set(x, 0, z); s.rotation.y = (r() - 0.5) * 0.4;
      s.add(at(cyl(0.025, 0.035, h, '#4E8A3A', 6, { pivot: 'bottom' }), 0, 0, 0));
      for (const k of [0.35, 0.6]) s.add(at(box(0.26, 0.02, 0.12, '#5A9A45', { outline: 0.004 }), 0.12 * (k > 0.5 ? -1 : 1), h * k, 0, 0, 0, (k > 0.5 ? 1 : -1) * 0.5));
      const hd = grp(); hd.position.set(0, h, 0); hd.scale.setScalar(o.hs ?? 1); s.add(hd);
      const face = grp(); face.add(at(cyl(0.13, 0.13, 0.05, '#5A3A1E', 12, { outline: 0.008 }), 0, 0, 0, PI / 2, 0, 0));
      for (let p = 0; p < 12; p++) { const a = p * TAU / 12; face.add(at(box(0.07, 0.15, 0.02, '#F2C21E', { taper: { x: 0.4, z: 1 } }), Math.sin(a) * 0.2, Math.cos(a) * 0.2, -0.005, 0, 0, -a)); }
      face.position.set(0, 0.06, 0.05); hd.add(face);
      heads.push({ hd, d: j * (o.wave ?? 0.12) + r() * 0.08 }); g.add(s);
    }
    const up = o.up ?? -0.45, down = o.down ?? 1.7;
    g.userData.update = t => { for (const it of heads) { const u = o.droopAt == null ? 0 : clamp01((t - o.droopAt - it.d) / 0.45), e = u < 1 ? smooth(u) * 1.08 : 1; it.hd.rotation.x = up + (down - up) * e - (u >= 1 ? 0 : 0); } };
    g.userData.update(-1); return g;
  },
  // a solar panel laid off: the panel on two little legs with shoes, two thin arms holding a cardboard sign (o.sign); o.walk: the legs step and the
  // panel bobs (o.phase); o.tilt the panel's lean
  solarWalker(o) {
    const g = grp(), body = grp(); g.add(body);
    const pnl = canvasPlane(0.9, 0.62, (c, W, H) => { c.fillStyle = '#1C3F7A'; c.fillRect(0, 0, W, H); c.strokeStyle = '#8FB6E8'; c.lineWidth = 3; for (let i = 1; i < 6; i++) { c.beginPath(); c.moveTo(i * W / 6, 0); c.lineTo(i * W / 6, H); c.stroke(); } for (let j = 1; j < 4; j++) { c.beginPath(); c.moveTo(0, j * H / 4); c.lineTo(W, j * H / 4); c.stroke(); } }, { res: 256 });
    const panel = grp(at(box(0.96, 0.68, 0.05, '#B9BEC4', { outline: 0.008 }), 0, 0, -0.01), at(pnl, 0, 0, 0.018)); panel.position.set(0, 1.05, 0); panel.rotation.x = -(o.tilt ?? 0.35); body.add(panel);
    body.add(at(box(0.08, 0.3, 0.08, '#7E858C'), 0, 0.75, -0.05));
    const legs = [-1, 1].map(s => { const L = grp(at(box(0.05, 0.6, 0.05, '#7E858C', { pivot: 'top' }), 0, 0, 0), at(box(0.12, 0.07, 0.2, '#2A2A2E', { outline: 0.006 }), 0, -0.6, 0.04)); L.position.set(s * 0.14, 0.64, 0); g.add(L); return L; });
    const sign = canvasPlane(0.56, 0.36, (c, W, H) => { c.fillStyle = '#C9A46A'; c.fillRect(0, 0, W, H); c.strokeStyle = '#8A6A3A'; c.lineWidth = 6; c.strokeRect(3, 3, W - 6, H - 6); c.fillStyle = INK; c.textAlign = 'center'; c.textBaseline = 'middle';
      const L = String(o.sign || 'SANS SOLEIL').split('\n'); c.font = `900 ${H * (L.length > 1 ? 0.3 : 0.38)}px Arial`; L.forEach((l, i) => c.fillText(l, W / 2, H * (L.length > 1 ? 0.32 + i * 0.38 : 0.53))); }, { res: 256 });
    const sg = grp(at(box(0.58, 0.38, 0.02, '#B08A50'), 0, 0, -0.012), sign); sg.position.set(0, 0.8, 0.24); body.add(sg);
    for (const s of [-1, 1]) body.add(rod([s * 0.4, 0.95, 0.05], [s * 0.22, 0.82, 0.24], 0.012, '#7E858C', 4));
    const ph = o.phase ?? 0;
    g.userData.update = t => { if (!o.walk) return; const w = (t + ph) * 9; legs[0].rotation.x = 0.45 * Math.sin(w); legs[1].rotation.x = -0.45 * Math.sin(w); body.position.y = 0.03 * Math.abs(Math.cos(w)); body.rotation.z = 0.04 * Math.sin(w); };
    g.userData.update(0); return g;
  },
  // the unemployment office's front: a cream wall (o.w), a glass door, a blue sign (o.text), a closed shutter beside it
  jobOffice(o) {
    const W = o.w ?? 6, g = grp();
    g.add(at(box(W, 3.4, 0.3, '#E7DFCC', { pivot: 'bottom', outline: 0.006 }), 0, 0, -0.15));
    const sign = canvasPlane(W * 0.7, 0.55, (c, Wc, Hc) => { c.fillStyle = '#2E5E9E'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#F4F1E8'; c.font = `900 ${Hc * 0.5}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.text || 'BUREAU DU CHÔMAGE', Wc / 2, Hc * 0.55); }, { res: 1024 });
    g.add(at(sign, 0, 2.85, 0.02));
    g.add(at(box(1.3, 2.3, 0.06, '#3A4A58', { pivot: 'bottom', outline: 0.006 }), o.doorX ?? 0, 0, 0.02), at(box(1.1, 1.9, 0.02, '#9FC3D6', { pivot: 'bottom' }), o.doorX ?? 0, 0.25, 0.06));
    const sh = canvasPlane(1.6, 2.0, (c, Wc, Hc) => { c.fillStyle = '#A9AEB3'; c.fillRect(0, 0, Wc, Hc); c.strokeStyle = '#8A9096'; c.lineWidth = 4; for (let y = 8; y < Hc; y += 16) { c.beginPath(); c.moveTo(0, y); c.lineTo(Wc, y); c.stroke(); } }, { res: 256 });
    g.add(at(sh, (o.doorX ?? 0) + 2.0, 1.1, 0.02));
    return g;
  },
  // the underside of the parasol seen from the ground: an unlit dome (o.r) of dull red and cream gores radiating from the zenith, the rim dark at the
  // horizon; o.holeAt / o.hole1: the hole (a blazing sun disc in a ragged ring of torn fabric) at azimuth o.az, elevation o.el (degrees), popping
  // open at that time with a flash; o.holeR its angular size (radius in degrees)
  canopySky(o) {
    const Rr = o.r ?? 90, n = o.ribs ?? 16, g = grp();
    const tex = (() => { const cv = document.createElement('canvas'); cv.width = 1024; cv.height = 256; const c = cv.getContext('2d');
      for (let i = 0; i < n; i++) { c.fillStyle = i % 2 ? (o.c2 || '#8E8576') : (o.c1 || '#7C2F2A'); c.fillRect(i * 1024 / n, 0, 1024 / n + 1, 256); }
      const gr = c.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, 'rgba(0,0,0,0.0)'); gr.addColorStop(0.75, 'rgba(0,0,0,0.12)'); gr.addColorStop(1, 'rgba(10,10,14,0.55)'); c.fillStyle = gr; c.fillRect(0, 0, 1024, 256);
      c.strokeStyle = 'rgba(30,20,20,0.5)'; c.lineWidth = 3; for (let i = 0; i < n; i++) { c.beginPath(); c.moveTo(i * 1024 / n, 0); c.lineTo(i * 1024 / n, 256); c.stroke(); }
      // (staging 2) o.haze: a grey murk over the lower part of the dome, so that seen from the ground its foot reads as an overcast horizon, not as a
      // striped wall standing behind the set
      if ((o.haze ?? 0) > 0) { const hz = c.createLinearGradient(0, 120, 0, 256); hz.addColorStop(0, 'rgba(118,116,112,0)'); hz.addColorStop(0.55, 'rgba(118,116,112,' + (o.haze * 0.8) + ')'); hz.addColorStop(1, 'rgba(118,116,112,' + o.haze + ')'); c.fillStyle = hz; c.fillRect(0, 0, 1024, 256); }
      const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t; })();
    const dome = new THREE.Mesh(new THREE.SphereGeometry(Rr, 64, 24, 0, TAU, 0, PI / 2 + 0.06), new THREE.MeshBasicMaterial({ map: tex, side: THREE.BackSide, fog: false, color: o.tint || '#FFFFFF' }));
    g.add(dome);
    if (o.holeAt != null || o.hole1) {
      const az = (o.az ?? 0) * PI / 180, el = (o.el ?? 50) * PI / 180, dir = new THREE.Vector3(Math.sin(az) * Math.cos(el), Math.sin(el), -Math.cos(az) * Math.cos(el));
      const hole = grp(), hr = Math.tan((o.holeR ?? 3) * PI / 180) * Rr * 0.97;
      hole.add(new THREE.Mesh(new THREE.CircleGeometry(hr, 32), new THREE.MeshBasicMaterial({ color: '#FFF6C8', fog: false })));
      hole.add(at(new THREE.Mesh(new THREE.CircleGeometry(hr * 0.62, 32), new THREE.MeshBasicMaterial({ color: '#FFFFFF', fog: false })), 0, 0, 0.05));
      for (let i = 0; i < 9; i++) { const a = i * TAU / 9 + 0.2, f = new THREE.Mesh(new THREE.ConeGeometry(hr * 0.28, hr * (0.5 + 0.3 * hsh(i)), 3), new THREE.MeshBasicMaterial({ color: i % 2 ? '#6E2824' : '#7E766A', fog: false, side: THREE.DoubleSide }));
        f.position.set(Math.cos(a) * hr * 1.08, Math.sin(a) * hr * 1.08, -0.2); f.rotation.z = a - PI / 2; f.rotation.x = 0.5; hole.add(f); }   // the torn flaps, curled toward the ground
      const glow = glowSprite('#FFE7A0', hr * 7, 0.9), flash = glowSprite('#FFFFFF', hr * 16, 1); hole.add(glow, flash);
      hole.position.copy(dir.clone().multiplyScalar(Rr * 0.97)); hole.lookAt(0, 0, 0); g.add(hole);
      g.userData.hole = dir.toArray();
      g.userData.update = t => { const u = o.hole1 ? 1 : (t - o.holeAt) / 0.22; hole.visible = u > 0; const s = o.hole1 ? 1 : outBack(u); hole.scale.setScalar(Math.max(0.001, s)); flash.material.opacity = o.hole1 ? 0 : Math.max(0, 1 - (t - o.holeAt) / 0.35); glow.material.opacity = 0.75 + 0.15 * Math.sin(t * 7); };
      g.userData.update(-1);
    }
    return g;
  },
  // the single beam: a shaft of sunlight (radius o.r, length o.len) along its local -Y from the pivot (the hole end at the top), additive, with a
  // brighter core; o.onAt: it shoots down from the top over 0.25 s
  lightShaft(o) {
    const Rr = o.r ?? 5, L = o.len ?? 80, g = grp();
    const mk = (r, op, col) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r * 1.05, L, 32, 1, true).translate(0, -L / 2, 0), addMat(col, op, null)); m.renderOrder = 6; return m; };
    const a = mk(Rr, o.op ?? 0.35, '#FFE9A8'), b = mk(Rr * 0.6, (o.op ?? 0.35) * 0.9, '#FFF6DA'); g.add(a, b);
    const spot = new THREE.Mesh(new THREE.CircleGeometry(Rr * 1.15, 40).rotateX(-PI / 2), addMat('#FFE6A0', o.spotOp ?? 0.5, softTex('radial'))); spot.position.y = -L + 0.06; spot.renderOrder = 6; if (o.spot !== false) g.add(spot);
    if (o.onAt != null) g.userData.update = t => { const u = smooth((t - o.onAt) / 0.25); a.scale.y = b.scale.y = Math.max(0.001, u); spot.visible = u > 0.95; };
    return g;
  },
  // the lit garden from the air: a disc of bright, warm green lawn (o.r) with a glowing rim, laid on a grey country; and a dark see-through ring
  // around it (o.dark: its opacity) out to o.outer, the shade
  sunPatch(o) {
    const Rr = o.r ?? 8, g = grp();
    const lawn = new THREE.Mesh(new THREE.CircleGeometry(Rr, 48).rotateX(-PI / 2), mat(o.color || '#8FD06A', { emissive: o.emissive || '#3A4A10', noGrain: true })); lawn.receiveShadow = true; lawn.position.y = o.y ?? 0.02;
    if (o.lawn !== false) g.add(lawn);
    const rim = new THREE.Mesh(new THREE.RingGeometry(Rr * 0.96, Rr * 1.12, 64).rotateX(-PI / 2), addMat('#FFE7A0', o.rimOp ?? 0.55, null)); rim.position.y = (o.y ?? 0.02) + 0.02; g.add(rim);
    if (o.dark) { const ring = new THREE.Mesh(new THREE.RingGeometry(Rr * 1.08, o.outer ?? 400, 64).rotateX(-PI / 2), new THREE.MeshBasicMaterial({ color: '#141824', transparent: true, opacity: o.dark, depthWrite: false })); ring.position.y = (o.y ?? 0.02) + 0.03; g.add(ring); }
    return g;
  },
  // a tank whose gun rises to the vertical (o.raiseAt over 0.45 s) and fires at o.fireAt: a muzzle flash, a recoil, a smoke ring, the shell going
  // straight up at o.shellV m/s (hidden past o.shellMax); o.color
  skyTank(o) {
    const c = o.color || '#66753E', c2 = '#56633A', d = '#2B2E22', g = grp(), hull = grp(); g.add(hull);
    for (const sd of [-1, 1]) { hull.add(at(box(0.62, 0.62, 4.1, d, { pivot: 'bottom', outline: 0.012 }), sd * 1.32, 0.06, 0)); for (let i = 0; i < 5; i++) hull.add(at(cyl(0.27, 0.27, 0.08, '#8A9460', 10), sd * 1.64, 0.34, -1.6 + i * 0.8, 0, 0, PI / 2)); hull.add(at(box(0.72, 0.07, 4.5, c2, { outline: 0.008 }), sd * 1.32, 0.74, 0)); }
    hull.add(at(box(2.1, 0.62, 4.3, c, { pivot: 'bottom', outline: 0.012 }), 0, 0.42, 0), at(box(2.1, 0.5, 0.9, c, { outline: 0.01 }), 0, 0.82, 2.25, 0.6, 0, 0));
    const tur = grp(); tur.position.set(0, 1.04, -0.2); hull.add(tur);
    tur.add(at(box(1.5, 0.56, 1.8, c, { pivot: 'bottom', outline: 0.012, taper: { x: 0.8, z: 0.86 } }), 0, 0, 0), at(cyl(0.3, 0.32, 0.12, c2, 12, { pivot: 'bottom' }), 0.3, 0.56, -0.3));
    const gun = grp(); gun.position.set(0, 0.3, 0.7); tur.add(gun); const brl = grp(); gun.add(brl);
    brl.add(at(cyl(0.085, 0.11, 2.6, c, 10, { outline: 0.01 }), 0, 0, 1.3, PI / 2, 0, 0), at(cyl(0.15, 0.15, 0.34, d, 10), 0, 0, 2.72, PI / 2, 0, 0), at(box(0.5, 0.36, 0.3, c2, { outline: 0.008 }), 0, 0, 0.1));
    const fl = grp(at(new THREE.Mesh(new THREE.ConeGeometry(0.4, 1.4, 8), new THREE.MeshBasicMaterial({ color: '#FFD86A' })), 0, 0, 3.6, PI / 2, 0, 0), at(glowSprite('#FFC860', 3.5, 1), 0, 0, 3.2)); fl.visible = false; gun.add(fl);
    const smoke = []; for (let i = 0; i < 8; i++) { const m = sphere(0.35, '#D9D6CE', 0, { unique: true }); m.castShadow = false; m.visible = false; smoke.push(m); g.add(m); }
    const shell = grp(at(cyl(0.07, 0.07, 0.4, '#C9A040', 8), 0, 0, 0), at(new THREE.Mesh(new THREE.ConeGeometry(0.07, 0.18, 8), mat('#C9A040')), 0, 0.29, 0), at(glowSprite('#FFE0A0', 1.4, 0.9), 0, -0.25, 0)); shell.visible = false; g.add(shell);
    const vmax = o.shellMax ?? 200, V = o.shellV ?? 160, muzzle = new THREE.Vector3(), dir = new THREE.Vector3(), qq = new THREE.Quaternion();
    g.userData.update = t => {
      const e = o.raiseAt == null ? (o.pitch ?? 0) : smooth((t - o.raiseAt) / 0.45) * (o.pitch ?? 1.5);
      gun.rotation.x = -e; const f = o.fireAt ?? 1e9, dt = t - f;
      brl.position.z = dt > 0 && dt < 0.3 ? -0.35 * (1 - dt / 0.3) : 0; hull.rotation.x = dt > 0 && dt < 0.35 ? 0.03 * Math.sin(dt * 30) * (1 - dt / 0.35) : 0;
      fl.visible = dt > 0 && dt < 0.09;
      gun.updateMatrixWorld(true); muzzle.set(0, 0, 3.2); gun.localToWorld(muzzle); g.worldToLocal(muzzle);
      smoke.forEach((m, i) => { const u = (dt - i * 0.02) / 1.2; m.visible = u > 0 && u < 1; const a = i / 8 * TAU; m.position.set(muzzle.x + Math.cos(a) * (0.3 + 1.2 * easeOut(u)), muzzle.y + 0.5 * u + Math.sin(a) * 0.3, muzzle.z + Math.sin(a) * (0.3 + 1.2 * easeOut(u))); m.scale.setScalar(0.6 + 1.4 * easeOut(u)); });
      // the shell flies along the barrel as it was at the shot (the gun's +Z in the prop's frame), nose first
      dir.set(0, Math.sin(o.pitch ?? 1.5), Math.cos(o.pitch ?? 1.5)); const h = dt > 0 ? V * dt : -1; shell.visible = h > 0 && h < vmax;
      shell.position.copy(muzzle).addScaledVector(dir, Math.max(0, h)); qq.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir); shell.quaternion.copy(qq); shell.scale.setScalar(1 + Math.min(4, h / 30));
    };
    g.userData.update(-1); return g;
  },
  // a protest sign: a cardboard panel (o.w x o.h) with hand-lettered text (o.text, lines split by \n) on a wooden stick (o.stick long, pivot at the
  // stick's foot), the text on +Z
  protestSign(o) {
    const W = o.w ?? 0.7, H = o.h ?? 0.45, S = o.stick ?? 0.9, g = grp(at(box(0.03, S, 0.03, '#A67C52', { pivot: 'bottom' }), 0, 0, -0.02));
    const pl = canvasPlane(W, H, (c, Wc, Hc) => { c.fillStyle = o.bg || '#E9DCC0'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = o.fg || '#B5302A'; c.textAlign = 'center'; c.textBaseline = 'middle';
      const L = String(o.text || 'RENDEZ-NOUS\nLE SOLEIL').split('\n'); const fs = Math.min(Hc * 0.8 / L.length, Wc * 1.5 / Math.max(...L.map(l => l.length))); c.font = `900 ${fs}px Arial`; L.forEach((l, i) => c.fillText(l, Wc / 2, Hc * ((i + 0.55) / L.length))); }, { res: 384 });
    g.add(at(box(W + 0.02, H + 0.02, 0.012, '#B89A6A', { outline: 0.006 }), 0, S, -0.008), at(pl, 0, S, 0.0)); return g;
  },
  // a warm light leak at the edge of a frame (the sun behind the camera): a big soft additive glow (o.s) with a smaller hot core
  lensGlare(o) { return grp(glowSprite(o.color || '#FFD890', o.s ?? 3, o.op ?? 0.85), glowSprite('#FFFFFF', (o.s ?? 3) * 0.35, 0.9)); },
  // a hand torch (a black and yellow body, a glowing lens) pointing along its local +Y from the grip (pivot at its butt); o.beam: the beam's length
  // (props_interrupteur torchBeam, flat, unlit glow), o.beamR its spread
  handTorch(o) {
    const g = grp(at(cyl(0.035, 0.035, 0.2, '#22252B', 8, { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(cyl(0.055, 0.04, 0.08, o.color || '#E8B830', 10, { pivot: 'bottom', outline: 0.008 }), 0, 0.2, 0),
      at(cyl(0.05, 0.05, 0.006, '#FFF6D0', 10, { emissive: '#FFF0B0', noGrain: true }), 0, 0.283, 0));
    if (o.beam) { const b = buildProp('torchBeam', { len: o.beam, r: o.beamR ?? 0.6, flat: true, opacity: o.beamOp ?? 0.7 }); b.position.y = 0.28; g.add(b); if (o.face) b.rotation.y = o.face; }
    if (o.glow !== false) g.add(at(glowSprite('#FFF0B0', o.glowS ?? 0.5, 0.9), 0, 0.3, 0));
    return g;
  },
  // torches under arrest on a car bonnet: o.n torches lying side by side along x, each with its handcuffs closed on its body, their beams sideways
  // (+Z); the last one's cuff closes at o.clickAt (a ring that swings shut)
  cuffedTorches(o) {
    const n = o.n ?? 5, gap = o.gap ?? 0.2, g = grp(), last = [];
    for (let i = 0; i < n; i++) {
      const x = (i - (n - 1) / 2) * gap, tg = grp(); tg.position.set(x, 0.055, 0); g.add(tg);
      const tc = RAYON_PROPS.handTorch({ beam: o.beam ?? 1.6, beamR: 0.35, beamOp: 0.5, glowS: 0.35 }); tc.rotation.x = PI / 2; tc.position.z = -0.14; tg.add(tc);
      const ringA = at(new THREE.Mesh(new THREE.TorusGeometry(0.055, 0.012, 6, 14), mat('#E8E8EC')), 0, 0, 0, 0, PI / 2, 0); addOutline(ringA, 0.08);
      const ringB = at(new THREE.Mesh(new THREE.TorusGeometry(0.055, 0.012, 6, 14), mat('#E8E8EC')), 0, 0, 0, 0, PI / 2, 0); addOutline(ringB, 0.08);
      const cuff = grp(at(ringA, 0, 0, -0.02), rod([0, -0.03, -0.02], [gap * 0.5, -0.04, -0.02], 0.006, '#B9BEC4', 4)); tg.add(cuff);
      if (i < n - 1) tg.add(at(ringB, gap, 0, -0.02)); else { const sw = grp(ringB); sw.position.set(0, 0, -0.02); tg.add(sw); last.push(sw); }
    }
    if (o.clickAt != null) g.userData.update = t => { const u = smooth((t - o.clickAt) / 0.12); last.forEach(sw => { sw.rotation.y = (1 - u) * 1.4; sw.position.x = (1 - u) * 0.06; }); };
    if (g.userData.update) g.userData.update(-1);
    return g;
  },
  // the press room's screen on a stand: the grey country on a grey sea under a green banner MISSION RÉUSSIE with a tick
  pressScreen(o) {
    const W = o.w ?? 2.2, H = W * 0.6, g = grp();
    const scr = canvasPlane(W, H, (c, Wc, Hc) => { c.fillStyle = '#5E6670'; c.fillRect(0, 0, Wc, Hc); drawCountry(c, Wc * 0.5, Hc * 0.6, Hc * 0.3, '#8C9096', '#3E434A');
      c.fillStyle = '#2E8A4A'; c.fillRect(0, 0, Wc, Hc * 0.22); c.fillStyle = '#F4F1E8'; c.font = `900 ${Hc * 0.13}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.text || 'MISSION RÉUSSIE', Wc * 0.47, Hc * 0.12);
      c.strokeStyle = '#F4F1E8'; c.lineWidth = Hc * 0.035; c.lineCap = 'round'; c.beginPath(); c.moveTo(Wc * 0.86, Hc * 0.12); c.lineTo(Wc * 0.89, Hc * 0.16); c.lineTo(Wc * 0.95, Hc * 0.06); c.stroke(); }, { res: 768, emissive: 0.55 });
    g.add(at(box(W + 0.12, H + 0.12, 0.08, '#24272D', { outline: 0.008 }), 0, (o.y ?? 1.9), -0.05), at(scr, 0, (o.y ?? 1.9), 0.0));
    if (o.stand !== false) g.add(at(box(0.1, (o.y ?? 1.9) - H / 2, 0.1, '#24272D', { pivot: 'bottom' }), 0, 0, -0.1), at(box(0.9, 0.05, 0.6, '#24272D', { pivot: 'bottom' }), 0, 0, -0.1));
    return g;
  },
  // picnic things for the packed garden: o.blankets [[x, z, ry, w, d, colour], ...] (checked cloths flat on the grass), baskets, bottles, towels
  picnicSpread(o) {
    const g = grp(), r = rng(o.seed || 31);
    const cloth = (w, d, col) => { const p = canvasPlane(w, d, (c, W, H) => { c.fillStyle = '#F4F1E8'; c.fillRect(0, 0, W, H); c.fillStyle = col; const k = 8; for (let i = 0; i < k; i++) for (let j = 0; j < k; j++) if ((i + j) % 2 === 0) c.fillRect(i * W / k, j * H / k, W / k + 1, H / k + 1); }, { res: 256 }); p.rotation.x = -PI / 2; p.receiveShadow = true; return p; };
    for (const [x, z, ry, w, d, col] of (o.blankets || [])) { const b = grp(at(cloth(w ?? 1.6, d ?? 1.2, col || '#C23A2E'), 0, 0.012, 0)); b.position.set(x, 0, z); b.rotation.y = ry ?? 0; g.add(b);
      if (r() < 0.7) g.add(at(box(0.36, 0.2, 0.24, '#B88A5A', { pivot: 'bottom', outline: 0.006 }), x + (r() - 0.5) * (w ?? 1.6) * 0.6, 0, z + (r() - 0.5) * 0.5, 0, r() * TAU, 0));
      if (r() < 0.6) g.add(at(cyl(0.035, 0.035, 0.3, ['#2F7A4A', '#7A2A3A', '#2E5E9E'][Math.floor(r() * 3)], 8, { pivot: 'bottom' }), x + (r() - 0.5) * 0.8, 0, z + (r() - 0.5) * 0.6)); }
    return g;
  },
  // a beach towel draped over something (o.w x o.d, stripes o.colors), the ends hanging o.hang down the sides
  beachTowel(o) {
    const w = o.w ?? 0.8, d = o.d ?? 1.6, hang = o.hang ?? 0.25, cols = o.colors || ['#2E8AC9', '#F4F1E8'], g = grp();
    const tex = (W, H) => (c, Wc, Hc) => { const k = 7; for (let i = 0; i < k; i++) { c.fillStyle = cols[i % cols.length]; c.fillRect(0, i * Hc / k, Wc, Hc / k + 1); } };
    g.add(at(canvasPlane(w, d, tex(w, d), { res: 128 }), 0, 0.01, 0, -PI / 2, 0, 0));
    for (const s of [-1, 1]) g.add(at(canvasPlane(w, hang, tex(w, hang), { res: 64 }), 0, -hang / 2, s * d / 2, 0, 0, 0));
    return g;
  },
  // the garage's back shelf: three planks on uprights, paint pots, boxes, a coiled hose; o.parasol: the furled little parasol lying on the top plank
  garageShelf(o) {
    const W = o.w ?? 2.0, g = grp(), r = rng(o.seed || 17);
    for (const s of [-1, 1]) g.add(at(box(0.05, 1.9, 0.4, '#8A6A4A', { pivot: 'bottom', outline: 0.005 }), s * W / 2, 0, 0));
    for (const y of [0.45, 1.05, 1.65]) { g.add(at(box(W, 0.04, 0.42, '#A07A52', { outline: 0.005 }), 0, y, 0));
      for (let i = 0; i < 4; i++) { const x = -W / 2 + 0.25 + i * (W - 0.4) / 3 + (r() - 0.5) * 0.1; if (r() < 0.5) g.add(at(cyl(0.1, 0.1, 0.2, ['#C9CDD3', '#B5302A', '#2E5E9E'][i % 3], 10, { pivot: 'bottom', outline: 0.006 }), x, y + 0.02, 0)); else g.add(at(box(0.3, 0.22, 0.3, '#B8925E', { pivot: 'bottom', outline: 0.006 }), x, y + 0.02, 0, 0, r() * 0.3, 0)); } }
    g.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.035, 6, 16), mat('#2F8A4A')), W / 2 - 0.3, 0.75, 0.05));
    return g;
  },
  // (round 1) hides the set's own clouds (pavillon always adds them; at a long lens they read as floating beige slabs): an empty prop that, each frame,
  // finds the scene's objects named 'cloud' (props.js cloud, set level, high above the ground) and hides them
  noClouds(o) {
    const g = grp();
    g.userData.update = () => { let rt = g; while (rt.parent) rt = rt.parent; if (rt !== g) rt.traverse(c => { if (c.name === 'cloud') c.visible = false; }); };
    return g;
  },
  // (round 1) the little parasol from the garage, held in the hand: the pivot is the grip (where the hand closes), a hooked wooden handle under it,
  // the pole up to a faded canopy (radius o.r, colours o.colors: washed-out pink and cream); furled before o.openAt, then it pops open in 0.16 s
  // with an overshoot and a wobble, and a cloud of soft beige dust puffs (smooth shaded, like the rocket smoke) bursts from the rim, hangs and sinks
  kidParasol(o) {
    const R = o.r ?? 0.5, L = o.len ?? 0.78, g = grp(), wood = '#A88A62', cols = o.colors || ['#D8AFA4', '#EDE5D0'];
    g.add(at(cyl(0.014, 0.014, L + 0.12, wood, 6, { pivot: 'bottom', outline: 0.004 }), 0, -0.12, 0));
    g.add(rod([0, -0.12, 0], [0.02, -0.17, 0], 0.016, wood, 5), rod([0.02, -0.17, 0], [0.07, -0.17, 0], 0.016, wood, 5), rod([0.07, -0.17, 0], [0.085, -0.12, 0], 0.016, wood, 5));
    const can = grp(); can.position.y = L; g.add(can);
    for (let i = 0; i < 8; i++) { const m = new THREE.Mesh(new THREE.ConeGeometry(R, R * 0.42, 1, 1, true, i * TAU / 8, TAU / 8), mat(cols[i % cols.length], { doubleSide: true, unique: true })); m.position.y = -R * 0.21; can.add(m); }
    for (let i = 0; i < 8; i++) { const a = i * TAU / 8; can.add(rod([0, 0, 0], [Math.sin(a) * R, -R * 0.42, Math.cos(a) * R], 0.006, '#8A8478', 3)); }
    can.add(at(sphere(0.025, '#C9B48A', 1), 0, 0.03, 0));
    const set = op => { can.scale.set(0.08 + 0.92 * op, 1 + (1 - op) * 2.4, 0.08 + 0.92 * op); can.position.y = L - (1 - op) * R * 0.5; };
    set(o.open ? 1 : 0);
    const puffs = []; for (let i = 0; i < (o.puffs ?? 16); i++) { const m = new THREE.Mesh(sphereGeo(2), cloudMat(o.dust || '#E6D7B4', '#B9A37C')); m.castShadow = false; m.visible = false; const a = i / (o.puffs ?? 16) * TAU + hsh(i) * 0.4;
      puffs.push({ m, a, out: 0.25 + 0.35 * hsh(i + 7), up: (hsh(i + 3) - 0.3) * 0.25, s: 0.07 + 0.07 * hsh(i + 11), d: 0.04 * hsh(i + 5) }); g.add(m); }
    g.userData.update = t => {
      if (o.openAt == null) return;
      const u = (t - o.openAt) / (o.openDur ?? 0.16), op = u <= 0 ? 0 : Math.min(1.08, outBack(u) * 0.97 + 0.03 * clamp01(u));
      set(op); const w = t - o.openAt - (o.openDur ?? 0.16); can.rotation.z = w > 0 ? 0.12 * Math.exp(-w * 6) * Math.sin(w * 22) : 0; can.rotation.x = w > 0 ? 0.07 * Math.exp(-w * 6) * Math.sin(w * 22 + 1.3) : 0;
      for (const p of puffs) { const v = (t - o.openAt - p.d) / (o.dustDur ?? 1.4); p.m.visible = v > 0 && v < 1; if (!p.m.visible) continue;
        const e = easeOut(Math.min(1, v * 2.2)), rr = R * (0.85 + p.out * e / R * 1.2); p.m.position.set(Math.sin(p.a) * rr, L - R * 0.35 + p.up * e - 0.35 * v * v, Math.cos(p.a) * rr);
        p.m.scale.setScalar(Math.max(0.005, p.s * (0.5 + 1.4 * e) * (v < 0.6 ? 1 : 1 - (v - 0.6) / 0.4))); }
    };
    g.userData.update(-1); return g;
  },
  // grey dust shaken out of the old parasol when it opens: o.at the burst, round grey puffs flying out and fading (scaled down, never transparent)
  dustBurst(o) {
    const g = grp(), ps = []; for (let i = 0; i < 12; i++) { const m = sphere(0.09 + 0.05 * hsh(i), '#B9B3A6', 0, { unique: true }); m.castShadow = false; m.visible = false; const a = i / 12 * TAU; ps.push({ m, d: [Math.cos(a), 0.3 + 0.5 * hsh(i + 4), Math.sin(a)] }); g.add(m); }
    g.userData.update = t => { const u = (t - (o.at ?? 0)) / (o.dur ?? 0.8); ps.forEach(p => { p.m.visible = u > 0 && u < 1; const e = easeOut(u), rr = (o.r ?? 0.9) * e; p.m.position.set(p.d[0] * rr, p.d[1] * rr - 0.25 * u * u, p.d[2] * rr); p.m.scale.setScalar(Math.max(0.01, (1 + 1.4 * e) * (1 - u * 0.85))); }); };
    g.userData.update(-1); return g;
  },
};
