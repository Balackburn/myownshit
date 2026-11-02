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
