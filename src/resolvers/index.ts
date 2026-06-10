import { isMolstructError } from '../errors';
import type { ResolvedStructure, ResolverChoice, ResolverFn } from '../types';
import { resolveWithCactus } from './cactus';
import { resolveWithPubChem } from './pubchem';

export { resolveWithCactus } from './cactus';
export { resolveWithPubChem } from './pubchem';

/**
 * Default resolution strategy: PubChem first; if it fails for any reason
 * other than cancellation, quietly try CACTUS and — if that also fails —
 * rethrow the original (more informative) PubChem error.
 */
export const resolveWithPubChemThenCactus: ResolverFn = async (name, signal) => {
  try {
    return await resolveWithPubChem(name, signal);
  } catch (primaryError) {
    if (isMolstructError(primaryError) && primaryError.code === 'ABORTED') {
      throw primaryError;
    }
    try {
      return await resolveWithCactus(name, signal);
    } catch (fallbackError) {
      if (isMolstructError(fallbackError) && fallbackError.code === 'ABORTED') {
        throw fallbackError;
      }
      throw primaryError;
    }
  }
};

/** Maps a ResolverChoice ('pubchem' | 'cactus' | fn) to a concrete function. */
export function getResolver(choice: ResolverChoice | undefined): ResolverFn {
  if (typeof choice === 'function') return choice;
  if (choice === 'cactus') return resolveWithCactus;
  return resolveWithPubChemThenCactus;
}

/**
 * Shared in-memory cache of resolved structures, keyed by resolver id +
 * normalized name. Avoids re-hitting PubChem for repeated queries.
 */
const structureCache = new Map<string, ResolvedStructure>();
const MAX_CACHE_ENTRIES = 500;

export function normalizeName(name: string): string {
  return name.trim().toLowerCase().replace(/\s+/g, ' ');
}

export function getCachedStructure(
  resolverId: string,
  name: string,
): ResolvedStructure | undefined {
  return structureCache.get(`${resolverId}::${normalizeName(name)}`);
}

export function setCachedStructure(
  resolverId: string,
  name: string,
  structure: ResolvedStructure,
): void {
  if (structureCache.size >= MAX_CACHE_ENTRIES) {
    // Drop the oldest entry (Map preserves insertion order).
    const oldest = structureCache.keys().next().value;
    if (oldest !== undefined) structureCache.delete(oldest);
  }
  structureCache.set(`${resolverId}::${normalizeName(name)}`, structure);
}

/** Clears the shared resolution cache (mainly useful in tests). */
export function clearStructureCache(): void {
  structureCache.clear();
}
