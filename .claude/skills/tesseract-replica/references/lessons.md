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
- (tornado) A glTF Model3D with `rotationY` 0 faces -Z, towards a camera at negative Z. -90 faces +X and 180 faces +Z. A
  camera looking along -X has +Z on its left.
- (tornado) The variable Nunito font registers as family `Nunito ExtraLight` with named instances: use style `Black`. Read
  `fonts.json` from the import result rather than guessing.
- (tornado) A light's colour is set on the Light3D item, not inside `emitter`.
- (tornado) 576×1024 raster previews with a dozen imported models took about 16 s each (`render_samples.sh`: 3 samples per
  shot is about 50 s per shot).

- (setup) Scene3D raster on Mesa lavapipe took 55-75 s per 1080×1920 frame for a trivial scene. Budget renders before
  promising a full export.
- (setup) Filmstrip tiles carry index and timecode labels. Comparison frames must come from `tsrct preview` or an export.
