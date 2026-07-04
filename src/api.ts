import { createAutoEngine } from './engines/auto';
import { MolstructError, toMolstructError } from './errors';
import { getResolver } from './resolvers';
import type {
  DrawOptions,
  RenderEngine,
  ResolverChoice,
  StructureSource,
} from './types';
import { decorateSvg } from './utils/svg';
import { applySvgOverrides } from './utils/svgOverrides';

/** Options for {@link renderMoleculeSvg}. Extends the full DrawOptions set. */
export interface RenderMoleculeOptions extends DrawOptions {
  /** Render this SMILES directly and skip name resolution entirely. */
  smiles?: string;
  /** Name resolver: 'pubchem' (default, with CACTUS fallback), 'cactus', or a fn. */
  resolver?: ResolverChoice;
  /**
   * Rendering engine. Defaults to an auto engine that uses RDKit.js (the same
   * high-fidelity depiction as the website) when its WASM assets are available
   * at `wasmPath`, and transparently falls back to the pure-JS OpenChemLib
   * engine otherwise (SSR/Node, no assets, or WebAssembly disabled).
   */
  engine?: RenderEngine;
  /**
   * Where `RDKit_minimal.js` / `.wasm` are served from, used by the default
   * auto engine. Default `'/rdkit'`. Ignored when `engine` is supplied.
   */
  wasmPath?: string;
  /** Cancels the (network) name resolution. */
  signal?: AbortSignal;
  /** Accessible title injected as the SVG <title>. */
  title?: string;
}

/** Result of {@link renderMoleculeSvg}. */
export interface RenderMoleculeResult {
  /** The rendered SVG markup (accessibility metadata injected). */
  svg: string;
  /** SMILES the structure was drawn from. */
  smiles: string;
  /** PubChem compound id, when resolved through PubChem. */
  cid?: number;
  /** The name that actually matched, when it differs from the query. */
  resolvedAs?: string;
  /** Which resolver (or 'direct') produced the structure. */
  source: StructureSource;
}

/** Skeletal drawing options for the headless API: no labels, element colors kept. */
const API_DEFAULTS: DrawOptions = {
  width: 320,
  height: 240,
  hideText: true,
  addStereoAnnotation: false,
};

const autoEngines = new Map<string, RenderEngine>();

function defaultEngine(wasmPath: string): RenderEngine {
  let engine = autoEngines.get(wasmPath);
  if (!engine) {
    engine = createAutoEngine(wasmPath);
    autoEngines.set(wasmPath, engine);
  }
  return engine;
}

/**
 * Resolves a molecule **name** (or a SMILES) to an accurate 2D **SVG** in one
 * call — the easy entry point for external sites and serverless functions.
 *
 * No React required. By default it resolves the name via PubChem and draws a
 * transparent, skeletal SVG with the pure-JS OpenChemLib engine (no WASM
 * assets to host).
 *
 * ```ts
 * const { svg } = await renderMoleculeSvg('aspirin', { width: 300 });
 * // or skip the network with a known structure:
 * const { svg } = await renderMoleculeSvg('', { smiles: 'CCO', strokeColour: '#0000ee' });
 * ```
 *
 * @throws {MolstructError} on resolution or rendering failure (typed `code`).
 */
export async function renderMoleculeSvg(
  query: string,
  options: RenderMoleculeOptions = {},
): Promise<RenderMoleculeResult> {
  let smiles = options.smiles?.trim();
  let cid: number | undefined;
  let resolvedAs: string | undefined;
  let source: StructureSource = 'direct';

  if (!smiles) {
    const name = query.trim();
    if (!name) {
      throw new MolstructError(
        'BAD_REQUEST',
        'Provide a molecule name as the first argument, or a `smiles` option.',
      );
    }
    const structure = await getResolver(options.resolver)(name, options.signal);
    smiles = structure.smiles;
    cid = structure.cid;
    resolvedAs = structure.resolvedAs;
    source = structure.source;
  }

  const engine = options.engine ?? defaultEngine(options.wasmPath ?? '/rdkit');
  try {
    await engine.ready();
  } catch (cause) {
    throw toMolstructError(cause, 'WASM_LOAD', 'Rendering engine failed to load.');
  }

  const draw: DrawOptions = { ...API_DEFAULTS, ...options };
  let svg = engine.renderToSvg(smiles, draw);
  svg = applySvgOverrides(svg, draw);
  const title = options.title ?? `2D structure of ${query || smiles}`;
  svg = decorateSvg(svg, title, `Rendered from SMILES: ${smiles}`);

  return { svg, smiles, cid, resolvedAs, source };
}
