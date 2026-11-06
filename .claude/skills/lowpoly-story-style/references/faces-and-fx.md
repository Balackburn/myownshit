# Faces, expressions, micro-animation and generated textures

## One face for everyone (with variations)
Every human character wears le mec's measured face set (`characters/lemec/face/expressions/face_<name>.png`) unless the cast says
`ownFace: True`. The variation comes from the cast/preset options, composited at load time (`engine/atlas.js` `variantFaceTexture`):

| option | effect |
|---|---|
| `skin: '#rrggbb'` | skin tone (skin pixels scaled from the hero's skin; ink and eye whites untouched) |
| `hair: 'bald'`, `hairColor` | the hair line at the top of the panel turns skin, or that colour |
| `facial: 'stubble' \| 'none' \| 'mustache' \| 'beard'`, `beardColor` | stubble kept or the clean-shaven face set; a bushy moustache; a full beard |
| `glasses: True`, `glassesColor` | frames round both eyes (extras with `seed % 3 == 0` get glasses automatically unless the preset says otherwise) |
| `lipstick: True` | red mouth and lashes (female presets set it) |
| `redNose: True` | a red nose |

## Expressions (56)
Measured: neutral, skeptical (suspicious), unimpressed, surprised, shocked, angry, sad, happy, sleepy, blink, scared, talk, talkWide, grin.
Designed in the same ink (`tools/face/gen_expressions.py`): laugh, cry (tears), sob, wink, tongue, tongueOut, rage (vein, clenched),
love (heart eyes, blush), dizzy (spirals), nervous (sweat drop), proud, pout, yawn, kiss, blush, sweat, whistle, lookSide, lookLeft,
lookUp, lookDown, starEyes, smirk, smug, confused, determined, eyeRoll, awe, sneaky, pain, disgust, disgusted, worried, relieved,
drool, squint, cold, surprisedHappy, evil, puppy, bigGrin, dead (x eyes). Old names still work (sideLook → lookSide, grimace → pain).
Each open-eyed face has a `_blink` twin and every face a `_clean` (no stubble) twin; the engine picks them.
To add one: write a recipe in `X` (brows: dy / rot (+ lifts the inner end) / thick; eyes: open | closed | happy | squeeze | x | spiral |
heart | star with s, pupil, lid, low, psize, shine; mouth: line | smile | frown | smirk | wavy | laugh | bigsmile | sob | yawn | O | o |
grimace | clench | evil | tongue | pout | kiss | whistle | drool; extras: tears, tear, sweat, blush, vein), then run
`python3 tools/face/gen_expressions.py --sheet /tmp/sheet.jpg` and look at the sheet.

Use them: give every beat an expression that plays the joke (the dry passer-by smirks under her umbrella, the bride cries under the rain
while he whistles, neighbours rage and eye-roll at the cinema, star eyes on a « 0,00 € » bill, drool when asleep standing).

## Micro-animation (automatic)
- Blinks every ~3.3 s on all open-eyed expressions (an occasional double blink), using the expression's own blink face.
- A quick blink on the first frames of a strong reaction (shocked, surprised, scared, awe, angry, rage, sob, nervous, puppy).
- Lip flaps alternate talk / talkWide with the voice envelope.
- Idle glances: a neutral face looks left or right for 0.45 s every ~4 s when nobody is talking.

## Face FX (situations)
`act(..., fx={'wet': True})` or a key `k(t, fx={'wet': True, 'tears': True})`:
- `wet`: hair strands stuck on the forehead with drips forming at their tips, drops running down the face (rain, flood, bath, shower).
- `tears`: drops streaming from both eyes (pair with `cry` or `sob`).
- `sweat`: drops at the temples and a big drop beside the head (effort, heat, lies).
- `blush`: pink hatched cheeks.
- `shiver`: the head trembles (cold, fear).

## Generated textures (FLUX 3 on Replicate)
`black-forest-labs/flux-3-image` via the Replicate MCP (`mcp__replicate__create_predictions`, `Prefer: wait=60`): text-to-image, or edit
with up to 10 reference images (pass URLs; large data URLs are expensive in tokens). Prompt for flat orthographic, flat-shaded,
pastel, "stylized low-poly video-game texture, no perspective, no shadows, no people, no text". Download the `replicate.delivery` URL
with curl within the hour, save as WebP in `absurd-shorts/assets/textures/`, list it in `engine/models.js` `TEXTURES` (preloaded before the
first frame) and use it with `imageTexture(url)`. In place: three Haussmann facades (cream, pink, grey) used by `parisStreet` by day
(the procedural facade stays at night for the lit windows; `flux: false` on a building opts out).

## Painted strokes (user feedback: « face should have pixels like drawn with paint »)
- `tools/face/gen_expressions.py` draws the features clean at 4x, then `paint()` repaints them like the measured face: a two-scale smooth
  displacement (wobbly contours), the ink processed apart from the fills with a noisy threshold on a blurred mask (uneven thickness, bites),
  a ragged 1-px edge at the native 400x1080 resolution, flat colours sampled on `face_neutral.png` (ink 45,37,31; eye white 205,189,166).
  Eyes are jittered 8-gons (hand-drawn quads), pupils jittered blobs, brows tapered (thick inner end), the mouth line tapered with a fat middle.
- Runtime variant features (glasses, moustache, beard, red nose, lashes) are drawn on an overlay canvas and passed through `paintLayer()`
  in `engine/atlas.js` (same idea in JS) before they go on the face; the glasses' lens tint stays smooth.

## New face FX (La canicule)
- `frozen: true`: frost over the face (white speckles at the edges, a pale blue wash), icicles along the jaw and under the nose, a frosted cap
  on the hair; `frozen: 'thaw'`: half the icicles, drops running at the jaw. `breath: true`: vapour puffs from the mouth (cold air).
  Combine with `shiver` and the expressions `cold` / `shocked`; clips `stiffStand` (frozen stiff) and `hugCold` (hugging himself).
