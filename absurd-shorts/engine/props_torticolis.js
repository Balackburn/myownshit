// « Le torticolis » (story 53, cycle 15): a man wakes up with a stiff neck, his head turned round to his back; since then he walks backwards to see
// where he goes; the prefecture issued him a driving licence back to front; he drives in reverse only; an osteopath put his head straight: it went
// round three times and locked looking at the sky; he presents the weather. Conventions as in props.js (metres, front +Z, pivot at the floor unless
// said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { mat, box, cyl, clamp01 } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const rnd = s => { let x = Math.sin(s * 127.1) * 43758.5453; return x - Math.floor(x); };
const unlit = pl => { pl.material = new THREE.MeshBasicMaterial({ map: pl.material.map, side: THREE.DoubleSide, toneMapped: false, transparent: !!pl.material.transparent, alphaTest: pl.material.transparent ? 0.05 : 0 }); pl.userData.noAO = true; return pl; };

export const TORTICOLIS_PROPS = {
  // The old pink French paper licence, written back to front (front +Z, pivot at its centre): o.s (1: 0.32 x 0.16 m, big enough to read in his hand),
  // the heading PERMIS DE CONDUIRE and every line mirrored, and for photo the back of a head (black hair, two ears, a collar). o.bright: unlit.
  reversePermit(o) {
    const s = o.s ?? 1, w = 0.32 * s, h = 0.16 * s;
    const mirror = (c, txt, x, y, font, color) => { c.save(); c.font = font; c.fillStyle = color; c.textAlign = 'center'; c.textBaseline = 'middle'; c.translate(x, y); c.scale(-1, 1); c.fillText(txt, 0, 0); c.restore(); };
    const face = canvasPlane(w, h, (c, W, H) => {
      c.fillStyle = '#F3B9C6'; c.fillRect(0, 0, W, H); c.strokeStyle = '#C97A8E'; c.lineWidth = H * 0.025; c.strokeRect(H * 0.03, H * 0.03, W - H * 0.06, H - H * 0.06);
      for (let i = 0; i < 40; i++) { c.strokeStyle = `rgba(200,110,140,${0.12 + 0.1 * rnd(i)})`; c.lineWidth = 1; c.beginPath(); c.arc(W * rnd(i + 1), H * rnd(i + 2), H * (0.1 + 0.3 * rnd(i + 3)), 0, TAU); c.stroke(); }   // the guilloché
      mirror(c, 'RÉPUBLIQUE FRANÇAISE', W * 0.5, H * 0.13, `bold ${H * 0.085}px Arial`, '#7A2E44');
      mirror(c, 'PERMIS DE CONDUIRE', W * 0.5, H * 0.28, `900 ${H * 0.14}px Arial`, '#5A1830');
      // the photo, on the right (on the left of a licence read the right way round): the back of a head
      const px = W * 0.66, py = H * 0.42, pw = W * 0.26, ph = H * 0.48; c.fillStyle = '#DCE6EE'; c.fillRect(px, py, pw, ph); c.strokeStyle = '#5A1830'; c.lineWidth = H * 0.012; c.strokeRect(px, py, pw, ph);
      c.fillStyle = '#2B2D42'; c.fillRect(px + pw * 0.2, py + ph * 0.86, pw * 0.6, ph * 0.14);   // the collar
      c.fillStyle = '#D9A066'; c.fillRect(px + pw * 0.4, py + ph * 0.7, pw * 0.2, ph * 0.18);   // the neck
      c.fillRect(px + pw * 0.18, py + ph * 0.36, pw * 0.08, ph * 0.18); c.fillRect(px + pw * 0.74, py + ph * 0.36, pw * 0.08, ph * 0.18);   // the ears
      c.fillStyle = '#1C1C22'; c.beginPath(); c.moveTo(px + pw * 0.24, py + ph * 0.72); c.lineTo(px + pw * 0.22, py + ph * 0.2); c.quadraticCurveTo(px + pw * 0.5, py + ph * 0.04, px + pw * 0.78, py + ph * 0.2);
      c.lineTo(px + pw * 0.76, py + ph * 0.72); c.quadraticCurveTo(px + pw * 0.5, py + ph * 0.8, px + pw * 0.24, py + ph * 0.72); c.fill();   // all hair, no face
      c.strokeStyle = '#3A3A48'; c.lineWidth = H * 0.008; for (let i = 0; i < 5; i++) { c.beginPath(); c.moveTo(px + pw * (0.32 + 0.09 * i), py + ph * 0.16); c.lineTo(px + pw * (0.3 + 0.1 * i), py + ph * 0.6); c.stroke(); }
      [['1. NOM', 0.5], ['2. PRÉNOM', 0.62], ['3. NÉ LE', 0.74], ['4. CATÉGORIE : B', 0.86]].forEach(([t, y]) => mirror(c, t, W * 0.32, H * y, `bold ${H * 0.07}px Arial`, '#5A1830'));
    }, { res: 768 });
    if (o.bright) unlit(face);
    const g = grp(at(box(w + 0.006, h + 0.006, 0.003, '#E9A3B4'), 0, 0, -0.002), face); face.position.z = 0.0025; return g;
  },

  // A TV weather map (front +Z, pivot at its centre, unlit like a screen): o.w (1.7) x o.h (1.05); a blue band MÉTÉO, a pale sea, the hexagon of France
  // in green with a darker rim, suns, clouds, a rain cloud and temperatures (o.temps)
  weatherMap(o) {
    const w = o.w ?? 1.7, h = o.h ?? 1.05, g = grp(at(box(w + 0.08, h + 0.08, 0.06, '#1E2430', { outline: 0.006 }), 0, 0, -0.035));
    const sun = (c, x, y, r) => { c.fillStyle = '#FFD23F'; c.strokeStyle = '#E8A21C'; c.lineWidth = r * 0.16; for (let i = 0; i < 10; i++) { const a = i * TAU / 10; c.beginPath(); c.moveTo(x + Math.cos(a) * r * 1.25, y + Math.sin(a) * r * 1.25); c.lineTo(x + Math.cos(a) * r * 1.65, y + Math.sin(a) * r * 1.65); c.stroke(); }
      c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill(); c.lineWidth = r * 0.1; c.stroke(); };
    const cloud = (c, x, y, r, rain) => { c.fillStyle = rain ? '#B8C0CC' : '#FFFFFF'; c.strokeStyle = '#7C8796'; c.lineWidth = r * 0.08;
      c.beginPath(); c.arc(x - r * 0.6, y + r * 0.1, r * 0.55, 0, TAU); c.arc(x, y - r * 0.2, r * 0.75, 0, TAU); c.arc(x + r * 0.65, y + r * 0.12, r * 0.5, 0, TAU); c.fill();
      c.beginPath(); c.arc(x - r * 0.6, y + r * 0.1, r * 0.55, PI * 0.5, PI * 1.5); c.stroke(); c.fillRect(x - r * 0.6, y + r * 0.1, r * 1.25, r * 0.55);
      if (rain) { c.strokeStyle = '#2F7FD6'; c.lineWidth = r * 0.14; for (let i = 0; i < 4; i++) { c.beginPath(); c.moveTo(x - r * 0.6 + i * r * 0.4, y + r * 0.8); c.lineTo(x - r * 0.75 + i * r * 0.4, y + r * 1.25); c.stroke(); } } };
    const pl = canvasPlane(w, h, (c, W, H) => {
      const gr = c.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#9CD3F2'); gr.addColorStop(1, '#6FB4E0'); c.fillStyle = gr; c.fillRect(0, 0, W, H);
      const cx = W * 0.5, cy = H * 0.58, R = H * 0.36, hex = [[-0.62, -0.78], [0.12, -0.98], [0.86, -0.52], [0.78, 0.42], [0.18, 0.95], [-0.72, 0.62], [-0.98, -0.12]];   // l'Hexagone, a little irregular
      c.fillStyle = '#7BC46B'; c.strokeStyle = '#3E7D3A'; c.lineWidth = H * 0.012; c.lineJoin = 'round'; c.beginPath(); hex.forEach(([x, y], i) => { const X = cx + x * R * 1.1, Y = cy + y * R; if (i) c.lineTo(X, Y); else c.moveTo(X, Y); }); c.closePath(); c.fill(); c.stroke();
      c.fillStyle = '#7BC46B'; c.beginPath(); c.ellipse(cx + R * 1.18, cy + R * 0.82, R * 0.07, R * 0.15, 0.3, 0, TAU); c.fill(); c.stroke();   // and the island
      sun(c, cx - R * 0.45, cy + R * 0.42, H * 0.055); sun(c, cx + R * 0.45, cy + R * 0.5, H * 0.05); cloud(c, cx - R * 0.35, cy - R * 0.45, H * 0.07, false); cloud(c, cx + R * 0.42, cy - R * 0.3, H * 0.065, true);
      c.font = `900 ${H * 0.075}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.lineWidth = H * 0.012; c.strokeStyle = '#1E2430';
      (o.temps || [['14°', -0.05, -0.62], ['21°', -0.62, 0.05], ['25°', 0.1, 0.25], ['18°', 0.62, 0.02]]).forEach(([t, x, y]) => { c.fillStyle = '#FFFFFF'; c.strokeText(t, cx + x * R, cy + y * R); c.fillText(t, cx + x * R, cy + y * R); });
      c.fillStyle = '#1F4E9E'; c.fillRect(0, 0, W, H * 0.16); c.fillStyle = '#FFFFFF'; c.font = `900 ${H * 0.11}px Arial`; c.fillText(o.title || 'MÉTÉO', W * 0.5, H * 0.085);
    }, { res: 1024 });
    unlit(pl); pl.position.z = 0.002; g.add(pl); return g;
  },

  // An anatomy poster in an osteopath's room (front +Z, pivot at its centre): o.w (0.6) x o.h (0.9), a cream sheet, a spine of stacked vertebrae under a
  // skull outline, the title o.title (OSTÉOPATHIE)
  spinePoster(o) {
    const w = o.w ?? 0.6, h = o.h ?? 0.9;
    const pl = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#F6F1E3'; c.fillRect(0, 0, W, H); c.strokeStyle = '#8A7A5A'; c.lineWidth = W * 0.012; c.strokeRect(W * 0.03, H * 0.02, W * 0.94, H * 0.96);
      c.fillStyle = '#2C4A8A'; c.font = `900 ${H * 0.055}px Arial`; c.textAlign = 'center'; c.fillText(o.title || 'OSTÉOPATHIE', W / 2, H * 0.08);
      c.strokeStyle = '#5A4A32'; c.fillStyle = '#EFE3C4'; c.lineWidth = W * 0.01; c.beginPath(); c.ellipse(W / 2, H * 0.19, W * 0.13, H * 0.075, 0, 0, TAU); c.fill(); c.stroke();   // the skull
      c.fillStyle = '#5A4A32'; c.beginPath(); c.arc(W * 0.45, H * 0.19, W * 0.03, 0, TAU); c.arc(W * 0.55, H * 0.19, W * 0.03, 0, TAU); c.fill();
      for (let i = 0; i < 17; i++) { const y = H * (0.29 + i * 0.037), ww = W * (0.1 + 0.05 * Math.sin(i * 0.35) + 0.035 * i / 17); c.fillStyle = i < 7 ? '#E8C9A0' : i < 12 ? '#E2BE90' : '#D9B07E';
        c.beginPath(); c.roundRect ? c.roundRect(W / 2 - ww / 2 + W * 0.02 * Math.sin(i * 0.4), y, ww, H * 0.028, H * 0.008) : c.rect(W / 2 - ww / 2, y, ww, H * 0.028); c.fill(); c.stroke(); }
      c.fillStyle = '#D9B07E'; c.beginPath(); c.moveTo(W * 0.4, H * 0.92); c.lineTo(W * 0.6, H * 0.92); c.lineTo(W * 0.5, H * 0.97); c.closePath(); c.fill(); c.stroke(); }, { res: 512 });
    const g = grp(at(box(w + 0.02, h + 0.02, 0.01, '#C9B98F'), 0, 0, -0.006), pl); pl.position.z = 0.001; return g;
  },

  // A bowl of cereal (pivot at its foot): o.r (0.075 m), white milk, orange rings floating
  cerealBowl(o) {
    const r = o.r ?? 0.075, g = grp(at(cyl(r, r * 0.62, r * 0.75, o.color || '#E85D4A', 14, { pivot: 'bottom', outline: 0.004 }), 0, 0, 0), at(cyl(r * 0.94, r * 0.94, 0.006, '#FBF8EE', 14), 0, r * 0.68, 0));
    for (let i = 0; i < 9; i++) { const a = i * 2.4, d = r * 0.62 * Math.sqrt((i + 0.5) / 9); g.add(at(new THREE.Mesh(new THREE.TorusGeometry(r * 0.12, r * 0.05, 4, 8), mat('#E8A33A')), Math.cos(a) * d, r * 0.7, Math.sin(a) * d, PI / 2, 0, 0)); }
    return g;
  },

  // A studio TV camera on a tripod (front +Z: the lens), pivot at the floor: a dark body, a lens, a viewfinder and a red tally light that is lit
  tvCamera(o) {
    const H = o.h ?? 1.35, g = grp();
    for (let i = 0; i < 3; i++) { const a = i * TAU / 3; g.add(at(cyl(0.018, 0.022, H, '#3A3F48', 6), Math.sin(a) * 0.25, H / 2 - 0.03, Math.cos(a) * 0.25, Math.cos(a) * 0.19, 0, -Math.sin(a) * 0.19)); }
    g.add(at(box(0.32, 0.26, 0.5, '#2A2E36', { outline: 0.008 }), 0, H + 0.13, 0), at(cyl(0.085, 0.1, 0.22, '#15171C', 12), 0, H + 0.13, 0.34, PI / 2, 0, 0), at(cyl(0.07, 0.07, 0.006, '#4A6E9A', 12), 0, H + 0.13, 0.452, PI / 2, 0, 0),
      at(box(0.18, 0.14, 0.12, '#2A2E36'), 0.12, H + 0.33, -0.12));
    const tally = new THREE.Mesh(new THREE.SphereGeometry(0.03, 8, 6), new THREE.MeshBasicMaterial({ color: '#FF2A2A', toneMapped: false })); tally.position.set(-0.1, H + 0.29, 0.2); g.add(tally);
    return g;
  },
};
