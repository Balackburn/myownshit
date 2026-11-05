# Shot library (absurd-shorts engine, director3)

Engine conventions: metres, Y up. A character faces +Z at `ry 0`; `ry` is in degrees and the facing direction is (sin ry, cos ry).
A camera looking −Z has +X on its right. `lens` is the vertical field of view. Helpers come from `scripts-fr/actu_common.py`
(`act`, `k`, `P`, `HAND_FLAT`, `SIGN_UP`) and the story script (`cam`, `scene`, `talk`, `cut`). Full working examples:
`absurd-shorts/scripts-fr/replica_tornado.py` (the reference, shot for shot) and `scripts-fr/vospapiers_tornado.py` (a new story,
30 shots, every pattern below).

Sets: `parisStreet` (road along Z at x ±5, sidewalks to ±10, Haussmann fronts at ±10.2, trees at x ±6.6 every 26 m, Eiffel tower at
(−8, 0, −175)), `replicaStreet` (the reference's suburb), `runway`, `skyHigh` (cloud deck at y 0), `aerialSuburb`, `grassland`,
`replicaCourt`, `spaceDark`, `brightCell` (bars at z = D/2 − 0.1, corridor wall at z = D/2 + 3.2), `office`, `interrogation`.

Props added for story remakes (`engine/props_vp.js`): `cloudChar` (face, blinks, bob, breathing, `expr` and `rain` keys),
`rain`, `earthGlobe`, `orbitTrail`, `windSwirl`, `barrierGate` (`open` keys with overshoot), `eiffelTower`, `frMap` + `dashRoute`,
`prisonFront` (`sold` key pops VENDU), `noticeBoard` (doc / sign / tag with `popAt`), `haussmann`.

## 1. Hook: the man doing the absurd thing (low, close, moving)

```python
scene('A01', t0, t1, 'parisStreet',
    actors=[act('mec', [7.0, 0, 0], 8, 'holdSign', 'angry', keys=[k(0.0, clip='chant'), k(0.7, clip='holdSign')])],
    props=[P('sign', 'protestSign', opts={'text': 'ON VEUT\nDU SOLEIL'}, scale=1.5, on={'actor': 'mec', 'hand': 'R', **SIGN_UP})],
    cams=[cam(0.0, [5.5, 0.7, 4.1], [6.0, 0.75, 3.8], [6.8, 2.35, -1.0], [6.95, 2.4, -1.0], lens=52, shake=0.02)])
```
The reference opens behind the man and orbits ~160° round him (`orbit_cams` in replica_tornado.py) while he walks.

## 2. The threat arrives (straight up past the character)

Camera 0.35-0.4 m high just in front of him, aimed 3 m up; the threat slides in with `ease='out'` and changes expression on arrival.
```python
P('cloud', 'cloudChar', pos=[11.5, 3.9, -0.8], opts={'expr': [[0, 'grumpy'], [0.7, 'smug']], 'rain': [[0.75, True]]}, scale=1.2,
  keys=[k(0.0, to=[7.3, 3.7, -0.6], dur=0.65, ease='out')])
```

## 3. Face close-up under the consequence

`cam(0.0, [6.95, 1.86, 1.45], [6.98, 1.85, 1.25], [7.0, 1.86, 0], ..., lens=46, shake=0.008)` with a `rain` sheet just in front of
the face and a deadpan expression that turns (`k(0.55, expr='sad')`).

## 4. Reaction + title card

Waist-up, lens 48, the character yells (`talk(line, t0, 'angry')` for the mouth); the card is a HyperFrames scene starting 0.07 s
into the shot and ending one frame before the cut.

## 5. Phone call / selfie

`phoneCall` clip with `phone911` on the right hand, slow push-in at lens 40-42 (the reference S4 orbits the head and locks the phone
to the camera: `camLock` props).

## 6. Authority figure at work (low wide) and its close-up (reverse angle)

Wide: low camera 0.85 m, lens 46, the cop at his post with the subject passing. Close-up: put the camera on the side the cop
**faces** (beside the subject he talks to), lens 42-44, `ry` turned toward the lens. A close-up from behind his back reads as a mistake.

## 7. Map (where it came from)

`skyHigh` with `layer: False`, `frMap` (k = 10 m per degree) and a `dashRoute` that draws in 1.1 s while a small `cloudChar` rides it;
camera at 96-120 m looking down at lens 42, descending.

## 8. Fast travel (tracking with streaks)

Camera and subject move together over 40 m in 1.3 s, `speedLines` alongside, `blur=[[0, dur, 0.012]]`, shake 0.03.

## 9. Stamp / slam insert

Top-down on a document (`noticeBoard` style `doc` lying flat), a `rubberStamp` dropping with `ease='in'` to the impact frame, the
mark popping at impact (`popAt = hit`, `popDur 0.18`), a second camera key at the impact with `shake 0.06`, blur 0.15 s → impact.

## 10. Vehicles (runway, plane, the subject cuffed to it)

`runway`; `plane` (nose +X, wing tip at local (−0.3, −0.35, ±6.5)); compute the wing tip in world space before hanging anything on
it. Take-off: the plane rolls with `ease='in'`, a gust (`speedLines` appearing) rips the subject off, camera whips after it with blur.

## 11. Space / the whole world

`spaceDark`, `earthGlobe` radius 2.2-3, `orbitTrail` radius 1.25× the globe; keep the camera ≥ 6× the radius away in 9:16 so
the globe fits the width.

## 12. Arrest, mugshot, cell

- Arrest: two officers with `cuffOther`, the arrested one `cuffedBack`; camera 4 m away for three people.
- Mugshot: `mugshotBoard` against the back wall, a `placard` floating at chest height (centred), front camera, flash click.
- Cell: `brightCell` with a wall sign; slam = first camera key with shake 0.05 for 0.25 s; through-the-bars close-up at lens 44 with
  the face between two bars.

## 13. Twist reveal (pop-in proof)

The document/sign pops toward the lens (`noticeBoard` `popAt` 0.35, `outBack`), held by or next to the character it belongs to,
framed so its widest text line fits the 9:16 width at that distance.

## 14. Final deadpan hold

A wide or medium with one small loop of motion (rain, bob, blink) and the last pop-in (price tag, gravestone), held 0.5-0.9 s past the
last word.
