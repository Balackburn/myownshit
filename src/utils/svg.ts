/** Escapes text for safe inclusion inside XML elements/attributes. */
export function escapeXml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

/**
 * Injects <title>/<desc> accessibility metadata and role="img" into an SVG
 * string produced by RDKit. Returns the input unchanged if no <svg> tag is found.
 */
export function decorateSvg(svg: string, title: string, desc: string): string {
  const match = svg.match(/<svg\b[^>]*>/);
  if (!match) return svg;
  let openTag = match[0];
  if (!/\brole=/.test(openTag)) {
    openTag = openTag.replace(/<svg\b/, '<svg role="img"');
  }
  const meta = `<title>${escapeXml(title)}</title><desc>${escapeXml(desc)}</desc>`;
  return svg.replace(match[0], `${openTag}${meta}`);
}

/** Triggers a client-side download of SVG markup as a .svg file. */
export function downloadSvgFile(svg: string, filename: string): void {
  const safeName = filename.endsWith('.svg') ? filename : `${filename}.svg`;
  const blob = new Blob([svg], { type: 'image/svg+xml;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = safeName;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}

/**
 * Copies text to the clipboard, preferring the async Clipboard API with a
 * hidden-textarea fallback for older/insecure contexts. Returns success.
 */
export async function copyTextToClipboard(text: string): Promise<boolean> {
  if (typeof navigator !== 'undefined' && navigator.clipboard?.writeText) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {
      // fall through to the legacy path
    }
  }
  try {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.setAttribute('readonly', '');
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    const ok = document.execCommand('copy');
    textarea.remove();
    return ok;
  } catch {
    return false;
  }
}
