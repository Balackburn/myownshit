// Export every human preset + creature (+ props with --props) to models/*.glb
//   node render/export-models.mjs [--props] [--only lemec,cop]
import fs from 'node:fs';
import path from 'node:path';
import { chromium, LAUNCH_ARGS } from './pw.mjs';
import { startServer } from './server.mjs';
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const args = process.argv.slice(2);
const only = args.includes('--only') ? args[args.indexOf('--only') + 1].split(',') : null;
const srv = await startServer();
const browser = await chromium.launch({ args: LAUNCH_ARGS });
const page = await browser.newPage();
page.on('pageerror', e => console.log('[pageerror]', e.message));
await page.goto(`http://127.0.0.1:${srv.address().port}/render/stage.html?mode=export`);
await page.waitForFunction(() => window.__ready, null, { timeout: 60000 });
const L = await page.evaluate(() => window.__engine.list());
const jobs = [...L.humans.map(n => ['human', n]), ...L.creatures.map(n => ['creature', n]), ...(args.includes('--props') ? L.props.map(n => ['prop', n]) : [])]
  .filter(([, n]) => !only || only.includes(n));
for (const [kind, name] of jobs) {
  const dir = path.join(ROOT, 'models', kind === 'human' ? 'humans' : kind === 'creature' ? 'creatures' : 'props'); fs.mkdirSync(dir, { recursive: true });
  try {
    const b64 = await page.evaluate(([k, n]) => window.__engine.exportOne(k, n), [kind, name]);
    const f = path.join(dir, name + '.glb'); fs.writeFileSync(f, Buffer.from(b64, 'base64'));
    console.log(kind.padEnd(8), name.padEnd(16), (fs.statSync(f).size / 1024).toFixed(0) + ' KB');
  } catch (e) { console.log('FAILED', kind, name, e.message.split('\n')[0]); }
}
await browser.close(); srv.close();
