import { Component, type ErrorInfo, type ReactNode } from 'react';

export interface MoleculeErrorBoundaryProps {
  children: ReactNode;
  /** Static fallback node, or a render function receiving the caught error. */
  fallback?: ReactNode | ((error: Error) => ReactNode);
  /** Notified when a rendering error is caught. */
  onError?: (error: Error, info: ErrorInfo) => void;
}

interface MoleculeErrorBoundaryState {
  error: Error | null;
}

/**
 * Class-based error boundary guarding the molecule renderer. Unexpected
 * render-time exceptions show a compact inline message instead of unmounting
 * the host application.
 */
export class MoleculeErrorBoundary extends Component<
  MoleculeErrorBoundaryProps,
  MoleculeErrorBoundaryState
> {
  state: MoleculeErrorBoundaryState = { error: null };

  static getDerivedStateFromError(error: Error): MoleculeErrorBoundaryState {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    this.props.onError?.(error, info);
  }

  render(): ReactNode {
    const { error } = this.state;
    if (error) {
      const { fallback } = this.props;
      if (typeof fallback === 'function') return fallback(error);
      if (fallback !== undefined) return fallback;
      return (
        <div className="rms-error" role="alert">
          <strong>Structure renderer crashed.</strong>
          <span>{error.message}</span>
        </div>
      );
    }
    return this.props.children;
  }
}
