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


TOR = {'rings': 14, 'height': 7.3, 'base': 0.39, 'top': 2.03, 'taper': 0.6, 'flare': 0.0, 'crownFlare': 1.08, 'chips': 30, 'teeth': True, 'gap': 0.22,
       'cols': ['#6B776F', '#7B877F', '#5B675F', '#84908A'], 'pale': 3, 'paleColor': '#D3CCB8', 'stripe': '#D9D2C0', 'stripeDark': '#55615A'}   # measured profile: 1.54x taller than wide
TORL = {**TOR, 'cols': ['#94A99D', '#A3B6AA', '#879C90', '#ABBDB1'], 'paleColor': '#DCE1D3', 'stripe': '#DDE2D6', 'stripeDark': '#7A9084'}   # the paler tornado of the ruins
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

def scene_f(sid, f0, f1, set_, actors=(), props=(), cams=(), **kw):
    """a scene between two reference frames (for shots split at an invisible cut, e.g. inside the S8 cloud white-out)"""
    return {'id': sid, 'set': set_, 'lines': [], 'actors': list(actors), 'props': list(props), 'sfx': [], 'cams': list(cams),
            'start': round(f0 / FPS, 6), 'duration': round((f1 - f0) / FPS, 6), **kw}


TORA = {**TOR, 'base': 0.3, 'top': 1.6, 'taper': 1.0, 'crownFlare': 1.15, 'cols': ['#5B675F', '#66726A', '#4F5A53', '#6F7B73'], 'pale': 2, 'paleColor': '#C9BC9C',
        'collar': [1.95, 3.3], 'rim': 40, 'rimAt': 1.6, 'rimSize': 0.34, 'ribbons': 8, 'ribbonFlat': True, 'ribbonR': 3.2, 'ribbonY0': 0.95, 'ribbonDY': 0.12,
        'dust': 0.8, 'chips': 40, 'stripe': '#4F5A53', 'stripeDark': '#4A554E'}   # the aerial look: narrow striped body, flat dark collar with rocks, tan ring
JETA = {'burner': 0.45, 'glow': 3.4, 'glowColor': '#FF6A22', 'missiles': 4}
V = 55.0                                                               # strike speed (m/s) of the jet + chase camera


def mv(p, dz, dx=0.0, dy=0.0):
    return [round(p[0] + dx, 3), round(p[1] + dy, 3), round(p[2] + dz, 3)]


# S8a 8.10-8.47: from below and behind, the jet climbs away into the blue and punches into the cloud deck overhead (contrail left
# behind); the deck is a small patch right above, so the first frames are pure sky
J0, J1 = [2, -147, -62], [20, -6, -150]
scenes.append(scene_f('S8a', 243, 254, 'skyHigh', props=[
    P('jet', 'fighterJet', pos=J0, rot=[0.9, 2.93, 0.18], opts={'burner': 1.0, 'glow': 4.5, 'missiles': 4}, keys=[k(0.0, to=J1, dur=0.27, ease='in')]),
    P('trail', 'missileSalvo', opts={'size': 3.0, 'trail': 1.0, 'trailWidth': 0.3, 'shots': [{'from': mv(J0, 18, -3, -14), 'to': J1, 't0': -0.03, 'dur': 0.3, 'body': False, 'hide': False, 'lin': True}]})],
    cams=[cam(0.0, [0, -150, 20], [0, -140, 8], [2, -146, -62], [18, -6, -120], lens=55, ease='in')],
    setOpts={'w': 300, 'd': 300, 'n': 150, 'h': 26, 'cz': -40, 'fog': False, 'sky': ['#5CABDF', '#7DC3E9']}))

# S8b 8.47-10.43: white-out (the camera dives through a cloud), then the strike seen from above-behind. Camera solved from the reference
# (solve_cam: rim/base screen rows, rim width, house size; tornado scale 9): altitude 236 -> 160 m, 242 -> 121 m from the tornado, pitch
# 48 -> 54 deg; the jet 24 m ahead, nose-down, nozzles facing us; the lock-on HUD is a HyperFrames layer
import math as _m
TZ = -520.0; TS = 9.0                        # tornado position (z) and scale for the aerial shots
def vdir(deg): return [0.0, -_m.sin(_m.radians(deg)), -_m.cos(_m.radians(deg))]
def ahead(c, deg, k=300.0): d = vdir(deg); return [round(c[i] + d[i] * k, 2) for i in range(3)]
def rel(c, r): return [round(c[0] + r[0], 2), round(c[1] + r[1], 2), round(c[2] + r[2], 2)]
def lerp3(a, b, u): return [round(a[i] + (b[i] - a[i]) * u, 2) for i in range(3)]
C8a, C8z = [0, 236, TZ + 242], [0, 160, TZ + 121]; P8a, P8z = 48.1, 53.6; T8 = 1.967
def c8(t): return lerp3(C8a, C8z, t / T8)
JR8a, JR8b = [-1.15, -20.34, -13.45], [0.13, -21.96, -11.02]        # jet relative to the camera at f270 and f312 (solved)
def cl_at(c, deg, k, off): p = ahead(c, deg, k); return [round(p[0] + off[0], 2), round(p[1] + off[1], 2), round(p[2] + off[2], 2)]
scenes.append(scene_f('S8b', 254, 313, 'aerialSuburb', props=[
    P('cl1', 'cumulus', pos=cl_at(C8a, P8a, 5, [0, -4, 0]), opts={'w': 14, 'h': 8, 'n': 14, 'seed': 3}),
    P('cl2', 'cumulus', pos=cl_at(C8a, P8a + 16, 80, [-26, -14, 0]), opts={'w': 80, 'h': 30, 'n': 30, 'seed': 8}),
    P('cl3', 'cumulus', pos=cl_at(C8a, P8a + 18, 84, [30, -16, 0]), opts={'w': 76, 'h': 28, 'n': 28, 'seed': 12}),
    P('cl4', 'cumulus', pos=cl_at(C8a, P8a + 24, 70, [0, -12, 0]), opts={'w': 90, 'h': 30, 'n': 34, 'seed': 15}),
    P('cl5', 'cumulus', pos=cl_at(C8a, P8a + 12, 26, [-4, -8, 0]), opts={'w': 60, 'h': 22, 'n': 30, 'seed': 21}),
    P('tornado', 'tornado', pos=[0, 0, TZ], scale=TS, opts=TORA),
    P('jet', 'fighterJet', pos=rel(C8a, [0, -62, 6]), rot=[-0.8, 3.1416, 0.04], opts=JETA, keys=[
        k(0.0, to=rel(c8(0.533), JR8a), dur=0.533, ease='out'), k(0.533, to=rel(C8z, lerp3(JR8a, JR8b, 1.0 + 1 / 42)), dur=T8 - 0.533, ease='linear')])],
    cams=[cam(0.0, C8a, C8z, ahead(C8a, P8a), ahead(C8z, P8z), lens=50)], shadow={'size': 300, 'center': [0, 0, TZ + 120]}))

# S9 10.43-11.17: over the cloud deck, the jet (seen nearly level, from the front-left 3/4, 38 m away) flies frame-left and lets the
# missiles go (they drop, ignite, race ahead); the camera looks level, the jet 10 deg above centre
JY = 66.0; T9 = 0.733; V9 = 60.0
HD = [-0.906, 0.0, 0.423]                     # heading: -X turned 25 deg toward the camera
J9a = [0, JY, 0]; J9b = [round(HD[0] * V9 * T9, 2), JY, round(HD[2] * V9 * T9, 2)]
msl9 = []
for i, (dx, dz) in enumerate([(1.0, 2.6), (1.5, -2.6), (0.4, 3.5), (0.9, -3.5)]):
    t0 = 0.08 + i * 0.07
    jx, jz = HD[0] * V9 * t0, HD[2] * V9 * t0
    st = [round(jx + dx, 2), JY - 1.2, round(jz + dz, 2)]
    msl9.append({'from': st, 'ctrl': [round(st[0] + HD[0] * 20, 2), JY - 4.0, round(st[2] + HD[2] * 20, 2)], 'to': [round(st[0] + HD[0] * 170, 2), JY - 9 - i, round(st[2] + HD[2] * 170, 2)],
                 't0': t0, 'dur': 0.8, 'trail': 0.3})
smk9 = [{'from': [round(-HD[0] * 70, 2), JY + 0.2, round(-HD[2] * 70, 2)], 'to': J9b, 't0': 0.0, 'dur': T9, 'body': False, 'hide': False, 'lin': True, 'trail': 0.75}]
CAM9 = [-1.7, -6.0, 43.0]
scenes.append(scene_f('S9', 313, 335, 'skyHigh', props=[
    P('jet', 'fighterJet', pos=J9a, rot=[0.6, -1.134, 0.45], opts={'burner': 0.5, 'glow': 2.6, 'missiles': 4}, keys=[k(0.0, to=J9b, dur=T9, ease='linear')]),
    P('msl', 'missileSalvo', opts={'size': 1.0, 'shots': msl9}),
    P('smk', 'missileSalvo', opts={'size': 1.6, 'trailOpacity': 0.6, 'shots': smk9})],
    cams=[cam(0.0, rel(J9a, CAM9), rel(J9b, CAM9), rel(J9a, [-1.7, -6.0, -10]), rel(J9b, [-1.7, -6.0, -10]), lens=48)],
    setOpts={'cz': -40, 'h': 30, 'n': 520, 'w': 1300, 'd': 1300, 'sky': ['#62AEE2', '#7CC2EC'], 'fogNear': 500, 'fogFar': 1800, 'fogColor': '#7DC2EC'}))

# S10 11.17-12.87: back on the chase view (solved: altitude 257 -> 157 m, 243 -> 105 m from the tornado, pitch 51 -> 56 deg; the jet ~40 m
# ahead, drifting left); the salvo streaks ahead from under the wings and converges on the tornado
C10a, C10b = [0, 257, TZ + 243], [0, 157, TZ + 105]; P10a, P10b = 51.0, 56.0; T10 = 1.7
JR10a, JR10b = [-0.67, -36.25, -21.79], [-3.65, -34.30, -12.36]
salvo = []
for i in range(14):
    t0 = 0.04 + i * 0.075
    side = -1 if i % 2 else 1
    u = t0 / T10
    st = rel(lerp3(C10a, C10b, u), rel(lerp3(JR10a, JR10b, u), [side * (2.0 + (i % 4) * 0.95), -0.6, 0.5]))
    tgt = [side * (2.5 + (i % 3) * 3), TS * (3.2 + (i % 5) * 0.8), TZ + (i % 4) * 2]
    mid = lerp3(st, tgt, 0.45)
    salvo.append({'from': st, 'ctrl': [round(mid[0] + side * (35 + (i % 4) * 18), 2), mid[1] + 10, mid[2]], 'to': tgt, 't0': t0, 'dur': 1.0 + (i % 3) * 0.12, 'trail': 0.6, 'v0': 0.4})
scenes.append(scene_f('S10', 335, 386, 'aerialSuburb', props=[
    P('tornado', 'tornado', pos=[0, 0, TZ], scale=TS, opts=TORA),
    P('jet', 'fighterJet', pos=rel(C10a, JR10a), rot=[-0.8, 3.1416, -0.03], opts={**JETA, 'burner': 0.7}, keys=[k(0.0, to=rel(C10b, JR10b), dur=T10, ease='linear')]),
    P('salvo', 'missileSalvo', opts={'size': 1.6, 'glow': 1.0, 'trailOpacity': 0.85, 'trailWidth': 0.16, 'shots': salvo})],
    cams=[cam(0.0, C10a, C10b, ahead(C10a, P10a), ahead(C10b, P10b), lens=50)], shadow={'size': 300, 'center': [0, 0, TZ + 120]}))

# S11 12.87-14.37: street level across the road (camera yawed ~8 deg right, pitched up ~6 deg, wide lens): the missile hits the tornado behind
# the cottages, fireball and glare, then smoke, debris and a second hit lower right
scenes.append(scene(11, 'S11', 'cottageStreet', props=[
    P('tornado', 'tornado', pos=[8.8, 0, -40], scale=4.6, opts={**TOR, 'chips': 44}),
    P('boom1', 'fireball', pos=[8.3, 18, -35], opts={'t0': 0.06, 'size': 7.0, 'n': 30, 'seed': 3, 'glowShare': 0.3, 'smokeColor': '#4A4441'}),
    P('boom2', 'fireball', pos=[11.5, 10.5, -34], opts={'t0': 0.86, 'size': 5.0, 'n': 22, 'seed': 9, 'smoke': 0.8, 'glowShare': 0.3, 'smokeColor': '#4A4441'}),
    P('msl', 'missileSalvo', opts={'size': 1.3, 'shots': [{'from': [40, 55, 0], 'to': [8.3, 18, -35], 't0': -0.2, 'dur': 0.26, 'trail': 0.5},
                                                         {'from': [42, 4, 2], 'to': [11.5, 10.5, -34], 't0': 0.56, 'dur': 0.3, 'trail': 0.6}]})],
    cams=[cam(0.0, [2.3, 1.3, 8.0], [2.3, 1.3, 8.0], [6.44, 4.75, -21.5], lens=68)], setOpts={'houseZ': -11.2, 'houses': [
        {'x': -0.5, 'w': 7.0, 'color': '#F4F2EC', 'roof': '#C9473A', 'eaves': True, 'door': '#2F7F8C', 'shutters': '#E3B33A', 'porchRoof': '#C9473A'},
        {'x': 6.0, 'w': 5.6, 'color': '#B8A6D9', 'roof': '#6A3A30', 'door': '#B5302A'}, {'x': 11.6, 'w': 5.6, 'color': '#E8A08A', 'roof': '#3E4A5E', 'door': '#2F5E8C'},
        {'x': 17.4, 'w': 5.8, 'color': '#EDCF7A', 'roof': '#B5402F'}, {'x': -7.6, 'w': 5.8, 'color': '#F0C6CF', 'roof': '#5E83C6'},
        {'x': -14.6, 'w': 6.0, 'color': '#A9C7E8', 'roof': '#B5402F', 'eaves': True}, {'x': 23.2, 'w': 5.8, 'color': '#F4F2EC', 'roof': '#3E4A5E'}]}))

# S12 14.37-16.10: high over the rows of cottages, the tornado on the field beyond; strikes land among the houses, closer and closer
scenes.append(scene(12, 'S12', 'cottageRows', props=[
    P('tornado', 'tornado', pos=[4, 0, -330], scale=6.5, opts={**TOR, 'chips': 30}),
    P('b1', 'fireball', pos=[0, 4, -205], opts={'t0': 0.5, 'size': 11, 'seed': 4, 'glowShare': 0.35}),
    P('b2', 'fireball', pos=[-14, 4, -105], opts={'t0': 1.05, 'size': 14, 'seed': 6, 'glowShare': 0.35, 'flash': 0.9}),
    P('b3', 'fireball', pos=[-16, 3, -38], opts={'t0': 1.5, 'size': 11, 'seed': 8, 'glowShare': 0.35}),
    P('msl', 'missileSalvo', opts={'size': 2.5, 'shots': [{'from': [90, 160, -300], 'to': [0, 4, -205], 't0': 0.2, 'dur': 0.3, 'trail': 0.5},
                                                         {'from': [70, 170, -260], 'to': [-14, 4, -105], 't0': 0.75, 'dur': 0.3, 'trail': 0.6},
                                                         {'from': [60, 160, -200], 'to': [-16, 3, -38], 't0': 1.2, 'dur': 0.3, 'trail': 0.6}]})],
    cams=[cam(0.0, [0, 30, 48], [0, 30, 46], [0, 6, -40], [0, 6, -42], lens=48)], setOpts={'rows': 13}))

# S13 16.10-17.63: "All of it.": the same streets in ruins, dark grade, a forest of smoke columns and fires, the tornado far behind
fl, sm = [], []
for j in range(9):
    for i in range(15):
        x = (i - 7) * 10.5 + (3.7 if j % 2 else 0); z = -j * 23
        fl.append([x + ((i * 13 + j) % 5 - 2) * 0.8, 0.6 + (i % 3) * 0.6, z + 2.0, 3.0 + (i + j) % 3 * 0.9])
        fl.append([x + 3.0, 0.4, z - 1.5, 2.2 + (i * j) % 3 * 0.7])
        if j >= 2:
            sm.append([x - 2.2, z - 1, 17 + (i * j % 5) * 2.5, 1.5])
            sm.append([x + 2.6, z - 3, 15 + (i % 4) * 2.5, 1.0])
scenes.append(scene(13, 'S13', 'cottageRows', props=[
    P('tornado', 'tornado', pos=[6, 0, -330], scale=6.5, opts={**TOR, 'chips': 30, **{k_: v_ for k_, v_ in TORL.items() if k_ in ('cols', 'stripe', 'stripeDark', 'paleColor')}}),
    P('fires', 'flameField', opts={'points': fl, 'seed': 3}),
    P('smoke', 'smokeField', opts={'points': sm, 'size': 1.05, 'per': 14, 'seed': 5})],
    cams=[cam(0.0, [0, 23.5, 40], [0, 23.2, 38.5], [0, 2.5, -60], [0, 2.3, -61.5], lens=48)], setOpts={'burnt': True, 'rows': 13}))

# S14 17.63-19.47: on the burnt road, low camera tilted up 18 deg, the tornado waves a white flag
scenes.append(scene(14, 'S14', 'ruinedStreet', props=[
    P('tornado', 'tornado', pos=[0, 0, -34], scale=2.3, opts={**TOR, 'chips': 40, **{k_: v_ for k_, v_ in TORL.items() if k_ in ('cols', 'stripe', 'stripeDark', 'paleColor')}}, keys=[k(0.0, to=[0, 0, -31], dur=1.83, ease='linear')]),
    P('flag', 'whiteFlag', pos=[0.4, 17.2, -29.5], rot=[0, 0, -0.3], scale=3.6, opts={'w': 1.6, 'h': 1.45, 'pole': 1.7}, keys=[k(0.0, to=[0.4, 17.2, -26.5], dur=1.83, ease='linear')])],
    cams=[cam(0.0, [0.3, 0.6, 6], [0.3, 0.6, 5.4], [0, 9.0, -30], [0, 9.1, -30], lens=60)]))

# S15-S22: placeholders until each shot is built (sky and tornado, so the full film plays in the comparison)
for i in range(15, 23):
    scenes.append(scene(i, f'S{i}', 'replicaStreet',
        props=[P('tornado', 'tornado', pos=[-6, 0, -30], scale=3.0, opts=TOR)],
        cams=[cam(0.0, [0, 1.6, 8], [0, 1.6, 8], [-6, 6, -30], lens=60)]))

# the director reads a prop's yaw from 'ry' (degrees); rot carries only the pitch and roll (radians). Convert rot[1] once here.
import math
for sc_ in scenes:
    for p_ in sc_['props']:
        if 'rot' in p_ and 'ry' not in p_:
            p_['ry'] = round(math.degrees(p_['rot'][1]), 3)

doc = {'version': 3, 'title': 'Replica: man lost his dog in a tornado', 'captionWords': 0, 'captionY': 0.81, 'tempo': 1.0,
       'voice': None, 'music': None, 'cast': {'mec': {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}}}, 'scenes': scenes, 'total': CUTS[-1] / FPS}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'replica_tornado.json')
json.dump(doc, open(out, 'w'), indent=1)
print(out, len(scenes), 'scenes', doc['total'], 's')
