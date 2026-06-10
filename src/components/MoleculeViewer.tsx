import {
  forwardRef,
  useEffect,
  useImperativeHandle,
  useMemo,
  useRef,
  useState,
  type MutableRefObject,
} from 'react';
import { MolstructError, describeError, toMolstructError } from '../errors';
import { useResolvedStructure } from '../hooks/useResolvedStructure';
import { createRDKitEngine } from '../rdkit/engine';
import { DEFAULT_WASM_PATH } from '../rdkit/loader';
import type {
  DrawOptions,
  MoleculeViewerHandle,
  MoleculeViewerProps,
  RenderEngine,
} from '../types';
import {
  copyTextToClipboard,
  decorateSvg,
  downloadSvgFile,
} from '../utils/svg';
import '../styles.css';

interface DrawOutcome {
  svg: string | null;
  /** Non-fatal problem (e.g. invalid highlight SMARTS) — molecule still drawn. */
  warning: MolstructError | null;
  error: MolstructError | null;
}

function useEngineReady(engine: RenderEngine): {
  ready: boolean;
  error: MolstructError | null;
} {
  const [state, setState] = useState<{ ready: boolean; error: MolstructError | null }>({
    ready: false,
    error: null,
  });

  useEffect(() => {
    let cancelled = false;
    setState({ ready: false, error: null });
    engine
      .ready()
      .then(() => {
        if (!cancelled) setState({ ready: true, error: null });
      })
      .catch((cause) => {
        if (!cancelled) {
          setState({
            ready: false,
            error: toMolstructError(cause, 'WASM_LOAD', 'Rendering engine failed to load.'),
          });
        }
      });
    return () => {
      cancelled = true;
    };
  }, [engine]);

  return state;
}

/** Keeps the latest value of a callback without retriggering effects. */
function useLatest<T>(value: T): MutableRefObject<T> {
  const ref = useRef(value);
  ref.current = value;
  return ref;
}

/**
 * Renders a 2D structure SVG for a molecule name (resolved via PubChem) or a
 * SMILES string (rendered directly), entirely in the browser via RDKit WASM.
 */
export const MoleculeViewer = forwardRef<MoleculeViewerHandle, MoleculeViewerProps>(
  function MoleculeViewer(props, ref) {
    const {
      name,
      smiles,
      width = 320,
      height = 260,
      options,
      wasmPath = DEFAULT_WASM_PATH,
      resolver,
      engine: engineProp,
      debounceMs = 400,
      onResolved,
      onError,
      onSvg,
      ariaLabel,
      renderLoading,
      renderError,
      className,
      style,
    } = props;

    const engine = useMemo(
      () => engineProp ?? createRDKitEngine(wasmPath),
      [engineProp, wasmPath],
    );
    const { ready: engineReady, error: engineError } = useEngineReady(engine);
    const {
      structure,
      loading: resolving,
      error: resolveError,
    } = useResolvedStructure({ name, smiles, resolver, debounceMs });

    // Key drawing on the serialized options so inline option objects don't
    // force a redraw every render.
    const optionsKey = JSON.stringify(options ?? {});
    const mergedOptions = useMemo<DrawOptions>(
      () => ({
        ...(options ?? {}),
        width: options?.width ?? width,
        height: options?.height ?? height,
      }),
      // eslint-disable-next-line react-hooks/exhaustive-deps
      [optionsKey, width, height],
    );

    const outcome = useMemo<DrawOutcome>(() => {
      if (!engineReady || !structure) {
        return { svg: null, warning: null, error: null };
      }
      try {
        return {
          svg: engine.renderToSvg(structure.smiles, mergedOptions),
          warning: null,
          error: null,
        };
      } catch (cause) {
        const error = toMolstructError(cause, 'RENDER', 'Failed to draw the molecule.');
        if (error.code === 'INVALID_SMARTS') {
          // Bad highlight pattern is non-fatal: redraw without the highlight.
          try {
            const { highlight: _highlight, ...withoutHighlight } = mergedOptions;
            return {
              svg: engine.renderToSvg(structure.smiles, withoutHighlight),
              warning: error,
              error: null,
            };
          } catch (retryCause) {
            return {
              svg: null,
              warning: null,
              error: toMolstructError(retryCause, 'RENDER', 'Failed to draw the molecule.'),
            };
          }
        }
        return { svg: null, warning: null, error };
      }
    }, [engine, engineReady, structure, mergedOptions]);

    const label =
      ariaLabel ??
      `2D chemical structure of ${name?.trim() || structure?.query || 'a molecule'}`;
    const decoratedSvg = useMemo(() => {
      if (!outcome.svg) return null;
      const desc = structure
        ? `Skeletal formula rendered from SMILES: ${structure.smiles}`
        : 'Skeletal formula of a molecule';
      return decorateSvg(outcome.svg, label, desc);
    }, [outcome.svg, structure, label]);

    // --- callback effects (latest-ref pattern keeps deps minimal) ---
    const onResolvedRef = useLatest(onResolved);
    const onErrorRef = useLatest(onError);
    const onSvgRef = useLatest(onSvg);

    useEffect(() => {
      if (structure) onResolvedRef.current?.(structure);
    }, [structure, onResolvedRef]);

    const activeError = engineError ?? resolveError ?? outcome.error;
    useEffect(() => {
      if (activeError) onErrorRef.current?.(activeError);
    }, [activeError, onErrorRef]);

    useEffect(() => {
      if (outcome.warning) onErrorRef.current?.(outcome.warning);
    }, [outcome.warning, onErrorRef]);

    useEffect(() => {
      if (decoratedSvg) onSvgRef.current?.(decoratedSvg);
    }, [decoratedSvg, onSvgRef]);

    // --- imperative handle ---
    const svgRef = useLatest(decoratedSvg);
    useImperativeHandle(
      ref,
      (): MoleculeViewerHandle => ({
        getSvgString: () => svgRef.current,
        downloadSvg: (filename?: string) => {
          const svg = svgRef.current;
          if (!svg) return;
          const base = filename ?? `${(name?.trim() || 'molecule').replace(/\s+/g, '-')}.svg`;
          downloadSvgFile(svg, base);
        },
        copySvgToClipboard: async () => {
          const svg = svgRef.current;
          if (!svg) return false;
          return copyTextToClipboard(svg);
        },
      }),
      [svgRef, name],
    );

    // --- render states ---
    const frameStyle = {
      width: mergedOptions.width,
      minHeight: mergedOptions.height,
      ...style,
    };
    const rootClass = ['rms-viewer', className].filter(Boolean).join(' ');

    if (activeError) {
      return (
        <div className={rootClass} style={frameStyle}>
          {renderError ? (
            renderError(activeError)
          ) : (
            <div className="rms-viewer__error" role="alert">
              <span className="rms-viewer__error-badge" aria-hidden="true">
                !
              </span>
              <p>{describeError(activeError)}</p>
            </div>
          )}
        </div>
      );
    }

    const busy = (!engineReady && !engineError) || resolving;
    if (busy && !decoratedSvg) {
      return (
        <div className={rootClass} style={frameStyle} aria-busy="true">
          {renderLoading ? (
            renderLoading()
          ) : (
            <div className="rms-viewer__loading" role="status">
              <span className="rms-viewer__spinner" aria-hidden="true" />
              <span className="rms-viewer__loading-text">
                {!engineReady ? 'Loading chemistry engine…' : 'Resolving molecule…'}
              </span>
            </div>
          )}
        </div>
      );
    }

    if (!decoratedSvg) {
      return (
        <div className={rootClass} style={frameStyle}>
          <div className="rms-viewer__placeholder">
            <span>Enter a molecule name or SMILES to render its structure.</span>
          </div>
        </div>
      );
    }

    return (
      <div className={rootClass} style={frameStyle}>
        <div
          className="rms-viewer__svg"
          role="img"
          aria-label={label}
          // SVG is produced locally by RDKit from a SMILES string, with
          // metadata inserted through escapeXml — not raw remote markup.
          dangerouslySetInnerHTML={{ __html: decoratedSvg }}
        />
      </div>
    );
  },
);
