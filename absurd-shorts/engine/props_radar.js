// « Le radar » (story 46): a man runs for his bus; a speed camera flashes him at 31 km/h in a 30 zone; above thirty, says the prefecture, a pedestrian is
// a vehicle: he gets a number plate, a technical inspection (tyres fine, horn fine, brakes refused), he may no longer walk; the bus pushes him every
// morning. Conventions as in props.js (metres, front +Z, pivot at the floor); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, ease, clamp01 } from './style.js';
import { grp, at, label, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const rnd = s => { let x = Math.sin(s * 127.1) * 43758.5453; return x - Math.floor(x); };
const wob = (u, f, d) => u < 0 ? 0 : Math.exp(-u * d) * Math.sin(u * f);
const keyed = (l, t, d) => { if (!l || !l.length) return d; let v = d, prev = d, t0 = -1; for (const [a, b] of l) { if (t >= a) { prev = v; v = b; t0 = a; } } if (t0 < 0) return v;
  const u = clamp01((t - t0) / 0.25); return prev + (v - prev) * ease.out(u); };   // [[t, value]]: eased (0.25 s) from the previous value

export const RADAR_PROPS = {
  // A French speed camera on its pole, front +Z: a grey cabinet, a dark window with the lens, a flash panel that fires at o.flashAt (or a list) for 0.08 s
  // (white, emissive, with a halo); o.h (2.1: the foot of the cabinet).
  speedCamera(o) {
    const h = o.h ?? 2.1, g = grp(at(cyl(0.06, 0.07, h, '#7A8088', 8, { pivot: 'bottom' }), 0, 0, 0));
    g.add(at(box(0.52, 0.62, 0.46, '#9AA1A9', { outline: 0.008 }), 0, h + 0.31, 0), at(box(0.56, 0.06, 0.5, '#6E747C'), 0, h + 0.65, 0));
    g.add(at(box(0.36, 0.22, 0.02, '#1B1D22'), 0, h + 0.4, 0.235), at(cyl(0.06, 0.06, 0.03, '#3A3D44', 12), -0.07, h + 0.4, 0.25, PI / 2, 0, 0));
    const fl = new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0, depthWrite: false });
    const flash = new THREE.Mesh(new THREE.PlaneGeometry(0.14, 0.14), fl); flash.position.set(0.1, h + 0.4, 0.248); flash.userData.noAO = true; g.add(flash);
    const halo = new THREE.Mesh(new THREE.CircleGeometry(0.6, 20), fl.clone()); halo.position.set(0.1, h + 0.4, 0.26); halo.userData.noAO = true; g.add(halo);
    const at0 = [].concat(o.flashAt ?? []);
    g.userData.update = t => { let k = 0; for (const a of at0) { const u = (t - a) / 0.09; if (u >= 0 && u < 1) k = Math.max(k, 1 - u); }
      flash.material.opacity = k; halo.material.opacity = 0.7 * k; halo.scale.setScalar(0.4 + 1.6 * k); };
    g.userData.update(0); return g;
  },

  // A speed display (radar pédagogique) on a pole, front +Z: black panel, the speed in big red LED digits (o.speed '31', from o.showAt) and under it a
  // face that turns sad (o.sadAt); o.h (2.0).
  speedDisplay(o) {
    const h = o.h ?? 2.0, g = grp(at(cyl(0.05, 0.06, h, '#7A8088', 8, { pivot: 'bottom' }), 0, 0, 0), at(box(0.8, 0.75, 0.1, '#1B1D22', { outline: 0.008 }), 0, h + 0.38, 0));
    const draw = (txt, color, face) => (c, W, H) => { c.fillStyle = '#0D0E10'; c.fillRect(0, 0, W, H);
      c.fillStyle = '#F4F1E8'; c.fillRect(0, 0, W, H * 0.13); c.fillStyle = '#1B1D22'; c.font = `900 ${Math.round(H * 0.085)}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.header || 'VOTRE VITESSE', W / 2, H * 0.07);   // (pass 2) a lit header: the housing never goes black
      if (txt) { c.fillStyle = color; c.font = `900 ${Math.round(H * 0.44)}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(txt, W / 2, H * 0.4); }
      if (face) { c.strokeStyle = color; c.lineWidth = H * 0.035; c.beginPath(); c.arc(W / 2, H * 0.8, H * 0.13, 0, TAU); c.stroke();
        c.fillStyle = color; c.beginPath(); c.arc(W / 2 - H * 0.045, H * 0.77, H * 0.018, 0, TAU); c.arc(W / 2 + H * 0.045, H * 0.77, H * 0.018, 0, TAU); c.fill();
        c.beginPath(); if (face === 'sad') c.arc(W / 2, H * 0.89, H * 0.06, PI * 1.15, PI * 1.85); else c.arc(W / 2, H * 0.79, H * 0.06, PI * 0.15, PI * 0.85); c.stroke(); } };
    const off = at(canvasPlane(0.7, 0.65, draw('', '#E8302A', o.sadAt != null ? 'sad' : null), { res: 256, emissive: 0.6 }), 0, h + 0.38, 0.052);   // (pass 2) the blink: the digits off, the face and the header still lit
    const on = at(canvasPlane(0.7, 0.65, draw(o.speed || '31', '#FF3B30', 'happy'), { res: 256, emissive: 1 }), 0, h + 0.38, 0.053);
    const sad = at(canvasPlane(0.7, 0.65, draw(o.speed || '31', '#FF3B30', 'sad'), { res: 256, emissive: 1 }), 0, h + 0.38, 0.054);
    g.add(off, on, sad);
    g.userData.update = t => { const s = o.showAt == null || t >= o.showAt, d = o.sadAt != null && t >= o.sadAt, blinkOff = d && t - o.sadAt < (o.blinkFor ?? 0.5) && Math.floor((t - o.sadAt) * 6) % 2 === 1;   // (pass 2) blinks for o.blinkFor (0.5 s), then the frown holds
      on.visible = s && !d; sad.visible = d && !blinkOff; off.visible = !s || blinkOff; };
    g.userData.update(0); return g;
  },

  // A French number plate (white, the blue band with F at the left): o.text ('PI-031-ON'), o.w (0.52); front +Z, origin at its middle.
  licensePlate(o) {
    const w = o.w ?? 0.52, h = w * 0.21, g = grp(at(box(w + 0.02, h + 0.02, 0.012, '#1B1D22'), 0, 0, -0.004));
    g.add(at(canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.fillStyle = '#1F4EA8'; c.fillRect(0, 0, W * 0.09, H); c.fillRect(W * 0.91, 0, W * 0.09, H);
      c.fillStyle = '#FFFFFF'; c.font = `bold ${Math.round(H * 0.32)}px Arial`; c.textAlign = 'center'; c.fillText('F', W * 0.045, H * 0.82);
      c.fillStyle = '#111111'; c.font = `900 ${Math.round(H * 0.7)}px Arial`; c.textBaseline = 'middle'; c.fillText(o.text || 'PI-031-ON', W / 2, H * 0.54); }, { res: 512 }), 0, 0, 0.004));
    return g;
  },

  // A round road sign on a pole, front +Z: o.text ('30') in a red ring; o.top ('ZONE') on a small panel over it; o.h (2.2).
  zoneSign(o) {
    const h = o.h ?? 2.2, g = grp(at(cyl(0.035, 0.035, h + 0.5, '#9AA1A9', 8, { pivot: 'bottom' }), 0, 0, -0.04));
    g.add(at(canvasPlane(0.62, 0.62, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.beginPath(); c.arc(W / 2, H / 2, W * 0.48, 0, TAU); c.fill(); c.strokeStyle = '#D0202A'; c.lineWidth = W * 0.11; c.beginPath(); c.arc(W / 2, H / 2, W * 0.41, 0, TAU); c.stroke();
      c.fillStyle = '#111111'; c.font = `900 ${Math.round(H * 0.38)}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.text || '30', W / 2, H * 0.53); }, { res: 256, transparent: true }), 0, h + 0.3, 0));
    if (o.top !== false) g.add(at(box(0.66, 0.24, 0.02, '#FFFFFF', { outline: 0.004 }), 0, h + 0.76, -0.01), at(label(o.top || 'ZONE', 0.6, 0.2, { bg: '#FFFFFF', fg: '#111111', wrap: false }), 0, h + 0.76, 0.002));
    return g;
  },

  // A big gauge on a wall, front +Z: a dial 0..50 with a red needle (o.needle [[t, value]], eased), and over it two lamps PIÉTON (green) / VÉHICULE
  // (red): the red one lights when the needle passes o.limit (30).
  speedGauge(o) {
    const R = o.r ?? 0.42, lim = o.limit ?? 30, max = o.max ?? 50, g = grp(at(box(1.1, 1.45, 0.06, '#2A2C31', { outline: 0.01 }), 0, 0, -0.03));
    g.add(at(canvasPlane(2 * R, 2 * R, (c, W, H) => { c.fillStyle = '#F4F1E8'; c.beginPath(); c.arc(W / 2, H / 2, W * 0.49, 0, TAU); c.fill();
      for (let v = 0; v <= max; v += 5) { const a = PI * 1.25 - (v / max) * PI * 1.5, r0 = W * (v % 10 ? 0.4 : 0.36), r1 = W * 0.46; c.strokeStyle = v > lim ? '#D0202A' : '#222'; c.lineWidth = v % 10 ? 3 : 6;
        c.beginPath(); c.moveTo(W / 2 + Math.cos(a) * r0, H / 2 - Math.sin(a) * r0); c.lineTo(W / 2 + Math.cos(a) * r1, H / 2 - Math.sin(a) * r1); c.stroke();
        if (v % 10 === 0) { c.fillStyle = v > lim ? '#D0202A' : '#222'; c.font = `bold ${Math.round(W * 0.08)}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(String(v), W / 2 + Math.cos(a) * W * 0.28, H / 2 - Math.sin(a) * W * 0.28); } }
      c.fillStyle = '#222'; c.font = `bold ${Math.round(W * 0.06)}px Arial`; c.textAlign = 'center'; c.fillText('km/h', W / 2, H * 0.72); }, { res: 512, transparent: true }), 0, -0.18, 0.005));
    const nd = grp(at(box(0.025, R * 0.82, 0.01, '#D0202A'), 0, R * 0.41, 0)); nd.position.set(0, -0.18, 0.02); g.add(nd, at(cyl(0.035, 0.035, 0.02, '#222', 10), 0, -0.18, 0.025, PI / 2, 0, 0));
    const lamp = (txt, c0, c1, x) => { const off = at(label(txt, 0.46, 0.16, { bg: c0, fg: '#EDEDED', wrap: false }), x, 0.56, 0.005), on = at(canvasPlane(0.46, 0.16, (c, W, H) => { c.fillStyle = c1; c.fillRect(0, 0, W, H); c.fillStyle = '#FFFFFF';
      c.font = `900 ${Math.round(H * 0.6)}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(txt, W / 2, H * 0.55); }, { res: 256, emissive: 1 }), x, 0.56, 0.006); g.add(off, on); return [on, off]; };
    const ped = lamp('PIÉTON', '#2F4A3A', '#2EB872', -0.26), veh = lamp('VÉHICULE', '#4A2F2F', '#E8302A', 0.26);
    // (pass 2 of 46) o.crank [[t0, t1, turns], ...]: a crank on the right side of the box (axis at local x 0.62, y -0.35, the knob 0.12 m out) that turns
    // that many times between t0 and t1; userData.crankAngle(t) gives its angle (0 = the knob straight right), for the hand that turns it
    let crank = null; const cks = o.crank || [];
    const crankAngle = t => { let a = 0; for (const [a0, a1, n] of cks) { if (t <= a0) break; a += TAU * n * clamp01((t - a0) / Math.max(0.01, a1 - a0)); } return a; };
    if (cks.length) { crank = grp(at(box(0.12, 0.03, 0.03, '#8A9198'), 0.06, 0, 0), at(cyl(0.02, 0.02, 0.09, '#C8202A', 8), 0.12, 0, 0.05, PI / 2, 0, 0)); crank.position.set(0.62, -0.35, 0.06);
      g.add(crank, at(cyl(0.03, 0.03, 0.08, '#5A5F69', 8), 0.62, -0.35, 0.02, PI / 2, 0, 0), at(box(0.1, 0.12, 0.04, '#2A2C31'), 0.6, -0.35, -0.01)); }
    g.userData.crankAngle = crankAngle;
    g.userData.update = t => { const v = keyed(o.needle, t, 0); nd.rotation.z = (PI * 1.25 - (v / max) * PI * 1.5) - PI / 2; const over = v > lim;   // (the needle is drawn pointing up: +Y)
      ped[0].visible = !over; ped[1].visible = over; veh[0].visible = over; veh[1].visible = !over; if (crank) crank.rotation.z = crankAngle(t); };
    g.userData.update(0); return g;
  },

  // A two-post car lift, front +Z: red posts o.gap (2.6) apart along X, a carriage on each that rises (o.lift [[t, height]], eased, from o.h0 0.15), arms
  // reaching in toward the middle (under a car's sills, or under a man's arms: o.armIn 0.85); userData.carriage(t) gives the height.
  carLift(o) {
    const gap = o.gap ?? 2.6, g = grp(), carr = [];
    for (const sx of [-1, 1]) { g.add(at(box(0.26, 3.4, 0.32, '#C8322A', { outline: 0.01, pivot: 'bottom' }), sx * gap / 2, 0, 0), at(box(0.5, 0.06, 0.6, '#5A5F69'), sx * gap / 2, 0.03, 0));
      const c = grp(at(box(0.32, 0.36, 0.36, '#3A3D44', { outline: 0.006 }), 0, 0, 0), at(box(o.armIn ?? 0.85, 0.07, 0.1, '#F2C230', { outline: 0.005 }), -sx * (o.armIn ?? 0.85) / 2, -0.1, 0.12),
        at(box(o.armIn ?? 0.85, 0.07, 0.1, '#F2C230', { outline: 0.005 }), -sx * (o.armIn ?? 0.85) / 2, -0.1, -0.12)); c.position.set(sx * gap / 2, 0, 0); g.add(c); carr.push(c); }
    g.add(at(box(gap + 0.26, 0.16, 0.22, '#C8322A', { outline: 0.008 }), 0, 3.48, 0));
    const hAt = t => keyed(o.lift, t, o.h0 ?? 0.15);
    g.userData.update = t => { const y = hAt(t) + 0.02 * wob(t - (o.lift?.[o.lift.length - 1]?.[0] ?? 1e9) - 0.25, 30, 8); for (const c of carr) c.position.y = y + 0.18; };
    g.userData.carriage = hAt; g.userData.update(0); return g;
  },

  // A roller brake tester set in the floor, front +Z: a dark pit with two pairs of striped rollers across X (o.w 1.4), spinning at o.spin [[t, turns/s]]
  // (eased), a console with a dial and a red lamp (o.lampAt) at the side.
  brakeRollers(o) {
    const w = o.w ?? 1.4, g = grp(at(box(w + 0.3, 0.02, 1.1, '#2A2C31'), 0, 0.005, 0)), rollers = [];
    for (const z of [-0.2, 0.2]) { const r = grp(at(cyl(0.12, 0.12, w, '#6E747C', 12), 0, 0, 0, 0, 0, PI / 2)); for (let i = 0; i < 6; i++) r.add(at(box(w, 0.012, 0.03, '#F2C230'), 0, 0, 0, i * PI / 3, 0, 0).translateY(0.122));
      r.position.set(0, 0.06, z); g.add(r); rollers.push(r); }
    g.add(at(box(0.36, 1.1, 0.3, '#9AA1A9', { outline: 0.008, pivot: 'bottom' }), w / 2 + 0.6, 0, -0.2), at(cyl(0.12, 0.12, 0.02, '#F4F1E8', 16), w / 2 + 0.6, 0.85, -0.04, PI / 2, 0, 0));
    const [lOn, lOff] = [mat('#FF3B30', { emissive: '#FF3B30', noGrain: true }), mat('#6A2A2A')]; const lampOn = at(box(0.08, 0.08, 0.04, '', { material: lOn }), w / 2 + 0.6, 1.0, -0.04), lampOff = at(box(0.08, 0.08, 0.04, '', { material: lOff }), w / 2 + 0.6, 1.0, -0.04); g.add(lampOn, lampOff);
    const spins = o.spin || [];
    // (pass 2 of 46) a big lever on the console (o.leverAt: pulled down in 0.08 s) and white streaks over the rollers while they spin (gone when they stop)
    const lever = grp(at(box(0.04, 0.55, 0.04, '#3A3D44'), 0, 0.27, 0), at(cyl(0.06, 0.06, 0.06, '#D3202A', 10), 0, 0.56, 0)); lever.position.set(w / 2 + 0.6, 1.1, 0.02); lever.rotation.x = -0.5; g.add(lever);
    const sm = new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.75, depthWrite: false }), streaks = [-0.2, 0.2].flatMap(z => [0, 1, 2].map(i => { const q = new THREE.Mesh(new THREE.PlaneGeometry(w * (0.5 + 0.2 * i), 0.012), sm); q.rotation.x = -PI / 2; q.position.set((i - 1) * 0.15, 0.19, z + (i - 1) * 0.05); q.userData.noAO = true; g.add(q); return q; }));
    g.userData.update = t => { let a = 0, v = 0; for (let i = 0; i < spins.length; i++) { const [t0, r] = spins[i], t1 = spins[i + 1]?.[0] ?? Infinity; if (t <= t0) break; a += (Math.min(t, t1) - t0) * r; v = r; }
      for (const r of rollers) r.rotation.x = -a * TAU; const lit = o.lampAt != null && t >= o.lampAt && Math.floor((t - o.lampAt) * 6) % 2 === 0; lampOn.visible = lit; lampOff.visible = !lit;
      lever.rotation.x = o.leverAt != null && t >= o.leverAt ? -0.5 + 1.3 * clamp01((t - o.leverAt) / 0.08) : -0.5;
      streaks.forEach((q, i) => { q.visible = v > 2 && Math.floor(t * 20 + i) % 2 === 0; }); };
    g.userData.update(0); return g;
  },

  // A wall a man goes through, front +Z: a plain wall o.w (3.6) x o.h (3.2); at o.burstAt a hole in his shape appears (his outline, arms up, legs apart,
  // a tuft: drawn dark with ragged edges, o.holeX / o.holeY its middle) and bricks fly out toward -Z for 0.6 s.
  burstWall(o) {
    const w = o.w ?? 3.6, h = o.h ?? 3.2, g = grp(at(box(w, h, 0.2, o.color || '#D9D3C7', { outline: 0.008, pivot: 'bottom' }), 0, 0, -0.1));
    const hx = o.holeX ?? 0, hy = o.holeY ?? 1.15, S = o.holeScale ?? 1;
    const hole = at(canvasPlane(1.6 * S, 2.6 * S, (c, W, H) => { const k = W / 1.6; c.fillStyle = '#1B1A18'; const r = (x, y, ww, hh) => c.fillRect((x + 0.8) * k - ww * k / 2, H - (y + 1.3) * k - hh * k / 2, ww * k, hh * k);
      r(0, 1.0, 0.42, 0.52); r(0, 1.36, 0.16, 0.16); r(0, 0.45, 0.46, 0.62); r(-0.45, 0.7, 0.62, 0.12); r(0.45, 0.7, 0.62, 0.12); r(-0.78, 0.98, 0.12, 0.5); r(0.78, 0.98, 0.12, 0.5);
      r(-0.18, -0.25, 0.14, 0.82); r(0.18, -0.25, 0.14, 0.82); r(-0.26, -0.62, 0.3, 0.12); r(0.26, -0.62, 0.3, 0.12);
      for (let i = 0; i < 120; i++) { const a = rnd(i) * TAU, x = rnd(i + 3) * 1.4 - 0.7, y = rnd(i + 5) * 2.2 - 0.9; c.fillRect((x + 0.8) * k + Math.cos(a) * 4, H - (y + 1.3) * k + Math.sin(a) * 4, 5, 5); } },
      { res: 512, transparent: true }), hx, hy, 0.005);
    hole.visible = false; g.add(hole);
    const bricks = Array.from({ length: 14 }, (_, i) => { const b = box(0.16, 0.08, 0.1, i % 3 ? (o.color || '#D9D3C7') : '#B8B0A2', { outline: 0.004 }); b.visible = false; g.add(b); return b; });
    g.userData.update = t => { const u = o.burstAt == null ? -1 : t - o.burstAt; hole.visible = u >= 0;
      bricks.forEach((b, i) => { const life = u / 0.6; b.visible = u >= 0 && life < 1; if (!b.visible) return; const a = rnd(i) * TAU, sp = 1.2 + rnd(i + 2) * 1.6;
        b.position.set(hx + Math.cos(a) * 0.5 * S * life * sp, hy + Math.sin(a) * 0.6 * S * life * sp + 1.5 * life - 3.5 * life * life, -0.1 - 1.8 * life * sp * 0.5); b.rotation.set(life * 9 * rnd(i + 4), life * 7, life * 5 * rnd(i + 6)); }); };
    g.userData.update(0); return g;
  },

  // A garage bay for a technical inspection (use with the set whiteVoid), front +Z (the open side): a concrete floor o.w (8) x o.d (7) with yellow
  // lines, a back wall (z = -o.d / 2) and two side walls o.h (4.2) high, a blue band, a big sign o.sign ('CONTRÔLE TECHNIQUE') on the back wall at o.signY
  // (3.3), a tool board, a strip light; the back wall may be left out (o.back false: a burstWall stands there instead).
  garageBay(o) {
    const w = o.w ?? 8, d = o.d ?? 7, h = o.h ?? 4.2, g = grp(at(box(w, 0.06, d, '#8C8E8A'), 0, -0.022, 0)),   // (pass 3 of 46) the floor 8 mm up: level with the void's floor and under its shadow catcher it z-fought in stairs
      wall = o.wall || '#E3E1DA', band = o.band || '#2F5E9E';
    for (const x of [-1.6, 1.6]) g.add(at(box(0.08, 0.005, d - 0.4, '#E8C531', { noGrain: true }), x, 0.011, 0));
    if (o.back !== false) g.add(at(box(w, h, 0.2, wall, { pivot: 'bottom', outline: 0.008 }), 0, 0, -d / 2 - 0.1), at(box(w, 0.5, 0.21, band), 0, 1.0, -d / 2 - 0.1));
    for (const sx of [-1, 1]) g.add(at(box(0.2, h, d, wall, { pivot: 'bottom', outline: 0.008 }), sx * (w / 2 + 0.1), 0, 0), at(box(0.21, 0.5, d, band), sx * (w / 2 + 0.1), 1.0, 0));
    g.add(at(box(w + 0.4, 0.2, d, '#C9C7C0'), 0, h + 0.1, 0));
    const sy = o.signY ?? 3.3, sw = o.signW ?? 4.4, sx = o.signX ?? 0;   // (pass 2 of 46) o.signX: the sign moved along the wall (over the lift, clear of its posts)
    g.add(at(box(sw + 0.12, 0.62, 0.06, '#1E5BB8', { outline: 0.008 }), sx, sy, -d / 2 + 0.04), at(label(o.sign || 'CONTRÔLE TECHNIQUE', sw, 0.5, { bg: '#1E5BB8', fg: '#FFFFFF', wrap: false }), sx, sy, -d / 2 + 0.075));
    g.add(at(box(1.4, 0.9, 0.04, '#5A5F69', { outline: 0.006 }), -w / 2 + 1.1, 1.9, -d / 2 + 0.03));
    for (let i = 0; i < 9; i++) g.add(at(box(0.04, 0.22 + 0.1 * (i % 3), 0.03, ['#C8322A', '#F2C230', '#9AA1A9'][i % 3]), -w / 2 + 0.55 + i * 0.14, 1.9, -d / 2 + 0.06));
    g.add(at(box(2.4, 0.06, 0.18, '#F4F1E8', { emissive: '#FFF6DA', noGrain: true }), 0, h - 0.05, 0));
    return g;
  },

  // A yellow wheel chock (cale), front +Z, origin at its foot: a wedge 0.22 long, 0.12 high (o.s scale).
  wheelChock(o) {
    const s = o.s ?? 1, sh = new THREE.Shape([new THREE.Vector2(-0.11, 0), new THREE.Vector2(0.11, 0), new THREE.Vector2(-0.11, 0.12)].map(v => v.multiplyScalar(s)));
    const m = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: 0.12 * s, bevelEnabled: false }), mat(o.color || '#F2C230')); m.position.z = -0.06 * s; m.castShadow = true; m.receiveShadow = true;
    return grp(m, at(box(0.02 * s, 0.1 * s, 0.13 * s, '#2A2C31'), -0.1 * s, 0.05 * s, 0));
  },
};
