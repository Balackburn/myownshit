// « Le bocal » (story 78): this man could not open a jar of pickles; a spoon, hot water, the firemen's hydraulic jaws, an army tank, a space station, a laser, a
// museum; then his grandmother opens it with one hand; he does not like pickles.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere } from './style.js';
import { grp, at } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const L = c => new THREE.MeshLambertMaterial({ color: c });
const keyAt = (keys, t, d) => { if (!keys || !keys.length) return d; if (t <= keys[0][0]) return keys[0][1]; for (let i = 1; i < keys.length; i++) { const [t1, v1] = keys[i]; if (t <= t1) { const [t0, v0] = keys[i - 1], u = clamp01((t - t0) / Math.max(1e-6, t1 - t0)), e = u * u * (3 - 2 * u); return v0 + (v1 - v0) * e; } } return keys[keys.length - 1][1]; };

export const BOCAL_PROPS = {
  // A jar of pickles (pivot at its bottom middle; o.s 1: 0.22 m tall): thick pale-green glass with a white glint, pale brine, five bumpy green
  // pickles standing in it, a ridged gold lid and a cream label (o.label, 'CORNICHONS'). o.openAt (s): the lid pops off, flies up spinning and lands
  // beside the jar; o.shake [[t0, t1], ...]: it rattles in place (someone wrestling with it); o.glint: the glint flashes (a laser bouncing off)
  // o.lidGone: the jar stands open, no lid (handed over after it was opened)
  picklesJar(o) {
    const s = o.s ?? 1, g = grp(), body = grp(); g.add(body);
    const glass = new THREE.MeshLambertMaterial({ color: '#E4F2E2', transparent: true, opacity: 0.38, side: THREE.DoubleSide, depthWrite: false });
    const wall = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.075, 0.19, 20, 1, true), glass); wall.position.y = 0.095; wall.renderOrder = 3; body.add(wall);
    body.add(at(cyl(0.077, 0.077, 0.012, '#D8E8D4', 20, { outline: 0.004 }), 0, 0.006, 0));   // the base
    const brine = new THREE.Mesh(new THREE.CylinderGeometry(0.071, 0.071, 0.165, 18), new THREE.MeshLambertMaterial({ color: '#D9DB8A', transparent: true, opacity: 0.5, depthWrite: false })); brine.position.y = 0.094; body.add(brine);
    for (let i = 0; i < 5; i++) { const a = i / 5 * TAU + 0.4, r = i === 4 ? 0 : 0.038, pk = grp();
      pk.add(at(cyl(0.017, 0.015, 0.15, '#5E8C2E', 8, { pivot: 'bottom', outline: 0.003 }), 0, 0, 0));
      for (let j = 0; j < 4; j++) pk.add(at(sphere(0.006, '#7AA33E', 0), Math.cos(j * 1.7) * 0.015, 0.03 + j * 0.03, Math.sin(j * 1.7) * 0.015));   // the bumps
      pk.position.set(Math.cos(a) * r, 0.014, Math.sin(a) * r); pk.rotation.set(0.12 * Math.sin(a), 0, 0.12 * Math.cos(a)); body.add(pk); }
    const glint = at(box(0.012, 0.13, 0.004, '#FFFFFF'), -0.045, 0.1, 0.062); glint.rotation.y = -0.6; body.add(glint);
    body.add(at(new THREE.Mesh(new THREE.CylinderGeometry(0.0765, 0.0765, 0.07, 20, 1, true), L('#F3E6C2')), 0, 0.085, 0));   // the label band
    const lab = document.createElement('canvas'); lab.width = 256; lab.height = 64; const c = lab.getContext('2d'); c.fillStyle = '#F3E6C2'; c.fillRect(0, 0, 256, 64);
    c.fillStyle = '#2F6B2A'; c.font = '900 34px Arial'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.label || 'CORNICHONS', 128, 34);
    const lt = new THREE.CanvasTexture(lab); lt.colorSpace = THREE.SRGBColorSpace;
    const lp = new THREE.Mesh(new THREE.PlaneGeometry(0.11, 0.028), new THREE.MeshBasicMaterial({ map: lt, transparent: true })); lp.position.set(0, 0.085, 0.0775); body.add(lp);
    const lid = grp(at(cyl(0.08, 0.08, 0.028, '#D9A93A', 22, { outline: 0.004 }), 0, 0, 0)); for (let i = 0; i < 16; i++) { const a = i / 16 * TAU; lid.add(at(box(0.006, 0.026, 0.006, '#B8892A'), Math.cos(a) * 0.081, 0, Math.sin(a) * 0.081)); }
    lid.add(at(cyl(0.06, 0.06, 0.004, '#E8C55A', 18), 0, 0.015, 0)); g.add(lid);
    const LY = 0.204, open = o.openAt, sh = o.shake || [];
    g.scale.setScalar(s);
    g.userData.update = t => {
      let jx = 0, jz = 0; for (const [a, b] of sh) if (t >= a && t < b) { jx = 0.004 * Math.sin(t * 71); jz = 0.003 * Math.sin(t * 53); }
      body.position.set(jx, 0, jz);
      if (open != null && t >= open) { const u = t - open, f = Math.min(1, u / 0.7);   // up, spinning, and down on the table beside the jar
        lid.position.set(0.18 * f + jx, LY + 0.32 * Math.sin(PI * f) - (LY - 0.014) * f * f, 0.05 * f + jz); lid.rotation.set(f < 1 ? u * 14 : 0, 0, f < 1 ? u * 9 : 0.03); }
      else { lid.position.set(jx, LY, jz); lid.rotation.set(0, 0, 0); }
      lid.visible = !o.lidGone;
      glint.material.color.set(o.glint && o.glint.some(([a, b]) => t >= a && t < b) ? '#FFF6A0' : '#FFFFFF'); glint.scale.y = o.glint && o.glint.some(([a, b]) => t >= a && t < b) ? 1.4 : 1;
    };
    g.userData.update(-1); return g;
  },

  // The firemen's hydraulic jaws (pivot at the handle end, the jaws pointing +Z): a yellow body with two black handles, two tapered steel arms that
  // open by o.open [[t, 0..1], ...]; o.breakAt (s): the arms snap off and fly apart, tumbling, with a puff; o.s scale (1: 0.9 m long)
  rescueJaws(o) {
    const s = o.s ?? 1, g = grp(), yel = '#E8C02A';
    g.add(at(cyl(0.07, 0.08, 0.42, yel, 12, { outline: 0.006 }), 0, 0, 0.21, PI / 2), at(box(0.2, 0.03, 0.03, '#1E1F24'), 0, 0.09, 0.08), at(box(0.03, 0.12, 0.03, '#1E1F24'), 0, 0.03, 0.02));
    g.add(at(box(0.05, 0.05, 0.06, '#C9CED4', { outline: 0.004 }), 0, 0, 0.44));   // the hinge
    const arms = []; for (const sd of [-1, 1]) { const piv = grp(); piv.position.set(0, 0, 0.45); const arm = at(box(0.045, 0.03, 0.42, '#AEB5BD', { outline: 0.005, taper: { x: 0.35, z: 1 } }), 0, 0, 0.21); piv.add(arm, at(box(0.06, 0.012, 0.06, '#5A6068'), 0, 0, 0.4)); g.add(piv); arms.push({ piv, sd }); }
    const puff = new THREE.Mesh(new THREE.SphereGeometry(0.12, 10, 8), new THREE.MeshBasicMaterial({ color: '#F2F0EA', transparent: true, opacity: 0.85, depthWrite: false })); puff.position.set(0, 0, 0.5); puff.visible = false; g.add(puff);
    g.scale.setScalar(s);
    g.userData.update = t => {
      const k = keyAt(o.open, t, 0), br = o.breakAt != null && t >= o.breakAt ? t - o.breakAt : -1;
      for (const a of arms) { if (br < 0) { a.piv.position.set(0, 0, 0.45); a.piv.rotation.set(0, a.sd * (0.04 + 0.42 * k), 0); }
        else { a.piv.position.set(a.sd * 0.9 * br, 0.8 * br - 2.5 * br * br, 0.45 + 0.4 * br); a.piv.rotation.set(br * 9 * a.sd, a.sd * 0.5, br * 6); } }
      puff.visible = br >= 0 && br < 0.35; if (puff.visible) { puff.scale.setScalar(0.4 + 3 * br); puff.material.opacity = 0.85 * (1 - br / 0.35); }
    };
    g.userData.update(-1); return g;
  },

  // An astronaut's helmet (pivot at the neck, attach to the 'head' joint): a clear glass bubble with a white glint and a thick white collar ring
  spaceHelmet(o) {
    const r = o.r ?? 0.3, g = grp();
    const bub = new THREE.Mesh(new THREE.SphereGeometry(r, 20, 14), new THREE.MeshLambertMaterial({ color: '#E8F4FF', transparent: true, opacity: 0.22, depthWrite: false, side: THREE.DoubleSide })); bub.position.y = r * 0.82; bub.renderOrder = 4; g.add(bub);
    g.add(at(new THREE.Mesh(new THREE.TorusGeometry(r * 0.72, r * 0.12, 8, 24), L('#F4F4F2')), 0, 0.02, 0, PI / 2));
    const gl = at(box(r * 0.08, r * 0.5, 0.004, '#FFFFFF'), -r * 0.45, r * 1.05, r * 0.72); gl.rotation.z = 0.4; gl.rotation.y = -0.5; g.add(gl);
    return g;
  },

  // A museum display (pivot at the floor middle): a white plinth o.h (1.0) high, a glass cube on it (o.w, 0.45) with a thin brass frame, a little
  // brass label on the plinth's front (o.text); put the exhibit on top of the plinth inside the glass; o.liftAt (s): the glass cover rises 0.6 m
  displayCase(o) {
    const w = o.w ?? 0.45, h = o.h ?? 1.0, g = grp(at(box(w * 0.95, h, w * 0.95, '#F2EFE8', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0));
    const glass = new THREE.Mesh(new THREE.BoxGeometry(w, w, w), new THREE.MeshLambertMaterial({ color: '#E6F3FA', transparent: true, opacity: 0.2, depthWrite: false, side: THREE.DoubleSide })); glass.position.y = h + w / 2; glass.renderOrder = 4; g.add(glass);
    for (const [x, z] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) g.add(at(box(0.012, w, 0.012, '#C9A43E'), x * w / 2, h + w / 2, z * w / 2));
    for (const y of [h + 0.006, h + w]) for (const [x, z, ry] of [[0, -1, 0], [0, 1, 0], [-1, 0, PI / 2], [1, 0, PI / 2]]) { const b = at(box(w, 0.012, 0.012, '#C9A43E'), x * w / 2, y, z * w / 2); b.rotation.y = ry; g.add(b); }
    const lab = document.createElement('canvas'); lab.width = 256; lab.height = 64; const c = lab.getContext('2d'); c.fillStyle = '#C9A43E'; c.fillRect(0, 0, 256, 64); c.fillStyle = '#2A2016'; c.font = '700 30px Arial'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.text || '', 128, 34);
    const lt = new THREE.CanvasTexture(lab); lt.colorSpace = THREE.SRGBColorSpace; const lp = new THREE.Mesh(new THREE.PlaneGeometry(w * 0.7, w * 0.175), new THREE.MeshLambertMaterial({ map: lt })); lp.position.set(0, h * 0.82, w * 0.476); g.add(lp);
    const cover = grp(); for (let i = g.children.length - 1; i >= 1; i--) { const ch = g.children[i]; if (ch === lp) continue; cover.add(ch); } g.add(cover);
    g.userData.update = t => { const u = o.liftAt == null ? 0 : clamp01((t - o.liftAt) / 0.25); cover.position.y = 0.6 * u * u * (3 - 2 * u); };
    g.userData.update(-1); return g;
  },
  // (cycle 40) A stream of water falling from a tap's spout (origin at the spout's mouth, falling along -Y): o.len (0.3 m) down to where it lands,
  // o.r (0.012 m) thick at the mouth and thinner below, wobbling; drops splash where it lands; o.on [[t0, t1], ...]: when it runs (always by default)
  tapStream(o) {
    const len = o.len ?? 0.3, r = o.r ?? 0.012, g = grp();
    const sm = new THREE.MeshBasicMaterial({ color: o.color || '#CFEFFF', transparent: true, opacity: o.opacity ?? 0.85, depthWrite: false });
    const s = new THREE.Mesh(new THREE.CylinderGeometry(r, r * 0.75, len, 8, 1, true), sm); s.position.y = -len / 2; s.userData.noAO = true; g.add(s);
    const dm = new THREE.MeshBasicMaterial({ color: '#E8F8FF', transparent: true, opacity: 0.9, depthWrite: false });
    const drops = Array.from({ length: 10 }, () => { const d = new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.012, 0.012), dm); d.userData.noAO = true; g.add(d); return d; });
    const ons = Array.isArray(o.on?.[0]) ? o.on : [o.on || [-1e9, 1e9]];
    g.userData.update = t => {
      const on = ons.some(([a, b]) => t >= a && t < b); s.visible = on; s.scale.set(1 + 0.15 * Math.sin(t * 47), 1, 1 + 0.15 * Math.cos(t * 41));
      drops.forEach((d, i) => { const ph = (t * 2.6 + i * 0.137) % 1, a = i * 2.4; d.visible = on; d.position.set(Math.cos(a) * 0.08 * ph, -len + 0.24 * ph * (1 - ph), Math.sin(a) * 0.08 * ph); });
    };
    g.userData.update(0); return g;
  },
};
