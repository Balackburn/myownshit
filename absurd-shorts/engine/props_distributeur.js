// « Le distributeur » (story 95, cycle 51): this man put a coin in the corridor's drinks machine; nothing fell. The minister ruled: it is a bank. It
// got its licence; this man is its first client (his arm still in the flap). The whole country saved in it; it never gave anything back. It bought
// the coffee machine, then the photocopier, named a director who drank it all in coffees: bankrupt. Leaning, it crushed the sandwich machine. Too big
// to fall: the army holds it at the shoulder and the State bails it out with two billion in coins. The sandwich machine got nothing. The stuck can
// finally drops: the director's bonus. This man claims his coin: it is invested for forty years. The bank was out of order from the start.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere, mat, rng, addOutline } from './style.js';
import { grp, at, canvasPlane, inst, rod } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = x => { const u = clamp01(x), c = 1.70158; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const noShadow = m => { m.traverse(c => { c.castShadow = false; }); return m; };
// a value keyed in time: keys [[t, v], ...] (sorted), eased (smoothstep) from each key to the next over the gap between them; before the first key
// its value, after the last key its value
function kv(keys, t, def = 0) {
  if (keys == null) return def;
  if (typeof keys === 'number') return keys;
  if (!keys.length) return def;
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) { const [a, va] = keys[i], [b, vb] = keys[i + 1]; if (t < b) return va + (vb - va) * smooth((t - a) / Math.max(1e-4, b - a)); }
  return keys[keys.length - 1][1];
}
const fitFont = (c, text, maxW, fs, weight = 900) => { c.font = `${weight} ${fs}px Arial`; while (c.measureText(text).width > maxW && fs > 6) { fs -= 1; c.font = `${weight} ${fs}px Arial`; } return fs; };

// the oversized bright can (pivot at its middle, upright along +Y): plain colour bands, no brand, no letters; o.s scale (1: 0.18 m tall, 1.5 x a can)
function bigCanMesh(o = {}) {
  const r = 0.05, h = 0.18, g = grp(), B = o.body || '#FF5A0A';
  const body = cyl(r, r, h * 0.86, B, 18, { unique: true, noGrain: true }); g.add(body);
  g.add(at(cyl(r * 1.002, r * 1.002, h * 0.16, o.band || '#FFD21E', 18, { noGrain: true }), 0, 0.012, 0));
  g.add(at(cyl(r * 1.004, r * 1.004, h * 0.07, o.band2 || '#1E5AE6', 18, { noGrain: true }), 0, 0.012, 0));
  g.add(at(cyl(r * 1.003, r * 1.003, h * 0.05, o.band2 || '#1E5AE6', 18, { noGrain: true }), 0, -h * 0.3, 0));
  g.add(at(cyl(r * 0.86, r, h * 0.07, '#D9DDE2', 18, { noGrain: true }), 0, h * 0.465, 0), at(cyl(r, r * 0.86, h * 0.07, '#BFC4CA', 18, { noGrain: true }), 0, -h * 0.465, 0));
  g.add(at(cyl(r * 0.84, r * 0.84, 0.004, '#C9CED4', 18), 0, h * 0.5, 0), at(box(0.026, 0.004, 0.014, '#9AA0A6'), 0.012, h * 0.503, 0));
  addOutline(body, 0.04);
  g.scale.setScalar(o.s ?? 1); return g;
}

// a brass plate with BANQUE engraved and four screws (front +Z, origin at its centre), w x h
function brassPlate(w, h, text) {
  const g = grp(at(box(w, h, 0.012, '#B8892E', { outline: 0.01 }), 0, 0, 0));
  const face = canvasPlane(w * 0.98, h * 0.94, (c, W, H) => {
    const gr = c.createLinearGradient(0, 0, W, H); gr.addColorStop(0, '#F2D07A'); gr.addColorStop(0.45, '#D9A945'); gr.addColorStop(0.55, '#F7DE95'); gr.addColorStop(1, '#C8922E');
    c.fillStyle = gr; c.fillRect(0, 0, W, H); c.strokeStyle = '#7A5418'; c.lineWidth = H * 0.06; c.strokeRect(H * 0.08, H * 0.08, W - H * 0.16, H - H * 0.16);
    const fs = fitFont(c, text, W * 0.72, Math.round(H * 0.6)); c.textAlign = 'center'; c.textBaseline = 'middle';
    c.fillStyle = '#FBE7A8'; c.fillText(text, W / 2 + H * 0.02, H * 0.54 + H * 0.02); c.fillStyle = '#4A3008'; c.fillText(text, W / 2, H * 0.54); void fs;
    c.fillStyle = '#6A4A14'; for (const [x, y] of [[0.05, 0.22], [0.95, 0.22], [0.05, 0.78], [0.95, 0.78]]) { c.beginPath(); c.arc(W * x, H * y, H * 0.06, 0, TAU); c.fill(); }
  }, { res: 512 });
  face.position.z = 0.0065; g.add(face); return g;
}

// the dull yellowed paper EN PANNE sticker (a plane facing +Z, origin at its centre), w wide: faded paper, soft dirty edges, a curled corner,
// thin brownish letters (soft at a distance, read only close up)
function penneSticker(w) {
  const h = w * 0.5;
  const p = canvasPlane(w, h, (c, W, H) => {
    c.clearRect(0, 0, W, H); c.fillStyle = '#EDE5C4'; c.beginPath(); c.moveTo(W * 0.02, H * 0.05); c.lineTo(W * 0.85, H * 0.02); c.lineTo(W * 0.99, H * 0.28); c.lineTo(W * 0.98, H * 0.97); c.lineTo(W * 0.03, H * 0.95); c.closePath(); c.fill();
    const gr = c.createRadialGradient(W * 0.4, H * 0.45, 0, W * 0.5, H * 0.5, W * 0.62); gr.addColorStop(0, 'rgba(255,250,230,0.1)'); gr.addColorStop(1, 'rgba(150,125,70,0.35)'); c.fillStyle = gr; c.fillRect(0, 0, W, H);
    c.fillStyle = 'rgba(110,85,40,0.18)'; for (let i = 0; i < 14; i++) { c.beginPath(); c.arc(W * hsh(i + 3), H * hsh(i + 9), H * (0.02 + 0.05 * hsh(i)), 0, TAU); c.fill(); }
    c.fillStyle = '#6A6250'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitFont(c, 'EN PANNE', W * 0.76, Math.round(H * 0.4), 600); c.fillText('EN PANNE', W / 2, H * 0.53);
    c.fillStyle = '#B9AB72'; c.beginPath(); c.moveTo(W * 0.99, H * 0.02); c.lineTo(W * 0.86, H * 0.02); c.lineTo(W * 0.99, H * 0.3); c.closePath(); c.fill();
    c.fillStyle = 'rgba(40,30,15,0.35)'; c.beginPath(); c.moveTo(W * 0.86, H * 0.02); c.lineTo(W * 0.99, H * 0.3); c.lineTo(W * 0.97, H * 0.33); c.lineTo(W * 0.83, H * 0.04); c.closePath(); c.fill();
  }, { res: 512, transparent: true });
  p.castShadow = false; return p;
}

export const DISTRIBUTEUR_PROPS = {
  // The tall red drinks machine (pivot at the floor under its middle, front +Z; 1.0 m wide, 2.15 m tall, 0.8 m deep, its front at z 0.4).
  // Glass on the left (x -0.45..0.12, y 0.72..1.98) with five rows of spirals of muted cans; at the front end of the bottom spiral of the third
  // column the one big bright can, tilted forward, stuck. The panel on the right: a blank green screen, a keypad, the coin slot at (0.31, 1.18),
  // a coin return, the coin-box door below (x 0.18..0.44, y 0.5..0.84, hinged on its right). The delivery flap under the glass (centre x -0.17, y
  // 0.30..0.58). The yellowed EN PANNE sticker on the glass's right edge at the slot's height (always).
  // o.plaque: true, or a time: the brass BANQUE plate on the header (from that time, with a pop); o.flapIn (0..1 or keys): the flap pushed in (an arm
  // inside); o.tilt [[t, deg], ...]: the machine leans to its right (toward +X) about its bottom right edge, eased between keys; o.creak [[t0, t1]]:
  // it shivers meanwhile; o.canWobble [t...]: the stuck can rocks for 0.5 s and stays; o.canDrop t: the spiral turns and the can falls into the flap
  // (0.6 s); o.canHide t: the can gone from then (picked up); o.boxOpen (0..1 or keys): the coin-box door opens; o.boxEmpty: the box's cavity shown
  // empty (always); o.coinsAt [t...]: a gold coin slides into the slot; o.funnel: true or a time: a giant funnel jammed in the slot, mouth up,
  // overflowing with coins; o.glint [t...]: a glint runs over the plate. userData: slot, flap, can (local points).
  drinkMachine(o) {
    const W = 1.0, H = 2.15, D = 0.8, FZ = D / 2, C = o.color || '#C9282B', CD = '#8E1B1E', IN = '#2C2E34';
    const GX0 = -0.45, GX1 = 0.12, GY0 = 0.72, GY1 = 1.98, GW = GX1 - GX0, GCX = (GX0 + GX1) / 2;
    const SLOT = [0.215, 1.2, FZ + 0.012], FLAP = [-0.17, 0.44, FZ], STK = [0.34, 1.2, FZ + 0.0145];
    const g = grp(), piv = grp(), body = grp(); g.add(piv); piv.add(body); piv.position.x = W / 2; body.position.x = -W / 2;
    // cabinet: back, sides, roof, plinth, the panel on the right, the band under the glass
    body.add(at(box(W, H, 0.04, IN, { pivot: 'bottom', outline: 0.01 }), 0, 0, -FZ + 0.02));
    for (const s of [-1, 1]) body.add(at(box(0.05, H, D, C, { pivot: 'bottom', outline: 0.01 }), s * (W / 2 - 0.025), 0, 0));
    body.add(at(box(W, 0.17, D, C, { outline: 0.01 }), 0, H - 0.085, 0), at(box(W - 0.02, 0.09, D - 0.02, CD, { pivot: 'bottom' }), 0, 0, 0));
    body.add(at(box(W / 2 - GX1 - 0.025, H - 0.17 - 0.09, 0.06, C, { pivot: 'bottom', outline: 0.008 }), (GX1 + W / 2 - 0.05) / 2 + 0.0125, 0.09, FZ - 0.03));
    // the band under the glass, cut round the flap's opening (x -0.42..0.08, y 0.30..0.58) so an arm can go in
    body.add(at(box(GW + 0.01, 0.21, 0.06, C, { pivot: 'bottom', outline: 0.008 }), GCX, 0.09, FZ - 0.03), at(box(GW + 0.01, GY0 - 0.58, 0.06, C, { pivot: 'bottom', outline: 0.008 }), GCX, 0.58, FZ - 0.03));
    body.add(at(box(0.04, 0.28, 0.06, C, { pivot: 'bottom' }), GX0 + 0.015, 0.3, FZ - 0.03), at(box(GX1 - 0.08 + 0.005, 0.28, 0.06, C, { pivot: 'bottom' }), (0.08 + GX1) / 2 + 0.0025, 0.3, FZ - 0.03));
    // header: a white drawn can and bubbles on a dark band (no words)
    const hdr = canvasPlane(W - 0.12, 0.13, (c, Wc, Hc) => { c.fillStyle = '#7A1517'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = 'rgba(255,255,255,0.9)';
      for (const x of [0.12, 0.88]) { const cx = Wc * x, w = Hc * 0.36, h = Hc * 0.72; c.fillRect(cx - w / 2, Hc * 0.14, w, h); c.fillStyle = '#7A1517'; c.fillRect(cx - w / 2, Hc * 0.42, w, Hc * 0.1); c.fillStyle = 'rgba(255,255,255,0.9)'; }
      for (let i = 0; i < 9; i++) { c.beginPath(); c.arc(Wc * (0.2 + 0.6 * hsh(i)), Hc * (0.2 + 0.6 * hsh(i + 4)), Hc * (0.04 + 0.05 * hsh(i + 9)), 0, TAU); c.fill(); } }, { res: 512 });
    body.add(at(hdr, 0, H - 0.085, FZ + 0.004));
    // glass frame and glass
    body.add(at(box(GW + 0.05, 0.03, 0.03, '#2A2A2E'), GCX, GY1, FZ - 0.005), at(box(GW + 0.05, 0.03, 0.03, '#2A2A2E'), GCX, GY0, FZ - 0.005));
    body.add(at(box(0.03, GY1 - GY0, 0.03, '#2A2A2E', { pivot: 'bottom' }), GX0 - 0.01, GY0, FZ - 0.005), at(box(0.03, GY1 - GY0, 0.03, '#2A2A2E', { pivot: 'bottom' }), GX1 + 0.01, GY0, FZ - 0.005));
    const glass = new THREE.Mesh(new THREE.PlaneGeometry(GW, GY1 - GY0), new THREE.MeshLambertMaterial({ color: '#CFE6F2', transparent: true, opacity: 0.08, depthWrite: false, side: THREE.DoubleSide }));
    glass.position.set(GCX, (GY0 + GY1) / 2, FZ - 0.006); body.add(glass);
    body.add(at(box(GW, GY1 - GY0, 0.02, '#1C2028'), GCX, (GY0 + GY1) / 2, -FZ + 0.06));
    // the dark lining of the glass column (the red walls lit inside read pink through the glass)
    for (const x of [GX0 - 0.012, GX1 + 0.012]) body.add(at(box(0.012, GY1 - GY0, D - 0.1, '#232731'), x, (GY0 + GY1) / 2, 0.0));
    body.add(at(box(GW + 0.03, 0.012, D - 0.1, '#232731'), GCX, GY1 - 0.01, 0.0), at(box(GW + 0.03, 0.012, D - 0.1, '#2E323C'), GCX, GY0 + 0.01, 0.0));
    body.add(at(box(GW - 0.04, 0.012, 0.012, '#FFF6E0', { emissive: '#FFE9B8', noGrain: true }), GCX, GY1 - 0.03, FZ - 0.05));
    // five rows of spirals with muted cans; shelves
    const COLS = [0, 1, 2, 3].map(i => GX0 + 0.075 + i * (GW - 0.15) / 3), ROWS = [0.78, 1.02, 1.26, 1.5, 1.74];
    const helix = (() => { const pts = []; for (let i = 0; i <= 120; i++) { const u = i / 120, a = u * TAU * 5; pts.push(new THREE.Vector3(0.048 * Math.cos(a), 0.048 * Math.sin(a), -0.32 + 0.64 * u)); } return new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 160, 0.0032, 4, false); })();
    const spiralMat = new THREE.MeshLambertMaterial({ color: '#7E868E' });
    const spirals = [];
    const muted = ['#4E5C6C', '#6A5A4C', '#4E6658', '#625870', '#66664A'];
    const cans = [], ccol = [];
    ROWS.forEach((y, ri) => {
      body.add(at(box(GW - 0.01, 0.012, D - 0.14, '#9AA0A6'), GCX, y, -0.03));
      COLS.forEach((x, ci) => {
        const sp = new THREE.Mesh(helix, spiralMat); sp.position.set(x, y + 0.055, FZ - 0.4); body.add(sp); spirals.push([ri, ci, sp]);
        const big = ri === 0 && ci === 2;
        for (let kk = 0; kk < 3; kk++) { if (big && kk === 2) continue; cans.push([x, y + 0.072, FZ - 0.62 + kk * 0.14, 0, 0, 0, 1, 1, 1]); ccol.push(muted[(ri * 2 + ci + kk) % muted.length]); }
      });
    });
    const canGeo = new THREE.CylinderGeometry(0.032, 0.032, 0.12, 12); body.add(inst(canGeo, new THREE.MeshLambertMaterial({ color: '#FFFFFF' }), cans, ccol));
    // the big bright can, tilted forward at the front end of the bottom spiral (column 1)
    const CAN0 = [COLS[2], ROWS[0] + 0.115, FZ - 0.09], can = grp(bigCanMesh({})); can.position.set(...CAN0); can.rotation.x = 0.42; can.rotation.z = -0.08; body.add(can);
    const big = spirals.find(([ri, ci]) => ri === 0 && ci === 2)[2];
    // the EN PANNE sticker on the glass, right edge, slot height
    // the panel: a glossy black plate (x 0.175..0.465, y 0.98..1.82) with a blank screen, a keypad high up, the slot low left and the small paper
    // EN PANNE sticker beside the slot, at its height; a coin return below
    body.add(at(box(0.29, 0.84, 0.012, '#39404C'), 0.32, 1.40, FZ + 0.006), at(canvasPlane(0.29, 0.84, (c, Wc, Hc) => { const gr = c.createLinearGradient(0, 0, Wc, Hc); gr.addColorStop(0, 'rgba(255,255,255,0.0)'); gr.addColorStop(0.35, 'rgba(210,225,240,0.16)'); gr.addColorStop(0.5, 'rgba(255,255,255,0.0)'); gr.addColorStop(0.75, 'rgba(210,225,240,0.08)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); c.clearRect(0, 0, Wc, Hc); c.fillStyle = gr; c.fillRect(0, 0, Wc, Hc); }, { res: 256, transparent: true }), 0.32, 1.40, FZ + 0.0125), at(box(0.2, 0.08, 0.006, '#9CE8A0', { emissive: '#2E6A34', noGrain: true }), 0.32, 1.74, FZ + 0.013));
    const keys = []; for (let r = 0; r < 4; r++) for (let c = 0; c < 3; c++) keys.push([0.27 + c * 0.05, 1.64 - r * 0.052, FZ + 0.014]);
    body.add(inst(new THREE.BoxGeometry(0.034, 0.034, 0.01), mat('#E6E2D8'), keys));
    body.add(at(box(0.09, 0.13, 0.014, '#C9CCD1', { outline: 0.01 }), SLOT[0], SLOT[1], FZ + 0.007), at(box(0.012, 0.065, 0.01, '#141414'), SLOT[0], SLOT[1] + 0.01, FZ + 0.014));
    body.add(at(box(0.12, 0.08, 0.05, '#2A2A2E'), 0.32, 0.98, FZ + 0.01), at(box(0.09, 0.05, 0.02, '#111114'), 0.32, 0.975, FZ + 0.03));
    const stk = penneSticker(o.stickerW ?? 0.068); stk.position.set(...STK); stk.rotation.z = o.stickerRot ?? 0; body.add(stk);
    // the coin box: a dark cavity behind a hinged grey door
    body.add(at(box(0.24, 0.32, 0.01, '#121214'), 0.31, 0.67, FZ + 0.004));
    const door = grp(at(box(0.25, 0.33, 0.02, '#8C949A', { outline: 0.01, unique: true }), -0.125, 0, 0), at(cyl(0.016, 0.016, 0.012, '#D9B85A', 10), -0.2, 0.0, 0.014, PI / 2, 0, 0), at(box(0.004, 0.014, 0.006, '#3A2A10'), -0.2, 0, 0.022));
    door.position.set(0.435, 0.67, FZ + 0.014); body.add(door);
    // the delivery flap: a dark recess and a plate hinged on its top edge
    body.add(at(box(0.5, 0.28, 0.012, '#141416'), FLAP[0], FLAP[1], FZ - 0.13), at(box(0.5, 0.012, 0.14, '#26282D'), FLAP[0], FLAP[1] - 0.135, FZ - 0.06), at(box(0.5, 0.012, 0.14, '#101012'), FLAP[0], FLAP[1] + 0.135, FZ - 0.06));
    for (const sx of [-1, 1]) body.add(at(box(0.012, 0.28, 0.14, '#1A1A1D'), FLAP[0] + sx * 0.245, FLAP[1], FZ - 0.06));
    body.add(at(box(0.54, 0.03, 0.04, '#2A2A2E'), FLAP[0], FLAP[1] + 0.155, FZ - 0.005), at(box(0.54, 0.03, 0.04, '#2A2A2E'), FLAP[0], FLAP[1] - 0.155, FZ - 0.005));
    const flap = grp(at(box(0.5, 0.27, 0.012, '#3A3C42', { outline: 0.01, unique: true }), 0, -0.135, 0)); flap.position.set(FLAP[0], FLAP[1] + 0.14, FZ - 0.004); body.add(flap);
    // the plate
    let plate = null; if (o.plaque != null && o.plaque !== false) { plate = grp(brassPlate(0.46, 0.115, o.plaqueText || 'BANQUE')); plate.position.set(0, H - 0.085, FZ + 0.02); body.add(plate); }
    const glint = new THREE.Mesh(new THREE.PlaneGeometry(0.05, 0.16), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0, depthWrite: false })); glint.rotation.z = 0.5;
    if (plate) { glint.position.set(0, 0, 0.012); plate.add(glint); }
    // the funnel jammed in the slot, its mouth up and toward us, full of coins
    let funnel = null;
    if (o.funnel != null && o.funnel !== false) {
      funnel = grp(); const R = 0.44, L = 0.85;
      const cone = new THREE.Mesh(new THREE.CylinderGeometry(R, 0.05, L, 24, 1, true), new THREE.MeshLambertMaterial({ color: '#9AA3AC', side: THREE.DoubleSide, flatShading: true })); cone.position.y = L / 2 + 0.16; cone.castShadow = true; funnel.add(cone);
      const rim = new THREE.Mesh(new THREE.TorusGeometry(R, 0.024, 6, 28), mat('#5E666E')); rim.rotation.x = PI / 2; rim.position.y = L + 0.16; funnel.add(rim);
      funnel.add(at(cyl(0.05, 0.05, 0.2, '#9AA1A8', 10), 0, 0.08, 0));
      const fill = new THREE.Mesh(new THREE.CylinderGeometry(R * 0.93, R * 0.6, 0.12, 24), mat('#E2B53C', { noGrain: true })); fill.position.y = L + 0.1; funnel.add(fill);
      const fl = []; const rr = rng(5); for (let i = 0; i < 60; i++) { const a = rr() * TAU, d = Math.sqrt(rr()) * R * 0.9; fl.push([Math.cos(a) * d, L + 0.165 + rr() * 0.03, Math.sin(a) * d, (rr() - 0.5) * 0.8, rr() * TAU, (rr() - 0.5) * 0.8]); }
      funnel.add(inst(new THREE.CylinderGeometry(0.035, 0.035, 0.008, 10), mat('#F0C64A', { noGrain: true }), fl));
      funnel.position.set(SLOT[0], SLOT[1], FZ + 0.01); funnel.rotation.x = 0.5; body.add(funnel);
    }
    // coins sliding into the slot
    const coinsAt = [].concat(o.coinsAt ?? []), coinM = mat('#E8BE3E', { noGrain: true });
    const coinObjs = [0, 1].map(() => { const c = at(cyl(0.028, 0.028, 0.006, '#E8BE3E', 14, { material: coinM, outline: 0.003 }), 0, 0, 0, 0, 0, PI / 2); c.visible = false; body.add(c); return c; });
    // a can that falls into the flap (o.canDrop)
    g.userData.slot = SLOT; g.userData.flap = FLAP; g.userData.can = CAN0; g.userData.sticker = STK;
    g.userData.update = t => {
      const tl = kv(o.tilt, t, 0) * PI / 180; let sh = 0;
      for (const [a, b] of o.creak || []) if (t >= a && t <= b) sh = 0.006 * Math.sin(t * 61) + 0.004 * Math.sin(t * 37);
      piv.rotation.z = -tl + sh;
      flap.rotation.x = 1.25 * kv(o.flapIn, t, 0);   // the bottom swings in (an arm pushed through)
      door.rotation.y = -1.9 * kv(o.boxOpen, t, 0);
      // the can: wobble, drop, hide
      let cw = 0; for (const a of [].concat(o.canWobble ?? [])) { const u = t - a; if (u >= 0 && u < 0.6) cw += 0.22 * Math.sin(u * 30) * Math.exp(-u * 6); }
      can.position.set(...CAN0); can.rotation.set(0.42 + cw, 0, -0.08 + cw * 0.4); can.visible = !(o.canHide != null && t >= o.canHide);
      if (o.canDrop != null) {
        const u = t - o.canDrop; big.rotation.z = u > 0 ? Math.min(u, 0.35) * 14 : 0;
        if (u > 0.3) { const f = clamp01((u - 0.3) / 0.4), y = CAN0[1] + 0.05 * Math.sin(f * PI) * (1 - f) + (FLAP[1] - 0.04 - CAN0[1]) * f * f; can.position.set(CAN0[0] + (FLAP[0] + 0.13 - CAN0[0]) * f, y, CAN0[2] + (FZ - 0.07 - CAN0[2]) * f + 0.06 * Math.sin(f * PI)); can.rotation.set(0.42 + f * 1.2, 0, -0.08 + f * 0.9);
          if (u > 0.7) { const b = u - 0.7; can.position.y += 0.03 * Math.abs(Math.sin(b * 18)) * Math.exp(-b * 9); can.rotation.set(PI / 2 - 0.25, 0, 0.8); } }
      }
      if (plate) { const pa = typeof o.plaque === 'number' ? t - o.plaque : 1; plate.visible = pa >= 0; plate.scale.setScalar(Math.max(0.01, pa < 0 ? 0.01 : outBack(pa / 0.28))); }
      if (plate) { let gk = -1; for (const a of [].concat(o.glint ?? [])) { const u = (t - a) / 0.35; if (u >= 0 && u < 1) gk = u; } glint.material.opacity = gk >= 0 ? 0.7 * Math.sin(gk * PI) : 0; glint.position.x = -0.22 + 0.44 * Math.max(0, gk); }
      if (funnel) { const fa = typeof o.funnel === 'number' ? t - o.funnel : 1; funnel.visible = fa >= 0; funnel.scale.setScalar(fa < 0 ? 0.01 : Math.max(0.01, outBack(fa / 0.25))); }
      coinObjs.forEach(c => { c.visible = false; }); let ci = 0;
      for (const a of coinsAt) { const u = (t - a) / 0.26; if (u >= -0.5 && u < 1 && ci < 2) { const c = coinObjs[ci++]; c.visible = true; const w = clamp01(u); c.position.set(SLOT[0], SLOT[1] + 0.012, SLOT[2] + 0.17 * (1 - w * w)); c.rotation.set(0, 0, PI / 2); c.scale.setScalar(1.3 * (u < 0 ? 1 : 1 - 0.35 * w)); } }
    };
    g.userData.update(-1); return g;
  },

  // The big bright can on its own (pivot at its middle, upright): the same one, to hold (attach to a hand) after it drops
  bigCan(o) { return grp(bigCanMesh(o)); },

  // A brass BANQUE plate on its own (front +Z, origin at its centre; o.w 0.42, o.h 0.11): from o.popAt it pops on with an overshoot; o.glint [t...]
  banquePlaque(o) {
    const g = grp(), p = grp(brassPlate(o.w ?? 0.42, o.h ?? 0.11, o.text || 'BANQUE')); g.add(p);
    const gl = new THREE.Mesh(new THREE.PlaneGeometry(0.045, 0.15), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0, depthWrite: false })); gl.rotation.z = 0.5; gl.position.z = 0.012; p.add(gl);
    g.userData.update = t => { const u = o.popAt == null ? 1 : (t - o.popAt) / 0.28; p.visible = u >= 0; const sc = u < 0 ? 0.01 : Math.max(0.01, outBack(u)), sq = u > 0.55 && u < 1.6 ? 0.28 * Math.sin((u - 0.55) / 1.05 * PI) * Math.exp(-(u - 0.55) * 1.5) : 0; p.scale.set(sc * (1 + sq), sc * (1 - sq), sc); p.rotation.z = u < 1 && u >= 0 ? 0.5 * (1 - u) : 0;
      let gk = -1; for (const a of [].concat(o.glint ?? [])) { const v = (t - a) / 0.35; if (v >= 0 && v < 1) gk = v; } gl.material.opacity = gk >= 0 ? 0.7 * Math.sin(gk * PI) : 0; gl.position.x = (o.w ?? 0.42) * (-0.5 + Math.max(0, gk)); };
    g.userData.update(-1); return g;
  },

  // The corridor (pivot on the floor at the foot of the back wall's middle; the wall runs along X at z 0, its face toward +Z): a blue-grey wall o.h
  // (3.0) high and o.len (18) long with a darker dado and a skirting, a pale lino floor with a tile grid o.depth (12) deep toward +Z, a ceiling with
  // light panels, a door far left (o.doorX), a cork board with blank memos (o.boardX), a plant; o.side: a side wall at that x (facing -X/+X by sign)
  corridor(o) {
    const L = o.len ?? 18, Hh = o.h ?? 3.0, Dp = o.depth ?? 12, g = grp(), WALL = o.wall || '#9FB7D0', DADO = o.dado || '#6F8AA8';
    g.add(at(box(L, Hh, 0.2, WALL, { pivot: 'bottom' }), 0, 0, -0.1));
    g.add(at(box(L, 0.95, 0.02, DADO, { pivot: 'bottom' }), 0, 0, 0.01), at(box(L, 0.04, 0.04, '#4E6680'), 0, 0.95, 0.02), at(box(L, 0.1, 0.03, '#3A4250', { pivot: 'bottom' }), 0, 0, 0.025));
    const cv = document.createElement('canvas'); cv.width = cv.height = 128; const x = cv.getContext('2d'); x.fillStyle = o.floor || '#C9C6B6'; x.fillRect(0, 0, 128, 128);
    x.fillStyle = 'rgba(80,80,70,0.25)'; x.fillRect(0, 0, 128, 3); x.fillRect(0, 0, 3, 128); x.fillStyle = 'rgba(255,255,255,0.07)'; x.fillRect(20, 30, 50, 40);
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.repeat.set(L / 0.6, Dp / 0.6);
    const fl = new THREE.Mesh(new THREE.BoxGeometry(L, 0.1, Dp), new THREE.MeshLambertMaterial({ map: tex })); fl.position.set(0, -0.05, Dp / 2); fl.receiveShadow = true; g.add(fl);
    g.add(at(box(L, 0.1, Dp, '#E8E6E0'), 0, Hh + 0.05, Dp / 2));
    for (let i = -3; i <= 3; i++) g.add(at(box(1.2, 0.03, 0.5, '#FFFFFF', { emissive: '#FFF6DA', noGrain: true }), i * 2.6, Hh - 0.01, 1.2));
    const dx = o.doorX ?? -5.2; g.add(at(box(1.0, 2.15, 0.06, '#7A8C9A', { pivot: 'bottom', outline: 0.006 }), dx, 0, 0.03), at(box(1.12, 2.22, 0.04, '#3A4250', { pivot: 'bottom' }), dx, 0, 0.01), at(box(0.12, 0.03, 0.05, '#D9DDE2'), dx + 0.36, 1.05, 0.08));
    const bx = o.boardX ?? 3.6; g.add(at(box(1.1, 0.75, 0.03, '#B98A5A', { outline: 0.006 }), bx, 1.7, 0.02));
    [[-0.3, 0.12, 0.05, '#F7F3EA'], [0.05, -0.1, -0.04, '#F2E27A'], [0.33, 0.1, 0.03, '#F7F3EA'], [-0.12, -0.18, 0.02, '#BFE0F2']].forEach(([px, py, rz, c]) => g.add(at(box(0.22, 0.28, 0.008, c), bx + px, 1.7 + py, 0.04, 0, 0, rz)));
    const px = o.plantX ?? -3.4; g.add(at(cyl(0.18, 0.14, 0.38, '#C8643A', 10, { pivot: 'bottom', outline: 0.008 }), px, 0, 0.35));
    for (let i = 0; i < 7; i++) g.add(at(box(0.08, 0.6, 0.02, '#4E8A4A', { pivot: 'bottom' }), px + Math.cos(i * 2.4) * 0.05, 0.35, 0.35 + Math.sin(i * 2.4) * 0.05, Math.sin(i * 1.3) * 0.4, i * 0.9, Math.cos(i * 1.7) * 0.4));
    if (o.side != null) g.add(at(box(0.2, Hh, Dp, WALL, { pivot: 'bottom' }), o.side, 0, Dp / 2));
    return g;
  },

  // The small sandwich machine (pivot at the floor under its middle, front +Z; 0.78 m wide, 1.5 m tall): a teal cabinet, a glass with three rows of
  // triangle sandwiches, a small panel; o.crush [[t, v], ...] (0..1): squashed flat by a weight from the top-left (v 1: a drawn flat shape 9 cm thick,
  // 30 % wider, a sandwich or two poking out, a dark ink outline round it); o.flat: crushed from the start
  sandwichMachine(o) {
    const W = 0.78, H = 1.5, D = 0.62, C = o.color || '#2E8C7E', g = grp(), body = grp(); g.add(body);
    body.add(at(box(W, H, D, C, { pivot: 'bottom', outline: 0.012, unique: true }), 0, 0, 0));
    body.add(at(box(0.5, 0.9, 0.012, '#2A2C31'), -0.08, 0.85, D / 2 + 0.004), at(new THREE.Mesh(new THREE.PlaneGeometry(0.46, 0.86), new THREE.MeshLambertMaterial({ color: '#DCEFF4', transparent: true, opacity: 0.2, depthWrite: false })), -0.08, 0.85, D / 2 + 0.012));
    const sw = []; for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) sw.push([-0.24 + c * 0.16, 0.5 + r * 0.28, D / 2 - 0.01]);
    for (const [px, py, pz] of sw) { const s = grp(at(box(0.12, 0.012, 0.06, '#F3E3B8'), 0, 0.05, 0), at(box(0.12, 0.016, 0.062, '#6BB04A'), 0, 0.038, 0), at(box(0.12, 0.014, 0.06, '#F2A0A0'), 0, 0.024, 0), at(box(0.12, 0.012, 0.06, '#F3E3B8'), 0, 0.01, 0)); s.position.set(px, py, pz); s.rotation.z = 0.0; body.add(s); }
    body.add(at(box(0.16, 0.5, 0.012, '#2A2A2E'), 0.26, 0.95, D / 2 + 0.004), at(box(0.06, 0.08, 0.01, '#C9CCD1'), 0.26, 0.9, D / 2 + 0.01), at(box(0.5, 0.16, 0.03, '#141416'), -0.08, 0.2, D / 2 + 0.005));
    const ink = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ color: '#1C1C20' })); ink.rotation.x = -PI / 2; ink.position.y = 0.003; ink.visible = false; g.add(ink);
    const bits = []; [[-0.55, 0.3, 0.6], [0.5, -0.1, -0.5], [0.15, 0.42, 1.9]].forEach(([px, pz, ry]) => { const s = grp(at(box(0.16, 0.014, 0.08, '#F3E3B8'), 0, 0.03, 0), at(box(0.16, 0.016, 0.082, '#6BB04A'), 0, 0.016, 0)); s.position.set(px, 0, pz); s.rotation.y = ry; s.visible = false; g.add(s); bits.push(s); });
    g.userData.update = t => { const v = o.flat ? 1 : kv(o.crush, t, 0), e = v; body.scale.set(1 + 0.32 * e, Math.max(0.06, 1 - 0.94 * e), 1 + 0.12 * e); body.rotation.z = 0.04 * Math.sin(e * PI);
      ink.visible = e > 0.9; ink.scale.set(W * 1.32 + 0.06, D * 1.12 + 0.06, 1); bits.forEach(b => { b.visible = e > 0.85; }); };
    g.userData.update(-1); return g;
  },

  // One big bright sandwich (pivot at its middle on the floor; a triangle o.s (1: 0.34 m a side) of white bread with lettuce, ham and cheese showing
  // at its long edge toward +Z)
  bigSandwich(o) {
    const s = o.s ?? 1, g = grp(), sh = new THREE.Shape(); sh.moveTo(-0.17, -0.1); sh.lineTo(0.17, -0.1); sh.lineTo(0, 0.19); sh.closePath();
    const layer = (y, h, c, sc = 1) => { const m = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: h, bevelEnabled: false }), mat(c, { noGrain: true })); m.rotation.x = -PI / 2; m.position.y = y; m.scale.set(sc, sc, 1); m.castShadow = true; return m; };
    const b1 = layer(0, 0.035, '#F6E7BE'), l = layer(0.035, 0.02, '#5DBB3E', 1.06), hm = layer(0.055, 0.022, '#F28A9A', 1.03), ch = layer(0.077, 0.016, '#FFD23A', 1.05), b2 = layer(0.093, 0.035, '#F6E7BE');
    addOutline(b1, 0.03); addOutline(b2, 0.03); g.add(b1, l, hm, ch, b2); g.scale.setScalar(s); return g;
  },

  // The chart of the press room (pivot at the foot of the easel, front +Z): a white sheet o.w (1.0) wide and 1.5 tall on a wooden easel: from the top a
  // drawn red vending machine (a glass with rows, a slot), a big black equals sign, a drawn bank (a pediment, four columns, three steps); no words.
  // o.flipAt: a blank cover sheet flips up over the top to show it; o.eqPop t: the equals sign throbs once
  bankChart(o) {
    const Wd = o.w ?? 1.0, Hd = Wd * 1.5, g = grp(), wood = '#8A5A34', y0 = 0.75;
    for (const s of [-1, 1]) g.add(at(box(0.05, y0 + Hd + 0.15, 0.05, wood, { pivot: 'bottom', outline: 0.01 }), s * (Wd / 2 - 0.06), 0, 0.06, -0.06, 0, -s * 0.05));
    g.add(at(box(0.05, 1.5, 0.05, wood, { pivot: 'bottom' }), 0, 0, -0.42, 0.29, 0, 0), at(box(Wd + 0.1, 0.06, 0.12, wood, { outline: 0.01 }), 0, y0, 0.12));
    g.add(at(box(Wd + 0.04, Hd + 0.04, 0.03, '#3A3A3E'), 0, y0 + Hd / 2, 0.08));
    const sheet = canvasPlane(Wd, Hd, (c, W, H) => {
      c.fillStyle = '#FBFAF5'; c.fillRect(0, 0, W, H); c.lineJoin = 'round'; c.lineCap = 'round';
      const ink = '#1C1C22', lw = W * 0.018;
      // the vending machine (top third)
      const mx = W * 0.33, my = H * 0.06, mw = W * 0.34, mh = H * 0.24;
      c.fillStyle = '#D8333A'; c.fillRect(mx, my, mw, mh); c.strokeStyle = ink; c.lineWidth = lw; c.strokeRect(mx, my, mw, mh);
      c.fillStyle = '#BFE3EE'; c.fillRect(mx + mw * 0.08, my + mh * 0.1, mw * 0.55, mh * 0.62); c.strokeRect(mx + mw * 0.08, my + mh * 0.1, mw * 0.55, mh * 0.62);
      c.lineWidth = lw * 0.6; for (let i = 1; i < 4; i++) { c.beginPath(); c.moveTo(mx + mw * 0.08, my + mh * (0.1 + 0.155 * i)); c.lineTo(mx + mw * 0.63, my + mh * (0.1 + 0.155 * i)); c.stroke(); }
      c.fillStyle = ink; c.fillRect(mx + mw * 0.76, my + mh * 0.35, mw * 0.05, mh * 0.12); c.fillRect(mx + mw * 0.1, my + mh * 0.8, mw * 0.5, mh * 0.1);
      // the equals sign
      c.fillStyle = ink; const ey = H * 0.37, ew = W * 0.42; c.fillRect(W / 2 - ew / 2, ey, ew, H * 0.035); c.fillRect(W / 2 - ew / 2, ey + H * 0.07, ew, H * 0.035);
      // the bank (bottom)
      const bx = W * 0.14, by = H * 0.52, bw = W * 0.72, bh = H * 0.3;
      c.fillStyle = '#E9E2CF'; c.strokeStyle = ink; c.lineWidth = lw;
      c.beginPath(); c.moveTo(bx, by + bh * 0.28); c.lineTo(bx + bw / 2, by); c.lineTo(bx + bw, by + bh * 0.28); c.closePath(); c.fill(); c.stroke();
      c.fillRect(bx + bw * 0.03, by + bh * 0.28, bw * 0.94, bh * 0.08); c.strokeRect(bx + bw * 0.03, by + bh * 0.28, bw * 0.94, bh * 0.08);
      for (let i = 0; i < 4; i++) { const cx = bx + bw * (0.14 + i * 0.24); c.fillRect(cx - bw * 0.05, by + bh * 0.36, bw * 0.1, bh * 0.44); c.strokeRect(cx - bw * 0.05, by + bh * 0.36, bw * 0.1, bh * 0.44); }
      for (let i = 0; i < 3; i++) { const sx = bx + bw * (0.0 - i * 0.03), sw = bw * (1.0 + i * 0.06); c.fillRect(sx, by + bh * (0.8 + i * 0.067), sw, bh * 0.067); c.strokeRect(sx, by + bh * (0.8 + i * 0.067), sw, bh * 0.067); }
    }, { res: 512 });
    sheet.position.set(0, y0 + Hd / 2, 0.1); g.add(sheet);
    const cover = grp(), cs = canvasPlane(Wd, Hd, (c, W, H) => { c.fillStyle = '#F4F1E6'; c.fillRect(0, 0, W, H); c.strokeStyle = 'rgba(0,0,0,0.12)'; c.lineWidth = 4; c.strokeRect(6, 6, W - 12, H - 12); }, { res: 256 });
    cs.position.y = -Hd / 2; cover.add(cs); cover.position.set(0, y0 + Hd, 0.106); g.add(cover);
    g.userData.update = t => { const u = o.flipAt == null ? -1 : (t - o.flipAt) / 0.3; const a = clamp01(u); cover.rotation.x = -PI * 0.97 * (a < 1 ? a * a * (3 - 2 * a) : 1); cover.visible = !(o.flipAt == null && o.open); };
    g.userData.update(-1); return g;
  },

  // A heap of gold coins (pivot at its foot): a gold mound o.R (0.5) wide, o.H (0.35) high with loose coins on it and around; o.grow [t0, t1]: it piles up
  goldHeap(o) {
    const R0 = o.R ?? 0.5, H0 = o.H ?? 0.35, rr = rng(o.seed || 7), g = grp(), inner = grp(); g.add(inner);
    const mound = new THREE.Mesh(new THREE.ConeGeometry(R0, H0, 18, 3), mat('#D9A830', { noGrain: true })); mound.position.y = H0 / 2; mound.castShadow = mound.receiveShadow = true;
    const pos = mound.geometry.attributes.position; for (let i = 0; i < pos.count; i++) { const y = pos.getY(i); if (y < H0 / 2 - 0.001 && y > -H0 / 2 + 0.001) { pos.setX(i, pos.getX(i) * (0.9 + rr() * 0.2)); pos.setZ(i, pos.getZ(i) * (0.9 + rr() * 0.2)); } }
    mound.geometry.computeVertexNormals(); inner.add(mound);
    const list = [], cols = []; const n = o.n ?? 140; for (let i = 0; i < n; i++) { const a = rr() * TAU, u = Math.sqrt(rr()) * 1.25, d = u * R0, y = u < 1 ? H0 * (1 - u) + 0.006 : 0.004; list.push([Math.cos(a) * d, y, Math.sin(a) * d, (rr() - 0.5) * 1.0, rr() * TAU, (rr() - 0.5) * 1.0]); cols.push(['#F2C84A', '#E2B53C', '#FFDB6A', '#C99A2A'][i % 4]); }
    inner.add(inst(new THREE.CylinderGeometry(0.04, 0.04, 0.008, 10), new THREE.MeshLambertMaterial({ color: '#FFFFFF' }), list, cols));
    g.userData.update = t => { if (!o.grow) return; const [a, b] = o.grow, k = Math.max(0.02, clamp01((t - a) / (b - a))); inner.scale.set(0.5 + 0.5 * k, k, 0.5 + 0.5 * k); };
    g.userData.update(-1); return g;
  },

  // A stream of gold coins pouring (world space): from o.from to o.to between o.t0 and o.t1, o.n (24) coins in flight at a time, falling with gravity
  // (a parabola from o.from with the horizontal speed it needs), spinning; o.spread (0.06 m); o.path [[t, from, to], ...]: both ends move (linear
  // between keys: a sack that follows a funnel's mouth)
  coinStream(o) {
    const g = grp(), n = o.n ?? 24, A = [...(o.from || [0, 1.5, 0])], B = [...(o.to || [0, 0.5, 0])], sp = o.spread ?? 0.06, coins = [];
    const ends = t => { const P = o.path; if (!P || !P.length) return; let i = 0; while (i < P.length - 1 && t >= P[i + 1][0]) i++; const a = P[i], b = P[Math.min(i + 1, P.length - 1)], u = b === a ? 0 : clamp01((t - a[0]) / Math.max(1e-4, b[0] - a[0]));
      for (let j = 0; j < 3; j++) { A[j] = a[1][j] + (b[1][j] - a[1][j]) * u; B[j] = a[2][j] + (b[2][j] - a[2][j]) * u; } };
    const m = mat('#F0C440', { noGrain: true });
    for (let i = 0; i < n; i++) { const c = at(cyl(0.032, 0.032, 0.007, '#F0C440', 10, { material: m }), 0, 0, 0); c.castShadow = false; g.add(c); coins.push(c); }
    ends(0); const T = Math.sqrt(Math.max(0.02, 2 * (A[1] - B[1]) / 9.8));
    g.userData.update = t => { ends(t); coins.forEach((c, i) => { const ph = i / n, cyc = (t - (o.t0 ?? 0)) / T + ph, born = (o.t0 ?? 0) + (Math.floor(cyc) - ph) * T; const u = cyc - Math.floor(cyc);
        c.visible = t >= (o.t0 ?? 0) && born + T * 0.0 < (o.t1 ?? 9) && born >= (o.t0 ?? 0) - T; if (!c.visible) return; const tt = u * T;
        c.position.set(A[0] + (B[0] - A[0]) * u + (hsh(i) - 0.5) * sp, A[1] - 0.5 * 9.8 * tt * tt, A[2] + (B[2] - A[2]) * u + (hsh(i + 3) - 0.5) * sp); c.rotation.set(t * 11 + i, t * 7 + i * 2, 0); }); };
    g.userData.update(-1); return g;
  },

  // A gold coin rolling on its edge (world space; pivot on the floor): from o.from [x, z] toward o.to [x, z] between o.t0 and o.t1 (slowing down,
  // wobbling more as it slows), then it topples flat (o.fall, 0.35 s after o.t1) with a short rattle; o.r (0.05 m); before o.t0 it sits on its edge at
  // o.from (o.hidden: not shown before o.t0)
  rollCoin(o) {
    const r = o.r ?? 0.05, g = grp(), spin = grp(), tilt = grp(); g.add(tilt); tilt.add(spin);
    const c = cyl(r, r, r * 0.16, '#E8BE3E', 20, { unique: true, noGrain: true }); addOutline(c, 0.04); c.rotation.x = PI / 2; spin.add(c);
    spin.add(at(cyl(r * 0.7, r * 0.7, r * 0.17, '#D2A42E', 16, { noGrain: true }), 0, 0, 0, PI / 2, 0, 0));
    const A = o.from || [0, 0], B = o.to || [1, 0], L = Math.hypot(B[0] - A[0], B[1] - A[1]), ux = (B[0] - A[0]) / L, uz = (B[1] - A[1]) / L, cv = o.curve ?? 0.12, W0 = o.wob ?? 0.6;
    const at_ = u => { const d = L * u, side = cv * Math.sin(u * PI); return [A[0] + ux * d - uz * side, A[1] + uz * d + ux * side]; };
    g.userData.update = t => { const t0 = o.t0 ?? 0, t1 = o.t1 ?? 1, v = clamp01((t - t0) / Math.max(0.01, t1 - t0)), u = 1 - Math.pow(1 - v, 2.2);
      g.visible = !(o.hidden && t < t0); const p = at_(u), q = at_(Math.min(1, u + 0.01)); g.position.set(p[0], 0, p[1]); g.rotation.y = Math.atan2(q[0] - p[0], q[1] - p[1]) + PI / 2;
      spin.rotation.z = -u * L / r;
      const w = t - t1; let tx = (v > 0 && v < 1 ? 0.05 + 0.12 * v * v : 0) * Math.sin(t * 22);
      if (w > 0) { if (w < W0) { const k = w / W0, ph = 2 * PI * (2.5 * k + 1.8 * k * k); tx = (0.12 + 0.55 * k * k) * Math.sin(ph); } else { const f = clamp01((w - W0) / 0.14); tx = (PI / 2 - 0.02) * f * f; } }
      tilt.rotation.x = tx; const rat = w > W0 + 0.14 ? 0.03 * Math.sin((w - W0) * 70) * Math.exp(-(w - W0 - 0.14) * 9) : 0; tilt.rotation.z = rat;
      tilt.position.y = r * Math.cos(Math.abs(tilt.rotation.x)) + r * 0.08 * Math.sin(Math.abs(tilt.rotation.x)); };
    g.userData.update(-1); return g;
  },

  // A plain money sack (pivot at its neck, the bag hanging down -Y; no sign): burlap, tied with a cord; o.open: the neck open with coins showing
  plainSack(o) {
    const s = o.s ?? 1, g = grp(), C = o.color || '#B08A58';
    const bag = new THREE.Mesh(new THREE.SphereGeometry(0.2, 10, 8), mat(C)); bag.scale.set(1.0, 1.15, 0.9); bag.position.y = -0.24; bag.castShadow = true; addOutline(bag, 0.03); g.add(bag);
    g.add(at(cyl(0.07, 0.12, 0.12, C, 10, { outline: 0.01 }), 0, -0.02, 0), at(torus_(0.075, 0.012, '#5A3A1E'), 0, -0.04, 0, PI / 2, 0, 0));
    if (o.open) g.add(at(cyl(0.065, 0.065, 0.01, '#E8BE3E', 12, { noGrain: true }), 0, 0.045, 0));
    g.scale.setScalar(s); g.userData.grip = [0, 0, 0]; return g;
  },

  // A plain wooden crate to stand on (pivot at the floor under its middle; 0.6 x o.h (0.42) x 0.5): slats and two dark bands, no marking
  woodCrate(o) {
    const h = o.h ?? 0.42, g = grp(at(box(0.6, h, 0.5, '#B07A44', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0));
    for (const y of [0.3, 0.7]) g.add(at(box(0.61, 0.03, 0.51, '#7A5028'), 0, h * y, 0));
    g.add(at(box(0.62, 0.02, 0.52, '#8E6034'), 0, h - 0.01, 0)); return g;
  },

  // An open-top metal coin box (pivot at its middle; its open top toward +Y): grey steel, the dark empty inside, a handle on its front
  coinBox(o) {
    const w = 0.32, h = 0.26, d = 0.26, g = grp(), C = '#9AA2AA';
    g.add(at(box(w, 0.014, d, C, { outline: 0.02 }), 0, -h / 2, 0));
    for (const s of [-1, 1]) g.add(at(box(0.014, h, d, C, { outline: 0.02 }), s * w / 2, 0, 0), at(box(w, h, 0.014, C, { outline: 0.02 }), 0, 0, s * d / 2));
    g.add(at(box(w - 0.02, 0.004, d - 0.02, '#585E66'), 0, -h / 2 + 0.01, 0));
    for (const s of [-1, 1]) g.add(at(box(0.004, h - 0.02, d - 0.02, '#6C727A'), s * (w / 2 - 0.009), 0, 0), at(box(w - 0.02, h - 0.02, 0.004, '#646A72'), 0, 0, s * (d / 2 - 0.009)));
    for (const [x, z] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) g.add(at(box(0.02, 0.02, 0.02, '#C9CED4'), x * w / 2, h / 2, z * d / 2));
    g.add(at(box(w + 0.01, 0.016, 0.016, '#C9CED4'), 0, h / 2, d / 2), at(box(w + 0.01, 0.016, 0.016, '#C9CED4'), 0, h / 2, -d / 2));
    for (let i = 0; i < 6; i++) g.add(at(box(0.014, 0.003, 0.014, '#9A9282'), (hsh(i) - 0.5) * w * 0.7, -h / 2 + 0.014, (hsh(i + 5) - 0.5) * d * 0.7));
    g.add(at(box(0.12, 0.024, 0.03, '#2A2A2E'), 0, h * 0.15, d / 2 + 0.02));
    return g;
  },

  // A tall leaning tower of nested white plastic coffee cups (pivot at its foot): o.n (24) cups, o.size (1.6: cups 0.15 m tall, 0.115 m a step),
  // a slight S-curve; o.sway (0.02 rad) a slow wobble; the whole tower leans by the prop's own rotation
  cupStack(o) {
    const n = o.n ?? 24, Z = o.size ?? 1.6, g = grp(), step = 0.072 * Z, rT = 0.042 * Z, rB = 0.03 * Z, hC = 0.095 * Z, cups = [];
    const geo = new THREE.CylinderGeometry(rT, rB, hC, 14, 1, true), m1 = new THREE.MeshLambertMaterial({ color: '#F4F2EC', side: THREE.DoubleSide }), m2 = new THREE.MeshLambertMaterial({ color: '#E2DED4', side: THREE.DoubleSide });
    const rimG = new THREE.TorusGeometry(rT, 0.004 * Z, 4, 14), rimM = mat('#C9C4B8');
    let parent = g;
    for (let i = 0; i < n; i++) { const c = grp(); const b = new THREE.Mesh(geo, i % 2 ? m1 : m2); b.position.y = hC / 2; b.castShadow = true; c.add(b); const rm = new THREE.Mesh(rimG, rimM); rm.rotation.x = PI / 2; rm.position.y = hC; c.add(rm);
      c.position.y = i ? step : 0; c.rotation.z = 0.012 * Math.sin(i * 0.5); parent.add(c); parent = c; cups.push(c); }
    const top = new THREE.Mesh(new THREE.CircleGeometry(rT * 0.95, 14), mat('#5A3A22')); top.rotation.x = -PI / 2; top.position.y = hC - 0.01; cups[n - 1].add(top);
    g.userData.update = t => { cups.forEach((c, i) => { c.rotation.z = 0.012 * Math.sin(i * 0.5) + (o.sway ?? 0.02) * 0.08 * Math.sin(t * 2.1 + i * 0.3); }); };
    g.userData.update(0); return g;
  },

  // The clerk's counter (pivot at the floor under its middle, the customer's side +Z): a pale wooden counter o.w (1.3) wide, 1.0 high, with a glass
  // window 0.8 tall standing on it in a dark frame, a half-moon gap at its foot; o.sheetAt [t0, t1]: a sheet slides out through the gap toward +Z
  // with a red REFUSÉ stamp on it
  glassCounter(o) {
    const W = o.w ?? 1.3, g = grp();
    g.add(at(box(W, 0.98, 0.55, o.color || '#C9A27A', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(W + 0.06, 0.05, 0.62, '#7A5A3C', { pivot: 'bottom' }), 0, 0.98, 0.0));
    g.add(at(box(W - 0.2, 0.06, 0.02, '#A8825C'), 0, 0.5, 0.28));
    const gy = 1.03, gh = 0.8;
    g.add(at(box(W, 0.04, 0.05, '#2A2C31'), 0, gy + gh, -0.05), at(box(0.04, gh, 0.05, '#2A2C31', { pivot: 'bottom' }), -W / 2 + 0.02, gy, -0.05), at(box(0.04, gh, 0.05, '#2A2C31', { pivot: 'bottom' }), W / 2 - 0.02, gy, -0.05));
    g.add(at(new THREE.Mesh(new THREE.PlaneGeometry(W - 0.04, gh - 0.08), new THREE.MeshLambertMaterial({ color: '#DCEFF4', transparent: true, opacity: 0.18, depthWrite: false, side: THREE.DoubleSide })), 0, gy + 0.04 + (gh - 0.08) / 2, -0.05));
    g.add(at(box(W - 0.04, 0.035, 0.05, '#2A2C31'), -0.0, gy + 0.0175, -0.05));
    g.add(at(box(0.34, 0.012, 0.01, '#141416'), 0, gy + 0.042, -0.02));
    const sheet = grp(), sheetIn = grp(); sheet.add(sheetIn); const sp = canvasPlane(0.32, 0.42, (c, W2, H2) => { c.fillStyle = '#FBFAF5'; c.fillRect(0, 0, W2, H2); c.fillStyle = '#B8BCC2'; for (let i = 0; i < 7; i++) c.fillRect(W2 * 0.12, H2 * (0.12 + i * 0.07), W2 * (0.76 - (i % 3) * 0.12), H2 * 0.022);
      c.save(); c.translate(W2 / 2, H2 * 0.7); c.rotate(-0.15); c.strokeStyle = '#D21E1E'; c.lineWidth = H2 * 0.03; c.strokeRect(-W2 * 0.45, -H2 * 0.12, W2 * 0.9, H2 * 0.24); c.fillStyle = '#D21E1E'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitFont(c, 'REFUSÉ', W2 * 0.82, Math.round(H2 * 0.2)); c.fillText('REFUSÉ', 0, H2 * 0.005); c.restore(); }, { res: 256 });
    sp.rotation.x = -PI / 2; sp.position.z = -0.21; sheetIn.add(sp, at(box(0.32, 0.002, 0.42, '#FBFAF5'), 0, -0.002, -0.21)); sheetIn.position.z = 0.21; sheet.visible = false; g.add(sheet);
    g.userData.update = t => { if (!o.sheetAt) return; const [a, b] = o.sheetAt, u = clamp01((t - a) / Math.max(0.01, b - a)); sheet.visible = t >= a; const v = smooth((t - b) / 0.3); sheet.position.set(0, 1.04, -0.3 + 0.5 * smooth(u)); sheetIn.rotation.x = (o.sheetYaw ? 1.25 : 0.7) * v; sheet.rotation.y = (o.sheetYaw ?? 0) * PI / 180 * v; sheet.scale.setScalar(1 + ((o.sheetScale ?? 1) - 1) * v); };   // o.sheetYaw (deg): it also turns that much toward the lens; o.sheetScale: grows (a cartoon cheat)   // once out it tips up toward the customer
    g.userData.update(-1); return g;
  },

  // The wall chart (front +Z, origin at its centre; o.w 1.3 x o.h 0.85): a white board in a dark frame with two plain axes and one thick blue line
  // climbing very slowly from the bottom left to a small pink piggy bank at its far right end; no labels, no digits. o.grow [t0, t1]: the line draws
  // itself out to the pig meanwhile (default: drawn)
  riseChart(o) {
    const W = o.w ?? 1.3, H = o.h ?? 0.85, g = grp(at(box(W + 0.06, H + 0.06, 0.03, '#2A2C31', { outline: 0.006 }), 0, 0, -0.016));
    const N = 12, frames = [];
    const draw = f => (c, Wc, Hc) => { c.fillStyle = '#FBFAF5'; c.fillRect(0, 0, Wc, Hc); c.strokeStyle = '#3A3D44'; c.lineWidth = Hc * 0.014; c.lineCap = 'round';
      c.beginPath(); c.moveTo(Wc * 0.08, Hc * 0.08); c.lineTo(Wc * 0.08, Hc * 0.9); c.lineTo(Wc * 0.95, Hc * 0.9); c.stroke();
      c.strokeStyle = 'rgba(58,61,68,0.15)'; c.lineWidth = Hc * 0.005; for (let i = 1; i < 5; i++) { c.beginPath(); c.moveTo(Wc * 0.08, Hc * (0.9 - i * 0.16)); c.lineTo(Wc * 0.95, Hc * (0.9 - i * 0.16)); c.stroke(); }
      const px = u => Wc * (0.1 + 0.66 * u), py = u => Hc * (0.84 - 0.5 * Math.pow(u, 1.8) - 0.008 * Math.sin(u * 40));
      c.strokeStyle = '#2C6FD8'; c.lineWidth = Hc * 0.045; c.lineJoin = 'round'; c.beginPath(); for (let i = 0; i <= 60 * f; i++) { const u = i / 60; if (i === 0) c.moveTo(px(u), py(u)); else c.lineTo(px(u), py(u)); } c.stroke();
      { const cx = Wc * 0.85, cy = py(1) - Hc * 0.02, r = Hc * 0.085; c.fillStyle = '#F2A2B8'; c.strokeStyle = '#3A2A30'; c.lineWidth = Hc * 0.01; c.beginPath(); c.ellipse(cx, cy, r * 1.25, r, 0, 0, TAU); c.fill(); c.stroke();
        c.beginPath(); c.ellipse(cx + r * 1.25, cy, r * 0.28, r * 0.36, 0, 0, TAU); c.fill(); c.stroke(); c.fillRect(cx - r * 0.7, cy + r * 0.7, r * 0.3, r * 0.5); c.fillRect(cx + r * 0.4, cy + r * 0.7, r * 0.3, r * 0.5);
        c.beginPath(); c.moveTo(cx + r * 0.2, cy - r * 0.8); c.lineTo(cx + r * 0.6, cy - r * 1.3); c.lineTo(cx + r * 0.75, cy - r * 0.7); c.fill(); c.stroke(); c.fillStyle = '#1C1D22'; c.beginPath(); c.arc(cx + r * 0.65, cy - r * 0.2, r * 0.1, 0, TAU); c.fill(); } };
    for (let i = 0; i < N; i++) { const p = canvasPlane(W, H, draw((i + 1) / N), { res: 512 }); p.visible = false; g.add(p); frames.push(p); }
    g.userData.update = t => { const u = o.grow ? clamp01((t - o.grow[0]) / Math.max(0.01, o.grow[1] - o.grow[0])) : 1; const i = Math.max(0, Math.min(N - 1, Math.ceil(u * N) - 1)); frames.forEach((f, j) => { f.visible = j === i; }); };
    g.userData.update(-1); return g;
  },

  // The hero's own painted face faintly reflected in a glossy black panel (a plane facing +Z, origin at its centre; o.w 0.1): his tall orange box
  // face drawn mirror-wise (flat-top black hair with its tuft, thin slanted brows, heavy-lidded eyes, stubble, a short flat mouth), see-through
  // (o.alpha 0.3 drawn into the canvas: the material opacity alone did not show) and cooled toward the panel, with two soft diagonal sheen streaks across it; o.drift [dx, dy, t0, t1]: it slides a little (he
  // leans in); o.blinkAt [t...]: his reflected eyes close for 0.12 s
  glassGhost(o) {
    const w = o.w ?? 0.1, h = w * (o.aspect ?? 1.3);
    const face = closed => (c, W, H) => { c.clearRect(0, 0, W, H); c.save(); c.translate(W, 0); c.scale(-1, 1);
      c.fillStyle = '#F2A868'; c.fillRect(W * 0.14, H * 0.18, W * 0.72, H * 0.8);
      if (!o.box) { c.fillStyle = '#E39456'; c.fillRect(W * 0.06, H * 0.42, W * 0.08, H * 0.16); c.fillRect(W * 0.86, H * 0.42, W * 0.08, H * 0.16); }
      c.fillStyle = '#16141A'; c.fillRect(W * 0.1, H * 0.06, W * 0.8, H * 0.17); c.beginPath(); c.moveTo(W * 0.55, H * 0.08); c.lineTo(W * 0.92, H * 0.0); c.lineTo(W * 0.86, H * 0.14); c.fill();
      c.fillRect(W * 0.1, H * 0.2, W * 0.06, H * 0.14);
      c.strokeStyle = '#2A1E18'; c.lineWidth = H * 0.018; c.lineCap = 'round';
      for (const [x0, x1, y0, y1] of [[0.24, 0.42, 0.36, 0.33], [0.58, 0.76, 0.33, 0.36]]) { c.beginPath(); c.moveTo(W * x0, H * y0); c.lineTo(W * x1, H * y1); c.stroke(); }
      for (const x of [0.33, 0.67]) { if (closed) { c.beginPath(); c.moveTo(W * (x - 0.08), H * 0.45); c.lineTo(W * (x + 0.08), H * 0.45); c.stroke(); continue; }
        c.fillStyle = '#FFFFFF'; c.beginPath(); c.ellipse(W * x, H * 0.45, W * 0.085, H * 0.035, 0, 0, TAU); c.fill(); c.fillStyle = '#16141A'; c.beginPath(); c.arc(W * (x + 0.015), H * 0.455, H * 0.024, 0, TAU); c.fill();
        c.fillStyle = '#C97A40'; c.fillRect(W * (x - 0.095), H * 0.405, W * 0.19, H * 0.03); }
      c.fillStyle = 'rgba(90,50,30,0.55)'; for (let i = 0; i < 26; i++) { c.beginPath(); c.arc(W * (0.22 + 0.56 * hsh(i)), H * (0.66 + 0.26 * hsh(i + 30)), H * 0.007, 0, TAU); c.fill(); }
      c.beginPath(); c.moveTo(W * 0.42, H * 0.76); c.lineTo(W * 0.6, H * 0.755); c.stroke(); c.restore();
      const sg = c.createLinearGradient(0, H, W, 0); sg.addColorStop(0.0, 'rgba(255,255,255,0)'); sg.addColorStop(0.42, 'rgba(255,255,255,0)'); sg.addColorStop(0.47, 'rgba(255,255,255,0.55)'); sg.addColorStop(0.52, 'rgba(255,255,255,0)'); sg.addColorStop(0.62, 'rgba(255,255,255,0)'); sg.addColorStop(0.64, 'rgba(255,255,255,0.35)'); sg.addColorStop(0.66, 'rgba(255,255,255,0)');
      c.globalCompositeOperation = 'source-atop'; c.fillStyle = sg; c.fillRect(0, 0, W, H);
      const kA = o.alpha ?? 0.3, im = c.getImageData(0, 0, W, H), d = im.data;
      for (let i = 0; i < d.length; i += 4) { const px = (i / 4) % W, py = Math.floor(i / 4 / W), dx = (px / W - 0.5) / 0.5, dy = (py / H - 0.52) / 0.5, f = kA * Math.max(0, 1 - Math.pow(Math.max(Math.abs(dx * 0.95), Math.abs(dy * 0.9)), 6)), gy = (d[i] + d[i + 1] + d[i + 2]) / 3;
        d[i] = (d[i] * 0.55 + gy * 0.45) * f; d[i + 1] = (d[i + 1] * 0.55 + gy * 0.45) * f; d[i + 2] = (d[i + 2] * 0.55 + gy * 0.45) * f; } c.putImageData(im, 0, 0); };   // dimmed, greyed and faded at the edges in the colour itself (added light)
    const mk = closed => { const q = canvasPlane(w, h, face(closed), { res: 256, transparent: true }); const map = q.material.map;
      q.material = new THREE.MeshBasicMaterial({ map, color: o.tint || '#B8CCDE', transparent: true, opacity: o.opacity ?? 1, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false });   // a reflection adds light to the black panel
      q.renderOrder = 3; q.castShadow = false; return q; };
    const a = mk(false), b = mk(true); b.visible = false;
    const g = grp(a, b);
    g.userData.update = t => { let off = [0, 0]; if (o.drift) { const [dx, dy, t0, t1] = o.drift, u = smooth((t - t0) / Math.max(0.01, t1 - t0)); off = [dx * u, dy * u]; }
      a.position.set(off[0], off[1], 0); b.position.set(off[0], off[1], 0); const cl = [].concat(o.blinkAt ?? []).some(x => t >= x && t < x + 0.12); a.visible = !cl; b.visible = cl; };
    g.userData.update(-1); return g;
  },
};

function torus_(R, r, c) { return new THREE.Mesh(new THREE.TorusGeometry(R, r, 6, 14), mat(c)); }
void rod; void sphere; void noShadow;
