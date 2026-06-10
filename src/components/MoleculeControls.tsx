import {
  useEffect,
  useId,
  useRef,
  useState,
  type ChangeEvent,
  type RefObject,
} from 'react';
import type {
  ColorScheme,
  DrawOptions,
  MoleculeViewerHandle,
} from '../types';
import { toHexColor } from '../utils/color';
import '../styles.css';

export interface MoleculeControlsProps {
  /** Current draw options (controlled). */
  options: DrawOptions;
  /** Receives the full next options object on every change. */
  onOptionsChange: (next: DrawOptions) => void;
  /** Ref to the MoleculeViewer this panel drives; enables the Output actions. */
  viewerRef?: RefObject<MoleculeViewerHandle | null>;
  /** Filename used by the Download action. Default "molecule.svg". */
  downloadFilename?: string;
  className?: string;
}

type CopyState = 'idle' | 'copied' | 'failed';

/** Elements offered by the custom-palette pickers: symbol, atomic number, default hex. */
const PALETTE_ELEMENTS: Array<[string, number, string]> = [
  ['C', 6, '#2b2b2b'],
  ['N', 7, '#2554a3'],
  ['O', 8, '#c0392b'],
  ['S', 16, '#b8860b'],
];

/**
 * Optional GUI panel that drives a MoleculeViewer through a shared DrawOptions
 * object: canvas geometry, styling, labels, substructure highlighting, and SVG
 * output actions (copy / download / view source). Fully keyboard-operable.
 */
export function MoleculeControls(props: MoleculeControlsProps) {
  const {
    options,
    onOptionsChange,
    viewerRef,
    downloadFilename = 'molecule.svg',
    className,
  } = props;
  const idBase = useId();
  const [copyState, setCopyState] = useState<CopyState>('idle');
  const [showSource, setShowSource] = useState(false);
  const [sourceText, setSourceText] = useState('');
  const copyResetTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (copyResetTimer.current) clearTimeout(copyResetTimer.current);
    };
  }, []);

  const patch = (partial: Partial<DrawOptions>) => {
    onOptionsChange({ ...options, ...partial });
  };

  const numberFromEvent = (event: ChangeEvent<HTMLInputElement>): number =>
    Number(event.target.value);

  const handleCopy = async () => {
    const ok = (await viewerRef?.current?.copySvgToClipboard()) ?? false;
    setCopyState(ok ? 'copied' : 'failed');
    if (copyResetTimer.current) clearTimeout(copyResetTimer.current);
    copyResetTimer.current = setTimeout(() => setCopyState('idle'), 1800);
  };

  const handleDownload = () => {
    viewerRef?.current?.downloadSvg(downloadFilename);
  };

  const handleToggleSource = () => {
    setShowSource((open) => {
      const next = !open;
      if (next) {
        setSourceText(
          viewerRef?.current?.getSvgString() ?? 'No SVG rendered yet.',
        );
      }
      return next;
    });
  };

  const fid = (suffix: string) => `${idBase}-${suffix}`;
  const highlight = options.highlight;

  return (
    <form
      className={['rms-controls', className].filter(Boolean).join(' ')}
      onSubmit={(event) => event.preventDefault()}
      aria-label="Molecule drawing controls"
    >
      <fieldset className="rms-controls__group">
        <legend>Canvas</legend>
        <div className="rms-controls__row">
          <label htmlFor={fid('width')}>Width {options.width ?? 320}px</label>
          <input
            id={fid('width')}
            type="range"
            min={140}
            max={800}
            step={10}
            value={options.width ?? 320}
            onChange={(e) => patch({ width: numberFromEvent(e) })}
          />
        </div>
        <div className="rms-controls__row">
          <label htmlFor={fid('height')}>Height {options.height ?? 260}px</label>
          <input
            id={fid('height')}
            type="range"
            min={140}
            max={800}
            step={10}
            value={options.height ?? 260}
            onChange={(e) => patch({ height: numberFromEvent(e) })}
          />
        </div>
        <div className="rms-controls__row">
          <label htmlFor={fid('rotate')}>Rotation {options.rotate ?? 0}°</label>
          <input
            id={fid('rotate')}
            type="range"
            min={0}
            max={359}
            step={1}
            value={options.rotate ?? 0}
            onChange={(e) => patch({ rotate: numberFromEvent(e) })}
          />
        </div>
        <div className="rms-controls__row">
          <label htmlFor={fid('padding')}>
            Padding {(options.padding ?? 0.06).toFixed(2)}
          </label>
          <input
            id={fid('padding')}
            type="range"
            min={0}
            max={0.3}
            step={0.01}
            value={options.padding ?? 0.06}
            onChange={(e) => patch({ padding: numberFromEvent(e) })}
          />
        </div>
      </fieldset>

      <fieldset className="rms-controls__group">
        <legend>Style</legend>
        <div className="rms-controls__row">
          <label htmlFor={fid('bond')}>
            Bond width {(options.bondLineWidth ?? 1).toFixed(1)}
          </label>
          <input
            id={fid('bond')}
            type="range"
            min={0.5}
            max={6}
            step={0.5}
            value={options.bondLineWidth ?? 1}
            onChange={(e) => patch({ bondLineWidth: numberFromEvent(e) })}
          />
        </div>
        <div className="rms-controls__row">
          <label htmlFor={fid('bg')}>Background</label>
          <input
            id={fid('bg')}
            type="color"
            value={toHexColor(options.backgroundColour, '#ffffff')}
            onChange={(e) => patch({ backgroundColour: e.target.value })}
          />
        </div>
        <div className="rms-controls__row">
          <label htmlFor={fid('scheme')}>Atom colors</label>
          <select
            id={fid('scheme')}
            value={options.colorScheme ?? 'default'}
            onChange={(e) => patch({ colorScheme: e.target.value as ColorScheme })}
          >
            <option value="default">RDKit default</option>
            <option value="monochrome">Monochrome</option>
            <option value="custom">Custom palette</option>
          </select>
        </div>
        {options.colorScheme === 'custom' && (
          <div className="rms-controls__palette">
            {PALETTE_ELEMENTS.map(([symbol, atomicNumber, fallback]) => (
              <span className="rms-controls__swatch" key={symbol}>
                <label htmlFor={fid(`pal-${symbol}`)}>{symbol}</label>
                <input
                  id={fid(`pal-${symbol}`)}
                  type="color"
                  value={toHexColor(options.customAtomPalette?.[atomicNumber], fallback)}
                  onChange={(e) =>
                    patch({
                      customAtomPalette: {
                        ...options.customAtomPalette,
                        [atomicNumber]: e.target.value,
                      },
                    })
                  }
                />
              </span>
            ))}
          </div>
        )}
        <div className="rms-controls__row rms-controls__row--check">
          <input
            id={fid('comic')}
            type="checkbox"
            checked={options.comicMode ?? false}
            onChange={(e) => patch({ comicMode: e.target.checked })}
          />
          <label htmlFor={fid('comic')}>Hand-drawn look (best effort)</label>
        </div>
      </fieldset>

      <fieldset className="rms-controls__group">
        <legend>Labels</legend>
        <div className="rms-controls__row rms-controls__row--check">
          <input
            id={fid('stereo')}
            type="checkbox"
            checked={options.addStereoAnnotation ?? false}
            onChange={(e) => patch({ addStereoAnnotation: e.target.checked })}
          />
          <label htmlFor={fid('stereo')}>Stereo annotations (R/S, E/Z)</label>
        </div>
        <div className="rms-controls__row rms-controls__row--check">
          <input
            id={fid('indices')}
            type="checkbox"
            checked={options.addAtomIndices ?? false}
            onChange={(e) => patch({ addAtomIndices: e.target.checked })}
          />
          <label htmlFor={fid('indices')}>Atom indices</label>
        </div>
        <div className="rms-controls__row rms-controls__row--check">
          <input
            id={fid('methyl')}
            type="checkbox"
            checked={options.explicitMethyl ?? false}
            onChange={(e) => patch({ explicitMethyl: e.target.checked })}
          />
          <label htmlFor={fid('methyl')}>Explicit methyl groups</label>
        </div>
        <div className="rms-controls__row rms-controls__row--check">
          <input
            id={fid('nolabels')}
            type="checkbox"
            checked={options.noAtomLabels ?? false}
            onChange={(e) => patch({ noAtomLabels: e.target.checked })}
          />
          <label htmlFor={fid('nolabels')}>Hide atom labels</label>
        </div>
        <div className="rms-controls__row">
          <label htmlFor={fid('legend')}>Caption</label>
          <input
            id={fid('legend')}
            type="text"
            value={options.legend ?? ''}
            placeholder="e.g. aspirin"
            onChange={(e) => patch({ legend: e.target.value || undefined })}
          />
        </div>
      </fieldset>

      <fieldset className="rms-controls__group">
        <legend>Highlight</legend>
        <div className="rms-controls__row">
          <label htmlFor={fid('smarts')}>SMARTS pattern</label>
          <input
            id={fid('smarts')}
            type="text"
            value={highlight?.smarts ?? ''}
            placeholder="e.g. c1ccccc1"
            spellCheck={false}
            onChange={(e) => {
              const smarts = e.target.value;
              patch({
                highlight: smarts
                  ? { smarts, color: highlight?.color }
                  : undefined,
              });
            }}
          />
        </div>
        <div className="rms-controls__row">
          <label htmlFor={fid('hlcolor')}>Highlight color</label>
          <input
            id={fid('hlcolor')}
            type="color"
            value={toHexColor(highlight?.color, '#ff8c8c')}
            disabled={!highlight?.smarts}
            onChange={(e) =>
              highlight?.smarts &&
              patch({ highlight: { smarts: highlight.smarts, color: e.target.value } })
            }
          />
        </div>
      </fieldset>

      <fieldset className="rms-controls__group">
        <legend>Output</legend>
        <div className="rms-controls__actions">
          <button type="button" onClick={handleCopy} disabled={!viewerRef}>
            {copyState === 'copied'
              ? 'Copied!'
              : copyState === 'failed'
                ? 'Copy failed'
                : 'Copy SVG'}
          </button>
          <button type="button" onClick={handleDownload} disabled={!viewerRef}>
            Download SVG
          </button>
          <button
            type="button"
            onClick={handleToggleSource}
            disabled={!viewerRef}
            aria-expanded={showSource}
          >
            {showSource ? 'Hide source' : 'View source'}
          </button>
        </div>
        {showSource && (
          <pre className="rms-controls__source" tabIndex={0}>
            <code>{sourceText}</code>
          </pre>
        )}
      </fieldset>
    </form>
  );
}
