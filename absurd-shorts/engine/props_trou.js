// Props for « Le trou » (story 37): a real hole in the pavement (the set cuts its ground with the same outline), the town hall's
// official map and its "NULLE PART" board, the car-park style COMPLET sign.
// Conventions as in props.js (metres, front +Z, pivot at the floor); every motion is a pure function of t.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, sphere, rng, ease, clamp01 } from './style.js';
import { grp, at, mesh, canvasPlane } from './props.js';

const PI = Math.PI, TAU = PI * 2;

// the broken edge of the hole: a jittered polygon [[x, z], ...] round the origin (shared by the ground cut and the shaft)
export function holeOutline(r = 0.9, seed = 5, n = 16) {
  const rr = rng(seed), pts = [];
  for (let i = 0; i < n; i++) { const a = i / n * TAU, k = r * (0.9 + 0.2 * rr()); pts.push([Math.cos(a) * k, Math.sin(a) * k]); }
  return pts;
}

export const TROU_PROPS = {
  // the shaft under a hole in the ground: earth walls that darken with depth, a slab section at the top, broken paving round the edge, cracks
  streetHole(o) {
    const r = o.r ?? 0.9, depth = o.depth ?? 6, pts = holeOutline(r, o.seed ?? 5), n = pts.length, g = grp(), rows = [0, -0.16, -0.17, -0.7, -1.6, -3.0, -depth];
    const cols = ['#C9BFAE', '#B3A896', '#8C6F52', '#6E5540', '#3E3026', '#17120E', '#060504'].map(c => new THREE.Color(c));
    const pos = [], col = [], idx = [];
    for (let i = 0; i <= n; i++) { const [x, z] = pts[i % n]; rows.forEach((y, k) => { pos.push(x, y, z); const c = cols[k]; col.push(c.r, c.g, c.b); }); }
    const R = rows.length; for (let i = 0; i < n; i++) for (let k = 0; k < R - 1; k++) { const a = i * R + k, b = (i + 1) * R + k; idx.push(a, a + 1, b, b, a + 1, b + 1); }
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); geo.setAttribute('color', new THREE.Float32BufferAttribute(col, 3)); geo.setIndex(idx);
    const wall = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.DoubleSide })); wall.castShadow = false; wall.userData.noAO = true; g.add(wall);
    const bot = new THREE.Mesh(new THREE.CircleGeometry(r * 1.3, 12).rotateX(-PI / 2), new THREE.MeshBasicMaterial({ color: '#050403' })); bot.position.y = -depth + 0.01; g.add(bot);
    const rr = rng((o.seed ?? 5) + 3), slab = o.slab || '#E4D6BE';
    for (let i = 0; i < n; i++) {   // broken paving: chunks lifted round the edge
      if (rr() < 0.3) continue; const [x, z] = pts[i], a = Math.atan2(z, x), s = 0.14 + 0.16 * rr();
      const m = box(s, 0.05 + 0.04 * rr(), s * (0.6 + 0.6 * rr()), new THREE.Color(slab).multiplyScalar(0.84 + 0.14 * rr()).getStyle(), { outline: 0.02 });
      m.position.set(x * 1.07, 0.03, z * 1.07); m.rotation.set((rr() - 0.5) * 0.5, -a + rr(), (rr() - 0.5) * 0.5); g.add(m);
    }
    for (let i = 0; i < 9; i++) {   // cracks running away from the hole
      const a = rr() * TAU, L = 0.5 + 0.9 * rr(), m = box(L, 0.004, 0.025, '#5A5148'); m.castShadow = false;
      m.position.set(Math.cos(a) * (r + L / 2 + 0.02), 0.011, Math.sin(a) * (r + L / 2 + 0.02)); m.rotation.y = -a + (rr() - 0.5) * 0.4; g.add(m);
      if (rr() < 0.6) { const L2 = L * 0.5, m2 = box(L2, 0.004, 0.02, '#5A5148'); m2.castShadow = false; const b = a + (rr() < 0.5 ? 0.7 : -0.7); m2.position.set(Math.cos(a) * (r + L * 0.7) + Math.cos(b) * L2 / 2, 0.011, Math.sin(a) * (r + L * 0.7) + Math.sin(b) * L2 / 2); m2.rotation.y = -b; g.add(m2); }
    }
    return g;
  },

  // a tax bill that says there is nothing to pay: IMPÔTS, the address NULLE PART, À PAYER : 0 € (front +Z, origin at its centre)
  taxBill(o) {
    const w = o.w ?? 0.5, h = o.h ?? 0.62;
    const c = canvasPlane(w, h, (g, W, H) => {
      g.fillStyle = '#FBF8EE'; g.fillRect(0, 0, W, H); g.fillStyle = '#2A4B9B'; g.fillRect(0, 0, W, H * 0.2); g.fillStyle = '#F4F1E8'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.font = `900 ${H * 0.13}px Arial`; g.fillText('IMPÔTS', W / 2, H * 0.105);
      g.fillStyle = '#1B1B1E'; g.font = `bold ${H * 0.062}px Arial`; g.fillText('ADRESSE : NULLE PART', W / 2, H * 0.3);
      g.fillStyle = '#6A6A70'; for (let i = 0; i < 3; i++) g.fillRect(W * 0.14, H * (0.38 + i * 0.045), W * (0.72 - i * 0.12), H * 0.014);
      g.fillStyle = '#1B1B1E'; g.font = `bold ${H * 0.075}px Arial`; g.fillText('À PAYER', W / 2, H * 0.58); g.fillStyle = '#C8202A'; g.font = `900 ${H * 0.27}px Arial`; g.fillText('0 €', W / 2, H * 0.8);
      g.strokeStyle = '#1B1B1E'; g.lineWidth = W * 0.012; g.strokeRect(W * 0.03, H * 0.024, W * 0.94, H * 0.952);
    }, { res: 512 });
    const g = grp(at(box(w, h, 0.006, '#FBF8EE'), 0, 0, -0.004), c); g.userData.grip = [0, -h / 2 + 0.03, 0]; return g;
  },

  // the form the clerk has just stamped: a file sheet « DOSSIER : LE TROU » with a big red INEXISTANT across it (front +Z, origin at its centre)
  stampedForm(o) {
    const w = o.w ?? 0.46, h = o.h ?? 0.58;
    const c = canvasPlane(w, h, (g, W, H) => {
      g.fillStyle = '#FBF8EE'; g.fillRect(0, 0, W, H); g.fillStyle = '#1B2A4A'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.font = `900 ${H * 0.085}px Arial`; g.fillText(o.title || 'DOSSIER : LE TROU', W / 2, H * 0.1);
      g.fillRect(W * 0.1, H * 0.165, W * 0.8, H * 0.012); g.fillStyle = '#8A8A90'; for (let i = 0; i < 7; i++) g.fillRect(W * 0.12, H * (0.25 + i * 0.085), W * (i % 3 === 2 ? 0.5 : 0.76), H * 0.02);
      g.save(); g.translate(W * 0.5, H * 0.56); g.rotate(-0.22); g.strokeStyle = '#C8202A'; g.lineWidth = H * 0.022; g.strokeRect(-W * 0.44, -H * 0.1, W * 0.88, H * 0.2); g.fillStyle = '#C8202A'; g.font = `900 ${H * 0.125}px Arial`; g.fillText(o.text || 'INEXISTANT', 0, H * 0.008); g.restore();
      g.strokeStyle = '#1B1B1E'; g.lineWidth = W * 0.012; g.strokeRect(W * 0.02, H * 0.016, W * 0.96, H * 0.968);
    }, { res: 512 });
    return grp(at(box(w, h, 0.006, '#FBF8EE'), 0, 0, -0.004), c);
  },

  // the town hall's official map: streets and blocks, and nothing where the hole is (o.stamp: a green "AUCUN TROU" across it)
  officialMap(o) {
    const w = o.w ?? 1.5, h = o.h ?? 1.05;
    const c = canvasPlane(w, h, (g, W, H) => {
      g.fillStyle = '#EFE6CF'; g.fillRect(0, 0, W, H); g.fillStyle = '#D9E3C6'; g.fillRect(W * 0.62, H * 0.5, W * 0.3, H * 0.3);
      g.strokeStyle = '#FBF8EE'; g.lineCap = 'round';
      for (const [x0, y0, x1, y1, lw] of [[0, 0.3, 1, 0.36, 0.05], [0, 0.72, 1, 0.66, 0.045], [0.25, 0.14, 0.3, 1, 0.045], [0.6, 0.14, 0.56, 1, 0.05], [0.84, 0.14, 0.88, 1, 0.03], [0, 0.52, 0.6, 0.5, 0.025]]) { g.lineWidth = W * lw; g.beginPath(); g.moveTo(W * x0, H * y0); g.lineTo(W * x1, H * y1); g.stroke(); }
      g.fillStyle = '#D8C9A6'; const r = rng(31); for (let i = 0; i < 26; i++) { const x = r() * 0.9 + 0.03, y = 0.17 + r() * 0.78; g.fillRect(W * x, H * y, W * (0.04 + 0.05 * r()), H * (0.03 + 0.04 * r())); }
      g.fillStyle = '#2A4B9B'; g.fillRect(0, 0, W, H * 0.13); g.fillStyle = '#F4F1E8'; g.font = `bold ${H * 0.085}px Arial`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(o.title || 'PLAN OFFICIEL', W / 2, H * 0.07);
      if (o.stamp !== false) { g.save(); g.translate(W * 0.5, H * 0.58); g.rotate(-0.16); g.strokeStyle = '#2E8B4A'; g.lineWidth = H * 0.022; g.strokeRect(-W * 0.34, -H * 0.11, W * 0.68, H * 0.22); g.fillStyle = '#2E8B4A'; g.font = `900 ${H * 0.15}px Arial`; g.fillText(o.stamp || 'AUCUN TROU', 0, H * 0.012); g.restore(); }
    }, { res: 1024 });
    return grp(at(box(w + 0.08, h + 0.08, 0.04, '#8A6A45', { outline: 0.006 }), 0, 0, 0), at(c, 0, 0, 0.024));
  },

  // cork board "NULLE PART": the four missing people as ID photos (o.n shown; o.at: times at which each one pops in)
  nowhereBoard(o) {
    const w = o.w ?? 1.5, h = o.h ?? 1.0, g = grp(at(box(w + 0.08, h + 0.08, 0.04, '#8A6A45', { outline: 0.006 }), 0, 0, 0), at(box(w, h, 0.01, '#C9A06A'), 0, 0, 0.022));
    g.add(at(canvasPlane(w * 0.9, h * 0.24, (c, W, H) => { c.fillStyle = '#F4F1E8'; c.fillRect(0, 0, W, H); c.fillStyle = '#1B1B1E'; c.font = `900 ${H * 0.7}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.title || 'NULLE PART', W / 2, H * 0.54); }, { res: 512 }), 0, h * 0.33, 0.03));
    const who = [{ skin: '#D9A877', suit: '#1F2E47', tie: '#C8202A' }, { skin: '#E2B48A', suit: '#E8C23A', hat: '#2A4B9B' }, { skin: '#C98E62', suit: '#B5302A', hat: '#E8B93A' }, { skin: '#E6BE98', suit: '#2B2B30', sash: true }], ph = [];
    who.forEach((p, i) => {
      const c = canvasPlane(0.26, 0.33, (c2, W, H) => {
        c2.fillStyle = '#FFFFFF'; c2.fillRect(0, 0, W, H); c2.fillStyle = '#DCE8F2'; c2.fillRect(W * 0.07, H * 0.06, W * 0.86, H * 0.88);
        c2.fillStyle = p.suit; c2.fillRect(W * 0.18, H * 0.74, W * 0.64, H * 0.2);
        if (p.tie) { c2.fillStyle = '#F2F2EC'; c2.fillRect(W * 0.43, H * 0.74, W * 0.14, H * 0.2); c2.fillStyle = p.tie; c2.fillRect(W * 0.47, H * 0.76, W * 0.06, H * 0.18); }
        if (p.sash) { c2.save(); c2.beginPath(); c2.rect(W * 0.18, H * 0.74, W * 0.64, H * 0.2); c2.clip(); c2.translate(W * 0.5, H * 0.84); c2.rotate(-0.7); ['#2A4B9B', '#F4F1E8', '#C8202A'].forEach((col, k) => { c2.fillStyle = col; c2.fillRect(-W * 0.6, (k - 1.5) * H * 0.045, W * 1.2, H * 0.045); }); c2.restore(); }
        c2.fillStyle = p.skin; c2.fillRect(W * 0.33, H * 0.2, W * 0.34, H * 0.56); c2.fillStyle = '#1A1A1A'; c2.fillRect(W * 0.31, H * 0.17, W * 0.38, H * 0.09);
        if (p.hat) { c2.fillStyle = p.hat; c2.fillRect(W * 0.27, H * 0.1, W * 0.46, H * 0.13); c2.fillRect(W * 0.24, H * 0.21, W * 0.52, H * 0.035); }
        c2.fillStyle = '#1A1A1A'; c2.fillRect(W * 0.4, H * 0.42, W * 0.05, H * 0.035); c2.fillRect(W * 0.56, H * 0.42, W * 0.05, H * 0.035); c2.fillRect(W * 0.43, H * 0.62, W * 0.15, H * 0.022);
      }, { res: 256 });
      const pin = sphere(0.016, '#C8202A', 0), q = grp(c, at(pin, 0, 0.14, 0.012)); q.position.set((i - 1.5) * w * 0.235, -h * 0.13, 0.034); q.rotation.z = [0.06, -0.05, 0.04, -0.07][i]; g.add(q); ph.push(q);
    });
    const ats = o.at || [], n = o.n ?? 4;
    g.userData.update = t => ph.forEach((q, i) => { const a = ats[i]; if (i >= n) { q.visible = false; return; } if (a == null) { q.visible = true; q.scale.setScalar(1); return; } q.visible = t >= a; if (q.visible) q.scale.setScalar(ease.outBack(clamp01((t - a) / 0.22))); });
    g.userData.update(0); return g;
  },

  // a car-park style sign on a post: a dark panel whose lamps spell COMPLET (lit red from o.onAt, with a blink)
  completSign(o) {
    const g = grp(), ph = o.h ?? 2.5, w = o.w ?? 1.25, h = o.ph ?? 0.44;
    g.add(at(cyl(0.045, 0.055, ph, '#3A3F47', 8, { pivot: 'bottom' }), 0, 0, 0), at(box(0.3, 0.05, 0.3, '#2B2F36'), 0, 0.025, 0), at(box(w + 0.1, h + 0.1, 0.12, '#22262C', { outline: 0.012 }), 0, ph + h / 2, 0));
    const face = (text, col, glow) => { const c = canvasPlane(w, h, (c2, W, H) => { c2.fillStyle = '#0D0F12'; c2.fillRect(0, 0, W, H); c2.fillStyle = col; let fs = H * 0.66; c2.font = `900 ${fs}px Arial`; const tw = c2.measureText(text).width; if (tw > W * 0.86) fs *= W * 0.86 / tw; c2.font = `900 ${fs}px Arial`; c2.textAlign = 'center'; c2.textBaseline = 'middle'; c2.fillText(text, W / 2, H * 0.55);
      c2.fillStyle = '#0D0F12'; for (let y = 0; y < H; y += H / 9) c2.fillRect(0, y, W, H / 40); for (let x = 0; x < W; x += W / 34) c2.fillRect(x, 0, W / 160, H); }, { res: 512, emissive: glow }); c.position.set(0, ph + h / 2, 0.062); c.userData.noAO = true; return c; };
    const off = face(o.textOff || 'LIBRE', '#2C5A3A', 0.25), on = face(o.text || 'COMPLET', '#FF4A36', 1.0); g.add(off, on);
    const onAt = o.onAt ?? 0;
    g.userData.update = t => { const u = t - onAt, lit = u >= 0 && !(u > 0.08 && u < 0.16) && !(u > 0.24 && u < 0.3); on.visible = lit; off.visible = u < 0; };   // the lamps stutter on: dark between two flashes, never LIBRE again
    g.userData.update(o.onAt == null ? 1 : 0); return g;
  },

  // the light that falls into the hole (cross-section set): a soft pale column, a few motes drifting in it
  holeLight(o) {
    const w = o.w ?? 1.5, h = o.h ?? 4.6, g = grp();
    const c = canvasPlane(w, h, (c2, W, H) => { const gr = c2.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, 'rgba(255,246,214,0.5)'); gr.addColorStop(0.6, 'rgba(255,246,214,0.16)'); gr.addColorStop(1, 'rgba(255,246,214,0.0)'); c2.fillStyle = gr; c2.fillRect(0, 0, W, H);
      const gx = c2.createLinearGradient(0, 0, W, 0); gx.addColorStop(0, 'rgba(0,0,0,1)'); gx.addColorStop(0.25, 'rgba(0,0,0,0)'); gx.addColorStop(0.75, 'rgba(0,0,0,0)'); gx.addColorStop(1, 'rgba(0,0,0,1)'); c2.globalCompositeOperation = 'destination-out'; c2.fillStyle = gx; c2.fillRect(0, 0, W, H); }, { res: 256, transparent: true });
    c.material = new THREE.MeshBasicMaterial({ map: c.material.map, transparent: true, depthWrite: false, side: THREE.DoubleSide }); c.position.y = h / 2; c.userData.noAO = true; c.castShadow = false; g.add(c);
    const r = rng(9), motes = []; for (let i = 0; i < 14; i++) { const m = new THREE.Mesh(new THREE.PlaneGeometry(0.02, 0.02), new THREE.MeshBasicMaterial({ color: '#FFF6D6', transparent: true, opacity: 0.7, depthWrite: false })); m.userData.noAO = true; motes.push({ m, x: (r() - 0.5) * w * 0.6, y: r() * h, p: r() * TAU, v: 0.05 + 0.08 * r() }); g.add(m); }
    g.userData.update = t => motes.forEach(q => { q.m.position.set(q.x + 0.06 * Math.sin(t * 0.7 + q.p), (q.y - t * q.v + 100 * h) % h, 0.02 + 0.05 * Math.sin(t * 0.9 + q.p * 2)); });
    g.userData.update(0); return g;
  },
};
