import { MolstructError } from '../errors';
import type { RDKitModule } from './types';

/**
 * Singleton loader for the RDKit.js MinimalLib.
 *
 * The MinimalLib is not consumable as an ES module by most bundlers, so we
 * inject `<script src="{wasmPath}/RDKit_minimal.js">` and then call the global
 * `window.initRDKitModule()`, pointing `locateFile` at the co-located .wasm.
 * The resulting module promise is cached per path; a failed load is evicted
 * so a later attempt can retry.
 */
const modulePromises = new Map<string, Promise<RDKitModule>>();

export const DEFAULT_WASM_PATH = '/rdkit';

export function loadRDKit(wasmPath: string = DEFAULT_WASM_PATH): Promise<RDKitModule> {
  const base = normalizeBase(wasmPath);
  let promise = modulePromises.get(base);
  if (!promise) {
    promise = initialize(base);
    promise.catch(() => {
      // Allow retrying after a transient failure (e.g. assets not yet deployed).
      if (modulePromises.get(base) === promise) modulePromises.delete(base);
    });
    modulePromises.set(base, promise);
  }
  return promise;
}

function normalizeBase(path: string): string {
  const trimmed = path.replace(/\/+$/, '');
  return trimmed === '' ? '.' : trimmed;
}

async function initialize(base: string): Promise<RDKitModule> {
  if (typeof window === 'undefined' || typeof document === 'undefined') {
    throw new MolstructError(
      'WASM_LOAD',
      'RDKit.js requires a browser environment; it cannot load during SSR.',
    );
  }
  if (typeof window.initRDKitModule !== 'function') {
    try {
      await injectScript(`${base}/RDKit_minimal.js`);
    } catch {
      // Transient failure (e.g. CDN edge not yet propagated): retry once
      // after a pause, cache-busting so a poisoned negative cache is skipped.
      await new Promise((resolve) => setTimeout(resolve, 1500));
      await injectScript(`${base}/RDKit_minimal.js?retry=1`);
    }
  }
  const init = window.initRDKitModule;
  if (typeof init !== 'function') {
    throw new MolstructError(
      'WASM_LOAD',
      `RDKit_minimal.js loaded from "${base}" but did not define initRDKitModule. ` +
        'Verify the copied asset is the RDKit.js MinimalLib build.',
    );
  }
  try {
    return await init({ locateFile: (file: string) => `${base}/${file}` });
  } catch (cause) {
    throw new MolstructError(
      'WASM_LOAD',
      `Failed to initialize the RDKit WASM module from "${base}". ` +
        'Ensure RDKit_minimal.wasm sits next to RDKit_minimal.js.',
      cause,
    );
  }
}

function injectScript(src: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const existing = document.querySelector<HTMLScriptElement>(
      `script[data-molstruct-rdkit][src="${src}"]`,
    );
    if (existing) {
      if (existing.dataset.molstructLoaded === 'true') {
        resolve();
        return;
      }
      existing.addEventListener('load', () => resolve(), { once: true });
      existing.addEventListener(
        'error',
        () => reject(scriptError(src)),
        { once: true },
      );
      return;
    }
    const script = document.createElement('script');
    script.src = src;
    script.async = true;
    script.dataset.molstructRdkit = 'true';
    script.addEventListener(
      'load',
      () => {
        script.dataset.molstructLoaded = 'true';
        resolve();
      },
      { once: true },
    );
    script.addEventListener(
      'error',
      () => {
        script.remove();
        reject(scriptError(src));
      },
      { once: true },
    );
    document.head.appendChild(script);
  });
}

function scriptError(src: string): MolstructError {
  return new MolstructError(
    'WASM_LOAD',
    `Could not load "${src}". Copy RDKit_minimal.js and RDKit_minimal.wasm ` +
      'from @rdkit/rdkit/dist into your served public directory (default /rdkit/).',
  );
}
