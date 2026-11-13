// « La bosse » (story 56, cycle 18): a man hit his head; the bump never stopped growing; the doctor measured it: three metres; the land registry
// classed it as a hill; on Sundays there are hikers; in winter a ski resort; yesterday the bump went down; the skiers fell from a height; the resort
// wants him to pay for their passes. Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure
// function of the shot time.
import * as THREE from 'three';
import { mat, box, cyl, sphere, addOutline, rng } from './style.js';
import { grp, at, rod, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const list = v => [].concat(v ?? []);
const sstep = u => { const x = Math.max(0, Math.min(1, u)); return x * x * (3 - 2 * x); };
// a value keyed in time: [[t, v], ...], eased (smoothstep) between keys, held before the first and after the last
function keyed(ks, t, dflt) {
  const k = list(ks); if (!k.length) return dflt;
  if (t <= k[0][0]) return k[0][1];
  for (let i = 1; i < k.length; i++) if (t < k[i][0]) { const [t0, v0] = k[i - 1], [t1, v1] = k[i]; return v0 + (v1 - v0) * sstep((t - t0) / Math.max(1e-6, t1 - t0)); }
  return k[k.length - 1][1];
}
// a damped wobble started at each time of a list: [[t, amplitude, frequency (rad/s), decay (1/s)], ...] (they add up)
function wobble(ks, t) {
  let v = 0;
  for (const [t0, a, f = 30, d = 6] of list(ks)) { const u = t - t0; if (u >= 0) v += a * Math.exp(-d * u) * Math.sin(f * u); }
  return v;
}

// ---- a tiny person (pivot at the feet, about h tall, front +Z): a hiker with a backpack and a stick, or a skier with skis, poles and a bobble hat.
// pose(t, name, phase): 'walk' (legs and arms swing, a bob), 'ski' (crouched, swaying), 'hang' (arms out, legs dangling, a slow swing: in the air
// before the fall), 'flail' (arms windmilling, legs kicking: falling), 'sit' (on the ground, legs out), 'wave' (one arm up and waving)
function figure(kind, color, h, seed = 1) {
  const r = rng(seed), k = h / 0.2, skin = '#E2A97E', pants = kind === 'skier' ? '#2E3A55' : '#5B4A3A';
  const g = grp(), body = grp(); g.add(body);
  const legL = grp(at(box(0.026 * k, 0.085 * k, 0.03 * k, pants, { pivot: 'top' }), 0, 0, 0)), legR = grp(at(box(0.026 * k, 0.085 * k, 0.03 * k, pants, { pivot: 'top' }), 0, 0, 0));
  legL.position.set(0.017 * k, 0.088 * k, 0); legR.position.set(-0.017 * k, 0.088 * k, 0);
  const torso = at(box(0.062 * k, 0.07 * k, 0.04 * k, color, { outline: 0.03 }), 0, 0.123 * k, 0);
  const head = at(box(0.04 * k, 0.045 * k, 0.04 * k, skin, { outline: 0.04 }), 0, 0.182 * k, 0);
  const hat = kind === 'skier' ? grp(at(box(0.044 * k, 0.016 * k, 0.044 * k, '#D93A3A'), 0, 0.21 * k, 0), at(sphere(0.012 * k, '#F4F4F4', 0), 0, 0.224 * k, 0))
    : at(box(0.05 * k, 0.01 * k, 0.05 * k, '#6E8B3D'), 0, 0.205 * k, 0);
  const eyes = grp(at(box(0.006 * k, 0.008 * k, 0.002 * k, '#1C1C1E'), 0.009 * k, 0.186 * k, 0.021 * k), at(box(0.006 * k, 0.008 * k, 0.002 * k, '#1C1C1E'), -0.009 * k, 0.186 * k, 0.021 * k));
  const armL = grp(at(box(0.016 * k, 0.065 * k, 0.018 * k, color, { pivot: 'top' }), 0, 0, 0)), armR = grp(at(box(0.016 * k, 0.065 * k, 0.018 * k, color, { pivot: 'top' }), 0, 0, 0));
  armL.position.set(0.04 * k, 0.153 * k, 0); armR.position.set(-0.04 * k, 0.153 * k, 0);
  body.add(legL, legR, torso, head, hat, eyes, armL, armR);
  let skis = null, poles = [];
  if (kind === 'skier') {
    skis = grp(at(box(0.014 * k, 0.004 * k, 0.17 * k, '#F2C230'), 0.017 * k, 0.002 * k, 0.02 * k), at(box(0.014 * k, 0.004 * k, 0.17 * k, '#F2C230'), -0.017 * k, 0.002 * k, 0.02 * k));
    legL.add(at(skis.children[0], 0, -0.085 * k, 0.02 * k)); legR.add(at(skis.children[0] || box(0.014 * k, 0.004 * k, 0.17 * k, '#F2C230'), 0, -0.085 * k, 0.02 * k));
    for (const a of [armL, armR]) { const p = at(cyl(0.002 * k, 0.002 * k, 0.11 * k, '#3A3A40', 4, { pivot: 'top' }), 0, -0.062 * k, 0); a.add(p); poles.push(p); }
  } else {
    body.add(at(box(0.05 * k, 0.06 * k, 0.026 * k, '#C4572E', { outline: 0.03 }), 0, 0.128 * k, -0.033 * k));   // the backpack
    const stick = at(cyl(0.0025 * k, 0.0025 * k, 0.12 * k, '#7A5634', 4, { pivot: 'top' }), 0, -0.062 * k, 0.004 * k); armR.add(stick);
  }
  const ph0 = r() * TAU;
  const pose = (t, name = 'walk') => {
    const w = t * 9 + ph0; body.position.set(0, 0, 0); body.rotation.set(0, 0, 0); legL.rotation.set(0, 0, 0); legR.rotation.set(0, 0, 0);
    armL.rotation.set(0, 0, 0); armR.rotation.set(0, 0, 0); head.rotation.set(0, 0, 0); eyes.rotation.set(0, 0, 0);
    if (name === 'walk') { const s = Math.sin(w); legL.rotation.x = 0.55 * s; legR.rotation.x = -0.55 * s; armL.rotation.x = -0.5 * s; armR.rotation.x = 0.5 * s; body.position.y = 0.006 * k * Math.abs(Math.cos(w)); body.rotation.x = 0.12; }
    else if (name === 'ski') { const s = Math.sin(t * 4 + ph0); body.rotation.x = 0.35; body.position.y = -0.012 * k; legL.rotation.x = -0.5; legR.rotation.x = -0.5; armL.rotation.x = 0.6; armR.rotation.x = 0.6; body.rotation.z = 0.18 * s; }
    else if (name === 'hang') { const s = Math.sin(t * 3 + ph0); armL.rotation.z = 2.3 + 0.15 * s; armR.rotation.z = -2.3 - 0.15 * s; legL.rotation.x = 0.25 * s; legR.rotation.x = -0.25 * s; body.rotation.z = 0.06 * s; }
    else if (name === 'flail') { const s = Math.sin(t * 26 + ph0), c = Math.cos(t * 26 + ph0); armL.rotation.set(2.6 * s, 0, 1.9 + 0.6 * c); armR.rotation.set(-2.6 * s, 0, -1.9 - 0.6 * c); legL.rotation.x = 0.9 * c; legR.rotation.x = -0.9 * c; }
    else if (name === 'sit') { body.position.y = -0.06 * k; legL.rotation.x = -1.45; legR.rotation.x = -1.45; armL.rotation.x = -0.4; armR.rotation.x = -0.4; }
    else if (name === 'wave') { const s = Math.sin(t * 14 + ph0); armR.rotation.z = -2.7 - 0.35 * s; }
    else if (name === 'look') { head.rotation.x = 0.5; }
  };
  pose(0, kind === 'skier' ? 'ski' : 'walk');
  return { g, pose, head };
}

// a little ski-lift chair: a bench on a hanger (pivot at the grip on the cable)
function liftChair(k, color) {
  return grp(at(cyl(0.003 * k, 0.003 * k, 0.12 * k, '#3A3A40', 4, { pivot: 'top' }), 0, 0, 0), at(box(0.09 * k, 0.012 * k, 0.04 * k, color, { outline: 0.03 }), 0, -0.12 * k, 0.012 * k),
    at(box(0.09 * k, 0.04 * k, 0.008 * k, color), 0, -0.1 * k, -0.006 * k));
}

export const BOSSE_PROPS = {
  // A bump on the skull that grows into a hill (pivot on the top of the skull: attach it to the head joint at [0, 0.5, 0]). Its size is a radius in
  // metres keyed in time, o.grow [[t, radius], ...] (eased between keys; o.r: a fixed one). o.mode 'ball' (the default without hill dressing): a ball of
  // skin that rises out of the skull, half buried while it is small, then sitting on it on a neck o.rb (0.11 m) wide; reddened by o.red (0..1), a shine
  // on its brow. o.mode 'hill' (the default with any dressing): a dome o.hr (0.7) as high as it is wide, its underside skin, balanced on his head.
  // o.throb [amp, beats per second, from, to]: it swells at each heartbeat (a quick rise, a slower fall). o.deflate [t, dur]: it goes down like a
  // balloon, wobbling, to nothing; o.plaster: a crossed plaster on the skull after it. Dressing (it scales with the bump, in the units of a radius of
  // 1): o.grass (a green cap 0..1 of the way down; o.grassAt: it spreads from the top from that time), o.snow (a white cap 0..1), o.trees (n),
  // o.path (a winding beige path to the top), o.flag, o.plaque (lines on a blue enamel plate on a post at the top: ['COLLINE']; o.plaqueAt: it drops
  // in from above and sinks in), o.hikers [[u0, speed, color], ...] walking up the path, o.skiers [[u0, speed, color, side], ...] sliding down in
  // zig-zags, o.lift (a chair lift up one side: pylons, cable, chairs). o.tape {phi, u: [[t, 0..1]], snap, readout: [text, from, to]}: a yellow tape
  // measure laid down a meridian from the top (phi: its side, PI / 2 = +Z), unrolled to u of the way down; from `snap` it whips back up to the top
  // and its hook flies on above it. userData.top(): the summit in the prop's frame at the current size.
  skullBump(o) {
    const dressed = !!(o.grass && o.mode === 'hill') || !!(o.snow || o.trees || o.path || o.hikers || o.skiers || o.lift);
    const mode = o.mode || (dressed ? 'hill' : 'ball'), HILL = mode === 'hill', HR = HILL ? (o.hr ?? 0.7) : 1, RB = o.rb ?? 0.11;
    const skinC = new THREE.Color(o.color || '#DDA273'), redC = new THREE.Color('#E0705C');
    const skinHex = '#' + skinC.clone().lerp(redC, Math.max(0, Math.min(1, o.red ?? 0.35))).getHexString();
    let domeGeo; if (HILL) { domeGeo = new THREE.SphereGeometry(1, 18, 9, 0, TAU, 0, PI / 2); domeGeo.scale(1, HR, 1); } else domeGeo = new THREE.SphereGeometry(1, 20, 14);
    const dome = new THREE.Mesh(domeGeo, mat(skinHex)); dome.castShadow = dome.receiveShadow = true; addOutline(dome, 0.025);
    const dg = grp(dome);
    if (HILL) { const cap = new THREE.Mesh(new THREE.CircleGeometry(1, 18).rotateX(PI / 2), mat(skinHex)); cap.position.y = 0.002; dg.add(cap); }   // its underside, seen from below
    const shine = at(sphere(0.22, '#FFF1E2', 1, { noGrain: true }), -0.32, HILL ? HR * 0.78 : 0.62, 0.62); shine.scale.set(1.0, 0.5, 0.45); shine.castShadow = false;
    if (o.shine !== false && !o.grass && !o.snow) dg.add(shine);
    const S = (th, ph, lift = 0) => new THREE.Vector3(Math.sin(th) * Math.cos(ph) * (1 + lift), HR * Math.cos(th) * (1 + lift), Math.sin(th) * Math.sin(ph) * (1 + lift));
    const r = rng(o.seed || 7);
    let grass = null, snow = null;
    if (o.grass) { const gg = new THREE.SphereGeometry(1.012, HILL ? 18 : 20, HILL ? 9 : 14, 0, TAU, 0, (HILL ? PI / 2 : PI) * Math.min(1, o.grass)); gg.scale(1, HR, 1); grass = new THREE.Mesh(gg, mat(o.grassColor || '#7DB955')); grass.receiveShadow = true; dg.add(grass); }
    if (o.snow) { const sg = new THREE.SphereGeometry(1.03, 18, 9, 0, TAU, 0, (HILL ? PI / 2 : PI) * Math.min(1, o.snow)); sg.scale(1, HR, 1); snow = new THREE.Mesh(sg, mat('#F6F8FB')); snow.receiveShadow = true; dg.add(snow); }
    const dress = grp(); dg.add(dress);
    for (let i = 0; i < (o.trees || 0); i++) {   // trees stand upright on the slope
      const th = 0.45 + r() * 0.85, ph = r() * TAU, p = S(th, ph), hT = 0.1 + r() * 0.06;
      const tr = grp(at(cyl(0.008, 0.01, hT * 0.35, '#6B4A2E', 5, { pivot: 'bottom' }), 0, 0, 0), at(cyl(0, hT * 0.38, hT, o.snow ? '#3E7A5A' : '#3F7F45', 6, { pivot: 'bottom' }), 0, hT * 0.25, 0));
      if (o.snow) tr.add(at(cyl(0, hT * 0.2, hT * 0.4, '#F6F8FB', 6, { pivot: 'bottom' }), 0, hT * 0.82, 0));
      tr.position.copy(p).multiplyScalar(0.985); dress.add(tr);
    }
    const PATHN = 46, TURNS = o.turns ?? 1.6, PH0 = o.pathPhase ?? 0.6;
    const pathAt = u => ({ th: PI / 2 * (1 - u) * 0.97 + 0.02, ph: PH0 + u * TURNS * TAU });   // u = 0 at the foot, 1 at the top
    if (o.path) for (let i = 0; i < PATHN; i++) {
      const u = i / PATHN, a = pathAt(u), b = pathAt(u + 1 / PATHN), pa = S(a.th, a.ph, 0.016), pb = S(b.th, b.ph, 0.016);
      const seg = box(0.06, 0.006, pa.distanceTo(pb) * 1.15, o.snow ? '#E3D7C2' : '#D8C190'); seg.position.copy(pa).add(pb).multiplyScalar(0.5); seg.lookAt(pb); seg.receiveShadow = true; dress.add(seg);
    }
    let flag = null;
    if (o.flag) { flag = grp(at(cyl(0.005, 0.005, 0.22, '#5A5A60', 5, { pivot: 'bottom' }), 0, 0, 0)); const cloth = at(box(0.11, 0.07, 0.004, o.flagColor || '#D93A3A'), 0.058, 0.18, 0); flag.add(cloth); flag.position.copy(S(0.06, 1.0)); dress.add(flag); flag.userData.cloth = cloth; }
    let plaque = null;
    if (o.plaque) {   // a blue enamel plate on a post, French street-name style
      const lines = list(o.plaque), w = 0.36, h = 0.16;
      const face = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#1D3F8A'; c.fillRect(0, 0, W, H); c.strokeStyle = '#2E8A4E'; c.lineWidth = W * 0.03; c.strokeRect(W * 0.03, W * 0.03, W * 0.94, H - W * 0.06);
        c.strokeStyle = '#F4F2EA'; c.lineWidth = W * 0.008; c.strokeRect(W * 0.06, W * 0.06, W * 0.88, H - W * 0.12); c.fillStyle = '#F4F2EA'; c.textAlign = 'center'; c.textBaseline = 'middle';
        const n = lines.length, lh = H * 0.74 / n; for (let i = 0; i < n; i++) { let fs = lh * 0.8; c.font = `700 ${fs}px Poppins, Arial, sans-serif`; while (c.measureText(lines[i]).width > W * 0.8 && fs > 8) { fs -= 2; c.font = `700 ${fs}px Poppins, Arial, sans-serif`; } c.fillText(lines[i], W / 2, H * 0.13 + lh * (i + 0.5)); } }, { res: 512 });
      face.position.z = 0.009;
      plaque = grp(at(cyl(0.008, 0.008, 0.34, '#3A4A40', 6, { pivot: 'bottom' }), 0, 0, -0.012), at(grp(at(box(w + 0.014, h + 0.014, 0.014, '#163370', { outline: 0.02 }), 0, 0, 0), face), 0, 0.34 - h / 2, 0));
      plaque.position.copy(S(0, 0)); plaque.position.y -= 0.02; plaque.rotation.y = o.plaqueYaw ?? 0; plaque.scale.setScalar(o.plaqueScale ?? 1); dress.add(plaque);   // o.plaqueScale: bigger for a far camera
    }
    let chairs = [], LA = null, LB = null;   // the chair lift: pylons, a cable, chairs going up
    if (o.lift) {
      const ph = o.liftPhase ?? -0.4, p0 = S(1.42, ph, 0.02), p1 = S(0.22, ph, 0.02), up = 0.2;
      LA = p0.clone().add(new THREE.Vector3(0, up, 0)); LB = p1.clone().add(new THREE.Vector3(0, up, 0));
      for (const p of [p0, S(0.85, ph, 0.02), p1]) dress.add(at(cyl(0.007, 0.009, up + 0.02, '#4A4E56', 5, { pivot: 'bottom' }), p.x, p.y - 0.01, p.z));
      dress.add(rod([LA.x, LA.y, LA.z], [LB.x, LB.y, LB.z], 0.003, '#2A2A30'));
      for (let i = 0; i < (o.chairs ?? 5); i++) { const c = liftChair(1, ['#D93A3A', '#2F6FB5', '#F2C230'][i % 3]); dress.add(c); chairs.push(c); }
    }
    const hikers = list(o.hikers).map((h, i) => { const f = figure('hiker', h[2] || ['#3C8DD9', '#E0A030', '#C8463A'][i % 3], 0.13, 11 + i); dress.add(f.g); return { f, u0: h[0] ?? 0, sp: h[1] ?? 0.08 }; });
    const skiers = list(o.skiers).map((s, i) => { const f = figure('skier', s[2] || ['#E04A3A', '#3A8FE0', '#7A4AC8', '#2EA86A'][i % 4], 0.13, 21 + i); dress.add(f.g); return { f, u0: s[0] ?? 0, sp: s[1] ?? 0.22, side: s[3] ?? (i * 1.7) }; });
    // the doctor's tape measure, laid down a meridian of the ball
    const tp = o.tape; let tapeSegs = [], hook = null, tag = null;
    const TN = 40, TEND = tp?.end ?? 2.5;
    if (tp) {
      const ph = tp.phi ?? PI / 2;
      for (let i = 0; i < TN; i++) { const a = S(TEND * i / TN, ph, 0.012), b = S(TEND * (i + 1) / TN, ph, 0.012);
        const sg = box(tp.w ?? 0.04, 0.006, a.distanceTo(b) * 1.04, i % 4 === 3 ? '#1C1C1E' : '#F5CE2E'); sg.position.copy(a).add(b).multiplyScalar(0.5); sg.lookAt(b); dress.add(sg); tapeSegs.push(sg); }
      hook = box(0.06, 0.03, 0.04, '#B88A3A', { outline: 0.03 }); dress.add(hook);
      if (tp.readout) { const tw = tp.tagW ?? 0.55, th = tw * 0.42; tag = canvasPlane(tw, th, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.strokeStyle = '#1C1C1E'; c.lineWidth = H * 0.06; c.strokeRect(0, 0, W, H);
          c.fillStyle = '#1C1C1E'; c.textAlign = 'center'; c.textBaseline = 'middle'; let fs = H * 0.62; c.font = `900 ${fs}px Arial`; while (c.measureText(tp.readout[0]).width > W * 0.86) { fs -= 2; c.font = `900 ${fs}px Arial`; } c.fillText(tp.readout[0], W / 2, H * 0.54); }, { res: 384 });
        tag.material = new THREE.MeshBasicMaterial({ map: tag.material.map, side: THREE.DoubleSide, toneMapped: false }); const tph = ph + (tp.tagDphi ?? 0), tq = S(tp.tagAt ?? 0.32, tph, 0.08); tag.position.copy(tq); tag.rotation.y = PI / 2 - tph; dress.add(tag); }   // (pass 4 of 56) tagDphi: the tag beside the tape, not on it
    }
    // the plaster after it went down (at the scale of the head, not of the bump)
    const plaster = o.plaster ? grp(at(box(0.15, 0.008, 0.035, '#F0D9B8', { outline: 0.03 }), 0, 0.004, 0, 0, 0.7, 0), at(box(0.15, 0.008, 0.035, '#F0D9B8', { outline: 0.03 }), 0, 0.006, 0, 0, -0.7, 0)) : null;
    const g = grp(dg); if (plaster) g.add(plaster);
    let size = o.r ?? 0.06;
    const lift0 = R => HILL ? 0 : Math.sqrt(Math.max(0, R * R - RB * RB));   // a ball sits on the skull on a neck RB wide, half buried while it is smaller than that
    g.userData.top = () => new THREE.Vector3(0, lift0(size) + HR * size, 0);
    g.userData.update = t => {
      let R = keyed(o.grow, t, o.r ?? 0.06);
      const th = o.throb; if (th) { const [amp, rate = 1.6, t0 = -1e9, t1 = 1e9] = th; if (t >= t0 && t <= t1) { const ph = ((t - t0) * rate) % 1; R *= 1 + amp * Math.exp(-ph * 7) * (1 - Math.exp(-ph * 55)); } }
      let sy = 1, sxz = 1;
      const df = o.deflate; if (df) { const u = (t - df[0]) / (df[1] || 0.5); if (u >= 1) R = 0.0001; else if (u > 0) { R *= Math.max(0.0001, 1 - sstep(u)); const wv = Math.sin(u * 40) * 0.22 * (1 - u); sy = 1 - 0.38 * sstep(Math.min(1, u * 1.6)) + wv; sxz = 1 + 0.18 * Math.sin(Math.min(1, u * 1.3) * PI) - wv * 0.6; } }   // (pass 2 of 56) it sags and bulges as it empties (it shrank evenly)
      size = R; dg.scale.set(R * sxz, R * sy, R * sxz); dg.position.y = lift0(R); dg.visible = R > 0.0005;
      if (plaster) plaster.visible = !!df && t >= df[0] + (df[1] || 0.5) * 0.85;
      if (grass && o.grassAt != null) { const u = Math.max(0, Math.min(1, (t - o.grassAt) / 0.35)); grass.visible = u > 0.01; grass.geometry.setDrawRange(0, Math.ceil(grass.geometry.index.count * Math.max(0.02, u) / 3) * 3); }
      if (plaque && o.plaqueAt != null) { const u = t - o.plaqueAt, top = S(0, 0); plaque.visible = u >= -0.12; plaque.position.set(top.x, top.y - 0.02 + (u < 0 ? -u * 6 : 0) - (u >= 0 && u < 0.12 ? 0.05 * Math.sin(u / 0.12 * PI) : 0), top.z); }
      for (const h of hikers) { const u = Math.min(0.985, (h.u0 + h.sp * t) % 1.0), a = pathAt(u), b = pathAt(Math.min(1, u + 0.02)), p = S(a.th, a.ph, 0.02), q = S(b.th, b.ph, 0.02);
        h.f.g.position.copy(p); h.f.g.rotation.set(0, Math.atan2(q.x - p.x, q.z - p.z), 0);   // (story 56) the yaw by hand: lookAt takes world points and laid them down once the hill sat on a head
        h.f.pose(t, u > 0.97 ? 'wave' : 'walk'); }
      for (const s of skiers) { const u = (s.u0 + s.sp * t) % 1.0, th2 = 0.12 + u * 1.3, ph = s.side + 0.35 * Math.sin(u * TAU * 2.2), p = S(th2, ph, 0.02), q = S(Math.min(1.5, th2 + 0.04), s.side + 0.35 * Math.sin((u + 0.02) * TAU * 2.2), 0.02);
        s.f.g.position.copy(p); s.f.g.rotation.set(0, Math.atan2(q.x - p.x, q.z - p.z), 0); s.f.pose(t, 'ski'); }
      if (chairs.length) { const n = chairs.length; chairs.forEach((c, i) => { const u = ((i / n) + t * (o.liftSpeed ?? 0.12)) % 1; c.position.lerpVectors(LA, LB, u); c.rotation.z = 0.08 * Math.sin(t * 2 + i); }); }
      if (flag) flag.userData.cloth.rotation.y = 0.25 * Math.sin(t * 7);
      if (tp) {
        let u = keyed(tp.u, t, 0), fly = -1;
        if (tp.snap != null && t >= tp.snap) { const v = (t - tp.snap) / 0.12; if (v < 1) u *= 1 - v * v; else { u = 0; fly = (t - tp.snap - 0.12) / 0.18; } }
        const n = Math.round(u * TN); tapeSegs.forEach((sg, i) => { sg.visible = i < n; });
        const ph = tp.phi ?? PI / 2, end = S(TEND * Math.max(0.002, u), ph, 0.03);
        // (pass 2 of 56) tp.hookTo [x, y, z] (in the ball's own frame, radius 1): the hook flies on an arc from the top to that point (the doctor's nose)
        // and hangs there 0.2 s before it drops (it flew straight up off the top: the CLAC had no cause)
        if (fly < 0) { hook.visible = u > 0.01; hook.position.copy(end); }
        else if (tp.hookTo) { const [hx, hy, hz] = tp.hookTo, f = Math.min(1, fly), e = f * f * (3 - 2 * f); hook.visible = fly < 2.1;
          hook.position.set(hx * e, HR + (hy - HR) * e + 0.35 * Math.sin(f * PI), hz * e - (fly > 1.1 ? (fly - 1.1) * 0.6 : 0)); hook.rotation.set(fly < 1 ? fly * 7 : 0.3, 0, 0); }
        else { hook.visible = fly < 1; hook.position.set(0, HR * (1 + 0.6 * fly), 0.15 * fly); hook.rotation.x = fly * 9; }
        if (tag) tag.visible = t >= (tp.readout[1] ?? -1e9) && t <= (tp.readout[2] ?? 1e9) && (tp.snap == null || t < tp.snap);
      }
    };
    g.userData.update(0); return g;
  },

  // A tiny person standing alone (pivot at the feet, o.h tall, 0.2 m): o.kind 'hiker' | 'skier', o.color (the jacket), o.pose ('walk', 'ski', 'hang',
  // 'flail', 'sit', 'wave', 'look') or o.poses [[t, name], ...] (the latest one wins): the skiers hang in the air where the slope was, look down, then flail
  miniFigure(o) {
    const f = figure(o.kind || 'skier', o.color || '#E04A3A', o.h ?? 0.2, o.seed || 3), g = grp(f.g);
    g.userData.update = t => { let p = o.pose || (o.kind === 'hiker' ? 'walk' : 'ski'); for (const [t0, nm] of list(o.poses)) if (t >= t0) p = nm; f.pose(t, p); };
    g.userData.update(0); return g;
  },

  // A tape measure (pivot at the case, the tape runs out along +Y): a yellow case with a black belt clip, a yellow tape with black ticks, a brass hook
  // at its end. o.len [[t, length], ...] (eased); o.snap: from that time the tape whips back into the case in 0.14 s, the end lashing about;
  // o.readout ['3,00 M', from, to]: a white tag at the end of the tape with the reading, big enough to read at phone size (o.tagW 0.28).
  tapeMeasure(o) {
    const g = grp(), cs = o.case ?? 0.11;
    g.add(at(box(cs, cs, cs * 0.45, '#F2C230', { outline: 0.03 }), 0, 0, 0), at(cyl(cs * 0.3, cs * 0.3, cs * 0.47, '#2A2A30', 12), 0, 0, 0, PI / 2, 0, 0), at(box(cs * 0.3, cs * 0.12, cs * 0.5, '#2A2A30'), 0, cs * 0.44, 0));
    const tex = (() => { const c = document.createElement('canvas'); c.width = 64; c.height = 512; const x = c.getContext('2d'); x.fillStyle = '#F5CE2E'; x.fillRect(0, 0, 64, 512); x.fillStyle = '#1C1C1E';
      for (let i = 0; i < 50; i++) { const y = i * 512 / 50, L = i % 10 === 0 ? 40 : i % 5 === 0 ? 28 : 16; x.fillRect(0, y, L, 3); } const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapT = THREE.RepeatWrapping; return t; })();
    const tapeM = new THREE.MeshLambertMaterial({ map: tex, side: THREE.DoubleSide }), tapeG = new THREE.PlaneGeometry(0.032, 1); tapeG.translate(0, 0.5, 0);
    const tape = new THREE.Mesh(tapeG, tapeM), tg = grp(tape); tg.position.set(0, cs * 0.5, cs * 0.12); g.add(tg);
    const hook = at(box(0.04, 0.012, 0.03, '#B88A3A', { outline: 0.03 }), 0, 0, 0.012); tg.add(hook);
    let tag = null; const ro = o.readout;
    if (ro) { const tw = o.tagW ?? 0.28, th = tw * 0.42; tag = canvasPlane(tw, th, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.strokeStyle = '#1C1C1E'; c.lineWidth = H * 0.06; c.strokeRect(0, 0, W, H);
        c.fillStyle = '#1C1C1E'; c.textAlign = 'center'; c.textBaseline = 'middle'; let fs = H * 0.62; c.font = `900 ${fs}px Arial`; while (c.measureText(ro[0]).width > W * 0.86) { fs -= 2; c.font = `900 ${fs}px Arial`; } c.fillText(ro[0], W / 2, H * 0.54); }, { res: 384 });
      tag.material = new THREE.MeshBasicMaterial({ map: tag.material.map, side: THREE.DoubleSide, toneMapped: false }); tg.add(tag); }
    g.userData.update = t => {
      let L = keyed(o.len, t, 0.05), lash = 0;
      if (o.snap != null && t >= o.snap) { const u = (t - o.snap) / 0.14; L = u >= 1 ? 0.02 : L * (1 - u * u); lash = u < 1 ? 0.5 * Math.sin(u * 22) * (1 - u) : 0.12 * Math.exp(-(t - o.snap - 0.14) * 9) * Math.sin((t - o.snap) * 40); }
      L = Math.max(0.02, L); tape.scale.y = L; tex.repeat.set(1, L * 2); hook.position.y = L; tg.rotation.z = lash;
      if (tag) { tag.visible = t >= (ro[1] ?? -1e9) && t <= (ro[2] ?? 1e9) && (o.snap == null || t < o.snap); tag.position.set(o.tagSide ?? 0.17, L - 0.02, 0.01); }
    };
    g.userData.update(0); return g;
  },

  // A bill that unrolls to the floor and away along it (pivot at the top edge, held in the hands, o.top (1.1 m) above the floor; it falls along -Y,
  // then runs along +Z on the floor): white paper o.w (0.3) wide with a heading (o.head 'FORFAITS') and rows of items with prices, a roll at its
  // end that rolls on. o.len [[t, length], ...] (eased): how much of it has unrolled; the rows repeat every o.rowsPer (0.45 m).
  billScroll(o) {
    const w = o.w ?? 0.3, top = o.top ?? 1.1, head = o.head || 'FORFAITS', g = grp();
    const rowsTex = (() => { const c = document.createElement('canvas'); c.width = 256; c.height = 512; const x = c.getContext('2d'); x.fillStyle = '#FBFAF4'; x.fillRect(0, 0, 256, 512); x.fillStyle = '#3A3A40';
      const items = o.items || ['FORFAIT JOURNÉE', 'FORFAIT SEMAINE', 'TÉLÉSIÈGE', 'LOCATION SKIS', 'CHOCOLAT CHAUD', 'FORFAIT ENFANT'];
      for (let i = 0; i < 6; i++) { const y = 40 + i * 80, pr = `${[49, 245, 12, 38, 4, 31][i]} €`, nm = items[i % items.length]; x.textAlign = 'right'; x.font = '700 24px Arial'; const pw = x.measureText(pr).width; x.fillText(pr, 242, y);
        x.textAlign = 'left'; let fs = 22; x.font = `600 ${fs}px Arial`; while (x.measureText(nm).width > 228 - pw - 12 && fs > 11) { fs -= 1; x.font = `600 ${fs}px Arial`; } x.fillText(nm, 14, y); x.fillRect(14, y + 18, 228, 2); }   // (pass 3 of 56) the name shrinks to clear its price (« CHOCOLAT CHAUD » ran into it)
      const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapT = THREE.RepeatWrapping; return t; })();
    const mk = () => { const tx = rowsTex.clone(); tx.needsUpdate = true; tx.wrapT = THREE.RepeatWrapping; const m = new THREE.Mesh(new THREE.PlaneGeometry(w, 1), new THREE.MeshLambertMaterial({ map: tx, side: THREE.DoubleSide })); m.receiveShadow = true; return m; };
    const down = mk(); down.geometry.translate(0, -0.5, 0); const along = mk(); along.geometry.translate(0, 0.5, 0); along.rotation.x = PI / 2;
    const hd = canvasPlane(w, w * 0.32, (c, W, H) => { c.fillStyle = '#C8302A'; c.fillRect(0, 0, W, H); c.fillStyle = '#FFFFFF'; c.textAlign = 'center'; c.textBaseline = 'middle'; let fs = H * 0.62; c.font = `900 ${fs}px Arial`; while (c.measureText(head).width > W * 0.88) { fs -= 2; c.font = `900 ${fs}px Arial`; } c.fillText(head, W / 2, H * 0.55); }, { res: 384 });
    hd.position.set(0, -w * 0.16, 0.002);
    const roll = at(cyl(0.035, 0.035, w * 1.02, '#F4F2EA', 12), 0, 0, 0, 0, 0, PI / 2); addOutline(roll, 0.04);
    g.add(down, along, hd, roll);
    g.userData.update = t => {
      const L = Math.max(0.05, keyed(o.len, t, 0.3)), Lv = Math.min(L, top - 0.035), Lf = Math.max(0, L - Lv);
      down.scale.y = Lv; down.material.map.repeat.set(1, Lv / (o.rowsPer ?? 0.45)); down.material.map.offset.set(0, -Lv / (o.rowsPer ?? 0.45));
      along.visible = Lf > 0.002; along.scale.y = Math.max(0.002, Lf); along.position.set(0, -top + 0.003, 0); along.material.map.repeat.set(1, Lf / (o.rowsPer ?? 0.45));
      if (Lf > 0.002) { roll.position.set(0, -top + 0.035, Lf); roll.rotation.set(Lf / 0.035, 0, PI / 2); } else { roll.position.set(0, -Lv, 0.0); roll.rotation.set(Lv / 0.035, 0, PI / 2); }
    };
    g.userData.update(0); return g;
  },

  // A doorway with a low beam (pivot at the floor in its middle, the passage along Z): two wooden posts and a beam o.h (1.72 m) up, o.w (1.3) wide,
  // a yellow sign on its face (o.sign 'ATTENTION À LA TÊTE'). o.shake [[t, amp], ...]: the beam quivers after a head hits it.
  lowBeam(o) {
    const w = o.w ?? 1.3, h = o.h ?? 1.72, bh = 0.2, g = grp(), C = o.color || '#8A5A34';
    for (const s of [-1, 1]) g.add(at(box(0.16, h + bh, 0.18, C, { outline: 0.012, pivot: 'bottom' }), s * (w / 2 + 0.08), 0, 0));
    // (pass 2 of 56) o.wall [width, height, colour]: the doorway set in a section of wall (a free-standing frame read as a prop on the floor)
    if (o.wall) { const [ww, wh, wc] = o.wall; for (const s of [-1, 1]) g.add(at(box(ww, wh, 0.14, wc || '#E9DCC6', { outline: 0.006, pivot: 'bottom' }), s * (w / 2 + 0.16 + ww / 2), 0, -0.01));
      g.add(at(box(w + 0.32, Math.max(0.01, wh - h - bh), 0.14, wc || '#E9DCC6', { outline: 0.006, pivot: 'bottom' }), 0, h + bh, -0.01)); }
    const beam = grp(at(box(w + 0.5, bh, 0.22, C, { outline: 0.012 }), 0, 0, 0)); beam.position.y = h + bh / 2; g.add(beam);
    if (o.sign !== false) { const txt = o.sign || 'ATTENTION À LA TÊTE', sw = Math.min(w * 0.9, 1.0), sh = 0.14;
      const sg = canvasPlane(sw, sh, (c, W, H) => { c.fillStyle = '#F2C230'; c.fillRect(0, 0, W, H); c.fillStyle = '#1C1C1E'; c.fillRect(0, 0, W, H * 0.1); c.fillRect(0, H * 0.9, W, H * 0.1);
        c.textAlign = 'center'; c.textBaseline = 'middle'; let fs = H * 0.5; c.font = `900 ${fs}px Arial`; while (c.measureText(txt).width > W * 0.92) { fs -= 2; c.font = `900 ${fs}px Arial`; } c.fillText(txt, W / 2, H * 0.53); }, { res: 512 });
      sg.position.set(0, 0, 0.115); beam.add(sg); }
    g.userData.update = t => { let a = 0; for (const [t0, k] of list(o.shake)) { const u = t - t0; if (u >= 0) a += k * Math.exp(-6 * u) * Math.sin(48 * u); } beam.position.y = h + bh / 2 + a * 0.6; beam.rotation.z = a; };
    g.userData.update(0); return g;
  },

  // A surveyor's level on its tripod (pivot at the floor, it sights along +Z): three wooden legs with steel feet, a yellow instrument with a lens, an
  // eyepiece at the back (about 1.45 m up), a little sun hood
  theodolite(o) {
    const H = o.h ?? 1.35, g = grp();
    for (let i = 0; i < 3; i++) { const a = i * TAU / 3 + 0.5, f = [Math.cos(a) * 0.38, 0, Math.sin(a) * 0.38]; g.add(rod(f, [0, H, 0], 0.016, '#B07A3E'), at(cyl(0.012, 0.004, 0.06, '#8E9398', 5), f[0], 0.03, f[2])); }
    g.add(at(cyl(0.11, 0.11, 0.03, '#3A3A40', 10), 0, H + 0.015, 0), at(box(0.16, 0.16, 0.24, '#F2C230', { outline: 0.02 }), 0, H + 0.11, 0),
      at(cyl(0.035, 0.045, 0.14, '#2A2A30', 10), 0, H + 0.12, 0.17, PI / 2, 0, 0), at(cyl(0.02, 0.02, 0.06, '#2A2A30', 8), 0, H + 0.12, -0.15, PI / 2, 0, 0),
      at(sphere(0.03, '#9FD3FF', 0, { emissive: '#4A7FAA' }), 0, H + 0.12, 0.24));
    return g;
  },
};
