/**
 * Generates ordered lookup candidates from a raw molecule query so that
 * common ways people write names still resolve:
 *
 * - "ASA (acetylsalicylic acid)" → tries the full string, then the
 *   parenthetical parts (longer part first — usually the full name).
 * - Greek letters: "β-carotene" → "beta-carotene"; "Δ9..." also gets a
 *   hyphenated "delta-9..." variant.
 * - Typographic dashes (– —) are normalized to "-".
 */
const GREEK: Record<string, string> = {
  α: 'alpha',
  β: 'beta',
  γ: 'gamma',
  δ: 'delta',
  ε: 'epsilon',
  ω: 'omega',
  Α: 'alpha',
  Β: 'beta',
  Γ: 'gamma',
  Δ: 'delta',
  Ε: 'epsilon',
  Ω: 'omega',
};

const GREEK_PATTERN = /[αβγδεωΑΒΓΔΕΩ]/;

export function expandQueryCandidates(raw: string): string[] {
  const out: string[] = [];
  const push = (value: string | undefined) => {
    const clean = value?.replace(/\s+/g, ' ').trim();
    if (clean && !out.some((c) => c.toLowerCase() === clean.toLowerCase())) {
      out.push(clean);
    }
  };

  const seeds: string[] = [];
  const base = raw.replace(/[–—]/g, '-');
  seeds.push(base);

  if (GREEK_PATTERN.test(base)) {
    const spelled = base.replace(/[αβγδεωΑΒΓΔΕΩ]/g, (ch) => GREEK[ch] ?? ch);
    seeds.push(spelled);
    // "delta9" style also commonly appears hyphenated as "delta-9".
    const hyphenated = spelled.replace(
      /(alpha|beta|gamma|delta|epsilon|omega)(\d)/gi,
      '$1-$2',
    );
    if (hyphenated !== spelled) seeds.push(hyphenated);
  }

  for (const seed of seeds) {
    push(seed);
    const paren = seed.match(/^(.*?)\(([^)]+)\)(.*)$/);
    if (paren) {
      const outside = `${paren[1]} ${paren[3]}`.replace(/\s+/g, ' ').trim();
      const inside = paren[2].trim();
      // The longer part is usually the spelled-out name — try it first.
      if (inside.length >= outside.length) {
        push(inside);
        push(outside);
      } else {
        push(outside);
        push(inside);
      }
    }
  }
  return out.slice(0, 5);
}
