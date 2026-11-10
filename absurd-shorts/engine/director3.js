// Director v3 — scene-based timeline (script "version": 3), built for coherent short films.
//
// What it guarantees (each one fixes a class of bugs seen in v2 renders):
//   • TIME   : every action, cut and caption is placed on the REAL word timings of the voice
//              ("L12", "L12.end", "L12#3" = word 3, "L12:rouste" = first word matching, "+/-" offsets).
//   • MOTION : a move always faces its direction of travel (no backward walking) and the gait cadence
//              is derived from ground speed and leg length (no foot sliding / gliding).
//              When a move ends the actor returns to its previous clip (no walking on the spot).
//   • FACING : face/look can target another actor (dialogues are played TO someone, not to a wall).
//   • CAMERA : shots are framed from the actual bounding boxes of the subjects over the whole shot
//              (any size, seated, scaled gorilla…), with angles RELATIVE to the subject's facing, and an
//              occlusion pass that turns the camera around walls/other actors. Nothing framed = warning.
//   • PROPS  : attach to hands/joints at a time, hand over, drop with gravity, move along paths.
//   • AUDIO  : footsteps generated from the gait, key/scene SFX, lip flaps from the voice envelope.
import * as THREE from 'three';
import { createStage, setLighting, LIGHTING } from './scene.js';
import { createLook } from './look.js';
import { buildHuman } from './human.js';
import { CLIPS, samplePose, actingBlend, blendPoses } from './animations.js';
import { toonUpgrade, blendToon, addToon } from './toon.js';
import { fingersUpgrade } from './fingers.js';
import { clothUpgrade } from './cloth.js';
import { hasFaceRig, faceState, blendFace, cloneFace } from './facerig.js';
import { ease, clamp01, lerp, PALETTE as P } from './style.js';

const Props = await import('/engine/props.js');
const Sets = await import('/engine/sets.js');
const Creatures = await import('/engine/creatures.js');
const Models = await import('/engine/models.js');   // GLB models (glbModel props), loaded before the first frame

export const GRADE = 'contrast(0.86) saturate(0.78) brightness(1.07)';
const FPS = 30, D2R = Math.PI / 180, ZERO = [0, 0, 0];
const JOINTS = ['hips', 'torso', 'neck', 'head', 'shoulderL', 'elbowL', 'handL', 'shoulderR', 'elbowR', 'handR', 'hipL', 'kneeL', 'footL', 'hipR', 'kneeR', 'footR'];
// gait table: default ground speed (m/s) and stride per gait cycle in leg lengths
const LOCO = {
  walk: [1.35, 1.63], strut: [1.05, 1.9], sneak: [0.7, 1.3], tiptoe: [0.6, 1.8], run: [3.3, 2.6], flee: [3.6, 2.6], flail: [3.4, 2.6],
  knuckleWalk: [1.3, 1.4], boxSneak: [0.55, 0.9], pushCartWalk: [1.15, 1.5], pushCart: [1.1, 1.5], carryBox: [1.1, 1.5], crawl: [0.7, 1.0],
  walkEat: [1.0, 1.4], carryBags: [1.1, 1.5],
  walkRead: [1.35, 1.63], walkWrite: [1.2, 1.6], marchPomp: [1.15, 1.8],
};
const SIZE = { // fraction of subject height framed from the top, fill of frame height, default elevation, lens
  ecu: { part: 'head', pad: 1.25, fill: 0.8, elev: 0, lens: 34 }, cu: { part: 'headShoulders', fill: 0.82, elev: 2, lens: 36 },
  mcu: { part: 0.42, fill: 0.84, elev: 3, lens: 38 }, ms: { part: 0.6, fill: 0.86, elev: 4, lens: 40 }, mls: { part: 0.8, fill: 0.86, elev: 5, lens: 40 },
  fs: { part: 1, fill: 0.8, elev: 6, lens: 42 }, ws: { part: 1, fill: 0.42, elev: 10, lens: 45 }, ews: { part: 1, fill: 0.22, elev: 16, lens: 46 },
};

let S = null;
const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
const wrapA = a => { while (a > Math.PI) a -= 2 * Math.PI; while (a < -Math.PI) a += 2 * Math.PI; return a; };
const lerpA = (a, b, w) => a + wrapA(b - a) * w;
const warn = (msg) => { S.warnings.push(msg); };

// ------------------------------------------------------------------------------------- loading
export async function load(script, { width, height } = {}) {
  const W = width || 720, H = height || 1280;
  const stage = createStage(W, H);
  stage.renderer.domElement.style.display = 'none';
  const out = document.createElement('canvas'); out.width = W; out.height = H; document.body.appendChild(out);
  S = { script, W, H, stage, out, ctx: out.getContext('2d'), cast: {}, scene: -1, warnings: [], events: [], camTimes: [], lineById: {}, tempo: script.tempo || 1 }; // tempo > 1: snappier gestures, blends and turns
  if (script.look === 'shaders' || script.look === 'natural') S.look = createLook(stage, W, H, { ...(script.lookOpts || {}), natural: script.look === 'natural' });   // engine/look.js: Minecraft-shader-style light, or 'natural' (scene light probe, soft VSM shadows, Neutral tone mapping)
  await Models.preload(Models.srcsIn(script)); await Models.preloadImages(Models.allTextures());
  for (const [id, c] of Object.entries(script.cast || {})) S.cast[id] = buildActor(c, id);
  script.scenes.forEach((sc, si) => sc.lines.forEach(l => { S.lineById[l.id] = { ...l, si, rs: l.start - sc.start, re: l.end - sc.start }; }));
  S.total = script.scenes.reduce((m, sc) => Math.max(m, sc.start + sc.duration), 0);
  await document.fonts?.ready;
  return { duration: S.total, scenes: script.scenes.map(sc => ({ id: sc.id, start: sc.start, duration: sc.duration })) };
}

function buildActor(c, id) {
  let obj;
  if (c.type === 'creature') obj = Creatures.buildCreature(c.name, c.opts || {});
  else if (c.type === 'prop') obj = Props.buildProp(c.name, c.opts || {});
  else obj = buildHuman(c.preset ? c : { preset: 'lemec', ...c });
  obj.name = id; obj.userData.castId = id;
  if (obj.userData.kind === 'human' && (c.toon ?? (S.script?.rig === 'toon'))) { toonUpgrade(obj); obj.userData.toonCfg = typeof c.toon === 'object' ? c.toon : {}; }   // cartoon rig (engine/toon.js): opt-in, old stories never take this path
  if (obj.userData.kind === 'human' && obj.userData.setFaceState && (c.faceRig ?? c.toon ?? (S.script?.rig === 'toon' || !!S.script?.faceRig))) obj.userData.faceRig = true;   // animated face layers
  if (obj.userData.toon && (c.fingers ?? S.script?.fingers)) fingersUpgrade(obj);   // hands with fingers (engine/fingers.js): script `fingers: true` or per character
  if (obj.userData.toon && (c.cloth ?? S.script?.cloth)) clothUpgrade(obj);         // a tie in volume, a shock of hair (engine/cloth.js): script `cloth: true` or per character
  // measured rig facts (rest pose, unit scale): leg length + hip height drive gait cadence and pivots
  obj.position.set(0, 0, 0); obj.rotation.set(0, 0, 0); obj.scale.setScalar(1); obj.updateMatrixWorld(true);
  const J = obj.userData.joints || {};
  const wp = (o) => o ? o.getWorldPosition(V()) : null;
  const hip = wp(J.hipL || J.hips), foot = wp(J.footL), hips = wp(J.hips);
  obj.userData.legLen = hip && foot ? Math.max(0.15, hip.y - foot.y) : (obj.userData.height || 1) * 0.45;
  obj.userData.hipY = hips ? hips.y : (obj.userData.height || 1) * 0.5;
  if (obj.userData.mover && J.hips) obj.userData.hipYMover = obj.userData.mover.worldToLocal(wp(J.hips)).y;
  return obj;
}

// ------------------------------------------------------------------------------------- time expressions
const normW = w => String(w).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9']/g, '');
function T(expr, sc) {
  if (expr == null) return 0;
  if (typeof expr === 'number') return expr;
  const s = String(expr).replace(/\s+/g, '');
  if (s === 'start') return 0;
  if (s === 'end') return sc.duration;
  const m = s.match(/^([A-Za-z]\w*?)(?:#(\d+)|:([^.+\-]+))?(\.end|\.mid)?([+-][\d.]+)?$/);
  if (!m) { warn(`bad time "${expr}"`); return 0; }
  const L = S.lineById[m[1]];
  if (!L) { warn(`unknown line "${m[1]}" in "${expr}"`); return 0; }
  let a = L.rs, b = L.re;
  const words = L.words || [];
  if (m[2] != null || m[3] != null) {
    const w = m[2] != null ? words[+m[2]] : words.find(x => normW(x.w).includes(normW(m[3])));
    if (!w) warn(`word not found in "${expr}" (${L.text})`); else { a = w.s - sc.start; b = w.e - sc.start; }
  }
  let t = m[4] === '.end' ? b : m[4] === '.mid' ? (a + b) / 2 : a;
  if (m[5]) t += parseFloat(m[5]);
  return t;
}

// ------------------------------------------------------------------------------------- scene setup
function setupScene(si, analyzing = false) {
  const sc = S.script.scenes[si];
  const { scene } = S.stage;
  if (S.root) scene.remove(S.root);
  for (const a of Object.values(S.cast)) {
    a.parent?.remove(a);
    const leak = []; a.traverse(n => { if (n !== a && (n.userData.isSceneProp || n.userData.isAttachment)) leak.push(n); });
    leak.forEach(n => n.parent?.remove(n));
  }
  S.root = new THREE.Group(); scene.add(S.root);
  let set;
  try { set = Sets.buildSet(sc.set || 'whiteVoid', sc.setOpts || {}); } catch (e) { warn(`set ${sc.set} failed: ${e.message}`); set = Sets.buildSet('whiteVoid', {}); }
  S.root.add(set); S.set = set; S.staticBoxes = null;
  S.lights = setLighting(scene, sc.lighting || set.userData.lighting || 'day');
  atmosphere(sc, set);
  if (S.look) S.look.setupLights(S.lights, set, sc);
  S.lightBase = { hemi: S.lights.hemi.intensity, key: S.lights.key.intensity, bg: scene.background.clone() };
  S.skyDome = null; set.traverse(o => { if (!S.skyDome && o.isMesh && o.renderOrder === -10 && o.material?.side === THREE.BackSide) S.skyDome = o; });   // exterior sets: tint the dome at night
  const anchors = set.userData.anchors || {};
  const place = (c) => {
    if (typeof c === 'string') { const a = anchors[c]; if (!a) warn(`[${sc.id}] unknown anchor ${c}`); return a ? [...a] : [0, 0, 0]; }
    if (c && !Array.isArray(c) && c.anchor) { const a = anchors[c.anchor] || [0, 0, 0], o = c.offset || ZERO; return [a[0] + o[0], a[1] + o[1], a[2] + o[2]]; }
    return c ? [...c] : [0, 0, 0];
  };
  S.place = place;
  // freeze window: [at, until) — until omitted = frozen for the rest of the scene. Keys of frozen actors / props are
  // written in scene time and remapped so they still fire at that scene time once time restarts.
  S.freezeAt = null; S.freezeUntil = Infinity; S.freezeExcept = new Set(sc.freeze?.except || []);
  // the S.lineById times are scene-relative already, so T() works here
  if (sc.freeze) { S.freezeAt = T(sc.freeze.at ?? 0, sc); S.freezeUntil = sc.freeze.until != null ? T(sc.freeze.until, sc) : Infinity; }
  // actors
  S.actors = (sc.actors || []).map(cfg => {
    const obj = S.cast[cfg.id] || (S.cast[cfg.id] = buildActor(cfg.spec || { preset: 'lemec' }, cfg.id));
    S.root.add(obj);
    for (const at of cfg.attach || []) attachStatic(obj, at);
    return prepActor(cfg, obj, sc, place);
  });
  S.actorById = Object.fromEntries(S.actors.map(a => [a.id, a]));
  // props
  // prop options ending in "At" (openAt, writeAt, closeAt, ...) accept scene time expressions ('M2:nom+0.2') or lists of them
  const optT = v => typeof v === 'string' ? T(v, sc) : Array.isArray(v) ? v.map(optT) : v;
  const resolveOpts = o => Object.fromEntries(Object.entries(o || {}).map(([k, v]) => [k, /At$/.test(k) ? optT(v) : v]));
  S.props = (sc.props || []).map(cfg => {
    const obj = Props.buildProp(cfg.name, resolveOpts(cfg.opts)); obj.name = 'prop:' + (cfg.id || cfg.name); obj.userData.isSceneProp = true;
    S.root.add(obj);
    const Pp = prepProp(cfg, obj, sc, place);
    if (cfg.alt) { // one alternate look, or a list of them in time order (e.g. watch -> broken -> taped)
      Pp.alts = [].concat(cfg.alt).map(a => { const o = Props.buildProp(a.name || cfg.name, resolveOpts(a.opts)); o.userData.isSceneProp = true; S.root.add(o); return { obj: o, at: T(a.at, sc), rot: a.rot || null }; }).sort((x, y) => x.at - y.at);
      Pp.alt = Pp.alts[0].obj; Pp.altAt = Pp.alts[0].at; Pp.altRot = Pp.alts[0].rot;
    }
    return Pp;
  });
  S.propById = Object.fromEntries(S.props.map(p => [p.id, p]));
  // tethers: a sagging cord rebuilt every frame between two moving anchors ({actor, hand|joint, offset} or {prop, offset}), e.g. a leash
  S.tethers = (sc.tethers || []).map(td => { const m = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshLambertMaterial({ color: td.color || '#C0392B' })); m.castShadow = true; m.frustumCulled = false; S.root.add(m); return { td, m }; });
  // crowds (background extras, deterministic)
  for (const cr of sc.crowd || []) for (let i = 0; i < (cr.count || 4); i++) {
    const id = `${cr.id || 'crowd'}${i}`, pos = cr.positions?.[i] || [cr.center[0] + ((i * 1.37) % 1 - 0.5) * (cr.spread || 3), 0, cr.center[2] + ((i * 0.61) % 1 - 0.5) * (cr.spread || 3)];
    const obj = buildActor(cr.spec || { preset: 'cop' }, id); S.root.add(obj);
    const a = prepActor({ id, pos, ry: cr.ry ?? 0, clip: cr.clip || 'idle', phase: i * 0.37, expr: cr.expr, keys: cr.keys }, obj, sc, place);
    S.actors.push(a); S.actorById[id] = a;
  }
  S.lines = sc.lines.map(l => ({ ...l, rs: l.start - sc.start, re: l.end - sc.start, chunks: chunk(l, sc) }));
  S.sc = sc; S.scene = si;
  precomputeReleases(sc);
  S.cams = (sc.cams || []).map((c, i) => ({ ...c, t0: T(c.at ?? 0, sc), i }));
  S.cams.sort((a, b) => a.t0 - b.t0);
  S.cams.forEach((c, i) => { c.t1 = i + 1 < S.cams.length ? S.cams[i + 1].t0 : sc.duration; });
  S.cams.forEach(c => { c.sol = solveCam(c, sc); });
  if (analyzing) collectEvents(sc);
}

// Per-scene atmosphere (scene keys override the set's userData): light tweaks {hemi, sky, ground, keyI, key, dir, bg}, linear fog
// {color, near, far}, camera clip planes near/far (aerial shots see kilometres), a shadow box {size, center} for wide exteriors,
// and objects flagged userData.followCam (a sky dome that stays centred on the camera, so the horizon is always at eye level).
function atmosphere(sc, set) {
  const { scene, camera } = S.stage, U = set.userData, L = S.lights;
  const l = { ...(U.light || {}), ...(sc.light || {}) };
  if (l.hemi != null) L.hemi.intensity = l.hemi; if (l.sky) L.hemi.color.set(l.sky); if (l.ground) L.hemi.groundColor.set(l.ground);
  if (l.keyI != null) L.key.intensity = l.keyI; if (l.key) L.key.color.set(l.key); if (l.dir) L.key.position.set(...l.dir); if (l.bg) scene.background = new THREE.Color(l.bg);
  const fog = sc.fog ?? U.fog; scene.fog = fog ? new THREE.Fog(fog.color, fog.near, fog.far) : null;
  camera.near = sc.near ?? U.near ?? 0.05; camera.far = sc.far ?? U.far ?? 400; camera.updateProjectionMatrix();
  const sh = sc.shadow ?? U.shadow;
  if (sh) {
    const c = V(...(sh.center || [0, 0, 0])), d = L.key.position.clone().normalize(), size = sh.size || 40, cam = L.key.shadow.camera;
    L.key.target.position.copy(c); L.key.position.copy(c).add(d.multiplyScalar(size * 2));
    cam.left = cam.bottom = -size; cam.right = cam.top = size; cam.near = 1; cam.far = size * 4.5; cam.updateProjectionMatrix();
    L.key.shadow.bias = sh.bias ?? -0.0008;
  }
  S.follow = []; set.traverse(o => { if (o.userData.followCam) S.follow.push(o); });
}

function attachStatic(obj, spec) {
  const J = obj.userData.joints || {}; const j = J[spec.joint || 'head'] || obj;
  const p = Props.buildProp(spec.name, spec.opts || {});
  p.position.set(...(spec.pos || ZERO)); if (spec.rot) p.rotation.set(...spec.rot); if (spec.scale) p.scale.setScalar(spec.scale);
  p.userData.isAttachment = true; j.add(p);
}

// ------------------------------------------------------------------------------------- actor tracks
function frozenRemap(id, t) { // scene time -> the actor's own clock (frozen actors skip the frozen window)
  if (S.freezeAt == null || S.freezeExcept.has(id) || !isFinite(S.freezeUntil)) return t;
  const a = S.freezeAt, u = S.freezeUntil; return t < a ? t : t < u ? a : t - (u - a);
}
function prepActor(cfg, obj, sc, place) {
  const A = { id: cfg.id, cfg, obj, kind: obj.userData.kind, pos0: place(cfg.anchor ? { anchor: cfg.anchor, offset: cfg.offset } : cfg.pos), scale0: cfg.scale ?? 1,
    ry0: typeof cfg.ry === 'number' ? cfg.ry * D2R : 0, face0: cfg.face ?? null, phase: cfg.phase || 0, speed: cfg.speed ?? 1,
    moves: [], clipKeys: [], faceKeys: [], lookKeys: [], exprKeys: [], scaleKeys: [], visKeys: [], sfx: [], fxKeys: [{ at: -1e6, fx: cfg.fx || {} }] };
  A.clipKeys.push({ at: -1e6, clip: cfg.clip || 'idle', params: cfg.params || {}, speed: cfg.speed ?? 1 });
  A.exprKeys.push({ at: -1e6, expr: cfg.expr || 'neutral' });
  A.scaleKeys.push({ at: -1e6, scale: A.scale0, dur: 0 });
  A.visKeys.push({ at: -1e6, visible: cfg.visible !== false });
  if (cfg.look) A.lookKeys.push({ at: -1e6, look: cfg.look });
  const keys = (cfg.keys || []).map(k => ({ ...k, t: frozenRemap(cfg.id || cfg.name, T(k.at ?? 0, sc)) })).sort((a, b) => a.t - b.t);
  for (const k of keys) {
    if (k.to != null || k.path) A.moves.push(k);
    else {
      if (k.clip) A.clipKeys.push({ at: k.t, clip: k.clip, params: k.params || {}, speed: k.speed ?? A.speed, key: k });
      if (k.face != null) A.faceKeys.push({ at: k.t, face: k.face, turn: k.turn ?? 0.22 / S.tempo });
    }
    if (k.look !== undefined) A.lookKeys.push({ at: k.t, look: k.look });
    if (k.expr) A.exprKeys.push({ at: k.t, expr: k.expr });
    if (k.fx) A.fxKeys.push({ at: k.t, fx: { ...k.fx } });   // face FX: {wet, tears, sweat, blush, shiver}
    if (k.toon) (A.toonKeys = A.toonKeys || [{ at: -1e6, toon: {}, dur: 0 }]).push({ at: k.t, toon: k.toon, dur: k.toonDur ?? 0.12, ease: k.toonEase || 'out' });   // cartoon channels keyed from the story (added to the clip's): {sq, scl, bend, face, ears, hat}; {} clears
    if (k.scale != null && k.to == null) A.scaleKeys.push({ at: k.t, scale: k.scale, dur: k.dur ?? 0.6, ease: k.ease || 'inOut' });
    if (k.visible != null) A.visKeys.push({ at: k.t, visible: k.visible });
    if (k.sfx) A.sfx.push({ t: k.t + (k.sfxAt || 0), name: k.sfx, vol: k.vol ?? 0.6 });
  }
  // resolve moves sequentially (each starts where the actor is at that time)
  const legLen = obj.userData.legLen;
  for (const mv of A.moves) {
    const start = posAt(A, mv.t);
    const pts = [start.toArray(), ...(mv.path ? mv.path.map(p => place(p)) : [place(mv.to)])].map(p => V(p[0], p[1] ?? start.y, p[2]));
    if (mv.path == null && mv.to && Array.isArray(mv.to) && mv.to[1] == null) pts[1].y = start.y;
    const segs = []; let L = 0;
    for (let i = 1; i < pts.length; i++) { const d = pts[i].clone().sub(pts[i - 1]); const l = Math.hypot(d.x, d.z) || d.length(); segs.push({ a: pts[i - 1], b: pts[i], l, L0: L, head: Math.atan2(d.x, d.z) }); L += l; }
    const clip = mv.clip ?? (mv.glide ? null : 'walk');
    const loco = LOCO[clip];
    const spd = mv.speed ?? (loco ? loco[0] : 1.5);
    const dur = mv.until != null ? Math.max(0.2, frozenRemap(cfg.id, T(mv.until, sc)) - mv.t) : mv.dur ?? Math.max(0.2, L / spd);
    Object.assign(mv, { pts, segs, L, clip, dur, t1: mv.t + dur, end: pts[pts.length - 1] });
    if (loco) { const sc_ = scaleAt(A, mv.t); mv.freq = mv.cadence ?? clamp((L / dur) / (loco[1] * legLen * sc_), 0.6, 4.2); }   // mv.cadence: gait cycles per second set by the story (small quick steps on the air)
    if (clip) {
      A.clipKeys.push({ at: mv.t, clip, params: { ...(mv.params || {}), freq: mv.freq }, speed: 1, move: mv });
      A.clipKeys.push({ at: mv.t1, clip: mv.then ?? '__prev__', params: mv.thenParams || (mv.then === clip ? { ...(mv.params || {}), freq: mv.freq } : {}), speed: mv.then === clip ? 1 : A.speed, afterMove: mv, t0: mv.then === clip ? mv.t : undefined });   // then = the move's own clip: its time continues (a one-shot clip must not replay)
    }
    if (mv.sfx) A.sfx.push({ t: mv.t, name: mv.sfx, vol: mv.vol ?? 0.6 });
    if (mv.land) A.sfx.push({ t: mv.t1, name: mv.land, vol: mv.vol ?? 0.6 });
  }
  A.clipKeys.sort((a, b) => a.at - b.at);
  for (let i = 0; i < A.clipKeys.length; i++) if (A.clipKeys[i].clip === '__prev__') {
    let j = i - 1; while (j >= 0 && (A.clipKeys[j].move || A.clipKeys[j].clip === '__prev__')) j--;
    const src = j >= 0 ? A.clipKeys[j] : { clip: 'idle', params: {} };
    A.clipKeys[i].clip = LOCO[src.clip] ? 'idle' : src.clip; A.clipKeys[i].params = src.params;
  }
  // lint: walking on the spot / gliding
  A.clipKeys.forEach((k, i) => {
    if (LOCO[k.clip] && !k.move) warn(`[${sc.id}] ${A.id}: gait "${k.clip}" at ${k.at.toFixed(2)}s without a move (walking on the spot)`);
    if (k.at < -1e5 && ONE_SHOT.has(k.clip)) warn(`[${sc.id}] ${A.id}: one-shot clip "${k.clip}" as the base clip: it is over before the shot starts; key it (k(0.0, clip=...))`);
  });
  for (const mv of A.moves) if (!mv.clip && !mv.glide && A.kind !== 'prop') warn(`[${sc.id}] ${A.id}: move at ${mv.t.toFixed(2)}s without gait (gliding)`);
  return A;
}
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));

function posAt(A, t) {
  let p = V(...A.pos0);
  for (const mv of A.moves) {
    if (!mv.segs) break;            // not resolved yet (during prep)
    if (t < mv.t) break;
    if (t >= mv.t1) { p = mv.end.clone(); continue; }
    let k = clamp01((t - mv.t) / mv.dur); k = (ease[mv.ease || 'linear'] || ease.linear)(k);
    p = alongPath(mv, k * mv.L);
    if (mv.arc) p.y += mv.arc * 4 * k * (1 - k);
  }
  return p;
}
function alongPath(mv, d) {
  for (const s of mv.segs) if (d <= s.L0 + s.l || s === mv.segs[mv.segs.length - 1]) { const w = s.l ? clamp01((d - s.L0) / s.l) : 1; return s.a.clone().lerp(s.b, w); }
  return mv.end.clone();
}
function headingAt(mv, t) {
  const d = clamp01((t - mv.t) / mv.dur) * mv.L;
  for (const s of mv.segs) if (d <= s.L0 + s.l) return s.head;
  return mv.segs[mv.segs.length - 1].head;
}
function faceTarget(A, f, t) {
  if (typeof f === 'number') return f * D2R;
  const me = posAt(A, t);
  let p = null;
  if (Array.isArray(f)) p = V(f[0], 0, f.length > 2 ? f[2] : f[1]);
  else if (S.actorById[f]) p = posAt(S.actorById[f], t);
  else if (S.propById[f]) p = propBasePos(S.propById[f], t);
  else return null;
  const dx = p.x - me.x, dz = p.z - me.z;
  return Math.hypot(dx, dz) < 1e-3 ? null : Math.atan2(dx, dz);
}
function facingAt(A, t, depth = 0) {
  if (depth > 40) return A.ry0;
  // latest source starting at or before t: move or face key
  let src = null;
  for (const mv of A.moves) if (mv.t <= t && (mv.face ?? 'move') !== 'keep' && (!src || mv.t >= src.t)) src = { t: mv.t, mv };
  for (const fk of A.faceKeys) if (fk.at <= t && (!src || fk.at >= src.t)) src = { t: fk.at, fk };
  if (!src) { const f0 = A.face0 != null ? faceTarget(A, A.face0, t) : null; return f0 ?? A.ry0; }
  const from = facingAt(A, src.t - 1e-4, depth + 1);
  if (src.mv) {
    const mv = src.mv, mode = mv.face ?? 'move';
    let target;
    if (t <= mv.t1) target = mode === 'move' ? (mv.back ? headingAt(mv, t) + Math.PI : headingAt(mv, t)) : (faceTarget(A, mode, t) ?? from);
    else {
      const endHead = mode === 'move' ? (mv.back ? headingAt(mv, mv.t1) + Math.PI : headingAt(mv, mv.t1)) : (faceTarget(A, mode, mv.t1) ?? from);
      if (mv.faceEnd == null) return endHead;
      const fe = faceTarget(A, mv.faceEnd, t) ?? endHead;
      return lerpA(endHead, fe, ease.out(clamp01((t - mv.t1) / (mv.turnEnd ?? 0.25 / S.tempo))));
    }
    return lerpA(from, target, ease.out(clamp01((t - mv.t) / (mv.turn ?? 0.16 / S.tempo))));
  }
  const target = faceTarget(A, src.fk.face, t) ?? from;
  return lerpA(from, target, ease.out(clamp01((t - src.fk.at) / src.fk.turn)));
}
function lastKey(list, t) { let k = list[0]; for (const x of list) { if (x.at <= t) k = x; else break; } return k; }
function prevKey(list, cur) { const i = list.indexOf(cur); return i > 0 ? list[i - 1] : null; }
function scaleAt(A, t) {
  let s = A.scale0;
  for (const k of A.scaleKeys) { if (k.at > t) break; s = k.dur ? lerp(s, k.scale, (ease[k.ease] || ease.inOut)(clamp01((t - k.at) / k.dur))) : k.scale; }
  return s;
}

// ------------------------------------------------------------------------------------- props
function prepProp(cfg, obj, sc, place) {
  const Pp = { id: cfg.id || cfg.name, cfg, obj, kind: 'prop', pos0: place(cfg.anchor ? { anchor: cfg.anchor, offset: cfg.offset } : cfg.pos), ry0: (cfg.ry || 0) * D2R, rx0: cfg.rot?.[0] || 0, rz0: cfg.rot?.[2] || 0,
    scale0: cfg.scale ?? 1, moves: [], own: [], visKeys: [{ at: -1e6, visible: cfg.visible !== false }], scaleKeys: [{ at: -1e6, scale: cfg.scale ?? 1, dur: 0 }], spin: cfg.spin || null, sfx: [], rotKeys: [], sqKeys: [] };
  if (cfg.rotOrder) obj.rotation.order = cfg.rotOrder;   // 'YXZ': rot[0] pitches the prop in the vertical plane it faces after ry (a stamp swung over by somebody who does not face down an axis)
  if (cfg.on) Pp.own.push({ at: -1e6, attach: cfg.on.actor || cfg.on, ...(typeof cfg.on === 'object' ? cfg.on : {}) });
  const keys = (cfg.keys || []).map(k => ({ ...k, t: frozenRemap(cfg.id || cfg.name, T(k.at ?? 0, sc)) })).sort((a, b) => a.t - b.t);
  for (const k of keys) {
    if (k.attach) Pp.own.push({ ...k, at: k.t });
    if (k.detach) Pp.own.push({ ...k, at: k.t });
    if (k.to != null || k.path) Pp.moves.push(k);
    if (k.visible != null) Pp.visKeys.push({ at: k.t, visible: k.visible });
    if (k.scale != null && k.to == null) Pp.scaleKeys.push({ at: k.t, scale: k.scale, dur: k.dur ?? 0.4, ease: k.ease || 'inOut' });
    if (k.sfx) Pp.sfx.push({ t: k.t, name: k.sfx, vol: k.vol ?? 0.6 });
    if (k.rotTo) Pp.rotKeys.push({ t: k.t, rot: k.rotTo, dur: k.dur ?? 0.4, ease: k.ease || 'inOut' });   // radians [x, y, z], Euler XYZ
    if (k.squash) Pp.sqKeys.push({ t: k.t, sq: k.squash, dur: k.dur ?? 0.3 });   // an impact: the prop is squashed to [sx, sy, sz] times its size at that instant and springs back over dur (a damped wobble)
  }
  for (const mv of Pp.moves) {
    const start = propBasePos(Pp, mv.t);
    const pts = [start.toArray(), ...(mv.path ? mv.path.map(p => place(p)) : [place(mv.to)])].map(p => V(p[0], p[1] ?? start.y, p[2]));
    const segs = []; let L = 0;
    for (let i = 1; i < pts.length; i++) { const d = pts[i].clone().sub(pts[i - 1]); const l = d.length(); segs.push({ a: pts[i - 1], b: pts[i], l, L0: L, head: Math.atan2(d.x, d.z) }); L += l; }
    Object.assign(mv, { pts, segs, L, dur: mv.dur ?? Math.max(0.2, L / (mv.speed ?? 1.2)), end: pts[pts.length - 1] }); mv.t1 = mv.t + mv.dur;
  }
  return Pp;
}
function propBasePos(Pp, t) {
  let p = V(...Pp.pos0);
  for (const mv of Pp.moves) {
    if (!mv.segs || t < mv.t) break;
    if (t >= mv.t1) { p = mv.end.clone(); continue; }
    let k = clamp01((t - mv.t) / mv.dur); k = (ease[mv.ease || 'inOut'] || ease.inOut)(k);
    p = alongPath(mv, k * mv.L); if (mv.arc) p.y += mv.arc * 4 * k * (1 - k);
  }
  return p;
}
function propOwnerAt(Pp, t) { let o = null; for (const k of Pp.own) { if (k.at <= t) o = k; else break; } return o; }
function jointFor(actorObj, k) {
  const J = actorObj.userData.joints || {};
  const name = k.joint || (k.hand === 'L' ? 'handL' : k.hand === 'R' || k.hand == null ? 'handR' : k.hand);
  return J[name] || actorObj;
}
function placeAttached(Pp, k, t) {
  const A = S.actorById[k.attach] || (S.propById[k.attach] ? { obj: S.propById[k.attach].obj, isProp: true } : null); if (!A) return false;
  const j = A.isProp ? A.obj : jointFor(A.obj, k);
  if (Pp.obj.parent !== j) j.add(Pp.obj);
  const g = Pp.obj.userData.grip || ZERO, isHand = !k.joint && !A.isProp;
  const off = k.offset || (isHand ? [-g[0], -0.1 - g[1], -g[2]] : ZERO);
  Pp.obj.position.set(off[0], off[1], off[2]);
  Pp.obj.rotation.set(...(k.rot || ZERO));
  const sc = (k.scale ?? scaleOf(Pp, t)) / Math.max(0.01, (A.obj.scale.x || 1));
  Pp.obj.scale.setScalar(sc); squashProp(Pp, t);
  return true;
}
// a keyed impact on a prop (key `squash`): squashed at the key, it springs back, overshooting a little
function squashProp(Pp, t) { let q = null; for (const k of Pp.sqKeys) { if (k.t > t) break; q = k; } if (!q) return; const u = (t - q.t) / q.dur; if (u >= 1) return;
  const a = Math.exp(-4.5 * u) * Math.cos(u * 11) * (1 - u), sc = Pp.obj.scale; sc.set(sc.x * (1 + (q.sq[0] - 1) * a), sc.y * (1 + (q.sq[1] - 1) * a), sc.z * (1 + (q.sq[2] - 1) * a)); }
function scaleOf(Pp, t) { let s = Pp.scale0; for (const k of Pp.scaleKeys) { if (k.at > t) break; s = k.dur ? lerp(s, k.scale, (ease[k.ease] || ease.inOut)(clamp01((t - k.at) / k.dur))) : k.scale; } return s; }

function precomputeReleases(sc) {
  for (const Pp of S.props) for (const k of Pp.own) if (k.detach && k.at > -1e5) {
    const prev = Pp.own[Pp.own.indexOf(k) - 1];
    if (!prev || !prev.attach) { k.rel = { pos: propBasePos(Pp, k.at), quat: new THREE.Quaternion() }; continue; }
    const A = S.actorById[prev.attach]; if (!A) continue;
    evalActor(A, k.at); placeAttached(Pp, prev, k.at);
    A.obj.updateMatrixWorld(true);
    const pos = Pp.obj.getWorldPosition(V()), quat = Pp.obj.getWorldQuaternion(new THREE.Quaternion());
    k.rel = { pos, quat, floor: k.floor ?? 0.02 };
    // a released prop that does not fall by gravity can be moved afterwards (`to` keys after the detach start where it was released): the object that hangs
    // in the air where the hand left it, then drops fast. k.wobble [amp, freq, decay]: it rocks in place meanwhile
    const later = k.fall ? [] : Pp.moves.filter(m => m.t >= k.at - 1e-6 && m.to != null);
    if (later.length) { let start = pos.clone(); for (const mv of later) { const end = V(mv.to[0] ?? start.x, mv.to[1] ?? start.y, mv.to[2] ?? start.z), d = end.clone().sub(start), l = d.length();   // a null coordinate keeps the release position
        Object.assign(mv, { pts: [start, end], segs: [{ a: start, b: end, l, L0: 0, head: Math.atan2(d.x, d.z) }], L: l, end }); start = end.clone(); } k.moves = later; }
    if (k.fall) { const h = Math.max(0, pos.y - k.rel.floor), vy = k.toss?.[1] || 0; k.landT = k.at + (vy + Math.sqrt(vy * vy + 2 * 9.8 * h)) / 9.8; if (k.impact) Pp.sfx.push({ t: k.landT, name: k.impact, vol: k.vol ?? 0.7 }); }
  }
}

function evalProp(Pp, t) {
  const o = propOwnerAt(Pp, t);
  const vis = lastKey(Pp.visKeys, t).visible; Pp.obj.visible = vis;
  if (o && o.attach && placeAttached(Pp, o, t)) { Pp.obj.userData.update?.(t); return; }
  if (Pp.obj.parent !== S.root) S.root.add(Pp.obj);
  if (o && o.detach && o.rel) {
    const dt = Math.max(0, t - o.at), p = o.rel.pos.clone();
    if (o.fall) { const vy = o.toss?.[1] || 0; p.y = Math.max(o.rel.floor, o.rel.pos.y + vy * dt - 0.5 * 9.8 * dt * dt); if (o.toss) { const k = Math.min(dt, o.landT - o.at); p.x += o.toss[0] * k; p.z += o.toss[2] * k; } }
    if (o.moves) for (const mv of o.moves) { if (t < mv.t) break; if (t >= mv.t1) { p.copy(mv.end); continue; } const k = (ease[mv.ease || 'inOut'] || ease.inOut)(clamp01((t - mv.t) / mv.dur)); p.copy(mv.pts[0]).lerp(mv.end, k); if (mv.arc) p.y += mv.arc * 4 * k * (1 - k); }
    Pp.obj.position.copy(p); Pp.obj.quaternion.copy(o.rel.quat); if (o.worldRot) Pp.obj.rotation.set(...o.worldRot);   // worldRot [x, y, z]: how it hangs once released (turned to the camera)
    if (o.wobble) Pp.obj.rotateZ(o.wobble[0] * Math.sin(dt * (o.wobble[1] ?? 20)) * Math.exp(-dt * (o.wobble[2] ?? 4)));
    if (o.fall && o.spinFall) Pp.obj.rotateX(o.spinFall * Math.min(dt, (o.landT ?? o.at) - o.at));
    if (o.restRot && t >= (o.landT ?? 0)) Pp.obj.rotation.set(...o.restRot);
  } else {
    Pp.obj.position.copy(propBasePos(Pp, t)); Pp.obj.rotation.set(Pp.rx0, Pp.ry0 + (Pp.spin ? Pp.spin * t : 0), Pp.rz0);
    if (Pp.rotKeys.length) { // rotTo keys: Euler lerp from the previous orientation (a roll is a change of z when the prop's nose is +Z)
      let r = [Pp.rx0, Pp.ry0, Pp.rz0];
      for (const rk of Pp.rotKeys) { if (t < rk.t) break; const w = rk.dur ? (ease[rk.ease] || ease.inOut)(clamp01((t - rk.t) / rk.dur)) : 1; r = r.map((v, i) => lerp(v, rk.rot[i], w)); }
      Pp.obj.rotation.set(r[0], r[1], r[2]);
    }
    const mv = Pp.moves.find(m => t >= m.t && t <= m.t1 && m.faceMove);
    if (mv) Pp.obj.rotation.y = headingAt(mv, t) + (mv.yawOffset || 0) * D2R;
    else { const last = [...Pp.moves].reverse().find(m => t > m.t1 && m.faceMove); if (last) Pp.obj.rotation.y = last.segs[last.segs.length - 1].head + (last.yawOffset || 0) * D2R; }
  }
  Pp.obj.scale.setScalar(scaleOf(Pp, t)); squashProp(Pp, t);
  Pp.obj.userData.update?.(t);
  if (Pp.alts) { // alternate looks after given times (the last one reached is shown in place of the prop)
    let cur = null; for (const a of Pp.alts) { a.obj.visible = false; if (t >= a.at) cur = a; }
    Pp.alt = cur ? cur.obj : Pp.alts[0].obj; Pp.altRot = cur ? cur.rot : Pp.alts[0].rot;
    const on = !!cur;
    Pp.obj.visible = !on && vis;
    if (on) { Pp.alt.visible = vis; Pp.obj.updateMatrixWorld(true); Pp.alt.position.copy(Pp.obj.getWorldPosition(V())); if (Pp.altRot) Pp.alt.rotation.set(...Pp.altRot); else Pp.alt.quaternion.copy(Pp.obj.getWorldQuaternion(new THREE.Quaternion())); Pp.alt.scale.setScalar(scaleOf(Pp, t)); }
  }
}

// ------------------------------------------------------------------------------------- actor evaluation
function speakingEnv(A, t) {
  for (const l of S.lines) if (l.speaker === A.id && t >= l.rs && t <= l.re && l.env) {
    const i = Math.floor((t - l.rs) * FPS); return l.env[Math.min(l.env.length - 1, Math.max(0, i))] || 0;
  }
  return null;
}
function clipPoseFn(A, key, t) {
  const lt = Math.max(0, (t - (key.t0 ?? key.at)) * (key.speed ?? 1) * (key.move || key.t0 != null ? 1 : S.tempo) + A.phase); // gaits keep their speed-derived cadence
  return samplePose(key.clip, lt, key.params || {});
}
function snapshot(A) {
  const J = A.obj.userData.joints || {}, out = {};
  for (const [k, g] of Object.entries(J)) out[k] = [g.rotation.x, g.rotation.y, g.rotation.z, g.position.x, g.position.y, g.position.z];
  const mv = A.obj.userData.mover; if (mv) out.__mover = [mv.rotation.x, mv.rotation.y, mv.rotation.z, mv.position.x, mv.position.y, mv.position.z];
  return out;
}
function writeSnap(A, a, b, w) {
  const J = A.obj.userData.joints || {};
  for (const [k, g] of Object.entries(J)) { const x = a[k], y = b[k]; if (!x || !y) continue; g.rotation.set(lerp(x[0], y[0], w), lerp(x[1], y[1], w), lerp(x[2], y[2], w)); g.position.set(lerp(x[3], y[3], w), lerp(x[4], y[4], w), lerp(x[5], y[5], w)); }
  const mv = A.obj.userData.mover; if (mv && a.__mover && b.__mover) { const x = a.__mover, y = b.__mover; mv.rotation.set(lerp(x[0], y[0], w), lerp(x[1], y[1], w), lerp(x[2], y[2], w)); mv.position.set(lerp(x[3], y[3], w), lerp(x[4], y[4], w), lerp(x[5], y[5], w)); }
}
const BLEND = 0.24;
const ONE_SHOT = new Set(['take', 'doubleTakeToon', 'scramble', 'hangAir', 'hangPhone', 'pancake', 'splat', 'paperThin', 'inflate', 'stretchGrab', 'periscope', 'hoseNeck', 'melt', 'meltDown', 'windUp', 'skidStop', 'teeter', 'stampPhone', 'stampDesk', 'cannonball', 'headStuck', 'sneeze', 'spinTop', 'headHammer']);   // clips that play once from their start: never as an actor's base clip
function effTime(id, t) {
  if (S.freezeAt == null || t <= S.freezeAt || S.freezeExcept.has(id)) return t;
  return t < S.freezeUntil ? S.freezeAt : t - (S.freezeUntil - S.freezeAt);
}
const frozenNow = t => S.freezeAt != null && t >= S.freezeAt && t < S.freezeUntil;

const EYES_SHUT = new Set(['blink', 'sleepy', 'happy', 'dead', 'laugh', 'cry', 'tongue', 'proud', 'yawn', 'kiss', 'relieved', 'drool', 'pain', 'bigGrin', 'tongueOut', 'dizzy', 'love', 'starEyes', 'wink']);
const STRONG = new Set(['shocked', 'surprised', 'scared', 'awe', 'angry', 'rage', 'sob', 'nervous', 'surprisedHappy', 'puppy']);
function evalActor(A, tIn) {
  const t = effTime(A.id, tIn);
  const obj = A.obj, ud = obj.userData;
  const vis = lastKey(A.visKeys, t).visible; obj.visible = vis;
  const pos = posAt(A, t), ry = facingAt(A, t), sc = scaleAt(A, t);
  const cur = lastKey(A.clipKeys, t), prev = prevKey(A.clipKeys, cur);
  const dt = t - cur.at;
  // expression (+ blink, + lip flaps while this actor speaks)
  const ek = lastKey(A.exprKeys, t); let expr = ek.expr, blink = false;
  const env = speakingEnv(A, tIn), ph = A.phase * 7 + (A.id ? A.id.length * 0.61 : 0);
  if (env != null && env > 0.16 && !['shocked', 'surprised', 'scared', 'sleepy', 'dead', 'happy', 'laugh', 'cry', 'yawn', 'awe'].includes(expr)) expr = env > 0.55 ? 'talkWide' : 'talk';
  else if (!EYES_SHUT.has(expr)) {
    // micro-animation: blinks (each expression keeps its own brows and mouth), a quick blink just before a strong reaction, idle glances
    const sinceKey = t - ek.at, cyc = (t + ph) % 3.3;
    if (cyc < 0.11 || (cyc > 0.3 && cyc < 0.38 && Math.floor((t + ph) / 3.3) % 3 === 1)) blink = true;
    if (sinceKey >= 0 && sinceKey < 0.09 && STRONG.has(expr)) blink = true;
    if (expr === 'neutral' && env == null) { const g = (t + ph * 1.7) % 4.1; if (g > 2.2 && g < 2.65) expr = Math.floor((t + ph) / 4.1) % 2 ? 'lookSide' : 'lookLeft'; }
  }
  if (ud.kind === 'human') {
    const pc = clipPoseFn(A, cur, t); let pose = pc;
    const kb = keyBlend(cur), BL = kb ?? BLEND / S.tempo, pp = prev && dt < (kb ?? BL + 0.12) ? clipPoseFn(A, prev, t) : null;
    if (pp) pose = kb != null ? blendPoses(pp, pose, ease.out(clamp01(dt / kb))) : actingBlend(pp, pose, dt, { dur: BL, anticipation: 0.06, antDur: 0.08 / S.tempo, overshoot: 0.5 });
    if (pp && ud.toon && (pc.root?.pivot || pp.root?.pivot)) pose.root.pivot = pc.root?.pivot || pp.root?.pivot;   // lying down / getting up turns about the hips all the way through the blend
    if (ud.toon) pose = toonOverlap(A, t, pose, BL);
    if (ud.toon && (ud.toonCfg?.shift ?? S.script?.idleShift)) pose = idleShift(A, t, pose, ud.toonCfg?.shift ?? S.script.idleShift);
    applyHuman(A, pose, pos, ry, sc);
    const tp = ud.toon ? toonLayer(A, t, pc, pp, dt, BL, sc, ry) : null;
    if (ud.faceRig) ud.setFaceState(rigFace(A, t, env, tp, pos, ry, sc)); else ud.setExpression?.(expr, blink);
    const fx = lastKey(A.fxKeys, t).fx; ud.setFx?.(fx, t);
    if (fx.shiver && ud.joints?.head) { ud.joints.head.rotation.z += 0.045 * Math.sin(t * 47); ud.joints.head.rotation.x += 0.02 * Math.sin(t * 61 + 1); }
  } else if (ud.kind === 'creature') {
    ud.setExpression?.(expr === 'talkWide' ? 'talk' : (expr === 'lookSide' || expr === 'lookLeft') ? ek.expr : expr);
    const lt = (k) => Math.max(0, (t - (k.t0 ?? k.at)) * (k.speed ?? 1) * (k.move || k.t0 != null ? 1 : S.tempo) + A.phase);
    if (prev && dt < BLEND / S.tempo) {
      ud.animate(prev.clip, lt(prev), prev.params || {}); const a = snapshot(A);
      ud.animate(cur.clip, lt(cur), cur.params || {}); const b = snapshot(A);
      writeSnap(A, a, b, ease.inOut(clamp01(dt / (BLEND / S.tempo))));
    } else ud.animate(cur.clip, lt(cur), cur.params || {});
    // pivot about the hips for human clips that ask for it (flips, lying down…)
    const hp = CLIPS[cur.clip] ? samplePose(cur.clip, lt(cur), cur.params || {}).root : null;
    if (hp?.pivot === 'hips' && ud.mover && ud.hipYMover) {
      const h = V(0, ud.hipYMover, 0), rh = h.clone().applyEuler(ud.mover.rotation);
      ud.mover.position.add(h.sub(rh));
    }
    obj.position.copy(pos); obj.rotation.set(0, ry, 0); obj.scale.setScalar(sc);
  } else { obj.position.copy(pos); obj.rotation.set(0, ry, 0); obj.scale.setScalar(sc); }
  // head look-at (on top of the clip), blended
  const lk = lastKey(A.lookKeys, t);
  if (lk && lk.look != null) {
    const w = ease.out(clamp01((t - lk.at - (ud.faceRig ? LOOK_LEAD : 0)) / 0.25));
    const off = lookOffsets(A, lk.look, t, pos, ry, sc);
    const plk = prevKey(A.lookKeys, lk); const off0 = plk && plk.look != null ? lookOffsets(A, plk.look, t, pos, ry, sc) : [0, 0];
    const J = ud.joints || {};
    const yaw = lerp(off0[0], off[0], w), pitch = lerp(off0[1], off[1], w);
    if (J.head) { J.head.rotation.y += yaw * 0.7; J.head.rotation.x += pitch * 0.8; }
    if (J.neck) { J.neck.rotation.y += yaw * 0.3; }
  } else if (lk && lk.look == null) {
    const plk = prevKey(A.lookKeys, lk);
    if (plk && plk.look != null && t - lk.at < 0.25 + LOOK_LEAD) { const off = lookOffsets(A, plk.look, t, pos, ry, sc), w = 1 - ease.out(clamp01((t - lk.at - (ud.faceRig ? LOOK_LEAD : 0)) / 0.25)); const J = ud.joints || {}; if (J.head) { J.head.rotation.y += off[0] * 0.7 * w; J.head.rotation.x += off[1] * 0.8 * w; } }
  }
  if (env != null && ud.joints?.head) ud.joints.head.rotation.x += 0.05 * env;
  return { pos, ry, sc };
}
// standing still, a cartoon actor shifts his weight from one leg to the other, by steps (not a slow sway: a shot lasts a second or two): the pelvis goes over the
// supporting leg, the other knee gives, the shoulders tilt back the other way. Each actor has his own rhythm. Opt-in: script `idleShift: 1` or cast toon {shift: 1}
function idleShift(A, t, pose, amt) {
  const rt = pose.root || {}, k0 = amt === true ? 1 : +amt || 0; if (!k0 || Math.abs(rt.rx || 0) > 0.3 || Math.abs(rt.rz || 0) > 0.3 || Math.abs(rt.y || 0) > 0.15) return pose;   // lying, sitting, in the air: no
  if (posAt(A, t - 0.25).distanceTo(posAt(A, t + 0.25)) > 0.02) return pose;   // on the move
  const h = hash01((A.id ? [...A.id].reduce((a, c) => a + c.charCodeAt(0), 0) : 7) * 0.37 + A.phase), P = 1.4 + 1.2 * h, x = (t + 5 + h * 9) / P, i = Math.floor(x), u = (x - i) * P;
  const val = j => (j % 2 ? 1 : -1) * (0.55 + 0.45 * hash01(j * 1.3 + h * 17)), s = (val(i - 1) + (val(i) - val(i - 1)) * ease.inOut(clamp01(u / 0.42))) * k0, a = Math.abs(s);
  const out = { ...pose, root: { ...rt, x: (rt.x || 0) + 0.07 * s, rz: (rt.rz || 0) - 0.02 * s } }, add = (j, v) => { const r = pose[j] || ZERO; out[j] = [r[0] + v[0], r[1] + v[1], r[2] + v[2]]; };
  add('hipL', [s < 0 ? -0.16 * a : 0, 0, -0.085 * s]); add('hipR', [s > 0 ? -0.16 * a : 0, 0, -0.085 * s]);   // both legs stay planted under the shifted pelvis; the free thigh comes forward
  add(s > 0 ? 'kneeR' : 'kneeL', [0.3 * a, 0, 0]); add(s > 0 ? 'footR' : 'footL', [-0.14 * a, 0, 0]);          // its knee gives, the heel lifts
  add('torso', [0, 0, 0.05 * s]); add('head', [0, 0, -0.03 * s]);
  return out;
}
// ---- cartoon rig layers (engine/toon.js): only for actors built with `toon`
// overlapping action: the far joints replay the pose a few frames late (forearms, hands, head), so gestures trail and settle
// a clip key can set its own blend from the previous clip (seconds): k(t, clip=..., blend=0.02) is a hard hit (plain fast blend, no anticipation, nothing trails);
// on a move: blend (into the gait) and thenBlend (into the clip that follows it)
const keyBlend = c => c.key?.blend ?? (c.move ? c.move.blend : c.afterMove?.thenBlend);
function toonPoseAt(A, tt, BL0) {
  const c = lastKey(A.clipKeys, tt), p = prevKey(A.clipKeys, c), d = tt - c.at, kb = keyBlend(c), BL = BLEND / S.tempo; let q = clipPoseFn(A, c, tt);
  if (p && kb != null) { if (d < kb) q = blendPoses(clipPoseFn(A, p, tt), q, ease.out(clamp01(d / kb))); }
  else if (p && d < BL + 0.12) q = actingBlend(clipPoseFn(A, p, tt), q, d, { dur: BL, anticipation: 0.06, antDur: 0.08 / S.tempo, overshoot: 0.5 });
  return q;
}
const TOON_LAG = { elbowL: 0.035, elbowR: 0.035, handL: 0.07, handR: 0.07, head: 0.045, neck: 0.02 };
function toonOverlap(A, t, pose, BL) {
  const k = A.obj.userData.toonCfg?.overlap ?? 1; if (!k) return pose;
  const out = { ...pose }, cache = {};
  for (const [j, lag] of Object.entries(TOON_LAG)) { const tt = Math.max(0, t - lag * k), key = tt.toFixed(4); const q = cache[key] || (cache[key] = toonPoseAt(A, tt, BL)); if (q[j]) out[j] = q[j]; }
  return out;
}
// the clip's own channels (blended across a clip change) + automatic layers: breathing, squash and stretch from the vertical motion,
// drag of the spine against horizontal acceleration (lean back on a start, carry on forward on a stop)
function toonLayer(A, t, pc, pp, dt, BL, sc, ry) {
  const ud = A.obj.userData, cfg = ud.toonCfg || {}, d = 1 / FPS;
  // the story's own keys (k(t, toon={...})); `auto` in a key (0..1) doses the automatic layers while the key holds: a choreographed fall (the feet leave,
  // the head stays) must not be stretched and squashed again by its own speed
  let keyed = null, ka = 1;
  if (A.toonKeys) { const kk = lastKey(A.toonKeys, t), pk = prevKey(A.toonKeys, kk), w = kk.dur ? (ease[kk.ease] || ease.out)(clamp01((t - kk.at) / kk.dur)) : 1, bl = pk && w < 1;
    keyed = bl ? blendToon(pk.toon, kk.toon, w) : kk.toon; ka = bl ? lerp(pk.toon.auto ?? 1, kk.toon.auto ?? 1, clamp01(w)) : (kk.toon.auto ?? 1); }
  const auto = (cfg.auto ?? 1) * ka;
  let tp = pp ? blendToon(pp.toon || {}, pc.toon || {}, ease.out(clamp01(dt / BL))) : (pc.toon || {});
  const extra = {}, ph = A.phase * 9 + (A.id ? A.id.length * 0.77 : 0);
  const br = (cfg.breathe ?? 1) * 0.012 * Math.sin(t * 1.75 + ph);   // breathing: the chest rises and falls
  const bend = { spine: [0, 0, 0, 1 + br, null] };
  if (auto) {
    const h = tt => posAt(A, tt).y + (clipPoseFn(A, lastKey(A.clipKeys, tt), tt).root?.y || 0);
    const h1 = h(t), vy = (h(t + d) - h(t - d)) / (2 * d), a1 = (h(t + d) - 2 * h1 + h(t - d)) / (d * d), a2 = (h(t + 2 * d) - 2 * h1 + h(t - 2 * d)) / (4 * d * d), a3 = (h(t + 3 * d) - 2 * h1 + h(t - 3 * d)) / (9 * d * d);
    const stretch = clamp(Math.abs(vy) * 0.05, 0, 0.32), squash = clamp(Math.max(a1 * 0.6, a2, a3) * 0.004, 0, 0.38);
    const sy = 1 + (stretch - squash) * auto; if (Math.abs(sy - 1) > 0.004) { const kx = 1 / Math.sqrt(sy); extra.sq = [kx, sy, kx]; }
    const hl = clamp(-a1 * 0.0016, -0.03, 0.22) * auto * (cfg.hatLag ?? 1); if (Math.abs(hl) > 0.004) extra.hat = [hl, 0, 0];   // the hat is not nailed on: it lifts when the body drops away, presses down on a landing
    const p0 = posAt(A, t - 3 * d), p1 = posAt(A, t), p2 = posAt(A, t + 3 * d), ax = (p2.x - 2 * p1.x + p0.x) / (9 * d * d), az = (p2.z - 2 * p1.z + p0.z) / (9 * d * d);
    const af = ax * Math.sin(ry) + az * Math.cos(ry), as = ax * Math.cos(ry) - az * Math.sin(ry);   // forward / sideways (the actor faces +Z turned by ry)
    bend.spine[0] = clamp(-af * 0.022, -0.5, 0.5) * auto; bend.spine[1] = clamp(as * 0.022, -0.4, 0.4) * auto;
    // limbs drag behind a fast swing (the upper part arcs against the joint's turn, the lower part a little more): rubber-hose arcs
    const dk = 0.026 * auto * (cfg.drag ?? 1);
    if (dk) { const pa = toonPoseAt(A, t - d, BL), pb = toonPoseAt(A, t + d, BL), ls = (cfg.limbSmear ?? S.script?.limbSmear ?? 0) * auto, w = (j, i) => ((pb[j]?.[i] || 0) - (pa[j]?.[i] || 0)) / (2 * d);
      for (const sd of ['L', 'R']) {
        const sx = w('shoulder' + sd, 0), sz = w('shoulder' + sd, 2), ex = w('elbow' + sd, 0), hx = w('hip' + sd, 0), kx = w('knee' + sd, 0);
        bend['arm' + sd] = [clamp(-sx * dk, -0.45, 0.45), clamp(-sz * dk, -0.45, 0.45), 0, 1, null]; bend['fore' + sd] = [clamp(-(sx + ex) * dk * 1.3, -0.6, 0.6), clamp(-sz * dk * 1.3, -0.6, 0.6), 0, 1, null];
        bend['leg' + sd] = [clamp(-hx * dk * 0.7, -0.3, 0.3), 0, 0, 1, null]; bend['shin' + sd] = [clamp(-(hx + kx) * dk * 0.8, -0.4, 0.4), 0, 0, 1, null];
        // a limb that swings very fast is drawn as a smear: its far half stretches and thins along the swing (opt-in: script `limbSmear: 1` or cast toon {limbSmear: 1})
        if (ls) { const ka = clamp((Math.hypot(sx + ex, sz) - 9) * 0.035, 0, 0.6) * ls, kl = clamp((Math.abs(hx + kx) - 9) * 0.03, 0, 0.5) * ls;
          if (ka > 0.02) { bend['fore' + sd][3] = 1 + ka; bend['arm' + sd][3] = 1 + 0.35 * ka; }
          if (kl > 0.02) { bend['shin' + sd][3] = 1 + kl; bend['leg' + sd][3] = 1 + 0.3 * kl; } }
      } }
    // a very fast travel smears the body along its path (a blur drawn as a stretch)
    const vx = (p2.x - p0.x) / (6 * d), vz = (p2.z - p0.z) / (6 * d), sp = Math.hypot(vx, vz), sm = clamp((sp - 5.5) * 0.07, 0, 0.7) * auto * (cfg.smear ?? 1);
    if (sm > 0.01) { const f = (vx * Math.sin(ry) + vz * Math.cos(ry)) / sp, sd = (vx * Math.cos(ry) - vz * Math.sin(ry)) / sp, q = extra.sq || [1, 1, 1]; extra.sq = [q[0] * (1 + sm * sd * sd - 0.2 * sm * f * f), q[1] * (1 - 0.15 * sm), q[2] * (1 + sm * f * f - 0.2 * sm * sd * sd)]; }
    // standing still: the weight drifts from one leg to the other (the spine leans a little, the neck rights the head)
    if (sp < 0.3) { const ws = 0.032 * Math.sin(t * 0.85 + ph * 1.3) * auto * (cfg.sway ?? 1); bend.spine[1] += ws; bend.neck = [0, -ws * 0.8, 0, 1, null]; }
  }
  extra.bend = bend;
  let all = addToon(tp, extra);
  if (keyed) all = addToon(all, keyed);
  ud.toon.apply(all, t, sc);
  if (ud.fingers) ud.fingers.set(all.hands);
  if (ud.cloth) {   // what trails: the apparent wind (scene wind minus his own velocity, taken a few frames late so it lags), in world space
    const tl = t - 0.04, dd = 2 * d, hy = tt => posAt(A, tt).y + (clipPoseFn(A, lastKey(A.clipKeys, tt), tt).root?.y || 0) * sc, a = posAt(A, tl - dd), b = posAt(A, tl + dd), w = windAt(tl);
    const lw = all.wind, wx = lw ? lw[0] * Math.cos(ry) + lw[2] * Math.sin(ry) : 0, wz = lw ? -lw[0] * Math.sin(ry) + lw[2] * Math.cos(ry) : 0;   // toon channel `wind`: his own wind, given in his frame
    A.obj.updateMatrixWorld(true); const sb = all.bend?.spine; ud.cloth.apply([w.x + wx - (b.x - a.x) / (2 * dd), w.y + (lw ? lw[1] : 0) - (hy(tl + dd) - hy(tl - dd)) / (2 * dd), w.z + wz - (b.z - a.z) / (2 * dd)], t, cfg.cloth ?? 1, sb ? (sb[4] ?? 1 / Math.sqrt(sb[3] ?? 1)) : 1, all.hairUp || 0);
  }
  return all;
}
// scene wind: fx {type: 'wind', at, dur, v: [x, y, z] (m/s, world), attack (0.06 s), release (0.25 s)}; gusts add up
function windAt(t) {
  const w = V(0, 0, 0);
  for (const f of S.sc?.fx || []) if (f.type === 'wind') { const a = T(f.at ?? 0, S.sc), dur = f.dur ?? 0.4, at_ = f.attack ?? 0.06, rl = f.release ?? 0.25, u = t - a; if (u < 0 || u > dur + rl) continue;
    const e = u < at_ ? u / at_ : u < dur ? 1 : 1 - (u - dur) / rl; w.x += f.v[0] * e; w.y += f.v[1] * e; w.z += f.v[2] * e; }
  return w;
}
// ---- face rig: the expression as numbers, blended from the previous one (the brows lead, the mouth trails, a little overshoot), then
// the life on top: a blink that closes and opens over a few frames, the eyes that move before the head, small darts of the pupils,
// lip flaps that keep the expression, and whatever the clip asks for (toon.face.expr)
const LOOK_LEAD = 0.07, FACE_DUR = 0.15, CROSS_SIGN = 1;
const RIG_STRONG = new Set([...STRONG, 'take', 'takeSmall', 'zap', 'gulp']), NO_FLAP = new Set(['shocked', 'surprised', 'scared', 'sleepy', 'dead', 'happy', 'laugh', 'cry', 'yawn', 'awe', 'take', 'takeSmall']);
const backOut = (u, c1) => 1 + (c1 + 1) * Math.pow(u - 1, 3) + c1 * Math.pow(u - 1, 2);
const hash01 = n => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const blinkLid = tb => tb < 0 ? 0 : tb < 0.066 ? Math.pow(tb / 0.066, 0.7) : tb < 0.1 ? 1 : tb < 0.24 ? 1 - ease.out((tb - 0.1) / 0.14) : 0;
function rigFace(A, t, env, tp, pos, ry, sc) {
  const custom = S.script?.faces, ek = lastKey(A.exprKeys, t), pk = prevKey(A.exprKeys, ek), since = t - ek.at, ph = A.phase * 7 + (A.id ? A.id.length * 0.61 : 0), cfg = A.obj.userData.faceCfg || {};
  let st;
  if (pk && since < FACE_DUR + 0.12) { const u = x => clamp01((since - x) / FACE_DUR); st = blendFace(faceState(pk.expr, custom), faceState(ek.expr, custom), backOut(u(0), 2.2), backOut(u(0.03), 1.3), ease.out(u(0.05))); }
  else st = cloneFace(faceState(ek.expr, custom));
  const cf = tp?.face; if (cf?.expr && cf.exprW > 0.01) st = blendFace(st, faceState(cf.expr, custom), Math.min(1.15, cf.exprW));   // the clip pulls the face (a take, a strain)
  const strong = RIG_STRONG.has(ek.expr) && since < 0.9 || (cf?.exprW || 0) > 0.3, E = st.eyes;
  // blink: every 3.3 s (sometimes twice), and a quick one that winds up a strong reaction
  let lid = 0;
  if (!strong && (cfg.blink ?? 1)) { const cyc = (t + ph) % 3.3; lid = blinkLid(cyc); if (Math.floor((t + ph) / 3.3) % 3 === 1) lid = Math.max(lid, blinkLid(cyc - 0.3)); }
  if (RIG_STRONG.has(ek.expr) && pk && since < 0.1) lid = Math.max(lid, Math.sin(Math.PI * clamp01(since / 0.1)));
  if (cf?.lid) lid = Math.max(lid, cf.lid);   // toon face.lid 0..1: a keyed blink (a slow one: key it up and down over a few frames) or heavy lids
  // gaze: toward the look target before the head gets there, into a turn of the body before it starts, and idle darts
  let gx = 0, gy = 0; const lk = lastKey(A.lookKeys, t), plk = lk ? prevKey(A.lookKeys, lk) : null;
  if (lk) {
    const to = lk.look != null ? lookOffsets(A, lk.look, t, pos, ry, sc) : [0, 0], from = plk && plk.look != null ? lookOffsets(A, plk.look, t, pos, ry, sc) : [0, 0];
    const wh = ease.out(clamp01((t - lk.at - LOOK_LEAD) / 0.25)), wg = ease.out(clamp01((t - lk.at) / 0.06));
    gx += (to[0] - from[0]) * (1 - wh) * wg * 1.5; gy += (to[1] - from[1]) * (1 - wh) * wg * 1.5;
    if (Math.abs(to[0] - from[0]) > 0.5 && t - lk.at > 0.02 && t - lk.at < 0.3) lid = Math.max(lid, blinkLid(t - lk.at - 0.05) * 0.85);   // a big shift of the gaze takes a blink with it
  }
  gx += clamp(wrapA(facingAt(A, t + 0.2) - ry) * 1.1, -0.7, 0.7);
  if (!strong && (cfg.darts ?? 1)) {
    const T = 1.9, x = (t + ph * 1.3) / T, i = Math.floor(x), tt = (x - i) * T;
    if (hash01(i + ph * 3.1) > 0.42) { const a = hash01(i * 2.7 + 1.3) * Math.PI * 2, m = (0.2 + 0.3 * hash01(i * 5.1 + 0.7)) * (lk && lk.look != null ? 0.5 : 1), t0 = 0.2 + 0.6 * hash01(i * 7.7), d = 0.25 + 0.35 * hash01(i * 3.3 + 2), u = tt - t0;
      const k = u < 0 ? 0 : u < 0.05 ? u / 0.05 : u < d ? 1 : u < d + 0.07 ? 1 - (u - d) / 0.07 : 0; gx += Math.cos(a) * m * k; gy += Math.sin(a) * m * 0.45 * k; }
  }
  const br = 1.1 * Math.sin(t * 1.75 + ph);   // the brows breathe with the chest
  for (const s of 'LR') { const e = E[s]; e.px = clamp(e.px + gx, -1, 1); e.py = clamp(e.py + gy, -1, 1); if (e.kind === 'open') e.lid = Math.max(e.lid, lid); st.brows[s].dy += br + 4 * lid; }
  // lip flaps: the mouth alone speaks, the brows punch the loud syllables
  if (env != null && env > 0.16 && !NO_FLAP.has(ek.expr)) { st.mouth = { ...st.mouth, spr: env > 0.6 ? 'open' : 'o', w: 1, h: 0.8 + 0.5 * env, tilt: 0 }; for (const s of 'LR') st.brows[s].dy -= 6 * env; }
  // the jaw drops: the mouth of a scream on the stretched lower face; eyes out on stalks leave dark sockets
  if (cf) {
    const jw = cf.jaw || 0;
    if (jw > 0.45) st.mouth = { ...st.mouth, spr: 'scream', w: 1, h: 0.5 + 0.5 * Math.min(1, jw), tilt: 0, dx: 0, dy: 0 }; else if (jw > 0.12 && !/scream|yawn|laugh|O/.test(st.mouth.spr)) st.mouth = { ...st.mouth, spr: 'O', w: 1, h: 0.8 + jw, tilt: 0, dx: 0, dy: 0 };
    if ((cf.pop || 0) > 0.08) for (const s of 'LR') { E[s] = { ...E[s], kind: 'dot', s: 2.2, open: 1 }; st.brows[s].dy -= 26 * cf.pop; }
    if (cf.cross) { E.L.px = clamp(E.L.px + CROSS_SIGN * 0.95 * cf.cross, -1, 1); E.R.px = clamp(E.R.px - CROSS_SIGN * 0.95 * cf.cross, -1, 1); }   // cross-eyed (painted eyes)
    if (cf.gx || cf.gy) for (const s of 'LR') { E[s].px = clamp(E[s].px + (cf.gx || 0), -1, 1); E[s].py = clamp(E[s].py + (cf.gy || 0), -1, 1); }   // face.gx / face.gy (-1..1): the pupils alone look aside (- = toward his right: screen left when he faces us) / down (+) or up (-), the head stays where it is (eyes that follow a thing while the face stays on us)
  }
  return st;
}
function lookOffsets(A, target, t, pos, ry, sc) {
  let p;
  if (Array.isArray(target)) p = V(...target);
  else if (S.actorById[target]) { const B = S.actorById[target]; p = posAt(B, effTime(B.id, t)); p.y += (B.obj.userData.height || 1.9) * scaleAt(B, t) * 0.9; }
  else if (S.propById[target]) { p = S.propById[target].obj.getWorldPosition(V()); }
  else return [0, 0];
  const eye = pos.clone(); eye.y += (A.obj.userData.height || 1.9) * sc * 0.9;
  const dx = p.x - eye.x, dz = p.z - eye.z, dy = p.y - eye.y;
  const yaw = clamp(wrapA(Math.atan2(dx, dz) - ry), -1.15, 1.15);
  const pitch = clamp(-Math.atan2(dy, Math.hypot(dx, dz)), -0.6, 0.6);
  return [yaw, pitch];
}
function applyHuman(A, pose, pos, ry, s) {
  const obj = A.obj, J = obj.userData.joints;
  for (const j of JOINTS) { if (!J[j]) continue; const r = pose[j] || ZERO; J[j].rotation.set(r[0], r[1], r[2]); }
  if (J.head) J.head.scale.setScalar(pose.headScale || 1);   // a clip can inflate the head (holding the breath) and flush it red (pose.flush 0..1)
  const hm = obj.userData.headMesh; if (hm && (pose.flush || hm.userData.flushed)) { const f = pose.flush || 0; for (const m of [].concat(hm.material)) { if (!m.color) continue; m.userData.c0 = m.userData.c0 || m.color.clone(); m.color.copy(m.userData.c0).multiply(new THREE.Color(1, 1 - 0.55 * f, 1 - 0.62 * f)); } hm.userData.flushed = f > 0; }
  const rt = pose.root || {};
  obj.rotation.order = 'YXZ';
  obj.rotation.set(rt.rx || 0, ry + (rt.ry || 0), rt.rz || 0);
  obj.scale.setScalar(s);
  const off = V(rt.x || 0, rt.y || 0, rt.z || 0).multiplyScalar(s).applyAxisAngle(V(0, 1, 0), ry);
  const p = pos.clone().add(off);
  if (rt.pivot === 'hips') {
    const h = V(0, obj.userData.hipY * s, 0), rh = h.clone().applyEuler(obj.rotation);
    p.add(h.sub(rh));
  }
  obj.position.copy(p);
}

function tetherAnchor(a) {
  const off = V(...(a.offset || [0, 0, 0]));
  if (a.actor && S.actorById[a.actor]) return jointFor(S.actorById[a.actor].obj, a).localToWorld(off);
  if (a.prop && S.propById[a.prop]) return S.propById[a.prop].obj.localToWorld(off);
  return null;
}
function evalTethers(t) {
  for (const { td, m } of S.tethers || []) {
    const on = (td.from == null || t >= td.from) && (td.until == null || t < td.until); m.visible = on; if (!on) continue;
    const a = tetherAnchor(td.a), b = tetherAnchor(td.b); if (!a || !b) { m.visible = false; continue; }
    const n = 10, sag = (td.sag ?? 0.25) * a.distanceTo(b), pts = [];
    for (let i = 0; i <= n; i++) { const u = i / n, p = a.clone().lerp(b, u); p.y -= sag * 4 * u * (1 - u); pts.push(p); }
    m.geometry.dispose(); m.geometry = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 20, td.radius || 0.012, 5);
  }
}
function evalAll(t) {
  for (const A of S.actors) evalActor(A, t);
  for (const Pp of S.props) evalProp(Pp, effTime(Pp.id, t));
  S.set?.userData.update?.(effTime('__set__', t));
  S.stage.scene.updateMatrixWorld(true);
  if (S.tethers?.length) { evalTethers(t); }
}

// ------------------------------------------------------------------------------------- camera
function subjectObjs(c) {
  const ids = c.frame == null ? [] : Array.isArray(c.frame) && typeof c.frame[0] !== 'number' ? c.frame : [c.frame];
  return ids.map(id => (typeof id === 'string' && (S.actorById[id] || S.propById[id.replace(/^prop:/, '')])) || (Array.isArray(id) ? { point: V(...id) } : null)).filter(Boolean);
}
function headBox(o) { // whole head joint subtree: face + hair + ears + hat/cap
  const ud = o.obj.userData;
  const src = ud.joints?.head || ud.headMesh;
  if (!src) return null;
  const b = new THREE.Box3();
  src.traverse(n => {
    if (!n.isMesh || !n.visible || n.name === 'outline') return;
    for (let p = n; p && p !== src; p = p.parent) if (p.userData.isSceneProp) return;   // a beard / prop on the head is not the head
    n.geometry.computeBoundingBox?.(); const bb = n.geometry.boundingBox?.clone().applyMatrix4(n.matrixWorld); if (bb) b.union(bb);
  });
  return b;
}
function bodyBox(root) {
  const b = new THREE.Box3();
  root.traverse(n => {
    if (!n.isMesh || !n.visible || n.name === 'outline') return;
    for (let p = n; p && p !== root; p = p.parent) if (p.userData.isSceneProp) return;
    n.geometry.computeBoundingBox?.(); const bb = n.geometry.boundingBox?.clone().applyMatrix4(n.matrixWorld); if (bb) b.union(bb);
  });
  return b;
}
let withProps = false;
function regionFor(subs, size) {
  const spec = SIZE[size] || SIZE.ms;
  const box = new THREE.Box3();
  for (const s of subs) {
    if (s.point) { box.expandByPoint(s.point.clone().addScalar(-0.4)); box.expandByPoint(s.point.clone().addScalar(0.4)); continue; }
    const src = s.alt && s.alt.visible ? s.alt : s.obj;
    if (!src.visible) continue;
    const full = s.kind === 'prop' || withProps ? new THREE.Box3().setFromObject(src) : bodyBox(src);
    if (full.isEmpty()) continue;
    let b = full.clone();
    if (spec.part === 'head' || spec.part === 'headShoulders') {
      const hb = s.kind !== 'prop' ? headBox(s) : null;
      if (hb && !hb.isEmpty()) {
        b = hb.clone(); const hh = hb.max.y - hb.min.y;
        if (spec.part === 'head') b.expandByScalar(hh * (spec.pad - 1) * 0.5);
        else { b.min.y -= hh * 0.5; b.max.y += hh * 0.06; const c = b.getCenter(V()); const w = Math.max(b.max.x - b.min.x, b.max.z - b.min.z) * 1.4; b.min.x = Math.min(b.min.x, c.x - w / 2); b.max.x = Math.max(b.max.x, c.x + w / 2); b.min.z = Math.min(b.min.z, c.z - w / 2); b.max.z = Math.max(b.max.z, c.z + w / 2); }
      } else { const h = full.max.y - full.min.y; b.min.y = full.max.y - h * (spec.part === 'head' ? 0.35 : 0.5); }
    } else if (typeof spec.part === 'number' && spec.part < 1) {
      const h = full.max.y - full.min.y; b.min.y = full.max.y - h * spec.part;
    }
    box.union(b);
  }
  return box;
}
function camBasis(yaw, elev) {
  const dir = V(Math.sin(yaw) * Math.cos(elev), Math.sin(elev), Math.cos(yaw) * Math.cos(elev));
  const right = V(Math.cos(yaw), 0, -Math.sin(yaw));
  return { dir, right };
}
const WIDTH_SLACK = { ecu: 2.2, cu: 1.9, mcu: 1.7, ms: 1.5, mls: 1.25, fs: 1.12, ws: 1.0, ews: 1.0 };
function fitDistance(box, yaw, elev, fov, fill, size) {
  const { dir, right } = camBasis(yaw, elev);
  const c = box.getCenter(V());
  let wMin = 1e9, wMax = -1e9, hMin = 1e9, hMax = -1e9, dMin = 1e9, dMax = -1e9;
  const up = V(0, 1, 0).sub(dir.clone().multiplyScalar(dir.y)).normalize();
  for (let i = 0; i < 8; i++) {
    const p = V(i & 1 ? box.max.x : box.min.x, i & 2 ? box.max.y : box.min.y, i & 4 ? box.max.z : box.min.z).sub(c);
    const r = p.dot(right), u = p.dot(up), d = p.dot(dir);
    wMin = Math.min(wMin, r); wMax = Math.max(wMax, r); hMin = Math.min(hMin, u); hMax = Math.max(hMax, u); dMin = Math.min(dMin, d); dMax = Math.max(dMax, d);
  }
  const tanV = Math.tan(fov * D2R / 2), tanH = tanV * (S.W / S.H);
  const dist = Math.max((hMax - hMin) / 2 / (tanV * fill), (wMax - wMin) / 2 / (WIDTH_SLACK[size] || 1) / (tanH * Math.min(0.86, fill + 0.04)));
  return { dist: dist + dMax, center: c, up };
}
function facingOf(s, t) { return s.point ? 0 : s.kind === 'prop' ? s.obj.rotation.y : facingAt(s, effTime(s.id, t)); }
const RAY = new THREE.Raycaster();
function blocked(from, to, ignore) {
  const d = to.clone().sub(from), L = d.length(); if (L < 0.05) return null;
  RAY.set(from, d.normalize()); RAY.near = 0.05; RAY.far = L;
  const fwd = RAY.intersectObjects(S.root.children, true);
  RAY.set(to, from.clone().sub(to).normalize()); RAY.near = 0.02; RAY.far = L - 0.05;
  const rev = RAY.intersectObjects(S.root.children, true).map(h => ({ ...h, distance: L - h.distance }));
  const hits = [...fwd, ...rev].sort((a, b) => a.distance - b.distance);
  for (const h of hits) {
    const o = h.object;
    if (!o.visible || o.name === 'outline' || !o.isMesh) continue;
    const m = Array.isArray(o.material) ? o.material[0] : o.material;
    if (m && m.transparent && m.opacity < 0.6) continue;
    let p = o, skip = false; while (p) { if (ignore.has(p)) { skip = true; break; } if (!p.visible) { skip = true; break; } p = p.parent; }
    if (skip) continue;
    if (isThin(o)) continue; // bars, rails, wires, decals, tiny props never hide a character
    return h.distance;
  }
  return null;
}
function isThin(o) { // a rod (two small dimensions) or a tiny object: see-through for occlusion purposes
  if (o.userData._thin != null) return o.userData._thin;
  const g = o.geometry; if (!g) return (o.userData._thin = true);
  if (!g.boundingBox) g.computeBoundingBox();
  const sz = g.boundingBox.getSize(V()).multiply(o.getWorldScale(V()));
  const d = [Math.abs(sz.x), Math.abs(sz.y), Math.abs(sz.z)].sort((a, b) => a - b);
  return (o.userData._thin = d[1] < 0.08 || d[2] < 0.12);
}
function solveCam(c, sc) {
  const t0 = c.t0, t1 = c.t1, span = Math.max(0.01, t1 - t0);
  if (c.from) return { kind: 'explicit', pos0: V(...c.from), pos1: V(...(c.to || c.from)), look0: V(...(c.lookAt || [0, 1.2, 0])), look1: V(...(c.lookAt2 || c.lookAt || [0, 1.2, 0])), fov: c.lens || 40 };
  if (c.ots || c.pov) return { kind: c.ots ? 'ots' : 'pov', spec: c.ots || c.pov, fov: c.lens || (c.ots ? 38 : 50) };
  const subs = subjectObjs(c);
  if (!subs.length) { warn(`[${sc.id}] cam@${t0.toFixed(2)} has no subject`); return { kind: 'explicit', pos0: V(0, 1.6, 6), pos1: V(0, 1.6, 6), look0: V(0, 1.2, 0), look1: V(0, 1.2, 0), fov: 40 }; }
  const size = c.size || 'ms', spec = SIZE[size] || SIZE.ms; withProps = !!c.withProps;
  const n = c.move === 'track' ? Math.max(2, Math.ceil(span / 0.2) + 1) : 4;
  const samples = [];
  for (let i = 0; i < n; i++) { const ts = t0 + span * (n === 1 ? 0 : i / (n - 1)) * 0.999; evalAll(ts); samples.push({ t: ts, box: regionFor(subs, size) }); }
  const union = new THREE.Box3(); samples.forEach(s => union.union(s.box));
  if (union.isEmpty()) { warn(`[${sc.id}] cam@${t0.toFixed(2)}: subjects invisible`); union.setFromCenterAndSize(V(0, 1, 0), V(1, 2, 1)); }
  const facing = c.worldAngle != null ? 0 : facingOf(subs[0], t0 + span * 0.3);
  const fov = c.lens || spec.lens, fill = c.fill || spec.fill;
  let elev = (c.elev ?? spec.elev) * D2R;
  const baseYaw = c.worldAngle != null ? c.worldAngle * D2R : facing + (c.angle ?? 15) * D2R;
  const ignore = new Set(subs.filter(s => s.obj).map(s => s.obj));
  const frameBox = c.move === 'track' ? samples[0].box : union;
  const CLUT = new THREE.Raycaster();
  const clutterAt = (pos, f, d, right) => { // big objects right in front of the lens (counter tops, stools, posts, parked cars)
    const halfH = d * Math.tan(fov * D2R / 2), halfW = halfH * S.W / S.H, maxD = Math.min(2.5, 0.5 * d);
    let n = 0;
    for (const gx of [-0.6, 0, 0.6]) for (const gy of [-0.7, -0.35, 0, 0.35, 0.7]) {
      const tgt = f.center.clone().addScaledVector(right, gx * halfW).addScaledVector(f.up, gy * halfH);
      CLUT.set(pos, tgt.sub(pos).normalize()); CLUT.near = 0.02; CLUT.far = maxD;
      for (const h of CLUT.intersectObjects(S.root.children, true)) {
        const o = h.object; if (!o.isMesh || !o.visible || o.name === 'outline') continue;
        const m = Array.isArray(o.material) ? o.material[0] : o.material; if (m && m.transparent && m.opacity < 0.6) continue;
        if (isThin(o)) continue;
        let p = o, skip = false; while (p) { if (ignore.has(p) || !p.visible) { skip = true; break; } p = p.parent; }
        if (!skip) { n++; break; }
      }
    }
    return n;
  };
  // ---- candidate cameras, checked at several moments of the shot (3 for tracking shots, 2 for fixed ones) ----
  // A subject is hidden when its head is blocked, or its whole upper row, or a whole column (a post), or 5 of 6 probes
  // (legs behind a desk / counter are fine). A camera inside an actor or inside static set geometry is rejected outright.
  const front = [0, 25, -25, 50, -50, 75, -75], back = [100, -100, 130, -130, 160, -160, 180];
  const tries = c.noOcclusion ? [[0, elev]] : [...front.map(o => [o, elev]), ...front.map(o => [o, elev + 18 * D2R]), ...back.map(o => [o, elev])];
  const cand = tries.map(([o, el]) => { const yaw = baseYaw + o * D2R, f = fitDistance(frameBox, yaw, el, fov, fill, size), bs = camBasis(yaw, el);
    return { yaw, el, f, d: f.dist * (c.zoom || 1), dir: bs.dir, right: bs.right, hidden: false, dead: false, score: 0, near: null, clutter: 0, why: '' }; });
  const groupsNow = () => {
    const groups = [];
    for (const s of subs) {
      if (s.point) continue; // framing helper only (it may sit inside a body or a prop)
      const b = regionFor([s], size); if (b.isEmpty()) continue;
      const cc = b.getCenter(V()), h = b.max.y - b.min.y, hb = s.kind !== 'prop' ? headBox(s) : null, lift = p => (p.y = Math.max(0.12, p.y), p);
      const probes = [{ p: lift(hb && !hb.isEmpty() ? hb.getCenter(V()) : V(cc.x, b.max.y - h * 0.12, cc.z)), u: 0, head: true }];
      for (const [row, fy] of [0.8, 0.5, 0.2].entries()) for (const u of [-1, 1]) probes.push({ p: lift(V(cc.x, b.min.y + h * fy, cc.z)), u, row });
      groups.push({ halfW: Math.max(0.05, Math.hypot(b.max.x - b.min.x, b.max.z - b.min.z) * 0.18), probes });
    }
    return groups;
  };
  if (!S.staticBoxes) { // big static set meshes (walls, rocks, counters): a camera must never sit inside one
    S.staticBoxes = [];
    S.set?.traverse(n => { if (!n.isMesh || !n.visible || n.name === 'outline' || isThin(n)) return; const bb = new THREE.Box3().setFromObject(n); const sz = bb.getSize(V());
      if (Math.max(sz.x, sz.y, sz.z) > 50 || Math.min(sz.x, sz.y, sz.z) < 0.03) return; S.staticBoxes.push(bb); });
  }
  const evalTimes = c.noOcclusion ? [] : c.move === 'track' ? [t0 + span * 0.02, t0 + span * 0.5, t0 + span * 0.98] : [t0 + span * 0.25, t0 + span * 0.75];
  for (const ts of evalTimes) {
    evalAll(ts);
    const groups = groupsNow();
    let live = null; if (c.move === 'track') { const lb = regionFor(subs, size); if (!lb.isEmpty()) live = lb.getCenter(V()); }
    for (const r of cand) {
      if (r.dead) continue;
      const center = live || r.f.center, pos = center.clone().add(r.dir.clone().multiplyScalar(r.d)); if (pos.y < 0.2) pos.y = 0.2;
      let inside = null;
      for (const B of S.actors) { if (ignore.has(B.obj) || !B.obj.visible) continue; if (new THREE.Box3().setFromObject(B.obj).expandByScalar(0.25).containsPoint(pos)) { inside = 'inside ' + B.id; break; } }
      if (!inside) for (const bb of S.staticBoxes) if (bb.containsPoint(pos)) { inside = 'inside set geometry'; break; }
      if (inside) { r.dead = true; r.hidden = true; r.score += 100; r.why = inside; continue; }
      for (const g of groups) {
        const hit = g.probes.map(pr => blocked(pr.p.clone().addScaledVector(r.right, pr.u * g.halfW), pos, ignore));
        hit.forEach(h => { if (h != null) { r.near = r.near == null ? h : Math.min(r.near, h); r.score += 1; } });
        if (hit[0] != null) r.score += 2;
        const grid = g.probes.map((pr, i) => ({ ...pr, b: hit[i] != null })).filter(pr => pr.row != null);
        const col = u => grid.filter(pr => pr.u === u), up = grid.filter(pr => pr.row === 0);
        if (hit[0] != null || (up.length && up.every(pr => pr.b)) || [-1, 1].some(u => col(u).length && col(u).every(pr => pr.b)) || grid.filter(pr => pr.b).length >= 5) { r.hidden = true; r.why = 'hidden(near ' + (r.near ?? 0).toFixed(2) + ')'; }
      }
      const cl = clutterAt(pos, { center, up: r.f.up }, r.d, r.right); r.clutter = Math.max(r.clutter, cl); if (cl >= 3) { r.hidden = true; r.score += cl; r.why += ' clutter ' + cl; }
    }
  }
  if (c.debug) for (const r of cand) console.error(`[camdbg ${sc.id}@${t0.toFixed(2)}] yaw ${(r.yaw / D2R).toFixed(0)} el ${(r.el / D2R).toFixed(0)} d ${r.d.toFixed(2)} hidden ${r.hidden} score ${r.score} ${r.why}`);
  let best = cand.find(r => !r.hidden);
  let fovUse = fov;
  if (!best) {
    best = cand.reduce((a2, b2) => (b2.score < a2.score ? b2 : a2));
    elev = best.el;
    if (best.near != null && best.near > 0.55 * best.d && !best.dead) { // obstacle near the camera (wall, foreground): step in front of it, widen the lens
      const dNew = Math.max(0.6, best.near - 0.3); fovUse = Math.min(70, 2 * Math.atan(Math.tan(fov * D2R / 2) * best.d / dNew) / D2R); best.d = dNew;
      warn(`[${sc.id}] cam@${t0.toFixed(2)} (${size} ${[].concat(c.frame).join(',')}): view blocked near the camera, moved in (fov ${fovUse.toFixed(0)})`);
    } else warn(`[${sc.id}] cam@${t0.toFixed(2)} (${size} ${[].concat(c.frame).join(',')}): no clear angle, least-occluded view used (score ${best.score}${best.dead ? ', INSIDE GEOMETRY' : ''})`);
  } else { elev = best.el; if (Math.abs(wrapA(best.yaw - baseYaw)) > 0.6) warn(`[${sc.id}] cam@${t0.toFixed(2)}: angle changed by ${(wrapA(best.yaw - baseYaw) / D2R).toFixed(0)}° to avoid occlusion`); }
  const sol = { kind: c.move === 'track' ? 'track' : 'frame', yaw: best.yaw, elev, d: best.d, center: best.f.center, up: best.f.up, fov: fovUse, size, subs, samples };
  // lint: back to camera on tight shots / subject outside frame
  if (['ecu', 'cu', 'mcu', 'ms'].includes(size) && !c.allowBack) for (const s of subs) if (!s.point && s.kind !== 'prop') {
    const f = facingOf(s, t0 + span * 0.5), rel = Math.abs(wrapA(best.yaw - f));
    if (rel > 1.9) warn(`[${sc.id}] cam@${t0.toFixed(2)}: ${s.id} has its back to the camera (${(rel / D2R).toFixed(0)}°)`);
  }
  return sol;
}
function camPoseAt(c, t) {
  const s = c.sol, span = Math.max(0.01, c.t1 - c.t0), k = (ease[c.ease || 'inOut'] || ease.inOut)(clamp01((t - c.t0) / span));
  if (s.kind === 'explicit') return { pos: s.pos0.clone().lerp(s.pos1, k), look: s.look0.clone().lerp(s.look1, k), fov: s.fov };
  if (s.kind === 'ots' || s.kind === 'pov') {
    const [aId, bId, sideIn] = s.spec; const A = S.actorById[aId], B = S.actorById[bId];
    if (!A || !B) return { pos: V(0, 1.6, 5), look: V(0, 1.2, 0), fov: 40 };
    const ha = headBox(A)?.getCenter(V()) || A.obj.position.clone().add(V(0, 1.7, 0));
    const hb = headBox(B)?.getCenter(V()) || B.obj.position.clone().add(V(0, 1.7, 0));
    const fwd = hb.clone().sub(ha); fwd.y = 0; fwd.normalize(); const right = V(fwd.z, 0, -fwd.x);
    const sa = A.obj.scale.x || 1, side = sideIn ?? 1;
    if (s.kind === 'pov') return { pos: ha.clone().add(fwd.clone().multiplyScalar(0.18 * sa)), look: hb.clone().add(V(0, -0.05, 0)), fov: s.fov };
    // Vertical OTS composed on screen: A's head big at the frame edge (x = -0.84·side), B's face right of centre (x = +0.24·side).
    // Solve the lateral offset so the two heads are exactly that far apart in angle, whatever their distance.
    const tanH = Math.tan(s.fov * D2R / 2) * (S.W / S.H), tanV = Math.tan(s.fov * D2R / 2);
    const angA = Math.atan(0.84 * tanH), angB = Math.atan(0.24 * tanH), sep = angA + angB;
    const D = Math.hypot(hb.x - ha.x, hb.z - ha.z), back = 1.0 * sa;
    let lo = 0, hi = 4; for (let i = 0; i < 32; i++) { const m = (lo + hi) / 2; if (Math.atan(m / back) - Math.atan(m / (back + D)) < sep) lo = m; else hi = m; }
    const sr = V(-fwd.z, 0, fwd.x); // screen-right when looking from A to B
    const pos0 = ha.clone().addScaledVector(fwd, -back).addScaledVector(sr, lo * side).add(V(0, 0.1 * sa, 0));
    const pos = pos0.lerp(pos0.clone().lerp(hb, 0.12), (c.move === 'push' ? k : 0));
    const toB = hb.clone().sub(pos), dist = Math.hypot(toB.x, toB.z);
    const yawL = Math.atan2(toB.x, toB.z) + angB * side;
    const look = pos.clone().add(V(Math.sin(yawL) * dist, 0, Math.cos(yawL) * dist)); look.y = hb.y - 0.16 * tanV * dist;
    return { pos, look, fov: s.fov };
  }
  let yaw = s.yaw, elev = s.elev, d = s.d, center = s.center.clone();
  const amt = c.amount ?? (c.move === 'orbit' ? 20 : c.move === 'crane' ? 12 : ['ecu', 'cu'].includes(s.size) ? 0.06 : 0.1);
  if (c.move === 'push') d *= 1 - amt * k; else if (c.move === 'pull') d *= 1 - amt * (1 - k);
  else if (c.move === 'orbit') yaw += amt * D2R * k; else if (c.move === 'crane') elev += amt * D2R * k;
  if (s.kind === 'track') { // follow the subject's live region (deterministic: recomputed at this frame)
    withProps = !!c.withProps; const b = regionFor(s.subs, s.size); if (!b.isEmpty()) center = b.getCenter(V());
  }
  const { dir, right } = camBasis(yaw, elev);
  const tanV = Math.tan(s.fov * D2R / 2), vis = 2 * d * tanV;
  const compose = c.compose ?? ({ ecu: 0.1, cu: 0.0, mcu: 0.02, ms: 0.04, mls: 0.05, fs: 0.04, ws: 0.03, ews: 0.03 }[s.size] ?? 0.04);
  const look = center.clone().add(V(0, -compose * vis, 0)).add(right.clone().multiplyScalar(-(c.offsetX || 0) * 0.25 * vis * (S.W / S.H)));
  const pos = center.clone().add(dir.multiplyScalar(d)); if (pos.y < 0.15) pos.y = 0.15;
  return { pos, look, fov: s.fov };
}
function placeCamera(t) {
  const cam = S.stage.camera;
  if (!S.cams.length) { S.curCam = null; cam.position.set(0, 1.6, 6); cam.lookAt(0, 1.2, 0); return; }
  let i = 0; for (let j = 0; j < S.cams.length; j++) if (S.cams[j].t0 <= t) i = j;
  const c = S.cams[i]; S.curCam = c;
  let p = camPoseAt(c, t);
  if (c.cut === false && i > 0) {
    const q = camPoseAt(S.cams[i - 1], c.t0), w = ease.inOut(clamp01((t - c.t0) / (c.glide ?? 0.8)));
    p = { pos: q.pos.clone().lerp(p.pos, w), look: q.look.clone().lerp(p.look, w), fov: lerp(q.fov, p.fov, w) };
  }
  const sc_ = S.sc;
  if (sc_.camDolly || sc_.camTruck || sc_.camPed || sc_.camPan || sc_.camTilt) {   // per-scene framing trims (A/B sweeps): dolly factor, truck/ped (m), pan/tilt (deg)
    const pos = p.pos.clone(), look = p.look.clone(), fwd = look.clone().sub(pos), right = new THREE.Vector3().crossVectors(fwd, new THREE.Vector3(0, 1, 0)).normalize();
    if (sc_.camDolly) { const off = pos.clone().sub(look).multiplyScalar(sc_.camDolly); pos.copy(look).add(off); }
    if (sc_.camTruck) { pos.addScaledVector(right, sc_.camTruck); look.addScaledVector(right, sc_.camTruck); }
    if (sc_.camPed) { pos.y += sc_.camPed; look.y += sc_.camPed; }
    const d = look.clone().sub(pos), L = d.length();
    if (sc_.camPan) look.addScaledVector(right, -Math.tan(sc_.camPan * D2R) * L);   // + pans left
    if (sc_.camTilt) look.y += Math.tan(sc_.camTilt * D2R) * L;                     // + tilts up
    p = { pos, look, fov: p.fov };
  }
  cam.position.copy(p.pos); cam.fov = p.fov; cam.aspect = S.W / S.H; cam.updateProjectionMatrix();
  cam.up.set(0, 1, 0); cam.lookAt(p.look);
  if (c.roll) cam.rotateZ(c.roll * D2R);
  if (c.whip) { const w = 1 - clamp01((t - c.t0) / 0.16); cam.rotateY(w * w * 0.8 * (c.whip === 'left' ? -1 : 1)); }
  let shake = c.shake || 0;
  for (const f of S.sc.fx || []) if (f.type === 'shake') { const a = T(f.at, S.sc); if (t >= a && t < a + (f.dur || 0.3)) shake += (f.amount || 0.03) * (1 - (t - a) / (f.dur || 0.3)); }
  if (shake) { cam.position.x += Math.sin(t * 71) * shake; cam.position.y += Math.cos(t * 53) * shake; }
}

// ------------------------------------------------------------------------------------- frame
export function renderFrame(tAbs) {
  if (!S) throw new Error('load() first');
  const t = Math.min(tAbs, S.total - 1e-4);
  let si = S.script.scenes.findIndex(sc => t >= sc.start && t < sc.start + sc.duration); if (si < 0) si = S.script.scenes.length - 1;
  if (si !== S.scene) setupScene(si);
  const sc = S.sc, lt = t - sc.start;
  const { renderer, scene, camera } = S.stage;
  const g = S.ctx;
  // camera/subject motion blur: sc.blur = shutter seconds, or [[t0, t1, shutter], ...] windows in scene time; K sub-frames averaged
  let shutter = 0; if (typeof sc.blur === 'number') shutter = sc.blur; else if (Array.isArray(sc.blur)) for (const [a, b, sh] of sc.blur) if (lt >= a && lt < b) shutter = sh;
  const K = shutter > 0 ? (sc.blurSamples || 5) : 1;
  for (let k = 0; k < K; k++) {
    const tk = K > 1 ? Math.max(0, lt - shutter * (K - 1 - k) / (K - 1)) : lt;
    evalAll(tk);
    lightCycle(tk);
    placeCamera(tk);
    if (sc.fogTo && scene.fog && sc.fog) { const u = Math.min(1, Math.max(0, tk / sc.duration)); scene.fog.near = sc.fog.near + (sc.fogTo.near - sc.fog.near) * u; scene.fog.far = sc.fog.far + (sc.fogTo.far - sc.fog.far) * u; }   // sc.fogTo: the veil follows a descending camera
    for (const o of S.follow || []) o.position.copy(camera.position);
    camLocked(camera);
    if (S.look) S.look.render(); else renderer.render(scene, camera);
    const frozen = frozenNow(tk);
    g.globalAlpha = 1 / (k + 1);
    g.filter = (S.curCam?.grade ?? S.sc.grade ?? S.script.grade ?? (S.look ? 'none' : GRADE)) + (frozen ? ' saturate(0.4) hue-rotate(-10deg) brightness(1.03)' : '') + (S.sc.soften ? ` blur(${S.sc.soften}px)` : '');   // sc.soften: match the reference's softness (px)
    g.drawImage(renderer.domElement, 0, 0, S.W, S.H);
  }
  g.globalAlpha = 1; g.filter = 'none';
  drawFX(g, lt);
  drawCaption(g, t);
  return si;
}
// props with cfg.camLock live in camera space (x right, y up, looking down -z): their pos, keys and rot are evaluated as usual, then
// carried by the camera (shake included). For screen-locked layers in 3D: a cloud bank sliding across the frame, a lens-close foreground.
const _q = new THREE.Quaternion();
function camLocked(camera) {
  let any = false;
  for (const Pp of S.props) { if (!Pp.cfg.camLock) continue; if (!any) { camera.updateMatrixWorld(true); any = true; }
    const o = Pp.obj; _q.setFromEuler(o.rotation); o.position.applyMatrix4(camera.matrixWorld); o.quaternion.copy(camera.quaternion).multiply(_q); o.updateMatrixWorld(true); }
}
function lightCycle(t) {
  const dn = S.sc.daynight; if (!dn) return;
  // k: 0 = day, 1 = night. Default: day/night cycles from `from`; once: falls to night and stays; rise: night until `from`, then day
  const t0 = T(dn.from, S.sc), P0 = dn.period || 1.2, u = (t - t0) / P0; let k;
  if (dn.rise) k = t < t0 ? 1 : u >= 0.5 ? 0 : 0.5 + 0.5 * Math.cos(u * 2 * Math.PI);
  else { if (t < t0) return; k = dn.once && u >= 0.5 ? 1 : 0.5 - 0.5 * Math.cos(u * 2 * Math.PI); }
  S.lights.hemi.intensity = lerp(S.lightBase.hemi, 0.7, k); S.lights.key.intensity = lerp(S.lightBase.key, 0.25, k);
  S.stage.scene.background = S.lightBase.bg.clone().lerp(new THREE.Color(P.skyNight), k);
  if (S.skyDome) S.skyDome.material.color.set('#FFFFFF').lerp(new THREE.Color('#1A2238'), k);
}
function drawFX(g, t) {
  const W = S.W, H = S.H;
  const grd = g.createRadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 0.75);
  grd.addColorStop(0, 'rgba(0,0,0,0)'); grd.addColorStop(1, 'rgba(20,15,10,0.22)'); g.fillStyle = grd; g.fillRect(0, 0, W, H);
  for (const f of S.sc.fx || []) {
    const a = T(f.at, S.sc), d = f.dur || 0.3, k = (t - a) / d; if (k < 0 || k > 1) continue;
    if (f.type === 'flash') { g.fillStyle = `rgba(255,255,255,${(1 - k) * 0.85})`; g.fillRect(0, 0, W, H); }
    if (f.type === 'fadeIn') { g.fillStyle = `rgba(0,0,0,${1 - k})`; g.fillRect(0, 0, W, H); }
    if (f.type === 'fadeBlack') { g.fillStyle = `rgba(0,0,0,${k})`; g.fillRect(0, 0, W, H); }
  }
}

// ------------------------------------------------------------------------------------- captions
const FUNCTION_WORDS = new Set(['le', 'la', 'les', 'l', 'un', 'une', 'des', 'du', 'de', 'd', 'sa', 'son', 'ses', 'mon', 'ma', 'mes', 'ton', 'ta', 'tes', 'leur', 'leurs', 'ce', 'cet', 'cette', 'ces', 'au', 'aux', 'a', 'et', 'ou', 'en', 'pour', 'par', 'sur', 'dans', 'avec', 'sans', 'qui', 'que', 'qu', 'il', 'elle', 'on', 'ils', 'se', 's', 'ne', 'n', 'plus', 'tres', 'trop', 'je', 'j', 'vous', 'nous', 'tu', 'me', 'm', 't', 'c', 'y']);
function chunk(l, sc) {
  const words = (l.words || []).map(w => ({ ...w }));
  if (!words.length) return [];
  if (l.speaker) { words[0].w = '« ' + words[0].w; words[words.length - 1].w += ' »'; }
  const maxW = S.script.captionWords || 3, chunks = []; let cur = [];
  words.forEach((w, i) => {
    cur.push(w);
    const dangling = FUNCTION_WORDS.has(normW(w.w.replace(/[«»]/g, ''))) && i < words.length - 1 && cur.length < maxW + 2;
    const end = /[.,!?;:…»]$/.test(w.w) || (cur.length >= maxW && !dangling) || i === words.length - 1;
    if (end) { chunks.push({ words: cur, s: cur[0].s, e: words[i + 1] ? words[i + 1].s : l.end + 0.15 }); cur = []; }
  });
  return chunks;
}
function drawCaption(g, t) {
  if (S.script.captions === false) return;
  let ch = null, line = null;
  for (const l of S.lines) for (const c of l.chunks) if (t >= c.s && t < c.e) { ch = c; line = l; }
  if (!ch) return;
  const W = S.W, H = S.H, hl = new Set((line.highlight || []).map(normW));
  const fs = Math.round(W * (S.script.captionSize || 0.058)), maxW = W * 0.7, cx = W * 0.47;
  g.save(); g.font = `800 ${fs}px "Arial Black", Arial, sans-serif`; g.textBaseline = 'middle';
  const parts = ch.words.map(w => w.w), rows = [[]]; let lw = 0;
  for (const p of parts) { const pw = g.measureText(p + ' ').width; if (lw + pw > maxW && rows[rows.length - 1].length) { rows.push([]); lw = 0; } rows[rows.length - 1].push(p); lw += pw; }
  const y0 = H * (S.script.captionY ?? 0.66) - (rows.length - 1) * fs * 0.6;
  rows.forEach((row, ri) => {
    const tw = g.measureText(row.join(' ')).width; let x = cx - tw / 2; const y = y0 + ri * fs * 1.2;
    for (const p of row) {
      const isHl = hl.has(normW(p));
      g.lineJoin = 'round'; g.lineWidth = fs * 0.2; g.strokeStyle = 'rgba(25,20,18,0.92)'; g.strokeText(p, x, y);
      g.fillStyle = isHl ? (S.script.highlightColor || P.salmon) : '#FFFFFF'; g.fillText(p, x, y);
      x += g.measureText(p + ' ').width;
    }
  });
  g.restore();
}

// ------------------------------------------------------------------------------------- events / QA
function collectEvents(sc) {
  const T0 = sc.start;
  for (const A of S.actors) {
    for (const e of A.sfx) S.events.push({ t: T0 + e.t, name: e.name, vol: e.vol, src: A.id });
    const h = (A.obj.userData.height || 1.9) * A.scale0;
    if (A.kind === 'creature' && !A.obj.userData.upright) continue;
    for (const mv of A.moves) if (mv.freq && LOCO[mv.clip]) {
      const heavy = h > 2.6, name = mv.clip === 'run' || mv.clip === 'flee' || mv.clip === 'flail' ? 'stepRun' : heavy ? 'stepHeavy' : mv.clip === 'tiptoe' || mv.clip === 'boxSneak' || mv.clip === 'sneak' ? 'stepSoft' : 'step';
      for (let k = 0; ; k++) { const te = mv.t + (0.25 + 0.5 * k) / mv.freq; if (te > mv.t1) break;
        let ts = te; if (S.freezeAt != null && !S.freezeExcept.has(A.id) && te > S.freezeAt) { if (!isFinite(S.freezeUntil)) break; ts = te + (S.freezeUntil - S.freezeAt); }
        S.events.push({ t: T0 + ts, name, vol: heavy ? 0.5 : 0.28, src: A.id }); }
    }
  }
  for (const Pp of S.props) for (const e of Pp.sfx) S.events.push({ t: T0 + e.t, name: e.name, vol: e.vol, src: Pp.id });
  for (const e of sc.sfx || []) { const { at, ...rest } = e; S.events.push({ ...rest, t: T0 + T(at ?? 0, sc), vol: e.vol ?? 0.5, src: 'scene', ...(e.until != null ? { dur: T(e.until, sc) - T(at ?? 0, sc) } : {}) }); }
  for (const c of S.cams) S.camTimes.push({ t: T0 + (c.t0 + c.t1) / 2, scene: sc.id, size: c.size || (c.ots ? 'ots' : c.pov ? 'pov' : 'explicit'), frame: [].concat(c.frame || c.ots || c.pov || []).join(',') });
}
export function frameDataURL(type = 'image/jpeg', q = 0.92) { return S.out.toDataURL(type, q); }
export function warnings() { return S.warnings; }
export function events() { return S.events; }
export function cams() { return S.camTimes; }
// analysis entry point used by render.mjs: builds every scene once to collect events, camera list and warnings
export async function analyze() { S.camTimes = []; S.events = []; S.warnings = []; for (let i = 0; i < S.script.scenes.length; i++) setupScene(i, true); S.scene = -1; return { warnings: S.warnings, events: S.events, cams: S.camTimes }; }
export function _S() { return S; }

// ------------------------------------------------------------------------------------- scene export (Tesseract test)
// The posed scene at time t as a binary glTF (metres, Y up) + the camera, for a path-traced comparison in Tesseract Scene3D.
// Ink outlines, the sky dome, sprites, particles and lights are left out; instances are expanded (Tesseract does not read
// EXT_mesh_gpu_instancing); every material becomes a rough non-metal MeshStandardMaterial (lit), screens and bubbles stay emissive.
export async function exportSceneGLB(tAbs, opts = {}) {
  renderFrame(tAbs);
  const { GLTFExporter } = await import('three/addons/exporters/GLTFExporter.js');
  const { mergeGeometries } = await import('three/addons/utils/BufferGeometryUtils.js');
  const root = S.root, cam = S.stage.camera; root.updateMatrixWorld(true);
  const kill = []; root.traverse(n => { const m = n.material;
    if (n.name === 'outline' || n.isSprite || n.isPoints || n.isLine || n.isLight || !n.visible || (n.isMesh && n.renderOrder === -10 && m?.side === THREE.BackSide)) kill.push(n); });
  kill.forEach(n => n.parent?.remove(n));
  const inst = []; root.traverse(n => { if (n.isInstancedMesh) inst.push(n); });
  for (const im of inst) { const g = new THREE.Group(); g.position.copy(im.position); g.quaternion.copy(im.quaternion); g.scale.copy(im.scale); const m4 = new THREE.Matrix4(), c = new THREE.Color();
    for (let i = 0; i < im.count; i++) { im.getMatrixAt(i, m4); const mm = new THREE.Mesh(im.geometry, im.material); if (im.instanceColor) { im.getColorAt(i, c); mm.material = im.material.clone(); mm.material.color?.multiply(c); } mm.applyMatrix4(m4); g.add(mm); }
    im.parent.add(g); im.parent.remove(im); }
  const conv = new Map(), cl = c => new THREE.Color(Math.min(1, c.r), Math.min(1, c.g), Math.min(1, c.b));
  root.traverse(n => { if (!n.isMesh) return; const one = m => { if (!m) return m; if (conv.has(m)) return conv.get(m);
      const glowing = m.isMeshBasicMaterial && m.toneMapped === false, em = m.emissive && (m.emissive.r + m.emissive.g + m.emissive.b) > 0.02;
      const s = new THREE.MeshStandardMaterial({ color: m.color ? cl(m.color) : new THREE.Color(1, 1, 1), map: m.map || null, roughness: 0.92, metalness: 0, transparent: !!m.transparent, opacity: m.opacity ?? 1, alphaTest: m.alphaTest || 0, side: m.side ?? THREE.FrontSide });
      if (glowing) { s.emissive = new THREE.Color(1, 1, 1); s.emissiveMap = m.map || null; s.color.setRGB(0, 0, 0); }
      else if (em) { s.emissive = cl(m.emissive); s.emissiveMap = m.emissiveMap || null; }
      conv.set(m, s); return s; };
    n.material = Array.isArray(n.material) ? n.material.map(one) : one(n.material); });
  let out = root;
  if (opts.merge) {   // one mesh per material (world transforms baked): a handful of draw calls instead of thousands
    root.updateMatrixWorld(true); const groups = new Map();
    root.traverse(n => { if (!n.isMesh || Array.isArray(n.material)) return; const g = n.geometry.index ? n.geometry.toNonIndexed() : n.geometry.clone(); g.applyMatrix4(n.matrixWorld);
      for (const k of Object.keys(g.attributes)) if (!['position', 'normal', 'uv'].includes(k)) g.deleteAttribute(k);
      if (!g.attributes.normal) g.computeVertexNormals(); if (!g.attributes.uv) g.setAttribute('uv', new THREE.Float32BufferAttribute(new Float32Array(g.attributes.position.count * 2), 2));
      (groups.get(n.material) || groups.set(n.material, []).get(n.material)).push(g); });
    out = new THREE.Group(); for (const [m, gs] of groups) { const mg = mergeGeometries(gs, false); if (mg) out.add(new THREE.Mesh(mg, m)); }
  }
  const buf = await new GLTFExporter().parseAsync(out, { binary: true, onlyVisible: true, maxTextureSize: opts.maxTex || 1024 });
  let bin = ''; const u8 = new Uint8Array(buf); for (let i = 0; i < u8.length; i += 0x8000) bin += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
  const dir = new THREE.Vector3(); cam.getWorldDirection(dir);
  return { glb: btoa(bin), camera: { position: cam.position.toArray(), direction: dir.toArray(), fov: cam.fov, aspect: cam.aspect },
           sun: S.lights?.key ? { direction: S.lights.key.position.clone().sub(S.lights.key.target.position).normalize().toArray(), intensity: S.lights.key.intensity, color: '#' + S.lights.key.color.getHexString() } : null,
           sky: '#' + (S.stage.scene.background?.getHexString?.() || 'a7d4ec') };
}

// One shot with its motion baked into glTF, for rendering in Tesseract: transforms sampled at `fps` over the shot (scene time),
// static meshes merged by material, every moving mesh flattened to the root with world-space position/quaternion/scale tracks
// (scale ~0 while hidden), a mesh whose texture changes (faces: expressions, blinks, lip flaps) split into one mesh per texture
// shown by a stepped scale track; instanced meshes expanded per instance. Returns the GLB (base64) + per-frame camera, the sun, the sky.
function poseAt(tAbs) {
  const t = Math.min(tAbs, S.total - 1e-4);
  let si = S.script.scenes.findIndex(sc => t >= sc.start && t < sc.start + sc.duration); if (si < 0) si = S.script.scenes.length - 1;
  if (si !== S.scene) setupScene(si);
  const lt = t - S.sc.start; evalAll(lt); lightCycle(lt); placeCamera(lt);
  for (const o of S.follow || []) o.position.copy(S.stage.camera.position);
  camLocked(S.stage.camera); S.root.updateMatrixWorld(true); S.stage.camera.updateMatrixWorld(true);
}
export async function exportShotGLB(si, { fps = 15, maxTex = 1024 } = {}) {
  const { GLTFExporter } = await import('three/addons/exporters/GLTFExporter.js');
  const { mergeGeometries } = await import('three/addons/utils/BufferGeometryUtils.js');
  const sc = S.script.scenes[si], n = Math.max(2, Math.round(sc.duration * fps) + 1), times = [...Array(n)].map((_, f) => Math.min(f / fps, sc.duration - 1e-3));
  poseAt(sc.start + 1e-4);
  const skip = o => o.name === 'outline' || o.isSprite || o.isPoints || o.isLine || o.isLight || (o.isMesh && o.renderOrder === -10 && o.material?.side === THREE.BackSide);
  const shown = o => { for (let p = o; p; p = p.parent) if (!p.visible) return false; return true; };
  const items = []; S.root.traverse(o => { if (skip(o)) return; if (o.isInstancedMesh) for (let i = 0; i < o.count; i++) items.push({ o, i });
    else if (o.isMesh && Array.isArray(o.material)) (o.geometry.groups.length ? o.geometry.groups : [{ start: 0, count: Infinity, materialIndex: 0 }]).forEach(g => items.push({ o, g }));   // heads: one box, six materials (the face is one of them)
    else if (o.isMesh) items.push({ o }); });
  const matOf = it => it.g ? it.o.material[it.g.materialIndex] : it.o.material;
  const m4 = new THREE.Matrix4(), cam = S.stage.camera, dir = new THREE.Vector3(), camS = [];
  for (const it of items) { it.M = []; it.vis = []; it.map = []; }
  for (let f = 0; f < n; f++) {
    poseAt(sc.start + times[f]);
    for (const it of items) { const o = it.o; if (it.i != null) { o.getMatrixAt(it.i, m4); it.M.push(o.matrixWorld.clone().multiply(m4)); } else it.M.push(o.matrixWorld.clone()); it.vis.push(shown(o) && !skip(o)); it.map.push(it.i == null ? (matOf(it)?.map || null) : null); }
    cam.getWorldDirection(dir); camS.push({ p: cam.position.toArray(), d: dir.toArray(), fov: cam.fov });
  }
  const conv = new Map(), cl = c => new THREE.Color(Math.min(1, c.r), Math.min(1, c.g), Math.min(1, c.b));
  const toStd = (m, map) => { const key = m.uuid + '|' + (map?.uuid || ''); if (conv.has(key)) return conv.get(key);
    const glowing = m.isMeshBasicMaterial && m.toneMapped === false, em = m.emissive && (m.emissive.r + m.emissive.g + m.emissive.b) > 0.02;
    const s = new THREE.MeshStandardMaterial({ color: m.color ? cl(m.color) : new THREE.Color(1, 1, 1), map: map ?? m.map ?? null, roughness: 0.92, metalness: 0, transparent: !!m.transparent, opacity: m.opacity ?? 1, alphaTest: m.alphaTest || 0, side: m.side ?? THREE.FrontSide });
    if (glowing) { s.emissive = new THREE.Color(1, 1, 1); s.emissiveMap = map ?? m.map ?? null; s.color.setRGB(0, 0, 0); } else if (em) { s.emissive = cl(m.emissive); s.emissiveMap = m.emissiveMap || null; }
    conv.set(key, s); return s; };
  const out = new THREE.Group(); out.name = 'shot'; const groups = new Map(), tracks = [], P = new THREE.Vector3(), Q = new THREE.Quaternion(), Sc = new THREE.Vector3(); let id = 0;
  const geoOf = (o, grp) => { let g = o.geometry.index ? o.geometry.toNonIndexed() : o.geometry.clone();
    if (grp) { const a = grp.start, b = Math.min(grp.start + grp.count, g.attributes.position.count), sub = new THREE.BufferGeometry(); for (const k of Object.keys(g.attributes)) { const at = g.attributes[k]; sub.setAttribute(k, new THREE.BufferAttribute(at.array.slice(a * at.itemSize, b * at.itemSize), at.itemSize)); } g = sub; }
    g.clearGroups(); for (const k of Object.keys(g.attributes)) if (!['position', 'normal', 'uv'].includes(k)) g.deleteAttribute(k);
    if (!g.attributes.normal) g.computeVertexNormals(); if (!g.attributes.uv) g.setAttribute('uv', new THREE.Float32BufferAttribute(new Float32Array(g.attributes.position.count * 2), 2)); return g; };
  for (const it of items) {
    const o = it.o, om = matOf(it); if (!it.vis.some(Boolean) || !om || Array.isArray(om)) continue;
    const maps = [...new Set(it.map)], still = it.M.every(M => M.equals(it.M[0])) && it.vis.every(Boolean) && maps.length === 1;
    if (still) { const g = geoOf(o, it.g); g.applyMatrix4(it.M[0]); const mat = toStd(om, maps[0]); (groups.get(mat) || groups.set(mat, []).get(mat)).push(g); continue; }
    for (const mp of maps) {   // one mesh per texture it shows during the shot
      const mesh = new THREE.Mesh(geoOf(o, it.g), toStd(om, mp)); mesh.name = 'a' + (id++); out.add(mesh);
      const pv = [], qv = [], sv = [];
      let Qp = new THREE.Quaternion(); it.M.forEach((M, f) => { M.decompose(P, Q, Sc); const ql = Q.length(); if (!(ql > 1e-6) || !isFinite(ql)) Q.copy(Qp); else Q.normalize(); if (Qp.dot(Q) < 0) Q.set(-Q.x, -Q.y, -Q.z, -Q.w); Qp.copy(Q); const on = it.vis[f] && it.map[f] === mp, k = on ? 1 : 1e-4; pv.push(P.x, P.y, P.z); qv.push(Q.x, Q.y, Q.z, Q.w); sv.push(Sc.x * k, Sc.y * k, Sc.z * k); });
      tracks.push(new THREE.VectorKeyframeTrack(mesh.name + '.position', times, pv), new THREE.QuaternionKeyframeTrack(mesh.name + '.quaternion', times, qv),
        new THREE.VectorKeyframeTrack(mesh.name + '.scale', times, sv, maps.length > 1 || !it.vis.every(Boolean) ? THREE.InterpolateDiscrete : THREE.InterpolateLinear));
    }
  }
  for (const [m, gs] of groups) { const mg = mergeGeometries(gs, false); if (mg) { const mm = new THREE.Mesh(mg, m); mm.name = 's' + (id++); out.add(mm); } }
  const clip = new THREE.AnimationClip('shot', times[n - 1], tracks);
  const buf = await new GLTFExporter().parseAsync(out, { binary: true, animations: tracks.length ? [clip] : [], onlyVisible: false, maxTextureSize: maxTex });
  let bin = ''; const u8 = new Uint8Array(buf); for (let i = 0; i < u8.length; i += 0x8000) bin += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
  return { glb: btoa(bin), id: sc.id, start: sc.start, duration: sc.duration, fps, times, camera: camS, aspect: cam.aspect, animated: tracks.length / 3,
           sun: S.lights?.key ? { direction: S.lights.key.position.clone().sub(S.lights.key.target.position).normalize().toArray(), intensity: S.lights.key.intensity, color: '#' + S.lights.key.color.getHexString() } : null,
           indoor: S.look ? !S.look.outdoor : false, sky: '#' + (S.stage.scene.background?.getHexString?.() || 'a7d4ec') };
}
