// « L'interrupteur » (story 40): a man turns his light off and the whole city goes out with it.
// Conventions as in props.js (metres, front +Z, pivot at the floor); every animated prop is a pure function of the shot time.
// Props meant for a shot in the dark (scene `dark`) use unlit materials, so that `inDark: true` shows them as they are.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, sphere, rng, ease, clamp01 } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const txt = (g, s, x, y, px, color = '#1B1B1E', weight = '900') => { g.fillStyle = color; g.font = `${weight} ${px}px Arial`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(s, x, y); };
const fit = (g, s, w, px, weight = '900') => { g.font = `${weight} ${px}px Arial`; const m = g.measureText(s).width; return m > w ? px * w / m : px; };
const wob = (t, f = 30, d = 6) => (t <= 0 ? 0 : Math.sin(t * f) * Math.exp(-t * d));
const keyed = (keys, t, e) => { if (!keys || !keys.length) return 0; if (t <= keys[0][0]) return keys[0][1]; for (let i = 0; i < keys.length - 1; i++) { const [t0, v0] = keys[i], [t1, v1] = keys[i + 1]; if (t < t1) { const u = clamp01((t - t0) / Math.max(1e-6, t1 - t0)); return v0 + (v1 - v0) * (e ? e(u) : u); } } return keys[keys.length - 1][1]; };
const flat = (color, o = {}) => new THREE.MeshBasicMaterial({ color, toneMapped: false, fog: false, ...o });   // a colour that owes nothing to the light of the set
const quad = (w, h, m) => { const q = new THREE.Mesh(new THREE.PlaneGeometry(w, h), m); q.castShadow = false; q.receiveShadow = false; return q; };
const solid = (w, h, d, m) => { const q = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m); q.castShadow = false; q.receiveShadow = false; return q; };
// the state of a thing that switches with the city: keys [[t, lit (0|1), spread (s)], ...]; a thing at distance d (0..1) follows each key `spread * d` later
const litAt = (keys, lit0, d, t, lag = 0) => { let s = lit0; for (const [t0, v, sp = 0.5] of keys) { if (t >= t0 + sp * d + (v ? 0 : lag)) s = v; else break; } return s; };

export const INTERRUPTEUR_PROPS = {
  // Paris at night from a height, as a painted depth of unlit shapes: a deep blue sky with stars and a moon, five rows of roofs that step back to a
  // skyline, lit windows, the tower above it all with its lights and its beam. Origin: the viewer's feet (a balcony); the city runs toward -Z. The nearest
  // roofs are o.drop (8 m) under his eyes and each row behind stands a little higher, so the skyline crosses the frame at about 40 % of its height for a
  // camera that looks level.
  // o.keys [[t, lit (0|1), spread], ...]: the city goes out (0) or comes back (1) as a wave that leaves the viewer and takes `spread` seconds to reach the far
  // rows; the tower follows the last row, o.towerLag (0.3 s) late when it goes out: it stands alone in the black, then pops. o.lit (1): the state at the start.
  // o.sparkle [t0, t1]: the tower glitters between these times (it does on the hour). o.eyes (40): pairs of eyes that open in the dark windows o.eyesLag
  // (0.45 s) after the black. o.moon false: no moon. o.towerX (16), o.towerH (52). Give it `inDark: true` in a shot that goes dark: it keeps its own lights
  cityNight(o) {
    const r = rng(o.seed || 23), drop = o.drop ?? 8, keys = (o.keys || []).slice().sort((a, b) => a[0] - b[0]), lit0 = o.lit ?? 1, g = grp(), eye = 2, y0 = -60;
    const sky = canvasPlane(420, 130, (c, W, H) => { const gr = c.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#040818'); gr.addColorStop(0.3, '#0A1438'); gr.addColorStop(0.52, '#1A2A66'); gr.addColorStop(1, '#1A2A66'); c.fillStyle = gr; c.fillRect(0, 0, W, H);
      const q = rng(5); for (let i = 0; i < 300; i++) { const x = q() * W, y = q() * H * 0.48, sz = 0.7 + q() * 1.5; c.fillStyle = `rgba(255, 250, 235, ${0.35 + 0.6 * q()})`; c.fillRect(x, y, sz, sz); } }, { res: 1024 });
    sky.material = flat('#FFFFFF', { map: sky.material.map }); sky.position.set(0, eye - 3, -165); sky.renderOrder = -5; g.add(sky);   // inside the sky dome of the set (radius 180)
    // the glow of the city on the horizon: it goes out with the windows
    const glow = canvasPlane(420, 44, (c, W, H) => { c.clearRect(0, 0, W, H); const gr = c.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, 'rgba(255, 180, 110, 0)'); gr.addColorStop(1, 'rgba(255, 180, 110, 0.42)'); c.fillStyle = gr; c.fillRect(0, 0, W, H); }, { res: 64, transparent: true });
    glow.material = flat('#FFFFFF', { map: glow.material.map, transparent: true, depthWrite: false, opacity: 0.8 }); glow.position.set(0, eye + 12, -164); g.add(glow);
    if (o.moon !== false) { const mx = o.moonX ?? -22, my = eye + (o.moonY ?? 36); g.add(at(new THREE.Mesh(new THREE.CircleGeometry(4.6, 28), flat('#F4EFD8')), mx, my, -163), at(new THREE.Mesh(new THREE.CircleGeometry(1.05, 14), flat('#DDD6B8')), mx - 1.4, my + 1.1, -162.8), at(new THREE.Mesh(new THREE.CircleGeometry(0.7, 12), flat('#DDD6B8')), mx + 1.3, my - 1.3, -162.8), at(new THREE.Mesh(new THREE.CircleGeometry(0.5, 10), flat('#DDD6B8')), mx - 0.4, my - 2.2, -162.8)); }
    g.add(at(solid(420, 0.5, 170, flat('#060914')), 0, y0, -80));
    // the rows: [z of the fronts, lowest and highest roof above the eye line minus drop, building widths, half the row's length, wall colours, floor height]
    const ROWS = [[-13, -3, 2, 5, 9, 14, ['#0A1124', '#0D152B'], 0], [-30, -1.5, 4, 6, 10, 20, ['#0F1934', '#121D3B'], 1], [-52, 1, 7, 7, 11, 28, ['#152244', '#18274C'], 2], [-80, 3.5, 10, 8, 12, 38, ['#1B2C58', '#1F3160'], 3], [-116, 6, 13, 8, 13, 50, ['#22376C', '#263C74'], 4]];
    const wins = [], eyes = [], dMax = 122, dim = [];   // dim: the walls and roofs, darker when the city is out (the glow of the windows is gone)
    for (const [z, lo, hi, w0, w1, half, cols, ri] of ROWS) {
      let x = -half - r() * 4;
      while (x < half) {
        const w = w0 + r() * (w1 - w0), top = eye - drop + lo + r() * (hi - lo), cx = x + w / 2, wall = cols[Math.floor(r() * cols.length)], dep = 10;
        const mw = flat(wall), mr = flat(new THREE.Color(wall).multiplyScalar(1.45).getStyle()); dim.push([mw, mw.color.clone()], [mr, mr.color.clone()]);
        g.add(at(solid(w, top - y0, dep, mw), cx, (top + y0) / 2, z - dep / 2), at(solid(w + 0.3, 1.2, dep + 0.3, mr), cx, top + 0.6, z - dep / 2));
        for (let i = 0; i < 2; i++) if (r() < 0.75) g.add(at(solid(0.7, 1.5, 0.7, flat('#3A2A2A')), cx + (r() - 0.5) * w * 0.7, top + 1.9, z - 1 - r() * 3));
        const cN = Math.max(2, Math.round(w / 2.3)), fN = ri === 0 ? 3 : 5;
        for (let f = 0; f < fN; f++) for (let cI = 0; cI < cN; cI++) {
          const wx = cx - w / 2 + (cI + 0.5) * w / cN, wy = top - 2.0 - f * 2.9, d = clamp01(Math.hypot(wx, z) / dMax), q = r();
          if (q < 0.56) wins.push({ x: wx, y: wy, z: z + 0.03, w: 0.95, h: 1.5, d, c: r() });
          else if (q < 0.8 && (ri === 1 || ri === 2) && f < 3) eyes.push({ x: wx, y: wy, z: z + 0.06, s: ri === 1 ? 0.26 : 0.38, d, ph: r() * 7, gz: (r() - 0.5) * 0.5 });
        }
        x += w + 0.2;
      }
    }
    const wm = new THREE.InstancedMesh(new THREE.PlaneGeometry(1, 1), flat('#FFFFFF'), wins.length), M = new THREE.Matrix4(), Z = new THREE.Matrix4().makeScale(0, 0, 0), col = new THREE.Color();
    wins.forEach((w, i) => { w.m = new THREE.Matrix4().makeScale(w.w, w.h, 1).setPosition(w.x, w.y, w.z); wm.setMatrixAt(i, w.m); wm.setColorAt(i, col.set(w.c < 0.6 ? '#FFD27A' : w.c < 0.85 ? '#FFB85A' : '#DCE9FF')); w.on = true; });
    wm.frustumCulled = false; wm.castShadow = false; g.add(wm);
    // the eyes in the dark windows: two pale dots a little apart, a blink now and then (the nearest eyes first)
    eyes.sort((a, b) => a.d - b.d);
    const nE = Math.min(o.eyes ?? 40, eyes.length), em = new THREE.InstancedMesh(new THREE.CircleGeometry(1, 10), flat('#F6F1E2'), Math.max(1, nE * 2)), pm = new THREE.InstancedMesh(new THREE.CircleGeometry(1, 8), flat('#0A0C14'), Math.max(1, nE * 2));
    em.frustumCulled = pm.frustumCulled = false; em.castShadow = pm.castShadow = false; em.count = pm.count = 0; g.add(em, pm);
    // the tower: a painted silhouette and two sets of light dots that take turns when it glitters; its beam turns
    const TH = o.towerH ?? 52, TW = TH * 0.42, tx = o.towerX ?? 16, tz = -150, ty = eye - drop - 4;
    const prof = v => 0.035 + 0.465 * Math.pow(1 - v, 2.1);   // half width (as a part of TW) at height v (0 = foot .. 1 = tip)
    const tower = canvasPlane(TW, TH, (c, W, H) => { c.clearRect(0, 0, W, H); c.fillStyle = '#31448A'; c.beginPath(); for (let i = 0; i <= 40; i++) { const v = i / 40; c.lineTo(W / 2 - prof(v) * W, H * (1 - v)); } for (let i = 40; i >= 0; i--) { const v = i / 40; c.lineTo(W / 2 + prof(v) * W, H * (1 - v)); } c.fill();
      c.globalCompositeOperation = 'destination-out'; c.beginPath(); c.ellipse(W / 2, H, W * 0.27, H * 0.19, 0, PI, TAU); c.fill();   // the arch between the feet
      c.lineWidth = W * 0.012; c.strokeStyle = 'rgba(0,0,0,0.5)'; for (let i = 2; i < 38; i += 2) { const v = i / 40, hw = prof(v) * W, y = H * (1 - v), y2 = H * (1 - v - 0.05); c.beginPath(); c.moveTo(W / 2 - hw, y); c.lineTo(W / 2 + prof(v + 0.05) * W, y2); c.moveTo(W / 2 + hw, y); c.lineTo(W / 2 - prof(v + 0.05) * W, y2); c.stroke(); }   // the lattice
      c.globalCompositeOperation = 'source-over'; c.fillStyle = '#3C509A'; [0.19, 0.4, 0.86].forEach(v => c.fillRect(W / 2 - prof(v) * W - W * 0.02, H * (1 - v) - H * 0.011, 2 * prof(v) * W + W * 0.04, H * 0.022)); }, { res: 512, transparent: true });
    tower.material = flat('#FFFFFF', { map: tower.material.map, transparent: true, alphaTest: 0.3 }); tower.position.set(tx, ty + TH / 2, tz); g.add(tower);
    const dots = kk => { const pl = canvasPlane(TW, TH, (c, W, H) => { c.clearRect(0, 0, W, H); const q = rng(40 + kk); for (let i = 0; i <= 50; i++) { const v = i / 50; for (const sd of [-1, 1]) { if (q() < 0.22) continue; c.fillStyle = q() < 0.5 ? '#FFF0BE' : '#FFD27A'; c.beginPath(); c.arc(W / 2 + sd * prof(v) * W, H * (1 - v), W * 0.013, 0, TAU); c.fill(); } }
      [0.19, 0.4, 0.86].forEach(v => { for (let x = -1; x <= 1.01; x += 0.2) { if (q() < 0.2) continue; c.fillStyle = '#FFF0BE'; c.beginPath(); c.arc(W / 2 + x * prof(v) * W, H * (1 - v), W * 0.013, 0, TAU); c.fill(); } }); }, { res: 512, transparent: true });
      pl.material = flat('#FFFFFF', { map: pl.material.map, transparent: true, depthWrite: false }); pl.position.set(tx, ty + TH / 2, tz + 0.2); g.add(pl); return pl; };
    const dA = dots(0), dB = dots(1), beam = quad(90, 1.8, flat('#FFF2C0', { transparent: true, opacity: 0.22, depthWrite: false, side: THREE.DoubleSide })), bp = grp(at(beam, 45, 0, 0)), tip = at(new THREE.Mesh(new THREE.CircleGeometry(1.0, 12), flat('#FFF6D8')), tx, ty + TH + 0.5, tz + 0.3);
    bp.position.set(tx, ty + TH, tz + 0.25); g.add(bp, tip);
    const eLag = o.eyesLag ?? 0.45, tLag = o.towerLag ?? 0.3;
    g.userData.update = t => {
      let any = false, nOn = 0;
      wins.forEach((w, i) => { const on = !!litAt(keys, lit0, w.d, t); if (on) nOn++; if (on !== w.on) { w.on = on; wm.setMatrixAt(i, on ? w.m : Z); any = true; } });
      if (any) wm.instanceMatrix.needsUpdate = true;
      const fr = nOn / Math.max(1, wins.length), dk = (o.offDim ?? 0.42) + (1 - (o.offDim ?? 0.42)) * fr; glow.material.opacity = 0.8 * fr; glow.visible = nOn > 0; for (const [m, c0] of dim) m.color.copy(c0).multiplyScalar(dk);
      const tw = !!litAt(keys, lit0, 1, t, tLag), sp = !!(o.sparkle && t >= o.sparkle[0] && t < o.sparkle[1]), fl = Math.floor(t * 14) % 2;
      dA.visible = tw && (!sp || fl === 0); dB.visible = tw && sp && fl === 1; beam.visible = tip.visible = tw; bp.rotation.y = t * 1.3; tower.material.color.setScalar(tw ? 1 : 0.5);
      // the eyes: once every window is out, they open one after the other, look about, blink
      let n = 0;
      if (nOn === 0 && nE) {
        let t0 = 0; for (const [tk, v, sp2 = 0.5] of keys) if (!v && t >= tk) t0 = tk + sp2;
        for (let i = 0; i < nE; i++) { const e = eyes[i], u = t - t0 - eLag - i * 0.014; if (u < 0) continue;
          const open = Math.min(1, u / 0.06), cyc = (t * 0.9 + e.ph) % 2.6, bl = cyc < 0.1 ? Math.abs(1 - cyc / 0.05) : 1, sy = Math.max(0.05, open * bl), lookX = e.gz + 0.35 * Math.sin(t * 1.1 + e.ph * 2);
          for (const sd of [-1, 1]) { M.makeScale(e.s, e.s * 1.25 * sy, 1).setPosition(e.x + sd * e.s * 1.25, e.y, e.z); em.setMatrixAt(n, M); M.makeScale(e.s * 0.42, e.s * 0.5 * sy, 1).setPosition(e.x + sd * e.s * 1.25 + lookX * e.s * 0.5, e.y, e.z + 0.02); pm.setMatrixAt(n, M); n++; } }
      }
      em.count = pm.count = n; if (n) { em.instanceMatrix.needsUpdate = true; pm.instanceMatrix.needsUpdate = true; }
    };
    g.userData.update(0); return g;
  },

  // a balcony to stand on above the city: a stone slab, an iron rail with upright bars, the wall of the flat behind with a lit French window.
  // Origin: the middle of the slab's top, the rail toward +Z when o.rail is 'front' (default: 'back', toward -Z: he faces us, the city behind him)
  balcony(o) {
    const w = o.w ?? 3.2, d = o.d ?? 1.3, back = (o.rail || 'back') === 'back', zr = back ? -d / 2 + 0.04 : d / 2 - 0.04, iron = '#20242C';
    const g = grp(at(box(w, 0.22, d, '#B9B2A4', { outline: 0.006 }), 0, -0.11, 0), at(box(w, 0.05, 0.06, iron), 0, 1.02, zr), at(box(w, 0.04, 0.05, iron), 0, 0.14, zr));
    for (let x = -w / 2 + 0.06; x <= w / 2 - 0.05; x += 0.16) g.add(at(box(0.025, 0.86, 0.025, iron), x, 0.58, zr));
    for (const sx of [-1, 1]) g.add(at(box(0.05, 1.04, 0.05, iron), sx * (w / 2 - 0.03), 0.52, zr), at(box(0.05, 0.05, d, iron), sx * (w / 2 - 0.03), 1.02, 0), at(box(0.04, 0.04, d, iron), sx * (w / 2 - 0.03), 0.14, 0));
    for (let z = -d / 2 + 0.2; z <= d / 2 - 0.1; z += 0.16) for (const sx of [-1, 1]) g.add(at(box(0.025, 0.86, 0.025, iron), sx * (w / 2 - 0.03), 0.58, z));
    return g;
  },

  // a rocker switch on its plate, three times its size so that it reads: o.flips [t, ...]: the rocker tips at each of these times (it starts on: o.on false
  // starts it off), and a little star of sparks marks the click. Origin: the middle of the plate, against the wall, front +Z
  rockerSwitch(o) {
    const s = o.s ?? 1, fl = (o.flips || []).slice().sort((a, b) => a - b), piv = grp(at(box(0.09 * s, 0.15 * s, 0.035 * s, o.rocker || '#FBFAF4', { outline: 0.012 }), 0, 0, 0.012 * s)); piv.position.z = 0.02 * s;
    const g = grp(at(box(0.2 * s, 0.28 * s, 0.02 * s, o.plate || '#EDEAE0', { outline: 0.014 }), 0, 0, 0.01 * s), piv), sparks = grp(); sparks.position.z = 0.06 * s; g.add(sparks);
    if (o.back) g.add(at(box(0.3 * s, 0.38 * s, 0.012 * s, o.back, { outline: 0.008 }), 0, 0, 0.002 * s));   // o.back: a darker panel behind the plate (a cream plate on a cream wall did not read); o.rocker / o.plate: their colours
    for (let i = 0; i < 6; i++) { const a = i * TAU / 6 + 0.3, q = quad(0.016 * s, 0.07 * s, flat('#FFE27A')); q.position.set(Math.sin(a) * 0.16 * s, Math.cos(a) * 0.16 * s, 0); q.rotation.z = -a; sparks.add(q); }
    g.userData.update = t => { let n = 0, last = -9; for (const f of fl) if (t >= f) { n++; last = f; }
      const on = ((o.on ?? true) ? 1 : 0) ^ (n % 2), u = t - last, k = u < 0.05 ? u / 0.05 : 1, a0 = on ? 0.3 : -0.3;
      piv.rotation.x = n ? -a0 + (a0 * 2) * k + 0.12 * wob(u - 0.05, 60, 14) * (on ? 1 : -1) : a0;
      sparks.visible = n > 0 && u < 0.14; if (sparks.visible) { const q = u / 0.14; sparks.scale.setScalar(0.6 + 1.1 * ease.out(q)); sparks.children.forEach(c => c.scale.y = 1 - q); } };
    g.userData.update(0); return g;
  },

  // an electrician's meter, big enough to read: a yellow box, a white dial with a red end, a needle. o.needle [[t, 0..1], ...] (it trembles past 0.85);
  // o.smokeAt: it starts to smoke. Origin: under the box, the dial toward +Z
  voltMeter(o) {
    const w = o.w ?? 0.5, h = w * 0.72, body = at(box(w, h, 0.16, '#F2C230', { outline: 0.012 }), 0, h / 2, 0), piv = grp(at(box(0.012, h * 0.52, 0.01, '#1B1B1E'), 0, h * 0.26, 0)); piv.position.set(0, h * 0.2, 0.09);
    const dial = canvasPlane(w * 0.84, h * 0.66, (c, W, H) => { c.fillStyle = '#FBFAF2'; c.fillRect(0, 0, W, H); c.lineWidth = H * 0.1; c.strokeStyle = '#2B2B30'; c.beginPath(); c.arc(W / 2, H * 0.98, H * 0.74, PI * 1.18, PI * 1.82); c.stroke();
      c.strokeStyle = '#D8322A'; c.beginPath(); c.arc(W / 2, H * 0.98, H * 0.74, PI * 1.66, PI * 1.82); c.stroke(); c.fillStyle = '#2B2B30'; for (let i = 0; i <= 8; i++) { const a = PI * (1.18 + 0.64 * i / 8); c.save(); c.translate(W / 2 + Math.cos(a) * H * 0.6, H * 0.98 + Math.sin(a) * H * 0.6); c.rotate(a + PI / 2); c.fillRect(-W * 0.006, -H * 0.05, W * 0.012, H * 0.1); c.restore(); }
      txt(c, 'V', W * 0.5, H * 0.2, H * 0.24, '#2B2B30'); }, { res: 384 });
    const g = grp(body, at(dial, 0, h * 0.56, 0.082), piv, at(sphere(0.022, '#1B1B1E', 1), 0, h * 0.2, 0.095), at(box(0.07, 0.035, 0.03, '#D8322A', { outline: 0.008 }), -w * 0.22, h * 0.09, 0.085), at(box(0.07, 0.035, 0.03, '#1B1B1E', { outline: 0.008 }), w * 0.22, h * 0.09, 0.085));
    const puffs = [0, 1, 2, 3].map(i => { const p = at(sphere(0.07, '#8E8E92', 1, { opacity: 0.8, unique: true }), 0, h, 0); p.castShadow = false; g.add(p); return p; });
    g.userData.update = t => { const v = keyed(o.needle, t, ease.out), tr = v > 0.85 ? 0.05 * Math.sin(t * 70) : 0; piv.rotation.z = (0.5 - v) * 1.15 * 2 * 0.5 + tr; body.rotation.z = v > 0.85 ? 0.012 * Math.sin(t * 83) : 0;
      puffs.forEach((p, i) => { const u = o.smokeAt == null ? -1 : ((t - o.smokeAt) * 1.3 + i * 0.25) % 1; p.visible = o.smokeAt != null && t >= o.smokeAt + i * 0.19; if (p.visible) { p.position.set(w * 0.2 * Math.sin(i * 2.1 + u * 3), h + u * 0.55, 0); p.scale.setScalar(0.6 + 1.5 * u); p.material.opacity = 0.8 * (1 - u); } }); };
    g.userData.update(0); return g;
  },

  // a jumper cable: from the origin to o.to [x, y, z] (in the prop's frame), hanging by o.sag (0.25 m), a crocodile clip at its far end. o.color
  jumperCable(o) {
    const to = new THREE.Vector3(...(o.to || [1, 0, 0])), mid = to.clone().multiplyScalar(0.5); mid.y -= o.sag ?? 0.25;
    const tube = new THREE.Mesh(new THREE.TubeGeometry(new THREE.QuadraticBezierCurve3(new THREE.Vector3(), mid, to), 14, o.r ?? 0.012, 5), mat(o.color || '#D8322A')); tube.castShadow = true;
    const clip = grp(at(box(0.035, 0.03, 0.1, o.color || '#D8322A', { outline: 0.006, taper: { x: 0.6 } }), 0, 0.016, 0.03), at(box(0.035, 0.03, 0.1, o.color || '#D8322A', { outline: 0.006, taper: { x: 0.6 } }), 0, -0.016, 0.03)); clip.position.copy(to); clip.lookAt(to.clone().add(to.clone().sub(mid)));
    return grp(tube, clip);
  },

  // the label of a fuse box, to slap on somebody: yellow, a black frame, a lightning triangle, o.text ('GÉNÉRAL'). Origin: its middle, front +Z
  fusePlate(o) {
    const w = o.w ?? 0.3, h = o.h ?? w * 0.5, s = o.text || 'GÉNÉRAL';
    const pl = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#F7CE2B'; c.fillRect(0, 0, W, H); c.strokeStyle = '#17171A'; c.lineWidth = H * 0.09; c.strokeRect(H * 0.045, H * 0.045, W - H * 0.09, H - H * 0.09);
      c.fillStyle = '#17171A'; c.beginPath(); c.moveTo(W * 0.14, H * 0.2); c.lineTo(W * 0.26, H * 0.2); c.lineTo(W * 0.19, H * 0.47); c.lineTo(W * 0.27, H * 0.47); c.lineTo(W * 0.13, H * 0.84); c.lineTo(W * 0.17, H * 0.56); c.lineTo(W * 0.09, H * 0.56); c.closePath(); c.fill();
      txt(c, s, W * 0.63, H * 0.54, fit(c, s, W * 0.62, H * 0.5), '#17171A'); }, { res: 384 });
    return grp(at(box(w, h, 0.008, '#17171A'), 0, 0, -0.005), pl);
  },

  // a public clock with lit figures: a dark case on the wall, amber digits. It shows o.from ('21:59') until o.at, then o.to ('22:00'), with a small jump of
  // the figures; the colon blinks. Unlit materials: it reads in a night set. Origin: its middle, front +Z
  ledClock(o) {
    const w = o.w ?? 1.0, h = w * 0.42, a0 = o.from || '21:59', a1 = o.to || '22:00';
    const face = s => { const pl = canvasPlane(w * 0.9, h * 0.72, (c, W, H) => { c.fillStyle = '#0D0E12'; c.fillRect(0, 0, W, H); txt(c, s.replace(':', ' '), W / 2, H * 0.55, fit(c, s, W * 0.9, H * 0.9), '#FFB02E'); }, { res: 384 }); pl.material = flat('#FFFFFF', { map: pl.material.map }); return pl; };
    const fa = at(face(a0), 0, 0, 0.045), fb = at(face(a1), 0, 0, 0.045), colon = grp(at(quad(h * 0.07, h * 0.07, flat('#FFB02E')), 0, h * 0.13, 0), at(quad(h * 0.07, h * 0.07, flat('#FFB02E')), 0, -h * 0.13, 0)); colon.position.z = 0.05;
    const g = grp(at(box(w, h, 0.08, '#1A1C22', { outline: 0.01 }), 0, 0, 0), fa, fb, colon);
    g.userData.update = t => { const on = o.at != null && t >= o.at, u = on ? t - o.at : 9; fa.visible = !on; fb.visible = on; const k = 1 + 0.22 * Math.max(0, 1 - u / 0.07) + 0.1 * wob(u - 0.07, 40, 12); fb.scale.set(k, k, 1); colon.visible = Math.floor(t * 2.4) % 2 === 0 || u < 0.3; };
    g.userData.update(0); return g;
  },

  // a candle in its holder (a dish with a ring to hold it by): the flame flickers; o.litAt: it lights then; o.outAt: it goes out, a thread of smoke goes up.
  // The flame and its halo are unlit (give the prop `inDark` in a dark shot). Origin: under the dish; held by the ring: on={..., offset}
  candle(o) {
    const fl = grp(at(new THREE.Mesh(new THREE.ConeGeometry(0.022, 0.085, 7), flat('#FFB23A')), 0, 0.045, 0), at(new THREE.Mesh(new THREE.ConeGeometry(0.012, 0.05, 6), flat('#FFF0B0')), 0, 0.032, 0)); fl.position.y = 0.2;
    const halo = at(new THREE.Mesh(new THREE.CircleGeometry(0.16, 20), flat('#FFC860', { transparent: true, opacity: 0.22, depthWrite: false, side: THREE.DoubleSide })), 0, 0.245, 0);
    const smoke = [0, 1, 2].map(() => { const p = sphere(0.014, '#C9C9CF', 1, { opacity: 0.7, unique: true }); p.castShadow = false; return p; });
    const g = grp(at(cyl(0.085, 0.07, 0.02, '#C9A24A', 12, { outline: 0.006 }), 0, 0.01, 0), at(cyl(0.024, 0.026, 0.17, '#F6F1E2', 8, { outline: 0.004 }), 0, 0.105, 0), at(box(0.004, 0.02, 0.004, '#1B1B1E'), 0, 0.2, 0), fl, halo, ...smoke);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.03, 0.007, 5, 12), mat('#C9A24A')); ring.position.set(0.1, 0.02, 0); ring.rotation.x = PI / 2; g.add(ring);
    g.userData.update = t => { const on = (o.litAt == null || t >= o.litAt) && (o.outAt == null || t < o.outAt), u = o.outAt != null ? t - o.outAt : -1;
      fl.visible = halo.visible = on; if (on) { const k = 1 + 0.16 * Math.sin(t * 19) + 0.09 * Math.sin(t * 37 + 1); fl.scale.set(1, k, 1); fl.rotation.z = 0.1 * Math.sin(t * 11); halo.scale.setScalar(1 + 0.07 * Math.sin(t * 23)); }
      smoke.forEach((p, i) => { const q = u - i * 0.07; p.visible = u >= 0 && q > 0 && q < 0.7; if (p.visible) { p.position.set(0.02 * Math.sin(q * 9 + i), 0.22 + q * 0.5, 0); p.scale.setScalar(1 + q * 3); p.material.opacity = 0.7 * (1 - q / 0.7); } }); };
    g.userData.update(0); return g;
  },

  // the sun as a lamp: a disc with rays and a face. o.offAt: it goes out like a bulb: the disc turns to cold grey, the rays fold back, a red thread of
  // filament dies in the middle, its eyes go wide then shut. Unlit: with `inDark` it stays in the black sky. Origin: its centre, front +Z; o.r (1.2 m)
  sunLamp(o) {
    const R = o.r ?? 1.2, disc = new THREE.Mesh(new THREE.CircleGeometry(R, 28), flat('#FFD23A')), rays = grp(), filM = flat('#FF5A2A', { transparent: true, side: THREE.DoubleSide }), fil = grp(...[-1.5, -0.5, 0.5, 1.5].map((x, i) => { const q = quad(R * 0.035, R * 0.2, filM); q.position.x = x * R * 0.085; q.rotation.z = (i % 2 ? 1 : -1) * 0.46; return q; })); fil.position.set(0, R * 0.52, 0.03);   // the filament: a little zigzag high in the bulb (v1: a ring round the mouth, which stayed as a red-brown rim on the dead sun)
    for (let i = 0; i < 12; i++) { const a = i * PI / 6, q = quad(0.14 * R, 0.5 * R, flat('#FFE07A')); q.geometry = new THREE.PlaneGeometry(0.14 * R, 0.5 * R).translate(0, 0.25 * R, 0); const p = grp(q); p.position.set(Math.sin(a) * R * 1.1, Math.cos(a) * R * 1.1, -0.01); p.rotation.z = -a; rays.add(p); }
    const eye = sx => { const e = grp(at(new THREE.Mesh(new THREE.CircleGeometry(R * 0.15, 16), flat('#FFFDF2')), 0, 0, 0), at(new THREE.Mesh(new THREE.CircleGeometry(R * 0.07, 12), flat('#2A1E12')), 0, 0, 0.01)); e.position.set(sx * R * 0.34, R * 0.2, 0.02); return e; };
    const eL = eye(-1), eR = eye(1), lids = [-1, 1].map(sx => at(quad(R * 0.34, R * 0.04, flat('#2A1E12')), sx * R * 0.34, R * 0.2, 0.03));
    const mouth = at(new THREE.Mesh(new THREE.RingGeometry(R * 0.2, R * 0.25, 16, 1, PI * 1.15, PI * 0.7), flat('#2A1E12', { side: THREE.DoubleSide })), 0, -R * 0.1, 0.02), oh = at(new THREE.Mesh(new THREE.CircleGeometry(R * 0.1, 14), flat('#2A1E12')), 0, -R * 0.32, 0.02);
    const inner = grp(rays, disc, eL, eR, ...lids, mouth, oh, fil), g = grp(inner), cOn = new THREE.Color('#FFD23A'), cOff = new THREE.Color(o.offColor || '#3A4152');
    g.userData.update = t => { const u = o.offAt == null ? -1 : t - o.offAt, off = u >= 0, k = off ? clamp01(u / 0.06) : 0;
      disc.material.color.copy(cOn).lerp(cOff, k); rays.children.forEach((p, i) => { p.scale.y = off ? Math.max(0.001, 1 - ease.out(clamp01(u / 0.12))) : 1 + 0.08 * Math.sin(t * 5 + i); p.visible = !off || u < 0.12; }); rays.rotation.z = off ? 0 : t * 0.25;
      const scared = o.scareAt != null && t >= o.scareAt && !off, shut = off && u > 0.45;
      for (const e of [eL, eR]) { e.visible = !shut; e.scale.setScalar(scared || (off && !shut) ? 1.45 : 1); e.children[1].scale.setScalar(scared || off ? 0.6 : 1); }
      lids.forEach(l => l.visible = shut); mouth.visible = !scared && !off; oh.visible = scared || off; oh.scale.setScalar(shut ? 0.5 : 1);
      fil.visible = off && u < (o.filament ?? 0.4); if (fil.visible) filM.opacity = Math.max(0, 1 - u / (o.filament ?? 0.4)) * (0.7 + 0.3 * Math.sin(t * 40)); inner.scale.setScalar(off ? 1 - 0.06 * Math.max(0, 1 - u / 0.2) : 1); };
    g.userData.update(0); return g;
  },

  // a telescope on its tripod: a brass spyglass in three draws. The widest draw, with the lens, is at the sky end: it goes up and the thinner draws come out
  // of it behind (v1 was a white tube, thickest at the eye end, with no lens: a bat). o.extend [[t, 0..1], ...]; o.tilt (deg above the horizon, default 40);
  // o.h (1.15 m: the height of its pivot: raise it until the eyepiece meets an eye, userData.eyepiece gives its place); o.len (0.9: the length of a draw);
  // o.color / o.ring. The lens and its glint are unlit. Origin: under the tripod; it points toward +Z and up
  telescope(o) {
    const tilt = (o.tilt ?? 40) * PI / 180, L = o.len ?? 0.9, H0 = o.h ?? 1.15, piv = grp(), brass = o.color || '#C99A3C', ring = o.ring || '#7A5A22'; piv.position.y = H0; piv.rotation.x = -tilt;
    const tube = (r, band) => { const t = grp(at(cyl(r, r, L, brass, 14, { outline: 0.006 }), 0, 0, 0, PI / 2, 0, 0), at(cyl(r + 0.008, r + 0.008, band, ring, 14), 0, 0, L / 2 - band / 2, PI / 2, 0, 0), at(cyl(r + 0.006, r + 0.006, 0.03, ring, 14), 0, 0, -L / 2 + 0.02, PI / 2, 0, 0));
      t.add(at(quad(r * 0.5, L * 0.9, flat('#F3D58A', { transparent: true, opacity: 0.55, side: THREE.DoubleSide })), 0, r + 0.002, 0, -PI / 2, 0, 0)); return t; };   // a pale line along the top: polished metal
    const d1 = tube(0.045, 0.04), d2 = tube(0.062, 0.05), d3 = tube(0.082, 0.07);
    const lens = at(new THREE.Mesh(new THREE.CircleGeometry(0.074, 18), flat('#9FD3F2', { side: THREE.DoubleSide })), 0, 0, L / 2 + 0.002), glint = at(new THREE.Mesh(new THREE.CircleGeometry(0.022, 10), flat('#FFFFFF', { side: THREE.DoubleSide })), -0.028, 0.03, L / 2 + 0.004), glint2 = at(new THREE.Mesh(new THREE.CircleGeometry(0.01, 8), flat('#FFFFFF', { side: THREE.DoubleSide })), 0.02, -0.03, L / 2 + 0.004);
    d3.add(lens, glint, glint2);
    piv.add(d1, d2, d3, at(cyl(0.03, 0.03, 0.09, '#1B1B1E', 10), 0, 0, -L / 2 - 0.04, PI / 2, 0, 0), at(cyl(0.04, 0.03, 0.03, '#1B1B1E', 10), 0, 0, -L / 2 - 0.085, PI / 2, 0, 0));
    const g = grp(piv, at(sphere(0.06, '#2B2B30', 1), 0, H0, 0));
    for (let i = 0; i < 3; i++) { const a = i * TAU / 3 + 0.5, leg = box(0.035, (H0 + 0.05) / Math.cos(0.3), 0.035, '#3A2E22', { pivot: 'top' }); leg.position.set(0, H0 - 0.02, 0); leg.rotation.set(0.3 * Math.cos(a), 0, -0.3 * Math.sin(a)); g.add(leg); }
    g.userData.update = t => { const k = keyed(o.extend, t, ease.outBack); d2.position.z = 0.012 + k * L * 0.82; d3.position.z = 0.024 + k * L * 1.64; };
    g.userData.update(0); g.userData.eyepiece = [0, H0 + Math.sin(tilt) * (-L / 2 - 0.1), Math.cos(tilt) * (-L / 2 - 0.1)]; return g;
  },

  // the beam of a torch: a pale cone that widens from the origin along +Z, o.len long (6 m), o.r wide at its end (0.9 m). o.sweep [[t, deg], ...]: it turns
  // about the vertical; o.pitch [[t, deg], ...]: it lifts. Unlit and see-through: give it `inDark` in a dark shot.
  // o.flat: a painted beam instead (v1's cone was a hard-edged triangle laid over the man who held it): a wedge in the prop's own XY plane (turn the prop to
  // the camera), soft at its edges and fading with the distance, that leaves the origin upward and leans by o.sweep degrees (+ = toward +X); the torch itself
  // is drawn at its foot (o.torch false: no torch)
  torchBeam(o) {
    const L = o.len ?? 6, R = o.r ?? 0.9;
    if (o.flat) {
      const pl = canvasPlane(2 * R, L, (c, W, H) => { c.clearRect(0, 0, W, H); const img = c.createImageData(W, H), col = new THREE.Color(o.color || '#FFF1B8');
        for (let y = 0; y < H; y++) { const v = 1 - y / H, hw = 0.035 + 0.965 * v; for (let x = 0; x < W; x++) { const u = Math.abs(x / W - 0.5) * 2 / hw, a = u >= 1 ? 0 : Math.pow(1 - u * u, 1.3) * Math.pow(1 - v, 1.5) * (0.35 + 0.65 * Math.min(1, v * 8)), i = (y * W + x) * 4;
          img.data[i] = col.r * 255; img.data[i + 1] = col.g * 255; img.data[i + 2] = col.b * 255; img.data[i + 3] = 255 * a; } } c.putImageData(img, 0, 0); }, { res: 256, transparent: true });
      pl.material = flat('#FFFFFF', { map: pl.material.map, transparent: true, opacity: o.opacity ?? 0.85, depthWrite: false, side: THREE.DoubleSide }); pl.position.set(0, L / 2, 0);
      const piv = grp(pl), g = grp(piv);
      if (o.torch !== false) piv.add(at(cyl(0.035, 0.03, 0.2, '#2B2B30', 10, { outline: 0.005 }), 0, -0.12, 0), at(cyl(0.05, 0.038, 0.06, '#F2C230', 10, { outline: 0.005 }), 0, -0.01, 0), at(new THREE.Mesh(new THREE.CircleGeometry(0.045, 12), flat('#FFFBE6', { side: THREE.DoubleSide })), 0, 0.022, 0, -PI / 2, 0, 0));
      g.userData.update = t => { piv.rotation.z = -keyed(o.sweep, t, ease.inOut) * PI / 180; };
      g.userData.update(0); return g;
    }
    const cone = new THREE.Mesh(new THREE.ConeGeometry(R, L, 18, 1, true).rotateX(-PI / 2).translate(0, 0, L / 2), flat(o.color || '#FFF1B8', { transparent: true, opacity: o.opacity ?? 0.3, depthWrite: false, side: THREE.DoubleSide }));
    const piv = grp(cone, at(new THREE.Mesh(new THREE.CircleGeometry(0.035, 10), flat('#FFFBE6', { side: THREE.DoubleSide })), 0, 0, 0.01)), g = grp(piv);
    g.userData.update = t => { piv.rotation.set(-keyed(o.pitch, t, ease.inOut) * PI / 180, keyed(o.sweep, t, ease.inOut) * PI / 180, 0, 'YXZ'); };
    g.userData.update(0); return g;
  },

  // a nightcap: a long striped cone that falls to one side, a pompon at its tip that swings. Origin: the top of the head (attach it to the head)
  nightCap(o) {
    const c1 = o.color || '#F4F1E8', c2 = o.stripe || '#3F6FB5', g = grp(at(box(0.3, 0.07, 0.3, c1, { outline: 0.006 }), 0, 0.035, 0)), a = grp(), b = grp(), pom = sphere(0.06, c1, 1);
    for (let i = 0; i < 3; i++) { const sg = box(0.26 - i * 0.05, 0.1, 0.26 - i * 0.05, i % 2 ? c1 : c2, { pivot: 'bottom', taper: 0.8 }); sg.position.y = 0.07 + i * 0.1; g.add(sg); }
    a.position.set(0, 0.36, 0); g.add(a); for (let i = 0; i < 3; i++) { const sg = box(0.11 - i * 0.02, 0.12, 0.11 - i * 0.02, i % 2 ? c2 : c1, { pivot: 'bottom', taper: 0.8 }); sg.position.y = i * 0.12; (i < 2 ? a : b).add(sg); }
    b.position.y = 0.24; a.add(b); pom.position.y = 0.26; b.add(pom); b.children[0].position.y = 0;
    g.userData.update = t => { const s = Math.sin(t * 2.6 + (o.ph || 0)); a.rotation.z = -0.75 + 0.07 * s; b.rotation.z = -0.9 + 0.16 * Math.sin(t * 2.6 + (o.ph || 0) - 0.6); };
    g.userData.update(0); return g;
  },

  // a letter that can be far too big: a white envelope with its flap line, a red stamp, a window. o.w (0.3 m), o.to / o.line2 (the address lines in the
  // window), o.title (printed top left). o.eyes [t0, t1]: two eyes look out of the window between these times (somebody is under it), and blink.
  // Unlit front (it reads in a dark shot with `inDark`). Origin: its middle, front +Z
  bigEnvelope(o) {
    const w = o.w ?? 0.3, h = w * 0.62;
    const pl = canvasPlane(w, h, (c, W, H) => { c.fillStyle = o.color || '#FBF8EE'; c.fillRect(0, 0, W, H); c.strokeStyle = '#CFC8B4'; c.lineWidth = H * 0.012; c.beginPath(); c.moveTo(0, 0); c.lineTo(W / 2, H * 0.42); c.lineTo(W, 0); c.stroke(); c.strokeRect(0, 0, W, H);
      c.fillStyle = '#C8322A'; c.fillRect(W * 0.8, H * 0.08, W * 0.13, H * 0.26); c.fillStyle = '#FBF8EE'; c.fillRect(W * 0.825, H * 0.12, W * 0.08, H * 0.18);
      if (o.title) { c.textAlign = 'left'; c.fillStyle = '#2B4C8C'; c.font = `900 ${H * 0.13}px Arial`; c.textBaseline = 'middle'; c.fillText(o.title, W * 0.06, H * 0.16); }
      c.fillStyle = '#DCE6EC'; c.fillRect(W * 0.1, H * 0.5, W * 0.62, H * 0.36); c.strokeStyle = '#9AA6AE'; c.lineWidth = H * 0.012; c.strokeRect(W * 0.1, H * 0.5, W * 0.62, H * 0.36);
      if (o.to) txt(c, o.to, W * 0.41, H * 0.61, fit(c, o.to, W * 0.56, H * 0.15), '#17171A'); if (o.line2) txt(c, o.line2, W * 0.41, H * 0.77, fit(c, o.line2, W * 0.56, H * 0.13), '#17171A'); }, { res: 512 });
    pl.material = flat('#FFFFFF', { map: pl.material.map, side: THREE.DoubleSide });
    const g = grp(at(solid(w, h, w * 0.012, flat('#E9E4D4')), 0, 0, -w * 0.008), pl), eyes = grp(); eyes.position.set(-w * 0.09, h * (0.5 - 0.68), w * 0.004); g.add(eyes);
    const cover = at(quad(w * 0.6, h * 0.34, flat('#DCE6EC')), 0, 0, 0); eyes.add(cover);
    const E = [-1, 1].map(sx => { const e = grp(at(new THREE.Mesh(new THREE.CircleGeometry(h * 0.1, 14), flat('#FFFFFF')), 0, 0, 0.001), at(new THREE.Mesh(new THREE.CircleGeometry(h * 0.045, 10), flat('#17171A')), 0, 0, 0.002)); e.position.x = sx * h * 0.15; e.children[0].scale.y = 1.2; eyes.add(e); return e; });
    g.userData.update = t => { const on = !!o.eyes && t >= o.eyes[0] && t < o.eyes[1]; eyes.visible = on; if (!on) return; const u = t - o.eyes[0], cyc = u % 1.3; let bl = !o.blinks && cyc > 0.5 && cyc < 0.62 ? Math.abs(1 - (cyc - 0.5) / 0.06) : 1; const op = Math.min(1, u / (o.eyesOpen ?? 0.08));
      for (const b of o.blinks || []) { const q = t - b; if (q >= 0 && q < 0.12) bl = Math.abs(1 - q / 0.06); }   // o.blinks [t, ...]: they blink then (default: one blink 0.5 s after they open, every 1.3 s)
      E.forEach(e => { e.scale.y = Math.max(0.05, bl * op); e.children[1].position.x = h * 0.03 * Math.sin(u * 2.2); }); };
    g.userData.update(0); return g;
  },

  // a match: a little stick with a red head. o.litAt: its flame takes; o.outAt: blown out. The flame is unlit (inDark). Origin: its foot, upright
  matchStick(o) {
    const fl = grp(at(new THREE.Mesh(new THREE.ConeGeometry(0.03, 0.11, 7), flat('#FFB23A')), 0, 0.055, 0), at(new THREE.Mesh(new THREE.ConeGeometry(0.016, 0.065, 6), flat('#FFF0B0')), 0, 0.04, 0)); fl.position.y = 0.2;
    const halo = at(new THREE.Mesh(new THREE.CircleGeometry(0.2, 20), flat('#FFC860', { transparent: true, opacity: 0.2, depthWrite: false, side: THREE.DoubleSide })), 0, 0.25, 0);
    const g = grp(at(box(0.014, 0.2, 0.014, '#D9B98A', { pivot: 'bottom' }), 0, 0, 0), at(box(0.024, 0.03, 0.024, '#B5302A'), 0, 0.2, 0), fl, halo);
    g.userData.update = t => { const on = o.litAt != null && t >= o.litAt && (o.outAt == null || t < o.outAt), u = t - (o.litAt || 0); fl.visible = halo.visible = on;
      if (on) { const k = (u < 0.1 ? 1 + 1.6 * (1 - u / 0.1) : 1) * (1 + 0.14 * Math.sin(t * 21) + 0.08 * Math.sin(t * 39)); fl.scale.set(k > 1.6 ? 1.5 : 1, k, k > 1.6 ? 1.5 : 1); halo.scale.setScalar((u < 0.1 ? 1.6 : 1) * (1 + 0.06 * Math.sin(t * 25))); } };
    g.userData.update(0); return g;
  },

  // a pair of eyes of its own, for what has no face rig (a pigeon, a cat, a statue, somebody at a window) in a dark shot: two pale ovals, two pupils.
  // o.s (0.05 m: the half width of an eye), o.gap (1.25: half the distance between the eyes, in s), o.tall (1.25), o.pupil (0.42: its radius, in s),
  // o.slit (a cat: the pupil is an upright slit), o.color / o.pupilColor. o.look [[t, -1..1], ...] and o.lookY [[t, -1..1], ...]: the pupils go aside, up (+)
  // or down; o.blinks [t, ...], o.openAt / o.shutAt; o.narrow [[t, 0..1], ...]: the upper lids come down aslant, the inner end lower: a glare (0.45: half
  // the eye; 1: shut); o.frame [w, h]: a dim window round them (somebody at a window). Unlit: give it `inDark`. Front +Z
  eyesPair(o) {
    const s = o.s ?? 0.05, tall = o.tall ?? 1.25, pr = o.pupil ?? 0.42, N = 14, in_ = grp(), g = grp(in_);
    // an ellipse (centre cx, cy; radii rx, ry) cut by a lid line y <= c + m x: columns from its left end to its right end, a top and a bottom point each
    const strip = () => { const ge = new THREE.BufferGeometry(); ge.setAttribute('position', new THREE.BufferAttribute(new Float32Array((N + 1) * 6), 3)); const ix = []; for (let i = 0; i < N; i++) ix.push(2 * i, 2 * i + 1, 2 * i + 2, 2 * i + 2, 2 * i + 1, 2 * i + 3); ge.setIndex(ix); return ge; };
    const shape = (ge, cx, cy, rx, ry, c, m) => { const p = ge.attributes.position;
      for (let i = 0; i <= N; i++) { const x = cx - rx * Math.cos(PI * i / N), h = ry * Math.sin(PI * i / N), yb = cy - h, yt = Math.min(cy + h, Math.max(c + m * x, yb)); p.setXYZ(2 * i, x, yt, 0); p.setXYZ(2 * i + 1, x, yb, 0); }
      p.needsUpdate = true; ge.computeBoundingSphere(); };
    const E = [-1, 1].map(sx => { const w = new THREE.Mesh(strip(), flat(o.color || '#F6F1E2', { side: THREE.DoubleSide })), pu = new THREE.Mesh(strip(), flat(o.pupilColor || '#0A0C14', { side: THREE.DoubleSide })); pu.position.z = 0.002; w.frustumCulled = pu.frustumCulled = false;
      const e = grp(w, pu); e.position.x = sx * s * (o.gap ?? 1.25); e.userData = { w, pu, sx }; in_.add(e); return e; });
    if (o.frame) { const [fw, fh] = o.frame, c0 = o.frameColor || '#101B30', c1 = o.barColor || '#22324F', b = Math.min(fw, fh) * 0.06, back = grp(at(quad(fw, fh, flat(c0)), 0, 0, 0));
      for (const [x, y, w2, h2] of [[0, fh / 2, fw + b, b], [0, -fh / 2, fw + b, b], [-fw / 2, 0, b, fh], [fw / 2, 0, b, fh]]) back.add(at(quad(w2, h2, flat(c1)), x, y, 0.001));
      back.position.set(0, o.frameY ?? 0, -0.01); g.add(back); }
    g.userData.update = t => { const on = (o.openAt == null || t >= o.openAt) && (o.shutAt == null || t < o.shutAt); in_.visible = on; if (!on) return;   // (the prop's own visibility belongs to the story's keys)
      let bl = 1; for (const b of o.blinks || []) { const u = t - b; if (u >= 0 && u < 0.12) bl = Math.abs(1 - u / 0.06); } const op = o.openAt == null ? 1 : Math.min(1, (t - o.openAt) / 0.06), lx = keyed(o.look, t, ease.inOut), ly = keyed(o.lookY, t, ease.inOut), n = clamp01(keyed(o.narrow, t, ease.inOut));
      const ry = s * tall, c = n > 0.001 ? ry * (1 - 2 * n) : ry * 2, m0 = 0.55 * Math.min(1, n * 2.2), pop = o.openAt == null ? 1 : 1 + 0.25 * Math.max(0, 1 - Math.abs((t - o.openAt) / 0.1 - 1)) * (t - o.openAt < 0.2 ? 1 : 0);   // a little overshoot as they open
      E.forEach(e => { const { w, pu, sx } = e.userData, m = m0 * sx, px = lx * s * (o.slit ? 0.62 : 0.5), py = ly * ry * 0.38; shape(w.geometry, 0, 0, s, ry, c, m); shape(pu.geometry, px, py, o.slit ? s * 0.16 : s * pr, o.slit ? ry * 0.82 : s * pr * Math.min(1.25, tall), c, m);
        e.scale.set(pop, Math.max(0.05, bl * op) * pop, 1); }); };
    g.userData.update(0); return g;
  },

  // stars that fly out of a knock, for a shot in the dark (the face's own stars are lit like the face: they go black with it): o.n (5) five-pointed stars
  // leave the origin at o.at, spread to o.r (0.4 m) in o.dur (0.45 s), spinning, and shrink away. Unlit: give it `inDark`. Front +Z
  impactStars(o) {
    const n = o.n ?? 5, R = o.r ?? 0.4, D = o.dur ?? 0.45, sz = o.size ?? 0.07, sh = new THREE.Shape();
    for (let i = 0; i < 10; i++) { const a = i * PI / 5 + PI / 2, r = i % 2 ? 0.45 : 1; sh[i ? 'lineTo' : 'moveTo'](Math.cos(a) * r, Math.sin(a) * r); } sh.closePath();
    const geo = new THREE.ShapeGeometry(sh), g = grp(), S = Array.from({ length: n }, (_, i) => { const m = new THREE.Mesh(geo, flat(i % 2 ? '#FFE27A' : '#FFF6C8', { side: THREE.DoubleSide })); m.castShadow = false; g.add(m); return m; });
    g.userData.update = t => { const u = (t - (o.at ?? 0)) / D; S.forEach((m, i) => { m.visible = u >= 0 && u < 1; if (!m.visible) return; const a = (o.a0 ?? 0.3) + i * TAU / n, k = ease.out(u), q = sz * (u < 0.15 ? u / 0.15 : 1 - 0.7 * (u - 0.15) / 0.85);
      m.position.set(Math.cos(a) * R * k, Math.sin(a) * R * k * (o.flatten ?? 1), 0); m.rotation.z = u * 5 * (i % 2 ? 1 : -1); m.scale.setScalar(Math.max(0.001, q)); }); };
    g.userData.update(0); return g;
  },

  // a glint on a pane of glass in the dark: two slanted pale bars that flash at o.at and slide away as they fade (o.dur 0.3 s). o.w (0.5 m). Unlit: `inDark`
  glassGlint(o) {
    const w = o.w ?? 0.5, D = o.dur ?? 0.3, mk = (bw, x) => { const q = quad(bw, w * 1.5, flat('#DFF1FF', { transparent: true, opacity: 0.8, depthWrite: false, side: THREE.DoubleSide })); q.position.x = x; return q; }, bars = [mk(w * 0.16, -w * 0.12), mk(w * 0.06, w * 0.1)], g = grp(...bars);
    g.rotation.z = -0.6;
    g.userData.update = t => { const u = (t - (o.at ?? 0)) / D; bars.forEach((b, i) => { b.visible = u >= 0 && u < 1; if (b.visible) { b.material.opacity = 0.8 * (u < 0.15 ? u / 0.15 : 1 - (u - 0.15) / 0.85); b.position.y = (u - 0.3) * w * 0.5 * (i ? 1.3 : 1); } }); };
    g.userData.update(0); return g;
  },

  // the house across the street, seen from a balcony: the top of its front (a dark wall, a roof line, two chimneys) with a row of big windows that switch
  // with the city: o.keys [[t, lit (0|1)], ...] (o.lit 1: their state at the start), each window o.lag (0.1 s) after the one on its left. In the dark, from
  // o.eyesAt on, a pair of round eyes opens in each window, one after the other (o.eyesLag 0.09 s), looks left and right and blinks: whole, big, clear of
  // the caption band (the eyes of the far city, cityNight, were specks cut by the roofs). Unlit. Origin: the middle of the roof line, front +Z; o.w (7 m),
  // o.h (6 m: how far down the wall goes), o.n (3 windows), o.win [w, h] (1.1 x 1.3 m), o.winY (-0.85: their middle under the roof line), o.gap (1.55 m)
  nearHouse(o) {
    const w = o.w ?? 7, h = o.h ?? 6, n = o.n ?? 3, [ww, wh] = o.win || [1.1, 1.3], wy = o.winY ?? -0.85, gap = o.gap ?? 1.55, keys = (o.keys || []).slice().sort((a, b) => a[0] - b[0]), lit0 = o.lit ?? 1, lag = o.lag ?? 0.1, es = o.eyeS ?? ww * 0.13;
    const g = grp(at(solid(w, h, 0.4, flat(o.wall || '#0A1124')), 0, -h / 2, -0.2), at(solid(w + 0.4, 0.26, 0.7, flat(o.roof || '#16203E')), 0, 0.13, -0.15), at(solid(w, 0.07, 0.42, flat(o.roof || '#16203E')), 0, wy - wh / 2 - 0.45, -0.19));
    for (const x of [-w * 0.3, w * 0.2]) g.add(at(solid(0.5, 0.85, 0.5, flat('#1A1626')), x, 0.68, -0.3), at(solid(0.6, 0.1, 0.6, flat('#262034')), x, 1.12, -0.3));
    const on = new THREE.Color(o.lightColor || '#FFD27A'), off = new THREE.Color(o.dark || '#0D1730'), W = [];
    for (let i = 0; i < n; i++) { const x = (i - (n - 1) / 2) * gap, pane = quad(ww, wh, flat('#FFD27A')), ep = grp(); pane.position.set(x, wy, 0.01); g.add(pane);
      for (const [dx, dy, a, b] of [[0, wh / 2, ww + 0.12, 0.08], [0, -wh / 2 - 0.02, ww + 0.22, 0.12], [-ww / 2, 0, 0.08, wh], [ww / 2, 0, 0.08, wh], [0, 0, 0.045, wh], [0, wh * 0.18, ww, 0.045]]) g.add(at(quad(a, b, flat('#222C4A')), x + dx, wy + dy, 0.02));
      const E = [-1, 1].map(sx => { const e = grp(at(new THREE.Mesh(new THREE.CircleGeometry(es, 18), flat('#F6F1E2')), 0, 0, 0), at(new THREE.Mesh(new THREE.CircleGeometry(es * 0.45, 12), flat('#0A0C14')), 0, 0, 0.002)); e.position.x = sx * es * 1.3; ep.add(e); return e; });
      ep.position.set(x, wy - wh * 0.14, 0.03); g.add(ep); W.push({ pane, ep, E, i }); }
    g.userData.update = t => { for (const q of W) { let st = lit0; for (const [tk, v] of keys) { if (t >= tk + lag * q.i) st = v; else break; }
      q.pane.material.color.copy(st ? on : off);
      const u = o.eyesAt == null || st ? -1 : t - (o.eyesAt + q.i * (o.eyesLag ?? 0.09)); q.ep.visible = u >= 0; if (u < 0) continue;
      const pop = Math.min(1, u / 0.05) * (1 + 0.3 * (u < 0.2 ? Math.max(0, 1 - Math.abs(u / 0.1 - 1)) : 0)), cyc = (u + q.i * 0.37) % 1.2, bl = cyc > 0.62 && cyc < 0.74 ? Math.abs(1 - (cyc - 0.62) / 0.06) : 1, lx = u < 0.14 ? 0 : (Math.sin((u - 0.14) * 7 + q.i * 2.1) > 0 ? 1 : -1);
      q.E.forEach(e => { e.scale.set(pop, Math.max(0.05, pop * bl), 1); e.children[1].position.x += (lx * es * 0.45 - e.children[1].position.x) * 0.5; }); } };
    g.userData.update(0); return g;
  },

  // somebody whistles: notes leave the origin one after the other, drift up and aside, rock and fade. o.n (3), o.from (0 s), o.every (0.16 s), o.size
  // (0.11 m), o.dx / o.dy: where they drift (m per second). Unlit. Front +Z
  whistleNotes(o) {
    const n = o.n ?? 3, sz = o.size ?? 0.11, g = grp(), N = Array.from({ length: n }, (_, i) => { const pl = canvasPlane(sz, sz * 1.3, (c, W, H) => { c.clearRect(0, 0, W, H); c.fillStyle = c.strokeStyle = o.color || '#1B1B1E'; c.lineWidth = W * 0.09;
      c.beginPath(); c.ellipse(W * 0.34, H * 0.78, W * 0.2, H * 0.11, -0.4, 0, TAU); c.fill(); c.beginPath(); c.moveTo(W * 0.51, H * 0.76); c.lineTo(W * 0.51, H * 0.14); c.stroke();
      if (i % 2) { c.beginPath(); c.moveTo(W * 0.51, H * 0.14); c.quadraticCurveTo(W * 0.9, H * 0.22, W * 0.82, H * 0.5); c.stroke(); } else { c.beginPath(); c.ellipse(W * 0.72, H * 0.66, W * 0.2, H * 0.11, -0.4, 0, TAU); c.fill(); c.beginPath(); c.moveTo(W * 0.89, H * 0.64); c.lineTo(W * 0.89, H * 0.06); c.lineTo(W * 0.51, H * 0.14); c.stroke(); } }, { res: 96, transparent: true });
      pl.material = flat('#FFFFFF', { map: pl.material.map, transparent: true, depthWrite: false, side: THREE.DoubleSide }); g.add(pl); return pl; });
    g.userData.update = t => N.forEach((m, i) => { const u = t - (o.from ?? 0) - i * (o.every ?? 0.16); m.visible = u >= 0 && u < (o.life ?? 0.7); if (!m.visible) return; const q = u / (o.life ?? 0.7);
      m.position.set((o.dx ?? 0.35) * u + 0.04 * Math.sin(u * 9 + i), (o.dy ?? 0.5) * u, 0.01 * i); m.rotation.z = 0.3 * Math.sin(u * 7 + i * 2); m.scale.setScalar(u < 0.08 ? u / 0.08 : 1); m.material.opacity = q < 0.7 ? 1 : 1 - (q - 0.7) / 0.3; });
    g.userData.update(0); return g;
  },

  // a burglar's mask to wear over the painted face: a black band along the line of the eyes (the painted face is askew: one eye sits 10 cm above the
  // other) with two holes: the painted eyes show through. Sized for the face panel of the series (0.24 x 0.5 m); attach it to the head:
  // on={actor, joint: 'head', offset: [0, 0.25, 0.092]}. o.th: the width of the band (0.1 m)
  bandMask(o) {
    const w = o.w ?? 0.24, h = o.h ?? 0.5, th = o.th ?? 0.1;
    const pl = canvasPlane(w, h, (c, W, H) => { c.clearRect(0, 0, W, H); const ex = [0.211 * W, 0.752 * W], ey = [0.262 * H, 0.457 * H], a = Math.atan2(ey[1] - ey[0], ex[1] - ex[0]);
      c.save(); c.translate((ex[0] + ex[1]) / 2, (ey[0] + ey[1]) / 2); c.rotate(a); c.fillStyle = '#141418'; c.fillRect(-W * 1.5, -th / w * W / 2, W * 3, th / w * W); c.restore();
      c.globalCompositeOperation = 'destination-out'; for (const k of [0, 1]) { c.beginPath(); c.ellipse(ex[k], ey[k], W * 0.17, H * (k ? 0.045 : 0.055), 0, 0, TAU); c.fill(); } c.globalCompositeOperation = 'source-over'; }, { res: 256, transparent: true });
    return grp(pl);
  },
};
