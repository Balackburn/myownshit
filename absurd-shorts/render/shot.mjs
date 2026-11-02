// Screenshot helper: node render/shot.mjs "<query string for gallery>" out.png [w] [h]
// e.g. node render/shot.mjs "what=humans" /tmp/humans.png 1600 900
import { chromium, LAUNCH_ARGS } from './pw.mjs';
import { startServer } from './server.mjs';
const [qs = 'what=humans', out = 'out/gallery.png', w = '1600', h = '900'] = process.argv.slice(2);
const srv = await startServer();
const browser = await chromium.launch({ args: LAUNCH_ARGS });
const page = await browser.newPage({ viewport: { width: +w, height: +h } });
page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console.log('[page]', m.text()); });
page.on('pageerror', e => console.log('[pageerror]', e.message));
await page.goto(`http://127.0.0.1:${srv.address().port}/render/stage.html?mode=gallery&${qs}`);
await page.waitForFunction(() => window.__ready, null, { timeout: 60000 });
await page.evaluate(async ({ qs, w, h }) => window.__engine.show(Object.fromEntries(new URLSearchParams(qs)), +w, +h), { qs, w, h });
await page.screenshot({ path: out });
await browser.close(); srv.close();
console.log('wrote', out);
