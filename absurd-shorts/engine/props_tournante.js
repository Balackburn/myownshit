// « La porte tournante » (story 57, cycle 19): a man went into a revolving door and never came out; he has been turning for three years; the power
// station plugged him into the grid; he lights the whole neighbourhood; the gym gave him a membership; yesterday the door stopped; he did not; the
// station bills him for the blackout. Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure
// function of the shot time.
import * as THREE from 'three';
import { mat, box, cyl, sphere, addOutline } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const list = v => [].concat(v ?? []);
// a value keyed in time: [[t, v], ...], linear between keys, held before the first and after the last
function lin(ks, t, dflt) {
  const k = list(ks); if (!k.length) return dflt;
  if (t <= k[0][0]) return k[0][1];
  for (let i = 1; i < k.length; i++) if (t < k[i][0]) { const [t0, v0] = k[i - 1], [t1, v1] = k[i]; return v0 + (v1 - v0) * (t - t0) / Math.max(1e-6, t1 - t0); }
  return k[k.length - 1][1];
}
// the integral from 0 to t of a rate keyed linearly ([[t, rate], ...], held outside the keys): how far a thing turning at that rate has turned
function integ(ks, t) {
  const k = list(ks); if (!k.length) return 0;
  let s = 0, prevT = 0, prevV = lin(k, 0, 0);
  const pts = k.map(p => p[0]).filter(x => x > 0 && x < t).concat([t]);
  for (const x of pts) { const v = lin(k, x, 0); s += (prevV + v) / 2 * (x - prevT); prevT = x; prevV = v; }
  return t < 0 ? 0 : s;
}
const glassMat = (op = 0.28) => new THREE.MeshStandardMaterial({ color: '#CFE6EE', transparent: true, opacity: op, roughness: 0.08, metalness: 0.1, depthWrite: false, side: THREE.DoubleSide });

export const TOURNANTE_PROPS = {
  // A revolving door (pivot at the floor in its middle, front +Z, the two openings toward ±Z): a drum o.r (1.0) wide and o.h (2.4) tall, curved glass
  // walls on its ±X sides, a dark metal canopy with a sign (o.text, 'ENTRÉE') over the front opening, a centre post and four glass wings with metal
  // frames. o.spin [[t, turns per second], ...] (linear between keys): the wings turn by the integral of that rate (a stop is a key at 0); above about
  // one turn a second a pale drum of blur fills between the wings; o.bulbs [[t, k]]: a ring of bulbs round the canopy lights up (0..1); o.wings false:
  // the drum alone. userData.angleAt(t): the wings' angle (rad), for a script that times something on a wing.
  revolvingDoor(o) {
    // (stills 2) o.glass [wall, wing] opacities (0.12, 0.07): seen through a wall and two panes a man inside came out grey (0.3 and 0.2)
    // (pass 2) o.frame: the colour of the posts and the wings' frames (brass: a navy suit read against navy posts at 1.07 to 1)
    const R = o.r ?? 1.0, H = o.h ?? 2.4, g = grp(), metal = o.metal || '#3A4048', frame = o.frame || metal;
    g.add(at(cyl(R + 0.04, R + 0.04, 0.03, '#5A6068', 32), 0, 0.015, 0));                                         // the floor plate
    g.add(at(cyl(R + 0.08, R + 0.08, 0.22, metal, 32), 0, H + 0.11, 0));                                            // the canopy
    for (const s of [-1, 1]) {   // the curved glass walls and their metal edges, on the ±X sides
      const wall = new THREE.Mesh(new THREE.CylinderGeometry(R, R, H, 20, 1, true, s > 0 ? PI / 4 : 5 * PI / 4, PI / 2), glassMat(o.glass?.[0] ?? 0.12)); wall.position.y = H / 2; g.add(wall);
      for (const a of [PI / 4, 3 * PI / 4]) { const th = s > 0 ? a : a + PI; g.add(at(box(0.06, H, 0.06, frame, { outline: 0.004 }), R * Math.sin(th), H / 2, R * Math.cos(th))); }
    }
    const sign = canvasPlane(1.4, 0.18, (c, W, Ht) => { c.fillStyle = '#1C2A3A'; c.fillRect(0, 0, W, Ht); c.fillStyle = '#F2D27A'; c.textAlign = 'center'; c.textBaseline = 'middle';
      let fs = Ht * 0.62; c.font = `900 ${fs}px Arial`; const tw = c.measureText(o.text || 'ENTRÉE').width; if (tw > W * 0.9) { fs *= W * 0.9 / tw; c.font = `900 ${fs}px Arial`; } c.fillText(o.text || 'ENTRÉE', W / 2, Ht * 0.54); }, { res: 512 });
    sign.position.set(0, H + 0.11, R + 0.085); g.add(sign);
    const bulbs = []; for (let i = 0; i < 18; i++) { const a = i / 18 * TAU, b = new THREE.Mesh(new THREE.SphereGeometry(0.035, 8, 6), new THREE.MeshStandardMaterial({ color: '#F4E6B8', emissive: '#FFD45A', emissiveIntensity: 0 }));
      b.position.set((R + 0.1) * Math.sin(a), H + 0.02, (R + 0.1) * Math.cos(a)); g.add(b); bulbs.push(b); }
    const rot = grp(); g.add(rot);
    if (!((o.inner ?? 0) > 0.2)) rot.add(at(cyl(0.05, 0.05, H, metal, 10), 0, H / 2, 0));   // (stills 3) no central post when a man turns at the axis: from the riding camera it came out through his face
    // o.inner: the wings start that far from the axis (0.05): room in the middle for a man who turns with the door (the post hidden in him)
    const r0 = o.inner ?? 0.05;
    if (o.wings !== false) for (let i = 0; i < 4; i++) { const w = grp(); w.rotation.y = i * PI / 2; rot.add(w);
      const L = R - 0.06 - r0, pane = new THREE.Mesh(new THREE.BoxGeometry(0.025, H - 0.16, L - 0.06), glassMat(o.glass?.[1] ?? 0.07)); pane.position.set(0, H / 2, r0 + (L - 0.06) / 2); w.add(pane);
      for (const y of [0.06, H - 0.06]) w.add(at(box(0.05, 0.08, L, frame, { outline: 0.004 }), 0, y, r0 + L / 2));
      w.add(at(box(0.05, H - 0.04, 0.05, frame, { outline: 0.004 }), 0, H / 2, r0 + L)); w.add(at(box(0.05, H - 0.04, 0.05, frame, { outline: 0.004 }), 0, H / 2, r0));
      w.add(at(box(0.04, 0.05, L * 0.6, '#C9CCD1'), 0.03, 1.05, r0 + L * 0.55)); }
    // (pass 2) the blur only on the drum's far side, behind him (both sides veiled him grey: suit saturation 0.14), with streaks round it
    const streak = document.createElement('canvas'); streak.width = 256; streak.height = 64; { const c = streak.getContext('2d'); c.fillStyle = 'rgba(230,242,246,0.55)'; c.fillRect(0, 0, 256, 64); c.fillStyle = 'rgba(255,255,255,0.95)'; for (let i = 0; i < 9; i++) c.fillRect((i * 53) % 256, 4 + i * 6.5, 70 + (i % 3) * 30, 2.2); }
    const stex = new THREE.CanvasTexture(streak); stex.wrapS = THREE.RepeatWrapping; stex.repeat.set(3, 1);
    const blur = new THREE.Mesh(new THREE.CylinderGeometry(R - 0.06, R - 0.06, H - 0.16, 28, 1, true), new THREE.MeshBasicMaterial({ map: stex, color: '#FFFFFF', transparent: true, opacity: 0, depthWrite: false, side: THREE.BackSide }));
    blur.position.y = H / 2; g.add(blur);
    g.userData.angleAt = t => TAU * integ(o.spin, t);
    g.userData.update = t => {
      rot.rotation.y = TAU * integ(o.spin, t);
      const rate = Math.abs(lin(o.spin, t, 0)); blur.material.opacity = Math.max(0, Math.min(0.82, (rate - 0.9) * 0.6)); blur.visible = blur.material.opacity > 0.01; stex.offset.x = -TAU * integ(o.spin, t) / TAU * 3;   // (stills v1) faint: a man turning at the axis is inside the drum and a thick blur whitened him; (pass 2) behind him only, so it can be strong
      const bk = lin(o.bulbs, t, 0); bulbs.forEach((b, i) => { b.material.emissiveIntensity = bk * (0.75 + 0.25 * Math.sin(t * 9 + i * 1.3)) * 2.2; });
    };
    g.userData.update(0); return g;
  },

  // A long beard (pivot at the chin, hanging along -Y, the face +Z): one tapered hanging mass o.len (0.7) long, o.color, swept out to one side by o.sweep
  // (rad, about Z) and out in front by o.lift (rad, about X): grown while he turned for three years (a fan of dark sticks read as a comb).
  longBeard(o) {
    // (pass 3 of 57) a chain of tapering, rounded tufts that curves and waves, a pointed tip, in his hair colour: six hard brown boxes read as a brick or
    // a plank on his chest. o.len (0.7), o.w (0.2), o.color, o.sweep: the curl to one side over its length (the trail of the spin), o.lift: forward,
    // o.wave [amp, rate]: a whip running down it
    const L = o.len ?? 0.7, w0 = o.w ?? 0.2, c = o.color || '#2B2622', N = 6, segL = L / N, g = grp(), segs = [];
    let parent = g;
    for (let i = 0; i < N; i++) {
      const u = i / N, w = w0 * (1 - 0.72 * u), seg = grp(); seg.position.y = i ? -segL : 0; parent.add(seg); parent = seg;
      const tuft = sphere(w * 0.55, c, 1); tuft.scale.set(1, (segL * 0.68) / (w * 0.55), 0.55); tuft.position.set(i % 2 ? 0.014 : -0.014, -segL * 0.5, 0.02 + 0.015 * u); addOutline(tuft, 0.05); seg.add(tuft);
      segs.push(seg);
    }
    const tip = new THREE.Mesh(new THREE.ConeGeometry(w0 * 0.14, segL * 0.9, 6).rotateX(PI), mat(c)); tip.position.y = -segL * 1.05; parent.add(tip);
    const base = segs.map((sg, i) => [(o.lift ?? 0.15) / N * (i ? 1 : 0.5), (o.sweep ?? 0) / N * (1 + 0.4 * Math.sin(i * 1.4))]);
    g.userData.update = t => { const [amp, rate] = o.wave || [0.12, 9]; segs.forEach((sg, i) => { sg.rotation.set(base[i][0], 0, base[i][1] + amp * Math.sin(t * rate - i * 0.9) * (i / N)); }); };
    g.userData.update(0);
    return g;
  },

  // A thick power cable from the origin (a big plug pushed into a socket box) to o.to [x, y, z] in the prop's frame, sagging by o.sag (0.3), o.color;
  // o.sparkAt [t...]: a crackle of yellow sparks at the plug for 0.3 s; o.flow [[t, k]]: bright dashes run along it toward o.to (the current)
  powerCable(o) {
    const to = o.to || [3, 0, 0], sag = o.sag ?? 0.3, g = grp();
    const mid = [to[0] / 2, Math.min(0, to[1]) / 2 - sag + 0.08, to[2] / 2], curve = new THREE.CatmullRomCurve3([new THREE.Vector3(0, 0.08, 0), new THREE.Vector3(...mid), new THREE.Vector3(...to)]);
    g.add(new THREE.Mesh(new THREE.TubeGeometry(curve, 40, o.r ?? 0.035, 8, false), mat(o.color || '#1B1C20')));
    g.add(at(box(0.22, 0.2, 0.12, '#E7E3D6', { outline: 0.006 }), 0, 0.1, -0.06), at(box(0.16, 0.14, 0.16, '#2A2C31', { outline: 0.006 }), 0, 0.1, 0.06));   // the socket box and the plug
    for (const x of [-0.04, 0.04]) g.add(at(cyl(0.008, 0.008, 0.06, '#C9A33A', 6), x, 0.1, 0.0, PI / 2, 0, 0));
    const dashes = []; for (let i = 0; i < 9; i++) { const d = new THREE.Mesh(new THREE.SphereGeometry((o.r ?? 0.035) * 1.25, 8, 6), new THREE.MeshBasicMaterial({ color: '#FFE36A', toneMapped: false })); g.add(d); dashes.push(d); }
    const sk = o.sparkSize ?? 1, sparks = []; for (let i = 0; i < 7; i++) { const s = new THREE.Mesh(new THREE.BoxGeometry(0.012 * sk, 0.09 * sk, 0.012 * sk), new THREE.MeshBasicMaterial({ color: '#FFE36A', toneMapped: false })); g.add(s); sparks.push(s); }   // (pass 3 of 57) o.sparkSize: two yellow specks at 1
    g.userData.update = t => {
      const fk = lin(o.flow, t, 0); dashes.forEach((d, i) => { const u = ((t * 0.9 + i / dashes.length) % 1); d.visible = fk > 0.02; d.position.copy(curve.getPointAt(u)); d.scale.setScalar(Math.max(0.01, fk)); });
      const s0 = list(o.sparkAt).filter(x => t >= x && t < x + 0.3).pop(); sparks.forEach((s, i) => { s.visible = s0 != null; if (!s.visible) return; const u = (t - s0) / 0.3, a = i / sparks.length * TAU + t * 3;
        s.position.set(Math.cos(a) * (0.08 + 0.25 * u), 0.12 + Math.sin(a * 1.7) * 0.15 * u, 0.12 + Math.sin(a) * (0.08 + 0.25 * u)); s.rotation.set(a, 0, a * 0.7); s.scale.setScalar(1 - u); });
    };
    g.userData.update(0); return g;
  },

  // An electricity meter on its post (front +Z, pivot at the floor): a grey box with a window, a disc that turns at o.spin [[t, turns/s]] and a
  // counter (o.count [[t, value]], kWh) whose digits roll; o.h (1.4) to the middle of the box
  meterBox(o) {
    const h = o.h ?? 1.4, g = grp(at(box(0.06, h - 0.2, 0.06, '#5A6068'), 0, (h - 0.2) / 2, -0.08), at(box(0.42, 0.5, 0.16, '#C9CCD1', { outline: 0.008 }), 0, h, 0));
    g.add(at(box(0.34, 0.36, 0.01, '#1C252A'), 0, h + 0.02, 0.081));
    const disc = grp(at(cyl(0.11, 0.11, 0.012, '#D7D9DC', 24), 0, 0, 0, PI / 2, 0, 0), at(box(0.02, 0.11, 0.014, '#D7262E'), 0, 0.055, 0.004)); disc.position.set(0, h - 0.06, 0.09); g.add(disc);
    let lastV = null; const cv = document.createElement('canvas'); cv.width = 256; cv.height = 64; const ctx = cv.getContext('2d'), tex = new THREE.CanvasTexture(cv);
    const panel = new THREE.Mesh(new THREE.PlaneGeometry(0.3, 0.075), new THREE.MeshBasicMaterial({ map: tex, toneMapped: false })); panel.position.set(0, h + 0.12, 0.088); g.add(panel);
    const draw = v => { const n = String(Math.floor(v)).padStart(6, '0').slice(-6); ctx.fillStyle = '#101418'; ctx.fillRect(0, 0, 256, 64); for (let i = 0; i < 6; i++) { ctx.fillStyle = i === 5 ? '#B8262E' : '#F4F1E8';
      ctx.fillRect(6 + i * 41, 6, 36, 52); ctx.fillStyle = i === 5 ? '#FFFFFF' : '#101418'; ctx.font = '900 44px Arial'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(n[i], 24 + i * 41, 34); } tex.needsUpdate = true; };
    g.userData.update = t => { disc.rotation.z = -TAU * integ(o.spin, t); const v = lin(o.count, t, 0); if (lastV !== Math.floor(v)) { lastV = Math.floor(v); draw(v); } };
    g.userData.update(0); return g;
  },

  // A row of town buildings at night (pivot at the floor in the middle, front +Z): o.n (7) dark blocks of seeded heights with a grid of windows that
  // light up in a wave from -X to +X between o.wave[0] and o.wave[1] (dark before), a few left dark; a sky of stars behind; o.w (14) wide
  nightSkyline(o) {
    const n = o.n ?? 7, W = o.w ?? 14, g = grp(), wins = [], rnd = s => { const x = Math.sin(s * 91.7) * 43758.5; return x - Math.floor(x); };
    for (let i = 0; i < n; i++) { const bw = W / n * 0.92, bh = 4 + rnd(i + 3) * 6, x = -W / 2 + (i + 0.5) * W / n;
      g.add(at(box(bw, bh, 2.0, ['#1E2638', '#232C40', '#1A2132'][i % 3], { outline: 0.01 }), x, bh / 2, 0));
      const cols = 3, rows = Math.floor((bh - 1) / 0.9);
      for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) { const m = new THREE.Mesh(new THREE.PlaneGeometry(bw / cols * 0.5, 0.45), new THREE.MeshStandardMaterial({ color: '#2B3346', emissive: '#FFD46A', emissiveIntensity: 0 }));
        const wx = x - bw / 2 + (c + 0.5) * bw / cols; m.position.set(wx, 0.9 + r * 0.9, 1.006); g.add(m); wins.push({ m, x: wx, dead: rnd(i * 37 + r * 7 + c) < 0.12 }); } }
    const xs = wins.map(w => w.x), x0 = Math.min(...xs), x1 = Math.max(...xs);
    g.userData.update = t => { const [a, b] = o.wave || [0, 0]; wins.forEach((w, i) => { const tl = a + (b - a) * (w.x - x0) / Math.max(1e-6, x1 - x0) + rnd(i * 3.3) * 0.12; const on = !w.dead && t >= tl;
      w.m.material.emissiveIntensity = on ? 1.8 : 0; w.m.material.color.set(on ? '#FFE9A8' : '#2B3346'); }); };
    g.userData.update(0); return g;
  },

  // The gym's membership card (front +Z, pivot at its centre): o.s (1: 0.17 x 0.107 m), white and orange, ABONNEMENT, a dumbbell; o.bright: unlit
  gymCard(o) {
    const s = o.s ?? 1, pl = canvasPlane(0.17 * s, 0.107 * s, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.fillStyle = '#F28C28'; c.fillRect(0, 0, W, H * 0.3);
      c.fillStyle = '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${H * 0.18}px Arial`; c.fillText('SALLE DE SPORT', W / 2, H * 0.15);
      c.fillStyle = '#1C252A'; let fs = H * 0.2; c.font = `900 ${fs}px Arial`; const tw = c.measureText('ABONNEMENT').width; if (tw > W * 0.9) { fs *= W * 0.9 / tw; c.font = `900 ${fs}px Arial`; } c.fillText('ABONNEMENT', W / 2, H * 0.5);
      c.fillStyle = '#F28C28'; c.fillRect(W * 0.32, H * 0.74, W * 0.36, H * 0.05); for (const x of [0.3, 0.66]) c.fillRect(W * x, H * 0.66, W * 0.05, H * 0.21); }, { res: 384 });
    if (o.bright) pl.material = new THREE.MeshBasicMaterial({ map: pl.material.map, side: THREE.DoubleSide, toneMapped: false });
    return grp(pl, at(box(0.172 * s, 0.109 * s, 0.003, '#D9D9D9'), 0, 0, -0.002));
  },
};
