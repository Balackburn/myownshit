import {
  useEffect,
  useRef,
  useState,
  type CSSProperties,
  type ReactNode,
} from 'react';
import { renderMoleculeSvg } from '../api';
import { MolstructError, describeError, toMolstructError } from '../errors';
import type { DrawOptions, ResolverChoice } from '../types';

export interface MoleculeImageProps {
  /** Molecule name to resolve via PubChem (e.g. "aspirin", "THC"). */
  name?: string;
  /** SMILES string; bypasses name resolution and any network call. */
  smiles?: string;
  /** Canvas width in px. Default 320. */
  width?: number;
  /** Canvas height in px. Default 240. */
  height?: number;
  /** Drawing options; skeletal/transparent by default. */
  options?: DrawOptions;
  /** Name resolver: 'pubchem' (default), 'cactus', or a custom function. */
  resolver?: ResolverChoice;
  /**
   * Where RDKit's WASM assets are served from (for the highest-fidelity
   * output). Defaults to `'/rdkit'`; if they are not hosted, the component
   * transparently falls back to the pure-JS engine.
   */
  wasmPath?: string;
  /** Accessible label. Defaults to "2D structure of {name}". */
  alt?: string;
  /** Called when the structure resolves. */
  onResolved?: (info: { smiles: string; cid?: number; resolvedAs?: string }) => void;
  /** Called on resolution/rendering errors. */
  onError?: (error: MolstructError) => void;
  /** Custom loading node. */
  loading?: ReactNode;
  /** Custom error node (receives the error). */
  errorFallback?: (error: MolstructError) => ReactNode;
  className?: string;
  style?: CSSProperties;
}

/**
 * The simplest way to put a molecule on a page: give it a name, get an SVG.
 *
 * ```tsx
 * <MoleculeImage name="aspirin" />
 * <MoleculeImage smiles="CCO" options={{ strokeColour: '#0000ee' }} />
 * ```
 *
 * Zero setup — it resolves the name and renders client-side, using RDKit when
 * its assets are available and the pure-JS engine otherwise. No stylesheet
 * import required. For an interactive, ref-driven viewer use `MoleculeViewer`.
 */
export function MoleculeImage(props: MoleculeImageProps) {
  const {
    name,
    smiles,
    width = 320,
    height = 240,
    options,
    resolver,
    wasmPath,
    alt,
    onResolved,
    onError,
    loading,
    errorFallback,
    className,
    style,
  } = props;

  const [svg, setSvg] = useState<string | null>(null);
  const [error, setError] = useState<MolstructError | null>(null);
  const [busy, setBusy] = useState(true);

  // Keep callbacks current without re-running the effect for new closures.
  const onResolvedRef = useRef(onResolved);
  const onErrorRef = useRef(onError);
  onResolvedRef.current = onResolved;
  onErrorRef.current = onError;

  const optionsKey = JSON.stringify(options ?? {});

  useEffect(() => {
    let cancelled = false;
    const controller = new AbortController();
    setBusy(true);
    setError(null);

    renderMoleculeSvg(name ?? '', {
      smiles,
      width,
      height,
      resolver,
      wasmPath,
      signal: controller.signal,
      title: alt,
      ...(options ?? {}),
    })
      .then((result) => {
        if (cancelled) return;
        setSvg(result.svg);
        setBusy(false);
        onResolvedRef.current?.({
          smiles: result.smiles,
          cid: result.cid,
          resolvedAs: result.resolvedAs,
        });
      })
      .catch((cause) => {
        if (cancelled) return;
        const err = toMolstructError(cause, 'RENDER', 'Failed to render molecule.');
        if (err.code === 'ABORTED') return;
        setError(err);
        setBusy(false);
        onErrorRef.current?.(err);
      });

    return () => {
      cancelled = true;
      controller.abort();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [name, smiles, width, height, resolver, wasmPath, alt, optionsKey]);

  const frameStyle: CSSProperties = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    width,
    minHeight: height,
    ...style,
  };
  const label = alt ?? `2D structure of ${name?.trim() || smiles || 'a molecule'}`;

  if (error) {
    return (
      <div className={className} style={frameStyle} role="alert">
        {errorFallback ? errorFallback(error) : describeError(error)}
      </div>
    );
  }
  if (busy && !svg) {
    return (
      <div className={className} style={frameStyle} role="status" aria-busy="true">
        {loading ?? 'Loading…'}
      </div>
    );
  }
  return (
    <div
      className={className}
      style={frameStyle}
      role="img"
      aria-label={label}
      // SVG is produced locally from a SMILES string, not injected from a
      // remote source; metadata is escaped in decorateSvg.
      dangerouslySetInnerHTML={{ __html: svg ?? '' }}
    />
  );
}
