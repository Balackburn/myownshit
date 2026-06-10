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

/**
 * True when the current environment can compile WebAssembly. False in
 * Safari Lockdown Mode and other WASM-disabled contexts — use the
 * OpenChemLib engine there instead.
 */
export function isWebAssemblyAvailable(): boolean {
  return (
    typeof WebAssembly === 'object' &&
    WebAssembly !== null &&
    typeof WebAssembly.instantiate === 'function'
  );
}

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
  if (!isWebAssemblyAvailable()) {
    throw new MolstructError(
      'WASM_LOAD',
      'WebAssembly is disabled in this browser (Safari Lockdown Mode and some ' +
        'privacy modes turn it off), so the RDKit engine cannot run. ' +
        'Use the pure-JS OpenChemLib engine or a browser with WebAssembly enabled.',
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
  // Fetch the WASM ourselves and pass the bytes to Emscripten (wasmBinary).
  // This sidesteps instantiateStreaming/MIME issues on static hosts and lets
  // us report the exact HTTP failure instead of an opaque init error.
  const wasmBinary = await fetchWasmBinary(`${base}/RDKit_minimal.wasm`);
  try {
    return await init({
      locateFile: (file: string) => `${base}/${file}`,
      wasmBinary,
    });
  } catch (cause) {
    const detail = cause instanceof Error ? cause.message : String(cause);
    throw new MolstructError(
      'WASM_LOAD',
      `RDKit WASM instantiation failed (${detail}).`,
      cause,
    );
  }
}

async function fetchWasmBinary(url: string): Promise<ArrayBuffer> {
  let response: Response;
  try {
    response = await fetch(url, { credentials: 'same-origin' });
  } catch (cause) {
    const detail = cause instanceof Error ? cause.message : String(cause);
    throw new MolstructError(
      'WASM_LOAD',
      `Could not fetch ${url} (${detail}). Check the network and wasmPath.`,
      cause,
    );
  }
  if (!response.ok) {
    throw new MolstructError(
      'WASM_LOAD',
      `HTTP ${response.status} fetching ${url}. ` +
        'Copy RDKit_minimal.wasm next to RDKit_minimal.js in your served public directory.',
    );
  }
  const buffer = await response.arrayBuffer();
  const magic = new Uint8Array(buffer.slice(0, 4));
  const isWasm =
    magic[0] === 0x00 && magic[1] === 0x61 && magic[2] === 0x73 && magic[3] === 0x6d;
  if (!isWasm) {
    const contentType = response.headers.get('content-type') ?? 'unknown';
    throw new MolstructError(
      'WASM_LOAD',
      `The file at ${url} is not a WebAssembly binary ` +
        `(content-type ${contentType}, ${buffer.byteLength} bytes) — ` +
        'the server likely returned an error or redirect page.',
    );
  }
  return buffer;
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
