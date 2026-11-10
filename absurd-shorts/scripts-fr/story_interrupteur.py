#!/usr/bin/env python3
"""L'interrupteur (story 40, cycle 4 of the cartoon staging): this man turned the light off on his way out. The whole city went out. He turned it
back on; it came back on. The town hall sent for an electrician: "The main switch, it's him." Since then he turns Paris off every evening at ten.
The burglars love him. The lovers too. The bill comes in his name. The whole bill. He asked for a raise. He got a night bonus. Yesterday at noon
he stepped out of his house. By reflex, he turned off. It has been night since. The astronomers are looking. The bill has already arrived.
Cartoon rig, cycle 4: shots in the dark (`dark`: only the eyes stay), a face keyed feature by feature, a ripple along a stretched arm, the tie as a
pull cord (toon channel `tie`). Natural look."""
from story_kit import *
import math

st = Story('interrupteur', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 6), ('S03', 'L01', 8), ('S04', 'L02', 0), ('S05', 'L02', 3), ('S06', 'L03', 0), ('S07', 'L03', 5), ('S08', 'L04', 0), ('S09', 'L04', 2),
         ('S10', 'L05', 0), ('S11', 'L05', 3), ('S12', 'L06', 0), ('S13', 'L06', 3), ('S14', 'L07', 0), ('S15', 'L07', 6), ('S16', 'L08', 0), ('S17', 'L08', 5),
         ('S18', 'L09', 0), ('S19', 'L09', 3), ('S20', 'L10', 0), ('S21', 'L10', 2), ('S22', 'L11', 0), ('S23', 'L12', 0), ('S24', 'L12', 3), ('S25', 'L12', 6)])

def glide(c, g=0.2): return {**c[0], 'cut': False, 'glide': g}
r3 = lambda v: [round(x, 3) for x in v]
# a ripple along a stretched arm (toon channel `wave`): a metres high, n waves on each half, moved along by ph (rising: toward the hand), vertical
RIP = lambda sd, a, ph, n=2: {'arm' + sd: [a, n, ph, 0, 1.5708], 'fore' + sd: [a, n, ph - n, 0, 1.5708]}
# where the tip of his tie hangs (the tie of the cartoon rig: 0.41 m long from a knot 1.61 m up, 0.135 m in front of the chest), for a man standing at
# pos, turned ry degrees, the tie stretched to `length` times its own and swung `fwd` radians away from the chest
def tie_tip(pos, ry, length=1.0, fwd=0.0):
    a = math.radians(ry); L = 0.02 + 0.41 * length; f = 0.135 + L * math.sin(fwd); y = 1.61 - L * math.cos(fwd)
    return r3([pos[0] + f * math.sin(a), pos[1] + y, pos[2] + f * math.cos(a)])

# ---- his living room (back wall at z = -3.6): the camera stands in the doorway, he is on his way out; the switch is far behind him, on the back wall
LIV = {'lamp': False, 'tv': False, 'plant': False}
H1 = [-0.2, 0, 1.3]                                  # where he stands, on his way out
SW1 = [1.4, 1.55, -3.56]                             # the switch (three times its size: it must read from the door)
C1 = lambda t=0.0: cam(t, [0.0, 1.55, 4.6], [0.0, 1.55, 4.5], [0.3, 1.5, -1.0], [0.3, 1.5, -1.0], lens=44)
SWITCH = lambda flips, on=True: P('switch', 'rockerSwitch', pos=SW1, opts={'s': 2.4, 'flips': flips, 'on': on})
TO_SW = lambda d, **kw: {'hands': {'L': 'point'}, 'reach': {'L': [SW1[0] - 0.02, SW1[1] + 0.02, SW1[2] + d, 1, 0.16, [0.5, -1, 0.3]]}, **kw}   # his left index d metres short of the rocker, the arm across the room

# 1: on his way out: a glance back with his eyes alone; the arm goes back across the whole room, a ripple along it; the finger stops short of the
#    switch, then taps it: black. Two eyes
A1, B1, K1 = 0.2, 0.32, 0.62                         # the wind-up, the throw, the tap
st.shot('S01', 'livingRoom', setOpts=LIV, actors=[act('mec', H1, 6, 'stand', 'neutral', keys=[k(0.0, look=None), k(0.08, toon={'face': {'gx': 0.9, 'gy': -0.1}}, toonDur=0.06),   # the light: his eyes go back to it, not his head
            k(A1, toon={'hands': {'L': 'point'}, 'reach': {'L': [0.25, 1.35, 2.0, 1, 0.16]}, 'bend': {'spine': [0.1, 0.14, 0, 1, None]}, 'sq': [1.04, 0.95, 1.04], 'face': {'gx': 0.9}}, toonDur=0.1, toonEase='out'),   # the index comes forward: the wind-up
            k(B1, toon=TO_SW(0.5, wave=RIP('L', 0.16, 0.6), bend={'spine': [-0.08, -0.16, 0, 1, None]}, sq=[0.97, 1.05, 0.97], face={'gx': 0.9, 'browL': 0.6}), toonDur=0.12, toonEase='out'),   # thrown back across the room
            k(B1 + 0.14, toon=TO_SW(0.16, wave=RIP('L', 0.07, 1.6), bend={'spine': [0, -0.1, 0, 1, None]}, face={'gx': 0.9, 'browL': 0.6}), toonDur=0.12),   # it stops short, still ringing
            k(K1 - 0.03, toon=TO_SW(0.045, face={'gx': 0.9, 'browL': 0.6}), toonDur=0.04),   # the tap
            k(K1 + 0.1, toon=TO_SW(0.05), toonDur=0.06), k(K1 + 0.1, expr='surprised'),   # in the black: two eyes, to us
            k(K1 + 0.32, toon=TO_SW(0.05, face={'lid': 1}), toonDur=0.04), k(K1 + 0.4, toon=TO_SW(0.05), toonDur=0.04),   # a blink
            k(K1 + 0.46, toon={'face': {'gx': -0.8}}, toonDur=0.12, toonEase='inOut')])],   # the arm comes home; his eyes go to the door
        props=[SWITCH([K1])],
        dark=[[K1 + 0.02, 1]], darkFloor=0.035,
        cams=[C1()])

# 2: on his way out, in the black: two eyes come toward us, bobbing with his steps; he walks into the glass door: flat on it, the eyes two spirals, stars
G2 = 0.5                                            # he meets the glass
ST2 = {'clear': [-30, 30], 'eiffel': False, 'night': True}
st.shot('S02', 'parisStreet', setOpts=ST2, lighting='night', actors=[act('mec', [8.6, 0, -4.6], 0, 'walk', 'neutral', keys=[k(0.0, look=None), k(0.0, to=[8.6, 0, -1.25], dur=G2, clip='walk', ease='linear'),
            k(G2, clip='pressGlass', expr='dizzy', blend=0.02), k(G2, toon={'sq': [1.5, 1.0, 0.22], 'scl': {'head': [1.25, 0.9, 1]}, 'face': {'stars': 1}}, toonDur=0.03),   # flat on the glass
            k(G2 + 0.12, toon={'sq': [1.35, 1.0, 0.3], 'face': {'stars': 1}}, toonDur=0.1), k(G2 + 0.14, to=[8.6, -0.55, -1.25], dur=0.26, ease='in', face='keep')])],   # and he slides down it
        dark=[[0, 1, 0.001]], darkFloor=0.035, darkEyes=1.5,
        fx=[{'type': 'shake', 'at': G2, 'dur': 0.16, 'amount': 0.03}],
        cams=[cam(0.0, [8.6, 1.62, 0.0], [8.6, 1.62, -0.05], [8.6, 1.6, -6.0], [8.6, 1.6, -6.0], lens=44)])

# 3: the whole city: Paris at night from a height; the black runs out from his street, row after row; the tower stands alone, lit, then pops; eyes open
#    in the dark windows
CITY = lambda keys, **kw: P('city', 'cityNight', pos=[0, 0, 0], opts={'keys': keys, **kw})
VIEW = lambda t, a, b: cam(t, a, b, [3.0, -3.5, -60.0], [3.0, -3.5, -60.0], lens=44)
st.shot('S03', 'spaceDark', setOpts={'stars': 300}, lighting='night',
        props=[CITY([[0.15, 0, 0.45]], towerLag=0.22, eyesLag=0.22, eyes=46)],
        cams=[VIEW(0.0, [0.0, 2.0, 8.0], [0.0, 1.8, 6.0])])

# 4: he turned it back on: the black, his eyes; the tap: the light: he stands where he stood, the arm across the room again, a lump on his head, a
#    star still going round it; the arm comes home
K4 = 0.28
st.shot('S04', 'livingRoom', setOpts=LIV, actors=[act('mec', H1, 6, 'stand', 'dizzy', keys=[k(-0.05, toon=TO_SW(0.16, face={'bump': 1, 'stars': 1}), toonDur=0), k(0.0, look=None),
            k(K4 - 0.03, toon=TO_SW(0.045, face={'bump': 1, 'stars': 1}), toonDur=0.04), k(K4 + 0.08, expr='unimpressed'),
            k(K4 + 0.1, toon=TO_SW(0.3, wave=RIP('L', 0.1, 0.5), face={'bump': 1, 'stars': 0.6, 'browR': -0.6, 'browL': 0.5}), toonDur=0.1),
            k(K4 + 0.26, toon={'face': {'bump': 1, 'stars': 0.3, 'browR': -0.6, 'browL': 0.5}, 'touch': {'R': ['face', 0.1, 1.02, 0.04, 1, 0.1]}, 'bend': {'spine': [0, 0.06, 0, 1, None]}}, toonDur=0.2, toonEase='outBack')])],   # the arm snaps home; the other hand goes to the lump
        props=[SWITCH([K4], on=False)],
        dark=[[0, 1, 0.001], [K4 + 0.02, 0]], darkFloor=0.035,
        cams=[C1()])

# 5: the city came back on: the light runs out again from his street; the tower glitters; then off, on: he is trying the switch
st.shot('S05', 'spaceDark', setOpts={'stars': 300}, lighting='night',
        props=[CITY([[0.1, 1, 0.35], [0.68, 0, 0.1], [0.86, 1, 0.1]], lit=0, towerLag=0.0, sparkle=[0.45, 0.68], eyes=0)],
        cams=[VIEW(0.0, [0.0, 1.8, 6.0], [0.0, 2.0, 7.4])])

# ---- the town hall brings an electrician to his living room
E7, H7 = [-0.36, 0, -0.3], [0.36, 0, -0.4]          # the electrician and him, face to face, three quarters to us
RE, RH = 30, -25
def face_pt(pos, ry, across=0.0, up=0.31, out=0.1):  # a point of the face of a man standing at pos, turned ry: across (m, + = his left), up (0 = chin .. 1 = top of the skull; nose 0.31, mouth 0.23, brow 0.8), out (m in front)
    a = math.radians(ry); return r3([pos[0] + out * math.sin(a) + across * math.cos(a), pos[1] + 1.77 + 0.5 * up, pos[2] + out * math.cos(a) - across * math.sin(a)])
NOSE7 = face_pt(H7, RH)
LUMP = {'bump': 0.8}

# 6: the mayor, in his sash, points at him; the electrician tears in with his meter and skids to a stop between them; his eyes go from the finger to the meter
M6, E6, H6 = [-0.78, 0, -1.8], [-0.05, 0, -0.3], [0.6, 0, -0.5]
st.shot('S06', 'livingRoom', setOpts=LIV, actors=[act('mec', H6, -18, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={'face': {**LUMP, 'gx': -0.9, 'browL': 0.7, 'browR': -0.4}}, toonDur=0.0),
            k(0.34, toon={'face': {**LUMP, 'gx': -0.5, 'gy': 0.7, 'browL': 0.9, 'browR': 0.9, 'eye': 0.2}}, toonDur=0.08, toonEase='outBack')]),   # the finger, then the meter under his nose
        act('maire', M6, 28, 'stand', 'angry', keys=[k(0.0, look='mec'), k(0.0, toon={'hands': {'R': 'point'}, 'reach': {'R': [-0.5, 2.2, -1.4, 1, 0.16]}, 'sq': [0.96, 1.06, 0.96]}, toonDur=0.0),
            k(0.1, toon={'hands': {'R': 'point'}, 'reach': {'R': [-0.1, 1.95, -1.0, 1, 0.16]}, 'bend': {'spine': [0.2, 0, 0, 1, None]}, 'face': {'jaw': 0.35}}, toonDur=0.08, toonEase='outBack')]),   # the finger comes down on him
        act('elec', [-2.9, 0, -0.3], 90, 'run', 'determined', keys=[k(0.0, to=E6, dur=0.3, clip='run', ease='linear', face=20), k(0.3, clip='skidStop', params={'dur': 0.3}, blend=0.03), k(0.3, look='mec'),
            k(0.56, clip='carry', blend=0.12, expr='hmm')])],
        props=[P('meter', 'voltMeter', pos=[-2.6, 1.0, 0.02], opts={'w': 0.42, 'needle': [[0, 0.12]]}, keys=[k(0.0, to=[0.12, 1.0, 0.06], dur=0.3, ease='linear'), k(0.3, to=[0.2, 1.02, 0.08], dur=0.2, ease='out'), k(0.5, to=[0.1, 1.02, 0.06], dur=0.2, ease='inOut')])],
        cams=[cam(0.0, [0.15, 1.6, 3.9], [0.12, 1.6, 3.7], [0.05, 1.45, -0.9], [0.05, 1.45, -0.9], lens=44)])

# 7: a clip on his nose: the needle slams over, the meter shakes and smokes; the electrician: eyes out, his helmet up; his: crossed on the clip
CL7, ND7 = 0.26, 0.38
MET7 = [0.0, 1.02, 0.12]
CLIP7 = lambda w, **kw: {'hands': {'R': 'pinch'}, 'reach': {'R': [NOSE7[0] - 0.03, NOSE7[1], NOSE7[2] + 0.02, w, 0.06]}, **kw}
st.shot('S07', 'livingRoom', setOpts=LIV, actors=[act('mec', H7, RH, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={'face': {**LUMP, 'gx': -0.6}}, toonDur=0.0),
            k(CL7, toon={'scl': {'head': [1.16, 0.88, 1]}, 'face': {**LUMP, 'cross': 1, 'eye': 0.35, 'brow': 0.8}}, toonDur=0.04), k(CL7 + 0.08, toon={'scl': {'head': [0.96, 1.04, 1]}, 'face': {**LUMP, 'cross': 1, 'eye': 0.35, 'brow': 0.8}}, toonDur=0.08, toonEase='outBack'),
            k(CL7 + 0.2, toon={'face': {**LUMP, 'cross': 1, 'eye': 0.35, 'brow': 0.8}}, toonDur=0.08), k(ND7 + 0.3, toon={'face': {**LUMP, 'cross': 0.6, 'eye': 0.2, 'browL': 0.8, 'browR': -0.3, 'gy': 0.5}}, toonDur=0.15)]),   # then down to the needle
        act('elec', E7, RE, 'stand', 'hmm', keys=[k(0.0, look=NOSE7), k(0.0, toon=CLIP7(0), toonDur=0.0), k(0.08, toon={'hands': {'R': 'pinch'}, 'reach': {'R': [-0.15, 1.75, 0.15, 1, 0.06]}, 'sq': [1.03, 0.96, 1.03]}, toonDur=0.08),   # the clip, held up
            k(CL7 - 0.06, toon=CLIP7(1), toonDur=0.06, toonEase='in'), k(CL7 + 0.1, toon={'face': {'gy': 0.8, 'gx': 0.3}}, toonDur=0.1), k(CL7 + 0.1, look=None),   # on his nose; his eyes go down to the dial
            k(ND7 + 0.06, expr='take'), k(ND7 + 0.06, toon={'sq': [0.9, 1.14, 0.9], 'hat': [0.3, 0.25, 0], 'face': {'pop': 0.85, 'jaw': 0.7, 'popLen': 0.16, 'eyeYaw': 0.5}}, toonDur=0.08, toonEase='outBack'),   # the take: eyes out at the dial, the helmet up
            k(ND7 + 0.4, toon={'hat': [0.05, 0.1, 0], 'face': {'pop': 0.5, 'jaw': 0.5, 'popLen': 0.12}}, toonDur=0.25)])],
        props=[P('meter', 'voltMeter', pos=MET7, rot=[-0.25, 0, 0], opts={'w': 0.44, 'needle': [[0, 0.12], [ND7 - 0.04, 0.12], [ND7 + 0.02, 1.0]], 'smokeAt': ND7 + 0.28}, keys=[k(ND7 + 0.02, squash=[1.12, 0.86, 1.0], dur=0.3)]),
               P('cable', 'jumperCable', pos=[MET7[0] + 0.1, MET7[1] + 0.2, MET7[2]], opts={'to': r3([NOSE7[0] - MET7[0] - 0.1, NOSE7[1] - MET7[1] - 0.2, NOSE7[2] - MET7[2] + 0.02]), 'sag': 0.22}, keys=[k(0.0, visible=False), k(CL7, visible=True)])],
        fx=[{'type': 'shake', 'at': ND7 + 0.02, 'dur': 0.3, 'amount': 0.012}],
        cams=[cam(0.0, [0.0, 1.62, 2.75], [0.0, 1.62, 2.6], [0.0, 1.55, -0.35], [0.0, 1.55, -0.35], lens=44)])

# 8: « L'interrupteur général, » : the electrician says it, takes the end of his tie and pulls it like the cord of a lamp: click, black: two pairs of
#    eyes; he pulls again: light
P8a, P8b = 0.6, 0.96
TIE8 = lambda L, fwd=0.25: tie_tip(H7, RH, L, fwd)
HOLD8 = lambda L, **kw: {'hands': {'R': 'grip'}, 'reach': {'R': [*TIE8(L), 1, 0.05, [-0.6, -0.6, 0.5]]}, **kw}   # the electrician's hand on the end of the tie
PULLED = lambda L, **kw: {'tie': [L, 0.25, 0], 'face': LUMP, **kw}   # him, the tie pulled to L times its length
def pull8(t):   # (his keys, the electrician's keys) for one pull at t: the tie goes down, his head after it; it snaps back, he springs up
    hk = [k(t - 0.06, toon=PULLED(1.75, bend={'spine': [0.28, 0, 0, 1, None], 'neck': [0.25, 0, 0, 0.8, None]}, sq=[1.05, 0.93, 1.05]), toonDur=0.06, toonEase='in'),
          k(t + 0.07, toon=PULLED(0.85, bend={'spine': [-0.1, 0, 0, 1.04, None], 'neck': [-0.1, 0, 0, 1.25, None]}, sq=[0.96, 1.07, 0.96]), toonDur=0.07, toonEase='out'),
          k(t + 0.17, toon=PULLED(1.06), toonDur=0.1), k(t + 0.26, toon=PULLED(1.0), toonDur=0.08)]
    ek = [k(t - 0.06, toon=HOLD8(1.75, bend={'spine': [0.12, 0, 0, 1, None]}), toonDur=0.06, toonEase='in'), k(t + 0.07, toon=HOLD8(0.9), toonDur=0.07, toonEase='out'), k(t + 0.17, toon=HOLD8(1.04), toonDur=0.1), k(t + 0.26, toon=HOLD8(1.0), toonDur=0.08)]
    return hk, ek
(h8a, e8a), (h8b, e8b) = pull8(P8a), pull8(P8b)
st.shot('S08', 'livingRoom', setOpts=LIV, actors=[act('mec', H7, RH, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=PULLED(1.0, face={**LUMP, 'gx': -0.5}), toonDur=0.0), k(0.3, toon=PULLED(1.0, face={**LUMP, 'gy': 0.8}), toonDur=0.1)] + h8a + h8b +   # his eyes go down to the hand on his tie
            [k(P8b + 0.3, toon=PULLED(1.0, face={**LUMP, 'browL': 0.8, 'browR': -0.5}), toonDur=0.1)]),
        act('elec', E7, RE, 'stand', 'neutral', keys=st.talk('L04', 'S08', 'smug') + [k(0.0, look='mec'), k(0.22, toon=HOLD8(1.0), toonDur=0.16, toonEase='out')] + e8a + e8b +
            [k(P8a + 0.12, look=None), k(P8b + 0.3, toon={'hands': {'L': 'thumbUp'}, 'reach': {'L': [0.0, 1.75, 0.0, 1, 0.1]}, 'face': {'browL': 0.8}}, toonDur=0.12, toonEase='outBack')])],   # in the black his eyes come to us; then a thumb at him
        dark=[[P8a + 0.02, 1], [P8b + 0.02, 0]], darkFloor=0.035,
        cams=[cam(0.0, [0.1, 1.6, 3.1], [0.08, 1.6, 2.95], [0.0, 1.5, -0.35], [0.0, 1.5, -0.35], lens=44)])

# 9: « c'est lui. » : he slaps the label of a fuse box on his forehead: GÉNÉRAL; his head goes into his shoulders and comes back, his eyes cross up to it
SL9 = 0.18
FORE9 = face_pt(H7, RH, 0.0, 0.8, 0.1)
st.shot('S09', 'livingRoom', setOpts=LIV, actors=[act('mec', H7, RH, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={'face': {'gx': -0.7, 'gy': -0.4}}, toonDur=0.0),
            k(SL9, toon={'scl': {'head': [1.3, 0.72, 1]}, 'bend': {'neck': [0, 0, 0, 0.5, None], 'spine': [0, 0, 0, 0.94, None]}, 'sq': [1.05, 0.94, 1.05], 'face': {'cross': 1, 'gy': -0.9, 'brow': 1, 'eye': 0.3}}, toonDur=0.03),
            k(SL9 + 0.1, toon={'scl': {'head': [0.93, 1.1, 1]}, 'bend': {'neck': [0, 0, 0, 1.3, None]}, 'face': {'cross': 1, 'gy': -0.9, 'brow': 1, 'eye': 0.3}}, toonDur=0.07, toonEase='out'),
            k(SL9 + 0.22, toon={'face': {'cross': 1, 'gy': -0.9, 'brow': 1, 'eye': 0.3}}, toonDur=0.12, toonEase='outBack'), k(SL9 + 0.42, toon={'face': {'browL': 0.7, 'browR': -0.6}}, toonDur=0.1), k(SL9 + 0.42, expr='deadpan')]),
        act('elec', E7, RE, 'stand', 'smug', keys=st.talk('L04', 'S09', 'smug') + [k(0.0, look='mec'), k(0.0, toon={'hands': {'R': 'open'}, 'reach': {'R': [-0.5, 2.35, 0.2, 1, 0.1]}, 'bend': {'spine': [-0.15, 0, 0, 1, None]}}, toonDur=0.0),   # the hand up behind him: the wind-up
            k(SL9 - 0.05, toon={'hands': {'R': 'open'}, 'reach': {'R': [FORE9[0] - 0.02, FORE9[1], FORE9[2] + 0.03, 1, 0.1]}, 'bend': {'spine': [0.2, 0, 0, 1, None]}}, toonDur=0.05, toonEase='in'),
            k(SL9 + 0.14, toon={'hands': {'R': 'thumbUp'}, 'reach': {'R': [-0.05, 1.95, 0.05, 1, 0.1]}}, toonDur=0.14, toonEase='outBack'), k(SL9 + 0.2, look=None)])],   # and a thumb at him, for us
        props=[P('plate', 'fusePlate', pos=[-0.5, 2.35, 0.24], ry=RH, opts={'w': 0.3}, keys=[k(SL9 - 0.05, to=[FORE9[0], FORE9[1], FORE9[2] + 0.01], dur=0.05, ease='in'), k(SL9, attach='mec', joint='head', offset=[0.0, 0.4, 0.094], rot=[0, 0, 0.06]), k(SL9, squash=[1.3, 0.72, 1.0], dur=0.3)])],
        fx=[{'type': 'shake', 'at': SL9, 'dur': 0.14, 'amount': 0.02}],
        cams=[cam(0.0, [0.05, 1.98, 2.4], [0.08, 1.98, 2.25], [0.05, 1.95, -0.35], [0.05, 1.95, -0.35], lens=44)])

st.cue('sfx:stretch', 'S01', B1, 0.35); st.cue('sfx:click', 'S01', K1, 0.6); st.cue('sfx:slideDown', 'S01', K1 + 0.03, 0.3)
st.cue('sfx:stepSoft', 'S02', 0.08, 0.3); st.cue('sfx:stepSoft', 'S02', 0.3, 0.3); st.cue('sfx:bonk', 'S02', G2, 0.6); st.cue('sfx:squeak', 'S02', G2 + 0.16, 0.35)
st.cue('sfx:slideDown', 'S03', 0.15, 0.4); st.cue('pop', 'S03', 0.15 + 0.45 + 0.22, 0.5)
st.cue('sfx:click', 'S04', K4, 0.6); st.cue('sfx:zip', 'S04', K4 + 0.1, 0.3)
st.cue('sfx:slideUp', 'S05', 0.1, 0.4); st.cue('sfx:click', 'S05', 0.68, 0.45); st.cue('sfx:click', 'S05', 0.86, 0.45)
st.cue('sfx:stepRun', 'S06', 0.0, 0.4); st.cue('sfx:brake', 'S06', 0.3, 0.3)
st.cue('sfx:clink', 'S07', CL7, 0.5); st.cue('sfx:static', 'S07', ND7, 0.45); st.cue('sfx:boing', 'S07', ND7 + 0.06, 0.3); st.cue('sfx:poof', 'S07', ND7 + 0.28, 0.3)
st.cue('sfx:twang', 'S08', P8a - 0.05, 0.4); st.cue('sfx:click', 'S08', P8a, 0.6); st.cue('sfx:twang', 'S08', P8b - 0.05, 0.4); st.cue('sfx:click', 'S08', P8b, 0.6)
st.cue('whoosh', 'S09', SL9 - 0.08, 0.3, 0.1, 700, 2600); st.cue('clack', 'S09', SL9, 0.6); st.cue('sfx:boing', 'S09', SL9 + 0.1, 0.3)

CITIZEN = lambda preset, seed, **kw: {'preset': preset, 'seed': seed, 'build': {'width': 0.86, 'headWidth': 1.3, **kw.pop('build', {})}, **kw}
st.write("L'interrupteur", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, extra_cast={
    'maire': {'preset': 'politique', 'sash': ['#2A4B9B', '#F4F1E8', '#C8202A'], 'sashW': 0.12, 'hair': 'combover', 'hairColor': '#B8B4AA', 'facial': 'mustache', 'beardColor': '#B8B4AA', 'glasses': False, 'seed': 13, 'skin': '#E6BE98', 'build': {'width': 0.96, 'headWidth': 1.3}},
    'elec': CITIZEN('worker', 83, glasses=False, suit='#3A6EA5', facial='mustache')})
