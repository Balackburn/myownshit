import {
  useEffect,
  useId,
  useRef,
  useState,
  type ChangeEvent,
  type ReactNode,
  type RefObject,
} from 'react';
import { STYLE_PRESETS } from '../presets';
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
  /**
   * Active engine id ('rdkit' | 'openchemlib'). RDKit-only controls are
   * disabled and badged when the OpenChemLib fallback is in use.
   */
  engineId?: string;
  /** Show the one-click theme presets row. Default true. */
  showPresets?: boolean;
  /** Filename used by the Download actions (extension is adjusted). */
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

function Section(props: {
  title: string;
  defaultOpen?: boolean;
  children: ReactNode;
}) {
  return (
    <details className="rms-controls__section" open={props.defaultOpen}>
      <summary>
        <span className="rms-controls__chevron" aria-hidden="true" />
        {props.title}
      </summary>
      <div className="rms-controls__body">{props.children}</div>
    </details>
  );
}

function RdkitBadge() {
  return (
    <span className="rms-controls__badge" title="Only applies to the RDKit engine">
      RDKit
    </span>
  );
}

/**
 * Control panel driving a MoleculeViewer through a shared DrawOptions object:
 * one-click theme presets, canvas geometry, universal styling (stroke color,
 * text color, hide text, stroke width — these work with both the RDKit and
 * OpenChemLib engines), RDKit-specific styling, labels, substructure
 * highlighting, and SVG/PNG output actions. Fully keyboard-operable.
 */
export function MoleculeControls(props: MoleculeControlsProps) {
  const {
    options,
    onOptionsChange,
    viewerRef,
    engineId,
    showPresets = true,
    downloadFilename = 'molecule',
    className,
  } = props;
  const idBase = useId();
  const [copyState, setCopyState] = useState<CopyState>('idle');
  const [showSource, setShowSource] = useState(false);
  const [sourceText, setSourceText] = useState('');
  const [activePreset, setActivePreset] = useState<string | null>(null);
  const copyResetTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const oclMode = engineId === 'openchemlib';
  const fid = (suffix: string) => `${idBase}-${suffix}`;
  const baseName = downloadFilename.replace(/\.(svg|png)$/i, '');

  useEffect(() => {
    return () => {
      if (copyResetTimer.current) clearTimeout(copyResetTimer.current);
    };
  }, []);

  const patch = (partial: Partial<DrawOptions>, keepPreset = false) => {
    if (!keepPreset) setActivePreset(null);
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

  const handleToggleSource = () => {
    setShowSource((open) => {
      const next = !open;
      if (next) {
        setSourceText(viewerRef?.current?.getSvgString() ?? 'No SVG rendered yet.');
      }
      return next;
    });
  };

  const highlight = options.highlight;

  return (
    <form
      className={['rms-controls', className].filter(Boolean).join(' ')}
      onSubmit={(event) => event.preventDefault()}
      aria-label="Molecule drawing controls"
    >
      {showPresets && (
        <div className="rms-controls__presets" role="group" aria-label="Theme presets">
          {STYLE_PRESETS.map((preset) => (
            <button
              key={preset.id}
              type="button"
              className={[
                'rms-controls__preset',
                activePreset === preset.id ? 'is-active' : '',
              ]
                .filter(Boolean)
                .join(' ')}
              onClick={() => {
                setActivePreset(preset.id);
                patch(preset.options, true);
              }}
            >
              <span className="rms-controls__preset-dots" aria-hidden="true">
                {preset.swatches.map((swatch, index) => (
                  <i key={index} style={{ background: swatch }} />
                ))}
              </span>
              {preset.label}
            </button>
          ))}
        </div>
      )}

      <Section title="Canvas">
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
          <label htmlFor={fid('rotate')}>
            Rotation {options.rotate ?? 0}° {oclMode && <RdkitBadge />}
          </label>
          <input
            id={fid('rotate')}
            type="range"
            min={0}
            max={359}
            step={1}
            disabled={oclMode}
            value={options.rotate ?? 0}
            onChange={(e) => patch({ rotate: numberFromEvent(e) })}
          />
        </div>
        <div className="rms-controls__row">
          <label htmlFor={fid('padding')}>
            Padding {(options.padding ?? 0.06).toFixed(2)} {oclMode && <RdkitBadge />}
          </label>
          <input
            id={fid('padding')}
            type="range"
            min={0}
            max={0.3}
            step={0.01}
            disabled={oclMode}
            value={options.padding ?? 0.06}
            onChange={(e) => patch({ padding: numberFromEvent(e) })}
          />
        </div>
      </Section>

      <Section title="Strokes & colors" defaultOpen>
        <div className="rms-controls__row">
          <label htmlFor={fid('bond')}>
            Stroke width {(options.bondLineWidth ?? 1).toFixed(1)}
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
          <label htmlFor={fid('boldness')}>
            Line boldness ×{(options.strokeWidthScale ?? 1).toFixed(1)}
          </label>
          <input
            id={fid('boldness')}
            type="range"
            min={0.4}
            max={4}
            step={0.2}
            value={options.strokeWidthScale ?? 1}
            onChange={(e) => {
              const value = numberFromEvent(e);
              patch({ strokeWidthScale: value === 1 ? undefined : value });
            }}
          />
        </div>
        <div className="rms-controls__row rms-controls__row--check">
          <input
            id={fid('stroke-on')}
            type="checkbox"
            checked={options.strokeColour != null}
            onChange={(e) =>
              patch({ strokeColour: e.target.checked ? '#27322b' : undefined })
            }
          />
          <label htmlFor={fid('stroke-on')}>Override stroke color</label>
          <input
            aria-label="Stroke color"
            type="color"
            disabled={options.strokeColour == null}
            value={toHexColor(options.strokeColour, '#27322b')}
            onChange={(e) => patch({ strokeColour: e.target.value })}
          />
        </div>
        <div className="rms-controls__row rms-controls__row--check">
          <input
            id={fid('text-on')}
            type="checkbox"
            checked={options.textColour != null}
            onChange={(e) =>
              patch({ textColour: e.target.checked ? '#27322b' : undefined })
            }
          />
          <label htmlFor={fid('text-on')}>Override text color</label>
          <input
            aria-label="Text color"
            type="color"
            disabled={options.textColour == null}
            value={toHexColor(options.textColour, '#27322b')}
            onChange={(e) => patch({ textColour: e.target.value })}
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
          <label htmlFor={fid('dblgap')}>
            Double-bond gap {(options.multipleBondOffset ?? 0.15).toFixed(2)}{' '}
            {oclMode && <RdkitBadge />}
          </label>
          <input
            id={fid('dblgap')}
            type="range"
            min={0.05}
            max={0.4}
            step={0.01}
            disabled={oclMode}
            value={options.multipleBondOffset ?? 0.15}
            onChange={(e) => patch({ multipleBondOffset: numberFromEvent(e) })}
          />
        </div>
        <div className="rms-controls__row">
          <label htmlFor={fid('scheme')}>
            Atom palette {oclMode && <RdkitBadge />}
          </label>
          <select
            id={fid('scheme')}
            disabled={oclMode}
            value={options.colorScheme ?? 'default'}
            onChange={(e) => patch({ colorScheme: e.target.value as ColorScheme })}
          >
            <option value="default">RDKit default</option>
            <option value="monochrome">Monochrome</option>
            <option value="custom">Custom palette</option>
          </select>
        </div>
        {options.colorScheme === 'custom' && !oclMode && (
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
            disabled={oclMode}
            checked={options.comicMode ?? false}
            onChange={(e) => patch({ comicMode: e.target.checked })}
          />
          <label htmlFor={fid('comic')}>
            Hand-drawn look {oclMode ? <RdkitBadge /> : '(best effort)'}
          </label>
        </div>
      </Section>

      <Section title="Labels & text">
        <div className="rms-controls__row rms-controls__row--check">
          <input
            id={fid('hidetext')}
            type="checkbox"
            checked={options.hideText ?? false}
            onChange={(e) =>
              patch({ hideText: e.target.checked, noAtomLabels: e.target.checked })
            }
          />
          <label htmlFor={fid('hidetext')}>Hide all text (skeletal)</label>
        </div>
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
            disabled={oclMode}
            checked={options.addAtomIndices ?? false}
            onChange={(e) => patch({ addAtomIndices: e.target.checked })}
          />
          <label htmlFor={fid('indices')}>
            Atom indices {oclMode && <RdkitBadge />}
          </label>
        </div>
        <div className="rms-controls__row rms-controls__row--check">
          <input
            id={fid('bindices')}
            type="checkbox"
            disabled={oclMode}
            checked={options.addBondIndices ?? false}
            onChange={(e) => patch({ addBondIndices: e.target.checked })}
          />
          <label htmlFor={fid('bindices')}>
            Bond indices {oclMode && <RdkitBadge />}
          </label>
        </div>
        <div className="rms-controls__row rms-controls__row--check">
          <input
            id={fid('methyl')}
            type="checkbox"
            disabled={oclMode}
            checked={options.explicitMethyl ?? false}
            onChange={(e) => patch({ explicitMethyl: e.target.checked })}
          />
          <label htmlFor={fid('methyl')}>
            Explicit methyl groups {oclMode && <RdkitBadge />}
          </label>
        </div>
        <div className="rms-controls__row">
          <label htmlFor={fid('fontsize')}>
            Label size {options.labelFontSize ?? 'auto'} {oclMode && <RdkitBadge />}
          </label>
          <input
            id={fid('fontsize')}
            type="range"
            min={6}
            max={40}
            step={1}
            disabled={oclMode}
            value={options.labelFontSize ?? 16}
            onChange={(e) => patch({ labelFontSize: numberFromEvent(e) })}
          />
        </div>
        <div className="rms-controls__row">
          <label htmlFor={fid('legend')}>
            Caption {oclMode && <RdkitBadge />}
          </label>
          <input
            id={fid('legend')}
            type="text"
            disabled={oclMode}
            value={options.legend ?? ''}
            placeholder="e.g. aspirin"
            onChange={(e) => patch({ legend: e.target.value || undefined })}
          />
        </div>
      </Section>

      <Section title="Highlight">
        <div className="rms-controls__row">
          <label htmlFor={fid('smarts')}>
            SMARTS pattern {oclMode && <RdkitBadge />}
          </label>
          <input
            id={fid('smarts')}
            type="text"
            disabled={oclMode}
            value={highlight?.smarts ?? ''}
            placeholder="e.g. c1ccccc1"
            spellCheck={false}
            onChange={(e) => {
              const smarts = e.target.value;
              patch({
                highlight: smarts ? { smarts, color: highlight?.color } : undefined,
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
            disabled={oclMode || !highlight?.smarts}
            onChange={(e) =>
              highlight?.smarts &&
              patch({ highlight: { smarts: highlight.smarts, color: e.target.value } })
            }
          />
        </div>
      </Section>

      <Section title="Output" defaultOpen>
        <div className="rms-controls__actions">
          <button type="button" onClick={handleCopy} disabled={!viewerRef}>
            {copyState === 'copied'
              ? 'Copied!'
              : copyState === 'failed'
                ? 'Copy failed'
                : 'Copy SVG'}
          </button>
          <button
            type="button"
            onClick={() => viewerRef?.current?.downloadSvg(`${baseName}.svg`)}
            disabled={!viewerRef}
          >
            SVG
          </button>
          <button
            type="button"
            onClick={() => {
              void viewerRef?.current?.downloadPng(`${baseName}.png`, 3);
            }}
            disabled={!viewerRef}
          >
            PNG
          </button>
          <button
            type="button"
            onClick={handleToggleSource}
            disabled={!viewerRef}
            aria-expanded={showSource}
          >
            {showSource ? 'Hide source' : 'Source'}
          </button>
        </div>
        {showSource && (
          <pre className="rms-controls__source" tabIndex={0}>
            <code>{sourceText}</code>
          </pre>
        )}
      </Section>
    </form>
  );
}
