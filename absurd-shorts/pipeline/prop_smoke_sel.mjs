// prop_smoke_sel.mjs ENGINE_DIR: builds every case of the props of story 109 « Le sel » at several times and fails on any error, warning or NaN.
// Usage from absurd-shorts/: node <this file> $PWD/engine
globalThis.Image = class { set src(v) { setTimeout(() => this.onerror && this.onerror(), 0); } };
globalThis.window = globalThis; globalThis.devicePixelRatio = 1;
const ctx = new Proxy({}, { get: (t, k) => (k === 'createLinearGradient' || k === 'createRadialGradient' || k === 'createPattern') ? () => ({ addColorStop() {} }) : (k === 'getImageData' ? () => ({ data: new Uint8ClampedArray(4) }) : (k === 'measureText' ? () => ({ width: 10 }) : (typeof k === 'string' ? () => {} : undefined))), set: () => true });
globalThis.document = { createElement: () => ({ getContext: () => ctx, width: 0, height: 0, style: {} }) };
const [dir] = process.argv.slice(2);
const m = await import(dir + '/props.js');
const CASES = [
  ['seShaker', { fill: [[0, 1], [0.3, 0.92]], settle: [0.3] }], ['seShaker', { fill: 0 }], ['seShaker', { fill: 0.5, h: 0.5 }],
  ['seHeap', { grow: [[0, 0], [0.3, 1]] }], ['seHeap', {}], ['seGrains', { on: [[0.2, 0.8]] }],
  ['seTable', { len: 3, places: [[-1, 1], [0, -1]], chairs: [[0.5, 1], [-0.5, -1]], flutter: true }], ['seTable', { len: 1, legs: false }], ['seLeaf', {}], ['seLeaf', { len: 1.2 }],
  ['seRoast', { snow: [[0, 0], [0.5, 1]] }], ['seRoast', {}], ['seUtensil', { kind: 'knife', snow: 1 }], ['seUtensil', { kind: 'fork' }], ['seSnowCap', {}],
  ['seHighChair', { bang: [[0, 2]], pop: 0.2 }], ['seHighChair', { bonnet: '#9FD0F0' }],
  ['seScroll', { head: true, len: 2 }], ['seScroll', { len: [[0, 0.1], [1, 6]], roll: true }], ['seScroll', { tail: true, len: 1.5 }],
  ['seAwning', {}], ['seLeekCrate', {}], ['seLeek', {}], ['seFruitBowl', {}], ['seCheese', {}], ['seRadish', {}],
  ['seScarecrow', { nod: [[0, 1]] }], ['seBoard', { draw: [[0, 0], [1, 1]], shudder: [0.5] }], ['seSteam', { on: [[0.1, 2]] }], ['seSteam', {}],
  ['seMill', {}], ['seLorry', {}], ['seLorry', { color: '#C8483A' }], ['seDining', { door: [[0, 0], [0.4, 1]], slam: 0.5 }], ['seDining', {}],
  ['seWheat', { n: 400, wind: true }], ['seBib', {}], ['seChair', {}], ['seHideSet', { boxes: [[0, 1, 0, 1, 0, 1]] }], ['seFill', {}],
  ['seWildHair', {}], ['seGroundCut', { holes: [[-5, 5, 0, 9]] }], ['seScroll', { tail: true, empty: true, len: 1 }], ['seLorry', { mirrors: false }], ['seWheat', { n: 300, wind: true, gust: [[0.2, 1]] }],
  ['seScarecrow', { nod: [[0, 1]], turn: [[0, 0], [0.5, 0.6]] }], ['seDining', { ceiling: false }]];
let bad = 0; console.warn = (...a) => { bad++; console.log('WARN', ...a); };
for (const [n, o] of CASES) { try { if (!m.PROP_NAMES.includes(n)) throw new Error('not registered'); const p = m.buildProp(n, o); for (const t of [0, 0.3, 0.55, 0.9, 1.5, 3]) p.userData.update?.(t);
  let nm = 0, nan = 0; p.traverse(c => { if (c.isMesh) { nm++; const a = c.geometry.attributes.position.array; for (let i = 0; i < a.length; i++) if (!Number.isFinite(a[i])) { nan++; break; } } });
  if (nan) { bad++; console.log('NaN', n, nan); } console.log('ok', n, nm, 'meshes'); } catch (e) { bad++; console.log('ERR', n, e.message, (e.stack || '').split('\n')[1]); } }
console.log(bad ? `${bad} problem(s)` : `all ${CASES.length} props built`); process.exit(bad ? 1 : 0);
