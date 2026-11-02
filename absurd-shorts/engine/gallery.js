// Visual QA gallery: lineups of characters / poses / expressions / props / sets / creatures.
import * as THREE from 'three';
import { createStage, setLighting } from './scene.js';
import { buildHuman, PRESETS } from './human.js';
import { samplePose, applyPose, CLIP_NAMES } from './animations.js';
import { EXPRESSIONS } from './face.js';
import { mat, PALETTE as P } from './style.js';

async function optional(path) { try { return await import(path); } catch (e) { console.warn('missing ' + path + ': ' + e.message); return null; } }

export async function show(q, w, h) {
  const { renderer, scene, camera } = createStage(w, h);
  setLighting(scene, q.light || 'interior');
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), mat(P.cream)); floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
  const items = [];
  const what = q.what || 'humans';
  if (what === 'humans') {
    const names = (q.list ? q.list.split(',') : Object.keys(PRESETS));
    names.forEach(n => items.push({ obj: buildHuman({ preset: n }), label: n, pose: q.pose || 'stand', t: 0.3 }));
  } else if (what === 'poses') {
    const names = q.list ? q.list.split(',') : CLIP_NAMES;
    names.forEach(n => items.push({ obj: buildHuman({ preset: q.preset || 'lemec' }), label: n, pose: n, t: +(q.t || 0.4) }));
  } else if (what === 'faces') {
    EXPRESSIONS.forEach(e => { const hm = buildHuman({ preset: q.preset || 'lemec' }); hm.userData.setExpression(e); items.push({ obj: hm, label: e, pose: 'stand', t: 0 }); });
  } else if (what === 'creatures') {
    const C = await optional('/engine/creatures.js');
    if (C) (q.list ? q.list.split(',') : C.CREATURE_NAMES).forEach(n => { const c = C.buildCreature(n); items.push({ obj: c, label: n, creature: true, t: +(q.t || 0.3), clip: q.clip || 'idle' }); });
  } else if (what === 'props') {
    const Pr = await optional('/engine/props.js');
    if (Pr) (q.list ? q.list.split(',') : Pr.PROP_NAMES).forEach(n => items.push({ obj: Pr.buildProp(n, {}), label: n, t: +(q.t || 0.5) }));
  } else if (what === 'set') {
    const Se = await optional('/engine/sets.js');
    if (Se) { scene.remove(floor); const s = Se.buildSet(q.name || 'office', {}); scene.add(s); setLighting(scene, s.userData.lighting || 'day');
      const hm = buildHuman('lemec'); applyPose(hm, samplePose('stand', 0), { x: 0, z: 0 }); scene.add(hm);
      camera.position.set(+(q.cx || 0), +(q.cy || 1.6), +(q.cz || 6)); camera.lookAt(0, 1.2, 0); s.userData.update?.(+(q.t || 1));
      renderer.render(scene, camera); return; }
  }
  // grid layout
  const cols = Math.min(items.length, +(q.cols || 8)); const rows = Math.ceil(items.length / cols); const sp = +(q.spacing || 1.0);
  items.forEach((it, i) => {
    const x = (i % cols - (cols - 1) / 2) * sp, z = -Math.floor(i / cols) * sp * 2.2;
    if (it.creature) { it.obj.position.set(x, 0, z); it.obj.userData.animate?.(it.clip, it.t); }
    else if (it.obj.userData.kind === 'human') applyPose(it.obj, samplePose(it.pose, it.t), { x, z });
    else { it.obj.position.set(x, 0, z); it.obj.userData.update?.(it.t); }
    scene.add(it.obj);
    const lab = label(it.label); lab.position.set(x, -0.0, z + 0.55); scene.add(lab);
  });
  const width = cols * sp, depth = rows * sp * 2.2;
  const dist = Math.max(width * 1.05, 3.2) * (w > h ? 1 : 1.8);
  camera.aspect = w / h; camera.updateProjectionMatrix();
  camera.position.set(0, +(q.cy || 1.4 + rows * 0.6), dist * 0.95 + (q.cz ? +q.cz : 0)); camera.lookAt(0, +(q.ly || 0.9), -depth * 0.35);
  if (q.cam) { const c = q.cam.split(',').map(Number); camera.fov = +(q.fov || 40); camera.updateProjectionMatrix(); camera.position.set(c[0], c[1], c[2]); camera.lookAt(c[3], c[4], c[5]); }
  if (q.nolabel) scene.children.filter(o => o.geometry?.type === 'PlaneGeometry' && o.material?.map && o.material.transparent).forEach(o => o.visible = false);
  renderer.render(scene, camera);
}

function label(text) {
  const c = document.createElement('canvas'); c.width = 256; c.height = 48; const g = c.getContext('2d');
  g.fillStyle = '#222'; g.font = 'bold 30px Arial'; g.textAlign = 'center'; g.fillText(text, 128, 34);
  const t = new THREE.CanvasTexture(c); const m = new THREE.Mesh(new THREE.PlaneGeometry(0.9, 0.17), new THREE.MeshBasicMaterial({ map: t, transparent: true }));
  m.rotation.x = -Math.PI / 2.6; return m;
}
