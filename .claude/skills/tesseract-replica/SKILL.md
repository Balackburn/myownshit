---
name: tesseract-replica
description: Recreate an existing animated video shot for shot in Tesseract and close the gap in a measured loop. The loop analyses the reference (cuts, word timings, colour, motion), builds an editable .tsrct (Scene3D shots, captions, titles, HUD), renders the same frames, scores the difference (SSIM, ΔE Lab, histogram, edge F1, sharpness), fixes the largest gap and repeats until nothing measurable or visible is left or the user stops. Use when someone asks to reproduce, match, replicate or copy a reference animation's look, timing, models and grade with Tesseract, or to compare a render with a reference.
---

# Replicate a reference video in Tesseract

This skill sits on top of the Tesseract skills; it does not replace them. Read `tesseract-3d` for Scene3D,
`tesseract-motion` for captions, titles and the HUD, and the matching Tesseract references (local operation, native authoring,
Scene3D basics and recipes) before writing actions. `tsrct` is `~/.local/share/Tesseract/bin/tsrct`; in a fresh container,
install it with `tesseract/README.md`.

The replica copies the look, the timing and the craft, never someone else's identity:
- leave out watermarks, account handles and logos printed in the reference, unless the person owns the video and asks for an exact
  copy (then their own handle stays);
- never imitate a real narrator's voice;
- treat the replica as a study, not something to publish.

Store the reference outside git. Commit only the measurements and small contact sheets.

## The loop

1. **Analyse.**
   - Run `scripts/ref_analyze.py REF.mp4 analysis/`. It gives cuts, per-shot Lab colour, saturation, motion, contact sheets and
     word timings from faster-whisper `base.en`; if Hugging Face rate-limits, retry after the wait it reports.
   - Check every cut on `cuts_check.jpg`: whips, flashes and cloud wipes are not cuts, and gradual wipes are missed, so look for
     them on the start/middle/end sheets.
   - Cross-check the cuts with `npx -y hyperframes@latest measure cuts REF.mp4 --json`. It is free, but on the tornado
     reference it missed 3 fast cuts and flagged 3 in-shot events (a title drop, an explosion flash, a whip crack). Trust
     neither tool without looking.
   - Write each shot start as frame ÷ fps rounded down: frame 83 at 30 fps is 2.766666, and 2.767 lands a frame late. Read
     consecutive frames around every change (cut, entrance, exit, flash): sheets sampled every quarter second miss 1-3 frame
     timing and one-frame flashes.
   - Fill `shots.json`. Per shot: frames, camera, subjects, set, effects. Per caption group: text, highlighted words, on/off
     times. Write `ANALYSIS.md`. A worked example is in `tesseract/01-tornado-replica/analysis/`.
2. **Plan the assets.** List each model and say where it comes from:
   - our three.js engine (`absurd-shorts`, exported to GLB with baked clips by `render/export-models.mjs`);
   - a new engine prop or a Blender build;
   - native Scene3D primitives.

   Prefer existing assets that already match the style, and add missing ones to the engine so later episodes reuse them.
3. **Build** one composition at the reference canvas (for example 576×1024 at 30 fps). Put one Scene3D layer per shot, with its
   `activeRange` exactly on the measured frames. Captions, title cards and HUD go in 2D layers on top. Keep one action batch per
   shot in `.tesseract-work/` so a shot can be rebuilt alone.
4. **Render samples.** `scripts/render_samples.sh Replica.tsrct shots.json renders/rN 3 [S1,S3]` renders the same instants that
   `compare.py` samples (3 per shot by default).
5. **Compare.** `scripts/compare.py --ref REF.mp4 --cand-frames renders/rN --shots shots.json --out compare/rN`, or `--cand video.mp4`
   after a full export.
   - Read `report.md`: shots worst first, with a diagnosis per sample.
   - Open `sheet_<shot>.jpg`: reference, candidate, ΔE heat map.
   - Look at the images; the numbers only rank the work.
6. **Fix the largest gap first**, in this order, because each later step is wasted if an earlier one is wrong:
   timing and cuts → framing and camera → models and poses → materials and texture → lighting → grade → motion blur → noise
   and compression. Change one family at a time, then re-render only the affected shots.
7. **Log the round.** Append to `ROUNDS.md`:
   - per-shot gap, SSIM, ΔE and edge F1, with the change from last round;
   - what was changed;
   - what is still different, and why.

   Add every reusable finding to `references/lessons.md`.
8. **Final judge.** At each milestone, export the full video and run `npx -y hyperframes@latest diff REF.mp4 replica.mp4 --sbs`.
   It runs locally without an account, comes from the `reverse-any-video` skill, and writes an original | yours side-by-side
   video. It gives:
   - per-frame SSIM, mean and p05, and the worst 4×4 cell;
   - missed or extra cuts, missing-content spans, and the worst moments.

   Score each caption box by itself with `--drawn x,y,w,h,a-b`: it reports the offset and the ink ratio, where under 1 means
   lighter, thinner or smaller. Its pass marks (mean 0.92, p05 0.85, cell 0.75) are the objective "matches" line.
9. **Repeat** from step 4. Stop when the user asks, or when a round improves no shot and the remaining differences are
   explained as unreachable: codec artefacts, a missing source asset, the narrator's voice, the creator's handle. After the
   visuals, export the full video and run `compare.py --cand` on it, including the audio timing check.

## Fast track: engine layer + HyperFrames (when Tesseract renders too slowly)

On the tornado replica, Tesseract raster cost about 10-60 s per frame on the CPU, which made full passes impossible. This track
closed most of the gap instead. It also runs each pass end to end in about 7 minutes.

- **3D picture:** use the absurd-shorts engine with a timed script (scenes cut on the reference frames, no TTS):
  `node render/render3.mjs script.json --timed --w 576 --h 1024 --workers 4 --out layer3d.mp4`. It renders about 4 fps.
- **Composite:** build a HyperFrames project holding `layer3d.mp4`, the original sound, and the captions, cards and HUD as
  sub-compositions keyed on measured frames. Run `npx hyperframes render`, then `npx hyperframes diff --sbs`. Show the
  side-by-side video to the person after every pass.
- **Loop on stills:**
  1. `render3.mjs --stills t1,t2,...` (about 20 s);
  2. `scripts/still_pairs.py` puts the reference frame next to each still;
  3. fix, then repeat.
- **Measure, don't guess:**
  - `scripts/solve_cam.py` solves a camera from feature rows and widths read on a grid overlay of the reference;
  - `scripts/shotstats.py` prints per-shot L*, a*, b* and chroma deltas, so global grade or lighting errors show up first;
  - read HUD and overlay keys by colour class, frame by frame.
- **Order of fixes that paid off:**
  1. the shot's true geometry (which side the camera is on, which buildings are there);
  2. the camera (solved);
  3. model proportions;
  4. the global grade (per-shot chroma);
  5. motion blur on the fast moves;
  6. details and micro-animation.

## Reading the numbers

`gap = (1 − SSIM) + ΔE/25 + hist + (1 − edge F1)`. 0 means identical. Rough meanings at the reference resolution:
- **edge F1 under 0.35:** the camera, lens or blocking is wrong. Fix this before anything else.
- **edge F1 0.35-0.6:** the poses, proportions or a small camera offset are wrong.
- **ΔE over 10 with good edges:** the materials or grade are wrong. dL/da/db give the direction.
- **histogram over 0.25:** the palette or exposure is wrong.
- **sharpness ratio under 0.6:** too soft. Over 1.7: missing motion blur or paper softness, aliasing, or too crisp.
- **pixel-level limit:** above about SSIM 0.9 with ΔE under 3, what is left is noise, compression and anti-aliasing. Re-encode
  the replica at the reference bitrate before the final comparison.

## Practical limits in the cloud container

- Rendering runs on the CPU (Mesa lavapipe). Iterate on 3 samples per shot, and export the whole video only at milestones.
- The path tracer's denoiser cannot download here: use raster, or path-trace with `--no-denoise`.
- H.264 export needs `--encoder-backend external-ffmpeg-command --ffmpeg-path /usr/bin/ffmpeg`.

See `references/lessons.md` for the findings collected so far.
