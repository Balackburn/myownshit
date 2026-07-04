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
    out = stripText(out);
  }

  const strokeCss = colorToCss(options.strokeColour);
  if (strokeCss) {
    // RDKit style-based strokes ("stroke:none" stays untouched).
    out = out.replace(/stroke:#[0-9a-fA-F]{3,8}/g, `stroke:${strokeCss}`);
    // Attribute-based strokes (OpenChemLib lines and wedge polygons).
    out = out.replace(
      /stroke=(["'])(?:rgb\([^)]*\)|#[0-9a-fA-F]{3,8})\1/g,
      `stroke="${strokeCss}"`,
    );
    // Solid stereo wedges are *filled* shapes, not strokes — recolor their
    // fill too so they read as part of the bond network, not a stray blob.
    // OpenChemLib draws them as <polygon fill="rgb(…)">.
    out = out.replace(
      /(<polygon\b[^>]*\bfill=["'])(?:rgb\([^)]*\)|#[0-9a-fA-F]{3,8})(["'])/g,
      `$1${strokeCss}$2`,
    );
    // RDKit draws them as <path class='bond-…' style='…fill:#hex…'> (normal
    // bonds use fill:none and are unaffected; the background rect and atom
    // glyphs are not bond paths, so they are left alone).
    out = out.replace(
      /<path\b[^>]*\bclass=['"]bond-[^>]*?\/>/g,
      (el) => el.replace(/fill:#[0-9a-fA-F]{3,8}/g, `fill:${strokeCss}`),
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
 * Removes every text element from an SVG for a pure skeletal depiction,
 * across both engine dialects, without touching bond geometry:
 *
 * - `<text>…</text>` and self-closing `<text/>` (OpenChemLib atom labels and
 *   any legend/annotation text).
 * - RDKit atom-label glyph paths, whose `class` attribute *starts with*
 *   `atom-`. Bond paths (`class='bond-… atom-… atom-…'`) start with `bond-`
 *   and are left intact, so this never deletes a bond.
 */
export function stripText(svg: string): string {
  return svg
    .replace(/<text\b[^>]*>[\s\S]*?<\/text>/g, '')
    .replace(/<text\b[^>]*\/>/g, '')
    .replace(/<tspan\b[^>]*>[\s\S]*?<\/tspan>/g, '')
    .replace(/<path\b[^>]*\bclass=['"]atom-[^'"]*['"][\s\S]*?\/>/g, '');
}

/**
 * Closes the gaps left where atom labels were/are drawn by snapping nearby
 * bond-line endpoints onto each label's atom centre, so a skeletal depiction
 * has bonds meeting cleanly at vertices instead of stopping short.
 *
 * Operates on OpenChemLib `<line>` bonds and `<text>` labels (RDKit avoids
 * the gap entirely by drawing with `noAtomLabels`, so it needs no fix-up).
 * Run this *before* {@link stripText}; it leaves the text elements in place.
 */
export function fillLabelGaps(svg: string): string {
  const labels: Array<{ cx: number; cy: number; r: number; maxMove: number }> = [];
  const textRe =
    /<text\b[^>]*?\bx="([\d.]+)"[^>]*?\by="([\d.]+)"[^>]*?\bfont-size="([\d.]+)"[^>]*>/g;
  for (let m = textRe.exec(svg); m; m = textRe.exec(svg)) {
    const x = parseFloat(m[1]);
    const y = parseFloat(m[2]);
    const fs = parseFloat(m[3]);
    // OpenChemLib anchors text at the left baseline; the connecting atom sits
    // roughly at the first glyph's centre, up and to the right of the anchor.
    labels.push({ cx: x + fs * 0.3, cy: y - fs * 0.34, r: fs * 1.15, maxMove: fs * 1.0 });
  }
  if (labels.length === 0) return svg;

  // Cap how far an endpoint may be moved. OpenChemLib offsets labels off-atom,
  // so the estimated centre can be wrong; a large snap would bend the bond.
  // Better a small residual gap than a broken-looking bond.
  const nearest = (px: number, py: number): { x: number; y: number } | null => {
    let best: { x: number; y: number } | null = null;
    let bd = Infinity;
    for (const l of labels) {
      const d = Math.hypot(px - l.cx, py - l.cy);
      if (d <= l.r && d <= l.maxMove && d < bd) {
        bd = d;
        best = { x: l.cx, y: l.cy };
      }
    }
    return best;
  };

  return svg.replace(/<line\b([^>]*?)\/>/g, (full, attrs: string) => {
    const x1 = attrs.match(/\bx1="([\d.]+)"/);
    const y1 = attrs.match(/\by1="([\d.]+)"/);
    const x2 = attrs.match(/\bx2="([\d.]+)"/);
    const y2 = attrs.match(/\by2="([\d.]+)"/);
    if (!x1 || !y1 || !x2 || !y2) return full;
    const p1 = { x: parseFloat(x1[1]), y: parseFloat(y1[1]) };
    const p2 = { x: parseFloat(x2[1]), y: parseFloat(y2[1]) };
    const s1 = nearest(p1.x, p1.y);
    const s2 = nearest(p2.x, p2.y);
    const n1 = s1 ?? p1;
    const n2 = s2 ?? p2;
    // Skip if snapping would collapse the bond to (near) a point.
    if (Math.hypot(n1.x - n2.x, n1.y - n2.y) < 1) return full;
    let next = attrs;
    if (s1) {
      next = next
        .replace(/\bx1="[\d.]+"/, `x1="${n1.x.toFixed(2)}"`)
        .replace(/\by1="[\d.]+"/, `y1="${n1.y.toFixed(2)}"`);
    }
    if (s2) {
      next = next
        .replace(/\bx2="[\d.]+"/, `x2="${n2.x.toFixed(2)}"`)
        .replace(/\by2="[\d.]+"/, `y2="${n2.y.toFixed(2)}"`);
    }
    return `<line${next}/>`;
  });
}

/**
 * Colors bonds that meet a colored atom label (heteroatoms) with that label's
 * color, so a skeletal depiction still shows oxygen/nitrogen/etc. by color even
 * after the text is stripped — mirroring how RDKit tints its half-bonds.
 *
 * OpenChemLib-oriented: reads `<text … fill="rgb(…)">` positions/colors and
 * recolors nearby `<line>` bonds. Black/near-black labels (carbon, hydrogen)
 * are ignored. Run before {@link stripText}; leaves the text in place.
 */
export function tintBondsToLabels(svg: string): string {
  const labels: Array<{ cx: number; cy: number; r: number; color: string }> = [];
  const re =
    /<text\b[^>]*?\bx="([\d.]+)"[^>]*?\by="([\d.]+)"[^>]*?\bfont-size="([\d.]+)"[^>]*?\bfill="([^"]+)"[^>]*>/g;
  for (let m = re.exec(svg); m; m = re.exec(svg)) {
    const color = m[4].trim();
    // Skip carbon/hydrogen (black) — only heteroatoms carry color.
    if (/^(#0{3,6}|rgb\(\s*0\s*,\s*0\s*,\s*0\s*\)|black)$/i.test(color)) continue;
    const x = parseFloat(m[1]);
    const y = parseFloat(m[2]);
    const fs = parseFloat(m[3]);
    labels.push({ cx: x + fs * 0.3, cy: y - fs * 0.34, r: fs * 1.6, color });
  }
  if (labels.length === 0) return svg;

  return svg.replace(/<line\b([^>]*?)\/>/g, (full, attrs: string) => {
    const x1 = attrs.match(/\bx1="([\d.]+)"/);
    const y1 = attrs.match(/\by1="([\d.]+)"/);
    const x2 = attrs.match(/\bx2="([\d.]+)"/);
    const y2 = attrs.match(/\by2="([\d.]+)"/);
    if (!x1 || !y1 || !x2 || !y2) return full;
    const near = (px: number, py: number) => {
      let best: string | null = null;
      let bd = Infinity;
      for (const l of labels) {
        const d = Math.hypot(px - l.cx, py - l.cy);
        if (d <= l.r && d < bd) {
          bd = d;
          best = l.color;
        }
      }
      return best;
    };
    const color =
      near(parseFloat(x1[1]), parseFloat(y1[1])) ??
      near(parseFloat(x2[1]), parseFloat(y2[1]));
    if (!color) return full;
    const next = attrs.replace(
      /\bstroke="(?:rgb\([^)]*\)|#[0-9a-fA-F]{3,8})"/,
      `stroke="${color}"`,
    );
    return next === attrs ? `<line${attrs} stroke="${color}"/>` : `<line${next}/>`;
  });
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
