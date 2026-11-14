// « Le café » (story 63, cycle 25): a man drank ten coffees in a row. He started to vibrate. So fast that he goes through walls. The town hall hired
// him as a jackhammer. He dug a metro line in one night. Yesterday he was served a decaf. He stopped dead, in the middle of the tunnel. The line has
// been blocked ever since. The passengers bring him coffees. Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every
// animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { mat, box, cyl } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const eo = x => 1 - Math.pow(1 - clamp01(x), 3);
const ob = x => { const c = 1.70158, u = clamp01(x) - 1; return 1 + (c + 1) * u * u * u + c * u * u; };   // ease out with an overshoot
const hash = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };

// a coffee cup on its saucer (pivot at the saucer's underside): white china, a handle toward +X, coffee inside unless o.empty
function cup(o = {}) {
  const g = grp(), china = o.color || '#F7F5EF';
  g.add(at(cyl(0.075, 0.07, 0.012, china, 18), 0, 0.006, 0), at(cyl(0.042, 0.032, 0.062, china, 16, { outline: 0.004 }), 0, 0.043, 0));
  const h = new THREE.Mesh(new THREE.TorusGeometry(0.016, 0.005, 6, 12), mat(china)); h.position.set(0.046, 0.046, 0); g.add(h);
  if (!o.empty) g.add(at(cyl(0.038, 0.038, 0.004, '#3B2216', 16), 0, 0.07, 0));
  return g;
}

export const CAFE_PROPS = {
  cup: o => cup(o),

  // A tower of empty cups on their saucers (pivot at its foot): from o.at[0] to o.at[1] they pop on one by one up to o.n (10), each with a little
  // overshoot; the tower leans and sways more as it grows (o.sway, 1). (S02) o.rattle [t, amp]: from t every cup jitters on the one below, the
  // higher the more (amp 0.012 m at the foot), hopping and turning a little (the table shakes under a man who vibrates)
  cupTower(o) {
    const n = o.n ?? 10, g = grp(), cups = [], [t0, t1] = o.at || [0, 1];
    for (let i = 0; i < n; i++) { const c = cup({ empty: true }); c.position.y = i * 0.078; c.rotation.y = hash(i) * TAU; g.add(c); cups.push(c); }
    g.userData.update = t => { const k = n * clamp01((t - t0) / Math.max(1e-3, t1 - t0)); let shown = 0; const ra = o.rattle && t >= o.rattle[0] ? (o.rattle[1] ?? 0.012) * clamp01((t - o.rattle[0]) / 0.15) : 0;
      cups.forEach((c, i) => { const u = k - i; c.visible = u > 0; if (!c.visible) return; shown++; const s = ob(u * 2.5); c.scale.setScalar(Math.max(0.01, s)); c.position.x = (hash(i + 7) - 0.5) * 0.02 * i;
        c.position.y = i * 0.078; c.rotation.y = hash(i) * TAU;
        if (ra) { const a = ra * (1 + 0.18 * i); c.position.x += a * Math.sin(t * 131 + i * 1.7); c.position.z = a * Math.sin(t * 117 + i * 2.3); c.position.y += 0.6 * a * Math.abs(Math.sin(t * 149 + i)); c.rotation.y += 4 * a * Math.sin(t * 97 + i); } });
      const lean = (o.sway ?? 1) * shown / n; g.rotation.z = lean * (0.05 + 0.04 * Math.sin(t * 7.3)); g.rotation.x = lean * 0.03 * Math.sin(t * 5.1 + 1); };
    g.userData.update(0); return g;
  },

  // A decaf (pivot at the saucer's underside): the cup and saucer, DÉCA in brown letters on the cup's front (+Z), two wisps of steam
  decaCup(o) {
    const g = cup({}), lb = canvasPlane(0.07, 0.03, (c, W, H) => { c.fillStyle = 'rgba(0,0,0,0)'; c.clearRect(0, 0, W, H); c.fillStyle = '#6B3A1E'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${Math.round(H * 0.82)}px Arial`; c.fillText(o.text || 'DÉCA', W / 2, H / 2); }, { res: 256, transparent: true });
    lb.position.set(0, 0.043, 0.041); g.add(lb);
    const wisps = [0, 1].map(i => { const w = new THREE.Mesh(new THREE.SphereGeometry(0.018, 8, 6), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0, depthWrite: false })); g.add(w); return w; });
    g.userData.update = t => wisps.forEach((w, i) => { const v = ((t * 0.9 + i * 0.5) % 1); w.position.set(0.01 * Math.sin(t * 3 + i), 0.08 + v * 0.12, 0); w.scale.setScalar(0.6 + v * 1.4); w.material.opacity = 0.6 * (1 - v); });
    g.userData.update(0); return g;
  },

  // A café's zinc bar (pivot at the floor in the middle of its front, the customer's side toward +Z): a wooden front o.w (2.6 m) long, 1.08 m high, a
  // zinc top with a rolled edge, a brass foot rail; an espresso machine on the top at o.machineX (chrome, two group heads, cups warming on top)
  zincBar(o) {
    const W = o.w ?? 2.6, D = 0.62, H = 1.08, g = grp();
    g.add(at(box(W, H - 0.05, D - 0.06, o.wood || '#6E3F24', { pivot: 'bottom', outline: 0.008 }), 0, 0, -D / 2 + 0.03));
    for (let i = 0; i < Math.floor(W / 0.5); i++) g.add(at(box(0.36, 0.62, 0.012, o.panel || '#7E4C2C', { outline: 0.004 }), -W / 2 + 0.3 + i * 0.5, 0.48, 0.004));
    g.add(at(box(W + 0.06, 0.05, D + 0.04, '#AEB4BA', { outline: 0.006 }), 0, H - 0.025, -D / 2), at(cyl(0.03, 0.03, W + 0.06, '#C2C8CE', 10), 0, H - 0.02, 0.02).rotateZ(PI / 2));
    g.add(at(cyl(0.018, 0.018, W - 0.2, '#C9A24B', 8), 0, 0.16, 0.12).rotateZ(PI / 2));
    const mx = o.machineX ?? -0.75, m = grp(at(box(0.62, 0.42, 0.4, '#C8CDD2', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(box(0.66, 0.05, 0.44, '#9AA0A6'), 0, 0.44, 0));
    for (const s of [-1, 1]) m.add(at(cyl(0.035, 0.03, 0.08, '#2A2C31', 10), s * 0.15, 0.2, 0.22), at(box(0.03, 0.03, 0.16, '#1E1F22'), s * 0.15, 0.18, 0.3));
    m.position.set(mx, H, -D / 2 - 0.02); g.add(m);
    for (let i = 0; i < 4; i++) g.add(at(cup({ empty: true }), mx - 0.21 + i * 0.14, H + 0.47, -D / 2 - 0.02));
    return g;
  },

  // A metro tunnel along X (pivot on the track bed in its middle): a concrete vault of radius o.r (2.4 m) over straight walls 1.4 m high, two rails
  // (1.44 m gauge) on sleepers, a cable tray and lamps every o.lampEvery (4 m) along the -Z wall, o.len (40 m) long. o.face (x, or null): a raw rock face
  // closes it there, cut by his digging; o.lit [[t, x], ...]: from t the lamps up to x are on (the tunnel lit as it is dug; default all on);
  // o.dust [[t0, t1], ...]: dust boiling off the face meanwhile. (script) o.faceMove [[t, x], ...]: the face moves (straight lines between the keys:
  // he digs it back); o.litFollow (m): the lamps are on up to that far behind the face wherever it is; o.endCap false: the far end (x = -len / 2)
  // left open (closed by default with a black plate, the tunnel running on into the dark)
  metroTunnel(o) {
    const R = o.r ?? 2.4, L = o.len ?? 40, h0 = 1.4, g = grp(), C = o.color || '#9A9A92';
    const cm = new THREE.MeshLambertMaterial({ color: C, side: THREE.BackSide }), vault = new THREE.Mesh(new THREE.CylinderGeometry(R, R, L, 28, 1, true, 0, PI), cm);
    vault.rotation.z = PI / 2; vault.rotation.y = 0; vault.position.y = h0; g.add(vault);
    for (const s of [-1, 1]) { const w = box(L, h0, 0.2, C); w.position.set(0, h0 / 2, s * (R + 0.1)); g.add(w); }
    g.add(at(box(L, 0.1, 2 * R, '#6E6A62'), 0, -0.05, 0));
    for (let x = -L / 2 + 0.3; x < L / 2; x += 0.62) g.add(at(box(0.22, 0.08, 2.1, '#5A4A3A'), x, 0.04, 0));
    for (const z of [-0.72, 0.72]) g.add(at(box(L, 0.1, 0.08, '#8E949A', { outline: 0.004 }), 0, 0.13, z));
    g.add(at(box(L, 0.12, 0.25, '#3A3C40'), 0, 1.1, -R + 0.15));
    const lamps = [], every = o.lampEvery ?? 4;
    for (let x = -L / 2 + every / 2; x < L / 2; x += every) { const lm = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.12, 0.08), new THREE.MeshBasicMaterial({ color: '#FFE8A8', toneMapped: false })); lm.position.set(x, 2.1, -R + 0.08); g.add(lm); lamps.push(lm); }
    let face = null;
    // (script of 63) the boulders keep to the rim of the bore and stand back in the face (in its middle they filled the place where he digs): big ones
    // round the edge, small ones studding the face itself, none sticking out more than about 0.45 m
    if (o.face != null) { face = grp(); for (let i = 0; i < 22; i++) { const r = 0.35 + hash(i) * 0.4, rk = new THREE.Mesh(new THREE.DodecahedronGeometry(r, 0), mat(i % 3 ? '#7A6A58' : '#6A5C4C')); const a = hash(i + 3) * PI, d = R * 0.7 + hash(i + 9) * (R * 0.3 - 0.15);
        rk.position.set(0.3 + hash(i + 5) * 0.3, Math.max(0.2, h0 + Math.sin(a) * d * 0.9), Math.cos(a) * d); rk.rotation.set(hash(i) * 3, hash(i + 1) * 3, 0); face.add(rk); }
      for (let i = 0; i < 40; i++) { const r = 0.12 + hash(i + 50) * 0.2, rk = new THREE.Mesh(new THREE.DodecahedronGeometry(r, 0), mat(i % 2 ? '#857462' : '#6E604F')); const a = hash(i + 51) * TAU, d = Math.sqrt(hash(i + 52)) * (R - 0.4);
        rk.position.set(0.22 + hash(i + 53) * 0.08, Math.min(h0 + R - 0.3, Math.max(0.15, h0 * 0.6 + Math.sin(a) * d)), Math.cos(a) * d); rk.rotation.set(hash(i + 54) * 3, hash(i + 55) * 3, 0); face.add(rk); }
      face.add(at(box(0.3, h0 + R, 2 * R, '#5E5244'), 0.35, (h0 + R) / 2, 0)); face.position.x = o.face; g.add(face); }
    if (o.endCap !== false) g.add(at(box(0.1, h0 + R + 0.2, 2 * R + 0.4, '#050608'), -L / 2, (h0 + R) / 2, 0));
    const FM = o.faceMove, faceX = t => { if (!FM || !FM.length) return o.face ?? 0; if (t <= FM[0][0]) return FM[0][1];
      for (let i = 1; i < FM.length; i++) if (t < FM[i][0]) { const [ta, xa] = FM[i - 1], [tb, xb] = FM[i]; return xa + (xb - xa) * (t - ta) / Math.max(1e-3, tb - ta); }
      return FM[FM.length - 1][1]; };
    g.userData.faceX = faceX;
    const puffs = [];
    // (stills 2 of 63) many small thin puffs: ten big opaque ones read as a ball rolling off the face
    // (review 1 of 63) angular grey puffs, lit by the lamps: soft round ones read as lens bokeh
    if (o.dust) for (let i = 0; i < 18; i++) { const p = new THREE.Mesh(new THREE.DodecahedronGeometry(0.17, 0), new THREE.MeshLambertMaterial({ color: i % 2 ? '#A49C90' : '#8E877C', flatShading: true, transparent: true, opacity: 0, depthWrite: false })); p.rotation.set(i, i * 2, 0); g.add(p); puffs.push(p); }
    g.userData.update = t => {
      const fxt = faceX(t); if (face) face.position.x = fxt;
      let litTo = Infinity; if (o.lit) { litTo = -Infinity; for (const [t0, x] of o.lit) if (t >= t0) litTo = x; }
      if (o.litFollow != null) litTo = fxt - o.litFollow;
      lamps.forEach(lm => { const on = lm.position.x <= litTo; lm.material.color.set(on ? '#FFE8A8' : '#3A3830'); });
      const active = (o.dust || []).some(([a, b]) => t >= a && t < b);
      puffs.forEach((p, i) => { const v = (t * 1.4 + i * 0.057) % 1; p.visible = active; if (!active) return; const fx = fxt - 0.25 - v * 1.6;
        p.position.set(fx, 0.4 + hash(i) * 2.4 + v * 0.3, (hash(i + 4) - 0.5) * 3.6); p.scale.setScalar(0.5 + v * 1.8); p.material.opacity = 0.62 * (1 - v); });
    };
    g.userData.update(0); return g;
  },

  // (S03) A wall that ripples like jelly where he goes through it (pivot at the middle of its foot, its face the plane z = 0 toward +Z): o.w (6 m) x
  // o.h (3.4); a cream paper with faint teal sprigs over a teal dado band (to o.dado, 0.95 m) and its trim, a skirting board, a framed seascape
  // (o.picture [x, y, w, h]: its centre in the wall's metres from the middle of the foot) and a light switch (o.switchX), all painted on the face so
  // they ripple with it. o.ripple [[t, x, y, amp], ...]: from t, rings run out from (x, y) at o.speed (3.2 m/s), o.wave (0.5 m) apart, dying away
  // (o.decay, 2.4 /s); amp (0.09 m) pushes the face toward +Z, and o.shear (0.6) of it sideways along the ring (the painted lines wave even head-on).
  // Behind it a plain back (o.back) down to o.thick (0.2 m)
  jellyWall(o) {
    const W = o.w ?? 6, H = o.h ?? 3.4, g = grp(), cv = document.createElement('canvas'); cv.width = 1024; cv.height = Math.round(1024 * H / W);
    const c = cv.getContext('2d'), sx = cv.width / W, sy = cv.height / H, X = x => (x + W / 2) * sx, Y = y => (H - y) * sy, dado = o.dado ?? 0.95;
    c.fillStyle = o.paper || '#F1E9D2'; c.fillRect(0, 0, cv.width, cv.height);
    c.fillStyle = o.sprig || '#C9DCCF';
    for (let j = 0; j * 0.24 < H; j++) for (let i = -1; i * 0.24 < W + 0.24; i++) { const px = -W / 2 + i * 0.24 + (j % 2) * 0.12, py = dado + 0.16 + j * 0.24; if (py > H - 0.05) continue;
      c.beginPath(); c.ellipse(X(px), Y(py), 0.016 * sx, 0.032 * sy, 0.5, 0, TAU); c.fill(); c.beginPath(); c.ellipse(X(px + 0.028), Y(py - 0.01), 0.016 * sx, 0.032 * sy, -0.5, 0, TAU); c.fill(); }
    c.fillStyle = o.band || '#7DB3AC'; c.fillRect(0, Y(dado), cv.width, dado * sy);
    c.fillStyle = o.trim || '#3F8A84'; c.fillRect(0, Y(dado + 0.035), cv.width, 0.07 * sy); c.fillRect(0, Y(0.12), cv.width, 0.12 * sy);
    if (o.picture !== false) { const [px, py, pw, ph] = o.picture || [0.9, 1.8, 1.0, 0.7];
      c.fillStyle = '#7A4E26'; c.fillRect(X(px - pw / 2), Y(py + ph / 2), pw * sx, ph * sy);
      const ix = X(px - pw / 2 + 0.07), iy = Y(py + ph / 2 - 0.07), iw = (pw - 0.14) * sx, ih = (ph - 0.14) * sy;
      c.fillStyle = '#A8D8F0'; c.fillRect(ix, iy, iw, ih * 0.56); c.fillStyle = '#2F7FB5'; c.fillRect(ix, iy + ih * 0.56, iw, ih * 0.44);
      c.fillStyle = '#FFFFFF'; c.beginPath(); c.moveTo(ix + iw * 0.46, iy + ih * 0.62); c.lineTo(ix + iw * 0.46, iy + ih * 0.14); c.lineTo(ix + iw * 0.7, iy + ih * 0.62); c.closePath(); c.fill();
      c.fillStyle = '#8A4A26'; c.fillRect(ix + iw * 0.32, iy + ih * 0.62, iw * 0.44, ih * 0.08);
      c.fillStyle = '#FFD84A'; c.beginPath(); c.arc(ix + iw * 0.17, iy + ih * 0.22, ih * 0.1, 0, TAU); c.fill(); }
    const swx = o.switchX ?? -W / 2 + 0.6; c.fillStyle = '#F8F6F0'; c.fillRect(X(swx), Y(1.2), 0.08 * sx, 0.12 * sy); c.strokeStyle = '#A9A496'; c.lineWidth = 2; c.strokeRect(X(swx), Y(1.2), 0.08 * sx, 0.12 * sy);
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
    const geo = new THREE.PlaneGeometry(W, H, Math.round(W * 16), Math.round(H * 16)); geo.translate(0, H / 2, 0);
    const face = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ map: tex })); face.receiveShadow = true; g.add(face);
    const T = o.thick ?? 0.2; g.add(at(box(W, H, T - 0.12, o.back || '#E3D7B8', { pivot: 'bottom' }), 0, 0, -(T + 0.12) / 2));
    const pos = geo.attributes.position, base = Float32Array.from(pos.array), sp = o.speed ?? 3.2, wv = o.wave ?? 0.5, dk = o.decay ?? 2.4;
    g.userData.update = t => {
      for (let i = 0; i < pos.count; i++) { const x = base[3 * i], y = base[3 * i + 1]; let dz = 0;
        let dx = 0, dy = 0;
        for (const [t0, rx, ry, amp] of (o.ripple || [])) { const tau = t - t0; if (tau <= 0) continue; const rr = Math.hypot(x - rx, y - ry), front = sp * tau; if (rr >= front) continue;
          const env = (amp ?? 0.09) * clamp01((front - rr) / 0.3) * Math.exp(-dk * tau - 0.3 * rr), ph = TAU * (front - rr) / wv; dz += env * Math.sin(ph);
          const dr = (o.shear ?? 0.6) * env * Math.cos(ph) / Math.max(0.05, rr); dx += (x - rx) * dr; dy += (y - ry) * dr; }
        const e = clamp01(Math.min(x + W / 2, W / 2 - x, y, H - y) / 0.35); pos.array[3 * i] = x + dx * e; pos.array[3 * i + 1] = y + dy * e; pos.array[3 * i + 2] = dz * e; }
      pos.needsUpdate = true; geo.computeVertexNormals(); };
    g.userData.update(0); return g;
  },

  // (S06) The ground cut open like a cartoon cutaway, one night of digging in one shot (pivot on the street surface in the middle of the cut, the cut
  // face the plane z = 0 toward +Z, the tunnel along X). Soil strata, stones, a pipe and roots down to y = -o.bottom (7 m); a metro tunnel o.th
  // (2.6 m) high with its floor at y = -o.depth (3.8), dug from o.x0 to o.x1 over o.at [t0, t1] (userData.dig(t): the face's x). Behind the face
  // the dug tunnel (a concrete back wall, rails on sleepers, lamps that light up as it passes), ahead of it the earth; rock chips thrown back off
  // the face while it moves. On the surface a pavement, a kerb and a road, lamp posts every 5 m, a row of Paris fronts o.far (16 m) back with lit
  // windows (o.frontH [12, 16]: their heights); a sky that turns from night to dawn over o.dawn [t0, t1] (the stars fade, the windows and the lamps go out), a moon that runs along
  // o.moon (three [x, y] points on the sky, o.far + 12 m back) over o.at, and a sun that comes up at o.sunX at the end. o.len (40 m): the cut's width
  groundCut(o) {
    const L = o.len ?? 40, D = o.depth ?? 3.8, TH = o.th ?? 2.6, B = o.bottom ?? 7, g = grp(), [t0, t1] = o.at || [0, 1], x0 = o.x0 ?? -L / 2, x1 = o.x1 ?? L / 2;
    const dig = t => x0 + (x1 - x0) * clamp01((t - t0) / Math.max(1e-3, t1 - t0)); g.userData.dig = dig;
    const top = -D + TH, DZ = 1.4;   // the tunnel's ceiling; how deep the cut goes into the ground
    const band = (y0, y1, col) => g.add(at(box(L, y0 - y1, DZ, col, { outline: 0.006 }), 0, (y0 + y1) / 2, -DZ / 2));
    band(0, -0.35, '#5E4330'); band(-0.35, top, '#A0703F'); band(-D, -D - 1.3, '#8C7A62'); band(-D - 1.3, -B, '#6C6052');
    const e1 = box(1, TH / 2, DZ, '#C29A62', { outline: 0.006 }), e2 = box(1, TH / 2, DZ, '#B08A5A', { outline: 0.006 }); g.add(e1, e2);   // the earth still to dig
    g.add(at(box(L, TH, 0.1, '#8E8E86'), 0, -D + TH / 2, -DZ + 0.05), at(box(L, 0.08, DZ, '#6A665E'), 0, -D + 0.04, -DZ / 2));
    for (let x = -L / 2 + 0.3; x < L / 2; x += 0.6) g.add(at(box(0.18, 0.06, 0.9, '#5A4A3A'), x, -D + 0.11, -DZ / 2));
    for (const z of [-0.4, -1.0]) g.add(at(box(L, 0.07, 0.06, '#9AA0A6'), 0, -D + 0.17, z));
    const lamps = []; for (let x = -L / 2 + 1.25; x < L / 2; x += 2.5) { const lm = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.1, 0.06), new THREE.MeshBasicMaterial({ color: '#3A3830', toneMapped: false }));
      lm.position.set(x, -D + 2.05, -DZ + 0.13); g.add(lm); lamps.push(lm); }
    for (let i = 0; i < 30; i++) { const px = -L / 2 + hash(i) * L, py = -0.5 - hash(i + 11) * (B - 0.8); if (py < top + 0.2 && py > -D - 0.2) continue;
      const st = new THREE.Mesh(new THREE.DodecahedronGeometry(0.1 + hash(i + 5) * 0.16, 0), mat(i % 2 ? '#8E8478' : '#A39888')); st.position.set(px, py, 0.02); st.scale.z = 0.5; g.add(st); }
    g.add(at(cyl(0.22, 0.22, L, '#7D8389', 12, { outline: 0.006 }), 0, -0.85, -0.2, 0, 0, PI / 2));
    for (let i = 0; i < 9; i++) g.add(at(cyl(0.015, 0.035, 0.6, '#4A3424', 5), -L / 2 + hash(i + 40) * L, -0.32, 0.02, 0, 0, (hash(i + 41) - 0.5) * 0.9));
    g.add(at(box(L, 0.16, 3.2, '#BDB8AE', { outline: 0.006 }), 0, 0.08, -1.6), at(box(L, 0.18, 0.2, '#9C978E'), 0, 0.09, -3.25), at(box(L, 0.04, 7, '#4A4C52'), 0, 0.02, -6.85), at(box(L, 0.16, 3, '#BDB8AE'), 0, 0.08, -11.85));
    const heads = []; for (let x = -L / 2 + 2.5; x < L / 2; x += 5) { g.add(at(cyl(0.05, 0.07, 4.2, '#2F3A3A', 8, { pivot: 'bottom' }), x, 0.16, -0.9));
      const h = new THREE.Mesh(new THREE.SphereGeometry(0.2, 10, 8), new THREE.MeshBasicMaterial({ color: '#FFE7A0', toneMapped: false })); h.position.set(x, 4.45, -0.9); g.add(h); heads.push(h); }
    const far = o.far ?? 16, wins = []; let fx = -L / 2;
    const [hA, hB] = o.frontH || [12, 16];   // the fronts' heights (lower ones leave the sky to the moon)
    for (let i = 0; fx < L / 2; i++) { const w = 7 + hash(i + 60) * 3, h = hA + hash(i + 61) * (hB - hA), nf = Math.max(1, Math.floor((h - 1.2) / 2.2));
      g.add(at(box(w - 0.1, h, 1, i % 2 ? '#EADFC8' : '#E4D6BA', { pivot: 'bottom', outline: 0.008 }), fx + w / 2, 0, -far), at(box(w - 0.1, 2.2, 1.2, '#7E8C99', { pivot: 'bottom' }), fx + w / 2, h, -far));
      for (let f = 0; f < nf; f++) for (let k = 0; k < Math.floor(w / 1.6); k++) { const m = new THREE.Mesh(new THREE.BoxGeometry(0.7, 1.1, 0.04), new THREE.MeshBasicMaterial({ color: '#FFD873', toneMapped: false }));
        m.position.set(fx + 0.9 + k * 1.6, 2.0 + f * 2.2, -far + 0.52); m.userData.lit = hash(i * 31 + f * 7 + k) < 0.6; g.add(m); wins.push(m); }
      fx += w; }
    const skyZ = -far - 12, SW = L * 1.6, SH = 60;
    const grad = (a, b) => { const cv = document.createElement('canvas'); cv.width = 8; cv.height = 256; const c = cv.getContext('2d'), gr = c.createLinearGradient(0, 0, 0, 256);
      gr.addColorStop(0, a); gr.addColorStop(1, b); c.fillStyle = gr; c.fillRect(0, 0, 8, 256); const tx = new THREE.CanvasTexture(cv); tx.colorSpace = THREE.SRGBColorSpace; return tx; };
    const night = new THREE.Mesh(new THREE.PlaneGeometry(SW, SH), new THREE.MeshBasicMaterial({ map: grad('#0B1430', '#2A3F78'), toneMapped: false })); night.position.set(0, SH / 2 - 8, skyZ); g.add(night);
    const dawn = new THREE.Mesh(new THREE.PlaneGeometry(SW, SH), new THREE.MeshBasicMaterial({ map: grad('#4C6FB8', '#FFB27A'), transparent: true, opacity: 0, toneMapped: false, depthWrite: false }));
    dawn.position.set(0, SH / 2 - 8, skyZ + 0.05); g.add(dawn);
    const stars = []; for (let i = 0; i < 80; i++) { const s = new THREE.Mesh(new THREE.CircleGeometry(0.06 + hash(i + 80) * 0.08, 6), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, toneMapped: false }));
      s.position.set((hash(i + 81) - 0.5) * SW, 12 + hash(i + 82) * 30, skyZ + 0.1); g.add(s); stars.push(s); }
    const moon = grp(new THREE.Mesh(new THREE.CircleGeometry(1.3, 24), new THREE.MeshBasicMaterial({ color: '#F6F2D8', toneMapped: false })));
    for (const [cx, cy, cr] of [[0.4, 0.3, 0.25], [-0.35, -0.2, 0.18], [0.1, -0.55, 0.14]]) moon.add(at(new THREE.Mesh(new THREE.CircleGeometry(cr, 12), new THREE.MeshBasicMaterial({ color: '#DCD6B6', toneMapped: false })), cx, cy, 0.01));
    moon.position.z = skyZ + 0.2; g.add(moon);
    const sun = new THREE.Mesh(new THREE.CircleGeometry(1.8, 28), new THREE.MeshBasicMaterial({ color: '#FFCB4A', toneMapped: false })); sun.position.z = skyZ + 0.15; g.add(sun);
    const chips = []; for (let i = 0; i < 14; i++) { const ch = new THREE.Mesh(new THREE.DodecahedronGeometry(0.07 + hash(i + 90) * 0.07, 0), mat('#9A8064')); g.add(ch); chips.push(ch); }
    const [d0, d1] = o.dawn || [t1 - 0.3, t1], mo = o.moon || [[-L / 6, 22], [0, 27], [L / 6, 17]];
    g.userData.update = t => {
      const x = dig(t), rest = L / 2 - x;
      for (const [e, y] of [[e1, top - TH / 4], [e2, -D + TH / 4]]) { e.visible = rest > 0.01; e.scale.x = Math.max(0.01, rest); e.position.set(x + rest / 2, y, -DZ / 2); }
      lamps.forEach(lm => lm.material.color.set(lm.position.x < x - 0.6 ? '#FFE8A8' : '#3A3830'));
      const dw = clamp01((t - d0) / Math.max(1e-3, d1 - d0)); dawn.material.opacity = dw; stars.forEach((s, i) => { s.visible = dw < 0.9; s.material.opacity = (1 - dw) * (0.6 + 0.4 * Math.sin(t * 3 + i)); });
      wins.forEach(m => m.material.color.set(m.userData.lit && dw < 0.6 ? '#FFD873' : '#5A6A84')); heads.forEach(h => h.material.color.set(dw < 0.75 ? '#FFE7A0' : '#9AA0A6'));
      const u = clamp01((t - t0) / Math.max(1e-3, t1 - t0)), kk = Math.min(1.999, u * 2), j = Math.floor(kk), f = kk - j;   // the moon along its three points
      moon.position.x = mo[j][0] + (mo[j + 1][0] - mo[j][0]) * f; moon.position.y = mo[j][1] + (mo[j + 1][1] - mo[j][1]) * f;
      sun.position.x = o.sunX ?? L / 5; sun.position.y = (o.sunY ?? [4, 13])[0] + ((o.sunY ?? [4, 13])[1] - (o.sunY ?? [4, 13])[0]) * eo(dw);
      const active = t >= t0 && t < t1; chips.forEach((ch, i) => { ch.visible = active; if (!active) return; const v = ((t - t0) * 2.2 + hash(i + 95)) % 1, a = 0.4 + hash(i + 96) * 0.9;
        ch.position.set(x - 0.2 - v * 1.6 * Math.cos(a), -D + 0.9 + hash(i + 97) * 1.2 + v * 2.2 * Math.sin(a) - 1.2 * v * v, -0.2 - hash(i + 98) * 0.9); ch.rotation.set(t * 9 + i, t * 7, 0); });
    };
    g.userData.update(0); return g;
  },

  // (S10, S12) The front carriage of a metro train, its nose toward +X (pivot at the floor in the middle of the nose's front): a cab end with a dark
  // windscreen, two headlights (glowing unless o.lights is false), a round line plate (o.line '10'), a buffer; the body o.len (8 m) long behind it,
  // cream with a teal band and dark side windows, in o.n (8) slices. o.crumple [t, k, dur]: from t the front k (0..1) of the body folds up like an
  // accordion in dur (0.1 s, with an overshoot), each slice squashed to o.fold (0.3) of its length and turned one way then the other; the windscreen
  // cracks
  metroNose(o) {
    const L = o.len ?? 8, W = o.w ?? 2.5, H = o.h ?? 2.3, n = o.n ?? 8, sl = L / n, g = grp(), slices = [], body = o.body || '#ECE7DA';
    for (let i = 0; i < n; i++) { const s = grp(at(box(sl, H - 0.06, W, body, { pivot: 'bottom', outline: 0.006 }), -sl / 2, 0.06, 0), at(box(sl + 0.004, 0.12, W + 0.012, o.band || '#2E8C86'), -sl / 2, 1.0, 0));
      for (const z of [-1, 1]) s.add(at(box(sl * 0.78, 0.72, 0.03, '#26323C'), -sl / 2, 1.5, z * (W / 2 + 0.01)));
      g.add(s); slices.push(s); }
    const cab = grp(at(box(0.12, H - 0.04, W, o.cab || '#E8E2D2', { pivot: 'bottom', outline: 0.008 }), 0.06, 0.04, 0), at(box(0.04, 0.86, W * 0.78, '#1E2A33'), 0.13, 1.52, 0),
      at(box(0.2, 0.22, W * 0.86, '#2A2C31', { outline: 0.006 }), 0.12, 0.32, 0), at(box(0.03, 0.12, W + 0.02, o.band || '#2E8C86'), 0.13, 1.0, 0));
    const lights = []; for (const z of [-1, 1]) { const hl = new THREE.Mesh(new THREE.CircleGeometry(0.13, 16), new THREE.MeshBasicMaterial({ color: o.lights === false ? '#8A8A80' : '#FFF6D0', toneMapped: false }));
      hl.rotation.y = PI / 2; hl.position.set(0.135, 0.72, z * W * 0.33); cab.add(hl); lights.push(hl); }
    const plate = canvasPlane(0.36, 0.36, (c, Wd, Ht) => { c.fillStyle = '#F4C430'; c.beginPath(); c.arc(Wd / 2, Ht / 2, Wd * 0.48, 0, TAU); c.fill(); c.fillStyle = '#1A1A1A'; c.textAlign = 'center'; c.textBaseline = 'middle';
      c.font = `900 ${Math.round(Ht * 0.56)}px Arial`; c.fillText(o.line ?? '10', Wd / 2, Ht * 0.54); }, { res: 128, transparent: true });
    plate.rotation.y = PI / 2; plate.position.set(0.135, 2.06, 0); cab.add(plate);
    const crack = canvasPlane(W * 0.78, 0.86, (c, Wd, Ht) => { c.clearRect(0, 0, Wd, Ht); c.strokeStyle = '#E8F2F8'; c.lineWidth = 3; const cx = Wd * 0.45, cy = Ht * 0.5;
      for (let i = 0; i < 9; i++) { let a = i / 9 * TAU + hash(i) * 0.4, x = cx, y = cy; c.beginPath(); c.moveTo(x, y); for (let k = 0; k < 5; k++) { a += (hash(i * 5 + k) - 0.5) * 0.6; x += Math.cos(a) * Wd * 0.09; y += Math.sin(a) * Ht * 0.12; c.lineTo(x, y); } c.stroke(); }
      c.beginPath(); c.arc(cx, cy, Ht * 0.12, 0, TAU); c.stroke(); }, { res: 256, transparent: true });
    crack.rotation.y = PI / 2; crack.position.set(0.16, 1.52, 0); crack.visible = false; cab.add(crack);
    // (review 1 of 63) seen from in front the folds were flat cream panels: once it crumples the cab face shows accordion pleats (bands shaded light and
    // dark with zig-zag edges) and a sawtooth roof sticks up along its top
    const pleat = canvasPlane(W * 0.98, H * 0.92, (c, Wd, Ht) => { c.clearRect(0, 0, Wd, Ht); const nb = 7, bw = Wd / nb;
      for (let i = 0; i < nb; i++) { const x0 = i * bw, gr = c.createLinearGradient(x0, 0, x0 + bw, 0); gr.addColorStop(0, i % 2 ? 'rgba(40,40,46,0.55)' : 'rgba(255,255,255,0.35)'); gr.addColorStop(1, i % 2 ? 'rgba(255,255,255,0.3)' : 'rgba(40,40,46,0.5)');
        c.fillStyle = gr; c.beginPath(); c.moveTo(x0, 0); for (let y = 0; y <= Ht; y += Ht / 10) c.lineTo(x0 + (Math.floor(y / (Ht / 10)) % 2 ? 6 : -6), y); c.lineTo(x0 + bw, Ht); c.lineTo(x0 + bw, 0); c.closePath(); c.fill();
        c.strokeStyle = 'rgba(20,20,24,0.8)'; c.lineWidth = 3; c.beginPath(); c.moveTo(x0, 0); for (let y = 0; y <= Ht; y += Ht / 10) c.lineTo(x0 + (Math.floor(y / (Ht / 10)) % 2 ? 6 : -6), y); c.stroke(); } }, { res: 256, transparent: true });
    pleat.rotation.y = PI / 2; pleat.position.set(0.15, H * 0.48, 0); pleat.visible = false; cab.add(pleat);
    const saw = new THREE.Shape(); saw.moveTo(-W / 2, 0); for (let i = 0; i <= 10; i++) saw.lineTo(-W / 2 + i * W / 10, i % 2 ? 0.28 : 0.04); saw.lineTo(W / 2, 0); saw.lineTo(-W / 2, 0);
    const roof = new THREE.Mesh(new THREE.ExtrudeGeometry(saw, { depth: 0.1, bevelEnabled: false }), mat(o.cab || '#E8E2D2')); roof.rotation.y = PI / 2; roof.position.set(0.0, H - 0.04, 0); roof.scale.y = 0.01; roof.visible = false; cab.add(roof); g.add(cab);
    g.userData.update = t => { let c = 0; const cr = o.crumple; if (cr && t >= cr[0]) c = ob((t - cr[0]) / Math.max(1e-3, cr[2] ?? 0.1));
      const K = cr ? Math.max(1, Math.round((cr[1] ?? 0.4) * n)) : 0, fold = o.fold ?? 0.3; let px = 0, pz = 0, ang = 0;
      crack.visible = c > 0.3; pleat.visible = roof.visible = c > 0.15; pleat.material.opacity = clamp01(c); roof.scale.y = Math.max(0.01, clamp01(c));
      // (stills 1 of 63) seen from in front the folds hid behind him: the folded slices also bulge and pinch in turn (a corrugated roofline above his
      // shoulders), the cab buckles back and tips, one headlight drops out of its socket on a spring
      slices.forEach((s, i) => { const k = i < K ? c : 0, sx = Math.max(0.05, 1 - k * (1 - fold)), th = i < K ? (i % 2 ? -1 : 1) * 0.4 * Math.min(1.2, k) : 0;
        s.position.set(px, 0, pz); s.rotation.y = th; s.scale.set(sx, 1 + (i % 2 ? -0.16 : 0.1) * k, 1 + (i % 2 ? 0.1 : -0.08) * k); const len = sl * sx; px -= Math.cos(th) * len; pz += Math.sin(th) * len; ang = th; });
      cab.rotation.z = 0.1 * c; cab.position.x = -0.05 * c;
      if (lights[1]) { const dr = clamp01(c), sw = cr && t >= cr[0] ? Math.sin((t - cr[0]) * 14) * Math.exp(-(t - cr[0]) * 2.5) : 0;
        lights[1].position.set(0.135 + 0.12 * dr, 0.72 - 0.32 * dr + 0.05 * sw, W * 0.33 + 0.06 * sw); }
      void ang; };
    g.userData.update(0); return g;
  },

  // (S11) A platform's departure board hung under the vault (pivot at its top middle, the face toward +Z): a black case o.w (1.9 m) x o.h (0.62) on
  // two rods o.rod (0.5 m) long, amber letters: o.title ('PROCHAIN MÉTRO') over a count of minutes that climbs from o.from (4) to o.to (3427) over
  // o.at [t0, t1], faster and faster, then blinks; o.unit ('MIN')
  departureBoard(o) {
    const W = o.w ?? 1.9, H = o.h ?? 0.62, g = grp(), cv = document.createElement('canvas'); cv.width = 768; cv.height = Math.round(768 * H / W);
    const c = cv.getContext('2d'), tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
    const face = new THREE.Mesh(new THREE.PlaneGeometry(W - 0.06, H - 0.06), new THREE.MeshBasicMaterial({ map: tex, toneMapped: false })); face.position.set(0, -H / 2, 0.041);
    g.add(at(box(W, H, 0.08, '#1A1B1F', { outline: 0.006 }), 0, -H / 2, 0), face);
    for (const s of [-1, 1]) g.add(at(cyl(0.012, 0.012, o.rod ?? 0.5, '#5A5E66', 6, { pivot: 'bottom' }), s * W * 0.35, 0, 0));
    let last = null; const [t0, t1] = o.at || [0, 1], A0 = o.from ?? 4, B0 = o.to ?? 3427;
    const fmt = v => String(Math.round(v)).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    g.userData.update = t => { const u = clamp01((t - t0) / Math.max(1e-3, t1 - t0)), v = A0 * Math.pow(B0 / A0, u * u), blink = t > t1 && Math.floor((t - t1) * 6) % 2 === 1, key = fmt(v) + (blink ? '_' : '');
      if (key === last) return; last = key;
      c.fillStyle = '#0A0A0C'; c.fillRect(0, 0, cv.width, cv.height); c.fillStyle = '#FFB22E'; c.textAlign = 'center'; c.textBaseline = 'middle';
      c.font = `bold ${Math.round(cv.height * 0.27)}px Arial`; c.fillText(o.title || 'PROCHAIN MÉTRO', cv.width / 2, cv.height * 0.27);
      if (!blink) { c.font = `bold ${Math.round(cv.height * 0.4)}px Arial`; c.fillText(`${fmt(v)} ${o.unit || 'MIN'}`, cv.width / 2, cv.height * 0.7); }
      tex.needsUpdate = true; };
    g.userData.update(0); return g;
  },

  // (S05) Cracks running out over a road from where he drills (pivot on the road at their centre): jagged dark lines out to o.r (1.6 m) and a dark hole
  // in the middle (o.hole, 0.34 m) that he sinks into, growing in jerks over o.at [t0, t1]; o.chunks (16) bits of asphalt flung up and out meanwhile
  roadCracks(o) {
    const R = o.r ?? 1.6, g = grp(), [t0, t1] = o.at || [0, 1];
    const pl = canvasPlane(2 * R, 2 * R, (c, Wd, Ht) => { c.clearRect(0, 0, Wd, Ht); const S = Wd / 2 / R; c.strokeStyle = '#1C1B1A'; c.lineCap = 'round';
      for (let i = 0; i < 10; i++) { let a = i / 10 * TAU + hash(i) * 0.5, rr = 0, x = Wd / 2, y = Ht / 2; const end = R * (0.55 + 0.45 * hash(i + 3));
        while (rr < end) { const nr = rr + 0.1 + hash(i * 7 + rr * 10) * 0.12; a += (hash(i * 13 + rr * 17) - 0.5) * 0.8; const nx = Wd / 2 + Math.cos(a) * nr * S, ny = Ht / 2 + Math.sin(a) * nr * S;
          c.lineWidth = Math.max(3.5, 18 * (1 - nr / R)); c.beginPath(); c.moveTo(x, y); c.lineTo(nx, ny); c.stroke(); x = nx; y = ny; rr = nr; } } }, { res: 512, transparent: true });   // (review 1 of 63) thick dark cracks (hairlines did not read)
    pl.rotation.x = -PI / 2; pl.position.y = 0.012; g.add(pl);
    const hole = new THREE.Mesh(new THREE.CircleGeometry(o.hole ?? 0.34, 20), new THREE.MeshBasicMaterial({ color: '#141312' })); hole.rotation.x = -PI / 2; hole.position.y = 0.016; g.add(hole);
    const chunks = []; for (let i = 0; i < (o.chunks ?? 16); i++) { const ch = new THREE.Mesh(new THREE.BoxGeometry(0.09 + hash(i + 20) * 0.08, 0.04 + hash(i + 21) * 0.03, 0.07 + hash(i + 22) * 0.07), mat(i % 3 ? '#6A6C72' : '#82848A')); g.add(ch); chunks.push(ch); }   // (review 1 of 63) flat grey slabs of asphalt (dark balls read as black marbles)
    g.userData.update = t => { const u = clamp01((t - t0) / Math.max(1e-3, t1 - t0)), j = Math.floor(u * 4) / 4 + eo((u * 4) % 1) / 4, s = u >= 1 ? 1 : 0.12 + 0.88 * j;
      pl.scale.set(s, s, 1); hole.scale.setScalar(0.35 + 0.65 * s); pl.visible = hole.visible = t >= t0;
      const active = t >= t0 && t < t1 + 0.3; chunks.forEach((ch, i) => { ch.visible = active; if (!active) return; const v = ((t - t0) * 2.4 + hash(i + 30)) % 1, a = hash(i + 31) * TAU, sp = 0.5 + hash(i + 32) * 1.1;
        ch.position.set(Math.cos(a) * (0.15 + sp * v), Math.max(0.02, (1.6 + hash(i + 33)) * v - 3.4 * v * v), Math.sin(a) * (0.15 + sp * v)); ch.rotation.set(t * 11 + i, t * 8 + i, 0); }); };
    g.userData.update(0); return g;
  },

  // (S08) A waiter's round tray (pivot at the middle of its underside): brushed steel o.r (0.19 m) with a rolled rim; carried flat at the shoulder
  serviceTray(o) {
    const R = o.r ?? 0.19, g = grp(at(cyl(R, R * 0.97, 0.01, o.color || '#C9CED4', 24, { outline: 0.003 }), 0, 0.005, 0));
    const rim = new THREE.Mesh(new THREE.TorusGeometry(R, 0.008, 6, 28), mat(o.color || '#C9CED4')); rim.rotation.x = PI / 2; rim.position.y = 0.012; g.add(rim);
    return g;
  },

  // (S09) A pebble falling from the vault (pivot at its centre): a grey stone o.r (0.045 m)
  pebble(o) { const m = new THREE.Mesh(new THREE.DodecahedronGeometry(o.r ?? 0.045, 0), mat(o.color || '#8C8478')); m.scale.y = 0.75; return grp(m); },

  // (S11) A plain block (pivot at its centre): o.w x o.h x o.d (1 m) of o.color, matte; a ceiling, an end wall, a black tunnel mouth
  slab(o) { const m = box(o.w ?? 1, o.h ?? 1, o.d ?? 1, o.color || '#3A3C42', o.outline ? { outline: o.outline } : {}); if (o.noShadow) m.traverse(n => { n.castShadow = false; }); return grp(m); },
};
