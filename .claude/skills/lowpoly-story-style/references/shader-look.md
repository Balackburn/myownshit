# The shader look and the natural look

Two light modes share `engine/look.js`: `'shaders'` (Minecraft-with-shaders: hard warm sun, blue shade) and, since « La canicule »
(story 34), `'natural'` (light bounced from the scene, soft shadows, auto exposure), the default for new stories. See the last section.

Since « Le ver de terre » (story 35), new stories render with `Story(name, look='shaders')` (`scripts-fr/story_kit.py`), which writes
`"look": "shaders"` in the script and per-scene `grade: 'none'`, `soften: 0.3`. The engine (`engine/look.js`, wired in `director3.js`)
then retunes each scene's light and renders through a post chain. Older stories keep the flat paper look (no `look` key).

## What it does
- Light (`setupLights`, per scene): a strong warm sun (key 3.0 outdoors, 2.4 indoors, colour `#FFD8A6`), a weaker bluish sky fill
  (hemisphere x 0.62 outdoors, 0.72 indoors), so shade is blue and contrasty; the sun is lowered to 38 degrees (long shadows) unless the set
  gives `userData.sun` (a direction the light comes from) — sets with buildings need one so the playing area is lit: `parisStreet`
  `[-0.35, 0.78, 0.52]` (down the street), `pavillon` `[0.55, 0.62, 0.56]`, `kitchenDay` `[-0.4, 0.62, 0.68]`.
- Post chain (EffectComposer, half-float, 4x MSAA): RenderPass, GTAO (ambient occlusion; sky dome, sprites, particles, glass, cut-outs and
  `userData.noAO` objects are hidden from its G-buffer), light shafts from the sun when it is in frame (screen-space march over the depth
  buffer: sky = far plane), bloom (strength 0.28, threshold 0.92), OutputPass with Khronos neutral tone mapping (keeps the paper hues),
  a grade (saturation 1.12, contrast 1.05, warm highlights / teal shadows, vignette 0.18).
- Outdoors: distance haze (fog from 70 m, horizon colour), a sun disc + glow sprite along the key light, a deeper blue sky (the dome's vertex
  colours are saturated once, never tone-mapped).

## Per-scene controls: `st.shot(..., look={...})`
`sunDir` [x, y, z] (where the light comes from: put it on the side the faces look toward — a face turned away from the sun is a dark blob),
`sun` (key multiplier), `fill` (fill multiplier: 1.3-1.5 for dark interiors), `exposure` (1.08 outdoors by default, 1.12 indoors; 1.4-1.6
for grey rooms like `interrogation`), `sunColor`, `elevation` (max sun elevation in degrees), `haze` false, `hazeColor`, `hazeNear`,
`hazeFar`, `ao`, `bloom`, `shafts`, `sat`, `contrast`, `warm` (0 = no split toning: snow scenes 0.25), `sunDisc` false, `deepSky` false.

## Lessons (Le ver de terre, La canicule)
- Check every shot's light direction against where the faces look; the first stills had three backlit shots (the worm talking to the mec,
  the avocado pleading toward the bench, the mec facing the avocado). Fix with `look={'sunDir': ...}` per shot, not by moving the set.
- Grey interiors read gloomy under the shader light: raise `exposure` and `fill` for those shots.
- Cost: about 4x the flat look on the CPU (SwiftShader): a 22 s story at 1080x1920 takes ~45 min with 3 workers on 4 cores. Don't run other
  renders (stills, critics) in parallel with a full render if you can avoid it.
- A/B tool: `scratchpad/look/ab.sh STORY "t1,t2,t3"` renders old vs shader stills side by side.

## The natural look: `Story(name, look='natural')` (default for new stories)
The user asked for more natural light without a path tracer (Tesseract was too slow and drops the ink outlines). Same post chain, plus:
- A light probe per shot: a cube camera (48 px, half float) captured on the first frame of each scene, in front of the first solid surface the
  camera looks at (raycast; never inside a wall, a fridge or a head), projected to spherical harmonics (sync port of three's
  `LightProbeGenerator`), added as a `THREE.LightProbe`. The bounce takes the set's colours (peach walls warm the faces, snow cools them).
  NaN/Inf texels are skipped (one bad shader texel turned whole frames black) and each texel is capped at 6.
- The probe's strength adapts: `probe` (1.7 indoors, 1.2 outdoors) times `min(1, probeTarget / mean radiance)` with `probeTarget` 0.3,
  so a white kitchen or a snowy street does not wash out.
- Auto exposure (a camera's light meter): a 48x86 linear render, centre-weighted mean luminance, exposure = base x (ref / mean)^0.7
  clamped to [0.7, 1.08] (ref 0.42 indoors, 0.32 outdoors; base 1.32 indoors, 1.14 outdoors). A shot that sets `look={'exposure': ...}`
  keeps that exposure.
- Soft VSM sun shadows (radius 9 indoors, 6 outdoors, 16 blur samples), sky fill x 0.45, Neutral tone mapping, bloom threshold 1.35
  (only lamps and glints bloom), grade lift 0.014 (no milky veil), saturation 1.1 indoors / 1.16 outdoors, contrast 0.98 / 1.04, warm 0.85.
- Per-shot extras: `probe`, `probeTarget`, `probeAt` [x, y, z], `meterRef`, `autoExposure` false, `softness`, `hemi`, `sunN`, `lift`,
  `bloomThreshold`. Debug: `"lookOpts": {"debugProbe": true}` logs the probe spot, its mean radiance, the meter and the exposure per shot.
- Lessons: the mec is about 2.3 m to the top of his head: aim standing shots at y 1.8-1.9. A move with `clip='sitFloor'` reverts to the
  previous clip when it ends (a walk becomes idle: he stands up again): add `then='sitFloor'` (or `then='stiffStand'`) to the key.
