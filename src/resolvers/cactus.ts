import { MolstructError, toMolstructError } from '../errors';
import type { ResolvedStructure } from '../types';

const CACTUS_BASE = 'https://cactus.nci.nih.gov/chemical/structure';

/**
 * Resolves a name to SMILES via the NCI CACTUS Chemical Identifier Resolver.
 *
 * Secondary resolver only: CACTUS enforces ~1 req/s, its CORS support is not
 * guaranteed, and the service is intermittently unavailable — every failure
 * mode is mapped to a typed MolstructError so callers can fall through.
 */
export async function resolveWithCactus(
  name: string,
  signal?: AbortSignal,
): Promise<ResolvedStructure> {
  const query = name.trim();
  if (!query) {
    throw new MolstructError('BAD_REQUEST', 'Molecule name is empty.');
  }
  const url = `${CACTUS_BASE}/${encodeURIComponent(query)}/smiles`;

  let response: Response;
  try {
    response = await fetch(url, { signal });
  } catch (cause) {
    throw toMolstructError(
      cause,
      'NETWORK',
      'Could not reach CACTUS (network failure or CORS rejection).',
    );
  }

  if (response.status === 404) {
    throw new MolstructError('NOT_FOUND', `CACTUS found no structure for "${query}".`);
  }
  if (!response.ok) {
    throw new MolstructError('NETWORK', `CACTUS request failed with HTTP ${response.status}.`);
  }

  const text = (await response.text()).trim();
  // CACTUS may return multiple SMILES lines; take the first non-empty one.
  const smiles = text.split('\n').map((line) => line.trim()).find(Boolean);
  if (!smiles || /<html/i.test(smiles)) {
    throw new MolstructError('NOT_FOUND', `CACTUS returned no usable SMILES for "${query}".`);
  }
  return { query, smiles, source: 'cactus' };
}
