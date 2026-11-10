// What trails on a cartoon actor (cycle 2). Opt-in: script `cloth: true` or cast `{cloth: true}`; without it nothing here is built.
//   - a tie in three segments: it hangs, swings forward on a stop, flies up in a fall, goes over the shoulder in a run or a head wind, flutters;
//   - a shock of hair on the crown: flat at rest, it stands up and leans with the wind (a fall, a sprint, a sneeze in the face).
// Both are driven by one vector, the apparent wind in world space, in m/s: the scene wind (fx {type: 'wind'}) minus the actor's own velocity. The director
// computes it without state (finite differences of the actor's track, a few frames late), so any frame can be rendered alone.
import * as THREE from 'three';
import { box } from './style.js';

const G0 = 6.5;                                   // how much wind (m/s) it takes to lift the tie to the horizontal
const sm = (x, a, b) => { const t = Math.max(0, Math.min(1, (x - a) / (b - a))); return t * t * (3 - 2 * t); };

export function clothUpgrade(obj) {
  const ud = obj.userData, J = ud.joints, d = ud.dims; if (!J?.torso || !d || ud.cloth) return ud.cloth;
  let tie = null, hair = null;
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
    tie = { root, segs, side: (ud.spec?.seed ?? 3) % 2 ? 1 : -1 };
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
    apply(aw = [0, 0, 0], t = 0, k = 1, fat = 1, hairUp = 0) {   // hairUp 0..1: hair left standing whatever the wind (toon channel `hairUp`)   // fat: how much the chest is inflated (the spine band's thickness): the knot stays on its surface
      const sp = Math.hypot(aw[0], aw[1], aw[2]), fl = Math.min(1, sp / 7);
      if (tie) {
        tie.root.position.z = (d.front + 0.014) * Math.max(0.6, fat);
        J.torso.getWorldQuaternion(q).invert(); const head = -F.set(aw[0], aw[1], aw[2]).applyQuaternion(q).z;   // the wind that blows onto the chest (m/s)
        F.set(aw[0], aw[1] - G0, aw[2]).applyQuaternion(q);
        let rx = Math.atan2(F.z, -F.y), rz = Math.atan2(F.x, Math.hypot(F.y, F.z)) * 0.8, over = 0;   // rx > 0: the tie swings forward (away from the chest), pi: straight up
        if (rx < 0) {   // pressed against the chest: it lies flat (a man leaning back, lying down); a strong head wind sends it up in front and back over a shoulder
          over = sm(head, 5, 11); rx = 3.5 * over; rz = rz * (1 - over) + tie.side * 0.75 * over;
        }
        const f1 = 0.1 * fl * Math.sin(t * 17 + 1), f2 = 0.3 * fl * Math.sin(t * 23 + 2.2), f3 = 0.5 * fl * Math.sin(t * 29 + 0.7);
        tie.segs[0].rotation.set(-(rx * 0.72 + f1) * k, 0, (rz * 0.6 + 0.3 * f1) * k);
        tie.segs[1].rotation.set(-(rx * 0.2 + f2) * k, 0, (rz * 0.3 + 0.4 * f2) * k);
        tie.segs[2].rotation.set(-(rx * 0.08 + f3) * k, 0, (rz * 0.1 + 0.5 * f3) * k);
      }
      if (hair) {
        J.head.getWorldQuaternion(q).invert(); F.set(aw[0], aw[1] - 2.2, aw[2]).applyQuaternion(q);   // a little gravity: upside down, the hair hangs
        const h = Math.hypot(F.x, F.z), up = Math.max(0, F.y), lift = Math.min(1, (h * 0.55 + up * 1.1) / 8 + hairUp) * k, lean = Math.min(1.15, h / (3.5 + up)) * k, hh = h || 1e-6;
        hair.g.rotation.set(lean * F.z / hh + 0.1 * lift * Math.sin(t * 27) - 0.25 * hairUp, 0, -lean * F.x / hh + 0.2 * hairUp * tie_side);
        const fan = Math.min(1, lift * 2.5);
        for (const q of hair.tufts) { q.m.scale.y = 0.02 + 5.2 * lift * q.hk * (1 + 0.12 * Math.sin(t * 31 + q.ph)); q.pv.rotation.set(q.fz * 0.5 * fan + 0.08 * lift * Math.sin(t * 23 + q.ph), 0, q.fx * 0.34 * fan + 0.1 * lift * Math.sin(t * 27 + q.ph * 1.3)); }
      }
    },
  };
  return ud.cloth;
}
