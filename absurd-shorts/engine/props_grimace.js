// « La grimace » (story 59, cycle 21): a man pulled a face; the wind turned; he stayed like that; the town hall refuses his identity photo; the carnival
// hired him as a mask; yesterday the wind turned again; the whole town stayed in a grimace; except him; the carnival fired him: he is too scary.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { mat, box, cyl, sphere, addOutline } from './style.js';
import { grp, at, canvasPlane } from './props.js';
import { makeFaceRig, faceState, hasFaceRig, cloneFace } from './facerig.js';

const PI = Math.PI, TAU = 2 * PI;
const list = v => [].concat(v ?? []);
// a value keyed in time: [[t, v], ...], linear between keys, held outside them
function lin(ks, t, dflt) {
  const k = list(ks); if (!k.length) return dflt;
  if (t <= k[0][0]) return k[0][1];
  for (let i = 1; i < k.length; i++) if (t < k[i][0]) { const [t0, v0] = k[i - 1], [t1, v1] = k[i]; return v0 + (v1 - v0) * (t - t0) / Math.max(1e-6, t1 - t0); }
  return k[k.length - 1][1];
}
// the turns made from 0 to t at a rate keyed linearly (turns per second)
function turns(ks, t, n = 120) { if (t <= 0) return 0; const h = t / n; let s = 0; for (let i = 0; i < n; i++) s += (lin(ks, i * h, 0) + lin(ks, (i + 1) * h, 0)) / 2 * h; return s; }

// (pass 2 of 59) the script's face offsets on a painted state, as director3.js applies them to a live face: the photo is the very same grimace
function faceWith(cf = {}) {
  const st = cloneFace(faceState(cf.expr || 'grimace')), E = st.eyes, cl = (v, a, b) => Math.max(a, Math.min(b, v));
  if (cf.cross) { E.L.px = cl(E.L.px + 0.95 * cf.cross, -1, 1); E.R.px = cl(E.R.px - 0.95 * cf.cross, -1, 1); }
  for (const sd of 'LR') { const b = st.brows[sd], e = E[sd], up = (cf.brow || 0) + (cf['brow' + sd] || 0), sz = (cf.eye || 0) + (cf['eye' + sd] || 0), pz = (cf.pupilSize || 0) + 0.5;
    if (up) b.dy -= 26 * up; if (sz) e.s = cl(e.s * (1 + sz), 0.5, 1.9); e.ps = cl(e.ps * (1 + pz), 0.3, 3.4); }
  if (typeof cf.mouth === 'string' && cf.mouth) st.mouth = { ...st.mouth, spr: cf.mouth, w: 1, h: 1, tilt: 0, dx: 0, dy: 0 };
  if (cf.mouthW || cf.mouthH || cf.mouthTilt) st.mouth = { ...st.mouth, w: st.mouth.w * (1 + (cf.mouthW || 0)), h: st.mouth.h * (1 + (cf.mouthH || 0)), tilt: st.mouth.tilt + (cf.mouthTilt || 0) };
  return st;
}

export const GRIMACE_PROPS = {
  // A weathervane (pivot at the foot of its rod, on a roof ridge): a black iron rod o.h (1.2) tall, the four letters N S E O on a cross, and on top an
  // arrow with a rooster that turns: o.spin [[t, turns per second]] (integrated: it whirls up and slows), o.yaw0 its heading at 0; o.wobble [t]: a shake
  // of the rooster from t. Past o.blur (1.2) turns a second, three fading ghosts trail the arrow (a smear: crisp, it strobed). o.roof: a slate roof ridge
  // under it, o.roof.len (3.2) long along X, with a brick chimney. o.lift [t0, a (m/s²), drift (m/s)]: from t0 the vane unscrews (it climbs 0.3 m/s)
  // and takes off like a helicopter, the rod and the letters spinning with the arrow.
  weathervane(o) {
    const h = o.h ?? 1.2, iron = '#22252B', g = grp(), vane = grp(), top = grp(); g.add(vane); vane.add(at(cyl(0.02, 0.025, h, iron, 6, { pivot: 'bottom' }), 0, 0, 0));
    if (o.roof) { const L = o.roof.len ?? 3.2, W = o.roof.w ?? 2.4, H = o.roof.h ?? 1.1, sl = o.roof.color || '#566170', sh = new THREE.Shape();
      sh.moveTo(-W / 2, -H); sh.lineTo(0, 0); sh.lineTo(W / 2, -H); sh.closePath();
      const geo = new THREE.ExtrudeGeometry(sh, { depth: L, bevelEnabled: false }).translate(0, 0, -L / 2).rotateY(PI / 2), rf = new THREE.Mesh(geo, mat(sl)); rf.castShadow = rf.receiveShadow = true; addOutline(rf, 0.006); g.add(rf);
      g.add(at(box(L + 0.08, 0.08, 0.14, o.roof.zinc || '#A9B2BA', { outline: 0.006 }), 0, 0.0, 0), at(box(0.42, 0.9, 0.42, '#A65A3E', { pivot: 'bottom', outline: 0.008 }), L * 0.3, -0.45, -0.25), at(box(0.5, 0.08, 0.5, '#7E4430'), L * 0.3, 0.47, -0.25));
      // (pass 3 of 59) slate courses down both slopes (a flat slab read as a blue wall) and the zinc ridge above
      const ang = Math.atan2(H, W / 2), dk = new THREE.Color(sl).multiplyScalar(0.72).getStyle();
      for (const sd of [-1, 1]) for (let k = 1; k < 7; k++) { const f = k / 7, y = -H * f, z = sd * (W / 2) * f;
        g.add(at(box(L + 0.02, 0.018, 0.03, dk), 0, y + 0.012, z + sd * 0.004, sd * ang, 0, 0)); }
      for (let i = 0; i < 2; i++) g.add(at(cyl(0.06, 0.06, 0.18, '#C9765A', 8, { pivot: 'bottom' }), L * 0.3 + (i - 0.5) * 0.16, 0.5, -0.25)); }
    for (const [a, l] of [[0, 'N'], [PI / 2, 'E'], [PI, 'S'], [-PI / 2, 'O']]) {
      vane.add(at(box(0.012, 0.012, 0.32, iron), 0.16 * Math.sin(a), h * 0.62, 0.16 * Math.cos(a), 0, a, 0));
      const lt = canvasPlane(0.1, 0.1, (c, W, H) => { c.clearRect(0, 0, W, H); c.fillStyle = iron; c.font = `900 ${H * 0.9}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(l, W / 2, H * 0.55); }, { res: 64, transparent: true });
      // (pass 3 of 59) two one-sided planes back to back: the double-sided plane read mirrored from behind (E and S backwards)
      lt.material.side = THREE.FrontSide; const lb = lt.clone(); lb.material = lt.material.clone(); lb.material.side = THREE.FrontSide;
      lt.position.set(0.34 * Math.sin(a), h * 0.62, 0.34 * Math.cos(a)); lt.rotation.y = a; lb.position.copy(lt.position); lb.rotation.y = a + PI; vane.add(lt, lb);
    }
    top.position.y = h; vane.add(top);
    // the rooster in silhouette, facing the arrow's point (+X): sickle tail feathers, body, neck, head, comb, beak, wattle, legs on the arrow
    const cockTex = (c, W, H) => { c.clearRect(0, 0, W, H); c.fillStyle = c.strokeStyle = iron; c.lineCap = 'round';
      c.lineWidth = W * 0.035; for (const [x0, y0, x1, y1] of [[0.46, 0.86, 0.48, 0.7], [0.58, 0.86, 0.57, 0.7]]) { c.beginPath(); c.moveTo(W * x0, H * y0); c.lineTo(W * x1, H * y1); c.stroke(); }
      c.beginPath(); c.ellipse(W * 0.5, H * 0.6, W * 0.2, H * 0.13, -0.15, 0, TAU); c.fill();
      c.beginPath(); c.moveTo(W * 0.58, H * 0.56); c.lineTo(W * 0.68, H * 0.34); c.lineTo(W * 0.79, H * 0.36); c.lineTo(W * 0.72, H * 0.62); c.closePath(); c.fill();
      c.beginPath(); c.arc(W * 0.74, H * 0.3, W * 0.075, 0, TAU); c.fill();
      for (const [x, y] of [[0.69, 0.22], [0.735, 0.195], [0.78, 0.215]]) { c.beginPath(); c.arc(W * x, H * y, W * 0.032, 0, TAU); c.fill(); }
      c.beginPath(); c.moveTo(W * 0.8, H * 0.27); c.lineTo(W * 0.9, H * 0.31); c.lineTo(W * 0.8, H * 0.34); c.closePath(); c.fill();
      c.beginPath(); c.ellipse(W * 0.785, H * 0.39, W * 0.022, H * 0.035, 0, 0, TAU); c.fill();
      c.lineWidth = W * 0.05; for (const [cx, cy, x1, y1] of [[0.12, 0.45, 0.14, 0.17], [0.2, 0.38, 0.22, 0.11], [0.3, 0.36, 0.31, 0.15]]) { c.beginPath(); c.moveTo(W * 0.36, H * 0.56); c.quadraticCurveTo(W * cx, H * cy, W * x1, H * y1); c.stroke(); } };
    const mkTop = op => { const t = grp(), m = op < 1 ? mat(iron, { opacity: op, unique: true }) : null;
      t.add(at(box(0.62, 0.025, 0.025, iron, m ? { material: m } : {}), 0, 0, 0), at(new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.14, 4).rotateZ(-PI / 2), m || mat(iron)), 0.36, 0, 0),
        at(box(0.02, 0.14, 0.16, iron, m ? { material: m } : {}), -0.32, 0.04, 0, 0, 0, 0.3));
      const ck = canvasPlane(0.46, 0.46, cockTex, { res: 256, transparent: true }); if (m) { ck.material.opacity = op; ck.material.depthWrite = false; } ck.position.set(0.04, 0.22, 0); t.add(ck); return t; };
    const main = mkTop(1); top.add(main); const ghosts = [0.42, 0.26, 0.14].map(op => { const gh = mkTop(op); top.add(gh); return gh; });
    const rate = t => lin(o.spin || [[0, 0]], t, 0), sign = t => Math.sign(rate(t)) || 1;
    g.userData.update = t => { let yaw = TAU * turns(o.spin || [[0, 0]], t) + (o.yaw0 ?? 0); const w = o.wobble; if (w && t >= w[0]) { const u = t - w[0]; yaw += 0.25 * Math.sin(u * 22) * Math.exp(-u * 5); }
      const L = o.lift, u = L ? t - L[0] : -1;
      // (pass 2 of 59) o.lift [t0, rise (s), height (m), hover (s), zip (m/s²)]: it unscrews up slowly, hovers bobbing, then zips off; three values: the old climb
      const ph = L && L.length >= 5 ? (u < L[1] ? L[2] * u / L[1] : u < L[1] + L[3] ? L[2] + 0.06 * Math.sin((u - L[1]) * 18) : L[2] + 0.5 * L[4] * (u - L[1] - L[3]) ** 2) : 0;
      if (u >= 0) { vane.rotation.y = yaw; top.rotation.y = 0; if (L.length >= 5) vane.position.set(0, ph, 0); else vane.position.set((L[2] ?? 0) * u, 0.3 * u + 0.5 * (L[1] ?? 6) * u * u, 0); } else { vane.rotation.y = 0; vane.position.set(0, 0, 0); vane.rotation.z = 0; top.rotation.y = yaw;
        // (pass 3 of 59) o.dip [t0, dur, depth]: the anticipation before it unscrews: the whole vane sinks into its socket and shudders, then comes back
        const D = o.dip; if (D && t >= D[0] && t < D[0] + D[1]) { const v = (t - D[0]) / D[1], env = Math.sin(PI * v); vane.position.y = -(D[2] ?? 0.12) * env; vane.rotation.z = 0.14 * Math.sin(v * 34) * env; } }
      const rr = Math.abs(rate(t)), bl = o.blur ?? 1.2, on = rr > bl;
      ghosts.forEach((gh, i) => { gh.visible = on; gh.rotation.y = -sign(t) * Math.min(0.5, 0.12 * rr) * (i + 1); }); };
    g.userData.update(0); return g;
  },

  // A carnival float (pivot at the floor in its middle, length along X): a platform o.w (2.6) long, o.d (1.4) deep, o.h (0.75) high with a striped skirt,
  // paper flowers along its edge, a garland pole at each end (roll it with prop keys: to / dur).
  carnivalFloat(o) {
    const w = o.w ?? 2.6, d = o.d ?? 1.4, h = o.h ?? 0.75, g = grp();
    const skirt = canvasPlane(w, h, (c, W, H) => { const cols = ['#E8463A', '#F5C33B', '#3A9BDC', '#52B76A', '#C255C8']; const n = 13; for (let i = 0; i < n; i++) { c.fillStyle = cols[i % cols.length]; c.fillRect(i * W / n, 0, W / n + 1, H); }
      c.fillStyle = 'rgba(255,255,255,0.85)'; for (let i = 0; i < n; i++) { c.beginPath(); c.arc((i + 0.5) * W / n, H * 0.12, W / n * 0.28, 0, TAU); c.fill(); } }, { res: 512 });
    // (pass 3 of 59) the skirt lifted 0.24 m with a gold fringe at its hem, a dark chassis and the wheels showing under it (a plain striped box)
    const lift = o.lift ?? 0.24, sk = skirt.clone(); sk.scale.y = (h - lift) / h;
    for (const [z, ry] of [[d / 2 + 0.005, 0], [-d / 2 - 0.005, PI]]) { const s = sk.clone(); s.position.set(0, lift + (h - lift) / 2, z); s.rotation.y = ry; g.add(s);
      for (let i = 0; i < 26; i++) g.add(at(box(0.05, 0.08, 0.012, '#E3B23C'), -w / 2 + (i + 0.5) * w / 26, lift - 0.03, z + Math.sign(z) * 0.004)); }
    g.add(at(box(w * 0.94, 0.12, d * 0.9, '#3A3A40'), 0, lift - 0.06, 0));
    g.add(at(box(w, 0.08, d, '#F4EBD8', { outline: 0.01 }), 0, h, 0));
    for (let i = 0; i < 9; i++) g.add(at(sphere(0.07, ['#E8463A', '#F5C33B', '#FFFFFF', '#C255C8'][i % 4], 1), -w / 2 + (i + 0.5) * w / 9, h + 0.07, d / 2 - 0.05));
    for (const sx of [-1, 1]) g.add(at(cyl(0.025, 0.025, 1.3, '#E8D9B0', 6, { pivot: 'bottom' }), sx * (w / 2 - 0.12), h, -d / 2 + 0.12), at(sphere(0.06, '#F5C33B', 1), sx * (w / 2 - 0.12), h + 1.32, -d / 2 + 0.12));
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) g.add(at(cyl(0.16, 0.16, 0.08, '#2A2C30', 10), sx * (w / 2 - 0.35), 0.16, sz * (d / 2 + 0.02), PI / 2, 0, 0));
    g.userData.deck = h + 0.04;
    return g;
  },

  // The identity photo of a man pulling a face (pivot at its centre, face +Z): his square head on the blue background, the eyes crossed and bulging,
  // the mouth stretched wide by two fingers, the tongue out; o.w (0.1) wide: scale it up for inserts.
  // (pass 2 of 59) painted by his own face rig (o.expr, 'grimace'): the drawn face did not look like him (round eyes, no stubble), so the refusal
  // looked reasonable; his head pulled wide (o.wide 1.3), his ears, his tongue out and aside, his navy jacket and red tie; o.stamp: a red REFUSÉE
  // printed across it (the stamp's imprint is part of the photo, above its face)
  grimacePhoto(o) {
    const w = o.w ?? 0.1, h = w * 1.25, g = grp(at(box(w * 1.12, h * 1.1, 0.002, '#FFFFFF', { outline: 0.004 }), 0, 0, 0));
    let face = null; if (hasFaceRig) { try { const fr = makeFaceRig(null); fr.set(o.face ? faceWith(o.face) : faceState(o.expr || 'grimace')); face = fr.canvas; } catch (e) { face = null; } }   // o.face: the script's face dict
    const draw = (c, W, H) => { c.fillStyle = '#9CC9E8'; c.fillRect(0, 0, W, H);
      c.fillStyle = '#1F2E4A'; c.fillRect(W * 0.08, H * 0.8, W * 0.84, H * 0.2); c.fillStyle = '#F2F2EC'; c.beginPath(); c.moveTo(W * 0.42, H * 0.8); c.lineTo(W * 0.5, H * 0.92); c.lineTo(W * 0.58, H * 0.8); c.fill();
      c.fillStyle = '#C8202A'; c.fillRect(W * 0.48, H * 0.82, W * 0.04, H * 0.18);
      const fw = W * 0.5 * (o.wide ?? 1.3), fh = H * 0.72, fx = (W - fw) / 2, fy = H * 0.06;
      c.fillStyle = '#D9A877'; c.fillRect(fx - W * 0.05, fy + fh * 0.4, W * 0.06, fh * 0.22); c.fillRect(fx + fw - W * 0.01, fy + fh * 0.4, W * 0.06, fh * 0.22);   // ears
      if (face) c.drawImage(face, fx, fy, fw, fh);
      else { c.fillStyle = '#E2A270'; c.fillRect(fx, fy, fw, fh); c.fillStyle = '#1E1A18'; c.fillRect(fx, fy, fw, fh * 0.16); c.fillStyle = '#2A1A14'; c.fillRect(fx + fw * 0.2, fy + fh * 0.45, fw * 0.6, fh * 0.03); }
      c.fillStyle = '#E0717F'; c.strokeStyle = '#7A2A34'; c.lineWidth = W * 0.012; c.beginPath(); c.ellipse(W * 0.44, fy + fh * 0.86, W * 0.07, H * 0.075, -0.4, 0, 2 * Math.PI); c.fill(); c.stroke();   // the tongue, out and aside
      if (o.stamp) { c.save(); c.translate(W / 2, H * 0.5); c.rotate(-0.28); c.font = `900 ${Math.round(H * 0.11)}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle';
        // (pass 3 of 59) a white halo under a darker ink: red on his orange face measured 2.2:1
        c.strokeStyle = 'rgba(255,255,255,0.95)'; c.lineWidth = W * 0.06; c.strokeRect(-W * 0.46, -H * 0.075, W * 0.92, H * 0.15); c.lineJoin = 'round'; c.lineWidth = W * 0.035; c.strokeText(o.stamp, 0, H * 0.008, W * 0.86);
        c.strokeStyle = c.fillStyle = 'rgba(150,8,20,0.97)'; c.lineWidth = W * 0.03; c.strokeRect(-W * 0.46, -H * 0.075, W * 0.92, H * 0.15); c.fillText(o.stamp, 0, H * 0.008, W * 0.86); c.restore(); } };
    const plane = canvasPlane(w, h, draw, { res: 384 }); plane.position.z = 0.0015; g.add(plane);
    g.userData.grip = [0, -h * 0.4, 0]; return g;
  },

  // A carnival banner across a street (pivot at its middle, front +Z): a cloth o.w (5) by o.h (0.9) in stripes with « CARNAVAL » (o.text) on it,
  // hung from two ropes to the facades at o.span (14) metres, with pennants along its top edge; it sways a little
  carnivalBanner(o) {
    const w = o.w ?? 5, h = o.h ?? 0.9, span = o.span ?? 14, g = grp(), cloth = grp(); g.add(cloth);
    const pl = canvasPlane(w, h, (c, W, H) => { const cols = ['#E8463A', '#F5C33B', '#3A9BDC', '#52B76A', '#C255C8']; for (let i = 0; i < 10; i++) { c.fillStyle = cols[i % 5]; c.fillRect(i * W / 10, 0, W / 10 + 1, H); }
      c.fillStyle = 'rgba(255,255,255,0.88)'; c.fillRect(W * 0.04, H * 0.16, W * 0.92, H * 0.68); c.fillStyle = '#C8202A'; c.font = `900 ${Math.round(H * 0.52)}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle';
      c.fillText(o.text || 'CARNAVAL', W / 2, H * 0.53, W * 0.86); }, { res: 768 });
    cloth.add(pl, at(box(w + 0.06, 0.05, 0.05, '#7A5A3C'), 0, h / 2 + 0.02, 0));
    for (const sx of [-1, 1]) { const len = (span - w) / 2, rope = at(box(len, 0.02, 0.02, '#5A4A3A'), sx * (w / 2 + len / 2), h / 2 + 0.25, 0, 0, 0, sx * -0.08); g.add(rope); }
    g.userData.update = t => { cloth.rotation.x = 0.06 * Math.sin(t * 2.2); cloth.position.z = 0.04 * Math.sin(t * 2.2); };
    g.userData.update(0); return g;
  },

  // A gust: o.n (14) leaves blown along +X across o.w (5) metres from o.startAt for o.dur (0.9) seconds, fluttering, o.h high (pivot where they enter)
  leafGust(o) {
    const n = o.n ?? 14, w = o.w ?? 5, g = grp(), leaves = [];
    // (pass 3 of 59) leaf-shaped (pointed ovals with a stem): the rectangles read as carnival confetti
    const lf = new THREE.Shape(); lf.moveTo(-0.055, 0); lf.quadraticCurveTo(-0.01, 0.04, 0.05, 0); lf.quadraticCurveTo(-0.01, -0.04, -0.055, 0); lf.lineTo(-0.075, 0.004); lf.lineTo(-0.075, -0.004); lf.lineTo(-0.055, 0);
    const leafGeo = new THREE.ShapeGeometry(lf);
    for (let i = 0; i < n; i++) { const m = new THREE.Mesh(leafGeo, new THREE.MeshLambertMaterial({ color: ['#D9832B', '#C8452E', '#E2B23A', '#8E9A3A'][i % 4], side: THREE.DoubleSide })); g.add(m); leaves.push({ m, y: 0.2 + ((i * 37) % 17) / 17 * (o.h ?? 1.8), z: (((i * 53) % 11) / 11 - 0.5) * (o.d ?? 1.2), d: (i * 0.071) % 0.35, s: 0.8 + ((i * 29) % 7) / 10 }); }
    g.userData.update = t => { const u0 = (t - (o.startAt ?? 0)) / (o.dur ?? 0.9);
      for (const L of leaves) { const u = u0 - L.d; L.m.visible = u > 0 && u < 1; if (!L.m.visible) continue; L.m.position.set(u * w * L.s, L.y + 0.25 * Math.sin(u * 9 + L.d * 20), L.z + 0.15 * Math.cos(u * 7)); L.m.rotation.set(u * 14, u * 9, u * 11); } };
    g.userData.update(0); return g;
  },
};
