# react-molstruct — API & embedding guide

Three ways to turn a molecule **name** (or SMILES) into a 2D **SVG**:

1. [`renderMoleculeSvg()`](#1-rendermoleculesvg-headless-js) — one async call, no React, runs in the browser, Node, or a serverless function.
2. [`<iframe>` embed](#2-iframe-embed-no-build-step) — paste a URL on any site. No build step, no API key.
3. [React components](#3-react-components) — `<MoleculeViewer>` + `<MoleculeControls>` for interactive UIs.

Rendering is **client-side**: names resolve through the public [PubChem PUG REST](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest) API and structures are drawn locally. The default depiction is a **transparent skeletal** structure (no atom labels, no stereo annotations, bonds meeting cleanly at vertices). Pass `hideText: false` to show atom labels.

---

## 1. `renderMoleculeSvg()` (headless JS)

```ts
import { renderMoleculeSvg } from 'react-molstruct';

// By name (resolves via PubChem):
const { svg, smiles, cid, resolvedAs } = await renderMoleculeSvg('aspirin', {
  width: 320,
  strokeColour: '#0000ee',
});

// By SMILES (no network call):
const { svg } = await renderMoleculeSvg('', { smiles: 'CCO' });
```

By default it uses the pure-JS **OpenChemLib** engine, so there are **no WASM assets to host** — it works in Node and any browser. Install the optional peer once:

```sh
npm install react-molstruct openchemlib
```

For higher-fidelity RDKit output, pass an engine (requires hosting the RDKit WASM assets — see [§3](#3-react-components)):

```ts
import { renderMoleculeSvg, createRDKitEngine } from 'react-molstruct';
const { svg } = await renderMoleculeSvg('caffeine', { engine: createRDKitEngine('/rdkit') });
```

### Returns — `RenderMoleculeResult`

| Field | Type | Description |
| --- | --- | --- |
| `svg` | `string` | The SVG markup, with `<title>`/`<desc>` accessibility metadata. |
| `smiles` | `string` | SMILES the structure was drawn from. |
| `cid` | `number?` | PubChem compound id, when resolved through PubChem. |
| `resolvedAs` | `string?` | The name that actually matched, when it differs from the query. |
| `source` | `'pubchem' \| 'cactus' \| 'direct' \| 'custom'` | Where the structure came from. |

Failures throw a typed `MolstructError` with a `code` (`NOT_FOUND`, `NETWORK`, `INVALID_SMILES`, …); `describeError(err)` returns a friendly message.

### Options — `RenderMoleculeOptions`

Everything in [`DrawOptions`](#drawoptions-reference) plus: `smiles`, `resolver` (`'pubchem' | 'cactus' | fn`), `engine`, `signal` (`AbortSignal`), and `title`.

### Node / serverless example

```ts
import { renderMoleculeSvg } from 'react-molstruct';

export default async function handler(req, res) {
  const { svg } = await renderMoleculeSvg(req.query.name ?? 'aspirin', {
    width: Number(req.query.w) || 320,
    strokeColour: req.query.stroke,
  });
  res.setHeader('content-type', 'image/svg+xml');
  res.send(svg);
}
```

---

## 2. `<iframe>` embed (no build step)

Point an iframe at the hosted `embed.html` with query parameters. Live demo + copy-paste builder: <https://balackburn.github.io/myownshit/>

```html
<iframe
  src="https://balackburn.github.io/myownshit/embed.html?name=aspirin&width=320&stroke=0000ee"
  style="border:0;width:320px;height:260px"
  loading="lazy"
  title="aspirin structure"
></iframe>
```

The embed posts a `{ type: 'molstruct:size', height }` message to the parent window so you can size the iframe responsively:

```js
addEventListener('message', (e) => {
  if (e.data?.type === 'molstruct:size') iframe.style.height = e.data.height + 'px';
});
```

### URL parameters

| Param | Meaning | Example |
| --- | --- | --- |
| `name` (or `q`) | Molecule name to resolve | `name=ibuprofen` |
| `smiles` | Direct SMILES (skips name lookup) | `smiles=CCO` |
| `width` (`w`), `height` (`h`) | Canvas size in px | `width=400` |
| `bond` | Bond line width | `bond=2` |
| `scale` | Stroke-width multiplier | `scale=1.5` |
| `stroke` | Stroke color (hex, no `#`, or CSS name) | `stroke=0000ee` |
| `text` | Atom-label color (only with `labels=1`) | `text=171717` |
| `bg` | Background color; omit for transparent | `bg=ffffff` |
| `rounded` | Rounded line caps (Figma look) | `rounded=1` |
| `rotate` | Rotation in degrees | `rotate=30` |
| `labels` | `1` shows atom labels (default skeletal) | `labels=1` |
| `stereo` | `1` shows stereo annotations | `stereo=1` |

Colors accept `rrggbb`, `#rrggbb`, a CSS name, or `none`/`transparent`.

---

## 3. React components

### `<MoleculeImage>` — zero-config (recommended)

The simplest drop-in: give it a name, it generates the SVG. No stylesheet
import, no asset hosting required (it auto-uses RDKit when available and falls
back to the pure-JS engine otherwise).

```tsx
import { MoleculeImage } from 'react-molstruct';

<MoleculeImage name="aspirin" />;                              // skeletal default
<MoleculeImage name="caffeine" options={{ hideText: false }} />; // with labels
<MoleculeImage smiles="CCO" width={240} options={{ strokeColour: '#0000ee' }} />;
```

Props: `name` / `smiles`, `width`, `height`, `options` (DrawOptions),
`resolver`, `wasmPath`, `alt`, `onResolved`, `onError`, `loading`,
`errorFallback`, `className`, `style`. It resolves, renders, and re-renders on
prop changes, aborting stale work automatically.

### `<MoleculeViewer>` — interactive

```tsx
import { MoleculeViewer } from 'react-molstruct';
import 'react-molstruct/styles.css';

<MoleculeViewer name="aspirin" />;
```

`<MoleculeViewer>` is RDKit-first (copy `RDKit_minimal.js` + `RDKit_minimal.wasm`
from `@rdkit/rdkit/dist` into your served `public/rdkit/`, or pass `wasmPath`),
with a ref API (`getSvgString`, `downloadSvg`, `downloadPng`,
`copySvgToClipboard`) and the optional `<MoleculeControls>` panel. For browsers
without WebAssembly, pass `engine={createAutoEngine(wasmPath)}` to fall back to
the pure-JS engine. See the [README](../README.md) for the full prop and ref API.

---

## DrawOptions reference

Colors accept hex strings (`'#0000ee'`) or RDKit `[r, g, b]` floats (0–1).

**Universal** (work with every engine, applied by SVG post-processing):

| Option | Type | Default | Notes |
| --- | --- | --- | --- |
| `width`, `height` | `number` | `320` / `240` | Canvas size in px. |
| `hideText` | `boolean` | **`true`** | Skeletal: hide all atom labels/text; bonds fill the gaps. |
| `strokeColour` | color | — | Force one color on every bond. |
| `textColour` | color | — | Force one color on all labels (needs `hideText: false`). |
| `backgroundColour` | color | — | Omit for a fully transparent background. |
| `strokeWidthScale` | `number` | `1` | Multiply every stroke width. |
| `roundedStrokes` | `boolean` | `false` | Round line caps/joins. |

**RDKit engine only** (ignored by the OpenChemLib fallback):

`bondLineWidth`, `addStereoAnnotation` (default `false`), `addAtomIndices`, `addBondIndices`, `explicitMethyl`, `rotate`, `padding`, `legend`, `legendFontSize`, `labelFontSize`, `multipleBondOffset`, `colorScheme` (`'default' | 'monochrome' | 'custom'`), `customAtomPalette`, `highlight` (`{ smarts, color }`), `comicMode`, `extraRDKitOptions`.

> The `bondLineWidth`/stereo options also apply to OpenChemLib; the rest are RDKit-specific. Use the universal options above for output that looks identical across engines.
