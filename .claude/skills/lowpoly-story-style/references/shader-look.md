# The shader look (light like "Minecraft with shaders")

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
