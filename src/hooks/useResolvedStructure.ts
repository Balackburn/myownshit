import { useEffect, useMemo, useState } from 'react';
import { MolstructError, toMolstructError } from '../errors';
import {
  getCachedStructure,
  getResolver,
  setCachedStructure,
} from '../resolvers';
import type { ResolvedStructure, ResolverChoice } from '../types';
import { useDebounce } from './useDebounce';

export interface UseResolvedStructureArgs {
  /** Molecule name to resolve. Ignored when `smiles` is provided. */
  name?: string;
  /** Direct SMILES input; bypasses network resolution entirely. */
  smiles?: string;
  /** Resolver selection; defaults to PubChem with CACTUS fallback. */
  resolver?: ResolverChoice;
  /** Debounce on name changes, in ms. Default 400. */
  debounceMs?: number;
}

export interface UseResolvedStructureResult {
  structure: ResolvedStructure | null;
  /** True while a network resolution is in flight (or pending debounce). */
  loading: boolean;
  error: MolstructError | null;
}

function resolverId(choice: ResolverChoice | undefined): string {
  if (typeof choice === 'function') return 'custom';
  return choice ?? 'pubchem';
}

/**
 * Resolves a molecule name to a structure with debouncing, a shared cache,
 * and AbortController-based cancellation of superseded requests.
 */
export function useResolvedStructure(
  args: UseResolvedStructureArgs,
): UseResolvedStructureResult {
  const { name, smiles, resolver, debounceMs = 400 } = args;
  const trimmedName = name?.trim() ?? '';
  const debouncedName = useDebounce(trimmedName, debounceMs);
  const id = resolverId(resolver);

  const directStructure = useMemo<ResolvedStructure | null>(() => {
    const trimmedSmiles = smiles?.trim();
    if (!trimmedSmiles) return null;
    return { query: trimmedSmiles, smiles: trimmedSmiles, source: 'direct' };
  }, [smiles]);

  const [state, setState] = useState<UseResolvedStructureResult>({
    structure: null,
    loading: false,
    error: null,
  });

  useEffect(() => {
    if (directStructure) return; // SMILES bypass: no fetching.

    if (!debouncedName) {
      setState({ structure: null, loading: false, error: null });
      return;
    }

    const cached = getCachedStructure(id, debouncedName);
    if (cached) {
      setState({ structure: cached, loading: false, error: null });
      return;
    }

    const controller = new AbortController();
    setState((prev) => ({ ...prev, loading: true, error: null }));

    getResolver(resolver)(debouncedName, controller.signal)
      .then((structure) => {
        if (controller.signal.aborted) return;
        setCachedStructure(id, debouncedName, structure);
        setState({ structure, loading: false, error: null });
      })
      .catch((cause) => {
        if (controller.signal.aborted) return;
        const error = toMolstructError(cause, 'NETWORK', 'Name resolution failed.');
        if (error.code === 'ABORTED') return;
        setState({ structure: null, loading: false, error });
      });

    return () => controller.abort();
    // `resolver` participates via `id` for built-ins; custom fns are assumed stable.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [debouncedName, id, directStructure]);

  if (directStructure) {
    return { structure: directStructure, loading: false, error: null };
  }
  // While the debounce window is open for a new non-empty name, report loading
  // so consumers can show a spinner immediately.
  const debouncePending = trimmedName !== debouncedName && trimmedName !== '';
  return debouncePending ? { ...state, loading: true } : state;
}
