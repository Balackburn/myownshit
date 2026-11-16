// « La table basse » (story 80): this man stubbed his toe on his coffee table; it was premeditated: special forces, a flashbang, a tank through three
// buildings, four pairs of handcuffs, a medal for the tank driver, a trial, twenty years, three guards in casts, life; on appeal an X-ray finds a
// bruise on the table: he is the one convicted, and the table is his cellmate.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere, addOutline } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const keyAt = (keys, t, d) => { if (!keys || !keys.length) return d; if (t <= keys[0][0]) return keys[0][1]; for (let i = 1; i < keys.length; i++) { const [t1, v1] = keys[i]; if (t <= t1) { const [t0, v0] = keys[i - 1], u = clamp01((t - t0) / Math.max(1e-6, t1 - t0)), e = u * u * (3 - 2 * u); return v0 + (v1 - v0) * e; } } return keys[keys.length - 1][1]; };
const hsh = i => { const x = Math.sin(i * 127.1 + 31.7) * 43758.5453; return x - Math.floor(x); };
// a pop-in: 0 before t0, an overshoot to 1.25 at t0 + 0.09, back to 1 at t0 + 0.2
const popK = (t, t0) => { if (t0 == null) return 1; const u = t - t0; if (u <= 0) return 0; if (u < 0.09) return 1.25 * (u / 0.09); if (u < 0.2) return 1.25 - 0.25 * (u - 0.09) / 0.11; return 1; };
const basic = (c, o = {}) => new THREE.MeshBasicMaterial({ color: c, transparent: o.opacity != null, opacity: o.opacity ?? 1, depthWrite: o.opacity == null, side: o.side || THREE.FrontSide });

export const TABLE_PROPS = {
  // The coffee table, the story's hero (pivot at the floor under its middle; o.w 1.1, o.d 0.6, o.h 0.42): a thick warm wooden top with a darker edge,
  // an apron under it and four square legs. The same model in every shot. o.squash [[t, v], ...]: the legs crushed to 1 - 0.75 v (a giant stamp:
  // key 0 -> 1 in one frame and back with a bounce); o.bruise: a blue bruise on the front right leg (true, or the time it appears); o.cuffs: a steel
  // ring round each leg (four soldiers cuffed to it); o.legT (0.075): the legs' thickness (thicker for the extreme close-up); o.bandage: a white
  // bandage wound round the bruised leg (the plaintiff in court)
  coffeeTable(o) {
    const w = o.w ?? 1.1, d = o.d ?? 0.6, h = o.h ?? 0.42, lt = o.legT ?? 0.075, top = 0.06, g = grp(), up = grp(), legs = [];
    const wood = o.color || '#B9824C', dark = o.edge || '#7A4E2A';
    up.add(at(box(w, top, d, wood, { outline: 0.012 }), 0, -top / 2, 0), at(box(w + 0.012, 0.018, d + 0.012, dark), 0, -top + 0.004, 0));
    up.add(at(box(w - 0.14, 0.07, 0.03, dark, { outline: 0.006 }), 0, -top - 0.035, d / 2 - 0.07), at(box(w - 0.14, 0.07, 0.03, dark, { outline: 0.006 }), 0, -top - 0.035, -d / 2 + 0.07));
    up.add(at(box(0.03, 0.07, d - 0.14, dark, { outline: 0.006 }), w / 2 - 0.07, -top - 0.035, 0), at(box(0.03, 0.07, d - 0.14, dark, { outline: 0.006 }), -w / 2 + 0.07, -top - 0.035, 0));
    // the grain: three darker streaks along the top
    for (let i = 0; i < 3; i++) up.add(at(box(w * (0.5 + 0.15 * i), 0.002, 0.012, '#A06E3E'), (i - 1) * 0.08, 0.001, -0.15 + i * 0.14));
    g.add(up);
    const L0 = h - top;
    [[1, 1], [-1, 1], [1, -1], [-1, -1]].forEach(([sx, sz], i) => {
      const lg = grp(), leg = at(box(lt, L0, lt, o.legs || '#9A6838', { pivot: 'bottom', outline: 0.008, taper: { x: 0.8, z: 0.8 } }), 0, 0, 0);
      lg.add(leg); lg.position.set(sx * (w / 2 - 0.09), 0, sz * (d / 2 - 0.09)); g.add(lg); legs.push({ lg, sx, sz, i });
      if (o.cuffs) { const ring = at(new THREE.Mesh(new THREE.TorusGeometry(lt * 0.95, 0.016, 6, 14), new THREE.MeshLambertMaterial({ color: '#D9DDE2' })), 0, L0 * 0.55, 0, PI / 2, 0, 0); addOutline(ring, 0.05); lg.add(ring); }
    });
    let bruise = null;
    if (o.bruise != null && o.bruise !== false) {
      bruise = canvasPlane(lt * 0.92, lt * 1.4, (c, W, H) => { c.clearRect(0, 0, W, H);
        const gr = c.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, W * 0.5); gr.addColorStop(0, '#3B2A7A'); gr.addColorStop(0.45, '#4C5BB5'); gr.addColorStop(0.8, 'rgba(110,150,200,0.85)'); gr.addColorStop(1, 'rgba(140,170,200,0)');
        c.fillStyle = gr; c.beginPath(); c.ellipse(W / 2, H / 2, W * 0.48, H * 0.46, 0, 0, TAU); c.fill();
        c.fillStyle = 'rgba(120,200,120,0.35)'; c.beginPath(); c.ellipse(W * 0.62, H * 0.66, W * 0.18, H * 0.12, 0.4, 0, TAU); c.fill(); }, { res: 128, transparent: true });
      bruise.position.set(0, L0 * 0.55, lt / 2 + 0.003); legs[0].lg.add(bruise);
    }
    if (o.bandage) { for (let i = 0; i < 3; i++) legs[0].lg.add(at(box(lt * 1.35, 0.045, lt * 1.35, '#F7F6F1', { outline: 0.004 }), 0, L0 * (0.42 + 0.11 * i), 0, 0, 0, (i - 1) * 0.12));
      legs[0].lg.add(at(box(lt * 0.5, 0.09, 0.012, '#F7F6F1', { outline: 0.003 }), lt * 0.35, L0 * 0.62, lt * 0.7, 0, 0, -0.5)); }
    g.userData.update = t => {
      const v = clamp01(keyAt(o.squash, t, 0)), sy = 1 - 0.75 * v, sx = 1 + 0.6 * v;
      for (const L of legs) { L.lg.scale.set(sx, sy, sx); L.lg.position.x = L.sx * (w / 2 - 0.09) * (1 + 0.18 * v); L.lg.position.z = L.sz * (d / 2 - 0.09) * (1 + 0.18 * v); }
      up.position.y = top + L0 * sy; up.scale.set(1 + 0.08 * v, 1 - 0.3 * v, 1 + 0.08 * v);
      if (bruise) bruise.visible = o.bruise === true || t >= o.bruise;
    };
    g.userData.update(0); g.userData.top = [0, h, 0]; return g;
  },

  // A yellow numbered evidence marker (pivot at the floor; front +Z): a folded tent of card, the number o.n black on both faces; o.at: it pops in with
  // an overshoot; o.s (1): 0.16 m tall
  evidenceMarker(o) {
    const s = o.s ?? 1, W = 0.13 * s, H = 0.16 * s, g = grp(), tent = grp(); g.add(tent);
    const face = () => canvasPlane(W, H, (c, Wc, Hc) => { c.fillStyle = '#F5C518'; c.fillRect(0, 0, Wc, Hc); c.strokeStyle = '#1B1B1B'; c.lineWidth = Wc * 0.05; c.strokeRect(Wc * 0.04, Hc * 0.04, Wc * 0.92, Hc * 0.92);
      c.fillStyle = '#111111'; c.font = `bold ${Hc * 0.62}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(String(o.n ?? 1), Wc / 2, Hc * 0.55); }, { res: 128 });
    const a = 0.32, f1 = face(), f2 = face();
    f1.position.set(0, H / 2 * Math.cos(a), H / 2 * Math.sin(a)); f1.rotation.x = -a; f2.position.set(0, H / 2 * Math.cos(a), -H / 2 * Math.sin(a)); f2.rotation.set(a, PI, 0);
    tent.add(f1, f2);
    g.userData.update = t => { const k = popK(t, o.at); tent.scale.setScalar(Math.max(0.001, k)); tent.visible = k > 0.001; };
    g.userData.update(0); return g;
  },

  // A flashbang going off (pivot at its centre): at o.at a white-yellow ball blows up to o.r (1.6 m) in three frames and fades over o.fade (0.3 s), a
  // ring of white rays round it; nothing before o.at
  flashBang(o) {
    const R = o.r ?? 1.6, fade = o.fade ?? 0.3, g = grp();
    const ball = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 2), basic('#FFF8D8', { opacity: 1 })); g.add(ball);
    const core = new THREE.Mesh(new THREE.IcosahedronGeometry(0.55, 2), basic('#FFFFFF', { opacity: 1 })); g.add(core);
    const rays = []; for (let i = 0; i < 12; i++) { const r_ = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1, 0.02), basic('#FFFFFF', { opacity: 1 })); r_.geometry.translate(0, 0.5, 0); r_.rotation.z = i / 12 * TAU; g.add(r_); rays.push(r_); }
    g.userData.update = t => { const u = t - (o.at ?? 0), grow = clamp01(u / 0.1), f = u < 0.1 ? 1 : clamp01(1 - (u - 0.1) / fade);
      const on = u >= 0 && f > 0.01; ball.visible = core.visible = on; rays.forEach(r_ => { r_.visible = on; });
      if (!on) return; ball.scale.setScalar(R * (0.2 + 0.8 * grow)); ball.material.opacity = 0.9 * f; core.scale.setScalar(R * (0.3 + 0.7 * grow)); core.material.opacity = f;
      rays.forEach((r_, i) => { r_.position.set(0, 0, 0.05); r_.scale.set(1, R * (0.9 + 0.9 * grow) * (0.8 + 0.4 * hsh(i)), 1); r_.material.opacity = f; }); };
    g.userData.update(-1); return g;
  },

  // A climbing rope hanging from its pivot (the top) down o.len (6 m), o.r 0.025; o.sway: it swings a little
  rope(o) {
    const L = o.len ?? 6, g = grp(), r = at(cyl(o.r ?? 0.025, o.r ?? 0.025, L, o.color || '#C9A86A', 6, { pivot: 'top' }), 0, 0, 0); g.add(r);
    g.userData.update = t => { r.rotation.z = (o.sway ?? 0.03) * Math.sin(t * 2.3 + (o.seed || 0)); r.rotation.x = (o.sway ?? 0.03) * 0.6 * Math.sin(t * 1.7 + 1 + (o.seed || 0)); };
    g.userData.update(0); return g;
  },

  // A block of flats (pivot at the floor under its front middle, front +Z, depth toward -Z): a cream facade with rows of windows, shutters and small
  // balconies, a grey roof; o.w 4.4, o.h 7.2, o.d 4.0, o.color. o.hole [x, y, r] (in the facade's frame; default [0, 1.3, 1.25]): a round hole right
  // through it, front to back, with a brick rim and a dark tunnel (one in a row of three lines up: you see through all three);
  // o.holeAt: before it the facade is whole (a tank about to come through); o.backAt: the same for the back facade (a tank about to come out)
  holedBlock(o) {
    const W = o.w ?? 4.4, H = o.h ?? 7.2, D = o.d ?? 4.0, [hx, hy, hr] = o.hole || [0, 1.3, 1.25], col = o.color || '#EBDDC4', g = grp();
    const drawFace = (holed, back) => (c, Wc, Hc) => { const k = Wc / W; c.fillStyle = col; c.fillRect(0, 0, Wc, Hc);
      c.fillStyle = 'rgba(0,0,0,0.06)'; for (let y = 0; y < H; y += 0.5) c.fillRect(0, Hc - y * k, Wc, 2);
      c.fillStyle = '#C9B89C'; c.fillRect(0, Hc - 0.5 * k, Wc, 0.5 * k);
      const cols = Math.max(2, Math.round(W / 1.25)), rows = Math.max(2, Math.floor((H - 0.6) / 1.6));
      for (let r = 0; r < rows; r++) for (let q = 0; q < cols; q++) { const x = (q + 0.5) * W / cols, y = 0.9 + r * 1.6;
        if (holed && Math.hypot(x - (W / 2 + hx), y + 0.55 - hy) < hr + 0.55) continue;
        c.fillStyle = '#3F6E8C'; c.fillRect((x - 0.32) * k, Hc - (y + 1.0) * k, 0.64 * k, 1.0 * k);
        c.fillStyle = '#9CC7DE'; c.fillRect((x - 0.27) * k, Hc - (y + 0.95) * k, 0.54 * k, 0.42 * k);
        c.fillStyle = back ? '#7D8C6A' : '#5E7F52'; c.fillRect((x - 0.5) * k, Hc - (y + 1.0) * k, 0.16 * k, 1.0 * k); c.fillRect((x + 0.34) * k, Hc - (y + 1.0) * k, 0.16 * k, 1.0 * k);
        if (r > 0) { c.fillStyle = '#2E3238'; c.fillRect((x - 0.42) * k, Hc - (y + 0.05) * k, 0.84 * k, 0.06 * k); for (let b = 0; b < 6; b++) c.fillRect((x - 0.4 + b * 0.16) * k, Hc - (y + 0.3) * k, 0.025 * k, 0.25 * k); } }
      if (holed) { c.save(); c.globalCompositeOperation = 'destination-out'; c.beginPath(); c.arc((W / 2 + hx) * k, Hc - hy * k, hr * k, 0, TAU); c.fill(); c.restore(); } };
    const mk = (holed, back) => { const p = canvasPlane(W, H, drawFace(holed, back), { res: 512, transparent: holed }); return p; };
    const fWhole = mk(false, false), fHole = mk(true, false), bHole = mk(true, true), bWhole = mk(false, true);
    fWhole.position.set(0, H / 2, 0.002); fHole.position.set(0, H / 2, 0.002); bHole.position.set(0, H / 2, -D - 0.002); bHole.rotation.y = PI; bWhole.position.copy(bHole.position); bWhole.rotation.y = PI;
    g.add(fWhole, fHole, bHole, bWhole);
    // the walls behind the facades: sides, roof, a dark inside (seen through the hole only as the tunnel)
    g.add(at(box(0.12, H, D, '#D8C8AC', { pivot: 'bottom', outline: 0.01 }), -W / 2 + 0.06, 0, -D / 2), at(box(0.12, H, D, '#D8C8AC', { pivot: 'bottom', outline: 0.01 }), W / 2 - 0.06, 0, -D / 2));
    g.add(at(box(W + 0.3, 0.5, D + 0.3, '#5F6B78', { pivot: 'bottom', outline: 0.01 }), 0, H, -D / 2), at(box(W + 0.1, 0.18, 0.18, '#CDBB9C', { outline: 0.006 }), 0, H - 0.1, 0.06));
    const tun = new THREE.Mesh(new THREE.CylinderGeometry(hr, hr, D, 20, 1, true), new THREE.MeshLambertMaterial({ color: '#4A3A30', side: THREE.BackSide }));
    tun.rotation.x = PI / 2; tun.position.set(hx, hy, -D / 2); g.add(tun);
    const rims = [grp(), grp()]; [0.03, -D - 0.03].forEach((z, q) => { for (let i = 0; i < 18; i++) { const a = i / 18 * TAU + hsh(i) * 0.2, rr = hr + 0.05 + 0.1 * hsh(i + 7);
      rims[q].add(at(box(0.28 + 0.12 * hsh(i + 3), 0.13, 0.12, i % 3 ? '#B8573A' : '#9C4630', { outline: 0.006 }), hx + rr * Math.cos(a), hy + rr * Math.sin(a), z, 0, 0, a + PI / 2)); } });
    g.add(rims[0], rims[1]);
    // the floor of the tunnel: a strip of rubble
    g.add(at(box(hr * 1.2, 0.08, D, '#8C7A66'), hx, hy - hr + 0.04, -D / 2));
    g.userData.update = t => { const holed = o.holeAt == null || t >= o.holeAt, bh = o.backAt == null || t >= o.backAt;
      fWhole.visible = !holed; fHole.visible = holed; rims[0].visible = holed; bWhole.visible = !bh; bHole.visible = bh; rims[1].visible = bh; tun.visible = holed || bh; };
    g.userData.update(0); return g;
  },

  // Bricks blown out of a wall (pivot at the hole's centre): at o.at, o.n (26) orange bricks fly out toward +Z and aside, spinning, fall under gravity
  // to the ground (o.floor: how far below the pivot, 1.3 m) and lie there; a grey dust cloud swells and fades; o.spread (1.0), o.speed (5 m/s)
  brickBurst(o) {
    const n = o.n ?? 26, g = grp(), bricks = [], fl = o.floor ?? 1.3, sp = o.speed ?? 5, spr = o.spread ?? 1.0;
    for (let i = 0; i < n; i++) { const b = box(0.24, 0.11, 0.12, i % 4 ? '#B8573A' : '#D9CBB0', { outline: 0.006 }); b.visible = false; g.add(b); bricks.push(b); }
    const dust = []; for (let i = 0; i < 7; i++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(0.5, 1), new THREE.MeshLambertMaterial({ color: '#CFC6B8', transparent: true, opacity: 0.9 })); m.visible = false; g.add(m); dust.push(m); }
    g.userData.update = t => { const u = t - (o.at ?? 0);
      bricks.forEach((b, i) => { if (u < 0) { b.visible = false; return; } b.visible = true;
        const a = (hsh(i) - 0.5) * PI * spr, vz = sp * (0.6 + 0.6 * hsh(i + 11)), vx = Math.sin(a) * sp * 0.7, vy = 1.5 + 3.5 * hsh(i + 23);
        let tt = u, y = vy * tt - 4.9 * tt * tt; const land = (vy + Math.sqrt(vy * vy + 2 * 9.8 * fl)) / 9.8; if (tt > land) { tt = land; y = -fl + 0.055; }
        b.position.set(vx * tt + (hsh(i + 5) - 0.5) * 0.6, Math.max(-fl + 0.055, y), vz * tt); b.rotation.set(tt * 9 * hsh(i + 2), tt * 7 * hsh(i + 4), tt * 8 * hsh(i + 6)); });
      dust.forEach((m, i) => { const v = (u - i * 0.03) / 1.1; m.visible = v > 0 && v < 1; if (!m.visible) return; m.position.set((hsh(i + 40) - 0.5) * 2.4 * Math.sqrt(v), -0.3 + 0.8 * v, 0.8 + 1.4 * v * hsh(i + 50)); m.scale.setScalar(0.5 + 1.6 * Math.sqrt(v)); m.material.opacity = 0.85 * (1 - v); }); };
    g.userData.update(-1); return g;
  },

  // A plaster cast on a foot (attach to a foot joint): a fat white boot with a bandage spiral and a pink toe end; o.s (1)
  footCast(o) {
    const s = o.s ?? 1, g = grp(at(box(0.2 * s, 0.17 * s, 0.36 * s, '#F7F6F1', { outline: 0.01 }), 0, 0.02 * s, 0.05 * s));
    for (let i = 0; i < 4; i++) g.add(at(box(0.212 * s, 0.025 * s, 0.03 * s, '#E2E0D8'), 0, 0.02 * s, (-0.08 + i * 0.075) * s, 0.25, 0, 0));
    g.add(at(box(0.16 * s, 0.07 * s, 0.03 * s, '#E9B9A0', { outline: 0.004 }), 0, -0.01 * s, 0.235 * s));
    return g;
  },

  // A crutch (pivot at its hand grip; it hangs down 0.95 m to its rubber foot and rises 0.42 m to the pad under the arm): two grey rails, a grip, a
  // padded top; o.color
  crutch(o) {
    const g = grp(), c = o.color || '#9AA3AD';
    for (const sx of [-1, 1]) g.add(at(box(0.025, 1.3, 0.025, c, { outline: 0.004 }), sx * 0.05, -0.27, 0, 0, 0, sx * 0.04));
    g.add(at(box(0.13, 0.035, 0.035, '#2B2E33', { outline: 0.004 }), 0, 0, 0), at(box(0.16, 0.05, 0.06, '#2B2E33', { outline: 0.006 }), 0, 0.42, 0));
    g.add(at(box(0.03, 0.25, 0.03, c, { outline: 0.004 }), 0, -1.02, 0), at(box(0.05, 0.05, 0.05, '#2B2E33'), 0, -1.15, 0));
    return g;
  },

  // A giant floor plan unrolled down from a bar held overhead (pivot at the bar's middle; front +Z): a cream sheet o.w (1.7) wide, o.len (2.1) long
  // when open, drawn like an architect's plan: the living room walls, the sofa, the coffee table (brown, filled), a trail of black footprints
  // walking straight into it and a red star where they meet; o.unroll [[t, 0..1], ...]: how far it has come down, a paper roll at the bottom edge
  planScroll(o) {
    const Wd = o.w ?? 1.7, Ln = o.len ?? 2.1, g = grp();
    g.add(at(cyl(0.035, 0.035, Wd + 0.2, '#6B4A32', 8, { outline: 0.006 }), 0, 0, 0, 0, 0, PI / 2));
    const cnv = document.createElement('canvas'); cnv.width = 512; cnv.height = Math.round(512 * Ln / Wd); const c = cnv.getContext('2d'), Wc = cnv.width, Hc = cnv.height;
    c.fillStyle = '#F3EEDD'; c.fillRect(0, 0, Wc, Hc); c.strokeStyle = '#1F3B73'; c.lineWidth = Wc * 0.02; c.strokeRect(Wc * 0.06, Hc * 0.05, Wc * 0.88, Hc * 0.9);
    c.lineWidth = Wc * 0.008; c.strokeStyle = 'rgba(31,59,115,0.25)'; for (let x = 0.1; x < 0.92; x += 0.08) { c.beginPath(); c.moveTo(Wc * x, Hc * 0.05); c.lineTo(Wc * x, Hc * 0.95); c.stroke(); }
    c.fillStyle = '#1F3B73'; c.font = `bold ${Wc * 0.07}px Arial`; c.textAlign = 'center'; c.fillText('SALON', Wc / 2, Hc * 0.12);
    c.fillStyle = '#8A97A8'; c.fillRect(Wc * 0.18, Hc * 0.17, Wc * 0.64, Hc * 0.09); c.strokeStyle = '#1F3B73'; c.lineWidth = Wc * 0.01; c.strokeRect(Wc * 0.18, Hc * 0.17, Wc * 0.64, Hc * 0.09);
    c.fillStyle = '#9A6838'; c.fillRect(Wc * 0.3, Hc * 0.36, Wc * 0.4, Hc * 0.11); c.strokeRect(Wc * 0.3, Hc * 0.36, Wc * 0.4, Hc * 0.11);
    c.fillStyle = '#F3EEDD'; c.font = `bold ${Wc * 0.055}px Arial`; c.fillText('TABLE', Wc / 2, Hc * 0.43);
    c.fillStyle = '#1B1B1B'; for (let i = 0; i < 7; i++) { const x = Wc * (0.5 + (i % 2 ? 0.05 : -0.05)), y = Hc * (0.9 - i * 0.055); c.beginPath(); c.ellipse(x, y, Wc * 0.028, Hc * 0.018, 0, 0, TAU); c.fill(); c.beginPath(); c.ellipse(x, y - Hc * 0.025, Wc * 0.02, Hc * 0.009, 0, 0, TAU); c.fill(); }
    c.fillStyle = '#D7262E'; c.beginPath(); for (let i = 0; i < 16; i++) { const a = -PI / 2 + i * PI / 8, rr = i % 2 ? Wc * 0.035 : Wc * 0.085; c.lineTo(Wc * 0.5 + rr * Math.cos(a), Hc * 0.49 + rr * Math.sin(a)); } c.closePath(); c.fill();
    const tex = new THREE.CanvasTexture(cnv); tex.colorSpace = THREE.SRGBColorSpace;
    const sheet = new THREE.Mesh(new THREE.PlaneGeometry(Wd, 1), new THREE.MeshLambertMaterial({ map: tex, side: THREE.DoubleSide })); sheet.geometry.translate(0, -0.5, 0); g.add(sheet);
    const roll = at(cyl(0.06, 0.06, Wd + 0.04, '#E9E3CF', 10, { outline: 0.006 }), 0, 0, 0.02, 0, 0, PI / 2); g.add(roll);
    g.userData.update = t => { const u = Math.max(0.02, clamp01(keyAt(o.unroll, t, 1))); sheet.scale.y = Ln * u; tex.repeat.set(1, u); tex.offset.set(0, 1 - u); roll.position.y = -Ln * u; roll.scale.y = 1; roll.rotation.x = u * 12; };
    g.userData.update(0); return g;
  },

  // An X-ray table (pivot at the floor under its middle; long side along X): a grey steel top 2.0 x 0.8 at 0.82 m on a white column and a foot; o.l
  xrayBed(o) {
    const l = o.l ?? 2.0, g = grp(at(box(l, 0.08, 0.8, '#C9D0D6', { outline: 0.01 }), 0, 0.78, 0), at(box(l - 0.1, 0.02, 0.7, '#E9EEF1'), 0, 0.83, 0));
    g.add(at(box(0.4, 0.74, 0.5, '#F2F4F5', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0), at(box(1.0, 0.06, 0.7, '#B9C1C8', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0));
    g.userData.top = [0, 0.84, 0]; return g;
  },

  // A light box with the X-ray of a table (pivot at the floor under its middle, front +Z; a panel o.w 1.3 x 1.0 on a stand at o.y 1.55): dark and
  // blank until o.at, then it blinks on (two flickers) to a glowing blue film where the table shows in white bones: the top slab and four legs with
  // round knuckles, one leg with a dark spot (o.spot, the bruise)
  xrayScreen(o) {
    const W = o.w ?? 1.3, H = o.h ?? 1.0, y = o.y ?? 1.55, g = grp();
    g.add(at(box(0.08, y - H / 2, 0.08, '#B9C1C8', { pivot: 'bottom' }), 0, 0, -0.05), at(box(0.7, 0.05, 0.5, '#B9C1C8', { pivot: 'bottom' }), 0, 0, -0.05));
    g.add(at(box(W + 0.12, H + 0.12, 0.08, '#E9EEF1', { outline: 0.01 }), 0, y, -0.06));
    const off = at(box(W, H, 0.01, '#20262C'), 0, y, 0);
    const on = canvasPlane(W, H, (c, Wc, Hc) => { const gr = c.createRadialGradient(Wc / 2, Hc / 2, 0, Wc / 2, Hc / 2, Wc * 0.7); gr.addColorStop(0, '#1E4C7A'); gr.addColorStop(1, '#0B1E33'); c.fillStyle = gr; c.fillRect(0, 0, Wc, Hc);
      c.fillStyle = 'rgba(235,248,255,0.92)'; c.shadowColor = '#BFE6FF'; c.shadowBlur = Wc * 0.03;
      c.fillRect(Wc * 0.12, Hc * 0.26, Wc * 0.76, Hc * 0.09);
      [0.2, 0.36, 0.64, 0.8].forEach((x, i) => { c.fillRect(Wc * x - Wc * 0.022, Hc * 0.35, Wc * 0.044, Hc * 0.46); c.beginPath(); c.arc(Wc * x, Hc * 0.35, Wc * 0.04, 0, TAU); c.fill(); c.beginPath(); c.arc(Wc * x, Hc * 0.81, Wc * 0.035, 0, TAU); c.fill(); });
      if (o.spot !== false) { c.shadowBlur = 0; c.fillStyle = 'rgba(20,30,60,0.85)'; c.beginPath(); c.ellipse(Wc * 0.8, Hc * 0.58, Wc * 0.035, Hc * 0.05, 0, 0, TAU); c.fill(); } }, { res: 512, emissive: 0.9 });
    on.position.set(0, y, 0.006); g.add(off, on);
    g.userData.update = t => { const u = t - (o.at ?? -1); const lit = u >= 0 && !(u > 0.05 && u < 0.09) && !(u > 0.14 && u < 0.17); on.visible = lit; off.visible = !lit; };
    g.userData.update(0); return g;
  },

  // A barred cell door (pivot at its hinge, the left edge at the floor; it closes along +X): a navy frame with nine bars and a lock plate; o.w 0.95,
  // o.h 2.15; o.open (1.6 rad) until o.slam, then it swings shut in 0.12 s and bounces twice (0.18, 0.06 rad) before it sits; o.plate: a white
  // plate across the bars at chest height (something to stamp)
  barDoor(o) {
    const W = o.w ?? 0.95, H = o.h ?? 2.15, g = grp(), leaf = grp(); g.add(leaf);
    leaf.add(at(box(0.07, H, 0.07, '#26324E', { pivot: 'bottom', outline: 0.006 }), 0.035, 0, 0), at(box(0.07, H, 0.07, '#26324E', { pivot: 'bottom', outline: 0.006 }), W - 0.035, 0, 0));
    for (const y of [0.06, H * 0.5, H - 0.06]) leaf.add(at(box(W, 0.08, 0.07, '#26324E', { outline: 0.006 }), W / 2, y, 0));
    for (let i = 1; i < 9; i++) leaf.add(at(cyl(0.017, 0.017, H, '#59606A', 6, { pivot: 'bottom' }), i * W / 9, 0, 0));
    leaf.add(at(box(0.14, 0.2, 0.1, '#E2B53C', { outline: 0.006 }), W - 0.12, H * 0.5, 0.02));
    if (o.plate) leaf.add(at(box(W * 0.8, 0.5, 0.03, '#F4F1E8', { outline: 0.006 }), W / 2, H * 0.62, 0.06));
    const A = o.open ?? 1.6;
    g.userData.update = t => { let a = A; if (o.slam != null) { const u = t - o.slam; if (u >= 0) { if (u < 0.12) a = A * (1 - (u / 0.12) * (u / 0.12)); else { const v = u - 0.12; a = v < 0.12 ? 0.18 * Math.sin(PI * v / 0.12) : v < 0.2 ? 0.06 * Math.sin(PI * (v - 0.12) / 0.08) : 0; } } } leaf.rotation.y = a; };
    g.userData.update(0); return g;
  },

  // A courtroom's back wall that falls flat away from us (pivot at the floor under its middle; front +Z): a cream wall o.w (9) x o.h (5) painted with
  // the room's navy and teal bands, the TRIBUNAL sign and the seal; at o.at it tips back about its foot (0.42 s, ease in), slams down, bounces
  // once; o.thick (0.2)
  fallWall(o) {
    const W = o.w ?? 9, H = o.h ?? 5, T = o.thick ?? 0.2, g = grp(), leaf = grp(); g.add(leaf);
    leaf.add(at(box(W, H, T, '#EFE9DC', { pivot: 'bottom', outline: 0.01 }), 0, 0, -T / 2));
    const face = canvasPlane(W, H, (c, Wc, Hc) => { const k = Wc / W; c.fillStyle = '#F3EFE6'; c.fillRect(0, 0, Wc, Hc);
      c.fillStyle = '#1F2D4E'; c.fillRect(0, Hc - 3.4 * k, Wc, 0.18 * k); c.fillStyle = '#3E7F86'; c.fillRect(0, Hc - 3.0 * k, Wc, 0.1 * k);
      c.fillStyle = '#B98A5A'; c.fillRect(0, Hc - 1.0 * k, Wc, 1.0 * k);
      [-3.6, -2.2, 2.2, 3.6].forEach((x, i) => { c.fillStyle = i % 2 ? '#3E7F86' : '#C2342A'; c.fillRect((W / 2 + x - 0.35) * k, Hc - 4.6 * k, 0.7 * k, 3.6 * k); });
      c.fillStyle = '#1F2D4E'; c.fillRect((W / 2 - 1.3) * k, Hc - 3.9 * k, 2.6 * k, 0.6 * k); c.strokeStyle = '#E2B53C'; c.lineWidth = 0.05 * k; c.strokeRect((W / 2 - 1.3) * k, Hc - 3.9 * k, 2.6 * k, 0.6 * k);
      c.fillStyle = '#F3EFE6'; c.font = `bold ${0.38 * k}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.sign || 'TRIBUNAL', W / 2 * k, Hc - 3.6 * k);
      c.fillStyle = '#E2B53C'; c.beginPath(); c.arc(W / 2 * k, Hc - 4.45 * k, 0.32 * k, 0, TAU); c.fill(); c.fillStyle = '#F3EFE6'; c.beginPath(); c.arc(W / 2 * k, Hc - 4.45 * k, 0.24 * k, 0, TAU); c.fill(); }, { res: 1024 });
    face.position.set(0, H / 2, 0.004); leaf.add(face);
    g.userData.update = t => { let a = 0; if (o.at != null) { const u = t - o.at; if (u > 0) { if (u < 0.42) a = (PI / 2) * (u / 0.42) * (u / 0.42); else { const v = u - 0.42; a = PI / 2 - (v < 0.16 ? 0.12 * Math.sin(PI * v / 0.16) : 0); } } } leaf.rotation.x = -a; };
    g.userData.update(0); return g;
  },

  // The dock (pivot at the floor under its middle; front +Z): a wooden box open at the back, o.w 1.6 x o.d 1.0 x o.h 0.95, a rail on top, a darker
  // panel; o.color
  dockBox(o) {
    const w = o.w ?? 1.6, d = o.d ?? 1.0, h = o.h ?? 0.95, c = o.color || '#8A5A34', c2 = '#6B4426', g = grp();
    g.add(at(box(w, h, 0.06, c, { pivot: 'bottom', outline: 0.01 }), 0, 0, d / 2), at(box(0.06, h, d, c, { pivot: 'bottom', outline: 0.01 }), -w / 2, 0, 0), at(box(0.06, h, d, c, { pivot: 'bottom', outline: 0.01 }), w / 2, 0, 0));
    g.add(at(box(w + 0.1, 0.06, 0.1, c2, { outline: 0.006 }), 0, h, d / 2), at(box(0.1, 0.06, d, c2, { outline: 0.006 }), -w / 2, h, 0), at(box(0.1, 0.06, d, c2, { outline: 0.006 }), w / 2, h, 0));
    g.add(at(box(w * 0.8, h * 0.55, 0.01, c2), 0, h * 0.42, d / 2 + 0.032));
    return g;
  },

  // A tactical lamp held like a rifle (pivot at its grip, pointing +Z): a black body with a short stock and a glowing lens, a soft cone of light o.len
  // (3 m) long and o.r (0.45 m) wide at its end; o.beam (0.22): the cone's opacity (lower by day)
  tacLight(o) {
    const L = o.len ?? 3, R = o.r ?? 0.45, g = grp();
    g.add(at(box(0.07, 0.08, 0.42, '#1E2024', { outline: 0.006 }), 0, 0.02, 0.12), at(box(0.06, 0.12, 0.05, '#1E2024'), 0, -0.05, 0.0), at(box(0.06, 0.07, 0.16, '#2C2F35'), 0, 0.0, -0.14));
    g.add(at(cyl(0.05, 0.05, 0.06, '#2C2F35', 10), 0, 0.03, 0.34, PI / 2, 0, 0), at(cyl(0.042, 0.042, 0.01, '#FFF6C8', 10, { emissive: '#FFF6C8' }), 0, 0.03, 0.372, PI / 2, 0, 0));
    if (L > 0) { const cone = new THREE.Mesh(new THREE.ConeGeometry(R, L, 18, 1, true), new THREE.MeshBasicMaterial({ color: '#FFF3C2', transparent: true, opacity: o.beam ?? 0.22, depthWrite: false, side: THREE.DoubleSide }));
      cone.rotation.x = -PI / 2; cone.position.set(0, 0.03, 0.38 + L / 2); cone.castShadow = false; g.add(cone); }
    return g;
  },

  // A tank driver's padded helmet (attach to the head joint at its top): a dark olive dome with ribs, ear flaps, goggles pushed up on the front
  tankHelmet(o) {
    const s = o.s ?? 1, c = o.color || '#3E4A2C', g = grp();
    g.add(at(box(0.3 * s, 0.13 * s, 0.27 * s, c, { pivot: 'bottom', outline: 0.006, taper: { x: 0.8, z: 0.8 } }), 0, 0, 0));
    for (const x of [-0.07, 0, 0.07]) g.add(at(box(0.03 * s, 0.14 * s, 0.28 * s, '#2F3A22'), x * s, 0.005 * s, 0));
    for (const sx of [-1, 1]) g.add(at(box(0.04 * s, 0.17 * s, 0.13 * s, c, { outline: 0.005 }), sx * 0.155 * s, -0.06 * s, 0));
    g.add(at(box(0.26 * s, 0.05 * s, 0.03 * s, '#6B4A32', { outline: 0.004 }), 0, 0.06 * s, 0.14 * s));
    for (const sx of [-1, 1]) g.add(at(cyl(0.035 * s, 0.035 * s, 0.03 * s, '#9CC7DE', 10), sx * 0.06 * s, 0.075 * s, 0.155 * s, PI / 2, 0, 0));
    return g;
  },
};
