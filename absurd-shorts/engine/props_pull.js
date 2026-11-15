// « Le pull » (story 74): this man went out with his jumper inside out; nobody dared tell him; the whole country copied him, down to the president
// and the fashion shows; when he turned it right side out, the street turned round and the police arrested him for indecent dress. Conventions as
// in props.js (metres, front +Z, pivot as said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI;

export const PULL_PROPS = {
  // A knitted jumper worn over the suit (attach to the torso joint; pivot at the bottom middle of the torso, front +Z): a knit shell o.w x o.h x o.d
  // (0.52 x 0.62 x 0.32) in o.color with ribbed collar, hem and armholes; o.inside (true): inside out: pale seams down the sides and the shoulders, the
  // knit's purl side (a flatter, paler tone) and a big white care label sticking up out of the back of the collar; o.flipAt: it turns right side out
  // at that time (a quick squash as it does)
  knitJumper(o) {
    const w = o.w ?? 0.52, h = o.h ?? 0.62, d = o.d ?? 0.32, C = new THREE.Color(o.color || '#C8322A'), g = grp();
    const knit = (purl) => canvasPlane(w, h, (c, W, H) => { const base = purl ? C.clone().lerp(new THREE.Color('#FFFFFF'), 0.18) : C.clone(); c.fillStyle = base.getStyle(); c.fillRect(0, 0, W, H);
      c.strokeStyle = purl ? 'rgba(255,255,255,0.18)' : 'rgba(0,0,0,0.18)'; c.lineWidth = W * 0.012;
      for (let x = 0; x < 14; x++) for (let y = 0; y < 18; y++) { const cx = (x + 0.5) * W / 14, cy = (y + 0.5) * H / 18; c.beginPath();
        if (purl) { c.moveTo(cx - W * 0.025, cy); c.lineTo(cx + W * 0.025, cy); } else { c.moveTo(cx - W * 0.025, cy - H * 0.018); c.lineTo(cx, cy + H * 0.018); c.lineTo(cx + W * 0.025, cy - H * 0.018); } c.stroke(); }
      c.fillStyle = C.clone().multiplyScalar(0.8).getStyle(); c.fillRect(0, H * 0.9, W, H * 0.1); c.fillRect(W * 0.32, 0, W * 0.36, H * 0.05); }, { res: 256 });
    const mk = (inside) => { const s = grp(); s.add(at(box(w, h, d, C.clone().multiplyScalar(inside ? 1.1 : 1).getStyle(), { outline: 0.008 }), 0, h / 2, 0));
      const f = knit(inside); f.position.set(0, h / 2, d / 2 + 0.002); s.add(f); const b = knit(inside); b.position.set(0, h / 2, -d / 2 - 0.002); b.rotation.y = PI; s.add(b);
      s.add(at(box(w * 0.45, 0.05, d * 1.04, C.clone().multiplyScalar(0.8).getStyle()), 0, h - 0.02, 0));   // the collar rib
      if (inside) {
        for (const sx of [-1, 1]) { s.add(at(box(0.012, h * 0.95, 0.012, '#F4F1E8'), sx * (w / 2 + 0.004), h / 2, d * 0.2), at(box(0.012, h * 0.95, 0.012, '#F4F1E8'), sx * (w / 2 + 0.004), h / 2, -d * 0.2));   // seams down the sides
          s.add(at(box(w * 0.3, 0.012, 0.012, '#F4F1E8'), sx * w * 0.3, h + 0.004, d * 0.2)); }   // and over the shoulders
        const tag = at(box(0.11, 0.09, 0.004, '#FFFFFF', { outline: 0.003 }), 0, h + 0.05, -d / 2 + 0.01); tag.rotation.x = -0.35; s.add(tag);   // the care label up out of the collar
        const side = at(box(0.004, 0.12, 0.07, '#FFFFFF', { outline: 0.002 }), w / 2 + 0.01, h * 0.25, 0); s.add(side); }
      return s; };
    const IN = mk(o.inside !== false), OUT = mk(false); g.add(IN, OUT);
    g.userData.update = t => { const f = o.flipAt != null && t >= o.flipAt; IN.visible = (o.inside !== false) && !f; OUT.visible = !IN.visible;
      if (o.flipAt != null) { const u = t - o.flipAt, a = u >= 0 && u < 0.25 ? Math.exp(-12 * u) * Math.cos(u * 40) : 0; g.scale.set(1 + 0.15 * a, 1 - 0.15 * a, 1 + 0.15 * a); } };
    g.userData.update(-1); return g;
  },

  // A shop's pile of jumpers on a table, labels out (pivot at the floor middle): o.n (8) folded jumpers of mixed colours, each with a white label on top
  jumperPile(o) {
    const n = o.n ?? 8, g = grp(), cols = ['#C8322A', '#2F62B5', '#2F8F6B', '#E8A33C', '#8E5AA8', '#F2C94E'];
    g.add(at(box(1.2, 0.75, 0.6, '#B98A5A', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0));
    for (let i = 0; i < n; i++) { const x = -0.38 + 0.38 * (i % 3), y = 0.75 + 0.07 * Math.floor(i / 3), c = cols[i % cols.length];
      g.add(at(box(0.34, 0.07, 0.3, c, { outline: 0.004 }), x, y + 0.035, 0), at(box(0.1, 0.004, 0.08, '#FFFFFF'), x, y + 0.072, 0.05)); }
    return g;
  },
};
