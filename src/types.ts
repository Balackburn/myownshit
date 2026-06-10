import type { CSSProperties, ReactNode } from 'react';
import type { MolstructError } from './errors';

/** An RGB(A) color as floats in the 0–1 range, the format RDKit.js expects. */
export type RGBColor =
  | [number, number, number]
  | [number, number, number, number];

/** A color as a CSS hex string ("#rrggbb" / "#rrggbbaa" / "#rgb") or an RDKit float triple. */
export type ColorInput = string | RGBColor;

/** Built-in atom coloring schemes. */
export type ColorScheme = 'default' | 'monochrome' | 'custom';

/** A substructure highlight request, expressed as a SMARTS (or SMILES) query. */
export interface HighlightSpec {
  /** SMARTS or SMILES pattern to match against the molecule. */
  smarts: string;
  /** Highlight color. Defaults to a soft red. */
  color?: ColorInput;
}

/**
 * Drawing customization. Friendly, typed surface over RDKit.js
 * `get_svg_with_highlights` options. Colors may be hex strings; they are
 * converted to RDKit's `[r, g, b]` 0–1 floats internally.
 */
export interface DrawOptions {
  /** Canvas width in px. Overrides the `width` prop of MoleculeViewer. */
  width?: number;
  /** Canvas height in px. Overrides the `height` prop of MoleculeViewer. */
  height?: number;
  /** Bond line thickness (RDKit `bondLineWidth`). */
  bondLineWidth?: number;
  /** Background color (RDKit `backgroundColour`). */
  backgroundColour?: ColorInput;
  /** Highlight color used when `highlight` matches (RDKit `highlightColour`). */
  highlightColour?: ColorInput;
  /** Default color of atom symbols (RDKit `symbolColour`). */
  symbolColour?: ColorInput;
  /** Caption rendered under the molecule (RDKit `legend`). */
  legend?: string;
  /** Legend font size in px (RDKit `legendFontSize`). */
  legendFontSize?: number;
  /** Fraction of canvas used as whitespace around the drawing (RDKit `padding`). */
  padding?: number;
  /** Rotation of the depiction in degrees (RDKit `rotate`). */
  rotate?: number;
  /** Hide all atom labels (RDKit `noAtomLabels`). */
  noAtomLabels?: boolean;
  /** Annotate stereocenters/bonds with R/S and E/Z (RDKit `addStereoAnnotation`). */
  addStereoAnnotation?: boolean;
  /** Draw atom indices (RDKit `addAtomIndices`). */
  addAtomIndices?: boolean;
  /** Draw bond indices (RDKit `addBondIndices`). */
  addBondIndices?: boolean;
  /** Draw terminal methyls explicitly as CH3 (RDKit `explicitMethyl`). */
  explicitMethyl?: boolean;
  /**
   * Atom palette: 'default' (RDKit CPK-like), 'monochrome' (single ink color),
   * or 'custom' (use `customAtomPalette`).
   */
  colorScheme?: ColorScheme;
  /**
   * Custom palette keyed by atomic number (e.g. { 6: '#1f2937', 8: '#dc2626' }).
   * Best-effort: forwarded as RDKit `atomColourPalette`.
   */
  customAtomPalette?: Record<number, ColorInput>;
  /** Substructure highlight by SMARTS. */
  highlight?: HighlightSpec;
  /**
   * Hand-drawn "comic" rendering. Best-effort: the RDKit MinimalLib may
   * ignore this key; the drawing still renders normally if so.
   */
  comicMode?: boolean;
  /**
   * Escape hatch: raw key/values merged verbatim into the RDKit options JSON
   * (after all mapped options). Color values here must already be 0–1 floats.
   */
  extraRDKitOptions?: Record<string, unknown>;
}

/** Where a structure came from. */
export type StructureSource = 'pubchem' | 'cactus' | 'direct' | 'custom';

/** Result of resolving a molecule name (or passing SMILES directly). */
export interface ResolvedStructure {
  /** The query that produced this structure (name or raw SMILES). */
  query: string;
  /** Isomeric SMILES preferred; connectivity SMILES as fallback. */
  smiles: string;
  /** PubChem compound id, when resolved through PubChem. */
  cid?: number;
  /** Connectivity (stereo-free) SMILES when available. */
  connectivitySmiles?: string;
  /** Which resolver produced the structure. */
  source: StructureSource;
}

/** A pluggable name→structure resolver. */
export type ResolverFn = (
  name: string,
  signal?: AbortSignal,
) => Promise<ResolvedStructure>;

/** Resolver selection: a built-in id or a custom function. */
export type ResolverChoice = 'pubchem' | 'cactus' | ResolverFn;

/** Imperative API exposed by MoleculeViewer via ref. */
export interface MoleculeViewerHandle {
  /** The current SVG markup (with accessibility metadata), or null if not rendered yet. */
  getSvgString(): string | null;
  /** Triggers a browser download of the current SVG. */
  downloadSvg(filename?: string): void;
  /** Copies the current SVG markup to the clipboard. Resolves true on success. */
  copySvgToClipboard(): Promise<boolean>;
}

export interface MoleculeViewerProps {
  /** Molecule name to resolve via PubChem (e.g. "aspirin"). */
  name?: string;
  /** SMILES string; when given, name resolution is bypassed. */
  smiles?: string;
  /** Canvas width in px (overridden by options.width). Default 320. */
  width?: number;
  /** Canvas height in px (overridden by options.height). Default 260. */
  height?: number;
  /** Drawing customization, deep-merged over sensible defaults. */
  options?: DrawOptions;
  /**
   * Base path from which RDKit_minimal.js / RDKit_minimal.wasm are served.
   * Default '/rdkit'.
   */
  wasmPath?: string;
  /** Name resolver: 'pubchem' (default, with CACTUS fallback), 'cactus', or a custom fn. */
  resolver?: ResolverChoice;
  /**
   * Rendering engine override. Defaults to the built-in RDKit.js engine for
   * `wasmPath`. Supply an OpenChemLib-backed implementation to swap engines.
   */
  engine?: RenderEngine;
  /** Debounce applied to name changes before fetching, in ms. Default 400. */
  debounceMs?: number;
  /** Called when a name resolves to a structure (or SMILES is accepted directly). */
  onResolved?: (structure: ResolvedStructure) => void;
  /** Called on resolution, WASM, or rendering errors (including non-fatal SMARTS errors). */
  onError?: (error: MolstructError) => void;
  /** Called with the final SVG markup whenever it changes. */
  onSvg?: (svg: string) => void;
  /** Accessible label; defaults to "2D chemical structure of {name}". */
  ariaLabel?: string;
  /** Custom loading UI. */
  renderLoading?: () => ReactNode;
  /** Custom error UI. */
  renderError?: (error: MolstructError) => ReactNode;
  className?: string;
  style?: CSSProperties;
}

/**
 * Pluggable rendering engine interface. RDKit.js is the built-in default;
 * an OpenChemLib-backed engine can be supplied by implementing this.
 */
export interface RenderEngine {
  /** Stable identifier, e.g. 'rdkit'. */
  readonly id: string;
  /** Resolves when the engine is ready to render synchronously. */
  ready(): Promise<void>;
  /** Renders a SMILES string to SVG markup. Throws MolstructError on failure. */
  renderToSvg(smiles: string, options: DrawOptions): string;
}
