// Full pipeline: script.json -> TTS + timings -> frames (headless Chromium) -> mix -> MP4.
//   node render/render.mjs scripts-fr/pigeon.json [--out out/pigeon.mp4] [--w 720 --h 1280 --fps 30]
//                          [--stills 0.5,3,7.2]  (only write PNG stills at those times, for QA)
//                          [--no-tts] (use estimated durations, silent video)
import { spawnSync, spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { chromium, LAUNCH_ARGS } from './pw.mjs';
import { startServer } from './server.mjs';

const args = process.argv.slice(2);
const flag = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? (args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : true) : d; };
const scriptPath = args.find(a => a.endsWith('.json'));
if (!scriptPath) { console.error('usage: node render/render.mjs <script.json> [--out file.mp4] [--stills t1,t2] [--no-tts]'); process.exit(1); }
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const name = path.basename(scriptPath, '.json');
const work = path.join(ROOT, 'out', 'work', name); fs.mkdirSync(work, { recursive: true });
const outFile = path.resolve(flag('out', path.join(ROOT, 'out', name + '.mp4')));
const W = +flag('w', 720), H = +flag('h', 1280), FPS = +flag('fps', 30);
const noTTS = !!flag('no-tts', false);
const stills = flag('stills', null);

// 1) narration + timing
let timedPath = path.join(work, 'script.timed.json');
if (noTTS) { fs.copyFileSync(scriptPath, timedPath); }
else {
  const r = spawnSync('python3', [path.join(ROOT, 'tools/audio.py'), 'tts', path.resolve(scriptPath), work], { stdio: 'inherit' });
  if (r.status) process.exit(r.status);
}
const script = JSON.parse(fs.readFileSync(timedPath, 'utf8'));

// 2) frames
const srv = await startServer();
const browser = await chromium.launch({ args: LAUNCH_ARGS });
const page = await browser.newPage({ viewport: { width: W, height: H } });
page.on('pageerror', e => console.log('[pageerror]', e.message));
page.on('console', m => { if (['error', 'warning'].includes(m.type())) console.log('[page]', m.text()); });
await page.goto(`http://127.0.0.1:${srv.address().port}/render/stage.html?mode=film`);
await page.waitForFunction(() => window.__ready, null, { timeout: 60000 });
const tl = await page.evaluate(async ({ script, W, H }) => window.__engine.load(script, { width: W, height: H }), { script, W, H });
console.log(`timeline ${tl.duration.toFixed(2)}s, ${tl.shots.length} shots`);

if (stills) {
  // --stills shots  -> one still per shot at 60 % of its length (+ contact sheet); else explicit times
  const ts = String(stills) === 'shots' ? tl.shots.map(sh => +(sh.start + sh.duration * 0.6).toFixed(2)) : String(stills).split(',').map(Number);
  for (const t of ts) {
    await page.evaluate(t => window.__engine.renderFrame(t), t);
    const data = await page.evaluate(() => window.__engine.frameDataURL('image/png'));
    const f = path.join(work, `still_${t.toFixed(2)}.png`); fs.writeFileSync(f, Buffer.from(data.split(',')[1], 'base64')); console.log('still', f);
  }
  await browser.close(); srv.close();
  const files = ts.map(t => path.join(work, `still_${t.toFixed(2)}.png`));
  const cols = Math.min(6, files.length), rows = Math.ceil(files.length / cols);
  const sheet = path.join(work, 'contact.png');
  spawnSync('ffmpeg', ['-y', '-v', 'error', ...files.flatMap(f => ['-i', f]), '-filter_complex',
    files.map((_, i) => `[${i}]scale=240:-1[s${i}]`).join(';') + ';' + files.map((_, i) => `[s${i}]`).join('') +
    `xstack=inputs=${files.length}:layout=` + files.map((_, i) => `${(i % cols) ? Array.from({ length: i % cols }, () => 'w0').join('+') : '0'}_${Math.floor(i / cols) ? Array.from({ length: Math.floor(i / cols) }, () => 'h0').join('+') : '0'}`).join('|') + ':fill=black', sheet]);
  console.log('contact sheet', sheet);
  process.exit(0);
}

const silent = path.join(work, 'video.mp4');
const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'medium', '-crf', '19', silent], { stdio: ['pipe', 'inherit', 'inherit'] });
const N = Math.ceil(tl.duration * FPS); const t0 = Date.now();
for (let i = 0; i < N; i++) {
  const data = await page.evaluate(t => { window.__engine.renderFrame(t); return window.__engine.frameDataURL('image/jpeg', 0.93); }, i / FPS);
  if (!ff.stdin.write(Buffer.from(data.split(',')[1], 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
  if (i % 30 === 0) process.stdout.write(`\rframe ${i}/${N}  ${((i + 1) / ((Date.now() - t0) / 1000)).toFixed(1)} fps   `);
}
ff.stdin.end(); await new Promise(r => ff.on('close', r));
await browser.close(); srv.close();
console.log('\nframes done');

// 3) audio mix + mux
if (noTTS) { fs.copyFileSync(silent, outFile); console.log('wrote (silent)', outFile); process.exit(0); }
const mix = path.join(work, 'mix.wav');
let r = spawnSync('python3', [path.join(ROOT, 'tools/audio.py'), 'mix', timedPath, mix], { stdio: 'inherit' });
if (r.status) process.exit(r.status);
// loudness: -14 LUFS integrated / -1.5 dBTP, the usual target for TikTok / Reels / Shorts
r = spawnSync('ffmpeg', ['-y', '-v', 'error', '-i', silent, '-i', mix, '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=7', '-ar', '44100', '-c:a', 'aac', '-b:a', '160k', '-shortest', outFile], { stdio: 'inherit' });
console.log(r.status ? 'mux failed' : 'wrote ' + outFile);
