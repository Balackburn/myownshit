// « Le centime » (story 77): this man paid his taxes one cent too much; the state refunds it with a minister, the republican guard, a brass band and
// helicopters; the cent arrives on a velvet cushion and goes into his piggy bank; the next day, a bill of two million for travel expenses.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere } from './style.js';
import { grp, at } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const L = c => new THREE.MeshLambertMaterial({ color: c });

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
    const coin = at(cyl(0.022, 0.022, 0.004, '#E2B53C', 14, { outline: 0.002 }), 0, 0.33, -0.01); coin.rotation.x = PI / 2; coin.rotation.y = PI / 2; coin.visible = false; g.add(coin);
    g.scale.setScalar(s);
    const drops = o.dropAt || [];
    g.userData.update = t => {
      coin.visible = false; let jig = 0;
      for (const d of drops) { const u = t - d;
        if (u >= -0.12 && u < 0.22) { coin.visible = true; const f = clamp01(u / 0.22); coin.position.y = 0.33 - 0.09 * f * f; coin.rotation.z = u * 9; }
        if (u >= 0.2 && u < 0.7) jig = Math.max(jig, Math.exp(-(u - 0.2) * 8) * Math.sin((u - 0.2) * 34)); }
      body.scale.set(1 + 0.08 * jig, 1 - 0.1 * jig, 1 + 0.08 * jig); body.rotation.z = 0.06 * jig;
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
    const s = o.s ?? 1, g = grp(), chrome = '#D7DCE2', brass = '#D9A93A';
    const dome = new THREE.Mesh(new THREE.SphereGeometry(0.15, 14, 8, 0, TAU, 0, PI / 2), L(chrome)); dome.scale.set(1.0, 0.85, 1.1); g.add(dome);
    g.add(at(box(0.31, 0.02, 0.33, chrome, { outline: 0.004 }), 0, 0.0, 0.0));   // the rim
    g.add(at(box(0.035, 0.07, 0.3, brass, { outline: 0.003 }), 0, 0.14, 0.0));   // the crest
    for (let i = 0; i < 7; i++) { const st = at(box(0.03, 0.42, 0.012, '#151619'), (i - 3) * 0.012, -0.08, -0.17 - 0.004 * Math.abs(i - 3)); st.rotation.x = 0.35 + 0.02 * (i % 3); g.add(st); }   // the horsehair down the back
    g.add(at(cyl(0.022, 0.012, 0.22, '#C8222E', 8, { pivot: 'bottom' }), 0.13, 0.04, 0.03));   // the red plume
    g.scale.setScalar(s); return g;
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
};
