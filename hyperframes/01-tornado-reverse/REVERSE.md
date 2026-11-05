# Replica of the tornado short (HyperFrames)

The person owns the rights to the original. The HyperFrames `reverse start` flow needs a Pro plan, which the account does
not have, so this project is built by hand to the same rules.

- **Canvas:** 576×1024 at 30 fps, 28.8 s, the original's probe.
- **Sound:** the original's own track (`ref.mp4`) plays as one audio over the whole film.
- **3D picture:** `assets/layer3d.mp4` is rendered by the absurd-shorts engine from
  `absurd-shorts/scripts-fr/replica_tornado.py`. Each scene is cut on the original's frames (22 shots).
  - The street is the `replicaStreet` set: pastel townhouses, fences, hills.
  - Props: `voxelDog` (it walks or paddles), `tornado` with 22 rings, `fighterJet`, and the `runway` set.
  - The character is `lemec` with the build `width 0.82, headWidth 1.3, headScale 1.0`. These proportions were measured on
    the original's frontal frames: head W/H ≈ 0.48, narrower shoulders.
- **HTML scenes:**
  - `compositions/captions.html` has the 24 caption groups in Nunito 900, fill #FEFEFC, highlight #D88168, a 7 px dark
    outline and a drop shadow, switched hard at the original's switch frames;
  - `compositions/theft.html` is the THEFT card, dropping in at f110;
  - `compositions/hud.html` is the S8 lock-on HUD. Every key was measured on the original frame by frame: the brackets
    zoom in at f256 (white, #FFFFFF), turn amber (#F7C837) at f282, then orange at f290, then red (#E92E2B) from f291,
    settling on (68,84)-(513,529). The diamond marker tracks the tornado, white outline then filled red. LOCKED scales
    in over f293-f297 and blinks off at f302-f303.
- **Passes:**
  - each pass renders the engine layer (about 3.5 min), then `npx hyperframes render` (about 1 min), then
    `npx hyperframes diff ref.mp4 renders/passN.mp4 --sbs`;
  - the side-by-side video goes to `passes/passN_sbs.mp4` and is shown in the chat.

| pass | mean SSIM | p05 | shots built |
|---|---|---|---|
| 1 | 0.671 | 0.546 | S1-S4 |
| 2 | 0.676 | 0.546 | S1-S7, new proportions |
| 3 | 0.668 | 0.491 | S1-S14: aerial strike, HUD, missiles, hit, explosions, ruins, white flag; new jet and tornado models |
| 4 | 0.685 | 0.492 | S1-S22, all shots built: courtroom dock and handcuffs, judge and gavel, wind turbine, officer and whip, gravestone; flat-topped tornado tabs |
| 5 | 0.685 | 0.492 | S1 reworked: cottages, orbit round his road side, tornado on the road, fast snatch; S4 close selfie with the phone showing the handle |
| 6 | 0.678 | 0.477 | motion blur (shutter accumulation) on fast moves; grade at the original's saturation (per-shot chroma gap ±4); S5 nozzle close-up rebuilt |
| 7 | 0.674 | 0.482 | tornado reads as pale horizontal stripes with a low crown; S2 dog closer; S5/S6 re-aimed; fireball palette; brighter flag; portrait muzzle; empty-content share 22% → 19% |
| 8 | 0.675 | 0.482 | S16 judge rebuilt on the original's composition (bright bench, smaller chair, wall, window, 3/4 judge, gavel on its head): its L* gap halved |
| 9 | 0.674 | 0.484 | per-shot grades calibrated on the measured deltas: every shot within ±3 L* and ±2.6 chroma of the original (most ±1) |
| 10 | 0.670 | 0.460 | aerial grid at the original's house size and rotation, slimmer long-bodied aerial tornado; S12 camera, tornado and blasts (flash then dark smoke) rebuilt |

Pass 3 notes:
- **Chase camera (S8b, S10):** solved from the original (`solve_cam.py`: rim and base rows, rim width, house size; tornado
  scale 9). It is a 50° dive with the jet 24 m ahead (S8) or 40 m ahead (S10), nose down, nozzles facing the camera.
- **Tornado:** stacked bands of jagged teeth, a crown of spikes and pale bands, measured 1.54× taller than wide. Seen from
  above it is a narrow striped body under a flat dark collar with rocks, a tan inner ring and flat tan swirl bands.
- **Mean SSIM:** it fell slightly although the shots are now built: frames that are close in structure but still differ in
  texture and detail score lower than the earlier flat placeholders did.

Still approximate:
- S3 (the explaining pose); S6, S16 and S22 are still 7-14 L* darker than the original;
- `shotstats.py` (scratch tool) gives per-shot L*, a*, b* and chroma deltas, which steer the grade and lighting fixes;
- SSIM caveat: matching a fine texture's scale without aligning it lowers SSIM. The denser house grid looks closer to the original but
  scores lower on S8 and S10. Judge those shots by eye, and use SSIM per shot to rank the work.
- Nunito stands in for the original's rounded caption face;
- the dog and the tornado are hand-built models.
