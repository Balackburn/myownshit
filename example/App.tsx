import { useEffect, useMemo, useRef, useState } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';
import {
  Alert,
  Button,
  Chip,
  ComboBox,
  Input,
  Label,
  Link,
  ListBox,
} from '@heroui/react';
import {
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
import { HeroPanel } from './HeroPanel';

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
  const suppressSuggestRef = useRef(false);

  useEffect(() => {
    if (suppressSuggestRef.current) {
      suppressSuggestRef.current = false;
      return;
    }
    const query = name.trim();
    if (query.length < 3) {
      setSuggestions([]);
      return;
    }
    const controller = new AbortController();
    const timer = setTimeout(() => {
      fetchNameSuggestions(query, 8, controller.signal)
        .then(setSuggestions)
        .catch(() => {
          // Suggestions are best-effort; resolution still works without them.
        });
    }, 250);
    return () => {
      clearTimeout(timer);
      controller.abort();
    };
  }, [name]);

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
    <div ref={containerRef} className="mx-auto max-w-[1199px] px-4 pb-16">
      <nav className="flex h-16 items-center justify-between" aria-label="Site">
        <span className="font-bold tracking-tight">react-molstruct</span>
        <Link
          href="https://github.com/Balackburn/myownshit"
          target="_blank"
          rel="noreferrer"
        >
          GitHub
        </Link>
      </nav>

      <header className="pt-12 pb-8" data-reveal>
        <p className="mb-4 font-mono text-[11px] tracking-[0.16em] uppercase text-muted">
          Client-side chemistry
        </p>
        <h1 className="mb-3 text-[clamp(32px,5.5vw,44px)] leading-tight font-bold tracking-tight text-balance">
          Molecule structures, drawn in your browser.
        </h1>
        <p className="max-w-[65ch] text-muted">
          Type a molecule name. The browser asks PubChem for the SMILES, then
          renders the 2D structure locally — no backend anywhere.
        </p>
      </header>

      <section className="mb-6 flex flex-col gap-3" aria-label="Molecule lookup" data-reveal>
        <ComboBox
          allowsCustomValue
          menuTrigger="input"
          inputValue={name}
          onInputChange={(value) => {
            setName(value);
            setLastError(null);
          }}
          onSelectionChange={(key) => {
            if (key != null) {
              suppressSuggestRef.current = true;
              setName(String(key));
              setLastError(null);
            }
          }}
          className="max-w-105"
        >
          <Label>Molecule name</Label>
          <ComboBox.InputGroup>
            <Input placeholder="e.g. caffeine" autoComplete="off" />
            <ComboBox.Trigger />
          </ComboBox.InputGroup>
          <ComboBox.Popover>
            <ListBox>
              {suggestions.map((term) => (
                <ListBox.Item key={term} id={term} textValue={term}>
                  {term}
                </ListBox.Item>
              ))}
            </ListBox>
          </ComboBox.Popover>
        </ComboBox>
        <div className="flex flex-wrap gap-2" role="group" aria-label="Example molecules">
          {PRESETS.map((preset) => (
            <Button
              key={preset}
              size="sm"
              variant={preset === name ? 'primary' : 'tertiary'}
              onPress={() => {
                suppressSuggestRef.current = true;
                setName(preset);
                setLastError(null);
              }}
            >
              {preset}
            </Button>
          ))}
        </div>
      </section>

      <main className="flex flex-wrap items-start gap-6" data-reveal>
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
        <HeroPanel
          options={options}
          onOptionsChange={setOptions}
          viewerRef={viewerRef}
          engineId={wasmAvailable ? 'rdkit' : 'openchemlib'}
          downloadFilename={name.trim().replace(/\s+/g, '-') || 'molecule'}
        />
      </main>

      <footer className="mt-6 flex flex-col gap-3 text-sm text-muted" data-reveal>
        {!wasmAvailable && (
          <Alert status="accent">
            <Alert.Content>
              <Alert.Title>Compatibility mode</Alert.Title>
              <Alert.Description>
                WebAssembly is disabled in this browser (e.g. Safari Lockdown
                Mode), so structures render with the pure-JS OpenChemLib
                engine. Substructure highlights and some styling options are
                unavailable.
              </Alert.Description>
            </Alert.Content>
          </Alert>
        )}
        {resolved && (
          <p className="flex flex-wrap items-center gap-2">
            {resolved.resolvedAs && (
              <Chip size="sm" color="accent">
                Matched {resolved.resolvedAs}
              </Chip>
            )}
            <span>
              Resolved via <strong>{resolved.source}</strong>
              {resolved.cid != null && (
                <>
                  {' — CID '}
                  <Link
                    href={`https://pubchem.ncbi.nlm.nih.gov/compound/${resolved.cid}`}
                    target="_blank"
                    rel="noreferrer"
                  >
                    {resolved.cid}
                  </Link>
                </>
              )}
            </span>
            <code className="rounded-md bg-surface px-2 py-0.5 font-mono text-xs break-all">
              {resolved.smiles}
            </code>
          </p>
        )}
        {lastError && lastError.code === 'INVALID_SMARTS' && (
          <p>{describeError(lastError)}</p>
        )}
      </footer>
    </div>
  );
}
