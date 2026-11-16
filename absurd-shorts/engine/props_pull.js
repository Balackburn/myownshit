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
  // (review 2) one action of the label per shot: o.tagPop (s): hidden until then, it springs up out of the collar with a stretch and a flop (a
  // colleague who stops, a wave across an office); o.tagRise { at, dur }: it rises slowly out of the collar, like a flag hoisted (a president);
  // o.tagHop (m): it hops at each step (|sin| of half o.tagRate, o.tagPhase), stretching as it goes up; o.tagKickAmp (1): how hard the kicks flop it;
  // o.popS / o.popAmp / o.popDecay / o.popFreq: after a turn the label comes back o.popS times bigger with o.popAmp of stretch that dies at
  // o.popDecay and rings at o.popFreq (1, 0.35, 9, 26: one flop; 1.5, 0.6, 3.6, 19: it shoots up and boings three times);
  // o.turn.amp (1): how far the jumper stretches and bulges over the head (0.45: one flat, resigned yank); o.tagLean (0.36 rad): how far the label
  // leans away from the wearer's head at rest (0.05: upright, beside a neighbour's head)
  // (final pass) o.tagSag { at, dur, amp }: the label sags slowly from that time, leaning further out (amp rad, 0.35) and a little shorter (the last
  // word); o.under (a colour, '#1F3550'): a suit front (jacket, white shirt V, red tie) under the jumper, seen while a turn lifts the jumper (one red
  // knit turning into another read as nothing); o.turn.bulges: in the struggle the jumper bulges twice, one lump on each side, with a still beat
  // between them (a sine wobble read as three frames of noise); o.sewnSteps [t...]: the sewn label is there loose from o.sewn, tilted and hanging
  // off its spot, and each step (a stitch) pulls it a share of the way flat into place, with a small snap
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
    let UNDER = null; if (o.under) { const uw = w * 0.9, uh = h * 0.94, ud = d * 0.88; UNDER = grp(at(box(uw, uh, ud, o.under, { outline: 0.008 }), 0, uh / 2, 0));
      const fr = canvasPlane(uw, uh, (c, W, H) => { c.fillStyle = o.under; c.fillRect(0, 0, W, H); c.fillStyle = '#F4F2EC'; c.beginPath(); c.moveTo(W * 0.3, 0); c.lineTo(W * 0.7, 0); c.lineTo(W * 0.5, H * 0.5); c.closePath(); c.fill();
        c.fillStyle = '#B5202A'; c.beginPath(); c.moveTo(W * 0.46, 0); c.lineTo(W * 0.54, 0); c.lineTo(W * 0.55, H * 0.4); c.lineTo(W * 0.5, H * 0.47); c.lineTo(W * 0.45, H * 0.4); c.closePath(); c.fill();
        c.strokeStyle = 'rgba(0,0,0,0.35)'; c.lineWidth = W * 0.03; c.beginPath(); c.moveTo(W * 0.28, 0); c.lineTo(W * 0.5, H * 0.52); c.lineTo(W * 0.72, 0); c.stroke(); }, { res: 128 });
      fr.position.set(0, uh / 2, ud / 2 + 0.003); UNDER.add(fr); UNDER.visible = false; g.add(UNDER); }
    let sewn = null; if (o.sewn != null) { sewn = careTag(o.sewnS ?? 0.85); sewn.position.set(w * 0.1, h * 0.3, d / 2 + 0.012); sewn.rotation.z = -0.12; OUT.add(sewn); }
    const SST = o.sewnSteps || null, sewP = sewn ? sewn.position.clone() : null;
    const T = o.turn || null, tPop = T ? T.at + 0.8 * T.dur : -1e9, kicks = [...(o.tagKick || []), ...(T ? [tPop] : []), ...(o.tagPop != null ? [o.tagPop] : [])];
    const TA = T ? (T.amp ?? 1) : 1, KA = o.tagKickAmp ?? 1, PS = o.popS ?? 1, PA = o.popAmp ?? 0.35, PD = o.popDecay ?? 9, PF = o.popFreq ?? 26, tagY = tags.length ? tags[0].position.y : 0;
    g.userData.update = t => {
      let ins = in0; if (o.flipAt != null && t >= o.flipAt) ins = false; if (T && t >= T.at + 0.5 * T.dur) ins = !in0;
      IN.visible = ins; OUT.visible = !ins;
      let py = 0, sx = 1, sy = 1, sz = 1, rz = 0;
      if (o.flipAt != null) { const u = t - o.flipAt, a = u >= 0 && u < 0.25 ? Math.exp(-12 * u) * Math.cos(u * 40) : 0; sx += 0.15 * a; sy -= 0.15 * a; sz = sx; }
      if (T && t >= T.at) { const u = (t - T.at) / T.dur;
        if (u < 0.3) { const e = 1 - (1 - u / 0.3) * (1 - u / 0.3); py = h * e; sy = 1 + 0.75 * TA * e; sx = 1 - 0.03 * e; sz = 1 + 0.45 * TA * e; }
        else if (u < 0.68 && T.bulges) { const q = (u - 0.3) / 0.38, b1 = q < 0.36 ? Math.sin(PI * q / 0.36) : 0, b2 = q > 0.56 && q < 0.92 ? Math.sin(PI * (q - 0.56) / 0.36) : 0, hang = q >= 0.36 && q <= 0.56 ? 1 : 0;
          py = h + 0.05 * TA * (b1 + b2) + 0.006 * hang * Math.sin(q * 60); sy = 1 + 0.75 * TA + 0.12 * TA * (b1 + b2); sx = 0.97 + 0.32 * TA * (b1 + b2); sz = 1 + 0.45 * TA + 0.2 * TA * (b1 + b2); rz = 0.22 * TA * (b1 - b2); }
        else if (u < 0.68) { const q = (u - 0.3) / 0.38; py = h + 0.03 * TA * Math.sin(q * 4 * PI); sy = 1 + 0.75 * TA + 0.1 * TA * Math.sin(q * 6 * PI); sx = 0.97 + 0.15 * TA * Math.sin(q * 4 * PI); sz = 1 + 0.45 * TA + 0.1 * TA * Math.sin(q * 4 * PI + 1.6); rz = 0.09 * TA * Math.sin(q * 4 * PI + 0.8); }
        else if (u < 0.8) { const e = (u - 0.68) / 0.12, e2 = e * e; py = h * (1 - e2); sy = 1 + 0.75 * TA - (0.75 * TA + 0.4 * TA) * e2; sx = 0.97 + (0.03 + 0.28 * TA) * e2; sz = 1 + 0.45 * TA - (0.45 * TA - 0.28 * TA) * e2; }
        else { const v = t - (T.at + 0.8 * T.dur), a = Math.exp(-9 * v) * Math.cos(30 * v); sy = 1 - 0.4 * TA * a; sx = 1 + 0.28 * TA * a; sz = sx; } }
      body.position.y = py; body.scale.set(sx, sy, sz); body.rotation.z = rz;
      if (UNDER) UNDER.visible = py > h * 0.22;
      for (const tag of tags) { let sc = 1, st = 0, ry = 1;   // its size, its stretch (taller and thinner), how far it is hoisted
        if (T && !in0) { if (t < tPop) sc = 0.001; else { const v = t - tPop; sc = PS; st = PA * Math.exp(-PD * v) * Math.cos(PF * v); } }
        if (o.tagPop != null) { if (t < o.tagPop) sc = 0.001; else { const v = t - o.tagPop; st = 0.5 * Math.exp(-8 * v) * Math.cos(24 * v); } }
        if (o.tagRise) { const u = clamp01((t - o.tagRise.at) / o.tagRise.dur); ry = Math.max(0.001, u * u * (3 - 2 * u)); }
        const hop = o.tagHop ? Math.abs(Math.sin(t * (o.tagRate ?? 4.2) * 0.5 + (o.tagPhase ?? 0))) : 0;
        let sag = 0; if (o.tagSag) { const u = clamp01((t - o.tagSag.at) / (o.tagSag.dur ?? 0.8)); sag = u * u * (3 - 2 * u); }
        tag.scale.set(sc * (1 - 0.45 * st), sc * (1 + st) * ry * (1 + (o.tagHop ? 0.3 * (hop - 0.5) : 0)) * (1 - 0.1 * sag), sc); tag.position.y = tagY + (o.tagHop ?? 0) * hop;
        tag.rotation.set(-0.12, 0, -side * ((o.tagLean ?? 0.36) + (o.tagSag ? (o.tagSag.amp ?? 0.35) * sag : 0)) + (o.tagSway ?? 0.07) * Math.sin(t * (o.tagRate ?? 4.2) + (o.tagPhase ?? 0)) + KA * kickOf(kicks, t)); }
      if (sewn && SST) { sewn.visible = t >= o.sewn; let n = 0, last = -1e9; for (const ts of SST) if (t >= ts) { n++; last = ts; } const f = n / SST.length, v = t - last, snap = n ? 0.25 * Math.exp(-12 * v) * Math.cos(30 * v) : 0;
        sewn.rotation.z = -0.12 + (1 - f) * 0.85 + snap * 0.4; sewn.position.set(sewP.x + (1 - f) * 0.05, sewP.y - (1 - f) * 0.07, sewP.z + (1 - f) * 0.02); sewn.scale.setScalar(1 + 0.3 * snap); }
      else if (sewn) { const v = t - o.sewn; sewn.visible = v >= 0; if (v >= 0) sewn.scale.setScalar(1 + 0.4 * Math.exp(-10 * v) * Math.cos(28 * v)); }
    };
    g.userData.update(-1); return g;
  },

  // (review 1) The care label alone (pivot at its bottom middle): to stand on a collar that is no jumper's (a judge's robe). o.s its scale (1: 0.24 x
  // 0.3 m), it sways (o.sway 0.07, o.rate 4.2) and flops at each time of o.kick; o.lean (rad): its rest lean about Z.
  careLabel(o) {
    const g = grp(), tag = careTag(o.s ?? 1); g.add(tag);
    g.userData.update = t => { tag.rotation.set(-0.1, 0, (o.lean ?? 0) + (o.sway ?? 0.07) * Math.sin(t * (o.rate ?? 4.2)) + (o.kickAmp ?? 1) * kickOf(o.kick, t)); };
    g.userData.update(0); return g;
  },

  // (review 1) An oversized sewing needle with its thread (attach to the hand; the needle points along +Y from the grip, 0.34 m at s 1): a steel
  // needle with an eye, and a red thread (o.color) that leaves the eye and hangs: it bends toward the ground whatever way the hand turns the
  // needle, and sways
  // (final pass) o.to [x, y, z] (world) and o.taut [[t0, t1], ...]: in those windows the thread runs from the eye to that point (the label being
  // sewn) in a shallow arc, pulled tight (a thread that only hung read as jabbing near the label, never into it)
  sewNeedle(o) {
    const s = o.s ?? 1, g = grp(at(cyl(0.005 * s, 0.02 * s, 0.34 * s, '#DCE1E6', 6, { outline: 0.006 }), 0, 0.12 * s, 0), at(box(0.05 * s, 0.07 * s, 0.012 * s, '#DCE1E6', { outline: 0.005 }), 0, -0.07 * s, 0));
    const n = 6, segs = Array.from({ length: n }, () => { const m = box(0.016 * s, 0.075 * s, 0.016 * s, o.color || '#C8322A'); g.add(m); return m; });
    const q = new THREE.Quaternion(), dn = new THREE.Vector3(), dir = new THREE.Vector3(), Y = new THREE.Vector3(0, 1, 0), p = new THREE.Vector3(), tg = new THREE.Vector3(), a0 = new THREE.Vector3(), a1 = new THREE.Vector3();
    const tautAt = t => (o.taut || []).find(w => t >= w[0] && t <= w[1]);
    g.userData.update = t => {
      const win = o.to ? tautAt(t) : null;
      if (win) { g.updateWorldMatrix(true, false); tg.set(o.to[0], o.to[1], o.to[2]); g.worldToLocal(tg); p.set(0, -0.1 * s, 0);
        const L = p.distanceTo(tg), sagK = 0.12 * L * (1 - Math.min(1, (t - win[0]) / 0.08));   // it snaps tight in the first frames
        g.getWorldQuaternion(q); dn.set(0, -1, 0).applyQuaternion(q.invert());
        segs.forEach((m, i) => { const u0 = i / n, u1 = (i + 1) / n; a0.copy(p).lerp(tg, u0).addScaledVector(dn, sagK * 4 * u0 * (1 - u0)); a1.copy(p).lerp(tg, u1).addScaledVector(dn, sagK * 4 * u1 * (1 - u1));
          dir.copy(a1).sub(a0); const l = dir.length(); m.position.copy(a0).add(a1).multiplyScalar(0.5); m.quaternion.setFromUnitVectors(Y, dir.multiplyScalar(1 / Math.max(1e-5, l))); m.scale.set(0.7, l / (0.075 * s), 0.7); });
        return; }
      segs.forEach(m => m.scale.set(1, 1, 1));
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

  // (review 2) A studio light on a stand (pivot at the floor, the lit face +Z): a tripod, a pole o.h high (2.0) and a softbox o.w x o.bh (0.55 x 0.42)
  // whose face glows in o.color (warm white); o.tilt (rad): the box tips down
  studioLight(o) {
    const H = o.h ?? 2.0, w = o.w ?? 0.55, bh = o.bh ?? 0.42, g = grp(at(cyl(0.02, 0.02, H, '#3A3F48', 6, { pivot: 'bottom' }), 0, 0, 0));
    for (let i = 0; i < 3; i++) { const a = i * 2 * PI / 3; g.add(at(cyl(0.014, 0.018, 0.5, '#3A3F48', 6), Math.sin(a) * 0.16, 0.2, Math.cos(a) * 0.16, Math.cos(a) * 0.6, 0, -Math.sin(a) * 0.6)); }
    const head = grp(at(box(w + 0.06, bh + 0.06, 0.22, '#23262D', { outline: 0.008 }), 0, 0, -0.1), at(box(w, bh, 0.02, o.color || '#FFF3CF'), 0, 0, 0.02));
    head.children[1].traverse(n => { if (n.isMesh && n.material && n.material.emissive) { n.material = n.material.clone(); n.material.emissive = new THREE.Color(o.color || '#FFF3CF'); n.material.emissiveIntensity = 0.9; } n.castShadow = false; });
    head.position.set(0, H, 0); head.rotation.x = o.tilt ?? 0.25; g.add(head); return g;
  },

  // (review 2) A lighting truss with spots and their beams (pivot at the middle of the bar, which runs along X): o.w wide (3), o.n spots (4), each
  // with a pale see-through cone of light o.len long (2.4) that tips forward by o.tilt (0.25 rad) and fans out sideways by o.fan (0.35 rad at the
  // ends); o.sweep (rad): the beams swing slowly; o.color the light; o.opacity (0.16); o.spread (0.22): how much each cone widens per metre
  lightTruss(o) {
    const w = o.w ?? 3, n = o.n ?? 4, len = o.len ?? 2.4, g = grp(at(box(w, 0.07, 0.07, '#4A4F58', { outline: 0.006 }), 0, 0.05, 0), at(box(w, 0.07, 0.07, '#4A4F58', { outline: 0.006 }), 0, -0.05, 0)), beams = [];
    for (let i = 0; i <= 8; i++) g.add(at(box(0.03, 0.17, 0.03, '#4A4F58'), -w / 2 + i * w / 8, 0, 0));
    for (let i = 0; i < n; i++) { const x = n > 1 ? -w / 2 + 0.25 + i * (w - 0.5) / (n - 1) : 0, piv = grp(); piv.position.set(x, -0.1, 0);
      piv.add(at(cyl(0.09, 0.07, 0.2, '#23262D', 8, { outline: 0.006 }), 0, -0.1, 0), at(cyl(0.085, 0.085, 0.015, o.color || '#FFF3CF', 8), 0, -0.21, 0));
      const cone = cyl(0.07, 0.07 + len * (o.spread ?? 0.22), len, o.color || '#FFF3CF', 10); cone.position.y = -0.21 - len / 2;
      cone.traverse(m => { m.castShadow = false; m.receiveShadow = false; if (m.isMesh && m.material) { m.material = m.material.clone(); m.material.transparent = true; m.material.opacity = o.opacity ?? 0.16; m.material.depthWrite = false; if (m.material.emissive) { m.material.emissive = new THREE.Color(o.color || '#FFF3CF'); m.material.emissiveIntensity = 0.6; } } });
      piv.add(cone); g.add(piv); beams.push({ piv, u: n > 1 ? i / (n - 1) - 0.5 : 0, i }); }
    g.userData.update = t => { for (const b of beams) b.piv.rotation.set(o.tilt ?? 0.25, 0, -b.u * 2 * (o.fan ?? 0.35) + (o.sweep ?? 0) * Math.sin(t * 1.7 + b.i * 1.3)); };
    g.userData.update(0); return g;
  },

  // (review 2) A studio monitor on a wheeled stand (pivot at the floor, the screen +Z): o.h (1.25) to the middle of a 0.62 x 0.4 screen that shows
  // the programme: a blue set, a presenter's bust in o.jumper with a white label over his shoulder, and a red bar with o.text
  studioMonitor(o) {
    const H = o.h ?? 1.25, g = grp(at(cyl(0.025, 0.025, H, '#3A3F48', 6, { pivot: 'bottom' }), 0, 0, 0), at(box(0.5, 0.05, 0.4, '#3A3F48', { outline: 0.006 }), 0, 0.04, 0), at(box(0.7, 0.48, 0.07, '#23262D', { outline: 0.008 }), 0, H, 0));
    const scr = canvasPlane(0.62, 0.4, (c, W, Hh) => { c.fillStyle = '#5878A8'; c.fillRect(0, 0, W, Hh); c.fillStyle = o.jumper || '#2F8F6B'; c.fillRect(W * 0.3, Hh * 0.55, W * 0.4, Hh * 0.45);
      c.fillStyle = '#E3B38A'; c.fillRect(W * 0.43, Hh * 0.2, W * 0.14, Hh * 0.36); c.fillStyle = '#3A2A20'; c.fillRect(W * 0.43, Hh * 0.2, W * 0.14, Hh * 0.07);
      c.fillStyle = '#FFFFFF'; c.strokeStyle = '#17181C'; c.lineWidth = W * 0.012; c.fillRect(W * 0.6, Hh * 0.34, W * 0.11, Hh * 0.22); c.strokeRect(W * 0.6, Hh * 0.34, W * 0.11, Hh * 0.22);
      c.fillStyle = '#D22B2B'; c.fillRect(0, Hh * 0.82, W, Hh * 0.18); c.fillStyle = '#FFFFFF'; c.font = `900 ${Hh * 0.13}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.text || 'EN DIRECT', W / 2, Hh * 0.915); }, { res: 256, emissive: 0.5 });
    scr.position.set(0, H, 0.04); g.add(scr); return g;
  },
};
