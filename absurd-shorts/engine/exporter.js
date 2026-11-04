// Exports characters/creatures/props to binary glTF (.glb) with the named joint hierarchy
// (rigid parenting = posable in Blender/Unity) and baked animation clips.
import * as THREE from 'three';
import { GLTFExporter } from 'three/addons/exporters/GLTFExporter.js';
import { buildHuman, PRESETS } from './human.js';
import { CLIPS, samplePose, applyPose } from './animations.js';

const opt = async p => { try { return await import(p); } catch { return null; } };

export const HUMAN_BAKE = [...new Set(['idle', 'walk', 'run', 'flee', 'handsOnHips', 'oneHandHip', 'point', 'salute', 'wave', 'shrug', 'facepalm', 'phone', 'think', 'armsCrossed', 'talk', 'yell', 'celebrate', 'scared', 'surrender', 'handcuffed', 'pressGlass', 'cry', 'dance', 'sit', 'sitWrite', 'slumpDesk', 'jump', 'startle', 'hangWire', 'lookAround', 'stareCamera', 'lurk', 'climbDown', 'sneak', 'crawl', 'kneel', 'explain', 'phoneCall', 'point', 'stand', 'holdOut', 'present', 'showPhone'])];

function deInstance(root) { // EXT_mesh_gpu_instancing is not read by every importer (Tesseract): expand instances into plain meshes
  const inst = []; root.traverse(n => { if (n.isInstancedMesh) inst.push(n); });
  for (const im of inst) {
    const g = new THREE.Group(); g.name = im.name; g.position.copy(im.position); g.quaternion.copy(im.quaternion); g.scale.copy(im.scale);
    const m4 = new THREE.Matrix4();
    for (let i = 0; i < im.count; i++) {
      im.getMatrixAt(i, m4); const m = new THREE.Mesh(im.geometry, im.material); m.applyMatrix4(m4);
      if (im.instanceColor) { const c = new THREE.Color(); im.getColorAt(i, c); m.material = im.material.clone(); m.material.color?.multiply(c); }
      g.add(m);
    }
    const parent = im.parent; parent.add(g); parent.remove(im);
  }
}

function clampMaterials(root) { // glTF factors must stay in 0..1 (our engine brightens some textures with colour > 1)
  const seen = new Set();
  root.traverse(n => [].concat(n.material || []).forEach(m => {
    if (seen.has(m)) return; seen.add(m);
    for (const k of ['color', 'emissive', 'specularColor', 'sheenColor', 'attenuationColor']) if (m[k]?.isColor) { m[k].r = Math.min(1, Math.max(0, m[k].r)); m[k].g = Math.min(1, Math.max(0, m[k].g)); m[k].b = Math.min(1, Math.max(0, m[k].b)); }
    for (const k of ['metalness', 'roughness', 'opacity', 'transmission', 'clearcoat', 'sheen']) if (typeof m[k] === 'number') m[k] = Math.min(1, Math.max(0, m[k]));
  }));
}

function stripForExport(root) {
  const kill = []; root.traverse(n => { if (n.name === 'outline') kill.push(n); });
  kill.forEach(n => n.parent.remove(n));
  deInstance(root); clampMaterials(root);
  // userData holds rig references + closures; keep only a tiny serialisable spec as glTF extras
  const spec = root.userData.spec ? JSON.parse(JSON.stringify(root.userData.spec)) : undefined;
  root.traverse(n => { n.userData = {}; });
  if (spec) root.userData = { spec };
}

function bakeHuman(h, clips, fps = 30, dur = 2) {
  const J = h.userData.joints; const out = [];
  for (const [jn, obj] of Object.entries(J)) if (!obj.name) obj.name = jn; // e.g. coatTail: an unnamed joint gives a channel with no target node
  const q = new THREE.Quaternion(), e = new THREE.Euler();
  for (const name of clips) {
    if (!CLIPS[name]) continue;
    const times = [], tracks = {}; const rootPos = [];
    for (let i = 0; i <= fps * dur; i++) {
      const t = i / fps; times.push(t); const p = samplePose(name, t);
      for (const [jn, obj] of Object.entries(J)) {
        const r = p[jn] || [0, 0, 0]; e.set(r[0], r[1], r[2]); q.setFromEuler(e);
        (tracks[jn] ||= []).push(q.x, q.y, q.z, q.w);
      }
      const rt = p.root || {}; rootPos.push(rt.x || 0, h.userData.joints.hips.position.y + (rt.y || 0), rt.z || 0);
    }
    const kf = Object.entries(tracks).map(([jn, v]) => new THREE.QuaternionKeyframeTrack(`${J[jn].name}.quaternion`, times, v));
    kf.push(new THREE.VectorKeyframeTrack(`${J.hips.name}.position`, times, rootPos));
    out.push(new THREE.AnimationClip(name, dur, kf));
  }
  return out;
}

async function toGLB(obj, animations = []) {
  const ex = new GLTFExporter();
  const buf = await ex.parseAsync(obj, { binary: true, animations, onlyVisible: true });
  let s = ''; const b = new Uint8Array(buf); for (let i = 0; i < b.length; i += 0x8000) s += String.fromCharCode.apply(null, b.subarray(i, i + 0x8000));
  return btoa(s);
}

export async function list() {
  const C = await opt('/engine/creatures.js'); const P = await opt('/engine/props.js');
  return { humans: Object.keys(PRESETS), creatures: C ? C.CREATURE_NAMES : [], props: P ? P.PROP_NAMES : [] };
}

export async function exportOne(kind, name, { bake = true } = {}) {
  let obj, anims = [];
  if (kind === 'human') {
    obj = buildHuman({ preset: name });
    // rest pose = all joint rotations at zero (arms straight down) so the Blender rig gets a clean bind pose
    if (bake && name === 'lemec') anims = bakeHuman(obj, HUMAN_BAKE); // same joint names on every preset → clips retarget 1:1
    stripForExport(obj); obj.name = name;
  } else if (kind === 'creature') {
    const C = await import('/engine/creatures.js'); obj = C.buildCreature(name); obj.userData.animate?.('idle', 0); stripForExport(obj); obj.name = name;
  } else {
    const P = await import('/engine/props.js'); obj = P.buildProp(name, {}); stripForExport(obj); obj.name = name;
  }
  const scene = new THREE.Scene(); scene.add(obj); scene.updateMatrixWorld(true);
  return toGLB(scene, anims);
}
