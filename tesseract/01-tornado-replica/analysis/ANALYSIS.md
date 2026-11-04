# Reference analysis: "This man lost his dog in a tornado"

The reference is a third-party TikTok upload (`tiktok_outofthisworld_9_7704432418710670622.mp4`). It is not committed: only the
measurements and small contact sheets derived from it are. It is the original English series that our `ce mec` engine imitates:
the same low-poly businessman, painted faces, burned-in captions with one highlighted word, and deadpan narration.

The replica is a calibration exercise for our Tesseract pipeline. It is not something to publish. It leaves out the creator's
handle, which is printed on the phone, the judge's bench and the gravestone, and it does not imitate the narrator's voice.

Machine-readable data:

| File | Contents |
|---|---|
| `shots.json` | shots, captions, look |
| `narration_words.json` | word timings from faster-whisper `base.en` |
| `shot_metrics.json` | per-shot Lab colour, saturation, motion |
| `ref_shots_*.jpg`, `ref_cuts.jpg` | contact sheets |

## File

- **Video:** 576×1024 (9:16), 30 fps constant, 864 frames, 28.8 s, H.264 High, yuv420p, BT.709 primaries, sRGB transfer, TV range,
  about 1.39 Mb/s. At this bitrate the blocking is visible in gradients and on fast motion.
- **Audio:** HE-AACv2, 44.1 kHz stereo, about 32 kb/s. Narration plus light sound effects. The narration runs 0.00-28.06 s.

## Structure: 22 shots, cut on the narration

The cuts were found frame by frame from luma and histogram differences, and every cut was checked by eye. The shot list is in
`shots.json`. The edit follows the voice:
- almost every cut lands on the first word of a sentence or clause (3.43 "That", 4.50 "so", 6.53 "The military", 12.87 "It hit",
  14.37 "It also", 16.10 "All", 17.63 "The tornado", 19.47 "It was", 21.60 "Now", 26.00 "Oh");
- other cuts land on a keyword (7.63 "fighter jet", 11.17 "everything", 20.23 "hard labor", 22.33 "wind turbine",
  24.13 "makes sure").

Shot lengths run from 0.47 to 2.8 s, with a median of about 1.4 s. There are two non-cut transitions:
- a motion-blur whip as the jet flies over the camera (frames 240-242);
- a cloud wipe inside S8 (frames 251-257), from the sky to the top-down lock-on view.

| Shot | Time (s) | Content | Camera |
|---|---|---|---|
| S1 | 0.00-1.90 | man walks the dog, the tornado takes the dog | low tracking, fast swing with motion blur |
| S2 | 1.90-3.43 | dog spinning in the tornado wall | close tracking |
| S3 | 3.43-4.50 | "That was theft.", THEFT card drops in | medium, low angle, static |
| S4 | 4.50-6.53 | phone call | selfie close-up |
| S5 | 6.53-7.03 | afterburner nozzle | extreme close-up |
| S6 | 7.03-7.63 | fuselage, US AIR FORCE | fast dolly tail→nose |
| S7 | 7.63-8.10 | take-off, fly-over | wide, then whip |
| S8 | 8.10-10.43 | climb, clouds, top-down lock-on HUD | follow, tilt down |
| S9 | 10.43-11.17 | missiles fired | profile |
| S10 | 11.17-12.87 | salvo converges on the tornado | top-down push-in |
| S11 | 12.87-14.37 | hit, fireball | street level, static |
| S12 | 14.37-16.10 | the neighbourhood explodes | high wide |
| S13 | 16.10-17.63 | ruins, fires, smoke ("All of it.") | wide, dark grade |
| S14 | 17.63-19.47 | tornado with a white flag | street level |
| S15 | 19.47-20.23 | tornado handcuffed in the dock | medium |
| S16 | 20.23-21.60 | judge strikes the gavel | low angle |
| S17 | 21.60-22.33 | tornado spins a wind turbine | low wide |
| S18 | 22.33-23.57 | turbine hub, rotor blur | low close |
| S19 | 23.57-24.13 | wide: tiny officer at the base | wide |
| S20 | 24.13-25.53 | officer cracks a whip | medium |
| S21 | 25.53-26.00 | rubble, the tornado keeps spinning | wide |
| S22 | 26.00-28.80 | gravestone with the dog's portrait | slow push-in |

## Captions

There are 24 groups of 1-4 words (listed with times in `shots.json`). Each group switches on the first spoken word of the group,
and the keywords are highlighted.
- **Typeface:** a heavy rounded sans, closest to Arial Rounded MT Bold or Nunito Black (to confirm in the loop). This is not the
  Arial Black our engine uses.
- **Colours:** fill `#FEFEFC`; highlighted words `#D88168`.
- **Outline:** dark `#1C252A`, about 3 px at 576 px wide, with a soft drop shadow.
- **Placement:** centred, block centre at y ≈ 0.81 of the height, cap height about 30 px out of 1024. One line, or two for
  "The tornado / surrendered." There is no animation: the text cuts on and off.

## Look

- **Shading:** flat low-poly forms with soft directional sun shadows and a bright sky fill. The palette is pastel, with gentle
  contrast:
  - mean L* is 60-80 in daylight shots;
  - mean saturation is 0.2-0.38;
  - the sky is a slightly desaturated light blue.
- **Paper texture:** a painted paper or canvas grain covers almost every surface and the sky. The tornado and the suit show
  blotchy hand-painted patches. Ink lines appear only on faces and some edges.
- **Motion blur:** real camera-motion blur on fast moves (S1 swing, S6 dolly, S7 fly-over, the S8 climb) and a rotor blur (S18).
  Static shots are crisp.
- **Grade by act:**
  - daylight suburbia (S1-S12): L* 59-78, b* from -16 (sky) to +18 (lawns);
  - ruins (S13-S14): L* 28-40, near-neutral;
  - courtroom (S15-S16): warm white;
  - grassland (S17-S22): green-biased, a* about -13.
- **Light effects:** additive bloom on the flames, explosions and afterburners. Debris chips (red, white, brown) circle the
  tornado in most shots.

## Assets

| Asset | Status in our engine | Plan |
|---|---|---|
| businessman (walk, gesture, phone, reach) | `lemec`, measured face and atlas | export GLB with baked clips |
| voxel dog (tan, black muzzle, big eyes, red collar and leash) | `dog` creature, to compare | adjust, then export |
| tornado (stacked tapered rings, painted grey-green, debris) | `tornado` prop | compare and retexture |
| pastel townhouses, picket fences, trees, road, hills | `house`, `fence`, `tree`, `bush`, sets | export, instance for the aerial grid |
| fighter jet (grey, roundels, nozzles, landing gear) | missing (only an airliner `plane`) | new model |
| missiles and smoke trails, afterburner flames | `rocket`, `flame` (partial) | new FX |
| explosion fireball, smoke, debris | `explosionBurst` | compare |
| burning ruins, smoke columns, burnt trees | missing | new |
| white flag | `flag` | export |
| courtroom, judge with wig and glasses, gavel | `courtroom` set, `judge` preset, `gavel` | export |
| giant handcuffs | `handcuffs` | export, scaled |
| wind turbine | missing | new model |
| police officer, whip, rocks | cop preset, `rock`; the whip is missing | new whip |
| gravestone, framed dog portrait, flowers, dirt mound, grass | `tallGrass`, `grassPatch`; the rest is missing | new |
| THEFT card, HUD brackets, LOCKED tag, captions | none | Tesseract 2D layers |

## How to replicate

1. Make the assets in the three.js engine (it already matches this series) and export them as GLB with baked clips. Import them
   into Tesseract as Scene3D models.
2. Build each shot as its own Scene3D layer in one composition, with its `activeRange` set to the measured frames. Captions, the
   title card and the HUD are 2D layers on top.
3. Match each camera from the contact sheets (lens, height, path, timing). Then match the lighting, then the grade and the paper
   texture.
4. Render the same frames as the reference at 576×1024 and compare. The skill `tesseract-replica` does this: SSIM, ΔE (Lab),
   histograms, an edge map, and a motion curve per shot. Fix the largest difference first, then repeat.
5. Known limits:
   - Tesseract renders on the CPU here, at about 1 min per raster frame at 1080×1920.
   - The path tracer's denoiser is unavailable here.
   - The creator's handle is left out.
   - Any narration uses our own voice.
