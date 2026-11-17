// « Le cheveu » (story 88): this man found a hair in his soup; a police helicopter lit the soup; the hair was arrested with tweezers,
// photographed from the front then in profile, questioned twelve hours under the lamp; it curled, which was held against it; the dogs followed
// its trail to the cook; they broke down his door, and every door in the street; the cook was bald, he was shaved anyway, then the customers and
// the passers-by for comparison, the police dog too, this man twice; under the microscope no match; the minister apologised to the hair; it was
// the last hair in the neighbourhood; the helicopter put it back, in this man's soup.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere, mat } from './style.js';
import { grp, at, canvasPlane, rod } from './props.js';

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
  // strand (dark backgrounds); o.sweat [t, ...]: a drop that runs down beside the eyes; o.hop [[t, h]]: a little jump (it straightens up)
  chvHair(o) {
    const L = o.L ?? 0.3, R = o.r ?? 0.009, g = grp(), body = grp(); g.add(body);
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
    let drop = null; if (o.sweat) { drop = new THREE.Mesh(new THREE.SphereGeometry(0.008, 8, 6), new THREE.MeshBasicMaterial({ color: '#9FD6F2' })); drop.scale.set(0.8, 1.3, 0.6); body.add(drop); }
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
      body.position.y = hop * 0.12;
      setTube(tube, pts, R, 60); capA.position.copy(pts[0]); capB.position.copy(pts[N - 1]);
      if (rimM) setTube(rimM, pts, R * 1.7, 60);
      const gp = pts.map(p => p.clone().add(new THREE.Vector3(-R * 0.35, R * 0.45, R * 0.55))); setTube(gl, gp, R * 0.22, 60);
      body.rotation.y = keyAt(o.yaw, t, 0, o.yawDur ?? 0.15) * PI / 180;
      const top = pts[N - 1];
      if (ey) {
        const on = keyAt(o.eyesOn, t, 1, 0.08) * (o.eyesFloat ? 1 : smooth((s - 0.5) / 0.4));
        ey.g.visible = on > 0.02; ey.g.scale.setScalar(Math.max(0.01, on));
        ey.g.position.set(top.x, top.y + 0.004, top.z + R * 1.2);
        const gz = (o.gaze || []).filter(k => t >= k[0]).pop() || [0, 0, 0];
        let lid = 0; for (const b of o.blinks || []) { const u = t - b; if (u >= 0 && u < 0.12) lid = Math.max(lid, 1 - Math.abs(u - 0.06) / 0.06); }
        ey.set(gz[1], gz[2], lid, keyAt(o.brow, t, 0, 0.1));
      }
      if (board) {
        const k = Math.round((o.boardU ?? 0.55) * (N - 1)), p = pts[k];
        board.position.set(p.x, p.y - 0.075, p.z + R + 0.004); board.rotation.y = keyAt(o.boardYaw, t, 0, o.yawDur ?? 0.15) * PI / 180;
      }
      if (drop) { let u = -1; for (const d of o.sweat) if (t >= d && t < d + 0.6) u = (t - d) / 0.6; drop.visible = u >= 0; if (u >= 0) drop.position.set(top.x + 0.03, top.y - 0.005 - u * 0.09, top.z + 0.012); }
    };
    g.userData.update(0); return g;
  },

  // A big soup bowl on a table (pivot at its foot): white with a blue rim, pale golden soup (o.soup) at 0.088, a spoon resting on the rim at the
  // right; o.steam: three soft wisps; o.ripple [t, ...]: a ring spreading on the soup (something lands); o.lit [[t, v]]: the soup brightens
  // (the searchlight); o.r (0.2)
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
    const wisps = []; if (o.steam) for (let i = 0; i < 3; i++) { const m = new THREE.Mesh(new THREE.PlaneGeometry(0.12, 0.12), softMat('#FFFFFF', 0.45)); m.userData.ph = i / 3; g.add(m); wisps.push(m); }
    const ring = new THREE.Mesh(new THREE.TorusGeometry(1, 0.06, 4, 28), new THREE.MeshBasicMaterial({ color: '#FFF6D8', transparent: true, opacity: 0.8 })); ring.rotation.x = PI / 2; ring.position.y = H * 0.82 + 0.003; g.add(ring);
    g.userData.surface = H * 0.82;
    g.userData.update = t => {
      sm.emissiveIntensity = 0.55 * keyAt(o.lit, t, 0, 0.15);
      wisps.forEach((m, i) => { const u = (t * 0.45 + m.userData.ph) % 1; m.position.set(Math.sin(u * 6 + i) * 0.03 + (i - 1) * 0.05, H + 0.05 + u * 0.35, 0); m.scale.setScalar(0.6 + u * 1.2); m.material.opacity = 0.4 * Math.sin(u * PI); });
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
    return g;
  },

  // Giant evidence tweezers (pivot at the hinge, the tips 0.5 m down -Y): two steel blades opened by o.open [[t, rad]] (0.18), rubber grips; with
  // o.hairAt a hair (o.hairL 0.28) hangs from the tips from then on, swinging (o.swing), with eyes (o.eyes, o.blinks)
  chvTweezers(o) {
    const Lt = o.len ?? 0.5, g = grp(), bl = [];
    for (const s of [-1, 1]) { const b = grp(at(box(0.045, Lt, 0.014, '#9AA4B0', { outline: 0.006, pivot: 'top' }), 0, 0, 0), at(box(0.046, 0.14, 0.018, '#2E3440', { outline: 0.003 }), 0, -Lt * 0.42, 0),
      at(box(0.03, 0.05, 0.012, '#B9C0C8', { outline: 0.003 }), -s * 0.012, -Lt + 0.01, 0, 0, 0, s * 0.35)); g.add(b); bl.push([b, s]); }
    g.add(at(box(0.06, 0.04, 0.03, '#9AA2AC', { outline: 0.004 }), 0, 0.01, 0));
    const hr = grp(); g.add(hr); const hm = new THREE.MeshLambertMaterial({ color: HAIR }), tb = new THREE.Mesh(new THREE.BufferGeometry(), hm); hr.add(tb);
    const ey = o.eyes ? eyePair(o.eyeS ?? 1, true) : null; if (ey) hr.add(ey.g);
    const HL = o.hairL ?? 0.28, pts = Array.from({ length: 30 }, () => new THREE.Vector3());
    g.userData.tips = [0, -Lt, 0];
    g.userData.update = t => {
      const op = keyAt(o.open, t, 0.18, 0.08); bl.forEach(([b, s]) => { b.rotation.z = s * op / 2; });
      hr.visible = o.hairAt != null && t >= o.hairAt; if (!hr.visible) return;
      const u0 = t - o.hairAt, sw = (o.swing ?? 0.6) * Math.exp(-2.2 * u0) * Math.sin(u0 * 9);
      pts.forEach((p, i) => { const u = i / 29; p.set(Math.sin(sw) * u * HL + 0.012 * Math.sin(u * 9 + t * 3) * u, -Lt + 0.01 - Math.cos(sw) * u * HL, 0.01 * Math.sin(u * 6 + t * 2)); });
      setTube(tb, pts, o.r ?? 0.009, 40);
      if (ey) { const q = pts[29]; ey.g.position.set(q.x, q.y + 0.03, q.z + 0.014); ey.g.rotation.z = sw; let lid = 0; for (const b of o.blinks || []) { const u = t - b; if (u >= 0 && u < 0.12) lid = 1 - Math.abs(u - 0.06) / 0.06; }
        ey.set(0, 0, lid, keyAt(o.brow, t, -0.6, 0.1)); }
    };
    g.userData.update(0); return g;
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
    const BL = o.beamLen ?? 0.9, cm = new THREE.MeshBasicMaterial({ color: '#FFE7A8', transparent: true, opacity: 0.16, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending });
    const cone = new THREE.Mesh(new THREE.CylinderGeometry(0.19, 0.5, BL, 20, 1, true), cm); cone.position.y = -0.2 - BL / 2; head.add(noShadow(cone));
    const halo = new THREE.Mesh(new THREE.PlaneGeometry(0.7, 0.7), softMat('#FFE2A0', 0.6, true)); halo.position.y = -0.2; halo.rotation.x = PI / 2; head.add(noShadow(halo));
    const L = new THREE.PointLight('#FFD9A0', o.power ?? 4, o.range ?? 3.5, 1.2); L.position.y = -0.3; head.add(L);
    g.userData.update = t => { const h = keyAt(o.heat, t, 0, 0.3), fl = 1 + 0.06 * h * Math.sin(t * 23);
      bm.color.setRGB(1, 0.96 - 0.35 * h, 0.82 - 0.65 * h); cm.color.setRGB(1, 0.9 - 0.3 * h, 0.66 - 0.5 * h); cm.opacity = (0.16 + 0.1 * h) * fl; sm.emissiveIntensity = 0.5 * h;
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
    g.userData.update = t => { const u = o.stampAt == null ? 1 : t - o.stampAt; st.visible = u >= 0; if (u >= 0) st.scale.setScalar(u < 0.1 ? 1.25 - 0.25 * (u / 0.1) : 1); };
    g.userData.update(0); return g;
  },

  // A battering ram (pivot at its middle, the striking end toward +Z): a dark steel cylinder o.len (1.1) long with a flat head, two yellow
  // carrying handles on top (userData.grips: local points for the hands, left and right)
  chvRam(o) {
    const L = o.len ?? 1.1, g = grp(), R = o.r ?? 0.09, C = o.color || '#2B2F36';
    g.add(at(cyl(R, R, L, C, 12, { outline: 0.006 }), 0, 0, 0, PI / 2, 0, 0), at(box(R * 2.6, R * 2.6, 0.06, '#1A1C20', { outline: 0.006 }), 0, 0, L / 2 + 0.03), at(cyl(R * 1.1, R * 1.1, 0.05, '#1A1C20', 12), 0, 0, -L / 2, PI / 2, 0, 0));
    for (const z of [-0.28, 0.22]) { g.add(at(box(0.03, 0.12, 0.03, '#E8B931', { outline: 0.004 }), 0, R + 0.06, z - 0.08), at(box(0.03, 0.12, 0.03, '#E8B931', { outline: 0.004 }), 0, R + 0.06, z + 0.08), at(box(0.035, 0.035, 0.2, '#E8B931', { outline: 0.004 }), 0, R + 0.12, z)); }
    for (const z of [-0.45, 0.45]) g.add(at(cyl(R * 1.08, R * 1.08, 0.04, '#E8B931', 12), 0, 0, z, PI / 2, 0, 0));
    g.userData.grips = [[0, R + 0.12, -0.28], [0, R + 0.12, 0.22]]; return g;
  },

  // A wall with a front door that falls flat (pivot at the floor under the doorway's middle; the wall in the XY plane): wall o.w (3) x o.h (3), a
  // doorway o.dw (1.0) x o.dh (2.15); the leaf (o.door colour, panels, a brass knob, a number plaque o.num) falls at o.fallAt toward o.dir (+1:
  // toward +Z, -1: toward -Z) about its bottom edge in o.fallDur (0.24 s), bounces, a puff of dust at the landing; o.facade: a townhouse front (o.h
  // 6, two windows, a cornice, o.color); o.dark: a dark room behind the doorway on the side the door falls to
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
    if (o.dark) g.add(at(box(dw + 0.2, dh + 0.1, 1.6, '#17181C'), 0, (dh + 0.1) / 2, dir * 0.9));
    const piv = grp(); piv.position.set(0, 0.0, dir * (T / 2)); g.add(piv);
    const leaf = grp(at(box(dw - 0.04, dh - 0.03, 0.06, o.door || '#2F5D8A', { outline: 0.008, pivot: 'bottom' }), 0, 0, 0)); piv.add(leaf);
    for (const [py, ph] of [[0.25, 0.75], [1.15, 0.75]]) for (const sx of [-1, 1]) leaf.add(at(box(dw * 0.36, ph, 0.02, '#244A70', { outline: 0.003 }), sx * dw * 0.22, py + ph / 2, -dir * 0.035));
    leaf.add(at(sphere(0.035, '#E2B53C', 1), dw * 0.36, dh * 0.47, -dir * 0.05));
    if (o.num) leaf.add(at(canvasPlane(0.16, 0.12, (c, w, h) => { c.fillStyle = '#F4F1E6'; c.fillRect(0, 0, w, h); c.fillStyle = '#1C1E24'; c.font = `900 ${h * 0.75}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(String(o.num), w / 2, h * 0.55); }, { res: 128 }), 0, dh * 0.82, -dir * 0.04, 0, dir > 0 ? PI : 0, 0));
    const puffs = []; for (let i = 0; i < 10; i++) { const m = new THREE.Mesh(new THREE.PlaneGeometry(0.4, 0.4), softMat('#D8CFC0', 0.7)); m.visible = false; m.userData.a = hsh(i) * TAU; g.add(noShadow(m)); puffs.push(m); }
    g.userData.update = t => {
      const u = o.fallAt == null ? -1 : t - o.fallAt, D = o.fallDur ?? 0.24;
      let a = 0; if (u >= 0) { if (u < D) a = (PI / 2) * (u / D) * (u / D); else { const v = u - D; a = PI / 2 - 0.12 * Math.exp(-9 * v) * Math.abs(Math.sin(v * 22)); } }
      piv.rotation.x = dir * Math.min(PI / 2, a);
      const pu = u - D; puffs.forEach((m, i) => { m.visible = pu >= 0 && pu < 0.9; if (!m.visible) return; const k = pu / 0.9, rx = (i / 9 - 0.5) * dw * 1.3; m.position.set(rx + Math.cos(m.userData.a) * k * 0.4, 0.12 + k * 0.5 * (0.5 + hsh(i + 3)), dir * (dh * (0.2 + 0.8 * hsh(i + 9)) + 0.1));
        m.scale.setScalar(0.6 + k * 1.8); m.material.opacity = 0.7 * (1 - k); m.lookAt(m.position.x, m.position.y, m.position.z + dir * 10); });
    };
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
  // o.bits [[t0, t1, colour], ...]: cut hair falls from the blade; o.s scales it
  chvClippers(o) {
    const S = o.s ?? 1, g = grp(), b = grp(); b.scale.setScalar(S); g.add(b);
    b.add(at(box(0.065, 0.17, 0.048, o.color || '#3A3F4A', { outline: 0.005, taper: { x: 0.85, z: 0.85 } }), 0, 0, 0), at(box(0.068, 0.04, 0.05, '#2A2E36', { outline: 0.004 }), 0, -0.07, 0));
    b.add(at(box(0.075, 0.025, 0.046, '#D2D8DE', { outline: 0.004 }), 0, 0.098, 0));
    for (let i = 0; i < 9; i++) b.add(at(box(0.005, 0.02, 0.02, '#16171B'), -0.034 + i * 0.0085, 0.118, 0.006));
    b.add(at(box(0.02, 0.03, 0.01, '#D23A2E', { outline: 0.002 }), 0, 0.02, 0.028), at(box(0.04, 0.005, 0.002, '#7E8696'), 0, -0.02, 0.025), at(box(0.04, 0.005, 0.002, '#7E8696'), 0, -0.035, 0.025));
    const cord = []; for (let i = 0; i < 14; i++) { const a = i * 1.4; cord.push(new THREE.Vector3(Math.cos(a) * 0.012, -0.09 - i * 0.008, Math.sin(a) * 0.012)); }
    b.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(cord), 40, 0.004, 4), mat('#1E2026')));
    const arcs = []; for (const s of [-1, 1]) for (let j = 0; j < 2; j++) { const a = new THREE.Mesh(new THREE.TorusGeometry(0.05 + j * 0.03, 0.004, 3, 10, 1.4), new THREE.MeshBasicMaterial({ color: o.arcColor || '#FFFFFF' })); a.rotation.z = s > 0 ? -0.7 : PI - 0.7; a.position.y = 0.06; b.add(a); arcs.push([a, s, j]); }
    const bits = []; for (let i = 0; i < 14; i++) { const m = new THREE.Mesh(new THREE.BoxGeometry(0.004, 0.03, 0.004), new THREE.MeshBasicMaterial({ color: '#2A2420' })); m.visible = false; g.add(m); bits.push(m); }
    g.userData.update = t => {
      const on = inWin(o.buzz, t);
      b.position.set(on ? 0.003 * Math.sin(t * 260) : 0, on ? 0.002 * Math.sin(t * 310) : 0, 0); b.rotation.z = on ? 0.03 * Math.sin(t * 190) : 0;
      arcs.forEach(([a, s, j]) => { a.visible = on && (Math.floor(t * 30) + j) % 2 === 0; });
      const win = (o.bits || []).find(w => t >= w[0] && t < w[1] + 0.8);
      bits.forEach((m, i) => { if (!win) { m.visible = false; return; } const t0 = win[0] + (i / 14) * (win[1] - win[0]), u = t - t0; m.visible = u >= 0 && u < 0.8; if (!m.visible) return;
        m.material.color.set(win[2] || '#2A2420'); m.position.set(((hsh(i) - 0.5) * 0.12) * S, (0.1 - 2.2 * u * u) * S, ((hsh(i + 5) - 0.5) * 0.08) * S); m.rotation.set(u * 9 + i, i, u * 7); m.scale.setScalar(S * 1.6); });
    };
    g.userData.update(0); return g;
  },

  // A pile of cut hair on the pavement with its evidence tag (pivot at the floor): a lumpy mound of o.color (and a few loose strands) that grows
  // with o.grow [[t, v]] (0..1, 1 = o.r 0.18 wide); the tag: a white card o.tagS (1) on a wire stake with a black number o.num and a red string,
  // facing +Z (turn the prop to the camera)
  chvHairPile(o) {
    const R = o.r ?? 0.18, C = o.color || '#3A2A20', g = grp(), pile = grp(); g.add(pile);
    for (let i = 0; i < 7; i++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 1), mat(C)); const a = i * 0.9, d = i ? R * 0.5 * hsh(i) : 0; m.position.set(Math.cos(a) * d, 0, Math.sin(a) * d); m.scale.set(R * (0.7 - 0.06 * i), R * (0.45 - 0.04 * i), R * (0.7 - 0.06 * i)); pile.add(m); }
    const dark = new THREE.Color(C).multiplyScalar(0.6).getStyle();
    for (let i = 0; i < 12; i++) { const a = hsh(i) * TAU, pts = []; for (let j = 0; j < 6; j++) pts.push(new THREE.Vector3(Math.cos(a) * R * (0.3 + j * 0.13), R * 0.35 - j * 0.05 + 0.05 * Math.sin(j * 2 + i), Math.sin(a) * R * (0.3 + j * 0.13) + 0.02 * Math.cos(j * 3)));
      pile.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 12, 0.006, 4), mat(i % 2 ? dark : C))); }
    const S = o.tagS ?? 1, tag = grp(); tag.position.set(R * 0.9, 0, R * 0.4); g.add(tag);
    tag.add(at(cyl(0.004, 0.004, 0.3 * S, '#8A8E92', 4, { pivot: 'bottom' }), 0, 0, 0));
    tag.add(at(canvasPlane(0.14 * S, 0.09 * S, (c, w, h) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, w, h); c.strokeStyle = '#C8202A'; c.lineWidth = h * 0.08; c.strokeRect(0, 0, w, h); c.fillStyle = '#16171B'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${h * 0.6}px Arial`; c.fillText(String(o.num ?? 1), w / 2, h * 0.56); }, { res: 128 }), 0, 0.3 * S + 0.045 * S, 0.004));
    tag.add(at(box(0.144 * S, 0.094 * S, 0.004, '#C8202A'), 0, 0.3 * S + 0.045 * S, 0));
    g.userData.update = t => { const v = keyAt(o.grow, t, 1, 0.3); pile.scale.set(Math.max(0.01, v), Math.max(0.01, v), Math.max(0.01, v)); pile.visible = v > 0.02; };
    g.userData.update(0); return g;
  },

  // A shine on a bald head (attach to the head joint, offset about [0, 0.5, 0.02] in the joint's units): a soft white highlight lying on the top
  // of the head, tilted toward the front, and a four-point glint that twinkles at o.twinkle [t, ...] (and o.tw0: always a faint one); o.s
  chvShine(o) {
    const S = o.s ?? 1, g = grp();
    const hl = new THREE.Mesh(new THREE.PlaneGeometry(0.16 * S, 0.08 * S), softMat('#FFFFFF', o.opacity ?? 0.85)); hl.rotation.x = -PI / 2 + (o.tilt ?? 0.5); hl.position.set(-0.03 * S, 0.004, 0.02 * S); g.add(noShadow(hl));
    const star = grp(); const sm = new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 1, depthWrite: false });
    for (let k = 0; k < 2; k++) { const r = new THREE.Mesh(new THREE.PlaneGeometry(0.012 * S, 0.12 * S), sm); r.rotation.z = k * PI / 2; star.add(r); }
    star.add(new THREE.Mesh(new THREE.PlaneGeometry(0.06 * S, 0.06 * S), softMat('#FFFFFF', 1))); star.position.set(0.04 * S, 0.03 * S, 0.06 * S); g.add(noShadow(star));
    g.userData.update = t => { let k = o.tw0 ?? 0.35; for (const t0 of o.twinkle || []) { const u = t - t0; if (u >= 0 && u < 0.3) k = Math.max(k, Math.sin(u / 0.3 * PI)); }
      star.scale.setScalar(Math.max(0.01, k)); star.rotation.z = t * 1.5; star.visible = k > 0.02; };
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

  // A searchlight beam (pivot at the lamp; the beam runs down -Y, aim it by rot): a soft additive cone o.len (8) long, o.r (0.6) wide at its end,
  // brighter at the core; o.on [[t, v]]
  chvBeam(o) {
    const Lb = o.len ?? 8, Rb = o.r ?? 0.6, g = grp(), ms = [];
    for (const [r, op] of [[Rb, 0.13], [Rb * 0.5, 0.16]]) { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.12, r, Lb, 24, 1, true), new THREE.MeshBasicMaterial({ color: o.color || '#FFF6C8', transparent: true, opacity: op, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending })); m.position.y = -Lb / 2; m.userData.op = op; g.add(noShadow(m)); ms.push(m); }
    g.add(at(sphere(o.lampR ?? 0.09, '#FFF6C8', 1, { emissive: '#FFF0B0' }), 0, 0, 0));
    g.userData.update = t => { const v = keyAt(o.on, t, 1, 0.1); ms.forEach(m => { m.material.opacity = m.userData.op * v; m.visible = v > 0.01; }); };
    g.userData.update(0); return g;
  },
};
