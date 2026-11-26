// prop_smoke_minuterie.mjs ENGINE_DIR: builds every case of the props of story 113 « La minuterie » at several times and fails on any error, warning or NaN.
// Usage from absurd-shorts/: node <this file> $PWD/engine
globalThis.Image = class { set src(v) { setTimeout(() => this.onerror && this.onerror(), 0); } };
globalThis.window = globalThis; globalThis.devicePixelRatio = 1;
const ctx = new Proxy({}, { get: (t, k) => (k === 'createLinearGradient' || k === 'createRadialGradient' || k === 'createPattern') ? () => ({ addColorStop() {} }) : (k === 'getImageData' ? () => ({ data: new Uint8ClampedArray(4) }) : (k === 'measureText' ? () => ({ width: 10 }) : (typeof k === 'string' ? () => {} : undefined))), set: () => true });
globalThis.document = { createElement: () => ({ getContext: () => ctx, width: 0, height: 0, style: {} }) };
const [dir] = process.argv.slice(2);
const m = await import(dir + '/props.js');
const CASES = [
  ['mnStairwell', {}], ['mnStairwell', { lit: [[0, 1], [0.5, 0]], front: true, flicker: [[0.2, 0.4]] }], ['mnStairwell', { from: 5, top: 7, hall: false }], ['mnStairwell', { top: 3 }],
  ['mnButtons', {}], ['mnButtons', { floors: [3], big: false, press: [[3, 0.3]], glow: [[0, 0.2], [0.5, 1]] }], ['mnButtons', { dots: true, size: 1.3, press: [[0, 0.1], [7, 0.5]] }],
  ['mnDarkLines', {}], ['mnDarkLines', { from: 2, top: 4 }],
  ['mnTimerBox', { open: [[0, 0], [0.4, 1]], hand: [[0, 1], [0.5, 0.5, 'step']], click: [0.5] }], ['mnTimerBox', {}],
  ['mnTrolley', { bump: [0.2, 0.9] }], ['mnTrolley', {}], ['mnClipboard', { tick: [0.3, 0.9] }], ['mnClipboard', {}], ['mnTicketRoll', { tear: [0.2, 0.8] }], ['mnTicketRoll', {}],
  ['mnCoins', { n: 6, count: [[0, 3], [0.5, 6]] }], ['mnCoins', {}], ['mnTowel', { sway: true }], ['mnBottle', {}], ['mnDoormat', {}], ['mnPiano', { wobble: [[0, 1]] }], ['mnPiano', {}],
  ['mnPodium', {}], ['mnMedal', { lift: [[0, 0], [0.5, 1]] }], ['mnMedal', {}], ['mnAnkleWeight', {}], ['mnSwollen', { grow: [[0, 0], [0.4, 1.2], [0.6, 1]] }], ['mnSwollen', {}],
  ['mnTieRope', { spin: 1.8, t0: 0.1 }], ['mnGhost', { at: 0.2 }], ['mnStrips', { from: 0.1, phase: 0.05 }], ['mnFloorLamp', {}], ['mnFloorLamp', { on: false }], ['mnGeranium', { water: [[0.1, 0.8]] }],
  ['mnPaper', {}], ['mnKey', { turn: [[0, 0], [0.4, 1.5]] }]];
let bad = 0; console.warn = (...a) => { bad++; console.log('WARN', ...a); };
for (const [n, o] of CASES) { try { if (!m.PROP_NAMES.includes(n)) throw new Error('not registered'); const p = m.buildProp(n, o); for (const t of [0, 0.3, 0.55, 0.9, 1.5, 3]) p.userData.update?.(t);
  let nm = 0, nan = 0; p.traverse(c => { if (c.isMesh) { nm++; const a = c.geometry.attributes.position.array; for (let i = 0; i < a.length; i++) if (!Number.isFinite(a[i])) { nan++; break; } } });
  if (nan) { bad++; console.log('NaN', n, nan); } console.log('ok', n, nm, 'meshes'); } catch (e) { bad++; console.log('ERR', n, e.message, (e.stack || '').split('\n')[1]); } }
console.log(bad ? `${bad} problem(s)` : `all ${CASES.length} props built`); process.exit(bad ? 1 : 0);
