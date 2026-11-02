// Hand-drawn line-art face painted onto the front of the box head.
// Matched to the character sheet + source frames (measured on the 160×440 px front face of the sheet):
//   • eyes SMALL (Ø ≈ 0.13 W), white with a thick ink ring and a dot pupil, strongly UNEVEN:
//     left eye high (0.30 W, 0.32 H), right eye low (0.66 W, 0.47 H)
//   • thin arched brows floating above each eye
//   • nose = tiny "w" squiggle (0.47 W, 0.63 H)    • mouth = short thick bar (0.34–0.66 W, 0.77 H)
//   • stubble = short VERTICAL dashes, sparse, lower third + upper lip + jaw
//   • hair = solid black cap with a scribbled curly fringe and sideburns down the face edges
//   • thick ink border around the whole face panel
import * as THREE from 'three';
import { rng } from './style.js';

export const EXPRESSIONS = [
  'neutral', 'blink', 'surprised', 'shocked', 'suspicious', 'unimpressed', 'sad', 'worried', 'angry',
  'smug', 'sleepy', 'scared', 'happy', 'disgusted', 'grimace', 'sideLook', 'dead', 'talk',
];

const cache = new Map();
const W = 256, H = 640; // face panel aspect ≈ head front (0.23 × 0.6)

function scribbleFringe(g, r, color, hairTop, style) {
  g.fillStyle = color; g.strokeStyle = color;
  if (style === 'receding') { g.fillRect(0, 0, 50, hairTop * 0.5); g.fillRect(W - 50, 0, 50, hairTop * 0.5); }
  else g.fillRect(0, 0, W, hairTop * 0.45);
  // curly scribble loops along the fringe
  const loops = style === 'curly' || style === 'afro' ? 260 : 170;
  for (let i = 0; i < loops; i++) {
    const x = r() * W; if (style === 'receding' && x > 55 && x < W - 55) continue;
    const y = hairTop * (0.35 + Math.pow(r(), 1.6) * 0.75);
    g.lineWidth = 2.2 + r() * 1.8; g.beginPath();
    const rad = 3 + r() * 5; g.arc(x, y, rad, r() * 6, r() * 6 + 3.5 + r() * 2); g.stroke();
  }
  // sideburns: scribbles running down both edges
  for (let i = 0; i < 70; i++) {
    const side = i % 2 ? 1 : 0; const x = side ? W - 4 - r() * 14 : 4 + r() * 14; const y = hairTop * 0.4 + r() * H * 0.12;
    g.lineWidth = 2 + r() * 1.5; g.beginPath(); g.arc(x, y, 2 + r() * 4, r() * 6, r() * 6 + 4); g.stroke();
  }
}

export function faceTexture(o = {}) {
  const opt = { skin: '#D9A877', hair: 'crew', hairColor: '#17181B', facial: 'stubble', expression: 'neutral', glasses: false, seed: 3, lipstick: false, ...o };
  const key = JSON.stringify(opt);
  if (cache.has(key)) return cache.get(key);
  const c = document.createElement('canvas'); c.width = W; c.height = H;
  const g = c.getContext('2d'); const r = rng(opt.seed);
  g.fillStyle = opt.skin; g.fillRect(0, 0, W, H);
  for (let i = 0; i < 380; i++) { g.fillStyle = `rgba(120,70,40,${r() * 0.045})`; g.fillRect(r() * W, r() * H, 4 + r() * 10, 3 + r() * 8); }
  g.lineCap = 'round'; g.lineJoin = 'round';

  const hairTop = { crew: 70, bald: 0, combover: 60, mohawk: 30, curly: 95, long: 100, bun: 70, slick: 60, buzz: 40, afro: 110, receding: 60, spiky: 80 }[opt.hair] ?? 70;
  if (opt.hair !== 'bald' && hairTop > 0) scribbleFringe(g, r, opt.hairColor, hairTop, opt.hair);
  if (opt.hair === 'long') { g.fillStyle = opt.hairColor; g.fillRect(0, 0, 22, H * 0.55); g.fillRect(W - 22, 0, 22, H * 0.55); }

  const e = opt.expression, ink = '#111';
  const L = { x: 0.30 * W, y: 0.32 * H }, R = { x: 0.66 * W, y: 0.47 * H }, er = 0.078 * W; // eye radius
  // --- brows (thin arcs) --------------------------------------------------
  const browCfg = {
    neutral: [0, 0, 0, 0], blink: [0, 0, 0, 0], surprised: [-10, 0, -10, 0], shocked: [-16, 0, -16, 0], suspicious: [-10, 0, 6, 8],
    unimpressed: [4, 0, 4, 0], sad: [-2, 8, -2, -8], worried: [-12, 10, -12, -10], angry: [6, -10, 6, 10], smug: [-8, 0, 2, 6],
    sleepy: [4, 0, 4, 0], scared: [-14, 10, -14, -10], happy: [-6, 0, -6, 0], disgusted: [2, -8, -8, 6], grimace: [-4, 8, -4, -8],
    sideLook: [-4, 0, 0, 0], dead: [0, 0, 0, 0], talk: [-3, 0, 0, 0],
  }[e] || [0, 0, 0, 0];
  const brow = (p, dy, tilt) => {
    g.strokeStyle = ink; g.lineWidth = 4; g.beginPath();
    const y = p.y - er * 2.6 + dy;
    g.moveTo(p.x - er * 1.1, y + 4 + tilt * 0.5); g.quadraticCurveTo(p.x, y - 5, p.x + er * 1.1, y + 4 - tilt * 0.5); g.stroke();
  };
  brow(L, browCfg[0], browCfg[1]); brow(R, browCfg[2], browCfg[3]);

  // --- eyes -------------------------------------------------------------------
  const eye = (p, { scale = 1, lid = 0, pupil = [0, 0], closed = false, happy = false, x = false } = {}) => {
    const rr = er * scale;
    if (x) { g.strokeStyle = ink; g.lineWidth = 4; g.beginPath(); g.moveTo(p.x - rr, p.y - rr); g.lineTo(p.x + rr, p.y + rr); g.moveTo(p.x + rr, p.y - rr); g.lineTo(p.x - rr, p.y + rr); g.stroke(); return; }
    if (closed) { g.strokeStyle = ink; g.lineWidth = 4; g.beginPath(); if (happy) g.arc(p.x, p.y + rr * 0.5, rr, Math.PI * 1.15, Math.PI * 1.85); else { g.moveTo(p.x - rr, p.y); g.lineTo(p.x + rr, p.y); } g.stroke(); return; }
    g.fillStyle = '#F7F5EE'; g.strokeStyle = ink; g.lineWidth = 4.5;
    g.beginPath(); g.arc(p.x, p.y, rr, 0, Math.PI * 2); g.fill(); g.stroke();
    g.fillStyle = ink; g.beginPath(); g.arc(p.x + pupil[0] * rr, p.y + pupil[1] * rr, rr * 0.36, 0, Math.PI * 2); g.fill();
    if (lid > 0) { // flat upper lid (unimpressed / skeptical look)
      const ly = p.y - rr + 2 * rr * lid;
      g.save(); g.beginPath(); g.arc(p.x, p.y, rr + 1, 0, Math.PI * 2); g.clip();
      g.fillStyle = opt.skin; g.fillRect(p.x - rr - 3, p.y - rr - 3, 2 * rr + 6, ly - (p.y - rr) + 3); g.restore();
      g.strokeStyle = ink; g.lineWidth = 4.5; g.beginPath(); const hw = Math.sqrt(Math.max(0, rr * rr - (ly - p.y) ** 2)); g.moveTo(p.x - hw - 2, ly); g.lineTo(p.x + hw + 2, ly); g.stroke();
    }
  };
  switch (e) {
    case 'blink': case 'sleepy': eye(L, { closed: true }); eye(R, { closed: true }); break;
    case 'happy': eye(L, { closed: true, happy: true }); eye(R, { closed: true, happy: true }); break;
    case 'dead': eye(L, { x: true }); eye(R, { x: true }); break;
    case 'surprised': eye(L, { scale: 1.2 }); eye(R, { scale: 1.15 }); break;
    case 'shocked': case 'scared': eye(L, { scale: 1.3, pupil: [0, 0.1] }); eye(R, { scale: 1.25, pupil: [0, 0.1] }); break;
    case 'unimpressed': eye(L, { lid: 0.5, pupil: [0, 0.3] }); eye(R, { lid: 0.5, pupil: [0, 0.3] }); break;
    case 'suspicious': eye(L, { lid: 0.5, pupil: [0.3, 0.2] }); eye(R, { pupil: [0.3, 0] }); break;
    case 'smug': eye(L, { lid: 0.45, pupil: [0.2, 0.3] }); eye(R, { lid: 0.3, pupil: [0.2, 0.2] }); break;
    case 'angry': eye(L, { lid: 0.35 }); eye(R, { lid: 0.35 }); break;
    case 'sad': case 'worried': eye(L, { pupil: [0, 0.35] }); eye(R, { pupil: [0, 0.35] }); break;
    case 'disgusted': eye(L, { lid: 0.5 }); eye(R, { scale: 1.05 }); break;
    case 'grimace': eye(L, { scale: 1.1 }); eye(R, { scale: 1.05 }); break;
    case 'sideLook': eye(L, { pupil: [0.5, 0] }); eye(R, { pupil: [0.5, 0] }); break;
    default: eye(L, { pupil: [0.08, 0.05] }); eye(R, { pupil: [0.08, 0.05] });
  }
  if (opt.glasses) {
    g.strokeStyle = ink; g.lineWidth = 4;
    g.strokeRect(L.x - er * 1.9, L.y - er * 1.6, er * 3.8, er * 3.2); g.strokeRect(R.x - er * 1.9, R.y - er * 1.6, er * 3.8, er * 3.2);
    g.beginPath(); g.moveTo(L.x + er * 1.9, L.y); g.lineTo(R.x - er * 1.9, R.y); g.stroke();
  }

  // --- nose: tiny "w" ------------------------------------------------------------
  const nx = 0.47 * W, ny = 0.63 * H; g.strokeStyle = ink; g.lineWidth = 3; g.beginPath();
  g.moveTo(nx - 9, ny - 3); g.quadraticCurveTo(nx - 6, ny + 5, nx - 1, ny); g.quadraticCurveTo(nx + 4, ny + 5, nx + 8, ny - 3); g.stroke();

  // --- facial hair: short vertical dashes -----------------------------------------
  const mouthY = 0.77 * H;
  if (opt.facial === 'stubble' || opt.facial === 'beard') {
    const n = opt.facial === 'beard' ? 700 : 85;
    for (let i = 0; i < n; i++) {
      const x = 14 + r() * (W - 28), y = 0.68 * H + Math.pow(r(), 0.8) * (H * 0.3);
      if (opt.facial === 'stubble' && Math.abs(y - mouthY) < 12 && x > 0.3 * W && x < 0.7 * W) continue;
      g.fillStyle = `rgba(18,18,18,${0.8 + r() * 0.2})`; const len = 8 + r() * 8;
      g.save(); g.translate(x, y); g.rotate((r() - 0.5) * 0.4); g.fillRect(-1.6, -len / 2, 3.2, len); g.restore();
    }
  }
  if (opt.facial === 'mustache' || opt.facial === 'cop') {
    g.fillStyle = opt.hairColor; g.beginPath();
    g.moveTo(W / 2 - 46, mouthY - 10); g.quadraticCurveTo(W / 2, mouthY - 38, W / 2 + 46, mouthY - 10);
    g.quadraticCurveTo(W / 2, mouthY - 20, W / 2 - 46, mouthY - 10); g.fill();
    for (let i = 0; i < 60; i++) { g.fillRect(20 + r() * (W - 40), 0.8 * H + r() * 0.17 * H, 2.4, 7); }
  }

  // --- mouth ------------------------------------------------------------------------
  g.strokeStyle = opt.lipstick ? '#B5302A' : ink; g.fillStyle = '#2A0E0A'; g.lineWidth = 6;
  const mx0 = 0.34 * W, mx1 = 0.66 * W, mc = (mx0 + mx1) / 2;
  g.beginPath();
  switch (e) {
    case 'surprised': g.ellipse(mc, mouthY + 4, 11, 15, 0, 0, Math.PI * 2); g.fill(); break;
    case 'shocked': case 'scared': { // open trapezoid, teeth on top, tongue
      g.moveTo(mc - 28, mouthY - 14); g.lineTo(mc + 28, mouthY - 14); g.lineTo(mc + 20, mouthY + 30); g.lineTo(mc - 20, mouthY + 30); g.closePath(); g.fill();
      g.lineWidth = 5; g.stroke(); g.fillStyle = '#F4F1E8'; g.fillRect(mc - 22, mouthY - 11, 44, 8); g.fillStyle = '#C46A6A'; g.beginPath(); g.ellipse(mc, mouthY + 24, 14, 6, 0, Math.PI, 0); g.fill(); break; }
    case 'grimace': { g.fillRect(mc - 32, mouthY - 10, 64, 22); g.lineWidth = 5; g.strokeRect(mc - 32, mouthY - 10, 64, 22); g.fillStyle = '#F4F1E8'; for (let k = 0; k < 4; k++) { g.fillRect(mc - 27 + k * 14, mouthY - 7, 10, 7); g.fillRect(mc - 27 + k * 14, mouthY + 2, 10, 7); } break; }
    case 'talk': g.ellipse(mc, mouthY + 2, 16, 8, 0, 0, Math.PI * 2); g.fill(); break;
    case 'happy': g.arc(mc, mouthY - 22, 30, Math.PI * 0.22, Math.PI * 0.78); g.stroke(); break;
    case 'smug': g.moveTo(mx0 + 4, mouthY); g.quadraticCurveTo(mc + 6, mouthY + 10, mx1 + 2, mouthY - 8); g.stroke(); break;
    case 'sad': case 'worried': g.arc(mc, mouthY + 24, 22, Math.PI * 1.22, Math.PI * 1.78); g.stroke(); break;
    case 'angry': case 'disgusted': g.moveTo(mx0, mouthY + 5); g.lineTo(mc - 8, mouthY - 2); g.lineTo(mc + 10, mouthY + 4); g.lineTo(mx1, mouthY - 2); g.stroke(); break;
    case 'dead': g.moveTo(mx0, mouthY); g.lineTo(mx1, mouthY); g.stroke(); g.fillStyle = '#C46'; g.fillRect(mc + 4, mouthY, 12, 16); break;
    default: g.moveTo(mx0, mouthY); g.lineTo(mx1, mouthY + 1); g.stroke();
  }

  // --- thick ink border around the face panel ---------------------------------------
  g.strokeStyle = ink; g.lineWidth = 10; g.strokeRect(5, 5, W - 10, H - 10);

  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  cache.set(key, tex);
  return tex;
}

// Side / back of the head: black cap with "drippy" streaks toward the back, stubble near the jaw.
export function sideTexture(o = {}) {
  const opt = { skin: '#D9A877', hair: 'crew', hairColor: '#17181B', facial: 'stubble', seed: 5, back: false, ...o };
  const key = 'side' + JSON.stringify(opt);
  if (cache.has(key)) return cache.get(key);
  const c = document.createElement('canvas'); c.width = 200; c.height = H;
  const g = c.getContext('2d'); const r = rng(opt.seed); const SW = 200;
  g.fillStyle = opt.skin; g.fillRect(0, 0, SW, H);
  if (opt.hair !== 'bald') {
    g.fillStyle = opt.hairColor;
    if (opt.back) { // back: hair down to ~45 %, drippy lower edge
      const base = opt.hair === 'long' ? H * 0.7 : H * 0.36; g.fillRect(0, 0, SW, base);
      for (let x = 0; x < SW; x += 9) { const d = 10 + r() * 60; g.fillRect(x, base - 2, 6 + r() * 4, d); g.beginPath(); g.arc(x + 5, base + d, 5, 0, Math.PI * 2); g.fill(); }
    } else { // side: cap on top, hair covering the BACK half, drips running down
      // u = 0 is the front edge of the side face for +x side after mirroring; we paint for "front on the left"
      g.fillRect(0, 0, SW, H * 0.09);
      const backStart = SW * 0.42; const base = opt.hair === 'long' ? H * 0.6 : H * 0.3;
      g.fillRect(backStart, 0, SW - backStart, base);
      for (let x = backStart; x < SW; x += 10) { const d = 10 + r() * 70; g.fillRect(x, base - 2, 5 + r() * 4, d); g.beginPath(); g.arc(x + 4, base + d, 4.5, 0, Math.PI * 2); g.fill(); }
      for (let x = 0; x < backStart; x += 8) { const d = 5 + r() * 22; g.fillRect(x, H * 0.09 - 2, 4 + r() * 3, d); }
    }
  }
  if (!opt.back && (opt.facial === 'stubble' || opt.facial === 'beard')) {
    for (let i = 0; i < (opt.facial === 'beard' ? 500 : 60); i++) { g.fillStyle = 'rgba(20,20,20,0.85)'; g.fillRect(r() * SW * 0.45, H * 0.7 + r() * H * 0.28, 2.4, 7); }
  }
  // dark edge line between the face and the side (sheet: thick ink on the front edge)
  if (!opt.back) { g.fillStyle = '#111'; g.fillRect(0, 0, 7, H); }
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  cache.set(key, tex); return tex;
}
