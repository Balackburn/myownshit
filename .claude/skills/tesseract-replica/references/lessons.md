# Lessons from replicas

Add a dated line for each finding you can reuse. Keep the newest at the top of each section.

## Analysis

- (tornado) Frame and histogram differences find hard cuts reliably. Two kinds of transition need a check by eye:
  - fly-over whips (2-3 blurred frames) show up as a cut followed by blur;
  - cloud wipes inside a shot are not detected at all.
- (tornado) Caption-band pixel tests are fooled by white clouds, trails and explosions behind the text. Time captions from the
  word timings instead (each group switches on its first word), then check the switch frames in the comparison.
- (tornado) faster-whisper 1.2.1 with PyAV fails on `av.open(..., metadata_errors=...)`. Decode the audio yourself and pass a
  float32 16 kHz numpy array instead.
- (tornado) Hugging Face rate-limits this shared IP (429). Wait for the time it reports and retry once. The `base.en` model is
  enough for clear English narration.

- (tornado) reverse-any-video's matching rules apply to captions too:
  - size the text from its ink (measure the reference glyph box, then the font size);
  - take caption switch frames from the caption band's pixels, checked by eye;
  - captions cut on and off hard.

  Its HyperFrames `reverse start` flow needs a HeyGen sign-in on the Pro plan, and the right to use the video. Its `diff` and
  `measure` commands work without either.

## Tesseract

- (tornado) The camera aim constraint wants `up: [0, 1, 0]` for an upright picture, even though +Y points down; `[0, -1, 0]`
  renders upside down.
- (tornado) A glTF Model3D with `rotationY` 0 faces -Z, towards a camera at negative Z. -90 faces +X and 180 faces +Z.
- (tornado) Measured with coloured boxes, with the aim constraint's `up: [0, 1, 0]`:
  - a camera looking +Z has +X on its right and -Y at the top;
  - a camera looking +X has +Z on its left (-Z on its right);
  - so a camera looking -X has +Z on its right.

  Work out which side every subject should appear on before placing it.
- (tornado) Render cost on Mesa lavapipe is mostly a fixed cost per frame, not a cost per pixel:
  - an empty Scene3D takes about 9 s per preview, about 12 s with sun shadows;
  - a street with about 70 models takes 24 s; a half-size canvas is no faster, and merging meshes per material saves little;
  - `export` is not faster per frame (34 s at its 720p minimum).

  For playable progress videos, run 2 previews in parallel at 10 fps (`render_video.sh`), and keep full 30 fps exports for
  milestones.
- (tornado) The variable Nunito font registers as family `Nunito ExtraLight` with named instances: use style `Black`. Read
  `fonts.json` from the import result rather than guessing.
- (tornado) A light's colour is set on the Light3D item, not inside `emitter`.
- (tornado) 576×1024 raster previews with a dozen imported models took about 16 s each (`render_samples.sh`: 3 samples per
  shot is about 50 s per shot).

- (setup) Scene3D raster on Mesa lavapipe took 55-75 s per 1080×1920 frame for a trivial scene. Budget renders before
  promising a full export.
- (setup) Filmstrip tiles carry index and timecode labels. Comparison frames must come from `tsrct preview` or an export.

## Engine + HyperFrames track (what actually closed the gap on the tornado replica)

- (tornado) When the target renderer is slow (Tesseract on lavapipe), build the 3D layer in a fast engine (three.js, about 4 fps at
  576×1024 with 4 workers), cut on the reference's frames, and composite text, cards, HUD and the original sound in HyperFrames.
  Score every pass with `npx hyperframes diff REF yours --sbs --json` and send the side-by-side video to the person.
- (tornado) Iterate on **stills**, not videos: render 8-14 stills at measured times, put them next to the reference frames
  (`still_pairs.py`), fix what you see, repeat. Render the full pass only when the stills are right; each still loop is about 20 s.
- (tornado) **Measure before you move a camera.** Overlay a pixel grid on full-resolution reference frames, read the rows and widths
  of 3-4 features (subject top, base, width, a known-size neighbour), then solve height, distance and pitch (`solve_cam.py`). Eyeballed
  cameras were wrong by 2× in distance; the solved camera matched on the first render.
- (tornado) Perspective lies about proportions: a low camera looking up shrinks the top of a tall subject. Measure proportions on a
  frame where the subject is near the frame centre and the camera roughly level, or correct each width by its distance.
- (tornado) Look for the shot's real geometry in the reference before building: in S1 the orbit went round the man's **road** side and
  the houses beside him were one-storey cottages, not the townhouses further down the street. Getting this wrong cost a full pass.
- (tornado) Per-shot colour statistics (`shotstats.py`: mean L*, a*, b*, chroma per shot) find systematic errors at once. Here the
  engine's default grade desaturated every shot (chroma -4 to -20); one grade change fixed 20 shots. Check this before tuning shots.
- (tornado) Motion blur matters on whips, orbits and fly-overs: average 5 sub-frames over a 20-50 ms shutter, only in the moving
  windows. Rotor blur is cheaper as semi-transparent ghost blades lagging the real ones.
- (tornado) HUD and graphic overlays: measure them frame by frame by colour class (white, amber, red pixel runs at least 40 px long)
  to get the box per frame, the colour switch frames and blinks (here LOCKED blinked off for 2 frames). Animate them from those keys.
- (tornado) A prop's yaw in the absurd-shorts director is `ry` in **degrees**; `rot` carries only pitch and roll in radians. Convert
  once in the script so a rotated prop is never silently ignored.
- (tornado) Models made of many small tilted facets read as noise up close (the tornado looked like a pinecone): use flat-topped tabs
  and keep pointed spikes for the silhouette (the crown) only.
- (tornado) Micro-animation is measurable. Use Farneback optical flow, frame to frame:
  - **global median per shot:** gives camera drift, pans and shake (jitter = mean |Δ| of the per-frame median);
  - **median in a subject box:** gives a spin or scroll speed (the tornado's horizontal px/frame).

  The original moved its camera in shots I had built static (S3, S5, S8, S9, S11, S12...), and the spin speed differed per shot (3.6× too
  fast in one, 44% too slow in another). Match these numbers before judging by eye.
- (tornado) Pin the HyperFrames CLI version in every command (`npx --yes hyperframes@X.Y.Z`). An unpinned `npx` grabbed a release the
  registry mirror did not serve yet and the render failed.
- (tornado) **Is a layer sliding or zooming?** Phase-correlate one band of the frame between consecutive frames (`cv2.phaseCorrelate`
  on the top 400 rows). A steady shift (here +160 px/frame, vertical, for 8 frames) means the layer slides as one piece: a camera
  rotation or a screen-locked layer, not a fly-through. In S8 the cloud deck's edge and its texture moved at the same 166 px/frame, so
  a fog trick or a world-space deck could never match it.
- (tornado) For a screen-locked layer inside a 3D shot (a cloud bank the camera punches into, a lens-close foreground), give the prop
  `camLock: true`: its pos, keys and rot are read in camera space (x right, y up, looking down -z) and it follows the camera, shake
  included. Key its edge in pixels: y_px = 512 - f_px * y / depth, with f_px = 512 / tan(fov / 2).
- (tornado) A contrail behind a jet in a locked chase must move with the jet (a cylinder fixed to the nozzles, growing in length).
  A world-space trail streaks under motion blur because the camera flies past it; the original's trail stayed crisp.
- (tornado) **Never read sizes off thumbnails.** On 216 px panels I judged the aerial tornado 20% too big; a 50 px grid on
  full-resolution frames showed it was 30% too small. Measure on full frames with a grid, then project your own geometry through
  your camera (a 30-line pinhole script from the scene JSON) to tune scale and camera path before rendering: the crater width and top
  row then matched within 15 px at three frames on the first render.
- (tornado) Read the shot boundary in the original: the white-out did not belong to one shot. The cloud bank slid in at the end of
  S8a and slid off at the start of S8b (edge rows measured frame by frame), and the jet emerged from it at f260, not from below.
