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
CS = 2.3                                                            # (first look) cutlery at cartoon size (life size it did not show)
CUTOPT = lambda kind: {'handle': '#2E3640'} if kind == 'fork' else {'color': '#AEB4BC', 'handle': '#2E3640'}   # (pass 2) dark handles: pale silver on the peach wall vanished in flight
HEADY = 2.05
def FLY(pid, name, frm, to, t, dur=0.16, fan=0.0, opts=None, scale=CS, lift=0.3, rattle=None):   # a piece of metal leaves its place and flies to him, flat against his chest
    mid = r3([(frm[0] + to[0]) / 2, max(frm[1], to[1]) + lift, (frm[2] + to[2]) / 2])   # (pass 2) on an arc, stretched along its flight, squashed on the hit
    R0 = [0, round(math.radians(MRY), 4), fan]; yaw = round(math.atan2(to[0] - frm[0], to[2] - frm[2]), 4); keys = []
    if rattle is not None:                                           # (pass 3) it rattles on the counter first: little hops, rocking from side to side
        for j in range(int((t - 0.03 - rattle) / 0.05)):
            tj = round(rattle + 0.05 * j, 3); sg = 1 if j % 2 else -1
            keys += [k(tj, rotTo=[round(0.08 * sg, 3), R0[1], round(fan + 0.18 * sg, 3)], dur=0.04), k(tj, to=[frm[0], round(frm[1] + (0.035 if j % 2 else 0.0), 3), frm[2]], dur=0.04)]
    else: keys.append(k(round(t - 0.2, 3), to=[frm[0], frm[1] + 0.02, frm[2]], dur=0.2))
    keys += [k(round(t - 0.03, 3), rotTo=[round(PI / 2, 4), yaw, 0], dur=0.03), k(t, squash=[0.55, 2.4, 0.55], dur=0.0),   # (pass 3) turned along its flight and stretched 2.4 times (a smear)
             k(t, to=mid, dur=round(dur * 0.5, 3), ease='out'), k(round(t + dur * 0.5, 3), to=to, dur=round(dur * 0.5, 3), ease='in'),
             k(round(t + dur, 3), rotTo=R0, dur=0.0), k(round(t + dur, 3), squash=[1.45, 0.6, 1.0], dur=0.0), k(round(t + dur + 0.05, 3), squash=[1.0, 1.0, 1.0], dur=0.06)]   # flat on the hit
    return P(pid, name, pos=frm, rot=R0, rotOrder='YXZ', scale=scale, opts=opts or CUTOPT(name), keys=keys)
def JOLTS(times, s=1.0):   # (pass 3) the whole body takes a series of hits (a head snap on a locked mannequin, the reviewers said)
    t0 = times[0]; out = [k(round(t0 - 0.05, 3), toon={'sq': [round(1 - 0.04 * s, 3), round(1 + 0.05 * s, 3), round(1 - 0.04 * s, 3)], 'bend': {'spine': [round(0.16 * s, 3), 0, 0, 1, None], 'neck': [round(0.1 * s, 3), 0, 0, 1, None]}, 'face': {'eye': 0.2, 'brow': 0.5}}, toonDur=0.04, toonEase='in')]   # pulled toward the metal a frame before
    for i, t in enumerate(times):
        a = 1.0 if i % 2 == 0 else 0.75
        out.append(k(round(t, 3), toon={'sq': [round(1 + 0.09 * s * a, 3), round(1 - 0.1 * s * a, 3), round(1 + 0.09 * s * a, 3)], 'bend': {'spine': [round(-0.2 * s * a, 3), round(0.05 * (1 if i % 2 else -1), 3), 0, 1, None], 'neck': [round(-0.24 * s * a, 3), 0, 0, 1, None],
                                         'armL': [round(0.42 * s * a, 3), round(0.3 * s * a, 3), 0, 1, None], 'armR': [round(0.42 * s * a, 3), round(-0.3 * s * a, 3), 0, 1, None]}, 'face': {'eye': round(0.35 * s, 3), 'brow': 0.6}}, toonDur=0.025, toonEase='out'))   # caved in, arms flung back, knees dipped
    tl = times[-1]
    return out + [k(round(tl + 0.09, 3), toon={'sq': [0.98, 1.03, 0.98], 'bend': {'spine': [round(0.06 * s, 3), 0, 0, 1, None], 'neck': [0.04, 0, 0, 1, None]}, 'face': {'brow': 0.3}}, toonDur=0.08),
                  k(round(tl + 0.22, 3), toon={'face': {'brow': 0.2}}, toonDur=0.12)]   # the recoil, then still
KEYS_ON = [-0.13, 0.27, 0.21]; PAN_CHEST = [0.05, 0.38, 0.25]   # (pass 3) the key ring on his cheek (it hung by his ear: outside the face it read as still on its hook); the pan higher on his chest (out of the caption band)
JOLT = lambda t, s=1.0: [k(round(t, 3), toon={'sq': [1 + 0.07 * s, 1 - 0.08 * s, 1 + 0.07 * s], 'bend': {'neck': [round(-0.22 * s, 3), 0, 0, 1, None]}, 'face': {'eye': 0.35 * s, 'brow': 0.6}}, toonDur=0.025),   # (pass 2) the head snaps back at each hit
                         k(round(t + 0.07, 3), toon={'bend': {'neck': [0, 0, 0, 1, None]}, 'face': {'brow': 0.3}}, toonDur=0.08)]

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
            k(round(IN1 + 0.34, 3), toon={'face': {'gulp': 1.0, 'eye': 0.3}, 'sq': [1.1, 0.86, 1.1], 'bend': {'neck': [0, 0, 0, 0.6, None], 'spine': [0.18, 0, 0, 1, None], 'armL': [0, -0.12, 0, 1, None], 'armR': [0, 0.12, 0, 1, None]}}, toonDur=0.06, toonEase='in'),   # (pass 3) the head sinks into the collar, the whole body crouches...
            k(round(IN1 + 0.42, 3), toon={'face': {'cross': 1.0, 'brow': 0.8, 'pop': 0.35, 'tremble': 1}, 'sq': [0.9, 1.16, 0.9], 'bend': {'spine': [-0.12, 0, 0, 1, None], 'armL': [0.2, 0.6, 0, 1, None], 'armR': [0.2, -0.6, 0, 1, None], 'foreL': [0, 0.4, 0, 1, None], 'foreR': [0, -0.4, 0, 1, None]}, 'hands': {'L': 'spread', 'R': 'spread'}}, toonDur=0.04, toonEase='outBack'),   # ...then the take: up off the floor, arms flung out, the crossed eyes shivering
            k(round(IN1 + 0.42, 3), to=[ME[0], 0.16, ME[2]], dur=0.07, glide=True, ease='out', face='keep'), k(round(IN1 + 0.56, 3), to=ME, dur=0.08, glide=True, ease='in', face='keep'),   # (pass 3) a hop: four frames of hang time
            k(round(IN1 + 0.64, 3), toon={'face': {'cross': 1.0, 'brow': 0.8, 'pop': 0.3, 'tremble': 1}, 'sq': [1.06, 0.93, 1.06], 'bend': {'armL': [0.1, 0.3, 0, 1, None], 'armR': [0.1, -0.3, 0, 1, None]}}, toonDur=0.04),   # landing
            k(round(IN1 + 0.74, 3), toon={'face': {'cross': 1.0, 'brow': 0.8, 'pop': 0.3, 'tremble': 1}, 'sq': [0.98, 1.03, 0.98]}, toonDur=0.08), k(round(IN1 + 1.0, 3), toon={'face': {'cross': 0.6, 'brow': 0.5, 'lid': 0.3}}, toonDur=0.2)])],
        props=[P('mag1', 'magnet', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.03, 0.04], 'face': 'camera'}, opts={'s': 0.3, 'glow': [0.0, IN1]}, keys=[k(round(IN1 - 0.02, 3), scale=0.01, dur=0.04)])],
        cams=[FC(0.0, [0.55, 1.9, -0.6], [[ME[0], 2.4, ME[2]], [ME[0], 2.9, ME[2]], [ME[0], 1.2, ME[2]], MAG1, *BODY()], top=0.08, bottom=0.7, drift=(-0.05, 0, -0.08))])   # (pass 3) room above him for the hop of the take
st.cue('sfx:gulp', 'S01', IN1 + 0.1, 0.45); st.cue('clang', 'S01', IN1 + 0.42, 0.15)

# 2: since then all metal jumps on him. Wider: the cutlery on the counter shivers, then flies across and sticks flat on his chest, clink, clink, clink
D2 = st.dur('S02'); JMP2 = round(st.at('S02', 'L02', 5) - 0.04, 3)
CUT2 = [('f1', 'fork', [0.05, 1.18, -3.0], -0.12, 1.3, -0.35), ('s1', 'spoon', [0.3, 1.18, -3.05], 0.1, 1.42, 0.25), ('f2', 'fork', [0.55, 1.18, -3.0], -0.02, 1.18, 0.05),
        ('s2', 'spoon', [0.8, 1.18, -3.05], 0.16, 1.24, -0.2), ('f3', 'fork', [-0.2, 1.18, -3.02], -0.18, 1.48, 0.4)]   # (pass 3) standing on the counter just behind him, in the frame (further along only a tine showed at the edge)   # (id, kind, on the counter, across his chest, height, fan)   # (pass 2) 0.12 lower: the top ones covered his face
st.shot('S02', 'kitchenDay', setOpts=KIT, actors=[
        act('mec', ME, MRY, 'stand', 'unimpressed', keys=[k(0.0, look=[0.3, 1.2, -3.0]), k(0.45, look='camera'), k(0.45, toon={'face': {'brow': 0.5, 'browL': 0.9}}, toonDur=0.1),   # (pass 2) the cutlery shivers: hm? at us
            k(round(JMP2 - 0.4, 3), look=[0.3, 1.2, -3.0]), k(round(JMP2 - 0.3, 3), toon={'face': {'brow': 0.7, 'eye': 0.3}}, toonDur=0.08),
            *JOLTS([JMP2 + 0.16 + 0.06 * i for i in range(len(CUT2))], 1.0), k(round(JMP2 + 0.5, 3), look=[round(ME[0] + 0.3 * FWD[0], 3), 1.15, round(ME[2] + 0.3 * FWD[1], 3)]),   # down at his chest
            k(round(JMP2 + 0.78, 3), look='camera'), k(round(JMP2 + 0.78, 3), expr='unimpressed')])],
        props=[FLY(f'c{i}', kind, frm, ON_BODY(lat, y), round(JMP2 + 0.06 * i, 3), fan=fan, rattle=0.4) for i, (pid, kind, frm, lat, y, fan) in enumerate(CUT2)],
        cams=[FC(0.0, [1.9, 1.6, 0.2], [[ME[0], 2.45, ME[2]], [ME[0], 0.95, ME[2]], [-0.3, 1.1, -3.05], [0.95, 1.1, -3.05], [0.4, 1.75, -3.05], *BODY()], top=0.12, bottom=0.74, drift=(-0.05, 0, -0.06))])   # (pass 2) a medium shot: him and the near end of the counter (the whole counter made him small at the left of a kitchen floor)
st.cue('sfx:ticks', 'S02', JMP2 - 0.25, 0.25); [st.cue('clang', 'S02', round(JMP2 + 0.16 + 0.06 * i, 3), 0.2) for i in range(len(CUT2))]

# 3: the forks. Close on him: a volley of forks zips in from the drawer at the right and thunks into a fan on his chest, one jolt each
D3 = st.dur('S03'); V3 = [round(0.12 + 0.11 * i, 3) for i in range(6)]
FAN3 = [(-0.15, 1.34, -0.5), (0.0, 1.44, -0.15), (0.15, 1.36, 0.3), (-0.08, 1.18, -0.3), (0.1, 1.16, 0.45), (0.02, 1.52, 0.1)]   # (pass 2) 0.14 lower, under his chin
DRAWER = [1.3, 0.85, -2.95]
st.shot('S03', 'kitchenDay', setOpts=KIT, actors=[
        act('mec', ME, MRY, 'stand', 'unimpressed', keys=[k(0.0, look=DRAWER), *JOLTS([t + 0.1 for t in V3], 1.0), k(0.85, look='camera'), k(0.85, toon={'face': {'lid': 0.35, 'brow': 0.2}}, toonDur=0.1)])],
        props=[*[P(f'v{i}', 'fork', pos=DRAWER, rot=[0, math.radians(MRY), fan], rotOrder='YXZ', scale=CS, opts=CUTOPT('fork'), keys=[k(0.0, visible=False), k(round(t - 0.01, 3), visible=True), k(round(t - 0.01, 3), squash=[0.55, 2.4, 0.55], dur=0.0),
                 k(round(t - 0.01, 3), rotTo=[round(PI / 2, 4), round(math.atan2(ON_BODY(lat, y, 0.22)[0] - DRAWER[0], ON_BODY(lat, y, 0.22)[2] - DRAWER[2]), 4), 0], dur=0.0), k(round(t + 0.1, 3), rotTo=[0, round(math.radians(MRY), 4), fan], dur=0.0),   # (pass 3) along its flight, stretched
                 k(t, to=r3([(DRAWER[0] + ON_BODY(lat, y, 0.22)[0]) / 2, 1.95, (DRAWER[2] + ON_BODY(lat, y, 0.22)[2]) / 2]), dur=0.05, ease='out'), k(round(t + 0.05, 3), to=ON_BODY(lat, y, 0.22), dur=0.05, ease='in'),   # (pass 2) on an arc
                 k(round(t + 0.1, 3), squash=[1.45, 0.6, 1.0], dur=0.0), k(round(t + 0.15, 3), squash=[1, 1, 1], dur=0.05)]) for i, ((lat, y, fan), t) in enumerate(zip(FAN3, V3))],
               *[P(f'old{i}', kind, pos=ON_BODY(lat, y), rot=[0, math.radians(MRY), fan], scale=CS, opts=CUTOPT(kind)) for i, (pid, kind, frm, lat, y, fan) in enumerate(CUT2)]],
        cams=[FC(0.0, [round(ME[0] + 1.55 * FWD[0], 3), 1.2, round(ME[2] + 1.55 * FWD[1], 3)], [[ME[0], 2.4, ME[2]], [ME[0], 1.15, ME[2]], *BODY()], top=0.12, bottom=0.74, drift=(0.03, 0.04, 0.02))])   # (pass 2) low and frontal, chest and face (it repeated S02's angle)
[st.cue('thud', 'S03', round(t + 0.1, 3), 0.2) for t in V3]

# 4: the keys. The key ring flies off its hook by the door and smacks his cheek; it stays there, swinging
D4 = st.dur('S04'); K4 = 0.22
HOOK4 = [-2.4, 1.55, -1.6]
CHEEK4 = [round(ME[0] + 0.24 * FWD[0] + 0.2 * RGT[0], 3), 2.02, round(ME[2] + 0.24 * FWD[1] + 0.2 * RGT[1], 3)]
FORKS_ON = lambda: [*[P(f'cf{i}', kind, on={'actor': 'mec', 'joint': 'torso', 'offset': [round(-lat, 3), round(y - 1.0, 3), 0.2], 'rot': [0, 0, fan]}, scale=CS, opts=CUTOPT(kind)) for i, (pid, kind, frm, lat, y, fan) in enumerate(CUT2)],
                    *[P(f'cv{i}', 'fork', on={'actor': 'mec', 'joint': 'torso', 'offset': [round(-lat, 3), round(y - 1.0, 3), 0.21], 'rot': [0, 0, fan]}, scale=CS, opts=CUTOPT('fork')) for i, (lat, y, fan) in enumerate(FAN3)]]   # everything stuck on his chest from now on
st.shot('S04', 'kitchenDay', setOpts=KIT, actors=[
        act('mec', ME, MRY, 'stand', 'unimpressed', keys=[k(0.0, look=HOOK4), k(round(K4 - 0.05, 3), toon={'bend': {'spine': [0, 0.1, 0, 1, None], 'neck': [0, 0.12, 0, 1, None]}, 'sq': [0.97, 1.04, 0.97], 'face': {'eye': 0.3, 'brow': 0.6}}, toonDur=0.04, toonEase='in'),   # (pass 3) pulled toward the keys a frame before
            k(K4, toon={'bend': {'spine': [-0.08, -0.2, 0, 1, None], 'neck': [0, -0.42, 0, 1, None], 'armR': [0.25, -0.45, 0, 1, None], 'armL': [0.1, 0.25, 0, 1, None]}, 'face': {'lidR': 0.8, 'brow': 0.7, 'eye': 0.3}, 'sq': [1.07, 0.92, 1.07]}, toonDur=0.03, toonEase='out'),   # smack: knocked aside from the waist up, an eye shut, knees dipped
            k(round(K4 + 0.12, 3), toon={'bend': {'spine': [0, 0.06, 0, 1, None], 'neck': [0, 0.06, 0, 1, None]}, 'face': {'lidR': 0.5, 'brow': 0.5}, 'sq': [0.98, 1.03, 0.98]}, toonDur=0.1),   # the recoil past upright
            k(round(K4 + 0.26, 3), toon={'bend': {'neck': [0, -0.06, 0, 1, None]}, 'face': {'lidR': 0.3, 'brow': 0.4}}, toonDur=0.15), k(round(K4 + 0.2, 3), look='camera')])],
        props=[*FORKS_ON(), P('keys4', 'keyRing', pos=HOOK4, scale=2.4, keys=[k(round(K4 - 0.12, 3), squash=[2.3, 0.62, 0.62], dur=0.0), k(round(K4 - 0.12, 3), to=CHEEK4, dur=0.12, ease='in'), k(K4, visible=False)]),   # (pass 3) stretched along its flight
               P('keys4b', 'keyRing', on={'actor': 'mec', 'joint': 'head', 'offset': KEYS_ON, 'face': 'camera'}, scale=2.4, keys=[k(0.0, visible=False), k(K4, visible=True), k(K4, squash=[1.35, 0.7, 1.0], dur=0.0), k(round(K4 + 0.06, 3), squash=[1, 1, 1], dur=0.06)])],   # flat on his cheek
        cams=[FC(0.0, [0.1, 1.95, -0.55], [[ME[0], 2.4, ME[2]], [ME[0], 1.35, ME[2]], CHEEK4, ON_BODY(-0.85, 2.2, 0.0), *BODY()], top=0.16, bottom=0.7)])   # (pass 3) room on his left: knocked aside, the head left the frame
st.cue('clang', 'S04', K4, 0.3)

# 5: the frying pan. It leaves the stove and flattens his face: BONG. (pass 3) He has turned back to us: the pan lands square on the whole face, his head a
#    pancake round it (rocked back, arms flung out); four frames, then it peels off top edge first, hangs three frames and drops onto his chest, leaving
#    its print; the head pops back past round, eyes out on stalks, stars round it
D5 = st.dur('S05'); P5 = 0.24; PEEL5 = round(P5 + 0.13, 3); DROP5 = round(P5 + 0.3, 3); YP = round(math.radians(MRY), 4)
STOVE5 = [1.35, 1.02, -3.2]
FACE5 = [round(ME[0] + 0.36 * FWD[0], 3), HEADY, round(ME[2] + 0.36 * FWD[1], 3)]
FLAT5 = {'scl': {'head': [1.5, 1.22, 0.42]}, 'sq': [1.08, 0.9, 1.08], 'lay': [-0.1, 0], 'bend': {'spine': [-0.18, 0, 0, 1, None], 'armL': [0.3, 0.55, 0, 1, None], 'armR': [0.3, -0.55, 0, 1, None]}, 'hands': {'L': 'spread', 'R': 'spread'}}
st.shot('S05', 'kitchenDay', setOpts=KIT, actors=[
        act('mec', ME, MRY, 'stand', 'unimpressed', keys=[k(0.0, look=STOVE5), k(0.04, toon={'face': {'eye': 0.5, 'brow': 1}}, toonDur=0.05), k(round(P5 - 0.16, 3), look='camera'),   # he sees it coming, turns back to us
            k(round(P5 - 0.05, 3), toon={'face': {'eye': 0.3, 'brow': 0.8}, 'sq': [0.97, 1.04, 0.97], 'bend': {'spine': [0.12, 0, 0, 1, None]}}, toonDur=0.04, toonEase='in'),   # pulled toward it
            k(P5, toon={**FLAT5, 'face': {'brow': 0.8}}, toonDur=0.02, toonEase='out'),   # BONG
            k(PEEL5, toon={**FLAT5, 'face': {'brow': 0.8, 'lid': 0.6}}, toonDur=0.04),   # still flat while the pan peels and hangs
            k(round(DROP5 + 0.03, 3), toon={'scl': {'head': [0.84, 1.26, 1.18]}, 'sq': [0.95, 1.07, 0.95], 'face': {'pop': 1, 'stars': 1}, 'lay': [0.03, 0]}, toonDur=0.05, toonEase='outBack'),   # back past round, eyes out on stalks
            k(round(DROP5 + 0.15, 3), toon={'scl': {'head': [1.06, 0.96, 1.0]}, 'face': {'pop': 0.6, 'stars': 1}}, toonDur=0.07),
            k(round(DROP5 + 0.26, 3), toon={'face': {'stars': 1, 'lid': 0.35}}, toonDur=0.1)])],
        props=[*FORKS_ON(), P('keys5', 'keyRing', on={'actor': 'mec', 'joint': 'head', 'offset': KEYS_ON, 'face': 'camera'}, scale=2.4),
               P('pan5', 'pan', pos=STOVE5, rot=[PI / 2, YP, 0], rotOrder='YXZ', opts={'r': 0.22}, keys=[k(round(P5 - 0.14, 3), to=FACE5, dur=0.14, ease='in'), k(P5, visible=False)]),
               P('pan5b', 'pan', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.26, 0.27], 'rot': [PI / 2, 0, 0]}, opts={'r': 0.27}, keys=[k(0.0, visible=False), k(P5, visible=True), k(PEEL5, visible=False)]),   # square over the whole face
               P('pan5d', 'pan', pos=[FACE5[0], round(HEADY + 0.02, 3), FACE5[2]], rot=[PI / 2, YP, 0], rotOrder='YXZ', opts={'r': 0.27}, keys=[k(0.0, visible=False), k(PEEL5, visible=True),
                 k(PEEL5, rotTo=[round(PI / 2 + 1.05, 4), YP, 0], dur=0.07, ease='out'), k(PEEL5, to=[round(FACE5[0] + 0.2 * FWD[0], 3), round(HEADY - 0.24, 3), round(FACE5[2] + 0.2 * FWD[1], 3)], dur=0.07, ease='out'),   # it peels off, top edge first, and hangs under his chin (his printed face above it)...
                 k(DROP5, to=[round(ME[0] + 0.32 * FWD[0], 3), 1.42, round(ME[2] + 0.32 * FWD[1], 3)], dur=0.08, ease='in'), k(round(DROP5 + 0.08, 3), visible=False)]),   # ...hangs three frames by its bottom edge, drops onto his chest
               P('print5', 'panPrint', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.26, 0.2], 'face': 'camera'}, opts={'r': 0.17, 'w': 0.03, 'fade': [round(DROP5 + 0.05, 3), round(DROP5 + 0.3, 3)]}, keys=[k(0.0, visible=False), k(PEEL5, visible=True)]),   # the pan's print on his face
               P('pan5c', 'pan', on={'actor': 'mec', 'joint': 'torso', 'offset': PAN_CHEST, 'rot': [-PI / 2, 0, -0.5]}, opts={'r': 0.17}, keys=[k(0.0, visible=False), k(round(DROP5 + 0.08, 3), visible=True)])],
        fx=[{'type': 'shake', 'at': P5, 'dur': 0.12, 'amount': 0.014}],
        cams=[FC(0.0, [round(ME[0] + 2.0 * FWD[0], 3), 1.95, round(ME[2] + 2.0 * FWD[1], 3)], [[ME[0], 2.55, ME[2]], [ME[0], 1.35, ME[2]], *BODY()], top=0.16, bottom=0.72)])   # (pass 2) face-on: the pan lands flat on his face
st.cue('clang', 'S05', P5, 0.55); st.cue('sfx:boing', 'S05', DROP5 + 0.03, 0.3); st.cue('clack', 'S05', DROP5 + 0.08, 0.25)

# ---- the street (parisStreet): he walks along the right-hand pavement toward +Z, covered in cutlery, the pan stuck on his chest now
PX = 6.6; STREET = {'clear': [-80, 80], 'eiffel': False, 'paveW': 6.5}
STUCK = lambda: [*FORKS_ON(), P('keysS', 'keyRing', on={'actor': 'mec', 'joint': 'head', 'offset': KEYS_ON, 'face': 'camera'}, scale=2.4),
                 P('panS', 'pan', on={'actor': 'mec', 'joint': 'torso', 'offset': PAN_CHEST, 'rot': [-PI / 2, 0, -0.5]}, opts={'r': 0.17})]

# 4 (line): even the street lamps bow as he passes. (pass 3) Low in front of him, down the pavement: one after the other the lamp posts bend over like
#    stems (a curve along their length, not a hinge), their heads dipping to his face, then spring back up past upright as he walks under them
D6 = st.dur('S06'); Z6 = (-3.6, 3.4); LAMPZ = (-1.6, 0.8, 2.9); LAMPX = 4.3; BOW6 = -1.4   # bent -1.4 rad the head comes down to 2.2 m, 2.3 m out: at his face
TL6 = lambda zl: (zl - Z6[0]) / (Z6[1] - Z6[0]) * D6                  # when he is level with it
def bow6(zl):
    tl = TL6(zl)
    return [[0.0, 0.0], [round(tl - 0.8, 3), 0.14], [round(tl - 0.62, 3), BOW6], [round(tl - 0.24, 3), 0.32], [round(tl - 0.04, 3), -0.12], [round(tl + 0.16, 3), 0.0]]   # a counter-lean, the bow, held, springs back past upright, settles
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [PX, 0, Z6[0]], 0, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, to=[PX, 0, Z6[1]], dur=D6, clip='walk', then='walk', ease='linear', face=0),
            k(round(TL6(LAMPZ[1]) - 0.5, 3), look=[round(LAMPX + 2.3, 3), 2.3, LAMPZ[1]]), k(round(TL6(LAMPZ[1]) - 0.5, 3), toon={'face': {'brow': 0.5, 'browL': 0.8}}, toonDur=0.1),   # a glance at the one bowing to him
            k(round(TL6(LAMPZ[1]) - 0.08, 3), look='camera'), k(round(TL6(LAMPZ[1]) - 0.08, 3), toon={'face': {'lid': 0.35}}, toonDur=0.12)])],
        props=[*STUCK(), *[P(f'lamp{i}', 'stemLamp', pos=[LAMPX, 0, z], opts={'bend': bow6(z), 'ease': 0.2}) for i, z in enumerate(LAMPZ)]],
        cams=[FC(0.0, [7.3, 0.9, 6.8], [[PX, 2.5, Z6[0]], [PX, 0.0, 1.2], [LAMPX, 4.5, LAMPZ[0]], [LAMPX, 4.5, LAMPZ[1]], [round(LAMPX - 0.3, 3), 0.0, LAMPZ[1]]], top=0.1, bottom=0.74, drift=(0.0, 0.0, -0.5))])   # (pass 3) low in front of him, off his right shoulder: the posts on the left bend across toward him
[st.cue('sfx:squeak', 'S06', round(TL6(z) - 0.62, 3), 0.2) for z in LAMPZ]; [st.cue('sfx:twang', 'S06', round(TL6(z) - 0.24, 3), 0.15) for z in LAMPZ]

# 5 (line): and the compasses no longer show the north. Over a hiker's shoulder, looking down at his compass: the needle leaves N, whirls, and points
#    at our man walking past behind
D7 = st.dur('S07'); H7 = [PX - 1.4, 0, 6.5]; ME7 = [PX + 0.4, 0, 9.4]
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[
        act('rando', H7, 20, 'stand', 'neutral', keys=[k(0.0, look=[H7[0] + 0.2, 0.9, H7[2] + 0.5]), k(0.0, toon={'reach': {'R': [round(H7[0] + 0.1, 3), 1.42, round(H7[2] + 0.55, 3), 1, 0.05]}, 'hands': {'R': 'flat'}}, toonDur=0.0),   # (pass 2) higher, further out
            k(0.85, toon={'reach': {'R': [round(H7[0] + 0.1, 3), 1.42, round(H7[2] + 0.55, 3), 1, 0.05]}, 'hands': {'R': 'flat'}, 'face': {'brow': 0.8, 'eye': 0.3}}, toonDur=0.1)]),
        act('mec', ME7, -90, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, to=[PX - 1.2, 0, 9.6], dur=D7, clip='walk', then='walk', ease='linear', face=-90)])],
        props=[*STUCK(), P('backpack7', 'backpack', on={'actor': 'rando', 'joint': 'torso', 'offset': [0, 0.42, -0.24]}),
               P('comp7', 'compass', on={'actor': 'rando', 'hand': 'R', 'offset': [0, 0.03, 0.12], 'rot': [0, PI, 0]}, scale=3.4, opts={'path': [[0.0, ME7[0], 1.4, ME7[2]], [D7, PX - 1.2, 1.4, 9.6]], 'spin': [0.35, 0.95], 'north': [0, 0, -1]})],
        cams=[FC(0.0, [round(H7[0] - 0.7, 3), 3.05, round(H7[2] - 0.45, 3)], [[round(H7[0] + 0.1, 3), 1.32, round(H7[2] + 0.55, 3)], [round(H7[0] + 0.1, 3), 1.55, round(H7[2] + 0.7, 3)], [PX - 0.4, 2.3, 9.5], [PX - 0.4, 0.4, 9.5]], top=0.08, bottom=0.64)])   # (pass 3) bottom 0.64: the dial at 55-65 % of the height, above the captions   # (first look) high over his right shoulder, looking down: the dial big in the middle, our man walking past beyond it   # (first look) over his right shoulder and above it (behind his head the frame was his skull and his backpack)
st.cue('sfx:zip', 'S07', 0.35, 0.25)

# 6 (line): they show him. Three passers-by on the pavement, each with a compass turned to us: every needle follows him as he walks in behind them;
#    (pass 3) he stops in the gap of the row at « lui », face clear, and looks at us; all three heads turn to him
D8 = st.dur('S08'); X8 = round(PX + 1.2, 3); LUI8 = round(st.at('S08', 'L06', 3) - 0.08, 3)
ZL8 = 12.6; Z8 = (round(ZL8 - 2.3, 3), ZL8)                           # (pass 3) where he stops: the gap between the mamie and the tourist
ROW8 = [('rando', [round(PX - 0.45, 3), 0, round(ZL8 - 1.25, 3)], -95), ('mamie', [round(PX - 0.45, 3), 0, round(ZL8 - 0.55, 3)], -90), ('touriste', [round(PX - 0.45, 3), 0, round(ZL8 + 0.65, 3)], -85)]   # a row facing the road and us
PATH8 = [[0.0, X8, 1.6, Z8[0]], [LUI8, X8, 1.6, ZL8], [D8, X8, 1.6, ZL8]]
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [X8, 0, Z8[0]], 0, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, to=[X8, 0, ZL8], dur=LUI8, clip='walk', then='stand', ease='out', face=0),   # he walks in behind them, taller than them...
            k(round(LUI8 + 0.1, 3), look='camera'), k(round(LUI8 + 0.1, 3), toon={'face': {'lid': 0.4, 'browL': 0.4}}, toonDur=0.12)]),   # ...stops in the gap and looks at us
        *[act(n, p, ry, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': [round(p[0] + 0.3 * math.sin(math.radians(ry)), 3), 1.4, round(p[2] + 0.3 * math.cos(math.radians(ry)), 3), 1, 0.05]}, 'hands': {'R': 'flat'}}, toonDur=0.0),
                                                 k(LUI8, look=[X8, 2.0, ZL8]), k(LUI8, toon={'reach': {'R': [round(p[0] + 0.3 * math.sin(math.radians(ry)), 3), 1.4, round(p[2] + 0.3 * math.cos(math.radians(ry)), 3), 1, 0.05]}, 'hands': {'R': 'flat'}, 'face': {'brow': 0.6, 'eye': 0.3}}, toonDur=0.08)]) for n, p, ry in ROW8]],   # « lui »: the heads turn to him
        props=[*STUCK(), P('backpack8', 'backpack', on={'actor': 'rando', 'joint': 'torso', 'offset': [0, 0.42, -0.24]}),
               *[P(f'comp8{i}', 'compass', on={'actor': n, 'hand': 'R', 'offset': [0, 0.03, 0.15], 'face': 'camera'}, scale=3.0, opts={'upright': True, 'path': PATH8}) for i, (n, p, ry) in enumerate(ROW8)]],   # every needle follows him along
        cams=[FC(0.0, [round(X8 - 6.4, 3), 2.9, round(ZL8 - 0.3, 3)], [[ROW8[0][1][0], 2.3, round(ROW8[0][1][2] - 0.4, 3)], [ROW8[2][1][0], 2.3, round(ROW8[2][1][2] + 0.4, 3)], [X8, 2.65, ZL8], [ROW8[1][1][0], 0.3, ZL8]], top=0.14, bottom=0.74)])   # (pass 3) square to the row from the road: the gap in the row is a gap in the frame
st.cue('sfx:zip', 'S08', 0.1, 0.2)

# ---- his building: a block on the right-hand side of the street (flatsWall, three floors over the shops); his window, the middle of the third floor
FX = 8.6; FLATS = lambda: P('flats', 'flatsWall', pos=[FX, 0, 30.0], ry=-90, opts={'w': 6.0, 'h': 12.6, 'cols': 3, 'rows': 3, 'depth': 1.25, 'y0': 3.0})
WIN = [round(FX + 0.42, 3), 9.0, 30.0]                              # he stands in his window, third floor   # (pass 3) 0.2 m nearer the front
RAIL = round(FX - 0.3, 3); RAILY = round(WIN[1] + 1.42, 3)           # just outside the top rail of his railing (9.95 + 0.42 m)
LEANW = {'bend': {'spine': [0.5, 0, 0, 1, None]}, 'reach': {'L': [RAIL, RAILY, round(WIN[2] + 0.22, 3), 1, 0.05, [0.7, -0.15, 0.7]], 'R': [RAIL, RAILY, round(WIN[2] - 0.22, 3), 1, 0.05, [-0.7, -0.15, 0.7]]}, 'hands': {'L': 'flat', 'R': 'flat'}}   # (pass 3) his forearms on the top rail
HIM_WIN = lambda keys=(): act('mec', WIN, -90, 'stand', 'unimpressed', keys=[k(0.0, look=[PX, 0.5, 30.0]), k(0.0, toon=LEANW, toonDur=0.0), *keys])   # (pass 2) leaning out on his railing (upright behind it, from below he was hidden)
CROWD = [('rando', [PX - 0.5, 0, 28.8], 75), ('rando2', [PX - 0.9, 0, 29.6], 80), ('touriste', [PX - 0.6, 0, 31.2], 105)]
def RAISE(p, ry, hy=2.05, side=0.32, fwd=0.2):                    # (pass 2) the compass held up beside the head, to the right (at chest height, from behind, their bodies hid it)
    f = (math.sin(math.radians(ry)), math.cos(math.radians(ry))); r = (-f[1], f[0])
    return [round(p[0] + fwd * f[0] + side * r[0], 3), hy, round(p[2] + fwd * f[1] + side * r[1], 3), 1, 0.05]
LOOKUP = lambda n, p, ry, t0=0.0: act(n, p, ry, 'stand', 'neutral', keys=[k(t0, look=[WIN[0], WIN[1] + 1.6, WIN[2]]), k(0.0, toon={'reach': {'R': RAISE(p, ry)}, 'hands': {'R': 'flat'}}, toonDur=0.0)])
CROWD_PROPS = lambda at=0.0: [P('bpA', 'backpack', on={'actor': 'rando', 'joint': 'torso', 'offset': [0, 0.42, -0.24]}), P('bpB', 'backpack', on={'actor': 'rando2', 'joint': 'torso', 'offset': [0, 0.42, -0.24]}, opts={'color': '#B5532A'}),
                       *[P(f'cc{i}', 'compass', on={'actor': n, 'hand': 'R', 'offset': [0, 0.03, 0.1], 'face': 'camera'}, scale=2.8, opts={'upright': True, 'target': [WIN[0], WIN[1] + 1.4, WIN[2]], 'at': at}) for i, (n, p, ry) in enumerate(CROWD)]]   # (pass 2) dials turned to us, the needles up at his window (pass 3: aimed in the turned dial, red end up)

# 7 (line): hikers, — at the foot of his block: three hikers with backpacks arrive, compasses out, the needles pointing up at his window
D9 = st.dur('S09'); END9 = [6.75, 8.35, 29.25]
C9A = FC(0.0, [1.8, 1.3, 26.2], [[PX - 0.9, 0.9, 29.6], [PX - 0.5, 2.5, 28.8], [PX - 0.6, 2.5, 31.2], [round(PX - 0.6, 3), 1.2, 31.4]], top=0.12, bottom=0.74)   # (pass 2) behind them, the raised compasses
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[HIM_WIN(), *[act(n, [p[0], 0, p[2] - 2.0], ry, 'stand', 'neutral', keys=[k(0.0, look=[WIN[0], WIN[1] + 1.6, WIN[2]]), k(0.0, to=p, dur=0.55, clip='walk', then='stand', ease='out'),   # (pass 2) in along the pavement
                                                                                                                        k(0.0, toon={'touch': {'R': ['torso', -0.18, 0.25, 0.32, 1, 0.05]}, 'hands': {'R': 'flat'}}, toonDur=0.0),   # (pass 2) at his chest while he walks
                                                                                                                        k(0.28, toon={'reach': {'R': RAISE(p, ry)}, 'hands': {'R': 'flat'}}, toonDur=0.12, toonEase='outBack')]) for n, p, ry in CROWD]],   # (pass 3) up go the compasses as they arrive
        props=[FLATS(), *CROWD_PROPS(at=0.3)],
        cams=[C9A, cam(0.64, C9A['from'], END9, C9A['lookAt'], [round(WIN[0] - 0.55, 3), 10.05, WIN[2]], lens=C9A['lens'], ease='out')])   # (pass 3) a later crane, ending tight on him: the window a third of the frame   # (pass 2) then a crane up to his window, leaning out (one frame for both made him a speck)

# 7 (line): boats, — a sailboat on its trailer rolls in and stops dead under his window: (pass 3) the hull pitches onto its bow and rocks, the mast
#    whips; the skipper at the stern lurches forward and back, his compass held up beside his head
D10 = st.dur('S10'); BOAT = [4.4, 0, 33.4]; ARR10 = 0.3; DECK = 1.12; SKIP10 = [4.4, DECK, round(BOAT[2] - 1.15, 3)]
UP10 = lambda **f: {'reach': {'R': RAISE(SKIP10, 0, hy=round(DECK + 2.0, 3))}, 'hands': {'R': 'flat'}, **f}
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[HIM_WIN(), *[LOOKUP(n, p, ry) for n, p, ry in CROWD],
        act('skipper', [SKIP10[0], DECK, round(SKIP10[2] - 6.0, 3)], 0, 'stand', 'neutral', keys=[k(0.0, look=[WIN[0], WIN[1] + 1.6, WIN[2]]), k(0.0, to=SKIP10, dur=ARR10, glide=True, ease='out', face='keep'),
            k(0.0, toon=UP10(), toonDur=0.0), k(ARR10, toon=UP10(lay=[0.24, 0], face={'eye': 0.3, 'brow': 0.7}), toonDur=0.04, toonEase='out'),   # the boat stops dead: he lurches forward...
            k(round(ARR10 + 0.1, 3), toon=UP10(lay=[-0.08, 0]), toonDur=0.08), k(round(ARR10 + 0.2, 3), toon=UP10(), toonDur=0.1)])],   # ...back, and settles, the compass still up
        props=[FLATS(), *CROWD_PROPS(), P('boat', 'sailboat', pos=[BOAT[0], 0, BOAT[2] - 6.0], ry=-90, opts={'brake': ARR10}, keys=[k(0.0, to=BOAT, dur=ARR10, ease='out')]),
               P('cskip', 'compass', on={'actor': 'skipper', 'hand': 'R', 'offset': [0, 0.03, 0.1], 'face': 'camera'}, scale=2.8, opts={'upright': True, 'target': [WIN[0], WIN[1] + 1.4, WIN[2]], 'at': ARR10})],
        cams=[FC(0.0, [1.6, 1.0, 27.0], [[BOAT[0], 4.3, round(BOAT[2] + 0.2, 3)], [BOAT[0], 0.0, round(BOAT[2] - 1.7, 3)], [BOAT[0], 0.0, round(BOAT[2] + 1.9, 3)], [PX - 0.6, 2.4, 31.2], [round(SKIP10[0] + 0.3, 3), round(DECK + 2.3, 3), SKIP10[2]]], top=0.1, bottom=0.74)])
st.cue('sfx:brake', 'S10', ARR10 - 0.08, 0.3)

# 7 (line): planes: everybody comes to his place. Wide from the road: a little plane taxis in and stops, propeller turning; the hikers, the boat;
#    up at his window he leans out, deadpan
D11 = st.dur('S11'); PLANE = [1.2, 0, 26.0]
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[HIM_WIN(keys=[k(0.0, toon=LEANW, toonDur=0.0), k(0.9, look='camera'), k(0.9, toon={**LEANW, 'face': {'lid': 0.4}}, toonDur=0.15),   # (pass 2) leaning on his railing
        k(1.4, toon={**LEANW, 'face': {'lid': 1}}, toonDur=0.06), k(1.5, toon={**LEANW, 'face': {'lid': 0.45}}, toonDur=0.08)]), *[LOOKUP(n, p, ry) for n, p, ry in CROWD],
        act('skipper', [4.4, 1.0, 33.4], 0, 'stand', 'neutral', keys=[k(0.0, look=[WIN[0], WIN[1] + 1.6, WIN[2]])])],
        props=[FLATS(), *CROWD_PROPS(), P('boat', 'sailboat', pos=BOAT, ry=-90), P('plane', 'propPlane', pos=[PLANE[0], 0, PLANE[2] - 9.0], ry=-90, scale=0.75, opts={'prop': 6},
               keys=[k(0.0, to=PLANE, dur=0.85, ease='out'), k(0.85, squash=[1.0, 0.95, 1.0], dur=0.0), k(0.92, squash=[1, 1, 1], dur=0.1)])],
        cams=[FC(0.0, [-1.2, 2.0, 15.0], [[FX, 11.4, 30.0], [PLANE[0], 0.0, PLANE[2] + 2.0], [PLANE[0], 2.2, PLANE[2] + 2.0], [round(PLANE[0] + 3.1, 3), 1.5, round(PLANE[2] + 0.4, 3)], [BOAT[0], 4.4, BOAT[2]], [PX - 0.6, 0.0, 31.2]], top=0.08, bottom=0.74, drift=(0.08, 0.04, 0.12)),   # (first look) wider: the window, the crowd, the boat, the plane's nose and its right wing
              FC(1.0, [round(WIN[0] - 2.6, 3), round(WIN[1] + 0.85, 3), round(WIN[2] + 1.0, 3)], [[WIN[0], 11.3, WIN[2]], [round(WIN[0] - 0.4, 3), 9.85, WIN[2]], [round(WIN[0] - 0.4, 3), 10.6, round(WIN[2] - 0.6, 3)], [round(WIN[0] - 0.4, 3), 10.6, round(WIN[2] + 0.6, 3)]], top=0.14, bottom=0.7, drift=(0.04, 0.03, -0.04))])   # (pass 2) from below, tight on him leaning out (the lower half was blank wall)   # then up at his window: he leans on the sill, deadpan, and looks at us
st.cue('engine', 'S11', 0.0, 0.35, 1.0)

# ---- the cartographers' office: a wall map of France, two cartographers in lab coats and glasses
MAP = [-0.4, 1.75, -3.55]; CART = [('carto1', [0.75, 0, -3.0], -50), ('carto2', [-1.55, 0, -2.95], 45)]   # (pass 3) at either side of the map, three-quarter to us (in profile at the frame edges before)
# 8 (line): the cartographers ruled. The one on the right taps the compass rose three times, his arm stretched right across the map; the one on the left
#    nods once, hard, at us
D12 = st.dur('S12')
TAP12 = [round(MAP[0] - 0.6, 3), round(MAP[1] + 0.35, 3), round(MAP[2] + 0.06, 3)]; BACK12 = [round(TAP12[0] + 0.25, 3), round(TAP12[1] - 0.1, 3), round(TAP12[2] + 0.3, 3)]
TAPK = lambda pt: {'reach': {'R': [*pt, 1, 0.08]}, 'hands': {'R': 'point'}, 'hose': 0.12, 'face': {'brow': 0.5}}
st.shot('S12', 'office', setOpts={'door': False}, actors=[
        act('carto1', CART[0][1], CART[0][2], 'stand', 'determined', keys=[k(0.0, look=TAP12), k(0.0, toon=TAPK(BACK12), toonDur=0.0),
            *[x for i in range(3) for x in (k(round(0.2 + 0.25 * i, 3), toon=TAPK(TAP12), toonDur=0.06, toonEase='in'), k(round(0.3 + 0.25 * i, 3), toon=TAPK(BACK12), toonDur=0.1, toonEase='out'))],   # tap, tap, tap
            k(1.0, look='camera'), k(1.0, toon={'face': {'brow': 0.6}}, toonDur=0.15)]),
        act('carto2', CART[1][1], CART[1][2], 'stand', 'neutral', keys=[k(0.0, look=[0.75, 2.2, -3.0]), k(0.55, look='camera'),
            k(0.82, toon={'bend': {'neck': [0.6, 0, 0, 1, None], 'spine': [0.12, 0, 0, 1, None]}, 'sq': [1.04, 0.95, 1.04], 'face': {'lid': 0.4, 'brow': 0.6}}, toonDur=0.08, toonEase='in'),   # one big nod...
            k(0.94, toon={'bend': {'neck': [-0.22, 0, 0, 1, None]}, 'sq': [0.98, 1.03, 0.98], 'face': {'brow': 0.8}}, toonDur=0.08, toonEase='out'), k(1.06, toon={'face': {'brow': 0.5}}, toonDur=0.12)])],   # ...back up past level, settles
        props=[P('map', 'mapFrance', pos=MAP, opts={'w': 1.5, 'h': 1.2, 'pin': [0.62, 0.66]})],   # (his arm stretches to the map: the pointer is his finger)
        cams=[FC(0.0, [-0.35, 1.7, 1.5], [[MAP[0] - 0.8, 2.4, MAP[2]], [MAP[0] + 0.8, 1.1, MAP[2]], [round(CART[0][1][0] + 0.45, 3), 2.35, CART[0][1][2]], [round(CART[1][1][0] - 0.45, 3), 2.35, CART[1][1][2]], [round(CART[0][1][0] + 0.45, 3), 0.3, CART[0][1][2]], [round(CART[1][1][0] - 0.45, 3), 0.3, CART[1][1][2]]], top=0.12, bottom=0.74)])   # (pass 3) half a metre of margin outside each
[st.cue('sfx:tick', 'S12', round(0.26 + 0.25 * i, 3), 0.25) for i in range(3)]

# 9 (line): the north, from now on, is him. Close on the map: the N of the rose is crossed out in red, a fat arrow is drawn to his face on the map
#    (NORD); then the whole map turns on the wall so that he comes to the top
D13 = st.dur('S13'); CR13, ROT13, AR13 = 0.1, 0.35, (1.05, 1.45)   # (pass 2) crossed out, turned over, then the arrow up to him
M13 = [0.25, 2.02, -3.5]                                             # (pass 2) the close-up cheats the map 0.65 m right and up: the window frame cut its left corner, the desks its bottom one
st.shot('S13', 'office', setOpts={'door': False}, actors=[],
        props=[P('map', 'mapFrance', pos=M13, opts={'w': 1.5, 'h': 1.2, 'pin': [0.62, 0.66], 'cross': CR13, 'arrow': list(AR13), 'rotate': [[ROT13, -10.0], [round(ROT13 + 0.12, 3), 150.0], [round(ROT13 + 0.55, 3), 136.0]], 'wordRot': 136, 'wordBeyond': True})],   # (pass 3) NORD beyond the pin, outlined: clear of the arrow
        cams=[cam(0.0, [M13[0], round(M13[1] - 0.08, 3), 1.95], [M13[0], round(M13[1] - 0.06, 3), 1.75], [M13[0], round(M13[1] - 0.05, 3), M13[2]], [M13[0], round(M13[1] - 0.03, 3), M13[2]], lens=40)])   # (pass 2) the whole map, the rose inside the frame, room for the turn
st.cue('sfx:scratch', 'S13', CR13, 0.3); st.cue('sfx:scratch', 'S13', AR13[0], 0.3); st.cue('sfx:squeak', 'S13', ROT13, 0.25)
st.card('S13', 'NORD', at=round(AR13[1], 3))

# 10 (line): all the maps were redrawn. The globe on the desk is spun; it slows and stops with his little block of flats on the pole, facing us
D14 = st.dur('S14'); GLOBE = [2.0, 0.72, -3.15]
st.shot('S14', 'office', setOpts={'door': False}, actors=[],
        props=[P('globe', 'globe', pos=GLOBE, opts={'r': 0.3, 'houseScale': 2.6, 'spin': [[0.05, round(D14 - 0.35, 3), 2.0]], 'houseLat': [[0.0, 28.0], [round(D14 - 0.32, 3), 90.0]]})],   # (pass 3) his block rides round, then slides up onto the pole once the globe stops
        cams=[cam(0.0, [GLOBE[0] + 0.15, 1.75, -1.75], [GLOBE[0] + 0.13, 1.73, -1.85], [GLOBE[0], 1.42, GLOBE[2]], [GLOBE[0], 1.44, GLOBE[2]], lens=40)])   # (pass 2) higher: the pole and his block on it in the frame
st.cue('sfx:zip', 'S14', 0.05, 0.25)

# 11 (line): he lives at the North Pole. His living room: snow falling indoors, drifts along the wall, frost on his face and his breath smoking; a polar
#     bear sits beside him on the sofa. (pass 3) A cold blue light; he shivers from head to foot, teeth chattering; his breath drifts off his face; snow
#     on the sofa back and arms, drifts at both ends
D15 = st.dur('S15'); SOFA = [0.0, 0, -2.75]
FORKS_LOW = lambda: [P(f'cl{i}', kind, on={'actor': 'mec', 'joint': 'torso', 'offset': [round(-lat, 3), round(y - 1.08, 3), 0.2], 'rot': [0, 0, fan]}, scale=CS, opts=CUTOPT(kind)) for i, (lat, y, fan, kind) in enumerate([(a, b, c, d) for (_, d, _f, a, b, c) in CUT2] + [(a, b, c, 'fork') for (a, b, c) in FAN3]) if y <= 1.36]   # (pass 3) only the lower ones, lower still: two forks covered his mouth
SHIV15 = [k(round(0.04 * i, 3), toon={'lay': [0, round(0.022 * (1 if i % 2 else -1), 3)], 'sq': [1.0, round(1.0 - 0.012 * (i % 2), 3), 1.0], 'face': {'lid': 0.45, 'jaw': 0.1 if i % 2 else 0.0, 'mouth': 'teeth', 'tremble': 1, **({'gx': -0.5} if 0.04 * i >= 0.7 else {})}}, toonDur=0.03) for i in range(int(D15 / 0.04))]   # shivering, teeth chattering
st.shot('S15', 'livingRoom', setOpts={'tv': False}, look={'sunColor': '#D6E4FF', 'tint': [0.9, 0.97, 1.1], 'warm': 0.25, 'sat': 0.9}, actors=[   # (pass 3) cool: it was graded as warm as the kitchen
        act('mec', [0.5, 0, -2.75], 0, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, fx={'breath': {'side': 0.32, 'up': 0.2, 'fwd': 0.12, 'size': 0.85}}), *SHIV15]),
        act('ours', [-0.62, 0, -2.85], 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.62, look=[0.5, 1.6, -2.75])])],
        props=[*FORKS_LOW(), P('snow', 'snowfall', pos=[0.0, 0, -1.6], opts={'w': 5.5, 'h': 4.0, 'd': 4.5, 'n': 800, 'size': 0.085}), P('bank', 'snowBank', pos=[0.0, 0, -3.42], opts={'len': 6.0}),
               P('bankL', 'snowBank', pos=[-1.85, 0, -2.45], opts={'len': 1.3, 'seed': 33}), P('bankR', 'snowBank', pos=[1.85, 0, -2.4], opts={'len': 1.3, 'seed': 35}),
               P('capB', 'snowBank', pos=[0.0, 1.07, -3.27], scale=0.7, opts={'len': 3.4, 'seed': 37}), P('capL', 'snowBank', pos=[-1.2, 0.7, -2.95], scale=0.6, opts={'len': 0.6, 'seed': 39}), P('capR', 'snowBank', pos=[1.2, 0.7, -2.95], scale=0.6, opts={'len': 0.6, 'seed': 41})],
        cams=[FC(0.0, [0.3, 1.3, 1.6], [[-1.2, 2.2, -2.85], [1.1, 2.1, -2.75], [0.0, 0.45, -2.4]], top=0.12, bottom=0.74, drift=(0.0, 0.0, -0.18))])   # (pass 3) tighter: to the knees
st.cue('sfx:ticks', 'S15', 0.1, 0.18)

# 12 (line): third floor, no lift. (pass 2) From the top of the stairwell: two explorers in red parkas climb the last flight bent double, heaving; one
#     swings his pennant down into the doormat (PÔLE NORD); the door opens; he looks down at them; then close on him in the doorway, a look at us
D16 = st.dur('S16'); LAND = 1.6; DOOR = [0.0, LAND, -2.9]; OPEN16 = 1.3; FLAG16 = 1.0
SLAB = '#D9D0C1'
EXP = [('explo1', [1.5, LAND, -0.45], -150), ('explo2', [2.25, LAND, 0.05], -145)]   # (pass 2) to the right: from the stairwell his bent head hid the planted pennant
HEAVE = lambda t0, s_=1.0: [k(round(t0 + 0.2 * i, 3), toon={'bend': {'spine': [0.95 if i % 2 == 0 else 0.68, 0, 0, 1, None], 'neck': [-0.3, 0, 0, 1, None], 'armL': [0.15 if i % 2 == 0 else -0.05, 0.1, 0, 1, None], 'armR': [0.15 if i % 2 == 0 else -0.05, -0.1, 0, 1, None]},
                                                                  'sq': [round(1.0 + (0.07 if i % 2 == 0 else -0.03) * s_, 3), round(1.0 - (0.08 if i % 2 == 0 else -0.04) * s_, 3), 1.0], 'face': {'jaw': 0.75 if i % 2 == 0 else 0.35, 'sweat': 1, 'lid': 0.55}}, toonDur=0.18, toonEase='inOut') for i in range(10)]   # (pass 3) doubled over, heaving hard: the back pumps, the shoulders rise and fall
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
               P('stairs16', 'stairs', pos=[1.25, 0, 2.44], opts={'steps': 8, 'w': 1.3, 'rail': False, 'nosing': False}),   # (pass 3) no handrail (it read as a pole into the captions), no navy nosing (broken lines from above)   # the last flight, coming up to the landing
               P('door16', 'door', pos=[DOOR[0], LAND, round(DOOR[2] + 0.02, 3)], opts={'w': 0.95, 'h': 2.15, 'openAt': OPEN16}),
               P('mat16', 'doormat', pos=[DOOR[0], round(LAND + 0.012, 3), -2.2], opts={'text': 'PÔLE NORD', 'w': 1.45, 'd': 0.84}),   # (pass 3) bigger: the letters were 7 px
               P('plaque16', 'bronzePlaque', pos=[1.6, round(LAND + 1.55, 3), round(DOOR[2] + 0.02, 3)], opts={'text': '3e ÉTAGE', 'w': 1.0, 'h': 0.4}),   # (pass 3) whole in the wide, outside the close-up (it was cut to « 3e É »)
               *[P(f'bp16{i}', 'backpack', on={'actor': n, 'joint': 'torso', 'offset': [0, 0.42, -0.24]}, opts={'color': '#2F7F5C' if i == 0 else '#B5532A'}) for i, (n, p_, ry) in enumerate(EXP)],
               P('flag16p', 'flag', on={'actor': 'explo1', 'joint': 'torso', 'offset': [0.12, 0.45, -0.32]}, scale=0.7, opts={'colors': ['#F2C230', '#F2C230', '#F2C230'], 'vertical': False, 'poleR': 0.03, 'poleColor': '#3A3D44'}, keys=[k(round(FLAG16 - 0.2, 3), visible=False)]),   # (pass 2) a pennant up off his backpack (held in the hand all the way it hung upside down)
               P('flag16', 'flag', on={'actor': 'explo1', 'hand': 'R', 'offset': [0, 0.0, 0.05], 'rot': [math.pi, 0, 0]}, opts={'colors': ['#F2C230', '#F2C230', '#F2C230'], 'vertical': False, 'poleR': 0.03, 'poleColor': '#3A3D44'}, keys=[k(0.0, visible=False), k(round(FLAG16 - 0.2, 3), visible=True), k(round(FLAG16 - 0.1, 3), visible=False)]),   # in his raised fist for a moment (the pole past the fingers points up only while the arm does)   # (pass 2) a thick dark pole: from high up a thin grey one vanished and the cloth floated like a card
               P('flag16b', 'flag', pos=[0.42, round(LAND + 0.75, 3), -1.95], ry=-30, opts={'colors': ['#F2C230', '#F2C230', '#F2C230'], 'vertical': False, 'poleR': 0.03, 'poleColor': '#3A3D44'}, keys=[k(0.0, visible=False), k(round(FLAG16 - 0.1, 3), visible=True),
                 k(round(FLAG16 - 0.1, 3), squash=[1.0, 1.45, 1.0], dur=0.0), k(round(FLAG16 - 0.1, 3), to=[0.42, LAND, -1.95], dur=0.1, ease='in'), k(FLAG16, squash=[1.0, 0.82, 1.0], dur=0.0), k(round(FLAG16 + 0.06, 3), squash=[1, 1, 1], dur=0.1)]),   # (pass 2) driven down into the mat   # (pass 3) stretched on its way down (a smear), squashed on the hit
               *[P(f'cl{i}', kind, on={'actor': 'mec', 'joint': 'torso', 'offset': [round(-lat, 3), round(y - 1.0, 3), 0.2], 'rot': [0, 0, fan]}, scale=CS, opts=CUTOPT(kind)) for i, (pid, kind, frm, lat, y, fan) in enumerate(CUT2)]],
        cams=[FC(0.0, [1.2, 7.5, 5.5], [[DOOR[0] - 0.6, LAND + 2.45, DOOR[2]], [DOOR[0] + 0.6, LAND + 2.45, DOOR[2]], [-0.35, LAND, -2.0], [1.4, 0.6, 1.62], [1.4, 2.6, 1.62], [2.4, LAND + 1.8, 0.05]], top=0.1, bottom=0.74, drift=(0.0, -0.08, -0.1)),   # (pass 2) they start higher up the flight: a tighter wide   # (pass 2) down the stairwell from high behind the last flight: its depth runs up the tall frame (from the side it ran across it and they were specks), and the leaf, seen edge on, leaves the doorway clear
              FC(round(OPEN16 + 0.6, 3), [-0.5, round(LAND + 1.8, 3), -0.6], [[DOOR[0], round(LAND + 2.4, 3), round(DOOR[2] + 0.35, 3)], [DOOR[0], round(LAND + 1.15, 3), round(DOOR[2] + 0.35, 3)], [DOOR[0] - 0.4, round(LAND + 1.7, 3), round(DOOR[2] + 0.35, 3)], [DOOR[0] + 0.4, round(LAND + 1.7, 3), round(DOOR[2] + 0.35, 3)]], top=0.16, bottom=0.68)])   # then close on him in the doorway
st.cue('sfx:gasp', 'S16', 0.1, 0.3); st.cue('sfx:gasp', 'S16', 0.55, 0.25); st.cue('thud', 'S16', FLAG16, 0.3); st.cue('sfx:carDoor', 'S16', OPEN16, 0.25)

st.write("L'aimant", rig='toon', fingers=True, cloth=True, idleShift=1.6, limbSmear=1, follow=1, pupil=0.5, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'rando': {'preset': 'tourist', 'seed': 471, 'hat': 'beanie', 'build': {'width': 0.92, 'headWidth': 1.25}},
    'rando2': {'preset': 'sportif', 'seed': 472, 'hat': 'beanie', 'build': {'width': 0.9, 'headWidth': 1.25}},
    'touriste': {'preset': 'tourist', 'seed': 473, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'mamie': {'preset': 'mamie', 'seed': 474, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'skipper': {'preset': 'fermier', 'seed': 475, 'hat': 'beanie', 'build': {'width': 0.95, 'headWidth': 1.25}},
    'carto1': {'preset': 'savant', 'seed': 476, 'hair': 'receding', 'hairColor': '#EDEDED', 'build': {'width': 0.9, 'headWidth': 1.25}},
    'carto2': {'preset': 'savant', 'seed': 477, 'hair': 'receding', 'hairColor': '#EDEDED', 'build': {'width': 0.95, 'headWidth': 1.25}},
    'explo1': {'preset': 'sportif', 'seed': 478, 'hat': 'beanie', 'hatColor': '#F4F2EA', 'suit': '#C8322A', 'pants': '#3A3D44', 'build': {'width': 1.05, 'headWidth': 1.25}},   # (pass 2) a red parka, dark trousers, a white hood
    'explo2': {'preset': 'sportif', 'seed': 479, 'hat': 'beanie', 'hatColor': '#F4F2EA', 'suit': '#D9822B', 'pants': '#3A3D44', 'build': {'width': 1.05, 'headWidth': 1.25}},
    'ours': {'type': 'creature', 'name': 'bear', 'opts': {'seed': 7, 'colors': {'body': '#F2F0E8', 'belly': '#E6E2D6', 'snout': '#D8D2C2', 'paw': '#CFC8B8'}}},
})
