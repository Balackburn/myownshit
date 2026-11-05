#!/usr/bin/env python3
"""replica_tornado.py: the 3D layer of the "man lost his dog in a tornado" replica, rendered by our engine.

The reference cuts set every scene's start and duration exactly (frame / 30 fps, from
tesseract/01-tornado-replica/analysis/shots.json). The JSON is already timed, so there is no TTS and no captions: the
captions, the THEFT card, the HUD and the original sound are HyperFrames layers on top
(hyperframes/01-tornado-reverse). Render with:
  node render/render3.mjs scripts-fr/replica_tornado.json --timed --w 576 --h 1024 --workers 4 --out out/replica_tornado_3d.mp4
Engine coordinates: metres, Y up, Z toward the default camera. A camera looking -Z has +X on its right; looking +Z, -X is
on its right; looking -X, -Z is on its right.
"""
import json, os
from actu_common import act, k, P

FPS = 30
CUTS = [0, 57, 103, 135, 196, 211, 229, 243, 313, 335, 386, 431, 483, 529, 584, 607, 648, 670, 707, 724, 766, 780, 864]


def span(i):
    return CUTS[i - 1] / FPS, (CUTS[i] - CUTS[i - 1]) / FPS


def cam(at, frm, to, look, look2=None, lens=60, ease='linear'):
    c = {'at': at, 'from': frm, 'to': to, 'lookAt': look, 'lens': lens, 'ease': ease}
    if look2: c['lookAt2'] = look2
    return c


def scene(i, sid, set_, actors=(), props=(), cams=(), **kw):
    st, du = span(i)
    return {'id': sid, 'set': set_, 'lines': [], 'actors': list(actors), 'props': list(props), 'sfx': [], 'cams': list(cams),
            'start': round(st, 6), 'duration': round(du, 6), **kw}


TOR = {'rings': 22, 'height': 5.8, 'base': 0.3, 'top': 1.75, 'taper': 1.25, 'flare': 0.35, 'chips': 30,
       'cols': ['#7F8C7C', '#9AA693', '#6E7A6B', '#B3BCA8', '#879483']}
scenes = []

# S1 0.00-1.90: low camera behind him and the dog walking away (-Z, houses on his right = +X); it orbits 180 deg round his
# right side (f16: profile from the house side, he walks frame-right) to his front (f34), revealing the tornado behind
# him (it came from where he walked); the dog is pulled back over him into it, he raises his left arm (frame right)
scenes.append(scene(1, 'S1', 'replicaStreet',
    actors=[act('mec', [0, 0, 0], 180, 'walk', 'neutral', keys=[
        k(0.0, to=[0, 0, -2.4], glide=True, dur=1.13, clip='walk', then='point', face='keep')])],
    props=[P('dog', 'voxelDog', pos=[-0.6, 0, -0.5], rot=[0, 3.1416, 0], scale=1.25, opts={'walk': True}, keys=[
               k(0.0, to=[-0.6, 0, -2.9], dur=1.13, ease='linear'),
               k(1.2, to=[-0.4, 1.8, -2.2], dur=0.25, ease='in'),
               k(1.45, to=[-12.0, 7.5, 22.0], dur=0.45, ease='in')]),
           P('tornado', 'tornado', pos=[-14, 0, 26], scale=3.5, opts=TOR)],
    cams=[cam(0.0, [0.5, 0.6, 2.2], [2.4, 0.9, -1.1], [0, 1.2, 0], [0, 1.3, -1.1], lens=72),
          cam(0.533, [2.4, 0.9, -1.1], [0.6, 1.0, -5.0], [0, 1.3, -1.1], [0, 1.5, -2.4], lens=72),
          cam(1.133, [0.6, 1.0, -5.0], [0.7, 1.05, -4.8], [0, 1.5, -2.4], [0, 1.8, -2.4], lens=72)]))

# S2 1.90-3.43: close tracking shot of the dog spinning in the tornado wall, mouth open
scenes.append(scene(2, 'S2', 'replicaStreet',
    props=[P('tornado', 'tornado', pos=[0, 0, -4.2], scale=5.2, opts={**TOR, 'chips': 10}),
           P('dog', 'voxelDog', pos=[-0.6, 6.2, 0], rot=[0.17, 0.6, 0.26], scale=1.25, opts={'tongue': True, 'paddle': True}, keys=[k(0.0, to=[0.1, 6.4, -0.3], dur=1.53, ease='linear')])],
    cams=[cam(0.0, [-0.6, 6.5, 3.9], [0.0, 6.6, 3.6], [-0.35, 6.3, 0], [0.15, 6.45, -0.2], lens=55)]))

# S3 3.43-4.50: low 3/4 medium shot on the near kerb, explaining hands; the camera looks across the road (-X) at the far houses
scenes.append(scene(3, 'S3', 'replicaStreet',
    actors=[act('mec', [-1.2, 0, 0], 45, 'explain', 'neutral')],
    cams=[cam(0.0, [0.2, 0.92, 0.3], [0.2, 0.92, 0.3], [-1.5, 2.25, -0.25], lens=74)]))

# S4 4.50-6.53: selfie close-up on the far sidewalk, phone in his LEFT hand (frame right), face left of centre, the road on
# the right (camera looks -Z, so +X is frame-right), the tornado far down the road
scenes.append(scene(4, 'S4', 'replicaStreet',
    actors=[act('mec', [-12.0, 0, 0], 0, 'phoneCallL', 'neutral')],
    props=[P('phone', 'phone911', on={'actor': 'mec', 'hand': 'L'}),
           P('tornado', 'tornado', pos=[-7, 0, -62], scale=3.0, opts=TOR)],
    cams=[cam(0.0, [-11.95, 1.68, 1.35], [-11.98, 1.7, 1.28], [-11.58, 1.84, 0], lens=74)]))

# S5 6.53-7.03: extreme close-up of a nozzle firing (afterburner), runway beyond
scenes.append(scene(5, 'S5', 'runway',
    props=[P('jet', 'fighterJet', pos=[0, 0, 0], opts={'burner': 1.0, 'gear': True})],
    cams=[cam(0.0, [2.2, 1.6, -7.4], [2.1, 1.6, -7.2], [0.1, 1.45, -6.6], [0.1, 1.45, -6.5], lens=50)]))

# S6 7.03-7.63: fast dolly along the fuselage from the burning exhausts to the nose wheel (U.S. AIR FORCE, roundel)
scenes.append(scene(6, 'S6', 'runway',
    props=[P('jet', 'fighterJet', pos=[0, 0, 0], opts={'burner': 1.0, 'gear': True})],
    cams=[cam(0.0, [2.6, 2.6, -5.5], [2.4, 2.2, 6.5], [0.3, 1.5, -3.0], [0.0, 0.7, 8.0], lens=55)]))

# S7 7.63-8.10: wide runway, the jet takes off toward the camera and passes over it
scenes.append(scene(7, 'S7', 'runway',
    props=[P('jet', 'fighterJet', pos=[0, 0, -60], opts={'burner': 1.0, 'gear': True}, keys=[k(0.0, to=[0, 2.0, -18], dur=0.3, ease='in'), k(0.3, to=[0, 7.0, 6], dur=0.17, ease='linear')])],
    cams=[cam(0.0, [0, 1.4, 8], [0, 1.4, 8], [0, 1.6, -40], [0, 5.0, -5], lens=40)]))

# S8-S22: placeholders until each shot is built (sky and tornado, so the full film plays in the comparison)
for i in range(8, 23):
    scenes.append(scene(i, f'S{i}', 'replicaStreet',
        props=[P('tornado', 'tornado', pos=[-6, 0, -30], scale=3.0, opts=TOR)],
        cams=[cam(0.0, [0, 1.6, 8], [0, 1.6, 8], [-6, 6, -30], lens=60)]))

doc = {'version': 3, 'title': 'Replica: man lost his dog in a tornado', 'captionWords': 0, 'captionY': 0.81, 'tempo': 1.0,
       'voice': None, 'music': None, 'cast': {'mec': {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}}}, 'scenes': scenes, 'total': CUTS[-1] / FPS}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'replica_tornado.json')
json.dump(doc, open(out, 'w'), indent=1)
print(out, len(scenes), 'scenes', doc['total'], 's')
