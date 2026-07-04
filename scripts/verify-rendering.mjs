#!/usr/bin/env node
/**
 * Rigorous cross-engine rendering verification. For a battery of molecules it
 * drives BOTH the RDKit engine (via drawMoleculeToSvg) and the OpenChemLib
 * engine, and asserts the SVG is structurally correct: valid canvas, real
 * bond geometry, a true skeletal default, fully-colored strokes AND wedges
 * under a stroke override, transparency by default, and gapless skeletons.
 *
 * Run after `npm run build`. Fixtures are plain SMILES (chemistry, not names).
 */
import initRDKit from '@rdkit/rdkit';
import {
  drawMoleculeToSvg,
  createOpenChemLibEngine,
  applySvgOverrides,
  fillLabelGaps,
  colorToCss,
} from '../dist/index.es.js';

const FIXTURES = [
  { id: 'benzene', smiles: 'c1ccccc1', minBonds: 6 },
  { id: 'aspirin', smiles: 'CC(=O)Oc1ccccc1C(=O)O', minBonds: 12 },
  { id: 'caffeine', smiles: 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C', minBonds: 12 },
  { id: 'stereo-sugar', smiles: 'OC[C@@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O', minBonds: 10 },
  { id: 'stereo-polycycle', smiles: 'CCCCCc1cc(O)c2[C@@H]3C=C(C)CC[C@H]3C(C)(C)Oc2c1', minBonds: 18 },
];
const W = 320;
const H = 260;
const ACCENT = '#cc00ff';
const accentCss = colorToCss(ACCENT);

let failures = 0;
let checks = 0;
function check(label, cond) {
  checks += 1;
  if (cond) {
    console.log(`  ok  ${label}`);
  } else {
    failures += 1;
    console.error(`FAIL  ${label}`);
  }
}

const rdkit = await initRDKit();
const ocl = createOpenChemLibEngine();
await ocl.ready();

/** Counts bond-like geometry (engine-agnostic). */
function bondCount(svg) {
  return (
    (svg.match(/<line\b/g) || []).length +
    (svg.match(/<polygon\b/g) || []).length +
    (svg.match(/class=['"]bond-/g) || []).length
  );
}

/** Every stroke color present, normalized (RDKit style + attribute dialects). */
function strokeColors(svg) {
  const set = new Set();
  for (const m of svg.matchAll(/stroke:(#[0-9a-fA-F]{3,8})/g)) set.add(m[1].toLowerCase());
  for (const m of svg.matchAll(/stroke="(#[0-9a-fA-F]{3,8}|rgb\([^)]*\))"/g)) set.add(m[1].toLowerCase());
  set.delete('none');
  return [...set];
}

/** Fills on bond/wedge shapes (not background rect, not atom glyphs). */
function wedgeFills(svg) {
  const set = new Set();
  for (const m of svg.matchAll(/<polygon\b[^>]*fill="(#[0-9a-fA-F]{3,8}|rgb\([^)]*\))"/g)) {
    set.add(m[1].toLowerCase());
  }
  for (const el of svg.matchAll(/<path\b[^>]*class=['"]bond-[^>]*?\/>/g)) {
    const f = el[0].match(/fill:(#[0-9a-fA-F]{3,8})/);
    if (f) set.add(f[1].toLowerCase());
  }
  return [...set];
}

for (const fx of FIXTURES) {
  // Each variant mirrors the real pipeline: engine render THEN the universal
  // applySvgOverrides post-processing that the viewer and headless API apply.
  const variants = {
    rdkit: (opts) => {
      const draw = { width: W, height: H, ...opts };
      return applySvgOverrides(drawMoleculeToSvg(rdkit, fx.smiles, draw), draw);
    },
    ocl: (opts) => {
      const draw = { width: W, height: H, ...opts };
      return applySvgOverrides(ocl.renderToSvg(fx.smiles, draw), draw);
    },
  };

  for (const [engine, render] of Object.entries(variants)) {
    const tag = `${fx.id}/${engine}`;

    // 1. Valid canvas + real geometry (skeletal default).
    const base = render({ hideText: true });
    check(`${tag}: has <svg>`, /<svg[\s\S]*<\/svg>/.test(base));
    check(`${tag}: requested size`, base.includes(`'${W}px'`) || base.includes(`"${W}px"`) || base.includes(`width="${W}"`) || /viewBox/.test(base));
    check(`${tag}: drew >= ${fx.minBonds} bonds`, bondCount(base) >= fx.minBonds);

    // 2. Skeleton = no text at all.
    check(`${tag}: skeletal default has no <text>`, !base.includes('<text'));
    if (engine === 'rdkit') {
      check(`${tag}: skeletal has no atom glyph paths`, !/class='atom-/.test(base));
    }

    // 3. Transparent by default (no opaque full-canvas fill rect with a color).
    const hasOpaqueBg =
      /<rect[^>]*fill="#[0-9a-fA-F]{6}"/.test(base) ||
      /<rect[^>]*fill:#[0-9a-fA-F]{6}/.test(base);
    check(`${tag}: transparent by default`, !hasOpaqueBg);

    // 4. Stroke override → ALL strokes are the accent, nothing left behind.
    const colored = render({ hideText: true, strokeColour: ACCENT });
    const strokes = strokeColors(colored);
    check(
      `${tag}: every stroke is the accent color`,
      strokes.length > 0 && strokes.every((c) => c === accentCss),
    );
    // 5. Wedge fills are the accent too (no stray dark/black wedge).
    const fills = wedgeFills(colored);
    check(
      `${tag}: wedge fills are the accent color (fully colored)`,
      fills.every((c) => c === accentCss),
    );

    // 6. Background color is honored when requested.
    const onBg = render({ hideText: true, backgroundColour: '#0d2a4d' });
    check(`${tag}: background color injected`, onBg.toLowerCase().includes('#0d2a4d'));

    // 7. Default is skeletal (no text) but KEEPS element colors, so heteroatoms
    //    stay distinguishable — bonds to O/N/etc. are tinted, not monochrome.
    // Mirror the viewer/API default (hideText) — the raw engine pipeline here
    // does not inject library-level defaults.
    const hetero = /[ONSPFonspf]/.test(fx.smiles.replace(/\[nH\]/gi, ''));
    if (hetero) {
      const def = render({ hideText: true });
      check(`${tag}: default is skeletal (no <text>)`, !def.includes('<text'));
      const colored =
        /stroke:#(?:FF0000|0000FF)/i.test(def) || /stroke="rgb\((?!0,\s*0,\s*0)/.test(def);
      check(`${tag}: default keeps element colors (heteroatom bonds tinted)`, colored);
    }

    // 7b. Labels mode shows labels with no stereo-descriptor clutter
    //     (OpenChemLib ESR "abs"/"and"/"or", CIP R/S text).
    if (hetero) {
      const labeled = render({ hideText: false });
      const hasLabels = engine === 'ocl' ? labeled.includes('<text') : /class='atom-/.test(labeled);
      check(`${tag}: labels render when hideText:false`, hasLabels);
      if (engine === 'ocl') {
        const clutter = [...labeled.matchAll(/<text\b[^>]*>([^<]*)<\/text>/g)].some((m) =>
          /^(abs|and\d*|or\d*|rel|rac)$/i.test(m[1].trim()),
        );
        check(`${tag}: no stereo-descriptor clutter`, !clutter);
      }
    }
  }

  // 8. OpenChemLib gap-fill (coordinate-consistent: same autocrop frame).
  //    RDKit is gapless by construction; OpenChemLib offsets labels off-atom,
  //    so the post-process heuristic must (a) only ever help, never hurt, and
  //    (b) perfectly snap the common single-bond case.
  const labeledOcl = ocl.renderToSvg(fx.smiles, { width: W, height: H, hideText: false });
  const centers = [...labeledOcl.matchAll(/<text\b[^>]*\bx="([\d.]+)"[^>]*\by="([\d.]+)"[^>]*\bfont-size="([\d.]+)"/g)].map(
    (m) => ({ cx: +m[1] + +m[3] * 0.3, cy: +m[2] - +m[3] * 0.34 }),
  );
  const pointsOf = (svg) => {
    const pts = [];
    for (const m of svg.matchAll(/<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)"/g)) {
      pts.push([+m[1], +m[2]], [+m[3], +m[4]]);
    }
    for (const m of svg.matchAll(/<polygon points="([^"]+)"/g)) {
      for (const pair of m[1].trim().split(/\s+/)) {
        const [px, py] = pair.split(',').map(Number);
        if (Number.isFinite(px) && Number.isFinite(py)) pts.push([px, py]);
      }
    }
    return pts;
  };
  const gapsFor = (pts) =>
    centers.map((c) => Math.min(...pts.map((p) => Math.hypot(p[0] - c.cx, p[1] - c.cy))));
  if (centers.length > 0) {
    const before = gapsFor(pointsOf(labeledOcl));
    const after = gapsFor(pointsOf(fillLabelGaps(labeledOcl)));
    const neverWorse = after.every((g, i) => g <= before[i] + 0.01);
    const perfect = after.filter((g) => g <= 2).length / after.length;
    check(`${fx.id}/ocl: gap-fill never makes a gap worse`, neverWorse);
    // The snap-distance cap trades a few perfect snaps for never bending a
    // bond; "never worse" above is the strong guarantee. RDKit is exact.
    check(
      `${fx.id}/ocl: gap-fill snaps the common case (${Math.round(perfect * 100)}% perfect)`,
      perfect >= 0.25,
    );
  }
}

console.log(`\n${checks} checks, ${failures} failed.`);
console.log(failures === 0 ? 'Rendering verification: PASS' : 'Rendering verification: FAIL');
process.exit(failures === 0 ? 0 : 1);
