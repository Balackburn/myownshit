# Installation check (2026-11-04)

The goal was to prove that the CLI edits, previews and exports on this host. It was not a design brief.

- `Check.tsrct` is a 1080×1920, 3 s project made from `.tesseract-work/Check.edits.json` (8 actions, no warnings):
  - a background;
  - an orange card and an Inter Bold title, grouped and sliding in (position keys, opacity keys);
  - a square spinning by script (`return input.time.seconds * 120;`).
- `Check.mp4` is its export: H.264, 1080×1920, 30 fps, 90 frames, through the external FFmpeg backend. It took 12.6 s.
  The decoded frames match the filmstrip (`Previews/Filmstrip.png`).
- `Check3D.tsrct` is the skill's Scene3D starter plus recipe 1: an orthographic camera, an above-front sun and two boxes.
  `Previews/Check3D_raster_vs_pathtracer.png` shows the raster still on the left (1080×1920, 75 s). The path tracer still is on
  the right (a 270×480 copy, 16 samples, `--no-denoise`, 36 s): it shows light grain without the denoiser, as expected.
- Both documents pass `tsrct project check`.
