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

## Tesseract

- (setup) Scene3D raster on Mesa lavapipe took 55-75 s per 1080×1920 frame for a trivial scene. Budget renders before
  promising a full export.
- (setup) Filmstrip tiles carry index and timecode labels. Comparison frames must come from `tsrct preview` or an export.
