#!/usr/bin/env node
/**
 * Dev-only test of the headless renderMoleculeSvg API and skeletal gap-fill,
 * with a mocked PubChem network. Names are generic placeholders.
 */
const requests = [];
function jsonResponse(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json' },
  });
}
globalThis.fetch = async (url) => {
  const u = String(url);
  requests.push(u);
  if (u.includes('/rest/autocomplete/compound/')) {
    return jsonResponse({ dictionary_terms: { compound: [] }, total: 0 });
  }
  if (u.includes('/rest/pug/compound/name/')) {
    const nm = decodeURIComponent(u.match(/compound\/name\/([^/]+)\//)[1]).toLowerCase();
    if (nm === 'placeholderol') {
      return jsonResponse({
        PropertyTable: {
          Properties: [
            { CID: 777, SMILES: 'CC(=O)Oc1ccccc1C(=O)O', ConnectivitySMILES: 'CC(=O)Oc1ccccc1C(=O)O' },
          ],
        },
      });
    }
    return jsonResponse({ Fault: { Code: 'PUGREST.NotFound' } }, 404);
  }
  return new Response('not found', { status: 404 });
};

const {
  renderMoleculeSvg,
  applySvgOverrides,
  fillLabelGaps,
  stripText,
  MolstructError,
} = await import('../dist/index.es.js');

let failures = 0;
function check(label, cond) {
  if (cond) console.log(`  ok  ${label}`);
  else {
    failures++;
    console.error(`FAIL  ${label}`);
  }
}

// 1. Render by name → SVG + metadata; skeletal default (no text).
const byName = await renderMoleculeSvg('placeholderol', { width: 300, height: 240 });
check('renders SVG by name', byName.svg.includes('<svg'));
check('returns smiles', byName.smiles === 'CC(=O)Oc1ccccc1C(=O)O');
check('returns CID', byName.cid === 777);
check('source is pubchem', byName.source === 'pubchem');
check('default is skeletal (no <text>)', !byName.svg.includes('<text'));
check('default keeps element colors (heteroatom bond tinted)', /stroke="rgb\((?!0,\s*0,\s*0)/.test(byName.svg));
check('injects accessible <title>', byName.svg.includes('<title>'));

// 2. Render by SMILES (no network); labels on when requested.
const reqBefore = requests.length;
const bySmiles = await renderMoleculeSvg('', {
  smiles: 'CCO',
  hideText: false,
  width: 200,
  height: 160,
});
check('smiles bypass makes no network request', requests.length === reqBefore);
check('source is direct', bySmiles.source === 'direct');
check('labels shown when hideText:false', bySmiles.svg.includes('<text'));

// 3. Empty input throws.
try {
  await renderMoleculeSvg('');
  check('empty query throws', false);
} catch (e) {
  check('empty query throws BAD_REQUEST', e instanceof MolstructError && e.code === 'BAD_REQUEST');
}

// 4. Unknown name throws NOT_FOUND.
try {
  await renderMoleculeSvg('zzqq-nope');
  check('unknown name throws', false);
} catch (e) {
  check('unknown name throws NOT_FOUND', e instanceof MolstructError && e.code === 'NOT_FOUND');
}

// 5. Gap-fill snaps bond endpoints onto former label centres.
const labeled =
  '<svg xmlns="http://www.w3.org/2000/svg" width="120" height="100">' +
  '<text x="50.00" y="40.00" font-size="14" fill="rgb(255,0,0)">O</text>' +
  '<line x1="62.00" y1="40.00" x2="90.00" y2="40.00" stroke="rgb(0,0,0)" stroke-width="2"/>' +
  '</svg>';
const filled = fillLabelGaps(labeled);
const endpoint = filled.match(/x1="([\d.]+)"/);
const labelCenterX = 50 + 14 * 0.3; // 54.2
check(
  'gap-fill moves the near endpoint toward the label centre',
  endpoint != null && Math.abs(parseFloat(endpoint[1]) - labelCenterX) < 0.5,
);
check('gap-fill leaves the far endpoint alone', filled.includes('x2="90.00"'));
check('stripText removes the label', !stripText(filled).includes('<text'));
check(
  'stripText keeps the bond line',
  (stripText(filled).match(/<line/g) || []).length === 1,
);

// 6. Far-away labels are not snapped (no false positives).
const farLabel =
  '<svg xmlns="http://www.w3.org/2000/svg">' +
  '<text x="10.00" y="10.00" font-size="14">O</text>' +
  '<line x1="200.00" y1="200.00" x2="240.00" y2="200.00" stroke="#000"/>' +
  '</svg>';
check('distant bond endpoints are not snapped', fillLabelGaps(farLabel).includes('x1="200.00"'));

// 7. Stroke override also fills solid stereo wedges (so they are fully
//    colored, not just outlined), across both engine dialects.
const oclWedge =
  '<svg xmlns="http://www.w3.org/2000/svg">' +
  '<rect width="100" height="100" fill="#ffffff" stroke="none"/>' +
  '<line x1="0" y1="0" x2="10" y2="10" stroke="rgb(0,0,0)"/>' +
  '<polygon points="1,2 3,4 5,6" fill="rgb(160,0,0)" stroke="rgb(160,0,0)"/>' +
  '</svg>';
const oclOut = applySvgOverrides(oclWedge, { strokeColour: '#cc00ff' });
check('OCL wedge polygon fill recolored', oclOut.includes('<polygon points="1,2 3,4 5,6" fill="#cc00ff"'));
check('OCL wedge polygon stroke recolored', /<polygon[^>]*stroke="#cc00ff"/.test(oclOut));
check('background rect fill is NOT recolored', oclOut.includes('<rect width="100" height="100" fill="#ffffff"'));

const rdkitWedge =
  "<svg xmlns='http://www.w3.org/2000/svg'>" +
  "<path class='bond-1 atom-1 atom-2' d='M 1,1 L 2,2' style='fill:#000000;fill-rule:evenodd;stroke:#000000;stroke-width:2.0px' />" +
  "<path class='bond-0 atom-0 atom-1' d='M 0,0 L 1,1' style='fill:none;stroke:#000000;stroke-width:2.0px' />" +
  '</svg>';
const rdkitOut = applySvgOverrides(rdkitWedge, { strokeColour: '#0000ee' });
check('RDKit solid-wedge fill recolored', rdkitOut.includes('fill:#0000ee'));
check('RDKit normal bond fill:none untouched', rdkitOut.includes('fill:none'));

console.log(
  failures === 0
    ? '\nRender API: all assertions passed.'
    : `\n${failures} API assertion(s) FAILED.`,
);
process.exit(failures === 0 ? 0 : 1);
