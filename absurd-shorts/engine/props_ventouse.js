// « La ventouse » (story 55, cycle 17): a man stuck a plunger on his forehead; it will not come off; his mutual insurer will not pay (it is plumbing),
// the plumber will not either (it is a forehead); since then he sticks to everything; the metro hired him as a handle; yesterday the plunger came off:
// the metro kept it; he is out of work. Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure
// function of the shot time.
import * as THREE from 'three';
import { mat, box, cyl, addOutline } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const list = v => [].concat(v ?? []);
// a damped wobble started at each time of a list: [[t, amplitude (rad), frequency (rad/s), decay (1/s)], ...] (the latest one wins)
function wobbleAt(ks, t) {
  let v = 0;
  for (const k of list(ks)) { const [t0, a, f = 34, d = 6] = k, u = t - t0; if (u < 0) continue; v = a * Math.exp(-d * u) * Math.sin(f * u); }
  return v;
}

export const VENTOUSE_PROPS = {
  // A sink plunger (pivot at the middle of the rim of its cup, the handle up +Y): a red rubber cup o.r (0.075 m) wide at the rim, a wooden handle
  // o.len (0.46 m) with a dark knob. o.wobble [[t, amp, freq, decay], ...]: the handle springs about the cup after a flick (a damped swing in X, a
  // little in Z); o.squash [[t, k]]: the cup flattens (k: 0.5 = half its height) and springs back (it sucks onto something);
  // o.cupColor, o.handleColor.
  plunger(o) {
    const R = o.r ?? 0.075, Lh = o.len ?? 0.46, cupC = o.cupColor || '#C2312A', hC = o.handleColor || '#C8935A';
    const cup = cyl(R * 0.48, R, R * 0.95, cupC, 14, { pivot: 'bottom' }); addOutline(cup, 0.006);
    const lip = at(cyl(R * 1.04, R * 1.04, 0.012, '#A3271F', 14), 0, 0.006, 0);
    const handle = grp(at(cyl(0.015, 0.015, Lh, hC, 8, { pivot: 'bottom' }), 0, 0, 0), at(cyl(0.026, 0.022, 0.05, '#4A2E1C', 8, { pivot: 'bottom' }), 0, Lh, 0));
    addOutline(handle.children[0], 0.004); handle.position.y = R * 0.9;
    const body = grp(cup, lip), g = grp(body, handle);
    g.userData.grip = [0, R * 0.9 + Lh * 0.8, 0];
    g.userData.update = t => {
      const w = wobbleAt(o.wobble, t); handle.rotation.x = w; handle.rotation.z = 0.35 * w;
      let k = 1; for (const s of list(o.squash)) { const u = t - s[0]; if (u >= 0 && u < 0.5) k = 1 - (1 - (s[1] ?? 0.55)) * Math.exp(-7 * u) * Math.cos(16 * u); }
      body.scale.set(1 + (1 - k) * 0.45, k, 1 + (1 - k) * 0.45); handle.position.y = R * 0.9 * k;
    };
    g.userData.update(0); return g;
  },

  // A kitchen island with a sink (pivot at the floor in its middle, front +Z): a cream block o.w (1.5) x o.d (0.75) x o.h (0.9) on a dark plinth, a
  // wooden top, a steel basin in the middle (its drain 0.16 m down: userData.drain), a goose-neck tap at the back, a sponge. The man stands at its
  // front and the camera can stand at its back (a sink against a wall only ever showed his back).
  islandSink(o) {
    const W = o.w ?? 1.5, D = o.d ?? 0.75, H = o.h ?? 0.9, g = grp();
    g.add(at(box(W, H - 0.1, D, o.color || '#F2EEE2', { pivot: 'bottom', outline: 0.008 }), 0, 0.1, 0), at(box(W - 0.06, 0.1, D - 0.06, '#5A5248', { pivot: 'bottom' }), 0, 0, 0));
    for (const [x, w] of [[-W / 2 + (W - 0.6) / 4, (W - 0.6) / 2], [W / 2 - (W - 0.6) / 4, (W - 0.6) / 2]]) g.add(at(box(w, 0.04, D + 0.04, o.top || '#B98A5A', { outline: 0.005 }), x, H, 0));
    g.add(at(box(0.6, 0.04, 0.1, o.top || '#B98A5A'), 0, H, -D / 2 + 0.05), at(box(0.6, 0.04, 0.1, o.top || '#B98A5A'), 0, H, D / 2 - 0.05));
    g.add(at(box(0.54, 0.16, D - 0.22, '#3E4448'), 0, H - 0.08, 0), at(box(0.58, 0.02, D - 0.18, '#C9CCD1', { outline: 0.004 }), 0, H - 0.005, 0), at(cyl(0.03, 0.03, 0.01, '#202428', 10), 0, H - 0.155, 0));
    const tap = grp(at(cyl(0.02, 0.02, 0.32, '#C9CCD1', 8, { pivot: 'bottom' }), 0, 0, 0), at(cyl(0.018, 0.018, 0.18, '#C9CCD1', 8), 0, 0.32, 0.07, PI / 2, 0, 0), at(cyl(0.016, 0.014, 0.06, '#C9CCD1', 8), 0, 0.29, 0.15));
    g.add(at(tap, 0, H, -D / 2 + 0.07), at(box(0.12, 0.05, 0.08, '#F2C230', { outline: 0.004 }), 0.42, H + 0.045, -0.15));
    g.userData.drain = [0, H - 0.155, 0]; return g;
  },

  // The mark the plunger leaves (front +Z, pivot at its centre, flat in XY): a red ring o.r (0.07 m) with a pink inside, to wear on a forehead.
  ringMark(o) {
    const R = o.r ?? 0.07, ring = new THREE.Mesh(new THREE.TorusGeometry(R, R * 0.18, 6, 24), mat(o.color || '#D23B32'));
    const inner = new THREE.Mesh(new THREE.CircleGeometry(R * 0.9, 24), mat(o.inner || '#F2A9A0'));
    inner.position.z = -0.004; ring.scale.z = 0.35; return grp(ring, inner);
  },

  // A metro carriage (pivot at the floor in its middle, its length along X, the doors on both long sides): o.len (12 m) x o.w (2.6) x o.h (2.3); grey
  // floor, cream walls with a teal band, dark window panes (the tunnel), blue bench seats along the walls, steel poles and two grab bars along the
  // ceiling, white light strips, sliding doors (o.doorColor) every o.doorEvery m; shells seen from inside and outside alike. o.sway [amp, freq]: the
  // whole car rocks (rad); o.light: light strips glow.
  metroCar(o) {
    const L = o.len ?? 12, W = o.w ?? 2.6, H = o.h ?? 2.3, g = grp(), wallC = o.wall || '#ECE7DA', band = o.band || '#2E8C86', glass = '#1E2A33', doorC = o.doorColor || '#2F6FB5';
    g.add(at(box(L, 0.06, W, o.floor || '#7C8288', { outline: 0.006 }), 0, -0.03, 0), at(box(L, 0.08, W, '#EDECE6'), 0, H + 0.04, 0));
    const every = o.doorEvery ?? 4, doors = [];
    for (const s of [-1, 1]) {
      const z = s * W / 2;
      g.add(at(box(L, 0.9, 0.06, wallC, { outline: 0.006 }), 0, 0.45, z), at(box(L, 0.5, 0.065, wallC), 0, H - 0.25, z), at(box(L, 0.08, 0.07, band), 0, 0.92, z));
      for (let x = -L / 2 + every / 2; x < L / 2; x += every) {
        for (const dx of [-1.25, 1.25]) g.add(at(box(1.3, 0.85, 0.05, glass), x + dx, 1.43, z), at(box(1.36, 0.06, 0.07, '#B9BEC4'), x + dx, 1.87, z), at(box(1.36, 0.06, 0.07, '#B9BEC4'), x + dx, 0.99, z));
        const d = at(grp(at(box(0.62, 2.0, 0.07, doorC, { outline: 0.006 }), -0.31, 1.0, 0), at(box(0.62, 2.0, 0.07, doorC, { outline: 0.006 }), 0.31, 1.0, 0),
          at(box(0.4, 0.6, 0.075, glass), -0.31, 1.4, 0), at(box(0.4, 0.6, 0.075, glass), 0.31, 1.4, 0)), x, 0, z); g.add(d); doors.push(d);
        if (s < 0) for (const dx of [-1.25, 1.25]) g.add(at(box(1.15, 0.12, 0.42, o.seat || '#2F5C9E', { outline: 0.005 }), x + dx, 0.45, -W / 2 + 0.3), at(box(1.15, 0.45, 0.08, o.seat || '#2F5C9E'), x + dx, 0.72, -W / 2 + 0.1),
          at(box(1.15, 0.12, 0.42, o.seat || '#2F5C9E', { outline: 0.005 }), x + dx, 0.45, W / 2 - 0.3), at(box(1.15, 0.45, 0.08, o.seat || '#2F5C9E'), x + dx, 0.72, W / 2 - 0.1));
        for (const sz of [-1, 1]) g.add(at(cyl(0.022, 0.022, H, '#C9CCD1', 8, { pivot: 'bottom' }), x + 0.8 * sz, 0, sz * 0.35));
      }
    }
    for (const s of [-1, 1]) g.add(at(cyl(0.02, 0.02, L, '#C9CCD1', 8), 0, 2.0, s * 0.42, 0, 0, PI / 2));
    for (let x = -L / 2 + 1; x < L / 2; x += 2) g.add(at(box(1.4, 0.03, 0.22, '#FFFFFF', { emissive: o.light === false ? null : '#FFF8E6', noGrain: true }), x, H - 0.01, 0));
    for (const sx of [-1, 1]) g.add(at(box(0.06, H, W, wallC, { outline: 0.006 }), sx * L / 2, H / 2, 0));
    g.userData.update = t => { if (!o.sway) return; g.rotation.x = o.sway[0] * Math.sin(t * (o.sway[1] ?? 9)); };
    g.userData.update(0); return g;
  },

  // A metro platform (pivot at the platform edge in its middle, the track toward +Z, the platform toward -Z): white bevelled tiles on the curved back
  // wall, a blue enamel station sign o.name, a slatted bench, the yellow edge line, the dark track pit below the edge. o.len (14 m).
  metroPlatform(o) {
    const L = o.len ?? 14, D = o.depth ?? 4, g = grp();
    g.add(at(box(L, 1.0, D, '#B9B2A6', { outline: 0.006 }), 0, -0.5, -D / 2), at(box(L, 0.012, 0.18, '#F2C230'), 0, 0.006, -0.25), at(box(L, 0.4, 3.4, '#2A2C30'), 0, -1.2, 1.7));
    const tiles = canvasPlane(L, 3.6, (c, Wd, Ht) => { c.fillStyle = '#F4F2EC'; c.fillRect(0, 0, Wd, Ht); c.strokeStyle = '#C9C5BC'; c.lineWidth = 2;
      const tw = Wd / (L / 0.15), th = Ht / (3.6 / 0.075); for (let y = 0; y < Ht; y += th) { c.beginPath(); c.moveTo(0, y); c.lineTo(Wd, y); c.stroke(); for (let x = ((y / th) % 2) * tw / 2; x < Wd; x += tw) { c.beginPath(); c.moveTo(x, y); c.lineTo(x, y + th); c.stroke(); } } }, { res: 1024 });
    g.add(at(tiles, 0, 1.8, -D + 0.02));
    const sign = canvasPlane(2.4, 0.5, (c, Wd, Ht) => { c.fillStyle = '#1F3F8F'; c.fillRect(0, 0, Wd, Ht); c.strokeStyle = '#FFFFFF'; c.lineWidth = Ht * 0.06; c.strokeRect(Ht * 0.08, Ht * 0.08, Wd - Ht * 0.16, Ht - Ht * 0.16);
      c.fillStyle = '#FFFFFF'; c.font = `bold ${Ht * 0.5}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.name || 'RUE DES ARTS', Wd / 2, Ht * 0.54); }, { res: 768 });
    g.add(at(box(2.5, 0.6, 0.04, '#13295E'), 0, 2.2, -D + 0.05), at(sign, 0, 2.2, -D + 0.075));
    const bench = grp(); for (let i = 0; i < 3; i++) bench.add(at(box(1.6, 0.04, 0.1, '#B5672E'), 0, 0.45, -0.12 + i * 0.12)); bench.add(at(box(1.6, 0.36, 0.05, '#B5672E'), 0, 0.68, -0.22, -0.12, 0, 0));
    for (const sx of [-0.7, 0.7]) bench.add(at(box(0.05, 0.45, 0.32, '#3A3C40', { pivot: 'bottom' }), sx, 0, 0));
    g.add(at(bench, o.benchX ?? 0, 0, -D + 0.8));
    return g;
  },
};
