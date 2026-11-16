// « Le bus » (story 72): this man missed his bus by two seconds and ran after it for three years, escorted by the gendarmes, followed by the cycle
// race, fed by an Italian waiter on the run; when the bus stopped he got on: it was not his bus. Conventions as in props.js (metres, front +Z, pivot
// at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere } from './style.js';
import { grp, at, canvasPlane, glowSprite } from './props.js';
import { FEU_PROPS } from './props_feu.js';   // (pass 3) the beard of story 66, wrapped by streamBeard

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const hash = i => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

// (pass 3 of 72) One shoe with a readable profile, toe toward +X, pivot under its middle: kind 'sneaker' | 'boot' | 'brogue', the upper in col, L
// long; worn: the sole gapes open at the toe and a hole shows on the side (used by bigShoe and shoeHeap)
function shoeMesh(kind, col, L, worn, seed) {
  const g = grp(), Wd = L * 0.38, soleC = kind === 'sneaker' ? '#F4F1E8' : kind === 'boot' ? '#2A2622' : '#3A2A1E', sh = L * 0.09;
  const so = grp(at(box(L, sh, Wd, soleC, { outline: 0.004 }), L / 2, 0, 0)); so.position.set(-L / 2, sh / 2, 0); if (worn) so.rotation.z = -0.3; g.add(so);
  if (kind === 'boot') {
    g.add(at(box(L * 0.85, L * 0.22, Wd, col, { outline: 0.005 }), 0, sh + L * 0.11, 0), at(box(L * 0.38, L * 0.55, Wd * 0.95, col, { outline: 0.005 }), -L * 0.25, sh + L * 0.22 + L * 0.27, 0));
    for (let i = 0; i < 4; i++) g.add(at(box(0.008, 0.008, Wd * 0.6, '#E9DCC0'), -L * 0.06, sh + L * (0.28 + 0.12 * i), 0));
  } else if (kind === 'brogue') {
    g.add(at(box(L * 0.22, L * 0.1, Wd * 0.9, '#22180F'), -L * 0.36, sh + L * 0.05, 0), at(box(L * 0.86, L * 0.18, Wd * 0.92, col, { outline: 0.005 }), -L * 0.02, sh + L * 0.14, 0));
    const cap = sphere(1, col, 1, { outline: 0.004 }); cap.scale.set(L * 0.2, L * 0.12, Wd * 0.47); cap.position.set(L * 0.36, sh + L * 0.1, 0); g.add(cap);
    g.add(at(box(L * 0.22, 0.008, Wd * 0.5, '#1A1410'), -L * 0.16, sh + L * 0.235, 0));
  } else {
    g.add(at(box(L * 0.7, L * 0.24, Wd * 0.95, col, { outline: 0.005 }), -L * 0.1, sh + L * 0.12, 0), at(box(L * 0.32, L * 0.14, Wd * 0.95, col, { outline: 0.005 }), L * 0.32, sh + L * 0.07, 0));
    g.add(at(box(L * 0.42, L * 0.045, Wd * 0.97, hash(seed + 2) > 0.5 ? '#FFFFFF' : '#1C1C1C'), -L * 0.05, sh + L * 0.1, 0), at(box(L * 0.2, 0.01, Wd * 0.62, '#1A1410'), -L * 0.28, sh + L * 0.245, 0));
    for (let i = 0; i < 3; i++) g.add(at(box(L * 0.04, 0.012, Wd * 0.72, '#FFFFFF'), L * (0.02 + 0.08 * i), sh + L * 0.245, 0));
  }
  if (worn) g.add(at(box(L * 0.12, L * 0.09, 0.006, '#120E0B'), L * 0.1, sh + L * 0.09, Wd / 2 + 0.004));
  return g;
}

export const BUS_PROPS = {
  // A French town sign on its post (front +Z): a white plate with a red border and the town's name; o.exit: the red bar across it (leaving the
  // town); o.name, o.w (1.3), o.h (post height to the plate's bottom, 1.5)
  // (pass 2) renamed from townSign: props_elan.js has a townSign (story 41), which this one, loaded after it, replaced
  exitSign(o) {
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
    const w = o.w ?? 0.5, h = o.h ?? 0.6, d = o.d ?? 0.3, Y = o.color || '#F7D23A', g = grp(), shell = grp(), em = o.lit ? { emissive: o.lit } : {}; g.add(shell);   // (pass 3) o.lit: an emissive colour (it stayed olive in the shade of a doorway)
    shell.add(at(box(w, h, d, Y, { outline: 0.008, ...em }), 0, h / 2, 0), at(box(w * 0.42, 0.05, d * 1.02, '#1C1E22'), 0, h - 0.02, 0));
    for (const s of [-1, 1]) shell.add(at(box(0.16, 0.16, d * 0.9, Y, { outline: 0.006, ...em }), s * (w / 2 + 0.06), h - 0.1, 0));
    // (pass 3) o.squash [hold, k]: on landing it squashes flat and wide to k (0.62) for hold s (0.12), then springs up past its size and settles
    g.userData.update = t => { if (o.at == null) return; const u = t - o.at; shell.visible = u >= 0; if (u < 0) return;
      const f = clamp01(u / 0.12); shell.position.y = (1 - f) * 0.6; let sq = u < 0.12 ? 1 : 1 + 0.18 * Math.exp(-14 * (u - 0.12)) * Math.cos((u - 0.12) * 30);
      if (o.squash && u >= 0.12) { const [hd, kq] = [o.squash[0] ?? 0.12, o.squash[1] ?? 0.62], v = u - 0.12; sq = v < hd ? kq : 1 + 0.22 * Math.exp(-11 * (v - hd)) * Math.cos((v - hd) * 24); }
      shell.scale.set(2 - sq, sq, 2 - sq); };
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
    if (o.core) g.add(cyl(R * 0.06, R * 0.8, H * 0.9, '#4A3526', 12, { pivot: 'bottom' }));   // (pass 2) o.core: a dark cone inside (a big heap of few shoes stays a heap, not a scatter)
    for (let i = 0; i < n; i++) { const f = i / n, rr = R * Math.sqrt(1 - f) * (0.4 + 0.6 * hash(i + 2)), a = i * 2.399, y = H * f * 0.95;
      const sh = grp(at(box(0.26, 0.09, 0.1, cols[i % 4], { outline: 0.004 }), 0, 0.05, 0), at(box(0.27, 0.025, 0.105, '#D8CFBF'), 0, 0.0, 0), at(box(0.1, 0.05, 0.08, cols[(i + 1) % 4]), -0.07, 0.11, 0));
      sh.position.set(Math.cos(a) * rr, y, Math.sin(a) * rr); sh.rotation.set(0.5 * (hash(i + 5) - 0.5), a + hash(i) * 2, 0.6 * (hash(i + 9) - 0.5)); g.add(sh); }
    return g;
  },

  // (pass 2 of 72) An LED destination plate (pivot at its middle, front +Z): heavy amber type on a black panel in a grey frame, o.text
  // ('21  ROME'), o.w x o.h (1.2 x 0.4); it glows by itself (it reads under the shade of a roof)
  busPlate(o) {
    const w = o.w ?? 1.2, h = o.h ?? 0.4, g = grp(), tx = o.text || '21  ROME';
    const face = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#0D0E11'; c.fillRect(0, 0, W, H); c.fillStyle = '#FFB21E'; c.textAlign = 'center'; c.textBaseline = 'middle';
      let fs = H * 0.8; c.font = `900 ${fs}px Arial`; const tw = c.measureText(tx).width; if (tw > W * 0.9) { fs *= W * 0.9 / tw; c.font = `900 ${fs}px Arial`; }
      c.fillText(tx, W / 2, H * 0.55); }, { res: 1024 });
    face.material = new THREE.MeshBasicMaterial({ map: face.material.map, toneMapped: false });
    g.add(at(box(w + 0.08, h + 0.08, 0.05, '#3A3E46', { outline: 0.008 }), 0, 0, 0)); face.position.z = 0.028; g.add(face);
    return g;
  },

  // (pass 2 of 72) A cartoon-size bus ticket (pivot at its middle, front +Z, printed on both sides): pale paper o.w x o.h (0.44 x 0.32) with a
  // thick ink edge, a blue band along the top with o.title ('LIGNE') and under it o.num ('12') as big as the paper allows; it glows by itself
  busTicket(o) {
    const w = o.w ?? 0.44, h = o.h ?? 0.32, g = grp();
    const draw = (c, W, H) => { c.fillStyle = o.paper || '#FFF4CF'; c.fillRect(0, 0, W, H); c.fillStyle = o.band || '#2F62B5'; c.fillRect(0, 0, W, H * 0.3);
      c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillStyle = '#FFFFFF'; c.font = `900 ${H * 0.24}px Arial`; c.fillText(o.title || 'LIGNE', W / 2, H * 0.165);
      c.fillStyle = '#14161A'; c.font = `900 ${H * 0.66}px Arial`; c.fillText(String(o.num ?? '12'), W / 2, H * 0.67);
      c.strokeStyle = '#14161A'; c.lineWidth = H * 0.06; c.strokeRect(H * 0.03, H * 0.03, W - H * 0.06, H - H * 0.06); };
    const f = canvasPlane(w, h, draw, { res: 768 }), b = canvasPlane(w, h, draw, { res: 256 });
    for (const m of [f, b]) m.material = new THREE.MeshBasicMaterial({ map: m.material.map, toneMapped: false });
    f.position.z = 0.005; b.position.z = -0.005; b.rotation.y = PI; g.add(at(box(w + 0.02, h + 0.02, 0.006, '#14161A'), 0, 0, 0), f, b);
    return g;
  },

  // (pass 2 of 72) A calf swollen like a balloon (pivot at the knee, hanging down -Y: put it on kneeL / kneeR): an egg o.r thick (0.21) and
  // o.len long (0.5), bulging to the back, in the trouser colour (o.color), throbbing. o.tape: a yellow measuring tape round its widest part.
  // o.grow [t0, t1]: it swells from a third of its size to all of it between those times, with a bounce (full from the start without it)
  bigCalf(o) {
    const R = o.r ?? 0.21, len = o.len ?? 0.5, g = grp(), b = grp(); g.add(b); b.position.set(0, -len * 0.48, -R * 0.3);
    const egg = sphere(1, o.color || '#2E3442', 2, o.outline ? { outline: o.outline } : {}); egg.scale.set(R, len * 0.54, R * 1.12); b.add(egg);
    let tp = null; if (o.tape) { tp = new THREE.Mesh(new THREE.TorusGeometry(1, 0.1, 6, 24), new THREE.MeshLambertMaterial({ color: '#F5CE2E' })); tp.rotation.x = PI / 2; tp.scale.set(R * (o.dig ?? 1.04), R * 1.16 * (o.dig ?? 1.04) / 1.04, 0.3); b.add(tp); }   // (pass 3) o.dig (1.04): under 1 the tape digs into the swelling
    // (pass 3) o.seam: a skin-coloured split down the back of the trouser leg that opens as it swells; o.snapAt: the tape snaps, its two ends whip off
    let seam = null; if (o.seam) { seam = sphere(1, o.seam, 1); seam.scale.set(R * 0.28, len * 0.4, R * 0.5); seam.position.set(0, 0, -R * 0.82); b.add(seam); }
    const ends = []; if (o.snapAt != null && tp) for (const s of [-1, 1]) { const e = at(box(R * 1.4, 0.05, 0.035, '#F5CE2E', { outline: 0.004 }), 0, 0, 0); e.visible = false; b.add(e); ends.push([e, s]); }
    g.userData.update = t => { let f = 1; if (o.grow) { const u = clamp01((t - o.grow[0]) / (o.grow[1] - o.grow[0])); f = 0.34 + 0.66 * (u >= 1 ? 1 + 0.12 * Math.exp(-9 * (t - o.grow[1])) * Math.cos((t - o.grow[1]) * 26) : u * u * (3 - 2 * u)); }
      if (o.pulses) { f = 0.34; let lv = 0.34; for (const [p0, p1, to] of o.pulses) { if (t < p0) break; const u = clamp01((t - p0) / (p1 - p0)); f = lv + (to - lv) * (u >= 1 ? 1 + 0.16 * Math.exp(-9 * (t - p1)) * Math.cos((t - p1) * 28) : u * u * (3 - 2 * u)); lv = to; } }
      const th = f * (1 + 0.04 * Math.sin(t * 11 + (o.phase ?? 0))); b.scale.set(th, 0.8 + 0.2 * f, th);
      if (seam) seam.scale.set(R * (0.12 + 0.3 * clamp01((f - 0.34) / 0.66)), len * 0.4, R * 0.5);
      if (o.snapAt != null && tp) { const v = t - o.snapAt; tp.visible = v < 0; ends.forEach(([e, s]) => { e.visible = v >= 0 && v < 0.6; if (!e.visible) return; e.position.set(s * (R * 0.9 + 1.6 * v), 0.6 * v - 3.0 * v * v, -0.3 * v); e.rotation.set(0, s * 9 * v, s * (0.4 + 6 * v)); }); } };
    g.userData.update(0); return g;
  },

  // (pass 2 of 72) A small blue beacon (pivot at its foot; `blueBeacon`: other stories have a `beacon`): a dark base and a blue dome o.r (0.07) that glows by itself, a pale spot turning
  // inside it o.rate turns a second (2). It puts no light on the scene (the two alternating lamps of policeFlash strobed the whole road)
  blueBeacon(o) {
    const R = o.r ?? 0.07, g = grp(), m = new THREE.MeshBasicMaterial({ color: '#1F5CFF' });
    const dome = new THREE.Mesh(new THREE.SphereGeometry(R, 10, 6, 0, TAU, 0, PI / 2), m), spot = new THREE.Mesh(new THREE.SphereGeometry(R * 0.42, 8, 6), new THREE.MeshBasicMaterial({ color: '#6FA8FF' }));   // (stills 4) deep blues, tone-mapped: the near-white spot bloomed into a pale pink disc
    dome.position.y = R * 0.5; g.add(at(cyl(R * 1.15, R * 1.15, R * 0.5, '#1C1E22', 10, { pivot: 'bottom' }), 0, 0, 0), dome, spot);
    g.userData.update = t => { const a = t * TAU * (o.rate ?? 2) + (o.phase ?? 0); spot.position.set(Math.cos(a) * R * 0.8, R * 0.95, Math.sin(a) * R * 0.8); m.color.set(Math.sin(a) > 0 ? '#2F6BFF' : '#1746C8'); };
    g.userData.update(0); return g;
  },

  // (pass 2 of 72) One long noodle as a thick yellow rope (pivot at its first end, the plate; o.to [x, y, z] its other end, his mouth; o.r thick,
  // 0.022): it flies up from the plate to the mouth between o.rise [t0, t1], stays stretched taut and trembling until o.snap, then lets go of the
  // plate and is sucked into the mouth in o.suck s (0.16), its free end whipping
  noodleRope(o) {
    const N = 16, g = grp(), R = o.r ?? 0.022, m = new THREE.MeshLambertMaterial({ color: o.color || '#F6CF3F' }), segs = [], balls = [];
    for (let i = 0; i < N; i++) { const s = new THREE.Mesh(new THREE.CylinderGeometry(R, R, 1, 7), m); g.add(s); segs.push(s); }
    for (let i = 0; i <= N; i++) { const s = new THREE.Mesh(new THREE.SphereGeometry(R, 7, 5), m); g.add(s); balls.push(s); }
    const A = new THREE.Vector3(0, 0, 0), B = new THREE.Vector3(...(o.to || [0, 0.3, 0.3])), p = new THREE.Vector3(), q = new THREE.Vector3(), d = new THREE.Vector3(), up = new THREE.Vector3(0, 1, 0);
    const [r0, r1] = o.rise || [0, 0.15], snap = o.snap ?? 1e9, suck = o.suck ?? 0.16;
    g.userData.update = t => {
      const u1 = clamp01((t - r0) / (r1 - r0)), u0 = t < snap ? 0 : clamp01((t - snap) / suck), on = t >= r0 && u0 < 0.999 && u1 > 0.01; g.visible = on; if (!on) return;
      const sag = 0.1 * (1 - u1), trem = t >= r1 && t < snap ? 0.012 * Math.sin(t * 75) : 0, whip = u0 > 0 ? 0.14 * Math.sin(u0 * 13) * (1 - u0) : 0;
      const pt = (u, out) => { out.lerpVectors(A, B, u); out.y += Math.sin(u * PI) * (trem - sag) + whip * (1 - u); out.x += whip * 0.6 * (1 - u); return out; };
      for (let i = 0; i <= N; i++) { pt(u0 + (u1 - u0) * i / N, p); balls[i].position.copy(p); }
      for (let i = 0; i < N; i++) { pt(u0 + (u1 - u0) * i / N, p); pt(u0 + (u1 - u0) * (i + 1) / N, q); d.subVectors(q, p); const L = d.length(), s = segs[i];
        s.visible = L > 1e-4; s.position.copy(p).add(q).multiplyScalar(0.5); if (L > 1e-4) s.quaternion.setFromUnitVectors(up, d.normalize()); s.scale.set(1, Math.max(L, 1e-4), 1); } };
    g.userData.update(0); return g;
  },

  // (pass 2 of 72) The driver's big inside mirror (pivot at the top of its arm, the glass toward +Z): a dark arm o.arm long (0.14) and a mirror
  // o.w x o.h (0.6 x 0.3) in a dark frame that shows nothing but sky and a cloud: turned away from the road behind
  rearMirror(o) {
    const w = o.w ?? 0.6, h = o.h ?? 0.3, arm = o.arm ?? 0.14, g = grp();
    const glass = canvasPlane(w, h, (c, W, H) => { const gr = c.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#6FB6E6'); gr.addColorStop(1, '#CFE9F5'); c.fillStyle = gr; c.fillRect(0, 0, W, H);
      c.fillStyle = '#FFFFFF'; for (const [x, y, rr] of [[0.3, 0.6, 0.2], [0.45, 0.5, 0.26], [0.62, 0.6, 0.2], [0.78, 0.66, 0.13]]) { c.beginPath(); c.arc(W * x, H * y, H * rr, 0, TAU); c.fill(); }
      c.strokeStyle = 'rgba(255,255,255,0.7)'; c.lineWidth = H * 0.05; c.beginPath(); c.moveTo(W * 0.08, H * 0.42); c.lineTo(W * 0.2, H * 0.1); c.stroke(); }, { res: 384 });
    glass.material = new THREE.MeshBasicMaterial({ map: glass.material.map, toneMapped: false });
    g.add(at(box(0.04, arm, 0.04, '#1C1E22'), 0, -arm / 2, 0), at(box(w + 0.06, h + 0.06, 0.04, '#1C1E22', { outline: 0.006 }), 0, -arm - h / 2, 0)); glass.position.set(0, -arm - h / 2, 0.022); g.add(glass);
    return g;
  },

  // (pass 2 of 72) A mountain flank with a road that zig-zags up it (pivot at the middle of its foot, the flank rising away toward -Z at o.slope
  // rad, 0.6): a painted slab o.w wide (60) and o.up long up the slope (44): alpine green going to rock and snow at the top, a grey road in
  // o.legs hairpin legs (5) that narrow with the height, a white line along it, dark pines beside the bends
  alpSlope(o) {
    const w = o.w ?? 60, up = o.up ?? 44, legs = o.legs ?? 5, g = grp();
    const pl = canvasPlane(w, up, (c, W, H) => { const gr = c.createLinearGradient(0, H, 0, 0); gr.addColorStop(0, '#8FBF6A'); gr.addColorStop(0.5, '#9DB88C'); gr.addColorStop(0.74, '#9AA39A'); gr.addColorStop(0.9, '#E9EEF2'); gr.addColorStop(1, '#FFFFFF');
      c.fillStyle = gr; c.fillRect(0, 0, W, H);
      const pts = [[W / 2, H * 0.995]]; for (let i = 1; i <= legs; i++) { const f = i / legs, y = H * (0.995 - 0.8 * f), half = W * (0.36 - 0.2 * f); pts.push([W / 2 + (i % 2 ? 1 : -1) * half, y]); }   // the first leg leaves the middle of the foot (where the real road arrives)
      for (let i = 0; i < 46; i++) { const f = hash(i + 11), x = W * hash(i + 3), y = H * (0.95 - 0.6 * f), s = H * 0.022 * (1.2 - f * 0.7); c.fillStyle = i % 2 ? '#3E6B48' : '#4E7F52'; c.beginPath(); c.moveTo(x, y - s * 2.2); c.lineTo(x - s * 0.8, y); c.lineTo(x + s * 0.8, y); c.closePath(); c.fill(); }
      c.lineCap = 'round'; c.lineJoin = 'round';
      for (const [col, k0] of [['#6C6F74', 1.25], ['#8C8C88', 1], ['#F2F0E8', 0.08]]) for (let i = 0; i < legs; i++) { const f = (i + 0.5) / legs; c.strokeStyle = col; c.lineWidth = H * 0.05 * (1 - 0.62 * f) * k0; if (k0 < 0.5) c.setLineDash([H * 0.02, H * 0.02]); else c.setLineDash([]);
        c.beginPath(); c.moveTo(pts[i][0], pts[i][1]); c.lineTo(pts[i + 1][0], pts[i + 1][1]); c.stroke(); } }, { res: 1024 });
    pl.rotation.x = -(PI / 2 - (o.slope ?? 0.6)); pl.position.set(0, Math.sin(o.slope ?? 0.6) * up / 2, -Math.cos(o.slope ?? 0.6) * up / 2); pl.castShadow = false; g.add(pl);
    return g;
  },

  // (pass 2 of 72) A worn sole coming off a shoe (pivot at the toe, the sole running back along -Z): a pale slab o.len long (0.34) that hangs
  // open and slaps shut o.rate times a second (7) between o.at [t0, t1] (hidden outside those times)
  flapSole(o) {
    const len = o.len ?? 0.34, g = grp(), fl = grp(at(box(o.w ?? 0.13, 0.025, len, '#E6DCC8', { outline: 0.004 }), 0, 0, -len / 2)); g.add(fl);   // o.w: its width (0.13)
    g.userData.update = t => { const on = !o.at || (t >= o.at[0] && t < o.at[1]); g.visible = on; if (!on) return; fl.rotation.x = -(0.15 + 0.8 * Math.abs(Math.sin(t * PI * (o.rate ?? 7)))); };
    g.userData.update(0); return g;
  },

  // (pass 2 of 72) A brand-new shoe (pivot under its heel, the toe toward +Z): a bright red trainer o.len long (0.4) with a white sole, a white
  // toe cap and a white stripe; o.color
  newShoe(o) {
    const L = o.len ?? 0.4, C = o.color || '#E0302A', g = grp();
    g.add(at(box(0.16, 0.05, L, '#FFFFFF', { outline: 0.006 }), 0, 0.025, L / 2 - 0.06), at(box(0.15, 0.11, L * 0.92, C, { outline: 0.006 }), 0, 0.105, L / 2 - 0.07), at(box(0.15, 0.08, L * 0.42, C), 0, 0.2, 0.02),
      at(box(0.152, 0.06, L * 0.2, '#FFFFFF'), 0, 0.085, L * 0.86 - 0.06), at(box(0.155, 0.03, L * 0.3, '#FFFFFF'), 0, 0.13, L * 0.42));
    return g;
  },

  // (pass 2 of 72) An Italian café front (pivot at the middle of its foot, front +Z): an ochre wall o.w x o.h (6.5 x 4.6) with green shutters, a
  // door, a red and white striped awning on two posts over the terrace and the sign o.name ('TRATTORIA')
  trattoria(o) {
    const w = o.w ?? 6.5, h = o.h ?? 4.6, g = grp();
    g.add(at(box(w, h, 0.4, o.wall || '#E9B569', { outline: 0.012 }), 0, h / 2, -0.2), at(box(w + 0.3, 0.3, 0.6, '#C8553A'), 0, h + 0.15, -0.2), at(box(1.3, 2.9, 0.1, '#6B3F26', { outline: 0.008 }), 0, 1.45, 0.03));
    for (const x of [-w * 0.32, w * 0.32]) { g.add(at(box(1.1, 1.5, 0.06, '#DCEFF2'), x, 2.2, 0.02)); for (const s of [-1, 1]) g.add(at(box(0.5, 1.6, 0.08, '#2E7D4F', { outline: 0.006 }), x + s * 0.82, 2.2, 0.05)); }
    const aw = canvasPlane(w * 0.96, 1.9, (c, W, H) => { const n = 12; for (let i = 0; i < n; i++) { c.fillStyle = i % 2 ? '#F7F3E8' : '#D23A2E'; c.fillRect(i * W / n, 0, W / n + 1, H); } c.fillStyle = 'rgba(0,0,0,0.12)'; c.fillRect(0, H * 0.86, W, H * 0.14); }, { res: 512 });
    aw.rotation.x = -PI / 2 + 0.42; aw.position.set(0, 3.25, 0.85); g.add(aw);
    for (const x of [-w * 0.46, w * 0.46]) g.add(at(box(0.06, 2.9, 0.06, '#F4F1E8', { pivot: 'bottom' }), x, 0, 1.6));
    const sg = canvasPlane(w * 0.6, 0.62, (c, W, H) => { c.fillStyle = '#2E7D4F'; c.fillRect(0, 0, W, H); c.fillStyle = '#FFF6D8'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${H * 0.72}px Arial`; c.fillText(o.name || 'TRATTORIA', W / 2, H * 0.55); }, { res: 512 });
    sg.position.set(0, 4.05, 0.02); g.add(sg);
    return g;
  },

  // (pass 3 of 72) A gendarmerie motorbike (pivot at the floor middle, front +X like `motorbike`, same size: use it at the same scale): white with a
  // blue band, a fairing with a lit headlamp and a windscreen, panniers, GENDARMERIE on both flanks, and at the back a mast with a blue beacon that
  // flashes above the rider's cap (o.mast, its top in prop units, 1.8); the engine shakes the body, the wheels turn (o.roll rad/s), o.rate flashes
  policeBike(o) {
    const g = grp(), body = grp(), wheels = [], W = '#F4F6F8', B = o.blue || '#1F4FA8', DK = '#1C1E22'; g.add(body);
    for (const x of [0.52, -0.5]) { const w = at(cyl(0.22, 0.22, 0.09, DK, 14), x, 0.22, 0, PI / 2, 0, 0); w.add(at(cyl(0.11, 0.11, 0.1, '#B8BEC6', 10), 0, 0, 0)); wheels.push(w); g.add(w); }
    body.add(at(box(0.86, 0.2, 0.2, W, { outline: 0.008 }), 0, 0.46, 0), at(box(0.865, 0.05, 0.205, B), 0, 0.42, 0));
    body.add(at(box(0.34, 0.17, 0.26, W, { outline: 0.008 }), 0.16, 0.63, 0), at(box(0.345, 0.04, 0.265, B), 0.16, 0.6, 0), at(box(0.36, 0.08, 0.24, DK), -0.18, 0.6, 0));
    body.add(at(box(0.18, 0.36, 0.38, W, { outline: 0.008 }), 0.5, 0.72, 0), at(box(0.185, 0.07, 0.385, B), 0.5, 0.64, 0));
    const hl = new THREE.Mesh(new THREE.CylinderGeometry(0.065, 0.065, 0.03, 14), new THREE.MeshBasicMaterial({ color: '#FFF4C8', toneMapped: false })); hl.rotation.z = PI / 2; hl.position.set(0.6, 0.76, 0); body.add(hl);
    const ws = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.18, 0.34), new THREE.MeshLambertMaterial({ color: '#CDEBF5', transparent: true, opacity: 0.5 })); ws.position.set(0.56, 0.96, 0); ws.rotation.z = 0.35; body.add(ws);   // low: a tall one hid the rider's face
    body.add(at(box(0.05, 0.05, 0.56, DK), 0.42, 0.88, 0), at(box(0.04, 0.3, 0.04, '#9AA0A6'), 0.44, 0.74, 0));
    for (const s of [-1, 1]) body.add(at(box(0.3, 0.22, 0.12, W, { outline: 0.006 }), -0.4, 0.5, s * 0.17), at(box(0.305, 0.05, 0.125, B), -0.4, 0.44, s * 0.17));
    for (const s of [-1, 1]) { const tx = canvasPlane(0.56, 0.1, (c, Wd, H) => { c.fillStyle = '#F4F6F8'; c.fillRect(0, 0, Wd, H); c.fillStyle = B; c.textAlign = 'center'; c.textBaseline = 'middle';
        let fs = H * 0.78; c.font = `900 ${fs}px Arial`; const tw = c.measureText('GENDARMERIE').width; if (tw > Wd * 0.94) { fs *= Wd * 0.94 / tw; c.font = `900 ${fs}px Arial`; } c.fillText('GENDARMERIE', Wd / 2, H * 0.55); }, { res: 512 });
      tx.material = new THREE.MeshBasicMaterial({ map: tx.material.map, toneMapped: false }); tx.position.set(0.08, 0.5, s * 0.104); if (s < 0) tx.rotation.y = PI; body.add(tx); }
    const top = o.mast ?? 1.8; body.add(at(box(0.025, top - 0.6, 0.025, '#9AA0A6', { pivot: 'bottom' }), -0.52, 0.6, 0), at(cyl(0.07, 0.07, 0.04, DK, 10, { pivot: 'bottom' }), -0.52, top, 0));
    const dome = new THREE.Mesh(new THREE.SphereGeometry(0.08, 12, 8, 0, TAU, 0, PI / 2), new THREE.MeshBasicMaterial({ color: '#38C8FF', toneMapped: false })); dome.position.set(-0.52, top + 0.04, 0); body.add(dome);
    const gl = glowSprite('#3FB8FF', 0.6, 0.6); gl.position.set(-0.52, top + 0.08, 0); body.add(gl);
    g.userData.update = t => { wheels.forEach(w => { w.rotation.y = (o.roll || 0) * t; }); body.position.y = (o.shake ?? 0.01) * (Math.sin(t * 92) + 0.6 * Math.sin(t * 57 + 1)); body.rotation.x = 0.012 * Math.sin(t * 41);
      const on = Math.sin(t * TAU * (o.rate ?? 2.2) + (o.phase ?? 0)); dome.material.color.set(on > 0 ? '#7FE4FF' : '#1C7CFF'); gl.material.opacity = 0.2 + 0.6 * Math.max(0, on); gl.scale.setScalar(0.45 + 0.35 * Math.max(0, on)); };
    g.userData.update(0); return g;
  },

  // (pass 3 of 72) A printed patch (pivot at its middle, front +Z): o.text in o.fg on o.bg, o.w x o.h (0.3 x 0.08), one or two lines (o.text2); it
  // glows by itself (a ministry's name on a tracksuit, read at phone size)
  textPatch(o) {
    const w = o.w ?? 0.3, h = o.h ?? 0.08, g = grp();
    const f = canvasPlane(w, h, (c, W, H) => { c.fillStyle = o.bg || '#F4F4F0'; c.fillRect(0, 0, W, H); c.fillStyle = o.fg || '#1F3E9C'; c.textAlign = 'center'; c.textBaseline = 'middle';
      const L = o.text2 ? [o.text || '', o.text2] : [o.text || '']; L.forEach((tx, i) => { let fs = H * (L.length > 1 ? 0.4 : 0.7); c.font = `900 ${fs}px Arial`; const tw = c.measureText(tx).width; if (tw > W * 0.92) { fs *= W * 0.92 / tw; c.font = `900 ${fs}px Arial`; }
        c.fillText(tx, W / 2, L.length > 1 ? H * (0.3 + 0.42 * i) : H * 0.55); }); }, { res: 512 });
    f.material = new THREE.MeshBasicMaterial({ map: f.material.map, toneMapped: false }); f.position.z = 0.004; g.add(at(box(w + 0.01, h + 0.01, 0.006, o.edge || '#1F3E9C'), 0, 0, 0), f);
    return g;
  },

  // (pass 3 of 72) One long noodle, alive (pivot at its plate end; o.to [x, y, z] its mouth end; o.r thick, 0.03): between o.rise [t0, t1] its free
  // end flies from the plate to the mouth; then it hangs in a sagging curve with a wave running along it toward the mouth, and as it is sucked it
  // straightens and thins in the middle (to o.thin of its thickness, 0.45, at o.snap); at o.snap it lets go of the plate: the tail whips and flicks
  // up and is sucked in in o.suck s (0.2), a few drops of sauce flying off the tail (o.sauce colour)
  noodleWave(o) {
    const N = 26, g = grp(), R = o.r ?? 0.03, m = new THREE.MeshLambertMaterial({ color: o.color || '#F6CF3F' }), segs = [], balls = [], drops = [];
    for (let i = 0; i < N; i++) { const s = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 1, 7), m); g.add(s); segs.push(s); }
    for (let i = 0; i <= N; i++) { const s = new THREE.Mesh(new THREE.SphereGeometry(1, 7, 5), m); g.add(s); balls.push(s); }
    for (let i = 0; i < 6; i++) { const d = sphere(R * 0.9, o.sauce || '#C7311E', 0); d.visible = false; g.add(d); drops.push(d); }
    const A = new THREE.Vector3(0, 0, 0), B = new THREE.Vector3(...(o.to || [0, 0.3, 0.3])), ax = new THREE.Vector3().subVectors(B, A), side = new THREE.Vector3().crossVectors(ax, new THREE.Vector3(0, 1, 0)).normalize();
    const p = new THREE.Vector3(), q = new THREE.Vector3(), d = new THREE.Vector3(), up = new THREE.Vector3(0, 1, 0), P = [];
    for (let i = 0; i <= N; i++) P.push(new THREE.Vector3());
    const [r0, r1] = o.rise || [0, 0.15], snap = o.snap ?? 1e9, suck = o.suck ?? 0.2, sag0 = o.sag ?? 0.16, thin = o.thin ?? 0.45;
    g.userData.update = t => {
      const u1 = clamp01((t - r0) / (r1 - r0)), u0 = t < snap ? 0 : clamp01((t - snap) / suck), on = t >= r0 && u0 < 0.999 && u1 > 0.01; g.visible = on;
      drops.forEach((dr, i) => { const v = t - snap; dr.visible = v > 0 && v < 0.45; if (!dr.visible) return; const a = i * 1.1 + 0.4; dr.position.set(Math.cos(a) * 0.5 * v + side.x * 0.3 * v, 0.9 * v - 4.9 * v * v, Math.sin(a) * 0.5 * v + side.z * 0.3 * v); });
      if (!on) return;
      const s = t < r1 ? 0 : t < snap ? clamp01((t - r1) / Math.max(0.05, snap - r1)) : 1;   // how stretched: 0 slack, 1 taut
      const sag = (t < r1 ? sag0 * (1.4 - 0.4 * u1) : sag0 * (1 - 0.85 * s)), amp = 0.05 * (1 - 0.6 * s), whip = u0 > 0 ? 0.22 * Math.sin(u0 * 12) * (1 - u0) : 0;
      for (let i = 0; i <= N; i++) { const u = u0 + (u1 - u0) * i / N; P[i].lerpVectors(A, B, u);
        P[i].y += -sag * Math.sin(PI * u) + amp * Math.sin(u * 3 * TAU - t * 22) * Math.sin(PI * u) + whip * (1 - u) * 0.8; P[i].addScaledVector(side, whip * (1 - u) * 0.6 + 0.02 * Math.sin(t * 9 + u * 6) * (1 - s)); }
      for (let i = 0; i <= N; i++) { const u = i / N, rr = R * (1 - (1 - thin) * s * Math.sin(PI * u)); balls[i].position.copy(P[i]); balls[i].scale.setScalar(rr); }
      for (let i = 0; i < N; i++) { p.copy(P[i]); q.copy(P[i + 1]); d.subVectors(q, p); const L = d.length(), sg = segs[i], u = (i + 0.5) / N, rr = R * (1 - (1 - thin) * s * Math.sin(PI * u));
        sg.visible = L > 1e-4; sg.position.copy(p).add(q).multiplyScalar(0.5); if (L > 1e-4) sg.quaternion.setFromUnitVectors(up, d.normalize()); sg.scale.set(rr, Math.max(L, 1e-4), rr); } };
    g.userData.update(0); return g;
  },

  // (pass 3 of 72) A big plate of spaghetti in red sauce (pivot at the plate's middle): a white plate o.r round (0.2), a heaped mound of yellow noodle
  // loops, a red sauce cap with two meatballs and a basil leaf
  spaghettiPlate(o) {
    const Rp = o.r ?? 0.2, g = grp(), nm = new THREE.MeshLambertMaterial({ color: '#F2D27A' });
    g.add(at(cyl(Rp, Rp * 0.8, 0.03, '#F7F5EF', 24, { outline: 0.005 }), 0, 0, 0));
    for (let i = 0; i < 26; i++) { const lay = i / 26, a = i * 2.399, rr = Rp * 0.62 * (1 - 0.7 * lay), t = new THREE.Mesh(new THREE.TorusGeometry(Rp * (0.2 + 0.08 * hash(i)), 0.011, 5, 16), nm);
      t.position.set(Math.cos(a) * rr * 0.6, 0.03 + Rp * 0.55 * lay, Math.sin(a) * rr * 0.6); t.rotation.set(PI / 2 + 0.5 * (hash(i + 4) - 0.5), 0.6 * (hash(i + 2) - 0.5), a); g.add(t); }
    const sc = sphere(Rp * 0.42, '#C7311E', 1); sc.scale.y = 0.38; sc.position.set(0, 0.03 + Rp * 0.56, 0); g.add(sc);
    for (const [x, z] of [[-0.05, 0.02], [0.05, -0.02]]) g.add(at(sphere(Rp * 0.15, '#7A3020', 1), x * Rp / 0.14, 0.05 + Rp * 0.6, z * Rp / 0.14));
    g.add(at(box(Rp * 0.22, 0.01, Rp * 0.12, '#2E8B3E'), 0.0, 0.07 + Rp * 0.62, 0.0, 0, 0.6, 0));
    return g;
  },

  // (pass 3 of 72) A splat of tomato sauce (pivot at its middle, front +Z: put it on a face and turn it to the camera): hidden until o.at, then a red
  // splat pops onto it (overshoot) while six drops fly out from it and fall; o.s its size (0.22)
  sauceSplat(o) {
    const S = o.s ?? 0.22, g = grp(), at0 = o.at ?? 0, drops = [];
    const sp = canvasPlane(S, S, (c, W, H) => { c.clearRect(0, 0, W, H); c.fillStyle = o.color || '#C7311E';
      for (let i = 0; i < 9; i++) { const a = i * 0.7, rr = (i ? 0.13 + 0.1 * hash(i) : 0.3) * W, d = i ? (0.18 + 0.14 * hash(i + 3)) * W : 0; c.beginPath(); c.arc(W / 2 + Math.cos(a) * d, H / 2 + Math.sin(a) * d, rr * 0.55, 0, TAU); c.fill(); } }, { res: 256, transparent: true });
    sp.material = new THREE.MeshBasicMaterial({ map: sp.material.map, transparent: true, depthWrite: false, toneMapped: false }); g.add(sp);
    for (let i = 0; i < 6; i++) { const d = sphere(S * 0.07, o.color || '#C7311E', 0); g.add(d); drops.push(d); }
    g.userData.update = t => { const u = t - at0; g.visible = u >= 0; if (u < 0) return; const k = u < 0.06 ? u / 0.06 * 1.25 : u < 0.14 ? 1.25 - 0.25 * (u - 0.06) / 0.08 : 1; sp.scale.set(k, k, 1);
      drops.forEach((d, i) => { const a = i * 1.05 + 0.3; d.visible = u < 0.5; d.position.set(Math.cos(a) * 1.4 * u, Math.sin(a) * 1.1 * u - 3.5 * u * u, 0.05 + 0.3 * u); }); };
    g.userData.update(-1); return g;
  },

  // (pass 3 of 72) The lump of a swallowed noodle running down under his jersey (pivot at the joint it is put on, his torso: it runs from o.from to
  // o.to, local, between o.at and o.at + o.dur, 0.35 s): a bump in the jersey's yellow (o.color), o.r round (0.07), with an ink outline
  throatLump(o) {
    const g = grp(), b = sphere(o.r ?? 0.07, o.color || '#F7D23A', 1, { outline: 0.006 }), A = new THREE.Vector3(...(o.from || [0, 0.62, 0.16])), Bv = new THREE.Vector3(...(o.to || [0, 0.18, 0.17]));
    b.scale.z = 0.7; g.add(b);
    g.userData.update = t => { const u = (t - (o.at ?? 0)) / (o.dur ?? 0.35); b.visible = u >= 0 && u <= 1; if (!b.visible) return; b.position.lerpVectors(A, Bv, u * u * (3 - 2 * u)); const k = Math.sin(PI * u) * 0.5 + 0.6; b.scale.set(k, k, 0.7 * k); };
    g.userData.update(-1); return g;
  },

  // (pass 3 of 72) One shoe with a real profile (pivot under its middle, toe toward +X): o.kind 'sneaker' (white sole, laces, a side stripe), 'boot'
  // (tall shaft, dark sole), 'brogue' (heel block, rounded toe cap); o.color the upper, o.len (0.32); o.worn: the sole gapes open at the toe and a
  // hole shows on the side
  bigShoe(o) { return shoeMesh(o.kind || 'sneaker', o.color || '#C0392B', o.len ?? 0.32, !!o.worn, o.seed ?? 1); },

  // (pass 3 of 72) A mountain of worn-out shoes (pivot at the floor middle): o.n shoes (110) of three kinds in bright and dark colours laid over the
  // surface of a cone o.r round (2) and o.h high (3.3), on a dark core; o.tumble (5) of them keep sliding and turning down the slope, one after another
  shoeHeap(o) {
    const n = o.n ?? 110, R = o.r ?? 2, H = o.h ?? 3.3, g = grp(), kinds = ['sneaker', 'boot', 'brogue'], cols = ['#C0392B', '#2E86C1', '#F4F1E8', '#7A4E2C', '#24211F', '#E67E22', '#27AE60', '#8E44AD', '#F1C40F', '#5A3A24'];
    g.add(cyl(R * 0.04, R * 0.97, H * 0.97, o.core || '#5C4A3E', 14, { pivot: 'bottom' }));
    for (let i = 0; i < n; i++) { const f = Math.sqrt(hash(i + 1)) * 0.96, y = H * (1 - f), rr = R * f, a = i * 2.399 + hash(i + 7);
      const sh = shoeMesh(kinds[i % 3], cols[(i * 7) % cols.length], 0.32 * (0.9 + 0.5 * hash(i + 3)), hash(i + 5) > 0.5, i);
      sh.position.set(Math.cos(a) * rr, y, Math.sin(a) * rr); const sl = Math.atan2(H, R); sh.rotation.set(0, -a + (hash(i + 9) - 0.5) * 2.5, 0); sh.rotateOnWorldAxis(new THREE.Vector3(-Math.sin(a), 0, Math.cos(a)), -sl * 0.9 + (hash(i + 11) - 0.5) * 0.8); g.add(sh); }
    const tum = []; for (let j = 0; j < (o.tumble ?? 5); j++) { const sh = shoeMesh(kinds[j % 3], cols[(j * 3 + 1) % cols.length], 0.4, true, 90 + j); g.add(sh); tum.push(sh); }
    g.userData.update = t => tum.forEach((sh, j) => { const u = ((t * 0.55 + j / tum.length) % 1), a = 0.9 + j * 1.3, rr = R * (0.08 + 0.95 * u); sh.position.set(Math.cos(a) * rr, H * (1 - 0.95 * u) * 0.98 + 0.12, Math.sin(a) * rr); sh.rotation.set(t * 5 + j, a, t * 3.3 + j * 2); });
    g.userData.update(0); return g;
  },

  // (pass 3 of 72) A clipboard (pivot at its middle, front +Z): a brown board o.w x o.h (0.22 x 0.3), a white sheet with lines and a tick list, a
  // steel clip at the top
  clipBoard(o) {
    const w = o.w ?? 0.22, h = o.h ?? 0.3, g = grp(at(box(w, h, 0.012, '#9A6B3E', { outline: 0.006 }), 0, 0, 0), at(box(w * 0.4, 0.04, 0.02, '#B8BEC6'), 0, h / 2 - 0.02, 0.01));
    const sh = canvasPlane(w * 0.88, h * 0.8, (c, W, H) => { c.fillStyle = '#FBFAF4'; c.fillRect(0, 0, W, H); c.strokeStyle = '#7C8FB0'; c.lineWidth = H * 0.012; for (let i = 1; i < 9; i++) { c.beginPath(); c.moveTo(W * 0.1, H * i / 9.5); c.lineTo(W * 0.9, H * i / 9.5); c.stroke(); }
      c.strokeStyle = '#C7311E'; c.lineWidth = H * 0.02; c.beginPath(); c.moveTo(W * 0.15, H * 0.3); c.lineTo(W * 0.85, H * 0.15); c.lineTo(W * 0.8, H * 0.7); c.stroke(); }, { res: 256 });
    sh.position.set(0, -h * 0.06, 0.008); g.add(sh); return g;
  },

  // (pass 3 of 72) A long beard that streams forward when he brakes (pivot at the chin; `beardHair` of story 66 inside, same options): it hangs; from
  // o.stream[0] to [1] it swings forward and up past his face to o.angle (2.0 rad), then from [1] to [2] it drops back onto his chest like a weight
  // and bounces off it twice
  streamBeard(o) {
    const g = grp(), piv = grp(), b = FEU_PROPS.beardHair({ ...o, swing: o.whip ? o.whip : null, whip: !!o.whip }); g.add(piv); piv.add(b);
    const [t0, t1, t2] = o.stream || [1e9, 1e9, 1e9], A = o.angle ?? 2.0;
    g.userData.update = t => { b.userData.update?.(t); let a = 0;
      if (t >= t0 && t < t1) { const u = (t - t0) / (t1 - t0); a = -A * u * u * (3 - 2 * u); }
      else if (t >= t1) { const u = t - t1, d = t2 - t1; a = u < d ? -A * (1 - (u / d) ** 2) : -0.35 * Math.exp(-7 * (u - d)) * Math.abs(Math.sin((u - d) * 12)); }
      piv.rotation.x = a; };
    g.userData.update(0); return g;
  },

  // (pass 3 of 72) An Italian cypress (pivot at its foot): a dark green spindle o.h tall (6) on a short trunk; o.color
  cypress(o) {
    const H = o.h ?? 6, g = grp(at(cyl(0.12, 0.16, H * 0.12, '#5B4030', 6, { pivot: 'bottom' }), 0, 0, 0)), c = o.color || '#2F5A34';
    const sp = sphere(1, c, 1); sp.scale.set(H * 0.11, H * 0.46, H * 0.11); sp.position.y = H * 0.52; g.add(sp);
    const s2 = sphere(1, o.color2 || '#3B6B3E', 1); s2.scale.set(H * 0.08, H * 0.3, H * 0.08); s2.position.set(H * 0.03, H * 0.66, H * 0.02); g.add(s2);
    return g;
  },

  // (pass 3 of 72) An umbrella pine (pivot at its foot): a tall bare trunk o.h (5.5) leaning a little, a flat wide dark green canopy on top
  umbrellaPine(o) {
    const H = o.h ?? 5.5, g = grp(at(cyl(0.14, 0.2, H * 0.82, '#6B4A34', 6, { pivot: 'bottom' }), 0, 0, 0, 0, 0, 0.06)), c = o.color || '#3E6B3A';
    for (const [x, z, r] of [[0, 0, 1], [0.9, 0.3, 0.7], [-0.8, -0.2, 0.75], [0.2, -0.8, 0.6]]) { const s = sphere(1, c, 1); s.scale.set(H * 0.26 * r, H * 0.08 * r, H * 0.26 * r); s.position.set(x * H * 0.12 + H * 0.05, H * 0.86, z * H * 0.12); g.add(s); }
    return g;
  },

  // (pass 3 of 72) A Roman street front (pivot at the middle of its foot, front +Z) to stand in front of a set's houses: an ochre or terracotta wall
  // o.w x o.h (13 x 21) with four floors of windows between green shutters, a balcony, a cornice, a terracotta roof edge and, on the ground floor,
  // arched doorways and a shop under a striped awning; o.color, o.seed
  romeFront(o) {
    const w = o.w ?? 13, h = o.h ?? 21, g = grp(), col = o.color || '#D9A15B', sd = o.seed ?? 1;
    const f = canvasPlane(w, h, (c, W, H) => { c.fillStyle = col; c.fillRect(0, 0, W, H); const px = W / w;
      c.fillStyle = 'rgba(0,0,0,0.06)'; for (let i = 0; i < 40; i++) c.fillRect(W * hash(i + sd), H * hash(i + 3 * sd), W * 0.08, H * 0.03);
      const cols = 5, fl = 4, gh = H * 0.2;
      for (let r = 0; r < fl; r++) for (let k = 0; k < cols; k++) { const x = W * (k + 0.5) / cols, y = gh + (H - gh) * (fl - r - 0.62) / (fl + 0.4), ww = px * 1.0, hh = px * 1.7;
        c.fillStyle = '#3A2A22'; c.fillRect(x - ww / 2, y - hh / 2, ww, hh); c.fillStyle = '#F2E6CC'; c.fillRect(x - ww / 2 - px * 0.12, y + hh / 2, ww + px * 0.24, px * 0.14);
        const open = hash(r * 7 + k + sd) > 0.35; c.fillStyle = '#3E6B48'; if (open) { c.fillRect(x - ww / 2 - px * 0.55, y - hh / 2, px * 0.5, hh); c.fillRect(x + ww / 2 + px * 0.05, y - hh / 2, px * 0.5, hh); } else c.fillRect(x - ww / 2, y - hh / 2, ww, hh);
        if (r === 1 && k % 2 === 0) { c.fillStyle = '#2A2422'; c.fillRect(x - ww * 0.8, y + hh / 2, ww * 1.6, px * 0.1); for (let b = 0; b < 6; b++) c.fillRect(x - ww * 0.8 + b * ww * 0.32, y + hh / 2, px * 0.04, px * 0.5); } }
      c.fillStyle = '#F2E6CC'; c.fillRect(0, gh - px * 0.25, W, px * 0.3); c.fillRect(0, H * 0.02, W, px * 0.45);
      for (let k = 0; k < cols; k++) { const x = W * (k + 0.5) / cols; if (k === 2) { c.fillStyle = '#2B2622'; c.fillRect(x - px * 1.4, gh * 0.08, px * 2.8, gh * 0.82); const s = 8; for (let i = 0; i < s; i++) { c.fillStyle = i % 2 ? '#F4EFE2' : (o.awning || '#2E7D4F'); c.fillRect(x - px * 1.7 + i * px * 3.4 / s, gh * 0.02, px * 3.4 / s, gh * 0.22); } continue; }
        c.fillStyle = '#4A3328'; c.beginPath(); c.moveTo(x - px * 0.7, gh * 0.95); c.lineTo(x - px * 0.7, gh * 0.4); c.arc(x, gh * 0.4, px * 0.7, PI, 0, false); c.lineTo(x + px * 0.7, gh * 0.95); c.fill(); } }, { res: o.res ?? 512 });   // (pass 3) 512: eighteen of these fronts at 1024 took the render to its memory limit (a stills run crashed on the last shot)
    f.rotation.x = PI; f.rotation.z = PI; f.position.y = h / 2; g.add(f);
    g.add(at(box(w + 0.4, 0.5, 1.2, o.roof || '#B5522F', { outline: 0.01 }), 0, h + 0.25, -0.4), at(box(w + 0.2, 0.3, 0.6, '#E9DCC0'), 0, h - 0.15, 0.1));
    return g;
  },

  // (pass 3 of 72) A Roman dome on the skyline (pivot at its foot): a drum, a ribbed grey-blue dome and a lantern, o.h high (60); no light of its own
  romeDome(o) {
    const H = o.h ?? 60, g = grp(), c = o.color || '#E3D6BC';
    g.add(at(box(H * 0.9, H * 0.3, H * 0.5, c, { pivot: 'bottom' }), 0, 0, 0), at(cyl(H * 0.26, H * 0.26, H * 0.18, c, 20, { pivot: 'bottom' }), 0, H * 0.3, 0));
    const d = new THREE.Mesh(new THREE.SphereGeometry(H * 0.25, 20, 10, 0, TAU, 0, PI / 2), new THREE.MeshLambertMaterial({ color: o.dome || '#9FB0B8' })); d.position.y = H * 0.48; d.scale.y = 1.25; g.add(d);
    g.add(at(cyl(H * 0.05, H * 0.05, H * 0.1, c, 10, { pivot: 'bottom' }), 0, H * 0.79, 0), at(sphere(H * 0.025, '#C9A23E', 1), 0, H * 0.91, 0));
    return g;
  },

  // (pass 3 of 72) The inside of a bus seen through its glass flank (pivot at the bus's own pivot: put it on the bus, `on={'actor': bus}`): window
  // pillars along both flanks, red seat backs in rows and passengers' heads (round, varied hair) at the windows; o.len (7.6), o.top (3.0)
  busCrowd(o) {
    const L = o.len ?? 7.6, top = o.top ?? 3.0, g = grp(), hz = 1.15, skins = ['#E8B48A', '#C68A5E', '#8D5A3B', '#F1C9A5'], hairs = ['#2B211C', '#6B4A2E', '#D9C27A', '#1C1C1C', '#B5B5B5'];
    for (const s of [-1, 1]) for (let i = 0; i <= 6; i++) g.add(at(box(0.07, top - 1.2, 0.05, '#22252B'), -L / 2 + 0.5 + i * (L - 1.0) / 6, 1.2 + (top - 1.2) / 2, s * (hz + 0.02)));
    for (let i = 0; i < 6; i++) { const x = -L / 2 + 0.9 + i * (L - 1.6) / 5; for (const s of [-1, 1]) { g.add(at(box(0.12, 0.7, 0.42, '#B5302A', { outline: 0.004 }), x, 1.15, s * 0.6));
        if (hash(i * 2 + (s > 0 ? 1 : 0) + 3) > 0.25) { const hd = sphere(0.17, skins[(i + (s > 0 ? 2 : 0)) % 4], 1); hd.scale.y = 1.15; hd.position.set(x + 0.18, 1.72, s * 0.6); g.add(hd);
          const hr = sphere(0.18, hairs[(i * 3 + (s > 0 ? 1 : 0)) % 5], 1); hr.scale.set(1, 0.6, 1); hr.position.set(x + 0.14, 1.86, s * 0.6); g.add(hr); } } }
    return g;
  },
};
