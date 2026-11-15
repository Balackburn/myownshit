// « Le pull » (story 74): this man went out with his jumper inside out; nobody dared tell him; the whole country copied him, down to the president
// and the fashion shows; when he turned it right side out, the street turned round and the police arrested him for indecent dress. Conventions as
// in props.js (metres, front +Z, pivot as said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI;
const clamp01 = x => Math.max(0, Math.min(1, x));

// (review 1) The care label, one design everywhere (pivot at its bottom middle, 0.24 x 0.3 m at s 1: about half a head): pure white with a dark
// outline, a black wash-tub symbol and two lines of text, printed on both faces.
function careTag(s = 1) {
  const w = 0.24 * s, h = 0.3 * s, g = grp(at(box(w, h, 0.008 * s, '#FFFFFF', { outline: 0.006 }), 0, h / 2, 0));
  const print = () => canvasPlane(w * 0.96, h * 0.96, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.strokeStyle = '#17181C'; c.lineWidth = W * 0.05; c.strokeRect(W * 0.03, H * 0.03, W * 0.94, H * 0.94);
    c.lineWidth = W * 0.06; c.lineJoin = 'round'; c.beginPath(); c.moveTo(W * 0.16, H * 0.2); c.lineTo(W * 0.27, H * 0.52); c.lineTo(W * 0.73, H * 0.52); c.lineTo(W * 0.84, H * 0.2); c.stroke();   // the wash tub...
    c.lineWidth = W * 0.045; c.beginPath(); c.moveTo(W * 0.22, H * 0.31); for (let i = 1; i <= 8; i++) c.lineTo(W * (0.22 + 0.07 * i), H * (0.31 + (i % 2 ? 0.035 : -0.02))); c.stroke();   // ...its water
    c.fillStyle = '#17181C'; c.font = `900 ${H * 0.13}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('100 % LAINE', W / 2, H * 0.68); c.fillText('LAVAGE 30°', W / 2, H * 0.84); }, { res: 256 });
  const f = print(); f.position.set(0, h / 2, 0.0045 * s + 0.001); const b = print(); b.position.set(0, h / 2, -0.0045 * s - 0.001); b.rotation.y = PI; g.add(f, b);
  return g;
}
const kickOf = (ks, t) => { let a = 0; for (const tk of ks || []) { const v = t - tk; if (v >= 0) a += 0.55 * Math.exp(-5 * v) * Math.sin(24 * v); } return a; };

export const PULL_PROPS = {
  // A knitted jumper worn over the suit (attach to the torso joint; pivot at the bottom middle of the torso, front +Z): a knit shell o.w x o.h x o.d
  // (0.62 x 0.62 x 0.4) in o.color with ribbed collar and hem; o.inside (true): inside out: pale seams down the sides and the shoulders, the knit's
  // purl side (a flatter, paler tone) and the care label standing up above one shoulder; o.flipAt: it turns right side out at that time (a quick
  // squash as it does).
  // (review 1) the label: o.tag (1: its scale; 0 = none), o.tagSide (1 = the wearer's left shoulder, -1 the right), it sways (o.tagSway 0.07 rad at
  // o.tagRate 4.2 rad/s, o.tagPhase) and is kicked at each time of o.tagKick (a damped flop); o.tie false: no shirt-and-tie V painted on the
  // front (a shop's jumper); o.sewn (s): a label pops onto the chest at that time (sewn on the outside; o.sewnS 0.85 its scale); o.sleeves: two
  // empty sleeves hang from the shoulders (a jumper nobody is wearing);
  // o.turn { at, dur }: the jumper is pulled over the head and turned the other way: it rises and stretches over the head (the head and the arms
  // lost inside), bulges twice in the struggle, changes side half-way, snaps down with a squash and settles with a wobble; turned inside out, its
  // label springs up at the end with an overshoot and a flop.
  knitJumper(o) {
    const w = o.w ?? 0.62, h = o.h ?? 0.62, d = o.d ?? 0.4, C = new THREE.Color(o.color || '#C8322A'), g = grp(), body = grp(); g.add(body);
    const knit = (purl, front) => canvasPlane(w, h, (c, W, H) => { const base = purl ? C.clone().lerp(new THREE.Color('#FFFFFF'), 0.18) : C.clone(); c.fillStyle = base.getStyle(); c.fillRect(0, 0, W, H);
      c.strokeStyle = purl ? 'rgba(255,255,255,0.18)' : 'rgba(0,0,0,0.18)'; c.lineWidth = W * 0.012;
      for (let x = 0; x < 14; x++) for (let y = 0; y < 18; y++) { const cx = (x + 0.5) * W / 14, cy = (y + 0.5) * H / 18; c.beginPath();
        if (purl) { c.moveTo(cx - W * 0.025, cy); c.lineTo(cx + W * 0.025, cy); } else { c.moveTo(cx - W * 0.025, cy - H * 0.018); c.lineTo(cx, cy + H * 0.018); c.lineTo(cx + W * 0.025, cy - H * 0.018); } c.stroke(); }
      c.fillStyle = C.clone().multiplyScalar(0.8).getStyle(); c.fillRect(0, H * 0.9, W, H * 0.1); c.fillRect(W * 0.32, 0, W * 0.36, H * 0.05);
      c.strokeStyle = C.clone().multiplyScalar(0.62).getStyle(); c.lineWidth = W * 0.012; for (let x = 0; x < 16; x++) { c.beginPath(); c.moveTo((x + 0.5) * W / 16, H * 0.905); c.lineTo((x + 0.5) * W / 16, H); c.stroke(); }
      if (front && o.tie !== false) { c.fillStyle = '#F4F2EC'; c.beginPath(); c.moveTo(W * 0.3, 0); c.lineTo(W * 0.7, 0); c.lineTo(W * 0.5, H * 0.34); c.closePath(); c.fill();
        c.fillStyle = o.tie || '#B5202A'; c.beginPath(); c.moveTo(W * 0.47, 0); c.lineTo(W * 0.53, 0); c.lineTo(W * 0.54, H * 0.26); c.lineTo(W * 0.5, H * 0.32); c.lineTo(W * 0.46, H * 0.26); c.closePath(); c.fill();
        c.strokeStyle = C.clone().multiplyScalar(0.7).getStyle(); c.lineWidth = W * 0.035; c.beginPath(); c.moveTo(W * 0.29, 0); c.lineTo(W * 0.5, H * 0.35); c.lineTo(W * 0.71, 0); c.stroke(); }
      else if (front) { c.strokeStyle = C.clone().multiplyScalar(0.7).getStyle(); c.lineWidth = W * 0.04; c.beginPath(); c.arc(W * 0.5, 0, W * 0.16, 0, PI); c.stroke(); } }, { res: 256 });
    const S = o.tag ?? 1, side = o.tagSide ?? 1, tags = [];
    const mk = (inside) => { const s = grp(); s.add(at(box(w, h, d, C.clone().multiplyScalar(inside ? 1.1 : 1).getStyle(), { outline: 0.008 }), 0, h / 2, 0));
      const f = knit(inside, true); f.position.set(0, h / 2, d / 2 + 0.002); s.add(f); const b = knit(inside, false); b.position.set(0, h / 2, -d / 2 - 0.002); b.rotation.y = PI; s.add(b);
      s.add(at(box(w * 0.45, 0.05, d * 1.04, C.clone().multiplyScalar(0.8).getStyle()), 0, h - 0.02, 0));   // the collar rib
      if (o.sleeves) for (const sx of [-1, 1]) { const col = C.clone().multiplyScalar(inside ? 1.1 : 1).getStyle();   // empty sleeves hanging from the shoulders
        const sl = grp(at(box(0.17, h * 0.82, d * 0.7, col, { outline: 0.008 }), 0, -h * 0.41, 0), at(box(0.18, 0.06, d * 0.72, C.clone().multiplyScalar(0.8).getStyle()), 0, -h * 0.8, 0));
        sl.position.set(sx * (w / 2 + 0.05), h - 0.04, 0); sl.rotation.z = sx * 0.32; s.add(sl); }
      if (inside) {
        for (const sx of [-1, 1]) { s.add(at(box(0.022, h * 0.95, 0.022, '#FFFFFF'), sx * (w / 2 + 0.006), h / 2, d * 0.2), at(box(0.022, h * 0.95, 0.022, '#FFFFFF'), sx * (w / 2 + 0.006), h / 2, -d * 0.2));   // seams down the sides
          s.add(at(box(w * 0.3, 0.02, 0.02, '#FFFFFF'), sx * w * 0.3, h + 0.006, d * 0.2)); }   // and over the shoulders
        if (S > 0) { const tag = careTag(S); tag.position.set(side * (w / 2 - 0.02), h - 0.015, -d * 0.18); s.add(tag); tags.push(tag); }   // the care label, standing above one shoulder
        const sd = at(box(0.004, 0.12, 0.07, '#FFFFFF', { outline: 0.002 }), -side * (w / 2 + 0.01), h * 0.25, 0); s.add(sd); }
      return s; };
    const in0 = o.inside !== false, IN = mk(true), OUT = mk(false); body.add(IN, OUT);
    let sewn = null; if (o.sewn != null) { sewn = careTag(o.sewnS ?? 0.85); sewn.position.set(w * 0.1, h * 0.3, d / 2 + 0.012); sewn.rotation.z = -0.12; OUT.add(sewn); }
    const T = o.turn || null, tPop = T ? T.at + 0.8 * T.dur : -1e9, kicks = [...(o.tagKick || []), ...(T ? [tPop] : [])];
    g.userData.update = t => {
      let ins = in0; if (o.flipAt != null && t >= o.flipAt) ins = false; if (T && t >= T.at + 0.5 * T.dur) ins = !in0;
      IN.visible = ins; OUT.visible = !ins;
      let py = 0, sx = 1, sy = 1, sz = 1, rz = 0;
      if (o.flipAt != null) { const u = t - o.flipAt, a = u >= 0 && u < 0.25 ? Math.exp(-12 * u) * Math.cos(u * 40) : 0; sx += 0.15 * a; sy -= 0.15 * a; sz = sx; }
      if (T && t >= T.at) { const u = (t - T.at) / T.dur;
        if (u < 0.3) { const e = 1 - (1 - u / 0.3) * (1 - u / 0.3); py = h * e; sy = 1 + 0.75 * e; sx = 1 - 0.03 * e; sz = 1 + 0.45 * e; }
        else if (u < 0.68) { const q = (u - 0.3) / 0.38; py = h + 0.03 * Math.sin(q * 4 * PI); sy = 1.75 + 0.1 * Math.sin(q * 6 * PI); sx = 0.97 + 0.15 * Math.sin(q * 4 * PI); sz = 1.45 + 0.1 * Math.sin(q * 4 * PI + 1.6); rz = 0.09 * Math.sin(q * 4 * PI + 0.8); }
        else if (u < 0.8) { const e = (u - 0.68) / 0.12, e2 = e * e; py = h * (1 - e2); sy = 1.75 - 1.15 * e2; sx = 0.97 + 0.31 * e2; sz = 1.45 - 0.17 * e2; }
        else { const v = t - (T.at + 0.8 * T.dur), a = Math.exp(-9 * v) * Math.cos(30 * v); sy = 1 - 0.4 * a; sx = 1 + 0.28 * a; sz = sx; } }
      body.position.y = py; body.scale.set(sx, sy, sz); body.rotation.z = rz;
      for (const tag of tags) { const pop = T && !in0 ? (t < tPop ? 0.001 : 1 + 0.35 * Math.exp(-9 * (t - tPop)) * Math.cos(26 * (t - tPop))) : 1;
        tag.scale.setScalar(pop); tag.rotation.set(-0.12, 0, -side * 0.36 + (o.tagSway ?? 0.07) * Math.sin(t * (o.tagRate ?? 4.2) + (o.tagPhase ?? 0)) + kickOf(kicks, t)); }
      if (sewn) { const v = t - o.sewn; sewn.visible = v >= 0; if (v >= 0) sewn.scale.setScalar(1 + 0.4 * Math.exp(-10 * v) * Math.cos(28 * v)); }
    };
    g.userData.update(-1); return g;
  },

  // (review 1) The care label alone (pivot at its bottom middle): to stand on a collar that is no jumper's (a judge's robe). o.s its scale (1: 0.24 x
  // 0.3 m), it sways (o.sway 0.07, o.rate 4.2) and flops at each time of o.kick; o.lean (rad): its rest lean about Z.
  careLabel(o) {
    const g = grp(), tag = careTag(o.s ?? 1); g.add(tag);
    g.userData.update = t => { tag.rotation.set(-0.1, 0, (o.lean ?? 0) + (o.sway ?? 0.07) * Math.sin(t * (o.rate ?? 4.2)) + kickOf(o.kick, t)); };
    g.userData.update(0); return g;
  },

  // (review 1) An oversized sewing needle with its thread (attach to the hand; the needle points along +Y from the grip, 0.34 m at s 1): a steel
  // needle with an eye, and a red thread (o.color) that leaves the eye and hangs: it bends toward the ground whatever way the hand turns the
  // needle, and sways
  sewNeedle(o) {
    const s = o.s ?? 1, g = grp(at(cyl(0.005 * s, 0.02 * s, 0.34 * s, '#DCE1E6', 6, { outline: 0.006 }), 0, 0.12 * s, 0), at(box(0.05 * s, 0.07 * s, 0.012 * s, '#DCE1E6', { outline: 0.005 }), 0, -0.07 * s, 0));
    const n = 6, segs = Array.from({ length: n }, () => { const m = box(0.016 * s, 0.075 * s, 0.016 * s, o.color || '#C8322A'); g.add(m); return m; });
    const q = new THREE.Quaternion(), dn = new THREE.Vector3(), dir = new THREE.Vector3(), Y = new THREE.Vector3(0, 1, 0), p = new THREE.Vector3();
    g.userData.update = t => {
      g.getWorldQuaternion(q); dn.set(0, -1, 0).applyQuaternion(q.invert());   // the world's down, in the needle's own frame
      p.set(0, -0.1 * s, 0);
      segs.forEach((m, i) => { const k = (i + 1) / n; dir.set(0.3 * Math.sin(t * 6 + i * 0.7) * k, -1, 0).normalize().lerp(dn, Math.min(1, 0.3 + 0.9 * k)).normalize();
        m.position.copy(p).addScaledVector(dir, 0.0375 * s); m.quaternion.setFromUnitVectors(Y, dir); p.addScaledVector(dir, 0.075 * s); });
    };
    g.userData.update(0); return g;
  },

  // A shop's pile of jumpers on a table, labels out (pivot at the floor middle): o.n (8) folded jumpers of mixed colours, each with a white label on top
  jumperPile(o) {
    const n = o.n ?? 8, g = grp(), cols = ['#C8322A', '#2F62B5', '#2F8F6B', '#E8A33C', '#8E5AA8', '#F2C94E'];
    g.add(at(box(1.2, 0.75, 0.6, '#B98A5A', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0));
    for (let i = 0; i < n; i++) { const x = -0.38 + 0.38 * (i % 3), y = 0.75 + 0.07 * Math.floor(i / 3), c = cols[i % cols.length];
      g.add(at(box(0.34, 0.07, 0.3, c, { outline: 0.004 }), x, y + 0.035, 0), at(box(0.14, 0.004, 0.11, '#FFFFFF', { outline: 0.003 }), x, y + 0.073, 0.05)); }
    return g;
  },
};
