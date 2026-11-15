// « Le champagne » (story 68, cycle 30): this man opened the champagne and the cork never came down. It went through the ceiling, then through the
// neighbour's living room; she complained, the police opened an inquiry, the town hall closed the sky, the air force gave chase and lost; it went
// into orbit, the scientists named it Bouchon 1, the television has a better picture since, the government made it a national treasure, the other
// countries claimed it, he got a bill for taking up space; yesterday it came down, right into his glass. The champagne was flat.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = PI * 2;
const clamp01 = x => Math.max(0, Math.min(1, x));
const eo = x => 1 - Math.pow(1 - clamp01(x), 3);
const hash = n => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const inWin = (w, t) => (w || []).some(([a, b]) => t >= a && t < b);
const lam = (color, opacity = 1) => new THREE.MeshLambertMaterial({ color, transparent: opacity < 1, opacity, depthWrite: opacity >= 1 });
const basic = (color, opacity = 1) => new THREE.MeshBasicMaterial({ color, transparent: opacity < 1, opacity, depthWrite: opacity >= 1 });
// keys [[t, v], ...] eased in and out between them, or a plain number
function keyAt(k, t, d = 0) {
  if (k == null) return d; if (typeof k === 'number') return k; if (!k.length) return d; if (t <= k[0][0]) return k[0][1];
  for (let i = 0; i < k.length - 1; i++) { const [t0, v0] = k[i], [t1, v1] = k[i + 1]; if (t < t1) { const u = (t - t0) / Math.max(1e-6, t1 - t0); return v0 + (v1 - v0) * u * u * (3 - 2 * u); } }
  return k[k.length - 1][1];
}
function canvasTex(w, h, draw) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

// the cork itself (shared by the cork prop, the flute it lands in and the control-room screen): 5 cm tall, the cap toward +Y
function corkMesh(o = {}) {
  const body = grp(), C = o.color || '#C9A26B', ol = { outline: 0.0015 };
  body.add(at(cyl(0.0118, 0.0128, 0.026, C, 12, ol), 0, -0.011, 0));                          // the stem (narrower at its foot: squeezed in the neck)
  body.add(at(cyl(0.0165, 0.0165, 0.012, C, 14, ol), 0, 0.008, 0));                           // the mushroom
  const dome = new THREE.Mesh(new THREE.SphereGeometry(0.0165, 14, 6, 0, TAU, 0, PI / 2), lam(C)); dome.scale.y = 0.45; dome.position.y = 0.014; body.add(dome);
  body.add(at(cyl(0.0172, 0.0172, 0.0025, '#D9B44A', 14), 0, 0.0205, 0));                      // the gold cap
  const wire = '#8C9096';
  body.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.0168, 0.0011, 4, 18), lam(wire)), 0, 0.004, 0, PI / 2, 0, 0));
  for (let i = 0; i < 4; i++) { const a = i / 4 * TAU + 0.4; body.add(at(cyl(0.0008, 0.0008, 0.018, wire, 4), Math.cos(a) * 0.0166, 0.012, Math.sin(a) * 0.0166)); }
  for (let i = 0; i < 12; i++) {                                                              // dark specks in the cork
    const a = hash(i) * TAU, y = -0.021 + hash(i + 9) * 0.03, rr = (y > 0.002 ? 0.0166 : 0.0124) + 0.0004, d = new THREE.Mesh(new THREE.CircleGeometry(0.0015, 5), lam('#8E6A40'));
    d.position.set(Math.cos(a) * rr, y, Math.sin(a) * rr); d.lookAt(Math.cos(a) * 2, y, Math.sin(a) * 2); body.add(d);
  }
  return body;
}

export const CHAMPAGNE_PROPS = {
  // A champagne cork (pivot at its middle, the cap toward +Y), 5 cm tall at scale 1 (scale it up for the far shots). o.spin (turns per second about
  // its own Y), o.tumble (rad per second end over end); o.trail [[t0, t1], ...]: a white streak behind it (toward -Y); o.fire [[t0, t1], ...]: a hot
  // halo and flames toward -Y (set its rotation so that +Y points where it goes); o.panels: two blue solar panels and an antenna (the satellite it
  // became); o.hideAt: gone from then on (it went into the glass, which shows its own)
  cork(o) {
    const g = grp(), body = corkMesh(o); g.add(body);
    if (o.panels) {
      for (const s of [-1, 1]) {
        body.add(at(cyl(0.0012, 0.0012, 0.022, '#8C9096', 4), s * 0.026, -0.006, 0, 0, 0, PI / 2), at(box(0.042, 0.0016, 0.024, '#2F62B5', { outline: 0.0012 }), s * 0.058, -0.006, 0));
        for (let j = 1; j < 4; j++) body.add(at(box(0.0009, 0.002, 0.024, '#9CC3F0'), s * (0.037 + j * 0.0105), -0.006, 0));
      }
      body.add(at(cyl(0.0007, 0.0007, 0.03, '#8C9096', 4), 0, 0.037, 0), at(new THREE.Mesh(new THREE.SphereGeometry(0.0024, 6, 4), basic('#FF4A3A')), 0, 0.053, 0));
    }
    const trail = grp();
    for (let i = 0; i < 3; i++) { const L = 0.1 + i * 0.12, c = new THREE.Mesh(new THREE.ConeGeometry(0.0115 - i * 0.002, L, 8, 1, true), basic('#FFFFFF', 0.5 - i * 0.14)); c.rotation.x = PI; c.position.y = -0.022 - L / 2; trail.add(c); }
    g.add(trail);
    const fire = grp(), fl = [['#FFF4B0', 0.013, 0.08], ['#FFB040', 0.018, 0.15], ['#FF5A24', 0.023, 0.24]].map(([c, r, L], i) => {
      const m = new THREE.Mesh(new THREE.ConeGeometry(r, L, 8, 1, true), basic(c, 0.92 - i * 0.16)); m.rotation.x = PI; m.userData.L = L; fire.add(m); return m; });
    const halo = new THREE.Mesh(new THREE.SphereGeometry(0.026, 12, 8), new THREE.MeshBasicMaterial({ color: '#FF8A3A', transparent: true, opacity: 0.45, depthWrite: false, blending: THREE.AdditiveBlending }));
    fire.add(halo); g.add(fire);
    g.userData.update = t => {
      g.visible = o.hideAt == null || t < o.hideAt;
      body.rotation.set((o.tumble || 0) * t, (o.spin || 0) * TAU * t, 0);
      trail.visible = inWin(o.trail, t); const f = inWin(o.fire, t); fire.visible = f;
      if (f) { fl.forEach((m, i) => { const k = 1 + 0.25 * Math.sin(t * 41 + i * 2.1) + 0.15 * Math.sin(t * 67 + i); m.scale.set(1, k, 1); m.position.y = -0.006 - m.userData.L * k / 2; }); halo.scale.setScalar(1 + 0.12 * Math.sin(t * 53)); }
    };
    g.userData.update(0); return g;
  },

  // A champagne flute (pivot at its foot): a foot, a stem and a tall bowl of clear glass, 0.2 m in all; the wine in it, o.level (0..1 of the bowl,
  // or keys [[t, level]]), bubbles rising in it until o.flatAt (then none, and the wine a duller gold: flat); o.lastBubble t: one slow bubble that
  // swells at the top and pops (blop); o.splashAt: a cork drops in: a crown of drops leaps out, the surface heaves, the cork bobs in it after
  // (o.corkScale 1); userData.grip: the middle of the stem
  flute(o) {
    const g = grp(), FH = 0.11, BR0 = 0.015, BR1 = 0.029, BY = 0.135, Y0 = BY - FH / 2;
    const glass = new THREE.MeshLambertMaterial({ color: '#EAF7FF', transparent: true, opacity: 0.3, side: THREE.DoubleSide, depthWrite: false });
    g.add(at(new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.032, 0.004, 18), glass), 0, 0.002, 0), at(new THREE.Mesh(new THREE.CylinderGeometry(0.0034, 0.0034, 0.072, 6), glass), 0, 0.04, 0));
    const bowl = new THREE.Mesh(new THREE.CylinderGeometry(BR1, BR0, FH, 20, 1, true), glass); bowl.position.y = BY; g.add(bowl);
    const bot = new THREE.Mesh(new THREE.ConeGeometry(BR0, 0.012, 20, 1, true), glass); bot.rotation.x = PI; bot.position.y = Y0 - 0.006; g.add(bot);
    const rim = new THREE.Mesh(new THREE.TorusGeometry(BR1, 0.0011, 4, 26), lam('#FFFFFF', 0.85)); rim.rotation.x = PI / 2; rim.position.y = BY + FH / 2; g.add(rim);
    const WINE = new THREE.Color('#F2C94E'), FLAT = new THREE.Color('#CDB27A');
    const wm = new THREE.MeshLambertMaterial({ color: WINE.clone(), transparent: true, opacity: 0.88 }), wine = new THREE.Mesh(new THREE.BufferGeometry(), wm); g.add(wine);
    const topM = new THREE.MeshLambertMaterial({ color: '#FBE6A0', transparent: true, opacity: 0.92 }), top = new THREE.Mesh(new THREE.CircleGeometry(1, 20), topM); top.rotation.x = -PI / 2; g.add(top);
    const rAt = h => BR0 + (BR1 - BR0) * clamp01(h / FH) - 0.0012;
    let lastH = -1; const setLevel = lv => { const h = Math.max(0.002, FH * 0.96 * clamp01(lv)); if (Math.abs(h - lastH) < 0.0005) return; lastH = h;
      wine.geometry.dispose(); wine.geometry = new THREE.CylinderGeometry(rAt(h), rAt(0), h, 20); wine.position.y = Y0 + h / 2; top.scale.setScalar(rAt(h)); top.position.y = Y0 + h + 0.0004; };
    const bub = []; for (let i = 0; i < 14; i++) { const m = new THREE.Mesh(new THREE.SphereGeometry(0.0021, 6, 4), basic('#FFFDF0', 0.85)); g.add(m); bub.push({ m, ph: hash(i + 1), per: 0.7 + 0.5 * hash(i + 21), a: hash(i + 41) * TAU, r: 0.35 + 0.5 * hash(i + 61) }); }
    const last = new THREE.Mesh(new THREE.SphereGeometry(0.003, 8, 6), basic('#FFFDF0', 0.9)); g.add(last);
    const drops = []; for (let i = 0; i < 12; i++) { const m = new THREE.Mesh(new THREE.SphereGeometry(0.0042, 6, 4), lam('#F7DC86')); g.add(m); drops.push({ m, a: i / 12 * TAU + hash(i + 5), up: 0.55 + 0.4 * hash(i + 15), out: 0.18 + 0.2 * hash(i + 25) }); }
    const crown = new THREE.Mesh(new THREE.TorusGeometry(1, 0.08, 4, 20), lam('#FCEBB0', 0.9)); crown.rotation.x = PI / 2; g.add(crown);
    const ck = corkMesh(); ck.scale.setScalar(o.corkScale ?? 1); g.add(ck);
    g.userData.grip = [0, 0.04, 0];
    g.userData.update = t => {
      setLevel(keyAt(o.level, t, 0.8)); const sy = top.position.y, h = sy - Y0;
      const fl = o.flatAt == null ? 0 : clamp01((t - o.flatAt) / 0.3); wm.color.copy(WINE).lerp(FLAT, fl); topM.color.set(fl > 0.5 ? '#E2CF9E' : '#FBE6A0');
      for (const b of bub) { const u = (t / b.per + b.ph) % 1, rr = rAt(h * u) * b.r; b.m.position.set(Math.cos(b.a) * rr, Y0 + 0.004 + (h - 0.006) * u, Math.sin(b.a) * rr); b.m.visible = h > 0.01 && fl < 0.5; b.m.scale.setScalar(0.7 + 0.6 * u); }
      if (o.lastBubble != null) { const u = (t - o.lastBubble + 0.9) / 0.9; last.visible = u >= 0 && u < 1.08 && h > 0.01; if (last.visible) { const k = clamp01(u); last.position.set(0.003, Y0 + 0.004 + (h - 0.004) * k, 0); last.scale.setScalar(u < 1 ? 0.8 + 0.4 * k : 1.9); } }
      else last.visible = false;
      const s = o.splashAt == null ? -1 : t - o.splashAt;
      for (const d of drops) { const on = s >= 0 && s < 0.4; d.m.visible = on; if (on) d.m.position.set(Math.cos(d.a) * (0.02 + d.out * s), sy + d.up * s - 4.9 * s * s, Math.sin(d.a) * (0.02 + d.out * s)); }
      crown.visible = s >= 0 && s < 0.22; if (crown.visible) { const k = eo(s / 0.22); crown.scale.set(0.012 + 0.03 * k, 0.012 + 0.03 * k, 1); crown.position.y = sy + 0.008 * Math.sin(PI * k); crown.material.opacity = 0.9 * (1 - k); }
      top.position.y = sy + (s >= 0 ? 0.004 * Math.sin(s * 34) * Math.exp(-5 * s) : 0);
      ck.visible = s >= 0; if (s >= 0) { ck.position.set(0.002, sy + 0.012 + 0.006 * Math.sin(s * 15) * Math.exp(-3.5 * s) - 0.03 * Math.max(0, 0.06 - s) / 0.06, 0); ck.rotation.set(0.15, 0, 0.45 + 0.25 * Math.sin(s * 9) * Math.exp(-3 * s)); }
    };
    g.userData.update(0); return g;
  },

  // Champagne foam gushing from a bottle's mouth (pivot at the mouth, it shoots along +Y): between o.at [t0, t1] blobs leave fast, spread and fall
  // back under gravity, each one lower than the last (the gush dies down); o.len (1.2 m: how high the first go), o.spread (0.3), o.size (0.045),
  // o.n (40), o.color ('#FFF6DC'); one blob in five is the colour of the wine
  foamJet(o) {
    const g = grp(), n = o.n ?? 40, [t0, t1] = o.at || [0, 1], L = o.len ?? 1.2, sp = o.spread ?? 0.3, sz = o.size ?? 0.045, G = 9.8;
    const m1 = lam(o.color || '#FFF6DC'), m2 = lam('#F3DE9A'), geo = new THREE.IcosahedronGeometry(1, 1), B = [];
    for (let i = 0; i < n; i++) {
      const m = new THREE.Mesh(geo, i % 5 === 4 ? m2 : m1); m.castShadow = false; g.add(m);
      const tb = t0 + (t1 - t0) * (i / n), die = Math.pow(1 - i / n, 0.8), v = Math.sqrt(2 * G * L * Math.max(0.12, die)), a = hash(i) * TAU, s = sp * (0.3 + 0.7 * hash(i + 7));
      B.push({ m, tb, v, vx: Math.cos(a) * s * v * 0.5, vz: Math.sin(a) * s * v * 0.5, r: sz * (0.6 + 0.8 * hash(i + 11)) });
    }
    g.userData.update = t => {
      for (const b of B) { const u = t - b.tb; if (u < 0 || u > 1.4) { b.m.visible = false; continue; } const y = b.v * u - 0.5 * G * u * u; if (y < -1.6) { b.m.visible = false; continue; }
        b.m.visible = true; b.m.position.set(b.vx * u, y, b.vz * u); const k = Math.min(1, u / 0.06) * (1 - 0.4 * clamp01((u - 0.5) / 0.9)), st = 1 + 0.8 * Math.max(0, 1 - u * 5);
        b.m.scale.set(b.r * k, b.r * k * st, b.r * k); }
    };
    g.userData.update(0); return g;
  },

  // A hole punched through a ceiling, a floor or a roof (a flat decal facing +Z, pivot at its centre: lay it with rot): a ragged hole the size of
  // the cork's head (o.r 0.1), a broken plaster rim, its inside o.inner ('#2A2A30'; the sky through it: '#8EC5EA'), cracks out to 2.2 r; nothing
  // before o.at, then it bursts open in two frames with chips and a puff of plaster (o.chip) flying out along +Z; o.fall: 1 (a ceiling: they fall
  // away along +Z) or -1 (a floor: they leap up and drop back)
  corkHole(o) {
    const R = o.r ?? 0.1, g = grp(), S = R * 4.6;
    const tex = canvasTex(256, 256, (x, W) => {
      const c = W / 2, rh = W * R / S, jag = (r, k, i) => r * (1 + k * (hash(i * 3.1) - 0.5));
      // (review 1 of 68) o.plaster: five short thin cracks and a wide light broken edge (nine thick tapering cracks round a dark disc read as a spider)
      const PL = !!o.plaster, nC = PL ? 5 : 9, lw = PL ? 2.2 : 4, reach = PL ? 1.25 : 1.6, extra = PL ? 0.25 : 0.6;
      x.strokeStyle = PL ? 'rgba(120,108,96,0.8)' : 'rgba(70,62,56,0.95)'; x.lineCap = 'round';
      for (let i = 0; i < nC; i++) { const a0 = i / nC * TAU + 0.5 * hash(i); let r = rh * (PL ? 1.3 : 1.05), a = a0; x.lineWidth = lw; x.beginPath(); x.moveTo(c + Math.cos(a) * r, c + Math.sin(a) * r);
        while (r < rh * (reach + extra * hash(i + 30)) * (PL ? 1.25 : 1)) { r += rh * 0.16; a += 0.22 * (hash(i * 7 + r) - 0.5); x.lineTo(c + Math.cos(a) * r, c + Math.sin(a) * r); } x.stroke(); }
      x.fillStyle = o.rim || (PL ? '#FBF6EC' : '#EEE6D6'); x.beginPath(); for (let i = 0; i < 22; i++) { const a = i / 22 * TAU, r = jag(rh * (PL ? 1.32 : 1.18), PL ? 0.34 : 0.22, i + 50); i ? x.lineTo(c + Math.cos(a) * r, c + Math.sin(a) * r) : x.moveTo(c + Math.cos(a) * r, c + Math.sin(a) * r); } x.fill();
      x.fillStyle = o.inner || '#2A2A30'; x.strokeStyle = '#3A322C'; x.lineWidth = 6; x.beginPath();
      for (let i = 0; i < 18; i++) { const a = i / 18 * TAU, r = jag(rh, 0.18, i + 90); i ? x.lineTo(c + Math.cos(a) * r, c + Math.sin(a) * r) : x.moveTo(c + Math.cos(a) * r, c + Math.sin(a) * r); } x.closePath(); x.fill(); x.stroke();
    });
    const dec = new THREE.Mesh(new THREE.PlaneGeometry(S, S), new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -4, polygonOffsetUnits: -4 }));
    dec.renderOrder = 2; g.add(dec);
    const chips = [], CH = o.chip || '#E6DDCC', fall = o.fall ?? 1;
    for (let i = 0; i < 12; i++) { const m = at(box(0.025 + 0.02 * hash(i + 3), 0.006, 0.02 + 0.015 * hash(i + 5), CH), 0, 0, 0); g.add(m); const a = hash(i + 7) * TAU; chips.push({ m, vx: Math.cos(a) * (0.4 + 0.5 * hash(i + 9)), vy: Math.sin(a) * (0.4 + 0.5 * hash(i + 9)), vz: 0.6 + 1.2 * hash(i + 11), sp: 6 + 8 * hash(i + 13) }); }
    const puffs = []; for (let i = 0; i < 6; i++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 1), lam(CH, 0.85)); m.castShadow = false; g.add(m); const a = i / 6 * TAU; puffs.push({ m, dx: Math.cos(a), dy: Math.sin(a) }); }
    g.userData.update = t => {
      const u = o.at == null ? 9 : t - o.at; dec.visible = u >= 0; if (u >= 0) dec.scale.setScalar(u < 0.07 ? 0.3 + 0.85 * eo(u / 0.07) : 1 + 0.05 * Math.max(0, 1 - (u - 0.07) / 0.1));
      for (const c of chips) { const on = u >= 0 && u < 0.9; c.m.visible = on; if (on) { const z = fall > 0 ? c.vz * u + 2.5 * u * u : c.vz * 1.8 * u - 4.9 * u * u; c.m.position.set(c.vx * u, c.vy * u, Math.max(-0.02, z)); c.m.rotation.set(c.sp * u, c.sp * 0.7 * u, 0); } }
      for (const p of puffs) { const on = u >= 0 && u < 0.7; p.m.visible = on; if (on) { const k = eo(u / 0.7); p.m.position.set(p.dx * R * (0.6 + 1.6 * k), p.dy * R * (0.6 + 1.6 * k), R * (0.3 + 1.2 * k)); p.m.scale.setScalar(R * (0.5 + 0.9 * k)); p.m.material.opacity = 0.85 * (1 - k * k); } }
    };
    g.userData.update(0); return g;
  },

  // A soup plate on a table (pivot at its foot): white with a blue rim, orange soup, a spoon resting in it; at o.burstAt something comes up through
  // it: the plate leaps and turns over, the soup jumps up in blobs and noodles (o.up: 0.9 m) and comes down round it, the blobs that fall back
  // stopping at o.floor (-0.75: the floor under a table top) as splats
  soupBowl(o) {
    const g = grp(), plate = grp(), SOUP = o.soup || '#E39A3A';
    plate.add(at(cyl(0.11, 0.07, 0.035, '#F4F2EC', 18, { outline: 0.003 }), 0, 0.0175, 0), at(new THREE.Mesh(new THREE.TorusGeometry(0.108, 0.006, 4, 24), lam('#3A6FB5')), 0, 0.034, 0, PI / 2, 0, 0));
    const soup = at(cyl(0.098, 0.098, 0.004, SOUP, 18), 0, 0.03, 0); plate.add(soup);
    plate.add(at(box(0.012, 0.004, 0.16, '#C9CDD2', { outline: 0.0015 }), 0.05, 0.05, 0.03, 0.35, 0.5, 0), at(new THREE.Mesh(new THREE.SphereGeometry(0.022, 8, 5), lam('#C9CDD2')), 0.02, 0.034, -0.02));
    g.add(plate);
    const up = o.up ?? 0.9, G = 9.8, v0 = Math.sqrt(2 * G * up), floor = o.floor ?? -0.75, bits = [], ngeo = new THREE.TorusGeometry(0.035, 0.006, 4, 10, PI * 1.4);
    for (let i = 0; i < 18; i++) {
      const noodle = i % 4 === 3, m = noodle ? new THREE.Mesh(ngeo, lam('#F2D27A')) : new THREE.Mesh(new THREE.IcosahedronGeometry(1, 1), lam(SOUP)); m.castShadow = false; g.add(m);
      const a = hash(i + 2) * TAU, k = 0.45 + 0.55 * hash(i + 4); bits.push({ m, noodle, vy: v0 * k, vx: Math.cos(a) * (0.25 + 0.5 * hash(i + 6)), vz: Math.sin(a) * (0.25 + 0.5 * hash(i + 6)), r: 0.018 + 0.02 * hash(i + 8), sp: 5 + 8 * hash(i + 10) });
    }
    g.userData.update = t => {
      const u = o.burstAt == null ? -1 : t - o.burstAt;
      if (u < 0) { plate.position.set(0, 0, 0); plate.rotation.set(0, 0, 0); soup.visible = true; }
      else { const k = Math.min(u, 0.62), y = 2.4 * k - 4.9 * k * k; plate.position.set(0.25 * k, Math.max(0, y), 0.1 * k); plate.rotation.set(0, 0, -PI * eo(k / 0.62)); soup.visible = u < 0.05; }
      for (const b of bits) {
        if (u < 0) { b.m.visible = false; continue; } b.m.visible = true; const y = 0.03 + b.vy * u - 0.5 * G * u * u, landed = y <= floor;
        const tl = landed ? (b.vy + Math.sqrt(b.vy * b.vy + 2 * G * (0.03 - floor))) / G : u;
        b.m.position.set(b.vx * tl, Math.max(floor, y), b.vz * tl);
        if (b.noodle) b.m.rotation.set(b.sp * Math.min(u, tl), b.sp * 0.6 * Math.min(u, tl), 0); else if (landed) b.m.scale.set(b.r * 1.6, b.r * 0.3, b.r * 1.6); else b.m.scale.setScalar(b.r * Math.min(1, u / 0.05));
      }
    };
    g.userData.update(0); return g;
  },

  // Splashed muck on a head (attach it to the head joint: pivot at the joint, the face toward +Z): blobs of o.color stuck on the face and the hair
  // from o.at (they land over 0.08 s), drips running down from them, and o.noodle: a noodle draped over the top of the head (the soup); o.w / o.h /
  // o.d: the head box it sits on (0.24 x 0.5 x 0.17 above the joint: the hero's); o.n (9 blobs)
  gunk(o) {
    const g = grp(), W = o.w ?? 0.24, H = o.h ?? 0.5, D = o.d ?? 0.17, C = o.color || '#E39A3A', blobs = [], drips = [], geo = new THREE.IcosahedronGeometry(1, 1);
    const n = o.n ?? 9;
    for (let i = 0; i < n; i++) {
      const onTop = i % 3 === 0, x = (hash(i + 1) - 0.5) * W * 0.85, y = onTop ? H + 0.005 : H * (0.18 + 0.75 * hash(i + 3)), z = onTop ? (hash(i + 5) - 0.5) * D * 0.8 : D / 2 + 0.004;
      const m = new THREE.Mesh(geo, lam(C)); m.castShadow = false; const r = 0.018 + 0.02 * hash(i + 7); m.userData = { x, y, z, r, onTop }; g.add(m); blobs.push(m);
      if (!onTop && i % 2) { const d = new THREE.Mesh(geo, lam(C)); d.castShadow = false; g.add(d); drips.push({ d, x, y, z, per: 0.8 + 0.6 * hash(i + 9), ph: hash(i + 11) }); }
    }
    let nd = null;
    if (o.noodle) { const pts = [[-W * 0.55, H * 0.72, 0.02], [-W * 0.3, H + 0.03, 0.03], [0.02, H + 0.035, 0.01], [W * 0.3, H + 0.025, -0.01], [W * 0.56, H * 0.8, 0.0], [W * 0.6, H * 0.55, 0.02]].map(p => new THREE.Vector3(...p));
      nd = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 24, 0.008, 5, false), lam('#F2D27A')); g.add(nd); }
    g.userData.update = t => {
      const u = o.at == null ? 9 : t - o.at, k = clamp01(u / 0.08);
      for (const m of blobs) { const { x, y, z, r, onTop } = m.userData; m.visible = u >= 0; if (u >= 0) { m.position.set(x, y, z); m.scale.set(r * (0.6 + 0.6 * k), onTop ? r * 0.5 * k + 0.002 : r * (0.6 + 0.6 * k), onTop ? r * k + 0.002 : r * 0.35 * k + 0.002); } }
      for (const d of drips) { const on = u > 0.1; d.d.visible = on; if (on) { const p = ((u - 0.1) / d.per + d.ph) % 1; d.d.position.set(d.x, d.y - 0.14 * p, d.z + 0.003); d.d.scale.set(0.007, 0.012 + 0.006 * p, 0.005); } }
      if (nd) nd.visible = u >= 0;
    };
    g.userData.update(0); return g;
  },

  // A magnifying glass (pivot at the end of its handle, the lens up +Y facing +Z): a dark wooden handle, a brass ring, a pale glass disc with a
  // white glint; o.r (0.07 m)
  magnifier(o) {
    const R = o.r ?? 0.07, g = grp(at(cyl(0.012, 0.014, 0.13, '#3B2A20', 8, { outline: 0.002 }), 0, 0.065, 0), at(cyl(0.015, 0.015, 0.02, '#B8902A', 8), 0, 0.135, 0));
    g.add(at(new THREE.Mesh(new THREE.TorusGeometry(R, 0.007, 6, 28), lam('#C9A23A')), 0, 0.145 + R, 0));
    g.add(at(new THREE.Mesh(new THREE.CircleGeometry(R, 28), new THREE.MeshBasicMaterial({ color: '#DDF0FF', transparent: true, opacity: 0.32, side: THREE.DoubleSide, depthWrite: false })), 0, 0.145 + R, 0));
    g.add(at(new THREE.Mesh(new THREE.RingGeometry(R * 0.55, R * 0.68, 12, 1, 2.2, 0.9), new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.75, side: THREE.DoubleSide, depthWrite: false })), 0, 0.145 + R, 0.002));
    g.userData.grip = [0, 0.05, 0]; return g;
  },

  // A television on its stand (pivot at the floor, the screen toward +Z): the picture is snow until o.clearAt, then, after a roll of two frames, a
  // football match, sharp and bright; rabbit-ear antennas on top (o.antenna: false: none); 0.9 x 0.66 x 0.55 like tv() in props.js
  oldTv(o) {
    const g = grp(at(box(0.9, 0.66, 0.55, '#5A3E2A', { pivot: 'bottom', outline: 0.01 }), 0, 0.3, 0), at(box(0.7, 0.3, 0.45, '#3B2A20', { pivot: 'bottom' }), 0, 0, 0));
    g.add(at(box(0.68, 0.52, 0.02, '#15161A'), -0.06, 0.63, 0.276), at(cyl(0.035, 0.035, 0.03, '#E8DCC0', 8), 0.36, 0.75, 0.28, PI / 2), at(cyl(0.035, 0.035, 0.03, '#E8DCC0', 8), 0.36, 0.6, 0.28, PI / 2));
    const noise = canvasTex(128, 96, (x, W, H) => { const im = x.createImageData(W, H); for (let i = 0; i < W * H; i++) { const v = 40 + 200 * hash(i * 1.7 + 3); im.data[i * 4] = im.data[i * 4 + 1] = im.data[i * 4 + 2] = v; im.data[i * 4 + 3] = 255; } x.putImageData(im, 0, 0); });
    noise.wrapS = noise.wrapT = THREE.RepeatWrapping; noise.repeat.set(0.5, 0.5); noise.magFilter = THREE.NearestFilter;
    const snow = new THREE.Mesh(new THREE.PlaneGeometry(0.62, 0.46), new THREE.MeshBasicMaterial({ map: noise })); snow.position.set(-0.06, 0.63, 0.288); g.add(snow);
    const pic = canvasPlane(0.62, 0.46, (x, W, H) => {
      const sky = x.createLinearGradient(0, 0, 0, H * 0.28); sky.addColorStop(0, '#2C3E66'); sky.addColorStop(1, '#5A6E9A'); x.fillStyle = sky; x.fillRect(0, 0, W, H * 0.28);
      for (let i = 0; i < 60; i++) { x.fillStyle = ['#D94A3A', '#F2F2F2', '#3A62B5', '#F2C94E'][i % 4]; x.fillRect(W * hash(i + 2), H * (0.14 + 0.12 * hash(i + 4)), W * 0.012, H * 0.03); }
      x.fillStyle = '#3F9A4A'; x.fillRect(0, H * 0.28, W, H * 0.72); x.fillStyle = '#4BAA56'; for (let i = 0; i < 6; i++) x.fillRect(0, H * (0.28 + i * 0.12), W, H * 0.06);
      x.strokeStyle = '#F4FAF4'; x.lineWidth = W * 0.01; x.beginPath(); x.moveTo(W * 0.08, H * 0.95); x.lineTo(W * 0.24, H * 0.32); x.lineTo(W * 0.76, H * 0.32); x.lineTo(W * 0.92, H * 0.95); x.stroke();
      x.beginPath(); x.moveTo(W * 0.5, H * 0.32); x.lineTo(W * 0.5, H * 0.95); x.stroke(); x.beginPath(); x.ellipse(W * 0.5, H * 0.6, W * 0.11, H * 0.07, 0, 0, TAU); x.stroke();
      [[0.32, 0.55, '#C8352A'], [0.42, 0.72, '#C8352A'], [0.6, 0.5, '#2C4A9A'], [0.7, 0.68, '#2C4A9A'], [0.55, 0.62, '#2C4A9A']].forEach(([px, py, c]) => { x.fillStyle = c; x.fillRect(W * px - W * 0.012, H * py - H * 0.06, W * 0.024, H * 0.06); x.fillStyle = '#E8B48A'; x.beginPath(); x.arc(W * px, H * py - H * 0.07, W * 0.012, 0, TAU); x.fill(); });
      x.fillStyle = '#FFFFFF'; x.beginPath(); x.arc(W * 0.5, H * 0.66, W * 0.012, 0, TAU); x.fill();
      x.fillStyle = 'rgba(10,20,40,0.8)'; x.fillRect(W * 0.04, H * 0.04, W * 0.3, H * 0.09); x.fillStyle = '#FFFFFF'; x.font = `bold ${H * 0.07}px Arial`; x.fillText('2 - 1', W * 0.12, H * 0.11);
    }, { res: 256 });
    pic.material = new THREE.MeshBasicMaterial({ map: pic.material.map }); pic.position.set(-0.06, 0.63, 0.289); g.add(pic);
    let ant = null; if (o.antenna !== false) { ant = grp(at(cyl(0.05, 0.06, 0.04, '#2A2A2E', 8), 0, 0.02, 0)); for (const s of [-1, 1]) ant.add(at(cyl(0.004, 0.004, 0.5, '#B8BCC2', 4, { pivot: 'bottom' }), 0, 0.03, 0, 0, 0, s * 0.45)); ant.position.set(0.05, 0.96, 0); g.add(ant); }
    g.userData.update = t => {
      const f = Math.floor(t * 30), c = o.clearAt == null ? 1e9 : o.clearAt, roll = t >= c && t < c + 0.07;
      snow.visible = t < c + 0.07; noise.offset.set(hash(f * 1.3), hash(f * 2.9 + 1)); pic.visible = t >= c;
      if (roll) { pic.position.y = 0.63 + 0.46 * (1 - (t - c) / 0.07) * 0.5; snow.position.y = pic.position.y - 0.46; } else { pic.position.y = 0.63; snow.position.y = 0.63; }
      if (ant) ant.rotation.z = t < c ? 0.08 * Math.sin(t * 9) : 0;
    };
    g.userData.update(0); return g;
  },

  // The big screen of a control room (pivot at its bottom centre, facing +Z): o.w x o.h (2.4 x 1.35), a dark blue field with the Earth drawn in the
  // middle and a dotted orbit round it; a small gold cork goes round the orbit (o.period 3 s); from o.nameAt the name o.name ('BOUCHON 1') springs
  // up under it in big yellow letters
  orbitScreen(o) {
    const W = o.w ?? 2.4, H = o.h ?? 1.35, g = grp(at(box(W + 0.12, H + 0.12, 0.08, '#1F2228', { outline: 0.008 }), 0, H / 2, -0.05));
    const bg = canvasPlane(W, H, (x, cw, ch) => {
      x.fillStyle = '#0D2044'; x.fillRect(0, 0, cw, ch); x.strokeStyle = 'rgba(120,170,255,0.18)'; x.lineWidth = 2; for (let i = 1; i < 12; i++) { x.beginPath(); x.moveTo(cw * i / 12, 0); x.lineTo(cw * i / 12, ch); x.stroke(); } for (let i = 1; i < 7; i++) { x.beginPath(); x.moveTo(0, ch * i / 7); x.lineTo(cw, ch * i / 7); x.stroke(); }
      const ex = cw / 2, ey = ch * 0.42, er = ch * 0.17; x.fillStyle = '#2F7FD0'; x.beginPath(); x.arc(ex, ey, er, 0, TAU); x.fill(); x.fillStyle = '#4FB25A';
      [[-0.3, -0.2, 0.35], [0.25, 0.1, 0.4], [-0.1, 0.45, 0.25]].forEach(([dx, dy, s]) => { x.beginPath(); x.ellipse(ex + dx * er, ey + dy * er, er * s, er * s * 0.6, 0.4, 0, TAU); x.fill(); });
      x.setLineDash([10, 10]); x.strokeStyle = '#F2E2A0'; x.lineWidth = 4; x.beginPath(); x.ellipse(ex, ey, cw * 0.32, ch * 0.3, 0, 0, TAU); x.stroke(); x.setLineDash([]);
    }, { res: 512, emissive: 0.85 });
    bg.position.set(0, H / 2, 0); g.add(bg);
    const ck = corkMesh(); ck.scale.setScalar(H * 1.6); g.add(ck);
    const name = canvasPlane(W * 0.62, H * 0.2, (x, cw, ch) => { x.fillStyle = '#FFD84A'; x.strokeStyle = '#3A2A00'; x.lineWidth = ch * 0.08; x.font = `900 ${ch * 0.74}px Arial`; x.textAlign = 'center'; x.textBaseline = 'middle'; x.strokeText(o.name || 'BOUCHON 1', cw / 2, ch * 0.55); x.fillText(o.name || 'BOUCHON 1', cw / 2, ch * 0.55); }, { res: 512, transparent: true, emissive: 0.9 });
    name.position.set(0, H * 0.12, 0.02); g.add(name);
    g.userData.update = t => {
      const a = t / (o.period ?? 3) * TAU; ck.position.set(Math.cos(a) * W * 0.32, H * 0.58 + Math.sin(a) * H * 0.3 - H * 0.0, 0.05); ck.rotation.set(0.3, a, -0.4);
      const u = o.nameAt == null ? 9 : t - o.nameAt; name.visible = u >= 0; if (u >= 0) { const k = u < 0.12 ? eo(u / 0.12) * 1.15 : 1.15 - 0.15 * clamp01((u - 0.12) / 0.1); name.scale.setScalar(Math.max(0.01, k)); }
    };
    g.userData.update(0); return g;
  },

  // A state portrait of the cork in a heavy gilt frame (pivot at the bottom centre of the frame, facing +Z): o.w (1.0) x o.h (1.25), the cork in oils
  // on a deep red ground with a tricolour sash across it; a grey veil over it slides off at o.unveilAt (0.3 s) and drops below the frame
  corkPortrait(o) {
    const W = o.w ?? 1.0, H = o.h ?? 1.25, g = grp(), F = 0.09, gold = '#C9A23A';
    for (const [w, h, x, y] of [[W + 2 * F, F, 0, H + F / 2], [W + 2 * F, F, 0, -F / 2], [F, H, -W / 2 - F / 2, H / 2], [F, H, W / 2 + F / 2, H / 2]]) g.add(at(box(w, h, 0.07, gold, { outline: 0.006 }), x, y + F, 0));
    const art = canvasPlane(W, H, (x, cw, ch) => {
      const gr = x.createRadialGradient(cw / 2, ch * 0.42, ch * 0.05, cw / 2, ch / 2, ch * 0.7); gr.addColorStop(0, '#8A2A2A'); gr.addColorStop(1, '#3A0E12'); x.fillStyle = gr; x.fillRect(0, 0, cw, ch);
      const cx = cw / 2, cr = cw * 0.24; x.fillStyle = '#C9A26B'; x.strokeStyle = '#4A3420'; x.lineWidth = cw * 0.012;
      x.beginPath(); x.ellipse(cx, ch * 0.32, cr, cr * 0.42, 0, PI, TAU); x.lineTo(cx + cr, ch * 0.42); x.lineTo(cx - cr, ch * 0.42); x.closePath(); x.fill(); x.stroke();
      x.beginPath(); x.moveTo(cx - cr * 0.72, ch * 0.42); x.lineTo(cx + cr * 0.72, ch * 0.42); x.lineTo(cx + cr * 0.64, ch * 0.78); x.lineTo(cx - cr * 0.64, ch * 0.78); x.closePath(); x.fill(); x.stroke();
      x.fillStyle = '#D9B44A'; x.fillRect(cx - cr * 0.6, ch * 0.2, cr * 1.2, ch * 0.03);
      x.fillStyle = '#8E6A40'; for (let i = 0; i < 26; i++) { x.beginPath(); x.arc(cx + (hash(i) - 0.5) * cr * 1.3, ch * (0.45 + 0.3 * hash(i + 5)), cw * 0.008, 0, TAU); x.fill(); }
      x.save(); x.translate(cx, ch * 0.55); x.rotate(-0.55); ['#2F62B5', '#F4F4F0', '#E0413A'].forEach((c, i) => { x.fillStyle = c; x.fillRect(-cw * 0.6, (i - 1.5) * ch * 0.035, cw * 1.2, ch * 0.035); }); x.restore();
      x.strokeStyle = 'rgba(255,230,160,0.25)'; x.lineWidth = 3; for (let i = 0; i < 40; i++) { x.beginPath(); x.moveTo(cw * hash(i + 70), ch * hash(i + 90)); x.lineTo(cw * hash(i + 70) + 14, ch * hash(i + 90) + 6); x.stroke(); }
    }, { res: 512, emissive: 0.25 });
    art.position.set(0, H / 2 + F, 0.01); g.add(art);
    const veil = new THREE.Mesh(new THREE.PlaneGeometry(W + 0.16, H + 0.16, 6, 6), lam('#8A8C9A')); veil.position.set(0, H / 2 + F, 0.06); g.add(veil);
    const vp = veil.geometry.attributes.position, v0 = vp.array.slice();
    g.userData.update = t => {
      const u = o.unveilAt == null ? -1 : (t - o.unveilAt) / 0.3, k = eo(u); veil.visible = u < 1;
      if (u <= 0) { veil.position.y = H / 2 + F; for (let i = 0; i < vp.count; i++) { vp.setXYZ(i, v0[i * 3], v0[i * 3 + 1], v0[i * 3 + 2] + 0.01 * Math.sin(v0[i * 3] * 9 + v0[i * 3 + 1] * 7)); } vp.needsUpdate = true; return; }
      veil.position.y = H / 2 + F - (H + 0.3) * k;
      for (let i = 0; i < vp.count; i++) { const x0 = v0[i * 3], y0 = v0[i * 3 + 1], w = 0.5 + 0.5 * Math.sin(x0 * 11 + y0 * 5); vp.setXYZ(i, x0 * (1 - 0.35 * k * (0.5 - y0 / (H + 0.16))), y0, 0.08 * k * w); }
      vp.needsUpdate = true;
    };
    g.userData.update(0); return g;
  },
};
