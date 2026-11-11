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

# ---- his living room (back wall at z = -3.6), seen from the door: he is at the left of the frame, on his way out; the switch is on the back wall at the
#      right of the frame: his arm goes to it ACROSS the picture (seen from in front of him it ran into depth: a short crumpled sleeve)
LIV = {'lamp': False, 'tv': False, 'plant': False, 'pictureX': 0.12, 'pictureW': 1.0}   # the painting between his head and the switch, touching neither (its border met his head in the key pose of the hook)
LIV7 = {'lamp': False, 'tv': False, 'plant': False, 'picture': False}   # S06-S09: a plain wall behind the heads (the painting filled the gap between them, its border on their chins, and the label landed on its corner)
H1 = [-0.62, 0, -2.0]                                 # where he stops, on his way out
SW1 = [1.15, 1.5, -3.52]                             # the switch, on the back wall
SHO1 = [H1[0] + 0.2, 1.6, H1[2]]                     # his left shoulder (on our right: he faces us)
_d1 = [SW1[i] - SHO1[i] for i in range(3)]; _n1 = math.sqrt(sum(v * v for v in _d1)); U1 = [v / _n1 for v in _d1]   # the way from his shoulder to the switch
C1 = lambda t=0.0: cam(t, [0.0, 1.55, 3.3], [0.0, 1.55, 3.2], [0.1, 1.47, -3.0], [0.1, 1.47, -3.0], lens=44)
SWITCH = lambda flips, on=True: P('switch', 'rockerSwitch', pos=SW1, opts={'s': 2.0, 'flips': flips, 'on': on, 'rocker': '#E8502A', 'plate': '#F7F2E6', 'back': '#5E6B7A'})   # an orange rocker on a pale plate on a grey panel
TO_SW = lambda d, **kw: {'hands': {'L': 'point'}, 'reach': {'L': [round(SW1[0] - d * U1[0], 3), round(SW1[1] - d * U1[1] + 0.02, 3), round(SW1[2] - d * U1[2] + 0.06, 3), 1, 0.16, [0.2, -1, 0.3]]}, **kw}   # his left index d metres short of the rocker, along the arm

# 1: on his way out: a step toward us, a glance back with his eyes alone; he leans away, then his arm is thrown across the whole room, a ripple along it;
#    the finger stops a hand short of the switch, four frames; then taps it: black. Two eyes
A1, B1, K1 = 0.1, 0.2, 0.64                          # the wind-up, the throw, the tap (the throw 0.12 s sooner: the finger held a hand short of the switch has eight frames)
st.shot('S01', 'livingRoom', setOpts=LIV, actors=[act('mec', [H1[0], 0, H1[2] - 0.35], 6, 'walk', 'neutral', keys=[k(0.0, look=None), k(0.0, to=H1, dur=0.1, clip='walk', ease='out', face=6), k(0.03, toon={'face': {'gx': 0.9, 'gy': -0.1}}, toonDur=0.05),   # a step; the light: his eyes go back to it, not his head
            k(A1, clip='stand', blend=0.06), k(A1, toon={'hands': {'L': 'point'}, 'reach': {'L': [H1[0] - 0.25, 1.45, H1[2] + 0.3, 1, 0.16]}, 'bend': {'spine': [0.0, 0.2, 0, 1, None]}, 'sq': [1.04, 0.95, 1.04], 'face': {'gx': 0.9}}, toonDur=0.1, toonEase='out'),   # he leans away from it, the index cocked across his chest: the wind-up
            k(B1, toon=TO_SW(0.55, wave=RIP('L', 0.07, 0.5, 1), bend={'spine': [0, -0.16, 0, 1, None]}, sq=[0.97, 1.05, 0.97], face={'gx': 0.9, 'browL': 0.6}), toonDur=0.1, toonEase='out'),   # thrown across the room
            k(B1 + 0.12, toon=TO_SW(0.2, wave=RIP('L', 0.035, 1.3, 1), bend={'spine': [0, -0.1, 0, 1, None]}, face={'gx': 0.9, 'browL': 0.6}), toonDur=0.08),   # it stops a hand short, still ringing: held four frames
            k(B1 + 0.26, toon=TO_SW(0.2, wave=RIP('L', 0.012, 2.4, 1), bend={'spine': [0, -0.08, 0, 1, None]}, face={'gx': 0.9, 'browL': 0.8, 'eye': 0.15}), toonDur=0.1),   # the ringing dies; a brow goes up: will it
            k(K1 - 0.04, toon=TO_SW(0.03, face={'gx': 0.9, 'browL': 0.6}), toonDur=0.04, toonEase='in'),   # the tap
            k(K1 + 0.1, toon=TO_SW(0.05), toonDur=0.06), k(K1 + 0.1, expr='surprised'),   # in the black: two eyes, to us
            k(K1 + 0.3, toon=TO_SW(0.05, face={'lid': 1}), toonDur=0.04), k(K1 + 0.38, toon=TO_SW(0.05), toonDur=0.04),   # a blink
            k(K1 + 0.44, toon={'face': {'gx': -0.8}}, toonDur=0.1, toonEase='inOut')])],   # the arm comes home; his eyes go to the door
        props=[SWITCH([K1])],
        dark=[[K1 + 0.02, 1]], darkFloor=0.035, darkEyes=1.5,
        cams=[C1(), glide([cam(K1 + 0.05, [H1[0] + 0.05, 2.06, H1[2] + 1.7], [H1[0] + 0.05, 2.06, H1[2] + 1.65], [H1[0], 2.04, H1[2]], [H1[0], 2.04, H1[2]], lens=44)], 0.22)])   # in the black the camera goes to his eyes

# 2: on his way out, in the black: two eyes come toward us, a dip at each of his two steps; he walks into the glass door: flat on it, his eyes wide
#    and flat for four frames, a glint on the pane, stars; then two spirals that slide down
G2 = 0.34                                           # he meets the glass
ST2 = {'clear': [-30, 30], 'eiffel': False, 'night': True}
STEP2 = lambda sy: {'sq': [1.0, sy, 1.0], 'auto': 0}
st.shot('S02', 'parisStreet', setOpts=ST2, lighting='night', actors=[act('mec', [8.6, 0, -3.2], 0, 'walk', 'neutral', keys=[k(0.0, look=None), k(0.0, to=[8.6, 0, -1.25], dur=G2, clip='walk', ease='linear'),
            k(0.04, toon=STEP2(0.9), toonDur=0.05), k(0.1, toon=STEP2(1.0), toonDur=0.06), k(0.2, toon=STEP2(0.9), toonDur=0.05), k(0.26, toon=STEP2(1.0), toonDur=0.06),   # two steps: his eyes dip and come back up
            k(G2, clip='pressGlass', blend=0.02), k(G2, toon={'sq': [1.5, 1.0, 0.22], 'scl': {'head': [1.5, 0.74, 1]}, 'auto': 0, 'face': {'eye': 0.5}}, toonDur=0.03),   # flat on the glass: his eyes wide and flat: four frames (no new expression here: a strong one starts with a blink, and the four frames were black)
            k(G2 + 0.2, expr='dizzy'), k(G2 + 0.2, toon={'sq': [1.4, 1.0, 0.25], 'scl': {'head': [1.25, 0.9, 1]}, 'auto': 0}, toonDur=0.05),   # six frames; then the spirals
            k(G2 + 0.25, to=[8.6, -0.3, -1.25], dur=round(st.dur('S02') - G2 - 0.25, 3), ease='out', face='keep')])],   # and he slides down it: not as far as the caption line
        props=[P('stars', 'impactStars', pos=[8.6, 2.1, -1.0], inDark=True, opts={'at': G2, 'n': 6, 'r': 0.5, 'r0': 0.62, 'dur': 0.4, 'size': 0.06}),   # round his eyes, not over them
               P('glint', 'glassGlint', pos=[8.9, 2.38, -1.04], inDark=True, opts={'at': G2 + 0.01, 'w': 0.2, 'dur': 0.3})],
        dark=[[0, 1, 0.001]], darkFloor=0.03, darkEyes=2.2,
        fx=[{'type': 'shake', 'at': G2, 'dur': 0.16, 'amount': 0.03}],
        cams=[cam(0.0, [8.6, 2.0, 0.25], [8.6, 2.0, 0.2], [8.6, 2.0, -6.0], [8.6, 2.0, -6.0], lens=44)])

# 3: the whole city: Paris at night from a height; the black runs out from his street, row after row; the tower stands alone, lit, then pops; eyes open
#    in the dark windows
CITY = lambda keys, **kw: P('city', 'cityNight', pos=[0, 0, 0], inDark=True, opts={'keys': keys, 'moonX': -8, **kw})   # inDark: drawn with its own colours in every shot (the shots give a `dark` key even when the light stays on)
LIT = [[0, 0, 0.001]]                                 # a shot that stays lit but draws what is `inDark` the same way as the dark shots
VIEW = lambda t, a, b: cam(t, a, b, [4.0, 1.5, -60.0], [4.0, 1.5, -60.0], lens=44)
NEAR = lambda **kw: P('house', 'nearHouse', pos=[0.75, 1.57, -9.0], inDark=True, opts=kw)   # the house across the street: its roof line a little under the middle of the frame, three big windows above the caption band (the windows and the eyes of the far city were specks, cut by roofs or behind the caption)
st.shot('S03', 'spaceDark', setOpts={'stars': 300}, lighting='night',
        props=[CITY([[0.15, 0, 0.45]], towerLag=0.22, eyesLag=0.22, eyes=0), NEAR(keys=[[0.15, 0]], lag=0.1, eyesAt=0.86, eyesLag=0.1)], dark=LIT,
        cams=[VIEW(0.0, [0.0, 2.3, 4.0], [0.0, 2.1, 1.5])])

# 4: he turned it back on: the black, his eyes; the tap: the light: he stands where he stood, the arm across the room again, a lump on his head, a
#    star still going round it; the arm comes home
K4 = 0.28
st.shot('S04', 'livingRoom', setOpts=LIV, actors=[act('mec', H1, 6, 'stand', 'unimpressed', keys=[k(-0.05, toon=TO_SW(0.2, face={'bump': 1, 'stars': 1, 'lid': 0.5}), toonDur=0), k(0.0, look=None),   # in the black: his eyes, heavy
            k(0.07, toon=TO_SW(0.2, face={'bump': 1, 'stars': 1, 'lid': 1}), toonDur=0.04), k(0.14, toon=TO_SW(0.2, face={'bump': 1, 'stars': 1, 'gx': 0.95, 'eye': 0.2}), toonDur=0.05),   # a blink; they dart to the switch
            k(K4 - 0.04, toon=TO_SW(0.03, face={'bump': 1, 'stars': 1, 'gx': 0.95}), toonDur=0.04, toonEase='in'), k(K4 + 0.08, expr='unimpressed'),   # the tap: the light
            k(K4 + 0.1, toon=TO_SW(0.3, wave=RIP('L', 0.06, 0.5, 1), face={'bump': 1, 'stars': 0.6, 'browR': -0.6, 'browL': 0.5}), toonDur=0.1),
            k(K4 + 0.26, toon={'face': {'bump': 1, 'stars': 0.3, 'browR': -0.6, 'browL': 0.5}, 'touch': {'R': ['face', 0.1, 1.02, 0.04, 1, 0.1]}, 'bend': {'spine': [0, 0.06, 0, 1, None]}}, toonDur=0.2, toonEase='outBack')])],   # the arm snaps home; the other hand goes to the lump
        props=[SWITCH([K4], on=False)],
        dark=[[0, 1, 0.001], [K4 + 0.02, 0]], darkFloor=0.035, darkEyes=1.5,
        cams=[cam(0.0, [H1[0] + 0.05, 2.06, H1[2] + 1.65], [H1[0] + 0.05, 2.06, H1[2] + 1.6], [H1[0], 2.04, H1[2]], [H1[0], 2.04, H1[2]], lens=44), C1(K4 + 0.02)])   # in the black: where S01 left us, close on his eyes (seen from the door they were small, at the edge of the frame); at the tap: the room

# 5: the city came back on: the light runs out again from his street; the tower glitters; then off, on: he is trying the switch
st.shot('S05', 'spaceDark', setOpts={'stars': 300}, lighting='night',
        props=[CITY([[0.1, 1, 0.35], [0.68, 0, 0.1], [0.86, 1, 0.1]], lit=0, towerLag=0.0, sparkle=[0.45, 0.68], eyes=0), NEAR(lit=0, keys=[[0.1, 1], [0.68, 0], [0.86, 1]], lag=0.05)], dark=LIT,
        cams=[VIEW(0.0, [0.0, 2.1, 1.5], [0.0, 2.3, 3.4])])

# ---- the town hall brings an electrician to his living room
E7, H7 = [-0.36, 0, -0.3], [0.36, 0, -0.4]          # the electrician and him, face to face, three quarters to us
RE, RH = 30, -25
def face_pt(pos, ry, across=0.0, up=0.31, out=0.1):  # a point of the face of a man standing at pos, turned ry: across (m, + = his left), up (0 = chin .. 1 = top of the skull; nose 0.31, mouth 0.23, brow 0.8), out (m in front)
    a = math.radians(ry); return r3([pos[0] + out * math.sin(a) + across * math.cos(a), pos[1] + 1.77 + 0.5 * up, pos[2] + out * math.cos(a) - across * math.sin(a)])
NOSE7 = face_pt(H7, RH)
LUMP = {'bump': 0.8}

# 6: the mayor, in his sash, points at him; the electrician tears in with his meter and slides in on his knees between them, the meter held up under
#    his nose; his eyes go from the finger to the meter. (v1: he skidded to a stop standing, in front of the mayor: the finger and half the face were gone)
M6, E6, H6 = [-0.72, 0, -1.25], [0.0, 0, -0.05], [0.66, 0, -0.5]
MET6 = [0.5, 1.02, 0.34]                             # the meter, at the end of his arms, in front of the hero's waist (higher, it hid the electrician's face)
st.shot('S06', 'livingRoom', setOpts=LIV7, actors=[act('mec', H6, -18, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={'face': {**LUMP, 'gx': -0.9, 'browL': 0.7, 'browR': -0.4}}, toonDur=0.0),
            k(0.4, toon={'face': {**LUMP, 'gx': -0.5, 'gy': 0.8, 'browL': 0.9, 'browR': 0.9, 'eye': 0.2}, 'bend': {'neck': [0.14, 0, 0, 1, None]}}, toonDur=0.08, toonEase='outBack')]),   # the finger, then the meter under his nose
        act('maire', M6, 24, 'stand', 'angry', keys=[k(0.0, look=None), k(0.0, toon={'hands': {'L': 'point'}, 'reach': {'L': [-0.45, 2.75, -1.1, 1, 0.16, [0, 1, 0.2]]}, 'sq': [0.94, 1.1, 0.94], 'face': {'gx': 0.9}}, toonDur=0.0),   # up on his toes, the arm high
            k(0.1, toon={'hands': {'L': 'point'}, 'reach': {'L': [0.3, 2.58, -0.75, 1, 0.16, [0, 1, 0.2]]}, 'sq': [0.94, 1.1, 0.94], 'bend': {'spine': [0.1, -0.16, 0, 1.04, None]}, 'face': {'jaw': 0.35, 'gx': 0.9}}, toonDur=0.08, toonEase='outBack'),   # the finger comes down on him from above, over the electrician's helmet
            k(0.5, toon={'hands': {'L': 'point'}, 'reach': {'L': [0.34, 2.5, -0.72, 1, 0.16, [0, 1, 0.2]]}, 'sq': [0.94, 1.1, 0.94], 'bend': {'spine': [0.12, -0.18, 0, 1.04, None]}, 'face': {'jaw': 0.2, 'gx': 0.9, 'gy': 0.4}}, toonDur=0.2, toonEase='inOut')]),   # it shakes at him: a moving hold
        act('elec', [-2.9, 0, -0.05], 90, 'run', 'determined', keys=[k(0.0, to=[-0.5, 0, -0.05], dur=0.24, clip='run', ease='linear', face=60), k(0.24, to=E6, dur=0.26, glide=True, ease='out', face=42), k(0.24, clip='kneelGive', blend=0.06), k(0.3, look=None),
            k(0.5, expr='hmm'), k(0.5, toon={'face': {'gx': 0.8, 'gy': -0.4}, 'bend': {'spine': [-0.08, 0, 0, 1, None]}}, toonDur=0.1, toonEase='outBack')])],   # on his knees, the meter up: he looks up at him
        props=[P('meter', 'voltMeter', pos=[-2.6, 0.95, 0.3], ry=14, opts={'w': 0.4, 'needle': [[0, 0.12]]}, keys=[k(0.0, to=[-0.1, 0.95, 0.34], dur=0.24, ease='linear'), k(0.24, to=MET6, dur=0.26, ease='out'), k(0.5, squash=[1.08, 0.9, 1.0], dur=0.25)])],
        cams=[cam(0.0, [0.15, 1.6, 3.9], [0.12, 1.6, 3.7], [0.05, 1.45, -0.9], [0.05, 1.45, -0.9], lens=44)])

# 7: a clip on his nose: the needle slams over, the meter shakes and smokes; the electrician: eyes out, his helmet up; his: crossed on the clip.
#    The meter is held up between them at chest height (lower, its dial sat in the caption band); the electrician's face stays three quarters to us, his
#    eyes alone go to the nose and to the dial (a look at them turned his head: a blank profile three shots running)
CL7, ND7 = 0.26, 0.38
MET7 = [0.0, 1.3, 0.14]
M7 = lambda **kw: {**kw, 'hands': {'L': 'grip', **kw.get('hands', {})}, 'reach': {'L': [MET7[0] - 0.25, MET7[1] + 0.14, MET7[2] + 0.02, 1, 0.06], **kw.get('reach', {})}}   # his left hand holds the meter up
CLIP7 = lambda w, **kw: M7(hands={'R': 'pinch'}, reach={'R': [NOSE7[0] - 0.03, NOSE7[1], NOSE7[2] + 0.02, w, 0.06]}, **kw)
st.shot('S07', 'livingRoom', setOpts=LIV7, actors=[act('mec', H7, RH, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={'face': {**LUMP, 'gx': -0.6}}, toonDur=0.0),
            k(CL7, toon={'scl': {'head': [1.16, 0.88, 1]}, 'face': {**LUMP, 'cross': 1, 'eye': 0.35, 'brow': 0.8}}, toonDur=0.04), k(CL7 + 0.08, toon={'scl': {'head': [0.96, 1.04, 1]}, 'face': {**LUMP, 'cross': 1, 'eye': 0.35, 'brow': 0.8}}, toonDur=0.08, toonEase='outBack'),
            k(CL7 + 0.2, toon={'face': {**LUMP, 'cross': 1, 'eye': 0.35, 'brow': 0.8}}, toonDur=0.08), k(ND7 + 0.3, toon={'face': {**LUMP, 'cross': 0.6, 'eye': 0.2, 'browL': 0.8, 'browR': -0.3, 'gy': 0.5}}, toonDur=0.15)]),   # then down to the needle
        act('elec', E7, RE, 'stand', 'hmm', keys=[k(0.0, look=None), k(0.0, toon=CLIP7(0, face={'gx': 0.9}), toonDur=0.0), k(0.08, toon=M7(hands={'R': 'pinch'}, reach={'R': [-0.15, 1.95, 0.15, 1, 0.06]}, sq=[1.03, 0.96, 1.03], face={'gx': 0.9, 'gy': -0.3}), toonDur=0.08),   # the clip, held up
            k(CL7 - 0.06, toon=CLIP7(1, face={'gx': 0.9, 'gy': -0.3}), toonDur=0.06, toonEase='in'), k(CL7 + 0.1, toon=M7(face={'gy': 0.9, 'gx': 0.5}), toonDur=0.1),   # on his nose; his eyes go down to the dial
            k(ND7 + 0.06, expr='take'), k(ND7 + 0.06, toon=M7(sq=[0.9, 1.14, 0.9], hat=[0.3, 0.25, 0], face={'pop': 0.85, 'jaw': 0.7, 'popLen': 0.16, 'eyeYaw': 0.45, 'eyePitch': 0.5}), toonDur=0.08, toonEase='outBack'),   # the take: eyes out at the dial, the helmet up
            k(ND7 + 0.4, toon=M7(hat=[0.05, 0.1, 0], face={'pop': 0.5, 'jaw': 0.5, 'popLen': 0.12, 'eyeYaw': 0.45, 'eyePitch': 0.5}), toonDur=0.25)])],
        props=[P('meter', 'voltMeter', pos=MET7, rot=[-0.12, 0, 0], opts={'w': 0.44, 'needle': [[0, 0.12], [ND7 - 0.04, 0.12], [ND7 + 0.02, 1.0]], 'smokeAt': ND7 + 0.28}, keys=[k(ND7 + 0.02, squash=[1.12, 0.86, 1.0], dur=0.3)]),
               P('cable', 'jumperCable', pos=[MET7[0] + 0.1, MET7[1] + 0.2, MET7[2]], opts={'to': r3([NOSE7[0] - MET7[0] - 0.1, NOSE7[1] - MET7[1] - 0.2, NOSE7[2] - MET7[2] + 0.02]), 'sag': 0.16}, keys=[k(0.0, visible=False), k(CL7, visible=True)])],
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
          k(t + 0.17, toon=PULLED(1.06, face={**LUMP, 'gx': -0.9, 'eye': 0.3}), toonDur=0.1), k(t + 0.26, toon=PULLED(1.0, face={**LUMP, 'gx': -0.9, 'eye': 0.3}), toonDur=0.08)]   # (in the black his eyes go to the electrician)
    ek = [k(t - 0.06, toon=HOLD8(1.75, bend={'spine': [0.12, 0, 0, 1, None]}), toonDur=0.06, toonEase='in'), k(t + 0.07, toon=HOLD8(0.9), toonDur=0.07, toonEase='out'), k(t + 0.17, toon=HOLD8(1.04, face={'lid': 1}), toonDur=0.05), k(t + 0.26, toon=HOLD8(1.0, face={'gx': 0.9}), toonDur=0.06)]   # (a blink, then a look at him: in the black, eyes that move)
    return hk, ek
(h8a, e8a), (h8b, e8b) = pull8(P8a), pull8(P8b)
st.shot('S08', 'livingRoom', setOpts=LIV7, actors=[act('mec', H7, RH, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=PULLED(1.0, face={**LUMP, 'gx': -0.5}), toonDur=0.0), k(0.3, toon=PULLED(1.0, face={**LUMP, 'gy': 0.8}), toonDur=0.1)] + h8a + h8b +   # his eyes go down to the hand on his tie
            [k(P8b + 0.3, toon=PULLED(1.0, face={**LUMP, 'browL': 0.8, 'browR': -0.5}), toonDur=0.1)]),
        act('elec', E7, RE, 'stand', 'neutral', keys=st.talk('L04', 'S08', 'neutral') + [k(0.0, look=None), k(0.02, toon=HOLD8(1.0), toonDur=0.22, toonEase='out')] + e8a + e8b +   # (his face stays three quarters to us from the start: turned to the hero, his eyes in the black were two slivers)
            [k(P8b + 0.3, toon={'hands': {'L': 'thumbUp'}, 'reach': {'L': [0.0, 1.75, 0.0, 1, 0.1]}, 'face': {'browL': 0.8}}, toonDur=0.12, toonEase='outBack')])],   # then a thumb at him
        dark=[[P8a + 0.02, 1], [P8b + 0.02, 0]], darkFloor=0.035, darkEyes=2.6,
        cams=[cam(0.0, [0.1, 1.6, 3.1], [0.08, 1.6, 2.95], [0.0, 1.5, -0.35], [0.0, 1.5, -0.35], lens=44)])

# 9: « c'est lui. » : he slaps the label of a fuse box on his forehead: GÉNÉRAL; his head goes into his shoulders and comes back, his eyes cross up to it
SL9 = 0.26
FORE9 = face_pt(H7, RH, 0.0, 0.92, 0.1)
X9 = {'cross': 1, 'gy': -0.9, 'brow': 0.5, 'eye': 0.3, 'pupilSize': 0.35}   # his eyes crossed up at the label: open (expr worried, not a STRONG one: no automatic blink), a little bigger, the pupils too
HAND9a, HAND9b = [-0.2, 1.5, 0.3], [-0.4, 2.5, 0.1]   # the label in his hand: shown, then wound up behind his head
_f9 = [math.sin(math.radians(RH)), math.cos(math.radians(RH))]   # where the hero's face looks
CAM9 = r3([H7[0] + 1.62 * _f9[0], 2.08, H7[2] + 1.62 * _f9[1]])   # the close camera: square to his forehead
st.shot('S09', 'livingRoom', setOpts=LIV7, actors=[act('mec', H7, RH, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={'face': {'gx': -0.7, 'gy': -0.4}}, toonDur=0.0),
            k(SL9, expr='worried'), k(SL9, toon={'scl': {'head': [1.3, 0.72, 1]}, 'bend': {'neck': [0, 0, 0, 0.5, None], 'spine': [0, 0, 0, 0.94, None]}, 'sq': [1.05, 0.94, 1.05], 'face': {**X9}}, toonDur=0.03),
            k(SL9 + 0.1, toon={'scl': {'head': [0.93, 1.1, 1]}, 'bend': {'neck': [0, 0, 0, 1.3, None]}, 'face': {**X9}}, toonDur=0.07, toonEase='out'),
            k(SL9 + 0.22, toon={'face': {**X9}}, toonDur=0.12, toonEase='outBack'), k(SL9 + 0.36, toon={'face': {**X9, 'browL': 0.5, 'browR': -0.3}}, toonDur=0.08)]),   # one beat in the close shot: the word and his eyes crossed up at it, to the cut
        act('elec', E7, RE, 'stand', 'smug', keys=st.talk('L04', 'S09', 'smug') + [k(0.0, look=None), k(0.0, toon={'hands': {'R': 'open'}, 'reach': {'R': [HAND9a[0], HAND9a[1] - 0.02, HAND9a[2] - 0.04, 1, 0.1]}}, toonDur=0.0),   # the label, shown in his hand
            k(0.05, toon={'hands': {'R': 'open'}, 'reach': {'R': [HAND9b[0], HAND9b[1] - 0.02, HAND9b[2] - 0.04, 1, 0.1]}, 'bend': {'spine': [-0.18, 0, 0, 1.03, None]}, 'sq': [0.97, 1.05, 0.97]}, toonDur=0.12, toonEase='outBack'),   # the wind-up: up behind his head, he leans back
            k(SL9 - 0.05, toon={'hands': {'R': 'open'}, 'reach': {'R': [FORE9[0] - 0.02, FORE9[1], FORE9[2] + 0.03, 1, 0.1]}, 'bend': {'spine': [0.2, 0, 0, 1, None]}}, toonDur=0.05, toonEase='in'),
            k(SL9, toon={'hands': {'R': 'open'}, 'reach': {'R': [FORE9[0] - 0.02, FORE9[1] - 0.25, FORE9[2] + 0.05, 1, 0.1]}, 'bend': {'spine': [0.26, 0, 0, 1, None]}}, toonDur=0.03),   # the palm stays on the label while the head sinks under it
            k(SL9 + 0.1, toon={'hands': {'R': 'thumbUp'}, 'reach': {'R': [-0.3, 1.72, 0.1, 1, 0.1]}}, toonDur=0.14, toonEase='outBack')])],   # then home, a thumb up at his own chest: out of the close shot
        props=[P('plate', 'fusePlate', pos=HAND9a, ry=0, opts={'w': 0.25}, keys=[k(0.05, to=HAND9b, dur=0.12, ease='outBack'), k(SL9 - 0.05, to=[FORE9[0], FORE9[1], FORE9[2] + 0.01], dur=0.05, ease='in'), k(SL9, attach='mec', joint='head', offset=[0.0, 0.462, 0.094], rot=[0, 0, 0.06]), k(SL9, squash=[1.3, 0.72, 1.0], dur=0.3)])],   # on the hairline: both eyes show under it
        fx=[{'type': 'shake', 'at': SL9, 'dur': 0.14, 'amount': 0.02}],
        cams=[cam(0.0, [0.0, 1.98, 2.75], [0.02, 1.98, 2.62], [0.0, 1.95, -0.35], [0.0, 1.95, -0.35], lens=44),
              cam(SL9 + 0.1, CAM9, [CAM9[0] + 0.04 * _f9[0], CAM9[1], CAM9[2] - 0.04 * _f9[1]], [FORE9[0], 2.05, FORE9[2]], [FORE9[0], 2.05, FORE9[2]], lens=28)])   # close on his forehead: GÉNÉRAL fills a third of the frame, his eyes crossed up at it (in the two-shot the word was 12 % of the width)

# ---- every evening at ten: his balcony above Paris
B10 = [0.2, 0, -0.15]                                # where he stands on the balcony, facing us, the city behind him
NIGHT = {'stars': 300}
BALC = lambda: P('balc', 'balcony', pos=[0, 0, 0], opts={'w': 3.4, 'd': 1.3})
CAPN = lambda: P('cap', 'nightCap', pos=[0, 0, 0], on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'side': -1})   # it falls to our left: the tower, on our right, stays clear of it
CITY10 = lambda keys, **kw: P('city', 'cityNight', pos=[0, 0, -0.7], inDark=True, opts={'keys': keys, 'towerX': 9.0, 'moonX': -34, 'moonY': 30, 'eyes': 0, **kw})   # the tower on our right, clear of his arm; the moon over the clock, clear of his other arm and of the pompom
CLOCK = lambda at_=None: P('clock', 'ledClock', pos=[-7.35, 4.2, -29.6], opts={'w': 3.9, 'from': '21:59', 'to': '22:00', 'at': at_} if at_ is not None else {'w': 3.9, 'from': '22:00'})   # on a front across the street, left of him in both shots: whole, and clear of his arms (5.6 m wide, an arm crossed its last figure)

# 10: 21:59 on the big clock across the street; it turns to 22:00: he yawns, arms up as far as they go
F10 = 0.3                                           # the clock turns
HANDS10 = lambda kk: {'L': [B10[0] + 0.3 + 0.1 * kk, 2.3 + 1.2 * kk, B10[2] + 0.05, 1, 0.1], 'R': [B10[0] - 0.3 - 0.1 * kk, 2.3 + 1.2 * kk, B10[2] + 0.05, 1, 0.1]}   # his hands, straight up over his shoulders: a narrow Y that leaves the frame
YAWN = lambda kk, **kw: {'hands': {'L': 'spread', 'R': 'spread'}, 'reach': HANDS10(kk), 'bend': {'spine': [-0.14 * kk, 0, 0, 1 + 0.14 * kk, None], 'neck': [-0.2 * kk, 0, 0, 1, None]},
                         'sq': [1 - 0.05 * kk, 1 + 0.1 * kk, 1 - 0.05 * kk], 'face': {'jaw': 0.95 * kk, 'jawLen': 0.5 * kk, 'mouth': 'yawn', 'mouthW': 0.7 * kk, 'mouthH': 0.5 * kk, 'lid': kk, 'brow': 0.7 * kk}, **kw}   # the jaw down to the knot of his tie, the mouth as wide as what is left of his face
st.shot('S10', 'spaceDark', setOpts=NIGHT, lighting='night', actors=[act('mec', B10, 4, 'stand', 'sleepy', keys=[k(0.0, look=None), k(0.06, toon={'face': {'gx': -0.9, 'gy': -0.5}}, toonDur=0.08),   # his eyes on the clock
            k(F10 + 0.06, toon={'sq': [1.04, 0.94, 1.04], 'face': {'lid': 0.6}}, toonDur=0.06), k(F10 + 0.14, toon=YAWN(0.35), toonDur=0.1, toonEase='out'),   # ten o'clock: he sinks a little, then it comes
            k(F10 + 0.3, toon=YAWN(1.0, wave={**RIP('L', 0.05, 0.4, 1), **RIP('R', 0.05, 0.9, 1)}), toonDur=0.2, toonEase='out'),   # arms out of the frame, the jaw on his tie
            k(F10 + 0.52, toon=YAWN(1.06, wave={**RIP('L', 0.04, 1.2, 1), **RIP('R', 0.04, 1.7, 1)}), toonDur=0.22),   # it still grows a little: a moving hold
            k(F10 + 0.66, toon={'sq': [1.04, 0.95, 1.04], 'face': {'lid': 0.7}}, toonDur=0.16, toonEase='inOut')])],   # the arms come down, without a bump before the cut
        props=[BALC(), CAPN(), CITY10([], sparkle=[F10, 99], towerX=16.5, towerH=44), CLOCK(F10)], dark=LIT,
        look={'sun': 2.6, 'sunColor': '#C4D6FF', 'sunDir': [-0.55, 0.45, 0.9], 'fill': 1.5},   # moonlight from in front of him, on our left: his sleeves are pale against the sky (navy on navy, the biggest stretch of the film had no silhouette)
        cams=[cam(0.0, [0.3, 1.9, 3.5], [0.3, 1.9, 3.35], [0.0, 1.85, -0.3], [0.0, 1.85, -0.3], lens=44)])   # a little further back than v1: the clock whole at his left, his arms up between it and the tower

# 11: he takes the end of his own tie and pulls: click; the black runs out over Paris behind him; the tower stands alone, then pops; his eyes shut
P11 = 0.6
TIE11 = lambda L: tie_tip(B10, 4, L, 0.15)
SELF = lambda L, **kw: {'hands': {'R': 'grip'}, 'reach': {'R': [*TIE11(L), 1, 0.05, [-0.7, -0.4, 0.4]]}, 'tie': [L, 0.15, 0], **kw}
st.shot('S11', 'spaceDark', setOpts=NIGHT, lighting='night', actors=[act('mec', B10, 4, 'stand', 'sleepy', keys=[k(0.0, look=None), k(0.12, toon=SELF(1.0), toonDur=0.16, toonEase='out'),   # the hand finds the tie without a look
            k(P11 - 0.06, toon=SELF(1.7, bend={'spine': [0.25, 0, 0, 1, None], 'neck': [0.25, 0, 0, 0.8, None]}, sq=[1.05, 0.93, 1.05]), toonDur=0.06, toonEase='in'),
            k(P11 + 0.07, toon=SELF(0.85, bend={'neck': [-0.1, 0, 0, 1.25, None]}, sq=[0.96, 1.07, 0.96]), toonDur=0.07, toonEase='out'), k(P11 + 0.17, toon=SELF(1.05), toonDur=0.1), k(P11 + 0.26, toon=SELF(1.0), toonDur=0.08),
            k(P11 + 0.4, toon={'face': {'gx': 0.8}}, toonDur=0.1), k(P11 + 0.62, expr='happy'), k(P11 + 0.62, toon={}, toonDur=0.1),   # in the black: a look over his shoulder; content
            k(P11 + 0.8, toon={'face': {'lid': 1}}, toonDur=0.1), k(P11 + 0.86, toon={'face': {'lid': 1}, 'bend': {'neck': [0.3, 0.08, 0, 1, None], 'spine': [0.06, 0, 0, 0.98, None]}}, toonDur=0.24, toonEase='inOut')])],   # the tower has gone out: good night: his head nods forward, the pompom after it (the cut-out stood stock-still for its last 0.7 s)
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
DZ12 = 0.38                                         # how far they sidle before the match (from 1.1 m away, one pair of eyes was cut by the edge of the frame)
B1b, B2b = [8.95, 0, 0.08], [9.15, 0, -0.78]         # where they stand in the light: the small one on our right with the match, the tall one hugging the set
back = lambda p_: [p_[0], p_[1], round(p_[2] - DZ12, 3)]
MATCH12 = [8.72, 1.92, -0.34]                       # the match: between their heads
LIT12 = lambda **kw: {'hands': {'R': 'pinch'}, 'reach': {'R': [*MATCH12, 1, 0.06, [0.2, -1, 0.3]]}, **kw}
st.shot('S12', 'parisStreet', setOpts=FAC, lighting='night', actors=[
        act('b1', back(B1b), -72, 'tiptoe', 'sneaky', keys=[k(0.0, look=None), k(0.0, to=B1b, dur=M12 - 0.08, clip='tiptoe', ease='linear', face=-72),
            k(M12 - 0.08, clip='stand', blend=0.05), k(M12 - 0.08, toon=LIT12(), toonDur=0.08, toonEase='out'),   # the match, struck between them
            k(M12 + 0.02, look=CAMB, expr='takeSmall'), k(M12 + 0.02, toon=LIT12(sq=[0.94, 1.08, 0.94], face={'eye': 0.3}), toonDur=0.05),   # caught
            k(M12 + 0.22, expr='happy'), k(M12 + 0.22, toon=LIT12(face={'mouth': 'teeth', 'mouthW': 0.3, 'browL': 0.6}), toonDur=0.1, toonEase='outBack'),   # a grin
            k(O12 - 0.12, toon={'hands': {'R': 'pinch'}, 'reach': {'R': [MATCH12[0], MATCH12[1] - 0.03, MATCH12[2] + 0.22, 1, 0.06, [0.2, -1, 0.3]]}, 'face': {'puff': 1, 'mouth': 'o'}}, toonDur=0.1),   # to his mouth: he blows
            k(O12 + 0.04, toon={'face': {'mouth': 'teeth', 'mouthW': 0.3}}, toonDur=0.06)]),   # the grin stays in the black
        act('b2', back(B2b), -104, 'carry', 'sneaky', keys=[k(0.0, look=None), k(0.0, to=B2b, dur=M12 - 0.08, clip='carryBox', ease='linear', face=-104), k(M12 - 0.08, clip='carry', blend=0.05),
            k(M12 + 0.05, look=CAMB, expr='takeSmall'), k(M12 + 0.05, toon={'sq': [0.95, 1.07, 0.95], 'bend': {'neck': [0, 0, 0, 1.3, None]}, 'face': {'eye': 0.3}}, toonDur=0.05),
            k(M12 + 0.28, expr='happy'), k(M12 + 0.28, toon={'face': {'mouth': 'teeth', 'mouthW': 0.3, 'lidR': 1}}, toonDur=0.1, toonEase='outBack')])],   # a grin and a wink
        props=[MASK('b1'), MASK('b2'), P('tv', 'tv', pos=[0, 0, 0], scale=0.62, on={'actor': 'b2', 'joint': 'torso', 'offset': [0.0, -0.22, 0.4]}),
               P('match', 'matchStick', pos=[0, 0, 0], inDark=True, on={'actor': 'b1', 'hand': 'R', 'offset': [0.0, -0.1, 0.02], 'rot': [3.1416, 0, 0]}, opts={'litAt': M12, 'outAt': O12}, keys=[k(0.0, visible=False), k(M12 - 0.06, visible=True), k(O12 + 0.02, visible=False)])],
        dark=[[0, 1, 0.001]], darkFloor=0.035, darkEyes=2.4,
        darkPool={'prop': 'match', 'lift': [0, 0.1, 0], 'r': 1.25, 'k': [[M12, 0.92, 0.06], [O12, 0, 0.04]], 'tint': '#FFDDA8'},   # the match lights a pool round itself: two faces, the set, the hands; the street stays black (v1 lit the whole street evenly)
        cams=[cam(0.0, [5.0, 1.62, -0.35], [5.1, 1.62, -0.35], [9.0, 1.55, -0.35], [9.0, 1.55, -0.35], lens=44)])   # a little further back: the television whole in the frame

# 13: the lovers: on a bench, two pairs of eyes, face on: hearts by the third frame; they lean and slide toward each other until they nearly touch; a
#     heart pops where they meet; a third pair opens behind, between them, big: a look left, a look right, and it sinks slowly behind their heads.
#     (v1: turned three quarters to each other: small eyes, both pairs aslant the same way; the lean was keyed on the twist of the spine; the heart came
#     up over the third one's head)
LA, LB, TH13 = [9.2, 0, -0.09], [9.2, 0, 0.61], [9.74, 0.14, 0.02]   # (the head tipped 30 degrees carries the eyes 0.26 m toward our left: they sit that much to the right of where their eyes must be)
LOVE, KISS, T13 = 0.16, 0.34, 0.44                   # their eyes turn to hearts; the heart; the third pair opens
LVL = lambda **kw: {'bend': {'neck': [0, 0.52, 0, 1, None]}, 'auto': 0, **kw}   # the painted eyes sit aslant on the face (one 10 cm above the other): the head tipped 30 degrees, each pair is level: in the black, two pairs side by side
BEAT13 = lambda t_, **f: [k(t_, toon=LVL(scl={'head': [1.16, 1.16, 1]}, **f), toonDur=0.04, toonEase='out'), k(round(t_ + 0.07, 3), toon=LVL(**f), toonDur=0.1, toonEase='inOut')]   # a heartbeat: the eyes swell and come back
st.shot('S13', 'parisStreet', setOpts=FAC, lighting='night', actors=[
        act('la', LA, -90, 'sit', 'neutral', keys=[k(0.0, look=None), k(-0.05, toon=LVL(face={'gx': 0.9, 'eye': 0.3}), toonDur=0.0), k(LOVE, expr='love'), k(0.06, to=[LA[0], 0, LA[2] + 0.09], dur=0.24, glide=True, ease='inOut', face='keep')] +   # round eyes, on him: five frames; then hearts; she slides to him
            BEAT13(KISS + 0.02) + BEAT13(KISS + 0.3) + BEAT13(KISS + 0.56)),   # and her heart beats: three times to the cut
        act('lb', LB, -90, 'sit', 'neutral', keys=[k(0.0, look=None), k(-0.05, toon=LVL(face={'gx': -0.9, 'eye': 0.3}), toonDur=0.0), k(LOVE + 0.02, expr='love'), k(0.06, to=[LB[0], 0, LB[2] - 0.09], dur=0.24, glide=True, ease='inOut', face='keep')] +
            BEAT13(KISS + 0.06) + BEAT13(KISS + 0.34) + BEAT13(KISS + 0.6)),
        act('b1', TH13, -90, 'stand', 'scared', darkEyes=2.9, keys=[k(0.0, look=None), k(0.0, toon={'face': {'lid': 1}}, toonDur=0.0), k(T13, toon={'face': {'eye': 0.5}, 'sq': [0.96, 1.05, 0.96]}, toonDur=0.04, toonEase='outBack'),   # the third pair snaps open, between them
            k(T13 + 0.08, toon={'face': {'eye': 0.5, 'gx': -1}}, toonDur=0.04), k(T13 + 0.2, toon={'face': {'eye': 0.5, 'gx': 1}}, toonDur=0.04), k(T13 + 0.32, toon={'face': {'eye': 0.4}, 'auto': 0}, toonDur=0.05),   # a look left, four frames; a look right, four frames; to us
            k(T13 + 0.32, to=[TH13[0], -0.62, TH13[2]], dur=round(st.dur('S13') - T13 - 0.32, 3), ease='inOut', face='keep')])],   # and it goes down slowly, behind their heads
        props=[P('bench', 'bench', pos=[9.35, 0, 0.0], ry=-90, opts={'w': 1.5}), P('pop', 'heartPop', pos=[8.98, 1.76, 0.0], ry=-90, inDark=True, opts={'at': KISS, 'size': 0.085, 'flat': True, 'color': '#FF7486', 'until': T13 + 0.3})],   # a flat, pale heart over the line of their eyes; it bursts before the third pair goes down
        dark=[[0, 1, 0.001]], darkFloor=0.0, darkEyes=2.2,
        cams=[cam(0.0, [6.8, 1.62, 0.0], [6.9, 1.64, 0.0], [9.2, 1.72, 0.0], [9.2, 1.72, 0.0], lens=44)])   # a little further back than v1: a gap between the two pairs wider than between two eyes of one

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
            k(CU14 + 0.04, toon=BOTH(E14c, face={'gy': 0.9, 'gx': 0.2}), toonDur=0.06), k(CU14 + 0.22, toon=BOTH(E14c, face={'browL': 0.4}), toonDur=0.05),   # he reads; up to us, blank: four frames
            k(CU14 + 0.36, toon=BOTH(E14c, face={'gy': 1.0, 'gx': 0.2, 'eye': 0.4, 'brow': 0.9}), toonDur=0.03), k(CU14 + 0.43, toon=BOTH(E14c, bend={'neck': [0.3, 0, 0, 1, None]}, sq=[0.97, 1.05, 0.97], face={'gy': 1.0, 'gx': 0.2, 'eye': 0.4, 'brow': 0.9}), toonDur=0.05, toonEase='outBack'),   # his eyes snap back down to it, his head after them, two frames late: the double take
            k(CU14 + 0.6, toon=BOTH(E14c, bend={'neck': [0.34, 0, 0, 1, None]}, face={'gy': 1.0, 'gx': -0.3, 'eye': 0.4, 'brow': 0.9}), toonDur=0.1)]),   # and they run along the line again
        act('fact', [8.95, 0, -3.2], 0, 'walk', 'happy', keys=[k(-0.05, toon=GIVE(E14a), toonDur=0.0), k(0.0, to=[8.95, 0, -1.5], dur=G14 - 0.1, clip='walk', ease='out', face=-30), k(0.0, toon=GIVE(E14b), toonDur=G14 - 0.1, toonEase='out'),
            k(G14 - 0.1, clip='stand', blend=0.1, look='mec'), k(G14 + 0.06, toon={'hands': {'R': 'open'}, 'reach': {'R': [8.8, 1.3, -1.2, 0.6, 0.05]}}, toonDur=0.12), k(G14 + 0.24, clip='salute', blend=0.12)])],   # he lets go, and salutes
        props=[HOME(), ENV(E14a, keys=[k(0.0, to=E14b, dur=G14 - 0.1, ease='out'), k(G14, to=E14c, dur=0.14, ease='outBack')])],
        cams=[cam(0.0, [4.7, 1.7, -0.92], [4.85, 1.7, -0.92], [9.0, 1.6, -0.92], [9.0, 1.6, -0.92], lens=44),
              cam(CU14, [7.45, 1.9, -0.4], [7.5, 1.9, -0.4], [8.85, 1.88, -0.4], [8.85, 1.88, -0.4], lens=44)])   # close: the envelope under his eyes

# 15: the whole bill: the envelope grows at each word; he holds it over his head, his knees give; it comes down flat on him. Seen from above: the envelope
#     on the pavement, and in its window, where his name was, two eyes
W15 = [0.04, 0.22, 0.37]                             # « Toute », « la », « facture »
SC15, Y15 = [2.2, 4.4, 7.5], [1.95, 2.55, 3.3]        # its size and the height of its middle after each word (its lower edge stays in his hands)
F15, L15 = 0.56, 0.66                                # it tips; it lands
UP15 = lambda i, **kw: BOTH([E14c[0], Y15[i] - 0.105 * SC15[i], E14c[2]], 0.34 * min(SC15[i], 2.4), **kw)
PRESS15 = lambda i: {'sq': [1 + 0.07 * (i + 1), 1 - 0.1 * (i + 1), 1 + 0.07 * (i + 1)], 'face': {'gy': -1, 'eye': 0.15 * (i + 1), 'sweat': 1 if i else 0, 'mouth': 'wavy' if i else 'o'}}
st.shot('S15', 'parisStreet', setOpts=DAY, actors=[act('mec', H14, RY14, 'stand', 'surprised', keys=[k(-0.05, toon=BOTH(E14c), toonDur=0.0), k(0.0, look=None)] +
            [x for i in range(3) for x in (k(W15[i], toon=UP15(i, **PRESS15(i)), toonDur=0.07, toonEase='outBack'),)] +
            [k(W15[2] + 0.1, toon=UP15(2, sq=PRESS15(2)['sq'], face={'gy': 0.1, 'eye': 0.45, 'sweat': 1, 'mouth': 'wavy', 'brow': 0.8}), toonDur=0.03),   # a look at us, under it: three frames
             k(F15, toon=UP15(2, sq=[1.3, 0.6, 1.3], face={'gy': -1, 'eye': 0.5, 'mouth': 'scream', 'jaw': 0.6}), toonDur=0.08), k(L15 - 0.03, clip='pancake', params={'flat': 0.05}, blend=0.03), k(L15 - 0.03, toon={}, toonDur=0.03)])],
        props=[HOME(), ENV(E14c, eyes=[L15 + 0.07, 99], eyesOpen=0.05, blinks=[L15 + 0.36], keys=[x for i in range(3) for x in (k(W15[i], to=[E14c[0], Y15[i], E14c[2]], dur=0.07, ease='outBack'), k(W15[i], scale=SC15[i], dur=0.07, ease='outBack'), k(W15[i] + 0.07, squash=[1.12, 0.9, 1.0], dur=0.14))] +
                   [k(F15, to=[8.75, 0.16, E14c[2]], dur=round(L15 - F15, 3), ease='in'), k(F15, rotTo=[-1.5708, -1.5708, 0], dur=round(L15 - F15, 3), ease='in'), k(L15, squash=[1.06, 1.0, 1.06], dur=0.3)])],
        fx=[{'type': 'shake', 'at': L15, 'dur': 0.2, 'amount': 0.035}],
        cams=[cam(0.0, [5.6, 1.8, -0.4], [5.55, 1.8, -0.4], [9.0, 1.8, -0.4], [9.0, 1.8, -0.4], lens=44),
              glide([cam(W15[0], [3.6, 2.35, -0.4], [3.5, 2.35, -0.4], [9.0, 2.35, -0.4], [9.0, 2.35, -0.4], lens=44)], round(W15[2] - W15[0] + 0.07, 3)),   # it backs off as the envelope grows: the whole of it stays in the frame
              glide([cam(F15 - 0.02, [5.35, 6.1, -0.4], [5.4, 6.05, -0.4], [8.6, 0.2, -0.4], [8.6, 0.2, -0.4], lens=44)], round(L15 - F15 + 0.06, 3))])   # the camera goes up as it comes down: the envelope from above

# ---- the town hall
MAI = {'map': False, 'plate': False, 'deskX': -2.7, 'flagX': 3.6, 'clockX': 9}
MA16, H16 = [-0.62, 0, -0.5], [0.26, 0, -0.1]          # the mayor; him: at 60 % of the width, his head under the white of the sign (at the right edge his arm was cut by the frame and his head sat on the red of the band)
# 16: he asked for a raise: he comes in flat as a sheet, edge-on: a line that sways; he turns three quarters to us: a cardboard cut-out; a thumb in his
#     mouth, he blows: three puffs, each gives him back a third of his thickness, the last a little too much; then a palm held out to the mayor
T16, B16 = 0.56, 0.8                                 # he turns; the thumb is in his mouth (the line is held nine frames first)
PUFF16 = [[B16 + 0.06, 0.34], [B16 + 0.2, 0.7], [B16 + 0.34, 1.18], [B16 + 0.44, 1.0]]   # three puffs, a pop each, then he settles at his size
P16 = PUFF16[2][0]                                   # the last puff: the pop
BLOW = lambda **f: {'hands': {'R': 'thumbUp'}, 'touch': {'R': ['face', 0.0, 0.23, 0.03, 1, 0.08]}, 'face': {'puff': 1, 'mouth': 'o', 'brow': -0.4, **f}}
st.shot('S16', 'mairie', setOpts=MAI, actors=[act('mec', [1.55, 0, -0.1], -90, 'paperThin', 'unimpressed', keys=[k(0.0, look=None), k(0.0, clip='paperThin', params={'puffs': PUFF16, 'thin': 0.04, 'flutter': 3.4}, blend=0.0),
            k(0.0, to=H16, dur=0.26, glide=True, ease='out', face=-88), k(T16, to=H16, dur=0.16, glide=True, ease='inOut', face=-64), k(B16 + 0.02, to=H16, dur=0.4, glide=True, ease='inOut', face=-32),   # in on a draught, edge-on, toward the mayor; then he turns a little to us: a tall card that flutters; as he fills he comes round to us
            k(B16 - 0.08, toon={'hands': {'R': 'thumbUp'}, 'touch': {'R': ['face', 0.0, 0.23, 0.03, 1, 0.08]}}, toonDur=0.08)] +   # the thumb in his mouth
            [x for i, (t_, v) in enumerate(PUFF16[:3]) for x in (k(t_ - 0.03, toon=BLOW(lid=1), toonDur=0.03), k(t_ + 0.03, toon=BLOW(eye=0.2 + 0.1 * i), toonDur=0.05))] +   # he blows: his cheeks, his eyes shut at each puff
            [k(PUFF16[3][0], clip='stand', blend=0.1, expr='smug'), k(PUFF16[3][0] + 0.03, toon={'hands': {'L': 'open'}, 'reach': {'L': [H16[0] - 0.5, 1.32, 0.22, 1, 0.1]}, 'face': {'browL': 0.8, 'browR': 0.8, 'mouth': 'smile', 'gx': -0.9}}, toonDur=0.12, toonEase='outBack')] +
            [k(round(PUFF16[3][0] + 0.16 + 0.06 * i, 3), toon={'hands': {'L': 'rest' if i % 2 == 0 else 'open'}, 'reach': {'L': [H16[0] - 0.5, 1.32 + (0.03 if i % 2 == 0 else 0), 0.22, 1, 0.1]}, 'face': {'browL': 0.8, 'browR': 0.8, 'mouth': 'smile', 'gx': -0.9}}, toonDur=0.05) for i in range(2)]),   # the fingers curl and open, twice: come on (the palm held out stopped dead for a third of a second)   # the palm out: a raise (his face stays three quarters to us: a look at the mayor showed the side of his head)
        act('maire', MA16, 26, 'stand', 'neutral', keys=[k(0.0, look='mec'), k(T16 + 0.1, toon={'face': {'browL': 0.9, 'browR': -0.3}}, toonDur=0.1)] +
            [k(t_ + 0.02, toon={'sq': [1 - 0.02 * (i + 1), 1 + 0.03 * (i + 1), 1 - 0.02 * (i + 1)], 'bend': {'spine': [-0.05 * (i + 1), 0, 0, 1, None]}, 'face': {'eye': 0.12 * (i + 1), 'brow': 0.3 * (i + 1)}}, toonDur=0.06, toonEase='outBack') for i, (t_, v) in enumerate(PUFF16[:3])] +   # he leans back a little more at each puff
            [k(PUFF16[3][0] + 0.2, toon={'face': {'browTilt': -14, 'mouth': 'frown'}}, toonDur=0.12), k(PUFF16[3][0] + 0.2, clip='thinkChin', blend=0.2)])],
        cams=[cam(0.0, [-0.08, 1.62, 4.0], [-0.12, 1.62, 3.85], [-0.2, 1.55, -0.3], [-0.2, 1.55, -0.3], lens=44)])

# 17: he got a night bonus: the mayor brings a candle out from behind his back and puts it in his hand; then he takes the end of his tie, and pulls: the
#     night. A flame, his eyes over it; the mayor's eyes and his teeth
G17, P17 = 0.44, 0.76
H17 = [0.3, 0, -0.1]
C17a, C17b, C17c = [-0.88, 1.0, -0.72], [-0.24, 1.42, 0.1], [-0.02, 1.3, 0.22]   # the candle: behind the mayor's back, presented, in the hero's hand
CAND = lambda p_, **kw: {'hands': {'R': 'grip'}, 'reach': {'R': [p_[0] + 0.1, p_[1] + 0.02, p_[2], 1, 0.05]}, **kw}   # the mayor's right hand on the ring of the holder
TAKE17 = lambda w=1, **kw: {'hands': {'L': 'grip'}, 'reach': {'L': [C17c[0] + 0.1, C17c[1] + 0.02, C17c[2], w, 0.05]}, **kw}
TIE17 = lambda L: tie_tip(H17, -14, L, 0.2)
st.shot('S17', 'mairie', setOpts=MAI, actors=[act('mec', H17, -14, 'stand', 'smug', keys=[k(0.0, look=None), k(0.0, toon={'hands': {'L': 'open'}, 'reach': {'L': [H16[0] - 0.5, 1.32, 0.22, 1, 0.1]}, 'face': {'gx': -0.9, 'browL': 0.6}}, toonDur=0.0),   # (his face stays three quarters to us, his eyes on the mayor: turned to him, we saw his hair)
            k(G17 - 0.06, toon=TAKE17(), toonDur=0.1), k(G17 + 0.1, expr='unimpressed', look=None), k(G17 + 0.12, toon=TAKE17(face={'gy': 0.8}), toonDur=0.08),   # he has it; he looks at it
            k(P17 - 0.06, toon=TAKE17(tie=[1.7, 0.2, 0], bend={'spine': [0.25, 0, 0, 1, None], 'neck': [0.25, 0, 0, 0.8, None]}, sq=[1.05, 0.93, 1.05]), toonDur=0.06, toonEase='in'),
            k(P17 + 0.07, toon=TAKE17(tie=[0.85, 0.2, 0], bend={'neck': [-0.1, 0, 0, 1.25, None]}, sq=[0.96, 1.07, 0.96]), toonDur=0.07, toonEase='out'), k(P17 + 0.17, toon=TAKE17(tie=[1.05, 0.2, 0]), toonDur=0.1),
            k(P17 + 0.26, toon=TAKE17(), toonDur=0.08), k(P17 + 0.4, toon=TAKE17(face={'gy': 0.9}), toonDur=0.1), k(P17 + 0.62, toon=TAKE17(), toonDur=0.1)]),   # in the black: down to the flame, up to us
        act('maire', MA16, 26, 'stand', 'happy', keys=[k(0.0, look='mec'), k(0.0, toon=CAND(C17a), toonDur=0.0), k(0.1, toon=CAND(C17b, sq=[0.97, 1.05, 0.97]), toonDur=0.16, toonEase='outBack'),   # from behind his back: there
            k(G17 - 0.08, toon=CAND(C17c), toonDur=0.1), k(G17 + 0.08, toon={'hands': {'R': 'grip'}, 'reach': {'R': [*TIE17(1.0), 1, 0.05, [0.6, -0.6, 0.5]]}}, toonDur=0.2, toonEase='out'),   # into his hand; then the tie
            k(P17 - 0.06, toon={'hands': {'R': 'grip'}, 'reach': {'R': [*TIE17(1.7), 1, 0.05, [0.6, -0.6, 0.5]]}, 'bend': {'spine': [0.12, 0, 0, 1, None]}}, toonDur=0.06, toonEase='in'),
            k(P17 + 0.07, toon={'hands': {'R': 'grip'}, 'reach': {'R': [*TIE17(0.9), 1, 0.05, [0.6, -0.6, 0.5]]}, 'face': {'mouth': 'teeth', 'mouthW': 0.3}}, toonDur=0.07), k(P17 + 0.26, toon={'bend': {'spine': [0.34, -0.3, 0, 1.04, None], 'neck': [-0.2, 0, 0, 1, None]}, 'face': {'mouth': 'teeth', 'mouthW': 0.4, 'browL': 0.7, 'browR': 0.7}}, toonDur=0.22, toonEase='inOut'), k(P17 + 0.1, look=None)])],   # in the black he leans in over the flame: his grin, lit from below
        props=[P('candle', 'candle', pos=C17a, inDark=True, keys=[k(0.1, to=C17b, dur=0.16, ease='outBack'), k(G17 - 0.08, to=C17c, dur=0.1, ease='inOut')])],
        dark=[[0, 0, 0.001], [P17 + 0.02, 1]], darkFloor=0.035, darkEyes=1.6,
        darkPool={'prop': 'candle', 'lift': [0, 0.3, 0], 'r': 0.95, 'k': [[P17 + 0.02, 0.9, 0.04]], 'tint': '#FFC98A'},   # the flame lights a little round itself: the hand that holds it, his chin
        cams=[cam(0.0, [-0.15, 1.62, 3.3], [-0.15, 1.62, 3.15], [-0.2, 1.6, -0.2], [-0.2, 1.6, -0.2], lens=44)])

# ---- yesterday at noon: the pavement in front of his door, seen along the street: the sun stands over the far end of it
SUNP = [7.0, 24.0, -34.0]                            # high over the street, between the two heads: no ray ends on a hat
SUN = lambda **kw: P('sun', 'sunLamp', pos=SUNP, inDark=True, opts={'r': 3.4, **kw})
C18 = [8.7, 0.45, 6.0]                               # low on the pavement, looking up the street
T18 = [8.6, 3.3, -4.0]
H19, DOOR19 = [9.0, 0, 0.8], [9.7, 0, 0.8]           # where he stops, in the sun; where he comes out of
DA, E1, E2 = [7.95, 0, 0.45], [8.5, 0, -4.6], [7.7, 0, -6.0]   # passers-by, all facing up the street toward us: the lady beside him on the open side of the pavement, nearly level with him (her arm will cross the frame to him: from 1.2 m behind him it ran into depth, behind his back); the two others far down the street, in the gaps between heads (the man in the straw hat stood right behind his head: a head with a brim)
CROWD = lambda keys=None, dame=None: [act('dame', dame or DA, 14, 'stand', 'happy', keys=(keys or {}).get('dame', [k(0.0, look=None), k(0.3, toon={'face': {'gx': 0.8}}, toonDur=0.1), k(0.6, toon={'bend': {'spine': [0, -0.06, 0, 1, None]}, 'face': {'gx': 0.8, 'lid': 1}}, toonDur=0.05), k(0.68, toon={'bend': {'spine': [0, -0.06, 0, 1, None]}, 'face': {'gx': 0.8}}, toonDur=0.05)])),   # she shifts her weight, looks at his door, blinks
                           act('e1', [8.5, 0, -2.6], 180, 'walk', 'neutral', keys=[k(0.0, look=None), k(0.0, to=[8.4, 0, -4.4], dur=1.2, clip='walk', ease='linear')]),   # the two others walk away down the street (they stood stock-still through four shots)
                           act('e2', [7.7, 0, -4.2], 180, 'walk', 'happy', keys=[k(0.0, look=None), k(0.0, to=[7.6, 0, -6.4], dur=1.2, clip='walk', ease='linear')])]
DAY19 = {**DAY, 'clouds': 0}                          # the street of these shots: a clean sky round the sun (a cloud sat on a ray of the sun, and behind a head it read as a hat)
HOME19 = lambda **kw: P('home', 'door', pos=[9.93, 0, 0.8], ry=-90, opts={'w': 1.0, 'h': 2.3, 'color': '#2F6E5C', 'frame': '#EDE6D4', **kw})

# 18: yesterday at noon: the sun, with a face, over the end of the street; the camera comes down from it to the pavement: people, his door
st.shot('S18', 'parisStreet', setOpts=DAY19, actors=CROWD(), props=[SUN(), HOME19()], dark=LIT,
        cams=[cam(0.0, C18, C18, [7.6, 19.5, -30.0], T18, lens=44, ease='inOut')])

# 19: he stepped out of his house: the door opens, he comes out into the sun, stops, hands on his hips, one eye shut against the light, a big breath
O19 = 0.3
st.shot('S19', 'parisStreet', setOpts=DAY19, actors=[act('mec', DOOR19, -90, 'walk', 'happy', keys=[k(0.0, look=None), k(0.02, to=H19, dur=O19, clip='walk', ease='out', face=2),
            k(O19 + 0.04, clip='handsOnHips', blend=0.14), k(O19 + 0.1, toon={'bend': {'spine': [-0.14, 0, 0, 1.08, None]}, 'sq': [0.97, 1.05, 0.97], 'face': {'lidR': 1, 'lowL': 0.3, 'browR': -0.5, 'browL': 0.5, 'mouth': 'bigsmile', 'cheeks': 1, 'gy': -0.5}}, toonDur=0.16, toonEase='outBack'),   # the sun in his face
            k(O19 + 0.32, toon={'bend': {'spine': [-0.22, 0, 0, 1.1, None]}, 'sq': [1.1, 1.03, 1.14], 'face': {'lid': 1, 'brow': 0.5, 'mouth': 'o', 'cheeks': 1}}, toonDur=0.22, toonEase='inOut'),   # a big breath in: his chest out, his eyes shut
            k(O19 + 0.6, toon={'bend': {'spine': [0.08, 0, 0, 0.98, None]}, 'sq': [0.97, 0.98, 0.96], 'face': {'lidR': 1, 'lowL': 0.3, 'browR': -0.5, 'browL': 0.5, 'mouth': 'bigsmile', 'cheeks': 1}}, toonDur=0.14, toonEase='out'),   # and out: his shoulders come down
            k(O19 + 0.76, toon={'face': {'lidR': 1, 'lowL': 0.3, 'browR': -0.5, 'browL': 0.5, 'mouth': 'smile', 'cheeks': 1}}, toonDur=0.1)])],   # (he is alone in this close frame: a passer-by showed behind his elbow)
        props=[SUN(), HOME19(openAt=0.0)], dark=LIT,
        cams=[cam(0.0, [8.45, 1.7, 4.3], [8.5, 1.7, 4.1], [9.0, 1.72, 0.8], [9.0, 1.72, 0.8], lens=44)])

# 20: by reflex: he looks up at the birds, whistling (notes in the sky); his right hand walks up his chest to the tie, finger by finger, and closes on it;
#     beside him the lady sees it: she shrinks under her hat, which jumps off her head; her arm shoots out across the frame and lands on his wrist; the
#     hat comes back down, late; she trembles
STEP20 = [0.08, 0.2, 0.32]                           # his hand climbs
GR20, NO20 = 0.44, 0.5                               # it closes on the tie; the lady's arm
TT20 = tie_tip(H19, 2, 1.0, 0.15)
WH20 = {'gx': 0.7, 'gy': -0.8, 'mouth': 'whistle', 'mouthW': 0.7, 'mouthH': 0.7, 'brow': 0.3}   # whistling at the sky
CLIMB = lambda i: {'hands': {'R': 'two'}, 'reach': {'R': [TT20[0] + 0.02, round(0.98 + 0.07 * i, 3), TT20[2] + 0.04, 1, 0.08, [-0.7, -0.4, 0.4]]}, 'face': WH20}
ONTIE = lambda L=1.0, **kw: {'hands': {'R': 'grip'}, 'reach': {'R': [*tie_tip(H19, 2, L, 0.15), 1, 0.05, [-0.7, -0.4, 0.4]]}, 'tie': [L, 0.15, 0], **kw}
WRIST20 = [round(TT20[0] - 0.13, 3), round(TT20[1] + 0.03, 3), round(TT20[2] + 0.05, 3)]   # his wrist, on the tie: where her hand lands
FACE20 = {'eye': 0.5, 'brow': 1.0, 'mouth': 'O', 'mouthH': 0.5, 'gx': 0.9}   # her face: eyes as big as they go, on her face (no stalks: that was the electrician's take)
STOP20 = lambda hat=0.0, nod=0.0, **kw: {'hands': {'L': 'spread'}, 'reach': {'L': [WRIST20[0], WRIST20[1], WRIST20[2], 1, 0.1, [0, 1, 0.3]]}, 'bend': {'spine': [0.06, -0.22, 0, 1, None], 'neck': [0, nod, 0, 1, None]}, 'hat': [hat, 0, 0], 'face': {**FACE20, 'gy': 0.4}, **kw}   # her arm across the frame, she leans after it
C20 = lambda t=0.0: cam(t, [8.58, 1.6, 5.2], [8.6, 1.6, 5.0], [8.6, 1.62, 0.6], [8.6, 1.62, 0.6], lens=44)   # the two of them side by side: her arm crosses the picture
st.shot('S20', 'parisStreet', setOpts=DAY19, actors=[act('mec', H19, 2, 'stand', 'happy', keys=[k(0.0, look=None), k(0.0, toon={'face': WH20}, toonDur=0.0)] +
            [k(t_, toon=CLIMB(i), toonDur=0.07, toonEase='outBack') for i, t_ in enumerate(STEP20)] +
            [k(GR20, toon=ONTIE(1.0, face=WH20), toonDur=0.07, toonEase='out')]),   # on the tie; he has not even looked
        act('dame', DA, 14, 'stand', 'happy', keys=[k(0.0, look=None), k(0.0, toon={'face': {'gx': 0.9}}, toonDur=0.0), k(GR20 - 0.1, toon={'face': {'gx': 0.9, 'gy': 0.5, 'eye': 0.2}}, toonDur=0.05), k(GR20 - 0.05, expr='shocked'),   # her eyes go to his hand
            k(GR20 - 0.05, toon={'sq': [1.24, 0.66, 1.24], 'hat': [0.5, 0.25, 0], 'face': {**FACE20, 'gy': 0.5}}, toonDur=0.05, toonEase='outBack'),   # the take: she shrinks under her hat, which stays up there
            k(NO20, toon=STOP20(0.42, sq=[0.95, 1.07, 0.95], wave=RIP('L', 0.1, 0.8, 1.5)), toonDur=0.07, toonEase='out'),   # NON: an arm across the picture, onto his wrist
            k(NO20 + 0.12, toon=STOP20(0.0, sq=[1.06, 0.93, 1.06], wave=RIP('L', 0.035, 1.6, 1.5)), toonDur=0.08, toonEase='in'),   # the hat lands, late: she gives under it
            k(NO20 + 0.19, toon=STOP20(0.03, 0.06), toonDur=0.05), k(NO20 + 0.25, toon=STOP20(0.0, -0.06), toonDur=0.05), k(NO20 + 0.31, toon=STOP20(0.03, 0.05, face={**FACE20, 'gy': 0.0}), toonDur=0.05)])],   # she trembles, her hat hops; her eyes come up from his hand to his face
        props=[SUN(), HOME19(), P('notes', 'whistleNotes', pos=[H19[0] - 0.02, 2.28, H19[2] + 0.25], opts={'n': 3, 'from': 0.0, 'every': 0.13, 'size': 0.27, 'dx': -0.5, 'dy': 0.8, 'life': 0.6, 'color': '#FFF6DC'})], dark=LIT,   # cream notes, up into the sky between the two heads (dark ones on the shop front did not show)
        cams=[C20()])

# 21: he turned off: the street, the sun over it, frightened; the tie: click: black; the sun goes out like a bulb, its filament dies, its eyes shut;
#     in the black: his eyes go up to where it was; hers go to him
P21 = 0.24
st.shot('S21', 'parisStreet', setOpts=DAY19, actors=[act('mec', H19, 2, 'stand', 'happy', keys=[k(-0.05, toon=ONTIE(1.0, face=WH20), toonDur=0.0), k(0.0, look=None),
            k(P21 - 0.06, toon=ONTIE(1.7, bend={'spine': [0.25, 0, 0, 1, None], 'neck': [0.25, 0, 0, 0.8, None]}, sq=[1.05, 0.93, 1.05]), toonDur=0.06, toonEase='in'),
            k(P21 + 0.07, toon=ONTIE(0.85, bend={'neck': [-0.1, 0, 0, 1.25, None]}, sq=[0.96, 1.07, 0.96]), toonDur=0.07, toonEase='out'), k(P21 + 0.17, toon=ONTIE(1.05), toonDur=0.1), k(P21 + 0.26, toon=ONTIE(1.0), toonDur=0.08),
            k(P21 + 0.2, expr='surprised'), k(P21 + 0.36, toon=ONTIE(1.0, face={'gy': -1, 'eye': 0.3}), toonDur=0.08)]),   # in the black his eyes go up, to where the sun was
        act('dame', DA, 14, 'stand', 'shocked', keys=[k(0.0, look=None), k(-0.05, toon=STOP20(0.0, 0.05, face={**FACE20, 'gy': 0.0}), toonDur=0.0), k(0.04, toon=STOP20(0.03, -0.06, face={**FACE20, 'gy': 0.0}), toonDur=0.05), k(0.1, toon=STOP20(0.0, 0.06, face={**FACE20, 'gy': 0.0}), toonDur=0.05), k(0.16, toon=STOP20(0.03, -0.05, face={**FACE20, 'gy': 0.0}), toonDur=0.05),   # she still trembles
            k(P21 + 0.14, expr='scared'), k(P21 + 0.14, toon={'face': {'gx': 0.9, 'gy': -0.6, 'eye': 0.3}}, toonDur=0.12),   # in the black: her eyes, up at where the sun was,
            k(P21 + 0.4, toon={'face': {'gx': 1.0, 'lid': 0.85}}, toonDur=0.08)])],   # then on him, narrowed
        props=[SUN(scareAt=0.0, offAt=P21 + 0.03), HOME19()],
        dark=[[0, 0, 0.001], [P21 + 0.02, 1]], darkFloor=0.03, darkEyes=4.6,   # (the camera is low and far: at 3 their eyes were 3 % of the frame)
        cams=[cam(0.0, C18, [8.7, 0.45, 5.8], T18, T18, lens=44)])

# 22: it has been night since: black; his eyes, alone, at the left of the frame; then pair after pair of eyes opens round him: at two windows, on the
#     pavement, a cat's: a wave that leaves him; they all narrow, on him; his look left, his look right; he tiptoes out of the picture, three dips of his
#     eyes, and every pupil goes with him. (v1: three pairs under reading size, one of them a hand from his own: a face with four eyes)
H22, C22 = [8.0, 0, -2.2], [8.6, 1.95, 3.8]          # him, six metres from the camera, BEHIND the other pairs (at three metres his black body hid the pairs at his feet); the camera of this shot (its own: in the black nobody knows where anybody stood)
HIM22 = (0.28, 0.43)                                 # where his eyes are in the frame (u, v: 0..1, v down)
L22, G22 = 0.42, 0.72                                # his pupils start across the crowd; he goes
def at22(u, v, d=5.0):                               # the place in the world of the point (u, v) of the frame, d metres in front of the camera
    return r3([C22[0] + (u - 0.5) * 0.4545 * d, C22[1] - 0.0132 * d - (v - 0.5) * 0.808 * d, C22[2] - d])
def EYES22(i, u, v, sz, open_, **kw):                # a pair of eyes at (u, v): it opens, looks ahead; at 0.36 s its pupils snap to him and its lids come down; then they follow him out
    lk = lambda hu, hv: (round(max(-1, min(1, (hu - u) / 0.3)), 2), round(max(-1, min(1, (v - hv) / 0.22)), 2))
    a, b, c = lk(*HIM22), lk(0.08, 0.52), lk(-0.3, 0.52)
    return P(f'eyes{i}', 'eyesPair', pos=at22(u, v), inDark=True, opts={'s': sz, 'openAt': open_, 'narrow': [[0.36, 0], [0.44, 0.42]],
             'look': [[0.36, 0], [0.42, a[0]], [G22, a[0]], [G22 + 0.2, b[0]], [G22 + 0.4, c[0]]], 'lookY': [[0.36, 0], [0.42, a[1]], [G22, a[1]], [G22 + 0.2, b[1]], [G22 + 0.4, c[1]]], 'color': '#CBD5E6', **kw})   # (a cool, slightly dimmer white: his cream pair stays the brightest thing in the frame)
WIN22 = {'tall': 1.0, 'gap': 1.2, 'frame': [0.46, 0.38]}   # somebody at a window: round eyes (the rule of S03, S15, S25)
PAIRS22 = [EYES22(1, 0.58, 0.48, 0.062, 0.05, tall=1.3), EYES22(2, 0.16, 0.69, 0.07, 0.07, tall=1.3, blinks=[0.57]), EYES22(3, 0.60, 0.335, 0.055, 0.10, **WIN22), EYES22(4, 0.56, 0.71, 0.066, 0.12),
           EYES22(5, 0.71, 0.60, 0.06, 0.15, **{'tall': 0.85, 'slit': True, 'color': '#D9E86B'}), EYES22(6, 0.37, 0.725, 0.056, 0.17, tall=1.1), EYES22(7, 0.84, 0.49, 0.058, 0.20, tall=1.15, blinks=[0.52]),
           EYES22(8, 0.86, 0.335, 0.055, 0.24, **WIN22), EYES22(9, 0.85, 0.705, 0.058, 0.28, tall=1.2)]
STEPS22 = [(round(H22[0] - 0.5 * (i + 1), 3), round(G22 + 0.2 * i, 3)) for i in range(2)]   # two long steps on tiptoe: (where, when) (three were a scurry)
SNEAK22 = lambda sy, **f: {'sq': [1.0, sy, 1.0], 'auto': 0, 'face': {'gx': -0.9, 'lid': 0.68, **f}}   # (auto 0: the rig's own drag and squash, fed by these quick steps, laid him on his side)
st.shot('S22', 'parisStreet', setOpts=DAY, actors=[act('mec', H22, 2, 'stand', 'surprised', keys=[k(0.0, look=None), k(-0.05, toon={'face': {'gy': -1, 'eye': 0.3}}, toonDur=0.0), k(0.04, toon={'face': {'eye': 0.3}}, toonDur=0.06),   # his eyes come down from where the sun was
            k(0.12, toon={'face': {'gx': 0.9, 'eye': 0.35}}, toonDur=0.04), k(0.24, toon={'face': {'gx': 0.5, 'gy': 0.8, 'eye': 0.4}}, toonDur=0.04), k(0.36, toon={'face': {'eye': 0.5}}, toonDur=0.05),   # a pair on his right; one at his feet; all of them: his eyes as big as they go
            k(L22 - 0.04, toon={'face': {'gx': -0.9, 'eye': 0.4}}, toonDur=0.04), k(L22, toon={'face': {'gx': 1.0, 'eye': 0.4}}, toonDur=0.26, toonEase='inOut'),   # one slow slide of his pupils, from the way out across all of them: eight frames (two looks of three frames each were a flicker)
            k(G22 - 0.03, toon=SNEAK22(0.94), toonDur=0.04), k(G22, expr='sneaky')] +   # and he goes: eyes half shut, to the left, a little lower
            [x for (x_, t_) in STEPS22 for x in (k(t_, to=[x_, 0, H22[2]], dur=0.14, glide=True, ease='inOut', face='keep'), k(t_, toon=SNEAK22(0.76), toonDur=0.07, toonEase='out'), k(round(t_ + 0.09, 3), toon=SNEAK22(0.93), toonDur=0.1, toonEase='inOut'))])],   # each step: he slides a pace, his eyes dip and come back up
        props=PAIRS22,
        dark=[[0, 1, 0.001]], darkFloor=0.0, darkEyes=5.2,   # (he is far: his eyes at this size are a tenth of the frame each, like the others' twice over)
        cams=[cam(0.0, [C22[0], C22[1], C22[2] + 0.1], [C22[0], C22[1], C22[2] - 0.1], [C22[0], 1.9, 0.0], [C22[0], 1.9, 0.0], lens=44)])

# 23: the astronomers are looking: black; one eye at the eyepiece of a brass telescope (the other shut); the tube draws out, and out, up across the frame;
#     nothing; a blink; he steps back: two eyes, one bigger; he raises a torch and sweeps the sky with it.
#     (v1: the eyepiece hung a third of the frame under his eye, the tube crossed the caption band, the beam lay over his own face)
AS, RA = [-0.45, 0, 0.0], 45                         # the astronomer, three quarters to us, turned to the tube
EYE23 = face_pt(AS, RA, 0.079, 0.54, 0.1)            # his left eye (the low one, at the right of the picture: `R` in the face channels): the one at the eyepiece
TL, TT, TR = 0.75, 40, 78                            # the telescope: the length of one draw (drawn out, its far end leaves the frame), its tilt, its heading (across the frame, a little toward us: the lens shows)
ax23 = lambda d_: [d_ * math.cos(math.radians(TT)) * math.sin(math.radians(TR)), d_ * math.sin(math.radians(TT)), d_ * math.cos(math.radians(TT)) * math.cos(math.radians(TR))]
PIV23 = r3([EYE23[i] + ax23(0.06 + TL / 2 + 0.1)[i] for i in range(3)])   # its pivot: the end of the eyepiece is 6 cm in front of his eye
X23, S23, B23 = [[0.1, 0], [0.26, 0.5], [0.32, 0.5], [0.48, 1.0]], 0.64, 0.84   # the draws; he steps back; the torch
BACK23 = [AS[0] - 0.08, 0, AS[2] + 0.05]             # where he steps back to
TORCH = [BACK23[0] + 0.2, 2.5, 0.32]                 # the torch, in his left hand, held up over his head: the beam goes up into the empty sky between him and the tube (in his right hand, at his side, it stood at the left edge of the frame and its beam left it)
st.shot('S23', 'spaceDark', setOpts={'stars': 0}, lighting='night', actors=[act('astro', AS, RA, 'stand', 'determined', keys=[k(0.0, look=None), k(0.0, toon={'face': {'lidL': 1, 'eyeR': 0.4, 'gx': 0.5, 'gy': -0.5}}, toonDur=0.0),   # at the eyepiece: one eye (the other shut)
            k(0.28, toon={'face': {'lidL': 1, 'eyeR': 0.5, 'gx': 0.7, 'gy': -0.6}}, toonDur=0.06), k(0.5, toon={'face': {'lidL': 1, 'eyeR': 0.5, 'gx': 0.2, 'gy': -0.2}}, toonDur=0.06),   # it searches; nothing
            k(0.55, toon={'face': {'lid': 1}}, toonDur=0.03), k(0.61, toon={'face': {'lidL': 1, 'eyeR': 0.5}}, toonDur=0.03),   # a blink
            k(S23, to=BACK23, dur=0.1, glide=True, ease='out', face=6), k(S23, expr='confused'), k(S23, toon={'sq': [0.96, 1.05, 0.96], 'face': {'eyeL': 0.5, 'eyeR': 0.1}}, toonDur=0.1, toonEase='outBack'),   # he steps back, to us: two eyes, one bigger than the other
            k(B23 - 0.1, toon={'hands': {'L': 'grip'}, 'reach': {'L': [*TORCH, 1, 0.05]}, 'face': {'gy': -0.9, 'gx': -0.5, 'eyeL': 0.3, 'eyeR': 0.3}}, toonDur=0.12, toonEase='out'),   # the torch, up at the sky
            k(B23 + 0.2, toon={'hands': {'L': 'grip'}, 'reach': {'L': [*TORCH, 1, 0.05]}, 'face': {'gy': -0.9, 'gx': 0.3, 'eyeL': 0.3, 'eyeR': 0.3}}, toonDur=0.16, toonEase='inOut'),   # his eyes go with the beam
            k(B23 + 0.4, toon={'hands': {'L': 'grip'}, 'reach': {'L': [*TORCH, 1, 0.05]}, 'face': {'gy': -0.9, 'gx': -0.6, 'eyeL': 0.3, 'eyeR': 0.3}}, toonDur=0.16, toonEase='inOut')])],
        props=[P('tel', 'telescope', pos=[PIV23[0], 0, PIV23[2]], ry=TR, inDark=True, opts={'extend': X23, 'tilt': TT, 'len': TL, 'h': PIV23[1]}),
               P('beam', 'torchBeam', pos=[TORCH[0], TORCH[1] + 0.1, TORCH[2]], ry=0, inDark=True, opts={'flat': True, 'len': 6.5, 'r': 1.0, 'sweep': [[B23, -24], [B23 + 0.2, 6], [B23 + 0.4, -28], [B23 + 0.58, -8]]}, keys=[k(0.0, visible=False), k(B23, visible=True)])],
        dark=[[0, 1, 0.001]], darkFloor=0.03, darkEyes=2.6,
        cams=[cam(0.0, [0.0, 1.9, 4.9], [0.0, 1.95, 4.75], [0.0, 2.3, 0.0], [0.0, 2.3, 0.0], lens=44)])

# 24: the bill: black; from the right an envelope as wide as a man is tall comes on, bobbing: the postman carries it over his head; the hero's eyes watch it come
H24 = [8.9, 0, 0.0]
EV24 = lambda keys, **kw: P('env', 'bigEnvelope', pos=[11.2, 2.3, 0.4], ry=0, inDark=True, scale=1.0, opts={'w': 1.25, 'title': 'ÉLECTRICITÉ', 'to': 'LE SOLEIL', 'line2': 'CHEZ CE MEC', **kw}, keys=keys)
WALK24 = [k(0.0, to=[10.55, 2.36, 0.4], dur=0.22, ease='linear'), k(0.22, to=[10.0, 2.28, 0.4], dur=0.22, ease='linear'), k(0.44, to=[9.5, 2.36, 0.4], dur=0.22, ease='linear'), k(0.66, to=[9.1, 2.3, 0.4], dur=0.22, ease='out')]
st.shot('S24', 'parisStreet', setOpts=DAY, actors=[act('mec', H24, 2, 'stand', 'surprised', keys=[k(0.0, look=None), k(0.1, toon={'face': {'gx': 0.9}}, toonDur=0.08), k(0.5, toon={'face': {'gx': 0.7, 'eye': 0.4}}, toonDur=0.1), k(0.85, toon={'face': {'eye': 0.5, 'gy': -0.3}}, toonDur=0.08)]),
        act('fact', [11.2, 0, -0.1], 0, 'holdUp', 'strain', darkEyes=False, keys=[k(0.0, look=None), k(0.0, to=[9.1, 0, -0.1], dur=0.88, clip='holdUp', ease='linear', face=0)])],
        props=[EV24(WALK24)],
        dark=[[0, 1, 0.001]], darkFloor=0.03, darkEyes=2.6,
        cams=[cam(0.0, [9.3, 2.05, 3.7], [8.95, 2.05, 3.6], [9.4, 2.1, 0.0], [8.95, 2.1, 0.0], lens=44, ease='inOut')])   # the camera comes left with the envelope and ends where the next shot starts

# 25: it has already arrived: the envelope stops in front of him: his eyes are gone behind it; then, in its window, where the name is: two eyes; a blink;
#     a look left, a look right; they stay
A25 = 0.3
st.shot('S25', 'parisStreet', setOpts=DAY, actors=[act('mec', H24, 2, 'stand', 'surprised', keys=[k(0.0, look=None), k(0.0, toon={'face': {'eye': 0.5, 'gy': -0.3}}, toonDur=0.0)]),
        act('fact', [9.1, 0, -0.1], 0, 'holdUp', 'strain', darkEyes=False, keys=[k(0.0, look=None), k(0.0, to=[8.9, 0, -0.35], dur=A25, clip='holdUp', ease='out', face=0), k(A25 + 0.3, expr='happy')])],
        props=[P('env', 'bigEnvelope', pos=[9.1, 2.3, 0.4], ry=0, inDark=True, opts={'w': 1.25, 'title': 'ÉLECTRICITÉ', 'to': 'LE SOLEIL', 'line2': 'CHEZ CE MEC', 'eyes': [A25 + 0.36, 99], 'blinks': [A25 + 0.52, A25 + 1.72], 'eyeLook': [[A25 + 0.7, 0], [A25 + 0.78, -1], [A25 + 1.04, -1], [A25 + 1.14, 1], [A25 + 1.4, 1], [A25 + 1.5, 0]]},   # a blink; to the left end of the window, eight frames; to the right end, eight frames; back to us; a late blink
                 keys=[k(0.0, to=[8.84, 2.3, 0.4], dur=A25, ease='out'), k(A25, squash=[1.06, 0.92, 1.0], dur=0.3)])],
        dark=[[0, 1, 0.001]], darkFloor=0.0, darkEyes=2.6,
        cams=[cam(0.0, [8.95, 2.05, 3.6], [8.84, 2.1, 3.45], [8.95, 2.1, 0.0], [8.84, 2.12, 0.0], lens=44, ease='out')])   # the envelope whole in the frame from the first image (the camera lagged behind it and cut its left end)

st.cue('sfx:stretch', 'S01', B1, 0.35); st.cue('sfx:click', 'S01', K1, 0.6); st.cue('sfx:slideDown', 'S01', K1 + 0.03, 0.3)
st.cue('sfx:stepSoft', 'S02', 0.04, 0.3); st.cue('sfx:stepSoft', 'S02', 0.2, 0.3); st.cue('sfx:bonk', 'S02', G2, 0.6); st.cue('sfx:squeak', 'S02', G2 + 0.25, 0.35)
st.cue('sfx:slideDown', 'S03', 0.15, 0.4); st.cue('pop', 'S03', 0.15 + 0.45 + 0.22, 0.5)
st.cue('sfx:click', 'S04', K4, 0.6); st.cue('sfx:zip', 'S04', K4 + 0.1, 0.3)
st.cue('sfx:slideUp', 'S05', 0.1, 0.4); st.cue('sfx:click', 'S05', 0.68, 0.45); st.cue('sfx:click', 'S05', 0.86, 0.45)
st.cue('sfx:stepRun', 'S06', 0.0, 0.4); st.cue('sfx:brake', 'S06', 0.24, 0.35)
st.cue('sfx:clink', 'S07', CL7, 0.5); st.cue('sfx:static', 'S07', ND7, 0.45); st.cue('sfx:boing', 'S07', ND7 + 0.06, 0.3); st.cue('sfx:poof', 'S07', ND7 + 0.28, 0.3)
st.cue('sfx:twang', 'S08', P8a - 0.05, 0.4); st.cue('sfx:click', 'S08', P8a, 0.6); st.cue('sfx:twang', 'S08', P8b - 0.05, 0.4); st.cue('sfx:click', 'S08', P8b, 0.6)
st.cue('sfx:stretch', 'S09', 0.05, 0.25); st.cue('whoosh', 'S09', SL9 - 0.08, 0.3, 0.1, 700, 2600); st.cue('clack', 'S09', SL9, 0.6); st.cue('sfx:boing', 'S09', SL9 + 0.1, 0.3)
st.cue('sfx:ding', 'S10', F10, 0.45); st.cue('sfx:stretch', 'S10', F10 + 0.1, 0.3)
st.cue('sfx:twang', 'S11', P11 - 0.05, 0.4); st.cue('sfx:click', 'S11', P11, 0.6); st.cue('sfx:slideDown', 'S11', P11 + 0.03, 0.4); st.cue('pop', 'S11', P11 + 0.02 + 0.5 + 0.26, 0.5)
st.cue('sfx:stepSoft', 'S12', 0.05, 0.25); st.cue('sfx:stepSoft', 'S12', 0.3, 0.25); st.cue('sfx:tick', 'S12', M12 - 0.04, 0.5); st.cue('sfx:gasp', 'S12', M12 + 0.03, 0.3); st.cue('sfx:ding', 'S12', M12 + 0.24, 0.3); st.cue('sfx:poof', 'S12', O12 - 0.02, 0.3)
st.cue('pop', 'S13', KISS, 0.45); st.cue('sfx:gulp', 'S13', T13, 0.4); st.cue('pop', 'S13', T13 + 0.3, 0.2); st.cue('sfx:slideDownSlow', 'S13', T13 + 0.32, 0.3)
st.cue('sfx:step', 'S14', 0.05, 0.3); st.cue('sfx:step', 'S14', 0.28, 0.3); st.cue('sfx:paper', 'S14', G14, 0.45)
for i_ in range(3): st.cue('sfx:boing', 'S15', W15[i_], 0.3 + 0.08 * i_)
st.cue('whoosh', 'S15', F15, 0.35, 0.12, 300, 1500); st.cue('thud', 'S15', L15, 0.7); st.cue('sfx:paper', 'S15', L15 + 0.02, 0.5)
st.cue('sfx:paper', 'S16', 0.05, 0.35); st.cue('pop', 'S16', PUFF16[0][0], 0.25); st.cue('pop', 'S16', PUFF16[1][0], 0.32); st.cue('pop', 'S16', P16, 0.55); st.cue('sfx:boing', 'S16', P16 + 0.04, 0.3)
st.cue('sfx:twang', 'S17', P17 - 0.05, 0.4); st.cue('sfx:click', 'S17', P17, 0.6)
st.cue('sfx:bell', 'S18', 0.05, 0.35); st.cue('sfx:whistle', 'S18', 0.4, 0.2)
st.cue('sfx:carDoor', 'S19', 0.0, 0.3); st.cue('sfx:step', 'S19', 0.1, 0.3); st.cue('sfx:step', 'S19', 0.24, 0.3)
st.cue('sfx:whistle', 'S20', 0.02, 0.3)
for t_ in STEP20: st.cue('sfx:tick', 'S20', t_, 0.4)
st.cue('sfx:gasp', 'S20', GR20 - 0.05, 0.45); st.cue('sfx:stretch', 'S20', NO20, 0.4)
st.cue('sfx:twang', 'S21', P21 - 0.05, 0.4); st.cue('sfx:click', 'S21', P21, 0.7); st.cue('sfx:slideDown', 'S21', P21 + 0.04, 0.5)
for i_, t_ in enumerate([0.05, 0.1, 0.15, 0.2, 0.28]): st.cue('pop', 'S22', t_, 0.16 + 0.03 * i_)
st.cue('sfx:gulp', 'S22', 0.38, 0.4)
for x_, t_ in STEPS22: st.cue('sfx:stepSoft', 'S22', t_, 0.3)
st.cue('sfx:slideUp', 'S23', 0.1, 0.35); st.cue('sfx:slideUp', 'S23', 0.32, 0.35); st.cue('sfx:click', 'S23', B23, 0.4)
st.cue('sfx:stepHeavy', 'S24', 0.05, 0.3); st.cue('sfx:stepHeavy', 'S24', 0.3, 0.3); st.cue('sfx:stepHeavy', 'S24', 0.55, 0.3); st.cue('sfx:grunt', 'S24', 0.4, 0.3)
st.cue('sfx:paper', 'S25', A25, 0.55); st.cue('sfx:ding', 'S25', A25 + 0.36, 0.4)

CITIZEN = lambda preset, seed, **kw: {'preset': preset, 'seed': seed, 'build': {'width': 0.86, 'headWidth': 1.3, **kw.pop('build', {})}, **kw}
st.card('S22', 'IL FAIT NUIT DEPUIS')
st.write("L'interrupteur", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, extra_cast={
    'maire': {'preset': 'politique', 'sash': ['#2A4B9B', '#F4F1E8', '#C8202A'], 'sashW': 0.12, 'hair': 'combover', 'hairColor': '#B8B4AA', 'facial': 'mustache', 'beardColor': '#B8B4AA', 'glasses': False, 'seed': 13, 'skin': '#E6BE98', 'build': {'width': 0.96, 'headWidth': 1.3}},
    'elec': CITIZEN('worker', 83, glasses=False, suit='#3A6EA5', facial='mustache'),
    'b1': CITIZEN('pyjama', 85, suit='#1D1D22', pants='#1D1D22', hat='beanie', hatColor='#1D1D22', facial='stubble', build={'height': 0.9, 'width': 1.0}),
    'b2': CITIZEN('pyjama', 87, suit='#1D1D22', pants='#1D1D22', hat='beanie', hatColor='#1D1D22', facial='mustache', build={'height': 1.06, 'width': 0.8}),
    'la': CITIZEN('femme', 89, suit='#B5486A'), 'lb': CITIZEN('lyceen', 91, suit='#3F7A5A', build={'height': 1.0}),
    'fact': CITIZEN('officiel', 93, suit='#2B4C8C', tie='#F2C230', hat='copcap', hatColor='#2B4C8C', glasses=False),
    'dame': CITIZEN('madame', 95, suit='#C8553D'), 'e1': CITIZEN('fermier', 97), 'e2': CITIZEN('gamin', 99), 'astro': CITIZEN('savant', 101)})
