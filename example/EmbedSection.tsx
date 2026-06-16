import { useEffect, useRef, useState } from 'react';
import { Button, Card } from '@heroui/react';
import type { DrawOptions } from 'react-molstruct';

export interface EmbedSectionProps {
  name: string;
  options: DrawOptions;
}

/** Maps the current name + DrawOptions to embed.html URL query parameters. */
function buildQuery(name: string, options: DrawOptions): string {
  const p = new URLSearchParams();
  if (name.trim()) p.set('name', name.trim());
  if (options.width) p.set('width', String(options.width));
  if (options.height) p.set('height', String(options.height));
  if (options.bondLineWidth != null) p.set('bond', String(options.bondLineWidth));
  if (options.strokeWidthScale != null) p.set('scale', String(options.strokeWidthScale));
  if (options.strokeColour) p.set('stroke', hex(options.strokeColour));
  if (options.textColour) p.set('text', hex(options.textColour));
  if (options.backgroundColour) p.set('bg', hex(options.backgroundColour));
  if (options.roundedStrokes) p.set('rounded', '1');
  if (options.rotate) p.set('rotate', String(options.rotate));
  if (options.hideText === false) p.set('labels', '1');
  if (options.addStereoAnnotation) p.set('stereo', '1');
  return p.toString();
}

function hex(color: string | number[]): string {
  return typeof color === 'string' ? color.replace(/^#/, '') : '';
}

/**
 * Live "Embed & API" panel: renders the current molecule through the actual
 * embed.html iframe API and offers a copy-paste snippet — the exact thing an
 * external wiki would paste.
 */
export function EmbedSection(props: EmbedSectionProps) {
  const base = import.meta.env.BASE_URL;
  const query = buildQuery(props.name, props.options);
  const src = `${location.origin}${base}embed.html?${query}`;
  const width = props.options.width ?? 320;
  const [height, setHeight] = useState((props.options.height ?? 260) + 16);
  const [copied, setCopied] = useState(false);
  const frameRef = useRef<HTMLIFrameElement | null>(null);

  // Resize the iframe to the height the embed reports via postMessage.
  useEffect(() => {
    const onMessage = (event: MessageEvent) => {
      const data = event.data as { type?: string; height?: number };
      if (
        data?.type === 'molstruct:size' &&
        typeof data.height === 'number' &&
        event.source === frameRef.current?.contentWindow
      ) {
        setHeight(Math.max(120, data.height));
      }
    };
    window.addEventListener('message', onMessage);
    return () => window.removeEventListener('message', onMessage);
  }, []);

  const snippet = `<iframe\n  src="${src}"\n  style="border:0;width:${width}px;height:${height}px"\n  loading="lazy"\n  title="${props.name || 'molecule'} structure"\n></iframe>`;

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(snippet);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch {
      setCopied(false);
    }
  };

  return (
    <Card className="p-4">
      <div className="mb-3 flex items-center justify-between gap-2">
        <span className="font-mono text-[11px] tracking-[0.16em] uppercase text-muted">
          Embed &amp; API
        </span>
        <Button size="sm" variant="primary" onPress={copy}>
          {copied ? 'Copied' : 'Copy iframe'}
        </Button>
      </div>
      <p className="mb-3 max-w-[65ch] text-sm text-muted">
        Paste this on any site — no build step, no API key. It tracks the
        options you set above. Full parameter reference in{' '}
        <a
          className="text-accent underline"
          href="https://github.com/Balackburn/myownshit/blob/main/docs/API.md"
          target="_blank"
          rel="noreferrer"
        >
          docs/API.md
        </a>
        .
      </p>
      <div className="flex flex-wrap items-start gap-4">
        <iframe
          ref={frameRef}
          src={src}
          title="Live embed preview"
          loading="lazy"
          className="rounded-lg border border-default"
          style={{ width, height }}
        />
        <pre className="min-w-60 flex-1 overflow-auto rounded-lg bg-surface p-3 font-mono text-xs leading-relaxed break-all whitespace-pre-wrap">
          <code>{snippet}</code>
        </pre>
      </div>
    </Card>
  );
}
