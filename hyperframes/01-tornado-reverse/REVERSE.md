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
  - `compositions/theft.html` is the THEFT card, dropping in at f110.
- **Passes:**
  - each pass renders the engine layer (about 3.5 min), then `npx hyperframes render` (about 1 min), then
    `npx hyperframes diff ref.mp4 renders/passN.mp4 --sbs`;
  - the side-by-side video goes to `passes/passN_sbs.mp4` and is shown in the chat.

| pass | mean SSIM | p05 | shots built |
|---|---|---|---|
| 1 | 0.671 | 0.546 | S1-S4 |
| 2 | 0.676 | 0.546 | S1-S7, new proportions |

Still approximate:
- S8-S22 are placeholders;
- Nunito stands in for the original's rounded caption face;
- the dog and the tornado are hand-built models.
