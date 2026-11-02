// Tiny static server for the engine (ES modules + import map to node_modules/three).
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.wav': 'audio/wav', '.glb': 'model/gltf-binary', '.webp': 'image/webp', '.jpg': 'image/jpeg' };
export function startServer(port = 0) {
  return new Promise(res => {
    const srv = http.createServer((req, resp) => {
      const u = decodeURIComponent(new URL(req.url, 'http://x').pathname);
      const f = path.join(ROOT, u === '/' ? '/render/stage.html' : u);
      if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { resp.writeHead(404); return resp.end('nf'); }
      resp.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' });
      fs.createReadStream(f).pipe(resp);
    });
    srv.listen(port, '127.0.0.1', () => res(srv));
  });
}
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const s = await startServer(Number(process.env.PORT || 5179));
  console.log('serving on http://127.0.0.1:' + s.address().port);
}
