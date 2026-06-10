import { MolstructError } from '../errors';
import type { DrawOptions, RenderEngine } from '../types';
import { drawMoleculeToSvg } from './draw';
import { DEFAULT_WASM_PATH, loadRDKit } from './loader';
import type { RDKitModule } from './types';

const engineCache = new Map<string, RenderEngine>();

/**
 * Creates (or returns the cached) RDKit-backed RenderEngine for a given asset
 * path. ready() loads the WASM module once; renderToSvg is synchronous after.
 */
export function createRDKitEngine(
  wasmPath: string = DEFAULT_WASM_PATH,
): RenderEngine {
  const cached = engineCache.get(wasmPath);
  if (cached) return cached;

  let module: RDKitModule | null = null;
  const engine: RenderEngine = {
    id: 'rdkit',
    async ready(): Promise<void> {
      if (!module) {
        module = await loadRDKit(wasmPath);
      }
    },
    renderToSvg(smiles: string, options: DrawOptions): string {
      if (!module) {
        throw new MolstructError(
          'WASM_LOAD',
          'RDKit engine used before ready() resolved.',
        );
      }
      return drawMoleculeToSvg(module, smiles, options);
    },
  };
  engineCache.set(wasmPath, engine);
  return engine;
}
