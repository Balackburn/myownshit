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


TOR = {'rings': 14, 'height': 7.3, 'base': 0.39, 'top': 2.03, 'taper': 0.6, 'flare': 0.0, 'crownFlare': 1.1, 'crownH': 1.7, 'crownSpike': 0.42, 'chips': 30, 'teeth': True,
       'gap': 0.05, 'band': 1.3, 'spike': 0.0, 'bands': 0.3, 'cols': ['#66726A', '#6E7A72', '#606C64', '#727E76'], 'paleColor': '#D3CCB8', 'stripe': '#B9B3A2', 'stripeDark': '#55615A'}   # measured profile: 1.54x taller than wide
TORL = {**TOR, 'cols': ['#94A99D', '#A3B6AA', '#879C90', '#ABBDB1'], 'paleColor': '#DCE1D3', 'stripe': '#DDE2D6', 'stripeDark': '#7A9084'}   # the paler tornado of the ruins
scenes = []

# S1 0.00-1.90: low camera behind him and the dog walking away (-Z; cottages on his right = +X, the road on his left); it orbits 180 deg
# round his LEFT (road) side - f18: from the road, looking at the cottages, he walks frame-left - to his front (f33), revealing the tornado
# behind him across the road; he stops at f36, the dog is yanked up and away over his left shoulder into the tornado, his left arm flies up
import math as _m1
def orbit_cams(t0, t1, n, centre_at, r0, r1, a0, a1, h0, h1, look_h=1.0, lens=72):
    """camera keys on an arc round a moving point: angle a (deg) 0 = behind (+Z side), 90 = his left (-X), 180 = in front (-Z)"""
    ks = []
    def pos(t):
        u = (t - t0) / (t1 - t0); u = u * u * (3 - 2 * u)
        a = _m1.radians(a0 + (a1 - a0) * u); r = r0 + (r1 - r0) * u; c = centre_at(t)
        return [round(c[0] - r * _m1.sin(a), 3), round(h0 + (h1 - h0) * u, 3), round(c[2] + r * _m1.cos(a), 3)]
    ts = [t0 + (t1 - t0) * i / n for i in range(n + 1)]
    for i in range(n):
        ca, cb = centre_at(ts[i]), centre_at(ts[i + 1])
        ks.append(cam(round(ts[i], 4), pos(ts[i]), pos(ts[i + 1]), [ca[0], look_h, ca[2]], [cb[0], look_h, cb[2]], lens=lens))
    return ks
WALK0, WALK1, TW = 0.6, -1.9, 1.2                     # he walks 2.5 m in 1.2 s (f0-f36), then stops
def man_at(t): u = min(1.0, max(0.0, t / TW)); return [0.0, 0.0, WALK0 + (WALK1 - WALK0) * u]
s1cams = [cam(0.0, [0.1, 0.6, WALK0 + 3.0], [0.1, 0.6, man_at(0.3)[2] + 3.0], [-0.35, 0.95, WALK0 - 3], [-0.35, 0.95, man_at(0.3)[2] - 3], lens=72)]
s1cams += orbit_cams(0.3, 1.1, 8, man_at, 3.0, 2.5, 0, 180, 0.62, 0.85, 1.05)
s1cams += [cam(1.1, [0, 0.85, man_at(1.1)[2] - 2.5], [0, 0.88, WALK1 - 2.7], [-0.26, 1.1, man_at(1.1)[2]], [-0.26, 1.2, WALK1], lens=72)]
scenes.append(scene(1, 'S1', 'replicaStreet', setOpts={'near': 'cottage', 'z0': -44.2, 'nearTown': [5]},
    actors=[act('mec', [0, 0, WALK0], 180, 'walk', 'neutral', keys=[
        k(0.0, to=[0, 0, WALK1], dur=TW, clip='walk', then='stand'), k(1.28, clip='reachUpL')])],
    props=[P('dog', 'voxelDog', pos=[-0.65, 0, WALK0 + 0.35], rot=[0, 3.1416, 0], scale=1.0, opts={'walk': True}, keys=[
               k(0.0, to=[-0.65, 0, WALK1 - 0.1], dur=TW, ease='linear'),
               k(1.24, to=[-0.85, 1.0, WALK1 + 0.6], dur=0.07, ease='out'),
               k(1.31, to=[-8.5, 7.0, 26.0], dur=0.2, ease='linear')]),
           P('tornado', 'tornado', pos=[-8.5, 0, 28], scale=1.9, opts=TOR)],
    cams=s1cams, blur=[[0.3, 1.1, 0.04], [1.26, 1.5, 0.03]]))

# S2 1.90-3.43: close tracking shot of the dog spinning in the tornado wall, mouth open
scenes.append(scene(2, 'S2', 'replicaStreet',
    props=[P('tornado', 'tornado', pos=[0, 0, -6.0], scale=3.6, opts={**TOR, 'chips': 10}),
           P('dog', 'voxelDog', pos=[-0.6, 6.2, 0], rot=[0.17, 0.6, 0.26], scale=1.25, opts={'tongue': True, 'paddle': True}, keys=[k(0.0, to=[0.1, 6.4, -0.3], dur=1.53, ease='linear')])],
    cams=[cam(0.0, [-0.55, 6.5, 2.7], [0.0, 6.6, 2.5], [-0.4, 6.42, 0], [0.12, 6.55, -0.2], lens=55)]))

# S3 3.43-4.50: low 3/4 medium shot on the near kerb, explaining hands; the camera looks across the road (-X) at the far houses
scenes.append(scene(3, 'S3', 'replicaStreet',
    actors=[act('mec', [-1.2, 0, 0], 45, 'explain', 'neutral')],
    cams=[cam(0.0, [0.2, 0.92, 0.3], [0.2, 0.92, 0.3], [-1.5, 2.25, -0.25], lens=74)]))

# S4 4.50-6.53: selfie close-up on the far sidewalk (0.7 m from his face, camera above eye level looking down 15 deg, wide lens): the road on
# the right, the townhouses beyond the fence on the left, the tornado far down the road; at f151 he brings up the phone beside his face,
# screen to the camera, showing the creator's handle
scenes.append(scene(4, 'S4', 'replicaStreet',
    actors=[act('mec', [-12.0, 0, 0], 0, 'stand', 'neutral', keys=[k(0.5, clip='showPhoneFaceL')])],
    props=[P('phone', 'phone911', pos=[-11.84, 1.45, 0.22], rot=[0, -0.15, -0.24], scale=1.12, opts={'screen': 'handle'}, keys=[k(0.0, visible=False), k(0.5, visible=True), k(0.5, to=[-11.84, 1.94, 0.22], dur=0.14, ease='out')]),
           P('tornado', 'tornado', pos=[20, 0, -150], scale=3.0, opts=TOR)],
    cams=[cam(0.0, [-12.0, 2.43, 0.9], [-11.97, 2.44, 0.89], [-11.96, 2.17, -0.07], [-11.94, 2.18, -0.07], lens=74)]))

# S5 6.53-7.03: extreme close-up from the jet's right side (camera at -X looking +X): the ribbed nozzle centre-right, a white-hot afterburner
# blasting frame-left over the runway, the tail fins above
scenes.append(scene(5, 'S5', 'runway', props=[P('jet', 'fighterJet', pos=[0, 0, 0], opts={'burner': 1.5, 'glow': 3.2, 'gear': True})],
    cams=[cam(0.0, [-4.3, 1.0, -7.0], [-4.25, 1.01, -7.1], [-0.6, 1.62, -7.15], [-0.6, 1.62, -7.2], lens=50)], blur=0.02))

# S6 7.03-7.63: fast dolly above the jet's left side from the wing and its roundel (U.S. AIR FORCE on the fuselage) to the canopy and the
# nose wheel, the runway beyond (motion blur)
scenes.append(scene(6, 'S6', 'runway', props=[P('jet', 'fighterJet', pos=[0, 0, 0], opts={'burner': 1.0, 'glow': 4, 'gear': True})],
    cams=[cam(0.0, [6.5, 6.0, -6.5], [4.0, 3.0, 3.5], [2.0, 1.5, -2.5], [0.8, 0.8, 5.5], lens=50, ease='inOut')], blur=0.01))

# S7 7.63-8.10: wide runway, the jet lifts off far away (dust behind it) and roars over the camera banking up-right (whip, motion blur)
scenes.append(scene(7, 'S7', 'runway',
    props=[P('jet', 'fighterJet', pos=[0, 0.2, -60], rot=[0, 0, 0.35], opts={'burner': 1.0, 'glow': 5, 'gear': True, 'missiles': 4}, keys=[k(0.0, to=[0, 2.0, -18], dur=0.3, ease='in'), k(0.3, to=[1.5, 7.0, 6], dur=0.17, ease='linear')]),
           P('dust', 'dustPuff', pos=[0, 0, -66], scale=6, opts={'color': '#D9C9A6', 'period': 0.8})],
    cams=[cam(0.0, [0, 1.4, 8], [0, 1.4, 8], [0, 1.6, -40], [0.6, 5.0, -5], lens=40)], blur=[[0.3, 0.47, 0.05]]))

def scene_f(sid, f0, f1, set_, actors=(), props=(), cams=(), **kw):
    """a scene between two reference frames (for shots split at an invisible cut, e.g. inside the S8 cloud white-out)"""
    return {'id': sid, 'set': set_, 'lines': [], 'actors': list(actors), 'props': list(props), 'sfx': [], 'cams': list(cams),
            'start': round(f0 / FPS, 6), 'duration': round((f1 - f0) / FPS, 6), **kw}


TORA = {**TOR, 'height': 8.6, 'base': 0.3, 'top': 1.45, 'taper': 1.0, 'crownFlare': 1.1, 'cols': ['#5B675F', '#66726A', '#4F5A53', '#6F7B73'], 'pale': 2, 'paleColor': '#C9BC9C',
        'bands': False, 'collar': [1.55, 2.5], 'rim': 36, 'rimAt': 1.3, 'rimSize': 0.28, 'ribbons': 8, 'ribbonFlat': True, 'ribbonR': 2.5, 'ribbonY0': 0.95, 'ribbonDY': 0.1,
        'dust': 0.8, 'chips': 40, 'stripe': '#4F5A53', 'stripeDark': '#4A554E'}   # the aerial look: long striped body, flat dark collar with rocks, tan ring
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
    setOpts={'w': 300, 'd': 300, 'n': 150, 'h': 26, 'cz': -40, 'fog': False, 'sky': ['#5CABDF', '#7DC3E9']}, blur=0.03))

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
    cams=[cam(0.0, C8a, C8z, ahead(C8a, P8a), ahead(C8z, P8z), lens=50)], shadow={'size': 300, 'center': [0, 0, TZ + 120]}, setOpts={'houseScale': 0.7, 'gridRot': 0.12}))

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
    cams=[cam(0.0, C10a, C10b, ahead(C10a, P10a), ahead(C10b, P10b), lens=50)], shadow={'size': 300, 'center': [0, 0, TZ + 120]}, setOpts={'houseScale': 0.66, 'gridRot': 0.2}))

# S11 12.87-14.37: street level across the road (camera yawed ~8 deg right, pitched up ~6 deg, wide lens): the missile hits the tornado behind
# the cottages, fireball and glare, then smoke, debris and a second hit lower right
scenes.append(scene(11, 'S11', 'cottageStreet', props=[
    P('tornado', 'tornado', pos=[8.8, 0, -40], scale=4.6, opts={**TOR, 'chips': 44}),
    P('boom1', 'fireball', pos=[8.3, 18, -35], opts={'t0': 0.06, 'size': 7.0, 'n': 50, 'seed': 3, 'glowShare': 0.14, 'smokeColor': '#3E3836', 'puff': 0.62}),
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
    P('tornado', 'tornado', pos=[14, 0, -165], scale=5.0, opts={**TOR, 'chips': 30}),
    P('b1', 'fireball', pos=[-11, 3, -100], opts={'t0': 0.3, 'size': 6.5, 'seed': 4, 'glowShare': 0.3, 'flash': 0.6, 'glare': 0.3, 'life': 0.6, 'flashScale': 0.9, 'smoke': 0.75, 'smokeColor': '#3A3432'}),
    P('b2', 'fireball', pos=[-5, 3, -62], opts={'t0': 1.1, 'size': 8.5, 'seed': 6, 'glowShare': 0.3, 'flash': 0.6, 'glare': 0.3, 'life': 0.6, 'flashScale': 0.9, 'smoke': 0.75, 'smokeColor': '#3A3432'}),
    P('b3', 'fireball', pos=[1, 3, -34], opts={'t0': 1.5, 'size': 8, 'seed': 8, 'glowShare': 0.3, 'flash': 0.6, 'glare': 0.3, 'life': 0.6, 'flashScale': 0.9, 'smoke': 0.75, 'smokeColor': '#3A3432'}),
    P('msl', 'missileSalvo', opts={'size': 2.5, 'shots': [{'from': [90, 160, -300], 'to': [-11, 3, -100], 't0': 0.0, 'dur': 0.3, 'trail': 0.5},
                                                         {'from': [70, 170, -260], 'to': [-5, 3, -62], 't0': 0.8, 'dur': 0.3, 'trail': 0.6},
                                                         {'from': [60, 160, -200], 'to': [1, 3, -34], 't0': 1.2, 'dur': 0.3, 'trail': 0.6}]})],
    cams=[cam(0.0, [0, 25, 34], [0, 25, 32.5], [0, -2.0, -46], [0, -2.0, -47.5], lens=48)], setOpts={'rows': 7}))

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
    P('flag', 'whiteFlag', pos=[-0.6, 16.4, -29.5], rot=[0, 0, -0.32], scale=3.6, opts={'w': 1.6, 'h': 1.45, 'pole': 1.75, 'glow': '#A8A49E'}, keys=[k(0.0, to=[-0.6, 16.4, -26.5], dur=1.83, ease='linear')])],
    cams=[cam(0.0, [0.3, 0.6, 6], [0.3, 0.6, 5.4], [0, 9.0, -30], [0, 9.1, -30], lens=60)]))

# --- act 3: court, hard labour, grave ----------------------------------------------------------------------------
HANDLE = '@outofthisworld_9'
TORC = {**TOR, 'cols': ['#7C8A82', '#8C9A92', '#6E7C74', '#96A49C'], 'paleColor': '#E2DCCB', 'stripe': '#E4DECF'}      # lit by the courtroom
TORS = {**TOR, 'cols': ['#5E6962', '#646F68', '#5A655E', '#68736C'], 'pale': 2, 'paleColor': '#C2C5B9', 'bands': False, 'chips': 40}          # S17/S18: strong light/dark stripes
TORG = {**TORS, 'pale': 4, 'paleColor': '#CFC4A8', 'ribbons': 5, 'ribbonFollow': True, 'ribbonY0': 0.15, 'ribbonDY': 0.6, 'ribbonH': 5.5, 'ribbonArc': 4.4,
        'ribbonTilt': 0.5, 'ribbonColor': '#CDC2A6', 'ribbonSpeed': 3}                                                                   # S19-S21: pale spiral bands

# S15 19.47-20.23: the tornado in the dock, giant white handcuffs; the judge tiny at the bench behind; slow push-in
scenes.append(scene(15, 'S15', 'replicaCourt', setOpts={'handle': HANDLE},
    actors=[act('judge', [0, -0.15, -14.0], 0, 'idle')],
    props=[P('dock', 'dock', pos=[0, 0, 0], opts={'w': 7.5, 'd': 6.5, 'h': 1.5}),
           P('tornado', 'tornado', pos=[0, 0.43, 0], scale=1.05, opts={**TORC, 'chips': 36}),
           P('cuffs', 'bigCuffs', pos=[-0.4, 6.4, 3.6], opts={'r': 0.85})],
    cams=[cam(0.0, [2.5, 3.0, 13.7], [2.3, 3.1, 12.6], [-0.3, 4.6, 0], [-0.3, 4.7, 0], lens=50)]))

# S16 20.23-21.60: low on the bench, the judge strikes the gavel (raise f607-613, hit on the block at f619), slow push-in
scenes.append(scene(16, 'S16', 'replicaCourt', setOpts={'handle': HANDLE, 'windowX': -1.5, 'chairW': 1.2, 'chairH': 2.75, 'chairX': 0.15, 'benchGlow': '#5A564A'},
    actors=[act('judge', [-0.35, -0.3, -14.0], -35, 'gavelStrikeL', params={'hit': 0.4})],
    props=[P('gavelUp', 'gavel', on={'actor': 'judge', 'hand': 'L'}, keys=[k(0.0, visible=True), k(0.38, visible=False)]),
           P('gavel', 'gavel', pos=[0.03, 1.41, -13.65], rot=[0, 0, -1.5708], keys=[k(0.0, visible=False), k(0.38, visible=True)]),
           P('block', 'soundBlock', pos=[0.5, 1.18, -13.65])],
    cams=[cam(0.0, [0.05, 1.27, -11.2], [0.03, 1.28, -11.45], [-0.12, 1.56, -14.0], [-0.12, 1.56, -14.0], lens=45)],
    fx=[{'type': 'shake', 'at': 0.4, 'dur': 0.12, 'amount': 0.006}]))

# S17 21.60-22.33: low wide on the field: the handcuffed tornado spins in front of the wind turbine
scenes.append(scene(17, 'S17', 'grassland', props=[
    P('turbine', 'windTurbine', pos=[-21, 0, -72], opts={'h': 60, 'rpm': 13, 'label': HANDLE}),
    P('tornado', 'tornado', pos=[2.5, 0, -33], scale=3.1, opts=TORS),
    P('cuffs', 'bigCuffs', pos=[2.1, 20.0, -28.5], opts={'r': 1.05}),
    P('rubble', 'rubble', pos=[2.5, 0, -33], opts={'r': 3.2, 'n': 18, 'size': 0.8}),
    P('grass', 'tallGrass', pos=[0, 0, 4], opts={'w': 26, 'd': 10, 'h': 0.5, 'count': 260, 'seed': 4})],
    cams=[cam(0.0, [0, 1.2, 12], [0, 1.25, 11.4], [-2, 14, -40], [-2, 14.2, -40], lens=52)]))

# S18 22.33-23.57: from the tornado's crown, looking up at the hub, the rotor spins up into a blur
scenes.append(scene(18, 'S18', 'grassland', props=[
    P('turbine', 'windTurbine', pos=[0, 0, -60], opts={'h': 60, 'rpm': 34, 'blur': 1.4, 'blurSpread': 0.7, 'label': HANDLE}),
    P('tornado', 'tornado', pos=[-2.5, 0, -6], scale=2.0, opts=TORS),
    P('cuffs', 'bigCuffs', pos=[-2.6, 15.2, -3.2], opts={'r': 0.7})],
    cams=[cam(0.0, [2, 16, 10], [2, 16.2, 9.5], [0, 39.4, -60], [0, 39.8, -60], lens=50)]))

# S19 23.57-24.13: wide: turbine left, the tornado right, a tiny officer whipping at its base
scenes.append(scene(19, 'S19', 'grassland',
    actors=[act('cop', [-6, 0, -50], 90, 'whipWalk')],
    props=[P('turbine', 'windTurbine', pos=[-19, 0, -132], opts={'h': 60, 'rpm': 13, 'label': HANDLE}),
           P('tornado', 'tornado', pos=[8, 0, -55], scale=5.4, opts=TORG),
           P('cuffs', 'bigCuffs', pos=[7.5, 38, -49], opts={'r': 1.6}),
           P('rubble', 'rubble', pos=[8, 0, -55], opts={'r': 5, 'n': 24, 'size': 1.1}),
           P('whip', 'whip', on={'actor': 'cop', 'hand': 'R'}, opts={'length': 2.8, 'period': 0.6}),
           P('grass', 'tallGrass', pos=[0, 0, 4], opts={'w': 26, 'd': 10, 'h': 0.45, 'count': 240, 'seed': 6})],
    cams=[cam(0.0, [0, 2.0, 10], [0, 2.0, 9.6], [-1, 6.3, -50], [-1, 6.3, -50], lens=45)]))

# S20 24.13-25.53: the officer strides in and cracks the whip at the tornado's base, boulders fly; the camera pans with him
scenes.append(scene(20, 'S20', 'grassland',
    actors=[act('cop', [-3.2, 0, -6], 90, 'stand', keys=[k(0.0, to=[0.9, 0, -6], dur=1.15, clip='whipWalk', then='stand'), k(1.15, face=0)])],
    props=[P('whip', 'whip', on={'actor': 'cop', 'hand': 'R'}, opts={'length': 2.8, 'period': 0.6}),
           P('tornado', 'tornado', pos=[6.5, 0, -11], scale=5.4, opts={**TORG, 'ribbons': 0}),
           P('rubble', 'rubble', pos=[6.5, 0, -11], opts={'r': 3.6, 'n': 30, 'size': 0.7, 'fly': 0.4}),
           P('turbine', 'windTurbine', pos=[-12, 0, -70], opts={'h': 60, 'rpm': 13, 'label': HANDLE}),
           P('grass', 'tallGrass', pos=[0, 0, -4], opts={'w': 16, 'd': 6, 'h': 0.32, 'count': 160, 'seed': 8})],
    cams=[cam(0.0, [-1.4, 1.05, -1.5], [0.3, 1.05, -1.5], [-1.0, 1.45, -6], [1.2, 1.45, -6], lens=50)]))

# S21 25.53-26.00: wide again, the officer whipping at the base
scenes.append(scene(21, 'S21', 'grassland',
    actors=[act('cop', [-1.5, 0, -50], 90, 'whipWalk')],
    props=[P('turbine', 'windTurbine', pos=[-21, 0, -132], opts={'h': 60, 'rpm': 13, 'label': HANDLE}),
           P('tornado', 'tornado', pos=[8, 0, -55], scale=5.4, opts=TORG),
           P('cuffs', 'bigCuffs', pos=[7.5, 38, -49], opts={'r': 1.6}),
           P('rubble', 'rubble', pos=[8, 0, -55], opts={'r': 5, 'n': 24, 'size': 1.1, 'fly': 0.3}),
           P('whip', 'whip', on={'actor': 'cop', 'hand': 'R'}, opts={'length': 2.8, 'period': 0.6}),
           P('grass', 'tallGrass', pos=[0, 0, 4], opts={'w': 26, 'd': 10, 'h': 0.45, 'count': 240, 'seed': 6})],
    cams=[cam(0.0, [1, 2.0, 12], [1, 2.0, 11.7], [1, 6.3, -50], [1, 6.3, -50], lens=45)]))

# S22 26.00-28.80: "Oh, and the dog is dead.": the dog's grave, R.I.P., his framed portrait, flowers, a fresh mound; slow push-in; the
# handcuffed tornado and the turbine far behind
scenes.append(scene(22, 'S22', 'grassland', props=[
    P('stone', 'gravestone', pos=[0, 0, -3.5], opts={'w': 1.0, 'h': 1.25, 'handle': HANDLE, 'dogColor': '#C0711E', 'dogMuzzle': '#4A2816'}),
    P('mound', 'dirtMound', pos=[0.05, 0, -2.5], opts={'w': 1.35, 'd': 1.6, 'h': 0.3}),
    P('flowers', 'flowers', pos=[0.42, 0.25, -3.18], scale=1.4),
    P('turbine', 'windTurbine', pos=[-46, 0, -190], opts={'h': 60, 'rpm': 13}),
    P('tornado', 'tornado', pos=[-34, 0, -150], scale=3.0, opts=TORG),
    P('cuffs', 'bigCuffs', pos=[-34.5, 19.5, -146.5], opts={'r': 1.0}),
    P('grass', 'tallGrass', pos=[0, 0, -4.3], opts={'w': 7, 'd': 2.0, 'h': 0.6, 'count': 700, 'seed': 12}),
    P('grassL', 'tallGrass', pos=[-1.6, 0, -2.9], opts={'w': 1.6, 'd': 2.4, 'h': 0.5, 'count': 160, 'seed': 14}), P('grassR', 'tallGrass', pos=[1.7, 0, -2.9], opts={'w': 1.6, 'd': 2.4, 'h': 0.5, 'count': 160, 'seed': 15}),
    P('grass2', 'tallGrass', pos=[0, 0, -1.3], opts={'w': 3.4, 'd': 0.5, 'h': 0.22, 'count': 50, 'seed': 13})],
    cams=[cam(0.0, [0.1, 0.66, -0.75], [0.08, 0.68, -1.35], [0, 0.55, -3.5], [0, 0.56, -3.5], lens=50)]))

# the director reads a prop's yaw from 'ry' (degrees); rot carries only the pitch and roll (radians). Convert rot[1] once here.
import math
for sc_ in scenes:
    for p_ in sc_['props']:
        if 'rot' in p_ and 'ry' not in p_:
            p_['ry'] = round(math.degrees(p_['rot'][1]), 3)

# per-shot grade, calibrated from the per-shot L* / chroma deltas against the reference (shotstats.py, pass 8)
SHOT_GRADES = {
 "S1": "contrast(0.9) saturate(1.02) brightness(1.091)",
 "S2": "contrast(0.9) saturate(1.01) brightness(1.118)",
 "S3": "contrast(0.9) saturate(0.85) brightness(1.055)",
 "S4": "contrast(0.9) saturate(0.99) brightness(1.122)",
 "S5": "contrast(0.9) saturate(1.26) brightness(1.116)",
 "S6": "contrast(0.9) saturate(1.35) brightness(1.204)",
 "S7": "contrast(0.9) saturate(1.13) brightness(1.077)",
 "S8": "contrast(0.9) saturate(0.86) brightness(1.111)",
 "S9": "contrast(0.9) saturate(1.12) brightness(1.031)",
 "S10": "contrast(0.9) saturate(0.80) brightness(1.151)",
 "S11": "contrast(0.9) saturate(1.14) brightness(1.108)",
 "S12": "contrast(0.9) saturate(1.04) brightness(1.022)",
 "S13": "contrast(0.9) saturate(0.80) brightness(0.981)",
 "S14": "contrast(0.9) saturate(1.20) brightness(1.147)",
 "S15": "contrast(0.9) saturate(0.99) brightness(0.932)",
 "S16": "contrast(0.9) saturate(1.09) brightness(1.220)",
 "S17": "contrast(0.9) saturate(0.95) brightness(1.159)",
 "S18": "contrast(0.9) saturate(0.80) brightness(1.156)",
 "S19": "contrast(0.9) saturate(0.87) brightness(1.094)",
 "S20": "contrast(0.9) saturate(1.00) brightness(1.110)",
 "S21": "contrast(0.9) saturate(0.87) brightness(1.116)",
 "S22": "contrast(0.9) saturate(1.19) brightness(1.204)"
}
for sc_ in scenes:
    key = 'S8' if sc_['id'] in ('S8a', 'S8b') else sc_['id']
    if key in SHOT_GRADES: sc_['grade'] = SHOT_GRADES[key]

doc = {'version': 3, 'title': 'Replica: man lost his dog in a tornado', 'grade': 'contrast(0.9) saturate(1.0) brightness(1.06)', 'captionWords': 0, 'captionY': 0.81, 'tempo': 1.0,
       'voice': None, 'music': None, 'cast': {'mec': {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
                 'judge': {'preset': 'judge', 'facial': 'stubble', 'build': {'width': 0.86, 'headWidth': 1.3, 'headScale': 1.05}},
                 'cop': {'preset': 'cop', 'suit': '#1E2D4A', 'pants': '#1E2D4A', 'facial': 'none', 'build': {'width': 0.82, 'headWidth': 1.3}}}, 'scenes': scenes, 'total': CUTS[-1] / FPS}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'replica_tornado.json')
json.dump(doc, open(out, 'w'), indent=1)
print(out, len(scenes), 'scenes', doc['total'], 's')
