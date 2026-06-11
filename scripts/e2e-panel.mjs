#!/usr/bin/env node
/**
 * Dev-only interaction test for the MoleculeControls panel: mounts the real
 * component (built bundle) in a DOM, drives tabs/switches/presets/shuffle
 * with native events, and asserts the options object actually changes.
 */
import { JSDOM } from 'jsdom';

const dom = new JSDOM('<!doctype html><html><body><div id="root"></div></body></html>', {
  url: 'http://localhost/',
  pretendToBeVisual: true,
});
globalThis.window = dom.window;
globalThis.document = dom.window.document;
globalThis.HTMLElement = dom.window.HTMLElement;
globalThis.Element = dom.window.Element;
globalThis.Node = dom.window.Node;
globalThis.getComputedStyle = dom.window.getComputedStyle;

const React = (await import('react')).default;
const { createRoot } = await import('react-dom/client');
const { MoleculeControls, STYLE_PRESETS } = await import('../dist/index.es.js');

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
let failures = 0;
function check(label, condition) {
  if (condition) console.log(`  ok  ${label}`);
  else {
    failures++;
    console.error(`FAIL  ${label}`);
  }
}

let currentOptions = { width: 300, height: 240 };
function Harness() {
  const [options, setOptions] = React.useState(currentOptions);
  currentOptions = options;
  return React.createElement(MoleculeControls, {
    options,
    onOptionsChange: setOptions,
    engineId: 'openchemlib',
  });
}

const container = document.getElementById('root');
const root = createRoot(container);
root.render(React.createElement(Harness));
await sleep(150);

// Structure renders.
const tabs = [...container.querySelectorAll('[role="tab"]')];
check('renders 4 tabs', tabs.length === 4);
check(
  `renders ${STYLE_PRESETS.length} preset chips`,
  container.querySelectorAll('.rms-controls__preset').length === STYLE_PRESETS.length,
);
check('Style tab active by default', tabs[0]?.getAttribute('aria-selected') === 'true');
check(
  'RDKit-only rows are badged in fallback mode',
  container.querySelectorAll('.rms-controls__badge').length > 0,
);

// Toggle the "Rounded caps" switch — option must change.
const roundedSwitch = [...container.querySelectorAll('input[role="switch"]')].find(
  (input) => container.querySelector(`label[for="${input.id}"]`)?.textContent === 'Rounded caps',
);
check('finds Rounded caps switch', !!roundedSwitch);
roundedSwitch?.click();
await sleep(80);
check('toggling switch updates options.roundedStrokes', currentOptions.roundedStrokes === true);

// Apply a preset — style keys land in options.
const figmaChip = [...container.querySelectorAll('.rms-controls__preset')].find((b) =>
  b.textContent?.includes('Figma'),
);
figmaChip?.click();
await sleep(80);
check('preset click applies strokeColour', currentOptions.strokeColour === '#0d99ff');
check('preset chip shows active state', figmaChip?.className.includes('is-active') === true);

// Switch to Canvas tab — content swaps.
tabs[1].click();
await sleep(80);
check('Canvas tab activates', tabs[1].getAttribute('aria-selected') === 'true');
check(
  'Canvas tab shows Width slider',
  [...container.querySelectorAll('label')].some((l) => l.textContent === 'Width'),
);

// Export tab shows actions.
tabs[3].click();
await sleep(80);
check(
  'Export tab shows Copy SVG action',
  [...container.querySelectorAll('button')].some((b) => b.textContent === 'Copy SVG'),
);

// Shuffle changes the active preset.
const shuffleBtn = [...container.querySelectorAll('button')].find(
  (b) => b.textContent === 'Shuffle',
);
shuffleBtn?.click();
await sleep(80);
check(
  'Shuffle applies some preset style',
  currentOptions.bondLineWidth != null,
);

// Reset clears style keys but keeps canvas size.
const resetBtn = [...container.querySelectorAll('button')].find(
  (b) => b.textContent === 'Reset',
);
resetBtn?.click();
await sleep(80);
check('Reset clears stroke colour', currentOptions.strokeColour == null);
check('Reset keeps canvas size', currentOptions.width === 300 && currentOptions.height === 240);

root.unmount();
console.log(failures === 0 ? '\nPanel E2E: all assertions passed.' : `\n${failures} panel assertion(s) FAILED.`);
process.exit(failures === 0 ? 0 : 1);
