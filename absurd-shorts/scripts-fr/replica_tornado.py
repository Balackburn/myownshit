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


def cam(at, frm, to, look, look2=None, lens=60, ease='linear', shake=None, roll=None):
    c = {'at': at, 'from': frm, 'to': to, 'lookAt': look, 'lens': lens, 'ease': ease}
    if look2: c['lookAt2'] = look2
    if shake: c['shake'] = shake
    if roll: c['roll'] = roll     # degrees, about the view axis (+: the image turns clockwise)
    return c


def scene(i, sid, set_, actors=(), props=(), cams=(), **kw):
    st, du = span(i)
    return {'id': sid, 'set': set_, 'lines': [], 'actors': list(actors), 'props': list(props), 'sfx': [], 'cams': list(cams),
            'start': round(st, 6), 'duration': round(du, 6), **kw}


TOR = {'rings': 14, 'height': 7.3, 'base': 0.39, 'top': 2.03, 'taper': 0.6, 'flare': 0.0, 'crownFlare': 1.24, 'crownH': 1.15, 'crownSpike': 0.25, 'crownTeeth': 1.35, 'crownLayers': 2, 'chips': 30, 'teeth': True,
       'gap': 0.05, 'band': 1.3, 'spike': 0.0, 'bands': 0.3, 'spinJitter': 0.35, 'cols': ['#66726A', '#6E7A72', '#606C64', '#727E76'], 'paleColor': '#D3CCB8', 'stripe': '#B9B3A2', 'stripeDark': '#55615A'}   # measured profile: 1.54x taller than wide
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
s1cams += [cam(1.1, [0.4, 0.45, man_at(1.1)[2] - 2.5], [0.4, 0.45, WALK1 - 2.7], [-0.4, 1.45, man_at(1.1)[2]], [-0.4, 1.45, WALK1], lens=72)]   # low and tilted up at him from his front-left, like the original's f33-f56 (+0.02-0.03 on stills)
scenes.append(scene(1, 'S1', 'replicaStreet', setOpts={'near': 'cottage', 'z0': -44.2, 'nearTown': [5]},
    actors=[act('mec', [0, 0, WALK0], 180, 'walk', 'neutral', keys=[
        k(0.0, to=[0, 0, WALK1], dur=TW, clip='walk', then='stand'), k(1.28, clip='reachUpL')])],
    props=[P('dog', 'voxelDog', pos=[-0.7, 0, WALK0 + 1.1], rot=[0, 3.1416, 0], scale=1.0, opts={'walk': True}, keys=[
               k(0.0, to=[-0.7, 0, WALK1 - 0.55], dur=TW, ease='linear'),
               k(1.24, to=[-0.85, 1.0, WALK1 + 0.6], dur=0.07, ease='out'),
               k(1.31, to=[-8.5, 7.0, 26.0], dur=0.2, ease='linear')]),
           P('tornado', 'tornado', pos=[-8.5, 0, 28], scale=1.9, opts=TOR)],
    cams=s1cams, blur=[[1.26, 1.5, 0.015]],   # the original's orbit (f12-f28) is crisp: no shutter there; a short one on the throw
    tethers=[{'a': {'actor': 'mec', 'hand': 'L', 'offset': [0, -0.06, 0]}, 'b': {'prop': 'dog', 'offset': [0, 0.55, 0.28]}, 'color': '#C8322A', 'radius': 0.011, 'sag': 0.18, 'until': 1.3}]))

# S2 1.90-3.43: close tracking shot of the dog spinning in the tornado wall, mouth open
scenes.append(scene(2, 'S2', 'replicaStreet',
    props=[P('tornado', 'tornado', pos=[0, 0, -6.0], scale=3.6, opts={**TOR, 'chips': 10, 'spin': 4.0}),
           P('dog', 'voxelDog', pos=[-0.6, 6.2, 0], rot=[0.17, 0.6, 0.26], scale=1.25, opts={'open': True, 'paddle': True}, keys=[k(0.0, to=[0.1, 6.4, -0.3], dur=1.53, ease='linear')]),
           P('leash2', 'leash', on={'actor': 'dog', 'offset': [0, 0.53, 0.3]}, opts={'length': 1.5, 'elev': -1.25, 'color': '#C8322A'})],
    cams=[cam(0.0, [-0.55, 6.5, 2.7], [0.0, 6.6, 2.5], [-0.4, 6.42, 0], [0.12, 6.55, -0.2], lens=55)]))

# S3 3.43-4.50: close 3/4 shot from chest height on the near kerb, explaining hands; the camera looks across the road (-X) at the far houses
scenes.append(scene(3, 'S3', 'replicaStreet', setOpts={'farX': -34.0},
    actors=[act('mec', [-1.2, 0, 0], -8, 'explainLook', 'neutral', params={'yaw': 1.0})],   # chest 3/4 toward screen-left (hands clear of the lens), face to the camera
    cams=[cam(0.0, [-0.211, 0.912, 0.6], [-0.181, 0.922, 0.58], [-2.056, 2.027, -0.378], [-2.026, 2.047, -0.388], lens=74, shake=0.003)]))   # head 225 px tall, centred x ~350 (grid reads of f120)

# S4 4.50-6.53: selfie close-up on the far sidewalk (0.84 m from his face, camera just above eye level, nearly level, wide lens): the road on
# the right, the townhouses beyond the fence on the left, the tornado ~60 m down the road behind his head; at f151 he brings up the phone beside his face,
# screen to the camera, showing the creator's handle
scenes.append(scene(4, 'S4', 'replicaStreet',
    actors=[act('mec4', [-11.933, 0, 0], -5.5, 'stand', 'neutral', keys=[k(0.48, face=-16, turn=0.22), k(0.5, clip='showPhoneFaceL')])],   # turns with his selfie camera
    props=[P('phone', 'phone911', camLock=True, pos=[0.115, -0.674, -0.504], rot=[-0.077, -0.171, -0.38], scale=0.92, opts={'screen': 'handle'},
             keys=[k(0.0, visible=False), k(0.5, visible=True), k(0.5, to=[0.115, -0.196, -0.541], dur=0.14, ease='out')]),   # held up beside his face (camera space; top at y ~485 like f180)
           P('tornado', 'tornado', pos=[-0.5, 0, -77.3], scale=3.6, opts=TOR, keys=[k(0.48, to=[7.8, 0, -75], dur=0.22, ease='inOut')])],   # stays just right of his head through the swing (f136-f190)
    cams=[cam(0.0, [-11.825, 2.006, 0.982], [-11.825, 2.006, 0.982], [-11.883, 2.088, -0.073], [-11.883, 2.088, -0.073], lens=74),     # vanishing point x ~325, head 386 px tall at x ~230 (f136-f148)
          cam(0.48, [-11.825, 2.006, 0.982], [-12.07, 2.02, 0.8], [-11.883, 2.088, -0.073], [-11.957, 2.088, -0.07], lens=74, ease='inOut'),   # the selfie swing: 10.5 deg about his head, pulled in to 472 px (f149-f156)
          cam(0.7, [-12.07, 2.02, 0.8], [-12.04, 2.03, 0.79], [-11.957, 2.088, -0.07], [-11.937, 2.098, -0.07], lens=74)],   # vanishing point x ~200 (f160-f195)
    setOpts={'farFenceX': -13.5}))   # the original's walk is ~3 m wide: fence ~1.4 m left of the lens (its base meets x 0 at y ~760)   # solved from the head rows (top 347, chin 790): at head height, 0.8 m, tilted up 4.3 deg

# S5 6.53-7.03: extreme close-up from the jet's right side (camera at -X looking +X): the ribbed nozzle centre-right, a white-hot afterburner
# blasting frame-left over the runway, the tail fins above
scenes.append(scene(5, 'S5', 'runway', props=[P('jet', 'fighterJet', pos=[0, 0, 0], opts={'burner': 1.5, 'glow': 2.6, 'glowColor': '#FFE6B0', 'hotCore': True, 'gear': True})],
    cams=[cam(0.0, [-2.93, 1.3, -8.98], [-2.88, 1.31, -9.08], [-0.6, 1.5, -7.3], [-0.6, 1.5, -7.35], lens=50, shake=0.03)], blur=0.008))   # rear-left 3/4, close: one nozzle, its glowing mouth toward us (the original is 4x sharper than a 0.02 s shutter)

# S6 7.03-7.63: fast dolly above the jet's left side from the wing and its roundel (U.S. AIR FORCE on the fuselage) to the canopy and the
# nose wheel, the runway beyond (motion blur)
scenes.append(scene(6, 'S6', 'runway', props=[P('jet', 'fighterJet', pos=[0, 0, 0], opts={'burner': 1.0, 'glow': 4, 'gear': True})],
    cams=[cam(0.0, [-9.5, 8.5, -7.5], [-6.0, 3.4, 4.5], [-1.6, 1.5, -1.8], [-0.4, 0.8, 5.6], lens=50, ease='inOut', shake=0.02)], blur=0.005))   # the original's dolly is 3x sharper than a 0.012 s shutter

# S7 7.63-8.10: wide runway, the jet lifts off far away (dust behind it) and roars over the camera banking up-right (whip, motion blur)
scenes.append(scene(7, 'S7', 'runway',
    props=[P('jet', 'fighterJet', pos=[0, 0.2, -60], rot=[0, 0, 0.0], opts={'burner': 1.0, 'glow': 5, 'gear': True, 'missiles': 4}, keys=[k(0.0, to=[0, 2.0, -18], dur=0.3, ease='in'),
        k(0.3, to=[-2.0, 14.0, 4], dur=0.1, ease='linear'), k(0.4, to=[-5.0, 24.0, 22], dur=0.07, ease='linear'),   # stays ~15 m away as it climbs over
        k(0.28, rotTo=[-0.5, 0, -0.4], dur=0.12)]),   # passes over to the upper left (nozzles there by f242), banking   # wings level, then nose up and banking as it climbs over the camera (belly, then rear, f238-f242)
           P('dust', 'dustPuff', pos=[0, 0, -66], scale=6, opts={'color': '#D9C9A6', 'period': 0.8})],
    cams=[cam(0.0, [0, 1.4, 8], [0, 1.4, 8], [0, 2.5, -40], [0, 3.4, -40], lens=40),          # horizon y 523 -> 543 (measured), nearly still until f234
          cam(0.17, [0, 1.4, 8], [0, 1.4, 8], [0, 3.4, -40], [-0.8, 60.0, -5], lens=40, ease='in')],   # then a fast whip up: all sky by f240
    blur=[[0.3, 0.47, 0.02]], blurSamples=10))

def scene_f(sid, f0, f1, set_, actors=(), props=(), cams=(), **kw):
    """a scene between two reference frames (for shots split at an invisible cut, e.g. inside the S8 cloud white-out)"""
    return {'id': sid, 'set': set_, 'lines': [], 'actors': list(actors), 'props': list(props), 'sfx': [], 'cams': list(cams),
            'start': round(f0 / FPS, 6), 'duration': round((f1 - f0) / FPS, 6), **kw}


TORA = {**TOR, 'height': 8.6, 'base': 0.3, 'top': 1.45, 'taper': 1.0, 'crownFlare': 1.1, 'cols': ['#6A766E', '#76827A', '#5E6A62', '#808C84'], 'pale': 2, 'paleColor': '#D6CBAE',
        'bands': False, 'crownFlare': 1.15, 'crownH': 0.8, 'crownSpike': 0.0, 'crater': {'r0': 1.3, 'r1': 3.55, 'bands': [[2.15, 2.85]], 'rocksIn': 14, 'rockIn': 0.5, 'rocksOut': 26, 'rockOut': 0.24, 'tilt': -0.2,
                   'color': '#727C75', 'rockColor': '#7E8881'},   # darker crater: the original reads L*55 (rendered L ~ 0.86 x material + 11)
        'ribbons': 8, 'ribbonFlat': True, 'ribbonR': 3.4, 'ribbonY0': 0.95, 'ribbonDY': 0.1, 'ribbonW': 2.5, 'ribbonFlatTilt': 0.35,   # one broad cream band, a thick inner wall, wide loose ribbons (f300 crop)
        'dust': 0.8, 'chips': 40, 'stripe': '#8E8A78', 'stripeDark': '#4A554E'}   # the aerial look (S8b, S10): long striped body, a rock crater on top
JETA = {'burner': 0.45, 'glow': 2.3, 'glowColor': '#FF6A22', 'missiles': 4}   # smaller nozzle glow, like the original
V = 55.0                                                               # strike speed (m/s) of the jet + chase camera


def mv(p, dz, dx=0.0, dy=0.0):
    return [round(p[0] + dx, 3), round(p[1] + dy, 3), round(p[2] + dz, 3)]


# S8a 8.10-8.47: a locked chase measured on the original. The camera trails the climbing jet (wingspan 86% of the frame at f244,
# 74% at f249: the jet pulls away ~0.74 m a frame), seen from just above-right of its path, so the contrail it starts at f246 streams
# to the lower-left corner (its tail recedes ~9 m a frame: 270 m/s airspeed, camera 3.8 m off the path). The cloud deck pops in at
# f248 with its scalloped edge at y = 320 px and slides down the frame 166 px a frame as one piece (phase correlation: pure
# vertical shift), swallowing the jet at f249.7 and the frame at f252.5: a camera-locked cloud bank (cloudCurtain), 5 m away.
import math as _m8
def _rx(v, a): c, s_ = _m8.cos(a), _m8.sin(a); return [v[0], c * v[1] - s_ * v[2], s_ * v[1] + c * v[2]]
def _ry(v, a): c, s_ = _m8.cos(a), _m8.sin(a); return [c * v[0] + s_ * v[2], v[1], -s_ * v[0] + c * v[2]]
def _rz(v, a): c, s_ = _m8.cos(a), _m8.sin(a); return [c * v[0] - s_ * v[1], s_ * v[0] + c * v[1], v[2]]
def rot_xyz(rot, v): return _rx(_ry(_rz(v, rot[2]), rot[1]), rot[0])          # three.js Euler XYZ: R = Rx Ry Rz
def nrm3(v): n_ = _m8.sqrt(sum(x * x for x in v)); return [x / n_ for x in v]
def cross3(a_, b_): return [a_[1] * b_[2] - a_[2] * b_[1], a_[2] * b_[0] - a_[0] * b_[2], a_[0] * b_[1] - a_[1] * b_[0]]
def comb(*terms): return [round(sum(k_ * v[i] for k_, v in terms), 3) for i in range(3)]   # sum of scalar * vector
def euler_from_basis(X, Y, Z):                                                  # rotation whose columns are X, Y, Z -> Euler XYZ
    y_ = _m8.asin(max(-1.0, min(1.0, Z[0])))
    if abs(Z[0]) < 0.9999999: return [round(_m8.atan2(-Z[1], Z[2]), 5), round(y_, 5), round(_m8.atan2(-Y[0], X[0]), 5)]
    return [round(_m8.atan2(Y[2], Y[1]), 5), round(y_, 5), 0.0]
def view_basis(fwd):                                                            # three.js lookAt with world up: right, up
    z_ = [-c for c in fwd]; x_ = nrm3(cross3([0, 1, 0], z_)); return x_, cross3(z_, x_)
JROT8 = [1.05, 3.04, 0.08]; F8 = nrm3(rot_xyz(JROT8, [0, 0, 1])); VJ8 = 270.0; T8A = 11 / 30
RS8, US8 = view_basis(F8)
J8a = [0.0, -78.0, -40.0]; J8b = comb((1, J8a), (VJ8 * T8A, F8))
JC8 = rot_xyz(JROT8, [0, 1.6, -3.0]); NZ8 = rot_xyz(JROT8, [0, 1.6, -7.45])     # the jet's visual centre and nozzle centre, from its pivot
O8 = comb((3.8 * 0.491, RS8), (3.8 * 0.871, US8))                                  # camera offset from the path: up-right (trail -> lower-left corner)
def d8(t): return 24.5                                                            # camera -> jet distance, locked from f245 (wingspan ~80% of the frame)
def jet8(t): return comb((1, J8a), (VJ8 * t, F8))
def cam8(t, d=None, off=None): return comb((1, jet8(t)), (1, JC8), (-(d or d8(t)), F8), (1, off or O8))
def look8(t): return comb((1, jet8(t)), (1, JC8), (0.25, RS8), (0.1, US8))
CAM8_0 = cam8(0.0, 15.0, comb((-0.6, RS8), (-2.2, US8)))                          # f243: closer and below (nozzles above the wing line, banked look),
                                                                                 # pulling back to the locked chase by f245
# cloud bank 5 m ahead of the camera, tilted 7 deg (its edge is ~65 px higher on the right), edge y_px = 320 + 166 (f - 248)
def fpy(lens): return 512 / _m8.tan(_m8.radians(lens / 2))                       # focal length in px (1024 px tall frame)
def bank_keys(fys, f0, dc, lens):
    """camera-space slide of a camLock cloud bank: fys = [(frame, edge y px at the frame centre)], f0 = scene start frame"""
    at_ = lambda y: [0.0, round((512 - y) * dc / fpy(lens), 4), -dc]
    keys_ = [k(round((fa - f0) / 30, 4), to=at_(yb), dur=round((fb - fa) / 30, 4), ease='linear') for (fa, ya), (fb, yb) in zip(fys, fys[1:])]
    return at_(fys[0][1]), keys_
DECK8_POS, DECK8_KEYS = bank_keys([(243, 320 - 166 * 5), (254, 320 + 166 * 6)], 243, 5.0, 55)   # edge y = 320 + 166 (f - 248)
noz_at = lambda t: comb((1, jet8(t)), (1, NZ8))
scenes.append(scene_f('S8a', 243, 254, 'skyHigh', props=[
    P('jet', 'fighterJet', pos=J8a, rot=JROT8, opts={'burner': 0.25, 'glow': 1.3, 'glowColor': '#FFB050', 'missiles': 4,
        'contrail': {'t0': 3 / 30, 'speed': 270, 'len': 45, 'r': 0.17, 'color': '#F3EDE2', 'soft': 0.35}}, keys=[k(0.0, to=J8b, dur=T8A, ease='linear')]),
    P('deck', 'cloudCurtain', camLock=True, pos=DECK8_POS, rot=[0, 0, round(_m8.radians(7), 4)], opts={'w': 5.6, 'h': 9.0, 'r': 0.62, 'seed': 37, 'bright': '#F4E9D7', 'shadow': '#B9CADC', 'plate': '#DEDCD6'},
      keys=[k(0.0, visible=False), k(0.14, visible=True)] + DECK8_KEYS)],   # its edge ~65 px higher on the right
    cams=[cam(0.0, CAM8_0, cam8(2 / 30), look8(0.0), look8(2 / 30), lens=55),
          cam(2 / 30, cam8(2 / 30), cam8(T8A), look8(2 / 30), look8(T8A), lens=55)],
    setOpts={'layer': False, 'fog': False, 'sky': ['#5EAEE0', '#8ACBEE']}, blur=[[0, 0.025, 0.03], [0.025, 0.15, 0.006], [0.15, 1, 0.013]], blurSamples=12))

# S8b 8.47-10.43: white-out (the camera dives through a cloud), then the strike seen from above-behind. Camera solved from the reference
# (solve_cam: rim/base screen rows, rim width, house size; tornado scale 9): altitude 236 -> 160 m, 242 -> 121 m from the tornado, pitch
# 48 -> 54 deg; the jet 24 m ahead, nose-down, nozzles facing us; the lock-on HUD is a HyperFrames layer
import math as _m
TZ = -520.0; TS = 9.0                        # tornado position (z) and scale for the aerial shots
AERIAL_HAZE = {'color': '#EEECE6', 'near': 150, 'far': 600}   # the original's veil grows with distance: top band +12 L*, chroma 26 -> 9 (band L* 79/70/67/63 at f275 matched)
AER_SET = {'road': '#8C9096', 'roofs': ['#D05A62', '#C8505A', '#5E7EC4', '#8C6A76', '#D05A62', '#5A6072', '#C25862', '#8A5A58', '#6A86C8'], 'pitch': 11.5, 'pair': 42, 'back': 18, 'wallH': 1.45}   # the original's aerial town: houses close together, tall walls, pinkish reds, slate and mauve roofs, blue-grey roads
TS8B = 9.0                                   # S8b: crater width measured on grid overlays (270 px at f270, 350 at f290, 420 at f312)
def vdir(deg): return [0.0, -_m.sin(_m.radians(deg)), -_m.cos(_m.radians(deg))]
def ahead(c, deg, k=300.0): d = vdir(deg); return [round(c[i] + d[i] * k, 2) for i in range(3)]
def rel(c, r): return [round(c[0] + r[0], 2), round(c[1] + r[1], 2), round(c[2] + r[2], 2)]
def lerp3(a, b, u): return [round(a[i] + (b[i] - a[i]) * u, 2) for i in range(3)]
C8a, C8z = [0, 236, TZ + 242], [0, 175, TZ + 145]; P8a, P8z = 46.2, 51.0; T8 = 1.967     # pitch 1.9 deg up: the base sits at y 490 (f290);
# the end point pulled back 20%: the crater grows 270 -> 350 -> 420 px (f270, f290, f312) on the original
def c8(t): return lerp3(C8a, C8z, t / T8)
JR8a, JR8b = [-1.26, -22.83, -16.9], [0.14, -24.62, -14.22]         # jet relative to the camera at f270 and f312 (solved, x1.1: wingspan)
def cl_at(c, deg, k, off): p = ahead(c, deg, k); return [round(p[0] + off[0], 2), round(p[1] + off[1], 2), round(p[2] + off[2], 2)]
DECK8B_POS, DECK8B_KEYS = bank_keys([(254, -150), (255, -60), (256, 40), (257, 143), (258, 246), (259, 338), (260, 410), (261, 470), (262, 570), (263, 660),
                                      (266, 720), (270, 800), (275, 860), (281, 900), (285, 960), (290, 1110)], 254, 5.0, 50)
scenes.append(scene_f('S8b', 254, 313, 'aerialSuburb', props=[
    P('deck', 'cloudCurtain', camLock=True, pos=DECK8B_POS, rot=[-0.6, 0, 0.25], keys=DECK8B_KEYS,
      opts={'down': True, 'w': 6.0, 'h': 7.0, 'r': 0.45, 'seed': 41, 'bright': '#F4E9D7', 'shadow': '#BDCCDC', 'plate': '#E2DFD8'}),   # lower lumps nearer (tilted), edge higher on the right
    P('tornado', 'tornado', pos=[0, 0, TZ], scale=TS8B, opts=TORA),
    P('jet', 'fighterJet', pos=rel(C8a, JR8a), rot=[-0.89, 3.1416, 0.04], opts=JETA, keys=[      # hidden in the bank until it slides past (f260)
        k(0.0, to=rel(c8(0.533), JR8a), dur=0.533, ease='linear'), k(0.533, to=rel(C8z, lerp3(JR8a, JR8b, 1.0 + 1 / 42)), dur=T8 - 0.533, ease='linear')])],
    cams=[cam(0.0, C8a, C8z, ahead(C8a, P8a), ahead(C8z, P8z), lens=50, shake=0.12)], shadow={'size': 300, 'center': [0, 0, TZ + 120]}, setOpts={'houseScale': 1.3, 'gridRot': -0.33, 'x': 1100, **AER_SET},   # houses as big as the original's (bottom rows ~60-70 px; A/B +0.02-0.04)
    blur=[[0, 0.34, 0.008]], blurSamples=8, fog=AERIAL_HAZE, fogTo={'near': 110, 'far': 440}))   # the veil thickens as the camera drops (band L* 73/70/68 at f300)

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
    msl9.append({'from': st, 'ctrl': [round(st[0] + HD[0] * 20, 2), JY - 4.0, round(st[2] + HD[2] * 20, 2)], 'to': [round(st[0] + HD[0] * 170, 2), JY - 42 - 4 * i, round(st[2] + HD[2] * 170, 2)],
                 't0': t0, 'dur': 0.8, 'trail': 0.7, 'v0': 0.3})   # leave at the jet's speed (60 m/s), then race ahead
smk9 = [{'from': [round(-HD[0] * 70, 2), JY + 0.2, round(-HD[2] * 70, 2)], 'to': J9b, 't0': 0.0, 'dur': T9, 'body': False, 'hide': False, 'lin': True, 'trail': 0.75}]
CAM9 = [-1.7, -6.0, 43.0]
scenes.append(scene_f('S9', 313, 335, 'skyHigh', props=[
    P('jet', 'fighterJet', pos=J9a, rot=[0.6, -1.134, -0.15], opts={'burner': 0.5, 'glow': 2.6, 'missiles': 4}, keys=[k(0.0, to=J9b, dur=T9, ease='linear')]),
    P('msl', 'missileSalvo', opts={'size': 1.3, 'trailWidth': 0.12, 'glow': 1.6, 'shots': msl9}),
    P('smk', 'missileSalvo', opts={'size': 1.6, 'trailOpacity': 0.6, 'shots': smk9})],
    cams=[cam(0.0, rel(J9a, CAM9), rel(J9b, CAM9), rel(J9a, [-1.7, -6.0, -10]), rel(J9b, [-1.7, -6.0, -10]), lens=48, shake=0.06)],
    setOpts={'cz': -40, 'h': 30, 'n': 520, 'w': 1300, 'd': 1300, 'sky': ['#62AEE2', '#7CC2EC'], 'fogNear': 500, 'fogFar': 1800, 'fogColor': '#7DC2EC'}))

# S10 11.17-12.87: back on the chase. Camera fitted (fit10: Nelder-Mead on the crater width, top and bottom rows and the base row read on
# grid overlays at f335/f358/f374/f385, all within ~20 px): 229 -> 117 m up, pitch 48 -> 42.6 deg, a linear move; the crater is seen
# ~30 deg above its plane (ellipse half as tall as wide) and sits lower than in S8b (height factor 0.67). The jet is seen from above
# (wings in plan view), drifting left then back; ~40 missiles streak up from under the camera and converge on the crater
C10a, C10b = [0, 228.8, TZ + 262.6], [0, 117.4, TZ + 138.3]; P10a, P10b = 47.9, 42.6; T10 = 1.7
TORA10 = {**TORA, 'height': 5.76}                                              # the squat S10 tornado (crater at 53 m)
def scr(x, y, d, lens=50): f_ = fpy(lens); return [round((x - 288) * d / f_, 3), round((512 - y) * d / f_, 3), -d]   # camera space of a pixel at depth d
JET10 = [(335, 290, 630, 43.9), (348, 230, 650, 42.4), (360, 180, 685, 39.1), (372, 150, 720, 37.9), (385, 185, 735, 35.7)]   # (frame, x, y px, depth m): wingspan 285 -> 350 px (crops of f336-f385)
PHI10 = _m8.radians(14)                                                          # the jet's axis 14 deg flatter than the view: seen from behind (fuselage ~0.5x as tall as at 27)
JROT10 = euler_from_basis([-1, 0, 0], [0, _m8.cos(PHI10), _m8.sin(PHI10)], [0, _m8.sin(PHI10), -_m8.cos(PHI10)])
def bank10(deg): return [JROT10[0], JROT10[1], round(JROT10[2] + _m8.radians(deg), 4)]   # roll about the nose (+: left wing up)
BANK10 = [(335, 1), (348, 2), (360, -3), (372, -1), (385, -2)]                   # wing tips nearly level on crops of f336-f385
import random as _rnd
_r10 = _rnd.Random(10); salvo = []
for i in range(40):
    t0 = round(0.25 + i * 0.031 + _r10.uniform(-0.012, 0.012), 3)   # the main salvo builds up after the first wave (few trails at f348, a sheaf by f372)
    cp_ = lerp3(C10a, C10b, t0 / T10)
    st = [round(_r10.uniform(-60, 60), 2), round(_r10.uniform(6, 30), 2), round(cp_[2] - _r10.uniform(0, 60), 2)]   # low, under the camera's ground point: below the frame, ~180 m deep, so the trails stay thin
    an = _r10.uniform(0, 2 * _m8.pi); rr = _r10.uniform(6, 30)
    tgt = [round(rr * _m8.cos(an), 2), round(_r10.uniform(35, 82), 2), round(TZ + rr * _m8.sin(an), 2)]                      # round the crater
    salvo.append({'from': st, 'to': tgt, 't0': t0, 'dur': round(_r10.uniform(0.8, 1.15), 3), 'trail': 0.75, 'v0': 0.55})
def cam10_world(t, pc):                                                             # a camera-space point of S10 at time t, in world space
    u = t / T10; c_ = lerp3(C10a, C10b, u); la_, lb_ = ahead(C10a, P10a), ahead(C10b, P10b); l_ = lerp3(la_, lb_, u)
    z_ = nrm3([c_[i] - l_[i] for i in range(3)]); x_ = nrm3(cross3([0, 1, 0], z_)); y_ = cross3(z_, x_)
    return [round(c_[i] + x_[i] * pc[0] + y_[i] * pc[1] + z_[i] * pc[2], 2) for i in range(3)]
def jet10_at(t):                                                                   # the jet's camera-space position at t (linear between keys)
    f_ = 335 + t * 30
    for (fa, xa, ya, da), (fb, xb, yb, db) in zip(JET10, JET10[1:]):
        if f_ <= fb: w_ = (f_ - fa) / (fb - fa); return scr(xa + (xb - xa) * w_, ya + (yb - ya) * w_, da + (db - da) * w_)
    return scr(*JET10[-1][1:])
salvo1 = []
for i in range(10):                                                                # the first wave leaves from under the jet's wings (f335-f344)
    t0 = round(i * 0.03, 3); jp = jet10_at(t0); side = -1 if i % 2 else 1
    st = cam10_world(t0, [jp[0] + side * (2.0 + (i % 4) * 1.0), jp[1] - 0.8, jp[2] + 1.5])
    an = _r10.uniform(0, 2 * _m8.pi); rr = _r10.uniform(6, 26)
    salvo1.append({'from': st, 'to': [round(rr * _m8.cos(an), 2), round(_r10.uniform(40, 80), 2), round(TZ + rr * _m8.sin(an), 2)], 't0': t0, 'dur': round(_r10.uniform(1.0, 1.25), 3), 'trail': 0.12, 'v0': 0.75})   # they leave faster than the camera (~100 m/s); short trails, so the old smoke never reaches the lens
scenes.append(scene_f('S10', 335, 386, 'aerialSuburb', props=[
    P('tornado', 'tornado', pos=[0, 0, TZ], scale=TS, opts=TORA10),
    P('jet', 'fighterJet', camLock=True, pos=scr(*JET10[0][1:]), rot=bank10(BANK10[0][1]), opts={**JETA, 'burner': 1.0},
      keys=[k(round((fa - 335) / 30, 4), to=scr(*b_[1:]), dur=round((b_[0] - fa) / 30, 4), ease='linear') for (fa, *_), b_ in zip(JET10, JET10[1:])]
           + [k(round((fa - 335) / 30, 4), rotTo=bank10(rb), dur=round((fb - fa) / 30, 4)) for (fa, _), (fb, rb) in zip(BANK10, BANK10[1:])]),
    P('salvo', 'missileSalvo', opts={'size': 1.6, 'glow': 2.0, 'glowColor': '#FF8A30', 'flame': 1.4, 'flameW': 1.8, 'flameColor': '#F58A2E', 'core': '#FFF2B8', 'bodyColor': '#F4F4F2',
                                     'trailOpacity': 0.95, 'trailWidth': 0.2, 'trailBase': 0.12, 'shots': salvo}),   # white body, orange flame with a pale heart, opaque thin trail
    P('salvo1', 'missileSalvo', opts={'size': 1.0, 'glow': 1.3, 'glowColor': '#FF8A30', 'flame': 1.2, 'flameW': 1.5, 'flameColor': '#F58A2E', 'core': '#FFF2B8', 'bodyColor': '#F4F4F2',
                                      'trailOpacity': 0.95, 'trailWidth': 0.1, 'trailBase': 0.08, 'shots': salvo1})],   # the first wave, seen near the jet
    cams=[cam(0.0, C10a, C10b, ahead(C10a, P10a), ahead(C10b, P10b), lens=50)], shadow={'size': 300, 'center': [0, 0, TZ + 120]}, setOpts={'houseScale': 1.3, 'gridRot': -0.36, 'x': 1100, **AER_SET},   # houses as big as the original's (bottom rows ~60-70 px; A/B +0.02-0.03)
    fog=AERIAL_HAZE, fogTo={'near': 55, 'far': 330}))   # same veil all along the 229 -> 117 m descent (band L* 76/71/70 at f372, 73/72/72 at f384)

# S11 12.87-14.37: a low camera (0.4 m) on the road near the curb, solved on f406 from the curb and the walk's far edge (dense line fits),
# the door-frame tops and the street's vanishing point (x ~1300): yawed 38 deg along the street, pitched up 12.4, rolled -1.2; the fence
# top rises above the horizon as in the original. The missile hits the tornado behind
# the cottages, fireball and glare, then smoke, debris and a second hit lower right
scenes.append(scene(11, 'S11', 'cottageStreet', props=[
    P('tornado', 'tornado', pos=[25.97, 2.0, -36.42], scale=4.6, opts={**TOR, 'chips': 44}),
    P('boom1', 'fireball', pos=[22.27, 21.43, -30.66], opts={'t0': 0.06, 'size': 7.0, 'n': 90, 'seed': 3, 'glowShare': 1.0, 'glare': 1.0, 'flash': 0.5, 'flashScale': 1.3, 'life': 0.6, 'smokeColor': '#54473F', 'puff': 0.72}),   # one glowing mass, then brown-grey smoke
    P('boom2', 'fireball', pos=[24.9, 13.85, -28.91], opts={'t0': 0.86, 'size': 5.0, 'n': 22, 'seed': 9, 'smoke': 0.8, 'glowShare': 0.3, 'smokeColor': '#4A4441'}),
    P('msl', 'missileSalvo', opts={'size': 1.3, 'shots': [{'from': [30.97, 54.39, 18.71], 'to': [22.27, 21.43, -30.66], 't0': -0.2, 'dur': 0.26, 'trail': 0.5},
                                                         {'from': [34.03, 3.45, 16.66], 'to': [24.9, 13.85, -28.91], 't0': 0.56, 'dur': 0.3, 'trail': 0.6}]})],   # props re-placed along their old screen rays
    cams=[cam(0.0, [-3.33, 0.41, 2.01], [-3.33, 0.41, 2.01], [14.62, 6.87, -21.15], lens=68, roll=-1.24)], fx=[{'type': 'shake', 'at': 0.1, 'dur': 0.6, 'amount': 0.05}, {'type': 'shake', 'at': 0.88, 'dur': 0.4, 'amount': 0.03}], setOpts={'houseZ': -11.2, 'houses': [
        {'x': -0.5, 'w': 7.0, 'color': '#F4F2EC', 'roof': '#C9473A', 'eaves': True, 'door': '#2F7F8C', 'shutters': '#E3B33A', 'porchRoof': '#C9473A'},
        {'x': 6.0, 'w': 5.6, 'color': '#B8A6D9', 'roof': '#6A3A30', 'door': '#B5302A'}, {'x': 11.6, 'w': 5.6, 'color': '#E8A08A', 'roof': '#3E4A5E', 'door': '#2F5E8C'},
        {'x': 17.4, 'w': 5.8, 'color': '#EDCF7A', 'roof': '#B5402F'}, {'x': -7.6, 'w': 5.8, 'color': '#F0C6CF', 'roof': '#5E83C6'},
        {'x': -14.6, 'w': 6.0, 'color': '#A9C7E8', 'roof': '#B5402F', 'eaves': True}, {'x': 23.2, 'w': 5.8, 'color': '#F4F2EC', 'roof': '#3E4A5E'}]}))

# S12 14.37-16.10: high over the rows of side-gabled cottages, the tornado on the field beyond; strikes land among the houses, closer and
# closer. Camera solved from grid reads of f433 (horizon y 170, row fronts y 960 / 700, tornado base (325, 320), crown top y 85): 27 m up,
# pitch 16.6 deg, the nearest row 35 m ahead; houses 6.6 m wide on a 7.6 m pitch (eaves: ridge along the street, no porch). The blasts
# keep the screen positions measured in pass 15, re-projected onto the ground for this camera (sizes scaled by the new distance)
BLAST12 = {'glowShare': 0.9, 'flash': 0.4, 'glare': 0.35, 'life': 0.4, 'flashScale': 1.8, 'smoke': 0.8, 'smokeColor': '#3E3836', 'n': 40, 'puff': 1.0, 'spread': 0.35, 'rise': 0.7, 'lag': 0.02, 'growT': 0.15}   # white-hot core, dark smoke within ~0.3 s (f444 -> f453), a brief glare
B12 = [([-10.16, 4, -132.77], 0.433, 8.4, 4), ([10.6, 5, -89.77], 0.833, 7.4, 6), ([-7.01, 5, -43.62], 1.233, 6.4, 8), ([4.45, 3.5, -19.56], 1.633, 5.0, 10)]   # hits at f444/f456/f468/f480, above the roofs
MSL12 = [[40, 140, -190], [55, 140, -150], [45, 130, -95], [50, 120, -70]]
scenes.append(scene(12, 'S12', 'cottageRows', props=[
    P('tornado', 'tornado', pos=[7, 0, -178], scale=5.0, opts={**TOR, 'chips': 30})]
    + [P(f'b{i + 1}', 'fireball', pos=pos, opts={'t0': t0, 'size': sz, 'seed': sd, **BLAST12}) for i, (pos, t0, sz, sd) in enumerate(B12)]
    + [P('msl', 'missileSalvo', opts={'size': 2.2, 'shots': [{'from': MSL12[i], 'to': B12[i][0], 't0': round(B12[i][1] - 0.27, 2), 'dur': 0.27, 'trail': 0.6} for i in range(4)]})],
    cams=[cam(0.0, [0, 27, 38.8], [0.4, 27, 37.3], [0, 3.15, -41.2], [2.6, 3.15, -42.7], lens=48)], setOpts={'rows': 8, 'eaves': True, 'pitch': 8.6, 'overhang': 0.3, 'houseScale': 1.12,   # bigger detached houses on wider lots (A/B +0.008)
        'roofs': ['#7A4E3E', '#3F4E6B', '#A0473A', '#6B3B32', '#5A6577', '#8C4A3A'], 'walls': ['#F3E3C3', '#EFC9C9', '#BFDDB4', '#F2D58A', '#F2BCA2', '#CBDDF0', '#F4F2EC', '#E3D0EA']}))

# S13 16.10-17.63: "All of it.": the same streets in ruins, dark grade, a forest of smoke columns and fires, the tornado far behind
fl, sm = [], []
for j in range(9):
    for i in range(15):
        x = (i - 7) * 10.5 + (3.7 if j % 2 else 0); z = -j * 23
        fl.append([x + ((i * 13 + j) % 5 - 2) * 0.8, 0.5 + (i % 3) * 0.5, z + 2.0, 2.3 + (i + j) % 3 * 0.6])
        fl.append([x + 3.0, 0.4, z - 1.5, 1.8 + (i * j) % 3 * 0.5])
        fl.append([x - 2.6, 0.6, z + 0.5, 1.6 + (i + 2 * j) % 3 * 0.4])
        sm.append([x - 2.2, z - 1, 22 + (i * j % 5) * 3, 1.2])
        sm.append([x + 2.6, z - 3, 19 + (i % 4) * 3, 0.8])
scenes.append(scene(13, 'S13', 'cottageRows', props=[
    P('tornado', 'tornado', pos=[18, 0, -435], scale=13.5, opts={**TOR, 'chips': 30, **{k_: v_ for k_, v_ in TORL.items() if k_ in ('cols', 'stripe', 'stripeDark', 'paleColor')}}),   # crown ~173 px wide, top y ~40 (grid reads)
    P('fires', 'flameField', opts={'points': fl, 'seed': 3}),
    P('smoke', 'smokeField', opts={'points': [[x_, z_, h_ * 0.8, y_] for x_, z_, h_, y_ in sm], 'size': 0.86, 'per': 30, 'seed': 5, 'twist': 13, 'twistAmp': 0.55, 'color': '#3B3533'})],   # twisted rope-like columns
    cams=[cam(0.0, [0, 23.5, 40], [0.4, 23.5, 39.5], [0, 2.5, -60], [2.4, 2.5, -60.5], lens=48)], setOpts={'burnt': True, 'rows': 13, 'houseScale': 1.25}))   # bigger shells (A/B +0.007-0.010)

# S14 17.63-19.47: on the burnt road, low camera tilted up 18.6 deg (grid reads of f545: road vanishing point y 810, tornado base y ~805,
# crown 340 px wide), the tornado ~30 m away waves a white flag; neutral light (the original's road is its raw asphalt colour #2B2A2F)
scenes.append(scene(14, 'S14', 'ruinedStreet', props=[
    P('tornado', 'tornado', pos=[0, 0, -25.5], rot=[0, 0, -0.08], scale=2.3, opts={**TOR, 'height': 6.2, 'top': 2.0, 'taper': 1.0, 'base': 0.22, 'bands': False, 'pale': 2, 'crownSpike': 0.2, 'chips': 40, 'spin': 0.8, **{k_: v_ for k_, v_ in TORL.items() if k_ in ('cols', 'stripe', 'stripeDark', 'paleColor')}}, keys=[k(0.0, to=[0, 0, -22.5], dur=1.83, ease='linear')]),   # shorter, wider
    P('flag', 'whiteFlag', pos=[1.4, 15.3, -21.0], rot=[0, 0, -0.32], scale=3.6, opts={'w': 1.6, 'h': 1.45, 'pole': 1.75, 'glow': '#A8A49E'}, keys=[k(0.0, to=[1.4, 15.3, -18.0], dur=1.83, ease='linear')])],   # the crown leans right ~4.5 deg (f560: top centre x 340 over a base at 280); cloth at x 373-560
    cams=[cam(0.0, [0.3, 0.6, 6], [0.3, 0.6, 5.4], [0, 12.7, -30], [0, 12.8, -30], lens=60)], light={'key': '#E6E4E0', 'sky': '#CFCFCF', 'ground': '#3E3E44'},
    setOpts={'flameScale': 1.6, 'road': '#302F36'}))   # renders ~#2B2A2F like the original's asphalt

# --- act 3: court, hard labour, grave ----------------------------------------------------------------------------
HANDLE = '@outofthisworld_9'
TORC = {**TOR, 'cols': ['#7C8A82', '#8C9A92', '#6E7C74', '#96A49C'], 'paleColor': '#E2DCCB', 'stripe': '#E4DECF'}      # lit by the courtroom
TORS = {**TOR, 'cols': ['#5E6962', '#646F68', '#5A655E', '#68736C'], 'pale': 2, 'paleColor': '#C2C5B9', 'bands': False, 'chips': 40}          # S17/S18: strong light/dark stripes
TORG = {**TORS, 'cols': ['#68736B', '#6E7970', '#646F67', '#727D75'], 'pale': None, 'bands': False, 'gap': 0.03, 'ribbons': 4, 'ribbonFollow': True, 'ribbonGap': 1.03,
        'ribbonY0': 0.16, 'ribbonDY': 0.64, 'ribbonH': 7.5, 'ribbonArc': 4.8, 'ribbonTilt': 0.62, 'ribbonColor': '#CEC4A8', 'ribbonSpeed': 3,
        'stripe': '#4E5852', 'stripeDark': '#4A544E'}   # S19-S21: dark body, thin pale spiral bands

# S15 19.47-20.23: the tornado in the dock, giant white handcuffs; the judge tiny at the bench behind; slow push-in
scenes.append(scene(15, 'S15', 'replicaCourt', setOpts={'handle': HANDLE},
    actors=[act('judge', [0, -0.15, -14.0], 0, 'idle')],
    props=[P('dock', 'dock', pos=[0, 0, 0], opts={'w': 7.5, 'd': 6.5, 'h': 1.5}),
           P('tornado', 'tornado', pos=[-0.7, 0.43, 0], rot=[0, 0, 0.13], scale=1.08, opts={**TORC, 'cols': ['#9AA8A0', '#A8B5AE', '#8E9C94', '#B2BFB8'], 'chips': 36, 'spin': 0.27}),   # crown at the frame top, base y ~840
           P('cuffs', 'bigCuffs', pos=[-0.9, 6.0, 3.4], opts={'r': 0.95})],
    cams=[cam(0.0, [2.5, 3.0, 13.7], [2.3, 3.1, 12.6], [-0.96, 4.6, 0], [-1.41, 4.7, 0], lens=50)]))   # tornado centred near x 280 like the original

# S16 20.23-21.60: low on the bench, the judge strikes the gavel (raise f607-613, hit on the block at f619), slow push-in
scenes.append(scene(16, 'S16', 'replicaCourt', setOpts={'handle': HANDLE, 'windowX': -1.5, 'chairW': 1.2, 'chairH': 2.75, 'chairX': 0.15, 'benchGlow': '#5A564A'},
    actors=[act('judge', [-0.35, -0.3, -14.0], -35, 'gavelStrikeL', params={'hit': 0.4})],
    props=[P('specs', 'glasses', on={'actor': 'judge', 'joint': 'head', 'offset': [0.02, 0.17, 0.15]}, opts={'r': 0.042, 'dx': 0.07}),
           P('gavelUp', 'gavel', on={'actor': 'judge', 'hand': 'L'}, keys=[k(0.0, visible=True), k(0.38, visible=False)]),
           P('gavel', 'gavel', pos=[-0.37, 1.41, -13.3], rot=[0, 0, -1.5708], keys=[k(0.0, visible=False), k(0.38, visible=True)]),   # head upright on the block, handle to his hand
           P('block', 'soundBlock', pos=[0.1, 1.18, -13.3])],                     # in frame right of the judge (it sat 20 deg off-axis, outside the frame)
    cams=[cam(0.0, [-0.05, 1.27, -11.5], [-0.07, 1.28, -11.75], [-0.27, 1.55, -14.0], [-0.27, 1.55, -14.0], lens=45)],
    fx=[{'type': 'shake', 'at': 0.4, 'dur': 0.18, 'amount': 0.018}]))

# S17 21.60-22.33: low wide on the field: the handcuffed tornado spins in front of the wind turbine
scenes.append(scene(17, 'S17', 'grassland', props=[
    P('turbine', 'windTurbine', pos=[-11, 0, -72], opts={'h': 60, 'rpm': 13, 'label': HANDLE}),    # just behind the tornado, its tower showing on the left
    P('tornado', 'tornado', pos=[-1.3, 0, -38], scale=3.6, opts={**TORS, 'cols': ['#6E7A72', '#76827A', '#6A766E', '#7E8A82'], 'pale': None, 'bands': 0.5, 'bandEvery': 1,
      'height': 8.5, 'top': 1.5, 'spin': 1.8}),                                      # narrow, tall, pale stripes on every ring
    P('cuffs', 'bigCuffs', pos=[-3.4, 22.0, -30.2], opts={'r': 1.6}),           # outside the body (it hid them), ~110 px wide
    P('rubble', 'rubble', pos=[-1.3, 0, -38], opts={'r': 3.2, 'n': 18, 'size': 0.8}),
    P('grass', 'tallGrass', pos=[0, 0, 4], opts={'w': 26, 'd': 10, 'h': 0.5, 'count': 260, 'seed': 4})],
    cams=[cam(0.0, [0, 1.2, 12], [0, 1.25, 11.4], [-2, 23.2, -40], [-2, 24.6, -40], lens=52)]))   # tilted up ~23 deg (rows of f660)

# S18 22.33-23.57: from the tornado's crown, looking up at the hub, the rotor spins up into a blur
TORS18 = {**TORG, 'cols': ['#7E8A80', '#86928A', '#76827A', '#8E9A92'], 'stripe': '#7A867E', 'stripeDark': '#6E7A72', 'crownSpike': 0.0, 'crownH': 1.3,
          'crownFlare': 1.15, 'crater': {'r0': 1.0, 'r1': 2.8, 'y': 7.25, 'dish': 0.12, 'bands': [[1.6, 1.8], [2.05, 2.25]], 'rocksIn': 10, 'rockIn': 0.26, 'rocksOut': 18,
          'rockOut': 0.17, 'color': '#7E8A82', 'rockColor': '#8A968E'}}   # the turbine stands in the crater crown: a drum, smooth light body, thin tan spirals
scenes.append(scene(18, 'S18', 'grassland', props=[
    P('turbine', 'windTurbine', pos=[1.2, 0, -20], opts={'h': 31, 'rpm': 34, 'blur': 1.4, 'blurSpread': 0.7, 'label': HANDLE}),   # planted in the crater, left of its centre: hub at y ~267
    P('tornado', 'tornado', pos=[3.1, 2.0, -20], scale=2.0, opts=TORS18),         # crown 30 m out, ~70% of the width, rim at y ~790 like the original
    P('cuffs', 'bigCuffs', pos=[1.1, 16.1, -15.4], opts={'r': 0.75}),
    P('clouds', 'cloudCurtain', camLock=True, pos=[0, -10.1, -50], opts={'down': True, 'w': 34, 'h': 16, 'r': 1.9, 'seed': 18, 'bright': '#FBFAF6', 'shadow': '#C6D6E6',
      'plate': '#EEF2F5'})],                                                       # above the cloud deck: white puffs behind the crown, top edge y ~733
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
    cams=[cam(0.0, [0, 2.0, 10], [0, 2.0, 9.6], [-1, 6.3, -50], [-2.2, 6.3, -50], lens=45)]))

# S20 24.13-25.53: the officer strides in and cracks the whip at the tornado's base, boulders fly; the camera pans with him
scenes.append(scene(20, 'S20', 'grassland',
    actors=[act('cop', [-1.9, 0, -6], 90, 'stand', keys=[k(0.0, to=[-0.5, 0, -6], dur=1.15, clip='whipWalk', then='stand'), k(1.15, face=0)])],
    props=[P('whip', 'whip', on={'actor': 'cop', 'hand': 'R'}, opts={'length': 2.8, 'period': 0.6}),
           P('tornado', 'tornado', pos=[6.5, 0, -11], scale=5.4, opts={**TORG, 'cols': ['#7E8A80', '#86928A', '#76827A', '#8E9A92'], 'stripe': '#7A867E', 'stripeDark': '#6E7A72'}),   # close and lit: light body, tan swirls
           P('rubble', 'rubble', pos=[6.5, 0, -11], opts={'r': 3.6, 'n': 30, 'size': 0.7, 'fly': 0.4}),
           P('turbine', 'windTurbine', pos=[-12, 0, -70], opts={'h': 60, 'rpm': 13, 'label': HANDLE}),
           P('grass', 'tallGrass', pos=[0, 0, -4], opts={'w': 16, 'd': 6, 'h': 0.32, 'count': 160, 'seed': 8})],
    cams=[cam(0.0, [-1.3, 1.05, -0.1], [-0.6, 1.05, -0.1], [-0.9, 1.45, -6], [-0.1, 1.45, -6], lens=50, shake=0.01)]))   # 5.9 m back: officer ~466 px tall, kept left of centre as he strides

# S21 25.53-26.00: wide again, the officer whipping at the base
scenes.append(scene(21, 'S21', 'grassland',
    actors=[act('cop', [-1.5, 0, -50], 90, 'whipWalk')],
    props=[P('turbine', 'windTurbine', pos=[-21, 0, -132], opts={'h': 60, 'rpm': 13, 'label': HANDLE}),
           P('tornado', 'tornado', pos=[8, 0, -55], scale=5.4, opts=TORG),
           P('cuffs', 'bigCuffs', pos=[7.5, 38, -49], opts={'r': 1.6}),
           P('rubble', 'rubble', pos=[8, 0, -55], opts={'r': 5, 'n': 24, 'size': 1.1, 'fly': 0.3}),
           P('whip', 'whip', on={'actor': 'cop', 'hand': 'R'}, opts={'length': 2.8, 'period': 0.6}),
           P('grass', 'tallGrass', pos=[0, 0, 4], opts={'w': 26, 'd': 10, 'h': 0.45, 'count': 240, 'seed': 6})],
    cams=[cam(0.0, [1, 2.0, 12], [1, 2.0, 11.7], [1, 6.3, -50], [0.6, 6.6, -50], lens=45, shake=0.08)]))

# S22 26.00-28.80: "Oh, and the dog is dead.": the dog's grave, R.I.P., his framed portrait, flowers, a fresh mound; slow push-in; the
# handcuffed tornado and the turbine far behind
scenes.append(scene(22, 'S22', 'grassland', props=[
    P('stone', 'gravestone', pos=[0, 0, -3.5], opts={'w': 1.0, 'h': 1.25, 'handle': HANDLE, 'dogColor': '#E0AC72', 'dogMuzzle': '#5A3420', 'dogYaw': 0.0, 'dogPitch': 0.35, 'dogEyes': 1.1,
                                                      'dogTongue': 'long', 'ripW': 0.95, 'ripH': 0.26, 'ripY': 0.15, 'baseW': 1.28, 'frameW': 0.77, 'frameH': 0.92, 'frameTop': 0.25,
                                                      'dogScale': 1.9, 'dogY': 0.03}),   # measured on f820: base 1.28 x the stone, frame 0.77 x 0.74 of it, its top 0.2 below the arch
    P('mound', 'dirtMound', pos=[0.15, 0, -2.05], opts={'w': 0.78, 'd': 1.15, 'h': 0.24, 'color': '#6E4630'}),   # 400 px wide, right of centre (f820)
    P('flowers', 'flowers', pos=[0.43, 0.0, -3.05], scale=1.1),   # on the grass in front of the base's right end, heads at y ~580
    P('turbine', 'windTurbine', pos=[-152, 0, -700], opts={'h': 60, 'rpm': 13}),   # small, on the horizon behind the tornado (x ~50, 120 px tall)
    P('tornado', 'tornado', pos=[-28.4, 0, -150], scale=3.0, opts=TORG),
    P('cuffs', 'bigCuffs', pos=[-28.9, 19.5, -146.5], opts={'r': 1.0}),
    P('grass', 'tallGrass', pos=[0, 0, -4.3], opts={'w': 7, 'd': 2.0, 'h': 0.6, 'count': 900, 'seed': 12, 'thin': 0.022, 'cols': ['#8CC86A', '#A3D47A', '#7BB85C', '#B2DC88']}),
    P('grassL', 'tallGrass', pos=[-0.85, 0, -2.7], opts={'w': 0.8, 'd': 1.4, 'h': 0.62, 'count': 260, 'seed': 14, 'thin': 0.022, 'cols': ['#8CC86A', '#A3D47A', '#7BB85C', '#B2DC88']}), P('grassR', 'tallGrass', pos=[1.0, 0, -2.7], opts={'w': 0.6, 'd': 1.4, 'h': 0.58, 'count': 200, 'seed': 15, 'thin': 0.022, 'cols': ['#8CC86A', '#A3D47A', '#7BB85C', '#B2DC88']}),
    P('grass2', 'tallGrass', pos=[0, 0, -1.3], opts={'w': 3.4, 'd': 0.5, 'h': 0.32, 'count': 45, 'seed': 13, 'thin': 0.045, 'soft': 0.55, 'cols': ['#9ED27C', '#B2DC8C', '#8CC86A', '#C0E29A']})],   # out-of-focus foreground
    cams=[cam(0.0, [-0.05, 0.50, 0.25], [-0.07, 0.52, -0.55], [-0.15, 0.356, -3.5], [-0.12, 0.425, -3.5], lens=50)]))   # end framing nudged 0.4 deg right/up (phase correlation: 7 px left, 9 px down)   # lower and level: horizon at y ~450, stone top y ~160 -> 96 (f790/f850)

# the director reads a prop's yaw from 'ry' (degrees); rot carries only the pitch and roll (radians). Convert rot[1] once here.
import math
for sc_ in scenes:
    for p_ in sc_['props']:
        if 'rot' in p_ and 'ry' not in p_:
            p_['ry'] = round(math.degrees(p_['rot'][1]), 3)

# per-shot grade, calibrated from the per-shot L* / chroma deltas against the reference (shotstats.py, pass 8)
# per-shot softness (Gaussian px) so our edges match the original's sharpness (median Laplacian variance per shot, pass 34)
SOFTEN = {'S1': 0.5, 'S2': 0.62, 'S3': 0.49, 'S4': 0.35, 'S7': 0.42, 'S8a': 0.58, 'S11': 0.33, 'S14': 0.55, 'S16': 0.33, 'S17': 0.46,
          'S18': 0.37, 'S19': 0.4, 'S20': 0.52, 'S21': 0.49, 'S22': 0.46}
SHOT_GRADES = {
 "S1": "contrast(0.9) saturate(1.02) brightness(1.091)",
 "S2": "contrast(0.9) saturate(1.01) brightness(1.118)",
 "S3": "contrast(0.9) saturate(0.85) brightness(1.055)",
 "S4": "contrast(0.9) saturate(0.99) brightness(1.122)",
 "S5": "contrast(0.9) saturate(1.26) brightness(1.116)",
 "S6": "contrast(0.9) saturate(1.35) brightness(1.204)",
 "S7": "contrast(0.9) saturate(1.13) brightness(1.077)",
 "S8a": "contrast(0.9) saturate(0.86) brightness(1.111)",
 "S8b": "contrast(0.97) saturate(1.04) brightness(1.0)",
 "S9": "contrast(0.9) saturate(1.12) brightness(1.031)",
 "S10": "contrast(0.97) saturate(1.06) brightness(1.01)",
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
    key = sc_['id']
    if key in SHOT_GRADES: sc_['grade'] = SHOT_GRADES[key]
    if key in SOFTEN: sc_['soften'] = SOFTEN[key]

doc = {'version': 3, 'title': 'Replica: man lost his dog in a tornado', 'grade': 'contrast(0.9) saturate(1.0) brightness(1.06)', 'captionWords': 0, 'captionY': 0.81, 'tempo': 1.0,
       'voice': None, 'music': None, 'cast': {'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},   # skin tint: face #CB9765 -> #B7906A (S3)
                 'mec4': {'preset': 'lemec', 'tint': '#D4E6FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},   # S4's close, bright key: #E8A768 -> #BF966E
                 'judge': {'preset': 'judge', 'facial': 'stubble', 'atlas': 'lemec', 'atlasBody': False, 'build': {'width': 0.86, 'headWidth': 1.3, 'headScale': 1.05}},
                 'cop': {'preset': 'cop', 'suit': '#1E2D4A', 'pants': '#1E2D4A', 'facial': 'none', 'atlas': 'lemec', 'atlasBody': False, 'build': {'width': 0.82, 'headWidth': 1.3}}}, 'scenes': scenes, 'total': CUTS[-1] / FPS}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'replica_tornado.json')
json.dump(doc, open(out, 'w'), indent=1)
print(out, len(scenes), 'scenes', doc['total'], 's')
