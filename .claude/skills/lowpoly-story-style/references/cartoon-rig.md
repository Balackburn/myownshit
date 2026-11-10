# Cartoon rig and face rig (opt-in)

For stories staged with visual gags: squash and stretch, bendable limbs, takes, an animated face. Old stories never load this path
(their renders are checked with regression stills). Sources: `engine/toon.js`, `engine/facerig.js`, the cartoon block at the end of
`engine/animations.js`, the automatic layers in `engine/director3.js` (`toonLayer`, `rigFace`).

## Turning it on

- Whole story: `st.write(title, rig='toon', ...)` (script key `"rig": "toon"`): every human gets the body rig and the face rig.
- One character: cast `{'toon': True}` (or `{'toon': {'auto': 0.6, 'breathe': 1, 'overlap': 1, 'drag': 1, 'smear': 1}}` to dose the
  automatic layers), `{'faceRig': True}` for the animated face alone.
- Give every non-hero character its own `seed` (or `glasses: False`): the default seed turns glasses on.

## What moves by itself (cartoon actors)

| Layer | What it does |
| --- | --- |
| breathing | the chest rises and falls (spine stretch ±1.2 %), the brows follow |
| squash and stretch | from the vertical motion: stretch with speed (≤ 32 %), squash on a landing (≤ 38 %), volume kept |
| spine drag | leans back on a start, carries on forward on a stop (from horizontal acceleration) |
| limb drag | arms and legs arc against a fast swing (rubber-hose arcs) |
| smear | above 5.5 m/s the body stretches along its path |
| overlap | elbows, hands, head and neck arrive a few frames after the rest |
| eyes | the pupils go to a look target 0.07 s before the head, glance into a turn of the body, dart now and then |
| blink | lids close in 2 frames, stay shut 1, open in 4; twice now and then; a quick one winds up a strong reaction |
| expressions | blend as numbers in 0.15 s: brows first (overshoot), eyes, then the mouth; lip flaps keep the expression |

## Channels (a clip returns them under `toon`; a story keys them with `k(t, toon={...}, toonDur=0.12, toonEase='out')`, `toon={}` clears)

- `sq: [sx, sy, sz]`: whole body about the feet. `scl: {head: [sx, sy, sz]}`.
- `bend: {spine|neck|armL|foreL|armR|foreR|legL|shinL|legR|shinR: [bx, bz, twist, stretch, fat]}`: bx, bz are the rotation of the far
  end with the signs of a joint's rotation.x / rotation.z; `stretch` multiplies the length (the far joint moves with it); `fat` the
  thickness (default keeps the volume).
- `face: {pop, popLen, pupil, eyeScale, jaw, jawLen, tongue, tongueLen, steam, bump, stars, expr, exprW}`: eyes out on stalks, the lower
  face stretching down with a scream painted on it, tongue, steam from the ears, a bump on the skull, stars circling the head, and
  `expr` + `exprW` pulling the painted face toward a named expression.
- `ears: radians`, `hat: [lift, tilt, spin]`.
- Lengths to remember: the neck is 0.1 m (a periscope needs ×8-10), a thigh or a shin about 0.47 m, an upper arm 0.34 m.

## Clips

`take` (hold, pop 0 = huge painted eyes / 1 = eyes on stalks, jaw, tongue), `doubleTakeToon` (side, beat), `scramble`, `dashOff`,
`hangAir` (downAt, usAt), `pancake` (popAt, stars), `paperThin`, `inflate`, `stretchGrab`, `periscope` (len), `accordion` (amp, freq,
decay, stars), `jelly`, `noodle`, `melt`, `windUp`, `walkRead`, `walkWrite`, `marchPomp`, `skidStop`, `teeter`, `swanDive`,
`cannonball`, `noseJump`, `squeezed`, `stampPhone`. Clips written for the old rig still play; they gain the automatic layers.

## Face rig

`tools/face/gen_rig.py` cuts the measured neutral face into layers (its own brows, eye outlines, whites, pupils and mouth) and paints the
rest with the same ink: `characters/lemec/face/rig/` (blank face, sprite atlas, `rig.json`). The engine composes them per frame:
continuous lids (the original draws a half-closed eye as a flat line over the lower part of the eye), pupils, eye size ×0.8-1.9, brows
(offset, tilt, three shapes), 33 mouth shapes (offset, width, height, tilt), cheeks, puffed cheeks, tears, sweat, blush, vein.
Variants (skin, hair line, clean-shaven, moustache, beard, glasses, lipstick) wear the same rig.

Expressions: the 56 of the face set (same names) plus `take`, `takeSmall`, `deadpan`, `dotEyes`, `greed` (euro eyes), `zap`, `gulp`,
`puffed`, `strain`, `teeth`, `hmm`, `side`, `sideL`. A story adds its own with `st.write(..., faces={'name': {recipe}})`, in the recipe
format of `tools/face/gen_expressions.py`.

Check sheets: `node tools/face/rig_sheet.mjs out.jpg [names] [--blend a:b:n] [--variant '{...}'] [--states '[...]']`.

## Testing

- Motion of a gag, in about a minute: `bash absurd-shorts/tools/motion_check.sh STORY S02 S05 OUTDIR` renders that run of shots in
  draft (cheaper shadows, `render3.mjs --draft --range a:b`) and writes one filmstrip per shot (every second frame). Read the strips
  before any full render: a natural-look film takes about an hour at 1080p, a draft of the whole film at 360p about five minutes
  (`node render/render3.mjs scripts-fr/story_x.json --timed --w 360 --h 640 --draft --out out/x_draft.mp4`, then
  `python3 tools/shot_strips.py out/x_draft.mp4 scripts-fr/story_x.json OUTDIR`).
- One shot changed after the full render: `render3.mjs ... --range a:b --out seg.mp4`, then `bash tools/splice_range.sh FILM seg.mp4 a NEW`.

- Regression of the old stories after any engine change: stills at fixed times before and after, compared pixel by pixel (the natural
  look has a noise floor of about 0.5 % of pixels). A change is accepted when the old stories stay under it.
- One clip or one gag: a 2.5 s test scene per clip with stills at chosen times; a motion strip (every frame over 1 s) for timing.
