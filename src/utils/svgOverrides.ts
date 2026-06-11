import type { ColorInput, DrawOptions } from '../types';
import { toRdkitColor } from './color';

/** Converts any ColorInput to a CSS hex color for direct use in SVG markup. */
export function colorToCss(color: ColorInput | undefined): string | undefined {
  const rgb = toRdkitColor(color);
  if (!rgb) return undefined;
  const to2 = (f: number) =>
    Math.round(Math.min(1, Math.max(0, f)) * 255)
      .toString(16)
      .padStart(2, '0');
  return `#${to2(rgb[0])}${to2(rgb[1])}${to2(rgb[2])}`;
}

/** The engine-independent subset of DrawOptions applied by post-processing. */
export type SvgOverrideOptions = Pick<
  DrawOptions,
  'strokeColour' | 'textColour' | 'hideText' | 'strokeWidthScale' | 'roundedStrokes'
>;

/**
 * Applies universal styling overrides to an SVG produced by any engine.
 *
 * Handles both markup dialects this library encounters:
 * - RDKit: CSS in `style='…stroke:#000000;stroke-width:2.0px…'`, atom labels
 *   as glyph paths `<path class='atom-N' … fill='#FF0000'/>`.
 * - OpenChemLib: presentation attributes `stroke="rgb(0,0,0)"`,
 *   `stroke-width="3"`, labels as `<text … fill="rgb(255,13,13)">`.
 */
export function applySvgOverrides(svg: string, options: SvgOverrideOptions): string {
  let out = svg;

  if (options.hideText) {
    // Text elements (OpenChemLib labels, any legends rendered as text).
    out = out.replace(/<text[\s\S]*?<\/text>/g, '');
    // RDKit atom-label glyph paths: class begins with "atom-" (bond paths
    // begin with "bond-", so they are untouched).
    out = out.replace(/<path class=['"]atom-[\s\S]*?\/>/g, '');
  }

  const strokeCss = colorToCss(options.strokeColour);
  if (strokeCss) {
    // RDKit style-based strokes ("stroke:none" stays untouched).
    out = out.replace(/stroke:#[0-9a-fA-F]{3,8}/g, `stroke:${strokeCss}`);
    // Attribute-based strokes (OpenChemLib).
    out = out.replace(
      /stroke=(["'])(?:rgb\([^)]*\)|#[0-9a-fA-F]{3,8})\1/g,
      `stroke="${strokeCss}"`,
    );
  }

  const textCss = colorToCss(options.textColour);
  if (textCss) {
    // RDKit atom-label glyphs carry a fill attribute at the end of the path.
    out = out.replace(
      /(<path class=['"]atom-[\s\S]*?fill=['"])(?:#[0-9a-fA-F]{3,8}|rgb\([^)]*\))(['"])/g,
      `$1${textCss}$2`,
    );
    // OpenChemLib text fills.
    out = out.replace(
      /(<text[^>]*?fill=["'])(?:rgb\([^)]*\)|#[0-9a-fA-F]{3,8})(["'])/g,
      `$1${textCss}$2`,
    );
  }

  const scale = options.strokeWidthScale;
  if (scale != null && scale > 0 && scale !== 1) {
    out = out.replace(
      /stroke-width:([0-9.]+)px/g,
      (_match, width: string) => `stroke-width:${(parseFloat(width) * scale).toFixed(2)}px`,
    );
    out = out.replace(
      /stroke-width=(["'])([0-9.]+)\1/g,
      (_match, quote: string, width: string) =>
        `stroke-width=${quote}${(parseFloat(width) * scale).toFixed(2)}${quote}`,
    );
  }

  if (options.roundedStrokes) {
    // RDKit declares caps/joins inside style attributes.
    out = out.replace(/stroke-linecap:butt/g, 'stroke-linecap:round');
    out = out.replace(/stroke-linejoin:miter/g, 'stroke-linejoin:round');
    // OpenChemLib lines (and any element without explicit caps) get
    // presentation attributes; style-declared values still win where present.
    out = out.replace(
      /<(line|polyline|path)\b(?![^>]*stroke-linecap)([\s\S]*?)(\/?>)/g,
      '<$1$2 stroke-linecap="round" stroke-linejoin="round"$3',
    );
  }

  return out;
}

/**
 * Inserts an opaque background rectangle right after the opening <svg> tag,
 * sized from the viewBox (or width/height) so it covers the whole canvas.
 * Used for engines (OpenChemLib) that emit transparent backgrounds.
 */
export function injectSvgBackground(svg: string, color: ColorInput): string {
  const css = colorToCss(color);
  if (!css) return svg;
  const open = svg.match(/<svg\b[^>]*>/);
  if (!open) return svg;

  let x = 0;
  let y = 0;
  let width: number | null = null;
  let height: number | null = null;

  const viewBox = open[0].match(/viewBox=["']\s*([-\d.]+)[ ,]+([-\d.]+)[ ,]+([-\d.]+)[ ,]+([-\d.]+)\s*["']/);
  if (viewBox) {
    x = parseFloat(viewBox[1]);
    y = parseFloat(viewBox[2]);
    width = parseFloat(viewBox[3]);
    height = parseFloat(viewBox[4]);
  } else {
    const w = open[0].match(/width=["']([\d.]+)/);
    const h = open[0].match(/height=["']([\d.]+)/);
    if (w && h) {
      width = parseFloat(w[1]);
      height = parseFloat(h[1]);
    }
  }
  if (width == null || height == null) return svg;

  const rect = `<rect x="${x}" y="${y}" width="${width}" height="${height}" fill="${css}" stroke="none"/>`;
  return svg.replace(open[0], `${open[0]}${rect}`);
}
