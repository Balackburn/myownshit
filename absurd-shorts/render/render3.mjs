// Pipeline for script v3 (scene timelines):
//   node render/render3.mjs scripts-fr/chrono3.json [--w 1080 --h 1920 --fps 30] [--workers 4]
//        [--preview]           360x640 @15 fps quick motion check (with audio)
//        [--stills cams]       one still per camera setup + contact sheet (framing QA), no video
//        [--stills 1.2,3.4]    stills at absolute times
//        [--probe]             (cycle 13) measure the key poses of the declared gags (script.gags), no render
//        [--strip 12.3:8]      8 consecutive frames at 12 fps from 12.3 s (motion QA) -> contact strip
//        [--range 12.3:14.1]   only that part of the film, in seconds (re-render one shot, then splice)
//        [--draft]             cheaper shadows (natural / shaders look) for motion previews
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
const even = v => 2 * Math.round(v / 2);   // the encoder refuses odd sizes (and the pipe then stalls)
const W = even(+flag('w', preview ? 360 : 1080)), H = even(+flag('h', preview ? 640 : 1920)), FPS = +flag('fps', preview ? 15 : 30);
const workers = +flag('workers', 4);
const work = path.join(ROOT, 'out', 'work', name); fs.mkdirSync(work, { recursive: true });
const outFile = path.resolve(flag('out', path.join(ROOT, 'out', name + (preview ? '_preview' : '') + '.mp4')));
const py = (...a) => { const r = spawnSync('python3', a, { stdio: 'inherit' }); if (r.status) process.exit(r.status); };

// 1) voice + real word timings (--timed: the JSON already carries scene start/duration, e.g. a replica cut on a reference; no TTS, silent video)
const timedMode = !!flag('timed', false);
if (!timedMode) py(path.join(ROOT, 'tools/audio3.py'), 'tts', path.resolve(scriptPath), work);
const timedPath = timedMode ? path.resolve(scriptPath) : path.join(work, 'script.timed.json');
const timed = JSON.parse(fs.readFileSync(timedPath, 'utf8'));

if (flag('draft', false)) timed.lookOpts = { ...(timed.lookOpts || {}), draft: true };   // --draft: cheaper shadows for motion previews (engine/look.js), never for a delivery
const srv = await startServer();
const url = `http://127.0.0.1:${srv.address().port}/render/stage.html?mode=film3`;
async function openPage(w = W, h = H) {
  const browser = await chromium.launch({ args: LAUNCH_ARGS });
  const page = await browser.newPage({ viewport: { width: Math.min(w, 1200), height: Math.min(h, 1200) } });
  page.on('pageerror', e => console.log('[pageerror]', e.message));
  page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console.log('[page]', m.text()); });   // warnings too: a prop that failed to build says so
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
// (cycle 13) --probe: the key poses of the gags declared in the script (st.gag in story_kit -> script.gags [{t, who, name}]), measured by the engine
// (engine/director3.js probe): head cut by the edge, too small to read, covered (by whom), in the caption band or under a title card. Prints one
// line per gag, writes out/work/<name>/probe.json, renders nothing else. Cheap at a small size: --w 288 --h 512.
if (flag('probe', false)) {
  const only = typeof flag('probe', false) === 'string' ? new Set(String(flag('probe')).split(',')) : null;   // --probe hic1,top2: only those gags
  const gags = (timed.gags || []).filter(g => !only || only.has(g.name)).sort((a, b) => a.t - b.t), cards = timed.cardTimes || [], res = [];
  if (!gags.length) console.log('probe: no gags declared (st.gag(...) in the story script)');
  for (const g of gags) {
    const [r] = await A.page.evaluate(({ t, sp }) => window.__engine.probe(t, [sp]), { t: g.t, sp: g });
    const w = [];
    if (r.err) w.push(r.err);
    else {
      const [x0, y0, x1, y1] = r.box;
      if (r.behind) w.push('behind the camera');
      if (x0 < 0) w.push(`cut by the left edge (${Math.round(-x0 / Math.max(1e-6, x1 - x0) * 100)} % of the head)`);
      if (x1 > 1) w.push(`cut by the right edge (${Math.round((x1 - 1) / Math.max(1e-6, x1 - x0) * 100)} % of the head)`);
      if (y0 < 0) w.push(`cut by the top (${Math.round(-y0 / Math.max(1e-6, r.h) * 100)} % of the head)`);
      if (y1 > 1) w.push(`cut by the bottom (${Math.round((y1 - 1) / Math.max(1e-6, r.h) * 100)} % of the head)`);
      if (g.prop) {   // a prop that carries text: big enough, turned to us
        if (r.h < 0.035) w.push(`${Math.round(r.h * 1000) / 10} % of the frame height: under 3.5 % its lettering will not read at phone size`);
        if (r.facing > 60) w.push(`turned ${r.facing} deg away from the lens`);
      } else if (r.h < 0.06) w.push(`head ${Math.round(r.h * 100)} % of the frame height: too small to read the face at phone size (7 % or more)`);
      if (r.seen < 0.67) w.push(`only ${Math.round(r.seen * 100)} % of the ${g.prop ? 'prop' : 'head'} seen` + (Object.keys(r.cover).length ? ': covered by ' + Object.entries(r.cover).map(([k, n]) => `${k} (${n}/9)`).join(', ') : ''));
      const capOv = Math.max(0, Math.min(y1, 0.86) - Math.max(y0, 0.77)) / Math.max(1e-6, r.h);
      if (capOv > 0.3) w.push(`${Math.round(capOv * 100)} % of the head in the caption band (y 0.77-0.86)`);
      const card = cards.find(c => g.t >= c - 0.05 && g.t < c + 1.0), cardOv = card != null ? Math.max(0, Math.min(y1, 0.2) - Math.max(y0, 0.06)) / Math.max(1e-6, r.h) : 0;
      if (cardOv > 0.2) w.push(`${Math.round(cardOv * 100)} % of the head under the title card (y 0.06-0.20, card at ${card.toFixed(2)} s)`);
    }
    res.push({ ...g, ...r, warnings: w });
    console.log(`  ${w.length ? '!' : 'ok'} ${g.prop ? 'text' : 'gag '} ${(g.name || '').padEnd(14)} ${g.t.toFixed(2)} s ${g.prop ? 'prop:' + g.prop : g.who}` + (r.box ? `: ${g.prop ? 'height' : 'head'} ${Math.round(r.h * 1000) / 10} %, seen ${Math.round(r.seen * 100)} %` + (g.prop ? `, facing ${r.facing} deg` : '') : '') + (w.length ? ' -- ' + w.join('; ') : ''));
  }
  fs.writeFileSync(path.join(work, 'probe.json'), JSON.stringify(res, null, 1));
  await A.browser.close(); srv.close(); process.exit(0);
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
// --range a:b (seconds): only that part of the film (to re-render one shot and splice it in)
const range = flag('range', null), [R0, R1] = range ? String(range).split(':').map(Number) : [0, A.tl.duration];
const F0 = Math.max(0, Math.round(R0 * FPS)), N = Math.min(Math.ceil(A.tl.duration * FPS), Math.round(R1 * FPS)), per = Math.ceil((N - F0) / workers), t0 = Date.now();
let done = 0;
const segs = await Promise.all(Array.from({ length: workers }, async (_, wi) => {
  const a = F0 + wi * per, b = Math.min(N, a + per); if (a >= b) return null;
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

if (timedMode) { fs.copyFileSync(silent, outFile); console.log('wrote', outFile, '(silent, timed)'); process.exit(0); }
// 4) audio mix (voice + synced SFX + ambience + music stems), mux at -14 LUFS, SRT + script next to the video
py(path.join(ROOT, 'tools/audio3.py'), 'mix', timedPath, path.join(work, 'events.json'), work);
spawnSync('ffmpeg', ['-y', '-v', 'error', '-i', silent, '-i', path.join(work, 'mix.wav'), '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=7', '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', '-shortest', outFile], { stdio: 'inherit' });
const base = outFile.replace(/\.mp4$/, '');
py(path.join(ROOT, 'tools/audio3.py'), 'srt', timedPath, base + '.srt');
fs.writeFileSync(base + '.script.txt', timed.scenes.map(s => `## ${s.id} (${s.set})\n` + s.lines.map(l => `[${l.start.toFixed(2)}–${l.end.toFixed(2)}] ${l.speaker ? l.speaker.toUpperCase() + ' : ' : ''}${l.text}`).join('\n')).join('\n\n'));
if (!preview) for (const st of ['voice', 'sfx', 'music']) fs.copyFileSync(path.join(work, st + '.wav'), `${base}.${st}.wav`);
console.log('wrote', outFile);
