# Pipeline — une histoire, du texte final à la publication TikTok

This runbook is for a Claude Code session that receives ONE assigned story (folder name `STORY`, number `NUM`, title `TITLE`, final French text
already written and audited by the parent session) and takes it to a published TikTok post at the series' quality: three critic rounds, a final
pass, a 1080x1920 30 fps final at −16 LUFS. It is exactly how the parent session produced stories 80-86. Read it once fully before starting.

Everything below is run from the repository root unless a `cd` is shown. `$PIPE` is your work dir (drafts, logs, TTS, critic folders), outside
the repo: `export PIPE=/tmp/pipe` at the start of every shell command that uses the pipeline (the scripts default to `/tmp/pipe`).

## 0. Prérequis (fresh container)

- Repository checked out at `/home/user/myownshit` (the skill's `mix.py` adds `/home/user/myownshit/absurd-shorts/tools` to its path; if your
  clone lives elsewhere, `ln -s <your clone> /home/user/myownshit`).
- Node: Playwright and Chromium are pre-installed (do NOT run `playwright install`). The renderer also needs three.js in `absurd-shorts/`:
  `cd absurd-shorts && npm install --no-save three@0.170.0` (only `node_modules/three` is needed; it is git-ignored).
- Python: `python3 -c "import cv2, numpy"` must work; if not: `pip install opencv-python-headless numpy`.
- ffmpeg/ffprobe: `which ffmpeg ffprobe`; if missing: `apt-get install -y ffmpeg`.
- HyperFrames is run through npx, pinned: `npx --yes hyperframes@0.9.13 ...` with `NODE_USE_ENV_PROXY=1 NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt`
  (the scripts set this). It refuses to render under 1 GB free disk.
- Postiz CLI for publishing: `which postiz` (if missing: `npm install -g postiz@2.0.27`).
- ElevenLabs: the key is injected by the network proxy. Always call TTS with `ELEVENLABS_API_KEY=proxy-injected`. Never ask for, print or store a key.
- Check disk first: `df -h /`. Keep ≥1.5 GB free; delete your own drafts and critic `*-frames` folders as you go.

## 1. Ce que la session parent a déjà fait

- Final text: `absurd-shorts/stories7/STORY/lines.json` (entries `{id, who:"N", text, hl}`) and `absurd-shorts/propositions/NUM-STORY.md`
  (each line with its intended staging, cards, running gag). Do not change the text.
- `engine/props.js` already imports and registers `STORY_PROPS` from `engine/props_STORY.js` (a stub exporting `{}` or an empty object). You fill
  `props_STORY.js`; you never edit `props.js` or any other shared engine file.
- The parent gives NUM, TITLE and the Postiz key in your prompt.

## 2. Narration

```
export PIPE=/tmp/pipe
cd absurd-shorts && ELEVENLABS_API_KEY=proxy-injected python3 pipeline/tts.py STORY 2>&1 | grep -v -i voice
python3 ../.claude/skills/lowpoly-story-style/scripts/place_narration.py stories7/STORY/lines.json $PIPE/s7/STORY/tts stories7/STORY/timeline.json --atempo 1.08 --tail 1.3
```
`hl` tokens must equal whitespace-split words of the text, punctuation and elisions included (`l'attaque`, `broyeuses.`).

## 3. Mise en scène (staging)

Model `absurd-shorts/scripts-fr/story_STORY.py` on `scripts-fr/story_place.py` and `scripts-fr/story_feuille.py`:
docstring (English summary, staging, props new/reused, lessons applied), `st = Story('STORY', look='natural')`, `st.plan(...)` with one shot per
line, a `# N: gloss. staging...` comment before each shot (the critic tools read these), project()-based CHECKS printed for every camera, cast in
`st.write(..., extra_cast={...})` — every extra cast entry needs a `preset` (without one it silently becomes the hero's navy suit), sound cues
(`st.cue`; any cue that needs a duration gets one), cards (`st.card`). New props go in `engine/props_STORY.js`; grep the existing `engine/props_*.js`
first and reuse. Check with stills only:
```
bash absurd-shorts/pipeline/stills.sh STORY st1 cams          # one still per camera + sheet -> $PIPE/s7/STORY/st1.jpg
bash absurd-shorts/pipeline/stills.sh STORY st2 "1.2,3.4,5.6" # stills at times
node absurd-shorts/pipeline/prop_smoke_example.mjs $PWD/absurd-shorts/engine   # adapt CASES to your props
```
Engine edits: edit a copy, `cp copy x.mjs && node --check x.mjs`, `python3 absurd-shorts/tools/lint_js_comments.py <file>` (never a `#` or `//`
comment mid-line followed by code), then install atomically (`cp copy engine/props_STORY.js.tmp && mv engine/props_STORY.js.tmp engine/props_STORY.js`).

## 4. Brouillons et revues (three rounds)

Long jobs always run detached, with a separate background watcher; never a foreground `sleep`, never `cmd && setsid ... &` (the whole chain gets
backgrounded):
```
export PIPE=/tmp/pipe; setsid nohup bash absurd-shorts/pipeline/draft.sh STORY 1 > $PIPE/s7/STORY_d1.log 2>&1 < /dev/null & disown
# watcher (Bash with run_in_background=true, timeout 7200000):
until grep -q "_D1_READY" /tmp/pipe/s7/STORY_d1.log 2>/dev/null; do sleep 30; done; cat /tmp/pipe/s7/STORY_d1.log
```
A draft is 480x854, 15 fps, ~25-35 min. `draft.sh` regenerates the json from the .py first, then runs the freeze check and the grey scan.

Round 1 critic folder:
```
mkdir -p $PIPE/critic/specs && cp absurd-shorts/pipeline/spec_example.py $PIPE/critic/specs/STORY.py   # rewrite every field for your story
python3 absurd-shorts/pipeline/tools/make_config1.py $PIPE/critic/specs/STORY.py
python3 absurd-shorts/pipeline/tools/make_critic.py $PIPE/critic/configs/STORY1.py
cd $PIPE/critic/STORY1 && bash build.sh stills && bash build.sh
```
The spec holds STORY, NUMBER, TITLE, CARD_WHAT (card word → what it stamps), NEW, CHOICES, SUMMARY, GLOSS (English gloss per line id), ANIM_GAGS,
ART_FOCUS (see `spec_example.py`).

Rounds 2 and 3: write `$PIPE/critic/configs/STORYN.note` (what changed since the last round, known weak spots, the freeze-check result, and the
sentence « This draft runs at 15 frames a second (to halve the render time); the final film runs at 30. »), then:
```
python3 absurd-shorts/pipeline/tools/round_config.py STORY PREV ROUND DRAFT NUM "TITLE" $PIPE/critic/configs/STORYN.note
python3 absurd-shorts/pipeline/tools/make_critic.py $PIPE/critic/configs/STORYN.py
cd $PIPE/critic/STORYN && bash build.sh stills && bash build.sh
```

### The two critics

With the Workflow tool: `Workflow({scriptPath: "absurd-shorts/pipeline/review-draft.js", args: {name: STORY, round: N, folder: "$PIPE/critic/STORYN"}})`
(the folder as an absolute path), then save `result.reports[i].report` to `$PIPE/critic/STORYN/review_{anim,art}.md`.

Without the Workflow tool: launch two independent Agent subagents in the same message (never one agent for both; neither sees the other's
report), each with this prompt (role = `anim`, then `art`):
> Read `<folder>/prompt_<role>.txt` and follow it exactly. It names `critic-instructions.md`, `brief.md`, `words.md` and the evidence images to
> open (open every image before scoring). Return the whole report as your final message, in exactly this form:
> `Score: x.x` / `Verdict: ...` / `Issues, most important first (at most five): ...` / `Keep: ...` / `Needs the user: ...` / `Viewed: ...` /
> `Not evaluated: ...`.
Save each report to `review_<role>.md`. The animation director judges gags, timing, rig use, holds; the art director judges composition,
readability at phone size, colour, props, caption/card bands, finish.

### Corrections

After each round, one correction pass (a fork/subagent or yourself) that owns only `story_STORY.py`/.json and `props_STORY.js`, works shot by shot
with stills, keeps what the critics list under Keep, keeps shot lengths and the narration, backs up before each change, and ends with a one-still-
per-shot sheet. Then the next draft. Typical scores: round 1 ≈ 5.5-6.5, round 3 ≈ 7.0-7.5.

After round 3: a final pass (safe fixes only), then:
```
bash absurd-shorts/pipeline/mix_test.sh STORY        # must print MIX_OK and about -16 LUFS
grep -n -o -E "'[A-Z][A-Z ]{3,}'" absurd-shorts/scripts-fr/story_STORY.py absurd-shorts/engine/props_STORY.js   # every on-screen word French
```

## 5. Rendu final et contrôle

```
export PIPE=/tmp/pipe; setsid nohup bash absurd-shorts/pipeline/final.sh STORY NUM "TITLE" > $PIPE/s7/STORY_final.log 2>&1 < /dev/null & disown
# watcher: until grep -q FINAL_READY /tmp/pipe/s7/STORY_final.log; do sleep 30; done; tail -8 /tmp/pipe/s7/STORY_final.log
```
~1 h 40 on 4 cores (3D layer with three browsers, then the HyperFrames project and render). Output: `hyperframes/NUM-STORY/renders/STORY.mp4`.
If only the HyperFrames half failed (`PROJECT FAILED` / `HF FAILED` in `$PIPE/s7/queue.log`), fix and run `bash absurd-shorts/pipeline/hf_only.sh
STORY NUM "TITLE"` (5 min) — never re-render the 3D for that.

QA must show: `width=1080|height=1920`, `I: -16.x LUFS`, the HyperFrames check with 0 errors, `dips: none` from the grey scan (or dips you can
explain, e.g. an intentional flash). Then a 14-frame sheet and LOOK at it (no English on screen, faces readable):
```
F=hyperframes/NUM-STORY/renders/STORY.mp4; mkdir -p $PIPE/s7/STORY/sheet; i=0
for t in 1.0 3.5 6.0 8.5 11.0 13.5 16.0 18.5 21.0 23.5 26.0 29.0 32.0 35.0; do i=$((i+1)); ffmpeg -loglevel error -y -ss $t -i $F -frames:v 1 -vf scale=216:384 $PIPE/s7/STORY/sheet/f$(printf %02d $i).png; done
ffmpeg -loglevel error -y -i $PIPE/s7/STORY/sheet/f%02d.png -vf tile=7x2 $PIPE/s7/STORY/final_sheet.jpg
```

## 6. Publication

From `absurd-shorts/`, with the key from your prompt typed inline (never in a file, script, commit, log or memory):
```
POSTIZ_API_KEY="<key from your prompt>" python3 tools/postiz_publish.py --only NUM-STORY --now 1
```
It prints the post id. It also updates `stories7/tiktok_published.json` locally: do NOT commit that file (the parent keeps the ledger; send it the
post id instead).

## 7. Commit, push, report

Commit only your story's own files:
`absurd-shorts/scripts-fr/story_STORY.py`, `absurd-shorts/scripts-fr/story_STORY.json`, `absurd-shorts/engine/props_STORY.js`,
`absurd-shorts/stories7/STORY/`, `hyperframes/NUM-STORY/` (renders/ is git-ignored; never force it), `absurd-shorts/propositions/NUM-STORY.md`.
NEVER commit `tiktok_published.json`, `JOURNAL.md`, `.claude/skills/.../SKILL.md`, `stories7/queue11.sh`, `engine/props.js` or any other shared file,
nor `out/`, renders, TTS mp3s, anything over 100 MB.
Before every commit: `git diff --cached | grep -c -E "sk_[A-Za-z0-9]{8}|<first 8 characters of the Postiz key>"` must print 0 (type the prefix inline from your prompt; never write it in a file). Push only to your own session branch, no PRs.
Then report to the parent session with `send_message` (its id is in your prompt): post id, the three rounds' scores, the final QA line, the
commit hash and branch, and short technique lessons (the parent adds them to the skill; you do not edit SKILL.md).

## 8. Règles qui comptent le plus

Full list: `.claude/skills/lowpoly-story-style/SKILL.md`, sections « Catalogue de gags et techniques » and « Erreurs à éviter ». The ones that
cost most when forgotten:
- `lens` is the vertical field; characters are ~2.3 m tall with the box head; the 9:16 frame is only ~2 m wide at 4-5 m: stage horizontal
  actions in depth (or top-down / high crane).
- Faces and key props above the caption band (77-83 % of the height); heads below the card band (7-18 %) when a card stamps.
- Flat grounds raised ≥5 cm; big ground slabs as no-depth layers; emissive surfaces ≥20 cm above grassland.
- `mat()` caches materials by colour: `unique: true` for anything you animate. `explosionBurst` ignores its start time: use `timedBurst`.
  `flash` at most 3 per second. `reach` takes no face points (`touch` does). A prop on a scaled joint does not inherit the scale.
- Two box heads face to face lose both faces in profile: stage in a V, faces ¾ to camera. Stay ≥20° off thin planes (glass, railings, paper).
- A white sheet or pale prop disappears on pale ground: give it a dark or saturated background.
- One side only for an indicator/lamp gag (both sides blinking = hazard lights). A SpriteMaterial without a radial texture renders as a square.
- No English on screen; numbers spelled out in the narration; no real organisations, brands, insignia or national flags; invented flags checked
  against real ones (orange/white/green or blue with a disc reads as India; red-over-white as Indonesia/Monaco/Poland; a thin mast with a
  crossbar reads as a church cross); hide real-army markings (white stars) with a wrapper prop.
- Darkness at the reference's level: collateral damage said as a detail, nobody shown hurt (people visibly evacuated), no animal hurt.
- Satire targets institutions and their absurd logic, never an ethnicity, religion, nationality, disability, gender or orientation.
- Before a 1 h 40 final, always run `mix_test.sh`.
- Never edit a .sh file that bash is running; never disable TLS verification; never write a secret anywhere.
