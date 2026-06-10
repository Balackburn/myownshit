/** Machine-readable error categories surfaced by react-molstruct. */
export type MolstructErrorCode =
  | 'NOT_FOUND'
  | 'BAD_REQUEST'
  | 'SERVER_BUSY'
  | 'NETWORK'
  | 'ABORTED'
  | 'INVALID_SMILES'
  | 'INVALID_SMARTS'
  | 'WASM_LOAD'
  | 'RENDER';

/** Typed error with a stable `code` for branching UI states. */
export class MolstructError extends Error {
  readonly code: MolstructErrorCode;
  readonly cause?: unknown;

  constructor(code: MolstructErrorCode, message: string, cause?: unknown) {
    super(message);
    this.name = 'MolstructError';
    this.code = code;
    this.cause = cause;
  }
}

/** Narrowing helper. */
export function isMolstructError(value: unknown): value is MolstructError {
  return value instanceof MolstructError;
}

/** Wraps unknown thrown values into a MolstructError without double-wrapping. */
export function toMolstructError(
  value: unknown,
  fallbackCode: MolstructErrorCode,
  fallbackMessage: string,
): MolstructError {
  if (isMolstructError(value)) return value;
  if (value instanceof DOMException && value.name === 'AbortError') {
    return new MolstructError('ABORTED', 'The request was cancelled.', value);
  }
  return new MolstructError(fallbackCode, fallbackMessage, value);
}

/** A short human-readable message for each error code, suitable for UI display. */
export function describeError(error: MolstructError): string {
  switch (error.code) {
    case 'NOT_FOUND':
      return 'No molecule was found with that name. Check the spelling or try a synonym.';
    case 'BAD_REQUEST':
      return 'The request was malformed. Try a simpler name or a SMILES string.';
    case 'SERVER_BUSY':
      return 'PubChem is busy right now. Please wait a moment and try again.';
    case 'NETWORK':
      return 'Could not reach the structure service. Check your connection.';
    case 'ABORTED':
      return 'The lookup was cancelled.';
    case 'INVALID_SMILES':
      return 'The structure string is not valid SMILES.';
    case 'INVALID_SMARTS':
      return 'The highlight pattern is not valid SMARTS; rendering without it.';
    case 'WASM_LOAD':
      return 'The chemistry rendering engine failed to load.';
    case 'RENDER':
      return 'The molecule could not be drawn.';
  }
}
