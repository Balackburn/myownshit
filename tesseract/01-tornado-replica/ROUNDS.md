# Replica rounds

The gap metric comes from `compare.py`: `(1 − SSIM) + ΔE/25 + hist + (1 − edge F1)`, where 0 means identical. Each round
samples 3 frames per shot at 576×1024 against the reference.

## Round 1: pipeline proof (S1, S3 and all captions)

| shot | gap | SSIM | ΔE | edges |
|---|---|---|---|---|
| S3 | 2.765 | 0.612 | 29.0 | 0.201 |
| S1 | 2.534 | 0.652 | 24.1 | 0.262 |

- **Built:**
  - engine GLBs imported into Tesseract (the exporter now expands instances, clamps factors and names unnamed joints);
  - the street from house, fence and tree models; the man walking with the baked `walk` clip; the dog; the tornado;
  - the 24 captions as Tesseract text in Nunito Black, with highlighted words and a dark stroke.
- **Matches already:** caption text, highlight colours, outline, position and switch times.
- **Different, largest first:**
  - **cameras:** ours are 2-3× too far and too high; the reference S1 camera sits low and close, and the S3 camera is a low
    3/4 close-up;
  - **houses:** the reference has 2-storey pastel townhouses tight against the sidewalk; ours are low bungalows;
  - **dog:** the reference dog is voxel with a boxy muzzle and big eyes;
  - **tornado:** much bigger and closer in the reference, with many painted bands;
  - **S3 pose:** hands raised in front of the chest;
  - **THEFT card:** missing;
  - **sky:** the reference has a gradient, clouds and distant green hills.

## Round 2: S1 and S3 cameras, THEFT card, explaining pose

| shot | gap | SSIM | ΔE | edges | change |
|---|---|---|---|---|---|
| S3 | 2.640 | 0.612 | 28.1 | 0.216 | -0.125 |
| S1 | 2.496 | 0.645 | 24.4 | 0.271 | -0.038 |

- **Added:**
  - the THEFT card (2D box and word, dropping in at f110 with a bounce): its timing and place match; it is slightly smaller
    than the reference;
  - a new `explain` clip in the engine (forearms forward, palms up), baked into the GLB;
  - closer, lower cameras.
- **Found:**
  - the S3 camera looks across the road at the houses on the far side, so the street needs houses on both sides (done after
    the round);
  - the man must face camera-left (rotY -130 with that camera);
  - the reference horizon sits at about 0.82 of the height, so the camera is lower and tilted up more.
- **Next:**
  - a 2-storey pastel townhouse model (reference rows: purple, yellow, blue, pink, white, with front gables, shutters and
    porches);
  - the voxel dog;
  - a bigger painted tornado;
  - a sky gradient with clouds and green hills;
  - then block S2 and S4-S22.

## Round 3: townhouses, voxel dog, big tornado, S2 and S4 blocked

| shot | gap | SSIM | ΔE | edges | change |
|---|---|---|---|---|---|
| S4 | 2.827 | 0.535 | 31.9 | 0.319 | new |
| S1 | 2.709 | 0.571 | 28.8 | 0.292 | +0.213 (worse) |
| S2 | 2.586 | 0.775 | 21.5 | 0.110 | new |
| S3 | 2.581 | 0.581 | 28.8 | 0.279 | -0.059 |

- **New engine props:**
  - `townhouse`: a 2-storey pastel house with a front gable, siding, framed windows, shutters and a porch. Exported in 6
    colours through the new `--variants` export option. The street now reads very close to the reference.
  - `voxelDog`: a cube head, black muzzle block and big eyes, with a tongue variant.
  - `tornado` options: rings, taper, top flare and colours. The 22-ring "big" version spins via a script animator.
- **Why S1 got worse:** the camera path does not follow the man.
  - In the reference he walks toward a low camera, then the camera swings to the road side and looks at him in profile with
    the houses behind.
  - It ends behind him as the dog flies into the tornado on the right. Our camera falls behind his actual position.
- **S4:** the composition is close (street behind, houses on both sides). The reference camera is closer:
  - the face sits left of centre, the road is on the right and the phone is at the right edge;
  - our phone hand stops at the shoulder;
  - our face is too orange: the face material is exported unlit, while the reference face is shaded, tan and papery.
- **Next:**
  - S1 camera keyed to the man's real path, with the dog leading on the leash;
  - S4 framing, and a phone attached to the hand;
  - export the faces as lit materials;
  - a global grade layer (lift, desaturate, paper texture);
  - then S5-S8.
