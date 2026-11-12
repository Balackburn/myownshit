// « L'ombre » (story 42): a man whose shadow is late, then leaves him; the town hall answers that she is of age.
// Conventions as in props.js (metres, front +Z, pivot at the floor); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, rng, ease, clamp01 } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI, INK = '#6A5878';   // the shade of every shadow of the story (the shadow actors are cast with the same colour): a violet half-way between a navy suit and a sunny wall
const txt = (g, s, x, y, px, color = '#1B1B1E', weight = '900') => { g.fillStyle = color; g.font = `${weight} ${px}px Arial`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(s, x, y); };
const fit = (g, s, w, px, weight = '900') => { g.font = `${weight} ${px}px Arial`; const m = g.measureText(s).width; return m > w ? px * w / m : px; };
const flat = (color, o = {}) => new THREE.MeshBasicMaterial({ color, toneMapped: false, ...o });
// the outline of a man of the series (a tall box of a head with a tuft, square shoulders, a tie) drawn on a canvas: feet at (x, y), h pixels tall.
// kind: 'man' | 'tall' | 'wide' | 'kid' | 'dog'
function drawFigure(c, x, y, h, col = INK, kind = 'man', slim = false) {
  c.fillStyle = col; const R = (a, b, w, hh) => c.fillRect(x + a * h, y - b * h - hh * h, w * h, hh * h);
  if (kind === 'dogv') { R(-0.11, 0.2, 0.22, 0.6); R(-0.11, 0.0, 0.07, 0.24); R(0.04, 0.0, 0.07, 0.24); R(-0.2, 0.52, 0.09, 0.2); R(0.11, 0.52, 0.09, 0.2); R(-0.13, 0.78, 0.26, 0.2); R(-0.07, 0.68, 0.14, 0.14); R(-0.17, 0.9, 0.07, 0.1); R(0.1, 0.9, 0.07, 0.1); return; }   // a dog hung by its collar: upright, its paws down, its ears up
  if (kind === 'dog') { R(-0.3, 0.12, 0.6, 0.22); R(-0.3, 0, 0.07, 0.14); R(-0.12, 0, 0.07, 0.14); R(0.08, 0, 0.07, 0.14); R(0.23, 0, 0.07, 0.14); R(0.2, 0.3, 0.26, 0.2); R(0.4, 0.34, 0.12, 0.1); R(0.22, 0.48, 0.06, 0.1); R(-0.42, 0.26, 0.14, 0.05); return; }
  const k = kind === 'tall' ? 0.72 : kind === 'wide' ? 1.5 : kind === 'kid' ? 1.15 : 1;   // how wide for its height
  R(-0.085 * k, 0, 0.07 * k, 0.4); R(0.015 * k, 0, 0.07 * k, 0.4);                         // legs
  c.beginPath(); c.moveTo(x - 0.2 * k * h, y - 0.74 * h); c.lineTo(x + 0.2 * k * h, y - 0.74 * h); c.lineTo(x + 0.12 * k * h, y - 0.38 * h); c.lineTo(x - 0.12 * k * h, y - 0.38 * h); c.closePath(); c.fill();   // jacket
  if (!slim) { R(-0.26 * k, 0.4, 0.06 * k, 0.33); R(0.2 * k, 0.4, 0.06 * k, 0.33); }       // arms (slim: against the body: on a hanger)
  R(-0.03 * k, 0.72, 0.06 * k, 0.06);                                                    // neck
  R(-0.085 * k, 0.77, 0.17 * k, 0.21);                                                   // head
  c.beginPath(); c.moveTo(x - 0.085 * k * h, y - 0.98 * h); c.lineTo(x - 0.03 * k * h, y - 1.03 * h); c.lineTo(x + 0.01 * k * h, y - 0.985 * h); c.lineTo(x + 0.06 * k * h, y - 1.04 * h); c.lineTo(x + 0.085 * k * h, y - 0.98 * h); c.closePath(); c.fill();   // the tuft
}

export const OMBRE_PROPS = {
  // A sunny blank wall (the side of a building, a garden wall) for shadows to play on: o.w (10 m) long, o.h (3.4) high, cream render, a darker foot,
  // a stone coping. Origin: the middle of its foot; its face toward +Z (the face is the plane z = 0).
  plainWall(o) {
    // o.strip: a string course at 2.9 m and, above it, the foot of the next floor and its balcony rail (the top of the picture is the bottom of a house)
    // o.plaque { text: 'RUE DU SOLEIL', x, y (2.35), w (1.05) }: a blue enamel street plaque (x: along the wall, from its middle)
    // o.stencil { text: "DÉFENSE D'AFFICHER", x, y (1.9), w (1.5) }: black stencilled capitals on the render, and the date of the law under them
    // o.sun { x, w (2.6), slope (0.5) }: the slanted edge of the shade of the house across the street, in the shade of the story's shadows (o.shade),
    //   over the top corner of the wall from x on (the rule of the film: a shadow is that violet)
    const w = o.w ?? 10, h = o.h ?? 3.4, g = grp(at(box(w, h, 0.3, o.color || '#F3E8D0', { pivot: 'bottom' }), 0, 0, -0.15), at(box(w + 0.06, o.footH ?? 0.42, 0.33, o.foot || '#DCCDB0', { pivot: 'bottom' }), 0, 0, -0.15));
    if (o.strip) { const up = o.up || o.color || '#F3E8D0';
      g.add(at(box(w + 0.1, 0.16, 0.5, o.cap || '#CDBE9F', { pivot: 'bottom' }), 0, 2.9, -0.1), at(box(w + 0.1, 0.06, 0.62, o.cap || '#CDBE9F', { pivot: 'bottom' }), 0, 3.06, -0.06));   // the string course, and the slab of the balcony on it
      g.add(at(box(w, 3.2, 0.3, up, { pivot: 'bottom' }), 0, 3.12, -0.15));                                                                                                             // the wall of the next floor
      const rail = grp(), ink = '#2B2D33'; for (let x = -w / 2 + 0.07; x < w / 2; x += 0.14) rail.add(at(box(0.022, 0.84, 0.022, ink, { pivot: 'bottom' }), x, 0, 0));
      rail.add(at(box(w, 0.04, 0.04, ink), 0, 0.84, 0), at(box(w, 0.03, 0.03, ink), 0, 0.12, 0)); rail.position.set(0, 3.12, 0.2); rail.traverse(q => { if (q.isMesh) q.castShadow = false; }); g.add(rail);
      for (let x = -w / 2 + 1.6; x < w / 2 - 0.8; x += 3.2) g.add(at(box(1.1, 2.2, 0.06, '#7C93A6', { pivot: 'bottom' }), x, 3.12, 0.0), at(box(0.5, 2.2, 0.05, '#DCE3E6', { pivot: 'bottom' }), x - 0.83, 3.12, 0.02), at(box(0.5, 2.2, 0.05, '#DCE3E6', { pivot: 'bottom' }), x + 0.83, 3.12, 0.02));   // tall windows, their shutters open
    } else g.add(at(box(w + 0.16, 0.14, 0.42, o.cap || '#CDBE9F', { pivot: 'bottom' }), 0, h, -0.15));
    if (o.plaque) { const q = o.plaque, pw = q.w ?? 1.05, ph = pw * 0.56, T = (q.text || 'RUE DU SOLEIL').split(' '), last = T.pop(), first = T.join(' ');
      const pl = canvasPlane(pw, ph, (c, W, H) => { c.fillStyle = '#2C8A55'; c.fillRect(0, 0, W, H); c.fillStyle = '#1F4FA8'; c.fillRect(H * 0.07, H * 0.07, W - H * 0.14, H * 0.86);
        txt(c, first, W / 2, H * 0.3, fit(c, first, W * 0.6, H * 0.2), '#FFFFFF'); txt(c, last, W / 2, H * 0.63, fit(c, last, W * 0.8, H * 0.4), '#FFFFFF'); }, { res: 512 });
      pl.position.set(q.x ?? 0, q.y ?? 2.35, 0.012); g.add(pl, at(box(pw + 0.02, ph + 0.02, 0.012, '#1B3F86'), q.x ?? 0, q.y ?? 2.35, 0.004)); }
    if (o.stencil) { const q = o.stencil, sw = q.w ?? 1.5, sh = sw * 0.3, tx0 = q.text || "DÉFENSE D'AFFICHER";
      const pl = canvasPlane(sw, sh, (c, W, H) => { c.clearRect(0, 0, W, H); txt(c, tx0, W / 2, H * 0.36, fit(c, tx0, W * 0.98, H * 0.56), '#2B2D33'); txt(c, q.sub ?? 'LOI DU 29 JUILLET 1881', W / 2, H * 0.82, fit(c, q.sub ?? 'LOI DU 29 JUILLET 1881', W * 0.7, H * 0.24), '#2B2D33', '700'); }, { res: 768, transparent: true });
      pl.material.transparent = true; pl.material.depthWrite = false; pl.material.opacity = 0.82; pl.position.set(q.x ?? 0, q.y ?? 1.9, 0.006); g.add(pl); }
    if (o.sun) { const q = o.sun, x0 = q.x ?? 0, sw = q.w ?? 2.6, k = q.slope ?? 0.5, top = o.strip ? 2.9 : h, sh = new THREE.Shape(); sh.moveTo(x0, top); sh.lineTo(x0 + sw, top); sh.lineTo(x0 + sw, top - Math.abs(sw) * k); sh.closePath();   // (w below 0: the wedge runs the other way)
      const m = new THREE.Mesh(new THREE.ShapeGeometry(sh), flat(o.shade || INK, { side: THREE.DoubleSide })); m.position.z = 0.004; m.userData.noAO = true; g.add(m); }
    return g;
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
    const w = o.w ?? 0.46, h = w * 1.36, g = grp(at(box(w + 0.02, h + 0.02, 0.012, '#E4E0D6', { outline: 0.008 }), 0, 0, -0.008));
    const face = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.fillStyle = '#C8202A'; c.fillRect(0, 0, W, H * 0.22); txt(c, o.title || 'PERDUE', W / 2, H * 0.118, fit(c, o.title || 'PERDUE', W * 0.9, H * 0.19), '#FFFFFF');
      drawFigure(c, W / 2, H * 0.86, H * 0.58, o.shade || INK); c.fillStyle = '#C9C5BB'; for (let i = 0; i < 2; i++) c.fillRect(W * 0.2, H * (0.9 + i * 0.035), W * (0.6 - i * 0.14), H * 0.014); }, { res: 512 });
    if (o.bright !== false) { face.material = flat('#FFFFFF', { map: face.material.map }); face.material.color.setScalar(o.bright ?? 0.93); }   // an unlit sheet: white paper on a pale wall (lit, it took the colour of the wall); o.bright false: lit
    g.add(face);
    if (o.back) { const bk = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#F1EEE6'; c.fillRect(0, 0, W, H); c.save(); c.translate(W, 0); c.scale(-1, 1); c.globalAlpha = 0.2; c.fillStyle = '#C8202A'; c.fillRect(0, 0, W, H * 0.22); c.globalAlpha = 0.26; drawFigure(c, W / 2, H * 0.86, H * 0.58, o.shade || INK); c.restore(); }, { res: 512 });
      bk.material = flat('#FFFFFF', { map: bk.material.map }); bk.material.color.setScalar(o.bright ?? 0.93); bk.position.z = -0.0145; bk.rotation.y = PI; g.add(bk); }   // o.back: seen from behind, the print shows through the paper
    // (a white ground under the word of the stamp: red on the violet of the figure did not read)
    const st = canvasPlane(w * 0.86, w * 0.3, (c, W, H) => { c.clearRect(0, 0, W, H); c.fillStyle = 'rgba(255,255,255,0.8)'; c.fillRect(H * 0.08, H * 0.08, W - H * 0.16, H * 0.84); c.strokeStyle = '#D0202A'; c.lineWidth = H * 0.1; c.strokeRect(H * 0.08, H * 0.08, W - H * 0.16, H * 0.84); txt(c, o.stamp || 'MAJEURE', W / 2, H * 0.54, fit(c, o.stamp || 'MAJEURE', W * 0.82, H * 0.62), '#D0202A'); }, { res: 512, transparent: true });
    st.material.transparent = true; st.material.depthWrite = false; st.position.set(0, -h * 0.08, 0.004); st.rotation.z = 0.2; g.add(st);
    g.userData.update = t => { const u = o.stampAt == null ? -1 : t - o.stampAt; st.visible = u >= 0; if (st.visible) st.scale.setScalar(1 + 0.9 * Math.max(0, 1 - u / 0.07) + 0.06 * Math.sin(Math.min(u, 0.3) * 40) * Math.exp(-u * 12)); };
    g.userData.update(0); return g;
  },

  // A rail of shadows for hire: a tube on two posts (o.w 2.4 m, the rail at o.h 2.0 m) and flat dark outlines hung from it by hangers (o.kinds: a list of
  // 'man' | 'tall' | 'wide' | 'kid' | 'dog'; each sways). o.sign: a board above (« LOCATION D'OMBRES »), o.price: a tag. Origin: the middle of its foot; front +Z.
  shadowRack(o) {
    // o.pick [[t, i], ...]: at that time the hand of the customer is on the hanger i: its shadow perks up (a hop, eyes wide; (cycle 7) o.hop: a real hop, that fraction of its height); o.gone [t, i]: from that time
    // the hanger i is empty (taken)
    const w = o.w ?? 2.4, H0 = o.h ?? 2.0, kinds = o.kinds || ['tall', 'man', 'kid', 'wide', 'dog', 'man'], g = grp(), sw = [], col = o.shade || INK;
    for (const s of [-1, 1]) g.add(at(cyl(0.03, 0.03, H0, '#8A8F98', 8, { pivot: 'bottom' }), s * w / 2, 0, 0), at(box(0.34, 0.04, 0.34, '#6E737C', { pivot: 'bottom' }), s * w / 2, 0, 0));
    g.add(at(cyl(0.022, 0.022, w + 0.1, '#A9AEB6', 8), 0, H0, 0, 0, 0, PI / 2));
    const slot = (w - 0.16) / kinds.length;
    kinds.forEach((kd, i) => {
      const fh = kd === 'tall' ? 1.72 : kd === 'kid' ? 0.95 : kd === 'dog' ? 0.62 : kd === 'dogv' ? 0.9 : kd === 'wide' ? 1.4 : (o.manH ?? 1.5), kk = kd === 'tall' ? 0.72 : kd === 'wide' ? 1.5 : kd === 'kid' ? 1.15 : 1, fw = kd === 'dog' ? fh * 1.1 : kd === 'dogv' ? fh * 0.5 : fh * 0.56 * kk * 1.06, piv = grp(); piv.position.set(-w / 2 + 0.08 + (i + 0.5) * slot, H0, 0);
      const pl = canvasPlane(fw, fh, (c, W, H) => { c.clearRect(0, 0, W, H); const fhp = H * (kd === 'dog' ? 0.9 : 0.95); drawFigure(c, W / 2, H * 0.985, fhp, col, kd, !!o.slim);
        c.fillStyle = '#FFFFFF'; if (kd === 'dog') { c.beginPath(); c.arc(W / 2 + 0.34 * fhp, H * 0.985 - 0.4 * fhp, 0.045 * fhp, 0, TAU); c.fill(); }
        else if (kd === 'dogv') for (const sx of [-1, 1]) { c.beginPath(); c.ellipse(W / 2 + sx * 0.06 * fhp, H * 0.985 - 0.89 * fhp, 0.032 * fhp, 0.036 * fhp, 0, 0, TAU); c.fill(); }
        else for (const sx of [-1, 1]) { c.beginPath(); c.ellipse(W / 2 + sx * 0.042 * kk * fhp, H * 0.985 - 0.9 * fhp, 0.026 * kk * fhp, 0.03 * fhp, 0, 0, TAU); c.fill(); } }, { res: 384, transparent: true });
      pl.material = flat('#FFFFFF', { map: pl.material.map, transparent: true, alphaTest: 0.5, side: THREE.DoubleSide }); pl.position.y = -0.1 - fh / 2; piv.add(pl);
      const hook = new THREE.Mesh(new THREE.TorusGeometry(0.035, 0.007, 5, 10, PI * 1.4), mat('#5B5F67')); hook.position.y = -0.035; piv.add(hook, at(box(Math.min(0.3, fw * 0.8), 0.012, 0.012, '#5B5F67'), 0, -0.1, 0));
      g.add(piv); sw.push({ piv, pl, i, ph: i * 1.7, amp: 0.035 + 0.02 * (i % 3), y0: pl.position.y, fh });
    });
    if (o.sign !== false) { const sh = o.signH ?? 0.36, sg = canvasPlane(w * 0.9, sh, (c, W, H) => { c.fillStyle = '#1B2F6B'; c.fillRect(0, 0, W, H); c.strokeStyle = '#F4F1E8'; c.lineWidth = H * 0.05; c.strokeRect(H * 0.08, H * 0.08, W - H * 0.16, H * 0.84); txt(c, o.sign || "LOCATION D'OMBRES", W / 2, H * 0.54, fit(c, o.sign || "LOCATION D'OMBRES", W * 0.86, H * 0.6), '#F4F1E8'); }, { res: 768 }); sg.position.set(0, H0 + 0.24 + sh / 2, 0.02); g.add(sg, at(box(w * 0.9 + 0.04, sh + 0.04, 0.03, '#14224E'), 0, H0 + 0.24 + sh / 2, 0)); }
    g.userData.update = t => { for (const s of sw) { s.piv.rotation.z = s.amp * Math.sin(t * 1.9 + s.ph) * (o.sway ?? 1); let k = 1, hop = 0; for (const [tt, i] of o.pick || []) if (i === s.i && t >= tt) { const u = t - tt; k = 1 + 0.16 * Math.exp(-u * 9) * Math.cos(u * 26); hop = (o.hop ?? 0) * s.fh * Math.exp(-u * 5) * Math.abs(Math.sin(u * 12)); }
        s.pl.scale.set(2 - k, k, 1); s.pl.position.y = s.y0 + hop; s.piv.visible = !(o.gone && o.gone[1] === s.i && t >= o.gone[0]); } };
    g.userData.update(0); return g;
  },

  // A fine: a pale yellow slip (o.w 0.3 m) headed « AMENDE », the offence in capitals (o.text 'SANS OMBRE'), a sum (o.sum '135 €'). Origin: its middle; front +Z.
  fineSlip(o) {
    const w = o.w ?? 0.3, h = w * 1.3, g = grp(at(box(w + 0.012, h + 0.012, 0.008, '#D8C870', { outline: 0.006 }), 0, 0, -0.006));
    for (const s of [1, -1]) { const f = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#F6E98C'; c.fillRect(0, 0, W, H); c.fillStyle = '#1B2F6B'; c.fillRect(0, 0, W, H * 0.2); c.fillRect(0, 0, W, H * 0.24); txt(c, 'AMENDE', W / 2, H * 0.125, fit(c, 'AMENDE', W * 0.9, H * 0.2), '#FFFFFF');
        const T = (o.text || 'SANS OMBRE').split(' '); T.forEach((s2, i) => txt(c, s2, W / 2, H * (0.37 + i * 0.2), fit(c, s2, W * 0.9, H * 0.2), '#1B1B1E')); txt(c, o.sum || '135 €', W / 2, H * 0.87, fit(c, o.sum || '135 €', W * 0.72, H * 0.19), '#C8202A'); }, { res: 384 });
      f.position.z = s * 0.001; if (s < 0) f.rotation.y = PI; g.add(f); }
    return g;
  },

  // The calendar of a shared custody: a board (o.w 1.0 m) headed « GARDE ALTERNÉE », two rows of seven days, alternately pale (LUI) and dark (ELLE).
  // o.mark [[t, day], ...]: a red frame on that day (0..13) from that time. Origin: its middle; front +Z.
  custodyCalendar(o) {
    // o.rows (2): 1: a single row of seven bigger days (a wider, lower board). o.big: one day alone, framed (the day of the shot): { day: 2, who: 'ELLE' }
    const rows = o.big ? 1 : (o.rows ?? 2), w = o.w ?? 1.0, h = o.big ? w * 1.18 : rows === 1 ? w * 0.48 : w * 0.74, col = o.shade || INK, hd = o.big ? 0.2 : rows === 1 ? 0.3 : 0.2;
    const g = grp(at(box(w + 0.04, h + 0.04, 0.02, '#8A7A60', { outline: 0.008 }), 0, 0, -0.012));
    const cellW = 0.9 / 7, cy0 = rows === 1 ? 0.65 : 0.42, cy1 = 0.74, bh = rows === 1 ? 0.56 : 0.27;   // in fractions of the board: the width of a day, the middle of each row, the height of a day
    g.add(canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#F7F1E1'; c.fillRect(0, 0, W, H); c.fillStyle = '#1B2F6B'; c.fillRect(0, 0, W, H * hd); txt(c, o.title || 'GARDE ALTERNÉE', W / 2, H * hd * 0.53, fit(c, o.title || 'GARDE ALTERNÉE', W * 0.9, H * hd * 0.68), '#FFFFFF');
      if (o.big) { const dark = (o.big.who || 'ELLE') === 'ELLE', a = W * 0.7, b = H * 0.66, cx = W / 2, cy = H * 0.6; c.fillStyle = dark ? col : '#FFFFFF'; c.fillRect(cx - a / 2, cy - b / 2, a, b); c.strokeStyle = '#D0202A'; c.lineWidth = W * 0.035; c.strokeRect(cx - a / 2, cy - b / 2, a, b);
        txt(c, String(o.big.day ?? 2), cx, cy - b * 0.12, b * 0.62, dark ? '#FFFFFF' : '#1B1B1E'); txt(c, o.big.who || 'ELLE', cx, cy + b * 0.33, b * 0.2, dark ? '#FFFFFF' : '#6B6457'); return; }
      for (let i = 0; i < 7 * rows; i++) { const cx = W * (0.05 + 0.9 * ((i % 7) + 0.5) / 7), cy = H * (i < 7 ? cy0 : cy1), dark = i % 2 === 1, a = W * cellW * 0.9, b = H * bh;
        c.fillStyle = dark ? col : '#FFFFFF'; c.fillRect(cx - a / 2, cy - b / 2, a, b); c.strokeStyle = '#8A7A60'; c.lineWidth = W * 0.004; c.strokeRect(cx - a / 2, cy - b / 2, a, b);
        txt(c, String(i + 1), cx, cy - b * 0.14, Math.min(b * 0.46, a * 0.74), dark ? '#FFFFFF' : '#1B1B1E'); txt(c, dark ? 'ELLE' : 'LUI', cx, cy + b * 0.3, Math.min(b * 0.2, a * 0.34), dark ? '#FFFFFF' : '#6B6457', '900'); } }, { res: 768 }));
    const cw = w * cellW, ch = h * bh, fr = grp(); for (const [dx, dy, a, b] of [[0, ch / 2, cw, 0.016], [0, -ch / 2, cw, 0.016], [cw / 2, 0, 0.016, ch], [-cw / 2, 0, 0.016, ch]]) fr.add(at(box(a + 0.016, b + 0.0, 0.006, '#D0202A'), dx, dy, 0)); fr.position.z = 0.006; g.add(fr);
    const rowY = i => h * (0.5 - (i < 7 ? cy0 : cy1));   // the middle of a row, from the middle of the board (the picture's y runs down)
    g.userData.update = t => { let d = -1; for (const [tt, day] of o.mark || []) if (t >= tt) d = day; fr.visible = d >= 0 && !o.big; if (fr.visible) fr.position.set(-w * 0.45 + cw / 2 + (d % 7) * cw, rowY(d), 0.006); };
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

  // A pedestrian crossing: o.n (6) white bars side by side along +X from the origin, each o.bar (0.5 m) wide and o.len (3 m) long along Z (the way
  // of the traffic), o.gap (0.5) apart. Origin: the near edge of the first bar, at road level.
  zebra(o) {
    const n = o.n ?? 6, L = o.len ?? 3.0, bw = o.bar ?? 0.5, gap = o.gap ?? 0.5, g = grp();
    for (let i = 0; i < n; i++) { const m = at(box(bw, 0.012, L, o.color || '#F2F0E8'), bw / 2 + i * (bw + gap), 0.009, 0); m.castShadow = false; g.add(m); }
    return g;
  },

  // The joints of a pavement: thin dark lines across it (o.w 2.4 m long, along X), every o.step (0.45 m) of Z over o.len (12 m), from the origin toward
  // -Z: something for the ground to go by with under a camera that travels. o.raised [n, ...]: the slab after the joint number n stands o.lip (0.035 m)
  // proud of the others: a step to bump over. Origin: the middle of the first joint.
  pavingJoints(o) {
    const w = o.w ?? 2.4, st = o.step ?? 0.45, L = o.len ?? 12, g = grp(), n = Math.floor(L / st), up = new Set(o.raised || []), lip = o.lip ?? 0.035;
    for (let i = 0; i <= n; i++) { const m = at(box(w, 0.004, 0.022, o.color || '#8E8478'), 0, 0.005, -i * st); m.castShadow = false; g.add(m);
      if (up.has(i)) g.add(at(box(w, lip, st - 0.03, o.slab || '#D2C8B8', { outline: 0.004 }), 0, lip / 2, -i * st - st / 2)); }
    for (const sx of [-0.5, 0.5]) for (let i = 0; i < n; i += 2) { const m = at(box(0.022, 0.004, st, o.color || '#8E8478'), sx * w * 0.42 * (i % 4 ? 1 : 0.4), 0.005, -i * st - st / 2); m.castShadow = false; g.add(m); }   // a few joints the other way: slabs, not stripes
    return g;
  },

  // A dashed line on a road: white dashes o.dash (1.0 m) long, o.w (0.12) wide, every o.period (2.0 m) of Z over o.len (14 m), from the origin toward -Z.
  roadDashes(o) {
    const d = o.dash ?? 1.0, P0 = o.period ?? 2.0, L = o.len ?? 14, g = grp();
    for (let z = 0; z < L; z += P0) { const m = at(box(o.w ?? 0.12, 0.01, d, o.color || '#EDEBE3'), 0, 0.008, -z - d / 2); m.castShadow = false; g.add(m); }
    return g;
  },

  // The face of a watch, big enough for a phone: an unlit white disc (o.r 0.07 m), a gold rim (o.rim false: none), two hands (o.hands: their colour;
  // false: none). Not worn: stand it where the wrist is when it is looked at, facing the camera, and key its scale (a watch on a wrist shows its strap
  // or its edge, whichever way the forearm turns). On a shadow: o.rim false, o.hands the shade. Origin: its middle; front +Z.
  watchFace(o) {
    const r = o.r ?? 0.07, g = grp(), disc = new THREE.Mesh(new THREE.CircleGeometry(r, 20), flat(o.color || '#FFFFFF')); disc.userData.noAO = true; g.add(disc);
    if (o.rim !== false) { const rm = new THREE.Mesh(new THREE.RingGeometry(r, r * 1.16, 20), flat(o.rim || '#C9A24B')); rm.position.z = 0.001; g.add(rm); }
    if (o.hands !== false) { const hc = flat(o.hands || '#2B2D33'); for (const [len, a] of [[0.62, 0.5], [0.42, -1.1]]) { const h = new THREE.Mesh(new THREE.PlaneGeometry(r * 0.13, r * len), hc); h.position.set(-Math.sin(a) * r * len / 2, Math.cos(a) * r * len / 2, 0.002); h.rotation.z = a; g.add(h); } }
    g.traverse(q => { if (q.isMesh) { q.castShadow = false; q.receiveShadow = false; } }); return g;
  },

  // The sole of a shoe, to pin under a foot that is shown to the camera (on: {actor, joint: 'footR', offset: [0, -0.07, 0.06]}): a tan leather sole, a
  // darker heel (o.len 0.26 m, o.w 0.09). Origin: its middle; it looks down -Y, the toe toward +Z.
  shoeSole(o) {
    const L = o.len ?? 0.26, w = o.w ?? 0.09;
    if (o.tread) {   // (cycle 7) a dark rubber sole with pale ribs across it: it reads as the underside of a shoe (a plain tan one read as a parcel)
      const g = grp(at(box(w, 0.012, L, o.color || '#3A3330', { outline: 0.005 }), 0, 0, 0));
      for (let i = 0; i < 6; i++) g.add(at(box(w * 0.8, 0.004, 0.012, o.rib || '#A89C8A'), 0, -0.008, L * (-0.38 + i * 0.15)));
      g.add(at(box(w * 0.96, 0.016, L * 0.24, o.heel || '#2A2422', { outline: 0.004 }), 0, -0.007, -L * 0.37)); return g;
    }
    return grp(at(box(w, 0.008, L, o.color || '#C9A070', { outline: 0.004 }), 0, 0, 0), at(box(w * 0.96, 0.014, L * 0.26, o.heel || '#7A5A3A'), 0, -0.006, -L * 0.36));
  },

  // (cycle 7) a big fist with its thumb up, to hold beside a face seen from above (a hand's own thumb points wherever its forearm lets it: out at his
  // side it read as a hitchhiker's): origin at the middle of the fist, the thumb along +Y, the knuckles toward +Z; o.skin, o.cuff (the sleeve)
  thumbsUp(o) {
    const sk = o.skin || '#D9A877', g = grp(at(box(0.12, 0.1, 0.11, sk, { outline: 0.005 }), 0, 0, 0), at(box(0.042, 0.11, 0.046, sk, { outline: 0.004 }), -0.036, 0.1, 0.008),
      at(box(0.13, 0.07, 0.12, o.cuff || '#1F2A44', { outline: 0.004 }), 0, -0.085, 0), at(box(0.135, 0.02, 0.125, '#F4F1E8'), 0, -0.045, 0));
    for (let i = 0; i < 3; i++) g.add(at(box(0.004, 0.06, 0.004, '#9A6A45'), 0.03 - i * 0.03, -0.005, 0.056));   // the folds between the fingers
    return g;
  },

  // A Paris bollard (« potelet »): a slim dark post (o.h 1.0 m) with a ball on top and a white band under it. Origin: its foot.
  potelet(o) {
    const h = o.h ?? 1.0, c = o.color || '#4A3B2E';
    const ball = new THREE.Mesh(new THREE.SphereGeometry(0.065, 10, 8), mat(c)); ball.position.y = h + 0.04; ball.castShadow = true;
    return grp(at(cyl(0.04, 0.045, h, c, 10, { pivot: 'bottom' }), 0, 0, 0), at(cyl(0.052, 0.052, 0.035, c, 10, { pivot: 'bottom' }), 0, h - 0.02, 0), at(cyl(0.043, 0.043, 0.07, '#F4F1E8', 10, { pivot: 'bottom' }), 0, h - 0.2, 0), ball);
  },

  // The white bands of a barrister's gown (a « rabat »): two pale tabs under the chin, unlit, to pin on a shadow. Origin: the knot; they hang down -Y; front +Z.
  rabat(o) {
    const s = o.s ?? 1, g = grp(), m = flat(o.color || '#F4F1E8');
    for (const sg of [-1, 1]) { const q = new THREE.Mesh(new THREE.PlaneGeometry(0.05, 0.16), m); q.position.set(sg * 0.03, -0.08, 0); q.rotation.z = sg * 0.1; q.castShadow = false; g.add(q); const b = q.clone(); b.rotation.y = PI; g.add(b); }
    g.scale.setScalar(s); return g;
  },
};
