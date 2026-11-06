# Pitfalls (first stills of a new story, and the replica passes)

Found on the first two still rounds of "Vos papiers" (30 shots) and in 50 replica passes. Check each before the full render.

- **9:16 is narrow.** Two cops 2.4 m apart at 3.9 m with lens 44 fell out of frame. Horizontal half-angle = atan(tan(lens/2) × 0.5625).
- **Close-ups from behind.** A cop barking « Vos papiers ! » was shot from behind his back. Put the camera on the side the character
  faces (reverse angle) and turn `ry` toward it; check `(sin ry, cos ry)` points at the lens.
- **Cameras inside walls.** A camera behind `brightCell`'s corridor wall rendered a blank frame. Know each set's walls.
- **Set props in the way.** Street trees (every 26 m at x ±6.6 in `parisStreet`) and lamps blocked a camera. Pick a z between them.
- **Text wider than the frame.** A deed 0.78 m wide at 1.8 m was cut on both sides. Size boards so the widest line fits the
  frame width at that distance.
- **Overlapping signs.** A pop-in price tag landed on the cell's wall sign. Know where the set already writes things.
- **Thick rain.** 2 cm emissive streaks read as white sticks. Use 8-10 mm translucent streaks.
- **Things that orbit.** A trail looping round the Earth was behind the globe in the sampled still. Sample a moving element at two times.
- **Tiny subjects.** The first hook still had the man small and his sign cut. Frame the hook close (2-4 m) and low.
- **A prop cuffed to a moving thing.** Compute the attachment point in world space (rotate the local point by the prop's yaw) before
  hanging the subject on it.
- **TTS speed setting.** Ignored by `eleven_v4`: use `atempo`.
- **Render from a snapshot.** Regenerating the JSON while a render starts renders the wrong version (it voided a replica pass).
- **Measure, don't eyeball.** Read sizes and positions on full-resolution frames with a grid, never on thumbnails (a 30 % error on
  the replica). Solve cameras with a pinhole projection of known points (`tesseract-replica` lessons).
- **Look for geometry that never shows.** Coplanar layers closer than 5 cm z-fight; parts rotated the wrong way hide inside others.
- **SSIM is not the goal.** It rewards blur and emptiness. Use it to rank shots, then judge structure, motion and framing by eye and
  with the motion map; fix what the viewer sees (missing-content spans first).

## Found on the seven "faits divers" stories (sable, lune, sapin, escargot, grève, colis, heure)

- **The story has to make sense on screen.** The first « Le sable » was rejected: the grain looked like a cloud (a sand-coloured
  `cloudChar`) and a dog appeared for no reason. Show each line literally, keep only characters the narration names, and give the key
  object its real look (a grain of sand is a faceted golden quartz pebble: `sandGrain`, not a character with a face).
- **Check stills at 85 % of each shot, not only 60 %.** Pop-in signs appear late and push-ins drift: « PENTHOUSE », « À VENDRE »,
  « € UNIQUEMENT », a station board's times and two cow clocks were cut at the edge only at the end of their shots.
- **Bold capitals are wider than 0.62 em.** Signs now measure their text (`textBoard`, `sign`, the queue ticket); keep sign text to
  two short lines in 9:16 anyway.
- **Same-colour effects vanish.** A light-blue water jet was invisible against the sky; use a saturated blue with white foam.
  A jet that flies away from the camera is foreshortened to nothing: film it side-on.
- **Comment placement.** A `// comment` pasted mid-line commented out `g.add(jet)`: nothing rendered and nothing errored.
- **Holding things.** With `holdOut` / `showPhone` the right hand is screen-left: turn the actor (`ry` about -35) or move him so the
  hand comes into frame, and attach flat items with `HAND_FLAT` so their face points at the lens (cards, shoes). Small held items
  (trays) read better as free props placed at the hands.
- **Sets bring their own furniture.** `pressRoom` has a podium and two French flags: pass `{'podium': False, 'flags': False}` or
  `{'flag': [...]}` for another country, and split the backdrop words with `|` (`'VENTE|AUX ENCHÈRES'`) or they overlap.
- **The beach was under water.** `seaSurface` ran its waves under the sand up to z = shore + 10; the sea now ends at the foam line.
- **`JUDGE()` is built for the judge.** Re-cast as someone else (an auctioneer) it read as two faces; stage a new shot instead.
- **Documents wider than the frame.** A 0.8 m document filmed from 1.55-1.75 m (lens 42) is wider than the 9:16 frame
  (width = 2 · d · tan 12.2° ≈ 0.43 · d): once its text filled the board, the words ran off both edges. Keep the camera at
  d ≥ (board width + 0.1) / 0.43, about 1.9-2.1 m for a 0.8 m document, at the END of the push-in.
- **One bad shot does not need a full re-render.** Render that shot's frames with `--stills` (t = n / 30), splice them into
  the 3D layer with ffmpeg `trim` + `concat`, check the frame count and that the frames outside the shot are unchanged, then re-run
  only the HyperFrames render (about 3 min instead of 20).

## From the critic review of « Le vélo » (two critics, three rounds: 6.0 → 7.4 → 7.6)

- **Critics sample each shot at 60 % and 85 %.** The gag of every shot (the prop, the reaction, the sign) must be visible
  and readable at both times, not only at the moment of the action. Check the 60 % and 85 % sheets before calling a story done.
- **Keep the subject out of the two text bands.** Captions sit at 76–86 % of the height and title cards at 8–18 %. A padlock,
  a podium number or a bike's body in the caption band is "hidden"; lift it by tilting the camera DOWN (lower look target).
  Faces under a title card get covered: check every shot that carries a card.
- **Calibrate projections on a render.** The characters are tall: a man's head top is about 2.1–2.3 m (2.3 m with a helmet);
  a rider's helmet on a bike about 2.3 m. The helper `scripts/proj.py` (where a world point lands in the 9:16 frame for a camera position, target and lens)
  is reliable once the heights are right.
- **Googly eyes for an object character must sit side by side across its front**, not one behind the other: head-on, the
  bike's eyes read as one ball ("a football"). A 3/4 angle reads best for any object character.
- **The hero must be the biggest, most central figure in its own beats** (the star on the red carpet, the winner on the podium):
  push in or lower the camera; supporting figures frame the edges.
- **Same-colour contrast**: a red bike on a red floor or carpet loses its silhouette. Change the floor (sets take `carpet` /
  `runner` colours now) or the carpet shade.
- **A flash is a radial bloom** (a camera-facing sprite with rays), not a flat disc: discs read as hat brims.
- **Shock face**: the atlas `shocked` mouth (trapezoid with teeth) reads as a grin at phone size; use `surprised` (O mouth,
  wide eyes) for "robbed / stunned".
- **A hanging prop (chain, tag) must hang in world space**: `cutChain` undoes the hand's rotation each frame. A held prop
  attached with HAND_FLAT only stays upright for forearm-forward poses.
- **Never a solid panel in front of a face**: the convertible's windscreen was a solid box and hid the driver; frames + glass.
- **Paparazzi/celebrity beats**: flashes must fire at the sampled times too (bursts all along the shot, a volley on the key word).
- **JS edit trap, again**: appending a `// comment` to a line that continues (`...; g.userData.update = ...`) comments out
  the rest of the line. Put comments only at the real end of a statement line, and run `node --check` after every engine edit.

## From the critic rounds of « La balance » (6.5 → 7.3 → 7.4), « Le sosie », « Le télétravail »

- **Thumbnails lie about placement.** A 180-px sheet tile can put a prop 20 % lower than it is; check placement on the
  full-size still (`out/work/story_X/stills/s_###.jpg`) before re-framing, and trust `scripts/proj.py` once heights are right.
- **Displays that change must read at 60 % and 85 %.** Count-ups land on the spoken number; blinks after a value lands stay
  under 0.3 s (75 ms phases) so a sampled frame never shows a blank display; ghost (unlit) segments at about 4 % alpha.
- **Do not show the twist before it is said.** A sign that carries the punchline (« HORS SERVICE ») stays dark/unlit until the
  word, then boots (flicker 0.3 s) on it, and lives in a close insert that fills about 80 % of the width.
- **No speech bubble where a title card lands** (8–18 %). If the card says the same word, drop the bubble and let the card shout.
- **The payoff prop must be big and must change hands in frame:** at least 10 % of the frame width, at 35–65 % of the height,
  handed over (or eaten) on its word, in a new angle (not a repeat of the previous set-up). End on a tableau that shows the gag
  (character + the prop/sign that makes it), not on a portrait that crops the gag out.
- **Expression range:** `grin` reads as proud/happy; `happy` often reads flat; `angry` reads as straining (holding the breath);
  `surprised`/`shocked` for the fall. Give the man a visible arc (proud → humiliated → outraged) across the story.
- **Over-the-shoulder through close heads fails:** a juror's head 1.3 m from the lens fills a third of the frame. Use a high OTS
  (camera ~1.5 m above the heads) or a 3/4 front angle that keeps the near heads at the frame edge.
- **Background landmarks behind heads** (the Eiffel tower, a lamp post) read as hats or horns; move the camera so they sit in
  clear sky.
- **Wide objects in 9:16** (a winged scale, a 2x2 video grid) cannot be big and whole: shrink the prop or turn it 3/4, and check
  that all four tiles / both wingtips are inside 90 % of the width.
- **Feet that must act** (tiptoe, stepping onto a scale) need the cast option `shoes: True` (boxy shoes around the ankle), a
  side view, and the feet above the caption band.
- **Engine reminders:** a camera segment glides from the previous one only with `cut: False` (+ `glide` seconds); `roll` is in
  degrees; a scene can take `light` overrides (night: low hemi, blue key); a clip can return `headScale` / `flush` (held breath).

## French only: numbers read in English, English words on screen (La balance, Le télétravail)
- The TTS read a line made only of digits and a noun, « 100 kilos. », in English ("one hundred kilos") with the French voice; the same digits inside a longer French sentence were read in French. Check every line before placing it: faster-whisper `detect_language` on each TTS file gives fr/en probabilities (the English lines scored en 0.99; a French line scores fr ≥ 0.9). Decode with ffmpeg to a numpy array if PyAV refuses the file.
- Fix with a `say` field on the line: the voice reads `say` (« Cent kilos. »), the caption keeps `text` (« 100 kilos. »). Both must have the same number of words, because the caption words are mapped 1:1 onto the spoken words' timings. Spell numbers out in `say` whenever a line is short or starts with digits.
- No English words on screen either, even common loanwords: CADRE / CHEF, not MANAGER / BOSS; SALLE DE SPORT, not GYM. Check prop defaults too (a call grid had a BOSS tile by default).
- A lone punctuation mark left after removing « » (« hors service ». → "service ." in the TTS text) used to count as an extra word and broke the caption build; the alignment now folds punctuation-only tokens into the previous word. Still put the final period inside the quotes.

## From « Le parapluie » (7.5 / 7.5) and « La file d'attente » (stories 31-32)
- **Keep faces out of the card band, not only bubbles.** Both critics measured the reveal shot: the « LA PLUIE » card (8–18 %) sat on the man's brow and the caption (≈ 76–83 %) on the cloud's face. On a carded shot, frame the head at 22–40 % and the gag object at 45–72 %: a wider, lower camera (frame top about 0.28 × frame height above the face).
- **Short TTS lines get misheard.** « Deux heures. » alone came back as « douze heures » (fr 0.70) and « Toute la nuit. » scored fr 0.59; « Puis deux heures. » / « Puis toute la nuit. » scored 0.95+. Give one-to-three-word lines a lead-in word, and re-run the faster-whisper check (transcript + language) after every regeneration.
- **Every « partout » beat needs a witness.** A list of places with the man alone in each reads as "the world never reacts": give each shot one reacting bystander inside the frame (a passer-by dry under a red umbrella, a colleague staring, a cinema row turning round in the screen light).
- **A dark set needs its own light.** The cinema measured luma 25–43 against 135–162 elsewhere: add a `flickerLight` (cool, 12–14) on the screen side so faces read.
- **Climaxes need texture and debris:** a flat rising plane does not read as a flood. `floodWater` takes `ripples` and `floaters` (parcels, letters, a stool) and has a wavy surface; raise it to the chest of the person in it.
- **The payoff document is a pop-in graphic:** about half the frame width, facing the lens (place it with a screen-space helper at 1.5–1.8 m from the final camera, ry toward the camera), the amount the biggest element, a stamp landing 0.3 s later, and a push-in toward it on its word (`waterBill`).
- **Speech bubbles must sit inside the frame at the speaker's depth:** at 1.4 m a 0.95 m bubble is wider than the frame. Size bubbles at 0.36–0.5 m for close shots and place them just above the speaker's head (not beside it), then check the still.
- **A camera in front of a queue looks through the queue.** For people standing in line, shoot from the side (3/4), never from the front along the line, or the person ahead covers the subject.
- **Aerial shots need a city around the set:** the street set alone shows empty ground from above. `cityBlocks` adds instanced blocks (skip rectangles for the set) and a park; scale the queue figures up (size 1.8) so the line reads as people from 70 m.
- **Prop names are global and the last definition wins silently.** A second `veil` in the props file replaced the one an older story used; grep for the name in every props file before adding one. When splicing code between two markers, search the end marker from the start position (`s.index(end, i)`): a repeated name made one edit duplicate 1 000 lines.
