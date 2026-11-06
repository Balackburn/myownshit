# Rendering a story with Tesseract (path tracer) on this CPU-only machine

Measured on « Le ver de terre » (22.3 s, 13 shots), 4 cores, no GPU (lavapipe Vulkan), Tesseract CLI 0.5.0.

## Pipeline (tesseract/03-ver-film)
1. `node export_shots.mjs <story.json> shots 15` — the engine's `exportShotGLB(si, {fps})` (engine/director3.js) bakes each shot:
   transforms sampled at 15 fps, static meshes merged by material (a few draw calls), moving meshes flattened with world
   position/quaternion/scale tracks (scale ~0 while hidden), multi-material meshes split by group (the heads: the face is one of six
   materials), a mesh whose texture changes (face expressions, blinks, lip flaps) split into one mesh per texture shown by a stepped
   scale track, instances expanded, quaternions normalised (Tesseract rejects non-unit keys). Sprites, particles and lights are dropped.
   About 1 s per shot.
2. `python3 build_film.py --total <s>` — one Scene3D layer per shot over its window (pixelsPerMeter 100; engine metres (x, y, z) ->
   scene pixels (100x, -100y, -100z)), the baked clip (`animation:path:shot`) driven by clipTime keyframes, the camera keyframed per
   sample with an aim target, `angleOfView` = the engine's horizontal FOV (2·atan(tan(vfov/2)·9/16)), a parallel sun aimed like the
   engine's key, sky colour as the world background + world light. The .tsrct is ~100 MB: keep it out of git.
3. Export: `--renderer path-tracer --samples 2 --max-bounces 2 --diffuse-bounces 1 --specular-bounces 1 --transmission-bounces 2
   --no-denoise --resolution 720p --fps 15`, split into two processes by `--start-frame/--frame-count` (`--start-ms` cannot be combined
   with `--frame-count`); Linux needs `--encoder-backend external-ffmpeg-command --ffmpeg-path /usr/bin/ffmpeg`.
4. `post_film.sh` — concat, hqdn3d denoise, lanczos to 1080x1920, a touch of saturation/contrast, 30 fps, then the story's HyperFrames
   project copied with the new `assets/layer3d.mp4` for captions, cards and the mix.

## Costs and limits
- Path tracer, one static shot, 1080x1920, 16 spp: 134 s/frame. Animated shots at 720p, 4 spp, default bounces: 39 s (garden) to
  74 s (courtroom) per frame. With 2 spp and 1-2 bounces: ~22 s in the courtroom, about the same look. 335 frames (15 fps): ~1.5 h.
- Tesseract's raster renderer is slower here than the path tracer (~26 s/frame whatever the resolution; ~100 s with unmerged geometry).
- The denoiser's weights download from captions-cdn.xyz directly (the CLI ignores HTTPS_PROXY), which fails in this sandbox; rendering
  needs `--no-denoise`, so denoise in post. Redirecting the domain at the system level was refused by the safety rules: do not retry.
- What is lost from the engine look: ink outlines (dropped from the export), sprites (mist, steam, snow), the shader look's grade.
