import { MolstructError, toMolstructError } from '../errors';
import type { ResolvedStructure, ResolverChoice, ResolverFn } from '../types';
import { fetchNameSuggestions } from './autocomplete';
import { expandQueryCandidates } from './candidates';
import { resolveWithCactus } from './cactus';
import { resolveWithPubChem } from './pubchem';

export { resolveWithCactus } from './cactus';
export { resolveWithPubChem } from './pubchem';
export { fetchNameSuggestions } from './autocomplete';
export { expandQueryCandidates } from './candidates';

function finalize(
  structure: ResolvedStructure,
  originalQuery: string,
  matchedName: string,
): ResolvedStructure {
  const differs =
    matchedName.trim().toLowerCase() !== originalQuery.trim().toLowerCase();
  return {
    ...structure,
    query: originalQuery,
    resolvedAs: differs ? matchedName : undefined,
  };
}

/**
 * Default resolution strategy, built for how people actually type names:
 *
 * 1. Expand the query into candidates (parenthetical parts, Greek-letter
 *    spellings, dash normalization) and try each against PubChem.
 * 2. If everything was a clean miss, ask PubChem's autocomplete for close
 *    dictionary terms (typo/abbreviation recovery) and resolve the best.
 * 3. Finally fall back to NCI CACTUS.
 *
 * When the matched name differs from the query, the result carries
 * `resolvedAs` so UIs can show what was actually found.
 */
export const resolveWithPubChemThenCactus: ResolverFn = async (name, signal) => {
  const candidates = expandQueryCandidates(name);
  let notFound: MolstructError | null = null;
  let hardError: MolstructError | null = null;

  for (const candidate of candidates) {
    try {
      return finalize(await resolveWithPubChem(candidate, signal), name, candidate);
    } catch (cause) {
      const error = toMolstructError(cause, 'NETWORK', 'Name resolution failed.');
      if (error.code === 'ABORTED') throw error;
      if (error.code === 'NOT_FOUND') {
        notFound = error;
      } else {
        // Network/server trouble: stop hammering PubChem with more variants.
        hardError = error;
        break;
      }
    }
  }

  if (!hardError) {
    try {
      const suggestions = await fetchNameSuggestions(candidates[0], 5, signal);
      const tried = new Set(candidates.map((c) => c.toLowerCase()));
      // Only follow suggestions plausibly related to the query, so a short or
      // ambiguous input never silently resolves to an unrelated popular hit.
      const plausible = suggestions.filter((s) => isRelatedSuggestion(name, s));
      for (const suggestion of plausible.slice(0, 3)) {
        if (tried.has(suggestion.toLowerCase())) continue;
        try {
          return finalize(
            await resolveWithPubChem(suggestion, signal),
            name,
            suggestion,
          );
        } catch (cause) {
          const error = toMolstructError(cause, 'NETWORK', 'Name resolution failed.');
          if (error.code === 'ABORTED') throw error;
          if (error.code !== 'NOT_FOUND') break;
        }
      }
    } catch (cause) {
      const error = toMolstructError(cause, 'NETWORK', 'Autocomplete failed.');
      if (error.code === 'ABORTED') throw error;
      // Autocomplete being down should not mask the primary outcome.
    }
  }

  for (const candidate of candidates.slice(0, 2)) {
    try {
      return finalize(await resolveWithCactus(candidate, signal), name, candidate);
    } catch (cause) {
      const error = toMolstructError(cause, 'NETWORK', 'CACTUS failed.');
      if (error.code === 'ABORTED') throw error;
    }
  }

  throw (
    hardError ??
    notFound ??
    new MolstructError('NOT_FOUND', `No structure found for "${name}".`)
  );
};

/**
 * Heuristic guard against false-positive name recovery: an autocomplete
 * suggestion is accepted only when it is recognizably the same query —
 * one contains the other, or they share a strong leading prefix. This keeps
 * genuine recoveries (abbreviations, light typos) while rejecting unrelated
 * popular compounds that autocomplete may return for a vague input.
 */
export function isRelatedSuggestion(query: string, suggestion: string): boolean {
  const q = query.trim().toLowerCase().replace(/\s+/g, '');
  const s = suggestion.trim().toLowerCase().replace(/\s+/g, '');
  if (!q || !s) return false;
  if (s.includes(q) || q.includes(s)) return true;
  // Shared leading prefix of at least 4 chars (or the whole short query).
  const minLen = Math.min(q.length, s.length);
  let common = 0;
  while (common < minLen && q[common] === s[common]) common += 1;
  return common >= Math.min(4, q.length);
}

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
