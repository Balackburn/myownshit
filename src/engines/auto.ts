import type { DrawOptions, RenderEngine } from '../types';
import { createOpenChemLibEngine } from './openchemlib';
import { createRDKitEngine } from '../rdkit/engine';

/**
 * An engine that prefers RDKit.js (the high-fidelity depiction used by
 * `<MoleculeViewer>` and the website) and transparently falls back to the
 * pure-JS OpenChemLib engine when WebAssembly or the RDKit assets are
 * unavailable (SSR/Node, Safari Lockdown Mode, assets not hosted).
 *
 * `wasmPath` is where `RDKit_minimal.js` / `.wasm` are served from. The first
 * `ready()` decides which engine to use; the choice is then cached.
 */
export function createAutoEngine(wasmPath = '/rdkit'): RenderEngine {
  let inner: RenderEngine | null = null;

  async function resolve(): Promise<RenderEngine> {
    if (inner) return inner;
    const rdkit = createRDKitEngine(wasmPath);
    try {
      await rdkit.ready();
      inner = rdkit;
    } catch {
      const ocl = createOpenChemLibEngine();
      await ocl.ready();
      inner = ocl;
    }
    return inner;
  }

  return {
    get id() {
      return inner?.id ?? 'auto';
    },
    async ready(): Promise<void> {
      await resolve();
    },
    renderToSvg(smiles: string, options: DrawOptions): string {
      if (!inner) {
        // ready() resolves the engine; callers always await it first.
        throw new Error('Auto engine used before ready() resolved.');
      }
      return inner.renderToSvg(smiles, options);
    },
  };
}
