# react-molstruct

Zero-backend React components that turn a molecule **name** into an accurate,
publication-style **2D structure SVG** — entirely in the browser.

- **Name → SMILES** via the [PubChem PUG REST API](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest)
  (CORS-enabled; fetched directly from the browser), with an optional
  [NCI CACTUS](https://cactus.nci.nih.gov/chemical/structure) fallback.
- **SMILES → SVG** via [RDKit.js](https://www.rdkit.org/rdkitjs) (the official
  RDKit WASM build), loaded once as a singleton.
- No server, no proxy, no Next.js. A static host is all you need.

```tsx
<MoleculeViewer name="aspirin" />
```

**Live demo:** <https://balackburn.github.io/myownshit/> — deployed to GitHub
Pages by [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml)
on every push; proof that a static host with no backend is enough.

## Install

```sh
npm install react-molstruct
npm install --save-dev @rdkit/rdkit@2025.3.4-1.0.0
```

`react` / `react-dom` (≥18) are peer dependencies.

### Copy the RDKit WASM assets (required, one-time)

RDKit.js ships as a classic script + WASM pair that must be served by your app
(the MinimalLib is not an importable ES module). Copy **both** files from
`node_modules/@rdkit/rdkit/dist/` into your served public directory:

```sh
mkdir -p public/rdkit
cp node_modules/@rdkit/rdkit/dist/RDKit_minimal.js  public/rdkit/
cp node_modules/@rdkit/rdkit/dist/RDKit_minimal.wasm public/rdkit/
```

The two files must stay co-located. The default `wasmPath` is `/rdkit`; pass a
different `wasmPath` prop if you serve them elsewhere. Pin
`@rdkit/rdkit@2025.3.4-1.0.0` (the rdkit-js npm release entered a maintainer
transition in April 2026 — avoid floating `latest`).

If you use Vite in the consuming app, also add:

```ts
// vite.config.ts
export default defineConfig({
  optimizeDeps: { exclude: ['@rdkit/rdkit'] },
});
```

## Usage

### Code-driven

```tsx
import { useRef } from 'react';
import {
  MoleculeViewer,
  type DrawOptions,
  type MoleculeViewerHandle,
} from 'react-molstruct';
import 'react-molstruct/styles.css';

const options: DrawOptions = {
  bondLineWidth: 1.5,
  backgroundColour: '#fffdf5',
  addStereoAnnotation: true,
  highlight: { smarts: 'C(=O)O', color: '#ffb3b3' }, // carboxylic acid
  legend: 'aspirin',
};

export function Aspirin() {
  const viewer = useRef<MoleculeViewerHandle>(null);
  return (
    <>
      <MoleculeViewer
        ref={viewer}
        name="aspirin"
        width={420}
        height={340}
        options={options}
        onResolved={(s) => console.log('CID', s.cid, s.smiles)}
        onError={(e) => console.warn(e.code, e.message)}
      />
      <button onClick={() => viewer.current?.downloadSvg('aspirin.svg')}>
        Download SVG
      </button>
    </>
  );
}
```

Render directly from SMILES (no network call at all):

```tsx
<MoleculeViewer smiles="CC(=O)Oc1ccccc1C(=O)O" options={{ legend: 'aspirin' }} />
```

### GUI-driven

`<MoleculeControls>` is an optional panel that drives a viewer through a shared
`DrawOptions` object and exposes output actions (copy SVG, download SVG, view
source):

```tsx
import { useRef, useState } from 'react';
import {
  MoleculeControls,
  MoleculeViewer,
  type DrawOptions,
  type MoleculeViewerHandle,
} from 'react-molstruct';
import 'react-molstruct/styles.css';

export function Playground() {
  const [options, setOptions] = useState<DrawOptions>({ width: 420, height: 340 });
  const viewer = useRef<MoleculeViewerHandle>(null);
  return (
    <>
      <MoleculeViewer ref={viewer} name="caffeine" options={options} />
      <MoleculeControls options={options} onOptionsChange={setOptions} viewerRef={viewer} />
    </>
  );
}
```

## API

### `<MoleculeViewer>` props

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `name` | `string` | — | Molecule name resolved via PubChem (debounced, cached, abortable). |
| `smiles` | `string` | — | Direct SMILES; bypasses name resolution. |
| `width` / `height` | `number` | `320` / `260` | Canvas size (overridden by `options.width/height`). |
| `options` | `DrawOptions` | `{}` | Drawing customization (see below). |
| `wasmPath` | `string` | `'/rdkit'` | Base path of the copied RDKit assets. |
| `resolver` | `'pubchem' \| 'cactus' \| ResolverFn` | `'pubchem'` | Name resolver. The default tries PubChem, then CACTUS. |
| `engine` | `RenderEngine` | RDKit | Pluggable rendering engine (e.g. an OpenChemLib adapter). |
| `debounceMs` | `number` | `400` | Debounce on name changes. |
| `onResolved` | `(s: ResolvedStructure) => void` | — | Name resolved (includes `cid`, `smiles`, `source`). |
| `onError` | `(e: MolstructError) => void` | — | Typed errors, incl. non-fatal `INVALID_SMARTS`. |
| `onSvg` | `(svg: string) => void` | — | Final SVG markup whenever it changes. |
| `ariaLabel`, `renderLoading`, `renderError`, `className`, `style` | — | — | Presentation hooks. |

Ref handle: `getSvgString()`, `downloadSvg(filename?)`, `copySvgToClipboard()`.

### `DrawOptions`

Friendly, typed surface over RDKit's `get_svg_with_highlights` options. Colors
accept hex strings (`'#dc2626'`) or RDKit `[r, g, b]` floats (0–1).

`width`, `height`, `bondLineWidth`, `backgroundColour`, `highlightColour`,
`symbolColour`, `legend`, `legendFontSize`, `padding`, `rotate` (degrees),
`noAtomLabels`, `addStereoAnnotation`, `addAtomIndices`, `addBondIndices`,
`explicitMethyl`, `colorScheme` (`'default' | 'monochrome' | 'custom'`),
`customAtomPalette` (by atomic number), `highlight` (`{ smarts, color }`),
`comicMode` (best-effort — the RDKit MinimalLib may ignore it), and
`extraRDKitOptions` (raw passthrough for any other `MolDrawOptions` key).

### Errors

All failures surface as `MolstructError` with a stable `code`:
`NOT_FOUND`, `BAD_REQUEST`, `SERVER_BUSY`, `NETWORK`, `ABORTED`,
`INVALID_SMILES`, `INVALID_SMARTS` (non-fatal; rendered without highlight),
`WASM_LOAD`, `RENDER`. `describeError(error)` returns a friendly message.

### No-WebAssembly fallback (Safari Lockdown Mode etc.)

Safari Lockdown Mode and some privacy modes disable WebAssembly entirely
(`Can't find variable: WebAssembly`), so RDKit cannot run there. The library
ships a pure-JS fallback engine backed by [OpenChemLib](https://github.com/cheminfo/openchemlib-js)
(optional peer dependency, dynamically imported on first use):

```sh
npm install openchemlib
```

```tsx
import {
  MoleculeViewer,
  createOpenChemLibEngine,
  isWebAssemblyAvailable,
} from 'react-molstruct';

const engine = isWebAssemblyAvailable() ? undefined : createOpenChemLibEngine();
<MoleculeViewer name="aspirin" engine={engine} />;
```

Fidelity is below RDKit and only `width`, `height`, `bondLineWidth`, and
`addStereoAnnotation` apply; highlights, legends, palettes, and rotation are
ignored in this mode.

### Lower-level exports

`loadRDKit(wasmPath)`, `drawMoleculeToSvg(rdkit, smiles, options)`,
`isValidSmiles`, `createRDKitEngine`, `resolveWithPubChem`, `resolveWithCactus`,
`useRdkit`, `useResolvedStructure`, `useDebounce`, `MoleculeErrorBoundary`,
plus all types.

## PubChem etiquette (built in)

PubChem allows ≤5 requests/second and ≤400/minute. The built-in resolver
debounces input, caches results, spaces requests ≥220 ms apart, cancels stale
requests with `AbortController`, and backs off exponentially on HTTP 503
(`PUGREST.ServerBusy`). It uses the **2025 property names** — `SMILES`
(isomeric, preferred) and `ConnectivitySMILES` — not the deprecated
`IsomericSMILES`/`CanonicalSMILES`.

## Demo

```sh
npm install
npm run dev      # copies the RDKit assets into example/public/rdkit and serves the demo
```

Try: aspirin, caffeine, ibuprofen, glucose, acetaminophen — plus gibberish to
see the not-found state.

## Development

```sh
npm run typecheck   # tsc --noEmit
npm run build       # vite library build → dist/ (ESM + CJS + d.ts + styles.css)
npm run build:demo  # static demo build → dist-demo/
```

## License

MIT
