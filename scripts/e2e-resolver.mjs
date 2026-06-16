#!/usr/bin/env node
/**
 * Dev-only test of the smart resolution chain with a mocked network:
 * candidate expansion (parentheticals, Greek letters), autocomplete
 * recovery for abbreviations/typos, resolvedAs reporting, and error paths.
 */
const requests = [];

function jsonResponse(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json' },
  });
}

// Mock PubChem: only the exact name "examplomide" exists; autocomplete is
// prefix-based (like the real service) — it returns names starting with the
// query, and a deliberately UNRELATED hit for the bare abbreviation "emd" to
// exercise the false-positive guard.
globalThis.fetch = async (url) => {
  const u = String(url);
  requests.push(u);
  if (u.includes('/rest/autocomplete/compound/')) {
    const q = decodeURIComponent(u.match(/compound\/([^/]+)\/json/)[1]).toLowerCase();
    let terms = [];
    if ('examplomide'.startsWith(q)) terms = ['Examplomide', 'Examplomide oxide'];
    else if (q === 'emd') terms = ['Examplomide']; // unrelated to "emd" → must be rejected
    return jsonResponse({ dictionary_terms: { compound: terms }, total: terms.length });
  }
  if (u.includes('/rest/pug/compound/name/')) {
    const nm = decodeURIComponent(u.match(/compound\/name\/([^/]+)\//)[1]).toLowerCase();
    if (nm === 'examplomide') {
      return jsonResponse({
        PropertyTable: {
          Properties: [{ CID: 4242, SMILES: 'CCO', ConnectivitySMILES: 'CCO' }],
        },
      });
    }
    return jsonResponse({ Fault: { Code: 'PUGREST.NotFound' } }, 404);
  }
  // CACTUS
  return new Response('not found', { status: 404 });
};

const {
  expandQueryCandidates,
  isRelatedSuggestion,
  resolveWithPubChemThenCactus,
  MolstructError,
} = await import('../dist/index.es.js');

let failures = 0;
function check(label, condition) {
  if (condition) console.log(`  ok  ${label}`);
  else {
    failures++;
    console.error(`FAIL  ${label}`);
  }
}

// 1. Candidate expansion.
const parens = expandQueryCandidates('EMD (Examplomide)');
check('parenthetical: keeps full query first', parens[0] === 'EMD (Examplomide)');
check('parenthetical: longer part preferred', parens[1] === 'Examplomide');
check('parenthetical: abbreviation included', parens.includes('EMD'));

const greek = expandQueryCandidates('β-examplomide');
check('greek letters spelled out', greek.includes('beta-examplomide'));
const greekNum = expandQueryCandidates('Δ9-examplomide');
check('greek + digit gets hyphen variant', greekNum.includes('delta-9-examplomide'));
const dashes = expandQueryCandidates('exa–mplomide');
check('typographic dash normalized', dashes[0] === 'exa-mplomide');

// 2. "ABBR (Full name)" resolves via the parenthetical candidate.
const viaParens = await resolveWithPubChemThenCactus('EMD (Examplomide)');
check('parenthetical query resolves', viaParens.smiles === 'CCO');
check('resolvedAs reports the matched name', viaParens.resolvedAs === 'Examplomide');
check('query preserved on result', viaParens.query === 'EMD (Examplomide)');

// 3. Typo / truncation recovers through prefix autocomplete.
const viaTypo = await resolveWithPubChemThenCactus('examplomid');
check('truncation resolves via autocomplete', viaTypo.resolvedAs === 'Examplomide');

// 4. False-positive guard: a bare unrelated abbreviation is NOT silently
//    resolved to the unrelated suggestion autocomplete returned for it.
check('guard rejects unrelated suggestion', !isRelatedSuggestion('EMD', 'Examplomide'));
check('guard accepts prefix/substring match', isRelatedSuggestion('examplomid', 'Examplomide'));
try {
  await resolveWithPubChemThenCactus('EMD');
  check('unrelated abbreviation does not false-positive', false);
} catch (error) {
  check(
    'unrelated abbreviation does not false-positive',
    error instanceof MolstructError && error.code === 'NOT_FOUND',
  );
}

// 5. Exact match carries no resolvedAs.
const exact = await resolveWithPubChemThenCactus('Examplomide');
check('exact match has no resolvedAs', exact.resolvedAs === undefined);

// 6. Genuinely unknown names still fail with NOT_FOUND.
try {
  await resolveWithPubChemThenCactus('zzqq-unknowable');
  check('unknown name throws', false);
} catch (error) {
  check(
    'unknown name throws MolstructError(NOT_FOUND)',
    error instanceof MolstructError && error.code === 'NOT_FOUND',
  );
}

check('mock network was exercised', requests.length > 6);
console.log(
  failures === 0
    ? '\nResolver chain: all assertions passed.'
    : `\n${failures} resolver assertion(s) FAILED.`,
);
process.exit(failures === 0 ? 0 : 1);
