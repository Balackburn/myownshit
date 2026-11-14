// « Le bâillement » (story 58, cycle 20): a man yawned too hard and his jaw fell to the ground; it never went back up; the town hall classed it as a
// slide; on Sundays there is a queue; the postman drops the mail in it; yesterday he shut his mouth, with the postman inside; he gets his mail from
// the inside. Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { mat, box, cyl, sphere, addOutline } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI;
const list = v => [].concat(v ?? []);
// a value keyed in time: [[t, v], ...], linear between keys, held before the first and after the last
function lin(ks, t, dflt) {
  const k = list(ks); if (!k.length) return dflt;
  if (t <= k[0][0]) return k[0][1];
  for (let i = 1; i < k.length; i++) if (t < k[i][0]) { const [t0, v0] = k[i - 1], [t1, v1] = k[i]; return v0 + (v1 - v0) * (t - t0) / Math.max(1e-6, t1 - t0); }
  return k[k.length - 1][1];
}
// a point keyed in time: [[t, x, y, z], ...], linear between keys
function linP(ks, t) {
  const k = list(ks); if (!k.length) return [0, 0, 0];
  if (t <= k[0][0]) return k[0].slice(1);
  for (let i = 1; i < k.length; i++) if (t < k[i][0]) { const a = k[i - 1], b = k[i], u = (t - a[0]) / Math.max(1e-6, b[0] - a[0]); return [1, 2, 3].map(j => a[j] + (b[j] - a[j]) * u); }
  return k[k.length - 1].slice(1);
}

export const BAILLEMENT_PROPS = {
  // A tongue laid on the ground as a slide (pivot at its root, on the ground, running out along +Z): pink, o.w (0.24) wide and o.len (1.5) long, a
  // darker groove down its middle and a tip that curls up; o.unroll [[t, 0..1]]: how much of it has rolled out, the rest a roll at its end that
  // travels out like a carpet's.
  tongueSlide(o) {
    const w = o.w ?? 0.24, L = o.len ?? 1.5, pink = o.color || '#E0717F', g = grp();
    const strip = new THREE.Mesh(new THREE.BoxGeometry(w, 0.03, 1).translate(0, 0.015, 0.5), mat(pink)); addOutline(strip, 0.04); g.add(strip);
    const groove = new THREE.Mesh(new THREE.BoxGeometry(w * 0.12, 0.032, 1).translate(0, 0.016, 0.5), mat('#B9505E')); g.add(groove);
    const tip = grp(at(new THREE.Mesh(new THREE.CylinderGeometry(w / 2, w / 2, 0.03, 16, 1, false, 0, PI).rotateZ(PI / 2).rotateY(PI / 2), mat(pink)), 0, 0.015, 0));
    g.add(tip);
    const roll = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, w * 0.98, 14).rotateZ(PI / 2), mat(pink)); addOutline(roll, 0.06); g.add(roll);
    g.userData.update = t => {
      const u = Math.max(0.02, Math.min(1, lin(o.unroll, t, 1))), Lu = L * u, rr = 0.025 + 0.07 * (1 - u);
      strip.scale.z = Lu; groove.scale.z = Lu * 0.92;
      roll.visible = u < 0.999; roll.scale.setScalar(1); roll.scale.set(1, rr, rr); roll.position.set(0, rr, Lu);
      tip.visible = u >= 0.999; tip.position.set(0, 0, Lu); tip.rotation.x = -0.5;   // the tip curls up once it is all out
    };
    g.userData.update(0); return g;
  },

  // A letter (pivot at its centre, face +Z): a white envelope o.w (0.17) wide, its flap drawn as a V, a red stamp in its corner.
  envelope(o) {
    const w = o.w ?? 0.17, h = w * 0.64, g = grp(at(box(w, h, 0.006, o.color || '#F7F5EE', { outline: 0.02 }), 0, 0, 0));
    for (const s of [-1, 1]) g.add(at(box(w * 0.58, 0.006, 0.008, '#B8B2A4'), s * w * 0.24, h * 0.18, 0.004, 0, 0, s * -0.5));
    g.add(at(box(w * 0.18, w * 0.18, 0.008, '#D23A2E'), w * 0.36, h * 0.3, 0.005));
    return g;
  },

  // A postman's satchel (pivot at the top of its strap, hung on a shoulder: the bag at the hip): a yellow leather bag with its flap, a dark strap,
  // letters sticking out of it.
  mailBag(o) {
    const c = o.color || '#E8B92E', g = grp(at(box(0.34, 0.25, 0.11, c, { outline: 0.012 }), 0, -0.72, 0.0), at(box(0.35, 0.1, 0.12, '#C99A1E'), 0, -0.63, 0.002),
      at(box(0.035, 0.75, 0.012, '#3A2A1E'), -0.08, -0.33, -0.05, 0, 0, 0.35));
    for (let i = 0; i < 3; i++) g.add(at(box(0.15, 0.1, 0.004, '#F7F5EE', { outline: 0.01 }), -0.08 + i * 0.07, -0.56 + (i % 2) * 0.02, -0.02 + i * 0.012, 0, 0, (i - 1) * 0.2));
    return g;
  },

  // Something moving inside a belly (pivot where it is attached, usually the torso): a bulge of cloth the colour of the suit, o.r (0.13) wide, with
  // an ink outline; o.path [[t, x, y, z], ...] where it is (in the frame of what it is attached to), o.size [[t, s]] how far it pushes out (0..1.5):
  // a knee, a fist, a head pushing against the cloth from inside.
  bellyBulge(o) {
    // (pass 3 of 58) the default is the jacket's own navy (suitNavy), with a thin outline and four creases fanning out from it: a lighter blue read as a
    // blue ball stuck on him (9,40,95 against 1,15,32), navy with a thick ink outline as a ball too: the creases make it the cloth pushed out
    const r = o.r ?? 0.13, c = o.color || '#1F3550', m = sphere(r, c, 1); m.scale.set(1, 1.15, 0.7); addOutline(m, o.outline ?? 0.025);
    const g = grp(m), creases = grp(); g.add(creases);
    for (let i = 0; i < 4; i++) { const a = PI / 4 + i * PI / 2, cr = at(box(r * 0.9, 0.006, 0.006, '#0B1626'), Math.cos(a) * r * 1.25, Math.sin(a) * r * 1.25, r * 0.12, 0, 0, a); creases.add(cr); }
    if (o.fist) for (let i = 0; i < 4; i++) m.add(at(sphere(r * 0.24, c, 1), (i - 1.5) * r * 0.42, r * 0.25, r * 0.86));
    g.userData.update = t => { const p = linP(o.path, t), s = Math.max(0.001, lin(o.size, t, 1)); m.position.set(p[0], p[1], p[2]); m.scale.set(s, s * 1.15, s * 0.7); m.visible = s > 0.02;
      creases.position.set(p[0], p[1], p[2]); creases.scale.setScalar(s); creases.visible = m.visible; };
    g.userData.update(0); return g;
  },

  // A ribbon for an opening (pivot at the floor in its middle, across X): two little posts o.w (1.2) apart and a red ribbon between them at o.h
  // (0.95) with a bow in its middle; o.cutAt: from that time the two halves drop and swing down from their posts.
  ribbonCut(o) {
    const w = o.w ?? 1.2, h = o.h ?? 0.95, g = grp(), red = '#D2282E';
    for (const s of [-1, 1]) g.add(at(cyl(0.035, 0.045, h + 0.08, '#C8B07A', 8, { pivot: 'bottom' }), s * w / 2, 0, 0), at(sphere(0.05, '#C8B07A', 1), s * w / 2, h + 0.1, 0));
    const halves = [-1, 1].map(s => { const hg = grp(at(box(w / 2, 0.06, 0.008, red, { outline: 0.02 }), -s * w / 4, 0, 0)); hg.position.set(s * w / 2, h, 0); g.add(hg); return { hg, s }; });
    const bow = grp(at(box(0.12, 0.09, 0.02, red, { outline: 0.02 }), -0.06, 0, 0, 0, 0, 0.5), at(box(0.12, 0.09, 0.02, red, { outline: 0.02 }), 0.06, 0, 0, 0, 0, -0.5)); bow.position.set(0, h, 0.01); g.add(bow);
    g.userData.update = t => {
      const u = o.cutAt == null ? -1 : t - o.cutAt;
      for (const { hg, s } of halves) { const a = u < 0 ? 0 : Math.min(1.35, u * 9) - 0.18 * Math.sin(Math.max(0, u - 0.15) * 11) * Math.exp(-Math.max(0, u - 0.15) * 3); hg.rotation.z = s * a; }
      bow.visible = u < 0; };
    g.userData.update(0); return g;
  },

  // Giant ceremonial scissors (pivot at their screw, the blades along +X): silver blades, red handles (o.handle: (pass 3 of 58) dark ones, the red handles
  // merged with the sash and the ribbon); o.snip [[t, 0..1]]: 1 open, 0 shut; o.open (0.35 rad): how far each blade opens.
  bigScissors(o) {
    const L = o.len ?? 0.5, g = grp(), mk = s => { const b = grp(at(box(L, 0.035, 0.012, '#D9DEE3', { outline: 0.02 }), L / 2, 0, 0), at(cyl(0.07, 0.07, 0.02, o.handle || '#C23A30', 12), -0.1, -s * 0.05, 0, PI / 2, 0, 0)); g.add(b); return b; };
    const a = mk(1), b = mk(-1); g.add(at(sphere(0.02, '#8A9097', 1), 0, 0, 0.012));
    g.userData.update = t => { const op = Math.max(0, Math.min(1, lin(o.snip, t, 1))) * (o.open ?? 0.35); a.rotation.z = op; b.rotation.z = -op; };
    g.userData.update(0); return g;
  },

  // A knitted cap lying loose (pivot at its rim's middle): a dome o.color ('#F2C230') with a turned-up band and a bobble: the postman's, left behind.
  // (pass 3 of 58) knitted: vertical ribs painted on the dome and a thicker turned-up cuff with its own ribs (smooth, it read as a hard hat)
  beanieHat(o) {
    const c = new THREE.Color(o.color || '#F2C230'), dk = c.clone().multiplyScalar(0.72), hex = '#' + c.getHexString(), dhex = '#' + dk.getHexString();
    const rib = (n, vertical) => { const cv = document.createElement('canvas'); cv.width = cv.height = 128; const x = cv.getContext('2d'); x.fillStyle = hex; x.fillRect(0, 0, 128, 128); x.fillStyle = dhex;
      for (let i = 0; i < n; i++) { if (vertical) x.fillRect(i * 128 / n, 0, 128 / n * 0.35, 128); else x.fillRect(0, i * 128 / n, 128, 128 / n * 0.3); }
      const tx = new THREE.CanvasTexture(cv); tx.colorSpace = THREE.SRGBColorSpace; return tx; };
    const dome = new THREE.Mesh(new THREE.SphereGeometry(0.11, 16, 8, 0, 2 * PI, 0, PI / 2), new THREE.MeshLambertMaterial({ map: rib(18, true), flatShading: true })); addOutline(dome, 0.05); dome.scale.set(1, 1.05, 1);
    const cuffTex = rib(18, true), cuff = new THREE.Mesh(new THREE.CylinderGeometry(0.122, 0.118, 0.065, 18), new THREE.MeshLambertMaterial({ map: cuffTex, color: '#D8D8D8', flatShading: true })); addOutline(cuff, 0.04);
    // (final pass of 58) o.boxy: the rig's own beanie (a tapered box, human.js) with the ribs and a cuff: the round one did not match the cap he wore
    if (o.boxy) { const bw = o.boxy[0] ?? 0.3, bh = o.boxy[1] ?? 0.12, bd = o.boxy[2] ?? 0.32, bm = new THREE.MeshLambertMaterial({ map: rib(14, true), flatShading: true });
      const top = box(bw, bh, bd, hex, { pivot: 'bottom', taper: 0.8, material: bm, outline: 0.03 }), band = box(bw * 1.04, bh * 0.32, bd * 1.04, dhex, { pivot: 'bottom', outline: 0.03 });
      return grp(top, band); }
    const g = grp(dome, at(cuff, 0, 0.02, 0)); if (o.bobble !== false) g.add(at(sphere(0.035, '#FFFFFF', 1), 0, 0.12, 0));   // (pass 2 of 58) o.bobble false: the cap he wore had none
    return g;
  },

  // A mayor's sash (pivot at the joint it is attached to, the chest): a band of blue, white and red worn from the right shoulder to the left hip,
  // o.w (0.13) wide, o.len (0.75) long, standing o.z (0.13) in front of the joint.
  mayorSash(o) {
    const w = o.w ?? 0.13, L = o.len ?? 0.75, g = grp(), b = grp();
    // (final pass of 58) blue nearest the collar (red was), gold fringed tassels at the hip
    (o.flip === false ? ['#1F3E99', '#F4F4F2', '#D2282E'] : ['#D2282E', '#F4F4F2', '#1F3E99']).forEach((c, i) => b.add(at(box(w / 3, L, 0.012, c, i === 1 ? {} : { outline: 0.01 }), (i - 1) * w / 3, 0, 0)));
    for (let i = 0; i < 2; i++) { b.add(at(box(w * 0.5, 0.05, 0.02, '#D9B44A', { outline: 0.02 }), (i - 0.5) * w * 0.5, -L / 2 - 0.02, 0.004)); for (let j = 0; j < 4; j++) b.add(at(box(0.008, 0.07, 0.008, '#C9A23E'), (i - 0.5) * w * 0.5 + (j - 1.5) * 0.014, -L / 2 - 0.08, 0.004)); }
    b.rotation.z = o.tilt ?? 0.62; b.position.set(0, o.y ?? -0.1, o.z ?? 0.13); g.add(b);
    return g;
  },
};
