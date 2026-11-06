// GLB models (for instance sand3d builds made with .claude/skills/lowpoly-story-style/scripts/sand3d_models.py), loaded before the first
// frame: the director calls preload(srcsIn(script)) in load(), then the `glbModel` prop clones them synchronously, so every frame is
// a pure function of time.
import * as THREE from 'three';
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

// ---- image textures (FLUX-generated set dressing in assets/textures/), preloaded like the GLBs so frames stay deterministic
export const TEXTURES = { facades: ['/assets/textures/facade_cream.webp', '/assets/textures/facade_pink.webp', '/assets/textures/facade_grey.webp'] };
const images = new Map(), texCache = new Map();
export async function preloadImages(urls) {
  await Promise.all([...new Set(urls)].filter(u => u && !images.has(u)).map(u => new Promise(res => {
    const im = new Image(); im.onload = () => { images.set(u, im); res(); }; im.onerror = () => { console.warn('[models] cannot load image', u); res(); }; im.src = u; })));
}
export const allTextures = () => Object.values(TEXTURES).flat();
export function imageTexture(url) {
  if (texCache.has(url)) return texCache.get(url);
  const im = images.get(url); if (!im) return null;
  const t = new THREE.Texture(im); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; t.needsUpdate = true; texCache.set(url, t); return t;
}
