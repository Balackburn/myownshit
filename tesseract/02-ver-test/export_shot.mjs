// node export_shot.mjs <story.json> <t> <out.glb> : the posed engine scene at time t -> GLB + camera/sun JSON (for the Tesseract test)
import fs from 'node:fs';
import path from 'node:path';
const ROOT = '/home/user/myownshit/absurd-shorts';
const { chromium, LAUNCH_ARGS } = await import(ROOT + '/render/pw.mjs');
const { startServer } = await import(ROOT + '/render/server.mjs');
const [script, t, out] = process.argv.slice(2);
const srv = await startServer(); const browser = await chromium.launch({ args: LAUNCH_ARGS });
const page = await browser.newPage({ viewport: { width: 540, height: 960 } });
page.on('pageerror', e => console.log('[pageerror]', e.message));
await page.goto(`http://127.0.0.1:${srv.address().port}/render/stage.html?mode=film3`);
await page.waitForFunction(() => window.__ready, null, { timeout: 60000 });
const s = JSON.parse(fs.readFileSync(script, 'utf8'));
await page.evaluate(async ({ s }) => window.__engine.load(s, { width: 1080, height: 1920 }), { s });
const r = await page.evaluate(async t => window.__engine.exportSceneGLB(t), +t);
fs.writeFileSync(out, Buffer.from(r.glb, 'base64')); delete r.glb;
fs.writeFileSync(out.replace(/\.glb$/, '.json'), JSON.stringify(r, null, 1));
console.log('glb', (fs.statSync(out).size / 1e6).toFixed(1), 'MB', JSON.stringify(r));
await browser.close(); srv.close();
