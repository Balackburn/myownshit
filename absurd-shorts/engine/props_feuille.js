// « La feuille » (story 86): this man cut himself on a sheet of paper; she melted into the crowd; description: white, rectangular; the police
// took in all the paper in the country, and every banknote, and the intern for harbouring a criminal; the finger recognised her; the prosecutor
// asked for the shredder; the president put the shredder to a referendum; fifty million ballots, a whole forest; the ballots all voted no, his
// first; the shredder was abolished; the gendarmes flattened every shredder; the sheet was released, turned into a dismissal letter, addressed
// to this man; he sold shredders.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere, addOutline, mat, rng } from './style.js';
import { grp, at, canvasPlane, buildProp, rod, label, inst, glassMat } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const outBack = x => { const u = clamp01(x), c = 1.70158; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const easeIn = x => { const u = clamp01(x); return u * u; };
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
const PAPER = '#F7F5EE', PAPER_BACK = '#ECE8DE', SMEAR = '#C8202A', INK = '#1B1B1E';
// the paper's canvas: white, the red smear low on the left edge, an optional typed word (o.text) revealed letter by letter
function sheetCanvas(w, h, o, back) {
  const cv = document.createElement('canvas'); cv.width = 384; cv.height = Math.round(384 * h / w); const c = cv.getContext('2d');
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
  const W = cv.width, H = cv.height, E = Math.round(W * (o.ear ?? 0.22));
  let shown = -1;
  const draw = n => {
    c.clearRect(0, 0, W, H); c.fillStyle = back ? PAPER_BACK : PAPER;
    c.beginPath(); c.moveTo(0, 0); c.lineTo(W - (o.ear === 0 ? 0 : E), 0); c.lineTo(W, o.ear === 0 ? 0 : E); c.lineTo(W, H); c.lineTo(0, H); c.closePath(); c.fill();
    if (!back && o.lines !== false) { c.fillStyle = 'rgba(40,60,90,0.10)'; for (let y = H * 0.62; y < H * 0.93; y += H * 0.06) c.fillRect(W * 0.1, y, W * 0.8, Math.max(1, H * 0.006)); }
    const sd = o.smearSide || 'both'; if (o.smear !== false && (sd === 'both' || (sd === 'back') === !!back)) { c.fillStyle = SMEAR; c.beginPath(); c.ellipse(W * 0.035, H * 0.78, W * 0.05, H * 0.035, 0.4, 0, TAU); c.fill(); c.beginPath(); c.ellipse(W * 0.075, H * 0.8, W * 0.03, H * 0.016, 0.2, 0, TAU); c.fill(); }
    if (!back && o.text && n > 0) {
      const s = o.text.slice(0, n); c.fillStyle = INK; c.textAlign = 'left'; c.textBaseline = 'middle';
      let fs = Math.round(H * 0.11); c.font = `bold ${fs}px "Courier New", monospace`; while (c.measureText(o.text).width > W * 0.86 && fs > 8) { fs -= 2; c.font = `bold ${fs}px "Courier New", monospace`; }
      c.fillText(s, W * 0.07, H * (o.textY ?? 0.3));
      c.fillStyle = 'rgba(27,27,30,0.55)'; for (let i = 0; i < 4; i++) c.fillRect(W * 0.07, H * (0.42 + i * 0.045), W * (0.78 - (i === 3 ? 0.3 : 0)), Math.max(1, H * 0.012));
    }
    tex.needsUpdate = true;
  };
  return { tex, set: n => { if (n !== shown) { shown = n; draw(n); } } };
}

export const FEUILLE_PROPS = {
  // THE sheet (pivot at its centre, front +Z, upright): a paper plane o.w (0.42) x o.h (0.56) of 8 x 10 cells, a dog-ear folded over at the top
  // right corner and a small red smear (his blood) low on the left edge, seen on both faces. o.text: a typed word on the front (o.typeAt, o.typeDur:
  // typed letter by letter; before typeAt nothing). Keys in time: o.curl [[t, v]] (0..1: the top curls back), o.tremble [[t, a]] (0..1: she
  // shivers), o.ear0 (0.9: how far the dog-ear is folded down, 0 standing up) and o.earKeys [[t, v]], o.wiggle [[t, a]] (she wriggles side to
  // side, a ballot leaving fingers). o.folded: a letter folded in three (a slab w x h/3 with two creases); o.bright: unlit (always readable)
  feuilleSheet(o) {
    const w = o.w ?? 0.42, h = o.h ?? 0.56, g = grp(), body = grp(); g.add(body);
    if (o.folded) {
      const fh = h / 3, s = grp(at(box(w, fh, 0.012, PAPER, { outline: 0.004 }), 0, 0, 0), at(box(w * 0.98, 0.004, 0.014, '#D8D3C6'), 0, fh * 0.18, 0.001), at(box(w * 0.98, 0.004, 0.014, '#D8D3C6'), 0, -fh * 0.18, 0.001));
      s.add(at(box(0.03, 0.02, 0.014, SMEAR), -w / 2 + 0.03, -fh * 0.3, 0.002)); body.add(s); return g;
    }
    const geo = new THREE.PlaneGeometry(w, h, 8, 10), pa = geo.attributes.position, base = pa.array.slice();
    const F = sheetCanvas(w, h, o, false), B = sheetCanvas(w, h, o, true);
    const M = (tex, side) => o.bright ? new THREE.MeshBasicMaterial({ map: tex, side, transparent: true, alphaTest: 0.5 }) : new THREE.MeshLambertMaterial({ map: tex, side, transparent: true, alphaTest: 0.5 });
    const front = new THREE.Mesh(geo, M(F.tex, THREE.FrontSide)), backM = new THREE.Mesh(geo, M(B.tex, THREE.BackSide)); front.castShadow = backM.castShadow = true; front.receiveShadow = backM.receiveShadow = true;
    body.add(front, backM);
    const E = w * (o.ear ?? 0.22), triG = new THREE.BufferGeometry();
    triG.setAttribute('position', new THREE.Float32BufferAttribute([E / 2, E / 2, 0, -E / 2, E / 2, 0, E / 2, -E / 2, 0], 3)); triG.setIndex([0, 1, 2]); triG.computeVertexNormals();
    const ear = new THREE.Mesh(triG, new THREE.MeshLambertMaterial({ color: '#E2DDCF', side: THREE.DoubleSide })); ear.castShadow = true;
    const hinge = grp(ear); hinge.position.set(w / 2 - E / 2, h / 2 - E / 2, 0.002);
    const axis = new THREE.Vector3(1, -1, 0).normalize(); body.add(hinge);
    if (o.ear === 0) hinge.visible = false;
    const nT = (o.text || '').length;
    g.userData.update = t => {
      const cu = keyAt(o.curl, t, 0, 0.18), tr = keyAt(o.tremble, t, 0, 0.12), wg = keyAt(o.wiggle, t, 0, 0.1);
      for (let i = 0; i < pa.count; i++) {
        const x = base[3 * i], y = base[3 * i + 1], v = (y + h / 2) / h, u = (x + w / 2) / w;
        const z = -cu * h * 0.55 * v * v + tr * 0.012 * Math.sin(t * 47 + v * 9 + u * 3) + wg * 0.05 * Math.sin(t * 22 + v * 6) * v;
        pa.setXYZ(i, x + wg * 0.02 * Math.sin(t * 22 + v * 4) * v, y * (1 - 0.25 * cu * v), z);
      }
      pa.needsUpdate = true; geo.computeVertexNormals();
      body.rotation.z = tr * 0.04 * Math.sin(t * 39) + wg * 0.25 * Math.sin(t * 17);
      const ef = keyAt(o.earKeys, t, o.ear0 ?? 0.9, 0.08); hinge.quaternion.setFromAxisAngle(axis, PI * ef * 0.97);
      hinge.position.z = 0.002 - cu * h * 0.55;
      let n = nT; if (o.typeAt != null) n = Math.max(0, Math.min(nT, Math.floor((t - o.typeAt) / ((o.typeDur ?? 0.8) / Math.max(1, nT)))));
      F.set(n); B.set(0);
    };
    g.userData.update(0); return g;
  },

  // An open ream lying on its back (pivot under its middle, long side along X): a stack of o.n (60) identical white sheets 0.42 x 0.56 (the hero's
  // sheet size), every edge drawn as a pale line, with its green paper wrapper torn open under it
  sheetStack(o) {
    const w = o.w ?? 0.44, d = o.d ?? 0.58, H = o.h ?? 0.14, g = grp();
    g.add(at(box(w + 0.04, 0.02, d + 0.04, o.wrap || '#2F7F5C', { pivot: 'bottom', outline: 0.004 }), 0, 0, 0), at(box(0.05, 0.08, d + 0.04, o.wrap || '#2F7F5C', { pivot: 'bottom' }), -w / 2 - 0.02, 0, 0, 0, 0, 0.5));
    if (o.empty) { g.add(at(box(0.05, 0.12, d + 0.04, o.wrap || '#2F7F5C', { pivot: 'bottom', outline: 0.004 }), w / 2 + 0.02, 0, 0, 0, 0, -0.35), at(box(w + 0.04, 0.1, 0.04, o.wrap || '#2F7F5C', { pivot: 'bottom', outline: 0.004 }), 0, 0, d / 2 + 0.02, 0.4, 0, 0), at(box(0.3, 0.004, 0.08, '#F4F1E8'), 0, 0.022, 0)); return g; }
    const cv = canvasPlane(d, H, (c, W, Hh) => { c.fillStyle = '#F4F2EA'; c.fillRect(0, 0, W, Hh); c.fillStyle = 'rgba(120,120,110,0.35)'; for (let y = 0; y < Hh; y += 3) c.fillRect(0, y, W, 1); }, { res: 256 });
    g.add(at(box(w, H, d, PAPER, { pivot: 'bottom' }), 0, 0.02, 0));
    for (const [x, ry] of [[w / 2 + 0.002, PI / 2], [-w / 2 - 0.002, -PI / 2]]) { const p = cv.clone(); g.add(at(p, x, 0.02 + H / 2, 0, 0, ry, 0)); }
    const p2 = canvasPlane(w, H, (c, W, Hh) => { c.fillStyle = '#F4F2EA'; c.fillRect(0, 0, W, Hh); c.fillStyle = 'rgba(120,120,110,0.35)'; for (let y = 0; y < Hh; y += 3) c.fillRect(0, y, W, 1); }, { res: 256 });
    g.add(at(p2, 0, 0.02 + H / 2, d / 2 + 0.002), at(p2.clone(), 0, 0.02 + H / 2, -d / 2 - 0.002, 0, PI, 0));
    const r = rng(o.seed || 5); for (let i = 0; i < 5; i++) g.add(at(box(w, 0.003, d, PAPER), (r() - 0.5) * 0.02, 0.02 + H + i * 0.004, (r() - 0.5) * 0.02, 0, (r() - 0.5) * 0.05, 0));
    g.userData.top = 0.02 + H + 0.02; return g;
  },

  // The shop's demo shredder (pivot at its foot, front +Z, 0.62 wide, 1.0 high): a grey basket bin under a dark cutting head with a slot on top,
  // a small green lamp, no word or brand; o.tag (true): a white price tag on a string from its corner (o.price '49 €'); o.flatAt (s): it is
  // squashed flat in 0.08 s with a bounce and stays flat, a puff of confetti bursting out; o.flat: already flat; o.plinth: on a low white plinth;
  // o.s (1)
  demoShredder(o) {
    const s = o.s ?? 1, g = grp(), sh = grp(); g.add(sh);
    const bin = box(0.6 * s, 0.7 * s, 0.42 * s, '#9AA1A8', { pivot: 'bottom', outline: 0.008, taper: { x: 1.06, z: 1.06 } });
    const head = grp(at(box(0.64 * s, 0.22 * s, 0.46 * s, '#2E3238', { pivot: 'bottom', outline: 0.008 }), 0, 0, 0), at(box(0.46 * s, 0.02 * s, 0.04 * s, '#0E0F12'), 0, 0.222 * s, 0),
      at(sphere(0.022 * s, '#3CD070', 0, { emissive: '#1E8A40', noGrain: true }), 0.24 * s, 0.13 * s, 0.232 * s), at(box(0.12 * s, 0.05 * s, 0.01 * s, '#4A4F57'), -0.18 * s, 0.12 * s, 0.232 * s));
    head.position.y = 0.7 * s; sh.add(bin, head, at(box(0.3 * s, 0.03 * s, 0.01 * s, '#7A8189'), 0, 0.45 * s, 0.215 * s));
    if (o.plinth) { const ph = o.ph ?? 0.3; g.add(at(box(0.8 * s, ph, 0.6 * s, '#F2F0EA', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0)); sh.position.y = ph; }
    let tag = null;
    if (o.tag !== false) { tag = grp(rod([0, 0, 0], [0.02, -0.22 * s, 0.02], 0.004, INK)); const tg = grp(at(box(0.16 * s, 0.1 * s, 0.006, PAPER, { outline: 0.004 }), 0, 0, 0), at(label(o.price || '49 €', 0.14 * s, 0.07 * s, { bg: null, fg: '#C8202A' }), 0, 0, 0.004)); tg.position.set(0.02, -0.27 * s, 0.02); tag.add(tg); tag.position.set(0.3 * s, 0.86 * s, 0.22 * s); sh.add(tag); }
    const puff = o.flatAt != null ? buildProp('confettiPuff', { at: o.flatAt, n: o.puffN ?? 18, seed: o.seed || 3, r: 0.6 * s }) : null; if (puff) { puff.position.y = 0.2; g.add(puff); }
    g.userData.update = t => {
      let f = o.flat ? 1 : 0; if (o.flatAt != null) f = easeIn((t - o.flatAt) / 0.08);
      const b = o.flatAt != null && t > o.flatAt + 0.08 ? 0.08 * Math.exp(-(t - o.flatAt - 0.08) * 9) * Math.abs(Math.sin((t - o.flatAt) * 30)) : 0;
      sh.scale.set(1 + 0.45 * f, Math.max(0.06, 1 - 0.94 * f + b), 1 + 0.35 * f);
      if (tag) tag.visible = f < 0.5 || o.keepTag; puff?.userData.update(t);
    };
    g.userData.update(0); return g;
  },

  // A puff of confetti (pivot at its centre): o.n (18) little coloured squares burst out at o.at, fly up and out o.r (0.6 m) and flutter down
  // over 0.9 s; hidden before and after
  confettiPuff(o) {
    const g = grp(), n = o.n ?? 18, R = o.r ?? 0.6, cols = ['#E8504A', '#F2C94C', '#5E8FD0', '#7FB069', '#D98AA8', '#F4F1E8'], bits = [];
    for (let i = 0; i < n; i++) { const m = new THREE.Mesh(new THREE.PlaneGeometry(0.06, 0.06), new THREE.MeshBasicMaterial({ color: cols[i % cols.length], side: THREE.DoubleSide })); m.castShadow = false; g.add(m); const a = hsh(i + (o.seed || 0) * 13) * TAU, e = 0.4 + hsh(i * 3 + 1) * 0.9; bits.push({ m, vx: Math.cos(a) * R * (0.6 + hsh(i * 7) * 0.8), vz: Math.sin(a) * R * (0.6 + hsh(i * 5) * 0.8), vy: e * 2.4, sp: 5 + hsh(i) * 9 }); }
    g.userData.update = t => { const u = t - (o.at ?? 0), on = u >= 0 && u < 0.95; for (const b of bits) { b.m.visible = on; if (!on) continue; const k = Math.min(u, 0.95); b.m.position.set(b.vx * (1 - Math.exp(-k * 4)) / 1.1, b.vy * k - 2.4 * k * k, b.vz * (1 - Math.exp(-k * 4)) / 1.1); b.m.rotation.set(t * b.sp, t * b.sp * 0.7, 0); } };
    g.userData.update(-1); return g;
  },

  // The shop's back wall of boxed shredders (pivot at the floor under its middle, front +Z): a white shelving unit o.w (4.4) x 2.6 with four
  // shelves, each holding identical cardboard boxes printed with a grey shredder drawing (no word, no brand); o.empty: the shelves are bare
  shredderWall(o) {
    const W = o.w ?? 4.4, g = grp(), rows = 4, H = 2.6;
    g.add(at(box(W, H, 0.06, '#E8E4DA', { pivot: 'bottom' }), 0, 0, -0.32), at(box(0.06, H, 0.6, '#F2F0EA', { pivot: 'bottom', outline: 0.004 }), -W / 2, 0, 0), at(box(0.06, H, 0.6, '#F2F0EA', { pivot: 'bottom', outline: 0.004 }), W / 2, 0, 0));
    const pic = canvasPlane(0.42, 0.34, (c, Wc, Hc) => { c.fillStyle = '#C9A06A'; c.fillRect(0, 0, Wc, Hc); c.fillStyle = '#F4F1E8'; c.fillRect(Wc * 0.2, Hc * 0.14, Wc * 0.6, Hc * 0.72); c.fillStyle = '#6E757D'; c.fillRect(Wc * 0.33, Hc * 0.42, Wc * 0.34, Hc * 0.38); c.fillStyle = '#2E3238'; c.fillRect(Wc * 0.3, Hc * 0.3, Wc * 0.4, Hc * 0.13); }, { res: 128 });
    for (let r_ = 0; r_ < rows; r_++) {
      const y = 0.12 + r_ * (H - 0.2) / rows; g.add(at(box(W, 0.04, 0.6, '#F2F0EA', { outline: 0.004 }), 0, y, 0));
      if (o.empty) continue;
      for (let x = -W / 2 + 0.3; x < W / 2 - 0.2; x += 0.5) { g.add(at(box(0.44, 0.36, 0.44, '#C9A06A', { pivot: 'bottom', outline: 0.004 }), x, y + 0.02, 0.02)); const p = pic.clone(); g.add(at(p, x, y + 0.2, 0.245)); }
    }
    g.add(at(box(W, 0.04, 0.6, '#F2F0EA'), 0, H - 0.02, 0)); return g;
  },

  // The sales counter (pivot at the floor under its middle, the customer's side +Z): a pale wooden counter o.w (2.2) x 1.0 high x 0.7 deep with a
  // darker top, a small card reader and a pen on a chain
  salesCounter(o) {
    const W = o.w ?? 2.2, g = grp(at(box(W, 0.96, 0.7, o.color || '#C9A27A', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(W + 0.08, 0.05, 0.78, o.top || '#7A5A3C', { pivot: 'bottom' }), 0, 0.96, 0), at(box(W - 0.2, 0.08, 0.02, '#A8825C'), 0, 0.5, 0.351));
    g.add(at(box(0.12, 0.05, 0.18, '#2A2D33', { outline: 0.004 }), W / 2 - 0.25, 1.035, -0.05), at(box(0.09, 0.005, 0.07, '#7FB3C8', { emissive: '#2A4A58', noGrain: true }), W / 2 - 0.25, 1.062, -0.07));
    g.userData.top = 1.01; return g;
  },

  // A police van (pivot at the floor under its middle, its nose +X, 5.4 x 2.2 x 2.6 m): white with a navy band and POLICE on both sides, a light
  // bar, rear doors swung open and a steel ramp from its open back down to the ground at o.rampLen (2.6) metres behind
  paddyWagon(o) {
    const g = grp(), L = 5.4, Wd = 2.2, rl = o.rampLen ?? 2.6;
    g.add(at(box(L - 1.3, 2.3, Wd, '#F4F4F0', { pivot: 'bottom', outline: 0.012 }), -0.65, 0.35, 0), at(box(1.3, 1.6, Wd - 0.06, '#F4F4F0', { pivot: 'bottom', outline: 0.012, taper: { x: 0.8, z: 1 } }), L / 2 - 0.65, 0.35, 0));
    g.add(at(box(1.0, 0.7, Wd - 0.04, '#9FC6D4', { noGrain: true }), L / 2 - 0.5, 1.6, 0), at(box(L + 0.02, 0.3, Wd + 0.02, '#1E3A6E'), 0, 0.8, 0), at(box(0.5, 0.14, 1.2, INK), L / 2 - 1.3, 2.72, 0), at(box(0.3, 0.14, 0.45, '#2A4C8A', { emissive: '#1A3A7A', noGrain: true }), L / 2 - 1.3, 2.84, 0.3), at(box(0.3, 0.14, 0.45, '#B5302A', { emissive: '#6A1A14', noGrain: true }), L / 2 - 1.3, 2.84, -0.3));
    for (const s of [-1, 1]) { g.add(at(label('POLICE', 2.2, 0.42, { bg: null, fg: '#1E3A6E' }), -0.8, 1.55, s * (Wd / 2 + 0.01), 0, s > 0 ? 0 : PI, 0)); for (const x of [-1.7, 1.6]) g.add(at(cyl(0.42, 0.42, 0.3, INK, 12), x, 0.42, s * 0.92, PI / 2), at(cyl(0.18, 0.18, 0.02, '#9AA0A8', 8), x, 0.42, s * 1.08, PI / 2)); }
    const bx = -L / 2 - 0.02; g.add(at(box(0.03, 2.1, Wd - 0.24, '#202328'), bx - 0.005, 1.45, 0), at(box(0.03, 0.06, Wd - 0.24, '#5A5F66'), bx - 0.01, 0.42, 0), at(label('POLICE', 1.2, 0.26, { bg: '#F4F4F0', fg: '#1E3A6E' }), bx - 0.03, 2.75, 0, 0, -PI / 2, 0), at(box(0.04, 0.3, 1.3, '#F4F4F0'), bx - 0.01, 2.75, 0));
    for (const s of [-1, 1]) { const d = grp(at(box(0.05, 2.2, Wd / 2 - 0.05, '#ECECE8', { outline: 0.008 }), 0, 0, -s * (Wd / 4 - 0.02))); d.position.set(bx, 1.45, s * (Wd / 2)); d.rotation.y = s * 1.9; g.add(d); }
    const ang = Math.atan2(0.42, rl), Lr = Math.hypot(rl, 0.42), rp = grp(at(box(Lr, 0.05, 1.3, '#8C939B', { outline: 0.006 }), -Lr / 2, 0, 0)); for (let i = 1; i < 8; i++) rp.add(at(box(0.04, 0.02, 1.3, '#6A7078'), -i * Lr / 8, 0.03, 0)); rp.rotation.z = ang; rp.position.set(bx, 0.42, 0); g.add(rp);
    g.userData.ramp = { top: [bx, 0.45, 0], foot: [bx - rl, 0.02, 0] }; return g;
  },

  // A procession of paper suspects (world space; pivot ignored): items walk in single file along o.path [[x, y, z], ...] (polyline) at o.speed
  // (1.1 m/s) from o.at, one every o.gap (0.9 m), bobbing like little marchers, each holding a tiny numbered mugshot board; o.kinds (list): 'ream',
  // 'news', 'book', 'map', 'poster', 'notes' (a banknote stack), cycled; o.lead (m, 0): the line starts that far along already; o.s (1); items hide
  // past the path's end (inside the van)
  paperParade(o) {
    const g = grp(), path = (o.path || [[0, 0, 0], [5, 0, 0]]).map(p => new THREE.Vector3(...p)), segs = []; let L = 0;
    for (let i = 1; i < path.length; i++) { const l = path[i].distanceTo(path[i - 1]); segs.push({ a: path[i - 1], b: path[i], l, L0: L }); L += l; }
    const kinds = o.kinds || ['ream', 'news', 'book', 'map', 'poster'], n = o.n ?? 8, s = o.s ?? 1, items = [];
    const mk = k => { const it = grp();
      if (k === 'ream') it.add(at(box(0.44, 0.16, 0.3, '#2F7F5C', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(0.445, 0.16, 0.1, PAPER, { pivot: 'bottom' }), 0, 0, 0));
      else if (k === 'news') it.add(at(box(0.5, 0.36, 0.04, '#E9E5D8', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(0.42, 0.05, 0.005, INK), 0, 0.3, 0.023), at(box(0.18, 0.12, 0.005, '#8C949A'), -0.1, 0.16, 0.023));
      else if (k === 'book') it.add(at(box(0.3, 0.42, 0.1, '#7A2E4E', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(0.28, 0.4, 0.09, PAPER), 0.012, 0.01, 0));
      else if (k === 'map') it.add(at(cyl(0.07, 0.07, 0.6, '#E8D9A8', 10, { outline: 0.006 }), 0, 0.3, 0), at(cyl(0.072, 0.072, 0.06, '#B5302A', 10), 0, 0.42, 0));
      else if (k === 'poster') it.add(at(box(0.36, 0.5, 0.01, PAPER, { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(0.3, 0.08, 0.006, '#C8202A'), 0, 0.42, 0.007), at(box(0.24, 0.26, 0.006, '#FFFFFF', { outline: 0.004 }), 0, 0.18, 0.008));
      else if (k === 'notes') { for (let j = 0; j < 4; j++) it.add(at(box(0.4, 0.06, 0.2, j % 2 ? '#8FB58A' : '#A8C79C', { pivot: 'bottom', outline: 0.004 }), (hsh(j) - 0.5) * 0.02, j * 0.06, 0)); it.add(at(box(0.41, 0.25, 0.03, '#E2D9A8'), 0, 0.12, 0)); }
      const pl = buildProp('placard', { text: o.board ?? `${String(100 + items.length * 7)}` }); pl.scale.setScalar(0.45); pl.position.set(0, 0.25, 0.18); it.add(pl);
      it.scale.setScalar(s); return it; };
    for (let i = 0; i < n; i++) { const it = mk(kinds[i % kinds.length]); g.add(it); items.push(it); }
    const P0 = new THREE.Vector3();
    const posAt = d => { if (d <= 0) return [path[0].clone(), segs[0]]; for (const sg of segs) if (d <= sg.L0 + sg.l) return [sg.a.clone().lerp(sg.b, (d - sg.L0) / sg.l), sg]; return [path[path.length - 1].clone(), segs[segs.length - 1]]; };
    g.userData.update = t => { const u = Math.max(0, t - (o.at ?? 0)), head = (o.lead ?? 0) + u * (o.speed ?? 1.1);
      items.forEach((it, i) => { const d = head - i * (o.gap ?? 0.9); it.visible = d > -0.01 && d < L - 0.05 && !(o.hideBefore != null && d < o.hideBefore); if (!it.visible) return;
        const [p, sg] = posAt(d); P0.copy(p); P0.y += Math.abs(Math.sin(d * 5.5)) * 0.08 * s; it.position.copy(P0);
        const dir = sg.b.clone().sub(sg.a); it.rotation.set(0, Math.atan2(dir.x, dir.z) + (o.yaw ?? 0), Math.sin(d * 5.5) * 0.12); }); };
    g.userData.update(0); return g;
  },

  // A wanted poster (pivot at its centre, front +Z): white paper 0.62 x 0.86 with RECHERCHÉE in red at the top and, below it, nothing but a blank
  // white rectangle framed in grey (her portrait); o.at: slapped on with a pop and a swing; o.peelAt: peeled off (hidden)
  wantedPoster(o) {
    const w = o.w ?? 0.62, h = o.h ?? 0.86, g = grp();
    const pl = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#F4F1E6'; c.fillRect(0, 0, W, H); c.fillStyle = '#B5201A'; c.textAlign = 'center'; c.textBaseline = 'middle'; let fs = Math.round(H * 0.12); c.font = `900 ${fs}px Arial`; while (c.measureText('RECHERCHÉE').width > W * 0.9) { fs -= 2; c.font = `900 ${fs}px Arial`; } c.fillText('RECHERCHÉE', W / 2, H * 0.12);
      c.strokeStyle = '#8C949A'; c.lineWidth = W * 0.02; c.fillStyle = '#FFFFFF'; c.fillRect(W * 0.2, H * 0.27, W * 0.6, H * 0.58); c.strokeRect(W * 0.2, H * 0.27, W * 0.6, H * 0.58); c.fillStyle = '#2A2A2E'; c.fillRect(W * 0.3, H * 0.9, W * 0.4, H * 0.02); }, { res: 384 });
    const inner = grp(pl, at(box(w, h, 0.004, '#DCD8CC'), 0, 0, -0.004)); g.add(inner);
    g.userData.update = t => { const u = t - (o.at ?? -1); inner.visible = u >= 0 && !(o.peelAt != null && t >= o.peelAt); if (!inner.visible) return; inner.scale.setScalar(u < 0.08 ? 1.25 - 0.25 * (u / 0.08) : 1); inner.rotation.z = 0.12 * Math.exp(-u * 6) * Math.sin(u * 22); };
    g.userData.update(0); return g;
  },

  // An observation window (pivot at the floor under its middle, in the XY plane): a pane of tinted glass o.w (2.4) x o.h (1.3) from 0.9 m up, a
  // dark frame and a sill
  glassPane(o) {
    const W = o.w ?? 2.4, H = o.h ?? 1.3, y0 = o.y ?? 0.9, g = grp();
    g.add(at(new THREE.Mesh(new THREE.PlaneGeometry(W, H), glassMat(o.opacity ?? 0.12, '#CFE4EA')), 0, y0 + H / 2, 0));
    for (const [x, y, w, h] of [[0, y0, W + 0.12, 0.08], [0, y0 + H, W + 0.12, 0.08], [-W / 2, y0 + H / 2, 0.08, H], [W / 2, y0 + H / 2, 0.08, H]]) g.add(at(box(w, h, 0.1, '#2A2E34', { outline: 0.004 }), x, y, 0));
    g.add(at(box(W + 0.3, 0.06, 0.36, '#3A3F45'), 0, y0 - 0.04, 0.12)); return g;
  },

  // A courthouse (or bank) front (pivot at the foot of its steps in the middle, front +Z): o.steps (6) stone steps 0.2 high and 0.4 deep, o.w
  // (12) wide, a portico of o.cols (6) columns, a pediment with o.title (TRIBUNAL) and tall dark double doors (open if o.open)
  courtFront(o) {
    const W = o.w ?? 12, n = o.steps ?? 6, g = grp(), st = '#D9D2C2', H = o.H ?? 6.2, top = n * 0.2, dz = -n * 0.4;
    for (let i = 0; i < n; i++) { const d = (n - i) * 0.4; g.add(at(box(W - i * 0.1, 0.2, d, i % 2 ? '#D2CBBA' : st, { pivot: 'bottom', outline: 0.004 }), 0, i * 0.2, -i * 0.4 - d / 2)); }
    g.add(at(box(W, 0.25, 3.0, st, { pivot: 'bottom' }), 0, top, dz - 1.5));
    const nc = o.cols ?? 6; for (let i = 0; i < nc; i++) { const x = -W / 2 + 0.9 + i * (W - 1.8) / (nc - 1); g.add(at(cyl(0.34, 0.38, H, '#E6E0D2', 10, { pivot: 'bottom', outline: 0.006 }), x, top + 0.25, dz - 0.6), at(box(0.9, 0.2, 0.9, '#D2CBBA', { pivot: 'bottom' }), x, top + 0.25, dz - 0.6), at(box(0.95, 0.24, 0.95, '#D2CBBA'), x, top + 0.25 + H, dz - 0.6)); }
    g.add(at(box(W + 0.4, 0.7, 1.6, '#E2DBCB', { outline: 0.006 }), 0, top + 0.6 + H, dz - 0.9));
    const ped = new THREE.Shape(); ped.moveTo(-W / 2 - 0.2, 0); ped.lineTo(W / 2 + 0.2, 0); ped.lineTo(0, 1.6); ped.closePath();
    const pm = new THREE.Mesh(new THREE.ExtrudeGeometry(ped, { depth: 1.2, bevelEnabled: false }), mat('#E6E0D2')); pm.castShadow = true; addOutline(pm, 0.01); g.add(at(pm, 0, top + 0.95 + H, dz - 1.6));
    g.add(at(label(o.title ?? 'TRIBUNAL', Math.min(5, W * 0.42), 0.55, { bg: '#E2DBCB', fg: '#5A5446', wrap: false }), 0, top + 0.6 + H, dz - 0.09));
    g.add(at(box(W - 0.6, H + 0.2, 0.3, '#CFC7B6', { pivot: 'bottom' }), 0, top + 0.25, dz - 3.0));
    const dw = 2.4, dh = o.doorH ?? 3.8;
    if (o.doorSign) g.add(at(box(2.6, 0.62, 0.08, '#1E3A6E', { outline: 0.006 }), 0, top + 0.25 + dh + 0.42, dz - 2.7), at(label(o.doorSign, 2.4, 0.5, { bg: '#1E3A6E', fg: '#F2C94C', wrap: false }), 0, top + 0.25 + dh + 0.42, dz - 2.65));
    if (o.open) g.add(at(box(dw, dh, 0.05, '#1A1C20', { pivot: 'bottom' }), 0, top + 0.25, dz - 2.84), at(box(dw / 2, dh, 0.08, '#5A3A26', { pivot: 'bottom', outline: 0.006 }), -dw * 0.9, top + 0.25, dz - 2.5, 0, 0.9, 0), at(box(dw / 2, dh, 0.08, '#5A3A26', { pivot: 'bottom', outline: 0.006 }), dw * 0.9, top + 0.25, dz - 2.5, 0, -0.9, 0));
    else g.add(at(box(dw, dh, 0.1, '#5A3A26', { pivot: 'bottom', outline: 0.006 }), 0, top + 0.25, dz - 2.82), at(box(0.04, dh, 0.12, '#3A2618'), 0, top + 0.25 + dh / 2, dz - 2.78));
    g.userData.top = top; g.userData.landing = [0, top + 0.25, dz - 0.4]; return g;
  },

  // A cluster of press microphones on a low stand (pivot at the floor, facing +Z): o.n (5) mics with coloured windscreens fanned round 1.45 m
  micCluster(o) {
    const g = grp(), n = o.n ?? 5, cols = ['#C8202A', '#2E6FB5', '#F2C94C', '#2E7D4F', '#F4F1E8', '#7A2E4E'];
    g.add(at(cyl(0.04, 0.06, o.h ?? 1.25, '#2A2D33', 6, { pivot: 'bottom' }), 0, 0, 0), at(cyl(0.22, 0.25, 0.04, '#2A2D33', 10), 0, 0.02, 0));
    for (let i = 0; i < n; i++) { const a = (i - (n - 1) / 2) * 0.28, y = (o.h ?? 1.25) + 0.05 + (i % 2) * 0.06; g.add(rod([0, (o.h ?? 1.25) - 0.05, 0], [Math.sin(a) * 0.18, y, 0.12], 0.012, '#2A2D33'), at(cyl(0.045, 0.045, 0.12, cols[i % cols.length], 8, { outline: 0.006 }), Math.sin(a) * 0.2, y + 0.02, 0.16, PI / 2 - 0.3, 0, 0)); }
    return g;
  },

  // The prosecutor's shredder on a trolley (pivot at the floor under its middle, front +Z): a steel trolley 0.9 x 0.8 high on four castors, the
  // price-tagged demo shredder on top and a deep red velvet cover over it with a gold fringe. o.offAt: the cover is whipped off (it flies up and
  // aside in 0.25 s and vanishes); o.onAt: thrown back on (it drops onto it in 0.2 s); o.covered (true): covered at t 0
  shredderTrolley(o) {
    const g = grp();
    g.add(at(box(0.9, 0.04, 0.6, '#B8BEC6', { outline: 0.006 }), 0, 0.8, 0), at(box(0.86, 0.03, 0.56, '#9AA1A8'), 0, 0.25, 0));
    for (const [x, z] of [[-0.42, -0.27], [0.42, -0.27], [-0.42, 0.27], [0.42, 0.27]]) g.add(at(box(0.03, 0.78, 0.03, '#9AA1A8', { pivot: 'bottom' }), x, 0.04, z), at(sphere(0.04, INK, 0), x, 0.04, z));
    const sh = buildProp('demoShredder', { s: 0.8, price: o.price }); sh.position.y = 0.82; g.add(sh);
    const cov = grp(at(box(0.7, 0.98, 0.56, '#7A1420', { pivot: 'bottom', outline: 0.006, taper: { x: 0.86, z: 0.86 } }), 0, 0, 0), at(box(0.74, 0.06, 0.6, '#D4A93C'), 0, 0.03, 0));
    cov.position.y = 0.82; g.add(cov);
    g.userData.update = t => {
      let up = o.covered === false ? 1 : 0;
      if (o.offAt != null && t >= o.offAt) up = smooth((t - o.offAt) / 0.25);
      if (o.onAt != null && t >= o.onAt) up = 1 - smooth((t - o.onAt) / 0.2);
      cov.visible = up < 0.98; cov.position.set(0.9 * up, 0.82 + 1.6 * up - 1.2 * up * up, 0.2 * up); cov.rotation.set(0.4 * up, 0, -1.4 * up); cov.scale.setScalar(1 - 0.3 * up);
      sh.userData.update?.(t);
    };
    g.userData.update(0); return g;
  },

  // The referendum poster on an easel (pivot at the easel's foot, front +Z): a white board 1.3 x 1.6 with the price-tagged shredder drawn big and,
  // under it, two square boxes with OUI and NON
  refPoster(o) {
    const g = grp(), W = 1.3, H = 1.6;
    g.add(rod([-0.5, 0, 0.25], [-0.35, 2.4, 0], 0.025, '#7A5A3C'), rod([0.5, 0, 0.25], [0.35, 2.4, 0], 0.025, '#7A5A3C'), rod([0, 0, -0.45], [0, 2.3, -0.02], 0.025, '#7A5A3C'), at(box(1.2, 0.05, 0.12, '#7A5A3C'), 0, 0.82, 0.1));
    const pl = canvasPlane(W, H, (c, Wc, Hc) => { c.fillStyle = '#FBFAF6'; c.fillRect(0, 0, Wc, Hc);
      c.fillStyle = '#9AA1A8'; c.fillRect(Wc * 0.3, Hc * 0.24, Wc * 0.4, Hc * 0.32); c.fillStyle = '#2E3238'; c.fillRect(Wc * 0.27, Hc * 0.12, Wc * 0.46, Hc * 0.12); c.fillStyle = '#0E0F12'; c.fillRect(Wc * 0.34, Hc * 0.11, Wc * 0.32, Hc * 0.014);
      c.strokeStyle = INK; c.lineWidth = 3; c.beginPath(); c.moveTo(Wc * 0.72, Hc * 0.2); c.lineTo(Wc * 0.8, Hc * 0.3); c.stroke(); c.fillStyle = '#FFFFFF'; c.fillRect(Wc * 0.76, Hc * 0.29, Wc * 0.14, Hc * 0.07); c.strokeRect(Wc * 0.76, Hc * 0.29, Wc * 0.14, Hc * 0.07); c.fillStyle = '#C8202A'; c.font = `bold ${Math.round(Hc * 0.04)}px Arial`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('49 €', Wc * 0.83, Hc * 0.326);
      c.lineWidth = 6; c.strokeStyle = INK; c.fillStyle = INK; c.font = `900 ${Math.round(Hc * 0.08)}px Arial`; c.textAlign = 'left';
      for (const [x, txt] of [[0.12, 'OUI'], [0.56, 'NON']]) { c.strokeRect(Wc * x, Hc * 0.7, Wc * 0.12, Wc * 0.12); c.fillText(txt, Wc * (x + 0.15), Hc * 0.7 + Wc * 0.06); } }, { res: 512 });
    g.add(at(box(W + 0.06, H + 0.06, 0.04, '#E2DBCB', { outline: 0.006 }), 0, 0.85 + H / 2, 0.08), at(pl, 0, 0.85 + H / 2, 0.105)); return g;
  },

  // A pointing stick (pivot at the grip, along +Y up to o.len (1.0)): thin wood with a black tip
  pointerStick(o) { const L = o.len ?? 1.0; return grp(rod([0, 0, 0], [0, L, 0], 0.012, '#B98A5A'), rod([0, L - 0.08, 0], [0, L, 0], 0.013, INK)); },

  // A sea of ballots (pivot at the floor under its middle): a white bumpy layer o.w (12) x o.d (10) whose top is at o.h (0.9) and, on top, o.n
  // (900) loose ballots lying every which way (instanced)
  ballotSea(o) {
    const W = o.w ?? 12, D = o.d ?? 10, Hh = o.h ?? 0.9, g = grp(), r = rng(o.seed || 8);
    g.add(at(box(W, Hh, D, '#F2F0EA', { pivot: 'bottom' }), 0, 0, 0));
    const L = []; for (let i = 0; i < (o.n ?? 900); i++) L.push([(r() - 0.5) * W, Hh + r() * 0.06, (r() - 0.5) * D, (r() - 0.5) * 0.5, r() * TAU, (r() - 0.5) * 0.5, 1, 1, 1]);
    const m = inst(new THREE.BoxGeometry(0.22, 0.008, 0.3), mat('#FBFAF6'), L); g.add(m);
    const L2 = []; for (let i = 0; i < 160; i++) L2.push([(r() - 0.5) * W, Hh + 0.02 + r() * 0.1, (r() - 0.5) * D, r() * 1.2, r() * TAU, r() * 1.2, 1, 1, 1]);
    g.add(inst(new THREE.BoxGeometry(0.22, 0.008, 0.3), mat('#E6E3DA'), L2)); return g;
  },

  // A snow shovel (pivot at the grip, the shaft along -Y down to the blade at o.len (1.3)): a wooden shaft and a wide red plastic blade
  snowShovel(o) { const L = o.len ?? 1.3, g = grp(rod([0, 0, 0], [0, -L, 0], 0.02, '#B98A5A'), at(box(0.18, 0.04, 0.04, INK), 0, 0, 0)); g.add(at(box(0.55, 0.42, 0.04, '#C8322A', { outline: 0.006 }), 0, -L - 0.18, 0.04, 0.3, 0, 0)); g.userData.grip = [0, 0, 0]; return g; },

  // A hillside of fresh stumps (pivot at the foot of the hill in the middle; the hill climbs toward -Z): a green slope o.w (60) wide rising
  // o.rise (9) m over o.d (40) m, covered with pale stumps in rows to the top, a few cut logs lying about
  stumpField(o) {
    const W = o.w ?? 60, D = o.d ?? 40, R = o.rise ?? 9, g = grp(), r = rng(o.seed || 11);
    const geo = new THREE.PlaneGeometry(W, D, 24, 16), pa = geo.attributes.position;
    for (let i = 0; i < pa.count; i++) { const x = pa.getX(i), y = pa.getY(i), v = (y + D / 2) / D; pa.setZ(i, R * smooth(v) + Math.sin(x * 0.3) * 0.4 * v + (hsh(i) - 0.5) * 0.3); }
    geo.computeVertexNormals(); const hill = new THREE.Mesh(geo, mat('#7FA85A')); hill.rotation.x = -PI / 2; hill.position.z = -D / 2; hill.receiveShadow = true; g.add(hill);
    const hAt = (x, z) => { const v = clamp01(-z / D); return R * smooth(v) + Math.sin(x * 0.3) * 0.4 * v; };
    const S = [], T = []; for (let z = -2; z > -D + 1; z -= 2.2) for (let x = -W / 2 + 2; x < W / 2 - 2; x += 2.0 + r() * 0.6) { const xx = x + (r() - 0.5) * 0.8, zz = z + (r() - 0.5) * 0.8, y = hAt(xx, zz), s = 0.8 + r() * 0.5; S.push([xx, y + 0.25 * s, zz, 0, r() * TAU, 0, s, s, s]); T.push([xx, y + 0.5 * s + 0.005, zz, 0, 0, 0, s, s, s]); }
    g.add(inst(new THREE.CylinderGeometry(0.3, 0.36, 0.5, 8), mat('#8A6A4A'), S), inst(new THREE.CylinderGeometry(0.29, 0.29, 0.01, 8), mat('#E8D2A0'), T));
    const Lg = []; for (let i = 0; i < 14; i++) { const x = (r() - 0.5) * W * 0.8, z = -3 - r() * (D - 6); Lg.push([x, hAt(x, z) + 0.25, z, 0, r() * TAU, PI / 2, 1, 2.4, 1]); } g.add(inst(new THREE.CylinderGeometry(0.25, 0.25, 1, 8), mat('#8A6A4A'), Lg));
    return g;
  },

  // A log truck (pivot at the floor under its middle, its nose +X, 8 m long): a cab, a flatbed with stakes loaded with logs, BULLETINS on a panel
  // on both sides of the load; o.loadAt: the last log rises from the ground beside it (o.side, +1: +Z) onto the top of the load over 0.6 s
  logTruck(o) {
    const g = grp(), L = 8, side = o.side ?? 1;
    g.add(at(box(1.8, 2.2, 2.3, '#2E6FB5', { pivot: 'bottom', outline: 0.01 }), L / 2 - 0.9, 0.5, 0), at(box(1.2, 0.8, 2.2, '#9FC6D4', { noGrain: true }), L / 2 - 0.5, 2.0, 0), at(box(L - 1.8, 0.3, 2.4, '#3A3F45', { pivot: 'bottom', outline: 0.008 }), -0.9, 0.7, 0));
    for (const s of [-1, 1]) { for (const x of [-2.8, -1.4, 2.9]) g.add(at(cyl(0.5, 0.5, 0.36, INK, 12), x, 0.5, s * 1.0, PI / 2)); for (const x of [-4.5, -2.7, -0.9, 0.9]) g.add(at(box(0.1, 1.6, 0.1, '#2A2D33', { pivot: 'bottom' }), x, 1.0, s * 1.15)); }
    const logs = []; for (let row = 0; row < 3; row++) for (let i = 0; i < 4 - row; i++) logs.push([-0.9, 1.3 + row * 0.42, -0.75 + i * 0.5 + row * 0.25]);
    g.add(inst(new THREE.CylinderGeometry(0.22, 0.22, 5.6, 8), mat('#8A6A4A'), logs.map(p => [p[0], p[1], p[2], 0, 0, PI / 2, 1, 1, 1])), inst(new THREE.CylinderGeometry(0.2, 0.2, 5.62, 8), mat('#E8D2A0'), logs.map(p => [p[0], p[1], p[2], 0, 0, PI / 2, 1, 1, 1])));
    for (const s of [-1, 1]) g.add(at(box(3.2, 0.7, 0.05, '#F4F1E8', { outline: 0.006 }), -0.9, 2.6, s * 1.24), at(label('BULLETINS', 3.0, 0.6, { bg: '#F4F1E8', fg: '#1E3A6E', wrap: false }), -0.9, 2.6, s * 1.27, 0, s > 0 ? 0 : PI, 0));
    const last = at(grp(at(cyl(0.22, 0.22, 4.8, '#8A6A4A', 8, { outline: 0.006 }), 0, 0, 0, 0, 0, PI / 2), at(cyl(0.205, 0.205, 4.82, '#E8D2A0', 8), 0, 0, 0, 0, 0, PI / 2)), -0.9, 0.25, side * 2.0); g.add(last);
    g.userData.update = t => { const u = o.loadAt != null ? smooth((t - o.loadAt) / 0.6) : 0; last.position.set(-0.9, 0.25 + (2.55 - 0.25) * u + Math.sin(u * PI) * 0.6, side * (2.0 - 2.0 * u)); };
    g.userData.update(0); return g;
  },

  // A transparent ballot box (pivot at its foot, front +Z): a glass cube 0.6 on a dark base with a steel frame, a slot in the lid and a white plate
  // with o.text (OUI | NON) on the front; o.fill [[t, n]]: n ballots (0..40) lie inside from t (they pile up)
  ballotBox(o) {
    const g = grp(), S = 0.6;
    g.add(at(box(S + 0.06, 0.06, S + 0.06, '#2A2D33', { pivot: 'bottom' }), 0, 0, 0), at(new THREE.Mesh(new THREE.BoxGeometry(S, S, S), glassMat(0.22, '#DDEEF2')), 0, 0.06 + S / 2, 0));
    for (const [x, z] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) g.add(at(box(0.025, S, 0.025, '#9AA1A8'), x * S / 2, 0.06 + S / 2, z * S / 2));
    g.add(at(box(S + 0.04, 0.03, S + 0.04, '#9AA1A8'), 0, 0.06 + S + 0.015, 0), at(box(0.28, 0.035, 0.03, INK), 0, 0.06 + S + 0.02, 0));
    g.add(at(box(0.36, 0.14, 0.01, '#FFFFFF', { outline: 0.004 }), 0, 0.06 + S * 0.72, S / 2 + 0.008), at(label(o.text || 'NON', 0.32, 0.12, { bg: '#FFFFFF', fg: INK, wrap: false }), 0, 0.06 + S * 0.72, S / 2 + 0.015));
    const r = rng(o.seed || 9), L = []; for (let i = 0; i < 40; i++) L.push([(r() - 0.5) * (S - 0.12), 0.07 + i * 0.012, (r() - 0.5) * (S - 0.12), (r() - 0.5) * 0.4, r() * TAU, (r() - 0.5) * 0.4, 1, 1, 1]);
    const pile = []; for (let i = 0; i < 40; i++) { const b = at(box(0.2, 0.006, 0.26, PAPER), ...L[i].slice(0, 6)); b.visible = false; g.add(b); pile.push(b); }
    g.userData.update = t => { const n = Math.round(keyAt(o.fill, t, 0, 0)); pile.forEach((b, i) => { b.visible = i < n; }); };
    g.userData.update(0); return g;
  },

  // Ballots that leave the voters' fingers on their own (world space): o.drops [{from, to, t0, dur, hold}]: a small white ballot hangs at `from`
  // (in the fingers) wriggling for `hold` (0.3) s, then flies in an arc to `to` (over the NON box's slot) and dives in nose first, hidden after
  divingBallots(o) {
    const g = grp(), items = [];
    for (const d of o.drops || []) { const b = grp(at(box(0.18, 0.24, 0.006, PAPER, { outline: 0.003 }), 0, 0, 0), at(box(0.12, 0.012, 0.007, '#8C949A'), 0, 0.06, 0.001)); b.visible = false; g.add(b); items.push({ b, d, A: new THREE.Vector3(...d.from), B: new THREE.Vector3(...d.to) }); }
    g.userData.update = t => { for (const { b, d, A, B } of items) {
      const hold = d.hold ?? 0.3, u = (t - d.t0 - hold) / d.dur, hv = t >= d.t0; b.visible = hv && u < 1; if (!b.visible) continue;
      if (u < 0) { b.position.copy(A); b.rotation.set(0, 0, 0.35 * Math.sin((t - d.t0) * 28)); continue; }
      const k = smooth(u); b.position.copy(A).lerp(B, k); b.position.y += Math.sin(k * PI) * (d.arc ?? 0.5) - (u > 0.85 ? (u - 0.85) * 0.6 : 0);
      b.rotation.set(-PI / 2 * easeIn(u), (d.spin ?? 1) * 2.5 * k, 0.3 * Math.sin(t * 25) * (1 - k)); } };
    g.userData.update(-1); return g;
  },

  // A steamroller (pivot at the floor under its middle, its nose +X, 4.6 m long): a yellow body, a big grey front drum, rear wheels, a seat under a
  // canopy, a big red ribbon bow on its nose
  steamroller(o) {
    const g = grp(), Y = '#E8B83A';
    g.add(at(box(2.4, 1.3, 1.8, Y, { pivot: 'bottom', outline: 0.01 }), -0.7, 0.6, 0), at(cyl(0.75, 0.75, 1.9, '#8C939B', 16, { outline: 0.01 }), 1.5, 0.75, 0, PI / 2), at(box(0.9, 0.3, 2.0, Y, { outline: 0.008 }), 1.5, 1.6, 0));
    for (const s of [-1, 1]) g.add(at(cyl(0.6, 0.6, 0.3, INK, 12), -1.4, 0.6, s * 0.95, PI / 2));
    g.add(at(box(0.6, 0.12, 0.6, '#2A2D33'), -0.7, 1.95, 0), at(box(0.12, 0.6, 0.6, '#2A2D33', { pivot: 'bottom' }), -1.05, 1.95, 0));
    for (const [x, z] of [[-1.5, -0.8], [-1.5, 0.8], [0.1, -0.8], [0.1, 0.8]]) g.add(at(box(0.06, 1.3, 0.06, '#2A2D33', { pivot: 'bottom' }), x, 1.9, z)); g.add(at(box(1.9, 0.08, 1.9, '#C8322A', { outline: 0.006 }), -0.7, 3.2, 0));
    const bow = grp(at(box(0.1, 0.5, 2.0, '#D21E2A', { outline: 0.006 }), 0, 0, 0)); for (const s of [-1, 1]) bow.add(at(box(0.08, 0.5, 0.6, '#D21E2A', { outline: 0.006 }), 0.05, 0.25, s * 0.35, s * 0.6, 0, 0), at(box(0.08, 0.6, 0.18, '#D21E2A'), 0.05, -0.45, s * 0.25, -s * 0.3, 0, 0)); bow.position.set(2.0, 1.6, 0); g.add(bow);
    g.userData.seat = [-0.7, 2.0, 0];
    const drum = g.children[1]; g.userData.update = t => { drum.rotation.set(PI / 2, 0, 0); drum.rotateY(-(o.spin ?? 2.5) * t); };
    return g;
  },

  // Rows of identical price-tagged shredders on a square (pivot at the start of the rows): o.rows [[z, x0, n, gap]] shredders along +X; each is
  // flattened (with its confetti puff) when the roller's front passes it: at t = o.at + (x - o.x0) / o.speed (s; o.x0 the roller's front at o.at)
  shredderRows(o) {
    const g = grp(), sh = [];
    for (const [z, x0, n, gap] of o.rows || []) for (let i = 0; i < n; i++) { const x = x0 + i * (gap ?? 1.4), tt = o.speed ? (o.at ?? 0) + (x - (o.x0 ?? 0)) / o.speed : null;
      const s = buildProp('demoShredder', { s: o.s ?? 0.9, flatAt: (z >= (o.rollZ0 ?? -1e9) && z <= (o.rollZ1 ?? 1e9)) ? tt : null, seed: i + 7, puffN: 12, price: o.price }); s.position.set(x, o.y ?? 0, z); s.rotation.y = o.face ?? 0; g.add(s); sh.push(s); }
    g.userData.update = t => sh.forEach(s => s.userData.update?.(t)); g.userData.update(0); return g;
  },

  // A typewriter on its own (pivot at its foot, the typist's side +Z): a dark green body 0.6 x 0.22 x 0.42, rows of round keys, a roller at the
  // back with paper guides; o.hitFrom..o.hitTo (s): the typebars hammer and the carriage creeps left with a little shake
  typewriter(o) {
    const g = grp(), body = grp(); g.add(body);
    body.add(at(box(0.62, 0.18, 0.44, '#2F4A3A', { pivot: 'bottom', outline: 0.008, taper: { x: 1, z: 0.8 } }), 0, 0, 0), at(box(0.5, 0.03, 0.2, '#22352A'), 0, 0.17, 0.08, -0.25, 0, 0));
    for (let r_ = 0; r_ < 3; r_++) for (let i = 0; i < 9; i++) body.add(at(cyl(0.016, 0.016, 0.02, '#F2F0EA', 8, { outline: 0.003 }), -0.2 + i * 0.05 + r_ * 0.02, 0.19 + r_ * 0.02, 0.17 - r_ * 0.045));
    const car = grp(at(cyl(0.05, 0.05, 0.7, INK, 12, { outline: 0.004 }), 0, 0, 0, 0, 0, PI / 2), at(cyl(0.03, 0.03, 0.78, '#9AA1A8', 8), 0, 0, 0, 0, 0, PI / 2), at(box(0.04, 0.06, 0.06, '#9AA1A8'), -0.39, 0, 0), at(box(0.04, 0.06, 0.06, '#9AA1A8'), 0.39, 0, 0)); car.position.set(0, 0.25, -0.14); body.add(car);
    const bar = grp(at(box(0.012, 0.16, 0.012, '#C9CDD3'), 0, 0.08, 0)); bar.position.set(0, 0.18, -0.02); body.add(bar);
    g.userData.paperAt = [0, 0.3, -0.16];
    g.userData.update = t => { const a = o.hitFrom ?? 1e9, b = o.hitTo ?? -1; const on = t >= a && t <= b; bar.rotation.x = on ? -0.9 * Math.abs(Math.sin((t - a) * 34)) : 0; car.position.x = on ? -0.1 * (t - a) / Math.max(0.01, b - a) : (t > b ? -0.1 : 0); body.position.y = on ? 0.004 * Math.sin(t * 70) : 0; };
    g.userData.update(0); return g;
  },

  // A finger plaster (pivot at its centre, along Y): a beige strip round a finger 0.026 thick, 0.036 long, with a white pad
  fingerBandage(o) { return grp(at(box(0.028, 0.036, 0.034, '#E8C9A0', { outline: 0.002 }), 0, 0, 0), at(box(0.029, 0.016, 0.035, '#FFFFFF'), 0, 0, 0.0005)); },

  // A paper cut (pivot at its centre): a thin red line 0.022 long across the finger's pad
  cutLine(o) { return grp(at(box(0.022, 0.004, 0.032, '#D8242A', { noGrain: true }), 0, 0, 0, 0, 0, 0.3)); },

  // A lanyard with a staff card (pivot at the back of the neck): a blue strap down both sides of the chest to a white card at chest height
  lanyard(o) {
    const g = grp(rod([-0.12, 0, 0.1], [-0.02, -0.42, 0.2], 0.008, '#2E6FB5'), rod([0.12, 0, 0.1], [0.02, -0.42, 0.2], 0.008, '#2E6FB5'));
    g.add(at(box(0.11, 0.15, 0.006, '#FFFFFF', { outline: 0.003 }), 0, -0.5, 0.205), at(box(0.07, 0.05, 0.007, '#9FC6D4'), 0, -0.47, 0.207), at(box(0.08, 0.01, 0.007, INK), 0, -0.54, 0.207)); return g;
  },

  // A bare paper shelf (pivot at the floor under its middle, front +Z): a grey metal shelf unit 1.2 x 1.9 x 0.45 with four empty shelves and a
  // torn green ream wrapper left on one of them
  bareShelf(o) {
    const g = grp(); for (const x of [-0.6, 0.6]) for (const z of [-0.2, 0.2]) g.add(at(box(0.04, 1.9, 0.04, '#7A8189', { pivot: 'bottom' }), x, 0, z));
    for (let i = 0; i < 4; i++) g.add(at(box(1.24, 0.03, 0.44, '#9AA1A8', { outline: 0.004 }), 0, 0.3 + i * 0.5, 0));
    g.add(at(box(0.3, 0.02, 0.22, '#2F7F5C', { outline: 0.003 }), 0.2, 0.83, 0.02, 0, 0.3, 0), at(box(0.05, 0.06, 0.22, '#2F7F5C'), 0.05, 0.84, 0.02, 0, 0.3, 0.5)); return g;
  },

  // The demo shredder's plinth, the shredder gone (pivot at its foot, front +Z): the low white plinth 0.72 x 0.3 x 0.54, its price tag lying on it
  emptyPlinth(o) {
    const ph = o.ph ?? 0.3, g = grp(at(box(0.8, ph, 0.6, '#F2F0EA', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(0.5, 0.004, 0.36, '#E4E0D6'), 0, ph + 0.002, 0));
    const tg = grp(at(box(0.16, 0.006, 0.1, PAPER, { outline: 0.004 }), 0, 0, 0), at(label(o.price || '49 €', 0.14, 0.07, { bg: null, fg: '#C8202A' }), 0, 0.004, 0, -PI / 2, 0, 0)); tg.position.set(0.12, ph + 0.005, 0.1); tg.rotation.y = 0.4; g.add(tg);
    g.add(at(rod([0, 0, 0], [0.18, 0, 0.06], 0.004, INK), 0.0, ph + 0.006, 0.08)); return g;
  },

  // A line-up wall (pivot at the floor under its middle, front +Z): the mugshot height chart o.w (5) wide and five numbered floor marks with
  // number plates 1 to 5 over them, o.gap (0.9) apart
  lineupWall(o) {
    const g = grp(), W = o.w ?? 5, gap = o.gap ?? 0.9; g.add(buildProp('mugshotBoard', { w: W, h: 2.4 }));
    for (let i = 0; i < 5; i++) { const x = (i - 2) * gap; g.add(at(box(0.3, 0.005, 0.3, '#F2C94C', { noGrain: true }), x, 0.004, 0.45), at(box(0.22, 0.2, 0.01, INK), x, 2.55, 0.02), at(label(String(i + 1), 0.18, 0.16, { bg: INK, fg: '#F4F1E8', wrap: false }), x, 2.55, 0.03)); }
    return g;
  },
};
