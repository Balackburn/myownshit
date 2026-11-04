"""tsx.py — compact builders for Tesseract action batches (Scene3D shots, captions, cards).

Coordinates follow Tesseract: X right, Y DOWN, Z into the screen, pixels; with pixelsPerMeter 100 one engine metre = 100 px.
Imported glTF models stand upright with their feet at y=0; a model with rotationY 0 faces -Z (towards a camera at negative Z).
Times inside a shot are shot-local frames at 30 fps (converted to layer milliseconds).
"""
import json, math

FPS = 30
IDT = {"anchorPoint": [0, 0], "position": [0, 0], "scale": [100, 100], "rotation": 0, "opacity": 100}


def ms(frames):
    return int(round(frames * 1000 / FPS))


def _hex(h):
    h = h.lstrip('#'); return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def lin(h):
    """sRGB hex -> scene-linear RGB (material inputs)."""
    return [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in _hex(h)]


def ext(h, a=1.0):
    """sRGB hex -> extended-sRGB RGBA (world, lights, 2D colours)."""
    return _hex(h) + [a]


def euler(rx=0, ry=0, rz=0):
    return {"type": "euler", "order": "XYZ", "orientation": [0, 0, 0], "rotationX": rx, "rotationY": ry, "rotationZ": rz}


def ease(kind='linear'):
    if kind == 'linear': return {"type": "linear"}
    if kind == 'hold': return {"type": "hold"}
    if kind == 'out': return {"type": "cubicBezier", "x1": 0.2, "y1": 0.8, "x2": 0.3, "y2": 1}
    if kind == 'in': return {"type": "cubicBezier", "x1": 0.7, "y1": 0, "x2": 0.8, "y2": 0.2}
    if kind == 'inout': return {"type": "cubicBezier", "x1": 0.45, "y1": 0, "x2": 0.55, "y2": 1}
    raise ValueError(kind)


class Doc:
    def __init__(self, start_id=1000):
        self.acts = []; self._id = start_id; self.batches = {}

    def nid(self):
        self._id += 1; return self._id

    def add(self, *acts):
        self.acts.extend(acts)

    def save(self, path):
        json.dump(self.acts, open(path, 'w'), indent=0)


class Shot:
    """One Scene3D layer covering reference frames f0..f1 (inclusive)."""

    def __init__(self, doc, layer_id, name, f0, f1, ppm=100, sky='#A9CFE3', amb_color='#C8DCEB', amb=0.55, fog=None, exposure=0):
        self.d = doc; self.L = layer_id; self.f0 = f0; self.f1 = f1; self.nframes = f1 - f0 + 1
        self.dur = ms(f1 + 1) - ms(f0); self._data = {}
        world = {"id": doc.nid(), "background": {"type": "color", "color": ext(sky)},
                 "light": {"source": {"type": "color", "color": ext(amb_color)}, "intensity": amb}}
        if fog: world["fog"] = {"color": ext(fog[0]), "startDistance": fog[1], "endDistance": fog[2]}
        doc.add({"type": "createFxScene3DLayer", "compositionId": "main", "layerId": layer_id, "name": name, "pixelsPerMeter": ppm,
                 "view": {"id": doc.nid(), "exposure": exposure}, "activeRange": {"start": ms(f0), "duration": self.dur}, "transform": IDT,
                 "world": world, "renderSettings": {"id": doc.nid(), "filmGate": None, "overscan": None, "lightGroups": [], "lightCollections": [],
                                                    "lightLinks": [], "outputs": [], "previewOutput": None}})

    # -- animation ---------------------------------------------------------------------------------------------
    def anim(self, item, prop, keys, vtype='vector3'):
        """keys: [(local_frame, value, easing='linear'), ...]"""
        kf = []
        for i, k in enumerate(keys):
            f, v = k[0], k[1]; e = k[2] if len(k) > 2 else 'linear'
            val = {"type": vtype, "value": v}
            kf.append({"id": f"k{self.L}_{item}_{prop}_{i}", "layerTime": ms(f), "value": val, "easing": ease(e)})
        self.d.add({"type": "setFxAnimator", "compositionId": "main", "target": {"type": "styleProperty", "layerId": self.L, "itemId": item, "propertyName": prop},
                    "animator": {"type": "keyframes", "enabled": True, "keyframes": kf}, "dependencies": [], "layerRefBindings": []})

    def script(self, item, prop, code):
        """procedural animator: code returns the value from input.time.seconds (layer-local)"""
        self.d.add({"type": "setFxAnimator", "compositionId": "main", "target": {"type": "styleProperty", "layerId": self.L, "itemId": item, "propertyName": prop},
                    "animator": {"type": "jsScript", "layerTimeJsCode": code}, "dependencies": [], "layerRefBindings": []})

    # -- objects -----------------------------------------------------------------------------------------------
    def group(self, pos, name='target', parent=None):
        gid = self.d.nid()
        self.d.add({"type": "addFxScene3DLayer", "compositionId": "main", "layerId": self.L,
                    "item": {"type": "Group3D", "id": gid, "parentId": parent, "name": name, "transform": {"position": list(pos)}}})
        return gid

    def camera(self, pos, target, fov=40, keys=None, tkeys=None, fkeys=None, roll=None):
        """aim camera at a Group3D target. keys/tkeys/fkeys: [(frame, value, ease)] for position / target / angleOfView."""
        tid = self.group(target, 'cam target'); cid = self.d.nid()
        self.d.add({"type": "addFxScene3DLayer", "compositionId": "main", "layerId": self.L, "item": {
            "type": "Camera3D", "id": cid, "parentId": None, "name": "Camera", "transform": {"position": list(pos), "relationships": {"constraints": [
                {"type": "aim", "id": self.d.nid(), "target": {"id": self.d.nid(), "target": {"type": "item", "item": tid}, "offset": [0, 0, 0], "offsetSpace": "local"},
                 "up": [0, 1, 0] if roll is None else [math.sin(math.radians(roll)), math.cos(math.radians(roll)), 0], "upSpace": "world", "forwardAxis": "positiveZ", "influence": 1}]}},
            "lens": {"type": "angle", "projection": {"type": "perspective", "angleOfView": fov}}}},
                   {"type": "setFxScene3DActiveCamera", "compositionId": "main", "layerId": self.L, "cameraItemId": cid})
        if keys: self.anim(cid, 'position', keys)
        if tkeys: self.anim(tid, 'position', tkeys)
        if fkeys: self.anim(cid, 'angleOfView', fkeys, 'float')
        self.cam, self.cam_target = cid, tid
        return cid

    def sun(self, rx=-50, ry=-35, irradiance=3.2, color='#FFF6E8', shadows=True):
        lid = self.d.nid()
        self.d.add({"type": "addFxScene3DLayer", "compositionId": "main", "layerId": self.L, "item": {
            "type": "Light3D", "id": lid, "parentId": None, "name": "Sun", "castsShadows": shadows, "color": ext(color), "transform": {"rotation": euler(rx, ry, 0)},
            "emitter": {"type": "parallel", "irradiance": irradiance}}})
        return lid

    def _slot(self, color, rough=0.9, metal=0.0, emissive=None, emissive_strength=1.0):
        inputs = {"baseColor": {"type": "constant", "value": lin(color)}, "roughness": {"type": "constant", "value": rough}}
        if metal: inputs["metallic"] = {"type": "constant", "value": metal}
        if emissive:
            inputs["emissiveColor"] = {"type": "constant", "value": [c * emissive_strength for c in lin(emissive)]}
        return {"id": self.d.nid(), "name": "Finish", "binding": {"id": self.d.nid(), "inputs": inputs}}

    def mesh(self, geom, pos, color, rot=(0, 0, 0), scale=(100, 100, 100), rough=0.9, metal=0.0, emissive=None, emissive_strength=1.0,
             name='mesh', shadows=True, parent=None):
        did, iid = self.d.nid(), self.d.nid(); slot = self._slot(color, rough, metal, emissive, emissive_strength)
        self.d.add({"type": "addFxScene3DFragment", "compositionId": "main", "layerId": self.L,
                    "data": [{"type": "mesh", "id": did, "name": name, "geometry": geom, "regions": [{"key": "primary", "name": "Primary"}, {"key": "side", "name": "Side"}]}],
                    "items": [{"type": "Mesh3D", "id": iid, "parentId": parent, "name": name, "dataId": did, "packing": "whole", "castsShadows": shadows,
                               "transform": {"position": list(pos), "rotation": euler(*rot), "scale": list(scale)},
                               "materialSlots": [slot], "regionSlots": [{"region": "primary", "slotId": slot["id"]}, {"region": "side", "slotId": slot["id"]}]}]})
        return iid

    def box(self, size, pos, color, **kw):
        return self.mesh({"type": "box", "size": list(size)}, pos, color, **kw)

    def ground(self, color, size=20000, y=0, **kw):
        return self.box((size, 10, size), (0, y + 5, 0), color, rough=0.95, name='ground', **kw)

    def model(self, asset, pos, rot=(0, 0, 0), scale=100, clip=None, clip_t0=0.0, clip_rate=1.0, clip_loop=True, name=None, shadows=True, parent=None):
        did = self._data.get(asset)
        data = []
        if did is None:
            did = self.d.nid(); self._data[asset] = did; data = [{"type": "model", "id": did, "name": asset, "assetId": asset}]
        iid = self.d.nid(); s = scale if isinstance(scale, (list, tuple)) else [scale] * 3
        item = {"type": "Model3D", "id": iid, "parentId": parent, "name": name or asset, "dataId": did, "castsShadows": shadows,
                "transform": {"position": list(pos), "rotation": euler(*rot), "scale": list(s)}, "materialSlots": [], "modelRegionSlots": []}
        if clip:
            item["clip"] = {"animation": f"animation:path:{clip}", "loop": clip_loop, "time": clip_t0}
            item["poseStack"] = [{"type": "clip", "source": {"type": "primary"}}]
        self.d.add({"type": "addFxScene3DFragment", "compositionId": "main", "layerId": self.L, "data": data, "items": [item]})
        if clip:
            self.anim(iid, 'clipTime', [(0, clip_t0), (self.nframes, clip_t0 + self.nframes / FPS * clip_rate)], 'float')
        return iid


# -- 2D layers ---------------------------------------------------------------------------------------------------
def caption(doc, layer_id, text, highlights, t0, t1, font=("Nunito", "Black"), size=33, y=846, stroke=4.0,
            fill='#FEFEFC', hl='#D88168', outline='#1C252A', width=576):
    """centred point-text caption with highlighted words (per-character fill overrides)."""
    animators = []
    for w in highlights:
        i = text.find(w)
        if i < 0: continue
        animators.append({"id": doc.nid(), "name": f"hl {w}", "fillColor": ext(hl), "selectors": [
            {"id": doc.nid(), "start": i, "end": i + len(w), "units": "index", "basedOn": "characters", "mode": "add", "amount": 1.0, "shape": "square"}],
            "wigglySelectors": []})
    f0 = int(round(t0 * FPS)); f1 = int(round(t1 * FPS))
    doc.add({"type": "createFxTextLayer", "compositionId": "main", "layerId": layer_id, "name": f"cap {text}", "insertIndex": 0,
             "activeRange": {"start": ms(f0), "duration": ms(f1) - ms(f0)},
             "transform": {"anchorPoint": [0, 0], "position": [width / 2, y], "scale": [100, 100], "rotation": 0, "opacity": 100},
             "sourceText": {"text": text, "fontFamily": font[0], "fontStyle": font[1], "fontSize": size, "fillColor": ext(fill), "justification": "center",
                            "strokeEnabled": True, "strokeColor": ext(outline), "strokeWidth": stroke, "strokeOverFill": False},
             "animators": animators})
