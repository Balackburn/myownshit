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
    // (pass 3 of 50) o.inner: the star's inner radius (0.62; 0.8 for a long word: the spikes bit into « BOUH ! » and swallowed its « ! »), o.fit: the
    // share of the width the word may take (0.62)
    const w = o.w ?? 0.55, txt = o.text || 'HIC !', inr = o.inner ?? 0.62, fit = o.fit ?? 0.62;
    const pl = canvasPlane(w, w * 0.62, (c, W, H) => { c.clearRect(0, 0, W, H); const cx = W / 2, cy = H / 2, n = 14;
      c.beginPath(); for (let i = 0; i <= 2 * n; i++) { const a = i * PI / n, r = (i % 2 ? inr : 0.98) * (0.5 + 0.08 * rnd(i)); c.lineTo(cx + Math.cos(a) * r * W * 0.98, cy + Math.sin(a) * r * H * 0.98); }
      c.closePath(); c.fillStyle = '#FFE14A'; c.fill(); c.lineWidth = H * 0.05; c.strokeStyle = '#1C1C1E'; c.stroke();
      c.fillStyle = '#1C1C1E'; c.textAlign = 'center'; c.textBaseline = 'middle'; let px = H * 0.42; c.font = `900 ${px}px Arial`; const tw = c.measureText(txt).width; if (tw > W * fit) { px *= W * fit / tw; c.font = `900 ${px}px Arial`; }
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
    // (pass 3 of 50) the flying pen: up 2.4 m/s and swelling to twice its size on the way (at its own size it read as a 2-3 px line sliding off the
    // paper), three fading copies behind it
    const penAt = u => ({ p: new THREE.Vector3(0.8 * u, 0.5 + 2.4 * u - 4.9 * u * u, 0.2 + 0.7 * u), rz: 9 * u, rx: 5 * u, s: 1 + Math.min(1, u / 0.15) });
    const ghosts = o.penOff == null ? [] : [0.45, 0.28, 0.14].map(op => { const gm = new THREE.MeshBasicMaterial({ color: '#2A2C31', transparent: true, opacity: op, depthWrite: false });
      const gh = grp(new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.012, 0.34), gm), new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.004, 0.05, 8), new THREE.MeshBasicMaterial({ color: '#C8202A', transparent: true, opacity: op, depthWrite: false })));
      gh.children[0].position.z = -0.17; gh.children[1].position.set(0, -0.02, -0.34); gh.children[1].rotation.x = PI / 2; gh.visible = false; g.add(gh); return gh; });
    g.userData.update = t => {
      drum.rotation.x = -t * sp / 0.11;
      const a = amp(t), off = Math.max(0, Math.abs(a) - 1.0); arm.rotation.set(-0.42 - 0.25 * off + 0.04 * off * Math.sin(t * 60), 0.42 * Math.max(-1.3, Math.min(1.3, a)), 0);
      if (o.penOff != null) { const u = t - o.penOff; arm.visible = u < 0.75; if (u >= 0) { const P = penAt(u); arm.position.copy(P.p); arm.rotation.z += P.rz; arm.rotation.x -= P.rx; arm.scale.setScalar(P.s); } else { arm.position.set(0, 0.5, 0.2); arm.scale.setScalar(1); }   // (pass 2 of 50) o.penOff: the pen flies off in an arc
        ghosts.forEach((gh, i) => { const v = u - 0.03 * (i + 1); gh.visible = v >= 0 && u < 0.5; if (gh.visible) { const P = penAt(v); gh.position.copy(P.p); gh.rotation.set(arm.rotation.x + 5 * (u - v), arm.rotation.y, arm.rotation.z - 9 * (u - v)); gh.scale.setScalar(P.s); } }); }   // (pass 3 of 50) three ghosts behind it: a smear
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
        const lab = o.labelAt == null ? 1 : t < o.labelAt ? 0 : 1 + 0.35 * Math.max(0, wob(t - o.labelAt + 0.045, 22, 7) / 0.9);   // (pass 2 of 50) o.labelAt: the label pops in on the word
        if (o.label !== '' && lab > 0) { const L = o.label || 'CANAPÉ';
          if (o.labelBelow) {   // (pass 2 of 50) under the dot, centred, its box behind the dot (beside it the box bit a notch out of the dot and ran off the frame)
            const fh = H * 0.07 * Math.min(o.labelMax ?? 2.2, 0.6 + 0.4 * zoom) * lab; c.font = `900 ${fh}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; const lw = c.measureText(L).width, ly = cy + W * 0.022 * zoom + fh * 0.95;
            c.fillStyle = '#FFFFFF'; c.fillRect(cx - lw / 2 - W * 0.02, ly - fh * 0.68, lw + W * 0.04, fh * 1.36); c.fillStyle = '#1B1B1E'; c.fillText(L, cx, ly);
            c.save(); c.translate(cx, cy); c.scale(zoom, zoom); c.translate(-cx, -cy); dot(); c.restore();
          } else { c.fillStyle = '#1B1B1E'; c.font = `bold ${H * 0.085 * Math.min(1.6, 0.8 + 0.25 * zoom)}px Arial`; c.textAlign = 'left'; c.textBaseline = 'middle';
            const lw = c.measureText(L).width; c.fillStyle = '#FFFFFF'; c.fillRect(cx + W * 0.04, cy - H * 0.12, lw + W * 0.03, H * 0.11); c.fillStyle = '#1B1B1E'; c.fillText(L, cx + W * 0.055, cy - H * 0.065); } }
        else if (o.labelBelow) { c.save(); c.translate(cx, cy); c.scale(zoom, zoom); c.translate(-cx, -cy); dot(); c.restore(); }
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
    // (pass 2 of 50) o.snap: the tape snaps. (pass 3) Into two halves that whip back to their posts, a ripple running along them, and droop to hang
    // there (it simply vanished between two frames)
    const ends = o.snap != null ? [-1, 1].map(sx => { const tx = tapeTex.clone(); tx.needsUpdate = true; tx.repeat.set(w / 2 / 0.5, 1);
      const geo = new THREE.PlaneGeometry(w / 2, 0.07, 16, 1); geo.translate(-sx * w / 4, 0, 0);   // from its post (x = 0) toward the middle
      const m = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ map: tx, side: THREE.DoubleSide })), e = grp(m); e.position.set(sx * w / 2, H, d / 2); e.visible = false; g.add(e);
      return { e, m, sx, base: geo.attributes.position.array.slice() }; }) : [];
    g.userData.update = t => { let k = 0; for (const [a, amp] of jumps) { const u = t - a; if (u >= 0 && u < 1) k += amp * wob(u, 26, 5); }
      if (o.snap != null) { const sn = t >= o.snap, u = t - o.snap; sides[2].m.visible = !sn;
        ends.forEach(E => { E.e.visible = sn; if (!sn) return; const sw = ease.out(clamp01(u / 0.16)), dr = ease.inOut(clamp01((u - 0.1) / 0.35));
          E.e.rotation.set(0, -E.sx * (2.6 * sw - 0.5 * wob(u - 0.16, 18, 5)), 0); E.e.scale.x = 1 - 0.35 * sw;   // the whip back past the post, a bounce
          const pa = E.m.geometry.attributes.position; for (let j = 0; j < pa.count; j++) { const f = Math.abs(E.base[3 * j]) / (w / 2), y = E.base[3 * j + 1];
            pa.setY(j, y + 0.09 * Math.sin(f * 3 * PI - u * 46) * Math.exp(-u * 5) * f - 0.42 * dr * f * f); } pa.needsUpdate = true; }); }
      for (const S of sides) { const pa = S.m.geometry.attributes.position; for (let j = 0; j < pa.count; j++) { const x = S.base[3 * j], y = S.base[3 * j + 1], f = Math.cos(PI * x / S.L); pa.setY(j, y + k * 0.12 * f - 0.03 * f * f); } pa.needsUpdate = true; }
      signs.forEach((sg, i) => { sg.rotation.x = 0.35 * k * (i ? -1 : 1); sg.position.y = 0.1 * k; });
      // the front plate drops with the snapped tape and lands on the floor, leaning (its group stays: only the tape mesh is hidden)
      // (pass 3) it spins toward the camera as it falls: one turn about its long axis before it lands (it slid down flat)
      if (o.snap != null && t >= o.snap && signs[0]) { const u = t - o.snap, tl = Math.sqrt((H - 0.25) / 4.9); signs[0].position.y = Math.max(-H + 0.25, -4.9 * u * u); signs[0].position.z = 0.25 * clamp01(u / tl);
        signs[0].rotation.set(-TAU * ease.out(clamp01(u / tl)), 0, Math.min(0.45, 1.6 * u)); } };
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
  // (0.6), o.color ('#4FA9E6'), o.r (0.022 m), o.life (0.75 s), o.g (9.8: lower for plaster flakes that drift): each drop flies on its arc under gravity, shrinks and is gone (the water from his cheeks)
  waterDrops(o) {
    const n = o.n ?? 16, g = grp(), dir = new THREE.Vector3(...(o.dir || [0, 0.6, 1])).normalize(), sp = o.speed ?? 2.4, spr = o.spread ?? 0.6, life = o.life ?? 0.75;
    const m = new THREE.MeshLambertMaterial({ color: o.color || '#4FA9E6', emissive: '#16507A', emissiveIntensity: 0.25 }), geo = new THREE.IcosahedronGeometry(o.r ?? 0.022, 0);
    const drops = Array.from({ length: n }, (_, i) => { const d = new THREE.Mesh(geo, m); d.castShadow = false; g.add(d);
      const v = dir.clone().add(new THREE.Vector3(Math.sin(i * 2.399) * spr, Math.cos(i * 1.7) * spr * 0.6, Math.sin(i * 3.1 + 1) * spr * 0.5)).normalize().multiplyScalar(sp * (0.7 + 0.5 * rnd(i + 3))); return { d, v, k: 0.6 + 0.8 * rnd(i) }; });
    g.userData.update = t => { const u = t - (o.at ?? 0); for (const q of drops) { const on = u >= 0 && u < life; q.d.visible = on; if (!on) continue;
      q.d.position.set(q.v.x * u, q.v.y * u - 0.5 * (o.g ?? 9.8) * u * u, q.v.z * u); q.d.scale.setScalar(q.k * (1 - 0.6 * u / life)); } };
    g.userData.update(0); return g;
  },

  // (pass 2 of 50) Cracks radiating from a point on a ceiling or a wall (a flat decal facing +Z, pivot at the centre): o.r (0.9 m), o.n (9 cracks), o.at:
  // they run out from the centre in 0.08 s
  // (pass 3 of 50) o.thick: line width times this (the 1-2 px hairlines vanished at phone size); o.edge: a light chipped edge drawn under each crack
  ceilingCracks(o) {
    const R = o.r ?? 0.9, n = o.n ?? 9, th = o.thick ?? 1;
    const pl = canvasPlane(2 * R, 2 * R, (c, W, H) => { c.clearRect(0, 0, W, H); c.lineCap = 'round'; c.lineJoin = 'round';
      const path = i => { let a = i * TAU / n + 0.3 * rnd(i), x = W / 2, y = H / 2; const L = W * (0.32 + 0.16 * rnd(i + 9)), pts = [[x, y]];
        for (let j = 0; j < 4; j++) { a += (rnd(i * 7 + j) - 0.5) * 0.7; x += Math.cos(a) * L / 4; y += Math.sin(a) * L / 4; pts.push([x, y]); } return pts; };
      for (const pass of o.edge ? [0, 1] : [1]) for (let i = 0; i < n; i++) { const pts = path(i);
        for (let j = 0; j < 4; j++) { c.beginPath(); c.moveTo(pts[j][0] + (pass ? 0 : W * 0.004 * th), pts[j][1] + (pass ? 0 : W * 0.004 * th)); c.lineTo(pts[j + 1][0] + (pass ? 0 : W * 0.004 * th), pts[j + 1][1] + (pass ? 0 : W * 0.004 * th));
          c.lineWidth = W * 0.012 * th * (1 - j / 4) * (pass ? 1 : 1.9); c.strokeStyle = pass ? '#3A2E26' : o.edge; c.stroke(); } }
      c.fillStyle = 'rgba(58,46,38,0.35)'; c.beginPath(); c.arc(W / 2, H / 2, W * 0.06, 0, TAU); c.fill(); }, { res: 512, transparent: true });
    pl.userData.noAO = true; const g = grp(pl);
    g.userData.update = t => { const u = (t - (o.at ?? 0)) / 0.08; g.visible = u >= 0; g.scale.setScalar(Math.min(1, Math.max(0.01, u))); };
    g.userData.update(0); return g;
  },

  // (pass 2 of 50) A French official's sash (écharpe tricolore): a band o.len (0.8 m) long, o.w (0.12) wide, blue-white-red along its length, worn
  // across the chest; attach it to the torso (joint 'torso', rot z about 0.9) with a little knot and fringe at the low end
  // (pass 3 of 50) a plaster ceiling seen from below (a plane facing -Y once laid with rot [PI / 2, 0, 0]): o.w x o.h, o.color, unlit with a soft
  // darker rim (lit by the room it came out the darkest, muddiest picture of the film: mean luma 125 against 150-173 everywhere else)
  ceilingPlaster(o) {
    const w = o.w ?? 7, h = o.h ?? 5.5, pl = canvasPlane(w, h, (c, W, H) => { const gr = c.createRadialGradient(W * (o.cx ?? 0.5), H * (o.cy ?? 0.5), 0, W / 2, H / 2, Math.max(W, H) * 0.62);
      gr.addColorStop(0, o.color || '#F6F1E8'); gr.addColorStop(1, o.rim || '#DCD3C4'); c.fillStyle = gr; c.fillRect(0, 0, W, H);
      for (let i = 0; i < 260; i++) { c.fillStyle = `rgba(120,100,80,${0.04 + 0.05 * rnd(i)})`; c.fillRect(W * rnd(i + 1), H * rnd(i + 2), W * 0.004, H * 0.004); } }, { res: 512 });
    pl.material = new THREE.MeshBasicMaterial({ map: pl.material.map, side: THREE.DoubleSide, toneMapped: false }); pl.userData.noAO = true; return grp(pl);
  },

  // (pass 3 of 50) a cloth over a plaque, pulled off (front +Z, origin at its centre): o.w x o.h, o.color; soft vertical folds and a scalloped hem
  // that sway; from o.at it crumples while its keys carry it away: the folds deepen, the top edge curls over, it gathers to a third of its height in
  // o.dur (0.3 s) (a flat sheet read as a stiff red slab)
  unveilCloth(o) {
    const w = o.w ?? 1.2, h = o.h ?? 0.6, geo = new THREE.PlaneGeometry(w, h, 18, 10), pa = geo.attributes.position, base = pa.array.slice();
    const m = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ color: o.color || '#B5302A', side: THREE.DoubleSide, flatShading: true })); m.castShadow = true;
    const g = grp(m), t0 = o.at ?? 1e9, dur = o.dur ?? 0.3, nf = o.folds ?? 4;
    g.userData.update = t => { const u = clamp01((t - t0) / dur), sway = 0.012 * Math.sin(t * 2.3);
      for (let i = 0; i < pa.count; i++) { const x = base[3 * i], y = base[3 * i + 1], v = 0.5 - y / h;   // v: 0 at the top edge, 1 at the hem
        const fold = Math.sin((x / w + 0.5) * nf * TAU) * (0.02 + 0.025 * v + 0.07 * u), hem = -0.035 * v * v * (0.5 + 0.5 * Math.cos((x / w) * 11)) * (1 - u);
        pa.setXYZ(i, x * (1 - 0.3 * u * v), y * (1 - 0.62 * u) + hem - 0.2 * u * u * h * v, fold + 0.3 * u * (1 - v) * (1 - v) + sway * v); }
      pa.needsUpdate = true; geo.computeVertexNormals(); };
    g.userData.update(0); return g;
  },

  sash(o) {
    const L = o.len ?? 0.8, W = o.w ?? 0.12;
    const tex = canvasPlane(W, L, (c, cw, ch) => { const s3 = cw / 3; c.fillStyle = '#1F3E9C'; c.fillRect(0, 0, s3, ch); c.fillStyle = '#F4F2EA'; c.fillRect(s3, 0, s3, ch); c.fillStyle = '#D21E2A'; c.fillRect(2 * s3, 0, cw - 2 * s3, ch); }, { res: 64 });
    const g = grp(tex, at(box(W * 0.9, 0.05, 0.03, '#E8C766'), 0, -L / 2, 0.01), at(box(W * 0.8, 0.07, 0.01, '#E8C766'), 0, -L / 2 - 0.05, 0.012));
    return g;
  },

  // (pass 2 of 50) A height ruler on a wall (front +Z, pivot at the foot of the bar): a yellow bar o.h (1.0 m) tall, o.w (0.09) wide, black ticks every
  // 0.1 m (long ones at the ends and the middle), black end bars, and a yellow plate with o.text ('1 M') in big black capitals beside its middle (o.side
  // 1: to the right, -1: to the left; o.plateW 0.46). o.pops [t, ...]: the plate jumps (scale 1.3 -> 1 with a wobble) at each time (he reaches the mark).
  heightRuler(o) {
    const H = o.h ?? 1.0, W = o.w ?? 0.09, g = grp(at(box(W, H, 0.02, '#F2C80F', { outline: 0.005 }), 0, H / 2, 0));
    for (let i = 0; i <= 10; i++) { const L = i % 5 === 0 ? W * 1.9 : W * 0.7; g.add(at(box(L, 0.012, 0.024, '#1B1B1E'), (L - W) / 2 - (i % 5 === 0 ? (L - W) / 2 : 0), H * i / 10, 0.002)); }
    const pw = o.plateW ?? 0.46, ph = pw * 0.5, side = o.side ?? 1, plate = grp(at(box(pw, ph, 0.025, '#F2C80F', { outline: 0.006 }), 0, 0, 0), at(label(o.text || '1 M', pw * 0.86, ph * 0.8, { bg: null, fg: '#1B1B1E', wrap: false }), 0, 0, 0.015));
    plate.position.set(side * (W / 2 + pw / 2 + 0.05), H / 2, 0.01); g.add(plate);
    g.add(at(box(0.05, 0.01, 0.02, '#1B1B1E'), side * (W / 2 + 0.025), H / 2, 0.01));
    g.userData.update = t => { let k = 0; for (const a of list(o.pops)) { const u = t - a; if (u >= 0 && u < 0.6) k = Math.max(k, Math.exp(-u * 7) * (0.3 + 0.1 * Math.sin(u * 30))); } plate.scale.setScalar(1 + k); };
    g.userData.update(0); return g;
  },

  // (pass 2 of 50) A giant novelty cheque (front +Z, pivot at its centre): o.w (1.0 m) x o.h (0.46), a stiff board; o.amount ('3 000 €') in big type over
  // half its height, o.text (the payer, 'ASSURANCE') top left, a signature; o.flutter (t): from then on it rocks and swings like a falling leaf (move it
  // down with keys: to=..., the flutter is inside, about its centre).
  bigCheque(o) {
    const w = o.w ?? 1.0, h = o.h ?? 0.46, inner = grp(), g = grp(inner);
    const face = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#EAF3E6'; c.fillRect(0, 0, W, H); c.strokeStyle = '#2C6A4A'; c.lineWidth = H * 0.03; c.strokeRect(H * 0.04, H * 0.04, W - H * 0.08, H * 0.92);
      c.fillStyle = '#2C6A4A'; c.font = `bold ${H * 0.13}px Arial`; c.textAlign = 'left'; c.textBaseline = 'middle'; c.fillText(o.text || 'ASSURANCE', W * 0.05, H * 0.17);
      c.fillStyle = '#1B1B1E'; c.textAlign = 'center'; let fs = H * 0.42; c.font = `900 ${fs}px Arial`; while (c.measureText(o.amount || '3 000 €').width > W * 0.86 && fs > 10) { fs -= 2; c.font = `900 ${fs}px Arial`; } c.fillText(o.amount || '3 000 €', W * 0.5, H * 0.56);
      c.strokeStyle = '#1B2A6B'; c.lineWidth = H * 0.025; c.beginPath(); c.moveTo(W * 0.6, H * 0.88); for (let i = 0; i < 7; i++) c.lineTo(W * (0.62 + i * 0.045), H * (i % 2 ? 0.8 : 0.9)); c.stroke(); }, { res: 768 });
    face.position.z = 0.009; inner.add(at(box(w, h, 0.016, '#DDE8D8', { outline: 0.006 }), 0, 0, 0), face);
    g.userData.update = t => { if (o.flutter == null || t < o.flutter) { inner.rotation.set(0, 0, 0); inner.position.set(0, 0, 0); return; } const u = t - o.flutter;
      inner.rotation.set(0.5 * Math.sin(u * 5.3 + 0.6), 0, 0.45 * Math.sin(u * 7.0)); inner.position.set(0.12 * Math.sin(u * 7.0), 0.03 * Math.cos(u * 14), 0); };
    g.userData.update(0); return g;
  },

};
