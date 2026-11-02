---
name: character-face
description: Reconstruct a cartoon character's painted face texture 1:1 from original video frames or screenshots, with code only (no image generation) - find the best close-ups, rectify the face panel, measure and vectorise every stroke, rebuild a clean skin plate, and produce measured + clearly-labelled designed expressions, validated against the reference pixels. Use when the user wants an exact / 1:1 face, face texture or expression sheet of an existing character (any character, not only Le Mec), wants to add a new character's face to the absurd-shorts engine, or asks why a face "doesn't look like the original".
---

# Character face — measured 1:1 reconstruction

The face of these characters is **a flat painted panel on a box head**: one quadrilateral of skin with a thick
ink border, hand-drawn strokes (brows, eye rings, pupils, a nose of 1–2 marks, a mouth bar, stubble dashes, a
scribbled hairline). A 1:1 texture therefore comes from **measuring and re-using the real strokes**, never from
redrawing "something similar". The pipeline lives in `absurd-shorts/tools/face/`.

What changed vs a hand-written landmark JSON: nothing is typed by hand. Corners, strokes, colours, stroke width and
the skin plate are all extracted from pixels; a human only *accepts* source frames and marks occluders.

## Truth hierarchy and labels
1. Original video frames / close-up screenshots supplied by the user (MEASURED).
2. Values derived from them by an explicit operation (rectification, registration, cloning): INFERRED, logged.
3. Anything not visible in the footage (an expression never shown): DESIGNED, built only by transforming the
   measured strokes (lid clip, brow raise/tilt, mouth bend/open). Never claim it is a reconstruction.
4. Character sheets / AI images: comparison only, never a source.
`face_landmarks.json` records, per source and per feature, a value or `"unverified"`, a confidence, and the
`inferred` list. Report these labels to the user.

## Files
- `tools/face/find_faces.py`: step 1, candidate close-ups in the videos (skin quad + thick border + white eye blob +
  ink ratio, ranked by area × frontality × sharpness). Writes `characters/<name>/face/candidates.json` + crops.
- `tools/face/reconstruct.py`: steps 2–7 (rectify, classify, plate, vectorise, compose, validate).
- `characters/<name>/character.json`: the character config (videos, skin HSV range, panel aspect range,
  canonical size, accepted `sources`, `caption_zone`).
- Outputs in `characters/<name>/face/`:
  - `rectified/<expr>.png` + `<expr>_classes.png` (colour-coded stroke classes: check them!)
  - `skin_plate_<expr>.png` (clean painted skin: real texture, grain restored)
  - `face_<expr>.svg` (editable: plate + one `<g>` per layer: border, hair, brow, eye, eyewhite, nose, mouth, stubble)
  - `expressions/face_<expr>.png` (the textures the engine uses)
  - `face_landmarks.json` (measurements, confidence, inferred, statuses, validation metrics)
  - `face_comparison.png` (reference | reconstruction | overlay: red = ink only in reference, cyan = only in ours)

## Workflow (new character)
1. **Config**: create `characters/<name>/character.json` (copy `characters/lemec/character.json`). Set `videos`,
   the skin HSV range (sample 3–4 skin pixels with OpenCV, add ±8 H, ±40 S/V), `aspect_min/max` of the panel (width/height),
   `canonical` (keep the measured aspect, e.g. 400×1080), `caption_zone` (vertical range of the burned-in captions).
2. **Find**: `python3 tools/face/find_faces.py characters/<name>/character.json --top 10 --step 2`.
   Look at the crops (tile them, open with Read). Reject frames where the green quad is not exactly the face panel.
3. **Accept sources** in `character.json → sources`: one `identity: true` frame (sharpest, frontal, least occluded:
   hairline, border, nose, stubble come from it) + one source per **expression that is visible** in the footage, named
   by what you see. Add `occlude: [[x0,y0,x1,y1]]` (normalised panel coords) for props / FX / hands in front of the face.
   Captions are masked automatically.
4. **Reconstruct**: `python3 tools/face/reconstruct.py characters/<name>/character.json`.
5. **Check, in this order** (open the images, do not trust numbers alone):
   - `rectified/*_classes.png`: brows yellow, eye rings green + whites cyan, mouth blue, nose magenta, stubble grey,
     hair red, border white, occluded = red tint. Fix misclassification by tuning the rule in `classify()` or adding an occluder.
   - `face_comparison.png`: the overlay must be black (both) everywhere on the identity row. On other rows, black on
     expression strokes; red/cyan stubble is expected (stubble comes from the identity frame by design).
   - `validation` in `face_landmarks.json`: identity `ink_iou` ≥ 0.85, `mae` ≤ 5 (Le Mec: 0.883 / 3.3).
     Other measured expressions: IoU 0.6–0.7 is normal (identity layers deliberately differ); look at the overlay.
6. **Fix 3 worst, re-run** (the run takes about 3 s).
7. **Engine**: `engine/atlas.js` loads `characters/lemec/face/` automatically (FACE_SET_DIR, EXPR_MAP). For a new character,
   point a preset at its face set (copy that block with its own dir) and render a close-up with
   `node render/shot.mjs "what=humans&list=<preset>&nolabel=1&cam=0.45,2.2,1.6,0,2.0,0&fov=38" out/f.png 576 1024`,
   next to an original frame.

## Rules (keep them)
1. Never redraw a measured stroke; vector layers are the traced outline of the real ink (0.6 px tolerance).
2. Never symmetrise, never mirror features, never apply "facial proportion" rules.
3. Identity layers (border, hairline, nose, stubble, skin) come from ONE identity frame, for every expression.
4. Expression layers (brows, eye rings, whites/pupils, mouth) come from the frame that shows that expression, after
   ECC registration onto the identity panel; if not shown → DESIGNED transform of measured strokes, labelled.
5. Occluded areas are not measured: mask them; any fill (stubble/skin cloned from neighbouring rows) goes in `inferred`.
6. Randomness only with a fixed seed (grain restoration uses seed 7).
7. A high IoU is not proof: always look at the overlay and at an engine close-up next to the original frame.
8. Never claim "1:1" for a designed expression or an unverified feature.

## Known limits (say them when relevant)
- Very low-resolution or motion-blurred close-ups lose thin strokes (stubble dashes merge).
- Hair/border touching the panel edge are both "edge ink"; the split is by size/position.
- Side and back of the head are NOT reconstructed by this pipeline (they come from the atlas or other frames).
- Expressions involving teeth/tongue are only drawn generically in designed mode (no measured source yet for Le Mec).
