import { MolstructError, toMolstructError } from '../errors';
import type { ResolvedStructure } from '../types';

const PUBCHEM_BASE = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug';

/**
 * Client-side politeness guard for PubChem's published limits
 * (≤5 requests/second, ≤400/minute): serializes requests with a minimum
 * spacing of 220ms between dispatches.
 */
const MIN_REQUEST_SPACING_MS = 220;
let lastDispatch = 0;
let gate: Promise<void> = Promise.resolve();

function rateGate(): Promise<void> {
  const next = gate.then(async () => {
    const wait = lastDispatch + MIN_REQUEST_SPACING_MS - Date.now();
    if (wait > 0) await sleep(wait);
    lastDispatch = Date.now();
  });
  // Keep the chain alive even if a caller's fetch later rejects.
  gate = next.catch(() => undefined);
  return next;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

interface PubChemPropertyRow {
  CID?: number;
  /** 2025 naming: isomeric SMILES (includes stereochemistry). */
  SMILES?: string;
  /** 2025 naming: connectivity SMILES (no stereochemistry). */
  ConnectivitySMILES?: string;
}

interface PubChemPropertyResponse {
  PropertyTable?: { Properties?: PubChemPropertyRow[] };
  Fault?: { Code?: string; Message?: string; Details?: string[] };
}

/**
 * Resolves a molecule name to SMILES via PubChem PUG REST.
 *
 * Uses the 2025 property names: `SMILES` (isomeric, preferred for depiction)
 * and `ConnectivitySMILES` (stereo-free fallback). Retries 503/ServerBusy with
 * exponential backoff; maps 404 to MolstructError('NOT_FOUND').
 */
export async function resolveWithPubChem(
  name: string,
  signal?: AbortSignal,
): Promise<ResolvedStructure> {
  const query = name.trim();
  if (!query) {
    throw new MolstructError('BAD_REQUEST', 'Molecule name is empty.');
  }
  // Names containing reserved URL characters go through the query-param form.
  const url = /[/\\?#%]/.test(query)
    ? `${PUBCHEM_BASE}/compound/name/property/SMILES,ConnectivitySMILES/JSON?name=${encodeURIComponent(query)}`
    : `${PUBCHEM_BASE}/compound/name/${encodeURIComponent(query)}/property/SMILES,ConnectivitySMILES/JSON`;

  const response = await fetchWithBackoff(url, signal);
  let body: PubChemPropertyResponse;
  try {
    body = (await response.json()) as PubChemPropertyResponse;
  } catch (cause) {
    throw new MolstructError('NETWORK', 'PubChem returned an unreadable response.', cause);
  }

  const row = body.PropertyTable?.Properties?.[0];
  const smiles = row?.SMILES || row?.ConnectivitySMILES;
  if (!row || !smiles) {
    throw new MolstructError('NOT_FOUND', `PubChem returned no structure for "${query}".`);
  }
  return {
    query,
    smiles,
    connectivitySmiles: row.ConnectivitySMILES,
    cid: row.CID,
    source: 'pubchem',
  };
}

async function fetchWithBackoff(url: string, signal?: AbortSignal): Promise<Response> {
  const maxAttempts = 3;
  let lastBusy: MolstructError | null = null;

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    if (signal?.aborted) {
      throw new MolstructError('ABORTED', 'The request was cancelled.');
    }
    if (attempt > 0) {
      await sleep(1000 * 2 ** (attempt - 1));
    }
    await rateGate();

    let response: Response;
    try {
      response = await fetch(url, { signal, headers: { Accept: 'application/json' } });
    } catch (cause) {
      throw toMolstructError(cause, 'NETWORK', 'Could not reach PubChem.');
    }

    if (response.ok) return response;

    const fault = await readFaultCode(response);
    if (response.status === 404 || fault === 'PUGREST.NotFound') {
      throw new MolstructError('NOT_FOUND', 'PubChem found no compound with that name.');
    }
    if (response.status === 400 || fault === 'PUGREST.BadRequest') {
      throw new MolstructError('BAD_REQUEST', 'PubChem rejected the request as malformed.');
    }
    if (response.status === 503 || fault === 'PUGREST.ServerBusy') {
      lastBusy = new MolstructError(
        'SERVER_BUSY',
        'PubChem is throttling requests (HTTP 503).',
      );
      continue; // back off and retry
    }
    throw new MolstructError(
      'NETWORK',
      `PubChem request failed with HTTP ${response.status}.`,
    );
  }
  throw lastBusy ?? new MolstructError('NETWORK', 'PubChem request failed.');
}

async function readFaultCode(response: Response): Promise<string | undefined> {
  try {
    const body = (await response.clone().json()) as PubChemPropertyResponse;
    return body.Fault?.Code;
  } catch {
    return undefined;
  }
}
