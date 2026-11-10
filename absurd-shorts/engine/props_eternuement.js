// « L'éternuement » (story 38): a sneeze measured, named, put on red alert, insured, and put to work.
// Every animated prop is a pure function of the shot time (userData.update(t)), so any frame renders alone.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, sphere, rng, ease, clamp01 } from './style.js';
import { grp, at, mesh, canvasPlane, glowSprite } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const txt = (g, s, x, y, px, color = '#1B1B1E', weight = '900') => { g.fillStyle = color; g.font = `${weight} ${px}px Arial`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(s, x, y); };
const fit = (g, s, w, px, weight = '900') => { g.font = `${weight} ${px}px Arial`; const m = g.measureText(s).width; return m > w ? px * w / m : px; };   // a font size that keeps the text inside w
// speed keys [[t, turns per second], ...] (linear between keys) -> turns done at time t
const turnsAt = (keys, t) => { let a = 0; for (let i = 0; i < keys.length; i++) { const [t0, v0] = keys[i], nx = keys[i + 1]; if (t <= t0) break; const t1 = nx ? Math.min(t, nx[0]) : t, v1 = nx ? v0 + (nx[1] - v0) * (t1 - t0) / Math.max(1e-6, nx[0] - t0) : v0; a += (v0 + v1) / 2 * (t1 - t0); } return a; };
const wob = (t, f = 30, d = 6) => (t <= 0 ? 0 : Math.sin(t * f) * Math.exp(-t * d));

export const ETERNUEMENT_PROPS = {
  // a hand anemometer: grip, mast, three cups on arms (origin at the grip, the rotor 0.34 m above). o.spin [[t, turns/s], ...]; the cups blur into a disc when fast
  anemometer(o) {
    const g = grp(at(cyl(0.022, 0.026, 0.16, '#2A2E35', 8), 0, 0, 0), at(cyl(0.012, 0.012, 0.26, '#C9CED3', 6), 0, 0.2, 0)), rotor = new THREE.Group(); rotor.position.y = 0.34; g.add(rotor);
    for (let i = 0; i < 3; i++) { const a = new THREE.Group(); a.rotation.y = i * TAU / 3; rotor.add(a); a.add(at(box(0.16, 0.012, 0.012, '#C9CED3'), 0.08, 0, 0), at(sphere(0.045, o.cups || '#C8202A', 1, { outline: 0.012 }), 0.17, 0, 0)); }   // o.cups: their colour (red ones vanish in front of a red sign)
    rotor.add(at(sphere(0.03, '#2A2E35', 1), 0, 0, 0));
    const disc = at(cyl(0.2, 0.2, 0.012, o.blur || '#E06A5A', 20), 0, 0, 0); disc.material = disc.material.clone(); disc.material.transparent = true; disc.material.opacity = 0; rotor.add(disc);
    const keys = o.spin || [[0, 0.6]];
    g.userData.update = t => { const k = keys.length; let v = keys[k - 1][1]; for (let i = 0; i < k - 1; i++) if (t < keys[i + 1][0]) { v = keys[i][1] + (keys[i + 1][1] - keys[i][1]) * clamp01((t - keys[i][0]) / (keys[i + 1][0] - keys[i][0])); break; }
      rotor.rotation.y = turnsAt(keys, t) * TAU; disc.material.opacity = clamp01((Math.abs(v) - 4) / 8) * 0.75; };
    g.userData.grip = [0, 0, 0]; return g;
  },

  // a round wind gauge that pops in: « km/h », a needle that slams to o.value (0..o.max) at o.at and trembles against the stop. Front +Z, origin at its centre
  windGauge(o) {
    const r = o.r ?? 0.5, max = o.max ?? 200, val = o.value ?? 200, a0 = 2.3, a1 = -2.3;   // needle angle at 0 and at max (radians from the top, + = left)
    const face = canvasPlane(2 * r, 2 * r, (g, W, H) => {
      g.clearRect(0, 0, W, H); g.fillStyle = '#F7F4EA'; g.beginPath(); g.arc(W / 2, H / 2, W * 0.48, 0, TAU); g.fill(); g.lineWidth = W * 0.035; g.strokeStyle = '#1B2A4A'; g.stroke();
      for (let i = 0; i <= 10; i++) { const a = a0 + (a1 - a0) * i / 10, c = Math.sin(a), s = Math.cos(a); g.strokeStyle = i >= 5 ? '#C8202A' : '#1B1B1E'; g.lineWidth = W * (i % 5 ? 0.012 : 0.022); g.beginPath(); g.moveTo(W / 2 - c * W * 0.445, H / 2 - s * W * 0.445); g.lineTo(W / 2 - c * W * 0.39, H / 2 - s * W * 0.39); g.stroke();
        if (i % 5 === 0) txt(g, String(max * i / 10), W / 2 - c * W * (i === 10 ? 0.3 : 0.31), H / 2 - s * W * (i === 10 ? 0.3 : 0.31), W * (i === 10 ? 0.125 : 0.085), i === 10 ? '#1B2A4A' : i >= 5 ? '#C8202A' : '#1B1B1E'); }   // the numbers sit outside the needle's reach; the last one, the one that is read out, bigger and in navy
      txt(g, 'km/h', W / 2, H * 0.74, W * 0.09, '#1B2A4A');
    }, { res: 512, transparent: true });
    const needle = new THREE.Group(); needle.add(at(box(0.04 * r * 2, r * 0.46, 0.012, '#C8202A'), 0, r * 0.2, 0), at(cyl(0.06 * r * 2, 0.06 * r * 2, 0.03, '#1B2A4A', 12), 0, 0, 0, PI / 2, 0, 0)); needle.position.z = 0.02;
    const g = grp(at(cyl(r * 1.02, r * 1.02, 0.03, '#1B2A4A', 28), 0, 0, -0.02, PI / 2, 0, 0), face, needle), at_ = o.at ?? 0.2, k = val / max;
    g.userData.update = t => { const u = t - at_, w = u < 0 ? 0 : ease.out(clamp01(u / 0.14)); needle.rotation.z = a0 + (a1 * k * 1.0 - a0) * w + (u > 0.14 ? 0.07 * Math.sin(t * 60) * Math.exp(-(u - 0.14) * 1.2) + 0.03 * Math.sin(t * 47) : 0); };
    g.userData.update(0); return g;
  },

  // the wind scale on the wall: three bands (BRISE, VENT, TEMPÊTE), a rider that climbs to the top band at o.at. Front +Z, origin at its centre
  windScale(o) {
    const w = o.w ?? 1.1, h = o.h ?? 1.5, rows = [['TEMPÊTE', '#C8202A', '> 100'], ['VENT', '#E8A33C', '50 - 100'], ['BRISE', '#5E9C6A', '0 - 50']], side = o.side ?? -1, x0 = side > 0 ? 0.06 : 0.2;   // o.side 1: the rider runs up the right-hand edge (under the finger of somebody who stands on that side)
    const face = canvasPlane(w, h, (g, W, H) => {
      g.fillStyle = '#F7F4EA'; g.fillRect(0, 0, W, H); g.fillStyle = '#1B2A4A'; g.fillRect(0, 0, W, H * 0.14); txt(g, 'ÉCHELLE DU VENT', W / 2, H * 0.072, fit(g, 'ÉCHELLE DU VENT', W * 0.9, H * 0.075), '#F7F4EA');
      rows.forEach(([nm, c, rg], i) => { const y = H * (0.17 + i * 0.275); g.fillStyle = c; g.fillRect(W * x0, y, W * 0.74, H * 0.25); txt(g, nm, W * (x0 + 0.37), y + H * 0.105, fit(g, nm, W * 0.66, H * 0.1), '#FFFFFF'); txt(g, rg + ' km/h', W * (x0 + 0.37), y + H * 0.195, H * 0.045, '#FFFFFF', 'bold'); });
      g.strokeStyle = '#1B2A4A'; g.lineWidth = W * 0.012; g.strokeRect(W * 0.006, W * 0.006, W * 0.988, H - W * 0.012);
    }, { res: 512 });
    const rider = grp(at(box(0.16 * w, 0.09 * h, 0.03, '#1B1B1E'), 0, 0, 0), at(box(0.09 * w, 0.09 * h, 0.03, '#1B1B1E'), 0.09 * w, 0, 0, 0, 0, PI / 4)); rider.position.set(side * 0.4 * w, 0, 0.03); rider.scale.x = -side;
    const g = grp(at(box(w, h, 0.03, '#F7F4EA', { outline: 0.006 }), 0, 0, -0.02), face, rider), yAt = i => h * (0.5 - (0.17 + i * 0.275 + 0.125)), at_ = o.at ?? 0.3;
    const mid = o.midAt;   // o.midAt: the rider first climbs to the middle band (VENT) at that time, then to the top at o.at
    g.userData.update = t => { const u = t - at_, k = u < 0 ? 0 : ease.out(clamp01(u / 0.22)), um = mid != null ? t - mid : -1, km = um < 0 ? 0 : ease.out(clamp01(um / 0.2)), y0 = yAt(2) + (yAt(1) - yAt(2)) * km;
      rider.position.y = y0 + (yAt(0) - y0) * k + (u > 0.22 ? 0.03 * h * wob(u - 0.22, 34, 7) : um > 0.2 && u < 0 ? 0.02 * h * wob(um - 0.2, 30, 8) : 0); };
    g.userData.update(0); return g;
  },

  // the list of first names for the storms: earlier names struck out, the next one framed in red at o.at. Front +Z, origin at its centre
  nameList(o) {
    const w = o.w ?? 0.9, h = o.h ?? 1.5, names = o.names || ['AMÉLIE', 'BENOÎT', 'CHANTAL', 'DIDIER', 'ÉLODIE', 'FERNAND', 'GISÈLE', 'HUBERT', 'IRÈNE'], next = o.next || 'JOSIANE', rowY = i => 0.2 + i * 0.076;
    const face = canvasPlane(w, h, (g, W, H) => {
      g.fillStyle = '#FBF8EE'; g.fillRect(0, 0, W, H); g.fillStyle = '#1B2A4A'; g.fillRect(0, 0, W, H * 0.13); txt(g, 'PRÉNOMS', W / 2, H * 0.068, H * 0.08, '#FBF8EE');
      names.forEach((n, i) => { const y = H * rowY(i); txt(g, n, W / 2, y, H * 0.05, '#8A8A90', 'bold'); g.strokeStyle = '#C8202A'; g.lineWidth = H * 0.007; g.beginPath(); g.moveTo(W * 0.22, y); g.lineTo(W * 0.78, y - H * 0.004); g.stroke(); });
      txt(g, next, W / 2, H * rowY(names.length), fit(g, next, W * 0.7, H * 0.075), '#1B1B1E');
      g.strokeStyle = '#1B2A4A'; g.lineWidth = W * 0.012; g.strokeRect(W * 0.006, W * 0.006, W * 0.988, H - W * 0.012);
    }, { res: 512 });
    const y = h * (0.5 - rowY(names.length)), fr = grp(at(box(w * 0.84, 0.012, 0.012, '#C8202A'), 0, h * 0.05, 0), at(box(w * 0.84, 0.012, 0.012, '#C8202A'), 0, -h * 0.05, 0), at(box(0.012, h * 0.1, 0.012, '#C8202A'), -w * 0.42, 0, 0), at(box(0.012, h * 0.1, 0.012, '#C8202A'), w * 0.42, 0, 0)); fr.position.set(0, y, 0.02);
    const sheet = grp(at(box(w, h, 0.02, '#FBF8EE', { outline: 0.006 }), 0, 0, -0.014), face, fr), g = grp(sheet), at_ = o.at ?? 0.4;
    // o.unroll [t0, dur]: a roller list: rolled up under its tube at the top until t0, then pulled down by its cord in dur seconds (it bounces at the bottom).
    // o.cordX: where the cord hangs (m from the middle); the knob's height above the origin is userData.handleY(t) (to guide a hand to it)
    let un = null;
    if (o.unroll) { const [t0, dur] = o.unroll, cx = o.cordX ?? w * 0.36, top = new THREE.Group(); top.position.y = h / 2; g.remove(sheet); sheet.position.y = -h / 2; top.add(sheet); g.add(top);
      const bar = at(box(w * 1.04, 0.05, 0.05, '#6B4A32', { outline: 0.006 }), 0, 0, 0.01), cord = at(cyl(0.006, 0.006, 0.14, '#3A3A40', 5), cx, -0.07, 0.03), knob = at(sphere(0.045, '#C8202A', 1, { outline: 0.008 }), cx, -0.16, 0.03), low = grp(bar, cord, knob); g.add(low);
      g.add(at(cyl(0.05, 0.05, w * 1.08, '#6B4A32', 10, { outline: 0.006 }), 0, h / 2 + 0.03, 0.02, 0, 0, PI / 2));   // the tube
      // o.roll [[t, k], ...]: after the first pull, the unrolled share k (0..1) follows these keys (a blind that snaps back up, is pulled down again)
      const rk = o.roll, kRoll = t => { for (let i = 0; i < rk.length - 1; i++) if (t < rk[i + 1][0]) return rk[i][1] + (rk[i + 1][1] - rk[i][1]) * ease.inOut(clamp01((t - rk[i][0]) / (rk[i + 1][0] - rk[i][0]))); return rk[rk.length - 1][1] * (1 + 0.03 * wob(t - rk[rk.length - 1][0], 30, 9)); };
      const kAt = t => { if (rk && t >= rk[0][0]) return Math.max(0.015, kRoll(t)); const u = (t - t0) / dur; return u <= 0 ? 0.015 : u >= 1 ? 1 + 0.035 * wob(t - t0 - dur, 30, 9) : 0.015 + 0.985 * ease.inOut(u); };
      un = t => { const k = kAt(t); top.scale.y = k; low.position.y = h / 2 - h * k; };
      g.userData.handleY = t => h / 2 - h * kAt(t) - 0.16; }
    g.userData.update = t => { const u = t - at_; fr.visible = u >= 0; const k = u < 0 ? 0 : ease.outBack(clamp01(u / 0.16)); fr.scale.set(1.5 - 0.5 * k, 1.5 - 0.5 * k, 1); un?.(t); };
    g.userData.update(0); return g;
  },

  // a name badge slapped on a chest: « TEMPÊTE » over a first name (front +Z, origin at its centre)
  nameBadge(o) {
    const w = o.w ?? 0.3, h = o.h ?? 0.2, name = o.name || 'JOSIANE';
    const face = canvasPlane(w, h, (g, W, H) => { g.fillStyle = '#FFFFFF'; g.fillRect(0, 0, W, H); g.fillStyle = '#C8202A'; g.fillRect(0, 0, W, H * 0.36); txt(g, 'TEMPÊTE', W / 2, H * 0.19, fit(g, 'TEMPÊTE', W * 0.86, H * 0.26), '#FFFFFF'); txt(g, name, W / 2, H * 0.68, fit(g, name, W * 0.88, H * 0.42), '#1B1B1E'); g.strokeStyle = '#1B1B1E'; g.lineWidth = W * 0.02; g.strokeRect(W * 0.01, W * 0.01, W * 0.98, H - W * 0.02); }, { res: 384 });
    return grp(at(box(w, h, 0.008, '#FFFFFF'), 0, 0, -0.005), face);
  },

  // the weather map on a screen: a blue country shape, a red spiral that turns over it with the storm's name, a red triangle « VIGILANCE ROUGE ». Front +Z
  stormMap(o) {
    const w = o.w ?? 1.5, h = o.h ?? 1.9, name = o.name || 'JOSIANE', bt = !!o.bandTop, dy = bt ? -0.1 : 0;
    const face = canvasPlane(w, h, (g, W, H) => {
      const y0 = bt ? 0.2 : 0.1, by = bt ? 0.1 : 0.86;   // o.bandTop: the red band under the title instead of at the foot (an arm that reaches the storm from below does not cross it)
      g.fillStyle = '#2E6FB5'; g.fillRect(0, 0, W, H); g.fillStyle = '#7FBF7A'; g.beginPath(); [[0.5, 0.16], [0.78, 0.25], [0.86, 0.45], [0.74, 0.72], [0.5, 0.8], [0.28, 0.72], [0.12, 0.5], [0.24, 0.3]].forEach(([x, y], i) => i ? g.lineTo(W * x, H * (y0 + y * 0.72)) : g.moveTo(W * x, H * (y0 + y * 0.72))); g.closePath(); g.fill(); g.strokeStyle = '#F7F4EA'; g.lineWidth = W * 0.012; g.stroke();
      g.fillStyle = '#C8202A'; g.fillRect(0, H * by, W, H * 0.14); txt(g, 'VIGILANCE ROUGE', W / 2, H * (by + 0.07), fit(g, 'VIGILANCE ROUGE', W * 0.9, H * 0.085), '#FFFFFF');
      g.fillStyle = '#1B2A4A'; g.fillRect(0, 0, W, H * 0.1); txt(g, 'MÉTÉO', W / 2, H * 0.052, H * 0.065, '#F7F4EA');
    }, { res: 512 });
    const sp = canvasPlane(0.62 * w, 0.62 * w, (g, W) => { g.clearRect(0, 0, W, W); g.strokeStyle = '#C8202A'; g.lineCap = 'round'; for (let k = 0; k < 2; k++) { g.lineWidth = W * 0.06; g.beginPath(); for (let a = 0; a < 7.2; a += 0.1) { const r = W * (0.05 + a * 0.058), x = W / 2 + Math.cos(a + k * PI) * r, y = W / 2 + Math.sin(a + k * PI) * r; a ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke(); } g.fillStyle = '#FFFFFF'; g.beginPath(); g.arc(W / 2, W / 2, W * 0.09, 0, TAU); g.fill(); }, { res: 384, transparent: true });
    sp.position.set(0.02 * w, (0.03 + dy) * h, 0.012);
    const tag = canvasPlane(0.62 * w, 0.14 * w, (g, W, H) => { g.fillStyle = '#FFFFFF'; g.fillRect(0, 0, W, H); g.strokeStyle = '#C8202A'; g.lineWidth = H * 0.12; g.strokeRect(H * 0.06, H * 0.06, W - H * 0.12, H * 0.88); txt(g, name, W / 2, H * 0.52, fit(g, name, W * 0.86, H * 0.66), '#C8202A'); }, { res: 384 }); tag.position.set(0.02 * w, (-0.2 + dy) * h, 0.03);
    const g = grp(at(box(w * 1.04, h * 1.03, 0.05, '#23262C', { outline: 0.008 }), 0, 0, -0.03), face, sp, tag);
    g.userData.update = t => { sp.rotation.z = -t * 3.2; tag.scale.setScalar(1 + 0.04 * Math.sin(t * 9)); if (o.tapAt != null) { const taps = [].concat(o.tapAt); let sh = 0, amp = o.tapAmp ?? 0.035, rest = 0; taps.forEach((ta, i) => { if (t >= ta) { sh = wob(t - ta, o.tapFreq ?? 46, o.tapDecay ?? 9); amp = o.tapAmps?.[i] ?? (o.tapAmp ?? 0.035); if (i === taps.length - 1 && o.crooked) rest = o.crooked * (1 - Math.exp(-(t - ta) * 9)); } });
        const a = amp * sh + rest; g.rotation.z = a; g.userData.x0 ??= g.position.x; g.userData.y0 ??= g.position.y;
        if (o.pivotTop) { g.position.x = g.userData.x0 + h / 2 * Math.sin(a); g.position.y = g.userData.y0 - h / 2 * (1 - Math.cos(a)); } else g.position.x = g.userData.x0 + 0.3 * amp * sh;
        tag.scale.multiplyScalar(1 + 0.25 * Math.min(1, Math.abs(sh))); } };
    // o.tapAt (a time or several): it swings when it is tapped: o.tapAmp rad, or o.tapAmps [per tap]; o.tapFreq / o.tapDecay (46 rad/s, 9: a shiver; 13 and 3: a pendulum);
    // o.pivotTop: it swings from its top edge (it hangs on a nail); o.crooked (rad): the last tap leaves it hanging askew
    return g;
  },

  // a triangular road sign carried on a pole: « VIGILANCE ROUGE » (o.text), the triangle red. Origin at the foot of the pole
  alertSign(o) {
    const h = o.h ?? 2.3, s = o.s ?? 0.7, text = o.text || '!';
    const tri = canvasPlane(s, s * 0.9, (g, W, H) => { g.clearRect(0, 0, W, H); g.fillStyle = '#C8202A'; g.beginPath(); g.moveTo(W / 2, H * 0.04); g.lineTo(W * 0.98, H * 0.96); g.lineTo(W * 0.02, H * 0.96); g.closePath(); g.fill(); g.fillStyle = '#FFFFFF'; g.beginPath(); g.moveTo(W / 2, H * 0.26); g.lineTo(W * 0.8, H * 0.85); g.lineTo(W * 0.2, H * 0.85); g.closePath(); g.fill(); txt(g, text, W / 2, H * 0.66, H * 0.42, '#1B1B1E'); }, { res: 384, transparent: true });
    tri.position.set(0, h - s * 0.45, 0.02);
    const g = grp(at(cyl(0.025, 0.025, h, '#8A9097', 6), 0, h / 2, 0), tri); g.userData.grip = [0, h * 0.42, 0]; return g;
  },

  // a rotating red beacon (on a hat, a pole, a roof): the dome turns and pulses. Origin at its base
  beacon(o) {
    const r = o.r ?? 0.09, dome = sphere(r, '#E8322A', 1); dome.material = dome.material.clone(); dome.material.emissive = new THREE.Color('#FF3B2A'); dome.position.y = r * 0.9;
    const g = grp(at(cyl(r * 1.1, r * 1.25, r * 0.5, '#2A2E35', 10), 0, r * 0.25, 0), dome, at(box(r * 2.6, r * 0.5, r * 0.3, '#FFD9A0'), 0, r * 0.9, 0));
    const bar = g.children[2]; bar.material = bar.material.clone(); bar.material.transparent = true; bar.material.opacity = 0.55;
    let hub = null;
    if (o.beams) {   // o.beams (m): two red beams that turn with it, like a lighthouse: the red alert sweeps the street and whoever stands in it
      const L = o.beams; hub = new THREE.Group(); hub.position.y = r * 0.9; g.add(hub);
      for (const sd of [1, -1]) { const c = cyl(r * 0.35, L * (o.beamWidth ?? 0.15), L, '#FF4A36', 12); c.material = c.material.clone(); c.material.transparent = true; c.material.opacity = o.beamOpacity ?? 0.3; c.material.depthWrite = false; c.material.emissive = new THREE.Color('#FF3B2A'); c.material.emissiveIntensity = 0.9;
        c.castShadow = false; c.receiveShadow = false; c.rotation.z = sd * PI / 2; c.position.x = sd * L / 2; const pv = new THREE.Group(); pv.rotation.z = sd * (o.beamTilt ?? 0); pv.add(c); hub.add(pv); }   // o.beamTilt (rad): the beams point up a little: when one sweeps toward the camera it passes over the head, not over the face
    }
    g.userData.update = t => { bar.rotation.y = t * 9; if (hub) hub.rotation.y = t * (o.turn ?? 9); dome.material.emissiveIntensity = 0.55 + 0.45 * Math.sin(t * 9); };
    return g;
  },

  // a low wall of sandbags (o.n bags per row, o.rows), along X, origin at the middle of its foot
  sandbags(o) {   // a low wall of sandbags: sagging jute sacks in staggered courses, each with its seam and its tied ear (o.n per course, o.rows courses); along X, origin at the foot
    const n = o.n ?? 5, rows = o.rows ?? 3, r = rng(o.seed ?? 4), g = new THREE.Group(), cols = ['#B89A66', '#C4A774', '#AD8F5C'];
    for (let j = 0; j < rows; j++) for (let i = 0; i < n - (j % 2); i++) { const c = cols[Math.floor(r() * 3)], k = new THREE.Group(), body = sphere(1, c, 1, { outline: 0.02 }); body.scale.set(0.275, 0.115 - 0.012 * (rows - 1 - j), 0.17);   // the lower ones are squashed by those above
      k.add(body, at(box(0.5, 0.008, 0.012, '#7A6238'), 0, 0.085, 0), at(box(0.07, 0.07, 0.12, c, { outline: 0.006, taper: { x: 0.5, z: 0.7 } }), 0.29, 0.015, 0, 0, 0, -0.5), at(box(0.014, 0.075, 0.125, '#5A4628'), 0.262, 0.012, 0, 0, 0, -0.5));
      k.position.set((i - (n - 1 - (j % 2)) / 2) * 0.52 + (r() - 0.5) * 0.04, 0.105 + j * 0.175, (r() - 0.5) * 0.06); k.rotation.set((r() - 0.5) * 0.12, (r() - 0.5) * 0.3 + (r() < 0.5 ? PI : 0), (r() - 0.5) * 0.1); g.add(k); }
    return g;
  },

  // a very big rubber stamp held by its knob (origin at the knob, the face 0.42 m below); o.color
  bigStamp(o) {
    const g = grp(at(sphere(0.07, '#5A3A28', 1), 0, 0, 0), at(cyl(0.035, 0.05, 0.2, '#6B4A32', 8), 0, -0.13, 0), at(box(0.34, 0.1, 0.24, '#3A2A20', { outline: 0.008 }), 0, -0.3, 0), at(box(0.32, 0.03, 0.22, o.color || '#C8202A'), 0, -0.365, 0));
    g.userData.grip = [0, 0, 0]; return g;
  },
  // what the stamp leaves: a red mark « CAT. NAT. » (o.text) on a transparent plane (stick it on a forehead, a sheet). Front +Z
  stampMark(o) {
    const w = o.w ?? 0.2, h = o.h ?? 0.11, text = o.text || 'CAT. NAT.';
    return canvasPlane(w, h, (g, W, H) => { g.clearRect(0, 0, W, H); g.strokeStyle = '#C8202A'; g.lineWidth = H * 0.1; g.strokeRect(H * 0.08, H * 0.08, W - H * 0.16, H * 0.84); txt(g, text, W / 2, H * 0.53, fit(g, text, W * 0.84, H * 0.56), '#C8202A'); }, { res: 384, transparent: true });
  },
  // the certificate on the insurer's wall: « CATASTROPHE NATURELLE » with a seal and a photo frame. Front +Z
  catNatDiploma(o) {
    const w = o.w ?? 1.0, h = o.h ?? 0.72;
    const face = canvasPlane(w, h, (g, W, H) => { g.fillStyle = '#FBF8EE'; g.fillRect(0, 0, W, H); g.strokeStyle = '#B08A3C'; g.lineWidth = W * 0.02; g.strokeRect(W * 0.03, W * 0.03, W * 0.94, H - W * 0.06); txt(g, 'CATASTROPHE', W / 2, H * 0.3, fit(g, 'CATASTROPHE', W * 0.8, H * 0.2), '#C8202A'); txt(g, 'NATURELLE', W / 2, H * 0.52, fit(g, 'NATURELLE', W * 0.8, H * 0.2), '#C8202A'); g.fillStyle = '#6A6A70'; for (let i = 0; i < 2; i++) g.fillRect(W * 0.22, H * (0.68 + i * 0.07), W * 0.4, H * 0.02); g.fillStyle = '#C8202A'; g.beginPath(); g.arc(W * 0.8, H * 0.75, H * 0.1, 0, TAU); g.fill(); }, { res: 512 });
    return grp(at(box(w * 1.06, h * 1.08, 0.04, '#5A3A28', { outline: 0.006 }), 0, 0, -0.025), face);
  },

  // a fishing rod with a pepper pot on its line (origin at the grip; the rod points along +Z and up); o.swing: the pot swings
  pepperRod(o) {
    const L = o.len ?? 1.9, tip = [0, L * 0.5, L * 0.86], g = grp(at(cyl(0.02, 0.012, L, '#6B4A32', 6), 0, tip[1] / 2, tip[2] / 2, Math.atan2(tip[2], tip[1]), 0, 0)), line = new THREE.Group(); line.position.set(...tip); g.add(line);
    const drop = o.drop ?? 0.7, k = o.pot ?? 1, pot = new THREE.Group(); pot.position.y = -drop; pot.rotation.y = o.potRy ?? 0; line.add(at(cyl(0.004, 0.004, drop, '#EDEDED', 4), 0, -drop / 2, 0), pot);   // o.pot: its size (1.6 reads at phone size); o.potRy: turns its label to the camera
    pot.add(at(cyl(0.05 * k, 0.06 * k, 0.13 * k, '#F4F1E8', 12, { outline: 0.008 }), 0, -0.06 * k, 0), at(cyl(0.052 * k, 0.04 * k, 0.035 * k, '#8A9097', 12), 0, 0.02 * k, 0));
    for (const sd of (o.back === false ? [1] : [1, -1])) { const lb = canvasPlane(0.105 * k, 0.07 * k, (c, W, H) => { c.fillStyle = '#1B1B1E'; c.fillRect(0, 0, W, H); txt(c, 'POIVRE', W / 2, H * 0.54, fit(c, 'POIVRE', W * 0.88, H * 0.62), '#F4F1E8'); }, { res: 256 }); lb.position.set(0, -0.06 * k, sd * 0.0585 * k); if (sd < 0) lb.rotation.y = PI; pot.add(lb); }
    const sp = []; if (o.specks !== false) { const q = rng(8); for (let i = 0; i < 14; i++) { const m = box(0.012 * k, 0.012 * k, 0.012 * k, '#2A2420'); m.castShadow = false; pot.add(m); sp.push([m, q(), (q() - 0.5) * 0.16 * k, (q() - 0.5) * 0.16 * k]); } }   // pepper falls out of it
    g.userData.update = t => { line.rotation.x = (o.swing ?? 0.25) * Math.sin(t * 3.1); line.rotation.z = 0.5 * (o.swing ?? 0.25) * Math.sin(t * 2.3 + 1);
      for (const [m, ph, x, z] of sp) { const u = (t * 1.3 + ph) % 1; m.position.set(x * (0.3 + u), -0.13 * k - 0.45 * u * u, z * (0.3 + u)); m.visible = u < 0.9; } };
    g.userData.grip = [0, 0, 0]; return g;
  },

  // a wall of mattresses to stop a recoil (o.n side by side, standing), along X, origin at the middle of its foot; it bulges at o.hitAt
  mattressWall(o) {
    const n = o.n ?? 3, H = o.h ?? 1.95, g = new THREE.Group(), ms = [], NS = 10, hs = H / NS;   // o.h: their height (1.95 standing; 1.2 lets a camera behind the wall see who stands in front of it)
    // each mattress is a stack of slices so that it can bow: white ticking with blue stripes on both faces, quilt buttons, the top and the foot rounded off
    for (let i = 0; i < n; i++) { const m = new THREE.Group(); m.position.x = (i - (n - 1) / 2) * 0.98; const sl = [];
      for (let k = 0; k < NS; k++) { const end = k === 0 || k === NS - 1, b = box(0.95, hs * 1.1, 0.24, '#F4F1EA', { taper: end ? { x: 0.93, z: 0.78 } : undefined }); if (k === 0) b.rotation.x = PI; b.position.y = (k + 0.5) * hs; m.add(b); sl.push(b);   // no outline on a slice: ten outlined slices read as a pile of boxes
        for (const sd of [1, -1]) { for (let q = 0; q < 6; q++) b.add(at(box(0.035, hs * (end ? 0.8 : 1.1), 0.006, '#5F86C4'), (q - 2.5) * 0.15, 0, sd * (end ? 0.105 : 0.122) * (k === 0 ? -1 : 1)));
          if (k % 3 === 1) for (const x of [-0.24, 0.24]) b.add(at(cyl(0.028, 0.028, 0.012, '#3C5F9E', 8), x, 0, sd * 0.126, PI / 2, 0, 0)); } }
      g.add(m); ms.push([m, sl]); }
    // o.hitAt: somebody is thrown into it from the -Z side (o.hitDir -1: from +Z): it bows deep in two frames, springs back past straight, settles
    g.userData.update = t => { const u = t - (o.hitAt ?? 1e9), hold = o.hold ?? 0, v = Math.max(0, u - hold), d = u < 0 ? 0 : (o.dent ?? 0.34) * Math.min(1, u / 0.08) * Math.exp(-v * 4.5) * Math.cos(v * 15) * (o.hitDir ?? 1);   // o.hold (s): it stays bowed that long before it springs back
      ms.forEach(([m, sl], i) => { const kk = i === Math.floor(n / 2) ? 1 : 0.45; sl.forEach((b, k) => { const v = (k + 0.5) / NS, bow = Math.sin(v * PI); b.position.z = d * kk * bow; b.rotation.x = (k === 0 ? PI : 0) + Math.atan(d * kk * PI * Math.cos(v * PI) / H); }); }); };   // each slice follows the slope of the bow
    g.userData.update(0); return g;
  },

  // three towns on a far ridge at dusk: clusters of dark houses whose windows light up one town after the other (o.at [t1, t2, t3]); along X, origin at the foot
  townLights(o) {
    const g = new THREE.Group(), r = rng(o.seed ?? 6), ats = o.at || [0.4, 0.6, 0.8], spread = o.spread ?? 9, depth = o.depth ?? [0, 0, 0], nh = o.houses ?? 9, wins = [[], [], []];   // o.depth [z1, z2, z3]: how far back each town sits; o.houses: per town (6 with o.spread 11 leaves a gap of dark hill between them)
    for (let k = 0; k < 3; k++) { const cx = o.sites ? o.sites[k][0] : (k - 1) * spread, cz = o.sites ? o.sites[k][1] : -depth[k];   // o.sites [[x, z] x 3]: where each town stands (in the prop's frame), instead of o.spread / o.depth
      for (let i = 0; i < nh; i++) { const mid = i === Math.floor(nh / 2), lm = o.landmarks ? k : 0, w = mid ? [0.8, 1.9, 0.34][lm] : 0.9 + r() * 1.3, h = mid ? [4.4 + k * 0.4, 2.5, 3.5][lm] : 1.0 + r() * 2.6, x = cx + (i - (nh - 1) / 2) * 0.95 + (r() - 0.5) * 0.3, b = at(box(w, h, 0.9, ['#2B3248', '#353C55', '#3E3A52'][i % 3], { pivot: 'bottom' }), x, 0, cz + (r() - 0.5) * 0.8); b.castShadow = false; g.add(b);
        if (mid && lm === 0) g.add(at(box(0.95, 1.5, 0.95, '#4A3A44', { pivot: 'bottom', taper: { x: 0.05, z: 0.05 } }), x, h, b.position.z));   // a steeple: one town, one steeple
        else if (mid && lm === 1) { const dm = sphere(0.86, '#4A3A44', 1); dm.scale.y = 0.95; dm.castShadow = false; g.add(at(dm, x, h, b.position.z), at(box(0.22, 0.5, 0.22, '#4A3A44', { pivot: 'bottom', taper: { x: 0.4, z: 0.4 } }), x, h + 0.78, b.position.z)); }   // a dome and its lantern
        else if (mid && lm === 2) g.add(at(cyl(0.85, 0.7, 1.05, '#3E3A52', 10), x, h + 0.5, b.position.z), at(cyl(0.1, 0.9, 0.4, '#4A3A44', 10), x, h + 1.22, b.position.z));   // a water tower: a tank on a stem
        else if (i % 3 === 1) g.add(at(box(w * 1.05, 0.5, 0.95, '#4A3A44', { pivot: 'bottom', taper: { x: 0.2, z: 1 } }), x, h, b.position.z));
        for (let a = 0; a < Math.floor(h / 0.5); a++) for (let c = 0; c < 2; c++) { if (r() < 0.25) continue; const wn = at(box(0.2, 0.24, 0.02, '#FFD76A'), x + (c - 0.5) * w * 0.45, 0.4 + a * 0.5, b.position.z + 0.46); wn.material = wn.material.clone(); wn.material.emissive = new THREE.Color('#FFC94A'); wn.castShadow = false; g.add(wn); wins[k].push([wn, r()]); } } }
    // o.landmarks: the tall building of each town is its own (a belfry, a dome, a water tower): three towns, not one town three times
    // o.pop: a town comes on all at once (its windows within a frame) under a warm glow (o.glow: its size in metres, o.glowK: its strength, 0.5), instead of window by window
    const glows = o.pop ? [0, 1, 2].map(k => { const cx = o.sites ? o.sites[k][0] : (k - 1) * spread, cz = o.sites ? o.sites[k][1] : -depth[k], sp = glowSprite('#FFC24A', (o.glow ?? 9), 0.0); sp.position.set(cx, 2.2, cz + 0.6); g.add(sp); return sp; }) : null;
    g.userData.update = t => { wins.forEach((ws, k) => ws.forEach(([m, ph]) => { const u = t - ats[k] - ph * (o.pop ? 0.035 : 0.22), on = u > 0; m.material.emissiveIntensity = on ? 1.4 + 0.5 * Math.exp(-u * 8) : 0; m.material.color.set(on ? '#FFD76A' : '#1E2233'); }));
      if (glows) glows.forEach((sp, k) => { const u = t - ats[k]; sp.material.opacity = u > 0 ? (o.glowK ?? 0.5) * Math.min(1, u / 0.05) * (1 + 0.5 * Math.exp(-u * 9)) : 0; sp.scale.setScalar((o.glow ?? 9) * (u > 0 ? 1 + 0.25 * Math.exp(-u * 9) : 1)); }); };
    g.userData.update(0); return g;
  },

  // a meadow in flower: o.n low-poly flowers (a stem and a head: white, yellow, poppy red, pink) over o.w x o.d metres, denser toward +Z when o.near (0..1), none
  // within o.clear [x, z, r] (where somebody stands); o.h: their height, o.head: the radius of a head. They sway (o.sway rad) and can all lean toward a point
  // (o.toward [x, z], in the prop's frame) by the angles of o.pull [[t, rad], ...], stretching as they lean: a breath that draws the whole field in. Origin
  // at the middle of the field
  flowerMeadow(o) {
    const w = o.w ?? 14, d = o.d ?? 14, n = o.n ?? 240, r = rng(o.seed ?? 21), g = new THREE.Group(), cols = o.colors || ['#FFFFFF', '#F6D23A', '#E8453C', '#F29CC0', '#FFFFFF', '#F6D23A'], near = o.near ?? 0.6, cl = o.clear, sway = o.sway ?? 0.06;
    const stemG = new THREE.CylinderGeometry(0.007, 0.011, 1, 4); stemG.translate(0, 0.5, 0);
    const headG = new THREE.IcosahedronGeometry(1, 0); headG.scale(1, 0.62, 1);
    const fl = [];
    for (let i = 0; i < n; i++) { const x = (r() - 0.5) * w, z = (Math.pow(r(), 1 / (1 + 2 * near)) - 0.5) * d, f = { x, z, h: (o.h ?? 0.32) * (0.6 + 0.8 * r()), s: (o.head ?? 0.07) * (0.7 + 0.6 * r()), c: Math.floor(r() * cols.length), ph: r() * TAU, a: r() * TAU };
      if (!(cl && Math.hypot(x - cl[0], z - cl[1]) < cl[2])) fl.push(f); }
    const stems = new THREE.InstancedMesh(stemG, mat('#4E8A3E'), fl.length), heads = cols.map((c, ci) => new THREE.InstancedMesh(headG, mat(c), Math.max(1, fl.filter(f => f.c === ci).length)));
    stems.castShadow = false; heads.forEach(h => { h.castShadow = false; }); g.add(stems, ...heads);
    const M = new THREE.Matrix4(), q = new THREE.Quaternion(), ax = new THREE.Vector3(), P_ = new THREE.Vector3(), Sc = new THREE.Vector3(), pk = o.pull, tw = o.toward;
    const pull = t => { if (!pk) return 0; if (t <= pk[0][0]) return pk[0][1]; for (let i = 0; i < pk.length - 1; i++) if (t < pk[i + 1][0]) return pk[i][1] + (pk[i + 1][1] - pk[i][1]) * ease.out((t - pk[i][0]) / (pk[i + 1][0] - pk[i][0])); return pk[pk.length - 1][1]; };
    g.userData.update = t => { const pl = pull(t), cnt = cols.map(() => 0);
      fl.forEach((f, i) => { const sw = sway * Math.sin(t * 1.7 + f.ph); let lx = sw * Math.cos(f.a), lz = sw * Math.sin(f.a);
        if (pl && tw) { const dx = tw[0] - f.x, dz = tw[1] - f.z, dd = Math.hypot(dx, dz) || 1, k = pl * (1 + 0.15 * Math.sin(t * 23 + f.ph)); lx += dx / dd * k; lz += dz / dd * k; }
        const a = Math.hypot(lx, lz), dxn = a ? lx / a : 1, dzn = a ? lz / a : 0, hh = f.h * (1 + 0.5 * pl); ax.set(dzn, 0, -dxn); q.setFromAxisAngle(ax, a);
        Sc.set(1, hh, 1); P_.set(f.x, 0, f.z); M.compose(P_, q, Sc); stems.setMatrixAt(i, M);
        P_.set(f.x + dxn * Math.sin(a) * hh, Math.cos(a) * hh, f.z + dzn * Math.sin(a) * hh); Sc.set(f.s, f.s, f.s); M.compose(P_, q, Sc); heads[f.c].setMatrixAt(cnt[f.c]++, M); });
      stems.instanceMatrix.needsUpdate = true; heads.forEach((h, ci) => { h.count = cnt[ci]; h.instanceMatrix.needsUpdate = true; }); };
    g.userData.update(0); return g;
  },

  // a grain of pollen seen very close: a yellow spiky ball that drifts and turns (origin at its centre); o.r
  pollenGrain(o) {
    const r = o.r ?? 0.05, core = sphere(r, o.color || '#FFF06A', 1, { outline: r * 0.34 }), g = grp(core), q = rng(3);   // pale lemon in a dark outline: on a skin its own hue it did not show
    for (let i = 0; i < 14; i++) { const a = q() * TAU, b = Math.acos(2 * q() - 1), s = at(cyl(r * 0.05, r * 0.16, r * 0.7, '#C98A1E', 5), Math.sin(b) * Math.cos(a) * r * 1.2, Math.cos(b) * r * 1.2, Math.sin(b) * Math.sin(a) * r * 1.2); s.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), s.position.clone().normalize()); g.add(s); }
    g.userData.update = t => { g.rotation.set(t * 1.7, t * 1.1, 0); };
    return g;
  },
  // a cloud of pollen that drifts with the wind: o.n grains in a box o.size [x, y, z], moving along o.dir (m/s), each bobbing; origin at the centre of the box at t = 0
  pollenCloud(o) {
    const n = o.n ?? 60, [sx, sy, sz] = o.size || [4, 2, 2], dir = o.dir || [-0.8, -0.1, 0], r = rng(o.seed ?? 9), g = new THREE.Group(), gs = [];
    for (let i = 0; i < n; i++) { const m = sphere(0.03 + r() * 0.035, i % 3 ? '#F2C230' : '#F6DD7A', 1); m.castShadow = false; const p = [(r() - 0.5) * sx, (r() - 0.5) * sy, (r() - 0.5) * sz]; g.add(m); gs.push([m, p, r() * TAU, 0.6 + r() * 0.8]); }
    g.userData.update = t => gs.forEach(([m, p, ph, k]) => m.position.set(p[0] + dir[0] * t * k + 0.12 * Math.sin(t * 1.9 + ph), p[1] + dir[1] * t * k + 0.1 * Math.sin(t * 2.6 + ph * 1.7), p[2] + dir[2] * t * k));
    g.userData.update(0); return g;
  },

  // the blast of a sneeze: white streaks and puffs that shoot along +Z from the origin between o.at and o.at + o.dur (o.len m long, o.spread wide)
  sneezeBlast(o) {
    const n = o.n ?? 26, len = o.len ?? 9, spread = o.spread ?? 1.4, at_ = o.at ?? 0, dur = o.dur ?? 0.4, r = rng(o.seed ?? 12), g = new THREE.Group(), ss = [];
    for (let i = 0; i < n; i++) { const puff = i % 4 === 0, m = puff ? sphere((0.16 + r() * 0.2) * (o.puff ?? 1), '#FFFFFF', 1) : box(0.03 + r() * 0.03, 0.03 + r() * 0.03, 0.7 + r() * 1.3, '#FFFFFF'); m.material = m.material.clone(); m.material.transparent = true; m.castShadow = false; g.add(m); ss.push([m, (r() - 0.5) * spread, 1.55 + (r() - 0.5) * spread * 0.8, r() * 0.35, 0.7 + r() * 0.6, puff]); }
    g.userData.update = t => ss.forEach(([m, x, y, d, k, puff]) => { const u = (t - at_ - d * dur) / (dur * 0.75), on = u > 0 && u < 1; m.visible = on; if (!on) return; const z = 0.4 + len * k * ease.out(u), w = 1 + 1.4 * u; m.position.set(x * w, y + (y - 1.55) * 0.8 * u, z); m.material.opacity = (puff ? 0.55 : 0.9) * (1 - u * u); if (puff) m.scale.setScalar(1 + 1.6 * u); });
    g.userData.update(-1); return g;
  },

  // a street advertising panel on two legs, a hairdresser's poster on it (o.title / o.sub / o.price); front +Z, origin at the foot, the board from o.y0 (0.5) up
  adPanel(o) {
    const w = o.w ?? 2.8, h = o.h ?? 2.3, y0 = o.y0 ?? 0.5;
    const th = o.textH ?? 1;   // o.textH (0..1): all the text in that share of the board, at the top (what is pinned on the board below leaves it readable)
    const face = canvasPlane(w, h, (g, W, H0) => { const H = H0 * th; g.fillStyle = o.bg || '#F6D7E0'; g.fillRect(0, 0, W, H0); g.fillStyle = o.band || '#C8457A'; g.fillRect(0, 0, W, H * (th < 1 ? 0.4 : 0.24)); txt(g, o.title || 'COIFFURE', W / 2, H * (th < 1 ? 0.21 : 0.125), fit(g, o.title || 'COIFFURE', W * 0.9, H * (th < 1 ? 0.3 : 0.17)), '#FFFFFF');
      if (th < 1) { txt(g, o.sub || 'BRUSHING', W / 2, H * 0.57, fit(g, o.sub || 'BRUSHING', W * 0.8, H * 0.24), '#1B2A4A'); txt(g, o.price || 'TENUE GARANTIE', W / 2, H * 0.84, fit(g, o.price || 'TENUE GARANTIE', W * 0.8, H * 0.2), '#C8457A', 'bold'); }
      else { txt(g, o.sub || 'BRUSHING', W / 2, H * 0.47, fit(g, o.sub || 'BRUSHING', W * 0.86, H * 0.2), '#1B2A4A'); txt(g, o.price || 'TENUE GARANTIE', W / 2, H * 0.72, fit(g, o.price || 'TENUE GARANTIE', W * 0.8, H * 0.11), '#C8457A', 'bold'); }
      g.strokeStyle = '#1B2A4A'; g.lineWidth = W * 0.012; g.strokeRect(W * 0.006, W * 0.006, W * 0.988, H0 - W * 0.012); }, { res: 768 });
    face.position.set(0, y0 + h / 2, 0.045);
    return grp(at(box(w * 1.04, h * 1.04, 0.08, '#2A2E35', { outline: 0.008 }), 0, y0 + h / 2, 0), face, at(box(0.1, y0 + 0.1, 0.1, '#2A2E35'), -w * 0.36, (y0 + 0.1) / 2, 0), at(box(0.1, y0 + 0.1, 0.1, '#2A2E35'), w * 0.36, (y0 + 0.1) / 2, 0));
  },
  // a hand that points, seen close (a cuff, a fist, the index out): the finger along -X... it points to its left; origin at the fingertip. o.skin, o.sleeve
  pointerHand(o) {
    const skin = o.skin || '#E0B48A', g = grp(at(box(0.11, 0.022, 0.03, skin), 0.055, 0, 0), at(box(0.1, 0.1, 0.05, skin), 0.16, -0.035, 0), at(box(0.035, 0.07, 0.035, skin), 0.14, 0.03, 0.01, 0, 0, 0.5),
      at(box(0.07, 0.115, 0.06, '#F4F1E8'), 0.245, -0.035, 0), at(box(0.3, 0.13, 0.07, o.sleeve || '#1E2E44'), 0.43, -0.035, 0));
    return g;
  },
  // a wig that has left its head (a curly mop; origin at its base): it tumbles when moved by the story
  wig(o) { const c = o.color || '#6A4024', hi = o.light || '#8A5A34', w = o.w ?? 0.34, curl = (x, y, z, len, ax) => at(cyl(0.035, 0.035, len, c, 8, { outline: 0.006 }), x, y, z, ax === 'x' ? 0 : PI / 2, 0, ax === 'x' ? PI / 2 : 0);
    // a bob wig that has lost its head: a rounded cap with a parting, a curled fringe on the brow, sides and back down to the jaw with tips that flip
    // outward, three loose strands trailing (origin: the top of the head it left; o.w: as wide as that head)
    const cap = sphere(1, c, 1, { outline: 0.03 }); cap.scale.set(w * 0.56, 0.11, 0.16); cap.position.set(0, 0.035, 0);
    const g = grp(cap, at(box(0.014, 0.012, 0.26, hi), w * 0.12, 0.138, 0, 0, 0.12, 0),   // the parting
      at(box(w * 1.04, 0.44, 0.06, c, { pivot: 'top', outline: 0.008, taper: { x: 0.9, z: 1 } }), 0, 0.06, -0.125), at(box(0.06, 0.36, 0.2, c, { pivot: 'top', outline: 0.006 }), -w / 2 - 0.005, 0.06, -0.02), at(box(0.06, 0.36, 0.2, c, { pivot: 'top', outline: 0.006 }), w / 2 + 0.005, 0.06, -0.02),
      curl(0, 0.02, 0.135, w * 0.92, 'x'), curl(-w * 0.2, 0.05, 0.15, w * 0.3, 'x'),   // the fringe: a roll on the brow and a curl over it
      curl(-w / 2 - 0.03, -0.31, -0.02, 0.2, 'z'), curl(w / 2 + 0.03, -0.31, -0.02, 0.2, 'z'), curl(0, -0.39, -0.16, w * 1.0, 'x'),   // the tips flip outward
      at(box(0.03, 0.3, 0.03, c, { pivot: 'top' }), -w * 0.3, -0.42, -0.15, -0.5, 0, 0.2), at(box(0.03, 0.36, 0.03, c, { pivot: 'top' }), 0, -0.42, -0.15, -0.6, 0, 0), at(box(0.03, 0.28, 0.03, c, { pivot: 'top' }), w * 0.3, -0.42, -0.15, -0.45, 0, -0.2)); return g; },
  // a sheet of newspaper carried by the wind: it flaps (two halves hinged), origin at the fold
  flyingPaper(o) {
    const half = s => { const m = canvasPlane(0.28, 0.4, (g, W, H) => { g.fillStyle = '#F4F1E8'; g.fillRect(0, 0, W, H); g.fillStyle = '#1B1B1E'; g.fillRect(W * 0.08, H * 0.06, W * 0.84, H * 0.1); g.fillStyle = '#8A8A90'; for (let i = 0; i < 9; i++) g.fillRect(W * 0.08, H * (0.22 + i * 0.08), W * (0.84 - (i % 3) * 0.2), H * 0.03); }, { res: 256 }); m.position.x = s * 0.14; const k = new THREE.Group(); k.add(m); return k; };
    const a = half(-1), b = half(1), g = grp(a, b); g.userData.update = t => { const f = 0.7 * Math.sin(t * 16); a.rotation.y = 0.5 + f; b.rotation.y = -0.5 - f; }; return g;
  },
};
