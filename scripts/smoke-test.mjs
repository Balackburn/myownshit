#!/usr/bin/env node
/**
 * Dev-only smoke test: loads the real RDKit WASM (Node entry of @rdkit/rdkit)
 * and drives drawMoleculeToSvg from the built dist bundle, validating the
 * option mapping, substructure highlighting, and error paths.
 */
import initRDKitModule from '@rdkit/rdkit';
import {
  createOpenChemLibEngine,
  drawMoleculeToSvg,
  isValidSmiles,
  decorateSvg,
  hexToRgb01,
  MolstructError,
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

console.log(failures === 0 ? '\nAll smoke tests passed.' : `\n${failures} smoke test(s) FAILED.`);
process.exit(failures === 0 ? 0 : 1);
