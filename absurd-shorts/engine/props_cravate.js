// « La cravate » (story 43): a man whose tie is caught in the lift door; the lift goes up, the tie follows, to the sixth floor.
// Conventions as in props.js (metres, front +Z, pivot at the floor); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, ease, clamp01 } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const keyed3 = (keys, t) => { if (!keys || !keys.length) return null; let a = keys[0]; for (let i = 0; i < keys.length; i++) { const k = keys[i], n = keys[i + 1]; if (t >= k[0]) { if (n && t < n[0]) { const u = (t - k[0]) / (n[0] - k[0]), e = (ease[k[4]] || (x => x))(u); return [k[1] + (n[1] - k[1]) * e, k[2] + (n[2] - k[2]) * e, k[3] + (n[3] - k[3]) * e]; } a = k; } } return [a[1], a[2], a[3]]; };

// one thing pegged on the rope: its top edge at the origin, hanging down -Y, facing +Z
const fitFont = (c, text, maxW, size, weight = '') => { c.font = `${weight} ${size}px Arial`; const w = c.measureText(text).width; return w > maxW ? size * maxW / w : size; };
function textSheet(w, h, head, lines, o = {}) {   // a white sheet with a bold heading and lines of type (unlit when o.bright)
  const pl = canvasPlane(w, h, (c, W, H) => { c.fillStyle = o.paper || '#F7F4EC'; c.fillRect(0, 0, W, H); c.strokeStyle = 'rgba(0,0,0,0.3)'; c.lineWidth = W * 0.01; c.strokeRect(W * 0.005, W * 0.005, W * 0.99, H - W * 0.01);
    c.fillStyle = o.ink || '#1B1B1E'; c.textAlign = 'center'; c.textBaseline = 'middle'; let y = H * (o.top ?? 0.13);
    if (head) { const fs = fitFont(c, head, W * 0.86, H * (o.headSize ?? 0.085), 'bold'); c.font = `bold ${fs}px Arial`; c.fillText(head, W / 2, y); y += fs * 0.85; c.fillRect(W * 0.1, y, W * 0.8, Math.max(2, H * 0.008)); y += fs * 0.9; }
    if (o.big) { const fs = fitFont(c, o.big, W * 0.88, H * (o.bigSize ?? 0.17), 'bold'); c.font = `bold ${fs}px Arial`; c.fillStyle = o.bigInk || c.fillStyle; c.fillText(o.big, W / 2, y + fs * 0.45); c.fillStyle = o.ink || '#1B1B1E'; y += fs * 1.25; }
    for (const ln of lines || []) { const lw = o.lineBold ? 'bold' : '', fs = fitFont(c, ln, W * 0.86, H * (o.lineSize ?? 0.06), lw); c.font = `${lw} ${fs}px Arial`; if (o.lineInk) c.fillStyle = o.lineInk; c.fillText(ln, W / 2, y); y += H * (o.lineGap ?? 0.085); }   // o.lineInk: the lines in their own colour   // o.lineBold: the lines in bold too
    if (o.rules) { c.fillStyle = 'rgba(27,27,30,0.32)'; let i = 0; while (y < H * 0.9) { c.fillRect(W * 0.12, y, W * (0.52 + 0.24 * ((i * 0.37) % 1)), Math.max(2, H * 0.008)); y += H * 0.05; i++; } }
  }, { res: 512 });
  if (o.bright) pl.material = new THREE.MeshBasicMaterial({ map: pl.material.map, side: THREE.DoubleSide });
  return pl;
}
function washing(kind, color, it = {}) {
  const g = grp(), peg = dx => at(box(0.02, 0.07, 0.03, '#E3C56A'), dx, 0.0, 0);
  if (kind === 'notice' || kind === 'bill') {   // (cycle 7) a notice pegged on it (it.head, it.lines), a bill (it.head on an envelope)
    const w = it.w ?? (kind === 'bill' ? 0.32 : 0.36), h = it.h ?? (kind === 'bill' ? 0.2 : 0.48);
    const pl = textSheet(w, h, it.head || (kind === 'bill' ? 'CHARGES' : 'AVIS'), it.lines || [], { bright: it.bright, paper: kind === 'bill' ? '#F1E6CC' : undefined, rules: kind === 'notice', headSize: kind === 'bill' ? 0.2 : 0.085, top: kind === 'bill' ? 0.4 : 0.13 });
    pl.position.set(0, -h / 2 - 0.02, 0.004); g.add(pl, peg(0)); return g;
  }
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
    const items = (o.items || []).map(it => { const q = washing(it.kind || 'shirt', it.color || '#F4F1E8', it); q.userData.it = it; g.add(q); return q; });
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

  // (cycle 7) a sheet of paper (front +Z, origin at its centre): o.w × o.h (0.42 × 0.56), o.head (bold heading), o.big (one line in large type),
  // o.lines [...], o.rules (small print under them), o.stamp { text, color, at, rot, y } (a stamp mark that slams on at t: from 1.6 times its size to 1,
  // with a jolt), o.bright (unlit), o.paper, o.ink, o.bigInk
  paperSheet(o) {
    const w = o.w ?? 0.42, h = o.h ?? 0.56, g = grp(textSheet(w, h, o.head, o.lines, o));
    if (o.stamp) { const s = o.stamp, sw = w * (s.w ?? 0.8), sh = sw * 0.32, col = s.color || '#C8202A';
      const sm = canvasPlane(sw, sh, (c, W, H) => { c.clearRect(0, 0, W, H); c.strokeStyle = c.fillStyle = col; c.lineWidth = H * 0.08; c.strokeRect(H * 0.06, H * 0.06, W - H * 0.12, H * 0.88); const fs = fitFont(c, s.text, W * 0.84, H * 0.6, 'bold'); c.font = `bold ${fs}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(s.text, W / 2, H * 0.55); }, { res: 512, transparent: true });
      if (o.bright) sm.material = new THREE.MeshBasicMaterial({ map: sm.material.map, transparent: true, alphaTest: 0.05, side: THREE.DoubleSide });
      sm.position.set(0, s.y ?? -h * 0.14, 0.004); sm.rotation.z = s.rot ?? 0.2; g.add(sm);
      const t0 = s.at ?? 0; g.userData.update = t => { const u = t - t0; sm.visible = u >= 0; if (u >= 0) sm.scale.setScalar(u < 0.07 ? 1.6 - 0.6 * (u / 0.07) : 1 + 0.06 * Math.sin((u - 0.07) * 45) * Math.exp(-(u - 0.07) * 16)); }; g.userData.update(0); }
    return g;
  },

  // (cycle 7) a folded name card (a little tent) on a seat or a table: o.text, o.w (0.36) × o.h (0.13), o.bg, o.fg; front +Z, origin at its foot
  nameCard(o) {
    const w = o.w ?? 0.36, h = o.h ?? 0.13, A = 0.3, g = grp(), bg = o.bg || '#F7F4EC', fg = o.fg || '#1B1B1E';
    const face = canvasPlane(w, h, (c, W, H) => { c.fillStyle = bg; c.fillRect(0, 0, W, H); c.strokeStyle = fg; c.lineWidth = H * 0.05; c.strokeRect(H * 0.08, H * 0.08, W - H * 0.16, H * 0.84); c.fillStyle = fg; const tx = o.text || 'NOM', fs = fitFont(c, tx, W * 0.84, H * 0.48, 'bold'); c.font = `bold ${fs}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(tx, W / 2, H * 0.55); }, { res: 512 });
    if (o.bright) face.material = new THREE.MeshBasicMaterial({ map: face.material.map, side: THREE.DoubleSide });
    const f = grp(at(face, 0, h / 2, 0)); f.rotation.x = -A; f.position.z = h * Math.sin(A); g.add(f);
    const b = grp(at(box(w, h, 0.004, bg), 0, h / 2, 0)); b.rotation.x = A; b.position.z = -h * Math.sin(A); g.add(b);
    return g;
  },

  // (cycle 7) a paint roller on a long handle: origin at the grip, the roller o.len (0.8) m up along +Y; o.color: the paint on it
  paintRoller(o) {
    const L = o.len ?? 0.8, g = grp(at(cyl(0.016, 0.016, L, '#8C7B5E', 6, { pivot: 'bottom' }), 0, -0.1, 0), at(box(0.22, 0.025, 0.025, '#6F7680'), 0, L - 0.1, 0));
    // (cycle 8) o.rollerR / o.rollerW: a bigger roller (0.05 / 0.26); o.sleeve: the sleeve's own colour, o.color then the band of paint on half of it
    // (a tan roller laying tan paint was a block the colour of what it laid)
    const R = o.rollerR ?? 0.05, RW = o.rollerW ?? 0.26, r = cyl(R, R, RW, o.sleeve || o.color || '#D9C7A3', 10); r.rotation.z = PI / 2; r.position.set(0, L - 0.04, 0.02); g.add(r);
    if (o.sleeve) { const pb = cyl(R * 1.04, R * 1.04, RW * 0.5, o.color || '#D9C7A3', 10); pb.rotation.z = PI / 2; pb.position.set(RW * 0.25, L - 0.04, 0.02); g.add(pb); }
    g.userData.grip = [0, 0, 0]; return g;
  },

  // (cycle 7) a painters' cradle: a plank o.w (1.6) × o.d (0.5) with a guard rail (o.color), a pot of paint (o.paint), hanging from two ropes that go up
  // to y = o.roofY (world) wherever the cradle is; origin at the middle of its floor. Move it with keys (to)
  paintCradle(o) {
    const w = o.w ?? 1.6, d = o.d ?? 0.5, c = o.color || '#E3A93A', g = grp(at(box(w, 0.07, d, '#9A8B72', { outline: 0.006 }), 0, 0.035, 0)), ropes = [], v = new THREE.Vector3();
    for (const sd of [-1, 1]) { for (const sz of [-1, 1]) g.add(at(box(0.04, 1.0, 0.04, c, { outline: 0.004 }), sd * (w / 2 - 0.03), 0.5, sz * (d / 2 - 0.03)));
      g.add(at(box(0.04, 0.04, d, c), sd * (w / 2 - 0.03), 1.0, 0)); const rp = cyl(0.012, 0.012, 1, '#3A3D44', 5, { pivot: 'bottom' }); rp.position.set(sd * (w / 2 - 0.03), 1.0, 0); g.add(rp); ropes.push(rp); }
    g.add(at(box(w, 0.04, 0.04, c, { outline: 0.004 }), 0, 1.0, d / 2 - 0.03), at(box(w, 0.04, 0.04, c), 0, 1.0, -d / 2 + 0.03), at(box(w, 0.04, 0.04, c), 0, 0.5, d / 2 - 0.03));
    g.add(at(cyl(0.11, 0.1, 0.2, o.paint || '#D9C7A3', 10), w / 2 - 0.3, 0.17, 0), at(cyl(0.112, 0.112, 0.012, '#B8A684', 10), w / 2 - 0.3, 0.27, 0));
    g.userData.update = () => { g.getWorldPosition(v); const s = g.getWorldScale(new THREE.Vector3()).y || 1; for (const rp of ropes) rp.scale.y = Math.max(0.01, ((o.roofY ?? 20) - v.y) / s - 1.0); };
    return g;
  },

  // (cycle 7) a tie knot to put over his own when the tie changes colour: o.color; attach it at his collar (it pops on with a scale key)
  tieKnot(o) { return grp(at(box(0.06, 0.056, 0.028, o.color || '#D9C7A3'), 0, 0, 0)); },
};
