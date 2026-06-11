#!/usr/bin/env node
/**
 * Dev-only visual test: renders caffeine through the OpenChemLib engine with
 * every style preset, asserts the style markers are present in each SVG, and
 * rasterizes a labeled contact sheet (visual-test.png) for human review.
 */
import { writeFileSync } from 'node:fs';
import sharp from 'sharp';
import {
  applySvgOverrides,
  createOpenChemLibEngine,
  colorToCss,
  STYLE_PRESETS,
} from '../dist/index.es.js';

const CAFFEINE = 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C';
const CELL_W = 360;
const CELL_H = 300;
const LABEL_H = 36;
const COLS = 5;
const ROWS = Math.ceil(STYLE_PRESETS.length / COLS);

let failures = 0;
function check(label, condition) {
  if (condition) console.log(`  ok  ${label}`);
  else {
    failures++;
    console.error(`FAIL  ${label}`);
  }
}

const engine = createOpenChemLibEngine();
await engine.ready();

const cells = [];
for (const preset of STYLE_PRESETS) {
  const options = { width: CELL_W - 32, height: CELL_H - LABEL_H - 24, ...preset.options };
  let svg = engine.renderToSvg(CAFFEINE, options);
  svg = applySvgOverrides(svg, options);

  check(`${preset.id}: renders SVG`, svg.includes('<svg'));
  if (preset.options.strokeColour) {
    const css = colorToCss(preset.options.strokeColour);
    check(`${preset.id}: stroke colour ${css} applied`, svg.includes(`stroke="${css}"`));
  }
  if (preset.options.hideText) {
    check(`${preset.id}: text hidden`, !svg.includes('<text'));
  }
  if (preset.options.roundedStrokes) {
    check(`${preset.id}: rounded caps applied`, svg.includes('stroke-linecap="round"'));
  }
  if (preset.options.backgroundColour) {
    const css = colorToCss(preset.options.backgroundColour);
    check(`${preset.id}: background ${css} injected`, svg.includes(`fill="${css}"`));
  }
  cells.push({ preset, svg: svg.replace(/<\?xml[\s\S]*?\?>/, '') });
}

// Compose a labeled contact sheet as one big SVG, then rasterize with sharp.
const sheetW = COLS * CELL_W;
const sheetH = ROWS * CELL_H;
let sheet = `<svg xmlns="http://www.w3.org/2000/svg" width="${sheetW}" height="${sheetH}" viewBox="0 0 ${sheetW} ${sheetH}">`;
sheet += `<rect width="${sheetW}" height="${sheetH}" fill="#ffffff"/>`;
cells.forEach(({ preset, svg }, index) => {
  const x = (index % COLS) * CELL_W;
  const y = Math.floor(index / COLS) * CELL_H;
  sheet += `<g transform="translate(${x},${y})">`;
  sheet += `<rect x="8" y="8" width="${CELL_W - 16}" height="${CELL_H - 16}" fill="none" stroke="rgba(0,0,0,0.12)"/>`;
  sheet += `<text x="20" y="${CELL_H - 20}" font-family="monospace" font-size="14" fill="#737373">${preset.label}</text>`;
  sheet += `<svg x="16" y="16" width="${CELL_W - 32}" height="${CELL_H - LABEL_H - 24}">${svg}</svg>`;
  sheet += `</g>`;
});
sheet += `</svg>`;

writeFileSync('visual-test.svg', sheet);
const png = await sharp(Buffer.from(sheet), { density: 110 }).png().toBuffer();
writeFileSync('visual-test.png', png);
const meta = await sharp(png).metadata();
check('contact sheet rasterized', meta.width > 0 && meta.height > 0 && png.length > 50_000);
console.log(`  sheet: visual-test.png ${meta.width}x${meta.height}, ${(png.length / 1024).toFixed(0)} kB`);

console.log(failures === 0 ? '\nVisual test: all assertions passed.' : `\n${failures} visual assertion(s) FAILED.`);
process.exit(failures === 0 ? 0 : 1);
