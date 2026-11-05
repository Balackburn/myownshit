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
