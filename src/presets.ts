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
   * and label toggles are left alone. `backgroundColour: undefined` means
   * fully transparent.
   */
  options: Partial<DrawOptions>;
}

/** All style keys every preset pins down, so switches never half-apply. */
const baseStyle: Partial<DrawOptions> = {
  backgroundColour: undefined,
  strokeColour: undefined,
  textColour: undefined,
  hideText: false,
  bondLineWidth: 1,
  strokeWidthScale: undefined,
  roundedStrokes: false,
  comicMode: false,
};

/**
 * Built-in visual themes (10). The universal keys (strokeColour, textColour,
 * hideText, strokeWidthScale, roundedStrokes) work with both the RDKit and
 * OpenChemLib engines. Backgrounds are transparent unless a theme sets one.
 */
export const STYLE_PRESETS: readonly StylePreset[] = [
  {
    id: 'classic',
    label: 'Classic',
    swatches: ['#ffffff', '#000000', '#ff0d0d'],
    options: { ...baseStyle },
  },
  {
    id: 'figma',
    label: 'Figma',
    swatches: ['#ffffff', '#0d99ff', '#1e1e1e'],
    options: {
      ...baseStyle,
      backgroundColour: '#ffffff',
      strokeColour: '#0d99ff',
      textColour: '#1e1e1e',
      bondLineWidth: 2.5,
      strokeWidthScale: 1.4,
      roundedStrokes: true,
    },
  },
  {
    id: 'ink',
    label: 'Ink',
    swatches: ['#f7f3ea', '#27322b', '#27322b'],
    options: {
      ...baseStyle,
      backgroundColour: '#f7f3ea',
      strokeColour: '#27322b',
      textColour: '#27322b',
      bondLineWidth: 1.5,
    },
  },
  {
    id: 'blueprint',
    label: 'Blueprint',
    swatches: ['#0d2a4d', '#cfe3ff', '#8fc4ff'],
    options: {
      ...baseStyle,
      backgroundColour: '#0d2a4d',
      strokeColour: '#cfe3ff',
      textColour: '#8fc4ff',
      bondLineWidth: 1.5,
      roundedStrokes: true,
    },
  },
  {
    id: 'neon',
    label: 'Neon',
    swatches: ['#101014', '#39ff88', '#ff5ec4'],
    options: {
      ...baseStyle,
      backgroundColour: '#101014',
      strokeColour: '#39ff88',
      textColour: '#ff5ec4',
      bondLineWidth: 2,
      roundedStrokes: true,
    },
  },
  {
    id: 'skeletal',
    label: 'Skeletal',
    swatches: ['#ffffff', '#1a1a1a', '#ffffff'],
    options: {
      ...baseStyle,
      strokeColour: '#1a1a1a',
      hideText: true,
      bondLineWidth: 2,
      roundedStrokes: true,
    },
  },
  {
    id: 'midnight',
    label: 'Midnight',
    swatches: ['#0b1021', '#a5b4fc', '#e0e7ff'],
    options: {
      ...baseStyle,
      backgroundColour: '#0b1021',
      strokeColour: '#a5b4fc',
      textColour: '#e0e7ff',
      bondLineWidth: 1.5,
    },
  },
  {
    id: 'candy',
    label: 'Candy',
    swatches: ['#fdf2f8', '#db2777', '#9d174d'],
    options: {
      ...baseStyle,
      backgroundColour: '#fdf2f8',
      strokeColour: '#db2777',
      textColour: '#9d174d',
      bondLineWidth: 2.5,
      roundedStrokes: true,
    },
  },
  {
    id: 'forest',
    label: 'Forest',
    swatches: ['#0f2417', '#7ddf9a', '#c9f3d5'],
    options: {
      ...baseStyle,
      backgroundColour: '#0f2417',
      strokeColour: '#7ddf9a',
      textColour: '#c9f3d5',
      bondLineWidth: 1.5,
      roundedStrokes: true,
    },
  },
  {
    id: 'comic',
    label: 'Comic',
    swatches: ['#fffbe8', '#3a2f20', '#b4552d'],
    options: {
      ...baseStyle,
      backgroundColour: '#fffbe8',
      bondLineWidth: 1.5,
      roundedStrokes: true,
      comicMode: true,
    },
  },
];
