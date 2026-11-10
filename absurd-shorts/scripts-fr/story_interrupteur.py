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
        dark=[[K1 + 0.02, 1]], darkFloor=0.035, darkEyes=1.5,
        cams=[C1(), glide([cam(K1 + 0.05, [-0.15, 2.06, 3.0], [-0.15, 2.06, 2.95], [-0.2, 2.04, 1.3], [-0.2, 2.04, 1.3], lens=44)], 0.22)])   # in the black the camera goes to his eyes

# 2: on his way out, in the black: two eyes come toward us, bobbing with his steps; he walks into the glass door: flat on it, the eyes two spirals, stars
G2 = 0.5                                            # he meets the glass
ST2 = {'clear': [-30, 30], 'eiffel': False, 'night': True}
st.shot('S02', 'parisStreet', setOpts=ST2, lighting='night', actors=[act('mec', [8.6, 0, -4.6], 0, 'walk', 'neutral', keys=[k(0.0, look=None), k(0.0, to=[8.6, 0, -1.25], dur=G2, clip='walk', ease='linear'),
            k(G2, clip='pressGlass', expr='dizzy', blend=0.02), k(G2, toon={'sq': [1.5, 1.0, 0.22], 'scl': {'head': [1.25, 0.9, 1]}, 'face': {'stars': 1}}, toonDur=0.03),   # flat on the glass
            k(G2 + 0.1, to=[8.6, -0.7, -1.25], dur=round(st.dur('S02') - G2 - 0.1, 3), ease='linear', face='keep')])],   # and he slides down it
        dark=[[0, 1, 0.001]], darkFloor=0.035, darkEyes=1.5,
        fx=[{'type': 'shake', 'at': G2, 'dur': 0.16, 'amount': 0.03}],
        cams=[cam(0.0, [8.6, 2.0, 0.25], [8.6, 2.0, 0.2], [8.6, 2.0, -6.0], [8.6, 2.0, -6.0], lens=44)])

# 3: the whole city: Paris at night from a height; the black runs out from his street, row after row; the tower stands alone, lit, then pops; eyes open
#    in the dark windows
CITY = lambda keys, **kw: P('city', 'cityNight', pos=[0, 0, 0], inDark=True, opts={'keys': keys, **kw})   # inDark: drawn with its own colours in every shot (the shots give a `dark` key even when the light stays on)
LIT = [[0, 0, 0.001]]                                 # a shot that stays lit but draws what is `inDark` the same way as the dark shots
VIEW = lambda t, a, b: cam(t, a, b, [4.0, 1.5, -60.0], [4.0, 1.5, -60.0], lens=44)
st.shot('S03', 'spaceDark', setOpts={'stars': 300}, lighting='night',
        props=[CITY([[0.15, 0, 0.45]], towerLag=0.22, eyesLag=0.22, eyes=46)], dark=LIT,
        cams=[VIEW(0.0, [0.0, 2.3, 4.0], [0.0, 2.1, 1.5])])

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
        props=[CITY([[0.1, 1, 0.35], [0.68, 0, 0.1], [0.86, 1, 0.1]], lit=0, towerLag=0.0, sparkle=[0.45, 0.68], eyes=0)], dark=LIT,
        cams=[VIEW(0.0, [0.0, 2.1, 1.5], [0.0, 2.3, 3.4])])

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
        cams=[cam(0.0, [0.0, 1.8, 3.25], [0.0, 1.8, 3.1], [0.0, 1.78, -0.35], [0.0, 1.78, -0.35], lens=44)])   # room over the heads: the take sends the electrician's head and helmet up

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
        dark=[[P8a + 0.02, 1], [P8b + 0.02, 0]], darkFloor=0.035, darkEyes=1.6,
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
        props=[P('plate', 'fusePlate', pos=[-1.1, 2.7, 0.3], ry=RH, opts={'w': 0.3}, keys=[k(SL9 - 0.05, to=[FORE9[0], FORE9[1], FORE9[2] + 0.01], dur=0.05, ease='in'), k(SL9, attach='mec', joint='head', offset=[0.0, 0.4, 0.094], rot=[0, 0, 0.06]), k(SL9, squash=[1.3, 0.72, 1.0], dur=0.3)])],
        fx=[{'type': 'shake', 'at': SL9, 'dur': 0.14, 'amount': 0.02}],
        cams=[cam(0.0, [0.05, 1.98, 2.4], [0.08, 1.98, 2.25], [0.05, 1.95, -0.35], [0.05, 1.95, -0.35], lens=44)])

# ---- every evening at ten: his balcony above Paris
B10 = [0.2, 0, -0.15]                                # where he stands on the balcony, facing us, the city behind him
NIGHT = {'stars': 300}
BALC = lambda: P('balc', 'balcony', pos=[0, 0, 0], opts={'w': 3.4, 'd': 1.3})
CAPN = lambda: P('cap', 'nightCap', pos=[0, 0, 0], on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.5, 0.0]})
CITY10 = lambda keys, **kw: P('city', 'cityNight', pos=[0, 0, -0.7], inDark=True, opts={'keys': keys, 'towerX': 6.0, 'eyes': 0, **kw})
CLOCK = lambda at_=None: P('clock', 'ledClock', pos=[-7.0, 4.2, -29.6], opts={'w': 5.6, 'from': '21:59', 'to': '22:00', 'at': at_} if at_ is not None else {'w': 5.6, 'from': '22:00'})   # on a front across the street, left of his head in both shots

# 10: 21:59 on the big clock across the street; it turns to 22:00: he yawns, arms up as far as they go
F10 = 0.3                                           # the clock turns
YAWN = lambda kk, **kw: {'bend': {'armL': [0, 0, 0, 1 + 0.5 * kk, None], 'foreL': [0, 0, 0, 1 + 0.5 * kk, None], 'armR': [0, 0, 0, 1 + 0.5 * kk, None], 'foreR': [0, 0, 0, 1 + 0.5 * kk, None], 'spine': [-0.12 * kk, 0, 0, 1 + 0.12 * kk, None]},
                         'sq': [1 - 0.05 * kk, 1 + 0.1 * kk, 1 - 0.05 * kk], 'face': {'jaw': 0.55 * kk, 'mouth': 'yawn', 'lid': kk, 'brow': 0.6 * kk}, **kw}
st.shot('S10', 'spaceDark', setOpts=NIGHT, lighting='night', actors=[act('mec', B10, 4, 'stand', 'sleepy', keys=[k(0.0, look=None), k(0.06, toon={'face': {'gx': -0.9, 'gy': -0.5}}, toonDur=0.08),   # his eyes on the clock
            k(F10 + 0.08, clip='yawnStretch', blend=0.22), k(F10 + 0.08, toon=YAWN(0.3), toonDur=0.1), k(F10 + 0.3, toon=YAWN(1.0, wave={**RIP('L', 0.05, 0.4, 1), **RIP('R', 0.05, 0.9, 1)}), toonDur=0.22, toonEase='out'),
            k(F10 + 0.55, toon=YAWN(1.0, wave={**RIP('L', 0.04, 1.2, 1), **RIP('R', 0.04, 1.7, 1)}), toonDur=0.25), k(F10 + 0.72, clip='stand', blend=0.14), k(F10 + 0.72, toon={'sq': [1.04, 0.95, 1.04]}, toonDur=0.12, toonEase='outBack')])],
        props=[BALC(), CAPN(), CITY10([], sparkle=[F10, 99]), CLOCK(F10)], dark=LIT,
        cams=[cam(0.0, [0.3, 1.9, 2.9], [0.3, 1.9, 2.75], [0.0, 1.85, -0.3], [0.0, 1.85, -0.3], lens=44)])

# 11: he takes the end of his own tie and pulls: click; the black runs out over Paris behind him; the tower stands alone, then pops; his eyes shut
P11 = 0.6
TIE11 = lambda L: tie_tip(B10, 4, L, 0.15)
SELF = lambda L, **kw: {'hands': {'R': 'grip'}, 'reach': {'R': [*TIE11(L), 1, 0.05, [-0.7, -0.4, 0.4]]}, 'tie': [L, 0.15, 0], **kw}
st.shot('S11', 'spaceDark', setOpts=NIGHT, lighting='night', actors=[act('mec', B10, 4, 'stand', 'sleepy', keys=[k(0.0, look=None), k(0.12, toon=SELF(1.0), toonDur=0.16, toonEase='out'),   # the hand finds the tie without a look
            k(P11 - 0.06, toon=SELF(1.7, bend={'spine': [0.25, 0, 0, 1, None], 'neck': [0.25, 0, 0, 0.8, None]}, sq=[1.05, 0.93, 1.05]), toonDur=0.06, toonEase='in'),
            k(P11 + 0.07, toon=SELF(0.85, bend={'neck': [-0.1, 0, 0, 1.25, None]}, sq=[0.96, 1.07, 0.96]), toonDur=0.07, toonEase='out'), k(P11 + 0.17, toon=SELF(1.05), toonDur=0.1), k(P11 + 0.26, toon=SELF(1.0), toonDur=0.08),
            k(P11 + 0.4, toon={'face': {'gx': 0.8}}, toonDur=0.1), k(P11 + 0.62, expr='happy'), k(P11 + 0.62, toon={}, toonDur=0.1),   # in the black: a look over his shoulder; content
            k(P11 + 0.88, toon={'face': {'lid': 1}}, toonDur=0.1)])],   # the tower has gone out: good night
        props=[BALC(), CAPN(), CITY10([[P11 + 0.02, 0, 0.5]], towerLag=0.26, sparkle=[0, 99]), CLOCK()],
        dark=[[P11 + 0.02, 1]], darkFloor=0.03, darkEyes=1.6,
        cams=[cam(0.0, [0.55, 1.9, 3.8], [0.55, 1.9, 3.6], [0.15, 1.72, -0.3], [0.15, 1.72, -0.3], lens=44)])   # him from the knees up, the tower over his shoulder: his eyes must read once it is dark

# ---- in the dark street
FAC = {'clear': [-30, 30], 'eiffel': False}          # the pavement in front of a shop front: the camera looks at the wall, no sky in the frame
CAMB = [6.3, 1.6, -0.5]
MASK = lambda a: P('bandeau_' + a, 'bandMask', pos=[0, 0, 0], on={'actor': a, 'joint': 'head', 'offset': [0.0, 0.25, 0.092]})
# 12: the burglars: two pairs of eyes sidle across the black; a match, struck between their heads: two men in black and masks, one hugging an old
#     television, caught; they grin at us, a thumb up, a wink; the match is blown out: two grins stay
M12, O12 = 0.55, 1.2                                # the match takes; it is blown out
DZ12 = 1.1                                          # how far they sidle before the match
B1b, B2b = [8.95, 0, -0.05], [9.15, 0, -0.9]         # where they stand in the light: the small one on our right with the match, the tall one hugging the set
back = lambda p_: [p_[0], p_[1], round(p_[2] - DZ12, 3)]
MATCH12 = [8.72, 1.92, -0.47]                       # the match: between their heads
LIT12 = lambda **kw: {'hands': {'R': 'pinch'}, 'reach': {'R': [*MATCH12, 1, 0.06, [0.2, -1, 0.3]]}, **kw}
st.shot('S12', 'parisStreet', setOpts=FAC, lighting='night', actors=[
        act('b1', back(B1b), -72, 'tiptoe', 'sneaky', keys=[k(0.0, look=None), k(0.0, to=B1b, dur=M12 - 0.08, clip='tiptoe', ease='linear', face=-72),
            k(M12 - 0.08, clip='stand', blend=0.05), k(M12 - 0.08, toon=LIT12(), toonDur=0.08, toonEase='out'),   # the match, struck between them
            k(M12 + 0.02, look=CAMB, expr='takeSmall'), k(M12 + 0.02, toon=LIT12(sq=[0.94, 1.08, 0.94], face={'eye': 0.3}), toonDur=0.05),   # caught
            k(M12 + 0.22, expr='happy'), k(M12 + 0.22, toon={'hands': {'R': 'pinch', 'L': 'thumbUp'}, 'reach': {'R': [*MATCH12, 1, 0.06, [0.2, -1, 0.3]], 'L': [8.62, 1.45, 0.2, 1, 0.08]}, 'face': {'mouth': 'teeth', 'mouthW': 0.3, 'browL': 0.6}}, toonDur=0.1, toonEase='outBack'),   # a grin, a thumb up
            k(O12 - 0.12, toon={'hands': {'R': 'pinch', 'L': 'thumbUp'}, 'reach': {'R': [MATCH12[0], MATCH12[1] - 0.03, MATCH12[2] + 0.22, 1, 0.06, [0.2, -1, 0.3]], 'L': [8.62, 1.45, 0.2, 1, 0.08]}, 'face': {'puff': 1, 'mouth': 'o'}}, toonDur=0.1),   # to his mouth: he blows
            k(O12 + 0.04, toon={'face': {'mouth': 'teeth', 'mouthW': 0.3}}, toonDur=0.06)]),   # the grin stays in the black
        act('b2', back(B2b), -104, 'carry', 'sneaky', keys=[k(0.0, look=None), k(0.0, to=B2b, dur=M12 - 0.08, clip='carryBox', ease='linear', face=-104), k(M12 - 0.08, clip='carry', blend=0.05),
            k(M12 + 0.05, look=CAMB, expr='takeSmall'), k(M12 + 0.05, toon={'sq': [0.95, 1.07, 0.95], 'bend': {'neck': [0, 0, 0, 1.3, None]}, 'face': {'eye': 0.3}}, toonDur=0.05),
            k(M12 + 0.28, expr='happy'), k(M12 + 0.28, toon={'face': {'mouth': 'teeth', 'mouthW': 0.3, 'lidR': 1}}, toonDur=0.1, toonEase='outBack')])],   # a grin and a wink
        props=[MASK('b1'), MASK('b2'), P('tv', 'tv', pos=[0, 0, 0], scale=0.62, on={'actor': 'b2', 'joint': 'torso', 'offset': [0.0, -0.22, 0.4]}),
               P('match', 'matchStick', pos=[0, 0, 0], inDark=True, on={'actor': 'b1', 'hand': 'R', 'offset': [0.0, -0.1, 0.02], 'rot': [3.1416, 0, 0]}, opts={'litAt': M12, 'outAt': O12}, keys=[k(0.0, visible=False), k(M12 - 0.06, visible=True), k(O12 + 0.02, visible=False)])],
        dark=[[0, 1, 0.001], [M12, 0.3, 0.06], [O12, 1, 0.04]], darkFloor=0.035, darkEyes=1.6,
        cams=[cam(0.0, [5.5, 1.62, -0.45], [5.6, 1.62, -0.45], [9.0, 1.55, -0.45], [9.0, 1.55, -0.45], lens=44)])

# 13: the lovers: two pairs of eyes on a bench turn to each other, turn to hearts, come together; a heart; a third pair opens between them, looks left,
#     looks right, and goes down slowly
LA, LB, TH13 = [9.2, 0, -0.3], [9.2, 0, 0.3], [9.75, 0, 0.0]
KISS = 0.6
LEAN = lambda sd, kk, **kw: {'bend': {'spine': [0, 0, sd * 0.2 * kk, 1, None], 'neck': [0, 0, sd * 0.22 * kk, 1 + 0.35 * kk, None]}, **kw}
st.shot('S13', 'parisStreet', setOpts=FAC, lighting='night', actors=[
        act('la', LA, -68, 'sit', 'happy', keys=[k(0.0, look='lb'), k(0.18, expr='love'), k(0.26, toon=LEAN(-1, 1.0), toonDur=0.3, toonEase='inOut')]),
        act('lb', LB, -112, 'sit', 'happy', keys=[k(0.0, look='la'), k(0.22, expr='love'), k(0.26, toon=LEAN(1, 1.0), toonDur=0.3, toonEase='inOut')]),
        act('b1', TH13, -90, 'stand', 'scared', keys=[k(0.0, look=None), k(0.0, toon={'face': {'lid': 1}}, toonDur=0.0), k(KISS + 0.12, toon={'face': {'eye': 0.5}, 'sq': [0.96, 1.05, 0.96]}, toonDur=0.05, toonEase='outBack'),   # the third pair opens, between them
            k(KISS + 0.24, toon={'face': {'eye': 0.5, 'gx': -1}}, toonDur=0.06), k(KISS + 0.34, toon={'face': {'eye': 0.5, 'gx': 1}}, toonDur=0.07), k(KISS + 0.42, toon={'face': {'eye': 0.5}}, toonDur=0.05),
            k(KISS + 0.42, to=[TH13[0], -0.9, TH13[2]], dur=0.26, ease='in', face='keep')])],   # and goes down
        props=[P('bench', 'bench', pos=[9.35, 0, 0.0], ry=-90, opts={'w': 1.5}), P('pop', 'heartPop', pos=[9.05, 2.02, 0.0], ry=-90, inDark=True, opts={'at': KISS, 'size': 0.1})],
        dark=[[0, 1, 0.001]], darkFloor=0.035, darkEyes=1.9,
        cams=[cam(0.0, [7.2, 1.62, 0.0], [7.3, 1.64, 0.0], [9.2, 1.72, 0.0], [9.2, 1.72, 0.0], lens=44)])

# ---- the bill: by day, at his door (the right-hand pavement of the Paris street; his door is in the front at x = 9.93)
DAY = {'clear': [-30, 30], 'eiffel': False}
H14, RY14 = [9.05, 0, -0.35], -72                    # him, in front of his door, facing the road
HOME = lambda **kw: P('home', 'door', pos=[9.93, 0, -0.35], ry=-90, opts={'w': 1.0, 'h': 2.3, 'color': '#2F6E5C', 'frame': '#EDE6D4', **kw})
ENV = lambda pos, sc=1.0, keys=None, **kw: P('env', 'bigEnvelope', pos=pos, ry=-90, rotOrder='YXZ', scale=sc, opts={'w': 0.34, 'title': 'ÉLECTRICITÉ', 'to': 'CE MEC', 'line2': 'CHEZ LUI', **kw}, keys=keys or [])
E14a, E14b, E14c = [8.82, 1.4, -1.9], [8.82, 1.42, -0.88], [8.8, 1.72, -0.4]   # the envelope: held out by the postman as he comes, at the end of his arm, then in front of the hero's chin
GIVE = lambda p_, **kw: {'hands': {'R': 'pinch'}, 'reach': {'R': [p_[0] + 0.03, p_[1] - 0.06, p_[2] - 0.12, 1, 0.05]}, **kw}
BOTH = lambda p_, w=0.34, **kw: {'hands': {'L': 'pinch', 'R': 'pinch'}, 'reach': {'L': [p_[0] + 0.03, p_[1] - 0.04, p_[2] + w * 0.46, 1, 0.05], 'R': [p_[0] + 0.03, p_[1] - 0.04, p_[2] - w * 0.46, 1, 0.05]}, **kw}

# 14: the bill comes in his name: the postman walks up, the envelope held out at arm's length; he takes it in both hands, up under his nose; close: ÉLECTRICITÉ,
#     CE MEC; his eyes over its edge go down to it, then come up to us, one brow up
G14, CU14 = 0.5, 0.78
st.shot('S14', 'parisStreet', setOpts=DAY, actors=[act('mec', H14, RY14, 'stand', 'neutral', keys=[k(0.0, look='fact'), k(G14 - 0.1, toon=BOTH(E14b), toonDur=0.1, toonEase='out'), k(G14, toon=BOTH(E14c), toonDur=0.14, toonEase='outBack'), k(G14 + 0.1, look=None),
            k(CU14 + 0.05, toon=BOTH(E14c, face={'gy': 0.9, 'gx': 0.2}), toonDur=0.08), k(CU14 + 0.45, toon=BOTH(E14c, face={'browL': 0.9, 'browR': -0.4, 'eye': 0.15}), toonDur=0.08, toonEase='outBack')]),   # he reads; then to us
        act('fact', [8.95, 0, -3.2], 0, 'walk', 'happy', keys=[k(-0.05, toon=GIVE(E14a), toonDur=0.0), k(0.0, to=[8.95, 0, -1.5], dur=G14 - 0.1, clip='walk', ease='out', face=-30), k(0.0, toon=GIVE(E14b), toonDur=G14 - 0.1, toonEase='out'),
            k(G14 - 0.1, clip='stand', blend=0.1, look='mec'), k(G14 + 0.06, toon={'hands': {'R': 'open'}, 'reach': {'R': [8.8, 1.3, -1.2, 0.6, 0.05]}}, toonDur=0.12), k(G14 + 0.24, clip='salute', blend=0.12)])],   # he lets go, and salutes
        props=[HOME(), ENV(E14a, keys=[k(0.0, to=E14b, dur=G14 - 0.1, ease='out'), k(G14, to=E14c, dur=0.14, ease='outBack')])],
        cams=[cam(0.0, [4.7, 1.7, -0.92], [4.85, 1.7, -0.92], [9.0, 1.6, -0.92], [9.0, 1.6, -0.92], lens=44),
              cam(CU14, [7.45, 1.9, -0.4], [7.5, 1.9, -0.4], [8.85, 1.88, -0.4], [8.85, 1.88, -0.4], lens=44)])   # close: the envelope under his eyes

# 15: the whole bill: the envelope grows at each word; he holds it over his head, his knees give; it comes down flat on him. Seen from above: the envelope
#     on the pavement, and in its window, where his name was, two eyes
W15 = [0.04, 0.22, 0.37]                             # « Toute », « la », « facture »
SC15, Y15 = [2.2, 4.4, 7.5], [1.95, 2.55, 3.3]        # its size and the height of its middle after each word (its lower edge stays in his hands)
F15, L15 = 0.6, 0.72                                 # it tips; it lands
UP15 = lambda i, **kw: BOTH([E14c[0], Y15[i] - 0.105 * SC15[i], E14c[2]], 0.34 * min(SC15[i], 2.4), **kw)
PRESS15 = lambda i: {'sq': [1 + 0.07 * (i + 1), 1 - 0.1 * (i + 1), 1 + 0.07 * (i + 1)], 'face': {'gy': -1, 'eye': 0.15 * (i + 1), 'sweat': 1 if i else 0, 'mouth': 'wavy' if i else 'o'}}
st.shot('S15', 'parisStreet', setOpts=DAY, actors=[act('mec', H14, RY14, 'stand', 'surprised', keys=[k(-0.05, toon=BOTH(E14c), toonDur=0.0), k(0.0, look=None)] +
            [x for i in range(3) for x in (k(W15[i], toon=UP15(i, **PRESS15(i)), toonDur=0.07, toonEase='outBack'),)] +
            [k(F15, toon=UP15(2, sq=[1.3, 0.6, 1.3], face={'gy': -1, 'eye': 0.5, 'mouth': 'scream', 'jaw': 0.6}), toonDur=0.1), k(L15 - 0.03, clip='pancake', params={'flat': 0.05}, blend=0.03), k(L15 - 0.03, toon={}, toonDur=0.03)])],
        props=[HOME(), ENV(E14c, eyes=[L15 + 0.22, 99], keys=[x for i in range(3) for x in (k(W15[i], to=[E14c[0], Y15[i], E14c[2]], dur=0.07, ease='outBack'), k(W15[i], scale=SC15[i], dur=0.07, ease='outBack'), k(W15[i] + 0.07, squash=[1.12, 0.9, 1.0], dur=0.14))] +
                   [k(F15, to=[8.75, 0.16, E14c[2]], dur=round(L15 - F15, 3), ease='in'), k(F15, rotTo=[-1.5708, -1.5708, 0], dur=round(L15 - F15, 3), ease='in'), k(L15, squash=[1.06, 1.0, 1.06], dur=0.3)])],
        fx=[{'type': 'shake', 'at': L15, 'dur': 0.2, 'amount': 0.035}],
        cams=[cam(0.0, [5.6, 1.8, -0.4], [5.55, 1.8, -0.4], [9.0, 1.8, -0.4], [9.0, 1.8, -0.4], lens=44),
              glide([cam(W15[0], [3.6, 2.35, -0.4], [3.5, 2.35, -0.4], [9.0, 2.35, -0.4], [9.0, 2.35, -0.4], lens=44)], round(W15[2] - W15[0] + 0.07, 3)),   # it backs off as the envelope grows: the whole of it stays in the frame
              glide([cam(F15 - 0.02, [6.3, 4.6, -0.4], [6.35, 4.55, -0.4], [8.6, 0.2, -0.4], [8.6, 0.2, -0.4], lens=44)], round(L15 - F15 + 0.06, 3))])   # the camera goes up as it comes down: the envelope from above

# ---- the town hall
MAI = {'map': False, 'plate': False, 'deskX': -2.7, 'flagX': 3.6, 'clockX': 9}
MA16, H16 = [-0.72, 0, -0.5], [0.5, 0, -0.1]
# 16: he asked for a raise: he comes in flat as a sheet, edge-on: a line that sways; he turns to us: flat; a thumb in his mouth, he blows: he pops back to
#     his size; then a palm held out to the mayor
T16, B16, P16 = 0.42, 0.62, 0.8                      # he turns to us; he blows; the pop
st.shot('S16', 'mairie', setOpts=MAI, actors=[act('mec', [2.6, 0, -0.1], 90, 'paperThin', 'unimpressed', keys=[k(0.0, look=None), k(0.0, clip='paperThin', params={'popAt': P16, 'thin': 0.04}, blend=0.0),
            k(0.0, to=H16, dur=T16 - 0.04, glide=True, ease='out', face=88), k(T16, to=H16, dur=0.14, glide=True, ease='inOut', face=-14),   # in on a draught, edge-on; then he turns
            k(B16 - 0.06, toon={'hands': {'R': 'thumbUp'}, 'touch': {'R': ['face', 0.0, 0.23, 0.03, 1, 0.08]}}, toonDur=0.08), k(B16 + 0.04, toon={'hands': {'R': 'thumbUp'}, 'touch': {'R': ['face', 0.0, 0.23, 0.03, 1, 0.08]}, 'face': {'puff': 1, 'mouth': 'o', 'brow': -0.4}}, toonDur=0.08),   # the thumb in his mouth: he blows
            k(P16 + 0.06, toon={'sq': [0.9, 1.12, 1.0]}, toonDur=0.06, toonEase='outBack'), k(P16 + 0.2, clip='stand', blend=0.12, expr='smug'),
            k(P16 + 0.2, toon={'hands': {'L': 'open'}, 'reach': {'L': [-0.05, 1.32, 0.22, 1, 0.1]}, 'face': {'browL': 0.8, 'browR': 0.8, 'mouth': 'smile'}}, toonDur=0.14, toonEase='outBack'), k(P16 + 0.2, look='maire')]),   # the palm out: a raise
        act('maire', MA16, 26, 'stand', 'neutral', keys=[k(0.0, look='mec'), k(T16 + 0.1, toon={'face': {'browL': 0.9, 'browR': -0.3}}, toonDur=0.1), k(P16 + 0.04, toon={'sq': [0.95, 1.06, 0.95], 'face': {'eye': 0.3, 'brow': 0.8}}, toonDur=0.06, toonEase='outBack'),
            k(P16 + 0.3, toon={'face': {'browTilt': -14, 'mouth': 'frown'}}, toonDur=0.12), k(P16 + 0.3, clip='thinkChin', blend=0.2)])],
        cams=[cam(0.0, [0.1, 1.62, 4.0], [0.05, 1.62, 3.85], [-0.1, 1.55, -0.3], [-0.1, 1.55, -0.3], lens=44)])

# 17: he got a night bonus: the mayor brings a candle out from behind his back and puts it in his hand; then he takes the end of his tie, and pulls: the
#     night. A flame, his eyes over it; the mayor's eyes and his teeth
G17, P17 = 0.44, 0.76
H17 = [0.42, 0, -0.1]
C17a, C17b, C17c = [-0.98, 1.0, -0.72], [-0.3, 1.42, 0.1], [0.1, 1.3, 0.22]   # the candle: behind the mayor's back, presented, in the hero's hand
CAND = lambda p_, **kw: {'hands': {'R': 'grip'}, 'reach': {'R': [p_[0] + 0.1, p_[1] + 0.02, p_[2], 1, 0.05]}, **kw}   # the mayor's right hand on the ring of the holder
TAKE17 = lambda w=1, **kw: {'hands': {'L': 'grip'}, 'reach': {'L': [C17c[0] + 0.1, C17c[1] + 0.02, C17c[2], w, 0.05]}, **kw}
TIE17 = lambda L: tie_tip(H17, -14, L, 0.2)
st.shot('S17', 'mairie', setOpts=MAI, actors=[act('mec', H17, -14, 'stand', 'smug', keys=[k(0.0, look='maire'), k(0.0, toon={'hands': {'L': 'open'}, 'reach': {'L': [-0.05, 1.32, 0.22, 1, 0.1]}}, toonDur=0.0),
            k(G17 - 0.06, toon=TAKE17(), toonDur=0.1), k(G17 + 0.1, expr='unimpressed', look=None), k(G17 + 0.12, toon=TAKE17(face={'gy': 0.8}), toonDur=0.08),   # he has it; he looks at it
            k(P17 - 0.06, toon=TAKE17(tie=[1.7, 0.2, 0], bend={'spine': [0.25, 0, 0, 1, None], 'neck': [0.25, 0, 0, 0.8, None]}, sq=[1.05, 0.93, 1.05]), toonDur=0.06, toonEase='in'),
            k(P17 + 0.07, toon=TAKE17(tie=[0.85, 0.2, 0], bend={'neck': [-0.1, 0, 0, 1.25, None]}, sq=[0.96, 1.07, 0.96]), toonDur=0.07, toonEase='out'), k(P17 + 0.17, toon=TAKE17(tie=[1.05, 0.2, 0]), toonDur=0.1),
            k(P17 + 0.26, toon=TAKE17(), toonDur=0.08), k(P17 + 0.4, toon=TAKE17(face={'gy': 0.9}), toonDur=0.1), k(P17 + 0.62, toon=TAKE17(), toonDur=0.1)]),   # in the black: down to the flame, up to us
        act('maire', MA16, 26, 'stand', 'happy', keys=[k(0.0, look='mec'), k(0.0, toon=CAND(C17a), toonDur=0.0), k(0.1, toon=CAND(C17b, sq=[0.97, 1.05, 0.97]), toonDur=0.16, toonEase='outBack'),   # from behind his back: there
            k(G17 - 0.08, toon=CAND(C17c), toonDur=0.1), k(G17 + 0.08, toon={'hands': {'R': 'grip'}, 'reach': {'R': [*TIE17(1.0), 1, 0.05, [0.6, -0.6, 0.5]]}}, toonDur=0.2, toonEase='out'),   # into his hand; then the tie
            k(P17 - 0.06, toon={'hands': {'R': 'grip'}, 'reach': {'R': [*TIE17(1.7), 1, 0.05, [0.6, -0.6, 0.5]]}, 'bend': {'spine': [0.12, 0, 0, 1, None]}}, toonDur=0.06, toonEase='in'),
            k(P17 + 0.07, toon={'hands': {'R': 'grip'}, 'reach': {'R': [*TIE17(0.9), 1, 0.05, [0.6, -0.6, 0.5]]}, 'face': {'mouth': 'teeth', 'mouthW': 0.3}}, toonDur=0.07), k(P17 + 0.3, toon={'face': {'mouth': 'teeth', 'mouthW': 0.3}}, toonDur=0.2), k(P17 + 0.1, look=None)])],
        props=[P('candle', 'candle', pos=C17a, inDark=True, keys=[k(0.1, to=C17b, dur=0.16, ease='outBack'), k(G17 - 0.08, to=C17c, dur=0.1, ease='inOut')])],
        dark=[[0, 0, 0.001], [P17 + 0.02, 1]], darkFloor=0.035, darkEyes=1.6,
        cams=[cam(0.0, [-0.05, 1.62, 3.3], [-0.05, 1.62, 3.15], [-0.1, 1.6, -0.2], [-0.1, 1.6, -0.2], lens=44)])

# ---- yesterday at noon: the pavement in front of his door, seen along the street: the sun stands over the far end of it
SUNP = [5.2, 18.8, -34.0]                            # left of the right-hand fronts: whole in the sky
SUN = lambda **kw: P('sun', 'sunLamp', pos=SUNP, inDark=True, opts={'r': 3.4, **kw})
C18 = [8.7, 0.45, 6.0]                               # low on the pavement, looking up the street
T18 = [8.6, 3.3, -4.0]
H19, DOOR19 = [9.0, 0, 0.8], [9.7, 0, 0.8]           # where he stops, in the sun; where he comes out of
DA, E1, E2 = [8.1, 0, -0.5], [9.6, 0, -1.4], [8.6, 0, -2.6]   # passers-by round him, all facing up the street toward us: the lady on our left, clear of him
CROWD = lambda keys=None: [act('dame', DA, 6, 'stand', 'happy', keys=(keys or {}).get('dame', [k(0.0, look=None)])), act('e1', E1, -8, 'stand', 'neutral', keys=(keys or {}).get('e1', [k(0.0, look=None)])),
                           act('e2', E2, 4, 'stand', 'happy', keys=(keys or {}).get('e2', [k(0.0, look=None)]))]
HOME19 = lambda **kw: P('home', 'door', pos=[9.93, 0, 0.8], ry=-90, opts={'w': 1.0, 'h': 2.3, 'color': '#2F6E5C', 'frame': '#EDE6D4', **kw})

# 18: yesterday at noon: the sun, with a face, over the end of the street; the camera comes down from it to the pavement: people, his door
st.shot('S18', 'parisStreet', setOpts=DAY, actors=CROWD(), props=[SUN(), HOME19()], dark=LIT,
        cams=[cam(0.0, C18, C18, [6.2, 14.5, -30.0], T18, lens=44, ease='inOut')])

# 19: he stepped out of his house: the door opens, he comes out into the sun, stops, hands on his hips, one eye shut against the light, a big breath
O19 = 0.3
st.shot('S19', 'parisStreet', setOpts=DAY, actors=[act('mec', DOOR19, -90, 'walk', 'happy', keys=[k(0.0, look=None), k(0.02, to=H19, dur=O19, clip='walk', ease='out', face=2),
            k(O19 + 0.04, clip='handsOnHips', blend=0.14), k(O19 + 0.1, toon={'bend': {'spine': [-0.14, 0, 0, 1.08, None]}, 'sq': [0.97, 1.05, 0.97], 'face': {'lidR': 1, 'lowL': 0.3, 'browR': -0.5, 'browL': 0.5, 'mouth': 'bigsmile', 'cheeks': 1, 'gy': -0.5}}, toonDur=0.16, toonEase='outBack'),   # the sun in his face
            k(O19 + 0.5, toon={'bend': {'spine': [0, 0, 0, 1, None]}, 'face': {'lidR': 1, 'lowL': 0.3, 'browR': -0.5, 'browL': 0.5, 'mouth': 'smile', 'cheeks': 1}}, toonDur=0.25)])] + CROWD(),   # he breathes out
        props=[SUN(), HOME19(openAt=0.0)], dark=LIT,
        cams=[cam(0.0, [8.45, 1.7, 4.3], [8.5, 1.7, 4.1], [9.0, 1.72, 0.8], [9.0, 1.72, 0.8], lens=44)])

# 20: by reflex: he looks up at the birds, whistling; his right hand walks up his chest to the tie, finger by finger, and closes on it; behind him the lady
#     sees it: her eyes come out, her arm shoots out across the frame to stop him; everything holds
STEP20 = [0.08, 0.2, 0.32]                           # his hand climbs
GR20, NO20 = 0.44, 0.5                               # it closes on the tie; the lady's arm
TT20 = tie_tip(H19, 2, 1.0, 0.15)
CLIMB = lambda i: {'hands': {'R': 'two'}, 'reach': {'R': [TT20[0] + 0.02, round(0.98 + 0.07 * i, 3), TT20[2] + 0.04, 1, 0.08, [-0.7, -0.4, 0.4]]}, 'face': {'gx': 0.7, 'gy': -0.8, 'mouth': 'whistle', 'brow': 0.3}}
ONTIE = lambda L=1.0, **kw: {'hands': {'R': 'grip'}, 'reach': {'R': [*tie_tip(H19, 2, L, 0.15), 1, 0.05, [-0.7, -0.4, 0.4]]}, 'tie': [L, 0.15, 0], **kw}
st.shot('S20', 'parisStreet', setOpts=DAY, actors=[act('mec', H19, 2, 'stand', 'happy', keys=[k(0.0, look=None), k(0.0, toon={'face': {'gx': 0.7, 'gy': -0.8, 'mouth': 'whistle', 'brow': 0.3}}, toonDur=0.0)] +
            [k(t_, toon=CLIMB(i), toonDur=0.07, toonEase='outBack') for i, t_ in enumerate(STEP20)] +
            [k(GR20, toon=ONTIE(1.0, face={'gx': 0.7, 'gy': -0.8, 'mouth': 'whistle', 'brow': 0.3}), toonDur=0.07, toonEase='out')]),   # on the tie; he has not even looked
        act('dame', DA, 6, 'stand', 'happy', keys=[k(0.0, look='mec'), k(GR20 - 0.06, expr='take'), k(GR20 - 0.06, toon={'sq': [0.92, 1.12, 0.92], 'face': {'pop': 0.8, 'jaw': 0.8, 'popLen': 0.14}}, toonDur=0.06, toonEase='outBack'),
            k(NO20, toon={'hands': {'L': 'spread'}, 'reach': {'L': [8.78, 1.72, 0.72, 1, 0.1, [0.3, 0.6, 0.3]]}, 'wave': RIP('L', 0.1, 0.8, 1.5), 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'pop': 0.8, 'jaw': 0.9, 'popLen': 0.14}}, toonDur=0.08, toonEase='out'),   # NON: an arm across the street
            k(NO20 + 0.1, toon={'hands': {'L': 'spread'}, 'reach': {'L': [8.8, 1.72, 0.76, 1, 0.1, [0.3, 0.6, 0.3]]}, 'wave': RIP('L', 0.03, 1.6, 1.5), 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'pop': 0.8, 'jaw': 0.9, 'popLen': 0.14}}, toonDur=0.1)]),
        act('e1', E1, -8, 'stand', 'neutral', keys=[k(0.0, look=None), k(NO20, look='mec', expr='surprised')]), act('e2', E2, 4, 'stand', 'happy', keys=[k(0.0, look=None), k(NO20 + 0.04, look='mec', expr='surprised')])],
        props=[SUN(), HOME19()], dark=LIT,
        cams=[cam(0.0, [8.5, 1.6, 3.9], [8.52, 1.6, 3.7], [9.05, 1.6, 0.6], [9.05, 1.6, 0.6], lens=44)])

# 21: he turned off: the street, the sun over it, frightened; the tie: click: black; the sun goes out like a bulb, a red thread dies in it, its eyes shut
P21 = 0.24
st.shot('S21', 'parisStreet', setOpts=DAY, actors=[act('mec', H19, 2, 'stand', 'happy', keys=[k(-0.05, toon=ONTIE(1.0, face={'gx': 0.7, 'gy': -0.8, 'mouth': 'whistle'}), toonDur=0.0), k(0.0, look=None),
            k(P21 - 0.06, toon=ONTIE(1.7, bend={'spine': [0.25, 0, 0, 1, None], 'neck': [0.25, 0, 0, 0.8, None]}, sq=[1.05, 0.93, 1.05]), toonDur=0.06, toonEase='in'),
            k(P21 + 0.07, toon=ONTIE(0.85, bend={'neck': [-0.1, 0, 0, 1.25, None]}, sq=[0.96, 1.07, 0.96]), toonDur=0.07, toonEase='out'), k(P21 + 0.17, toon=ONTIE(1.05), toonDur=0.1), k(P21 + 0.26, toon=ONTIE(1.0), toonDur=0.08),
            k(P21 + 0.2, expr='surprised'), k(P21 + 0.42, toon=ONTIE(1.0, face={'gy': -1}), toonDur=0.08)]),   # in the black his eyes go up, to where the sun was
        act('dame', DA, 6, 'stand', 'take', keys=[k(0.0, look='mec'), k(-0.05, toon={'hands': {'L': 'spread'}, 'reach': {'L': [8.8, 1.72, 0.76, 1, 0.1, [0.3, 0.6, 0.3]]}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {'pop': 0.8, 'jaw': 0.9, 'popLen': 0.14}}, toonDur=0.0), k(P21 + 0.2, expr='scared'), k(P21 + 0.2, toon={}, toonDur=0.2)]),
        act('e1', E1, -8, 'stand', 'surprised', keys=[k(0.0, look='mec')]), act('e2', E2, 4, 'stand', 'surprised', keys=[k(0.0, look='mec')])],
        props=[SUN(scareAt=0.0, offAt=P21 + 0.03), HOME19()],
        dark=[[0, 0, 0.001], [P21 + 0.02, 1]], darkFloor=0.03, darkEyes=1.7,
        cams=[cam(0.0, C18, [8.7, 0.45, 5.8], T18, T18, lens=44)])

# 22: it has been night since: black; every pair of eyes in the street turns to his; his look left, look right; he tiptoes out of the picture, the others' eyes
#     go with him
L22, G22 = 0.3, 0.62
st.shot('S22', 'parisStreet', setOpts=DAY, actors=[act('mec', H19, 2, 'stand', 'surprised', keys=[k(0.0, look=None), k(L22, toon={'face': {'gx': -1}}, toonDur=0.06), k(L22 + 0.14, toon={'face': {'gx': 1}}, toonDur=0.08), k(L22 + 0.26, toon={'face': {'gy': 0.4}}, toonDur=0.06),
            k(G22, to=[7.2, 0, 1.4], dur=round(st.dur('S22') - G22, 3), clip='tiptoe', ease='in', face=-20), k(G22, expr='sneaky')]),
        act('dame', DA, 6, 'stand', 'unimpressed', keys=[k(0.0, look='mec')]), act('e1', E1, -8, 'stand', 'unimpressed', keys=[k(0.12, look='mec')]), act('e2', E2, 4, 'stand', 'unimpressed', keys=[k(0.2, look='mec')])],
        props=[P('pig', 'eyesPair', pos=[8.25, 0.22, 1.9], inDark=True, opts={'s': 0.035, 'blinks': [0.5, 0.9], 'look': [[0, 0.8], [G22, 0.8], [G22 + 0.4, -1]]})],   # a pigeon, low on the kerb, looks at him too
        dark=[[0, 1, 0.001]], darkFloor=0.03, darkEyes=1.9,
        cams=[cam(0.0, [8.7, 1.95, 3.9], [8.7, 1.95, 3.7], [8.8, 1.9, 0.0], [8.8, 1.9, 0.0], lens=44)])

# 23: the astronomers are looking: black; an eye at the eyepiece (the other shut); the telescope draws out, and out; nothing; he steps back, two eyes, takes
#     a torch and sweeps the sky with it
AS, TEL = [-0.55, 0, 0.0], [0.0, 0, 0.25]
X23, S23, B23 = [[0.12, 0], [0.3, 0.5], [0.36, 0.5], [0.52, 1.0]], 0.62, 0.86   # the draws; he steps back; the torch
TORCH = [-0.42, 1.55, 0.5]
st.shot('S23', 'spaceDark', setOpts={'stars': 0}, lighting='night', actors=[act('astro', AS, 40, 'stand', 'determined', keys=[k(0.0, look=None), k(0.0, toon={'bend': {'spine': [0.45, 0, -0.1, 1, None]}, 'face': {'lidR': 1, 'eyeL': 0.4}}, toonDur=0.0),   # bent to the eyepiece: one eye
            k(S23, toon={'sq': [0.96, 1.05, 0.96], 'face': {'eyeL': 0.5, 'eyeR': 0.1}}, toonDur=0.1, toonEase='outBack'), k(S23, expr='confused', face=10),   # nothing: he straightens, to us: one eye bigger than the other
            k(B23 - 0.1, toon={'hands': {'R': 'grip'}, 'reach': {'R': [*TORCH, 1, 0.05]}, 'face': {'gy': -0.9, 'gx': 0.4}}, toonDur=0.12, toonEase='out')])],   # the torch, up at the sky
        props=[P('tel', 'telescope', pos=TEL, ry=55, inDark=True, opts={'extend': X23, 'tilt': 48, 'len': 0.8}),
               P('beam', 'torchBeam', pos=TORCH, ry=40, inDark=True, opts={'len': 7, 'r': 0.9, 'pitch': [[0, 62]], 'sweep': [[B23, -30], [B23 + 0.2, 28], [B23 + 0.4, -22], [B23 + 0.58, 12]]}, keys=[k(0.0, visible=False), k(B23, visible=True)])],
        dark=[[0, 1, 0.001]], darkFloor=0.03, darkEyes=1.8,
        cams=[cam(0.0, [0.15, 1.9, 4.6], [0.15, 1.95, 4.4], [0.1, 2.3, 0.0], [0.1, 2.3, 0.0], lens=44)])

# 24: the bill: black; from the right an envelope as wide as a man is tall comes on, bobbing: the postman carries it over his head; the hero's eyes watch it come
H24 = [8.9, 0, 0.0]
EV24 = lambda keys, **kw: P('env', 'bigEnvelope', pos=[11.2, 2.3, 0.4], ry=0, inDark=True, scale=1.0, opts={'w': 1.25, 'title': 'ÉLECTRICITÉ', 'to': 'LE SOLEIL', 'line2': 'CHEZ CE MEC', **kw}, keys=keys)
WALK24 = [k(0.0, to=[10.55, 2.36, 0.4], dur=0.22, ease='linear'), k(0.22, to=[10.0, 2.28, 0.4], dur=0.22, ease='linear'), k(0.44, to=[9.5, 2.36, 0.4], dur=0.22, ease='linear'), k(0.66, to=[9.1, 2.3, 0.4], dur=0.22, ease='out')]
st.shot('S24', 'parisStreet', setOpts=DAY, actors=[act('mec', H24, 2, 'stand', 'surprised', keys=[k(0.0, look=None), k(0.1, toon={'face': {'gx': 0.9}}, toonDur=0.08), k(0.5, toon={'face': {'gx': 0.7, 'eye': 0.4}}, toonDur=0.1), k(0.85, toon={'face': {'eye': 0.5, 'gy': -0.3}}, toonDur=0.08)]),
        act('fact', [11.2, 0, -0.1], 0, 'holdUp', 'strain', keys=[k(0.0, look=None), k(0.0, to=[9.1, 0, -0.1], dur=0.88, clip='holdUp', ease='linear', face=0)])],
        props=[EV24(WALK24)],
        dark=[[0, 1, 0.001]], darkFloor=0.03, darkEyes=1.7,
        cams=[cam(0.0, [9.2, 2.05, 3.7], [9.15, 2.05, 3.6], [9.2, 2.1, 0.0], [9.2, 2.1, 0.0], lens=44)])

# 25: it has already arrived: the envelope stops in front of him: his eyes are gone behind it; then, in its window, where the name is: two eyes; a blink;
#     a look left, a look right; they stay
A25 = 0.3
st.shot('S25', 'parisStreet', setOpts=DAY, actors=[act('mec', H24, 2, 'stand', 'surprised', keys=[k(0.0, look=None), k(0.0, toon={'face': {'eye': 0.5, 'gy': -0.3}}, toonDur=0.0)]),
        act('fact', [9.1, 0, -0.1], 0, 'holdUp', 'strain', keys=[k(0.0, look=None), k(0.0, to=[8.9, 0, -0.35], dur=A25, clip='holdUp', ease='out', face=0), k(A25 + 0.3, expr='happy')])],
        props=[P('env', 'bigEnvelope', pos=[9.1, 2.3, 0.4], ry=0, inDark=True, opts={'w': 1.25, 'title': 'ÉLECTRICITÉ', 'to': 'LE SOLEIL', 'line2': 'CHEZ CE MEC', 'eyes': [A25 + 0.36, 99]},
                 keys=[k(0.0, to=[8.84, 2.3, 0.4], dur=A25, ease='out'), k(A25, squash=[1.06, 0.92, 1.0], dur=0.3)])],
        dark=[[0, 1, 0.001]], darkFloor=0.03, darkEyes=1.7,
        cams=[cam(0.0, [9.15, 2.05, 3.6], [8.86, 2.12, 3.3], [9.2, 2.1, 0.0], [8.86, 2.14, 0.0], lens=44, ease='out')])   # it ends on the envelope, whole in the frame

st.cue('sfx:stretch', 'S01', B1, 0.35); st.cue('sfx:click', 'S01', K1, 0.6); st.cue('sfx:slideDown', 'S01', K1 + 0.03, 0.3)
st.cue('sfx:stepSoft', 'S02', 0.08, 0.3); st.cue('sfx:stepSoft', 'S02', 0.3, 0.3); st.cue('sfx:bonk', 'S02', G2, 0.6); st.cue('sfx:squeak', 'S02', G2 + 0.16, 0.35)
st.cue('sfx:slideDown', 'S03', 0.15, 0.4); st.cue('pop', 'S03', 0.15 + 0.45 + 0.22, 0.5)
st.cue('sfx:click', 'S04', K4, 0.6); st.cue('sfx:zip', 'S04', K4 + 0.1, 0.3)
st.cue('sfx:slideUp', 'S05', 0.1, 0.4); st.cue('sfx:click', 'S05', 0.68, 0.45); st.cue('sfx:click', 'S05', 0.86, 0.45)
st.cue('sfx:stepRun', 'S06', 0.0, 0.4); st.cue('sfx:brake', 'S06', 0.3, 0.3)
st.cue('sfx:clink', 'S07', CL7, 0.5); st.cue('sfx:static', 'S07', ND7, 0.45); st.cue('sfx:boing', 'S07', ND7 + 0.06, 0.3); st.cue('sfx:poof', 'S07', ND7 + 0.28, 0.3)
st.cue('sfx:twang', 'S08', P8a - 0.05, 0.4); st.cue('sfx:click', 'S08', P8a, 0.6); st.cue('sfx:twang', 'S08', P8b - 0.05, 0.4); st.cue('sfx:click', 'S08', P8b, 0.6)
st.cue('whoosh', 'S09', SL9 - 0.08, 0.3, 0.1, 700, 2600); st.cue('clack', 'S09', SL9, 0.6); st.cue('sfx:boing', 'S09', SL9 + 0.1, 0.3)
st.cue('sfx:ding', 'S10', F10, 0.45); st.cue('sfx:stretch', 'S10', F10 + 0.1, 0.3)
st.cue('sfx:twang', 'S11', P11 - 0.05, 0.4); st.cue('sfx:click', 'S11', P11, 0.6); st.cue('sfx:slideDown', 'S11', P11 + 0.03, 0.4); st.cue('pop', 'S11', P11 + 0.02 + 0.5 + 0.26, 0.5)
st.cue('sfx:stepSoft', 'S12', 0.05, 0.25); st.cue('sfx:stepSoft', 'S12', 0.3, 0.25); st.cue('sfx:tick', 'S12', M12 - 0.04, 0.5); st.cue('sfx:gasp', 'S12', M12 + 0.03, 0.3); st.cue('sfx:ding', 'S12', M12 + 0.24, 0.3); st.cue('sfx:poof', 'S12', O12 - 0.02, 0.3)
st.cue('pop', 'S13', KISS, 0.45); st.cue('sfx:gulp', 'S13', KISS + 0.12, 0.4); st.cue('sfx:slideDownSlow', 'S13', KISS + 0.42, 0.3)
st.cue('sfx:step', 'S14', 0.05, 0.3); st.cue('sfx:step', 'S14', 0.28, 0.3); st.cue('sfx:paper', 'S14', G14, 0.45)
for i_ in range(3): st.cue('sfx:boing', 'S15', W15[i_], 0.3 + 0.08 * i_)
st.cue('whoosh', 'S15', F15, 0.35, 0.12, 300, 1500); st.cue('thud', 'S15', L15, 0.7); st.cue('sfx:paper', 'S15', L15 + 0.02, 0.5)
st.cue('sfx:paper', 'S16', 0.05, 0.35); st.cue('pop', 'S16', P16, 0.55); st.cue('sfx:boing', 'S16', P16 + 0.04, 0.3)
st.cue('sfx:twang', 'S17', P17 - 0.05, 0.4); st.cue('sfx:click', 'S17', P17, 0.6)
st.cue('sfx:bell', 'S18', 0.05, 0.35); st.cue('sfx:whistle', 'S18', 0.4, 0.2)
st.cue('sfx:carDoor', 'S19', 0.0, 0.3); st.cue('sfx:step', 'S19', 0.1, 0.3); st.cue('sfx:step', 'S19', 0.24, 0.3)
st.cue('sfx:whistle', 'S20', 0.02, 0.3)
for t_ in STEP20: st.cue('sfx:tick', 'S20', t_, 0.4)
st.cue('sfx:gasp', 'S20', GR20 - 0.05, 0.45); st.cue('sfx:stretch', 'S20', NO20, 0.4)
st.cue('sfx:twang', 'S21', P21 - 0.05, 0.4); st.cue('sfx:click', 'S21', P21, 0.7); st.cue('sfx:slideDown', 'S21', P21 + 0.04, 0.5)
st.cue('sfx:gulp', 'S22', L22, 0.4); st.cue('sfx:stepSoft', 'S22', G22 + 0.05, 0.3); st.cue('sfx:stepSoft', 'S22', G22 + 0.25, 0.3); st.cue('sfx:stepSoft', 'S22', G22 + 0.42, 0.25)
st.cue('sfx:slideUp', 'S23', 0.12, 0.35); st.cue('sfx:slideUp', 'S23', 0.36, 0.35); st.cue('sfx:click', 'S23', B23, 0.4)
st.cue('sfx:stepHeavy', 'S24', 0.05, 0.3); st.cue('sfx:stepHeavy', 'S24', 0.3, 0.3); st.cue('sfx:stepHeavy', 'S24', 0.55, 0.3); st.cue('sfx:grunt', 'S24', 0.4, 0.3)
st.cue('sfx:paper', 'S25', A25, 0.55); st.cue('sfx:ding', 'S25', A25 + 0.36, 0.4)

CITIZEN = lambda preset, seed, **kw: {'preset': preset, 'seed': seed, 'build': {'width': 0.86, 'headWidth': 1.3, **kw.pop('build', {})}, **kw}
st.write("L'interrupteur", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, extra_cast={
    'maire': {'preset': 'politique', 'sash': ['#2A4B9B', '#F4F1E8', '#C8202A'], 'sashW': 0.12, 'hair': 'combover', 'hairColor': '#B8B4AA', 'facial': 'mustache', 'beardColor': '#B8B4AA', 'glasses': False, 'seed': 13, 'skin': '#E6BE98', 'build': {'width': 0.96, 'headWidth': 1.3}},
    'elec': CITIZEN('worker', 83, glasses=False, suit='#3A6EA5', facial='mustache'),
    'b1': CITIZEN('pyjama', 85, suit='#1D1D22', pants='#1D1D22', hat='beanie', hatColor='#1D1D22', facial='stubble', build={'height': 0.9, 'width': 1.0}),
    'b2': CITIZEN('pyjama', 87, suit='#1D1D22', pants='#1D1D22', hat='beanie', hatColor='#1D1D22', facial='mustache', build={'height': 1.06, 'width': 0.8}),
    'la': CITIZEN('femme', 89, suit='#B5486A'), 'lb': CITIZEN('lyceen', 91, suit='#3F7A5A', build={'height': 1.0}),
    'fact': CITIZEN('officiel', 93, suit='#2B4C8C', tie='#F2C230', hat='copcap', hatColor='#2B4C8C', glasses=False),
    'dame': CITIZEN('madame', 95, suit='#C8553D'), 'e1': CITIZEN('fermier', 97), 'e2': CITIZEN('gamin', 99), 'astro': CITIZEN('savant', 101)})
