---
name: verify-molstruct
description: Rigorously verify react-molstruct's molecule-to-SVG generation before shipping. Use when changing rendering, engines (RDKit/OpenChemLib), DrawOptions, skeletal/gap-fill logic, name resolution, the headless API, or the embed page — or whenever the user asks to "test", "verify it works", or "ship" molecule rendering. Confirms both engines produce structurally correct SVGs (valid canvas, real bonds, true skeletal default, fully-colored strokes AND wedges, transparency, gapless skeletons) and that the API/components work.
---

# Verify react-molstruct rendering

This project turns a molecule **name** (or SMILES) into a 2D **SVG**, entirely
client-side, via two engines: **RDKit.js** (WASM, high fidelity — used by the
website, embed, and headless API when available) and **OpenChemLib** (pure JS
fallback when WebAssembly is unavailable). Rendering correctness is the product;
verify it rigorously before shipping.

## Procedure

Run from the repo root. Always build first — the suites import the built bundle.

```sh
npm run build          # library → dist/ (must succeed with no TS errors)
npm test               # all suites below, in order
```

`npm test` runs, and each must end with a PASS / "all assertions passed" line:

1. `scripts/smoke-test.mjs` — RDKit + OpenChemLib draw, option mapping, errors.
2. `scripts/e2e-react.mjs` — `<MoleculeViewer>` in a DOM: options reach the SVG.
3. `scripts/e2e-panel.mjs` — control panel interactions mutate options.
4. `scripts/e2e-resolver.mjs` — name candidate expansion, autocomplete recovery,
   and the false-positive guard.
5. `scripts/e2e-api.mjs` — `renderMoleculeSvg()`, skeletal default, gap-fill,
   stripText, and wedge-fill recoloring.
6. `scripts/verify-rendering.mjs` — the rigorous cross-engine matrix (below).

Then verify the demo and embed build:

```sh
npm run build:demo     # multi-page (index + embed) build must succeed
```

## What "correct" means (verify-rendering.mjs asserts all of these)

For a battery of molecules (incl. stereochemistry) on **both** engines:

- **Valid canvas + geometry** — a `<svg>` at the requested size with at least
  the expected number of bond elements.
- **Skeletal default** — with no options, the output has **no `<text>`** and (RDKit)
  no atom-glyph paths. This is the product default.
- **Transparent default** — no opaque full-canvas background rect unless
  `backgroundColour` is set.
- **Stroke override fully colors everything** — with `strokeColour`, *every*
  stroke is that color and **every wedge fill** (OpenChemLib `<polygon>`,
  RDKit `bond-*` path `fill:`) is that color too. A stray dark/black wedge is a
  bug (regression test for the "wedge not fully colored" report).
- **Background honored** — `backgroundColour` injects a matching rect.
- **Labels mode** — `hideText: false` shows labels (skip all-carbon molecules).
- **Gap-fill** — RDKit skeletons are gapless by construction; OpenChemLib's
  `fillLabelGaps` must **never make a gap worse** and must snap the common
  single-bond case (>= 40% of labels land exactly on the vertex).

## Spot-check visually (optional but recommended)

`scripts/visual-test.mjs` rasterizes a labeled contact sheet (`visual-test.png`)
of every preset via sharp. Open it and confirm structures look like real
skeletal formulae with clean, fully-colored bonds and no broken gaps.

## Ship checklist

Only ship when: `npm run build` is clean, `npm test` ends green (all six suites),
`npm run build:demo` succeeds, and any rendering change is reflected in
`scripts/verify-rendering.mjs`. Then commit and push to the working branch.
If a check fails, first decide whether it is a **product** bug or a **test**
artifact (e.g. comparing two independently `autoCrop`-ed OpenChemLib frames
yields false gaps) and fix the real cause — never weaken an assertion to make
it pass.
