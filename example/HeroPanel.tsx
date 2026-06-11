import { useRef, useState, type ReactNode, type RefObject } from 'react';
import {
  Button,
  Card,
  Chip,
  Label,
  ListBox,
  Select,
  Slider,
  Switch,
  Tabs,
  TextField,
  Input,
} from '@heroui/react';
import {
  STYLE_PRESETS,
  type ColorScheme,
  type DrawOptions,
  type MoleculeViewerHandle,
  toHexColor,
} from 'react-molstruct';

export interface HeroPanelProps {
  options: DrawOptions;
  onOptionsChange: (next: DrawOptions) => void;
  viewerRef: RefObject<MoleculeViewerHandle | null>;
  /** 'rdkit' | 'openchemlib' — RDKit-only rows are disabled in fallback mode. */
  engineId: string;
  downloadFilename: string;
}

function RdkitChip() {
  return (
    <Chip size="sm" color="default" className="ml-2 align-middle">
      RDKit
    </Chip>
  );
}

function SliderRow(props: {
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
    <Slider
      aria-label={props.label}
      className="w-full"
      value={props.value}
      minValue={props.min}
      maxValue={props.max}
      step={props.step}
      isDisabled={props.disabled}
      onChange={(value) =>
        props.onChange(Array.isArray(value) ? value[0] : value)
      }
    >
      <div className="flex w-full items-center justify-between">
        <Label className="text-sm">
          {props.label}
          {props.badge && <RdkitChip />}
        </Label>
        <span className="font-mono text-xs text-muted">{props.display}</span>
      </div>
      <Slider.Track>
        <Slider.Fill />
        <Slider.Thumb />
      </Slider.Track>
    </Slider>
  );
}

function SwitchRow(props: {
  label: string;
  checked: boolean;
  disabled?: boolean;
  badge?: boolean;
  trailing?: ReactNode;
  onChange: (checked: boolean) => void;
}) {
  return (
    <div className="flex items-center justify-between gap-3">
      <span className="text-sm">
        {props.label}
        {props.badge && <RdkitChip />}
      </span>
      <span className="flex items-center gap-2">
        {props.trailing}
        <Switch
          aria-label={props.label}
          isSelected={props.checked}
          isDisabled={props.disabled}
          onChange={props.onChange}
        >
          <Switch.Control>
            <Switch.Thumb />
          </Switch.Control>
        </Switch>
      </span>
    </div>
  );
}

function ColorWell(props: {
  label: string;
  value: string;
  disabled?: boolean;
  onChange: (hex: string) => void;
}) {
  return (
    <input
      aria-label={props.label}
      type="color"
      disabled={props.disabled}
      value={props.value}
      onChange={(e) => props.onChange(e.target.value)}
      className="size-7 cursor-pointer rounded-md border border-default disabled:cursor-not-allowed disabled:opacity-40"
    />
  );
}

/**
 * HeroUI v3 control panel for the demo: tabs, sliders, switches, preset
 * chips, and SVG/PNG export, driving the library's DrawOptions object.
 */
export function HeroPanel(props: HeroPanelProps) {
  const { options, onOptionsChange, viewerRef, engineId, downloadFilename } =
    props;
  const oclMode = engineId === 'openchemlib';
  const baseName = downloadFilename.replace(/\.(svg|png)$/i, '');

  const [activePreset, setActivePreset] = useState<string | null>(null);
  const [copyLabel, setCopyLabel] = useState('Copy SVG');
  const [showSource, setShowSource] = useState(false);
  const [sourceText, setSourceText] = useState('');
  const copyTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const patch = (partial: Partial<DrawOptions>, keepPreset = false) => {
    if (!keepPreset) setActivePreset(null);
    onOptionsChange({ ...options, ...partial });
  };

  const applyPreset = (id: string) => {
    const preset = STYLE_PRESETS.find((p) => p.id === id);
    if (!preset) return;
    setActivePreset(id);
    patch(preset.options, true);
  };

  const shuffle = () => {
    const pool = STYLE_PRESETS.filter((p) => p.id !== activePreset);
    applyPreset(pool[Math.floor(Math.random() * pool.length)].id);
  };

  const handleCopy = async () => {
    const ok = (await viewerRef.current?.copySvgToClipboard()) ?? false;
    setCopyLabel(ok ? 'Copied' : 'Copy failed');
    if (copyTimer.current) clearTimeout(copyTimer.current);
    copyTimer.current = setTimeout(() => setCopyLabel('Copy SVG'), 1800);
  };

  const highlight = options.highlight;

  return (
    <Card className="w-full max-w-95 shrink-0 p-4">
      <div className="mb-3 flex items-center justify-between">
        <span className="font-mono text-[11px] tracking-[0.16em] uppercase text-muted">
          Appearance
        </span>
        <span className="flex gap-2">
          <Button size="sm" variant="secondary" onPress={shuffle}>
            Shuffle
          </Button>
          <Button
            size="sm"
            variant="secondary"
            onPress={() => {
              setActivePreset(null);
              onOptionsChange({ width: options.width, height: options.height });
            }}
          >
            Reset
          </Button>
        </span>
      </div>

      <div className="mb-3 flex flex-wrap gap-1.5" role="group" aria-label="Theme presets">
        {STYLE_PRESETS.map((preset) => (
          <Button
            key={preset.id}
            size="sm"
            variant={activePreset === preset.id ? 'primary' : 'tertiary'}
            onPress={() => applyPreset(preset.id)}
          >
            <span className="mr-1.5 inline-flex gap-0.5" aria-hidden="true">
              {preset.swatches.map((swatch, i) => (
                <i
                  key={i}
                  className="size-2.5 rounded-full shadow-[inset_0_0_0_1px_rgba(0,0,0,0.15)]"
                  style={{ background: swatch }}
                />
              ))}
            </span>
            {preset.label}
          </Button>
        ))}
      </div>

      <Tabs defaultSelectedKey="style">
        <Tabs.ListContainer>
          <Tabs.List aria-label="Setting groups">
            <Tabs.Tab id="style">
              Style
              <Tabs.Indicator />
            </Tabs.Tab>
            <Tabs.Tab id="canvas">
              Canvas
              <Tabs.Indicator />
            </Tabs.Tab>
            <Tabs.Tab id="labels">
              Labels
              <Tabs.Indicator />
            </Tabs.Tab>
            <Tabs.Tab id="export">
              Export
              <Tabs.Indicator />
            </Tabs.Tab>
          </Tabs.List>
        </Tabs.ListContainer>

        <Tabs.Panel id="style" className="flex flex-col gap-4 pt-4">
          <SliderRow
            label="Stroke width"
            display={(options.bondLineWidth ?? 1).toFixed(1)}
            value={options.bondLineWidth ?? 1}
            min={0.5}
            max={6}
            step={0.5}
            onChange={(v) => patch({ bondLineWidth: v })}
          />
          <SliderRow
            label="Line boldness"
            display={`×${(options.strokeWidthScale ?? 1).toFixed(1)}`}
            value={options.strokeWidthScale ?? 1}
            min={0.4}
            max={4}
            step={0.2}
            onChange={(v) => patch({ strokeWidthScale: v === 1 ? undefined : v })}
          />
          <SwitchRow
            label="Rounded caps"
            checked={options.roundedStrokes ?? false}
            onChange={(v) => patch({ roundedStrokes: v })}
          />
          <SwitchRow
            label="Stroke color"
            checked={options.strokeColour != null}
            trailing={
              <ColorWell
                label="Stroke color"
                disabled={options.strokeColour == null}
                value={toHexColor(options.strokeColour, '#171717')}
                onChange={(hex) => patch({ strokeColour: hex })}
              />
            }
            onChange={(v) => patch({ strokeColour: v ? '#171717' : undefined })}
          />
          <SwitchRow
            label="Text color"
            checked={options.textColour != null}
            trailing={
              <ColorWell
                label="Text color"
                disabled={options.textColour == null}
                value={toHexColor(options.textColour, '#171717')}
                onChange={(hex) => patch({ textColour: hex })}
              />
            }
            onChange={(v) => patch({ textColour: v ? '#171717' : undefined })}
          />
          <SwitchRow
            label="Background"
            checked={options.backgroundColour != null}
            trailing={
              <ColorWell
                label="Background color"
                disabled={options.backgroundColour == null}
                value={toHexColor(options.backgroundColour, '#ffffff')}
                onChange={(hex) => patch({ backgroundColour: hex })}
              />
            }
            onChange={(v) => patch({ backgroundColour: v ? '#ffffff' : undefined })}
          />
          <SliderRow
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
          <div className="flex items-center justify-between gap-3">
            <span className="text-sm">
              Atom palette
              {oclMode && <RdkitChip />}
            </span>
            <Select
              aria-label="Atom palette"
              className="w-40"
              isDisabled={oclMode}
              selectedKey={options.colorScheme ?? 'default'}
              onSelectionChange={(key) =>
                patch({ colorScheme: String(key) as ColorScheme })
              }
            >
              <Select.Trigger>
                <Select.Value />
                <Select.Indicator />
              </Select.Trigger>
              <Select.Popover>
                <ListBox>
                  <ListBox.Item id="default" textValue="Default">
                    Default
                  </ListBox.Item>
                  <ListBox.Item id="monochrome" textValue="Monochrome">
                    Monochrome
                  </ListBox.Item>
                  <ListBox.Item id="custom" textValue="Custom">
                    Custom
                  </ListBox.Item>
                </ListBox>
              </Select.Popover>
            </Select>
          </div>
          {options.colorScheme === 'custom' && !oclMode && (
            <div className="flex gap-4">
              {(
                [
                  ['C', 6, '#2b2b2b'],
                  ['N', 7, '#2554a3'],
                  ['O', 8, '#c0392b'],
                  ['S', 16, '#b8860b'],
                ] as Array<[string, number, string]>
              ).map(([symbol, atomicNumber, fallback]) => (
                <span key={symbol} className="flex flex-col items-center gap-1">
                  <span className="font-mono text-xs text-muted">{symbol}</span>
                  <ColorWell
                    label={`${symbol} color`}
                    value={toHexColor(
                      options.customAtomPalette?.[atomicNumber],
                      fallback,
                    )}
                    onChange={(hex) =>
                      patch({
                        customAtomPalette: {
                          ...options.customAtomPalette,
                          [atomicNumber]: hex,
                        },
                      })
                    }
                  />
                </span>
              ))}
            </div>
          )}
          <SwitchRow
            label="Hand-drawn look"
            checked={options.comicMode ?? false}
            disabled={oclMode}
            badge={oclMode}
            onChange={(v) => patch({ comicMode: v })}
          />
        </Tabs.Panel>

        <Tabs.Panel id="canvas" className="flex flex-col gap-4 pt-4">
          <SliderRow
            label="Width"
            display={`${options.width ?? 320}px`}
            value={options.width ?? 320}
            min={140}
            max={800}
            step={10}
            onChange={(v) => patch({ width: v })}
          />
          <SliderRow
            label="Height"
            display={`${options.height ?? 260}px`}
            value={options.height ?? 260}
            min={140}
            max={800}
            step={10}
            onChange={(v) => patch({ height: v })}
          />
          <SliderRow
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
        </Tabs.Panel>

        <Tabs.Panel id="labels" className="flex flex-col gap-4 pt-4">
          <SwitchRow
            label="Hide all text"
            checked={options.hideText ?? false}
            onChange={(v) => patch({ hideText: v, noAtomLabels: v })}
          />
          <SwitchRow
            label="Stereo annotations"
            checked={options.addStereoAnnotation ?? false}
            onChange={(v) => patch({ addStereoAnnotation: v })}
          />
          <SwitchRow
            label="Atom indices"
            checked={options.addAtomIndices ?? false}
            disabled={oclMode}
            badge={oclMode}
            onChange={(v) => patch({ addAtomIndices: v })}
          />
          <SwitchRow
            label="Explicit methyls"
            checked={options.explicitMethyl ?? false}
            disabled={oclMode}
            badge={oclMode}
            onChange={(v) => patch({ explicitMethyl: v })}
          />
          <SliderRow
            label="Label size"
            display={
              options.labelFontSize != null ? `${options.labelFontSize}px` : 'Auto'
            }
            value={options.labelFontSize ?? 16}
            min={6}
            max={40}
            step={1}
            disabled={oclMode}
            badge={oclMode}
            onChange={(v) => patch({ labelFontSize: v })}
          />
          <TextField
            value={options.legend ?? ''}
            isDisabled={oclMode}
            onChange={(value) => patch({ legend: value || undefined })}
          >
            <Label className="text-sm">
              Caption
              {oclMode && <RdkitChip />}
            </Label>
            <Input placeholder="None" />
          </TextField>
          <TextField
            value={highlight?.smarts ?? ''}
            isDisabled={oclMode}
            onChange={(smarts) =>
              patch({
                highlight: smarts ? { smarts, color: highlight?.color } : undefined,
              })
            }
          >
            <Label className="text-sm">
              Highlight SMARTS
              {oclMode && <RdkitChip />}
            </Label>
            <Input placeholder="e.g. c1ccccc1" spellCheck={false} />
          </TextField>
          <SwitchRow
            label="Highlight color"
            checked={!!highlight?.smarts}
            disabled
            trailing={
              <ColorWell
                label="Highlight color"
                disabled={oclMode || !highlight?.smarts}
                value={toHexColor(highlight?.color, '#ff8c8c')}
                onChange={(hex) =>
                  highlight?.smarts &&
                  patch({ highlight: { smarts: highlight.smarts, color: hex } })
                }
              />
            }
            onChange={() => undefined}
          />
        </Tabs.Panel>

        <Tabs.Panel id="export" className="flex flex-col gap-3 pt-4">
          <div className="flex flex-wrap gap-2">
            <Button size="sm" variant="primary" onPress={handleCopy}>
              {copyLabel}
            </Button>
            <Button
              size="sm"
              variant="secondary"
              onPress={() => viewerRef.current?.downloadSvg(`${baseName}.svg`)}
            >
              Download SVG
            </Button>
            <Button
              size="sm"
              variant="secondary"
              onPress={() => {
                void viewerRef.current?.downloadPng(`${baseName}.png`, 3);
              }}
            >
              Download PNG
            </Button>
            <Button
              size="sm"
              variant="secondary"
              onPress={() => {
                setShowSource((open) => {
                  if (!open) {
                    setSourceText(
                      viewerRef.current?.getSvgString() ?? 'No SVG rendered yet.',
                    );
                  }
                  return !open;
                });
              }}
            >
              {showSource ? 'Hide source' : 'View source'}
            </Button>
          </div>
          {showSource && (
            <pre
              tabIndex={0}
              className="max-h-44 overflow-auto rounded-lg bg-surface p-2 font-mono text-xs leading-relaxed break-all whitespace-pre-wrap"
            >
              <code>{sourceText}</code>
            </pre>
          )}
        </Tabs.Panel>
      </Tabs>
    </Card>
  );
}
