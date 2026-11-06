// GLB models (for instance sand3d builds made with .claude/skills/lowpoly-story-style/scripts/sand3d_models.py), loaded before the first
// frame: the director calls preload(srcsIn(script)) in load(), then the `glbModel` prop clones them synchronously, so every frame is
// a pure function of time.
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const cache = new Map();

export async function preload(urls) {
  const loader = new GLTFLoader();
  const todo = [...new Set(urls)].filter(u => u && !cache.has(u));
  await Promise.all(todo.map(u => new Promise(res => loader.load(u, g => { cache.set(u, g.scene); res(); }, undefined,
    e => { console.warn('[models] cannot load', u, e?.message || e); res(); }))));
}

export const model = url => cache.get(url) || null;

// every glbModel src in a film script: the scenes' props (and their alternates) and props in the cast
export function srcsIn(script) {
  const out = [], add = (name, opts) => { if (name === 'glbModel' && opts?.src) out.push(opts.src); };
  for (const sc of script.scenes || []) for (const p of sc.props || []) {
    add(p.name, p.opts);
    for (const a of [].concat(p.alt || [])) add(a.name || p.name, a.opts);
  }
  for (const c of Object.values(script.cast || {})) if (c.type === 'prop') add(c.name, c.opts);
  return out;
}
