# Style match: originals vs character sheet vs our engine

Method (from the "2.5D motion studio" course): every value is labelled **MEASURED** (read from a
frame or the file), **ESTIMATED** (by eye) or **DECISION** (our creative choice). Check anything
you build on against the frames listed.

## File / timing
| item | value | label |
|---|---|---|
| resolution / fps | 576×1024, 30 fps (we render 720×1280 or 1080×1920) | MEASURED (ffprobe) |
| motion cadence | **on ones**: 2% duplicate frames in the run (V4 0.2–2.2 s) and the pigeon flight (V1 14.8–16.4 s) | MEASURED (frame-diff) |
| cuts | hard cuts, no transitions; V5 has 22 detected cuts in 27.9 s (≈ 1.3 s/shot) | MEASURED (scdet) |
| captions | 1–4 words, centred at 65–82% of the height, salmon keyword | MEASURED (frames) |
| narrator | median F0 110 Hz, pauses 0.25–0.4 s | MEASURED (audio) |

## Character, the target (sheet + V1/V2 frames)
| part | target | label | where in the engine |
|---|---|---|---|
| head | tall box W/H 0.36 (sheet) to 0.43 (V1 2.6 s); chin slightly narrower than the forehead | MEASURED | `human.js` hw 0.235 / hh 0.56, taper 0.9→1.0 |
| face border | thick black ink around the front face panel | MEASURED | `face.js` strokeRect 10 px |
| eyes | small (Ø ≈ 0.13–0.16 W), white with a thick ring and a dot pupil; **left high (0.30 W, 0.32 H), right low (0.66 W, 0.47 H)** | MEASURED (sheet panel 1) | `face.js` L/R, er = 0.078 W |
| brows | thin arcs floating above the eyes | MEASURED | `face.js` brow() lineWidth 4 |
| nose | tiny "w" at (0.47 W, 0.63 H) | MEASURED | `face.js` |
| mouth | short thick bar 0.34–0.66 W at 0.77 H | MEASURED | `face.js` |
| stubble | sparse short **vertical dashes**, lower third + upper lip + jaw | MEASURED (detail panel) | `face.js` 85 dashes |
| hair | black cap, scribbled curly fringe, sideburns; on the side/back a black mass with drips | MEASURED (sheet turnaround) | `face.js` scribbleFringe / sideTexture |
| ear | rectangular block with a notch, set toward the back of the head | MEASURED | `human.js` ear + notch |
| neck | long, ≈ 0.43 × head width | ESTIMATED | `human.js` |
| jacket | navy #1F3550, square shoulders, long (upper thigh), **teal lapel on the character's right only**, navy lapel with an ink edge on the left, **white pocket stroke** on the left chest | MEASURED (V2 0.3 s, sheet front) | `human.js` lapels / pocket |
| shirt / tie | white V; red tie, fairly wide, tapering to the bottom | MEASURED | `human.js` |
| hands | skin "mittens" + white cuffs | MEASURED | `human.js` |
| material | matte, flat-shaded, light paper grain, no specular | ESTIMATED | `style.js` Lambert + grain |
| expressions | neutral, shocked (open trapezoid mouth + teeth), unimpressed (lids at 50%), suspicious (one lid), grimace (rectangle of teeth), worried, smug | MEASURED (sheet row 2) | `face.js` EXPRESSIONS |
| poses | phone to the ear, arms up, hand behind the head, arm out palm up, arms crossed, shrug, hand on chin | MEASURED (sheet row 3) | `animations.js` phone/armsUp/scratchHead/present/armsCrossed/shrug/thinkChin |

## Acting (DECISION, derived from the motion-design skill + course)
- Anticipation 15% / 4 frames, then ease-out-back (~4–8% overshoot), settled in ~0.45 s.
- Overlap: head +3 frames ahead, forearms −2 frames, hands −3 frames.
- "Every move starts with a look": the expression changes 4 frames before the body moves.
- No idle bounce: breathing ≤ 1.5% and a blink every ~3.3 s. Deadpan holds of 10–20 frames after each joke.

## Differences between the sheet and the originals (choose per series)
| point | sheet | originals | our default |
|---|---|---|---|
| eye size | small, both round | medium, one round + one half-closed | small and uneven (sheet) — use `suspicious` for the "half-lid" look of the originals |
| legs | medium | very long | in between (legs 0.49·H, head ×1.07) |
| lapels | one teal | one teal (V2) | one teal (`symmetricLapels: true` for two) |
| background | neutral grey-beige | cream/teal/red sets | sets per scene; `whiteVoid` for sheet-style shots |

## Blender
`tools/blender/build_rig.py` builds `models/blender/lemec.blend` from the GLB: a `LeMec_Rig` armature
(16 bones, stick display), meshes rigidly parented to the bones, 36 `LeMec_<clip>` actions (fake user).
Rendering in this container: Cycles CPU without the denoiser (`use_denoising = False`); no Eevee/Workbench (no EGL).
