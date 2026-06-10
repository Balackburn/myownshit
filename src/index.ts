// react-molstruct — zero-backend molecule name → 2D SVG rendering for React.

// Components
export { MoleculeViewer } from './components/MoleculeViewer';
export { MoleculeControls } from './components/MoleculeControls';
export type { MoleculeControlsProps } from './components/MoleculeControls';
export { MoleculeErrorBoundary } from './components/ErrorBoundary';
export type { MoleculeErrorBoundaryProps } from './components/ErrorBoundary';

// Hooks
export { useRdkit } from './hooks/useRdkit';
export type { UseRdkitResult } from './hooks/useRdkit';
export { useResolvedStructure } from './hooks/useResolvedStructure';
export type {
  UseResolvedStructureArgs,
  UseResolvedStructureResult,
} from './hooks/useResolvedStructure';
export { useDebounce } from './hooks/useDebounce';

// RDKit engine layer
export { loadRDKit, DEFAULT_WASM_PATH } from './rdkit/loader';
export { drawMoleculeToSvg, isValidSmiles, DEFAULT_DRAW_OPTIONS } from './rdkit/draw';
export { createRDKitEngine } from './rdkit/engine';
export type { RDKitModule, JSMol } from './rdkit/types';

// Resolvers
export {
  resolveWithPubChem,
  resolveWithCactus,
  resolveWithPubChemThenCactus,
  getResolver,
  clearStructureCache,
} from './resolvers';

// Errors
export { MolstructError, isMolstructError, describeError } from './errors';
export type { MolstructErrorCode } from './errors';

// Utilities
export { hexToRgb01, toHexColor, toRdkitColor } from './utils/color';
export {
  decorateSvg,
  downloadSvgFile,
  copyTextToClipboard,
  escapeXml,
} from './utils/svg';

// Types
export type {
  ColorInput,
  ColorScheme,
  DrawOptions,
  HighlightSpec,
  MoleculeViewerHandle,
  MoleculeViewerProps,
  RenderEngine,
  ResolvedStructure,
  ResolverChoice,
  ResolverFn,
  RGBColor,
  StructureSource,
} from './types';
