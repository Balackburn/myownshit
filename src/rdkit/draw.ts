import { MolstructError } from '../errors';
import type { DrawOptions } from '../types';
import { toRdkitColor } from '../utils/color';
import type { JSMol, RDKitModule } from './types';

export const DEFAULT_DRAW_OPTIONS: Required<
  Pick<DrawOptions, 'width' | 'height' | 'bondLineWidth' | 'padding'>
> = {
  width: 320,
  height: 260,
  bondLineWidth: 1,
  padding: 0.06,
};

const DEFAULT_HIGHLIGHT_COLOR: [number, number, number] = [1, 0.55, 0.55];

/**
 * Renders a SMILES string to an SVG via RDKit's get_svg_with_highlights.
 *
 * Throws MolstructError('INVALID_SMILES') when RDKit rejects the molecule and
 * MolstructError('INVALID_SMARTS') when options.highlight.smarts is invalid
 * (callers may retry without the highlight). All WASM objects are freed.
 */
export function drawMoleculeToSvg(
  rdkit: RDKitModule,
  smiles: string,
  options: DrawOptions = {},
): string {
  let mol: JSMol | null = null;
  try {
    try {
      mol = rdkit.get_mol(smiles);
    } catch (cause) {
      throw new MolstructError('INVALID_SMILES', `RDKit could not parse: ${smiles}`, cause);
    }
    if (!mol || !mol.is_valid()) {
      throw new MolstructError('INVALID_SMILES', `RDKit could not parse: ${smiles}`);
    }
    const details = buildDetails(rdkit, mol, options);
    try {
      return mol.get_svg_with_highlights(JSON.stringify(details));
    } catch (cause) {
      throw new MolstructError('RENDER', 'RDKit failed to render the molecule.', cause);
    }
  } finally {
    mol?.delete();
  }
}

/** Validates a SMILES string against RDKit without rendering. */
export function isValidSmiles(rdkit: RDKitModule, smiles: string): boolean {
  let mol: JSMol | null = null;
  try {
    mol = rdkit.get_mol(smiles);
    return !!mol && mol.is_valid();
  } catch {
    return false;
  } finally {
    mol?.delete();
  }
}

function buildDetails(
  rdkit: RDKitModule,
  mol: JSMol,
  options: DrawOptions,
): Record<string, unknown> {
  const details: Record<string, unknown> = {
    width: options.width ?? DEFAULT_DRAW_OPTIONS.width,
    height: options.height ?? DEFAULT_DRAW_OPTIONS.height,
    bondLineWidth: options.bondLineWidth ?? DEFAULT_DRAW_OPTIONS.bondLineWidth,
    padding: options.padding ?? DEFAULT_DRAW_OPTIONS.padding,
  };

  // Transparent by default: only draw a background when one is requested.
  const background = toRdkitColor(options.backgroundColour);
  if (background) {
    details.backgroundColour = background;
  } else {
    details.clearBackground = false;
  }

  if (options.legend) details.legend = options.legend;
  if (options.legendFontSize != null) details.legendFontSize = options.legendFontSize;
  if (options.rotate != null && options.rotate !== 0) details.rotate = options.rotate;
  if (options.noAtomLabels) details.noAtomLabels = true;
  if (options.addStereoAnnotation) details.addStereoAnnotation = true;
  if (options.addAtomIndices) details.addAtomIndices = true;
  if (options.addBondIndices) details.addBondIndices = true;
  if (options.explicitMethyl) details.explicitMethyl = true;
  if (options.comicMode) details.comicMode = true; // best-effort; MinimalLib may ignore
  if (options.multipleBondOffset != null) {
    details.multipleBondOffset = options.multipleBondOffset;
  }
  if (options.labelFontSize != null) {
    details.minFontSize = options.labelFontSize;
    details.maxFontSize = options.labelFontSize;
  }

  const symbolColour = toRdkitColor(options.symbolColour);
  if (options.colorScheme === 'monochrome') {
    details.symbolColour = symbolColour ?? [0, 0, 0];
  } else if (symbolColour) {
    details.symbolColour = symbolColour;
  }
  if (options.colorScheme === 'custom' && options.customAtomPalette) {
    const palette: Record<string, unknown> = {};
    for (const [atomicNumber, color] of Object.entries(options.customAtomPalette)) {
      const rgb = toRdkitColor(color);
      if (rgb) palette[atomicNumber] = rgb;
    }
    if (Object.keys(palette).length > 0) {
      // Best-effort: atomColourPalette is part of full MolDrawOptions JSON.
      details.atomColourPalette = palette;
    }
  }

  if (options.highlight?.smarts?.trim()) {
    const { atoms, bonds } = matchSubstructure(rdkit, mol, options.highlight.smarts.trim());
    details.atoms = atoms;
    details.bonds = bonds;
    details.highlightColour =
      toRdkitColor(options.highlight.color) ??
      toRdkitColor(options.highlightColour) ??
      DEFAULT_HIGHLIGHT_COLOR;
  } else if (options.highlightColour) {
    const rgb = toRdkitColor(options.highlightColour);
    if (rgb) details.highlightColour = rgb;
  }

  if (options.extraRDKitOptions) {
    Object.assign(details, options.extraRDKitOptions);
  }
  return details;
}

function matchSubstructure(
  rdkit: RDKitModule,
  mol: JSMol,
  smarts: string,
): { atoms: number[]; bonds: number[] } {
  let qmol: JSMol | null = null;
  try {
    try {
      qmol = rdkit.get_qmol(smarts);
    } catch (cause) {
      throw new MolstructError('INVALID_SMARTS', `Invalid SMARTS pattern: ${smarts}`, cause);
    }
    if (!qmol || !qmol.is_valid()) {
      throw new MolstructError('INVALID_SMARTS', `Invalid SMARTS pattern: ${smarts}`);
    }
    let raw: string;
    try {
      raw = mol.get_substruct_matches(qmol);
    } catch {
      raw = mol.get_substruct_match(qmol);
    }
    const atoms = new Set<number>();
    const bonds = new Set<number>();
    let parsed: unknown;
    try {
      parsed = JSON.parse(raw || '[]');
    } catch {
      parsed = [];
    }
    const matches = Array.isArray(parsed) ? parsed : [parsed];
    for (const match of matches) {
      if (match && typeof match === 'object') {
        const m = match as { atoms?: number[]; bonds?: number[] };
        m.atoms?.forEach((a) => atoms.add(a));
        m.bonds?.forEach((b) => bonds.add(b));
      }
    }
    return { atoms: [...atoms], bonds: [...bonds] };
  } finally {
    qmol?.delete();
  }
}
