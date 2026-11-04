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
