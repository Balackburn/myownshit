// « Le cheveu » (story 88): this man found a hair in his soup; a police helicopter lit the soup; the hair was arrested with tweezers,
// photographed from the front then in profile, questioned twelve hours under the lamp; it curled, which was held against it; the dogs followed
// its trail to the cook; they broke down his door, and every door in the street; the cook was bald, he was shaved anyway, then the customers and
// the passers-by for comparison, the police dog too, this man twice; under the microscope no match; the minister apologised to the hair; it was
// the last hair in the neighbourhood; the helicopter put it back, in this man's soup.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere, mat } from './style.js';
import { grp, at, canvasPlane, rod, buildProp } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = x => { const u = clamp01(x), c = 1.70158; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const noShadow = m => { m.traverse(c => { c.castShadow = false; }); return m; };
// a value keyed in time: keys [[t, v], ...] (sorted); eased between keys over `blend` seconds after each key (0: a step)
function keyAt(keys, t, def = 0, blend = 0.2) {
  if (!keys || !keys.length) return def;
  let v = def, prev = def, t0 = -1e9;
  for (const [kt, kv] of keys) { if (t >= kt) { prev = v; v = kv; t0 = kt; } else break; }
  if (blend <= 0) return v;
  return prev + (v - prev) * smooth((t - t0) / blend);
}
const inWin = (wins, t) => (wins || []).some(([a, b]) => t >= a && t < b);
// a keyed [sx, sy, sz] (keys [[t, [sx, sy, sz]], ...]), eased over `blend` s after each key, [1, 1, 1] before the first
function sqAt(keys, t, blend = 0.06) { const r = [1, 1, 1]; for (let i = 0; i < 3; i++) r[i] = keyAt((keys || []).map(([kt, v]) => [kt, v[i]]), t, 1, blend); return r; }
const HAIR = '#121214';
// a soft round sprite texture (white centre fading out), shared
let _soft = null;
function softTex() {
  if (_soft) return _soft;
  const c = document.createElement('canvas'); c.width = c.height = 64; const x = c.getContext('2d'), gr = x.createRadialGradient(32, 32, 0, 32, 32, 32);
  gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.5, 'rgba(255,255,255,0.45)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  x.fillStyle = gr; x.fillRect(0, 0, 64, 64); _soft = new THREE.CanvasTexture(c); return _soft;
}
const softMat = (color, opacity = 1, add = false) => new THREE.MeshBasicMaterial({ color, map: softTex(), transparent: true, opacity, depthWrite: false, side: THREE.DoubleSide, blending: add ? THREE.AdditiveBlending : THREE.NormalBlending });
// (round 1) LIGHT THAT SITS BEHIND PEOPLE. A beam drawn as a see-through cone over a man greys his navy suit (review 1: the searchlight
// ghosted him). Here a beam is an additive mesh in the OPAQUE pass (transparent false, no depth write) at renderOrder 0.5: the set and the
// props (0) are drawn first, the beam adds its light over them, and the actors, bumped to renderOrder 1 by onTopActors(), are drawn last and
// cover it: the light passes behind every person, never over a face. A thing that must stay crisp inside a beam takes renderOrder 1 as well.
const BEAM_ORDER = 0.5;
function onTopActors(self) {
  // every frame: everything in the shot but the set, the beams and what is flagged userData.chvUnder (the room, the helicopter) is drawn after
  // the beams (the cloth and the attached props of an actor are built or re-parented after the first frame)
  let root = self; while (root && root.parent && !root.parent.isScene) root = root.parent; if (!root || !root.children) return;
  root.children.forEach((c, i) => { if (i === 0 || c.userData.chvUnder || c.userData.chvBeam) return;
    c.traverse(n => { if (n.isMesh && n.renderOrder === 0 && !(n.material && n.material.transparent) && n.material?.blending !== THREE.AdditiveBlending) n.renderOrder = 1; }); });
}
const onTop = (g, ord = 1) => { g.traverse(n => { if (n.isMesh && n.renderOrder <= 0) n.renderOrder = ord; }); return g; };
function beamMat(color, opacity) {
  return new THREE.MeshBasicMaterial({ color, transparent: false, opacity, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, vertexColors: true, toneMapped: true });
}
// an open cone along -Y from r0 (at y 0) to r1 (at y -len), brighter at the top (fade: what is left at the far end) and soft at its rim (rings)
function beamCone(len, r0, r1, color, opacity, fade = 0.55, seg = 28) {
  const g = new THREE.CylinderGeometry(r0, r1, len, seg, 6, true); g.translate(0, -len / 2, 0);
  const pos = g.attributes.position, cols = [];
  for (let i = 0; i < pos.count; i++) { const u = clamp01(-pos.getY(i) / len), k = 1 - (1 - fade) * u; cols.push(k, k, k); }
  g.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3));
  const m = new THREE.Mesh(g, beamMat(color, opacity)); m.renderOrder = BEAM_ORDER; m.castShadow = false; m.receiveShadow = false; m.userData.noAO = true; return m;
}
// a tube through points, rebuilt in place (a strand of hair)
function setTube(m, pts, r, seg = 40) {
  const old = m.geometry; m.geometry = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), seg, r, 6, false); old.dispose();
}
// a little pair of cartoon eyes (front +Z): whites, pupils, optional brows; returns {g, set(gx, gy, lid, brow)}
function eyePair(s = 1, brows = false) {
  const g = grp(), W = new THREE.MeshBasicMaterial({ color: '#FFFFFF' }), K = new THREE.MeshBasicMaterial({ color: '#0C0C0E' }), parts = [];
  for (const sx of [-1, 1]) {
    const e = grp(); e.position.x = sx * 0.019 * s; g.add(e);
    const wh = new THREE.Mesh(new THREE.SphereGeometry(0.0175 * s, 12, 8), W); wh.scale.z = 0.6; e.add(wh);
    const ring = new THREE.Mesh(new THREE.SphereGeometry(0.0195 * s, 12, 8), K); ring.scale.z = 0.55; ring.position.z = -0.002 * s; e.add(ring);
    const pu = new THREE.Mesh(new THREE.SphereGeometry(0.0085 * s, 10, 6), K); pu.scale.z = 0.5; pu.position.z = 0.0095 * s; e.add(pu);
    let br = null; if (brows) { br = at(box(0.026 * s, 0.006 * s, 0.006 * s, '#0C0C0E'), 0, 0.027 * s, 0.006 * s); e.add(br); }
    parts.push({ e, wh, pu, br, sx });
  }
  const set = (gx = 0, gy = 0, lid = 0, brow = 0) => parts.forEach(({ e, pu, br, sx }) => {
    e.scale.y = Math.max(0.12, 1 - lid); pu.position.x = gx * 0.007 * s; pu.position.y = -gy * 0.007 * s;
    if (br) { br.rotation.z = -sx * brow * 0.5; br.position.y = (0.027 + 0.004 * Math.abs(brow)) * s; }
  });
  set(); return { g, set };
}

export const CHEVEU_PROPS = {
  // THE HAIR (the star): one black strand o.L long (0.3) and o.r thick (0.009), pivot at its root. Two states keyed and blended:
  // o.stand [[t, v]]: 0 floating (lying along X on y 0, waving like a hair on soup), 1 upright (rising along +Y with a small S);
  // o.curl [[t, v]]: 0 straight, 1 a tight coil (the curl runs down from its top); o.wig: the wave's amplitude (fraction of L, 0.06),
  // o.waveF its speed; o.yaw [[t, deg]]: the whole hair turns (the profile mugshot); o.eyes: a pair of cartoon eyes at its top (o.eyeS, o.brows,
  // o.gaze [[t, gx, gy]], o.blinks [t, ...], o.brow [[t, v]]: -1 worried .. 1 cross), o.eyesOn [[t, 0|1]]; o.board: a small black number
  // board hung on its front with white lines (o.board ['N° 0088', ...], o.boardY, o.boardYaw [[t, deg]]); o.rim: a pale halo colour round the
  // strand (dark backgrounds); o.sweat [t, ...]: a drop that runs down beside the eyes; o.hop [[t, h]]: a little jump (it straightens up);
  // (round 1) o.onTop: drawn after the beams (crisp inside a searchlight); o.rimW: the halo's width (1.7 times the strand)
  // (round 2) o.hang: the pivot is the top of the hair, which hangs below it (on a winch cable); o.cable [x, y, z]: a world point the hang point
  // is tied to by a bright unlit cable with a dark hull (o.cableR 0.009, o.cableC, o.cableRim); o.pend [[t, rad], ...]: a pendulum swing about the
  // pivot, dying out (o.pendF rad/s, o.pendK decay); o.eyeU: where the eyes sit along the strand (1: its top); o.boing t: the curl's spring, a
  // wind-up stretch over 0.22 s before t, the coil swinging on an arc, then two or three overshoot bounces; o.flick [t, ...]: four big sweat drops
  // fly off the top in arcs; o.sweatS: the size of the running drop
  // (final pass) o.eyesFace: the eyes stay turned to the front when the hair turns (o.yaw: the profile mugshot keeps its face); o.sway [amp rad,
  // rad/s]: a slow sway of the whole strand
  chvHair(o) {
    const L = o.L ?? 0.3, R = o.r ?? 0.009, g = grp(), sw = grp(), body = grp(); g.add(sw); sw.add(body);
    const hm = new THREE.MeshLambertMaterial({ color: o.color || HAIR, emissive: '#000000' });
    const tube = new THREE.Mesh(new THREE.BufferGeometry(), hm); tube.castShadow = true; body.add(tube);
    const capA = new THREE.Mesh(new THREE.SphereGeometry(R, 8, 6), hm), capB = new THREE.Mesh(new THREE.SphereGeometry(R * 1.15, 8, 6), hm); body.add(capA, capB);
    let rimM = null;
    if (o.rim) { rimM = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshBasicMaterial({ color: o.rim, side: THREE.BackSide })); body.add(rimM); }
    const gl = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshBasicMaterial({ color: '#5A5E6A' })); body.add(gl);   // a thin glint line along it
    const ey = o.eyes ? eyePair(o.eyeS ?? 1, !!o.brows) : null; if (ey) body.add(ey.g);
    let board = null;
    if (o.board) {
      const lines = Array.isArray(o.board) ? o.board : [String(o.board)], bw = o.boardW ?? 0.12, bh = o.boardH ?? 0.075;
      board = grp(); const pl = canvasPlane(bw, bh, (c, W, H) => { c.fillStyle = '#16171B'; c.fillRect(0, 0, W, H); c.strokeStyle = '#E8E8E2'; c.lineWidth = W * 0.02; c.strokeRect(W * 0.04, H * 0.06, W * 0.92, H * 0.88);
        c.fillStyle = '#F4F4EE'; c.textAlign = 'center'; c.textBaseline = 'middle'; const n = lines.length;
        lines.forEach((s, i) => { c.font = `900 ${H * (n > 1 ? 0.34 : 0.5)}px Arial`; c.fillText(s, W / 2, H * ((i + 0.5) / n * 0.86 + 0.07)); }); }, { res: 256 });
      board.add(pl, at(box(bw + 0.006, bh + 0.006, 0.004, '#0A0A0C'), 0, 0, -0.003));
      board.add(rod([-bw * 0.4, bh / 2, 0], [0, bh / 2 + 0.035, -0.004], 0.0015, '#D8D8D0'), rod([bw * 0.4, bh / 2, 0], [0, bh / 2 + 0.035, -0.004], 0.0015, '#D8D8D0'));
      body.add(board);
    }
    let drop = null; if (o.sweat) { drop = new THREE.Mesh(new THREE.SphereGeometry(0.008 * (o.sweatS ?? 1), 8, 6), new THREE.MeshBasicMaterial({ color: '#9FD6F2' })); drop.scale.set(0.8, 1.3, 0.6); body.add(drop); }
    let cab = null, cabR = null;
    if (o.cable) { cab = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshBasicMaterial({ color: o.cableC || '#F4F6FA' })); cabR = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshBasicMaterial({ color: o.cableRim || '#0E1428', side: THREE.BackSide })); cab.frustumCulled = cabR.frustumCulled = false; g.add(cab, cabR); }
    const flk = []; for (const t0 of o.flick || []) for (let i = 0; i < 4; i++) { const dm = grp(new THREE.Mesh(new THREE.SphereGeometry(0.016, 10, 8), new THREE.MeshBasicMaterial({ color: '#8ED2F4' })), new THREE.Mesh(new THREE.SphereGeometry(0.021, 10, 8), new THREE.MeshBasicMaterial({ color: '#16324A', side: THREE.BackSide })));
      dm.children.forEach(c => c.scale.set(0.8, 1.25, 0.8)); dm.visible = false; body.add(dm); flk.push([dm, t0, (i % 2 ? 1 : -1) * (0.45 + 0.25 * hsh(i + t0 * 7)), 0.55 + 0.3 * hsh(i * 3 + 1)]); }
    const _v = new THREE.Vector3(), _o = new THREE.Vector3();
    const N = 44, pts = Array.from({ length: N }, () => new THREE.Vector3()), A = o.wig ?? 0.06, wf = o.waveF ?? 2.2;
    const P0 = new THREE.Vector3(), P1 = new THREE.Vector3(), P2 = new THREE.Vector3();
    g.userData.update = t => {
      const s = keyAt(o.stand, t, o.stand0 ?? 0, 0.25), c = keyAt(o.curl, t, 0, o.curlDur ?? 0.35), ph = t * wf, hop = keyAt(o.hop, t, 0, 0.12);
      const turns = o.turns ?? 4.5, Rc = o.curlR ?? L * 0.1, Hc = L * 0.42;
      for (let i = 0; i < N; i++) {
        const u = i / (N - 1);
        P0.set((u - 0.5) * L, 0.004 * Math.sin(TAU * 2 * u + ph), A * L * 1.3 * Math.sin(TAU * 1.3 * u + ph));
        const w2 = A * (1 - 0.6 * hop);
        P1.set(w2 * L * Math.sin(TAU * 0.9 * u + ph) * Math.min(1, u * 3) + (o.lean ?? 0) * u * L, u * L, 0.25 * w2 * L * Math.sin(TAU * 0.6 * u + ph * 0.7));
        const th = u * turns * TAU; P2.set(Rc * Math.sin(th), u * Hc + 0.004, Rc * Math.cos(th) - Rc);
        const wi = smooth((c - (1 - u) * 0.35) / 0.65);
        pts[i].copy(P0).lerp(P1, s).lerp(P2, wi);
      }
      let sy = 1, arc = 0;
      if (o.boing != null) { const u = t - o.boing;
        if (u < 0) sy = 1 + 0.38 * smooth((u + 0.22) / 0.22);
        else { sy = 1 + 0.38 * Math.exp(-4.2 * u) * Math.cos(TAU * 3.1 * u); arc = 0.5 * Math.sin(PI * Math.min(1, u / 0.36)) * Math.exp(-2 * u); } }
      body.scale.set(1 / Math.sqrt(sy), sy, 1 / Math.sqrt(sy)); body.rotation.z = arc;
      body.position.y = hop * 0.12 - (o.hang ? L : 0);
      let pa = 0; for (const [t0, a] of o.pend || []) { const u = t - t0; if (u >= 0) pa += a * Math.exp(-(o.pendK ?? 2.4) * u) * Math.sin((o.pendF ?? 7) * u); }
      sw.rotation.z = pa;
      if (cab) { g.updateWorldMatrix(true, false); _v.set(...o.cable); g.worldToLocal(_v); _o.set(0, 0, 0); const cr = o.cableR ?? 0.009;
        const oc = cab.geometry, orr = cabR.geometry; cab.geometry = new THREE.TubeGeometry(new THREE.LineCurve3(_o.clone(), _v.clone()), 1, cr, 8, false); cabR.geometry = new THREE.TubeGeometry(new THREE.LineCurve3(_o.clone(), _v.clone()), 1, cr * 1.9, 8, false); oc.dispose(); orr.dispose(); }
      for (const [dm, t0, vx, vy] of flk) { const u = t - t0; dm.visible = u >= 0 && u < 0.55; if (!dm.visible) continue; const tp = pts[N - 1]; dm.position.set(tp.x + vx * u, tp.y + vy * u - 2.2 * u * u, tp.z + 0.02); dm.scale.setScalar(Math.max(0.01, 1 - 0.5 * u)); }
      setTube(tube, pts, R, 60); capA.position.copy(pts[0]); capB.position.copy(pts[N - 1]);
      if (rimM) setTube(rimM, pts, R * (o.rimW ?? 1.7), 60);
      const gp = pts.map(p => p.clone().add(new THREE.Vector3(-R * 0.35, R * 0.45, R * 0.55))); setTube(gl, gp, R * 0.22, 60);
      body.rotation.y = keyAt(o.yaw, t, 0, o.yawDur ?? 0.15) * PI / 180;
      if (o.sway) body.rotation.z += o.sway[0] * Math.sin(t * (o.sway[1] ?? 3));
      const top = pts[Math.round((o.eyeU ?? 1) * (N - 1))];
      if (ey) {
        const on = keyAt(o.eyesOn, t, 1, 0.08) * (o.eyesFloat ? 1 : smooth((s - 0.5) / 0.4));
        ey.g.visible = on > 0.02; ey.g.scale.setScalar(Math.max(0.01, on));
        ey.g.position.set(top.x, top.y + 0.004, top.z + R * 1.2);
        const gz = (o.gaze || []).filter(k => t >= k[0]).pop() || [0, 0, 0];
        let lid = 0; for (const b of o.blinks || []) { const u = t - b; if (u >= 0 && u < 0.12) lid = Math.max(lid, 1 - Math.abs(u - 0.06) / 0.06); }
        ey.set(gz[1], gz[2], lid, keyAt(o.brow, t, 0, 0.1));
        ey.g.rotation.y = o.eyesFace ? -body.rotation.y : 0;
      }
      if (board) {
        const k = Math.round((o.boardU ?? 0.55) * (N - 1)), p = pts[k];
        board.position.set(p.x, p.y - 0.075, p.z + R + 0.004); board.rotation.y = keyAt(o.boardYaw, t, 0, o.yawDur ?? 0.15) * PI / 180;
      }
      if (drop) { let u = -1; for (const d of o.sweat) if (t >= d && t < d + 0.6) u = (t - d) / 0.6; drop.visible = u >= 0; if (u >= 0) drop.position.set(top.x + 0.03, top.y - 0.005 - u * 0.09, top.z + 0.012); }
    };
    g.userData.update(0); if (o.onTop) onTop(g); return g;
  },

  // A big soup bowl on a table (pivot at its foot): white with a blue rim, pale golden soup (o.soup) at 0.088, a spoon resting on the rim at the
  // right; o.steam: three soft wisps; o.ripple [t, ...]: a ring spreading on the soup (something lands); o.lit [[t, v]]: the soup brightens
  // (the searchlight); o.r (0.2); (round 1) with o.lit a white-hot disc, a glare (o.glareS) and, with o.star, a twinkle
  chvBowl(o) {
    const Rb = o.r ?? 0.2, g = grp(), H = Rb * 0.55;
    const prof = [[0.001, 0], [Rb * 0.5, 0], [Rb * 0.55, 0.012], [Rb * 0.78, H * 0.35], [Rb * 0.95, H * 0.8], [Rb, H]].map(([x, y]) => new THREE.Vector2(x, y));
    const bowl = new THREE.Mesh(new THREE.LatheGeometry(prof, 24), mat(o.color || '#F7F4EC', { doubleSide: true })); bowl.castShadow = true; g.add(bowl);
    g.add(at(new THREE.Mesh(new THREE.TorusGeometry(Rb, 0.009, 6, 32), mat(o.rimColor || '#2F64B0')), 0, H, 0, PI / 2, 0, 0));
    g.add(at(new THREE.Mesh(new THREE.TorusGeometry(Rb * 0.87, 0.006, 4, 32), mat(o.rimColor || '#2F64B0')), 0, H * 0.62, 0, PI / 2, 0, 0));
    const sm = new THREE.MeshLambertMaterial({ color: o.soup || '#EFD48A', emissive: o.soup || '#EFD48A', emissiveIntensity: 0.0 });
    const soup = at(new THREE.Mesh(new THREE.CircleGeometry(Rb * 0.93, 28), sm), 0, H * 0.82, 0, -PI / 2, 0, 0); g.add(soup);
    for (let i = 0; i < 5; i++) { const a = i * 2.2 + 0.4, d = Rb * (0.3 + 0.45 * hsh(i)); g.add(at(box(0.022, 0.012, 0.022, '#D9A24A'), Math.cos(a) * d, H * 0.82 + 0.004, Math.sin(a) * d, 0, a, 0)); }   // croutons
    if (o.spoon !== false) { const sp = grp(at(box(0.024, 0.008, 0.26, '#C9CFD6', { outline: 0.002 }), 0, 0, 0.13), at(new THREE.Mesh(new THREE.SphereGeometry(0.035, 10, 6), mat('#C9CFD6')), 0, 0, 0.28)); sp.children[1].scale.set(0.8, 0.25, 1.1);
      sp.position.set(Rb * 0.95, H + 0.01, -0.02); sp.rotation.set(0.12, 1.75, 0); g.add(sp); }
    // (round 2) steam as three thin white squiggles low over the soup (soft discs read as grey smudges on a navy jacket)
    const wisps = []; if (o.steam) for (let i = 0; i < 3; i++) { const q = []; for (let j = 0; j < 12; j++) { const u = j / 11; q.push(new THREE.Vector3(0.014 * Math.sin(u * TAU * 1.4 + i * 2), u * 0.09, 0)); }
      const m = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(q), 18, 0.0032, 4), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0, depthWrite: false })); m.userData.ph = i / 3; g.add(noShadow(m)); wisps.push(m); }
    const ring = new THREE.Mesh(new THREE.TorusGeometry(1, 0.06, 4, 28), new THREE.MeshBasicMaterial({ color: '#FFF6D8', transparent: true, opacity: 0.8 })); ring.rotation.x = PI / 2; ring.position.y = H * 0.82 + 0.003; g.add(ring);
    g.userData.surface = H * 0.82;
    // (round 1) the hot spot of the searchlight: a white-hot disc on the soup, a glare above it and a four-point star (o.lit keys dose them)
    const hot = new THREE.Mesh(new THREE.CircleGeometry(Rb * 0.9, 28), softMat('#FFFBEA', 1, true)); hot.rotation.x = -PI / 2; hot.position.y = H * 0.82 + 0.006; g.add(noShadow(hot));
    const glare = new THREE.Sprite(new THREE.SpriteMaterial({ map: softTex(), color: '#FFF4CC', transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0 })); glare.position.y = H * 0.82 + 0.05; g.add(glare);
    const star = grp(); const stm = new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.9, depthWrite: false, blending: THREE.AdditiveBlending });
    for (let k = 0; k < 2; k++) { const r = new THREE.Mesh(new THREE.PlaneGeometry(0.018, 0.5), stm); r.rotation.z = k * PI / 2 + PI / 4; star.add(r); }
    star.position.set(-Rb * 0.25, H + 0.04, Rb * 0.5); g.add(noShadow(star));
    g.userData.update = t => {
      const lv = keyAt(o.lit, t, 0, 0.15);
      sm.emissiveIntensity = (o.litK ?? 0.9) * lv; hot.visible = lv > 0.01; hot.material.opacity = 0.85 * lv;
      glare.visible = lv > 0.01; glare.material.opacity = 0.9 * lv; glare.scale.setScalar(Rb * (o.glareS ?? 3.2) * (0.92 + 0.08 * Math.sin(t * 13)));
      star.visible = lv > 0.3 && !!o.star; star.scale.setScalar(Math.max(0.01, lv * (0.8 + 0.25 * Math.sin(t * 9)))); star.rotation.z = t * 0.8;
      wisps.forEach((m, i) => { const u = (t * 0.55 + m.userData.ph) % 1; m.position.set((i - 1) * 0.065 + 0.008 * Math.sin(t * 3 + i), H + 0.025 + u * 0.06, 0.03 * (1 - i)); m.scale.setScalar((0.7 + 0.4 * u) * (o.steamS ?? 1)); m.material.opacity = (o.steamOp ?? 0.9) * Math.sin(u * PI); });
      let rr = -1; for (const r0 of o.ripple || []) if (t >= r0 && t < r0 + 0.7) rr = (t - r0) / 0.7; ring.visible = rr >= 0;
      if (rr >= 0) { const s = 0.03 + rr * Rb * 0.8; ring.scale.set(s, s, 0.12); ring.material.opacity = 0.8 * (1 - rr); }
    };
    g.userData.update(0); return g;
  },

  // A round bistro table under a red-and-white checked cloth (pivot at the floor): top o.r (0.5) at o.h (0.76), the cloth hanging o.drop (0.32)
  chvTable(o) {
    const Rt = o.r ?? 0.5, H = o.h ?? 0.76, D = o.drop ?? 0.32, g = grp();
    const check = (rep) => { const c = document.createElement('canvas'); c.width = c.height = 128; const x = c.getContext('2d'); x.fillStyle = '#F6F2EA'; x.fillRect(0, 0, 128, 128); x.fillStyle = 'rgba(200,40,46,0.85)'; x.fillRect(0, 0, 64, 128); x.fillStyle = 'rgba(200,40,46,0.85)'; x.fillRect(0, 0, 128, 64); x.fillStyle = 'rgba(150,20,26,0.9)'; x.fillRect(0, 0, 64, 64);
      const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.wrapS = tx.wrapT = THREE.RepeatWrapping; tx.repeat.set(rep[0], rep[1]); tx.magFilter = THREE.NearestFilter; return tx; };
    const top = new THREE.Mesh(new THREE.CircleGeometry(Rt + 0.03, 32), new THREE.MeshLambertMaterial({ map: check([7, 7]) })); top.rotation.x = -PI / 2; top.position.y = H + 0.002; top.receiveShadow = true; g.add(top);
    const sk = new THREE.Mesh(new THREE.CylinderGeometry(Rt + 0.03, Rt + 0.07, D, 32, 1, true), new THREE.MeshLambertMaterial({ map: check([22, 2]), side: THREE.DoubleSide })); sk.position.y = H - D / 2; sk.castShadow = true; g.add(sk);
    g.add(at(cyl(0.05, 0.05, H - D, '#2A2B30', 8, { pivot: 'bottom' }), 0, 0, 0), at(cyl(0.25, 0.28, 0.03, '#2A2B30', 12), 0, 0.015, 0));
    g.userData.top = [0, H, 0]; return g;
  },

  // The bistro dining room (pivot at the floor centre; the back wall at o.back, -1.5): a cream wall over a dark red wainscot, a window opening
  // (o.win [cx, cy, w, h]) with green shutters swung open outside, a chalkboard SOUPE DU JOUR, a framed picture, two glowing sconces, a tiled
  // floor; outside nothing but the night (set a dark whiteVoid) and a few stars and the moon far behind (o.stars)
  chvRoom(o) {
    const W = o.w ?? 7, Hh = o.h ?? 3.3, Z = o.back ?? -1.5, T = 0.16, [cx, cy, ww, wh] = o.win || [0.8, 2.0, 1.4, 1.3], g = grp();
    const wall = o.wall || '#EBDDBE', wain = o.wain || '#7A3328', x0 = cx - ww / 2, x1 = cx + ww / 2, y0 = cy - wh / 2, y1 = cy + wh / 2;
    const piece = (xa, xb, ya, yb, c) => { if (xb - xa < 0.01 || yb - ya < 0.01) return; g.add(at(box(xb - xa, yb - ya, T, c), (xa + xb) / 2, (ya + yb) / 2, Z - T / 2)); };
    piece(-W / 2, x0, 1.0, Hh, wall); piece(x1, W / 2, 1.0, Hh, wall); piece(x0, x1, y1, Hh, wall); piece(x0, x1, 1.0, y0, wall);
    piece(-W / 2, W / 2, 0, 1.0, wain); g.add(at(box(W, 0.06, 0.04, '#4A1E18'), 0, 1.0, Z + 0.02));
    const fr = o.frame || '#2E5A46';
    g.add(at(box(ww + 0.12, 0.08, 0.22, '#F2EEE4', { outline: 0.006 }), cx, y0 - 0.02, Z + 0.04));   // the sill
    for (const [x, y, w, h] of [[x0 - 0.04, cy, 0.08, wh + 0.08], [x1 + 0.04, cy, 0.08, wh + 0.08], [cx, y1 + 0.04, ww + 0.16, 0.08]]) g.add(at(box(w, h, T + 0.04, fr, { outline: 0.006 }), x, y, Z - T / 2));
    for (const s of [-1, 1]) { const sh = grp(at(box(ww / 2, wh, 0.04, fr, { outline: 0.006 }), s * ww / 4, 0, 0)); for (let i = 0; i < 5; i++) sh.add(at(box(ww / 2 - 0.06, 0.03, 0.05, '#24483A'), s * ww / 4, -wh / 2 + 0.15 + i * (wh - 0.3) / 4, 0.01));
      sh.position.set(s > 0 ? x1 : x0, cy, Z - T - 0.03); sh.rotation.y = s * (o.shut ?? 0.45); g.add(sh); }
    if (o.board !== false) {   // the chalkboard
      const cb = canvasPlane(0.8, 1.0, (c, w, h) => { c.fillStyle = '#26302C'; c.fillRect(0, 0, w, h); c.fillStyle = '#F4F1E6'; c.textAlign = 'center'; c.font = `900 ${h * 0.12}px Arial`; c.fillText('SOUPE', w / 2, h * 0.2); c.fillText('DU JOUR', w / 2, h * 0.34);
        c.font = `700 ${h * 0.09}px Arial`; c.fillText('VELOUTÉ', w / 2, h * 0.56); c.fillText('6,50 €', w / 2, h * 0.72); c.strokeStyle = '#F4F1E6'; c.lineWidth = 3; c.beginPath(); c.moveTo(w * 0.2, h * 0.42); c.lineTo(w * 0.8, h * 0.42); c.stroke(); });
      const bx = o.boardX ?? -1.5; g.add(at(box(0.9, 1.1, 0.04, '#6B4A2E', { outline: 0.006 }), bx, 1.9, Z + 0.03), at(cb, bx, 1.9, Z + 0.055));
    }
    if (o.picture !== false) { const px = o.picX ?? 2.5; g.add(at(box(0.6, 0.5, 0.04, '#B88A3A', { outline: 0.006 }), px, 2.15, Z + 0.03), at(box(0.5, 0.4, 0.01, '#9CC2D8'), px, 2.15, Z + 0.055), at(box(0.5, 0.14, 0.012, '#6E9A5A'), px, 2.0, Z + 0.06)); }
    for (const sx of (o.sconces || [-0.4, 2.0])) { g.add(at(box(0.08, 0.16, 0.06, '#C9A043'), sx, 2.25, Z + 0.03), at(sphere(0.07, '#FFE9B0', 1, { emissive: '#FFD27A' }), sx, 2.38, Z + 0.1));
      const sp = new THREE.Mesh(new THREE.PlaneGeometry(0.7, 0.7), softMat('#FFD890', 0.35, true)); sp.position.set(sx, 2.38, Z + 0.12); g.add(noShadow(sp)); }
    const fl = canvasPlane(W, 6, (c, w, h) => { c.fillStyle = o.floor || '#D9CDB4'; c.fillRect(0, 0, w, h); c.fillStyle = o.floor2 || '#B7A88A'; const n = 14; for (let i = 0; i < n * 2; i++) for (let j = 0; j < n; j++) if ((i + j) % 2) c.fillRect(i * w / (n * 2), j * h / n, w / (n * 2), h / n); }, { res: 512 });
    fl.rotation.x = -PI / 2; fl.position.set(0, 0.012, Z + 3); fl.receiveShadow = true; g.add(fl);
    if (o.stars !== false) {   // the night outside the window
      const sk = canvasPlane(14, 9, (c, w, h) => { const gr = c.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#0E1530'); gr.addColorStop(1, '#2A3A66'); c.fillStyle = gr; c.fillRect(0, 0, w, h);
        c.fillStyle = '#FFFFFF'; for (let i = 0; i < 90; i++) { const r = 1 + 2 * hsh(i + 7); c.globalAlpha = 0.5 + 0.5 * hsh(i + 3); c.fillRect(hsh(i) * w, hsh(i + 50) * h * 0.85, r, r); } c.globalAlpha = 1;
        c.fillStyle = '#F4EFD8'; c.beginPath(); c.arc(w * 0.72, h * 0.22, h * 0.06, 0, TAU); c.fill(); }, { res: 1024, emissive: 1 });
      sk.material.color.set('#000000'); sk.position.set(cx, cy + 2.5, Z - 16); g.add(noShadow(sk));
    }
    g.userData.chvUnder = true; return g;
  },

  // Giant evidence tweezers (pivot at the hinge, the tips o.len (0.5) down -Y): two broad light steel blades (o.bw 0.06 wide) with dark ink
  // edges opened by o.open [[t, rad]] (0.18), black rubber grips; with o.hairAt a hair (o.hairL 0.4, o.r 0.012) hangs from the tips from then on,
  // swinging (o.swing), its pair of eyes (o.eyes, o.eyeS, o.blinks, o.brow [[t, v]]) right under the tips where it is pinched; o.rim: a pale
  // halo round the strand (a black hair over a dark uniform), o.rimW its width
  chvTweezers(o) {
    const Lt = o.len ?? 0.5, BW = o.bw ?? 0.06, g = grp(), bl = [], ST = o.steel || '#D3DAE2', TP = o.tip || '#E8ECF0';
    for (const s of [-1, 1]) { const b = grp(at(box(BW, Lt, 0.022, ST, { outline: 0.008, pivot: 'top', taper: { x: 0.55, z: 1 } }), 0, 0, 0), at(box(BW * 1.04, Lt * 0.3, 0.028, '#22262E', { outline: 0.004 }), 0, -Lt * 0.36, 0),
      at(box(BW * 0.6, 0.06, 0.02, TP, { outline: 0.004 }), -s * 0.01, -Lt + 0.02, 0, 0, 0, s * 0.3)); g.add(b); bl.push([b, s]); }
    g.add(at(box(BW * 1.4, 0.06, 0.04, '#9AA2AC', { outline: 0.005 }), 0, 0.015, 0), at(sphere(0.02, '#5A626C', 1), 0, 0.015, 0.022));
    const hr = grp(); g.add(hr); const hm = new THREE.MeshLambertMaterial({ color: HAIR }), tb = new THREE.Mesh(new THREE.BufferGeometry(), hm); hr.add(tb);
    const rimM = o.rim ? new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshBasicMaterial({ color: o.rim, side: THREE.BackSide })) : null; if (rimM) hr.add(rimM);
    const ey = o.eyes ? eyePair(o.eyeS ?? 1.4, true) : null; if (ey) hr.add(ey.g);
    const HL = o.hairL ?? 0.4, R = o.r ?? 0.012, pts = Array.from({ length: 30 }, () => new THREE.Vector3());
    g.userData.tips = [0, -Lt, 0];
    g.userData.update = t => {
      const op = keyAt(o.open, t, 0.18, 0.08); bl.forEach(([b, s]) => { b.rotation.z = s * op / 2; });
      hr.visible = o.hairAt != null && t >= o.hairAt; if (!hr.visible) return;
      const u0 = t - o.hairAt, sw = (o.swing ?? 0.6) * Math.exp(-2.2 * u0) * Math.sin(u0 * 9);
      pts.forEach((p, i) => { const u = i / 29; p.set(Math.sin(sw) * u * HL + 0.018 * Math.sin(u * 9 + t * 4) * u, -Lt + 0.01 - Math.cos(sw) * u * HL, 0.012 * Math.sin(u * 6 + t * 2)); });
      setTube(tb, pts, R, 40); if (rimM) setTube(rimM, pts, R * (o.rimW ?? 1.8), 40);
      if (ey) { const q = pts[2]; ey.g.position.set(q.x, q.y - 0.01, q.z + R * 1.6); ey.g.rotation.z = sw * 0.3; let lid = 0; for (const b of o.blinks || []) { const u = t - b; if (u >= 0 && u < 0.12) lid = 1 - Math.abs(u - 0.06) / 0.06; }
        const gz = (o.gaze || []).filter(k => t >= k[0]).pop() || [0, 0, 0]; ey.set(gz[1], gz[2], lid, keyAt(o.brow, t, -0.6, 0.1)); }
    };
    g.userData.update(0); return g;
  },

  // (round 1) A clear evidence bag held open (pivot at its middle, facing +Z): a pale see-through pouch o.w (0.3) x o.h (0.4) with a white
  // edge seam, a zip strip along the open top (white), a big red label band with white writing (o.text 'SCELLÉ', o.num 'N° 0088')
  chvBag(o) {
    const W = o.w ?? 0.3, H = o.h ?? 0.4, g = grp();
    const film = new THREE.Mesh(new THREE.BoxGeometry(W, H, 0.03), new THREE.MeshLambertMaterial({ color: '#DDEEF6', transparent: true, opacity: 0.38, depthWrite: false })); film.renderOrder = 2; g.add(film);
    for (const [x, y, w, h] of [[-W / 2, 0, 0.012, H], [W / 2, 0, 0.012, H], [0, -H / 2, W, 0.012]]) g.add(at(box(w, h, 0.034, '#F4F8FA'), x, y, 0));
    g.add(at(box(W + 0.01, 0.025, 0.04, '#FFFFFF', { outline: 0.003 }), 0, H / 2, 0));
    const lab = canvasPlane(W * 0.86, H * 0.3, (c, w, h) => { c.fillStyle = '#C8202A'; c.fillRect(0, 0, w, h); c.fillStyle = '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle';
      c.font = `900 ${h * 0.38}px Arial`; c.fillText(o.text || 'SCELLÉ', w / 2, h * 0.34); c.font = `700 ${h * 0.26}px Arial`; c.fillText(o.num || 'N° 0088', w / 2, h * 0.74); }, { res: 256 });
    lab.position.set(0, -H * 0.2, 0.018); g.add(lab);
    g.userData.grip = [0, H / 2, 0]; return g;
  },

  // A mugshot height chart sized for a hair (pivot at the floor centre, facing +Z): a pale board o.w (0.8) x o.h (0.62) with grey lines every
  // 5 cm and numbered every 10 (cm), a pale ledge to stand on (top 0.03)
  chvMugWall(o) {
    const W = o.w ?? 0.8, H = o.h ?? 0.62, g = grp();
    const pl = canvasPlane(W, H, (c, w, h) => { c.fillStyle = o.color || '#E9EDF0'; c.fillRect(0, 0, w, h); c.fillStyle = '#7E8B98'; c.font = `900 ${h * 0.055}px Arial`; c.textBaseline = 'middle';
      for (let cm = 5; cm * 0.01 < H - 0.02; cm += 5) { const y = h * (1 - (cm * 0.01 + 0.03) / H), thick = cm % 10 === 0; c.fillRect(thick ? w * 0.13 : w * 0.18, y - (thick ? 2 : 1), thick ? w * 0.74 : w * 0.64, thick ? 4 : 2);
        if (thick) { c.textAlign = 'left'; c.fillText(String(cm), w * 0.015, y); c.textAlign = 'right'; c.fillText(String(cm), w * 0.985, y); } } }, { res: 512 });
    g.add(at(pl, 0, H / 2, 0), at(box(W + 0.04, H + 0.04, 0.02, '#5E6670'), 0, H / 2, -0.012), at(box(W, 0.03, 0.22, '#D2D7DC', { outline: 0.003 }), 0, 0.015, 0.11));
    return g;
  },

  // The interrogation lamp clamped on the table (pivot at its base): a dark post o.h (0.85) high, an arm reaching o.reach (0.5) forward, a big
  // metal shade at its end pointing down (o.tilt rad toward the front, 0.25); a glowing bulb, a soft cone of light o.beamLen (0.9) long and a warm
  // point light; o.heat [[t, v]]: 0 white .. 1 hot orange (brighter, the shade glows, a heat shimmer)
  chvLamp(o) {
    const Hp = o.h ?? 0.85, Rr = o.reach ?? 0.5, g = grp(), C = '#2B2F36';
    g.add(at(cyl(0.12, 0.14, 0.04, C, 12, { outline: 0.004 }), 0, 0.02, 0), at(cyl(0.02, 0.02, Hp, C, 8, { pivot: 'bottom' }), 0, 0, 0), at(sphere(0.035, C, 1), 0, Hp, 0));
    g.add(rod([0, Hp, 0], [0, Hp + 0.08, Rr], 0.018, C), at(sphere(0.03, C, 1), 0, Hp + 0.08, Rr));
    const head = grp(); head.position.set(0, Hp + 0.08, Rr); head.rotation.x = o.tilt ?? 0.25; g.add(head);
    const sm = new THREE.MeshLambertMaterial({ color: o.shade || '#3E5A4E', side: THREE.DoubleSide, emissive: '#FF6A20', emissiveIntensity: 0 });
    const shade = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.2, 0.2, 18, 1, true), sm); shade.position.y = -0.1; shade.castShadow = true; head.add(shade);
    head.add(at(cyl(0.05, 0.05, 0.03, C, 12), 0, 0, 0));
    const bm = new THREE.MeshBasicMaterial({ color: '#FFF4D0' }), bulb = new THREE.Mesh(new THREE.SphereGeometry(0.07, 12, 8), bm); bulb.position.y = -0.17; head.add(bulb);
    const BL = o.beamLen ?? 0.9, cone = beamCone(BL, 0.19, o.beamR ?? 0.5, '#FFE7A8', 0.16, 0.5, 20), cm = cone.material; cone.position.y = -0.2; head.add(cone);   // (round 1) behind people
    const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: softTex(), color: '#FFE2A0', transparent: true, opacity: 0.6, depthWrite: false, blending: THREE.AdditiveBlending })); halo.position.y = -0.2; halo.scale.setScalar(0.45); head.add(halo);   // (round 1) a sprite: the flat disc read as a line seen edge-on
    const L = new THREE.PointLight('#FFD9A0', o.power ?? 4, o.range ?? 3.5, 1.2); L.position.y = -0.3; head.add(L);
    g.userData.update = t => { onTopActors(g); const h = keyAt(o.heat, t, 0, 0.3), fl = 1 + 0.06 * h * Math.sin(t * 23);
      bm.color.setRGB(1, 0.96 - 0.35 * h, 0.82 - 0.65 * h); cm.color.setRGB(1, 0.9 - 0.3 * h, 0.66 - 0.5 * h); cm.opacity = (o.beamOp ?? 0.16) * (1 + 0.6 * h) * fl; sm.emissiveIntensity = 0.5 * h;
      L.intensity = (o.power ?? 4) * (1 + 0.8 * h) * fl; L.color.setRGB(1, 0.85 - 0.3 * h, 0.63 - 0.45 * h); halo.material.color.setRGB(1, 0.89 - 0.3 * h, 0.63 - 0.45 * h); };
    g.userData.update(0); return g;
  },

  // A police file lying open on the table (pivot at its middle, flat, the text toward +Z): a manila folder, a white sheet with a photo of the
  // hair (a black squiggle) and typed lines; at o.stampAt a red stamp mark o.stamp ('RETENU') lands across it (pop, then stays); o.s scales it
  chvFile(o) {
    const S = o.s ?? 1, g = grp();
    g.add(at(box(0.62 * S, 0.012, 0.44 * S, '#D9AE5E', { outline: 0.003 }), 0, 0.006, 0));
    const sheet = canvasPlane(0.56 * S, 0.4 * S, (c, w, h) => { c.fillStyle = '#F8F6F0'; c.fillRect(0, 0, w, h); c.fillStyle = '#FFFFFF'; c.fillRect(w * 0.06, h * 0.1, w * 0.3, h * 0.55); c.strokeStyle = '#3A3D44'; c.lineWidth = 2; c.strokeRect(w * 0.06, h * 0.1, w * 0.3, h * 0.55);
      c.strokeStyle = '#111114'; c.lineWidth = w * 0.012; c.lineCap = 'round'; c.beginPath(); for (let i = 0; i <= 30; i++) { const u = i / 30, x = w * 0.21 + Math.sin(u * 9) * w * 0.035, y = h * 0.6 - u * h * 0.42; i ? c.lineTo(x, y) : c.moveTo(x, y); } c.stroke();
      c.fillStyle = '#4A4E58'; for (let i = 0; i < 7; i++) c.fillRect(w * 0.42, h * (0.14 + i * 0.1), w * (0.45 - 0.05 * (i % 3)), h * 0.025); c.font = `900 ${h * 0.09}px Arial`; c.fillStyle = '#1C1E24'; c.fillText('N° 0088', w * 0.06, h * 0.84); }, { res: 512 });
    sheet.rotation.x = -PI / 2; sheet.position.y = 0.014; g.add(sheet);
    const st = canvasPlane(0.42 * S, 0.14 * S, (c, w, h) => { c.clearRect(0, 0, w, h); c.strokeStyle = '#C8202A'; c.lineWidth = h * 0.1; c.strokeRect(h * 0.08, h * 0.08, w - h * 0.16, h * 0.84); c.fillStyle = '#C8202A'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${h * 0.62}px Arial`; c.fillText(o.stamp || 'RETENU', w / 2, h * 0.54); }, { res: 512, transparent: true });
    st.rotation.set(-PI / 2, 0, 0.18); st.position.set(0.04 * S, 0.018, 0.02 * S); g.add(st);
    // (round 2) o.bounceAt: the file jumps off the table under the slam and settles
    const inner = grp(); while (g.children.length) inner.add(g.children[0]); g.add(inner);
    g.userData.update = t => { const u = o.stampAt == null ? 1 : t - o.stampAt; st.visible = u >= 0; if (u >= 0) st.scale.setScalar(u < 0.1 ? 1.25 - 0.25 * (u / 0.1) : 1);
      const v = o.bounceAt == null ? -1 : t - o.bounceAt; inner.position.y = v > 0.03 && v < 0.8 ? 0.04 * Math.exp(-6 * v) * Math.abs(Math.sin((v - 0.03) * 16)) : 0; inner.rotation.x = v > 0.03 && v < 0.8 ? -0.05 * Math.exp(-6 * v) * Math.sin((v - 0.03) * 16) : 0; };
    g.userData.update(0); return g;
  },

  // A battering ram (pivot at its middle, the striking end toward +Z): a dark steel cylinder o.len (1.1) long with a flat head, two yellow
  // carrying handles on top (userData.grips: local points for the hands, left and right)
  chvRam(o) {
    const L = o.len ?? 1.1, g = grp(), R = o.r ?? 0.09, C = o.color || '#2B2F36', Y = o.trim || '#E8B931';
    g.add(at(cyl(R, R, L, C, 12, { outline: 0.006 }), 0, 0, 0, PI / 2, 0, 0), at(box(R * 2.6, R * 2.6, 0.06, '#1A1C20', { outline: 0.006 }), 0, 0, L / 2 + 0.03), at(cyl(R * 1.1, R * 1.1, 0.05, '#1A1C20', 12), 0, 0, -L / 2, PI / 2, 0, 0));
    for (const z of [-0.28, 0.22]) { g.add(at(box(0.03, 0.12, 0.03, Y, { outline: 0.004 }), 0, R + 0.06, z - 0.08), at(box(0.03, 0.12, 0.03, Y, { outline: 0.004 }), 0, R + 0.06, z + 0.08), at(box(0.035, 0.035, 0.2, Y, { outline: 0.004 }), 0, R + 0.12, z)); }
    for (const z of [-0.45, 0.45]) g.add(at(cyl(R * 1.08, R * 1.08, 0.04, Y, 12), 0, 0, z, PI / 2, 0, 0));
    g.userData.grips = [[0, R + 0.12, -0.28], [0, R + 0.12, 0.22]]; return g;
  },

  // A wall with a front door that falls flat (pivot at the floor under the doorway's middle; the wall in the XY plane): wall o.w (3) x o.h (3), a
  // doorway o.dw (1.0) x o.dh (2.15); the leaf (o.door colour, panels, a brass knob, a number plaque o.num) falls at o.fallAt toward o.dir (+1:
  // toward +Z, -1: toward -Z) about its bottom edge in o.fallDur (0.24 s), bounces, a puff of dust at the landing; o.facade: a townhouse front (o.h
  // 6, two windows, a cornice, o.color); o.dark: a dark room behind the doorway on the side the door falls to; (round 1) o.bounce (0.12 rad),
  // o.bounceF, o.bounceDecay: the rebound after the slam; o.slamSq: the leaf squashes as it lands; o.puffOut: the dust blows out on the near
  // side of the doorway (the street), o.puffS / o.puffUp its size and rise
  chvDoorWall(o) {
    const W = o.w ?? 3, H = o.h ?? (o.facade ? 6 : 3), dw = o.dw ?? 1.0, dh = o.dh ?? 2.15, T = 0.2, dir = o.dir ?? 1, g = grp(), wc = o.color || '#E2D3B4';
    g.add(at(box((W - dw) / 2, H, T, wc), -(W + dw) / 4, H / 2, 0), at(box((W - dw) / 2, H, T, wc), (W + dw) / 4, H / 2, 0), at(box(dw, H - dh, T, wc), 0, dh + (H - dh) / 2, 0));
    const tr = o.trim || '#F4F0E6';
    for (const s of [-1, 1]) g.add(at(box(0.1, dh + 0.1, T + 0.06, tr, { outline: 0.006 }), s * (dw / 2 + 0.05), (dh + 0.1) / 2, 0));
    g.add(at(box(dw + 0.3, 0.12, T + 0.08, tr, { outline: 0.006 }), 0, dh + 0.1, 0));
    if (o.facade) {
      for (const sx of [-1, 1]) { const wx = sx * W * 0.25; for (const wy of [3.3, 4.9]) g.add(at(box(0.7, 1.0, T + 0.04, tr, { outline: 0.006 }), wx, wy, 0), at(box(0.56, 0.86, T + 0.06, '#34485E'), wx, wy, 0)); }
      g.add(at(box(W + 0.1, 0.18, T + 0.25, tr, { outline: 0.006 }), 0, H, 0), at(box(W, 0.1, T + 0.12, tr), 0, 2.75, 0));
    }
    if (o.dark) g.add(at(box(dw + 0.2, dh + 0.1, 1.6, '#17181C'), 0, (dh + 0.1) / 2, (o.darkDir ?? dir) * 0.9));
    const piv = grp(); piv.position.set(0, 0.0, dir * (T / 2)); g.add(piv);
    const leaf = grp(at(box(dw - 0.04, dh - 0.03, 0.06, o.door || '#2F5D8A', { outline: 0.008, pivot: 'bottom' }), 0, 0, 0)); piv.add(leaf);
    for (const [py, ph] of [[0.25, 0.75], [1.15, 0.75]]) for (const sx of [-1, 1]) leaf.add(at(box(dw * 0.36, ph, 0.02, '#244A70', { outline: 0.003 }), sx * dw * 0.22, py + ph / 2, -dir * 0.035));
    leaf.add(at(sphere(0.035, '#E2B53C', 1), dw * 0.36, dh * 0.47, -dir * 0.05));
    if (o.num) leaf.add(at(canvasPlane(0.16, 0.12, (c, w, h) => { c.fillStyle = '#F4F1E6'; c.fillRect(0, 0, w, h); c.fillStyle = '#1C1E24'; c.font = `900 ${h * 0.75}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(String(o.num), w / 2, h * 0.55); }, { res: 128 }), 0, dh * 0.82, -dir * 0.04, 0, dir > 0 ? PI : 0, 0));
    const puffs = []; for (let i = 0; i < 10; i++) { const m = new THREE.Mesh(new THREE.PlaneGeometry(0.4, 0.4), softMat('#D8CFC0', 0.7)); m.visible = false; m.userData.a = hsh(i) * TAU; g.add(noShadow(m)); puffs.push(m); }
    g.userData.update = t => {
      const u = o.fallAt == null ? -1 : t - o.fallAt, D = o.fallDur ?? 0.24;
      let a = 0; if (u >= 0) { if (u < D) a = (PI / 2) * (u / D) * (u / D); else { const v = u - D; a = PI / 2 - (o.bounce ?? 0.12) * Math.exp(-(o.bounceDecay ?? 9) * v) * Math.abs(Math.sin(v * (o.bounceF ?? 22))); } }
      if (o.slamSq && u >= D) { const v = u - D, k = Math.exp(-14 * v) * Math.cos(v * 40); leaf.scale.set(1 + 0.08 * k, 1 - 0.05 * k, 1); }
      piv.rotation.x = dir * Math.min(PI / 2, a);
      const pu = u - D; puffs.forEach((m, i) => { m.visible = pu >= 0 && pu < 0.9; if (!m.visible) return; const k = pu / 0.9, rx = (i / 9 - 0.5) * dw * 1.3; m.position.set(rx + Math.cos(m.userData.a) * k * 0.4, 0.12 + k * (o.puffUp ?? 0.5) * (0.5 + hsh(i + 3)), o.puffOut ? -dir * (0.2 + k * (0.4 + 0.6 * hsh(i + 9))) : dir * (dh * (0.2 + 0.8 * hsh(i + 9)) + 0.1));
        m.scale.setScalar((0.6 + k * 1.8) * (o.puffS ?? 1)); m.material.opacity = 0.7 * (1 - k); m.lookAt(m.position.x, m.position.y, m.position.z + (o.puffOut ? -dir : dir) * 10); });
    };
    if (o.under) g.userData.chvUnder = true;   // (round 2) drawn before the beams: a torch beam stays visible in front of it
    g.userData.update(0); return g;
  },

  // A short hallway seen from inside (pivot at the floor under the front door's middle; the hall runs toward +Z): floor boards, two side walls
  // o.hw (1.7) apart, a ceiling at o.h (2.9), a bare bulb, a coat rack with a hat, a framed photo
  chvHall(o) {
    const HW = o.hw ?? 1.7, Lh = o.len ?? 4.5, Hc = o.h ?? 2.9, g = grp(), wc = o.wall || '#D6C3A0';
    const fl = canvasPlane(HW, Lh, (c, w, h) => { c.fillStyle = '#8A6644'; c.fillRect(0, 0, w, h); c.fillStyle = '#6E5034'; for (let i = 1; i < 6; i++) c.fillRect(i * w / 6 - 2, 0, 4, h); }, { res: 256 });
    fl.rotation.x = -PI / 2; fl.position.set(0, 0.012, Lh / 2); fl.receiveShadow = true; g.add(fl);
    for (const s of [-1, 1]) g.add(at(box(0.1, Hc, Lh, wc), s * (HW / 2 + 0.05), Hc / 2, Lh / 2), at(box(0.04, 0.12, Lh, '#7A5A3A'), s * HW / 2, 0.06, Lh / 2));
    g.add(at(box(HW + 0.2, 0.1, Lh, '#F2EEE4'), 0, Hc + 0.05, Lh / 2));
    g.add(at(cyl(0.006, 0.006, 0.4, '#222', 4, { pivot: 'top' }), 0, Hc, 1.6), at(sphere(0.06, '#FFE9B0', 1, { emissive: '#FFD27A' }), 0, Hc - 0.45, 1.6));
    g.add(at(box(0.04, 1.75, 0.04, '#5A3A28', { pivot: 'bottom' }), -HW / 2 + 0.12, 0, 1.2), at(box(0.3, 0.04, 0.04, '#5A3A28'), -HW / 2 + 0.12, 1.7, 1.2), at(cyl(0.12, 0.13, 0.12, '#3A3D44', 10), -HW / 2 + 0.16, 1.82, 1.2));
    g.add(at(box(0.04, 0.4, 0.5, '#B88A3A', { outline: 0.005 }), HW / 2 - 0.02, 1.6, 1.9), at(box(0.02, 0.32, 0.42, '#9CC2D8'), HW / 2 - 0.04, 1.6, 1.9));
    const L = new THREE.PointLight('#FFE2B0', o.power ?? 2.5, 5, 1.4); L.position.set(0, Hc - 0.55, 1.6); g.add(L);
    return g;
  },

  // Electric hair clippers (pivot at the middle of the body, the blade toward +Y, the switch toward +Z): a dark grey body, a steel blade with a
  // black comb, a red switch, a short coiled cord at the bottom; o.buzz [[t0, t1], ...]: it vibrates and buzz arcs flicker either side;
  // o.bits [[t0, t1, colour], ...]: cut hair falls from the blade; o.s scales it; (round 1) o.sq [[t, [sx, sy, sz]], ...]: keyed squash and
  // stretch (eased over 0.05 s): it stretches into a pass and squashes as it recoils off the scalp; (final pass) o.rim: a bright edge (a
  // back-face shell o.rimW 0.008 wide round body and blade: it reads against a dark doorway)
  chvClippers(o) {
    const S = o.s ?? 1, g = grp(), b = grp(); b.scale.setScalar(S); g.add(b);
    b.add(at(box(0.065, 0.17, 0.048, o.color || '#3A3F4A', { outline: 0.005, taper: { x: 0.85, z: 0.85 } }), 0, 0, 0), at(box(0.068, 0.04, 0.05, '#2A2E36', { outline: 0.004 }), 0, -0.07, 0));
    b.add(at(box(0.075, 0.025, 0.046, '#D2D8DE', { outline: 0.004 }), 0, 0.098, 0));
    if (o.rim) b.add(new THREE.Mesh(new THREE.BoxGeometry(0.065 + 2 * (o.rimW ?? 0.008), 0.25 + 2 * (o.rimW ?? 0.008), 0.048 + 2 * (o.rimW ?? 0.008)).translate(0, 0.015, 0), new THREE.MeshBasicMaterial({ color: o.rim, side: THREE.BackSide })));
    for (let i = 0; i < 9; i++) b.add(at(box(0.005, 0.02, 0.02, '#16171B'), -0.034 + i * 0.0085, 0.118, 0.006));
    b.add(at(box(0.02, 0.03, 0.01, '#D23A2E', { outline: 0.002 }), 0, 0.02, 0.028), at(box(0.04, 0.005, 0.002, '#7E8696'), 0, -0.02, 0.025), at(box(0.04, 0.005, 0.002, '#7E8696'), 0, -0.035, 0.025));
    const cord = []; for (let i = 0; i < 14; i++) { const a = i * 1.4; cord.push(new THREE.Vector3(Math.cos(a) * 0.012, -0.09 - i * 0.008, Math.sin(a) * 0.012)); }
    b.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(cord), 40, 0.004, 4), mat('#1E2026')));
    const arcs = []; for (const s of [-1, 1]) for (let j = 0; j < 2; j++) { const a = new THREE.Mesh(new THREE.TorusGeometry(0.05 + j * 0.03, 0.004, 3, 10, 1.4), new THREE.MeshBasicMaterial({ color: o.arcColor || '#FFFFFF' })); a.rotation.z = s > 0 ? -0.7 : PI - 0.7; a.position.y = 0.06; b.add(a); arcs.push([a, s, j]); }
    const bits = []; for (let i = 0; i < 14; i++) { const m = new THREE.Mesh(new THREE.BoxGeometry(0.004, 0.03, 0.004), new THREE.MeshBasicMaterial({ color: '#2A2420' })); m.visible = false; g.add(m); bits.push(m); }
    g.userData.update = t => {
      const on = inWin(o.buzz, t);
      b.position.set(on ? 0.003 * Math.sin(t * 260) : 0, on ? 0.002 * Math.sin(t * 310) : 0, 0); b.rotation.z = on ? 0.03 * Math.sin(t * 190) : 0;
      if (o.sq) { const q = sqAt(o.sq, t, 0.05); b.scale.set(S * q[0], S * q[1], S * q[2]); }
      arcs.forEach(([a, s, j]) => { a.visible = on && (Math.floor(t * 30) + j) % 2 === 0; });
      const win = (o.bits || []).find(w => t >= w[0] && t < w[1] + 0.8);
      bits.forEach((m, i) => { if (!win) { m.visible = false; return; } const t0 = win[0] + (i / 14) * (win[1] - win[0]), u = t - t0; m.visible = u >= 0 && u < 0.8; if (!m.visible) return;
        m.material.color.set(win[2] || '#2A2420'); m.position.set(((hsh(i) - 0.5) * 0.12) * S, (0.1 - 2.2 * u * u) * S, ((hsh(i + 5) - 0.5) * 0.08) * S); m.rotation.set(u * 9 + i, i, u * 7); m.scale.setScalar(S * 1.6); });
    };
    g.userData.update(0); return g;
  },

  // A pile of cut hair on the pavement with its evidence tag (pivot at the floor): a lumpy mound of o.color (and a few loose strands) that grows
  // with o.grow [[t, v]] (0..1, 1 = o.r 0.18 wide); the tag: a white card o.tagS (1) on a wire stake with a black number o.num and a red string,
  // facing +Z (turn the prop to the camera); (round 1) o.tufts [t, ...]: a fist-sized tuft (o.tuftS 0.11) pops onto the pile at each time
  chvHairPile(o) {
    const R = o.r ?? 0.18, C = o.color || '#3A2A20', g = grp(), pile = grp(); g.add(pile);
    const dark = new THREE.Color(C).multiplyScalar(0.6).getStyle();
    // (round 2) o.curly: the pile is a heap of loose curls and strands (lumps read as potatoes), a low dark core under them
    const curl = (col, sz, sd) => { const q = [], n = 2 + hsh(sd) * 1.5, rr = sz * (0.35 + 0.25 * hsh(sd + 1)); for (let j = 0; j <= 18; j++) { const u = j / 18, th = u * n * TAU; q.push(new THREE.Vector3(rr * Math.cos(th), (u - 0.5) * sz * 0.9, rr * Math.sin(th))); }
      const m = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(q), 30, sz * 0.09, 5), mat(col)); m.rotation.set(hsh(sd + 2) * PI, hsh(sd + 3) * PI, hsh(sd + 4) * PI); return m; };
    if (o.curly) { const core = new THREE.Mesh(new THREE.SphereGeometry(1, 10, 6, 0, TAU, 0, PI / 2), mat(dark)); core.scale.set(R * 0.62, R * 0.3, R * 0.62); pile.add(core);
      for (let i = 0; i < 26; i++) { const a = hsh(i + 11) * TAU, d = R * 0.7 * Math.sqrt(hsh(i + 23)), m = curl(i % 3 ? C : dark, R * (0.42 + 0.2 * hsh(i + 5)), i * 7 + 1); m.position.set(Math.cos(a) * d, R * 0.12 + R * 0.38 * (1 - d / (R * 0.7)) * hsh(i + 31), Math.sin(a) * d); pile.add(m); } }
    else for (let i = 0; i < 7; i++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 1), mat(C)); const a = i * 0.9, d = i ? R * 0.5 * hsh(i) : 0; m.position.set(Math.cos(a) * d, 0, Math.sin(a) * d); m.scale.set(R * (0.7 - 0.06 * i), R * (0.45 - 0.04 * i), R * (0.7 - 0.06 * i)); pile.add(m); }
    for (let i = 0; i < 12; i++) { const a = hsh(i) * TAU, pts = []; for (let j = 0; j < 6; j++) pts.push(new THREE.Vector3(Math.cos(a) * R * (0.3 + j * 0.13), R * 0.35 - j * 0.05 + 0.05 * Math.sin(j * 2 + i), Math.sin(a) * R * (0.3 + j * 0.13) + 0.02 * Math.cos(j * 3)));
      pile.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 12, 0.006, 4), mat(i % 2 ? dark : C))); }
    const S = o.tagS ?? 1, tag = grp(); tag.position.set(R * 0.9, 0, R * 0.4); g.add(tag);
    tag.add(at(cyl(0.004, 0.004, 0.3 * S, '#8A8E92', 4, { pivot: 'bottom' }), 0, 0, 0));
    tag.add(at(canvasPlane(0.14 * S, 0.09 * S, (c, w, h) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, w, h); c.strokeStyle = '#C8202A'; c.lineWidth = h * 0.08; c.strokeRect(0, 0, w, h); c.fillStyle = '#16171B'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${h * 0.6}px Arial`; c.fillText(String(o.num ?? 1), w / 2, h * 0.56); }, { res: 128 }), 0, 0.3 * S + 0.045 * S, 0.004));
    tag.add(at(box(0.144 * S, 0.094 * S, 0.004, '#C8202A'), 0, 0.3 * S + 0.045 * S, 0));
    const tufts = (o.tufts || []).map((t0, i) => { const tg = grp(), a = i * 2.4 + hsh(i + 2) * 0.8, d = R * (0.25 + 0.5 * hsh(i + 4)), ts = o.tuftS ?? 0.11;
      if (o.curly) { for (let j = 0; j < 3; j++) { const m = curl(j % 2 ? dark : C, ts * 1.3, i * 13 + j * 5 + 3); m.position.set((hsh(i + j) - 0.5) * ts, 0, (hsh(i + j + 9) - 0.5) * ts); tg.add(m); } }
      else { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(ts, 1), mat(i % 2 ? dark : C)); m.scale.set(1, 0.7, 1); tg.add(m); }
      for (let j = 0; j < 5; j++) { const b = hsh(i * 7 + j) * TAU, q = []; for (let k = 0; k < 5; k++) q.push(new THREE.Vector3(Math.cos(b) * ts * (0.4 + k * 0.28), ts * (0.3 + 0.25 * Math.sin(k * 1.7 + j)), Math.sin(b) * ts * (0.4 + k * 0.28)));
        tg.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(q), 8, 0.005, 4), mat(j % 2 ? dark : C))); }
      tg.position.set(Math.cos(a) * d, R * 0.25 + ts * 0.5 * (i % 3), Math.sin(a) * d); g.add(tg); return [tg, t0]; });
    g.userData.update = t => { const v = keyAt(o.grow, t, 1, 0.3); pile.scale.set(Math.max(0.01, v), Math.max(0.01, v), Math.max(0.01, v)); pile.visible = v > 0.02;
      for (const [tg, t0] of tufts) { const u = t - t0; tg.visible = u >= 0; if (u >= 0) tg.scale.setScalar(Math.max(0.01, outBack(u / 0.18))); } };
    g.userData.update(0); return g;
  },

  // A shine on a bald head (attach to the head joint, offset about [0, 0.5, 0.02] in the joint's units): a soft white highlight lying on the top
  // of the head, tilted toward the front, and a four-point glint that twinkles at o.twinkle [t, ...] (and o.tw0: always a faint one); o.s;
  // (round 1) o.flare [[t, size], ...]: a big flare of the glint (size times) over 0.45 s
  chvShine(o) {
    const S = o.s ?? 1, g = grp();
    const hl = new THREE.Mesh(new THREE.PlaneGeometry(0.16 * S, 0.08 * S), softMat('#FFFFFF', o.opacity ?? 0.85)); hl.rotation.x = -PI / 2 + (o.tilt ?? 0.5); hl.position.set(-0.03 * S, 0.004, 0.02 * S); g.add(noShadow(hl));
    const star = grp(); const sm = new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 1, depthWrite: false });
    for (let k = 0; k < 2; k++) { const r = new THREE.Mesh(new THREE.PlaneGeometry(0.012 * S, 0.12 * S), sm); r.rotation.z = k * PI / 2; star.add(r); }
    star.add(new THREE.Mesh(new THREE.PlaneGeometry(0.06 * S, 0.06 * S), softMat('#FFFFFF', 1))); star.position.set(0.04 * S, 0.03 * S, 0.06 * S); g.add(noShadow(star));
    g.userData.update = t => { let k = o.tw0 ?? 0.35; for (const t0 of o.twinkle || []) { const u = t - t0; if (u >= 0 && u < 0.3) k = Math.max(k, Math.sin(u / 0.3 * PI)); }
      let big = 1; for (const [t0, b] of o.flare || []) { const u = t - t0; if (u >= 0 && u < 0.45) big = Math.max(big, 1 + (b - 1) * Math.sin(u / 0.45 * PI)); if (u >= 0 && u < 0.45) k = Math.max(k, 1); }
      star.scale.setScalar(Math.max(0.01, k * big)); star.rotation.z = t * 1.5; star.visible = k > 0.02; };
    g.userData.update(0); return g;
  },

  // A laboratory microscope (pivot at its base, facing +Z: the stage and the slide toward the front): a black base, a white curved arm, the stage
  // with a glass slide and a hair on it, a turret of three objectives, the tube and the eyepiece slanting back up; a light under the stage; o.s
  chvMicroscope(o) {
    const S = o.s ?? 1, g = grp(), b = grp(); b.scale.setScalar(S); g.add(b); const W = '#F2F2EE', K = '#1E2026';
    b.add(at(box(0.24, 0.05, 0.3, K, { outline: 0.004 }), 0, 0.025, 0), at(box(0.07, 0.34, 0.08, W, { outline: 0.004, pivot: 'bottom' }), 0, 0.05, -0.1, -0.15, 0, 0));
    b.add(at(box(0.2, 0.02, 0.17, K, { outline: 0.004 }), 0, 0.2, 0.03), at(box(0.12, 0.004, 0.05, '#BFE4F2', { opacity: 0.8 }), 0, 0.212, 0.04), at(box(0.07, 0.004, 0.006, HAIR), 0, 0.216, 0.04, 0, 0.5, 0));
    b.add(at(sphere(0.022, '#FFF2C0', 1, { emissive: '#FFE490' }), 0, 0.17, 0.04));
    b.add(at(cyl(0.04, 0.04, 0.04, K, 10), 0, 0.33, 0.02), ...[-1, 0, 1].map(i => at(cyl(0.012, 0.016, 0.07, i ? '#C9CFD6' : '#D9B44A', 8, { outline: 0.003 }), i * 0.025, 0.28, 0.03 + Math.abs(i) * 0.01, i * 0.3, 0, 0)));
    b.add(at(cyl(0.03, 0.035, 0.22, W, 10, { outline: 0.004 }), 0, 0.42, -0.02, -0.55, 0, 0), at(cyl(0.022, 0.022, 0.07, K, 10, { outline: 0.003 }), 0, 0.52, -0.075, -0.55, 0, 0));
    b.add(at(cyl(0.025, 0.025, 0.05, '#C9CFD6', 10), 0.09, 0.2, -0.05, 0, 0, PI / 2), at(cyl(0.025, 0.025, 0.05, '#C9CFD6', 10), -0.09, 0.2, -0.05, 0, 0, PI / 2));
    return g;
  },

  // Shelves of labelled hair samples (pivot at the floor centre, facing +Z): a grey metal rack o.w (2.4) x o.h (2.0), three shelves, on each o.n
  // (7) clear bags with a lock of hair inside (brown, blond, black, red, grey, white) and a white label with a number
  chvBagShelf(o) {
    const W = o.w ?? 2.4, H = o.h ?? 2.0, D = 0.35, n = o.n ?? 7, g = grp(), C = '#7E868F', cols = ['#5A3A22', '#D8B25A', '#1E1C1E', '#B5532A', '#9A9A96', '#EDEBE4', '#3A2A20'];
    for (const s of [-1, 1]) for (const z of [-1, 1]) g.add(at(box(0.04, H, 0.04, C, { pivot: 'bottom' }), s * W / 2, 0, z * D / 2));
    const lab = document.createElement('canvas'); lab.width = 512; lab.height = 64; const x = lab.getContext('2d');
    [0.5, 1.1, 1.7].forEach((y, row) => { g.add(at(box(W, 0.03, D, '#A9B0B8', { outline: 0.004 }), 0, y, 0));
      for (let i = 0; i < n; i++) { const bx = -W / 2 + (i + 0.5) * W / n, k = (i * 3 + row * 2) % cols.length;
        g.add(at(box(0.2, 0.27, 0.05, '#E8F2F4', { opacity: 0.55 }), bx, y + 0.15, 0.05), at(box(0.2, 0.03, 0.055, '#C8202A'), bx, y + 0.28, 0.05));
        const pts = []; for (let j = 0; j < 8; j++) pts.push(new THREE.Vector3(bx + Math.sin(j * 1.3 + i) * 0.04, y + 0.06 + j * 0.022, 0.06 + 0.01 * Math.cos(j)));
        g.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 16, 0.009, 4), mat(cols[k])));
        g.add(at(canvasPlane(0.15, 0.05, (c, w, h) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, w, h); c.fillStyle = '#16171B'; c.font = `900 ${h * 0.7}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(String(100 + row * n + i + 1), w / 2, h * 0.56); }, { res: 96 }), bx, y + 0.07, 0.08)); } });
    void x; return g;
  },

  // The comparison screen (pivot at the bottom of its stand, facing +Z): a monitor o.w (0.8) wide showing two hair samples side by side (the
  // soup's black one, then a brown one) with a scan line sweeping them from o.scan, and at o.crossAt a big red cross pops over the screen
  chvScreen(o) {
    const W = o.w ?? 0.8, H = W * 0.62, g = grp(), Y = o.y ?? 0.32;
    g.add(at(box(0.18, 0.02, 0.14, '#2A2D33'), 0, 0.01, 0), at(box(0.04, Y, 0.04, '#2A2D33', { pivot: 'bottom' }), 0, 0, -0.02), at(box(W + 0.06, H + 0.06, 0.05, '#1E2026', { outline: 0.006 }), 0, Y + H / 2, 0));
    const scr = canvasPlane(W, H, (c, w, h) => { c.fillStyle = '#12202E'; c.fillRect(0, 0, w, h);
      for (const [i, col] of [[0, '#0E0E10'], [1, '#8A5A2E']]) { const x0 = w * (0.06 + i * 0.48); c.fillStyle = '#E8EEF2'; c.fillRect(x0, h * 0.12, w * 0.42, h * 0.76);
        c.strokeStyle = col; c.lineWidth = w * 0.022; c.lineCap = 'round'; c.beginPath(); for (let j = 0; j <= 30; j++) { const u = j / 30, x = x0 + w * 0.21 + Math.sin(u * (i ? 6 : 9)) * w * 0.07, y = h * 0.8 - u * h * 0.6; j ? c.lineTo(x, y) : c.moveTo(x, y); } c.stroke();
        c.fillStyle = '#12202E'; c.font = `900 ${h * 0.09}px Arial`; c.textAlign = 'center'; c.fillText(i ? 'N° 2' : 'N° 1', x0 + w * 0.21, h * 0.22); } }, { res: 512, emissive: 0.85 });
    scr.position.set(0, Y + H / 2, 0.027); g.add(scr);
    const scan = at(box(0.012, H * 0.8, 0.004, '#7FE0FF', { emissive: '#7FE0FF' }), 0, Y + H / 2, 0.031); g.add(scan);
    const X = grp(); const xm = new THREE.MeshBasicMaterial({ color: '#E8202A' }), xo = new THREE.MeshBasicMaterial({ color: '#FFFFFF' });
    for (const s of [-1, 1]) { const bar = new THREE.Mesh(new THREE.PlaneGeometry(W * 0.95, H * 0.14), xm); bar.rotation.z = s * Math.atan2(H * 0.8, W * 0.9); X.add(bar); const ol = new THREE.Mesh(new THREE.PlaneGeometry(W * 0.98, H * 0.19), xo); ol.rotation.z = bar.rotation.z; ol.position.z = -0.002; X.add(ol); }
    X.position.set(0, Y + H / 2, 0.04); g.add(X);
    g.userData.update = t => { const s0 = o.scan ?? 0, s1 = o.crossAt ?? 1, u = (t - s0) / Math.max(0.1, s1 - s0); scan.visible = u >= 0 && u < 1; if (scan.visible) scan.position.x = -W * 0.44 + W * 0.88 * ((u * 2) % 1);
      const v = t - s1; X.visible = v >= 0; if (v >= 0) { const k = outBack(v / 0.16); X.scale.setScalar(Math.max(0.01, k)); X.rotation.z = 0.04 * Math.sin(v * 30) * Math.exp(-6 * v); } };
    g.userData.update(0); return g;
  },

  // A small display stand for the hair (pivot at the floor, facing +Z): a white column o.h (1.12) high with gold bands, a round red velvet
  // cushion on top (its top at o.h + 0.06); o.panel: a pale oval card behind the hair for contrast (o.panelColor)
  chvStand(o) {
    const Hs = o.h ?? 1.12, g = grp(), W = o.color || '#F2EFE8';
    g.add(at(cyl(0.2, 0.23, 0.06, W, 14, { outline: 0.005 }), 0, 0.03, 0), at(cyl(0.1, 0.12, Hs - 0.1, W, 14, { outline: 0.005, pivot: 'bottom' }), 0, 0.06, 0), at(cyl(0.17, 0.14, 0.05, W, 14, { outline: 0.005 }), 0, Hs - 0.02, 0));
    for (const y of [0.12, Hs - 0.06]) g.add(at(cyl(0.125, 0.125, 0.02, '#D9AE3A', 14), 0, y, 0));
    const cu = new THREE.Mesh(new THREE.SphereGeometry(0.15, 16, 10), mat(o.cushion || '#B5202A')); cu.scale.set(1, 0.28, 1); cu.position.y = Hs + 0.02; g.add(cu);
    for (let i = 0; i < 4; i++) { const a = i * PI / 2 + PI / 4; g.add(at(sphere(0.022, '#D9AE3A', 1), Math.cos(a) * 0.15, Hs + 0.02, Math.sin(a) * 0.15)); }
    if (o.panel) { const p = new THREE.Mesh(new THREE.CircleGeometry(0.22, 24), mat(o.panelColor || '#F6F3EA')); p.scale.set(0.8, 1.15, 1); p.position.set(0, Hs + 0.25, -0.14); g.add(p); g.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.012, 4, 24), mat('#D9AE3A')), 0, Hs + 0.25, -0.138)); g.children[g.children.length - 1].scale.set(0.8, 1.15, 1); }
    g.userData.top = [0, Hs + 0.06, 0]; return g;
  },

  // A pool of light (pivot at its centre, lying flat): a soft warm disc o.r (0.45) on a surface, with a point light o.h (0.6) above it; o.on [[t, v]]
  chvPool(o) {
    const g = grp(), m = new THREE.Mesh(new THREE.CircleGeometry(o.r ?? 0.45, 28), softMat(o.color || '#FFF2C0', 0.9, true)); m.rotation.x = -PI / 2; m.position.y = 0.004; g.add(noShadow(m));
    const L = new THREE.PointLight(o.color || '#FFF2C0', o.power ?? 3, o.range ?? 2.5, 1.3); L.position.y = o.h ?? 0.6; g.add(L);
    g.userData.update = t => { const v = keyAt(o.on, t, 1, 0.12); m.material.opacity = 0.9 * v; m.visible = v > 0.01; L.intensity = (o.power ?? 3) * v; };
    g.userData.update(0); return g;
  },

  // A searchlight beam (pivot at the lamp; the beam runs down -Y, aim it by rot): an additive cone o.len (8) long, o.r (0.6) wide at its end,
  // with a brighter core; (round 1) drawn in the opaque pass behind every actor (see onTopActors): it never greys a face or a suit; o.on [[t, v]];
  // o.r0 (0.12): its width at the lamp; o.op (0.13): its strength; o.fade: what is left of it at the far end (0.6)
  chvBeam(o) {
    const Lb = o.len ?? 8, Rb = o.r ?? 0.6, g = grp(), ms = [];
    for (const [r, op] of [[Rb, o.op ?? 0.13], [Rb * 0.45, (o.op ?? 0.13) * 1.4]]) { const m = beamCone(Lb, o.r0 ?? 0.12, r, o.color || '#FFF6C8', op, o.fade ?? 0.6); m.userData.op = op; g.add(m); ms.push(m); }
    g.add(at(sphere(o.lampR ?? 0.09, '#FFF6C8', 1, { emissive: '#FFF0B0' }), 0, 0, 0));
    const fl = new THREE.Sprite(new THREE.SpriteMaterial({ map: softTex(), color: '#FFF4CC', transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0.9 })); fl.scale.setScalar(o.flare ?? 0.8); g.add(fl);
    g.userData.chvBeam = true;
    g.userData.update = t => { onTopActors(g); const v = keyAt(o.on, t, 1, 0.1); ms.forEach(m => { m.material.opacity = m.userData.op * v; m.visible = v > 0.01; }); fl.material.opacity = 0.9 * v; fl.visible = v > 0.01; };
    g.userData.update(0); return g;
  },
  // (round 1) A police helicopter seen at night (pivot at the middle of its cabin, the nose toward +Z), about 3.3 m long: a rounded navy cabin
  // (o.color) with a big pale-blue glazed nose, a tail boom tapering back to a fin, a stabiliser and a two-blade tail rotor, a mast with four
  // dark main blades (o.spin turns/s, slow enough to read at 15 frames a second) over a faint spinning disc, two skids on struts, a searchlight
  // under the nose (userData.lamp: its local point) and a red beacon on the fin blinking once a second. No writing, no insignia. o.rim: a pale
  // halo round the whole silhouette (a navy machine against the night sky), o.rimW its thickness (m)
  chvHeli(o) {
    const C = o.color || '#34569A', D = '#1A2232', G = o.glass || '#B4D6EE', g = grp(), parts = [];
    const lam = (c, e) => new THREE.MeshLambertMaterial({ color: c, emissive: e || '#000000' });
    const add = (geo, m, x, y, z, rx = 0, ry = 0, rz = 0, sx = 1, sy = 1, sz = 1) => { const ms = new THREE.Mesh(geo, m); ms.position.set(x, y, z); ms.rotation.set(rx, ry, rz); ms.scale.set(sx, sy, sz); ms.castShadow = false; g.add(ms); parts.push(ms); return ms; };
    const body = lam(C, o.emissive || '#1C3060'), dark = lam(D, '#0C1220');
    add(new THREE.SphereGeometry(1, 18, 12), body, 0, 0, 0, 0, 0, 0, 0.62, 0.6, 1.0);
    add(new THREE.SphereGeometry(1, 16, 10, 0, TAU, 0, PI * 0.5), lam(G, '#2A4458'), 0, 0.02, 0.32, PI / 2 + 0.25, 0, 0, 0.58, 0.72, 0.5);
    add(new THREE.BoxGeometry(1.0, 0.3, 0.9), body, 0, 0.42, -0.25, 0, 0, 0, 0.62, 1, 1);
    add(new THREE.CylinderGeometry(0.09, 0.2, 1.75, 10), body, 0, 0.12, -1.55, PI / 2, 0, 0);
    add(new THREE.BoxGeometry(0.06, 0.55, 0.32), body, 0, 0.36, -2.38, -0.25, 0, 0);
    add(new THREE.BoxGeometry(0.7, 0.04, 0.2), body, 0, 0.12, -2.25);
    add(new THREE.CylinderGeometry(0.06, 0.08, 0.22, 8), dark, 0, 0.66, -0.2);
    for (const s of [-1, 1]) { add(new THREE.BoxGeometry(0.05, 0.05, 1.5), dark, s * 0.42, -0.78, 0.05);
      for (const z of [-0.35, 0.45]) add(new THREE.BoxGeometry(0.035, 0.3, 0.035), dark, s * 0.34, -0.63, z, 0, 0, s * 0.45); }
    const lampP = [0, -0.5, 0.62]; add(new THREE.CylinderGeometry(0.09, 0.07, 0.12, 10), dark, lampP[0], lampP[1] + 0.05, lampP[2]);
    add(new THREE.SphereGeometry(0.075, 10, 8), new THREE.MeshBasicMaterial({ color: '#FFF8DC' }), ...lampP);
    const rotor = grp(); rotor.position.set(0, 0.79, -0.2); g.add(rotor);
    for (let i = 0; i < 4; i++) { const b = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.025, 1.75), dark); b.position.z = 0.875; const arm = grp(b); arm.rotation.y = i * PI / 2; rotor.add(arm); }
    const disc = new THREE.Mesh(new THREE.CircleGeometry(1.75, 32), new THREE.MeshBasicMaterial({ color: '#C8D2E0', transparent: true, opacity: o.discOpacity ?? 0.16, side: THREE.DoubleSide, depthWrite: false })); disc.rotation.x = -PI / 2; disc.position.set(0, 0.8, -0.2); g.add(disc);
    const tr = grp(); tr.position.set(0.06, 0.4, -2.42); g.add(tr);
    for (let i = 0; i < 2; i++) { const b = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.5, 0.06), dark); b.rotation.x = i * PI / 2; tr.add(b); }
    const bm = new THREE.MeshBasicMaterial({ color: '#FF2A2A' }), beacon = new THREE.Mesh(new THREE.SphereGeometry(0.05, 8, 6), bm); beacon.position.set(0, 0.66, -2.45); g.add(beacon);
    if (o.rim) { const rm = new THREE.MeshBasicMaterial({ color: o.rim, side: THREE.BackSide }), w = o.rimW ?? 0.04;
      for (const ms of [...parts]) { if (ms.material.isMeshBasicMaterial) continue; const h = new THREE.Mesh(ms.geometry, rm); h.position.copy(ms.position); h.rotation.copy(ms.rotation);
        ms.geometry.computeBoundingBox(); const bb = ms.geometry.boundingBox, sz = new THREE.Vector3(); bb.getSize(sz);
        h.scale.set(ms.scale.x * (1 + 2 * w / Math.max(0.02, sz.x * ms.scale.x)), ms.scale.y * (1 + 2 * w / Math.max(0.02, sz.y * ms.scale.y)), ms.scale.z * (1 + 2 * w / Math.max(0.02, sz.z * ms.scale.z))); g.add(h); }
      for (const arm of rotor.children) { const b = arm.children[0], h = new THREE.Mesh(b.geometry, rm); h.position.copy(b.position); h.scale.set(1 + 2 * w / 0.13, 1 + 2 * w / 0.025, 1 + 2 * w / 1.75); arm.add(h); } }
    g.userData.lamp = lampP; g.userData.chvUnder = true;
    g.userData.update = t => { rotor.rotation.y = (o.spin ?? 1.15) * TAU * t; tr.rotation.x = 5 * TAU * t; beacon.visible = (t % 1) < 0.18;
      const sw = o.sway ?? 0.04; g.rotation.z = sw * Math.sin(t * 1.9); g.position.y = 0.05 * Math.sin(t * 2.3); };
    g.userData.update(0); return g;
  },

  // (round 1) A short fat police torch (pivot at the grip; the light shines down -Y: aim it like a beam): a cream body with black rubber rings,
  // a wider head and a glowing lens, a flare on the lens and a visible beam o.len (1.2) long and o.r (0.16) wide at its end, drawn behind people;
  // o.on [[t, v]]
  chvTorch(o) {
    const g = grp(), K = '#1E2026', B = o.color || '#EFE2B6';
    g.add(at(cyl(0.048, 0.048, 0.2, B, 10, { outline: 0.006 }), 0, 0.03, 0), at(cyl(0.052, 0.052, 0.025, K, 10), 0, 0.09, 0), at(cyl(0.052, 0.052, 0.025, K, 10), 0, -0.02, 0));
    g.add(at(cyl(0.05, 0.078, 0.07, B, 12, { outline: 0.006 }), 0, -0.105, 0), at(cyl(0.08, 0.08, 0.02, K, 12), 0, -0.15, 0));
    const lens = new THREE.Mesh(new THREE.CircleGeometry(0.068, 16), new THREE.MeshBasicMaterial({ color: '#FFFBE6' })); lens.rotation.x = PI / 2; lens.position.y = -0.162; g.add(lens);
    const cone = beamCone(o.len ?? 1.2, 0.06, o.r ?? 0.16, '#FFF4C8', o.op ?? 0.22, 0.7, 20); cone.position.y = -0.165; g.add(cone);
    const core = beamCone(o.len ?? 1.2, 0.04, (o.r ?? 0.16) * 0.45, '#FFFBE6', (o.op ?? 0.22) * 1.2, 0.8, 16); core.position.y = -0.165; g.add(core);
    const fl = new THREE.Sprite(new THREE.SpriteMaterial({ map: softTex(), color: '#FFF4CC', transparent: true, depthWrite: false, blending: THREE.AdditiveBlending })); fl.position.y = -0.18; fl.scale.setScalar(0.32); g.add(fl);
    g.userData.update = t => { onTopActors(g); const v = keyAt(o.on, t, 1, 0.08); for (const m of [cone, core]) { m.visible = v > 0.01; } cone.material.opacity = (o.op ?? 0.22) * v; core.material.opacity = (o.op ?? 0.22) * 1.2 * v; fl.material.opacity = v; };
    g.userData.update(0); return g;
  },

  // (round 1) A tall pleated chef's toque (pivot at the bottom of its band): a white band, a pleated column widening upward (o.h 0.34 high),
  // a puffed crown; o.s scales it. Attach it to the head (offset about [0, 0.5, 0]) or to a hand; (final pass) o.wob [[t, rad], ...]: it wobbles
  chvToque(o) {
    const S = o.s ?? 1, g = grp(), b = grp(); b.scale.setScalar(S); g.add(b); const W = '#FAFAF6', Hc = o.h ?? 0.34;
    if (o.wob) g.userData.update = t => { let a = 0; for (const [t0, amp] of o.wob) { const u = t - t0; if (u >= 0) a += amp * Math.exp(-5 * u) * Math.sin(u * 24); } b.rotation.z = a; b.rotation.x = 0.5 * a; };
    b.add(at(cyl(0.165, 0.165, 0.08, '#F0F0EA', 16, { outline: 0.008, pivot: 'bottom' }), 0, 0, 0), at(cyl(0.2, 0.17, Hc, W, 16, { outline: 0.008, pivot: 'bottom' }), 0, 0.08, 0));
    for (let i = 0; i < 12; i++) { const a = i / 12 * TAU; b.add(at(box(0.012, Hc * 0.96, 0.02, '#DADAD2'), Math.sin(a) * 0.18, 0.08 + Hc / 2, Math.cos(a) * 0.18, 0.11 * Math.cos(a), a, -0.11 * Math.sin(a) * 0)); }
    const cr = new THREE.Mesh(new THREE.SphereGeometry(0.24, 16, 10), mat(W)); cr.scale.set(1, 0.5, 1); cr.position.y = 0.08 + Hc + 0.02; b.add(cr);
    for (let i = 0; i < 6; i++) { const a = i / 6 * TAU + 0.3, m = new THREE.Mesh(new THREE.SphereGeometry(0.1, 10, 8), mat(W)); m.position.set(Math.sin(a) * 0.15, 0.08 + Hc + 0.06, Math.cos(a) * 0.15); b.add(m); }
    return g;
  },

  // (round 1) The front of a double-breasted chef's jacket (attach to the torso joint, offset [0, 0, 0]): a white wrap panel over the chest (it
  // hides a tie and the lapel V) with the overlap's seam, two rows of three round buttons, a stand-up collar round the neck; o.w (0.36)
  // the panel's width, o.z (0.18) the front of the chest, o.buttons ('#2A2A30')
  chvChefFront(o) {
    const g = grp(), W = o.w ?? 0.36, Z = o.z ?? 0.18, Hp = o.h ?? 0.5, y0 = o.y0 ?? 0.12, Wc = '#F6F6F2', K = o.buttons || '#2A2A30';
    g.add(at(box(W, Hp, 0.014, Wc, { outline: 0.004 }), 0, y0 + Hp / 2, Z + 0.007));
    g.add(at(box(0.008, Hp * 0.92, 0.006, '#C9C9C2'), W * 0.16, y0 + Hp * 0.48, Z + 0.016));
    for (const x of [-1, 1]) for (let i = 0; i < 3; i++) g.add(at(sphere(0.019, K, 1), x * W * 0.24, y0 + Hp * (0.24 + i * 0.25), Z + 0.02));
    g.add(at(cyl(0.11, 0.115, 0.07, Wc, 12, { outline: 0.004 }), 0, y0 + Hp + 0.02, 0.0));
    return g;
  },

  // (round 1) A plain dark wall panel (pivot at its bottom centre, facing +Z): o.w x o.h, o.color, a thin frame (o.frame) and a faint diagonal
  // sheen (a one-way mirror) so it reads as glass, not a hole
  chvPanel(o) {
    const W = o.w ?? 2, H = o.h ?? 1.2, g = grp();
    g.add(at(box(W + 0.1, H + 0.1, 0.05, o.frame || '#2A2E34', { outline: 0.004 }), 0, H / 2, 0), at(box(W, H, 0.06, o.color || '#141A20'), 0, H / 2, 0.005));
    if (o.sheen !== false) for (const [x, w] of [[-0.15, 0.18], [0.12, 0.07]]) g.add(at(box(w * W, H * 1.05, 0.002, '#3A4654'), x * W, H / 2, 0.037, 0, 0, 0.5));
    return g;
  },

  // (round 2) The SHAVED police dog (pivot at the floor between its feet, front +Z), built so it cannot read as a pig: a slim body on long legs,
  // a narrow head with a long muzzle and a black nose at its tip, tall upright pointed ears, a long thin tail held up, a blue collar with a
  // round gold badge (plain, no writing, no insignia); skin o.color (pale greyish pink), o.muzzle; o.proud [[t, v]]: chin up, chest out (0..1);
  // o.wag: tail beats per second (side to side); o.tongue: a pink tongue out; o.eyes: eye size
  chvDogShaved(o) {
    const C = o.color || '#E6C2C2', M = o.muzzle || '#D8A9AE', K = '#141416', g = grp(), body = grp(); g.add(body);
    body.add(at(box(0.25, 0.24, 0.66, C, { outline: 0.01 }), 0, 0.56, 0));
    body.add(at(box(0.27, 0.27, 0.22, C, { outline: 0.01 }), 0, 0.6, 0.2));
    for (const [x, z] of [[-0.085, 0.24], [0.085, 0.24], [-0.085, -0.25], [0.085, -0.25]]) body.add(at(box(0.075, 0.46, 0.08, C, { outline: 0.008, pivot: 'bottom' }), x, 0.0, z), at(box(0.08, 0.04, 0.1, M), x, 0.02, z + 0.01));
    const neck = at(box(0.15, 0.3, 0.15, C, { outline: 0.008 }), 0, 0.8, 0.31, 0.45, 0, 0); body.add(neck);
    const col = at(box(0.19, 0.06, 0.19, '#2F5D8A', { outline: 0.006 }), 0, 0.76, 0.3, 0.45, 0, 0); body.add(col);
    const badge = grp(at(cyl(0.05, 0.05, 0.015, '#E2B53C', 14, { outline: 0.005 }), 0, 0, 0, PI / 2, 0, 0), at(cyl(0.03, 0.03, 0.018, '#C9952A', 12), 0, 0, 0.002, PI / 2, 0, 0)); badge.position.set(0, 0.69, 0.41); body.add(badge);
    const head = grp(); head.position.set(0, 0.96, 0.4); body.add(head);
    head.add(at(box(0.2, 0.2, 0.22, C, { outline: 0.01 }), 0, 0, 0));
    head.add(at(box(0.13, 0.11, 0.24, M, { outline: 0.008 }), 0, -0.05, 0.21), at(box(0.07, 0.05, 0.04, K), 0, -0.02, 0.34));
    const es = o.eyes ?? 1;
    for (const sx of [-1, 1]) { head.add(at(box(0.065 * es, 0.065 * es, 0.02, '#FFFFFF'), sx * 0.06, 0.04, 0.112), at(box(0.03 * es, 0.035 * es, 0.02, K), sx * 0.055, 0.04, 0.122));
      const e = new THREE.Mesh(new THREE.ConeGeometry(0.055, 0.24, 4), mat(C)); e.position.set(sx * 0.068, 0.2, -0.04); e.rotation.set(-0.08, PI / 4, -sx * 0.12); head.add(e);
      const ei = new THREE.Mesh(new THREE.ConeGeometry(0.03, 0.15, 4), mat(o.ear || '#C98E96')); ei.position.set(sx * 0.068, 0.18, -0.005); ei.rotation.set(-0.08, PI / 4, -sx * 0.12); head.add(ei); }
    if (o.tongue) head.add(at(box(0.06, 0.1, 0.025, '#E86A84', { outline: 0.005 }), 0.025, -0.14, 0.26, 0.15, 0, 0.1));
    const tail = grp(); tail.position.set(0, 0.66, -0.32); body.add(tail); tail.add(at(box(0.045, 0.34, 0.045, C, { outline: 0.008, pivot: 'bottom' }), 0, 0, 0, -0.55, 0, 0));
    g.userData.update = t => { const pr = keyAt(o.proud, t, 0, 0.18); head.rotation.x = -0.35 * pr; head.position.y = 0.96 + 0.04 * pr; body.position.y = 0.0; neck.rotation.x = 0.45 - 0.25 * pr;
      tail.rotation.z = 0.55 * Math.sin(t * TAU * (o.wag ?? 3)); tail.rotation.x = -0.15 * pr; };
    g.userData.head = head; g.userData.update(0); return g;
  },

  // (round 1) A dog built on the voxel dog with a longer muzzle and pointed ears (so it reads as a dog, not a pig), a wagging tail and two
  // behaviours: o.sniff [[t0, t1], ...]: nose to the ground and up in quick sniffs; o.proud [[t, v]]: the chest out and the head up (v 0..1);
  // o.wag (2.5): tail beats per second; other options go to the voxel dog (color, muzzle, tongue, eyes, walk)
  chvDog(o) {
    const g = grp(), d = buildProp('voxelDog', o), head = d.userData.head, base = d.userData.update, inner = d.children[0]; d.userData = {}; g.add(d);
    const hk = head.children;
    if (hk[1]) { hk[1].scale.z = 1.9; hk[1].position.z += 0.11; hk[1].position.y += 0.01; }
    if (hk[2]) hk[2].position.z += 0.21;
    for (let i = 3; i < hk.length; i++) { const c = hk[i]; if (i >= 9) c.position.z += 0.2; }
    for (const i of [7, 8]) if (hk[i]) hk[i].visible = false;
    const earC = o.ear || new THREE.Color(o.color || '#D9A15A').multiplyScalar(0.78).getStyle();
    for (const s of [-1, 1]) { const e = new THREE.Mesh(new THREE.ConeGeometry(0.065, 0.2, 4), mat(earC)); e.position.set(s * 0.12, 0.24, -0.04); e.rotation.set(-0.1, PI / 4, s * -0.28); head.add(e); }
    let tail = null; const tl = inner.children[5];
    if (tl) { inner.remove(tl); tail = grp(); tail.position.set(0, 0.54, -0.26); tl.position.set(0, 0.11, -0.05); tail.add(tl); inner.add(tail); }
    const H0 = head.position.clone(), R0 = head.rotation.x;
    g.userData.update = t => { if (base) base(o.walkUntil == null ? t : (t < o.walkUntil ? t * (o.scrabble ?? 1) : Math.round(o.walkUntil * (o.scrabble ?? 1) * 4.4) / 4.4));   // (final pass) o.walkUntil: the legs scrabble (o.scrabble times faster) then stop straight
      const pr = keyAt(o.proud, t, 0, 0.18), sn = inWin(o.sniff, t);
      head.rotation.x = (base ? head.rotation.x : R0) + (sn ? 0.42 + 0.16 * Math.sin(t * 19) : 0) - 0.3 * pr;
      head.position.y = (base ? head.position.y : H0.y) - (sn ? 0.08 : 0) + 0.05 * pr; head.position.z = H0.z + 0.03 * pr;
      inner.scale.set(1, 1 + 0.07 * pr, 1); inner.position.y = 0.0;
      if (tail) tail.rotation.z = 0.6 * Math.sin(t * TAU * (o.wag ?? 2.5));
    };
    g.userData.head = head; g.userData.update(0); return g;
  },
};
