// « Le bocal » (story 78): this man could not open a jar of pickles; a spoon, hot water, the firemen's hydraulic jaws, an army tank, a space station, a laser, a
// museum; then his grandmother opens it with one hand; he does not like pickles.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere, addOutline } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const L = c => new THREE.MeshLambertMaterial({ color: c });
const keyAt = (keys, t, d) => { if (!keys || !keys.length) return d; if (t <= keys[0][0]) return keys[0][1]; for (let i = 1; i < keys.length; i++) { const [t1, v1] = keys[i]; if (t <= t1) { const [t0, v0] = keys[i - 1], u = clamp01((t - t0) / Math.max(1e-6, t1 - t0)), e = u * u * (3 - 2 * u); return v0 + (v1 - v0) * e; } } return keys[keys.length - 1][1]; };

export const BOCAL_PROPS = {
  // A jar of pickles (pivot at its bottom middle; o.s 1: 0.22 m tall): thick pale-green glass with a white glint, pale brine, five bumpy green
  // pickles standing in it, a ridged gold lid and a cream label (o.label, 'CORNICHONS'). o.openAt (s): the lid pops off, flies up spinning and lands
  // beside the jar; o.shake [[t0, t1], ...]: it rattles in place (someone wrestling with it); o.glint: the glint flashes (a laser bouncing off)
  // o.lidGone: the jar stands open, no lid (handed over after it was opened)
  // (review 1 of 78) o.lidArc (0.32) / o.lidFar (0.18) / o.lidFly (0.7 s): the popped lid's flight (a flick sends it high and far, out of the frame)
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
    // (review 2 of 78) o.hops [[t, amp], ...]: the ground shakes: the whole jar hops amp metres (before its scale) and its lid rattles shut;
    // o.lidGlow [[t0, t1], ...]: the lid glows red-hot (a laser on it); o.lidFace: the popped lid tumbles FACE-ON to the prop's front (+Z) along its arc
    // (edge-on, it read as a coin) and, with o.lidOut, keeps rising out of the frame instead of landing; o.lidSize (1): its size in flight;
    // o.lidZ (0.05): how far it comes forward
    const LY = 0.204, open = o.openAt, sh = o.shake || [], hp = o.hops || [], gw = o.lidGlow || [];
    const hot = new THREE.Mesh(new THREE.CylinderGeometry(0.086, 0.086, 0.034, 22), new THREE.MeshBasicMaterial({ color: '#FF5A2A', transparent: true, opacity: 0.0, depthWrite: false })); hot.renderOrder = 5; hot.visible = false; lid.add(hot);
    g.scale.setScalar(s);
    g.userData.update = t => {
      let jx = 0, jz = 0; for (const [a, b] of sh) if (t >= a && t < b) { jx = 0.004 * Math.sin(t * 71); jz = 0.003 * Math.sin(t * 53); }
      let hy = 0, ly = 0; for (const [a, amp] of hp) { const u = (t - a) / 0.2; if (u >= 0 && u < 1) { hy += amp * 4 * u * (1 - u); ly += amp * 0.9 * Math.sin(PI * Math.min(1, u * 1.6)) * (u < 0.62 ? 1 : 0); } }
      body.position.set(jx, hy, jz);
      if (open != null && t >= open) { const u = t - open, f = Math.min(1, u / (o.lidFly ?? 0.7)), sz = o.lidSize ?? 1;   // up, spinning, and down on the table beside the jar
        if (o.lidOut) lid.position.set((o.lidFar ?? 0.18) * f + jx, LY + (o.lidArc ?? 0.32) * (1 - (1 - f) * (1 - f)), (o.lidZ ?? 0.05) * f + jz);
        else lid.position.set((o.lidFar ?? 0.18) * f + jx, LY + (o.lidArc ?? 0.32) * Math.sin(PI * f) - (LY - 0.014) * f * f, (o.lidZ ?? 0.05) * f + jz);
        if (o.lidFace) lid.rotation.set(PI / 2 + 0.55 * Math.sin(u * 17), 0.35 * Math.sin(u * 11), u * 5); else lid.rotation.set(f < 1 ? u * 14 : 0, 0, f < 1 ? u * 9 : 0.03);
        lid.scale.setScalar(1 + (sz - 1) * Math.min(1, u / 0.08)); lid.userData.gone = !!o.lidOut && f >= 1; }
      else { lid.position.set(jx, LY + hy + ly, jz); lid.rotation.set(0, 0, 0); lid.scale.setScalar(1); lid.userData.gone = false; }
      const gk = gw.reduce((m, [a, b]) => Math.max(m, t >= a && t < b ? Math.min(1, (t - a) / 0.25) : 0), 0); hot.visible = gk > 0; hot.material.opacity = 0.8 * gk * (0.85 + 0.15 * Math.sin(t * 40)); hot.scale.setScalar(1 + 0.06 * gk);
      lid.visible = !o.lidGone && !lid.userData.gone;
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
    const lab = document.createElement('canvas'); lab.width = 256; lab.height = 64; const c = lab.getContext('2d'); c.fillStyle = '#C9A43E'; c.fillRect(0, 0, 256, 64); c.fillStyle = '#2A2016'; let fs = 30; c.font = `700 ${fs}px Arial`; while (c.measureText(o.text || '').width > 236 && fs > 10) { fs -= 1; c.font = `700 ${fs}px Arial`; } c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.text || '', 128, 34);   // (review 1 of 78) the text is fitted to the plate (it ran off it)
    const lt = new THREE.CanvasTexture(lab); lt.colorSpace = THREE.SRGBColorSpace; const lp = new THREE.Mesh(new THREE.PlaneGeometry(w * 0.7, w * 0.175), new THREE.MeshLambertMaterial({ map: lt })); lp.position.set(0, h * 0.82, w * 0.476); g.add(lp);
    const cover = grp(); for (let i = g.children.length - 1; i >= 1; i--) { const ch = g.children[i]; if (ch === lp) continue; cover.add(ch); } g.add(cover);
    // (review 2 of 78) o.liftH (0.6 m): how high the cover is lifted; o.noCover: the plinth alone, its glass already taken off (the shot after)
    g.userData.update = t => { const u = o.liftAt == null ? 0 : clamp01((t - o.liftAt) / (o.liftDur ?? 0.25)), v = o.liftAt == null || !o.coverAway ? 0 : clamp01((t - o.liftAt - (o.liftDur ?? 0.25) - 0.05) / 0.35);
      cover.position.set(0, (o.liftH ?? 0.6) * u * u * (3 - 2 * u) - 1.4 * v * v, -0.75 * v); cover.rotation.x = -0.5 * v; cover.visible = v < 1 && !o.noCover; };   // (review 1 of 78) o.coverAway: once lifted, the glass is put aside behind the plinth (it hung in mid-air)
    g.userData.update(-1); return g;
  },
  // (review 2 of 78) The firemen's BIG hydraulic jaws (pivot at the handle end, the jaws pointing +Z; o.s 1: 0.92 m long): a yellow body with a black
  // power pack, a grip handle on each side (local x = +-0.17, z = 0.12: where the two hands go) and a real jaw head: two steel arms in two segments
  // with teeth and hooked tips that close on the lid. o.open [[t, 0..1], ...]: how wide the tips are; o.bow [[t, 0..1], ...]: the arms bow outward
  // under the strain while the tips stay shut on the lid; o.breakAt (s): the arms snap off and fly apart, tumbling, with a puff
  bigJaws(o) {
    const s = o.s ?? 1, g = grp(), yel = '#E8C02A', blk = '#1E1F24', steel = '#AEB5BD', L1 = 0.22, L2 = 0.25;
    g.add(at(cyl(0.075, 0.085, 0.42, yel, 12, { outline: 0.006 }), 0, 0, 0.21, PI / 2), at(box(0.13, 0.1, 0.16, blk, { outline: 0.005 }), 0, 0.1, 0.16), at(box(0.05, 0.05, 0.07, '#C9CED4', { outline: 0.004 }), 0, 0, 0.44));
    for (const sd of [-1, 1]) g.add(at(box(0.1, 0.03, 0.03, blk), sd * 0.125, 0, 0.12), at(box(0.035, 0.035, 0.15, blk, { outline: 0.004 }), sd * 0.17, 0, 0.12));   // the two side grips
    g.add(at(box(0.16, 0.03, 0.03, '#C8322A'), 0, 0.0, 0.34));   // a red band
    const arms = [];
    for (const sd of [-1, 1]) { const p1 = grp(), p2 = grp(); p1.position.set(sd * 0.02, 0, 0.45);
      p1.add(at(box(0.05, 0.045, L1, steel, { outline: 0.005 }), 0, 0, L1 / 2)); p2.position.set(0, 0, L1); p1.add(p2);
      p2.add(at(box(0.046, 0.04, L2, steel, { outline: 0.005, taper: { x: 0.55, z: 1 }, taperAxis: 'z' }), 0, 0, L2 / 2));
      for (let i = 0; i < 4; i++) p2.add(at(box(0.016, 0.03, 0.022, '#5A6068'), -sd * 0.026, 0, 0.05 + i * 0.05, 0, sd * 0.5, 0));   // the teeth, on the inside
      p2.add(at(box(0.05, 0.045, 0.035, '#5A6068', { outline: 0.004 }), -sd * 0.022, 0, L2 - 0.005, 0, -sd * 0.7, 0));   // the hooked tip
      g.add(p1); arms.push({ p1, p2, sd }); }
    const puff = new THREE.Mesh(new THREE.IcosahedronGeometry(0.12, 1), new THREE.MeshLambertMaterial({ color: '#FFFFFF', flatShading: true })); addOutline(puff, 0.06); puff.position.set(0, 0, 0.8); puff.visible = false; g.add(puff);
    g.scale.setScalar(s);
    g.userData.update = t => {
      const k = keyAt(o.open, t, 0), bw = keyAt(o.bow, t, 0), br = o.breakAt != null && t >= o.breakAt ? t - o.breakAt : -1;
      const th = 0.1 + 0.5 * k, b = 0.3 * bw, tip = (L1 + L2) * Math.sin(th), th2 = Math.asin(Math.max(-1, Math.min(1, (tip - L1 * Math.sin(th + b)) / L2))) - (th + b);
      for (const a of arms) { if (br < 0) { a.p1.position.set(a.sd * 0.02, 0, 0.45); a.p1.rotation.set(0, a.sd * (th + b), 0); a.p2.rotation.set(0, a.sd * th2, 0); }
        else { a.p1.position.set(a.sd * (0.02 + 1.3 * br), 1.1 * br - 2.6 * br * br, 0.45 + 0.35 * br); a.p1.rotation.set(br * 9 * a.sd, a.sd * (0.6 + br * 2), br * 6); a.p2.rotation.set(0, -a.sd * 0.5, 0); } }
      puff.visible = br >= 0 && br < 0.4; if (puff.visible) { const u = br / 0.4; puff.scale.setScalar(u < 0.3 ? 0.4 + 4.5 * u : 1.75 * (1 - (u - 0.3) / 0.7)); }
    };
    g.userData.update(-1); return g;
  },

  // (review 2 of 78) A big spoon that folds (pivot at the top of its handle, hanging bowl-down along -Y; o.len 0.45 m): at o.foldAt its lower third
  // (neck and bowl) folds sideways (toward +X) to o.angle (1.5 rad, a right angle) with a springy overshoot, and the handle shivers; o.color
  bendSpoon(o) {
    const len = o.len ?? 0.45, g = grp(), c = o.color || '#C9CED4', hl = len * 0.62, bl = len - hl, up = grp(), low = grp(); g.add(up, low);
    up.add(at(box(len * 0.075, hl, len * 0.022, c, { outline: 0.012 }), 0, -hl / 2, 0)); up.add(at(box(len * 0.1, len * 0.1, len * 0.024, c, { outline: 0.012 }), 0, -len * 0.05, 0));
    low.position.set(0, -hl, 0); low.add(at(box(len * 0.06, bl * 0.42, len * 0.022, c, { outline: 0.012 }), 0, -bl * 0.21, 0));
    const bowl = new THREE.Mesh(new THREE.SphereGeometry(len * 0.13, 12, 8), new THREE.MeshLambertMaterial({ color: c, flatShading: true })); bowl.scale.set(1, 1.35, 0.42); bowl.position.set(0, -bl * 0.42 - len * 0.15, 0); addOutline(bowl, 0.05); low.add(bowl);
    g.userData.update = t => { const u = o.foldAt == null ? -1 : t - o.foldAt, A = o.angle ?? 1.5;
      low.rotation.z = u < 0 ? 0 : A * (1 - Math.exp(-u * 30)) * (1 + 0.28 * Math.exp(-u * 7) * Math.cos(u * 38));
      up.rotation.z = u < 0 || u > 0.5 ? 0 : 0.07 * Math.exp(-u * 8) * Math.sin(u * 90); };
    g.userData.update(-1); return g;
  },

  // (review 2 of 78) An army tank in metres (pivot on the ground under its middle, front +Z; 3.3 m wide, 4.8 m long, 2.3 m high): two track bands with
  // road wheels, an olive hull with a sloped front, a turret with a hatch, a white star and a LONG gun (2.9 m). o.gun [[t, rad], ...]: the gun's
  // pitch (positive: down); o.turret [[t, rad], ...]: the turret's turn; o.flat [[t, 0..1], ...]: the o.flatSide (1: +X) track goes flat, the hull
  // sinks on that side and the gun droops by o.droop (0.5 rad) more; o.rumble [[t0, t1, amp], ...]: the hull shudders on its tracks
  battleTank(o) {
    const c = o.color || '#66753E', c2 = '#56633A', d = '#2B2E22', g = grp(), hull = grp(), tracks = [];
    for (const sd of [-1, 1]) { const tk = grp(); tk.position.set(sd * 1.32, 0, 0);
      tk.add(at(box(0.62, 0.62, 4.1, d, { pivot: 'bottom', outline: 0.012 }), 0, 0.06, 0));
      for (const z of [-2.05, 2.05]) tk.add(at(cyl(0.34, 0.34, 0.62, d, 12), 0, 0.37, z, 0, 0, PI / 2));
      for (let i = 0; i < 5; i++) tk.add(at(cyl(0.27, 0.27, 0.08, '#8A9460', 10), sd * 0.3, 0.34, -1.6 + i * 0.8, 0, 0, PI / 2), at(cyl(0.1, 0.1, 0.1, d, 8), sd * 0.31, 0.34, -1.6 + i * 0.8, 0, 0, PI / 2));
      tk.add(at(box(0.72, 0.07, 4.5, c2, { outline: 0.008 }), 0, 0.74, 0));   // the mudguard
      g.add(tk); tracks.push({ tk, sd }); }
    hull.add(at(box(2.1, 0.62, 4.3, c, { pivot: 'bottom', outline: 0.012 }), 0, 0.42, 0), at(box(2.1, 0.5, 0.9, c, { outline: 0.01 }), 0, 0.82, 2.25, 0.6, 0, 0));
    const tur = grp(); tur.position.set(0, 1.04, -0.2); hull.add(tur);
    tur.add(at(box(1.5, 0.56, 1.8, c, { pivot: 'bottom', outline: 0.012, taper: { x: 0.8, z: 0.86 } }), 0, 0, 0), at(cyl(0.3, 0.32, 0.12, c2, 12, { pivot: 'bottom' }), 0.3, 0.56, -0.3), at(box(0.5, 0.05, 0.4, d), 0.3, 0.7, -0.3, -0.5, 0, 0));
    const gun = grp(); gun.position.set(0, 0.3, 0.85); tur.add(gun);
    gun.add(at(cyl(0.085, 0.11, 2.6, c, 10, { outline: 0.01 }), 0, 0, 1.3, PI / 2, 0, 0), at(cyl(0.15, 0.15, 0.34, d, 10), 0, 0, 2.72, PI / 2, 0, 0), at(box(0.5, 0.36, 0.3, c2, { outline: 0.008 }), 0, 0, 0.1));
    for (const sd of [-1, 1]) { const st = canvasPlane(0.5, 0.5, (cc, W, H) => { cc.clearRect(0, 0, W, H); cc.fillStyle = '#F4F1E8'; cc.beginPath(); for (let i = 0; i < 10; i++) { const a = -PI / 2 + i * PI / 5, rr = i % 2 ? W * 0.2 : W * 0.48; cc.lineTo(W / 2 + rr * Math.cos(a), H / 2 + rr * Math.sin(a)); } cc.closePath(); cc.fill(); }, { res: 128, transparent: true });
      st.rotation.y = sd * PI / 2; st.position.set(sd * 0.69, 0.28, 0.0); tur.add(st); }
    g.add(hull);
    const puff = new THREE.Mesh(new THREE.IcosahedronGeometry(0.42, 1), new THREE.MeshLambertMaterial({ color: '#FFFFFF', flatShading: true })); addOutline(puff, 0.05); puff.visible = false; g.add(puff);
    const fs = o.flatSide ?? 1;
    g.userData.update = t => {
      const f = keyAt(o.flat, t, 0); let ry = 0; for (const [a, b, amp] of o.rumble || []) if (t >= a && t < b) ry += (amp ?? 0.02) * Math.sin(t * 61);
      for (const T of tracks) { const k = T.sd === fs ? f : 0; T.tk.scale.set(1 + 0.22 * k, 1 - 0.55 * k, 1 + 0.03 * k); }
      hull.position.set(0, ry - 0.3 * f, 0); hull.rotation.set(0.006 * Math.sin(t * 53) * (ry ? 1 : 0), 0, -fs * 0.2 * f);
      tur.rotation.y = keyAt(o.turret, t, 0); gun.rotation.x = keyAt(o.gun, t, 0) + (o.droop ?? 0.5) * f;
      const fk = o.flat || []; let pk = 0; for (let i = 1; i < fk.length; i++) { const u = (t - fk[i - 1][0]) / 0.45; if (fk[i][1] > fk[i - 1][1] && u >= 0 && u < 1) pk = Math.max(pk, u < 0.3 ? u / 0.3 : 1 - (u - 0.3) / 0.7); }
      puff.visible = pk > 0.02; puff.position.set(fs * 1.95, 0.3 + 0.25 * pk, 0.6); puff.scale.setScalar(0.3 + 1.1 * pk);
    };
    g.userData.update(0); return g;
  },

  // (review 2 of 78) Drawn puffs of smoke or dust (pivot at their source): o.n (6) opaque white balls with an ink outline that swell, drift up and out
  // and shrink away over o.life (0.9 s). o.at (s): one burst; without it they come one after another for ever (o.every between two, default
  // life / n): a column that keeps rising. o.size (0.3 m), o.rise (0.8 m), o.spread (0.4 m), o.color
  toonPuff(o) {
    const n = o.n ?? 6, life = o.life ?? 0.9, g = grp(), m = new THREE.MeshLambertMaterial({ color: o.color || '#FFFFFF', flatShading: true }), balls = [];
    for (let i = 0; i < n; i++) { const b = new THREE.Mesh(new THREE.IcosahedronGeometry(o.size ?? 0.3, 1), m); addOutline(b, 0.05); b.visible = false; g.add(b); balls.push(b); }
    const every = o.every ?? life / n, hsh = i => { const x = Math.sin(i * 127.1 + 31.7) * 43758.5453; return x - Math.floor(x); };
    g.userData.update = t => { balls.forEach((b, i) => {
      let u; if (o.at != null) u = (t - o.at - i * 0.03) / life; else { const ph = (t - (o.startAt ?? 0) - i * every) / (n * every); u = t < (o.startAt ?? 0) + i * every ? -1 : (ph - Math.floor(ph)) * (n * every) / life; }
      if (u < 0 || u >= 1) { b.visible = false; return; }
      const a = hsh(i) * TAU, rr = (o.spread ?? 0.4) * (0.4 + 0.6 * hsh(i + 9)) * Math.sqrt(u), sc = (0.55 + 0.45 * hsh(i + 5)) * (u < 0.2 ? u / 0.2 : u > 0.6 ? 1 - (u - 0.6) / 0.4 : 1);
      b.visible = sc > 0.03; b.position.set(Math.cos(a) * rr, (o.rise ?? 0.8) * u * (0.6 + 0.4 * hsh(i + 3)), Math.sin(a) * rr * (o.flatZ ?? 1)); b.scale.setScalar(Math.max(0.03, sc)); b.rotation.set(u * 2 + i, u * 3, 0); }); };
    g.userData.update(-1); return g;
  },

  // (review 2 of 78) A big round window on space (pivot at its centre, facing +Z; o.r 1.0 m): black sky with stars, the blue curve of the Earth with
  // clouds along the bottom, a thick white ring with bolts. It glows by itself (the module's wall behind the astronauts was grey on grey)
  spaceWindow(o) {
    const R = o.r ?? 1.0, g = grp();
    const win = canvasPlane(2 * R, 2 * R, (c, W, H) => { c.clearRect(0, 0, W, H); c.save(); c.beginPath(); c.arc(W / 2, H / 2, W / 2, 0, TAU); c.clip(); c.fillStyle = '#03060F'; c.fillRect(0, 0, W, H);
      c.fillStyle = '#FFFFFF'; for (let i = 0; i < 70; i++) { const x = (i * 53 % 97) / 97 * W, y = (i * 31 % 89) / 89 * H * 0.7, q = 1 + (i % 3); c.fillRect(x, y, q, q); }
      const gr = c.createRadialGradient(W * 0.5, H * 1.55, H * 0.6, W * 0.5, H * 1.55, H * 1.0); gr.addColorStop(0, '#1F6FD0'); gr.addColorStop(0.9, '#3F97E6'); gr.addColorStop(0.97, '#9FD4FF'); gr.addColorStop(1, '#E8F6FF');
      c.fillStyle = gr; c.beginPath(); c.arc(W * 0.5, H * 1.55, H * 1.0, 0, TAU); c.fill();
      c.fillStyle = 'rgba(255,255,255,0.9)'; for (const [x, y, rx, ry] of [[0.3, 0.72, 0.13, 0.035], [0.62, 0.66, 0.1, 0.03], [0.5, 0.82, 0.16, 0.04], [0.8, 0.8, 0.08, 0.03]]) { c.beginPath(); c.ellipse(W * x, H * y, W * rx, H * ry, 0.1, 0, TAU); c.fill(); }
      c.fillStyle = '#4FA85A'; c.beginPath(); c.ellipse(W * 0.4, H * 0.9, W * 0.12, H * 0.05, 0.2, 0, TAU); c.fill(); c.restore(); }, { res: 512, emissive: 1.0, transparent: true });
    g.add(win); const ring = new THREE.Mesh(new THREE.TorusGeometry(R, R * 0.09, 8, 32), new THREE.MeshLambertMaterial({ color: '#F4F4F0', flatShading: true })); ring.position.z = 0.02; g.add(ring);
    for (let i = 0; i < 12; i++) { const a = i / 12 * TAU; g.add(at(cyl(R * 0.03, R * 0.03, 0.03, '#9AA3AC', 6), Math.cos(a) * R, Math.sin(a) * R, 0.1, PI / 2, 0, 0)); }
    return g;
  },

  // (review 2 of 78) A laser cannon on a tripod (pivot on the floor under it, the barrel pointing +Z at o.h 1.02 m): a grey-blue body with a coil,
  // a barrel and a red lens. o.charge [t0, t1]: it whines up: the body swells back, the coil and the lens brighten; o.fireAt (s): the kick: the whole
  // head jumps back and settles
  laserCannon(o) {
    const g = grp(), head = grp(), H = o.h ?? 1.02; head.position.y = H; g.add(head);
    for (let i = 0; i < 3; i++) { const a = i / 3 * TAU + 0.5, leg = at(box(0.045, H, 0.045, '#2E343A', { pivot: 'top' }), 0, H - 0.1, 0); leg.rotation.set(0.3 * Math.cos(a), 0, 0.3 * Math.sin(a)); g.add(leg); }
    const body = at(box(0.3, 0.26, 0.5, '#4A5560', { outline: 0.006 }), 0, 0, 0); head.add(body);
    const coils = []; for (let i = 0; i < 4; i++) { const cm = new THREE.MeshLambertMaterial({ color: '#D9A93A', flatShading: true, emissive: new THREE.Color('#FF7A2A'), emissiveIntensity: 0 }); const co = new THREE.Mesh(new THREE.TorusGeometry(0.075, 0.016, 6, 14), cm); co.position.set(0, 0.02, 0.32 + i * 0.07); head.add(co); coils.push(cm); }
    head.add(at(box(0.1, 0.1, 0.5, '#3A424A', { outline: 0.005 }), 0, 0.02, 0.5));
    const lm = new THREE.MeshLambertMaterial({ color: '#E8342A', flatShading: true, emissive: new THREE.Color('#FF2A1A'), emissiveIntensity: 0.3 }), lens = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.14, 0.03), lm); lens.position.set(0, 0.02, 0.76); head.add(lens);
    head.add(at(box(0.05, 0.08, 0.05, '#C8322A'), 0.1, 0.17, -0.12), at(box(0.2, 0.05, 0.12, '#2E343A'), 0, -0.15, 0));
    g.userData.update = t => { const ch = o.charge, k = ch ? clamp01((t - ch[0]) / Math.max(0.01, ch[1] - ch[0])) : 0, on = ch && t >= ch[0] && (o.fireAt == null || t < o.fireAt + 0.9) ? k : 0, u = o.fireAt == null ? -1 : t - o.fireAt;
      const sw = u < 0 ? on : Math.max(0, 1 - u / 0.15); body.scale.set(1 + 0.22 * sw, 1 + 0.22 * sw, 1 + 0.06 * sw); head.position.z = -0.06 * (u < 0 ? on : 0) - (u >= 0 ? 0.22 * Math.exp(-u * 9) * Math.cos(u * 22) : 0);
      head.rotation.x = u >= 0 ? -0.18 * Math.exp(-u * 8) * Math.cos(u * 20) : 0.01 * on * Math.sin(t * 80);
      coils.forEach((cm, i) => { cm.emissiveIntensity = u >= 0 && u < 0.9 ? 1.4 : 1.6 * clamp01(on * 4 - i); }); lm.emissiveIntensity = u >= 0 && u < 0.9 ? 2.2 : 0.3 + 1.2 * on; };
    g.userData.update(-1); return g;
  },

  // (review 2 of 78) A hexagonal nut (pivot at its centre, its hole along +X so that it rolls along Z; o.r 0.07 m)
  hexNut(o) {
    const r = o.r ?? 0.07, g = grp(at(cyl(r, r, r * 0.7, o.color || '#8E969C', 6, { outline: 0.02 }), 0, 0, 0, 0, 0, PI / 2), at(cyl(r * 0.45, r * 0.45, r * 0.72, '#2B2E33', 8), 0, 0, 0, 0, 0, PI / 2)); return g;
  },

  // (review 2 of 78) A camera flash (pivot at its centre; turn it to the camera): a white eight-pointed star that bursts at each time of o.at for
  // 0.13 s (o.w 0.5 m), with a point light for the instant
  camFlash(o) {
    const w = o.w ?? 0.5, g = grp(), ats = [].concat(o.at ?? []);
    const star = canvasPlane(w, w, (c, W, H) => { c.clearRect(0, 0, W, H); c.fillStyle = '#FFFFFF'; c.beginPath(); for (let i = 0; i < 16; i++) { const a = i * PI / 8, rr = i % 2 ? W * 0.14 : W * (i % 4 ? 0.36 : 0.5); c.lineTo(W / 2 + rr * Math.cos(a), H / 2 + rr * Math.sin(a)); } c.closePath(); c.fill(); }, { res: 128, emissive: 1.0, transparent: true });
    star.visible = false; g.add(star); const l = new THREE.PointLight('#FFFFFF', 0, 6, 1.2); g.add(l);
    g.userData.update = t => { let k = 0; for (const a of ats) { const u = (t - a) / 0.13; if (u >= 0 && u < 1) k = Math.max(k, u < 0.3 ? u / 0.3 : 1 - (u - 0.3) / 0.7); } star.visible = k > 0.02; star.scale.setScalar(0.3 + 0.9 * k); star.rotation.z = 0.4 * k; l.intensity = 5 * k; };
    g.userData.update(-1); return g;
  },

  // (review 2 of 78) Pebbles on a road (pivot at their middle, on the ground): o.n (7) small grey stones over o.w x o.d (1.2 x 0.8 m) that jump at
  // each [t, amp] of o.hops (the ground shaking under a tank), each a little late on the last
  roadPebbles(o) {
    const n = o.n ?? 7, g = grp(), st = [], hsh = i => { const x = Math.sin(i * 91.7 + 13.3) * 43758.5453; return x - Math.floor(x); };
    for (let i = 0; i < n; i++) { const r = 0.025 + 0.03 * hsh(i), b = sphere(r, ['#8E8A84', '#A39E96', '#6F6B66'][i % 3], 0); b.position.set((hsh(i + 3) - 0.5) * (o.w ?? 1.2), r * 0.7, (hsh(i + 7) - 0.5) * (o.d ?? 0.8)); b.userData.y0 = r * 0.7; b.userData.lag = 0.05 * hsh(i + 11); g.add(b); st.push(b); }
    g.userData.update = t => { for (const b of st) { let y = 0; for (const [a, amp] of o.hops || []) { const u = (t - a - b.userData.lag) / 0.24; if (u >= 0 && u < 1) y += amp * 4 * u * (1 - u); } b.position.y = b.userData.y0 + y; b.rotation.x = y * 30; } };
    g.userData.update(-1); return g;
  },

  // (review 2 of 78) Lab goggles (pivot at the bridge, attach to the 'head' joint): a dark rubber band round the head with two round tinted lenses
  labGoggles(o) {
    const g = grp(), r = o.r ?? 0.05, dx = o.dx ?? 0.055;
    g.add(at(box(0.25, 0.035, 0.2, '#2A2D33'), 0, 0, -0.085));
    for (const sd of [-1, 1]) { g.add(at(cyl(r, r, 0.03, '#2A2D33', 12, { outline: 0.03 }), sd * dx, 0, 0.0, PI / 2, 0, 0), at(cyl(r * 0.78, r * 0.78, 0.034, o.tint || '#E8B23A', 12, { emissive: o.tint || '#E8B23A' }), sd * dx, 0, 0.004, PI / 2, 0, 0)); }
    return g;
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
