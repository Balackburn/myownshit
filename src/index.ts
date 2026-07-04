// react-molstruct — zero-backend molecule name → 2D SVG rendering for React.

// Headless render API (no React required)
export { renderMoleculeSvg } from './api';
export type { RenderMoleculeOptions, RenderMoleculeResult } from './api';

// Components
export { MoleculeViewer, DEFAULT_VIEWER_OPTIONS } from './components/MoleculeViewer';
export { MoleculeImage } from './components/MoleculeImage';
export type { MoleculeImageProps } from './components/MoleculeImage';
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
export { loadRDKit, DEFAULT_WASM_PATH, isWebAssemblyAvailable } from './rdkit/loader';
export { drawMoleculeToSvg, isValidSmiles, DEFAULT_DRAW_OPTIONS } from './rdkit/draw';
export { createRDKitEngine } from './rdkit/engine';
export type { RDKitModule, JSMol } from './rdkit/types';

// Fallback engine (pure JS, no WebAssembly; requires optional peer "openchemlib")
export { createOpenChemLibEngine } from './engines/openchemlib';
// Auto engine: RDKit when available, OpenChemLib otherwise.
export { createAutoEngine } from './engines/auto';

// Resolvers
export {
  resolveWithPubChem,
  resolveWithCactus,
  resolveWithPubChemThenCactus,
  fetchNameSuggestions,
  expandQueryCandidates,
  isRelatedSuggestion,
  getResolver,
  clearStructureCache,
} from './resolvers';

// Errors
export { MolstructError, isMolstructError, describeError } from './errors';
export type { MolstructErrorCode } from './errors';

// Style presets
export { STYLE_PRESETS } from './presets';
export type { StylePreset } from './presets';

// Utilities
export { hexToRgb01, toHexColor, toRdkitColor } from './utils/color';
export {
  decorateSvg,
  downloadSvgFile,
  downloadPngFile,
  svgToPngBlob,
  copyTextToClipboard,
  escapeXml,
} from './utils/svg';
export {
  applySvgOverrides,
  injectSvgBackground,
  colorToCss,
  stripText,
  fillLabelGaps,
  tintBondsToLabels,
} from './utils/svgOverrides';
export type { SvgOverrideOptions } from './utils/svgOverrides';

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
