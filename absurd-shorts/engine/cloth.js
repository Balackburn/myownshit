// What trails on a cartoon actor (cycle 2). Opt-in: script `cloth: true` or cast `{cloth: true}`; without it nothing here is built.
//   - a tie in three segments: it hangs, swings forward on a stop, flies up in a fall, goes over the shoulder in a run or a head wind, flutters;
//   - a shock of hair on the crown: flat at rest, it stands up and leans with the wind (a fall, a sprint, a sneeze in the face).
// Both are driven by one vector, the apparent wind in world space, in m/s: the scene wind (fx {type: 'wind'}) minus the actor's own velocity. The director
// computes it without state (finite differences of the actor's track, a few frames late), so any frame can be rendered alone.
import * as THREE from 'three';
import { box } from './style.js';

const G0 = 6.5;                                   // how much wind (m/s) it takes to lift the tie to the horizontal
const sm = (x, a, b) => { const t = Math.max(0, Math.min(1, (x - a) / (b - a))); return t * t * (3 - 2 * t); };

export function clothUpgrade(obj, opts = {}) {
  const ud = obj.userData, J = ud.joints, d = ud.dims; if (!J?.torso || !d || ud.cloth) return ud.cloth;
  let tie = null, hair = null, tails = null;
  if (opts.tails && d.jacketColor && d.tailW) {   // (cycle 6) the two tails of a suit jacket (script / cast `tails: true`): they hang behind the hips, fly back in a run, up in a fall
    const g = new THREE.Group(); g.name = 'tails3d'; g.position.set(0, 0.03, -d.front - 0.006); J.torso.add(g);
    const w = d.tailW / 2 - 0.008, L = 0.27;
    tails = [-1, 1].map(s => { const pv = new THREE.Group(); pv.position.set(s * (w / 2 + 0.008), 0, 0); g.add(pv); pv.add(box(w, L, 0.014, d.jacketColor, { pivot: 'top', taper: { x: 1.1, z: 1 } })); return { pv, s }; });
  }
  if (d.tieColor) {   // the flat tie (a box, or paint on the hero's jacket) gives way to a real one
    ud.hideFlatTie?.();
    const root = new THREE.Group(); root.name = 'tie3d'; root.position.set(d.tieX || 0, d.torsoH * 0.9, d.front + 0.014); J.torso.add(root);
    const knot = box(0.052, 0.05, 0.022, d.tieColor); knot.position.set(0, 0.0, 0.004); root.add(knot);
    const L = [0.2, 0.2, 0.23].map(k => k * d.torsoH), W = [[0.05, 0.058], [0.058, 0.068], [0.068, 0.078]], segs = []; let parent = root, y = -0.02;
    L.forEach((len, i) => {
      const g = new THREE.Group(); g.position.y = y; parent.add(g);
      const m = box(W[i][1], len, 0.012, d.tieColor, { pivot: 'top', taper: { x: W[i][0] / W[i][1], z: 1 } }); g.add(m);
      if (i === 2) { const tip = box(0.055, 0.055, 0.012, d.tieColor); tip.rotation.z = Math.PI / 4; tip.position.y = -len; g.add(tip); }   // the point
      segs.push(g); parent = g; y = -len;
    });
    tie = { root, segs, side: (ud.spec?.seed ?? 3) % 2 ? 1 : -1, knot, col0: d.tieColor };
    if (opts.knotOnly) segs[0].visible = false;   // (cycle 7) cast `tieKnot: true`: only the knot is left at his collar (the rest of the tie is a prop: a rope caught in a lift door)
  }
  if (J.head && d.hairColor && d.hw) {   // a shock of hair: the footprint of the crown, almost flat at rest
    const g = new THREE.Group(); g.name = 'hairShock'; g.position.set(0, d.hh, 0); J.head.add(g);
    // five tufts (three in front, two behind), flat on the crown at rest; when the hair stands each one is a spike of its own height, fanned out (one block
    // standing up read as a fez)
    const tufts = [[-0.32, 0.2, 0.36, 0.9], [0, 0.22, 0.36, 1.25], [0.32, 0.2, 0.36, 1.0], [-0.17, -0.24, 0.42, 1.1], [0.2, -0.24, 0.42, 0.8]].map(([x, z, w, hk], i) => {
      const pv = new THREE.Group(); pv.position.set(x * d.hw, 0, z * d.hd); g.add(pv);
      const m = box(d.hw * w, 0.05, d.hd * 0.5, d.hairColor, { pivot: 'bottom', taper: { x: 0.14, z: 0.22 } }); m.scale.y = 0.02; pv.add(m);
      return { pv, m, hk, fx: -x * 1.5, fz: z * 0.9, ph: i * 1.7 };
    });
    hair = { g, tufts };
  }
  const F = new THREE.Vector3(), q = new THREE.Quaternion(), tie_side = (ud.spec?.seed ?? 3) % 2 ? 1 : -1;
  ud.cloth = {
    // aw: apparent wind in world space, m/s (the scene wind minus the actor's own velocity); t: time (flutter); k: dose 0..1.
    // Gravity and wind are brought into the frame of the chest (the tie) and of the head (the hair), so lying down or upside down works too
    apply(aw = [0, 0, 0], t = 0, k = 1, fat = 1, hairUp = 0, pull = null, opt = null) {   // pull [length, forward, aside]: the tie taken in a hand (toon channel `tie`): it stretches (1 = its own length) and swings toward the hand (radians)   // hairUp 0..1: hair left standing whatever the wind (toon channel `hairUp`)   // fat: how much the chest is inflated (the spine band's thickness): the knot stays on its surface
      const sp = Math.hypot(aw[0], aw[1], aw[2]), fl = Math.min(1, sp / 7);
      if (tie && tie.knot) { const c = opt?.knot || tie.col0; if (tie.knot.userData.col !== c) { if (!tie.knot.userData.own) { tie.knot.material = tie.knot.material.clone(); tie.knot.userData.own = true; } tie.knot.material.color.set(c); tie.knot.userData.col = c; } }   // (cycle 7) toon channel `knot`: another colour for the knot (his tie painted over)
      if (tie) {
        tie.root.position.z = (d.front + 0.014) * Math.max(0.6, fat);
        J.torso.getWorldQuaternion(q).invert(); const head = -F.set(aw[0], aw[1], aw[2]).applyQuaternion(q).z;   // the wind that blows onto the chest (m/s)
        F.set(aw[0], aw[1] - G0, aw[2]).applyQuaternion(q);
        let rx = Math.atan2(F.z, -F.y), rz = Math.atan2(F.x, Math.hypot(F.y, F.z)) * 0.8, over = 0;   // rx > 0: the tie swings forward (away from the chest), pi: straight up
        if (rx < 0) {   // pressed against the chest: it lies flat (a man leaning back, lying down); a strong head wind sends it up in front and back over a shoulder
          over = sm(head, 5, 11); rx = 3.5 * over; rz = rz * (1 - over) + tie.side * 0.75 * over;
          if (opt?.gravity) { const inv = sm(F.y, 0.5, 4.5); if (inv > 0) { rx += (Math.PI - 0.2 - rx) * inv; rz *= 1 - inv; } }   // (cycle 6, `clothGravity`) the chest upside down: gravity takes the tie toward the head, the wind lays it on the chin and the face
        }
        const f1 = 0.1 * fl * Math.sin(t * 17 + 1), f2 = 0.3 * fl * Math.sin(t * 23 + 2.2), f3 = 0.5 * fl * Math.sin(t * 29 + 0.7);
        tie.segs[0].rotation.set(-(rx * 0.72 + f1) * k, 0, (rz * 0.6 + 0.3 * f1) * k);
        tie.segs[1].rotation.set(-(rx * 0.2 + f2) * k, 0, (rz * 0.3 + 0.4 * f2) * k);
        tie.segs[2].rotation.set(-(rx * 0.08 + f3) * k, 0, (rz * 0.1 + 0.5 * f3) * k);
        tie.segs[0].scale.y = pull ? Math.max(0.2, pull[0] ?? 1) : 1; if (pull) { tie.segs[0].rotation.x -= pull[1] || 0; tie.segs[0].rotation.z += pull[2] || 0; }
      }
      if (tails) {
        J.torso.getWorldQuaternion(q).invert(); F.set(aw[0], aw[1] - G0, aw[2]).applyQuaternion(q);
        const lift = Math.max(0, Math.atan2(-F.z, -F.y));   // blown back by a head wind, up over the back in a fall; against the legs otherwise
        for (const tl of tails) tl.pv.rotation.set(Math.min(2.7, lift * 0.9 + fl * (0.22 * Math.sin(t * 21 + tl.s * 1.3) + 0.1 * Math.sin(t * 33 + tl.s))) * k, 0, tl.s * 0.18 * Math.min(1, lift) * k);
      }
      if (hair) {
        J.head.getWorldQuaternion(q).invert(); F.set(aw[0], aw[1] - 2.2, aw[2]).applyQuaternion(q);   // a little gravity: upside down, the hair hangs
        const h = Math.hypot(F.x, F.z), up = Math.max(0, F.y), lift = Math.min(1, (h * 0.55 + up * 1.1) / 8 + hairUp) * k, lean = Math.min(1.15, h / (3.5 + up)) * k, hh = h || 1e-6;
        const fan = Math.min(1, lift * 2.5);
        hair.g.visible = lift > 0.012;   // flat on the scalp it is not drawn (seen edge-on, the flat tufts were a black line floating over a tilted head)
        hair.g.rotation.set(lean * fan * F.z / hh + 0.1 * lift * Math.sin(t * 27) - 0.25 * hairUp, 0, -lean * fan * F.x / hh + 0.2 * hairUp * tie_side);   // it leans only once it stands
        for (const q of hair.tufts) { q.m.scale.y = 0.02 + 5.2 * lift * q.hk * (1 + 0.12 * Math.sin(t * 31 + q.ph)); q.pv.rotation.set(q.fz * 0.5 * fan + 0.08 * lift * Math.sin(t * 23 + q.ph), 0, q.fx * 0.34 * fan + 0.1 * lift * Math.sin(t * 27 + q.ph * 1.3)); }
      }
    },
  };
  return ud.cloth;
}
