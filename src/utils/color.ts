import type { ColorInput, RGBColor } from '../types';

/**
 * Converts a color (hex string or 0–1 float array) to RDKit's expected
 * [r, g, b] / [r, g, b, a] float format. Returns undefined for unparseable input.
 */
export function toRdkitColor(color: ColorInput | undefined): RGBColor | undefined {
  if (color == null) return undefined;
  if (Array.isArray(color)) return color;
  return hexToRgb01(color);
}

/** Parses "#rgb", "#rrggbb", or "#rrggbbaa" into 0–1 floats. */
export function hexToRgb01(hex: string): RGBColor | undefined {
  const value = hex.trim().replace(/^#/, '');
  if (!/^[0-9a-fA-F]{3}$|^[0-9a-fA-F]{6}$|^[0-9a-fA-F]{8}$/.test(value)) {
    return undefined;
  }
  if (value.length === 3) {
    const [r, g, b] = value.split('').map((c) => parseInt(c + c, 16) / 255);
    return [r, g, b];
  }
  const r = parseInt(value.slice(0, 2), 16) / 255;
  const g = parseInt(value.slice(2, 4), 16) / 255;
  const b = parseInt(value.slice(4, 6), 16) / 255;
  if (value.length === 8) {
    const a = parseInt(value.slice(6, 8), 16) / 255;
    return [r, g, b, a];
  }
  return [r, g, b];
}

/** Converts a ColorInput to a "#rrggbb" hex string for <input type="color">. */
export function toHexColor(color: ColorInput | undefined, fallback: string): string {
  if (color == null) return fallback;
  if (typeof color === 'string') {
    const parsed = hexToRgb01(color);
    if (!parsed) return fallback;
    return rgb01ToHex(parsed);
  }
  return rgb01ToHex(color);
}

function rgb01ToHex(rgb: RGBColor): string {
  const to2 = (f: number) =>
    Math.round(Math.min(1, Math.max(0, f)) * 255)
      .toString(16)
      .padStart(2, '0');
  return `#${to2(rgb[0])}${to2(rgb[1])}${to2(rgb[2])}`;
}
