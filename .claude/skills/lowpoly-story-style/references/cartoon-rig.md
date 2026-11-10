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

## Keys added for staging (second pass of cycle 1)

- `auto: 0..1` inside a toon key doses the automatic layers while the key holds (`k(t, toon={'auto': 0, ...})`): use it for a choreographed fall or a
  lift-like descent, where the stretch from speed and the squash from deceleration would move the head.
- `blend=<seconds>` on a clip key: its own blend from the previous clip (plain and fast: no anticipation, nothing trails). `blend=0.02` is a hard hit.
  On a move: `blend` (into the gait) and `thenBlend` (into the clip that follows).
- `cadence=<cycles per second>` on a move: the gait frequency set by the story (quick small steps on the air).
- A stretched leg grows downward from the hip (the feet go down, the body stays); the spine and the neck grow upward.
- A base clip (the actor's `clip`) started long before the shot: one-shot clips (`stampDesk`, `hangPhone`, `splat`, `cannonball`...) must be keyed:
  `k(0.0, clip=...)`.
- Props: after `detach=True` (no `fall`), later `to` keys move the prop from where it was released (`None` keeps a coordinate); `worldRot=[x, y, z]`
  turns it to the camera; `wobble=[amp, freq, decay]` rocks it in place.

## Added in the third pass of cycle 1 (after the second review)

- `face.eyeYaw` / `face.eyeRoll` (radians): the popped eyeballs turn at the end of their stalks. Yaw brings the pupils round to a camera that films the
  stalks from the side (sign: toward the actor's +X, his left); roll turns them about the stalk (a look round). `face.popBlink: 1` closes lids over
  them, `face.stalkRed: 0..1` takes the stalks from skin to pink (they read on a pale ground), `face.stalkBow` (m) bows them outward.
- `face.lid: 0..1`: the painted eyes close by key (a slow blink: 0 -> 1 -> 0 over seven frames; the automatic blinks stay).
- `scl: {handL | handR: [sx, sy, sz]}`: a hand that swells (the big glove of a last wave).
- `royalWave`: `fore` (1.84 puts the forearm upright, so a stretched forearm grows straight up) and `foreAmp` (0.3 when it is stretched: the far end
  of a 3.5 m forearm swings a metre for 0.1 rad). `meltDown`: `flat` (0.97: down to a film; then hide the actor and show the prop `meltPuddle`).
  `hoseNeck`: `curve` and `lean` (a standing arc to the side / forward: a swan's neck).
- Prop `meltPuddle` (props_trou.js): `color`, `dots` (the pattern of the shirt), `r`, `at` + `dur` (it spreads), `landAt` (it jiggles), `eyesAt`,
  `gaze: [[t, x, y, z], ...]` (directions), `blinks: [t, ...]`. Hat `firecrest` (a fireman's helmet that reads from far).

- Fourth pass: `meltDown` takes `sink: 1` (upright, like a candle: head into the shoulders, trunk shorter and wider, legs last; nothing folds forward);
  the part of a stretched limb that lies past its far joint (the bit of neck inside the head) stays rigid; `completSign` takes `onColor` / `onGlow`;
  `windTurbine` takes `rpmKeys: [[t, rpm], ...]` (ghost blades only once it is fast); new clips `stampDown` (hit) and `shakeHands` (role, stopAt, thumbAt).
- A flash check for coplanar surfaces: `python3 absurd-shorts/tools/flash_check.py FILM.mp4 scripts-fr/story_x.json`.

## Added in cycle 2 (opt-in: `st.write(..., fingers=True, cloth=True, idleShift=1)` or per cast member)

- **Finger hands** (`engine/fingers.js`): a palm, four two-part fingers, a two-part thumb in place of the mitten. Toon channel
  `hands: {L: 'point', R: [index, middle, ring, little, thumb, splay]}`; poses `rest`, `open`, `spread`, `fist`, `point`, `two`, `pinch`, `thumbUp`,
  `grip`, `claw`. Curls 0..1, thumb -1 (up) .. 1 (folded), splay -1..1. The palm faces +Z of the hand joint; turn the wrist with `handL` / `handR`.
- **What trails** (`engine/cloth.js`): a tie in three segments (the painted one is removed from the hero's jacket) and a shock of hair on the crown,
  both driven by the apparent wind (scene wind minus the actor's own velocity, in the frame of the chest and of the head): the tie swings on a stop,
  flies up in a fall, goes over the shoulder only in a head wind above 5-11 m/s; the hair stands in a wind. Toon channel `hairUp: 0..1` leaves the hair
  standing whatever the wind (somebody who has just been blown at).
- **Scene wind**: `fx=[{'type': 'wind', 'at': t, 'dur': d, 'v': [x, y, z], 'attack': 0.06, 'release': 0.25}]` (m/s, world; gusts add up).
- **Idle weight shift** (`idleShift=1`): standing actors change their supporting leg in short moves, each at his own time.
- `face.cross: 0..1`: cross-eyed (painted eyes and popped eyes). The engine warns when a one-shot clip is given as an actor's base clip.
- Clips: `sneezeUp` (dur, breaths, float), `sneeze`, `sniff`, `poster` (pinned flat on a wall, then sliding down: high, slideAt, slide), `spinTop`
  (turns), `headHammer` (at), `blownBack`, `leanAway` (side).
- Facts: `lens` in `cam()` is the vertical field of view in degrees (44 gives a horizontal half-angle of 12.8 deg; a bigger number is wider). A key at
  exactly t = 0 shows the previous clip on the first frame: key a one-shot clip at -0.05.

## Clips

`take` (hold, pop 0 = huge painted eyes / 1 = eyes on stalks, jaw, tongue), `doubleTakeToon` (side, beat), `scramble`, `dashOff`,
`hangAir` (downAt, usAt), `pancake` (popAt, stars), `paperThin`, `inflate`, `stretchGrab`, `periscope` (len), `accordion` (amp, freq,
decay, stars), `jelly`, `noodle`, `melt`, `windUp`, `walkRead`, `walkWrite`, `marchPomp`, `skidStop`, `teeter`, `swanDive`,
`cannonball`, `noseJump`, `squeezed`, `stampPhone`. Clips written for the old rig still play; they gain the automatic layers.

Second pass: `fallDrag` (falling feet first, everything trails), `splat` (flat on his back like a rug for a camera looking down 30 deg; popAt, stars,
blinkAt), `royalWave` (bent elbow, wrist; side, flickAt), `stampDesk` (hit), `hangPhone` (downAt, usAt, expr), `reachHigh` (side), `headStuck`
(upside down, legs wobbling; sink), `meltDown` (dur, spread, landAt), `hoseNeck` (len, sway, backAt); `accordion` takes `hit: True` (hard landing, bellows
bounces), `teeter` takes `spin`, `pop`, `jaw`.

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
