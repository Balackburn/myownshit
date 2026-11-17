// prop_smoke_example.mjs ENGINE_DIR: builds every case of a story's new props (here the props of story 85) at several times and fails on any error or warning.
// Usage from absurd-shorts/: node pipeline/prop_smoke_example.mjs $PWD/engine   (copy it, then replace CASES with your own props and options)
globalThis.Image = class { set src(v) { setTimeout(() => this.onerror && this.onerror(), 0); } };
globalThis.window = globalThis; globalThis.devicePixelRatio = 1;
const ctx = new Proxy({}, { get: (t, k) => (k === 'createLinearGradient' || k === 'createRadialGradient' || k === 'createPattern') ? () => ({ addColorStop() {} }) : (k === 'getImageData' ? () => ({ data: new Uint8ClampedArray(4) }) : (k === 'measureText' ? () => ({ width: 10 }) : (typeof k === 'string' ? () => {} : undefined))), set: () => true });
globalThis.document = { createElement: () => ({ getContext: () => ctx, width: 0, height: 0, style: {} }) };
const [dir] = process.argv.slice(2);
const m = await import(dir + '/props.js');
const CASES = [['parkLot', { rows: [[-10.5, -18.75, 16], [0.5, -18.75, 16]], lamps: [[0, 8]], zebra: [0, -14, 4], arrows: [[3, -5, 1.57]] }],
  ['bayCar', { blink: 'L', brake: [0.4, 0.5], hop: [[0.2, 0.3]] }], ['bayCar', { flatAt: 0.6, color: '#5E8FD0' }], ['bayCar', { dark: true, flag: ['#2E8B57', '#F2C94C'], open: 'L' }], ['bayCar', { flat: true }], ['bayCar', { clear: true, blink: 'R' }], ['parkedRows', { rows: [[0.5, -18.75, 16, 1]], skip: ['0:3'] }],
  ['flatRows', { rows: [[-10.5, -18.75, 16, -1], [0.5, -18.75, 16, 1]], skip: ['0:8'], wisps: 4 }],
  ['superStore', { clock: { base: 600, flipAt: 0.3 }, foldAt: 0.5 }], ['superStore', { folded: true, clock: { base: 590 } }], ['countdownClock', { base: 600, flipAt: 0.2 }],
  ['warMap', { red: [0.2, -0.1], blue: [0.4, 0.1] }], ['flagPin', {}], ['warship', { aim: [[0, 0], [0.5, 0.6]], counter: true, laps: [[0, 38], [0.8, 39], [1.4, 40]] }],
  ['ringRoad', { booms: 0.4, cars: [{ color: '#F2C94C', a0: 30 }, { dark: true, flag: ['#7A2E8C', '#F4F1E8'], a0: 120 }] }], ['ringRoad', { booms: 'down', grass: true }],
  ['plainCheese', {}], ['cheeseShelf', {}], ['laserDot', { pts: [[0, 0, 1, 0], [1, 0.2, 1.4, 0]], src: [3, 2, 4] }], ['bombDrop', { drops: [{ from: [0, 20, 0], to: [0, 0.5, 0], t0: 0.2, dur: 0.8 }] }],
  ['hubcap', {}], ['tankTower', {}], ['bayFlag', { plantAt: 0.4 }], ['borderPost', { open: [[0.5, 80]], gantry: true }], ['bayTape', { stretch: [0.2, 1.0] }], ['fullTrolley', {}], ['emptyWallet', {}], ['plainTank', { turret: [[0, 0.5]] }], ['tankTower', { sway: 0.4 }], ['coinDrop', { from: [0, 1.6, 0], to: [0, 1.2, 0], at: 0.3 }], ['superStore', { foldAt: 0.2, staged: true, clock: { base: 590 } }], ['warship', { gunS: 1.6, aim: [[0, 0.3]] }], ['bombDrop', { hang: 0.2, drops: [{ from: [0, 20, 0], to: [0, 0.5, 0], t0: 0.2, dur: 0.8 }] }], ['bayCar', { blink: 'both', indS: 1.8, glow: 0.9, blinkP: 0.55, clear: true, dash: 'R' }], ['helmetLine', { path: [[0, 0], [5, 0], [5, 30]] }], ['bayCar', { clear: true, roofUp: 0.14, wheel: true, blink: 'R', glowY: 0.3, brake: [0.2, 0.45], brakeAmp: 0.16, skirt: true }], ['emptyWallet', { s: 1.8, slots: true, open: 1.1 }], ['moth', { from: [0, 1.4, 0], to: [0.2, 2.6, 0], at: 0.4 }], ['jetShadows', { jets: [[0, 0], [-4, 5], [4, 5]], t0: 0.1, t1: 0.5, z0: 20, z1: -30 }]];
let bad = 0; console.warn = (...a) => { bad++; console.log('WARN', ...a); };
for (const [n, o] of CASES) { try { const p = m.buildProp(n, o); for (const t of [0, 0.3, 0.55, 0.9, 1.5, 3]) p.userData.update?.(t); let nm = 0; p.traverse(c => { if (c.isMesh) nm++; }); console.log('ok', n, nm, 'meshes'); } catch (e) { bad++; console.log('ERR', n, e.message, e.stack.split('\n')[1]); } }
console.log(bad ? `${bad} problem(s)` : `all ${CASES.length} props built`); process.exit(bad ? 1 : 0);
