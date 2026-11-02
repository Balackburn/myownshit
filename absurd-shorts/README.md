# absurd-shorts

A procedural low-poly 3D engine that renders **vertical absurdist narrated shorts** (9:16) from a
JSON script: characters, rig and animations, props, sets, camera grammar, burned-in captions with
highlighted keywords, TTS narration, a procedural music bed and SFX. It produces an MP4.

Built to reproduce the *format* of "This man used X to Y…" shorts (deadpan narrator, flat-shaded
toy-like 3D, cream/teal/navy/brick-red palette). It ships with a French writing skill:
`.claude/skills/ce-mec-shorts/`.

## Quick start
```bash
cd absurd-shorts
npm install                     # three.js; Playwright + Chromium must be available (pre-installed here)
sudo apt-get install espeak-ng mbrola mbrola-fr1   # offline French TTS fallback
pip install numpy scipy

node render/render.mjs scripts-fr/aspirateur.json                 # → out/aspirateur.mp4
node render/render.mjs scripts-fr/aspirateur.json --no-tts --stills 1,4,8   # quick QA stills
node render/shot.mjs "what=humans&cols=9&spacing=0.9" out/cast.png 1800 1000  # gallery
node render/export-models.mjs   # → models/**/*.glb (posable rigs, lemec.glb carries 36 clips)
node render/catalog.mjs         # prints every preset/clip/prop/set/creature name
```
Better voices: set `ELEVENLABS_API_KEY` (or `OPENAI_API_KEY`) and the pipeline uses it automatically.

## Layout
| path | what |
|---|---|
| `engine/style.js` | palette, paper-grain Lambert materials, box/cyl/text helpers, easing |
| `engine/face.js` | hand-drawn face textures, 14 expressions, hair/stubble/glasses |
| `engine/human.js` | parametric human + rigid puppet rig (17 outfits, 12 hairstyles, 12 hats, 25 presets) |
| `engine/animations.js` | 50+ procedural pose clips, blending, `applyPose` |
| `engine/creatures.js` | animals with googly eyes + their clips |
| `engine/props.js`, `engine/sets.js` | prop and environment libraries |
| `engine/director.js` | timeline, camera presets, actions, captions, overlays, FX |
| `engine/exporter.js` | GLB export with baked animation clips |
| `tools/audio.py` | TTS (ElevenLabs / OpenAI / espeak-mbrola), word timings, music bed, SFX, mix |
| `render/*.mjs` | static server, renderer, gallery screenshots, model export, catalogue |
| `scripts-fr/` | example episodes (JSON) |
| `models/` | exported GLB models |

Rendering uses software WebGL in headless Chromium (~6 fps at 720×1280), so a 20 s short takes about 2 minutes.
