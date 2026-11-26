// prop_smoke_moutons.mjs ENGINE_DIR: builds every case of the props of story 111 « Les moutons » at several times and fails on any error, warning or NaN.
// Usage from absurd-shorts/: node pipeline/prop_smoke_moutons.mjs $PWD/engine
globalThis.Image = class { set src(v) { setTimeout(() => this.onerror && this.onerror(), 0); } };
globalThis.window = globalThis; globalThis.devicePixelRatio = 1;
const ctx = new Proxy({}, { get: (t, k) => (k === 'createLinearGradient' || k === 'createRadialGradient' || k === 'createPattern') ? () => ({ addColorStop() {} }) : (k === 'getImageData' ? () => ({ data: new Uint8ClampedArray(4) }) : (k === 'measureText' ? () => ({ width: 10 }) : (typeof k === 'string' ? () => {} : undefined))), set: () => true });
globalThis.document = { createElement: () => ({ getContext: () => ctx, width: 0, height: 0, style: {} }) };
const [dir] = process.argv.slice(2);
const m = await import(dir + '/props.js');
const CASES = [
  ['mtSheep', {}], ['mtSheep', { black: true, hops: [[0.1, 0.4, [0, 0, 1.2], 0.7]], yaw: [[0, 0], [0.6, 1.2]], head: [[0.5, 0.6]], nod: [0.3, 0.9], blinks: [0.4] }],
  ['mtSheep', { black: true, back: [[0, 1]], tap: [0.3, 0.8], snore: [[0, 3]], expr: [[0, 'closed']] }], ['mtSheep', { s: 0.6, clip: [[0, 'sit']], chew: [[0, 2]], bleat: [0.5] }],
  ['mtSheep', { vanish: 0.4 }], ['mtSheep', { appear: 0.2, shake: [[0.3, 1.5]], chin: [[0, 0.3]], sq: [[0, [1, 1, 1]], [0.5, [1.2, 0.8, 1.2]]], bob: 0.05, pop: [0.2, 0.9] }],
  ['mtFleece', { fill: [{ kind: 'box', x: [-2, 2], y: [0, 2], z: [-2, 0], n: 60 }, { kind: 'layer', x: [-5, 5], z: [-5, 5], n: 40 }, { kind: 'heap', c: [0, 0, 0], r: 1, h: 1, n: 20 }, { kind: 'ramp', a: [0, 2, -2], b: [0, 0, 1], w: 1, n: 30 }, { kind: 'pts', pts: [[0, 1, 0, 1]] }] }],
  ['mtFleece', { fill: [{ kind: 'box', x: [-1, 1], y: [0, 1], z: [-1, 1], n: 30 }], grow: [0.1, 0.8], bob: 0.03 }], ['mtFleece', { fill: [{ kind: 'layer', x: [-3, 3], z: [-3, 3], n: 30 }], shrink: [0.2, 0.6] }],
  ['mtFleece', { fill: [{ kind: 'ramp', a: [0, 2, -2], b: [0, 0, 1], w: 1, n: 30 }], front: { dir: [0, -1, 1], from: -2, to: 2, t0: 0, t1: 1 } }], ['mtFleece', { fill: [] }],
  ['mtFence', {}], ['mtFence', { pop: 0.2, rattle: [0.6], len: 2, h: 0.9 }],
  ['mtBubble', {}], ['mtBubble', { state: [[0, 0], [0.5, 1], [1, 2]], night: true, sheep: true, pop: 0.1, period: 0.8, t0: 0.2, w: 2.2 }],
  ['mtWoolHair', { pop: 0.3, bob: 0.05 }], ['mtWoolHair', {}],
  ['mtPlough', { speed: 2 }], ['mtPlough', { roll: false }], ['mtStall', {}], ['mtCup', {}],
  ['mtRope', { a: [[0, [0, 1, 0]], [0.5, [1, 1, 0]]], chain: [[0, 0.6, 1], [0.5, 0.6, 1.5]] }], ['mtRope', { chainK: [[[0, [0, 0.6, 1]], [1, [0.5, 0.6, 1]]]] }],
  ['mtCape', {}], ['mtFeltHat', {}], ['mtCrook', {}], ['mtEyeshade', {}], ['mtSleeve', {}], ['mtLedger', { flip: [0.2, 5, 0.08] }], ['mtLedger', {}],
  ['mtDeskLamp', {}], ['mtStudio', {}], ['mtBowTie', {}], ['mtPencil', {}], ['mtJumper', { color: '#5E8C4A', pop: 0.4 }], ['mtJumper', {}],
  ['mtKnitSleeve', { pop: 0.4 }], ['mtNightWindow', { nods: [0.2, 0.6], frown: [[0, 0], [1, 1]], look: [[0, 0], [1, -1]], lean: [[0, 0], [1, 0.1]] }],
  ['mtNightRow', {}], ['mtMoon', {}], ['mtPail', {}], ['mtMilk', { at: 0.3 }], ['mtPuff', { at: 0.2 }], ['mtBlob', { pop: 0.1, vanish: 0.8 }], ['mtBlob', {}]];
let bad = 0; console.warn = (...a) => { bad++; console.log('WARN', ...a); };
for (const [n, o] of CASES) { try { if (!m.PROP_NAMES.includes(n)) throw new Error('not registered'); const p = m.buildProp(n, o); for (const t of [0, 0.15, 0.3, 0.45, 0.55, 0.9, 1.5, 3]) p.userData.update?.(t);
  let nm = 0, nan = 0; p.traverse(c => { if (c.isMesh) { nm++; const a = c.geometry.attributes.position.array; for (let i = 0; i < a.length; i++) if (!Number.isFinite(a[i])) { nan++; break; }
    if (c.isInstancedMesh) { const im = c.instanceMatrix.array; for (let i = 0; i < im.length; i++) if (!Number.isFinite(im[i])) { nan++; break; } } }
    for (const v of [c.position, c.scale]) if (![v.x, v.y, v.z].every(Number.isFinite)) nan++; });
  if (nan) { bad++; console.log('NaN', n, nan); } console.log('ok', n, nm, 'meshes'); } catch (e) { bad++; console.log('ERR', n, e.message, (e.stack || '').split('\n')[1]); } }
console.log(bad ? `${bad} problem(s)` : `all ${CASES.length} props built`); process.exit(bad ? 1 : 0);
