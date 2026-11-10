// Contact sheet of the face rig (engine/facerig.js): every preset, or a list of states / blends, drawn by the engine's own compositor.
//   node tools/face/rig_sheet.mjs out.jpg                      all presets
//   node tools/face/rig_sheet.mjs out.jpg neutral,take,greed   these presets
//   node tools/face/rig_sheet.mjs out.jpg --blend neutral:shocked:8     8 steps of the transition between two presets
//   node tools/face/rig_sheet.mjs out.jpg --variant '{"skin":"#8A5A3C","glasses":true,"facial":"mustache"}' [names]
//   node tools/face/rig_sheet.mjs out.jpg --states '[{"expr":"neutral","lid":0.5,"px":0.8}, ...]'   (lid/low/px/py/ps/s applied to both eyes)
import fs from 'node:fs';
import path from 'node:path';
import { chromium, LAUNCH_ARGS } from '../../render/pw.mjs';
import { startServer } from '../../render/server.mjs';
const args = process.argv.slice(2), out = args[0]; if (!out) { console.error('usage: node tools/face/rig_sheet.mjs out.jpg [names] [--blend a:b:n] [--variant json] [--states json] [--cols n] [--w px]'); process.exit(1); }
const opt = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : d; };
const names = args[1] && !args[1].startsWith('--') ? args[1].split(',') : null;
const srv = await startServer(), browser = await chromium.launch({ args: LAUNCH_ARGS }), page = await browser.newPage();
page.on('pageerror', e => console.log('[pageerror]', e.message)); page.on('console', m => { if (m.type() === 'error') console.log('[page]', m.text()); });
await page.goto(`http://127.0.0.1:${srv.address().port}/render/blank.html`);
const data = await page.evaluate(async ({ names, blend, variant, states, cols, tw }) => {
  const F = await import('/engine/facerig.js'); if (!F.RIG) return null;
  const rig = F.makeFaceRig(variant ? JSON.parse(variant) : null), items = [];
  if (blend) { const [a, b, n] = blend.split(':'); for (let i = 0; i < +n; i++) { const w = i / (+n - 1); items.push([`${a}>${b} ${w.toFixed(2)}`, F.blendFace(F.faceState(a), F.faceState(b), w)]); } }
  else if (states) for (const s of JSON.parse(states)) { const st = F.cloneFace(F.faceState(s.expr || 'neutral')); for (const sd of 'LR') for (const k of ['lid', 'low', 'px', 'py', 'ps', 's']) if (s[k] != null) st.eyes[sd][k] = s[k]; if (s.mouth) st.mouth.spr = s.mouth; items.push([s.label || JSON.stringify(s), st]); }
  else for (const n of names || Object.keys(F.RIG.presets)) items.push([n, F.faceState(n)]);
  const th = Math.round(tw * 1080 / 400), rows = Math.ceil(items.length / cols), c = document.createElement('canvas'); c.width = cols * tw; c.height = rows * (th + 18); const g = c.getContext('2d');
  g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height); g.font = '12px sans-serif'; g.fillStyle = '#000';
  items.forEach(([label, st], i) => { rig.set(st); const x = (i % cols) * tw, y = Math.floor(i / cols) * (th + 18); g.drawImage(rig.canvas, x, y, tw, th); g.fillText(label.slice(0, 26), x + 3, y + th + 13); });
  return c.toDataURL('image/jpeg', 0.9);
}, { names, blend: opt('blend', null), variant: opt('variant', null), states: opt('states', null), cols: +opt('cols', 12), tw: +opt('w', 160) });
if (!data) { console.error('face rig not found'); process.exit(1); }
fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true }); fs.writeFileSync(out, Buffer.from(data.split(',')[1], 'base64'));
await browser.close(); srv.close(); console.log('wrote', out);
