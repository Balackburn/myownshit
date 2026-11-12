#!/usr/bin/env python3
"""L'aimant (story 47, cycle 9 of the cartoon staging): this man swallowed a magnet. Since then all metal jumps on him: the forks, the keys, the
frying pan. Even the street lamps bow as he passes. And the compasses no longer show the north: they show him. Hikers, boats, planes: everybody comes
to his door. The cartographers ruled: the north, from now on, is him. All the maps were redrawn. He lives at the North Pole. Third floor, no lift.
Staging: every gag is a magnet's pull on a man: the gulp and the crossed eyes, the cutlery that leaves the counter and sticks to his chest, a fan of
forks thunking in one after another, the keys on his cheek, the pan that flattens his face, the lamp posts that lean after him like sunflowers, the
compass needles that all swing to him, the crowd, the boat and the plane under his window, the map that turns on the wall to put him at the top, the
globe that stops with his block on the pole, a polar bear on his sofa, the explorers who plant their flag on his doormat. Natural look."""
from story_kit import *
import math

st = Story('aimant', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L03', 2), ('S05', 'L03', 4), ('S06', 'L04', 0), ('S07', 'L05', 0), ('S08', 'L06', 0),
         ('S09', 'L07', 0), ('S10', 'L07', 1), ('S11', 'L07', 2), ('S12', 'L08', 0), ('S13', 'L09', 0), ('S14', 'L10', 0), ('S15', 'L11', 0), ('S16', 'L12', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(22, 70), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)

# ---- the kitchen (kitchenDay: the counter along the back wall at z -3.3, its top at 0.95; the stove plate at the right)
ME = [-0.6, 0, -2.3]; MRY = 60                                      # he stands at the left, turned toward the counter on the right and three-quarter to us
FWD = (math.sin(math.radians(MRY)), math.cos(math.radians(MRY))); RGT = (-FWD[1], FWD[0])   # his front and his right (he faces +X+Z: his right is +Z... toward the camera side)
def ON_BODY(lat, y, out=0.21):                                      # a point on the front of his chest: lat (m, + = his right), y (height)
    return r3([ME[0] + out * FWD[0] + lat * RGT[0], y, ME[2] + out * FWD[1] + lat * RGT[1]])
KIT = {'fridge': True}
BODY = lambda: [ON_BODY(-0.5, 1.45, 0.0), ON_BODY(0.5, 1.45, 0.0)]                    # (first look) his shoulders: framing points (his centre alone left half of him out of the frame)
CS = 2.2                                                            # (first look) cutlery at cartoon size (life size it did not show)
HEADY = 2.05
def FLY(pid, name, frm, to, t, dur=0.12, fan=0.0, opts=None, scale=CS):   # a piece of metal leaves its place and flies to him, flat against his chest
    return P(pid, name, pos=frm, rot=[0, math.radians(MRY), fan], scale=scale, opts=opts or {}, keys=[k(round(t - 0.2, 3), to=[frm[0], frm[1] + 0.02, frm[2]], dur=0.2),   # it shivers first
             k(t, to=to, dur=dur, ease='in'), k(round(t + dur, 3), squash=[1.2, 0.8, 1.2], dur=0.0), k(round(t + dur + 0.05, 3), squash=[1.0, 1.0, 1.0], dur=0.06)])
JOLT = lambda t, s=1.0: [k(round(t, 3), toon={'sq': [1 + 0.06 * s, 1 - 0.07 * s, 1 + 0.06 * s], 'face': {'eye': 0.35 * s, 'brow': 0.6}}, toonDur=0.025), k(round(t + 0.07, 3), toon={'face': {'brow': 0.3}}, toonDur=0.06)]

# 1: this man swallowed a magnet. Close: he looks at the red horseshoe magnet in his fingers like a sweet, pops it in: a gulp goes down; his eyes cross
D1 = st.dur('S01'); IN1 = 0.62
MAG1 = [round(ME[0] + 0.36 * FWD[0] + 0.06 * RGT[0], 3), 1.55, round(ME[2] + 0.36 * FWD[1] + 0.06 * RGT[1], 3)]   # (first look) at his chest, where he looks down at it
HOLD1 = ['face', 0.06, -0.55, 0.36, 1, 0.05]; MOUTH1 = ['face', 0.02, 0.24, 0.06, 1, 0.04]
st.shot('S01', 'kitchenDay', setOpts=KIT, actors=[
        act('mec', ME, MRY, 'stand', 'neutral', keys=[k(0.0, look=MAG1), k(0.0, toon={'touch': {'R': HOLD1}, 'hands': {'R': 'pinch'}, 'face': {'brow': 0.5, 'gy': 0.6}}, toonDur=0.0),
            k(0.25, toon={'touch': {'R': HOLD1}, 'hands': {'R': 'pinch'}, 'face': {'brow': 0.8, 'gy': 0.6, 'jaw': 0.15}}, toonDur=0.1),   # mm, a sweet
            k(round(IN1 - 0.16, 3), toon={'touch': {'R': MOUTH1}, 'hands': {'R': 'pinch'}, 'face': {'jaw': 0.5}}, toonDur=0.14, toonEase='in'),   # in it goes
            k(IN1, toon={'touch': {'R': ['face', 0.02, 0.2, 0.14, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'face': {'jaw': 0.0, 'puff': 0.6}}, toonDur=0.05), k(round(IN1 + 0.08, 3), toon={'face': {'gulp': 0.0, 'eye': 0.3}}, toonDur=0.02),
            k(round(IN1 + 0.1, 3), toon={'face': {'gulp': 1.0, 'eye': 0.4}}, toonDur=0.28), k(round(IN1 + 0.1, 3), look='camera'),   # the gulp goes down
            k(round(IN1 + 0.34, 3), toon={'face': {'gulp': 1.0, 'eye': 0.3}, 'sq': [1.06, 0.92, 1.06], 'bend': {'neck': [0, 0, 0, 0.6, None]}}, toonDur=0.06, toonEase='in'),   # (pass 2) the head sinks into the collar...
            k(round(IN1 + 0.42, 3), toon={'face': {'cross': 1.0, 'brow': 0.8, 'pop': 0.35, 'tremble': 1}, 'sq': [0.95, 1.07, 0.95]}, toonDur=0.04, toonEase='outBack'),   # ...then the take, the crossed eyes shivering   # clink: his eyes cross
            k(round(IN1 + 0.7, 3), toon={'face': {'cross': 1.0, 'brow': 0.8, 'pop': 0.3, 'tremble': 1}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.08), k(round(IN1 + 1.0, 3), toon={'face': {'cross': 0.6, 'brow': 0.5, 'lid': 0.3}}, toonDur=0.2)])],
        props=[P('mag1', 'magnet', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.03, 0.04]}, opts={'s': 0.22, 'glow': [0.0, IN1]}, keys=[k(round(IN1 - 0.02, 3), scale=0.01, dur=0.04)])],
        cams=[FC(0.0, [0.55, 1.9, -0.6], [[ME[0], 2.4, ME[2]], [ME[0], 1.2, ME[2]], MAG1, *BODY()], top=0.16, bottom=0.7, drift=(-0.05, 0, -0.08))])
st.cue('sfx:gulp', 'S01', IN1 + 0.1, 0.45); st.cue('clang', 'S01', IN1 + 0.42, 0.15)

# 2: since then all metal jumps on him. Wider: the cutlery on the counter shivers, then flies across and sticks flat on his chest, clink, clink, clink
D2 = st.dur('S02'); JMP2 = round(st.at('S02', 'L02', 5) - 0.04, 3)
CUT2 = [('f1', 'fork', [0.55, 0.96, -3.12], -0.12, 1.42, -0.35), ('s1', 'spoon', [0.85, 0.96, -3.15], 0.1, 1.55, 0.25), ('f2', 'fork', [1.15, 0.96, -3.1], -0.02, 1.3, 0.05),
        ('s2', 'spoon', [1.4, 0.96, -3.14], 0.16, 1.36, -0.2), ('f3', 'fork', [0.7, 0.96, -3.0], -0.18, 1.62, 0.4)]   # (id, kind, on the counter, across his chest, height, fan)
st.shot('S02', 'kitchenDay', setOpts=KIT, actors=[
        act('mec', ME, MRY, 'stand', 'unimpressed', keys=[k(0.0, look=[1.0, 1.0, -3.1]), k(round(JMP2 - 0.3, 3), toon={'face': {'brow': 0.7, 'eye': 0.3}}, toonDur=0.08),
            *[x for i in range(len(CUT2)) for x in JOLT(JMP2 + 0.12 + 0.05 * i, 0.8)], k(round(JMP2 + 0.5, 3), look='camera'), k(round(JMP2 + 0.5, 3), expr='unimpressed')])],
        props=[FLY(f'c{i}', kind, frm, ON_BODY(lat, y), round(JMP2 + 0.05 * i, 3), fan=fan) for i, (pid, kind, frm, lat, y, fan) in enumerate(CUT2)],
        cams=[FC(0.0, [2.3, 1.55, 0.9], [[ME[0], 2.4, ME[2]], [ME[0], 0.0, ME[2]], [1.5, 1.0, -3.2], [0.4, 1.0, -3.2], *BODY()], top=0.14, bottom=0.74, drift=(-0.06, 0, -0.08))])
st.cue('sfx:ticks', 'S02', JMP2 - 0.25, 0.25); [st.cue('clang', 'S02', round(JMP2 + 0.12 + 0.05 * i, 3), 0.2) for i in range(len(CUT2))]

# 3: the forks. Close on him: a volley of forks zips in from the drawer at the right and thunks into a fan on his chest, one jolt each
D3 = st.dur('S03'); V3 = [round(0.12 + 0.11 * i, 3) for i in range(6)]
FAN3 = [(-0.15, 1.48, -0.5), (0.0, 1.58, -0.15), (0.15, 1.5, 0.3), (-0.08, 1.32, -0.3), (0.1, 1.3, 0.45), (0.02, 1.7, 0.1)]
DRAWER = [1.3, 0.85, -2.95]
st.shot('S03', 'kitchenDay', setOpts=KIT, actors=[
        act('mec', ME, MRY, 'stand', 'unimpressed', keys=[k(0.0, look=DRAWER), *[x for t in V3 for x in JOLT(t + 0.1, 1.0)], k(0.85, look='camera'), k(0.85, toon={'face': {'lid': 0.35, 'brow': 0.2}}, toonDur=0.1)])],
        props=[*[P(f'v{i}', 'fork', pos=DRAWER, rot=[0, math.radians(MRY), fan], scale=CS, keys=[k(0.0, visible=False), k(round(t - 0.01, 3), visible=True), k(t, to=ON_BODY(lat, y, 0.22), dur=0.1, ease='in'),
                 k(round(t + 0.1, 3), squash=[1.25, 0.75, 1.25], dur=0.0), k(round(t + 0.15, 3), squash=[1, 1, 1], dur=0.05)]) for i, ((lat, y, fan), t) in enumerate(zip(FAN3, V3))],
               *[P(f'old{i}', kind, pos=ON_BODY(lat, y), rot=[0, math.radians(MRY), fan], scale=CS) for i, (pid, kind, frm, lat, y, fan) in enumerate(CUT2)]],
        cams=[FC(0.0, [0.4, 1.75, -0.95], [[ME[0], 2.35, ME[2]], [ME[0], 1.1, ME[2]], [DRAWER[0] - 0.4, 1.2, DRAWER[2]], *BODY()], top=0.14, bottom=0.72, drift=(-0.04, 0, -0.05))])
[st.cue('thud', 'S03', round(t + 0.1, 3), 0.2) for t in V3]

# 4: the keys. The key ring flies off its hook by the door and smacks his cheek; it stays there, swinging
D4 = st.dur('S04'); K4 = 0.22
HOOK4 = [-2.4, 1.55, -1.6]
CHEEK4 = [round(ME[0] + 0.24 * FWD[0] + 0.2 * RGT[0], 3), 2.02, round(ME[2] + 0.24 * FWD[1] + 0.2 * RGT[1], 3)]
FORKS_ON = lambda: [*[P(f'cf{i}', kind, on={'actor': 'mec', 'joint': 'torso', 'offset': [round(-lat, 3), round(y - 1.0, 3), 0.2], 'rot': [0, 0, fan]}, scale=CS) for i, (pid, kind, frm, lat, y, fan) in enumerate(CUT2)],
                    *[P(f'cv{i}', 'fork', on={'actor': 'mec', 'joint': 'torso', 'offset': [round(-lat, 3), round(y - 1.0, 3), 0.21], 'rot': [0, 0, fan]}, scale=CS) for i, (lat, y, fan) in enumerate(FAN3)]]   # everything stuck on his chest from now on
st.shot('S04', 'kitchenDay', setOpts=KIT, actors=[
        act('mec', ME, MRY, 'stand', 'unimpressed', keys=[k(0.0, look=HOOK4), k(K4, toon={'bend': {'neck': [0, -0.35, 0, 1, None]}, 'face': {'lidR': 0.8, 'brow': 0.7, 'eye': 0.3}, 'sq': [1.04, 0.96, 1.04]}, toonDur=0.03, toonEase='out'),   # smack: the head knocked aside, an eye shut
            k(round(K4 + 0.2, 3), toon={'bend': {'neck': [0, -0.08, 0, 1, None]}, 'face': {'lidR': 0.3, 'brow': 0.4}}, toonDur=0.15), k(round(K4 + 0.2, 3), look='camera')])],
        props=[*FORKS_ON(), P('keys4', 'keyRing', pos=HOOK4, scale=2.4, keys=[k(K4 - 0.12, to=CHEEK4, dur=0.12, ease='in'), k(K4, visible=False)]),
               P('keys4b', 'keyRing', on={'actor': 'mec', 'joint': 'head', 'offset': [-0.2, 0.3, 0.08]}, scale=2.4, keys=[k(0.0, visible=False), k(K4, visible=True)])],
        cams=[FC(0.0, [0.1, 1.95, -0.55], [[ME[0], 2.4, ME[2]], [ME[0], 1.35, ME[2]], CHEEK4, *BODY()], top=0.16, bottom=0.7)])
st.cue('clang', 'S04', K4, 0.3)

# 5: the frying pan. It leaves the stove and flattens his face: BONG; it stays stuck on, stars round his head
D5 = st.dur('S05'); P5 = 0.24
STOVE5 = [1.35, 1.02, -3.2]
FACE5 = [round(ME[0] + 0.3 * FWD[0], 3), HEADY, round(ME[2] + 0.3 * FWD[1], 3)]
st.shot('S05', 'kitchenDay', setOpts=KIT, actors=[
        act('mec', ME, MRY, 'stand', 'unimpressed', keys=[k(0.0, look=STOVE5), k(round(P5 - 0.12, 3), toon={'face': {'eye': 0.5, 'brow': 1}}, toonDur=0.05),
            k(P5, toon={'scl': {'head': [1.32, 1.02, 0.5]}, 'sq': [1.08, 0.92, 1.08], 'face': {'stars': 1, 'brow': 0.8}, 'lay': [-0.08, 0]}, toonDur=0.02, toonEase='out'),   # flat-faced, rocked back
            k(round(P5 + 0.14, 3), toon={'scl': {'head': [1.3, 1.0, 0.52]}, 'face': {'stars': 1}, 'lay': [-0.06, 0]}, toonDur=0.04),   # (pass 2) held flat four frames
            k(round(P5 + 0.2, 3), toon={'scl': {'head': [0.86, 1.22, 1.15]}, 'face': {'stars': 1, 'pop': 0.3}, 'lay': [0.02, 0]}, toonDur=0.05, toonEase='out'),   # the pan drops: the head pops back past round
            k(round(P5 + 0.28, 3), toon={'scl': {'head': [1.06, 0.96, 1.0]}, 'face': {'stars': 1}}, toonDur=0.06),
            k(round(P5 + 0.3, 3), toon={'scl': {'head': [1.18, 1.0, 0.66]}, 'face': {'stars': 1}, 'hands': {'L': 'spread', 'R': 'spread'}}, toonDur=0.12)])],
        props=[*FORKS_ON(), P('keys5', 'keyRing', on={'actor': 'mec', 'joint': 'head', 'offset': [-0.2, 0.3, 0.08]}, scale=2.4),
               P('pan5', 'pan', pos=STOVE5, rot=[PI / 2, math.radians(MRY) + PI, 0], rotOrder='YXZ', opts={'r': 0.17}, keys=[k(round(P5 - 0.14, 3), to=FACE5, dur=0.14, ease='in'), k(P5, visible=False)]),
               P('pan5b', 'pan', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.25, 0.24], 'rot': [PI / 2, 0, 0]}, opts={'r': 0.2}, keys=[k(0.0, visible=False), k(P5, visible=True), k(round(P5 + 0.2, 3), visible=False)]),   # (pass 2) flat on his face, then down
               P('pan5c', 'pan', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.05, 0.05, 0.24], 'rot': [-PI / 2, 0, -0.5]}, opts={'r': 0.17}, keys=[k(0.0, visible=False), k(round(P5 + 0.2, 3), visible=True)])],
        fx=[{'type': 'shake', 'at': P5, 'dur': 0.12, 'amount': 0.012}],
        cams=[FC(0.0, [round(ME[0] + 2.0 * FWD[0], 3), 1.95, round(ME[2] + 2.0 * FWD[1], 3)], [[ME[0], 2.5, ME[2]], [ME[0], 1.35, ME[2]], *BODY()], top=0.16, bottom=0.72)])   # (pass 2) face-on: the pan lands flat on his face
st.cue('clang', 'S05', P5, 0.55); st.cue('sfx:boing', 'S05', P5 + 0.03, 0.3)

# ---- the street (parisStreet): he walks along the right-hand pavement toward +Z, covered in cutlery, the pan stuck on his chest now
PX = 6.6; STREET = {'clear': [-80, 80], 'eiffel': False, 'paveW': 6.5}
STUCK = lambda: [*FORKS_ON(), P('keysS', 'keyRing', on={'actor': 'mec', 'joint': 'head', 'offset': [-0.2, 0.3, 0.08]}, scale=2.4),
                 P('panS', 'pan', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.05, 0.05, 0.24], 'rot': [-PI / 2, 0, -0.5]}, opts={'r': 0.17})]

# 4 (line): even the street lamps bow as he passes. Low from the road: three lamp posts lean toward him as he comes level, then spring back
D6 = st.dur('S06'); Z6 = (-3.6, 3.4); LAMPZ = (-2.0, 0.6, 3.0); LAMPX = 5.3   # (pass 2) a little further out: clear of him
def lean6(zl):
    tl = (zl - Z6[0]) / (Z6[1] - Z6[0]) * D6                         # when he is level with it
    return [k(round(max(0.0, tl - 0.62), 3), rotTo=[0, 0, 0.05], dur=0.12, ease='inOut'), k(round(max(0.0, tl - 0.48), 3), rotTo=[0, 0, -0.42], dur=0.34, ease='inOut'), k(round(tl + 0.12, 3), rotTo=[0, 0, 0.12], dur=0.22, ease='inOut'),
            k(round(tl + 0.34, 3), rotTo=[0, 0, -0.05], dur=0.16, ease='inOut'), k(round(tl + 0.5, 3), rotTo=[0, 0, 0.0], dur=0.14, ease='inOut')]   # (pass 2) a little counter-lean, then over the pavement toward him, back past upright   # toward him (+X: ry 180 turns +Z rotation that way), then back past upright, settling
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [PX, 0, Z6[0]], 0, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, to=[PX, 0, Z6[1]], dur=D6, clip='walk', then='walk', ease='linear', face=0)])],
        props=[*STUCK(), *[P(f'lamp{i}', 'streetLamp', pos=[LAMPX, 0, z], ry=180, keys=lean6(z)) for i, z in enumerate(LAMPZ)]],
        cams=[FC(0.0, [4.3, 0.65, 8.6], [[PX, 2.5, Z6[0]], [PX, 0.0, 0.6], [LAMPX, 4.6, LAMPZ[0]], [LAMPX, 4.6, LAMPZ[2]], [LAMPX - 0.6, 0.0, LAMPZ[2]]], top=0.1, bottom=0.74, drift=(0.0, 0.0, -0.6))])   # (first look) low in front of him, down the pavement: the lamps lean sideways toward him as he walks at us (from the side they leaned into the depth)
[st.cue('sfx:squeak', 'S06', round((z - Z6[0]) / (Z6[1] - Z6[0]) * D6 - 0.3, 3), 0.2) for z in LAMPZ]

# 5 (line): and the compasses no longer show the north. Over a hiker's shoulder, looking down at his compass: the needle leaves N, whirls, and points
#    at our man walking past behind
D7 = st.dur('S07'); H7 = [PX - 1.4, 0, 6.5]; ME7 = [PX + 0.4, 0, 9.4]
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[
        act('rando', H7, 20, 'stand', 'neutral', keys=[k(0.0, look=[H7[0] + 0.2, 0.9, H7[2] + 0.5]), k(0.0, toon={'reach': {'R': [round(H7[0] + 0.1, 3), 1.42, round(H7[2] + 0.55, 3), 1, 0.05]}, 'hands': {'R': 'flat'}}, toonDur=0.0),   # (pass 2) higher, further out
            k(0.85, toon={'reach': {'R': [round(H7[0] + 0.1, 3), 1.42, round(H7[2] + 0.55, 3), 1, 0.05]}, 'hands': {'R': 'flat'}, 'face': {'brow': 0.8, 'eye': 0.3}}, toonDur=0.1)]),
        act('mec', ME7, -90, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, to=[PX - 1.2, 0, 9.6], dur=D7, clip='walk', then='walk', ease='linear', face=-90)])],
        props=[*STUCK(), P('backpack7', 'backpack', on={'actor': 'rando', 'joint': 'torso', 'offset': [0, 0.42, -0.24]}),
               P('comp7', 'compass', on={'actor': 'rando', 'hand': 'R', 'offset': [0, 0.03, 0.12], 'rot': [0, PI, 0]}, scale=3.4, opts={'path': [[0.0, ME7[0], 1.4, ME7[2]], [D7, PX - 1.2, 1.4, 9.6]], 'spin': [0.35, 0.95], 'north': [0, 0, -1]})],
        cams=[FC(0.0, [round(H7[0] - 0.7, 3), 3.05, round(H7[2] - 0.45, 3)], [[round(H7[0] + 0.1, 3), 1.32, round(H7[2] + 0.55, 3)], [round(H7[0] + 0.1, 3), 1.55, round(H7[2] + 0.7, 3)], [PX - 0.4, 2.3, 9.5], [PX - 0.4, 0.4, 9.5]], top=0.1, bottom=0.8)])   # (first look) high over his right shoulder, looking down: the dial big in the middle, our man walking past beyond it   # (first look) over his right shoulder and above it (behind his head the frame was his skull and his backpack)
st.cue('sfx:zip', 'S07', 0.35, 0.25)

# 6 (line): they show him. Three passers-by on the pavement, each with a compass turned to us: every needle points at him in the middle; he steps
#    aside: every needle swings after him; « lui »: all three heads turn to him
D8 = st.dur('S08'); Z8 = (9.4, 14.6); X8 = round(PX + 1.2, 3); LUI8 = round(st.at('S08', 'L06', 3) - 0.08, 3)
ZL8 = round(Z8[0] + (Z8[1] - Z8[0]) * LUI8 / D8, 3)                    # (pass 2) where he is at « lui »: a gap in the row there
ROW8 = [('rando', [round(PX - 0.45, 3), 0, round(ZL8 - 1.45, 3)], -95), ('mamie', [round(PX - 0.45, 3), 0, round(ZL8 - 0.55, 3)], -90), ('touriste', [round(PX - 0.45, 3), 0, round(ZL8 + 0.85, 3)], -85)]   # (first look) a row facing the road and us (from behind them their compasses were hidden)
ZAT8 = lambda t: round(Z8[0] + (Z8[1] - Z8[0]) * t / D8, 3)
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [X8, 0, Z8[0]], 0, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, to=[X8, 0, Z8[1]], dur=D8, clip='walk', then='walk', ease='linear', face=0)]),   # he walks along behind them, taller than them
        *[act(n, p, ry, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': [round(p[0] + 0.3 * math.sin(math.radians(ry)), 3), 1.4, round(p[2] + 0.3 * math.cos(math.radians(ry)), 3), 1, 0.05]}, 'hands': {'R': 'flat'}}, toonDur=0.0),
                                                 k(LUI8, look=[X8, 2.0, ZAT8(LUI8 + 0.1)]), k(LUI8, toon={'reach': {'R': [round(p[0] + 0.3 * math.sin(math.radians(ry)), 3), 1.4, round(p[2] + 0.3 * math.cos(math.radians(ry)), 3), 1, 0.05]}, 'hands': {'R': 'flat'}, 'face': {'brow': 0.6, 'eye': 0.3}}, toonDur=0.08)]) for n, p, ry in ROW8]],   # « lui »: the heads turn back to him
        props=[*STUCK(), P('backpack8', 'backpack', on={'actor': 'rando', 'joint': 'torso', 'offset': [0, 0.42, -0.24]}),
               *[P(f'comp8{i}', 'compass', on={'actor': n, 'hand': 'R', 'offset': [0, 0.03, 0.15], 'face': 'camera'}, scale=3.0, opts={'upright': True, 'path': [[0.0, X8, 1.6, Z8[0]], [D8, X8, 1.6, Z8[1]]]}) for i, (n, p, ry) in enumerate(ROW8)]],   # every needle follows him along
        cams=[FC(0.0, [1.2, 3.4, 12.0], [[ROW8[0][1][0], 2.3, round(ROW8[0][1][2] - 0.4, 3)], [ROW8[2][1][0], 2.3, round(ROW8[2][1][2] + 0.4, 3)], [X8, 2.55, ZL8], [ROW8[1][1][0], 0.3, ZL8]], top=0.14, bottom=0.74)])   # from the road: the row and their compasses, him walking behind
#   (pass 2) raised to 3.4 m, the row shifted half a metre on, him further back: he walks behind them, so from head height he was hidden behind each in turn; from above, his head and chest clear theirs
st.cue('sfx:zip', 'S08', 0.1, 0.2)

# ---- his building: a block on the right-hand side of the street (flatsWall, three floors over the shops); his window, the middle of the third floor
FX = 8.6; FLATS = lambda: P('flats', 'flatsWall', pos=[FX, 0, 30.0], ry=-90, opts={'w': 6.0, 'h': 12.6, 'cols': 3, 'rows': 3, 'depth': 1.25, 'y0': 3.0})
WIN = [round(FX + 0.62, 3), 9.0, 30.0]                              # he stands in his window, third floor
HIM_WIN = lambda keys=(): act('mec', WIN, -90, 'stand', 'unimpressed', keys=[k(0.0, look=[PX, 0.5, 30.0]), *keys])
CROWD = [('rando', [PX - 0.5, 0, 28.8], 75), ('rando2', [PX - 0.9, 0, 29.6], 80), ('touriste', [PX - 0.6, 0, 31.2], 105)]
LOOKUP = lambda n, p, ry, t0=0.0: act(n, p, ry, 'stand', 'neutral', keys=[k(t0, look=[WIN[0], WIN[1] + 1.6, WIN[2]]), k(0.0, toon={'reach': {'R': [round(p[0] + 0.25 * math.sin(math.radians(ry)), 3), 1.35, round(p[2] + 0.25 * math.cos(math.radians(ry)), 3), 1, 0.05]}, 'hands': {'R': 'flat'}}, toonDur=0.0)])
CROWD_PROPS = lambda: [P('bpA', 'backpack', on={'actor': 'rando', 'joint': 'torso', 'offset': [0, 0.42, -0.24]}), P('bpB', 'backpack', on={'actor': 'rando2', 'joint': 'torso', 'offset': [0, 0.42, -0.24]}, opts={'color': '#B5532A'}),
                       *[P(f'cc{i}', 'compass', on={'actor': n, 'hand': 'R', 'offset': [0, 0.03, 0.07]}, scale=2.2, opts={'target': [WIN[0], WIN[1] + 1.4, WIN[2]]}) for i, (n, p, ry) in enumerate(CROWD)]]

# 7 (line): hikers, — at the foot of his block: three hikers with backpacks arrive, compasses out, the needles pointing up at his window
D9 = st.dur('S09')
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[HIM_WIN(), *[act(n, [p[0] - 1.6, 0, p[2] - 1.2], ry, 'stand', 'neutral', keys=[k(0.0, look=[WIN[0], WIN[1] + 1.6, WIN[2]]), k(0.0, to=p, dur=0.55, clip='walk', then='stand', ease='out'),
                                                                                                                        k(0.0, toon={'reach': {'R': [round(p[0] - 1.6 + 0.25 * math.sin(math.radians(ry)), 3), 1.35, round(p[2] - 1.2 + 0.25 * math.cos(math.radians(ry)), 3), 1, 0.05]}, 'hands': {'R': 'flat'}}, toonDur=0.0),
                                                                                                                        k(0.55, toon={'reach': {'R': [round(p[0] + 0.25 * math.sin(math.radians(ry)), 3), 1.35, round(p[2] + 0.25 * math.cos(math.radians(ry)), 3), 1, 0.05]}, 'hands': {'R': 'flat'}}, toonDur=0.1)]) for n, p, ry in CROWD]],
        props=[FLATS(), *CROWD_PROPS()],
        cams=[FC(0.0, [3.2, 0.9, 25.5], [[PX - 0.9, 2.4, 29.6], [PX - 0.5, 0.0, 28.8], [PX - 0.6, 2.4, 31.2], [FX, 11.0, 30.0]], top=0.08, bottom=0.74, drift=(0.06, 0, 0.1))])

# 7 (line): boats, — a sailboat on its trailer rolls in and stops under his window, its skipper holding up a compass
D10 = st.dur('S10'); BOAT = [4.4, 0, 33.4]
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[HIM_WIN(), *[LOOKUP(n, p, ry) for n, p, ry in CROWD],
        act('skipper', [4.4, 1.0, 33.4 - 6.0], 0, 'stand', 'neutral', keys=[k(0.0, look=[WIN[0], WIN[1] + 1.6, WIN[2]]), k(0.0, to=[4.4, 1.0, 33.4], dur=0.45, glide=True, ease='out', face='keep'),
            k(0.0, toon={'reach': {'R': [4.6, 2.6, 33.5, 1, 0.05]}, 'hands': {'R': 'flat'}}, toonDur=0.0)])],
        props=[FLATS(), *CROWD_PROPS(), P('boat', 'sailboat', pos=[BOAT[0], 0, BOAT[2] - 6.0], ry=-90, keys=[k(0.0, to=BOAT, dur=0.45, ease='out'), k(0.45, squash=[1.0, 0.94, 1.0], dur=0.0), k(0.5, squash=[1, 1, 1], dur=0.08)]),
               P('cskip', 'compass', on={'actor': 'skipper', 'hand': 'R', 'offset': [0, 0.03, 0.07]}, scale=2.2, opts={'target': [WIN[0], WIN[1] + 1.4, WIN[2]]})],
        cams=[FC(0.0, [1.6, 1.0, 27.0], [[BOAT[0], 4.6, BOAT[2]], [BOAT[0] - 1.0, 0.0, BOAT[2] - 1.6], [BOAT[0], 0.0, BOAT[2] + 1.6], [PX - 0.6, 2.4, 31.2]], top=0.1, bottom=0.74)])

# 7 (line): planes: everybody comes to his place. Wide from the road: a little plane taxis in and stops, propeller turning; the hikers, the boat;
#    up at his window he leans out, deadpan
D11 = st.dur('S11'); PLANE = [1.2, 0, 26.0]
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[HIM_WIN(keys=[k(0.9, look='camera'), k(0.9, toon={'face': {'lid': 0.4}}, toonDur=0.15)]), *[LOOKUP(n, p, ry) for n, p, ry in CROWD],
        act('skipper', [4.4, 1.0, 33.4], 0, 'stand', 'neutral', keys=[k(0.0, look=[WIN[0], WIN[1] + 1.6, WIN[2]])])],
        props=[FLATS(), *CROWD_PROPS(), P('boat', 'sailboat', pos=BOAT, ry=-90), P('plane', 'propPlane', pos=[PLANE[0], 0, PLANE[2] - 9.0], ry=-90, scale=0.75, opts={'prop': 6},
               keys=[k(0.0, to=PLANE, dur=0.85, ease='out'), k(0.85, squash=[1.0, 0.95, 1.0], dur=0.0), k(0.92, squash=[1, 1, 1], dur=0.1)])],
        cams=[FC(0.0, [-1.2, 2.0, 15.0], [[FX, 11.4, 30.0], [PLANE[0], 0.0, PLANE[2] + 2.0], [PLANE[0], 2.2, PLANE[2] + 2.0], [round(PLANE[0] + 3.1, 3), 1.5, round(PLANE[2] + 0.4, 3)], [BOAT[0], 4.4, BOAT[2]], [PX - 0.6, 0.0, 31.2]], top=0.08, bottom=0.74, drift=(0.08, 0.04, 0.12)),   # (first look) wider: the window, the crowd, the boat, the plane's nose and its right wing
              FC(1.0, [round(WIN[0] - 3.4, 3), 9.9, round(WIN[2] + 1.4, 3)], [[WIN[0], 11.3, WIN[2]], [WIN[0], 9.2, WIN[2]], [round(WIN[0] - 0.2, 3), 10.2, round(WIN[2] - 0.6, 3)], [round(WIN[0] - 0.2, 3), 10.2, round(WIN[2] + 0.6, 3)]], top=0.14, bottom=0.66, drift=(0.05, 0.0, -0.05))])   # then up at his window: he leans on the sill, deadpan, and looks at us
st.cue('engine', 'S11', 0.0, 0.35, 1.0)

# ---- the cartographers' office: a wall map of France, two cartographers in lab coats and glasses
MAP = [-0.4, 1.75, -3.55]; CART = [('carto1', [-1.65, 0, -2.55], 25), ('carto2', [0.9, 0, -2.5], -25)]
# 8 (line): the cartographers ruled. Two cartographers at the map: one taps the compass rose with a long pointer, the other nods hard
D12 = st.dur('S12')
TAP12 = [round(MAP[0] - 0.6, 3), round(MAP[1] + 0.35, 3), round(MAP[2] + 0.06, 3)]
st.shot('S12', 'office', setOpts={'door': False}, actors=[
        act('carto1', CART[0][1], CART[0][2], 'stand', 'determined', keys=[k(0.0, look=TAP12), *[k(round(0.2 + 0.3 * i, 3), toon={'reach': {'R': [round(TAP12[0] + 0.05 * (i % 2), 3), TAP12[1], round(TAP12[2] + (0.02 if i % 2 else 0.12), 3), 1, 0.08]}, 'hands': {'R': 'point'}, 'hose': 0.12}, toonDur=0.08) for i in range(4)], k(1.1, look='camera')]),
        act('carto2', CART[1][1], CART[1][2], 'stand', 'neutral', keys=[k(0.0, look=TAP12), *[k(round(0.35 + 0.2 * i, 3), toon={'bend': {'neck': [0.35 if i % 2 == 0 else -0.1, 0, 0, 1, None]}}, toonDur=0.08) for i in range(5)]])],
        props=[P('map', 'mapFrance', pos=MAP, opts={'w': 1.5, 'h': 1.2, 'pin': [0.62, 0.66]})],   # (his arm stretches to the map: the pointer is his finger)
        cams=[FC(0.0, [-0.2, 1.6, 1.6], [[MAP[0] - 0.8, 2.4, MAP[2]], [MAP[0] + 0.8, 1.1, MAP[2]], [CART[0][1][0], 2.35, CART[0][1][2]], [CART[1][1][0], 2.35, CART[1][1][2]], [CART[0][1][0], 0.6, CART[0][1][2]]], top=0.12, bottom=0.74)])

# 9 (line): the north, from now on, is him. Close on the map: the N of the rose is crossed out in red, a fat arrow is drawn to his face on the map
#    (NORD); then the whole map turns on the wall so that he comes to the top
D13 = st.dur('S13'); CR13, ROT13, AR13 = 0.1, 0.35, (1.05, 1.45)   # (pass 2) crossed out, turned over, then the arrow up to him
M13 = [0.25, 2.02, -3.5]                                             # (pass 2) the close-up cheats the map 0.65 m right and up: the window frame cut its left corner, the desks its bottom one
st.shot('S13', 'office', setOpts={'door': False}, actors=[],
        props=[P('map', 'mapFrance', pos=M13, opts={'w': 1.5, 'h': 1.2, 'pin': [0.62, 0.66], 'cross': CR13, 'arrow': list(AR13), 'rotate': [[ROT13, -10.0], [round(ROT13 + 0.12, 3), 150.0], [round(ROT13 + 0.55, 3), 136.0]], 'wordRot': 136})],
        cams=[cam(0.0, [M13[0], round(M13[1] - 0.08, 3), 1.95], [M13[0], round(M13[1] - 0.06, 3), 1.75], [M13[0], round(M13[1] - 0.05, 3), M13[2]], [M13[0], round(M13[1] - 0.03, 3), M13[2]], lens=40)])   # (pass 2) the whole map, the rose inside the frame, room for the turn
st.cue('sfx:scratch', 'S13', CR13, 0.3); st.cue('sfx:scratch', 'S13', AR13[0], 0.3); st.cue('sfx:squeak', 'S13', ROT13, 0.25)
st.card('S13', 'NORD', at=round(AR13[1], 3))

# 10 (line): all the maps were redrawn. The globe on the desk is spun; it slows and stops with his little block of flats on the pole, facing us
D14 = st.dur('S14'); GLOBE = [2.0, 0.72, -3.15]
st.shot('S14', 'office', setOpts={'door': False}, actors=[],
        props=[P('globe', 'globe', pos=GLOBE, opts={'r': 0.3, 'houseScale': 2.6, 'spin': [[0.05, round(D14 - 0.35, 3), 2.0]]})],
        cams=[cam(0.0, [GLOBE[0] + 0.15, 1.75, -1.75], [GLOBE[0] + 0.13, 1.73, -1.85], [GLOBE[0], 1.42, GLOBE[2]], [GLOBE[0], 1.44, GLOBE[2]], lens=40)])   # (pass 2) higher: the pole and his block on it in the frame
st.cue('sfx:zip', 'S14', 0.05, 0.25)

# 11 (line): he lives at the North Pole. His living room: snow falling indoors, drifts along the wall, frost on his face and his breath smoking; a polar
#     bear sits beside him on the sofa; he sips a hot drink, deadpan
D15 = st.dur('S15'); SOFA = [0.0, 0, -2.75]
st.shot('S15', 'livingRoom', setOpts={'tv': False}, actors=[
        act('mec', [0.5, 0, -2.75], 0, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, fx={'breath': True}), k(0.0, toon={'face': {'lid': 0.45}}, toonDur=0.0), k(0.7, toon={'face': {'lid': 0.5, 'gx': -0.5}}, toonDur=0.1)]),
        act('ours', [-0.62, 0, -2.85], 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.62, look=[0.5, 1.6, -2.75])])],
        props=[*FORKS_ON(), P('snow', 'snowfall', pos=[0.0, 0, -1.6], opts={'w': 5.5, 'h': 4.0, 'd': 4.5, 'n': 600, 'size': 0.06}), P('bank', 'snowBank', pos=[0.0, 0, -3.42], opts={'len': 6.0})],
        cams=[FC(0.0, [0.3, 1.25, 1.9], [[-1.3, 2.2, -2.85], [1.1, 2.1, -2.75], [0.0, 0.0, -2.4]], top=0.12, bottom=0.74, drift=(0.0, 0.0, -0.18))])

# 12 (line): third floor, no lift. (pass 2) From the top of the stairwell: two explorers in red parkas climb the last flight bent double, heaving; one
#     swings his pennant down into the doormat (PÔLE NORD); the door opens; he looks down at them; then close on him in the doorway, a look at us
D16 = st.dur('S16'); LAND = 1.6; DOOR = [0.0, LAND, -2.9]; OPEN16 = 1.3; FLAG16 = 1.0
SLAB = '#D9D0C1'
EXP = [('explo1', [1.5, LAND, -0.45], -150), ('explo2', [2.25, LAND, 0.05], -145)]   # (pass 2) to the right: from the stairwell his bent head hid the planted pennant
HEAVE = lambda t0, s_=1.0: [k(round(t0 + 0.22 * i, 3), toon={'bend': {'spine': [0.85, 0, 0, 1, None], 'neck': [-0.25, 0, 0, 1, None]}, 'sq': [1.0 + (0.04 if i % 2 == 0 else -0.01) * s_, 1.0 - (0.04 if i % 2 == 0 else -0.01) * s_, 1.0], 'face': {'jaw': 0.6, 'sweat': 1, 'lid': 0.55}}, toonDur=0.2, toonEase='inOut') for i in range(8)]   # doubled over, heaving
st.shot('S16', 'whiteVoid', actors=[
        act('explo1', [1.05, 1.2, 0.9], 180, 'stand', 'tired', keys=[k(0.0, look=[DOOR[0], LAND + 0.3, DOOR[2] + 0.6]), k(0.0, to=EXP[0][1], dur=0.6, clip='walk', then='stand', ease='out', face=-150),
            *HEAVE(0.0)[:3],
            k(round(FLAG16 - 0.22, 3), toon={'bend': {'spine': [0.3, 0, 0, 1, None]}, 'reach': {'R': [0.6, LAND + 2.05, -1.25, 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'jaw': 0.4, 'sweat': 1, 'brow': 0.6}}, toonDur=0.1),   # the pennant pulled off his pack and up...
            k(FLAG16, toon={'bend': {'spine': [0.75, 0, 0, 1, None]}, 'reach': {'R': [0.42, LAND + 1.3, -1.95, 1, 0.05]}, 'hands': {'R': 'grip'}, 'face': {'jaw': 0.3, 'sweat': 1}}, toonDur=0.08, toonEase='in'),   # ...and driven down into the mat, his fist on the pole
            k(round(FLAG16 + 0.2, 3), toon={'bend': {'spine': [0.85, 0, 0, 1, None]}, 'face': {'jaw': 0.6, 'sweat': 1, 'lid': 0.55}}, toonDur=0.15)]),
        act('explo2', [1.4, 0.6, 1.62], 180, 'stand', 'tired', keys=[k(0.0, look=[DOOR[0], LAND + 0.3, DOOR[2] + 0.6]), k(0.1, to=EXP[1][1], dur=0.8, clip='walk', then='stand', ease='out', face=-145), *HEAVE(0.05, 1.2)]),
        act('mec', [DOOR[0], LAND, round(DOOR[2] - 0.75, 3)], 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(OPEN16, to=[DOOR[0], LAND, round(DOOR[2] + 0.35, 3)], dur=0.3, clip='walk', then='stand', ease='out', face=0),   # (pass 2) well behind the door until it opens
            k(round(OPEN16 + 0.3, 3), look=[1.5, LAND + 0.6, -0.45]), k(round(OPEN16 + 0.85, 3), look='camera'), k(round(OPEN16 + 0.85, 3), toon={'face': {'lid': 0.4, 'browL': 0.5}}, toonDur=0.12),
            k(round(OPEN16 + 1.25, 3), toon={'face': {'lid': 1, 'browL': 0.5}}, toonDur=0.08), k(round(OPEN16 + 1.36, 3), toon={'face': {'lid': 0.45, 'browL': 0.5}}, toonDur=0.1)])],   # a slow blink
        props=[P('wall16', 'plainWall', pos=[0.0, LAND, round(DOOR[2] - 0.05, 3)], opts={'w': 8.0, 'h': 3.2, 'color': '#EDE6D6'}),
               P('land16', 'plainWall', pos=[0.0, LAND, -1.35], rot=[-math.pi / 2, 0, 0], opts={'w': 8.0, 'h': 3.1, 'color': SLAB}),   # the landing, 1.6 m up
               P('front16', 'plainWall', pos=[0.0, 0.0, 0.2], opts={'w': 8.0, 'h': LAND, 'color': '#E4DBCB'}),
               P('stairs16', 'stairs', pos=[1.25, 0, 2.44], opts={'steps': 8, 'w': 1.3}),   # the last flight, coming up to the landing
               P('door16', 'door', pos=[DOOR[0], LAND, round(DOOR[2] + 0.02, 3)], opts={'w': 0.95, 'h': 2.15, 'openAt': OPEN16}),
               P('mat16', 'doormat', pos=[DOOR[0], round(LAND + 0.012, 3), -2.25], opts={'text': 'PÔLE NORD', 'w': 1.15, 'd': 0.68}),
               P('plaque16', 'bronzePlaque', pos=[1.05, round(LAND + 1.55, 3), round(DOOR[2] + 0.02, 3)], opts={'text': '3e ÉTAGE', 'w': 0.85, 'h': 0.34}),
               *[P(f'bp16{i}', 'backpack', on={'actor': n, 'joint': 'torso', 'offset': [0, 0.42, -0.24]}, opts={'color': '#2F7F5C' if i == 0 else '#B5532A'}) for i, (n, p_, ry) in enumerate(EXP)],
               P('flag16p', 'flag', on={'actor': 'explo1', 'joint': 'torso', 'offset': [0.12, 0.45, -0.32]}, scale=0.7, opts={'colors': ['#F2C230', '#F2C230', '#F2C230'], 'vertical': False, 'poleR': 0.03, 'poleColor': '#3A3D44'}, keys=[k(round(FLAG16 - 0.2, 3), visible=False)]),   # (pass 2) a pennant up off his backpack (held in the hand all the way it hung upside down)
               P('flag16', 'flag', on={'actor': 'explo1', 'hand': 'R', 'offset': [0, 0.0, 0.05], 'rot': [math.pi, 0, 0]}, opts={'colors': ['#F2C230', '#F2C230', '#F2C230'], 'vertical': False, 'poleR': 0.03, 'poleColor': '#3A3D44'}, keys=[k(0.0, visible=False), k(round(FLAG16 - 0.2, 3), visible=True), k(round(FLAG16 - 0.1, 3), visible=False)]),   # in his raised fist for a moment (the pole past the fingers points up only while the arm does)   # (pass 2) a thick dark pole: from high up a thin grey one vanished and the cloth floated like a card
               P('flag16b', 'flag', pos=[0.42, round(LAND + 0.75, 3), -1.95], ry=-30, opts={'colors': ['#F2C230', '#F2C230', '#F2C230'], 'vertical': False, 'poleR': 0.03, 'poleColor': '#3A3D44'}, keys=[k(0.0, visible=False), k(round(FLAG16 - 0.1, 3), visible=True),
                 k(round(FLAG16 - 0.1, 3), to=[0.42, LAND, -1.95], dur=0.1, ease='in'), k(FLAG16, squash=[1.0, 0.88, 1.0], dur=0.0), k(round(FLAG16 + 0.06, 3), squash=[1, 1, 1], dur=0.1)]),   # (pass 2) driven down into the mat
               *[P(f'cl{i}', kind, on={'actor': 'mec', 'joint': 'torso', 'offset': [round(-lat, 3), round(y - 1.0, 3), 0.2], 'rot': [0, 0, fan]}, scale=CS) for i, (pid, kind, frm, lat, y, fan) in enumerate(CUT2)]],
        cams=[FC(0.0, [1.2, 7.5, 5.5], [[DOOR[0] - 0.6, LAND + 2.45, DOOR[2]], [DOOR[0] + 0.6, LAND + 2.45, DOOR[2]], [-0.35, LAND, -2.0], [1.4, 0.6, 1.62], [1.4, 2.6, 1.62], [2.4, LAND + 1.8, 0.05]], top=0.1, bottom=0.74, drift=(0.0, -0.08, -0.1)),   # (pass 2) they start higher up the flight: a tighter wide   # (pass 2) down the stairwell from high behind the last flight: its depth runs up the tall frame (from the side it ran across it and they were specks), and the leaf, seen edge on, leaves the doorway clear
              FC(round(OPEN16 + 0.6, 3), [-0.5, round(LAND + 1.8, 3), -0.6], [[DOOR[0], round(LAND + 2.4, 3), round(DOOR[2] + 0.35, 3)], [DOOR[0], round(LAND + 1.15, 3), round(DOOR[2] + 0.35, 3)], [DOOR[0] - 0.4, round(LAND + 1.7, 3), round(DOOR[2] + 0.35, 3)], [DOOR[0] + 0.4, round(LAND + 1.7, 3), round(DOOR[2] + 0.35, 3)]], top=0.16, bottom=0.68)])   # then close on him in the doorway
st.cue('sfx:gasp', 'S16', 0.1, 0.3); st.cue('sfx:gasp', 'S16', 0.55, 0.25); st.cue('thud', 'S16', FLAG16, 0.3); st.cue('sfx:carDoor', 'S16', OPEN16, 0.25)

st.write("L'aimant", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, follow=1, pupil=0.5, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'rando': {'preset': 'tourist', 'seed': 471, 'hat': 'beanie', 'build': {'width': 0.92, 'headWidth': 1.25}},
    'rando2': {'preset': 'sportif', 'seed': 472, 'hat': 'beanie', 'build': {'width': 0.9, 'headWidth': 1.25}},
    'touriste': {'preset': 'tourist', 'seed': 473, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'mamie': {'preset': 'mamie', 'seed': 474, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'skipper': {'preset': 'fermier', 'seed': 475, 'hat': 'beanie', 'build': {'width': 0.95, 'headWidth': 1.25}},
    'carto1': {'preset': 'savant', 'seed': 476, 'build': {'width': 0.9, 'headWidth': 1.25}},
    'carto2': {'preset': 'savant', 'seed': 477, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'explo1': {'preset': 'sportif', 'seed': 478, 'hat': 'beanie', 'hatColor': '#F4F2EA', 'suit': '#C8322A', 'pants': '#3A3D44', 'build': {'width': 1.05, 'headWidth': 1.25}},   # (pass 2) a red parka, dark trousers, a white hood
    'explo2': {'preset': 'sportif', 'seed': 479, 'hat': 'beanie', 'hatColor': '#F4F2EA', 'suit': '#D9822B', 'pants': '#3A3D44', 'build': {'width': 1.05, 'headWidth': 1.25}},
    'ours': {'type': 'creature', 'name': 'bear', 'opts': {'seed': 7, 'colors': {'body': '#F2F0E8', 'belly': '#E6E2D6', 'snout': '#D8D2C2', 'paw': '#CFC8B8'}}},
})
