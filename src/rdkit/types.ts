/**
 * Minimal typings for the RDKit.js MinimalLib surface this library uses.
 * The MinimalLib is loaded as a global script (it is not an importable ES
 * module), so these types describe the runtime objects on `window`.
 */
export interface JSMol {
  is_valid(): boolean;
  get_svg(width?: number, height?: number): string;
  /** Options are passed as a JSON string; colors as [r,g,b] floats 0–1. */
  get_svg_with_highlights(details: string): string;
  /** Returns a JSON string like {"atoms":[...],"bonds":[...]} (first match). */
  get_substruct_match(query: JSMol): string;
  /** Returns a JSON string of an array of {atoms,bonds} (all matches). */
  get_substruct_matches(query: JSMol): string;
  /** Frees the underlying WASM memory. MUST be called when done. */
  delete(): void;
}

export interface RDKitModule {
  version(): string;
  /** Returns a mol (possibly invalid — check is_valid()) or null on hard failure. */
  get_mol(input: string, details?: string): JSMol | null;
  /** Builds a query mol from SMARTS/SMILES for substructure matching. */
  get_qmol(input: string): JSMol | null;
}

export interface InitRDKitOptions {
  locateFile?: (file: string) => string;
  /** Pre-fetched WASM bytes; skips Emscripten's own (streaming) fetch. */
  wasmBinary?: ArrayBuffer;
}

declare global {
  interface Window {
    initRDKitModule?: (options?: InitRDKitOptions) => Promise<RDKitModule>;
  }
}
