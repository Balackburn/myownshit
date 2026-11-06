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
  a rider's helmet on a bike about 2.3 m. The helper `scratchpad/tools/proj.py` (where a world point lands in the 9:16 frame)
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
