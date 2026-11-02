// Director: turns a timed JSON script into deterministic frames.
//   load(script) -> builds cast; renderFrame(t) -> draws WebGL + caption overlay into one canvas.
// Grammar copied from the source shorts:
//   * one narration chunk per shot, a cut every ~1–2.5 s
//   * slow push-ins, deadpan close-ups after every absurd beat, occasional whip-pan
//   * burned-in captions: 2–4 words, white bold w/ dark outline, key nouns in salmon
import * as THREE from 'three';
import { createStage, setLighting } from './scene.js';
import { buildHuman } from './human.js';
import { samplePose, blendPoses, actingBlend, applyPose } from './animations.js';
import { ease, clamp01, lerp, rng, PALETTE as P } from './style.js';

const opt = async (p) => { try { return await import(p); } catch (e) { console.warn('[director] optional module missing', p, e.message); return null; } };
const Props = await opt('/engine/props.js');
const Sets = await opt('/engine/sets.js');
const Creatures = await opt('/engine/creatures.js');

let S = null; // state

export async function load(script, { width, height } = {}) {
  const W = width || script.width || 720, H = height || script.height || 1280;
  const stage = createStage(W, H);
  stage.renderer.domElement.style.display = 'none';
  const out = document.createElement('canvas'); out.width = W; out.height = H; out.id = 'film'; document.body.appendChild(out);
  // timeline
  let t0 = 0;
  const shots = script.shots.map((s, i) => { const d = s.duration ?? estimateDuration(s); const r = { ...s, index: i, start: t0, duration: d }; t0 += d; return r; });
  S = { script, shots, total: t0, W, H, stage, out, ctx: out.getContext('2d'), cast: {}, currentShot: -1, shotObjects: [] };
  for (const [id, c] of Object.entries(script.cast || {})) S.cast[id] = buildActor(c);
  await document.fonts?.ready;
  return { duration: t0, shots: shots.map(s => ({ start: s.start, duration: s.duration })) };
}

function estimateDuration(s) { // fallback when no TTS timing: ~3.3 words/s like the source narrator
  const words = (s.line || '').split(/\s+/).filter(Boolean).length;
  return Math.max(1.1, words / 3.3 + 0.35) + (s.hold || 0);
}

function buildActor(c) {
  if (!c || c.type === 'human' || c.preset) return buildHuman(c.preset ? c : { preset: 'lemec', ...c });
  if (c.type === 'creature' && Creatures) return Creatures.buildCreature(c.name, c.opts || {});
  if (c.type === 'prop' && Props) return Props.buildProp(c.name, c.opts || {});
  const g = new THREE.Group(); g.userData.kind = 'placeholder'; return g;
}

function setupShot(shot) {
  const { scene } = S.stage;
  for (const o of S.shotObjects) { o.parent?.remove(o); }
  S.shotObjects = [];
  // detach actors from scene + props from hands
  for (const a of Object.values(S.cast)) { a.parent?.remove(a); a.traverse(n => { if (n.userData.attachedProp) { n.remove(n.userData.attachedProp); n.userData.attachedProp = null; } }); }
  const setName = shot.set || S.lastSet || 'whiteVoid'; S.lastSet = setName;
  let set = null;
  if (Sets) { try { set = Sets.buildSet(setName, shot.setOpts || {}); } catch (e) { console.warn('set failed', setName, e.message); } }
  if (!set) { set = new THREE.Group(); const f = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), new THREE.MeshLambertMaterial({ color: P.cream })); f.rotation.x = -Math.PI / 2; f.receiveShadow = true; set.add(f); set.userData.lighting = 'interior'; }
  scene.add(set); S.shotObjects.push(set); S.set = set;
  setLighting(scene, shot.lighting || set.userData.lighting || 'day');
  // actors
  S.actorsInShot = (shot.actors || []).map(a => {
    const obj = S.cast[a.id] || (S.cast[a.id] = buildActor(a.spec || { preset: 'lemec' }));
    scene.add(obj);
    if (a.hold) attachProp(obj, a.hold);
    return { cfg: a, obj };
  });
  // props
  S.propsInShot = (shot.props || []).map(p => {
    let obj = Props ? Props.buildProp(p.name, p.opts || {}) : new THREE.Group();
    scene.add(obj); S.shotObjects.push(obj); return { cfg: p, obj };
  });
  // extra one-off creatures / humans (crowds: e.g. 12 cops)
  for (const cr of shot.crowd || []) {
    const r = rng(cr.seed || 11);
    for (let i = 0; i < (cr.count || 5); i++) {
      const obj = buildActor(cr.spec || { preset: 'cop' });
      const ang = (cr.ring ? i / cr.count * Math.PI * 2 : 0);
      const pos = cr.ring ? [cr.center[0] + Math.cos(ang) * cr.ring, 0, cr.center[2] + Math.sin(ang) * cr.ring] : [cr.center[0] + (r() - 0.5) * (cr.spread || 4), 0, cr.center[2] + (r() - 0.5) * (cr.spread || 4)];
      const ry = cr.ring ? Math.atan2(cr.center[0] - pos[0], cr.center[2] - pos[2]) : (cr.ry || 0);
      scene.add(obj); S.shotObjects.push(obj);
      S.actorsInShot.push({ cfg: { id: '_crowd' + i, pos, ry, clip: cr.clip || 'idle', phase: r() * 3, scale: cr.scale }, obj });
    }
  }
}

function attachProp(actor, hold) {
  if (!Props) return;
  const spec = typeof hold === 'string' ? { name: hold } : hold;
  const J = actor.userData.joints; const hand = J?.['hand' + (spec.hand || 'R')];
  if (!hand) return;
  const p = Props.buildProp(spec.name, spec.opts || {});
  const g = p.userData.grip || [0, 0, 0];
  p.position.set(-g[0], -0.1 - g[1], -g[2]);
  if (spec.rot) p.rotation.set(...spec.rot);
  if (spec.scale) p.scale.setScalar(spec.scale);
  hand.add(p); hand.userData.attachedProp = p;
}

// ---- per-frame evaluation -------------------------------------------------
function evalTrack(cfg, lt, dur) {
  // base placement with optional move (pos -> to) eased over [moveStart, moveEnd]
  const from = cfg.pos || [0, 0, 0];
  let x = from[0], y = from[1], z = from[2], ry = (cfg.ry || 0) * Math.PI / 180;
  if (cfg.to) {
    const ms = cfg.moveStart ?? 0, me = cfg.moveEnd ?? dur;
    const k = (ease[cfg.moveEase || 'linear'] || ease.linear)(clamp01((lt - ms) / Math.max(0.01, me - ms)));
    x = lerp(from[0], cfg.to[0], k); y = lerp(from[1], cfg.to[1] ?? from[1], k); z = lerp(from[2], cfg.to[2], k);
  }
  if (cfg.ryTo !== undefined) ry = lerp(ry, cfg.ryTo * Math.PI / 180, ease.inOut(clamp01(lt / dur)));
  let scale = cfg.scale || 1;
  if (cfg.scaleTo) scale = lerp(scale, cfg.scaleTo, (ease[cfg.scaleEase || 'inOut'])(clamp01((lt - (cfg.scaleStart || 0)) / ((cfg.scaleEnd ?? dur) - (cfg.scaleStart || 0)))));
  return { x, y, z, ry, scale };
}

function currentAction(cfg, lt) {
  // actions: [{at, clip, expr, params}] — the last one whose `at` <= lt wins; crossfade with previous
  const base = { at: 0, clip: cfg.clip || 'idle', expr: cfg.expr || 'neutral', params: cfg.params };
  const list = [base, ...(cfg.actions || [])].sort((a, b) => a.at - b.at);
  let cur = list[0], prev = null;
  for (const a of list) if (a.at <= lt) { prev = cur === a ? prev : cur; cur = a; }
  return { cur, prev: prev && prev !== cur ? prev : null };
}

function poseActor({ cfg, obj }, lt, dur, globalT) {
  const tr = evalTrack(cfg, lt, dur);
  const { cur, prev } = currentAction(cfg, lt);
  const ph = cfg.phase || 0;
  if (obj.userData.kind === 'human') {
    let pose = samplePose(cur.clip, lt - cur.at + ph, cur.params);
    if (prev) { // acting transition: anticipation → overshoot → settle, head leads, hands trail
      const dt = lt - cur.at;
      if (dt < 0.6) pose = cur.snap ? pose : actingBlend(samplePose(prev.clip, lt + ph, prev.params), pose, dt, { anticipation: cur.anticipation ?? 0.15, overshoot: cur.overshoot ?? 1.2 });
    }
    if (cfg.lookAt) { // turn head toward camera / point
      pose.head = pose.head || [0, 0, 0]; pose.head = [pose.head[0] + (cfg.lookAt[0] || 0), pose.head[1] + (cfg.lookAt[1] || 0), pose.head[2]];
    }
    applyPose(obj, pose, tr);
    // expression + automatic blinking + lip flap while "talk" is set
    // "every move starts with a look": the face changes ~4 frames before the body
    const ahead = currentAction(cfg, lt + 0.13).cur;
    let expr = (ahead.expr || cur.expr || cfg.expr || 'neutral');
    if (cfg.talk && expr === 'neutral' && Math.sin((globalT + ph) * 22) > 0.2) expr = 'talk';
    if ((expr === 'neutral' || expr === 'suspicious') && ((globalT + ph * 7) % 3.3) < 0.12) expr = 'blink';
    obj.userData.setExpression?.(expr);
  } else {
    obj.position.set(tr.x, tr.y, tr.z); obj.rotation.y = tr.ry; obj.scale.setScalar(tr.scale);
    obj.userData.animate?.(cur.clip, lt - cur.at + ph, cur.params || {});
    if (cur.expr) obj.userData.setExpression?.(cur.expr);
    obj.userData.update?.(globalT);
  }
  if (obj.userData.kind === 'human' && tr.scale !== 1) obj.scale.setScalar(tr.scale);
}

function targetPoint(target) {
  if (Array.isArray(target)) return new THREE.Vector3(...target);
  const a = S.actorsInShot.find(x => x.cfg.id === target) || S.actorsInShot[0];
  if (!a) return new THREE.Vector3(0, 1.2, 0);
  const h = (a.obj.userData.height || 1.9) * a.obj.scale.y;
  return new THREE.Vector3(a.obj.position.x, a.obj.position.y + h, a.obj.position.z);
}

// Framing presets measured from the source (portrait 9:16, slightly low, 3/4 angles).
const CAM = {
  extremeClose: { dist: 1.1, dy: -0.22, look: -0.27, fov: 38 },  // face fills frame (reaction beats)
  close:        { dist: 1.55, dy: -0.3, look: -0.38, fov: 38 },   // head + shoulders
  medium:       { dist: 2.7, dy: -0.55, look: -0.62, fov: 40 },   // waist up (default narration)
  full:         { dist: 4.4, dy: -0.75, look: -0.95, fov: 40 },   // whole body
  wide:         { dist: 8.5, dy: 0.6, look: -1.1, fov: 42 },      // establishing / big object
  extremeWide:  { dist: 16, dy: 3, look: -1.2, fov: 42 },
  low:          { dist: 2.6, dy: -1.55, look: -0.7, fov: 44 },    // hero/looming low angle
  high:         { dist: 3.2, dy: 2.6, look: -1.2, fov: 42 },      // overhead-ish
  feet:         { dist: 1.6, dy: -1.6, look: -1.75, fov: 40 },    // shoes / ground detail
};

function placeCamera(shot, lt) {
  const cam = S.stage.camera; const c = shot.camera || {};
  const dur = shot.duration;
  const k = ease[c.ease || 'inOut'](clamp01(lt / dur));
  let tgt = c.follow ? targetPoint(c.follow) : targetPoint(c.target ?? (shot.actors?.[0]?.id));
  if (c.offset) tgt.add(new THREE.Vector3(...c.offset));
  if (c.from) { // explicit camera path
    const from = new THREE.Vector3(...c.from), to = c.to ? new THREE.Vector3(...c.to) : from;
    cam.position.copy(from.lerp(to, k));
    const la = c.lookAt ? new THREE.Vector3(...c.lookAt) : tgt;
    cam.lookAt(la);
    cam.fov = c.fov || 40;
  } else {
    const pr = CAM[c.preset || 'medium'] || CAM.medium;
    const yaw = ((c.angle ?? 18) + (c.orbit || 0) * k) * Math.PI / 180;
    const dist = pr.dist * (c.zoom || 1) * (1 - (c.push ?? 0.12) * k);
    const pos = new THREE.Vector3(tgt.x + Math.sin(yaw) * dist, tgt.y + pr.dy + (c.dy || 0), tgt.z + Math.cos(yaw) * dist);
    cam.position.copy(pos);
    cam.lookAt(tgt.x, tgt.y + pr.look + (c.lookDy || 0), tgt.z);
    cam.fov = c.fov || pr.fov;
  }
  // whip-pan in (first 0.18 s) and handheld shake
  if (c.whip) { const w = 1 - clamp01(lt / 0.18); cam.rotateY(w * w * 0.9 * (c.whip === 'left' ? -1 : 1)); }
  const shake = (c.shake || 0) + (shot.fx || []).filter(f => f.type === 'shake' && lt >= (f.at || 0) && lt < (f.at || 0) + (f.dur || 0.4)).reduce((s, f) => s + (f.amount || 0.04), 0);
  if (shake) { cam.position.x += Math.sin(lt * 61) * shake; cam.position.y += Math.cos(lt * 47) * shake; }
  cam.aspect = S.W / S.H; cam.updateProjectionMatrix();
}

export function renderFrame(t) {
  if (!S) throw new Error('load() first');
  t = Math.min(t, S.total - 1e-4);
  let i = S.shots.findIndex(s => t >= s.start && t < s.start + s.duration); if (i < 0) i = S.shots.length - 1;
  const shot = S.shots[i];
  if (i !== S.currentShot) { setupShot(shot); S.currentShot = i; }
  const lt = t - shot.start;
  for (const a of S.actorsInShot) poseActor(a, lt, shot.duration, t);
  for (const p of S.propsInShot) poseActor(p, lt, shot.duration, t);
  S.set?.userData.update?.(t);
  placeCamera(shot, lt);
  const { renderer, scene, camera } = S.stage;
  renderer.render(scene, camera);
  // composite
  const g = S.ctx; g.drawImage(renderer.domElement, 0, 0, S.W, S.H);
  drawFX(g, shot, lt);
  drawOverlays(g, shot, lt);
  drawCaption(g, shot, lt);
  if (S.script.watermark) drawWatermark(g, S.script.watermark);
  return i;
}

// ---- 2D layers -------------------------------------------------------------
function drawFX(g, shot, lt) {
  const W = S.W, H = S.H;
  // soft vignette like the source grade
  const grd = g.createRadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 0.75);
  grd.addColorStop(0, 'rgba(0,0,0,0)'); grd.addColorStop(1, 'rgba(20,15,10,0.22)');
  g.fillStyle = grd; g.fillRect(0, 0, W, H);
  for (const f of shot.fx || []) {
    const at = f.at || 0, d = f.dur || 0.3, k = (lt - at) / d;
    if (k < 0 || k > 1) continue;
    if (f.type === 'flash') { g.fillStyle = `rgba(255,255,255,${(1 - k) * 0.9})`; g.fillRect(0, 0, W, H); }
    if (f.type === 'fadeBlack') { g.fillStyle = `rgba(0,0,0,${k})`; g.fillRect(0, 0, W, H); }
    if (f.type === 'fadeIn') { g.fillStyle = `rgba(0,0,0,${1 - k})`; g.fillRect(0, 0, W, H); }
    if (f.type === 'blackout') { g.fillStyle = '#000'; g.fillRect(0, 0, W, H); }
    if (f.type === 'redAlert') { g.fillStyle = `rgba(200,40,30,${0.25 * Math.abs(Math.sin(lt * 10))})`; g.fillRect(0, 0, W, H); }
  }
}

function drawOverlays(g, shot, lt) {
  const W = S.W, H = S.H;
  for (const o of shot.overlays || []) {
    if (lt < (o.at || 0) || lt > (o.until ?? 1e9)) continue;
    const pop = ease.outBack(clamp01((lt - (o.at || 0)) / 0.25));
    g.save();
    if (o.style === 'banner') { // top banner: "60 km/h" + sub-label (traffic camera gag)
      const bh = H * 0.11; g.fillStyle = 'rgba(241,233,210,0.93)'; g.fillRect(0, H * 0.02, W, bh * pop);
      g.fillStyle = P.redDark; g.font = `bold ${Math.round(H * 0.055)}px Arial`; g.textAlign = 'center'; g.textBaseline = 'middle';
      g.fillText(o.text, W / 2, H * 0.02 + bh / 2);
      if (o.sub) { g.fillStyle = 'rgba(241,233,210,0.93)'; g.fillRect(0, H * 0.84, W, H * 0.05); g.fillStyle = '#333'; g.font = `${Math.round(H * 0.022)}px Arial`; g.fillText(o.sub, W / 2, H * 0.865); }
    } else if (o.style === 'stamp') { // big rotated stamp "VENDU", "COUPABLE"
      g.translate(W / 2, H * (o.y ?? 0.35)); g.rotate(-0.15); g.scale(pop, pop);
      g.strokeStyle = P.red; g.lineWidth = 10; g.font = `900 ${Math.round(H * 0.075)}px Arial`; g.textAlign = 'center'; g.textBaseline = 'middle';
      const tw = g.measureText(o.text).width; g.strokeRect(-tw / 2 - 24, -H * 0.05, tw + 48, H * 0.1);
      g.fillStyle = P.red; g.fillText(o.text, 0, 4);
    } else if (o.style === 'phone') { // 911-style phone screen overlay
      const pw = W * 0.42, ph = pw * 1.4; g.translate(W / 2, H * 0.36); g.scale(pop, pop);
      g.fillStyle = '#111'; roundRect(g, -pw / 2 - 10, -ph / 2 - 10, pw + 20, ph + 20, 28); g.fill();
      g.fillStyle = '#2F6FB5'; roundRect(g, -pw / 2, -ph / 2, pw, ph, 20); g.fill();
      g.fillStyle = '#fff'; g.textAlign = 'center'; g.font = `900 ${Math.round(pw * 0.32)}px Arial`; g.fillText(o.text || '17', 0, -ph * 0.12);
      g.font = `bold ${Math.round(pw * 0.11)}px Arial`; g.fillText(o.sub || 'POLICE', 0, ph * 0.05);
      g.beginPath(); g.arc(0, ph * 0.28, pw * 0.14, 0, Math.PI * 2); g.fillStyle = '#3DAA6A'; g.fill();
    } else { // plain label
      g.fillStyle = o.color || '#fff'; g.font = `bold ${Math.round(H * (o.size || 0.04))}px Arial`; g.textAlign = 'center';
      g.lineWidth = 6; g.strokeStyle = 'rgba(0,0,0,0.7)'; g.strokeText(o.text, W / 2, H * (o.y ?? 0.15)); g.fillText(o.text, W / 2, H * (o.y ?? 0.15));
    }
    g.restore();
  }
}

function roundRect(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }

// never end a caption chunk on an article/preposition ("pour ranger sa | chambre")
const FUNCTION_WORDS = new Set(['le','la','les','l','un','une','des','du','de','d','sa','son','ses','sa','mon','ma','mes','ton','ta','tes','leur','leurs','ce','cet','cette','ces','au','aux','a','à','et','ou','en','pour','par','sur','dans','avec','sans','qui','que','qu','il','elle','on','ils','se','s','ne','n','plus','tres','trop','the','a','an','his','her','to','of','in','on','and','its']);
const norm = w => w.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9*']/g, '');

// Caption chunks: from TTS word timings when present, else evenly spread by length.
function captionChunks(shot) {
  if (shot._chunks) return shot._chunks;
  const words = shot.words || spreadWords(shot.line || '', shot.duration);
  const maxW = S.script.captionWords || 3;
  const chunks = []; let cur = [];
  words.forEach((w, i) => {
    cur.push(w);
    const dangling = FUNCTION_WORDS.has(norm(w.w)) && i < words.length - 1 && cur.length < maxW + 2;
    const end = /[.,!?;:…]$/.test(w.w) || (cur.length >= maxW && !dangling) || i === words.length - 1;
    if (end) { chunks.push({ words: cur, start: cur[0].s, end: words[i + 1] ? words[i + 1].s : shot.duration }); cur = []; }
  });
  shot._chunks = chunks; return chunks;
}
function spreadWords(line, dur) {
  const ws = line.split(/\s+/).filter(Boolean); const tot = ws.reduce((s, w) => s + w.length + 2, 0);
  let acc = 0; const speak = Math.max(0.5, dur - 0.25);
  return ws.map(w => { const s = acc / tot * speak; acc += w.length + 2; return { w, s, e: acc / tot * speak }; });
}

function drawCaption(g, shot, lt) {
  if (!shot.line || S.script.captions === false) return;
  const ch = captionChunks(shot).find(c => lt >= c.start && lt < c.end) || null;
  if (!ch) return;
  const W = S.W, H = S.H, hl = new Set((shot.highlight || []).map(norm));
  const fs = Math.round(W * (S.script.captionSize || 0.058));
  g.save(); g.font = `800 ${fs}px "Arial Black", Arial, sans-serif`; g.textBaseline = 'middle';
  // wrap into max 2 lines
  const parts = ch.words.map(w => w.w); const lines = [[]]; let lw = 0;
  for (const p of parts) { const pw = g.measureText(p + ' ').width; if (lw + pw > W * 0.78 && lines[lines.length - 1].length) { lines.push([]); lw = 0; } lines[lines.length - 1].push(p); lw += pw; }
  const y0 = H * (shot.captionY ?? S.script.captionY ?? 0.68) - (lines.length - 1) * fs * 0.6;
  const pop = 1 + 0.08 * (1 - ease.out(clamp01((lt - ch.start) / 0.12))); // tiny pop-in
  lines.forEach((ln, li) => {
    const text = ln.join(' '); const tw = g.measureText(text).width; let x = W / 2 - tw / 2; const y = y0 + li * fs * 1.2;
    for (const p of ln) {
      const isHl = hl.has(norm(p).replace(/[*]/g, '')) || hl.has(norm(p));
      g.save(); g.translate(x, y); g.scale(pop, pop);
      g.lineJoin = 'round'; g.lineWidth = fs * 0.2; g.strokeStyle = 'rgba(25,20,18,0.9)'; g.strokeText(p, 0, 0);
      g.fillStyle = isHl ? (S.script.highlightColor || P.salmon) : '#FFFFFF'; g.fillText(p, 0, 0);
      g.restore();
      x += g.measureText(p + ' ').width;
    }
  });
  g.restore();
}

function drawWatermark(g, text) {
  const W = S.W, H = S.H; g.save(); g.font = `bold ${Math.round(W * 0.03)}px Arial`; g.textAlign = 'center';
  g.fillStyle = 'rgba(40,60,90,0.55)'; const tw = g.measureText(text).width; g.fillRect(W / 2 - tw / 2 - 12, H * 0.93 - W * 0.025, tw + 24, W * 0.05);
  g.fillStyle = '#fff'; g.fillText(text, W / 2, H * 0.93 + W * 0.01); g.restore();
}

export function frameDataURL(type = 'image/jpeg', q = 0.92) { return S.out.toDataURL(type, q); }
export function info() { return { total: S?.total, shots: S?.shots.length }; }
