// « La porte » (story 39): a man holds a door for a lady and can never let go of it.
// Conventions as in props.js (metres, front +Z, pivot at the floor); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, sphere, rng, ease, clamp01 } from './style.js';
import { grp, at, canvasPlane, glassMat } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const txt = (g, s, x, y, px, color = '#1B1B1E', weight = '900') => { g.fillStyle = color; g.font = `${weight} ${px}px Arial`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(s, x, y); };
const fit = (g, s, w, px, weight = '900') => { g.font = `${weight} ${px}px Arial`; const m = g.measureText(s).width; return m > w ? px * w / m : px; };
const wob = (t, f = 30, d = 6) => (t <= 0 ? 0 : Math.sin(t * f) * Math.exp(-t * d));
// keys [[t, v], ...] -> value at t (linear between keys, held outside); o.ease eases each span
const keyed = (keys, t, e) => { if (!keys || !keys.length) return 0; if (t <= keys[0][0]) return keys[0][1]; for (let i = 0; i < keys.length - 1; i++) { const [t0, v0] = keys[i], [t1, v1] = keys[i + 1]; if (t < t1) { const u = clamp01((t - t0) / Math.max(1e-6, t1 - t0)); return v0 + (v1 - v0) * (e ? e(u) : u); } } return keys[keys.length - 1][1]; };

// where the handle of a shopDoor is, in the door's own frame, when the leaf is open by `deg` degrees and slid by `slide` metres (for a guided hand).
// The same numbers as in shopDoor below: hinge on the left jamb, the bar 0.12 m from the free edge, 0.07 m off the glass, 1.1 m up
export const doorHandle = (w = 1.0, deg = 0, slide = 0) => { const a = deg * PI / 180, r = w - 0.12; return [-w / 2 + r * Math.cos(a) - 0.07 * Math.sin(a) + slide, 1.1, 0.03 + r * Math.sin(a) + 0.07 * Math.cos(a)]; };

export const PORTE_PROPS = {
  // a shop entrance: two jambs and a lintel, a sign band above (o.sign), a glass door leaf hinged on the left jamb with a long bar handle on its outer face.
  // o.swing [[t, degrees], ...]: how far the leaf is open (0 closed, 80 held open toward +Z); o.slide [[t, metres], ...]: the leaf slides sideways into the wall
  // (it was automatic all along); o.led [t]: the sensor above the door turns from red to green at that time. Origin: the middle of the threshold
  shopDoor(o) {
    const w = o.w ?? 1.0, h = o.h ?? 2.5, fr = o.frame || '#2E4A3F', sign = o.sign || 'BOULANGERIE', sw = o.signW ?? w + 1.5;
    const g = grp(at(box(0.14, h + 0.14, 0.2, fr, { outline: 0.008 }), -w / 2 - 0.07, (h + 0.14) / 2, 0), at(box(0.14, h + 0.14, 0.2, fr, { outline: 0.008 }), w / 2 + 0.07, (h + 0.14) / 2, 0), at(box(w + 0.28, 0.14, 0.2, fr, { outline: 0.008 }), 0, h + 0.07, 0));
    if (o.sign !== false) { const band = canvasPlane(sw, 0.6, (c, W, H) => { c.fillStyle = o.signBg || '#F6E7C8'; c.fillRect(0, 0, W, H); c.strokeStyle = fr; c.lineWidth = H * 0.06; c.strokeRect(H * 0.05, H * 0.05, W - H * 0.1, H * 0.9); txt(c, sign, W / 2, H * 0.54, fit(c, sign, W * 0.86, H * 0.6), o.signFg || '#7A3B1E'); }, { res: 768 });
      g.add(at(box(sw + 0.08, 0.68, 0.1, fr, { outline: 0.008 }), 0, h + 0.14 + 0.36, 0.02), at(band, 0, h + 0.14 + 0.36, 0.075)); }
    // what is seen through the doorway: a warm bakery (shelves, loaves, a counter), painted on a plane just behind the leaf (o.inside false: a dark hall)
    g.add(at(o.inside === false ? box(w, h, 0.02, '#2A2420') : canvasPlane(w, h, (c, W, H) => { const gr = c.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#F6D38A'); gr.addColorStop(1, '#C98A3E'); c.fillStyle = gr; c.fillRect(0, 0, W, H);
      for (let i = 0; i < 4; i++) { const y = H * (0.16 + i * 0.15); c.fillStyle = '#7A4A22'; c.fillRect(W * 0.06, y, W * 0.88, H * 0.018); for (let k = 0; k < 5; k++) { c.fillStyle = k % 2 ? '#D99A45' : '#C27A2E'; c.beginPath(); c.ellipse(W * (0.16 + k * 0.17), y - H * 0.03, W * 0.07, H * 0.026, -0.3, 0, TAU); c.fill(); } }
      c.fillStyle = '#8A5A2E'; c.fillRect(0, H * 0.74, W, H * 0.26); c.fillStyle = '#A9703A'; c.fillRect(0, H * 0.74, W, H * 0.03); }, { res: 384, emissive: 0.5 }), 0, h / 2, -0.07));
    const sensor = at(box(0.2, 0.08, 0.08, '#23262C'), 0, h + 0.02, 0.13), led = at(sphere(0.022, '#E8322A', 1), 0.06, h + 0.02, 0.175); led.material = led.material.clone(); led.material.emissive = new THREE.Color('#FF3B2A'); led.material.emissiveIntensity = 0.9; g.add(sensor, led);
    const track = new THREE.Group(), piv = new THREE.Group(); piv.position.set(-w / 2, 0, 0.03); track.add(piv); g.add(track);
    const glass = at(box(w - 0.06, h - 0.08, 0.02, '#BFE3EE'), w / 2, h / 2, 0); glass.material = glassMat(o.glass ?? 0.34, '#BFE3EE'); glass.castShadow = false;   // o.glass: how much the pane veils what is behind it (0.34; 0.14 for somebody pressed behind it who must stay readable)
    piv.add(glass, at(box(w, 0.07, 0.05, '#8A9097'), w / 2, 0.035, 0), at(box(w, 0.07, 0.05, '#8A9097'), w / 2, h - 0.035, 0), at(box(0.07, h, 0.05, '#8A9097'), 0.035, h / 2, 0), at(box(0.07, h, 0.05, '#8A9097'), w - 0.035, h / 2, 0),
      at(cyl(0.022, 0.022, 0.62, '#D9B45A', 8, { outline: 0.006 }), w - 0.12, 1.1, 0.07), at(box(0.03, 0.03, 0.07, '#D9B45A'), w - 0.12, 1.36, 0.035), at(box(0.03, 0.03, 0.07, '#D9B45A'), w - 0.12, 0.84, 0.035),
      at(cyl(0.022, 0.022, 0.62, '#D9B45A', 8), w - 0.12, 1.1, -0.07));
    g.userData.update = t => { piv.rotation.y = -keyed(o.swing, t, ease.inOut) * PI / 180; track.position.x = keyed(o.slide, t, ease.inOut);
      const on = o.led != null && t >= o.led; led.material.color.set(on ? '#3CC46E' : '#E8322A'); led.material.emissive.set(on ? '#3CE07A' : '#FF3B2A'); };
    g.userData.update(0); return g;
  },

  // a sleeve that has been stretched across the town: navy segments through o.path [[x, y, z], ...] (in the prop's frame), sagging a little between
  // the points (o.sag), o.r thick. o.grow [t0, t1]: it is paid out from the first point to the last between those times. o.hand: a cuff and a hand at the end
  sleeveLine(o) {
    const path = o.path || [[0, 1, 0], [3, 1, 0]], r = o.r ?? 0.05, col = o.color || '#1E2E44', g = new THREE.Group(), pts = [], sag = o.sag ?? 0.12, segs = [];
    for (let i = 0; i < path.length - 1; i++) { const a = new THREE.Vector3(...path[i]), b = new THREE.Vector3(...path[i + 1]), n = Math.max(2, Math.round(a.distanceTo(b) / 0.6)); for (let k = 0; k < n; k++) { const u = k / n, p = a.clone().lerp(b, u); p.y -= sag * Math.sin(u * PI) * Math.min(1, a.distanceTo(b) / 3); pts.push(p); } }
    pts.push(new THREE.Vector3(...path[path.length - 1])); let tot = 0;
    for (let i = 0; i < pts.length - 1; i++) { const a = pts[i], b = pts[i + 1], L = a.distanceTo(b), m = box(r * 2, L * 1.04, r * 1.6, col); m.position.copy(a).lerp(b, 0.5); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), b.clone().sub(a).normalize()); g.add(m); segs.push([m, tot, L]); tot += L; }
    let hand = null;
    if (o.hand) { const e = pts[pts.length - 1], d = e.clone().sub(pts[pts.length - 2]).normalize(); hand = grp(at(box(r * 2.3, 0.07, r * 1.9, '#F4F1E8'), 0, 0.035, 0), at(box(0.085, 0.1, 0.045, o.skin || '#E2B48A'), 0, 0.12, 0)); hand.position.copy(e); hand.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d); g.add(hand); }
    g.userData.update = t => { if (!o.grow) return; const k = ease.inOut(clamp01((t - o.grow[0]) / Math.max(1e-6, o.grow[1] - o.grow[0]))) * tot; for (const [m, d0, L] of segs) m.visible = d0 < k; if (hand) hand.visible = k >= tot - 1e-3; };
    g.userData.update(0); g.userData.length = tot; return g;
  },

  // a counter on the wall: « PASSAGES PAR JOUR » and a number that rolls from o.from to o.to between o.at and o.at + o.dur, then blinks. Front +Z, origin at its centre
  rollCounter(o) {
    const w = o.w ?? 1.1, h = o.h ?? 0.7, from = o.from ?? 0, to = o.to ?? 4000, at_ = o.at ?? 0.2, dur = o.dur ?? 0.6, label = o.label || 'PASSAGES PAR JOUR';
    const fmt = n => String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    let last = null, ctx = null, tex = null, W0 = 0, H0 = 0;
    const draw = n => { const c = ctx, W = W0, H = H0; c.fillStyle = '#1B2A4A'; c.fillRect(0, 0, W, H); c.fillStyle = '#F7F4EA'; c.fillRect(W * 0.04, H * 0.3, W * 0.92, H * 0.62); txt(c, label, W / 2, H * 0.16, fit(c, label, W * 0.9, H * 0.17), '#F7F4EA'); txt(c, fmt(n), W / 2, H * 0.63, fit(c, '0 000', W * 0.8, H * 0.5), '#C8202A'); };
    const face = canvasPlane(w, h, (c, W, H) => { ctx = c; W0 = W; H0 = H; draw(from); }, { res: 512 }); tex = face.material.map;
    const g = grp(at(box(w * 1.05, h * 1.08, 0.06, '#23262C', { outline: 0.008 }), 0, 0, -0.035), face);
    g.userData.update = t => { const u = clamp01((t - at_) / dur), n = Math.round(from + (to - from) * ease.out(u)); if (n !== last && ctx) { last = n; draw(n); if (tex) tex.needsUpdate = true; }
      face.scale.setScalar(1 + (u >= 1 ? 0.05 * Math.abs(wob(t - at_ - dur, 18, 5)) : 0)); };
    g.userData.update(0); return g;
  },

  // a hand tally counter (a chrome clicker held in a fist): its thumb button pumps o.rate times a second from o.at. Origin at the grip
  tallyClicker(o) {
    const g = grp(at(cyl(0.035, 0.035, 0.03, '#C9CED3', 12, { outline: 0.006 }), 0, 0, 0, PI / 2, 0, 0), at(box(0.04, 0.018, 0.012, '#1B1B1E'), 0, 0.004, 0.017)), btn = at(cyl(0.01, 0.01, 0.03, '#8A9097', 6), 0.02, 0.04, 0); g.add(btn);
    g.userData.update = t => { const u = t - (o.at ?? 0); btn.position.y = 0.04 - (u > 0 ? 0.012 * Math.abs(Math.sin(u * PI * (o.rate ?? 12))) : 0); };
    g.userData.grip = [0, 0, 0]; return g;
  },

  // a doorman's cap (burgundy, a gold band, a black peak); origin at the base (the top of a head)
  doormanCap(o) {
    const c = o.color || '#7A1E2A';
    return grp(at(cyl(0.125, 0.115, 0.09, c, 14, { outline: 0.008 }), 0, 0.045, 0), at(cyl(0.132, 0.132, 0.014, c, 14), 0, 0.095, 0), at(cyl(0.118, 0.118, 0.028, '#D9B45A', 14), 0, 0.022, 0), at(box(0.17, 0.012, 0.09, '#1B1B1E'), 0, 0.008, 0.13, 0.2, 0, 0));
  },

  // a bronze plaque with engraved text (o.text, two lines split on a slash) and four screws. Front +Z, origin at its centre
  bronzePlaque(o) {
    const w = o.w ?? 0.6, h = o.h ?? 0.36, lines = (o.text || 'MONUMENT/HISTORIQUE').split('/');
    const face = canvasPlane(w, h, (c, W, H) => { const gr = c.createLinearGradient(0, 0, W, H); gr.addColorStop(0, '#C9A25A'); gr.addColorStop(0.5, '#E2C27E'); gr.addColorStop(1, '#A9843E'); c.fillStyle = gr; c.fillRect(0, 0, W, H); c.strokeStyle = '#6B4A1E'; c.lineWidth = H * 0.05; c.strokeRect(H * 0.07, H * 0.07, W - H * 0.14, H * 0.86);
      lines.forEach((s, i) => txt(c, s, W / 2, H * (lines.length === 1 ? 0.52 : 0.34 + i * 0.33), fit(c, s, W * 0.8, H * 0.26), '#4A3212')); }, { res: 512 });
    const g = grp(at(box(w * 1.03, h * 1.05, 0.03, '#8A6A2E', { outline: 0.008 }), 0, 0, -0.018), face);
    for (const [x, y] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) g.add(at(cyl(0.012, 0.012, 0.012, '#6B4A1E', 6), x * w * 0.44, y * h * 0.38, 0.006, PI / 2, 0, 0));
    return g;
  },

  // a wall box with one big button and a lamp (red, green from o.at); the button goes in at o.at. Front +Z, origin at its centre
  wallSwitch(o) {
    const lamp = at(sphere(0.03, '#E8322A', 1), 0, 0.1, 0.05); lamp.material = lamp.material.clone(); lamp.material.emissive = new THREE.Color('#FF3B2A'); lamp.material.emissiveIntensity = 0.9;
    const btn = at(cyl(0.055, 0.055, 0.04, '#3CC46E', 12, { outline: 0.006 }), 0, -0.04, 0.05, PI / 2, 0, 0), g = grp(at(box(0.2, 0.34, 0.07, '#C9CED3', { outline: 0.008 }), 0, 0, 0), lamp, btn);
    if (o.label !== false) g.add(at(canvasPlane(0.18, 0.06, (c, W, H) => { c.fillStyle = '#1B1B1E'; c.fillRect(0, 0, W, H); txt(c, o.label || 'AUTO', W / 2, H * 0.55, fit(c, o.label || 'AUTO', W * 0.8, H * 0.7), '#F7F4EA'); }, { res: 256 }), 0, -0.135, 0.037));
    g.userData.update = t => { const on = o.at != null && t >= o.at; lamp.material.color.set(on ? '#3CC46E' : '#E8322A'); lamp.material.emissive.set(on ? '#3CE07A' : '#FF3B2A'); btn.position.z = 0.05 - (on ? 0.02 * Math.min(1, (t - o.at) / 0.05) : 0); };
    g.userData.update(0); return g;
  },

  // a pigeon standing on something (a wire, a sleeve): a round grey breast, a small head with a beak and an eye, a green and violet patch on the neck, folded
  // wings, a tail wedge, pink legs; it bobs its head. Seen from the side it reads as a pigeon (front on it was a grey cube). o.flyAt: it takes off and is
  // gone; o.flap [t0, t1]: its wings beat between these times (it is landing); o.sleep: head tucked into its shoulders, puffed up. Origin at its feet, facing +Z
  pigeon(o) {
    const G = '#8E98A6', D = '#6E7A8A', body = at(box(0.13, 0.12, 0.22, G, { outline: 0.008, taper: { x: 0.8, z: 0.7 } }), 0, 0.1, 0), breast = at(sphere(0.075, '#9AA4B2', 1), 0, 0.105, 0.07), tail = at(box(0.09, 0.02, 0.13, D, { outline: 0.006, taper: { x: 1.5, z: 1 }, taperAxis: 'z' }), 0, 0.09, -0.16, 0.25, 0, 0);
    const head = grp(at(box(0.07, 0.07, 0.075, D, { outline: 0.006 }), 0, 0, 0), at(box(0.02, 0.018, 0.045, '#E8A33C'), 0, -0.008, 0.055), at(box(0.074, 0.03, 0.06, '#5E8F6E'), 0, -0.045, -0.002), at(box(0.072, 0.02, 0.058, '#8A6AA8'), 0, -0.068, -0.002),
      at(sphere(0.012, '#17161A', 0), 0.036, 0.008, 0.014), at(sphere(0.012, '#17161A', 0), -0.036, 0.008, 0.014)); head.position.set(0, 0.2, 0.1);
    const wl = at(box(0.02, 0.08, 0.17, D), -0.072, 0.11, -0.02), wr = at(box(0.02, 0.08, 0.17, D), 0.072, 0.11, -0.02), g = grp(body, breast, tail, head, wl, wr, at(box(0.012, 0.05, 0.012, '#D98A8A'), -0.03, 0.025, 0.01), at(box(0.012, 0.05, 0.012, '#D98A8A'), 0.03, 0.025, 0.01));
    const ph = o.ph ?? 0;
    g.userData.update = t => { const fly = o.flyAt != null ? Math.max(0, t - o.flyAt) : 0, fl = !!(o.flap && t >= o.flap[0] && t < o.flap[1]);
      if (o.sleep) { head.position.set(0, 0.15, 0.05); head.rotation.x = 0.5; body.scale.set(1.12, 1.12 + 0.04 * Math.sin(t * 2 + ph), 1); }
      else { head.position.z = 0.1 + 0.02 * Math.max(0, Math.sin(t * 7 + ph)); head.position.y = 0.2 - 0.03 * Math.max(0, Math.sin(t * 2.3 + ph * 2)); }
      wl.rotation.z = fly || fl ? 1.2 * Math.sin((fly || t) * 40) + 0.6 : 0; wr.rotation.z = fly || fl ? -1.2 * Math.sin((fly || t) * 40) - 0.6 : 0;
      if (o.flyAt != null) { g.position.y = (g.userData.y0 ??= g.position.y) + fly * 6 * fly + (fly ? 0.3 : 0) * Math.min(1, fly * 10); g.position.x = (g.userData.x0 ??= g.position.x) + fly * 3; g.visible = fly < 0.8; } };
    return g;
  },

  // a pillow: a soft white cushion with a darker seam (o.w 0.5 x o.h 0.32, o.d 0.12 thick). Origin: its middle
  pillow(o) {
    const w = o.w ?? 0.5, h = o.h ?? 0.32, d = o.d ?? 0.12;
    return grp(at(box(w, h, d, o.color || '#F4F1E8', { outline: 0.012, taper: { x: 0.9, z: 0.8 } }), 0, 0, 0), at(box(w * 0.86, 0.012, d * 1.02, '#D9D4C4'), 0, 0, 0));
  },
};
