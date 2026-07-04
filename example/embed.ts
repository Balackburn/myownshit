/**
 * Embeddable molecule renderer. External sites drop an <iframe> pointing here
 * with URL parameters and get a live 2D structure SVG — no build step, no API
 * key, no backend. See docs/API.md for the full parameter reference.
 *
 *   <iframe src="https://.../embed.html?name=aspirin&width=320&stroke=0000ee"
 *           style="border:0;width:320px;height:260px"></iframe>
 */
import {
  renderMoleculeSvg,
  type RenderMoleculeOptions,
} from 'react-molstruct';

const params = new URLSearchParams(location.search);
const mount = document.getElementById('embed')!;

function num(key: string): number | undefined {
  const raw = params.get(key);
  if (raw == null || raw === '') return undefined;
  const value = Number(raw);
  return Number.isFinite(value) ? value : undefined;
}

/** Truthy flag: present and not "0"/"false"/"no". */
function flag(key: string): boolean | undefined {
  if (!params.has(key)) return undefined;
  const raw = (params.get(key) ?? '').toLowerCase();
  return raw !== '0' && raw !== 'false' && raw !== 'no';
}

/** Color: accepts "#rrggbb", "rrggbb", a CSS name, or "none"/"transparent". */
function color(key: string): string | undefined {
  const raw = params.get(key);
  if (raw == null || raw === '') return undefined;
  if (raw === 'none' || raw === 'transparent') return undefined;
  return /^[0-9a-fA-F]{3,8}$/.test(raw) ? `#${raw}` : raw;
}

const name = params.get('name') ?? params.get('q') ?? '';
const smiles = params.get('smiles') ?? undefined;

const options: RenderMoleculeOptions = {
  smiles,
  // Use the site's hosted RDKit assets so the embed matches the website
  // exactly (falls back to the pure-JS engine if they fail to load).
  wasmPath: `${import.meta.env.BASE_URL}rdkit`,
  width: num('width') ?? num('w') ?? 320,
  height: num('height') ?? num('h') ?? 260,
  bondLineWidth: num('bond'),
  strokeWidthScale: num('scale'),
  strokeColour: color('stroke'),
  textColour: color('text'),
  backgroundColour: color('bg'),
  roundedStrokes: flag('rounded'),
  rotate: num('rotate'),
  // Skeletal (no atom labels) by default, with element colors kept. `labels=1`
  // shows atom labels.
  hideText: flag('labels') === undefined ? true : !flag('labels'),
  addStereoAnnotation: flag('stereo') ?? false,
};

/** Reports the rendered height so parents can size the iframe responsively. */
function reportSize(): void {
  const svg = mount.querySelector('svg');
  const height = Math.ceil(
    svg?.getBoundingClientRect().height || mount.scrollHeight || 0,
  );
  if (height > 0) {
    parent.postMessage({ type: 'molstruct:size', height: height + 16 }, '*');
  }
}

renderMoleculeSvg(name, options)
  .then((result) => {
    mount.innerHTML = result.svg;
    document.title = `react-molstruct — ${name || result.smiles}`;
    reportSize();
  })
  .catch((error: unknown) => {
    const message =
      error && typeof error === 'object' && 'message' in error
        ? String((error as { message: unknown }).message)
        : 'Could not render molecule.';
    mount.innerHTML = `<span class="embed-msg">${message.replace(/[<>&]/g, '')}</span>`;
    reportSize();
  });
