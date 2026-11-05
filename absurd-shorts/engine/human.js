// Parametric low-poly human ("Le Mec") with a rigid puppet rig.
// Proportions measured from the source frames (figure ≈ 1.95 u tall):
//   head  = tall narrow slab 0.27w × 0.50h × 0.22d, slight trapezoid, ink outline
//   neck  = long skin box 0.10w × 0.16h
//   torso = boxy jacket, shoulders 0.50w tapering to 0.36w at the waist
//   legs  = very long (≈ 0.98 u), thin, boxy black shoes
// Every part is a box so the rig is a hierarchy of pivots (no skinning) — exactly
// the stiff, toy-like motion of the original.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl, addOutline, rng } from './style.js';
import { faceTexture, sideTexture } from './face.js';
import { atlasImage, atlasBox, atlasUV, atlasMaterial, atlasFaceTexture, atlasSideTexture, atlasBackTexture, R as AR, allFaces } from './atlas.js';

export const OUTFITS = ['suit', 'cop', 'swat', 'judge', 'chef', 'doctor', 'worker', 'tourist', 'prisoner', 'pajamas', 'vampire', 'tracksuit', 'waiter', 'scientist', 'farmer', 'firefighter', 'skirtsuit', 'mao'];
export const HAIRS = ['crew', 'bald', 'combover', 'mohawk', 'curly', 'long', 'bun', 'slick', 'buzz', 'afro', 'receding', 'spiky'];
export const HATS = ['none', 'copcap', 'swatcap', 'hardhat', 'toque', 'wig', 'beanie', 'fedora', 'cowboy', 'firehelmet', 'party', 'crown', 'maocap', 'beekeeper'];
export const FACIALS = ['stubble', 'none', 'mustache', 'beard'];

// Named presets — the cast. `lemec` is the protagonist archetype.
export const PRESETS = {
  lemec:     { outfit: 'suit', suit: P.suitNavy, tie: P.tieRed, lapel: P.lapelTeal, hair: 'crew', facial: 'stubble', atlas: 'lemec' }, // painted atlas (assets/lemec_atlas.webp)
  lemec_charcoal: { outfit: 'suit', suit: P.suitCharcoal, tie: P.tieRed, lapel: P.lapelTeal, hair: 'crew', facial: 'stubble' },
  lemec_brown:    { outfit: 'suit', suit: P.suitBrown, tie: P.yellow, lapel: P.creamDark, hair: 'slick', facial: 'stubble' },
  lemec_beige:    { outfit: 'suit', suit: P.suitBeige, tie: P.navy, lapel: P.salmon, hair: 'combover', facial: 'mustache' },
  lemec_glasses:  { outfit: 'suit', suit: P.suitNavy, tie: P.teal, lapel: P.lapelTeal, hair: 'receding', facial: 'stubble', glasses: true },
  boss:      { outfit: 'suit', suit: P.suitCharcoal, tie: P.yellow, lapel: P.grey, hair: 'bald', facial: 'beard', build: { belly: 0.12 } },
  cop:       { outfit: 'cop', hat: 'copcap', hair: 'curly', facial: 'cop' },
  cop2:      { outfit: 'cop', hat: 'copcap', hair: 'crew', facial: 'stubble', build: { belly: 0.08 } },
  swat:      { outfit: 'swat', hat: 'swatcap', hair: 'buzz', facial: 'none' },
  judge:     { outfit: 'judge', hat: 'wig', hair: 'bald', facial: 'none', glasses: true },
  chef:      { outfit: 'chef', hat: 'toque', hair: 'crew', facial: 'mustache' },
  doctor:    { outfit: 'doctor', hair: 'receding', facial: 'none', glasses: true },
  worker:    { outfit: 'worker', hat: 'hardhat', hair: 'buzz', facial: 'beard' },
  tourist:   { outfit: 'tourist', hat: 'fedora', hair: 'bald', facial: 'mustache', build: { belly: 0.14 } },
  prisoner:  { outfit: 'prisoner', hair: 'buzz', facial: 'stubble' },
  pyjama:    { outfit: 'pajamas', hair: 'spiky', facial: 'stubble' },
  vampire:   { outfit: 'vampire', hair: 'bald', facial: 'none', skin: '#C9C7BE', ears: 'pointy', claws: true, build: { height: 1.05, width: 0.85 } },
  sportif:   { outfit: 'tracksuit', hair: 'mohawk', facial: 'none' },
  serveur:   { outfit: 'waiter', hair: 'slick', facial: 'mustache' },
  savant:    { outfit: 'scientist', hair: 'afro', hairColor: '#DADADA', facial: 'none', glasses: true },
  fermier:   { outfit: 'farmer', hat: 'cowboy', hair: 'crew', facial: 'beard' },
  pompier:   { outfit: 'firefighter', hat: 'firehelmet', hair: 'crew', facial: 'mustache' },
  fringant:  { outfit: 'suit', suit: '#E1C25A', tie: '#3A3D44', lapel: '#E1C25A', hair: 'buzz', facial: 'none', glasses: true, skin: '#7A5034', symmetricLapels: true }, // fictional Gus-Fring-style boss (yellow shirt, glasses)
  madame:    { outfit: 'skirtsuit', suit: P.red, lapel: P.cream, hair: 'bun', facial: 'none', lipstick: true, skin: P.skinPale },
  mamie:     { outfit: 'skirtsuit', suit: P.tealLight, lapel: P.cream, hair: 'curly', hairColor: '#D8D8D8', facial: 'none', glasses: true, build: { height: 0.9 } },
  gamin:     { outfit: 'tracksuit', hair: 'spiky', facial: 'none', build: { height: 0.62, width: 0.85, headScale: 1.15 } },
  // autumn-2026 news series (satire of public images; generic low-poly designs, no caricature)
  footballeur: { outfit: 'mao', hair: 'buzz', facial: 'none', skin: '#5E3F2C' },           // "Mbappé en Mao" meme: grey-green tunic, no tie
  politique:   { outfit: 'suit', suit: '#2B3A55', tie: '#1F2A3D', lapel: '#2B3A55', hair: 'slick', hairColor: '#2A2420', facial: 'none', build: { height: 1.04, width: 0.94 } },
  infiltre:    { outfit: 'tracksuit', suit: '#55595F', hat: 'beanie', hair: 'receding', hairColor: '#8A8A86', facial: 'mustache' }, // 52-year-old cop in a hoodie
  lyceen:      { outfit: 'tracksuit', hair: 'spiky', facial: 'none', build: { height: 0.9, width: 0.9, headScale: 1.08 } },
  lyceenne:    { outfit: 'tracksuit', suit: '#C9729A', hair: 'bun', facial: 'none', lipstick: true, skin: '#C8955F', build: { height: 0.88, width: 0.88, headScale: 1.08 } },
  proviseur:   { outfit: 'suit', suit: '#5C4330', tie: '#C8372D', lapel: '#5C4330', hair: 'bald', facial: 'mustache', glasses: true, build: { belly: 0.1 } },
  commissaire: { outfit: 'suit', suit: '#7A6448', tie: '#3A3D44', lapel: '#6B573E', hat: 'fedora', hair: 'receding', facial: 'mustache', build: { belly: 0.08 } },
  // "Le resto chinois": the restaurant owner today and as a young man under Mao, Mao-era police, the black-market dealer,
  // patriotic netizens, party officials, the man himself in a tunic. Generic faces; clothes carry the period.
  restaurateur:    { outfit: 'waiter', tie: '#B5302A', hair: 'slick', hairColor: '#17161A', facial: 'none', skin: '#E0B48A', build: { height: 0.97 } },
  restaurateurMao: { outfit: 'mao', suit: '#4A5C70', pants: '#4A5C70', lapel: '#3E4E60', hat: 'maocap', hatColor: '#4A5C70', hair: 'slick', hairColor: '#17161A', facial: 'none', skin: '#E0B48A', build: { height: 0.97 } },
  policeMao:       { outfit: 'mao', suit: '#5C6B3A', pants: '#4A5730', lapel: '#4E5C32', collarTabs: true, hat: 'maocap', hatColor: '#5C6B3A', hatStar: true, hair: 'buzz', hairColor: '#17161A', facial: 'none', skin: '#D9AA80' },
  dealer:          { outfit: 'mao', suit: '#3A3A40', pants: '#2A2A30', lapel: '#2A2A30', hat: 'maocap', hatColor: '#2A2A30', hair: 'slick', hairColor: '#17161A', facial: 'mustache', glasses: true, skin: '#D9AA80' },
  internaute:      { outfit: 'tracksuit', suit: '#B5302A', hair: 'spiky', hairColor: '#17161A', facial: 'none', skin: '#E0B48A' },
  internaute2:     { outfit: 'tracksuit', suit: '#E0B020', hair: 'bun', hairColor: '#17161A', facial: 'none', lipstick: true, skin: '#E8C09A', build: { height: 0.92, width: 0.9 } },
  officiel:        { outfit: 'mao', suit: '#3A3D44', pants: '#3A3D44', lapel: '#2E3036', hair: 'slick', hairColor: '#17161A', facial: 'none', glasses: true, skin: '#D9AA80', build: { belly: 0.06 } },
  mecMao:          { outfit: 'mao', suit: '#5B6150', pants: '#5B6150', lapel: '#4A5040', hair: 'crew', facial: 'stubble', atlas: 'lemec', atlasBody: false },
  // "Le looksmaxing": the TikTok guru (fictional), the date, a TV journalist, the man's looksmaxing stages (inflated, orange),
  // how he sees himself, Glucksmann scared / perfect / deflated (satire of the "no charisma" public image), extras
  clavicule:   { outfit: 'tracksuit', suit: '#1E1E22', pants: '#1E1E22', hair: 'slick', hairColor: '#2A2420', facial: 'none', glasses: true, skin: '#C98A5A', build: { height: 1.05, width: 1.45, headScale: 0.82 } },
  femme:       { outfit: 'skirtsuit', suit: '#5E8C7A', lapel: '#F2EDE4', hair: 'long', hairColor: '#5A3A28', facial: 'none', lipstick: true, skin: '#E8C09A', build: { height: 0.94, width: 0.9 } },
  journaliste: { outfit: 'skirtsuit', suit: '#2E4563', lapel: '#F2EDE4', hair: 'bun', hairColor: '#3A2A20', facial: 'none', lipstick: true, glasses: true, skin: '#E8C09A', build: { height: 0.95, width: 0.9 } },
  mecGonfle:   { outfit: 'suit', suit: P.suitNavy, tie: P.tieRed, lapel: P.lapelTeal, hair: 'crew', facial: 'stubble', atlas: 'lemec', build: { width: 1.6, belly: 0.22, headScale: 0.86 } },
  mecOrange:   { outfit: 'suit', suit: P.suitNavy, tie: P.tieRed, lapel: P.lapelTeal, hair: 'crew', facial: 'stubble', atlas: 'lemec', tint: '#FF9A55', build: { width: 1.6, belly: 0.22, headScale: 0.86 } },
  mecMonstre:  { outfit: 'suit', suit: P.suitNavy, tie: P.tieRed, lapel: P.lapelTeal, hair: 'crew', facial: 'stubble', atlas: 'lemec', tint: '#FF9A55', build: { width: 1.95, belly: 0.14, headScale: 0.8 } },
  mecBeau:     { outfit: 'suit', suit: P.suitNavy, tie: P.tieRed, lapel: P.lapelTeal, hair: 'crew', facial: 'stubble', atlas: 'lemec', build: { height: 1.07, width: 1.18, headScale: 0.95 } },
  glucksPeur:  { outfit: 'suit', suit: '#2B3A55', tie: '#1F2A3D', lapel: '#2B3A55', hair: 'slick', hairColor: '#2A2420', facial: 'none', build: { height: 0.8, width: 0.8, headScale: 1.18 } },
  glucksBeau:  { outfit: 'suit', suit: '#2B3A55', tie: '#B5302A', lapel: '#2B3A55', hair: 'slick', hairColor: '#17161A', facial: 'none', build: { height: 1.13, width: 1.32, headScale: 0.9 } },
  glucksMou:   { outfit: 'suit', suit: '#2B3A55', tie: '#1F2A3D', lapel: '#2B3A55', hair: 'slick', hairColor: '#2A2420', facial: 'none', build: { height: 0.78, width: 0.76, belly: 0.06, headScale: 1.2 } },
  apiculteur:  { outfit: 'doctor', suit: '#F2EDE4', pants: '#F2EDE4', hat: 'beekeeper', hair: 'crew', facial: 'beard', beardColor: '#6A4A2A', skin: '#E0B48A' },
  avocat:      { outfit: 'judge', hat: 'none', hair: 'slick', hairColor: '#3A3A40', facial: 'none', glasses: true },
  prefet:      { outfit: 'suit', suit: '#1E2E44', tie: '#B5302A', lapel: '#1E2E44', hair: 'receding', hairColor: '#8A8A86', facial: 'mustache', glasses: true, build: { belly: 0.08 } },
  mecPrisonnier: { outfit: 'prisoner', hair: 'crew', facial: 'stubble', atlas: 'lemec', atlasBody: false },
  mecPyjama:   { outfit: 'pajamas', hair: 'crew', facial: 'stubble', atlas: 'lemec', atlasBody: false },
  carabiniere: { outfit: 'cop', suit: '#1B1C24', pants: '#1B1C24', tie: '#1B1C24', lapel: '#1B1C24', shirt: '#F2F2EE', cuff: '#1B1C24', hat: 'copcap', hatColor: '#1B1C24', hatBand: '#C8322A', sash: '#F2F2EE', hair: 'slick', hairColor: '#2A2420', facial: 'mustache', skin: '#E0B48A' },
  looksmaxeur: { outfit: 'tracksuit', suit: '#2A2A30', pants: '#2A2A30', hair: 'buzz', facial: 'none', skin: '#E8935A', build: { width: 1.4, headScale: 0.86 } },
};

const OUTFIT_COLORS = {
  suit:        { jacket: P.suitNavy, shirt: P.shirt, pants: P.suitNavy, shoes: P.black, tie: P.tieRed, lapel: P.lapelTeal, cuff: P.white },
  cop:         { jacket: P.copBlue, shirt: P.copBlue, pants: P.copBlueDark, shoes: P.black, tie: P.copBlueDark, lapel: P.copBlueDark, cuff: P.copBlue },
  swat:        { jacket: P.swat, shirt: P.swat, pants: P.swat, shoes: P.black, tie: null, lapel: null, cuff: P.swat },
  judge:       { jacket: P.black, shirt: P.white, pants: P.black, shoes: P.black, tie: P.white, lapel: P.black, cuff: P.black },
  chef:        { jacket: P.white, shirt: P.white, pants: '#3B3B3B', shoes: P.black, tie: P.red, lapel: P.white, cuff: P.white },
  doctor:      { jacket: P.white, shirt: P.tealPale, pants: P.tealPale, shoes: P.white, tie: P.navy, lapel: P.white, cuff: P.white },
  worker:      { jacket: '#E07A2E', shirt: '#4B6A8C', pants: '#4B6A8C', shoes: P.woodDark, tie: null, lapel: P.yellow, cuff: '#E07A2E' },
  tourist:     { jacket: '#E8A33C', shirt: '#E8A33C', pants: P.suitBeige, shoes: P.wood, tie: null, lapel: P.pink, cuff: P.skin },
  prisoner:    { jacket: '#E07A2E', shirt: '#E07A2E', pants: '#E07A2E', shoes: P.white, tie: null, lapel: null, cuff: '#E07A2E' },
  pajamas:     { jacket: '#9DB7D9', shirt: '#9DB7D9', pants: '#9DB7D9', shoes: P.red, tie: null, lapel: P.white, cuff: '#9DB7D9' },
  vampire:     { jacket: '#111216', shirt: '#111216', pants: '#111216', shoes: P.black, tie: null, lapel: '#25262C', cuff: '#111216' },
  tracksuit:   { jacket: P.teal, shirt: P.white, pants: P.teal, shoes: P.white, tie: null, lapel: P.white, cuff: P.white },
  waiter:      { jacket: P.black, shirt: P.white, pants: P.black, shoes: P.black, tie: P.black, lapel: P.black, cuff: P.white },
  scientist:   { jacket: P.white, shirt: P.salmon, pants: P.greyDark, shoes: P.black, tie: P.navy, lapel: P.white, cuff: P.white },
  farmer:      { jacket: '#5A7FA6', shirt: P.red, pants: '#5A7FA6', shoes: P.woodDark, tie: null, lapel: '#5A7FA6', cuff: P.red },
  firefighter: { jacket: '#D9A23A', shirt: '#D9A23A', pants: '#D9A23A', shoes: P.black, tie: null, lapel: P.grey, cuff: P.grey },
  skirtsuit:   { jacket: P.red, shirt: P.shirt, pants: null, shoes: P.black, tie: null, lapel: P.cream, cuff: P.white, skirt: true },
  mao:         { jacket: '#7C7E68', shirt: '#7C7E68', pants: '#7C7E68', shoes: P.black, tie: null, lapel: '#6A6C58', cuff: '#7C7E68' },
};

export function buildHuman(spec = {}) {
  if (typeof spec === 'string') spec = { preset: spec };
  const preset = PRESETS[spec.preset || 'lemec'] || {};
  const o = { skin: P.skin, hairColor: P.hair, glasses: false, hat: 'none', ears: 'normal', claws: false, seed: 3, ...preset, ...spec };
  const C = { ...OUTFIT_COLORS[o.outfit || 'suit'] };
  if (o.suit) { C.jacket = o.suit; if (C.pants && o.outfit === 'suit') C.pants = o.suit; }
  if (o.tie) C.tie = o.tie; if (o.lapel) C.lapel = o.lapel; if (o.pants) C.pants = o.pants; if (o.shirt) C.shirt = o.shirt; if (o.cuff) C.cuff = o.cuff;
  C.hat = o.hatColor; C.hatStar = !!o.hatStar; C.hatBand = o.hatBand;
  const B = { height: 1, width: 1, belly: 0, headScale: 1.1, headWidth: 1, ...(preset.build || {}), ...(spec.build || {}) };   // headWidth: widens the head box only (the tornado reference head is W/H ~0.48)
  const H = B.height, Wd = B.width;
  // Painted-atlas mode: every part samples its zone of assets/lemec_atlas.webp
  const ATL = o.atlas === 'lemec' && !!atlasImage, ATLB = ATL && o.atlasBody !== false;
  const half = (r, top) => top ? [r[0], r[1], r[2], (r[1] + r[3]) / 2] : [r[0], (r[1] + r[3]) / 2, r[2], r[3]];
  const AT = {
    pelvis: allFaces(AR.jacketSide, { pz: AR.jacketBack, nz: AR.jacketBack }),
    jacket: allFaces(AR.jacketSide, { pz: AR.jacketFront, nz: AR.jacketBack, py: AR.navyBlock2, ny: AR.navyBlock2 }),
    tail: allFaces(AR.jacketSide, { pz: AR.jacketBack, nz: AR.jacketBack }),
    pad: allFaces(AR.navyBlock2), sleeve: allFaces(AR.navyBlock, { px: AR.jacketSide, nx: AR.jacketSide }),
    cuff: allFaces(AR.cuff, { px: AR.cuffSide, nx: AR.cuffSide, ny: AR.cuffEnd }),
    skin: allFaces(AR.skinCap), neck: { px: AR.neckA, nx: AR.neckB, pz: AR.skinCap, nz: AR.neckC, py: AR.skinCap, ny: AR.skinCap },
    thighL: allFaces(AR.legSide, { pz: half(AR.legFrontR, true), nz: half(AR.jacketBack, true) }), shinL: allFaces(AR.legSide, { pz: half(AR.legFrontR, false), nz: half(AR.jacketBack, false) }),
    thighR: allFaces(AR.legSide, { pz: half(AR.legFrontL, true), nz: half(AR.jacketBack, true) }), shinR: allFaces(AR.legSide, { pz: half(AR.legFrontL, false), nz: half(AR.jacketBack, false) }),
    shoe: { py: AR.shoeTop, pz: AR.shoeFront, nz: AR.shoeFront, px: AR.shoeSide, nx: AR.shoeSide, ny: AR.shoeSole },
  };
  // naked gag: every clothed part becomes skin (head keeps its painted/measured face), censor bar added below
  const CLOTHED = ['pelvis', 'jacket', 'tail', 'pad', 'sleeve', 'cuff', 'thighL', 'shinL', 'thighR', 'shinR', 'shoe'];
  const part0 = (kind, w, h, d, color, opts = {}) => o.naked && CLOTHED.includes(kind) ? box(w, h, d, o.skin, opts)
    : ATL && AT[kind] && (ATLB || kind === 'skin' || kind === 'neck') ? atlasBox(w, h, d, AT[kind], opts) : box(w, h, d, color, opts);
  const part = (kind, ...a) => { const m = part0(kind, ...a); if (kind === 'skin' || kind === 'neck') m.userData.skinPart = true; return m; };

  const root = new THREE.Group(); root.name = 'human';
  const J = {}; // joints
  const joint = (name, parent, x, y, z) => { const g = new THREE.Group(); g.name = name; g.position.set(x, y, z); parent.add(g); J[name] = g; return g; };

  const legLen = 0.49 * H, hipY = legLen * 2 + 0.07;
  const hips = joint('hips', root, 0, hipY, 0);
  // pelvis / jacket skirt
  if (!C.skirt) hips.add(part('pelvis', 0.37 * Wd, 0.16, 0.22 + B.belly, C.pants, { pivot: 'top' }));
  const torso = joint('torso', hips, 0, 0, 0);
  const torsoH = 0.62 * H;
  // MEASURED on the originals (V1 18.4 s, V2 6.6 s): shoulders ≈ 37–39 % of the height and ≈ 1.8× the head height,
  // i.e. a wide, square jacket under a narrow head. Jacket 0.46 wide at the waist → 0.65 at the shoulders.
  const jacket = part('jacket', 0.4 * Wd, torsoH, 0.24 + B.belly, C.jacket, { pivot: 'bottom', taper: { x: 1.65, z: 1.05 } }); // V-shape: waist ≈ 0.6 × shoulders
  jacket.name = 'jacket'; torso.add(jacket);
  // jacket tails (the long suit coat)
  if (!o.naked && ['suit', 'judge', 'vampire', 'doctor', 'scientist', 'waiter', 'skirtsuit'].includes(o.outfit)) {
    const tailLen = o.outfit === 'judge' || o.outfit === 'vampire' ? 0.85 * H : o.outfit === 'doctor' || o.outfit === 'scientist' ? 0.45 : 0.1; // shoulder→hem ≈ 31 % of the height (measured)
    const tail = part('tail', 0.4 * Wd, tailLen, 0.25 + B.belly, C.jacket, { pivot: 'top', taper: { x: o.outfit === 'judge' || o.outfit === 'vampire' ? 1.35 : 1, z: 1 } });
    tail.position.y = 0.02; torso.add(tail); J.coatTail = tail;
  }
  if (C.skirt) { const sk = box(0.38 * Wd, 0.42, 0.24, C.jacket, { pivot: 'top', taper: { x: 1.25, z: 1.15 } }); torso.add(sk); }
  const front = 0.121 + B.belly / 2;
  // shirt V + lapels + tie
  if (o.naked) { const bar = box(0.3, 0.16, 0.03, P.black); bar.position.set(0, -0.05, 0.13); hips.add(bar); for (let i = 0; i < 4; i++) { const b = box(0.075, 0.08, 0.032, '#2A2A2E'); b.position.set(-0.11 + i * 0.075, -0.05 + (i % 2 ? 0.04 : -0.04), 0.131); hips.add(b); } }
  else if (ATLB) { /* lapels, shirt, tie, pocket stroke are painted on the atlas front */ }
  else if (C.lapel && !o.naked) {
    const shirtV = new THREE.Mesh(new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-0.17 * Wd, torsoH * 0.99, 0), new THREE.Vector3(0.17 * Wd, torsoH * 0.99, 0), new THREE.Vector3(0, torsoH * 0.28, 0)]), mat(C.shirt, { doubleSide: true }));
    shirtV.geometry.computeVertexNormals(); shirtV.position.z = front + 0.004; torso.add(shirtV);
    // Signature detail (sheet + source): ONE coloured lapel on the character's right (-X),
    // the other lapel in jacket colour with an ink edge, plus a white pocket-square stroke on the left chest.
    for (const s of [-1, 1]) {
      const pts = [new THREE.Vector3(s * 0.135 * Wd, torsoH * 0.99, 0), new THREE.Vector3(s * 0.29 * Wd, torsoH * 0.97, 0), new THREE.Vector3(s * 0.01, torsoH * 0.27, 0)];
      const colour = (s < 0 || o.symmetricLapels) ? C.lapel : C.jacket;
      const lap = new THREE.Mesh(new THREE.BufferGeometry().setFromPoints(pts), mat(colour, { doubleSide: true }));
      lap.geometry.computeVertexNormals(); lap.position.z = front + 0.008; torso.add(lap);
      const edge = new THREE.Line(new THREE.BufferGeometry().setFromPoints([pts[1], pts[2], pts[0]]), new THREE.LineBasicMaterial({ color: '#0D1118' }));
      edge.position.z = front + 0.011; torso.add(edge);
    }
    if (o.outfit === 'suit' || o.outfit === 'skirtsuit') {
      const curve = new THREE.QuadraticBezierCurve3(new THREE.Vector3(0.16 * Wd, torsoH * 0.78, 0), new THREE.Vector3(0.18 * Wd, torsoH * 0.66, 0), new THREE.Vector3(0.17 * Wd, torsoH * 0.55, 0));
      const pocket = new THREE.Mesh(new THREE.TubeGeometry(curve, 8, 0.004, 4), mat('#F3EEE4', { noGrain: true }));
      pocket.position.z = front + 0.01; torso.add(pocket);
    }
  } else {
    const chest = box(0.2, 0.2, 0.01, C.shirt); chest.position.set(0, torsoH * 0.82, front); torso.add(chest);
  }
  if (C.tie && !ATLB && !o.naked) { const tie = box(0.042, torsoH * 0.62, 0.012, C.tie, { taper: { x: 1.45, z: 1 }, taperAxis: 'y' }); tie.rotation.z = Math.PI; tie.position.set(0, torsoH * 0.66, front + 0.014); torso.add(tie); }
  if (o.bib && !o.naked) for (const sd of [1, -1]) { const c = document.createElement('canvas'); c.width = 128; c.height = 96; const x = c.getContext('2d'); x.fillStyle = '#FFFFFF'; x.fillRect(0, 0, 128, 96);   // race number, front and back
    x.fillStyle = '#1C1C20'; x.font = '900 64px Arial'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(String(o.bib), 64, 52); const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
    const b = new THREE.Mesh(new THREE.PlaneGeometry(0.17, 0.13), new THREE.MeshLambertMaterial({ map: tx })); b.position.set(0, torsoH * 0.5, sd * (front + 0.016)); if (sd < 0) b.rotation.y = Math.PI; torso.add(b); }
  // buttons / badge details
  if (!ATLB && (o.outfit === 'suit' || o.outfit === 'waiter')) for (const y of [0.2, 0.1]) { const b = box(0.02, 0.02, 0.01, P.black); b.position.set(0.035, torsoH * y, front + 0.008); torso.add(b); }
  if (o.outfit === 'cop') { const badge = box(0.06, 0.05, 0.01, P.yellow); badge.position.set(0.1, torsoH * 0.78, front + 0.01); torso.add(badge); for (const s of [-1, 1]) { const pk = box(0.09, 0.06, 0.01, C.pants); pk.position.set(s * 0.1, torsoH * 0.68, front + 0.006); torso.add(pk); } const belt = box(0.42 * Wd, 0.05, 0.24 + B.belly, P.black); belt.position.y = 0.02; torso.add(belt); }
  if (o.sash && !o.naked) { const cols = [].concat(o.sash), sw = (o.sashW || 0.055) / cols.length, sg = new THREE.Group();   // bandolier (carabiniere) or a mayor's tricolour sash (o.sash = [c1, c2, c3])
    cols.forEach((c, i) => { const sh = box(sw, torsoH * 1.08, 0.014, c); sh.position.x = (i - (cols.length - 1) / 2) * sw; sg.add(sh); }); sg.rotation.z = -0.62; sg.position.set(0, torsoH * 0.55, front + 0.022); torso.add(sg); }
  if (o.outfit === 'swat') { const vest = box(0.44 * Wd, torsoH * 0.6, 0.27, '#2A3442'); vest.position.y = torsoH * 0.55; torso.add(vest); const t = textLabel('SWAT', 0.16, 0.05); t.position.set(0, torsoH * 0.7, 0.14); torso.add(t); }
  if (o.outfit === 'prisoner' || o.outfit === 'pajamas') for (let i = 1; i < 6; i++) { const st = box(0.43 * Wd + 0.01, 0.025, 0.235, o.outfit === 'prisoner' ? '#B85A1E' : P.white); st.position.y = torsoH * i / 6; torso.add(st); }
  if (o.outfit === 'mao') { for (const [x, y] of [[-0.1, 0.72], [0.1, 0.72], [-0.1, 0.32], [0.1, 0.32]]) { const pk = box(0.1, 0.08, 0.01, o.outfit === 'mao' && o.suit ? new THREE.Color(C.jacket).multiplyScalar(0.86).getStyle() : '#6A6C58'); pk.position.set(x, torsoH * y, front + 0.006); torso.add(pk); } for (let i = 0; i < 5; i++) { const bt = box(0.018, 0.018, 0.01, '#3A3B32'); bt.position.set(0, torsoH * (0.2 + i * 0.16), front + 0.008); torso.add(bt); } const col = box(0.16, 0.05, 0.12, C.jacket); col.position.set(0, torsoH + 0.02, 0.0); torso.add(col);
    if (o.collarTabs) for (const sx of [-1, 1]) { const tab = box(0.035, 0.03, 0.012, '#B5302A'); tab.position.set(sx * 0.055, torsoH + 0.02, 0.062); torso.add(tab); } }
  if (o.outfit === 'tourist') { const r = rng(9); for (let i = 0; i < 16; i++) { const f = box(0.05, 0.05, 0.01, [P.pink, P.green, P.white][i % 3]); f.position.set((r() - 0.5) * 0.36, r() * torsoH, front + 0.006); torso.add(f); } }
  if (o.outfit === 'worker' || o.outfit === 'firefighter') for (const y of [0.35, 0.6]) { const st = box(0.43 * Wd + 0.01, 0.035, 0.235, P.grey); st.position.y = torsoH * y; torso.add(st); }

  // neck + head
  const neck = joint('neck', torso, 0, torsoH, 0);
  if (o.outfit === 'vampire') { const col = box(0.36, 0.2, 0.26, '#25262C', { pivot: 'bottom', taper: { x: 1.3, z: 1.2 } }); neck.add(col); }
  neck.add(part('neck', 0.085, 0.15, 0.08, o.skin, { pivot: 'bottom' }));
  const head = joint('head', neck, 0, 0.1, 0); // short neck: ≈ 4–5 % of the height visible (measured)
  const hs = B.headScale;
  const hw = 0.185 * hs * B.headWidth, hh = 0.5 * hs, hd = 0.17 * hs; // MEASURED: head = 20–22 % of the height, W/H ≈ 0.37 (V1/V2); the tornado reference ≈ 0.48
  const faceOpts = { skin: o.skin, hair: o.hair, hairColor: o.hairColor, facial: o.facial === 'cop' ? 'mustache' : o.facial, glasses: o.glasses, lipstick: o.lipstick, seed: o.seed, redNose: o.redNose, beardColor: o.beardColor };
  const headMats = ATL ? [
    new THREE.MeshLambertMaterial({ map: atlasSideTexture(false) }), new THREE.MeshLambertMaterial({ map: atlasSideTexture(true) }),
    atlasMaterial(), atlasMaterial(),
    new THREE.MeshBasicMaterial({ map: atlasFaceTexture('neutral'), color: new THREE.Color(0.97, 0.97, 0.97) }), // flat painted panel: unlit like the originals (face RGB ≈ 235,203,173)
    new THREE.MeshLambertMaterial({ map: atlasBackTexture() }),
  ] : [
    new THREE.MeshLambertMaterial({ map: sideTexture(faceOpts) }), new THREE.MeshLambertMaterial({ map: mirrored(sideTexture(faceOpts)) }),
    mat(o.hair === 'bald' ? o.skin : o.hairColor), mat(o.skin),
    new THREE.MeshLambertMaterial({ map: faceTexture({ ...faceOpts, expression: 'neutral' }) }),
    new THREE.MeshLambertMaterial({ map: sideTexture({ ...faceOpts, back: true }) }),
  ];
  const headGeo = new THREE.BoxGeometry(hw, hh, hd); headGeo.translate(0, hh / 2, 0);
  // subtle trapezoid + skew: jaw a touch wider, crown leaning back (very characteristic)
  const pp = headGeo.attributes.position;
  // MEASURED on frontal originals (find_faces quads): the face panel is NOT a rectangle — top edge slopes down
// ≈ 9° toward image-right (character's left, +x), bottom edge rises ≈ 3°, so that side is ≈ 9 % shorter (R/L 0.90–0.92).
const TOP = Math.tan(9 * Math.PI / 180), BOT = Math.tan(3 * Math.PI / 180);
for (let i = 0; i < pp.count; i++) {
  const t = pp.getY(i) / hh, x = pp.getX(i), u = (x + hw / 2) / hw;   // u: 0 = image left … 1 = image right (camera in front, +x = image right)
  pp.setY(i, pp.getY(i) - (o.irregularHead === false ? 0 : (t > 0.5 ? TOP * hw * u : -BOT * hw * u)));
  pp.setZ(i, pp.getZ(i) - 0.015 * t);
}
  if (ATL) atlasUV(headGeo, { py: AR.headTop, ny: AR.headBottom });
  headGeo.computeVertexNormals();
  const headMesh = new THREE.Mesh(headGeo, headMats); headMesh.castShadow = true; headMesh.name = 'headMesh';
  addOutline(headMesh, 0.035); head.add(headMesh);
  // ears
  for (const s of [-1, 1]) {
    let ear;
    if (o.ears === 'pointy') ear = box(0.03, 0.14, 0.07, o.skin, { taper: { x: 0.2, z: 0.2 } });
    else if (ATL) { ear = part('skin', 0.022, 0.095, 0.062, o.skin); const notch = box(0.006, 0.055, 0.024, '#7E5434'); notch.position.set(s * 0.011, 0, 0.004); ear.add(notch); }
    else { ear = box(0.028, 0.085, 0.055, o.skin); const notch = box(0.006, 0.05, 0.022, '#9A6A45'); notch.position.set(s * 0.013, 0, 0.004); ear.add(notch); }
    if (ATL) ear.position.set(s * (hw / 2 + 0.01), hh * 0.225, hd * 0.1); // sits on the ear painted on the atlas side panel
    else ear.position.set(s * (hw / 2 + 0.012), hh * 0.52, -hd * 0.22); if (o.ears === 'pointy') ear.rotation.z = -s * 0.5; head.add(ear);
  }
  // hair volume on top for big styles
  if (['afro', 'curly', 'mohawk', 'bun', 'long', 'spiky'].includes(o.hair)) {
    let hv;
    if (o.hair === 'afro') hv = box(hw * 1.6, 0.26, hd * 1.6, o.hairColor);
    else if (o.hair === 'mohawk') hv = box(0.05, 0.14, hd, o.hairColor, { taper: { x: 0.4, z: 1 } });
    else if (o.hair === 'bun') { hv = box(0.12, 0.1, 0.12, o.hairColor); hv.position.z = -0.06; }
    else if (o.hair === 'spiky') { hv = new THREE.Group(); for (let i = 0; i < 6; i++) { const s = box(0.05, 0.1, 0.05, o.hairColor, { taper: 0.1 }); s.position.set(-0.1 + i * 0.04, 0, (i % 2 ? 0.03 : -0.04)); s.rotation.z = (i - 2.5) * 0.15; hv.add(s); } }
    else hv = box(hw * 1.12, 0.07, hd * 1.12, o.hairColor);
    hv.position.y = hh + (o.hair === 'afro' ? 0.06 : 0.035); head.add(hv);
    if (o.hair === 'long') { const back = box(hw * 1.08, hh * 0.85, 0.05, o.hairColor, { pivot: 'top' }); back.position.set(0, hh, -hd / 2 - 0.02); head.add(back); }
  }
  addHat(head, o.hat, hw, hh, hd, C);

  // arms
  const shoulderY = torsoH * 0.93, shoulderX = 0.315 * Wd; // arms hang from the outer edge of the square jacket
  for (const s of ['L', 'R']) {
    const sx = s === 'L' ? 1 : -1; // character's left is +x (facing +z)
    const sh = joint('shoulder' + s, torso, sx * shoulderX, shoulderY, 0);
    const pad = part('pad', 0.15 * Wd, 0.09, 0.22, C.jacket); pad.position.set(-sx * 0.03, 0.01, 0); sh.add(pad);
    sh.add(part('sleeve', 0.12, 0.36 * H, 0.13, C.jacket, { pivot: 'top' }));
    const el = joint('elbow' + s, sh, 0, -0.34 * H, 0);
    el.add(part('sleeve', 0.11, 0.3 * H, 0.12, C.jacket, { pivot: 'top' }));
    const cuff = part('cuff', 0.1, 0.05, 0.11, C.cuff); cuff.position.y = -0.3 * H; el.add(cuff);
    const hand = joint('hand' + s, el, 0, -0.31 * H, 0);
    // mitten hand + thumb (flat paddle, slightly cupped like the source)
    hand.add(o.gloves ? box(0.09, 0.135, 0.045, o.gloves, { pivot: 'top' }) : part('skin', 0.085, 0.13, 0.04, o.skin, { pivot: 'top' }));   // o.gloves: e.g. a chauffeur's white gloves
    const th = o.gloves ? box(0.03, 0.065, 0.035, o.gloves, { pivot: 'top' }) : part('skin', 0.025, 0.06, 0.03, o.skin, { pivot: 'top' }); th.position.set(sx * 0.04, -0.01, 0.01); th.rotation.z = sx * 0.5; hand.add(th);
    if (o.claws) for (let i = 0; i < 4; i++) { const f = box(0.014, 0.22, 0.014, '#D9D3C0', { pivot: 'top', taper: 0.3 }); f.position.set(-0.03 + i * 0.02, -0.1, 0); hand.add(f); }
  }
  // legs
  for (const s of ['L', 'R']) {
    const sx = s === 'L' ? 1 : -1;
    const hp = joint('hip' + s, hips, sx * 0.105 * Wd, -0.05, 0);
    if (C.skirt) { hp.add(box(0.08, legLen, 0.08, o.skin, { pivot: 'top' })); }
    else hp.add(part('thigh' + s, 0.14 * Wd, legLen, 0.14, C.pants, { pivot: 'top' }));
    const kn = joint('knee' + s, hp, 0, -legLen, 0);
    kn.add(C.skirt ? box(0.07, legLen, 0.07, o.skin, { pivot: 'top' }) : part('shin' + s, 0.13 * Wd, legLen, 0.13, C.pants, { pivot: 'top' }));
    const ft = joint('foot' + s, kn, 0, -legLen, 0);
    const shoe = part('shoe', 0.14, 0.09, 0.29, C.shoes, { pivot: 'top' }); shoe.position.z = 0.06; // big boxy shoes (measured) ft.add(shoe);
  }

  root.userData = { kind: 'human', spec: o, joints: J, headMesh, faceOpts, hipY, height: hipY + torsoH + 0.1 + hh };
  root.userData.setExpression = (expr) => {
    const m = headMesh.material[4];
    const tex = ATL ? atlasFaceTexture(expr) : faceTexture({ ...faceOpts, expression: expr });
    if (m.map !== tex) { m.map = tex; m.needsUpdate = true; }
  };
  // rest pose snapshot for the animator
  root.userData.rest = Object.fromEntries(Object.entries(J).map(([k, v]) => [k, v.position.clone()]));
  root.traverse(n => { if (n.isMesh && n.name !== 'outline') { n.castShadow = true; } });
  if (o.tint) { const tc = new THREE.Color(o.tint); // fake tan / sunburn: multiply the skin parts and the painted head (cloned materials)
    const tintMat = m => { const c = m.clone(); c.color = (m.color ? m.color.clone() : new THREE.Color(1, 1, 1)).multiply(tc); return c; };
    root.traverse(n => { if (n.isMesh && (n.userData.skinPart || n === headMesh)) n.material = Array.isArray(n.material) ? n.material.map(tintMat) : tintMat(n.material); }); }
  return root;
}

function mirrored(tex) { const t = tex.clone(); t.wrapS = THREE.RepeatWrapping; t.repeat.x = -1; t.offset.x = 1; t.needsUpdate = true; return t; }

function textLabel(t, w, h) {
  const c = document.createElement('canvas'); c.width = 256; c.height = Math.round(256 * h / w);
  const g = c.getContext('2d'); g.fillStyle = '#EDEDED'; g.font = `bold ${c.height * 0.8}px Arial`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(t, 128, c.height / 2);
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  return new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tex, transparent: true }));
}

function addHat(head, hat, hw, hh, hd, C) {
  if (!hat || hat === 'none') return;
  const g = new THREE.Group(); g.position.y = hh; head.add(g);
  switch (hat) {
    case 'copcap': {
      const crown = box(hw * 1.25, 0.1, hd * 1.35, C.hat || P.copBlueDark, { pivot: 'bottom', taper: { x: 1.15, z: 1.15 } }); g.add(crown);
      if (C.hatBand) { const band = box(hw * 1.33, 0.04, hd * 1.43, C.hatBand); band.position.y = 0.02; g.add(band); }   // carabiniere: red cap band
      const visor = box(hw * 1.1, 0.02, 0.1, P.black); visor.position.set(0, 0.01, hd * 0.7); visor.rotation.x = 0.25; g.add(visor);
      const badge = box(0.05, 0.04, 0.01, P.yellow); badge.position.set(0, 0.06, hd * 0.72); g.add(badge); break; }
    case 'swatcap': { g.add(box(hw * 1.15, 0.08, hd * 1.2, P.swat, { pivot: 'bottom' })); const v = box(hw, 0.02, 0.1, P.swat); v.position.set(0, 0.01, hd * 0.65); g.add(v); break; }
    case 'hardhat': { const hc = C.hat || P.yellow; g.add(box(hw * 1.3, 0.12, hd * 1.4, hc, { pivot: 'bottom', taper: 0.8 })); const b = box(hw * 1.6, 0.02, hd * 1.7, hc); g.add(b); break; }   // hatColor: e.g. a UN blue helmet
    case 'toque': { const t = box(hw * 1.05, 0.28, hd * 1.1, P.white, { pivot: 'bottom', taper: 1.35 }); g.add(t); break; }
    case 'bikehelmet': { const hc = C.hat || '#F2F2EE', sh = box(hw * 1.24, 0.12, hd * 1.42, hc, { pivot: 'bottom', taper: 0.72 }); sh.position.z = -hd * 0.06; g.add(sh);   // aero cycling helmet: dark vents, a short tail
      for (const x of [-0.3, 0, 0.3]) { const v = box(hw * 0.13, 0.016, hd * 1.0, '#1C1C20'); v.position.set(x * hw, 0.118, -hd * 0.06); g.add(v); }
      const tail = box(hw * 0.7, 0.07, hd * 0.4, hc, { pivot: 'bottom', taper: 0.55 }); tail.position.set(0, 0.0, -hd * 0.82); g.add(tail); break; }
    case 'wig': { // barrister's wig: a puffy white cap and three stacked rolls (curls) over each ear
      const W = '#EFEDE6', w = box(hw * 1.35, 0.13, hd * 1.3, W, { pivot: 'bottom', outline: 0.01 }); g.add(w);
      for (const s of [-1, 1]) for (let i = 0; i < 3; i++) { const c = cyl(0.055, 0.055, hd * 0.95, W, 8, { outline: 0.02 }); c.rotation.x = Math.PI / 2; c.position.set(s * (hw * 0.66 + 0.03), -0.02 - i * 0.1, -hd * 0.08); g.add(c); }
      for (let i = 0; i < 3; i++) { const c = cyl(0.06, 0.06, hw * 1.2, W, 8, { outline: 0.02 }); c.rotation.z = Math.PI / 2; c.position.set(0, 0.1, -hd * 0.3 + i * 0.12); g.add(c); }
      break; }
    case 'beanie': g.add(box(hw * 1.15, 0.12, hd * 1.2, P.red, { pivot: 'bottom', taper: 0.8 })); break;
    case 'fedora': { g.add(box(hw * 1.7, 0.02, hd * 1.9, P.woodDark)); g.add(box(hw * 1.1, 0.12, hd * 1.2, P.woodDark, { pivot: 'bottom', taper: 0.9 })); const band = box(hw * 1.12, 0.03, hd * 1.22, P.black); band.position.y = 0.03; g.add(band); break; }
    case 'cowboy': { const b = box(hw * 2.2, 0.02, hd * 2.2, P.wood); g.add(b); g.add(box(hw * 1.1, 0.16, hd * 1.2, P.wood, { pivot: 'bottom', taper: 0.85 })); break; }
    case 'firehelmet': { g.add(box(hw * 1.25, 0.13, hd * 1.4, P.red, { pivot: 'bottom', taper: 0.75 })); const br = box(hw * 1.3, 0.02, hd * 2, P.red); br.position.z = -0.04; g.add(br); break; }
    case 'party': { const c = new THREE.Mesh(new THREE.ConeGeometry(0.09, 0.26, 6), mat(P.pink)); c.position.y = 0.13; g.add(c); break; }
    case 'maocap': { const c = C.hat || '#4A5C70'; g.add(box(hw * 1.18, 0.1, hd * 1.25, c, { pivot: 'bottom', taper: { x: 1.12, z: 1.12 } }));
      const vz = box(hw * 0.95, 0.018, 0.09, c); vz.position.set(0, 0.012, hd * 0.66); vz.rotation.x = 0.18; g.add(vz);
      if (C.hatStar) { const st = box(0.045, 0.045, 0.01, '#C8281E'); st.position.set(0, 0.055, hd * 0.66); st.rotation.z = Math.PI / 4; g.add(st); } break; }
    case 'beekeeper': { const b = new THREE.Mesh(new THREE.CylinderGeometry(hw * 1.5, hw * 1.5, 0.02, 16), mat('#F2EDE4')); g.add(b); const c = new THREE.Mesh(new THREE.CylinderGeometry(hw * 0.75, hw * 0.8, 0.12, 12), mat('#F2EDE4')); c.position.y = 0.07; g.add(c);
      const v = new THREE.Mesh(new THREE.CylinderGeometry(hw * 1.15, hw * 1.15, hh * 0.85, 16, 1, true), new THREE.MeshLambertMaterial({ color: '#2A2A2E', transparent: true, opacity: 0.45, side: THREE.DoubleSide, depthWrite: false })); v.position.y = -hh * 0.42; g.add(v); break; }
    case 'crown': { for (let i = 0; i < 5; i++) { const p = box(0.04, 0.12, 0.03, P.yellow, { taper: 0.2 }); const a = i / 5 * Math.PI * 2; p.position.set(Math.cos(a) * 0.09, 0.06, Math.sin(a) * 0.08); g.add(p); } g.add(box(hw * 0.9, 0.05, hd * 0.9, P.yellow, { pivot: 'bottom' })); break; }
  }
}
