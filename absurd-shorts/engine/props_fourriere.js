// « La fourrière » (story 45): a man double-parks "for one minute"; the pound tows him, not the car; at the pound they clamp him; to leave, the owner
// must pay; the owner is the car, and it has no hands; it honks for three weeks; the neighbours complain, against him; the pound comes back for the car and
// parks it in its space: on him. He pays for the space.
// Conventions as in props.js (metres, pivot at the floor); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, ease, clamp01 } from './style.js';
import { grp, at, glassMat, label, torus, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const rnd = s => { let x = Math.sin(s * 127.1) * 43758.5453; return x - Math.floor(x); };
const wob = (u, f, d) => u < 0 ? 0 : Math.exp(-u * d) * Math.sin(u * f);
const spans = l => !l ? [] : Array.isArray(l[0]) ? l : [l];                       // [t0, t1] or [[t0, t1], ...]
const inSpan = (l, t) => spans(l).some(([a, b]) => t >= a && t < b);
const stepKey = (l, t, d) => { let v = d; for (const q of l || []) if (t >= q[0]) v = q.slice(1); return v; };   // [[t, a, b, ...]] held until the next key
const lerpKeys = (l, t, d) => {   // [[t, a, b, ...]]: eased between keys (0.12 s ease-out into each key)
  if (!l || !l.length) return d; let prev = d;
  for (let i = 0; i < l.length; i++) { const q = l[i]; if (t < q[0]) break; const nxt = q.slice(1), k = ease.out(clamp01((t - q[0]) / 0.12));
    prev = prev.map((v, j) => v + ((nxt[j] ?? v) - v) * k); if (k >= 1) prev = nxt.slice(); }
  return prev;
};
const basic = (color, opacity = 1) => new THREE.MeshBasicMaterial({ color, transparent: opacity < 1, opacity, depthWrite: opacity >= 1 });
const lamp = (on, off) => [mat(on, { emissive: on, noGrain: true }), mat(off)];

export const FOURRIERE_PROPS = {
  // A small city car facing +X with a cartoon life. o.color ('#6CC4A4'); o.plate.
  // Eyes: the headlights are eyes; o.eyes (true) gives them dark pupils; o.gaze [[t, gx, gy]] (-1..1, gx + = toward +Z, gy + = up);
  // o.lids [[t, k, tilt]] (k 0 open .. 1 shut; tilt + = cross: the inner ends drop); o.blink [t, ...] (a blink of 5 frames at each).
  // o.hazard [t0, t1] (or a list): the four orange corner lights blink at 1.7 Hz. o.honk [[t, dur], ...]: a squash, then a stretch with a hop, and rings
  // from the grille every 0.12 s while it lasts (a long honk trembles). o.wipe [[t0, t1], ...]: the two wipers flail and stretch (o.wipeLen 2.2): little
  // arms that cannot reach. o.pv [[t, n]]: n parking fines under the driver's wiper (the pile grows out of the glass). o.leaves [[t, n]]: dead leaves on
  // the roof and the bonnet (up to 40). o.bounce [[t, amp]]: the body bounces on its springs (a landing; amp 0.1 = 10 cm). o.sag (0): the body rests lower
  // and wider (it sits on something soft). userData.front / roof / wiper: local points for the script.
  // (cycle 8) o.reach [[t0, t1], ...] with o.reachTo [x, y, z] (world): the two wipers leave the glass and stretch toward that point, trembling, and stop
  // o.reachShort (0.15 m) short of it: little arms that cannot reach (flailing on its own windscreen they never reached for anything)
  // (cycle 8, pass 3 of story 45) the lids are curved caps seated inside the rims, closing on a dark curved lash line (shut: a lash arc along the bottom of
  // the rim; flat boards over the eyes read as tape); the wipers flail and reach as two-segment arms with an elbow and a rubber blade at the tip that
  // flaps (a straight rod read as a cable), with shake strokes at the tips while they strain; a honk gathers first (a 20 % squash, eyes squeezed, from
  // 0.1 s before its time), then stretches and hops clear (o.honkHop, 0.3 m), lands with a bounce; the rings leave the grille below the eyes, small near
  // the face and growing as they go (o.ringUp: a rise, default 0)
  carToon(o) {
    const C = o.color || '#6CC4A4', L = 3.5, Wd = 1.62, g = grp(), body = grp(); g.add(body);
    const DARK = '#3E434C', GLASS = o.glassColor || '#BFE3EE';
    body.add(at(box(L, 0.6, Wd, C, { outline: 0.012 }), 0, 0.64, 0));                                        // lower body, 0.34 .. 0.94
    body.add(at(box(L + 0.05, 0.14, Wd + 0.04, DARK), 0, 0.4, 0));                                          // bumpers and sills
    body.add(at(box(0.5, 0.05, Wd - 0.2, '#58BBA0'), 1.3, 0.955, 0));                                       // a bonnet crease
    const cx = -0.3, cy0 = 0.94, ch = 0.66;
    body.add(at(box(1.95, ch, 1.48, C, { outline: 0.01, taper: { x: 0.76, z: 0.84 } }), cx, cy0 + ch / 2, 0));   // the cabin (its roof is 1.48 x 1.24)
    const slope = Math.atan2(1.95 * 0.12, ch);                                                               // the tapered faces lean back by this much
    // windows: pale opaque panes just outside the cabin faces
    const ws = at(box(0.02, ch * 0.8, 1.2, GLASS, { noGrain: true }), cx + 1.95 / 2 - 1.95 * 0.06 + 0.012, cy0 + ch * 0.48, 0, 0, 0, slope); body.add(ws);   // windscreen
    body.add(at(box(0.02, ch * 0.72, 1.14, GLASS, { noGrain: true }), cx - 1.95 / 2 + 1.95 * 0.06 - 0.012, cy0 + ch * 0.48, 0, 0, 0, -slope));            // rear window
    const sideA = Math.atan2(0.74 * 0.16, ch);
    for (const sz of [-1, 1]) for (const [x, w] of [[0.24, 0.6], [-0.5, 0.6]]) body.add(at(box(w, ch * 0.62, 0.02, GLASS, { noGrain: true }), cx + x, cy0 + ch * 0.47, sz * (0.74 * 0.92 + 0.012), -sz * sideA, 0, 0));
    // wheels (in the body: the whole car hops and squashes as one)
    for (const x of [-1.15, 1.15]) for (const z of [-0.74, 0.74]) body.add(at(cyl(0.31, 0.31, 0.24, P.ink, 12), x, 0.31, z, PI / 2), at(cyl(0.14, 0.14, 0.02, '#C9CDD3', 8), x, 0.31, z * 1.17, PI / 2));
    // headlight eyes: white discs, dark pupils, lids in the body colour that grow down from the top edge
    const eyes = [], LR = 0.136, LIDN = 24, lidMat = new THREE.MeshLambertMaterial({ color: C, side: THREE.DoubleSide }), lashMat = new THREE.MeshBasicMaterial({ color: '#1B1B1E', side: THREE.DoubleSide });
    const lidIdx = []; for (let j = 0; j < LIDN; j++) { const a = 2 * j; lidIdx.push(a, a + 2, a + 1, a + 1, a + 2, a + 3); }
    // a column strip across the disc: for u in -LR..LR the lid covers from its edge line up to the top of the disc; the lash is a band under that edge
    const setLid = (E, k) => { const b = 0.35 * LR, v0 = (LR + b + 0.004) * (1 - k) + (-0.66 * LR - 0.01) * k, w = 0.022, P1 = E.lid.geometry.attributes.position, P2 = E.lash.geometry.attributes.position;
      for (let j = 0; j <= LIDN; j++) { const u = -LR + 2 * LR * j / LIDN, top = Math.sqrt(Math.max(0, LR * LR - u * u)), edge = v0 - b * (1 - (u / LR) ** 2);
        const lo = Math.min(top, Math.max(edge, -top)); P1.setXYZ(2 * j, u, lo, 0); P1.setXYZ(2 * j + 1, u, top, 0);
        const lt = Math.min(top, Math.max(edge, -top + w)), on = k > 0.02 && edge < top; P2.setXYZ(2 * j, u, on ? Math.max(-top, lt - w) : top, 0); P2.setXYZ(2 * j + 1, u, on ? lt : top, 0); }
      P1.needsUpdate = P2.needsUpdate = true; E.lid.geometry.computeBoundingSphere(); E.lash.geometry.computeBoundingSphere(); };
    for (const sz of [-1, 1]) {
      const e = grp(); e.position.set(L / 2 + 0.005, 0.76, sz * 0.48); body.add(e);
      e.add(at(cyl(0.15, 0.15, 0.04, '#FFFBEA', 16, { emissive: '#FFF3C4', noGrain: true }), 0.02, 0, 0, 0, 0, PI / 2));
      e.add(at(torus(0.15, 0.018, DARK, 6, 20), 0.035, 0, 0, 0, PI / 2, 0));
      const pup = at(cyl(0.062, 0.062, 0.02, '#1B1B1E', 12), 0.05, 0, 0, 0, 0, PI / 2); pup.visible = o.eyes !== false; e.add(pup);
      const lid = new THREE.Mesh(new THREE.BufferGeometry(), lidMat), lash = new THREE.Mesh(new THREE.BufferGeometry(), lashMat);
      const nrm = () => { const a = new Float32Array((LIDN + 1) * 6); for (let i = 2; i < a.length; i += 3) a[i] = 1; return new THREE.BufferAttribute(a, 3); };   // (normals: a lit material without them gave NaN, and the bloom spread it over the whole frame: black)
      lid.geometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array((LIDN + 1) * 6), 3)); lid.geometry.setAttribute('normal', nrm()); lid.geometry.setIndex(lidIdx);
      lash.geometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array((LIDN + 1) * 6), 3)); lash.geometry.setAttribute('normal', nrm()); lash.geometry.setIndex(lidIdx);
      lid.frustumCulled = lash.frustumCulled = false; lash.position.z = 0.002;
      const lidG = grp(); lidG.add(lid, lash); lidG.position.set(0.066, 0, 0); lidG.rotation.set(0, PI / 2, 0); e.add(lidG);   // (pass 3) a cap inside the rim, in front of the pupil
      eyes.push({ sz, pup, lid, lash, lidG });
    }
    // corner lights (hazards): on and off copies swapped
    const [hOn, hOff] = lamp('#FFB020', '#B8691C'), corners = [];
    for (const x of [L / 2 + 0.01, -L / 2 - 0.01]) for (const sz of [-1, 1]) { const on = at(box(0.05, 0.1, 0.16, '', { material: hOn }), x, 0.78, sz * 0.74), off = at(box(0.05, 0.1, 0.16, '', { material: hOff }), x, 0.78, sz * 0.74); body.add(on, off); corners.push([on, off]); }
    body.add(at(box(0.04, 0.14, 0.34, P.red), -L / 2 - 0.01, 0.62, -0.5), at(box(0.04, 0.14, 0.34, P.red), -L / 2 - 0.01, 0.62, 0.5));   // tail lights
    body.add(at(box(0.03, 0.2, 0.86, '#2A2C31'), L / 2 + 0.012, 0.52, 0));                                                              // grille
    for (const sx of [-1, 1]) body.add(at(label(o.plate || 'FG-412-HJ', 0.52, 0.12, { bg: P.white, fg: P.ink, wrap: false }), sx * (L / 2 + 0.03), 0.43, 0, 0, sx * PI / 2, 0));
    // wipers: pivots at the foot of the windscreen; local X = the glass normal, local Y = up the glass; the arm lies along local -Z
    const AW = o.armW ?? 1, wsFootX = cx + 1.95 / 2 - 0.02, wipers = [], armMat = new THREE.MeshLambertMaterial({ color: o.armColor || '#1E2024' }),   // (final pass) o.armW: the reaching arms that many times thicker, o.armColor, o.bladeColor, o.elbowUp (0.16 m), o.shakeR / o.shakeL (the tremble ticks round the tip)
      _M = new THREE.Vector3(), _E = new THREE.Vector3(), _D = new THREE.Vector3();
    for (const z0 of [0.5, -0.06]) {
      const pv = grp(); pv.position.set(wsFootX + 0.03, cy0 + 0.05, z0); pv.rotation.z = slope; body.add(pv);
      const arm = grp(); pv.add(arm); arm.add(at(box(0.03, 0.03, 0.56, '#1E2024'), 0.02, 0, -0.28), at(box(0.025, 0.06, 0.46, '#2A2C31'), 0.035, 0, -0.32), at(cyl(0.03, 0.03, 0.04, '#1E2024', 8), 0.02, 0, 0, 0, 0, PI / 2));
      // (pass 3) the arm that moves: two segments (unit boxes along -Z, scaled), an elbow, a rubber blade across the tip, shake strokes
      const seg1 = grp(), m1 = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.045, 1).translate(0, 0, -0.5), armMat), elbow = grp(), seg2 = grp(), m2 = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.04, 1).translate(0, 0, -0.5), armMat);
      const tip = grp(), blade = grp(at(box(0.035 * Math.min(AW, 1.8), 0.3, 0.06 * Math.min(AW, 1.8), o.bladeColor || '#1E2024', { outline: 0.006 }), 0, 0, 0), at(box(0.02, 0.3, 0.025, o.bladeColor ? '#8A8F96' : '#3A3D44'), 0.02, 0, 0.0)), knob = new THREE.Mesh(new THREE.SphereGeometry(0.035 * AW, 8, 6), armMat);
      seg1.add(m1, elbow); elbow.add(knob, seg2); seg2.add(m2, tip); tip.add(blade); pv.add(seg1); seg1.visible = false;
      const SR = o.shakeR ?? 0.2, SL = o.shakeL ?? 0.12, shakes = [0, 1, 2, 3].map(j => { const sm = new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.012, SL), new THREE.MeshBasicMaterial({ color: '#1B1B1E' })); const a = j * PI / 2 + 0.6; sm.position.set(0, SR * Math.cos(a), 0.05 + SR * 0.6 * Math.sin(a)); sm.rotation.x = a; tip.add(sm); return sm; });   // (final pass) behind the tip, never toward what it reaches for
      wipers.push({ pv, arm, z0, seg1, m1, elbow, seg2, m2, tip, blade, shakes });
    }
    // parking fines: a pile in the driver's wiper frame (the wiper on the +Z side)
    const fines = [], PV = wipers[0].pv;
    for (let i = 0; i < 48; i++) { const f = grp(at(box(0.004, 0.13, 0.2, '#F6F4EC', { noGrain: true }), 0, 0, 0), at(box(0.006, 0.03, 0.2, '#E8742A', { noGrain: true }), 0.001, 0.045, 0));
      f.position.set(0.02 + i * 0.011, 0.07 + 0.03 * (rnd(i) - 0.5), -0.24 + 0.08 * (rnd(i + 5) - 0.5)); f.rotation.x = 0.5 * (rnd(i + 9) - 0.5); f.visible = false; PV.add(f); fines.push(f); }
    // dead leaves
    const leaves = [], LC = ['#C9762E', '#B5532A', '#D9A23A', '#8E5A2B'];
    for (let i = 0; i < 40; i++) { const onRoof = i % 3 !== 0, x = onRoof ? cx + (rnd(i) - 0.5) * 1.3 : 0.75 + rnd(i) * 0.9, y = onRoof ? cy0 + ch + 0.012 : 0.96, z = (rnd(i + 3) - 0.5) * (onRoof ? 0.95 : 1.3);
      const lf = at(box(0.13, 0.012, 0.08, LC[i % 4], { noGrain: true }), x, y, z, 0, rnd(i + 7) * TAU, 0); lf.visible = false; body.add(lf); leaves.push(lf); }
    // honk rings: expanding hoops in front of the grille
    const rm = basic('#FFF6C8', 0.85), RT_ = o.ringTube ?? 0.05, rings = Array.from({ length: 6 }, () => { const r = new THREE.Mesh(new THREE.TorusGeometry(1, RT_, 6, 28), rm.clone()); r.rotation.y = PI / 2; r.visible = false; r.userData.noAO = true; g.add(r);
      if (o.ringInk) { const kl = new THREE.Mesh(new THREE.TorusGeometry(1, RT_ * 1.6, 6, 28), basic('#1B1B1E', 0.9)); kl.position.z = -0.01; kl.userData.noAO = true; r.add(kl); } return r; });   // (final pass) o.ringTube (0.05): thicker hoops; o.ringInk: a dark keyline behind each
    const honks = o.honk || [], wipes = spans(o.wipe), WL = o.wipeLen ?? 2.2, reaches = spans(o.reach), RT = o.reachTo ? new THREE.Vector3(...o.reachTo) : null, wpA = new THREE.Vector3(), wpB = new THREE.Vector3();
    g.userData.update = t => {
      // body: honk squash and hop, landing bounce, sag
      let sy = 1, hop = 0, trem = 0, squint = 0; const HH = o.honkHop ?? 0.3;
      for (const [h0, hd] of honks) { const u = t - h0; if (u < -0.1 || u > hd + 0.8) continue;
        if (u < 0) { const a = ease.inOut((u + 0.1) / 0.1); sy *= 1 - 0.2 * a; squint = Math.max(squint, 0.6 * a); }                          // it gathers itself: squashed, eyes squeezed
        else { const air = clamp01(u / 0.3); hop += HH * Math.sin(PI * air);                                                                 // up and clear of the road
          sy *= u < 0.3 ? 1 + 0.16 * Math.sin(PI * Math.min(1, air * 1.6)) : 1 - 0.16 * wob(u - 0.3, 24, 6);                                // stretched in the air, a bounce on landing
          if (u < 0.08) squint = Math.max(squint, 0.6 * (1 - u / 0.08)); }
        if (u >= 0 && u < hd) trem = Math.max(trem, clamp01((hd - 0.3) / 0.6)); }
      for (const [b0, amp] of o.bounce || []) { const u = t - b0; if (u < 0 || u > 1.2) continue; sy *= 1 - 2.2 * amp * wob(u, 20, 4.5); hop -= amp * Math.max(0, 1 - u / 0.08) * (u < 0.08 ? 1 : 0); }
      const sag = o.sag ?? 0; sy *= 1 - 0.18 * sag;
      const sxz = 1 / Math.sqrt(Math.max(0.4, sy));
      body.scale.set(sxz, sy, sxz); body.position.set(0.012 * trem * Math.sin(t * 71), hop + 0.006 * trem * Math.abs(Math.sin(t * 53)), 0.01 * trem * Math.sin(t * 59));
      // eyes
      const [gx, gy] = lerpKeys(o.gaze, t, [0, 0]); let [lk, tilt] = lerpKeys(o.lids, t, [0, 0]);
      for (const b of o.blink || []) { const u = (t - b) / (5 / 30); if (u >= 0 && u < 1) lk = Math.max(lk, Math.sin(u * PI)); }
      lk = Math.max(lk, squint);
      for (const e of eyes) { e.pup.position.set(0.05, 0.065 * gy, 0.065 * gx); const kk = clamp01(lk + 0.22 * Math.abs(tilt)); e.lidG.visible = kk > 0.01; if (e.lidG.visible) setLid(e, kk); e.lidG.rotation.set(0, PI / 2, e.sz * 0.45 * tilt); }
      // hazards
      const hz = inSpan(o.hazard, t) && Math.floor((t - (spans(o.hazard).find(([a, b]) => t >= a && t < b)?.[0] ?? 0)) * 3.4) % 2 === 0;
      for (const [on, off] of corners) { on.visible = hz; off.visible = !hz; }
      // wipers
      const wk = wipes.find(([a, b]) => t >= a && t < b), rk = RT && reaches.find(([a, b]) => t >= a && t < b);
      if (rk) { g.updateWorldMatrix(true, true);
        wipers.forEach((w, i) => { const u = t - rk[0], grow = 1 - Math.pow(1 - clamp01(u / 0.28), 3), tr = 0.014 * Math.sin(t * 63 + i * 2.1);
          w.arm.visible = false; w.seg1.visible = true; w.pv.getWorldPosition(wpA); wpB.copy(RT); wpB.y += (i ? -0.08 : 0.08) + tr;
          const d = wpA.distanceTo(wpB), reach = Math.max(0.3, (d - (o.reachShort ?? 0.15)) * grow + 0.5 * (1 - grow));
          _D.subVectors(wpB, wpA).normalize(); _E.copy(wpA).addScaledVector(_D, reach);                                   // the tip: short of the point
          _M.addVectors(wpA, _E).multiplyScalar(0.5); _M.y += ((o.elbowUp ?? 0.16) + 0.025 * Math.sin(t * 41 + i)) * grow;                  // the elbow, up: a bent little arm
          w.seg1.rotation.set(0, 0, 0); w.seg1.updateWorldMatrix(true, false); w.seg1.lookAt(_M); w.seg1.rotateY(PI); const l1 = wpA.distanceTo(_M);
          w.m1.scale.set(AW, AW, l1); w.elbow.position.set(0, 0, -l1); w.seg1.updateWorldMatrix(true, true);
          w.seg2.rotation.set(0, 0, 0); w.seg2.updateWorldMatrix(true, false); w.seg2.lookAt(_E); w.seg2.rotateY(PI); const l2 = _M.distanceTo(_E);
          w.m2.scale.set(AW, AW, l2); w.tip.position.set(0, 0, -l2); w.blade.rotation.set(0.45 * Math.sin(t * 47 + i * 1.7), 0, 0);   // the blade flaps
          const fl = Math.floor(t * 15 + i) % 2 === 0 && u > 0.2; w.shakes.forEach((sm, j) => { sm.visible = fl && (j + i) % 2 === Math.floor(t * 15) % 2; }); });
      } else
      wipers.forEach((w, i) => { if (!wk) { w.arm.visible = true; w.seg1.visible = false; w.arm.rotation.x = 0.05; w.arm.scale.set(1, 1, 1); return; }
        const u = t - wk[0], grow = clamp01(u / 0.18), ph = t * TAU * 4.6 + i * 1.9, Lt = 0.56 * (1 + (WL - 1) * grow * (0.85 + 0.15 * Math.sin(ph * 1.7)));
        w.arm.visible = false; w.seg1.visible = true; w.shakes.forEach(sm => { sm.visible = false; });
        w.seg1.rotation.set(0.9 + 0.75 * Math.sin(ph), 0, 0); w.m1.scale.set(AW, AW, Lt * 0.5); w.elbow.position.set(0, 0, -Lt * 0.5);     // (pass 3) a flail with an elbow:
        w.seg2.rotation.set(0.7 * Math.sin(ph - 1.3), 0, 0); w.m2.scale.set(AW, AW, Lt * 0.5); w.tip.position.set(0, 0, -Lt * 0.5);      // the forearm lags (a whip, not a rod)
        w.blade.rotation.set(0.5 * Math.sin(ph - 2.2), 0, 0); });
      // fines and leaves
      const nPv = Math.round(stepKey(o.pv, t, [0])[0]), nLf = Math.round(stepKey(o.leaves, t, [0])[0]);
      fines.forEach((f, i) => { f.visible = i < nPv; }); leaves.forEach((l, i) => { l.visible = i < nLf; });
      // honk rings
      let ri = 0; for (const r of rings) r.visible = false;
      for (const [h0, hd] of honks) for (let e = h0; e < h0 + Math.max(0.12, hd); e += 0.12) { const u = (t - e) / 0.42; if (u < 0 || u >= 1 || ri >= rings.length) continue;
        const r = rings[ri++]; r.visible = true; r.position.set(L / 2 + 0.15 + 1.4 * u, 0.45 + hop + (o.ringUp ?? 0.0) * u, 0); r.scale.setScalar(0.1 + 0.55 * u * u); r.material.opacity = 0.85 * (1 - u); if (r.children[0]) r.children[0].material.opacity = 0.9 * (1 - u); }   // (pass 3) from the grille, under the eyes: small near the face, growing as they leave
    };
    g.userData.update(0);
    g.userData.front = [L / 2, 0.76, 0]; g.userData.roof = [cx, cy0 + ch, 0]; g.userData.wiper = [wsFootX, cy0 + 0.1, 0.25];
    return g;
  },

  // A tow truck (dépanneuse) facing +X, 6.6 m long: a white cab with an orange band and a light bar, a flat bed, a yellow crane at the back; FOURRIÈRE on
  // the doors and the skirts. o.beacons [t0, t1] (or a list; default always): the two orange lights flash. userData.tip: the crane tip (local): put a
  // craneHook under it with top = the tip's height. o.tip [x, y] (local; [-3.8, 3.25]): a longer boom reaches further behind the bed (-5.5: 2.4 m).
  towTruck(o) {
    const g = grp(), W = 2.0, wc = o.color || '#F4F3EE', band = o.band || '#E8742A', Y = '#F2C230', navy = '#1E3E7B';
    g.add(at(box(6.5, 0.3, 1.8, '#3A3D44'), -0.35, 0.62, 0));                                                       // chassis
    for (const x of [2.05, -1.35, -2.45]) for (const z of [-0.86, 0.86]) g.add(at(cyl(0.46, 0.46, 0.34, P.ink, 12), x, 0.46, z, PI / 2), at(cyl(0.2, 0.2, 0.02, '#C9CDD3', 8), x, 0.46, z * 1.21, PI / 2));
    g.add(at(box(1.7, 1.6, W, wc, { outline: 0.012 }), 2.15, 0.75 + 0.8, 0));                                      // cab, 0.75 .. 2.35
    g.add(at(box(0.2, 0.5, W - 0.1, wc, { outline: 0.008 }), 3.08, 1.0, 0));                                       // the nose
    g.add(at(box(0.02, 0.6, 1.72, '#4D6E8A', { noGrain: true }), 3.005, 1.88, 0, 0, 0, -0.12));                    // windscreen
    for (const sz of [-1, 1]) g.add(at(box(0.85, 0.55, 0.02, '#4D6E8A', { noGrain: true }), 2.4, 1.86, sz * (W / 2 + 0.01)));
    g.add(at(box(1.72, 0.2, W + 0.02, band), 2.15, 1.3, 0), at(box(0.22, 0.2, W - 0.08, band), 3.09, 1.12, 0));
    g.add(at(box(0.04, 0.3, 1.4, '#2A2C31'), 3.19, 0.98, 0));
    for (const sz of [-1, 1]) g.add(at(box(0.04, 0.16, 0.32, '#FFF6C8', { emissive: '#FFF0B0', noGrain: true }), 3.19, 1.0, sz * 0.72));
    for (const sz of [-1, 1]) g.add(at(label('FOURRIÈRE', o.signW ?? 1.3, o.signH ?? 0.3, { bg: wc, fg: navy, wrap: false }), o.signX ?? 2.0, o.signY ?? 1.62, sz * (W / 2 + 0.012), 0, sz > 0 ? 0 : PI, 0));   // (final pass) o.signX / signY / signW / signH: the word bigger and clear of the wheels
    // light bar
    g.add(at(box(0.36, 0.1, 1.5, '#2A2C31'), 2.2, 2.4, 0)); const [bOn, bOff] = lamp('#FF9A1F', '#B8691C'), beac = [];
    for (const sz of [-1, 1]) { const on = at(box(0.3, 0.2, 0.36, '', { material: bOn }), 2.2, 2.55, sz * 0.5), off = at(box(0.3, 0.2, 0.36, '', { material: bOff }), 2.2, 2.55, sz * 0.5); g.add(on, off); beac.push([on, off, sz]); }
    // bed and skirts
    g.add(at(box(4.6, 0.18, 2.1, '#5A5F69', { outline: 0.01 }), -0.8, 1.06, 0));
    for (const sz of [-1, 1]) { g.add(at(box(4.6, 0.08, 0.06, Y), -0.8, 1.18, sz * 1.05), at(box(3.4, 0.4, 0.04, wc, { outline: 0.006 }), -0.65, 0.78, sz * 0.94));
      g.add(at(label('FOURRIÈRE', 2.2, 0.32, { bg: wc, fg: navy, wrap: false }), -0.65, 0.78, sz * 0.962, 0, sz > 0 ? 0 : PI, 0)); }
    // crane: a post at the back of the bed and a boom leaning back and up
    const post = [-2.75, 1.15], top = [-2.75, 2.45], tip = o.tip || [-3.8, 3.25];
    g.add(at(box(0.28, top[1] - post[1], 0.28, Y, { outline: 0.008 }), post[0], (post[1] + top[1]) / 2, 0));
    const bl = Math.hypot(tip[0] - top[0], tip[1] - top[1]), ba = Math.atan2(tip[1] - top[1], tip[0] - top[0]);
    g.add(at(box(bl + 0.2, 0.22, 0.22, Y, { outline: 0.008 }), (top[0] + tip[0]) / 2, (top[1] + tip[1]) / 2, 0, 0, 0, ba));
    g.add(at(box(0.3, 0.3, 0.3, '#2A2C31'), tip[0], tip[1], 0), at(cyl(0.12, 0.12, 0.3, '#3A3D44', 10), top[0], top[1], 0, PI / 2));
    g.userData.update = t => { const on = !o.beacons || inSpan(o.beacons, t);
      for (const [a, b, sz] of beac) { const lit = on && Math.floor(t * 5 + (sz > 0 ? 0.5 : 0)) % 2 === 0; a.visible = lit; b.visible = !lit; } };
    g.userData.update(0); g.userData.tip = [tip[0], tip[1] - 0.15, 0];
    return g;
  },

  // A wheel clamp (sabot de Denver), bright yellow, sized for a shoe (o.s 1; 2.2 for a car wheel). Origin at the middle of the foot; the foot points
  // along +Z: a disc on the outer side (+X), a small plate on the inner side, a bar over the instep, a padlock. o.snapAt: the bar swings shut in 0.07 s
  // with a bounce (open before, by o.open 1.3 rad); o.rattle [[t, dur]]: it rattles (the foot tried to go).
  wheelClamp(o) {
    const Y = o.color || '#F2C230', g = grp(), k = grp(); g.add(k); k.scale.setScalar(o.s ?? 1);
    k.add(at(cyl(0.16, 0.16, 0.05, Y, 14, { outline: 0.006 }), 0.15, 0.06, 0, 0, 0, PI / 2), at(cyl(0.05, 0.05, 0.07, '#2A2C31', 8), 0.16, 0.06, 0, 0, 0, PI / 2));
    k.add(at(box(0.04, 0.16, 0.2, Y, { outline: 0.005 }), -0.14, 0.06, 0));
    const bar = grp(); bar.position.set(0.15, 0.06, 0); k.add(bar);
    bar.add(at(box(0.32, 0.05, 0.07, Y, { outline: 0.005 }), -0.15, 0.12, 0.02), at(box(0.05, 0.14, 0.07, Y, { outline: 0.005 }), -0.29, 0.06, 0.02));
    k.add(at(box(0.09, 0.11, 0.06, '#C8322A', { outline: 0.005 }), 0.19, -0.06, 0.08), at(torus(0.03, 0.009, '#9AA0A8', 5, 10, PI), 0.19, 0.0, 0.08));
    g.userData.update = t => {
      const u = o.snapAt == null ? 1 : (t - o.snapAt) / 0.07; bar.rotation.z = u < 0 ? -(o.open ?? 1.3) : -(o.open ?? 1.3) * (1 - clamp01(u)) + (u > 1 ? 0.12 * wob((t - o.snapAt - 0.07), 40, 9) : 0);
      let r = 0; for (const [a, d] of o.rattle || []) if (t >= a && t < a + d) r = 1; k.position.set(0.01 * r * Math.sin(t * 77), 0.008 * r * Math.abs(Math.sin(t * 61)), 0); k.rotation.z = 0.06 * r * Math.sin(t * 53);
    };
    g.userData.update(0); return g;
  },

  // (cycle 8) A man swollen round like a balloon: a navy sphere o.r (0.5 m) with his shirt's white V, his red tie and teal lapels on its front (+Z),
  // to attach to his torso and grow with scale keys (the rig's boxes only made a bigger box: a sign on a pole). o.suit, o.tie, o.lapel
  balloonSuit(o) {
    const R = o.r ?? 0.5, g = grp(), ball = new THREE.Mesh(new THREE.SphereGeometry(R, 20, 14), mat(o.suit || '#1E2E44')); ball.castShadow = true; g.add(ball);
    const f = R * 0.97, sh = at(box(R * 0.42, R * 0.62, 0.02, '#F2EEE6'), 0, R * 0.42, f - 0.02, -0.5, 0, 0); g.add(sh);
    for (const sx of [-1, 1]) g.add(at(box(R * 0.2, R * 0.66, 0.02, o.lapel || '#2E8C8A'), sx * R * 0.22, R * 0.4, f - 0.01, -0.5, 0, sx * 0.35));
    g.add(at(box(R * 0.1, R * 0.7, 0.025, o.tie || '#C8202A'), 0, R * 0.12, f + 0.005, -0.15, 0, 0));
    return g;
  },

  // A Paris pay-and-display machine (horodateur), front +Z: a dark grey column, a blue P on a stalk, a pale green screen (o.screen 'PAYEZ ICI'), a keypad,
  // a card slot, a ticket tray, a blue sticker (o.sticker 'STATIONNEMENT PAYANT'). o.ticketAt: a ticket slides out of the tray (and stays out); o.ticketGone: it disappears (taken).
  parkingMeter(o) {
    const g = grp(), D = '#3B4048';
    g.add(at(box(0.5, 0.1, 0.38, '#2A2C31'), 0, 0.05, 0), at(box(0.42, 1.25, 0.3, D, { outline: 0.008 }), 0, 0.725, 0), at(box(0.46, 0.08, 0.34, '#2A2C31'), 0, 1.39, 0));
    g.add(at(box(0.04, 0.24, 0.04, '#2A2C31'), 0, 1.55, 0));
    for (const s of [1, -1]) g.add(at(label('P', 0.32, 0.32, { bg: '#1E5BB8', fg: '#FFFFFF', wrap: false }), 0, 1.82, s * 0.012, 0, s > 0 ? 0 : PI, 0));
    g.add(at(label(o.screen || 'PAYEZ ICI', 0.3, 0.13, { bg: '#BFE6B0', fg: '#1E2A1E', wrap: false }), 0, 1.2, 0.152));
    for (let r = 0; r < 4; r++) for (let c = 0; c < 3; c++) g.add(at(box(0.06, 0.04, 0.02, '#C9CDD3'), -0.08 + 0.08 * c, 1.02 - 0.055 * r, 0.155));
    g.add(at(box(0.14, 0.02, 0.02, '#111215'), 0, 0.74, 0.155), at(box(0.22, 0.07, 0.07, '#1B1C20'), 0, 0.56, 0.16));
    g.add(at(label(o.sticker || 'STATIONNEMENT PAYANT', o.stickerW ?? 0.36, o.stickerH ?? 0.08, { bg: o.stickerBg || '#1E5BB8', fg: '#FFFFFF', wrap: !!o.stickerWrap }), 0, o.stickerY ?? 0.36, 0.152));   // (cycle 8) o.stickerW / H / Y / Bg / Wrap: a sticker that reads
    const tk = grp(at(box(0.09, 0.004, 0.14, '#FFFFFF', { noGrain: true }), 0, 0, 0), at(box(0.09, 0.005, 0.025, '#1E5BB8', { noGrain: true }), 0, 0.001, 0.05)); tk.position.set(0, 0.575, 0.12); g.add(tk);
    g.userData.update = t => { const u = o.ticketAt == null ? -1 : clamp01((t - o.ticketAt) / 0.3); tk.visible = u > 0 && !(o.ticketGone != null && t >= o.ticketGone); tk.position.z = 0.12 + 0.12 * u; };
    g.userData.update(0); return g;
  },

  // A painted parking bay on the asphalt: white lines o.w (2.4) by o.l (5.0) long along X, open on the -X side; a number painted at the far end (o.num
  // '12'); an optional word along the bay (o.word). Origin at the middle of the bay, at ground level.
  parkingBay(o) {
    const w = o.w ?? 2.4, l = o.l ?? 5.0, g = grp(), wm = mat('#F2F1EA', { noGrain: true });
    for (const sz of [-1, 1]) g.add(at(box(l, 0.008, 0.1, '', { material: wm }), 0, 0.01, sz * w / 2));
    g.add(at(box(0.1, 0.008, w + 0.1, '', { material: wm }), l / 2, 0.01, 0));
    const txt = (s, ww, hh, x, rot) => at(canvasPlane(ww, hh, (c, W, H) => { c.fillStyle = '#F2F1EA'; c.font = `900 ${Math.round(H * 0.8)}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(s, W / 2, H * 0.55); }, { res: 512, transparent: true }), x, 0.014, 0, -PI / 2, 0, rot);
    if (o.num) g.add(txt(String(o.num), 1.0, 0.7, l / 2 - 0.65, PI / 2 + (o.numFlip ? PI : 0)));   // (final pass) o.numFlip: the number reads from the lane side
    if (o.word) g.add(txt(o.word, l * 0.62, 0.42, -0.2, PI / 2 + (o.wordFlip ? PI : 0)));
    return g;
  },

  // The pound's cash desk: a prefab cabin o.w (2.4) wide, 2.75 high, 1.8 deep, front +Z, a tall window (0.98-2.38 m) with a counter (a clerk stands
  // behind it at z = 0.35: her face in the window), a blue CAISSE board on the roof; o.notice: a printed notice taped beside the window ({head, big, lines}).
  cashBooth(o) {
    const w = o.w ?? 2.4, h = 2.75, d = 1.8, g = grp(), wall = o.color || '#E9E6DE', trim = '#9AA3AD';
    const W0 = -0.7, W1 = 0.7, Y0 = 0.98, Y1 = 2.38;   // the window opening: tall enough that the cashier's face shows in it
    g.add(at(box(w, h, 0.08, '#CFCAC0'), 0, h / 2, -d / 2));                                                     // back wall
    for (const sx of [-1, 1]) g.add(at(box(0.08, h, d, wall, { outline: 0.01 }), sx * w / 2, h / 2, 0));
    g.add(at(box(w + 0.16, 0.14, d + 0.16, trim, { outline: 0.01 }), 0, h + 0.07, 0));                        // roof
    g.add(at(box(w, Y0, 0.08, wall, { outline: 0.008 }), 0, Y0 / 2, d / 2), at(box(w, h - Y1, 0.08, wall, { outline: 0.008 }), 0, (h + Y1) / 2, d / 2));
    g.add(at(box(w / 2 + W0, Y1 - Y0, 0.08, wall), (-w / 2 + W0) / 2, (Y0 + Y1) / 2, d / 2), at(box(w / 2 - W1, Y1 - Y0, 0.08, wall), (w / 2 + W1) / 2, (Y0 + Y1) / 2, d / 2));
    g.add(at(box(W1 - W0 + 0.2, 0.06, 0.42, trim, { outline: 0.006 }), 0, Y0 + 0.03, d / 2 + 0.12));            // the counter
    g.add(at(box(W1 - W0, Y1 - Y0, 0.01, '', { material: glassMat(0.12, '#DDEFF4') }), 0, (Y0 + Y1) / 2 + 0.06, d / 2 + 0.02));
    g.add(at(box(W1 - W0, 0.1, 0.03, '#C9CDD3'), 0, Y0 + 0.07, d / 2 + 0.02));                                   // the slot under the glass
    g.add(at(box(1.5, 0.36, 0.05, '#1E5BB8', { outline: 0.006 }), 0, h + 0.36, d / 2 - 0.02), at(label(o.sign || 'CAISSE', 1.36, 0.28, { bg: '#1E5BB8', fg: '#FFFFFF', wrap: false }), 0, h + 0.36, d / 2 + 0.01));   // on the roof
    g.add(at(box(0.05, 0.2, 0.05, '#5A5F69'), -0.6, h + 0.12, d / 2 - 0.05), at(box(0.05, 0.2, 0.05, '#5A5F69'), 0.6, h + 0.12, d / 2 - 0.05));
    g.add(at(box(w - 0.16, 0.06, d - 0.2, '#B7B0A3'), 0, 0.03, 0));
    return g;
  },

  // A wall of flats over the street, front +Z: o.cols (3) x o.rows (2) windows with their shutters and a rail; behind each window a room (an actor stands
  // in it on a floor at the window's foot minus 0.95 m: userData.floors[row]); o.w (7.5), o.h (8.0), o.y0 (3.0: the first floor's floor), o.storey (3.0).
  // o.lit [[t, 0..1]]: the rooms light up (night); o.color; o.shutter; o.depth (1.8: how deep the rooms go behind the front).
  flatsWall(o) {
    const cols = o.cols ?? 3, rows = o.rows ?? 2, w = o.w ?? 7.5, h = o.h ?? 8.0, y0 = o.y0 ?? 3.0, sto = o.storey ?? 3.0, g = grp();
    const wall = o.color || '#F1E6CF', sh = o.shutter || '#5C8FA8', ww = 1.15, wh = 1.55, sill = 0.95, D = o.depth ?? 1.8, cw = w / cols;
    const xs = Array.from({ length: cols }, (_, c) => -w / 2 + cw * (c + 0.5)), ys = Array.from({ length: rows }, (_, r) => y0 + sto * r + sill);
    // the facade: horizontal bands and piers around the openings
    const band = (ya, yb) => yb > ya && g.add(at(box(w, yb - ya, 0.3, wall, { outline: 0.008 }), 0, (ya + yb) / 2, -0.15));
    let yPrev = 0; for (const y of ys) { band(yPrev, y); yPrev = y + wh; } band(yPrev, h);
    for (const y of ys) { let xPrev = -w / 2; for (const x of xs) { const a = x - ww / 2; if (a > xPrev) g.add(at(box(a - xPrev, wh, 0.3, wall), (a + xPrev) / 2, y + wh / 2, -0.15)); xPrev = x + ww / 2; }
      g.add(at(box(w / 2 - xPrev, wh, 0.3, wall), (w / 2 + xPrev) / 2, y + wh / 2, -0.15)); }
    g.add(at(box(w + 0.1, 0.4, 0.34, o.foot || '#DCCDB0'), 0, 0.2, -0.12));
    const rooms = [], litMats = [];
    for (const y of ys) for (const x of xs) {
      const fl = y - sill, rm = mat(o.room || '#E3C9A0', { unique: true }); litMats.push(rm);
      g.add(at(box(ww + 0.4, sto - 0.1, 0.06, '', { material: rm }), x, fl + (sto - 0.1) / 2, -D));                 // the back wall of the room
      for (const sx of [-1, 1]) g.add(at(box(0.06, sto - 0.1, D, '#D8BE95'), x + sx * (ww / 2 + 0.2), fl + (sto - 0.1) / 2, -D / 2));
      g.add(at(box(ww + 0.4, 0.06, D, '#9C7A55'), x, fl - 0.03, -D / 2), at(box(ww + 0.4, 0.06, D, '#EFE4D0'), x, fl + sto - 0.1, -D / 2));
      g.add(at(box(ww + 0.16, 0.07, 0.36, '#DCCDB0', { outline: 0.005 }), x, y - 0.035, 0.02));                            // sill
      for (const sx of [-1, 1]) g.add(at(box(0.52, wh, 0.05, sh, { outline: 0.005 }), x + sx * (ww / 2 + 0.28), y + wh / 2, 0.04));   // shutters, open
      const rail = grp(); for (let i = 0; i <= 8; i++) rail.add(at(box(0.02, 0.42, 0.02, '#2B2D33'), -ww / 2 + i * ww / 8, 0.21, 0));
      rail.add(at(box(ww, 0.03, 0.03, '#2B2D33'), 0, 0.42, 0)); rail.position.set(x, y, 0.06); rail.traverse(q => { if (q.isMesh) q.castShadow = false; }); g.add(rail);
      rooms.push([x, fl]);
    }
    g.userData.floors = ys.map(y => y - sill); g.userData.rooms = rooms;
    const base = new THREE.Color(o.room || '#E3C9A0'), lit = new THREE.Color('#FFD27A');
    g.userData.update = t => { const k = lerpKeys(o.lit, t, [0])[0]; for (const m of litMats) { m.color.copy(base).lerp(lit, k); if (m.emissive) m.emissive.set('#C9922E').multiplyScalar(0.6 * k); } };
    g.userData.update(0); return g;
  },

  // A pound sign on two posts: o.text ('FOURRIÈRE'), o.sub (a smaller second line), o.w (3.4), o.h (1.1), o.y (2.2: the bottom of the board); front +Z.
  poundSign(o) {
    const w = o.w ?? 3.4, h = o.h ?? 1.1, y = o.y ?? 2.2, g = grp();
    for (const sx of [-1, 1]) g.add(at(box(0.12, y + h, 0.12, '#5A5F69', { pivot: 'bottom' }), sx * w * 0.38, 0, -0.08));
    g.add(at(box(w + 0.1, h + 0.1, 0.08, '#1E3E7B', { outline: 0.01 }), 0, y + h / 2, 0));
    g.add(at(label(o.text || 'FOURRIÈRE', w - 0.2, (o.sub ? 0.62 : 0.9) * h, { bg: '#1E3E7B', fg: '#FFFFFF', wrap: false }), 0, y + h * (o.sub ? 0.64 : 0.5), 0.045));
    if (o.sub) g.add(at(label(o.sub, w - 0.4, 0.3 * h, { bg: '#1E3E7B', fg: '#F2C230', wrap: false }), 0, y + h * 0.2, 0.045));
    return g;
  },
};
