// Exports characters/creatures/props to binary glTF (.glb) with the named joint hierarchy
// (rigid parenting = posable in Blender/Unity) and baked animation clips.
import * as THREE from 'three';
import { GLTFExporter } from 'three/addons/exporters/GLTFExporter.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { buildHuman, PRESETS } from './human.js';
import { CLIPS, samplePose, applyPose } from './animations.js';

const opt = async p => { try { return await import(p); } catch { return null; } };

export const HUMAN_BAKE = [...new Set(['idle', 'walk', 'run', 'flee', 'handsOnHips', 'oneHandHip', 'point', 'salute', 'wave', 'shrug', 'facepalm', 'phone', 'think', 'armsCrossed', 'talk', 'yell', 'celebrate', 'scared', 'surrender', 'handcuffed', 'pressGlass', 'cry', 'dance', 'sit', 'sitWrite', 'slumpDesk', 'jump', 'startle', 'hangWire', 'lookAround', 'stareCamera', 'lurk', 'climbDown', 'sneak', 'crawl', 'kneel', 'explain', 'phoneCall', 'phoneCallL', 'point', 'stand', 'holdOut', 'present', 'showPhone'])];

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

// merge a static prop into one mesh per material (world transforms baked): far fewer draw calls for software renderers
function mergeByMaterial(root) {
  root.updateMatrixWorld(true);
  const groups = new Map();
  root.traverse(n => {
    if (!n.isMesh || n.isSkinnedMesh || !n.geometry) return;
    const mats = [].concat(n.material); if (mats.length !== 1) return;     // multi-material meshes stay as they are
    let g = n.geometry.clone(); g.applyMatrix4(n.matrixWorld);
    if (g.index) g = g.toNonIndexed();
    for (const k of Object.keys(g.attributes)) if (!['position', 'normal', 'uv'].includes(k)) g.deleteAttribute(k);
    if (!g.attributes.normal) g.computeVertexNormals();
    if (!g.attributes.uv) g.setAttribute('uv', new THREE.Float32BufferAttribute(new Float32Array(g.attributes.position.count * 2), 2));
    g.morphAttributes = {};
    const key = mats[0].uuid; if (!groups.has(key)) groups.set(key, { mat: mats[0], geos: [], nodes: [] });
    groups.get(key).geos.push(g); groups.get(key).nodes.push(n);
  });
  const out = new THREE.Group(); out.name = root.name;
  for (const { mat, geos, nodes } of groups.values()) {
    const merged = mergeGeometries(geos, false); if (!merged) { nodes.forEach(n => out.add(n.clone())); continue; }
    const m = new THREE.Mesh(merged, mat); m.castShadow = true; m.receiveShadow = true; out.add(m);
  }
  return out;
}

export async function list() {
  const C = await opt('/engine/creatures.js'); const P = await opt('/engine/props.js');
  return { humans: Object.keys(PRESETS), creatures: C ? C.CREATURE_NAMES : [], props: P ? P.PROP_NAMES : [] };
}

export async function exportOne(kind, name, { bake = true, opts = {}, merge = false } = {}) {
  let obj, anims = [];
  if (kind === 'human') {
    obj = buildHuman({ preset: name });
    // rest pose = all joint rotations at zero (arms straight down) so the Blender rig gets a clean bind pose
    if (bake && name === 'lemec') anims = bakeHuman(obj, HUMAN_BAKE); // same joint names on every preset → clips retarget 1:1
    stripForExport(obj); obj.name = name;
  } else if (kind === 'creature') {
    const C = await import('/engine/creatures.js'); obj = C.buildCreature(name); obj.userData.animate?.('idle', 0); stripForExport(obj); obj.name = name;
  } else {
    const P = await import('/engine/props.js'); obj = P.buildProp(name, opts); stripForExport(obj); obj.name = name;
    if (merge) obj = mergeByMaterial(obj);
  }
  const scene = new THREE.Scene(); scene.add(obj); scene.updateMatrixWorld(true);
  return toGLB(scene, anims);
}
