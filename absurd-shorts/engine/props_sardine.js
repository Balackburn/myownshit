// « La sardine » (story 108, cycle 57): this man pitched his tent with one peg missing, so he drove in a real sardine, in oil. The storm takes the
// whole campsite but his tent; the whole country plants sardines; the seagulls follow the smell and pull up a campsite a night; thirty thousand tents
// migrate south in a V; the whole country sleeps in his tent, packed like sardines; in the morning his sardine is gone and they plant the biggest one:
// him. All along a seagull keeps the stolen chrome peg in its beak.
// Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time. Every name
// starts with `sa`. No word, figure, currency sign, flag, emblem or cross anywhere: the tin has no label, the scale a blank dial, the tents are plain.
import * as THREE from 'three';
import { box, cyl, sphere, mat, addOutline } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const u = clamp01(x); return u * u * (3 - 2 * u); };
const hsh = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
// a value keyed in time: keys [[t, v], ...] (sorted), eased (smoothstep) between keys; a plain number is a constant
function kv(keys, t, def = 0) {
  if (keys == null) return def;
  if (typeof keys === 'number') return keys;
  if (!keys.length) return def;
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) { const [a, va] = keys[i], [b, vb] = keys[i + 1]; if (t < b) return va + (vb - va) * smooth((t - a) / Math.max(1e-4, b - a)); }
  return keys[keys.length - 1][1];
}
// a bounce after each time in ts: 1 at the hit, decaying (for squashes)
const bump = (ts, t, k = 9, f = 28) => (ts || []).reduce((s, t0) => { const u = t - t0; return u > 0 && u < 0.8 ? s + Math.exp(-k * u) * Math.cos(u * f) : s; }, 0);
const CHROME = '#D9DEE4';
// a glint: a slim four-point star tilted 45 degrees (never an upright cross), pulsing every `every` seconds
function glint(size, every = 1.3, ph = 0) {
  const g = grp(); const mk = (w, h) => { const s = new THREE.Shape(); s.moveTo(0, h); s.lineTo(w, 0); s.lineTo(0, -h); s.lineTo(-w, 0); s.closePath(); const m = new THREE.Mesh(new THREE.ShapeGeometry(s), new THREE.MeshBasicMaterial({ color: '#FFFBE0', transparent: true, depthWrite: false })); return m; };
  const a = mk(size * 0.12, size), b = mk(size, size * 0.12); g.add(a, b); g.rotation.z = PI / 4;
  g.userData.tick = t => { const u = ((t + ph) % every) / every; const q = u < 0.25 ? Math.sin(u / 0.25 * PI) : 0; g.scale.setScalar(0.05 + q); a.material.opacity = b.material.opacity = q; g.visible = q > 0.02; };
  return g;
}

export const SARDINE_PROPS = {
  // A small dome tent (pivot at the floor in its middle, door toward +Z): a plain-coloured dome, two dark crossed poles, a darker door, four guy ropes
  // to four fat pegs at the corners. o.color ('#F07A1E'), o.w (1.6), o.h (1.1). o.loose: the front-left corner has no peg (its flap beats, its rope
  // lies slack; o.looseUntil t: till then); o.ropes false: no ropes nor pegs (a flying tent: o.trail: the ropes hang down); o.bulge [[t, v]]: it swells like a balloon (and
  // wobbles); o.sag [[t, v]]: it slumps; o.lift [[t, y]]: it rises (o.tilt [[t, rad]]); o.lit: lit from inside (an unlit glowing dome: pair with
  // inDark); o.top false: the dome is cut away (seen from above: the floor and a low wall); o.flap [[t0, t1]]: the loose corner lifts
  saTent(o) {
    const W = o.w ?? 1.6, H = o.h ?? 1.1, C = new THREE.Color(o.color || '#F07A1E'), g = grp(), k = grp(); g.add(k);
    const dk = C.clone().multiplyScalar(0.55), dkHex = '#' + dk.getHexString();
    const domeMat = o.lit ? new THREE.MeshBasicMaterial({ color: C.clone().lerp(new THREE.Color('#FFF0C0'), 0.45) }) : mat('#' + C.getHexString());
    const dome = new THREE.Mesh(new THREE.SphereGeometry(1, 18, 9, 0, TAU, 0, PI / 2), domeMat); dome.scale.set(W / 2, H, W / 2); addOutline(dome, 0.01); dome.castShadow = true;
    const body = grp(dome); k.add(body);
    for (const s of [-1, 1]) { const p = new THREE.Mesh(new THREE.TorusGeometry(1, 0.012, 4, 20, PI), mat('#3A3D44')); p.scale.set(W / 2 * 1.01, H * 1.01, 1); p.rotation.y = s * PI / 4; body.add(p); }
    const ds = new THREE.Shape(); ds.absarc(0, 0, 1, 0, PI, false); ds.closePath(); const door = new THREE.Mesh(new THREE.ShapeGeometry(ds), o.lit ? new THREE.MeshBasicMaterial({ color: '#FFE7A0' }) : mat(dkHex)); door.scale.set(W * 0.2, H * 0.62, 1); door.position.set(0, 0.01, W / 2 * 0.995); body.add(door);
    const floor = at(cyl(W / 2, W / 2, 0.06, dkHex, 18, { outline: 0.01 }), 0, 0.03, 0); k.add(floor);   // (round 2) a real floor under the dome
    if (o.top === false) { body.visible = false; const wall = new THREE.Mesh(new THREE.CylinderGeometry(W / 2, W / 2, 0.22, 24, 1, true), mat('#' + C.getHexString(), { side: THREE.DoubleSide })); wall.position.y = 0.11; k.add(wall); floor.material = mat('#' + C.clone().lerp(new THREE.Color('#FFFFFF'), 0.35).getHexString()); }
    const corners = [0, 1, 2, 3].map(i => { const a = PI / 4 + i * PI / 2; return [Math.sin(a), Math.cos(a)]; });   // 0: front right, 1: back right, 2: back left, 3: front left
    const flaps = [], ropes = [], pegs = [];
    corners.forEach(([x, z], i) => {
      const f = grp(); f.position.set(x * W / 2 * 0.98, 0.02, z * W / 2 * 0.98); f.rotation.y = Math.atan2(x, z); const tri = new THREE.Shape(); tri.moveTo(-0.09, 0); tri.lineTo(0.09, 0); tri.lineTo(0, 0.16); tri.closePath();
      const fm = new THREE.Mesh(new THREE.ShapeGeometry(tri), mat(dkHex, { side: THREE.DoubleSide })); fm.rotation.x = -PI / 2 + 0.25; f.add(fm); k.add(f); flaps.push(f);
      if (o.ropes === false) return;
      const R = W / 2 * 1.55, px = x * R, pz = z * R, loose = o.loose && i === 3;
      const top = new THREE.Vector3(x * W / 2 * 0.62, H * 0.62, z * W / 2 * 0.62), end = new THREE.Vector3(px, 0.06, pz);
      const rope = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 1, 4), mat('#E8E2D0')); rope.userData = { top, end, loose, i }; k.add(rope); ropes.push(rope);
      if (!loose && o.pegs !== false) { const pg = grp(at(cyl(0.022, 0.022, 0.16, CHROME, 6, { outline: 0.02 }), 0, 0.02, 0), at(box(0.09, 0.02, 0.03, CHROME, { outline: 0.02 }), 0, 0.1, 0)); pg.position.set(px, 0, pz); k.add(pg); pegs.push(pg); }
    });
    if (o.ropes === false && o.trail) corners.forEach(([x, z], i) => { const r = at(cyl(0.008, 0.008, 0.9, '#E8E2D0', 4, { pivot: 'top' }), x * W / 2 * 0.95, 0.05, z * W / 2 * 0.95, 0.5 * z, 0, -0.5 * x); r.userData.sw = i; k.add(r); flaps.push(r); });   // (round 1) o.trail: four ropes trail down and back
    const tmp = new THREE.Vector3(), up = new THREE.Vector3(0, 1, 0);
    const setRope = (r, a, b) => { tmp.subVectors(b, a); const L = tmp.length(); r.position.copy(a).addScaledVector(tmp, 0.5); r.scale.set(1, L, 1); r.quaternion.setFromUnitVectors(up, tmp.normalize()); };
    g.userData.update = t => {
      const bl = kv(o.bulge, t), sg = kv(o.sag, t), wob = bl > 0.01 ? Math.sin(t * 11) * 0.06 * bl : 0;
      body.scale.set(1 + 0.3 * bl + wob, (1 + 0.12 * bl - wob) * (1 - 0.55 * sg), 1 + 0.3 * bl - wob);
      const ly = kv(o.lift, t), tl = kv(o.tilt, t); k.position.y = ly; k.rotation.z = tl + (o.ropes === false || ly > 0.05 ? 0.06 * Math.sin(t * 3.1) : 0); k.rotation.x = kv(o.tiltX, t) + ((o.ropes === false || ly > 0.05) ? 0.05 * Math.sin(t * 2.3 + 1) : 0); floor.scale.set(body.scale.x, 1, body.scale.z);   // o.tiltX [[t, rad]]: about X (+Z side up when negative)
      const fl = (o.flap || []).some(([a, b]) => t > a && t < b);
      flaps.forEach((f, i) => { if (f.userData.sw != null) { f.rotation.x = 0.5 + 0.15 * Math.sin(t * 6 + i); return; } f.rotation.x = o.loose && i === 3 && (o.looseUntil == null || t < o.looseUntil) ? 0.4 + 0.45 * Math.sin(t * 17) + (fl ? -0.6 : 0) : 0; });
      for (const r of ropes) { const { top, end, i: ri } = r.userData; const loose = o.loose && ri === 3 && (o.looseUntil == null || t < o.looseUntil); const e = loose ? tmp.set(top.x * 1.5, 0.03, top.z * 1.5).clone() : (ly > 0.05 ? new THREE.Vector3(end.x * 0.5, -ly + 0.05, end.z * 0.5) : (ri === 3 && o.ropeY != null ? new THREE.Vector3(end.x, o.ropeY, end.z) : end)); const tp = top.clone(); tp.x *= body.scale.x; tp.z *= body.scale.z; tp.y *= body.scale.y; setRope(r, tp, e); }
      for (const p of pegs) p.visible = ly < 0.05;
    };
    g.userData.update(0); return g;
  },
  // The stolen tent peg (pivot at its grip, a third from the hook; the shaft along +Z, the hook end at -Z): a fat chrome rod with a hooked top and a
  // glint every 1.3 s. o.len (0.42), o.glint false
  saPeg(o) {
    const L = o.len ?? 0.5, g = grp(); const sh = new THREE.Mesh(new THREE.CylinderGeometry(0.036, 0.024, L, 8), mat('#AEB8C4', { emissive: '#22262C' })); g.add(at(box(0.012, 0.012, L * 0.85, '#FFFFFF', { emissive: '#FFFFFF' }), 0.022, 0.024, L * 0.2)); sh.rotation.x = PI / 2; sh.position.z = L * 0.2; addOutline(sh, 0.03); g.add(sh);
    const tip = new THREE.Mesh(new THREE.ConeGeometry(0.018, 0.06, 8), mat(CHROME)); tip.rotation.x = PI / 2; tip.position.z = L * 0.7 + 0.03; g.add(tip);
    const hk = new THREE.Mesh(new THREE.TorusGeometry(0.055, 0.026, 6, 10, PI * 1.2), mat('#AEB8C4', { emissive: '#22262C' })); hk.rotation.y = PI / 2; hk.position.set(0, 0.04, -L * 0.3); addOutline(hk, 0.03); g.add(hk);
    const gl = glint(0.16, 1.1, o.ph ?? 0); gl.position.set(0.03, 0.05, L * 0.1); if (o.glint !== false) g.add(gl);
    g.userData.update = t => { gl.userData.tick(t); }; g.userData.update(0); return g;
  },
  // A wooden mallet (pivot at the grip's end, the head toward -Y)
  saMallet(o) { return grp(at(cyl(0.022, 0.026, 0.42, '#C49A62', 6, { outline: 0.02 }), 0, -0.21, 0), at(cyl(0.075, 0.075, 0.24, '#8A5A32', 10, { outline: 0.02 }), 0, -0.46, 0, 0, 0, PI / 2)); },
  // A flat silver sardine tin (pivot at its middle bottom, long side along X), no label: a rounded silver box, a lid that rolls back on its key from
  // o.openAt (0.4 s), the sardines' silver backs inside. o.s
  saTin(o) {
    const S = o.s ?? 1, g = grp(), k = grp(); g.add(k); k.scale.setScalar(S);
    k.add(at(box(0.26, 0.045, 0.15, '#C8CED6', { pivot: 'bottom', outline: 0.012, emissive: '#262A30' }), 0, 0, 0), at(box(0.24, 0.006, 0.13, '#8A7A4A'), 0, 0.044, 0));
    for (let i = 0; i < 3; i++) k.add(at(box(0.22, 0.012, 0.03, '#AEB8C4', { emissive: '#3A4250' }), 0, 0.046, -0.04 + 0.04 * i));
    const lid = at(box(0.26, 0.006, 0.15, '#DDE2E8', { pivot: 'bottom', outline: 0.01, emissive: '#2A2E34' }), 0, 0.045, 0), roll = at(cyl(0.012, 0.012, 0.15, '#DDE2E8', 8), 0.13, 0.055, 0, PI / 2, 0, 0);
    const key = grp(at(box(0.05, 0.004, 0.012, '#B8BEC6'), 0.025, 0, 0), new THREE.Mesh(new THREE.TorusGeometry(0.014, 0.004, 4, 8), mat('#B8BEC6'))); key.children[1].position.x = 0.055; key.children[1].rotation.x = PI / 2; key.position.set(0.13, 0.055, 0.08);
    k.add(lid, roll, key);
    g.userData.update = t => { const u = o.openAt == null ? 0 : smooth((t - o.openAt) / (o.openDur ?? 0.4)); lid.scale.x = 1 - 0.92 * u; roll.position.x = 0.13 - 0.24 * u; key.position.x = 0.13 - 0.24 * u; roll.scale.set(1 + 2 * u, 1, 1 + 2 * u); lid.position.x = -0.12 * u; };
    g.userData.update(0); return g;
  },
  // A big glistening sardine (pivot at its middle, head toward +Z): a blue-grey back, a silver belly, a forked tail, a round eye and a moving glint.
  // o.len (0.34); o.stretch [[t, v]]: pulled out like a worm (longer, thinner); o.squash [[t, v]]: squashed along its length (fatter); o.wiggle
  saSardine(o) {   // (round 3) a real fish silhouette: a slim silver body, a blue-green back, a dark gill line, a big eye, a forked tail fin and a dorsal fin standing up (+Y), an oily highlight
    const L = o.len ?? 0.34, g = grp(), k = grp(); g.add(k);
    const belly = new THREE.Mesh(new THREE.SphereGeometry(1, 16, 10), mat('#E2E8EE', { emissive: '#4A5664' })); belly.scale.set(L * 0.1, L * 0.16, L * 0.46); addOutline(belly, 0.025); k.add(belly);
    const back = new THREE.Mesh(new THREE.SphereGeometry(1, 16, 6, 0, TAU, 0, PI * 0.38), mat('#2E7A86', { emissive: '#0E2A30' })); back.scale.set(L * 0.103, L * 0.163, L * 0.465); k.add(back);
    for (const sx of [-1, 1]) { const gl = new THREE.Mesh(new THREE.TorusGeometry(L * 0.13, L * 0.008, 4, 10, PI * 0.8), mat('#5A6470')); gl.rotation.set(0, sx * PI / 2, PI * 0.6); gl.position.set(sx * L * 0.085, 0, L * 0.22); k.add(gl);
      k.add(at(sphere(L * 0.05, '#FFFFFF', 0), sx * L * 0.08, L * 0.035, L * 0.33), at(sphere(L * 0.028, '#14161A', 0), sx * L * 0.1, L * 0.035, L * 0.345)); }
    const tl = new THREE.Shape(); tl.moveTo(0, 0); tl.lineTo(-L * 0.2, L * 0.15); tl.lineTo(-L * 0.12, 0); tl.lineTo(-L * 0.2, -L * 0.15); tl.closePath();   // the forked tail, in the fish's vertical plane
    const tail = grp(); const tm = new THREE.Mesh(new THREE.ShapeGeometry(tl), mat('#3E8A96', { side: THREE.DoubleSide })); tm.rotation.y = PI / 2; addOutline(tm, 0.025); tail.add(tm); tail.position.z = -L * 0.42; k.add(tail);
    const df = new THREE.Shape(); df.moveTo(0, 0); df.lineTo(L * 0.12, 0); df.lineTo(0.0, L * 0.08); df.closePath(); const dm = new THREE.Mesh(new THREE.ShapeGeometry(df), mat('#2E7A86', { side: THREE.DoubleSide })); dm.rotation.y = -PI / 2; dm.position.set(0, L * 0.14, -L * 0.05); k.add(dm);
    const sh = at(box(0.006, L * 0.035, L * 0.55, '#FFFFFF', { emissive: '#FFFFFF' }), L * 0.095, L * 0.02, 0); k.add(sh);
    g.userData.update = t => { const s = kv(o.stretch, t), q = kv(o.squash, t); k.scale.set((1 - 0.35 * s) * (1 + 0.6 * q), (1 - 0.35 * s) * (1 + 0.6 * q), (1 + 1.4 * s) * (1 - 0.55 * q));
      const wg = o.wiggle || (o.wiggleAt && t > o.wiggleAt[0] && t < o.wiggleAt[1]); tail.rotation.y = wg ? 0.6 * Math.sin(t * 26) : 0.12 * Math.sin(t * 3); k.rotation.y = wg ? 0.12 * Math.sin(t * 26 + 1) : 0; sh.position.z = L * 0.12 * Math.sin(t * 3); };
    g.userData.update(0); return g;
  },
  // A patch of dark turned soil (pivot at the ground): o.r (0.45)
  saSoil(o) { const m = new THREE.Mesh(new THREE.CircleGeometry(o.r ?? 0.45, 20), mat('#4A3020')); m.rotation.x = -PI / 2; m.position.y = 0.03; m.material.polygonOffset = true; m.material.polygonOffsetFactor = -2; return grp(m); },
  // A clean fish skeleton lying on the ground (pivot at its middle, along X): a white spine, ribs, a skull and a tail fin. o.len (0.8)
  saBones(o) {
    const L = o.len ?? 0.8, g = grp(), W = '#F6F4EE';
    g.add(at(box(L * 0.75, 0.025, 0.025, W, { outline: 0.02 }), 0, 0.02, 0));
    for (let i = 0; i < 9; i++) { const x = -L * 0.3 + i * L * 0.07, h = L * 0.13 * (1 - Math.abs(i - 4) / 6); for (const s of [-1, 1]) g.add(at(box(0.016, 0.016, h, W, { outline: 0.015 }), x, 0.02, s * h / 2, 0, s * 0.35, 0)); }
    const sk = new THREE.Mesh(new THREE.ConeGeometry(L * 0.11, L * 0.22, 4), mat(W)); sk.rotation.z = -PI / 2; sk.scale.set(1, 1, 0.4); sk.position.set(L * 0.45, 0.04, 0); addOutline(sk, 0.02); g.add(sk);
    g.add(at(sphere(L * 0.025, '#2A2A2A', 0), L * 0.47, 0.06, L * 0.03));
    const tl = new THREE.Shape(); tl.moveTo(0, 0); tl.lineTo(-L * 0.14, L * 0.11); tl.lineTo(-L * 0.1, 0); tl.lineTo(-L * 0.14, -L * 0.11); tl.closePath(); const tm = new THREE.Mesh(new THREE.ShapeGeometry(tl), mat(W, { side: THREE.DoubleSide })); tm.rotation.x = -PI / 2; tm.position.set(-L * 0.37, 0.025, 0); addOutline(tm, 0.02); g.add(tm);
    return g;
  },
  // A hole in the ground (pivot at the ground): a dark disc in a ring of turned soil. o.r (0.12)
  saHole(o) { const R = o.r ?? 0.12, g = grp(); const d = new THREE.Mesh(new THREE.CircleGeometry(R, 18), mat('#1E140C')); d.rotation.x = -PI / 2; d.position.y = 0.09; const rg = new THREE.Mesh(new THREE.CylinderGeometry(R * 1.05, R * 1.9, 0.12, 18, 1, true), mat('#6A4A2C', { side: THREE.DoubleSide })); rg.position.y = 0.06; addOutline(rg, 0.01);
    const top = new THREE.Mesh(new THREE.RingGeometry(R, R * 1.15, 18), mat('#7A5A3A')); top.rotation.x = -PI / 2; top.position.y = 0.121; g.add(d, rg, top); return g; },   // (round 1) a raised collar of soil (a flat disc flickered against the grass)
  // A round white belly to put on the seagull (pivot at its middle). o.r (0.12)
  saBelly(o) { const m = new THREE.Mesh(new THREE.SphereGeometry(o.r ?? 0.12, 12, 8), mat('#F6F4EE')); m.scale.set(1, 0.9, 1.1); addOutline(m, 0.02); return grp(m); },
  // A caravan (pivot at the floor in its middle, length along X, door toward +Z): a cream body, a plain blue band, two windows, one wheel, a drawbar
  saCaravan(o) {
    const g = grp(); g.add(at(box(3.0, 1.8, 1.8, '#F2EEE2', { pivot: 'bottom', outline: 0.006 }), 0, 0.35, 0), at(box(3.02, 0.22, 1.82, '#3E6A9A'), 0, 0.7, 0), at(box(3.1, 0.1, 1.9, '#D8D2C2'), 0, 2.18, 0));
    for (const x of [-0.8, 0.8]) g.add(at(box(0.7, 0.45, 0.02, '#9CC4DE', { emissive: '#3A5A70' }), x, 1.55, 0.91));
    g.add(at(box(0.55, 1.2, 0.02, '#E2DCCC', { outline: 0.01 }), 0, 0.95, 0.91), at(cyl(0.34, 0.34, 0.2, '#1E2024', 12), 0.2, 0.34, 0.85, PI / 2, 0, 0), at(box(0.9, 0.06, 0.06, '#5E656D'), 1.9, 0.4, 0));
    return g;
  },
  // A giant tuna (pivot at its middle, head toward +X): a dark blue back, a silver belly, a forked tail, a yellow finlet row. o.len (1.1)
  saTuna(o) {
    const L = o.len ?? 1.1, g = grp(); const b = new THREE.Mesh(new THREE.SphereGeometry(1, 14, 8), mat('#C8D0D8')); b.scale.set(L * 0.5, L * 0.18, L * 0.15); addOutline(b, 0.012); g.add(b);
    const bk = new THREE.Mesh(new THREE.SphereGeometry(1, 14, 6, 0, TAU, 0, PI * 0.45), mat('#24406A')); bk.scale.set(L * 0.505, L * 0.185, L * 0.155); g.add(bk);
    const tl = new THREE.Shape(); tl.moveTo(0, 0); tl.lineTo(-L * 0.2, L * 0.2); tl.lineTo(-L * 0.12, 0); tl.lineTo(-L * 0.2, -L * 0.2); tl.closePath(); const tm = new THREE.Mesh(new THREE.ShapeGeometry(tl), mat('#24406A', { side: THREE.DoubleSide })); tm.position.x = -L * 0.46; addOutline(tm, 0.012); g.add(tm);
    for (let i = 0; i < 5; i++) g.add(at(box(0.03, 0.04, 0.02, '#E8C030'), -L * 0.1 - i * L * 0.06, L * 0.16, 0));
    g.add(at(sphere(L * 0.03, '#FFFFFF', 0), L * 0.38, L * 0.03, L * 0.12), at(sphere(L * 0.016, '#14161A', 0), L * 0.39, L * 0.03, L * 0.14));
    return g;
  },
  // A fishmonger's stall (pivot at the floor in its middle, front toward +Z): a counter topped with crushed ice blocks, wooden mallets laid out on it
  // like fish in rows, and one rolled-up tent lying across the ice. o.n mallets (8)
  saStall(o) {
    const g = grp(); g.add(at(box(2.4, 0.9, 0.9, '#E8E4DA', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(2.5, 0.08, 1.0, '#9AA0A6'), 0, 0.92, 0));
    for (let i = 0; i < 10; i++) g.add(at(box(0.24, 0.09, 0.4, i % 2 ? '#DDF0F6' : '#CFE8F2', { outline: 0.006 }), -1.08 + i * 0.24, 1.0, 0.05, 0, 0.05 * (hsh(i) - 0.5), 0));
    const n = o.n ?? 8; for (let i = 0; i < n; i++) { const m = grp(at(cyl(0.02, 0.022, 0.4, '#C49A62', 6, { outline: 0.015 }), 0, 0, 0.0, PI / 2, 0, 0), at(cyl(0.065, 0.065, 0.2, '#8A5A32', 10, { outline: 0.015 }), 0, 0, -0.28, 0, 0, PI / 2)); m.position.set(-0.95 + (i % 4) * 0.32 + (i > 3 ? 0.16 : 0), 1.1, i > 3 ? 0.25 : -0.12); m.rotation.y = 0.15; g.add(m); }
    g.add(at(cyl(0.13, 0.13, 0.9, '#F07A1E', 12, { outline: 0.01 }), 0.75, 1.15, 0.0, 0, 0, PI / 2)); for (const x of [0.5, 1.0]) g.add(at(cyl(0.135, 0.135, 0.04, '#3A3D44', 12), x, 1.15, 0.0, 0, 0, PI / 2));
    return g;
  },
  // A shop scale (pivot at its base): a box, a column, a blank white dial with a needle (no figure), a pan on top. o.weighAt: the pan dips, the needle
  // swings and settles
  saScale(o) {
    const g = grp(at(box(0.3, 0.12, 0.26, '#E8E4DA', { pivot: 'bottom', outline: 0.01 }), 0, 0, 0)), pan = grp(at(cyl(0.16, 0.13, 0.03, '#C8CED6', 14, { outline: 0.01 }), 0, 0, 0));
    g.add(at(box(0.12, 0.28, 0.12, '#E8E4DA', { pivot: 'bottom', outline: 0.01 }), 0, 0.12, -0.06)); const dial = new THREE.Mesh(new THREE.CircleGeometry(0.1, 20), mat('#FBFAF6')); dial.position.set(0, 0.3, 0.003); g.add(dial);
    g.add(at(cyl(0.105, 0.105, 0.012, '#5E656D', 20), 0, 0.3, -0.001, PI / 2, 0, 0)); const nd = grp(at(box(0.008, 0.08, 0.004, '#1E2E5A'), 0, 0.04, 0)); nd.position.set(0, 0.3, 0.01); g.add(nd);
    pan.position.set(0, 0.42, -0.06); g.add(pan, at(box(0.03, 0.02, 0.03, '#5E656D'), 0, 0.41, -0.06));
    g.userData.update = t => { const u = o.weighAt == null ? 0 : clamp01((t - o.weighAt) / 0.1); const q = o.weighAt == null || t < o.weighAt ? 0 : Math.exp(-4 * (t - o.weighAt)) * Math.cos((t - o.weighAt) * 18); nd.rotation.z = -(1.1 * u + 0.5 * q); pan.position.y = 0.42 - 0.03 * u - 0.015 * q; };
    g.userData.update(0); return g;
  },
  // A giant butterfly net (pivot at the grip, the pole up +Y): a long pole, a ring, a solid white cone with a grid texture (opaque) hanging back
  // toward -Z. o.s; o.tilt [[t, rad]]: the swing (about X)
  saNet(o) {
    const S = o.s ?? 1, g = grp(), k = grp(); g.add(k); k.scale.setScalar(S);
    k.add(at(cyl(0.025, 0.03, 2.2, '#A8845A', 6, { pivot: 'bottom', outline: 0.02 }), 0, 0, 0));
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.6, 0.025, 6, 24), mat('#8A9098')); ring.position.set(0, 2.8, 0); ring.rotation.x = PI / 2 * 0.9; k.add(ring);
    const tex = canvasPlane(1, 1, (c, W, H) => { c.fillStyle = '#F6F4EE'; c.fillRect(0, 0, W, H); c.strokeStyle = '#B8B4AA'; c.lineWidth = W * 0.012; for (let i = 0; i <= 12; i++) { c.beginPath(); c.moveTo(i * W / 12, 0); c.lineTo(i * W / 12, H); c.stroke(); c.beginPath(); c.moveTo(0, i * H / 12); c.lineTo(W, i * H / 12); c.stroke(); } }, { res: 256 });
    const cone = new THREE.Mesh(new THREE.ConeGeometry(0.6, 1.1, 20, 1, true), new THREE.MeshLambertMaterial({ map: tex.material.map, side: THREE.DoubleSide })); cone.rotation.x = -PI / 2 * 0.9; cone.position.set(0, 2.8 - 0.05, -0.55); addOutline(cone, 0.01); k.add(cone);
    g.userData.update = t => { k.rotation.x = kv(o.tilt, t); }; g.userData.update(0); return g;
  },
  // A fat orange ring the size of a forearm (pivot at its middle, in the XY plane): a bird ring for a tent pole, a darker seam
  saRing(o) { const g = grp(); const m = new THREE.Mesh(new THREE.TorusGeometry(o.r ?? 0.14, 0.05, 8, 18), mat('#F08A1E')); addOutline(m, 0.02); g.add(m, at(box(0.02, 0.11, 0.11, '#B85A10'), o.r ?? 0.14, 0, 0)); return g; },
  // A pair of big binoculars (pivot at the middle, looking along +Z)
  saBinoculars(o) { const g = grp(); for (const s of [-1, 1]) g.add(at(cyl(0.045, 0.05, 0.2, '#3A3D44', 10, { outline: 0.015 }), s * 0.055, 0, 0, PI / 2, 0, 0), at(cyl(0.05, 0.05, 0.01, '#9CC4DE', 10), s * 0.055, 0, 0.1, PI / 2, 0, 0)); g.add(at(box(0.07, 0.03, 0.06, '#2A2C30'), 0, 0, 0)); return g; },
  // A folding camp chair (pivot at the floor in its middle, facing +Z): a green seat and back on a grey frame
  saChair(o) {
    const g = grp(); g.add(at(box(0.5, 0.04, 0.45, '#3E7A4A', { outline: 0.01 }), 0, 0.42, 0), at(box(0.5, 0.45, 0.04, '#3E7A4A', { outline: 0.01 }), 0, 0.68, -0.22, -0.15, 0, 0));
    for (const s of [-1, 1]) g.add(at(box(0.025, 0.6, 0.025, '#8A9098'), s * 0.24, 0.3, 0, 0.5, 0, 0), at(box(0.025, 0.6, 0.025, '#8A9098'), s * 0.24, 0.3, 0, -0.5, 0, 0));
    return g;
  },
  // Flattened yellow rectangles of grass where tents stood (pivot at the ground): o.spots [[x, z, w, d, ry], ...]
  saFlats(o) { const g = grp(); for (const [x, z, w, d, ry] of o.spots || [[0, 0, 1.6, 1.6, 0]]) { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, d), mat('#D8C878')); m.rotation.set(-PI / 2, 0, ry || 0); m.position.set(x, 0.035, z); m.material.polygonOffset = true; m.material.polygonOffsetFactor = -2; g.add(m); } return g; },
  // Rain as light streaks (pivot at the middle of the ground): o.w, o.d, o.h, o.n; they fall at o.v (9 m/s) slanted
  saRain(o) {
    const W = o.w ?? 8, D = o.d ?? 6, Hh = o.h ?? 5, n = o.n ?? 160, g = grp(), ds = [], m = new THREE.MeshBasicMaterial({ color: '#CFE0FF', transparent: true, opacity: 0.45, depthWrite: false });
    for (let i = 0; i < n; i++) { const d = new THREE.Mesh(new THREE.BoxGeometry(0.01, 0.35, 0.01), m); d.rotation.z = 0.2; d.userData = { x: (hsh(i) - 0.5) * W, z: (hsh(i + 9) - 0.5) * D, p: hsh(i + 17) }; g.add(d); ds.push(d); }
    g.userData.update = t => { for (const d of ds) { const u = (d.userData.p + t * (o.v ?? 9) / Hh) % 1; d.position.set(d.userData.x - 0.2 * u * Hh * 0.2, Hh * (1 - u), d.userData.z); } }; g.userData.update(0); return g;
  },
  // A hillside / slope full of small plain dome tents seen from afar (pivot at the middle): o.n tents over o.w x o.d, on a ground that rises toward -Z
  // (o.rise); each tent a plain colour; o.glint: a glint at a corner of each (a fish tail)
  saTentField(o) {
    const n = o.n ?? 60, W = o.w ?? 16, D = o.d ?? 12, rise = o.rise ?? 0.35, g = grp(), gl = [], cols = ['#F07A1E', '#3E8ACC', '#E8C030', '#5EAA4A', '#E8913A', '#8A5AB0'];
    if (o.ground !== false) { const gm = new THREE.Mesh(new THREE.PlaneGeometry(W * 1.4, D * 1.4, 8, 8), mat(o.groundColor || '#7DBA5A')); gm.rotation.x = -PI / 2 + Math.atan(rise); gm.position.set(0, D * 0.0, 0); g.add(gm); }
    for (let i = 0; i < n; i++) { const x = (hsh(i) - 0.5) * W, z = (hsh(i + 33) - 0.5) * D, y = -z * rise; const c = new THREE.Color(cols[i % cols.length]);
      const d = new THREE.Mesh(new THREE.SphereGeometry(0.4, 10, 5, 0, TAU, 0, PI / 2), mat('#' + c.getHexString())); d.scale.set(1, o.domeH ?? 0.7, 1); d.position.set(x, y, z); addOutline(d, 0.02); g.add(d); for (const s of [-1, 1]) g.add(at(box(0.012, 0.012, 0.55, '#F4F1EA'), x + s * 0.42, y + 0.12, z + 0.25, -0.45, s * 0.6, 0));
      if (o.tails) { const tf = new THREE.Mesh(new THREE.ConeGeometry(0.07, 0.22, 4), mat('#D8E0E8', { emissive: '#606870' })); tf.position.set(x + 0.38, y + 0.11, z + 0.3); tf.rotation.z = PI; addOutline(tf, 0.02); g.add(tf); }
      if (o.glint) { const q = glint(0.16, 1.1, hsh(i + 5) * 1.1); q.position.set(x + 0.4, y + 0.2, z + 0.32); g.add(q); gl.push(q); } }
    g.userData.update = t => { for (const q of gl) q.userData.tick(t); }; g.userData.update(0); return g;
  },
  // A glint by itself (pivot at its middle): o.size (0.12), o.every (1.2)
  saGlint(o) { const g = grp(), q = glint(o.size ?? 0.12, o.every ?? 1.2, o.ph ?? 0); g.add(q); g.userData.update = t => q.userData.tick(t); g.userData.update(0); return g; },
  // A drop of drool hanging from a beak (pivot at its top): a thin string and a round drop that stretches down from o.at
  saDrool(o) { const g = grp(), s = at(cyl(0.004, 0.004, 1, '#DDEEFF', 5, { pivot: 'top' }), 0, 0, 0), d = at(sphere(0.018, '#DDEEFF', 0), 0, 0, 0); g.add(s, d); g.userData.update = t => { const u = o.at == null ? 1 : smooth((t - o.at) / 0.5); const L = 0.01 + (o.len ?? 0.12) * u + 0.015 * Math.sin(t * 5); s.scale.y = L; d.position.y = -L; g.visible = u > 0.01; }; g.userData.update(0); return g; },
  // A sandwich (pivot at its middle): two bread slices, a lettuce and ham layer
  saSandwich(o) { return grp(at(box(0.16, 0.025, 0.1, '#E8C88A', { outline: 0.01 }), 0, 0.03, 0), at(box(0.17, 0.012, 0.11, '#7AB84A'), 0, 0.012, 0), at(box(0.16, 0.012, 0.1, '#E89A9A'), 0, 0.0, 0), at(box(0.16, 0.025, 0.1, '#E8C88A', { outline: 0.01 }), 0, -0.02, 0)); },
  // A flash of lightning in the sky (pivot at its top): a bright zigzag, visible for 0.12 s at each time of o.at
  saBolt(o) {
    const g = grp(), m = new THREE.MeshBasicMaterial({ color: '#F4F8FF' }), pts = [[0, 0], [0.4, -1.2], [-0.2, -1.4], [0.5, -2.8], [-0.1, -3.0], [0.4, -4.2]];
    for (let i = 0; i < pts.length - 1; i++) { const [x0, y0] = pts[i], [x1, y1] = pts[i + 1], L = Math.hypot(x1 - x0, y1 - y0); const s = new THREE.Mesh(new THREE.BoxGeometry(0.08, L, 0.02), m); s.position.set((x0 + x1) / 2, (y0 + y1) / 2, 0); s.rotation.z = -Math.atan2(x1 - x0, y1 - y0); g.add(s); }
    g.userData.update = t => { g.visible = (o.at || []).some(a => t > a && t < a + 0.12); }; g.userData.update(0); return g;
  },
  // Plain shop shelves (pivot at the floor in the middle, front toward +Z): grey uprights, four shelves of blank coloured boxes, no word. o.w (2.4)
  saShelf(o) {
    const W = o.w ?? 2.4, g = grp(), cols = ['#E8C030', '#3E8ACC', '#E8913A', '#5EAA4A', '#F2EEE2', '#8A5AB0'];
    g.add(at(box(W, 2.0, 0.05, '#C8CCD2', { pivot: 'bottom', outline: 0.006 }), 0, 0, -0.25));
    for (const x of [-W / 2, W / 2]) g.add(at(box(0.05, 2.0, 0.5, '#9AA0A6', { pivot: 'bottom' }), x, 0, 0));
    for (let j = 0; j < 4; j++) { const y = 0.15 + j * 0.5; g.add(at(box(W, 0.03, 0.5, '#B8BEC6'), 0, y, 0)); if (o.empty) continue;
      for (let i = 0; i < Math.floor(W / 0.2); i++) g.add(at(box(0.16, 0.24 + 0.08 * hsh(i + j * 9), 0.3, cols[(i + j * 2) % cols.length], { pivot: 'bottom', outline: 0.01 }), -W / 2 + 0.12 + i * 0.2, y + 0.015, 0)); }
    return g;
  },
  // A striped fishmonger's apron in two colours (attach to the torso; pivot at its top middle; faces +Z): o.w (0.5), o.h (0.8)
  saApron(o) {
    const W = o.w ?? 0.5, H = o.h ?? 0.8, pl = canvasPlane(W, H, (c, w, h) => { const n = 9; for (let i = 0; i < n; i++) { c.fillStyle = i % 2 ? '#F4F1EA' : '#1E2E5A'; c.fillRect(i * w / n, 0, w / n + 1, h); } }, { res: 256 });
    pl.position.y = -H / 2; const g = grp(pl); return g;
  },
  // A cow bell (pivot at its strap's top): a brass cup on a brown strap
  saBell(o) { const g = grp(at(box(0.04, 0.12, 0.01, '#6A4A2C'), 0, -0.06, 0)); const b = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.06, 0.09, 8), mat('#D8A830')); b.position.y = -0.16; addOutline(b, 0.02); g.add(b); return g; },
  // A sleeping bag with a camper's round face in its hood (pivot at its top, hanging down -Y): o.color ('#3E6A9A')
  saBag(o) { const g = grp(); const b = new THREE.Mesh(new THREE.CapsuleGeometry(0.17, 0.75, 4, 10), mat(o.color || '#3E6A9A')); b.position.y = -0.55; addOutline(b, 0.015); g.add(b);
    g.add(at(sphere(0.11, '#E8B88A', 1), 0, -0.22, 0.12)); for (const s of [-1, 1]) g.add(at(sphere(0.015, '#14161A', 0), s * 0.035, -0.2, 0.225)); g.add(at(cyl(0.006, 0.006, 0.3, '#E8E2D0', 4, { pivot: 'bottom' }), 0, -0.05, 0)); return g; },
  // Arms and feet poking out of a tent door (pivot at the door's bottom middle, out toward +Z): two boots and two hands at odd angles that wriggle
  saLimbs(o) {
    const g = grp(), ls = []; const add_ = (col, w, h, d, x, y, rz) => { const q = grp(at(box(w, h, d, col, { outline: 0.01 }), 0, 0, d / 2)); q.position.set(x, y, 0); q.rotation.z = rz; g.add(q); ls.push(q); };
    add_('#3A3D44', 0.09, 0.08, 0.26, -0.16, 0.06, 0.1); add_('#8A5A32', 0.09, 0.08, 0.24, 0.14, 0.12, -0.3); add_('#E8B88A', 0.06, 0.03, 0.2, -0.05, 0.38, 0.6); add_('#E8B88A', 0.06, 0.03, 0.2, 0.08, 0.28, -0.8);
    g.userData.update = t => ls.forEach((q, i) => { q.rotation.x = 0.25 * Math.sin(t * (7 + i) + i); q.scale.z = 1 + 0.25 * Math.sin(t * 5 + i * 2); }); g.userData.update(0); return g;
  },
  // A sheet of white wrapping paper (pivot at its middle): o.wrapAt: flat, then folded into a bundle
  saPaper(o) { const g = grp(), m = at(box(0.5, 0.004, 0.4, '#F6F4EE', { outline: 0.01 }), 0, 0, 0); g.add(m); g.userData.update = t => { const u = o.wrapAt == null ? 0 : smooth((t - o.wrapAt) / 0.3); m.scale.set(1 - 0.6 * u, 1 + 30 * u, 1 - 0.5 * u); }; g.userData.update(0); return g; },
  // A spotlight beam (pivot at its top): a soft pale cone o.h (1.6) long, unlit, half transparent
  saBeam(o) { const H = o.h ?? 1.6, c = new THREE.Mesh(new THREE.ConeGeometry(o.r ?? 0.45, H, 20, 1, true), new THREE.MeshBasicMaterial({ color: '#FFF6D8', transparent: true, opacity: 0.18, depthWrite: false, side: THREE.DoubleSide })); c.position.y = -H / 2; return grp(c); },
  // A tent's floor seen from above with its top cut away (pivot at the floor in the middle): a rectangular floor o.w x o.d with a low wall rim
  // (o.color '#F07A1E')
  saTentCut(o) { const W = o.w ?? 2.6, D = o.d ?? 2.5, C = o.color || '#F07A1E', g = grp(); g.add(at(box(W, 0.03, D, '#F6C89A', { outline: 0.006 }), 0, 0.015, 0));
    for (const [w, d, x, z] of [[W + 0.12, 0.08, 0, -D / 2], [W + 0.12, 0.08, 0, D / 2], [0.08, D, -W / 2, 0], [0.08, D, W / 2, 0]]) g.add(at(box(w, 0.28, d, C, { pivot: 'bottom', outline: 0.008 }), x, 0, z)); return g; },
  // A sleeping-bag blanket over a lying body (pivot at its middle on the floor, its length along Z): o.w (0.42), o.l (1.25), o.color; a pale pillow
  // at the head end (+Z) unless o.pillow false
  saBlanket(o) { const W = o.w ?? 0.42, L = o.l ?? 1.25, g = grp(); const b = new THREE.Mesh(new THREE.CapsuleGeometry(W / 2, L - W, 4, 10), mat(o.color || '#3E6A9A')); b.rotation.x = PI / 2; b.scale.set(1.15, 1, 0.5); b.position.y = o.y ?? 0.36; addOutline(b, 0.012); g.add(b); return g; },
  // A wooden farm fence (pivot at the ground in the middle, along X): o.w (2.6) long, posts every 0.8 m, two rails
  saFence(o) { const W = o.w ?? 2.6, g = grp(); for (let x = -W / 2; x <= W / 2 + 1e-3; x += 0.8) g.add(at(box(0.08, 1.1, 0.08, '#8A6A45', { pivot: 'bottom', outline: 0.01 }), x, 0, 0)); for (const y of [0.45, 0.9]) g.add(at(box(W, 0.07, 0.04, '#A07A50', { outline: 0.01 }), 0, y, 0.05)); return g; },
  // A display dome over the tin (pivot at its rim on the cushion): a pale blue, mostly opaque glass bell with a white highlight band at mid-height and a
  // knob on top (never see-through over a body). o.r (0.22), o.h (0.4)
  saDome(o) { const R = o.r ?? 0.22, H = o.h ?? 0.4, g = grp(), gm = new THREE.MeshLambertMaterial({ color: '#D8ECF6', transparent: true, opacity: 0.55, depthWrite: false });
    const wall = new THREE.Mesh(new THREE.CylinderGeometry(R, R, H - R * 0.8, 20, 1, true), gm); wall.position.y = (H - R * 0.8) / 2; const cap = new THREE.Mesh(new THREE.SphereGeometry(R, 20, 8, 0, TAU, 0, PI / 2), gm); cap.position.y = H - R * 0.8; cap.scale.y = 0.8;
    const hl = new THREE.Mesh(new THREE.CylinderGeometry(R * 1.005, R * 1.005, 0.05, 20, 1, true, -0.6, 1.2), new THREE.MeshBasicMaterial({ color: '#FFFFFF' })); hl.position.y = (H - R * 0.8) * 0.55;
    const rim = new THREE.Mesh(new THREE.TorusGeometry(R, 0.01, 4, 24), mat('#B8C4CC')); rim.rotation.x = PI / 2; g.add(wall, cap, hl, rim, at(sphere(0.025, '#B8C4CC', 1), 0, H - R * 0.8 + R * 0.8, 0)); return g; },
  // A display plinth (pivot at the floor): a white-and-grey column o.h (0.95) high, o.w (0.45) square
  saPlinth(o) { const W = o.w ?? 0.45, H = o.h ?? 0.95; return grp(at(box(W, H, W, '#F2EEE4', { pivot: 'bottom', outline: 0.006 }), 0, 0, 0), at(box(W + 0.06, 0.05, W + 0.06, '#C8CCD2'), 0, H, 0), at(box(W + 0.06, 0.06, W + 0.06, '#C8CCD2'), 0, 0.03, 0)); },
};
