// What trails on a cartoon actor (cycle 2). Opt-in: script `cloth: true` or cast `{cloth: true}`; without it nothing here is built.
//   - a tie in three segments: it hangs, swings forward on a stop, flies up in a fall, goes over the shoulder in a run or a head wind, flutters;
//   - a shock of hair on the crown: flat at rest, it stands up and leans with the wind (a fall, a sprint, a sneeze in the face).
// Both are driven by one vector, the apparent wind in the actor's own frame (x: to his left, y: up, z: forward), in m/s: the scene wind minus his own
// velocity. The director computes it without state (finite differences of the actor's track, a few frames late), so any frame can be rendered alone.
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
    const m = box(d.hw * 0.98, 0.05, d.hd * 0.98, d.hairColor, { pivot: 'bottom', taper: { x: 0.82, z: 0.7 } }); g.add(m); g.scale.y = 0.02;
    hair = { g };
  }
  ud.cloth = {
    // w: apparent wind in the actor's frame (m/s); t: time (flutter); k: dose 0..1
    apply(w = [0, 0, 0], t = 0, k = 1) {
      const [wx, wy, wz] = w, sp = Math.hypot(wx, wy, wz), fl = Math.min(1, sp / 7);
      if (tie) {
        const Fy = -G0 + wy, Fz = wz, Fx = wx;
        let rx = Math.atan2(Fz, -Fy), rz = Math.atan2(Fx, Math.hypot(Fy, Fz)) * 0.8, over = 0;   // rx > 0: the tie swings forward (away from the chest), pi: straight up
        if (rx < 0) {   // blown against the chest: it lies flat, then climbs over a shoulder
          const a = -rx; over = sm(a, 0.3, 1.2); rx = -0.06 * Math.min(1, a / 0.3) * (1 - over) + 3.5 * over; rz += tie.side * 0.75 * over;   // up in front, then back over the shoulder (never through the chest)
        }
        const f1 = 0.1 * fl * Math.sin(t * 17 + 1), f2 = 0.3 * fl * Math.sin(t * 23 + 2.2), f3 = 0.5 * fl * Math.sin(t * 29 + 0.7);
        tie.segs[0].rotation.set(-(rx * 0.72 + f1) * k, 0, (rz * 0.6 + 0.3 * f1) * k);
        tie.segs[1].rotation.set(-(rx * 0.2 + f2) * k, 0, (rz * 0.3 + 0.4 * f2) * k);
        tie.segs[2].rotation.set(-(rx * 0.08 + f3) * k, 0, (rz * 0.1 + 0.5 * f3) * k);
      }
      if (hair) {
        const up = Math.max(0, wy), lift = Math.min(1, (Math.hypot(wx, wz) * 0.6 + up) / 9) * k;
        hair.g.scale.y = 0.02 + 5.2 * lift * (1 + 0.12 * Math.sin(t * 31)); const h = Math.hypot(wx, wz) || 1e-6, lean = Math.min(1.1, Math.hypot(wx, wz) / (4 + up)) * k;
        hair.g.rotation.set(lean * wz / h * 1.0 + 0.1 * lift * Math.sin(t * 27), 0, -lean * wx / h * 1.0);
      }
    },
  };
  return ud.cloth;
}
