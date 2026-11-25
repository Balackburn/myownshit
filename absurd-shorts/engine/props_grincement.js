// « Le grincement » (story 98): this man's door squeaks, and for the State it is a language. The neighbour complained about the noise, three
// linguists declared it a language spoken by one door, threatened, so oiling it is forbidden and the gendarmes seize his oil can; closing the door
// would cut it off, so he lives with it open; the whole country learns the squeak for the bac (the neighbour fails three times and moves out); the
// president gives his New Year wishes squeaking; ten years later the dictionary: a thousand pages, one word, which means « de l'huile ».
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
// The squeak is one big sprite (three thick saturated arcs with a dark outline, popping and wobbling off the hinge), always paired with a sound
// cue in the script. The oil can is a big saturated red can that reads at phone size, drawn after the clear bag's film so the film never washes it.
import * as THREE from 'three';
import { box, cyl, sphere, mat } from './style.js';
import { grp, at, canvasPlane, rod } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = (x, c = 2.2) => { const u = clamp01(x); return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const lerp = (a, b, u) => a + (b - a) * u;
const V2 = (x, y) => new THREE.Vector2(x, y);
// [[t, v], ...] -> v at t, smoothstep between keys (a key [t, v, 'lin'] makes its segment linear)
const keyAt = (K, t, d = 0) => {
  if (!K || !K.length) return d;
  if (t <= K[0][0]) return K[0][1];
  for (let i = 1; i < K.length; i++) if (t < K[i][0]) { const u = (t - K[i - 1][0]) / Math.max(1e-6, K[i][0] - K[i - 1][0]); return lerp(K[i - 1][1], K[i][1], K[i][2] === 'lin' ? u : smooth(u)); }
  return K[K.length - 1][1];
};
// a damped wobble summed over [[t0, amp, freq, decay], ...]
const rattle = (R, t) => { let s = 0; for (const [t0, amp, f, dk] of R || []) { const u = t - t0; if (u > 0) s += amp * Math.sin(u * (f ?? 18)) * Math.exp(-u * (dk ?? 3.5)); } return s; };
const INK = '#1B1E2A';
const tex = cv => { const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t; };
const canvas = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
// text that fits a box (measureText), centred
const fitText = (c, s, x, y, maxW, maxH, weight = 900, family = 'Arial') => { let fs = maxH; c.font = `${weight} ${fs}px ${family}`; const w = c.measureText(s).width; if (w > maxW) { fs *= maxW / w; c.font = `${weight} ${fs}px ${family}`; } c.fillText(s, x, y); return fs; };
// an oil drop path (tip up) centred at (x, y), height h
const dropPath = (c, x, y, h) => { const r = h * 0.34; c.beginPath(); c.moveTo(x, y - h * 0.5); c.bezierCurveTo(x + r * 0.35, y - h * 0.22, x + r * 1.05, y + h * 0.02, x + r, y + h * 0.17); c.arc(x, y + h * 0.17, r, 0, PI); c.bezierCurveTo(x - r * 1.05, y + h * 0.02, x - r * 0.35, y - h * 0.22, x, y - h * 0.5); c.closePath(); };
const drawDrop = (c, x, y, h, fill = '#E8A818', edge = INK, lw = 0.07) => {
  dropPath(c, x, y, h); c.fillStyle = fill; c.fill(); c.lineWidth = h * lw; c.strokeStyle = edge; c.lineJoin = 'round'; c.stroke();
  c.fillStyle = 'rgba(255,255,255,0.75)'; c.beginPath(); c.ellipse(x - h * 0.12, y + h * 0.08, h * 0.05, h * 0.11, 0.35, 0, TAU); c.fill();
};

// (round 1 fix) a soft additive glow: a square plane o size wide with a radial gradient in colour col, peak opacity op, at position p (faces +Z)
const glowPlane = (size, col, op, p) => {
  const N = 128, cv = canvas(N, N), c = cv.getContext('2d'), gr = c.createRadialGradient(N / 2, N / 2, 0, N / 2, N / 2, N / 2);
  gr.addColorStop(0, col); gr.addColorStop(0.35, col); gr.addColorStop(1, 'rgba(0,0,0,0)'); c.fillStyle = gr; c.fillRect(0, 0, N, N);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(size, size), new THREE.MeshBasicMaterial({ map: tex(cv), transparent: true, opacity: op, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false, side: THREE.DoubleSide }));
  m.position.set(p[0], p[1], p[2]); m.renderOrder = 3; return m;
};

export const GRINCEMENT_PROPS = {

  // ---------------------------------------------------------------- the squeak (pivot at the hinge; give the prop face: 'camera')
  // Three thick arcs ))) opening to o.side (1: toward +X of the prop, i.e. the image right once turned to the camera; -1: the left), o.size (0.7 m)
  // across: a dark ink outline, a red-orange body and a yellow core with a white glint. Each time in o.at it pops (the arcs grow one after the other
  // with an overshoot), wobbles off the hinge (rocking, jittering, drifting outward) and fades after o.life (0.72 s); o.amp: a size factor per pop;
  // o.onTop: drawn over everything (a hinge hidden by its own door frame from a low camera)
  grinSqueak(o) {
    const S = o.size ?? 0.7, side = o.side ?? 1, life = o.life ?? 0.72, pops = (o.at || []).map((t, i) => [t, (o.amp || [])[i] ?? 1]).sort((a, b) => a[0] - b[0]);
    const g = grp(), inner = grp(); g.add(inner); if (side < 0) inner.scale.x = -1;
    const arcs = [0, 1, 2].map(i => {
      const N = 256, cv = canvas(N, N), c = cv.getContext('2d'), cx = N * 0.08, cy = N / 2, R = N * (0.25 + i * 0.22), a = 0.95 - i * 0.165;
      const stroke = (w, col, r = R, a0 = -a, a1 = a) => { c.strokeStyle = col; c.lineWidth = w; c.lineCap = 'round'; c.beginPath(); c.arc(cx, cy, r, a0, a1); c.stroke(); };
      stroke(N * 0.16, INK); stroke(N * 0.11, o.edge || '#FF4316'); stroke(N * 0.058, o.color || '#FFD60A'); stroke(N * 0.02, 'rgba(255,255,255,0.9)', R - N * 0.012, -a + 0.12, -a + 0.5);
      const m = new THREE.Mesh(new THREE.PlaneGeometry(S, S), new THREE.MeshBasicMaterial({ map: tex(cv), transparent: true, depthWrite: false, depthTest: !o.onTop, toneMapped: false, side: THREE.DoubleSide }));
      m.renderOrder = 8; m.position.x = S * (0.5 - 0.08); const h = grp(m); inner.add(h); return { h, m };
    });
    g.userData.update = t => {
      let p = null; for (const q of pops) if (t >= q[0]) p = q;
      const u = p ? t - p[0] : -1, on = u >= 0 && u < life; inner.visible = on; if (!on) return;
      const fade = clamp01((life - u) / 0.16), A = p[1];
      inner.rotation.z = 0.22 * Math.sin(u * 21) * Math.exp(-2.0 * u);
      arcs.forEach(({ h, m }, i) => {
        const v = u - i * 0.04, k = v < 0 ? 0.01 : outBack(v / 0.12) * (1 + 0.08 * Math.sin(v * 30 + i) * Math.exp(-2.5 * v)), s = Math.max(0.01, k * (0.7 + 0.3 * fade) * A);
        h.scale.set(s, s * (1 + 0.09 * Math.sin(v * 27 + i * 1.7)), 1); h.position.set(S * 0.14 * u * (1 + i * 0.35), S * 0.035 * Math.sin(v * 37 + i * 2), 0); m.material.opacity = fade;
      });
    };
    g.userData.update(-1); return g;
  },

  // ---------------------------------------------------------------- a house front with its door (pivot on the ground at the door's middle, the
  // street +Z, the wall's face at z 0). o.w (7) x o.h (3.2) wall in o.wall, from x o.x0 (-o.w/2); o.door {w 1.15, h 2.6, color, hinge 'L'|'R' (seen
  // from the street), swing [[t, rad]] (inward, positive opens), open (rad), rattle [[t0, amp, freq, decay]], inside: false | {w, d, wall, floor,
  // light}}; o.windows [{x, y, w, h, kind 'glass'|'open'|'lit'|'night', shutters colour}] ('open': a dark room behind and a sill that sticks out,
  // somebody can stand behind it); o.roof (colour) / o.roof false; o.snow: snow on the eave and the sills; o.num: a house number by the door;
  // o.step: a stone doorstep; o.trim (frames); o.box (m): side walls that deep. userData.hinge: the hinge's [x, z] in the prop's frame.
  grinFacade(o) {
    const W = o.w ?? 7, H = o.h ?? 3.2, T = o.t ?? 0.25, x0 = o.x0 ?? -W / 2, g = grp(), wallC = o.wall || '#F2D58A', trim = o.trim || '#F4F4F0';
    const D = { w: 1.15, h: 2.6, color: '#1F6E7A', hinge: 'L', ...(o.door || {}) }, dw = D.w, dh = D.h, wins = o.windows || [];
    const outline = o.door === false ? [V2(x0, 0), V2(x0 + W, 0), V2(x0 + W, H), V2(x0, H)]
      : [V2(x0, 0), V2(-dw / 2, 0), V2(-dw / 2, dh), V2(dw / 2, dh), V2(dw / 2, 0), V2(x0 + W, 0), V2(x0 + W, H), V2(x0, H)];
    const sh = new THREE.Shape(outline);
    for (const wd of wins) { const p = new THREE.Path(); p.moveTo(wd.x - wd.w / 2, wd.y); p.lineTo(wd.x + wd.w / 2, wd.y); p.lineTo(wd.x + wd.w / 2, wd.y + wd.h); p.lineTo(wd.x - wd.w / 2, wd.y + wd.h); p.lineTo(wd.x - wd.w / 2, wd.y); sh.holes.push(p); }
    const wall = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: T, bevelEnabled: false }), mat(wallC)); wall.position.z = -T; wall.castShadow = wall.receiveShadow = true; g.add(wall);
    // plinth, a band under the eave, the roof
    const plC = o.plinth || '#B9AE9A';
    if (o.door === false) g.add(at(box(W, 0.32, 0.05, plC, { pivot: 'bottom' }), x0 + W / 2, 0, 0.02));
    else { const lw = -dw / 2 - x0 - 0.1, rw = x0 + W - dw / 2 - 0.1; if (lw > 0.05) g.add(at(box(lw, 0.32, 0.05, plC, { pivot: 'bottom' }), x0 + lw / 2, 0, 0.02)); if (rw > 0.05) g.add(at(box(rw, 0.32, 0.05, plC, { pivot: 'bottom' }), x0 + W - rw / 2, 0, 0.02)); }
    if (o.roof !== false) {
      const rc = o.roof || '#B5402F';
      g.add(at(box(W + 0.5, 0.18, 0.12, trim, { outline: 0.006 }), x0 + W / 2, H - 0.05, 0.05), at(box(W + 0.6, 0.16, 0.9, rc, { outline: 0.008 }), x0 + W / 2, H + 0.1, -0.25));
      g.add(at(box(W + 0.6, 0.14, 3.2, rc, { outline: 0.008 }), x0 + W / 2, H + 0.75, -1.55, -0.42, 0, 0));
      if (o.snow) g.add(at(box(W + 0.62, 0.12, 0.92, '#F4F7FA', { noGrain: true }), x0 + W / 2, H + 0.23, -0.25), at(box(W + 0.62, 0.1, 3.2, '#F4F7FA', { noGrain: true }), x0 + W / 2, H + 0.84, -1.5, -0.42, 0, 0));
    }
    // o.box (depth): side walls and a back wall, so the house reads as a volume when it is seen from the side
    if (o.box) { const bd = o.box; for (const x of [x0, x0 + W]) g.add(at(box(0.2, H, bd, wallC, { outline: 0.006 }), x + (x === x0 ? 0.1 : -0.1), H / 2, -T - bd / 2)); g.add(at(box(W, H, 0.2, wallC), x0 + W / 2, H / 2, -T - bd + 0.1)); }
    // windows
    for (const wd of wins) {
      const cx = wd.x, cy = wd.y + wd.h / 2, fw = 0.09, kind = wd.kind || 'glass';
      for (const [x, y, w, h] of [[cx - wd.w / 2 - fw / 2, cy, fw, wd.h + fw * 2], [cx + wd.w / 2 + fw / 2, cy, fw, wd.h + fw * 2], [cx, wd.y + wd.h + fw / 2, wd.w + fw * 2, fw]]) g.add(at(box(w, h, 0.08, trim, { outline: 0.005 }), x, y, 0.03));
      const sillD = kind === 'open' ? 0.34 : 0.16; g.add(at(box(wd.w + 0.3, 0.08, sillD, trim, { outline: 0.006 }), cx, wd.y - 0.03, sillD / 2 - 0.06));
      if (o.snow) g.add(at(box(wd.w + 0.28, 0.05, sillD, '#F4F7FA', { noGrain: true }), cx, wd.y + 0.03, sillD / 2 - 0.06));
      if (kind === 'open') {
        const dd = wd.d ?? 1.4, ic = wd.inside || '#39404E';
        g.add(at(box(wd.w + 0.4, wd.h + 0.6, 0.05, ic), cx, cy, -T - dd), at(box(0.05, wd.h + 0.6, dd, ic), cx - wd.w / 2 - 0.2, cy, -T - dd / 2), at(box(0.05, wd.h + 0.6, dd, ic), cx + wd.w / 2 + 0.2, cy, -T - dd / 2));
        g.add(at(box(wd.w + 0.4, 0.05, dd, '#2E333E'), cx, wd.y + wd.h + 0.3, -T - dd / 2), at(box(wd.w + 0.4, 0.05, dd, '#4A4038'), cx, Math.max(0.03, wd.y - 1.4), -T - dd / 2));
        if (wd.lamp !== false) { const L = new THREE.PointLight('#FFD9A0', wd.lamp ?? 1.6, 3.5, 1.4); L.position.set(cx, cy + 0.3, -T - 0.5); g.add(L); }
      } else {
        const gc = kind === 'lit' ? '#F5CE7A' : kind === 'night' ? '#33456E' : '#A9CCE6';
        g.add(at(box(wd.w, wd.h, 0.03, gc, kind === 'lit' ? { emissive: '#C9922E' } : { emissive: kind === 'night' ? '#141E36' : '#2A4A66' }), cx, cy, -T * 0.5));
        g.add(at(box(0.05, wd.h, 0.05, trim), cx, cy, -T * 0.5 + 0.03), at(box(wd.w, 0.05, 0.05, trim), cx, cy, -T * 0.5 + 0.03));
      }
      if (wd.shutters) for (const sd of [-1, 1]) { const sw = wd.w * 0.52; const s = at(box(sw, wd.h + 0.05, 0.04, wd.shutters, { outline: 0.006 }), cx + sd * (wd.w / 2 + 0.1 + sw / 2), cy, 0.05);
        g.add(s); for (let i = 1; i < 6; i++) g.add(at(box(sw * 0.86, 0.02, 0.01, new THREE.Color(wd.shutters).multiplyScalar(0.78).getStyle()), cx + sd * (wd.w / 2 + 0.1 + sw / 2), wd.y + wd.h * i / 6, 0.075)); }
    }
    if (o.num) g.add(at(box(0.3, 0.3, 0.03, '#1E3E7A', { outline: 0.006 }), dw / 2 + 0.45, 2.0, 0.02), at(canvasPlane(0.26, 0.26, (c, w, h) => { c.fillStyle = '#1E3E7A'; c.fillRect(0, 0, w, h); c.fillStyle = '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, String(o.num), w / 2, h * 0.55, w * 0.8, h * 0.7); }, { res: 128 }), dw / 2 + 0.45, 2.0, 0.037));
    if (o.door === false) return g;
    // the door: a frame, the leaf on its hinge, the doorstep, the room behind
    for (const [x, y, w, h] of [[-dw / 2 - 0.06, dh / 2 + 0.03, 0.12, dh + 0.06], [dw / 2 + 0.06, dh / 2 + 0.03, 0.12, dh + 0.06], [0, dh + 0.06, dw + 0.24, 0.12]]) g.add(at(box(w, h, 0.1, trim, { outline: 0.006 }), x, y, 0.03));
    if (o.step !== false) g.add(at(box(dw + 0.5, 0.14, 0.5, o.stepColor || '#C9C2B2', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0.25));
    const hs = D.hinge === 'R' ? -1 : 1, hx = -hs * dw / 2, piv = grp(); piv.position.set(hx, 0.02, -0.06); g.add(piv);
    const lw = dw - 0.03, lh = dh - 0.04, dc = D.color, dk = new THREE.Color(dc).multiplyScalar(0.78).getStyle(), lf = grp(); lf.position.x = hs * lw / 2; piv.add(lf);
    lf.add(at(box(lw, lh, 0.07, dc, { outline: 0.008, unique: true }), 0, lh / 2, 0));
    // (round 1 fix) four raised panels with pale mouldings round each (two tall above, two short below), so the leaf reads as a panelled door
    const lt = new THREE.Color(dc).lerp(new THREE.Color('#FFFFFF'), 0.32).getStyle();
    for (const f of [1, -1]) {
      for (const [py, ph] of [[lh * 0.69, lh * 0.36], [lh * 0.235, lh * 0.27]]) for (const px of [-lw * 0.205, lw * 0.205]) {
        const pw = lw * 0.3, mt = 0.026;
        lf.add(at(box(pw - 0.03, ph - 0.03, 0.028, dk), px, py, f * 0.045));
        for (const [mx, my, mw, mh] of [[px, py + ph / 2, pw + mt, mt], [px, py - ph / 2, pw + mt, mt], [px - pw / 2, py, mt, ph + mt], [px + pw / 2, py, mt, ph + mt]]) lf.add(at(box(mw, mh, 0.024, lt), mx, my, f * 0.046));
      }
      lf.add(at(sphere(0.055, '#E2B53C', 1), hs * (lw / 2 - 0.12), lh * 0.47, f * 0.07), at(cyl(0.04, 0.04, 0.03, '#C9982E', 8), hs * (lw / 2 - 0.12), lh * 0.47, f * 0.045, PI / 2));
    }
    lf.add(at(box(0.3, 0.06, 0.02, '#C9982E', { outline: 0.004 }), 0, lh * 0.44, 0.05));
    for (const y of [0.35, dh - 0.45]) g.add(at(box(0.05, 0.16, 0.05, '#4A4A50'), hx, y, -0.02));
    const ins = D.inside === false ? null : { w: 3.4, d: 3.6, wall: '#F1E4C8', floor: '#A9805A', light: 3.2, ...(D.inside || {}) };
    if (ins) {
      const iw = ins.w, id = ins.d, z0 = -T, ih = Math.min(H - 0.05, 3.0);
      g.add(at(box(iw, 0.06, id, ins.floor), 0, 0.03, z0 - id / 2), at(box(iw, ih, 0.08, ins.wall), 0, ih / 2, z0 - id), at(box(iw, 0.08, id, '#E9DDC4'), 0, ih, z0 - id / 2));
      for (const sd of [-1, 1]) g.add(at(box(0.08, ih, id, ins.wall), sd * iw / 2, ih / 2, z0 - id / 2));
      g.add(at(box(iw, 0.5, 0.02, ins.band || '#C9B48E'), 0, 0.25, z0 - id + 0.05));
      if (ins.light) { const L = new THREE.PointLight('#FFD8A0', ins.light, 6, 1.3); L.position.set(0, ih - 0.4, z0 - id * 0.45); g.add(L); }
    }
    g.userData.hinge = [hx, -0.06];
    const setA = a => { piv.rotation.y = hs * a; };
    g.userData.update = t => setA((D.swing ? keyAt(D.swing, t, D.open ?? 0) : (D.open ?? 0)) + rattle(D.rattle, t));
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the oil can (pivot under its base, the spout toward +X): a classic burette
  // (round 1 fix: the tall can with a loop handle read as a kettle) (round 2: a drum base, a narrow waist and a slim cone, a brass neck and a big
  // round thumb pump) one long thin spout angled up and out from the top of the neck, no handle; about 0.42 m tall
  // to the spout's tip (o.s scales it in place), o.flip: the spout toward -X. o.over: the bagged copy, drawn after the bag's film (transparent at
  // opacity 1, renderOrder 5).
  grinOilCan(o) {
    const g = grp(), b = grp(); g.add(b); b.scale.setScalar(o.s ?? 1); if (o.flip) b.scale.x *= -1;
    const M = (c, e) => { const m = new THREE.MeshLambertMaterial({ color: c, emissive: e || '#000000', flatShading: true }); if (o.over) { m.transparent = true; m.opacity = 1; m.depthWrite = true; } return m; };
    const mk = (geo, c, x, y, z, e) => { const m = new THREE.Mesh(geo, M(c, e)); m.position.set(x, y, z); m.castShadow = true; if (o.over) m.renderOrder = 5; b.add(m); return m; };
    const red = o.color || '#E0261C', inkM = new THREE.MeshBasicMaterial({ color: INK, side: THREE.BackSide }); if (o.over) { inkM.transparent = true; inkM.opacity = 1; }
    const inked = (m, s = 1.07) => { const i = new THREE.Mesh(m.geometry, inkM); i.scale.setScalar(s); m.add(i); if (o.over) i.renderOrder = 4; return m; };
    // (round 2 fix: the squat cone on a disc read as a bell or a spinning top) one turned profile: a straight drum base, a sharp step in to a narrow
    // waist, a slim cone up to a brass neck; the spout leaves the top of the neck, and a big round thumb pump stands on the shoulder at the back
    const prof = [[0.0, 0.0], [0.136, 0.0], [0.138, 0.012], [0.134, 0.062], [0.112, 0.074], [0.066, 0.086], [0.056, 0.104], [0.05, 0.13], [0.036, 0.172], [0.025, 0.196], [0.0, 0.2]].map(([x, y]) => V2(x, y));
    inked(mk(new THREE.LatheGeometry(prof, 18), red, 0, 0, 0, '#3A0806'), 1.06);
    mk(new THREE.CylinderGeometry(0.1395, 0.1395, 0.016, 18), '#FFC414', 0, 0.038, 0, '#4A3000');
    inked(mk(new THREE.CylinderGeometry(0.022, 0.026, 0.05, 10), '#D9A93A', 0, 0.215, 0, '#3A2A08'), 1.15);
    inked(mk(new THREE.CylinderGeometry(0.03, 0.03, 0.012, 10), '#D9A93A', 0, 0.242, 0, '#3A2A08'), 1.15);
    const glint = mk(new THREE.BoxGeometry(0.016, 0.034, 0.01), '#FFFFFF', -0.07, 0.04, 0.118, '#FFFFFF'); glint.rotation.y = -0.5;
    const glint2 = mk(new THREE.BoxGeometry(0.01, 0.05, 0.01), '#FFFFFF', -0.026, 0.13, 0.04, '#FFFFFF'); glint2.rotation.set(0.25, -0.45, 0);
    const tip = [0.37, 0.43, 0]; const sp = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.016, 1, 6), M('#C9CED4', '#2A2E34')); const a = new THREE.Vector3(0.01, 0.238, 0), d = new THREE.Vector3(...tip).sub(a);
    sp.scale.y = d.length(); sp.position.copy(a).addScaledVector(d, 0.5); sp.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.clone().normalize()); sp.castShadow = true; if (o.over) sp.renderOrder = 5; b.add(sp);
    const spI = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.016, 1, 6), inkM); spI.scale.set(2.0, 1.02, 2.0); sp.add(spI);
    inked(mk(new THREE.CylinderGeometry(0.016, 0.02, 0.07, 8), '#D9A93A', -0.062, 0.135, 0, '#3A2A08'), 1.2).rotation.z = 0.35;
    inked(mk(new THREE.CylinderGeometry(0.04, 0.04, 0.016, 12), '#E8B83C', -0.078, 0.172, 0, '#3A2A08'), 1.15).rotation.z = 0.35;
    const lever = mk(new THREE.BoxGeometry(0.075, 0.012, 0.022), '#D9A93A', -0.04, 0.196, 0, '#3A2A08'); lever.rotation.z = 0.5;
    g.userData.tip = tip.map(v => v * (o.s ?? 1)); return g;
  },

  // ---------------------------------------------------------------- the sealed evidence bag (pivot at its middle, facing +Z; give the prop face:
  // 'camera'): a barely tinted film o.w (0.46) x o.h (0.62) with thick white seams, two diagonal glints, a red-and-white zip strip on top and a red
  // label band at the bottom (o.text 'SCELLÉ', o.num 'N° 98'); the oil can inside (o.can false: empty), drawn after the film. o.open: the zip strip
  // parted and the mouth held open (to catch the can). o.flat [[t, v], ...] (round 1 fix): v 1 squashes the bag flat onto its bottom edge (wide and
  // low), v < 0 stretches it tall (the re-inflation's overshoot).
  grinBag(o) {
    const W = o.w ?? 0.46, H = o.h ?? 0.62, root = grp(), g = grp(); root.add(g);
    const film = new THREE.Mesh(new THREE.BoxGeometry(W, H, 0.05), new THREE.MeshLambertMaterial({ color: '#EAF6FC', transparent: true, opacity: o.opacity ?? 0.16, depthWrite: false, emissive: '#22303A' })); film.renderOrder = 2; g.add(film);
    for (const [x, y, w, h] of [[-W / 2, 0, 0.022, H], [W / 2, 0, 0.022, H], [0, -H / 2, W, 0.022]]) g.add(at(box(w, h, 0.056, '#F6FAFC', { outline: 0.004 }), x, y, 0));
    for (const [x, y, l, rz] of [[-W * 0.33, H * 0.3, H * 0.2, -0.5], [-W * 0.22, H * 0.36, H * 0.11, -0.5]]) { const gl = new THREE.Mesh(new THREE.PlaneGeometry(0.012, l), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.5, depthWrite: false })); gl.position.set(x, y, 0.03); gl.rotation.z = rz; gl.renderOrder = 6; g.add(gl); }
    if (o.open) { for (const sd of [-1, 1]) g.add(at(box(W * 0.5, 0.035, 0.06, '#FFFFFF', { outline: 0.004 }), sd * W * 0.25, H / 2 + 0.02, sd * 0.03, 0.25 * sd)); }
    else { g.add(at(box(W + 0.02, 0.045, 0.07, '#FFFFFF', { outline: 0.004 }), 0, H / 2, 0)); for (let i = 0; i < 6; i++) g.add(at(box(W / 12, 0.047, 0.072, '#D8262C'), -W / 2 + (i + 0.5) * W / 6, H / 2, 0)); }
    const lab = canvasPlane(W * 0.9, H * 0.2, (c, w, h) => { c.fillStyle = '#C8202A'; c.fillRect(0, 0, w, h); c.fillStyle = '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle';
      fitText(c, o.text || 'SCELLÉ', w / 2, h * 0.38, w * 0.86, h * 0.52); c.font = `700 ${h * 0.26}px Arial`; c.fillText(o.num || 'N° 98', w / 2, h * 0.79); }, { res: 256, emissive: 0.25 });
    lab.position.set(0, -H * 0.37, 0.03); lab.renderOrder = 6; g.add(lab);
    if (o.can !== false) { const cn = GRINCEMENT_PROPS.grinOilCan({ over: true, s: o.canS ?? 0.84 }); cn.position.set(-0.1, -H * 0.235, 0.0); cn.rotation.set(0, -0.3, 0.0); g.add(cn); }
    if (o.flat) root.userData.update = t => { const v = keyAt(o.flat, t, 0), sy = 1 - 0.62 * v; g.scale.set(1 + 0.42 * v, sy, 1 + 0.15 * v); g.position.y = -H / 2 * (1 - sy); };
    if (o.flat) root.userData.update(0);
    return root;
  },

  // ---------------------------------------------------------------- the bronze plaque screwed on the door (pivot at its middle, facing +Z): a
  // polished bronze plate o.w (0.78) x o.h (1.0) with a raised border and four screws; on it a big amber oil drop crossed out by a thick red
  // prohibition ring and bar (no words). o.screwAt [t0, t1]: the last screw (o.screw: 0 top left, 1 top right, 2 bottom left, 3 bottom right) spins in.
  grinPlaque(o) {
    const W = o.w ?? 0.78, H = o.h ?? 1.0, g = grp();
    g.add(at(box(W + 0.05, H + 0.05, 0.03, '#6A4518', { outline: 0.006 }), 0, 0, -0.01));
    const face = canvasPlane(W, H, (c, w, h) => {
      const gr = c.createLinearGradient(0, 0, w, h); gr.addColorStop(0, '#E8B860'); gr.addColorStop(0.45, '#B9802E'); gr.addColorStop(0.55, '#F0C878'); gr.addColorStop(1, '#8E5A1E'); c.fillStyle = gr; c.fillRect(0, 0, w, h);
      c.strokeStyle = '#6A4518'; c.lineWidth = w * 0.035; c.strokeRect(w * 0.05, h * 0.04, w * 0.9, h * 0.92); c.strokeStyle = '#FFE2A0'; c.lineWidth = w * 0.01; c.strokeRect(w * 0.075, h * 0.06, w * 0.85, h * 0.88);
      const cx = w / 2, cy = h * 0.5, R = w * 0.36;
      c.fillStyle = '#FFF6E0'; c.beginPath(); c.arc(cx, cy, R, 0, TAU); c.fill();
      drawDrop(c, cx, cy + R * 0.04, R * 1.25, '#E8A818', INK, 0.06);
      c.strokeStyle = '#D81E1E'; c.lineWidth = w * 0.09; c.beginPath(); c.arc(cx, cy, R, 0, TAU); c.stroke();
      c.beginPath(); c.moveTo(cx - R * 0.7, cy - R * 0.7); c.lineTo(cx + R * 0.7, cy + R * 0.7); c.stroke();
      c.strokeStyle = INK; c.lineWidth = w * 0.012; c.beginPath(); c.arc(cx, cy, R + w * 0.05, 0, TAU); c.stroke();
    }, { res: 512, emissive: 0.18 });
    face.position.z = 0.008; g.add(face);
    const screws = [[-1, 1], [1, 1], [-1, -1], [1, -1]].map(([sx, sy]) => { const s = grp(at(cyl(0.028, 0.028, 0.02, '#D9DCDE', 10, { outline: 0.003 }), 0, 0, 0, PI / 2), at(box(0.04, 0.008, 0.006, '#4A4A50'), 0, 0, 0.012)); s.position.set(sx * (W / 2 - 0.06), sy * (H / 2 - 0.06), 0.02); g.add(s); return s; });
    g.userData.update = t => { const S = o.screwAt; if (!S) return; const u = clamp01((t - S[0]) / Math.max(0.05, S[1] - S[0])); const sc = screws[o.screw ?? 3]; sc.rotation.z = -u * 14; sc.position.z = 0.02 + 0.03 * (1 - u); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a small door on a stand (pivot under its base, facing +Z): a frame o.w (0.34)
  // x o.h (0.5) on a little plinth, a leaf hinged on the left (seen from the front) that swings toward the back by o.swing [[t, rad]] or, from o.beats
  // [t, ...], opens to o.amp (1.1 rad) and swings back in o.beatDur (0.45 s). o.ornate: dark wood, gilt frame, a pediment and carved panels.
  grinMiniDoor(o) {
    const W = o.w ?? 0.34, H = o.h ?? 0.5, g = grp(), orn = !!o.ornate, fr = orn ? '#D9AE3A' : (o.frame || '#F4F4F0'), lc = o.color || (orn ? '#5A2E1E' : '#2F7F8C');
    g.add(at(box(W + 0.16, 0.05, 0.16, orn ? '#3A2418' : '#8A6A44', { pivot: 'bottom', outline: 0.004 }), 0, 0, 0));
    for (const [x, y, w, h] of [[-W / 2 - 0.025, H / 2 + 0.05, 0.05, H + 0.05], [W / 2 + 0.025, H / 2 + 0.05, 0.05, H + 0.05], [0, H + 0.075, W + 0.1, 0.05]]) g.add(at(box(w, h, 0.06, fr, { outline: 0.004 }), x, y, 0));
    g.add(at(box(W, H, 0.01, '#20242C'), 0, H / 2 + 0.05, -0.03));
    if (orn) { const tri = new THREE.Shape([V2(-W / 2 - 0.06, 0), V2(W / 2 + 0.06, 0), V2(0, 0.12)]); const pd = new THREE.Mesh(new THREE.ExtrudeGeometry(tri, { depth: 0.05, bevelEnabled: false }), mat(fr)); pd.position.set(0, H + 0.1, -0.025); g.add(pd); g.add(at(sphere(0.025, fr, 1), 0, H + 0.24, 0)); }
    const piv = grp(); piv.position.set(-W / 2, 0.05, 0); g.add(piv);
    const lf = grp(at(box(W - 0.01, H - 0.01, 0.025, lc, { outline: 0.004 }), (W - 0.01) / 2, H / 2, 0)); piv.add(lf);
    const pc = orn ? '#7A4430' : new THREE.Color(lc).multiplyScalar(0.8).getStyle();
    for (const f of [1, -1]) { for (const py of [H * 0.7, H * 0.28]) lf.add(at(box(W * 0.6, H * 0.32, 0.008, pc), W / 2, py, f * 0.016)); lf.add(at(sphere(0.016, '#E2B53C', 0), W - 0.05, H * 0.47, f * 0.022)); }
    if (orn) for (const f of [1, -1]) lf.add(at(box(W * 0.68, 0.012, 0.004, '#D9AE3A'), W / 2, H * 0.49, f * 0.02));
    g.userData.update = t => { let a = o.swing ? keyAt(o.swing, t, 0) : (o.open ?? 0); const bd = o.beatDur ?? 0.45, A = o.amp ?? 1.1;
      for (const b of o.beats || []) { const u = (t - b) / bd; if (u > 0 && u < 1) a = Math.max(a, A * Math.sin(PI * Math.pow(u, 0.7))); }
      piv.rotation.y = a + rattle(o.rattle, t); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- the complaint form (pivot at its middle, facing +Z; face: 'camera'): a pale
  // blue sheet o.w (0.42) x o.h (0.56) with a navy header bar, ruled lines, two tick boxes, a pictogram (a door with three arcs, crossed by a red
  // exclamation badge) and a signature scrawl; no words.
  grinForm(o) {
    const W = o.w ?? 0.42, H = o.h ?? 0.56, g = grp();
    g.add(at(box(W + 0.02, H + 0.02, 0.006, '#2A3550'), 0, 0, -0.004));
    g.add(canvasPlane(W, H, (c, w, h) => {
      c.fillStyle = '#E4EEF8'; c.fillRect(0, 0, w, h); c.fillStyle = '#2C4A8A'; c.fillRect(0, 0, w, h * 0.1);
      c.fillStyle = '#FFFFFF'; for (let i = 0; i < 3; i++) c.fillRect(w * (0.08 + i * 0.12), h * 0.035, w * 0.08, h * 0.03);
      const px = w * 0.5, py = h * 0.33, dh = h * 0.26; c.fillStyle = '#2F7F8C'; c.fillRect(px - dh * 0.3, py - dh / 2, dh * 0.5, dh); c.strokeStyle = INK; c.lineWidth = w * 0.012; c.strokeRect(px - dh * 0.3, py - dh / 2, dh * 0.5, dh);
      c.strokeStyle = '#FF4316'; c.lineWidth = w * 0.022; c.lineCap = 'round'; for (let i = 0; i < 3; i++) { c.beginPath(); c.arc(px + dh * 0.22, py, dh * (0.22 + i * 0.16), -0.8, 0.8); c.stroke(); }
      c.fillStyle = '#D81E1E'; c.beginPath(); c.arc(w * 0.82, h * 0.2, w * 0.08, 0, TAU); c.fill(); c.fillStyle = '#FFFFFF'; c.fillRect(w * 0.81, h * 0.155, w * 0.02, h * 0.05); c.fillRect(w * 0.81, h * 0.22, w * 0.02, h * 0.015);
      c.strokeStyle = '#8A9AB4'; c.lineWidth = h * 0.006; for (let i = 0; i < 5; i++) { c.beginPath(); c.moveTo(w * 0.1, h * (0.56 + i * 0.07)); c.lineTo(w * 0.9, h * (0.56 + i * 0.07)); c.stroke(); }
      c.strokeStyle = INK; c.lineWidth = h * 0.006; for (let i = 0; i < 2; i++) c.strokeRect(w * 0.1, h * (0.53 + i * 0.07), w * 0.05, w * 0.05);
      c.strokeStyle = '#1E2E66'; c.lineWidth = h * 0.008; c.beginPath(); c.moveTo(w * 0.55, h * 0.93); for (let i = 0; i < 12; i++) c.lineTo(w * (0.56 + i * 0.028), h * (0.93 - 0.03 * Math.sin(i * 1.9))); c.stroke();
    }, { res: 256 }));
    return g;
  },

  // ---------------------------------------------------------------- the failed exam sheet (pivot at its middle, facing +Z; face: 'camera'): a white
  // sheet o.w (0.5) x o.h (0.66) with « BAC » on top, ruled lines and three big slanted red stamps « 0/20 » one over another; two strips of tape
  grinExamSheet(o) {
    const W = o.w ?? 0.5, H = o.h ?? 0.66, g = grp();
    g.add(at(box(W + 0.02, H + 0.02, 0.006, '#7E8894'), 0, 0, -0.004));
    g.add(canvasPlane(W, H, (c, w, h) => {
      c.fillStyle = '#F4F7FA'; c.fillRect(0, 0, w, h); c.fillStyle = '#1E2E44'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, 'BAC', w / 2, h * 0.09, w * 0.5, h * 0.1);
      c.strokeStyle = '#9AA8BC'; c.lineWidth = h * 0.005; for (let i = 0; i < 10; i++) { c.beginPath(); c.moveTo(w * 0.08, h * (0.2 + i * 0.075)); c.lineTo(w * 0.92, h * (0.2 + i * 0.075)); c.stroke(); }
      [[0.5, 0.36, -0.18], [0.46, 0.58, 0.12], [0.54, 0.8, -0.08]].forEach(([x, y, r]) => { c.save(); c.translate(w * x, h * y); c.rotate(r); c.strokeStyle = '#D81E1E'; c.lineWidth = w * 0.03; c.strokeRect(-w * 0.36, -h * 0.085, w * 0.72, h * 0.17);
        c.fillStyle = '#D81E1E'; fitText(c, '0/20', 0, h * 0.008, w * 0.62, h * 0.15); c.restore(); });
    }, { res: 512 }));
    for (const [x, y, r] of [[-W * 0.38, H * 0.46, 0.6], [W * 0.38, H * 0.46, -0.6]]) g.add(at(box(0.16, 0.045, 0.004, '#E8E0B8', { opacity: 0.85 }), x, y, 0.004, 0, 0, r));
    return g;
  },

  // ---------------------------------------------------------------- the dictionary (pivot under it, lying open, the spine along Z, pages up +Y):
  // a thick leather book o.w (0.9, both pages) x o.d (0.62); the right page shows the one word o.word (« IIIIIK ») huge; o.defAt: under it the
  // definition o.def (« de l'huile ») and an oil drop write in.
  // o.flip [t0, t1, n, accel] (round 1 fix): n blank pages turn right to left, each one sooner and faster than the last (start times follow
  // (j / (n - 1)) ^ (1 / accel), durations shrink from 0.3 s to 0.055 s); a fast page drags three fading ghosts behind it (a smear fan); the last one
  // slams down at t1 (a hard stop) and the whole book gives a small settle bounce (squash, rebound) over the next 0.5 s.
  // o.closed: the closed volume (o.w/2 x o.d x o.thick), a real huge book: dark red leather boards proud of a cream page block whose edges show
  // fine page lines and a bevel, a rounded spine with raised gold bands, gold corner pieces, a gilt frame and « DICTIONNAIRE » on the cover.
  grinBook(o) {
    const W = o.w ?? 0.9, D = o.d ?? 0.62, root = grp(), g = grp(), lea = o.leather || '#7A2A22', gold = '#E2B53C', pw = W / 2 - 0.02; root.add(g);
    if (o.closed) {
      const Th = o.thick ?? 0.24, bw = W / 2, bt = 0.035, ov = 0.035, pg = '#F2E8D0', pl = '#CDBE98';
      for (const y of [bt / 2, Th - bt / 2]) g.add(at(box(bw + ov, bt, D + 2 * ov, lea, { outline: 0.006 }), ov / 2, y, 0));
      g.add(at(box(bw - 0.02, Th - 2 * bt, D, pg), 0.0, Th / 2, 0));
      for (let i = 1; i < 9; i++) { const y = bt + (Th - 2 * bt) * i / 9; g.add(at(box(bw - 0.03, 0.003, 0.004, pl), 0.0, y, D / 2 + 0.001), at(box(0.004, 0.003, D - 0.01, pl), bw / 2 - 0.009, y, 0)); }
      for (const y of [bt + 0.004, Th - bt - 0.004]) g.add(at(box(bw - 0.02, 0.008, 0.012, '#E2D4AE'), 0.0, y, D / 2 - 0.002), at(box(0.012, 0.008, D, '#E2D4AE'), bw / 2 - 0.012, y, 0));
      const spine = new THREE.Mesh(new THREE.CylinderGeometry(Th / 2, Th / 2, D + 2 * ov, 14), mat(lea)); spine.rotation.x = PI / 2; spine.position.set(-bw / 2, Th / 2, 0); spine.scale.set(0.55, 1, 1); g.add(spine);
      for (const z of [-0.36, -0.12, 0.12, 0.36]) { const bd = new THREE.Mesh(new THREE.CylinderGeometry(Th / 2 + 0.012, Th / 2 + 0.012, 0.04, 14), mat(gold)); bd.rotation.x = PI / 2; bd.position.set(-bw / 2, Th / 2, z * D); bd.scale.set(0.58, 1, 1); g.add(bd); }
      const cs = 0.17, tri = new THREE.Shape([V2(0, 0), V2(cs, 0), V2(0, cs)]), tg = new THREE.ExtrudeGeometry(tri, { depth: 0.012, bevelEnabled: false });
      const cx0 = ov / 2 - (bw + ov) / 2, cx1 = ov / 2 + (bw + ov) / 2, cz = D / 2 + ov;
      for (const y of [Th + 0.001, -0.001]) for (const [x, z, sx, sz] of [[cx1, cz, -1, -1], [cx1, -cz, -1, 1], [cx0, cz, 1, -1], [cx0, -cz, 1, 1]]) {
        const m = new THREE.Mesh(tg, mat(gold, { emissive: '#4A3608' })); m.rotation.x = -PI / 2; m.scale.set(sx, sz * -1, y > 0 ? 1 : -1); m.position.set(x, y, z); g.add(m);
        g.add(at(box(0.014, bt + 0.004, cs * 0.9, gold), x - sx * 0.006, y > 0 ? Th - bt / 2 : bt / 2, z + sz * cs * 0.45), at(box(cs * 0.9, bt + 0.004, 0.014, gold), x + sx * cs * 0.45, y > 0 ? Th - bt / 2 : bt / 2, z - sz * 0.006));
      }
      const cov = canvasPlane(bw * 0.9, D * 0.9, (c, w, h) => { c.fillStyle = lea; c.fillRect(0, 0, w, h); c.strokeStyle = gold; c.lineWidth = w * 0.025; c.strokeRect(w * 0.08, h * 0.07, w * 0.84, h * 0.86);
        c.lineWidth = w * 0.008; c.strokeRect(w * 0.12, h * 0.1, w * 0.76, h * 0.8);
        c.fillStyle = gold; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, 'DICTIONNAIRE', w / 2, h * 0.32, w * 0.72, h * 0.12); fitText(c, 'DU GRINCEMENT', w / 2, h * 0.46, w * 0.62, h * 0.07, 700); drawDrop(c, w / 2, h * 0.68, h * 0.2, gold, '#5A1A12', 0.05); }, { res: 512, emissive: 0.12 });
      cov.rotation.x = -PI / 2; cov.position.set(ov / 2, Th + 0.004, 0); g.add(cov);
      return root;
    }
    // the open book: covers, page blocks (a thick fan on the left: a thousand pages), the spine
    g.add(at(box(W + 0.06, 0.03, D + 0.05, lea, { outline: 0.006 }), 0, 0.015, 0));
    g.add(at(box(pw, 0.09, D - 0.02, '#EFE4C8', { outline: 0.004 }), -pw / 2 - 0.01, 0.075, 0), at(box(pw, 0.05, D - 0.02, '#EFE4C8', { outline: 0.004 }), pw / 2 + 0.01, 0.055, 0));
    for (let i = 1; i < 8; i++) g.add(at(box(pw, 0.002, 0.003, '#C9BC9C'), -pw / 2 - 0.01, 0.03 + i * 0.011, D / 2 - 0.009));
    const pageDraw = (wordOn, defOn) => (c, w, h) => {
      c.fillStyle = '#FBF5E4'; c.fillRect(0, 0, w, h);
      if (wordOn) { c.fillStyle = INK; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, o.word || 'IIIIIK', w / 2, h * 0.26, w * 0.86, h * 0.26, 900, 'Georgia'); c.fillStyle = '#9A3A22'; c.fillRect(w * 0.15, h * 0.41, w * 0.7, h * 0.012); }
      if (defOn) { c.fillStyle = '#1E2E44'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, o.def || "de l'huile", w / 2, h * 0.54, w * 0.86, h * 0.15, 800, 'Georgia'); if (!o.dropPop) drawDrop(c, w / 2, h * 0.75, h * 0.17, '#E8A818', INK, 0.06); }
    };
    // a page lies face up: its width along X, the top of its text toward -Z (read by a camera above the book, on its +Z side)
    const mkPage = (draw, x, y) => { const p = canvasPlane(pw, D - 0.04, draw, { res: 512 }); p.rotation.x = -PI / 2; p.position.set(x, y, 0); return p; };
    const left = mkPage(pageDraw(false, false), -pw / 2 - 0.01, 0.121), rightBlank = mkPage(pageDraw(false, false), pw / 2 + 0.01, 0.081), rightWord = mkPage(pageDraw(true, false), pw / 2 + 0.01, 0.0815), rightDef = mkPage(pageDraw(true, true), pw / 2 + 0.01, 0.082);
    for (const p of [left, rightBlank, rightWord, rightDef]) g.add(p);
    left.material.side = rightBlank.material.side = THREE.FrontSide;
    // (round 3 fix) o.dropPop: the oil drop is its own sticker over the page: it pops in with an overshoot at o.defAt, then keeps rocking and
    // swelling gently, and the book gives a small settle bounce as it lands (no still frame on the payoff)
    const Dp = D - 0.04, dropSp = o.dropPop ? canvasPlane(Dp * 0.36, Dp * 0.36, (c, w, h) => { c.clearRect(0, 0, w, h); drawDrop(c, w / 2, h * 0.5, h * 0.47, '#E8A818', INK, 0.06); }, { res: 256, transparent: true }) : null;
    if (dropSp) { dropSp.rotation.x = -PI / 2; dropSp.position.set(pw / 2 + 0.01, 0.084, Dp * 0.25); dropSp.renderOrder = 3; dropSp.visible = false; g.add(dropSp); }
    // the turning pages: a pool of sheets on pivots on the spine, each lies along +X and turns over to -X
    const F = o.flip || null, nF = F ? F[2] : 0, acc = F ? (F[3] ?? 2.4) : 1, pool = [];
    const starts = [], durs = [];
    if (F) { const dl = 0.055; for (let j = 0; j < nF; j++) { const q = nF > 1 ? j / (nF - 1) : 1; durs.push(lerp(0.3, dl, Math.pow(q, 0.8))); starts.push(F[0] + (F[1] - dl - F[0]) * Math.pow(q, 1 / acc)); } }
    for (let i = 0; i < (F ? 18 : 0); i++) { const pv = grp(), sh = canvasPlane(pw, D - 0.05, (c, w, h) => { c.fillStyle = i % 2 ? '#F7EFDA' : '#FBF5E4'; c.fillRect(0, 0, w, h); c.strokeStyle = 'rgba(160,140,100,0.5)'; c.lineWidth = w * 0.01; c.strokeRect(1, 1, w - 2, h - 2); }, { res: 128, emissive: 0.3 });
      const mO = sh.material, mT = mO.clone(); mT.transparent = true; mT.depthWrite = false;
      sh.rotation.x = -PI / 2; sh.position.x = pw / 2; pv.add(sh); pv.position.set(0, 0.085, 0); pv.visible = false; g.add(pv); pool.push([pv, sh, mO, mT]); }
    root.userData.update = t => {
      const showWord = !F || t >= F[1];
      if (F) {
        const live = [];
        for (let j = 0; j < nF; j++) { const u = (t - starts[j]) / durs[j]; if (u < 0 || u > 1.6) continue;
          if (u <= 1) live.push([u, 1]);
          if (durs[j] < 0.15) for (const [lag, op] of [[0.16, 0.5], [0.32, 0.3], [0.48, 0.15]]) { const v = u - lag; if (v >= 0 && v <= 1) live.push([v, op]); } }
        pool.forEach(([pv, sh, mO, mT], i) => { const e = live[i]; pv.visible = !!e; if (!e) return; const [u, op] = e, a = op < 1 ? u : smooth(u);
          pv.rotation.z = PI * a; pv.position.y = 0.085 + 0.07 * Math.sin(PI * a) + i * 0.0004; sh.material = op < 1 ? mT : mO; mT.opacity = op; });
        const v = t - F[1], b = v > 0 && v < 0.6 ? Math.exp(-6.5 * v) * Math.cos(v * 26) : 0;
        g.scale.set(1 + 0.03 * b, 1 - 0.16 * b, 1 + 0.03 * b);
      }
      const def = o.defAt != null && t >= o.defAt;
      rightBlank.visible = !showWord; rightWord.visible = showWord && !def; rightDef.visible = showWord && def;
      if (dropSp) { const v = t - o.defAt; dropSp.visible = def;
        if (def) { const k = Math.max(0.01, outBack(v / 0.2, 2.4)) * (1 + 0.06 * Math.sin(v * 8.5)); dropSp.scale.set(k, k, 1); dropSp.rotation.z = 0.16 * Math.sin(v * 7) * Math.exp(-1.5 * v) + 0.05 * Math.sin(v * 4.2);
          const b = v < 0.7 ? Math.exp(-6 * v) * Math.cos(v * 24) : 0; g.scale.set(1 + 0.02 * b, 1 - 0.12 * b, 1 + 0.02 * b); } }
    };
    root.userData.update(0); return root;
  },

  // ---------------------------------------------------------------- a wooden lectern (pivot at the floor, facing +Z): a column, a slanted top
  // o.w (1.1) x o.d (0.75) at o.h (1.15), a lip at the front
  grinLectern(o) {
    const W = o.w ?? 1.1, Dd = o.d ?? 0.75, Hh = o.h ?? 1.15, g = grp(), wc = o.color || '#7A4A2A';
    g.add(at(box(0.7, 0.08, 0.6, '#5A341E', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(0.32, Hh - 0.1, 0.32, wc, { pivot: 'bottom', outline: 0.006 }), 0, 0.08, 0));
    const top = grp(at(box(W, 0.06, Dd, wc, { outline: 0.006 }), 0, 0, 0), at(box(W, 0.06, 0.05, '#5A341E'), 0, 0.05, Dd / 2)); top.position.set(0, Hh, 0); top.rotation.x = o.tilt ?? 0.25; g.add(top);
    g.userData.top = [0, Hh + 0.04, 0]; return g;
  },

  // ---------------------------------------------------------------- the television (pivot at the floor, facing +Z): a cabinet with a deep open
  // screen o.w (1.5) x o.h (0.95) whose bottom is at o.y (1.0) on a low stand; the picture is a little real scene inside it (a tiny actor set behind
  // the bezel): a cream panelled backdrop, a warm light; o.on false: dark. The screen's middle is at userData.screen. o.cabinet false (round 2):
  // no brown cabinet under it, a thin dark post on a round foot.
  grinTV(o) {
    const W = o.w ?? 1.5, H = o.h ?? 0.95, Y = o.y ?? 1.0, Dp = o.depth ?? 0.9, g = grp(), C = o.color || '#2A2D33';
    if (o.cabinet === false) g.add(at(cyl(0.42, 0.46, 0.05, '#2A2D33', 16), 0, 0.025, -0.3), at(box(0.12, Y, 0.12, '#3A3D44', { pivot: 'bottom' }), 0, 0, -0.3));
    else { g.add(at(box(W + 0.6, 0.5, 0.7, '#7A5236', { pivot: 'bottom', outline: 0.008 }), 0, 0, -0.2)); g.add(at(box(0.3, Y - 0.5, 0.2, '#3A3D44', { pivot: 'bottom' }), 0, 0.5, -0.3)); }
    const bz = 0.1;
    for (const [x, y, w, h] of [[-W / 2 - bz / 2, Y + H / 2, bz, H + 2 * bz], [W / 2 + bz / 2, Y + H / 2, bz, H + 2 * bz], [0, Y + H + bz / 2, W + 2 * bz, bz], [0, Y - bz / 2, W + 2 * bz, bz]]) g.add(at(box(w, h, 0.12, C, { outline: 0.008 }), x, y, 0));
    for (const sd of [-1, 1]) g.add(at(box(0.04, H, Dp, C), sd * (W / 2 + 0.02), Y + H / 2, -Dp / 2), at(box(W, 0.04, Dp, C), 0, sd > 0 ? Y + H + 0.02 : Y - 0.02, -Dp / 2));
    const bg = canvasPlane(W, H, (c, w, h) => { c.fillStyle = o.wall || '#E9DCC0'; c.fillRect(0, 0, w, h); c.strokeStyle = '#C9A55A'; c.lineWidth = w * 0.008;
      for (const x of [0.06, 0.38, 0.7]) c.strokeRect(w * x, h * 0.08, w * 0.24, h * 0.6); c.fillStyle = '#B79A70'; c.fillRect(0, h * 0.78, w, h * 0.22); }, { res: 256, emissive: o.on === false ? 0 : 0.35 });
    bg.position.set(0, Y + H / 2, -Dp + 0.03); g.add(bg);
    if (o.on !== false) { const L = new THREE.PointLight('#FFE6C0', o.power ?? 1.4, 2.0, 1.2); L.position.set(0, Y + H * 0.8, -0.15); g.add(L); }
    g.add(at(sphere(0.025, '#E8402A', 0, { emissive: '#E8402A' }), W / 2 - 0.05, Y - 0.05, 0.065));
    g.userData.screen = [0, Y + H / 2, 0]; return g;
  },

  // ---------------------------------------------------------------- a speech bubble with an oil drop in it, no words (pivot at the tail's tip,
  // facing +Z; face: 'camera'): a white rounded bubble o.w (0.6) wide with a thick ink edge and a big amber drop; it pops out at o.popAt (from
  // nothing, an overshoot, a wobble) and the drop bobs. o.tail 'left' | 'right': the side the tail points to.
  grinBubble(o) {
    const W = o.w ?? 0.6, Hh = W * 0.8, g = grp(), inner = grp(); g.add(inner);
    const N = 256, cv = canvas(N, Math.round(N * 1.2)), c = cv.getContext('2d'), w = N, h = cv.height, bh = h * 0.72, sx = o.tail === 'right' ? -1 : 1;
    c.save(); if (sx < 0) { c.translate(w, 0); c.scale(-1, 1); }
    const shape = () => { c.beginPath(); c.ellipse(w * 0.55, bh * 0.52, w * 0.42, bh * 0.44, 0, 0, TAU); c.moveTo(w * 0.3, bh * 0.8); c.lineTo(w * 0.06, h * 0.98); c.lineTo(w * 0.48, bh * 0.92); };
    c.lineJoin = 'round'; shape(); c.lineWidth = w * 0.07; c.strokeStyle = INK; c.stroke(); c.fillStyle = '#FFFFFF'; shape(); c.fill(); c.restore();
    drawDrop(c, sx > 0 ? w * 0.55 : w * 0.45, bh * 0.54, bh * 0.66, '#E8A818', INK, 0.07);
    const m = new THREE.Mesh(new THREE.PlaneGeometry(W, W * 1.2), new THREE.MeshBasicMaterial({ map: tex(cv), transparent: true, depthWrite: false, toneMapped: false, side: THREE.DoubleSide }));
    m.renderOrder = 7; m.position.set(sx * W * 0.44, W * 0.58, 0); inner.add(m); void Hh;
    g.userData.update = t => { const u = o.popAt == null ? 1 : t - o.popAt; inner.visible = u >= 0; if (u < 0) return; const k = Math.max(0.01, outBack(u / 0.18, 2.6)); inner.scale.setScalar(k);
      inner.rotation.z = 0.12 * Math.sin(u * 16) * Math.exp(-2.5 * u); m.position.y = W * 0.58 + 0.015 * Math.sin(u * 5); };
    g.userData.update(-1); return g;
  },

  // ---------------------------------------------------------------- snow blowing in through a doorway (pivot at the doorway's foot): o.n (70)
  // white flakes born outside within o.spread [w, h] around o.from [x, y, z] and carried along o.dir [x, y, z] (m/s) with a wobble, looping over
  // o.life (1.6 s); o.r flake radius (0.025)
  grinSnowStream(o) {
    const n = o.n ?? 70, g = grp(), fr = o.from || [0, 1.3, 2.5], dir = o.dir || [0, -0.25, -2.2], sp = o.spread || [1.6, 1.8], life = o.life ?? 1.6, r = o.r ?? 0.025;
    // (round 3 fix) round flakes (the faceted icosahedra read as hexagonal confetti); o.facet: the old faceted ones
    const geo = o.facet ? new THREE.IcosahedronGeometry(r, 0) : new THREE.SphereGeometry(r, 10, 7), m = new THREE.MeshBasicMaterial({ color: '#FFFFFF', toneMapped: false }), flakes = [];
    for (let i = 0; i < n; i++) { const f = new THREE.Mesh(geo, m); const hs = Math.sin(i * 91.7) * 0.5 + 0.5, hs2 = Math.sin(i * 37.3 + 1) * 0.5 + 0.5, hs3 = Math.sin(i * 53.1 + 2) * 0.5 + 0.5; f.userData.h = [hs, hs2, hs3]; g.add(f); flakes.push(f); }
    g.userData.update = t => { for (const f of flakes) { const [a, b, c2] = f.userData.h, u = ((t / life) + a) % 1;
      f.position.set(fr[0] + (b - 0.5) * sp[0] + dir[0] * u * life + 0.08 * Math.sin(t * 3 + a * 9), fr[1] + (c2 - 0.5) * sp[1] + dir[1] * u * life + 0.05 * Math.sin(t * 4 + b * 7), fr[2] + dir[2] * u * life);
      f.scale.setScalar(0.6 + 0.8 * c2); } };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a flat irregular patch on the ground (pivot at its middle, on the ground): o.r
  // (0.9) across, o.color; painted without a depth test after a ground layer (renderOrder o.ro, -1.1), raised o.y (0.065)
  grinPatch(o) {
    const R = o.r ?? 0.9, pts = []; for (let i = 0; i < 28; i++) { const a = i / 28 * TAU, k = 1 + 0.16 * Math.sin(3 * a + 0.4) + 0.1 * Math.sin(5 * a + 1.7); pts.push(V2(Math.cos(a) * R * k * (o.sx ?? 1.3), Math.sin(a) * R * k)); }
    const m = new THREE.Mesh(new THREE.ShapeGeometry(new THREE.Shape(pts)), new THREE.MeshLambertMaterial({ color: o.color || '#5E6670', depthTest: false, depthWrite: false, side: THREE.DoubleSide }));
    m.rotation.x = -PI / 2; m.position.y = o.y ?? 0.065; m.renderOrder = o.ro ?? -1.1; m.receiveShadow = true;
    if (!o.wet) return grp(m);
    // (round 3 fix) o.wet: a melted wet patch instead of a flat blob: the same outline in six opaque rings shading from the snow's colour (o.ground)
    // to the wet grey in the middle (a soft edge; opaque and drawn first like the plain patch: a transparent layer without depth test covers the
    // actors), a long cool sheen across it, and a ring of slush lumps and melting snow round its edge
    const SX = o.sx ?? 1.3, cG = new THREE.Color(o.ground || '#E4E8EE'), cW = new THREE.Color(o.color || '#5E6670'), rings = [];
    for (let i = 0; i < 6; i++) { const sc = 1.24 - i * 0.06, mi = new THREE.Mesh(new THREE.ShapeGeometry(new THREE.Shape(pts.map(q => V2(q.x * sc, q.y * sc)))), new THREE.MeshLambertMaterial({ color: cG.clone().lerp(cW, (i + 1) / 6), depthTest: false, depthWrite: false, side: THREE.DoubleSide }));
      mi.rotation.x = -PI / 2; mi.position.y = (o.y ?? 0.065) + 0.0005 * i; mi.renderOrder = (o.ro ?? -1.1) - 0.06 + 0.01 * i; mi.receiveShadow = true; rings.push(mi); }
    const sheen = new THREE.Mesh(new THREE.CircleGeometry(R * 0.55, 20), new THREE.MeshLambertMaterial({ color: cW.clone().lerp(new THREE.Color('#DCE8F4'), 0.45), emissive: '#3A4654', depthTest: false, depthWrite: false, side: THREE.DoubleSide }));
    sheen.scale.set(SX * 0.95, 0.2, 1); sheen.rotation.set(-PI / 2, 0, 0.25); sheen.position.set(R * 0.1, (o.y ?? 0.065) + 0.004, -R * 0.05); sheen.renderOrder = (o.ro ?? -1.1) + 0.01;
    const glint = new THREE.Mesh(new THREE.CircleGeometry(R * 0.09, 12), new THREE.MeshBasicMaterial({ color: '#F4F8FC', depthTest: false, depthWrite: false, side: THREE.DoubleSide }));
    glint.scale.set(SX * 1.2, 0.3, 1); glint.rotation.set(-PI / 2, 0, 0.25); glint.position.set(R * 0.35, (o.y ?? 0.065) + 0.005, -R * 0.12); glint.renderOrder = (o.ro ?? -1.1) + 0.02;
    m.visible = false; const g = grp(m, ...rings, sheen, glint);
    for (let i = 0; i < 22; i++) { const a = i / 22 * TAU + 0.13 * Math.sin(i * 7.1), q = pts[Math.round(a / TAU * 28) % 28], k = 1.12 + 0.08 * Math.sin(i * 3.7);
      const lump = sphere(0.03 + 0.02 * (0.5 + 0.5 * Math.sin(i * 5.3)), i % 3 ? '#EEF2F6' : '#D3DAE2', 1); lump.scale.set(1.4, 0.45, 1.1); lump.position.set(q.x * k, (o.y ?? 0.065) - 0.01, -q.y * k); g.add(lump); }
    return g;
  },

  // ---------------------------------------------------------------- a duvet over somebody lying in bed (pivot at its foot end's middle on the
  // mattress, lying along -Z toward the pillow): (round 1 fix: the slab, its fold and its stripes read as stairs) one soft rounded mass o.w (1.05) x
  // o.len (1.5), a capsule half sunk in the mattress, o.color, a pale rolled edge at the top; o.pull [[t, extra]]: the top edge slides further toward
  // the pillow by extra metres; o.bib [[t, h]]: for somebody sitting up, the top of the duvet rises as one rounded hump to h metres over the mattress
  // (he pulls it up to his nose); o.drape (rad, round 2): the hump's top leans back onto his chest and the rolled edge, in the duvet's colour, sits on
  // its front face under the top (a pale roll on top read as a tray lid)
  grinDuvet(o) {
    const W = o.w ?? 1.05, Lb = o.len ?? 1.5, g = grp(), c = o.color || '#E8EEF6', fc = new THREE.Color(c).lerp(new THREE.Color(o.fold || '#F7F9FC'), 0.18).getStyle();
    const cap = new THREE.CapsuleGeometry(0.5, 1, 6, 18); cap.rotateX(PI / 2);
    const slab = new THREE.Mesh(cap, mat(c, { unique: true })); slab.castShadow = slab.receiveShadow = true; g.add(slab);
    const bib = o.bib ? new THREE.Mesh(new THREE.CapsuleGeometry(0.5, 1, 6, 18), mat(c, { unique: true })) : null;
    const roll = new THREE.Mesh(new THREE.CapsuleGeometry(0.5, 1, 4, 14), mat(o.drape ? new THREE.Color(c).lerp(new THREE.Color('#FFFFFF'), 0.08).getStyle() : fc)); roll.rotation.z = PI / 2; g.add(roll);
    if (bib) { bib.castShadow = bib.receiveShadow = true; g.add(bib); }
    g.userData.update = t => { const L = Lb + keyAt(o.pull, t, 0); slab.scale.set(W, 0.36, L / 2); slab.position.set(0, 0.0, -L / 2);
      if (bib) { const h = Math.max(0.2, keyAt(o.bib, t, 0.6)), dr = o.drape ?? 0; bib.scale.set(W * 0.92, h / 2, 0.3); bib.position.set(0, h * 0.25, -L + 0.12); bib.rotation.x = -dr;
        if (dr) { roll.scale.set(0.09, W * 0.45, 0.12); roll.position.set(0, h * 0.62, -L + 0.12 + 0.14 - h * 0.37 * Math.sin(dr)); } else { roll.scale.set(0.16, W * 0.47, 0.26); roll.position.set(0, h * 0.93, -L + 0.12); } }
      else { roll.scale.set(0.12, W * 0.48, 0.14); roll.position.set(0, 0.17, -L + 0.08); } };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- a knitted scarf (attach to the torso joint, offset about [0, 0.5, 0.02]): a
  // fat ring round the collar and a tail that hangs on the chest, striped; o.color, o.stripe
  grinScarf(o) {
    const c1 = o.color || '#D8402A', c2 = o.stripe || '#F2E6C8', g = grp();
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.15, 0.055, 6, 14), mat(c1)); ring.rotation.x = PI / 2; ring.scale.set(1.15, 1, 0.9); g.add(ring);
    for (let i = 0; i < 5; i++) g.add(at(box(0.11, 0.075, 0.05, i % 2 ? c2 : c1, { outline: 0.004 }), 0.06, -0.06 - i * 0.075, 0.16 + 0.004 * i, 0.08, 0, 0.06));
    return g;
  },

  // ---------------------------------------------------------------- a formal office wall (pivot at the floor in the middle, facing +Z): a cream
  // wall o.w (6) x o.h (3.6) with gilt-framed panels, a dark wood dado, two heavy plain green curtains framing a tall window with a garden light, a
  // bookcase; no flag, no emblem, no portrait
  grinOfficeWall(o) {
    const W = o.w ?? 6, Hh = o.h ?? 3.6, g = grp();
    g.add(at(box(W, Hh, 0.1, o.wall || '#EDE3CC'), 0, Hh / 2, -0.05), at(box(W, 0.9, 0.06, '#6A4028', { outline: 0.004 }), 0, 0.45, 0.01), at(box(W, 0.06, 0.08, '#C9A55A'), 0, 0.92, 0.02));
    for (const x of [-2.2, 2.2]) { g.add(at(box(1.1, 1.7, 0.03, '#E5D8BC', { outline: 0.004 }), x, 2.0, 0.01)); for (const [dx, dy, w, h] of [[-0.55, 0, 0.04, 1.7], [0.55, 0, 0.04, 1.7], [0, 0.85, 1.14, 0.04], [0, -0.85, 1.14, 0.04]]) g.add(at(box(w, h, 0.04, '#C9A55A'), x + dx, 2.0 + dy, 0.03)); }
    g.add(at(box(1.3, 2.2, 0.02, '#BFDDEE', { emissive: '#5A7A8E' }), 0, 2.1, 0.0), at(box(0.06, 2.2, 0.05, '#F4F1E8'), 0, 2.1, 0.03), at(box(1.3, 0.06, 0.05, '#F4F1E8'), 0, 2.4, 0.03));
    for (const sd of [-1, 1]) { g.add(at(box(0.55, 2.9, 0.14, o.curtain || '#2E5A48', { outline: 0.006 }), sd * 0.95, 1.95, 0.1)); for (let i = 0; i < 3; i++) g.add(at(box(0.03, 2.8, 0.02, '#244A3A'), sd * (0.78 + i * 0.16), 1.95, 0.18)); }
    g.add(at(box(1.9, 0.12, 0.2, '#C9A55A', { outline: 0.004 }), 0, 3.45, 0.12));
    return g;
  },

  // ---------------------------------------------------------------- a big formal desk (pivot at the floor in the middle, the sitter's side -Z,
  // the visitors' side +Z): dark wood o.w (2.2) x o.d (1.0) x 0.78, a green leather top, gilt edge, a front panel
  grinDesk(o) {
    const W = o.w ?? 2.2, Dd = o.d ?? 1.0, Hh = o.h ?? 0.78, g = grp(), wc = o.color || '#5A341E';
    g.add(at(box(W, 0.06, Dd, wc, { outline: 0.006 }), 0, Hh - 0.03, 0), at(box(W - 0.2, 0.012, Dd - 0.2, '#2E5A3A'), 0, Hh + 0.006, 0), at(box(W + 0.02, 0.02, Dd + 0.02, '#C9A55A'), 0, Hh - 0.07, 0));
    g.add(at(box(W - 0.04, Hh - 0.1, 0.05, wc, { pivot: 'bottom', outline: 0.006 }), 0, 0, Dd / 2 - 0.05));
    for (const sd of [-1, 1]) g.add(at(box(0.5, Hh - 0.1, Dd - 0.1, wc, { pivot: 'bottom', outline: 0.006 }), sd * (W / 2 - 0.27), 0, 0));
    for (const x of [-0.6, 0.6]) g.add(at(box(0.5, 0.4, 0.01, '#6A4028'), x, 0.36, Dd / 2 - 0.02), at(box(0.46, 0.012, 0.012, '#C9A55A'), x, 0.56, Dd / 2 - 0.015));
    g.userData.top = [0, Hh + 0.012, 0]; return g;
  },

  // ---------------------------------------------------------------- a gilt banner board for the exam hall (pivot at its middle, facing +Z): o.text
  // lines on a deep green board with a gold edge, fitted to the board
  grinBoard(o) {
    const W = o.w ?? 2.4, Hh = o.h ?? 0.8, lines = o.lines || ['BAC', 'ÉPREUVE DE GRINCEMENT'], g = grp();
    g.add(at(box(W + 0.08, Hh + 0.08, 0.05, '#C9A55A', { outline: 0.006 }), 0, 0, -0.03));
    g.add(canvasPlane(W, Hh, (c, w, h) => { c.fillStyle = o.bg || '#24483A'; c.fillRect(0, 0, w, h); c.fillStyle = o.fg || '#F4F1E8'; c.textAlign = 'center'; c.textBaseline = 'middle';
      const n = lines.length; lines.forEach((s, i) => fitText(c, s, w / 2, h * (i + 0.55) / n, w * 0.9, h * (i === 0 ? 0.62 : 0.4) / n * 1.4)); }, { res: 512, emissive: 0.1 }));
    return g;
  },

  // ---------------------------------------------------------------- a tall library bookcase (pivot at the floor in the middle, facing +Z): dark
  // wood o.w (3) x o.h (3.4), o.rows (6) shelves of leather spines in deep reds, greens, blues and browns, a few gold bands; instanced, deterministic
  grinBookcase(o) {
    const W = o.w ?? 3, Hh = o.h ?? 3.4, rows = o.rows ?? 6, g = grp(), wc = o.color || '#4A2C1A', D = 0.4;
    g.add(at(box(W + 0.12, Hh, 0.05, '#2E1A10'), 0, Hh / 2, -D / 2), at(box(W + 0.16, 0.16, D + 0.06, wc, { outline: 0.006 }), 0, Hh + 0.08, 0));
    for (const sd of [-1, 1]) g.add(at(box(0.08, Hh, D, wc, { pivot: 'bottom', outline: 0.006 }), sd * (W / 2 + 0.04), 0, 0));
    const cols = ['#7A2A22', '#2E5A3A', '#2C4A7A', '#6A4A2A', '#8A3A2A', '#3A5A5A', '#5A2A4A', '#9A7A3A'], rh = (Hh - 0.2) / rows;
    const geo = new THREE.BoxGeometry(1, 1, 1); let k = 0;
    for (let r = 0; r < rows; r++) { const y = 0.12 + r * rh; g.add(at(box(W, 0.04, D, wc, { outline: 0.004 }), 0, y, 0)); let x = -W / 2 + 0.02;
      while (x < W / 2 - 0.08) { const h1 = Math.sin(k * 12.9898) * 0.5 + 0.5, bw = 0.05 + 0.05 * h1, bh = rh * (0.62 + 0.3 * (Math.sin(k * 4.1) * 0.5 + 0.5)), c = cols[k % cols.length];
        const b = new THREE.Mesh(geo, mat(c)); b.scale.set(bw, bh, D * 0.8); b.position.set(x + bw / 2, y + 0.02 + bh / 2, 0.02); g.add(b);
        if (k % 3 === 0) g.add(at(box(bw + 0.004, 0.015, 0.01, '#D9AE3A'), x + bw / 2, y + 0.02 + bh * 0.8, D * 0.42));
        x += bw + 0.004; k++; } }
    return g;
  },

  // ---------------------------------------------------------------- a bedside lamp (pivot at the floor): a little table, a lamp with a warm cream
  // shade that glows and a warm point light (o.power 2.2, range 3.5); (round 1 fix) o.pool: a visible warm pool, soft additive glows on the wall
  // behind (o.wall [dx, dy, dz, size], facing +X by default) and round the shade
  grinBedLamp(o) {
    const g = grp(), s = o.s ?? 1, b = grp(); g.add(b); b.scale.setScalar(s);
    b.add(at(box(0.45, 0.55, 0.4, '#8A6A44', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(cyl(0.07, 0.09, 0.05, '#3A3D44', 10), 0, 0.575, 0), at(cyl(0.015, 0.015, 0.25, '#3A3D44', 6, { pivot: 'bottom' }), 0, 0.58, 0));
    b.add(at(cyl(0.1, 0.17, 0.2, '#FFE6B0', 12, { emissive: '#F0B058', outline: 0.004 }), 0, 0.88, 0));
    const L = new THREE.PointLight('#FFC880', o.power ?? 2.2, o.range ?? 3.5, 1.3); L.position.set(0, 0.86 * s, 0.1); g.add(L);
    if (o.pool) {
      const P = o.pool === true ? {} : o.pool;
      g.add(glowPlane(P.halo ?? 0.9, P.color || '#FFB860', P.op ?? 0.55, [0, 0.9 * s, 0.02]));
      if (P.wall) { const [dx, dy, dz, sz] = P.wall, w = glowPlane(sz, P.color || '#FFB860', P.wallOp ?? 0.45, [dx, dy, dz]); w.rotation.y = P.wallRy ?? PI / 2; g.add(w); }
      if (P.floor) { const [dx, dz, sz] = P.floor, f = glowPlane(sz, P.color || '#FFB860', P.floorOp ?? 0.35, [dx, 0.04, dz]); f.rotation.x = -PI / 2; g.add(f); }
    }
    return g;
  },

  // ---------------------------------------------------------------- (round 1 fix) a knitted beanie (attach to the head joint, offset [0, 0.5, 0]):
  // a turned-up ribbed cuff that wraps the top of the box head o.w (0.34) x o.d (0.26), a rounded knit crown and a fluffy pompom; o.color, o.cuff,
  // o.pom. Not a fez: the crown is a dome, the cuff wider than the crown's base, the pompom on top.
  grinBeanie(o) {
    const W = o.w ?? 0.34, Dd = o.d ?? 0.26, c = o.color || '#C8322A', cc = o.cuff || new THREE.Color(c).multiplyScalar(0.82).getStyle(), g = grp();
    g.add(at(box(W + 0.04, 0.12, Dd + 0.04, cc, { outline: 0.008 }), 0, -0.07, 0));
    for (let i = 0; i < 7; i++) { const x = -W / 2 + (i + 0.5) * W / 7; g.add(at(box(0.012, 0.11, 0.006, new THREE.Color(cc).multiplyScalar(0.78).getStyle()), x, -0.07, Dd / 2 + 0.022)); }
    const dome = new THREE.Mesh(new THREE.SphereGeometry(1, 16, 10, 0, TAU, 0, PI / 2), mat(c)); dome.scale.set(W / 2 + 0.01, 0.17, Dd / 2 + 0.01); dome.position.y = -0.02; dome.castShadow = true; g.add(dome);
    const dI = new THREE.Mesh(dome.geometry, new THREE.MeshBasicMaterial({ color: INK, side: THREE.BackSide })); dI.scale.setScalar(1.05); dome.add(dI);
    for (const a of [-0.5, 0, 0.5]) g.add(at(box(0.01, 0.12, 0.006, new THREE.Color(c).multiplyScalar(0.8).getStyle()), a * W * 0.5, 0.05, Dd / 2 - 0.005 - 0.03 * Math.abs(a), -0.5, 0, -a * 0.6));
    const pom = sphere(0.065, o.pom || '#F4F1E8', 1); pom.position.y = 0.17; g.add(pom);
    return g;
  },

  // ---------------------------------------------------------------- (round 1 fix) a long white sage's beard (attach to the head joint at the chin,
  // about [0, 0.04, 0.1]): one full tapered mass o.len (1.1) long from the jaw down past the belt, o.w (0.3) wide at the jaw, thick and rounded,
  // a pointed split tip and a few strand lines; it sways a little (o.wave [amp, rate]). Reads as a beard, not a jabot: it is long, narrows steadily
  // to a point and keeps its volume.
  grinBeard(o) {
    // (round 2 fix: the flat tapered plate read as an apron) the outline is scalloped in long wavy locks that narrow to a split tip, the front face is
    // faceted (each lock's ridge stands out and catches the light), with a few wavy grey strand grooves and a small rounded jaw piece instead of a bar
    const L = o.len ?? 1.1, w = o.w ?? 0.3, c = o.color || '#F2F2EE', sc = o.strand || '#B9BEC6', g = grp(), sw = grp(); g.add(sw);
    const N = 10, half = u => w / 2 * Math.pow(1 - u, 0.75) + 0.012, R = [], Lf = [];
    for (let i = 0; i <= N; i++) { const u = i / N, y = -L * u * (i === N ? 0.97 : 1), bump = (i % 2 ? 0.03 : -0.012) * (1 - 0.5 * u);
      R.push(V2(half(u) + bump, y)); Lf.push(V2(-(half(u) + (i % 2 ? -0.012 : 0.028) * (1 - 0.5 * u)), -L * u * (i === N ? 1.0 : 1))); }
    R[N] = V2(0.04, -L * 0.97); Lf[N] = V2(-0.03, -L);
    const sh = new THREE.Shape([...R, V2(0.0, -L * 0.88), ...Lf.reverse()]);
    const geo = new THREE.ExtrudeGeometry(sh, { depth: 0.07, bevelEnabled: true, bevelThickness: 0.03, bevelSize: 0.02, bevelSegments: 1, curveSegments: 2 }); geo.translate(0, 0, -0.035);
    const pos = geo.attributes.position;
    for (let i = 0; i < pos.count; i++) { const x = pos.getX(i), y = pos.getY(i), z = pos.getZ(i); if (z > 0.02) pos.setZ(i, z + 0.035 * Math.cos(x / w * 9.0 + y * 7.0) * (1 + y / L * 0.5)); }
    geo.computeVertexNormals();
    const m = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ color: c, flatShading: true })); m.castShadow = true; sw.add(m);
    const mI = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: INK, side: THREE.BackSide })); mI.scale.set(1.05, 1.01, 1.15); m.add(mI);
    const jaw = new THREE.Mesh(new THREE.SphereGeometry(1, 8, 5), new THREE.MeshLambertMaterial({ color: c, flatShading: true })); jaw.scale.set(w * 0.5, 0.06, 0.07); jaw.position.set(0, 0.0, 0.05); g.add(jaw);
    for (const x0 of [-0.24, 0.02, 0.26]) { let px = x0 * w, py = -L * 0.08;
      for (let j = 0; j < 4; j++) { const ny = py - L * 0.17, nx = x0 * w * (1 - (j + 1) * 0.2) + (j % 2 ? 0.018 : -0.018), dx = nx - px, dy = ny - py, len = Math.hypot(dx, dy);
        const st = at(box(0.01, len, 0.006, sc), (px + nx) / 2, (py + ny) / 2, 0.095, 0, 0, Math.atan2(-dx, dy)); sw.add(st); px = nx; py = ny; } }
    g.userData.update = t => { const [amp, rate] = o.wave || [0.04, 3]; sw.rotation.z = amp * Math.sin(t * rate); sw.rotation.x = -(o.lift ?? 0.16) + 0.5 * amp * Math.sin(t * rate * 0.7 + 1); };
    g.userData.update(0); return g;
  },

  // ---------------------------------------------------------------- (round 1 fix) the invigilator's conductor baton (attach to a hand): a long
  // white stick o.len (0.62) with a dark cork grip, pointing along +Z of the hand from the grip
  grinBaton(o) {
    const L = o.len ?? 0.62, g = grp();
    const st = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.014, L, 6), mat('#F6F4EC', { emissive: '#4A4A46' })); st.rotation.x = PI / 2; st.position.z = L / 2; g.add(st);
    const sI = new THREE.Mesh(st.geometry, new THREE.MeshBasicMaterial({ color: INK, side: THREE.BackSide })); sI.scale.set(1.9, 1.01, 1.9); st.add(sI);
    g.add(at(cyl(0.025, 0.02, 0.09, '#5A3A28', 8), 0, 0, 0.0, PI / 2));
    return g;
  },

  // ---------------------------------------------------------------- (round 1 fix) a small moving van seen from its back (pivot at the floor in its
  // middle, the front toward -Z, the open back toward +Z): a white box o.len (3.0) long with a blue band and « DÉMÉNAGEMENT » on its sides (o.text), a
  // coloured cab in front with a dark windscreen and side window, four dark wheels with pale hubs, tail lamps, and both rear doors swung wide open
  // (o.doors, rad) on a dark load space with a few boxes inside; (round 3 fix) a wheel arch over each wheel (o.arches false: none)
  grinVan(o) {
    const Lv = o.len ?? 3.0, Wv = 1.7, Hb = 1.75, C = o.color || '#E8742E', g = grp(), y0 = 0.35, zb = Lv / 2;
    // (round 3 fix) a hollow load box (floor, roof, two walls, a dark bulkhead, grey lining), so the boxes inside show through the open back
    const Lb = Lv - 1.0, tw = 0.06;
    g.add(at(box(Wv, 0.08, Lb, '#8A8E94', { pivot: 'bottom', outline: 0.008 }), 0, y0, 0.5), at(box(Wv, 0.08, Lb, '#F4F2EC', { pivot: 'bottom', outline: 0.01 }), 0, y0 + Hb - 0.08, 0.5));
    for (const sd of [-1, 1]) g.add(at(box(tw, Hb, Lb, '#F4F2EC', { pivot: 'bottom', outline: 0.01 }), sd * (Wv / 2 - tw / 2), y0, 0.5), at(box(0.01, Hb - 0.16, Lb - 0.08, '#6E727A', { pivot: 'bottom' }), sd * (Wv / 2 - tw - 0.006), y0 + 0.08, 0.5));
    g.add(at(box(Wv - 0.02, Hb - 0.1, 0.06, '#4A4E56', { pivot: 'bottom' }), 0, y0 + 0.05, 0.5 - Lb / 2 + 0.03));
    for (const [x, y, z, s] of [[-0.35, 0.0, zb - 0.4, 0.5], [0.3, 0.0, zb - 0.6, 0.6], [-0.2, 0.5, zb - 0.7, 0.45], [0.28, 0.6, zb - 0.8, 0.4]]) g.add(at(box(s, s * 0.8, s, '#C49A66', { pivot: 'bottom', outline: 0.006 }), x, y0 + 0.06 + y, z));
    for (const sd of [-1, 1]) { g.add(at(box(0.012, 0.16, Lv - 1.1, '#2F62B5'), sd * (Wv / 2 + 0.006), y0 + 0.5, 0.5)); if (o.text === '') continue;
      const t = canvasPlane(Lv - 1.3, 0.34, (c, w, h) => { c.fillStyle = '#F4F2EC'; c.fillRect(0, 0, w, h); c.fillStyle = '#2F62B5'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, o.text ?? 'DÉMÉNAGEMENT', w / 2, h * 0.55, w * 0.94, h * 0.8); }, { res: 512 });
      t.rotation.y = sd * PI / 2; t.position.set(sd * (Wv / 2 + 0.008), y0 + 1.2, 0.5); g.add(t); }
    g.add(at(box(Wv - 0.06, 0.95, 1.0, C, { pivot: 'bottom', outline: 0.012 }), 0, y0, -Lv / 2 + 0.5), at(box(Wv - 0.06, 0.55, 0.75, C, { pivot: 'bottom', outline: 0.01 }), 0, y0 + 0.95, -Lv / 2 + 0.62));
    g.add(at(box(Wv - 0.2, 0.42, 0.03, '#33456E', { emissive: '#1A2238' }), 0, y0 + 1.22, -Lv / 2 + 0.24, -0.35, 0, 0));
    for (const sd of [-1, 1]) g.add(at(box(0.02, 0.36, 0.5, '#33456E', { emissive: '#1A2238' }), sd * (Wv / 2 - 0.02), y0 + 1.2, -Lv / 2 + 0.66));
    g.add(at(box(Wv, 0.14, 0.1, '#3A3D44', { outline: 0.006 }), 0, y0 + 0.08, zb + 0.03), at(box(Wv, 0.14, 0.1, '#3A3D44'), 0, y0 + 0.1, -Lv / 2 - 0.02));
    for (const sd of [-1, 1]) g.add(at(box(0.08, 0.22, 0.04, '#D8262C', { emissive: '#6A0A0A' }), sd * (Wv / 2 - 0.04), y0 + 0.45, zb + 0.01));
    for (const z of [-Lv / 2 + 0.55, Lv / 2 - 0.55]) for (const sd of [-1, 1]) { const wh = cyl(0.34, 0.34, 0.24, '#22252A', 14); wh.rotation.z = PI / 2; wh.position.set(sd * (Wv / 2 - 0.08), 0.34, z); g.add(wh);
      const hub = cyl(0.15, 0.15, 0.02, '#B9BEC4', 8); hub.rotation.z = PI / 2; hub.position.set(sd * (Wv / 2 + 0.05), 0.34, z); g.add(hub);
      // (round 3 fix) a wheel arch on the body's side over each wheel: a dark well and a grey rim
      if (o.arches !== false) { const well = new THREE.Mesh(new THREE.CircleGeometry(0.42, 12, 0, PI), new THREE.MeshLambertMaterial({ color: '#1E2024', side: THREE.DoubleSide }));
        well.rotation.y = PI / 2; well.position.set(sd * (Wv / 2 + 0.012), 0.34, z); g.add(well);
        const rim = new THREE.Mesh(new THREE.TorusGeometry(0.43, 0.035, 4, 12, PI), mat('#4A4E56')); rim.rotation.y = PI / 2; rim.position.set(sd * (Wv / 2 + 0.02), 0.34, z); g.add(rim); } }
    const da = o.doors ?? 1.9;
    for (const sd of [-1, 1]) { const pv = grp(); pv.position.set(sd * Wv / 2, y0 + 0.05, zb); pv.rotation.y = sd * da; g.add(pv);
      pv.add(at(box(Wv / 2 - 0.02, Hb - 0.12, 0.05, '#ECEAE2', { pivot: 'bottom', outline: 0.008 }), -sd * (Wv / 4 - 0.01), 0, 0.03), at(box(0.05, 0.3, 0.02, '#8A8E94'), -sd * (Wv / 2 - 0.14), (Hb - 0.12) * 0.5, 0.06)); }
    return g;
  },

  // ---------------------------------------------------------------- (round 1 fix) a bare bulb hanging from a ceiling rose (pivot at the rose): a
  // round plate, a cord o.drop (0.6) long, a cap and a glowing bulb with a soft halo, a faint cone of light under it and a warm point light (o.power,
  // o.range); it swings by o.swing (rad) at o.rate (rad/s) the whole shot; o.pool [y, size]: a soft warm pool on the surface at height y (relative to
  // the pivot, e.g. the shelf) that slides under the swinging bulb
  grinBulb(o) {
    const d = o.drop ?? 0.6, g = grp(), arm = grp(); g.add(arm);
    g.add(at(cyl(0.07, 0.07, 0.025, '#E6E2D8', 12, { outline: 0.004 }), 0, -0.012, 0));
    arm.add(at(cyl(0.006, 0.006, d, '#222222', 4, { pivot: 'top' }), 0, 0, 0), at(cyl(0.022, 0.022, 0.06, '#3A3A3A', 8), 0, -d, 0), at(sphere(0.055, '#FFF1C8', 1, { emissive: '#FFD27A', noGrain: true }), 0, -d - 0.07, 0));
    const halo = glowPlane(o.halo ?? 0.55, '#FFD890', 0.7, [0, -d - 0.07, 0.02]); halo.userData.bill = true; arm.add(halo);
    const cone = new THREE.Mesh(new THREE.ConeGeometry(o.coneR ?? 0.5, o.coneH ?? 1.0, 16, 1, true), new THREE.MeshBasicMaterial({ color: '#FFE2A0', transparent: true, opacity: o.coneOp ?? 0.07, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, toneMapped: false }));
    cone.position.y = -d - 0.07 - (o.coneH ?? 1.0) / 2; arm.add(cone);
    const l = new THREE.PointLight(o.color || '#FFCF8A', o.power ?? 5, o.range ?? 6, 1.3); l.position.set(0, -d - 0.12, 0.05); arm.add(l);
    const pool = o.pool ? glowPlane(o.pool[1], '#FFC870', o.poolOp ?? 0.4, [0, o.pool[0], 0]) : null; if (pool) { pool.rotation.x = -PI / 2; g.add(pool); }
    g.userData.update = t => { const a = (o.swing ?? 0) * Math.sin(t * (o.rate ?? 2.4) + (o.ph ?? 0)); arm.rotation.z = a;
      if (pool) pool.position.x = -o.pool[0] * Math.tan(a); };
    g.userData.update(0); return g;
  },
  // ---------------------------------------------------------------- (round 3 fix) a long hairdo that overhangs a box head (attach to the head
  // joint, offset [0, 0, 0]): seen from behind or three-quarter rear it reads as hair, not a box. A rounded crown over the back two thirds of the
  // head, wider than the head, and a back curtain whose outline bulges past the cheeks, falls onto the shoulders with a scalloped hem and flicks
  // out at both ends; an ink edge on each. o.w / o.h / o.d: the head's width (0.222), height (0.5) and depth (0.17); o.color; o.sway (rad);
  // o.bob: the curtain's lower edge as a fraction of the head's height (-0.02: onto the shoulders; about 0.4: a bob over a bare nape)
  grinHairDo(o) {
    const W = o.w ?? 0.222, H = o.h ?? 0.5, D = o.d ?? 0.17, c = o.color || '#C8503A', g = grp(), sw = grp(); g.add(sw);
    const hm = new THREE.MeshLambertMaterial({ color: c, flatShading: true }), ink = new THREE.MeshBasicMaterial({ color: INK, side: THREE.BackSide });
    const crown = new THREE.Mesh(new THREE.CylinderGeometry(W * 0.6, W * 0.6, D * 0.78, 10, 1, false, -PI * 0.5, PI), hm);
    crown.rotation.x = -PI / 2; crown.position.set(0, H, -D * 0.12); crown.scale.set(1, 1, 0.75); crown.castShadow = true; g.add(crown);
    const cI = new THREE.Mesh(crown.geometry, ink); cI.scale.set(1.06, 1.03, 1.06); crown.add(cI);
    const yb = H * (o.bob ?? -0.02), ym = (H * 0.92 + yb) / 2, yq = yb + (H * 0.92 - yb) * 0.2;
    const P_ = [V2(-W * 0.6, H * 0.92), V2(-W * 0.66, ym), V2(-W * 0.63, yq), V2(-W * 0.6, yb), V2(-W * 0.84, yb - H * 0.07), V2(-W * 0.62, yb - H * 0.11)];
    for (let i = 0; i <= 6; i++) { const x = -W * 0.5 + W * i / 6; P_.push(V2(x, yb - H * (i % 2 ? 0.15 : 0.1))); }
    P_.push(V2(W * 0.62, yb - H * 0.11), V2(W * 0.84, yb - H * 0.07), V2(W * 0.6, yb), V2(W * 0.63, yq), V2(W * 0.66, ym), V2(W * 0.6, H * 0.92));
    const sh = new THREE.Shape(P_); sh.absarc(0, H * 0.92, W * 0.6, 0, PI, false);
    const geo = new THREE.ExtrudeGeometry(sh, { depth: 0.035, bevelEnabled: true, bevelThickness: 0.012, bevelSize: 0.01, bevelSegments: 1, curveSegments: 6 });
    const back = new THREE.Mesh(geo, hm); back.position.set(0, 0, -D / 2 - 0.045); back.castShadow = true; sw.add(back);
    const bI = new THREE.Mesh(geo, ink); bI.scale.set(1.04, 1.03, 1.2); back.add(bI);
    for (const sd of [-1, 1]) { const lh = H * 0.96 - yb, lk = at(box(0.03, lh, D * 0.55, c, { outline: 0.006 }), sd * (W / 2 + 0.018), yb + lh / 2, -D * 0.22); g.add(lk); }
    g.userData.update = t => { sw.rotation.x = -0.06 + (o.sway ?? 0.03) * Math.sin(t * 2.1); };
    g.userData.update(0); return g;
  },
};
