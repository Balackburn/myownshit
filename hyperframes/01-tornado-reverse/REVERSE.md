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
  - pin the CLI (`npx --yes hyperframes@0.9.13 ...`): an unpinned `npx hyperframes` fetched a version the registry mirror did not
    serve yet and failed;
  - each pass renders the engine layer (about 5 min), then `npx hyperframes render` (about 1 min), then
    `npx hyperframes diff ref.mp4 renders/passN_delivery.mp4 --sbs`, the delivery file being re-encoded like the original
    (`libx264 -profile:v high -b:v 1380k`; flat areas of the original measure 2-5× smoother than our 5.5 Mb/s render);
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
| 11 | 0.670 | 0.460 | S13 smoke columns from every row with fire in each shell; S15 tornado smaller and leaning (bench visible); S22 push-in distance; S4 reframing tried and reverted |
| 12 | 0.671 | 0.461 | micro-animation from optical flow: tornado spin per shot, camera shakes, pans and tilts; S2 wall streaming; S6 dolly direction; empty-content share 16% |
| 13 | 0.670 | 0.461 | S1 leash (engine tethers: a cord between two moving anchors), dog walks from behind to ahead; S2 open mouth and dangling leash |
| 14 | 0.674 | 0.469 | S3 staging (3/4 facing left, forearms out, head to camera, distant houses); delivery encode at the original's bitrate (H.264 High, ~1.4 Mb/s) |
| 15 | 0.675 | 0.469 | S12 blasts at the original's frames (f445/458/469/480), positions projected from screen to ground; S16 framing |
| 16 | 0.675 | 0.468 | S19/S21 tornado: dark smooth body with wide pale spiral bands wrapped tight; S17 layout; S22 lower mound |
| 17 | 0.675 | 0.468 | S4 skeptical expression and head turn, phone against the cheek (a lower camera aim was tried again and scored worse) |
| 18 | 0.675 | 0.468 | judge and officer with the painted lemec face like the original; judge glasses as a 3D prop; officer path kept left of centre |
| 19 | 0.674 | 0.463 | S8 rebuilt from measurements: locked chase with a contrail fixed to the jet, a camera-locked cloud bank sliding 166 px/frame that swallows the jet (f250) and slides off in S8b (jet emerges at f260); aerial crown is a rock crater sized on grid reads; missing content 17.9% → 15.5% |
| 20 | 0.678 | 0.479 | distance haze on the aerial shots (bands within ~2-6 L*); S10 camera fitted to the crater (45°, squat tornado), jet from above with banking, ~50 missiles incl. a wing launch; THEFT card at the original's size, font, spring bounce and tilt |
| 21 | 0.679 | 0.480 | S3 camera moved in to the original's framing (head size and position from grid reads; body 3/4, face to camera); S12 camera solved from the house rows, horizon and tornado, side-gabled cottages packed on a 7.6 m pitch, muted roofs; missing content 15.6% → 11.9% |
| 22 | 0.679 | 0.480 | S14: the road had never rendered (1 cm above the ground: z-fight), now asphalt with dashes at the original's colour; camera tilt 18.6° as measured, closer V-shaped tornado with broken pale stripes, bigger flames, neutral light; missing content 11.9% → 5.6% |
| 23 | 0.678 | 0.480 | S20 camera at the officer's measured size and place, turbine behind him, lighter tornado with tan swirls; S18 crater crown under the turbine; missing content 5.6% → 3.4% |

Pass 19-20 notes:
- **Engine:** `camLock` props live in camera space (screen-locked layers inside a 3D shot: the cloud bank); `rotTo` keys rotate props
  (the S10 jet banks); `cloudCurtain` is a self-shaded bank of lumps; the jet carries an optional contrail fixed to its nozzles; the
  tornado has an aerial `crater` crown (dish, inner and outer rock rings, cream bands).
- **Measured, not eyeballed:** the cloud edge rows per frame, its slide by phase correlation, the crater width/top/bottom/base rows on
  50 px grids, then the camera fitted by projecting our own geometry (S8b end point pulled back 20%, S10 refit to a 45° view).
- **SSIM caveat again:** the real cloud lumps sliding off scored lower than the old flat white-out on f258-f272 (pass 19), although they
  match the original; the haze in pass 20 brought S8b above its pass-18 score anyway.

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
