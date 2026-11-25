// « Le pardon » (story 103, cycle 55): this man said « pardon » in the street and the president pardoned him; of what, nobody knew. You cannot pardon
// an innocent, so he was tried for nothing, condemned at noon, pardoned at one past; every « pardon » became a plea, the metro became a court, the
// prisons emptied, the minister banned the word. The president never said pardon: he was the one who bumped him.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time. Every name
// starts with `pd` (props.js merges all the story tables into one: a plain name could override another story's). No word, no figure, no flag drawn.
import * as THREE from 'three';
import { box, cyl, sphere, mat, addOutline } from './style.js';
import { grp, at, canvasPlane, rod } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = x => { const u = clamp01(x), c = 1.70158; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const noShadow = m => { m.traverse(c => { c.castShadow = false; }); return m; };
// a value keyed in time: keys [[t, v], ...] (sorted), eased (smoothstep) between keys; a plain number is a constant
function kv(keys, t, def = 0) {
  if (keys == null) return def;
  if (typeof keys === 'number') return keys;
  if (!keys.length) return def;
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) { const [a, va] = keys[i], [b, vb] = keys[i + 1]; if (t < b) return va + (vb - va) * smooth((t - a) / Math.max(1e-4, b - a)); }
  return keys[keys.length - 1][1];
}
const popS = (t, t0, d = 0.22) => t < t0 ? 0 : outBack((t - t0) / d);
const wrap01 = x => ((x % 1) + 1) % 1;
// a dusk picture (canvas): an orange-to-rose sky, a row of dark-blue roofs with lit yellow windows (never a black night)
function paintDusk(c, W, H, seed = 1, country = false) {
  const g = c.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#E8794A'); g.addColorStop(0.45, '#F4A25A'); g.addColorStop(0.75, '#F7C27A'); g.addColorStop(1, '#F2D49A');
  if (seed < 0) { const d = c.createLinearGradient(0, 0, 0, H); d.addColorStop(0, '#5FA8E0'); d.addColorStop(1, '#BFE0F4'); c.fillStyle = d; c.fillRect(0, 0, W, H); } else { c.fillStyle = g; c.fillRect(0, 0, W, H); }   // a negative seed: the same country by day
  if (country) {   // low hills, fields, hedges and a few far houses with lit windows
    c.fillStyle = '#7A6A5A'; c.beginPath(); c.moveTo(0, H); for (let q = 0; q <= 10; q++) c.lineTo(W * q / 10, H * (0.72 + 0.05 * Math.sin(q * 1.7 + seed))); c.lineTo(W, H); c.fill();
    c.fillStyle = '#5E7A4A'; c.fillRect(0, H * 0.82, W, H * 0.18); c.fillStyle = '#4A6A3A'; for (let q = 0; q < 14; q++) { c.beginPath(); c.ellipse(W * (q + 0.5) / 14, H * 0.82, W * 0.04, H * 0.025, 0, 0, TAU); c.fill(); }
    for (let q = 0; q < 5; q++) { const hx = W * (0.1 + 0.2 * q + 0.05 * hsh(q + seed)), hy = H * (0.74 + 0.03 * hsh(q + 3)), hw = W * 0.035, hh = H * 0.035; c.fillStyle = '#5A4A5E'; c.fillRect(hx, hy - hh, hw, hh); c.beginPath(); c.moveTo(hx - 2, hy - hh); c.lineTo(hx + hw / 2, hy - hh * 1.7); c.lineTo(hx + hw + 2, hy - hh); c.fill(); c.fillStyle = '#FFD878'; c.fillRect(hx + hw * 0.2, hy - hh * 0.7, hw * 0.25, hh * 0.3); c.fillRect(hx + hw * 0.6, hy - hh * 0.7, hw * 0.25, hh * 0.3); }
    return; }
  let x = 0, i = 0; while (x < W) { const bw = W * (0.08 + 0.08 * hsh(seed + i)), bh = H * (0.16 + 0.14 * hsh(seed + i + 7)); c.fillStyle = i % 2 ? '#4A3A5E' : '#3E3354';
    c.fillRect(x, H - bh, bw, bh); c.beginPath(); c.moveTo(x - 2, H - bh); c.lineTo(x + bw / 2, H - bh - H * 0.05); c.lineTo(x + bw + 2, H - bh); c.fill();
    c.fillStyle = '#FFD878'; for (let r = 0; r < 3; r++) for (let q = 0; q < 2; q++) if (hsh(seed + i * 9 + r * 3 + q) > 0.35) c.fillRect(x + bw * (0.2 + 0.42 * q), H - bh + bh * (0.18 + 0.27 * r), bw * 0.2, bh * 0.13);
    x += bw; i++; }
}


// the huge lemon-yellow tie with big polka dots (pivot at its knot, hangs down -Y, faces +Z); L its length
function TIE(L = 0.6) {
  const g = grp(), w = L * 0.36;
  const knot = new THREE.Mesh(new THREE.BoxGeometry(w * 0.55, w * 0.5, 0.05), mat('#F2DC2E')); addOutline(knot, 0.03); g.add(knot);
  const blade = canvasPlane(w, L, (c, W, H) => { c.fillStyle = '#F4E030'; c.beginPath(); c.moveTo(W * 0.3, 0); c.lineTo(W * 0.7, 0); c.lineTo(W, H * 0.86); c.lineTo(W * 0.5, H); c.lineTo(0, H * 0.86); c.closePath(); c.fill();
    c.lineWidth = W * 0.04; c.strokeStyle = '#2A2A20'; c.stroke(); c.save(); c.clip(); c.fillStyle = '#1E3A8A';
    for (let r = 0; r < 6; r++) for (let q = 0; q < 3; q++) { c.beginPath(); c.arc(W * (0.18 + 0.32 * q + (r % 2) * 0.16), H * (0.1 + 0.15 * r), W * 0.09, 0, TAU); c.fill(); } c.restore(); }, { res: 256, transparent: true });
  blade.position.set(0, -L / 2 - w * 0.2, 0.03); g.add(blade);
  return g;
}
// a parchment scroll face (canvas): cream paper, curled ends, wavy ink lines (no letter), a red wax seal at the bottom
function paintScroll(c, W, H) { c.fillStyle = '#F2E2B8'; c.fillRect(0, 0, W, H); c.strokeStyle = '#6A4A2A'; c.lineWidth = W * 0.012;
  for (let i = 0; i < 7; i++) { c.beginPath(); const y = H * (0.14 + 0.09 * i); c.moveTo(W * 0.14, y); for (let x = 0.14; x <= 0.86; x += 0.04) c.lineTo(W * x, y + H * 0.008 * Math.sin(x * 40 + i)); c.stroke(); }
  c.fillStyle = '#B5241E'; c.beginPath(); c.arc(W * 0.5, H * 0.84, W * 0.1, 0, TAU); c.fill(); c.fillStyle = '#8A1812'; c.beginPath(); c.arc(W * 0.5, H * 0.84, W * 0.055, 0, TAU); c.fill(); }
// A rolled scroll (pivot at its middle, along X): a cream tube with spiral ends and a red ribbon with a seal
function ROLL(L = 0.42, r = 0.06) { const g = grp(), t = new THREE.Mesh(new THREE.CylinderGeometry(r, r, L, 12), mat('#F2E2B8')); t.rotation.z = PI / 2; addOutline(t, 0.02); g.add(t);
  for (const sx of [-1, 1]) g.add(at(cyl(r * 0.55, r * 0.55, 0.012, '#C9A86A', 10), sx * (L / 2 + 0.004), 0, 0, 0, 0, PI / 2), at(cyl(r * 0.2, r * 0.2, 0.014, '#8A6A3A', 8), sx * (L / 2 + 0.006), 0, 0, 0, 0, PI / 2));
  g.add(at(cyl(r * 1.06, r * 1.06, 0.05, '#C8322A', 12), 0, 0, 0, 0, 0, PI / 2), at(cyl(r * 0.45, r * 0.45, 0.02, '#9A1E18', 10), 0, 0, r * 1.05, PI / 2, 0, 0)); return g; }
export const PARDON_PROPS = {
  // The president (his own round model, not a human rig; pivot at the floor between his feet, faces +Z): a barrel body in a dark suit with a white
  // shirt V and a tie, short legs, short arms with round hands, a big round kindly head (pink cheeks, little eyes, a wide smile, grey side hair).
  // o.round: how round (1 = round, 1.4 = ten kilos more); o.pj: pyjamas (pale blue stripes, no tie); o.sit: seated (legs forward, body lower by
  // o.seatY under his standing hip); o.walk [t0, t1, freq]: a waddle (legs, sway, bob); o.wave [[t0, t1], ...]: his right hand waves side to side
  // at shoulder height (never at the forehead); o.pat [t, ...]: his right hand pats down in front at o.patAt [x, y, z] (relative); o.bounce [t, ...]:
  // a squash-stretch bounce on each time; o.look [[t, yaw], ...]: his head turns; o.smile [[t, 0..1]]: beaming; o.blink [t, ...]; o.pop: the
  // button that pops (hidden after o.popAt); the huge lemon polka-dot tie (o.flap: it flaps, strides per second); o.sign [[t0, t1]]: his right hand
  // scribbles in front; o.raise [[t0, t1]]: his right arm up at the side; o.hold [[t0, t1]]: both arms up in front; o.straighten [[t0, t1]]: both hands
  // at the tie, it wags then sits straight; o.puff [t]: the chest swells and settles; o.signUp [[t0, t1]]: scribbles up by his shoulder
  pdPresident(o) {
    const k = o.round ?? 1, SU = o.pj ? '#A9C2E2' : (o.suit || '#2B3A55'), g = grp(), root = grp(); g.add(root);
    const bodyR = 0.42 * k, hipY = o.sit ? 0.5 : 0.62, legL = 0.5;
    const body = grp(); body.position.y = hipY + bodyR * 0.9; root.add(body);
    const torso = new THREE.Mesh(new THREE.SphereGeometry(bodyR, 18, 14), mat(SU)); torso.scale.set(1.05, 1.15, 0.95); addOutline(torso, 0.012); body.add(torso);
    if (o.pj) for (let i = -3; i <= 3; i++) { const st = new THREE.Mesh(new THREE.TorusGeometry(bodyR * Math.sqrt(1 - (i / 4) ** 2) * 1.04, 0.012, 4, 24), mat('#F4F6FA')); st.rotation.x = PI / 2; st.position.y = i * bodyR * 0.27; st.scale.set(1.05, 0.95, 1); body.add(st); }
    else { const v = new THREE.Mesh(new THREE.ConeGeometry(bodyR * 0.36, bodyR * 0.9, 3), mat('#F2F2EE')); v.rotation.set(PI, 0, 0); v.position.set(0, bodyR * 0.55, bodyR * 0.82); v.scale.set(1, 1, 0.3); body.add(v);
      const tie = TIE(bodyR * 1.15); tie.position.set(0, bodyR * 0.85, bodyR * 0.9); tie.rotation.x = -0.32; body.add(tie); body.userData.tie = tie; }   // the huge lemon polka-dot tie
    const btn = at(cyl(0.035, 0.035, 0.015, o.pj ? '#F4F6FA' : '#1A1C20', 12, { outline: 0.04 }), 0, -bodyR * 0.15, bodyR * 0.96, PI / 2 - 0.1, 0, 0); body.add(btn);
    const head = grp(); head.position.y = bodyR * 1.05; body.add(head);
    const hd = new THREE.Mesh(new THREE.SphereGeometry(0.27, 18, 14), mat('#F2C29A')); hd.scale.set(1.08, 1, 1); hd.position.y = 0.24; addOutline(hd, 0.015); head.add(hd);
    const face = canvasPlane(0.4, 0.3, (c, W, H) => { c.clearRect(0, 0, W, H);
      c.fillStyle = 'rgba(232,110,110,0.55)'; for (const x of [0.2, 0.8]) { c.beginPath(); c.ellipse(W * x, H * 0.62, W * 0.09, H * 0.08, 0, 0, TAU); c.fill(); }
      c.strokeStyle = '#3A2A20'; c.lineWidth = W * 0.022; c.lineCap = 'round'; for (const x of [0.33, 0.67]) { c.beginPath(); c.arc(W * x, H * 0.42, W * 0.05, PI * 1.1, PI * 1.9); c.stroke(); }   // kind closed-ish eyes
      c.beginPath(); c.arc(W * 0.5, H * 0.55, W * 0.16, PI * 0.15, PI * 0.85); c.stroke();   // a wide smile
      c.fillStyle = '#E8A27A'; c.beginPath(); c.ellipse(W * 0.5, H * 0.52, W * 0.05, H * 0.06, 0, 0, TAU); c.fill();
      c.strokeStyle = '#6A6A6A'; c.lineWidth = W * 0.02; for (const x of [0.33, 0.67]) { c.beginPath(); c.moveTo(W * x - W * 0.06, H * 0.28); c.lineTo(W * x + W * 0.06, H * 0.26); c.stroke(); } }, { res: 256, transparent: true });
    face.position.set(0, 0.25, 0.268); head.add(face);
    const eyesOpen = canvasPlane(0.24, 0.08, (c, W, H) => { c.clearRect(0, 0, W, H); c.fillStyle = '#2A1E16'; for (const x of [0.2, 0.8]) { c.beginPath(); c.arc(W * x, H * 0.5, H * 0.35, 0, TAU); c.fill(); } }, { res: 128, transparent: true }); eyesOpen.position.set(0, 0.255, 0.275); head.add(eyesOpen);
    for (const sx of [-1, 1]) head.add(at(sphere(0.07, '#B9B9B6', 1), sx * 0.26, 0.28, -0.02), at(sphere(0.05, '#F2C29A', 0), sx * 0.29, 0.22, 0.02));   // grey side hair, ears
    head.add(at(sphere(0.12, '#B9B9B6', 1), 0, 0.46, -0.1));
    const arms = [-1, 1].map(sx => { const sh = grp(); sh.position.set(sx * bodyR * 0.82, bodyR * 0.35, 0);   // (inside the barrel: a raised arm stays joined to it)
      body.add(sh);
      const ar = at(cyl(0.07, 0.065, 0.42, SU, 8, { outline: 0.02 }), 0, -0.2, 0); sh.add(ar); sh.add(at(sphere(0.075, '#F2C29A', 1, { outline: 0.03 }), 0, -0.44, 0)); sh.rotation.z = sx * 0.35; return sh; });
    const legs = [-1, 1].map(sx => { const hp = grp(); hp.position.set(sx * bodyR * 0.42, hipY, 0); root.add(hp);
      hp.add(at(cyl(0.1, 0.09, legL, o.pj ? SU : (o.pants || SU), 8, { outline: 0.02 }), 0, -legL / 2, 0), at(box(0.16, 0.08, 0.26, '#1A1C20', { outline: 0.02 }), 0, -legL + 0.02 - (o.sit ? 0 : 0.08), 0.06)); return hp; });
    if (o.sit) legs.forEach(l => { l.rotation.x = -PI / 2 + 0.1; });
    g.userData.update = t => {
      let bob = 0, sway = 0, sqy = 1;
      const W = o.walk; if (W && t >= W[0] && t <= W[1]) { const ph = (t - W[0]) * TAU * (W[2] ?? 1.8); legs.forEach((l, i) => { l.rotation.x = 0.5 * Math.sin(ph + i * PI); }); bob = 0.03 * Math.abs(Math.sin(ph)); sway = 0.08 * Math.sin(ph); }
      for (const b of o.puff || []) { const u = t - b; if (u >= 0 && u < 0.9) sqy *= 1 + 0.14 * Math.sin(Math.min(1, u / 0.25) * PI / 2) * (u < 0.5 ? 1 : 1 - (u - 0.5) / 0.4) + 0.03 * Math.exp(-6 * u) * Math.sin(u * 25); }   // o.puff [t]: the chest swells proudly and settles
      for (const b of o.bounce || []) { const u = t - b; if (u >= 0 && u < 0.3) sqy *= 1 - 0.18 * Math.exp(-9 * u) * Math.cos(u * 30); }
      sqy *= 1 + 0.018 * Math.sin(t * 4.2); head.position.y = bodyR * 1.05 + 0.012 * Math.sin(t * 4.2 + 0.6);   // always breathing
      root.position.y = bob; root.rotation.z = sway; body.scale.set(1 / Math.sqrt(sqy), sqy, 1 / Math.sqrt(sqy));
      head.rotation.y = kv(o.look, t, 0);
      arms[1].rotation.set(0, 0, 0.35); arms[0].rotation.set(0, 0, -0.35);
      for (const [a, b] of o.wave || []) if (t >= a && t <= b) { const u = Math.min(1, (t - a) / 0.15); arms[0].rotation.set(0, 0, -(0.35 + 2.1 * u) + 0.35 * u * Math.sin((t - a) * 14)); }   // his right arm (at -X) up to the side, waving
      const pa = o.patArm === 'L' ? 1 : 0, sg = pa ? 1 : -1; for (const p of o.pat || []) { const u = t - p; if (u >= -0.3 && u < 0) { const f = (u + 0.3) / 0.3; arms[pa].rotation.set(-0.2 * f, 0, sg * (0.35 + 0.8 * Math.sin(f * PI * 0.6))); }   // the arm arcs up and out...
        else if (u >= 0 && u < 0.3) arms[pa].rotation.set(-0.3, 0, sg * (0.55 + 0.08 * Math.exp(-10 * u) * Math.sin(u * 40))); }   // ...and lands on the case beside him with a little bounce
      if (o.restAt != null && t >= o.restAt) arms[pa].rotation.set(-0.3, 0, sg * 0.55);   // o.restAt: his hand stays on the case
      if (o.carry) { arms[0].rotation.set(0, 0, -0.18); arms[1].rotation.set(0, 0, 0.18); }   // o.carry: both arms down, a case in each hand
      for (const [a, b] of o.sign || []) if (t >= a && t <= b) arms[0].rotation.set(-1.25 + 0.12 * Math.sin((t - a) * 26), 0.15 * Math.sin((t - a) * 13), -0.15);   // o.sign: his right hand scribbles in front of him
      for (const [a, b] of o.raise || []) if (t >= a && t <= b) { const u = Math.min(1, (t - a) / 0.15); arms[0].rotation.set(0, 0, -(0.35 + 1.65 * u)); }   // o.raise: his right arm up at the side (holds a scroll up beside his head)
      for (const [a, b] of o.hold || []) if (t >= a && t <= b) { arms[0].rotation.set(-2.2, 0, -0.25); arms[1].rotation.set(-2.2, 0, 0.25); }   // o.hold: both arms up in front (holds a scroll up to us)
      for (const [a, b] of o.straighten || []) if (t >= a && t <= b) { const u = (t - a) / (b - a); arms[0].rotation.set(-1.6, 0.3, -0.5); arms[1].rotation.set(-1.4, -0.3, 0.5); arms[0].rotation.x += 0.25 * Math.sin(u * PI * 4); arms[1].rotation.x += 0.25 * Math.sin(u * PI * 4); if (body.userData.tie) { body.userData.tie.rotation.z = 0.5 * Math.sin(u * PI * 4) * (1 - u); body.userData.tie.scale.y = 1 + 0.12 * Math.abs(Math.sin(u * PI * 4)) * (1 - u); } }   // o.straighten: both hands tug at the tie, it wags then sits straight
      for (const [a, b] of o.signUp || []) if (t >= a && t <= b) arms[0].rotation.set(-2.75 + 0.15 * Math.sin((t - a) * 24), 0.2 * Math.sin((t - a) * 12), -0.25);   // o.signUp: his right hand up by his shoulder, scribbling on a scroll held there
      if (body.userData.tie && o.flap) body.userData.tie.rotation.set(-0.32 - 0.25 * Math.abs(Math.sin(t * o.flap * PI)), 0, 0.2 * Math.sin(t * o.flap * PI * 2));   // o.flap: the tie flaps as he strides
      const sm = kv(o.smile, t, 0.6); face.scale.set(1, 1, 1); eyesOpen.visible = !(o.blink || []).some(b => t >= b && t < b + 0.1) && sm < 0.85;
      btn.visible = !(o.popAt != null && t >= o.popAt);
    };
    g.userData.update(-1); return g;
  },

  // A plain room (pivot at the middle of its floor; back wall at z = -o.d/2, open toward +Z): floor, back and two side walls, a skirting board;
  // o.w / o.d / o.h, o.wall / o.floor colours; o.window { x, y, w, h, dusk }: a window in the back wall (a pale sky, or the dusk picture)
  pdRoom(o) {
    const W = o.w ?? 6, D = o.d ?? 5, H = o.h ?? 3, WC = o.wall || '#E9DCC8', g = grp(), bz = -D / 2;
    const fl = new THREE.Mesh(new THREE.PlaneGeometry(W, D), mat(o.floor || '#C79E72')); fl.rotation.x = -PI / 2; fl.position.y = 0.025; fl.receiveShadow = true; g.add(fl);   // (lifted clear of a set's own floor: no z-fight flashes)
    g.add(at(box(W, H, 0.12, WC, { pivot: 'bottom' }), 0, 0, bz - 0.06), at(box(0.12, H, D, WC, { pivot: 'bottom' }), -W / 2, 0, 0), at(box(0.12, H, D, WC, { pivot: 'bottom' }), W / 2, 0, 0));
    g.add(at(box(W, 0.12, 0.03, o.trim || '#F4EEE2'), 0, 0.06, bz + 0.015));
    if (o.window) { const q = o.window, ww = q.w ?? 1.2, wh = q.h ?? 1.2, wx = q.x ?? 0, wy = q.y ?? 1.6;
      const pic = canvasPlane(ww, wh, (c, Wc, Hc) => { if (q.dusk) paintDusk(c, Wc, Hc, 3); else { c.fillStyle = '#BFE0F2'; c.fillRect(0, 0, Wc, Hc); } }, { res: 256, emissive: 0.9 }); pic.position.set(wx, wy, bz + 0.005); g.add(pic);
      for (const [dx, dy, bw, bh] of [[0, wh / 2, ww + 0.1, 0.08], [0, -wh / 2, ww + 0.2, 0.08], [-ww / 2, 0, 0.08, wh], [ww / 2, 0, 0.08, wh], [0, 0, 0.05, wh]]) g.add(at(box(bw, bh, 0.06, '#F4EEE2', { outline: 0.006 }), wx + dx, wy + dy, bz + 0.03)); }
    return g;
  },

  // A bakery front (pivot at the floor in the middle, faces +Z): a cream facade, a striped awning, a window full of loaves, an open dark doorway
  // (x = o.doorX), no name; o.w
  pdBakery(o) {
    const w = o.w ?? 7, dx = o.doorX ?? 0, g = grp();
    for (const [x0, x1] of [[-w / 2, dx - 0.65], [dx + 0.65, w / 2]]) g.add(at(box(x1 - x0, 4.2, 0.3, '#F2E2C2', { pivot: 'bottom', outline: 0.005 }), (x0 + x1) / 2, 0, -0.15));
    g.add(at(box(1.3, 1.85, 0.3, '#F2E2C2', { pivot: 'bottom' }), dx, 2.35, -0.15), at(box(1.2, 2.3, 0.05, '#2A1E16'), dx, 1.15, -0.25));
    for (let i = 0; i < 12; i++) g.add(at(box(w / 12, 0.08, 0.9, i % 2 ? '#F4F1EA' : '#C8322A', { outline: 0.006 }), -w / 2 + (i + 0.5) * w / 12, 2.75, 0.35, -0.35, 0, 0));
    for (const sx of [-1, 1]) { const wx = dx + sx * 2.0; g.add(at(box(1.8, 1.3, 0.05, '#FFE9B8', { emissive: '#8A6A2A', noGrain: true }), wx, 1.4, 0.02), at(box(1.9, 0.08, 0.2, '#7A5A3C'), wx, 0.75, 0.08));
      for (let i = 0; i < 5; i++) g.add(at(cyl(0.05, 0.045, 0.6, '#D9A35C', 8, { outline: 0.02 }), wx - 0.6 + i * 0.3, 1.0 + 0.3 * (i % 2), 0.1, 0.3, 0, PI / 2 - 0.4)); }
    return g;
  },
  // The huge lemon polka-dot tie alone (attach to a torso joint; pivot at its knot, hangs -Y, faces +Z); o.L its length; o.flap: it flaps
  pdTie(o) { const g = grp(), t = TIE(o.L ?? 0.6); g.add(t); g.userData.update = tt => { if (o.flap) t.rotation.set(-0.15 - 0.3 * Math.abs(Math.sin(tt * o.flap * PI)), 0, 0.25 * Math.sin(tt * o.flap * PI * 2)); }; g.userData.update(0); return g; },

  // A headless dark-suited torso that barges in (pivot at the floor under it, faces +Z): a dark jacket block on legs, white shirt V, the huge lemon
  // polka-dot tie flapping, a shoulder; used where the face must stay out of frame (the top is cut by the frame); o.round (1)
  pdTorso(o) {
    const k = o.round ?? 1, g = grp(), b = grp(); g.add(b);
    b.add(at(box(0.85 * k, 1.1, 0.55 * k, '#22283A', { pivot: 'bottom', outline: 0.01 }), 0, 0.9, 0), at(box(0.8 * k, 0.12, 0.5 * k, '#1A1E2C'), 0, 2.0, 0));
    const v = new THREE.Mesh(new THREE.ConeGeometry(0.17, 0.45, 3), mat('#F2F2EE')); v.rotation.x = PI; v.position.set(0, 1.78, 0.28 * k); v.scale.set(1, 1, 0.3); b.add(v);
    for (const sx of [-1, 1]) b.add(at(cyl(0.1, 0.1, 0.9, '#22283A', 8, { pivot: 'bottom', outline: 0.02 }), sx * 0.22, 0, 0), at(cyl(0.11, 0.1, 0.8, '#22283A', 8, { outline: 0.02 }), sx * 0.52 * k, 1.5, 0, 0, 0, sx * 0.12));
    const tie = TIE(0.75); tie.position.set(0, 1.95, 0.29 * k); b.add(tie);
    g.userData.update = t => { tie.rotation.set(-0.15 - 0.35 * Math.abs(Math.sin(t * 7)), 0, 0.3 * Math.sin(t * 9));
      const h = o.hitAt != null ? t - o.hitAt : -1; b.rotation.z = h > 0 && h < 0.3 ? 0.15 * Math.sin(h / 0.3 * PI) : 0; b.rotation.y = o.turn ?? 0; };
    g.userData.update(-1); return g;
  },

  // A long baguette (pivot at its middle, along X): a thick golden crust with dark scoring; at o.snapAt it first bends and stretches (2-3 frames),
  // then breaks in two with a crack: the halves tip apart showing a torn pale crumb end, a burst of crumbs; o.half 'L' | 'R': one half alone, its
  // torn end at x = 0
  pdBaguette(o) {
    const L = o.len ?? 0.7, R = o.r ?? 0.058, CR = '#C9873A', g = grp(), all = grp(), halves = []; g.add(all);
    for (const sd of [-1, 1]) { if (o.half && (o.half === 'L') !== (sd < 0)) continue; const h = grp();
      const m = new THREE.Mesh(new THREE.CylinderGeometry(R, R, L / 2 - 0.04, 10), mat(CR)); m.rotation.z = PI / 2; m.position.x = sd * (L / 4 + 0.02); m.scale.set(1, 1, 0.82); addOutline(m, 0.02); h.add(m);
      const tip = new THREE.Mesh(new THREE.SphereGeometry(R, 10, 8), mat(CR)); tip.scale.set(1.3, 1, 0.82); tip.position.x = sd * (L / 2 - 0.02); addOutline(tip, 0.02); h.add(tip);
      for (let i = 0; i < 3; i++) h.add(at(box(0.07, 0.012, 0.032, '#8A5424'), sd * (L * 0.09 + i * 0.085), R * 0.8, 0, 0, 0.55 * sd, 0.12));   // the scoring
      for (let i = 0; i < 7; i++) { const a = i / 7 * TAU; h.add(at(box(0.03, 0.03, 0.03, i % 2 ? '#F4E6C2' : '#E9D3A0'), sd * (0.02 + 0.012 * (i % 3)), Math.cos(a) * R * 0.55, Math.sin(a) * R * 0.45, a, a, 0)); }   // the torn crumb end
      h.add(at(cyl(R * 0.85, R * 0.85, 0.02, '#F4E6C2', 10), sd * 0.025, 0, 0, 0, 0, PI / 2)); all.add(h); halves.push({ h, sd }); }
    const crumbs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map(i => { const m = at(box(0.04, 0.03, 0.035, i % 3 ? '#E9D3A0' : CR, { outline: 0.03 }), 0, 0, 0); g.add(m); return m; });
    g.userData.update = t => { const u = o.snapAt != null ? t - o.snapAt : -1;
      if (!o.half) { const pre = o.snapAt != null && u > -0.1 && u <= 0 ? 1 + u / 0.1 : 0;   // the bend and stretch just before the crack
        all.scale.set(1 + 0.18 * pre, 1 - 0.12 * pre, 1); all.rotation.z = 0;
        const k = u > 0 ? outBack(u / 0.16) : 0;
        for (const { h, sd } of halves) { h.rotation.z = -sd * (0.18 * pre + 0.95 * k); h.position.set(sd * 0.05 * k, 0.04 * pre - 0.03 * k, 0); } }
      crumbs.forEach((m, i) => { const du = u - 0.008 * i; m.visible = du > 0 && du < 0.8 && !o.half; if (!m.visible) return; const a = i / 10 * TAU; m.position.set(Math.cos(a) * 0.6 * du, 1.3 * du - 3.2 * du * du, Math.sin(a) * 0.35 * du + 0.06); m.rotation.set(du * 9, du * 6, 0); }); };
    g.userData.update(-1); return g;
  },

  // A big parchment scroll (pivot at its middle, faces +Z, upright): a sheet with curled rods top and bottom, wavy ink lines, a red wax seal;
  // o.w / o.h; o.signAt: signature strokes; o.xAt: a big red X stamps across it DIAGONALLY (two diagonal strokes, never upright), slamming down with a squash
  pdScroll(o) {
    const w = o.w ?? 0.5, h = o.h ?? 0.7, g = grp(), k = grp(); g.add(k);
    k.add(canvasPlane(w, h, paintScroll, { res: 256 }));
    for (const y of [h / 2, -h / 2]) k.add(at(cyl(0.035, 0.035, w + 0.08, '#E2CC98', 10, { outline: 0.03 }), 0, y, 0.02, 0, 0, PI / 2));
    const sigs = (o.signAt || []).map((ts, i) => { const m = at(box(w * (0.22 + 0.06 * i), 0.018, 0.01, '#14161A'), -w * 0.25 + i * w * 0.18, -h * 0.28 + 0.03 * Math.sin(i * 2), 0.012, 0, 0, (i % 2 ? -0.5 : 0.45)); k.add(m); return { m, ts }; });   // o.signAt [t, ...]: a signature stroke appears at each time
    let X = null;   // (a local: buildProp hoists this group's userData onto its wrapper, so g.userData is empty by the time update runs)
    if (o.xAt != null) { X = grp(); for (const sg of [-1, 1]) X.add(at(box(Math.hypot(w, h) * 0.85, 0.07, 0.02, '#D8262E', { outline: 0.02 }), 0, 0, 0.04, 0, 0, sg * Math.atan2(h, w))); k.add(X); }
    // the X falls from above the frame (o.xFrom m higher, 0.1 s), stretched in its fall, squashes flat on impact and bounces back to rest
    g.userData.update = t => { for (const { m, ts } of sigs) m.visible = t >= ts; if (X) { const u = t - o.xAt + 0.1; X.visible = u >= 0; if (u < 0) return; const F = o.xFrom ?? 1.4;
      if (u < 0.1) { const f = u / 0.1; X.position.y = F * (1 - f * f); X.scale.set(0.85, 1.35, 1); }
      else { const v = u - 0.1; X.position.y = 0.05 * Math.max(0, Math.sin(v * 22)) * Math.exp(-9 * v); const q = Math.exp(-12 * v) * Math.cos(v * 34); X.scale.set(1 + 0.35 * q, 1 - 0.4 * q, 1); } } };
    g.userData.update(-1); return g;
  },
  // A tall pile of rolled scrolls (pivot at the floor, faces +Z): neat rows of big rolls with spiral ends and red ribbons, a slight sag, up to o.h;
  // o.adds [t, ...]: one more roll pops on top at each time (squash on landing), o.perRow of them a row; o.w its width
  pdScrollPile(o) { const H = o.h ?? 2.6, W = o.w ?? 0.9, r = o.r ?? 0.065, g = grp(); let n = 0, top = 0;
    for (let y = r; y < H; y += r * 1.8) { const cols = Math.max(1, Math.round((W - 0.25 * (y / H)) / 0.15)); for (let c = 0; c < cols; c++) { const x = (c - (cols - 1) / 2) * 0.15 + ((n * 7) % 3 - 1) * 0.01;
        const R0 = ROLL(0.44, r); R0.position.set(x, y, 0.03 * Math.sin(n)); R0.rotation.y = 0.15 * Math.sin(n * 1.3); g.add(R0); n++; } top = y; }
    const extra = (o.adds || []).map((ta, i) => { const pr = o.perRow ?? 3, R1 = ROLL(0.44, r); R1.position.set(((i % pr) - (pr - 1) / 2) * 0.13, top + r * 1.8 * (1 + Math.floor(i / pr)), 0); g.add(R1); return { R1, ta }; });
    g.userData.update = t => { for (const { R1, ta } of extra) { const u = t - ta; R1.visible = u >= 0; const q = u > 0 ? Math.exp(-12 * u) * Math.cos(u * 30) : 0; R1.scale.set(1 + 0.3 * q, 1 - 0.35 * q, 1 + 0.3 * q); } };
    g.userData.update(-1); return g; },
  // A scroll conveyor (pivot at the floor in its middle, belt along X): a dark belt on legs, open parchments riding flat along it at o.speed m/s; each
  // one gets a black signature stroke as it passes x = o.signX (under the president's pen)
  pdConveyor(o) { const L = o.len ?? 3, g = grp(at(box(L, 0.1, 0.55, '#2A2C31', { outline: 0.01 }), 0, 0.85, 0)), sx0 = o.signX ?? 0;
    for (const x of [-L / 2 + 0.1, L / 2 - 0.1]) g.add(at(box(0.08, 0.85, 0.45, '#5E656D', { pivot: 'bottom' }), x, 0, 0));
    for (let x = -L / 2 + 0.15; x < L / 2; x += 0.3) g.add(at(box(0.03, 0.105, 0.56, '#3E4148'), x, 0.85, 0));
    const sc = [0, 1, 2, 3, 4, 5, 6].map(() => { const p = grp(at(box(0.34, 0.012, 0.42, '#F2E2B8', { outline: 0.03 }), 0, 0, 0), at(box(0.38, 0.05, 0.05, '#E2CC98'), 0, 0.02, -0.21), at(cyl(0.035, 0.035, 0.012, '#B5241E', 10), 0.1, 0.012, 0.12));
      for (let i = 0; i < 4; i++) p.add(at(box(0.24, 0.004, 0.012, '#9A8460'), -0.02, 0.008, -0.13 + i * 0.06));
      const sig = grp(at(box(0.2, 0.008, 0.02, '#14161A'), -0.04, 0.012, 0.13, 0, 0.35, 0), at(box(0.1, 0.008, 0.02, '#14161A'), 0.05, 0.012, 0.11, 0, -0.6, 0)); p.add(sig); g.add(p); return { p, sig }; });
    g.userData.update = t => { sc.forEach(({ p, sig }, i) => { const x = wrap01(t * (o.speed ?? 0.9) / L + i / 7) * L - L / 2; p.position.set(x, 0.92, 0); sig.visible = x > sx0; }); };
    g.userData.update(-1); return g; },

  // A big empty evidence tray on a table (pivot at the floor, faces +Z): a wooden table, a wide flat grey tray, a large brown tag lying in it
  pdTray(o) { return grp(at(box(1.3, 0.06, 0.7, '#8A6A45', { outline: 0.01 }), 0, 0.82, 0), ...[-0.55, 0.55].flatMap(x => [-0.28, 0.28].map(z => at(box(0.06, 0.82, 0.06, '#6A4A30', { pivot: 'bottom' }), x, 0, z))),
    at(box(0.95, 0.05, 0.55, '#9AA3A8', { outline: 0.02 }), 0, 0.875, 0), at(box(0.85, 0.02, 0.45, '#BFC6CC'), 0, 0.9, 0), at(box(0.3, 0.008, 0.18, '#B5793A', { outline: 0.04 }), 0.15, 0.915, 0.05, 0, 0.3, 0), at(cyl(0.02, 0.02, 0.01, '#F2E2B8', 8), 0.03, 0.92, 0.0)); },
  // A big iron ball and chain (pivot at the hand end of the chain): a black ball under three dark links, o.r the ball's radius
  pdBallChain(o) { const r = o.r ?? 0.2, g = grp(); for (let i = 0; i < 4; i++) { const l = new THREE.Mesh(new THREE.TorusGeometry(0.05, 0.016, 5, 10), mat('#3A3D44')); l.position.y = -0.09 * i; l.rotation.y = i % 2 ? PI / 2 : 0; addOutline(l, 0.04); g.add(l); }
    const b = new THREE.Mesh(new THREE.SphereGeometry(r, 14, 10), new THREE.MeshPhongMaterial({ color: '#2A2C31', shininess: 60 })); b.position.y = -0.36 - r; addOutline(b, 0.02); g.add(b); return g; },

  // A big wall clock with no figure (pivot at its centre, faces +Z): a pale face, twelve tick marks, two dark hands both straight up; o.jumpAt: the
  // minute hand jumps one visible notch (6 degrees, overshoot) with a wobble of the whole clock; o.r
  pdClock(o) { const R = o.r ?? 0.6, g = grp(), k = grp(); g.add(k);
    k.add(at(cyl(R + 0.06, R + 0.06, 0.08, '#6A4A30', 32, { outline: 0.008 }), 0, 0, -0.04, PI / 2, 0, 0), at(cyl(R, R, 0.04, '#FBF8F0', 32), 0, 0, 0.01, PI / 2, 0, 0));
    for (let i = 0; i < 60; i++) { const a = i / 60 * TAU, big = i % 5 === 0; k.add(at(box(big ? 0.035 : 0.012, big ? 0.12 : 0.05, 0.01, '#1E2126'), Math.sin(a) * R * 0.86, Math.cos(a) * R * 0.86, 0.035, 0, 0, -a)); }
    const hr = grp(at(box(0.06, R * 0.5, 0.02, '#1E2126', { outline: 0.03 }), 0, R * 0.22, 0)); hr.position.z = 0.05; k.add(hr);
    const mn = grp(at(box(0.04, R * 0.78, 0.02, '#1E2126', { outline: 0.03 }), 0, R * 0.36, 0)); mn.position.z = 0.07; k.add(mn); k.add(at(sphere(0.05, '#1E2126', 1), 0, 0, 0.08));
    g.userData.update = t => { const u = o.jumpAt != null ? t - o.jumpAt : -1, step = TAU / 60; mn.rotation.z = u < 0 ? 0 : -step * (u < 0.06 ? 1.5 * u / 0.06 : 1 + 0.4 * Math.exp(-12 * (u - 0.06)) * Math.cos((u - 0.06) * 45));
      k.rotation.z = u > 0 && u < 0.5 ? 0.025 * Math.exp(-7 * u) * Math.sin(u * 50) : 0; k.position.x = u > 0 && u < 0.4 ? 0.01 * Math.sin(u * 70) * Math.exp(-6 * u) : 0; };
    g.userData.update(-1); return g; },

  // A prison front (pivot at the floor in the middle of the gateway, faces +Z): a grey block 1 m deep with a real passage through it (2.2 x 2.6 m),
  // three rows of barred windows lit warm yellow on both faces, a barred gate across the passage's front (hinged at its left); o.gate [[t, 0..1]]:
  // how open the gate is (it swings out toward +Z); o.offAt / o.offEvery: the windows go grey row by row from the top; o.lit === false: grey all
  // along (daylight); o.key: a big brass key left in the gate's lock; no sign
  pdPrison(o) {
    const w = o.w ?? 9, G = 1.1, GH = 2.6, C = '#9AA0A6', g = grp();
    g.add(at(box(w / 2 - G, 6.2, 1.0, C, { pivot: 'bottom', outline: 0.004 }), -(w / 2 + G) / 2, 0, -0.5), at(box(w / 2 - G, 6.2, 1.0, C, { pivot: 'bottom', outline: 0.004 }), (w / 2 + G) / 2, 0, -0.5),
      at(box(2 * G, 6.2 - GH, 1.0, C, { pivot: 'bottom', outline: 0.004 }), 0, GH, -0.5), at(box(w + 0.3, 0.3, 1.2, '#7E858C', { outline: 0.004 }), 0, 6.2, -0.5),
      at(box(2 * G + 0.3, 0.25, 1.1, '#7E858C', { outline: 0.006 }), 0, GH + 0.12, -0.5));
    const rows = [];
    for (let r = 0; r < 3; r++) { const rm = mat('#FFD878', { emissive: '#E8B040', noGrain: true, unique: true });
      for (let q = 0; q < 6; q++) { const x = -w / 2 + 0.9 + q * (w - 1.8) / 5, y = 1.6 + r * 1.55; if (Math.abs(x) < G + 0.5 && r === 0) continue;
        for (const [z, sg] of [[0.01, 1], [-1.01, -1]]) { g.add(at(box(0.7, 0.9, 0.02, '#FFD878', { material: rm }), x, y, z)); for (let b = 0; b < 4; b++) g.add(at(box(0.04, 0.9, 0.04, '#3A3D44'), x - 0.27 + b * 0.18, y, z + sg * 0.02)); } }
      rows.push(rm); }
    const gate = grp(); gate.position.set(-G, 0, 0.08); g.add(gate);
    for (let b = 0; b < 8; b++) gate.add(at(cyl(0.03, 0.03, GH - 0.1, '#2A2C31', 6, { pivot: 'bottom' }), 0.14 + b * 0.275, 0.02, 0));
    gate.add(at(box(2 * G, 0.08, 0.06, '#2A2C31'), G, 0.3, 0), at(box(2 * G, 0.08, 0.06, '#2A2C31'), G, GH - 0.15, 0), at(box(0.22, 0.32, 0.1, '#3A3D44', { outline: 0.02 }), 2 * G - 0.2, 1.2, 0.05));
    if (o.key) gate.add(at(cyl(0.1, 0.1, 0.035, '#E0B040', 12, { outline: 0.04 }), 2 * G - 0.2, 1.2, 0.36, PI / 2, 0, 0), at(cyl(0.05, 0.05, 0.04, '#3A3D44', 10), 2 * G - 0.2, 1.2, 0.37, PI / 2, 0, 0),
      at(box(0.06, 0.06, 0.28, '#E0B040', { outline: 0.04 }), 2 * G - 0.2, 1.2, 0.2), at(box(0.06, 0.08, 0.04, '#E0B040'), 2 * G - 0.2, 1.15, 0.12));   // the big key left in the lock
    const dark = new THREE.Color('#6E757C'), lit = new THREE.Color('#FFD878'), litE = new THREE.Color('#E8B040'), off = new THREE.Color('#000000');
    const gk = o.gate || [], gEnd = gk.length ? gk[gk.length - 1][0] : 1e9;
    g.userData.update = t => { const gb = t > gEnd ? 0.07 * Math.exp(-7 * (t - gEnd)) * Math.sin((t - gEnd) * 20) : 0; gate.rotation.y = -1.7 * kv(o.gate, t, 0) - gb;   // a little bounce at the end of its swing
      rows.forEach((rm, r) => { const isOff = o.lit === false || (o.offAt != null && t >= o.offAt + (2 - r) * (o.offEvery ?? 0.3)); rm.color.copy(isOff ? dark : lit); rm.emissive.copy(isOff ? off : litE); }); };
    g.userData.update(-1); return g;
  },
  // A flat ground (pivot at its middle, 3 cm up, clear of a set's own floor): o.w x o.d of o.color; o.kerb z: a kerb stone along X there and the road beyond
  pdGround(o) { const W = o.w ?? 40, D = o.d ?? 30, g = grp(), f = new THREE.Mesh(new THREE.PlaneGeometry(W, D), mat(o.color || '#E4D6BE')); f.rotation.x = -PI / 2; f.position.y = 0.03; f.receiveShadow = true; g.add(f);
    if (o.kerb != null) { const rd = new THREE.Mesh(new THREE.PlaneGeometry(W, 8), mat('#6E6E72')); rd.rotation.x = -PI / 2; rd.position.set(0, 0.025, o.kerb + 4.1); g.add(rd, at(box(W, 0.14, 0.2, '#D9CDB4'), 0, 0.07, o.kerb)); rd.position.y = 0.031; }
    return g; },
  // A plain town facade (pivot at the floor in the middle, faces +Z): a cream wall o.w x o.h, rows of tall windows with grey-blue shutters, a cornice; no sign
  pdFacade(o) { const w = o.w ?? 12, h = o.h ?? 9, g = grp(at(box(w, h, 0.4, o.color || '#EFE6D2', { pivot: 'bottom', outline: 0.004 }), 0, 0, -0.2), at(box(w + 0.2, 0.25, 0.6, '#D9CDB4'), 0, h, -0.2), at(box(w, 0.2, 0.5, '#D9CDB4'), 0, 3.0, -0.2));
    for (let fl = 0; fl < 3; fl++) for (let x = -w / 2 + 1.2; x < w / 2 - 0.8; x += 2.0) { const y = 3.9 + fl * 1.75; g.add(at(box(0.8, 1.25, 0.03, '#5E7A94'), x, y, 0.01), at(box(0.95, 0.08, 0.12, '#F4F1EA'), x, y - 0.66, 0.05));
      for (const sx of [-1, 1]) g.add(at(box(0.36, 1.25, 0.04, o.shutter || '#8FA9B8', { outline: 0.02 }), x + sx * 0.6, y, 0.03)); }
    for (let x = -w / 2 + 1.5; x < w / 2 - 1; x += 3.0) g.add(at(box(1.6, 2.2, 0.03, '#3A4450'), x, 1.15, 0.01));
    return g; },
  // A plain lectern (pivot at the floor, faces +Z): a pale wooden box, two short dark microphones; no emblem
  pdPodium(o) { return grp(at(box(0.8, 1.1, 0.5, '#C9B08A', { pivot: 'bottom', outline: 0.006, taper: 1.15 }), 0, 0, 0), at(box(0.95, 0.06, 0.6, '#A88A64'), 0, 1.13, 0),
    ...[-0.15, 0.15].map(x => at(cyl(0.015, 0.015, 0.3, '#2A2C31', 6), x, 1.3, 0.1, 0.4, 0, x)), ...[-0.15, 0.15].map(x => at(sphere(0.04, '#2A2C31', 1), x * 1.4, 1.45, 0.16))); },
  // A plain wooden dock (pivot at the floor in its middle, faces +Z): a low wooden box open at the back, a broad rail on top at o.h (1.0), a bench inside;
  // o.open 'L': no left side (at -X), the way out
  pdDock(o) { const w = o.w ?? 1.6, h = o.h ?? 1.0, W = '#8A6A45';
    return grp(at(box(w, h - 0.06, 0.08, W, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0.35), ...[-1, 1].filter(s => !(o.open === 'L' && s < 0)).map(s => at(box(0.08, h - 0.06, 0.7, W, { pivot: 'bottom', outline: 0.006 }), s * w / 2, 0, 0)),
      at(box(w + 0.12, 0.08, 0.2, '#6A4A30', { outline: 0.01 }), 0, h - 0.02, 0.35), ...[-1, 1].filter(s => !(o.open === 'L' && s < 0)).map(s => at(box(0.14, 0.08, 0.74, '#6A4A30'), s * w / 2, h - 0.02, 0)),
      at(box(w - 0.2, 0.08, 0.36, '#6A4A30', { outline: 0.01 }), 0, 0.46, -0.2), at(box(w - 0.2, 0.46, 0.06, '#5A3E28', { pivot: 'bottom' }), 0, 0, -0.2)); },
  // A plain wooden judge's bench (pivot at the floor in its middle, faces +Z): a tall panelled wooden front, a top, a raised floor behind; no emblem
  pdJudgeBench(o) { const w = o.w ?? 2.6, h = o.h ?? 1.35, g = grp(at(box(w, h, 0.7, '#7A5A3C', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(w + 0.15, 0.08, 0.85, '#5A3E28', { outline: 0.01 }), 0, h + 0.04, -0.05),
      at(box(w, 0.4, 1.4, '#6A4A30', { pivot: 'bottom' }), 0, 0, -1.0));
    for (let i = 0; i < 3; i++) g.add(at(box(w / 3 - 0.16, h - 0.35, 0.02, '#8A6A45', { outline: 0.02 }), -w / 3 + i * w / 3, h / 2, 0.36));
    return g; },
  // A big wall switch on a plate (pivot at its middle, faces +Z): o.flipAt: the lever snaps down
  pdSwitch(o) { const g = grp(at(box(0.3, 0.45, 0.04, '#E8E2D2', { outline: 0.02 }), 0, 0, 0)), lv = grp(at(box(0.08, 0.2, 0.06, '#C9CED4', { outline: 0.03 }), 0, 0.1, 0.05)); g.add(lv);
    g.userData.update = t => { lv.rotation.x = o.flipAt != null && t >= o.flipAt ? PI - 0.4 * Math.exp(-15 * (t - o.flipAt)) : 0.3; }; g.userData.update(-1); return g; },
  // A white board held up (pivot at its middle, faces +Z): « PARDON » in big black letters sized to fit, struck through by ONE diagonal red line
  pdBoard(o) { const w = o.w ?? 1.1, h = o.h ?? 0.6;
    return grp(at(box(w + 0.04, h + 0.04, 0.03, '#C9CED4', { outline: 0.01 }), 0, 0, -0.02), canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); let fs = H * 0.6; c.font = `900 ${fs}px Arial`;
      while (c.measureText('PARDON').width > W * 0.86) { fs *= 0.95; c.font = `900 ${fs}px Arial`; } c.fillStyle = '#14161A'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('PARDON', W / 2, H * 0.53);
      c.strokeStyle = '#D8262E'; c.lineWidth = H * 0.09; c.lineCap = 'round'; c.beginPath(); c.moveTo(W * 0.08, H * 0.82); c.lineTo(W * 0.92, H * 0.18); c.stroke(); }, { res: 512 })); },
  // A big ticket pad held (pivot at its middle, faces +Z): a white pad with grey lines (no word), a red header band; o.tearAt: the top sheet flaps
  pdTicket(o) { const g = grp(at(box(0.3, 0.42, 0.06, '#FBF8F0', { outline: 0.03 }), 0, 0, 0), at(box(0.32, 0.07, 0.07, '#C8322A', { outline: 0.03 }), 0, 0.2, 0)); for (let i = 0; i < 6; i++) g.add(at(box(0.22, 0.014, 0.065, '#9AA3A8'), 0, 0.1 - i * 0.055, 0)); return g; },
  // A paper cup (pivot at its bottom): white with a brown band; o.fall [t0]: it drops and tips over, a splash
  pdCup(o) { const g = grp(), c = grp(at(cyl(0.06, 0.045, 0.14, '#F4F1EA', 10, { pivot: 'bottom', outline: 0.03 }), 0, 0, 0), at(cyl(0.062, 0.058, 0.04, '#8A5A38', 10), 0, 0.07, 0)); g.add(c);
    const sp = at(cyl(0.18, 0.18, 0.01, '#8A5A38', 14), 0.2, 0.005, 0); g.add(sp);
    g.userData.update = t => { const u = o.fall != null ? t - o.fall : -1; c.position.y = u < 0 ? (o.h ?? 1.0) : u < 0.3 ? (o.h ?? 1.0) * (1 - (u / 0.3) ** 2) : 0; c.rotation.z = u > 0.3 ? -PI / 2 * smooth((u - 0.3) / 0.1) : 0; sp.visible = u > 0.32; sp.scale.setScalar(Math.min(1, (u - 0.3) * 6)); };
    g.userData.update(-1); return g; },
  // A big grocery bag (pivot at its bottom): a kraft paper bag with a baguette, leeks and an apple poking out
  pdGroceries(o) { return grp(at(box(0.36, 0.42, 0.24, '#C9A06A', { pivot: 'bottom', outline: 0.02 }), 0, 0, 0), at(cyl(0.03, 0.03, 0.5, '#D9A35C', 8), -0.08, 0.5, 0, 0.2, 0, 0.2), at(cyl(0.025, 0.025, 0.4, '#7CC25A', 6), 0.08, 0.5, 0.02, -0.2, 0, -0.2), at(sphere(0.06, '#D8262E', 1), 0.05, 0.44, -0.05)); },
  // A window picture of five cheering people throwing flowers (pivot at its middle, faces +Z): painted, the petals flutter (o.w / o.h)
  pdCheer(o) { const w = o.w ?? 1.4, h = o.h ?? 1.1, g = grp(), pic = canvasPlane(w, h, (c, W, H) => { const gr = c.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#7FC0EA'); gr.addColorStop(1, '#CFE8F6'); c.fillStyle = gr; c.fillRect(0, 0, W, H);
      const cols = ['#C8322A', '#3E7FB6', '#F2C94C', '#5E8C4A', '#8A5AB6']; for (let i = 0; i < 5; i++) { const x = W * (0.12 + 0.19 * i), y = H * 0.62; c.fillStyle = cols[i]; c.fillRect(x - W * 0.05, y, W * 0.1, H * 0.38);
        c.fillStyle = '#E8B98A'; c.beginPath(); c.arc(x, y - H * 0.07, W * 0.045, 0, TAU); c.fill(); c.strokeStyle = cols[i]; c.lineWidth = W * 0.025; c.beginPath(); c.moveTo(x - W * 0.04, y + H * 0.04); c.lineTo(x - W * 0.08, y - H * 0.12); c.moveTo(x + W * 0.04, y + H * 0.04); c.lineTo(x + W * 0.08, y - H * 0.12); c.stroke(); } }, { res: 256, emissive: 0.9 });
    g.add(pic); const pet = [0, 1, 2, 3, 4, 5, 6, 7, 8].map(i => { const m = at(box(0.04, 0.03, 0.01, ['#E8508A', '#F2C94C', '#FFFFFF'][i % 3]), 0, 0, 0.02); g.add(m); return m; });
    g.userData.update = t => { pet.forEach((m, i) => { const u = wrap01(t * 0.6 + i / 9); m.position.set((hsh(i) - 0.5) * w * 0.9, h * 0.45 - u * h * 0.9, 0.02); m.rotation.z = t * 5 + i; }); }; g.userData.update(0); return g; },
  // Two swing doors in a wall opening (pivot at the floor in the middle, faces +Z): padded leather doors 1.9 m tall with round windows, posts and a
  // lintel, a wall either side; o.swingAt: they burst open toward +Z and swing back and forth with dying overshoots
  pdSwingDoors(o) { const g = grp(), W = o.wall || '#E3D3B5', ds = [-1, 1].map(sd => { const p = grp(); p.position.set(sd * 0.62, 0, 0); g.add(p);
      p.add(at(box(0.6, 1.9, 0.07, '#7A2E2A', { outline: 0.008 }), -sd * 0.31, 1.0, 0), at(cyl(0.12, 0.12, 0.08, '#CFE3EE', 14), -sd * 0.31, 1.55, 0, PI / 2, 0, 0));
      for (let i = 0; i < 4; i++) p.add(at(sphere(0.015, '#D9A93A', 0), -sd * (0.08 + i * 0.15), 0.3, 0.04));
      return { p, sd }; });
    g.add(at(box(0.12, 2.3, 0.2, '#6A4A30', { pivot: 'bottom', outline: 0.008 }), -0.7, 0, 0), at(box(0.12, 2.3, 0.2, '#6A4A30', { pivot: 'bottom', outline: 0.008 }), 0.7, 0, 0), at(box(1.52, 0.14, 0.2, '#6A4A30', { outline: 0.008 }), 0, 2.3, 0));
    g.add(at(box(3.0, 3.6, 0.15, W, { pivot: 'bottom' }), -2.26, 0, -0.05), at(box(3.0, 3.6, 0.15, W, { pivot: 'bottom' }), 2.26, 0, -0.05), at(box(1.4, 1.2, 0.15, W, { pivot: 'bottom' }), 0, 2.4, -0.05));
    g.userData.update = t => { const u = o.swingAt != null ? t - o.swingAt : -1; for (const { p, sd } of ds) p.rotation.y = u > 0 ? sd * (u < 0.08 ? 1.4 * u / 0.08 : 1.4 * Math.exp(-2.2 * (u - 0.08)) * Math.cos((u - 0.08) * 8)) : 0; }; g.userData.update(-1); return g; },
  // A long robe skirt (attach to the hips joint; pivot at the waist, hangs -Y): a flared gown from the waist to the ankles, o.color, o.L its length,
  // a few vertical folds; o.jabot: a white bib (attach a second one to the torso with o.bib)
  pdRobe(o) { const L = o.L ?? 0.9, C = o.color || '#14161A', g = grp();
    if (o.bib) { g.add(at(box(0.16, 0.22, 0.03, '#F4F4F0', { outline: 0.03 }), 0, 0, 0)); return g; }
    const c = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.36, L, 14, 1, true), mat(C, { doubleSide: true })); c.position.y = -L / 2; c.scale.z = 0.8; addOutline(c, 0.01); g.add(c);
    for (let i = 0; i < 6; i++) { const a = i / 6 * TAU + 0.3; g.add(at(box(0.02, L * 0.9, 0.02, C === '#14161A' ? '#2A2C31' : '#8E1C17'), Math.sin(a) * 0.29, -L * 0.52, Math.cos(a) * 0.23, -0.12 * Math.cos(a), 0, 0.12 * Math.sin(a))); }
    return g; },
  // A big rucksack (attach to the torso joint; pivot at its back face's middle, faces -Z away from the back): a tall rounded pack with a flap and a
  // buckle, two side pockets, a rolled mat on top, two shoulder straps over the shoulders; o.color
  pdRucksack(o) { const C = o.color || '#2F7F5C', D = o.dark || '#1E5A40', g = grp();
    g.add(at(box(0.42, 0.6, 0.3, C, { outline: 0.01 }), 0, 0, -0.17));
    const topc = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.42, 12), mat(C)); topc.rotation.z = PI / 2; topc.position.set(0, 0.3, -0.17); addOutline(topc, 0.02); g.add(topc);   // the rounded top
    g.add(at(box(0.44, 0.26, 0.33, D, { outline: 0.02 }), 0, 0.22, -0.18), at(box(0.06, 0.08, 0.04, '#D9A93A'), 0, 0.1, -0.35));   // the flap and its buckle
    for (const sx of [-1, 1]) g.add(at(box(0.08, 0.22, 0.18, D, { outline: 0.02 }), sx * 0.25, -0.12, -0.17), at(box(0.06, 0.62, 0.03, '#2A2C31'), sx * 0.13, 0.05, 0.02), at(box(0.06, 0.03, 0.25, '#2A2C31'), sx * 0.13, 0.35, 0.1));
    g.add(at(cyl(0.08, 0.08, 0.5, '#E8742A', 10, { outline: 0.02 }), 0, 0.5, -0.17, 0, 0, PI / 2)); return g; },
};
