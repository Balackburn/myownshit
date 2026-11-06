#!/usr/bin/env python3
"""build_film.py: « Le ver de terre » rebuilt in Tesseract from the engine's baked shots (shots/SXX.glb + SXX.json): one Scene3D layer
per shot over its time window, the baked clip playing (clipTime keyframes), the camera keyframed per sample, the shot's sun and sky.
usage: python3 build_film.py [--total 22.34] [--out Film.tsrct]"""
import json, math, os, subprocess, sys, glob, argparse
sys.path.insert(0, '/home/user/myownshit/tesseract/01-tornado-replica/build')
from tsx import Doc, ext
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.join(HERE, '.tesseract-work'); os.makedirs(W, exist_ok=True)
T = os.path.expanduser('~/.local/share/Tesseract/bin/tsrct')
ENV = dict(os.environ, TESSERACT_CALLER='agent-skill', TESSERACT_SKILL='tesseract-3d', TESSERACT_HOST='claude', TESSERACT_DISTRIBUTION='standalone-skill')
def tsrct(*a):
    r = subprocess.run([T, *a], capture_output=True, text=True, env=ENV)
    if r.returncode: raise SystemExit(f"tsrct {' '.join(a[:3])} failed:\n{(r.stderr or r.stdout)[:3000]}")
    return r.stdout
ap = argparse.ArgumentParser(); ap.add_argument('--total', type=float, default=22.34); ap.add_argument('--out', default='Film.tsrct'); a = ap.parse_args()
shots = sorted((json.load(open(f)) for f in glob.glob(os.path.join(HERE, 'shots', 'S*.json'))), key=lambda s: s['start'])
P = os.path.join(HERE, a.out)
if os.path.exists(P): os.remove(P)
tsrct('project', 'create', '--project', P)
ed = os.path.join(W, 'editable.json'); tsrct('project', 'checkout', '--project', P, '--output', ed)
d = json.load(open(ed)); d['dimensions'] = {'width': 1080, 'height': 1920}; d['duration'] = a.total; json.dump(d, open(ed, 'w')); tsrct('project', 'commit', '--project', P, '--file', ed)
for s in shots: tsrct('project', 'import-asset', '--project', P, '--file', os.path.join(HERE, 'shots', s['id'] + '.glb'), '--asset-id', s['id'], '--kind', 'model3d')
cv = lambda v: [round(v[0] * 100, 3), round(-v[1] * 100, 3), round(-v[2] * 100, 3)]   # engine metres (Y up, -Z forward) -> scene pixels (Y down, Z in)
ms = lambda t: int(round(t * 1000))
lin = {"type": "linear"}
doc = Doc(1000)
for li, s in enumerate(shots):
    L = 10 + li; start, dur = ms(s['start']), ms(s['duration'])
    sky = '#6AA8E6' if not s.get('indoor') else '#F2E6D2'
    world = {"id": doc.nid(), "background": {"type": "color", "color": ext(sky)}, "light": {"source": {"type": "color", "color": ext('#BCD6F2' if not s.get('indoor') else '#F4EBDD')}, "intensity": 0.5 if not s.get('indoor') else 0.75}}
    doc.add({"type": "createFxScene3DLayer", "compositionId": "main", "layerId": L, "name": s['id'], "pixelsPerMeter": 100, "view": {"id": doc.nid(), "exposure": 0},
             "activeRange": {"start": start, "duration": dur}, "transform": {"anchorPoint": [0, 0], "position": [0, 0], "scale": [100, 100], "rotation": 0, "opacity": 100},
             "world": world, "renderSettings": {"id": doc.nid(), "filmGate": None, "overscan": None, "lightGroups": [], "lightCollections": [], "lightLinks": [], "outputs": [], "previewOutput": None}})
    did, mid = doc.nid(), doc.nid()
    item = {"type": "Model3D", "id": mid, "parentId": None, "name": s['id'], "dataId": did, "castsShadows": True, "receivesShadows": True,
            "transform": {"position": [0, 0, 0], "rotation": {"type": "euler", "order": "XYZ", "orientation": [0, 0, 0], "rotationX": 0, "rotationY": 0, "rotationZ": 0}, "scale": [100, 100, 100]},
            "materialSlots": [], "modelRegionSlots": []}
    if s['animated']:
        item["clip"] = {"animation": "animation:path:shot", "loop": False, "time": 0.0}; item["poseStack"] = [{"type": "clip", "source": {"type": "primary"}}]
    doc.add({"type": "addFxScene3DFragment", "compositionId": "main", "layerId": L, "data": [{"type": "model", "id": did, "name": s['id'], "assetId": s['id']}], "items": [item]})
    if s['animated']:
        doc.add({"type": "setFxAnimator", "compositionId": "main", "target": {"type": "styleProperty", "layerId": L, "itemId": mid, "propertyName": "clipTime"},
                 "animator": {"type": "keyframes", "enabled": True, "keyframes": [{"id": f"ct{L}a", "layerTime": 0, "value": {"type": "float", "value": 0.0}, "easing": lin},
                                                                                  {"id": f"ct{L}b", "layerTime": dur, "value": {"type": "float", "value": s['duration']}, "easing": lin}]}, "dependencies": [], "layerRefBindings": []})
    cam = s['camera']; c0 = cam[0]; tgt = lambda c: cv([c['p'][i] + c['d'][i] * 10 for i in range(3)])
    tid, cid = doc.nid(), doc.nid()
    doc.add({"type": "addFxScene3DLayer", "compositionId": "main", "layerId": L, "item": {"type": "Group3D", "id": tid, "parentId": None, "name": "cam target", "transform": {"position": tgt(c0)}}})
    hfov = math.degrees(2 * math.atan(math.tan(math.radians(c0['fov'] / 2)) * s['aspect']))
    doc.add({"type": "addFxScene3DLayer", "compositionId": "main", "layerId": L, "item": {"type": "Camera3D", "id": cid, "parentId": None, "name": "Camera", "transform": {"position": cv(c0['p']), "relationships": {"constraints": [
        {"type": "aim", "id": doc.nid(), "target": {"id": doc.nid(), "target": {"type": "item", "item": tid}, "offset": [0, 0, 0], "offsetSpace": "local"}, "up": [0, 1, 0], "upSpace": "world", "forwardAxis": "positiveZ", "influence": 1}]}},
        "lens": {"type": "angle", "projection": {"type": "perspective", "angleOfView": round(hfov, 3)}}}},
        {"type": "setFxScene3DActiveCamera", "compositionId": "main", "layerId": L, "cameraItemId": cid})
    moving = any(c['p'] != c0['p'] or c['d'] != c0['d'] for c in cam)
    if moving:
        for iid, f in ((cid, lambda c: cv(c['p'])), (tid, tgt)):
            doc.add({"type": "setFxAnimator", "compositionId": "main", "target": {"type": "styleProperty", "layerId": L, "itemId": iid, "propertyName": "position"},
                     "animator": {"type": "keyframes", "enabled": True, "keyframes": [{"id": f"k{L}_{iid}_{k}", "layerTime": ms(t), "value": {"type": "vector3", "value": f(c)}, "easing": lin} for k, (t, c) in enumerate(zip(s['times'], cam))]},
                     "dependencies": [], "layerRefBindings": []})
    sd = (s.get('sun') or {}).get('direction', [0.5, 0.7, 0.5]); sun_from = [c0['p'][i] + sd[i] * 40 for i in range(3)]
    sid, stid = doc.nid(), doc.nid()
    doc.add({"type": "addFxScene3DLayer", "compositionId": "main", "layerId": L, "item": {"type": "Group3D", "id": stid, "parentId": None, "name": "sun target", "transform": {"position": cv(c0['p'])}}})
    doc.add({"type": "addFxScene3DLayer", "compositionId": "main", "layerId": L, "item": {"type": "Light3D", "id": sid, "parentId": None, "name": "Sun", "castsShadows": True, "color": ext('#FFE2BE'),
             "transform": {"position": cv(sun_from), "relationships": {"constraints": [{"type": "aim", "id": doc.nid(), "target": {"id": doc.nid(), "target": {"type": "item", "item": stid}, "offset": [0, 0, 0], "offsetSpace": "local"}, "up": [0, 1, 0], "upSpace": "world", "forwardAxis": "positiveZ", "influence": 1}]}},
             "emitter": {"type": "parallel", "irradiance": 3.4 if not s.get('indoor') else 2.8, "angularDiameter": 1.2}}})
acts = os.path.join(W, 'actions.json'); doc.save(acts); tsrct('project', 'apply', '--project', P, '--actions', acts)
print('built', P, len(shots), 'shots')
