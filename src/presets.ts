import type { DrawOptions } from './types';

/** A one-click visual theme: a named patch over the style-related DrawOptions. */
export interface StylePreset {
  id: string;
  label: string;
  /** Three representative colors shown as dots in the GUI: [background, stroke, text]. */
  swatches: [string, string, string];
  /**
   * Style patch. Every preset sets the same style keys (with `undefined` to
   * clear), so switching presets is deterministic; canvas size, highlights,
   * and label toggles are left alone.
   */
  options: Partial<DrawOptions>;
}

/**
 * Built-in visual themes. The universal keys (strokeColour, textColour,
 * hideText) work with both the RDKit and OpenChemLib engines.
 */
export const STYLE_PRESETS: readonly StylePreset[] = [
  {
    id: 'classic',
    label: 'Classic',
    swatches: ['#ffffff', '#000000', '#ff0d0d'],
    options: {
      backgroundColour: '#ffffff',
      strokeColour: undefined,
      textColour: undefined,
      hideText: false,
      bondLineWidth: 1,
      strokeWidthScale: undefined,
      comicMode: false,
    },
  },
  {
    id: 'ink',
    label: 'Ink',
    swatches: ['#f7f3ea', '#27322b', '#27322b'],
    options: {
      backgroundColour: '#f7f3ea',
      strokeColour: '#27322b',
      textColour: '#27322b',
      hideText: false,
      bondLineWidth: 1.5,
      strokeWidthScale: undefined,
      comicMode: false,
    },
  },
  {
    id: 'blueprint',
    label: 'Blueprint',
    swatches: ['#0d2a4d', '#cfe3ff', '#8fc4ff'],
    options: {
      backgroundColour: '#0d2a4d',
      strokeColour: '#cfe3ff',
      textColour: '#8fc4ff',
      hideText: false,
      bondLineWidth: 1.5,
      strokeWidthScale: undefined,
      comicMode: false,
    },
  },
  {
    id: 'neon',
    label: 'Neon',
    swatches: ['#101014', '#39ff88', '#ff5ec4'],
    options: {
      backgroundColour: '#101014',
      strokeColour: '#39ff88',
      textColour: '#ff5ec4',
      hideText: false,
      bondLineWidth: 2,
      strokeWidthScale: undefined,
      comicMode: false,
    },
  },
  {
    id: 'skeletal',
    label: 'Skeletal',
    swatches: ['#ffffff', '#1a1a1a', '#ffffff'],
    options: {
      backgroundColour: '#ffffff',
      strokeColour: '#1a1a1a',
      textColour: undefined,
      hideText: true,
      bondLineWidth: 2,
      strokeWidthScale: undefined,
      comicMode: false,
    },
  },
  {
    id: 'comic',
    label: 'Comic',
    swatches: ['#fffbe8', '#3a2f20', '#b4552d'],
    options: {
      backgroundColour: '#fffbe8',
      strokeColour: undefined,
      textColour: undefined,
      hideText: false,
      bondLineWidth: 1.5,
      strokeWidthScale: undefined,
      comicMode: true,
    },
  },
];
