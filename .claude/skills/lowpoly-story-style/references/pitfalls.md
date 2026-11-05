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
