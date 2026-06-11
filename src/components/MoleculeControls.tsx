import {
  useEffect,
  useId,
  useLayoutEffect,
  useRef,
  useState,
  type CSSProperties,
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
  /** Ref to the MoleculeViewer this panel drives; enables the Export actions. */
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

const TABS = ['Style', 'Canvas', 'Labels', 'Export'] as const;

/** Elements offered by the custom-palette pickers: symbol, atomic number, default hex. */
const PALETTE_ELEMENTS: Array<[string, number, string]> = [
  ['C', 6, '#2b2b2b'],
  ['N', 7, '#2554a3'],
  ['O', 8, '#c0392b'],
  ['S', 16, '#b8860b'],
];

function Badge() {
  return (
    <span className="rms-controls__badge" title="Only applies to the RDKit engine">
      RDKit
    </span>
  );
}

function Switch(props: {
  id: string;
  checked: boolean;
  disabled?: boolean;
  onChange: (checked: boolean) => void;
}) {
  return (
    <span className="rms-switch">
      <input
        id={props.id}
        type="checkbox"
        role="switch"
        checked={props.checked}
        disabled={props.disabled}
        onChange={(e) => props.onChange(e.target.checked)}
      />
      <span className="rms-switch__track" aria-hidden="true">
        <span className="rms-switch__knob" />
      </span>
    </span>
  );
}

function SwitchRow(props: {
  id: string;
  label: string;
  checked: boolean;
  disabled?: boolean;
  badge?: boolean;
  trailing?: ReactNode;
  onChange: (checked: boolean) => void;
}) {
  return (
    <div className="rms-controls__row">
      <label htmlFor={props.id}>
        {props.label}
        {props.badge && <Badge />}
      </label>
      <span className="rms-controls__trailing">
        {props.trailing}
        <Switch
          id={props.id}
          checked={props.checked}
          disabled={props.disabled}
          onChange={props.onChange}
        />
      </span>
    </div>
  );
}

function SliderRow(props: {
  id: string;
  label: string;
  display: string;
  value: number;
  min: number;
  max: number;
  step: number;
  disabled?: boolean;
  badge?: boolean;
  onChange: (value: number) => void;
}) {
  return (
    <div className="rms-controls__row rms-controls__row--slider">
      <div className="rms-controls__rowtop">
        <label htmlFor={props.id}>
          {props.label}
          {props.badge && <Badge />}
        </label>
        <span className="rms-controls__value">{props.display}</span>
      </div>
      <input
        id={props.id}
        type="range"
        min={props.min}
        max={props.max}
        step={props.step}
        disabled={props.disabled}
        value={props.value}
        onChange={(e: ChangeEvent<HTMLInputElement>) =>
          props.onChange(Number(e.target.value))
        }
      />
    </div>
  );
}

/**
 * Apple-style control panel driving a MoleculeViewer through a shared
 * DrawOptions object: segmented tabs with a sliding indicator, grouped
 * setting rows with switches, one-click theme presets, shuffle/reset, and
 * SVG/PNG export. Universal options (stroke color, text color, hide text,
 * stroke width/boldness, rounded caps) work with both engines; RDKit-only
 * rows are disabled and badged when the fallback engine is active.
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
  const fid = (suffix: string) => `${idBase}-${suffix}`;
  const oclMode = engineId === 'openchemlib';
  const baseName = downloadFilename.replace(/\.(svg|png)$/i, '');

  const [activeTab, setActiveTab] = useState(0);
  const [direction, setDirection] = useState(1);
  const [activePreset, setActivePreset] = useState<string | null>(null);
  const [copyState, setCopyState] = useState<CopyState>('idle');
  const [showSource, setShowSource] = useState(false);
  const [sourceText, setSourceText] = useState('');
  const copyResetTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Sliding indicator under the segmented control.
  const tabRefs = useRef<Array<HTMLButtonElement | null>>([]);
  const [indicator, setIndicator] = useState({ left: 0, width: 0 });
  useLayoutEffect(() => {
    const measure = () => {
      const el = tabRefs.current[activeTab];
      if (el) setIndicator({ left: el.offsetLeft, width: el.offsetWidth });
    };
    measure();
    window.addEventListener('resize', measure);
    return () => window.removeEventListener('resize', measure);
  }, [activeTab]);

  useEffect(() => {
    return () => {
      if (copyResetTimer.current) clearTimeout(copyResetTimer.current);
    };
  }, []);

  const patch = (partial: Partial<DrawOptions>, keepPreset = false) => {
    if (!keepPreset) setActivePreset(null);
    onOptionsChange({ ...options, ...partial });
  };

  const selectTab = (index: number) => {
    setDirection(index > activeTab ? 1 : -1);
    setActiveTab(index);
  };

  const applyPreset = (id: string) => {
    const preset = STYLE_PRESETS.find((p) => p.id === id);
    if (!preset) return;
    setActivePreset(id);
    patch(preset.options, true);
  };

  const shuffle = () => {
    const pool = STYLE_PRESETS.filter((p) => p.id !== activePreset);
    const next = pool[Math.floor(Math.random() * pool.length)];
    applyPreset(next.id);
  };

  const reset = () => {
    setActivePreset(null);
    onOptionsChange({ width: options.width, height: options.height });
  };

  const handleCopy = async () => {
    const ok = (await viewerRef?.current?.copySvgToClipboard()) ?? false;
    setCopyState(ok ? 'copied' : 'failed');
    if (copyResetTimer.current) clearTimeout(copyResetTimer.current);
    copyResetTimer.current = setTimeout(() => setCopyState('idle'), 1800);
  };

  const toggleSource = () => {
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
      onSubmit={(e) => e.preventDefault()}
      aria-label="Molecule drawing controls"
    >
      <header className="rms-controls__header">
        <span className="rms-controls__title">Appearance</span>
        <span className="rms-controls__header-actions">
          <button type="button" className="rms-btn rms-btn--soft" onClick={shuffle}>
            Shuffle
          </button>
          <button type="button" className="rms-btn rms-btn--soft" onClick={reset}>
            Reset
          </button>
        </span>
      </header>

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
              onClick={() => applyPreset(preset.id)}
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

      <div className="rms-controls__tabs" role="tablist" aria-label="Setting groups">
        <span
          className="rms-controls__tab-indicator"
          aria-hidden="true"
          style={{
            transform: `translateX(${indicator.left}px)`,
            width: indicator.width || undefined,
          }}
        />
        {TABS.map((tab, index) => (
          <button
            key={tab}
            ref={(el) => {
              tabRefs.current[index] = el;
            }}
            type="button"
            role="tab"
            id={fid(`tab-${index}`)}
            aria-selected={activeTab === index}
            aria-controls={fid('tabpanel')}
            className={[
              'rms-controls__tab',
              activeTab === index ? 'is-active' : '',
            ]
              .filter(Boolean)
              .join(' ')}
            onClick={() => selectTab(index)}
          >
            {tab}
          </button>
        ))}
      </div>

      <div
        key={activeTab}
        id={fid('tabpanel')}
        role="tabpanel"
        aria-labelledby={fid(`tab-${activeTab}`)}
        className="rms-controls__tabpanel"
        style={{ '--rms-dir': direction } as CSSProperties}
      >
        {activeTab === 0 && (
          <>
            <div className="rms-controls__caption">Strokes</div>
            <div className="rms-controls__group">
              <SliderRow
                id={fid('bond')}
                label="Stroke width"
                display={(options.bondLineWidth ?? 1).toFixed(1)}
                value={options.bondLineWidth ?? 1}
                min={0.5}
                max={6}
                step={0.5}
                onChange={(v) => patch({ bondLineWidth: v })}
              />
              <SliderRow
                id={fid('boldness')}
                label="Line boldness"
                display={`×${(options.strokeWidthScale ?? 1).toFixed(1)}`}
                value={options.strokeWidthScale ?? 1}
                min={0.4}
                max={4}
                step={0.2}
                onChange={(v) =>
                  patch({ strokeWidthScale: v === 1 ? undefined : v })
                }
              />
              <SwitchRow
                id={fid('rounded')}
                label="Rounded caps"
                checked={options.roundedStrokes ?? false}
                onChange={(v) => patch({ roundedStrokes: v })}
              />
            </div>
            <div className="rms-controls__caption">Colors</div>
            <div className="rms-controls__group">
              <SwitchRow
                id={fid('stroke-on')}
                label="Stroke color"
                checked={options.strokeColour != null}
                trailing={
                  <input
                    aria-label="Stroke color"
                    type="color"
                    disabled={options.strokeColour == null}
                    value={toHexColor(options.strokeColour, '#171717')}
                    onChange={(e) => patch({ strokeColour: e.target.value })}
                  />
                }
                onChange={(v) =>
                  patch({ strokeColour: v ? '#171717' : undefined })
                }
              />
              <SwitchRow
                id={fid('text-on')}
                label="Text color"
                checked={options.textColour != null}
                trailing={
                  <input
                    aria-label="Text color"
                    type="color"
                    disabled={options.textColour == null}
                    value={toHexColor(options.textColour, '#171717')}
                    onChange={(e) => patch({ textColour: e.target.value })}
                  />
                }
                onChange={(v) => patch({ textColour: v ? '#171717' : undefined })}
              />
              <SwitchRow
                id={fid('bg-on')}
                label="Background"
                checked={options.backgroundColour != null}
                trailing={
                  <input
                    aria-label="Background color"
                    type="color"
                    disabled={options.backgroundColour == null}
                    value={toHexColor(options.backgroundColour, '#ffffff')}
                    onChange={(e) => patch({ backgroundColour: e.target.value })}
                  />
                }
                onChange={(v) =>
                  patch({ backgroundColour: v ? '#ffffff' : undefined })
                }
              />
            </div>
            <div className="rms-controls__caption">Engine</div>
            <div className="rms-controls__group">
              <SliderRow
                id={fid('dblgap')}
                label="Double-bond gap"
                display={(options.multipleBondOffset ?? 0.15).toFixed(2)}
                value={options.multipleBondOffset ?? 0.15}
                min={0.05}
                max={0.4}
                step={0.01}
                disabled={oclMode}
                badge={oclMode}
                onChange={(v) => patch({ multipleBondOffset: v })}
              />
              <div className="rms-controls__row">
                <label htmlFor={fid('scheme')}>
                  Atom palette
                  {oclMode && <Badge />}
                </label>
                <select
                  id={fid('scheme')}
                  disabled={oclMode}
                  value={options.colorScheme ?? 'default'}
                  onChange={(e) =>
                    patch({ colorScheme: e.target.value as ColorScheme })
                  }
                >
                  <option value="default">Default</option>
                  <option value="monochrome">Monochrome</option>
                  <option value="custom">Custom</option>
                </select>
              </div>
              {options.colorScheme === 'custom' && !oclMode && (
                <div className="rms-controls__row rms-controls__row--palette">
                  {PALETTE_ELEMENTS.map(([symbol, atomicNumber, fallback]) => (
                    <span className="rms-controls__swatch" key={symbol}>
                      <label htmlFor={fid(`pal-${symbol}`)}>{symbol}</label>
                      <input
                        id={fid(`pal-${symbol}`)}
                        type="color"
                        value={toHexColor(
                          options.customAtomPalette?.[atomicNumber],
                          fallback,
                        )}
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
              <SwitchRow
                id={fid('comic')}
                label="Hand-drawn look"
                checked={options.comicMode ?? false}
                disabled={oclMode}
                badge={oclMode}
                onChange={(v) => patch({ comicMode: v })}
              />
            </div>
          </>
        )}

        {activeTab === 1 && (
          <div className="rms-controls__group">
            <SliderRow
              id={fid('width')}
              label="Width"
              display={`${options.width ?? 320}px`}
              value={options.width ?? 320}
              min={140}
              max={800}
              step={10}
              onChange={(v) => patch({ width: v })}
            />
            <SliderRow
              id={fid('height')}
              label="Height"
              display={`${options.height ?? 260}px`}
              value={options.height ?? 260}
              min={140}
              max={800}
              step={10}
              onChange={(v) => patch({ height: v })}
            />
            <SliderRow
              id={fid('rotate')}
              label="Rotation"
              display={`${options.rotate ?? 0}°`}
              value={options.rotate ?? 0}
              min={0}
              max={359}
              step={1}
              disabled={oclMode}
              badge={oclMode}
              onChange={(v) => patch({ rotate: v })}
            />
            <SliderRow
              id={fid('padding')}
              label="Padding"
              display={(options.padding ?? 0.06).toFixed(2)}
              value={options.padding ?? 0.06}
              min={0}
              max={0.3}
              step={0.01}
              disabled={oclMode}
              badge={oclMode}
              onChange={(v) => patch({ padding: v })}
            />
          </div>
        )}

        {activeTab === 2 && (
          <>
            <div className="rms-controls__caption">Text</div>
            <div className="rms-controls__group">
              <SwitchRow
                id={fid('hidetext')}
                label="Hide all text"
                checked={options.hideText ?? false}
                onChange={(v) => patch({ hideText: v, noAtomLabels: v })}
              />
              <SwitchRow
                id={fid('stereo')}
                label="Stereo annotations"
                checked={options.addStereoAnnotation ?? false}
                onChange={(v) => patch({ addStereoAnnotation: v })}
              />
              <SwitchRow
                id={fid('indices')}
                label="Atom indices"
                checked={options.addAtomIndices ?? false}
                disabled={oclMode}
                badge={oclMode}
                onChange={(v) => patch({ addAtomIndices: v })}
              />
              <SwitchRow
                id={fid('bindices')}
                label="Bond indices"
                checked={options.addBondIndices ?? false}
                disabled={oclMode}
                badge={oclMode}
                onChange={(v) => patch({ addBondIndices: v })}
              />
              <SwitchRow
                id={fid('methyl')}
                label="Explicit methyls"
                checked={options.explicitMethyl ?? false}
                disabled={oclMode}
                badge={oclMode}
                onChange={(v) => patch({ explicitMethyl: v })}
              />
              <SliderRow
                id={fid('fontsize')}
                label="Label size"
                display={options.labelFontSize != null ? `${options.labelFontSize}px` : 'Auto'}
                value={options.labelFontSize ?? 16}
                min={6}
                max={40}
                step={1}
                disabled={oclMode}
                badge={oclMode}
                onChange={(v) => patch({ labelFontSize: v })}
              />
              <div className="rms-controls__row">
                <label htmlFor={fid('legend')}>
                  Caption
                  {oclMode && <Badge />}
                </label>
                <input
                  id={fid('legend')}
                  type="text"
                  disabled={oclMode}
                  value={options.legend ?? ''}
                  placeholder="None"
                  onChange={(e) => patch({ legend: e.target.value || undefined })}
                />
              </div>
            </div>
            <div className="rms-controls__caption">Highlight</div>
            <div className="rms-controls__group">
              <div className="rms-controls__row">
                <label htmlFor={fid('smarts')}>
                  Highlight SMARTS
                  {oclMode && <Badge />}
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
                  disabled={oclMode || !highlight?.smarts}
                  onChange={(e) =>
                    highlight?.smarts &&
                    patch({
                      highlight: { smarts: highlight.smarts, color: e.target.value },
                    })
                  }
                />
              </div>
            </div>
          </>
        )}

        {activeTab === 3 && (
          <div className="rms-controls__group rms-controls__group--export">
            <div className="rms-controls__actions">
              <button
                type="button"
                className="rms-btn rms-btn--primary"
                onClick={handleCopy}
                disabled={!viewerRef}
              >
                {copyState === 'copied'
                  ? 'Copied'
                  : copyState === 'failed'
                    ? 'Copy failed'
                    : 'Copy SVG'}
              </button>
              <button
                type="button"
                className="rms-btn rms-btn--soft"
                onClick={() => viewerRef?.current?.downloadSvg(`${baseName}.svg`)}
                disabled={!viewerRef}
              >
                Download SVG
              </button>
              <button
                type="button"
                className="rms-btn rms-btn--soft"
                onClick={() => {
                  void viewerRef?.current?.downloadPng(`${baseName}.png`, 3);
                }}
                disabled={!viewerRef}
              >
                Download PNG
              </button>
              <button
                type="button"
                className="rms-btn rms-btn--soft"
                onClick={toggleSource}
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
          </div>
        )}
      </div>
    </form>
  );
}
