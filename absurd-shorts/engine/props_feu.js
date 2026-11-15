// « Le feu rouge » (story 66, pass 2): this man waits at a red light for twelve years. The props of pass 2: the French pedestrian signal (a red man
// over a green man), a beard of hair (clumps, not slats), a woven nest, dust that bursts off him and falls, tear fountains, a big ticket, the little
// house built round him, a heap of letters, a reporter's microphone and a boom. Conventions as in props.js (metres, front +Z, pivot at the floor
// unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const hash = n => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const L = c => new THREE.MeshLambertMaterial({ color: c });
const ball = (r, c, seg = 10) => new THREE.Mesh(new THREE.SphereGeometry(r, seg, Math.max(6, seg - 2)), typeof c === 'string' ? L(c) : c);
const inkM = new THREE.MeshBasicMaterial({ color: '#1A1A1E', side: THREE.BackSide });
const UP = new THREE.Vector3(0, 1, 0);
// a tapered segment from a to b (Vector3), radius ra at a and rb at b
function seg(a, b, ra, rb, m) { const d = b.clone().sub(a), l = Math.max(1e-4, d.length()), ms = new THREE.Mesh(new THREE.CylinderGeometry(rb, ra, l, 7, 1), m);
  ms.position.copy(a).add(b).multiplyScalar(0.5); ms.quaternion.setFromUnitVectors(UP, d.normalize()); ms.castShadow = true; return ms; }
// a line of text in bold Arial at (x, y), shrunk to fit maxW
function fit(c, s, x, y, size, maxW) { let fs = size; c.font = `900 ${fs}px Arial`; const w = c.measureText(s).width; if (w > maxW) { fs *= maxW / w; c.font = `900 ${fs}px Arial`; } c.fillText(s, x, y); }
// the little man of a pedestrian light, in round strokes: standing (arms down, legs together) or walking (legs apart, arms swinging)
function pedMan(c, W, H, col, walk) {
  c.fillStyle = '#0B0C10'; c.fillRect(0, 0, W, H); c.strokeStyle = col; c.fillStyle = col; c.lineCap = 'round'; c.lineJoin = 'round'; c.lineWidth = W * 0.11;
  const P = (x, y) => [W * x, H * y], line = (a, b) => { c.beginPath(); c.moveTo(...P(...a)); c.lineTo(...P(...b)); c.stroke(); };
  c.beginPath(); c.arc(W * (walk ? 0.52 : 0.5), H * 0.16, W * 0.085, 0, TAU); c.fill();
  if (walk) { line([0.52, 0.3], [0.48, 0.58]); line([0.48, 0.58], [0.34, 0.88]); line([0.48, 0.58], [0.6, 0.72]); line([0.6, 0.72], [0.66, 0.88]); line([0.51, 0.34], [0.36, 0.5]); line([0.51, 0.34], [0.66, 0.46]); }
  else { line([0.5, 0.3], [0.5, 0.6]); line([0.5, 0.6], [0.43, 0.88]); line([0.5, 0.6], [0.57, 0.88]); line([0.5, 0.33], [0.39, 0.58]); line([0.5, 0.33], [0.61, 0.58]); }
}

export const FEU_PROPS = {
  // The French pedestrian signal (pivot at the foot of its pole, lenses +Z): a dark housing on a grey pole, a red standing man over a green walking
  // man in square lenses with visors; o.state [[t, 'r' | 'g' | 'off'], ...]; the lit lens glows with a halo and pops when it comes on; o.web: a
  // spider's web across the green lens; o.h the height of the pole to the housing, o.s its size (1: lenses 34 cm)
  pedSignal(o) {
    const Hp = o.h ?? 2.3, s = o.s ?? 1, g = grp(), hw = 0.46 * s, hh = 0.96 * s, hd = 0.24 * s, LS = 0.34 * s, zf = hd / 2 + 0.004;
    g.add(at(cyl(0.05, 0.06, Hp + hh * 0.3, '#4A5058', 8, { pivot: 'bottom' }), 0, 0, -hd / 2 - 0.05));
    const head = grp(at(box(hw, hh, hd, '#17191E', { outline: 0.012 }), 0, 0, 0)); head.position.set(0, Hp + hh / 2, 0); g.add(head);
    const lens = {};
    for (const [k, y, col, dark, walk] of [['r', hh * 0.24, '#FF3B2F', '#3A1210', false], ['g', -hh * 0.24, '#3EE06A', '#0F3A1C', true]]) {
      const lit = canvasPlane(LS, LS, (c, W, H) => pedMan(c, W, H, col, walk), { res: 256, emissive: 1.0 }), off = canvasPlane(LS, LS, (c, W, H) => pedMan(c, W, H, dark, walk), { res: 256 });
      lit.position.set(0, y, zf); off.position.set(0, y, zf); head.add(lit, off);
      const halo = new THREE.Mesh(new THREE.CircleGeometry(LS * 0.95, 20), new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0, depthWrite: false })); halo.position.set(0, y, zf + 0.012); head.add(halo);
      head.add(at(box(LS * 1.08, 0.025, 0.11 * s, '#17191E'), 0, y + LS * 0.56, zf + 0.05));
      lens[k] = { lit, off, halo };
    }
    if (o.web) { const m = new THREE.LineBasicMaterial({ color: '#F4F4F0', transparent: true, opacity: 0.85 }), R = LS * 0.66, wy = -hh * 0.24, z = zf + 0.02, V = (x, y) => new THREE.Vector3(x, y, z);
      for (let i = 0; i < 8; i++) { const a = i / 8 * TAU; head.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([V(0, wy), V(Math.cos(a) * R, wy + Math.sin(a) * R)]), m)); }
      for (let k = 1; k <= 4; k++) { const pts = []; for (let i = 0; i <= 8; i++) { const a = i / 8 * TAU, rr = R * k / 4.4; pts.push(V(Math.cos(a) * rr, wy + Math.sin(a) * rr)); } head.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), m)); } }
    const st = o.state || [[0, 'r']];
    g.userData.update = t => { let i = 0; for (let j = 0; j < st.length; j++) if (st[j][0] <= t) i = j; const on = st[i][1], u = t - st[i][0];
      for (const k of ['r', 'g']) { const L_ = lens[k], isOn = k === on; L_.lit.visible = isOn; L_.off.visible = !isOn; L_.halo.material.opacity = isOn ? 0.3 : 0;
        const p = isOn && i > 0 ? 1 + 0.3 * Math.max(0, 1 - u / 0.08) : 1; L_.lit.scale.set(p, p, 1); } };
    g.userData.update(0); return g;
  },

  // A beard of hair (pivot at the chin, hanging down -Y): o.n clumps (9), each a chain of tapered segments that waves and bulges forward over the
  // chest (o.bulge), fuller at the chin, grey-white with darker strands; o.len long (the ground), the middle clumps curl forward on the ground over
  // o.coil; o.swing [t0, t1, amp]: it swings about the chin (a walk); grow it with scale keys
  beardHair(o) {
    const n = o.n ?? 9, len = o.len ?? 1.3, coil = o.coil ?? 0.3, g = grp(), sw = grp(); g.add(sw);
    const mats = [L(o.color || '#D3CEC4'), L(o.dark || '#958E84')], r0 = o.r ?? 0.034, W = o.w ?? 0.22, strands = [];
    for (let i = 0; i < n; i++) {
      const u0 = n > 1 ? i / (n - 1) - 0.5 : 0, x0 = u0 * W, ph = hash(i + 3) * TAU, amp = 0.012 + 0.01 * hash(i + 7), Ln = len * (0.86 + 0.14 * (1 - Math.abs(u0) * 1.6)), pts = [];
      for (let k = 0; k <= 12; k++) { const u = k / 12; pts.push(new THREE.Vector3(x0 * (1 - 0.45 * u) + amp * Math.sin(u * 9 + ph), -Ln * u, 0.03 + (o.bulge ?? 0.14) * Math.sin(PI * Math.min(1, u * 1.12)))); }
      if (coil > 0 && Math.abs(u0) < 0.3) { const e = pts[pts.length - 1]; for (let k = 1; k <= 6; k++) { const a = k / 6 * PI * 1.4; pts.push(new THREE.Vector3(e.x + Math.sin(a) * coil * 0.25, e.y + 0.012, e.z + coil * (0.5 - 0.5 * Math.cos(a * 0.75)))); } }
      const ms = [];
      for (let k = 0; k < pts.length - 1; k++) { const m = seg(pts[k], pts[k + 1], r0 * (1 - 0.78 * k / (pts.length - 1)), r0 * (1 - 0.78 * (k + 1) / (pts.length - 1)), mats[i % 2]); sw.add(m); ms.push(m); }
      strands.push({ pts, ms, len: ms.map((m, k) => pts[k + 1].distanceTo(pts[k])) });
    }
    const dv = new THREE.Vector3(), p2 = Array.from({ length: 48 }, () => new THREE.Vector3());
    // o.swing [t0, t1, amp]: it swings from t0 and, after t1, the swing dies away over about a second (it snapped straight at t1); o.whip: each point
    // turns about the chin by an angle that grows toward the tip and lags behind it, so the beard bends like hair (one rigid swing read as a scythe)
    g.userData.update = t => { const s = o.swing; if (!s) return;
      const A = s[2] ?? 0.15, u = t - s[0], env = t <= s[0] ? 0 : t < s[1] ? 1 : Math.exp(-(t - s[1]) * 3.5);
      if (!o.whip) { const w = A * env * Math.sin(u * 7); sw.rotation.x = w; sw.rotation.z = 0.4 * w; return; }
      for (const S of strands) { const N = S.pts.length;
        for (let k = 0; k < N; k++) { const f = k / (N - 1), a = env * A * (0.3 + 0.9 * f) * Math.sin(u * 7 - 1.8 * f), b = 0.4 * a, P0 = S.pts[k];
          const y1 = P0.y * Math.cos(a) - P0.z * Math.sin(a), z1 = P0.y * Math.sin(a) + P0.z * Math.cos(a);
          p2[k].set(P0.x * Math.cos(b) - y1 * Math.sin(b), P0.x * Math.sin(b) + y1 * Math.cos(b), z1); }
        for (let k = 0; k < N - 1; k++) { const m = S.ms[k]; dv.copy(p2[k + 1]).sub(p2[k]); const l = dv.length(); m.position.copy(p2[k]).add(p2[k + 1]).multiplyScalar(0.5);
          m.quaternion.setFromUnitVectors(UP, dv.multiplyScalar(1 / Math.max(1e-5, l))); m.scale.y = l / Math.max(1e-5, S.len[k]); } } };
    g.userData.update(0); return g;
  },

  // A woven nest of twigs (pivot at its bottom middle): sixty-four twigs laid round a bowl in three courses over a dark hollow; o.max eggs (3) pop in
  // with a squash at the o.layAt times
  twigNest(o) {
    const R = o.r ?? 0.36, g = grp(), cols = ['#8A6236', '#A27A47', '#6E4C2A', '#B88E58'];
    g.add(at(new THREE.Mesh(new THREE.SphereGeometry(R * 0.82, 14, 8, 0, TAU, PI / 2, PI / 2), L('#4A3220')), 0, R * 0.42, 0));
    for (let i = 0; i < 64; i++) { const a = i * 2.399, lay = i % 3, rr = R * (0.78 + 0.12 * lay), tw = box(R * (0.7 + 0.4 * hash(i)), 0.016, 0.016, cols[i % 4]);
      tw.position.set(Math.cos(a) * rr, 0.06 + lay * R * 0.16 + 0.02 * hash(i + 5), Math.sin(a) * rr); tw.rotation.set((hash(i + 1) - 0.5) * 0.6, -a + PI / 2 + (hash(i + 2) - 0.5) * 0.5, (hash(i + 3) - 0.5) * 0.5); g.add(tw); }
    const eggs = [], nE = o.max ?? 3, lay = [].concat(o.layAt ?? []);
    for (let i = 0; i < nE; i++) { const a = i * 2.1 + 0.4, e = ball(R * 0.17, '#EEF3F2', 10); e.position.set(Math.cos(a) * R * 0.32, R * 0.44, Math.sin(a) * R * 0.32); g.add(e); eggs.push(e); }
    g.userData.update = t => { eggs.forEach((e, i) => { if (!lay.length) { e.visible = true; e.scale.set(1, 1.3, 1); return; } const u = t - lay[Math.min(i, lay.length - 1)];
      const k = u < 0 ? 0 : u < 0.06 ? u / 0.06 * 1.25 : u < 0.14 ? 1.25 - 0.25 * (u - 0.06) / 0.08 : 1, sq = u > 0 && u < 0.12 ? 0.82 : 1;
      e.visible = k > 0.01; e.scale.set(k / Math.sqrt(sq), 1.3 * k * sq, k / Math.sqrt(sq)); }); };
    g.userData.update(0); return g;
  },

  // Dust that bursts off him and falls (pivot at the burst point): o.n solid outlined puffs (18) thrown out at o.at, falling o.floor metres to the
  // ground and sliding to a stop, shrinking away over o.life (translucent shards hovering at his shoulders read as a render glitch)
  dustFall(o) {
    const n = o.n ?? 18, g = grp(), fl = o.floor ?? 1.2, life = o.life ?? 1.0, m = L(o.color || '#CFC6B4'), puffs = [];
    for (let i = 0; i < n; i++) { const p = new THREE.Mesh(new THREE.IcosahedronGeometry((o.r ?? 0.07) * (0.6 + 0.8 * hash(i)), 1), m), ol = new THREE.Mesh(p.geometry, inkM); ol.scale.setScalar(1.12); p.add(ol); p.visible = false; g.add(p);
      const a = i * 2.399; puffs.push({ p, v: [Math.cos(a) * (0.5 + 0.6 * hash(i + 4)), 0.3 + 0.9 * hash(i + 6), Math.sin(a) * (0.4 + 0.5 * hash(i + 8))], d: 0.03 * hash(i + 9) }); }
    g.userData.update = t => { for (const q of puffs) { const u = t - (o.at ?? 0) - q.d, on = u >= 0 && u < life; q.p.visible = on; if (!on) continue;
      const y = Math.max(-fl, q.v[1] * u - 4.9 * u * u), sl = y <= -fl ? 0.35 : 1; q.p.position.set(q.v[0] * u * sl, y, q.v[2] * u * sl);
      q.p.scale.setScalar((0.6 + 0.8 * Math.min(1, u / 0.12)) * (1 - 0.6 * clamp01((u - life * 0.6) / (life * 0.4)))); } };
    g.userData.update(-1); return g;
  },

  // Two cartoon tear fountains (pivot between the eyes; attach to the head joint): from each eye (o.dx either side, o.y up) a stream of outlined blue
  // drops arcs out sideways and falls, o.rate drops a second each side, from o.at to o.until
  tearFountain(o) {
    const g = grp(), dx = o.dx ?? 0.09, rate = o.rate ?? 14, life = o.life ?? 0.55, sp = o.speed ?? 1.4, R = o.r ?? 0.018, nPer = Math.ceil(rate * life) + 1;
    const m = new THREE.MeshLambertMaterial({ color: '#5FB4F0', emissive: '#1E5FA8', emissiveIntensity: 0.4 }), ink = new THREE.MeshBasicMaterial({ color: '#123A63', side: THREE.BackSide });
    const mk = () => { const b = new THREE.Mesh(new THREE.SphereGeometry(R, 8, 6), m), tip = new THREE.Mesh(new THREE.ConeGeometry(R * 0.94, R * 2.4, 8), m); tip.position.y = R * 1.25;
      const ol = new THREE.Mesh(b.geometry, ink); ol.scale.setScalar(1.25); return grp(b, tip, ol); };
    const drops = []; for (const sd of [-1, 1]) for (let i = 0; i < nPer; i++) { const d = mk(); d.visible = false; g.add(d); drops.push({ d, sd, i }); }
    const vel = new THREE.Vector3(), per = nPer / rate;
    g.userData.update = t => { const t0 = o.at ?? 0, t1 = o.until ?? 1e9;
      for (const q of drops) { let b = t0 + q.i / rate; if (t >= b) b += Math.floor((t - b) / per) * per; const u = t - b, on = t >= t0 && b <= t1 && u >= 0 && u < life; q.d.visible = on; if (!on) continue;
        const vx = q.sd * sp * (0.9 + 0.2 * hash(q.i)), vy = sp * 0.55, vz = sp * 0.25; q.d.position.set(q.sd * dx + vx * u, (o.y ?? 0) + vy * u - 4.9 * u * u, vz * u);
        vel.set(vx, vy - 9.8 * u, vz); q.d.quaternion.setFromUnitVectors(UP, vel.normalize().negate()); } };
    g.userData.update(-1); return g;
  },

  // A big ticket (pivot at its middle, front +Z): pink paper, AMENDE on a red band across the top, ruled lines, the sum in big figures, a blue stamp
  bigTicket(o) {
    const w = o.w ?? 0.34, h = o.h ?? 0.48;
    const face = canvasPlane(w, h, (c, W, H) => { c.fillStyle = o.color || '#F6C7D2'; c.fillRect(0, 0, W, H); c.fillStyle = '#C8322A'; c.fillRect(0, 0, W, H * 0.18);
      c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillStyle = '#FFFFFF'; fit(c, o.title || 'AMENDE', W / 2, H * 0.095, H * 0.12, W * 0.86);
      c.strokeStyle = '#9A6A76'; c.lineWidth = H * 0.008; for (let i = 0; i < 4; i++) { c.beginPath(); c.moveTo(W * 0.1, H * (0.3 + i * 0.08)); c.lineTo(W * 0.9, H * (0.3 + i * 0.08)); c.stroke(); }
      c.fillStyle = '#16181C'; fit(c, o.sum || '135 €', W / 2, H * 0.74, H * 0.2, W * 0.84);
      c.strokeStyle = '#2F62B5'; c.lineWidth = H * 0.012; c.beginPath(); c.arc(W * 0.8, H * 0.9, H * 0.06, 0, TAU); c.stroke(); }, { res: 512 });
    face.position.z = 0.002; return grp(at(box(w, h, 0.003, '#EAD3D8'), 0, 0, 0), face);
  },

  // The little house the town hall built round him (pivot on the floor in the middle of its doorway, the doorway +Z): cream walls o.w x o.d x o.h, a
  // zinc roof with a chimney, a doorway with no door where he stands, a window with a box of red flowers, a little blue number plate, a doormat
  kerbHouse(o) {
    const W = o.w ?? 2.4, D = o.d ?? 2.0, H = o.h ?? 2.75, dw = o.door ?? 1.0, dh = o.doorH ?? 2.62, t = 0.12, g = grp(), cream = o.color || '#F1E6CF', side = (W - dw) / 2, rise = o.rise ?? 0.9;
    g.add(at(box(side, H, t, cream, { outline: 0.006 }), -(dw / 2 + side / 2), H / 2, 0), at(box(side, H, t, cream, { outline: 0.006 }), dw / 2 + side / 2, H / 2, 0), at(box(dw, H - dh, t, cream), 0, dh + (H - dh) / 2, 0));
    g.add(at(box(dw + 0.16, 0.08, t + 0.06, '#C9B48E'), 0, dh + 0.04, 0.02), at(box(W, H, t, cream), 0, H / 2, -D), at(box(t, H, D, cream), -W / 2, H / 2, -D / 2), at(box(t, H, D, cream), W / 2, H / 2, -D / 2));
    const tri = new THREE.ShapeGeometry(new THREE.Shape([new THREE.Vector2(0, 0), new THREE.Vector2(-D, 0), new THREE.Vector2(-D / 2, rise)]));
    for (const sd of [-1, 1]) { const gm = new THREE.Mesh(tri, new THREE.MeshLambertMaterial({ color: cream, side: THREE.DoubleSide })); gm.rotation.y = -PI / 2; gm.position.set(sd * W / 2, H, 0); g.add(gm); }
    const rl = Math.hypot(D / 2 + 0.2, rise), ang = Math.atan2(rise, D / 2 + 0.2);
    for (const sd of [-1, 1]) { const sl = box(W + 0.3, 0.07, rl, o.roof || '#8E979F', { outline: 0.008 }); sl.position.set(0, H + rise / 2, -D / 2 + sd * (D / 4 + 0.1)); sl.rotation.x = sd * ang; g.add(sl); }
    g.add(at(box(0.34, 0.9, 0.34, '#B8573E', { outline: 0.006 }), W * 0.28, H + rise * 0.7, -D * 0.7), at(box(0.42, 0.08, 0.42, '#8E979F'), W * 0.28, H + rise * 0.7 + 0.46, -D * 0.7));
    const wx = -(dw / 2 + side / 2);
    g.add(at(box(0.5, 0.6, 0.05, '#2F7F86'), wx, 1.65, t / 2 + 0.01), at(box(0.42, 0.52, 0.05, '#BFE3EA'), wx, 1.65, t / 2 + 0.02), at(box(0.56, 0.14, 0.2, '#7A4E2A'), wx, 1.28, t / 2 + 0.1));
    for (let i = 0; i < 5; i++) g.add(at(ball(0.05, i % 2 ? '#E0413A' : '#F2C230', 7), wx - 0.2 + i * 0.1, 1.4, t / 2 + 0.12));
    const plate = canvasPlane(0.2, 0.15, (c, Wc, Hc) => { c.fillStyle = '#1F3B73'; c.fillRect(0, 0, Wc, Hc); c.strokeStyle = '#FFFFFF'; c.lineWidth = Wc * 0.05; c.strokeRect(Wc * 0.06, Hc * 0.08, Wc * 0.88, Hc * 0.84);
      c.fillStyle = '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle'; fit(c, o.number || '1', Wc / 2, Hc * 0.54, Hc * 0.62, Wc * 0.7); }, { res: 128 });
    plate.position.set(dw / 2 + side / 2, 2.0, t / 2 + 0.01); g.add(plate);
    g.add(at(box(0.9, 0.02, 0.5, '#8A5A3A'), 0, 0.01, 0.3));
    return g;
  },

  // A heap of letters on the ground (pivot at its middle): o.n envelopes (24), white and a few tinted, lying at random angles, piled higher in the
  // middle, o.r across
  letterPile(o) {
    const g = grp(), n = o.n ?? 24, R = o.r ?? 0.3, cols = ['#F7F4EC', '#F7F4EC', '#F2E6C8', '#DCE8F4', '#F6D9DF'];
    for (let i = 0; i < n; i++) { const e = box(0.22, 0.006, 0.14, cols[i % 5], { outline: 0.004 }), a = i * 2.399, rr = R * Math.sqrt(hash(i));
      e.position.set(Math.cos(a) * rr, 0.004 + 0.009 * Math.floor(i * 0.5) * (1 - rr / R), Math.sin(a) * rr); e.rotation.set((hash(i + 1) - 0.5) * 0.3, hash(i + 2) * TAU, (hash(i + 3) - 0.5) * 0.3); g.add(e); }
    return g;
  },

  // A reporter's microphone held out (pivot at the grip, the head +Z): a black stick, a grey ball head, a cube flag in o.color with o.text on its sides
  pressMic(o) {
    const g = grp(at(cyl(0.016, 0.02, 0.24, '#1C1D22', 8), 0, 0, 0.07, PI / 2, 0, 0), at(ball(0.048, '#4A4E56', 10), 0, 0, 0.22), at(box(0.09, 0.07, 0.09, o.color || '#C8322A'), 0, 0, 0.13));
    for (const sd of [-1, 1]) { const f = canvasPlane(0.09, 0.07, (c, W, H) => { c.fillStyle = o.color || '#C8322A'; c.fillRect(0, 0, W, H); c.fillStyle = '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle'; fit(c, o.text || 'INFO', W / 2, H * 0.55, H * 0.55, W * 0.86); }, { res: 128 });
      f.position.set(sd * 0.0465, 0, 0.13); f.rotation.y = sd * PI / 2; g.add(f); }
    g.userData.grip = [0, 0, 0]; return g;
  },

  // A sound boom (pivot at the hand, the pole along +Z and up o.tilt): a grey pole o.len long, a furry grey windshield at its end
  boomMic(o) {
    const len = o.len ?? 2.2, g = grp(), arm = grp(at(cyl(0.018, 0.018, len, '#7A7F87', 6), 0, 0, len / 2, PI / 2, 0, 0));
    const fur = new THREE.Mesh(new THREE.CapsuleGeometry(0.07, 0.28, 4, 8), L('#8C8C88')); fur.rotation.x = PI / 2; fur.position.z = len + 0.12; arm.add(fur);
    arm.rotation.x = -(o.tilt ?? 0.5); g.add(arm); return g;
  },

  // Confetti raining down (pivot at the bottom middle of its box o.w x o.h x o.d): o.n pieces (160) of six colours, already spread through the box,
  // falling and fluttering from o.at, looping (the burst of 66's draft 1 was specks: another confetti prop of the same name won)
  confettiRain(o) {
    const n = o.n ?? 160, W = o.w ?? 3, H = o.h ?? 3, D = o.d ?? 1, sp = o.speed ?? 1.2, g = grp(), cols = o.colors || ['#E0413A', '#F2C230', '#3A7BD5', '#4CC26A', '#F28CC2', '#FFFFFF'];   // (review 2 of 67) o.colors: the paper colours (tricolour)
    const geo = new THREE.PlaneGeometry(o.s ?? 0.07, (o.s ?? 0.07) * 0.65), pcs = [];
    for (let i = 0; i < n; i++) { const m = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ color: cols[i % cols.length], side: THREE.DoubleSide })); m.visible = false; g.add(m);
      pcs.push({ m, x: (hash(i) - 0.5) * W, z: (hash(i + 1) - 0.5) * D, ph: hash(i + 2), v: sp * (0.7 + 0.6 * hash(i + 3)), sw: 0.08 + 0.1 * hash(i + 4) }); }
    g.userData.update = t => { const u = t - (o.at ?? 0); for (const p of pcs) { p.m.visible = u >= 0; if (u < 0) continue; const y = H - ((u * p.v + p.ph * H) % H);
      p.m.position.set(p.x + p.sw * Math.sin(u * 5 + p.ph * 9), y, p.z + p.sw * Math.cos(u * 4 + p.ph * 7)); p.m.rotation.set(u * 7 + p.ph * 9, u * 5 + p.ph * 3, u * 3); } };
    g.userData.update(-1); return g;
  },

  // Dark glasses (pivot at the bridge, front +Z; attach to the head joint): two black lenses, a bridge, the temples; o.ear (default on): a curled white
  // wire from the right temple down toward the collar (bodyguards in red caps and grey jackets read as tourists)
  shades(o) {
    const s = o.s ?? 1, g = grp(), m = new THREE.MeshPhongMaterial({ color: '#0E0F12', shininess: 90 });
    for (const sd of [-1, 1]) { const l = new THREE.Mesh(new THREE.BoxGeometry(0.1 * s, 0.055 * s, 0.012 * s), m); l.position.set(sd * 0.062 * s, 0, 0); g.add(l, at(box(0.008 * s, 0.008 * s, 0.16 * s, '#16181C'), sd * 0.115 * s, 0.01 * s, -0.08 * s)); }
    g.add(at(box(0.03 * s, 0.01 * s, 0.01 * s, '#16181C'), 0, 0.012 * s, 0));
    if (o.ear !== false) { const pts = []; for (let i = 0; i <= 24; i++) { const u = i / 24; pts.push(new THREE.Vector3(-0.12 * s + 0.012 * s * Math.cos(u * 30), -0.02 * s - 0.2 * s * u, -0.12 * s + 0.012 * s * Math.sin(u * 30))); }
      g.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 48, 0.004 * s, 5, false), L('#D8D4CC'))); }
    return g;
  },

  // A spider's thread (pivot at its top, hanging down -Y): its length follows o.keys [[t, len, dur, ease ('in' | 'out' | 'inOut')], ...] from the
  // length before (a spider that drops and bounces on it); length 0: not there
  thread(o) {
    const g = grp(), m = new THREE.Mesh(new THREE.CylinderGeometry(o.r ?? 0.004, o.r ?? 0.004, 1, 4), new THREE.MeshBasicMaterial({ color: o.color || '#F4F4F0' })); m.geometry.translate(0, -0.5, 0); g.add(m);
    const ks = o.keys || [[0, 1, 0]], E = { in: u => u * u, out: u => 1 - (1 - u) * (1 - u), inOut: u => u < 0.5 ? 2 * u * u : 1 - 2 * (1 - u) * (1 - u) };
    g.userData.update = t => { let len = ks[0][1]; for (let i = 1; i < ks.length; i++) { const [t0, l1, d, e] = ks[i]; if (t < t0) break; const u = d ? clamp01((t - t0) / d) : 1; len = len + (l1 - len) * (E[e] || E.inOut)(u); }
      m.visible = len > 0.005; m.scale.set(1, Math.max(0.005, len), 1); };
    g.userData.update(0); return g;
  },

  // A tricolour cockade for a lapel (pivot at its middle, front +Z): three discs, red outside, white, blue at the middle, o.r across
  cockade(o) { const r = o.r ?? 0.035, g = grp(); [['#E0413A', 1], ['#F4F4F0', 0.66], ['#2F62B5', 0.33]].forEach(([c, k], i) => { const d = new THREE.Mesh(new THREE.CircleGeometry(r * k, 16), L(c)); d.position.z = 0.002 * (i + 1); g.add(d); }); return g; },
};
