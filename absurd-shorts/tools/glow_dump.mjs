// node tools/glow_dump.mjs OUT.png [big] [expr]: the glow canvas of the face rig (the eyes drawn for a shot in the dark), to look for seams in the 2D drawing
import fs from 'node:fs';
import { chromium, LAUNCH_ARGS } from '../render/pw.mjs';
import { startServer } from '../render/server.mjs';
const out = process.argv[2], big = Number(process.argv[3] || 5.2), expr = process.argv[4] || 'neutral';
const srv = await startServer(); const browser = await chromium.launch({ args: LAUNCH_ARGS }); const page = await browser.newPage();
page.on('pageerror', e => console.log('[pageerror]', e.message));
await page.goto(`http://127.0.0.1:${srv.address().port}/render/blank.html`);
const data = await page.evaluate(async ({ big, expr }) => {
  const m = await import('/engine/facerig.js'); const fr = m.makeFaceRig(null); const st = m.cloneFace(m.faceState(expr));
  for (const s of 'LR') { st.eyes[s].px = 0.3; st.eyes[s].py = 0.1; }
  const tex = fr.glow(st, big); return { url: tex.image.toDataURL('image/png'), w: tex.image.width, h: tex.image.height, eyes: st.eyes };
}, { big, expr });
fs.writeFileSync(out, Buffer.from(data.url.split(',')[1], 'base64')); console.log(data.w, data.h, JSON.stringify(data.eyes));
await browser.close(); srv.close();
