import { useEffect, useState } from 'react';
import { MolstructError, toMolstructError } from '../errors';
import { DEFAULT_WASM_PATH, loadRDKit } from '../rdkit/loader';
import type { RDKitModule } from '../rdkit/types';

export interface UseRdkitResult {
  /** The RDKit module once loaded, else null. */
  rdkit: RDKitModule | null;
  /** True while the WASM module is loading. */
  loading: boolean;
  /** Load failure, if any. */
  error: MolstructError | null;
}

/**
 * Loads the RDKit.js WASM module (singleton per wasmPath) and exposes
 * loading/error/ready state. Safe across many simultaneous consumers —
 * the underlying loader caches the module promise.
 */
export function useRdkit(wasmPath: string = DEFAULT_WASM_PATH): UseRdkitResult {
  const [rdkit, setRdkit] = useState<RDKitModule | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<MolstructError | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    loadRDKit(wasmPath)
      .then((module) => {
        if (cancelled) return;
        setRdkit(module);
        setLoading(false);
      })
      .catch((cause) => {
        if (cancelled) return;
        setError(toMolstructError(cause, 'WASM_LOAD', 'Failed to load RDKit.'));
        setRdkit(null);
        setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [wasmPath]);

  return { rdkit, loading, error };
}
