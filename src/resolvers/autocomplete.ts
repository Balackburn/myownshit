import { toMolstructError } from '../errors';
import { pubchemRateGate } from './pubchem';

const AUTOCOMPLETE_BASE =
  'https://pubchem.ncbi.nlm.nih.gov/rest/autocomplete/compound';

interface AutocompleteResponse {
  dictionary_terms?: { compound?: unknown[] };
  total?: number;
}

/**
 * Fetches compound-name suggestions from PubChem's autocomplete API — the
 * same service that powers PubChem's own search box. Useful both for live
 * typeahead UIs and for recovering from misspelled or abbreviated names.
 *
 * Returns an empty array for short queries or when nothing matches; throws
 * MolstructError only on network-level failures.
 */
export async function fetchNameSuggestions(
  query: string,
  limit = 8,
  signal?: AbortSignal,
): Promise<string[]> {
  const q = query.trim();
  if (q.length < 2) return [];
  await pubchemRateGate();

  let response: Response;
  try {
    response = await fetch(
      `${AUTOCOMPLETE_BASE}/${encodeURIComponent(q)}/json?limit=${limit}`,
      { signal, headers: { Accept: 'application/json' } },
    );
  } catch (cause) {
    throw toMolstructError(cause, 'NETWORK', 'Could not reach PubChem autocomplete.');
  }
  if (!response.ok) return [];

  let body: AutocompleteResponse;
  try {
    body = (await response.json()) as AutocompleteResponse;
  } catch {
    return [];
  }
  const terms = body.dictionary_terms?.compound;
  if (!Array.isArray(terms)) return [];
  return terms.filter((term): term is string => typeof term === 'string');
}
