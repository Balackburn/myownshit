// « La valise » (story 54, cycle 16): a man lost his suitcase at the airport; it went round the world without him (forty countries, three hundred
// flights); the airline gave a loyalty card, to the suitcase; it flies first class, he flies in the hold; yesterday it came back, with a little
// suitcase; he pays the maintenance. Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure
// function of the shot time.
import * as THREE from 'three';
import { mat, box, cyl, clamp01 } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const rnd = s => { const x = Math.sin(s * 127.1) * 43758.5453; return x - Math.floor(x); };
// a value keyed in time: [[t, v], ...], linear between keys, held outside them
const keyAt = (keys, t, d = 0) => { if (!keys || !keys.length) return d; if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) if (t < keys[i][0]) { const [t0, v0] = keys[i - 1], [t1, v1] = keys[i]; return v0 + (v1 - v0) * (t - t0) / Math.max(1e-6, t1 - t0); }
  return keys[keys.length - 1][1]; };
// a pop-in: 0 before, up to 1.3 in two frames, a damped settle on 1 by 0.2 s
const popK = u => u < 0 ? 0 : u < 0.06 ? 1.3 * u / 0.06 : u < 0.2 ? 1 + 0.3 * Math.cos((u - 0.06) / 0.14 * PI * 1.5) * (1 - (u - 0.06) / 0.14) : 1;
const unlit = pl => { pl.material = new THREE.MeshBasicMaterial({ map: pl.material.map, side: THREE.DoubleSide, toneMapped: false, transparent: !!pl.material.transparent, alphaTest: pl.material.transparent ? 0.05 : 0 }); return pl; };
const CITIES = ['PARIS', 'LE CAIRE', 'TOKYO', 'RIO', 'NEW YORK', 'SYDNEY', 'ROMA', 'OSLO', 'DAKAR', 'LIMA', 'SÉOUL', 'MEXICO', 'BOMBAY', 'LISBOA', 'NAIROBI', 'QUÉBEC'];
const STICK = ['#E8463A', '#F2C230', '#3C8DD9', '#3CB371', '#F28C28', '#9B59B6', '#FFFFFF', '#E86FA8'];

// one travel sticker (front +Z, pivot at its centre): a round or a rounded-rectangle label with a city name, seeded by i
function sticker(i, s = 1) {
  const round = rnd(i * 3.1) < 0.45, w = (round ? 0.12 : 0.15) * s, h = (round ? 0.12 : 0.085) * s, bg = STICK[i % STICK.length], fg = bg === '#FFFFFF' || bg === '#F2C230' ? '#1E2A4A' : '#FFFFFF';
  const pl = canvasPlane(w, h, (c, W, H) => {
    c.fillStyle = bg; c.strokeStyle = '#1E2A4A'; c.lineWidth = H * 0.06;
    if (round) { c.beginPath(); c.arc(W / 2, H / 2, W * 0.46, 0, TAU); c.fill(); c.stroke(); }
    else { const r = H * 0.22; c.beginPath(); c.moveTo(r, H * 0.04); c.lineTo(W - r, H * 0.04); c.quadraticCurveTo(W * 0.98, H * 0.04, W * 0.98, r); c.lineTo(W * 0.98, H - r); c.quadraticCurveTo(W * 0.98, H * 0.96, W - r, H * 0.96);
      c.lineTo(r, H * 0.96); c.quadraticCurveTo(W * 0.02, H * 0.96, W * 0.02, H - r); c.lineTo(W * 0.02, r); c.quadraticCurveTo(W * 0.02, H * 0.04, r, H * 0.04); c.fill(); c.stroke(); }
    const txt = CITIES[i % CITIES.length]; c.fillStyle = fg; c.textAlign = 'center'; c.textBaseline = 'middle';
    c.font = `900 ${Math.min(H * 0.34, W * 1.5 / Math.max(4, txt.length))}px Arial`; c.fillText(txt, W / 2, H * (round ? 0.5 : 0.52));
    c.fillStyle = fg; c.globalAlpha = 0.6; c.font = `900 ${H * 0.16}px Arial`; if (round) c.fillText('✈', W / 2, H * 0.24);
  }, { res: 256, transparent: true });
  return pl;
}

export const VALISE_PROPS = {
  // A hard-shell suitcase standing on its four wheels (front +Z, pivot at the floor): o.w 0.5 x o.h 0.68 x o.d 0.26, o.color, ribs on its front
  // shell. The front half is a lid hinged along its top edge: o.open [[t, angle rad]] swings it up and out (stood up: a hood; laid on its back with
  // rot [-PI/2, 0, 0]: a mouth that opens toward whoever is in front of it). o.handle (0..1 or [[t, k]]): the telescopic handle out; o.stickers (n)
  // travel stickers on the front, o.stickerTimes [t...] each one popping on at its time (none: all on); o.tag: a luggage tag on the carry handle,
  // 'gold' for the loyalty card in it (o.tagSwing: it swings); o.shades: dark round sunglasses on the front top (two lenses like eyes), 'mask' a pink
  // sleep mask; o.pacifier: a pink baby's dummy on the front; o.selfie: a selfie stick from its top with a phone (o.selfie the angle, rad); o.bob
  // [[t, amp]]: it hops on its wheels (rolling, or for joy).
  suitcase(o) {
    const W = o.w ?? 0.5, H = o.h ?? 0.68, D = o.d ?? 0.26, C = o.color || '#C0392B', dark = new THREE.Color(C).multiplyScalar(0.72).getStyle(), wh = 0.05;
    const g = grp(), body = grp(); g.add(body);
    body.add(at(box(W, H, D / 2, C, { outline: 0.006 }), 0, wh + H / 2, -D / 4));                       // the back shell
    body.add(at(box(W + 0.006, H + 0.006, 0.014, '#2A2D33'), 0, wh + H / 2, 0));                       // the zip band
    const hinge = grp(); hinge.position.set(0, wh + H, 0); body.add(hinge);
    const lid = grp(at(box(W, H, D / 2, C, { outline: 0.006 }), 0, -H / 2, D / 4)); hinge.add(lid);
    for (const x of [-0.28, 0, 0.28]) lid.add(at(box(0.05 * W / 0.5, H * 0.86, 0.012, dark), x * W, -H / 2, D / 2 + 0.004));   // ribs on the shell
    lid.add(at(box(W * 0.9, H * 0.9, 0.01, '#3A3F48'), 0, -H / 2, 0.006));                              // the inside of the lid (seen when it opens)
    body.add(at(box(W * 0.9, 0.012, D * 0.4, '#E9E2D2'), 0, wh + H * 0.97, -D * 0.25));                  // the lining at the top of the back shell
    body.add(at(box(W * 0.34, 0.035, 0.035, '#2A2D33', { outline: 0.004 }), 0, wh + H + 0.035, -D * 0.2));   // the carry handle
    for (const x of [-W * 0.17, W * 0.17]) body.add(at(box(0.02, 0.035, 0.02, '#2A2D33'), x, wh + H + 0.017, -D * 0.2));
    for (const x of [-W / 2 + 0.05, W / 2 - 0.05]) for (const z of [-D / 2 + 0.04, D / 2 - 0.04]) body.add(at(cyl(wh * 0.5, wh * 0.5, 0.03, '#1C1C22', 10), x, wh * 0.5, z, 0, 0, PI / 2));   // wheels
    // the telescopic handle at the back
    const tele = grp(); body.add(tele); for (const x of [-W * 0.3, W * 0.3]) tele.add(at(box(0.018, 0.5, 0.018, '#9AA3AD'), x, wh + H - 0.25, -D / 2 - 0.012));
    tele.add(at(box(W * 0.66, 0.035, 0.035, '#2A2D33', { outline: 0.004 }), 0, wh + H, -D / 2 - 0.012));
    // stickers on the lid's face
    const st = []; const n = o.stickers || 0;
    for (let i = 0; i < n; i++) { const s = sticker((o.seed ?? 0) * 17 + i, Math.min(W, H) / 0.5); const u = rnd(i * 7.3 + (o.seed ?? 0)), v = rnd(i * 4.9 + 1.7 + (o.seed ?? 0));
      s.position.set((u - 0.5) * W * 0.78, -H * (0.12 + 0.76 * v), D / 2 + 0.012 + i * 0.0006); s.rotation.z = (rnd(i * 2.3) - 0.5) * 0.7; lid.add(s); st.push(s); }
    // the luggage tag on its strap
    let tag = null;
    if (o.tag) { tag = grp(); tag.position.set(0, wh + H + 0.05, -D * 0.2 + 0.02); body.add(tag);
      tag.add(at(box(0.012, 0.1, 0.004, '#2A2D33'), 0, -0.05, 0));
      const gold = o.tag === 'gold', card = canvasPlane(0.11, 0.07, (c, Wc, Hc) => { const gr = c.createLinearGradient(0, 0, Wc, Hc); gr.addColorStop(0, gold ? '#FFE27A' : '#F4F1E8'); gr.addColorStop(0.5, gold ? '#E8B830' : '#E2DDD0'); gr.addColorStop(1, gold ? '#FFD45A' : '#F4F1E8');
        c.fillStyle = gr; c.fillRect(0, 0, Wc, Hc); c.strokeStyle = gold ? '#9A6A10' : '#8A8578'; c.lineWidth = Hc * 0.06; c.strokeRect(0, 0, Wc, Hc); c.fillStyle = gold ? '#5A3A06' : '#3A3A40'; c.textAlign = 'center'; c.textBaseline = 'middle';
        c.font = `900 ${Hc * 0.3}px Arial`; c.fillText(gold ? 'OR' : '✈', Wc / 2, Hc * 0.5); }, { res: 192 });
      card.position.set(0, -0.135, 0.006); tag.add(card, at(box(0.116, 0.076, 0.004, gold ? '#C99A20' : '#B8B2A4'), 0, -0.135, 0)); }
    // eyewear
    if (o.shades) { const ey = grp(); ey.position.set(0, -H * 0.16, D / 2 + 0.02); lid.add(ey);
      if (o.shades === 'mask') { for (const x of [-1, 1]) ey.add(at(new THREE.Mesh(new THREE.SphereGeometry(0.07 * W / 0.5, 10, 6), mat('#F5A3C0')), x * W * 0.16, 0, 0)); ey.children.forEach(q => q.scale.set(1.25, 0.75, 0.3)); ey.add(at(box(W * 1.02, 0.02, 0.02, '#F5A3C0'), 0, 0, -0.01)); }
      else { for (const x of [-1, 1]) { const l = new THREE.Mesh(new THREE.CylinderGeometry(0.06 * W / 0.5, 0.06 * W / 0.5, 0.012, 16), new THREE.MeshStandardMaterial({ color: '#141820', roughness: 0.15, metalness: 0.4 })); l.rotation.x = PI / 2; l.position.x = x * W * 0.16; ey.add(l); }
        ey.add(at(box(W * 0.12, 0.012, 0.01, '#141820'), 0, 0.02, 0), at(box(W * 1.0, 0.012, 0.012, '#141820'), 0, 0.03, -0.01)); } }
    if (o.pacifier) { const pc = grp(); pc.position.set(W * 0.2, -H * 0.3, D / 2 + 0.03); lid.add(pc);
      pc.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.035, 0.008, 6, 14), mat('#F5A3C0')), 0, 0, 0.012), at(cyl(0.05, 0.05, 0.012, '#F5A3C0', 14), 0, 0, 0, PI / 2, 0, 0), at(new THREE.Mesh(new THREE.SphereGeometry(0.022, 8, 6), mat('#F7E6B5')), 0, 0, -0.012)); }
    if (o.selfie != null && o.selfie !== false) { const a = typeof o.selfie === 'number' ? o.selfie : 0.6, sg = grp(); sg.position.set(W * 0.3, wh + H, 0); sg.rotation.z = -a; body.add(sg);
      sg.add(at(cyl(0.008, 0.008, 0.85, '#2A2D33', 6), 0, 0.425, 0), at(box(0.075, 0.14, 0.012, '#1C1C22', { outline: 0.004 }), 0, 0.88, 0.0), at(box(0.064, 0.125, 0.004, '#7FB8E8'), 0, 0.88, -0.008)); }
    g.userData.update = t => {
      hinge.rotation.x = -keyAt(o.open, t, 0);
      const hk = Array.isArray(o.handle) ? keyAt(o.handle, t, 0) : (o.handle || 0); tele.position.y = 0.42 * clamp01(hk);
      const times = o.stickerTimes; st.forEach((s, i) => { const k = times && times[i] != null ? popK(t - times[i]) : 1; s.visible = k > 0.001; s.scale.setScalar(Math.max(0.001, k)); });
      if (tag) tag.rotation.x = (o.tagSwing ?? 0.25) * Math.sin(t * 7.0) * Math.exp(-0.3 * t);
      const b = keyAt(o.bob, t, 0); body.position.y = b > 0 ? b * Math.abs(Math.sin(t * 9.0)) : 0;
    };
    g.userData.update(0); return g;
  },

  // A baggage carousel (pivot at the floor, at the middle of the oval): o.len (6) of straight belt on each side, ends of radius o.r (1.2), a belt
  // of moving steel slats (o.speed m/s along the oval; the front straight runs +X at z +o.r, the back straight -X at z -o.r), a steel island in the
  // middle and a skirt round it, a tunnel over the back straight (at x o.hatchX) whose exit, its -X face, hangs with rubber flap strips (o.flap
  // [[t, k]]: lifted outward 0..1, they sway back), a number plate o.number on both sides. o.items [[s0, color, w, h, d, stickers]]: suitcases
  // lying on the belt that ride round with it (s0: where along the oval at t = 0, from the front-left corner); g.userData.at(s) gives the point and
  // heading of the belt at arc length s, for a script to put a bag on it.
  carousel(o) {
    const Ls = o.len ?? 6, R = o.r ?? 1.2, bw = 0.62, Hb = 0.42, spd = o.speed ?? 0.55, P = 2 * Ls + TAU * R, g = grp();
    const pathAt = s => { s = ((s % P) + P) % P;
      if (s < Ls) return [-Ls / 2 + s, R, 0];                                                     // front straight, +X
      s -= Ls; if (s < PI * R) { const a = s / R; return [Ls / 2 + R * Math.sin(a), R * Math.cos(a), -a]; }   // right end
      s -= PI * R; if (s < Ls) return [Ls / 2 - s, -R, -PI];                                      // back straight, -X
      s -= Ls; const a = s / R; return [-Ls / 2 - R * Math.sin(a), -R * Math.cos(a), -PI - a]; };    // left end
    g.userData.at = s => { const [x, z, h] = pathAt(s); return { pos: [x, Hb + 0.02, z], heading: h }; };
    // the island and the skirt; (first look) the island flush with the belt: raised 0.2 m above it, it hid the far straight and whatever rode on it
    g.add(at(box(Ls, Hb, 2 * (R - bw / 2) - 0.04, '#B7BEC6', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0));
    for (const s of [-1, 1]) g.add(at(cyl(R - bw / 2 - 0.02, R - bw / 2 - 0.02, Hb, '#B7BEC6', 20), s * Ls / 2, Hb / 2, 0));
    g.add(at(box(Ls - 0.1, 0.02, 2 * (R - bw / 2) - 0.14, '#8C949D'), 0, Hb + 0.01, 0));
    const skirt = (y, h, col) => { g.add(at(box(Ls, h, 0.05, col), 0, y, R + bw / 2), at(box(Ls, h, 0.05, col), 0, y, -R - bw / 2));
      for (const s of [-1, 1]) { const ring = new THREE.Mesh(new THREE.CylinderGeometry(R + bw / 2, R + bw / 2, h, 24, 1, true, s > 0 ? 0 : PI, PI), mat(col)); ring.material.side = THREE.DoubleSide; ring.position.set(s * Ls / 2, y, 0); g.add(ring); } };
    skirt(Hb / 2, Hb, '#5E6670'); skirt(Hb + 0.015, 0.03, '#D9DEE3');
    // the slats
    const ns = Math.round(P / 0.3), slats = [];
    for (let i = 0; i < ns; i++) { const sl = box(0.27, 0.035, bw, i % 2 ? '#3A4048' : '#454C55'); sl.castShadow = false; g.add(sl); slats.push(sl); }
    // the hatch over the back straight: a tunnel along the belt (the bags ride through it toward -X), its exit hung with rubber flap strips
    // o.hatchH: the height of its mouth (a man can lean in at 1.9)
    const hx = o.hatchX ?? 0, hw = 1.3, hh = o.hatchH ?? 0.95, hatch = grp(); hatch.position.set(hx, 0, -R); g.add(hatch);
    hatch.add(at(box(hw + 0.3, 0.25, bw + 0.34, '#8C949D', { outline: 0.006 }), 0, Hb + hh + 0.12, 0));
    for (const s of [-1, 1]) hatch.add(at(box(hw + 0.3, Hb + hh, 0.15, '#8C949D', { outline: 0.006 }), 0, (Hb + hh) / 2, s * (bw / 2 + 0.095)));
    hatch.add(at(box(0.04, hh, bw, '#15181D'), hw / 2, Hb + hh / 2, 0));                                // dark inside
    const flaps = []; for (let i = 0; i < 7; i++) { const f = grp(at(box(0.012, hh - 0.03, bw / 7 - 0.008, '#2A2E34'), 0, -(hh - 0.03) / 2, 0)); f.position.set(-hw / 2 - 0.16, Hb + hh, -bw / 2 + (i + 0.5) * bw / 7); hatch.add(f); flaps.push(f); }
    if (o.number != null) for (const s of [-1, 1]) { const pl = canvasPlane(0.5, 0.3, (c, Wc, Hc) => { c.fillStyle = '#F2C230'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#1E2A4A'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${Hc * 0.72}px Arial`; c.fillText(String(o.number), Wc / 2, Hc * 0.55); }, { res: 128 });
      unlit(pl); pl.position.set(0, Hb + hh + 0.12, s * (bw / 2 + 0.18)); if (s < 0) pl.rotation.y = PI; hatch.add(pl); }
    // bags riding round
    const bags = (o.items || []).map(([s0, col, w = 0.5, h = 0.68, d = 0.26, nst = 0], i) => { const b = VALISE_PROPS.suitcase({ w, h, d, color: col, stickers: nst, seed: 40 + i });
      const holder = grp(b); b.rotation.x = -PI / 2; b.position.set(0, d / 2, (h + 0.05) / 2); g.add(holder); return [holder, s0]; });   // laid on its back, its length along the belt
    g.userData.update = t => {
      const off = spd * t;
      slats.forEach((sl, i) => { const [x, z, h] = pathAt(i * P / ns + off); sl.position.set(x, Hb + 0.012, z); sl.rotation.y = h; });
      bags.forEach(([b, s0]) => { const [x, z, h] = pathAt(s0 + off); b.position.set(x, Hb + 0.03, z); b.rotation.y = h + PI / 2; const hid = Math.abs(z + R) < 0.05 && Math.abs(x - hx) < hw / 2 + 0.1; b.visible = !hid; });
      const fk = keyAt(o.flap, t, 0); flaps.forEach((f, i) => { const sw = 0.08 * Math.sin(t * 11 + i * 0.9) * Math.exp(-3 * Math.max(0, t - (o.flap?.[o.flap.length - 1]?.[0] ?? 0))); f.rotation.z = -(1.2 * fk * (0.8 + 0.2 * Math.sin(i * 1.7)) + sw); });   // lifted out toward -X
    };
    g.userData.update(0); return g;
  },

  // The airline's gold loyalty card (front +Z, pivot at its centre): o.s (1: 0.17 x 0.107 m, twice a real card so that it reads in a hand),
  // CARTE OR, FIDÉLITÉ, a little plane, a chip; gold on both sides; o.bright: unlit (it glints)
  loyaltyCard(o) {
    const s = o.s ?? 1, w = 0.17 * s, h = 0.107 * s;
    const face = canvasPlane(w, h, (c, W, H) => { const gr = c.createLinearGradient(0, 0, W, H); gr.addColorStop(0, '#FFE58A'); gr.addColorStop(0.45, '#E3AE2A'); gr.addColorStop(0.55, '#F6D266'); gr.addColorStop(1, '#C8901C');
      c.fillStyle = gr; c.fillRect(0, 0, W, H); c.strokeStyle = '#8A5A08'; c.lineWidth = H * 0.04; c.strokeRect(H * 0.03, H * 0.03, W - H * 0.06, H - H * 0.06);
      c.fillStyle = '#4A2E04'; c.textAlign = 'left'; c.textBaseline = 'middle'; c.font = `900 ${H * 0.2}px Arial`; c.fillText('CARTE OR', W * 0.08, H * 0.24);
      c.font = `bold ${H * 0.12}px Arial`; c.fillText('FIDÉLITÉ', W * 0.08, H * 0.84); c.font = `900 ${H * 0.3}px Arial`; c.textAlign = 'right'; c.fillText('✈', W * 0.93, H * 0.3);
      c.fillStyle = '#D9C27A'; c.fillRect(W * 0.08, H * 0.42, W * 0.16, H * 0.22); c.strokeStyle = '#8A6A1A'; c.lineWidth = H * 0.015; c.strokeRect(W * 0.08, H * 0.42, W * 0.16, H * 0.22); }, { res: 384 });
    if (o.bright) unlit(face);
    const g = grp(at(box(w, h, 0.004, '#D9A42A'), 0, 0, 0)); face.position.z = 0.0025; g.add(face); return g;
  },

  // A pyramid of the desert (pivot at the middle of its base): o.base (side, 8), o.h (5.5), sand stone with darker courses
  pyramid(o) {
    const b = o.base ?? 8, h = o.h ?? 5.5, m = new THREE.Mesh(new THREE.ConeGeometry(b / Math.SQRT2, h, 4, 6), mat(o.color || '#E2BE78')); m.rotation.y = PI / 4; m.position.y = h / 2; m.castShadow = true; m.receiveShadow = true;
    const g = grp(m); for (let i = 1; i < 6; i++) { const y = h * i / 6, r = (b / Math.SQRT2) * (1 - i / 6); const ring = new THREE.Mesh(new THREE.CylinderGeometry(r + 0.01, r + 0.01, 0.06, 4, 1, true), mat('#C9A060')); ring.rotation.y = PI / 4; ring.position.y = y; g.add(ring); }
    return g;
  },

  // An airliner's cabin, inside (pivot at the floor in the middle of the aisle; the aisle runs along Z for o.len (8) m, X across, ±o.half (1.9)): a
  // navy carpet, cream walls leaning in, a row of windows on each side (blue sky, a cloud), overhead bins, a strip of ceiling lights, a curtain at
  // the far end (o.curtain: the first-class curtain, blue)
  cabinShell(o) {
    const L = o.len ?? 8, hw = o.half ?? 1.9, H = o.h ?? 2.3, g = grp();
    g.add(at(box(2 * hw, 0.04, L, '#2F3E66'), 0, -0.02, 0));                                        // carpet
    g.add(at(box(0.6, 0.005, L, '#B9A16A'), 0, 0.003, 0));                                          // the aisle runner
    for (const s of [-1, 1]) {
      const wall = box(0.06, H, L, '#EDE6D6'); wall.position.set(s * hw, H / 2, 0); wall.rotation.z = s * 0.1; g.add(wall);
      g.add(at(box(0.5, 0.42, L, '#E4DDCB', { outline: 0.005 }), s * (hw - 0.32), H - 0.3, 0));      // overhead bins
      g.add(at(box(0.5, 0.02, L, '#BFB6A2'), s * (hw - 0.32), H - 0.52, 0));
      for (let z = -L / 2 + 0.6; z < L / 2 - 0.3; z += 0.95) {
        const win = canvasPlane(0.26, 0.36, (c, W, Hh) => { const gr = c.createLinearGradient(0, 0, 0, Hh); gr.addColorStop(0, '#5FA8E8'); gr.addColorStop(1, '#BFE3FA'); c.fillStyle = '#C9C2B2'; c.fillRect(0, 0, W, Hh);
          const r = W * 0.42; c.fillStyle = gr; c.beginPath(); c.moveTo(W * 0.08, Hh * 0.28); c.quadraticCurveTo(W * 0.08, Hh * 0.06, W / 2, Hh * 0.06); c.quadraticCurveTo(W * 0.92, Hh * 0.06, W * 0.92, Hh * 0.28); c.lineTo(W * 0.92, Hh * 0.72); c.quadraticCurveTo(W * 0.92, Hh * 0.94, W / 2, Hh * 0.94); c.quadraticCurveTo(W * 0.08, Hh * 0.94, W * 0.08, Hh * 0.72); c.closePath(); c.fill();
          c.fillStyle = '#FFFFFF'; c.beginPath(); c.arc(W * 0.4, Hh * 0.6, r * 0.25, 0, TAU); c.arc(W * 0.55, Hh * 0.56, r * 0.3, 0, TAU); c.arc(W * 0.66, Hh * 0.62, r * 0.22, 0, TAU); c.fill(); void r; }, { res: 128 });
        unlit(win); win.position.set(s * (hw - 0.06), 1.25, z); win.rotation.y = -s * PI / 2; g.add(win); }
    }
    g.add(at(box(2 * hw, 0.05, L, '#F2EDE2'), 0, H, 0), at(box(0.25, 0.02, L * 0.95, '#FFF6D8', { emissive: '#FFE9B0', noGrain: true }), 0, H - 0.03, 0));   // ceiling, light strip
    if (o.curtain !== false) { for (let i = 0; i < 9; i++) g.add(at(box(0.22, H - 0.1, 0.03, i % 2 ? '#2C5AA0' : '#3466B0'), -hw + 0.25 + i * (2 * hw - 0.5) / 8, (H - 0.1) / 2, -L / 2 + 0.05)); }
    g.add(at(box(2 * hw, H, 0.06, '#E4DDCB'), 0, H / 2, -L / 2 - 0.03));
    return g;
  },

  // A first-class seat (front +Z, pivot at the floor): a wide leather armchair, tall reclined back with a headrest, broad armrests (a little screen
  // on the right one), a footrest; o.color (cognac leather)
  firstSeat(o) {
    const C = o.color || '#9A5B34', dk = new THREE.Color(C).multiplyScalar(0.7).getStyle(), g = grp();
    g.add(at(box(0.8, 0.3, 0.75, '#3A3F48', { pivot: 'bottom' }), 0, 0, 0), at(box(0.72, 0.16, 0.7, C, { pivot: 'bottom', outline: 0.006 }), 0, 0.3, 0.02));
    const back = grp(at(box(0.72, 0.95, 0.18, C, { outline: 0.006 }), 0, 0.48, 0), at(box(0.5, 0.22, 0.12, dk, { outline: 0.005 }), 0, 0.9, 0.1)); back.position.set(0, 0.42, -0.3); back.rotation.x = -0.2; g.add(back);
    for (const s of [-1, 1]) g.add(at(box(0.14, 0.28, 0.7, dk, { pivot: 'bottom', outline: 0.005 }), s * 0.43, 0.3, 0.0));
    g.add(at(box(0.1, 0.012, 0.16, '#1C2430'), 0.43, 0.585, 0.12), at(box(0.62, 0.08, 0.36, dk, { outline: 0.004 }), 0, 0.2, 0.55));
    return g;
  },

  // A champagne flute (pivot at the foot): a glass foot and stem, a tall bowl of champagne with a white head (o.level 0..1) and bubbles rising
  flute(o) {
    const g = grp(), glass = new THREE.MeshStandardMaterial({ color: '#E8F4FA', transparent: true, opacity: 0.35, roughness: 0.05, depthWrite: false });
    g.add(at(new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.006, 16), glass), 0, 0.003, 0), at(new THREE.Mesh(new THREE.CylinderGeometry(0.005, 0.005, 0.09, 8), glass), 0, 0.05, 0));
    const lev = o.level ?? 0.8, hB = 0.13; g.add(at(new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.012, hB, 16, 1, true), glass), 0, 0.095 + hB / 2, 0));
    const wine = new THREE.Mesh(new THREE.CylinderGeometry(0.012 + 0.018 * lev, 0.012, hB * lev, 14), new THREE.MeshStandardMaterial({ color: '#F3CF5A', transparent: true, opacity: 0.85, roughness: 0.2 })); wine.position.y = 0.095 + hB * lev / 2; g.add(wine);
    g.add(at(cyl(0.012 + 0.018 * lev, 0.012 + 0.018 * lev, 0.01, '#FFF8E2', 14), 0, 0.095 + hB * lev, 0));
    const bub = []; for (let i = 0; i < 6; i++) { const b = new THREE.Mesh(new THREE.SphereGeometry(0.003, 5, 4), mat('#FFFFFF')); g.add(b); bub.push(b); }
    g.userData.update = t => bub.forEach((b, i) => { const u = (t * 0.8 + rnd(i)) % 1; b.position.set((rnd(i + 3) - 0.5) * 0.012, 0.1 + u * hB * lev * 0.95, (rnd(i + 5) - 0.5) * 0.012); });
    g.userData.update(0); return g;
  },

  // A plane's cargo hold, inside (pivot at the floor in the middle; long along Z for o.len (6), ±o.half (1.6) across): dark blue-grey walls and
  // ceiling, steel ribs, a cargo net on the back wall, rollers in the floor, one bare bulb (warm, emissive) swinging a little (o.swing)
  cargoHold(o) {
    const L = o.len ?? 6, hw = o.half ?? 1.6, H = o.h ?? 1.7, g = grp();
    g.add(at(box(2 * hw, 0.04, L, '#3E4652'), 0, -0.02, 0), at(box(2 * hw, 0.05, L, '#2E3440'), 0, H, 0), at(box(2 * hw, H, 0.06, '#353C48'), 0, H / 2, -L / 2));
    for (const s of [-1, 1]) g.add(at(box(0.06, H, L, '#353C48'), s * hw, H / 2, 0));
    for (let z = -L / 2 + 0.4; z < L / 2; z += 0.7) { g.add(at(box(2 * hw, 0.08, 0.08, '#596273'), 0, H - 0.06, z)); for (const s of [-1, 1]) g.add(at(box(0.08, H, 0.08, '#596273'), s * (hw - 0.05), H / 2, z)); }
    for (let x = -hw + 0.3; x < hw; x += 0.45) g.add(at(cyl(0.03, 0.03, L, '#7A8494', 6), x, 0.03, 0, PI / 2, 0, 0));
    const net = canvasPlane(2 * hw - 0.3, H - 0.2, (c, W, Hh) => { c.clearRect(0, 0, W, Hh); c.strokeStyle = '#B8862E'; c.lineWidth = W * 0.006; for (let i = 0; i <= 12; i++) { c.beginPath(); c.moveTo(i * W / 12, 0); c.lineTo(i * W / 12, Hh); c.stroke(); } for (let j = 0; j <= 8; j++) { c.beginPath(); c.moveTo(0, j * Hh / 8); c.lineTo(W, j * Hh / 8); c.stroke(); } }, { res: 256, transparent: true });
    net.position.set(0, H / 2, -L / 2 + 0.06); g.add(net);
    const lamp = grp(at(cyl(0.006, 0.006, 0.3, '#1C1C22', 4), 0, -0.15, 0), at(new THREE.Mesh(new THREE.SphereGeometry(0.06, 10, 8), new THREE.MeshStandardMaterial({ color: '#FFE2A0', emissive: '#FFD27A', emissiveIntensity: 2.2 })), 0, -0.33, 0));
    lamp.position.set(o.lampX ?? 0, H, o.lampZ ?? 0); g.add(lamp);
    if (o.light !== false) { const l = new THREE.PointLight('#FFD9A0', o.light ?? 5, 6, 1.6); l.position.set(o.lampX ?? 0, H - 0.4, o.lampZ ?? 0); g.add(l); }
    g.userData.update = t => { lamp.rotation.z = (o.swing ?? 0.15) * Math.sin(t * 2.6); lamp.rotation.x = 0.5 * (o.swing ?? 0.15) * Math.sin(t * 1.9 + 1); };
    g.userData.update(0); return g;
  },

  // A FRAGILE label (front +Z, pivot at its centre): o.w (0.3) x 0.4 o.w, white with a red border, FRAGILE and a broken glass; o.bright: unlit
  fragileTag(o) {
    const w = o.w ?? 0.3, h = w * 0.4, pl = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.strokeStyle = '#D7262E'; c.lineWidth = H * 0.1; c.strokeRect(H * 0.06, H * 0.06, W - H * 0.12, H - H * 0.12);
      c.fillStyle = '#D7262E'; c.textAlign = 'left'; c.textBaseline = 'middle'; c.font = `900 ${H * 0.44}px Arial`; c.fillText('FRAGILE', W * 0.27, H * 0.54);
      c.strokeStyle = '#D7262E'; c.lineWidth = H * 0.06; c.beginPath(); c.moveTo(W * 0.08, H * 0.24); c.lineTo(W * 0.2, H * 0.24); c.lineTo(W * 0.17, H * 0.5); c.lineTo(W * 0.11, H * 0.5); c.closePath(); c.stroke();
      c.beginPath(); c.moveTo(W * 0.14, H * 0.5); c.lineTo(W * 0.14, H * 0.76); c.moveTo(W * 0.1, H * 0.78); c.lineTo(W * 0.18, H * 0.78); c.moveTo(W * 0.13, H * 0.24); c.lineTo(W * 0.15, H * 0.36); c.lineTo(W * 0.13, H * 0.42); c.stroke(); }, { res: 256 });
    if (o.bright) unlit(pl); return grp(pl);
  },

  // An airport terminal hall (pivot at the floor in the middle; put it in the white void): o.w (14) wide, the back wall at z o.back (-4) and the side
  // walls running to z o.front (6), o.h (5) high with a ceiling and light strips; pale tiled floor; along the back wall a band of tall windows on the
  // apron (blue sky, the tail of a parked airliner, the tarmac); two round pillars; a sign hung from the ceiling, o.sign (BAGAGES) beside a suitcase
  // icon, yellow on navy (o.signX, o.signY, o.signZ)
  terminalHall(o) {
    const W = o.w ?? 14, back = o.back ?? -4, front = o.front ?? 6, H = o.h ?? 5, L = front - back, mz = (front + back) / 2, g = grp();
    const floor = canvasPlane(W, L, (c, Wc, Hc) => { c.fillStyle = '#D3CFC6'; c.fillRect(0, 0, Wc, Hc); c.strokeStyle = '#BDB8AE'; c.lineWidth = 2; const nx = Math.round(W / 0.8), ny = Math.round(L / 0.8);
      for (let i = 0; i <= nx; i++) { c.beginPath(); c.moveTo(i * Wc / nx, 0); c.lineTo(i * Wc / nx, Hc); c.stroke(); } for (let j = 0; j <= ny; j++) { c.beginPath(); c.moveTo(0, j * Hc / ny); c.lineTo(Wc, j * Hc / ny); c.stroke(); } }, { res: 1024 });
    floor.rotation.x = -PI / 2; floor.position.set(0, 0.004, mz); floor.receiveShadow = true; g.add(floor);
    g.add(at(box(W, 0.1, L, '#C9C4BA'), 0, -0.05, mz));
    const wallC = o.wall || '#E3E8EC';
    g.add(at(box(W, H, 0.2, wallC), 0, H / 2, back - 0.1)); for (const sx of [-1, 1]) g.add(at(box(0.2, H, L, wallC), sx * (W / 2 + 0.1), H / 2, mz));
    g.add(at(box(W, 0.12, L, '#F1F3F4'), 0, H + 0.06, mz));
    for (let x = -W / 2 + 1.5; x < W / 2 - 1; x += 3) g.add(at(box(0.3, 0.03, L * 0.9, '#FFF8E6', { emissive: '#FFF0C8', noGrain: true }), x, H - 0.02, mz));
    // the windows on the apron
    const win = canvasPlane(W - 1.2, 2.4, (c, Wc, Hc) => { const gr = c.createLinearGradient(0, 0, 0, Hc); gr.addColorStop(0, '#6FB6EC'); gr.addColorStop(0.7, '#CFE9F7'); gr.addColorStop(0.71, '#7D848C'); gr.addColorStop(1, '#6A7078'); c.fillStyle = gr; c.fillRect(0, 0, Wc, Hc);
      c.fillStyle = '#FFFFFF'; [[0.15, 0.25, 0.05], [0.42, 0.18, 0.04], [0.8, 0.28, 0.06]].forEach(([x, y, r]) => { c.beginPath(); c.arc(Wc * x, Hc * y, Hc * r * 2, 0, TAU); c.arc(Wc * (x + 0.03), Hc * (y - 0.02), Hc * r * 2.4, 0, TAU); c.arc(Wc * (x + 0.06), Hc * y, Hc * r * 1.8, 0, TAU); c.fill(); });
      c.fillStyle = '#F4F5F6'; c.beginPath(); c.moveTo(Wc * 0.6, Hc * 0.7); c.lineTo(Wc * 0.66, Hc * 0.28); c.lineTo(Wc * 0.7, Hc * 0.28); c.lineTo(Wc * 0.72, Hc * 0.7); c.fill();   // a parked airliner's tail
      c.fillStyle = '#2F6FB5'; c.beginPath(); c.moveTo(Wc * 0.655, Hc * 0.36); c.lineTo(Wc * 0.665, Hc * 0.29); c.lineTo(Wc * 0.698, Hc * 0.29); c.lineTo(Wc * 0.705, Hc * 0.36); c.fill();
      c.fillStyle = '#F4F5F6'; c.fillRect(Wc * 0.3, Hc * 0.62, Wc * 0.42, Hc * 0.09); c.fillStyle = '#D9DCE0'; c.fillRect(Wc * 0.3, Hc * 0.69, Wc * 0.42, Hc * 0.02);
      c.strokeStyle = '#F2C230'; c.lineWidth = Hc * 0.012; c.setLineDash([Hc * 0.05, Hc * 0.04]); c.beginPath(); c.moveTo(0, Hc * 0.88); c.lineTo(Wc, Hc * 0.86); c.stroke(); c.setLineDash([]);
      c.fillStyle = '#5A6068'; for (let i = 0; i <= 8; i++) c.fillRect(i * Wc / 8 - Wc * 0.004, 0, Wc * 0.008, Hc); }, { res: 1024 });
    unlit(win); win.position.set(0, 2.0, back + 0.01); g.add(win);
    g.add(at(box(W, 0.9, 0.06, '#9AA4AE'), 0, 0.45, back + 0.03));
    for (const x of o.pillars || [-4.5, 4.5]) g.add(at(cyl(0.32, 0.32, H, '#EDEFF1', 16), x, H / 2, o.pillarZ ?? -1.2));
    if (o.sign !== false) { const sg = canvasPlane(2.6, 0.7, (c, Wc, Hc) => { c.fillStyle = '#1E2A4A'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#F2C230'; c.textAlign = 'left'; c.textBaseline = 'middle'; c.font = `900 ${Hc * 0.52}px Arial`; c.fillText(o.sign || 'BAGAGES', Wc * 0.3, Hc * 0.55);
        c.strokeStyle = '#F2C230'; c.lineWidth = Hc * 0.07; c.strokeRect(Wc * 0.07, Hc * 0.3, Wc * 0.15, Hc * 0.48); c.beginPath(); c.moveTo(Wc * 0.115, Hc * 0.3); c.lineTo(Wc * 0.115, Hc * 0.18); c.lineTo(Wc * 0.175, Hc * 0.18); c.lineTo(Wc * 0.175, Hc * 0.3); c.stroke(); }, { res: 512 });
      unlit(sg); const sgG = grp(at(box(2.7, 0.8, 0.06, '#141C30'), 0, 0, -0.04), sg, at(box(0.03, 0.8, 0.03, '#5A6068'), -1.0, 0.8, 0), at(box(0.03, 0.8, 0.03, '#5A6068'), 1.0, 0.8, 0)); sg.position.z = 0.002;
      sgG.position.set(o.signX ?? 0, o.signY ?? 3.6, o.signZ ?? -2.6); g.add(sgG); }
    return g;
  },

  // A check-in baggage scale beside the desk (front +Z, pivot at the floor): a low grey platform o.w (0.75) x o.d (0.6), 0.25 high, with a little
  // display on a post that reads o.kg ('23 KG')
  bagScale(o) {
    const w = o.w ?? 0.75, d = o.d ?? 0.6, g = grp(at(box(w, 0.22, d, '#8C949D', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(w - 0.06, 0.03, d - 0.06, '#3A3F48'), 0, 0.235, 0));
    g.add(at(box(0.04, 0.55, 0.04, '#5A6068', { pivot: 'bottom' }), w / 2 - 0.05, 0.22, -d / 2 + 0.05));
    const scr = canvasPlane(0.2, 0.09, (c, W, H) => { c.fillStyle = '#10151C'; c.fillRect(0, 0, W, H); c.fillStyle = '#5BE07A'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${H * 0.62}px monospace`; c.fillText(o.kg || '23 KG', W / 2, H * 0.55); }, { res: 128 });
    unlit(scr); scr.position.set(w / 2 - 0.05, 0.82, -d / 2 + 0.08); g.add(scr, at(box(0.22, 0.11, 0.04, '#2A2E34'), w / 2 - 0.05, 0.82, -d / 2 + 0.055));
    return g;
  },

  // An airport departures board (front +Z, pivot at its centre, lit like a screen): o.w (1.8) x o.h (1.1), DÉPARTS, rows of cities with times and
  // gates in yellow on black; a big counter VOLS that runs from o.from to o.to between o.t0 and o.t1 (eased out), the rows flipping as it runs
  flightBoard(o) {
    const w = o.w ?? 1.8, h = o.h ?? 1.1, g = grp(at(box(w + 0.08, h + 0.08, 0.08, '#1A1D22', { outline: 0.006 }), 0, 0, -0.045));
    const scr = canvasPlane(w, h, () => {}, { res: 512 }); unlit(scr); scr.position.z = 0.002; g.add(scr);
    const tex = scr.material.map, cv = tex.image, cx = cv.getContext('2d'); let last = -1;
    const draw = n => { const W = cv.width, H = cv.height; cx.fillStyle = '#0E1014'; cx.fillRect(0, 0, W, H);
      cx.fillStyle = '#F2C230'; cx.fillRect(0, 0, W, H * 0.14); cx.fillStyle = '#0E1014'; cx.textAlign = 'left'; cx.textBaseline = 'middle'; cx.font = `900 ${H * 0.1}px Arial`; cx.fillText('DÉPARTS', W * 0.04, H * 0.075);
      cx.textAlign = 'right'; cx.fillText('✈', W * 0.96, H * 0.075);
      cx.font = `bold ${H * 0.068}px monospace`; cx.textAlign = 'left';
      for (let r = 0; r < 5; r++) { const ci = (r + Math.floor(n / 7)) % CITIES.length, y = H * (0.22 + r * 0.095); cx.fillStyle = r % 2 ? '#1A1D24' : '#14171D'; cx.fillRect(0, y - H * 0.045, W, H * 0.09);
        cx.fillStyle = '#F2C230'; cx.fillText(`${String(6 + ((r * 3 + n) % 17)).padStart(2, '0')}:${String((r * 25 + n * 5) % 60).padStart(2, '0')}`, W * 0.04, y); cx.fillText(CITIES[ci], W * 0.24, y); cx.fillText(`${1 + (ci + r) % 9}`, W * 0.88, y); }
      cx.fillStyle = '#FFFFFF'; cx.font = `900 ${H * 0.13}px Arial`; cx.textAlign = 'left'; cx.fillText('VOLS', W * 0.06, H * 0.82); cx.textAlign = 'right'; cx.fillStyle = '#F2C230'; cx.font = `900 ${H * 0.2}px monospace`; cx.fillText(String(n), W * 0.94, H * 0.82);
      tex.needsUpdate = true; };
    g.userData.update = t => { const u = clamp01((t - (o.t0 ?? 0)) / Math.max(0.01, (o.t1 ?? 1) - (o.t0 ?? 0))), e = 1 - Math.pow(1 - u, 3), n = Math.round((o.from ?? 0) + ((o.to ?? 300) - (o.from ?? 0)) * e); if (n !== last) { last = n; draw(n); } };
    g.userData.update(0); return g;
  },
};
