// node export_shots.mjs <story.json> <outdir> [fps] [only S01,S02]: every shot with its motion baked -> outdir/S01.glb + S01.json
import fs from 'node:fs';
const ROOT = '/home/user/myownshit/absurd-shorts';
const { chromium, LAUNCH_ARGS } = await import(ROOT + '/render/pw.mjs');
const { startServer } = await import(ROOT + '/render/server.mjs');
const [script, outdir, fps = '15', only = ''] = process.argv.slice(2); fs.mkdirSync(outdir, { recursive: true });
const srv = await startServer(); const browser = await chromium.launch({ args: LAUNCH_ARGS });
const page = await browser.newPage({ viewport: { width: 540, height: 960 } });
page.on('pageerror', e => console.log('[pageerror]', e.message));
await page.goto(`http://127.0.0.1:${srv.address().port}/render/stage.html?mode=film3`);
await page.waitForFunction(() => window.__ready, null, { timeout: 60000 });
const s = JSON.parse(fs.readFileSync(script, 'utf8'));
const tl = await page.evaluate(async ({ s }) => window.__engine.load(s, { width: 1080, height: 1920 }), { s });
for (let si = 0; si < tl.scenes.length; si++) {
  const id = tl.scenes[si].id; if (only && !only.split(',').includes(id)) continue;
  const t0 = Date.now(); const r = await page.evaluate(async a => window.__engine.exportShotGLB(a.si, { fps: a.fps }), { si, fps: +fps });
  fs.writeFileSync(`${outdir}/${id}.glb`, Buffer.from(r.glb, 'base64')); delete r.glb; fs.writeFileSync(`${outdir}/${id}.json`, JSON.stringify(r));
  console.log(id, (fs.statSync(`${outdir}/${id}.glb`).size / 1e6).toFixed(1) + ' MB', r.animated + ' moving meshes', r.times.length + ' samples', ((Date.now() - t0) / 1000).toFixed(0) + ' s');
}
await browser.close(); srv.close();
