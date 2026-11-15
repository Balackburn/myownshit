// « Le bus » (story 72): this man missed his bus by two seconds and ran after it for three years, escorted by the gendarmes, followed by the cycle
// race, fed by an Italian waiter on the run; when the bus stopped he got on: it was not his bus. Conventions as in props.js (metres, front +Z, pivot
// at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const hash = i => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

export const BUS_PROPS = {
  // A French town sign on its post (front +Z): a white plate with a red border and the town's name; o.exit: the red bar across it (leaving the
  // town); o.name, o.w (1.3), o.h (post height to the plate's bottom, 1.5)
  townSign(o) {
    const w = o.w ?? 1.3, ph = w * 0.42, y = o.h ?? 1.5, g = grp();
    g.add(at(box(0.07, y + ph, 0.07, '#8E949A', { pivot: 'bottom' }), 0, 0, -0.06));
    const face = canvasPlane(w, ph, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.strokeStyle = '#D22B2B'; c.lineWidth = H * 0.1; c.strokeRect(H * 0.07, H * 0.07, W - H * 0.14, H - H * 0.14);
      c.fillStyle = '#17181C'; c.textAlign = 'center'; c.textBaseline = 'middle'; let fs = H * 0.42; c.font = `900 ${fs}px Arial`; const tw = c.measureText(o.name || 'VILLE').width; if (tw > W * 0.82) { fs *= W * 0.82 / tw; c.font = `900 ${fs}px Arial`; }
      c.fillText(o.name || 'VILLE', W / 2, H * 0.53);
      if (o.exit) { c.strokeStyle = '#D22B2B'; c.lineWidth = H * 0.12; c.beginPath(); c.moveTo(W * 0.08, H * 0.88); c.lineTo(W * 0.92, H * 0.12); c.stroke(); } }, { res: 512 });
    g.add(at(box(w + 0.04, ph + 0.04, 0.03, '#C9CDD2', { outline: 0.006 }), 0, y + ph / 2, 0)); face.position.set(0, y + ph / 2, 0.017); g.add(face);
    return g;
  },

  // A race number to pin on a back or a chest (pivot at its middle, front +Z): a white bib with the number o.num big in black, a red strip along
  // the top and four safety pins at the corners, o.w x o.h (0.26 x 0.2)
  raceBib(o) {
    const w = o.w ?? 0.26, h = o.h ?? 0.2, g = grp();
    const face = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.fillStyle = '#D22B2B'; c.fillRect(0, 0, W, H * 0.16);
      c.fillStyle = '#16181C'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${H * 0.62}px Arial`; c.fillText(String(o.num ?? '1'), W / 2, H * 0.6); }, { res: 256 });
    g.add(at(box(w, h, 0.004, '#F4F4F0'), 0, 0, 0)); face.position.z = 0.003; g.add(face);
    for (const [x, y] of [[-1, 1], [1, 1], [-1, -1], [1, -1]]) g.add(at(sphere(0.008, '#C9CDD2', 0), x * (w / 2 - 0.018), y * (h / 2 - 0.018), 0.006));
    return g;
  },

  // The yellow jersey thrown over his suit (pivot at the bottom middle of his torso, front +Z): a yellow shell o.w x o.h x o.d (0.5 x 0.6 x 0.3)
  // with short sleeves and a black collar band; o.at: it drops on from above at that time, squashing down onto his shoulders (before it, hidden)
  jersey(o) {
    const w = o.w ?? 0.5, h = o.h ?? 0.6, d = o.d ?? 0.3, Y = o.color || '#F7D23A', g = grp(), shell = grp(); g.add(shell);
    shell.add(at(box(w, h, d, Y, { outline: 0.008 }), 0, h / 2, 0), at(box(w * 0.42, 0.05, d * 1.02, '#1C1E22'), 0, h - 0.02, 0));
    for (const s of [-1, 1]) shell.add(at(box(0.16, 0.16, d * 0.9, Y, { outline: 0.006 }), s * (w / 2 + 0.06), h - 0.1, 0));
    g.userData.update = t => { if (o.at == null) return; const u = t - o.at; shell.visible = u >= 0; if (u < 0) return;
      const f = clamp01(u / 0.12); shell.position.y = (1 - f) * 0.6; const sq = u < 0.12 ? 1 : 1 + 0.18 * Math.exp(-14 * (u - 0.12)) * Math.cos((u - 0.12) * 30); shell.scale.set(2 - sq, sq, 2 - sq); };
    g.userData.update(-1); return g;
  },

  // A plate of spaghetti held out (pivot at the plate's middle): a white plate, a yellow nest of noodles and two meatballs; o.noodle [x, y, z]
  // (local): one long noodle from the nest to that point (his mouth), slurped in between o.slurp [t0, t1] (it shortens to nothing, wobbling)
  pastaPlate(o) {
    const g = grp(), Rp = o.r ?? 0.14;
    g.add(at(cyl(Rp, Rp * 0.8, 0.025, '#F7F5EF', 20, { outline: 0.004 }), 0, 0, 0));
    for (let i = 0; i < 9; i++) { const a = i * 0.7, rr = Rp * (0.25 + 0.45 * hash(i)); const t = new THREE.Mesh(new THREE.TorusGeometry(Rp * 0.22, 0.008, 5, 14), new THREE.MeshLambertMaterial({ color: '#F2D27A' }));
      t.position.set(Math.cos(a) * rr * 0.6, 0.025 + 0.012 * (i % 3), Math.sin(a) * rr * 0.6); t.rotation.set(PI / 2 + 0.3 * (hash(i + 4) - 0.5), 0, a); g.add(t); }
    for (const x of [-0.035, 0.04]) g.add(at(sphere(0.022, '#8A3B26', 1), x, 0.06, 0.01));
    if (o.noodle) { const N = 14, segs = [], m = new THREE.MeshLambertMaterial({ color: '#F2D27A' }); for (let i = 0; i < N; i++) { const s = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 1, 5), m); g.add(s); segs.push(s); }
      const A = new THREE.Vector3(0, 0.05, 0), B = new THREE.Vector3(...o.noodle), p = new THREE.Vector3(), q = new THREE.Vector3(), d = new THREE.Vector3();
      const pt = (u, t, out) => { out.lerpVectors(A, B, u); out.y += Math.sin(u * PI) * 0.06 + 0.012 * Math.sin(u * 18 + t * 30) * (1 - u); return out; };
      g.userData.update = t => { const [t0, t1] = o.slurp || [1e9, 1e9], k = clamp01((t - t0) / (t1 - t0)), u0 = k;   // the eaten part comes off the plate end
        for (let i = 0; i < N; i++) { const ua = u0 + (1 - u0) * i / N, ub = u0 + (1 - u0) * (i + 1) / N; pt(ua, t, p); pt(ub, t, q); d.subVectors(q, p); const L = d.length(), s = segs[i];
          s.visible = k < 0.999 && L > 1e-4; s.position.copy(p).add(q).multiplyScalar(0.5); s.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize()); s.scale.set(1, L, 1); } };
      g.userData.update(0); }
    return g;
  },

  // A heap of worn-out shoes by the road (pivot at the floor middle): o.n (60) shoes, brown and black, each with a pale sole and a hole, piled in a
  // cone o.r round (0.9) and o.h high (0.8)
  shoePile(o) {
    const n = o.n ?? 60, R = o.r ?? 0.9, H = o.h ?? 0.8, g = grp(), cols = ['#5A3A24', '#2B2620', '#7A4E2C', '#3E3A36'];
    for (let i = 0; i < n; i++) { const f = i / n, rr = R * Math.sqrt(1 - f) * (0.4 + 0.6 * hash(i + 2)), a = i * 2.399, y = H * f * 0.95;
      const sh = grp(at(box(0.26, 0.09, 0.1, cols[i % 4], { outline: 0.004 }), 0, 0.05, 0), at(box(0.27, 0.025, 0.105, '#D8CFBF'), 0, 0.0, 0), at(box(0.1, 0.05, 0.08, cols[(i + 1) % 4]), -0.07, 0.11, 0));
      sh.position.set(Math.cos(a) * rr, y, Math.sin(a) * rr); sh.rotation.set(0.5 * (hash(i + 5) - 0.5), a + hash(i) * 2, 0.6 * (hash(i + 9) - 0.5)); g.add(sh); }
    return g;
  },
};
