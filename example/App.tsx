import {
  useEffect,
  useMemo,
  useRef,
  useState,
  type KeyboardEvent,
} from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';
import {
  MoleculeControls,
  MoleculeErrorBoundary,
  MoleculeViewer,
  createOpenChemLibEngine,
  describeError,
  fetchNameSuggestions,
  isWebAssemblyAvailable,
  type DrawOptions,
  type MoleculeViewerHandle,
  type MolstructError,
  type ResolvedStructure,
} from 'react-molstruct';
import 'react-molstruct/styles.css';

const PRESETS = ['aspirin', 'caffeine', 'ibuprofen', 'glucose', 'acetaminophen'];

export function App() {
  const [name, setName] = useState('aspirin');
  const [options, setOptions] = useState<DrawOptions>({
    width: 420,
    height: 340,
    addStereoAnnotation: true,
  });
  const [resolved, setResolved] = useState<ResolvedStructure | null>(null);
  const [lastError, setLastError] = useState<MolstructError | null>(null);
  const viewerRef = useRef<MoleculeViewerHandle | null>(null);

  // Live name suggestions from PubChem autocomplete.
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [suggestionsOpen, setSuggestionsOpen] = useState(false);
  const [highlightIndex, setHighlightIndex] = useState(-1);
  const suppressSuggestRef = useRef(false);

  useEffect(() => {
    if (suppressSuggestRef.current) {
      suppressSuggestRef.current = false;
      return;
    }
    const query = name.trim();
    if (query.length < 3) {
      setSuggestions([]);
      setSuggestionsOpen(false);
      return;
    }
    const controller = new AbortController();
    const timer = setTimeout(() => {
      fetchNameSuggestions(query, 8, controller.signal)
        .then((terms) => {
          setSuggestions(terms);
          setSuggestionsOpen(terms.length > 0);
          setHighlightIndex(-1);
        })
        .catch(() => {
          // Suggestions are best-effort; resolution still works without them.
        });
    }, 250);
    return () => {
      clearTimeout(timer);
      controller.abort();
    };
  }, [name]);

  const pickSuggestion = (term: string) => {
    suppressSuggestRef.current = true;
    setName(term);
    setLastError(null);
    setSuggestionsOpen(false);
    setHighlightIndex(-1);
  };

  const onNameKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (!suggestionsOpen || suggestions.length === 0) return;
    if (event.key === 'ArrowDown') {
      event.preventDefault();
      setHighlightIndex((i) => (i + 1) % suggestions.length);
    } else if (event.key === 'ArrowUp') {
      event.preventDefault();
      setHighlightIndex((i) => (i <= 0 ? suggestions.length - 1 : i - 1));
    } else if (event.key === 'Enter' && highlightIndex >= 0) {
      event.preventDefault();
      pickSuggestion(suggestions[highlightIndex]);
    } else if (event.key === 'Escape') {
      setSuggestionsOpen(false);
    }
  };

  // Safari Lockdown Mode (and similar) disables WebAssembly entirely;
  // fall back to the pure-JS OpenChemLib engine so the demo still renders.
  const wasmAvailable = isWebAssemblyAvailable();
  const fallbackEngine = useMemo(
    () => (wasmAvailable ? undefined : createOpenChemLibEngine()),
    [wasmAvailable],
  );

  // Entrance reveal: from bottom, ease-out, staggered — collapsed entirely
  // under prefers-reduced-motion.
  const containerRef = useRef<HTMLDivElement | null>(null);
  useGSAP(
    () => {
      const mm = gsap.matchMedia();
      mm.add('(prefers-reduced-motion: no-preference)', () => {
        gsap.fromTo(
          '[data-reveal]',
          { autoAlpha: 0, y: 40 },
          {
            autoAlpha: 1,
            y: 0,
            duration: 0.4,
            ease: 'power2.out',
            stagger: 0.08,
            clearProps: 'transform,opacity,visibility',
          },
        );
      });
    },
    { scope: containerRef },
  );

  return (
    <div className="demo" ref={containerRef}>
      <nav className="demo__nav" aria-label="Site">
        <a className="demo__brand" href="./">
          react-molstruct
        </a>
        <a
          href="https://github.com/Balackburn/myownshit"
          target="_blank"
          rel="noreferrer"
        >
          GitHub
        </a>
      </nav>

      <header className="demo__header" data-reveal>
        <p className="demo__eyebrow">Client-side chemistry</p>
        <h1>Molecule structures, drawn in your browser.</h1>
        <p>
          Type a molecule name. The browser asks PubChem for the SMILES, then
          renders the 2D structure locally — no backend anywhere.
        </p>
      </header>

      <section className="demo__query" aria-label="Molecule lookup" data-reveal>
        <label htmlFor="molecule-name">Molecule name</label>
        <div className="demo__combobox">
          <input
            id="molecule-name"
            type="text"
            value={name}
            placeholder="e.g. caffeine"
            autoComplete="off"
            role="combobox"
            aria-expanded={suggestionsOpen}
            aria-controls="molecule-suggestions"
            aria-autocomplete="list"
            onChange={(event) => {
              setName(event.target.value);
              setLastError(null);
            }}
            onKeyDown={onNameKeyDown}
            onBlur={() => setSuggestionsOpen(false)}
            onFocus={() => suggestions.length > 0 && setSuggestionsOpen(true)}
          />
          {suggestionsOpen && (
            <ul
              id="molecule-suggestions"
              className="demo__suggestions"
              role="listbox"
              aria-label="Name suggestions"
            >
              {suggestions.map((term, index) => (
                <li
                  key={term}
                  role="option"
                  aria-selected={index === highlightIndex}
                  className={[
                    'demo__suggestion',
                    index === highlightIndex ? 'is-highlighted' : '',
                  ]
                    .filter(Boolean)
                    .join(' ')}
                  // mousedown so selection wins over the input's blur
                  onMouseDown={(event) => {
                    event.preventDefault();
                    pickSuggestion(term);
                  }}
                  onMouseEnter={() => setHighlightIndex(index)}
                >
                  {term}
                </li>
              ))}
            </ul>
          )}
        </div>
        <div className="demo__presets" role="group" aria-label="Example molecules">
          {PRESETS.map((preset) => (
            <button
              key={preset}
              type="button"
              className={preset === name ? 'is-active' : undefined}
              onClick={() => {
                setName(preset);
                setLastError(null);
              }}
            >
              {preset}
            </button>
          ))}
        </div>
      </section>

      <main className="demo__stage" data-reveal>
        <MoleculeErrorBoundary>
          <MoleculeViewer
            ref={viewerRef}
            name={name}
            options={options}
            engine={fallbackEngine}
            wasmPath={`${import.meta.env.BASE_URL}rdkit`}
            onResolved={(structure) => {
              setResolved(structure);
              setLastError(null);
            }}
            onError={(error) => setLastError(error)}
          />
        </MoleculeErrorBoundary>
        <MoleculeControls
          options={options}
          onOptionsChange={setOptions}
          viewerRef={viewerRef}
          engineId={wasmAvailable ? 'rdkit' : 'openchemlib'}
          downloadFilename={name.trim().replace(/\s+/g, '-') || 'molecule'}
        />
      </main>

      <footer className="demo__meta" data-reveal>
        {!wasmAvailable && (
          <p className="demo__warning">
            WebAssembly is disabled in this browser (e.g. Safari Lockdown
            Mode), so structures render with the pure-JS OpenChemLib engine.
            Substructure highlights and most styling options are unavailable
            in this mode.
          </p>
        )}
        {resolved && (
          <p>
            {resolved.resolvedAs && (
              <>
                Matched <strong>{resolved.resolvedAs}</strong> —{' '}
              </>
            )}
            Resolved via <strong>{resolved.source}</strong>
            {resolved.cid != null && (
              <>
                {' '}
                — PubChem CID{' '}
                <a
                  href={`https://pubchem.ncbi.nlm.nih.gov/compound/${resolved.cid}`}
                  target="_blank"
                  rel="noreferrer"
                >
                  {resolved.cid}
                </a>
              </>
            )}
            {' — '}
            <code>{resolved.smiles}</code>
          </p>
        )}
        {lastError && lastError.code === 'INVALID_SMARTS' && (
          <p className="demo__warning">{describeError(lastError)}</p>
        )}
      </footer>
    </div>
  );
}
