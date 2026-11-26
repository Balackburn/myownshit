// « La minuterie » (story 113, cycle 59): this man lives on the seventh floor and the stairwell's light timer lasts thirty seconds: he never gets
// home before the dark. He hires a coach, until the evening he has light all the way to his door. The landlord finds that too long and sets fifteen
// seconds; he keeps up, five steps a stride. Champions come to train in his stairwell and the landlord charges at the door; a short timer is a gym
// at home, rents double, every landlord in the country shortens his; grandparents move into the hall, removal men run pianos up the stairs and win
// the world stair championship. His timer now lasts one second. Yesterday he twisted his ankle on the third floor and sat in the dark: above his
// head there was a button. There is one on every floor.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
// Running gag drawn here: a glowing orange timer button on every landing (mnButtons, on the newel column at the well's end, facing the front), which
// the old neighbour presses on every landing and the hero never sees. Floors are counted by landings and by rows of painted dots, never by a number.
// The stairwell (mnStairwell) is a cutaway: the front (+Z) open unless o.front; its geometry is shared with the script (story_minuterie.py):
//   floor height 2.8; floor landing k at y 2.8 k, x 1.4 .. 3.8 (the ground floor hall runs on to x 7.0); half landing k at y 2.8 k + 1.4, x -2.8 .. -1.4;
//   flight A_k (front, z 0.45 .. 1.5) climbs from the floor landing (x 1.4) to the half landing (x -1.4), flight B_k (back, z -1.5 .. -0.45) from the half
//   landing to floor landing k + 1; 8 risers of 0.175, treads of 0.35; the well z -0.45 .. 0.45; the newel column x 1.12 .. 1.4, z -0.14 .. 0.14 (its
//   front face carries the buttons at 1.8 above each landing); the back wall's face at z -1.5; each floor's door at x 2.9; the front door of the hall
//   at x 6.0, its big button at x 5.05, 1.35 high.
import * as THREE from 'three';
import { box, cyl, sphere, mat, addOutline } from './style.js';
import { grp, at, glowSprite, canvasPlane, rod } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const lerp = (a, b, u) => a + (b - a) * u;
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
// [[t, v], ...] -> v at t, smoothstep between keys (a key [t, v, 'lin'] makes its segment linear, [t, v, 'step'] jumps at t)
const keyAt = (K, t, d = 0) => {
  if (K === undefined || K === null) return d;
  if (typeof K === 'number') return K;
  if (!K.length) return d;
  if (t <= K[0][0]) return K[0][1];
  for (let i = 1; i < K.length; i++) if (t < K[i][0]) {
    if (K[i][2] === 'step') return K[i - 1][1];
    const u = (t - K[i - 1][0]) / Math.max(1e-6, K[i][0] - K[i - 1][0]); return lerp(K[i - 1][1], K[i][1], K[i][2] === 'lin' ? u : smooth(u));
  }
  return K[K.length - 1][1];
};
// [[t, v], ...] -> the last v whose time has come (a switch)
const stepAt = (K, t, d) => { if (typeof K === 'number') return K; let v = d; for (const k of K || []) { if (t >= k[0]) v = k[1]; else break; } return v; };
// a pop (0 before t0, overshoot, settles at 1)
const popK = (t0, t, dur = 0.2) => { if (t0 == null) return 1; const u = (t - t0) / dur; if (u <= 0) return 0; if (u >= 2.5) return 1; return u < 1 ? 1.2 * Math.sin(u * PI / 2) : 1 + 0.2 * Math.cos((u - 1) * PI * 1.2) * Math.exp(-(u - 1) * 2.5); };
// a damped wobble summed over the times [t, ...]
const wob = (T, t, amp, f = 22, dk = 4.3) => { let s = 0; for (const t0 of T || []) { const u = t - t0; if (u > 0) s += amp * Math.sin(u * f) * Math.exp(-u * dk); } return s; };
const INK = '#1B1E2A';
const ink = (m, t = 0.02) => { addOutline(m, t); return m; };
const noCast = g => { g.traverse(c => { if (c.isMesh) c.castShadow = false; }); return g; };
const basic = (c, o = {}) => new THREE.MeshBasicMaterial({ color: c, ...o });
const OFF = { polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -8 };

// the stairwell's numbers (see the header)
const FH = 2.8, ZB = -1.5, ZF = 1.5, XL = -2.8, XR = 3.8, XH = 7.0, XW = 1.4, RISE = 0.175, RUN = 0.35, NST = 8;
const ZA0 = 0.45, ZB1 = -0.45, COLX0 = 1.12, COLZ = 0.14, BH = 1.8, DOORX = 2.9;
const C = { wall: '#EFE6D3', dado: '#BFD3C0', floor: '#D69A78', hall: '#D8B08E', step: '#E6CFA8', nose: '#8A5A3A', wood: '#7A4A2E', col: '#E9DECB', slab: '#E2D6BE', door: '#6F8FB2', frame: '#F4EEE0', dot: '#5A3E2E', end: '#E8DDC8' };

// a box placed by its bounds (x0..x1, y0..y1, z0..z1)
function slabB(x0, x1, y0, y1, z0, z1, color, o = {}) { const m = box(x1 - x0, y1 - y0, z1 - z0, color, o); m.position.set((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2); return m; }

// a tartan painted on a canvas (lilac, sage and butter: no clan, no flag)
function tartan(c, W, H) {
  c.fillStyle = '#8E6AAE'; c.fillRect(0, 0, W, H);
  const band = (x, w, col, a) => { c.globalAlpha = a; c.fillStyle = col; c.fillRect(x, 0, w, H); c.fillRect(0, x, W, w); c.globalAlpha = 1; };
  for (let i = 0; i < 4; i++) { const o = i * W / 4; band(o + W * 0.02, W * 0.07, '#6E9C7A', 0.75); band(o + W * 0.13, W * 0.02, '#F2D27A', 0.9); band(o + W * 0.19, W * 0.035, '#3E2F5A', 0.6); }
}

export const MINUTERIE_PROPS = {
  // ---------------------------------------------------------------- the stairwell: a cutaway of seven floors over the ground floor hall (see the header for its
  // numbers). o.top (7): the highest floor landing; o.from (0): the lowest floor built (a shot high up skips the rest); o.lit: [[t, 0 | 1], ...] the bare
  // bulbs on or off (the scene's dark keys do the dark itself); o.wave [t0, dt]: the bulbs come on floor by floor from t0, dt apart; o.topH (2.8): the
  // top floor's height (a podium needs headroom); o.front: a front wall with stairwell windows (reverse angles); o.hall (true): the ground
  // floor's front door, letterboxes and big tiles; o.cap: the roof slab. The set casts no shadow (a stack of slabs blacked out every floor below),
  // the actors still do on its floors.
  mnStairwell(o) {
    const g = grp(), top = o.top ?? 7, from = o.from ?? 0, bulbs = [], TH = o.topH ?? FH;
    const bulbMat = () => new THREE.MeshLambertMaterial({ color: '#FFF4D2', emissive: '#FFE3A0', emissiveIntensity: 1.1 });
    const addBulb = (x, y, z, fl) => {
      const m = bulbMat(), b = new THREE.Mesh(new THREE.SphereGeometry(0.075, 12, 8), m), s = glowSprite('#FFD27A', 0.75, 0.55);
      b.scale.y = 1.25; g.add(at(cyl(0.006, 0.006, 0.1, '#2A2C31', 4), x, y - 0.05, z), at(cyl(0.03, 0.026, 0.07, '#3A3D44', 8), x, y - 0.12, z)); b.position.set(x, y - 0.21, z); s.position.set(x, y - 0.21, z); g.add(b, s);
      bulbs.push([m, s, fl]);
    };
    for (let k = from; k <= top; k++) {
      const y = FH * k;
      // the floor landing (the ground floor: the whole floor of the hall and of the stair's foot)
      if (k === 0) { g.add(ink(slabB(XL, XH, -0.14, 0.02, ZB, ZF, C.hall), 0.005)); }
      else g.add(ink(slabB(XW, XR, y - 0.22, y, ZB, ZF, C.floor), 0.006));
      // the walls of this floor: the back wall with a dado on the landing, the end walls
      const yT = k === top ? y + TH - 0.22 : y + FH;
      g.add(slabB(XL - 0.2, XW, y, yT, ZB - 0.2, ZB, C.wall));
      g.add(slabB(XW, XR, y, y + 1.0, ZB - 0.2, ZB, C.dado), slabB(XW, XR, y + 1.0, yT, ZB - 0.2, ZB, C.wall));
      g.add(slabB(XL - 0.2, XL, y, yT, ZB - 0.2, ZF, C.end));
      if (k === 0) {
        g.add(slabB(XR, XH, 0, 1.0, ZB - 0.2, ZB, C.dado), slabB(XR, XH, 1.0, FH, ZB - 0.2, ZB, C.wall), slabB(XH, XH + 0.2, 0, FH, ZB - 0.2, ZF, C.end), ink(slabB(XR, XH + 0.2, FH - 0.22, FH, ZB - 0.2, ZF, C.slab), 0.006));
      } else g.add(slabB(XR, XR + 0.2, y - 0.22, yT, ZB - 0.2, ZF, C.end));
      // the floor's door (not on the ground floor: the front door is in the hall), a frame proud of the wall, a knob, and the floor's row of dots
      if (k >= 1) {
        g.add(slabB(DOORX - 0.58, DOORX + 0.58, y, y + 2.28, ZB, ZB + 0.025, C.frame), ink(slabB(DOORX - 0.5, DOORX + 0.5, y, y + 2.18, ZB, ZB + 0.055, C.door), 0.006));
        g.add(slabB(DOORX - 0.4, DOORX + 0.4, y + 1.2, y + 2.0, ZB + 0.055, ZB + 0.07, '#8EAACB'), slabB(DOORX - 0.4, DOORX + 0.4, y + 0.2, y + 1.0, ZB + 0.055, ZB + 0.07, '#8EAACB'));
        g.add(at(sphere(0.045, '#E8C25A', 1, { outline: 0.02 }), DOORX - 0.36, y + 1.05, ZB + 0.1), at(box(0.06, 0.1, 0.02, '#C9A040'), DOORX - 0.36, y + 0.95, ZB + 0.075));
        for (let j = 0; j < k; j++) { const d = at(cyl(0.04, 0.04, 0.02, C.dot, 12), 2.2 - 0.11 * j, y + 1.55, ZB + 0.01, PI / 2, 0, 0); g.add(d); }
      }
      // the bare bulb of the landing
      addBulb(3.35, (k === top ? y + TH : y + FH) - 0.22, -0.9, k);
      if (k === 0) addBulb(5.4, FH - 0.22, -0.9, 0);
      // the newel column for this floor (the buttons ride on its front face)
      g.add(ink(slabB(COLX0, XW, y + (k === 0 ? 0.02 : 0), k === top ? y + TH - 0.22 : y + FH, -COLZ, COLZ, C.col), 0.006));
      if (k === top) { if (o.cap !== false) g.add(ink(slabB(XL - 0.2, XR + 0.2, y + TH - 0.22, y + TH + 0.05, ZB - 0.2, ZF, C.slab), 0.006)); continue; }
      // the half landing, and the two flights of this floor
      const yh = y + 1.4;
      g.add(ink(slabB(XL, -XW, yh - 0.22, yh, ZB, ZF, C.floor), 0.006));
      g.add(slabB(XL - 0.2, XW, yh + 1.0, yh + 1.04, ZB, ZB + 0.012, '#D9CDB5'));
      for (let i = 0; i < NST; i++) {
        const ya = y + RISE * (i + 1), xa1 = XW - RUN * i, xa0 = xa1 - RUN, yb = yh + RISE * (i + 1), xb0 = -XW + RUN * i, xb1 = xb0 + RUN;
        g.add(ink(slabB(xa0, xa1, ya - 0.36, ya, ZA0, ZF, C.step), 0.005), slabB(xa1 - 0.05, xa1 + 0.012, ya - 0.035, ya + 0.012, ZA0, ZF, C.nose));
        g.add(ink(slabB(xb0, xb1, yb - 0.36, yb, ZB, ZB1, C.step), 0.005), slabB(xb0 - 0.012, xb0 + 0.05, yb - 0.035, yb + 0.012, ZB, ZB1, C.nose));
      }
      // banisters: a plain wooden handrail on posts along each flight's inner edge, across the half landing's end and beside the column
      const railA = [[XW, y + 0.95], [-XW, yh + 0.95]], railB = [[-XW, yh + 0.95], [XW, y + FH + 0.95]];
      g.add(rod([railA[0][0], railA[0][1], ZA0 + 0.03], [railA[1][0], railA[1][1], ZA0 + 0.03], 0.03, C.wood), rod([railB[0][0], railB[0][1], ZB1 - 0.03], [railB[1][0], railB[1][1], ZB1 - 0.03], 0.03, C.wood));
      for (let i = 0; i <= NST; i += 2) {
        const xa = XW - RUN * i - (i === NST ? 0 : 0.17), ya = y + RISE * Math.min(NST, i + 1), xb = -XW + RUN * i + (i === NST ? 0 : 0.17), yb = yh + RISE * Math.min(NST, i + 1);
        g.add(rod([xa, ya, ZA0 + 0.03], [xa, ya + 0.95 - (i === NST ? 0 : RISE * 0.5), ZA0 + 0.03], i % 4 === 0 ? 0.026 : 0.013, C.wood));
        g.add(rod([xb, yb, ZB1 - 0.03], [xb, yb + 0.95 - (i === NST ? 0 : RISE * 0.5), ZB1 - 0.03], i % 4 === 0 ? 0.026 : 0.013, C.wood));
      }
      g.add(rod([-XW + 0.03, yh + 0.95, ZB1], [-XW + 0.03, yh + 0.95, ZA0], 0.03, C.wood), rod([-XW + 0.03, yh, 0], [-XW + 0.03, yh + 0.95, 0], 0.015, C.wood));
      g.add(rod([XW - 0.12, y + 0.95, COLZ], [XW - 0.12, y + 0.95, ZA0 + 0.03], 0.026, C.wood), rod([XW - 0.12, y + 0.95, -COLZ], [XW - 0.12, y + 0.95, ZB1 - 0.03], 0.026, C.wood));
      if (o.front) {
        g.add(slabB(XL - 0.2, XR + 0.2, y, yh + 0.6, ZF, ZF + 0.2, C.wall), slabB(XL - 0.2, -1.2, yh + 0.6, y + FH, ZF, ZF + 0.2, C.wall), slabB(0.2, XR + 0.2, yh + 0.6, y + FH, ZF, ZF + 0.2, C.wall));
        g.add(slabB(-1.2, 0.2, yh + 1.9, y + FH, ZF, ZF + 0.2, C.wall), slabB(-1.2, 0.2, yh + 0.6, yh + 1.9, ZF + 0.12, ZF + 0.16, '#BFDDF2', { emissive: '#7FA8C8', noGrain: true }));
        if (k === 0) g.add(slabB(XR, XH + 0.2, 0, FH, ZF, ZF + 0.2, C.wall));
      }
    }
    // the hall: the front door (glazed above), blank letterboxes, a strip of big floor tiles
    if (from === 0 && o.hall !== false) {
      g.add(slabB(5.3, 6.7, 0, 2.5, ZB, ZB + 0.03, C.frame), ink(slabB(5.38, 6.62, 0, 2.42, ZB, ZB + 0.07, '#2F5E8C'), 0.006), slabB(5.5, 6.5, 1.25, 2.25, ZB + 0.07, ZB + 0.09, '#CFE6F5', { emissive: '#9FC4E0', noGrain: true }));
      g.add(at(box(0.32, 0.04, 0.05, '#E8C25A', { outline: 0.01 }), 5.62, 1.05, ZB + 0.12));
      for (let i = 0; i < 8; i++) { const x = 3.98 + (i % 4) * 0.2, yy = 1.25 + Math.floor(i / 4) * 0.3; g.add(ink(slabB(x, x + 0.18, yy, yy + 0.26, ZB, ZB + 0.12, '#B7863E'), 0.004), slabB(x + 0.03, x + 0.15, yy + 0.17, yy + 0.2, ZB + 0.12, ZB + 0.13, '#2A2C31')); }
      for (let i = 0; i < 9; i++) g.add(slabB(XW + 0.6 * i + 0.03, XW + 0.6 * i + 0.57, 0.02, 0.042, ZB + 0.2, ZF - 0.1, i % 2 ? '#E2C4A4' : '#CFA27E'));
    }
    noCast(g);
    g.userData.update = t => { const on = stepAt(o.lit, t, 1) > 0.5, fl = (o.flicker || []).some(([a, b]) => t >= a && t < b && Math.floor((t - a) * 22) % 2 === 0);
      for (const [m, s, k] of bulbs) { const L = on && !fl && (!o.wave || t >= o.wave[0] + k * o.wave[1]); m.emissiveIntensity = L ? 1.1 : 0; m.color.set(L ? '#FFF4D2' : '#B9B4A6'); s.visible = L; } };
    g.userData.update(0);
    return g;
  },

  // ---------------------------------------------------------------- the timer buttons (the running gag): one on the newel column's front face at 1.8 above
  // each floor landing in o.floors ([0..7]), and the big one beside the hall's front door (o.big, true). Each a pale plate, an orange ring and a glowing
  // orange cap, and a soft orange glow that faces the camera (it reads as an orange dot from anywhere, and in the dark: give the prop inDark).
  // o.press [[floor, t], ...] (0: the big one): the cap goes in, the glow flares; o.glow (1): the glow's strength, a number or keys; o.dots: bigger glows
  // (the final shot up the well); o.size (1).
  mnButtons(o) {
    const g = grp(), S = o.size ?? 1, list = [], floors = o.floors || [0, 1, 2, 3, 4, 5, 6, 7];
    const one = (x, y, z, big, floor) => {
      const b = grp(), w = (big ? 0.3 : 0.22) * S;
      b.add(ink(at(box(w, w, 0.025, '#D2D6DA'), 0, 0, 0.0125), 0.006));
      const ring = at(new THREE.Mesh(new THREE.TorusGeometry(w * 0.3, w * 0.06, 6, 20), new THREE.MeshLambertMaterial({ color: '#FFB347', emissive: '#FF8A1E', emissiveIntensity: 0.9 })), 0, 0, 0.03);
      const cap = at(new THREE.Mesh(new THREE.CylinderGeometry(w * 0.24, w * 0.24, 0.03, 18), new THREE.MeshLambertMaterial({ color: '#FFB04A', emissive: '#FF8A1E', emissiveIntensity: 1.0 })), 0, 0, 0.04, PI / 2, 0, 0);
      addOutline(cap, 0.01);
      const gl = glowSprite('#FF9A2E', (o.dots ? 0.95 : 0.6) * S * (big ? 1.25 : 1), 0.85); gl.position.z = 0.09;
      b.add(ring, cap, gl); b.position.set(x, y, z); g.add(b); list.push({ floor, cap, gl, base: gl.scale.x });
    };
    for (const k of floors) one(XW - 0.14, FH * k + BH, COLZ + 0.002, false, k);
    if (o.big !== false) one(5.05, 1.35, ZB + 0.002, true, 0);
    g.userData.update = t => { const G = keyAt(o.glow, t, 1);
      for (const L of list) { let push = 0, flare = 0;
        for (const [f, tp] of o.press || []) if (f === L.floor && t >= tp) { const u = t - tp; push = Math.max(push, u < 0.22 ? 1 : 0); flare = Math.max(flare, Math.exp(-u * 4) * 0.9); }
        L.cap.position.z = 0.04 - 0.018 * push; const s = L.base * (1 + flare) * (0.92 + 0.08 * Math.sin(t * 5.3 + L.floor)); L.gl.scale.set(s, s, 1); L.gl.material.opacity = clamp01(0.85 * G + flare * 0.3); L.gl.visible = G > 0.01 || flare > 0.02; } };
    g.userData.update(0);
    return g;
  },

  // ---------------------------------------------------------------- what stays of the stairwell in the dark: pale lines along every step's nose, the handrails,
  // the landings' edges and the door frames, for the floors o.from .. o.top (give it inDark and visible keys: hidden while the light is on)
  mnDarkLines(o) {
    const g = grp(), M = basic(o.color || '#C9D9F6', { toneMapped: false }), top = o.top ?? 7, from = o.from ?? 0;
    const bar = (x0, x1, y0, y1, z0, z1) => { const m = new THREE.Mesh(new THREE.BoxGeometry(Math.max(0.01, x1 - x0), Math.max(0.01, y1 - y0), Math.max(0.01, z1 - z0)), M); m.position.set((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2); g.add(m); };
    const line = (a, b, r = 0.016) => { const d = new THREE.Vector3(b[0] - a[0], b[1] - a[1], b[2] - a[2]), L = d.length(), m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, L, 5), M);
      m.position.set((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize()); g.add(m); };
    for (let k = from; k <= top; k++) {
      const y = FH * k;
      if (k >= 1) { bar(XW - 0.02, XR, y + 0.005, y + 0.03, ZF - 0.02, ZF + 0.015); bar(DOORX - 0.6, DOORX + 0.6, y + 2.28, y + 2.31, ZB + 0.03, ZB + 0.05); bar(DOORX - 0.6, DOORX - 0.57, y, y + 2.3, ZB + 0.03, ZB + 0.05); bar(DOORX + 0.57, DOORX + 0.6, y, y + 2.3, ZB + 0.03, ZB + 0.05); }
      if (k === top) continue;
      const yh = y + 1.4;
      bar(XL, -XW + 0.02, yh + 0.005, yh + 0.03, ZF - 0.02, ZF + 0.015);
      for (let i = 0; i < NST; i++) { const ya = y + RISE * (i + 1), xa1 = XW - RUN * i, yb = yh + RISE * (i + 1), xb0 = -XW + RUN * i;
        bar(xa1 - 0.035, xa1 + 0.025, ya + 0.012, ya + 0.03, ZA0, ZF + 0.012); bar(xb0 - 0.025, xb0 + 0.035, yb + 0.012, yb + 0.03, ZB, ZB1); }
      line([XW, y + 0.95, ZA0 + 0.03], [-XW, yh + 0.95, ZA0 + 0.03], 0.038); line([-XW, yh + 0.95, ZB1 - 0.03], [XW, y + FH + 0.95, ZB1 - 0.03], 0.038);
      line([-XW + 0.03, yh + 0.95, ZB1], [-XW + 0.03, yh + 0.95, ZA0], 0.038);
    }
    return g;
  },

  // ---------------------------------------------------------------- the timer's grey wall box (pivot at its back, centred; front +Z): a hinged door (o.open
  // keys 0..1, hinge on its left), inside a white dial with six tick marks and one dark hand on a knob, a pale bar along the arc up to the hand (the time
  // left), no digit anywhere. o.hand keys 0..1 (1: thirty seconds, the hand up to the left end of the arc; 0.5 half; 0.03 the last tick); o.click [t, ...]:
  // the box jolts
  mnTimerBox(o) {
    const g = grp(), body = grp(); g.add(body);
    const W = 0.36, H = 0.46, D = 0.11, A0 = 2.3, A1 = -2.3;
    body.add(ink(at(box(W, H, D, '#A3ACB4'), 0, 0, D / 2), 0.008), at(box(W - 0.04, H - 0.04, 0.01, '#5E666E'), 0, 0, D + 0.001));
    const dial = grp(); dial.position.set(0, 0.03, D + 0.012); body.add(dial);
    dial.add(at(cyl(0.135, 0.135, 0.012, '#F6F1E3', 24, { outline: 0.012 }), 0, 0, 0, PI / 2, 0, 0));
    for (let i = 0; i < 6; i++) { const a = lerp(A0, A1, i / 5), tk = at(box(0.014, 0.04, 0.008, INK), Math.sin(a) * 0.105, Math.cos(a) * 0.105, 0.01, 0, 0, -a); dial.add(tk); }
    const seg = [];
    for (let i = 0; i < 24; i++) { const a = lerp(A0, A1, (i + 0.5) / 24), s = at(box(0.026, 0.016, 0.006, '#7FC08A', { noGrain: true }), Math.sin(a) * 0.078, Math.cos(a) * 0.078, 0.008, 0, 0, -a); dial.add(s); seg.push([s, (i + 0.5) / 24]); }
    const hand = grp(); hand.position.z = 0.016; dial.add(hand);
    hand.add(at(box(0.016, 0.1, 0.008, '#22324A', { outline: 0.006 }), 0, 0.05, 0), at(cyl(0.028, 0.028, 0.02, '#3A3D44', 12, { outline: 0.01 }), 0, 0, 0.004, PI / 2, 0, 0));
    body.add(at(box(0.07, 0.03, 0.02, '#3A3D44'), 0, -0.17, D + 0.012));
    const door = grp(); door.position.set(-W / 2, 0, D + 0.02); body.add(door);
    door.add(ink(at(box(W, H, 0.02, '#AEB7BF'), W / 2, 0, 0), 0.008), at(box(0.03, 0.08, 0.015, '#5E666E'), W - 0.04, 0, 0.015));
    g.userData.update = t => { const p = clamp01(keyAt(o.hand, t, 1)), a = lerp(A1, A0, p); hand.rotation.z = -a; for (const [s, u] of seg) s.visible = (1 - u) <= p + 0.001;
      door.rotation.y = -1.95 * clamp01(keyAt(o.open, t, 0)); body.rotation.z = wob(o.click, t, 0.06, 30, 9); };
    g.userData.update(0);
    return g;
  },

  // ---------------------------------------------------------------- the neighbour's shopping trolley (pivot on the floor under the axle; the bag in front, +Z,
  // the handle 0.98 up and 0.08 behind; tip it back with rot x < 0 as it is pulled): two wheels, a tube frame, a tartan bag with a flap and a strap.
  // o.bump [t, ...]: it jolts up a step (the bag squashes and the flap flips)
  mnTrolley(o) {
    const g = grp(), K = grp(); g.add(K);
    for (const sx of [-1, 1]) { const w = at(cyl(0.11, 0.11, 0.05, '#2A2C31', 14, { outline: 0.012 }), sx * 0.2, 0.11, 0, 0, 0, PI / 2); K.add(w, at(cyl(0.04, 0.04, 0.055, '#C9CED3', 8), sx * 0.2, 0.11, 0, 0, 0, PI / 2)); }
    K.add(rod([-0.2, 0.11, 0], [0.2, 0.11, 0], 0.012, '#9AA0A6'), rod([-0.16, 0.11, -0.02], [-0.16, 0.98, -0.08], 0.014, '#9AA0A6'), rod([0.16, 0.11, -0.02], [0.16, 0.98, -0.08], 0.014, '#9AA0A6'), rod([-0.17, 0.98, -0.08], [0.17, 0.98, -0.08], 0.022, '#3A3D44'));
    K.add(at(box(0.38, 0.03, 0.26, '#9AA0A6'), 0, 0.09, 0.12));
    const bag = grp(); bag.position.set(0, 0.11, 0.12); K.add(bag);
    const bm = canvasPlane(1, 1, tartan, { res: 128 }).material; bm.side = THREE.FrontSide;
    const body = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.56, 0.26), bm); body.position.y = 0.29; addOutline(body, 0.012); bag.add(body);
    const flap = grp(); flap.position.set(0, 0.57, -0.13); bag.add(flap); flap.add(ink(at(box(0.37, 0.025, 0.28, '#6A4A8E'), 0, 0.012, 0.14), 0.01), at(box(0.06, 0.12, 0.01, '#3E2F5A'), 0, -0.04, 0.285));
    g.userData.update = t => { let j = 0, f = 0; for (const tb of o.bump || []) { const u = t - tb; if (u > 0 && u < 0.5) { j = Math.max(j, Math.sin(Math.min(1, u / 0.12) * PI) * 0.06 * (u < 0.12 ? 1 : 0)); f = Math.max(f, Math.exp(-u * 7) * Math.sin(u * 30)); } }
      K.position.y = j; bag.scale.set(1 + 0.08 * f, 1 - 0.1 * f, 1 + 0.06 * f); flap.rotation.x = -0.5 * Math.abs(f); };
    g.userData.update(0);
    return g;
  },

  // ---------------------------------------------------------------- the landlord's clipboard (pivot at its middle, the paper +Z): ruled lines, no letter; o.tick
  // [t, ...]: a tick pops on the next line at each time
  mnClipboard(o) {
    const g = grp(); g.add(ink(at(box(0.26, 0.34, 0.012, '#9A6A3E'), 0, 0, 0), 0.01), at(box(0.22, 0.28, 0.004, '#FBF8EE'), 0, -0.01, 0.008), at(box(0.12, 0.04, 0.02, '#C9CED3', { outline: 0.008 }), 0, 0.16, 0.012));
    for (let i = 0; i < 5; i++) g.add(at(box(0.15, 0.006, 0.002, '#9AA6B8'), 0.02, 0.08 - i * 0.05, 0.011));
    const ticks = (o.tick || []).map((tt, i) => { const tk = grp(); tk.add(at(box(0.012, 0.03, 0.003, '#2E7A4A'), -0.008, 0, 0, 0, 0, 0.7), at(box(0.012, 0.055, 0.003, '#2E7A4A'), 0.012, 0.01, 0, 0, 0, -0.5)); tk.position.set(-0.08, 0.08 - i * 0.05, 0.013); g.add(tk); return [tk, tt]; });
    g.userData.update = t => { for (const [tk, tt] of ticks) { const s = popK(tt, t, 0.1); tk.scale.setScalar(Math.max(0.001, s)); tk.visible = s > 0.01; } };
    g.userData.update(0);
    return g;
  },

  // ---------------------------------------------------------------- a roll of blank tickets (pivot at the roll's axle, the strip hanging toward -Y and +Z): o.tear
  // [t, ...]: the lowest ticket comes off and flies out (+Z, up, spinning) and shrinks away; the strip is a ticket shorter between tears
  mnTicketRoll(o) {
    const g = grp(); g.add(ink(at(cyl(0.07, 0.07, 0.15, '#F2E6C8', 14), 0, 0, 0, 0, 0, PI / 2), 0.01), at(cyl(0.025, 0.025, 0.17, '#8A6A45', 8), 0, 0, 0, 0, 0, PI / 2));
    const strip = grp(); strip.position.set(0, 0, 0.07); g.add(strip);
    const tk = []; for (let i = 0; i < 3; i++) { const q = grp(); q.add(ink(at(box(0.14, 0.09, 0.004, '#F6EBCB'), 0, -0.045, 0), 0.006), at(box(0.12, 0.004, 0.005, '#C9A86A'), 0, -0.088, 0.001)); q.position.y = -0.095 * i; strip.add(q); tk.push(q); }
    const fly = grp(); fly.add(ink(at(box(0.14, 0.09, 0.004, '#F6EBCB'), 0, 0, 0), 0.006)); g.add(fly);
    g.userData.update = t => { let last = null; for (const tt of o.tear || []) if (t >= tt) last = tt; const u = last == null ? 99 : t - last;
      tk[2].visible = u > 0.25; fly.visible = u < 0.45; if (fly.visible) { fly.position.set(0.05 * u * 4, -0.24 + 1.2 * u - 1.6 * u * u, 0.12 + 0.5 * u); fly.rotation.set(u * 6, u * 3, u * 9); fly.scale.setScalar(Math.max(0.01, 1 - u * 1.5)); } };
    g.userData.update(0);
    return g;
  },

  // ---------------------------------------------------------------- a stack of plain gold coins (pivot at its bottom): no figure, no symbol; o.n (8) coins, o.count
  // [[t, n], ...] how many show (each new one pops on top), o.r (0.075)
  mnCoins(o) {
    const g = grp(), N = o.n ?? 8, R = o.r ?? 0.075, H = 0.026, cs = [];
    for (let i = 0; i < N; i++) { const c = at(cyl(R, R, H, i % 2 ? '#E8C25A' : '#F0CF6A', 16, { outline: 0.012 }), (hsh(i) - 0.5) * 0.012, H / 2 + i * H, (hsh(i + 7) - 0.5) * 0.012, 0, hsh(i + 3) * PI, 0); g.add(c); cs.push(c); }
    g.userData.update = t => { const n = stepAt(o.count, t, N); let lastT = -9; for (const k of o.count || []) if (t >= k[0]) lastT = k[0];
      cs.forEach((c, i) => { c.visible = i < n; c.scale.setScalar(i === n - 1 ? Math.max(0.01, popK(lastT, t, 0.08)) : 1); }); };
    g.userData.update(0);
    return g;
  },

  // ---------------------------------------------------------------- a towel hung over a handrail (pivot at the fold on the rail, along X): two drops of cloth
  // and a hem, o.color; o.sway: it swings a little
  mnTowel(o) {
    const g = grp(), c = o.color || '#5FB0A8', k = grp(); g.add(k);
    k.add(ink(at(box(0.42, 0.5, 0.025, c), 0, -0.25, 0.045), 0.01), ink(at(box(0.42, 0.36, 0.025, c), 0, -0.18, -0.045), 0.01), at(box(0.42, 0.06, 0.12, c), 0, 0.0, 0), at(box(0.43, 0.035, 0.03, '#F4EEE2'), 0, -0.44, 0.046));
    g.userData.update = t => { k.rotation.x = o.sway ? 0.05 * Math.sin(t * 2.4) : 0; };
    return g;
  },

  // ---------------------------------------------------------------- a sports water bottle (pivot at its bottom): a pale blue body, a white cap, a plain band
  mnBottle(o) { return grp(ink(at(cyl(0.05, 0.055, 0.22, '#8EC6E8', 12), 0, 0.11, 0), 0.012), at(cyl(0.056, 0.056, 0.05, '#F4EEE2', 12), 0, 0.12, 0), at(cyl(0.035, 0.045, 0.05, '#F4F4F0', 10, { outline: 0.01 }), 0, 0.245, 0), at(cyl(0.012, 0.012, 0.03, '#F4F4F0', 6), 0, 0.285, 0)); },

  // ---------------------------------------------------------------- a plain doormat (pivot at its bottom): bristle brown, a darker border, no word
  mnDoormat(o) { const w = o.w ?? 0.95, d = o.d ?? 0.55; return grp(ink(at(box(w, 0.03, d, '#6E4A2E'), 0, 0.015, 0), 0.006), at(box(w - 0.1, 0.034, d - 0.1, '#A8784A'), 0, 0.017, 0)); },

  // ---------------------------------------------------------------- an upright piano (pivot at the floor under its middle, keyboard +Z): a dark body, a lid,
  // a music desk, white keys with black ones, two pedals, casters; o.wobble [[t0, t1]]: it rocks while carried
  mnPiano(o) {
    const g = grp(), K = grp(); g.add(K); const B = o.color || '#5A3424', D = '#3E2418';
    K.add(ink(at(box(1.5, 1.3, 0.55, B), 0, 0.72, -0.05), 0.012), ink(at(box(1.56, 0.06, 0.62, D), 0, 1.39, -0.05), 0.012));
    K.add(ink(at(box(1.46, 0.1, 0.24, B), 0, 0.78, 0.31), 0.01), at(box(1.36, 0.035, 0.16, '#F8F4EA'), 0, 0.845, 0.34));
    for (let i = 0; i < 18; i++) if (i % 7 !== 2 && i % 7 !== 6) K.add(at(box(0.04, 0.03, 0.09, '#141A22'), -0.64 + i * 0.075, 0.875, 0.3));
    K.add(ink(at(box(1.0, 0.36, 0.05, D), 0, 1.13, 0.24), 0.008), ink(at(box(0.12, 0.62, 0.12, D), -0.66, 0.38, 0.28), 0.008), ink(at(box(0.12, 0.62, 0.12, D), 0.66, 0.38, 0.28), 0.008));
    K.add(at(box(0.05, 0.02, 0.1, '#E8C25A'), -0.08, 0.06, 0.25), at(box(0.05, 0.02, 0.1, '#E8C25A'), 0.08, 0.06, 0.25));
    for (const sx of [-0.65, 0.65]) for (const sz of [-0.25, 0.2]) K.add(at(cyl(0.04, 0.04, 0.05, '#2A2C31', 8), sx, 0.025, sz, 0, 0, PI / 2));
    g.userData.update = t => { let w = 0; for (const [a, b] of o.wobble || []) if (t >= a && t < b) w = Math.sin((t - a) * 17) * 0.07; K.rotation.z = w; K.rotation.x = w * 0.4; };
    return g;
  },

  // ---------------------------------------------------------------- a three-step podium (pivot at the floor under the middle block): the middle block highest
  // (gold), the left lower (silver), the right lowest (bronze); colours and heights only, no figure
  mnPodium(o) {
    const g = grp(), W = 0.85, D = o.d ?? 0.8, H = [0.6, 0.95, 0.4], X = [-W, 0, W], Cc = ['#C9D2DA', '#E8C25A', '#C98A5A'], Tc = ['#E4EAF0', '#F6DC86', '#DDA678'];
    for (let i = 0; i < 3; i++) g.add(ink(at(box(W, H[i], D, Cc[i], { pivot: 'bottom' }), X[i], 0, 0), 0.008), at(box(W + 0.04, 0.05, D + 0.04, Tc[i]), X[i], H[i] + 0.02, 0));
    g.userData.tops = H.map((h, i) => [X[i], h + 0.045, 0]); return g;
  },

  // ---------------------------------------------------------------- a plain gold medal on a mustard ribbon, bitten (attach it to the head joint; pivot at the
  // mouth: the disc there, its edge between the teeth, the ribbon falling in a V to the collar); o.lift keys 0..1: from the chest (0) up to the mouth (1)
  mnMedal(o) {
    const g = grp(), d = grp(); g.add(d);
    const disc = ink(at(cyl(0.085, 0.085, 0.022, '#F0C850', 18, { emissive: '#6A4A10' }), 0, 0, 0, PI / 2, 0, 0), 0.012); d.add(disc, at(cyl(0.06, 0.06, 0.024, '#E2B43E', 18), 0, 0, 0.001, PI / 2, 0, 0));
    const rib = (sx) => { const r = at(box(0.045, 0.32, 0.01, '#D9A520', { outline: 0.006 }), sx * 0.05, 0.17, -0.02, 0.3, 0, -sx * 0.32); return r; };
    d.add(rib(-1), rib(1));
    g.userData.update = t => { const u = clamp01(keyAt(o.lift, t, 1)); d.position.set(0, lerp(-0.45, 0, u), lerp(0.08, 0.02, u)); d.rotation.x = lerp(0.2, -0.4, u); };
    g.userData.update(0);
    return g;
  },

  // ---------------------------------------------------------------- an ankle weight (attach to a foot joint; pivot at the ankle): a padded navy cuff with a grey
  // strap, worn over the trousers
  mnAnkleWeight(o) { return grp(ink(at(cyl(0.085, 0.09, 0.1, '#2E4A7A', 10), 0, 0.09, 0), 0.012), at(cyl(0.092, 0.092, 0.03, '#B9C0C8', 10), 0, 0.09, 0), at(box(0.05, 0.05, 0.03, '#B9C0C8'), 0, 0.09, 0.09)); },

  // ---------------------------------------------------------------- the swollen ankle (attach to a foot joint; pivot at the ankle): a round balloon the colour of
  // the skin between the trouser hem and the shoe, o.grow keys 0..1 (it swells with an overshoot), a throb; a pale highlight; o.skin
  mnSwollen(o) {
    const g = grp(), b = grp(); g.add(b); const sk = o.skin || '#E2A878';
    const m = new THREE.Mesh(new THREE.SphereGeometry(0.15, 16, 12), new THREE.MeshLambertMaterial({ color: sk })); addOutline(m, 0.03); b.add(m, at(sphere(0.035, '#F6D8C0', 1, { noGrain: true }), 0.05, 0.07, 0.11));
    b.add(at(cyl(0.11, 0.08, 0.06, '#E8A0A0', 10), 0, -0.1, 0));
    g.userData.update = t => { const s = keyAt(o.grow, t, 1), th = s > 0.5 ? 1 + 0.05 * Math.sin(t * 9) : 1, k = Math.max(0.001, s * th); b.scale.set(k, k * 0.92, k); b.position.y = 0.08 + 0.04 * s; b.visible = s > 0.02; };
    g.userData.update(0);
    return g;
  },

  // ---------------------------------------------------------------- a skipping rope swung round (pivot at the middle of the line between the hands, which run
  // along X from -o.half to +o.half): a red cord in an arc of o.r under that line, turned about it by o.spin (turns per second) from o.t0; the cord ends
  // in two short handles at the hands
  mnTieRope(o) {
    const g = grp(), half = o.half ?? 0.42, R = o.r ?? 0.95, n = 22, arc = grp(); g.add(arc);
    const pts = []; for (let i = 0; i <= n; i++) { const u = i / n, x = lerp(-half, half, u), d = Math.sin(u * PI); pts.push(new THREE.Vector3(x, -R * d, 0)); }
    const tube = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 40, 0.028, 6), new THREE.MeshLambertMaterial({ color: o.color || '#C8372D' })); addOutline(tube, 0.012); arc.add(tube);
    for (const sx of [-1, 1]) g.add(at(cyl(0.03, 0.03, 0.12, '#C8372D', 8, { outline: 0.01 }), sx * half, 0, 0, 0, 0, PI / 2));
    g.userData.update = t => { arc.rotation.x = TAU * (o.spin ?? 1.6) * Math.max(0, t - (o.t0 ?? 0)) + (o.a0 ?? 0); };
    g.userData.update(0);
    return g;
  },

  // ---------------------------------------------------------------- the hero-shaped hole of speed (pivot at the floor, facing +Z): where he stood, his outline in
  // white dashes (box head, shoulders, legs) with speed lines streaming toward -X (o.dir 1) for o.dur (0.55) s from o.at, fading
  mnGhost(o) {
    const g = grp(), M = basic('#FFFFFF', { transparent: true, opacity: 1, depthWrite: false }), dir = o.dir ?? 1, lines = [];
    const P = [[-0.14, 2.28], [0.14, 2.28], [0.14, 1.8], [0.34, 1.62], [0.34, 1.0], [0.18, 1.0], [0.16, 0.05], [0.02, 0.05], [0, 0.9], [-0.02, 0.05], [-0.16, 0.05], [-0.18, 1.0], [-0.34, 1.0], [-0.34, 1.62], [-0.14, 1.8], [-0.14, 2.28]];
    for (let i = 0; i < P.length - 1; i++) { const a = P[i], b = P[i + 1], L = Math.hypot(b[0] - a[0], b[1] - a[1]), nd = Math.max(1, Math.round(L / 0.12));
      for (let j = 0; j < nd; j++) { const u0 = (j + 0.15) / nd, u1 = (j + 0.75) / nd, x0 = lerp(a[0], b[0], u0), y0 = lerp(a[1], b[1], u0), x1 = lerp(a[0], b[0], u1), y1 = lerp(a[1], b[1], u1);
        const m = new THREE.Mesh(new THREE.BoxGeometry(Math.hypot(x1 - x0, y1 - y0), 0.03, 0.01), M); m.position.set((x0 + x1) / 2, (y0 + y1) / 2, 0); m.rotation.z = Math.atan2(y1 - y0, x1 - x0); g.add(m); } }
    for (let i = 0; i < 9; i++) { const m = new THREE.Mesh(new THREE.BoxGeometry(1, 0.035, 0.01), M); m.position.set(0, 0.25 + i * 0.23, 0.02); g.add(m); lines.push([m, 0.6 + 0.9 * hsh(i), hsh(i + 9)]); }
    g.userData.update = t => { const u = (t - (o.at ?? 0)) / (o.dur ?? 0.55); g.visible = u >= 0 && u < 1; M.opacity = clamp01(1.4 - u * 1.4);
      for (const [m, L, ph] of lines) { const w = L * (0.4 + u * 1.2); m.scale.x = w; m.position.x = -dir * (0.3 + w / 2 + u * (0.6 + ph)); } };
    g.userData.update(-1);
    return g;
  },

  // ---------------------------------------------------------------- one block's stairwell windows at night (pivot at the bottom of the strip, facing +Z): a
  // narrow strip of o.n (6) tall windows on a dark band, lit together and blinking on and off fast (o.period 0.22 s, o.phase), o.from: dark before
  mnStrips(o) {
    const g = grp(), N = o.n ?? 6, h = o.fh ?? 2.8, ws = [];
    g.add(at(box(1.2, N * h + 0.4, 0.06, '#2A3046'), 0, (N * h + 0.4) / 2, 0));
    for (let i = 0; i < N; i++) { const m = new THREE.MeshBasicMaterial({ color: '#FFE9A8' }), w = new THREE.Mesh(new THREE.BoxGeometry(0.7, 1.5, 0.04), m); w.position.set(0, 0.6 + i * h + 0.75, 0.04); g.add(w); ws.push(m); }
    const halo = glowSprite('#FFD27A', N * h * 0.55, 0.0); halo.position.set(0, N * h / 2, 0.3); g.add(halo);
    g.userData.update = t => { const on = t >= (o.from ?? -1) && Math.floor((t + (o.phase ?? 0)) / (o.period ?? 0.22)) % 2 === 0;
      for (const m of ws) m.color.set(on ? '#FFE9A8' : '#3A4058'); halo.material.opacity = on ? 0.35 : 0; };
    g.userData.update(0);
    return g;
  },

  // ---------------------------------------------------------------- a standard lamp (pivot at its foot): a tall stem, a pleated cream shade, lit (o.on true)
  mnFloorLamp(o) {
    const g = grp(at(cyl(0.16, 0.18, 0.04, '#3A3D44', 12), 0, 0.02, 0), at(cyl(0.018, 0.018, 1.45, '#8A6A45', 6, { pivot: 'bottom' }), 0, 0.04, 0));
    g.add(ink(at(cyl(0.18, 0.28, 0.32, '#F6E2B0', 12, { emissive: o.on === false ? '#000000' : '#C8A050' }), 0, 1.58, 0), 0.01));
    if (o.on !== false) { const s = glowSprite('#FFD27A', 0.9, 0.35); s.position.y = 1.5; g.add(s); }
    return g;
  },

  // ---------------------------------------------------------------- a geranium in a terracotta pot (pivot at its foot): round leaves, red flower heads; o.water
  // [[t0, t1]]: it perks up (the heads bob) while watered
  mnGeranium(o) {
    const g = grp(), K = grp(); g.add(ink(at(cyl(0.13, 0.1, 0.2, '#C9683A', 12, { pivot: 'bottom' }), 0, 0, 0), 0.01), at(cyl(0.14, 0.14, 0.035, '#B85A30', 12), 0, 0.2, 0), K);
    for (let i = 0; i < 7; i++) { const a = i * 0.9; K.add(at(sphere(0.07, '#5E9A4E', 1), Math.cos(a) * 0.08, 0.27 + 0.03 * (i % 3), Math.sin(a) * 0.08)); }
    const heads = []; for (let i = 0; i < 3; i++) { const a = i * 2.1 + 0.4, h = at(sphere(0.06, '#E2504A', 1, { outline: 0.02 }), Math.cos(a) * 0.07, 0.42 + 0.04 * i, Math.sin(a) * 0.07); K.add(h); heads.push(h); }
    g.userData.update = t => { let w = 0; for (const [a, b] of o.water || []) if (t >= a && t < b + 0.5) w = 1; heads.forEach((h, i) => { h.position.y = 0.42 + 0.04 * i + w * 0.025 * Math.sin(t * 12 + i); }); };
    return g;
  },

  // ---------------------------------------------------------------- a newspaper held open (pivot at its middle, the pages facing +Z): two pages of grey ruled
  // columns and a grey picture, no word
  mnPaper(o) {
    const g = grp();
    for (const sx of [-1, 1]) { const p = at(box(0.34, 0.46, 0.006, '#F4F0E4', { outline: 0.006 }), sx * 0.175, 0, sx * 0.02, 0, -sx * 0.18, 0); g.add(p);
      for (let i = 0; i < 9; i++) p.add(at(box(0.26, 0.012, 0.004, '#9AA0A0'), 0, 0.18 - i * 0.04, 0.005)); p.add(at(box(0.14, 0.11, 0.004, '#B8BEC0'), -0.05, -0.12, 0.006)); }
    return g;
  },

  // ---------------------------------------------------------------- a small brass key standing in a lock (pivot at the tip, the bow toward +Z): o.turn keys
  // (radians about Z)
  mnKey(o) { const g = grp(), k = grp(); g.add(k); k.add(at(box(0.012, 0.025, 0.08, '#E8C25A', { outline: 0.006 }), 0, 0, 0.04), ink(at(cyl(0.035, 0.035, 0.012, '#E8C25A', 10), 0, 0, 0.1, 0, 0, PI / 2), 0.008));
    g.userData.update = t => { k.rotation.z = keyAt(o.turn, t, 0); }; return g; },
};
