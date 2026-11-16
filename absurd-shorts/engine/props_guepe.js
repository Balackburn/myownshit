// « La guêpe » (story 81): this man filed a complaint against a wasp; the police charged; he demanded an air strike; a satellite found it near the
// sugar bowl; an aircraft carrier put to sea, in his sink; a fighter took off from the sink, missed the wasp, razed the building and the town hall;
// the front froze between the fridge and the sink all winter, sugar rationed; the State asked for a ceasefire, the wasp got the sugar bowl, the
// general staff gave itself medals, the wasp too. It was a fly.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere, addOutline, mat, rng } from './style.js';
import { grp, at, canvasPlane, glowSprite, buildProp } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
// the weight of a list of windows at t: 0 outside, eased up over e s after a window opens and down over e s before it closes
const winW = (wins, t, e = 0.08) => { if (!wins) return 0; let w = 0; for (const [a, b] of wins) w = Math.max(w, Math.min(smooth((t - a) / e), smooth((b - t) / e))); return w; };
// a pop-in: 0 before t0, an overshoot to 1.25 at t0 + 0.09, back to 1 at t0 + 0.2
const popK = (t, t0) => { if (t0 == null) return 1; const u = t - t0; if (u <= 0) return 0; if (u < 0.09) return 1.25 * (u / 0.09); if (u < 0.2) return 1.25 - 0.25 * (u - 0.09) / 0.11; return 1; };
const basic = (c, o = {}) => new THREE.MeshBasicMaterial({ color: c, transparent: o.opacity != null, opacity: o.opacity ?? 1, depthWrite: o.opacity == null, side: o.side || THREE.FrontSide });
const _up = new THREE.Vector3(0, 1, 0), _a = new THREE.Vector3(), _b = new THREE.Vector3();
// a unit cylinder (height 1 along Y, centred) stretched and turned so that it runs from a to b
function setRod(m, a, b) {
  _a.set(a[0], a[1], a[2]); _b.set(b[0], b[1], b[2]); const L = _a.distanceTo(_b);
  m.position.copy(_a).add(_b).multiplyScalar(0.5); m.scale.set(1, Math.max(1e-4, L), 1);
  if (L > 1e-6) m.quaternion.setFromUnitVectors(_up, _b.sub(_a).normalize());
}
const unitRod = (r, color) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 1, 5), mat(color)); m.castShadow = true; return m; };
const mixP = (a, b, w) => [a[0] + (b[0] - a[0]) * w, a[1] + (b[1] - a[1]) * w, a[2] + (b[2] - a[2]) * w];
const noShadow = m => { m.traverse(c => { c.castShadow = false; }); return m; };

// the insect's own flag (pivot at the foot of its pole): a pale toothpick pole o.h tall, a black pennant with a white sugar cube on it, waving
function pennant(h = 0.09, w = 0.06) {
  const g = grp(), pole = at(cyl(h * 0.025, h * 0.025, h, '#E8D9B5', 5, { pivot: 'bottom' }), 0, 0, 0);
  const cloth = canvasPlane(w, w * 0.62, (c, W, H) => { c.clearRect(0, 0, W, H); c.fillStyle = '#16181C'; c.beginPath(); c.moveTo(0, 0); c.lineTo(W, H * 0.5); c.lineTo(0, H); c.closePath(); c.fill();
    c.fillStyle = '#FFFFFF'; c.fillRect(W * 0.12, H * 0.33, W * 0.24, H * 0.34); c.strokeStyle = '#B9B9B9'; c.lineWidth = W * 0.02; c.strokeRect(W * 0.12, H * 0.33, W * 0.24, H * 0.34); }, { res: 128, transparent: true });
  const cg = grp(); cloth.position.set(w / 2, 0, 0); cg.add(cloth); cg.position.set(0, h - w * 0.31, 0); g.add(pole, cg);
  g.userData.wave = t => { cg.rotation.y = 0.25 * Math.sin(t * 5.5); cloth.rotation.y = 0.15 * Math.sin(t * 7 + 1); };
  return g;
}

export const GUEPE_PROPS = {
  // The hero insect, a house fly (pivot at its feet, the head toward +Z; 0.11 m long at scale 1): a dark grey thorax and abdomen with a blue-green
  // sheen, a round head with two big dark-red eyes (a white glint on each), two clear veined wings folded back in a V, six thin black legs. No stripes
  // and no sting: the narration says « guêpe », the picture never lies. o.buzz [[t0, t1], ...]: airborne, the wings a fast blur (a pale fan each side),
  // the legs hanging, a small bob (o.bob 0.01 m); o.rub [[t0, t1], ...]: the front feet meet under the head and rub; o.eat [[t0, t1], ...]: the head dips,
  // the proboscis out, a dab every 0.25 s; o.salute (s): the right front leg up to the eye and held; o.plant [t0, t1]: both front legs up over the head
  // (holding a flag's pole), pushed down at t1; o.medal (true or s): a tiny gold medal on a tricolour ribbon on its right flank (o.medalSide -1: left);
  // o.halo (0): a soft pale glow behind it (dark backgrounds); o.look [[t, rad], ...]: the head turns (yaw)
  houseFly(o) {
    const g = grp(), bd = grp(); g.add(bd);
    const dark = '#3A3E44', belly = '#2C353A';
    const thorax = at(sphere(0.024, dark, 1), 0, 0.03, 0.002); thorax.scale.set(1, 0.92, 1.1); addOutline(thorax, 0.14);
    const abdomen = at(sphere(0.027, belly, 1), 0, 0.026, -0.04); abdomen.scale.set(1.0, 0.78, 1.5); addOutline(abdomen, 0.12);
    const sheen = at(sphere(0.02, '#3F7074', 1, { opacity: 0.55 }), 0.006, 0.036, -0.038); sheen.scale.set(0.8, 0.45, 1.3); sheen.castShadow = false;
    const head = grp(); head.position.set(0, 0.034, 0.03); bd.add(thorax, abdomen, sheen, head);
    const hd = sphere(0.018, dark, 1); hd.scale.set(1.15, 1, 0.9); addOutline(hd, 0.14); head.add(hd);
    for (const s of [-1, 1]) {
      const e = at(sphere(0.0155, '#9C2A21', 1), s * 0.0135, 0.004, 0.006); e.scale.set(0.9, 1.05, 0.95); addOutline(e, 0.1); head.add(e);
      const gl = at(sphere(0.0035, '#FFFFFF', 0, { emissive: '#FFFFFF' }), s * 0.0125, 0.011, 0.019); gl.castShadow = false; head.add(gl);
      head.add(at(cyl(0.0012, 0.0012, 0.012, '#1E2024', 4), s * 0.004, 0.012, 0.016, 0.6, 0, -s * 0.3));
    }
    const prob = grp(); prob.position.set(0, -0.012, 0.012); prob.add(at(cyl(0.002, 0.0035, 0.016, '#2A2E33', 5, { pivot: 'top' }), 0, 0, 0)); head.add(prob);
    // the wings: a veined clear blade on a hinge (Euler order ZYX: swung out about Y, then raised about Z); a pale fan each side when they buzz
    const wingTex = (c, W, H) => { c.clearRect(0, 0, W, H); c.fillStyle = 'rgba(232,240,248,0.6)'; c.strokeStyle = 'rgba(36,42,50,0.9)'; c.lineWidth = W * 0.04;
      c.beginPath(); c.ellipse(W / 2, H / 2, W * 0.45, H * 0.47, 0, 0, TAU); c.fill(); c.stroke(); c.lineWidth = W * 0.025;
      for (const f of [0.3, 0.5, 0.72]) { c.beginPath(); c.moveTo(W / 2, H * 0.96); c.quadraticCurveTo(W * f, H * 0.5, W * (0.12 + f * 0.75), H * 0.06); c.stroke(); } };
    const wings = [-1, 1].map(s => {
      const h = grp(); h.rotation.order = 'ZYX'; h.position.set(s * 0.009, 0.05, 0.002);
      const bl = canvasPlane(0.032, 0.078, wingTex, { res: 128, transparent: true }); bl.rotation.x = -PI / 2; bl.position.set(0, 0, -0.039);
      bl.material.depthWrite = false; bl.castShadow = false; h.add(bl);
      const fh = grp(); fh.position.copy(h.position); fh.rotation.z = s * 0.45; if (s < 0) fh.scale.x = -1;
      const fan = new THREE.Mesh(new THREE.CircleGeometry(0.078, 18, -0.4 * PI, 0.8 * PI), basic('#E9EFF5', { opacity: 0.3, side: THREE.DoubleSide })); fan.rotation.x = -PI / 2; fan.castShadow = false;
      fh.add(fan); fh.visible = false; bd.add(h, fh); return { s, h, fh, fan };
    });
    // the legs: a thigh and a shin each, re-aimed every frame (front, middle, hind; right side s = -1)
    const legs = [];
    [0.016, 0.0, -0.014].forEach((z, i) => { for (const s of [-1, 1]) { const up = unitRod(0.0024, '#1C1E22'), lo = unitRod(0.002, '#1C1E22'); bd.add(up, lo); legs.push({ s, i, z, up, lo }); } });
    let medal = null;
    if (o.medal != null && o.medal !== false) {
      const ms = o.medalSide ?? 1; medal = grp();
      ['#2F62B5', '#F4F4F0', '#E0413A'].forEach((c, i) => medal.add(at(box(0.0045, 0.014, 0.0012, c), -0.0045 + i * 0.0045, 0.0, 0)));
      const disc = at(cyl(0.0085, 0.0085, 0.002, '#E6B84A', 12, { emissive: '#5A3E0A' }), 0, -0.012, 0.0006, PI / 2, 0, 0); addOutline(disc, 0.12); medal.add(disc);
      medal.position.set(ms * 0.021, 0.033, 0.012); medal.rotation.y = ms * PI / 4; bd.add(medal);
    }
    if (o.halo) { const hs = glowSprite('#FFF4D6', 0.22, o.halo); hs.position.set(0, 0.03, -0.01); g.add(hs); }
    const lookAt_ = (t) => { const L = o.look; if (!L || !L.length) return 0; if (t <= L[0][0]) return L[0][1]; for (let i = 1; i < L.length; i++) if (t <= L[i][0]) { const u = smooth((t - L[i - 1][0]) / Math.max(1e-6, L[i][0] - L[i - 1][0])); return L[i - 1][1] + (L[i][1] - L[i - 1][1]) * u; } return L[L.length - 1][1]; };
    g.userData.update = t => {
      const wB = winW(o.buzz, t, 0.05), wR = winW(o.rub, t, 0.1), wE = winW(o.eat, t, 0.1);
      const wS = o.salute == null ? 0 : smooth((t - o.salute) / 0.12);
      const wP = o.plant ? winW([[o.plant[0], o.plant[1] + 0.25]], t, 0.12) : 0, push = o.plant ? smooth((t - o.plant[1]) / 0.1) : 0;
      bd.position.y = wB * ((o.bob ?? 0.01) * (0.6 + 0.4 * Math.sin(t * 6.3)) + 0.006);
      bd.position.x = wB * 0.004 * Math.sin(t * 4.1);
      const dab = wE * 0.12 * Math.max(0, Math.sin(t * TAU * 4));
      bd.rotation.x = 0.12 * wE - 0.12 * wP; head.rotation.x = 0.45 * wE + dab; head.rotation.y = lookAt_(t); prob.scale.set(1, 0.2 + 0.8 * wE, 1);
      for (const W of wings) {
        if (wB > 0.5) { const ph = t * TAU * 11.3 + (W.s > 0 ? 0 : 0.5); W.h.rotation.set(0, -W.s * (0.95 + 0.55 * Math.sin(ph)), W.s * (0.6 + 0.45 * Math.sin(ph + 1.2)));
          W.fh.visible = true; W.fan.material.opacity = 0.24 + 0.08 * Math.sin(t * 37); }
        else { W.h.rotation.set(0, -W.s * (0.3 + 0.04 * wR), W.s * 0.05); W.fh.visible = false; }
      }
      const wv = t * TAU * 3.2;
      for (const L of legs) {
        const { s, i, z } = L, R = [s * 0.011, 0.02, z];
        let K = [s * 0.04, 0.034, z + (i === 0 ? 0.012 : i === 2 ? -0.01 : 0)], F = [s * 0.05, 0.0, z + (i === 0 ? 0.03 : i === 2 ? -0.03 : 0)];
        if (i === 0) {
          if (wR > 0) { const k2 = [s * 0.022, 0.03, 0.045], f2 = [s * (0.004 + 0.004 * Math.sin(wv + (s > 0 ? 0 : PI))), 0.024 + 0.004 * Math.sin(wv * 0.5 + s), 0.064 + 0.006 * Math.sin(wv + (s > 0 ? PI : 0))];
            K = mixP(K, k2, wR); F = mixP(F, f2, wR); }
          if (wP > 0) { K = mixP(K, [s * 0.026, 0.054, 0.046], wP); F = mixP(F, [s * 0.008, 0.078 - 0.022 * push, 0.06], wP); }
          if (s < 0 && wS > 0) { K = mixP(K, [s * 0.034, 0.058, 0.03], wS); F = mixP(F, [s * 0.017, 0.066, 0.046], wS); }
        }
        if (wB > 0) { K = mixP(K, [s * 0.03, 0.012, z - 0.004], wB); F = mixP(F, [s * 0.028, -0.008, z - 0.022], wB); }
        setRod(L.up, R, K); setRod(L.lo, K, F);
      }
      if (medal) medal.visible = o.medal === true || t >= o.medal;
    };
    g.userData.update(0); return g;
  },

  // The sugar bowl (pivot at its foot, front +Z; 0.16 m across): white porcelain with a blue band and a gold rim, two little ears, a domed lid with a
  // knob. o.lid 'off': the lid lies on its side beside it and a heap of sugar cubes shows; o.clink (s): the lid hops and settles; o.flag (s): the
  // insect's flag pushed into the knob at that time (it shows from o.flagFrom, o.flag - 0.6, held 4.5 cm above the knob, and wobbles once in);
  // o.dust: a grey film (ruins); o.snow: a cap of snow on the lid. userData.rim (the front of the rim), userData.knob (the top of the knob)
  sugarBowl(o) {
    const g = grp(), R = 0.08, H = 0.075, wht = o.dust ? '#E6E2DA' : '#FAFAF6', y0 = 0.01;
    const bowl = at(cyl(R, R * 0.74, H, wht, 18), 0, y0 + H / 2, 0); addOutline(bowl, 0.04); g.add(bowl);
    g.add(at(cyl(R * 0.62, R * 0.66, y0, wht, 16, { pivot: 'bottom' }), 0, 0, 0), at(cyl(R * 0.955 + 0.002, R * 0.9 + 0.002, 0.016, '#2F5FA8', 18), 0, y0 + H * 0.62, 0));
    g.add(at(new THREE.Mesh(new THREE.TorusGeometry(R, 0.004, 5, 24), mat('#D9B04A')), 0, y0 + H, 0, PI / 2, 0, 0));
    for (const s of [-1, 1]) g.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.02, 0.006, 5, 10, PI), mat(wht)), s * (R + 0.006), y0 + H * 0.6, 0, 0, 0, -s * PI / 2));
    const lid = grp(), dome = new THREE.Mesh(new THREE.SphereGeometry(R * 1.02, 18, 8, 0, TAU, 0, PI / 2), mat(wht)); dome.scale.y = 0.42; dome.castShadow = true; addOutline(dome, 0.04);
    const knob = at(sphere(0.016, wht, 1), 0, R * 0.42 + 0.012, 0); addOutline(knob, 0.12);
    lid.add(dome, knob, at(new THREE.Mesh(new THREE.TorusGeometry(R * 0.55, 0.003, 4, 20), mat('#2F5FA8')), 0, R * 0.3, 0, PI / 2, 0, 0));
    if (o.snow) { const sn = new THREE.Mesh(new THREE.SphereGeometry(R * 0.98, 14, 6, 0, TAU, 0, PI / 2), mat('#F7F9FB')); sn.scale.y = 0.55; sn.position.y = 0.008; lid.add(sn); }
    const top = y0 + H, off = o.lid === 'off';
    if (off) { lid.position.set(R * 1.75, R * 0.98, 0.02); lid.rotation.set(0, 0.3, PI / 2 - 0.15);
      g.add(at(cyl(R * 0.94, R * 0.94, 0.004, '#F2EBDD', 18), 0, top - 0.012, 0));
      const rr = rng(o.seed || 5); for (let i = 0; i < 9; i++) { const a = i / 9 * TAU + rr() * 0.4, d = i === 0 ? 0 : R * (0.35 + rr() * 0.3);
        const cube = at(box(0.026, 0.026, 0.026, '#FFFFFF', { outline: 0.06 }), Math.cos(a) * d, top - 0.004 + (i === 0 ? 0.018 : rr() * 0.01), Math.sin(a) * d, rr() * 0.5, rr() * 1.5, rr() * 0.5); g.add(cube); } }
    else lid.position.set(0, top, 0);
    g.add(lid);
    let flag = null; if (o.flag != null) { flag = pennant(0.09, 0.06); g.add(flag); }
    const kTop = top + R * 0.42 + 0.028;
    g.userData.update = t => {
      if (!off) { lid.position.y = top; lid.rotation.z = 0;
        if (o.clink != null && t >= o.clink) { const u = t - o.clink; lid.position.y = top + 0.012 * Math.max(0, Math.sin(u * 22)) * Math.exp(-u * 6); lid.rotation.z = 0.06 * Math.sin(u * 30) * Math.exp(-u * 7); } }
      if (flag) { const from = o.flagFrom ?? o.flag - 0.6; flag.visible = t >= from; const u = t - o.flag, d = u < 0 ? 1 : 1 - smooth(u / 0.1);
        flag.position.set(0.004, kTop - 0.02 + 0.045 * d, 0); flag.rotation.z = u > 0 ? 0.25 * Math.exp(-u * 5) * Math.sin(u * 18) : 0; flag.userData.wave(t); }
    };
    g.userData.update(0); g.userData.rim = [0, top, R * 0.92]; g.userData.knob = [0, kTop, 0]; return g;
  },

  // The insect's flag on its own (pivot at the foot of its pole; o.h 0.09 m tall, o.w 0.06 wide): planted on the fridge, it marks the enemy line;
  // o.at: it pops in
  pennantFlag(o) {
    const g = grp(), p = pennant(o.h ?? 0.09, o.w ?? 0.06); g.add(p);
    g.userData.update = t => { const k = popK(t, o.at); p.scale.setScalar(Math.max(0.001, k)); p.visible = k > 0.001; p.userData.wave(t); };
    g.userData.update(0); return g;
  },

  // An aircraft carrier, plain grey with an invented roundel (pivot at its waterline under the middle, the bow toward +Z; o.L 1.8 m: the size jammed in
  // a kitchen sink, scaled up with the prop's scale at sea): a hull narrowing to a raked bow, a flat dark deck wider than the hull with a white centre
  // line, an angled landing line, yellow edge marks and a catapult track; the island on the right (+X) with dark bridge windows, a mast and a turning
  // radar; o.wake: a bow wave and a white wake (at sea); o.hatch [[t, 0..1], ...]: a deck hatch opens (userData.hatch: where the white handkerchief
  // rises); o.snow: snow on the deck and the island; o.waterline (true): a dark band at y 0 and a red hull below it (seen in the sink).
  // userData.deck: the deck's height; userData.cat0 / cat1: the catapult's two ends (prop space)
  carrier(o) {
    const L = o.L ?? 1.8, B = 0.22 * L, Hh = 0.13 * L, dr = 0.05 * L, g = grp(), gry = '#8E969E', dk = '#50565D';
    const hullShape = new THREE.Shape(); hullShape.moveTo(-B / 2, L / 2); hullShape.lineTo(B / 2, L / 2); hullShape.lineTo(B / 2, -0.22 * L); hullShape.lineTo(0.05 * B, -L / 2); hullShape.lineTo(-0.05 * B, -L / 2); hullShape.lineTo(-B / 2, -0.22 * L); hullShape.closePath();
    const hg = new THREE.ExtrudeGeometry(hullShape, { depth: Hh + dr, bevelEnabled: false }); hg.rotateX(-PI / 2); hg.translate(0, -dr, 0);
    const hull = new THREE.Mesh(hg, mat(gry)); hull.castShadow = hull.receiveShadow = true; addOutline(hull, 0.01); g.add(hull);
    if (o.waterline !== false) { const lg = new THREE.ExtrudeGeometry(hullShape, { depth: dr * 0.98, bevelEnabled: false }); lg.rotateX(-PI / 2); lg.translate(0, -dr, 0); lg.scale(1.012, 1, 1.004);
      const low = new THREE.Mesh(lg, mat('#9E3B32')); g.add(low); g.add(at(box(B * 1.03, 0.012 * L, L * 0.75, '#2E3236'), 0, 0.004 * L, -0.08 * L)); }
    // the deck: wider than the hull, an angled overhang on the left at the back, a sponson on the right under the island
    const dy = Hh, dS = new THREE.Shape(), W2 = 0.165 * L;
    dS.moveTo(-W2, L * 0.48); dS.lineTo(W2 * 0.95, L * 0.48); dS.lineTo(W2, -0.05 * L); dS.lineTo(W2 * 0.55, -0.38 * L); dS.lineTo(0.03 * L, -0.5 * L); dS.lineTo(-0.06 * L, -0.5 * L); dS.lineTo(-W2 * 0.75, -0.36 * L); dS.lineTo(-W2 * 1.05, 0.05 * L); dS.closePath();
    const dg = new THREE.ExtrudeGeometry(dS, { depth: 0.012 * L, bevelEnabled: false }); dg.rotateX(-PI / 2); dg.translate(0, dy, 0);
    const deck = new THREE.Mesh(dg, mat(dk)); deck.castShadow = deck.receiveShadow = true; addOutline(deck, 0.006); g.add(deck);
    const dt = dy + 0.012 * L + 0.0015;
    g.add(at(box(0.006 * L, 0.002, 0.82 * L, '#F2F2EE'), -0.02 * L, dt, -0.02 * L));
    const ang = at(box(0.006 * L, 0.002, 0.55 * L, '#F2F2EE'), -0.06 * L, dt, 0.2 * L, 0, -0.16, 0); g.add(ang);
    for (let i = 0; i < 9; i++) g.add(at(box(0.004 * L, 0.002, 0.03 * L, '#F2C230'), (i % 2 ? 1 : -1) * W2 * 0.92, dt, -0.4 * L + i * 0.1 * L));
    const cat0 = [0.06 * L, dt, -0.32 * L], cat1 = [0.06 * L, dt, 0.45 * L];
    g.add(at(box(0.008 * L, 0.0025, cat1[2] - cat0[2], '#2A2D31'), cat0[0], dt, (cat0[2] + cat1[2]) / 2));
    const rnd = canvasPlane(0.1 * L, 0.1 * L, (c, W, H) => { c.clearRect(0, 0, W, H); c.fillStyle = '#F2F2EE'; c.beginPath(); c.arc(W / 2, H / 2, W * 0.48, 0, TAU); c.fill();
      c.fillStyle = '#E58A2E'; c.beginPath(); c.arc(W / 2, H / 2, W * 0.4, 0, TAU); c.fill(); c.fillStyle = '#2F8C7A'; c.beginPath(); c.moveTo(W / 2, H * 0.24); c.lineTo(W * 0.73, H * 0.68); c.lineTo(W * 0.27, H * 0.68); c.closePath(); c.fill(); }, { res: 128, transparent: true });
    rnd.rotation.x = -PI / 2; rnd.position.set(-0.07 * L, dt + 0.001, -0.3 * L); g.add(rnd);
    // the island
    const isl = grp(); isl.position.set(0.125 * L, dt, -0.04 * L); g.add(isl);
    isl.add(at(box(0.06 * L, 0.075 * L, 0.2 * L, '#A2AAB2', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(0.05 * L, 0.04 * L, 0.11 * L, '#A2AAB2', { pivot: 'bottom', outline: 0.01 }), 0, 0.075 * L, -0.02 * L));
    isl.add(at(box(0.052 * L, 0.012 * L, 0.112 * L, '#1E2A33'), 0, 0.098 * L, -0.02 * L), at(box(0.062 * L, 0.01 * L, 0.18 * L, '#1E2A33'), 0, 0.058 * L, 0.0));
    isl.add(at(cyl(0.004 * L, 0.004 * L, 0.09 * L, '#6E767E', 5, { pivot: 'bottom' }), 0, 0.115 * L, -0.03 * L));
    const sideR = rnd.clone(); sideR.rotation.set(0, -PI / 2, 0); sideR.scale.setScalar(0.45); sideR.position.set(0.031 * L, 0.04 * L, 0.03 * L); sideR.rotation.y = PI / 2; isl.add(sideR);
    const radar = grp(at(box(0.05 * L, 0.012 * L, 0.006 * L, '#D9DDE1', { outline: 0.02 }), 0, 0, 0)); radar.position.set(0, 0.2 * L, -0.03 * L); isl.add(radar);
    // the hatch, aft on the left of the deck
    const hatchP = [-0.08 * L, dt, -0.2 * L], hl = grp(at(box(0.05 * L, 0.006 * L, 0.05 * L, '#6A7078', { outline: 0.02 }), 0, 0, 0.025 * L)); hl.position.set(hatchP[0], dt + 0.003 * L, hatchP[2] - 0.025 * L);
    g.add(at(box(0.05 * L, 0.002, 0.05 * L, '#141619'), hatchP[0], dt, hatchP[2]), hl);
    if (o.snow) { const rr = rng(9); for (let i = 0; i < 14; i++) g.add(at(box((0.04 + rr() * 0.08) * L, 0.006 * L, (0.04 + rr() * 0.1) * L, '#F6F8FA'), (rr() - 0.5) * 0.25 * L, dt + 0.002, (rr() - 0.5) * 0.85 * L, 0, rr(), 0));
      isl.add(at(box(0.064 * L, 0.01 * L, 0.205 * L, '#F6F8FA'), 0, 0.077 * L, 0), at(box(0.054 * L, 0.01 * L, 0.115 * L, '#F6F8FA'), 0, 0.117 * L, -0.02 * L)); }
    let wake = null, bowW = null;
    if (o.wake) { const wm = basic('#FFFFFF', { opacity: 0.8, side: THREE.DoubleSide });
      wake = new THREE.Mesh(new THREE.PlaneGeometry(B * 1.6, L * 2.2, 4, 20), wm); wake.rotation.x = -PI / 2; wake.position.set(0, 0.006 * L, -L * 1.55); g.add(noShadow(wake));
      bowW = grp(); for (const s of [-1, 1]) { const w = at(new THREE.Mesh(new THREE.ConeGeometry(0.06 * L, 0.32 * L, 6, 1, true), basic('#FFFFFF', { opacity: 0.85, side: THREE.DoubleSide })), s * 0.08 * L, 0.01 * L, 0.36 * L, PI / 2 + 0.1, 0, -s * 0.5); w.scale.set(1, 1, 0.35); bowW.add(noShadow(w)); } g.add(bowW); }
    g.userData.update = t => {
      radar.rotation.y = t * 3.2;
      const hv = o.hatch ? (() => { let v = 0; for (const [tt, vv] of o.hatch) if (t >= tt) v = vv; return v; })() : 0; hl.rotation.x = -1.9 * hv;
      if (wake) { const p = wake.geometry.attributes.position; for (let i = 0; i < p.count; i++) { const y = p.getY(i), k = (y + L * 1.1) / (L * 2.2); p.setX(i, Math.sign(p.getX(i)) * B * (0.35 + 0.9 * (1 - k)) + 0.02 * L * Math.sin(y * 9 / L + t * 6)); }
        p.needsUpdate = true; wake.material.opacity = 0.75; bowW.scale.setScalar(1 + 0.08 * Math.sin(t * 9)); }
    };
    g.userData.update(0); g.userData.deck = dt; g.userData.cat0 = cat0; g.userData.cat1 = cat1; g.userData.hatch = [hatchP[0], dt, hatchP[2]]; return g;
  },

  // Water spilling over an edge (pivot at the middle of the edge's top, the fall toward +Z then down to the floor o.h, 0.9 m, below): a rippling sheet
  // o.w (0.5) wide that curls over the lip and falls, white splashes where it lands, and a pool on the floor growing from o.r0 (0.3) to o.r (1.2 m) over
  // o.grow (1.6 s) from o.at (0); o.calm: a still pool (no sheet; the flood has stopped)
  waterSpill(o) {
    const Wd = o.w ?? 0.5, Ht = o.h ?? 0.9, g = grp(), wm = new THREE.MeshLambertMaterial({ color: '#7CC6E6', transparent: true, opacity: 0.72, side: THREE.DoubleSide, emissive: new THREE.Color('#2E6E8A'), emissiveIntensity: 0.4, depthWrite: false });
    let sheet = null, base = null;
    if (!o.calm) { const geo = new THREE.PlaneGeometry(Wd, 1, 6, 16); base = geo.attributes.position.array.slice(); sheet = new THREE.Mesh(geo, wm); g.add(noShadow(sheet)); }
    const pool = new THREE.Mesh(new THREE.CircleGeometry(1, 28), new THREE.MeshLambertMaterial({ color: '#8FD2EC', transparent: true, opacity: 0.6, emissive: new THREE.Color('#3C7E98'), emissiveIntensity: 0.35, depthWrite: false }));
    pool.rotation.x = -PI / 2; pool.position.set(0, -Ht + 0.004, 0.25); g.add(noShadow(pool));
    const spl = []; if (!o.calm) for (let i = 0; i < 6; i++) { const m = sphere(0.025, '#FFFFFF', 1, { unique: true, opacity: 0.9 }); m.castShadow = false; g.add(m); spl.push(m); }
    g.userData.update = t => {
      const u = Math.max(0, t - (o.at ?? 0));
      if (sheet) { const p = sheet.geometry.attributes.position;
        for (let i = 0; i < p.count; i++) { const x = base[i * 3], v = base[i * 3 + 1] + 0.5, a = Math.min(v * 4, 1) * PI / 2;
          const z = v < 0.25 ? 0.05 * Math.sin(a) : 0.05 + (v - 0.25) * 0.12, y = v < 0.25 ? -0.04 * (1 - Math.cos(a)) : -0.04 - (v - 0.25) / 0.75 * (Ht - 0.04);
          p.setXYZ(i, x * (1 + 0.15 * v) + 0.01 * Math.sin(v * 20 - t * 14 + x * 9), y, z + 0.008 * Math.sin(v * 31 - t * 18)); }
        p.needsUpdate = true; sheet.geometry.computeVertexNormals(); }
      const r = (o.r0 ?? 0.3) + ((o.r ?? 1.2) - (o.r0 ?? 0.3)) * smooth(u / (o.grow ?? 1.6)); pool.scale.set(r, r * 0.8, 1);
      spl.forEach((m, i) => { const f = (t * 2.2 + i / 6) % 1; m.position.set((i / 5 - 0.5) * Wd, -Ht + 0.03 + 0.14 * Math.sin(PI * f), 0.18 + 0.12 * f); m.scale.setScalar(0.6 + Math.sin(PI * f)); });
    };
    g.userData.update(0); return g;
  },

  // A wall shelf of plates (pivot at the middle of its back edge on the wall, front +Z): a wooden plank o.w (0.72) with a rail, o.n (5) plates standing
  // on edge (white with a blue rim) and two cups; o.burst (s): the plates leap off toward +Z, spinning, and fall under gravity to the floor o.floor
  // (1.45 m) below, where each lies broken in two
  plateShelf(o) {
    const Wd = o.w ?? 0.72, n = o.n ?? 5, fl = o.floor ?? 1.45, g = grp(), rr = rng(o.seed || 11);
    g.add(at(box(Wd, 0.03, 0.2, '#B98A5A', { outline: 0.01 }), 0, 0, 0.1), at(box(Wd, 0.02, 0.02, '#8A6040'), 0, 0.06, 0.18));
    for (const s of [-1, 1]) g.add(at(box(0.02, 0.1, 0.16, '#8A6040'), s * (Wd / 2 - 0.02), -0.06, 0.08));
    const plates = [];
    for (let i = 0; i < n; i++) {
      const p = grp(); for (const s of [-1, 1]) { const half = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 0.014, 14, 1, false, s > 0 ? 0 : PI, PI), mat('#FAFAF6')); half.castShadow = true;
        const rim = new THREE.Mesh(new THREE.TorusGeometry(0.105, 0.006, 4, 14, PI), mat('#2F5FA8')); rim.rotation.set(PI / 2, 0, s > 0 ? -PI / 2 : PI / 2); rim.position.y = 0.008;
        const hg = grp(half, rim); hg.userData.s = s; p.add(hg); }
      p.userData.p0 = [-Wd / 2 + 0.09 + i * (Wd - 0.18) / Math.max(1, n - 1), 0.125, 0.08]; p.userData.v = [(rr() - 0.5) * 1.4, 1.0 + rr() * 1.2, 1.4 + rr() * 1.1]; p.userData.sp = [(rr() - 0.5) * 18, (rr() - 0.5) * 8, (rr() - 0.5) * 18];
      g.add(p); plates.push(p);
    }
    for (const s of [-1, 1]) g.add(at(cyl(0.035, 0.03, 0.07, s > 0 ? '#E8452C' : '#F2C230', 8, { pivot: 'bottom', outline: 0.03 }), s * (Wd / 2 - 0.06), 0.015, 0.06));
    g.userData.update = t => {
      for (const p of plates) { const [x0, y0, z0] = p.userData.p0, [vx, vy, vz] = p.userData.v, u = o.burst == null ? -1 : t - o.burst;
        if (u <= 0) { p.position.set(x0, y0, z0); p.rotation.set(PI / 2 - 0.12, 0, 0); p.children.forEach(h => h.position.set(0, 0, 0)); continue; }
        const tl = (vy + Math.sqrt(vy * vy + 2 * 9.8 * (fl + y0))) / 9.8, uu = Math.min(u, tl);
        p.position.set(x0 + vx * uu, y0 + vy * uu - 4.9 * uu * uu, z0 + vz * uu);
        if (u < tl) { p.rotation.set(PI / 2 - 0.12 + p.userData.sp[0] * u, p.userData.sp[1] * u, p.userData.sp[2] * u); p.children.forEach(h => h.position.set(0, 0, 0)); }
        else { p.position.y = -fl + 0.008; p.rotation.set(0, p.userData.sp[1], 0); p.children.forEach(h => h.position.set(h.userData.s * 0.03 * Math.min(1, (u - tl) * 12), 0, 0)); }
      }
    };
    g.userData.update(0); return g;
  },

  // A riot shield (pivot at its middle, the face toward +Z): clear polycarbonate o.w (0.5) x o.h (0.85) in a black frame, a white band POLICE across the
  // top; o.bent (rad): its top third folded back (dented)
  riotShield(o) {
    const Wd = o.w ?? 0.5, Ht = o.h ?? 0.85, g = grp(), lowH = Ht * 0.66, topH = Ht - lowH;
    const pane = (h) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(Wd, h), new THREE.MeshLambertMaterial({ color: '#BFD8E6', transparent: true, opacity: 0.45, side: THREE.DoubleSide, depthWrite: false })); m.castShadow = false; return m; };
    const lo = grp(at(pane(lowH), 0, lowH / 2, 0)), hi = grp(at(pane(topH), 0, topH / 2, 0));
    const frame = (gg, h, top) => { gg.add(at(box(0.025, h, 0.025, '#16181C'), -Wd / 2, h / 2, 0), at(box(0.025, h, 0.025, '#16181C'), Wd / 2, h / 2, 0)); if (top) gg.add(at(box(Wd + 0.025, 0.025, 0.025, '#16181C'), 0, h, 0)); else gg.add(at(box(Wd + 0.025, 0.025, 0.025, '#16181C'), 0, 0, 0)); };
    frame(lo, lowH, false); frame(hi, topH, true);
    hi.add(at(canvasPlane(Wd * 0.92, topH * 0.5, (c, W, H) => { c.fillStyle = '#F4F4F0'; c.fillRect(0, 0, W, H); c.fillStyle = '#16181C'; c.font = `900 ${H * 0.62}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('POLICE', W / 2, H * 0.55); }, { res: 256 }), 0, topH * 0.5, 0.004));
    hi.position.y = lowH; hi.rotation.x = -(o.bent ?? 0); lo.add(hi); lo.position.y = -Ht / 2; g.add(lo);
    g.add(at(box(0.12, 0.03, 0.04, '#16181C'), 0, 0, -0.03));
    return g;
  },

  // A riot helmet to wear on a head (hang it on the head joint at the top of the head: origin there, the face toward +Z): a dark navy dome, a raised clear
  // visor, a chin strap; o.dent: the dome caved in on one side and tilted (a baton blow); o.s (1)
  riotHelmet(o) {
    const s = o.s ?? 1, g = grp(), h = grp(); g.add(h);
    const dome = new THREE.Mesh(new THREE.SphereGeometry(0.16, 14, 8, 0, TAU, 0, PI / 2), mat('#1F2838')); dome.scale.set(1.0, 0.95, 1.12); dome.castShadow = true; addOutline(dome, 0.03); h.add(dome);
    h.add(at(box(0.33, 0.03, 0.36, '#1F2838', { outline: 0.006 }), 0, 0.01, 0));
    const vis = new THREE.Mesh(new THREE.CylinderGeometry(0.175, 0.175, 0.13, 14, 1, true, -PI / 2.6, PI / 1.3), new THREE.MeshLambertMaterial({ color: '#CFE3EE', transparent: true, opacity: 0.5, side: THREE.DoubleSide, depthWrite: false }));
    vis.position.set(0, 0.11, 0.02); vis.rotation.x = -0.9; h.add(vis);
    if (o.dent) { const d = at(sphere(0.07, '#151B26', 1), 0.07, 0.12, 0.02); d.scale.set(0.6, 0.35, 1.0); h.add(d); dome.scale.set(1.0, 0.82, 1.12); h.rotation.z = 0.22; h.rotation.x = 0.08;
      for (let i = 0; i < 3; i++) h.add(at(box(0.004, 0.06, 0.004, '#0A0C10'), 0.08 + i * 0.012, 0.12 - i * 0.01, 0.06 + i * 0.01, 0, 0, 0.6 - i * 0.4)); }
    g.scale.setScalar(s); return g;
  },

  // An army helmet to wear on a head (hang it on the head joint at the top of the head): a rounded olive steel helmet with a rim and a strap; o.snow: a
  // cap of snow on it; o.s (1)
  armyHelmet(o) {
    const s = o.s ?? 1, g = grp();
    const dome = new THREE.Mesh(new THREE.SphereGeometry(0.155, 14, 8, 0, TAU, 0, PI / 2), mat('#5C6B3C')); dome.scale.set(1.05, 0.9, 1.12); dome.castShadow = true; addOutline(dome, 0.03); g.add(dome);
    g.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.17, 0.018, 5, 18), mat('#4E5C32')), 0, 0.005, 0, PI / 2, 0, 0));
    if (o.snow) { const sn = new THREE.Mesh(new THREE.SphereGeometry(0.15, 12, 6, 0, TAU, 0, PI / 2), mat('#F7F9FB')); sn.scale.set(0.95, 0.5, 1.0); sn.position.y = 0.1; g.add(sn); }
    g.scale.setScalar(s); return g;
  },

  // The air strike request (pivot at its middle, the face toward +Z): an A5 sheet with a big black plane pictogram, a dotted line, and a red stamp
  // URGENT that slams on at o.stamp (s) (it pops in, tilted); o.w (0.15)
  strikeForm(o) {
    const Wd = o.w ?? 0.15, Ht = Wd * 1.41, g = grp();
    g.add(at(box(Wd, Ht, 0.002, '#FBFAF4', { outline: 0.02 }), 0, 0, 0));
    const face = canvasPlane(Wd * 0.94, Ht * 0.94, (c, W, H) => { c.fillStyle = '#FBFAF4'; c.fillRect(0, 0, W, H); c.fillStyle = '#1C1E22';
      c.fillRect(W * 0.1, H * 0.06, W * 0.8, H * 0.025); c.fillRect(W * 0.1, H * 0.11, W * 0.55, H * 0.02);
      c.save(); c.translate(W / 2, H * 0.42); c.rotate(-0.5); c.beginPath(); c.moveTo(0, -H * 0.2); c.lineTo(W * 0.05, -H * 0.12); c.lineTo(W * 0.05, -H * 0.03); c.lineTo(W * 0.34, H * 0.05); c.lineTo(W * 0.34, H * 0.1); c.lineTo(W * 0.05, H * 0.06);
      c.lineTo(W * 0.04, H * 0.15); c.lineTo(W * 0.13, H * 0.2); c.lineTo(W * 0.13, H * 0.23); c.lineTo(0, H * 0.2); c.lineTo(-W * 0.13, H * 0.23); c.lineTo(-W * 0.13, H * 0.2); c.lineTo(-W * 0.04, H * 0.15); c.lineTo(-W * 0.05, H * 0.06);
      c.lineTo(-W * 0.34, H * 0.1); c.lineTo(-W * 0.34, H * 0.05); c.lineTo(-W * 0.05, -H * 0.03); c.lineTo(-W * 0.05, -H * 0.12); c.closePath(); c.fill(); c.restore();
      c.setLineDash([W * 0.03, W * 0.025]); c.lineWidth = H * 0.006; c.strokeStyle = '#1C1E22'; for (const y of [0.74, 0.82, 0.9]) { c.beginPath(); c.moveTo(W * 0.1, H * y); c.lineTo(W * 0.9, H * y); c.stroke(); } }, { res: 256 });
    face.position.z = 0.0015; g.add(face);
    const st = canvasPlane(Wd * 0.8, Wd * 0.3, (c, W, H) => { c.clearRect(0, 0, W, H); c.strokeStyle = '#D42A22'; c.lineWidth = H * 0.1; c.strokeRect(H * 0.08, H * 0.08, W - H * 0.16, H - H * 0.16);
      c.fillStyle = '#D42A22'; c.font = `900 ${H * 0.58}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('URGENT', W / 2, H * 0.55); }, { res: 256, transparent: true });
    const sg = grp(st); sg.position.set(0, -Ht * 0.12, 0.003); sg.rotation.z = 0.22; g.add(sg);
    g.userData.update = t => { const k = popK(t, o.stamp); sg.scale.setScalar(Math.max(0.001, k)); sg.visible = k > 0.001; };
    g.userData.update(0); return g;
  },

  // A green four-point glint (pivot at its centre, it always faces the camera): at o.at it flashes up to o.size (1.2) and fades over o.dur (0.45 s)
  lensGlint(o) {
    const g = grp(), sz = o.size ?? 1.2, tex = canvasPlane(1, 1, (c, W, H) => { c.clearRect(0, 0, W, H); const gr = c.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, W / 2);
      gr.addColorStop(0, 'rgba(230,255,230,1)'); gr.addColorStop(0.15, 'rgba(90,255,120,0.95)'); gr.addColorStop(0.5, 'rgba(40,220,90,0.25)'); gr.addColorStop(1, 'rgba(40,220,90,0)'); c.fillStyle = gr; c.fillRect(0, 0, W, H);
      c.fillStyle = 'rgba(200,255,210,0.95)'; for (const r of [0, PI / 2]) { c.save(); c.translate(W / 2, H / 2); c.rotate(r); c.beginPath(); c.moveTo(-W * 0.5, 0); c.lineTo(0, -H * 0.035); c.lineTo(W * 0.5, 0); c.lineTo(0, H * 0.035); c.closePath(); c.fill(); c.restore(); } }, { res: 256, transparent: true }).material.map;
    const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, fog: false })); g.add(sp);
    g.userData.update = t => { const u = t - (o.at ?? 0), d = o.dur ?? 0.45; const k = u < 0 ? 0 : u < 0.08 ? u / 0.08 : Math.max(0, 1 - (u - 0.08) / d);
      sp.visible = k > 0.01; sp.scale.setScalar(sz * (0.4 + 0.8 * k)); sp.material.opacity = k; sp.material.rotation = u * 1.5; };
    g.userData.update(0); return g;
  },

  // A red map pin (pivot at its point): a round red head on a steel needle, o.s (1: 0.12 m tall); it drops from o.drop (0.8 m) above and lands at o.at
  // with a little bounce, and a red ring ripples out round its point; before o.at - fall time it is not there
  mapPin(o) {
    const s = o.s ?? 1, g = grp(), pin = grp(); g.add(pin);
    pin.add(at(cyl(0.004 * s, 0.001 * s, 0.07 * s, '#C9CCD1', 6, { pivot: 'bottom' }), 0, 0, 0));
    const head = at(sphere(0.03 * s, '#E1261C', 2), 0, 0.085 * s, 0); addOutline(head, 0.08); pin.add(head, at(sphere(0.008 * s, '#FFFFFF', 0, { emissive: '#FFFFFF' }), -0.012 * s, 0.098 * s, 0.022 * s));
    const ring = new THREE.Mesh(new THREE.RingGeometry(0.8, 1.0, 32), basic('#E1261C', { opacity: 0.8, side: THREE.DoubleSide })); ring.rotation.x = -PI / 2; ring.position.y = 0.003; g.add(noShadow(ring));
    const drop = o.drop ?? 0.8, tf = Math.sqrt(2 * drop / 9.8);
    g.userData.update = t => { const u = t - (o.at ?? 0);
      pin.visible = u > -tf; pin.position.y = u < 0 ? drop * (u / -tf) ** 2 : 0.02 * s * Math.max(0, Math.sin(u * 20)) * Math.exp(-u * 8);
      pin.scale.set(1, u >= 0 && u < 0.06 ? 0.85 : 1, 1);
      const v = u < 0 ? -1 : u / 0.6; ring.visible = v >= 0 && v < 1; const R = 0.03 * s + 0.25 * s * v; ring.scale.setScalar(R); ring.material.opacity = 0.8 * (1 - v); };
    g.userData.update(0); return g;
  },

  // A satellite view's reticle on the ground (pivot at its centre, flat on XZ): four green corner brackets and a crosshair o.r (0.35 m), that close in
  // from twice their size at o.at and pulse
  satReticle(o) {
    const R = o.r ?? 0.35, g = grp(), m = basic('#3CFF6A', { opacity: 0.9 }), parts = grp(); g.add(parts);
    for (const [sx, sz] of [[1, 1], [-1, 1], [1, -1], [-1, -1]]) parts.add(at(box(R * 0.35, 0.004, R * 0.04, '#3CFF6A', { material: m }), sx * R * 0.82, 0, sz * R), at(box(R * 0.04, 0.004, R * 0.35, '#3CFF6A', { material: m }), sx * R, 0, sz * R * 0.82));
    parts.add(at(box(R * 0.5, 0.004, R * 0.025, '#3CFF6A', { material: m }), 0, 0, 0), at(box(R * 0.025, 0.004, R * 0.5, '#3CFF6A', { material: m }), 0, 0, 0));
    noShadow(parts);
    g.userData.update = t => { const u = t - (o.at ?? 0); parts.visible = u >= 0; const k = 1 + Math.max(0, 1 - u / 0.25); parts.scale.set(k, 1, k); m.opacity = 0.75 + 0.2 * Math.sin(t * 14); };
    g.userData.update(0); return g;
  },

  // A wall hit by a missile (pivot on the wall surface, the wall's face toward +Z): at o.at a flash, a black scorch and cracks that run out over 0.15 s,
  // chips that fly; o.r (0.35 m)
  wallImpact(o) {
    const R = o.r ?? 0.35, g = grp(), rr = rng(o.seed || 3);
    const crack = canvasPlane(R * 2.4, R * 2.4, (c, W, H) => { c.clearRect(0, 0, W, H); const gr = c.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, W * 0.28); gr.addColorStop(0, 'rgba(20,18,16,0.95)'); gr.addColorStop(0.6, 'rgba(40,34,30,0.7)'); gr.addColorStop(1, 'rgba(60,50,40,0)');
      c.fillStyle = gr; c.fillRect(0, 0, W, H); c.strokeStyle = 'rgba(24,20,18,0.95)'; c.lineCap = 'round';
      for (let i = 0; i < 9; i++) { let x = W / 2, y = H / 2, a = i / 9 * TAU + rr() * 0.5; c.lineWidth = W * 0.018; c.beginPath(); c.moveTo(x, y);
        for (let j = 0; j < 5; j++) { a += (rr() - 0.5) * 0.9; const d = W * (0.05 + rr() * 0.06); x += Math.cos(a) * d; y += Math.sin(a) * d; c.lineTo(x, y); c.lineWidth *= 0.8; } c.stroke(); } }, { res: 256, transparent: true });
    crack.position.z = 0.004; g.add(crack);
    const fl = glowSprite('#FFD27A', R * 3, 1); fl.position.z = 0.1; g.add(fl);
    const chips = []; for (let i = 0; i < 10; i++) { const m = at(box(0.03 + rr() * 0.03, 0.02, 0.02, ['#E9D6BC', '#CDB89A', '#F6D7AE'][i % 3]), 0, 0, 0); m.userData.v = [(rr() - 0.5) * 2.4, (rr() - 0.2) * 2.2, 0.8 + rr() * 1.6]; g.add(m); chips.push(m); }
    g.userData.update = t => { const u = t - (o.at ?? 0);
      crack.visible = u >= 0; crack.scale.setScalar(Math.max(0.001, smooth(u / 0.15)));
      fl.visible = u >= 0 && u < 0.25; fl.material.opacity = Math.max(0, 1 - u / 0.25);
      chips.forEach(m => { m.visible = u >= 0 && u < 0.9; const [vx, vy, vz] = m.userData.v; m.position.set(vx * u, vy * u - 4.9 * u * u, vz * u); m.rotation.set(u * 9, u * 7, 0); }); };
    g.userData.update(0); return g;
  },

  // The heap of rubble where his building stood (pivot at the foot of the heap's middle): a mound o.r (3.2 m) wide and o.h (2.2 m) high of concrete
  // and brick chunks, broken slabs, a few rods of rebar, the bare kitchen floor (peach and cream tiles) flat on top; o.wall [t0, ...]: the last piece of
  // wall standing at its back-left, it topples over at t0; o.dust: dust rolling off its slopes (puffs that spread and fade, for ever); o.snow: snow on it.
  // userData.top: the middle of the floor on top
  rubbleHeap(o) {
    const R = o.r ?? 3.2, Hh = o.h ?? 2.2, g = grp(), rr = rng(o.seed || 21), geo = new THREE.DodecahedronGeometry(1, 0), cols = ['#C9C0AE', '#B5AC9A', '#D8CFBD', '#A79F8F', '#B9664E', '#D9B48F'];
    const core = new THREE.Mesh(new THREE.SphereGeometry(1, 14, 8, 0, TAU, 0, PI / 2), mat('#B8AF9E')); core.scale.set(R, Hh, R * 0.9); core.castShadow = core.receiveShadow = true; g.add(core);
    for (let i = 0; i < 120; i++) { const a = rr() * TAU, d = Math.sqrt(rr()) * R * 0.98, y = Hh * Math.sqrt(Math.max(0, 1 - (d / R) ** 2)), s = 0.12 + rr() * 0.35;
      const m = new THREE.Mesh(i % 7 === 0 ? new THREE.BoxGeometry(1, 0.25, 0.6) : geo, mat(cols[i % cols.length])); m.position.set(Math.cos(a) * d, y - s * 0.2, Math.sin(a) * d * 0.9); m.scale.setScalar(s * (i % 7 === 0 ? 2.2 : 1)); m.rotation.set(rr() * 3, rr() * 3, rr() * 3); m.castShadow = m.receiveShadow = true; g.add(m); }
    for (let i = 0; i < 8; i++) { const a = rr() * TAU, d = R * (0.3 + rr() * 0.5), y = Hh * Math.sqrt(1 - (d / R) ** 2); g.add(at(cyl(0.012, 0.012, 0.6 + rr() * 0.5, '#6E4A36', 4, { pivot: 'bottom' }), Math.cos(a) * d, y - 0.1, Math.sin(a) * d * 0.9, rr() - 0.5, 0, rr() - 0.5)); }
    const top = Hh - 0.02, fw = 1.9, tiles = grp();
    for (let i = 0; i < 6; i++) for (let j = 0; j < 5; j++) tiles.add(at(box(0.3, 0.03, 0.3, (i + j) % 2 ? '#F4E6CC' : '#E9B88E'), -fw / 2 + 0.15 + i * 0.32, 0, -0.75 + 0.15 + j * 0.32, (rr() - 0.5) * 0.04, 0, (rr() - 0.5) * 0.04));
    tiles.position.y = top; g.add(tiles);
    let wall = null; if (o.wall) { wall = grp(at(box(1.2, 1.7, 0.18, '#F6D7AE', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(1.2, 0.95, 0.02, '#9FD8C8', { pivot: 'bottom' }), 0, 0, 0.1), at(box(0.5, 0.5, 0.2, '#B5AC9A'), 0.45, 1.7, 0, 0.3, 0, 0.6));
      wall.position.set(-0.75, top, -0.7); g.add(wall); }
    if (o.snow) { for (let i = 0; i < 40; i++) { const a = rr() * TAU, d = Math.sqrt(rr()) * R * 0.95, y = Hh * Math.sqrt(Math.max(0, 1 - (d / R) ** 2)); const m = new THREE.Mesh(geo, mat('#F6F8FA')); m.position.set(Math.cos(a) * d, y, Math.sin(a) * d * 0.9); m.scale.set(0.35, 0.08, 0.35); g.add(m); } }
    const puffs = []; if (o.dust) for (let i = 0; i < 10; i++) { const m = sphere(0.4, '#D8CFBA', 1, { unique: true, opacity: 0.85 }); m.castShadow = false; m.userData.a = i / 10 * TAU + rr() * 0.3; m.userData.ph = rr(); g.add(m); puffs.push(m); }
    g.userData.update = t => {
      if (wall) { const u = t - o.wall[0]; wall.rotation.x = u <= 0 ? 0 : Math.min(PI / 2, 4.5 * u * u + 0.6 * u); }
      puffs.forEach(m => { const f = (t * 0.55 + m.userData.ph) % 1, a = m.userData.a, d = R * (0.55 + 0.6 * f); m.position.set(Math.cos(a) * d, Hh * 0.55 * (1 - f) + 0.2, Math.sin(a) * d * 0.9); m.scale.setScalar(0.6 + 1.6 * f); m.material.opacity = 0.85 * (1 - f); });
    };
    g.userData.update(0); g.userData.top = [0, top + 0.015, 0]; return g;
  },

  // The ruins of the kitchen at ground level (pivot at the middle of the floor; front +Z): the peach and cream tiles o.w (5.2) x o.d (3.6) with a few
  // missing, the stumps of two walls (back and left) with jagged tops and the kitchen's peach paint and mint band inside, heaps of concrete and brick
  // round the edges, a fallen beam; o.smoke: thin grey wisps rising from the heaps (for ever); o.snow: snow on everything, white patches on the tiles
  ruinFloor(o) {
    const Wd = o.w ?? 5.2, Dp = o.d ?? 3.6, g = grp(), rr = rng(o.seed || 31), geo = new THREE.DodecahedronGeometry(1, 0), cols = ['#C9C0AE', '#B5AC9A', '#D8CFBD', '#A79F8F', '#B9664E'];
    const tl = grp(); for (let i = 0; i < Math.round(Wd / 0.4); i++) for (let j = 0; j < Math.round(Dp / 0.4); j++) { if (rr() < 0.05) continue;
      tl.add(at(box(0.39, 0.02, 0.39, (i + j) % 2 ? '#F4E6CC' : '#E9B88E'), -Wd / 2 + 0.2 + i * 0.4, 0.01, -Dp / 2 + 0.2 + j * 0.4)); } g.add(tl);
    const stump = (len, x, z, ry) => { const s = grp(); const n = Math.round(len / 0.3); for (let i = 0; i < n; i++) { const h = 0.35 + rr() * 0.9 * (1 - Math.abs(i / n - 0.4));
        s.add(at(box(0.3, h, 0.2, '#E8DCC8', { pivot: 'bottom' }), -len / 2 + 0.15 + i * 0.3, 0, 0), at(box(0.3, Math.min(h, 0.95), 0.01, '#9FD8C8', { pivot: 'bottom' }), -len / 2 + 0.15 + i * 0.3, 0, 0.105), ...(h > 0.96 ? [at(box(0.3, h - 0.95, 0.01, '#F6D7AE', { pivot: 'bottom' }), -len / 2 + 0.15 + i * 0.3, 0.95, 0.105)] : [])); }
      s.position.set(x, 0, z); s.rotation.y = ry; g.add(s); };
    stump(Wd * 0.9, 0, -Dp / 2 - 0.15, 0); stump(Dp * 0.8, -Wd / 2 - 0.15, -0.2, PI / 2);
    for (let i = 0; i < 70; i++) { const side = i % 3, s = 0.12 + rr() * 0.32; let x, z;
      if (side === 0) { x = -Wd / 2 - 0.4 + rr() * Wd * 1.1; z = -Dp / 2 - 0.5 - rr() * 1.2; } else if (side === 1) { x = -Wd / 2 - 0.5 - rr() * 1.2; z = -Dp / 2 + rr() * Dp; } else { x = Wd / 2 + 0.3 + rr() * 1.4; z = -Dp / 2 + rr() * Dp * 1.1; }
      const m = new THREE.Mesh(i % 6 === 0 ? new THREE.BoxGeometry(1, 0.25, 0.6) : geo, mat(cols[i % cols.length])); m.position.set(x, s * 0.5, z); m.scale.setScalar(s * (i % 6 === 0 ? 2 : 1)); m.rotation.set(rr() * 3, rr() * 3, rr() * 3); m.castShadow = m.receiveShadow = true; g.add(m); }
    g.add(at(box(2.4, 0.16, 0.2, '#8A6A4E', { outline: 0.01 }), Wd / 2 + 0.6, 0.3, -Dp / 2 + 0.4, 0.1, 0.5, 0.35));
    for (let i = 0; i < 12; i++) g.add(at(box(0.08 + rr() * 0.1, 0.05, 0.06 + rr() * 0.1, cols[i % cols.length]), (rr() - 0.5) * Wd * 0.9, 0.04, (rr() - 0.5) * Dp * 0.9, 0, rr() * 3, 0));
    if (o.snow) { for (let i = 0; i < 26; i++) g.add(at(box(0.3 + rr() * 0.8, 0.012, 0.3 + rr() * 0.7, '#F6F8FA'), (rr() - 0.5) * Wd, 0.026, (rr() - 0.5) * Dp, 0, rr() * 3, 0));
      for (let i = 0; i < 40; i++) { const m = new THREE.Mesh(geo, mat('#F6F8FA')); const side = i % 3; m.position.set(side === 2 ? Wd / 2 + 0.4 + rr() * 1.2 : -Wd / 2 - 0.2 + rr() * Wd, side === 0 ? 0.35 : 0.25, side === 0 ? -Dp / 2 - 0.6 - rr() : -Dp / 2 + rr() * Dp); if (side === 1) m.position.x = -Wd / 2 - 0.5 - rr(); m.scale.set(0.35, 0.1, 0.35); g.add(m); } }
    const wisps = []; if (o.smoke) for (let i = 0; i < 9; i++) { const m = sphere(0.18, '#9A958E', 1, { unique: true, opacity: 0.6 }); m.castShadow = false; m.userData.x = [-Wd / 2 - 0.6, Wd / 2 + 0.8, 0.6][i % 3]; m.userData.z = [-0.3, 0.2, -Dp / 2 - 0.8][i % 3]; m.userData.ph = i / 9; g.add(m); wisps.push(m); }
    g.userData.update = t => { wisps.forEach(m => { const f = (t * 0.35 + m.userData.ph * 3) % 1; m.position.set(m.userData.x + 0.3 * Math.sin(t + m.userData.ph * 9), 0.3 + 2.4 * f, m.userData.z); m.scale.setScalar(0.6 + 2.0 * f); m.material.opacity = 0.55 * (1 - f); }); };
    g.userData.update(0); return g;
  },

  // A building that pancakes (pivot at its foot): it builds the prop o.of (townHall) with o.opts, and at o.at (s) squashes it to o.flat (0.12) of its
  // height over o.dur (0.45 s) with a lurch, while puffs of dust burst out round its foot; o.pole: a freestanding flagpole in front of it (o.poleAt [x, z],
  // o.poleH 5 m) whose flag slides down and flops onto the rubble at its foot at o.at + 0.25 — the pole stays standing
  collapse(o) {
    const g = grp(), inner = buildProp(o.of || 'townHall', o.opts || {}), pv = grp(inner); g.add(pv);
    const W = (o.opts && o.opts.w) || 6, rr = rng(o.seed || 7), puffs = [];
    const cols = ['#C9C0AE', '#B5AC9A', '#D8CFBD', '#EDE4D0'], deb = grp(); g.add(deb);
    for (let i = 0; i < 40; i++) { const m = new THREE.Mesh(new THREE.DodecahedronGeometry(1, 0), mat(cols[i % 4])); m.position.set((rr() - 0.5) * W * 1.1, 0.2, (rr() - 0.5) * 4.0 + 0.6); m.scale.setScalar(0.2 + rr() * 0.5); m.rotation.set(rr() * 3, rr() * 3, 0); deb.add(m); }
    for (let i = 0; i < 12; i++) { const m = sphere(1, '#DDD3BF', 1, { unique: true, opacity: 0.9 }); m.castShadow = false; m.userData.a = i / 12 * TAU; g.add(m); puffs.push(m); }
    let pole = null, flagG = null;
    if (o.pole) { const PH = o.poleH ?? 5, [px, pz] = o.poleAt || [-W * 0.6, 3.0]; pole = grp(at(cyl(0.05, 0.06, PH, '#E8E8E4', 8, { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(sphere(0.09, '#D9B04A', 1), 0, PH, 0)); pole.position.set(px, 0, pz); g.add(pole);
      flagG = grp(); ['#2F62B5', '#F4F4F0', '#E0413A'].forEach((c, i) => flagG.add(at(box(0.4, 0.8, 0.02, c, { outline: 0.01 }), 0.25 + i * 0.4, -0.4, 0))); pole.add(flagG); flagG.userData.PH = PH; }
    g.userData.update = t => { const u = t - (o.at ?? 0), d = o.dur ?? 0.45, f = o.flat ?? 0.12;
      const k = u <= 0 ? 0 : Math.min(1, (u / d) ** 2); pv.scale.set(1 + 0.06 * k, 1 - (1 - f) * k, 1 + 0.06 * k); pv.rotation.z = u > 0 && u < d * 1.6 ? 0.05 * Math.sin(u * 14) * (1 - k * 0.5) : 0;
      deb.visible = u > d * 0.6;
      puffs.forEach((m, i) => { const v = u < 0 ? -1 : u / 1.4; m.visible = v >= 0 && v < 1; const a = m.userData.a, r = W * (0.4 + 0.5 * smooth(v * 1.5)); m.position.set(Math.cos(a) * r, 0.6 + 1.2 * v + 0.3 * (i % 3), Math.sin(a) * r * 0.6 + 0.8); m.scale.setScalar(0.6 + 1.8 * smooth(v * 2)); m.material.opacity = 0.9 * (1 - v); });
      if (flagG) { const PH = flagG.userData.PH, uf = u - 0.25; if (uf <= 0) { flagG.position.y = PH - 0.05; flagG.rotation.set(0, 0, 0); flagG.children.forEach((c, i) => { c.rotation.y = 0.2 * Math.sin(t * 5 + i); }); }
        else { const fall = Math.min(1, (uf / 0.55) ** 2); flagG.position.y = (PH - 0.05) * (1 - fall) + 0.45 * fall; flagG.rotation.z = -1.3 * fall; flagG.children.forEach(c => { c.rotation.y = 0.2 * (1 - fall); }); } }
    };
    g.userData.update(0); return g;
  },

  // A general's chestful of medals (hang it on the torso, front +Z: origin at the middle of the chest): o.rows (6) rows of ribbon bars in every colour
  // from the collar to the belt, o.n (5) gold, silver and bronze medals hanging under them that swing; o.w (0.3)
  medalRack(o) {
    const Wd = o.w ?? 0.3, rows = o.rows ?? 6, n = o.n ?? 5, g = grp(), rr = rng(o.seed || 13), C = ['#C8222E', '#2F62B5', '#F4F4F0', '#2F8C5A', '#F2C230', '#6A3FA0', '#E58A2E', '#1C1E22'];
    for (let r = 0; r < rows; r++) for (let i = 0; i < 6; i++) g.add(at(box(Wd / 6 - 0.004, 0.022, 0.012, C[Math.floor(rr() * C.length)]), -Wd / 2 + Wd / 12 + i * Wd / 6, 0.16 - r * 0.028, 0));
    const meds = [];
    for (let i = 0; i < n; i++) { const m = grp(), c = ['#E6B84A', '#C9CCD1', '#B87333'][i % 3];
      m.add(at(box(0.03, 0.06, 0.006, C[(i * 3) % C.length]), 0, -0.03, 0)); const disc = at(cyl(0.022, 0.022, 0.006, c, 12, { emissive: i % 3 === 0 ? '#5A3E0A' : null }), 0, -0.075, 0.003, PI / 2, 0, 0); addOutline(disc, 0.1); m.add(disc);
      m.position.set(-Wd / 2 + Wd / (2 * n) + i * Wd / n, 0.16 - rows * 0.028 - 0.005, 0.01); g.add(m); meds.push(m); }
    g.userData.update = t => { meds.forEach((m, i) => { m.rotation.x = 0.12 * Math.sin(t * 4.5 + i * 1.3); m.rotation.z = 0.08 * Math.sin(t * 3.7 + i); }); };
    g.userData.update(0); return g;
  },

  // The ceasefire treaty (pivot at its middle, lying flat face up): a blank cream sheet with a ruled border, a red wax seal and a ribbon, no text;
  // o.w (0.3)
  treatySheet(o) {
    const Wd = o.w ?? 0.3, g = grp();
    const sh = canvasPlane(Wd, Wd * 1.35, (c, W, H) => { c.fillStyle = '#F7F1DF'; c.fillRect(0, 0, W, H); c.strokeStyle = '#B79A5E'; c.lineWidth = W * 0.012; c.strokeRect(W * 0.06, H * 0.05, W * 0.88, H * 0.9); c.strokeRect(W * 0.08, H * 0.065, W * 0.84, H * 0.87); }, { res: 256 });
    sh.rotation.x = -PI / 2; sh.position.y = 0.002; g.add(sh);
    const seal = at(cyl(0.028, 0.03, 0.008, '#B3241C', 10, { outline: 0.06 }), Wd * 0.3, 0.006, Wd * 0.48); g.add(seal);
    for (const s of [-1, 1]) g.add(at(box(0.016, 0.002, 0.07, '#2F62B5'), Wd * 0.3 + s * 0.012, 0.004, Wd * 0.48 + 0.05, 0, s * 0.25, 0));
    return g;
  },
};
