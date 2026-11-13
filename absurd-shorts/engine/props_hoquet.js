// « Le hoquet » (story 47): a man has had the hiccups for three days; at each hiccup he jumps a metre; the seismographs record an earthquake (magnitude
// four, epicentre: his sofa); the prefecture evacuates the building, but not him (one does not evacuate an epicentre); the firemen try the glass of
// water upside down, then the big fright: he stays stuck to the ceiling; the State declares him a natural disaster, his insurance pays him; since then
// he drinks nothing but soda. Conventions as in props.js (metres, front +Z, pivot at the floor); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, ease, clamp01 } from './style.js';
import { grp, at, label, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const rnd = s => { let x = Math.sin(s * 127.1) * 43758.5453; return x - Math.floor(x); };
const wob = (u, f, d) => u < 0 ? 0 : Math.exp(-u * d) * Math.sin(u * f);
const list = v => [].concat(v ?? []);
// a canvas that is redrawn every frame (a scrolling paper trace, a pulsing map): the plane, and a redraw(fn) that repaints it
function liveCanvas(w, h, res, opts = {}) {
  const c = document.createElement('canvas'); c.width = res; c.height = Math.max(8, Math.round(res * h / w));
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const m = opts.basic ? new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide, toneMapped: false, transparent: !!opts.transparent, alphaTest: opts.transparent ? 0.05 : 0 })
    : new THREE.MeshLambertMaterial({ map: tex, side: THREE.DoubleSide });
  const pl = new THREE.Mesh(new THREE.PlaneGeometry(w, h), m); pl.userData.noAO = true;
  let last = null;
  const redraw = (key, fn) => { if (key === last) return; last = key; fn(c.getContext('2d'), c.width, c.height); tex.needsUpdate = true; };
  return { pl, redraw };
}

export const HOQUET_PROPS = {
  // A comic sound burst « HIC ! »: a yellow star with a black outline and the word, popping at each time of o.at [t, ...] (0.1 s out-back, held o.hold
  // 0.32 s with a wiggle, gone in 0.08 s); o.w (0.55 m), o.text ('HIC !'), o.tilt (rad, a different slant at each pop when it is a list). Faces +Z (give
  // it face: 'camera'). Each pop also jumps a little (o.rise, 0.12 m), the sound going up with him.
  hicBurst(o) {
    const w = o.w ?? 0.55, txt = o.text || 'HIC !';
    const pl = canvasPlane(w, w * 0.62, (c, W, H) => { c.clearRect(0, 0, W, H); const cx = W / 2, cy = H / 2, n = 14;
      c.beginPath(); for (let i = 0; i <= 2 * n; i++) { const a = i * PI / n, r = (i % 2 ? 0.62 : 0.98) * (0.5 + 0.08 * rnd(i)); c.lineTo(cx + Math.cos(a) * r * W * 0.98, cy + Math.sin(a) * r * H * 0.98); }
      c.closePath(); c.fillStyle = '#FFE14A'; c.fill(); c.lineWidth = H * 0.05; c.strokeStyle = '#1C1C1E'; c.stroke();
      c.fillStyle = '#1C1C1E'; c.textAlign = 'center'; c.textBaseline = 'middle'; let px = H * 0.42; c.font = `900 ${px}px Arial`; const tw = c.measureText(txt).width; if (tw > W * 0.62) { px *= W * 0.62 / tw; c.font = `900 ${px}px Arial`; }
      c.fillText(txt, cx, cy + H * 0.02); }, { res: 384, transparent: true });
    pl.material = new THREE.MeshBasicMaterial({ map: pl.material.map, transparent: true, alphaTest: 0.05, side: THREE.DoubleSide, toneMapped: false }); pl.userData.noAO = true;
    const inner = grp(pl), g = grp(inner), ats = list(o.at), hold = o.hold ?? 0.32, tilts = list(o.tilt ?? [0.18, -0.22, 0.1, -0.15]);
    g.userData.update = t => { let k = 0, ti = 0, u0 = 0;
      ats.forEach((a, i) => { const u = t - a; if (u >= 0 && u < 0.1 + hold + 0.08) { ti = i; u0 = u; k = u < 0.1 ? ease.outBack(u / 0.1) : u < 0.1 + hold ? 1 + 0.06 * Math.sin((u - 0.1) * 40) * Math.exp(-(u - 0.1) * 6) : 1 - (u - 0.1 - hold) / 0.08; } });
      inner.visible = k > 0.01; inner.scale.setScalar(Math.max(0.01, k)); inner.rotation.z = tilts[ti % tilts.length]; inner.position.y = (o.rise ?? 0.12) * clamp01(u0 / 0.25); };
    g.userData.update(0); return g;
  },

  // A drum seismograph on a lab bench, front +Z, 0.9 m wide: a grey base, a white paper drum turning (axis along X), a paper band falling from it to the
  // front with the trace printed on it, scrolling toward the viewer, and the pen arm whose tip writes on the drum. o.spikes [[t, amp], ...] (amp 0..1.5):
  // at each, the pen swings across (a decaying zigzag) and the trace keeps it; over 1 the pen jumps off the paper and the arm rattles. o.speed (paper,
  // 0.12 m/s).
  seismograph(o) {
    const g = grp(at(box(0.9, 0.16, 0.5, '#8A9198', { outline: 0.006 }), 0, 0.08, 0), at(box(0.86, 0.04, 0.46, '#6E757C'), 0, 0.18, 0));
    for (const x of [-0.38, 0.38]) g.add(at(box(0.04, 0.22, 0.06, '#5A6168'), x, 0.3, -0.05));
    const drum = grp(at(cyl(0.11, 0.11, 0.7, '#F4F1E6', 20, { noGrain: true }), 0, 0, 0, 0, 0, PI / 2)); drum.position.set(0, 0.36, -0.05); g.add(drum);
    for (let i = 0; i < 6; i++) drum.add(at(box(0.7, 0.004, 0.012, '#C9C3B0'), 0, 0.111 * Math.cos(i * PI / 3), 0.111 * Math.sin(i * PI / 3), i * PI / 3, 0, 0));   // ruled lines (they show it turning)
    const BW = 0.62, BL = 0.5, sp = o.speed ?? 0.12, spikes = (o.spikes || []).map(([a, b]) => [a, b]);
    const band = liveCanvas(BW, BL, 512); band.pl.rotation.x = -PI / 2 + 0.35; band.pl.position.set(0, 0.215, 0.2); g.add(band.pl);   // tilted toward a camera in front
    const amp = (tt) => { let v = 0.04 * Math.sin(tt * 31) * Math.sin(tt * 7.3); for (const [a, s] of spikes) { const u = tt - a; if (u >= 0 && u < 1.2) v += s * wob(u, 38, 4.2) * 1.15; } return v; };
    const arm = grp(at(box(0.012, 0.012, 0.34, '#2A2C31'), 0, 0, -0.17), at(cyl(0.012, 0.004, 0.05, '#C8202A', 8), 0, -0.02, -0.34, PI / 2, 0, 0)); arm.position.set(0, 0.5, 0.2); g.add(arm);
    g.add(at(box(0.05, 0.3, 0.05, '#5A6168'), o.postX ?? 0, 0.35, 0.22));   // o.postX: the pen post aside (in the middle it hid the nib)
    g.userData.update = t => {
      drum.rotation.x = -t * sp / 0.11;
      const a = amp(t), off = Math.max(0, Math.abs(a) - 1.0); arm.rotation.set(-0.42 - 0.25 * off + 0.04 * off * Math.sin(t * 60), 0.42 * Math.max(-1.3, Math.min(1.3, a)), 0);
      if (o.penOff != null) { const u = t - o.penOff; arm.visible = u < 0.75; if (u >= 0) { arm.position.set(0.7 * u, 0.5 + 1.6 * u - 4.9 * u * u, 0.2 + 0.4 * u); arm.rotation.z += 9 * u; arm.rotation.x -= 5 * u; } else arm.position.set(0, 0.5, 0.2); }   // (pass 2 of 50) o.penOff: the pen flies off in an arc
      band.redraw(Math.round(t * 30), (c, W, H) => { c.fillStyle = '#FBF8EE'; c.fillRect(0, 0, W, H); c.strokeStyle = 'rgba(60,80,120,0.25)'; c.lineWidth = 2;
        for (let i = 1; i < 6; i++) { c.beginPath(); c.moveTo(W * i / 6, 0); c.lineTo(W * i / 6, H); c.stroke(); }
        c.strokeStyle = o.ink ? '#0B1236' : '#1B2A6B'; c.lineWidth = W * (o.ink ?? 0.008); c.lineJoin = 'round'; c.beginPath();   // (pass 2 of 50) o.ink: a thick dark line that reads at phone size
        for (let j = 0; j <= 120; j++) { const y = H * j / 120, tt = t - (y / H) * BL / sp, v = Math.max(-(o.clampV ?? 1.35), Math.min(o.clampV ?? 1.35, amp(tt))); const x = W * (0.5 + 0.34 * v); if (j === 0) c.moveTo(x, y); else c.lineTo(x, y); }
        c.stroke(); c.fillStyle = '#1B2A6B'; c.font = `bold ${H * 0.05}px Arial`; c.textAlign = 'left'; c.fillText(o.label || 'SISMO 3', W * 0.03, H * 0.95); });
    };
    g.userData.update(0); return g;
  },

  // A wall screen with a city map, front +Z (o.w 1.6 m, o.h 1.0 m): a dark frame, pale streets on a grey-green ground, a heading (o.head 'MAGNITUDE 4') in a
  // red band, a red dot with its label (o.label 'CANAPÉ') and red rings that pulse out from it at each time of o.pulses [t, ...]; o.zoom [[t, k]]: the map
  // zooms in on the dot (k 1 .. 3) from that time (0.4 s ease-out).
  quakeMap(o) {
    const w = o.w ?? 1.6, h = o.h ?? 1.0, g = grp(at(box(w + 0.08, h + 0.08, 0.05, '#1E2228', { outline: 0.008 }), 0, 0, -0.03));
    const scr = liveCanvas(w, h, o.res ?? 512, { basic: true }); g.add(scr.pl); scr.pl.position.z = 0.002;   // (pass 2 of 50) o.res: a sharper map for a close-up
    const pulses = list(o.pulses), zk = o.zoom || [];
    g.userData.update = t => { let zoom = 1; for (const [a, k] of zk) if (t >= a) zoom = 1 + (k - 1) * ease.inOut(clamp01((t - a) / (o.zoomDur ?? 0.4)));
      scr.redraw(Math.round(t * 30), (c, W, H) => { const cx = W * (o.dotX ?? 0.55), cy = H * (o.dotY ?? 0.58); c.fillStyle = '#C9D3C2'; c.fillRect(0, 0, W, H); c.save(); c.translate(cx, cy); c.scale(zoom, zoom); c.translate(-cx, -cy);
        c.strokeStyle = '#F4F2EA'; for (let i = -6; i < 16; i++) { c.lineWidth = (i % 3 ? 0.01 : 0.022) * W; c.beginPath(); c.moveTo(i * W * 0.11, 0); c.lineTo(i * W * 0.11 + H * 0.25, H); c.stroke(); c.beginPath(); c.moveTo(0, i * H * 0.13); c.lineTo(W, i * H * 0.13 - W * 0.08); c.stroke(); }
        c.fillStyle = '#8FB4D8'; c.beginPath(); c.moveTo(0, H * 0.18); c.bezierCurveTo(W * 0.3, H * 0.28, W * 0.5, H * 0.08, W, H * 0.22); c.lineTo(W, H * 0.3); c.bezierCurveTo(W * 0.5, H * 0.16, W * 0.3, H * 0.36, 0, H * 0.26); c.fill();   // the river
        for (const a of pulses) { const u = (t - a) / 0.9; if (u < 0 || u >= 1) continue; c.strokeStyle = `rgba(200,32,42,${1 - u})`; c.lineWidth = W * 0.012; for (const q of [0, 0.33]) { const r = (u + q) % 1; c.beginPath(); c.arc(cx, cy, W * 0.05 + r * W * 0.45, 0, TAU); c.stroke(); } }
        const dot = () => { c.fillStyle = '#C8202A'; c.beginPath(); c.arc(cx, cy, W * 0.022, 0, TAU); c.fill(); c.strokeStyle = '#FFFFFF'; c.lineWidth = W * 0.006; c.stroke(); };
        if (!o.labelBelow) dot(); c.restore();
        if (o.label !== '') { const L = o.label || 'CANAPÉ';
          if (o.labelBelow) {   // (pass 2 of 50) under the dot, centred, its box behind the dot (beside it the box bit a notch out of the dot and ran off the frame)
            c.font = `900 ${H * 0.07 * Math.min(2.2, 0.6 + 0.4 * zoom)}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; const lw = c.measureText(L).width, fh = H * 0.07 * Math.min(2.2, 0.6 + 0.4 * zoom), ly = cy + W * 0.022 * zoom + fh * 0.95;
            c.fillStyle = '#FFFFFF'; c.fillRect(cx - lw / 2 - W * 0.02, ly - fh * 0.68, lw + W * 0.04, fh * 1.36); c.fillStyle = '#1B1B1E'; c.fillText(L, cx, ly);
            c.save(); c.translate(cx, cy); c.scale(zoom, zoom); c.translate(-cx, -cy); dot(); c.restore();
          } else { c.fillStyle = '#1B1B1E'; c.font = `bold ${H * 0.085 * Math.min(1.6, 0.8 + 0.25 * zoom)}px Arial`; c.textAlign = 'left'; c.textBaseline = 'middle';
            const lw = c.measureText(L).width; c.fillStyle = '#FFFFFF'; c.fillRect(cx + W * 0.04, cy - H * 0.12, lw + W * 0.03, H * 0.11); c.fillStyle = '#1B1B1E'; c.fillText(L, cx + W * 0.055, cy - H * 0.065); } }
        else { c.save(); c.translate(cx, cy); c.scale(zoom, zoom); c.translate(-cx, -cy); if (o.labelBelow) dot(); c.restore(); }
        c.fillStyle = '#B0101A'; c.fillRect(0, 0, W, H * 0.16); c.fillStyle = '#FFFFFF'; c.font = `900 ${H * 0.11}px Arial`; c.textAlign = 'center'; c.fillText(o.head || 'MAGNITUDE 4', W / 2, H * 0.085); }); };
    g.userData.update(0); return g;
  },

  // Red rings on the floor round a point (pivot at the floor, a flat decal 2 mm up): o.r (2.4 m, the outer one), o.n (4 rings), pulsing out at each time
  // of o.pulses [t, ...] (each ring swells 15 % and flashes), o.base (0.5: their opacity at rest). Seen from above: the epicentre round the sofa.
  quakeRings(o) {
    const R = o.r ?? 2.4, n = o.n ?? 4, g = grp(), rings = [];
    for (let i = 0; i < n; i++) { const r = R * (i + 1) / n, m = new THREE.Mesh(new THREE.RingGeometry(r - 0.05, r + 0.05, 48).rotateX(-PI / 2), new THREE.MeshBasicMaterial({ color: '#D3202A', transparent: true, opacity: 0.5, depthWrite: false })); m.position.y = 0.004 + 0.001 * i; m.userData.noAO = true; g.add(m); rings.push(m); }
    const pulses = list(o.pulses);
    g.userData.update = t => { rings.forEach((m, i) => { let k = 0; for (const a of pulses) { const u = t - a - 0.05 * i; if (u >= 0 && u < 0.5) k = Math.max(k, Math.sin(PI * u / 0.5)); } m.scale.setScalar(1 + 0.15 * k); m.material.opacity = (o.base ?? 0.5) + (1 - (o.base ?? 0.5)) * k; }); };
    g.userData.update(0); return g;
  },

  // A police cordon round a rectangle (o.w x o.d, centred on the pivot): four striped posts and red-and-white tape at 0.9 m, with signs hanging from it
  // (o.sign 'ÉPICENTRE') on the sides that face +Z and -X. o.jumps [[t, amp]]: the tape jumps and wobbles (a hiccup inside).
  cordon(o) {   // o.signW / o.signH: the ÉPICENTRE plates (0.62 x 0.2 m; from 4.6 m up they were unreadable)
    const w = o.w ?? 2.6, d = o.d ?? 1.8, g = grp(), H = o.h ?? 0.9, C = [[-w / 2, -d / 2], [w / 2, -d / 2], [w / 2, d / 2], [-w / 2, d / 2]];
    for (const [x, z] of C) { g.add(at(cyl(0.035, 0.035, H + 0.1, '#E8E4DA', 8, { pivot: 'bottom' }), x, 0, z), at(box(0.25, 0.04, 0.25, '#3A3D44'), x, 0.02, z)); for (let i = 0; i < 3; i++) g.add(at(cyl(0.037, 0.037, 0.08, '#C8202A', 8), x, 0.2 + i * 0.3, z)); }
    const tapeTex = (() => { const c = document.createElement('canvas'); c.width = 256; c.height = 16; const x = c.getContext('2d'); for (let i = 0; i < 16; i++) { x.fillStyle = i % 2 ? '#F4F2EA' : '#D3202A'; x.beginPath(); x.moveTo(i * 16, 0); x.lineTo(i * 16 + 16, 0); x.lineTo(i * 16 + 8, 16); x.lineTo(i * 16 - 8, 16); x.fill(); } const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = THREE.RepeatWrapping; return t; })();
    const sides = [], signs = [];
    for (let i = 0; i < 4; i++) { const [x0, z0] = C[i], [x1, z1] = C[(i + 1) % 4], L = Math.hypot(x1 - x0, z1 - z0), tx = tapeTex.clone(); tx.needsUpdate = true; tx.repeat.set(L / 0.5, 1);
      const m = new THREE.Mesh(new THREE.PlaneGeometry(L, 0.07, 16, 1), new THREE.MeshLambertMaterial({ map: tx, side: THREE.DoubleSide })); const s = grp(m); s.position.set((x0 + x1) / 2, H, (z0 + z1) / 2); s.rotation.y = -Math.atan2(z1 - z0, x1 - x0); g.add(s); sides.push({ s, m, L, base: m.geometry.attributes.position.array.slice() });
      if (i === 2 || i === 3) { const mk = () => label(o.sign || 'ÉPICENTRE', o.signW ?? 0.62, o.signH ?? 0.2, { bg: '#FFE14A', fg: '#1B1B1E', wrap: false }), sy = -((o.signH ?? 0.2) / 2 + 0.03);
        // (50) printed on both faces: seen from outside, the front plate read backwards
        const sg = grp(at(mk(), 0, sy, 0.01), at(mk(), 0, sy, -0.01, 0, PI, 0)); s.add(sg); signs.push(sg); } }
    const jumps = o.jumps || [];
    const ends = o.snap != null ? [-1, 1].map(sx => { const e = new THREE.Mesh(new THREE.PlaneGeometry(0.06, 0.42), new THREE.MeshLambertMaterial({ color: '#D3202A', side: THREE.DoubleSide })); e.position.set(sx * (w / 2 - 0.03), H - 0.21, d / 2); e.visible = false; g.add(e); return e; }) : [];   // (pass 2 of 50) o.snap: the tape snaps
    g.userData.update = t => { let k = 0; for (const [a, amp] of jumps) { const u = t - a; if (u >= 0 && u < 1) k += amp * wob(u, 26, 5); }
      if (o.snap != null) { const sn = t >= o.snap, u = t - o.snap; sides[2].m.visible = !sn; ends.forEach((e, i) => { e.visible = sn; if (sn) e.rotation.z = (i ? 1 : -1) * 0.5 * wob(u + 0.05, 14, 3); }); }
      for (const S of sides) { const pa = S.m.geometry.attributes.position; for (let j = 0; j < pa.count; j++) { const x = S.base[3 * j], y = S.base[3 * j + 1], f = Math.cos(PI * x / S.L); pa.setY(j, y + k * 0.12 * f - 0.03 * f * f); } pa.needsUpdate = true; }
      signs.forEach((sg, i) => { sg.rotation.x = 0.35 * k * (i ? -1 : 1); sg.position.y = 0.1 * k; });
      // the front plate drops with the snapped tape and lands on the floor, leaning (its group stays: only the tape mesh is hidden)
      if (o.snap != null && t >= o.snap && signs[0]) { const u = t - o.snap; signs[0].position.y = Math.max(-H + 0.25, -4.9 * u * u); signs[0].rotation.set(0, 0, Math.min(0.45, 1.6 * u)); } };
    g.userData.update(0); return g;
  },

  // A soda can with a bendy straw (front +Z, pivot at its foot, held by its middle: userData.grip): o.color ('#C8202A'), o.text ('SODA'), o.straw (true).
  sodaCan(o) {
    const g = grp(at(cyl(0.045, 0.045, 0.16, o.color || '#C8202A', 12, { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(cyl(0.04, 0.045, 0.012, P.grey, 12), 0, 0.166, 0),
      at(label(o.text || 'SODA', 0.085, 0.04, { bg: null, fg: '#FFFFFF' }), 0, 0.085, 0.046));
    if (o.straw !== false) g.add(at(cyl(0.006, 0.006, 0.14, '#F4F2EA', 6), 0.012, 0.22, 0), at(cyl(0.006, 0.006, 0.08, '#F4F2EA', 6), 0.04, 0.3, 0, 0, 0, -0.9), at(cyl(0.0062, 0.0062, 0.05, '#E85A6A', 6), 0.012, 0.2, 0));
    g.userData.grip = [0, 0.08, 0]; return g;
  },

  // Rows of soda cans (a fridge shelf, a pyramid): o.rows (3), o.cols (6), o.pyramid (true: each row one can shorter and half a can in), colours mixed.
  sodaStack(o) {
    const g = grp(), rows = o.rows ?? 3, cols = o.cols ?? 6, C = o.colors || ['#C8202A', '#E8A33A', '#3A6EA5', '#2F9A5B'];
    for (let r = 0; r < rows; r++) { const nc = o.pyramid === false ? cols : cols - r; for (let i = 0; i < nc; i++) { const x = (i - (nc - 1) / 2) * 0.095, y = r * 0.17; g.add(at(cyl(0.045, 0.045, 0.16, C[(i + r) % C.length], 10, { pivot: 'bottom', outline: 0.006 }), x, y, 0), at(cyl(0.04, 0.045, 0.012, P.grey, 10), x, y + 0.166, 0)); } }
    return g;
  },
  // (pass 2 of 50) Blue water drops bursting from a point (pivot): o.at (t), o.n (16), o.dir [x, y, z] (the main direction), o.speed (2.4 m/s), o.spread
  // (0.6), o.color ('#4FA9E6'), o.r (0.022 m), o.life (0.75 s): each drop flies on its arc under gravity, shrinks and is gone (the water from his cheeks)
  waterDrops(o) {
    const n = o.n ?? 16, g = grp(), dir = new THREE.Vector3(...(o.dir || [0, 0.6, 1])).normalize(), sp = o.speed ?? 2.4, spr = o.spread ?? 0.6, life = o.life ?? 0.75;
    const m = new THREE.MeshLambertMaterial({ color: o.color || '#4FA9E6', emissive: '#16507A', emissiveIntensity: 0.25 }), geo = new THREE.IcosahedronGeometry(o.r ?? 0.022, 0);
    const drops = Array.from({ length: n }, (_, i) => { const d = new THREE.Mesh(geo, m); d.castShadow = false; g.add(d);
      const v = dir.clone().add(new THREE.Vector3(Math.sin(i * 2.399) * spr, Math.cos(i * 1.7) * spr * 0.6, Math.sin(i * 3.1 + 1) * spr * 0.5)).normalize().multiplyScalar(sp * (0.7 + 0.5 * rnd(i + 3))); return { d, v, k: 0.6 + 0.8 * rnd(i) }; });
    g.userData.update = t => { const u = t - (o.at ?? 0); for (const q of drops) { const on = u >= 0 && u < life; q.d.visible = on; if (!on) continue;
      q.d.position.set(q.v.x * u, q.v.y * u - 4.9 * u * u, q.v.z * u); q.d.scale.setScalar(q.k * (1 - 0.6 * u / life)); } };
    g.userData.update(0); return g;
  },

  // (pass 2 of 50) Cracks radiating from a point on a ceiling or a wall (a flat decal facing +Z, pivot at the centre): o.r (0.9 m), o.n (9 cracks), o.at:
  // they run out from the centre in 0.08 s
  ceilingCracks(o) {
    const R = o.r ?? 0.9, n = o.n ?? 9;
    const pl = canvasPlane(2 * R, 2 * R, (c, W, H) => { c.clearRect(0, 0, W, H); c.strokeStyle = '#3A2E26'; c.lineCap = 'round';
      for (let i = 0; i < n; i++) { let a = i * TAU / n + 0.3 * rnd(i), x = W / 2, y = H / 2, L = W * (0.32 + 0.16 * rnd(i + 9)); c.lineWidth = W * 0.012; c.beginPath(); c.moveTo(x, y);
        for (let j = 0; j < 4; j++) { a += (rnd(i * 7 + j) - 0.5) * 0.7; x += Math.cos(a) * L / 4; y += Math.sin(a) * L / 4; c.lineTo(x, y); c.lineWidth = W * 0.012 * (1 - j / 4); } c.stroke(); }
      c.fillStyle = 'rgba(58,46,38,0.35)'; c.beginPath(); c.arc(W / 2, H / 2, W * 0.06, 0, TAU); c.fill(); }, { res: 512, transparent: true });
    pl.userData.noAO = true; const g = grp(pl);
    g.userData.update = t => { const u = (t - (o.at ?? 0)) / 0.08; g.visible = u >= 0; g.scale.setScalar(Math.min(1, Math.max(0.01, u))); };
    g.userData.update(0); return g;
  },

  // (pass 2 of 50) A French official's sash (écharpe tricolore): a band o.len (0.8 m) long, o.w (0.12) wide, blue-white-red along its length, worn
  // across the chest; attach it to the torso (joint 'torso', rot z about 0.9) with a little knot and fringe at the low end
  sash(o) {
    const L = o.len ?? 0.8, W = o.w ?? 0.12;
    const tex = canvasPlane(W, L, (c, cw, ch) => { const s3 = cw / 3; c.fillStyle = '#1F3E9C'; c.fillRect(0, 0, s3, ch); c.fillStyle = '#F4F2EA'; c.fillRect(s3, 0, s3, ch); c.fillStyle = '#D21E2A'; c.fillRect(2 * s3, 0, cw - 2 * s3, ch); }, { res: 64 });
    const g = grp(tex, at(box(W * 0.9, 0.05, 0.03, '#E8C766'), 0, -L / 2, 0.01), at(box(W * 0.8, 0.07, 0.01, '#E8C766'), 0, -L / 2 - 0.05, 0.012));
    return g;
  },

};
