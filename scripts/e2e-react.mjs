#!/usr/bin/env node
/**
 * Dev-only end-to-end test of the React pipeline in a DOM environment:
 * renders the real MoleculeViewer (built bundle) with the OpenChemLib
 * engine — the same path a no-WebAssembly browser takes — and asserts
 * that style options actually reach the rendered SVG.
 */
import { JSDOM } from 'jsdom';

const dom = new JSDOM('<!doctype html><html><body><div id="root"></div></body></html>', {
  url: 'http://localhost/',
  pretendToBeVisual: true,
});
globalThis.window = dom.window;
globalThis.document = dom.window.document;
try {
  Object.defineProperty(globalThis, 'navigator', {
    value: dom.window.navigator,
    configurable: true,
  });
} catch {
  // Node's built-in navigator getter suffices for react-dom.
}
globalThis.HTMLElement = dom.window.HTMLElement;
globalThis.Element = dom.window.Element;
globalThis.Node = dom.window.Node;
globalThis.getComputedStyle = dom.window.getComputedStyle;

const React = (await import('react')).default;
const { createRoot } = await import('react-dom/client');
const { MoleculeViewer, createOpenChemLibEngine } = await import('../dist/index.es.js');

const ASPIRIN = 'CC(=O)Oc1ccccc1C(=O)O';
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

let failures = 0;
function check(label, condition) {
  if (condition) console.log(`  ok  ${label}`);
  else {
    failures++;
    console.error(`FAIL  ${label}`);
  }
}

const engine = createOpenChemLibEngine();
const container = document.getElementById('root');
const root = createRoot(container);

function render(options) {
  root.render(
    React.createElement(MoleculeViewer, { smiles: ASPIRIN, engine, options }),
  );
}

// 1. Default render: SVG appears, background transparent (no injected rect fill).
render({ width: 300, height: 240 });
await sleep(400);
let html = container.innerHTML;
check('viewer renders SVG via OCL engine', html.includes('<svg'));
check('default background is transparent (no bg rect)', !/<rect[^>]*fill="#/.test(html));
check('transparent checkerboard class applied', html.includes('rms-viewer__svg--transparent'));

// 2. Stroke color override reaches the DOM.
render({ width: 300, height: 240, strokeColour: '#ff0000' });
await sleep(250);
html = container.innerHTML;
check('stroke color change reaches rendered SVG', html.includes('stroke="#ff0000"'));
check('old black strokes gone', !html.includes('stroke="rgb(0,0,0)"'));

// 3. Hide text strips labels.
render({ width: 300, height: 240, hideText: true });
await sleep(250);
html = container.innerHTML;
check('hide text strips labels from rendered SVG', !html.includes('<text'));

// 4. Figma-style rounded strokes + boldness.
render({ width: 300, height: 240, roundedStrokes: true, strokeWidthScale: 2 });
await sleep(250);
html = container.innerHTML;
check('rounded caps applied', html.includes('stroke-linecap="round"'));
check('stroke width scaled', /stroke-width="2\.00"/.test(html));

// 5. Background color applies (and checkerboard class drops).
render({ width: 300, height: 240, backgroundColour: '#0d2a4d' });
await sleep(250);
html = container.innerHTML;
check('background color reaches rendered SVG', html.includes('fill="#0d2a4d"'));
check('checkerboard class removed with solid bg', !html.includes('rms-viewer__svg--transparent'));

// 6. Text recolor.
render({ width: 300, height: 240, textColour: '#123456' });
await sleep(250);
html = container.innerHTML;
check('text color change reaches rendered SVG', /<text[^>]*fill="#123456"/.test(html));

root.unmount();
console.log(failures === 0 ? '\nE2E React pipeline: all assertions passed.' : `\n${failures} E2E assertion(s) FAILED.`);
process.exit(failures === 0 ? 0 : 1);
