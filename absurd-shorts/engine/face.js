// Hand-drawn line-art face painted onto the front of the box head.
// Signature traits from the source: asymmetric eyes (one round + dot pupil,
// one half-lidded), thick arched brows, a tiny flat mouth line, a side nose
// stroke, dense stubble dots on the lower third and a spiky hatched hairline.
import * as THREE from 'three';
import { rng } from './style.js';

export const EXPRESSIONS = [
  'neutral', 'blink', 'surprised', 'shocked', 'suspicious', 'sad', 'angry',
  'smug', 'sleepy', 'scared', 'happy', 'disgusted', 'dead', 'talk',
];

const cache = new Map();

export function faceTexture(o = {}) {
  const opt = {
    skin: '#D9A877', hair: 'crew', hairColor: '#17181B', facial: 'stubble',
    expression: 'neutral', glasses: false, seed: 3, lipstick: false, ...o,
  };
  const key = JSON.stringify(opt);
  if (cache.has(key)) return cache.get(key);
  const W = 256, H = 512;
  const c = document.createElement('canvas'); c.width = W; c.height = H;
  const g = c.getContext('2d'); const r = rng(opt.seed);
  // skin + subtle mottling
  g.fillStyle = opt.skin; g.fillRect(0, 0, W, H);
  for (let i = 0; i < 500; i++) { g.fillStyle = `rgba(120,70,40,${r() * 0.05})`; g.fillRect(r() * W, r() * H, 3 + r() * 8, 2 + r() * 6); }
  g.lineCap = 'round'; g.lineJoin = 'round'; g.strokeStyle = '#111'; g.fillStyle = '#111';

  // --- hairline -------------------------------------------------------
  const hairTop = { crew: 70, bald: 0, combover: 60, mohawk: 40, curly: 95, long: 100, bun: 80, slick: 75, buzz: 45, afro: 110, receding: 50, spiky: 85 }[opt.hair] ?? 70;
  if (opt.hair !== 'bald' && hairTop > 0) {
    g.fillStyle = opt.hairColor; g.strokeStyle = opt.hairColor;
    if (opt.hair === 'receding') { g.fillRect(0, 0, 40, hairTop); g.fillRect(W - 40, 0, 40, hairTop); }
    else g.fillRect(0, 0, W, hairTop * 0.55);
    // spiky hatching along the hairline
    for (let x = 0; x < W; x += 3) {
      if (opt.hair === 'receding' && x > 40 && x < W - 40) continue;
      const len = hairTop * (0.35 + r() * 0.6);
      g.lineWidth = 1 + r() * 2.2; g.beginPath(); g.moveTo(x, hairTop * 0.4);
      const curl = opt.hair === 'curly' || opt.hair === 'afro' ? 8 : 2;
      g.quadraticCurveTo(x + (r() - 0.5) * curl * 3, hairTop * 0.5 + len * 0.5, x + (r() - 0.5) * 6, hairTop * 0.35 + len);
      g.stroke();
    }
    if (opt.hair === 'combover') { g.lineWidth = 3; for (let i = 0; i < 14; i++) { g.beginPath(); g.moveTo(20, 20 + i * 3); g.quadraticCurveTo(W / 2, 5 + i * 4, W - 10, 30 + i * 2); g.stroke(); } }
    if (opt.hair === 'long') { g.fillRect(0, 0, 26, H * 0.62); g.fillRect(W - 26, 0, 26, H * 0.62); }
  }
  g.strokeStyle = '#111'; g.fillStyle = '#111';

  const e = opt.expression;
  const eyeY = 185, lx = 76, rx = 176;
  // --- eyebrows -------------------------------------------------------
  const browPose = {
    neutral: [[-4, 0], [4, 0]], blink: [[-4, 0], [4, 0]], surprised: [[-18, -6], [-18, 6]], shocked: [[-24, -8], [-24, 8]],
    suspicious: [[-16, -6], [6, 10]], sad: [[-6, 12], [-6, -12]], angry: [[4, 14], [4, -14]], smug: [[-12, -4], [2, 6]],
    sleepy: [[4, 0], [4, 0]], scared: [[-14, 10], [-14, -10]], happy: [[-10, -2], [-10, 2]], disgusted: [[2, 10], [-10, -6]],
    dead: [[0, 0], [0, 0]], talk: [[-6, 0], [4, 0]],
  }[e] || [[0, 0], [0, 0]];
  const brow = (cx, dy, tilt, flip) => {
    g.lineWidth = 11; g.beginPath();
    const y = eyeY - 50 + dy;
    g.moveTo(cx - 26, y + tilt * (flip ? -1 : 1) * 0.5 + 6);
    g.quadraticCurveTo(cx, y - 12, cx + 26, y - tilt * (flip ? -1 : 1) * 0.5 + 6);
    g.stroke();
  };
  brow(lx, browPose[0][0], browPose[0][1], false); brow(rx, browPose[1][0], browPose[1][1], true);

  // --- eyes ------------------------------------------------------------
  const eyeOpen = (cx, cy, w, h, pupil = [0, 0], lid = 0) => {
    g.fillStyle = '#F7F4EC'; g.lineWidth = 4;
    g.beginPath(); g.ellipse(cx, cy, w, h, 0, 0, Math.PI * 2); g.fill(); g.stroke();
    g.fillStyle = '#111'; g.beginPath(); g.arc(cx + pupil[0], cy + pupil[1], Math.min(w, h) * 0.33, 0, Math.PI * 2); g.fill();
    if (lid > 0) { // heavy upper lid
      g.fillStyle = opt.skin; g.beginPath(); g.ellipse(cx, cy - h, w + 3, h * 2 * lid, 0, 0, Math.PI); g.fill();
      g.lineWidth = 5; g.beginPath(); g.moveTo(cx - w, cy - h + h * 2 * lid); g.lineTo(cx + w, cy - h + h * 2 * lid); g.stroke();
    }
  };
  const eyeClosed = (cx, cy, happy) => { g.lineWidth = 5; g.beginPath(); if (happy) g.arc(cx, cy + 6, 16, Math.PI * 1.1, Math.PI * 1.9); else { g.moveTo(cx - 18, cy); g.lineTo(cx + 18, cy); } g.stroke(); };
  const eyeX = (cx, cy) => { g.lineWidth = 5; g.beginPath(); g.moveTo(cx - 14, cy - 14); g.lineTo(cx + 14, cy + 14); g.moveTo(cx + 14, cy - 14); g.lineTo(cx - 14, cy + 14); g.stroke(); };
  switch (e) {
    case 'blink': case 'sleepy': eyeClosed(lx, eyeY); eyeClosed(rx, eyeY + 4); break;
    case 'happy': eyeClosed(lx, eyeY, true); eyeClosed(rx, eyeY, true); break;
    case 'dead': eyeX(lx, eyeY); eyeX(rx, eyeY); break;
    case 'surprised': eyeOpen(lx, eyeY, 28, 28); eyeOpen(rx, eyeY + 3, 24, 24, [0, 0]); break;
    case 'shocked': case 'scared': eyeOpen(lx, eyeY, 32, 35, [0, 2]); eyeOpen(rx, eyeY + 2, 28, 31, [-2, 2]); break;
    case 'suspicious': eyeOpen(lx, eyeY, 26, 18, [6, 0], 0.45); eyeOpen(rx, eyeY + 2, 25, 22, [6, 0]); break;
    case 'smug': eyeOpen(lx, eyeY, 25, 19, [4, 2], 0.5); eyeOpen(rx, eyeY + 3, 22, 18, [4, 2], 0.45); break;
    case 'angry': eyeOpen(lx, eyeY, 25, 19, [0, 0], 0.35); eyeOpen(rx, eyeY + 2, 22, 18, [0, 0], 0.35); break;
    case 'sad': eyeOpen(lx, eyeY + 3, 22, 19, [0, 4], 0.3); eyeOpen(rx, eyeY + 5, 20, 18, [0, 4], 0.3); break;
    case 'disgusted': eyeOpen(lx, eyeY, 22, 12, [3, 0], 0.4); eyeOpen(rx, eyeY + 2, 25, 22, [3, 0]); break;
    default: // the signature asymmetric stare: one round eye, one droopy
      eyeOpen(lx, eyeY, 35, 32, [3, 1]); eyeOpen(rx, eyeY + 12, 31, 22, [3, 2], 0.4);
  }
  if (opt.glasses) {
    g.lineWidth = 5; g.strokeStyle = '#111';
    g.strokeRect(lx - 32, eyeY - 26, 64, 50); g.strokeRect(rx - 32, eyeY - 24, 64, 50);
    g.beginPath(); g.moveTo(lx + 32, eyeY - 6); g.lineTo(rx - 32, eyeY - 6); g.stroke();
  }

  // --- nose (single side stroke, like the source) -----------------------
  g.lineWidth = 4; g.beginPath(); g.moveTo(150, 250); g.quadraticCurveTo(158, 280, 146, 292); g.stroke();

  // --- facial hair ------------------------------------------------------
  const mouthY = 385;
  if (opt.facial === 'stubble' || opt.facial === 'beard') {
    const dens = opt.facial === 'beard' ? 2200 : 330;
    for (let i = 0; i < dens; i++) {
      const x = 12 + r() * (W - 24), y = 335 + Math.pow(r(), 0.7) * (H - 345);
      if (opt.facial === 'stubble' && Math.abs(y - mouthY) < 10 && Math.abs(x - W / 2) < 40) continue;
      g.fillStyle = `rgba(20,20,20,${0.55 + r() * 0.45})`;
      g.fillRect(x, y, 2 + r() * 1.5, 2 + r() * 2.5);
    }
  }
  if (opt.facial === 'mustache' || opt.facial === 'cop') {
    g.fillStyle = opt.hairColor; g.beginPath();
    g.moveTo(W / 2 - 50, mouthY - 8); g.quadraticCurveTo(W / 2, mouthY - 34, W / 2 + 50, mouthY - 8);
    g.quadraticCurveTo(W / 2, mouthY - 16, W / 2 - 50, mouthY - 8); g.fill();
    for (let i = 0; i < 260; i++) { g.fillStyle = 'rgba(20,20,20,0.7)'; g.fillRect(25 + r() * (W - 50), 330 + r() * 160, 2, 2); }
  }

  // --- mouth -------------------------------------------------------------
  g.strokeStyle = opt.lipstick ? '#B5302A' : '#111'; g.fillStyle = '#1a0c08'; g.lineWidth = 6;
  g.beginPath();
  switch (e) {
    case 'surprised': g.ellipse(W / 2, mouthY + 4, 12, 16, 0, 0, Math.PI * 2); g.fill(); break;
    case 'shocked': case 'scared': g.ellipse(W / 2, mouthY + 10, 20, 34, 0, 0, Math.PI * 2); g.fill(); break;
    case 'talk': g.ellipse(W / 2, mouthY + 4, 18, 9, 0, 0, Math.PI * 2); g.fill(); break;
    case 'happy': g.arc(W / 2, mouthY - 16, 30, Math.PI * 0.2, Math.PI * 0.8); g.stroke(); break;
    case 'smug': g.moveTo(W / 2 - 22, mouthY + 2); g.quadraticCurveTo(W / 2 + 10, mouthY + 6, W / 2 + 28, mouthY - 10); g.stroke(); break;
    case 'sad': g.arc(W / 2, mouthY + 26, 24, Math.PI * 1.2, Math.PI * 1.8); g.stroke(); break;
    case 'angry': case 'disgusted': g.moveTo(W / 2 - 26, mouthY + 6); g.lineTo(W / 2 - 8, mouthY - 2); g.lineTo(W / 2 + 10, mouthY + 4); g.lineTo(W / 2 + 26, mouthY - 2); g.stroke(); break;
    case 'dead': g.moveTo(W / 2 - 18, mouthY); g.lineTo(W / 2 + 18, mouthY); g.stroke(); g.fillStyle = '#C46'; g.fillRect(W / 2 + 4, mouthY, 12, 16); break;
    default: g.moveTo(W / 2 - 22, mouthY); g.lineTo(W / 2 + 20, mouthY + 1); g.stroke();
  }

  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  cache.set(key, tex);
  return tex;
}

// Side / back of the head: hair cap + stubble, so turning heads still reads right.
export function sideTexture(o = {}) {
  const opt = { skin: '#D9A877', hair: 'crew', hairColor: '#17181B', facial: 'stubble', seed: 5, back: false, ...o };
  const key = 'side' + JSON.stringify(opt);
  if (cache.has(key)) return cache.get(key);
  const W = 256, H = 512; const c = document.createElement('canvas'); c.width = W; c.height = H;
  const g = c.getContext('2d'); const r = rng(opt.seed);
  g.fillStyle = opt.skin; g.fillRect(0, 0, W, H);
  if (opt.hair !== 'bald') {
    const depth = opt.back ? (opt.hair === 'long' ? 360 : 200) : (opt.hair === 'long' ? 300 : 120);
    g.fillStyle = opt.hairColor; g.fillRect(0, 0, W, depth * 0.6);
    g.strokeStyle = opt.hairColor;
    for (let x = 0; x < W; x += 3) { g.lineWidth = 1 + r() * 2; g.beginPath(); g.moveTo(x, depth * 0.5); g.lineTo(x + (r() - 0.5) * 6, depth * (0.6 + r() * 0.45)); g.stroke(); }
  }
  if (!opt.back && (opt.facial === 'stubble' || opt.facial === 'beard')) {
    for (let i = 0; i < (opt.facial === 'beard' ? 1500 : 400); i++) { g.fillStyle = 'rgba(20,20,20,0.75)'; g.fillRect(r() * W * 0.6, 300 + r() * 212, 2, 3); }
  }
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  cache.set(key, tex); return tex;
}
