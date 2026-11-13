// « La photocopieuse » (story 49): a man sits on the office photocopier; it copies him whole; the copy comes out of the tray; HR hires it (a copy
// costs only paper), then runs off five hundred, double-sided to save; he is fired: not conforming to the original, too thick; his complaint is
// photocopied five hundred times; since then he puts paper in the machine.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, ease, clamp01, rng } from './style.js';
import { grp, at, label, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const list = v => [].concat(v ?? []);
const grey = v => `rgb(${v},${v},${v})`;

// the man as a black-and-white photocopy, drawn flat (his box head and stubble, the suit, the tie): the cutouts of the copy fountain
function drawCopyMan(c, W, H, back = false, sheet = false, painted = false) {
  c.clearRect(0, 0, W, H);
  if (sheet) { c.fillStyle = '#F7F6F1'; c.fillRect(W * 0.03, H * 0.005, W * 0.94, H * 0.99); c.strokeStyle = grey(170); c.lineWidth = Math.max(1, W * 0.008); c.strokeRect(W * 0.03, H * 0.005, W * 0.94, H * 0.99); }   // (pass 2 of 49) o.sheet: printed on a white sheet with its margin (one design for every copy)
  if (back && back !== 'face') { c.fillStyle = grey(232); c.fillRect(W * 0.1, H * 0.03, W * 0.8, H * 0.95); return; }   // the blank back of a single-sided copy
  const R = (x, y, w, h, v) => { c.fillStyle = grey(v); c.fillRect(W * x, H * y, W * w, H * h); };
  R(0.36, 0.62, 0.11, 0.35, 58); R(0.53, 0.62, 0.11, 0.35, 58); R(0.32, 0.955, 0.16, 0.035, 25); R(0.52, 0.955, 0.16, 0.035, 25);   // legs, shoes
  c.fillStyle = grey(66); c.beginPath(); c.moveTo(W * 0.16, H * 0.3); c.lineTo(W * 0.84, H * 0.3); c.lineTo(W * 0.71, H * 0.66); c.lineTo(W * 0.29, H * 0.66); c.closePath(); c.fill();   // the jacket
  R(0.09, 0.31, 0.09, 0.31, 66); R(0.82, 0.31, 0.09, 0.31, 66); R(0.09, 0.61, 0.09, 0.05, 196); R(0.82, 0.61, 0.09, 0.05, 196);   // arms, hands
  c.fillStyle = grey(238); c.beginPath(); c.moveTo(W * 0.41, H * 0.3); c.lineTo(W * 0.59, H * 0.3); c.lineTo(W * 0.5, H * 0.47); c.closePath(); c.fill();   // the shirt
  R(0.475, 0.31, 0.05, 0.21, 112);                                                                                             // the tie
  R(0.455, 0.255, 0.09, 0.05, 186); R(0.35, 0.025, 0.3, 0.24, 200); R(0.35, 0.025, 0.3, 0.05, 38);                               // neck, head, hair
  if (painted) {   // (pass 3 of 49) the same face as the printed copy (the hero's painted face in greys): white eyes under heavy lids, small pupils, slanted brows
    const E = (cx) => { c.fillStyle = grey(244); c.beginPath(); c.ellipse(W * cx, H * 0.148, W * 0.034, H * 0.017, 0, 0, TAU); c.fill(); c.fillStyle = grey(150); c.fillRect(W * (cx - 0.036), H * 0.128, W * 0.072, H * 0.014);
      c.fillStyle = grey(16); c.beginPath(); c.arc(W * (cx + 0.004), H * 0.151, W * 0.011, 0, TAU); c.fill(); };
    E(0.44); E(0.56); c.fillStyle = grey(30); c.save(); c.translate(W * 0.44, H * 0.118); c.rotate(-0.12); c.fillRect(-W * 0.04, -H * 0.005, W * 0.08, H * 0.01); c.restore();
    c.save(); c.translate(W * 0.56, H * 0.118); c.rotate(0.12); c.fillRect(-W * 0.04, -H * 0.005, W * 0.08, H * 0.01); c.restore(); R(0.465, 0.215, 0.07, 0.008, 40);
  } else { R(0.40, 0.115, 0.07, 0.012, 22); R(0.53, 0.115, 0.07, 0.012, 22); R(0.425, 0.14, 0.03, 0.022, 22); R(0.555, 0.14, 0.03, 0.022, 22); R(0.455, 0.215, 0.09, 0.009, 30); }   // brows, eyes, mouth
  c.fillStyle = grey(120); for (let i = 0; i < 30; i++) c.fillRect(W * (0.38 + ((i * 37) % 24) / 100), H * (0.19 + ((i * 13) % 6) / 100), Math.max(1, W * 0.006), Math.max(1, W * 0.006));   // stubble
  c.strokeStyle = grey(18); c.lineWidth = Math.max(1, W * 0.01); c.strokeRect(W * 0.35, H * 0.025, W * 0.3, H * 0.24);
}

export const PHOTOCOPIE_PROPS = {
  // An office photocopier (front +Z, about 1.1 m wide, its glass at 0.97 m): a beige body, three paper drawers, the glass under a lid hinged at the
  // back (o.lid: its opening in radians, 0 = shut; or keys o.lidKeys [[t, rad]], eased 0.25 s), a control panel at the front right with a small
  // green screen and a big green button, the output tray on its right side (+X). o.scanAt (t or list): the green light bar sweeps under the glass
  // (o.scanDur 0.6 s) with a glow escaping round whatever sits on it; o.sheetsAt (t or list): a sheet slides out onto the tray; o.drawerAt: the
  // bottom drawer slides out (o.drawerCloseAt: back in). userData.top: the glass, userData.tray: the tip of the tray.
  photocopier(o) {
    const g = grp(), W = 1.1, H = 0.95, D = 0.7, body = o.color || '#E6E1D5'; let btn = null;
    g.add(at(box(W, H, D, body, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(W + 0.02, 0.06, D + 0.02, '#9A958B', { pivot: 'bottom' }), 0, 0, 0));
    const drawers = [0.14, 0.34, 0.54].map((y, i) => { const d = grp(at(box(W - 0.1, 0.17, 0.04, '#D8D2C4', { outline: 0.006 }), 0, 0, 0), at(box(0.22, 0.03, 0.03, '#6E6A62'), 0, 0.03, 0.03)); d.position.set(0, y + 0.085, D / 2 + 0.01); g.add(d); return d; });
    const glass = new THREE.Mesh(new THREE.BoxGeometry(W - 0.12, 0.012, D - 0.12), new THREE.MeshLambertMaterial({ color: '#2E3A44', transparent: true, opacity: 0.85 })); glass.position.set(0, H + 0.006, 0); g.add(glass);
    const bar = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.008, D - 0.14), new THREE.MeshBasicMaterial({ color: '#7DFF6A', toneMapped: false })); bar.position.set(0, H - 0.004, 0); bar.userData.noAO = true; bar.visible = false; g.add(bar);
    const glowM = new THREE.MeshBasicMaterial({ color: '#8CFF78', transparent: true, opacity: 0.0, depthWrite: false, toneMapped: false, side: THREE.DoubleSide });
    const glow = new THREE.Mesh(new THREE.BoxGeometry(W + 0.06, 0.16, D + 0.06), glowM); glow.position.set(0, H + 0.08, 0); glow.userData.noAO = true; glow.visible = false; g.add(glow);
    const lid = grp(at(box(W - 0.02, 0.06, D - 0.02, '#D9D3C6', { outline: 0.008 }), 0, 0.03, (D - 0.02) / 2), at(box(W - 0.12, 0.005, D - 0.14, '#F2F1EC'), 0, -0.003, (D - 0.02) / 2));   // the white pad under the lid
    lid.position.set(0, H + 0.012, -D / 2 + 0.01); g.add(lid);
    const panel = grp(at(box(0.36, 0.1, 0.2, '#CFC9BC', { outline: 0.006 }), 0, 0.05, 0), at(box(0.16, 0.012, 0.09, '#2D4F3A', { emissive: '#1F5C36' }), -0.07, 0.106, 0), (btn = at(cyl(o.btnR ?? 0.035, o.btnR ?? 0.035, 0.03, '#33B24A', 14), 0.1, 0.11, 0.02)));   // (pass 3 of 49) o.btnR, o.pressAt
    panel.position.set(W / 2 - 0.2, H, D / 2 - 0.02); panel.rotation.x = 0.3; g.add(panel);
    if (btn?.material) btn.material = btn.material.clone();   // its own material: the press lights this button only
    g.add(at(box(0.36, 0.025, 0.4, '#CFC9BC', { outline: 0.006 }), W / 2 + 0.17, 0.6, 0.0, 0, 0, -0.18), at(box(0.04, 0.2, 0.42, '#CFC9BC'), W / 2 + 0.02, 0.62, 0));   // the output tray
    const sheets = list(o.sheetsAt).map(() => { const s = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.004, 0.21), mat('#FAFAF7')); s.visible = false; g.add(s); return s; });
    const lk = o.lidKeys || [[0, o.lid ?? 0]];
    const lidAt = t => { let v = lk[0][1]; for (let i = 1; i < lk.length; i++) { const [t1, v1] = lk[i]; if (t < t1) break; v = v + (v1 - v) * ease.inOut(clamp01((t - t1) / 0.25)); } return v; };
    g.userData.update = t => {
      lid.rotation.x = -lidAt(t);
      if (btn) { const pr = list(o.pressAt).some(a => t >= a && t < a + 0.16); btn.position.y = pr ? 0.098 : 0.11; btn.material.emissive?.set(pr ? '#4CFF66' : '#000000'); }
      const sa = list(o.scanAt).find(a => t >= a && t < a + (o.scanDur ?? 0.6)); bar.visible = sa != null; glow.visible = sa != null;
      if (sa != null) { const u = (t - sa) / (o.scanDur ?? 0.6); bar.position.x = (-0.5 + u) * (W - 0.16); glowM.opacity = 0.22 + 0.12 * Math.sin(u * 40); glow.scale.set(1, 1 + 0.3 * Math.sin(u * PI), 1); }
      list(o.sheetsAt).forEach((a, i) => { const u = clamp01((t - a) / 0.28), s = sheets[i]; s.visible = t >= a; if (!s.visible) return; s.position.set(W / 2 + 0.05 + 0.24 * ease.out(u), 0.63 + 0.012 * i - 0.05 * ease.out(u), 0); s.rotation.z = -0.18; });
      if (o.drawerAt != null) { const u = ease.out(clamp01((t - o.drawerAt) / 0.3)) - (o.drawerCloseAt != null ? ease.in(clamp01((t - o.drawerCloseAt) / 0.25)) : 0); drawers[0].position.z = D / 2 + 0.01 + 0.4 * u; }
    };
    g.userData.update(0); g.userData.top = [0, H + 0.012, 0]; g.userData.tray = [W / 2 + 0.33, 0.6, 0]; return g;
  },

  // A plane of green scanning light (o.w × o.d) that climbs from o.y0 to o.y1 between o.at and o.at + o.dur (a copier scanning a whole man); a flicker
  scanPlane(o) {
    const w = o.w ?? 1.0, d = o.d ?? 0.7, g = grp(), m = new THREE.MeshBasicMaterial({ color: o.color || '#7DFF6A', transparent: true, opacity: 0.55, depthWrite: false, toneMapped: false, side: THREE.DoubleSide });
    const pl = new THREE.Mesh(new THREE.PlaneGeometry(w, d), m); pl.rotation.x = -PI / 2; pl.userData.noAO = true; g.add(pl);
    const edge = new THREE.Mesh(new THREE.BoxGeometry(w, 0.012, 0.012), new THREE.MeshBasicMaterial({ color: '#D8FFD0', toneMapped: false })); edge.position.z = d / 2; g.add(edge);
    g.userData.update = t => { const u = (t - (o.at ?? 0)) / (o.dur ?? 0.6); g.visible = u >= 0 && u <= 1; if (!g.visible) return; g.position.y = (o.y0 ?? 0) + ((o.y1 ?? 2.4) - (o.y0 ?? 0)) * ease.inOut(u); m.opacity = 0.45 + 0.15 * Math.sin(t * 70); };
    g.userData.update(0); return g;
  },

  // Five hundred copies of him: flat black-and-white cutouts of the man (o.w × o.h) shot out of o.from one after the other between o.t0 and o.t1,
  // each on an arc (o.flight 0.55 s), spinning, to land upright on its spot of a grid (o.grid {x0, z0, dx, dz, cols}, facing o.face rad), then stand there
  // with a little paper flutter. o.n cutouts; o.recto: the man on both faces (double-sided), else a blank back. o.start: the ones already standing.
  copyFountain(o) {
    const n = o.n ?? 30, w = o.w ?? 0.85, h = o.h ?? 2.1, g = grp(), r = rng(o.seed ?? 49);
    const mk = back => { const m = canvasPlane(w, h, (c, W, H) => drawCopyMan(c, W, H, back, !!o.sheet, !!o.painted), { res: 256, transparent: true }); if (o.opaque) { m.material.transparent = false; m.material.alphaTest = 0.5; m.material.depthWrite = true; } return m; };   // (pass 3 of 49) o.painted, o.opaque
    const front = mk(false), backM = o.recto ? mk('face') : mk(true);
    if (o.cool) { front.material.color.set(o.cool); backM.material.color.set(o.cool); }   // (pass 2 of 49) o.cool: a cool cast on the grey prints (under the warm grade they read sepia)
    const G = o.grid || { x0: 0, z0: 0, dx: 0.7, dz: 0.6, cols: 6 }, F = o.from || [0, 0.6, 0], fl = o.flight ?? 0.55, st = o.start ?? 0;
    const cuts = Array.from({ length: n }, (_, i) => { const c = grp(front.clone(), at(backM.clone(), 0, 0, -0.002, 0, PI, 0)); c.children.forEach(m => m.position.y = h / 2); g.add(c);
      const col = i % G.cols, row = Math.floor(i / G.cols); return { c, tx: G.x0 + col * G.dx + (r() - 0.5) * 0.08, tz: G.z0 + row * G.dz + (r() - 0.5) * 0.06, ta: i < st ? -10 : (o.t0 ?? 0) + ((o.t1 ?? 1) - (o.t0 ?? 0)) * (i - st) / Math.max(1, n - st - 1), spin: (r() < 0.5 ? -1 : 1) * (1 + Math.floor(r() * 2)), ph: r() * TAU }; });
    g.userData.update = t => { for (const q of cuts) { const u = (t - q.ta) / fl;
      if (u < 0) { q.c.visible = false; continue; } q.c.visible = true;
      if (u >= 1) { q.c.position.set(q.tx, 0, q.tz); q.c.rotation.set(0.03 * Math.sin(t * 3.1 + q.ph), (o.face ?? 0) + 0.06 * Math.sin(t * 1.7 + q.ph), 0); continue; }
      const e = ease.out(u); q.c.position.set(F[0] + (q.tx - F[0]) * u, F[1] * (1 - u) + 1.6 * Math.sin(PI * u), F[2] + (q.tz - F[2]) * u);
      const fl2 = (o.flutter ?? 0) * Math.sin(PI * u);   // (pass 3 of 49) o.flutter: the sheets rock as they fly (rigid boards before)
      q.c.rotation.set(PI / 2 * (1 - e) * 0.9 + fl2 * Math.sin(u * 26 + q.ph), (o.face ?? 0) + q.spin * TAU * (1 - e), 0.4 * Math.sin(u * PI) + fl2 * Math.sin(u * 19 + 2 * q.ph)); } };
    g.userData.update(0); return g;
  },

  // Sheets of paper (0.21 × 0.3, o.text on them) shot out of o.from between o.t0 and o.t1 (o.n of them), raining onto a pile round o.pile [x, z] (radius
  // o.r) that grows into a mound o.pileH high by o.t1 + 0.3: a man can be buried in his own complaint
  paperFountain(o) {
    const n = o.n ?? 70, g = grp(), r = rng(o.seed ?? 7), F = o.from || [0, 0.6, 0], PL = o.pile || [0, 0], R = o.r ?? 0.7, PH = o.pileH ?? 1.2;
    const tex = canvasPlane(0.21, 0.3, (c, W, H) => { c.fillStyle = '#FAFAF7'; c.fillRect(0, 0, W, H); c.fillStyle = '#C8202A'; c.font = `900 ${Math.round(H * 0.07)}px Arial`; c.textAlign = 'center'; c.fillText(o.text ?? 'RÉCLAMATION', W / 2, H * 0.16);
      c.fillStyle = '#9A9A9A'; for (let i = 0; i < 9; i++) c.fillRect(W * 0.12, H * (0.28 + i * 0.07), W * (0.76 - (i % 3) * 0.12), Math.max(1, H * 0.012)); }, { res: 128 });
    const mound = new THREE.Mesh(new THREE.ConeGeometry(1, 1, 14, 1, true), mat('#F4F3EE')); mound.position.set(PL[0], 0, PL[1]); g.add(mound);
    // (pass 2 of 49) o.stack: the pile built of sheets stacked with jagged edges (o.stackN, 110) instead of a smooth cone (it read as a ball gown); o.rain: the
    // sheets fall from above the pile (o.rainH, 3.4 m) fluttering, instead of arcing out of the tray
    const stackS = []; if (o.stack) { const sm = mat('#F6F5F0'), sm2 = mat('#E6E4DC'), NS = o.stackN ?? 110;
      for (let i = 0; i < NS; i++) { const y = (i + 0.5) / NS * PH, rr = R * (1 - 0.7 * y / PH) * (0.3 + 0.7 * r()), a = r() * TAU, b = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.022, 0.3), i % 3 ? sm : sm2);
        b.position.set(PL[0] + Math.cos(a) * rr, y, PL[1] + Math.sin(a) * rr); b.rotation.set((r() - 0.5) * 0.3, r() * TAU, (r() - 0.5) * 0.3); b.castShadow = true; g.add(b); stackS.push({ b, y }); } }
    const S = Array.from({ length: n }, (_, i) => { const m = tex.clone(); g.add(m); const a = r() * TAU, rr = Math.sqrt(r()) * R; return { m, ta: (o.t0 ?? 0) + ((o.t1 ?? 1) - (o.t0 ?? 0)) * i / n, x: PL[0] + Math.cos(a) * rr, z: PL[1] + Math.sin(a) * rr, rr, sp: (r() - 0.5) * 12, ph: r() * TAU }; });
    g.userData.update = t => { const k = clamp01((t - (o.t0 ?? 0)) / (((o.t1 ?? 1) + 0.3) - (o.t0 ?? 0))), mh = PH * ease.out(k);
      mound.visible = !o.stack && mh > 0.02; mound.scale.set(R * (0.6 + 0.4 * k), mh, R * (0.6 + 0.4 * k)); mound.position.y = mh / 2; for (const q of stackS) q.b.visible = q.y <= mh;
      for (const s of S) { const u = (t - s.ta) / 0.6; if (u < 0) { s.m.visible = false; continue; } s.m.visible = true;
        const top = Math.max(0, mh * (1 - s.rr / (R * (0.6 + 0.4 * k) + 1e-3))) + 0.01;
        if (u >= 1) { s.m.position.set(s.x, top, s.z); s.m.rotation.set(-PI / 2 + 0.3 * Math.sin(s.ph), 0, s.ph); continue; }
        if (o.rain) { const H0 = o.rainH ?? 3.4, e = u * u, fl = 0.18 * Math.sin(u * TAU * 1.5 + s.ph) * (1 - u); s.m.position.set(s.x + fl, H0 + (top - H0) * e, s.z + 0.6 * fl); s.m.rotation.set(-PI / 2 + 0.7 * Math.sin(u * TAU * 1.5 + s.ph) * (1 - u), s.ph, 0.4 * Math.cos(u * TAU + s.ph) * (1 - u)); continue; }   // falling from above, fluttering
        s.m.position.set(F[0] + (s.x - F[0]) * u, F[1] + (top - F[1]) * u + 1.2 * Math.sin(PI * u), F[2] + (s.z - F[2]) * u); s.m.rotation.set(u * s.sp, u * s.sp * 0.7, s.ph); } };
    g.userData.update(0); return g;
  },

  // A big steel caliper (pied à coulisse), its bar along +X (o.len 1.0 m), the jaws hanging down (-Y) from it; the sliding jaw at o.gap metres from
  // the fixed one, or keys o.gapKeys [[t, gap]] (eased 0.2 s); the readout on the slider shows o.text (or the gap in cm). Pivot at the fixed jaw's top.
  caliper(o) {
    const L = o.len ?? 1.0, jaw = o.jaw ?? 0.3, g = grp(), steel = '#B9BEC4';
    g.add(at(box(L, 0.05, 0.02, steel, { outline: 0.004 }), L / 2, 0, 0)); for (let i = 0; i < 20; i++) g.add(at(box(0.004, i % 5 ? 0.012 : 0.022, 0.003, '#2A2C31'), 0.05 + i * (L - 0.1) / 20, 0.012, 0.012));
    g.add(at(box(0.04, jaw, 0.02, steel, { outline: 0.004, pivot: 'top' }), 0.02, -0.025, 0));
    const slide = grp(at(box(0.1, 0.09, 0.035, '#9AA0A7', { outline: 0.004 }), 0, 0, 0), at(box(0.04, jaw, 0.02, steel, { outline: 0.004, pivot: 'top' }), -0.03, -0.045, 0)); g.add(slide);
    let cur = null; const DW = o.dispW ?? 0.09, disp = canvasPlane(DW, DW * 0.55, () => {}, { res: 256 }); disp.position.set(0, 0.012 + (DW > 0.1 ? DW * 0.3 : 0), 0.019); disp.rotation.y = o.dispRy ?? 0; slide.add(disp);   // (pass 3 of 49) o.dispRy: the readout turned toward the lens   // o.dispW: a bigger readout
    const draw = txt => { const c = disp.material.map.image, x = c.getContext('2d'); x.fillStyle = '#C9E3C6'; x.fillRect(0, 0, c.width, c.height); x.fillStyle = '#14161A'; x.font = `900 ${Math.round(c.height * 0.62)}px Arial`; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(txt, c.width / 2, c.height * 0.55); disp.material.map.needsUpdate = true; };
    const gk = o.gapKeys || [[0, o.gap ?? 0.3]];
    const gapAt = t => { let v = gk[0][1]; for (let i = 1; i < gk.length; i++) { const [t1, v1] = gk[i]; if (t < t1) break; v = v + (v1 - v) * ease.inOut(clamp01((t - t1) / (o.gapEase ?? 0.2))); } return v; };   // (pass 2 of 49) o.gapEase: a snap (0.05) instead of 0.2 s
    g.userData.update = t => { const gp = gapAt(t); slide.position.x = 0.07 + gp; const txt = o.text ? (typeof o.text === 'string' ? o.text : (o.text.find(([a]) => t >= a) || o.text[0])[1]) : `${Math.round(gp * 100)} cm`; if (txt !== cur) { cur = txt; draw(txt); } };
    g.userData.update(0); g.userData.grip = [L * 0.75, 0, 0]; return g;
  },

  // A ream of paper (500 sheets): a white block in a coloured wrapper with a label; pivot at its bottom
  paperReam(o) {
    const c = o.color || '#2F7F5C', g = grp(at(box(0.3, 0.06, 0.21, '#FAFAF7', { pivot: 'bottom', outline: 0.004 }), 0, 0, 0), at(box(0.302, 0.05, 0.16, c, { pivot: 'bottom' }), 0, 0.005, 0));
    g.add(at(label(o.text ?? '500 FEUILLES', 0.2, 0.035, { bg: '#FFFFFF', fg: '#14161A' }), 0, 0.032, 0.106));
    g.userData.grip = [0, 0.03, 0]; return g;
  },

  // A red rubber-stamp mark (o.text, e.g. NON CONFORME) on a transparent plane o.w wide, tilted o.rot; from o.at it lands with a little pop
  // (named stampPop: as stampMark it replaced the older stories' stampMark, of other options, in the merged prop table)
  stampPop(o) {
    const w = o.w ?? 0.3, h = w * 0.36, g = grp(), pl = canvasPlane(w, h, (c, W, H) => { c.strokeStyle = '#D21E1E'; c.lineWidth = H * 0.08; c.strokeRect(H * 0.06, H * 0.06, W - H * 0.12, H - H * 0.12);
      c.fillStyle = '#D21E1E'; c.font = `900 ${Math.round(H * 0.46)}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.text ?? 'NON CONFORME', W / 2, H * 0.54, W * 0.9); }, { res: 512, transparent: true });
    pl.rotation.z = o.rot ?? -0.15; pl.userData.noAO = true; g.add(pl);
    g.userData.update = t => { const u = (t - (o.at ?? 0)) / 0.12; g.visible = u >= 0; if (!g.visible) return; const s = u < 1 ? 1.4 - 0.4 * ease.out(u) : 1; g.scale.setScalar(s); };
    g.userData.update(0); return g;
  },

  // His face printed on the back of a flat copy (double-sided): a grey painted face on a plane (o.w × o.h), front +Z; hang it on the back of the head
  backFace(o) {
    const w = o.w ?? 0.3, h = o.h ?? 0.42;
    const pl = canvasPlane(w, h, (c, W, H) => { c.fillStyle = grey(200); c.fillRect(0, 0, W, H); c.fillStyle = grey(38); c.fillRect(0, 0, W, H * 0.2);
      c.fillStyle = grey(12); c.fillRect(W * 0.14, H * 0.36, W * 0.28, H * 0.06); c.fillRect(W * 0.58, H * 0.36, W * 0.28, H * 0.06); c.fillRect(W * 0.22, H * 0.47, W * 0.14, H * 0.11); c.fillRect(W * 0.64, H * 0.47, W * 0.14, H * 0.11); c.fillRect(W * 0.3, H * 0.79, W * 0.4, H * 0.05);   // (first look) bolder: at phone size the thin features vanished
      c.strokeStyle = grey(15); c.lineWidth = W * 0.04; c.strokeRect(W * 0.02, H * 0.02, W * 0.96, H * 0.96);
      c.fillStyle = grey(120); for (let i = 0; i < 40; i++) c.fillRect(W * (0.15 + ((i * 37) % 70) / 100), H * (0.66 + ((i * 13) % 12) / 100), Math.max(1, W * 0.02), Math.max(1, W * 0.02)); }, { res: 256 });
    pl.userData.noAO = true; const g = grp(pl);
    if (o.blinkAt) { const lid = grp(at(new THREE.Mesh(new THREE.PlaneGeometry(w * 0.3, h * 0.13), new THREE.MeshBasicMaterial({ color: '#C8C8C8' })), -w * 0.21, h * 0.04, 0.002), at(new THREE.Mesh(new THREE.PlaneGeometry(w * 0.3, h * 0.13), new THREE.MeshBasicMaterial({ color: '#C8C8C8' })), w * 0.21, h * 0.04, 0.002),
        at(new THREE.Mesh(new THREE.PlaneGeometry(w * 0.26, h * 0.025), new THREE.MeshBasicMaterial({ color: '#141414' })), -w * 0.21, h * 0.0, 0.003), at(new THREE.Mesh(new THREE.PlaneGeometry(w * 0.26, h * 0.025), new THREE.MeshBasicMaterial({ color: '#141414' })), w * 0.21, h * 0.0, 0.003));
      lid.traverse(m => { m.userData.noAO = true; }); g.add(lid); const B = [].concat(o.blinkAt);   // (pass 2 of 49) o.blinkAt [t...]: the printed back face blinks (closed eyes drawn over its eyes for 0.14 s)
      g.userData.update = t => { lid.visible = B.some(b => t >= b && t < b + 0.14); }; g.userData.update(0); }
    return g;
  },
};
