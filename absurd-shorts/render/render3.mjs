// Pipeline for script v3 (scene timelines):
//   node render/render3.mjs scripts-fr/chrono3.json [--w 1080 --h 1920 --fps 30] [--workers 4]
//        [--preview]           360x640 @15 fps quick motion check (with audio)
//        [--stills cams]       one still per camera setup + contact sheet (framing QA), no video
//        [--stills 1.2,3.4]    stills at absolute times
//        [--strip 12.3:8]      8 consecutive frames at 12 fps from 12.3 s (motion QA) -> contact strip
//        [--out out/x.mp4]
// Steps: tts3 (ElevenLabs timestamps) -> analysis (warnings, events, camera list) -> frames (parallel) -> mix3 -> mux -> SRT.
import { spawnSync, spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { chromium, LAUNCH_ARGS } from './pw.mjs';
import { startServer } from './server.mjs';

const args = process.argv.slice(2);
const flag = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? (args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : true) : d; };
const scriptPath = args.find(a => a.endsWith('.json'));
if (!scriptPath) { console.error('usage: node render/render3.mjs <script.json> [--preview] [--stills cams] [--workers 4]'); process.exit(1); }
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const name = path.basename(scriptPath, '.json');
const preview = !!flag('preview', false);
const W = +flag('w', preview ? 360 : 1080), H = +flag('h', preview ? 640 : 1920), FPS = +flag('fps', preview ? 15 : 30);
const workers = +flag('workers', 4);
const work = path.join(ROOT, 'out', 'work', name); fs.mkdirSync(work, { recursive: true });
const outFile = path.resolve(flag('out', path.join(ROOT, 'out', name + (preview ? '_preview' : '') + '.mp4')));
const py = (...a) => { const r = spawnSync('python3', a, { stdio: 'inherit' }); if (r.status) process.exit(r.status); };

// 1) voice + real word timings
py(path.join(ROOT, 'tools/audio3.py'), 'tts', path.resolve(scriptPath), work);
const timedPath = path.join(work, 'script.timed.json');
const timed = JSON.parse(fs.readFileSync(timedPath, 'utf8'));

const srv = await startServer();
const url = `http://127.0.0.1:${srv.address().port}/render/stage.html?mode=film3`;
async function openPage(w = W, h = H) {
  const browser = await chromium.launch({ args: LAUNCH_ARGS });
  const page = await browser.newPage({ viewport: { width: Math.min(w, 1200), height: Math.min(h, 1200) } });
  page.on('pageerror', e => console.log('[pageerror]', e.message));
  page.on('console', m => { if (m.type() === 'error') console.log('[page]', m.text()); });
  await page.goto(url); await page.waitForFunction(() => window.__ready, null, { timeout: 60000 });
  const tl = await page.evaluate(async ({ s, w, h }) => window.__engine.load(s, { width: w, height: h }), { s: timed, w, h });
  return { browser, page, tl };
}

// 2) analysis: warnings (framing / motion lint), SFX events, camera setups
const A = await openPage();
const an = await A.page.evaluate(async () => window.__engine.analyze());
fs.writeFileSync(path.join(work, 'events.json'), JSON.stringify(an.events));
fs.writeFileSync(path.join(work, 'cams.json'), JSON.stringify(an.cams, null, 1));
fs.writeFileSync(path.join(work, 'warnings.txt'), an.warnings.join('\n'));
console.log(`timeline ${A.tl.duration.toFixed(2)}s, ${A.tl.scenes.length} scenes, ${an.cams.length} camera setups, ${an.events.length} sfx events, ${an.warnings.length} warnings`);
for (const w of an.warnings.slice(0, 80)) console.log('  ! ' + w);

async function grab(page, t, file, type = 'image/png') {
  await page.evaluate(t => window.__engine.renderFrame(t), t);
  const data = await page.evaluate(ty => window.__engine.frameDataURL(ty, 0.9), type);
  fs.writeFileSync(file, Buffer.from(data.split(',')[1], 'base64'));
}
const stills = flag('stills', null), strip = flag('strip', null);
if (stills || strip) {
  const dir = path.join(work, 'stills'); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  let items;
  if (strip) { const [t0, n] = String(strip).split(':').map(Number); items = Array.from({ length: n || 8 }, (_, i) => ({ t: t0 + i / 12, label: `${(t0 + i / 12).toFixed(2)}` })); }
  else if (stills === 'cams' || stills === true) items = an.cams.map((c, i) => ({ t: c.t, label: `${i} ${c.scene} ${c.size} ${c.frame}`.slice(0, 40) }));
  else items = String(stills).split(',').map(Number).map(t => ({ t, label: t.toFixed(2) }));
  const files = [];
  for (const [i, it] of items.entries()) { const f = path.join(dir, `s_${String(i).padStart(3, '0')}.jpg`); await grab(A.page, it.t, f, 'image/jpeg'); files.push({ f, label: it.label }); }
  fs.writeFileSync(path.join(dir, 'list.json'), JSON.stringify(files));
  py(path.join(ROOT, 'tools/sheet.py'), path.join(dir, 'list.json'), path.join(work, strip ? 'strip.jpg' : 'cams.jpg'), strip ? '8' : '10');
  await A.browser.close(); srv.close(); process.exit(0);
}
await A.browser.close();

// 3) frames, in parallel workers (each renders a contiguous range into its own segment)
const N = Math.ceil(A.tl.duration * FPS), per = Math.ceil(N / workers), t0 = Date.now();
let done = 0;
const segs = await Promise.all(Array.from({ length: workers }, async (_, wi) => {
  const a = wi * per, b = Math.min(N, a + per); if (a >= b) return null;
  const seg = path.join(work, `seg_${wi}.mp4`);
  const P = await openPage();
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'medium', '-crf', preview ? '26' : '18', seg], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = a; i < b; i++) {
    const data = await P.page.evaluate(t => { window.__engine.renderFrame(t); return window.__engine.frameDataURL('image/jpeg', 0.93); }, i / FPS);
    if (!ff.stdin.write(Buffer.from(data.split(',')[1], 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
    if (++done % 60 === 0) process.stdout.write(`\rframes ${done}/${N}  ${(done / ((Date.now() - t0) / 1000)).toFixed(1)} fps   `);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await P.browser.close();
  return seg;
}));
srv.close();
console.log(`\nframes done in ${((Date.now() - t0) / 60000).toFixed(1)} min`);
const list = path.join(work, 'segs.txt'); fs.writeFileSync(list, segs.filter(Boolean).map(s => `file '${s}'`).join('\n'));
const silent = path.join(work, 'video.mp4');
spawnSync('ffmpeg', ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', silent], { stdio: 'inherit' });

// 4) audio mix (voice + synced SFX + ambience + music stems), mux at -14 LUFS, SRT + script next to the video
py(path.join(ROOT, 'tools/audio3.py'), 'mix', timedPath, path.join(work, 'events.json'), work);
spawnSync('ffmpeg', ['-y', '-v', 'error', '-i', silent, '-i', path.join(work, 'mix.wav'), '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=7', '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', '-shortest', outFile], { stdio: 'inherit' });
const base = outFile.replace(/\.mp4$/, '');
py(path.join(ROOT, 'tools/audio3.py'), 'srt', timedPath, base + '.srt');
fs.writeFileSync(base + '.script.txt', timed.scenes.map(s => `## ${s.id} (${s.set})\n` + s.lines.map(l => `[${l.start.toFixed(2)}–${l.end.toFixed(2)}] ${l.speaker ? l.speaker.toUpperCase() + ' : ' : ''}${l.text}`).join('\n')).join('\n\n'));
if (!preview) for (const st of ['voice', 'sfx', 'music']) fs.copyFileSync(path.join(work, st + '.wav'), `${base}.${st}.wav`);
console.log('wrote', outFile);
