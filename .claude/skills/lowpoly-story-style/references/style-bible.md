# Style bible (measured on the tornado reference)

## Format and pacing

- Deliver 1080×1920 at 30 fps (the reference circulates at 576×1024; every pixel size below is given for 576 wide, multiply by 1.875).
- 25-50 s. The reference is 28.8 s, 23 shots: a cut every 1.25 s on average, from 11 frames (a whip insert) to 84 frames (the final hold).
- Every sentence gets one or two shots. A cut lands **one frame before** the word that opens the shot.
- The narration never stops: lines sit back to back with 0.06-0.16 s gaps (0.06 before a quote that answers, 0.12-0.16 before a
  punchline). The film ends 0.5-0.9 s after the last word.
- Dialogue is quoted one-liners in the same voice, read more expressively ("That was theft." / « Vos papiers ! »).

## Narration

- Deadpan narrator, short declarative sentences (3-9 words), past tense (passé composé in French).
- Structure: a hook naming the man and the absurd event ("This man lost his dog in a tornado." / « Ce mec manifestait à Paris. »),
  then each line pushes the absurd logic one step (an institution takes it literally: police, army, court, administration),
  escalation to a huge consequence, a twist that turns the tables, and a dry final aside ("Oh, and the dog is dead.").
- 2-3 keywords per line are highlighted in the captions (nouns of the joke, the verdict, the twist).
- The satire targets the institution's absurd logic or the prejudice, never a people.

## Cameras (engine: `lens` = vertical field of view in degrees)

- Lenses 38-74. Close-ups 42-50, mediums 44-50, wides 40-55, low hero angles 50-72, aerials 40-42.
- Default height is low: 0.35-0.9 m looking up at characters; eye level only for face close-ups; aerials 100-700 m.
- **Every shot moves.** Slow push-ins (2-10 % of the distance), trucks, orbits (S1 orbits 160° round the man), tilts that follow the
  action, whips with 2-3 blurred frames. Optical-flow measurement: the reference has 1.3-4× more small (non-camera) motion than a
  first-pass build, so add idle motion to everything that holds.
- Shake 0.008-0.03 for handheld life, 0.05-0.06 for 2-4 frames on impacts (a door slams, a stamp hits).
- Motion blur only inside fast windows: shutter 0.012-0.02 s, 6-10 samples; never on held shots (the reference is crisp there).
- 9:16 is narrow: the horizontal half-angle is atan(tan(lens/2) × 0.5625), 12.8° at lens 44. Two people 2 m apart need ≥ 4.5 m of
  distance. Plan every two-shot with that number.

## Look

- Sky: vertical gradient #62AEE2 (top) → #A7D4EC (horizon), soft white cumulus.
- Sets: pastel facades (#F2F0EA, #B9A6D6, #F2D06B, #9EC7E8, #F2B8C6, #D9604C), white fences, trees as round low-poly blobs, asphalt
  #6E6E72 with dashes, sidewalks #E4D6BE, grass #93BC6A, hills on the horizon.
- Flat-shaded Lambert, paper grain on big surfaces, thin outlines on some props. Nothing glossy.
- Grade per shot as a CSS filter on the 3D layer: `contrast(0.9)`, `saturate(0.85-1.35)` (outdoors 1.05-1.15), `brightness(1.0-1.2)`.
  The reference is bright and soft, never contrasty.
- Softness: Gaussian 0.33-0.62 px at 576 wide (0.6-1.2 px at 1080). Never blur beyond that: it reads as out of focus.

## Characters

- The man: box head (width/height ≈ 0.48: `headWidth 1.3`), slim body (`width 0.82`), navy suit, teal lapels, red tie, stubble;
  on close-ups his skin is tinted toward #B7906A (`tint` on the cast). Cops: navy #1E2D4A uniform and cap; colleagues vary hair and
  moustache.
- Poses are stiff and snappy, with holds; gestures blend in 0.24 s with a little anticipation and overshoot (the director does it).
- Faces carry the acting: neutral, angry, smug, suspicious, shocked, sad, grimace... Blinks every ~3 s. On a quoted line the speaker's
  mouth opens on each spoken word and closes between words (keys from the TTS word timings).
- Things that hold still in the reference still live: tornadoes spin and shed chips, clouds bob, wobble and breathe, turbines turn,
  grass sways, flames flicker.

## Effects and props

- Pop-ins: signs, stamps, documents and price tags scale 0 → 1 with `outBack` in 0.18-0.35 s and settle with a small tilt.
- Rain: thin translucent streaks (8-10 mm wide, opacity 0.5), never thick white bars.
- Explosions: puffs that grow fast (0.15-0.3 s) inside dark smoke, a short flash; debris flung outward.
- Trails and streaks are unlit white (MeshBasicMaterial) so they read on any background.

## Text layers (HyperFrames, never inside the 3D)

- Captions: Nunito 900, 32 px (60 at 1080), white #FEFEFC, 7 px stroke #1C252A (13 at 1080) painted under the fill, shadow
  0 2px 3px rgba(0,0,0,.35), keywords #D88168. Centred, top at 812 of 1024 (79 %). Groups of 2-4 words, at most 22 characters, cut at
  punctuation and never after a small word ("le", "une", "à"...). Each group appears on its first word (−0.03 s) and stays until the
  next: hard cuts, no fades, no pop.
- Title card (one per key beat, 1-3 per film): navy #203447 card 521×114 px at (24, 75), white Poppins 600 69 px with a faint glow.
  It drops from above with the measured spring: y −200, −153, +56.5, +29, +4.5, −20, −32, −30, −19.5, −7.5, +1, +4.5, +2.5, −1.5, −5, −7,
  −7.5, −5.5, −3.5, −1, 0 px on 21 consecutive frames, tilt settling at 1.27°.
- HUD (lock-on): white brackets that zoom in and track, amber #F7C837, orange #F79544, then red #E92E2B; a diamond on the target;
  a red tag (Roboto 700) scaling in with `back.out(2)` and blinking off for 2 frames.

## Sound

- Whole mix −16 LUFS integrated, LRA 2-3 LU, true peak ≤ −1.5 dBTP.
- Narration carries the loudness (alone about −16.5 LUFS).
- Music: a steady pad without a strong beat about 15 dB under the voice (≈ −31 LUFS); loop a clean section with equal-power
  crossfades; fade in 0.3 s, out 0.8 s.
- Effects only on visible actions: impacts and slams, whooshes on whips, beeps on the HUD, rain while it rains (about −28 LUFS
  integrated, peaks near −6 dBFS).
