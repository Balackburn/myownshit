# Ready-made 3D models from sand3d (search, build, use)

When a story needs an object the engine does not have (a key, a padlock, a van, a toaster…), look for it in the sand3d datasets before
modelling it by hand. sand3d (Sandflow, https://github.com/Sandflow-ai/sand3d, Apache-2.0) writes 3D objects as short Python programs
over Blender's `bpy`; its datasets on Hugging Face hold about 100 000 such programs (CC BY 4.0):

| source | rows (train) | what |
|---|---|---|
| `objaverse` | 64 642 | everyday objects from Objaverse/Sketchfab: the one to search first |
| `cad` | 23 363 | mechanical parts from public CAD sets |
| `articraft` | 8 737 | articulated objects (joints declared) |
| `simready` | 2 194 | NVIDIA SimReady assets |
| `automate` | 780 | mechanical assemblies |

Each row: `entry` (the object's name and the function that builds it, e.g. `key`, `toolbox`, `van`), `family` (category, e.g.
`vehicle`, `container`, `fastener or hardware`), `program`, a `render`, `f_score` (fidelity to the source, 1 = best), `n_joints`,
`license`, `source_license`, `attribution`, `license_status`.

## The tool: `scripts/sand3d_models.py`

```bash
T=.claude/skills/lowpoly-story-style/scripts/sand3d_models.py
python3 $T find --entry key --n 12 --sheet /tmp/keys.jpg          # exact object name; look at the sheet, pick a row
python3 $T find --like van --family vehicle --n 12 --sheet /tmp/vans.jpg
python3 $T search "french delivery van" --sources objaverse        # full text (noisier: "key" also finds keyboards)
python3 $T get objaverse 4643                                       # -> absurd-shorts/assets/models/key-objaverse-4643/
python3 $T build absurd-shorts/assets/models/key-objaverse-4643     # -> .../model.glb (metres, Y up, front +Z)
python3 $T credits absurd-shorts/assets/models/key-objaverse-*      # attribution lines for the description
```

- `install` (automatic on the first `build`) makes a venv at `$SAND3D_VENV` (default `/root/.venvs/sand3d`): Python 3.13 + `bpy` 5.2,
  about 400 MB, with `uv`. The system Blender (4.0) is too old for sand3d (it needs bpy 4.5 or 5.2).
- The programs are code from the internet. `build` refuses anything but `import sand3d as s3d` and `math`: no file, system, `eval`,
  dunder or private-`s3d` access; then it runs the program in an isolated process (`python -I`, a temporary working directory, a time
  limit). Never run a dataset program any other way, and never relax the check to make one pass: pick another row.
- The Hugging Face dataset viewer API has outages (HTTP 500/502/504, "authentication check failed"), sometimes for an hour. Build the
  local index once per session: `python3 $T index --sources objaverse` (about 80 s: it reads only the name, category, score and licence
  columns of the Parquet files, 28 MB for objaverse, kept in `~/.cache/sand3d_index/`). Then `find` and `search` fall back on it, and
  `get` reads the program and the render straight from the Parquet files (`find --local` skips the API). These commands need pyarrow,
  so they re-run themselves in the sand3d venv.
- Choose on the render sheet, not the name: prefer `f_score` ≥ 0.95, few parts, a clear silhouette at phone size. Check
  `license_status` is `ok` and the licence is CC BY 4.0 (or more open).

## In the engine: the `glbModel` prop

```python
P('key', 'glbModel', pos=[-0.13, 1.5, -6.95], ry=15, rot=[1.4, 0, 0.3],
  opts={'src': '/assets/models/key-objaverse-4643/model.glb', 'size': 0.105, 'outline': 0.0012})
```

- The director preloads every `glbModel` src of the script before the first frame (`engine/models.js`), so frames stay deterministic.
- `size`: the largest side in metres (or `height`: the height). The model is centred on x/z and set on the ground (y = 0 of the prop).
- Restyled by default to the series' look: flat Lambert with the paper grain, each material's own colour kept. `colors`
  `{'#rrggbb': '#rrggbb'}` swaps colours (match the palette), `tint: ['#colour', 0.3]` pulls them toward one; `restyle: false` keeps
  the GLB's materials.
- `outline`: ink outline thickness in metres (constant, safe for off-centre geometry): 0.001-0.002 for hand props, 0.01-0.03 for
  cars and buildings, like the hand-made props.
- Each file uses its own axes (a sand3d screw lies along Z, a key lies in the XZ plane): look at a still before trusting an orientation.
  `lay: true` puts the long side along x (lying; then `ry` spins it on the floor, and ry ≈ 90 points it back at a camera that looks along
  -Z, end-on and invisible); `up: true` stands it along y. `yaw` (degrees) turns the model inside the prop when its front is not +Z.
  Flat objects (keys, cards, coins) lying in the XZ plane stand up with `rot=[1.4..1.57, 0, tilt]`; add π to the tilt if one comes out
  upside down.
- `thick: 2.4` fattens the two short axes: a real-proportion screw is a hair on a phone screen. `stretch: [x, y, z]` scales the file's
  own axes.
- A missing or unreadable GLB renders a magenta cube: look at a still before rendering the film.

## Lessons (Le serrurier, the first story with sand3d models)

- L'armoire: the sand3d screw (objaverse row 21338) reads in the floor close-ups and held up beside a face only with `lay`/`up` and
  `thick: 2.4`; 20 GLB screws for the pile cost nothing noticeable in render time. The dataset's wardrobes were plain boxes, so the
  wardrobe stayed hand-made: pick on the render sheet and keep the hand-made prop when the dataset's version reads worse.

- Three objaverse keys (rows 4643, 18162, 16286) built in about 10 s each, 11-16 KB per GLB, and read far better in the close-up
  than the hand-made keys: real bows, teeth and holes.
- Hanging objects on a hand: the hand's local axes change with the clip (in `lookItem` the hand's +y points up, in a raised arm it
  points down), so an offset that works in one pose hides the object in another. For a held still pose, place the objects in world
  space just under the hand and check the still; attach with `on={'actor', 'hand'}` only when the hand moves, and test the offset.
- Keep a hand-made ring (`keyRing` with `bare: True`) and hang the GLB keys on it: mixing both is invisible once restyled.
- Credits: copy the `credits` lines into the project (`stories7/<story>/credits.txt`) and give them to the person for the post's
  description; CC BY 4.0 asks for the author, the source and the licence.
