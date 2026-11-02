# Script JSON format (absurd-shorts engine)

A full working example: `absurd-shorts/scripts-fr/aspirateur.json`.

```jsonc
{
  "title": "L'aspirateur",
  "width": 720, "height": 1280,            // optional (default 720×1280), --w/--h override
  "captionWords": 3,                         // max words per caption chunk
  "captionY": 0.68,                          // vertical caption position (0 = top)
  "captionSize": 0.058,                      // font size as a fraction of the width
  "highlightColor": "#E8775F",               // salmon (reference)
  "watermark": "@moncompte",                 // optional, bottom of the frame
  "voice": { "engine": "espeak|elevenlabs|openai", "id": "<voice id>", "speed": 172, "pitch": 32, "gap": 0.12, "rate": 1.1 },
  "music": { "mood": "quirky|tense|sad|night|epic", "vol": 0.09, "seed": 1 },   // null = no music
  "cast": {                                  // persistent actors, reused from one shot to the next
    "mec":  { "preset": "lemec" },                                  // human
    "chat": { "type": "creature", "name": "cat", "opts": { "upright": true, "clothes": "tie" } }
  },
  "shots": [ /* see below */ ]
}
```

## Shot
```jsonc
{
  "line": "Ce mec a utilisé un aspirateur",   // captions + narration ("" = silent shot)
  "say": "…",                                 // optional: narration text if different (e.g. "p*tain" in captions)
  "highlight": ["aspirateur"],                // words in salmon (accent/case-insensitive)
  "duration": 2.0,                            // optional: computed from TTS (+ hold)
  "hold": 0.4,                                // extra silence after the line
  "minDuration": 0.9,
  "set": "livingRoom", "setOpts": {},         // reuses the previous set if omitted
  "lighting": "night",                        // forces lighting: day|interior|night|dusk|savannah|dark
  "actors": [ /* Actor */ ],
  "props":  [ /* Prop  */ ],
  "crowd":  [ { "spec": {"preset":"cop"}, "count": 12, "center": [0,0,-3], "ring": 2.5, "clip": "idle", "seed": 3 } ],
  "camera": { /* Camera */ },
  "fx":       [ { "type": "flash|shake|fadeBlack|fadeIn|blackout|redAlert", "at": 0.2, "dur": 0.3, "amount": 0.04 } ],
  "overlays": [ { "style": "banner|stamp|phone|label", "text": "60 km/h", "sub": "CAMÉRA RADAR / 014", "at": 0, "until": 1.5, "y": 0.35 } ],
  "sfx":      [ "whoosh", { "name": "gavel", "at": 0.6, "vol": 0.6 } ],
  "captionY": 0.72                            // per-shot override
}
```

### Actor
```jsonc
{
  "id": "mec",                       // key in cast (or a new id + "spec")
  "spec": { "preset": "cop" },       // when the id isn't in cast
  "pos": [0, 0, 0], "ry": 0,         // position (m) / Y rotation (degrees; 0 = facing the camera at +Z)
  "to": [2, 0, 0], "moveStart": 0, "moveEnd": 1.5, "moveEase": "linear|inOut|out|in|outBack",
  "ryTo": 90,
  "scale": 1, "scaleTo": 6, "scaleStart": 0.2, "scaleEnd": 1.4, "scaleEase": "inOut",   // grow/shrink (giant ant, sucked-up cat)
  "clip": "handsOnHips", "params": {},
  "expr": "neutral",
  "actions": [ { "at": 0.8, "clip": "startle", "expr": "shocked" }, { "at": 1.4, "clip": "stareCamera" } ],
  "hold": { "name": "leafBlower", "hand": "R", "rot": [0, 0, 0], "scale": 1 },  // prop in hand (humans)
  "talk": true,                      // lips move (neutral expression)
  "lookAt": [0.1, -0.3],             // added head rotation [x, y] (radians)
  "phase": 0                         // animation offset (crowds)
}
```
Creatures accept `clip` (idle, walk, run, flee, fly, hop, peck, sit, talk, celebrate, sleep, angry, eat, grow, carry, point) and `expr`.

### Prop
```jsonc
{ "name": "tornado", "pos": [0,0,-6], "ry": 0, "to": [0,0,-1], "scale": 1, "scaleTo": 2, "opts": { "length": 6 } }
```
Animated props (tornado, helicopter, policeCar, zzz, explosionBurst…) animate themselves with time.

### Camera
```jsonc
{
  "preset": "extremeClose|close|medium|full|wide|extremeWide|low|high|feet",
  "target": "mec" | [x, y, z],       // default: first actor in the shot (point = top of the head)
  "follow": "mec",                   // follows a moving actor (chase)
  "angle": 18,                       // yaw in degrees around the target (0 = straight on, 90 = profile)
  "orbit": 20,                       // degrees of yaw added over the shot
  "push": 0.12,                      // dolly-in (fraction of the distance) over the shot; 0 = static
  "zoom": 1, "dy": 0, "lookDy": 0, "offset": [0, 0, 0], "fov": 40,
  "whip": "left|right",              // whip-pan at the start of the shot
  "shake": 0.02,
  "from": [x,y,z], "to": [x,y,z], "lookAt": [x,y,z], "ease": "inOut"   // explicit camera path (overrides the preset)
}
```
Preset framings: `extremeClose` face (reactions), `close` head+shoulders, `medium` waist up (default narration), `full` full body, `wide` establishing / large object, `low` low angle (threat), `high` high angle, `feet` ground level.

## Catalogue
Generated from the code: `cd absurd-shorts && node render/catalog.mjs` (prints the up-to-date lists).

- **Human presets**: see `catalog.md` (generated). The main one is `lemec` (navy suit, red tie, teal lapels, stubble).
- **Human overrides**: `outfit`, `suit`, `tie`, `lapel`, `skin`, `hair`, `hairColor`, `facial` (stubble|none|mustache|beard), `glasses`, `hat`, `ears` (normal|pointy), `claws`, `build` {height, width, belly, headScale}, `seed`.
- **Expressions**: neutral, blink, surprised, shocked, suspicious, sad, angry, smug, sleepy, scared, happy, disgusted, dead, talk.
- **SFX**: whoosh, pop, thud, ding, siren (French pin-pon), shutter, kaching, scratch, boing, splat, glass, gavel, wind, rotor, click, sting (wah-wah), tada, crickets, step.

See `catalog.md` for clips, props, sets and creatures.
