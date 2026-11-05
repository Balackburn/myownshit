# One-pass production

Paths are relative to the repo root. Work files go in a scratch folder; only sources and finals are committed.

## 1. Script

- Remaking an existing short: transcribe it locally (no upload):
  `npx --yes hyperframes@0.9.13 transcribe audio16k.wav -m small -l fr --json -d WORK` (whisper.cpp; `small` for French).
  Fix the obvious misspellings by hand.
- Write `lines.json`: `[{"id": "L01", "who": "N"|"C", "text": "...", "hl": ["mot", "clé."]}, ...]`. `C` = a quoted line (same voice,
  expressive settings). Keep the punctuation the captions need; « » are stripped for the TTS.

## 2. Narration (ElevenLabs, voice from `VOICE` in actu_common.py)

```bash
export ELEVENLABS_API_KEY=...   # from the person's environment only
```
Per line: `tools/audio3.py`'s `tts_ts(text, VOICE, VOICE['narrator' or 'character'], previous_text, next_text)` returns mp3 bytes
and character timings (see `hyperframes/02-vos-papiers` history: `tts_vp.py`). The `speed` voice setting has **no effect** on
`eleven_v4`: to tighten the film, time-stretch each line with `ffmpeg -af atempo=1.05-1.10` and divide the timings by the factor.

## 3. Timeline

`python3 scripts/place_narration.py lines.json tts/ timeline.json` places the lines back to back (gaps in the script's `GAP`,
default 0.10 s), keeps word times, adds a 0.84 s tail. Copy it next to the story script (`scripts-fr/<story>_timeline.json`).

## 4. Shot plan and engine script

Copy `scripts-fr/vospapiers_tornado.py`: it loads the timeline, cuts one frame before chosen words (`cut('L10', 3)` = before the
4th word of L10), offers `talk()` for lip flaps and sets per-shot grade and softness. Plan 1-2 shots per line, 1.0-2.4 s each, using
`references/shot-library.md`. Give every shot one moving element besides the camera.

## 5. Stills loop (2-3 rounds, ~2 min each)

```bash
node render/render3.mjs scripts-fr/<story>.json --timed --w 576 --h 1024 --stills t1,t2,...   # one still per shot at 60 %
```
Tile them into one sheet and fix framing (see `pitfalls.md`) until every shot reads. Re-render only the shots you changed.

## 6. Full render (from a snapshot)

```bash
cp scripts-fr/<story>.json scripts-fr/<story>_render.json   # never render the file you are still editing
node render/render3.mjs scripts-fr/<story>_render.json --timed --w 1080 --h 1920 --workers 4 --out out/<story>_3d.mp4
```
About 1.4-1.7 fps at 1080×1920 with 4 workers (45 s ≈ 15 min).

## 7. Sound

`scripts/mix.py` (edit its cue list): narration placed from the timeline, a music bed looped from a clean section of a licensed or
owned stem (for these films: the tornado reference's own background, separated from its voice with MDX-Net, see
`hyperframes/01-tornado-fr/tools/separate_mdx.py`), synthesized effects on the visible actions. Targets: mix −16 LUFS, peak ≤ −1.5 dBTP.

## 8. HyperFrames composition

`python3 scripts/build_hf.py timeline.json hyperframes/<NN-story> --cards "A04:AGRESSION,A08:VOS PAPIERS"` writes the captions and
one composition per card; copy `hyperframes/02-vos-papiers/index.html` for the root (1080×1920, layer3d video, audio, card hosts
0.07 s after their shot starts, captions host). Then:
```bash
npx --yes hyperframes@0.9.13 check --json        # fix errors; the craft "closing line" warning can point at a HUD tag
npx --yes hyperframes@0.9.13 snapshot --at ...    # look at captions, cards and the first and last frames
npx --yes hyperframes@0.9.13 render -o renders/<story>.mp4 --fps 30
```

## 9. QA before sending

- Loudness of the render's audio (ebur128): −16 ± 0.5 LUFS.
- Contact sheet of one frame per shot: every subject in frame, no camera inside a wall, text readable.
- `scripts/motion.py` against a reference in the same style (or the previous version): shots with near-zero residual motion freeze.
- Send the MP4, then commit the sources.
