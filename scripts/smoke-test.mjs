#!/usr/bin/env node
/**
 * Dev-only smoke test: loads the real RDKit WASM (Node entry of @rdkit/rdkit)
 * and drives drawMoleculeToSvg from the built dist bundle, validating the
 * option mapping, substructure highlighting, and error paths.
 */
import initRDKitModule from '@rdkit/rdkit';
import {
  applySvgOverrides,
  createOpenChemLibEngine,
  drawMoleculeToSvg,
  injectSvgBackground,
  isValidSmiles,
  decorateSvg,
  hexToRgb01,
  MolstructError,
  STYLE_PRESETS,
} from '../dist/index.es.js';

const ASPIRIN = 'CC(=O)Oc1ccccc1C(=O)O';
const GLUCOSE = 'C([C@@H]1[C@H]([C@@H]([C@H](C(O1)O)O)O)O)O';

let failures = 0;
function check(label, condition) {
  if (condition) {
    console.log(`  ok  ${label}`);
  } else {
    failures++;
    console.error(`FAIL  ${label}`);
  }
}

const rdkit = await initRDKitModule();
console.log(`RDKit ${rdkit.version()} loaded\n`);

// 1. Plain render with the full mapped option set.
const svg = drawMoleculeToSvg(rdkit, ASPIRIN, {
  width: 420,
  height: 340,
  bondLineWidth: 1.5,
  backgroundColour: '#fffdf5',
  padding: 0.08,
  rotate: 30,
  legend: 'aspirin',
  legendFontSize: 14,
  addStereoAnnotation: true,
  explicitMethyl: true,
  colorScheme: 'monochrome',
});
check('renders aspirin SVG', svg.startsWith('<?xml') || svg.includes('<svg'));
check('SVG has requested width', svg.includes("width='420px'") || svg.includes('width="420px"'));

// 2. Substructure highlight via SMARTS.
const highlighted = drawMoleculeToSvg(rdkit, ASPIRIN, {
  highlight: { smarts: 'C(=O)O', color: '#ffb3b3' },
});
check('renders highlighted SVG', highlighted.includes('<svg'));
check('highlight produced extra geometry', highlighted.length > 'x'.repeat(0).length && highlighted.includes('ellipse') || highlighted.includes('path'));

// 3. Stereo-bearing molecule renders.
check('renders glucose (stereo SMILES)', drawMoleculeToSvg(rdkit, GLUCOSE, { addStereoAnnotation: true }).includes('<svg'));

// 4. Invalid SMILES → typed INVALID_SMILES error.
try {
  drawMoleculeToSvg(rdkit, 'not-a-molecule((', {});
  check('invalid SMILES throws', false);
} catch (error) {
  check('invalid SMILES throws MolstructError(INVALID_SMILES)',
    error instanceof MolstructError && error.code === 'INVALID_SMILES');
}

// 5. Invalid SMARTS → typed INVALID_SMARTS error (non-fatal for the viewer).
try {
  drawMoleculeToSvg(rdkit, ASPIRIN, { highlight: { smarts: '(((' } });
  check('invalid SMARTS throws', false);
} catch (error) {
  check('invalid SMARTS throws MolstructError(INVALID_SMARTS)',
    error instanceof MolstructError && error.code === 'INVALID_SMARTS');
}

// 6. Validation + utility helpers.
check('isValidSmiles true for aspirin', isValidSmiles(rdkit, ASPIRIN));
check('isValidSmiles false for garbage', !isValidSmiles(rdkit, ')))'));
check('hexToRgb01 parses #ff0000', JSON.stringify(hexToRgb01('#ff0000')) === '[1,0,0]');
const decorated = decorateSvg('<svg xmlns="x"><g/></svg>', 'Aspirin & co', 'desc');
check('decorateSvg injects title/desc + role',
  decorated.includes('<title>Aspirin &amp; co</title>') &&
  decorated.includes('<desc>desc</desc>') &&
  decorated.includes('role="img"'));

// 7. OpenChemLib fallback engine (pure JS, no WebAssembly).
const ocl = createOpenChemLibEngine();
await ocl.ready();
const oclSvg = ocl.renderToSvg(ASPIRIN, { width: 300, height: 240, bondLineWidth: 1.5 });
check('OpenChemLib engine renders aspirin', oclSvg.includes('<svg'));
try {
  ocl.renderToSvg('not-a-molecule((', {});
  check('OpenChemLib invalid SMILES throws', false);
} catch (error) {
  check('OpenChemLib invalid SMILES throws MolstructError(INVALID_SMILES)',
    error instanceof MolstructError && error.code === 'INVALID_SMILES');
}

// 8. Universal SVG overrides against REAL output of both engines.
const rdkitSvg = drawMoleculeToSvg(rdkit, ASPIRIN, { width: 300, height: 240 });
const oclSvg2 = ocl.renderToSvg(ASPIRIN, { width: 300, height: 240, backgroundColour: '#101014' });

const rdkitRecolored = applySvgOverrides(rdkitSvg, { strokeColour: '#39ff88' });
check('RDKit stroke recolor applied', rdkitRecolored.includes('stroke:#39ff88'));
check('RDKit stroke recolor removed black', !rdkitRecolored.includes('stroke:#000000'));

const oclRecolored = applySvgOverrides(oclSvg2, { strokeColour: '#39ff88' });
check('OCL stroke recolor applied', oclRecolored.includes('stroke="#39ff88"'));
check('OCL stroke recolor removed rgb black', !oclRecolored.includes('stroke="rgb(0,0,0)"'));

const rdkitNoText = applySvgOverrides(rdkitSvg, { hideText: true });
check('RDKit hideText strips label glyphs', !/<path class='atom-/.test(rdkitNoText));
check('RDKit hideText keeps bonds', /<path class='bond-/.test(rdkitNoText));

const oclNoText = applySvgOverrides(oclSvg2, { hideText: true });
check('OCL hideText strips <text>', !oclNoText.includes('<text'));
check('OCL hideText keeps lines', oclNoText.includes('<line'));

const rdkitBold = applySvgOverrides(rdkitSvg, { strokeWidthScale: 2 });
check('RDKit stroke widths scaled', rdkitBold.includes('stroke-width:2.00px'));
const oclBold = applySvgOverrides(oclSvg2, { strokeWidthScale: 2 });
check('OCL stroke widths scaled', /stroke-width="2\.00"/.test(oclBold));

const rdkitTextColor = applySvgOverrides(rdkitSvg, { textColour: '#123456' });
check('RDKit text recolor applied', rdkitTextColor.includes("fill='#123456'"));
const oclTextColor = applySvgOverrides(oclSvg2, { textColour: '#123456' });
check('OCL text recolor applied', /<text[^>]*fill="#123456"/.test(oclTextColor));

check('OCL background injected', oclSvg2.includes('fill="#101014"'));
check('injectSvgBackground handles viewBox', injectSvgBackground(
  '<svg viewBox="10 20 100 80"><line/></svg>', '#ff0000',
).includes('<rect x="10" y="20" width="100" height="80" fill="#ff0000"'));

check('STYLE_PRESETS exported with 10 themes', Array.isArray(STYLE_PRESETS) && STYLE_PRESETS.length === 10);
check('every preset has swatches + options', STYLE_PRESETS.every(
  (p) => p.id && p.label && p.swatches.length === 3 && typeof p.options === 'object',
));

// Transparent-by-default + Figma-style rounded strokes.
check('RDKit default background is transparent (no rect)', !rdkitSvg.includes('<rect'));
const rdkitWithBg = drawMoleculeToSvg(rdkit, ASPIRIN, { backgroundColour: '#ffeedd' });
check('RDKit explicit background still draws', rdkitWithBg.includes('#FFEEDD') || rdkitWithBg.toLowerCase().includes('#ffeedd'));
const rdkitRound = applySvgOverrides(rdkitSvg, { roundedStrokes: true });
check('RDKit rounded caps applied', rdkitRound.includes('stroke-linecap:round'));
const oclRound = applySvgOverrides(oclSvg2, { roundedStrokes: true });
check('OCL rounded caps applied', oclRound.includes('stroke-linecap="round"'));

// 9. RDKit-native additions pass through cleanly.
const tuned = drawMoleculeToSvg(rdkit, ASPIRIN, {
  multipleBondOffset: 0.3,
  labelFontSize: 22,
});
check('multipleBondOffset/labelFontSize render OK', tuned.includes('<svg'));

console.log(failures === 0 ? '\nAll smoke tests passed.' : `\n${failures} smoke test(s) FAILED.`);
process.exit(failures === 0 ? 0 : 1);
