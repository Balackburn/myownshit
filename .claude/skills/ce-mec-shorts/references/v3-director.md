# Director v3 — scene timelines locked to the real voice

v3 is the default pipeline (`engine/director3.js`, `render/render3.mjs`, `tools/audio3.py`). It replaced the
v2 "one sentence = one shot" model, which produced backward walking, characters talking to walls and empty
shots. Working examples: `scripts-fr/chrono3.py` (45–55 s, dialogue) and `scripts-fr/gorille3.py` (4 min,
24 scenes). Write the storyboard in Python (helpers `L / act / k / cam / P`), which generates the JSON.

## Data model

```
episode: { version: 3, title, captionWords: 3, captionY: 0.66, voice, music, cast: {id: spec}, scenes: [...] }
voice:   { name: 'allan tiktok', model: 'eleven_v4',
           narrator: {stability .8, style 0, rate 1.06}, character: {stability .4, style .4, rate 1.02} }
scene:   { id, set, setOpts, lighting, ambience, lines, actors, props, cams, sfx, fx, freeze, daynight, pre, tail }
line:    { id, text, speaker?, highlight?: [words], pre? }  speaker = actor id -> same voice, character settings, lip flaps
```

- The voice is generated first (ElevenLabs `/with-timestamps`). Every time in a scene can then be written
  against the real words: `'g12'` (line start), `'g12.end'`, `'g12.mid'`, `'g12#3'` (4th word), `'g12:gros'`
  (first word containing "gros"), plus an offset `'g12:gros+0.4'`. A word with a hyphen cannot be matched by
  name, so use `#index` for it. `python3 tools/when.py out/work/<name>/script.timed.json g12:gros` prints the
  absolute time, which is useful for `--stills`.
- A dialogue line is spoken by a character with the same authorised voice and only another intonation. The
  narrator never repeats a line that a character has already spoken.

### Actors
`{id, pos, ry (deg), clip, expr, face (initial target id or deg), scale, visible, params, keys: [...]}`

Keys (all take `at`):
- **move**: `{to | path, clip (gait, default walk), speed | dur, then, thenParams, faceEnd (target | deg), face: 'move'|'keep'|target, glide, arc, land, ease}`.
  - The actor automatically faces the direction of travel, and the gait cadence comes from the speed.
  - After the move the previous clip resumes, unless `then` is set.
  - `glide` + `arc` moves along a jump arc (vault, hitFly, airborne). `face: 'keep'` is for knock-backs.
- **clip**: `{clip, params, speed}`; **face**: `{face, turn}`; **look**: `{look: target | null}` (head only);
  **expr**: `{expr}`; **scale**: `{scale, dur, ease}`; **visible**: `{visible}`; plus `sfx` / `sfxAt` / `vol` on any key.
- Never put a clip key inside a move, because the actor would glide; chain with `then` instead. Never start
  an actor on a gait clip without a move (the lint reports "walking on the spot").

### Props
`{id, name, opts, pos | anchor+offset, ry, scale, visible, on: {actor, hand | joint, offset, rot}, keys, alt}`
- Keys: `attach` (to an actor's hand or joint, or to another prop) and `detach` with
  `{fall, toss: [vx, vy, vz], spinFall, impact, restRot}`. Moves on free props use `{to | path, dur, ease}`.
  `visible` / `scale` / `sfx` keys also work, and `alt` swaps in a broken look.
- `joint: 'root'` attaches to the actor object itself. It follows position and facing, but **also the clip's
  root offset**: a crouch lowers the prop. Compensate in `offset` (the Metal Gear box uses
  `h 1.5, offset [0, 0.66, 0.3]`).

### Cameras
`{at, frame: id | [ids] | [x,y,z], size: ecu|cu|mcu|ms|mls|fs|ws|ews, angle (deg, relative to the first subject's facing) | worldAngle, elev, lens, zoom, move: push|pull|orbit|crane|track, amount, ots: [a, b, side], pov: [a, b], allowBack, noOcclusion, withProps, cut: false + glide}`
- Framing comes from the real bounding boxes over the whole shot. Close-ups keep the face above the
  captions; 9:16 tight shots may crop arms.
- **OTS** is solved on screen: A's head sits big at the frame edge and B's face is right of centre, at any
  distance. `side` picks which edge.
- **Occlusion solver**: each candidate camera is checked at 2 moments of a fixed shot or 3 of a tracking shot.
  - Per subject it probes the head, the upper row, each column and a 6-point grid. Rods, bars and rails are
    see-through. Legs behind a desk are allowed.
  - It also rejects foreground clutter (an object covering ≥3 of 15 rays in the front half) and any camera
    inside an actor or static set geometry.
  - It tries front angles, then +18° elevation, then back angles.
  - When everything is blocked, it steps in front of an obstacle near the camera, or uses the least-occluded
    view and warns.

## The QA loop (do all of it, every time)
1. `python3 scripts-fr/<slug>.py`, then
   `node render/render3.mjs scripts-fr/<slug>.json --w 360 --h 640 --stills cams`.
   This generates the voice (cached in `out/tts_cache3`), prints the **warnings** (blocked views, back to
   camera, walking on the spot, unknown words) and writes `out/work/<slug>/cams.jpg`, one still per setup.
   Read the whole sheet; split it into parts of 40 setups if it is long.
2. Fix every grey, black or empty frame, every subject that is not visible, and every foreground object
   eating the frame. Then rerun.
3. `--stills t1,t2` at full size (`--w 540 --h 960`) for doubtful frames: faces, props in hands, the box gag.
4. `--preview` (360×640 at 15 fps, with audio). Check motion with `tools/strip.sh video.mp4 out.jpg start dur fps cols`
   and read the strips scene by scene, looking for backward walking, gliding, facing, contact and timing.
5. Final render: `node render/render3.mjs scripts-fr/<slug>.json`.
   - Output: 1080×1920, 30 fps, H.264/AAC at −14 LUFS, plus `.srt`, `.script.txt` and voice/SFX/music stems.
   - Throughput: about 2 fps with 4 workers, so a 4-minute film takes about an hour. Run it in the background.
6. Verify with ffprobe and ebur128, and grab a few frames of the MP4. You cannot listen to the audio in this
   environment, so say so.

## Staging rules learned the hard way
- Everyone exits away from the next shot's subject. In the chrono bar, the clients leave on the left so
  nobody crosses the drunk's shot on the right.
- Check props against the set: desks are 1.7×0.8 and rotated, and a character never stands inside one. Go
  around it with a `path`.
- A sign or parked car near the visitor side ruins shots. Move set dressing (`setOpts`: `signX` / `signZ` for
  the zoo) and hide vehicles until they arrive.
- Secondary faces are procedural line art. Strokes were made thicker for phone size; use `redNose` /
  `beardColor` for gags.
- No overlays at all (no banners, dates or floating symbols); captions only. The hidden watermark
  `wmSign` (poster, sticker or stand) appears on 4–5 sets in a 4-minute film and never centre frame.

## Places and backgrounds (viz3d pass)

Sets follow the `visualize-in-3d` skill (codepawl/viz3d, installed in `.claude/skills/`), adapted to the series look
(flat matte low-poly, paper grain, muted palette, outlines on key objects):

- **Build from real references, not memory.** A place gets the elements its real counterpart has. For example, a gorilla
  habitat has rockwork with the night-house door, a climbing frame with ropes and a fire-hose hammock, a dead climbing
  tree, hay, logs, worn dirt and a visitor promenade.
- **Detail in the order the camera sees it:** silhouette, then large forms, then panel lines, signage and lights.
- **Lived in:** every room holds what its people really own (a lab has glassware, drums, a fume hood and hazmat suits;
  a fast food has tills, menu boards and fryers; a station has lockers, cabinets, a water cooler and a coffee corner).
- **Motivated light:** visible lamps, tube lights and screens. Gyms and interiors use `interior` lighting; dark subjects
  must read against floors and walls.
- **Keep acting areas clear:** the centre, the paths in the storyboard, desk fronts and cell fronts. Re-run
  `--stills cams` after any set change and check that nothing new eats the frame.
- **QA:** `node tools/qa_sets.mjs zoo,lab,...` lists coplanar (z-fighting) pairs and mesh/triangle counts per set.
  `engine/qa/frame-guard.js` and `coplanar-check.js` are the viz3d scripts.
  Visible coplanar faces need ≥ 2 cm separation; flat ground details are slabs, not planes at y = 0.003.
- **Brand signage** can be a set option (`restaurant` `setOpts: {brand: 'MASTER POULET'}`) instead of a floating scene prop.

## Props that change over time, writing gags, inside-out cameras (from "Son nom dessus")

Working example: `scripts-fr/marqueur.py`.

- **Prop options ending in `At` accept time expressions**, single or as lists, for example `openAt`, `closeAt`,
  `writeAt` and `writeAt2`: `opts: {'writeAt': 'M4:sur', 'writeDur': 1.0}` or `opts: {'openAt': [-0.6, 'M1:Tous-0.1'], 'closeAt': ['M1:voler+0.25']}`.
  - The fridge opens and closes in cycles.
  - The door takes `plaque`, a felt-pen `name` that moves with the leaf, plus `openAt` and `closeAt`.
  - Check every word anchor: `L:word` matches the **first word containing** that text, so `'M10:Vous'` hit "vous," three words
    earlier. Use `#index` or another word instead (`'M10:voulez'`).
- **`scrawl`** writes felt-pen handwriting on any surface: `opts {text, w, h, color, writeAt, writeDur, strike, underline}`.
  - The letters appear left to right while the writer holds `drawOn`, `drawMid` (chair back), `drawLow` (crouched, car
    side), `drawUp` or `sitDraw`.
  - Attach it to a prop with `on: {actor: 'chair', offset, rot}` or to a forehead with `{actor, joint: 'head', offset: [0, 0.455, 0.094]}`.
  - Use dark ink on light surfaces only: black on a navy chair is unreadable, so the office chair is light grey.
  - `yogurt` takes `name`, `strike` and `name2` (the new owner in red) for the "crossed-out name" punchline.
- **Held cups and pots stay upright** with `on: {hand: 'L', rot: [1.5708, 0, 0], offset: [0, -0.12, -0.05]}` and a
  forearm close to horizontal (shoulder + elbow pitch ≈ −1.6). Clips with that arm are `writeOnHeld`, `eatSpoon`, `sitEatSpoon` and `walkEat`.
  - A prop held up beside the face (the granny's giant marker) needs `rot: [π, 0, 0]`. Put it in the hand on the camera
    side, then re-`attach` it to the writing hand.
- **Inside-out camera.** A person using a fridge, a door or a vault faces away from every front camera. Use an explicit
  camera inside the object instead: `{'at': t, 'from': [3.42, 1.6, -3.45], 'lookAt': [3.12, 1.78, -2.3], 'lens': 62}`.
  - That shot keeps the yogurt in the foreground and the face in the opening.
  - When the door closes, the frame goes "dark" for a comic beat ("Putain,").
  - Repeat the same POV as a motif: the theft, "Tous les jours.", the name, the startle.
- **Inserts of written text** frame a point (`[[x, y, z]]`, a 0.8 m box) with `cu` and `noOcclusion`.
  - Shoot them after the writer steps aside, or from the side away from the writer: the writer's body stands between a
    front camera and the surface.
- Other new clips: `bow` (servile banker), `pointDown` ("à genoux"), `kneelGive` and `kneelMassage`, `sitSip`,
  `carryBags` and `holdBags` (shopping bags), and `showMarker` / `showMarkerL`.
- Other new props: `officeChair`, `cupboard` (broom closet, `sign` on the header plate), `shoppingBag`, `moneySack` and
  `spoon`.
- `office` takes `setOpts {door: false, printer: false}`. The film then supplies its own animated door and puts the closet
  in the right corner.

## Fast news series (actu01–actu10): what changed and what bit

The news series lives in `scripts-fr/actu_common.py` plus `actu01_pigeon.py` … `actu10_chat.py`, with the gag bank
`gags-actu-automne-2026.md`.

- **Pace.** Faster cutting and faster acting come from:
  - episode `tempo: 1.35`, which plays gestures, blends and turns faster (gaits keep the cadence derived from their speed);
  - narrator rate 1.12 and character rate 1.08;
  - shots of about 1.5 s;
  - an extra insert in any static shot longer than about 3 s.
- **Standard set-ups** live in `actu_common.py`:
  - interrogation room: suspect in the far chair, inspector at the table's right end with `ry -90`, so both are in profile from the front;
  - a post lying flat on a table, read from above (`tweet_on_table` / `tweet_cam`);
  - the press-room apology (`pressRoom`: backdrop words, `bg`/`fg`, optional podium and flags);
  - the cell and the court.
- **Overhead props.** With the arm raised, the hand's local +y points down, so anything held above the head needs
  `rot [π, 0, 0]` and the grip offset along +y (`SIGN_UP`). Signs and the parasol came out upside down before this was
  fixed. A flat card shown at arm's length uses `HAND_FLAT`.
- **Contrast.** Navy suits vanish on the navy press-room backdrop. Use `bg '#D9E2E8', fg '#2E4563'` for debates and
  treaties.
  - Canvas text in the same colour as its background is invisible. A cream notebook needs a dark `bg`.
- **Cells and bars.** An `ms` of two subjects 1 m apart puts the camera beyond the cell bars. Use an explicit `POV`
  inside the cell.
- **Creature speakers** (a pigeon's "Rou.", a goat's "Mèèè.", a dog's "Wouf") are spoken with the same voice. A dog that
  barks to the camera (`face` toward it) reads better than one barking at the suspect.
- **Queue.** Write and check the next story while the previous one renders. If you edit a JSON while its render has
  already started, that render uses the old version: stop it and queue it again.

## Long story with a flashback (« Le resto chinois », 2 min 30)

Working example: `scripts-fr/restochinois.py` (16 scenes, 51 lines, 91 camera set-ups).

- **Per-scene grade.** `scene.grade` replaces the film grade (a CSS filter string). The flashback uses
  `'contrast(0.9) saturate(0.45) sepia(0.62) brightness(1.04)'` on every past scene, and a white `flash` fx on both sides of
  the cut into it. Rule of thumb: sepia = the past, normal = the present.
- **Music cues.** A scene sfx named `music:<kind>` goes to the music stem and fades the episode bed out under it:
  `{'at': 'R12', 'name': 'music:zouk', 'until': 'R14+1.0', 'vol': 0.42, 'file': 'assets/music/user/x.mp3', 'offset': 0}`.
  - `until` (or `dur`) sets the length.
  - When `file` exists (a track the user holds the rights to, kept out of git), it is played from `offset`. Otherwise the
    procedural stand-in for `<kind>` plays: `zouk` is an original groove made in code.
  - Never download a song from YouTube or any other site. Name the song in the narration if needed; say where the user can
    drop their own file.
- **New SFX:** `sniff`, `static`, `choir` (the "treasure" swell: cutlery, the greatness of China, falling in love), `jet`,
  `fanfare`, `heartbeat`.
- **New sets:**
  - `chineseRestaurant`: `brand`, round tables, lanterns, fish tank, bar.
  - `proKitchen`: wok range with live flames, prep island, a big clock with `clockRate`.
  - `maoStreet`: 1970s hutong with Chinese slogans, a red gate, bicycles, a loudspeaker, a side alley.
  - `tinyCell`: a 0.62 m niche behind bars, tally marks, a drawn window.
  - `pavillon`: a suburban house front.
  - `pressRoom` now takes `fontScale` (long backdrop words), `podium: false` and `flagOpts` (`{'colors': ['#DE2910'], 'prc': True}`).
- **New props:**
  - Cutlery and tableware: `fork` / `knife` (`handle` colour, `shine`), `chopsticks` (`single`), `riceBowl`, `noodlePlate`.
  - Animated: `powderLine` (`goneAt`), `cutleryCase` (`openAt`, `beam`: golden light), `boombox` (`text` on the tape, `playAt`,
    `stopAt`, `bpm`: the cones pulse), `flame`, `aquarium`.
  - Set dressing and the rest: `megaphone`, `planter`, `plane`, `photo`, `windowDrawing`, `lantern`, `hornSpeaker`, and `flag`
    with `prc`.
- **New presets:** `restaurateur`, `restaurateurMao`, `policeMao`, `dealer`, `internaute`, `internaute2`, `officiel` and
  `mecMao`.
  - Hat `maocap` takes `hatColor` and `hatStar`. Outfits also take `pants` and `collarTabs`.
  - `atlasBody: false` keeps the protagonist's painted head with any outfit (`mecMao` is "ce mec" in a tunic).
- **What bit:**
  - Two actors facing each other: `ry = degrees(atan2(dx, dz))` toward the other one. A sign error had the dealer talk to the
    wall. A profile two-shot then sits at the worldAngle perpendicular to the line between them.
  - A point frame (`[[x, y, z]]`) is narrow in 9:16. Two animals 1.4 m apart fell outside it and looked "missing". Frame on
    their ids instead, and check positions with a probe before assuming a bug.
  - A long prop attached behind an actor (the giant fork in his backside) disappears into a wall less than 0.8 m behind him.
    Move the actor away from the wall, or drop the podium.
  - The floor of a narrow barred cell cannot be filmed: the bottom rail, the posts and the man's legs are in the way. Give the
    prop to the actor (he holds his one-chopstick "bed" up).
  - In the press room the seated journalists block the solver's cameras. Use explicit POVs, from in front of them or from above
    their heads at the back.
  - Overhead and forward props both need `rot [π, 0, 0]` (`FORK_UP`, `SIGN_UP`). A held flag needs `withProps=True` on the
    camera, or it is cut off above the frame.
- **Satire of China:**
  - No put-on accent: one voice, as everywhere else.
  - Generic faces. Period clothes and props carry the setting.
  - The joke aims at the regime and its propaganda, made obvious by a "SOURIEZ" cue card during "the happiest man in the world".
  - Chinese text renders (WenQuanYi is installed). Use real, correct slogans (为人民服务) or plain phrases (禁止西方产品).

## Transformation story (« Le looksmaxing », 2 min 27)

Working example: `scripts-fr/looksmaxing.py`.

- **POV `lens` is a vertical field of view in degrees.** Bigger means wider.
  - About 58–60 shows head and chest at 1 m (a mirror shot).
  - 34–40 is a tight insert.
  - A "wide" POV with lens 30 at 1 m only shows the tie.
- **A move key lands on a pose only with `then`.** Give both `clip` (during the move) and `then` (after). For a jump cut, use
  `glide=True, dur=0.05, clip='sitLookItem', then='sitLookItem'`. With `clip` alone the old clip comes back after the move,
  and `then` alone was not applied either.
- **Per-camera grade.** A camera entry can carry `grade` (CSS filter): `{**POV(...), 'grade': DREAM}`. Two uses here:
  - "how he sees himself": the handsome version in the same spot, bright and warm;
  - the perfect man's reveal.
- **Progressive uglification** means one cast id per stage, swapped in place with `visible` keys at the same position, plus a
  `poof`.
  - `mecGonfle`: width 1.6 and belly. `mecOrange`: the same with `tint`. `mecMonstre`: width 1.95, small head.
  - `tint` multiplies the skin parts and the painted head (cloned materials), so the painted face keeps its expressions.
- **Face add-ons** attach to the head joint, whose origin is the bottom of the head.
  - `squareJaw` at y 0.02, z 0.05.
  - `googlyEyes` at y = 0.5·hs·0.6, z = 0.085·hs + 0.012.
  - `faceLumps` (bumps and bandages) at y = 0.5·hs·0.55.
  - `monster_face(actor, hs)` in the script builds the set. They follow a lying head too (the surgery seen from above).
- **Mirror scenes.** The person faces the mirror (`ry 180`), so the inside-out mirror POV gives the face. A side POV from the
  hand side shows the injection. Keep about 1 m between person and mirror.
- **New props:** `kit72` (case of 72 vials, the lid's label), `chainsaw` (`runAt` / `stopAt` shiver), `squareJaw`,
  `googlyEyes`, `faceLumps`, `ringLight`, `mirrorFull`, `fitPoster`, `halo`.
- **New set:** `chambre`, a bedroom restyled with `wall`, `poster`, `posterBg`/`posterFg`, `blanket` and `curtain`.
- **New presets:**
  - The guru: `clavicule`, a fictional character with tiny head and huge shoulders.
  - `femme`, `journaliste`, the extras `looksmaxeur`, and `mecBeau` (how he sees himself).
  - Glucksmann in three states: `glucksPeur` (small, scared), `glucksBeau` (tall, V-shaped) and `glucksMou` (small,
    deflated).
- **New SFX:** `chainsaw`.
- **Violence by ellipsis.** The chainsaw goes up by his face with the buzz, the shot fades to black, and the next scene opens
  on the bandages.
- **Real people.** Nothing sexual and nothing about private life. A real partner of a public figure is replaced by a
  fictional character: "48 hours instead of 2 minutes" became a TV interview, with the day/night cycle and a spinning clock.
  Make no Nazi comparisons, and name no hard drugs for a real person ("le programme").

## Six classic shorts in one batch (parfum, journal, frigo, canette, machine, réveil)

Working examples: `scripts-fr/parfum.py`, `journal.py`, `frigo.py`, `canette.py`, `machine.py`, `reveil.py` (about 19–23 s each).

- **Time expressions with a hyphenated word fail.** `L:lui-même` is a "bad time" that resolves to 0, and a camera at 0
  silently replaces the scene's first shot. Use the 0-based word index instead: `R5#7`. A number plus an offset as a string
  (`"0.05+0.12"`) is also a bad time; compute the number in Python.
- **Contact-sheet stills are taken at each shot's midpoint.** A white still can just be a flash event, and a prop "already
  there" can be mid-move. Check with `--stills t1,t2,...` before changing anything.
- **Someone facing an object against the back wall shows their back to every camera.** Stage them in profile (`ry ±90`) with
  a front camera; the engine warns from about 100°. This applies to a nightstand alarm clock, a washing machine, a judge's
  bench or a dog in the dock. Otherwise turn the subject (`face=10`) for the close-up.
- **Day and night:**
  - `daynight: {from, period, once: True}` falls to night and stays there (snooze).
  - `rise: True` keeps the scene at night until `from`, then brings the day (a sunrise with the `sun` prop moving up).
  - Exterior sets with a sky dome are tinted too.
  - For an obvious night after a cut, add a per-camera `grade` (`brightness(0.62) saturate(0.75)`).
- **Tiny people** (actor `scale` 0.11–0.17):
  - A low POV next to a big prop sells the size; a close-up makes them look normal again.
  - A shrink is a `scale` key with `dur`.
  - Inside the `washingMachine` drum, put the hips at local z 0.36–0.40 in the glass dome. `tumble` spins them; `walk`
    without a move is a hamster wheel (the engine warns, but here it is wanted).
- **A flying man.** The `superman` clip lies flat with the face toward the travel direction. Film it with an `ms` track at
  angle −70 to −80. A `cu` on it showed the top of the head.
  - The soda jet is a recoloured `beerStream` (`color`, `r`, `flare`) on the hand, with the can held upside down
    (`rot [π,0,0]`).
  - A speed camera's `flashAt`, timed to the word, plus a `flash` fx: the actor's constant-speed glide is computed so he
    passes the radar head on that word.
- **CCTV footage.** A POV from the camera prop in the far corner, 4 m or more away, lens about 48, `grade` night vision.
  Close above the subject it only shows an arm.
- **Visiting room.** Bars seen edge-on fill the frame; use the `interrogation` table, with the inmate in the prisoner outfit.
- **`stareCamera` is a standing pose.** On an actor sitting on a table it makes him stand up; keep the sitting clip and use
  the expression only.
- **New clips:** `superman`, `shakeCan`, `tumble`, `pointSelf` (index finger on the chest: "moi ?").
- **New props:**
  - `washingMachine`: `spinAt`/`spinRates` (rad/s), `laundry` + `laundryAt`. It vibrates on fast spins; set `shake: 0` to
    stop that.
  - `alarmClock`: `time`/`time2`/`switchAt`/`ringAt`/`stopAt`.
  - `sun`, `securityCam`, `honeyJar`, `nest` (`layAt` list), `perfume`, `jean`.
  - `dustPuff` now takes `once` + `startAt`, for a burst on a word.
- **New presets:** `apiculteur`, `avocat`, `prefet`, `mecPrisonnier`, `mecPyjama`.

## Viral-loop batch (parking, pas, voisin, photo): staging lessons

Working examples: `scripts-fr/parking.py`, `pas.py`, `voisin.py`, `photo.py`. They were written with
`references/viral-loop-fr.md` and run 31-35 s.

- **A man driving.** Use the `car` prop (faces +x, light glass). The driver is a separate actor at `userData.seat`, with clip
  `drive` or `sit`, given the same glide as the car (same `to`, `dur` and `ease`, for example `ease='linear'`).
  - Raise the roof enough: a seated head poked through the first version.
  - In-car close-ups go through the windscreen (`worldAngle` about 65) with `noOcclusion=True`; the occlusion test treats glass
    as a wall.
  - Over a row of parked cars, side tracking shots only see roofs. Use a high plunging POV over the row instead; the same POV
    first and last makes the loop.
- **Paths with height.** `path` points can climb: he walks over a car parked on the pavement (boot, roof, bonnet) and over a
  house roof (back eave, ridge, front eave, ground).
  - Time the visible part with the speed. A slow descent arrives after the next line has started.
- **Cross-section ("dollhouse").** A `floorSlab` (with a swinging lamp and `shakeAt`) at y about 3 over a living room, an upper
  wall panel (a blank `signBoard`), and the party standing on the slab.
  - The collapse is one key on the slab plus the same `to`/`dur`/`ease` glide on every actor and prop standing on it.
  - Split the scene right after the impact. The next scene starts with the slab down and extras added via `crowd`. Crowd
    extras can't move, so they must not exist before the fall.
- **Smiles.** The protagonist's measured `happy` face has a downturned mouth (he never smiles in the footage). The designed
  `grin` (an open smile painted over the measured neutral, labelled "designed" in `face_landmarks.json`) is the one to use. Drawn faces map
  `grin` to `happy`.
- **Counter shots.** A person facing a counter or ticket window has no room for a front close-up: the camera lands inside the
  counter. Leave about 1 m, turn him (`face=20`), or use `angle` ±40.
- **New props:** `car`, `brickWall` (pops up with `scale` keys), `broom` (`grip`; overhead with `rot [π,0,0]`),
  `floorSlab`, `pedometer` (`countAt`/`rate` or a fixed `value`), `rubberStamp`, `stampMark` (transparent red stamp:
  REFUSÉ, RADIÉ), `idPhoto` (`smile`), `photoBooth` (`flashAt`, seat), `mugshotBoard`, `placard`.
- **New set and clip:** `cave` (cellar: low ceiling, bulb, pipes, mattress); `pokeUp` (jabbing the ceiling with a broom, `freq`).
- **Expression `grin`.**
