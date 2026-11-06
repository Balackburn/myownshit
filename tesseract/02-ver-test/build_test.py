#!/usr/bin/env python3
"""build_test.py: one shot of « Le ver de terre » rebuilt in Tesseract Scene3D from the engine's posed scene (shot.glb + shot.json),
1080x1920, camera and sun matched; then preview with raster or the path tracer.
usage: python3 build_test.py [--renderer raster|path-tracer] [--samples N] [--out still.png]"""
import json, math, os, subprocess, sys, argparse
sys.path.insert(0, '/home/user/myownshit/tesseract/01-tornado-replica/build')
from tsx import Doc, ext
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.join(HERE, '.tesseract-work'); os.makedirs(W, exist_ok=True)
T = os.path.expanduser('~/.local/share/Tesseract/bin/tsrct')
ENV = dict(os.environ, TESSERACT_CALLER='agent-skill', TESSERACT_SKILL='tesseract-3d', TESSERACT_HOST='claude', TESSERACT_DISTRIBUTION='standalone-skill')
def tsrct(*a):
    r = subprocess.run([T, *a], capture_output=True, text=True, env=ENV)
    if r.returncode: raise SystemExit(f"tsrct {' '.join(a[:3])} failed:\n{(r.stderr or r.stdout)[:3000]}")
    return r.stdout
ap = argparse.ArgumentParser(); ap.add_argument('--renderer', default='raster'); ap.add_argument('--samples', type=int, default=0); ap.add_argument('--out', default=os.path.join(HERE, 'still.png'))
ap.add_argument('--glb', default='shot.glb'); ap.add_argument('--w', type=int, default=1080); ap.add_argument('--h', type=int, default=1920); ap.add_argument('--project', default='VerTest.tsrct'); ap.add_argument('--no-preview', action='store_true'); ap.add_argument('--sun', type=float, default=3.4); ap.add_argument('--amb', type=float, default=0.5); a = ap.parse_args()
J = json.load(open(os.path.join(HERE, 'shot.json')))
P = os.path.join(HERE, a.project)
if os.path.exists(P): os.remove(P)
tsrct('project', 'create', '--project', P)
ed = os.path.join(W, 'editable.json'); tsrct('project', 'checkout', '--project', P, '--output', ed)
d = json.load(open(ed)); d['dimensions'] = {'width': a.w, 'height': a.h}; d['duration'] = 1.0; json.dump(d, open(ed, 'w')); tsrct('project', 'commit', '--project', P, '--file', ed)
imp = tsrct('project', 'import-asset', '--project', P, '--file', os.path.join(HERE, a.glb), '--asset-id', 'shot', '--kind', 'model3d')
open(os.path.join(W, 'import.txt'), 'w').write(imp)
cv = lambda v: [round(v[0] * 100, 3), round(-v[1] * 100, 3), round(-v[2] * 100, 3)]   # engine metres (Y up, -Z forward) -> scene pixels (Y down, Z in)
doc = Doc(1000); L = 1
world = {"id": doc.nid(), "background": {"type": "color", "color": ext(J.get('sky', '#7FB8E8'))}, "light": {"source": {"type": "color", "color": ext('#BCD6F2')}, "intensity": a.amb}}
doc.add({"type": "createFxScene3DLayer", "compositionId": "main", "layerId": L, "name": "Le ver de terre S01", "pixelsPerMeter": 100, "view": {"id": doc.nid(), "exposure": 0},
         "activeRange": {"start": 0, "duration": 1000}, "transform": {"anchorPoint": [0, 0], "position": [0, 0], "scale": [100, 100], "rotation": 0, "opacity": 100},
         "world": world, "renderSettings": {"id": doc.nid(), "filmGate": None, "overscan": None, "lightGroups": [], "lightCollections": [], "lightLinks": [], "outputs": [], "previewOutput": None}})
did, mid = doc.nid(), doc.nid()
doc.add({"type": "addFxScene3DFragment", "compositionId": "main", "layerId": L, "data": [{"type": "model", "id": did, "name": "shot", "assetId": "shot"}],
         "items": [{"type": "Model3D", "id": mid, "parentId": None, "name": "scene", "dataId": did, "castsShadows": True, "receivesShadows": True,
                    "transform": {"position": [0, 0, 0], "rotation": {"type": "euler", "order": "XYZ", "orientation": [0, 0, 0], "rotationX": 0, "rotationY": 0, "rotationZ": 0}, "scale": [100, 100, 100]},
                    "materialSlots": [], "modelRegionSlots": []}]})
def aimed(kind, name, pos, target, extra):
    tid, iid = doc.nid(), doc.nid()
    doc.add({"type": "addFxScene3DLayer", "compositionId": "main", "layerId": L, "item": {"type": "Group3D", "id": tid, "parentId": None, "name": name + ' target', "transform": {"position": target}}})
    item = {"type": kind, "id": iid, "parentId": None, "name": name, "transform": {"position": pos, "relationships": {"constraints": [
        {"type": "aim", "id": doc.nid(), "target": {"id": doc.nid(), "target": {"type": "item", "item": tid}, "offset": [0, 0, 0], "offsetSpace": "local"}, "up": [0, 1, 0], "upSpace": "world", "forwardAxis": "positiveZ", "influence": 1}]}}}
    item.update(extra); doc.add({"type": "addFxScene3DLayer", "compositionId": "main", "layerId": L, "item": item}); return iid
c = J['camera']; cp = c['position']; cdv = c['direction']
hfov = math.degrees(2 * math.atan(math.tan(math.radians(c['fov'] / 2)) * c['aspect']))
cid = aimed('Camera3D', 'Camera', cv(cp), cv([cp[i] + cdv[i] * 10 for i in range(3)]), {"lens": {"type": "angle", "projection": {"type": "perspective", "angleOfView": round(hfov, 3)}}})
doc.add({"type": "setFxScene3DActiveCamera", "compositionId": "main", "layerId": L, "cameraItemId": cid})
sd = J['sun']['direction']; sun_pos = [cp[i] + sd[i] * 40 for i in range(3)]
aimed('Light3D', 'Sun', cv(sun_pos), cv(cp), {"castsShadows": True, "color": ext('#FFE2BE'), "emitter": {"type": "parallel", "irradiance": a.sun, "angularDiameter": 1.2}})
acts = os.path.join(W, 'actions.json'); doc.save(acts)
tsrct('project', 'apply', '--project', P, '--actions', acts)
if a.no_preview: raise SystemExit(0)
args = ['preview', '--project', P, '--time', '0.1', '--output', a.out, '--renderer', a.renderer]
if a.samples: args += ['--samples', str(a.samples)]
import time; t0 = time.time(); r = tsrct(*args); print(r.strip()[:600]); print('wall seconds', round(time.time() - t0, 1))
