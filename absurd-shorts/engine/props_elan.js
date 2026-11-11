// « L'élan » (story 41): a man runs for his bus, cannot stop, and the town hall makes a bus line of him.
// Conventions as in props.js (metres, front +Z, pivot at the floor); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, sphere, rng, ease, clamp01 } from './style.js';
import { grp, at, mesh, torus, canvasPlane, glassMat } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const txt = (g, s, x, y, px, color = '#1B1B1E', weight = '900') => { g.fillStyle = color; g.font = `${weight} ${px}px Arial`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(s, x, y); };
const fit = (g, s, w, px, weight = '900') => { g.font = `${weight} ${px}px Arial`; const m = g.measureText(s).width; return m > w ? px * w / m : px; };
const wob = (t, f = 30, d = 6) => (t <= 0 ? 0 : Math.sin(t * f) * Math.exp(-t * d));
const keyed = (keys, t, e) => { if (!keys || !keys.length) return 0; if (t <= keys[0][0]) return keys[0][1]; for (let i = 0; i < keys.length - 1; i++) { const [t0, v0] = keys[i], [t1, v1] = keys[i + 1]; if (t < t1) { const u = clamp01((t - t0) / Math.max(1e-6, t1 - t0)); return v0 + (v1 - v0) * (e ? e(u) : u); } } return keys[keys.length - 1][1]; };
const flat = (color, o = {}) => new THREE.MeshBasicMaterial({ color, toneMapped: false, fog: false, ...o });
const quad = (w, h, m) => { const q = new THREE.Mesh(new THREE.PlaneGeometry(w, h), m); q.castShadow = false; q.receiveShadow = false; return q; };
const AMBER = '#FFB02E', LEDBG = '#0D0E12';
// an amber text on a black panel (w x h metres), unlit: a bus display. The text is fitted to the panel.
const ledText = (s, w, h, res = 384, color = AMBER) => { const pl = canvasPlane(w, h, (c, W, H) => { c.fillStyle = LEDBG; c.fillRect(0, 0, W, H); txt(c, s, W / 2, H * 0.54, fit(c, s, W * 0.9, H * 0.78), color); }, { res }); pl.material = flat('#FFFFFF', { map: pl.material.map }); pl.castShadow = false; return pl; };
// the index of the text in force at t for keys [[t, text], ...] (the first one before its time)
const stepAt = (keys, t) => { let i = 0; for (let k = 0; k < keys.length; k++) if (t >= keys[k][0]) i = k; return i; };
// a pole of n short segments that bends as an arc in its XY plane: bend(a) leans the top by a radians toward +X (the first segment stays upright).
// `tip` is a group at the top that follows the bend. The same sum is done in Python (story_elan.py: pole_pt) to put a guided hand on the pole.
function arcPole(h, r, color, n = 14) {
  const root = grp(), segs = []; let parent = root;
  for (let i = 0; i < n; i++) { const j = grp(); j.position.y = i ? h / n : 0; parent.add(j); j.add(cyl(r, r, h / n * 1.06, color, 6, { pivot: 'bottom' })); segs.push(j); parent = j; }
  const tip = grp(); tip.position.y = h / n; parent.add(tip);
  // bend(a): an arc, the same curve all the way up. bend(a, grip): a pole pulled by a hand `grip` metres up: it bows from its foot (most at the foot, as a
  // rod held at one end does), and is straight above the hand, leaning by a
  const lean = (a, grip, i) => grip ? a * (1 - (1 - Math.min(1, (i * h / n) / grip)) ** 2) : a * i / (n - 1);
  return { root, tip, segs, bend: (a, grip = 0) => segs.forEach((j, i) => { j.rotation.z = i ? -(lean(a, grip, i) - lean(a, grip, i - 1)) : 0; }) };
}
// the lean of a pole at t: o.bend keys [[t, a], ...] (eased in and out) plus o.spring [[t0, a0, freq (16), damp (4.5)], ...]: let go at t0 from a0, it
// rings (a0 * cos * exp); a spring replaces the keyed value from its t0 on
const leanAt = (o, t) => { let a = keyed(o.bend, t, ease.inOut); for (const [t0, a0, f = 16, d = 4.5] of o.spring || []) if (t >= t0) a = a0 * Math.cos((t - t0) * f) * Math.exp(-(t - t0) * d); return a; };

export const ELAN_PROPS = {
  // a city bus facing +X, its doors on its right side (+Z): green skirt, a band of windows you can see through (actors stand inside on the floor,
  // y = userData.floor), a pale roof, a wide windscreen, the line display above it (o.line '12', o.dest 'GARE') and a second one above the front door.
  // o.len (7.6 m). o.doors [[t, 0..1], ...]: the two leaves of each door slide apart (1 = open). The driver sits at userData.seat (front left).
  // o.rock [[t0, amp], ...]: the body rocks on its springs from t0 (a start, a stop).
  // Open, the leaves stand o.doorOut (0.2 m) out of the flank (plug doors: they show from behind), then slide apart.
  cityBus(o) {
    const L = o.len ?? 7.6, W = 2.3, C = o.color || '#2F8F6B', C2 = o.roof || '#F1EEE3', DK = '#22252B', g = grp(), body = grp(), gl = glassMat(o.glass ?? 0.12, '#DCEFF2');
    const y0 = 0.34, yS = 1.2, yW = o.top ?? 2.3, yR = yW + 0.48, hx = L / 2, hz = W / 2;   // o.top: the top of the windows = the ceiling (2.3; a cap that jumps or a passenger who hops goes through it: 2.65 leaves them room)
    body.add(at(box(L, 0.1, W, DK), 0, y0 + 0.05, 0));                                                                  // the floor
    body.add(at(box(L, yS - y0, 0.05, C, { outline: 0.012 }), 0, (y0 + yS) / 2, -hz), at(box(0.05, yS - y0, W, C, { outline: 0.012 }), -hx, (y0 + yS) / 2, 0), at(box(0.05, yS - y0 - 0.1, W, C, { outline: 0.012 }), hx, (y0 + yS) / 2 - 0.05, 0));
    const doorsX = [hx - 1.55, -0.7], dw = 1.1;                                                                         // the centres of the two doors
    let x0 = -hx; for (const dx of [...doorsX].sort((a, b) => a - b)) { const x1 = dx - dw / 2; body.add(at(box(x1 - x0, yS - y0, 0.05, C, { outline: 0.012 }), (x0 + x1) / 2, (y0 + yS) / 2, hz)); x0 = dx + dw / 2; }
    body.add(at(box(hx - x0, yS - y0, 0.05, C, { outline: 0.012 }), (x0 + hx) / 2, (y0 + yS) / 2, hz));
    body.add(at(box(L + 0.04, yR - yW, W + 0.04, C2, { outline: 0.012 }), 0, (yW + yR) / 2, 0), at(box(L - 0.5, 0.08, W - 0.5, C2), 0, yR + 0.04, 0));   // the roof
    { const ce = quad(L - 0.12, W - 0.12, flat(o.ceiling || '#DDD8CB')); ce.rotation.x = PI / 2; ce.position.set(0, yW - 0.004, 0); body.add(ce); }   // a pale ceiling under it (unlit: the inside of the roof was a dark slab behind the driver's cap)
    const pil = []; for (let x = -hx + 0.02; x < hx - 0.6; x += 1.26) pil.push(x); pil.push(hx - 0.03);
    for (const x of pil) for (const z of [-hz, hz]) if (!doorsX.some(dx => z > 0 && Math.abs(x - dx) < dw / 2 - 0.02)) body.add(at(box(0.09, yW - yS, 0.06, C2), x, (yS + yW) / 2, z));
    body.add(at(mesh(new THREE.BoxGeometry(L - 0.1, yW - yS, 0.02), gl), 0, (yS + yW) / 2, -hz), at(mesh(new THREE.BoxGeometry(0.02, yW - yS, W - 0.1), gl), -hx, (yS + yW) / 2, 0));
    x0 = -hx; for (const dx of [...doorsX].sort((a, b) => a - b)) { const x1 = dx - dw / 2; body.add(at(mesh(new THREE.BoxGeometry(x1 - x0, yW - yS, 0.02), gl), (x0 + x1) / 2, (yS + yW) / 2, hz)); x0 = dx + dw / 2; }
    body.add(at(mesh(new THREE.BoxGeometry(hx - x0, yW - yS, 0.02), gl), (x0 + hx) / 2, (yS + yW) / 2, hz));
    body.add(at(mesh(new THREE.BoxGeometry(0.02, yW - 1.0, W - 0.16), gl), hx, (1.0 + yW) / 2, 0), at(box(0.06, 0.05, W - 0.1, DK), hx + 0.01, 1.0, 0));   // the windscreen and its sill
    const disp = ledText(`${o.line || '12'}  ${o.dest || 'GARE'}`, W * 0.8, 0.34); disp.rotation.y = PI / 2; disp.position.set(hx + 0.03, (yW + yR) / 2, 0); body.add(disp);
    const side = ledText(o.line || '12', 0.5, 0.3, 192); side.position.set(doorsX[0], (yW + yR) / 2, hz + 0.03); body.add(side);
    const rear = ledText(o.line || '12', 0.6, 0.34, 192); rear.rotation.y = -PI / 2; rear.position.set(-hx - 0.03, (yW + yR) / 2, 0.5); body.add(rear);
    const leaves = []; for (const dx of doorsX) for (const s of [-1, 1]) { const lf = grp(at(mesh(new THREE.BoxGeometry(dw / 2 - 0.02, yW - y0 - 0.1, 0.03), glassMat(o.doorGlass ?? 0.3, '#CFE6EA')), 0, 0, 0), at(box(dw / 2, 0.06, 0.05, DK), 0, -(yW - y0) / 2 + 0.06, 0), at(box(0.04, yW - y0 - 0.1, 0.05, DK), s * (dw / 4 - 0.02), 0, 0));
      lf.position.set(dx + s * dw / 4, (y0 + yW) / 2, hz); body.add(lf); leaves.push({ lf, x: dx + s * dw / 4, s }); }
    body.add(at(box(0.08, 0.32, W + 0.06, DK), hx + 0.02, 0.5, 0), at(box(0.08, 0.3, W + 0.06, DK), -hx - 0.02, 0.5, 0));                        // the bumpers
    for (const z of [-0.75, 0.75]) body.add(at(box(0.04, 0.14, 0.3, '#FFF6C8', { noGrain: true }), hx + 0.05, 0.82, z), at(box(0.04, 0.16, 0.26, P.red), -hx - 0.05, 0.86, z));
    for (const z of [-hz - 0.16, hz + 0.16]) body.add(at(box(0.05, 0.34, 0.2, DK), hx - 0.05, 2.05, z), at(box(0.04, 0.04, 0.2, DK), hx - 0.05, 2.2, z * 0.94));   // the mirrors, like two ears
    const sx = hx - 0.95, sz = -0.55;                                                                                       // the driver: front left
    body.add(at(box(0.5, 0.1, 0.5, '#3A3D44'), sx - 0.1, y0 + 0.5, sz), at(box(0.1, 0.7, 0.5, '#3A3D44'), sx - 0.36, y0 + 0.85, sz, 0, 0, 0.12), at(box(0.3, 0.5, 1.9, '#2A2A2E'), hx - 0.2, y0 + 0.36, 0),
      at(torus(0.23, 0.03, P.ink, 6, 16), sx + 0.44, y0 + 0.9, sz, 0, PI / 2, 0.5), at(cyl(0.025, 0.025, 0.34, P.ink, 6), sx + 0.53, y0 + 0.72, sz, 0, 0, -0.5));
    for (const x of [doorsX[0] - 0.75, doorsX[1] + 0.75, doorsX[1] - 0.85]) body.add(at(cyl(0.025, 0.025, yW - y0 - 0.1, '#F2C230', 6, { pivot: 'bottom' }), x, y0 + 0.1, 0.35));   // yellow poles to hold on to
    for (let x = -hx + 0.55; x < doorsX[1] - 0.8; x += 0.8) body.add(at(box(0.42, 0.08, 0.5, '#3D6FA8'), x, y0 + 0.5, -hz + 0.34), at(box(0.07, 0.5, 0.5, '#3D6FA8'), x - 0.2, y0 + 0.78, -hz + 0.34));   // seats along the far side
    g.add(body);
    for (const x of [hx - 1.55 - 0.95, -hx + 1.5]) for (const z of [-hz + 0.02, hz - 0.02]) g.add(at(cyl(0.46, 0.46, 0.3, P.ink, 14), x, 0.46, z, PI / 2), at(cyl(0.2, 0.2, 0.02, P.grey, 8), x, 0.46, z + Math.sign(z) * 0.16, PI / 2));
    g.userData.update = t => { const k = ease.inOut(clamp01(keyed(o.doors, t)));
      for (const { lf, x, s } of leaves) { lf.position.x = x + s * k * (dw / 2 - 0.06); lf.position.z = hz + (o.doorOut ?? 0.2) * Math.min(1, k * 3); }
      let rz = 0; for (const [t0, a = 0.02] of o.rock || []) rz += a * wob(t - t0, 9, 3.2); body.rotation.z = rz; body.position.y = 0.6 * Math.abs(rz); };
    g.userData.update(0); g.userData.seat = [sx - 0.1, y0 + 0.02, sz]; g.userData.floor = y0 + 0.1; g.userData.doors = doorsX.map(x => [x, y0 + 0.1, hz]); return g;
  },

  // the pole of a bus stop: a grey pole (o.h 2.75 m) with the plate of the line at its top (BUS, then o.line '12 BIS' on a coloured badge) and a framed
  // timetable at chest height. It bends as an arc toward its +X: o.bend [[t, radians], ...] (eased), o.spring [[t0, a0, freq, damp], ...] (let go at t0 from
  // a0: it rings and comes to rest). Turn the prop (ry) to choose the side it bends to. Front +Z.
  busStopPole(o) {
    const h = o.h ?? 2.75, pole = arcPole(h, 0.035, '#5B626B'), g = grp(pole.root);
    const plate = grp(at(box(0.56, 0.7, 0.04, '#2C6FB5', { outline: 0.012 }), 0, 0, 0));
    for (const s of [-1, 1]) { const top = canvasPlane(0.5, 0.26, (c, W, H) => { c.fillStyle = '#2C6FB5'; c.fillRect(0, 0, W, H); txt(c, 'BUS', W / 2, H * 0.55, H * 0.8, '#FFFFFF'); }, { res: 256 }); top.position.set(0, 0.18, s * 0.022); if (s < 0) top.rotation.y = PI;
      const bot = canvasPlane(0.5, 0.3, (c, W, H) => { c.fillStyle = '#F4F1E8'; c.fillRect(0, 0, W, H); c.fillStyle = o.badge || '#E0572E'; c.beginPath(); c.roundRect(W * 0.06, H * 0.1, W * 0.88, H * 0.8, H * 0.18); c.fill(); txt(c, o.line || '12 BIS', W / 2, H * 0.54, fit(c, o.line || '12 BIS', W * 0.78, H * 0.62), '#FFFFFF'); }, { res: 256 }); bot.position.set(0, -0.17, s * 0.022); if (s < 0) bot.rotation.y = PI;
      plate.add(top, bot); }
    plate.position.set(0, -0.32, o.plateOff ?? 0); pole.tip.add(plate);   // o.plateOff (0.06): the plate in front of its pole, not pierced by it
    const frame = grp(at(box(0.34, 0.46, 0.03, '#E9E4D6', { outline: 0.01 }), 0, 0, 0)); for (let i = 0; i < 6; i++) frame.add(at(box(0.26, 0.018, 0.005, '#8E949C'), 0, 0.16 - i * 0.06, 0.018));
    frame.position.set(0, h / 14 * 0.5 + (o.boardDy ?? 0), 0.05); pole.segs[7].add(frame);   // o.boardDy: the timetable lower on the pole
    g.userData.update = t => pole.bend(leanAt(o, t)); g.userData.update(0); return g;
  },

  // a traffic light on a pole (o.h 3.0 m): a black head with three lenses facing +Z. o.state [[t, 'r' | 'a' | 'g'], ...]: the lens lit from t (unlit
  // materials: it shows its colour in any light), with a small pop of the lens. It bends like the stop pole: o.bend / o.spring (toward its +X).
  // o.headRy (degrees): the head turned on the pole (the lenses face another way than the prop's +Z: a pole that bends along the street under a head that faces it).
  // o.bendGrip (m): the pole is pulled by a hand at that height: it bows from its foot, straight above the hand (default: one arc all the way up).
  trafficLight(o) {
    const h = o.h ?? 3.0, HC = o.housing || '#1F2228', pole = arcPole(h - 0.9, 0.05, o.poleColor || '#3A3F47'), g = grp(pole.root), head = grp(at(box(0.34, 0.92, 0.26, HC, { outline: 0.012 }), 0, 0.46, 0), at(box(0.42, 0.04, 0.3, HC), 0, 0.94, 0));   // o.poleColor, o.housing: a galvanised pole, a dark green housing (a black display next to it must not read as part of the signal)
    const COL = { r: '#FF3B2F', a: '#FFB02E', g: '#3EE06A' }, OFF = { r: '#4A1512', a: '#4A3610', g: '#12401F' }, lens = {};
    ['r', 'a', 'g'].forEach((k, i) => { const m = quad(0.2, 0.2, flat(OFF[k])); m.geometry = new THREE.CircleGeometry(0.1, 16); m.position.set(0, 0.74 - i * 0.28, 0.135); const halo = quad(0.5, 0.5, flat(COL[k], { transparent: true, opacity: 0.0, depthWrite: false })); halo.geometry = new THREE.CircleGeometry(0.15, 16); halo.position.set(0, 0.74 - i * 0.28, 0.132);
      head.add(halo, m, at(box(0.26, 0.03, 0.1, HC), 0, 0.74 - i * 0.28 + 0.115, 0.17)); lens[k] = { m, halo }; });
    head.rotation.y = (o.headRy ?? 0) * PI / 180; pole.tip.add(head);
    if (o.ped) {   // o.ped 'r' | 'g': a pedestrian signal under the main one, on the side of the prop's -Z (the road, when the lenses face up the street): a red standing man, or a green walking one
      const man = (col, y, walk) => { const c = canvasPlane(0.22, 0.24, (g2, W, H) => { g2.fillStyle = '#0D0E12'; g2.fillRect(0, 0, W, H); g2.fillStyle = col; g2.beginPath(); g2.arc(W / 2, H * 0.2, H * 0.11, 0, TAU); g2.fill(); g2.fillRect(W * 0.4, H * 0.33, W * 0.2, H * 0.34); g2.fillRect(W * (walk ? 0.3 : 0.4), H * 0.66, W * 0.09, H * 0.28); g2.fillRect(W * (walk ? 0.61 : 0.51), H * 0.66, W * 0.09, H * 0.28); }, { res: 128 }); c.material = flat('#FFFFFF', { map: c.material.map }); c.position.set(0, y, -0.102); c.rotation.y = PI; return c; };
      const pb = grp(at(box(0.3, 0.56, 0.2, HC, { outline: 0.01 }), 0, 0, 0), man(o.ped === 'g' ? '#4A1512' : '#FF3B2F', 0.135, false), man(o.ped === 'g' ? '#3EE06A' : '#12401F', -0.135, true)); pb.position.set(0, -0.42, -0.16); pole.tip.add(pb);
    }
    const st = o.state || [[0, 'r']];
    g.userData.update = t => { pole.bend(leanAt(o, t), o.bendGrip || 0); const i = stepAt(st, t), on = st[i][1], u = t - st[i][0];   // o.bendGrip (m): the height of the hand that pulls it: it bows from its foot and is straight above
      for (const k of 'rag') { const lit = k === on; lens[k].m.material.color.set(lit ? COL[k] : OFF[k]); lens[k].halo.material.opacity = lit ? 0.28 : 0; const s = lit ? 1 + 0.35 * Math.max(0, 1 - u / 0.08) : 1; lens[k].m.scale.setScalar(s); } };
    g.userData.update(0); return g;
  },

  // the waiting-time display of a stop: a black box on a pole (o.h 2.6 m to its middle; o.pole false: the box alone, origin at its middle), front +Z.
  // A small fixed line on top (o.line '12 BIS') and a big one that changes: o.texts [[t, 'text'], ...]; each change pops.
  busDisplay(o) {
    const w = o.w ?? 0.95, hh = w * 0.5, g = grp(), boxG = grp(at(box(w, hh, 0.1, '#1A1C22', { outline: 0.012 }), 0, 0, 0)), keys = o.texts || [[0, '8 MIN']];
    const top = ledText(o.line || '12 BIS', w * 0.88, hh * 0.3, 256, '#FFFFFF'); top.position.set(0, hh * 0.3, 0.052); boxG.add(top);
    const faces = keys.map(([, s]) => { const f = ledText(s, w * 0.88, hh * 0.5); f.position.set(0, -hh * 0.14, 0.053); boxG.add(f); return f; });
    if (o.pole !== false) { const y = o.h ?? 2.6; g.add(at(cyl(0.04, 0.04, y, '#5B626B', 6, { pivot: 'bottom' }), 0, 0, -0.06)); boxG.position.y = y; }
    g.add(boxG);
    g.userData.update = t => { const i = stepAt(keys, t), u = t - keys[i][0]; faces.forEach((f, k) => { f.visible = k === i; }); const s = i > 0 ? 1 + 0.2 * Math.max(0, 1 - u / 0.07) + 0.08 * wob(u - 0.07, 40, 12) : 1; faces[i].scale.set(s, s, 1); };
    g.userData.update(0); return g;
  },

  // the line display he wears on his head: a black bar (o.w 0.4 m) on two short stalks; o.texts [[t, 'text'], ...] (or o.text). Origin: the foot of the
  // stalks, on the top of the skull; front +Z. Attach it to the head with `sway` so that it rocks with his steps.
  headSign(o) {
    const w = o.w ?? 0.4, hh = o.hh ?? 0.13, keys = o.texts || [[0, o.text || '12 BIS']], g = grp(at(box(w, hh, 0.05, '#1A1C22', { outline: 0.008 }), 0, 0.07 + hh / 2, 0)), pr = o.posts ?? 0.008;
    if (o.frame) g.add(at(box(w + 0.03, hh + 0.03, 0.04, o.frame), 0, 0.07 + hh / 2, -0.002));   // o.frame: a thin lighter frame round the panel (it stays his, next to a dark traffic light); o.posts: the radius of its two posts
    for (const s of [-1, 1]) g.add(at(cyl(pr, pr, 0.08, o.frame || '#5B626B', 5, { pivot: 'bottom' }), s * w * 0.3, 0, 0));
    const faces = keys.map(([, s]) => { const f = ledText(s, w * 0.92, hh * 0.78, 256); f.position.set(0, 0.07 + hh / 2, 0.027); g.add(f); return f; });
    g.userData.update = t => { const i = stepAt(keys, t), u = t - keys[i][0]; faces.forEach((f, k) => { f.visible = k === i; }); const s = i > 0 ? 1 + 0.25 * Math.max(0, 1 - u / 0.07) : 1; faces[i].scale.set(s, s, 1); };
    g.userData.update(0); return g;
  },

  // the sign at the edge of a French town: a white panel with a black border and the name (o.name 'PARIS'); o.exit (true): the red bar across it (you leave).
  // On one post (the middle of the panel o.y 2.0 m up). o.spinAt: something passes, the panel spins on its post like a weathercock: o.turns (2.5) turns
  // that die in o.spinDur (1.3 s). Readable from both sides.
  townSign(o) {
    const w = o.w ?? 1.25, hh = w * 0.36, y = o.y ?? 2.0, panel = grp(at(box(w, hh, 0.04, '#F4F1E8', { outline: 0.014 }), 0, 0, 0));
    for (const s of [-1, 1]) { const f = canvasPlane(w * 0.97, hh * 0.94, (c, W, H) => { c.fillStyle = '#F7F4EA'; c.fillRect(0, 0, W, H); c.strokeStyle = '#1B1B1E'; c.lineWidth = H * 0.07; c.strokeRect(H * 0.06, H * 0.06, W - H * 0.12, H * 0.88); txt(c, o.name || 'PARIS', W / 2, H * 0.54, fit(c, o.name || 'PARIS', W * 0.78, H * 0.6));
      if (o.exit !== false) { c.strokeStyle = '#D8281F'; c.lineWidth = H * 0.11; c.beginPath(); c.moveTo(W * 0.04, H * 0.92); c.lineTo(W * 0.96, H * 0.08); c.stroke(); } }, { res: 512 }); f.position.z = s * 0.022; if (s < 0) f.rotation.y = PI; panel.add(f); }
    panel.position.y = y; const g = grp(at(cyl(0.04, 0.04, y + hh / 2, '#8E949C', 6, { pivot: 'bottom' }), 0, 0, 0), panel);
    g.userData.update = t => { const u = o.spinAt == null ? -1 : t - o.spinAt, d = o.spinDur ?? 1.3; panel.rotation.y = u <= 0 ? 0 : TAU * (o.turns ?? 2.5) * ease.out(clamp01(u / d)) + 0.25 * wob(u - d, 11, 4); };
    g.userData.update(0); return g;
  },

  // the board of a lap counter, on a stick held in the fist: a small word on top (o.word 'TOUR') and a big number that flips: o.flips [[t, 'n'], ...]
  // (the first one is the number at the start). Origin: the bottom of the stick (in the fist); front +Z.
  lapBoard(o) {
    const w = o.w ?? 0.36, hh = w * 1.15, keys = o.flips || [[0, '2']], g = grp(at(cyl(0.014, 0.014, 0.34, P.woodDark, 6, { pivot: 'bottom' }), 0, 0, 0)), board = grp(at(box(w, hh, 0.03, '#F4F1E8', { outline: 0.012, ...(o.bright ? { emissive: '#8E8B84' } : {}) }), 0, 0, 0));   // o.bright: its face lit from inside a little: the lightest thing in a frame where it hangs alone, in the shade of a house front
    const word = canvasPlane(w * 0.9, hh * 0.2, (c, W, H) => { c.fillStyle = '#2C4A8A'; c.fillRect(0, 0, W, H); txt(c, o.word || 'TOUR', W / 2, H * 0.56, H * 0.74, '#FFFFFF'); }, { res: 192 }); word.position.set(0, hh * 0.36, 0.017); board.add(word);
    const flap = grp(); flap.position.set(0, -hh * 0.1, 0.018); board.add(flap);
    const faces = keys.map(([, s]) => { const f = canvasPlane(w * 0.86, hh * 0.66, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); txt(c, s, W / 2, H * 0.54, H * 0.92, '#1B1B1E'); }, { res: 192, emissive: o.bright ? 0.5 : 0 }); flap.add(f); return f; });
    board.position.y = 0.34 + hh / 2; g.add(board);
    g.userData.update = t => { const i = stepAt(keys, t), u = t - keys[i][0], d = 0.1, k = i > 0 && u < d ? u / d : 1; faces.forEach((f, n) => { f.visible = n === (k < 0.5 && i > 0 ? i - 1 : i); }); flap.scale.y = Math.max(0.04, Math.abs(Math.cos(k * PI))) * (i > 0 ? 1 + 0.2 * Math.max(0, 1 - (u - d) / 0.08) * (u >= d ? 1 : 0) : 1); };
    g.userData.update(0); return g;
  },

  // a desk that a blow splits in two: two halves (o.w 1.7 m wide in all, o.d 0.8, o.h 0.76), each with its outer side panel. o.at: the halves fall
  // toward the middle (a V: each turns on its outer foot by o.angle 0.5 rad, with a bounce) and jump apart by o.gap (0.06 m). Front +Z (the drawers face -Z).
  splitDesk(o) {
    const w = o.w ?? 1.7, d = o.d ?? 0.8, h = o.h ?? 0.76, C = o.color || '#8A5A36', g = grp(), halves = [];
    for (const s of [-1, 1]) { const hv = grp(at(box(w / 2, 0.06, d, C, { outline: 0.012 }), -s * w / 4, h - 0.03, 0), at(box(0.06, h - 0.06, d - 0.06, C, { outline: 0.01 }), -0.03 * s, (h - 0.06) / 2, 0), at(box(w / 2 - 0.1, 0.4, 0.04, '#74492B'), -s * w / 4, h - 0.28, d / 2 - 0.06));
      hv.position.set(s * w / 2, 0, 0); g.add(hv); halves.push({ hv, s }); }
    g.userData.update = t => { const u = o.at == null ? -1 : t - o.at, k = u <= 0 ? 0 : ease.out(clamp01(u / 0.16)) + 0.16 * wob(u - 0.16, 20, 7);
      for (const { hv, s } of halves) { hv.rotation.z = s * (o.angle ?? 0.5) * k; hv.position.x = s * (w / 2 + (o.gap ?? 0.06) * Math.min(1, k)); } };
    g.userData.update(0); return g;
  },

  // the map of a bus line that is a loop: a pale board (o.w 0.62 m, 1.3 times as high) with a coloured title band (o.title 'LIGNE 12 BIS'), a closed
  // line with its stops, and the marker of the bus: a little head with a red tie that goes round, one lap in o.lap (1.4 s), clockwise. Origin: the middle
  // of the bottom edge; front +Z.
  lineMap(o) {
    const w = o.w ?? 0.62, hh = w * 1.3, COL = o.color || '#E0572E', g = grp(), rx = w * 0.3, ry = hh * 0.26, cy = hh * 0.42;
    const pt = a => [rx * Math.sign(Math.cos(a)) * Math.pow(Math.abs(Math.cos(a)), 0.6), cy + ry * Math.sign(Math.sin(a)) * Math.pow(Math.abs(Math.sin(a)), 0.6)];
    const face = canvasPlane(w, hh, (c, W, H) => { c.fillStyle = '#F7F4EA'; c.fillRect(0, 0, W, H); c.fillStyle = COL; c.fillRect(0, 0, W, H * 0.15); txt(c, o.title || 'LIGNE 12 BIS', W / 2, H * 0.08, fit(c, o.title || 'LIGNE 12 BIS', W * 0.88, H * 0.1), '#FFFFFF');
      const X = x => W / 2 + x / w * W, Y = y => H - y / hh * H; c.strokeStyle = COL; c.lineWidth = W * 0.045; c.lineJoin = 'round'; c.beginPath(); for (let i = 0; i <= 96; i++) { const [x, y] = pt(i / 96 * TAU); if (i) c.lineTo(X(x), Y(y)); else c.moveTo(X(x), Y(y)); } c.closePath(); c.stroke();
      for (let i = 0; i < 8; i++) { const [x, y] = pt((i + 0.5) / 8 * TAU); c.fillStyle = '#FFFFFF'; c.strokeStyle = '#1B1B1E'; c.lineWidth = W * 0.012; c.beginPath(); c.arc(X(x), Y(y), W * 0.032, 0, TAU); c.fill(); c.stroke(); }
      c.fillStyle = '#B9BFC6'; for (let i = 0; i < 3; i++) c.fillRect(W * 0.3, H * (0.52 + i * 0.045), W * (0.4 - i * 0.07), H * 0.016); }, { res: 512 });
    face.position.set(0, hh / 2, 0.016); g.add(at(box(w + 0.03, hh + 0.03, 0.025, '#D9D2C0', { outline: 0.01 }), 0, hh / 2, 0), face);
    const mk = grp(at(box(0.052, 0.07, 0.012, '#E9B98C', { outline: 0.006 }), 0, 0.012, 0), at(box(0.056, 0.022, 0.014, '#1B1B1E'), 0, 0.05, 0), at(box(0.016, 0.03, 0.014, '#D8281F'), 0, -0.036, 0)); mk.position.z = 0.03; g.add(mk);
    g.userData.update = t => { const a = PI / 2 - TAU * ((t - (o.from ?? 0)) / (o.lap ?? 1.4)), [x, y] = pt(a); mk.position.x = x; mk.position.y = y; mk.rotation.z = 0.12 * Math.sin(t * 30); };
    g.userData.update(0); return g;
  },

  // a bus ticket the size of a hand (o.w 0.2 m): white, a coloured stripe, the line (o.line '12 BIS'). o.punchAt: a hole is punched in it (it jumps).
  // Origin: its middle; front +Z; hold it by a corner.
  bigTicket(o) {
    const w = o.w ?? 0.2, hh = w * 0.48, g = grp(at(box(w, hh, 0.006, '#FBFAF4', { outline: 0.006 }), 0, 0, 0));
    for (const s of [-1, 1]) { const f = canvasPlane(w * 0.96, hh * 0.92, (c, W, H) => { c.fillStyle = '#FBFAF4'; c.fillRect(0, 0, W, H); c.fillStyle = o.color || '#C2378C'; c.fillRect(0, H * 0.62, W, H * 0.2); txt(c, o.line || '12 BIS', W * (o.textX ?? 0.5), H * 0.34, fit(c, o.line || '12 BIS', W * (o.textW ?? 0.8), H * 0.46));   /* o.textX / o.textW: the line set to one side, a blank margin for the punch */ }, { res: 192 }); f.position.z = s * 0.004; if (s < 0) f.rotation.y = PI; g.add(f); }
    const hole = quad(0.03, 0.03, flat(o.hole || '#1B1B1E')); /* o.hole: its colour (the sky seen through it) */ hole.geometry = new THREE.CircleGeometry(hh * 0.13, 10); hole.position.set(w * (o.holeAt?.[0] ?? 0.3), hh * (o.holeAt?.[1] ?? 0.1), 0.006);   /* o.holeAt [fx, fy]: where it is punched, in fractions of the width and of the height from the middle */ const hole2 = hole.clone(); hole2.position.z = -0.006; hole2.rotation.y = PI; g.add(hole, hole2);
    g.userData.update = t => { const u = o.punchAt == null ? -1 : t - o.punchAt; hole.visible = hole2.visible = u >= 0; const s = u >= 0 ? 1 + 0.3 * Math.max(0, 1 - u / 0.08) : 1; g.scale.setScalar(s); };
    g.userData.update(0); return g;
  },

  // the stop button of a bus, on its yellow box (o.s 1 = 9 cm): a red button that goes in at o.pressAt, a red ring that flashes round it. Origin: the
  // back of the box; front +Z. Hang it on the knot of his tie.
  stopButton(o) {
    const s = o.s ?? 1, g = grp(at(box(0.09, 0.09, 0.035, '#F2C230', { outline: 0.008 }), 0, 0, 0.018)), btn = at(cyl(0.028, 0.028, 0.02, '#D8281F', 12), 0, 0, 0.045, PI / 2), ring = quad(0.2, 0.2, flat('#FF3B2F', { transparent: true, opacity: 0, depthWrite: false, depthTest: false }));   // drawn over everything: as it grows it went into his chest and his collar
    ring.geometry = new THREE.RingGeometry(0.05, 0.065, 20); ring.position.z = 0.05; ring.renderOrder = 20; g.add(btn, ring); g.scale.setScalar(s);
    g.userData.update = t => { const u = o.pressAt == null ? -1 : t - o.pressAt; btn.position.z = u >= 0 ? 0.045 - 0.012 * Math.max(0, 1 - Math.max(0, u - 0.1) / 0.08) : 0.045; ring.material.opacity = u >= 0 && u < 0.3 ? 0.9 * (1 - u / 0.3) : 0; ring.scale.setScalar(u >= 0 ? 1 + 2.2 * Math.min(1, u / 0.3) : 1); };
    g.userData.update(0); return g;
  },

  // the smoke of heels that brake: puffs born one after the other along a path and left behind. o.path [[t, x, z], ...] in the prop's own frame (where
  // the heels are at t); o.from / o.to: puffs are born between those times, o.every (0.035 s) apart; each grows, rises and fades in o.life (0.45 s).
  // o.marks: two dark skid marks drawn on the ground along the path as the heels pass (o.gap 0.22 m apart).
  heelSmoke(o) {
    const g = grp(), r = rng(o.seed || 7), path = o.path || [[0, 0, 0]], t0 = o.from ?? path[0][0], t1 = o.to ?? path[path.length - 1][0], ev = o.every ?? 0.035, life = o.life ?? 0.45, puffs = [];
    const pos = t => [keyed(path.map(p => [p[0], p[1]]), t), keyed(path.map(p => [p[0], p[2]]), t)];
    for (let tb = t0; tb <= t1 + 1e-6; tb += ev) { const m = sphere(0.085 + r() * 0.045, o.color || '#F3EFE8', 1, { unique: true, opacity: 0.99 }); m.castShadow = false; m.visible = false; g.add(m); const [x, z] = pos(tb); puffs.push({ m, tb, x, z, dy: 0.5 + r() * 0.5, dz: (r() - 0.5) * 0.3, k: 0.8 + r() * 0.6 }); }
    const marks = []; if (o.marks) for (const s of [-1, 1]) { const m = quad(1, 0.06, flat('#3A3A3E', { transparent: true, opacity: 0.75, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -8, polygonOffsetUnits: -32 })); m.rotation.x = -PI / 2; m.renderOrder = 4; g.add(m); marks.push({ m, s }); }   // o.marksY: their height (0.012; over a roadStrip: 0.08)
    g.userData.update = t => { for (const p of puffs) { const u = (t - p.tb) / life; p.m.visible = u >= 0 && u < 1; if (!p.m.visible) continue; p.m.position.set(p.x, 0.07 + p.dy * 0.7 * u, p.z + p.dz * u); p.m.scale.setScalar(p.k * (0.45 + 1.5 * ease.out(u))); p.m.material.opacity = 0.8 * (1 - u * u); }
      if (marks.length) { const [xa, za] = pos(t0), [xb, zb] = pos(Math.min(Math.max(t, t0), t1)), len = Math.hypot(xb - xa, zb - za), a = Math.atan2(zb - za, xb - xa);
        for (const { m, s } of marks) { m.visible = t > t0 && len > 0.02; m.scale.x = Math.max(0.02, len); m.position.set((xa + xb) / 2 + s * (o.gap ?? 0.22) / 2 * Math.sin(a), o.marksY ?? 0.012, (za + zb) / 2 - s * (o.gap ?? 0.22) / 2 * Math.cos(a)); m.rotation.z = -a; } } };
    g.userData.update(0); return g;
  },

  // the enamel plate of a station: navy, a white border, white letters (o.text 'GARE'), o.w (1.7 m) wide; origin: its middle; front +Z
  stationSign(o) {
    const w = o.w ?? 1.7, hh = w * 0.3, g = grp(at(box(w, hh, 0.04, '#1B2F6B', { outline: 0.012 }), 0, 0, 0));
    const f = canvasPlane(w * 0.97, hh * 0.92, (c, W, H) => { c.fillStyle = '#1B2F6B'; c.fillRect(0, 0, W, H); c.strokeStyle = '#F4F1E8'; c.lineWidth = H * 0.06; c.strokeRect(H * 0.08, H * 0.08, W - H * 0.16, H * 0.84); txt(c, o.text || 'GARE', W / 2, H * 0.55, fit(c, o.text || 'GARE', W * 0.78, H * 0.66), '#F4F1E8'); }, { res: 512 });
    f.position.z = 0.022; g.add(f); return g;
  },

  // A furled umbrella held like a shepherd's crook: a thick shaft (o.len 1.25 m) with a big bright crook at its far end (o.crook 0.14 m radius,
  // o.crookColor), the cloth furled round the shaft. Origin: the grip, 0.12 m from the ferrule; the shaft goes up +Y; the crook curls toward -X and
  // comes back down (held flat pointing -X after a turn of +90 degrees about Z, it hangs down over what it catches). o.shake [[t0, amp]]: it quivers.
  crookUmbrella(o) {
    const L = o.len ?? 1.25, R = o.crook ?? 0.14, tube = o.tube ?? 0.036, g = grp(), b = new THREE.Group(), cc = o.crookColor || '#E63B2E', cols = o.colors || ['#2F7F5C', '#F2EDE4'];
    b.add(at(cyl(0.022, 0.022, L + 0.12, '#2B2F36', 8, { pivot: 'bottom' }), 0, -0.12, 0));
    for (let i = 0; i < 6; i++) b.add(at(cyl(0.05 - i * 0.003, 0.056 - i * 0.003, (L - 0.42) / 6, cols[i % 2], 8, { pivot: 'bottom' }), 0, 0.2 + i * (L - 0.42) / 6, 0));
    const crook = torus(R, tube, cc, 8, 14, PI * 1.25); crook.position.set(-R, L, 0); b.add(crook, at(sphere(tube * 1.15, cc, 1), -R + R * Math.cos(PI * 1.25), L + R * Math.sin(PI * 1.25), 0));
    g.add(b);
    g.userData.update = t => { let a = 0; for (const [t0, amp] of o.shake || []) if (t >= t0) a += amp * wob(t - t0, 46, 7); b.rotation.z = a; };
    g.userData.update(0); return g;
  },

  // an oversized ticket punch (pliers): two handles, two jaws; o.snapAt: the jaws snap shut (and bounce open a little). Origin: the pivot; the jaws point +Y.
  ticketPunch(o) {
    const s = o.s ?? 1, g = grp(), A = new THREE.Group(), B = new THREE.Group(), steel = o.jaw || '#C9CED6', grip = o.grip || '#D8281F';   // o.grip: the colour of its handles; o.jaw: of its jaws (dark steel reads on a pale ticket)
    for (const [G, sg] of [[A, 1], [B, -1]]) { G.add(at(box(0.03, 0.2, 0.03, steel, { outline: 0.008 }), sg * 0.012, 0.1, 0), at(box(0.036, 0.2, 0.036, grip, { outline: 0.008 }), sg * 0.02, -0.11, 0), at(box(0.05, 0.03, 0.04, steel), sg * 0.005, 0.2, 0)); g.add(G); }
    g.scale.setScalar(s);
    g.userData.update = t => { const u = o.snapAt == null ? -1 : t - o.snapAt, open = u < 0 ? 0.3 : u < 0.05 ? 0.3 * (1 - u / 0.05) : 0.12 * Math.min(1, (u - 0.05) / 0.12); A.rotation.z = -open; B.rotation.z = open; };
    g.userData.update(0); return g;
  },

  // confetti punched out of a ticket: o.n dots (1) that leave from o.at, fall o.fall metres in o.dur seconds, spinning, drifting o.drift [x, z] (the wind)
  confetti(o) {
    const g = grp(), r = rng(o.seed || 5), n = o.n ?? 1, ds = [];
    for (let i = 0; i < n; i++) { const m = quad(0.05 * (o.s ?? 1), 0.05 * (o.s ?? 1), flat(o.color || '#FBFAF4', { side: THREE.DoubleSide })); m.geometry = new THREE.CircleGeometry(0.025 * (o.s ?? 1), 10); m.visible = false; g.add(m); ds.push({ m, vx: (r() - 0.5) * 0.5, vy: 0.6 + r() * 0.5, ph: r() * 6 }); }
    g.userData.update = t => { const u = (t - (o.at ?? 0)); for (const d of ds) { d.m.visible = u >= 0 && u <= (o.dur ?? 0.8); if (!d.m.visible) continue; const k = u / (o.dur ?? 0.8);
      d.m.position.set(d.vx * u + (o.drift?.[0] ?? 0) * u, d.vy * u - (o.fall ?? 0.6) * k * k - 0.6 * u * u * 0, (o.drift?.[1] ?? 0) * u); d.m.rotation.set(u * 14 + d.ph, u * 9, 0); } };
    g.userData.update(-1); return g;
  },

  // a wristwatch for a puppet's wrist: a dark strap and a pale dial (o.s 1 = 4.5 cm). Attach it to a hand: on={'actor': id, 'hand': 'L', 'offset': [0, 0.06, 0]}
  wristWatch(o) {
    const s = o.s ?? 1, R = o.dialR ?? 0.026, g = grp(at(box(0.075, 0.03, 0.075, o.strap || '#2B2F36', { outline: 0.006 }), 0, 0, 0));   // o.dialR: a bigger dial; o.both: a dial on each side of the wrist (whichever way the forearm turns, one faces the camera); o.bright: an unlit white dial
    for (const sg of (o.both ? [1, -1] : [1])) { const d = cyl(R, R, 0.012, o.dial || '#F4F1E8', 14); if (o.bright) d.material = flat(o.dial || '#FFFFFF'); g.add(at(d, 0, 0, sg * 0.04, PI / 2), at(cyl(R * 1.15, R * 1.15, 0.008, '#C9A24B', 14), 0, 0, sg * 0.036, PI / 2)); }
    g.scale.setScalar(s); return g;
  },

  // The legs of a sprint as a wheel: a blurred disc the colour of the trousers, four streaks and four shoes going round. Attach it at the waist of a runner
  // (on: {actor, joint: 'torso'}) whose own legs are shrunk away (toon bend legL / legR / shinL / shinR: stretch 0.05). o.r (0.62 m): its radius; o.rate
  // (2.5 turns a second: a shoe moves a third of the way to the next one each frame); o.color, o.shoe; o.from / o.to: when it shows.
  legWheel(o) {
    const R = o.r ?? 0.62, g = grp(), w = new THREE.Group(), col = o.color || '#1E2A44', tr = (c, op) => flat(c, { transparent: true, opacity: op, depthWrite: false, side: THREE.DoubleSide });
    const disc = quad(1, 1, tr(col, 0.34)); disc.geometry = new THREE.RingGeometry(R * 0.2, R * 0.97, 28); w.add(disc);
    for (let i = 0; i < 4; i++) { const a = i * PI / 2, leg = quad(R * 0.85, 0.12, tr(col, 0.85)); leg.position.set(Math.cos(a) * R * 0.5, Math.sin(a) * R * 0.5, 0.003); leg.rotation.z = a; w.add(leg);
      const tail = quad(1, 1, tr(col, 0.5)); tail.geometry = new THREE.RingGeometry(R * 0.82, R * 0.99, 10, 1, a - 0.5, 0.5); tail.position.z = 0.002; w.add(tail);   // the blur behind each shoe
      const shoe = box(0.25, 0.1, 0.12, o.shoe || '#15171C', { outline: 0.01 }); shoe.position.set(Math.cos(a) * R, Math.sin(a) * R, 0); shoe.rotation.z = a - PI / 2; w.add(shoe); }
    w.position.y = -R * 0.74; g.add(w);
    g.userData.update = t => { g.visible = t >= (o.from ?? -1e9) && t <= (o.to ?? 1e9); w.rotation.set(0, PI / 2, 0); w.rotateZ((o.rate ?? 2.5) * TAU * t); };
    g.userData.update(0); return g;
  },

  // a feather left in the air by a bird that has gone: from o.at it comes down o.fall metres (1.2) in o.dur seconds (1.2), rocking from side to side
  // (o.sway metres, o.swings times), tilting as it goes; o.s: its size (1 = 16 cm). Put the prop where the bird was.
  feather(o) {
    const s = o.s ?? 1, g = grp(), f = new THREE.Group(), side = { side: THREE.DoubleSide }, vane = quad(0.16 * s, 0.055 * s, flat(o.color || '#DDE1E7', side)), quill = quad(0.19 * s, 0.01 * s, flat('#8F959E', side));
    vane.geometry = new THREE.ShapeGeometry(new THREE.Shape().moveTo(-0.08 * s, 0).quadraticCurveTo(-0.02 * s, 0.04 * s, 0.08 * s, 0).quadraticCurveTo(-0.02 * s, -0.035 * s, -0.08 * s, 0), 6);
    quill.position.set(-0.012 * s, 0, 0.001); f.add(vane, quill); g.add(f);
    g.userData.update = t => { const u = (t - (o.at ?? 0)) / (o.dur ?? 1.2); f.visible = u >= 0 && u <= 1; if (!f.visible) return; const ph = u * (o.swings ?? 2.5) * TAU;
      f.position.set((o.sway ?? 0.22) * Math.sin(ph), -(o.fall ?? 1.2) * (u + 0.04 * Math.sin(2 * ph)), 0.05 * Math.cos(ph)); f.rotation.set(0.5 * Math.sin(ph * 0.5), 0.6 * Math.cos(ph * 0.7), -0.75 * Math.cos(ph)); };
    g.userData.update(-1); return g;
  },

  // a straight strip of country road along Z (o.len 120 m, o.w 7 m) with a dashed middle line and pale verges: lay it on a field
  roadStrip(o) {
    // Three layers painted over the field in a fixed order, without a depth test (the field is flat): a strip 500 m long a few centimetres over a
    // ground plane 9 km wide fought with it for depth (the road flickered in the draft, was gone in the final look, then showed only in part).
    // The ground under it must be drawn first: its renderOrder is -2 (the grassland set); whatever stands on the road is drawn after, as usual.
    const len = o.len ?? 120, w = o.w ?? 7, g = grp(), lay = c => new THREE.MeshLambertMaterial({ color: c, depthTest: false, depthWrite: false });
    const q = (ww, c, x, y, k) => { const m = quad(ww, len, lay(c)); m.receiveShadow = true; m.rotation.x = -PI / 2; m.position.set(x, y, 0); m.renderOrder = -1.5 + 0.1 * k; return m; };
    g.add(q(w + 1.2, '#D8CFB6', 0, 0.01, 1), q(w, '#77777B', 0, 0.015, 2));
    for (let z = -len / 2 + 1; z < len / 2; z += 4) { const m = quad(0.16, 1.8, lay('#F4F1E8')); m.rotation.x = -PI / 2; m.position.set(0, 0.02, z); m.renderOrder = -1.2; g.add(m); }
    return g;
  },
};
