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
| 24 | 0.682 | 0.480 | S4 camera solved from the head rows (head height, 0.8 m, tilted up), phone and tornado placed; skin tinted to the original's (face #CB9765 → #B7906A); S18 cloud deck behind a drum-shaped crater crown; S22 arched headstone (the arch was inside the slab), big-eyed dog with its tongue out, thin grass; worst-cell SSIM 0.23 → 0.32 |
| 25 | 0.683 | 0.480 | S11 blast glows as one mass then turns brown-grey (life 0.6, glowShare 1); S13 twisted rope-like smoke columns, the big tornado behind them (grid reads) |
| 26 | 0.683 | 0.480 | S16 gavel and sound block placed in frame (the block sat 20° off-axis, the gavel inside the robe); S15 bigger, paler tornado, cuffs at the original's height; flared crown plates in every street shot (−0.003 per shot: too sparse, made dense in pass 27) |
| 27 | 0.683 | 0.480 | S5 nozzle seen from behind-left with a glowing mouth; S9 jet shows its top, missiles leave at its speed and dive ahead; S17 restaged from the measured rows (camera up 23°, tall narrow tornado, turbine just behind, cuffs outside the body); dense double crown ring |
| 28 | 0.683 | 0.480 | S17 tornado with thin pale stripes on every ring and a lighter body (no lean: the original stands nearly straight) |
| 29 | 0.685 | 0.480 | S22 soft out-of-focus foreground grass (+0.013); S4 round open eyes (neutral face); smaller nozzle glows on the aerial jet |
| 30 | 0.685 | 0.480 | S7: jet wings level, banking as it passes over; camera holds the measured horizon (523 → 543 px), then whips up to all-sky by f240 |
| 31 | 0.685 | 0.480 | S18 turbine planted in the crater, its thick tower rising out of the crown (the flagged S18 frames shrink) |
| 32 | 0.685 | 0.479 | S7 flyover: the jet climbs over the camera to the upper left, banking, ~15 m away; the camera whips up after it with a short blur (S7 0.879 → 0.881) |
| 33 | 0.680 | 0.429 | Aerial town grid turned the other way (−0.33/−0.36 rad: rows now slope down-right ~15° like the original), bigger denser houses with taller walls, pinkish roofs, blue-grey roads; S10 jet seen from behind (14°), level wings, measured path; white missiles with orange flames; S12 blasts on the original's hits (f444/456/468/480). Regression: a crisper near haze darkened the middle bands (S10 0.464 → 0.415, S8b 0.577 → 0.554) and the S14 lean went the wrong way |
| 34 | 0.689 | 0.484 | Aerial veil restored (pass 32's near/far) and keyed through the camera's descent (`fogTo`): band L* within 1-3 of the original at f270-f384 (S10 0.473, best yet); S22 re-laid out from f820 (base 1.28× the stone, taller frame set higher, bigger dog face, stone 49 px right, camera 0.2 m lower and level so the horizon sits at y 490, turbine and tornado small on the horizon: 0.636 → 0.672); S14 lean flipped to the right with the flag moved over (0.786); S11 camera solved from the curb, the walk edge, door tops and the vanishing point (0.4 m up, yawed 38°) |
| 35 | 0.690 | 0.483 | S4 selfie swing: the camera orbits 10.5° about his head at f149-f156 (street vanishing point x 325 → 200) while he turns with it, phone locked to the camera, wider far sidewalk (fence 1.4 m left of the lens), early camera 0.18 m back (head 386 → 472 px): 0.660 → 0.668; S12 blasts reach full size in 0.15 s with a bigger flash: 0.515 → 0.519. Tried and reverted: S13 re-staged from 77 m (fits the street bands, loses the bottom band) |
| 36 | 0.690 | 0.483 | Sharpness matched per shot (median Laplacian variance): a 0.33-0.62 px soften on the over-crisp shots (S2, S3, S14, S17, S20-S22 up 0.001-0.003); motion blur removed where the original is crisp (S1 orbit f12-f28, S5, S6, S8b cloud exit: faithful, −0.001 to −0.004 SSIM); S22 camera tilted down 1.6°, bigger dog face |
| 37 | 0.690 | 0.480 | Aerial crater rebuilt from the f300 crop: one broad cream band, a thick wall of big inner rocks, wide loose ribbons, the dish tilted 11° away (luma SSIM +0.010 in S10); a saturation boost on S8b/S10 cost more in the chroma planes (U/V −0.03) than it gained, so S10 fell to 0.467: reverted in pass 38. The HyperFrames score is ffmpeg's SSIM over Y, U and V |
| 38 | 0.691 | 0.486 | Saturation boost reverted (the chroma planes recover) with the rebuilt crater kept: S10 0.467 → 0.476 and S8b 0.575 → 0.582, both best yet; S10 trails 2× thicker with bigger flame glows; S13 smoke columns thicker (size 0.72 → 0.86): 0.644 → 0.652 |
| 39 | 0.692 | 0.488 | S22 dog portrait frontal and tipped 0.35 rad toward us (its top shows, ears at the top corners), smaller eyes and head (S22 0.672 → 0.679); S11 blast smoke in 90 smaller lumps. Rejected on A/B stills: S12 front gables, thicker S10 trails, a longer grave mound, an S22 camera truck, a bigger S1 tornado |
| 40 | 0.693 | 0.488 | S1 f33-f56 shot low (0.45 m) and tilted up at him from his front-left, like the original (S1 0.699 → 0.709); the empty sky above him is flagged as missing content (the original's big tornado stands to his right: a bigger one behind him lost 0.03-0.05 on stills, so the staging needs a proper solve) |
| 41 | 0.696 | 0.506 | Houses at the original's size, chosen on A/B stills: aerial towns houseScale 0.95/0.82 → 1.3 (S10 0.477 → 0.507, S8b 0.582 → 0.594), burnt S13 shells 1.25 (0.652 → 0.660); worst frame 0.44 → 0.49. Rejected on stills: S12 houses 1.1 (they merge into terraces, unlike the original's detached cottages), S16 nameplate higher, a phone hand in S4, a bigger S1 tornado |
| 42 | 0.696 | 0.510 | S12 houses 1.12× on lots 8.6 m apart (bigger but still detached: 0.519 → 0.526); lighter body for the S19-S22 tornado (+0.002 in S19 and S21). Rejected on stills: denser aerial rows, a wider S17 tornado |

Pass 21-27 notes:
- **Missing content as the planner:** each span `hyperframes diff` flagged pointed at one structural miss: S3 framing, the S14 road, S20
  framing, the S18 sky. Fixing those took the share from 15.6% to 3.4%.
- **Hidden geometry:** two parts never showed in any earlier pass. The S14 road z-fought with the ground plane (1 cm apart), and the S22
  headstone arch was turned into the slab. Probe with flat magenta/cyan colours and read the pixels.
- **Character framing:** S3 and S4 cameras solved from the head's top and chin rows (S4: the camera at head height, 0.8 m away, tilted up),
  not from guessed head positions.
- **Cast colour:** the man's skin is tinted to the original's (measured on close-ups while sky and suit matched).
- **Tornado crown:** a dense double ring of flared plates now, as in the original, instead of castle merlons.

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
