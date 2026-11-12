// « Le code-barres » (story 48): a man falls asleep in a supermarket; an employee sticks a price label on him; he beeps at the checkout (one man:
// 2,49 €); the manager scans him: in stock; he is put on promotion (minus fifty per cent: he shrinks by half), vacuum-packed for freshness, bought by a
// lady, brought back the next day (manufacturing defect), recalled by the manufacturer: he goes back to his mother, who asks for a refund.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, ease, clamp01 } from './style.js';
import { grp, at, label, canvasPlane } from './props.js';

const PI = Math.PI;
const list = v => [].concat(v ?? []);
const pulse = (t, ts, len) => list(ts).some(a => t >= a && t < a + len);
function liveCanvas(w, h, res, basic = true) {
  const c = document.createElement('canvas'); c.width = res; c.height = Math.max(8, Math.round(res * h / w));
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const m = basic ? new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide, toneMapped: false }) : new THREE.MeshLambertMaterial({ map: tex, side: THREE.DoubleSide });
  const pl = new THREE.Mesh(new THREE.PlaneGeometry(w, h), m); pl.userData.noAO = true; let last = null;
  return { pl, redraw: (key, fn) => { if (key === last) return; last = key; fn(c.getContext('2d'), c.width, c.height); tex.needsUpdate = true; } };
}
// a barcode drawn into a canvas box (x, y, w, h): bars of seeded widths, digits under them
function drawBarcode(c, x, y, w, h, seed = 7, digits = '3 760123 456789') {
  let s = seed; const rnd = () => { s = (s * 9301 + 49297) % 233280; return s / 233280; };
  c.fillStyle = '#111214'; let cx = x; const bh = h * 0.78;
  while (cx < x + w) { const bw = w * (0.008 + 0.022 * rnd()); if (rnd() > 0.42) c.fillRect(cx, y, bw, bh); cx += bw + w * (0.006 + 0.012 * rnd()); }
  c.font = `bold ${Math.round(h * 0.18)}px Arial`; c.textAlign = 'center'; c.textBaseline = 'alphabetic'; c.fillText(digits, x + w / 2, y + h * 0.99);
}

export const CODEBARRE_PROPS = {
  // A hand-held price-label gun, front +Z (the nozzle), held by its handle (userData.grip): an orange body, the label roll on top, a black trigger.
  // o.clackAt [t...]: the trigger snaps in and the body jolts (a label goes on).
  priceGun(o) {
    const g = grp(), body = grp(); g.add(body);
    body.add(at(box(0.07, 0.11, 0.24, o.color || '#E8742A', { outline: 0.006 }), 0, 0.09, 0.02), at(box(0.05, 0.05, 0.06, '#2A2C31'), 0, 0.08, 0.16));
    body.add(at(cyl(0.055, 0.055, 0.06, '#F4F2EA', 14), 0, 0.17, -0.03, 0, 0, PI / 2), at(cyl(0.02, 0.02, 0.065, '#9AA1A9', 8), 0, 0.17, -0.03, 0, 0, PI / 2));
    const handle = at(box(0.05, 0.15, 0.06, '#2A2C31', { outline: 0.005 }), 0, -0.02, -0.06, 0.25, 0, 0); body.add(handle);
    const trig = grp(at(box(0.02, 0.07, 0.025, '#111214'), 0, -0.03, 0)); trig.position.set(0, 0.03, 0.0); body.add(trig);
    g.userData.update = t => { const on = pulse(t, o.clackAt, 0.08); trig.rotation.x = on ? -0.5 : 0; body.rotation.x = on ? -0.12 : 0; body.position.z = on ? 0.012 : 0; };
    g.userData.update(0); g.userData.grip = [0, -0.02, -0.06]; return g;
  },
  // A price label: a white sticker o.w (0.16) × o.h (0.1) with a barcode and the price in red (o.price '2,49 €'), front +Z, origin at its centre.
  // o.bright: unlit (a sticker that must read on a face in the shade).
  barcodeLabel(o) {
    const w = o.w ?? 0.16, h = o.h ?? 0.1, pl = canvasPlane(w, h, (c, W, H) => {
      c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.strokeStyle = 'rgba(0,0,0,0.35)'; c.lineWidth = W * 0.012; c.strokeRect(W * 0.01, W * 0.01, W * 0.98, H - W * 0.02);
      drawBarcode(c, W * 0.07, H * 0.1, W * 0.86, H * 0.5, o.seed ?? 7, o.digits || '3 760123 456789');
      c.fillStyle = o.ink || '#C8202A'; c.font = `900 ${Math.round(H * 0.3)}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.price || '2,49 €', W / 2, H * 0.8);
    }, { res: 512 });
    if (o.bright) pl.material = new THREE.MeshBasicMaterial({ map: pl.material.map, side: THREE.DoubleSide });
    return grp(at(box(w + 0.006, h + 0.006, 0.003, '#E6E3DA'), 0, 0, -0.002), pl);
  },
  // The anti-theft gate at a shop's exit: two pale pillars o.gap (1.1 m) apart along X, origin between their feet; at each top a red lamp that flashes
  // at o.beepAt [t...] for o.flash (0.5 s), blinking.
  securityGate(o) {
    const gap = o.gap ?? 1.1, g = grp(), lamps = [], red = new THREE.MeshBasicMaterial({ color: '#FF2A1E', toneMapped: false }), off = mat('#7A1E1A');
    for (const sx of [-1, 1]) {
      const x = sx * gap / 2; g.add(at(box(0.14, 0.05, 0.46, '#8F949B'), x, 0.025, 0), at(box(0.1, 1.5, 0.4, '#EDEBE6', { pivot: 'bottom', outline: 0.006 }), x, 0.05, 0));
      g.add(at(box(0.104, 0.5, 0.3, '#D7D4CC'), x, 0.85, 0));
      const on = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.12, 0.41), red); on.position.set(x, 1.6, 0); on.userData.noAO = true; const of = at(box(0.11, 0.12, 0.41, '', { material: off }), x, 1.6, 0);
      g.add(on, of); lamps.push([on, of]);
    }
    g.userData.update = t => { const fl = (o.flash ?? 0.5), act = list(o.beepAt).find(a => t >= a && t < a + fl), blink = act != null && Math.floor((t - act) * 12) % 2 === 0;
      for (const [on, of] of lamps) { on.visible = blink; of.visible = !blink; } };
    g.userData.update(0); return g;
  },
  // A small screen on a short stand (a checkout's customer display, a manager's tablet), front +Z, origin at its foot: o.w (0.5) × o.h (0.32), o.stand
  // (0.3 m; 0 = no stand). o.pages [[t, ['LINE', 'LINE'], {face: true, big: 1}], ...]: what it shows from t (the first line big, the next ones under it;
  // face: a little pictogram of the man on the left). o.dark: dark screen with pale green type (else white with dark type).
  lcdScreen(o) {
    const w = o.w ?? 0.5, h = o.h ?? 0.32, st = o.stand ?? 0.3, g = grp(), dark = o.dark !== false;
    if (st > 0) g.add(at(box(0.05, st, 0.05, '#3A3D44', { pivot: 'bottom' }), 0, 0, 0), at(box(0.22, 0.02, 0.16, '#3A3D44'), 0, 0.01, 0));
    g.add(at(box(w + 0.05, h + 0.05, 0.05, '#1E2024', { outline: 0.006 }), 0, st + h / 2, -0.03));
    const L = liveCanvas(w, h, 512); L.pl.position.set(0, st + h / 2, 0.0); g.add(L.pl);
    const pages = o.pages || [[0, ['']]];
    g.userData.update = t => { let i = 0; pages.forEach((p, j) => { if (t >= p[0]) i = j; });
      L.redraw(i, (c, W, H) => { const [, lines, opt = {}] = pages[i];
        c.fillStyle = dark ? '#0E1A14' : '#F7F7F4'; c.fillRect(0, 0, W, H); const ink = dark ? '#8CFFC0' : '#14161A', x0 = opt.face ? W * 0.36 : W * 0.06;
        if (opt.face) { const fx = W * 0.05, fy = H * 0.2, fw = W * 0.24, fh = H * 0.62; c.fillStyle = '#1E2A44'; c.fillRect(fx, fy + fh * 0.62, fw, fh * 0.38); c.fillStyle = '#D9A066'; c.fillRect(fx + fw * 0.18, fy, fw * 0.64, fh * 0.62);
          c.fillStyle = '#111214'; c.fillRect(fx + fw * 0.18, fy, fw * 0.64, fh * 0.1); c.fillRect(fx + fw * 0.3, fy + fh * 0.26, fw * 0.1, fh * 0.08); c.fillRect(fx + fw * 0.6, fy + fh * 0.26, fw * 0.1, fh * 0.08); c.fillStyle = '#C8202A'; c.fillRect(fx + fw * 0.46, fy + fh * 0.62, fw * 0.08, fh * 0.3); }
        c.textAlign = 'left'; c.textBaseline = 'middle'; let y = H * 0.3;
        lines.forEach((ln, k) => { const big = k === 0 ? (opt.big ?? 1) : 0.62, fs = Math.round(H * 0.2 * big); c.font = `900 ${fs}px Arial`; c.fillStyle = k === 0 || !opt.accent ? ink : opt.accent;
          let s = fs; while (c.measureText(ln).width > W - x0 - W * 0.04 && s > 8) { s -= 2; c.font = `900 ${s}px Arial`; } c.fillText(ln, x0, y); y += H * (k === 0 ? 0.3 : 0.24); }); }); };
    g.userData.update(0); return g;
  },
  // A promotion sticker: a yellow starburst o.r (0.22 m) with red type (o.text '-50 %'), front +Z, origin at its centre; o.bright unlit.
  starSticker(o) {
    const r = o.r ?? 0.22, pl = canvasPlane(2 * r, 2 * r, (c, W, H) => { c.clearRect(0, 0, W, H); const n = 14; c.beginPath();
      for (let i = 0; i < 2 * n; i++) { const a = i * PI / n - PI / 2, rr = (i % 2 ? 0.8 : 1.0) * W * 0.48; c.lineTo(W / 2 + rr * Math.cos(a), H / 2 + rr * Math.sin(a)); } c.closePath();
      c.fillStyle = o.color || '#FFD21F'; c.fill(); c.lineWidth = W * 0.025; c.strokeStyle = '#C8202A'; c.stroke();
      c.fillStyle = o.ink || '#C8202A'; c.textAlign = 'center'; c.textBaseline = 'middle'; const t = o.text || '-50 %'; let fs = Math.round(H * 0.3); c.font = `900 ${fs}px Arial`;
      while (c.measureText(t).width > W * 0.72 && fs > 8) { fs -= 2; c.font = `900 ${fs}px Arial`; } c.fillText(t, W / 2, H * 0.53); }, { res: 512, transparent: true });
    pl.material = new THREE.MeshBasicMaterial({ map: pl.material.map, transparent: true, alphaTest: 0.05, side: THREE.DoubleSide, toneMapped: !o.bright }); pl.userData.noAO = true;
    return grp(pl);
  },
  // A vacuum pack: a clear plastic skin round a thing o.w (0.9) × o.h (2.4) × o.d (0.6), pivot at its foot, front +Z: shiny edges, a white label
  // (o.label 'SOUS VIDE'). o.tight [[t, k], ...] (eased): the skin sucked in to k of its size across (0.62: tight on him), with crinkles when tight.
  vacuumBag(o) {
    const w = o.w ?? 0.9, h = o.h ?? 2.4, d = o.d ?? 0.6, g = grp(), skin = grp(); g.add(skin);
    const film = new THREE.MeshLambertMaterial({ color: '#DDEFF6', transparent: true, opacity: o.opacity ?? 0.28, depthWrite: false, side: THREE.DoubleSide });
    skin.add(at(new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), film), 0, 0.5, 0));
    const edge = mat('#F4FAFC'); for (const [x, z] of [[-0.5, -0.5], [0.5, -0.5], [-0.5, 0.5], [0.5, 0.5]]) skin.add(at(new THREE.Mesh(new THREE.BoxGeometry(0.012, 1, 0.012), edge), x, 0.5, z));
    const crink = []; for (let i = 0; i < 9; i++) { const m = new THREE.Mesh(new THREE.BoxGeometry(0.004, 0.08, 0.3), edge); m.position.set((i % 3 - 1) * 0.3, 0.15 + 0.1 * i, 0.5); m.rotation.z = 0.6 * ((i * 7) % 5 - 2) / 2; m.visible = false; skin.add(m); crink.push(m); }
    skin.add(at(new THREE.Mesh(new THREE.BoxGeometry(1.04, 0.03, 1.04), edge), 0, 1.0, 0), at(new THREE.Mesh(new THREE.BoxGeometry(1.04, 0.03, 1.04), edge), 0, 0.0, 0));   // the welded seams
    if (o.label !== false) { const lb = canvasPlane(0.34, 0.16, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.fillStyle = '#1E5BB8'; c.fillRect(0, 0, W, H * 0.3); c.fillStyle = '#FFFFFF'; c.font = `900 ${Math.round(H * 0.22)}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.brand || 'FRAÎCHEUR', W / 2, H * 0.16);
        c.fillStyle = '#14161A'; c.font = `900 ${Math.round(H * 0.3)}px Arial`; c.fillText(o.label || 'SOUS VIDE', W / 2, H * 0.62); }, { res: 256 }); lb.position.set(0, o.labelY ?? 0.42, 0.502); lb.scale.set(1 / w, 1 / h, 1); lb.userData.noAO = true; skin.add(lb); }
    const keysT = o.tight || [[0, 1]];
    g.userData.update = t => { let k = keysT[0][1]; for (let i = 1; i < keysT.length; i++) { const [t0, v0] = keysT[i - 1], [t1, v1] = keysT[i]; if (t >= t1) k = v1; else if (t > t0) { k = v0 + (v1 - v0) * ease.inOut(clamp01((t - t0) / (t1 - t0))); break; } else break; }
      skin.scale.set(w * k, h * (0.97 + 0.03 * k), d * k); crink.forEach(m => { m.visible = k < 0.85; }); };
    g.userData.update(0); return g;
  },
  // A scanner's beam: a thin red rod from the prop's origin along o.vec [dx, dy, dz] (metres), unlit, a little flicker; give it visible keys.
  laserBeam(o) {
    const v = new THREE.Vector3(...(o.vec || [0, 0, 1])), L = v.length() || 1, r = o.r ?? 0.01, g = grp();
    const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, L, 6), new THREE.MeshBasicMaterial({ color: o.color || '#FF2A1E', toneMapped: false }));
    m.position.copy(v).multiplyScalar(0.5); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), v.clone().normalize()); m.userData.noAO = true; g.add(m);
    const dot = new THREE.Mesh(new THREE.SphereGeometry(r * 3.2, 8, 6), new THREE.MeshBasicMaterial({ color: '#FF6A50', toneMapped: false })); dot.position.copy(v); dot.userData.noAO = true; g.add(dot);
    g.userData.update = t => { const k = 0.85 + 0.15 * Math.sin(t * 90); m.scale.set(k, 1, k); };
    g.userData.update(0); return g;
  },
  // A service counter (returns desk): a counter o.w (1.8) long, its top at 1.0, a sign over it on two rods (o.text 'RETOURS', o.sub 'SERVICE CLIENTS'),
  // front +Z, origin at the foot of its front face.
  serviceDesk(o) {
    const w = o.w ?? 1.8, g = grp(at(box(w, 1.0, 0.6, o.color || '#D9D3C4', { pivot: 'bottom', outline: 0.006 }), 0, 0, -0.3), at(box(w + 0.08, 0.05, 0.7, '#8C6A4A'), 0, 1.02, -0.3));
    g.add(at(box(w * 0.9, 0.3, 0.02, o.band || '#1E5BB8'), 0, 0.62, 0.005));
    const sw = Math.min(1.6, w * 0.9); g.add(at(box(sw + 0.1, 0.5, 0.05, '#1E5BB8', { outline: 0.006 }), 0, 2.45, -0.45), at(label(o.text || 'RETOURS', sw, 0.3, { bg: '#1E5BB8', fg: '#FFFFFF', wrap: false }), 0, 2.5, -0.42));
    if (o.sub !== false) g.add(at(label(o.sub || 'SERVICE CLIENTS', sw * 0.8, 0.12, { bg: '#1E5BB8', fg: '#DCE8FF', wrap: false }), 0, 2.29, -0.42));
    for (const sx of [-1, 1]) g.add(at(cyl(0.012, 0.012, 0.8, '#7A8088', 6, { pivot: 'bottom' }), sx * sw * 0.42, 2.7, -0.45));
    return g;
  },
};
