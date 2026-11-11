// « L'ombre » (story 42): a man whose shadow is late, then leaves him; the town hall answers that she is of age.
// Conventions as in props.js (metres, front +Z, pivot at the floor); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, rng, ease, clamp01 } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI, INK = '#262833';
const txt = (g, s, x, y, px, color = '#1B1B1E', weight = '900') => { g.fillStyle = color; g.font = `${weight} ${px}px Arial`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(s, x, y); };
const fit = (g, s, w, px, weight = '900') => { g.font = `${weight} ${px}px Arial`; const m = g.measureText(s).width; return m > w ? px * w / m : px; };
const flat = (color, o = {}) => new THREE.MeshBasicMaterial({ color, toneMapped: false, ...o });
// the outline of a man of the series (a tall box of a head with a tuft, square shoulders, a tie) drawn on a canvas: feet at (x, y), h pixels tall.
// kind: 'man' | 'tall' | 'wide' | 'kid' | 'dog'
function drawFigure(c, x, y, h, col = INK, kind = 'man') {
  c.fillStyle = col; const R = (a, b, w, hh) => c.fillRect(x + a * h, y - b * h - hh * h, w * h, hh * h);
  if (kind === 'dog') { R(-0.3, 0.12, 0.6, 0.22); R(-0.3, 0, 0.07, 0.14); R(-0.12, 0, 0.07, 0.14); R(0.08, 0, 0.07, 0.14); R(0.23, 0, 0.07, 0.14); R(0.2, 0.3, 0.26, 0.2); R(0.4, 0.34, 0.12, 0.1); R(0.22, 0.48, 0.06, 0.1); R(-0.42, 0.26, 0.14, 0.05); return; }
  const k = kind === 'tall' ? 0.72 : kind === 'wide' ? 1.5 : kind === 'kid' ? 1.15 : 1;   // how wide for its height
  R(-0.085 * k, 0, 0.07 * k, 0.4); R(0.015 * k, 0, 0.07 * k, 0.4);                         // legs
  c.beginPath(); c.moveTo(x - 0.2 * k * h, y - 0.74 * h); c.lineTo(x + 0.2 * k * h, y - 0.74 * h); c.lineTo(x + 0.12 * k * h, y - 0.38 * h); c.lineTo(x - 0.12 * k * h, y - 0.38 * h); c.closePath(); c.fill();   // jacket
  R(-0.26 * k, 0.4, 0.06 * k, 0.33); R(0.2 * k, 0.4, 0.06 * k, 0.33);                       // arms
  R(-0.03 * k, 0.72, 0.06 * k, 0.06);                                                    // neck
  R(-0.085 * k, 0.77, 0.17 * k, 0.21);                                                   // head
  c.beginPath(); c.moveTo(x - 0.085 * k * h, y - 0.98 * h); c.lineTo(x - 0.03 * k * h, y - 1.03 * h); c.lineTo(x + 0.01 * k * h, y - 0.985 * h); c.lineTo(x + 0.06 * k * h, y - 1.04 * h); c.lineTo(x + 0.085 * k * h, y - 0.98 * h); c.closePath(); c.fill();   // the tuft
}

export const OMBRE_PROPS = {
  // A sunny blank wall (the side of a building, a garden wall) for shadows to play on: o.w (10 m) long, o.h (3.4) high, cream render, a darker foot,
  // a stone coping. Origin: the middle of its foot; its face toward +Z (the face is the plane z = 0).
  plainWall(o) {
    const w = o.w ?? 10, h = o.h ?? 3.4;
    return grp(at(box(w, h, 0.3, o.color || '#F3E8D0', { pivot: 'bottom' }), 0, 0, -0.15), at(box(w + 0.06, o.footH ?? 0.42, 0.33, o.foot || '#DCCDB0', { pivot: 'bottom' }), 0, 0, -0.15), at(box(w + 0.16, 0.14, 0.42, o.cap || '#CDBE9F', { pivot: 'bottom' }), 0, h, -0.15));
  },

  // The place of a shadow that has not come: the outline of a man in dashes on a wall (o.h 1.75 m tall), faintly filled, a question mark on its chest.
  // o.at: it pops in at that time (absent before). Origin: its feet; front +Z (lay it 1 cm off the wall).
  ghostOutline(o) {
    const h = o.h ?? 1.75, w = h * 0.66, col = o.color || INK;
    const pl = canvasPlane(w, h * 1.1, (c, W, H) => {
      const mk = () => { const t = document.createElement('canvas'); t.width = W; t.height = H; return t; }, m = mk(), ring = mk(), mg = m.getContext('2d'), rg = ring.getContext('2d'), r = Math.round(W * 0.022);
      drawFigure(mg, W / 2, H * 0.975, H * 0.88, '#000000');
      for (let a = 0; a < 16; a++) rg.drawImage(m, Math.cos(a * TAU / 16) * r, Math.sin(a * TAU / 16) * r);            // the figure, grown by r
      rg.globalCompositeOperation = 'destination-out'; rg.drawImage(m, 0, 0);                                           // minus itself: its edge
      rg.lineWidth = W * 0.035; rg.strokeStyle = '#000'; for (let k = -H; k < W + H; k += W * 0.105) { rg.beginPath(); rg.moveTo(k, 0); rg.lineTo(k + H, H); rg.stroke(); }   // cut into dashes
      rg.globalCompositeOperation = 'source-in'; rg.fillStyle = col; rg.fillRect(0, 0, W, H);
      c.clearRect(0, 0, W, H); c.globalAlpha = 0.09; c.drawImage(m, 0, 0); c.globalAlpha = 1; c.drawImage(ring, 0, 0);
      txt(c, '?', W / 2, H * 0.47, H * 0.2, col);
    }, { res: 512, transparent: true });
    pl.material.transparent = true; pl.material.depthWrite = false; pl.position.y = h * 0.55; const g = grp(pl);
    g.userData.update = t => { const u = o.at == null ? 1 : t - o.at; pl.visible = u >= 0; if (pl.visible) { const k = 1 + 0.35 * Math.max(0, 1 - u / 0.08) - 0.06 * Math.sin(Math.min(u, 0.35) * 30) * Math.exp(-u * 10); pl.scale.set(k, 2 - k, 1); } };
    g.userData.update(0); return g;
  },

  // The notice of a lost shadow: a cream sheet (o.w 0.46 m), a red band « PERDUE », the black outline of a man, lines of small print.
  // o.stampAt: a red stamp (o.stamp 'MAJEURE') lands across it at that time (it pops and settles). Origin: its middle; front +Z.
  lostPoster(o) {
    const w = o.w ?? 0.46, h = w * 1.36, g = grp(at(box(w + 0.02, h + 0.02, 0.012, '#CFC6B2', { outline: 0.008 }), 0, 0, -0.008));
    g.add(canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#F7F1E1'; c.fillRect(0, 0, W, H); c.fillStyle = '#C8202A'; c.fillRect(0, 0, W, H * 0.17); txt(c, o.title || 'PERDUE', W / 2, H * 0.09, fit(c, o.title || 'PERDUE', W * 0.86, H * 0.125), '#FFFFFF');
      drawFigure(c, W / 2, H * 0.84, H * 0.6); c.fillStyle = '#B9B2A2'; for (let i = 0; i < 3; i++) c.fillRect(W * 0.2, H * (0.885 + i * 0.03), W * (0.6 - i * 0.12), H * 0.012); }, { res: 512 }));
    const st = canvasPlane(w * 0.86, w * 0.3, (c, W, H) => { c.clearRect(0, 0, W, H); c.strokeStyle = '#D0202A'; c.lineWidth = H * 0.1; c.strokeRect(H * 0.08, H * 0.08, W - H * 0.16, H * 0.84); txt(c, o.stamp || 'MAJEURE', W / 2, H * 0.54, fit(c, o.stamp || 'MAJEURE', W * 0.82, H * 0.62), '#D0202A'); }, { res: 512, transparent: true });
    st.material.transparent = true; st.material.depthWrite = false; st.position.set(0, -h * 0.08, 0.004); st.rotation.z = 0.2; g.add(st);
    g.userData.update = t => { const u = o.stampAt == null ? -1 : t - o.stampAt; st.visible = u >= 0; if (st.visible) st.scale.setScalar(1 + 0.9 * Math.max(0, 1 - u / 0.07) + 0.06 * Math.sin(Math.min(u, 0.3) * 40) * Math.exp(-u * 12)); };
    g.userData.update(0); return g;
  },

  // A rail of shadows for hire: a tube on two posts (o.w 2.4 m, the rail at o.h 2.0 m) and flat dark outlines hung from it by hangers (o.kinds: a list of
  // 'man' | 'tall' | 'wide' | 'kid' | 'dog'; each sways). o.sign: a board above (« LOCATION D'OMBRES »), o.price: a tag. Origin: the middle of its foot; front +Z.
  shadowRack(o) {
    const w = o.w ?? 2.4, H0 = o.h ?? 2.0, kinds = o.kinds || ['tall', 'man', 'kid', 'wide', 'dog', 'man'], g = grp(), sw = [];
    for (const s of [-1, 1]) g.add(at(cyl(0.03, 0.03, H0, '#8A8F98', 8, { pivot: 'bottom' }), s * w / 2, 0, 0), at(box(0.34, 0.04, 0.34, '#6E737C', { pivot: 'bottom' }), s * w / 2, 0, 0));
    g.add(at(cyl(0.022, 0.022, w + 0.1, '#A9AEB6', 8), 0, H0, 0, 0, 0, PI / 2));
    kinds.forEach((kd, i) => {
      const fh = kd === 'tall' ? 1.72 : kd === 'kid' ? 0.95 : kd === 'dog' ? 0.62 : kd === 'wide' ? 1.45 : 1.5, fw = fh * (kd === 'dog' ? 1.1 : kd === 'wide' ? 0.85 : 0.6), piv = grp(); piv.position.set(-w / 2 + (i + 0.5) * w / kinds.length, H0, 0);
      const pl = canvasPlane(fw, fh, (c, W, H) => { c.clearRect(0, 0, W, H); drawFigure(c, W / 2, H * 0.985, H * (kd === 'dog' ? 0.9 : 0.95), INK, kd); }, { res: 384, transparent: true });
      pl.material = flat('#FFFFFF', { map: pl.material.map, transparent: true, alphaTest: 0.5, side: THREE.DoubleSide }); pl.position.y = -0.1 - fh / 2; piv.add(pl);
      const hook = new THREE.Mesh(new THREE.TorusGeometry(0.035, 0.007, 5, 10, PI * 1.4), mat('#5B5F67')); hook.position.y = -0.035; piv.add(hook, at(box(0.3, 0.012, 0.012, '#5B5F67'), 0, -0.1, 0));
      g.add(piv); sw.push({ piv, ph: i * 1.7, amp: 0.035 + 0.02 * (i % 3) });
    });
    if (o.sign !== false) { const sg = canvasPlane(w * 0.9, 0.36, (c, W, H) => { c.fillStyle = '#1B2F6B'; c.fillRect(0, 0, W, H); c.strokeStyle = '#F4F1E8'; c.lineWidth = H * 0.05; c.strokeRect(H * 0.08, H * 0.08, W - H * 0.16, H * 0.84); txt(c, o.sign || "LOCATION D'OMBRES", W / 2, H * 0.54, fit(c, o.sign || "LOCATION D'OMBRES", W * 0.86, H * 0.52), '#F4F1E8'); }, { res: 768 }); sg.position.set(0, H0 + 0.42, 0.02); g.add(sg, at(box(w * 0.9 + 0.04, 0.4, 0.03, '#14224E'), 0, H0 + 0.42, 0)); }
    g.userData.update = t => { for (const s of sw) s.piv.rotation.z = s.amp * Math.sin(t * 1.9 + s.ph) * (o.sway ?? 1); };
    g.userData.update(0); return g;
  },

  // A fine: a pale yellow slip (o.w 0.3 m) headed « AMENDE », the offence in capitals (o.text 'SANS OMBRE'), a sum (o.sum '135 €'). Origin: its middle; front +Z.
  fineSlip(o) {
    const w = o.w ?? 0.3, h = w * 1.3, g = grp(at(box(w + 0.012, h + 0.012, 0.008, '#D8C870', { outline: 0.006 }), 0, 0, -0.006));
    for (const s of [1, -1]) { const f = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#F6E98C'; c.fillRect(0, 0, W, H); c.fillStyle = '#1B2F6B'; c.fillRect(0, 0, W, H * 0.2); txt(c, 'AMENDE', W / 2, H * 0.105, fit(c, 'AMENDE', W * 0.8, H * 0.14), '#FFFFFF');
        const T = (o.text || 'SANS OMBRE').split(' '); T.forEach((s2, i) => txt(c, s2, W / 2, H * (0.38 + i * 0.19), fit(c, s2, W * 0.84, H * 0.17), '#1B1B1E')); txt(c, o.sum || '135 €', W / 2, H * 0.86, fit(c, o.sum || '135 €', W * 0.5, H * 0.13), '#C8202A'); }, { res: 384 });
      f.position.z = s * 0.001; if (s < 0) f.rotation.y = PI; g.add(f); }
    return g;
  },

  // The calendar of a shared custody: a board (o.w 1.0 m) headed « GARDE ALTERNÉE », two rows of seven days, alternately pale (LUI) and dark (ELLE).
  // o.mark [[t, day], ...]: a red frame on that day (0..13) from that time. Origin: its middle; front +Z.
  custodyCalendar(o) {
    const w = o.w ?? 1.0, h = w * 0.74, g = grp(at(box(w + 0.04, h + 0.04, 0.02, '#8A7A60', { outline: 0.008 }), 0, 0, -0.012)), cw = w * 0.9 / 7, ch = h * 0.3, x0 = -w * 0.45 + cw / 2, y0 = h * 0.08;
    g.add(canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#F7F1E1'; c.fillRect(0, 0, W, H); c.fillStyle = '#1B2F6B'; c.fillRect(0, 0, W, H * 0.2); txt(c, o.title || 'GARDE ALTERNÉE', W / 2, H * 0.105, fit(c, o.title || 'GARDE ALTERNÉE', W * 0.86, H * 0.13), '#FFFFFF');
      for (let i = 0; i < 14; i++) { const cx = W * (0.05 + 0.9 * ((i % 7) + 0.5) / 7), cy = H * (i < 7 ? 0.42 : 0.74), dark = i % 2 === 1, a = W * 0.9 / 7 * 0.9, b = H * 0.27;
        c.fillStyle = dark ? INK : '#FFFFFF'; c.fillRect(cx - a / 2, cy - b / 2, a, b); c.strokeStyle = '#8A7A60'; c.lineWidth = W * 0.004; c.strokeRect(cx - a / 2, cy - b / 2, a, b);
        txt(c, String(i + 1), cx, cy - b * 0.14, b * 0.42, dark ? '#F7F1E1' : '#1B1B1E'); txt(c, dark ? 'ELLE' : 'LUI', cx, cy + b * 0.28, b * 0.2, dark ? '#F7F1E1' : '#6B6457', '700'); } }, { res: 768 }));
    const fr = grp(); for (const [dx, dy, a, b] of [[0, ch / 2, cw, 0.012], [0, -ch / 2, cw, 0.012], [cw / 2, 0, 0.012, ch], [-cw / 2, 0, 0.012, ch]]) fr.add(at(box(a + 0.012, b + 0.0, 0.006, '#D0202A'), dx, dy, 0)); fr.position.z = 0.006; g.add(fr);
    g.userData.update = t => { let d = -1; for (const [tt, day] of o.mark || []) if (t >= tt) d = day; fr.visible = d >= 0; if (fr.visible) fr.position.set(x0 + (d % 7) * cw, (d < 7 ? 1 : -1) * h * 0.16 - y0 * 0, 0.006); };
    g.userData.update(0); return g;
  },

  // A strip of cobblestones: o.len (6 m) along Z, o.w (2.4) wide, rounded setts in staggered rows, standing o.h (0.035 m) proud of the road.
  // Origin: the middle of the strip, at road level.
  cobbles(o) {
    const L = o.len ?? 6, w = o.w ?? 2.4, s = o.size ?? 0.17, hh = o.h ?? 0.035, r = rng(o.seed || 9), g = grp(), cols = ['#8E8A84', '#A19C93', '#7C7872', '#B0AAA0'];
    g.add(at(box(w + 0.1, 0.02, L + 0.1, '#5E5B57'), 0, 0.006, 0));
    const geo = new THREE.BoxGeometry(s * 0.86, hh, s * 0.86), nx = Math.floor(w / s), nz = Math.floor(L / s), per = [[], [], [], []];
    for (let j = 0; j < nz; j++) for (let i = 0; i < nx; i++) per[Math.floor(r() * 4)].push([(-w / 2 + (i + 0.5 + (j % 2 ? 0.5 : 0)) * s) * (i === nx - 1 && j % 2 ? 0 : 1), 0.012 + hh / 2 + r() * 0.008, -L / 2 + (j + 0.5) * s]);
    per.forEach((pts, k) => { const im = new THREE.InstancedMesh(geo, mat(cols[k]), pts.length), m = new THREE.Matrix4(); pts.forEach((p, n) => { m.makeRotationY((r() - 0.5) * 0.12); m.setPosition(p[0], p[1], p[2]); im.setMatrixAt(n, m); }); im.castShadow = false; im.receiveShadow = true; g.add(im); });
    return g;
  },

  // The white bands of a barrister's gown (a « rabat »): two pale tabs under the chin, unlit, to pin on a shadow. Origin: the knot; they hang down -Y; front +Z.
  rabat(o) {
    const s = o.s ?? 1, g = grp(), m = flat(o.color || '#F4F1E8');
    for (const sg of [-1, 1]) { const q = new THREE.Mesh(new THREE.PlaneGeometry(0.05, 0.16), m); q.position.set(sg * 0.03, -0.08, 0); q.rotation.z = sg * 0.1; q.castShadow = false; g.add(q); const b = q.clone(); b.rotation.y = PI; g.add(b); }
    g.scale.setScalar(s); return g;
  },
};
