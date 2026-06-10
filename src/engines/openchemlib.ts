import { MolstructError } from '../errors';
import type { DrawOptions, RenderEngine } from '../types';
import { injectSvgBackground } from '../utils/svgOverrides';

/**
 * Structural types for the slice of OpenChemLib this engine uses, so the
 * emitted declarations carry no dependency on openchemlib's own types.
 */
interface OCLMoleculeLike {
  toSVG(
    width: number,
    height: number,
    id?: string,
    options?: Record<string, unknown>,
  ): string;
}
interface OCLLike {
  Molecule: { fromSmiles(smiles: string): OCLMoleculeLike };
}

let oclPromise: Promise<OCLLike> | null = null;

function loadOCL(): Promise<OCLLike> {
  if (!oclPromise) {
    oclPromise = import('openchemlib')
      .then((mod) => ((mod as { default?: OCLLike }).default ?? mod) as OCLLike)
      .catch((cause) => {
        oclPromise = null;
        throw new MolstructError(
          'WASM_LOAD',
          'Could not load the OpenChemLib fallback engine. ' +
            'Install the optional "openchemlib" package to use it.',
          cause,
        );
      });
  }
  return oclPromise;
}

/**
 * Pure-JavaScript rendering engine backed by OpenChemLib — no WebAssembly
 * required, so it works where WASM is disabled (e.g. Safari Lockdown Mode).
 *
 * Depiction fidelity is below RDKit and only a subset of DrawOptions applies
 * (width, height, bondLineWidth, stereo annotations); highlights, legends,
 * palettes, and rotation are ignored. `openchemlib` is an optional peer
 * dependency, loaded on first use via dynamic import.
 */
export function createOpenChemLibEngine(): RenderEngine {
  let ocl: OCLLike | null = null;
  return {
    id: 'openchemlib',
    async ready(): Promise<void> {
      if (!ocl) {
        ocl = await loadOCL();
      }
    },
    renderToSvg(smiles: string, options: DrawOptions): string {
      if (!ocl) {
        throw new MolstructError(
          'WASM_LOAD',
          'OpenChemLib engine used before ready() resolved.',
        );
      }
      let mol: OCLMoleculeLike;
      try {
        mol = ocl.Molecule.fromSmiles(smiles);
      } catch (cause) {
        throw new MolstructError(
          'INVALID_SMILES',
          `OpenChemLib could not parse: ${smiles}`,
          cause,
        );
      }
      try {
        let svg = mol.toSVG(options.width ?? 320, options.height ?? 260, undefined, {
          autoCrop: true,
          autoCropMargin: 12,
          strokeWidth: options.bondLineWidth ?? 1,
          suppressChiralText: !options.addStereoAnnotation,
          suppressCIPParity: !options.addStereoAnnotation,
          noStereoProblem: true,
        });
        // OpenChemLib emits a transparent background; honor backgroundColour.
        if (options.backgroundColour != null) {
          svg = injectSvgBackground(svg, options.backgroundColour);
        }
        return svg;
      } catch (cause) {
        throw new MolstructError(
          'RENDER',
          'OpenChemLib failed to render the molecule.',
          cause,
        );
      }
    },
  };
}
