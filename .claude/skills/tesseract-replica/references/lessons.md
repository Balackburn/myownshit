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
- (tornado) **Probe a colour that won't change.** S14's road never rendered in 20 passes: it lay 1 cm above a huge ground plane and
  lost the depth test in the headless renderer, so the "olive road" I kept grading was bare ground. When tuning a material changes
  nothing, paint it magenta and the suspect neighbour cyan, render one still and read the pixels. Keep coplanar layers ≥ 5 cm apart.
- (tornado) Read pixel colours on the original before grading: its road was exactly the asphalt's base colour (#2B2A2F) while ours came
  out warm because of the scene light. A per-scene neutral `light` override fixed it without touching the shared preset.
- (tornado) Character framing: solving a camera from a guessed head position failed twice (the arm ended in the lens). Move the camera
  along the head-camera line (the head keeps its screen position while its size scales by the distance ratio), then re-aim by the
  pixel offset. Two stills were enough.
- (tornado) **Look for geometry that never shows.** Two props had parts hidden for 20 passes: the road (z-fight, see above) and the
  headstone's arch, turned by +90° instead of -90° so the half-disc sat inside the slab. When a model "looks flat" on screen, check each
  part's orientation in a close still before tuning colours or cameras.
- (tornado) **Read what the background really is.** In S18 the bottom of the frame was clouds, not grass: the turbine and the tornado's
  crown stood above the cloud deck. A camera-locked cloud bank behind the crown fixed the shot (+0.025 SSIM) where moving the camera
  never could.
- (tornado) Measure skin on a close-up, not on the shot grade: the face was too orange (#E8A768 vs #BF966E) while the sky and suit
  matched, so the fix was a skin tint on the cast (the engine multiplies the painted head), not a grade that would shift the whole shot.
- (tornado) Missing-content spans (from `hyperframes diff`) are the best pass planner: each span pointed at one structural miss (S3
  framing, S14 road, S20 framing, S18 sky). Fixing those took the share from 17.9% to 3.4% in six passes while mean SSIM moved little.
- (tornado) **Measure camera tilt per frame, and check the sign.** In S7 I read the horizon off a thumbnail, got it wrong, then tilted
  the camera the wrong way. Detecting the lowest sky row per frame gave the real curve (523 → 543 px, then a whip to all-sky by f240) and
  showed the camera had to look *up* 1.1°, then whip up fast; a single linear tilt could never fit it.
- (tornado) Soft, out-of-focus foreground (grass in front of a close subject) is cheap to fake: wider blades, lighter colour,
  opacity ~0.55 with depthWrite off. It raised S22 by 0.013 where crisp thin blades had lowered it.
- (tornado) **Check the sign of a grid rotation with an edge-orientation histogram.** The aerial town in S8b/S10 had its rows sloping
  up to the right for twenty passes; the original's slope down by ~15°. A magnitude-weighted histogram of Sobel edge angles over a band
  (`edge = (atan2(gy, gx) + 90°) mod 180°`) put the peaks at 12-17° (original) vs 172-177° (ours) in seconds. A ground line at yaw ψ
  projects to a screen slope of about tan ψ · sin(pitch), so 15° on screen at a 45° pitch is a ~20° yaw. The fix was a sign flip, not
  a bigger angle.
- (tornado) Distance fog with a camera that drops 110 m in a shot clears as the camera descends. To keep the veil at the same place on
  screen (crisp bottom rows, white top band), key the fog's near/far over the shot (`fogTo`). Work from the ray lengths: bottom row
  = altitude / sin(pitch + vfov/2), top row = altitude / sin(pitch − vfov/2).
- (tornado) Trails launched near a fast camera sweep the lens. If a missile's start speed is lower than the camera's, the camera
  overtakes its launch point and its old smoke fills the frame as thick wedges. Launch from points far below the frame (~180 m deep),
  give missiles near the camera a start speed above the camera's, and keep their trails short.
- (tornado) Calibrate a material against its rendered lightness with two renders, not a fog estimate. The crater went from L*67 to L*37
  between two colours; a straight line through the two points gave the colour for the original's L*55 at the first try.
- (tornado) Change one size factor at a time. Raising blast size, puff size, glare and flash together made the S12 explosions three
  times too big. Each factor alone was reasonable. A cloud of size S spans about 4.2·S, so size it from the measured pixel width:
  S ≈ width_px · depth / (4.2 · f).
- (tornado) **Score a candidate still against the previous pass's 3D layer, not its delivery.** The delivery carries captions and the
  HUD that the still lacks, which made every new still look worse. Read the same frame from the last 3D layer, mask the caption band,
  and compare band by band (top, middle, bottom). This flagged an S13 re-stage that fit the street lines to within 10 px but lost 0.05 in
  the bottom band: it was reverted before costing a 15-minute render.
- (tornado) A camera solve that fits the lines is not enough when the content differs. The original's S13 town has bigger shells on
  wider lots and a denser smoke forest. Matching the camera alone moved every object off its old place without landing on the
  original's, and SSIM went down.
- (tornado) **Selfie pans:** when the subject holds the camera, the background swings while he stays in place. Orbit the camera
  around his head by the pan angle, turn the actor by the same angle with a `face` key, and lock the handheld prop to the camera
  (`camLock`). In S4 the street's vanishing point jumps from x 325 to 200 in eight frames (f149-f156); a static camera could never
  match either half.
- (tornado) **Match sharpness per shot, and don't let SSIM talk you into blur.** Compare the median Laplacian variance of the original
  and ours above the caption band, shot by shot. Ours was 1.3-4× crisper in fifteen shots and 3-4× blurrier where a long shutter
  smeared a move the original keeps crisp (S1's orbit, S5, S6). A Gaussian blur on every frame raised SSIM in every shot, even the
  already-soft ones: that is SSIM's bias toward blur, not a match. So soften only up to the measured match (a 0.3-0.6 px CSS blur on the
  3D canvas, `soften`), and shorten the shutters the original doesn't show, even though both cost a little SSIM.
- (tornado) A dense element can be scored by size alone: thicker S13 smoke columns raised SSIM monotonically (0.56 → 1.0: −0.013 …
  +0.02) because the original's middle band is mostly smoke. Stop where it still reads like the original (distinct ropes, fire showing
  through), not at the SSIM peak.
- (tornado) **Test with the scoring tool's own metric.** `hyperframes diff` reports ffmpeg's SSIM over Y, U and V (All, weighted by
  plane size), not a grey-level SSIM. A saturation boost that looked right raised luma SSIM in S10 (+0.010) but lowered both chroma
  planes (−0.03), and the shot fell. Score candidates with `ffmpeg -lavfi ssim` on yuv420p. Render base and variant stills through
  the same pipeline (a JPEG still against an H.264 frame carries a −0.003…−0.006 bias), and only then spend a 15-minute render.
  Rejected this way, at a minute each: front-gabled houses in S12 (−0.01), a longer grave mound (−0.01), a camera truck in S22 (−0.03),
  thinner smoke (−0.013).
- (tornado) **In a busy repeated texture, element size is the big lever.** The aerial towns scored low for thirty passes. A/B stills
  on house scale alone moved S8b by +0.02-0.04 and S10 by +0.02-0.03 per frame (0.95/0.82 → 1.3), more than any crater, haze or
  missile change. Measure the repeated element on full-resolution frames (bottom rows and middle rows), set the scale to match, then
  stop: past the measured size SSIM keeps rising only because coarser texture is easier to match.
- (tornado) **A bright element in the wrong place costs more than a missing one.** Fires, flashes and glows that sit elsewhere than
  the original's are scored twice, once where they are and once where they should be. Shrinking S13's flames to 0.72× raised its stills by
  +0.02; S14's flame band 1.6 → 1.0 gave +0.004. Where the element is right (S5's afterburner sits on the original's nozzle), bigger and
  brighter wins instead (+0.007). Pick the size from the A/B, but keep the element visible if the original shows it.
- (tornado) Give the director per-scene framing trims (`camDolly`, `camTruck`, `camPed`, `camPan`, `camTilt`) so framing variants
  are pure JSON edits. A sweep script then renders the base and each variant at three sample times and ranks them by ffmpeg SSIM: about
  25 s per variant, small enough to run while a full pass renders.
- (tornado) **Render from a snapshot of the timeline, never from the file you keep editing.** Pass 48 launched in the same step that
  rewrote the shared JSON (back to the previous pass, for its commit). The renderer read the file a second later and re-rendered the
  previous pass: a 15-minute pass with no change. Copy the JSON to a render-only file before launching, and check the first log
  lines (or a printed list of the scene keys you changed) before trusting the result.
