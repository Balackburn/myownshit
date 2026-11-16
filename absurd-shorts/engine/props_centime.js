// « Le centime » (story 77): this man paid his taxes one cent too much; the state refunds it with a minister, the republican guard, a brass band and
// helicopters; the cent arrives on a velvet cushion and goes into his piggy bank; the next day, a bill of two million for travel expenses.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere } from './style.js';
import { grp, at, rod, canvasPlane, glassMat, buildProp } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const L = c => new THREE.MeshLambertMaterial({ color: c });
// (pass 3 of 77) text that shrinks until it fits maxW (a canvas 2D context, its font set here)
const fitText = (c, text, maxW, fs, weight = 900) => { c.font = `${weight} ${fs}px Arial`; while (c.measureText(text).width > maxW && fs > 6) { fs -= 1; c.font = `${weight} ${fs}px Arial`; } return fs; };
const lenAt = (keys, t) => { if (typeof keys === 'number') return keys; let v = keys[0][1]; for (let i = 0; i < keys.length; i++) { const [t0, v0] = keys[i]; if (t < t0) break; v = v0; const nx = keys[i + 1]; if (nx && t < nx[0]) { v = v0 + (nx[1] - v0) * clamp01((t - t0) / Math.max(1e-4, nx[0] - t0)); break; } } return v; };

export const CENTIME_PROPS = {
  // A pink piggy bank (pivot at the floor middle, snout +Z): a round body, a snout with two nostrils, ears, four stubby legs, a curly tail and a coin
  // slot on its back; o.dropAt [t...]: a gold coin appears over the slot, drops in (0.22 s) and the pig jiggles; o.s scale (1: 0.3 m long)
  piggyBank(o) {
    const s = o.s ?? 1, g = grp(), body = grp(), pk = o.color || '#F2A2B8', dk = '#D97F98';
    g.add(body);
    const b = new THREE.Mesh(new THREE.SphereGeometry(0.12, 14, 10), L(pk)); b.scale.set(1.0, 0.92, 1.25); b.position.y = 0.13; body.add(b);
    const sn = at(cyl(0.048, 0.052, 0.05, dk, 12, { outline: 0.003 }), 0, 0.13, 0.155); sn.rotation.x = PI / 2; body.add(sn);
    for (const sx of [-1, 1]) {
      body.add(at(sphere(0.01, '#5A2E3A', 0), sx * 0.018, 0.13, 0.182));   // a nostril
      body.add(at(sphere(0.014, '#1C1D22', 0), sx * 0.05, 0.19, 0.115));   // an eye
      const ear = at(box(0.045, 0.05, 0.012, dk, { outline: 0.003 }), sx * 0.065, 0.235, 0.06); ear.rotation.set(-0.3, 0, sx * -0.4); body.add(ear);
      for (const sz of [-1, 1]) body.add(at(cyl(0.025, 0.028, 0.06, dk, 8, { pivot: 'bottom' }), sx * 0.06, 0, sz * 0.08));   // a leg
    }
    body.add(at(box(0.05, 0.006, 0.012, '#3A2A30'), 0, 0.243, -0.01));   // the slot
    const tail = new THREE.Mesh(new THREE.TorusGeometry(0.018, 0.006, 6, 12, PI * 1.6), L(dk)); tail.position.set(0, 0.16, -0.155); tail.rotation.y = PI / 2; body.add(tail);
    // (pass 3 of 77) o.coin { r, color, rim, pre, hover }: a darker copper coin with a light rim (gold between his fingers, it merged with the hand), visible
    // `pre` seconds before the drop, hanging `hover` above the floor of the pig (clear of the fingers)
    const CO = o.coin || {}, cr = CO.r ?? 0.022, hov = CO.hover ?? 0.33, pre = CO.pre ?? 0.12;
    const coin = grp(); const cd = cyl(cr, cr, 0.005, CO.color || '#E2B53C', 16, { outline: 0.002 }); cd.rotation.x = PI / 2; coin.add(cd);
    if (CO.rim) for (const z of [-0.003, 0.003]) { const rg = new THREE.Mesh(new THREE.TorusGeometry(cr * 0.86, cr * 0.09, 5, 20), L(CO.rim)); rg.position.z = z; coin.add(rg); }
    coin.position.set(0, hov, -0.01); coin.rotation.y = CO.ry ?? PI / 2; coin.visible = false; g.add(coin);
    g.scale.setScalar(s);
    const drops = o.dropAt || [];
    g.userData.update = t => {
      coin.visible = false; let jig = 0;
      for (const d of drops) { const u = t - d;
        if (u >= -pre && u < 0.22) { coin.visible = true; const f = clamp01(u / 0.22); coin.position.y = hov - (hov - 0.24) * f * f; coin.rotation.z = u > 0 ? u * 9 : 0.12 * Math.sin(u * 16); }
        if (u >= 0.2 && u < 0.7) jig = Math.max(jig, Math.exp(-(u - 0.2) * 8) * Math.sin((u - 0.2) * 34)); }
      const J = o.jig ?? 1;   // (review 1 of 77) o.jig: how hard it jiggles (1: a jiggle nobody saw at phone size; 3: a squash and stretch)
      body.scale.set(1 + 0.08 * J * jig, 1 - 0.1 * J * jig, 1 + 0.08 * J * jig); body.rotation.z = 0.06 * J * jig;
    };
    g.userData.update(-1); return g;
  },

  // A red velvet cushion carried on the flat of two hands (pivot at its bottom middle): o.w (0.36) square, plumped, gold piping round its edge and a
  // gold tassel at each corner
  velvetCushion(o) {
    const w = o.w ?? 0.36, g = grp(), red = o.color || '#A8182A', gold = '#E2B53C';
    g.add(at(box(w, 0.07, w, red, { pivot: 'bottom', outline: 0.004 }), 0, 0, 0), at(box(w * 0.86, 0.03, w * 0.86, '#B82236'), 0, 0.075, 0));   // plumped top
    for (const [x, z, l, ry] of [[0, w / 2, w, 0], [0, -w / 2, w, 0], [w / 2, 0, w, PI / 2], [-w / 2, 0, w, PI / 2]]) { const p = at(box(l, 0.012, 0.012, gold), x, 0.07, z); p.rotation.y = ry; g.add(p); }
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(at(cyl(0.006, 0.006, 0.05, gold, 6, { pivot: 'top' }), sx * w / 2, 0.07, sz * w / 2), at(sphere(0.016, gold, 0), sx * w / 2, 0.01, sz * w / 2));
    return g;
  },

  // The republican guard's helmet (pivot at the crown of the head, front +Z): a chrome dome with a brass crest, a long black horsehair plume flowing
  // down the back and a red plume standing up at the left side; attach it to the 'head' joint
  guardHelmet(o) {
    // (pass 3 of 77) o.gold: a gold dome with a darker crest, a short peak instead of the wide rim and a tall red plume (the chrome dome with its flat rim
    // read as a white brimmed hat); o.knockAt (s): the helmet tips over his eyes and wobbles back (an over-snapped salute, a jerk awake), o.knock the angle
    const s = o.s ?? 1, root = grp(), g = grp(), chrome = o.gold ? '#E8B83A' : '#D7DCE2', brass = o.gold ? '#B07A1E' : '#D9A93A'; root.add(g);
    const dome = new THREE.Mesh(new THREE.SphereGeometry(0.15, 14, 8, 0, TAU, 0, PI / 2), L(chrome)); dome.scale.set(1.0, o.gold ? 1.05 : 0.85, 1.1); g.add(dome);
    if (o.gold) g.add(at(box(0.3, 0.035, 0.32, brass, { outline: 0.004 }), 0, 0.0, 0.0), at(box(0.24, 0.02, 0.1, chrome, { outline: 0.003 }), 0, -0.005, 0.19), at(box(0.3, 0.05, 0.02, '#FFF3C4'), 0, 0.07, 0.158));
    else g.add(at(box(0.31, 0.02, 0.33, chrome, { outline: 0.004 }), 0, 0.0, 0.0));
    g.add(at(box(0.035, 0.07, 0.3, brass, { outline: 0.003 }), 0, o.gold ? 0.17 : 0.14, 0.0));
    for (let i = 0; i < 7; i++) { const st = at(box(0.03, 0.42, 0.012, '#151619'), (i - 3) * 0.012, -0.08, -0.17 - 0.004 * Math.abs(i - 3)); st.rotation.x = 0.35 + 0.02 * (i % 3); g.add(st); }
    if (o.gold) g.add(at(cyl(0.05, 0.022, 0.36, '#D8202C', 8, { pivot: 'bottom', outline: 0.004 }), 0, 0.17, 0.1), at(sphere(0.052, '#D8202C', 1), 0, 0.53, 0.1));
    else g.add(at(cyl(0.022, 0.012, 0.22, '#C8222E', 8, { pivot: 'bottom' }), 0.1, 0.06, 0.03));
    const kn = [].concat(o.knockAt ?? []), ka = o.knock ?? 0.55;
    if (kn.length) { root.userData.update = t => { let a = 0; for (const k0 of kn) { const u = t - k0; if (u >= 0) a = u < 0.07 ? ka * u / 0.07 : ka * (o.stay ?? 0.45) + ka * (1 - (o.stay ?? 0.45)) * Math.exp(-(u - 0.07) * 6) * Math.cos((u - 0.07) * 20); if (o.back != null && t > o.back) a *= Math.max(0, 1 - (t - o.back) / 0.12); }
      g.rotation.x = a; g.position.set(0, -0.03 * a, 0.09 * a); }; root.userData.update(0); }
    root.scale.setScalar(s); return root;
  },

  // A rotating police light on the counter (pivot at its base): a dark base, a red glass dome and, from o.from (s), a bright beam turning round
  // o.rps (2) times a second, the dome glowing
  beacon(o) {
    const g = grp(), from = o.from ?? 0, rps = o.rps ?? 2;
    g.add(at(cyl(0.05, 0.055, 0.04, '#26282C', 12, { pivot: 'bottom', outline: 0.003 }), 0, 0, 0));
    const domeM = new THREE.MeshBasicMaterial({ color: '#7A1A1A' }), dome = new THREE.Mesh(new THREE.SphereGeometry(0.045, 12, 8, 0, TAU, 0, PI / 2), domeM); dome.position.y = 0.04; g.add(dome);
    const BL = o.len ?? 0.6, geo = new THREE.ConeGeometry(BL * 0.25, BL, 16, 1, true); geo.translate(0, -BL / 2, 0); geo.rotateZ(PI / 2);   // (stills 1) o.len: the beam's reach (1.4 m crossed the whole frame)
    const beam = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: '#FF4A3A', transparent: true, opacity: o.opacity ?? 0.22, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending }));
    const spin = grp(); spin.position.y = 0.06; spin.add(beam); g.add(spin);
    g.userData.update = t => { const on = t >= from; spin.visible = on; domeM.color.set(on ? (Math.sin((t - from) * rps * TAU) > -0.2 ? '#FF3A2A' : '#B02020') : '#7A1A1A'); spin.rotation.y = (t - from) * rps * TAU; };
    g.userData.update(-1); return g;
  },
  // (pass 3 of 77) A one-cent coin that reads as a coin (pivot at its centre, its faces along Z): a copper disc o.r (0.04), a light raised rim, a face
  // with a big 1 and CENT; o.glint [t...]: a four-point star flashes beside it (at o.glintAt [x, y], metres) for o.flash (0.3 s): never on top of it
  centCoin(o) {
    const r = o.r ?? 0.04, g = grp(), cu = o.color || '#B5673A', rim = o.rim || '#F2B98C';
    const d = cyl(r, r, r * 0.16, cu, 28, { outline: 0.0025 }); d.rotation.x = PI / 2; g.add(d);
    for (const sz of [-1, 1]) { const rg = new THREE.Mesh(new THREE.TorusGeometry(r * 0.9, r * 0.075, 6, 28), L(rim)); rg.position.z = sz * r * 0.08; g.add(rg);
      const f = canvasPlane(r * 1.66, r * 1.66, (c, W) => { c.clearRect(0, 0, W, W); c.fillStyle = '#C97C46'; c.beginPath(); c.arc(W / 2, W / 2, W * 0.49, 0, TAU); c.fill();
        c.fillStyle = '#6E3414'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${W * 0.7}px Arial`; c.fillText('1', W * 0.36, W * 0.52);
        c.font = `900 ${W * 0.17}px Arial`; c.save(); c.translate(W * 0.72, W * 0.52); c.rotate(-PI / 2); c.fillText('CENT', 0, 0); c.restore();
        c.fillStyle = '#F2B98C'; for (let i = 0; i < 6; i++) { const a = -0.9 + i * 0.36; c.beginPath(); c.arc(W / 2 + Math.cos(a) * W * 0.4, W / 2 - Math.sin(a) * W * 0.4, W * 0.022, 0, TAU); c.fill(); } }, { res: 256, transparent: true });
      f.position.z = sz * r * 0.09; if (sz < 0) f.rotation.y = PI; g.add(f); }
    const star = canvasPlane(r * 2.6, r * 2.6, (c, W) => { c.clearRect(0, 0, W, W); c.fillStyle = '#FFFFFF'; c.beginPath(); for (let i = 0; i < 8; i++) { const a = i * TAU / 8, rr = W * (i % 2 ? 0.07 : 0.48); c.lineTo(W / 2 + Math.cos(a) * rr, W / 2 + Math.sin(a) * rr); } c.closePath(); c.fill(); }, { res: 128, transparent: true, emissive: 1 });
    const ga = o.glintAt || [r * 1.5, r * 1.3]; star.position.set(ga[0], ga[1], r * 0.4); star.visible = false; g.add(star);
    const fl = [].concat(o.glint ?? []), dur = o.flash ?? 0.3;
    g.userData.update = t => { star.visible = false; for (const f0 of fl) { const u = (t - f0) / dur; if (u >= 0 && u < 1) { star.visible = true; const k = Math.sin(u * PI); star.scale.set(k, k, 1); star.rotation.z = u * 1.2; } } };
    g.userData.update(-1); return g;
  },

  // (pass 3 of 77) A cheque of the Treasury (in the XY plane, front +Z: lay it flat with rot [-PI / 2, 0, a]): o.w x o.h, a blue frame, the payee
  // lines and the amount o.amount in a box that fills the right half
  taxCheque(o) {
    const w = o.w ?? 0.46, h = o.h ?? 0.2, g = grp(at(box(w, h, 0.004, '#FBF7EA', { outline: 0.004 }), 0, 0, 0));
    const f = canvasPlane(w * 0.985, h * 0.97, (c, W, H) => { c.fillStyle = '#FBF7EA'; c.fillRect(0, 0, W, H); c.strokeStyle = '#2F62B5'; c.lineWidth = H * 0.035; c.strokeRect(H * 0.05, H * 0.05, W - H * 0.1, H - H * 0.1);
      c.fillStyle = '#2F62B5'; c.textBaseline = 'middle'; c.textAlign = 'left'; fitText(c, o.text || 'TRÉSOR PUBLIC', W * 0.38, H * 0.2); c.fillText(o.text || 'TRÉSOR PUBLIC', W * 0.05, H * 0.24);
      c.fillStyle = '#9AA0A8'; for (const y of [0.46, 0.62, 0.78]) c.fillRect(W * 0.05, H * y, W * 0.34, H * 0.035);
      c.fillStyle = '#FFFFFF'; c.fillRect(W * 0.44, H * 0.16, W * 0.52, H * 0.68); c.strokeStyle = '#1C1D22'; c.lineWidth = H * 0.04; c.strokeRect(W * 0.44, H * 0.16, W * 0.52, H * 0.68);
      c.fillStyle = '#1C1D22'; c.textAlign = 'center'; const a = o.amount || '0,01 €'; fitText(c, a, W * 0.46, H * 0.5); c.fillText(a, W * 0.7, H * 0.52); }, { res: 512 });
    f.position.z = 0.004; g.add(f); return g;
  },

  // (pass 3 of 77) A postage stamp with a serrated edge (in the XY plane, front +Z): o.w x o.h, a red field, its price o.text in large white type;
  // o.at (s): it is not there before, and lands with a pop
  postStamp(o) {
    const w = o.w ?? 0.16, h = o.h ?? 0.2, g = grp(), body = grp(); g.add(body);
    const f = canvasPlane(w, h, (c, W, H) => { c.clearRect(0, 0, W, H); const m = W * 0.07, n = 9, nh = Math.max(3, Math.round(n * H / W)); c.fillStyle = '#FFFFFF'; c.fillRect(m, m, W - 2 * m, H - 2 * m);
      for (let i = 0; i <= n; i++) for (const y of [m, H - m]) { c.beginPath(); c.arc(m + (W - 2 * m) * i / n, y, m * 0.72, 0, TAU); c.fill(); }
      for (let j = 0; j <= nh; j++) for (const x of [m, W - m]) { c.beginPath(); c.arc(x, m + (H - 2 * m) * j / nh, m * 0.72, 0, TAU); c.fill(); }
      c.fillStyle = o.color || '#C8322A'; c.fillRect(m * 2.2, m * 2.2, W - 4.4 * m, H - 4.4 * m);
      c.fillStyle = '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle'; const t = o.text || '3,00 €'; fitText(c, t, W - 5.6 * m, H * 0.36); c.fillText(t, W / 2, H * 0.52);
      fitText(c, o.top || 'TIMBRE', W - 6 * m, H * 0.12, 800); c.fillText(o.top || 'TIMBRE', W / 2, H * 0.24); fitText(c, o.bottom || 'RF', W - 6 * m, H * 0.12, 800); c.fillText(o.bottom || 'RF', W / 2, H * 0.8); }, { res: 512, transparent: true });
    body.add(f);
    g.userData.update = t => { if (o.at == null) return; const u = t - o.at; body.visible = u >= 0; const k = u < 0 ? 1 : u < 0.07 ? 1.5 - 0.5 * u / 0.07 : 1 + 0.12 * Math.exp(-(u - 0.07) * 10) * Math.cos((u - 0.07) * 30); body.scale.set(k, k, 1); };
    g.userData.update(0); return g;
  },

  // (pass 3 of 77) The minister's car (the shared car, nose +X): a navy body that takes the light, pale tinted glass, chrome bumpers, grille and side
  // strips, a tricolour flag on each front wing; its rear door on the side o.doorSide (-1: local -Z) is hinged at its REAR edge and swings open at
  // o.doorAt (s) over a dark opening, so a camera in front of the car sees who steps out (a black car was a detail-free mass, review 2)
  ministerCar(o) {
    const C = o.color || '#2B3F73', LT = o.light || '#4A66A6', CH = '#DDE2E8', g = grp(), side = o.doorSide ?? -1, go = o.glass ?? 0.75, gc = o.glassColor || '#A9C8E6';
    g.add(buildProp('car', { color: C, glass: go, glassColor: gc, plate: o.plate || 'RF-001-RF' }));
    g.add(at(box(0.1, 0.14, 1.9, CH, { outline: 0.006 }), 2.04, 0.5, 0), at(box(0.1, 0.14, 1.9, CH, { outline: 0.006 }), -2.04, 0.5, 0), at(box(0.04, 0.24, 1.0, CH), 2.02, 0.74, 0));
    for (const z of [-0.915, 0.915]) g.add(at(box(3.7, 0.045, 0.02, CH), 0, 0.9, z), at(box(3.9, 0.13, 0.012, LT), 0, 0.74, z), at(box(0.16, 0.035, 0.03, CH), 0.25, 0.82, z));
    g.add(at(box(1.5, 0.012, 1.5, LT), 1.2, 0.916, 0), at(box(2.6, 0.012, 1.4, LT), -0.25, 2.06, 0));
    for (const z of [-0.78, 0.78]) { g.add(rod([1.75, 0.9, z], [1.75, 1.46, z], 0.012, CH)); ['#2F62B5', '#F4F4F0', '#E0413A'].forEach((c, i) => g.add(at(box(0.1, 0.2, 0.012, c, { outline: 0.003 }), 1.69 - 0.1 * i, 1.35, z))); }
    // o.hingeFront: the leaf hangs from its FRONT edge (the usual way: for a camera behind the car); sx: which way the leaf runs from its hinge
    const x0 = -1.58, x1 = -0.3, dl = x1 - x0, hf = !!o.hingeFront, sx = hf ? -1 : 1, hinge = grp(); hinge.position.set(hf ? x1 : x0, 0, side * 0.93);
    g.add(at(box(dl, 1.6, 0.012, '#20232B'), (x0 + x1) / 2, 1.16, side * 0.914));
    const leaf = grp(at(box(dl, 0.58, 0.05, C, { outline: 0.008 }), sx * dl / 2, 0.66, 0), at(box(dl, 0.045, 0.06, CH), sx * dl / 2, 0.9, 0), at(box(0.16, 0.035, 0.07, CH), sx * (dl - 0.2), 0.82, 0), at(box(dl, 0.13, 0.054, LT), sx * dl / 2, 0.74, 0));
    const gl = new THREE.Mesh(new THREE.BoxGeometry(dl - 0.1, 0.98, 0.02), glassMat(go, gc)); gl.position.set(sx * dl / 2, 1.46, 0); leaf.add(gl);
    for (const x of [0.03, dl - 0.03]) leaf.add(at(box(0.06, 1.05, 0.05, C), sx * x, 1.46, 0));
    leaf.add(at(box(dl, 0.06, 0.05, C), sx * dl / 2, 1.98, 0)); hinge.add(leaf); g.add(hinge);
    const ang = o.doorAngle ?? 1.25, dd = o.doorDur ?? 0.16;
    g.userData.update = t => { let a = 0; if (o.doorAt != null) { const u = (t - o.doorAt) / dd; a = u <= 0 ? 0 : u < 1 ? ang * (1 - (1 - u) * (1 - u)) : ang * (1 + 0.08 * Math.exp(-(u - 1) * 3) * Math.cos((u - 1) * 9)); } hinge.rotation.y = -sx * side * a; };
    g.userData.update(0); return g;
  },

  // (pass 3 of 77) A street clock on a post (pivot at the foot, its face +Z): a face of radius o.r (0.45) at o.h (3.2 m); between o.from and o.to (s)
  // the minute hand makes o.turns (1) full turns and the hour hand moves on from o.hour (3): an hour goes by in a shot
  streetClock(o) {
    const r = o.r ?? 0.45, hgt = o.h ?? 3.2, g = grp(), ink = '#1C1D22', iron = o.color || '#2F4A3A';
    g.add(at(cyl(0.06, 0.08, hgt - r, iron, 8, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(cyl(0.16, 0.2, 0.2, iron, 8, { pivot: 'bottom' }), 0, 0, 0));
    const head = grp(); head.position.y = hgt; g.add(head);
    const rm = cyl(r * 1.1, r * 1.1, 0.14, iron, 24, { outline: 0.008 }); rm.rotation.x = PI / 2; head.add(rm);
    const face = canvasPlane(2 * r, 2 * r, (c, W) => { c.clearRect(0, 0, W, W); c.fillStyle = '#FBF8EE'; c.beginPath(); c.arc(W / 2, W / 2, W * 0.495, 0, TAU); c.fill(); c.fillStyle = ink;
      for (let i = 0; i < 12; i++) { const a = i * TAU / 12, k = i % 3 === 0 ? 2 : 1; c.save(); c.translate(W / 2 + Math.sin(a) * W * 0.41, W / 2 - Math.cos(a) * W * 0.41); c.rotate(a); c.fillRect(-W * 0.013 * k, -W * 0.05, W * 0.026 * k, W * 0.1); c.restore(); } }, { res: 256, transparent: true });
    face.position.z = 0.074; head.add(face);
    const hand = (len, wd, z) => { const p = grp(at(box(wd, len, 0.01, ink), 0, len / 2 - wd, 0)); p.position.z = z; head.add(p); return p; };
    const hh = hand(r * 0.5, r * 0.1, 0.084), mh = hand(r * 0.82, r * 0.065, 0.096); head.add(at(sphere(r * 0.075, '#C8322A', 0), 0, 0, 0.1));
    const t0 = o.from ?? 0, t1 = o.to ?? 1, turns = o.turns ?? 1, h0 = o.hour ?? 3;
    g.userData.update = t => { const u = clamp01((t - t0) / Math.max(1e-3, t1 - t0)); mh.rotation.z = -u * turns * TAU; hh.rotation.z = -(h0 + u * turns) * TAU / 12; };
    g.userData.update(0); return g;
  },

  // (pass 3 of 77) A television camera on a tripod (pivot at the floor, its lens +Z): a pale grey body that takes the light, a dark lens with a blue
  // glass and a highlight, a viewfinder, a handle, and two red tally lights (back and front) that blink (o.blink false: steady); o.h (1.5 m)
  newsCam(o) {
    const g = grp(), grey = o.color || '#98A1AD', dk = '#3A3F48', hgt = o.h ?? 1.5;
    for (let i = 0; i < 3; i++) { const a = i * TAU / 3 + 0.5; g.add(rod([0, hgt - 0.08, 0], [Math.sin(a) * 0.46, 0, Math.cos(a) * 0.46], 0.022, dk)); }
    g.add(at(cyl(0.07, 0.07, 0.12, dk, 8), 0, hgt - 0.05, 0));
    const head = grp(); head.position.y = hgt + 0.02; g.add(head);
    head.add(at(box(0.3, 0.3, 0.62, grey, { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(box(0.312, 0.09, 0.34, '#C4CBD4'), 0, 0.2, 0.05));
    const lens = cyl(0.11, 0.09, 0.26, dk, 14, { outline: 0.006 }); lens.rotation.x = PI / 2; lens.position.set(0, 0.16, 0.43); head.add(lens);
    const hood = cyl(0.15, 0.12, 0.1, '#23262E', 14); hood.rotation.x = PI / 2; hood.position.set(0, 0.16, 0.6); head.add(hood);
    const gl = new THREE.Mesh(new THREE.CircleGeometry(0.105, 16), new THREE.MeshBasicMaterial({ color: '#7FB6E0' })); gl.position.set(0, 0.16, 0.652); head.add(gl);
    head.add(at(sphere(0.03, '#FFFFFF', 0), 0.04, 0.2, 0.655), at(box(0.08, 0.1, 0.22, dk, { outline: 0.004 }), -0.19, 0.24, -0.22), rod([0.1, 0.3, -0.22], [0.1, 0.42, 0.22], 0.018, dk));
    const tm = new THREE.MeshBasicMaterial({ color: '#FF2A1A' });
    for (const [x, y, z, rr] of [[0, 0.36, -0.25, 0.05], [0.0, 0.34, 0.3, 0.035]]) { const tl = new THREE.Mesh(new THREE.SphereGeometry(rr, 10, 8), tm); tl.position.set(x, y, z); head.add(tl); }
    head.rotation.x = o.tilt ?? 0;
    g.userData.update = t => { const on = o.blink === false || Math.sin(t * (o.rate ?? 9)) > -0.3; tm.color.set(on ? '#FF2A1A' : '#7A1410'); };
    g.userData.update(0); return g;
  },

  // (pass 3 of 77) A reporter's hand microphone (pivot at the grip, the head up +Y): a dark handle, a white cube with o.text (TV) on its four faces, a
  // red foam ball; attach it with face: 'camera' so it stands upright whatever the hand does; o.s scale
  handMic(o) {
    const g = grp(at(cyl(0.022, 0.018, 0.24, '#23262E', 8, { pivot: 'bottom' }), 0, -0.08, 0), at(sphere(0.062, o.color || '#E0413A', 1), 0, 0.22, 0), at(box(0.1, 0.075, 0.1, '#FFFFFF', { outline: 0.004 }), 0, 0.12, 0));
    for (const [ry, x, z] of [[0, 0, 0.051], [PI, 0, -0.051], [PI / 2, 0.051, 0], [-PI / 2, -0.051, 0]]) { const p = canvasPlane(0.09, 0.065, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.fillStyle = '#2F62B5'; c.textAlign = 'center'; c.textBaseline = 'middle'; fitText(c, o.text || 'TV', W * 0.86, H * 0.8); c.fillText(o.text || 'TV', W / 2, H * 0.54); }, { res: 128 }); p.position.set(x, 0.12, z); p.rotation.y = ry; g.add(p); }
    g.scale.setScalar(o.s ?? 1); return g;
  },

  // (pass 3 of 77) A front door with a letter slot (pivot at the floor middle, front +Z): o.w x o.h, four panels, a cream fanlight over it, a brass
  // knob and a brass slot at o.slotY (0.95) whose flap swings in at o.flapAt (s) and flutters
  mailDoor(o) {
    const w = o.w ?? 1.08, h = o.h ?? 1.9, g = grp(), C = o.color || '#6FA6BE', dk = o.dark || '#578CA4', brass = '#D9A93A', sy = o.slotY ?? 0.95;
    g.add(at(box(w, h, 0.05, C, { pivot: 'bottom', outline: 0.008 }), 0, 0, 0));
    for (const [y, hh] of [[1.2, 0.56], [0.2, 0.56]]) for (const sx of [-1, 1]) g.add(at(box(w * 0.36, hh, 0.02, dk, { pivot: 'bottom' }), sx * w * 0.22, y, 0.03));
    const fan = new THREE.Mesh(new THREE.CylinderGeometry(w / 2, w / 2, 0.04, 16, 1, false, PI / 2, PI), L('#F6EFD8')); fan.rotation.x = PI / 2; fan.position.set(0, h, 0); g.add(fan);
    g.add(at(box(w, 0.07, 0.07, '#EADFC0'), 0, h, 0.02), at(sphere(0.045, brass, 1), w * 0.38, 1.05, 0.07));
    g.add(at(box(0.42, 0.11, 0.012, brass, { outline: 0.004 }), 0, sy, 0.034), at(box(0.34, 0.045, 0.006, '#1C1D22'), 0, sy, 0.042));
    const flap = grp(at(box(0.36, 0.06, 0.008, brass, { outline: 0.003 }), 0, -0.03, 0)); flap.position.set(0, sy + 0.03, 0.05); g.add(flap);
    g.userData.update = t => { let a = 0; if (o.flapAt != null) { const u = t - o.flapAt; a = u < 0 ? 0 : u < 0.08 ? 1.3 * u / 0.08 : 1.3 * Math.exp(-(u - 0.08) * 5) * Math.abs(Math.cos((u - 0.08) * 14)); } flap.rotation.x = -a; };
    g.userData.update(0); return g;
  },

  // (pass 3 of 77) A snore bubble at the nose (attach to the head joint, in front of the face; it grows toward +Z): from o.from it swells and shrinks
  // every o.period (0.6 s) up to o.r (0.11); at o.popAt it swells once more and is gone
  snoreBubble(o) {
    const g = grp(), b = new THREE.Mesh(new THREE.SphereGeometry(1, 12, 9), new THREE.MeshLambertMaterial({ color: '#BFE3F5', transparent: true, opacity: 0.8 })); g.add(b);
    const hl = new THREE.Mesh(new THREE.SphereGeometry(0.2, 8, 6), new THREE.MeshBasicMaterial({ color: '#FFFFFF' })); hl.position.set(-0.42, 0.45, 0.72); b.add(hl);
    const from = o.from ?? 0, pop = o.popAt ?? 1e9, R = o.r ?? 0.11, per = o.period ?? 0.6;
    g.userData.update = t => { const on = t >= from && t < pop + 0.05; b.visible = on; if (!on) return; const k = t >= pop ? 1.4 : 0.3 + 0.7 * (0.5 - 0.5 * Math.cos((t - from) / per * TAU)), s = R * k; b.scale.setScalar(s); b.position.set(0, 0, s); };
    g.userData.update(0); return g;
  },

  // (pass 3 of 77) The guard's dress: a sabre held at the shoulder (pivot at the hilt, the blade up +Y, o.len 0.95) ...
  sabre(o) {
    const len = o.len ?? 0.95;
    return grp(at(box(0.03, len, 0.012, '#E4E8EE', { pivot: 'bottom', outline: 0.004 }), 0, 0.1, 0), at(box(0.15, 0.03, 0.05, '#D9A93A', { outline: 0.003 }), 0, 0.09, 0), at(cyl(0.02, 0.02, 0.12, '#23262E', 6, { pivot: 'bottom' }), 0, -0.03, 0));
  },
  // ... and his red epaulettes with a gold fringe (pivot between the shoulders, at their height; o.w 0.52: from one shoulder to the other)
  epaulettes(o) {
    const g = grp(), w = o.w ?? 0.52;
    for (const sx of [-1, 1]) g.add(at(box(0.2, 0.05, 0.22, '#D8202C', { outline: 0.004 }), sx * w / 2, 0, 0), at(box(0.04, 0.1, 0.22, '#E2B53C'), sx * (w / 2 + 0.09), -0.045, 0));
    return g;
  },

  // (pass 3 of 77) The band's instruments, big enough to read (o.kind): 'sousa': a sousaphone (pivot at the chest: attach to the torso), a gold ring
  // round the body and a wide bell over the head that swells on the o.beat times; 'trumpet' (pivot at the grip, the bell +Z, 0.5 m long); 'drum'
  // (pivot at the belly: attach to the torso), a red drum with a white skin that jumps on o.beat; 'stick': a drumstick (pivot at the grip, +Y)
  bandInstr(o) {
    const br = o.color || '#E2B53C', g = grp(), k = o.kind || 'sousa', beat = o.beat || [];
    const hit = t => { let a = 0; for (const b of beat) { const u = t - b; if (u >= 0 && u < 0.2) a = Math.max(a, 1 - u / 0.2); } return a; };
    if (k === 'sousa') { const ring = new THREE.Mesh(new THREE.TorusGeometry(0.4, 0.06, 8, 22), L(br)); ring.rotation.set(0.3, 0, 0.55); ring.position.set(0, 0.1, 0); g.add(ring);
      g.add(rod([0.32, 0.3, -0.08], [0.3, 1.0, -0.02], 0.055, br));
      const bell = grp(), cone = new THREE.Mesh(new THREE.CylinderGeometry(0.44, 0.09, 0.42, 18, 1, true), new THREE.MeshLambertMaterial({ color: br, side: THREE.DoubleSide })); cone.position.y = 0.21; bell.add(cone);
      const rimT = new THREE.Mesh(new THREE.TorusGeometry(0.44, 0.03, 6, 22), L('#F6D878')); rimT.rotation.x = PI / 2; rimT.position.y = 0.42; bell.add(rimT);
      const hole = new THREE.Mesh(new THREE.CircleGeometry(0.2, 16), new THREE.MeshBasicMaterial({ color: '#7A5A16' })); hole.rotation.x = -PI / 2; hole.position.y = 0.2; bell.add(hole);
      bell.position.set(0.3, 0.98, 0.0); bell.rotation.x = 1.0; g.add(bell);
      g.userData.update = t => { const a = hit(t); bell.scale.setScalar(1 + 0.2 * a); }; }
    else if (k === 'trumpet') { const tube = cyl(0.016, 0.016, 0.42, br, 8, { outline: 0.003 }); tube.rotation.x = PI / 2; tube.position.set(0, 0.02, 0.16); g.add(tube);
      const bell = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.016, 0.16, 16, 1, true), new THREE.MeshLambertMaterial({ color: br, side: THREE.DoubleSide })); bell.rotation.x = PI / 2; bell.position.set(0, 0.02, 0.44); g.add(bell);
      for (const z of [0.06, 0.11, 0.16]) g.add(at(cyl(0.011, 0.011, 0.08, '#C9A043', 6), 0, 0.07, z));
      g.userData.update = t => { const a = hit(t); bell.scale.set(1 + 0.25 * a, 1, 1 + 0.25 * a); }; }
    else if (k === 'drum') { const dr = grp(at(cyl(0.24, 0.24, 0.26, '#C8322A', 18, { outline: 0.005 }), 0, 0, 0), at(cyl(0.245, 0.245, 0.02, '#F4F1E8', 18), 0, 0.135, 0), at(cyl(0.25, 0.25, 0.03, br, 18), 0, 0.115, 0), at(cyl(0.25, 0.25, 0.03, br, 18), 0, -0.115, 0));
      dr.rotation.x = 0.5; g.add(dr); const skin = dr.children[1];
      g.userData.update = t => { const a = hit(t); skin.position.y = 0.135 + 0.03 * a; dr.scale.set(1 + 0.06 * a, 1 - 0.12 * a, 1 + 0.06 * a); }; }
    else g.add(at(cyl(0.012, 0.012, 0.34, '#E8D9B0', 6, { pivot: 'bottom' }), 0, -0.04, 0), at(sphere(0.026, '#E8D9B0', 0), 0, 0.31, 0));
    if (g.userData.update) g.userData.update(-1);
    if (o.s) g.scale.setScalar(o.s); return g;
  },

  // (pass 3 of 77) The bill that unrolls (pivot at the hands: it hangs down -Y for o.top metres, then runs on the floor toward +Z): o.w wide (0.5),
  // o.max long in all (4.4 m); o.len [[t, metres], ...]: how much is unrolled. Its content is laid out once along its whole length (a header, the
  // rows o.rows [[name, price], ...], then at o.totalAt metres from the top a red block TOTAL with o.total in type as wide as the paper, then small
  // print), upright for a camera in front; the roll at its end hops as it runs. (The shared billScroll repeats six ski-pass rows, upside down on the floor.)
  expenseBill(o) {
    const w = o.w ?? 0.5, top = o.top ?? 1.55, Lmax = o.max ?? 4.4, g = grp(), rows = o.rows || [['VOITURE', '480 000 €'], ['GARDE', '620 000 €'], ['FANFARE', '230 000 €'], ['HÉLICOPTÈRES', '540 000 €'], ['COUSSIN', '129 999,99 €'], ['CENTIME', '0,01 €']];
    const tAt = o.totalAt ?? 2.7, tLen = o.totalLen ?? 0.8, total = o.total || '2 000 000 €';
    const cv = document.createElement('canvas'); cv.width = 384; cv.height = Math.round(384 * Lmax / w); const x = cv.getContext('2d'), W = cv.width, H = cv.height, m = W / w;
    x.fillStyle = '#FBF4DC'; x.fillRect(0, 0, W, H); x.fillStyle = '#C9B98A'; x.fillRect(0, 0, W * 0.025, H); x.fillRect(W * 0.975, 0, W * 0.025, H);
    x.textBaseline = 'middle'; x.fillStyle = '#C8302A'; x.fillRect(0, 0, W, 0.22 * m); x.fillStyle = '#FFFFFF'; x.textAlign = 'center'; fitText(x, o.head || 'FACTURE', W * 0.86, 0.16 * m); x.fillText(o.head || 'FACTURE', W / 2, 0.115 * m);
    const y0 = 0.3 * m, step = (tAt * m - y0) / rows.length;
    rows.forEach(([nm, pr], i) => { const y = y0 + step * i; x.fillStyle = '#2A2C33'; x.textAlign = 'left'; fitText(x, nm, W * 0.88, step * 0.3, 800); x.fillText(nm, W * 0.06, y + step * 0.26);
      x.textAlign = 'right'; x.fillStyle = '#C8302A'; fitText(x, pr, W * 0.88, step * 0.36); x.fillText(pr, W * 0.94, y + step * 0.64); x.fillStyle = '#B9A878'; x.fillRect(W * 0.06, y + step * 0.92, W * 0.88, 3); });
    const ty = tAt * m, th = tLen * m; x.fillStyle = '#C8302A'; x.fillRect(W * 0.04, ty + th * 0.05, W * 0.92, th * 0.9); x.fillStyle = '#FFFFFF'; x.textAlign = 'center';
    fitText(x, 'TOTAL', W * 0.6, th * 0.26); x.fillText('TOTAL', W / 2, ty + th * 0.27); fitText(x, total, W * 0.84, th * 0.44); x.fillText(total, W / 2, ty + th * 0.64);
    x.fillStyle = '#8A8F98'; for (let y = ty + th + 0.08 * m; y < H - 0.04 * m; y += 0.09 * m) x.fillRect(W * 0.06, y, W * (0.5 + 0.38 * ((y * 7 % 13) / 13)), 4);
    const mk = () => { const tx = new THREE.CanvasTexture(cv); tx.colorSpace = THREE.SRGBColorSpace; const geo = new THREE.PlaneGeometry(w, 1); geo.translate(0, -0.5, 0); const me = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ map: tx, side: THREE.DoubleSide })); me.receiveShadow = true; return me; };
    const down = mk(), along = mk(); along.rotation.x = -PI / 2;
    const roll = cyl(0.04, 0.04, w * 1.03, '#F4F0E2', 12, { outline: 0.004 }); roll.rotation.z = PI / 2;
    g.add(down, along, roll);
    g.userData.update = t => {
      const Lc = Math.max(0.02, Math.min(Lmax, lenAt(o.len ?? 1, t))), Lv = Math.min(Lc, top - 0.03), Lf = Math.max(0, Lc - Lv);
      down.scale.y = Lv; down.material.map.repeat.set(1, Lv / Lmax); down.material.map.offset.set(0, 1 - Lv / Lmax);
      along.visible = Lf > 0.002; along.scale.y = Math.max(0.002, Lf); along.position.set(0, -top + 0.012, 0); along.material.map.repeat.set(1, Lf / Lmax); along.material.map.offset.set(0, 1 - Lc / Lmax);
      const end = Lc >= Lmax - 1e-3;
      if (Lf > 0.002) { roll.visible = !end; roll.position.set(0, -top + 0.045 + (o.hop ?? 0.07) * Math.abs(Math.sin(Lf * 6)) * Math.exp(-Lf * 0.5), Lf); roll.rotation.x = Lf / 0.04; } else { roll.visible = true; roll.position.set(0, -Lv, 0.0); roll.rotation.x = Lv / 0.04; }
    };
    g.userData.update(0); return g;
  },
};
