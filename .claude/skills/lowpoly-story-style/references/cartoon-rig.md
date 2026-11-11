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
- **Dark skins**: cast `faceRim: True` (or 0..1) draws a crisp pale outline round the brows, the eyes and the mouth of the painted face. Without it the
  black line work has no contrast on a dark skin and the face reads as a plain box at phone size. Never lighten the skin instead. Check with
  `node tools/face/rig_sheet.mjs out.jpg --variant '{"skin":"#8A5A3C","rim":true}'` and look at it reduced to a fifth.
- Clips: `sneezeUp` (dur, breaths, float), `sneeze`, `sniff`, `poster` (pinned flat on a wall, then sliding down: high, slideAt, slide), `spinTop`
  (turns), `headHammer` (at), `blownBack`, `leanAway` (side).
- Facts: `lens` in `cam()` is the vertical field of view in degrees (44 gives a horizontal half-angle of 12.8 deg; a bigger number is wider). A key at
  exactly t = 0 shows the previous clip on the first frame: key a one-shot clip at -0.05.

## Added in cycle 3 (guided hands, a wind of his own, what the first review of story 38 asked for)

- **`reach: { L | R: [x, y, z, w, tip, [px, py, pz]] }`**: a hand guided to a point of the world by a two-bone solver (shoulder and elbow). `w` 0..1
  blends from the clip's pose (keys fade it in and out), `tip` (m) makes the fingertips arrive instead of the wrist (0.16 for a pointing index, 0.05 for a
  fist round a knob), the last value says where the elbow goes (a direction in the frame of the chest; default low, a little out and back). A point further
  than the arm is long stretches both parts of the arm: the cartoon reach comes for free. Key it with the same times, durations and eases as the prop it
  follows (`toonEase` and the prop's `ease`).
- **`touch: { L | R: [joint, x, y, z, w, tip, pole] }`**: the same to a point of his own body, which follows the head wherever the spine and the neck take
  it: `['torso', x, y, z]` or `['head', ...]` in the joint's own units (a head is 0.5 high), or on the face in face units:
  `['face', across (-0.5..0.5, + his left), up (0 chin .. 1 skull; under the nose 0.31, mouth 0.23, an eye 0.62), metres in front]`.
  `sneezeUp` and `sniff` hold the index under the nose with it (`ik: 1`, elbow out to the side: `[-1, 0.2, 0.3]`).
- The puppeteer's trick: when a held prop must land exactly (a stamp on a skull, a knob pulled down, a rider pushed up), give the PROP its own keys and
  guide the hand to its handle. `rotOrder='YXZ'` on a prop lets `rot[0]` pitch it in the plane it faces after `ry`.
- **`wind: [x, y, z]`** (m/s, in his own frame, +Z in front): a wind of his own on the tie and the hair, added to the scene wind: an inhale pulls them up
  to the nose (`[0, 11, 3]` in pulses), a sniff a little.
- Hair on end is five tufts (three in front, two behind), each with its own height and flutter; flat on the crown at rest.
- Clips: `shakeHands2` (role `pump` | `wave`, `grip` point, `amp [first, last]`, `freq`, `stopAt`, `two`, `thumbAt`): one held point, the stroke two frames
  later at each joint, a ring-down; `plankFall` (`hang`, `lean`, `feet`); `sneeze` (`fold`, `chin`: the face stays on a camera in front);
  `sneezeUp` (`ik`, `back`, the inhale's `wind`); `sniff` (`ik`).
- A part of the rig must be applied once per frame (it turns its child joints each time): with a guided hand the spine and the neck are bent first, then
  the solver runs, then the limbs.
- **Limb smears** (opt-in: `st.write(..., limbSmear=1)` or cast toon `{limbSmear: 1}`): an arm or a leg whose joints turn faster than about 9 rad/s is drawn
  as a smear: its far half stretches (up to x1.6 for an arm, x1.5 for a leg) and thins, on top of the drag arcs. Legs that spin on the spot (`scramble`),
  arms that windmill (`teeter`), a top that spins become rubber for the frames where they move fastest. It does nothing to a guided hand.
- **`face.gx` / `face.gy`** (-1..1, painted faces of the face rig): the pupils alone look aside (- = toward his right: screen left when he faces us) or
  down (+) / up (-); the head stays where it is. Use it when a character must watch something beside or above him while his face stays on the camera
  (a head turned further than 45 degrees shows its blank side). Give him a wide-eyed expression, or the pupils hide under the lids.
- Clips, second batch: `sneezeUp` as a ratchet (`times` [start of each breath], `last`, `tremble`: what a breath gains stays; the top of the last one is
  held, shaking); `shakeHands2` pump: `thumb` [x, y, z] (the thumb's hand is guided to a point of the world, in clear sky between two heads),
  `thumbTwist` (rad; 0 set the thumb upright for an arm that goes across the body: sweep it on stills), two pumps along the way; wave: a ring-down after
  `stopAt` (three wobbles in twelve frames, feet planted, the head two frames behind the chest, stars from the release); `sniff` `held`;
  `poster` `peelK` (3: he comes off head first, folded over like wallpaper).
- A flight out of something (a mattress, a cannon): `cannonball` with `spin: 1 / flight time` (one turn), a `to` key with `arc`, then `land` with a
  squash key `sq [1.5, 0.58, 1.0]` (x, not z: seen from the side, z makes him longer on screen).
- **Prop key `squash: [sx, sy, sz]`** (with `dur`, 0.3 s): an impact on a prop: at the key it is squashed to that many times its size and springs back
  with a small overshoot (a plate slammed on a wall `[1.1, 0.82, 1]`, a cap that lands on a head `[1.35, 0.5, 1.35]`). It works on free and attached props
  and multiplies the `scale` keys.

## Added in cycle 4 (a face keyed feature by feature, ripples, the tie, shots in the dark)

- **`face`, one feature at a time, one side at a time.** Every value is an offset from the expression in place (0 = unchanged), so a key bends a named
  expression instead of replacing it: `brow` / `browL` / `browR` (1 = up to the hairline, -1 = down on the eye), `browTilt` / `browTiltL` / `browTiltR`
  (degrees, > 0 lifts the inner end), `lidL` / `lidR` (0..1: a wink, a heavy eye), `low` / `lowL` / `lowR` (0..0.5: the lower lid, a squint),
  `eye` / `eyeL` / `eyeR` (0.4 = 40 % bigger: one eye bigger than the other is a look of suspicion), `mouth: 'name'` (a mouth of the face set: O, o, open,
  scream, teeth, grimace, clench, kiss, pout, whistle, smirk, wavy, zigzag, tongueout, evil, sob, yawn...), `mouthW` / `mouthH` (0.5 = half as wide / tall
  again), `mouthTilt`, `mouthDx` / `mouthDy` (px on the 400 px face: a mouth pulled to one side), `cheeks`, `puff`, `sweat`, `blush`, `tears`, `tear`,
  `vein`, `shadow` (0..1). **L is the left of the picture when he faces us** (his own right eye, the high one).
  Typical uses: `{'browL': 0.9, 'browR': -0.3}` (he knows), `{'lidR': 1, 'mouth': 'smirk'}` (a wink at us), `{'eye': 0.3, 'cross': 1, 'brow': 0.8}` (a clip
  on the nose), `{'puff': 1, 'mouth': 'o'}` (he blows).
- **`wave: { armL | foreL | ... | neck | spine: [amp (m), waves, phase (turns), free, axis (rad)] }`**: a ripple along a part, on top of its bend. The two ends
  stay where they are (a guided hand keeps its point); `free: 1` lets the far end whip (a head on a noodle neck). Key the phase from 0 to 2 and the ripple
  travels twice along the limb; rising phase goes toward the hand. On an arm stretched level by a guided hand, `axis: 1.5708` is the vertical ripple, the
  one that reads from any side. For a whole arm give both halves, the second with `phase - waves` (the story helper `RIP`). Amplitudes: 0.06 m for a taut
  arm that hums, 0.16 m for an arm thrown across a room.
- **`tie: [length, forward, aside]`** (needs `cloth`): the tie taken in a hand. It stretches (1 = its own length, 1.7 = pulled like the cord of a lamp)
  and swings toward the hand (radians). Key it back through 0.85 and 1.05 so that it snaps. The tip of a tie at rest hangs 1.18 m up, 0.135 m in front of
  the chest (knot at 1.61 m, 0.41 m long): the story helper `tie_tip(pos, ry, length, fwd)` gives the point for the hand that pulls it.
- **A shot in the dark**: `st.shot(..., dark=[[t, k, ramp], ...], darkFloor=0.035, darkEyes=1.3)`. `k` 1 = the lights are off, 0 = on; each step is reached in
  `ramp` seconds (default one frame: a switch). The picture falls to cold silhouettes one can barely see (`darkFloor` 0 = black). **The eyes of every
  character with the face rig stay**: the open eyes with their pupils (bigger, heavy lids lifted), a blink makes them vanish, drawn eyes (crosses, spirals,
  happy arcs) show in pale ink, hearts and stars keep their colours, a mouth that shows teeth or a tongue shows too (`face.mouth: 'teeth'`: a grin alone in
  the black); eyes popped out on stalks, stars round a head and a lump show as well. They are hidden by whatever stands in front of the head. A prop with
  `inDark=True` stays visible, lit as in the light (a flame, a torch beam, a white envelope, a city with its own lights); a cast member with
  `darkEyes: False` has no eyes in the dark. Needs `look='natural'` or `'shaders'`.
  The eyes are on the face: **a head seen from the side or from behind shows nothing**, so stage dark shots facing the camera (three quarters at most).
- Head dimensions for placing things on a face (build of the series: head 0.24 wide, 0.5 high, 0.17 deep, its base 1.77 m up): eyes at 0.74 (picture left)
  and 0.54 (picture right) of the head's height, nose 0.31, mouth 0.23; the forehead for a label: offset `[0, 0.4, 0.094]` on the head joint.

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
- The cartoon stories against their own delivered films: render stills at frame-exact times (`f / 30`) and compare them with frame `f` of
  `out/story_<name>_3d.mp4`; a time between two frames differs wherever something moves fast and proves nothing. Characters must match; shadows of turning
  blades and the exposure of a shot metered at another frame may differ by a little.

## Added in cycle 5 (follow-through, settling, props that are not nailed on, pupils; clips for a man who cannot stop)

All opt-in: without them a character is exactly the cycle-4 one.
- **Follow-through** (`st.write(..., follow=1)`, or `toon: {follow: 1}` in a cast entry): free arms behave as damped pendulums driven by the
  acceleration of the root (he starts: they stay behind; he stops dead: they go on, come back, settle in two or three swings; the forearm follows
  the arm 0.05 s late; the head lags on the neck; tie and hair get the same push through `wind`). Stateless like the rest of the engine: the
  root's acceleration over the last 0.75 s weighted by a pendulum's response (12.5 rad/s, damping 0.2). A guided hand or an arm raised by the
  clip does not swing.
- **`settle: a`** in a toon key: once the key is reached the spine wobbles and dies in 0.5 s: a pose that lands instead of a pose that stops.
- **`sway`** on an attached prop (`on={..., 'sway': 1}`): a bird on a cap, a sign on a head, a bag: it rocks about its foot with its carrier.
- **`face.pupilSize` / `pupilSizeL` / `pupilSizeR`**: the painted pupils grow (1 = twice the size: a look that reads from far) or shrink
  (-0.5: pinpricks of fear).
- **`face.tongueYaw`** (rad, + = toward his left) with `tongue` and `tongueLen`: the tongue blown aside by the wind of a run (1.5: flat across
  the cheek and out past the head), fluttering; `tongueDip`: its pitch.
- Clips: `heelBrake` (braking with the heels and not stopping: on a fast `glide` move; lean, mill, chatter), `flag` (carried along behind a
  runner, the body flat in the air, legs fluttering, swinging like a pendulum; `phase` to offset several passengers; `dir: -1`: on his back,
  feet first; the hips fly about 1 m above the actor's position), `shoulderRide` (sitting on another's shoulders: put the actor 1.25 m above
  the runner's position, same move keys).
- Props of story 41 (`engine/props_elan.js`): `cityBus` (see-through, doors, displays, a driver's seat), `busStopPole` and `trafficLight`
  (poles that bend as an arc: `bend` keys, `spring`; `pole_pt` in `story_elan.py` gives the same point for a guided hand), `busDisplay`,
  `headSign`, `townSign` (spins like a weathercock), `lapBoard`, `splitDesk`, `lineMap`, `bigTicket`, `stopButton`, `heelSmoke`, `roadStrip`,
  `stationSign`.
