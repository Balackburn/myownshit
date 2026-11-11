// « La cravate » (story 43): a man whose tie is caught in the lift door; the lift goes up, the tie follows, to the sixth floor.
// Conventions as in props.js (metres, front +Z, pivot at the floor); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, ease, clamp01 } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const keyed3 = (keys, t) => { if (!keys || !keys.length) return null; let a = keys[0]; for (let i = 0; i < keys.length; i++) { const k = keys[i], n = keys[i + 1]; if (t >= k[0]) { if (n && t < n[0]) { const u = (t - k[0]) / (n[0] - k[0]), e = (ease[k[4]] || (x => x))(u); return [k[1] + (n[1] - k[1]) * e, k[2] + (n[2] - k[2]) * e, k[3] + (n[3] - k[3]) * e]; } a = k; } } return [a[1], a[2], a[3]]; };

// one thing pegged on the rope: its top edge at the origin, hanging down -Y, facing +Z
function washing(kind, color) {
  const g = grp(), peg = dx => at(box(0.02, 0.07, 0.03, '#E3C56A'), dx, 0.0, 0);
  if (kind === 'sock') g.add(at(box(0.09, 0.2, 0.02, color, { outline: 0.004 }), 0, -0.12, 0), at(box(0.15, 0.08, 0.02, color, { outline: 0.004 }), 0.03, -0.24, 0), at(box(0.09, 0.03, 0.022, '#F4F1E8'), 0, -0.04, 0), peg(0));
  else if (kind === 'towel') g.add(at(box(0.42, 0.5, 0.015, color, { outline: 0.004 }), 0, -0.27, 0), at(box(0.42, 0.05, 0.017, '#F4F1E8'), 0, -0.42, 0), peg(-0.14), peg(0.14));
  else if (kind === 'shorts') g.add(at(box(0.34, 0.14, 0.02, color, { outline: 0.004 }), 0, -0.09, 0), at(box(0.15, 0.14, 0.02, color, { outline: 0.004 }), -0.095, -0.21, 0), at(box(0.15, 0.14, 0.02, color, { outline: 0.004 }), 0.095, -0.21, 0), peg(-0.12), peg(0.12));
  else g.add(at(box(0.3, 0.36, 0.02, color, { outline: 0.004 }), 0, -0.2, 0), at(box(0.14, 0.1, 0.02, color, { outline: 0.004 }), -0.2, -0.08, 0, 0, 0, 0.5), at(box(0.14, 0.1, 0.02, color, { outline: 0.004 }), 0.2, -0.08, 0, 0, 0, -0.5), peg(-0.1), peg(0.1));   // 'shirt'
  return g;
}

export const CRAVATE_PROPS = {
  // A tie that has become a rope. A flat ribbon (o.w 0.075 m wide) from the prop's own origin (attach it to his collar: on = {actor, joint, offset})
  // through o.via [[x, y, z], ...] (points of the world: the top of a door, a corner) to its far end: o.to [x, y, z], or o.toKeys [[t, x, y, z, ease?],
  // ...] (the cabin that goes up). Taut: straight between its points.
  //   o.pluck [[t, amp (m), freq (Hz), speed (m/s), damp (1/s)], ...]: somebody plays it at its far end... at o.pluckAt (0..1 of its length from the far
  //     end, 0): a wave runs down to him from there, and dies; it shakes sideways (along o.side [x, y, z], default world X)
  //   o.paint [t0, t1]: from t0 to t1 another colour (o.color2 '#D9C7A3') comes down it from the far end (the house painters)
  //   o.items [{ at: 0..1 (from the far end), kind: 'sock' | 'shirt' | 'towel' | 'shorts', color, from: t }, ...]: washing pegged on it, each popping on
  //   o.color ('#C8202A'), o.face [x, y, z] (the way its flat side looks: world +Z)
  // userData.length(t): its length (m): a wave started at t0 with speed v reaches him at t0 + (1 - pluckAt) * length / v
  tieRope(o) {
    const N = o.n ?? 48, w = o.w ?? 0.075, g = grp(), C1 = new THREE.Color(o.color || '#C8202A'), C2 = new THREE.Color(o.color2 || '#D9C7A3');
    const pos = new Float32Array((N + 1) * 2 * 3), col = new Float32Array((N + 1) * 2 * 3), idx = [];
    for (let i = 0; i < N; i++) { const a = i * 2; idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); }
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(pos, 3)); geo.setAttribute('color', new THREE.BufferAttribute(col, 3)); geo.setIndex(idx);
    const m = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ vertexColors: true, side: THREE.DoubleSide })); m.frustumCulled = false; m.castShadow = false; m.receiveShadow = false; g.add(m);
    const items = (o.items || []).map(it => { const q = washing(it.kind || 'shirt', it.color || '#F4F1E8'); q.userData.it = it; g.add(q); return q; });
    const FACE = new THREE.Vector3(...(o.face || [0, 0, 1])).normalize(), SIDE = new THREE.Vector3(...(o.side || [1, 0, 0])).normalize();
    const A = new THREE.Vector3(), B = new THREE.Vector3(), d = new THREE.Vector3(), q = new THREE.Vector3(), wv = new THREE.Vector3(), inv = new THREE.Matrix4(), tmp = new THREE.Vector3();
    const path = t => { g.updateWorldMatrix(true, false); const pts = [new THREE.Vector3().setFromMatrixPosition(g.matrixWorld)]; for (const v of o.via || []) pts.push(new THREE.Vector3(...v)); const e = keyed3(o.toKeys, t) || o.to || [0, 3, 0]; pts.push(new THREE.Vector3(...e)); return pts; };
    const lengthOf = pts => { let L = 0; for (let i = 1; i < pts.length; i++) L += pts[i].distanceTo(pts[i - 1]); return L; };
    g.userData.length = t => lengthOf(path(t));
    g.userData.update = t => {
      const pts = path(t), L = Math.max(1e-3, lengthOf(pts)); inv.copy(g.matrixWorld).invert();
      const cum = [0]; for (let i = 1; i < pts.length; i++) cum.push(cum[i - 1] + pts[i].distanceTo(pts[i - 1]));
      const node = (s, out) => { let i = 1; while (i < pts.length - 1 && cum[i] < s) i++; const u = clamp01((s - cum[i - 1]) / Math.max(1e-6, cum[i] - cum[i - 1])); out.copy(pts[i - 1]).lerp(pts[i], u); d.copy(pts[i]).sub(pts[i - 1]).normalize(); return out; };
      const pa = o.paint ? clamp01((t - o.paint[0]) / Math.max(1e-3, o.paint[1] - o.paint[0])) : 0;   // how far down the second colour has come
      const off = sFar => { let x = 0; for (const [t0, amp, f = 6, v = 14, damp = 3.5] of o.pluck || []) { const s0 = (o.pluckAt || 0) * L, tt = t - t0 - Math.abs(sFar - s0) / v; if (tt > 0) x += amp * Math.sin(TAU * f * tt) * Math.exp(-damp * tt); } return x * Math.sin(PI * clamp01(sFar / L)) ** 0.5; };
      for (let i = 0; i <= N; i++) { const s = L * i / N; node(s, q); q.addScaledVector(SIDE, off(L - s));
        wv.crossVectors(d, FACE); if (wv.lengthSq() < 1e-6) wv.copy(SIDE); wv.normalize().multiplyScalar(w / 2);
        for (const sg of [-1, 1]) { tmp.copy(q).addScaledVector(wv, sg).applyMatrix4(inv); const k = (i * 2 + (sg > 0 ? 1 : 0)) * 3; pos[k] = tmp.x; pos[k + 1] = tmp.y; pos[k + 2] = tmp.z; const c = (1 - i / N) < pa ? C2 : C1; col[k] = c.r; col[k + 1] = c.g; col[k + 2] = c.b; } }
      geo.attributes.position.needsUpdate = true; geo.attributes.color.needsUpdate = true; geo.computeVertexNormals();
      for (const it of items) { const c = it.userData.it, sFar = clamp01(c.at ?? 0.5) * L, u = t - (c.from ?? 0); it.visible = u >= 0; if (!it.visible) continue;
        node(L - sFar, q); q.addScaledVector(SIDE, off(sFar)).addScaledVector(FACE, 0.012); const pop = u < 0.14 ? 1 + 0.35 * Math.sin(PI * u / 0.14) : 1, sw = 0.5 * (off(sFar + 0.05) - off(sFar - 0.05)) / 0.1;
        it.position.copy(q.applyMatrix4(inv)); it.rotation.set(0, 0, sw + 0.05 * Math.sin(t * 2.3 + sFar)); it.scale.setScalar(pop / Math.max(1e-3, g.getWorldScale(tmp).x)); }
    };
    g.userData.update(0); return g;
  },
};
