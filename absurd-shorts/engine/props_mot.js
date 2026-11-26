// « Le mot » (story 105, cycle 55): a noise wakes this man every night; he pins up a note, « Certains se reconnaîtront. », and the whole country
// recognises itself; noise is banned, the country sleeps at last, giant microphones follow the noise to his bed: he snores, he wakes himself up.
// The next morning there is a note on his door; sixty million notes. His neighbours wear pink earmuffs all along.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time. Every name
// starts with `mo` (props.js merges all the story tables into one: a plain name could override another story's). The only words drawn: the note.
import * as THREE from 'three';
import { box, cyl, sphere, mat, addOutline } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
// a value keyed in time: keys [[t, v], ...] (sorted), eased (smoothstep) between keys; a plain number is a constant
function kv(keys, t, def = 0) {
  if (keys == null) return def;
  if (typeof keys === 'number') return keys;
  if (!keys.length) return def;
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) { const [a, va] = keys[i], [b, vb] = keys[i + 1]; if (t < b) return va + (vb - va) * smooth((t - a) / Math.max(1e-4, b - a)); }
  return keys[keys.length - 1][1];
}
// a damped shake after each time in ts (amplitude a, frequency f, decay k)
const shake = (ts, t, a = 1, f = 40, k = 8) => (ts || []).reduce((s, t0) => { const u = t - t0; return u > 0 && u < 1.2 ? s + a * Math.exp(-k * u) * Math.sin(u * f) : s; }, 0);
// the note, painted: an off-white sheet, two lines of big black felt-tip capitals sized to fit, a strip of tape at the top
const NOTE = ['CERTAINS SE', 'RECONNAÎTRONT.'];
function paintNote(c, W, H, small = false) {
  c.fillStyle = '#FBF8EE'; c.fillRect(0, 0, W, H); c.strokeStyle = '#D9D2BE'; c.lineWidth = W * 0.01; c.strokeRect(W * 0.01, H * 0.01, W * 0.98, H * 0.98);
  let fs = H * 0.3; c.font = `900 ${fs}px Arial`; while (Math.max(...NOTE.map(s => c.measureText(s).width)) > W * 0.88) { fs *= 0.95; c.font = `900 ${fs}px Arial`; }
  c.fillStyle = '#1C1E24'; c.textAlign = 'center'; c.textBaseline = 'middle'; NOTE.forEach((s, i) => c.fillText(s, W / 2 + (i ? 3 : -2) * (small ? 0.3 : 1), H * (0.4 + i * 0.3)));
  c.fillStyle = 'rgba(220,210,170,0.85)'; c.fillRect(W * 0.38, 0, W * 0.24, H * 0.07);
}
// a sheet of scribble lines (no readable text): wavy grey lines and a squiggle
function paintScribble(c, W, H, seed = 1) {
  c.fillStyle = '#FBF8EE'; c.fillRect(0, 0, W, H); c.strokeStyle = '#3A3D44'; c.lineWidth = W * 0.018; c.lineCap = 'round';
  for (let i = 0; i < 6; i++) { const y = H * (0.14 + i * 0.13); c.beginPath(); c.moveTo(W * 0.1, y); for (let x = 0.1; x < 0.9 - 0.15 * hsh(i + seed); x += 0.04) c.lineTo(W * x, y + H * 0.018 * Math.sin(x * 40 + i + seed)); c.stroke(); }
}
// pink fluff: a lumpy ball of small spheres (an earmuff cup)
function FLUFF(r, col = '#FF5FA8') { const g = grp(), core = new THREE.Mesh(new THREE.SphereGeometry(r, 14, 10), mat(col)); addOutline(core, 0.02); g.add(core);
  for (let i = 0; i < 14; i++) { const a = hsh(i) * TAU, b = (hsh(i + 9) - 0.5) * PI, s = new THREE.Mesh(new THREE.SphereGeometry(r * (0.32 + 0.12 * hsh(i + 3)), 7, 5), mat(i % 3 ? col : '#FF86BE')); s.position.set(Math.cos(a) * Math.cos(b) * r * 0.85, Math.sin(b) * r * 0.85, Math.sin(a) * Math.cos(b) * r * 0.85); g.add(s); }
  return g; }

export const MOT_PROPS = {
  // A plain room (pivot at the middle of its floor; back wall at z = -o.d/2, open toward +Z): floor, back and side walls, a skirting board;
  // o.window { x, y, w, h, sky }: a window in the back wall showing a flat sky colour (pale dawn blue by default); o.doorX: a doorway in it
  moRoom(o) {
    const W = o.w ?? 6, D = o.d ?? 5, H = o.h ?? 3, WC = o.wall || '#D9E4F0', g = grp(), bz = -D / 2;
    const fl = new THREE.Mesh(new THREE.PlaneGeometry(W, D), mat(o.floor || '#B9A58A')); fl.rotation.x = -PI / 2; fl.position.y = 0.025; fl.receiveShadow = true; g.add(fl);
    if (o.doorX != null) { const dx = o.doorX, a0 = dx - 0.55, a1 = dx + 0.55;   // o.doorX: an opening 1.1 x 2.2 m in the back wall (a door goes in it)
      g.add(at(box(a0 + W / 2, H, 0.12, WC, { pivot: 'bottom' }), (a0 - W / 2) / 2, 0, bz - 0.06), at(box(W / 2 - a1, H, 0.12, WC, { pivot: 'bottom' }), (a1 + W / 2) / 2, 0, bz - 0.06), at(box(1.1, H - 2.2, 0.12, WC, { pivot: 'bottom' }), dx, 2.2, bz - 0.06)); }
    else g.add(at(box(W, H, 0.12, WC, { pivot: 'bottom' }), 0, 0, bz - 0.06));
    g.add(at(box(0.12, H, D, WC, { pivot: 'bottom' }), -W / 2, 0, 0), at(box(0.12, H, D, WC, { pivot: 'bottom' }), W / 2, 0, 0));
    g.add(at(box(W, 0.12, 0.03, o.trim || '#F4EEE2'), 0, 0.06, bz + 0.015));
    if (o.window) { const q = o.window, ww = q.w ?? 1.2, wh = q.h ?? 1.2, wx = q.x ?? 0, wy = q.y ?? 1.6;
      g.add(at(box(ww, wh, 0.02, q.sky || '#BFD8EE', { emissive: q.glow || '#5A7A9A', noGrain: true }), wx, wy, bz + 0.005));
      for (const [dx, dy, bw, bh] of [[0, wh / 2, ww + 0.1, 0.08], [0, -wh / 2, ww + 0.2, 0.08], [-ww / 2, 0, 0.08, wh], [ww / 2, 0, 0.08, wh], [0, 0, 0.05, wh]]) g.add(at(box(bw, bh, 0.06, '#F4EEE2', { outline: 0.006 }), wx + dx, wy + dy, bz + 0.03)); }
    return g;
  },
  // A flat ground (pivot at its middle, 3 cm up): o.w x o.d of o.color; o.kerb z: a kerb stone along X there and the road beyond
  moGround(o) { const W = o.w ?? 40, D = o.d ?? 30, g = grp(), f = new THREE.Mesh(new THREE.PlaneGeometry(W, D), mat(o.color || '#E4D6BE')); f.rotation.x = -PI / 2; f.position.y = 0.03; f.receiveShadow = true; g.add(f);
    if (o.kerb != null) { const rd = new THREE.Mesh(new THREE.PlaneGeometry(W, 8), mat('#6E6E72')); rd.rotation.x = -PI / 2; rd.position.set(0, 0.031, o.kerb + 4.1); g.add(rd, at(box(W, 0.14, 0.2, '#D9CDB4'), 0, 0.07, o.kerb)); }
    return g; },
  // A town facade (pivot at the floor in the middle, faces +Z): a cream wall, a shop-floor band, a cornice, floors of tall windows with shutters and
  // moulded heads, balconies on the first floor; o.lit: the windows glow warm (dawn); no sign
  moFacade(o) { const w = o.w ?? 12, h = o.h ?? 9, C = o.color || '#EFE6D2', T = '#D9CDB4', g = grp(at(box(w, h, 0.4, C, { pivot: 'bottom', outline: 0.004 }), 0, 0, -0.2));
    g.add(at(box(w + 0.3, 0.3, 0.75, T, { outline: 0.006 }), 0, h, -0.2), at(box(w, 0.25, 0.55, T, { outline: 0.006 }), 0, 3.0, -0.2), at(box(w, 3.0, 0.42, '#D8CBB4', { pivot: 'bottom' }), 0, 0, -0.18));
    const fls = Math.max(1, Math.floor((h - 3.4) / 1.75));
    for (let fl = 0; fl < fls; fl++) for (let x = -w / 2 + 1.2; x < w / 2 - 0.8; x += 2.0) { const y = 3.9 + fl * 1.75;
      g.add(at(box(0.8, 1.25, 0.03, o.lit ? '#FFD98A' : '#5E7A94', o.lit ? { emissive: '#B08030', noGrain: true } : {}), x, y, 0.01), at(box(1.05, 0.12, 0.14, T, { outline: 0.01 }), x, y + 0.72, 0.06), at(box(0.95, 0.08, 0.12, '#F4F1EA'), x, y - 0.66, 0.05));
      for (const sx of [-1, 1]) g.add(at(box(0.36, 1.25, 0.04, o.shutter || '#8FA9B8', { outline: 0.02 }), x + sx * 0.6, y, 0.03));
      if (fl === 0) { g.add(at(box(1.1, 0.06, 0.4, '#3A3D44'), x, y - 0.66, 0.22)); for (let b = 0; b < 8; b++) g.add(at(box(0.02, 0.46, 0.02, '#2A2C31'), x - 0.5 + b * 0.143, y - 0.42, 0.4)); } }
    for (let x = -w / 2 + 1.5; x < w / 2 - 1; x += 3.0) g.add(at(box(1.6, 2.2, 0.03, '#3A4450'), x, 1.15, 0.03));
    return g; },
  // The note « CERTAINS SE RECONNAÎTRONT. » (pivot at its middle, faces +Z): a sheet o.w x o.h; o.pinAt: it is slapped up (pops from flat, a squash)
  moNote(o) { const w = o.w ?? 0.42, h = o.h ?? 0.3, g = grp(), k = grp(); g.add(k); k.add(canvasPlane(w, h, paintNote, { res: 512 }), at(box(w, h, 0.004, '#E8E2D2'), 0, 0, -0.004));
    g.userData.update = t => { const u = o.pinAt != null ? t - o.pinAt : 1; const q = u < 0 ? 0 : Math.exp(-10 * u) * Math.cos(u * 30); k.scale.set(1 + 0.15 * q, 1 - 0.15 * q, 1); k.visible = u >= 0; };
    g.userData.update(0); return g; },
  // A cork board (pivot at its middle, faces +Z): a framed cork panel with three small blank cards pinned
  moCork(o) { const w = o.w ?? 1.1, h = o.h ?? 0.8; return grp(at(box(w + 0.08, h + 0.08, 0.03, '#7A5A3C', { outline: 0.01 }), 0, 0, -0.02), at(box(w, h, 0.03, '#C49A66'), 0, 0, 0),
    ...[[-0.35, 0.2, 0.08, '#F4F1E8'], [0.38, -0.2, -0.06, '#E2EAF0'], [-0.3, -0.25, 0.04, '#F3E9C9']].map(([x, y, rz, c]) => at(box(0.2, 0.15, 0.006, c, { outline: 0.03 }), x * w, y * h, 0.02, 0, 0, rz))); },
  // A bank of blank letterboxes (pivot at its middle, faces +Z): two rows of four sage-green boxes with dark slots, no names
  moBoxes(o) { const g = grp(); for (let i = 0; i < 8; i++) { const x = (i % 4 - 1.5) * 0.34, y = 0.15 - Math.floor(i / 4) * 0.3; g.add(at(box(0.31, 0.27, 0.1, i % 2 ? '#7E8C6E' : '#8A977A', { outline: 0.005 }), x, y, 0), at(box(0.2, 0.02, 0.012, '#1F2228'), x, y + 0.07, 0.055)); } return g; },
  // Big fluffy bright-pink earmuffs (attach to the head joint; pivot at the middle of the head): two head-width cups on a pink band over the top;
  // o.r cup radius, o.span the half distance between the cups, o.top the band's height; o.bow: a gift ribbon and bow (the last shot); o.pop t: pops in
  moEarmuffs(o) { const r = o.r ?? 0.16, S = o.span ?? 0.24, T = o.top ?? 0.3, g = grp(), k = grp(); g.add(k);
    for (const sx of [-1, 1]) { const c = FLUFF(r); c.position.set(sx * S, 0, 0); c.scale.set(0.75, 1, 1); k.add(c); }
    const band = new THREE.Mesh(new THREE.TorusGeometry(S, 0.035, 6, 18, PI), mat('#E8448E')); band.position.y = 0; band.scale.set(1, T / S, 1); addOutline(band, 0.04); k.add(band);
    if (o.bow) { const RC = o.ribbon || '#E8B020', rm = mat(RC);   // (round 1) a looped ribbon bow on the band: two big loops, a knot, two tails (a bar across read as a key)
      for (const sx of [-1, 1]) { const lp = new THREE.Mesh(new THREE.TorusGeometry(0.1, 0.03, 6, 16), rm); lp.scale.set(1.5, 0.8, 1); lp.position.set(sx * 0.14, T + 0.08, 0); lp.rotation.set(0, 0, sx * 0.35); addOutline(lp, 0.04); k.add(lp);
        k.add(at(box(0.07, 0.22, 0.025, RC, { outline: 0.04 }), sx * 0.08, T - 0.07, 0.04, 0, 0, sx * 0.45)); }
      k.add(at(sphere(0.05, RC, 1, { outline: 0.04 }), 0, T + 0.07, 0.02)); }
    const H0 = o.dropH ?? 0;   // (round 1) o.dropAt: it falls from H0 m above and lands at its place with a squash and a wobble
    g.userData.update = t => { let s = 1, y = 0, q = 0;
      if (o.pop != null) { const u = t - o.pop; s = u < 0 ? 0.001 : 1 + 0.25 * Math.exp(-8 * u) * Math.sin(u * 25); }
      if (o.dropAt != null) { const u = t - o.dropAt; if (u < 0) s = 0.001; else if (u < 0.3) y = H0 * (1 - (u / 0.3) ** 2); else q = Math.exp(-9 * (u - 0.3)) * Math.cos((u - 0.3) * 28); }
      k.scale.set(s * (1 + 0.18 * q), s * (1 - 0.22 * q), s * (1 + 0.18 * q)); k.position.y = y; };
    g.userData.update(0); return g; },
  // A puffy duvet over the legs of a man sitting/lying in bed (pivot at the middle of its top end, lies along +Z): a soft wide box, o.color; o.flapAt []: it
  // jumps (the man bolting upright under it)
  moDuvet(o) { const T = o.h ?? 0.22, g = grp(), d = new THREE.Mesh(new THREE.BoxGeometry(o.w ?? 1.25, T, o.l ?? 1.25), mat(o.color || '#8FB8D8')); d.position.set(0, T / 2, (o.l ?? 1.25) / 2); addOutline(d, 0.01); g.add(d);   // (round 1) o.h its thickness
    const fold = at(box((o.w ?? 1.25) + 0.02, T + 0.02, 0.16, '#F4F1EA', { outline: 0.02 }), 0, T / 2 + 0.01, 0.08); g.add(fold);
    g.userData.update = t => { const s = shake(o.flapAt, t, 0.15, 30, 7); d.scale.y = 1 + s; fold.scale.y = 1 + s; }; g.userData.update(0); return g; },
  // A bedside lamp on a small table (pivot at the floor): a warm glowing shade; o.wobble [t, ...]: it rocks and the light flickers
  moLamp(o) { const g = grp(at(box(0.45, 0.55, 0.4, '#8A6A45', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0)), l = grp(); l.position.y = 0.55; g.add(l);
    const shadeM = mat('#FFE6A8', { emissive: '#F0A040', noGrain: true, unique: true });   // (round 1) a bigger shade and a real warm light: the lamp is on in every bedroom shot
    l.add(at(cyl(0.07, 0.1, 0.05, '#3A3D44', 10), 0, 0.025, 0), at(cyl(0.018, 0.018, 0.3, '#3A3D44', 6, { pivot: 'bottom' }), 0, 0.03, 0), at(new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.24, 0.3, 14, 1, true), shadeM), 0, 0.44, 0));
    const P0 = o.power ?? 2.4, bulb = new THREE.PointLight('#FFB060', P0, 3.4, 1.4); bulb.position.y = 0.42; bulb.castShadow = false; l.add(bulb);
    g.userData.update = t => { const s = shake(o.wobble, t, 0.25, 34, 6), p = o.pulse ? 0.8 + 0.2 * Math.sin(t * TAU * o.pulse) : 1, k = (1 - Math.min(0.7, Math.abs(s) * 3)) * p;
      l.rotation.z = s; shadeM.emissive.setRGB(0.94, 0.63, 0.25).multiplyScalar(k); bulb.intensity = P0 * k; };
    g.userData.update(0); return g; },
  // A window with curtains (pivot at its middle, in a back wall, faces +Z): a pale dawn pane, two cloth curtains; o.flap [t, ...]: the curtains billow in
  moCurtains(o) { const w = o.w ?? 1.1, h = o.h ?? 1.3, g = grp(at(box(w, h, 0.02, '#CFE0F0', { emissive: '#7090B0', noGrain: true }), 0, 0, 0), at(box(w + 0.12, 0.08, 0.06, '#F4EEE2', { outline: 0.01 }), 0, h / 2 + 0.06, 0.03));
    const cs = [-1, 1].map(sx => { const p = grp(); p.position.set(sx * (w / 2 - 0.12), h / 2, 0.08); g.add(p); p.add(at(box(0.36, h + 0.1, 0.04, o.color || '#E8A0A0', { outline: 0.01 }), 0, -(h + 0.1) / 2, 0)); return { p, sx }; });
    g.userData.update = t => { const s = (o.flap || []).reduce((a, t0) => { const u = t - t0; return u > 0 && u < 1 ? a + Math.sin(Math.min(1, u / 0.12) * PI / 2) * Math.exp(-4 * u) * (1 + 0.3 * Math.sin(u * 30)) : a; }, 0);
      for (const { p, sx } of cs) { p.rotation.x = -0.9 * s; p.rotation.z = sx * 0.25 * s; } };
    g.userData.update(0); return g; },
  // A plain police-station front (pivot at the floor in the middle, faces +Z): a grey stone block, a big glazed door at o.doorX, two steps, barred
  // windows, a plain blue lamp over the door; no emblem, no flag, no lettering
  moStation(o) { const w = o.w ?? 10, dx = o.doorX ?? 0, g = grp(at(box(w, 6, 0.5, '#B9BEC4', { pivot: 'bottom', outline: 0.004 }), 0, 0, -0.25), at(box(w + 0.3, 0.3, 0.7, '#9AA0A6', { outline: 0.006 }), 0, 6, -0.25));
    g.add(at(box(1.6, 2.6, 0.06, '#3A4A5E', { outline: 0.006 }), dx, 1.3 + 0.3, 0.01), at(box(1.4, 2.3, 0.07, '#9FC6D8', { emissive: '#3E6A7A' }), dx, 1.5 + 0.2, 0.02), at(box(0.05, 2.3, 0.08, '#3A4A5E'), dx, 1.7, 0.03));
    g.add(at(box(2.4, 0.15, 0.6, '#9AA0A6', { outline: 0.006 }), dx, 0.075, 0.3), at(box(2.0, 0.15, 0.35, '#A8AEB4', { outline: 0.006 }), dx, 0.225, 0.18), at(box(0.3, 0.25, 0.25, '#2E5C9E', { emissive: '#18305A' }), dx, 3.25, 0.15));
    for (const x of [-3.6, -2.0, 2.0, 3.6]) { g.add(at(box(0.9, 1.3, 0.03, '#5E7A94'), x + dx * 0, 2.0, 0.01)); for (let b = 0; b < 4; b++) g.add(at(box(0.04, 1.3, 0.04, '#3A3D44'), x - 0.33 + b * 0.22, 2.0, 0.04)); g.add(at(box(0.9, 1.0, 0.03, '#5E7A94'), x, 4.3, 0.01)); }
    return g; },
  // A signed confession sheet (pivot at its middle, faces +Z, upright): a white sheet, grey scribble lines, a signature; o.stampAt [t, ...]: a red stamp mark
  // appears at each time with a little squash of the sheet
  moSheet(o) { const w = o.w ?? 0.3, h = o.h ?? 0.4, g = grp(), k = grp(); g.add(k); k.add(canvasPlane(w, h, (c, W, H) => { paintScribble(c, W, H, o.seed ?? 1); c.strokeStyle = '#1C2A5A'; c.lineWidth = W * 0.02; c.beginPath(); c.moveTo(W * 0.5, H * 0.9); c.bezierCurveTo(W * 0.6, H * 0.8, W * 0.7, H * 0.98, W * 0.88, H * 0.86); c.stroke(); }, { res: 256 }), at(box(w, h, 0.004, '#E8E2D2'), 0, 0, -0.004));
    const st = (o.stampAt || []).map((ts, i) => { const m = new THREE.Mesh(new THREE.CircleGeometry(w * 0.16, 14), new THREE.MeshBasicMaterial({ color: '#C8322A' })); m.position.set(-w * 0.22 + i * w * 0.12, -h * 0.2 + i * h * 0.1, 0.006); k.add(m); return { m, ts }; });
    g.userData.update = t => { let q = 0; for (const { m, ts } of st) { m.visible = t >= ts; const u = t - ts; if (u > 0) q += Math.exp(-12 * u) * Math.cos(u * 30); } k.scale.set(1 + 0.1 * q, 1 - 0.12 * q, 1); };
    g.userData.update(0); return g; },
  // A rubber stamp (pivot at its base, the rubber at y = 0): a red rubber pad, a dark block, a round wooden handle on top
  moStamp(o) { return grp(at(box(0.12, 0.03, 0.08, '#C8322A'), 0, 0.015, 0), at(box(0.13, 0.05, 0.09, '#3A3D44', { outline: 0.03 }), 0, 0.055, 0), at(cyl(0.02, 0.02, 0.1, '#8A6A45', 8), 0, 0.13, 0), at(sphere(0.04, '#8A6A45', 1, { outline: 0.04 }), 0, 0.2, 0)); },
  // A tall pile of signed sheets (pivot at the floor, faces +Z): a slightly leaning stack of white sheets up to o.h, a few edges askew
  moPile(o) { const H = o.h ?? 1.5, g = grp(); let y = 0; for (let i = 0; y < H; i++) { const th = 0.02; g.add(at(box(0.32 + 0.02 * hsh(i), th, 0.42, i % 7 === 3 ? '#F2EDDE' : '#FBF8EE', i % 4 === 0 ? { outline: 0.02 } : {}), 0.02 * Math.sin(i * 0.7) + y * 0.03, y + th / 2, 0.015 * Math.cos(i), 0, 0.12 * Math.sin(i * 1.9), 0)); y += th; } return g; },
  // A big bright-orange cordless drill (pivot at its grip, the bit toward +X): a body, a chuck and bit, a black battery under the grip; no brand
  moDrill(o) { return grp(at(box(0.34, 0.14, 0.11, '#F07A1E', { outline: 0.02 }), 0.08, 0.13, 0), at(box(0.09, 0.2, 0.09, '#F07A1E', { outline: 0.02 }), 0, 0, 0), at(box(0.14, 0.08, 0.13, '#2A2C31', { outline: 0.02 }), 0, -0.13, 0),
    at(cyl(0.04, 0.035, 0.08, '#2A2C31', 10), 0.29, 0.13, 0, 0, 0, PI / 2), at(cyl(0.012, 0.008, 0.16, '#C9CED4', 6), 0.41, 0.13, 0, 0, 0, PI / 2), at(box(0.05, 0.04, 0.02, '#2A2C31'), 0.04, 0.06, 0.05)); },
  // A flat front door in its frame on a landing wall (pivot at the floor in the middle, faces +Z): o.color leaf, a knob, a bell button beside it; o.open
  // [[t, 0..1]]: it swings inward (away from +Z) hinged at its left; o.note: the note taped on its outer face at eye level; the doorway is open
  // (put a room behind it)
  moDoor(o) { const W = 0.95, H = 2.1, g = grp(), C = o.color || '#2F5E8C';
    g.add(at(box(0.1, H + 0.1, 0.14, '#F2EDE2', { outline: 0.006 }), -W / 2 - 0.05, (H + 0.1) / 2, 0), at(box(0.1, H + 0.1, 0.14, '#F2EDE2', { outline: 0.006 }), W / 2 + 0.05, (H + 0.1) / 2, 0), at(box(W + 0.2, 0.1, 0.14, '#F2EDE2', { outline: 0.006 }), 0, H + 0.05, 0));
    g.add(at(box(0.06, 0.1, 0.03, '#E8E2D2', { outline: 0.03 }), W / 2 + 0.25, 1.4, 0.03), at(cyl(0.018, 0.018, 0.02, '#C8322A', 8), W / 2 + 0.25, 1.42, 0.05, PI / 2, 0, 0));
    const lf = grp(); lf.position.set(-W / 2, 0, 0); g.add(lf); lf.add(at(box(W, H, 0.05, C, { outline: 0.006 }), W / 2, H / 2, 0), at(sphere(0.035, '#E3C56A', 1), W - 0.1, 1.0, 0.04));
    for (const y of [0.55, 1.5]) lf.add(at(box(W - 0.2, 0.7, 0.01, C === '#2F5E8C' ? '#2A5480' : '#5A3E28'), W / 2, y, 0.03));
    if (o.note) { const n = canvasPlane(0.4, 0.29, paintNote, { res: 512 }); n.position.set(W / 2, 1.62, 0.04); lf.add(n); }
    g.userData.update = t => { lf.rotation.y = 1.6 * kv(o.open, t, 0); }; g.userData.update(0); return g; },
  // A council room front bench and lectern (pivot at the floor in the middle, faces +Z): a straight wooden bench with a desk front in a row, a plain
  // coloured hanging panel behind (no word, no emblem), a lectern at o.lecternX
  moCouncil(o) { const W = o.w ?? 4.2, g = grp(at(box(W, 0.85, 0.5, '#8A6A45', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0.6), at(box(W + 0.1, 0.06, 0.6, '#6A4A30', { outline: 0.01 }), 0, 0.88, 0.6), at(box(W - 0.2, 0.45, 0.45, '#7A5A3C', { pivot: 'bottom' }), 0, 0, -0.1), at(box(W - 0.2, 0.6, 0.08, '#6A4A30', { pivot: 'bottom' }), 0, 0.45, -0.32));
    if (o.riser) g.add(at(box(W + 0.3, o.riser, 1.7, '#7A5A3C', { pivot: 'bottom', outline: 0.006 }), 0, -o.riser, 0.15));   // (round 1) a step: a second straight row behind and above
    if (o.panel !== false) g.add(at(box(o.panelW ?? 2.6, 1.3, 0.04, o.panel || '#3E6A9A', { outline: 0.006 }), o.panelX ?? 0, o.panelY ?? 2.6, -1.6), at(box((o.panelW ?? 2.6) + 0.1, 0.08, 0.06, '#C9A24A'), o.panelX ?? 0, (o.panelY ?? 2.6) + 0.68, -1.58));
    const lx = o.lecternX ?? 0; if (o.lecternX !== null) g.add(at(box(0.7, 1.05, 0.45, '#8A6A45', { pivot: 'bottom', outline: 0.006 }), lx, 0, o.lecternZ ?? -1.0), at(box(0.8, 0.06, 0.55, '#6A4A30'), lx, 1.08, o.lecternZ ?? -1.0)); return g; },
  // A fire engine (pivot at the floor in its middle, faces +X, length along X): a red body and cab with a window, a white stripe, a ladder on the
  // roof, the roof siren wrapped in a big knitted striped tea cosy with a pompom; turning wheels at o.speed; no cross, crest or number
  moFireTruck(o) { const g = grp(), R = '#C8322A', wh = [];
    g.add(at(box(4.4, 1.5, 2.1, R, { pivot: 'bottom', outline: 0.005 }), -0.5, 0.5, 0), at(box(1.6, 1.9, 2.1, R, { pivot: 'bottom', outline: 0.005 }), 1.8, 0.5, 0), at(box(4.4, 0.12, 2.12, '#F4F1EA'), -0.5, 1.2, 0));
    for (const z of [-1.06, 1.06]) g.add(at(box(0.9, 0.7, 0.02, '#9FC6D8', { emissive: '#3E6A7A' }), 1.9, 1.85, z));
    g.add(at(box(1.0, 0.75, 2.12, '#9FC6D8', { emissive: '#3E6A7A' }), 2.55, 1.85, 0), at(box(0.2, 0.3, 2.0, '#3A3D44'), 2.65, 0.65, 0));
    for (let i = 0; i < 6; i++) g.add(at(box(0.04, 0.06, 0.6, '#C9CED4'), 0.0 + i * 0.3, 2.08, 0)); for (const z of [-0.3, 0.3]) g.add(at(box(1.6, 0.06, 0.05, '#C9CED4'), 0.75, 2.08, z));
    // (round 1) the siren and its knitted tea cosy sit over the side step, above the firemen (o.cosyX), big: the gag is in the middle of the frame
    const cx = o.cosyX ?? -1.0, cy = o.cosyY ?? 2.5, cosy = grp(); cosy.position.set(cx, cy, 0.2); g.add(cosy, at(box(0.7, 0.12, 0.7, '#3A3D44', { outline: 0.02 }), cx, 2.06, 0.2), at(cyl(0.08, 0.08, cy - 2.06, '#8A8F96', 8, { pivot: 'bottom', outline: 0.02 }), cx, 2.06, 0.2), at(box(0.62, 0.08, 0.62, '#3A3D44', { outline: 0.02 }), cx, cy - 0.02, 0.2));
    for (let i = 0; i < 6; i++) { const r0 = 0.42 - i * 0.05, b = new THREE.Mesh(new THREE.CylinderGeometry(r0 - 0.045, r0, 0.12, 16), mat(['#E8742A', '#F2C94C', '#3E7FB6', '#5E8C4A', '#C86A8A', '#E8742A'][i])); b.position.y = 0.06 + i * 0.12; addOutline(b, 0.02); cosy.add(b); }
    cosy.add(at(sphere(0.13, '#F4F1EA', 1, { outline: 0.03 }), 0, 0.82, 0));
    for (const x of [-2.0, 1.8]) for (const z of [-1.05, 1.05]) { const w_ = grp(at(cyl(0.48, 0.48, 0.3, '#1E2024', 14), 0, 0, 0, PI / 2, 0, 0), at(cyl(0.22, 0.22, 0.32, '#C9CED4', 8), 0, 0, 0, PI / 2, 0, 0), at(box(0.3, 0.06, 0.33, '#8A8F96'), 0, 0, 0)); w_.position.set(x, 0.48, z); g.add(w_); wh.push(w_); }
    g.userData.update = t => { for (const w_ of wh) w_.rotation.z = -t * (o.speed ?? 3) / 0.48; cosy.rotation.z = 0.05 * Math.sin(t * 9); cosy.scale.y = 1 + 0.04 * Math.sin(t * 18); }; g.userData.update(0); return g; },
  // A wheelie bin (pivot at its bottom middle, faces +Z): a dark green tapered tub, a lid, two wheels at the back; o.lid [[t, 0..1]]: the lid lifts
  moBin(o) { const C = o.color || '#5E6A74', LC = o.lidColor || '#F2C94C', g = grp(at(box(0.6, 0.95, 0.7, C, { pivot: 'bottom', outline: 0.01, taper: 1.12 }), 0, 0.05, 0)), lid = grp(at(box(0.7, 0.06, 0.8, LC, { outline: 0.01 }), 0, 0, 0.38)); lid.position.set(0, 1.03, -0.38); g.add(lid);
    for (const sx of [-1, 1]) g.add(at(cyl(0.1, 0.1, 0.06, '#1E2024', 10), sx * 0.3, 0.1, -0.32, 0, 0, PI / 2)); g.add(at(box(0.5, 0.05, 0.05, '#3A3D44'), 0, 0.98, -0.42));
    // (round 1) o.blanket: swaddled like a baby in a pale blue blanket with a white fold (a bare green tub read as a box)
    if (o.blanket) g.add(at(box(0.74, 0.62, 0.84, o.blanket === true ? '#BFD8F0' : o.blanket, { pivot: 'bottom', outline: 0.012, taper: 1.06 }), 0, 0.12, 0), at(box(0.78, 0.1, 0.88, '#F4F1EA', { outline: 0.012 }), 0, 0.76, 0));
    g.userData.update = t => { lid.rotation.x = -1.2 * kv(o.lid, t, 0); }; g.userData.update(0); return g; },
  // A big rooster (pivot at its feet, faces +X, side on): a white-and-russet body, a dark green tail fan, a red comb and wattle, a yellow beak and legs;
  // o.crow [t, ...]: the head throws back, the beak gapes, the comb shakes (silent)
  moRooster(o) { const g = grp(), b = grp(); b.position.y = 0.42; g.add(b);
    const body = new THREE.Mesh(new THREE.SphereGeometry(0.26, 14, 10), mat('#F4F1EA')); body.scale.set(1.25, 1, 0.85); addOutline(body, 0.02); b.add(body);
    b.add(at(new THREE.Mesh(new THREE.SphereGeometry(0.18, 10, 8), mat('#B5652E')), -0.05, 0.02, 0.17), at(new THREE.Mesh(new THREE.SphereGeometry(0.18, 10, 8), mat('#B5652E')), -0.05, 0.02, -0.17));   // russet wings
    for (let i = 0; i < 5; i++) { const f = at(box(0.06, 0.42, 0.14, i % 2 ? '#1E5A40' : '#2A3A4A', { outline: 0.03 }), -0.32, 0.22, 0, 0, 0, 0.5 + i * 0.18); f.position.z = (i - 2) * 0.04; b.add(f); }   // the tail fan
    const nk = grp(); nk.position.set(0.22, 0.12, 0); b.add(nk); nk.add(at(cyl(0.08, 0.11, 0.26, '#E8B070', 8, { pivot: 'bottom', outline: 0.02 }), 0, 0, 0, 0, 0, -0.3));
    const hd = grp(); hd.position.set(0.08, 0.26, 0); nk.add(hd); hd.add(at(sphere(0.1, '#F4F1EA', 1, { outline: 0.03 }), 0, 0, 0));
    for (let i = 0; i < 4; i++) hd.add(at(box(0.05, 0.08, 0.04, '#D8262E', { outline: 0.04 }), -0.05 + i * 0.045, 0.1 + 0.02 * Math.sin(i * 2), 0, 0, 0, -0.2 + i * 0.1));   // the comb
    hd.add(at(box(0.04, 0.07, 0.03, '#D8262E'), 0.07, -0.08, 0), at(sphere(0.018, '#14161A', 0), 0.05, 0.03, 0.08), at(sphere(0.018, '#14161A', 0), 0.05, 0.03, -0.08));
    const bu = at(new THREE.Mesh(new THREE.ConeGeometry(0.035, 0.1, 6), mat('#F2C94C')), 0.13, 0.0, 0, 0, 0, -PI / 2); const bl = at(new THREE.Mesh(new THREE.ConeGeometry(0.03, 0.08, 6), mat('#E8B030')), 0.12, -0.03, 0, 0, 0, -PI / 2); hd.add(bu, bl);
    for (const z of [-0.07, 0.07]) g.add(at(cyl(0.015, 0.015, 0.25, '#E8B030', 5, { pivot: 'bottom' }), 0.02, 0.0, z), at(box(0.1, 0.02, 0.06, '#E8B030'), 0.05, 0.01, z));
    g.userData.update = t => { let c = 0; for (const t0 of o.crow || []) { const u = t - t0; if (u > -0.12 && u < 0.6) c = Math.max(c, u < 0 ? (u + 0.12) / 0.12 * 0.3 : u < 0.45 ? 1 : 1 - (u - 0.45) / 0.15); }
      nk.rotation.z = -0.15 * (1 - c) + 0.55 * c; hd.rotation.z = 0.6 * c; bl.rotation.z = -PI / 2 - 0.7 * c; bl.position.y = -0.03 - 0.03 * c; b.scale.set(1 - 0.05 * c, 1 + 0.12 * c, 1); b.rotation.z = 0.1 * c; };
    g.userData.update(0); return g; },
  // A glass dome (pivot at its rim's centre, the dome rises along +Y): no glass fill (a translucent pane in front of a body reads badly): a metal rim,
  // a knob, a few bright edge highlights; o.fog [t, ...]: an OPAQUE white mist fills the dome at each time and clears (never semi-transparent);
  // o.r its radius
  moDome(o) { const R = o.r ?? 0.6, Hh = o.h ?? R * 1.15, sy = Hh / R, g = grp(), body = grp(), mist = grp(); g.add(body); body.add(mist);
    body.add(at(new THREE.Mesh(new THREE.TorusGeometry(R, 0.04, 6, 28), mat('#B9BEC4')), 0, 0.01, 0, PI / 2, 0, 0), at(sphere(0.07, '#B9BEC4', 1, { outline: 0.04 }), 0, Hh + 0.05, 0));
    // (round 1) the glass reads: a fresnel shell, clear in the middle and white at the silhouette (floating rings alone read as hoops)
    const glassM = new THREE.ShaderMaterial({ transparent: true, depthWrite: false,
      vertexShader: 'varying vec3 vN; varying vec3 vV; void main() { vec4 mv = modelViewMatrix * vec4(position, 1.0); vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix * mv; }',
      fragmentShader: 'varying vec3 vN; varying vec3 vV; void main() { float f = 1.0 - abs(dot(normalize(vN), normalize(vV))); gl_FragColor = vec4(0.9, 0.96, 1.0, 0.03 + 0.8 * pow(f, 2.5)); }' });
    const shell = new THREE.Mesh(new THREE.SphereGeometry(R, 28, 16, 0, TAU, 0, PI / 2), glassM); shell.scale.y = sy; shell.renderOrder = 2; body.add(shell);
    for (let i = 0; i < 2; i++) { const a = new THREE.Mesh(new THREE.TorusGeometry(R * 0.98, 0.014, 4, 24, PI * 0.3), new THREE.MeshBasicMaterial({ color: '#FFFFFF' })); a.rotation.set(0, -0.6 + i * 0.22, PI * 0.38 + i * 0.06); a.scale.y = sy; body.add(a); }   // two glints
    const m = new THREE.Mesh(new THREE.SphereGeometry(R * 0.99, 18, 12, 0, TAU, 0, PI / 2), new THREE.MeshLambertMaterial({ color: '#FFFFFF', emissive: '#C8CCD2' })); m.scale.y = sy; mist.add(m);
    for (let i = 0; i < 6; i++) mist.add(at(sphere(R * 0.28, '#F2F4F6', 1), Math.cos(i) * R * 0.55, Hh * (0.3 + 0.12 * (i % 3)), Math.sin(i * 1.7) * R * 0.3 + R * 0.62));
    // o.fog [t, ...]: an OPAQUE white mist fills it in 0.06 s, holds, then wipes down to the rim and the glass is clear again (never see-through)
    g.userData.update = t => { let f = 0; for (const t0 of o.fog || []) { const u = t - t0; if (u > 0 && u < 0.5) f = Math.max(f, u < 0.06 ? u / 0.06 : u < 0.2 ? 1 : 1 - (u - 0.2) / 0.3); }
      mist.visible = f > 0.03; mist.scale.set(1, Math.max(0.03, f), 1);
      const q = (o.squash || []).reduce((a, t0) => { const u = t - t0; return u > 0 && u < 0.6 ? a + Math.exp(-9 * u) * Math.cos(u * 30) : a; }, 0); body.scale.set(1 + 0.1 * q, 1 - 0.13 * q, 1 + 0.1 * q); };
    g.userData.update(0); return g; },
  // A wooden fence post with two rails (pivot at the floor, rails along X): the post top at o.h (1.0)
  moFence(o) { const h = o.h ?? 1.0, g = grp(at(box(0.18, h, 0.18, '#8A6A45', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0)); for (const y of [0.4, 0.8]) g.add(at(box(o.w ?? 4, 0.1, 0.06, '#9A7A55', { outline: 0.008 }), 0, y * h, -0.1)); return g; },
  // A plain red barn (pivot at the floor, faces +Z): a red box with a white-trimmed door and a grey roof; no sign
  moBarn(o) { const g = grp(at(box(4, 2.6, 3, '#B5452E', { pivot: 'bottom', outline: 0.005 }), 0, 0, 0)); const rf = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 2.3, 1.4, 4, 1), mat('#6E6E72')); rf.rotation.y = PI / 4; rf.scale.set(1.25, 1, 0.95); rf.position.y = 3.3; g.add(rf);
    g.add(at(box(1.4, 1.8, 0.04, '#8A2E1E', { outline: 0.01 }), 0, 0.9, 1.51), at(box(1.5, 0.08, 0.05, '#F4F1EA'), 0, 1.84, 1.52), at(box(0.08, 1.8, 0.05, '#F4F1EA'), 0, 0.9, 1.53)); return g; },
  // A café table with two chairs (pivot at the floor, faces +Z): a round table top on a pedestal, two bistro chairs at the sides (o.chairs false: none)
  moCafeTable(o) { const g = grp(at(cyl(0.45, 0.45, 0.04, '#E8E2D2', 18, { outline: 0.01 }), 0, 0.74, 0), at(cyl(0.03, 0.03, 0.72, '#3A3D44', 6, { pivot: 'bottom' }), 0, 0, 0), at(cyl(0.22, 0.25, 0.03, '#3A3D44', 10), 0, 0.015, 0));
    if (o.chairs !== false) for (const sx of [-1, 1]) { const c = grp(at(cyl(0.2, 0.2, 0.04, '#8A5A38', 12), 0, 0.46, 0), at(cyl(0.02, 0.02, 0.46, '#3A3D44', 6, { pivot: 'bottom' }), 0, 0, 0), at(box(0.04, 0.45, 0.36, '#8A5A38', { outline: 0.02 }), sx * 0.18, 0.7, 0)); c.position.x = sx * 0.75; g.add(c); }
    return g; },
  // A sheet of scribbles (pivot at its middle, faces +Z): a big sheet of wavy lines, no readable text; o.seed varies the lines
  moScribble(o) { const w = o.w ?? 0.4, h = o.h ?? 0.3; return grp(canvasPlane(w, h, (c, W, H) => paintScribble(c, W, H, o.seed ?? 1), { res: 256 }), at(box(w, h, 0.004, '#E8E2D2'), 0, 0, -0.004)); },
  // A café awning and shopfront (pivot at the floor in the middle, faces +Z): a striped awning, a window, a door; no sign
  moCafeFront(o) { const w = o.w ?? 7, g = grp(at(box(w, 3.4, 0.3, '#E8D8B8', { pivot: 'bottom', outline: 0.005 }), 0, 0, -0.15));
    for (let i = 0; i < 12; i++) g.add(at(box(w / 12, 0.08, 1.1, i % 2 ? '#F4F1EA' : '#2E6A4A', { outline: 0.006 }), -w / 2 + (i + 0.5) * w / 12, 2.75, 0.45, -0.35, 0, 0));
    g.add(at(box(2.4, 1.6, 0.04, '#9FC6D8', { emissive: '#3E6A7A' }), -1.6, 1.3, 0.02), at(box(2.4, 1.6, 0.04, '#9FC6D8', { emissive: '#3E6A7A' }), 1.6, 1.3, 0.02), at(box(1.0, 2.2, 0.04, '#5A3E28', { outline: 0.006 }), 0, 1.1, 0.02)); return g; },
  // A block of flats cut open on three flats stacked one above the other (pivot at the floor of the middle flat, faces +Z): three rooms o.rw wide with
  // pale dawn walls, floors and slabs, a warm wall lamp and a dawn window in each, a bed in each, side on (head at -X); outer walls; no number
  moCutaway(o) { const g = grp(), RW = o.rw ?? 3.2, H = 2.6, D = 2.2, FH = H + 0.25, WC = o.walls || ['#CFDCEA', '#D9E4F0', '#D2DEEC'], lamps = [];
    for (let i = -1; i <= 1; i++) { const y = i * FH;
      g.add(at(box(RW, H, 0.1, WC[i + 1], { pivot: 'bottom' }), 0, y, -D / 2), at(box(RW + 0.02, 0.25, D, '#B9AE9A', { outline: 0.004 }), 0, y - 0.125, 0));
      g.add(at(box(0.8, 0.8, 0.02, '#CFE0F0', { emissive: '#6A88A8', noGrain: true }), 0.75, y + 1.6, -D / 2 + 0.06), at(box(0.9, 0.06, 0.05, '#F4EEE2'), 0.75, y + 2.03, -D / 2 + 0.08), at(box(0.9, 0.06, 0.05, '#F4EEE2'), 0.75, y + 1.17, -D / 2 + 0.08));
      // (round 1) a bigger bedside lamp with a real warm light in each flat; o.pulse (Hz): the middle one (his) pulses
      const lm = mat('#FFE6A8', { emissive: '#F0A040', noGrain: true, unique: true }), lt = new THREE.PointLight('#FFB060', 1.6, 3.0, 1.4); lt.position.set(-1.0, y + 1.1, -0.3); lt.castShadow = false;
      g.add(at(box(0.36, 0.5, 0.3, '#8A6A45', { pivot: 'bottom', outline: 0.01 }), -1.15, y, -0.75), at(new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.2, 0.24, 12, 1, true), lm), -1.15, y + 0.78, -0.75), at(cyl(0.015, 0.015, 0.2, '#3A3D44', 6, { pivot: 'bottom' }), -1.15, y + 0.5, -0.75), lt);
      lamps.push({ lm, lt, mid: i === 0 });
      if (o.beds !== false) { const B = grp(at(box(1.1, 0.28, 1.9, '#5A3E28', { pivot: 'bottom' }), 0, 0.1, 0), at(box(1.0, 0.22, 1.8, '#F4F1EA'), 0, 0.48, 0), at(box(0.6, 0.12, 0.32, '#FBF8EE', { taper: 0.85 }), 0, 0.64, -0.68), at(box(1.14, 0.9, 0.08, '#5A3E28', { pivot: 'bottom', outline: 0.01 }), 0, 0, -0.98)); B.position.set(0.0, y, -0.35); B.rotation.y = PI / 2; g.add(B); } }   // side on: the sleeper reads in profile
    g.add(at(box(RW + 0.04, 0.25, D, '#B9AE9A', { outline: 0.004 }), 0, 2 * FH - 0.125, 0));
    for (const sx of [-1, 1]) g.add(at(box(0.18, 3 * FH + 0.25, D + 0.1, '#CFC6B4', { pivot: 'bottom', outline: 0.005 }), sx * (RW / 2 + 0.09), -FH - 0.25, 0));
    g.userData.update = t => { for (const { lm, lt, mid } of lamps) { const p = mid && o.pulse ? 0.65 + 0.35 * Math.sin(t * TAU * o.pulse) : 1; lm.emissive.setRGB(0.94, 0.63, 0.25).multiplyScalar(p); lt.intensity = 1.6 * p; } };
    g.userData.update(0); return g; },
  // A rooftop ridge (pivot at the ridge's middle, ridge along X at y = 0): two tiled slopes going down, a chimney; o.aerial: a TV aerial on a mast that
  // rattles at o.rattle [t, ...]
  moRoof(o) { const L = o.len ?? 6, g = grp(), ae = grp();
    for (const sz of [-1, 1]) { const s = new THREE.Mesh(new THREE.BoxGeometry(L, 0.08, 2.4), mat('#B5652E')); s.position.set(0, -0.6, sz * 1.05); s.rotation.x = sz * 0.55; addOutline(s, 0.006); g.add(s);
      for (let i = 0; i < 5; i++) g.add(at(box(L, 0.03, 0.04, '#8A4A22'), 0, -0.15 - i * 0.24, sz * (0.25 + i * 0.42), sz * 0.55, 0, 0)); }
    g.add(at(box(L + 0.1, 0.12, 0.18, '#8A4A22', { outline: 0.01 }), 0, 0, 0), at(box(0.5, 0.9, 0.5, '#B9AE9A', { pivot: 'bottom', outline: 0.008 }), -L / 2 + 0.8, -0.2, 0));
    ae.position.set(L / 2 - 0.9, 0, 0); g.add(ae); ae.add(at(cyl(0.025, 0.025, 1.4, '#6E757C', 6, { pivot: 'bottom' }), 0, 0, 0), at(box(0.9, 0.03, 0.03, '#6E757C'), 0, 1.1, 0), at(box(0.03, 0.03, 0.6, '#6E757C'), 0, 1.3, 0));
    for (let i = 0; i < 5; i++) ae.add(at(box(0.02, 0.02, 0.4 - i * 0.05, '#6E757C'), -0.35 + i * 0.17, 1.1, 0));
    g.userData.update = t => { ae.rotation.z = shake(o.rattle, t, 0.12, 45, 4); ae.rotation.x = shake(o.rattle, t, 0.06, 37, 4); }; g.userData.update(0); return g; },
  // A row of shutters on a facade (pivot at the middle, faces +Z): o.n pairs of slatted blue shutters on dark windows; o.rattle [t, ...]: they rattle
  moShutters(o) { const n = o.n ?? 4, g = grp(), ps = [];
    for (let i = 0; i < n; i++) { const x = (i - (n - 1) / 2) * 1.6; g.add(at(box(0.8, 1.2, 0.02, '#3A4450'), x, 0, 0)); for (const sx of [-1, 1]) { const p = grp(); p.position.set(x + sx * 0.4, 0, 0.03); g.add(p); p.add(at(box(0.38, 1.2, 0.04, '#5F8FB0', { outline: 0.02 }), -sx * 0.19, 0, 0)); for (let s = 0; s < 6; s++) p.add(at(box(0.36, 0.02, 0.05, '#4A7896'), -sx * 0.19, -0.5 + s * 0.2, 0.01)); ps.push({ p, sx, i }); } }
    g.userData.update = t => { for (const { p, sx, i } of ps) p.rotation.y = sx * (0.12 + shake(o.rattle, t - i * 0.03, 0.18, 38, 5)); }; g.userData.update(0); return g; },
  // A big cat sitting (pivot at its feet, faces +Z): a grey tabby box body, a round head with ears, a curled tail; o.turn [[t, yaw]]: the head turns
  moCat(o) { const g = grp(), C = o.color || '#8A8F96', D = '#5E656D', hd = grp();
    g.add(at(box(0.36, 0.42, 0.5, C, { pivot: 'bottom', outline: 0.02, taper: 0.85 }), 0, 0, -0.05), at(box(0.38, 0.06, 0.52, D), 0, 0.2, -0.05), at(box(0.38, 0.06, 0.52, D), 0, 0.32, -0.05));
    const tl = at(new THREE.Mesh(new THREE.TorusGeometry(0.2, 0.04, 6, 12, PI * 1.2), mat(C)), 0.1, 0.08, -0.25, 0, PI / 2, 0); addOutline(tl, 0.04); g.add(tl);
    hd.position.set(0, 0.52, 0.12); g.add(hd); hd.add(at(box(0.3, 0.26, 0.26, C, { outline: 0.02 }), 0, 0, 0));
    for (const sx of [-1, 1]) hd.add(at(new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.12, 4), mat(C)), sx * 0.09, 0.17, 0), at(box(0.06, 0.07, 0.02, '#C8E06A', { emissive: '#4A6020' }), sx * 0.07, 0.03, 0.135), at(box(0.015, 0.05, 0.021, '#14161A'), sx * 0.07, 0.03, 0.137));
    hd.add(at(box(0.05, 0.03, 0.02, '#E8A0A0'), 0, -0.04, 0.135));
    g.userData.update = t => { hd.rotation.y = kv(o.turn, t, 0); hd.rotation.x = shake(o.flinch, t, 0.2, 30, 6); }; g.userData.update(0); return g; },
  // A big pigeon (pivot at its feet, faces +Z): a grey body, a green-violet neck, a small head with an orange eye; o.turn [[t, yaw]]: the head turns
  moPigeon(o) { const g = grp(), hd = grp(), body = new THREE.Mesh(new THREE.SphereGeometry(0.16, 12, 8), mat('#8E959E')); body.scale.set(0.9, 0.85, 1.3); body.position.y = 0.2; addOutline(body, 0.03); g.add(body);
    g.add(at(box(0.12, 0.05, 0.2, '#5E656D', { outline: 0.03 }), 0, 0.2, -0.22, 0.3, 0, 0), at(cyl(0.08, 0.1, 0.12, '#5E8C7A', 8), 0, 0.32, 0.08));
    for (const sx of [-1, 1]) g.add(at(cyl(0.01, 0.01, 0.1, '#D86A6A', 4, { pivot: 'bottom' }), sx * 0.05, 0, 0.02));
    hd.position.set(0, 0.42, 0.1); g.add(hd); hd.add(at(sphere(0.07, '#8E959E', 1, { outline: 0.04 }), 0, 0, 0), at(new THREE.Mesh(new THREE.ConeGeometry(0.018, 0.05, 5), mat('#3A3D44')), 0, -0.01, 0.08, PI / 2, 0, 0));
    for (const sx of [-1, 1]) hd.add(at(sphere(0.016, '#E8742A', 0), sx * 0.045, 0.015, 0.045));
    g.userData.update = t => { hd.rotation.y = kv(o.turn, t, 0); hd.position.y = 0.42 + shake(o.flinch, t, 0.04, 30, 6); }; g.userData.update(0); return g; },
  // A small truck with a crane boom and a giant boom microphone (pivot at the floor in the truck's middle, faces +X): a white cab and flatbed, a turret,
  // a telescopic boom from the turret to the mic; o.tip [[t, [x, y, z]], ...]: where the mic is (truck coordinates), eased between keys; the mic a big
  // grey fluffy windshield on a short handle
  moMicTruck(o) { const g = grp(), C = '#F4F1EA';
    g.add(at(box(3.2, 0.9, 1.9, C, { pivot: 'bottom', outline: 0.005 }), -0.4, 0.45, 0), at(box(1.3, 1.6, 1.9, C, { pivot: 'bottom', outline: 0.005 }), 1.7, 0.45, 0), at(box(0.9, 0.7, 1.92, '#9FC6D8', { emissive: '#3E6A7A' }), 1.9, 1.5, 0), at(box(3.2, 0.12, 1.92, '#3E7FB6'), -0.4, 1.0, 0));
    for (const x of [-1.4, 1.6]) for (const z of [-0.95, 0.95]) g.add(at(cyl(0.4, 0.4, 0.26, '#1E2024', 12), x, 0.4, z, PI / 2, 0, 0));
    const base = [-0.8, 1.6, 0]; g.add(at(cyl(0.35, 0.4, 0.3, '#8A8F96', 12, { outline: 0.01 }), base[0], 1.5, 0));
    const boom = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.1, 1, 8), mat('#E8B030')); addOutline(boom, 0.03); g.add(boom);
    const mic = grp(FLUFF(0.32, '#9AA0A6')); mic.children[0].scale.set(1.8, 1, 1); g.add(mic); mic.add(at(cyl(0.05, 0.05, 0.6, '#2A2C31', 6), -0.62, 0, 0, 0, 0, PI / 2));
    const T = o.tip || [[0, [0.5, 4, 0]]];
    const tipAt = t => { if (t <= T[0][0]) return T[0][1]; for (let i = 0; i < T.length - 1; i++) { const [a, pa] = T[i], [b, pb] = T[i + 1]; if (t < b) { const u = smooth((t - a) / (b - a)); return pa.map((v, j) => v + (pb[j] - v) * u); } } return T[T.length - 1][1]; };
    const A = new THREE.Vector3(...base), B = new THREE.Vector3(), E = new THREE.Vector3(), Y = new THREE.Vector3(0, 1, 0), X = new THREE.Vector3(1, 0, 0);
    // (round 1) the boom runs from the turret right into the mic's handle (it stopped short and the mic floated): the mic is turned along the boom
    g.userData.update = t => { const p = tipAt(t); B.set(p[0], p[1], p[2]); const dn = B.clone().sub(A).normalize(); E.copy(B).addScaledVector(dn, -0.85); const d = E.clone().sub(A), L = d.length();
      boom.position.copy(A).addScaledVector(d, 0.5); boom.scale.set(1, Math.max(0.1, L), 1); boom.quaternion.setFromUnitVectors(Y, d.clone().normalize());
      mic.position.copy(B); mic.quaternion.setFromUnitVectors(X, dn); mic.rotateX(0.06 * Math.sin(t * 7)); };
    g.userData.update(0); return g; },
  // A giant boom microphone alone (pivot at its middle, points along +X): a big grey fluffy windshield on a pole going back toward -X; o.sway: it hovers
  moMic(o) { const g = grp(), m = FLUFF(o.r ?? 0.32, '#9AA0A6'); m.children[0].scale.set(1.8, 1, 1); g.add(m, at(cyl(0.05, 0.05, o.pole ?? 2.5, '#2A2C31', 6), -(o.pole ?? 2.5) / 2 - 0.3, 0, 0, 0, 0, PI / 2));
    g.userData.update = t => { m.position.y = 0.03 * Math.sin(t * 3); g.rotation.z = shake(o.jolt, t, 0.15, 30, 5); }; g.userData.update(0); return g; },
  // Big studio headphones (attach to the head joint; pivot at the middle of the head): two dark cups on a band over the top; o.span, o.top
  moPhones(o) { const S = o.span ?? 0.24, T = o.top ?? 0.3, g = grp(); for (const sx of [-1, 1]) g.add(at(cyl(0.12, 0.12, 0.08, '#2A2C31', 14, { outline: 0.03 }), sx * S, 0, 0, 0, 0, PI / 2), at(cyl(0.09, 0.09, 0.02, '#C8322A', 12), sx * (S + 0.045), 0, 0, 0, 0, PI / 2));
    const band = new THREE.Mesh(new THREE.TorusGeometry(S, 0.03, 6, 18, PI), mat('#3A3D44')); band.scale.set(1, T / S, 1); addOutline(band, 0.04); g.add(band); return g; },
  // A landing papered with notes (pivot at the floor in the middle, faces +Z): a back wall o.w x o.h, side walls, a ceiling, all tiled with copies of the
  // note at slight angles (the wall seen through gaps), and a stair flight going up at the right, its steps covered too
  moPapered(o) { const W = o.w ?? 4.5, H = o.h ?? 3, D = o.d ?? 3, g = grp(), CW = '#E8E0D0';
    if (o.doorX != null) { const a0 = o.doorX - 0.55, a1 = o.doorX + 0.55; g.add(at(box(a0 + W / 2, H, 0.1, CW, { pivot: 'bottom' }), (a0 - W / 2) / 2, 0, -D / 2), at(box(W / 2 - a1, H, 0.1, CW, { pivot: 'bottom' }), (a1 + W / 2) / 2, 0, -D / 2), at(box(1.1, H - 2.2, 0.1, CW, { pivot: 'bottom' }), o.doorX, 2.2, -D / 2)); }
    else g.add(at(box(W, H, 0.1, CW, { pivot: 'bottom' }), 0, 0, -D / 2));
    g.add(at(box(0.1, H, D, CW, { pivot: 'bottom' }), -W / 2, 0, 0), at(box(0.1, H, D, CW, { pivot: 'bottom' }), W / 2, 0, 0), at(box(W, 0.1, D, CW), 0, H, 0));
    const tex = canvasPlane(0.42, 0.3, paintNote, { res: 256 }), geo = tex.geometry, m_ = tex.material;
    const put = (x, y, z, ry, rx, i) => { const n = new THREE.Mesh(geo, m_); n.position.set(x, y, z); n.rotation.set(rx, ry, 0.15 * (hsh(i) - 0.5)); g.add(n); };
    let i = 0; for (let y = 0.2; y < H; y += 0.27) for (let x = -W / 2 + 0.25; x < W / 2; x += 0.38) { if (o.doorX != null && Math.abs(x - o.doorX) < 0.55 && y < 2.2) continue; put(x + 0.04 * (hsh(i) - 0.5), y, -D / 2 + 0.06 + 0.002 * (i % 3), 0, 0, i++); }
    for (const sx of [-1, 1]) for (let y = 0.2; y < H; y += 0.27) for (let z = -D / 2 + 0.3; z < D / 2; z += 0.38) put(sx * (W / 2 - 0.06), y, z, -sx * PI / 2, 0, i++);
    for (let z = -D / 2 + 0.25; z < D / 2; z += 0.3) for (let x = -W / 2 + 0.25; x < W / 2; x += 0.4) put(x, H - 0.06, z, 0, PI / 2, i++);
    return g; },
  // An avalanche of notes sliding down (pivot at the floor where it lands, spreads toward +Z): o.n sheets that slide from o.from (local [x, y, z]) down
  // to a heap at the pivot, staggered from o.at over o.dur; the heap stays
  moAvalanche(o) { const n = o.n ?? 60, g = grp(), F = o.from || [0.8, 1.6, -1.2], t0 = o.at ?? 0, dur = o.dur ?? 1.0, tex = canvasPlane(0.42, 0.3, paintNote, { res: 256 }), sh = [], M = o.mound;
    // (round 1) o.mound {h, r}: the sheets land on a mound round the pivot (the man under it is buried); o.burst t: they fly out to a low ring round it
    for (let i = 0; i < n; i++) { const m = new THREE.Mesh(tex.geometry, tex.material); let end, ring = null;
      if (M) { const a = hsh(i) * TAU, rr = Math.sqrt(hsh(i + 2)) * M.r, top = M.h * (1 - (rr / M.r) ** 2); end = [Math.cos(a) * rr, 0.04 + Math.min(top, M.h * (0.12 + 0.88 * i / n)), Math.sin(a) * rr];
        const R2 = M.r * 1.25 + 0.35 * hsh(i + 6); ring = [Math.cos(a) * R2, 0.04 + 0.16 * hsh(i + 8) * (1 - Math.min(1, (R2 - M.r) / 0.6)), Math.sin(a) * R2]; }
      else end = [(hsh(i) - 0.5) * 1.6, 0.04 + Math.floor(i / 12) * 0.05 + 0.1 * hsh(i + 4) * (1 - Math.floor(i / 12) / 6), (hsh(i + 2) - 0.3) * 1.1];
      g.add(m); sh.push({ m, end, ring, ts: t0 + dur * (i / n), r: hsh(i + 7) }); }
    g.userData.update = t => { const b = o.burst != null ? smooth((t - o.burst) / 0.25) : 0;
      for (const { m, end, ring, ts, r } of sh) { const u = clamp01((t - ts) / 0.45); m.visible = t >= ts - 0.01 || o.preset; const p = o.preset ? 1 : u;
        let x = F[0] + (end[0] - F[0]) * p, y = F[1] + (end[1] - F[1]) * p + 0.3 * Math.sin(p * PI), z = F[2] + (end[2] - F[2]) * p;
        if (ring && b > 0) { x += (ring[0] - end[0]) * b; y += (ring[1] - end[1]) * b + 0.45 * Math.sin(b * PI); z += (ring[2] - end[2]) * b; }
        m.position.set(x, y, z); m.rotation.set(-PI / 2 + 0.6 * (r - 0.5) + (1 - p) * 2 * r + b * (1 - b) * 4 * r, r * TAU, 0.3 * (r - 0.5) * (1 - p)); } };
    g.userData.update(0); return g; },
  // A stair flight going up (pivot at the bottom step's front middle, rises toward -Z and +Y): o.n steps of o.w, a handrail
  moStairs(o) { const n = o.n ?? 8, w = o.w ?? 1.1, g = grp(); for (let i = 0; i < n; i++) g.add(at(box(w, 0.18, 0.3, i % 2 ? '#B9A58A' : '#C4B096', { pivot: 'bottom', outline: 0.006 }), 0, i * 0.18, -i * 0.28));
    g.add(at(box(0.05, 0.05, n * 0.3, '#5A3E28'), w / 2, 0.95 + n * 0.09, -n * 0.14, Math.atan2(0.18, 0.28), 0, 0)); return g; },
  moSmear(o) {   // (round 1) speed lines behind a fast rise (pivot at the bottom middle, lines along +Y): at each o.at time five white lines show for o.dur (0.13) s, shoot up and shrink; o.h, o.w
    const g = grp(), H = o.h ?? 1.0, W = o.w ?? 0.6, D = o.dur ?? 0.13, ls = [];
    for (let i = 0; i < 5; i++) { const b = box(0.04, 1, 0.04, o.color || '#FFFFFF', { pivot: 'bottom', outline: 0.03, emissive: '#B8C4D4', noGrain: true }); b.position.set((i / 4 - 0.5) * W, 0, (hsh(i) - 0.5) * 0.15); g.add(b); ls.push({ b, l: H * (0.6 + 0.4 * hsh(i + 3)) }); }
    g.userData.update = t => { let u = -1; for (const t0 of o.at || []) { const v = (t - t0) / D; if (v >= 0 && v < 1) u = v; }
      for (const { b, l } of ls) { b.visible = u >= 0; if (u >= 0) { b.position.y = H * 0.5 * u; b.scale.y = Math.max(0.02, l * (1 - u)); } } };
    g.userData.update(0); return g; },
  moSnore(o) {   // (round 1) snore lines (pivot at the mouth): three wavy strokes rise and fan out at each o.at time, for 0.6 s; o.big: the index of a bigger one (no letters)
    const g = grp(), ws = [];
    for (let i = 0; i < 3; i++) { const pts = []; for (let j = 0; j <= 16; j++) { const u = j / 16; pts.push(new THREE.Vector3(Math.sin(u * TAU * 1.5) * 0.05, u * 0.32, 0)); }
      const tb = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 24, 0.016, 5), mat(o.color || '#3A4A6A')); g.add(tb); ws.push({ tb, i }); }
    g.userData.update = t => { let u = -1, big = 1; (o.at || []).forEach((t0, j) => { const v = (t - t0) / 0.6; if (v >= 0 && v < 1) { u = v; big = j === o.big ? 1.5 : 1; } });
      for (const { tb, i } of ws) { tb.visible = u >= 0; if (u >= 0) { const s = (0.5 + 0.9 * u) * big; tb.position.set((i - 1) * 0.12 * (1 + u) * big, 0.05 + 0.35 * u * big, 0); tb.rotation.z = -(i - 1) * 0.4; tb.scale.setScalar(s); } } };
    g.userData.update(0); return g; },
  moHat(o) {   // (round 1) a farmer's straw hat (attach to the head joint; pivot at the brim): o.nod [t, ...]: it lifts and flaps a beat after each nod (overlap)
    const g = grp(), h = grp(); g.add(h);
    h.add(at(cyl(0.4, 0.4, 0.03, '#E8C878', 18, { outline: 0.02 }), 0, 0, 0), at(cyl(0.2, 0.23, 0.2, '#E8C878', 14, { pivot: 'bottom', outline: 0.02 }), 0, 0.01, 0), at(cyl(0.235, 0.235, 0.05, '#8A4A2E', 14), 0, 0.05, 0));
    g.userData.update = t => { let y = 0, rx = 0; for (const t0 of o.nod || []) { const u = t - t0 - 0.08; if (u > 0 && u < 0.8) { const e = Math.exp(-6 * u); y += 0.09 * e * Math.max(0, Math.sin(Math.min(1, u / 0.1) * PI / 2)); rx += -0.35 * e * Math.sin(u * 16); } } h.position.y = y; h.rotation.x = rx; };
    g.userData.update(0); return g; },
  moCap(o) {   // (round 1) a plain peaked cap (attach to the head joint; pivot at its band's bottom): a dark crown, a band, a black peak; no badge, no braid
    const C = o.color || '#1E2A44';
    return grp(at(box(0.46, 0.14, 0.46, C, { outline: 0.02, taper: 1.14 }), 0, 0.11, 0), at(box(0.42, 0.07, 0.42, '#14182A', { outline: 0.02 }), 0, 0.035, 0), at(box(0.38, 0.025, 0.2, '#14161A', { outline: 0.02 }), 0, 0.0, 0.27, 0.22, 0, 0)); },
  moBarrier(o) {   // (round 1) queue barriers (pivot at the floor): o.lines [[x0, z0, x1, z1], ...]: chrome posts with a red belt between them, a zigzag lane
    const g = grp();
    for (const [x0, z0, x1, z1] of o.lines || []) { const L = Math.hypot(x1 - x0, z1 - z0), n = Math.max(1, Math.round(L / 0.9));
      for (let i = 0; i <= n; i++) { const x = x0 + (x1 - x0) * i / n, z = z0 + (z1 - z0) * i / n; g.add(at(cyl(0.03, 0.03, 0.95, '#C9CED4', 8, { pivot: 'bottom', outline: 0.02 }), x, 0, z), at(cyl(0.13, 0.15, 0.04, '#5E656D', 12), x, 0.02, z)); }
      const b = at(box(L, 0.06, 0.012, o.color || '#C8322A', { outline: 0.02 }), (x0 + x1) / 2, 0.88, (z0 + z1) / 2); b.rotation.y = -Math.atan2(z1 - z0, x1 - x0); g.add(b); }
    return g; },
};
