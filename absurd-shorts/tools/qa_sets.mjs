// Set QA (viz3d checks): z-fighting pairs per set (coplanar-check.js) + mesh / triangle counts.
//   node tools/qa_sets.mjs [set1,set2,...] [--tol 0.006]
import { chromium, LAUNCH_ARGS } from '../render/pw.mjs';
import { startServer } from '../render/server.mjs';

const args = process.argv.slice(2);
const tolI = args.indexOf('--tol'); const tol = tolI >= 0 ? +args[tolI + 1] : 0.006;
const sets = (args.find(a => !a.startsWith('--') && a !== String(tol)) || 'office,bar,bank,street,livingRoom,zoo,kitchenNight,rooftopPowerLine,secretGym,lab,policeStation,restaurant,farm,prisonCell').split(',');
const srv = await startServer();
const browser = await chromium.launch({ args: LAUNCH_ARGS });
const page = await browser.newPage({ viewport: { width: 360, height: 640 } });
page.on('pageerror', e => console.log('[pageerror]', e.message));
await page.goto(`http://127.0.0.1:${srv.address().port}/render/stage.html?mode=film3`);
await page.waitForFunction(() => window.__ready, null, { timeout: 60000 });
const script = { version: 3, title: 'qa', captionWords: 3, voice: { name: 'none' }, cast: {},
  scenes: sets.map((s, i) => ({ id: 's' + i, set: s.split(':')[0], setOpts: s.includes(':') ? JSON.parse(s.slice(s.indexOf(':') + 1)) : {}, lines: [], actors: [], props: [], cams: [{ at: 0, from: [0, 1.6, 6], lookAt: [0, 1, 0] }], start: i, duration: 1 })) };
script.duration = sets.length;
const res = await page.evaluate(async ({ script, tol }) => {
  const E = window.__engine; await E.load(script, { width: 360, height: 640 });
  const { findCoplanarPairs } = await import('/engine/qa/coplanar-check.js');
  const out = [];
  for (let i = 0; i < script.scenes.length; i++) {
    E.renderFrame(i + 0.5);
    const S = E._S(); const set = S.set;
    let meshes = 0, tris = 0; set.traverse(n => { if (n.isMesh) { meshes++; const g = n.geometry; tris += (g.index ? g.index.count : g.attributes.position.count) / 3 * (n.isInstancedMesh ? n.count : 1); } });
    // outline shells are back-face copies (never z-fight); bottom faces resting on a floor are hidden, so keep only
    // pairs whose visible (max) faces meet
    const hide = []; set.traverse(n => { if (n.name === 'outline' && n.visible) { n.visible = false; hide.push(n); } });
    const pairs = findCoplanarPairs(set, { tolerance: tol, minimumArea: 0.02 }); hide.forEach(n => (n.visible = true));
    out.push({ set: script.scenes[i].set, meshes, tris: Math.round(tris), pairs: pairs.slice(0, 12) });
  }
  return out;
}, { script, tol });
for (const r of res) {
  console.log(`== ${r.set}: ${r.meshes} meshes, ${r.tris} tris, ${r.pairs.length} coplanar pairs (<${tol * 100} cm)`);
  for (const p of r.pairs) console.log(`   ${p.first} / ${p.second}  axis ${p.axis}  gap ${p.gapCm} cm  overlap ${p.overlapM2} m2`);
}
await browser.close(); srv.close();
