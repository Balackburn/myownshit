---
name: ce-mec-shorts
description: Write, storyboard and render vertical 9:16 absurdist narrated shorts in French ("Ce mec a utilisé X pour Y…") with a low-poly 3D businessman, deadpan narrator, burned-in captions with highlighted keywords and dry punchlines with French swearing (ce mec, ce con, putain). Use when the user asks for a "ce mec" short, an absurd TikTok/Reels/Shorts video in this style, a new episode, a script in this format, or wants to render/modify one with the absurd-shorts engine.
---

# Ce mec — absurd 3D shorts in French

The pipeline lives in `absurd-shorts/` (Three.js procedural engine + headless renderer + audio).
You write a **JSON script**; the engine builds the characters, sets, camera, captions, voice,
music and SFX, and outputs an MP4 (720×1280, 30 fps by default).

**Default pipeline = director v3** (scene timelines locked to the real ElevenLabs word timings, auto-facing
moves, real dialogue lines, auto-framed cameras with an occlusion solver): read `references/v3-director.md`
and start from `absurd-shorts/scripts-fr/chrono3.py` (short) or `gorille3.py` (long). The sections below
"Workflow" describe the older v2 one-shot-per-sentence model (`render/render.mjs`), kept for legacy scripts.

Read before writing (in this order, only what you need):
0. `references/v3-director.md`: v3 data model, time expressions, camera solver, QA loop, staging rules. **Always.**
1. `references/formula.md`: the 8-beat formula, French language/swearing rules, checklist, premise bank, 10 example scripts. **Always.**
2. `references/scene-json.md`: JSON format + catalogue (presets, clips, expressions, props, sets, creatures, camera presets, FX, SFX). **Always before storyboarding.**
3. `references/style-match.md`: measured style target (sheet + originals → engine parameters), acting rules, Blender notes. Read it before touching the character or the animations.
4. `references/analysis.md`: frame-by-frame analysis of the 5 reference videos (timings, framings, mechanics, character design). Read it when you need to calibrate rhythm or framing, or when the user asks "why".

## Workflow

### 1. Script (text)
- Unless the user gives a premise, propose **3 hooks** (B1) from `formula.md` §4 or invented ones, pick the strongest, and write the 8–11 sentences.
- Apply the checklist in `formula.md` §3. Read it aloud mentally, deadpan. Cut every word that doesn't serve the logic.
- Show the text to the user (one line per sentence, swears included) if they want to approve it; otherwise go straight on.

### 2. Storyboard → JSON
- One sentence = one shot (split a sentence into 2 shots if it holds 2 images). Fill `line` (displayed captions) and optionally `say` (what the voice says, if different).
- For each shot pick: `set`, `actors` (preset/creature + `clip` + `expr` + position), `props`, `camera` (`preset` + `angle` + `push`), optional `fx`/`overlays`/`sfx`.
- **Editing grammar (MEASURED, see analysis.md §6)**: ONE TAKE PER LOCATION. The shots of the same location are chained with `"cut": false`:
  the camera glides (push/pan/tilt/follow) from beat to beat, set/actors/props stay in place. Cut only when the location changes
  (3–5 locations for 20 s). Every take must contain something moving (an object, an animal, the camera).
- **Framing grammar** (from the reference):
  - B1: `medium` with a 3/4 angle (18–25°), the man holding the prop (`hold`).
  - After every absurd beat: **deadpan reaction** = `extremeClose`, angle 0–10°, clip `stareCamera`, push 0.05.
  - Threat / big object: `low` or `wide`. Chase: `full` with `follow` + a large angle (side tracking).
  - Twist: a change of set (court, street, night) + `hold: 0.3`.
  - Tag: static or slow push shot, `hold: 0.8–1.2` (silence at the end).
- 1 silent visual beat per video: a shot with `"line": ""` and `"duration": 0.8`.
- Highlights: `"highlight": ["chat", "plainte"]`.
- Save to `absurd-shorts/scripts-fr/<slug>.json`. Start from `absurd-shorts/scripts-fr/aspirateur.json` (a full working example).

### 3. Visual QA (cheap) before the full render
```bash
cd absurd-shorts && node render/render.mjs scripts-fr/<slug>.json --no-tts --stills 0.5,2.5,5,8,11,14
```
Open the PNGs in `out/work/<slug>/` with the Read tool. Check: framing (head not cut off unless it's an ECU), captions readable, props in the right place, the right characters. Fix the JSON, then run it again.

### 4. Final render
```bash
cd absurd-shorts && node render/render.mjs scripts-fr/<slug>.json
```
→ `absurd-shorts/out/<slug>.mp4`.
**Voice**: the default is the ElevenLabs voice **"allan tiktok"** (`"voice": {"engine": "elevenlabs", "name": "allan tiktok"}`, resolved by name from the account's library). This needs `ELEVENLABS_API_KEY` in the environment and the `api.elevenlabs.io` host allowed by the network policy. If an ElevenLabs MCP with a text-to-speech tool is connected instead, generate one file per shot with it (shot index = position in `shots`, silent shots skipped), save them as `voice/<slug>/shot00.mp3`, `shot01.mp3`… and set `"voice": {"engine": "files", "dir": "voice/<slug>"}`. The same mode works with your own recorded voice (one take per sentence). Otherwise OpenAI TTS (`OPENAI_API_KEY`), then offline espeak-ng + mbrola (robotic, last resort; say so to the user). `--w 1080 --h 1920` for full HD (slower). Check a few frames of the MP4 with ffmpeg + Read before handing it over.

### 5. Variants / series
- Change the protagonist via `cast.mec.preset` (`lemec`, `lemec_charcoal`, `lemec_brown`, `lemec_beige`, `lemec_glasses`, `boss`, `madame`, `mamie`, `gamin`…) or by overriding `suit`, `tie`, `hair`, `facial`, `glasses`, `hat`.
- Keep the same protagonist across a series (recurring identity), and change sets/institutions from one episode to the next.

## Hard rules
- Original content only: don't copy the reference creator's stories, watermark or name. Reproduce the format, not the jokes.
- Swears: "ce mec" + "ce con" + "putain" (+ at most 1 from the reserve list), never a slur targeting a group of people.
- 16–24 s, 8–11 sentences, the last one short, silence at the end.
- If a needed prop/creature doesn't exist: add it to `absurd-shorts/engine/props.js` / `creatures.js` (box() + palette style, deterministic), check it with `node render/shot.mjs "what=props&list=<nom>&cols=1&cam=1.5,1.2,2.5,0,0.6,0" out/p.png 576 1024`, and **don't** fall back on a text placeholder in the final video.

## Engine files (if you need to extend it)
- `engine/style.js` palette, paper materials, box()/cyl()/textPlane() helpers
- `engine/atlas.js` painted texture atlas for the protagonist (`assets/lemec_atlas.webp`, zones + expressions)
- `engine/face.js` drawn faces (14 expressions) · `engine/human.js` parametric human + rig (17 outfits, 12 hairstyles, 12 hats, 25 presets)
- `engine/animations.js` 50+ pose clips · `engine/creatures.js` animals with googly eyes · `engine/props.js` · `engine/sets.js`
- `engine/director.js` timeline, cameras, captions, overlays, FX · `tools/audio.py` TTS, music bed, SFX, mix · `render/render.mjs` pipeline
- `render/export-models.mjs` exports every character to GLB (`absurd-shorts/models/`) for Blender/Unity.
- `tools/blender/build_rig.py` builds `models/blender/lemec.blend` (armature + 36 actions) from the GLB: `blender -b --python tools/blender/build_rig.py -- models/humans/lemec.glb models/blender/lemec.blend --render out/turnaround.png`.
- `tools/install-skills.sh` installs the companion skills (motion-design, remotion, hyperframes, gsap, earshot, painted-animation, blender-claymation…). Use `motion-design` for timing/easing and `earshot` to listen to the mix before delivering it, if available.
