// « Le service client » (story 73): this man called customer service and was put on hold; the hold music has been playing for ten years, became
// the national anthem, the band plays it at the parade; yesterday someone picked up: « for an adviser, press one »; he pressed one; the music came
// back. Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const hash = i => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
// (pass 2) halo: the note is drawn first as a thick pale shape, then in its colour on top: a sticker edge that keeps it clear of a painting, a street or a
// chalk board behind it
const noteTex = (kind, col, halo) => canvasPlane(1, 1.3, (c, W, H) => { c.clearRect(0, 0, W, H); c.lineCap = 'round'; c.lineJoin = 'round';
  const shape = (ink, grow) => { c.fillStyle = c.strokeStyle = ink;
    const blob = (x, y) => { c.beginPath(); c.ellipse(x, y, W * 0.2 + grow, H * 0.11 + grow, -0.4, 0, TAU); c.fill(); };
    c.lineWidth = W * 0.09 + 2 * grow; blob(W * 0.34, H * 0.76); c.beginPath(); c.moveTo(W * 0.51, H * 0.74); c.lineTo(W * 0.51, H * 0.17); c.stroke();
    if (kind) { c.beginPath(); c.moveTo(W * 0.51, H * 0.17); c.quadraticCurveTo(W * 0.88, H * 0.26, W * 0.8, H * 0.5); c.stroke(); }
    else { blob(W * 0.72, H * 0.68); c.beginPath(); c.moveTo(W * 0.89, H * 0.66); c.lineTo(W * 0.89, H * 0.11); c.lineTo(W * 0.51, H * 0.17); c.stroke(); } };
  if (halo) shape(halo, W * 0.05); shape(col, 0); }, { res: 128, transparent: true });
const SKIN = '#D9A877', RED = '#E3241B';
// a telephone handset drawn as an icon (the sign everybody reads as « phone »): a thick arc with a round end at each tip
const handsetIcon = (c, cx, cy, R, col) => { c.strokeStyle = c.fillStyle = col; c.lineCap = 'round'; c.lineWidth = R * 0.42; c.beginPath(); c.arc(cx, cy + R * 0.55, R, PI * 1.22, PI * 1.78); c.stroke();
  for (const sd of [-1, 1]) { c.save(); c.translate(cx + sd * R * 0.8, cy - R * 0.02); c.rotate(sd * 0.75); c.beginPath(); c.roundRect(-R * 0.3, -R * 0.24, R * 0.6, R * 0.48, R * 0.14); c.fill(); c.restore(); } };

export const CONSEILLER_PROPS = {
  // Hold music coming out of a phone, endlessly (pivot at the source; face it to the camera): o.rate notes a second (3) from o.from to o.until, each
  // drifting up and out to the side (o.dx, o.dy m/s) on a wobble, swelling in and fading out over o.life (1.2 s); o.color (navy), o.size (0.09)
  // (pass 2) o.halo: the colour of the sticker edge round each note (white; false: none); o.stopAt: the music stops dead at that time: no new note,
  // the notes in the air freeze where they are for o.hang (0.18 s), then drop like stones and are gone; o.sway (0.04 m): the wobble
  holdNotes(o) {
    const rate = o.rate ?? 3, life = o.life ?? 1.2, sz = o.size ?? 0.09, n = Math.ceil(rate * life) + 1, g = grp(), N = [], halo = o.halo === false ? null : (o.halo || '#FFFFFF');
    for (let i = 0; i < n; i++) { const pl = noteTex(i % 2, o.color || '#22305A', halo); pl.scale.set(sz, sz, 1); pl.material.depthWrite = false; pl.material.side = THREE.DoubleSide; pl.visible = false; g.add(pl); N.push(pl); }
    const per = n / rate, sw = o.sway ?? 0.04;
    g.userData.update = t => { const t0 = o.from ?? 0, t1 = o.until ?? 1e9, stop = o.stopAt ?? 1e9, hang = o.hang ?? 0.18, te = Math.min(t, stop);
      N.forEach((m, i) => { let b = t0 + i / rate; if (te >= b) b += Math.floor((te - b) / per) * per; const u = te - b, on = te >= t0 && b <= t1 && u >= 0 && u < life && t < stop + hang + 0.7; m.visible = on; if (!on) return;
        const side = (o.side ?? (hash(i + Math.floor(b * 3)) > 0.5 ? 1 : -1)), q = u / life, fall = Math.max(0, t - stop - hang);
        m.position.set(side * (o.dx ?? 0.25) * u + sw * Math.sin(u * 8 + i), (o.dy ?? 0.45) * u - 6 * fall * fall, 0.005 * i); m.rotation.z = 0.35 * Math.sin(u * 6 + i * 2) + (t > stop ? 0.5 * Math.min(1, fall * 4) * (i % 2 ? 1 : -1) : 0);
        const s = sz * (u < 0.1 ? u / 0.1 : 1) * (q > 0.75 && t <= stop ? 1 - (q - 0.75) / 0.25 : 1) * (t > stop ? Math.max(0.6, 1 - 0.15 * Math.sin(Math.min(1, (t - stop) / hang) * PI)) : 1); m.scale.set(s, s, 1); }); };
    g.userData.update(-1); return g;
  },

  // (pass 2) THE phone of the story, big and red so that it reads at the ear in a wide shot (pivot at its middle, screen +Z, back -Z): a chunky red
  // handset o.w wide (0.17), twice as tall, o.d thick (0.06), a stub antenna with a black tip, a dark call screen (o.label) with a green handset, and
  // on its back a white disc with a red handset: seen from behind, on an ear, it still says « phone »
  bigPhone(o) {
    const w = o.w ?? 0.17, h = w * 2.0, d = o.d ?? 0.06, col = o.case || RED, g = grp(at(box(w, h, d, col, { outline: 0.007 }), 0, 0, 0));
    g.add(at(cyl(0.014, 0.014, 0.09, col, 8, { outline: 0.004 }), -w * 0.3, h / 2 + 0.045, 0), at(sphere(0.022, '#1C1C1E', 1), -w * 0.3, h / 2 + 0.1, 0));
    // o.keypad 1: the screen shows the twelve keys of the insert (phoneKeypad) instead of the call screen
    const scr = o.keypad ? canvasPlane(w * 0.84, h * 0.88, (c, W, H) => { c.fillStyle = '#0E1A26'; c.fillRect(0, 0, W, H); c.fillStyle = '#CFE3F2'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `700 ${W * 0.085}px Arial`; c.fillText(o.label || 'SERVICE CLIENT', W / 2, H * 0.08);
      ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#'].forEach((kk, i) => { const x = W * (0.22 + 0.28 * (i % 3)), y = H * (0.3 + 0.16 * Math.floor(i / 3)); c.fillStyle = '#2A3846'; c.beginPath(); c.arc(x, y, W * 0.11, 0, TAU); c.fill(); c.fillStyle = '#FFFFFF'; c.font = `700 ${W * 0.1}px Arial`; c.fillText(kk, x, y + W * 0.005); }); }, { res: 256, emissive: 0.35 })
      : canvasPlane(w * 0.84, h * 0.88, (c, W, H) => { c.fillStyle = '#10202E'; c.fillRect(0, 0, W, H); c.fillStyle = '#CFE3F2'; c.textAlign = 'center'; c.textBaseline = 'middle';
      const tx = o.label || 'SERVICE CLIENT'; let px = W * 0.13; c.font = `700 ${px}px Arial`; const tw = c.measureText(tx).width; if (tw > W * 0.9) { px *= W * 0.9 / tw; c.font = `700 ${px}px Arial`; } c.fillText(tx, W / 2, H * 0.12);
      c.fillStyle = '#3CCB6A'; c.beginPath(); c.arc(W / 2, H * 0.42, W * 0.3, 0, TAU); c.fill(); handsetIcon(c, W / 2, H * 0.42, W * 0.15, '#FFFFFF');
      c.fillStyle = '#2A3846'; for (let i = 0; i < 6; i++) { c.beginPath(); c.arc(W * (0.22 + 0.28 * (i % 3)), H * (0.72 + 0.14 * Math.floor(i / 3)), W * 0.09, 0, TAU); c.fill(); } }, { res: 256, emissive: 0.35 });
    scr.position.z = d / 2 + 0.002; g.add(scr);
    const bk = canvasPlane(w * 0.9, h * 0.9, (c, W, H) => { c.fillStyle = col; c.fillRect(0, 0, W, H); c.fillStyle = '#FFFFFF'; c.beginPath(); c.arc(W / 2, H * 0.4, W * 0.36, 0, TAU); c.fill(); handsetIcon(c, W / 2, H * 0.4, W * 0.19, col);
      c.fillStyle = 'rgba(255,255,255,0.85)'; for (let i = 0; i < 3; i++) c.fillRect(W * 0.25, H * (0.74 + 0.06 * i), W * 0.5, H * 0.022); }, { res: 256 });
    bk.position.z = -d / 2 - 0.002; bk.rotation.y = PI; g.add(bk);
    return g;
  },

  // (pass 2) A wall calendar that loses its years (pivot at its middle, front +Z): a red header on two rings, a big year; from o.from the pages rip
  // off one after the other, faster and faster, each flying up and out on an arc and turning (two or three in the air at once); the last year
  // (o.years [y0, y1]) lands at o.land with a little squash and stays
  tearCalendar(o) {
    const ys = o.years || [2016, 2026], n = ys[1] - ys[0] + 1, t0 = o.from ?? 0.1, t1 = o.land ?? 1.0, fly = o.fly ?? 0.6, g = grp(), body = grp();
    body.add(at(box(0.56, 0.62, 0.02, '#F4F1E8', { outline: 0.005 }), 0, 0, 0), at(box(0.56, 0.12, 0.025, '#C8322A'), 0, 0.25, 0.003));
    for (const x of [-0.16, 0.16]) body.add(at(cyl(0.012, 0.012, 0.05, '#3A3D44', 6), x, 0.31, 0.02));
    g.add(body);
    const page = y => canvasPlane(0.5, 0.42, (c, W, H) => { c.fillStyle = '#F4F1E8'; c.fillRect(0, 0, W, H); c.fillStyle = '#1C252A'; c.font = `900 ${H * 0.44}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(String(y), W / 2, H * 0.42);
      c.fillStyle = '#8A8F96'; c.font = `700 ${H * 0.12}px Arial`; c.fillText('JANVIER', W / 2, H * 0.84); }, { res: 256 });
    const pages = []; for (let i = 0; i < n; i++) { const pv = new THREE.Group(), pl = page(ys[0] + i); pl.position.y = -0.21; pv.add(pl); pv.position.set(0, 0.15, 0.012 + 0.0008 * (n - i)); g.add(pv); pages.push(pv); }
    // page i (i < n - 1) rips off at T[i]: the gaps shrink (an ease-in over the years)
    const T = []; for (let i = 0; i < n - 1; i++) T.push(t0 + (t1 - t0) * Math.pow(i / (n - 1), 0.75));
    g.userData.update = t => { let top = 0; for (let i = 0; i < n - 1; i++) if (t >= T[i]) top = i + 1;
      pages.forEach((pv, i) => { const u = i < n - 1 ? t - T[i] : -1; pv.scale.set(1, 1, 1);
        if (i < top) { if (u > fly) { pv.visible = false; return; } pv.visible = true; const sd = i % 2 ? 1 : -1, q = u / fly;
          pv.position.set(sd * (0.5 + 0.45 * hash(i)) * u * 2, 0.2 + 2.6 * u - 1.5 * u * u, 0.03 + 0.14 * u); pv.rotation.set(-1.9 * q, 0.6 * sd * q, sd * (0.4 + 1.3 * q)); }   // (stills 2) up and out, not at the lens: the year under them stays in view
        else { pv.visible = i === top || i === top + 1; pv.position.set(0, 0.15, 0.012 + 0.0008 * (n - i)); pv.rotation.set(0, 0, 0); } });
      const ul = t - t1, k = ul >= 0 && ul < 0.4 ? Math.exp(-7 * ul) * Math.cos(ul * 26) : 0; body.scale.set(1 + 0.07 * k, 1 - 0.09 * k, 1); pages[n - 1].scale.set(1 + 0.07 * k, 1 - 0.09 * k, 1);
      const sh = t >= t0 && t < t1 ? 0.012 * Math.sin(t * 70) : 0; g.rotation.z = sh; };
    g.userData.update(0); return g;
  },

  // (pass 2) A speech bubble with its tail on whoever speaks (pivot at the tip of the tail; face it to the camera): a white bubble with a dark edge,
  // jagged like an electronic voice (o.jag false: round), o.text in it; it pops in at o.at with an overshoot; o.w wide (0.4); o.side 1: the bubble
  // sits up and to the right of the tip (-1: to the left)
  voiceBubble(o) {
    const w = o.w ?? 0.4, hh = w * 0.72, sd = o.side ?? 1, g = grp();
    const pl = canvasPlane(w, hh, (c, W, H) => { c.clearRect(0, 0, W, H); const cx = W * 0.54, cy = H * 0.4, rx = W * 0.4, ry = H * 0.3, n = 18; c.lineJoin = 'round';
      c.beginPath(); c.moveTo(W * 0.04, H * 0.97); c.lineTo(W * 0.3, H * 0.52); c.lineTo(W * 0.46, H * 0.62); c.closePath(); c.fillStyle = '#FFFFFF'; c.fill(); c.lineWidth = H * 0.035; c.strokeStyle = '#1C1C1E'; c.stroke();
      c.beginPath(); for (let i = 0; i <= 2 * n; i++) { const a = i * PI / n, r = o.jag === false ? 1 : (i % 2 ? 0.86 : 1.0); c.lineTo(cx + Math.cos(a) * rx * r, cy + Math.sin(a) * ry * r); } c.closePath(); c.fill(); c.stroke();
      c.beginPath(); c.moveTo(W * 0.1, H * 0.9); c.lineTo(W * 0.31, H * 0.56); c.lineTo(W * 0.43, H * 0.6); c.closePath(); c.fill();
      c.fillStyle = '#1C1C1E'; c.textAlign = 'center'; c.textBaseline = 'middle'; const tx = o.text || 'BIP'; let px = H * 0.3; c.font = `900 ${px}px Arial`; const tw = c.measureText(tx).width; if (tw > rx * 1.45) { px *= rx * 1.45 / tw; c.font = `900 ${px}px Arial`; } c.fillText(tx, cx, cy + px * 0.04); }, { res: 256, transparent: true });
    pl.material.depthWrite = false; pl.scale.x = sd; pl.position.set(sd * w * 0.46, hh * 0.47, 0); const pv = new THREE.Group(); pv.add(pl); g.add(pv);
    g.userData.update = t => { const u = t - (o.at ?? 0); if (u < 0) { pv.visible = false; return; } pv.visible = true; const k = u < 0.3 ? 1 + 0.35 * Math.exp(-9 * u) * Math.cos(u * 22) - Math.exp(-30 * u) : 1; pv.scale.setScalar(Math.max(0.01, k) * (1 + 0.03 * Math.sin(u * 14))); };
    g.userData.update(-1); return g;
  },

  // A brass band instrument to hold (pivot at the grip): o.kind 'trumpet' (a gold tube and bell pointing +Z), 'tuba' (a big gold coil with the bell
  // up) or 'drum' (a red drum on a strap, o.beat [t...]: the skin jumps); o.s scale
  brass(o) {
    const G = o.color || '#E2B53C', g = grp(), k = o.kind || 'trumpet';
    if (k === 'trumpet') { const tube = at(cyl(0.012, 0.012, 0.32, G, 8, { outline: 0.003 }), 0, 0.02, 0.1); tube.rotation.x = PI / 2; g.add(tube);
      const bell = at(new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.12, 14, 1, true), new THREE.MeshLambertMaterial({ color: G, side: THREE.DoubleSide })), 0, 0.02, 0.3); bell.rotation.x = -PI / 2; g.add(bell);
      for (const z of [0.02, 0.06, 0.1]) g.add(at(cyl(0.008, 0.008, 0.06, '#C9A043', 6), 0, 0.06, z)); }
    else if (k === 'tuba') { const coil = new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.035, 8, 18), new THREE.MeshLambertMaterial({ color: G })); coil.position.set(0, 0.1, 0); g.add(coil);
      const bell = at(new THREE.Mesh(new THREE.ConeGeometry(0.17, 0.26, 16, 1, true), new THREE.MeshLambertMaterial({ color: G, side: THREE.DoubleSide })), 0.12, 0.38, 0); bell.rotation.z = PI; g.add(bell); }
    else { const dr = grp(at(cyl(0.18, 0.18, 0.2, '#C8322A', 16, { outline: 0.004 }), 0, 0, 0), at(cyl(0.185, 0.185, 0.02, '#F4F1E8', 16), 0, 0.105, 0), at(cyl(0.185, 0.185, 0.02, '#F4F1E8', 16), 0, -0.105, 0)); dr.rotation.x = PI / 2; g.add(dr);
      const skin = dr.children[1]; g.userData.update = t => { let a = 0; for (const b of o.beat || []) { const u = t - b; if (u >= 0 && u < 0.15) a = Math.max(a, Math.exp(-u * 30)); } skin.position.y = 0.105 + 0.02 * a; }; }
    if (o.s) g.scale.setScalar(o.s); return g;
  },

  // A bridal veil (attach to the head joint; pivot at the crown): a white comb and a long sheer veil falling down the back, swaying a little
  bridalVeil(o) {
    const g = grp(), L = o.len ?? 0.9, W = o.w ?? 0.5;
    g.add(at(box(0.22, 0.03, 0.06, '#F4F1E8', { outline: 0.003 }), 0, 0.02, 0));
    const m = new THREE.MeshLambertMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.72, side: THREE.DoubleSide, depthWrite: false });
    const geo = new THREE.PlaneGeometry(W, L, 4, 8); geo.translate(0, -L / 2, 0); const veil = new THREE.Mesh(geo, m); veil.position.set(0, 0.02, -0.06); veil.rotation.x = 0.18; g.add(veil);
    const p0 = geo.attributes.position.array.slice();
    g.userData.update = t => { const a = geo.attributes.position.array; for (let i = 0; i < a.length; i += 3) { const y = p0[i + 1], f = -y / L; a[i + 2] = p0[i + 2] - 0.05 * f * f * (1 + Math.sin(t * 2.2 + p0[i] * 4)); } geo.attributes.position.needsUpdate = true; };
    g.userData.update(0); return g;
  },

  // A flagpole with a flag that rises (pivot at the foot): a white pole o.h high (6), a tricolour flag climbing it between o.raise [t0, t1] and
  // flapping
  flagPole(o) {
    const H = o.h ?? 6, g = grp(), fw = o.w ?? 1.5, fh = fw * 0.66;
    g.add(at(cyl(0.05, 0.06, H, '#EDEDED', 8, { pivot: 'bottom', outline: 0.004 }), 0, 0, 0), at(sphere(0.08, '#E2B53C', 1), 0, H + 0.04, 0));
    const fl = grp(); const cols = o.colors || ['#2F62B5', '#F4F4F0', '#E0413A'];
    cols.forEach((c, i) => { const geo = new THREE.PlaneGeometry(fw / cols.length, fh, 3, 1); const s = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ color: c, side: THREE.DoubleSide })); s.position.set(0.06 + fw / cols.length * (i + 0.5), 0, 0); fl.add(s); });
    g.add(fl);
    g.userData.update = t => { const [a, b] = o.raise || [-1, -0.5], k = clamp01((t - a) / (b - a)); fl.position.y = 0.6 + (H - fh / 2 - 0.7) * k;
      fl.children.forEach((s, i) => { s.rotation.y = 0.12 * Math.sin(t * 5 + i * 0.9); s.position.z = 0.04 * Math.sin(t * 5 + i * 0.9); }); };
    g.userData.update(0); return g;
  },

  // A phone's call screen with its keypad, big for an insert (pivot at its middle, screen +Z): a phone o.w wide (0.5), a timer line on top
  // (o.label), twelve round keys; o.pressAt: the key '1' lights up green and sinks at that time
  // (pass 2) o.case: the colour of the phone (black; the story's red), with the stub antenna of bigPhone; o.hold 1: a hand and a navy sleeve hold it
  // from below; o.finger 1: a pointing hand comes in from the lower right, its index lands on the 1 at o.pressAt, presses, lifts and goes back down
  // to the corner within about 0.2 s: the green key stays in the clear
  phoneKeypad(o) {
    const w = o.w ?? 0.5, h = w * 2.0, col = o.case || '#17181C', g = grp(at(box(w, h, 0.04 + (o.case ? 0.1 : 0), col, { outline: 0.006 }), 0, 0, o.case ? -0.05 : 0));
    if (o.case) g.add(at(cyl(0.04, 0.04, 0.26, col, 8, { outline: 0.006 }), -w * 0.3, h / 2 + 0.13, -0.05), at(sphere(0.065, '#1C1C1E', 1), -w * 0.3, h / 2 + 0.29, -0.05));
    const draw = lit => (c, W, H) => { c.fillStyle = '#0E1A26'; c.fillRect(0, 0, W, H); c.fillStyle = '#CFE3F2'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `700 ${W * 0.07}px Arial`; c.fillText(o.label || 'EN ATTENTE', W / 2, H * 0.08);
      const keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#'];
      keys.forEach((kk, i) => { const x = W * (0.22 + 0.28 * (i % 3)), y = H * (0.3 + 0.16 * Math.floor(i / 3)); c.fillStyle = lit && kk === '1' ? '#3CCB6A' : '#2A3846'; c.beginPath(); c.arc(x, y, W * (lit && kk === '1' ? 0.125 : 0.11), 0, TAU); c.fill();
        if (lit && kk === '1') { c.strokeStyle = '#BDF5CF'; c.lineWidth = W * 0.018; c.stroke(); }
        c.fillStyle = '#FFFFFF'; c.font = `700 ${W * 0.1}px Arial`; c.fillText(kk, x, y + W * 0.005); }); };
    const off = canvasPlane(w * 0.9, h * 0.92, draw(false), { res: 256, emissive: 0.3 }), on = canvasPlane(w * 0.9, h * 0.92, draw(true), { res: 256, emissive: 0.55 }); off.position.z = on.position.z = 0.021; g.add(off, on);
    const k1 = [w * 0.9 * (0.22 - 0.5), h * 0.92 * (0.5 - 0.3)];   // the middle of the key 1
    if (o.hold) { const hd = grp(at(box(w * 0.7, w * 0.42, 0.22, SKIN, { outline: 0.006 }), 0, -h * 0.34, -0.2), at(box(w * 0.17, w * 0.5, 0.1, SKIN, { outline: 0.005 }), -w * 0.56, -h * 0.26, -0.02),
        at(box(w * 0.78, w * 1.6, 0.3, '#1F3550', { outline: 0.006 }), 0, -h * 0.34 - w * 1.0, -0.22), at(box(w * 0.8, w * 0.12, 0.31, '#FAF8F2'), 0, -h * 0.34 - w * 0.24, -0.22));
      for (let i = 0; i < 4; i++) hd.add(at(box(w * 0.2, w * 0.13, 0.1, SKIN, { outline: 0.004 }), w * 0.52, -h * 0.4 + i * w * 0.16, -0.02)); g.add(hd); }
    let fg = null;
    if (o.finger) { fg = grp(); const L = w * 0.62;   // the index along -X+Y (toward the upper left), its tip at the group's origin
      const idx = at(box(L, w * 0.15, w * 0.14, SKIN, { outline: 0.005 }), L / 2, 0, 0), fist = at(box(w * 0.5, w * 0.46, w * 0.3, SKIN, { outline: 0.006 }), L + w * 0.22, -w * 0.1, 0),
        cuff = at(box(w * 0.14, w * 0.5, w * 0.34, '#FAF8F2'), L + w * 0.52, -w * 0.1, 0), arm = at(box(w * 2.4, w * 0.52, w * 0.36, '#1F3550', { outline: 0.006 }), L + w * 1.78, -w * 0.1, 0);
      const nail = at(box(w * 0.1, w * 0.11, 0.004, '#F1CBA4'), w * 0.07, 0, w * 0.072); fg.add(idx, fist, cuff, arm, nail); fg.rotation.z = -0.62; g.add(fg); }
    g.userData.update = t => { const pa = o.pressAt, p = pa != null && t >= pa; on.visible = p; off.visible = !p;
      if (fg && pa != null) { const u = t - pa, rest = [w * 0.62, -h * 0.52], far = [w * 1.5, -h * 0.95];   // far (out of frame) -> the key (u = 0) -> rest (the lower right corner, the key in the clear)
        const e = x => x < 0.5 ? 2 * x * x : 1 - 2 * (1 - x) * (1 - x); let x, y, z;
        if (u < -0.22) { [x, y] = far; z = 0.12; } else if (u < 0) { const q = e((u + 0.22) / 0.22); x = far[0] + (k1[0] - far[0]) * q; y = far[1] + (k1[1] - far[1]) * q; z = 0.12 - 0.09 * q; }
        else if (u < 0.07) { x = k1[0]; y = k1[1]; z = 0.03 - 0.012 * Math.sin(u / 0.07 * PI); }
        else { const q = e(Math.min(1, (u - 0.07) / 0.16)); x = k1[0] + (rest[0] - k1[0]) * q; y = k1[1] + (rest[1] - k1[1]) * q; z = 0.03 + 0.08 * q; x += 0.004 * Math.sin(u * 5); }
        fg.position.set(x, y, z); }
      const up = pa != null ? t - pa : -1, kk = up >= 0 && up < 0.3 ? Math.exp(-10 * up) * Math.cos(up * 30) : 0; on.scale.setScalar(1 + 0.02 * kk); };
    g.userData.update(-1); return g;
  },
};
